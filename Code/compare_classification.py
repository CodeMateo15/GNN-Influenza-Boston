"""Read as a severity band, how often was each forecast right?

`compare_models.py` asks how close the forecast rate was. `compare_severity.py`
asks whether it crossed each alert threshold in time. This asks the classifier's
question: put every forecast into one of CDC's four bands -- low, moderate, high,
very high -- and score it the way a classification model is scored. It also
answers the question behind it: **is it better to forecast the band directly
than to forecast the rate and bin it?** The direct route is
`run_severity_classifier.py`, and its runs are scored here beside the binned ones.

One citywide set of cut points is used for every neighborhood-week
(`severity.citywide_thresholds`, CDC's Moving Epidemic Method at IT50 / IT90 /
IT98, fitted on weeks before the test window), and a rate is banded by the plain
rule in `Thresholds.band`: below IT50 low, below IT90 moderate, below IT98 high,
otherwise very high.

Each rate model is banded five ways, by its point forecast and by the edges of
its 95% and 99% intervals. The lower edge is the optimistic call, the upper edge
the cautious one. `persistence` and `seasonal_naive` are banded by the point
only: they are copies of a past week, and an interval around a copy says nothing
about the forecast itself.

    python Code/compare_classification.py                     # every horizon
    python Code/compare_classification.py --results-dir Code/results/horizon_02

Per horizon, outputs land in that horizon's `_comparison/`; the cross-horizon
tables in `results/_comparison_horizons/`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.colors import LinearSegmentedColormap
    from scipy.stats import norm
    from sklearn.metrics import precision_recall_curve, roc_curve
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. "
                     f"Install pandas numpy matplotlib scipy scikit-learn.") from exc

from compare_severity import _table, discover_runs, horizon_roots, resolve_horizon
from influenza import paths, severity
from influenza.cities import get as get_city
from influenza.classification import (
    ALERT_LABELS,
    ALERT_LEVELS,
    band_confusion,
    band_scores,
)
from influenza.cli import add_city_arg, city_results_dir
from influenza.intervals import Z95
from influenza.metrics import segment_labels
from influenza.palette import INK_MUTED, INK_PRIMARY, INK_SECONDARY, SERIES, SURFACE, style_axes
from plot_forecasts import load_predictions

Z99 = float(norm.ppf(0.995))

# Copies of a past week. Banding their interval edges would score the interval
# recipe, not the forecast.
POINT_ONLY = {"persistence", "seasonal_naive"}

CLASSIFIER_SUBDIR = "_severity_classifier"
BOUND_ORDER = ["point", "lower99", "lower95", "upper95", "upper99", "argmax"]
BOUND_LABELS = {
    "point": "point forecast",
    "lower95": "95% lower edge", "upper95": "95% upper edge",
    "lower99": "99% lower edge", "upper99": "99% upper edge",
    "argmax": "most likely band",
}
SEGMENTS = ("overall", "flu_season")

# Four validated colour slots. The project palette's red and green collide
# under protanopia, so the curves also differ by line style.
DEFAULT_PLOT_MODELS = ["persistence", "xgboost", "gnn_st", "xgb_severity"]
LINESTYLES = ["-", "--", "-.", ":"]
HEADLINE_MODELS = ["persistence", "seasonal_naive", "arima", "lstm", "xgboost",
                   "gnn_st", "xgb_severity"]

BAND_TABLE = ["model", "bound", "accuracy", "f1_macro", "precision_macro", "recall_macro"]


def _alert_table(tag: str) -> list[str]:
    return ["model", "bound", f"{tag}_precision", f"{tag}_recall", f"{tag}_f1",
            f"{tag}_roc_auc", f"{tag}_pr_auc"]


# --- turning each run into bands ---------------------------------------------

def rate_bounds(model: str, frame: pd.DataFrame) -> dict[str, np.ndarray]:
    """The rates a model is banded by: its point forecast and interval edges.

    The 99% edges are the calibrated 95% band stretched by Z99/Z95 -- reading it
    as Gaussian, which is what `severity.exceedance_probability` already does.
    The spread comes from the upper edge only, because the lower one is clipped
    at zero (see `severity.predictive_sigma`).
    """
    predicted = frame["predicted"].to_numpy(float)
    bounds = {"point": predicted}
    if model in POINT_ONLY or not {"lower", "upper"}.issubset(frame.columns):
        return bounds
    sigma = severity.predictive_sigma(predicted, frame["upper"].to_numpy(float), z=Z95)
    bounds["lower95"] = frame["lower"].to_numpy(float)
    bounds["upper95"] = frame["upper"].to_numpy(float)
    bounds["lower99"] = np.maximum(predicted - Z99 * sigma, 0.0)
    bounds["upper99"] = predicted + Z99 * sigma
    return bounds


def banded_rows(results_root: Path, runs, classifier_runs, cuts, *, horizon: int,
                flu_months) -> pd.DataFrame:
    """One row per (model, bound, neighborhood-week): true band, forecast band,
    and one ranking score per alert level."""
    parts = []
    for model, variant in runs:
        frame = load_predictions(model, variant, results_root)
        frame = frame.loc[frame["horizon"].eq(horizon)
                          & frame["actual"].notna() & frame["predicted"].notna()]
        true_band = cuts.band(frame["actual"].to_numpy(float))
        for bound, values in rate_bounds(model, frame).items():
            part = pd.DataFrame({
                "model": model, "variant": variant, "bound": bound,
                "target_date": frame["target_date"].to_numpy(),
                "neighborhood": frame["neighborhood"].to_numpy(),
                "true_band": true_band, "pred_band": cuts.band(values),
            })
            # A rate ranks weeks for every alert level at once.
            for level in ALERT_LEVELS:
                part[f"score_{level}"] = values
            parts.append(part)

    for model, variant, path in classifier_runs:
        frame = pd.read_csv(path, parse_dates=["target_date"])
        frame = frame.loc[frame["horizon"].eq(horizon)]
        probability = frame.filter(like="p_").to_numpy(float)
        part = pd.DataFrame({
            "model": model, "variant": variant, "bound": "argmax",
            "target_date": frame["target_date"].to_numpy(),
            "neighborhood": frame["neighborhood"].to_numpy(),
            # Re-banded from `actual` rather than trusting the stored label, so a
            # change to the cut points shows up as a mismatch, not silently.
            "true_band": cuts.band(frame["actual"].to_numpy(float)),
            "pred_band": frame["pred_band"].to_numpy(int),
        })
        stored = frame["true_band"].to_numpy(int)
        if not np.array_equal(stored, part["true_band"].to_numpy()):
            raise SystemExit(f"error: {path} was labelled with different cut points than "
                             f"these; re-run run_severity_classifier.py.")
        for level in ALERT_LEVELS:
            part[f"score_{level}"] = probability[:, level:].sum(axis=1)
        parts.append(part)

    if not parts:
        raise SystemExit(f"error: no horizon-{horizon} predictions under {results_root}.")
    rows = pd.concat(parts, ignore_index=True)
    rows = rows.loc[rows["true_band"].ge(0) & rows["pred_band"].ge(0)]
    rows["segment"] = segment_labels(rows["target_date"], flu_months)
    return rows


def score_rows(rows: pd.DataFrame, *, horizon: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(long metrics, long confusion counts) per model, bound and segment."""
    metrics, confusion = [], []
    for (model, variant, bound), group in rows.groupby(["model", "variant", "bound"], sort=False):
        for segment in SEGMENTS:
            part = group if segment == "overall" else group.loc[group["segment"].eq(segment)]
            if part.empty:
                continue
            identity = {"model": model, "variant": variant, "bound": bound,
                        "horizon": horizon, "segment": segment}
            scores = {level: part[f"score_{level}"].to_numpy() for level in ALERT_LEVELS}
            metrics.append({**identity, **band_scores(part["true_band"], part["pred_band"],
                                                      scores)})
            counts = band_confusion(part["true_band"], part["pred_band"])
            for actual, row in enumerate(counts):
                for forecast, count in enumerate(row):
                    confusion.append({**identity,
                                      "actual_band": severity.SEVERITY_BANDS[actual],
                                      "forecast_band": severity.SEVERITY_BANDS[forecast],
                                      "count": int(count)})
    metrics = pd.DataFrame(metrics)
    metrics["bound"] = pd.Categorical(metrics["bound"], BOUND_ORDER, ordered=True)
    return metrics.sort_values(["model", "bound", "segment"]), pd.DataFrame(confusion)


