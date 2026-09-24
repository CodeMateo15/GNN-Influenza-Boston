"""Was the week bad, and did the forecast say so?

The rest of this project scores forecasts on continuous error -- RMSE, MAE,
correlation. Those answer "how close was the number". They do not answer the
question a public-health reader asks, which is whether the model said the coming
week would cross into a severity level worth acting on.

This module supplies the missing half. It follows CDC's in-season severity
assessment: weekly indicator values are compared against intensity thresholds
derived from previous seasons, giving a band.

    below IT50   low          IT50..IT90   moderate
    IT90..IT98   high         at or above IT98   very high

The thresholds come from the Moving Epidemic Method (MEM). The recipe below is
the one in the `mem` R package (lozalojo/mem) under its own defaults --
i.type.intensity=6, i.tails.intensity=1, i.n.max=-1:

  1. A season runs August to July.
  2. Take the `values_per_season` highest weekly values of each reference
     season and pool them. MEM's rule is max(1, round(30 / n_seasons)), which
     holds the pooled sample near 30 however many seasons are available.
  3. Work in logs: mu = mean(log x), sd = sample sd(log x).
  4. The threshold at level p is the one-sided upper limit
     exp(mu + k_p * sd), with k_p = qt(p, m-1) * sqrt(1 + 1/m).

Two details of step 4 are easy to get wrong and are load-bearing:

  * It is `sd`, not `sd / sqrt(m)`. mem's `iconfianza.logx` builds an interval
    for a *future observation*, not for the mean. The `sd / sqrt(m)` variant is
    `iconfianza.geometrica`, reached with i.type.intensity=2, and it gives much
    tighter thresholds.
  * qt(0.50, df) is 0, so **IT50 is exactly the geometric mean** of the pooled
    values. That is a useful sanity check on any implementation.

CDC uses levels 0.50 / 0.90 / 0.98; mem's own default is 0.40 / 0.90 / 0.975.
Both are here -- CDC's is the default because this module is modelled on the
CDC assessment.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm, t as student_t

from .constants import TEST_START
from .intervals import Z95

SEVERITY_BANDS = ("low", "moderate", "high", "very high")

# CDC's in-season severity levels. mem's own defaults are kept for comparison,
# since a reader coming from the MEM literature will expect those.
CDC_LEVELS = (0.50, 0.90, 0.98)
MEM_LEVELS = (0.40, 0.90, 0.975)

# The citywide indicator sits in the same tables as the neighborhoods, so it
# needs a name that cannot collide with one.
CITYWIDE = "CITYWIDE"

# MEM holds the pooled sample near this many values, whatever the season count.
MEM_TARGET_POOL = 30

# Below this the log-sd is estimated from too few values for the 98th-percentile
# threshold to mean anything; callers warn rather than silently proceeding.
MIN_USEFUL_POOL = 10

# Rare events cluster every forecast probability into the lowest bin under
# equal-width binning, so the reliability bins are deliberately uneven.
RELIABILITY_BINS = (0.0, 0.02, 0.05, 0.10, 0.20, 0.40, 0.70, 1.0)

# Named reference-season sets. The season is labelled by its starting year, so
# 2022 is the 2022-23 season.
REFERENCE_SEASON_SETS: dict[str, tuple[int, ...] | None] = {
    # The three complete seasons since the COVID disruption.
    "post_covid": (2022, 2023, 2024),
    # Adds two pre-pandemic anchors. 2019-20 is dropped because COVID truncated
    # its tail, 2020-21 because NPIs suppressed it to a citywide peak of 12.6
    # against a normal ~100, and 2021-22 because it was still recovering.
    "exclude_covid": (2017, 2018, 2022, 2023, 2024),
    # Every season available before the threshold cutoff.
    "all": None,
}

_EPS = 1e-9


def season_label(dates, season_start_month: int | None = None) -> np.ndarray:
    """Season start year for each date. August starts a new season by default.

    `season_start_month` is the month the series sits at its annual floor, so
    that no observed week is split across two seasons. August for the two US
    cities; February for Buenos Aires, whose floor is December-February and
    whose season runs April-September.

    MEM defines the season as ISO week 30 to week 29, which falls in late July.
    Rounding that to the August boundary keeps the label computable from the
    month alone and moves no observed week between seasons: Boston's ILI series
    is at its annual floor throughout July and August.
    """
    stamps = pd.DatetimeIndex(pd.to_datetime(dates))
    boundary = 8 if season_start_month is None else int(season_start_month)
    return np.where(stamps.month >= boundary, stamps.year, stamps.year - 1)


def season_name(year: int) -> str:
    """2022 -> '2022-23', for table headings."""
    return f"{year}-{str(year + 1)[2:]}"


def citywide_series(rates: pd.DataFrame) -> pd.Series:
    """Unweighted mean rate across neighborhoods, skipping suppressed cells.

    Unweighted so that Fenway counts as much as Dorchester, matching the `macro`
    scope in metrics.py. A population-weighted mean would be a different
    indicator and would need a population denominator this project does not
    carry per week.
    """
    return rates.mean(axis=1, skipna=True)


@dataclass(frozen=True)
class Thresholds:
    """Fitted intensity thresholds for one indicator, with their provenance.

    The provenance fields are not decoration. A threshold is only interpretable
    alongside which seasons produced it and where the data was cut off, and
    `fitted_through` is what lets a reader confirm no test week leaked in.
    """

    indicator: str
    levels: tuple[float, ...]
    values: dict[float, float]
    reference_seasons: tuple[int, ...]
    values_per_season: int
    n_pooled: int
    geometric_mean: float
    log_sd: float
    use_t: bool
    fitted_through: str

    @property
    def underpowered(self) -> bool:
        return self.n_pooled < MIN_USEFUL_POOL

    def value(self, level: float) -> float:
        return self.values[level]

    def band(self, x) -> np.ndarray:
        """Band code per value: 0 low, 1 moderate, 2 high, 3 very high.

        A missing value gets -1, not 0. A suppressed week is not a quiet week,
        and banding it 'low' would invent an observation.
        """
        values = np.asarray(x, dtype=float)
        edges = [self.values[level] for level in self.levels]
        codes = np.zeros(values.shape, dtype=int)
        for rank, edge in enumerate(edges, start=1):
            codes = np.where(values >= edge, rank, codes)
        return np.where(np.isfinite(values), codes, -1)

    def label(self, x) -> np.ndarray:
        return band_labels(self.band(x))

    def to_json(self) -> dict:
        return {
            "method": "MEM intensity thresholds, one-sided log-normal upper limits",
            "indicator": self.indicator,
            "levels": list(self.levels),
            "thresholds": {f"{level:g}": self.values[level] for level in self.levels},
            "reference_seasons": [season_name(y) for y in self.reference_seasons],
            "values_per_season": self.values_per_season,
            "n_pooled": self.n_pooled,
            "geometric_mean": self.geometric_mean,
            "log_sd": self.log_sd,
            "use_t": self.use_t,
            "fitted_through": self.fitted_through,
            "underpowered": self.underpowered,
        }


def band_labels(codes) -> np.ndarray:
    """Band codes to names; -1 becomes an empty string."""
    codes = np.asarray(codes, dtype=int)
    lookup = np.array(("",) + SEVERITY_BANDS, dtype=object)
    return lookup[np.clip(codes + 1, 0, len(SEVERITY_BANDS))]


def pool_size(n_seasons: int) -> int:
    """MEM's values-per-season rule: max(1, round(30 / n_seasons))."""
    if n_seasons <= 0:
        raise ValueError("Need at least one reference season to size the pool.")
    return max(1, int(round(MEM_TARGET_POOL / n_seasons)))


