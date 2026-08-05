"""ARIMA baselines for weekly Boston neighborhood influenza rates.

Runs the COVID-excluded and post-COVID experiments used by the GNN notebooks.
Predictions and metrics are written beneath Code/baseline_outputs by default.
"""

from __future__ import annotations

import argparse
import time
import warnings
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.stats import pearsonr
    from statsmodels.tsa.arima.model import ARIMA
except ImportError as exc:  # pragma: no cover - friendly command-line failure
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib statsmodels."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "Data" / "BPHC Flu Data" / "BPHC Dashboard Influenza Neighborhood.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "baseline_outputs"
TEST_START = pd.Timestamp("2025-10-01")
TEST_END = pd.Timestamp("2026-05-31")
COVID_START = pd.Timestamp("2020-03-01")
COVID_END = pd.Timestamp("2022-06-30")
POST_COVID_START = pd.Timestamp("2022-07-01")
LOOKBACK = 8
HORIZONS = (1, 2)

NEIGHBORHOODS = [
    "Allston/Brighton", "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown", "Dorchester", "East Boston", "Fenway", "Hyde Park",
    "Jamaica Plain", "Mattapan", "Roslindale", "Roxbury", "South Boston",
    "South End", "West Roxbury",
]
SHORT_NAMES = [
    "Allston", "BackBay+", "Charlestown", "Dorchester", "E.Boston", "Fenway",
    "HydePark", "JamaicaPlain", "Mattapan", "Roslindale", "Roxbury",
    "S.Boston", "S.End", "W.Roxbury",
]


def neighborhood_index(name: str) -> int | None:
    value = name.lower().strip()
    matches = [
        ("west roxbury", 13), ("south boston", 11), ("south end", 12),
        ("east boston", 4), ("hyde park", 6), ("jamaica plain", 7),
        ("bb/bh/dt/ne/we", 1), ("back bay", 1), ("beacon hill", 1),
        ("allston", 0), ("brighton", 0), ("charlestown", 2),
        ("dorchester", 3), ("dor ", 3), ("dor(", 3), ("fenway", 5),
        ("mattapan", 8), ("roslindale", 9), ("roxbury", 10),
    ]
    return next((idx for key, idx in matches if key in value), None)


