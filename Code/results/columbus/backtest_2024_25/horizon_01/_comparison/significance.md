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
| gnn_st_nograph | 52 | -0.52 [-0.88, -0.19] | -0.91 [-1.45, -0.35] | -0.31 [-0.53, -0.12] | 0.018 [0.011, 0.049] | 0.007 | 0.010 | reference better |
| xgboost_parity | 52 | -0.82 [-1.85, -0.12] | -1.76 [-3.27, -0.10] | -0.55 [-1.31, -0.04] | 0.023 [0.006, 0.055] | 0.013 | 0.041 | reference better |
| lstm_parity | 52 | -0.84 [-1.19, -0.51] | -0.83 [-1.57, -0.30] | -0.55 [-0.84, -0.33] | 0.049 [0.026, 0.128] | 0.000 | 0.000 | reference better |
| persistence | 52 | -1.22 [-2.06, -0.24] | -0.71 [-2.89, 1.49] | -0.57 [-1.13, 0.26] | 0.046 [0.024, 0.145] | 0.013 | 0.050 | reference better |
| blend_baseline | 52 | -1.59 [-3.56, -0.31] | -3.46 [-6.21, -0.40] | -0.95 [-2.42, -0.01] | 0.032 [-0.000, 0.060] | 0.013 | 0.041 | reference better |
| sarima | 52 | -1.62 [-3.59, -0.33] | -4.07 [-7.31, -0.42] | -1.46 [-3.27, -0.29] | 0.109 [0.001, 0.153] | 0.013 | 0.017 | reference better |
| arima | 52 | -2.56 [-4.49, -1.16] | -5.42 [-8.54, -1.89] | -2.37 [-4.47, -0.91] | 0.246 [0.233, 0.278] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -2.98 [-5.42, -1.32] | -5.56 [-9.24, -1.64] | -1.65 [-3.08, -0.76] | 0.182 [0.050, 0.249] | 0.001 | 0.004 | reference better |
| xgboost | 52 | -3.56 [-7.99, -0.62] | -8.59 [-15.02, -0.95] | -2.82 [-6.85, -0.24] | 0.231 [-0.016, 0.373] | 0.013 | 0.039 | reference better |
| gat_parity | 52 | -3.92 [-6.72, -1.91] | -6.76 [-10.87, -2.79] | -3.22 [-5.89, -1.43] | 0.073 [-0.014, 0.134] | 0.000 | 0.000 | reference better |
| climatology | 52 | -4.49 [-9.08, -1.23] | -9.51 [-16.17, -1.69] | -2.65 [-6.52, -0.19] | 0.246 [-0.015, 0.396] | 0.003 | 0.041 | reference better |
| lstm | 52 | -4.69 [-9.07, -1.58] | -9.47 [-15.54, -2.46] | -4.71 [-9.66, -1.32] | 0.139 [0.022, 0.228] | 0.001 | 0.003 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.877 |
| gnn_st_nograph | 0.944 |
| lstm_parity | 0.995 |
| xgboost_parity | 0.996 |
| persistence | 1.000 |
| blend_baseline | 1.081 |
| sarima | 1.189 |
| seasonal_naive | 1.232 |
| arima | 1.386 |
| climatology | 1.446 |
| xgboost | 1.482 |
| gat_parity | 1.567 |
| lstm | 1.887 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