def mem_intensity_thresholds(
    values_by_season: list[np.ndarray],
    *,
    levels: tuple[float, ...] = CDC_LEVELS,
    values_per_season: int | None = None,
    use_t: bool = True,
) -> tuple[dict[float, float], dict[str, float]]:
    """MEM thresholds from the highest values of each reference season.

    Returns the thresholds keyed by level, plus the fit summary
    (values_per_season, n_pooled, geometric_mean, log_sd) that the caller
    records as provenance.
    """
    seasons = [np.asarray(v, dtype=float) for v in values_by_season]
    seasons = [v[np.isfinite(v)] for v in seasons]
    seasons = [v for v in seasons if v.size]
    if not seasons:
        raise ValueError("No finite values in any reference season.")

    per_season = pool_size(len(seasons)) if values_per_season is None else int(values_per_season)
    pooled = np.concatenate([np.sort(v)[::-1][:per_season] for v in seasons])

    # mem shifts by 1 rather than dropping zeros, so a suppressed-to-zero week
    # still contributes. Matching that keeps the thresholds comparable to any
    # published MEM figure.
    shift = 1.0 if np.any(pooled <= 0) else 0.0
    logs = np.log(pooled + shift)
    m = logs.size
    mu = float(logs.mean())
    sd = float(logs.std(ddof=1)) if m > 1 else 0.0

    thresholds: dict[float, float] = {}
    for level in levels:
        if use_t and m > 1:
            k = float(student_t.ppf(level, m - 1)) * np.sqrt(1.0 + 1.0 / m)
        else:
            k = float(norm.ppf(level))
        thresholds[level] = float(np.exp(mu + k * sd) - shift)

    summary = {
        "values_per_season": per_season,
        "n_pooled": m,
        "geometric_mean": float(np.exp(mu) - shift),
        "log_sd": sd,
    }
    return thresholds, summary


