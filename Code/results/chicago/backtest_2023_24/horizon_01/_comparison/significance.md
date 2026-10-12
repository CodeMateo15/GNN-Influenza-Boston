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
| gnn_st_nograph | 52 | -0.09 [-0.14, -0.03] | -0.11 [-0.16, -0.07] | -0.05 [-0.09, -0.02] | 0.070 [0.044, 0.106] | 0.001 | 0.001 | reference better |
| xgboost_parity | 52 | -0.11 [-0.18, -0.04] | -0.08 [-0.13, -0.03] | -0.05 [-0.07, -0.03] | 0.050 [0.028, 0.085] | 0.000 | 0.000 | reference better |
| sarima | 52 | -0.14 [-0.20, -0.09] | -0.17 [-0.22, -0.13] | -0.08 [-0.12, -0.05] | 0.067 [0.044, 0.093] | 0.000 | 0.000 | reference better |
| blend_baseline | 52 | -0.14 [-0.28, -0.05] | -0.21 [-0.33, -0.12] | -0.09 [-0.14, -0.05] | 0.074 [0.054, 0.108] | 0.001 | 0.000 | reference better |
| xgboost | 52 | -0.15 [-0.25, -0.06] | -0.09 [-0.16, -0.02] | -0.07 [-0.13, -0.03] | 0.053 [0.010, 0.102] | 0.000 | 0.001 | reference better |
| lstm | 52 | -0.16 [-0.25, -0.08] | -0.13 [-0.26, -0.03] | -0.03 [-0.08, 0.00] | -0.016 [-0.058, 0.001] | 0.000 | 0.066 | reference better |
| gat_parity | 52 | -0.18 [-0.30, -0.08] | -0.12 [-0.21, -0.04] | -0.07 [-0.15, -0.02] | 0.020 [-0.020, 0.048] | 0.000 | 0.002 | reference better |
| arima | 52 | -0.25 [-0.32, -0.16] | -0.27 [-0.34, -0.20] | -0.13 [-0.18, -0.09] | 0.130 [0.100, 0.155] | 0.000 | 0.000 | reference better |
| lstm_parity | 52 | -0.29 [-0.36, -0.23] | -0.48 [-0.54, -0.41] | -0.19 [-0.23, -0.14] | 0.107 [0.081, 0.137] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.30 [-0.38, -0.21] | -0.65 [-0.72, -0.57] | -0.24 [-0.30, -0.18] | 0.129 [0.108, 0.158] | 0.000 | 0.000 | reference better |
| climatology | 52 | -0.34 [-0.70, -0.11] | -0.53 [-0.91, -0.23] | -0.19 [-0.33, -0.09] | 0.093 [0.014, 0.163] | 0.001 | 0.000 | reference better |
| seasonal_naive | 52 | -0.67 [-0.93, -0.43] | -1.08 [-1.37, -0.80] | -0.54 [-0.74, -0.37] | 0.197 [0.060, 0.294] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.818 |
| lstm | 0.844 |
| xgboost_parity | 0.855 |
| gnn_st_nograph | 0.859 |
| xgboost | 0.873 |
| gat_parity | 0.874 |
| sarima | 0.879 |
| blend_baseline | 0.886 |
| arima | 0.914 |
| climatology | 0.958 |
| lstm_parity | 0.958 |
| persistence | 1.000 |
| seasonal_naive | 1.226 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
