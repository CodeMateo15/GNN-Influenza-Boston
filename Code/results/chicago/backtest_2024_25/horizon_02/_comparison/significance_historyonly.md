# Is `gnn_st_historyonly_tuned`'s lead bigger than chance? — horizon 2, `full`

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
| lstm_tuned | 52 | -0.01 [-0.08, 0.05] | 0.07 [-0.01, 0.15] | 0.02 [-0.03, 0.06] | -0.081 [-0.118, -0.052] | 0.756 | 0.439 | not distinguishable |
| flusight_baseline | 52 | -0.10 [-0.31, 0.14] | -0.60 [-0.77, -0.40] | -0.18 [-0.29, -0.07] | 0.071 [0.047, 0.107] | 0.756 | 0.001 | not distinguishable |
| persistence | 52 | -0.10 [-0.31, 0.14] | -0.60 [-0.77, -0.40] | -0.21 [-0.29, -0.12] | 0.071 [0.047, 0.107] | 0.756 | 0.000 | not distinguishable |
| sarima | 52 | -0.11 [-0.23, -0.03] | -0.07 [-0.22, 0.05] | -0.06 [-0.15, 0.01] | 0.012 [-0.037, 0.059] | 0.068 | 0.185 | reference better |
| blend_baseline | 52 | -0.20 [-0.47, -0.02] | -0.28 [-0.52, -0.09] | -0.11 [-0.21, -0.04] | 0.029 [0.001, 0.068] | 0.093 | 0.004 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_noweather_tuned | 0.786 |
| transfer_finetune_from_boston | 0.788 |
| transfer_finetune_from_pooled_others | 0.788 |
| gnn_st_noadapt | 0.792 |
| transfer_finetune_from_pooled_all3 | 0.795 |
| gnn_st_tuned | 0.800 |
| gnn_st | 0.801 |
| gnn_st_nodemofeat_tuned | 0.812 |
| transfer_zeroshot_from_pooled_all3 | 0.813 |
| colagnn_tuned | 0.820 |
| lstm_tuned | 0.843 |
| gnn_st_historyonly_tuned | 0.854 |
| gnn_st_nograph_tuned | 0.860 |
| transfer_zeroshot_from_pooled_others | 0.868 |
| transfer_zeroshot_from_boston | 0.872 |
| gnn_st_nograph | 0.873 |
| xgboost | 0.891 |
| xgboost_parity | 0.891 |
| sarima | 0.895 |
| xgboost_tuned | 0.896 |
| blend_baseline | 0.933 |
| lstm_s10 | 0.965 |
| arima | 0.968 |
| flusight_baseline | 0.982 |
| persistence | 1.000 |
| lstm | 1.010 |
| lstm_parity | 1.028 |
| climatology | 1.064 |
| seasonal_naive | 1.110 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
