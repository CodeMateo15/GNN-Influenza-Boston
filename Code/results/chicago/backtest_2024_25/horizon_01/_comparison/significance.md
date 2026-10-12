# Is `gnn_st`'s lead bigger than chance? — horizon 1, `full`

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
| gat_parity | 52 | -0.13 [-0.24, -0.06] | -0.02 [-0.09, 0.03] | -0.04 [-0.08, -0.02] | -0.019 [-0.032, -0.010] | 0.000 | 0.001 | reference better |
| lstm | 52 | -0.15 [-0.25, -0.06] | -0.06 [-0.12, -0.00] | -0.06 [-0.09, -0.02] | -0.013 [-0.032, -0.002] | 0.000 | 0.001 | reference better |
| gnn_st_nograph | 52 | -0.15 [-0.28, -0.06] | -0.18 [-0.32, -0.08] | -0.08 [-0.13, -0.05] | 0.070 [0.048, 0.111] | 0.000 | 0.000 | reference better |
| xgboost_parity | 52 | -0.24 [-0.43, -0.11] | -0.20 [-0.34, -0.07] | -0.12 [-0.20, -0.06] | 0.083 [0.058, 0.120] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.25 [-0.33, -0.17] | -0.71 [-0.81, -0.61] | -0.27 [-0.33, -0.21] | 0.118 [0.093, 0.160] | 0.000 | 0.000 | reference better |
| xgboost | 52 | -0.26 [-0.46, -0.12] | -0.21 [-0.39, -0.07] | -0.13 [-0.22, -0.06] | 0.089 [0.056, 0.134] | 0.000 | 0.000 | reference better |
| sarima | 52 | -0.30 [-0.51, -0.15] | -0.26 [-0.43, -0.12] | -0.16 [-0.27, -0.08] | 0.084 [0.046, 0.124] | 0.000 | 0.000 | reference better |
| arima | 52 | -0.32 [-0.47, -0.20] | -0.27 [-0.43, -0.14] | -0.16 [-0.23, -0.10] | 0.153 [0.118, 0.184] | 0.000 | 0.000 | reference better |
| blend_baseline | 52 | -0.38 [-0.76, -0.10] | -0.44 [-0.71, -0.20] | -0.20 [-0.31, -0.12] | 0.089 [0.068, 0.122] | 0.000 | 0.000 | reference better |
| lstm_parity | 52 | -0.40 [-0.57, -0.28] | -0.47 [-0.60, -0.37] | -0.22 [-0.30, -0.17] | 0.120 [0.090, 0.172] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -0.71 [-1.19, -0.35] | -1.13 [-1.58, -0.76] | -0.49 [-0.74, -0.29] | 0.270 [0.117, 0.398] | 0.000 | 0.000 | reference better |
| climatology | 52 | -0.80 [-1.65, -0.16] | -1.13 [-1.93, -0.35] | -0.42 [-0.73, -0.18] | 0.223 [0.073, 0.401] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.803 |
| gat_parity | 0.833 |
| lstm | 0.844 |
| gnn_st_nograph | 0.864 |
| xgboost_parity | 0.890 |
| xgboost | 0.899 |
| sarima | 0.919 |
| arima | 0.922 |
| blend_baseline | 0.948 |
| lstm_parity | 0.968 |
| persistence | 1.000 |
| climatology | 1.113 |
| seasonal_naive | 1.161 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
