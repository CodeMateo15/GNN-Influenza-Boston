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
| sarima | 52 | -0.04 [-0.10, 0.02] | -0.01 [-0.05, 0.05] | -0.01 [-0.04, 0.01] | -0.025 [-0.052, 0.006] | 0.333 | 0.427 | not distinguishable |
| blend_baseline | 52 | -0.06 [-0.14, 0.00] | -0.07 [-0.16, 0.01] | -0.02 [-0.05, 0.00] | 0.004 [-0.014, 0.023] | 0.210 | 0.193 | not distinguishable |
| lstm_tuned | 52 | -0.08 [-0.22, 0.04] | 0.01 [-0.17, 0.14] | -0.00 [-0.06, 0.05] | -0.076 [-0.136, -0.040] | 0.333 | 0.927 | not distinguishable |
| flusight_baseline | 52 | -0.27 [-0.39, -0.14] | -0.57 [-0.67, -0.44] | -0.24 [-0.34, -0.14] | 0.075 [0.040, 0.105] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.27 [-0.39, -0.14] | -0.57 [-0.67, -0.44] | -0.21 [-0.28, -0.13] | 0.075 [0.040, 0.105] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.817 |
| gnn_st_nodemofeat_tuned | 0.820 |
| gnn_st_tuned | 0.822 |
| gnn_st_noweather_tuned | 0.824 |
| colagnn_tuned | 0.840 |
| lstm_s10 | 0.850 |
| gnn_st_historyonly_tuned | 0.851 |
| lstm_tuned | 0.853 |
| xgboost_parity | 0.853 |
| lstm | 0.855 |
| sarima | 0.862 |
| gnn_st_nograph | 0.863 |
| gnn_st_nograph_tuned | 0.863 |
| xgboost | 0.864 |
| xgboost_tuned | 0.867 |
| blend_baseline | 0.868 |
| arima | 0.912 |
| climatology | 0.921 |
| lstm_parity | 0.939 |
| persistence | 1.000 |
| flusight_baseline | 1.023 |
| seasonal_naive | 1.178 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
