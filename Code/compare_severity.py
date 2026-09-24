"""Did the forecast say the week would be bad, and did it say so in time?

`compare_models.py` ranks models on how close the number was. This ranks them on
whether they called the CDC-style severity band and the timing of the threshold
crossings -- a different question, and the one a public-health reader asks.

Thresholds come from `influenza/severity.py` (Moving Epidemic Method, CDC's
IT50/IT90/IT98 levels). Everything is read from the predictions.csv files
already on disk, so no model is re-run:

    python Code/compare_severity.py --results-dir Code/results/horizon_01
    python Code/compare_severity.py --results-dir Code/results/horizon_01 --variant post_covid
    python Code/compare_severity.py --reference-seasons exclude_covid    # sensitivity
    python Code/compare_severity.py --values-per-season 1               # CDC-literal peak week

Outputs land in a `_comparison/` beside the results being read, so each horizon
keeps its own set.
"""

from __future__ import annotations

import argparse
import math
import json
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
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas numpy matplotlib scipy.") from exc

from compare_models import _cells_scored, _markdown_table, update_readme
from influenza import paths, severity
from influenza.cities import get as get_city
from influenza.cli import add_city_arg, city_results_dir
from influenza.constants import NEIGHBORHOODS, SHORT_NAMES, TEST_END, TEST_START
from influenza.intervals import Z95
from influenza.metrics import segment_labels
from influenza.palette import (
    ACTUAL,
    ACTUAL_WIDTH,
    AXIS,
    INK_MUTED,
    INK_PRIMARY,
    INK_SECONDARY,
    LINE_WIDTH,
    SERIES,
    SEVERITY_WASH,
    SURFACE,
    marker,
    series_colour,
    style_axes,
)
from plot_forecasts import load_predictions, style_dates

SHORT = dict(zip(NEIGHBORHOODS, SHORT_NAMES))

# Four models, because palette.series_colour raises beyond four validated slots.
DEFAULT_PLOT_MODELS = ["persistence", "seasonal_naive", "arima", "gnn_st"]

ALL_SEGMENTS = "overall,flu_season"
CITY = None  # the City being analysed; set in main()

SEGMENT_LABELS = {
    "overall": "Overall (full year)",
    "flu_season": "Flu season (Oct–Mar)",
    "off_season": "Off-season (Apr–Sep)",
}
SCOPES = ("citywide", "pooled", "neighborhood")
SCOPE_LABELS = {
    "citywide": "Citywide indicator",
    "pooled": "All neighborhood-weeks pooled",
    "neighborhood": "Per neighborhood",
}

# Higher is better. Everything else in the tables is an error or a rate where
# lower is better, or a bias where nearer zero is better.
DESCENDING = {
    "POD", "precision", "CSI", "F1", "PSS", "HSS", "MCC", "accuracy", "BSS",
    "exact_band", "within_one_band", "kappa_quadratic",
}
RANKABLE = ["PSS", "CSI", "F1", "HSS", "MCC", "BSS", "POD", "precision"]

CONTINGENCY_COLUMNS = ["n_obs", "n_events", "base_rate", "hits", "false_alarms",
                       "misses", "correct_neg", "POD", "FAR", "precision", "FPR",
                       "CSI", "F1", "PSS", "HSS", "MCC", "accuracy", "frequency_bias"]
BAND_COLUMNS = ["exact_band", "within_one_band", "kappa_quadratic", "mean_band_error"]
BRIER_COLUMNS = ["brier", "brier_ref", "BSS"]

README_BEGIN = "<!-- BEGIN SEVERITY -->"
README_END = "<!-- END SEVERITY -->"


# --- discovery ---------------------------------------------------------------

def discover_runs(results_root: Path) -> list[tuple[str, str]]:
    """(model, variant) pairs that have a predictions.csv, '_' dirs skipped."""
    found = sorted(
        path for path in results_root.glob("*/*/predictions.csv")
        if not any(part.startswith("_") for part in path.relative_to(results_root).parts)
    )
    return [(path.parent.parent.name, path.parent.name) for path in found]


def horizon_roots(results_root: Path) -> list[Path]:
    roots = [p for p in results_root.glob("horizon_*") if p.is_dir() and discover_runs(p)]
    return sorted(roots, key=lambda p: int(p.name.split("_")[1]))


def resolve_horizon(results_root: Path, runs: list[tuple[str, str]],
                    requested: int | None) -> int:
    """Infer the horizon when the tree holds exactly one, as compare_models does."""
    horizons: set[int] = set()
    for model, variant in runs:
        frame = pd.read_csv(results_root / model / variant / "predictions.csv",
                            usecols=["horizon"])
        horizons.update(int(h) for h in frame["horizon"].unique())
    if requested is not None:
        if requested not in horizons:
            raise SystemExit(f"error: horizon {requested} not in these results; "
                             f"available: {sorted(horizons)}")
        return requested
    if len(horizons) == 1:
        return horizons.pop()
    raise SystemExit(f"error: these results hold horizons {sorted(horizons)}; "
                     f"pass --horizon to pick one.")


# --- turning predictions into severity statements ---------------------------

