"""Probabilistic scores and paired tests between two models' forecasts.

metrics.py answers "how far off was the point forecast". This module answers
the two questions a reviewer asks next:

  1. How good was the whole forecast -- the band as well as the point?
     Answered with the weighted interval score (WIS), the scoring rule the CDC
     FluSight hub ranks teams on (Bracher et al. 2021, PLoS Comput Biol
     17:e1008618). Lower is better, it is in the target's own units (rate per
     100,000), and with enough quantile levels it approximates CRPS.

  2. Is model A's lead over model B bigger than chance?
     Answered two ways, both over TARGET WEEKS rather than over cells:
       * a Diebold-Mariano test on the weekly loss difference, with a HAC
         variance and the Harvey-Leybourne-Newbold small-sample correction;
       * a moving-block bootstrap confidence interval on the metric difference.

Why weeks and not cells. A test season is ~49 weeks x 14 neighborhoods = ~690
cells, but they are nowhere near 690 independent observations: Boston's
neighborhoods co-move almost completely (the 0.938 ceiling in METHODS.md), and
consecutive weeks are autocorrelated. Treating cells as independent -- or the
14 neighborhoods as 14 paired observations, which is what the ablation Wilcoxon
does -- makes every difference look significant. So the unit resampled and
tested here is the target week, with all neighborhoods kept together inside it,
and the bootstrap draws weeks in contiguous blocks so the autocorrelation
survives the resampling.

What this module does NOT do is make 49 weeks into more than one season. A
significant difference on one season is a statement about that season; the
backtest folds (run_backtest.py) are what generalise it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

from .intervals import QUANTILE_COLUMNS, QUANTILE_LEVELS

# The level of the 95% band every model in this project writes.
ALPHA_95 = 0.05

# FluSight's 23 quantile levels live in intervals.py beside the code that
# writes them to predictions.csv as q0.010 ... q0.990.
FLUSIGHT_QUANTILES = QUANTILE_LEVELS

_KEYS = ["target_date", "neighborhood", "horizon"]


# --- scores ---------------------------------------------------------------

def interval_score(actual, lower, upper, alpha: float) -> np.ndarray:
    """Interval score of a central (1 - alpha) band, per observation.

    Width, plus a penalty of 2/alpha per unit the truth fell outside the band.
    A band that is too narrow pays through the penalty, one that is too wide
    through its width, so the score is minimised by the honest band.
    """
    actual = np.asarray(actual, float)
    lower = np.asarray(lower, float)
    upper = np.asarray(upper, float)
    below = np.clip(lower - actual, 0.0, None)
    above = np.clip(actual - upper, 0.0, None)
    return (upper - lower) + (2.0 / alpha) * (below + above)


def wis_from_interval(actual, median, lower, upper, alpha: float = ALPHA_95) -> np.ndarray:
    """WIS from a point forecast and one central band (K = 1).

    This is the score every committed predictions.csv supports today, since
    each carries a point forecast and one 95% band. It is a proper score, but
    with one band it leans heavily on the tails, so it is reported as "WIS-95"
    and must not be compared against a 23-quantile WIS from another source.

        WIS = (0.5 * |y - m| + (alpha / 2) * IS_alpha) / (K + 0.5)
    """
    actual = np.asarray(actual, float)
    median = np.asarray(median, float)
    return (0.5 * np.abs(actual - median)
            + (alpha / 2.0) * interval_score(actual, lower, upper, alpha)) / 1.5


def wis_from_quantiles(actual, quantiles: pd.DataFrame | np.ndarray,
                       levels=FLUSIGHT_QUANTILES) -> np.ndarray:
    """WIS from a full set of predictive quantiles.

    `quantiles` is (n, len(levels)), columns in the order of `levels`, which
    must be symmetric about 0.5 and include it. Computed as the mean pinball
    loss times 2, which is algebraically the same as the interval form and
    does not need the levels paired up by hand.
    """
    actual = np.asarray(actual, float)[:, None]
    values = np.asarray(quantiles, float)
    tau = np.asarray(levels, float)[None, :]
    if values.shape[1] != tau.shape[1]:
        raise ValueError(f"{values.shape[1]} quantile columns for {tau.shape[1]} levels")
    if not np.any(np.isclose(tau, 0.5)):
        raise ValueError("WIS needs the median (level 0.5) among the quantile levels")
    diff = actual - values
    pinball = np.maximum(tau * diff, (tau - 1.0) * diff)
    # 2 * mean pinball equals WIS with weights alpha_k / 2 on each interval and
    # 1/2 on the median, normalised by (K + 1/2).
    return 2.0 * pinball.mean(axis=1)


def pit_values(actual, quantiles: np.ndarray, levels=FLUSIGHT_QUANTILES) -> np.ndarray:
    """Probability integral transform, interpolated between quantile levels.

    A calibrated forecast gives PIT values uniform on [0, 1]. A U-shaped
    histogram means the bands are too narrow, a hump means too wide, and a
    slope means the forecast is biased.
    """
    actual = np.asarray(actual, float)
    values = np.asarray(quantiles, float)
    tau = np.asarray(levels, float)
    out = np.empty(actual.size)
    for i, (y, row) in enumerate(zip(actual, values)):
        out[i] = np.interp(y, np.maximum.accumulate(row), tau, left=0.0, right=1.0)
    return out


# --- pairing ----------------------------------------------------------------

def align(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    """Inner-join two predictions frames on the cells both scored.

    Columns come back suffixed _a / _b; `actual` is taken once and checked to
    agree, because two models scored against different truths are not a pair.
    Suppressed weeks (actual NaN) are dropped, exactly as metrics.py drops them.
    """
    keep = [c for c in ("predicted", "lower", "upper", *QUANTILE_COLUMNS)
            if c in a.columns and c in b.columns]
    left = a[_KEYS + ["actual"] + keep].copy()
    right = b[_KEYS + ["actual"] + keep].copy()
    for frame in (left, right):
        frame["target_date"] = pd.to_datetime(frame["target_date"])
    joined = left.merge(right, on=_KEYS, suffixes=("_a", "_b"))
    # Relative tolerance: models that round-trip the target through float32
    # normalisation (the GAT, the GNN) store it to ~1e-5 relative, which is not
    # a different observation.
    same = np.isclose(joined["actual_a"], joined["actual_b"], equal_nan=True,
                      rtol=1e-4, atol=1e-4)
    if not same.all():
        raise ValueError(f"{int((~same).sum())} cells disagree on the observed value; "
                         "the two runs were scored against different data")
    joined = joined.rename(columns={"actual_a": "actual"}).drop(columns="actual_b")
    finite = np.isfinite(joined["actual"]) & np.isfinite(joined["predicted_a"]) \
        & np.isfinite(joined["predicted_b"])
    return joined.loc[finite].reset_index(drop=True)


def cell_losses(pair: pd.DataFrame, side: str) -> pd.DataFrame:
    """Per-cell squared error, absolute error and WIS-95 for one side of a pair."""
    actual = pair["actual"].to_numpy(float)
    predicted = pair[f"predicted_{side}"].to_numpy(float)
    out = pd.DataFrame({"sq": (predicted - actual) ** 2, "abs": np.abs(predicted - actual)})
    if f"lower_{side}" in pair and f"upper_{side}" in pair:
        out["wis"] = wis_from_interval(actual, predicted, pair[f"lower_{side}"],
                                       pair[f"upper_{side}"])
    if has_quantiles(pair):
        out["wisq"] = wis_from_quantiles(actual, _quantile_matrix(pair, side))
    return out


def has_quantiles(pair: pd.DataFrame) -> bool:
    """True when both sides of an aligned pair carry the full 23 quantiles."""
    return all(f"{c}_{side}" in pair for c in QUANTILE_COLUMNS for side in ("a", "b"))


def _quantile_matrix(pair: pd.DataFrame, side: str) -> np.ndarray:
    return pair[[f"{c}_{side}" for c in QUANTILE_COLUMNS]].to_numpy(float)


# --- Diebold-Mariano ------------------------------------------------------

@dataclass
class DMResult:
    statistic: float
    p_value: float
    mean_difference: float
    n_weeks: int
    lag: int


def diebold_mariano(loss_a, loss_b, horizon: int) -> DMResult:
    """Two-sided DM test that two forecasts have equal expected loss.

    `loss_a` and `loss_b` are one number per target week (the loss averaged
    over neighborhoods that week). The difference d = a - b is negative when A
    is better. Its long-run variance uses a Newey-West (Bartlett) kernel over
    h - 1 lags, because an h-step forecast's errors overlap for h - 1 weeks by
    construction; the HLN correction then rescales for small samples and the
    statistic is referred to Student t with n - 1 df, which at n ~ 49 matters.
    """
    d = np.asarray(loss_a, float) - np.asarray(loss_b, float)
    d = d[np.isfinite(d)]
    n = d.size
    lag = max(int(horizon) - 1, 0)
    if n < 5:
        return DMResult(np.nan, np.nan, float(d.mean()) if n else np.nan, n, lag)
    centred = d - d.mean()
    variance = centred @ centred / n
    for k in range(1, lag + 1):
        weight = 1.0 - k / (lag + 1.0)
        variance += 2.0 * weight * (centred[k:] @ centred[:-k]) / n
    if variance <= 0:
        # Identical forecasts, or a kernel that went negative on a tiny sample.
        return DMResult(0.0 if np.allclose(d, 0) else np.nan, 1.0 if np.allclose(d, 0) else np.nan,
                        float(d.mean()), n, lag)
    statistic = d.mean() / np.sqrt(variance / n)
    h = lag + 1
    correction = np.sqrt((n + 1 - 2 * h + h * (h - 1) / n) / n)
    statistic *= correction
    p_value = 2.0 * stats.t.sf(abs(statistic), df=n - 1)
    return DMResult(float(statistic), float(p_value), float(d.mean()), n, lag)


# --- block bootstrap --------------------------------------------------------

def default_block_length(n_weeks: int) -> int:
    """n^(1/3), the usual rate for a moving-block bootstrap of a mean; 4 at 49 weeks."""
    return max(2, int(round(n_weeks ** (1.0 / 3.0))))


def _block_indices(n: int, block: int, rng: np.random.Generator) -> np.ndarray:
    starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
    return (starts[:, None] + np.arange(block)[None, :]).ravel()[:n]


def pooled_rmse(pair: pd.DataFrame, side: str) -> float:
    err = pair[f"predicted_{side}"].to_numpy(float) - pair["actual"].to_numpy(float)
    return float(np.sqrt(np.mean(err ** 2)))


def pooled_mae(pair: pd.DataFrame, side: str) -> float:
    err = pair[f"predicted_{side}"].to_numpy(float) - pair["actual"].to_numpy(float)
    return float(np.mean(np.abs(err)))


def pooled_wis(pair: pd.DataFrame, side: str) -> float:
    return float(np.mean(wis_from_interval(pair["actual"], pair[f"predicted_{side}"],
                                           pair[f"lower_{side}"], pair[f"upper_{side}"])))


def macro_corr(pair: pd.DataFrame, side: str) -> float:
    """Mean over neighborhoods of the Pearson r across weeks, as metrics.py's macro scope."""
    values = []
    for _, part in pair.groupby("neighborhood", sort=False):
        a = part["actual"].to_numpy(float)
        p = part[f"predicted_{side}"].to_numpy(float)
        if a.size > 2 and a.std() > 0 and p.std() > 0:
            values.append(float(np.corrcoef(a, p)[0, 1]))
    return float(np.mean(values)) if values else np.nan


