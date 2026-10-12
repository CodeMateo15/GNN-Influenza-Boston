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
| xgboost_parity | 52 | 0.09 [-0.53, 0.84] | -0.53 [-1.26, 0.89] | -0.14 [-0.70, 0.42] | -0.055 [-0.123, 0.002] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 52 | -0.04 [-0.30, 0.23] | -0.21 [-0.46, 0.21] | 0.05 [-0.08, 0.15] | 0.001 [-0.014, 0.012] | 1.000 | 1.000 | not distinguishable |
| sarima | 52 | -0.05 [-0.50, 0.43] | -0.21 [-0.75, 0.79] | -0.03 [-0.33, 0.31] | 0.054 [-0.013, 0.126] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 52 | -0.12 [-0.36, 0.14] | -0.34 [-0.57, 0.03] | -0.22 [-0.48, 0.01] | 0.026 [0.007, 0.048] | 1.000 | 0.808 | not distinguishable |
| seasonal_naive | 52 | -0.25 [-1.12, 1.01] | 1.00 [-1.18, 2.82] | 0.73 [-0.49, 2.83] | -0.060 [-0.184, 0.085] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 52 | -0.30 [-0.99, 0.52] | -0.79 [-1.49, 0.58] | 0.03 [-0.38, 0.47] | -0.051 [-0.100, -0.006] | 1.000 | 1.000 | not distinguishable |
| xgboost | 52 | -0.71 [-1.87, 0.24] | -1.66 [-3.32, 0.23] | -0.43 [-1.40, 0.28] | -0.012 [-0.142, 0.090] | 1.000 | 1.000 | not distinguishable |
| climatology | 52 | -1.75 [-3.35, -0.40] | -2.95 [-4.89, -0.51] | -0.27 [-1.30, 0.50] | 0.003 [-0.129, 0.114] | 0.355 | 1.000 | reference better |
| persistence | 52 | -2.62 [-6.71, 0.45] | -3.36 [-11.71, 2.54] | -1.98 [-4.09, -0.13] | 0.122 [0.014, 0.266] | 1.000 | 0.579 | not distinguishable |
| arima | 52 | -2.77 [-4.82, -0.93] | -4.57 [-6.57, -1.88] | -2.84 [-5.23, -0.95] | 0.364 [0.270, 0.454] | 0.131 | 0.233 | reference better |
| lstm | 52 | -2.90 [-4.97, -0.94] | -4.45 [-6.41, -1.79] | -3.04 [-5.62, -1.01] | 0.186 [0.038, 0.347] | 0.131 | 0.233 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| seasonal_naive | 0.680 |
| gnn_st_nograph | 0.760 |
| blend_baseline | 0.763 |
| gnn_st | 0.766 |
| sarima | 0.769 |
| xgboost_parity | 0.783 |
| lstm_parity | 0.792 |
| climatology | 0.798 |
| xgboost | 0.817 |
| persistence | 1.000 |
| arima | 1.102 |
| lstm | 1.126 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
