# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 4, `full`

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
| sarima | 52 | 0.06 [-0.01, 0.13] | 0.04 [-0.01, 0.11] | 0.02 [-0.02, 0.07] | -0.032 [-0.086, 0.009] | 0.493 | 0.746 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.02 [-0.09, 0.05] | -0.10 [-0.18, -0.03] | -0.03 [-0.06, -0.00] | 0.042 [0.008, 0.069] | 1.000 | 0.290 | not distinguishable |
| blend_baseline | 52 | -0.03 [-0.15, 0.08] | -0.14 [-0.28, -0.03] | -0.01 [-0.04, 0.03] | 0.023 [-0.010, 0.053] | 1.000 | 0.746 | not distinguishable |
| xgboost_tuned | 52 | -0.05 [-0.15, 0.05] | -0.07 [-0.18, 0.03] | -0.04 [-0.09, -0.00] | -0.017 [-0.059, 0.022] | 1.000 | 0.295 | not distinguishable |
| lstm_tuned | 52 | -0.05 [-0.10, -0.01] | -0.15 [-0.20, -0.10] | -0.06 [-0.08, -0.04] | 0.062 [0.022, 0.093] | 0.153 | 0.000 | reference better |
| lstm_s10 | 52 | -0.20 [-0.32, -0.06] | -0.14 [-0.25, -0.02] | -0.06 [-0.12, 0.00] | 0.040 [-0.039, 0.095] | 0.041 | 0.295 | reference better |
| flusight_baseline | 52 | -0.37 [-0.58, -0.16] | -0.75 [-0.97, -0.55] | -0.30 [-0.48, -0.14] | 0.148 [0.065, 0.206] | 0.015 | 0.013 | reference better |
| persistence | 52 | -0.37 [-0.58, -0.16] | -0.75 [-0.97, -0.55] | -0.25 [-0.37, -0.14] | 0.148 [0.065, 0.206] | 0.015 | 0.001 | reference better |
| colagnn_tuned | 52 | -0.37 [-0.69, -0.12] | -0.32 [-0.60, -0.08] | -0.15 [-0.30, -0.02] | 0.273 [0.090, 0.489] | 0.100 | 0.295 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| sarima | 0.818 |
| gnn_st_tuned | 0.833 |
| blend_baseline | 0.839 |
| gnn_st | 0.848 |
| gnn_st_nograph_tuned | 0.852 |
| xgboost_parity | 0.856 |
| xgboost_tuned | 0.860 |
| climatology | 0.863 |
| xgboost | 0.864 |
| gnn_st_nograph | 0.865 |
| lstm_parity | 0.867 |
| lstm_tuned | 0.873 |
| lstm_s10 | 0.875 |
| lstm | 0.880 |
| arima | 0.900 |
| colagnn_tuned | 0.931 |
| persistence | 1.000 |
| flusight_baseline | 1.035 |
| seasonal_naive | 1.104 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
