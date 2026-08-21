"""Graph neural network forecasts of weekly Boston neighborhood influenza rates.

Replaces the three near-identical notebooks. Which graph and which features a
run uses comes from the EXPERIMENTS registry in influenza/config.py:

    python Code/run_gnn.py --experiment gnn_multiedge
    python Code/run_gnn.py --experiment gnn_corrbinary --corr-threshold 0.9
    python Code/run_gnn.py --experiment gnn_multiedge --rt --name gnn_multiedge_rt
    python Code/run_gnn.py --list

Predictions carry MC-Dropout predictive intervals, so metrics.csv includes
interval coverage alongside RMSE / MAPE / MAE / Corr.
"""

from __future__ import annotations

import argparse
from dataclasses import replace

try:
    import numpy as np
    import pandas as pd
    import torch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib torch "
        "torch-geometric."
    ) from exc

from influenza import (
    finish_run,
    paths,
    save_loss_curve,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_window, run_tag)
from influenza.config import EXPERIMENTS, Experiment
from influenza.graphs import build_graph
from influenza.intervals import empirical_coverage
from influenza.models import InfluenzaGNN
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.training import (
    calibrate_intervals,
    mc_dropout_forward,
    seed_everything,
    train_gcn,
)


def resolve_experiment(args: argparse.Namespace) -> Experiment:
    """Start from the registry entry, then apply the exposed CLI overrides."""
    if args.experiment not in EXPERIMENTS:
        raise SystemExit(
            f"Unknown experiment {args.experiment!r}. Available: {', '.join(sorted(EXPERIMENTS))}"
        )
    experiment = EXPERIMENTS[args.experiment]
    if experiment.model != "gcn_fusion":
        raise SystemExit(
            f"{args.experiment!r} is a {experiment.model} model. Use run_dualtopo.py instead."
        )

    graph_changes: dict = {}
    if args.corr_threshold is not None:
        graph_changes["corr_threshold"] = args.corr_threshold
    if args.geo_max_hop is not None:
        graph_changes["geo_max_hop"] = args.geo_max_hop
    if args.anchors is not None:
        graph_changes["anchors"] = args.anchors

    feature_changes: dict = {}
    if args.rt:
        feature_changes["use_rt"] = True
    if args.seasonality:
        feature_changes["use_seasonality"] = True
    if args.imputed_flag:
        feature_changes["use_imputed_flag"] = True

    train_changes: dict = {}
    if args.epochs is not None:
        train_changes["epochs"] = args.epochs
    if args.seed is not None:
        train_changes["seed"] = args.seed

    experiment = replace(
        experiment,
        name=args.name or experiment.name,
        variant=args.variant if args.variant != "all" else experiment.variant,
        normalize=args.normalize or experiment.normalize,
        target=args.target or experiment.target,
        graph=replace(experiment.graph, **graph_changes) if graph_changes else experiment.graph,
        features=replace(experiment.features, **feature_changes) if feature_changes else experiment.features,
        train=replace(experiment.train, **train_changes) if train_changes else experiment.train,
        window=resolve_window(args, experiment.window),
    )
    return experiment


