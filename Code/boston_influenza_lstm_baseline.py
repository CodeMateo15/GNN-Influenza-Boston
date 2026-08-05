"""Multivariate LSTM baselines for weekly Boston neighborhood influenza rates."""

from __future__ import annotations

import argparse
import copy
import random
import time
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import torch
    import torch.nn as nn
    from scipy.stats import pearsonr
    from torch.utils.data import DataLoader, TensorDataset
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib torch."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "Data" / "BPHC Flu Data" / "BPHC Dashboard Influenza Neighborhood.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "baseline_outputs"
TEST_START, TEST_END = pd.Timestamp("2025-10-01"), pd.Timestamp("2026-05-31")
COVID_START, COVID_END = pd.Timestamp("2020-03-01"), pd.Timestamp("2022-06-30")
POST_COVID_START = pd.Timestamp("2022-07-01")
LOOKBACK, HORIZONS = 8, (1, 2)
SEED = 42

NEIGHBORHOODS = [
    "Allston/Brighton", "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown", "Dorchester", "East Boston", "Fenway", "Hyde Park",
    "Jamaica Plain", "Mattapan", "Roslindale", "Roxbury", "South Boston",
    "South End", "West Roxbury",
]
SHORT_NAMES = ["Allston", "BackBay+", "Charlestown", "Dorchester", "E.Boston", "Fenway", "HydePark", "JamaicaPlain", "Mattapan", "Roslindale", "Roxbury", "S.Boston", "S.End", "W.Roxbury"]


def neighborhood_index(name: str) -> int | None:
    value = name.lower().strip()
    matches = [
        ("west roxbury", 13), ("south boston", 11), ("south end", 12), ("east boston", 4),
        ("hyde park", 6), ("jamaica plain", 7), ("bb/bh/dt/ne/we", 1), ("back bay", 1),
        ("beacon hill", 1), ("allston", 0), ("brighton", 0), ("charlestown", 2),
        ("dorchester", 3), ("dor ", 3), ("dor(", 3), ("fenway", 5), ("mattapan", 8),
        ("roslindale", 9), ("roxbury", 10),
    ]
    return next((idx for key, idx in matches if key in value), None)


