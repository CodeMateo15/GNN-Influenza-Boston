#!/usr/bin/env python3
"""Forecast the severity band directly, instead of forecasting the rate.

Every other model here predicts a case rate, and compare_classification.py
bins that rate into CDC's four bands after the fact. This one is trained to
output the band itself -- low / moderate / high / very high, h weeks ahead --
so the two routes can be compared on the same metrics: is it better to classify
the week than to predict the number and then classify it?

Same inputs as `run_xgboost.py` (the `gnn_st` feature columns, one pooled model
over all neighborhoods with the node id as a feature), same split, same tree
settings. Only the target and the objective change.

    python Code/run_severity_classifier.py --variant post_covid --horizons 2 \
        --output-dir Code/results/horizon_02 --checkpoint-dir Code/checkpoints/horizon_02

Labels use the single citywide MEM cut points (`severity.citywide_thresholds`),
fitted on weeks before the test window. Outputs go to
`<output-dir>/_severity_classifier/<name>/<variant>/`; the leading underscore
keeps them out of compare_models.py and compare_severity.py, which expect a
rate forecast in every predictions.csv they find.
"""

from __future__ import annotations

# Thread pinning must happen before numpy is imported. See influenza/threads.py.
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
    raise SystemExit("run_severity_classifier.py needs xgboost. pip install xgboost") from exc

from influenza import paths, severity, split_origins, track_emissions, valid_origins, variant_data
from influenza.artifacts import git_sha
from influenza.classification import ALERT_LEVELS, band_confusion, band_scores
from influenza.cli import add_common_args, city_output_dirs, resolve_city, resolve_window, run_tag
from influenza.config import EXPERIMENTS
from influenza.samples import build_samples, load_dataset, positions_to_rows
from run_xgboost import DEFAULT_PARAMS, flatten

SUBDIR = "_severity_classifier"
N_BANDS = len(severity.SEVERITY_BANDS)
PROBABILITY_COLUMNS = [f"p_{band.replace(' ', '_')}" for band in severity.SEVERITY_BANDS]

CLASSIFIER_PARAMS = {**{k: v for k, v in DEFAULT_PARAMS.items() if k != "objective"},
                     "objective": "multi:softprob", "eval_metric": "mlogloss"}


def balanced_weights(labels: np.ndarray) -> np.ndarray:
    """Inverse class frequency, so each band carries equal total weight.

    Without it the model is rewarded for saying 'low' every week: 92% of
    training rows are low, and that alone scores 92% accuracy.
    """
    counts = np.bincount(labels, minlength=N_BANDS).astype(float)
    present = counts > 0
    weight = np.zeros(N_BANDS)
    weight[present] = labels.size / (present.sum() * counts[present])
    return weight[labels]


