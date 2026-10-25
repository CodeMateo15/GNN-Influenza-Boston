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
| gnn_st_nodemofeat_tuned | 52 | 0.01 [-0.02, 0.02] | -0.01 [-0.02, -0.00] | -0.00 [-0.01, 0.00] | -0.001 [-0.004, 0.001] | 0.656 | 0.187 | not distinguishable |
| gnn_st_noweather_tuned | 52 | 0.00 [-0.02, 0.01] | 0.02 [0.01, 0.04] | 0.01 [0.00, 0.01] | -0.007 [-0.011, -0.004] | 0.994 | 0.027 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.13 [-0.25, -0.04] | -0.18 [-0.32, -0.07] | -0.08 [-0.12, -0.04] | 0.068 [0.040, 0.107] | 0.002 | 0.000 | reference better |
| gnn_st_historyonly_tuned | 52 | -0.17 [-0.32, -0.06] | -0.19 [-0.29, -0.10] | -0.09 [-0.13, -0.06] | 0.063 [0.050, 0.093] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_noweather_tuned | 0.798 |
| transfer_finetune_from_boston | 0.800 |
| transfer_finetune_from_pooled_all3 | 0.800 |
| transfer_finetune_from_pooled_others | 0.801 |
| gnn_st_noadapt | 0.802 |
| gnn_st | 0.803 |
| gnn_st_tuned | 0.803 |
| gnn_st_nodemofeat_tuned | 0.805 |
| transfer_zeroshot_from_pooled_all3 | 0.810 |
| gat_tuned | 0.827 |
| colagnn_tuned | 0.827 |
| gat_parity | 0.833 |
| transfer_zeroshot_from_pooled_others | 0.841 |
| lstm | 0.844 |
| lstm_s10 | 0.849 |
| lstm_tuned | 0.849 |
| transfer_zeroshot_from_boston | 0.856 |
| gnn_st_nograph_tuned | 0.858 |
| gnn_st_nograph | 0.864 |
| gnn_st_historyonly_tuned | 0.868 |
| dualtopo_tuned | 0.869 |
| xgboost_parity | 0.890 |
| xgboost_tuned | 0.896 |
| xgboost | 0.899 |
| sarima | 0.919 |
| arima | 0.922 |
| blend_baseline | 0.948 |
| lstm_parity | 0.968 |
| flusight_baseline | 0.979 |
| persistence | 1.000 |
| climatology | 1.113 |
| seasonal_naive | 1.161 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
