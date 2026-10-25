# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 2, `full`

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
| gnn_st_nodemofeat_tuned | 53 | 0.04 [0.00, 0.06] | 0.02 [-0.02, 0.06] | 0.01 [-0.01, 0.03] | -0.013 [-0.026, -0.001] | 0.066 | 1.000 | other better |
| gnn_st_noweather_tuned | 53 | 0.03 [0.01, 0.05] | -0.00 [-0.03, 0.03] | 0.00 [-0.01, 0.01] | -0.006 [-0.019, 0.001] | 0.020 | 1.000 | other better |
| gnn_st_nograph_tuned | 53 | -0.08 [-0.25, 0.02] | -0.16 [-0.38, -0.02] | -0.07 [-0.15, -0.02] | 0.113 [0.012, 0.195] | 0.199 | 0.093 | not distinguishable |
| gnn_st_historyonly_tuned | 53 | -0.09 [-0.20, -0.02] | -0.11 [-0.23, -0.01] | -0.07 [-0.11, -0.04] | 0.085 [0.014, 0.128] | 0.126 | 0.017 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_nodemofeat_tuned | 0.806 |
| gnn_st_noweather_tuned | 0.810 |
| transfer_finetune_from_boston | 0.810 |
| gnn_st | 0.811 |
| gnn_st_tuned | 0.811 |
| gnn_st_noadapt | 0.811 |
| colagnn_tuned | 0.824 |
| lstm_tuned | 0.849 |
| transfer_zeroshot_from_boston | 0.854 |
| gnn_st_historyonly_tuned | 0.865 |
| lstm_s10 | 0.866 |
| sarima | 0.866 |
| gnn_st_nograph_tuned | 0.867 |
| gnn_st_nograph | 0.867 |
| xgboost_tuned | 0.871 |
| lstm | 0.876 |
| xgboost_parity | 0.888 |
| xgboost | 0.893 |
| blend_baseline | 0.904 |
| arima | 0.915 |
| lstm_parity | 0.950 |
| climatology | 0.962 |
| flusight_baseline | 0.995 |
| persistence | 1.000 |
| seasonal_naive | 1.113 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
