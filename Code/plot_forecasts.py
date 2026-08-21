"""Overlay several models' forecasts against the observed series.

    python Code/plot_forecasts.py
    python Code/plot_forecasts.py --models persistence,arima,lstm,gnn_multiedge
    python Code/plot_forecasts.py --horizon 2 --no-ci
    python Code/plot_forecasts.py --neighborhoods Dorchester,Roxbury,Charlestown

Writes two figures to results/_comparison/:

  forecast_overlay_h<N>.png    one panel per neighborhood
  forecast_citywide_h<N>.png   the 14-neighborhood mean, one large panel

Shaded ribbons are 95% predictive intervals. Every model's interval comes from
the same recipe -- residual variance affine in the predicted level, calibrated
to 95% coverage on the validation split -- so the widths are comparable rather
than each model grading its own homework. See influenza/intervals.py.
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
    from matplotlib.lines import Line2D
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas numpy matplotlib.") from exc

from influenza import NEIGHBORHOODS, SHORT_NAMES, paths
from influenza.palette import (
    ACTUAL,
    ACTUAL_WIDTH,
    BAND_ALPHA,
    INK_MUTED,
    INK_PRIMARY,
    INK_SECONDARY,
    LINE_WIDTH,
    SEASON,
    SEASON_ALPHA,
    SURFACE,
    marker,
    series_colour,
    style_axes,
)
from influenza import severity
from influenza.constants import TEST_END, TEST_START
from influenza.data import load_rates
from influenza.plots import _flu_season_spans

# Default set: the three baselines the user compares against, plus the flagship
# graph model. Four is also the number of validated categorical slots.
DEFAULT_MODELS = ["persistence", "seasonal_naive", "arima", "lstm"]
DEFAULT_WITH_GNN = ["persistence", "arima", "lstm", "gnn_multiedge"]

# One style per severity boundary, so the three lines are told apart without a
# per-panel label. Same ink throughout: they are one ordered family, not three
# unrelated series, and the categorical slots belong to the models.
THRESHOLD_STYLES = [
    ((0, (1, 3)), 0.8, 0.50),
    ((0, (4, 3)), 1.0, 0.65),
    ((0, (7, 2)), 1.2, 0.80),
]


def load_predictions(model: str, variant: str, results_root: Path) -> pd.DataFrame:
    path = results_root / model / variant / "predictions.csv"
    if not path.exists():
        # Runs live one tree per forecast horizon, so pointing at the bare
        # results root finds nothing. Say which trees exist instead of
        # suggesting a run script that may not even be the right one.
        nested = sorted((p for p in results_root.glob("horizon_*")
                         if (p / model / variant / "predictions.csv").exists()),
                        key=lambda p: int(p.name.split("_")[1]))
        if nested:
            listed = "\n".join(f"  --results-dir {p} --horizon {int(p.name.split('_')[1])}"
                               for p in nested)
            raise SystemExit(
                f"error: {path} not found — results are split by forecast horizon.\n"
                f"{model}/{variant} is available in:\n{listed}"
            )
        raise SystemExit(
            f"error: {path} not found. Run the model first, e.g.\n"
            f"  python Code/run_all_horizons.py --models {model}"
        )
    frame = pd.read_csv(path, parse_dates=["target_date"])
    frame["model"] = model
    return frame


def draw_thresholds(ax, thresholds) -> None:
    """Severity boundaries as reference lines, one style per level.

    Lines, not the filled bands used on severity_bands.png. On a forecast panel
    the lines and 95% ribbons are the content; four background washes behind
    them, on top of the gold season shading, turns the panel to mud.
    """
    for index, (value, _band) in enumerate(severity.band_entry_labels(thresholds)):
        dashes, width, alpha = THRESHOLD_STYLES[min(index, len(THRESHOLD_STYLES) - 1)]
        ax.axhline(value, color=INK_SECONDARY, linewidth=width, linestyle=dashes,
                   alpha=alpha, zorder=2)


def threshold_handles(thresholds) -> list:
    """Legend entries naming each boundary by the band it opens."""
    handles = []
    for index, (value, band) in enumerate(severity.band_entry_labels(thresholds)):
        dashes, width, alpha = THRESHOLD_STYLES[min(index, len(THRESHOLD_STYLES) - 1)]
        handles.append(Line2D([0], [0], color=INK_SECONDARY, linewidth=width,
                              linestyle=dashes, alpha=alpha,
                              label=f"{band} (≥{value:.0f})"))
    return handles


def draw_series(ax, part: pd.DataFrame, colour: str, mark: str, label: str, *, show_ci: bool):
    part = part.sort_values("target_date")
    if show_ci and {"lower", "upper"}.issubset(part.columns) and part["lower"].notna().any():
        ax.fill_between(part["target_date"], part["lower"], part["upper"],
                        color=colour, alpha=BAND_ALPHA, linewidth=0, zorder=1)
    ax.plot(part["target_date"], part["predicted"], color=colour, linewidth=LINE_WIDTH,
            marker=mark, markersize=3.2, markevery=6, markeredgewidth=0,
            label=label, zorder=3, solid_capstyle="round")


def legend_handles(models: list[str], *, show_ci: bool) -> list:
    handles = [Line2D([0], [0], color=ACTUAL, linewidth=ACTUAL_WIDTH, label="Observed")]
    for index, model in enumerate(models):
        handles.append(Line2D([0], [0], color=series_colour(index), linewidth=LINE_WIDTH,
                              marker=marker(index), markersize=5, markeredgewidth=0,
                              label=model))
    if show_ci:
        handles.append(Line2D([0], [0], color=INK_MUTED, linewidth=6, alpha=0.3,
                              label="95% interval"))
    return handles


def subtitle(show_ci: bool, *, scale_note: str = "") -> str:
    """Two short lines. Kept explicit rather than relying on auto-wrap, which
    reflows with figure width and then collides with the title."""
    first = ["Gold bands mark the flu season (Oct-Mar)."]
    if show_ci:
        first.insert(0, "Ribbons are 95% predictive intervals, calibrated on the "
                        "validation split by one shared recipe.")
    second = [scale_note] if scale_note else []
    second.append("Exact values: results/_comparison/comparison_wide.csv.")
    return " ".join(first) + "\n" + " ".join(second)


def style_dates(ax) -> None:
    """Quarterly ticks. Monthly ticks collide once panels are this narrow."""
    import matplotlib.dates as mdates

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))


def plot_grid(frames: pd.DataFrame, models: list[str], neighborhoods: list[str],
              path: Path, *, horizon: int, show_ci: bool,
              ceilings: dict[str, float], thresholds=None,
              per_neighborhood: dict | None = None) -> None:
    n = len(neighborhoods)
    cols = 2 if n <= 4 else (3 if n <= 9 else 4)
    rows = int(np.ceil(n / cols))
    # sharey is not used: the limits are set explicitly from the observed series
    # so that the same neighborhood gets the same axis in every model's figure.
    fig, axes = plt.subplots(rows, cols, figsize=(5.0 * cols, 3.1 * rows),
                             sharex=True, sharey=False, squeeze=False)
    fig.patch.set_facecolor(SURFACE)

    spans = _flu_season_spans(frames["target_date"].unique())
    clipped: list[str] = []

    for position, neighborhood in enumerate(neighborhoods):
        ax = axes.flat[position]
        style_axes(ax)
        ceiling = ceilings.get(neighborhood)
        panel_thresholds = (per_neighborhood or {}).get(neighborhood, thresholds)
        if panel_thresholds is not None:
            draw_thresholds(ax, panel_thresholds)
        for low, high in spans:
            ax.axvspan(low, high, color=SEASON, alpha=SEASON_ALPHA, linewidth=0, zorder=0)

        here = frames.loc[frames["neighborhood"].eq(neighborhood)]
        for index, model in enumerate(models):
            draw_series(ax, here.loc[here["model"].eq(model)],
                        series_colour(index), marker(index), model, show_ci=show_ci)

        observed = (here.loc[here["model"].eq(models[0]), ["target_date", "actual"]]
                    .drop_duplicates().sort_values("target_date"))
        ax.plot(observed["target_date"], observed["actual"], color=ACTUAL,
                linewidth=ACTUAL_WIDTH, label="Observed", zorder=4, solid_capstyle="round")

        short = SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)]
        if ceiling:
            ax.set_ylim(0, ceiling)
            # A forecast above the ceiling is cut off. Say which, rather than
            # letting a reader think the model never went that high.
            if float(np.nanmax(here["predicted"].to_numpy(dtype=float), initial=0.0)) > ceiling:
                clipped.append(short)
                ax.annotate("↑ clipped", xy=(0.985, 0.94), xycoords="axes fraction",
                            ha="right", fontsize=6.5, color=INK_MUTED)
        ax.set_title(short, fontsize=10, color=INK_PRIMARY, loc="left", pad=6)
        style_dates(ax)

    for ax in axes.flat[n:]:
        ax.axis("off")

    # With sharex, only the final row keeps tick labels -- but a short last row
    # leaves the right-hand columns with no dates at all. Re-enable them on the
    # lowest panel of every column.
    for column in range(cols):
        occupied = [row for row in range(rows) if row * cols + column < n]
        if occupied:
            bottom = axes[occupied[-1]][column]
            bottom.tick_params(axis="x", labelbottom=True)
            for label in bottom.get_xticklabels():
                label.set_visible(True)

    fig.supylabel("ILI ED visits per 100,000", fontsize=9, color=INK_SECONDARY)
    handles = legend_handles(models, show_ci=show_ci)
    if thresholds is not None:
        handles += threshold_handles(thresholds)
    fig.legend(handles=handles, loc="lower center",
               ncol=min(len(handles), 6), frameon=False, fontsize=9,
               labelcolor=INK_SECONDARY, bbox_to_anchor=(0.5, 0.0))
    # Position the header in inches from the top, not in figure fractions: the
    # figure height scales with the number of rows, so a fixed fraction puts the
    # subtitle on top of the title once the grid is short.
    height = fig.get_size_inches()[1]
    scale_note = f"Forecasts run off the top in: {', '.join(clipped)}." if clipped else ""
    fig.suptitle(f"Observed vs forecast ILI rate, {horizon} week{'s' if horizon > 1 else ''} ahead",
                 fontsize=13, color=INK_PRIMARY, x=0.5, y=1 - 0.22 / height)
    fig.text(0.5, 1 - 0.60 / height, subtitle(show_ci, scale_note=scale_note),
             ha="center", va="top", fontsize=8, color=INK_MUTED, linespacing=1.5)
    legend_inches = 0.42
    fig.tight_layout(rect=(0.015, legend_inches / height, 1, 1 - 1.05 / height))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path}")


def plot_citywide(frames: pd.DataFrame, models: list[str], path: Path, *,
                  horizon: int, show_ci: bool, ceiling: float | None = None,
                  thresholds=None) -> None:
    """The 14-neighborhood mean. One panel, so the lines are readable at a glance."""
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor(SURFACE)
    style_axes(ax)

    if thresholds is not None:
        draw_thresholds(ax, thresholds)
    for low, high in _flu_season_spans(frames["target_date"].unique()):
        ax.axvspan(low, high, color=SEASON, alpha=SEASON_ALPHA, linewidth=0, zorder=0)

    for index, model in enumerate(models):
        part = frames.loc[frames["model"].eq(model)]
        mean = part.groupby("target_date").agg(
            predicted=("predicted", "mean"),
            lower=("lower", "mean") if "lower" in part.columns else ("predicted", "mean"),
            upper=("upper", "mean") if "upper" in part.columns else ("predicted", "mean"),
        ).reset_index()
        draw_series(ax, mean, series_colour(index), marker(index), model, show_ci=show_ci)

    observed = (frames.loc[frames["model"].eq(models[0])]
                .groupby("target_date")["actual"].mean().reset_index())
    ax.plot(observed["target_date"], observed["actual"], color=ACTUAL,
            linewidth=ACTUAL_WIDTH + 0.4, label="Observed", zorder=4, solid_capstyle="round")

    if ceiling:
        ax.set_ylim(0, ceiling)
    ax.set_ylabel("Mean ILI ED visits per 100,000", fontsize=10, color=INK_SECONDARY)
    ax.set_xlabel("Target week", fontsize=10, color=INK_SECONDARY)
    ax.set_title(f"City mean across 14 neighborhoods — {horizon} week"
                 f"{'s' if horizon > 1 else ''} ahead",
                 fontsize=14, color=INK_PRIMARY, loc="left", pad=44)
    ax.text(0, 1.012, subtitle(show_ci), transform=ax.transAxes,
            fontsize=8, color=INK_MUTED, va="bottom", linespacing=1.5)
    style_dates(ax)
    handles = legend_handles(models, show_ci=show_ci)
    if thresholds is not None:
        handles += threshold_handles(thresholds)
    ax.legend(handles=handles, loc="upper left",
              frameon=False, fontsize=9, labelcolor=INK_SECONDARY, ncol=2)
    fig.tight_layout()
    fig.savefig(path, dpi=170, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--models", default=",".join(DEFAULT_WITH_GNN),
                        help="Comma-separated, in the order they should be coloured. "
                             "Maximum four -- the palette has four validated slots.")
    parser.add_argument("--variant", default="post_covid")
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--neighborhoods", default=None,
                        help="Comma-separated subset; default is all 14.")
    parser.add_argument("--no-ci", action="store_true", help="Hide the 95% ribbons.")
    parser.add_argument("--per-neighborhood-scale", action="store_true",
                        help="Give each panel its own y-scale and its own severity "
                             "thresholds. The default standardises both across all "
                             "panels, which makes heights directly comparable at the "
                             "cost of flattening the smaller neighborhoods -- Fenway "
                             "peaks near 21 per 100,000 against Dorchester's 256.")
    parser.add_argument("--y-max", type=float, default=None,
                        help="Override the shared y ceiling. Default: rounded up to cover "
                             "the busiest neighborhood and the top threshold.")
    parser.add_argument("--no-severity", action="store_true",
                        help="Hide the CDC-style severity band shading.")
    parser.add_argument("--reference-seasons", default="post_covid",
                        help="Reference seasons for the severity thresholds; see "
                             "docs/SEVERITY.md.")
    parser.add_argument("--results-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Default: a _comparison/ beside --results-dir, so a "
                             "per-horizon run does not write into the top-level one.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not models:
        raise SystemExit("error: --models is empty")
    if len(models) > 4:
        raise SystemExit(
            f"error: {len(models)} models requested but only four categorical slots are "
            "validated as distinguishable. Plot fewer, or make two figures -- cycling "
            "the palette would give two models the same colour."
        )

    frames = pd.concat([load_predictions(m, args.variant, args.results_dir.resolve())
                        for m in models], ignore_index=True)
    frames = frames.loc[frames["horizon"].eq(args.horizon)]
    if frames.empty:
        raise SystemExit(f"error: no predictions at horizon {args.horizon}")

    missing_ci = [m for m in models
                  if "lower" not in frames.columns
                  or frames.loc[frames["model"].eq(m), "lower"].isna().all()]
    if missing_ci and not args.no_ci:
        print(f"warning: no interval columns for {', '.join(missing_ci)}; "
              "re-run those models to get 95% bands.", file=sys.stderr)

    neighborhoods = ([n.strip() for n in args.neighborhoods.split(",")]
                     if args.neighborhoods else list(NEIGHBORHOODS))
    unknown = [n for n in neighborhoods if n not in NEIGHBORHOODS]
    if unknown:
        raise SystemExit(f"error: unknown neighborhood(s) {unknown}.\n"
                         f"Known: {', '.join(NEIGHBORHOODS)}")

    # n_obs can differ between models (a horizon-1-only model keeps one extra
    # origin), which would silently plot different week sets on one axis.
    counts = frames.groupby("model")["target_date"].nunique()
    if counts.nunique() > 1:
        print(f"warning: models cover different numbers of weeks "
              f"({counts.to_dict()}); the overlay shows each on its own weeks.",
              file=sys.stderr)

    show_ci = not args.no_ci

    # Axes and thresholds come from the observed series, never from the
    # predictions, so every model's figure carries the same reference geometry.
    rates = load_rates()
    fitted, shared, per_neighborhood = None, None, None
    if not args.no_severity:
        named = severity.REFERENCE_SEASON_SETS
        fitted = severity.fit_thresholds(
            rates,
            reference_seasons=(named[args.reference_seasons] if args.reference_seasons in named
                               else tuple(int(y) for y in args.reference_seasons.split(","))),
        )
        # The citywide set is the shared one. Pooling all 14 neighborhoods
        # instead would draw every pooled value from Dorchester and Roxbury, and
        # 12 of the 14 would then read 'low' even at their own season peak.
        shared = fitted[severity.CITYWIDE]
        if args.per_neighborhood_scale:
            per_neighborhood, shared = fitted, None

    if args.per_neighborhood_scale:
        ceilings = severity.panel_ceilings(rates, fitted or {},
                                           window=(TEST_START, TEST_END))
    else:
        ceiling = args.y_max or severity.shared_ceiling(
            rates, shared, window=(TEST_START, TEST_END))
        ceilings = {name: ceiling for name in (*NEIGHBORHOODS, severity.CITYWIDE)}

    print(f"Overlaying {len(models)} models on {len(neighborhoods)} neighborhoods "
          f"at horizon {args.horizon}:")
    if shared is not None:
        print(f"  shared y-scale 0-{ceilings[NEIGHBORHOODS[0]]:.0f}, shared thresholds "
              + ", ".join(f"{band} ≥{value:.0f}"
                          for value, band in severity.band_entry_labels(shared)))
    out = (args.out_dir or paths.comparison_dir(args.results_dir)).resolve()
    plot_grid(frames, models, neighborhoods, out / f"forecast_overlay_h{args.horizon}.png",
              horizon=args.horizon, show_ci=show_ci, ceilings=ceilings,
              thresholds=shared, per_neighborhood=per_neighborhood)
    plot_citywide(frames, models, out / f"forecast_citywide_h{args.horizon}.png",
                  horizon=args.horizon, show_ci=show_ci,
                  ceiling=ceilings.get(severity.CITYWIDE),
                  thresholds=shared or (fitted or {}).get(severity.CITYWIDE))


if __name__ == "__main__":
    main()
