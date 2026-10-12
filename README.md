# GNN-Influenza-Boston

Week-ahead forecasting of influenza-like illness (ILI) emergency-department visit
rates for the 14 neighborhoods of Boston, framed as a problem on a graph. The
question the project asks is whether the structure *connecting* neighborhoods —
shared borders, correlated histories, similar demographics —
carries forecasting signal beyond each neighborhood's own history.

## Status: work in progress

This is an active research repository, not a finished result or a stable tool.

- Numbers move as data defects are found and corrected. Five more were found in
  September 2026 and are recorded as defects 5-9 in
  [Data notes](Code/docs/DATA_NOTES.md); two of them were the largest single
  source of error in the graph models, and fixing them moved the then-current
  graph arm from RMSE 24.90 to 19.12 at one week ahead with no model change at
  all.
- **On seasons its design never saw** (a rolling-origin backtest, 2022-25, with
  every learned model tuned the same way on validation weeks only), adding the
  graph reliably improves the graph model (`gnn_st`) in Boston: it beats the
  same model without the graph at one week in all three seasons, and at two and
  four weeks in two of three. It does **not** reliably beat the best tuned
  non-graph models. It ties a tuned LSTM and a tuned Cola-GNN at one week, and
  leads them at two and four weeks in direction, but clearly in only one season
  of three against the LSTM and never against Cola-GNN. In Columbus it leads only at one week. In Buenos Aires it cannot be
  told apart from persistence. Its forecast error (weighted interval score) is
  18-28% below persistence's in Boston. See
  [Methods § With every model tuned](Code/docs/METHODS.md#with-every-model-tuned-the-same-way).
- **The pipeline ports by data alone.** A city is a profile (nodes, season,
  loader) and a graph derived from boundary polygons. Boston's hand-drawn map
  was ~85% right, and the models score the same on polygon-derived maps (33 of
  36 week-level comparisons tied). A model trained on Boston and applied to
  Columbus with no local training matches one trained on Columbus, and a
  zero-shot model's error is below persistence's in every case tested. The graph's
  *advantage*, though, is Boston-specific. See
  [Methods § Portability](Code/docs/METHODS.md#portability-does-the-model-need-a-hand-drawn-map-and-does-it-travel).
- **A measured ceiling bounds all of it.** Distributing a *perfect* citywide
  forecast across neighborhoods by their historical shares scores macro Corr
  0.938. Boston's neighborhoods co-move almost completely, so correlations here
  should be read against 0.94, not 1.0 — and macro Corr of 0.90 at two to four
  weeks ahead is not reachable on this data. See
  [Methods](Code/docs/METHODS.md#how-good-can-any-model-get-here-a-measured-ceiling).
- Script flags, feature sets and result layouts still change without notice.

## Data

Weekly resolution, 2017-12-31 through 2026-05, over Boston's 14 BPHC
neighborhoods plus 7 non-scored "anchor" nodes standing in for the surrounding
area (Cambridge/Somerville, Brookline, Chelsea/Revere/Winthrop, the suburbs, and
the water between them).

| Source | What it is |
| --- | --- |
| `Data/BPHC Flu Data/` | **The target series.** Boston Public Health Commission dashboard exports: weekly ILI ED-visit rates per 100,000 by neighborhood (436 weeks, 2017-12-31 → 2026-05-03), plus citywide counts, ILI as a share of ED visits, monthly demographics, and daily flu wastewater by sewershed (2024-08 on). |
| `Data/BPHC Covid and RSV Data/` | Monthly neighborhood COVID cases and testing, confirmed RSV cases, and COVID/RSV wastewater. Optional covariates. |
| `Data/Weather/` | Weekly weather per neighborhood — temperature, humidity, precipitation, wind (438 weeks, 2017-12-31 → 2026-05-17). Scraped by `Code/scrapers/scrape_weather.py`. |
| `Data/Neighborhood Data/` | 22 Boston Indicators / BPDA tables (population, age, poverty, commute mode, housing, education, labor force, …), reduced to eight static per-neighborhood features. |
| `Data/Mass Flu Vaccination Data/` | Massachusetts dashboard flu vaccination workbooks, 2023-24 through 2025-26. Optional feature. |

### Third city: Buenos Aires (AMBA)

19 partidos of the Buenos Aires conurbano, from Argentina's national
respiratory surveillance (SNVS) with INDEC 2022 census denominators. Southern
Hemisphere (flu season April–September) with its own evaluation window,
because the feed backfills for about four months. Details in
[AMBA data notes](Code/docs/AMBA_DATA_NOTES.md).

### Second city: Columbus OH

Boston's findings rest on one city and one test season, so a second
city is being added to test whether the *model ordering* reproduces — not
whether Columbus forecasts better. Franklin County publishes ILI
emergency-department surveillance at a sub-city geography with enough history to
reach Boston's evaluation window.

| Source | What it is |
| --- | --- |
| `Data/Columbus Influenza Data/` | Weekly counts per area for **17 areas** and 238 contiguous weeks (2022-01-02 → 2026-07-19): ILI ED visits, flu hospitalisations and COVID cases (`columbus_*_weekly_counts.csv`), plus a ZIP→area crosswalk. They are aggregated by `Code/scrapers/build_columbus_panel.py` from three line-level Columbus Public Health extracts (one row per visit or case, keyed to home ZIP), which are kept private to the project and are not in this repository. |
| `Data/Columbus Weather/` | Weekly weather per area, from the same Open-Meteo endpoint as Boston's. Generated by `Code/scrapers/scrape_weather_columbus.py`. |

Unlike Boston's, the Columbus target is **constructed**: the extracts carry no
rate and no population denominator. Read
[Columbus data notes](Code/docs/COLUMBUS_DATA_NOTES.md) before using any of it —
in particular, Columbus zeros are real observations whereas Boston's missing
weeks are suppression, so `n_obs` and MAPE are not comparable across the cities.

Verify the layer with `python Code/run_columbus_data_check.py`.

## Data availability

- **Boston:** rates are published by the Boston Public Health Commission
  (public dashboard).
- **Buenos Aires:** data are published by Argentina's Ministry of Health (SNVS).
- **Columbus:** the data were provided by Columbus Public Health as
  de-identified visit-level extracts. With their agreement, the weekly
  area-level counts used in every analysis are public in this repository. The
  visit-level extracts are available from Columbus Public Health on request.
- **Weather:** Open-Meteo (CC BY 4.0).
- **Boundaries:** the City of Boston, the US Census Bureau and Argentina's
  Instituto Geográfico Nacional.

The forecasting models are also released as an installable package for health
departments,
[areaFluForecast](https://github.com/CodeMateo15/areaFluForecast).

## Quickstart

```bash
pip install -r requirements.txt
python Code/run_arima.py --variant post_covid          # a cheap baseline
python Code/run_gnn.py   --experiment gnn_st          # the current model
```

## More detail

- [Methods, results and limitations](Code/docs/METHODS.md) — models, evaluation, leaderboards, what the numbers actually say
- [Data notes](Code/docs/DATA_NOTES.md) — per-file quirks and known defects
- [Columbus data notes](Code/docs/COLUMBUS_DATA_NOTES.md) — the second city: sources, the 17-area geography, and where it cannot match Boston
- [Graph design](Code/docs/EDGES_AND_NODES_NOTES.txt) — nodes, edge types, weighting
- [Severity bands](Code/docs/SEVERITY.md) · [Rt caveats](Code/docs/RT_CAVEATS.md)
