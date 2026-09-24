"""Verify the Buenos Aires data layer before any model is trained on it.

    python -u Code/run_buenos_aires_data_check.py
    python -u Code/run_buenos_aires_data_check.py --strict

Same role as run_columbus_data_check.py: every assertion here is something that
would otherwise show up as a mysteriously bad metric three hours into a sweep.
A third city is where silent shape and alignment bugs live, and Buenos Aires
adds two failure modes the US cities do not have -- a hemisphere-flipped season
and a surveillance feed that backfills for months.

`--strict` turns warnings into failures.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.cities import get as get_city  # noqa: E402
from influenza.constants import WEATHER_COLS  # noqa: E402

PASS, FAIL, WARN = "pass", "FAIL", "warn"
_results: list[tuple[str, str, str]] = []


def check(name: str, condition: bool, detail: str = "", *, warn_only: bool = False) -> bool:
    status = PASS if condition else (WARN if warn_only else FAIL)
    _results.append((status, name, detail))
    marker = {PASS: "  ok ", FAIL: "FAIL ", WARN: "warn "}[status]
    print(f"{marker} {name}" + (f"  -- {detail}" if detail else ""), flush=True)
    return condition


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as failures.")
    args = parser.parse_args()

    city = get_city("buenos_aires")
    loaders = city.loaders

    print(f"\n{'=' * 72}\n{city.label} data check\n{'=' * 72}")

    # --- Node set -----------------------------------------------------------
    coverage = pd.read_csv(paths.AMBA_COVERAGE_FILE)
    check("19 scored partidos", city.n_neigh == 19, f"got {city.n_neigh}")
    check("5 anchor partidos", city.n_anchors == 5, f"got {city.n_anchors}")
    check("scored set is exactly the >=90%-coverage set",
          set(city.node_names) == set(coverage[coverage.keep_core].partido))
    check("no partido is both scored and an anchor",
          not (set(city.node_names) & set(city.anchor_names)))
    check("node order is alphabetical and therefore stable",
          list(city.node_names) == sorted(city.node_names))

    # --- Graph --------------------------------------------------------------
    known = set(city.short_names) | set(city.anchor_short) | {city.background_short}
    endpoints = {n for pair in (*city.geo_edges, *city.geo_edges_anchor,
                                *city.geo_edges_background) for n in pair}
    check("every edge endpoint is a known node", endpoints <= known,
          f"unknown: {sorted(endpoints - known)}")
    degree: dict[str, int] = {}
    for a, b in (*city.geo_edges, *city.geo_edges_anchor):
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1
    isolated = [s for s in city.short_names if degree.get(s, 0) == 0]
    check("no scored partido is isolated in the graph", not isolated, f"{isolated}")
    check("edge count matches the derived file",
          len(city.geo_edges) + len(city.geo_edges_anchor) == 48,
          f"got {len(city.geo_edges) + len(city.geo_edges_anchor)}")

    # --- Rates --------------------------------------------------------------
    rates = loaders.load_rates()
    check("rates are weeks x 19 partidos", rates.shape[1] == 19, f"{rates.shape}")
    check("rate columns are the scored nodes in order",
          list(rates.columns) == list(city.node_names))
    gaps = pd.Series(rates.index).diff().dropna().dt.days.unique()
    check("week grid is contiguous at 7 days", set(gaps) <= {7}, f"gaps {sorted(gaps)}")
    check("weeks start on Sunday", set(rates.index.dayofweek) == {6},
          f"dayofweek {sorted(set(rates.index.dayofweek))}")
    finite = rates.to_numpy(dtype=float)
    check("no negative rates", np.nanmin(finite) >= 0, f"min {np.nanmin(finite):.3f}")
    check("no infinities", not np.isinf(finite).any())
    nan_share = float(np.isnan(finite).mean())
    check("blackout share is small", nan_share < 0.10, f"{nan_share:.1%} NaN")
    check("blackouts are NaN, not zero -- matching the City flag",
          city.suppresses_small_counts and np.isnan(finite).any(),
          "a blackout must be missing data, not an observed zero")

    # --- Population denominator --------------------------------------------
    population = loaders.load_partido_population()
    check("every scored partido has an INDEC population",
          not population.reindex(city.node_names).isna().any())
    check("populations are plausible for the conurbano",
          bool(population.reindex(city.node_names).between(50_000, 2_500_000).all()),
          f"{int(population.min()):,}-{int(population.max()):,}")

    # --- Season: the whole reason this city is different --------------------
    citywide = rates.mean(axis=1)
    peaks = {year: group.idxmax() for year, group in citywide.groupby(citywide.index.year)
             if len(group) > 26}
    peak_weeks = {year: int(stamp.isocalendar().week) for year, stamp in peaks.items()}
    check("every full year peaks in epiweeks 18-28 (Southern season)",
          all(18 <= w <= 28 for w in peak_weeks.values()),
          ", ".join(f"{y}:SE{w}" for y, w in sorted(peak_weeks.items())))
    check("City.flu_months is April-September",
          city.flu_months == frozenset({4, 5, 6, 7, 8, 9}), f"{sorted(city.flu_months)}")
    in_season = citywide[citywide.index.month.isin(list(city.flu_months))].mean()
    off_season = citywide[~citywide.index.month.isin(list(city.flu_months))].mean()
    check("the declared season really is the high season",
          in_season > off_season * 1.5,
          f"in-season mean {in_season:.1f} vs off-season {off_season:.1f} per 100k")
    # The boundary must sit in the annual TROUGH, not at its exact argmin. The
    # trough here is flat -- December 19.8, January 20.9, February 20.8 per
    # 100,000, a 6% spread -- so which of the three is lowest is noise, and an
    # argmin test would fail or pass on a rounding difference. What actually
    # matters is that no observed week is split across two seasons, which any
    # month in the trough satisfies.
    monthly = citywide.groupby(citywide.index.month).mean()
    trough = set(monthly[monthly <= monthly.min() * 1.20].index.astype(int))
    check("season_start_month sits in the annual trough",
          city.season_start_month in trough,
          f"trough is months {sorted(trough)}, boundary is {city.season_start_month}")

    # --- Backfill trim ------------------------------------------------------
    raw = pd.read_csv(paths.AMBA_PANEL_FILE, parse_dates=["week_start"])
    check("the still-filling tail was trimmed",
          rates.index.max() < raw.week_start.max(),
          f"panel ends {raw.week_start.max().date()}, "
          f"rates end {rates.index.max().date()}")

    # --- Evaluation window --------------------------------------------------
    check("the city declares its own evaluation window",
          city.test_start is not None and city.test_end is not None)
    test_end = pd.Timestamp(city.test_end)
    check("the test window ends at or before the last complete week",
          test_end <= rates.index.max(),
          f"window ends {test_end.date()}, data ends {rates.index.max().date()}")
    window_weeks = rates.loc[pd.Timestamp(city.test_start):test_end]
    check("the test window is about a year", 50 <= len(window_weeks) <= 54,
          f"{len(window_weeks)} weeks")
    check("the test window contains a season peak",
          any(pd.Timestamp(city.test_start) <= p <= test_end for p in peaks.values()),
          f"peaks at {[str(p.date()) for p in peaks.values()]}")
    check("enough history remains to train on",
          int((rates.index < pd.Timestamp(city.test_start)).sum()) >= 100,
          f"{int((rates.index < pd.Timestamp(city.test_start)).sum())} weeks before the window")

    # --- Weather ------------------------------------------------------------
    weather = loaders.load_weather(rates.index)
    check("weather has all six shared columns",
          set(weather) == set(WEATHER_COLS), f"{sorted(weather)}")
    shapes = {k: v.shape for k, v in weather.items()}
    check("weather arrays are weeks x 19",
          all(s == (len(rates), 19) for s in shapes.values()),
          f"{sorted(set(shapes.values()))}")
    check("weather has no NaN after the median fill",
          not any(np.isnan(v).any() for v in weather.values()))
    # Southern hemisphere: July must be colder than January, or the
    # coordinates were entered with the sign flipped.
    temp = pd.Series(weather["temp_mean_c"].mean(axis=1), index=rates.index)
    july = temp[temp.index.month == 7].mean()
    january = temp[temp.index.month == 1].mean()
    check("July is colder than January (Southern hemisphere)", july < january,
          f"July {july:.1f}C vs January {january:.1f}C")

    # --- Demographics -------------------------------------------------------
    static, names, _ = loaders.load_static_demographics()
    check("demographics advertised as available", city.supports("demographics"))
    check("five demographic columns, named",
          names == ["pop_density", "poverty_rate", "pct_children", "pct_elderly",
                    "owner_rate"], f"{names}")
    check("static block is 19 partidos x 5", static.shape == (19, 5), f"{static.shape}")
    check("static block is min-max scaled with no NaN",
          not np.isnan(static).any() and static.min() == 0.0 and static.max() == 1.0)
    raw = pd.read_csv(paths.AMBA_STATIC_FILE, comment="#").set_index("partido")
    # Face validity: deprivation and age structure should run opposite ways
    # across the conurbano -- the poorer western and southern partidos are the
    # younger ones. A sign or column mix-up in the INDEC parse would break this.
    rho = raw["poverty_rate"].corr(raw["pct_elderly"], method="spearman")
    check("deprivation proxy runs opposite to the elderly share", rho < -0.5,
          f"Spearman {rho:.2f}")
    check("Vicente Lopez is the least deprived partido",
          raw["poverty_rate"].idxmin() == "VICENTE LÓPEZ",
          f"least deprived: {raw['poverty_rate'].idxmin()}")
    check("weather and seasonality are available",
          city.supports("weather") and city.supports("seasonality"))

    # --- Globals ------------------------------------------------------------
    globals_frame = loaders.load_globals(rates.index, ("ili_count",))
    check("ili_count global aligns with the week index",
          list(globals_frame.index) == list(rates.index))
    check("ili_count is positive where observed",
          float(np.nanmin(globals_frame["ili_count"].to_numpy())) >= 0)

    # --- Report -------------------------------------------------------------
    failed = [r for r in _results if r[0] == FAIL]
    warned = [r for r in _results if r[0] == WARN]
    print(f"\n{'=' * 72}")
    print(f"{len(_results) - len(failed) - len(warned)} passed, "
          f"{len(warned)} warned, {len(failed)} failed")
    print(f"Outputs: {paths.display(paths.AMBA_DIR, paths.ROOT)}")
    if failed or (args.strict and warned):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
