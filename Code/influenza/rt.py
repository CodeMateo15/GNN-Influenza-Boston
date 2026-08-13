"""Effective reproduction number via epyestim (the Cori et al. method).

Read docs/RT_CAVEATS.md before using this as a feature. In short: the input is a
WEEKLY per-100,000 rate, while epyestim expects DAILY case counts. Bridging that
gap requires interpolating within each week, so the result is better described as
a relative growth index than as a reproduction number, and epyestim's credible
intervals are not valid here. Only the median is kept.

Two things are done differently from the package defaults, both deliberately:

* Smoothing is trailing, not centred. epyestim's default LOWESS window is
  centred, which would make Rt(t) depend on incidence after t -- a leak, since
  Rt is used as a feature to predict later weeks.
* The generation-interval and reporting-delay distributions are influenza's, not
  the COVID defaults the package ships with.
"""

from __future__ import annotations

import hashlib
import warnings

import numpy as np
import pandas as pd

from . import paths
from .constants import NEIGHBORHOODS
from .data import impute_causal

# Influenza generation interval: mean 2.85 d, sd 0.93 d (Cauchemez et al. 2004).
GT_MEAN, GT_SD = 2.85, 0.93
# Infection to ILI presentation at an emergency department.
DELAY_MEAN, DELAY_SD = 3.0, 2.0

# Nominal population scale. Rt is driven by the ratio between successive
# incidence values, so this only affects the (discarded) interval width.
PSEUDO_POPULATION = 100_000
TRAILING_WINDOW_DAYS = 14
R_WINDOW_DAYS = 7


def _gamma_from_moments(mean: float, sd: float):
    from epyestim.distributions import discretise_gamma

    shape = (mean / sd) ** 2
    scale = sd ** 2 / mean
    return discretise_gamma(a=shape, scale=scale)


def _cache_key(rates: pd.DataFrame, causal: bool) -> str:
    digest = hashlib.sha256()
    digest.update(np.ascontiguousarray(rates.to_numpy(dtype=np.float64)).tobytes())
    digest.update(str(rates.index[0]).encode())
    digest.update(str(rates.index[-1]).encode())
    digest.update(f"{GT_MEAN},{GT_SD},{DELAY_MEAN},{DELAY_SD},{causal},"
                  f"{TRAILING_WINDOW_DAYS},{R_WINDOW_DAYS}".encode())
    return digest.hexdigest()[:16]


def weekly_rt(
    rates: pd.DataFrame,
    *,
    causal: bool = True,
    n_samples: int = 20,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Per-neighborhood weekly growth index, aligned to `rates.index`.

    Returns a (weeks x 14) frame. Bootstrapping is slow, so results are cached
    under results/_cache keyed on the data and the configuration.
    """
    cache_path = paths.CACHE_DIR / f"rt_{_cache_key(rates, causal)}.csv"
    if use_cache and cache_path.exists():
        cached = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        if list(cached.columns) == list(rates.columns) and cached.index.equals(rates.index):
            return cached

    try:
        from epyestim import bagging_r
        from epyestim.estimate_r import estimate_r
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Rt features need epyestim. Install it with 'pip install epyestim==0.1'."
        ) from exc

    generation = _gamma_from_moments(GT_MEAN, GT_SD)
    delay = _gamma_from_moments(DELAY_MEAN, DELAY_SD)
    filled, _ = impute_causal(rates)

    columns: dict[str, pd.Series] = {}
    for neighborhood in rates.columns:
        series = filled[neighborhood].astype(float)
        # Weekly rate per 100k -> nominal daily counts. The interpolation is the
        # step that makes this an approximation; see docs/RT_CAVEATS.md.
        daily = series.resample("D").interpolate("linear") / 7.0 * (PSEUDO_POPULATION / 100_000)

        if causal:
            # `bagging_r` cannot be made causal: its Richardson-Lucy
            # deconvolution and LOWESS smoothing are both fitted over the whole
            # series, so Rt(t) moves when later weeks are added -- measured at up
            # to 0.71 on this data, which would leak the future into a feature.
            # `estimate_r` is the pure Cori et al. estimator, where Rt(t) depends
            # only on incidence up to t. We pre-smooth with a trailing mean and
            # skip the delay deconvolution; the cost is that Rt is shifted later
            # in time by roughly the reporting delay.
            smoothed = daily.rolling(TRAILING_WINDOW_DAYS, min_periods=1).mean().clip(lower=0.0)
            posterior = estimate_r(smoothed, generation, a_prior=3.0, b_prior=1.0,
                                   window_size=R_WINDOW_DAYS)
            # Posterior is Gamma(a, scale=b); its mean is the Cori point estimate.
            estimated = posterior["a_posterior"] * posterior["b_posterior"]
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                bagged = bagging_r(
                    daily.clip(lower=0.0),
                    gt_distribution=generation,
                    delay_distribution=delay,
                    a_prior=3, b_prior=1,
                    smoothing_window=21,
                    r_window_size=R_WINDOW_DAYS,
                    n_samples=n_samples,
                )
            # Only the median is kept: the credible intervals assume genuine
            # daily counts and are not meaningful on interpolated data.
            estimated = bagged["Q0.5"]

        columns[neighborhood] = estimated.reindex(rates.index, method="ffill")

    result = pd.DataFrame(columns, index=rates.index)[list(rates.columns)]
    # Leading weeks precede epyestim's own start cutoff; 1.0 means "no growth".
    result = result.ffill().fillna(1.0).clip(lower=0.0, upper=10.0)

    if use_cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(cache_path)
    return result


def growth_ratio(rates: pd.DataFrame) -> pd.DataFrame:
    """Plain week-over-week ratio, for comparison against the Rt estimate.

    If Rt carries information beyond this, it should not be a simple monotone
    function of it.
    """
    filled, _ = impute_causal(rates)
    return (filled / filled.shift(1)).replace([np.inf, -np.inf], np.nan)
