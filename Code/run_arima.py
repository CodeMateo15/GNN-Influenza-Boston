"""ARIMA baseline for weekly Boston neighborhood influenza rates.

One univariate model per neighborhood: the order is chosen by walk-forward
validation RMSE, then the fitted state is rolled forward one observed week at a
time across the test window.

    python Code/run_arima.py --variant post_covid
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import sys
import warnings

try:
    import numpy as np
    import pandas as pd
    from statsmodels.tsa.arima.model import ARIMA
except ImportError as exc:  # pragma: no cover - friendly command-line failure
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib statsmodels."
    ) from exc

from influenza import (
    Window,
    finish_run,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_variants, resolve_window, run_tag)
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals

MODEL = "arima"
MAX_P = MAX_Q = 4
MAX_D = 2


# Forecasts above this multiple of the observed historical maximum are treated
# as a diverged fit rather than a prediction. `enforce_stationarity=False` lets
# statsmodels return explosive AR roots, and an explosive forecast is perfectly
# finite -- Dorchester once produced 1e34 on the first test week and grew 1.5x
# weekly -- so an isfinite() check alone does not catch it.
DIVERGENCE_FACTOR = 10.0
DIVERGENCE_FLOOR = 10.0


def forecast_bound(history: pd.Series) -> float:
    """Largest forecast value considered a prediction rather than a divergence."""
    observed = history.dropna()
    peak = float(observed.max()) if len(observed) else 0.0
    return max(peak * DIVERGENCE_FACTOR, DIVERGENCE_FLOOR)


def _check(values: np.ndarray, steps: int, bound: float) -> np.ndarray:
    if values.size != steps or not np.all(np.isfinite(values)):
        raise ValueError("non-finite ARIMA forecast")
    if np.any(np.abs(values) > bound):
        raise ValueError(f"diverged ARIMA forecast (|{np.max(np.abs(values)):.3g}| > {bound:.3g})")
    return values


def safe_forecast(history: pd.Series, order: tuple[int, int, int], steps: int) -> tuple[np.ndarray, bool]:
    """Forecast, falling back to the last observed value if the fit fails."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fitted = ARIMA(history, order=order, enforce_stationarity=False,
                           enforce_invertibility=False).fit()
            values = np.asarray(fitted.forecast(steps=steps), dtype=float)
        return _check(values, steps, forecast_bound(history)), False
    except Exception:
        observed = history.dropna()
        fallback = float(observed.iloc[-1]) if len(observed) else 0.0
        return np.full(steps, fallback), True


def walk_forward_forecasts(
    series: pd.Series,
    order: tuple[int, int, int],
    origins: pd.DatetimeIndex,
    steps: int,
    initial_end: pd.Timestamp | None = None,
) -> tuple[list[np.ndarray], int]:
    """Fit once, then update the model state with each newly observed week."""
    forecasts: list[np.ndarray] = []
    fallbacks = 0
    first_end = initial_end if initial_end is not None else origins[0]
    bound = forecast_bound(series.loc[:first_end])
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = ARIMA(series.loc[:first_end], order=order, enforce_stationarity=False,
                           enforce_invertibility=False).fit()
        last_end = first_end
        for origin in origins:
            new_values = series.loc[(series.index > last_end) & (series.index <= origin)]
            if len(new_values):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    result = result.append(new_values, refit=False)
            values = np.asarray(result.forecast(steps=steps), dtype=float)
            forecasts.append(_check(values, steps, bound))
            last_end = origin
    except Exception:
        forecasts = []
        for origin in origins:
            values, fallback = safe_forecast(series.loc[:origin], order, steps)
            forecasts.append(values)
            fallbacks += int(fallback)
    return forecasts, fallbacks