def fit_thresholds(
    rates: pd.DataFrame,
    *,
    reference_seasons: tuple[int, ...] | None = None,
    threshold_end: pd.Timestamp = TEST_START,
    levels: tuple[float, ...] = CDC_LEVELS,
    values_per_season: int | None = None,
    use_t: bool = True,
    include_citywide: bool = True,
) -> dict[str, Thresholds]:
    """One set of thresholds per neighborhood, plus the citywide indicator.

    Per-neighborhood rather than one shared threshold because the scale differs
    by nearly sevenfold across the city -- season peaks run from about 48 per
    100,000 in Fenway to 320 in Dorchester. A single citywide cut point would
    label Dorchester severe every winter and Fenway never.

    `threshold_end` is exclusive and defaults to TEST_START. Without it the
    2024-25 season reaches into June and July 2025, which are inside the
    evaluation window: the thresholds a forecast is judged against would have
    been fitted partly on the period being judged.
    """
    threshold_end = pd.Timestamp(threshold_end)
    history = rates.loc[rates.index < threshold_end]
    if history.empty:
        raise ValueError(
            f"No weeks before threshold_end={threshold_end.date()}; "
            f"data spans {rates.index.min().date()}..{rates.index.max().date()}."
        )

    seasons = pd.Series(season_label(history.index), index=history.index)
    available = tuple(sorted(seasons.unique()))
    wanted = available if reference_seasons is None else tuple(sorted(reference_seasons))
    missing = [y for y in wanted if y not in available]
    if missing:
        raise ValueError(
            f"Reference seasons {[season_name(y) for y in missing]} are not in the data "
            f"before {threshold_end.date()}. Available: {[season_name(y) for y in available]}."
        )

    indicators: dict[str, pd.Series] = {column: history[column] for column in history.columns}
    if include_citywide:
        indicators[CITYWIDE] = citywide_series(history)

    fitted: dict[str, Thresholds] = {}
    for name, series in indicators.items():
        by_season, used = [], []
        for year in wanted:
            values = series.loc[seasons == year].dropna().to_numpy(dtype=float)
            if values.size:
                by_season.append(values)
                used.append(year)
        if not by_season:
            # An indicator with no data in any reference season cannot be
            # thresholded; omitting it is honest, inventing one is not.
            continue
        thresholds, summary = mem_intensity_thresholds(
            by_season, levels=levels, values_per_season=values_per_season, use_t=use_t,
        )
        fitted[name] = Thresholds(
            indicator=name,
            levels=tuple(levels),
            values=thresholds,
            reference_seasons=tuple(used),
            use_t=use_t,
            fitted_through=str(threshold_end.date()),
            **summary,
        )
    return fitted


