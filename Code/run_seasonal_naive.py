"""Seasonal-naive baseline: predict each week with the same week one year ago.

The simplest thing that respects influenza's annual cycle, and the floor every
other model in this project has to clear. A model that cannot beat "last year,
same week" has not learned anything about influenza that a calendar doesn't
already know.

The lag-52 source week is always at least 52 weeks before the target and
therefore at or before the forecast origin, so nothing here uses future data.

    python Code/run_seasonal_naive.py --variant post_covid
"""

from __future__ import annotations

import argparse

try:
    import numpy as np
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install pandas numpy scipy matplotlib."
    ) from exc

from influenza import (
    Window,
    finish_run,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_variants, resolve_window, run_tag)
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals

SEASON_LAG_WEEKS = 52
NEAREST_TOLERANCE_WEEKS = 2

# Lag 1 is persistence ("same as last week"), which is a different claim from
# "same week last year" and deserves its own row in the leaderboard. It is the
# single most important reference here: a one-week-ahead forecaster that cannot
# beat persistence has not learned anything about influenza dynamics.
LAG_NAMES = {1: "persistence", 52: "seasonal_naive"}


def seasonal_prediction(
    series: pd.Series,
    target_date: pd.Timestamp,
    train_median: float,
    lag_weeks: int,
    horizon: int,
) -> tuple[float, str]:
    """Value from `lag_weeks` before `target_date`, with a documented fallback chain.

    The effective lag is `max(lag_weeks, horizon)`, because a forecast made at
    the origin cannot use any week later than the origin. Without that clamp,
    persistence (lag 1) at horizon 2 would read the week *after* the origin and
    score as well at two weeks ahead as at one -- a leak, not a result. The
    seasonal lag of 52 already exceeds any horizon here, so it is unaffected.

    Returns the prediction and which rule produced it, so the mix of exact
    lag hits versus fallbacks is auditable in predictions.csv.
    """
    source = target_date - pd.Timedelta(weeks=max(lag_weeks, horizon))
    if source in series.index:
        value = series.loc[source]
        if np.isfinite(value):
            return float(value), "lag"

    # The same week last year may itself have been suppressed. Look outward a
    # fortnight either side before giving up -- still all >= 50 weeks old.
    for offset in range(1, NEAREST_TOLERANCE_WEEKS + 1):
        for candidate in (source - pd.Timedelta(weeks=offset), source + pd.Timedelta(weeks=offset)):
            if candidate in series.index:
                value = series.loc[candidate]
                if np.isfinite(value):
                    return float(value), f"nearest{offset:+d}"

    return float(train_median), "train_median"


def run_variant(rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, checkpoint_root = city_output_dirs(args, city)
    data = variant_data(rates, variant)
    origins = valid_origins(data.index, window)
    split = split_origins(data.index, origins, window)
    lag_weeks = args.season_lag
    model_name = args.name or LAG_NAMES.get(lag_weeks, f"naive_lag{lag_weeks}")

    print(f"\n{'=' * 72}\n{model_name.upper()} (lag {lag_weeks} weeks) | {variant}\n{'=' * 72}")
    print(f"Train origins: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)}")
    first_target, last_target = split.test_target_span()
    print(f"Test targets: {first_target.date()} -> {last_target.date()}")

    # The lag source can predate the variant slice (a post-COVID target week in
    # 2025 looks back to 2024, which is inside the slice, but exclude_covid
    # targets can reach into a removed window), so index the full series.
    full = rates
    train_end = split.index[split.train[-1]]
    train_medians = full.loc[full.index <= train_end].median()

    def forecast(positions: list[int]) -> pd.DataFrame:
        rows: list[dict] = []
        for position in positions:
            for horizon in window.horizons:
                target_date = split.index[position + horizon]
                for neighborhood in city.node_names:
                    actual = float(data.available.at[target_date, neighborhood])
                    predicted, source = seasonal_prediction(
                        full[neighborhood], target_date,
                        float(train_medians[neighborhood]), lag_weeks, horizon,
                    )
                    predicted = max(0.0, predicted)
                    rows.append({
                        "origin_date": split.index[position],
                        "target_date": target_date,
                        "horizon": horizon,
                        "neighborhood": neighborhood,
                        "actual": actual,
                        "predicted": predicted,
                        "error": predicted - actual,
                        "source": source,
                    })
        return pd.DataFrame(rows)

    with track_emissions(run_tag(model_name, variant, window), enabled=not args.no_carbon) as carbon:
        validation = forecast(split.val)
        predictions = forecast(split.test)

    # Same interval recipe as every other model, fitted on the validation split.
    interval_model = fit_intervals(validation["predicted"], validation["actual"],
                                   validation["horizon"])
    predictions = attach_intervals(predictions, interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"],
                                  predictions["upper"])
    print(f"\n95% interval calibrated on {interval_model.n_validation} validation points; "
          f"test coverage {coverage:.1f}%")

    sources = predictions["source"].value_counts()
    print("\nPrediction sources:")
    for name, count in sources.items():
        print(f"  {name:14s} {count:5d} ({count / len(predictions) * 100:.1f}%)")

    finish_run(
        model=model_name,
        variant=variant,
        predictions=predictions,
        config={
            "target_kind": "level",
            "normalize": "none",
            "window": window.to_json(),
            "split": split.to_json(),
            "season_lag_weeks": lag_weeks,
            "nearest_tolerance_weeks": NEAREST_TOLERANCE_WEEKS,
            "prediction_sources": sources.to_dict(),
            "n_params": 0,
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
        title=f"{model_name} (lag {lag_weeks}w, {variant}) — horizon {window.min_horizon}",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--season-lag", type=int, default=SEASON_LAG_WEEKS,
                        help="Lag in weeks used as the prediction. 52 = same week last "
                             "year (seasonal naive); 1 = persistence.")
    parser.add_argument("--name", default=None,
                        help="Override the results directory name.")
    args = parser.parse_args()
    if args.season_lag < 1:
        parser.error("--season-lag must be positive")
    return args


def main() -> None:
    args = parse_args()
    window = resolve_window(args, Window())
    city = resolve_city(args)
    rates = city.loaders.load_rates()
    print(f"Loaded {len(rates)} weekly dates and {rates.shape[1]} neighborhoods")
    for variant in resolve_variants(args.variant):
        run_variant(rates, variant, window, args, city)


if __name__ == "__main__":
    main()
