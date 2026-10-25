# Component ablations on the unseen seasons

What each kind of information adds to `gnn_st`, measured on the unseen test
seasons with the same equal-budget tuning as the map ablation. Paper:
`Paper/overleaf_v2/main.txt`, Results "What each component adds", Table 3,
Figure 4; Appendix S1 tables `tab:components` and `tab:historyonly`.

## Arms

| Component removed | Arm (`Code/influenza/config.py`) | Differs from `gnn_st` by |
|---|---|---|
| Environment | `gnn_st_noweather` | `use_weather=False` |
| Demographics | `gnn_st_nodemofeat` | `use_demographics=False` (demographic *links* kept; they belong to the map) |
| Map | `gnn_st_nograph` | no geo/corr/demo edges, no anchors, `adaptive=False` (already run for the paper) |
| All three | `gnn_st_historyonly` | `gnn_st_lagsonly` features (no weather, demographics, suppression flag, calendar, globals) on `gnn_st_nograph`'s graph |

Every arm keeps the blended baseline (`target="blend"`). Each was tuned with
`Code/tune.py`: 12 configurations per city, fold and horizon, picked on
validation MAE, then retrained with 10 seeds (`<arm>_tuned`).

## Commands

```bash
# Stage 1: 12 one-seed configurations per cell (864 tasks)
python Code/tune.py list --arms gnn_st_noweather,gnn_st_nodemofeat,gnn_st_historyonly \
    --cities boston,columbus,chicago --out Code/sweep/tasks_tune_components.jsonl
sbatch --export=ALL,CHUNK=4,TASKS=Code/sweep/tasks_tune_components.jsonl \
    --array=0-215%50 Code/sweep/array.sbatch
# Pick per cell (merges into Code/sweep/tuned_configs.json) and write the finals
python Code/tune.py select --arms gnn_st_noweather,gnn_st_nodemofeat,gnn_st_historyonly \
    --cities boston,columbus,chicago
python Code/tune.py finals --arms gnn_st_noweather,gnn_st_nodemofeat,gnn_st_historyonly \
    --cities boston,columbus,chicago --out Code/sweep/tasks_tuned_final_components.jsonl --chunk 1
sbatch --export=ALL,CHUNK=1,TASKS=Code/sweep/tasks_tuned_final_components.jsonl \
    --array=0-71%50 Code/sweep/array.sbatch
# Collect, then the week-level tests (2 Holm families per season x horizon)
for c in boston columbus chicago; do python Code/run_backtest.py --city $c --collect-only; done
bash Code/sweep/components_significance.sh
```

Outputs: `<arm>_tuned/` under each `[city/]backtest_<s>/horizon_<hh>/`, and
`_comparison/significance_components.{csv,md}` (reference `gnn_st_tuned`) and
`_comparison/significance_historyonly.{csv,md}` (reference
`gnn_st_historyonly_tuned` vs `blend_baseline`, `sarima`, `persistence`,
`flusight_baseline`, `lstm_tuned`).

## Data provenance (read before re-running Boston)

The Boston reference runs the paper reports (`gnn_st_tuned`,
`gnn_st_nograph_tuned`, every baseline; created 2026-09-25) were scored against
the BPHC neighborhood file as of commit `57a26397`. BPHC later revised 5 weekly
values before June 2025, and the revised file is what the repository has from
commit `d8ff652d` on:

| Neighborhood | Week starting | `57a26397` | revised |
|---|---|---|---|
| Dorchester (02122, 02124) | 2018-08-19 | 24.6 | 26.8 |
| Jamaica Plain | 2018-03-04 | 15.3 | 13.6 |
| East Boston | 2022-10-16 | 10.9 | 12.5 |
| Jamaica Plain | 2022-11-13 | 20.4 | 22.1 |
| South Boston | 2022-11-13 | 12.7 | 10.6 |

The first pass of the component arms ran against the revised file (Explorer's
copy was refreshed 2026-10-13) and failed `compare_significance.py`'s
same-observations check on Boston 2022-23. The Boston component arms were
therefore re-run, tuning and finals, in a separate Explorer root
(`/scratch/$USER/gnn-flu-june`, `GNNFLU_ROOT` in `array.sbatch`) whose
`Data/BPHC Flu Data/` holds the `57a26397` files and whose other data folders
link to the main root. Boston weather in the two versions is identical before
June 2025. Task list: `Code/sweep/tasks_tune_components_boston_june.jsonl`,
then `select`/`finals` in that root.

Columbus and Chicago component runs used the main root. Their test-season
observed values match the reference runs in every cell (all 3 horizons, every
unseen season), which `compare_significance.py` checks.

To reproduce the Boston numbers from the repository, check out the BPHC files
at `57a26397` first:

```bash
git checkout 57a26397 -- "Data/BPHC Flu Data/"
```
