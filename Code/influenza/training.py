"""Training loop, MC-Dropout inference and predictive-interval calibration."""

from __future__ import annotations

import copy
import random
from dataclasses import dataclass

import numpy as np
import torch

from .config import TrainSpec
from .samples import Normalization, Samples

Z95 = 1.959964


def seed_everything(seed: int) -> None:
    """Seed immediately before model construction.

    The notebooks seeded ~30 cells before building the model, so any change in
    the intervening pandas or matplotlib work shifted the weight initialisation.
    Seeding at the point of use makes a run reproducible from its recorded seed.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def masked_mse(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """MSE over observed cells only; NaN targets are suppressed BPHC weeks."""
    observed = torch.isfinite(target)
    if not bool(observed.any()):
        return prediction.sum() * 0.0
    return ((prediction[observed] - target[observed]) ** 2).mean()


@dataclass
class TrainResult:
    best_epoch: int
    best_val_loss: float
    train_losses: list[float]
    val_losses: list[float]
    epochs_run: int


def train_gcn(
    model: torch.nn.Module,
    train: Samples,
    val: Samples,
    *,
    edge_index: torch.Tensor,
    edge_weight: torch.Tensor,
    spec: TrainSpec,
    device: torch.device,
    n_neigh: int,
    verbose: bool = True,
) -> TrainResult:
    """Per-sample training over the full graph, matching the notebook loop."""
    optimizer = torch.optim.Adam(model.parameters(), lr=spec.lr, weight_decay=spec.weight_decay)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, patience=spec.plateau_patience, factor=spec.plateau_factor
    )
    edge_index = edge_index.to(device)
    edge_weight = edge_weight.to(device)

    tensors = _to_tensors(train, device)
    val_tensors = _to_tensors(val, device)

    train_losses: list[float] = []
    val_losses: list[float] = []
    best_val, best_state, best_epoch, patience = np.inf, None, 0, 0
    epoch = 0

    for epoch in range(1, spec.epochs + 1):
        model.train()
        total = 0.0
        for idx in np.random.permutation(len(tensors)):
            X, g, y = tensors[idx]
            optimizer.zero_grad()
            prediction = model(X, edge_index, g, edge_weight)
            loss = masked_mse(prediction[:n_neigh], y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=spec.grad_clip)
            optimizer.step()
            total += float(loss.item())
        train_losses.append(total / max(len(tensors), 1))

        model.eval()
        with torch.no_grad():
            val_total = sum(
                float(masked_mse(model(X, edge_index, g, edge_weight)[:n_neigh], y).item())
                for X, g, y in val_tensors
            )
        val_losses.append(val_total / max(len(val_tensors), 1))
        scheduler.step(val_losses[-1])

        if val_losses[-1] < best_val:
            best_val, best_epoch = val_losses[-1], epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            patience = 0
        else:
            patience += 1

        if verbose and (epoch == 1 or epoch % 10 == 0):
            print(f"Epoch {epoch:3d} | train MSE {train_losses[-1]:.6f} | "
                  f"val MSE {val_losses[-1]:.6f} | lr {optimizer.param_groups[0]['lr']:.6f}")
        if patience >= spec.early_stop_patience:
            if verbose:
                print(f"Early stopping at epoch {epoch}")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return TrainResult(best_epoch=best_epoch, best_val_loss=float(best_val),
                       train_losses=train_losses, val_losses=val_losses, epochs_run=epoch)


def _to_tensors(samples: Samples, device: torch.device) -> list[tuple]:
    return [
        (
            torch.from_numpy(samples.X[i]).to(device),
            torch.from_numpy(samples.g[i]).to(device),
            torch.from_numpy(samples.y[i]).to(device),
        )
        for i in range(len(samples.positions))
    ]


# ---------------------------------------------------------------------------
# MC-Dropout inference with calibrated predictive intervals
# ---------------------------------------------------------------------------

@dataclass
class Prediction:
    mean: np.ndarray     # (S, n_neigh, n_horizons) in rate units
    lower: np.ndarray
    upper: np.ndarray
    actual: np.ndarray   # NaN where suppressed


def mc_dropout_forward(
    model: torch.nn.Module,
    samples: Samples,
    *,
    edge_index: torch.Tensor,
    edge_weight: torch.Tensor,
    norm: Normalization,
    n_neigh: int,
    device: torch.device,
    n_mc: int,
    target: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (mc_draws, actual) in rate units.

    mc_draws has shape (n_mc, S, n_neigh, n_horizons). model.train() enables
    dropout only -- the model has no BatchNorm and no nn.Dropout submodules.
    """
    edge_index = edge_index.to(device)
    edge_weight = edge_weight.to(device)
    tensors = _to_tensors(samples, device)
    anchors = samples.anchors[:, :, None]

    model.train()
    draws: list[np.ndarray] = []
    with torch.no_grad():
        for _ in range(n_mc):
            per_sample = [
                model(X, edge_index, g, edge_weight)[:n_neigh].cpu().numpy()
                for X, g, _ in tensors
            ]
            draws.append(np.stack(per_sample, axis=0))
    model.eval()

    normalized = np.stack(draws, axis=0)
    if target == "delta":
        normalized = normalized + anchors[None]
        actual_norm = samples.y + anchors
    else:
        actual_norm = samples.y

    return norm.to_level(normalized.reshape(-1, *normalized.shape[2:])).reshape(normalized.shape), \
        norm.to_level(actual_norm)


def calibrate_intervals(
    test_draws: np.ndarray,
    val_draws: np.ndarray | None,
    val_actual: np.ndarray | None,
    horizons: tuple[int, ...],
) -> tuple[Prediction, "IntervalModel"]:
    """95% predictive intervals from MC spread plus level-dependent noise.

    Uses the shared recipe in influenza.intervals -- the same one every baseline
    uses -- so the bands are comparable across models. The only difference here
    is that MC-Dropout supplies an epistemic variance term, which widens the band
    where the model itself is uncertain. MC-Dropout alone captures only that
    epistemic component and badly under-covers, hence the residual term.
    """
    from .intervals import IntervalModel, fit_intervals

    mean = test_draws.mean(axis=0)
    epistemic = test_draws.var(axis=0)
    horizon_grid = np.broadcast_to(np.asarray(horizons), mean.shape)

    if val_draws is not None and val_actual is not None and val_draws.shape[1] > 1:
        val_mean = val_draws.mean(axis=0)
        val_epistemic = val_draws.var(axis=0)
        val_horizon = np.broadcast_to(np.asarray(horizons), val_mean.shape)
        model = fit_intervals(val_mean.ravel(), val_actual.ravel(), val_horizon.ravel(),
                             epistemic=val_epistemic.ravel())
    else:
        model = IntervalModel(fitted=False, note="no validation split available")

    lower, upper = model.bounds(mean.ravel(), horizon_grid.ravel(), epistemic=epistemic.ravel())
    return (
        Prediction(mean=mean, lower=lower.reshape(mean.shape),
                   upper=upper.reshape(mean.shape), actual=np.empty(0)),
        model,
    )