def pooled_wis_quantiles(pair: pd.DataFrame, side: str) -> float:
    """Mean 23-quantile WIS -- the FluSight score proper."""
    return float(np.mean(wis_from_quantiles(pair["actual"], _quantile_matrix(pair, side))))


METRIC_FUNCTIONS = {"RMSE": pooled_rmse, "MAE": pooled_mae, "WIS95": pooled_wis,
                    "WIS": pooled_wis_quantiles, "Corr": macro_corr}


@dataclass
class BootstrapResult:
    estimate: float
    low: float
    high: float
    n_weeks: int
    block: int


def block_bootstrap_difference(pair: pd.DataFrame, metric: str, *, n_boot: int = 2000,
                               block: int | None = None, seed: int = 0,
                               level: float = 0.95) -> BootstrapResult:
    """Percentile CI for metric(A) - metric(B), resampling whole target weeks in blocks.

    Each draw picks contiguous runs of weeks with replacement, keeps every
    neighborhood inside each chosen week, recomputes the metric for both
    models on the same draw, and records the difference. Because both sides
    see the same weeks, what the interval measures is how much the gap between
    the models depends on which weeks the season happened to contain.

    The same week can appear twice in one draw; for macro Corr that simply
    weights it twice, which is the point.
    """
    function = METRIC_FUNCTIONS[metric]
    # Integer week codes in time order, so blocks are runs of consecutive weeks.
    codes, weeks = pd.factorize(pair["target_date"], sort=True)
    n = len(weeks)
    block = block or default_block_length(n)
    estimate = function(pair, "a") - function(pair, "b")
    groups = [np.flatnonzero(codes == k) for k in range(n)]
    rng = np.random.default_rng(seed)
    draws = np.empty(n_boot)
    for i in range(n_boot):
        rows = np.concatenate([groups[k] for k in _block_indices(n, block, rng)])
        sample = pair.iloc[rows]
        draws[i] = function(sample, "a") - function(sample, "b")
    tail = (1.0 - level) / 2.0
    low, high = np.nanquantile(draws, [tail, 1.0 - tail])
    return BootstrapResult(float(estimate), float(low), float(high), int(n), int(block))


def weekly_loss(pair: pd.DataFrame, side: str, loss: str) -> pd.Series:
    """One number per target week: the loss averaged over that week's neighborhoods."""
    frame = cell_losses(pair, side)
    frame["target_date"] = pair["target_date"].to_numpy()
    return frame.groupby("target_date")[loss].mean().sort_index()


# --- multiple comparisons -------------------------------------------------

def holm(p_values) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values (family-wise error), same order as input.

    Uniformly more powerful than plain Bonferroni and valid under any
    dependence between the tests, which matters here: every arm is compared
    against the same reference on the same weeks, so the tests are correlated.
    """
    p = np.asarray(p_values, float)
    out = np.full_like(p, np.nan)
    finite = np.isfinite(p)
    if not finite.any():
        return out
    values = p[finite]
    order = np.argsort(values)
    m = values.size
    adjusted = np.minimum(1.0, np.maximum.accumulate((m - np.arange(m)) * values[order]))
    back = np.empty(m)
    back[order] = adjusted
    out[finite] = back
    return out