def run(experiment: Experiment, args: argparse.Namespace) -> None:
    window = experiment.window
    city = resolve_city(args)
    results_root, checkpoint_root = city_output_dirs(args, city)
    rates = city.loaders.load_rates()
    data = variant_data(rates, experiment.variant)

    dataset = load_dataset(experiment.features, city=city, rates=data.available,
                           need_mbta=experiment.graph.transit)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)

    # Correlation edges must see only pre-test weeks, or the graph structure
    # itself encodes the evaluation period.
    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    graph = build_graph(experiment.graph, city=city, flu_history=history,
                        static=dataset.static, mbta=dataset.mbta)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'=' * 72}\n{city.label} | {experiment.name} | {experiment.variant} | "
          f"device={device}\n{'=' * 72}")
    if experiment.note:
        print(f"{experiment.note}\n")
    print(f"Graph: {graph.summary()}")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    first_target, last_target = split.test_target_span()
    print(f"Test targets: {first_target.date()} -> {last_target.date()}")

    samples, norm = build_samples(dataset, split, experiment.features, window, graph,
                                  target=experiment.target, normalize=experiment.normalize)
    print(f"Node features: {samples.n_feat} | global covariates: {samples.n_global} "
          f"| target: {experiment.target} | normalize: {experiment.normalize}")

    train_set = samples.subset(positions_to_rows(samples, split.train))
    val_set = samples.subset(positions_to_rows(samples, split.val))
    test_set = samples.subset(positions_to_rows(samples, split.test))

    edge_index, edge_weight = graph.edge_tensors()

    with track_emissions(run_tag(experiment.name, experiment.variant, window),
                         enabled=not args.no_carbon) as carbon:
        seed_everything(experiment.train.seed)
        model = InfluenzaGNN(
            n_node_feat=samples.n_feat,
            n_global=samples.n_global,
            n_horizons=len(window.horizons),
            hidden1=experiment.train.hidden[0],
            hidden2=experiment.train.hidden[1],
            fusion_out=experiment.train.hidden[2],
            dropout=experiment.train.dropout,
        ).to(device)
        print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

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
        test_draws, val_draws, val_actual, window.horizons)
    print(f"Best epoch: {result.best_epoch} | validation MSE: {result.best_val_loss:.6f}")

    records: list[dict] = []
    for sample_idx, position in enumerate(test_set.positions):
        for h_idx, horizon in enumerate(window.horizons):
            target_date = split.index[position + horizon]
            for node, neighborhood in enumerate(city.node_names):
                records.append({
                    "origin_date": split.index[position],
                    "target_date": target_date,
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
    print(f"95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")

    checkpoint_path = checkpoint_root / f"{experiment.name}_{experiment.variant}.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model_state_dict": model.state_dict(),
        "experiment": experiment.to_json(),
        "edge_index": edge_index,
        "edge_weight": edge_weight,
        "node_names": graph.node_names,
        "flu_means": norm.flu_mean,
        "flu_stds": norm.flu_std,
        "neighborhoods": list(city.node_names),
        "feature_names": samples.feature_names,
        "global_names": samples.global_names,
        "best_epoch": result.best_epoch,
        "best_val_mse": result.best_val_loss,
    }, checkpoint_path)
    print(f"Checkpoint: {checkpoint_path}")

    out = finish_run(
        model=experiment.name,
        variant=experiment.variant,
        predictions=predictions,
        config={
            "target_kind": experiment.target,
            "normalize": experiment.normalize,
            "split": split.to_json(),
            "graph_counts": graph.counts,
            "n_nodes": graph.n_nodes,
            "edge_weight_range": [float(graph.W.min()), float(graph.W.max())],
            "n_node_features": samples.n_feat,
            "n_global": samples.n_global,
            "feature_names": samples.feature_names,
            "global_names": samples.global_names,
            "n_params": sum(p.numel() for p in model.parameters()),
            "best_epoch": result.best_epoch,
            "best_val_mse": result.best_val_loss,
            "epochs_run": result.epochs_run,
            "checkpoint": paths.display(checkpoint_path),
            "experiment": experiment.to_json(),
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
            "city": city.name,
        },
        extras=True,
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
    )
    save_loss_curve(result.train_losses, result.val_losses, out / "loss_curve.png",
                    title=f"{experiment.name} ({experiment.variant}) training")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    parser.add_argument("--experiment", default="gnn_multiedge",
                        help="Registry entry from influenza/config.py.")
    parser.add_argument("--name", default=None,
                        help="Override the results directory name (for ablation arms).")
    parser.add_argument("--list", action="store_true", help="List experiments and exit.")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--corr-threshold", type=float, default=None)
    parser.add_argument("--geo-max-hop", type=int, default=None)
    parser.add_argument("--anchors", choices=["none", "single", "seven"], default=None)
    parser.add_argument("--normalize", choices=["all", "train"], default=None,
                        help="'all' reproduces the notebooks but leaks the test window.")
    parser.add_argument("--target", choices=["delta", "level"], default=None)
    parser.add_argument("--rt", action="store_true", help="Add the Rt growth-index feature.")
    parser.add_argument("--seasonality", action="store_true",
                        help="Add sin/cos of the target week's calendar position.")
    parser.add_argument("--imputed-flag", action="store_true",
                        help="Add a per-lag indicator for imputed (suppressed) weeks.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list:
        for name, experiment in EXPERIMENTS.items():
            print(f"{name:26s} [{experiment.model}] {experiment.note}")
        return
    run(resolve_experiment(args), args)


if __name__ == "__main__":
    main()
