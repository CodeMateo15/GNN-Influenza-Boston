# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 1, `post_covid`

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
| gnn_st_nograph_tuned | 52 | -0.00 [-0.21, 0.21] | 0.02 [-0.42, 0.50] | -0.13 [-0.31, 0.03] | 0.006 [0.002, 0.015] | 1.000 | 0.597 | not distinguishable |
| blend_baseline | 52 | -0.03 [-0.39, 0.30] | 0.10 [-0.96, 1.05] | 0.02 [-0.21, 0.24] | 0.009 [0.004, 0.022] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | -0.31 [-0.89, 0.22] | -0.81 [-2.32, 0.67] | -0.10 [-0.52, 0.28] | 0.019 [0.010, 0.042] | 1.000 | 1.000 | not distinguishable |
| flusight_baseline | 52 | -0.35 [-0.92, 0.15] | -0.84 [-2.35, 0.61] | -0.27 [-0.73, 0.14] | 0.019 [0.010, 0.042] | 1.000 | 0.917 | not distinguishable |
| lstm_tuned | 52 | -0.99 [-1.76, -0.33] | -1.99 [-3.39, -0.55] | -0.79 [-1.42, -0.25] | 0.030 [0.016, 0.060] | 0.011 | 0.009 | reference better |
| colagnn_tuned | 52 | -3.28 [-4.47, -2.23] | -5.08 [-7.51, -2.87] | -2.56 [-3.45, -1.71] | -0.004 [-0.032, 0.019] | 0.000 | 0.000 | reference better |
| sarima | 52 | -6.64 [-9.23, -4.04] | -18.23 [-27.81, -9.50] | -6.16 [-8.74, -3.58] | 0.132 [0.070, 0.175] | 0.000 | 0.000 | reference better |
| xgboost_tuned | 52 | -7.28 [-9.37, -5.40] | -11.92 [-17.44, -7.20] | -5.08 [-6.69, -3.71] | 0.136 [0.085, 0.175] | 0.000 | 0.000 | reference better |
| gat_tuned | 52 | -11.10 [-14.90, -8.19] | -17.63 [-24.60, -10.47] | -8.06 [-12.06, -5.18] | 0.258 [0.140, 0.331] | 0.000 | 0.000 | reference better |
| dualtopo_tuned | 52 | -11.62 [-16.81, -8.03] | -20.01 [-28.89, -12.07] | -9.97 [-15.67, -6.03] | 0.351 [0.134, 0.507] | 0.000 | 0.000 | reference better |
| lstm_s10 | 52 | -12.12 [-16.26, -8.78] | -22.97 [-30.24, -15.59] | -11.13 [-15.65, -7.70] | 0.227 [0.134, 0.309] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.985 |
| gnn_st | 0.985 |
| gnn_st_tuned | 0.987 |
| gnn_st_nograph | 0.996 |
| persistence | 1.000 |
| gnn_st_nograph_tuned | 1.003 |
| flusight_baseline | 1.022 |
| lstm_parity | 1.082 |
| lstm_tuned | 1.091 |
| arima | 1.114 |
| colagnn_tuned | 1.323 |
| xgboost_tuned | 1.655 |
| xgboost_parity | 1.708 |
| sarima | 1.797 |
| gat_parity | 2.029 |
| gat_tuned | 2.048 |
| xgboost | 2.208 |
| dualtopo_tuned | 2.298 |
| climatology | 2.365 |
| seasonal_naive | 2.372 |
| lstm_s10 | 2.452 |
| lstm | 2.478 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