# --- figures -----------------------------------------------------------------

def plot_confusion(rows: pd.DataFrame, models: list[str], path: Path, *, horizon: int) -> None:
    """One 4x4 matrix per model, point forecast (argmax for the classifier).

    Shaded by the share of each actual band's weeks, so the rare bands are
    readable next to 580 low weeks; the number printed is the raw count.
    """
    present = [m for m in models if m in set(rows["model"])]
    if not present:
        return
    cmap = LinearSegmentedColormap.from_list("band_share", [SURFACE, SERIES[0]])
    columns = min(4, len(present))
    n_rows = int(np.ceil(len(present) / columns))
    fig, axes = plt.subplots(n_rows, columns, figsize=(3.3 * columns, 3.3 * n_rows),
                             facecolor=SURFACE, squeeze=False)
    names = ["low", "mod.", "high", "v. high"]
    for ax, model in zip(axes.flat, present):
        part = rows.loc[rows["model"].eq(model) & rows["bound"].isin(["point", "argmax"])]
        counts = band_confusion(part["true_band"], part["pred_band"])
        share = counts / np.maximum(counts.sum(axis=1, keepdims=True), 1)
        ax.imshow(share, cmap=cmap, vmin=0, vmax=1)
        for i in range(4):
            for j in range(4):
                ax.text(j, i, str(counts[i, j]), ha="center", va="center", fontsize=8,
                        color="white" if share[i, j] > 0.6 else INK_PRIMARY)
        ax.set_xticks(range(4), names, fontsize=7)
        ax.set_yticks(range(4), names, fontsize=7)
        ax.set_title(model, fontsize=9, color=INK_PRIMARY)
        for side in ax.spines.values():
            side.set_visible(False)
    for ax in axes.flat[len(present):]:
        ax.axis("off")
    fig.supxlabel("Forecast band", fontsize=9, color=INK_SECONDARY)
    fig.supylabel("Actual band", fontsize=9, color=INK_SECONDARY)
    fig.suptitle(f"Which band did each model put the week in? — horizon {horizon}",
                 fontsize=11, color=INK_PRIMARY)
    fig.tight_layout()
    print(f"note ({path.name}): shade = share of that actual band's weeks; "
          f"number = weeks. Point forecast for rate models.", file=sys.stderr)
    _save(fig, path)