def indicator_frame(predictions: pd.DataFrame, fitted: dict[str, severity.Thresholds],
                    *, citywide_sigma: str) -> pd.DataFrame:
    """One row per (indicator, target week), with band codes and exceedance
    probabilities for every level.

    The citywide indicator is the unweighted mean across neighborhoods, matching
    how its threshold was fitted. Its predictive spread is the **mean** of the
    per-neighborhood spreads, not sigma/sqrt(n): neighborhood forecast errors in
    this data move together, driven by the same citywide epidemic, so treating
    them as independent would shrink the band by nearly a factor of four and
    manufacture confidence the models have not earned.
    """
    frame = predictions.loc[:, ["target_date", "neighborhood", "actual", "predicted", "upper"]].copy()
    frame["sigma"] = severity.predictive_sigma(frame["predicted"], frame["upper"], z=Z95)
    frame = frame.rename(columns={"neighborhood": "indicator"})

    weekly = frame.groupby("target_date", sort=True)
    if citywide_sigma == "independent":
        sigma = weekly["sigma"].apply(lambda s: float(np.sqrt(np.nansum(s ** 2)) / max(s.notna().sum(), 1)))
    else:
        sigma = weekly["sigma"].mean()
    citywide = pd.DataFrame({
        "target_date": sigma.index,
        "indicator": severity.CITYWIDE,
        "actual": weekly["actual"].mean().to_numpy(),
        "predicted": weekly["predicted"].mean().to_numpy(),
        "sigma": sigma.to_numpy(),
    })
    citywide["upper"] = citywide["predicted"] + Z95 * citywide["sigma"]

    combined = pd.concat([frame, citywide], ignore_index=True)
    # A suppressed week is not an observation. Dropping here keeps every layer
    # below working on the same rows.
    combined = combined.loc[combined["actual"].notna() & combined["predicted"].notna()]
    combined["segment"] = segment_labels(combined["target_date"], CITY.flu_months)
    combined["season"] = severity.season_label(combined["target_date"],
                                               CITY.season_start_month)

    parts = []
    for name, part in combined.groupby("indicator", sort=False):
        thresholds = fitted.get(name)
        if thresholds is None:
            continue
        part = part.copy()
        part["true_band"] = thresholds.band(part["actual"].to_numpy())
        part["pred_band"] = thresholds.band(part["predicted"].to_numpy())
        for level in thresholds.levels:
            cut = thresholds.values[level]
            tag = f"{level * 100:g}"
            part[f"exceed_true_{tag}"] = part["actual"].to_numpy() >= cut
            part[f"exceed_pred_{tag}"] = part["predicted"].to_numpy() >= cut
            part[f"p_exceed_{tag}"] = severity.exceedance_probability(
                part["predicted"].to_numpy(), part["upper"].to_numpy(), cut, z=Z95)
        parts.append(part)
    if not parts:
        raise SystemExit("error: no indicator in the predictions has fitted thresholds.")
    return pd.concat(parts, ignore_index=True)


def series_labels(frame: pd.DataFrame) -> np.ndarray:
    """'model' when a model appears once, 'model/variant' when it has several.

    The figures key on this rather than on `model`. Without it, running without
    --variant puts two rows under one model name, which silently pools two
    different runs into one bar -- or, where the plot reindexes, crashes.
    """
    variants = frame.groupby("model")["variant"].transform("nunique")
    return np.where(variants > 1, frame["model"] + "/" + frame["variant"], frame["model"])


def _scope_groups(bands: pd.DataFrame, scope: str):
    """(indicator label, rows) for one scope."""
    if scope == "citywide":
        part = bands.loc[bands["indicator"].eq(severity.CITYWIDE)]
        if not part.empty:
            yield severity.CITYWIDE, part
    elif scope == "pooled":
        part = bands.loc[~bands["indicator"].eq(severity.CITYWIDE)]
        if not part.empty:
            yield "ALL", part
    elif scope == "neighborhood":
        part = bands.loc[~bands["indicator"].eq(severity.CITYWIDE)]
        for name, rows in part.groupby("indicator", sort=False):
            yield name, rows
    else:
        raise ValueError(f"Unknown scope: {scope!r}")


def score(bands: pd.DataFrame, fitted: dict[str, severity.Thresholds], *,
          model: str, variant: str, horizon: int, scopes: list[str],
          segments: list[str], levels: tuple[float, ...]) -> pd.DataFrame:
    """Long-form severity scores: one row per (scope, indicator, segment, level).

    Band-agreement rows carry `label='bands'` and an empty `level`, because they
    describe all four bands at once rather than one crossing. Repeating them on
    every level row would invite a reader to average the same number three times.
    """
    rows: list[dict] = []
    for scope in scopes:
        for indicator, all_rows in _scope_groups(bands, scope):
            # Pooled rows span 14 different thresholds, so no single number
            # belongs in the `threshold` column for them.
            reference = None if scope == "pooled" else fitted[indicator]
            for segment in segments:
                part = (all_rows if segment == "overall"
                        else all_rows.loc[all_rows["segment"].eq(segment)])
                if part.empty:
                    continue
                identity = {"model": model, "variant": variant, "horizon": horizon,
                            "scope": scope, "indicator": indicator, "segment": segment}

                agreement = severity.band_agreement(part["true_band"].to_numpy(),
                                                    part["pred_band"].to_numpy())
                rows.append({**identity, "level": np.nan, "label": "bands",
                             "threshold": np.nan, **agreement,
                             "underpowered": agreement["n_obs"] < 1})

                for level in levels:
                    tag = f"{level * 100:g}"
                    observed = part[f"exceed_true_{tag}"].to_numpy()
                    forecast = part[f"exceed_pred_{tag}"].to_numpy()
                    table = severity.contingency(observed, forecast)
                    brier = severity.brier_scores(observed.astype(float),
                                                 part[f"p_exceed_{tag}"].to_numpy())
                    # A threshold nothing crossed cannot rank anything. Say so
                    # rather than emitting a zero that reads as 'no skill'.
                    rows.append({
                        **identity, "level": level, "label": f"IT{tag}",
                        "threshold": np.nan if reference is None else reference.values[level],
                        **table, **brier,
                        "underpowered": table["n_events"] < 5,
                    })
    return pd.DataFrame(rows)