def thresholds_frame(fitted: dict[str, Thresholds]) -> pd.DataFrame:
    """Long-form threshold table, one row per (indicator, level)."""
    rows = []
    for name, thresholds in fitted.items():
        for rank, level in enumerate(thresholds.levels, start=1):
            rows.append({
                "indicator": name,
                "level": level,
                "label": f"IT{level * 100:g}",
                "threshold": thresholds.values[level],
                "band_at_or_above": SEVERITY_BANDS[min(rank, len(SEVERITY_BANDS) - 1)],
                "reference_seasons": " ".join(season_name(y) for y in thresholds.reference_seasons),
                "values_per_season": thresholds.values_per_season,
                "n_pooled": thresholds.n_pooled,
                "geometric_mean": thresholds.geometric_mean,
                "log_sd": thresholds.log_sd,
                "use_t": thresholds.use_t,
                "fitted_through": thresholds.fitted_through,
                "underpowered": thresholds.underpowered,
            })
    return pd.DataFrame(rows)


# --- Turning a forecast into a severity statement ---------------------------

def predictive_sigma(predicted, upper, *, z: float = Z95) -> np.ndarray:
    """Predictive standard deviation implied by the calibrated 95% band.

    `intervals.py` writes a band of half-width kappa * Z95 * sqrt(variance), so
    dividing the upper half-width by Z95 recovers the scale it was built from.

    The **upper** bound only. The lower bound is clipped at zero
    (intervals.py:83) because a rate cannot be negative, so at low predicted
    levels it is nearer the prediction than the upper bound is; using it, or
    averaging the two, would understate the spread exactly where most weeks sit.
    """
    predicted = np.asarray(predicted, dtype=float)
    upper = np.asarray(upper, dtype=float)
    return np.maximum(upper - predicted, 0.0) / z


def exceedance_probability(predicted, upper, threshold: float, *, z: float = Z95) -> np.ndarray:
    """P(rate >= threshold), from the calibrated interval around each forecast.

    The band is symmetric and calibrated to 95% on validation, so reading it as
    a Gaussian predictive distribution adds no assumption that the band itself
    did not already make. Where the band has collapsed to zero width there is no
    distribution to integrate and the forecast is its own point mass, which is a
    hard 0 or 1.
    """
    predicted = np.asarray(predicted, dtype=float)
    sigma = predictive_sigma(predicted, upper, z=z)
    degenerate = sigma <= _EPS
    safe = np.where(degenerate, 1.0, sigma)
    probability = 1.0 - norm.cdf((threshold - predicted) / safe)
    return np.where(degenerate, (predicted >= threshold).astype(float), probability)


# --- Layer 1: did it call the crossing? -------------------------------------

CONTINGENCY_METRICS = ("POD", "FAR", "precision", "CSI", "F1", "PSS", "HSS", "MCC",
                       "accuracy", "frequency_bias")


def _ratio(numerator: float, denominator: float) -> float:
    """NaN, not zero, when the denominator is empty.

    Zero would read as 'no skill'. The truth in that case is 'not measurable' --
    at an 8% base rate several of these denominators genuinely do empty out, and
    conflating the two would let an unmeasurable model outrank a measured one.
    """
    return float(numerator / denominator) if denominator > 0 else float("nan")


def contingency(observed_exceed, forecast_exceed) -> dict[str, float]:
    """2x2 table and its skill scores for one threshold.

    Inputs are boolean, already filtered to weeks with an observed value.
    """
    observed = np.asarray(observed_exceed, dtype=bool)
    forecast = np.asarray(forecast_exceed, dtype=bool)
    if observed.shape != forecast.shape:
        raise ValueError(f"Shape mismatch: {observed.shape} observed vs {forecast.shape} forecast.")

    hits = float(np.sum(observed & forecast))
    false_alarms = float(np.sum(~observed & forecast))
    misses = float(np.sum(observed & ~forecast))
    correct_neg = float(np.sum(~observed & ~forecast))
    n = hits + false_alarms + misses + correct_neg

    pod = _ratio(hits, hits + misses)
    fpr = _ratio(false_alarms, false_alarms + correct_neg)
    numerator = hits * correct_neg - false_alarms * misses
    hss_denominator = ((hits + misses) * (misses + correct_neg)
                       + (hits + false_alarms) * (false_alarms + correct_neg))
    mcc_denominator = np.sqrt((hits + false_alarms) * (hits + misses)
                              * (correct_neg + false_alarms) * (correct_neg + misses))

    return {
        "n_obs": int(n),
        "n_events": int(hits + misses),
        "base_rate": _ratio(hits + misses, n),
        "hits": int(hits),
        "false_alarms": int(false_alarms),
        "misses": int(misses),
        "correct_neg": int(correct_neg),
        "POD": pod,
        "FAR": _ratio(false_alarms, hits + false_alarms),
        "precision": _ratio(hits, hits + false_alarms),
        "FPR": fpr,
        "CSI": _ratio(hits, hits + false_alarms + misses),
        "F1": _ratio(2 * hits, 2 * hits + false_alarms + misses),
        # Peirce skill score. Zero for both degenerate forecasts -- never alert
        # and always alert -- which is why it leads the tables here.
        "PSS": pod - fpr,
        "HSS": _ratio(2 * numerator, hss_denominator),
        "MCC": _ratio(numerator, float(mcc_denominator)),
        "accuracy": _ratio(hits + correct_neg, n),
        # Above 1 the model raises more alerts than there were events.
        "frequency_bias": _ratio(hits + false_alarms, hits + misses),
    }