def plot_curves(rows: pd.DataFrame, metrics: pd.DataFrame, models: list[str], path: Path,
                *, horizon: int, level: int = 1) -> None:
    """ROC and precision-recall curves for one alert level, side by side."""
    present = [m for m in models if m in set(rows["model"])][:len(SERIES)]
    if not present:
        return
    tag = ALERT_LEVELS[level]
    fig, (roc_ax, pr_ax) = plt.subplots(1, 2, figsize=(10, 4.4), facecolor=SURFACE)
    base_rate = None
    for index, model in enumerate(present):
        part = rows.loc[rows["model"].eq(model) & rows["bound"].isin(["point", "argmax"])]
        observed = part["true_band"].to_numpy() >= level
        score = part[f"score_{level}"].to_numpy()
        if not 0 < observed.sum() < observed.size:
            continue
        base_rate = observed.mean()
        row = metrics.loc[metrics["model"].eq(model) & metrics["segment"].eq("overall")
                          & metrics["bound"].isin(["point", "argmax"])].iloc[0]
        style = dict(color=SERIES[index], ls=LINESTYLES[index], lw=1.8)
        fpr, tpr, _ = roc_curve(observed, score)
        roc_ax.plot(fpr, tpr, label=f"{model}  {row[f'{tag}_roc_auc']:.3f}", **style)
        precision, recall, _ = precision_recall_curve(observed, score)
        pr_ax.plot(recall, precision, label=f"{model}  {row[f'{tag}_pr_auc']:.3f}",
                   drawstyle="steps-post", **style)
    roc_ax.plot([0, 1], [0, 1], color=INK_MUTED, lw=1.0, ls=":")
    if base_rate is not None:
        pr_ax.axhline(base_rate, color=INK_MUTED, lw=1.0, ls=":")
        pr_ax.annotate(f"random: {base_rate:.3f}", (1.0, base_rate), xytext=(-4, 4),
                       textcoords="offset points", ha="right", fontsize=7, color=INK_MUTED)
    for ax, xlabel, ylabel, title in (
            (roc_ax, "False-alarm rate", "Share of events caught", "ROC — area under curve"),
            (pr_ax, "Share of events caught (recall)", "Alerts that were right (precision)",
             "Precision–recall — area under curve")):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
        ax.set_xlabel(xlabel, fontsize=9, color=INK_SECONDARY)
        ax.set_ylabel(ylabel, fontsize=9, color=INK_SECONDARY)
        ax.set_title(title, fontsize=10, color=INK_PRIMARY)
        style_axes(ax, grid_axis="both")
        ax.legend(fontsize=8, frameon=False, loc="lower right" if ax is roc_ax else "upper right")
    fig.suptitle(f"Ranking weeks that turned out {ALERT_LABELS[level]} — horizon {horizon}",
                 fontsize=11, color=INK_PRIMARY)
    fig.tight_layout()
    _save(fig, path)


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {paths.display(path)}")