def timing(bands: pd.DataFrame, fitted: dict[str, severity.Thresholds], *,
           model: str, variant: str, horizon: int, levels: tuple[float, ...]) -> pd.DataFrame:
    """Onset, peak and lead time per (indicator, season, level)."""
    rows: list[dict] = []
    for indicator, part in bands.groupby("indicator", sort=False):
        thresholds = fitted.get(indicator)
        if thresholds is None:
            continue
        for season, season_rows in part.groupby("season", sort=True):
            for level in levels:
                if level not in thresholds.values:
                    continue
                result = severity.timing_row(
                    season_rows["target_date"], season_rows["actual"],
                    season_rows["predicted"], thresholds.values[level],
                )
                rows.append({
                    "model": model, "variant": variant, "horizon": horizon,
                    "indicator": indicator, "season": severity.season_name(int(season)),
                    "level": level, "label": f"IT{level * 100:g}",
                    "threshold": thresholds.values[level], **result,
                })
    return pd.DataFrame(rows)


# --- plots -------------------------------------------------------------------

def plot_bands(rates: pd.DataFrame, fitted: dict[str, severity.Thresholds],
               path: Path, *, test_start: pd.Timestamp, test_end: pd.Timestamp,
               reference_note: str, standardise: bool = True) -> None:
    """The CDC-style figure: observed rate against intensity bands.

    Standardised by default -- one y scale and one set of bands (the citywide
    set) on every panel, so the panels can be read against each other. With
    `standardise=False` each panel gets its own thresholds and its own scale,
    which is what the scoring actually uses; the trade is that no two panels are
    then on the same axis.
    """
    citywide = severity.citywide_series(rates)
    panels = [(severity.CITYWIDE, citywide)] + [(n, rates[n]) for n in NEIGHBORHOODS]
    panels = [(name, series) for name, series in panels if name in fitted]
    common = fitted[severity.CITYWIDE] if standardise else None
    common_ceiling = (severity.shared_ceiling(rates, common, window=(test_start, test_end))
                      if standardise else None)

    # One shared x range, so a panel whose first weeks were suppressed is not
    # silently drawn on a different timeline from its neighbours.
    span = rates.loc[(rates.index >= test_start) & (rates.index <= test_end)].index
    span = span if len(span) else rates.index

    # One cell per panel plus one for the legend, four across. Boston's 15
    # panels + legend fill the historical 4x4 exactly (same figure size); a
    # fixed 4x4 has no room for Columbus's 18 or Buenos Aires's 20.
    rows = math.ceil((len(panels) + 1) / 4)
    fig, axes = plt.subplots(rows, 4, figsize=(19, 3.25 * rows), facecolor=SURFACE,
                             squeeze=False)
    for ax, (name, series) in zip(axes.flat, panels):
        thresholds = common or fitted[name]
        window = series.loc[(series.index >= test_start) & (series.index <= test_end)].dropna()
        if window.empty:
            window = series.dropna()
        ceiling = common_ceiling or severity.panel_ceiling(window, thresholds)
        for low, high, rank in severity.band_spans(thresholds, ceiling):
            ax.axhspan(low, min(high, ceiling), color=SEVERITY_WASH[rank], lw=0, zorder=0)
        for level in thresholds.levels[0:]:
            ax.axhline(thresholds.values[level], color=INK_MUTED, lw=0.7, ls=":", zorder=2)
        ax.plot(window.index, window.to_numpy(), color=ACTUAL, lw=ACTUAL_WIDTH, zorder=3)
        peak = window.idxmax()
        ax.plot([peak], [window.max()], "o", color=ACTUAL, ms=4.5, zorder=4)
        band = severity.SEVERITY_BANDS[int(thresholds.band([window.max()])[0])]
        # Offset clear of the curve: the peak sits at the top of a steep rise,
        # so a label placed on the point lands on the descending limb. The
        # rounded bbox this used to wear is gone with the rest of the chrome.
        ax.annotate(f"{window.max():.0f} — {band}", (peak, window.max()),
                    textcoords="offset points", xytext=(7, 7), fontsize=7,
                    zorder=5)
        ax.set_ylim(0, ceiling)
        ax.set_xlim(span.min(), span.max())
        ax.set_title(SHORT.get(name, name), fontsize=8.5, color=INK_PRIMARY)
        style_axes(ax, grid_axis="y")
        style_dates(ax)
    for ax in axes.flat[len(panels):]:
        ax.axis("off")

    handles = [plt.Rectangle((0, 0), 1, 1, color=SEVERITY_WASH[i], label=label)
               for i, label in enumerate(
                   [f"low (<{thresholds.values[thresholds.levels[0]]:.0f})"]
                   + [f"{band} (≥{value:.0f})"
                      for value, band in severity.band_entry_labels(thresholds)])]
    handles.append(Line2D([0], [0], color=ACTUAL, lw=ACTUAL_WIDTH, label="Observed rate"))
    axes.flat[len(panels)].legend(handles=handles, loc="center", fontsize=8, frameon=False)

    fig.suptitle("Observed ILI ED visit rate against MEM intensity bands", fontsize=13)
    print(f"note: {reference_note}", file=sys.stderr)
    fig.supylabel("ILI ED visits per 100,000", color=INK_SECONDARY, fontsize=9)
    fig.tight_layout(rect=(0.01, 0.0, 1.0, 0.935))
    _save(fig, path)


