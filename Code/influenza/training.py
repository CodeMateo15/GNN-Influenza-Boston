"""Training loop, MC-Dropout inference and predictive-interval calibration."""

from __future__ import annotations

import copy
import os
import random
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn.functional as F

from .config import TrainSpec
from .samples import Normalization, Samples

Z95 = 1.959964


def seed_everything(seed: int) -> None:
    """Seed immediately before model construction, and pin everything else.

    The notebooks seeded ~30 cells before building the model, so any change in
    the intervening pandas or matplotlib work shifted the weight initialisation.
    Seeding at the point of use makes a run reproducible from its recorded seed.

    Seeding alone is not enough. At this model size torch's intra-op threading is
    pure overhead, and multithreaded reductions sum in a nondeterministic order,
    so two runs of the same seed on the same machine under different load could
    disagree -- and because early stopping compares validation losses, a float
    tie broken differently selects a different epoch and therefore a different
    model. Pinning to one thread makes the recorded seed an actual guarantee and
    is faster here besides.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def masked_mse(prediction: torch.Tensor, target: torch.Tensor,
               weights: torch.Tensor | None = None) -> torch.Tensor:
    """MSE over observed cells only; NaN targets are suppressed BPHC weeks.

    `weights` is optional and normalised to mean 1 over the observed cells, so
    the default call is unchanged. Model selection always calls this without
    weights -- see the epoch loop -- so a weighted training loss never decides
    which checkpoint is kept.
    """
    observed = torch.isfinite(target)
    if not bool(observed.any()):
        return prediction.sum() * 0.0
    squared = (prediction[observed] - target[observed]) ** 2
    if weights is None:
        return squared.mean()
    w = weights[observed]
    return (squared * w).sum() / w.sum().clamp_min(1e-8)


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
    two_sided: bool = False,
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
                             epistemic=val_epistemic.ravel(), two_sided=two_sided)
    else:
        model = IntervalModel(fitted=False, note="no validation split available")

    lower, upper = model.bounds(mean.ravel(), horizon_grid.ravel(), epistemic=epistemic.ravel())
    return (
        Prediction(mean=mean, lower=lower.reshape(mean.shape),
                   upper=upper.reshape(mean.shape), actual=np.empty(0)),
        model,
    )


# ---------------------------------------------------------------------------
# SpatioTemporalGNN training
# ---------------------------------------------------------------------------

def masked_huber(prediction: torch.Tensor, target: torch.Tensor,
                 delta: float = 1.0, weights: torch.Tensor | None = None
                 ) -> torch.Tensor:
    """Huber over observed cells only. NaN targets are suppressed weeks.

    `weights` is an optional per-cell weight, normalised to mean 1 over the
    observed cells so that changing it does not also change the effective
    learning rate. Passing None is the unweighted mean, byte-identical to
    `F.huber_loss`'s own reduction.
    """
    observed = torch.isfinite(target)
    if not bool(observed.any()):
        return prediction.sum() * 0.0
    if weights is None:
        return F.huber_loss(prediction[observed], target[observed], delta=delta)
    per_cell = F.huber_loss(prediction[observed], target[observed],
                            delta=delta, reduction="none")
    w = weights[observed]
    return (per_cell * w).sum() / w.sum().clamp_min(1e-8)


def slope_weights(move: torch.Tensor, target: torch.Tensor,
                  strength: float) -> torch.Tensor | None:
    """Per-cell weight rising with how far the epidemic moved over the horizon.

    A squared-error loss has no term for timing, so when the turn date is
    uncertain the risk-minimising forecast is a smoothed, slightly late peak:
    being late is the cheap hedge. This makes it less cheap, by giving the cells
    where the curve actually moved more say than the cells where it stood still.

        w = 1 + strength * |move| / mean(|move|)

    `move` is the change from the origin level to the target week -- the quantity
    the network is really being asked for. Scaled by its own mean over the
    observed cells of the batch, so `strength` means "how many times more weight
    does an average-sized move get than a stationary week", independent of
    normalisation. Returns None at strength 0 so the unweighted path is taken
    rather than multiplied by a tensor of ones.
    """
    if strength <= 0:
        return None
    observed = torch.isfinite(target)
    magnitude = move.abs()
    scale = magnitude[observed].mean().clamp_min(1e-8) if bool(observed.any()) else 1.0
    return 1.0 + strength * magnitude / scale


def soft_pearson(prediction: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    """1 - Pearson r over the observed cells of a batch. Differentiable.

    Corr is one of the four reported CORE_METRICS, so training toward it is
    metric-aligned rather than a trick -- but two guard rails make that claim
    honest, and both are enforced elsewhere: RMSE / MAE / MAPE come from the same
    predictions and are reported unchanged, and model selection on the validation
    split stays plain masked MSE, so the restored checkpoint is never
    Pearson-selected. What this term actually buys is variance, not mean: it moves
    single-seed macro Corr at h=2 by about +0.03 while barely moving the ensemble.
    """
    observed = torch.isfinite(target)
    if int(observed.sum()) < 3:
        return prediction.sum() * 0.0
    p = prediction[observed]
    y = target[observed]
    p = p - p.mean()
    y = y - y.mean()
    denominator = p.norm() * y.norm() + 1e-8
    return 1.0 - (p * y).sum() / denominator


def composite_loss(prediction: torch.Tensor, target: torch.Tensor, *,
                   huber_delta: float = 0.0,
                   pearson_weight: float = 0.0,
                   weights: torch.Tensor | None = None) -> torch.Tensor:
    """Point loss plus an optional correlation term.

    `weights` applies only to the point term. The correlation term is a single
    scalar over the whole batch and has no per-cell decomposition to weight.
    """
    if huber_delta <= 0:
        point = masked_mse(prediction, target, weights=weights)
    else:
        point = masked_huber(prediction, target, delta=huber_delta, weights=weights)
    if pearson_weight <= 0:
        return point
    return point + pearson_weight * soft_pearson(prediction, target)


def _stgnn_tensors(samples: Samples, device: torch.device) -> list[tuple]:
    """(X, g, y, anchor, clim, trend) per sample. clim/trend are None when unused."""
    out = []
    for i in range(len(samples.positions)):
        clim = (None if samples.clim is None
                else torch.from_numpy(samples.clim[i]).to(device))
        trend = (None if samples.trend is None
                 else torch.from_numpy(samples.trend[i]).to(device))
        out.append((
            torch.from_numpy(samples.X[i]).to(device),
            torch.from_numpy(samples.g[i]).to(device),
            torch.from_numpy(samples.y[i]).to(device),
            torch.from_numpy(samples.anchors[i]).to(device),
            clim,
            trend,
        ))
    return out


def train_stgnn(
    model: torch.nn.Module,
    train: Samples,
    val: Samples,
    *,
    relations: list[tuple],
    spec: TrainSpec,
    device: torch.device,
    n_neigh: int,
    blended: bool,
    target_kind: str = "blend",
    verbose: bool = True,
) -> TrainResult:
    """Mini-batch training for SpatioTemporalGNN.

    Kept separate from `train_gcn` rather than overloaded: the forward signatures
    differ, `run_dualtopo.py` imports `masked_mse` from here, and the legacy arms
    must keep reproducing byte-for-byte.

    Two departures from `train_gcn`, both fixing measured underfitting. The old
    loop did per-sample updates and early-stopped at epoch 4 of 29 on the
    superseded gcn_fusion arms; mini-batches of 16 plus cosine annealing over a
    fixed epoch budget let the model actually train. Early stopping is therefore disabled by
    default for this path (`early_stop_patience` very large) while best-state
    restore is kept, so the selected weights are still the best validation epoch
    rather than the last one.
    """
    if spec.optimizer == "adamw":
        optimizer = torch.optim.AdamW(model.parameters(), lr=spec.lr,
                                      weight_decay=spec.weight_decay)
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=spec.lr,
                                     weight_decay=spec.weight_decay)
    if spec.schedule == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=spec.epochs)
        step_on_val = False
    else:
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, patience=spec.plateau_patience, factor=spec.plateau_factor)
        step_on_val = True

    relations = [(name, index.to(device), weight.to(device))
                 for name, index, weight in relations]
    tensors = _stgnn_tensors(train, device)
    val_tensors = _stgnn_tensors(val, device)
    batch_size = spec.batch_size or 16

    def run_batch(rows: list[int], grad: bool):
        predictions, targets, moves = [], [], []
        for idx in rows:
            X, g, y, anchor, clim, trend = tensors[idx] if grad else val_tensors[idx]
            kwargs = dict(anchor=anchor, clim=clim) if blended else {}
            if kwargs and target_kind == "trendblend":
                kwargs["trend"] = trend
            out = model(X, relations, g, **kwargs)
            predictions.append(out[:n_neigh])
            targets.append(y)
            # How far the epidemic moved from the origin week to the target
            # week. For the `delta` parameterisation the label already IS that
            # move; for `blend` and `level` it is the label minus the origin.
            moves.append(y if target_kind == "delta" else y - anchor.unsqueeze(1))
        return (torch.cat(predictions, dim=0), torch.cat(targets, dim=0),
                torch.cat(moves, dim=0))

    train_losses: list[float] = []
    val_losses: list[float] = []
    best_val, best_state, best_epoch, patience = np.inf, None, 0, 0
    epoch = 0

    for epoch in range(1, spec.epochs + 1):
        model.train()
        order = np.random.permutation(len(tensors))
        total, n_batches = 0.0, 0
        for start in range(0, len(order), batch_size):
            rows = [int(i) for i in order[start:start + batch_size]]
            optimizer.zero_grad()
            prediction, target, move = run_batch(rows, grad=True)
            loss = composite_loss(prediction, target, huber_delta=spec.huber_delta,
                                  pearson_weight=spec.pearson_weight,
                                  weights=slope_weights(move, target, spec.slope_weight))
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=spec.grad_clip)
            optimizer.step()
            total += float(loss.item())
            n_batches += 1
        train_losses.append(total / max(n_batches, 1))

        # Model selection stays on plain masked MSE even when the training loss
        # carries a correlation term, so the checkpoint is not Pearson-selected.
        model.eval()
        with torch.no_grad():
            prediction, target, _ = run_batch(list(range(len(val_tensors))), grad=False)
            val_losses.append(float(masked_mse(prediction, target).item()))
        scheduler.step(val_losses[-1]) if step_on_val else scheduler.step()

        if val_losses[-1] < best_val:
            best_val, best_epoch = val_losses[-1], epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            patience = 0
        else:
            patience += 1

        if verbose and (epoch == 1 or epoch % 25 == 0):
            print(f"Epoch {epoch:3d} | train {train_losses[-1]:.6f} | "
                  f"val MSE {val_losses[-1]:.6f} | lr {optimizer.param_groups[0]['lr']:.6f}")
        if patience >= spec.early_stop_patience:
            if verbose:
                print(f"Early stopping at epoch {epoch}")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
    return TrainResult(best_epoch=best_epoch, best_val_loss=float(best_val),
                       train_losses=train_losses, val_losses=val_losses, epochs_run=epoch)


def mc_dropout_stgnn(
    model: torch.nn.Module,
    samples: Samples,
    *,
    relations: list[tuple],
    norm: Normalization,
    n_neigh: int,
    device: torch.device,
    n_mc: int,
    target: str,
) -> tuple[np.ndarray, np.ndarray]:
    """MC-Dropout draws for SpatioTemporalGNN, in rate units.

    `blend` and `trendblend` need no post-hoc reconstruction: the model already
    added its learned baseline inside forward, so the output is a level exactly
    like `level`. Only `delta` still has to be re-anchored here.
    """
    relations = [(name, index.to(device), weight.to(device))
                 for name, index, weight in relations]
    tensors = _stgnn_tensors(samples, device)
    anchors = samples.anchors[:, :, None]
    blended = target in ("blend", "trendblend", "cascade")

    model.train()
    draws: list[np.ndarray] = []
    with torch.no_grad():
        for _ in range(n_mc):
            per_sample = []
            for X, g, _y, anchor, clim, trend in tensors:
                kwargs = dict(anchor=anchor, clim=clim) if blended else {}
                if kwargs and target == "trendblend":
                    kwargs["trend"] = trend
                per_sample.append(model(X, relations, g, **kwargs)[:n_neigh].cpu().numpy())
            draws.append(np.stack(per_sample, axis=0))
    model.eval()

    normalized = np.stack(draws, axis=0)
    if target == "delta":
        normalized = normalized + anchors[None]
        actual_norm = samples.y + anchors
    else:
        actual_norm = samples.y

    return (norm.to_level(normalized.reshape(-1, *normalized.shape[2:])).reshape(normalized.shape),
            norm.to_level(actual_norm))
