"""Compute the Rt growth index and show what it actually looks like.

Produces results/_diagnostics/rt_by_neighborhood.png and rt_weekly.csv, plus a
leakage check and a redundancy check against the plain week-over-week growth
ratio. Run this before deciding whether Rt is worth using as a model feature.

    python Code/run_rt_diagnostics.py
"""

from __future__ import annotations

import argparse

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.stats import pearsonr, spearmanr
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}.") from exc

from influenza import NEIGHBORHOODS, SHORT_NAMES, load_rates, paths, variant_data
from influenza.cities import get as get_city
from influenza.cli import add_city_arg
from influenza.palette import (
    ACTUAL, INK_MUTED, INK_PRIMARY, INK_SECONDARY, SEASON, SEASON_ALPHA,
    SURFACE, series_colour, style_axes,
)
from influenza.plots import _flu_season_spans
from influenza.rt import growth_ratio, weekly_rt


def style_dates(ax, months: int = 6) -> None:
    """Half-yearly ticks; monthly labels collide at this panel width."""
    import matplotlib.dates as mdates

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=months))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))


def leakage_check(rates: pd.DataFrame, truncate_weeks: int = 12) -> tuple[float, int]:
    """Recompute Rt on a truncated series; earlier values must not move.

    This is the test that the trailing-smoothing change actually worked. With
    epyestim's default centred smoothing, dropping the last weeks shifts values
    well before the cut.
    """
    full = weekly_rt(rates, use_cache=False)
    short = weekly_rt(rates.iloc[:-truncate_weeks], use_cache=False)
    common = short.index
    difference = (full.loc[common] - short).abs().to_numpy()
    finite = difference[np.isfinite(difference)]
    return (float(finite.max()) if finite.size else float("nan")), int(finite.size)


def redundancy_check(rt: pd.DataFrame, rates: pd.DataFrame) -> tuple[float, float]:
    ratio = growth_ratio(rates)
    a = rt.to_numpy().ravel()
    b = np.log(np.clip(ratio.to_numpy().ravel(), 1e-6, None))
    keep = np.isfinite(a) & np.isfinite(b)
    if keep.sum() < 10:
        return float("nan"), float("nan")
    return float(pearsonr(a[keep], b[keep])[0]), float(spearmanr(a[keep], b[keep])[0])


