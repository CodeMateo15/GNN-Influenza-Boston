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
| gnn_st_nograph | 52 | 0.11 [-0.10, 0.29] | 0.20 [0.02, 0.37] | 0.09 [-0.03, 0.20] | 0.037 [-0.006, 0.096] | 0.447 | 0.105 | not distinguishable |
| xgboost_parity | 52 | 0.05 [-0.17, 0.22] | 0.19 [-0.03, 0.39] | 0.06 [-0.09, 0.20] | 0.034 [-0.023, 0.108] | 1.000 | 0.728 | not distinguishable |
| sarima | 52 | 0.03 [-0.10, 0.16] | 0.12 [-0.03, 0.27] | 0.04 [-0.05, 0.13] | 0.023 [-0.020, 0.081] | 1.000 | 0.915 | not distinguishable |
| persistence | 52 | 0.02 [-0.06, 0.12] | -0.25 [-0.33, -0.16] | -0.09 [-0.14, -0.03] | 0.056 [0.034, 0.080] | 1.000 | 0.000 | not distinguishable |
| arima | 52 | -0.01 [-0.20, 0.15] | 0.10 [-0.08, 0.26] | 0.01 [-0.11, 0.12] | 0.073 [0.033, 0.107] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 52 | -0.03 [-0.37, 0.21] | 0.10 [-0.15, 0.34] | -0.02 [-0.24, 0.17] | 0.051 [0.015, 0.081] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 52 | -0.04 [-0.12, 0.06] | -0.13 [-0.22, -0.03] | -0.06 [-0.11, 0.01] | 0.056 [0.035, 0.081] | 1.000 | 0.089 | not distinguishable |
| xgboost | 52 | -0.13 [-0.56, 0.15] | -0.02 [-0.49, 0.39] | -0.05 [-0.34, 0.17] | 0.111 [-0.023, 0.253] | 1.000 | 1.000 | not distinguishable |
| climatology | 52 | -0.41 [-1.19, 0.14] | -0.45 [-1.22, 0.27] | -0.35 [-0.93, 0.10] | 0.288 [0.022, 0.443] | 0.268 | 0.125 | not distinguishable |
| lstm | 52 | -0.45 [-1.19, 0.08] | -0.39 [-1.13, 0.28] | -0.26 [-0.81, 0.13] | 0.312 [0.045, 0.416] | 0.134 | 0.315 | not distinguishable |
| seasonal_naive | 52 | -0.48 [-1.19, 0.03] | -0.85 [-1.53, -0.27] | -0.42 [-0.75, -0.14] | 0.307 [0.065, 0.465] | 0.083 | 0.000 | not distinguishable |
| gat_parity | 52 | -2705279.15 [-6463892.08, -351085.11] | -14270950.81 [-23282458.80, -3757443.38] | -1653601.33 [-2742127.59, -812298.41] | 0.088 [-0.007, 0.210] | 0.050 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_nograph | 0.874 |
| xgboost_parity | 0.893 |
| sarima | 0.909 |
| arima | 0.927 |
| gnn_st | 0.935 |
| blend_baseline | 0.949 |
| xgboost | 0.970 |
| lstm_parity | 0.974 |
| persistence | 1.000 |
| lstm | 1.114 |
| climatology | 1.176 |
| seasonal_naive | 1.225 |
| gat_parity | 1148267.120 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
