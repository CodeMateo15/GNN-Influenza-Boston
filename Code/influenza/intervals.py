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

--- The symmetry problem, and the two-sided option -------------------------

Steps 1-3 produce a band that is symmetric about the point forecast, because a
variance has no side. The residuals here are not symmetric, and the reason is
the forecast lag documented in Code/compare_timing.py: every model in this
project tracks the season's shape but arrives a week or two behind it, so it
reads low while the curve climbs and high while it falls. At horizon 2 that
showed up in `gnn_st` as 95.5% coverage overall but **83.9% on weeks when the
curve was climbing** against 97.4% when it was falling. The band was not too
narrow on average; it was the wrong shape, and a single kappa could only trade
one regime against the other.

`two_sided=True` fits the two edges separately, by quantile regression of the
signed residual on the same level term plus the model's own uncertainty:

    upper edge  ~  quantile 0.975 of (actual - predicted)
    lower edge  ~  quantile 0.025 of (actual - predicted)

both linear in [1, max(predicted, 0)], then a single kappa as in step 3 so the
pair still lands on 95% overall.

Measured on the committed horizon-2 `gnn_st` predictions with an interleaved
holdout -- fitted on the odd test weeks, scored on the even ones -- this moves
the worst regime from 13.8 points off 95% to 4.7, and the mean miss across
rising / flat / falling weeks from 6.6 points to 3.1. The extra width goes
where the uncertainty is: flu-season mean width rises from 47.9 to 67.0 per
100,000 while **off-season width is unchanged at 24.6 against 24.7**, which is
the check that matters, since the flat months are most of the year and an
inflated band would be most obviously wrong across them.

Two things were tried first and did not work, recorded so they are not tried
again:

  * **A momentum term in the variance**, Var += gamma * (weekly change at the
    origin)^2. Fitted by least squares alongside the level term, gamma comes out
    exactly 0.0: the two columns are collinear in season -- a high level is a
    fast-moving level -- so the level term absorbs it. Added to the two-sided fit
    as a fourth regressor it takes a NEGATIVE coefficient on the upper edge,
    which is the wrong sign for the mechanism it is supposed to represent, and
    improves the worst regime by 1.4 points. That is noise being fitted, not a
    momentum effect, so it is not here.

  * **Turning it on for every model.** It is a flag, not the new default, and the
    reason is `seasonal_naive`: its band goes from 97.4% coverage to 89.5%, and
    on falling weeks from 98.1% to 80.6%. Both edges here are linear in the
    model's OWN predicted level, which only carries information about the spread
    of its own residuals if the prediction is about this season. The seasonal
    baseline predicts last year's value, so its level says little about this
    year's error, and a level-linear edge is the wrong shape for it. The old
    symmetric recipe hid that by over-covering. Turn the flag on for all models
    or none of them, so the widths stay comparable -- that is what the shared
    recipe buys, and a per-model switch would spend it.

  * **A second kappa per side**, or per side and per direction of travel, on top
    of the level-only variance. Both fix the rising weeks by breaking the falling
    ones (87.5% and 88.9% respectively), because a one-sided 2.5% tail estimated
    from a few hundred validation cells has only a handful of exceedances in it.
    Letting the level regressor carry the asymmetry, as the two-sided fit does,
    is what makes it estimable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

Z95 = 1.959964
TARGET_COVERAGE = 0.95
# Ceiling on the calibration scale. Reaching it means the two-sided fit
# degenerated, not that the residuals are genuinely that wide, so the fit is
# abandoned for that horizon rather than scaled up without limit.
MAX_KAPPA = 16.0