def plot_skill(long: pd.DataFrame, path: Path, *, scope: str, segment: str,
               metric: str, models: list[str]) -> None:
    """Skill per model per threshold, with the no-skill line marked."""
    part = long.loc[long["scope"].eq(scope) & long["segment"].eq(segment)
                    & long["label"].str.startswith("IT") & long["series"].isin(models)]
    if part.empty:
        return
    labels = [lab for lab in ("IT50", "IT90", "IT98") if lab in set(part["label"])]
    order = [m for m in models if m in set(part["series"])]

    fig, ax = plt.subplots(figsize=(9, 4.4), facecolor=SURFACE)
    width = 0.8 / max(len(labels), 1)
    for index, label in enumerate(labels):
        view = part.loc[part["label"].eq(label)].set_index("series").reindex(order)
        events = view["n_events"].fillna(0).astype(int)
        positions = np.arange(len(order)) + index * width - 0.4 + width / 2
        bars = ax.bar(positions, view[metric].to_numpy(), width * 0.92,
                      color=series_colour(index),
                      label=f"{label} ({int(events.max()) if len(events) else 0} events)")
        for rect, flag in zip(bars, view["underpowered"].fillna(True)):
            if flag:
                ax.text(rect.get_x() + rect.get_width() / 2,
                        (rect.get_height() if np.isfinite(rect.get_height()) else 0) + 0.01,
                        "!", ha="center", fontsize=8, color=INK_MUTED)
    ax.axhline(0.0, color=INK_SECONDARY, lw=1.0)
    ax.set_xticks(np.arange(len(order)))
    ax.set_xticklabels(order, rotation=18, ha="right", fontsize=8)
    ax.set_ylabel(metric, color=INK_SECONDARY, fontsize=9)
    ax.set_title(f"{metric} by intensity threshold — {SCOPE_LABELS[scope]}, "
                 f"{SEGMENT_LABELS.get(segment, segment)}", fontsize=11, color=INK_PRIMARY)
    style_axes(ax)
    ax.legend(fontsize=8, frameon=False, ncol=3)
    # Caption printed rather than drawn: plain figures carry no paragraphs.
    print(f"note ({path.name}): " + "0 is no skill: both 'never alert' and 'always alert' score 0. "
                        "! marks a threshold with fewer than 5 observed events.", file=sys.stderr)
    _save(fig, path)


def plot_reliability(bands: dict[str, pd.DataFrame], models: list[str], path: Path, *,
                     level: float, scope: str) -> None:
    """Are the exceedance probabilities honest?

    `models` fixes the colour order. Without it the slots would follow dict
    insertion order and a model would wear one colour here and another on the
    skill and timing figures, which is the exact failure palette.py warns about.
    """
    tag = f"{level * 100:g}"
    fig, ax = plt.subplots(figsize=(5.6, 5.4), facecolor=SURFACE)
    ax.plot([0, 1], [0, 1], color=INK_MUTED, lw=1.0, ls="--", zorder=1)
    drawn = False
    for index, model in enumerate(models):
        frame = bands.get(model)
        if frame is None:
            continue
        part = (frame.loc[frame["indicator"].eq(severity.CITYWIDE)] if scope == "citywide"
                else frame.loc[~frame["indicator"].eq(severity.CITYWIDE)])
        if part.empty:
            continue
        curve = severity.reliability_curve(part[f"exceed_true_{tag}"].to_numpy(float),
                                           part[f"p_exceed_{tag}"].to_numpy())
        curve = curve.loc[curve["n_obs"] > 0]
        ax.plot(curve["mean_forecast"], curve["observed_frequency"],
                color=series_colour(index), lw=LINE_WIDTH, marker=marker(index),
                ms=5, markeredgewidth=0, label=model, zorder=3)
        drawn = True
    if not drawn:
        plt.close(fig)
        return
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xlabel(f"Forecast P(rate ≥ IT{tag})", color=INK_SECONDARY, fontsize=9)
    ax.set_ylabel("Observed frequency", color=INK_SECONDARY, fontsize=9)
    ax.set_title(f"Reliability at IT{tag} — {SCOPE_LABELS[scope]}", fontsize=11,
                 color=INK_PRIMARY)
    style_axes(ax, grid_axis="both")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    # Caption printed rather than drawn: plain figures carry no paragraphs.
    print(f"note ({path.name}): " + "On the diagonal the stated probability matches how often it happened. "
                        "Below it the model is over-confident.", file=sys.stderr)
    _save(fig, path)


def plot_timing(frame: pd.DataFrame, path: Path, *, level: float, models: list[str]) -> None:
    """Onset-error distribution per model, in weeks."""
    part = frame.loc[frame["level"].eq(level) & frame["series"].isin(models)
                     & ~frame["indicator"].eq(severity.CITYWIDE)
                     & frame["onset_error_weeks"].notna()]
    if part.empty:
        return
    order = [m for m in models if m in set(part["series"])]

    fig, ax = plt.subplots(figsize=(8.4, 4.2), facecolor=SURFACE)
    rng = np.random.default_rng(0)
    for index, model in enumerate(order):
        values = part.loc[part["series"].eq(model), "onset_error_weeks"].to_numpy(float)
        ax.scatter(values, np.full(values.size, index) + rng.uniform(-0.14, 0.14, values.size),
                   color=series_colour(index), s=26, marker=marker(index),
                   linewidths=0, alpha=0.85, zorder=3)
        ax.plot([np.median(values)], [index], "|", color=INK_PRIMARY, ms=22, mew=2, zorder=4)
    ax.axvline(0.0, color=INK_SECONDARY, lw=1.0)
    ax.set_yticks(np.arange(len(order)))
    ax.set_yticklabels(order, fontsize=8)
    ax.set_xlabel("Onset error in weeks  (negative = warned early, positive = late)",
                  color=INK_SECONDARY, fontsize=9)
    ax.set_title(f"When did the forecast first cross IT{level * 100:g}?", fontsize=11,
                 color=INK_PRIMARY)
    style_axes(ax, grid_axis="x")
    # Caption printed rather than drawn: plain figures carry no paragraphs.
    print(f"note ({path.name}): " + "One point per neighborhood-season. The bar is the median. "
                        "Neighborhood-seasons where neither series crossed are omitted.", file=sys.stderr)
    _save(fig, path)


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {paths.display(path)}")


