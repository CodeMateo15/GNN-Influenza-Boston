"""Dual-Topo-STGCN — the paper-faithful reference model.

Reimplements Luo et al. (2025), "A novel graph neural network based approach for
influenza-like illness nowcasting", BMC Public Health 25:408. Deliberately
minimal: ILI rates are the only feature, and the two topologies (geographic
adjacency and thresholded ILI correlation) feed two parallel pathways that are
fused before the readout.

    python Code/run_dualtopo.py
    python Code/run_dualtopo.py --experiment dualtopo_no_bg   # background-node ablation
    python Code/run_dualtopo.py --variant full                # more than 3 seasons of history

Unlike run_gnn.py this needs no torch_geometric: message passing is a dense
einsum against a pre-normalised adjacency.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import replace

try:
    import numpy as np
    import pandas as pd
    import torch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib torch."
    ) from exc

from influenza import (
    NEIGHBORHOODS,
    finish_run,
    load_rates,
    paths,
    save_loss_curve,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import add_common_args, resolve_window
from influenza.config import EXPERIMENTS, Experiment
from influenza.graphs import build_graph
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals
from influenza.models import DualTopoSTGCN
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.training import masked_mse, seed_everything


def to_sequence(samples, lookback: int) -> np.ndarray:
    """(S, n_nodes, lookback) feature rows -> (S, 1, n_nodes, lookback) in time order.

    build_samples emits lags most-recent-first (lag0 = the origin week), so the
    time axis is reversed here to run forward for the temporal convolutions.
    """
    if samples.X.shape[2] != lookback:
        raise ValueError(
            f"Expected exactly {lookback} features (the ILI lags) but got "
            f"{samples.X.shape[2]}. Dual-Topo-STGCN takes ILI rates only -- check "
            "that weather, demographics and global covariates are all off."
        )
    return samples.X[:, None, :, ::-1].copy()


def resolve_experiment(args: argparse.Namespace) -> Experiment:
    if args.experiment not in EXPERIMENTS:
        raise SystemExit(f"Unknown experiment {args.experiment!r}. "
                         f"Available: {', '.join(sorted(EXPERIMENTS))}")
    experiment = EXPERIMENTS[args.experiment]
    if experiment.model != "dualtopo":
        raise SystemExit(f"{args.experiment!r} is a {experiment.model} model. Use run_gnn.py.")

    graph_changes = {}
    if args.corr_threshold is not None:
        graph_changes["corr_threshold"] = args.corr_threshold
    if args.anchors is not None:
        graph_changes["anchors"] = args.anchors
    train_changes = {}
    if args.epochs is not None:
        train_changes["epochs"] = args.epochs
    if args.seed is not None:
        train_changes["seed"] = args.seed

    return replace(
        experiment,
        name=args.name or experiment.name,
        variant=args.variant if args.variant != "all" else experiment.variant,
        graph=replace(experiment.graph, **graph_changes) if graph_changes else experiment.graph,
        train=replace(experiment.train, **train_changes) if train_changes else experiment.train,
        window=resolve_window(args, experiment.window),
    )


def run(experiment: Experiment, args: argparse.Namespace) -> None:
    window = experiment.window
    data = variant_data(load_rates(), experiment.variant)
    dataset = load_dataset(experiment.features, rates=data.available)
    split = split_origins(dataset.week_index, valid_origins(dataset.week_index, window), window)

    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    graph = build_graph(experiment.graph, flu_history=history)
    if graph.W_corr is None:
        raise SystemExit("dualtopo requires GraphSpec(dual=True, corr=True).")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'=' * 72}\n{experiment.name} | {experiment.variant} | device={device}\n{'=' * 72}")
    print(f"{experiment.note}\n")
    print(f"Geographic topology: {graph.summary()}")
    print(f"Correlation topology: {int((np.triu(graph.W_corr, 1) > 0).sum())} undirected edges")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    print(f"Test targets: {split.index[split.test[0] + 1].date()} -> "
          f"{split.index[split.test[-1] + window.max_horizon].date()}")
    if len(split.train) < 100:
        print(f"  note: only {len(split.train)} training origins. A 52-week input window on "
              f"the {experiment.variant} slice is a much smaller data budget than the "
              f"paper's 364 samples; try --variant full for the whole series.")

    samples, norm = build_samples(dataset, split, experiment.features, window, graph,
                                  target=experiment.target, normalize=experiment.normalize)
    sequences = to_sequence(samples, window.lookback)

    a_geo = torch.tensor(graph.normalized(graph.W), dtype=torch.float32, device=device)
    a_corr = torch.tensor(graph.normalized(graph.W_corr), dtype=torch.float32, device=device)

    rows = {name: positions_to_rows(samples, getattr(split, name))
            for name in ("train", "val", "test")}
    tensors = {
        name: (torch.from_numpy(sequences[idx]).to(device),
               torch.from_numpy(samples.y[idx]).to(device))
        for name, idx in rows.items()
    }

    with track_emissions(f"{experiment.name}:{experiment.variant}",
                         enabled=not args.no_carbon) as carbon:
        seed_everything(experiment.train.seed)
        model = DualTopoSTGCN(
            n_nodes=graph.n_nodes,
            n_neigh=graph.n_neigh,
            input_window=window.lookback,
            spatial_channels=experiment.train.hidden[0],
            out_channels=experiment.train.hidden[1],
            n_horizons=len(window.horizons),
            fusion=args.fusion,
        ).to(device)
        print(f"Parameters: {sum(p.numel() for p in model.parameters()):,} | "
              f"time axis before readout: {model.time_out}")

        optimizer = torch.optim.Adam(model.parameters(), lr=experiment.train.lr,
                                     weight_decay=experiment.train.weight_decay)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=experiment.train.plateau_factor,
            patience=experiment.train.plateau_patience)

        batch_size = experiment.train.batch_size or 26
        x_train, y_train = tensors["train"]
        x_val, y_val = tensors["val"]
        train_losses, val_losses = [], []
        best_val, best_state, best_epoch, patience = np.inf, None, 0, 0
        epoch = 0

        for epoch in range(1, experiment.train.epochs + 1):
            model.train()
            order = torch.randperm(len(x_train), device=device)
            total = 0.0
            for start in range(0, len(order), batch_size):
                idx = order[start:start + batch_size]
                optimizer.zero_grad()
                prediction = model(x_train[idx], a_geo, a_corr)[:, :graph.n_neigh]
                loss = masked_mse(prediction, y_train[idx])
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), experiment.train.grad_clip)
                optimizer.step()
                total += float(loss.item()) * len(idx)
            train_losses.append(total / max(len(x_train), 1))

            model.eval()
            with torch.no_grad():
                val_loss = float(masked_mse(
                    model(x_val, a_geo, a_corr)[:, :graph.n_neigh], y_val).item())
            val_losses.append(val_loss)
            scheduler.step(val_loss)

            if val_loss < best_val:
                best_val, best_epoch = val_loss, epoch
                best_state = copy.deepcopy(model.state_dict())
                patience = 0
            else:
                patience += 1
            if epoch == 1 or epoch % 10 == 0:
                print(f"Epoch {epoch:3d} | train MSE {train_losses[-1]:.6f} | "
                      f"val MSE {val_loss:.6f} | lr {optimizer.param_groups[0]['lr']:.6f}")
            if patience >= experiment.train.early_stop_patience:
                print(f"Early stopping at epoch {epoch}")
                break

        if best_state is not None:
            model.load_state_dict(best_state)
        model.eval()
        x_test, _ = tensors["test"]
        with torch.no_grad():
            normalized = model(x_test, a_geo, a_corr)[:, :graph.n_neigh].cpu().numpy()
            normalized_val = model(x_val, a_geo, a_corr)[:, :graph.n_neigh].cpu().numpy()

    test_rows = rows["test"]
    anchors = samples.anchors[test_rows][:, :, None]
    predicted = norm.to_level(normalized + anchors if experiment.target == "delta" else normalized)
    actual = norm.to_level(samples.y[test_rows] + anchors
                           if experiment.target == "delta" else samples.y[test_rows])
    print(f"Best epoch: {best_epoch} | validation MSE: {best_val:.6f}")

    # DualTopoSTGCN has no dropout layers, so there is no MC-Dropout epistemic
    # term here; the interval comes from validation residuals alone, by the same
    # recipe the baselines use.
    val_rows = rows["val"]
    val_anchors = samples.anchors[val_rows][:, :, None]
    val_pred = norm.to_level(normalized_val + val_anchors
                             if experiment.target == "delta" else normalized_val)
    val_actual = norm.to_level(samples.y[val_rows] + val_anchors
                               if experiment.target == "delta" else samples.y[val_rows])
    val_horizon = np.broadcast_to(np.asarray(window.horizons), val_pred.shape)
    interval_model = fit_intervals(np.maximum(val_pred, 0.0).ravel(),
                                   val_actual.ravel(), val_horizon.ravel())

    records = []
    for sample_idx, position in enumerate(split.test):
        for h_idx, horizon in enumerate(window.horizons):
            for node, neighborhood in enumerate(NEIGHBORHOODS):
                value = max(0.0, float(predicted[sample_idx, node, h_idx]))
                records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": float(actual[sample_idx, node, h_idx]),
                    "predicted": value,
                    "error": value - float(actual[sample_idx, node, h_idx]),
                })

    checkpoint_path = paths.CHECKPOINT_DIR / f"{experiment.name}_{experiment.variant}.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "experiment": experiment.to_json(),
        "a_geo": a_geo.cpu(), "a_corr": a_corr.cpu(),
        "node_names": graph.node_names,
        "flu_means": norm.flu_mean, "flu_stds": norm.flu_std,
        "neighborhoods": NEIGHBORHOODS,
        "best_epoch": best_epoch, "best_val_mse": best_val,
    }, checkpoint_path)
    print(f"Checkpoint: {checkpoint_path}")

    predictions = attach_intervals(pd.DataFrame(records), interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")

    out = finish_run(
        model=experiment.name,
        variant=experiment.variant,
        predictions=predictions,
        config={
            "target_kind": experiment.target,
            "normalize": experiment.normalize,
            "split": split.to_json(),
            "graph_counts": graph.counts,
            "corr_topology_edges": int((np.triu(graph.W_corr, 1) > 0).sum()),
            "n_nodes": graph.n_nodes,
            "fusion": args.fusion,
            "time_axis_before_readout": model.time_out,
            "n_params": sum(p.numel() for p in model.parameters()),
            "best_epoch": best_epoch,
            "best_val_mse": best_val,
            "epochs_run": epoch,
            "paper": "Luo et al. 2025, BMC Public Health 25:408",
            "paper_gaps_filled": {
                "fusion_operator": args.fusion,
                "corr_threshold": experiment.graph.corr_threshold,
                "optimizer": "Adam",
            },
            "checkpoint": str(checkpoint_path.relative_to(paths.CODE_DIR)),
            "experiment": experiment.to_json(),
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        extras=True,
        bands=True,
        carbon=carbon,
        results_root=args.output_dir,
        title=f"{experiment.name} ({experiment.variant}) — horizon 1",
    )
    save_loss_curve(train_losses, val_losses, out / "loss_curve.png",
                    title=f"{experiment.name} ({experiment.variant}) training")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    parser.add_argument("--experiment", default="dualtopo")
    parser.add_argument("--name", default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--corr-threshold", type=float, default=None)
    parser.add_argument("--anchors", choices=["none", "single", "seven"], default=None)
    parser.add_argument("--fusion", choices=["concat", "mean", "max"], default="concat",
                        help="The paper lists a menu without saying which it used.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(resolve_experiment(args), args)


if __name__ == "__main__":
    main()
