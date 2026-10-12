# Is `gnn_st`'s lead bigger than chance? — horizon 1, `full`

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
| gat_parity | 53 | -0.10 [-0.20, -0.04] | -0.11 [-0.19, -0.05] | -0.07 [-0.11, -0.04] | 0.016 [-0.035, 0.044] | 0.002 | 0.000 | reference better |
| gnn_st_nograph | 53 | -0.14 [-0.25, -0.06] | -0.13 [-0.26, -0.05] | -0.08 [-0.13, -0.05] | 0.092 [0.052, 0.135] | 0.000 | 0.000 | reference better |
| lstm | 53 | -0.14 [-0.19, -0.09] | -0.09 [-0.13, -0.05] | -0.07 [-0.09, -0.05] | -0.009 [-0.032, 0.005] | 0.000 | 0.000 | reference better |
| blend_baseline | 53 | -0.15 [-0.28, -0.07] | -0.27 [-0.36, -0.21] | -0.15 [-0.17, -0.13] | 0.107 [0.081, 0.139] | 0.000 | 0.000 | reference better |
| sarima | 53 | -0.18 [-0.27, -0.13] | -0.14 [-0.20, -0.09] | -0.10 [-0.13, -0.07] | 0.070 [0.037, 0.110] | 0.000 | 0.000 | reference better |
| xgboost_parity | 53 | -0.19 [-0.31, -0.11] | -0.15 [-0.29, -0.06] | -0.11 [-0.16, -0.07] | 0.098 [0.054, 0.164] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -0.22 [-0.33, -0.15] | -0.17 [-0.29, -0.09] | -0.12 [-0.17, -0.09] | 0.099 [0.055, 0.154] | 0.000 | 0.000 | reference better |
| arima | 53 | -0.25 [-0.35, -0.17] | -0.22 [-0.34, -0.13] | -0.13 [-0.19, -0.09] | 0.134 [0.076, 0.191] | 0.000 | 0.000 | reference better |
| persistence | 53 | -0.26 [-0.32, -0.19] | -0.68 [-0.74, -0.61] | -0.25 [-0.30, -0.19] | 0.147 [0.115, 0.192] | 0.000 | 0.000 | reference better |
| lstm_parity | 53 | -0.27 [-0.33, -0.22] | -0.44 [-0.49, -0.39] | -0.22 [-0.24, -0.19] | 0.139 [0.102, 0.187] | 0.000 | 0.000 | reference better |
| climatology | 53 | -0.36 [-0.78, -0.08] | -0.55 [-0.99, -0.16] | -0.26 [-0.35, -0.20] | 0.145 [0.033, 0.245] | 0.002 | 0.000 | reference better |
| seasonal_naive | 53 | -0.44 [-0.67, -0.25] | -0.96 [-1.22, -0.73] | -0.47 [-0.64, -0.34] | 0.099 [0.021, 0.128] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.801 |
| gat_parity | 0.859 |
| lstm | 0.859 |
| gnn_st_nograph | 0.864 |
| sarima | 0.878 |
| xgboost_parity | 0.887 |
| xgboost | 0.897 |
| arima | 0.908 |
| blend_baseline | 0.919 |
| lstm_parity | 0.975 |
| persistence | 1.000 |
| climatology | 1.010 |
| seasonal_naive | 1.176 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
