"""Calibrated 95% predictive intervals, by the same method for every model.

A forecast without an interval says nothing about its own reliability, and
intervals built by different recipes cannot be compared. So one recipe is used
throughout, fitted on the validation split and applied unchanged to the test
split:

  1. Residual variance is modelled as affine in the predicted level,
     Var(residual) ~= alpha_h + beta_h * max(level, 0), fitted per horizon by
     least squares on validation residuals. A single absolute width would be
     far too wide through the flat off-season (mean rate ~5 per 100,000) and too
     narrow at the winter peak (~60), so the width has to scale with the level.

  2. Where a model supplies its own uncertainty -- MC-Dropout spread for the
     GCN -- that variance is added, so the band widens where the model itself is
     unsure. Models without such a component simply pass epistemic=None.

  3. A per-horizon scalar kappa rescales the band so that empirical coverage on
     the validation split is 95%. This is what makes the bands comparable across
     models: none of them relies on the residuals actually being Gaussian, and
     all of them are calibrated against the same held-out weeks.

Validation residuals, never test residuals: an interval fitted on the data it is
then scored against is not a prediction.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

Z95 = 1.959964
TARGET_COVERAGE = 0.95


@dataclass
class IntervalModel:
    """Fitted interval parameters, one set per horizon."""

    alpha: dict[int, float] = field(default_factory=dict)
    beta: dict[int, float] = field(default_factory=dict)
    kappa: dict[int, float] = field(default_factory=dict)
    n_validation: int = 0
    fitted: bool = True
    note: str = ""

    def to_json(self) -> dict:
        return {
            "method": "affine-in-level residual variance, kappa-calibrated to 95% on validation",
            "alpha": {str(k): v for k, v in self.alpha.items()},
            "beta": {str(k): v for k, v in self.beta.items()},
            "kappa": {str(k): v for k, v in self.kappa.items()},
            "n_validation": self.n_validation,
            "fitted": self.fitted,
            "note": self.note,
        }

    def bounds(self, predicted, horizon, epistemic=None) -> tuple[np.ndarray, np.ndarray]:
        """95% lower and upper bounds for flat arrays of predictions.

        `horizon` labels each prediction so the right per-horizon parameters
        apply. `epistemic` is an optional variance to add.
        """
        predicted = np.asarray(predicted, dtype=float)
        horizon = np.asarray(horizon)
        variance = np.zeros_like(predicted)
        scale = np.ones_like(predicted)

        for h in np.unique(horizon):
            mask = horizon == h
            key = int(h)
            alpha = self.alpha.get(key, float(np.nanvar(predicted[mask])) or 1.0)
            beta = self.beta.get(key, 0.0)
            variance[mask] = alpha + beta * np.maximum(predicted[mask], 0.0)
            scale[mask] = self.kappa.get(key, 1.0)

        if epistemic is not None:
            variance = variance + np.clip(np.asarray(epistemic, dtype=float), 0.0, None)

        half_width = scale * Z95 * np.sqrt(np.maximum(variance, 0.0))
        # ILI rates cannot be negative, so the lower bound is clipped at zero.
        return np.maximum(0.0, predicted - half_width), predicted + half_width


def fit_intervals(predicted, actual, horizon, *, epistemic=None) -> IntervalModel:
    """Fit the interval model on validation predictions."""
    predicted = np.asarray(predicted, dtype=float)
    actual = np.asarray(actual, dtype=float)
    horizon = np.asarray(horizon)
    epistemic = None if epistemic is None else np.asarray(epistemic, dtype=float)

    usable = np.isfinite(predicted) & np.isfinite(actual)
    model = IntervalModel(n_validation=int(usable.sum()))

    if usable.sum() < 10:
        model.fitted = False
        model.note = (f"only {int(usable.sum())} usable validation points; "
                      "falling back to a constant band from the prediction variance")
        return model

    for h in np.unique(horizon):
        mask = usable & (horizon == h)
        key = int(h)
        if mask.sum() < 10:
            model.alpha[key] = float(np.nanvar(actual[mask])) or 1.0
            model.beta[key] = 0.0
            model.kappa[key] = 1.0
            continue

        level = np.maximum(predicted[mask], 0.0)
        squared = (predicted[mask] - actual[mask]) ** 2
        design = np.column_stack([np.ones(mask.sum()), level])
        coefficients, *_ = np.linalg.lstsq(design, squared, rcond=None)
        alpha = max(float(coefficients[0]), 0.0)
        beta = max(float(coefficients[1]), 0.0)
        if alpha <= 0.0 and beta <= 0.0:
            # A degenerate fit would give a zero-width band; keep a floor.
            alpha = float(squared.mean())
        model.alpha[key] = alpha
        model.beta[key] = beta

        variance = alpha + beta * level
        if epistemic is not None:
            variance = variance + np.clip(epistemic[mask], 0.0, None)
        std = np.sqrt(np.maximum(variance, 1e-12))
        z = np.abs((predicted[mask] - actual[mask]) / std)
        z = z[np.isfinite(z)]
        model.kappa[key] = max(float(np.quantile(z, TARGET_COVERAGE)) / Z95, 1e-6) if z.size else 1.0

    return model


def empirical_coverage(actual, lower, upper) -> float:
    """Percentage of observations that fell inside the band."""
    actual = np.asarray(actual, dtype=float)
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    keep = np.isfinite(actual) & np.isfinite(lower) & np.isfinite(upper)
    if not keep.any():
        return float("nan")
    return float(((actual[keep] >= lower[keep]) & (actual[keep] <= upper[keep])).mean() * 100)


def attach_intervals(predictions, model: IntervalModel, *, epistemic=None):
    """Add `lower`/`upper` columns to a long-form predictions frame."""
    lower, upper = model.bounds(
        predictions["predicted"].to_numpy(),
        predictions["horizon"].to_numpy(),
        epistemic=epistemic,
    )
    out = predictions.copy()
    out["lower"] = lower
    out["upper"] = upper
    return out