@dataclass
class IntervalModel:
    """Fitted interval parameters, one set per horizon."""

    alpha: dict[int, float] = field(default_factory=dict)
    beta: dict[int, float] = field(default_factory=dict)
    kappa: dict[int, float] = field(default_factory=dict)
    # Per-horizon coefficients for the two edges, [const, level, sqrt(epistemic)],
    # present only when fitted with two_sided=True. Empty means the symmetric
    # variance recipe, which is what every run before September 2026 used and
    # what `two_sided=False` still reproduces exactly.
    upper_coef: dict[int, list[float]] = field(default_factory=dict)
    lower_coef: dict[int, list[float]] = field(default_factory=dict)
    n_validation: int = 0
    fitted: bool = True
    note: str = ""

    @property
    def two_sided(self) -> bool:
        """True when the two edges were fitted separately, so the band is skewed."""
        return bool(self.upper_coef and self.lower_coef)

    def to_json(self) -> dict:
        method = "affine-in-level residual variance, kappa-calibrated to 95% on validation"
        if self.two_sided:
            method = ("two-sided quantile regression of the signed residual on the "
                      "predicted level, kappa-calibrated to 95% on validation")
        payload = {
            "method": method,
            "alpha": {str(k): v for k, v in self.alpha.items()},
            "beta": {str(k): v for k, v in self.beta.items()},
            "kappa": {str(k): v for k, v in self.kappa.items()},
            "n_validation": self.n_validation,
            "fitted": self.fitted,
            "note": self.note,
        }
        if self.two_sided:
            payload["edge_terms"] = ["const", "level"]
            payload["upper_coef"] = {str(k): v for k, v in self.upper_coef.items()}
            payload["lower_coef"] = {str(k): v for k, v in self.lower_coef.items()}
        return payload

    def bounds(self, predicted, horizon, epistemic=None) -> tuple[np.ndarray, np.ndarray]:
        """95% lower and upper bounds for flat arrays of predictions.

        `horizon` labels each prediction so the right per-horizon parameters
        apply. `epistemic` is an optional variance to add.
        """
        predicted = np.asarray(predicted, dtype=float)
        horizon = np.asarray(horizon)
        if self.two_sided:
            return self._two_sided_bounds(predicted, horizon, epistemic)

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

    def _two_sided_bounds(self, predicted, horizon, epistemic):
        """The skewed band: each edge from its own fitted quantile."""
        above = np.zeros_like(predicted)
        below = np.zeros_like(predicted)
        for h in np.unique(horizon):
            mask = horizon == h
            key = int(h)
            upper = self.upper_coef.get(key)
            lower = self.lower_coef.get(key)
            if upper is None or lower is None:
                # A horizon with too few validation rows keeps the symmetric
                # fallback rather than borrowing another horizon's shape.
                alpha = self.alpha.get(key, float(np.nanvar(predicted[mask])) or 1.0)
                beta = self.beta.get(key, 0.0)
                half = (self.kappa.get(key, 1.0) * Z95
                        * np.sqrt(np.maximum(alpha + beta * np.maximum(predicted[mask], 0.0), 0.0)))
                above[mask] = half
                below[mask] = half
                continue
            design = _edge_design(predicted[mask])
            scale = self.kappa.get(key, 1.0)
            # An edge is clipped at the point forecast rather than allowed to
            # cross it: a fitted quantile that comes out on the wrong side of
            # zero would otherwise invert the band.
            above[mask] = scale * np.maximum(design @ np.asarray(upper, dtype=float), 0.0)
            below[mask] = scale * np.maximum(-(design @ np.asarray(lower, dtype=float)), 0.0)
        return np.maximum(0.0, predicted - below), predicted + above


def _edge_design(predicted) -> np.ndarray:
    """[1, level] -- the regressors both edges are linear in.

    The model's own uncertainty is deliberately NOT a third column here, and
    that is a measurement rather than an oversight. Adding `sqrt(epistemic)`
    changed coverage by nothing at all on the horizon-2 holdout -- 96.4% overall
    and 95.3% on rising weeks either way, mean width within 0.1 per 100,000 --
    and took a negative coefficient on the upper edge, which is the wrong sign
    for "the model is unsure, so widen". MC-Dropout spread is largely a function
    of the level already, so once both edges scale with the level there is
    nothing left for it to explain.

    Leaving it out has a second benefit worth naming: the two-sided band needs
    only the point forecast, so it is the same two numbers per side for every
    model in the project, which is what the shared-recipe claim in
    docs/METHODS.md rests on. The epistemic term still enters the SYMMETRIC
    recipe unchanged.
    """
    level = np.maximum(np.asarray(predicted, dtype=float), 0.0)
    return np.column_stack([np.ones_like(level), level])


