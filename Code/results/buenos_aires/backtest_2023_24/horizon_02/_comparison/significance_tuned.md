# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 2, `post_covid`

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
| blend_baseline | 52 | -0.05 [-0.60, 0.43] | -0.05 [-1.24, 1.18] | 0.01 [-0.39, 0.35] | 0.016 [0.004, 0.028] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.07 [-0.33, 0.23] | -0.23 [-0.73, 0.34] | -0.12 [-0.36, 0.08] | 0.004 [0.002, 0.008] | 1.000 | 1.000 | not distinguishable |
| lstm_tuned | 52 | -0.84 [-1.86, 0.07] | -2.61 [-4.26, -0.74] | -0.38 [-0.89, 0.16] | 0.025 [0.005, 0.070] | 0.450 | 1.000 | not distinguishable |
| persistence | 52 | -1.10 [-2.33, -0.03] | -2.17 [-4.66, 0.51] | -0.51 [-1.55, 0.31] | 0.044 [0.014, 0.081] | 0.277 | 1.000 | reference better |
| flusight_baseline | 52 | -1.18 [-2.42, -0.13] | -2.22 [-4.68, 0.44] | -0.52 [-1.69, 0.42] | 0.044 [0.014, 0.081] | 0.248 | 1.000 | reference better |
| colagnn_tuned | 52 | -3.49 [-4.92, -2.20] | -4.91 [-8.71, -1.46] | -2.61 [-3.74, -1.58] | -0.006 [-0.040, 0.023] | 0.000 | 0.000 | reference better |
| sarima | 52 | -6.46 [-8.58, -4.39] | -12.36 [-18.37, -7.03] | -5.37 [-7.46, -3.38] | 0.158 [0.068, 0.227] | 0.000 | 0.000 | reference better |
| xgboost_tuned | 52 | -9.94 [-12.88, -7.29] | -16.65 [-25.14, -9.44] | -6.84 [-9.31, -4.80] | 0.206 [0.128, 0.266] | 0.000 | 0.000 | reference better |
| lstm_s10 | 52 | -11.44 [-15.70, -7.79] | -21.70 [-29.14, -13.75] | -11.43 [-16.52, -7.48] | 0.290 [0.141, 0.430] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.947 |
| gnn_st_tuned | 0.949 |
| gnn_st_nograph_tuned | 0.961 |
| gnn_st_nograph | 0.980 |
| lstm_tuned | 0.987 |
| persistence | 1.000 |
| flusight_baseline | 1.001 |
| gnn_st | 1.003 |
| lstm_parity | 1.016 |
| colagnn_tuned | 1.211 |
| arima | 1.301 |
| sarima | 1.488 |
| xgboost_parity | 1.629 |
| xgboost_tuned | 1.636 |
| xgboost | 1.772 |
| climatology | 1.804 |
| seasonal_naive | 1.809 |
| lstm_s10 | 2.096 |
| lstm | 2.144 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