# --- Layer 2: did it get the right band? ------------------------------------

BAND_METRICS = ("exact_band", "within_one_band", "kappa_quadratic", "mean_band_error")


def band_agreement(true_codes, pred_codes, *, n_bands: int = len(SEVERITY_BANDS)) -> dict[str, float]:
    """Agreement over all four bands, not just one crossing.

    `mean_band_error` is signed on purpose: a model that habitually calls one
    band too high and one that calls one band too low both score the same
    exact-match rate, and they are not the same failure.
    """
    true_codes = np.asarray(true_codes, dtype=int)
    pred_codes = np.asarray(pred_codes, dtype=int)
    keep = (true_codes >= 0) & (pred_codes >= 0)
    true_codes, pred_codes = true_codes[keep], pred_codes[keep]
    if true_codes.size == 0:
        return {"n_obs": 0, **{key: float("nan") for key in BAND_METRICS}}

    observed = np.zeros((n_bands, n_bands), dtype=float)
    np.add.at(observed, (true_codes, pred_codes), 1.0)
    observed /= observed.sum()
    expected = np.outer(observed.sum(axis=1), observed.sum(axis=0))

    grid = np.arange(n_bands)
    weights = (grid[:, None] - grid[None, :]) ** 2 / (n_bands - 1) ** 2
    disagreement = float((weights * observed).sum())
    chance = float((weights * expected).sum())

    return {
        "n_obs": int(true_codes.size),
        "exact_band": float(np.mean(true_codes == pred_codes)),
        "within_one_band": float(np.mean(np.abs(true_codes - pred_codes) <= 1)),
        # Undefined when chance disagreement is zero, which happens whenever a
        # single band accounts for every week -- common in a quiet season.
        "kappa_quadratic": 1.0 - disagreement / chance if chance > 0 else float("nan"),
        "mean_band_error": float(np.mean(pred_codes - true_codes)),
    }


# --- Layer 3: was its confidence honest? ------------------------------------

def brier_scores(observed_exceed, probability, *, base_rate: float | None = None) -> dict[str, float]:
    """Brier score, and its skill against always forecasting the base rate.

    Climatology is the reference because a constant 8% forecast is what a model
    has to beat to be worth anything: it is already well calibrated and already
    scores a low Brier at a low base rate.
    """
    observed = np.asarray(observed_exceed, dtype=float)
    probability = np.asarray(probability, dtype=float)
    keep = np.isfinite(observed) & np.isfinite(probability)
    observed, probability = observed[keep], probability[keep]
    if observed.size == 0:
        return {"brier": float("nan"), "brier_ref": float("nan"), "BSS": float("nan")}

    reference = float(observed.mean()) if base_rate is None else float(base_rate)
    brier = float(np.mean((probability - observed) ** 2))
    brier_ref = float(np.mean((reference - observed) ** 2))
    return {
        "brier": brier,
        "brier_ref": brier_ref,
        # Zero when the season had no events, since then climatology is perfect.
        "BSS": 1.0 - brier / brier_ref if brier_ref > 0 else float("nan"),
    }