def _quantile_fit(design: np.ndarray, residual: np.ndarray, tau: float) -> np.ndarray:
    """Quantile regression by linear programming -- exact, not iterative.

    The pinball loss is piecewise linear, so minimising it is an LP:

        min  sum(tau * u + (1 - tau) * v)
        s.t. design @ c + u - v = residual,  u >= 0, v >= 0,  c free

    so that u - v is the residual-minus-fit, u its positive part and v its
    negative part. Writing the constraint the other way round negates the error
    and fits the 1-tau quantile instead, which shows up as a level slope of the
    wrong sign.

    Solved with HiGHS. A gradient method on the same objective is a poor fit --
    the loss is not differentiable at the knots, which is where the solution
    sits -- and a Powell search on it gave visibly unconverged coefficients.
    """
    from scipy.optimize import linprog

    n, p = design.shape
    identity = np.eye(n)
    a_eq = np.hstack([design, identity, -identity])
    cost = np.concatenate([np.zeros(p), np.full(n, tau), np.full(n, 1.0 - tau)])
    bounds = [(None, None)] * p + [(0, None)] * (2 * n)
    result = linprog(cost, A_eq=a_eq, b_eq=residual, bounds=bounds, method="highs")
    if not result.success:
        # Fall back to the unconditional quantile rather than raising: a band
        # that ignores the level still covers, and a failed solve should not
        # take a completed training run down with it.
        coefficients = np.zeros(p)
        coefficients[0] = float(np.quantile(residual, tau))
        return coefficients
    return np.asarray(result.x[:p], dtype=float)


def _coverage_kappa(model: IntervalModel, key: int, predicted, actual) -> float:
    """Scale on both edges that lands this horizon on TARGET_COVERAGE.

    Bisection rather than a closed form: the two-sided band is asymmetric, so
    the 95th percentile of |z| no longer describes its coverage. Coverage is
    non-decreasing in the scale -- a wider band can only admit more points -- so
    the search is well posed.
    """
    horizon = np.full(len(predicted), key)

    def coverage(scale: float) -> float:
        probe = IntervalModel(alpha=model.alpha, beta=model.beta,
                              upper_coef=model.upper_coef, lower_coef=model.lower_coef,
                              kappa={key: scale})
        lower, upper = probe.bounds(predicted, horizon)
        return float(((actual >= lower) & (actual <= upper)).mean())

    low, high = 1e-6, 1.0
    while high <= MAX_KAPPA and coverage(high) < TARGET_COVERAGE:
        low, high = high, high * 2.0
    if high > MAX_KAPPA:
        # The band cannot reach 95% at any sane scale, which means the fitted
        # edges collapsed rather than that the data are wide. Signal it so the
        # caller can drop back to the symmetric recipe instead of shipping a
        # band scaled by 2^30.
        return float("nan")
    for _ in range(60):
        middle = 0.5 * (low + high)
        if coverage(middle) >= TARGET_COVERAGE:
            high = middle
        else:
            low = middle
    return max(high, 1e-6)


def fit_intervals(predicted, actual, horizon, *, epistemic=None,
                  two_sided: bool = False) -> IntervalModel:
    """Fit the interval model on validation predictions.

    `two_sided=True` fits the two edges of the band separately, which is what
    stops a lagged forecast under-covering the weeks when the curve is climbing.
    See the module docstring for the measurement and for what was tried first.
    Default False, so every committed metrics.csv reproduces unchanged.
    """
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

        if two_sided:
            # Signed, not squared: which side of the forecast the truth fell on
            # is the whole point, and it is exactly what the variance recipe
            # above throws away.
            residual = actual[mask] - predicted[mask]
            design = _edge_design(predicted[mask])
            tail = (1.0 - TARGET_COVERAGE) / 2.0
            model.upper_coef[key] = _quantile_fit(design, residual, 1.0 - tail).tolist()
            model.lower_coef[key] = _quantile_fit(design, residual, tail).tolist()
            # Quantile regression is self-calibrating on the rows it was fitted
            # to, so this lands very near 1.0; it is here as the safety net that
            # keeps the nominal 95% honest if the two edges disagree.
            scale = _coverage_kappa(model, key, predicted[mask], actual[mask])
            if np.isfinite(scale):
                model.kappa[key] = scale
                continue
            model.upper_coef.pop(key, None)
            model.lower_coef.pop(key, None)
            model.note = (f"{model.note} two-sided fit degenerated at horizon {key}; "
                          f"fell back to the symmetric band").strip()
            # Falls through to the symmetric calibration below.

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
