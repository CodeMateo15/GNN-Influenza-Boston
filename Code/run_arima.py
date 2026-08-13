"""ARIMA baseline for weekly Boston neighborhood influenza rates.

One univariate model per neighborhood: the order is chosen by walk-forward
validation RMSE, then the fitted state is rolled forward one observed week at a
time across the test window.

    python Code/run_arima.py --variant post_covid
"""

from __future__ import annotations

import argparse
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
    NEIGHBORHOODS,
    SHORT_NAMES,
    Window,
    finish_run,
    load_rates,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import add_common_args, resolve_variants, resolve_window
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
) -> tuple[int, int, int]:
    """Grid search (p, d, q) by one-step walk-forward RMSE on the validation origins.

    An order that needs the fallback path on validation is disqualified outright:
    its RMSE would be the fallback's, which says nothing about the order itself
    and would happily select a model that diverges on the test window.
    """
    best_order, best_rmse = (1, 0, 0), np.inf
    actual = np.asarray([series.loc[d + pd.Timedelta(weeks=1)] for d in val_dates], dtype=float)
    for p in range(MAX_P):
        for d in range(MAX_D):
            for q in range(MAX_Q):
                order = (p, d, q)
                preds, fallbacks = walk_forward_forecasts(
                    series, order, val_dates, steps=1, initial_end=train_dates[-1]
                )
                if fallbacks:
                    continue
                rmse = _selection_rmse(preds, actual)
                if np.isfinite(rmse) and rmse < best_rmse:
                    best_order, best_rmse = order, rmse
    return best_order


def _selection_rmse(preds: list[np.ndarray], actual: np.ndarray) -> float:
    """One-step validation RMSE used for order selection.

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


def run_variant(rates: pd.DataFrame, variant: str, window: Window, args: argparse.Namespace) -> None:
    data = variant_data(rates, variant)
    origins = valid_origins(data.index, window)
    split = split_origins(data.index, origins, window)

    train_dates = split.origin_dates(split.train)
    val_dates = split.origin_dates(split.val)
    test_dates = split.origin_dates(split.test)

    print(f"\n{'=' * 72}\nARIMA | {variant}\n{'=' * 72}")
    print(f"Train origins: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    print(f"Test targets: {split.index[split.test[0] + 1].date()} -> "
          f"{split.index[split.test[-1] + window.max_horizon].date()}")

    # Tracking covers only the fitting work, and must close before finish_run,
    # which serialises the emissions summary.
    with track_emissions(f"{MODEL}:{variant}", enabled=not args.no_carbon) as carbon:
        records: list[dict] = []
        val_records: list[dict] = []
        fallback_count = 0
        missing_targets = 0
        selected: dict[str, tuple[int, int, int]] = {}
        for idx, neighborhood in enumerate(NEIGHBORHOODS):
            # The NaN-holed calendar keeps true week spacing across an excluded
            # window, so the Kalman filter does not treat a gap as contiguous.
            series = data.calendar[neighborhood]
            order = select_order(series, train_dates, val_dates)
            selected[neighborhood] = order
            print(f"[{idx + 1:02d}/{len(NEIGHBORHOODS)}] {SHORT_NAMES[idx]:12s} selected ARIMA{order}")

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
                                   validation["horizon"])
    predictions = attach_intervals(predictions, interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")
    orders_table = pd.DataFrame(
        [{"neighborhood": n, "order": str(o)} for n, o in selected.items()]
    )
    print(f"Fallback forecasts: {fallback_count} | "
          f"suppressed target cells (not scored): {missing_targets}")

    finish_run(
        model=MODEL,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": "level",
            "normalize": "none",
            "window": window.to_json(),
            "split": split.to_json(),
            "order_grid": {"p": MAX_P - 1, "d": MAX_D - 1, "q": MAX_Q - 1},
            "selected_orders": {n: str(o) for n, o in selected.items()},
            "fallback_forecasts": fallback_count,
            "missing_target_cells": missing_targets,
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        extra_tables={"selected_orders": orders_table},
        results_root=args.output_dir,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    window = resolve_window(args, Window())
    rates = load_rates()
    print(f"Loaded {len(rates)} weekly dates and {rates.shape[1]} neighborhoods")
    for variant in resolve_variants(args.variant):
        run_variant(rates, variant, window, args)


if __name__ == "__main__":
    main()
