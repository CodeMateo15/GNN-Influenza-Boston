# Is `gnn_st`'s lead bigger than chance? — horizon 1, `post_covid`

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
| lstm | 53 | -0.45 [-0.75, -0.06] | -0.51 [-0.99, 0.05] | -0.53 [-0.80, -0.22] | 0.007 [-0.025, 0.028] | 0.032 | 0.000 | reference better |
| gnn_st_nograph | 53 | -0.59 [-0.98, -0.30] | -1.01 [-1.66, -0.45] | -0.39 [-0.63, -0.22] | 0.051 [0.031, 0.092] | 0.001 | 0.000 | reference better |
| xgboost_parity | 53 | -0.61 [-1.30, -0.05] | -1.21 [-2.19, -0.20] | -0.44 [-0.73, -0.19] | 0.024 [0.006, 0.067] | 0.032 | 0.000 | reference better |
| lstm_parity | 53 | -0.75 [-1.08, -0.48] | -1.14 [-1.68, -0.65] | -0.51 [-0.69, -0.35] | 0.054 [0.034, 0.101] | 0.000 | 0.000 | reference better |
| blend_baseline | 53 | -0.78 [-1.16, -0.49] | -1.23 [-1.84, -0.66] | -0.48 [-0.73, -0.28] | 0.056 [0.035, 0.103] | 0.000 | 0.000 | reference better |
| arima | 53 | -0.98 [-1.49, -0.56] | -1.62 [-2.49, -0.87] | -0.60 [-0.99, -0.32] | 0.078 [0.051, 0.127] | 0.000 | 0.000 | reference better |
| sarima | 53 | -1.16 [-1.65, -0.77] | -1.73 [-2.40, -1.12] | -0.68 [-1.00, -0.45] | 0.074 [0.050, 0.121] | 0.000 | 0.000 | reference better |
| persistence | 53 | -1.17 [-1.55, -0.82] | -1.80 [-2.40, -1.22] | -0.72 [-1.06, -0.49] | 0.071 [0.044, 0.127] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -1.61 [-2.68, -0.65] | -2.76 [-4.21, -1.25] | -1.64 [-2.37, -1.08] | 0.086 [0.039, 0.154] | 0.001 | 0.000 | reference better |
| gat_parity | 53 | -1.70 [-3.42, -0.62] | -2.98 [-5.63, -0.96] | -0.92 [-1.98, -0.27] | 0.124 [0.006, 0.217] | 0.004 | 0.004 | reference better |
| climatology | 53 | -3.06 [-5.05, -1.42] | -4.81 [-7.17, -2.36] | -1.90 [-3.17, -0.98] | 0.130 [0.012, 0.283] | 0.000 | 0.000 | reference better |
| seasonal_naive | 53 | -4.07 [-8.24, -1.53] | -8.97 [-16.61, -2.32] | -5.81 [-10.67, -2.82] | 0.247 [0.093, 0.359] | 0.004 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.821 |
| gnn_st_nograph | 0.917 |
| xgboost_parity | 0.930 |
| blend_baseline | 0.940 |
| lstm_parity | 0.946 |
| lstm | 0.953 |
| arima | 0.970 |
| sarima | 0.991 |
| persistence | 1.000 |
| gat_parity | 1.049 |
| xgboost | 1.229 |
| climatology | 1.291 |
| seasonal_naive | 2.262 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
