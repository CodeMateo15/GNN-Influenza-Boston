# Chicago data notes

What the fourth city's data is, where it comes from, and where it does not line
up with the other three. Same spirit as `AMBA_DATA_NOTES.md`: differences are
recorded, not smoothed over.

## 1. Source and terms

* **Series:** Chicago Department of Public Health, *Influenza Risk Level by ZIP
  Code*, City of Chicago Data Portal dataset
  [`8vvr-jv2g`](https://data.cityofchicago.org/d/8vvr-jv2g), compiled from
  Illinois ESSENCE emergency-department syndromic surveillance.
* **Polygons:** *Boundaries - ZIP Codes*,
  [`unjd-c2ca`](https://data.cityofchicago.org/d/unjd-c2ca).
* Both are keyless Socrata endpoints. Use is governed by the City of Chicago
  Data Portal terms and disclaimer
  (<https://www.chicago.gov/city/en/narr/foia/data_disclaimer.html>); the
  portal marks the data provisional. The raw table used is kept at
  `Data/Chicago/source/8vvr-jv2g.csv`.

Build: `build_chicago_panel.py` (add `--download` to refetch) →
`derive_chicago_adjacency.py` → `scrape_acs_chicago.py` (needs
`CENSUS_API_KEY`) → `scrape_weather_chicago.py`.

## 2. The target is an index, not a rate

Each value is an **ILI activity level from 1 to 10**: a ZIP's percent of ED
visits for ILI against that same ZIP's summer mean. Level 1 is at or below the
summer mean and each level after that is roughly one more standard deviation
above it, **capped at 10**. Consequences:

* No count and no denominator. The loader passes the level through as-is, so
  MAE, RMSE and WIS for Chicago are in **levels**, not per 100,000, and are not
  comparable in size with the other cities. Correlation-type metrics are.
* **The cap flattens peaks.** 13% of ZIP-weeks sit at 10, and a strong season
  is a plateau of 10s, so "peak week" picks the first week of the plateau and
  peak height carries no information above the cap. Trust timing measures
  built on the whole curve (lag, weeks behind) over peak offsets.
* The baseline is each ZIP's own summer, so levels compare a ZIP with itself.
  Two ZIPs at the same level are not at the same absolute ILI share.
* There is no honest city-wide covariate (a sum of indices is not a count), so
  `available_globals` is empty.

## 3. Gaps

The portal publishes 346 of the 365 weeks from 2019-09-29 to 2026-09-20. All 19
missing weeks are May–September 2020, when the whole city is absent. The panel
keeps a complete weekly grid with those weeks as NaN, and treats any absent
ZIP-week as missing rather than zero (`suppresses_small_counts=True`). After
2022-07-01 (the `post_covid` variant) the 58 scored ZIPs are 100% complete.

### Flat series in the 2022-23 fold (fixed 2026-10-11)

ZIP 60707 reported level 1 in every week before June 2022, and 60827 did the
same from when it joined in September 2020. In the 2022-23 fold, 60707's
training standard deviation is therefore exactly 0. The shared scalers
(`influenza/windows.py: normalization` and `influenza/samples.py: _zscore`)
divided by `std + 1e-8`, so the first non-1 test week became about 9e8. That
produced:

- Cola-GNN and GAT forecasts in the millions;
- degraded LSTM and Dual-Topo forecasts;
- the graph model receiving the value through its neighbours, while the no-map
  version did not.

**Fix:** `safe_scale` scales a column with std ≤ 1e-6 by 1. Any column with
spread keeps the old `std + 1e-8` bit for bit, so no Boston or Columbus fold
changes. A scan of every city and fold found no other zero-spread column.

**Reruns:** every learned Chicago 2022-23 run, including that fold's tuning,
was rerun with the fix (jobs 10985373 and 10985374, then finals). The
pre-fix outputs are kept on Explorer as `*.prefix_2026-10-11`.

## 4. Node set: 58 scored, 1 anchor

ZIP **60106** (Bensenville, mostly outside the city) has rows but no polygon,
so it is dropped. Its series is also the thinnest in the table (14% coverage).

The remaining 59 are split by the Buenos Aires coverage rule unchanged, ≥90% of
panel weeks reported. It makes one anchor, **60827** (Riverdale / Calumet Park,
southern city limit, 0.858), which only joined the feed in September 2020.
Measured over `post_covid` alone it would be complete and scored. The rule was
kept as Buenos Aires defines it rather than tuned per city. (The code would
also run with no anchors: graphs, samples and training all slice on `n_neigh`,
and the anchor-edge check passes at 0 == 0.)

**O'Hare (60666)** is a scored node. It has no residents and no Census ZCTA, so
its demographics are filled with the city median. It touches the rest of the
city through one short border (to 60656), so its only graph edge is that one.

## 5. Graph, centroids and weather

`derive_chicago_adjacency.py` applies the shared-boundary rule (≥2 shared
vertices) and finds **115 borders** among the 59 ZIPs. The count is the same at
4–7 decimals. That leaves 113 edges between scored ZIPs and 2 to the anchor.
The same script writes area-weighted centroids, and flags **36 city-edge
ZIPs** (35 of them scored) with more than 1 km of perimeter that borders no
other ZIP. Those drain to the `Outside` node under the `single` anchor scheme.
The lakefront counts as outside.

Weather comes from Open-Meteo with the shared fetcher and aggregation. The 59
centroids fall in **12 archive grid cells**, so the scraper fetches each cell
once. Chicago's weather therefore has only 12 distinct series across 58 nodes.

## 6. Variants and evaluation

* `post_covid` is the modelling variant, as in every city.
* `full` is allowed, and it is the backtest variant (as in Boston), because it
  is the only variant that can train the 2022-23 fold. The pre-2022 history is
  half a pre-COVID season, the COVID years and the 2020 gap.
* Backtest evidence folds are 2022-23 through 2025-26, with **no development
  season**: nothing was tuned on Chicago.
* The test window is the shared 2025-05-31 to 2026-05-31.

## 7. Demographics

All eight `STATIC_DEMO_COLS` come from the ACS 2023 5-year estimates, per ZCTA,
using the variable definitions from `scrape_acs_columbus.py`. Land area is
`shape_area` from the City polygons. They exist because four frozen backtest
arms (`gnn_st`, `gnn_st_nograph`, `xgboost`, `xgboost_parity`) read them. The
ablations elsewhere found them inert.
