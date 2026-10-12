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
| blend_baseline | 52 | 2.58 [0.42, 4.74] | 4.66 [0.34, 9.52] | 1.01 [-0.82, 2.75] | 0.059 [-0.008, 0.112] | 0.100 | 0.904 | other better |
| lstm_parity | 52 | 1.73 [0.53, 2.97] | 2.69 [0.44, 5.09] | 0.70 [-0.30, 1.61] | 0.017 [-0.005, 0.042] | 0.060 | 0.765 | other better |
| gnn_st_nograph | 52 | 0.18 [-0.14, 0.49] | 0.72 [0.13, 1.33] | -0.06 [-0.35, 0.22] | 0.010 [-0.001, 0.024] | 0.778 | 1.000 | not distinguishable |
| persistence | 52 | -0.12 [-4.12, 3.53] | -0.99 [-8.40, 7.04] | -0.89 [-4.69, 2.13] | 0.181 [0.030, 0.299] | 0.944 | 1.000 | not distinguishable |
| arima | 52 | -1.55 [-4.17, 1.07] | -3.10 [-8.53, 3.19] | -3.06 [-6.54, -0.33] | 0.261 [0.152, 0.356] | 0.778 | 0.447 | not distinguishable |
| sarima | 52 | -3.96 [-6.57, -1.49] | -10.65 [-16.24, -4.94] | -3.72 [-6.16, -1.53] | 0.084 [0.020, 0.147] | 0.036 | 0.035 | reference better |
| seasonal_naive | 52 | -5.44 [-7.05, -4.02] | -11.02 [-14.58, -7.61] | -4.36 [-5.32, -3.45] | 0.115 [0.054, 0.207] | 0.000 | 0.000 | reference better |
| xgboost_parity | 52 | -5.48 [-7.02, -4.16] | -9.51 [-13.51, -5.84] | -4.22 [-5.41, -3.16] | 0.131 [0.063, 0.200] | 0.000 | 0.000 | reference better |
| lstm | 52 | -5.50 [-7.60, -3.23] | -8.93 [-12.62, -5.43] | -6.69 [-11.58, -3.19] | 0.427 [0.211, 0.622] | 0.000 | 0.035 | reference better |
| climatology | 52 | -5.76 [-7.61, -4.08] | -9.99 [-14.35, -5.95] | -4.31 [-5.86, -2.88] | 0.066 [-0.012, 0.152] | 0.000 | 0.000 | reference better |
| xgboost | 52 | -6.37 [-7.99, -4.98] | -10.85 [-15.20, -6.97] | -4.65 [-6.00, -3.58] | 0.166 [0.085, 0.252] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.869 |
| lstm_parity | 0.891 |
| gnn_st | 0.939 |
| gnn_st_nograph | 0.943 |
| persistence | 1.000 |
| arima | 1.149 |
| sarima | 1.195 |
| xgboost_parity | 1.229 |
| climatology | 1.236 |
| seasonal_naive | 1.239 |
| xgboost | 1.259 |
| lstm | 1.399 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
