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

Default target is the residual from the train-only harmonic climatology, for the
same reason the GNN uses a baseline and with one extra: trees cannot extrapolate
beyond the range they were trained on, so asking them for a level in a season
higher than any in training guarantees a flat-topped forecast. Subtracting the
seasonal curve first turns that into an anomaly problem, which trees handle.
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

from influenza import finish_run, paths, split_origins, track_emissions, valid_origins, variant_data
from influenza.cli import add_common_args, city_output_dirs, resolve_city, resolve_window, run_tag
from influenza.climatology import fit_climatology
from influenza.config import EXPERIMENTS
from influenza.intervals import empirical_coverage, fit_intervals
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
    parser.add_argument("--target", choices=("climatology", "level"), default="climatology")
    parser.add_argument("--features-from", default="gnn_st",
                        help="Registry arm whose FeatureSpec supplies the columns, so "
                             "the baseline reads the same inputs as the graph model.")
    parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS["n_estimators"])
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

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

    X_all, meta = flatten(samples, n_neigh)
    print(f"Pooled design matrix: {X_all.shape[0]} rows x {X_all.shape[1]} columns "
          f"({samples.n_feat} node features + node id)")

    train_rows = set(positions_to_rows(samples, split.train))
    val_rows = set(positions_to_rows(samples, split.val))
    test_rows = positions_to_rows(samples, split.test)

    records: list[dict] = []
    with track_emissions(run_tag(args.name, args.variant, window),
                         enabled=not args.no_carbon) as carbon:
        for h_idx, horizon in enumerate(window.horizons):
            # Targets in RATE units, so the climatology offset is interpretable.
            y_rate = np.full(len(meta), np.nan, dtype=np.float64)
            base = np.zeros(len(meta), dtype=np.float64)
            for r, (s, node) in enumerate(meta):
                position = samples.positions[s]
                actual = norm.to_level(samples.y[s:s + 1])[0, node, h_idx]
                y_rate[r] = actual
                base[r] = clim_rate[position + horizon, node]

            target = y_rate - base if args.target == "climatology" else y_rate
            observed = np.isfinite(target)

            def mask(rowset):
                idx = [r for r, (s, _) in enumerate(meta) if s in rowset]
                return [r for r in idx if observed[r]]

            tr, va = mask(train_rows), mask(val_rows)
            model = xgb.XGBRegressor(**{**DEFAULT_PARAMS,
                                        "n_estimators": args.n_estimators,
                                        "random_state": args.seed,
                                        "early_stopping_rounds": 50})
            model.fit(X_all[tr], target[tr], eval_set=[(X_all[va], target[va])], verbose=False)
            best = model.best_iteration
            print(f"  h={horizon}: best_iteration={best} of {args.n_estimators}, "
                  f"val RMSE={model.best_score:.4f}")

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

            prediction = model.predict(X_all)
            if args.target == "climatology":
                prediction = prediction + base
            prediction = np.maximum(prediction, 0.0)

            # Intervals from the shared recipe, fitted on validation only, so the
            # bands are comparable with every other model in the repository.
            va_all = [r for r, (s, _) in enumerate(meta) if s in val_rows and observed[r]]
            horizon_col = np.full(len(va_all), horizon)
            interval = fit_intervals(prediction[va_all], y_rate[va_all], horizon_col,
                                     two_sided=args.two_sided_intervals)
            lower, upper = interval.bounds(prediction, np.full(len(meta), horizon))

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
            "params": {**DEFAULT_PARAMS, "n_estimators": args.n_estimators,
                       "random_state": args.seed},
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
    )


if __name__ == "__main__":
    main()
