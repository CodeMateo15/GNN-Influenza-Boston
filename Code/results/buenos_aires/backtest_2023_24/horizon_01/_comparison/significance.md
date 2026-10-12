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
| gnn_st_nograph | 52 | 0.01 [-0.20, 0.19] | 0.02 [-0.66, 0.70] | -0.08 [-0.30, 0.08] | 0.010 [0.003, 0.020] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 52 | -0.03 [-0.43, 0.27] | 0.08 [-1.14, 1.17] | 0.00 [-0.27, 0.24] | 0.012 [0.005, 0.025] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | -0.31 [-0.95, 0.18] | -0.83 [-2.49, 0.73] | -0.11 [-0.58, 0.25] | 0.022 [0.011, 0.045] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 52 | -0.82 [-1.59, -0.23] | -1.52 [-3.10, -0.09] | -0.74 [-1.41, -0.22] | 0.028 [0.017, 0.056] | 0.009 | 0.004 | reference better |
| arima | 52 | -1.13 [-2.20, -0.09] | -1.75 [-4.64, 1.23] | -0.98 [-1.94, -0.13] | 0.066 [0.002, 0.083] | 0.023 | 0.015 | reference better |
| sarima | 52 | -6.63 [-9.11, -4.17] | -18.25 [-27.64, -9.74] | -6.17 [-8.68, -3.67] | 0.135 [0.068, 0.179] | 0.000 | 0.000 | reference better |
| xgboost_parity | 52 | -7.61 [-9.99, -5.66] | -12.48 [-18.16, -7.53] | -5.49 [-7.42, -4.00] | 0.162 [0.084, 0.205] | 0.000 | 0.000 | reference better |
| gat_parity | 52 | -10.99 [-15.22, -8.14] | -17.62 [-25.20, -10.71] | -7.93 [-11.89, -5.26] | 0.249 [0.127, 0.339] | 0.000 | 0.000 | reference better |
| lstm | 52 | -12.35 [-16.47, -9.19] | -23.37 [-30.45, -16.16] | -11.35 [-15.68, -8.13] | 0.216 [0.124, 0.294] | 0.000 | 0.000 | reference better |
| xgboost | 52 | -13.21 [-16.44, -10.20] | -23.89 [-32.54, -16.12] | -9.29 [-11.93, -6.96] | 0.249 [0.176, 0.292] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -14.26 [-17.82, -11.31] | -26.08 [-34.00, -18.49] | -10.53 [-12.93, -8.39] | 0.270 [0.207, 0.319] | 0.000 | 0.000 | reference better |
| climatology | 52 | -14.58 [-18.50, -11.13] | -25.05 [-33.71, -17.03] | -10.49 [-13.50, -7.86] | 0.222 [0.128, 0.288] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.985 |
| gnn_st | 0.985 |
| gnn_st_nograph | 0.996 |
| persistence | 1.000 |
| lstm_parity | 1.082 |
| arima | 1.114 |
| xgboost_parity | 1.708 |
| sarima | 1.797 |
| gat_parity | 2.029 |
| xgboost | 2.208 |
| climatology | 2.365 |
| seasonal_naive | 2.372 |
| lstm | 2.478 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
