# Is `gnn_st`'s lead bigger than chance? — horizon 2, `full`

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
| sarima | 52 | 0.05 [-0.07, 0.17] | 0.09 [-0.06, 0.24] | 0.05 [-0.03, 0.15] | -0.012 [-0.048, 0.024] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 52 | 0.04 [-0.27, 0.26] | 0.06 [-0.24, 0.32] | 0.04 [-0.14, 0.17] | 0.060 [-0.024, 0.127] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | 0.02 [-0.10, 0.14] | -0.32 [-0.43, -0.23] | -0.10 [-0.20, 0.00] | 0.033 [-0.001, 0.059] | 1.000 | 0.267 | not distinguishable |
| lstm_parity | 52 | 0.02 [-0.09, 0.11] | -0.06 [-0.19, 0.05] | -0.02 [-0.09, 0.05] | 0.029 [-0.008, 0.053] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 52 | 0.01 [-0.32, 0.23] | 0.09 [-0.22, 0.38] | -0.02 [-0.24, 0.17] | 0.026 [-0.031, 0.049] | 1.000 | 1.000 | not distinguishable |
| xgboost_parity | 52 | -0.01 [-0.31, 0.19] | 0.06 [-0.26, 0.33] | 0.01 [-0.18, 0.17] | 0.059 [-0.033, 0.150] | 1.000 | 1.000 | not distinguishable |
| arima | 52 | -0.02 [-0.25, 0.16] | 0.05 [-0.19, 0.25] | 0.01 [-0.15, 0.14] | 0.078 [0.006, 0.115] | 1.000 | 1.000 | not distinguishable |
| xgboost | 52 | -0.14 [-0.61, 0.18] | -0.13 [-0.66, 0.34] | -0.09 [-0.41, 0.15] | 0.135 [-0.041, 0.281] | 1.000 | 1.000 | not distinguishable |
| climatology | 52 | -0.27 [-0.97, 0.22] | -0.36 [-1.10, 0.35] | -0.27 [-0.79, 0.13] | 0.209 [-0.059, 0.350] | 1.000 | 1.000 | not distinguishable |
| seasonal_naive | 52 | -0.34 [-0.94, 0.11] | -0.75 [-1.38, -0.19] | -0.35 [-0.62, -0.10] | 0.228 [-0.004, 0.384] | 1.000 | 0.028 | not distinguishable |
| lstm | 52 | -0.34 [-1.06, 0.15] | -0.36 [-1.15, 0.34] | -0.20 [-0.72, 0.16] | 0.307 [0.024, 0.422] | 1.000 | 1.000 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| sarima | 0.899 |
| gnn_st_nograph | 0.910 |
| xgboost_parity | 0.925 |
| arima | 0.927 |
| gnn_st | 0.934 |
| lstm_parity | 0.947 |
| blend_baseline | 0.947 |
| xgboost | 0.991 |
| persistence | 1.000 |
| lstm | 1.063 |
| climatology | 1.115 |
| seasonal_naive | 1.162 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
