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
| blend_baseline | 52 | 0.95 [-0.23, 2.12] | 1.66 [-1.30, 4.65] | 0.55 [-0.32, 1.43] | 0.029 [-0.004, 0.056] | 0.356 | 0.782 | not distinguishable |
| gnn_st_nograph | 52 | 0.63 [0.21, 1.09] | 1.21 [0.28, 2.26] | 0.23 [-0.13, 0.58] | 0.011 [-0.003, 0.024] | 0.028 | 0.782 | other better |
| persistence | 52 | -0.11 [-1.81, 1.42] | -0.46 [-4.58, 3.74] | 0.03 [-1.33, 1.21] | 0.057 [0.007, 0.107] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 52 | -0.12 [-1.18, 0.84] | -0.78 [-3.18, 1.86] | -0.13 [-0.82, 0.51] | 0.048 [0.026, 0.090] | 1.000 | 1.000 | not distinguishable |
| arima | 52 | -3.16 [-4.97, -1.50] | -4.84 [-9.60, 0.27] | -2.96 [-4.86, -1.40] | 0.162 [0.082, 0.221] | 0.001 | 0.002 | reference better |
| sarima | 52 | -5.46 [-7.12, -3.78] | -10.65 [-15.28, -6.68] | -4.83 [-6.60, -3.13] | 0.171 [0.082, 0.237] | 0.000 | 0.000 | reference better |
| xgboost_parity | 52 | -8.77 [-11.23, -6.61] | -14.81 [-21.56, -9.01] | -6.24 [-8.30, -4.56] | 0.199 [0.131, 0.253] | 0.000 | 0.000 | reference better |
| xgboost | 52 | -10.77 [-13.88, -8.08] | -19.20 [-27.22, -12.03] | -7.66 [-10.20, -5.53] | 0.235 [0.153, 0.292] | 0.000 | 0.000 | reference better |
| lstm | 52 | -10.82 [-14.73, -7.69] | -20.54 [-26.80, -14.21] | -11.36 [-16.16, -7.77] | 0.292 [0.149, 0.435] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -10.99 [-13.64, -8.73] | -20.29 [-27.04, -13.53] | -8.03 [-9.86, -6.41] | 0.213 [0.145, 0.288] | 0.000 | 0.000 | reference better |
| climatology | 52 | -11.32 [-14.59, -8.45] | -19.26 [-27.24, -12.26] | -7.98 [-10.53, -5.72] | 0.165 [0.073, 0.244] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.947 |
| gnn_st_nograph | 0.980 |
| persistence | 1.000 |
| gnn_st | 1.003 |
| lstm_parity | 1.016 |
| arima | 1.301 |
| sarima | 1.488 |
| xgboost_parity | 1.629 |
| xgboost | 1.772 |
| climatology | 1.804 |
| seasonal_naive | 1.809 |
| lstm | 2.144 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
