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
| blend_baseline | 53 | -0.01 [-0.15, 0.12] | -0.18 [-0.37, 0.01] | -0.09 [-0.13, -0.04] | 0.090 [-0.002, 0.148] | 1.000 | 0.007 | not distinguishable |
| sarima | 53 | -0.01 [-0.09, 0.05] | -0.00 [-0.09, 0.09] | -0.02 [-0.06, 0.03] | 0.000 [-0.062, 0.044] | 1.000 | 0.839 | not distinguishable |
| lstm_parity | 53 | -0.02 [-0.16, 0.11] | -0.17 [-0.37, 0.01] | -0.09 [-0.14, -0.04] | 0.087 [-0.008, 0.146] | 1.000 | 0.009 | not distinguishable |
| gnn_st_nograph | 53 | -0.02 [-0.18, 0.10] | -0.09 [-0.34, 0.10] | -0.04 [-0.13, 0.03] | 0.086 [-0.045, 0.190] | 1.000 | 0.839 | not distinguishable |
| climatology | 53 | -0.03 [-0.29, 0.18] | -0.24 [-0.53, 0.05] | -0.09 [-0.17, -0.01] | -0.004 [-0.098, 0.102] | 1.000 | 0.159 | not distinguishable |
| xgboost_parity | 53 | -0.06 [-0.18, 0.06] | -0.08 [-0.26, 0.08] | -0.06 [-0.11, -0.01] | 0.078 [-0.006, 0.137] | 1.000 | 0.159 | not distinguishable |
| xgboost | 53 | -0.06 [-0.18, 0.05] | -0.06 [-0.24, 0.08] | -0.05 [-0.10, 0.01] | 0.066 [-0.021, 0.141] | 1.000 | 0.371 | not distinguishable |
| seasonal_naive | 53 | -0.11 [-0.36, 0.22] | -0.65 [-0.92, -0.31] | -0.29 [-0.45, -0.12] | -0.049 [-0.125, 0.030] | 1.000 | 0.014 | not distinguishable |
| lstm | 53 | -0.16 [-0.37, 0.04] | -0.20 [-0.49, 0.06] | -0.13 [-0.22, -0.03] | 0.101 [-0.061, 0.229] | 1.000 | 0.123 | not distinguishable |
| arima | 53 | -0.22 [-0.41, -0.03] | -0.23 [-0.46, -0.01] | -0.15 [-0.24, -0.05] | 0.180 [0.006, 0.310] | 0.340 | 0.034 | reference better |
| persistence | 53 | -0.35 [-0.49, -0.20] | -0.84 [-1.01, -0.65] | -0.32 [-0.43, -0.21] | 0.186 [0.032, 0.309] | 0.001 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.787 |
| sarima | 0.799 |
| gnn_st_nograph | 0.812 |
| xgboost | 0.819 |
| xgboost_parity | 0.830 |
| climatology | 0.849 |
| lstm_parity | 0.849 |
| blend_baseline | 0.849 |
| lstm | 0.872 |
| arima | 0.888 |
| seasonal_naive | 0.982 |
| persistence | 1.000 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
