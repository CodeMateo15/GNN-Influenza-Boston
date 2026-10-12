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
| gnn_st_nograph | 52 | -0.21 [-0.66, 0.24] | -0.40 [-1.01, 0.14] | -0.16 [-0.48, 0.13] | 0.009 [-0.020, 0.044] | 0.766 | 0.791 | not distinguishable |
| xgboost_parity | 52 | -0.31 [-1.17, 0.42] | -1.21 [-2.28, 0.40] | -0.39 [-1.21, 0.20] | -0.008 [-0.033, 0.022] | 0.766 | 0.791 | not distinguishable |
| sarima | 52 | -0.57 [-1.75, 0.34] | -1.67 [-3.33, 0.32] | -0.70 [-1.88, 0.10] | 0.048 [-0.028, 0.086] | 0.766 | 0.731 | not distinguishable |
| lstm_parity | 52 | -0.64 [-1.12, -0.30] | -0.94 [-1.67, -0.40] | -0.56 [-1.04, -0.24] | 0.052 [0.023, 0.122] | 0.027 | 0.062 | reference better |
| blend_baseline | 52 | -0.95 [-2.36, 0.17] | -2.39 [-4.26, -0.01] | -0.55 [-1.71, 0.22] | -0.008 [-0.049, 0.025] | 0.495 | 0.791 | not distinguishable |
| persistence | 52 | -1.38 [-3.30, 0.27] | -1.21 [-5.49, 2.27] | -0.76 [-1.90, 0.51] | 0.042 [0.005, 0.156] | 0.495 | 0.791 | not distinguishable |
| seasonal_naive | 52 | -1.62 [-2.84, -0.51] | -2.45 [-4.48, -0.60] | -0.61 [-1.28, 0.06] | 0.083 [0.004, 0.164] | 0.056 | 0.731 | reference better |
| xgboost | 52 | -2.22 [-5.19, -0.02] | -5.51 [-9.63, -0.32] | -1.79 [-4.49, 0.03] | 0.130 [-0.052, 0.254] | 0.318 | 0.663 | reference better |
| arima | 52 | -2.70 [-4.75, -0.92] | -5.63 [-8.46, -1.99] | -3.06 [-5.69, -1.05] | 0.194 [0.156, 0.290] | 0.014 | 0.019 | reference better |
| climatology | 52 | -3.12 [-6.43, -0.62] | -6.40 [-10.65, -1.06] | -1.61 [-4.21, 0.17] | 0.146 [-0.051, 0.280] | 0.094 | 0.731 | reference better |
| lstm | 52 | -3.46 [-6.43, -0.96] | -6.57 [-10.40, -1.60] | -3.86 [-7.68, -1.04] | 0.084 [-0.027, 0.192] | 0.039 | 0.062 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.872 |
| gnn_st_nograph | 0.898 |
| xgboost_parity | 0.938 |
| blend_baseline | 0.964 |
| lstm_parity | 0.966 |
| seasonal_naive | 0.975 |
| sarima | 0.991 |
| persistence | 1.000 |
| climatology | 1.145 |
| xgboost | 1.176 |
| arima | 1.390 |
| lstm | 1.526 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