def select_order(
    series: pd.Series,
    train_dates: pd.DatetimeIndex,
    val_dates: pd.DatetimeIndex,
    window: Window,
    *,
    max_d: int = MAX_D,
) -> tuple[int, int, int]:
    """Grid search (p, d, q) by walk-forward RMSE on the validation origins,
    scored at the horizon the run will actually be evaluated at.

    Scoring at one step regardless of horizon would pick the order that best
    predicts next week and then apply it a year out, which are not the same
    question: a (0,1,1) random walk is near-optimal at one week and a straight
    line at fifty-two.

    An order that needs the fallback path on validation is disqualified outright:
    its RMSE would be the fallback's, which says nothing about the order itself
    and would happily select a model that diverges on the test window.
    """
    horizon, steps = window.min_horizon, window.max_horizon
    best_order, best_rmse = (1, 0, 0), np.inf
    actual = np.asarray([series.loc[d + pd.Timedelta(weeks=horizon)] for d in val_dates],
                        dtype=float)
    for p in range(MAX_P):
        for d in range(max_d):
            for q in range(MAX_Q):
                order = (p, d, q)
                preds, fallbacks = walk_forward_forecasts(
                    series, order, val_dates, steps=steps, initial_end=train_dates[-1]
                )
                if fallbacks:
                    continue
                # Keep one value per origin -- the week being scored -- so the
                # shape check in _selection_rmse still compares elementwise.
                rmse = _selection_rmse([f[horizon - 1:horizon] for f in preds], actual)
                if np.isfinite(rmse) and rmse < best_rmse:
                    best_order, best_rmse = order, rmse
    return best_order


def _selection_rmse(preds: list[np.ndarray], actual: np.ndarray) -> float:
    """Validation RMSE at the scored horizon, used for order selection.

    `ravel()` matters: `preds` is a list of length-1 arrays, so `np.asarray`
    gives shape (n, 1), and subtracting the (n,) actuals would broadcast into an
    (n, n) outer difference instead of comparing elementwise. The pre-refactor
    code had exactly that bug. `nanmean` skips validation weeks whose target was
    suppressed upstream.
    """
    predicted = np.asarray(preds, dtype=float).ravel()
    if predicted.size != actual.size:
        raise ValueError(f"forecast/actual length mismatch: {predicted.size} vs {actual.size}")
    squared = (predicted - actual) ** 2
    return float(np.sqrt(np.nanmean(squared))) if np.any(np.isfinite(squared)) else np.inf