def fit_one(X, y, tr, va, *, seed: int, n_estimators: int, weighted: bool):
    """One booster; returns (probabilities over all rows, 4 columns, best val loss).

    XGBoost needs labels 0..K-1 with every one present, so a band absent from
    the training rows is dropped from the fit and its column padded with zero.
    Validation rows in such a band are dropped from early stopping for the same
    reason -- the model cannot be scored on a class it cannot output.
    """
    present = np.unique(y[tr])
    encode = {band: i for i, band in enumerate(present)}
    va = [r for r in va if y[r] in encode]
    y_tr = np.array([encode[b] for b in y[tr]])
    y_va = np.array([encode[b] for b in y[va]])
    model = xgb.XGBClassifier(**{**CLASSIFIER_PARAMS, "n_estimators": n_estimators,
                                 "random_state": seed, "early_stopping_rounds": 50})
    model.fit(X[tr], y_tr, sample_weight=balanced_weights(y[tr]) if weighted else None,
              eval_set=[(X[va], y_va)], verbose=False)
    probability = np.zeros((X.shape[0], N_BANDS))
    probability[:, present] = model.predict_proba(X)
    return model, probability, float(model.best_score)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("exclude_covid", "post_covid"))
    parser.set_defaults(variant="post_covid")
    parser.add_argument("--name", default="xgb_severity")
    parser.add_argument("--features-from", default="gnn_st",
                        help="Registry arm whose FeatureSpec supplies the columns.")
    parser.add_argument("--reference-seasons", default="post_covid",
                        choices=[k for k, v in severity.REFERENCE_SEASON_SETS.items() if v],
                        help="Seasons the citywide cut points are fitted on.")
    parser.add_argument("--class-weight", choices=("balanced", "none"), default="balanced")
    parser.add_argument("--n-estimators", type=int, default=DEFAULT_PARAMS["n_estimators"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-seeds", type=int, default=5,
                        help="Boosters per horizon; their probabilities are averaged.")
    args = parser.parse_args()
    if args.n_seeds < 1:
        raise SystemExit("--n-seeds must be at least 1")

    city = resolve_city(args)
    results_root, checkpoint_root = city_output_dirs(args, city)
    reference = EXPERIMENTS[args.features_from]
    window = resolve_window(args, reference.window, city)

    rates = city.loaders.load_rates()
    cuts = severity.citywide_thresholds(city, rates, reference_seasons=args.reference_seasons)
    data = variant_data(rates, args.variant)
    dataset = load_dataset(reference.features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)

    from influenza.graphs import build_graph
    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    static = dataset.static
    if reference.graph.demo and static is None:
        static = city.loaders.load_static_demographics()[0]
    graph = build_graph(reference.graph, city=city, flu_history=history, static=static)
    n_neigh = graph.n_neigh
    samples, norm = build_samples(dataset, split, reference.features, window, graph,
                                  target="level", normalize=reference.normalize)

    print(f"\n{'=' * 72}\n{city.label} | {args.name} | {args.variant} | "
          f"class_weight={args.class_weight}\n{'=' * 72}")
    print(f"Train {len(split.train)} | Validation {len(split.val)} | Test {len(split.test)} origins")
    print("Citywide cut points (MEM, fitted before "
          f"{cuts.fitted_through}): "
          + " | ".join(f"IT{l * 100:g} = {cuts.values[l]:.1f}" for l in cuts.levels))

    X_all, meta = flatten(samples, n_neigh)
    train_rows = set(positions_to_rows(samples, split.train))
    val_rows = set(positions_to_rows(samples, split.val))
    test_rows = set(positions_to_rows(samples, split.test))
    seeds = [args.seed + i for i in range(args.n_seeds)]

    # Status-line contract (run_progress.py): one "epoch" per fitted booster.
    total = len(window.horizons) * len(seeds)
    print(f"Budget: {total} epochs x 1 seeds", flush=True)

    records: list[dict] = []
    class_counts: dict[str, dict[str, list[int]]] = {}
    best_iterations: dict[str, list[int]] = {}
    step = 0
    with track_emissions(run_tag(args.name, args.variant, window),
                         enabled=not args.no_carbon) as carbon:
        for h_idx, horizon in enumerate(window.horizons):
            y_rate = np.array([norm.to_level(samples.y[s:s + 1])[0, node, h_idx]
                               for s, node in meta], dtype=np.float64)
            y_band = cuts.band(y_rate)
            observed = y_band >= 0

            def rows(rowset):
                return [r for r, (s, _) in enumerate(meta) if s in rowset and observed[r]]

            tr, va, te = rows(train_rows), rows(val_rows), rows(test_rows)
            class_counts[f"h{horizon}"] = {
                name: np.bincount(y_band[idx], minlength=N_BANDS).tolist()
                for name, idx in (("train", tr), ("val", va), ("test", te))}
            print(f"  h={horizon}: band counts (low/moderate/high/very high) "
                  + " | ".join(f"{k} {v}" for k, v in class_counts[f'h{horizon}'].items()))

            probability = np.zeros((len(meta), N_BANDS))
            best_iterations[f"h{horizon}"] = []
            for seed in seeds:
                model, member, loss = fit_one(X_all, y_band, tr, va, seed=seed,
                                              n_estimators=args.n_estimators,
                                              weighted=args.class_weight == "balanced")
                probability += member / len(seeds)
                best_iterations[f"h{horizon}"].append(int(model.best_iteration))
                step += 1
                print(f"Epoch {step} | h={horizon} seed={seed} val_mlogloss={loss:.4f} "
                      f"best_iteration={model.best_iteration}", flush=True)
                # Keep the first seed's booster, as run_xgboost keeps its one.
                if seed == seeds[0]:
                    path = checkpoint_root / f"{args.name}_{args.variant}_h{horizon:02d}.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    model.save_model(path)

            predicted = probability.argmax(axis=1)
            for r in te:
                s, node = meta[r]
                position = samples.positions[s]
                records.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[position + horizon],
                    "horizon": horizon,
                    "neighborhood": city.node_names[node],
                    "actual": float(y_rate[r]),
                    "true_band": int(y_band[r]),
                    "pred_band": int(predicted[r]),
                    **dict(zip(PROBABILITY_COLUMNS, probability[r].tolist())),
                })

    predictions = (pd.DataFrame(records)
                   .sort_values(["horizon", "target_date", "neighborhood"])
                   .reset_index(drop=True))

    metric_rows = []
    for horizon, part in predictions.groupby("horizon"):
        prob = part[PROBABILITY_COLUMNS].to_numpy()
        scores = {level: prob[:, level:].sum(axis=1) for level in ALERT_LEVELS}
        metric_rows.append({"model": args.name, "variant": args.variant,
                            "horizon": int(horizon),
                            **band_scores(part["true_band"], part["pred_band"], scores)})
        print(f"\nh={horizon} confusion (rows = actual, columns = forecast; "
              f"low / moderate / high / very high):")
        print(band_confusion(part["true_band"], part["pred_band"]))
    metrics = pd.DataFrame(metric_rows)

    out = results_root / SUBDIR / args.name / args.variant
    out.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(out / "predictions.csv", index=False)
    metrics.to_csv(out / "metrics.csv", index=False)
    config = {
        "model": args.name,
        "variant": args.variant,
        "git_sha": git_sha(),
        "created": pd.Timestamp.now().isoformat(timespec="seconds"),
        "model_class": "xgboost.XGBClassifier",
        "features_from": args.features_from,
        "window": window.to_json(),
        "split": split.to_json(),
        "params": {**CLASSIFIER_PARAMS, "n_estimators": args.n_estimators},
        "seeds": seeds,
        "best_iterations": best_iterations,
        "class_weight": args.class_weight,
        "cut_points": {f"IT{l * 100:g}": cuts.values[l] for l in cuts.levels},
        "cut_points_fitted_through": cuts.fitted_through,
        "reference_seasons": [severity.season_name(y) for y in cuts.reference_seasons],
        "class_counts": class_counts,
        "city": city.name,
    }
    (out / "run_config.json").write_text(json.dumps(config, indent=2, default=str) + "\n")

    with pd.option_context("display.width", 160, "display.max_columns", 30):
        print("\n" + metrics.round(3).to_string(index=False))
    if carbon is not None:
        print(carbon.format_report())
    print(f"Outputs: {paths.display(out)}", flush=True)


if __name__ == "__main__":
    main()
