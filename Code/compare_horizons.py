"""Compare every model across forecast horizons.

compare_models.py answers "which model is best?" at one horizon. This answers
the prior question: "at what horizon does the choice of model start to matter?"
At one week ahead it does not -- next week's ILI is almost this week's, and
every model lands within noise of persistence. The interesting quantity is how
that gap opens as the horizon grows.

Three things come out of that framing:

  * **The error-growth curve.** RMSE against horizon, per model.
  * **Skill against the seasonal floor.** RMSE divided by seasonal_naive's. 1.0
    is the floor. A model that hugs 1.0 at every horizon has learned nothing a
    calendar does not already know, however good its raw RMSE looks.
  * **The spread.** Standard deviation of RMSE across models at each horizon. If
    that does not grow, the harder question did not actually separate them and
    the whole exercise is negative -- which is worth reporting as such.

Reads the per-horizon trees written by run_all_horizons.py:

    python Code/compare_horizons.py
    python Code/compare_horizons.py --models arima,lstm,dualtopo,gnn_st
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas numpy matplotlib.") from exc

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import palette, paths
from influenza.cities import get as get_city
from influenza.cli import add_city_arg, city_results_dir
from influenza.metrics import CORE_METRICS

# The two naive models are the floors every other model is judged against, not
# peers competing for a categorical slot -- exactly how plot_forecasts.py treats
# the observed series. Drawing them in ink also frees all four validated colour
# slots for models that are actually trying.
REFERENCE_STYLES = {
    "persistence": {"color": palette.INK_MUTED, "linestyle": ":", "linewidth": 1.6},
    "seasonal_naive": {"color": palette.INK_SECONDARY, "linestyle": "--", "linewidth": 1.6},
}
DEFAULT_MODELS = "arima,lstm,dualtopo,gnn_st"


def discover(results_root: Path) -> list[tuple[int, Path]]:
    """Every (horizon, metrics.csv) under results/horizon_*/<model>/<variant>/."""
    found: list[tuple[int, Path]] = []
    for horizon_root in sorted(results_root.glob("horizon_*")):
        if not horizon_root.is_dir():
            continue
        try:
            horizon = int(horizon_root.name.split("_")[1])
        except (IndexError, ValueError):
            print(f"warning: skipping {horizon_root.name}, not a horizon_NN directory",
                  file=sys.stderr)
            continue
        for path in sorted(horizon_root.glob("*/*/metrics.csv")):
            if any(part.startswith("_") for part in path.relative_to(horizon_root).parts):
                continue
            found.append((horizon, path))
    return found


def load_one(horizon: int, path: Path) -> pd.DataFrame | None:
    """One run's metrics, with the provenance a cross-horizon read needs.

    The directory name is authoritative for the horizon; the metrics column is
    cross-checked against it, because a mismatch means the run was written with
    a different --horizons than its directory claims and every row is suspect.
    """
    frame = pd.read_csv(path)
    if "segment" not in frame.columns:
        print(f"warning: {path} has no 'segment' column (pre-refactor); skipping",
              file=sys.stderr)
        return None

    recorded = sorted(int(h) for h in frame["horizon"].unique())
    if recorded != [horizon]:
        print(f"warning: {path.parent} sits under horizon_{horizon:02d} but its metrics "
              f"record horizons {recorded}; skipping", file=sys.stderr)
        return None

    model, variant = path.parent.parent.name, path.parent.name
    frame["model"] = frame.get("model", pd.Series(dtype=str)).fillna(model)
    frame["variant"] = frame.get("variant", pd.Series(dtype=str)).fillna(variant)
    frame["horizon"] = horizon

    meta = {"target_kind": None, "normalize": None, "n_params": None,
            "fallback_forecasts": None, "fallback_share": None,
            "test_interval_coverage": None, "lookback": None, "n_train": None}
    config_path = path.parent / "run_config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        window = config.get("window") or config.get("experiment", {}).get("window", {})
        split = config.get("split", {})
        for key in meta:
            meta[key] = config.get(key)
        meta["lookback"] = window.get("lookback")
        meta["n_train"] = split.get("n_train")
    for key, value in meta.items():
        frame[key] = value
    return frame


def build_long(frames: list[pd.DataFrame], scope: str) -> pd.DataFrame:
    # Runs differ in which provenance columns they carry (only ARIMA has
    # fallback_forecasts), and a column of all-None is an object column whose
    # concat dtype handling is deprecated. Drop those per frame, then align on
    # the union so the missing ones come back as proper float NaN.
    frames = [frame.dropna(axis=1, how="all") for frame in frames]
    columns = list(dict.fromkeys(c for frame in frames for c in frame.columns))
    frames = [frame.reindex(columns=columns) for frame in frames]
    long = pd.concat(frames, ignore_index=True)
    long = long.loc[long["scope"].eq(scope)].copy()
    keep = ["model", "variant", "horizon", "segment", "scope", "n_obs", *CORE_METRICS,
            "CI_coverage", "fallback_forecasts", "fallback_share", "target_kind",
            "lookback", "n_train", "n_params"]
    long = long[[c for c in keep if c in long.columns]]
    return long.sort_values(["model", "variant", "horizon", "segment"]).reset_index(drop=True)


def build_matrix(long: pd.DataFrame, segment: str, metrics=("RMSE", "Corr")) -> pd.DataFrame:
    """One row per (model, variant), one column per metric x horizon."""
    view = long.loc[long["segment"].eq(segment)]
    wide = view.pivot_table(index=["model", "variant"], columns="horizon",
                            values=list(metrics))
    wide.columns = [f"{metric}_h{horizon:02d}" for metric, horizon in wide.columns]
    return wide.reset_index().sort_values(f"RMSE_h{view['horizon'].max():02d}")


def _series(long: pd.DataFrame, model: str, variant: str, segment: str,
            metric: str) -> pd.Series:
    view = long.loc[long["model"].eq(model) & long["variant"].eq(variant)
                    & long["segment"].eq(segment)]
    return view.set_index("horizon")[metric].sort_index()


def _finish(fig, ax, path: Path, *, horizons: list[int], xlabel: str) -> None:
    palette.style_axes(ax)
    ax.set_xscale("log")
    ax.set_xticks(horizons)
    ax.set_xticklabels([str(h) for h in horizons])
    ax.minorticks_off()
    ax.set_xlabel(xlabel, color=palette.INK_SECONDARY, fontsize=8)
    fig.patch.set_facecolor(palette.SURFACE)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)
    print(f"  {path}")


def plot_error_growth(long: pd.DataFrame, models: list[str], variant: str,
                      segment: str, metric: str, path: Path) -> None:
    horizons = sorted(long["horizon"].unique())
    fig, ax = plt.subplots(figsize=(7.0, 4.2))

    for name, style in REFERENCE_STYLES.items():
        series = _series(long, name, variant, segment, metric)
        if not series.empty:
            ax.plot(series.index, series.to_numpy(), label=f"{name} (floor)", **style)

    for slot, model in enumerate(models):
        series = _series(long, model, variant, segment, metric)
        if series.empty:
            continue
        ax.plot(series.index, series.to_numpy(), label=model,
                color=palette.series_colour(slot), marker=palette.marker(slot),
                markersize=4, linewidth=palette.LINE_WIDTH)

    ax.set_ylabel(f"{metric} (ILI per 100,000)" if metric in ("RMSE", "MAE") else metric,
                  color=palette.INK_SECONDARY, fontsize=8)
    ax.set_title(f"Forecast error against horizon — {variant}, {segment}",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=7, labelcolor=palette.INK_SECONDARY, ncol=2)
    _finish(fig, ax, path, horizons=horizons, xlabel="Weeks ahead (log scale)")


def plot_skill(long: pd.DataFrame, models: list[str], variant: str, segment: str,
               path: Path) -> None:
    """RMSE relative to seasonal_naive. Below 1.0 is skill; 1.0 is the calendar."""
    horizons = sorted(long["horizon"].unique())
    floor = _series(long, "seasonal_naive", variant, segment, "RMSE")
    if floor.empty:
        print("  (no seasonal_naive rows; skipping skill plot)")
        return

    def ratio(model: str) -> pd.Series:
        """Skill on the horizons this model and the floor actually share.

        A model missing a horizon -- a failed run, or a sweep still in flight --
        would otherwise divide into the floor's longer index and produce a
        series that no longer lines up with its own x values.
        """
        series = _series(long, model, variant, segment, "RMSE")
        shared = series.index.intersection(floor.index)
        return (series.loc[shared] / floor.loc[shared]).sort_index()

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.axhline(1.0, color=palette.INK_SECONDARY, linestyle="--", linewidth=1.6,
               label="seasonal_naive (floor)")
    skill = ratio("persistence")
    if not skill.empty:
        ax.plot(skill.index, skill.to_numpy(), label="persistence",
                **REFERENCE_STYLES["persistence"])

    for slot, model in enumerate(models):
        skill = ratio(model)
        if skill.empty:
            continue
        ax.plot(skill.index, skill.to_numpy(), label=model,
                color=palette.series_colour(slot), marker=palette.marker(slot),
                markersize=4, linewidth=palette.LINE_WIDTH)

    ax.set_ylabel("RMSE ÷ seasonal_naive RMSE", color=palette.INK_SECONDARY, fontsize=8)
    ax.set_title(f"Skill against the seasonal floor — {variant}, {segment}",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=7, labelcolor=palette.INK_SECONDARY, ncol=2)
    _finish(fig, ax, path, horizons=horizons, xlabel="Weeks ahead (log scale)")


def plot_facets(long: pd.DataFrame, variant: str, segment: str, path: Path) -> None:
    """Every model, one small panel each, with the two floors repeated.

    The palette has four validated categorical slots and this project has
    nineteen runs, so the full set cannot go on one axes. Faceting is the honest
    resolution: shared y-scale keeps the panels comparable.
    """
    view = long.loc[long["variant"].eq(variant) & long["segment"].eq(segment)]
    models = [m for m in sorted(view["model"].unique()) if m not in REFERENCE_STYLES]
    if not models:
        return
    horizons = sorted(long["horizon"].unique())

    columns = 4
    rows = int(np.ceil(len(models) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(3.0 * columns, 2.3 * rows),
                             sharex=True, sharey=True)
    axes = np.atleast_1d(axes).ravel()

    ceiling = view["RMSE"].max() * 1.08
    for index, model in enumerate(models):
        ax = axes[index]
        for name, style in REFERENCE_STYLES.items():
            floor = _series(long, name, variant, segment, "RMSE")
            if not floor.empty:
                ax.plot(floor.index, floor.to_numpy(), **style)
        series = _series(long, model, variant, segment, "RMSE")
        ax.plot(series.index, series.to_numpy(), color=palette.SERIES[0],
                marker="o", markersize=3, linewidth=palette.LINE_WIDTH)
        ax.set_title(model, fontsize=8)
        ax.set_ylim(0, ceiling)
        ax.set_xscale("log")
        ax.set_xticks(horizons)
        ax.set_xticklabels([str(h) for h in horizons])
        ax.minorticks_off()
        palette.style_axes(ax)
    for ax in axes[len(models):]:
        ax.set_visible(False)

    fig.suptitle(f"RMSE against horizon, every model — {variant}, {segment}. "
                 f"Dotted = persistence, dashed = seasonal_naive.",
                 fontsize=10)
    fig.patch.set_facecolor(palette.SURFACE)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)
    print(f"  {path}")


# Counts and week numbers are integers even after a groupby has floated them;
# rendering horizon 1 as "1.000" makes the table harder to read, not more precise.
_INTEGER_COLUMNS = {"horizon", "n_models", "n_obs", "n_train", "n_params", "lookback",
                    "fallback_forecasts", "best horizon (lowest RMSE÷floor)"}


def _cell(value, column: str) -> str:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return ""
    if isinstance(value, (int, float, np.number)):
        return f"{int(value)}" if column in _INTEGER_COLUMNS else f"{float(value):.3f}"
    return str(value)


def _table(frame: pd.DataFrame) -> list[str]:
    header = "| " + " | ".join(frame.columns) + " |"
    rule = "| " + " | ".join("---" for _ in frame.columns) + " |"
    rows = [
        "| " + " | ".join(_cell(v, c) for v, c in zip(row, frame.columns)) + " |"
        for _, row in frame.iterrows()
    ]
    return [header, rule, *rows]


def leaderboard(long: pd.DataFrame, variant: str, segment: str, scope: str) -> str:
    view = long.loc[long["variant"].eq(variant) & long["segment"].eq(segment)]
    horizons = sorted(view["horizon"].unique())

    lines = [
        f"# Leaderboard by forecast horizon — {variant}",
        "",
        f"`segment={segment}`, `scope={scope}`. RMSE is ILI ED visits per 100,000. "
        f"Every horizon scores the same 49 target weeks, so the columns are directly "
        f"comparable.",
        "",
    ]

    floor = _series(long, "seasonal_naive", variant, segment, "RMSE")
    persistence = _series(long, "persistence", variant, segment, "RMSE")

    # The headline: does the choice of model start to matter?
    lines += ["## Does the horizon separate the models?", ""]
    spread = view.groupby("horizon")["RMSE"].agg(["std", "min", "max", "count"])
    spread["max_minus_min"] = spread["max"] - spread["min"]
    spread = spread.reset_index().rename(columns={"std": "RMSE_std", "count": "n_models"})
    lines += _table(spread[["horizon", "n_models", "RMSE_std", "max_minus_min", "min", "max"]])
    lines += [
        "",
        "If `RMSE_std` does not grow with the horizon, the models are still "
        "indistinguishable and the longer horizon did not help.",
        "",
    ]

    lines += ["## Skill against the two floors", ""]
    skill_rows = []
    for model in sorted(view["model"].unique()):
        if model in REFERENCE_STYLES:
            continue
        series = _series(long, model, variant, segment, "RMSE")
        beats_p = [h for h in series.index if h in persistence.index and series[h] < persistence[h]]
        beats_s = [h for h in series.index if h in floor.index and series[h] < floor[h]]
        skill_rows.append({
            "model": model,
            "beats persistence at": ", ".join(str(h) for h in beats_p) or "never",
            "beats seasonal_naive at": ", ".join(str(h) for h in beats_s) or "never",
            "best horizon (lowest RMSE÷floor)":
                min(((series[h] / floor[h], h) for h in series.index if h in floor.index),
                    default=(np.nan, None))[1],
        })
    lines += _table(pd.DataFrame(skill_rows))
    lines += [""]

    for horizon in horizons:
        at_h = view.loc[view["horizon"].eq(horizon)].copy()
        at_h = at_h.sort_values("RMSE")
        at_h["note"] = ""
        # fallback_share only exists when an ARIMA run is in the set.
        if "fallback_share" in at_h.columns:
            degraded = at_h["fallback_share"].fillna(0) > 0
            at_h.loc[degraded, "note"] = at_h.loc[degraded, "fallback_share"].map(
                lambda s: f"DEGRADED: {s:.0%} of forecasts fell back to persistence"
            )
        if "seasonal_naive" in at_h["model"].values and "persistence" in at_h["model"].values:
            same = np.isclose(
                at_h.loc[at_h["model"].eq("seasonal_naive"), "RMSE"].iloc[0],
                at_h.loc[at_h["model"].eq("persistence"), "RMSE"].iloc[0],
            )
            if same:
                at_h.loc[at_h["model"].isin(["persistence", "seasonal_naive"]), "note"] = (
                    "identical at this horizon by construction"
                )
        columns = ["model", "RMSE", "MAE", "Corr", "n_obs", "note"]
        lines += [f"## Horizon {horizon}", ""]
        lines += _table(at_h[[c for c in columns if c in at_h.columns]])
        lines += [""]

    lines += [
        "### Reading the naive baselines",
        "",
        "`persistence` predicts the last value the forecaster could actually see, so "
        "at horizon *h* it reaches back *h* weeks. `seasonal_naive` reaches back 52. "
        "At horizon 52 those are the same week, so the two models are identical there "
        "by construction — not a bug, and not two independent baselines.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    results_root = city_results_dir(args, get_city(args.city)).resolve()
    found = discover(results_root)
    if not found:
        raise SystemExit(
            f"error: no results/horizon_*/<model>/<variant>/metrics.csv under {results_root}. "
            f"Run 'python Code/run_all_horizons.py' first."
        )

    frames = [load_one(horizon, path) for horizon, path in found]
    frames = [f for f in frames if f is not None]
    if not frames:
        raise SystemExit("error: every discovered metrics.csv was skipped; see warnings above.")

    long = build_long(frames, args.scope)
    horizons = sorted(long["horizon"].unique())
    print(f"Discovered {len(frames)} runs across horizons {horizons} under {results_root}")

    out = (args.out_dir or paths.CROSS_HORIZON_DIR).resolve()
    out.mkdir(parents=True, exist_ok=True)
    long.to_csv(out / "horizon_long.csv", index=False)
    build_matrix(long, args.segment).to_csv(out / "horizon_matrix.csv", index=False)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    available = set(long["model"].unique())
    missing = [m for m in models if m not in available]
    if missing:
        print(f"warning: no rows for {missing}; plotting the rest", file=sys.stderr)
    models = [m for m in models if m in available]
    if len(models) > len(palette.SERIES):
        raise SystemExit(f"error: --models takes at most {len(palette.SERIES)} names "
                         f"(the palette has that many validated slots); got {len(models)}. "
                         f"The full set is in error_growth_facets.png.")

    print("\nWriting:")
    plot_error_growth(long, models, args.variant, args.segment, args.metric,
                      out / "error_growth.png")
    plot_skill(long, models, args.variant, args.segment, out / "skill_vs_seasonal.png")
    plot_facets(long, args.variant, args.segment, out / "error_growth_facets.png")
    (out / "leaderboard_horizons.md").write_text(
        leaderboard(long, args.variant, args.segment, args.scope))
    print(f"  {out / 'leaderboard_horizons.md'}")

    view = long.loc[long["variant"].eq(args.variant) & long["segment"].eq(args.segment)]
    spread = view.groupby("horizon")["RMSE"].std()
    print(f"\nRMSE spread across models ({args.variant}, {args.segment}):")
    for horizon, value in spread.items():
        print(f"  horizon {horizon:>2}: {value:6.2f}")
    print(f"\nOutputs: {out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--models", default=DEFAULT_MODELS,
                        help=f"Up to {len(palette.SERIES)} coloured series. The naive "
                             f"baselines are always drawn as reference lines.")
    parser.add_argument("--variant", default="post_covid")
    parser.add_argument("--segment", default="overall",
                        choices=["overall", "flu_season", "off_season"])
    parser.add_argument("--scope", default="pooled",
                        choices=["pooled", "macro", "neighborhood", "cross_week"])
    parser.add_argument("--metric", default="RMSE", choices=list(CORE_METRICS))
    return parser.parse_args()


if __name__ == "__main__":
    main()