# --- markdown ----------------------------------------------------------------

CROSSING_VIEW = ["model", "variant", "n_events", "base_rate", "hits", "misses",
                 "false_alarms", "POD", "FAR", "CSI", "F1", "PSS", "BSS"]

# Counts, not measurements. They arrive as floats because the band-agreement rows
# leave them empty, and compare_models._format would render 51 as "51.000".
COUNT_COLUMNS = ("n_obs", "n_events", "hits", "false_alarms", "misses",
                 "correct_neg", "n_seasons_crossed", "n_weeks")


def _table(view: pd.DataFrame) -> list[str]:
    """_markdown_table, with count columns kept as integers."""
    view = view.copy()
    for column in view.columns:
        if column in COUNT_COLUMNS:
            view[column] = view[column].astype("Int64")
    return _markdown_table(view)


def _events_note(count: int) -> str:
    plural = "event" if count == 1 else "events"
    return f" — **underpowered: {count} observed {plural}**, not ranked"


def timing_summary(frame: pd.DataFrame, *, level: float) -> pd.DataFrame:
    """Per-model timing, aggregated over neighborhood-seasons.

    The median, not the mean: a neighborhood-season where the model never
    crossed the threshold contributes no onset error at all, and the handful
    that do cross are a small enough sample for one outlier to move a mean.
    """
    part = frame.loc[frame["level"].eq(level) & ~frame["indicator"].eq(severity.CITYWIDE)]
    if part.empty:
        return pd.DataFrame()
    grouped = part.groupby(["model", "variant"], sort=False, observed=True)
    summary = pd.DataFrame({
        "n_seasons_crossed": grouped["onset_error_weeks"].count(),
        "median_onset_error_weeks": grouped["onset_error_weeks"].median(),
        "median_lead_time_weeks": grouped["lead_time_weeks"].median(),
        "mean_abs_onset_error": grouped["onset_error_weeks"].apply(lambda s: s.abs().mean()),
        "median_peak_week_error": grouped["peak_week_error_weeks"].median(),
        "median_peak_error": grouped["peak_error"].median(),
    }).reset_index()
    return summary.sort_values("mean_abs_onset_error")


def leaderboard_markdown(long: pd.DataFrame, timings: pd.DataFrame,
                         fitted: dict[str, severity.Thresholds],
                         args: argparse.Namespace, warnings: list[str]) -> str:
    scopes = [s.strip() for s in args.scope.split(",")]
    segments = [s.strip() for s in args.segment.split(",")]
    ascending = args.rank_by not in DESCENDING
    citywide = fitted[severity.CITYWIDE]

    lines = [
        f"Severity thresholds from the {len(citywide.reference_seasons)} reference "
        f"seasons {', '.join(severity.season_name(y) for y in citywide.reference_seasons)}, "
        f"fitted on weeks before {citywide.fitted_through}, "
        f"levels {'/'.join(f'IT{l * 100:g}' for l in citywide.levels)}, "
        f"{citywide.values_per_season} values per season "
        f"({citywide.n_pooled} pooled). Horizon {args.horizon}, ranked by "
        f"**{args.rank_by}**.",
        "",
        "**PSS (Peirce skill score) leads these tables because it is 0 for both "
        "trivial forecasts.** At an 8% base rate, never alerting scores 92% "
        "accuracy and always alerting scores a perfect POD of 1.0; PSS gives both "
        "of them nothing. CSI and F1 sit beside it because PSS is measured against "
        "a large correct-negative count and moves little when a model raises many "
        "false alarms in absolute terms — CSI ignores correct negatives entirely "
        "and will show that.",
        "",
        "Citywide thresholds: "
        + ", ".join(f"IT{l * 100:g} = {citywide.values[l]:.1f}" for l in citywide.levels)
        + " per 100,000.",
        "",
    ]

    for scope in scopes:
        if scope == "neighborhood":
            continue  # too many rows for the headline document; it is in the CSV
        scoped = long.loc[long["scope"].eq(scope)]
        if scoped.empty:
            continue
        lines += [f"# {SCOPE_LABELS[scope]}", ""]
        for segment in segments:
            part = scoped.loc[scoped["segment"].eq(segment)]
            if part.empty:
                continue
            lines += [f"## {SEGMENT_LABELS.get(segment, segment)}", ""]

            for label in ("IT50", "IT90", "IT98"):
                view = part.loc[part["label"].eq(label)]
                if view.empty:
                    continue
                events = int(view["n_events"].max())
                note = ""
                if bool(view["underpowered"].any()):
                    note = _events_note(events)
                    view = view.sort_values("n_events", ascending=False)
                else:
                    view = view.sort_values(args.rank_by, ascending=ascending)
                lines += [f"### Crossing {label}{note}", ""]
                columns = [c for c in CROSSING_VIEW if c in view.columns]
                lines += [*_table(view[columns]), ""]

            agreement = part.loc[part["label"].eq("bands")]
            if not agreement.empty:
                agreement = agreement.sort_values("exact_band", ascending=False)
                lines += ["### All four bands"
                          f"{_cells_scored(agreement, unit='weeks')}", "",
                          "*`mean_band_error` above zero means the model calls severity "
                          "higher than it turned out to be.*", ""]
                columns = ["model", "variant", "n_obs", *BAND_COLUMNS]
                lines += [*_table(agreement[columns]), ""]

    if not timings.empty:
        summary = timing_summary(timings, level=args.timing_level)
        if not summary.empty:
            lines += [f"# Timing at IT{args.timing_level * 100:g}", "",
                      "Per neighborhood-season, over the neighborhood indicators. "
                      "Negative onset error means the forecast crossed the threshold "
                      "*before* the observation did, so positive lead time is a warning "
                      "in advance.", "",
                      *_table(summary), ""]

    if warnings:
        lines += ["# Notes", ""] + [f"- {w}" for w in warnings] + [""]
    return "\n".join(lines)