def load_rates() -> pd.DataFrame:
    if not DATA_FILE.exists(): raise FileNotFoundError(f"Boston influenza data not found: {DATA_FILE}")
    frame = pd.read_csv(DATA_FILE)
    frame = frame.loc[frame["date_type"].eq("Weekly")].copy()
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["rate"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["node"] = frame["demographic_value"].map(neighborhood_index)
    frame = frame.dropna(subset=["date", "rate", "node"]); frame["node"] = frame["node"].astype(int)
    rates = frame.groupby(["date", "node"])["rate"].mean().unstack("node").sort_index()
    rates = rates.reindex(columns=range(14)).fillna(0.0); rates.columns = NEIGHBORHOODS
    return rates.astype(float)


def variant_data(rates: pd.DataFrame, variant: str) -> pd.DataFrame:
    if variant == "exclude_covid": return rates.loc[~rates.index.to_series().between(COVID_START, COVID_END)].copy()
    if variant == "post_covid": return rates.loc[rates.index >= POST_COVID_START].copy()
    raise ValueError(f"Unknown variant: {variant}")


def sample_positions(rates: pd.DataFrame) -> list[int]:
    positions = []
    for t in range(LOOKBACK, len(rates) - max(HORIZONS)):
        span = rates.index[t - LOOKBACK + 1 : t + max(HORIZONS) + 1]
        if len(span) == LOOKBACK + max(HORIZONS) and np.all(np.diff(span.values).astype("timedelta64[D]") == np.timedelta64(7, "D")):
            positions.append(t)
    return positions


def split_positions(rates: pd.DataFrame, positions: list[int]) -> tuple[list[int], list[int], list[int]]:
    test = [t for t in positions if TEST_START <= rates.index[t + 1] <= TEST_END]
    test_set = set(test); non_test = [t for t in positions if t not in test_set]
    n_val = max(1, int(0.15 * len(non_test)))
    train, val = non_test[:-n_val], non_test[-n_val:]
    # Purge samples whose horizon-2 label overlaps the following split.
    val_target_start, test_target_start = rates.index[val[0] + 1], rates.index[test[0] + 1]
    train = [t for t in train if rates.index[t + max(HORIZONS)] < val_target_start]
    val = [t for t in val if rates.index[t + max(HORIZONS)] < test_target_start]
    if not train or not val or not test: raise ValueError("Configured dates yield an empty split.")
    return train, val, test


def arrays(rates: pd.DataFrame, positions: list[int], mean: np.ndarray, std: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    normalized = (rates.to_numpy(dtype=np.float32) - mean) / std
    x = np.stack([normalized[t - LOOKBACK + 1:t + 1] for t in positions]).astype(np.float32)
    y = np.stack([np.stack([normalized[t + h] for h in HORIZONS]) for t in positions]).astype(np.float32)
    return x, y


class MultivariateLSTM(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lstm = nn.LSTM(input_size=14, hidden_size=64, batch_first=True)
        self.output = nn.Linear(64, 14 * len(HORIZONS))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded, _ = self.lstm(x)
        return self.output(encoded[:, -1]).view(-1, len(HORIZONS), 14)


def train_model(x_train: np.ndarray, y_train: np.ndarray, x_val: np.ndarray, y_val: np.ndarray,
                device: torch.device, epochs: int, batch_size: int) -> tuple[MultivariateLSTM, int, float]:
    model = MultivariateLSTM().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    criterion = nn.MSELoss()
    generator = torch.Generator().manual_seed(SEED)
    loader = DataLoader(TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
                        batch_size=batch_size, shuffle=True, generator=generator)
    val_x, val_y = torch.from_numpy(x_val).to(device), torch.from_numpy(y_val).to(device)
    best_state, best_loss, best_epoch, patience = None, np.inf, 0, 0
    for epoch in range(1, epochs + 1):
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad(); loss = criterion(model(xb), yb); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        model.eval()
        with torch.no_grad(): val_loss = float(criterion(model(val_x), val_y).item())
        if val_loss < best_loss - 1e-7:
            best_loss, best_epoch, best_state, patience = val_loss, epoch, copy.deepcopy(model.state_dict()), 0
        else: patience += 1
        if epoch == 1 or epoch % 10 == 0: print(f"Epoch {epoch:3d} | validation MSE {val_loss:.6f}")
        if patience >= 25: break
    if best_state is not None: model.load_state_dict(best_state)
    return model, best_epoch, best_loss


def metric_values(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual, predicted = np.asarray(actual, float), np.asarray(predicted, float); error = predicted - actual
    mask = np.abs(actual) > 1e-12
    corr = float(pearsonr(actual, predicted)[0]) if actual.size > 1 and actual.std() > 0 and predicted.std() > 0 else np.nan
    return {"RMSE": float(np.sqrt(np.mean(error ** 2))), "MAE": float(np.mean(np.abs(error))),
            "MAPE": float(np.mean(np.abs(error[mask] / actual[mask])) * 100) if mask.any() else np.nan,
            "Corr": corr, "MAPE_n": int(mask.sum())}


def build_metrics(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for horizon, hdf in predictions.groupby("horizon"):
        per = []
        for neighborhood, ndf in hdf.groupby("neighborhood", sort=False):
            values = metric_values(ndf.actual.to_numpy(), ndf.predicted.to_numpy()); per.append(values)
            rows.append({"scope": "neighborhood", "neighborhood": neighborhood, "horizon": horizon, **values})
        rows.append({"scope": "macro", "neighborhood": "AVERAGE", "horizon": horizon,
                     **{k: float(np.nanmean([m[k] for m in per])) for k in ("RMSE", "MAE", "MAPE", "Corr")},
                     "MAPE_n": int(sum(m["MAPE_n"] for m in per))})
        rows.append({"scope": "pooled", "neighborhood": "ALL", "horizon": horizon,
                     **metric_values(hdf.actual.to_numpy(), hdf.predicted.to_numpy())})
    return pd.DataFrame(rows)


def save_plot(predictions: pd.DataFrame, path: Path, title: str) -> None:
    data = predictions.loc[predictions.horizon.eq(1)]
    fig, axes = plt.subplots(4, 4, figsize=(18, 14), sharex=True, sharey=True)
    for i, (ax, neighborhood) in enumerate(zip(axes.flat, NEIGHBORHOODS)):
        part = data.loc[data.neighborhood.eq(neighborhood)]
        ax.plot(part.target_date, part.actual, color="#2c3e50", label="Actual")
        ax.plot(part.target_date, part.predicted, "--", color="#e74c3c", label="Predicted")
        ax.set_title(SHORT_NAMES[i], fontsize=9); ax.tick_params(axis="x", rotation=35, labelsize=7)
    for ax in axes.flat[14:]: ax.axis("off")
    axes.flat[0].legend(fontsize=8); fig.suptitle(title)
    fig.supxlabel("Target week"); fig.supylabel("Flu rate per 100,000")
    fig.tight_layout(); fig.savefig(path, dpi=160, bbox_inches="tight"); plt.close(fig)


def run_variant(all_rates: pd.DataFrame, variant: str, output_root: Path, epochs: int, batch_size: int) -> None:
    started = time.perf_counter(); rates = variant_data(all_rates, variant)
    positions = sample_positions(rates); train, val, test = split_positions(rates, positions)
    train_rows = rates.iloc[:train[-1] + max(HORIZONS) + 1].to_numpy(dtype=np.float32)
    mean, std = train_rows.mean(axis=0, keepdims=True), train_rows.std(axis=0, keepdims=True) + 1e-8
    x_train, y_train = arrays(rates, train, mean, std); x_val, y_val = arrays(rates, val, mean, std)
    x_test, _ = arrays(rates, test, mean, std)
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'=' * 72}\nLSTM | {variant} | device={device}\n{'=' * 72}")
    print(f"Train: {len(train)} | Validation: {len(val)} | Test: {len(test)}")
    model, best_epoch, best_loss = train_model(x_train, y_train, x_val, y_val, device, epochs, batch_size)
    model.eval()
    with torch.no_grad(): normalized_pred = model(torch.from_numpy(x_test).to(device)).cpu().numpy()
    predicted = np.maximum(0.0, normalized_pred * std[:, None, :] + mean[:, None, :])
    records = []
    for sample_idx, t in enumerate(test):
        for h_idx, horizon in enumerate(HORIZONS):
            target_date = rates.index[t + horizon]
            for node, neighborhood in enumerate(NEIGHBORHOODS):
                actual, pred = float(rates.iloc[t + horizon, node]), float(predicted[sample_idx, h_idx, node])
                records.append({"origin_date": rates.index[t], "target_date": target_date, "horizon": horizon,
                                "neighborhood": neighborhood, "actual": actual, "predicted": pred, "error": pred - actual})
    predictions = pd.DataFrame(records).sort_values(["horizon", "target_date", "neighborhood"])
    metrics = build_metrics(predictions); out = output_root / "lstm" / variant; out.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(out / "predictions.csv", index=False); metrics.to_csv(out / "metrics.csv", index=False)
    save_plot(predictions, out / "actual_vs_predicted_horizon1.png", f"LSTM ({variant}) — horizon 1")
    summary = metrics.loc[metrics.scope.isin(["macro", "pooled"]), ["scope", "horizon", "RMSE", "MAE", "MAPE", "Corr"]]
    print(f"Best epoch: {best_epoch} | validation MSE: {best_loss:.6f}")
    print("\nPrimary comparison and horizon summary:\n" + summary.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"Runtime: {time.perf_counter() - started:.1f}s\nOutputs: {out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["all", "exclude_covid", "post_covid"], default="all")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1: parser.error("--epochs and --batch-size must be positive")
    return args


def main() -> None:
    args = parse_args(); rates = load_rates()
    variants = ("exclude_covid", "post_covid") if args.variant == "all" else (args.variant,)
    print(f"Loaded {len(rates)} weekly dates and {rates.shape[1]} neighborhoods from {DATA_FILE}")
    for variant in variants: run_variant(rates, variant, args.output_dir.resolve(), args.epochs, args.batch_size)


if __name__ == "__main__": main()
