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
| xgboost_parity | 53 | -0.32 [-0.93, 0.11] | -0.61 [-1.53, 0.22] | -0.76 [-1.28, -0.28] | 0.016 [-0.047, 0.090] | 0.597 | 0.080 | not distinguishable |
| xgboost | 53 | -0.39 [-0.98, 0.08] | -0.59 [-1.44, 0.21] | -1.52 [-2.41, -0.75] | 0.009 [-0.064, 0.098] | 0.597 | 0.022 | not distinguishable |
| gnn_st_nograph | 53 | -0.42 [-1.04, -0.04] | -0.77 [-1.76, 0.13] | -0.30 [-0.76, 0.09] | 0.100 [0.027, 0.164] | 0.597 | 0.409 | reference better |
| lstm_parity | 53 | -0.79 [-1.48, -0.33] | -1.35 [-2.41, -0.37] | -0.60 [-1.01, -0.26] | 0.137 [0.060, 0.205] | 0.167 | 0.043 | reference better |
| blend_baseline | 53 | -0.81 [-1.69, -0.29] | -1.45 [-2.71, -0.32] | -0.38 [-1.09, 0.24] | 0.140 [0.041, 0.226] | 0.227 | 0.409 | reference better |
| sarima | 53 | -1.01 [-2.12, -0.05] | -0.97 [-2.56, 0.35] | -1.09 [-1.76, -0.58] | 0.094 [0.019, 0.145] | 0.445 | 0.010 | reference better |
| climatology | 53 | -1.61 [-2.62, -0.69] | -2.31 [-3.44, -1.14] | -0.77 [-1.71, -0.06] | 0.026 [-0.067, 0.127] | 0.039 | 0.335 | reference better |
| lstm | 53 | -1.62 [-3.00, -0.45] | -2.23 [-4.05, -0.32] | -1.07 [-2.02, -0.19] | 0.219 [0.048, 0.400] | 0.186 | 0.197 | reference better |
| arima | 53 | -1.79 [-3.27, -0.52] | -2.70 [-4.78, -0.51] | -1.22 [-2.26, -0.28] | 0.306 [0.095, 0.492] | 0.167 | 0.166 | reference better |
| seasonal_naive | 53 | -2.62 [-7.23, 0.08] | -6.46 [-15.14, 0.47] | -4.68 [-9.60, -1.68] | 0.143 [-0.031, 0.244] | 0.597 | 0.203 | not distinguishable |
| persistence | 53 | -3.36 [-5.56, -1.87] | -4.66 [-7.21, -2.48] | -1.82 [-3.37, -0.67] | 0.314 [0.111, 0.495] | 0.010 | 0.123 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.709 |
| gnn_st_nograph | 0.757 |
| blend_baseline | 0.769 |
| lstm_parity | 0.805 |
| xgboost_parity | 0.830 |
| climatology | 0.831 |
| lstm | 0.880 |
| sarima | 0.882 |
| arima | 0.904 |
| xgboost | 0.951 |
| persistence | 1.000 |
| seasonal_naive | 1.456 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