def reliability_curve(observed_exceed, probability, *,
                      bins: tuple[float, ...] = RELIABILITY_BINS) -> pd.DataFrame:
    """Forecast probability against observed frequency, per probability bin."""
    observed = np.asarray(observed_exceed, dtype=float)
    probability = np.asarray(probability, dtype=float)
    keep = np.isfinite(observed) & np.isfinite(probability)
    observed, probability = observed[keep], probability[keep]

    edges = np.asarray(bins, dtype=float)
    index = np.clip(np.digitize(probability, edges[1:-1], right=False), 0, len(edges) - 2)
    rows = []
    for slot in range(len(edges) - 1):
        mask = index == slot
        rows.append({
            "bin_lower": edges[slot],
            "bin_upper": edges[slot + 1],
            "n_obs": int(mask.sum()),
            "mean_forecast": float(probability[mask].mean()) if mask.any() else float("nan"),
            "observed_frequency": float(observed[mask].mean()) if mask.any() else float("nan"),
        })
    return pd.DataFrame(rows)


# --- Layer 4: did it call it at the right time? -----------------------------

TIMING_METRICS = ("onset_error_weeks", "lead_time_weeks", "peak_week_error_weeks", "peak_error")


def _first_crossing(dates: pd.DatetimeIndex, values: np.ndarray, threshold: float):
    above = np.nonzero(np.asarray(values, dtype=float) >= threshold)[0]
    return dates[above[0]] if above.size else pd.NaT


def _weeks_between(later, earlier) -> float:
    if pd.isna(later) or pd.isna(earlier):
        return float("nan")
    return float((pd.Timestamp(later) - pd.Timestamp(earlier)).days / 7.0)


def timing_row(dates, actual, predicted, threshold: float) -> dict:
    """Onset, peak and lead time for one indicator over one season.

    Restricted to weeks with an observed value, so the forecast onset and the
    actual onset are searched over the same weeks. Letting the forecast alert on
    a suppressed week it could never be checked against would flatter its lead
    time.
    """
    frame = pd.DataFrame({
        "target_date": pd.to_datetime(dates),
        "actual": np.asarray(actual, dtype=float),
        "predicted": np.asarray(predicted, dtype=float),
    }).dropna(subset=["actual", "predicted"]).sort_values("target_date")

    if frame.empty:
        return {key: float("nan") for key in TIMING_METRICS} | {
            "n_weeks": 0, "onset_actual": pd.NaT, "onset_pred": pd.NaT,
            "peak_week_actual": pd.NaT, "peak_week_pred": pd.NaT,
            "peak_actual": float("nan"), "peak_pred": float("nan"),
            "first_alert_week": pd.NaT,
        }

    dates = pd.DatetimeIndex(frame["target_date"])
    observed, forecast = frame["actual"].to_numpy(), frame["predicted"].to_numpy()
    onset_actual = _first_crossing(dates, observed, threshold)
    onset_pred = _first_crossing(dates, forecast, threshold)

    return {
        "n_weeks": int(len(frame)),
        "onset_actual": onset_actual,
        "onset_pred": onset_pred,
        # Positive means the forecast crossed later than the observation did.
        "onset_error_weeks": _weeks_between(onset_pred, onset_actual),
        # The same quantity with the operational sign: positive is warning ahead
        # of the crossing, which is the number a reader wants.
        "lead_time_weeks": _weeks_between(onset_actual, onset_pred),
        "first_alert_week": onset_pred,
        "peak_week_actual": dates[int(np.argmax(observed))],
        "peak_week_pred": dates[int(np.argmax(forecast))],
        "peak_week_error_weeks": _weeks_between(dates[int(np.argmax(forecast))],
                                                dates[int(np.argmax(observed))]),
        "peak_actual": float(observed.max()),
        "peak_pred": float(forecast.max()),
        "peak_error": float(forecast.max() - observed.max()),
    }


# --- shared chart geometry --------------------------------------------------
#
# Panel limits live here, not in the plotting scripts, so that every figure that
# shows a rate uses the same ceiling for a given neighborhood. The point is that
# the ceiling is computed from the *observation* and the thresholds, never from
# the series being drawn: a y-axis fitted to the predictions rescales whenever
# the model changes, and two models' panels then cannot be compared by eye even
# though they show the same weeks.

