"""Two reference forecasts that need no learning: the seasonal curve, and its blend with persistence.

`gnn_st` does not predict the rate directly. It predicts a residual from a
baseline, s_h * (this week's rate) + (1 - s_h) * (the seasonal curve at the
target week), and at four weeks ahead most of its skill could be that baseline
rather than the network. Neither half was on the leaderboard, so there was no
way to tell. This writes both:

  climatology     the train-only harmonic seasonal curve of influenza/climatology.py,
                  per node, at the target week. Same fit, same cutoff, as the one
                  inside gnn_st, xgboost and the parity LSTM.
  blend_baseline  s_h * origin level + (1 - s_h) * climatology, with s_h the
                  least-squares share on the VALIDATION rows, clipped to [0, 1].
                  This is gnn_st's baseline with the network switched off.

If `gnn_st` cannot clearly beat `blend_baseline`, the network adds little over
the prior it starts from.

    python Code/run_climatology.py --variant post_covid --horizons 2
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
from influenza.climatology import fit_climatology
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals


def frame(split, positions, window, city, actual, clim_rate, origin_rate) -> pd.DataFrame:
    """Long-form rows with both components, so the blend can be formed afterwards."""
    rows: list[dict] = []
    for position in positions:
        for horizon in window.horizons:
            target = position + horizon
            for node, neighborhood in enumerate(city.node_names):
                rows.append({
                    "origin_date": split.index[position],
                    "target_date": split.index[target],
                    "horizon": horizon,
                    "neighborhood": neighborhood,
                    "actual": float(actual[target, node]),
                    "clim": float(clim_rate[target, node]),
                    "origin": float(origin_rate[position, node]),
                })
    return pd.DataFrame(rows)


def fit_share(validation: pd.DataFrame) -> dict[int, float]:
    """Per-horizon least-squares share of the origin level in y - clim = s (origin - clim)."""
    shares = {}
    for horizon, part in validation.groupby("horizon"):
        part = part[np.isfinite(part["actual"])]
        gap = (part["origin"] - part["clim"]).to_numpy()
        excess = (part["actual"] - part["clim"]).to_numpy()
        shares[int(horizon)] = float(np.clip(gap @ excess / max(gap @ gap, 1e-12), 0.0, 1.0))
    return shares


def run_variant(rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, _ = city_output_dirs(args, city)
    data = variant_data(rates, variant)
    available = data.available
    origins = valid_origins(available.index, window)
    split = split_origins(available.index, origins, window)

    climatology = fit_climatology(available, end=split.train[-1] + window.max_horizon + 1)
    clim_rate = climatology.level(available.index)
    origin_rate = impute_causal(available)[0].to_numpy(dtype=np.float64)
    actual = available.to_numpy(dtype=np.float64)

    print(f"\n{'=' * 72}\nCLIMATOLOGY + BLEND BASELINE | {variant}\n{'=' * 72}")
    print(f"Train origins: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")

    with track_emissions(run_tag("climatology", variant, window),
                         enabled=not args.no_carbon, city=city.name) as carbon:
        validation = frame(split, split.val, window, city, actual, clim_rate, origin_rate)
        test = frame(split, split.test, window, city, actual, clim_rate, origin_rate)
        shares = fit_share(validation)
    print("Origin-level share of the blend, fitted on validation: "
          + ", ".join(f"h={h}: {s:.3f}" for h, s in shares.items()))

    for name, predict in (
        ("climatology", lambda f: f["clim"]),
        ("blend_baseline", lambda f: f["horizon"].map(shares) * f["origin"]
                                     + (1.0 - f["horizon"].map(shares)) * f["clim"]),
    ):
        val_part = validation.assign(predicted=np.maximum(predict(validation), 0.0))
        test_part = test.assign(predicted=np.maximum(predict(test), 0.0))
        test_part["error"] = test_part["predicted"] - test_part["actual"]
        interval_model = fit_intervals(val_part["predicted"], val_part["actual"],
                                       val_part["horizon"],
                                       two_sided=args.two_sided_intervals)
        predictions = attach_intervals(test_part.drop(columns=["clim", "origin"]), interval_model)
        coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                      predictions["upper"])
        print(f"{name}: 95% interval test coverage {coverage:.1f}%")
        finish_run(
            model=name,
            variant=variant,
            predictions=predictions,
            config={
                "target_kind": "climatology" if name == "climatology" else "blend",
                "normalize": "none",
                "window": window.to_json(),
                "split": split.to_json(),
                "climatology": climatology.to_json(),
                **({"blend_share": {str(k): v for k, v in shares.items()},
                    "blend_share_fitted_on": "validation"} if name == "blend_baseline" else {}),
                "n_params": 0 if name == "climatology" else len(shares),
                "intervals": interval_model.to_json(),
                "test_interval_coverage": coverage,
            },
            bands=True,
            carbon=carbon,
            results_root=results_root,
            city=city,
            title=f"{name} ({variant}) — horizon {window.min_horizon}",
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