def load_rates() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Boston influenza data not found: {DATA_FILE}")
    frame = pd.read_csv(DATA_FILE)
    frame = frame.loc[frame["date_type"].eq("Weekly")].copy()
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["rate"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["node"] = frame["demographic_value"].map(neighborhood_index)
    frame = frame.dropna(subset=["date", "rate", "node"])
    frame["node"] = frame["node"].astype(int)
    rates = frame.groupby(["date", "node"])["rate"].mean().unstack("node").sort_index()
    rates = rates.reindex(columns=range(len(NEIGHBORHOODS))).fillna(0.0)
    rates.columns = NEIGHBORHOODS
    return rates.astype(float)


def variant_data(rates: pd.DataFrame, variant: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return model series (possibly containing missing weeks) and available observations."""
    model_data = rates.copy()
    if variant == "exclude_covid":
        model_data.loc[COVID_START:COVID_END] = np.nan
        available = rates.loc[~rates.index.to_series().between(COVID_START, COVID_END)].copy()
    elif variant == "post_covid":
        model_data = rates.loc[rates.index >= POST_COVID_START].copy()
        available = model_data.copy()
    else:  # guarded by argparse
        raise ValueError(f"Unknown variant: {variant}")
    return model_data, available


def sample_origins(available: pd.DataFrame) -> list[pd.Timestamp]:
    dates = available.index
    origins: list[pd.Timestamp] = []
    for t in range(LOOKBACK, len(dates) - max(HORIZONS)):
        span = dates[t - LOOKBACK + 1 : t + max(HORIZONS) + 1]
        if len(span) == LOOKBACK + max(HORIZONS) and np.all(np.diff(span.values).astype("timedelta64[D]") == np.timedelta64(7, "D")):
            origins.append(dates[t])
    return origins


def split_origins(origins: list[pd.Timestamp]) -> tuple[list[pd.Timestamp], list[pd.Timestamp], list[pd.Timestamp]]:
    test = [d for d in origins if TEST_START <= d + pd.Timedelta(weeks=1) <= TEST_END]
    non_test = [d for d in origins if d not in set(test)]
    n_val = max(1, int(0.15 * len(non_test)))
    train, val = non_test[:-n_val], non_test[-n_val:]
    # Purge boundary samples whose two-week target overlaps the following split.
    val_target_start = val[0] + pd.Timedelta(weeks=1)
    test_target_start = test[0] + pd.Timedelta(weeks=1)
    train = [d for d in train if d + pd.Timedelta(weeks=max(HORIZONS)) < val_target_start]
    val = [d for d in val if d + pd.Timedelta(weeks=max(HORIZONS)) < test_target_start]
    if not train or not val or not test:
        raise ValueError("The configured date ranges do not yield non-empty train/validation/test sets.")
    return train, val, test


def safe_forecast(history: pd.Series, order: tuple[int, int, int], steps: int) -> tuple[np.ndarray, bool]:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fitted = ARIMA(history, order=order, enforce_stationarity=False, enforce_invertibility=False).fit()
            values = np.asarray(fitted.forecast(steps=steps), dtype=float)
        if values.size != steps or not np.all(np.isfinite(values)):
            raise ValueError("non-finite ARIMA forecast")
        return values, False
    except Exception:
        observed = history.dropna()
        fallback = float(observed.iloc[-1]) if len(observed) else 0.0
        return np.full(steps, fallback), True


def select_order(series: pd.Series, train: list[pd.Timestamp], val: list[pd.Timestamp]) -> tuple[int, int, int]:
    best_order, best_rmse = (1, 0, 0), np.inf
    actual = np.asarray([series.loc[d + pd.Timedelta(weeks=1)] for d in val], dtype=float)
    for p in range(4):
        for d in range(2):
            for q in range(4):
                order = (p, d, q)
                preds = walk_forward_forecasts(series, order, val, steps=1, initial_end=train[-1])[0]
                rmse = float(np.sqrt(np.mean((np.asarray(preds) - actual) ** 2)))
                if np.isfinite(rmse) and rmse < best_rmse:
                    best_order, best_rmse = order, rmse
    return best_order


def walk_forward_forecasts(series: pd.Series, order: tuple[int, int, int], origins: list[pd.Timestamp],
                           steps: int, initial_end: pd.Timestamp | None = None) -> tuple[list[np.ndarray], int]:
    """Fit once, then update model state with each newly observed week."""
    forecasts: list[np.ndarray] = []
    fallbacks = 0
    first_end = initial_end if initial_end is not None else origins[0]
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
            if values.size != steps or not np.all(np.isfinite(values)):
                raise ValueError("non-finite ARIMA forecast")
            forecasts.append(values)
            last_end = origin
    except Exception:
        forecasts = []
        for origin in origins:
            values, fallback = safe_forecast(series.loc[:origin], order, steps)
            forecasts.append(values); fallbacks += int(fallback)
    return forecasts, fallbacks


def metric_values(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual, predicted = np.asarray(actual, float), np.asarray(predicted, float)
    error = predicted - actual
    mask = np.abs(actual) > 1e-12
    corr = float(pearsonr(actual, predicted)[0]) if actual.size > 1 and actual.std() > 0 and predicted.std() > 0 else np.nan
    return {
        "RMSE": float(np.sqrt(np.mean(error ** 2))),
        "MAE": float(np.mean(np.abs(error))),
        "MAPE": float(np.mean(np.abs(error[mask] / actual[mask])) * 100) if mask.any() else np.nan,
        "Corr": corr,
        "MAPE_n": int(mask.sum()),
    }


def build_metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for horizon, hdf in predictions.groupby("horizon"):
        per_neighborhood = []
        for neighborhood, ndf in hdf.groupby("neighborhood", sort=False):
            values = metric_values(ndf["actual"].to_numpy(), ndf["predicted"].to_numpy())
            row = {"scope": "neighborhood", "neighborhood": neighborhood, "horizon": horizon, **values}
            rows.append(row); per_neighborhood.append(values)
        rows.append({
            "scope": "macro", "neighborhood": "AVERAGE", "horizon": horizon,
            **{key: float(np.nanmean([m[key] for m in per_neighborhood])) for key in ("RMSE", "MAE", "MAPE", "Corr")},
            "MAPE_n": int(sum(m["MAPE_n"] for m in per_neighborhood)),
        })
        rows.append({"scope": "pooled", "neighborhood": "ALL", "horizon": horizon,
                     **metric_values(hdf["actual"].to_numpy(), hdf["predicted"].to_numpy())})
    return pd.DataFrame(rows)


def save_plot(predictions: pd.DataFrame, path: Path, title: str) -> None:
    data = predictions.loc[predictions["horizon"].eq(1)]
    fig, axes = plt.subplots(4, 4, figsize=(18, 14), sharex=True, sharey=True)
    for ax, neighborhood in zip(axes.flat, NEIGHBORHOODS):
        part = data.loc[data["neighborhood"].eq(neighborhood)]
        ax.plot(part["target_date"], part["actual"], color="#2c3e50", label="Actual")
        ax.plot(part["target_date"], part["predicted"], "--", color="#e74c3c", label="Predicted")
        ax.set_title(SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)], fontsize=9)
        ax.tick_params(axis="x", rotation=35, labelsize=7)
    for ax in axes.flat[len(NEIGHBORHOODS):]: ax.axis("off")
    axes.flat[0].legend(fontsize=8)
    fig.suptitle(title)
    fig.supxlabel("Target week"); fig.supylabel("Flu rate per 100,000")
    fig.tight_layout(); fig.savefig(path, dpi=160, bbox_inches="tight"); plt.close(fig)


def run_variant(rates: pd.DataFrame, variant: str, output_root: Path) -> None:
    started = time.perf_counter()
    model_data, available = variant_data(rates, variant)
    origins = sample_origins(available)
    train, val, test = split_origins(origins)
    records, fallback_count, selected = [], 0, {}
    print(f"\n{'=' * 72}\nARIMA | {variant}\n{'=' * 72}")
    print(f"Train origins: {len(train)} | Validation: {len(val)} | Test: {len(test)}")
    for idx, neighborhood in enumerate(NEIGHBORHOODS, start=1):
        series = model_data[neighborhood]
        order = select_order(series, train, val)
        selected[neighborhood] = order
        print(f"[{idx:02d}/14] {SHORT_NAMES[idx-1]:14s} selected ARIMA{order}")
        test_forecasts, failures = walk_forward_forecasts(series, order, test, max(HORIZONS))
        fallback_count += failures
        for origin, forecast in zip(test, test_forecasts):
            for horizon in HORIZONS:
                target_date = origin + pd.Timedelta(weeks=horizon)
                actual = float(available.at[target_date, neighborhood])
                predicted = max(0.0, float(forecast[horizon - 1]))
                records.append({"origin_date": origin, "target_date": target_date, "horizon": horizon,
                                "neighborhood": neighborhood, "actual": actual, "predicted": predicted,
                                "error": predicted - actual, "arima_order": str(order)})
    predictions = pd.DataFrame(records).sort_values(["horizon", "target_date", "neighborhood"])
    metrics = build_metrics(predictions)
    out = output_root / "arima" / variant
    out.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(out / "predictions.csv", index=False)
    metrics.to_csv(out / "metrics.csv", index=False)
    pd.DataFrame([{"neighborhood": n, "order": str(o)} for n, o in selected.items()]).to_csv(out / "selected_orders.csv", index=False)
    save_plot(predictions, out / "actual_vs_predicted_horizon1.png", f"ARIMA ({variant}) — horizon 1")
    summary = metrics.loc[metrics["scope"].isin(["macro", "pooled"]), ["scope", "horizon", "RMSE", "MAE", "MAPE", "Corr"]]
    print("\nPrimary comparison and horizon summary:\n" + summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"Fallback forecasts: {fallback_count} | Runtime: {time.perf_counter() - started:.1f}s")
    print(f"Outputs: {out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["all", "exclude_covid", "post_covid"], default="all")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rates = load_rates()
    variants = ("exclude_covid", "post_covid") if args.variant == "all" else (args.variant,)
    print(f"Loaded {len(rates)} weekly dates and {rates.shape[1]} neighborhoods from {DATA_FILE}")
    for variant in variants:
        run_variant(rates, variant, args.output_dir.resolve())


if __name__ == "__main__":
    main()
