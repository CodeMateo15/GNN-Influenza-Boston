#!/usr/bin/env python3
"""Graph Attention Network baseline (Luo et al. 2025 comparison model).

Luo et al. compare Dual-Topo-STGCN against ARIMA, LSTM, Conv-LSTM and GAT, and
GAT places last at Corr 0.5994. This is that GAT: a plain spatial attention
network over ILI history with no temporal encoder, kept standalone for the same
reason `run_dualtopo.py` is standalone.

Do not confuse it with the `gnn_st_gat` arm. That one swaps GATConv into
SpatioTemporalGNN and asks whether attention beats degree-normalised averaging
*given* a temporal stack. This one asks what the paper asked. The two answer
different questions and, on this data, give very different numbers -- which is
itself the interesting result.

The paper specifies its GAT only as a standard multi-head attention network over
the topology, so layer count, head count, hidden width and the readout are our
choices and are recorded in run_config.json, exactly as the three unstated
Dual-Topo-STGCN choices are.

    python Code/run_gat.py --variant post_covid
    python Code/run_gat.py --variant full --horizons 2
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
from dataclasses import replace

try:
    import numpy as np
    import pandas as pd
    import torch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "run_gat.py needs torch and torch-geometric: pip install torch torch-geometric"
    ) from exc

from influenza import (
    finish_run, paths, save_loss_curve, split_origins, track_emissions,
    valid_origins, variant_data,
)
from influenza.cli import (add_common_args, check_experiment_supported,
                           city_output_dirs, resolve_city,
                           resolve_window, run_tag)
from influenza.config import EXPERIMENTS
from influenza.graphs import build_graph
from influenza.intervals import empirical_coverage
from influenza.models import GATBaseline
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.training import (calibrate_intervals, mc_dropout_forward,
                                seed_everything, train_gcn)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("exclude_covid", "post_covid", "full"))
    parser.add_argument("--experiment", default="gat")
    parser.add_argument("--name", default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--heads", type=int, default=None)
    args = parser.parse_args()

    if args.experiment not in EXPERIMENTS:
        raise SystemExit(f"Unknown experiment {args.experiment!r}")
    experiment = EXPERIMENTS[args.experiment]
    if experiment.model != "gat":
        raise SystemExit(
            f"{args.experiment!r} is a {experiment.model} model. Use run_gnn.py "
            "for stgnn/gcn_fusion arms and run_dualtopo.py for the paper's STGCN."
        )

    train_changes: dict = {}
    if args.epochs is not None:
        train_changes["epochs"] = args.epochs
    if args.seed is not None:
        train_changes["seed"] = args.seed
    if args.heads is not None:
        train_changes["hidden"] = (experiment.train.hidden[0], args.heads)
    experiment = replace(
        experiment,
        name=args.name or experiment.name,
        variant=args.variant,
        train=replace(experiment.train, **train_changes) if train_changes else experiment.train,
        window=resolve_window(args, experiment.window, resolve_city(args)),
    )

    window = experiment.window
    city = resolve_city(args)
    check_experiment_supported(experiment, city)
    results_root, checkpoint_root = city_output_dirs(args, city)

    rates = city.loaders.load_rates()
    data = variant_data(rates, experiment.variant)
    dataset = load_dataset(experiment.features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)

    # Correlation edges see pre-test weeks only; the slice stays at the call site.
    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    graph = build_graph(experiment.graph, city=city, flu_history=history,
                        static=dataset.static)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'=' * 72}\n{city.label} | {experiment.name} | {experiment.variant} | "
          f"device={device}\n{'=' * 72}")
    print(f"{experiment.note}\n")
    print(f"Graph: {graph.summary()}")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")

    samples, norm = build_samples(dataset, split, experiment.features, window, graph,
                                  target=experiment.target, normalize=experiment.normalize)
    if samples.n_feat != window.lookback:
        raise SystemExit(
            f"Expected exactly {window.lookback} node features (the ILI lags) but got "
            f"{samples.n_feat}. The GAT baseline takes ILI rates only -- check that "
            "weather, demographics and global covariates are all off."
        )
    print(f"Node features: {samples.n_feat} (ILI lags only) | target: {experiment.target}")

    train_set = samples.subset(positions_to_rows(samples, split.train))
    val_set = samples.subset(positions_to_rows(samples, split.val))
    test_set = samples.subset(positions_to_rows(samples, split.test))
    edge_index, edge_weight = graph.edge_tensors()

    hidden, heads = experiment.train.hidden[0], experiment.train.hidden[1]
    with track_emissions(run_tag(experiment.name, experiment.variant, window),
                         enabled=not args.no_carbon) as carbon:
        seed_everything(experiment.train.seed)
        model = GATBaseline(lookback=window.lookback, hidden=hidden, heads=heads,
                            n_horizons=len(window.horizons),
                            dropout=experiment.train.dropout).to(device)
        print(f"Parameters: {sum(p.numel() for p in model.parameters()):,} "
              f"({hidden} hidden, {heads} heads)")

        result = train_gcn(model, train_set, val_set, edge_index=edge_index,
                           edge_weight=edge_weight, spec=experiment.train,
                           device=device, n_neigh=graph.n_neigh)

        torch.manual_seed(experiment.train.mc_seed)
        mc_kwargs = dict(edge_index=edge_index, edge_weight=edge_weight, norm=norm,
                         n_neigh=graph.n_neigh, device=device,
                         n_mc=experiment.train.mc_samples, target=experiment.target)
        test_draws, test_actual = mc_dropout_forward(model, test_set, **mc_kwargs)
        val_draws, val_actual = mc_dropout_forward(model, val_set, **mc_kwargs)

    prediction, interval_model = calibrate_intervals(
        test_draws, val_draws, val_actual, window.horizons,
        two_sided=args.two_sided_intervals)
    print(f"Best epoch: {result.best_epoch} | validation MSE: {result.best_val_loss:.6f}")

    records: list[dict] = []
    for sample_idx, position in enumerate(test_set.positions):
        for h_idx, horizon in enumerate(window.horizons):
            for node, neighborhood in enumerate(city.node_names):
                records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": float(test_actual[sample_idx, node, h_idx]),
                    "predicted": max(0.0, float(prediction.mean[sample_idx, node, h_idx])),
                    "error": float(prediction.mean[sample_idx, node, h_idx]
                                   - test_actual[sample_idx, node, h_idx]),
                    "lower": float(prediction.lower[sample_idx, node, h_idx]),
                    "upper": float(prediction.upper[sample_idx, node, h_idx]),
                })

    predictions = pd.DataFrame(records)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"95% interval test coverage {coverage:.1f}%")

    checkpoint_path = checkpoint_root / f"{experiment.name}_{experiment.variant}.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(),
                "experiment": experiment.to_json(),
                "edge_index": edge_index, "edge_weight": edge_weight,
                "flu_means": norm.flu_mean, "flu_stds": norm.flu_std,
                "neighborhoods": list(city.node_names)}, checkpoint_path)

    out = finish_run(
        model=experiment.name, variant=experiment.variant, predictions=predictions,
        config={
            "model_class": "GATBaseline",
            "paper": "Luo et al. 2025, BMC Public Health 25:408 (comparison model)",
            "paper_reported_corr": 0.5994,
            "paper_gaps_filled": {
                "n_layers": 2, "hidden": hidden, "heads": heads,
                "activation": "ELU", "readout": "linear",
                "edge_weight": "passed as a 1-d edge feature (edge_dim=1)",
                "note": "The paper specifies only a standard multi-head attention "
                        "network over the topology; these are our choices.",
            },
            "target_kind": experiment.target,
            "split": split.to_json(),
            "graph_counts": graph.counts,
            "n_node_features": samples.n_feat,
            "n_params": sum(p.numel() for p in model.parameters()),
            "best_epoch": result.best_epoch,
            "best_val_mse": result.best_val_loss,
            "test_interval_coverage": coverage,
            "city": city.name,
        },
        extras=True, bands=True, carbon=carbon,
        results_root=results_root, city=city,
    )
    save_loss_curve(result.train_losses, result.val_losses, out / "loss_curve.png",
                    title=f"{experiment.name} ({experiment.variant}) training")


if __name__ == "__main__":
    main()
