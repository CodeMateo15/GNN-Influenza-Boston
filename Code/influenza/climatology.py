"""A per-node seasonal baseline, fitted on training weeks only.

Why this exists: at four weeks ahead, the origin week's rate is a poor starting
point. Measured on the 2025-26 test season, the correlation between Boston's
citywide rate and its own value four weeks earlier is 0.271, while a plain
seasonal average scores 0.697. The seasonal average does not decay with the
horizon -- it is the same curve whether you ask about next week or next quarter
-- so it becomes the better baseline exactly where autoregression fails.

The models therefore predict a residual from a *blend* of the two baselines
rather than from the origin level alone; see `models.SpatioTemporalGNN`.

Fitted in log1p space because ILI rates are strictly positive, right-skewed and
span an order of magnitude between the off-season floor and the winter peak. A
harmonic regression on the raw rate spends its budget on the peak and can go
negative in the trough.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

DEFAULT_HARMONICS = 3


def _design(index: pd.DatetimeIndex, n_harmonics: int) -> np.ndarray:
    """Intercept plus sin/cos pairs on the day-of-year angle.

    Day-of-year rather than ISO week: week 53 exists every five or six years and
    would put a discontinuity in an otherwise smooth encoding. Same reasoning,
    and the same 365.2425, as `FeatureSpec.use_seasonality` in samples.py.
    """
    angle = 2.0 * np.pi * index.dayofyear.to_numpy(dtype=np.float64) / 365.2425
    columns = [np.ones(len(index))]
    for k in range(1, n_harmonics + 1):
        columns.append(np.sin(k * angle))
        columns.append(np.cos(k * angle))
    return np.column_stack(columns)


@dataclass(frozen=True)
class Climatology:
    """Harmonic seasonal baseline, one coefficient vector per node."""

    coefficients: np.ndarray      # (n_terms, n_nodes)
    n_harmonics: int
    n_train_rows: int
    fallback_nodes: tuple[int, ...]

    def level(self, index: pd.DatetimeIndex) -> np.ndarray:
        """Expected rate per node for each week in `index`, in rate units."""
        predicted = _design(index, self.n_harmonics) @ self.coefficients
        # Back out of log1p. Clipped at zero because a rate cannot be negative
        # and expm1 of a small negative fit would produce one.
        return np.maximum(np.expm1(predicted), 0.0)

    def to_json(self) -> dict:
        return {
            "n_harmonics": self.n_harmonics,
            "n_train_rows": self.n_train_rows,
            "n_terms": int(self.coefficients.shape[0]),
            "fallback_nodes": list(self.fallback_nodes),
        }


def fit_climatology(
    rates: pd.DataFrame,
    *,
    end: int | None = None,
    n_harmonics: int = DEFAULT_HARMONICS,
) -> Climatology:
    """Fit the seasonal baseline on `rates` rows before `end`.

    `end` is a row position, not a date, matching `windows.normalization` -- pass
    `split.train[-1] + window.max_horizon + 1` so the fit sees exactly the weeks
    the training targets already revealed and no more. Leaving it None fits on
    everything, which leaks and exists only for diagnostics.

    Suppressed weeks are NaN and are dropped per node rather than imputed: a
    seasonal mean built from invented zeros would sit below the truth everywhere.
    A node with too few observations to identify the harmonics falls back to its
    own mean, which is reported rather than hidden.
    """
    frame = rates if end is None else rates.iloc[:end]
    values = frame.to_numpy(dtype=np.float64)
    design = _design(frame.index, n_harmonics)
    n_terms = design.shape[1]

    coefficients = np.zeros((n_terms, values.shape[1]), dtype=np.float64)
    fallback: list[int] = []
    for node in range(values.shape[1]):
        observed = np.isfinite(values[:, node])
        # Need more rows than terms for the fit to be identified at all; 2x is
        # the margin at which the harmonics stop chasing individual weeks.
        if int(observed.sum()) < 2 * n_terms:
            fallback.append(node)
            mean = np.nanmean(values[:, node]) if observed.any() else 0.0
            coefficients[0, node] = np.log1p(max(mean, 0.0))
            continue
        target = np.log1p(np.maximum(values[observed, node], 0.0))
        beta, *_ = np.linalg.lstsq(design[observed], target, rcond=None)
        coefficients[:, node] = beta

    return Climatology(
        coefficients=coefficients,
        n_harmonics=n_harmonics,
        n_train_rows=int(len(frame)),
        fallback_nodes=tuple(fallback),
    )