def readme_markdown(long: pd.DataFrame, fitted: dict[str, severity.Thresholds],
                    args: argparse.Namespace, out: Path) -> str:
    """One compact table: PSS at IT50 and IT90, pooled, plus band accuracy."""
    citywide = fitted[severity.CITYWIDE]
    part = long.loc[long["scope"].eq("pooled") & long["segment"].eq("overall")]
    pieces = []
    for label in ("IT50", "IT90"):
        view = part.loc[part["label"].eq(label), ["model", "variant", "PSS", "CSI"]]
        if view.empty:
            continue
        pieces.append(view.rename(columns={"PSS": f"PSS ({label})", "CSI": f"CSI ({label})"})
                      .set_index(["model", "variant"]))
    bands = part.loc[part["label"].eq("bands"), ["model", "variant", "exact_band"]]
    if not bands.empty:
        pieces.append(bands.rename(columns={"exact_band": "band exact"})
                      .set_index(["model", "variant"]))
    if not pieces:
        return "No severity scores available.\n"

    table = pd.concat(pieces, axis=1).reset_index()
    sort_col = "PSS (IT50)"
    if sort_col in table.columns:
        table = table.sort_values(sort_col, ascending=False)

    try:
        rel = out.relative_to(paths.ROOT).as_posix()
    except ValueError:
        rel = out.as_posix()

    return "\n".join([
        f"Horizon {args.horizon}, all neighborhood-weeks pooled, full year. "
        f"Thresholds from {', '.join(severity.season_name(y) for y in citywide.reference_seasons)}, "
        f"fitted on weeks before {citywide.fitted_through}.",
        "",
        *_table(table),
        "",
        "PSS (Peirce skill score) is 0 for both a never-alert and an always-alert "
        "forecast, so it cannot be gamed by the 8% base rate. Method and caveats: "
        "[`Code/docs/SEVERITY.md`](Code/docs/SEVERITY.md). Full tables: "
        f"[`{rel}/severity_leaderboard.md`]({rel}/severity_leaderboard.md).",
    ]) + "\n"


# --- CLI ---------------------------------------------------------------------

def parse_levels(text: str) -> tuple[float, ...]:
    try:
        levels = tuple(sorted(float(piece) for piece in text.split(",") if piece.strip()))
    except ValueError as exc:
        raise SystemExit(f"error: --levels must be comma-separated numbers, got {text!r}") from exc
    if not levels or not all(0.0 < level < 1.0 for level in levels):
        raise SystemExit(f"error: --levels must lie strictly between 0 and 1, got {text!r}")
    return levels


