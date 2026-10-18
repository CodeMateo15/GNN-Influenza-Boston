"""A FluSight-style baseline: this week's value, with bands from past changes.

The CDC FluSight hub scores every team against a baseline whose median is the
most recent observation and whose spread comes from the history of how much the
series has moved. Relative WIS against it is how FluSight reports skill, so a
paper that uses FluSight's scoring rule should also show its reference model.

Here, per node and per forecast origin t:

  median     y_t, the latest observed rate (causally imputed through a
             suppressed week, as every model's inputs are);
  quantiles  y_t + the quantiles of the h-week changes y_s - y_{s-h} over all
             weeks s <= t, symmetrised by including each change's negative, so
             the band is centred on "no change" and widens with the horizon
             exactly as fast as this node's history says it should.

No parameters are fitted and nothing after t is read. The point forecast equals
`persistence`'s; only the distribution differs, so the two rows differ in WIS
and coverage but not in MAE or RMSE.

This follows the FluSight baseline's logic, not its code: FluSight works on
state-level admissions and simulates multi-week paths, whereas this uses the
h-week change directly, which gives the same spread for a random walk.

    python Code/run_flusight_baseline.py --variant post_covid --horizons 2
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from influenza import (
    Window,
    finish_run,
    impute_causal,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_variants, resolve_window, run_tag)
from influenza.intervals import QUANTILE_COLUMNS, QUANTILE_LEVELS, empirical_coverage

MODEL = "flusight_baseline"
# Fewer past changes than this and the quantiles are not worth quoting; the node
# falls back to the pooled changes of every node at that origin.
MIN_CHANGES = 20


def run_variant(rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, _ = city_output_dirs(args, city)
    data = variant_data(rates, variant)
    available = data.available
    origins = valid_origins(available.index, window)
    split = split_origins(available.index, origins, window)
    observed = available.to_numpy(dtype=np.float64)
    filled = impute_causal(available)[0].to_numpy(dtype=np.float64)
    levels = np.asarray(QUANTILE_LEVELS)

    print(f"\n{'=' * 72}\nFLUSIGHT-STYLE BASELINE | {city.label} | {variant}\n{'=' * 72}")
    rows: list[dict] = []
    fallbacks = 0
    with track_emissions(run_tag(MODEL, variant, window), enabled=not args.no_carbon,
                         city=city.name) as carbon:
        for position in split.test:
            for horizon in window.horizons:
                history = observed[:position + 1]
                changes = history[horizon:] - history[:-horizon]        # (weeks, nodes)
                pooled = changes[np.isfinite(changes)]
                pooled = np.concatenate([pooled, -pooled])
                for node, neighborhood in enumerate(city.node_names):
                    own = changes[:, node]
                    own = own[np.isfinite(own)]
                    if own.size >= MIN_CHANGES:
                        spread = np.concatenate([own, -own])
                    else:
                        spread, fallbacks = pooled, fallbacks + 1
                    median = filled[position, node]
                    q = np.maximum(median + np.quantile(spread, levels), 0.0)
                    q = np.maximum.accumulate(q)
                    target = position + horizon
                    actual = float(observed[target, node])
                    rows.append({
                        "origin_date": split.index[position],
                        "target_date": split.index[target],
                        "horizon": horizon,
                        "neighborhood": neighborhood,
                        "actual": actual,
                        "predicted": float(median),
                        "error": float(median) - actual,
                        "lower": float(q[list(QUANTILE_LEVELS).index(0.025)]),
                        "upper": float(q[list(QUANTILE_LEVELS).index(0.975)]),
                        **{name: float(v) for name, v in zip(QUANTILE_COLUMNS, q)},
                    })
    predictions = pd.DataFrame(rows)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"], predictions["upper"])
    print(f"95% band test coverage {coverage:.1f}% | node-origins on pooled changes: {fallbacks}")

    finish_run(
        model=MODEL,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": "level",
            "normalize": "none",
            "window": window.to_json(),
            "split": split.to_json(),
            "method": "median = latest observation; quantiles = latest + symmetrised "
                      "empirical h-week changes up to the origin",
            "min_changes_per_node": MIN_CHANGES,
            "pooled_fallbacks": fallbacks,
            "n_params": 0,
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
        title=f"{MODEL} ({variant}) — horizon {window.min_horizon}",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    city = resolve_city(args)
    window = resolve_window(args, Window(), city)
    rates = city.loaders.load_rates()
    for variant in resolve_variants(args.variant):
        run_variant(rates, variant, window, args, city)


if __name__ == "__main__":
    main()
