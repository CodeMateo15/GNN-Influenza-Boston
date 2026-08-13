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
from influenza.plots import _flu_season_spans

# Default set: the three baselines the user compares against, plus the flagship
# graph model. Four is also the number of validated categorical slots.
DEFAULT_MODELS = ["persistence", "seasonal_naive", "arima", "lstm"]
DEFAULT_WITH_GNN = ["persistence", "arima", "lstm", "gnn_multiedge"]


def load_predictions(model: str, variant: str, results_root: Path) -> pd.DataFrame:
    path = results_root / model / variant / "predictions.csv"
    if not path.exists():
        raise SystemExit(
            f"error: {path} not found. Run the model first, e.g.\n"
            f"  python Code/run_{model.split('_')[0]}.py --variant {variant}"
        )
    frame = pd.read_csv(path, parse_dates=["target_date"])
    frame["model"] = model
    return frame


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
              path: Path, *, horizon: int, show_ci: bool, free_y: bool) -> None:
    n = len(neighborhoods)
    cols = 2 if n <= 4 else (3 if n <= 9 else 4)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(5.0 * cols, 3.1 * rows),
                             sharex=True, sharey=not free_y, squeeze=False)
    fig.patch.set_facecolor(SURFACE)

    spans = _flu_season_spans(frames["target_date"].unique())

    for position, neighborhood in enumerate(neighborhoods):
        ax = axes.flat[position]
        style_axes(ax)
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
    fig.legend(handles=legend_handles(models, show_ci=show_ci), loc="lower center",
               ncol=min(len(models) + 2, 6), frameon=False, fontsize=9,
               labelcolor=INK_SECONDARY, bbox_to_anchor=(0.5, 0.0))
    # Position the header in inches from the top, not in figure fractions: the
    # figure height scales with the number of rows, so a fixed fraction puts the
    # subtitle on top of the title once the grid is short.
    height = fig.get_size_inches()[1]
    scale_note = ("Each panel has its own y-scale, so compare models within a panel, "
                  "not magnitudes across panels." if free_y else "All panels share one y-scale.")
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
                  horizon: int, show_ci: bool) -> None:
    """The 14-neighborhood mean. One panel, so the lines are readable at a glance."""
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor(SURFACE)
    style_axes(ax)

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

    ax.set_ylabel("Mean ILI ED visits per 100,000", fontsize=10, color=INK_SECONDARY)
    ax.set_xlabel("Target week", fontsize=10, color=INK_SECONDARY)
    ax.set_title(f"City mean across 14 neighborhoods — {horizon} week"
                 f"{'s' if horizon > 1 else ''} ahead",
                 fontsize=14, color=INK_PRIMARY, loc="left", pad=26)
    ax.text(0, 1.03, subtitle(show_ci), transform=ax.transAxes,
            fontsize=8, color=INK_MUTED)
    style_dates(ax)
    ax.legend(handles=legend_handles(models, show_ci=show_ci), loc="upper left",
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
    parser.add_argument("--shared-y", action="store_true",
                        help="One y-scale for every panel (comparable, but squashes "
                             "the smaller neighborhoods).")
    parser.add_argument("--results-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--out-dir", type=Path, default=paths.COMPARISON_DIR)
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
    print(f"Overlaying {len(models)} models on {len(neighborhoods)} neighborhoods "
          f"at horizon {args.horizon}:")
    out = args.out_dir.resolve()
    plot_grid(frames, models, neighborhoods, out / f"forecast_overlay_h{args.horizon}.png",
              horizon=args.horizon, show_ci=show_ci, free_y=not args.shared_y)
    plot_citywide(frames, models, out / f"forecast_citywide_h{args.horizon}.png",
                  horizon=args.horizon, show_ci=show_ci)


if __name__ == "__main__":
    main()
