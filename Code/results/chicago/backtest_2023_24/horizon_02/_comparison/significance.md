# Is `gnn_st`'s lead bigger than chance? — horizon 2, `full`

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
| sarima | 52 | -0.10 [-0.17, -0.05] | -0.11 [-0.16, -0.05] | -0.06 [-0.10, -0.03] | 0.036 [0.011, 0.071] | 0.012 | 0.005 | reference better |
| gnn_st_nograph | 52 | -0.12 [-0.18, -0.05] | -0.11 [-0.18, -0.05] | -0.06 [-0.12, -0.02] | 0.084 [0.045, 0.127] | 0.005 | 0.016 | reference better |
| xgboost_parity | 52 | -0.12 [-0.21, -0.04] | -0.06 [-0.14, 0.02] | -0.05 [-0.09, -0.02] | 0.061 [0.026, 0.104] | 0.016 | 0.016 | reference better |
| blend_baseline | 52 | -0.12 [-0.26, -0.03] | -0.17 [-0.31, -0.05] | -0.07 [-0.12, -0.03] | 0.065 [0.039, 0.102] | 0.023 | 0.009 | reference better |
| xgboost | 52 | -0.14 [-0.25, -0.04] | -0.05 [-0.14, 0.03] | -0.07 [-0.13, -0.02] | 0.036 [-0.008, 0.093] | 0.016 | 0.033 | reference better |
| lstm | 52 | -0.19 [-0.31, -0.08] | -0.11 [-0.25, 0.01] | -0.05 [-0.10, -0.01] | -0.013 [-0.065, 0.024] | 0.005 | 0.033 | reference better |
| lstm_parity | 52 | -0.23 [-0.29, -0.17] | -0.41 [-0.48, -0.33] | -0.17 [-0.21, -0.12] | 0.118 [0.084, 0.152] | 0.000 | 0.000 | reference better |
| climatology | 52 | -0.27 [-0.57, -0.07] | -0.44 [-0.77, -0.16] | -0.14 [-0.26, -0.06] | 0.056 [-0.007, 0.123] | 0.023 | 0.006 | reference better |
| arima | 52 | -0.28 [-0.41, -0.15] | -0.25 [-0.38, -0.13] | -0.13 [-0.21, -0.07] | 0.142 [0.095, 0.182] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.33 [-0.44, -0.22] | -0.67 [-0.78, -0.54] | -0.25 [-0.32, -0.18] | 0.136 [0.099, 0.174] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -0.60 [-0.88, -0.37] | -0.99 [-1.28, -0.71] | -0.50 [-0.71, -0.33] | 0.160 [0.044, 0.259] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.817 |
| xgboost_parity | 0.853 |
| lstm | 0.855 |
| sarima | 0.862 |
| gnn_st_nograph | 0.863 |
| xgboost | 0.864 |
| blend_baseline | 0.868 |
| arima | 0.912 |
| climatology | 0.921 |
| lstm_parity | 0.939 |
| persistence | 1.000 |
| seasonal_naive | 1.178 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
