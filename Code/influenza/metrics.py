"""The single metric implementation for every model in this project.

Core metrics are RMSE, MAPE, MAE and Pearson correlation (Corr). Every model
reports exactly these, so `compare_models.py` can rank them against each other.

Two independent axes are reported:

  segment  which target weeks are scored -- overall / flu_season / off_season
  scope    how those rows are aggregated -- neighborhood / macro / pooled /
           cross_week

Predictions are generated once over the full-year test window; segments are
row masks over that one set of predictions, never a re-run.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from .constants import FLU_MONTHS, SEGMENTS

CORE_METRICS = ("RMSE", "MAPE", "MAE", "Corr")
EXTRA_METRICS = ("R2", "Spearman", "CCC")

_ID_COLUMNS = ["model", "variant", "segment", "scope", "neighborhood", "horizon"]


def lins_ccc(predicted: np.ndarray, actual: np.ndarray) -> float:
    """Lin's concordance correlation coefficient.

    Unlike Pearson r this penalises bias and scale error, so a forecast that is
    perfectly correlated but systematically low still scores below 1.
    """
    predicted = np.asarray(predicted, float)
    actual = np.asarray(actual, float)
    if predicted.size < 2:
        return float("nan")
    mp, ma = predicted.mean(), actual.mean()
    vp, va = predicted.var(), actual.var()
    cov = float(np.mean((predicted - mp) * (actual - ma)))
    denom = vp + va + (mp - ma) ** 2
    return float(2 * cov / denom) if denom > 0 else 0.0


def metric_values(
    actual,
    predicted,
    *,
    lower=None,
    upper=None,
    extras: bool = False,
) -> dict[str, float]:
    """Core metrics for one aligned actual/predicted pair.

    Pairs with a missing actual are dropped -- suppressed BPHC weeks are not
    observations and must not be scored as zeros. `n_obs` reports how many
    survived, and `MAPE_n` how many of those were non-zero (MAPE's own domain).
    """
    actual = np.asarray(actual, float)
    predicted = np.asarray(predicted, float)
    keep = np.isfinite(actual) & np.isfinite(predicted)
    actual, predicted = actual[keep], predicted[keep]

    if actual.size == 0:
        out = {"n_obs": 0, "RMSE": np.nan, "MAPE": np.nan, "MAE": np.nan,
               "Corr": np.nan, "MAPE_n": 0}
        if extras:
            out.update({key: np.nan for key in EXTRA_METRICS})
        if lower is not None:
            out["CI_coverage"] = np.nan
        return out

    error = predicted - actual
    mask = np.abs(actual) > 1e-12
    can_correlate = actual.size > 1 and actual.std() > 0 and predicted.std() > 0

    out: dict[str, float] = {
        "n_obs": int(actual.size),
        "RMSE": float(np.sqrt(np.mean(error ** 2))),
        "MAPE": float(np.mean(np.abs(error[mask] / actual[mask])) * 100) if mask.any() else np.nan,
        "MAE": float(np.mean(np.abs(error))),
        "Corr": float(pearsonr(actual, predicted)[0]) if can_correlate else np.nan,
        "MAPE_n": int(mask.sum()),
    }

    if extras:
        ss_tot = float(np.sum((actual - actual.mean()) ** 2))
        out["R2"] = float(1 - np.sum(error ** 2) / ss_tot) if ss_tot > 0 else np.nan
        out["Spearman"] = float(spearmanr(actual, predicted)[0]) if can_correlate else np.nan
        out["CCC"] = lins_ccc(predicted, actual)

    if lower is not None and upper is not None:
        lower = np.asarray(lower, float)[keep]
        upper = np.asarray(upper, float)[keep]
        inside = (actual >= lower) & (actual <= upper)
        out["CI_coverage"] = float(np.mean(inside) * 100)

    return out


def segment_labels(target_dates, flu_months=None) -> np.ndarray:
    """'flu_season' for in-season target weeks, 'off_season' otherwise.

    `flu_months` defaults to the Northern-Hemisphere Oct-Mar set so that every
    existing call keeps its behaviour. A Southern-Hemisphere city passes its
    own: Buenos Aires peaks in epiweeks 22-24 and its season is Apr-Sep, so the
    default would label its entire epidemic "off_season" and then report that
    the off-season is where all the error is.
    """
    months = pd.DatetimeIndex(pd.to_datetime(target_dates)).month
    months_in_season = list(FLU_MONTHS if flu_months is None else flu_months)
    return np.where(np.isin(months, months_in_season), "flu_season", "off_season")


def _segment_mask(frame: pd.DataFrame, segment: str) -> pd.Series:
    if segment == "overall":
        return pd.Series(True, index=frame.index)
    return frame["segment"] == segment


def _cross_week_row(frame: pd.DataFrame) -> dict[str, float]:
    """Cross-neighborhood agreement, averaged over weeks.

    This is a different question from the per-neighborhood metrics: on a given
    week, does the model rank the 14 neighborhoods correctly?
    """
    spearmans, cccs = [], []
    for _, week in frame.groupby("target_date"):
        a = week["actual"].to_numpy(float)
        p = week["predicted"].to_numpy(float)
        keep = np.isfinite(a) & np.isfinite(p)
        a, p = a[keep], p[keep]
        if a.size > 1 and a.std() > 0 and p.std() > 0:
            spearmans.append(float(spearmanr(a, p)[0]))
            cccs.append(lins_ccc(p, a))
    return {
        "n_obs": len(spearmans),
        "Spearman": float(np.nanmean(spearmans)) if spearmans else np.nan,
        "CCC": float(np.nanmean(cccs)) if cccs else np.nan,
    }


def build_metrics(
    predictions: pd.DataFrame,
    *,
    model: str,
    variant: str,
    extras: bool = False,
    segments: tuple[str, ...] = SEGMENTS,
) -> pd.DataFrame:
    """Long-form metrics table: one row per (segment, scope, neighborhood, horizon).

    `predictions` must have columns target_date, horizon, neighborhood, actual,
    predicted, and optionally lower/upper for interval coverage.
    """
    frame = predictions.copy()
    frame["segment"] = segment_labels(frame["target_date"])
    has_bands = {"lower", "upper"}.issubset(frame.columns)

    def band(part: pd.DataFrame) -> dict:
        if not has_bands:
            return {}
        return {"lower": part["lower"].to_numpy(), "upper": part["upper"].to_numpy()}

    rows: list[dict] = []
    for segment in segments:
        seg = frame.loc[_segment_mask(frame, segment)]
        if seg.empty:
            continue
        for horizon, hdf in seg.groupby("horizon"):
            per_neighborhood: list[dict[str, float]] = []
            for neighborhood, ndf in hdf.groupby("neighborhood", sort=False):
                values = metric_values(
                    ndf["actual"].to_numpy(), ndf["predicted"].to_numpy(),
                    extras=extras, **band(ndf),
                )
                per_neighborhood.append(values)
                rows.append({
                    "model": model, "variant": variant, "segment": segment,
                    "scope": "neighborhood", "neighborhood": neighborhood,
                    "horizon": horizon, **values,
                })

            # macro: unweighted mean over neighborhoods, so a small neighborhood
            # counts as much as a large one.
            averaged = {
                key: float(np.nanmean([m[key] for m in per_neighborhood]))
                for key in per_neighborhood[0]
                if key not in ("n_obs", "MAPE_n")
            }
            rows.append({
                "model": model, "variant": variant, "segment": segment,
                "scope": "macro", "neighborhood": "AVERAGE", "horizon": horizon,
                "n_obs": int(sum(m["n_obs"] for m in per_neighborhood)),
                "MAPE_n": int(sum(m["MAPE_n"] for m in per_neighborhood)),
                **averaged,
            })

            # pooled: every (week, neighborhood) cell flattened together.
            rows.append({
                "model": model, "variant": variant, "segment": segment,
                "scope": "pooled", "neighborhood": "ALL", "horizon": horizon,
                **metric_values(hdf["actual"].to_numpy(), hdf["predicted"].to_numpy(),
                                extras=extras, **band(hdf)),
            })

            if extras:
                rows.append({
                    "model": model, "variant": variant, "segment": segment,
                    "scope": "cross_week", "neighborhood": "ALL", "horizon": horizon,
                    **_cross_week_row(hdf),
                })

    metrics = pd.DataFrame(rows)
    ordered = _ID_COLUMNS + ["n_obs"] + list(CORE_METRICS) + ["MAPE_n"]
    ordered += [c for c in metrics.columns if c not in ordered]
    return metrics[[c for c in ordered if c in metrics.columns]]


def summary_table(
    metrics: pd.DataFrame,
    *,
    segments: tuple[str, ...] = ("overall", "flu_season", "off_season"),
    scopes: tuple[str, ...] = ("macro", "pooled"),
) -> str:
    """Compact console summary of the headline rows."""
    view = metrics.loc[
        metrics["segment"].isin(segments) & metrics["scope"].isin(scopes),
        ["segment", "scope", "horizon", "n_obs", *CORE_METRICS],
    ].sort_values(["horizon", "segment", "scope"])
    return view.to_string(index=False, float_format=lambda x: f"{x:.4f}")