# --- markdown ----------------------------------------------------------------

def _view(metrics: pd.DataFrame, columns: list[str], sort: str) -> pd.DataFrame:
    part = metrics.loc[metrics["segment"].eq("overall")]
    part = part.sort_values(sort, ascending=False)[columns].copy()
    part["bound"] = part["bound"].astype(str)
    return part


def horizon_markdown(metrics: pd.DataFrame, rows: pd.DataFrame, cuts, *, horizon: int,
                     notes: list[str]) -> str:
    overall = metrics.loc[metrics["segment"].eq("overall")]
    cut_text = ", ".join(f"IT{l * 100:g} = {cuts.values[l]:.1f}" for l in cuts.levels)
    lines = [
        f"# Severity bands as a classification problem — horizon {horizon}",
        "",
        f"One citywide set of cut points for every neighborhood-week ({cut_text} per "
        f"100,000; CDC's Moving Epidemic Method on "
        f"{', '.join(severity.season_name(y) for y in cuts.reference_seasons)}, fitted "
        f"on weeks before {cuts.fitted_through}). {int(overall['n_obs'].max())} "
        f"neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is "
        f"the direct classifier's most likely band.",
        "",
        "## Across all four bands, how often was the band right?",
        "",
        "Accuracy is carried by the ~92% of weeks that are low: a model that always "
        "says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it "
        "averages the four bands equally, so missing every high week costs as much as "
        "missing every low one.",
        "",
        *_table(_view(metrics, BAND_TABLE, "f1_macro")),
        "",
    ]
    for level, tag in ALERT_LEVELS.items():
        events = int(overall[f"{tag}_n_events"].max())
        base = float(overall[f"{tag}_base_rate"].max())
        flag = (f" — **underpowered: {events} events**"
                if bool(overall[f"{tag}_underpowered"].any()) else "")
        lines += [
            f"## If it had raised an alert for '{ALERT_LABELS[level]}', would it have "
            f"been right?{flag}",
            "",
            f"{events} such weeks, base rate {base:.3f}. Precision: of the alerts, the "
            f"share that were real. Recall: of the real weeks, the share it caught. "
            f"ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). "
            f"PR-AUC: the same, judged only on the rare weeks — chance is the base "
            f"rate, {base:.3f}, not 0.5. The AUCs use the ranking alone, so a model's "
            f"interval edges differ from its point forecast there only where the band "
            f"width reorders weeks.",
            "",
            *_table(_view(metrics, _alert_table(tag), f"{tag}_pr_auc")),
            "",
        ]
    lines += ["## Confusion matrices (rows = actual band, columns = forecast band)", ""]
    for model in HEADLINE_MODELS:
        part = rows.loc[rows["model"].eq(model) & rows["bound"].isin(["point", "argmax"])]
        if part.empty:
            continue
        counts = band_confusion(part["true_band"], part["pred_band"])
        table = pd.DataFrame(counts, columns=list(severity.SEVERITY_BANDS))
        table.insert(0, "actual \\ forecast", list(severity.SEVERITY_BANDS))
        lines += [f"**{model}**", "", *_table(table), ""]
    if notes:
        lines += ["## Notes", ""] + [f"- {n}" for n in notes] + [""]
    return "\n".join(lines)