PANEL_HEADROOM = 1.12


def panel_ceiling(observed, thresholds: "Thresholds | None" = None, *,
                  headroom: float = PANEL_HEADROOM) -> float:
    """Y-axis ceiling for one indicator, independent of any model's forecasts.

    Tall enough for the observed peak and for the top intensity threshold, so the
    'very high' band is always visible even in a neighborhood that never reached
    it. Forecasts above this are clipped, and the caller is expected to say so.
    """
    values = np.asarray(observed, dtype=float)
    values = values[np.isfinite(values)]
    top = float(values.max()) if values.size else 0.0
    if thresholds is not None:
        top = max(top, thresholds.values[thresholds.levels[-1]])
    return float(top * headroom) if top > 0 else 1.0


def panel_ceilings(rates: pd.DataFrame, fitted: dict[str, "Thresholds"] | None = None, *,
                   window: tuple[pd.Timestamp, pd.Timestamp] | None = None,
                   headroom: float = PANEL_HEADROOM,
                   shared: bool = False) -> dict[str, float]:
    """`panel_ceiling` for every neighborhood plus the citywide indicator.

    With `shared=True` every indicator gets the same ceiling, which makes
    magnitudes comparable across panels at the cost of flattening the smaller
    neighborhoods -- Fenway peaks near 21 per 100,000 against Dorchester's 256.
    """
    frame = rates
    if window is not None:
        start, end = window
        clipped = rates.loc[(rates.index >= start) & (rates.index <= end)]
        frame = clipped if not clipped.empty else rates

    series = {column: frame[column] for column in frame.columns}
    series[CITYWIDE] = citywide_series(frame)
    fitted = fitted or {}
    ceilings = {name: panel_ceiling(values, fitted.get(name), headroom=headroom)
                for name, values in series.items()}
    if shared:
        # The citywide mean is an average and so always lower than the busiest
        # neighborhood; it must not drag a shared ceiling down.
        highest = max(v for k, v in ceilings.items() if k != CITYWIDE) if len(ceilings) > 1 else \
            max(ceilings.values())
        ceilings = {name: highest for name in ceilings}
    return ceilings


def band_spans(thresholds: "Thresholds", ceiling: float) -> list[tuple[float, float, int]]:
    """(low, high, band_code) rectangles for shading a panel's severity bands."""
    edges = [0.0] + [thresholds.values[level] for level in thresholds.levels]
    top = max(ceiling, edges[-1])
    spans = []
    for index in range(len(edges)):
        high = edges[index + 1] if index + 1 < len(edges) else top
        spans.append((edges[index], min(high, top), index))
    return spans


def shared_ceiling(rates: pd.DataFrame, thresholds: "Thresholds | None" = None, *,
                   window: tuple[pd.Timestamp, pd.Timestamp] | None = None,
                   headroom: float = PANEL_HEADROOM, round_to: int = 50) -> float:
    """One y ceiling for every panel, rounded up to a readable number.

    Covers the busiest neighborhood and the top threshold, so no panel clips and
    every panel is directly comparable. Rounded so the axis reads 300 rather
    than 287.
    """
    frame = rates
    if window is not None:
        start, end = window
        clipped = rates.loc[(rates.index >= start) & (rates.index <= end)]
        frame = clipped if not clipped.empty else rates

    top = float(np.nanmax(frame.to_numpy(dtype=float))) if frame.size else 0.0
    if thresholds is not None:
        top = max(top, thresholds.values[thresholds.levels[-1]])
    top *= headroom
    if round_to > 0:
        top = float(np.ceil(top / round_to) * round_to)
    return top or float(round_to)


def band_entry_labels(thresholds: "Thresholds") -> list[tuple[float, str]]:
    """(threshold value, band it opens) for legend entries.

    The lines are boundaries, so each one is named for the band it lets you
    into: crossing the first puts a week in 'moderate'. 'low' is the region
    below the first line and gets no line of its own.
    """
    return [(thresholds.values[level], SEVERITY_BANDS[index + 1])
            for index, level in enumerate(thresholds.levels)]
