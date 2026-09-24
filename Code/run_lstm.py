"""Multivariate LSTM baseline for weekly Boston neighborhood influenza rates.

All 14 neighborhoods enter as one input vector, so the model can use
cross-neighborhood information but has no graph structure to guide it -- which
is the point of comparing it against the GNNs.

    python Code/run_lstm.py --variant post_covid
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import copy
import random

try:
    import numpy as np
    import pandas as pd
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib torch."
    ) from exc

from influenza import (
    SEED,
    impute_causal,
    Window,
    finish_run,
    normalization,
    paths,
    save_loss_curve,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_variants, resolve_window, run_tag)
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals

MODEL = "lstm"
HIDDEN_SIZE = 64
PATIENCE = 25


class MultivariateLSTM(nn.Module):
    def __init__(self, n_inputs: int, n_horizons: int, hidden_size: int = HIDDEN_SIZE) -> None:
        super().__init__()
        self.n_inputs = n_inputs
        self.n_horizons = n_horizons
        self.lstm = nn.LSTM(input_size=n_inputs, hidden_size=hidden_size, batch_first=True)
        self.output = nn.Linear(hidden_size, n_inputs * n_horizons)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded, _ = self.lstm(x)
        return self.output(encoded[:, -1]).view(-1, self.n_horizons, self.n_inputs)


def arrays(features: pd.DataFrame, targets: pd.DataFrame, positions: list[int], mean, std, window: Window):
    """Sliding-window tensors of normalized rates.

    `features` is causally imputed so inputs are finite; `targets` keeps NaN for
    suppressed weeks so the loss can mask them instead of learning fake zeros.
    """
    x_source = (features.to_numpy(dtype=np.float32) - mean) / std
    y_source = (targets.to_numpy(dtype=np.float32) - mean) / std
    x = np.stack([x_source[t - window.lookback + 1 : t + 1] for t in positions]).astype(np.float32)
    y = np.stack([
        np.stack([y_source[t + h] for h in window.horizons]) for t in positions
    ]).astype(np.float32)
    return x, y


def masked_mse(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """MSE over observed cells only. NaN targets are suppressed BPHC weeks."""
    observed = torch.isfinite(target)
    if not bool(observed.any()):
        return prediction.sum() * 0.0
    diff = (prediction[observed] - target[observed]) ** 2
    return diff.mean()


def train_model(x_train, y_train, x_val, y_val, device, epochs, batch_size, window,
                n_series):
    # n_series is the city's scored-node count: the LSTM takes all of them as one
    # input vector, so it is 14 for Boston and 17 for Columbus.
    model = MultivariateLSTM(n_series, len(window.horizons)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    criterion = masked_mse
    generator = torch.Generator().manual_seed(SEED)
    loader = DataLoader(
        TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
        batch_size=batch_size, shuffle=True, generator=generator,
    )
    val_x = torch.from_numpy(x_val).to(device)
    val_y = torch.from_numpy(y_val).to(device)

    best_state, best_loss, best_epoch, patience = None, np.inf, 0, 0
    train_history: list[float] = []
    val_history: list[float] = []
    for epoch in range(1, epochs + 1):
        model.train()
        epoch_loss = 0.0
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            epoch_loss += float(loss.item()) * len(xb)
        model.eval()
        with torch.no_grad():
            val_loss = float(criterion(model(val_x), val_y).item())
        train_history.append(epoch_loss / len(x_train))
        val_history.append(val_loss)

        if val_loss < best_loss - 1e-7:
            best_loss, best_epoch = val_loss, epoch
            best_state = copy.deepcopy(model.state_dict())
            patience = 0
        else:
            patience += 1
        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:3d} | validation MSE {val_loss:.6f}")
        if patience >= PATIENCE:
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_epoch, best_loss, train_history, val_history


def run_variant(all_rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, checkpoint_root = city_output_dirs(args, city)
    data = variant_data(all_rates, variant)
    rates = data.available
    origins = valid_origins(rates.index, window)
    split = split_origins(rates.index, origins, window)

    features, imputed = impute_causal(rates)
    print(f"Causally imputed {int(imputed.to_numpy().sum())} of "
          f"{imputed.size} feature cells (suppressed neighborhood-weeks).")

    mean, std = normalization(rates, split, mode="train")
    x_train, y_train = arrays(features, rates, split.train, mean, std, window)
    x_val, y_val = arrays(features, rates, split.val, mean, std, window)
    x_test, _ = arrays(features, rates, split.test, mean, std, window)

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'=' * 72}\nLSTM | {variant} | device={device}\n{'=' * 72}")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    first_target, last_target = split.test_target_span()
    print(f"Test targets: {first_target.date()} -> {last_target.date()}")

    # Tracking wraps only the modelling work, so the measured energy is training
    # and inference rather than CSV writing. It must also close before
    # finish_run, which serialises the emissions summary.
    with track_emissions(run_tag(MODEL, variant, window), enabled=not args.no_carbon) as carbon:
        model, best_epoch, best_loss, train_history, val_history = train_model(
            x_train, y_train, x_val, y_val, device, args.epochs, args.batch_size, window,
            city.n_neigh,
        )
        model.eval()
        with torch.no_grad():
            normalized_pred = model(torch.from_numpy(x_test).to(device)).cpu().numpy()
            normalized_val = model(torch.from_numpy(x_val).to(device)).cpu().numpy()
        predicted = np.maximum(0.0, normalized_pred * std[:, None, :] + mean[:, None, :])
        val_predicted = np.maximum(0.0, normalized_val * std[:, None, :] + mean[:, None, :])

    records: list[dict] = []
    for sample_idx, position in enumerate(split.test):
        for h_idx, horizon in enumerate(window.horizons):
            target_date = split.index[position + horizon]
            for node, neighborhood in enumerate(city.node_names):
                actual = float(rates.iloc[position + horizon, node])
                pred = float(predicted[sample_idx, h_idx, node])
                records.append({
                    "origin_date": split.index[position],
                    "target_date": target_date,
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": actual,
                    "predicted": pred,
                    "error": pred - actual,
                })

    # Validation predictions in rate units, for the interval calibration.
    val_rows: list[dict] = []
    for sample_idx, position in enumerate(split.val):
        for h_idx, horizon in enumerate(window.horizons):
            target_date = split.index[position + horizon]
            for node, neighborhood in enumerate(city.node_names):
                val_rows.append({
                    "horizon": horizon,
                    "actual": float(rates.at[target_date, neighborhood]),
                    "predicted": float(val_predicted[sample_idx, h_idx, node]),
                })
    validation = pd.DataFrame(val_rows)

    print(f"Best epoch: {best_epoch} | validation MSE: {best_loss:.6f}")

    checkpoint_path = checkpoint_root / f"{MODEL}_{variant}.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "flu_means": mean,
        "flu_stds": std,
        "neighborhoods": list(city.node_names),
        "horizons": list(window.horizons),
        "lookback": window.lookback,
        "hidden_size": HIDDEN_SIZE,
        "best_epoch": best_epoch,
        "best_val_mse": best_loss,
    }, checkpoint_path)
    print(f"Checkpoint: {checkpoint_path}")

    interval_model = fit_intervals(validation["predicted"], validation["actual"],
                                   validation["horizon"],
                                   two_sided=args.two_sided_intervals)
    predictions = attach_intervals(pd.DataFrame(records), interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                 predictions["upper"])
    print(f"95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")

    out = finish_run(
        model=MODEL,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": "level",
            "normalize": "train",
            "window": window.to_json(),
            "split": split.to_json(),
            "hidden_size": HIDDEN_SIZE,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seed": SEED,
            "best_epoch": best_epoch,
            "best_val_mse": best_loss,
            "n_params": sum(p.numel() for p in model.parameters()),
            "imputed_feature_cells": int(imputed.to_numpy().sum()),
            "checkpoint": paths.display(checkpoint_path),
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
    )
    save_loss_curve(train_history, val_history, out / "loss_curve.png",
                    title=f"LSTM ({variant}) training")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        parser.error("--epochs and --batch-size must be positive")
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
