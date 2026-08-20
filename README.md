# GNN-Influenza-Boston

Week-ahead forecasting of influenza-like illness (ILI) emergency-department visit
rates for the 14 neighborhoods of Boston, framed as a problem on a graph. The
question the project asks is whether the structure *connecting* neighborhoods —
shared borders, correlated histories, similar demographics, transit flows —
carries forecasting signal beyond each neighborhood's own history.

## Status: work in progress

This is an active research repository, not a finished result or a stable tool.

- The graph models do not yet beat simple baselines at one week ahead.
- Numbers move as data defects are found and corrected.
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
| `Data/MBTA/` | March 2026 GTFS feed, transit ridership edges between neighborhoods derived from it, a 14×14 adjacency matrix, and neighborhood boundary GeoJSON. |
| `Data/Neighborhood Data/` | 22 Boston Indicators / BPDA tables (population, age, poverty, commute mode, housing, education, labor force, …), reduced to eight static per-neighborhood features. |
| `Data/Mass Flu Vaccination Data/` | Massachusetts dashboard flu vaccination workbooks, 2023-24 through 2025-26. Optional feature. |

`Data/Weather copy/` is a stale snapshot that nothing reads — ignore it.

## Quickstart

```bash
pip install -r requirements.txt
python Code/run_arima.py --variant post_covid
```

## More detail

- [Methods, results and limitations](Code/docs/METHODS.md) — models, evaluation, leaderboards, what the numbers actually say
- [Data notes](Code/docs/DATA_NOTES.md) — per-file quirks and known defects
- [Graph design](Code/docs/EDGES_AND_NODES_NOTES.txt) — nodes, edge types, weighting
- [Severity bands](Code/docs/SEVERITY.md) · [Rt caveats](Code/docs/RT_CAVEATS.md)
- [Transit edge methodology](Data/MBTA/README_mbta_edges.txt)
