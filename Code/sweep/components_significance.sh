#!/bin/bash
# Week-level tests for the component ablations (Code/results/_components/README.md).
# Two Holm families per season x horizon: gnn_st_tuned vs its 4 component
# removals, and the history-only version vs the history-only baselines + LSTM.
# Run from anywhere: bash Code/sweep/components_significance.sh
cd "$(dirname "$0")/../.."
PY=${PYTHON:-python}
COMP=gnn_st_noweather_tuned,gnn_st_nodemofeat_tuned,gnn_st_nograph_tuned,gnn_st_historyonly_tuned
HIST=blend_baseline,sarima,persistence,flusight_baseline,lstm_tuned
for spec in "boston:full:2022_23 2023_24 2024_25" "columbus:post_covid:2024_25" "chicago:full:2022_23 2023_24 2024_25 2025_26"; do
  city=${spec%%:*}; rest=${spec#*:}; variant=${rest%%:*}; seasons=${rest#*:}
  for s in $seasons; do
    if [ $city = boston ]; then dir=Code/results/backtest_$s; else dir=Code/results/$city/backtest_$s; fi
    $PY -u Code/compare_significance.py --city $city --results-dir $dir --variant $variant --reference gnn_st_tuned --models $COMP --tag components
    $PY -u Code/compare_significance.py --city $city --results-dir $dir --variant $variant --reference gnn_st_historyonly_tuned --models $HIST --tag historyonly
  done
done
echo "Outputs: significance_components / significance_historyonly under each backtest_<s>/horizon_<hh>/_comparison/"