def run_variant(rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, checkpoint_root = city_output_dirs(args, city)
    data = variant_data(rates, variant)
    origins = valid_origins(data.index, window)
    split = split_origins(data.index, origins, window)

    train_dates = split.origin_dates(split.train)
    val_dates = split.origin_dates(split.val)
    test_dates = split.origin_dates(split.test)

    print(f"\n{'=' * 72}\nARIMA | {variant}\n{'=' * 72}")
    print(f"Train origins: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    first_target, last_target = split.test_target_span()
    print(f"Test targets: {first_target.date()} -> {last_target.date()}")

    # Tracking covers only the fitting work, and must close before finish_run,
    # which serialises the emissions summary.
    with track_emissions(run_tag(MODEL, variant, window), enabled=not args.no_carbon) as carbon:
        records: list[dict] = []
        val_records: list[dict] = []
        fallback_count = 0
        missing_targets = 0
        selected: dict[str, tuple[int, int, int]] = {}
        for idx, neighborhood in enumerate(city.node_names):
            # The NaN-holed calendar keeps true week spacing across an excluded
            # window, so the Kalman filter does not treat a gap as contiguous.
            series = data.calendar[neighborhood]
            order = select_order(series, train_dates, val_dates, window, max_d=args.max_d)
            selected[neighborhood] = order
            print(f"[{idx + 1:02d}/{city.n_neigh}] {city.short_names[idx]:12s} selected ARIMA{order}")

            # Validation forecasts with the *selected* order, so the predictive
            # interval is calibrated on the same held-out weeks every other model
            # uses rather than on the order-search residuals.
            val_forecasts, _ = walk_forward_forecasts(
                series, order, val_dates, window.max_horizon, initial_end=train_dates[-1]
            )
            for position, forecast in zip(split.val, val_forecasts):
                for horizon in window.horizons:
                    target_date = split.index[position + horizon]
                    val_records.append({
                        "horizon": horizon,
                        "actual": float(data.available.at[target_date, neighborhood]),
                        "predicted": max(0.0, float(forecast[horizon - 1])),
                    })

            forecasts, failures = walk_forward_forecasts(series, order, test_dates, window.max_horizon)
            fallback_count += failures
            for position, forecast in zip(split.test, forecasts):
                for horizon in window.horizons:
                    target_date = split.index[position + horizon]
                    # NaN when BPHC suppressed that neighborhood-week; carried
                    # through so build_metrics drops it instead of scoring a zero.
                    actual = float(data.available.at[target_date, neighborhood])
                    missing_targets += int(not np.isfinite(actual))
                    predicted = max(0.0, float(forecast[horizon - 1]))
                    records.append({
                        "origin_date": split.index[position],
                        "target_date": target_date,
                        "horizon": horizon,
                        "neighborhood": neighborhood,
                        "actual": actual,
                        "predicted": predicted,
                        "error": predicted - actual,
                        "arima_order": str(order),
                    })

    predictions = pd.DataFrame(records)
    validation = pd.DataFrame(val_records)
    interval_model = fit_intervals(validation["predicted"], validation["actual"],
                                   validation["horizon"],
                                   two_sided=args.two_sided_intervals)
    predictions = attach_intervals(predictions, interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")
    orders_table = pd.DataFrame(
        [{"neighborhood": n, "order": str(o)} for n, o in selected.items()]
    )
    n_forecasts = city.n_neigh * len(split.test)
    fallback_share = fallback_count / n_forecasts if n_forecasts else 0.0
    print(f"Fallback forecasts: {fallback_count}/{n_forecasts} ({fallback_share:.1%}) | "
          f"suppressed target cells (not scored): {missing_targets}")
    if fallback_count:
        # The fallback is "repeat the last observed value" -- persistence. At long
        # horizons a d>=1 fit extrapolates a line or a parabola, trips the
        # divergence guard, and lands here for every origin, producing a
        # completed run whose metrics are persistence's under an ARIMA label.
        # Say so at the point of failure; compare_horizons.py flags it again.
        print(f"warning: {fallback_share:.1%} of test forecasts fell back to the last "
              f"observed value, i.e. persistence. Treat this row as degraded, not as "
              f"an ARIMA result. Try --max-d 1 to cap the extrapolation degree.",
              file=sys.stderr)

    finish_run(
        model=MODEL,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": "level",
            "normalize": "none",
            "window": window.to_json(),
            "split": split.to_json(),
            "order_grid": {"p": MAX_P - 1, "d": args.max_d - 1, "q": MAX_Q - 1},
            "selected_orders": {n: str(o) for n, o in selected.items()},
            "fallback_forecasts": fallback_count,
            "fallback_share": fallback_share,
            "selection_horizon": window.min_horizon,
            "missing_target_cells": missing_targets,
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        extra_tables={"selected_orders": orders_table},
        results_root=results_root,
        city=city,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--max-d", type=int, default=MAX_D,
                        help="Exclusive upper bound on the differencing order d. "
                             "Default 2 (so d in {0,1}). At long horizons d=1 already "
                             "extrapolates a straight line for the whole forecast, so "
                             "capping it is the cheapest guard against divergence.")
    args = parser.parse_args()
    if not 1 <= args.max_d <= MAX_D:
        parser.error(f"--max-d must be between 1 and {MAX_D}")
    return args


def main() -> None:
    args = parse_args()
    window = resolve_window(args, Window(), resolve_city(args))
    city = resolve_city(args)
    rates = city.loaders.load_rates()
    print(f"Loaded {len(rates)} weekly dates and {rates.shape[1]} neighborhoods")
    for variant in resolve_variants(args.variant):
        run_variant(rates, variant, window, args, city)


if __name__ == "__main__":
    main()
