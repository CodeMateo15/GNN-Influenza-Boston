# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 1, `full`

Each row asks: on the weeks of this test season, is the reference model's error
really lower than this model's, or could the gap come from which weeks the season
happened to contain? Differences are **reference minus other**, so for MAE, RMSE
and WIS a negative number means the reference is better; for Corr, positive does.
The bracket is a 95% confidence interval from resampling whole weeks in blocks of
4 (all neighborhoods kept together inside a week). A gap whose interval crosses 0
is not distinguishable from chance on this season.

`p (MAE)` and `p (WIS)` are Diebold-Mariano tests on the weekly loss, Holm-adjusted
across the rows of this table. WIS scores the whole forecast distribution -- point
and spread together -- in rate per 100,000, lower is better. It is FluSight's
weighted interval score over 23 quantiles where both runs wrote them, else the
one-band version from the 95% interval (WIS-95); the column says which.

| other model | weeks | ΔMAE [95% CI] | ΔRMSE [95% CI] | ΔWIS [95% CI] | ΔCorr [95% CI] | p (MAE) | p (WIS) | verdict on MAE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_noweather_tuned | 53 | 0.03 [0.01, 0.04] | 0.01 [-0.00, 0.02] | 0.01 [0.00, 0.01] | -0.006 [-0.013, -0.004] | 0.000 | 0.021 | other better |
| gnn_st_nodemofeat_tuned | 53 | 0.01 [-0.00, 0.03] | 0.01 [-0.01, 0.02] | 0.00 [-0.01, 0.01] | -0.003 [-0.013, 0.002] | 0.018 | 0.554 | not distinguishable |
| gnn_st_historyonly_tuned | 53 | -0.12 [-0.24, -0.05] | -0.13 [-0.25, -0.05] | -0.08 [-0.12, -0.05] | 0.089 [0.051, 0.132] | 0.004 | 0.000 | reference better |
| gnn_st_nograph_tuned | 53 | -0.12 [-0.26, -0.04] | -0.17 [-0.35, -0.05] | -0.08 [-0.15, -0.04] | 0.103 [0.036, 0.171] | 0.006 | 0.002 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_noweather_tuned | 0.795 |
| gnn_st_nodemofeat_tuned | 0.799 |
| gnn_st | 0.801 |
| gnn_st_tuned | 0.801 |
| gnn_st_noadapt | 0.805 |
| transfer_finetune_from_boston | 0.805 |
| colagnn_tuned | 0.814 |
| lstm_tuned | 0.831 |
| lstm_s10 | 0.845 |
| transfer_zeroshot_from_boston | 0.853 |
| gat_tuned | 0.855 |
| gat_parity | 0.859 |
| lstm | 0.859 |
| gnn_st_nograph | 0.864 |
| gnn_st_historyonly_tuned | 0.865 |
| gnn_st_nograph_tuned | 0.866 |
| sarima | 0.878 |
| xgboost_tuned | 0.886 |
| xgboost_parity | 0.887 |
| dualtopo_tuned | 0.889 |
| xgboost | 0.897 |
| arima | 0.908 |
| blend_baseline | 0.919 |
| lstm_parity | 0.975 |
| flusight_baseline | 0.991 |
| persistence | 1.000 |
| climatology | 1.010 |
| seasonal_naive | 1.176 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
