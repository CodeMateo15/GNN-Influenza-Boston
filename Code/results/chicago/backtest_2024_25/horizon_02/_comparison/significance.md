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
| gnn_st_nograph | 52 | -0.17 [-0.33, -0.05] | -0.22 [-0.40, -0.08] | -0.10 [-0.18, -0.04] | 0.091 [0.049, 0.142] | 0.040 | 0.007 | reference better |
| xgboost | 52 | -0.22 [-0.46, -0.06] | -0.23 [-0.49, -0.03] | -0.13 [-0.25, -0.04] | 0.089 [0.028, 0.147] | 0.040 | 0.018 | reference better |
| xgboost_parity | 52 | -0.23 [-0.46, -0.06] | -0.24 [-0.47, -0.04] | -0.13 [-0.25, -0.04] | 0.089 [0.037, 0.137] | 0.040 | 0.018 | reference better |
| persistence | 52 | -0.23 [-0.35, -0.10] | -0.76 [-0.89, -0.63] | -0.28 [-0.35, -0.21] | 0.133 [0.103, 0.179] | 0.001 | 0.000 | reference better |
| sarima | 52 | -0.24 [-0.47, -0.08] | -0.23 [-0.45, -0.06] | -0.13 [-0.27, -0.04] | 0.074 [0.018, 0.115] | 0.024 | 0.016 | reference better |
| blend_baseline | 52 | -0.33 [-0.70, -0.05] | -0.44 [-0.76, -0.16] | -0.19 [-0.31, -0.09] | 0.091 [0.063, 0.129] | 0.040 | 0.001 | reference better |
| arima | 52 | -0.40 [-0.60, -0.23] | -0.54 [-0.95, -0.23] | -0.24 [-0.38, -0.13] | 0.142 [0.099, 0.176] | 0.000 | 0.000 | reference better |
| lstm | 52 | -0.45 [-0.87, -0.12] | -0.56 [-0.95, -0.18] | -0.30 [-0.58, -0.08] | 0.050 [-0.001, 0.108] | 0.024 | 0.013 | reference better |
| lstm_parity | 52 | -0.50 [-0.81, -0.27] | -0.71 [-0.96, -0.47] | -0.32 [-0.48, -0.19] | 0.187 [0.148, 0.228] | 0.000 | 0.000 | reference better |
| seasonal_naive | 52 | -0.58 [-1.04, -0.23] | -1.05 [-1.51, -0.69] | -0.44 [-0.69, -0.25] | 0.248 [0.078, 0.387] | 0.009 | 0.000 | reference better |
| climatology | 52 | -0.67 [-1.48, -0.08] | -1.05 [-1.85, -0.28] | -0.37 [-0.68, -0.14] | 0.200 [0.039, 0.383] | 0.040 | 0.005 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.801 |
| gnn_st_nograph | 0.873 |
| xgboost | 0.891 |
| xgboost_parity | 0.891 |
| sarima | 0.895 |
| blend_baseline | 0.933 |
| arima | 0.968 |
| persistence | 1.000 |
| lstm | 1.010 |
| lstm_parity | 1.028 |
| climatology | 1.064 |
| seasonal_naive | 1.110 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
