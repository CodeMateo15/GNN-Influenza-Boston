# Is `gnn_st`'s lead bigger than chance? — horizon 4, `post_covid`

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
| blend_baseline | 49 | 0.91 [-1.06, 2.44] | 3.44 [0.23, 6.24] | 0.43 [-1.17, 1.65] | 0.076 [0.041, 0.115] | 0.942 | 1.000 | not distinguishable |
| lstm_parity | 49 | -0.16 [-1.08, 0.57] | 1.18 [0.45, 1.97] | 0.18 [-0.49, 0.79] | 0.027 [0.002, 0.072] | 0.942 | 1.000 | not distinguishable |
| gnn_st_nograph | 49 | -0.36 [-0.64, -0.09] | -0.77 [-1.23, -0.24] | -0.25 [-0.44, -0.12] | 0.003 [-0.007, 0.013] | 0.088 | 0.030 | reference better |
| sarima | 49 | -1.37 [-3.62, 0.24] | 4.10 [-4.67, 10.38] | -0.41 [-2.25, 0.95] | 0.100 [0.061, 0.139] | 0.942 | 1.000 | not distinguishable |
| persistence | 49 | -1.81 [-5.01, 0.46] | 0.54 [-8.22, 6.15] | -1.02 [-3.58, 0.70] | 0.173 [0.093, 0.252] | 0.942 | 1.000 | not distinguishable |
| arima | 49 | -4.53 [-7.64, -1.75] | -0.79 [-4.19, 2.76] | -3.23 [-5.95, -1.21] | 0.259 [0.158, 0.336] | 0.042 | 0.069 | reference better |
| xgboost_parity | 49 | -5.29 [-6.66, -4.03] | -12.17 [-14.94, -9.81] | -3.80 [-4.62, -2.96] | 0.038 [0.006, 0.065] | 0.000 | 0.000 | reference better |
| xgboost | 49 | -6.72 [-8.57, -5.04] | -16.09 [-19.96, -12.59] | -5.24 [-6.39, -4.00] | 0.074 [0.030, 0.114] | 0.000 | 0.000 | reference better |
| climatology | 49 | -8.42 [-10.71, -5.96] | -19.68 [-23.95, -15.84] | -7.01 [-8.47, -5.50] | 0.032 [-0.024, 0.074] | 0.000 | 0.000 | reference better |
| seasonal_naive | 49 | -8.99 [-13.47, -5.66] | -18.58 [-27.44, -9.33] | -7.32 [-11.07, -4.68] | 0.156 [0.083, 0.233] | 0.001 | 0.001 | reference better |
| lstm | 49 | -11.06 [-15.55, -7.32] | -23.44 [-32.99, -14.20] | -8.89 [-14.29, -4.99] | 0.245 [0.066, 0.417] | 0.000 | 0.004 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.890 |
| lstm_parity | 0.909 |
| gnn_st | 0.923 |
| gnn_st_nograph | 0.942 |
| sarima | 0.954 |
| persistence | 1.000 |
| arima | 1.167 |
| xgboost_parity | 1.210 |
| xgboost | 1.319 |
| climatology | 1.452 |
| seasonal_naive | 1.477 |
| lstm | 1.595 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
