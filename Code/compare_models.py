"""Rank every model that has written results, on identical metrics.

Discovery is by glob, so dropping a new results/<model>/<variant>/ directory in
makes it appear here with no registration step:

    python Code/compare_models.py
    python Code/compare_models.py --segment flu_season --rank-by MAE
    python Code/compare_models.py --update-readme

Directories beginning with '_' are skipped, which excludes _legacy_pre_refactor,
_emissions, _cache and _comparison automatically.
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

from influenza import NEIGHBORHOODS, SHORT_NAMES, paths
from influenza.metrics import CORE_METRICS
from influenza.palette import series_colour

# Full name -> short label, for the compact win-count table.
SHORT = dict(zip(NEIGHBORHOODS, SHORT_NAMES))

# Lower is better for error metrics, higher for correlation.
DESCENDING = {"Corr", "Spearman", "CCC", "R2", "CI_coverage"}

# All three are reported by default: the full year, the season that matters
# operationally, and the quiet months. Errors differ by roughly 3x between the
# last two, so a single full-year number hides which one a model is good at.
ALL_SEGMENTS = "overall,flu_season,off_season"
SEGMENT_LABELS = {
    "overall": "Overall (full year)",
    "flu_season": "Flu season (Oct–Mar)",
    "off_season": "Off-season (Apr–Sep)",
    "legacy": "Legacy, pre-refactor window",
}
README_BEGIN = "<!-- BEGIN LEADERBOARD -->"
README_END = "<!-- END LEADERBOARD -->"


def discover(results_root: Path) -> list[Path]:
    return sorted(
        path for path in results_root.glob("*/*/metrics.csv")
        if not any(part.startswith("_") for part in path.relative_to(results_root).parts)
    )


def load_one(path: Path, results_root: Path, *, allow_legacy: bool) -> pd.DataFrame | None:
    frame = pd.read_csv(path)
    relative = path.relative_to(results_root)

    if "segment" not in frame.columns:
        message = (f"{relative}: pre-refactor schema (no 'segment' column) — re-run "
                   f"'python Code/run_{relative.parts[0]}.py --variant {relative.parts[1]}'")
        if not allow_legacy:
            raise SystemExit(f"error: {message}")
        print(f"warning: {message}; labelling as segment='legacy'", file=sys.stderr)
        frame["segment"] = "legacy"

    frame["model"] = frame.get("model", pd.Series(dtype=str)).fillna(relative.parts[0])
    frame["variant"] = frame.get("variant", pd.Series(dtype=str)).fillna(relative.parts[1])

    # Provenance columns come from the sibling config and emissions files; they
    # are what let a reader see that two rows are not actually comparable.
    meta: dict = {"target_kind": None, "normalize": None, "n_params": None, "git_sha": None}
    config_path = path.parent / "run_config.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        for key in meta:
            meta[key] = config.get(key)
    emissions_path = path.parent / "emissions.json"
    if emissions_path.exists():
        emissions = json.loads(emissions_path.read_text())
        meta["kg_co2"] = emissions.get("kg_co2")
        meta["kwh"] = emissions.get("kwh")
        meta["runtime_s"] = emissions.get("duration_s")
    for key, value in meta.items():
        frame[key] = value
    return frame


def build_long(frames: list[pd.DataFrame], args: argparse.Namespace) -> pd.DataFrame:
    long = pd.concat(frames, ignore_index=True)
    long = long.loc[long["scope"].eq(args.scope) & long["horizon"].eq(args.horizon)]
    if args.models:
        wanted = {m.strip() for m in args.models.split(",")}
        long = long.loc[long["model"].isin(wanted)]
    if args.variant:
        long = long.loc[long["variant"].eq(args.variant)]
    segments = [s.strip() for s in args.segment.split(",")]
    long = long.loc[long["segment"].isin(segments)]
    if long.empty:
        raise SystemExit("error: no rows matched the requested filters.")

    # Rank within a segment, and additionally within a neighborhood when that is
    # the scope -- otherwise the ranks would compare Fenway against Dorchester.
    rank_within = ["segment"] + (["neighborhood"] if args.scope == "neighborhood" else [])
    for metric in CORE_METRICS:
        long[f"rank_{metric}"] = (
            long.groupby(rank_within)[metric]
            .rank(ascending=metric not in DESCENDING, method="min")
        )
    return long.sort_values([*rank_within, args.rank_by],
                            ascending=args.rank_by not in DESCENDING)


def check_comparability(long: pd.DataFrame, scope: str = "pooled") -> list[str]:
    """Surface the ways in which two rows might not be measuring the same thing."""
    warnings: list[str] = []
    # n_obs legitimately differs between neighborhoods (coverage is uneven), so
    # at neighborhood scope compare only within a neighborhood.
    group = ["segment"] + (["neighborhood"] if scope == "neighborhood" else [])
    for label, part in long.groupby(group):
        sizes = part["n_obs"].dropna()
        if sizes.nunique() > 1:
            where = label if isinstance(label, str) else "/".join(str(x) for x in label)
            # Name only the minority groups. Listing all twenty models, as an
            # earlier version did, buried the three that actually differ.
            majority = int(sizes.mode().iloc[0])
            odd = part.loc[part["n_obs"].ne(majority)]
            detail = "; ".join(
                f"{int(n)} cells: {', '.join(sorted(set(g['model'] + '/' + g['variant'])))}"
                for n, g in odd.groupby("n_obs")
            )
            warnings.append(
                f"'{where}': most models were scored on {majority} cells, but — {detail}. "
                "A horizon-1-only model keeps one extra forecast origin, so its errors "
                "are averaged over slightly different weeks."
            )
    for column, label in (("target_kind", "target parameterisation"),
                          ("normalize", "normalisation reference")):
        values = long[column].dropna().unique()
        if len(values) > 1:
            groups = long.groupby(column)["model"].unique().to_dict()
            detail = "; ".join(f"{k}: {', '.join(sorted(set(v)))}" for k, v in groups.items())
            warnings.append(f"mixed {label} in this table ({detail}). "
                            "Differences here are not purely model quality.")
    return warnings


def identity_keys(scope: str) -> list[str]:
    """What makes a row unique. At neighborhood scope the name is part of it.

    Getting this wrong is silent: pivot_table's default aggfunc is `mean`, so
    omitting `neighborhood` at neighborhood scope would quietly average the 14
    of them into one plausible-looking number.
    """
    return ["model", "variant"] + (["neighborhood"] if scope == "neighborhood" else [])


def build_wide(long: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    keys = identity_keys(args.scope)
    # Interval coverage rides along with the point metrics: a model whose 95%
    # band only covers 85% of observations is overstating its own precision, and
    # that is worth seeing next to its RMSE.
    values = list(CORE_METRICS)
    if "CI_coverage" in long.columns and long["CI_coverage"].notna().any():
        values.append("CI_coverage")

    duplicated = long.duplicated(subset=[*keys, "segment"]).sum()
    if duplicated:
        raise SystemExit(
            f"error: {duplicated} rows share the same {keys + ['segment']} and would be "
            "silently averaged. This is a bug in the scope handling, not in your data."
        )

    pivot = long.pivot_table(index=keys, columns="segment", values=values)
    pivot.columns = [f"{metric}_{segment}" for metric, segment in pivot.columns]
    meta_columns = ["target_kind", "normalize", "n_params", "git_sha"]
    if "kg_co2" in long.columns:
        meta_columns += ["kg_co2", "kwh", "runtime_s"]
    meta = long.groupby(keys)[meta_columns].first()
    ranks = long.groupby(keys)[f"rank_{args.rank_by}"].mean().rename("mean_rank")
    wide = pivot.join(meta).join(ranks).reset_index()
    sort_col = f"{args.rank_by}_{args.segment.split(',')[0].strip()}"
    if sort_col in wide.columns:
        sort_by = (["neighborhood", sort_col] if args.scope == "neighborhood" else [sort_col])
        wide = wide.sort_values(sort_by, ascending=args.rank_by not in DESCENDING)
    return wide


def observed_scale(long: pd.DataFrame, results_root: Path, args: argparse.Namespace) -> pd.DataFrame:
    """Mean observed rate per (neighborhood, segment).

    An RMSE of 20 is a different claim in Fenway (mean rate ~9) than in
    Dorchester (~63), so the per-neighborhood tables carry the scale alongside
    the errors. Actuals are identical across models, so any one run supplies them.
    """
    from influenza.metrics import segment_labels

    for model, variant in long[["model", "variant"]].drop_duplicates().itertuples(index=False):
        path = results_root / model / variant / "predictions.csv"
        if not path.exists():
            continue
        frame = pd.read_csv(path, parse_dates=["target_date"])
        frame = frame.loc[frame["horizon"].eq(args.horizon)]
        if frame.empty:
            continue
        frame["segment"] = segment_labels(frame["target_date"])
        overall = frame.assign(segment="overall")
        both = pd.concat([frame, overall], ignore_index=True)
        return (both.groupby(["neighborhood", "segment"])["actual"]
                .agg(mean_observed="mean", peak_observed="max").reset_index())
    return pd.DataFrame(columns=["neighborhood", "segment", "mean_observed", "peak_observed"])


def save_plot(long: pd.DataFrame, path: Path, args: argparse.Namespace) -> None:
    """Grouped bars: one panel per metric, one bar per segment within each model."""
    from matplotlib.patches import Patch

    from influenza.palette import (
        INK_MUTED, INK_PRIMARY, INK_SECONDARY, SURFACE, style_axes,  # noqa: F401
    )

    segments = [s.strip() for s in args.segment.split(",")]
    order = (long.loc[long["segment"].eq(segments[0])]
             .sort_values(args.rank_by, ascending=args.rank_by not in DESCENDING))
    labels = [r.model if r.variant == "post_covid" else f"{r.model} ({r.variant})"
              for r in order.itertuples()]
    keys = list(zip(order["model"], order["variant"]))

    # Height is driven by the number of models, not models x segments: the three
    # bars of a group sit inside one row, they do not each need their own.
    figure_height = max(7.0, 0.34 * len(keys) + 1.6)
    fig, axes = plt.subplots(2, 2, figsize=(16, figure_height))
    fig.patch.set_facecolor(SURFACE)
    positions = np.arange(len(keys))
    bar_height = 0.78 / max(len(segments), 1)
    colours = [series_colour(i) for i in range(min(len(segments), 4))]

    for ax, metric in zip(axes.flat, CORE_METRICS):
        style_axes(ax, grid_axis="x")
        for s_idx, segment in enumerate(segments):
            part = long.loc[long["segment"].eq(segment)].set_index(["model", "variant"])
            values = [float(part[metric].get(key, np.nan)) for key in keys]
            offset = (s_idx - (len(segments) - 1) / 2) * bar_height
            ax.barh(positions + offset, values, height=bar_height,
                    color=colours[s_idx % len(colours)], linewidth=0)
        # Deliberately no per-bar numbers. Twenty models x three segments x four
        # panels is 240 labels, which collide wherever two models are close --
        # exactly the case a reader cares about. The tables carry exact values.
        ax.set_yticks(positions)
        ax.set_yticklabels(labels, fontsize=7, color=INK_PRIMARY)
        ax.invert_yaxis()
        ax.margins(x=0.12)
        ax.set_title(f"{metric} — {'higher' if metric in DESCENDING else 'lower'} is better",
                     fontsize=11, color=INK_PRIMARY, loc="left", pad=8)

    handles = [Patch(facecolor=colours[i % len(colours)],
                     label=SEGMENT_LABELS.get(s, s)) for i, s in enumerate(segments)]
    fig.legend(handles=handles, loc="upper center", ncol=len(segments), frameon=False,
               fontsize=9, labelcolor=INK_SECONDARY,
               bbox_to_anchor=(0.5, 1 - 0.55 / figure_height))
    fig.suptitle(f"Model comparison by segment — scope={args.scope}, "
                 f"horizon {args.horizon}, ranked by {args.rank_by}",
                 fontsize=13, color=INK_PRIMARY, y=1 - 0.16 / figure_height)
    fig.text(0.5, 1 - 0.92 / figure_height,
             "Off-season MAPE is inflated by near-zero rates; rank the off-season on "
             "RMSE or MAE instead.", ha="center", fontsize=8, color=INK_MUTED)
    fig.tight_layout(rect=(0, 0, 1, 1 - 1.15 / figure_height))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def _cells_scored(part: pd.DataFrame, *, unit: str = "cells", dash: bool = True) -> str:
    """Report the scored count, as a range when models disagree.

    Quoting the maximum would credit every model with the extra forecast origin
    that only the horizon-1-only models actually have.
    """
    sizes = part["n_obs"].dropna().astype(int)
    if sizes.empty:
        return ""
    lead = " — " if dash else ", "
    if sizes.nunique() == 1:
        return f"{lead}{sizes.iloc[0]} {unit} scored"
    return f"{lead}{sizes.min()}–{sizes.max()} {unit} scored (models differ)"


def leaderboard_markdown(long: pd.DataFrame, wide: pd.DataFrame,
                         args: argparse.Namespace, warnings: list[str]) -> str:
    """One ranked section per segment.

    A single wide table with every metric crossed by every segment runs to
    seventeen columns and is unreadable. Three separate rankings also make the
    point that the ordering is not the same in each: a model can be strong
    overall and mediocre in the season that actually matters.
    """
    segments = [s.strip() for s in args.segment.split(",")]
    ascending = args.rank_by not in DESCENDING
    metrics = [m for m in (*CORE_METRICS, "CI_coverage") if m in long.columns]
    extra = [c for c in ("target_kind", "normalize") if c in long.columns]

    lines = [
        f"Ranked by **{args.rank_by}** within each segment, `scope={args.scope}`, "
        f"horizon {args.horizon}.",
        "",
    ]
    for segment in segments:
        part = long.loc[long["segment"].eq(segment)]
        if part.empty:
            continue
        part = part.sort_values(args.rank_by, ascending=ascending)
        lines += [f"## {SEGMENT_LABELS.get(segment, segment)}"
                  f"{_cells_scored(part)}", ""]
        if segment == "off_season":
            lines += ["*Mean rate is about 5 per 100,000 here, so MAPE is large and "
                      "unstable by construction — rank on RMSE or MAE, not MAPE.*", ""]
        lines += [*_markdown_table(part[["model", "variant", *metrics, *extra]]), ""]

    lines += _ranking_agreement(long, segments, args)

    if warnings:
        lines += ["## Comparability notes", ""] + [f"- {w}" for w in warnings] + [""]
    return "\n".join(lines)


def _ranking_agreement(long: pd.DataFrame, segments: list[str],
                       args: argparse.Namespace) -> list[str]:
    """Does the ordering survive across segments? Says so explicitly if not."""
    if len(segments) < 2:
        return []
    leaders = {}
    for segment in segments:
        part = long.loc[long["segment"].eq(segment)]
        if part.empty:
            continue
        best = part.loc[part[args.rank_by].idxmin() if args.rank_by not in DESCENDING
                        else part[args.rank_by].idxmax()]
        leaders[segment] = f"{best.model} ({best.variant})"
    if not leaders:
        return []

    lines = ["## Does the ranking agree across segments?", ""]
    lines += [f"- **{SEGMENT_LABELS.get(s, s)}**: `{m}`" for s, m in leaders.items()]
    lines += [""]
    if len(set(leaders.values())) == 1:
        lines += [f"The same model leads every segment, so the ranking is robust to "
                  f"which part of the year you score.", ""]
    else:
        lines += ["The leader changes between segments. Off-season and flu-season are "
                  "close to different problems — the off-season is flat and near zero, "
                  "the flu season has the peak that actually matters operationally — so "
                  "a model tuned on a full-year average is not necessarily the one you "
                  "would deploy for a surge.", ""]
    return lines


def _format(view: pd.DataFrame) -> pd.DataFrame:
    out = view.copy()
    for column in out.columns:
        if out[column].dtype.kind == "f":
            out[column] = out[column].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
    return out


def _markdown_table(view: pd.DataFrame) -> list[str]:
    view = _format(view)
    lines = ["| " + " | ".join(view.columns) + " |",
             "| " + " | ".join("---" for _ in view.columns) + " |"]
    lines += ["| " + " | ".join(str(v) for v in row) + " |"
              for row in view.itertuples(index=False)]
    return lines


def neighborhood_leaderboard(
    long: pd.DataFrame,
    scale: pd.DataFrame,
    args: argparse.Namespace,
    warnings: list[str],
    pooled_order: list[str] | None = None,
) -> str:
    """One ranked section per neighborhood, plus a win-count summary."""
    segments = [s.strip() for s in args.segment.split(",")]
    primary = segments[0]
    here = long.loc[long["segment"].eq(primary)].copy()
    ascending = args.rank_by not in DESCENDING

    scale_lookup = (scale.loc[scale["segment"].eq(primary)]
                    .set_index("neighborhood") if not scale.empty else pd.DataFrame())

    # Order sections by disease burden, so the neighborhoods that matter most for
    # planning come first rather than alphabetically.
    if not scale_lookup.empty:
        order = (scale_lookup["mean_observed"].sort_values(ascending=False).index.tolist())
        order = [n for n in order if n in set(here["neighborhood"])]
    else:
        order = sorted(here["neighborhood"].unique())

    lines = [
        f"# Per-neighborhood leaderboard — horizon {args.horizon}",
        "",
        f"Ranked by **{args.rank_by}**. One section per neighborhood, ordered by mean "
        f"observed rate (highest burden first), and within each neighborhood one "
        f"sub-table per segment: {', '.join(SEGMENT_LABELS.get(s, s) for s in segments)}.",
        "",
        "Every model is scored on the same weeks within a neighborhood, but "
        "coverage differs *between* neighborhoods (Charlestown has 35 suppressed "
        "weeks of 201), so the week count is reported per sub-table. Compare models "
        "down a sub-table; do not compare error magnitudes across neighborhoods or "
        "across segments without also reading the mean rate.",
        "",
    ]

    # --- Win counts, per segment -------------------------------------------
    def winners_for(segment: str) -> pd.DataFrame:
        part = long.loc[long["segment"].eq(segment)]
        if part.empty:
            return part
        picks = (part.groupby("neighborhood")[args.rank_by].idxmin() if ascending
                 else part.groupby("neighborhood")[args.rank_by].idxmax())
        return part.loc[picks].assign(
            label=lambda d: d["model"] + " (" + d["variant"] + ")")

    per_segment = {s: winners_for(s) for s in segments}
    per_segment = {s: w for s, w in per_segment.items() if not w.empty}

    # Rows are models, columns are segments: shows at a glance whether the same
    # model wins the quiet months and the surge.
    tally = pd.DataFrame({
        SEGMENT_LABELS.get(s, s): w["model"].value_counts()
        for s, w in per_segment.items()
    }).fillna(0).astype(int)
    tally = tally.rename_axis("model").reset_index()
    tally = tally.sort_values(tally.columns[1], ascending=False)

    lines += [f"## Summary — neighborhoods won, out of {len(order)}", "",
              *_markdown_table(tally), "",
              "Variants of the same model are pooled here. Which neighborhoods each "
              "one takes, per segment:", ""]
    for segment, won_frame in per_segment.items():
        detail = (won_frame.groupby("label")["neighborhood"]
                  .apply(lambda s: ", ".join(sorted(SHORT.get(n, n) for n in s))))
        lines += [f"- **{SEGMENT_LABELS.get(segment, segment)}** — "
                  + "; ".join(f"`{k}`: {v}" for k, v in detail.items())]
    lines += [""]

    winners = per_segment.get(primary, pd.DataFrame())
    counts = (winners["label"].value_counts().rename_axis("model")
              .reset_index(name="won") if not winners.empty else pd.DataFrame())
    section_leader = counts.iloc[0]["model"] if len(counts) else "n/a"
    won = int(counts.iloc[0]["won"]) if len(counts) else 0
    total = len(order)

    note = [f"`{section_leader}` wins {won} of {total} neighborhoods."]
    if pooled_order:
        pooled_leader = pooled_order[0]
        if pooled_leader != section_leader:
            rank = (pooled_order.index(section_leader) + 1
                    if section_leader in pooled_order else None)
            placing = f"ranks {rank} " if rank else "ranks lower "
            note.append(
                f"The pooled leaderboard is led by `{pooled_leader}` instead, and "
                f"`{section_leader}` {placing}there. That is not a contradiction: the "
                "pooled metric flattens all 14 neighborhoods into one set of cells, so "
                "it is dominated by the high-rate ones (Dorchester and Roxbury average "
                "roughly five times Fenway's rate). Winning most neighborhoods and "
                "winning the pooled error are different achievements, and which one you "
                "want depends on whether you are allocating city-wide capacity or "
                "advising a specific neighborhood."
            )
        else:
            note.append(f"`{pooled_leader}` also leads the pooled leaderboard, so the "
                        "ranking is consistent across both views.")
    lines += [" ".join(note), ""]

    # --- Per-neighborhood sections -----------------------------------------
    metrics = [m for m in (*CORE_METRICS, "CI_coverage") if m in long.columns]
    for neighborhood in order:
        lines += [f"## {neighborhood}", ""]

        context = []
        if neighborhood in scale_lookup.index:
            row = scale_lookup.loc[neighborhood]
            context.append(f"mean observed {row['mean_observed']:.1f}, "
                           f"peak {row['peak_observed']:.1f} per 100,000 over the full year")
        if context:
            lines += ["*" + "; ".join(context) + "*", ""]

        for segment in segments:
            part = long.loc[long["segment"].eq(segment)
                            & long["neighborhood"].eq(neighborhood)]
            if part.empty:
                continue
            part = part.sort_values(args.rank_by, ascending=ascending)
            detail = _cells_scored(part, unit="weeks", dash=False)
            seg_scale = scale.loc[scale["segment"].eq(segment)
                                  & scale["neighborhood"].eq(neighborhood)]
            if not seg_scale.empty:
                detail += f", mean {float(seg_scale['mean_observed'].iloc[0]):.1f}"
            lines += [f"### {SEGMENT_LABELS.get(segment, segment)}{detail}", ""]
            lines += [*_markdown_table(part[["model", "variant", *metrics]]), ""]

    if warnings:
        lines += ["## Comparability notes", ""] + [f"- {w}" for w in warnings] + [""]
    return "\n".join(lines)


def readme_markdown(wide: pd.DataFrame, args: argparse.Namespace) -> str:
    """Compact cross-segment view for the README.

    The full leaderboard is three ranked tables of twenty rows, which is too much
    for a front page. Here every model is one row and the three segments sit side
    by side, so the reader can see at a glance that the ordering changes between
    them. Two metrics only: RMSE for magnitude, Corr for shape.
    """
    segments = [s.strip() for s in args.segment.split(",")]
    metrics = ["RMSE", "Corr"]
    columns = ["model", "variant"]
    rename = {"model": "model", "variant": "variant"}
    for metric in metrics:
        for segment in segments:
            source = f"{metric}_{segment}"
            if source in wide.columns:
                columns.append(source)
                short = {"overall": "all", "flu_season": "flu", "off_season": "off"}
                rename[source] = f"{metric} ({short.get(segment, segment)})"

    view = wide[columns].rename(columns=rename)
    sort_col = f"RMSE ({'all'})"
    if sort_col in view.columns:
        view = view.sort_values(sort_col)

    lines = [
        f"Horizon {args.horizon}, `scope={args.scope}`, sorted by overall RMSE. "
        "`all` = full year (48 weeks), `flu` = Oct–Mar (26), `off` = Apr–Sep (22).",
        "",
        *_markdown_table(view),
        "",
        "Per-segment rankings with MAPE, MAE and interval coverage are in "
        "[`Code/results/_comparison/leaderboard.md`]"
        "(Code/results/_comparison/leaderboard.md); per-neighborhood breakdowns in "
        "[`leaderboard_by_neighborhood.md`]"
        "(Code/results/_comparison/leaderboard_by_neighborhood.md).",
    ]
    return "\n".join(lines) + "\n"


def update_readme(markdown: str, readme: Path) -> None:
    if not readme.exists():
        print(f"warning: {readme} does not exist; skipping --update-readme", file=sys.stderr)
        return
    text = readme.read_text()
    if README_BEGIN not in text or README_END not in text:
        print(f"warning: {readme} has no {README_BEGIN} / {README_END} markers; skipping",
              file=sys.stderr)
        return
    head, _, rest = text.partition(README_BEGIN)
    _, _, tail = rest.partition(README_END)
    readme.write_text(f"{head}{README_BEGIN}\n{markdown}{README_END}{tail}")
    print(f"Updated leaderboard block in {readme}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--models", default=None, help="Comma-separated subset.")
    parser.add_argument("--variant", default=None)
    parser.add_argument("--segment", default=ALL_SEGMENTS,
                        help=f"Comma-separated segments to report (default: {ALL_SEGMENTS}).")
    parser.add_argument("--scope", default="pooled",
                        choices=["pooled", "macro", "neighborhood", "cross_week"])
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--rank-by", default="RMSE", choices=list(CORE_METRICS))
    parser.add_argument("--allow-legacy", action="store_true",
                        help="Include pre-refactor metrics.csv files, labelled 'legacy'.")
    parser.add_argument("--by-neighborhood", action="store_true", default=True,
                        help="Also write a leaderboard with one section per neighborhood "
                             "(default on).")
    parser.add_argument("--no-by-neighborhood", dest="by_neighborhood",
                        action="store_false",
                        help="Skip the per-neighborhood leaderboard.")
    parser.add_argument("--update-readme", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results_root = args.results_dir.resolve()
    found = discover(results_root)
    if not found:
        raise SystemExit(f"error: no metrics.csv under {results_root}")
    print(f"Discovered {len(found)} model/variant results under {results_root}")

    frames = [load_one(path, results_root, allow_legacy=args.allow_legacy) for path in found]
    frames = [f for f in frames if f is not None]
    long = build_long(frames, args)
    warnings = check_comparability(long, args.scope)
    wide = build_wide(long, args)

    out = paths.COMPARISON_DIR
    out.mkdir(parents=True, exist_ok=True)
    long.to_csv(out / "comparison_long.csv", index=False)
    wide.to_csv(out / "comparison_wide.csv", index=False)
    if args.scope == "neighborhood":
        # One ranked bar chart cannot carry models x 14 neighborhoods; the right
        # forms for that are the per-neighborhood tables and plot_forecasts.py.
        print("note: skipping comparison.png at neighborhood scope — see "
              "leaderboard_by_neighborhood.md, or plot_forecasts.py for the curves.")
    else:
        save_plot(long, out / "comparison.png", args)
    markdown = leaderboard_markdown(long, wide, args, warnings)
    (out / "leaderboard.md").write_text(markdown)

    if args.by_neighborhood:
        per_args = argparse.Namespace(**{**vars(args), "scope": "neighborhood"})
        per_long = build_long(frames, per_args)
        per_warnings = check_comparability(per_long, "neighborhood")
        per_wide = build_wide(per_long, per_args)
        per_wide.to_csv(out / "comparison_by_neighborhood.csv", index=False)
        scale = observed_scale(per_long, results_root, per_args)
        pooled_order = [f"{r.model} ({r.variant})" for r in wide.itertuples()]
        (out / "leaderboard_by_neighborhood.md").write_text(
            neighborhood_leaderboard(per_long, scale, per_args, per_warnings,
                                     pooled_order=pooled_order))
        n_neigh = per_long["neighborhood"].nunique()
        print(f"\nPer-neighborhood leaderboard: {n_neigh} sections -> "
              f"{out / 'leaderboard_by_neighborhood.md'}")

    segments = [s.strip() for s in args.segment.split(",")]
    display = ["model", "variant"] + [
        f"{m}_{s}" for s in segments for m in CORE_METRICS if f"{m}_{s}" in wide.columns
    ]
    print(f"\nRanked by {args.rank_by} on segment={segments[0]}, scope={args.scope}, "
          f"horizon={args.horizon}:\n")
    print(wide[display].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    for warning in warnings:
        print(f"\nwarning: {warning}", file=sys.stderr)
    if args.update_readme:
        update_readme(readme_markdown(wide, args), paths.ROOT / "README.md")
    print(f"\nOutputs: {out}")


if __name__ == "__main__":
    main()