def cross_horizon_markdown(frame: pd.DataFrame) -> str:
    overall = frame.loc[frame["segment"].eq("overall")].copy()
    overall["bound"] = overall["bound"].astype(str)
    headline = overall.loc[overall["model"].isin(HEADLINE_MODELS)
                           & overall["bound"].isin(["point", "argmax"])]

    def wide(part: pd.DataFrame, metric: str) -> pd.DataFrame:
        table = part.pivot_table(index=["model", "bound"], columns="horizon", values=metric)
        table.columns = [f"h={h}" for h in table.columns]
        return table.reset_index()

    lines = [
        "# Classify the week, or forecast the rate? — horizons 1, 2, 4",
        "",
        "Every rate model is banded by its point forecast; `xgb_severity` is trained "
        "to output the band directly. Same cut points, same weeks, same metrics.",
        "",
        "## Across all four bands, how often was the band right? (macro F1)",
        "",
        *_table(wide(headline, "f1_macro").sort_values(wide(headline, "f1_macro").columns[-1],
                                                       ascending=False)),
        "",
    ]
    for tag, label in (("moderate_plus", "moderate or worse"), ("high_plus", "high or worse")):
        table = wide(headline, f"{tag}_pr_auc")
        lines += [f"## How well does it rank the weeks that turned out {label}? (PR-AUC)", "",
                  *_table(table.sort_values(table.columns[-1], ascending=False)), ""]
    table = wide(overall, "f1_macro")
    lines += ["## Every model and band edge (macro F1)", "",
              "The lower edge is the optimistic call, the upper edge the cautious one.", "",
              *_table(table), ""]
    return "\n".join(lines)


# --- CLI ---------------------------------------------------------------------

def classifier_runs(results_root: Path, variant: str | None):
    found = sorted((results_root / CLASSIFIER_SUBDIR).glob("*/*/predictions.csv"))
    return [(p.parent.parent.name, p.parent.name, p) for p in found
            if variant is None or p.parent.name == variant]


