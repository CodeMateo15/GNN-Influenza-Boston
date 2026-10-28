# Paper scripts: how every figure and table is made

Every figure in the paper is drawn by code in this folder with matplotlib, from
result files already in `Code/results/` and data in `Data/`. No figure is drawn by
hand or by an image generator, and nothing here retrains a model. To rebuild them,
run from the repository root:

```
/opt/anaconda3/bin/python Paper/scripts/make_figures.py              # all figures -> Paper/overleaf_v2/figures/
/opt/anaconda3/bin/python Paper/scripts/make_figures.py figure1      # one figure (function names match figure numbers)
/opt/anaconda3/bin/python Paper/scripts/make_severity.py             # Figure S5 and the severity table rows
/opt/anaconda3/bin/python Paper/scripts/make_tables.py > tables.txt  # LaTeX rows for the results tables
python3 Paper/scripts/make_inline.py                                 # main_inline.txt reading copy
```

Each figure is written as a PDF (vector, for submission) and a PNG (300 dpi).
`make_tables.py` prints table rows only. The captions and footnotes are in
`overleaf_v2/main.txt` and `supplement.txt`, and the rows are pasted in from its output.

Python environment: `Code/env/environment.yml`.

## Figures

| Figure | Script and function | Made from |
|---|---|---|
| 1A, Boston map | `make_figures.py`, `figure1()` | `Data/Neighborhood Data/boston_polygons_tract_neighborhoods.geojson` (shading, dots), `boston_edges_land.csv` (border lines), `GEO_EDGES_ANCHOR` in `Code/influenza/cities/boston.py` (water links). Fenway's dot is placed at Fenway Park. |
| 1B, timeline | `figure1()` | Season dates for each city, written in the function |
| 1C, model diagram | `figure1()`, `model_schematic()` | Boxes and arrows drawn in matplotlib |
| 2 | `figure2()` | `Code/results/{,columbus/,chicago/}_backtest/backtest.csv` |
| 3 | `figure3()` | `backtest_<season>/horizon_<hh>/_comparison/significance_tuned.csv` (from `Code/compare_significance.py`) |
| 4 | `figure4()` | `predictions.csv` of `gnn_st_tuned` and `persistence`, Boston |
| 5 | `figure5()` | `_comparison/significance_components.csv` (see `Code/results/_components/README.md`) |
| 6 | `figure6()`, `map_benefit()` | `predictions.csv` of the full and no-map models, by neighborhood, with the geojson above |
| S1 | `figure_s1_blend()` | `run_config.json` of each `gnn_st_tuned` run |
| S2 | `figure_s2_tuning()` | `Code/sweep/tuned_configs.json` |
| S3 | `figure_s3_pit()` | `predictions.csv` of `gnn_st_tuned`, Boston |
| S4 | `figure_s4_all_neighborhoods()` | `predictions.csv` of `gnn_st_tuned`, Boston |
| S5 | `make_severity.py`, `figure_s5()` | `Code/results/_severity_backtest/` (from `Code/compare_severity.py`) |
| S6 | `figure_s6_severity_confusion()` | `Code/results/_severity_backtest/boston/.../severity_bands.csv` |

## Tables

| Table | Source |
|---|---|
| 1, data and seasons | Written by hand from the data descriptions in `Data/` |
| 2 | `make_tables.py`, `main_table("boston")` |
| 3 | `make_tables.py`, `component_table()` |
| 4, maps | `make_tables.py`, `maps_table()`, from `Code/results/boston_geo_land/` and `boston_geo_tract/` |
| 5, transfer | `make_tables.py`, `transfer_table()` |
| S1, S2 | Descriptive, written by hand |
| S3, search spaces | `SEARCH` in `Code/tune.py` |
| S4–S6 | `make_tables.py`, `per_season()` |
| S7–S9 | `make_tables.py`, `significance()` |
| S10–S12 | `make_tables.py`, `point_metrics()` |
| S13, S14 | `make_severity.py`, `latex()` |
| S15 | `make_tables.py`, `component_significance("components")` |
| S16 | `make_tables.py`, `component_significance("historyonly")` |
| S17 | `make_tables.py`, `ablation_table()` |
| S18 | `make_tables.py`, `pooled_table()` |
| S19, compute | `Code/compare_compute.py --results-dir Code/results/backtest_2024_25 --variant full` writes `_compute/compute_table.tex`; the paper rounds it |

The result files themselves come from the model runs described in `Code/docs/`.
The task lists and settings for those runs are in `Code/sweep/`.