def parse_reference_seasons(text: str) -> tuple[int, ...] | None:
    if text in severity.REFERENCE_SEASON_SETS:
        return severity.REFERENCE_SEASON_SETS[text]
    try:
        return tuple(sorted(int(piece) for piece in text.split(",") if piece.strip()))
    except ValueError as exc:
        raise SystemExit(
            f"error: --reference-seasons takes a name "
            f"({', '.join(severity.REFERENCE_SEASON_SETS)}) or comma-separated start years "
            f"like 2022,2023,2024 — got {text!r}"
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Default: a _comparison/ beside the results being read.")
    parser.add_argument("--models", default=None, help="Comma-separated subset.")
    parser.add_argument("--variant", default=None)
    parser.add_argument("--horizon", type=int, default=None,
                        help="Default: inferred when the tree holds exactly one.")
    parser.add_argument("--segment", default=ALL_SEGMENTS,
                        help=f"Comma-separated segments (default: {ALL_SEGMENTS}).")
    parser.add_argument("--scope", default=",".join(SCOPES),
                        help=f"Comma-separated subset of {', '.join(SCOPES)}.")
    parser.add_argument("--rank-by", default="PSS", choices=RANKABLE)
    parser.add_argument("--reference-seasons", default="post_covid",
                        help="Named set (%s) or start years like 2022,2023,2024."
                             % ", ".join(severity.REFERENCE_SEASON_SETS))
    parser.add_argument("--levels", default="0.50,0.90,0.98",
                        help="Intensity levels. CDC uses 0.50,0.90,0.98; MEM's own "
                             "default is 0.40,0.90,0.975.")
    parser.add_argument("--values-per-season", type=int, default=None,
                        help="Highest values taken from each reference season. Default: "
                             "MEM's max(1, round(30 / n_seasons)).")
    parser.add_argument("--use-t", action="store_true", default=True,
                        help="Student-t quantile with mem's sqrt(1+1/m) inflation (default).")
    parser.add_argument("--no-use-t", dest="use_t", action="store_false",
                        help="Normal quantile instead.")
    parser.add_argument("--threshold-end", type=pd.Timestamp, default=None,
                        help="Exclusive cutoff for threshold fitting. Default: the city's test start, "
                             "which is what keeps the test window out of the thresholds.")
    parser.add_argument("--citywide-sigma", default="correlated",
                        choices=["correlated", "independent"])
    parser.add_argument("--plot-models", default=",".join(DEFAULT_PLOT_MODELS),
                        help="Up to four models for the comparison figures.")
    parser.add_argument("--per-neighborhood-scale", action="store_true",
                        help="Draw severity_bands.png with each panel on its own scale and "
                             "its own thresholds, instead of one shared set. Affects the "
                             "figure only -- the scores always use per-neighborhood "
                             "thresholds.")
    parser.add_argument("--timing-level", type=float, default=0.50,
                        help="Which threshold the timing tables use.")
    parser.add_argument("--update-readme", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    global NEIGHBORHOODS, SHORT_NAMES, SHORT, CITY
    city = get_city(args.city)
    CITY = city
    SEGMENT_LABELS.update(city.segment_labels)
    test_start, test_end = city.evaluation_window()
    if args.threshold_end is None:
        args.threshold_end = test_start
    # Node names and the rate series come from the city, not from Boston's
    # module-level constants. Rebound here rather than threaded through every
    # plot function: the call graph is a dozen deep and the names are read-only
    # after this point.
    NEIGHBORHOODS = list(city.node_names)
    SHORT_NAMES = list(city.short_names)
    SHORT = dict(zip(NEIGHBORHOODS, SHORT_NAMES))
    results_root = city_results_dir(args, city).resolve()
    runs = discover_runs(results_root)
    if not runs:
        nested = horizon_roots(results_root)
        if nested:
            listed = "\n".join(f"  python Code/compare_severity.py --results-dir {p}"
                               for p in nested)
            raise SystemExit(f"error: no runs directly under {results_root} — results are "
                             f"split by forecast horizon. Try:\n{listed}")
        raise SystemExit(f"error: no */*/predictions.csv under {results_root}. "
                         f"Run a model first, e.g. python Code/run_all_horizons.py")

    if args.models:
        wanted = {m.strip() for m in args.models.split(",")}
        runs = [(m, v) for m, v in runs if m in wanted]
    if args.variant:
        runs = [(m, v) for m, v in runs if v == args.variant]
    if not runs:
        raise SystemExit("error: no runs matched --models / --variant.")

    horizon = resolve_horizon(results_root, runs, args.horizon)
    args.horizon = horizon
    levels = parse_levels(args.levels)
    scopes = [s.strip() for s in args.scope.split(",")]
    unknown = [s for s in scopes if s not in SCOPES]
    if unknown:
        raise SystemExit(f"error: unknown scope(s) {unknown}; choose from {list(SCOPES)}.")
    segments = [s.strip() for s in args.segment.split(",")]

    out_dir = (args.out_dir or paths.comparison_dir(results_root)).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    # --- thresholds ---------------------------------------------------------
    rates = city.loaders.load_rates()
    reference = parse_reference_seasons(args.reference_seasons)
    fitted = severity.fit_thresholds(
        rates, reference_seasons=reference, threshold_end=args.threshold_end,
        levels=levels, values_per_season=args.values_per_season, use_t=args.use_t,
        season_start_month=city.season_start_month,
    )
    citywide = fitted[severity.CITYWIDE]
    plural = "value" if citywide.values_per_season == 1 else "values"
    print(f"Thresholds from {len(citywide.reference_seasons)} reference seasons "
          f"({', '.join(severity.season_name(y) for y in citywide.reference_seasons)}), "
          f"{citywide.values_per_season} {plural} each, {citywide.n_pooled} pooled, "
          f"fitted on weeks before {citywide.fitted_through}.")
    for name, level in (("IT%g" % (l * 100), l) for l in levels):
        print(f"  citywide {name} = {citywide.values[level]:.1f} per 100,000")
    if citywide.underpowered:
        warnings.append(
            f"Only {citywide.n_pooled} pooled values per indicator "
            f"(fewer than {severity.MIN_USEFUL_POOL}); the log-SD, and so the highest "
            f"threshold, rests on very little data. Raise --values-per-season or add "
            f"reference seasons.")

    frame = severity.thresholds_frame(fitted)
    frame.to_csv(out_dir / "severity_thresholds.csv", index=False)
    (out_dir / "severity_thresholds.json").write_text(json.dumps(
        {name: t.to_json() for name, t in fitted.items()}, indent=2) + "\n")
    print(f"Wrote {paths.display(out_dir / 'severity_thresholds.csv')}")

    # --- score every run ----------------------------------------------------
    score_rows, timing_rows, band_rows = [], [], []
    degenerate = 0
    for model, variant in runs:
        predictions = load_predictions(model, variant, results_root)
        predictions = predictions.loc[predictions["horizon"].eq(horizon)]
        if predictions.empty:
            warnings.append(f"`{model}/{variant}` has no horizon-{horizon} rows; skipped.")
            continue
        if "upper" not in predictions.columns:
            predictions = predictions.assign(upper=np.nan)
            warnings.append(f"`{model}/{variant}` has no interval bounds; its exceedance "
                            f"probabilities and Brier scores are blank.")

        bands = indicator_frame(predictions, fitted, citywide_sigma=args.citywide_sigma)
        degenerate += int((bands["sigma"] <= 0).sum())
        bands = bands.assign(model=model, variant=variant, horizon=horizon)
        band_rows.append(bands)

        score_rows.append(score(bands, fitted, model=model, variant=variant,
                                horizon=horizon, scopes=scopes, segments=segments,
                                levels=levels))
        timing_rows.append(timing(bands, fitted, model=model, variant=variant,
                                  horizon=horizon, levels=levels))

    if not score_rows:
        raise SystemExit(f"error: no run produced horizon-{horizon} predictions.")

    long = pd.concat(score_rows, ignore_index=True)
    timings = pd.concat(timing_rows, ignore_index=True)
    all_bands = pd.concat(band_rows, ignore_index=True)
    for table in (long, timings, all_bands):
        table["series"] = series_labels(table)

    if degenerate:
        warnings.append(f"{degenerate} forecast rows had a zero-width interval, so their "
                        f"exceedance probability is a hard 0 or 1 rather than a "
                        f"distribution.")
    for label in ("IT50", "IT90", "IT98"):
        view = long.loc[long["label"].eq(label) & long["scope"].eq("pooled")]
        if not view.empty and bool(view["underpowered"].all()):
            warnings.append(f"{label} was crossed on only {int(view['n_events'].max())} "
                            f"neighborhood-weeks in this window, so its scores are reported "
                            f"but not ranked.")

    ordered = ["model", "variant", "series", "horizon", "scope", "indicator", "segment",
               "level", "label", "threshold"]
    ordered += [c for c in (*CONTINGENCY_COLUMNS, *BRIER_COLUMNS, *BAND_COLUMNS,
                            "underpowered") if c in long.columns]
    long = long[[c for c in ordered if c in long.columns]]
    long.to_csv(out_dir / "severity_long.csv", index=False)
    timings.to_csv(out_dir / "severity_timing.csv", index=False)

    keep = ["model", "variant", "horizon", "indicator", "target_date", "season", "segment",
            "actual", "predicted", "sigma", "true_band", "pred_band"]
    keep += [c for c in all_bands.columns if c.startswith("p_exceed_")]
    all_bands[keep].sort_values(["model", "variant", "indicator", "target_date"]).to_csv(
        out_dir / "severity_bands.csv", index=False)
    for name in ("severity_long.csv", "severity_timing.csv", "severity_bands.csv"):
        print(f"Wrote {paths.display(out_dir / name)}")

    # --- figures ------------------------------------------------------------
    requested = [m.strip() for m in args.plot_models.split(",") if m.strip()]
    available = list(dict.fromkeys(long["series"]))
    # A requested model expands to one series per variant it was run with.
    plot_models = [s for m in requested for s in available
                   if s == m or s.startswith(f"{m}/")]
    if len(plot_models) > len(SERIES):
        warnings.append(f"--plot-models listed {len(plot_models)} models but only "
                        f"{len(SERIES)} validated colours exist; plotting the first "
                        f"{len(SERIES)}.")
        plot_models = plot_models[:len(SERIES)]
    if not plot_models:
        plot_models = sorted(available)[:len(SERIES)]

    reference_note = (
        f"Thresholds: MEM, levels {'/'.join('IT%g' % (l * 100) for l in levels)}, "
        f"reference seasons {', '.join(severity.season_name(y) for y in citywide.reference_seasons)}, "
        f"fitted on weeks before {citywide.fitted_through}."
    )
    if not args.per_neighborhood_scale:
        # Without this the figure and the CSV disagree: on shared bands
        # Dorchester's peak reads 'very high', but scored against Dorchester's
        # own thresholds the same week is 'moderate'.
        reference_note += ("  Shared citywide bands on every panel; the scores in "
                           "severity_long.csv use each neighborhood's own thresholds.")
    plot_bands(rates, fitted, out_dir / "severity_bands.png",
               test_start=test_start, test_end=test_end, reference_note=reference_note,
               standardise=not args.per_neighborhood_scale)
    headline_scope = "pooled" if "pooled" in scopes else scopes[0]
    plot_skill(long, out_dir / "severity_skill.png", scope=headline_scope,
               segment=segments[0], metric=args.rank_by, models=plot_models)
    reliability_source = {label: all_bands.loc[all_bands["series"].eq(label)]
                          for label in plot_models}
    plot_reliability(reliability_source, plot_models, out_dir / "severity_reliability.png",
                     level=levels[0],
                     scope="pooled" if headline_scope != "citywide" else "citywide")
    plot_timing(timings, out_dir / "severity_timing.png", level=args.timing_level,
                models=plot_models)

    # --- markdown -----------------------------------------------------------
    markdown = leaderboard_markdown(long, timings, fitted, args, warnings)
    (out_dir / "severity_leaderboard.md").write_text(markdown)
    print(f"Wrote {paths.display(out_dir / 'severity_leaderboard.md')}")

    if args.update_readme:
        readme = paths.DOCS_DIR / "METHODS.md"
        text = readme.read_text() if readme.exists() else ""
        if README_BEGIN not in text:
            print(f"warning: {readme} has no {README_BEGIN} / {README_END} markers; skipping",
                  file=sys.stderr)
        else:
            import compare_models
            saved = (compare_models.README_BEGIN, compare_models.README_END)
            compare_models.README_BEGIN, compare_models.README_END = README_BEGIN, README_END
            try:
                update_readme(readme_markdown(long, fitted, args, out_dir), readme)
            finally:
                compare_models.README_BEGIN, compare_models.README_END = saved

    for note in warnings:
        print(f"note: {note}", file=sys.stderr)


if __name__ == "__main__":
    main()