def run_horizon(results_root: Path, args, city, cuts) -> pd.DataFrame:
    runs = [(m, v) for m, v in discover_runs(results_root)
            if args.variant is None or v == args.variant]
    # A horizon_XX root names its horizon; a run inside it may carry others too
    # (gnn_cascade writes h=1 and h=2), so the name decides rather than the files.
    named = results_root.name.split("_")
    requested = int(named[1]) if named[0] == "horizon" and named[1].isdigit() else None
    horizon = resolve_horizon(results_root, runs, requested)
    classifiers = classifier_runs(results_root, args.variant)
    notes = [
        f"99% edges are the validation-calibrated 95% band stretched by "
        f"{Z99:.3f}/{Z95:.3f} under a Gaussian reading; unlike the 95% band they were "
        f"not calibrated on held-out weeks.",
        "persistence and seasonal_naive are scored on their point forecast only.",
    ]
    if not classifiers:
        notes.append("No direct classifier found; run run_severity_classifier.py.")

    print(f"\n=== horizon {horizon}: {len(runs)} rate runs, {len(classifiers)} classifier runs")
    rows = banded_rows(results_root, runs, classifiers, cuts, horizon=horizon,
                       flu_months=city.flu_months)
    metrics, confusion = score_rows(rows, horizon=horizon)

    out = paths.comparison_dir(results_root)
    out.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(out / "classification_long.csv", index=False)
    confusion.to_csv(out / "classification_confusion.csv", index=False)
    (out / "classification_leaderboard.md").write_text(
        horizon_markdown(metrics, rows, cuts, horizon=horizon, notes=notes))
    for name in ("classification_long.csv", "classification_confusion.csv",
                 "classification_leaderboard.md"):
        print(f"Wrote {paths.display(out / name)}")

    plot_confusion(rows, HEADLINE_MODELS, out / "classification_confusion.png",
                   horizon=horizon)
    plot_models = [m.strip() for m in args.plot_models.split(",") if m.strip()]
    plot_curves(rows, metrics, plot_models, out / "classification_pr_roc.png",
                horizon=horizon)

    view = metrics.loc[metrics["segment"].eq("overall")
                       & metrics["bound"].isin(["point", "argmax"])]
    print(view[["model", "bound", "accuracy", "f1_macro", "moderate_plus_pr_auc",
                "high_plus_pr_auc"]].sort_values("f1_macro", ascending=False)
          .round(3).to_string(index=False))
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None,
                        help="One horizon root, or the results root to score every horizon.")
    parser.add_argument("--variant", default="post_covid",
                        help="Only runs of this variant (default post_covid; 'all' for every one).")
    parser.add_argument("--reference-seasons", default="post_covid",
                        choices=[k for k, v in severity.REFERENCE_SEASON_SETS.items() if v])
    parser.add_argument("--plot-models", default=",".join(DEFAULT_PLOT_MODELS),
                        help="Up to four models for the ROC / PR figure.")
    args = parser.parse_args()
    if args.variant == "all":
        args.variant = None
    return args


def main() -> None:
    args = parse_args()
    city = get_city(args.city)
    results_root = city_results_dir(args, city).resolve()
    rates = city.loaders.load_rates()
    cuts = severity.citywide_thresholds(city, rates, reference_seasons=args.reference_seasons)
    print("Citywide cut points: "
          + " | ".join(f"IT{l * 100:g} = {cuts.values[l]:.1f}" for l in cuts.levels)
          + f" (fitted before {cuts.fitted_through})")

    roots = [results_root] if discover_runs(results_root) else horizon_roots(results_root)
    if not roots:
        raise SystemExit(f"error: no */*/predictions.csv under {results_root}.")
    frames = [run_horizon(root, args, city, cuts) for root in roots]

    if len(frames) > 1:
        combined = pd.concat(frames, ignore_index=True)
        out = results_root / paths.CROSS_HORIZON_DIR.name
        out.mkdir(parents=True, exist_ok=True)
        combined.to_csv(out / "classification_by_horizon.csv", index=False)
        (out / "classification_by_horizon.md").write_text(cross_horizon_markdown(combined))
        for name in ("classification_by_horizon.csv", "classification_by_horizon.md"):
            print(f"Wrote {paths.display(out / name)}")


if __name__ == "__main__":
    main()