def save_plot(rt: pd.DataFrame, rates: pd.DataFrame, path: str) -> None:
    """One panel per neighborhood, Rt only, on a single shared scale."""
    spans = _flu_season_spans(rates.index)
    fig, axes = plt.subplots(4, 4, figsize=(20, 13), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    for ax, neighborhood in zip(axes.flat, NEIGHBORHOODS):
        style_axes(ax)
        for low, high in spans:
            ax.axvspan(low, high, color=SEASON, alpha=SEASON_ALPHA, lw=0, zorder=0)
        ax.axhline(1.0, color=INK_MUTED, ls=":", lw=1, zorder=1)
        ax.plot(rt.index, rt[neighborhood], color=series_colour(0), lw=1.4, zorder=3)
        ax.set_ylim(0.6, 2.2)
        ax.set_title(SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)], fontsize=10,
)
        ax.tick_params(axis="x", labelsize=7)
        style_dates(ax, months=12)
    for ax in axes.flat[len(NEIGHBORHOODS):]:
        ax.axis("off")
    fig.supylabel("Rt growth index", fontsize=10, color=INK_SECONDARY)
    fig.suptitle("Rt growth index by neighborhood", fontsize=14)
    print("note: gold bands mark the flu season; the dotted line is Rt = 1. This is a "
          "growth index computed from an interpolated weekly rate, not a reproduction "
          "number -- see docs/RT_CAVEATS.md.", file=sys.stderr)
    fig.tight_layout(rect=(0.015, 0, 1, 0.945))
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def save_paired_plot(rt: pd.DataFrame, rates: pd.DataFrame, path: str,
                     neighborhoods: list[str]) -> None:
    """Rt above its own ILI curve, as stacked panels sharing one x-axis.

    Deliberately NOT a twin y-axis. Two measures on different scales in one frame
    invite a reader to compare their heights, which means nothing -- the apparent
    lead or lag between the two curves would depend entirely on where the two
    scales happened to be pinned. Stacked panels share the time axis, which is
    the only axis the comparison actually needs.
    """
    spans = _flu_season_spans(rates.index)
    fig, axes = plt.subplots(2, len(neighborhoods), figsize=(5.2 * len(neighborhoods), 6.4),
                             sharex=True, squeeze=False,
                             gridspec_kw={"height_ratios": [1, 1], "hspace": 0.12})
    fig.patch.set_facecolor(SURFACE)

    for column, neighborhood in enumerate(neighborhoods):
        top, bottom = axes[0][column], axes[1][column]
        for ax in (top, bottom):
            style_axes(ax)
            for low, high in spans:
                ax.axvspan(low, high, color=SEASON, alpha=SEASON_ALPHA, lw=0, zorder=0)
        top.axhline(1.0, color=INK_MUTED, ls=":", lw=1, zorder=1)
        top.plot(rt.index, rt[neighborhood], color=series_colour(0), lw=1.5, zorder=3)
        top.set_ylim(0.6, 2.2)
        top.set_title(SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)], fontsize=11,
)
        bottom.plot(rates.index, rates[neighborhood], color=ACTUAL, lw=1.5, zorder=3)
        bottom.tick_params(axis="x", labelsize=8)
        style_dates(bottom, months=12)
        if column == 0:
            top.set_ylabel("Rt growth index", fontsize=9, color=INK_SECONDARY)
            bottom.set_ylabel("ILI per 100,000", fontsize=9, color=INK_SECONDARY)

    fig.suptitle("Rt growth index against the epidemic curve it was computed from",
                 fontsize=13)
    print("note: stacked panels share one time axis rather than a twin y-axis -- the two "
          "measures have different units, so only their timing is comparable.",
          file=sys.stderr)
    fig.tight_layout(rect=(0, 0, 1, 0.925))
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--variant", default="post_covid",
                        choices=["post_covid", "exclude_covid", "full"])
    parser.add_argument("--skip-leakage-check", action="store_true",
                        help="The leakage check recomputes Rt twice without the cache.")
    args = parser.parse_args()

    global NEIGHBORHOODS, SHORT_NAMES
    city = get_city(args.city)
    if args.variant not in city.variants:
        raise SystemExit(f"--variant {args.variant} is not available for {city.label}. "
                         f"{city.label} supports: {', '.join(city.variants)}.")
    NEIGHBORHOODS = list(city.node_names)
    SHORT_NAMES = list(city.short_names)

    rates = variant_data(city.loaders.load_rates(), args.variant).available
    print(f"Computing Rt for {rates.shape[1]} neighborhoods over {len(rates)} weeks...")
    rt = weekly_rt(rates)

    out = paths.city_root(city.name) / paths.DIAGNOSTICS_DIR.name
    out.mkdir(parents=True, exist_ok=True)
    rt.to_csv(out / "rt_weekly.csv")
    save_plot(rt, rates, str(out / "rt_by_neighborhood.png"))
    # Four nodes spanning the range of case volumes. Picked from the data
    # rather than named, so this works for any city: the four Boston names
    # that used to be hardcoded here were the highest, second, and two low
    # ones, which is exactly what the quantile pick reproduces.
    ranked = rates.mean().sort_values(ascending=False).index.tolist()
    picks = [ranked[i] for i in dict.fromkeys(
        [0, 1, max(0, len(ranked) - 2), len(ranked) - 1])]
    save_paired_plot(rt, rates, str(out / "rt_vs_incidence.png"), picks)

    values = rt.to_numpy().ravel()
    values = values[np.isfinite(values)]
    print(f"\nRt: median {np.median(values):.3f}, "
          f"5th-95th percentile [{np.percentile(values, 5):.3f}, {np.percentile(values, 95):.3f}], "
          f"share above 1: {(values > 1).mean() * 100:.1f}%")

    pearson, spearman = redundancy_check(rt, rates)
    print(f"Against plain week-over-week log growth: Pearson {pearson:.3f}, Spearman {spearman:.3f}")
    print("  A strong positive relationship would mean Rt is a re-encoding of the")
    print("  growth ratio; a weak or negative one means much of its structure comes")
    print("  from the weekly-to-daily interpolation rather than the epidemic.")

    if not args.skip_leakage_check:
        drift, n = leakage_check(rates)
        print(f"\nCausality check: truncating the last 12 weeks changes earlier Rt values "
              f"by at most {drift:.2e} across {n} cells.")
        print("  Should be ~0. A non-trivial number means smoothing is still reading forward.")

    print(f"\nOutputs: {out}")
    print("Interpretation caveats: docs/RT_CAVEATS.md")


if __name__ == "__main__":
    main()
