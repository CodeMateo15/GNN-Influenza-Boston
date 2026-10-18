#!/usr/bin/env python3
"""Gradient-boosted trees over the same per-node features the GNN sees.

Why this baseline exists. `lstm` is the "same data, no graph, neural" control
and `arima` is the univariate one, but nothing in the repository was a strong
*tabular* learner. Boosted trees are the default answer to a small-sample
regression problem with a few dozen engineered features, which is exactly the
shape of this one -- 122 training origins, 14 nodes, ~40 columns. If trees match
the graph model, the graph is not doing anything a gradient booster cannot.

One model is fitted over all nodes pooled, not one per node. Per-node fitting
would give each tree 122 rows, and the node's identity is supplied as a feature
instead, so the model can still specialise while sharing structure. That is the
same argument `load_monthly_neighborhood` makes about ratios: pool the evidence,
then let the model separate it.

    python Code/run_xgboost.py --variant post_covid --horizons 2
    python Code/run_xgboost.py --target level        # predict the rate directly
    python Code/run_xgboost.py --target blend --n-seeds 10   # gnn_st's target and ensemble

Default target is the residual from the train-only harmonic climatology, for the
same reason the GNN uses a baseline and with one extra: trees cannot extrapolate
beyond the range they were trained on, so asking them for a level in a season
higher than any in training guarantees a flat-topped forecast. Subtracting the
seasonal curve first turns that into an anomaly problem, which trees handle.

`--target blend` subtracts gnn_st's baseline instead: s_h * origin level +
(1 - s_h) * climatology. gnn_st learns s_h by gradient; trees cannot, so here it
is the least-squares share on the TRAINING rows, clipped to [0, 1] -- the best
fixed blend the training targets support. Validation stays untouched for early
stopping and the interval fit.
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import json

import numpy as np
import pandas as pd

try:
    import xgboost as xgb
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "run_xgboost.py needs xgboost. pip install xgboost"
    ) from exc

from influenza import (finish_run, impute_causal, paths, split_origins, track_emissions,
                       valid_origins, variant_data)
from influenza.cli import add_common_args, city_output_dirs, resolve_city, resolve_window, run_tag
from influenza.climatology import fit_climatology
from influenza.config import EXPERIMENTS
from influenza.intervals import empirical_coverage, fit_intervals, quantile_record
from influenza.samples import build_samples, load_dataset, positions_to_rows

DEFAULT_PARAMS = dict(
    n_estimators=600,
    learning_rate=0.03,
    max_depth=4,          # shallow: 1,700 pooled rows does not support deep trees
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=4,
    reg_lambda=2.0,
    objective="reg:squarederror",
)


def flatten(samples, n_neigh: int, node_ids: bool = True):
    """(S, n_nodes, n_feat) -> one row per (origin, scored node).

    The node index rides along as a feature so a single pooled model can still
    tell Dorchester from Fenway. It is left as an integer rather than one-hot:
    trees split on it directly and 14 one-hot columns would dilute the column
    subsampling.
    """
    S = samples.X.shape[0]
    rows, meta = [], []
    for s in range(S):
        for node in range(n_neigh):
            feat = samples.X[s, node]
            if node_ids:
                feat = np.concatenate([feat, [node]])
            rows.append(feat)
            meta.append((s, node))
    return np.asarray(rows, dtype=np.float32), meta


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("exclude_covid", "post_covid", "full"))
    parser.add_argument("--name", default="xgboost")
    parser.add_argument("--target", choices=("climatology", "level", "blend"),
                        default="climatology")
    parser.add_argument("--features-from", default="gnn_st",
                        help="Registry arm whose FeatureSpec supplies the columns, so "
                             "the baseline reads the same inputs as the graph model.")
    parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS["n_estimators"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-seeds", type=int, default=1,
                        help="Boosters per horizon, seeds seed..seed+n-1, averaged. The row "
                             "and column subsampling make seeds differ; gnn_st uses 10.")
    for key in ("learning_rate", "max_depth", "min_child_weight", "reg_lambda",
                "subsample", "colsample_bytree"):
        kind = int if key == "max_depth" else float
        parser.add_argument(f"--{key.replace('_', '-')}", type=kind, default=DEFAULT_PARAMS[key])
    args = parser.parse_args()
    params = {**DEFAULT_PARAMS, **{k: getattr(args, k) for k in (
        "learning_rate", "max_depth", "min_child_weight", "reg_lambda",
        "subsample", "colsample_bytree")}, "n_estimators": args.n_estimators}
    seeds = [args.seed + i for i in range(args.n_seeds)]

    city = resolve_city(args)
    results_root, checkpoint_root = city_output_dirs(args, city)
    reference = EXPERIMENTS[args.features_from]
    window = resolve_window(args, reference.window, city)

    rates = city.loaders.load_rates()
    data = variant_data(rates, args.variant)
    dataset = load_dataset(reference.features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)

    # The graph is built only because build_samples needs its node count; no edge
    # ever reaches the model. That is the point of this baseline.
    from influenza.graphs import build_graph
    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    static = dataset.static
    if reference.graph.demo and static is None:
        static = city.loaders.load_static_demographics()[0]
    graph = build_graph(reference.graph, city=city, flu_history=history,
                        static=static)
    n_neigh = graph.n_neigh

    samples, norm = build_samples(dataset, split, reference.features, window, graph,
                                  target="level", normalize=reference.normalize)

    print(f"\n{'=' * 72}\n{city.label} | {args.name} | {args.variant} | "
          f"target={args.target}\n{'=' * 72}")
    print(f"Train {len(split.train)} | Validation {len(split.val)} | Test {len(split.test)} origins")

    end = split.train[-1] + window.max_horizon + 1
    climatology = fit_climatology(dataset.rates, end=end)
    clim_rate = climatology.level(dataset.week_index)
    # Origin level for the blend, causally imputed as every model's inputs are.
    origin_rate = impute_causal(dataset.rates)[0].to_numpy(dtype=np.float64)

    X_all, meta = flatten(samples, n_neigh)
    print(f"Pooled design matrix: {X_all.shape[0]} rows x {X_all.shape[1]} columns "
          f"({samples.n_feat} node features + node id)")

    train_rows = set(positions_to_rows(samples, split.train))
    val_rows = set(positions_to_rows(samples, split.val))
    test_rows = positions_to_rows(samples, split.test)

    records: list[dict] = []
    val_records: list[dict] = []
    blend_shares: dict[int, float] = {}
    best_iterations: dict[int, list[int]] = {}
    print(f"Budget: {len(window.horizons) * len(seeds)} epochs x 1 seeds", flush=True)
    print("--- seed 0 (1/1) ---", flush=True)
    step = 0
    with track_emissions(run_tag(args.name, args.variant, window),
                         enabled=not args.no_carbon, city=city.name) as carbon:
        for h_idx, horizon in enumerate(window.horizons):
            # Targets in RATE units, so the climatology offset is interpretable.
            y_rate = np.full(len(meta), np.nan, dtype=np.float64)
            base = np.zeros(len(meta), dtype=np.float64)
            origin = np.zeros(len(meta), dtype=np.float64)
            for r, (s, node) in enumerate(meta):
                position = samples.positions[s]
                actual = norm.to_level(samples.y[s:s + 1])[0, node, h_idx]
                y_rate[r] = actual
                base[r] = clim_rate[position + horizon, node]
                origin[r] = origin_rate[position, node]

            observed = np.isfinite(y_rate)

            def mask(rowset):
                idx = [r for r, (s, _) in enumerate(meta) if s in rowset]
                return [r for r in idx if observed[r]]

            tr, va = mask(train_rows), mask(val_rows)
            if args.target == "blend":
                # Least-squares share of the origin level in y - clim = s (origin - clim),
                # on training rows only, clipped so the blend stays a convex mix.
                gap = origin[tr] - base[tr]
                share = float(np.clip((gap @ (y_rate[tr] - base[tr])) / max(gap @ gap, 1e-12),
                                      0.0, 1.0))
                blend_shares[horizon] = share
                base = share * origin + (1.0 - share) * base
                print(f"  h={horizon}: origin-level share of the blend {share:.3f}")
            target = y_rate if args.target == "level" else y_rate - base

            boosters = []
            for seed in seeds:
                model = xgb.XGBRegressor(**{**params, "random_state": seed,
                                            "early_stopping_rounds": 50})
                with carbon.phase("train"):
                    model.fit(X_all[tr], target[tr], eval_set=[(X_all[va], target[va])],
                              verbose=False)
                carbon.add_epochs(1)
                boosters.append(model)
                step += 1
                print(f"Epoch {step} | h={horizon} seed={seed} best_iteration="
                      f"{model.best_iteration} val RMSE={model.best_score:.4f}", flush=True)
            best_iterations[horizon] = [int(m.best_iteration) for m in boosters]
            model = boosters[0]
            best = model.best_iteration

            # Persist the booster. Trees are the one model family with an exact,
            # instant Shapley method (TreeExplainer), and until now this script
            # fit a model, predicted, and threw it away -- so the cheapest
            # attribution in the project was the one that could not be computed.
            # Horizon is in the filename because this loop fits a SEPARATE model
            # per horizon inside a single run, unlike the .pt writers.
            booster_path = (checkpoint_root /
                            f"{args.name}_{args.variant}_h{horizon:02d}.json")
            booster_path.parent.mkdir(parents=True, exist_ok=True)
            model.save_model(booster_path)
            # The design matrix is samples.X[s, node] plus a trailing node-id
            # column (see flatten). run_shap.py needs that layout to group
            # columns, and reconstructing it by convention would silently rot.
            (booster_path.with_suffix(".meta.json")).write_text(json.dumps({
                "feature_names": [*samples.feature_names, "node_id"],
                "lookback": samples.lookback,
                "temporal_channels": samples.temporal_channels,
                "target": args.target,
                "horizon": horizon,
                "city": city.name,
                "variant": args.variant,
                "best_iteration": int(best),
            }, indent=2))

            prediction = np.mean([m.predict(X_all) for m in boosters], axis=0)
            if args.target != "level":
                prediction = prediction + base
            prediction = np.maximum(prediction, 0.0)

            # Intervals from the shared recipe, fitted on validation only, so the
            # bands are comparable with every other model in the repository.
            va_all = [r for r, (s, _) in enumerate(meta) if s in val_rows and observed[r]]
            horizon_col = np.full(len(va_all), horizon)
            interval = fit_intervals(prediction[va_all], y_rate[va_all], horizon_col,
                                     two_sided=args.two_sided_intervals)
            lower, upper = interval.bounds(prediction, np.full(len(meta), horizon))
            quantiles = interval.quantiles(prediction, np.full(len(meta), horizon))

            for r in va_all:
                s, node = meta[r]
                position = samples.positions[s]
                val_records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": city.node_names[node],
                    "actual": float(y_rate[r]),
                    "predicted": float(prediction[r]),
                })
            for r, (s, node) in enumerate(meta):
                if s not in set(test_rows):
                    continue
                position = samples.positions[s]
                records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": city.node_names[node],
                    "actual": float(y_rate[r]),
                    "predicted": float(prediction[r]),
                    "error": float(prediction[r] - y_rate[r]),
                    "lower": float(lower[r]),
                    "upper": float(upper[r]),
                    **quantile_record(quantiles[r]),
                })

    predictions = pd.DataFrame(records)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"95% interval test coverage {coverage:.1f}%")

    finish_run(
        model=args.name, variant=args.variant, predictions=predictions,
        config={
            "model_class": "xgboost.XGBRegressor",
            "target_kind": args.target,
            "features_from": args.features_from,
            "n_node_features": samples.n_feat,
            "pooled_rows": int(X_all.shape[0]),
            "params": {**params, "random_state": args.seed},
            "n_seeds": len(seeds),
            "seeds": seeds,
            "best_iterations": {str(k): v for k, v in best_iterations.items()},
            **({"blend_share": {str(k): v for k, v in blend_shares.items()}}
               if blend_shares else {}),
            "split": split.to_json(),
            "climatology": climatology.to_json(),
            "test_interval_coverage": coverage,
            "city": city.name,
            "note": "One pooled model over all nodes with the node index as a "
                    "feature. No edges reach the model; it reads the same "
                    "per-node columns the graph model does.",
        },
        extras=True, bands=True, carbon=carbon,
        results_root=results_root, city=city,
        extra_tables={"predictions_val": pd.DataFrame(val_records)},
    )


if __name__ == "__main__":
    main()
