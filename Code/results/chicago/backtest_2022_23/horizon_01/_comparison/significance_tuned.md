# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 1, `full`

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
| gnn_st_nograph_tuned | 52 | -0.09 [-0.19, 0.00] | -0.26 [-0.38, -0.15] | -0.11 [-0.17, -0.05] | 0.102 [0.071, 0.147] | 0.012 | 0.000 | not distinguishable |
| lstm_tuned | 52 | -0.15 [-0.30, -0.05] | -0.08 [-0.20, 0.02] | -0.06 [-0.16, 0.00] | -0.034 [-0.066, -0.026] | 0.002 | 0.022 | reference better |
| lstm_s10 | 52 | -0.18 [-0.33, -0.06] | -0.08 [-0.20, 0.01] | -0.07 [-0.17, -0.00] | -0.026 [-0.058, -0.007] | 0.001 | 0.022 | reference better |
| sarima | 52 | -0.19 [-0.27, -0.12] | -0.30 [-0.37, -0.22] | -0.15 [-0.20, -0.11] | 0.090 [0.049, 0.141] | 0.000 | 0.000 | reference better |
| xgboost_tuned | 52 | -0.19 [-0.37, -0.06] | -0.24 [-0.42, -0.09] | -0.13 [-0.24, -0.04] | 0.103 [0.038, 0.187] | 0.001 | 0.001 | reference better |
| flusight_baseline | 52 | -0.20 [-0.28, -0.10] | -0.67 [-0.76, -0.57] | -0.24 [-0.32, -0.15] | 0.123 [0.090, 0.147] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.20 [-0.28, -0.10] | -0.67 [-0.76, -0.57] | -0.28 [-0.35, -0.20] | 0.123 [0.090, 0.147] | 0.000 | 0.000 | reference better |
| blend_baseline | 52 | -0.25 [-0.53, -0.05] | -0.31 [-0.52, -0.14] | -0.21 [-0.39, -0.07] | 0.117 [0.068, 0.152] | 0.002 | 0.000 | reference better |
| colagnn_tuned | 52 | -0.34 [-0.77, -0.04] | -0.30 [-0.69, 0.02] | -0.17 [-0.43, 0.01] | 0.102 [0.024, 0.168] | 0.004 | 0.022 | reference better |
| gat_tuned | 52 | -0.57 [-1.19, -0.16] | -0.60 [-1.20, -0.06] | -0.33 [-0.79, -0.01] | 0.203 [0.036, 0.308] | 0.001 | 0.012 | reference better |
| dualtopo_tuned | 52 | -0.70 [-1.51, -0.16] | -0.91 [-1.76, -0.07] | -0.43 [-1.01, -0.02] | 0.867 [0.251, 1.181] | 0.002 | 0.012 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.806 |
| gnn_st_tuned | 0.806 |
| lstm_tuned | 0.849 |
| lstm | 0.854 |
| lstm_s10 | 0.856 |
| gnn_st_nograph | 0.874 |
| gnn_st_nograph_tuned | 0.880 |
| xgboost_parity | 0.891 |
| xgboost_tuned | 0.897 |
| sarima | 0.909 |
| colagnn_tuned | 0.924 |
| arima | 0.927 |
| blend_baseline | 0.949 |
| lstm_parity | 0.959 |
| xgboost | 0.969 |
| flusight_baseline | 0.971 |
| persistence | 1.000 |
| gat_parity | 1.012 |
| gat_tuned | 1.037 |
| dualtopo_tuned | 1.102 |
| climatology | 1.176 |
| seasonal_naive | 1.225 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
