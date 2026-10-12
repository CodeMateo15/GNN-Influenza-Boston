# Is `gnn_st`'s lead bigger than chance? — horizon 4, `full`

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
| xgboost_parity | 52 | 0.09 [-0.08, 0.23] | 0.06 [-0.11, 0.23] | 0.01 [-0.14, 0.15] | -0.006 [-0.034, 0.023] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 52 | 0.07 [-0.05, 0.20] | 0.04 [-0.09, 0.19] | 0.03 [-0.04, 0.09] | -0.017 [-0.047, 0.015] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 52 | 0.06 [-0.21, 0.28] | 0.05 [-0.26, 0.37] | -0.03 [-0.30, 0.21] | -0.007 [-0.040, 0.024] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 52 | 0.06 [-0.10, 0.18] | -0.02 [-0.17, 0.12] | 0.00 [-0.11, 0.09] | 0.026 [-0.018, 0.061] | 1.000 | 1.000 | not distinguishable |
| sarima | 52 | -0.02 [-0.11, 0.07] | -0.03 [-0.11, 0.05] | -0.00 [-0.09, 0.10] | -0.008 [-0.043, 0.038] | 1.000 | 1.000 | not distinguishable |
| climatology | 52 | -0.05 [-0.50, 0.30] | -0.18 [-0.70, 0.34] | -0.17 [-0.58, 0.16] | 0.068 [-0.075, 0.174] | 1.000 | 1.000 | not distinguishable |
| xgboost | 52 | -0.06 [-0.46, 0.25] | -0.10 [-0.58, 0.37] | -0.14 [-0.52, 0.18] | 0.076 [-0.071, 0.192] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | -0.06 [-0.29, 0.23] | -0.50 [-0.79, -0.20] | -0.16 [-0.30, 0.01] | 0.017 [-0.047, 0.078] | 1.000 | 0.655 | not distinguishable |
| arima | 52 | -0.07 [-0.37, 0.19] | 0.01 [-0.36, 0.32] | -0.02 [-0.33, 0.21] | 0.139 [-0.004, 0.254] | 1.000 | 1.000 | not distinguishable |
| seasonal_naive | 52 | -0.11 [-0.48, 0.26] | -0.57 [-1.00, -0.12] | -0.24 [-0.47, 0.02] | 0.086 [-0.098, 0.264] | 1.000 | 0.689 | not distinguishable |
| lstm | 52 | -0.15 [-0.64, 0.28] | -0.22 [-0.84, 0.33] | -0.08 [-0.41, 0.20] | 0.248 [-0.086, 0.492] | 1.000 | 1.000 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| lstm_parity | 0.889 |
| xgboost_parity | 0.896 |
| gnn_st_nograph | 0.903 |
| gnn_st | 0.905 |
| sarima | 0.907 |
| arima | 0.917 |
| blend_baseline | 0.925 |
| lstm | 0.953 |
| xgboost | 0.988 |
| persistence | 1.000 |
| climatology | 1.008 |
| seasonal_naive | 1.050 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
