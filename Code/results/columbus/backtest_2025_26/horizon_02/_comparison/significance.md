# Is `gnn_st`'s lead bigger than chance? — horizon 2, `post_covid`

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
| xgboost_parity | 53 | -0.37 [-1.09, 0.27] | -0.98 [-1.98, 0.09] | -0.31 [-0.73, 0.10] | 0.003 [-0.028, 0.060] | 0.270 | 0.091 | not distinguishable |
| gnn_st_nograph | 53 | -0.67 [-1.06, -0.39] | -1.10 [-1.68, -0.53] | -0.40 [-0.74, -0.16] | 0.071 [0.038, 0.113] | 0.001 | 0.029 | reference better |
| blend_baseline | 53 | -0.72 [-1.14, -0.43] | -1.23 [-1.90, -0.61] | -0.40 [-0.77, -0.11] | 0.070 [0.040, 0.112] | 0.001 | 0.044 | reference better |
| lstm | 53 | -0.78 [-1.45, -0.05] | -0.95 [-1.74, -0.07] | -0.58 [-0.97, -0.12] | 0.031 [-0.028, 0.099] | 0.071 | 0.029 | reference better |
| lstm_parity | 53 | -0.85 [-1.26, -0.53] | -1.34 [-1.93, -0.75] | -0.60 [-0.86, -0.38] | 0.084 [0.053, 0.128] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -1.08 [-2.06, -0.22] | -1.90 [-3.07, -0.59] | -1.12 [-2.00, -0.38] | 0.032 [-0.041, 0.131] | 0.071 | 0.017 | reference better |
| arima | 53 | -1.22 [-1.95, -0.63] | -2.08 [-3.07, -1.14] | -0.77 [-1.36, -0.34] | 0.119 [0.063, 0.193] | 0.001 | 0.015 | reference better |
| sarima | 53 | -1.26 [-1.83, -0.83] | -1.81 [-2.50, -1.21] | -0.80 [-1.12, -0.56] | 0.083 [0.043, 0.129] | 0.000 | 0.000 | reference better |
| persistence | 53 | -1.72 [-2.49, -1.13] | -2.63 [-3.55, -1.76] | -1.01 [-1.63, -0.55] | 0.120 [0.065, 0.190] | 0.000 | 0.001 | reference better |
| climatology | 53 | -2.13 [-3.65, -0.85] | -3.34 [-5.11, -1.56] | -1.25 [-2.56, -0.22] | 0.039 [-0.076, 0.181] | 0.006 | 0.044 | reference better |
| seasonal_naive | 53 | -3.14 [-7.10, -0.74] | -7.49 [-14.99, -0.92] | -5.17 [-9.91, -2.20] | 0.156 [-0.004, 0.249] | 0.083 | 0.029 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.797 |
| xgboost_parity | 0.859 |
| blend_baseline | 0.877 |
| gnn_st_nograph | 0.879 |
| lstm | 0.913 |
| lstm_parity | 0.918 |
| arima | 0.952 |
| sarima | 0.959 |
| persistence | 1.000 |
| xgboost | 1.023 |
| climatology | 1.049 |
| seasonal_naive | 1.838 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
