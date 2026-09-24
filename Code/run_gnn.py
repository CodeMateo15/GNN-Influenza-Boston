"""Graph neural network forecasts of weekly Boston neighborhood influenza rates.

Replaces the three near-identical notebooks. Which graph and which features a
run uses comes from the EXPERIMENTS registry in influenza/config.py:

    python Code/run_gnn.py --experiment gnn_st
    python Code/run_gnn.py --experiment gnn_st --corr-threshold 0.9
    python Code/run_gnn.py --experiment gnn_st --rt --name gnn_st_rt
    python Code/run_gnn.py --list

Predictions carry MC-Dropout predictive intervals, so metrics.csv includes
interval coverage alongside RMSE / MAPE / MAE / Corr.
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
from influenza import data
from influenza.cli import (add_common_args, check_experiment_supported,
                           city_output_dirs, resolve_city,
                          resolve_window, run_tag)
from influenza.config import EXPERIMENTS, Experiment
from influenza.graphs import build_graph
from influenza.intervals import empirical_coverage
from influenza.models import InfluenzaGNN, SpatioTemporalGNN
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.training import mc_dropout_stgnn, train_stgnn


def _blend_init(horizons) -> tuple[float, ...]:
    """Logits for the origin-level share of the baseline, one per horizon.

    Decreasing in the horizon because that is what the data says: Boston's
    citywide corr(rate_t, rate_{t-h}) is 0.906 at h=1 and 0.271 at h=4, while the
    seasonal curve holds 0.697 at every horizon. sigmoid(2.5)=0.92 at h=1 falls
    to sigmoid(-1.5)=0.18 by h=12. Only the starting point -- the model learns it.
    """
    scale = {1: 2.5, 2: 1.5, 3: 0.8, 4: 0.0}
    return tuple(scale.get(int(h), -1.5) for h in horizons)


def _assert_mc_dropout_valid(model) -> None:
    """MC-Dropout requires functional dropout and no running-statistics norms.

    `mc_dropout_forward` calls model.train() at inference to enable dropout. An
    nn.Dropout submodule would work, but a BatchNorm would also switch to batch
    statistics and silently corrupt every draw -- and the failure looks like bad
    calibration, not like a bug. LayerNorm is fine: it keeps no running stats.
    """
    import torch.nn as nn
    offenders = sorted({
        type(module).__name__ for module in model.modules()
        if isinstance(module, (nn.Dropout, nn.Dropout1d, nn.Dropout2d,
                               nn.BatchNorm1d, nn.BatchNorm2d, nn.InstanceNorm1d))
    })
    if offenders:
        raise SystemExit(
            f"{type(model).__name__} contains {offenders}, which breaks MC-Dropout: "
            "influenza/intervals.py calibrates on draws taken with model.train(), "
            "so any module whose inference behaviour differs from training would "
            "corrupt every interval. Use F.dropout and LayerNorm."
        )
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
    if experiment.model not in ("gcn_fusion", "stgnn"):
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
    if getattr(args, "n_seeds", None) is not None:
        if args.n_seeds < 1:
            raise SystemExit("--n-seeds must be at least 1")
        train_changes["n_seeds"] = args.n_seeds
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
        window=resolve_window(args, experiment.window, resolve_city(args)),
    )
    return experiment


def run(experiment: Experiment, args: argparse.Namespace) -> None:
    window = experiment.window
    city = resolve_city(args)
    check_experiment_supported(experiment, city)
    results_root, checkpoint_root = city_output_dirs(args, city)
    rates = city.loaders.load_rates()
    data = variant_data(rates, experiment.variant)

    dataset = load_dataset(experiment.features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)

    # Correlation edges must see only pre-test weeks, or the graph structure
    # itself encodes the evaluation period.
    history = dataset.rates.loc[dataset.rates.index < window.test_start]

    # Demographics are two separate things: node FEATURES and the similarity
    # EDGES built from them. `load_dataset` is demand-driven on FeatureSpec, so
    # it returns static=None when the features are off -- which used to make
    # `use_demographics=False` with `demo=True` an unsatisfiable combination
    # rather than a meaningful ablation. Load the matrix for the graph when the
    # graph asks for it, independently of whether the model sees it as input.
    # Kept at the call site, like the correlation-edge slice above, so the reason
    # the graph needs data the model does not is visible.
    graph_static = dataset.static
    if experiment.graph.demo and graph_static is None:
        graph_static = city.loaders.load_static_demographics()[0]

    graph = build_graph(experiment.graph, city=city, flu_history=history,
                        static=graph_static)

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
    # Echoed so run_progress.py can compute a percentage without instrumenting
    # the training loop: it needs the denominator, and the epoch lines only give
    # the numerator.
    print(f"Budget: {experiment.train.epochs} epochs x "
          f"{max(1, experiment.train.n_seeds)} seeds")

    train_set = samples.subset(positions_to_rows(samples, split.train))
    val_set = samples.subset(positions_to_rows(samples, split.val))
    test_set = samples.subset(positions_to_rows(samples, split.test))

    edge_index, edge_weight = graph.edge_tensors()

    relations = graph.relation_tensors(list(experiment.train.relations))
    if experiment.model == "stgnn" and not relations:
        raise SystemExit(
            f"None of the requested relations {list(experiment.train.relations)} exist in "
            f"this graph. Available: {['all', *sorted(graph.relations)]}. A silently "
            "empty relation list would train the model with no spatial term at all, "
            "which reads as 'the graph does not help' rather than as a config error."
        )

    def build_model() -> torch.nn.Module:
        if experiment.model == "stgnn":
            return SpatioTemporalGNN(
                lookback=samples.lookback,
                temporal_channels=samples.temporal_channels,
                n_static_feat=samples.n_static_feat,
                n_global=samples.n_global,
                n_nodes=graph.n_nodes,
                n_horizons=len(window.horizons),
                relation_names=[name for name, _, _ in relations],
                hidden=experiment.train.channels,
                dropout=experiment.train.dropout,
                dilations=experiment.train.dilations,
                adaptive_dim=experiment.train.adaptive_dim if experiment.train.adaptive else 0,
                dropedge=experiment.train.drop_edge,
                blend_init=_blend_init(window.horizons),
                horizon_steps=tuple(int(h) for h in window.horizons),
                trend_anchor=experiment.target == "trendblend",
                cascade=experiment.target == "cascade",
                n_blocks=experiment.train.n_blocks,
                conv=experiment.train.conv,
                heads=experiment.train.heads,
            ).to(device)
        return InfluenzaGNN(
            n_node_feat=samples.n_feat,
            n_global=samples.n_global,
            n_horizons=len(window.horizons),
            hidden1=experiment.train.hidden[0],
            hidden2=experiment.train.hidden[1],
            fusion_out=experiment.train.hidden[2],
            dropout=experiment.train.dropout,
        ).to(device)

    seeds = [experiment.train.seed + i for i in range(max(1, experiment.train.n_seeds))]
    members: list[dict] = []

    with track_emissions(run_tag(experiment.name, experiment.variant, window),
                         enabled=not args.no_carbon) as carbon:
        for member, seed in enumerate(seeds):
            seed_everything(seed)
            model = build_model()
            _assert_mc_dropout_valid(model)
            if member == 0:
                print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
            if len(seeds) > 1:
                print(f"\n--- seed {seed} ({member + 1}/{len(seeds)}) ---")

            if experiment.model == "stgnn":
                result = train_stgnn(
                    model, train_set, val_set, relations=relations,
                    spec=experiment.train, device=device, n_neigh=graph.n_neigh,
                    blended=experiment.target in ("blend", "trendblend", "cascade"),
                    target_kind=experiment.target)
                mc_kwargs = dict(relations=relations, norm=norm, n_neigh=graph.n_neigh,
                                 device=device, target=experiment.target)
                forward = mc_dropout_stgnn
            else:
                result = train_gcn(model, train_set, val_set, edge_index=edge_index,
                                   edge_weight=edge_weight, spec=experiment.train,
                                   device=device, n_neigh=graph.n_neigh)
                mc_kwargs = dict(edge_index=edge_index, edge_weight=edge_weight,
                                 norm=norm, n_neigh=graph.n_neigh, device=device,
                                 target=experiment.target)
                forward = mc_dropout_forward

            # Split the MC budget across members so the total number of draws is
            # unchanged and the pooled spread now also carries seed variance --
            # which is the honest epistemic term, since the h=4 per-seed spread is
            # wider than any architecture change measured.
            per_member = max(1, experiment.train.mc_samples // len(seeds))
            torch.manual_seed(experiment.train.mc_seed + member)
            test_d, test_actual = forward(model, test_set, n_mc=per_member, **mc_kwargs)
            val_d, val_actual = forward(model, val_set, n_mc=per_member, **mc_kwargs)
            members.append({"seed": seed, "result": result, "model": model,
                            "test": test_d, "val": val_d})

    # A seed whose best epoch sits at the very end of the budget was probably
    # still improving when training stopped, which silently caps the ensemble.
    # Detecting it is better than padding the budget on a guess: the budget is
    # also the cosine schedule's T_max, so raising it changes the learning-rate
    # curve and invalidates the measurement it was chosen from.
    ceiling = 0.95 * experiment.train.epochs
    truncated = [m["seed"] for m in members if m["result"].best_epoch >= ceiling]
    if truncated:
        print(f"  WARNING: seed(s) {truncated} peaked at or past {ceiling:.0f} of "
              f"{experiment.train.epochs} epochs, so they may still have been "
              f"improving when the budget ran out. Raise TrainSpec.epochs -- and "
              f"re-measure, because epochs is also the cosine schedule's T_max.")

    test_draws = np.concatenate([m["test"] for m in members], axis=0)
    val_draws = np.concatenate([m["val"] for m in members], axis=0)
    model = members[0]["model"]
    result = min((m["result"] for m in members), key=lambda r: r.best_val_loss)

    prediction, interval_model = calibrate_intervals(
        test_draws, val_draws, val_actual, window.horizons,
        two_sided=args.two_sided_intervals)
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

    # The same table for the VALIDATION split. Without it, anything that needs
    # fitting on held-out forecasts -- the de-lag gamma in compare_timing.py, any
    # ensemble weight -- has nowhere honest to fit, and the only alternative is
    # tuning on the test weeks. The interval parameters already fit here; this
    # just writes the rows out so other corrections can too.
    val_mean = val_draws.mean(axis=0)
    val_records: list[dict] = []
    for sample_idx, position in enumerate(val_set.positions):
        for h_idx, horizon in enumerate(window.horizons):
            for node, neighborhood in enumerate(city.node_names):
                val_records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": float(val_actual[sample_idx, node, h_idx]),
                    "predicted": max(0.0, float(val_mean[sample_idx, node, h_idx])),
                })
    val_predictions = pd.DataFrame(val_records)
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
            **_stgnn_provenance(experiment, members, samples, dataset, split, window),
        },
        extras=True,
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
        extra_tables={**_seed_spread_table(members),
                      "predictions_val": val_predictions},
    )
    save_loss_curve(result.train_losses, result.val_losses, out / "loss_curve.png",
                    title=f"{experiment.name} ({experiment.variant}) training")



def _stgnn_provenance(experiment, members, samples, dataset, split, window) -> dict:
    """Extra run_config fields that make a headline number auditable.

    The learned blend and relation gates are not diagnostics -- they are the
    answer to "what did the model lean on", which is the question the project
    exists to ask. Recording them next to the metrics is what stops that answer
    from having to be re-derived from a checkpoint later.
    """
    extra: dict = {
        "seeds": [m["seed"] for m in members],
        "n_seeds": len(members),
        "ensemble_reduction": "mean of pooled MC draws in normalized space",
        "per_seed_best_val_mse": {m["seed"]: m["result"].best_val_loss for m in members},
        "per_seed_best_epoch": {m["seed"]: m["result"].best_epoch for m in members},
        "carry_forward_limits": {
            name: data.carry_forward_limit(name) for name in samples.global_names
        },
    }
    try:
        extra["globals_coverage"] = data.coverage_report(
            dataset.week_index, dataset.globals_,
            test_start=window.test_start, test_end=window.test_end)
    except Exception:  # noqa: BLE001 - provenance must never fail a run
        pass
    if experiment.model != "stgnn":
        return extra

    first = members[0]["model"]
    extra["lookback"] = samples.lookback
    extra["temporal_channels"] = samples.temporal_channels
    extra["n_static_features"] = samples.n_static_feat
    extra["relations_used"] = list(experiment.train.relations)
    extra["blend_origin_share_per_horizon"] = {
        int(h): round(v, 4) for h, v in zip(window.horizons, first.blend_weights())
    }
    extra["relation_gate_per_block"] = [
        {k: round(v, 4) for k, v in block.items()} for block in first.gate_weights()
    ]
    extra["per_seed_blend_origin_share"] = {
        m["seed"]: [round(v, 4) for v in m["model"].blend_weights()] for m in members
    }
    if experiment.target == "trendblend":
        # A result in its own right, like the blend share beside it: how much of
        # the recent trend the model chose to carry into its anchor. Near 0 means
        # it declined, and the arm reduces to `gnn_st`.
        extra["blend_trend_share_per_horizon"] = {
            int(h): round(v, 4) for h, v in zip(window.horizons, first.trend_weights())
        }
        extra["per_seed_blend_trend_share"] = {
            m["seed"]: [round(v, 4) for v in m["model"].trend_weights()] for m in members
        }
    return extra


def _seed_spread_table(members) -> dict:
    """One row per ensemble member, so the per-seed range is in the results tree.

    The h=4 per-seed standard deviation of macro Corr is about 0.05 -- wider than
    any single architecture change measured -- so a headline number without this
    table beside it cannot be told apart from a lucky draw.
    """
    if len(members) <= 1:
        return {}
    rows = [{"seed": m["seed"], "best_epoch": m["result"].best_epoch,
             "best_val_mse": m["result"].best_val_loss,
             "epochs_run": m["result"].epochs_run}
            for m in members]
    return {"seed_spread": pd.DataFrame(rows)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    parser.add_argument("--experiment", default="gnn_st",
                        help="Registry entry from influenza/config.py.")
    parser.add_argument("--name", default=None,
                        help="Override the results directory name (for ablation arms).")
    parser.add_argument("--list", action="store_true", help="List experiments and exit.")
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--corr-threshold", type=float, default=None)
    parser.add_argument("--geo-max-hop", type=int, default=None)
    # "full" is the city-neutral synonym for "seven" and is what the xcity_* arms
    # use; it was valid in the registry but rejected by the CLI.
    parser.add_argument("--anchors", choices=["none", "single", "seven", "full"], default=None)
    parser.add_argument("--normalize", choices=["all", "train"], default=None,
                        help="'all' reproduces the notebooks but leaks the test window.")
    parser.add_argument("--target",
                        choices=["delta", "level", "blend", "trendblend", "cascade"],
                        default=None,
                        help="What the network predicts a residual from. 'delta' is "
                             "the origin level, 'level' is nothing, 'blend' is a "
                             "learned mix of the origin level and the seasonal "
                             "climatology, and 'trendblend' is that mix with the "
                             "origin half extrapolated along the recent trend rather "
                             "than held flat (SpatioTemporalGNN only).")
    parser.add_argument("--n-seeds", type=int, default=None,
                        help="Ensemble members, seeds seed..seed+n-1. Overrides the "
                             "registry. Ablations only need enough seeds to rank, "
                             "not the 10 the headline arm uses.")
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
