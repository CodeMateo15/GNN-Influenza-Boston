"""Multivariate LSTM baseline for weekly Boston neighborhood influenza rates.

All 14 neighborhoods enter as one input vector, so the model can use
cross-neighborhood information but has no graph structure to guide it -- which
is the point of comparing it against the GNNs.

    python Code/run_lstm.py --variant post_covid

The defaults reproduce the committed leaderboard run: one seed, an 8-week
window, a plain level target. The parity arm gives the LSTM what `gnn_st` gets
apart from the graph and the covariates -- the same 16-week window, the same
seasonal blend target, the same ten-seed ensemble:

    python Code/run_lstm.py --variant post_covid --lookback 16 --target blend --n-seeds 10
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
from influenza.climatology import fit_climatology
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals

MODEL = "lstm"
HIDDEN_SIZE = 64
PATIENCE = 25


class MultivariateLSTM(nn.Module):
    def __init__(self, n_inputs: int, n_horizons: int, hidden_size: int = HIDDEN_SIZE,
                 dropout: float = 0.0, blend_init: tuple[float, ...] | None = None) -> None:
        super().__init__()
        self.n_inputs = n_inputs
        self.n_horizons = n_horizons
        self.lstm = nn.LSTM(input_size=n_inputs, hidden_size=hidden_size, batch_first=True)
        # Identity at 0 rather than Dropout(0.0), so the default path draws no
        # random numbers and reproduces the committed run bit for bit.
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()
        self.output = nn.Linear(hidden_size, n_inputs * n_horizons)
        # The same blend head as models.SpatioTemporalGNN: one sigmoid share per
        # horizon between the origin level and the seasonal curve, with the
        # network predicting the residual. None keeps the plain level target.
        self.blend_logit = (None if blend_init is None else
                            nn.Parameter(torch.tensor(blend_init, dtype=torch.float32)))

    def forward(self, x: torch.Tensor, clim: torch.Tensor | None = None) -> torch.Tensor:
        encoded, _ = self.lstm(x)
        out = self.output(self.dropout(encoded[:, -1])).view(-1, self.n_horizons, self.n_inputs)
        if self.blend_logit is None:
            return out
        share = torch.sigmoid(self.blend_logit)[None, :, None]
        origin = x[:, -1, :][:, None, :]
        return share * origin + (1.0 - share) * clim + out


def arrays(features: pd.DataFrame, targets: pd.DataFrame, positions: list[int], mean, std,
           window: Window, clim_rate: np.ndarray | None = None):
    """Sliding-window tensors of normalized rates, plus the normalized seasonal curve.

    `features` is causally imputed so inputs are finite; `targets` keeps NaN for
    suppressed weeks so the loss can mask them instead of learning fake zeros.
    `clim_rate` is (weeks, nodes) in rate units; its values at each target week
    come back normalized like the targets, or as zeros when it is None.
    """
    x_source = (features.to_numpy(dtype=np.float32) - mean) / std
    y_source = (targets.to_numpy(dtype=np.float32) - mean) / std
    x = np.stack([x_source[t - window.lookback + 1 : t + 1] for t in positions]).astype(np.float32)
    y = np.stack([
        np.stack([y_source[t + h] for h in window.horizons]) for t in positions
    ]).astype(np.float32)
    if clim_rate is None:
        clim = np.zeros_like(y)
    else:
        c_source = (clim_rate.astype(np.float32) - mean) / std
        clim = np.stack([
            np.stack([c_source[t + h] for h in window.horizons]) for t in positions
        ]).astype(np.float32)
    return x, y, clim


def masked_mse(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """MSE over observed cells only. NaN targets are suppressed BPHC weeks."""
    observed = torch.isfinite(target)
    if not bool(observed.any()):
        return prediction.sum() * 0.0
    diff = (prediction[observed] - target[observed]) ** 2
    return diff.mean()


def train_model(train, val, device, args, window, n_series, seed, blend_init):
    # n_series is the city's scored-node count: the LSTM takes all of them as one
    # input vector, so it is 14 for Boston and 17 for Columbus.
    x_train, y_train, c_train = train
    x_val, y_val, c_val = val
    epochs, batch_size = args.epochs, args.batch_size
    model = MultivariateLSTM(n_series, len(window.horizons), hidden_size=args.hidden_size,
                             dropout=args.dropout, blend_init=blend_init).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    criterion = masked_mse
    generator = torch.Generator().manual_seed(seed)
    loader = DataLoader(
        TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train),
                      torch.from_numpy(c_train)),
        batch_size=batch_size, shuffle=True, generator=generator,
    )
    val_x = torch.from_numpy(x_val).to(device)
    val_y = torch.from_numpy(y_val).to(device)
    val_c = torch.from_numpy(c_val).to(device)

    best_state, best_loss, best_epoch, patience = None, np.inf, 0, 0
    train_history: list[float] = []
    val_history: list[float] = []
    for epoch in range(1, epochs + 1):
        model.train()
        epoch_loss = 0.0
        for xb, yb, cb in loader:
            xb, yb, cb = xb.to(device), yb.to(device), cb.to(device)
            optimizer.zero_grad()
            loss = criterion(model(xb, cb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            epoch_loss += float(loss.item()) * len(xb)
        model.eval()
        with torch.no_grad():
            val_loss = float(criterion(model(val_x, val_c), val_y).item())
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


def _blend_init(horizons) -> tuple[float, ...]:
    """The same starting logits as run_gnn._blend_init, so both begin from one prior."""
    scale = {1: 2.5, 2: 1.5, 3: 0.8, 4: 0.0}
    return tuple(scale.get(int(h), -1.5) for h in horizons)


def _blend_shares(model: MultivariateLSTM) -> list[float]:
    """Learned origin-level share per horizon, from the last seed."""
    return torch.sigmoid(model.blend_logit.detach()).cpu().tolist()


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
    clim_rate, climatology = None, None
    if args.target == "blend":
        # Train-only, with the same cutoff as xgboost and gnn_st: the fit sees
        # exactly the weeks the training targets already revealed.
        climatology = fit_climatology(rates, end=split.train[-1] + window.max_horizon + 1)
        clim_rate = climatology.level(rates.index)
    train = arrays(features, rates, split.train, mean, std, window, clim_rate)
    val = arrays(features, rates, split.val, mean, std, window, clim_rate)
    x_test, _, c_test = arrays(features, rates, split.test, mean, std, window, clim_rate)
    x_val, c_val = val[0], val[2]
    blend_init = _blend_init(window.horizons) if args.target == "blend" else None
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'=' * 72}\nLSTM | {variant} | device={device}\n{'=' * 72}")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    print(f"Target: {args.target} | lookback {window.lookback} | seeds {args.n_seeds}")
    first_target, last_target = split.test_target_span()
    print(f"Test targets: {first_target.date()} -> {last_target.date()}")

    # Tracking wraps only the modelling work, so the measured energy is training
    # and inference rather than CSV writing. It must also close before
    # finish_run, which serialises the emissions summary.
    seeds = [SEED + i for i in range(args.n_seeds)]
    print(f"Budget: {args.epochs} epochs x {len(seeds)} seeds", flush=True)
    per_seed: list[dict] = []
    test_draws, val_draws = [], []
    with track_emissions(run_tag(args.name, variant, window), enabled=not args.no_carbon,
                         city=city.name) as carbon:
        for i, seed in enumerate(seeds, start=1):
            print(f"--- seed {seed} ({i}/{len(seeds)}) ---", flush=True)
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
            with carbon.phase("train"):
                model, best_epoch, best_loss, train_history, val_history = train_model(
                    train, val, device, args, window, city.n_neigh, seed, blend_init,
                )
            carbon.add_epochs(len(train_history))
            model.eval()
            with carbon.phase("eval"), torch.no_grad():
                normalized_pred = model(torch.from_numpy(x_test).to(device),
                                        torch.from_numpy(c_test).to(device)).cpu().numpy()
                normalized_val = model(torch.from_numpy(x_val).to(device),
                                       torch.from_numpy(c_val).to(device)).cpu().numpy()
            test_draws.append(normalized_pred * std[:, None, :] + mean[:, None, :])
            val_draws.append(normalized_val * std[:, None, :] + mean[:, None, :])
            per_seed.append({"seed": seed, "best_epoch": best_epoch, "best_val_mse": best_loss})
        # The ensemble is the mean over seeds, as for gnn_st, clipped at zero
        # after averaging so a single seed's negative draw cannot bias it upward.
        predicted = np.maximum(0.0, np.mean(test_draws, axis=0))
        val_predicted = np.maximum(0.0, np.mean(val_draws, axis=0))
    best_epoch = int(np.median([r["best_epoch"] for r in per_seed]))
    best_loss = float(np.mean([r["best_val_mse"] for r in per_seed]))

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
                    "origin_date": split.index[position],
                    "target_date": target_date,
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": float(rates.at[target_date, neighborhood]),
                    "predicted": float(val_predicted[sample_idx, h_idx, node]),
                })
    validation = pd.DataFrame(val_rows)

    print(f"Best epoch: {best_epoch} | validation MSE: {best_loss:.6f}")

    checkpoint_path = checkpoint_root / f"{args.name}_{variant}.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "flu_means": mean,
        "flu_stds": std,
        "neighborhoods": list(city.node_names),
        "horizons": list(window.horizons),
        "lookback": window.lookback,
        "hidden_size": args.hidden_size,
        "target": args.target,
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
        model=args.name,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": args.target,
            "normalize": "train",
            "window": window.to_json(),
            "split": split.to_json(),
            "hidden_size": args.hidden_size,
            "dropout": args.dropout,
            "lr": args.lr,
            "weight_decay": args.weight_decay,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "seed": SEED,
            "n_seeds": len(seeds),
            "seeds": seeds,
            "per_seed": per_seed,
            **({"climatology": climatology.to_json(),
                "blend_share": _blend_shares(model)} if climatology is not None else {}),
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
        # Held-out forecasts for tune.py, which selects on validation only.
        extra_tables={"predictions_val": validation},
    )
    save_loss_curve(train_history, val_history, out / "loss_curve.png",
                    title=f"LSTM ({variant}) training, last seed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    parser.add_argument("--name", default=MODEL,
                        help="Results directory name, so a parity arm does not overwrite "
                             "the committed lstm run.")
    parser.add_argument("--epochs", type=int, default=120)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--hidden-size", type=int, default=HIDDEN_SIZE)
    parser.add_argument("--dropout", type=float, default=0.0)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--target", choices=("level", "blend"), default="level",
                        help="'blend' predicts a residual from the same origin/seasonal "
                             "blend gnn_st uses, so the two differ only in architecture.")
    parser.add_argument("--n-seeds", type=int, default=1,
                        help="Ensemble size. gnn_st uses 10; 1 reproduces the committed run.")
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1 or args.n_seeds < 1:
        parser.error("--epochs, --batch-size and --n-seeds must be positive")
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
