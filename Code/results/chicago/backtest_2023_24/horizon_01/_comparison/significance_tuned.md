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
| colagnn_tuned | 52 | -0.06 [-0.12, 0.00] | -0.01 [-0.06, 0.04] | -0.02 [-0.05, 0.01] | -0.005 [-0.025, 0.017] | 0.028 | 0.216 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.08 [-0.13, -0.03] | -0.10 [-0.16, -0.06] | -0.06 [-0.10, -0.02] | 0.073 [0.048, 0.117] | 0.004 | 0.002 | reference better |
| lstm_tuned | 52 | -0.10 [-0.20, -0.02] | -0.10 [-0.24, -0.01] | -0.04 [-0.10, 0.00] | -0.009 [-0.046, 0.018] | 0.028 | 0.185 | reference better |
| xgboost_tuned | 52 | -0.11 [-0.17, -0.06] | -0.09 [-0.14, -0.04] | -0.06 [-0.09, -0.03] | 0.060 [0.039, 0.102] | 0.000 | 0.000 | reference better |
| lstm_s10 | 52 | -0.12 [-0.21, -0.04] | -0.09 [-0.21, -0.00] | -0.03 [-0.08, 0.01] | -0.022 [-0.061, -0.002] | 0.004 | 0.193 | reference better |
| sarima | 52 | -0.14 [-0.20, -0.09] | -0.18 [-0.23, -0.12] | -0.09 [-0.12, -0.06] | 0.071 [0.048, 0.102] | 0.000 | 0.000 | reference better |
| blend_baseline | 52 | -0.14 [-0.29, -0.05] | -0.22 [-0.35, -0.11] | -0.10 [-0.15, -0.05] | 0.078 [0.056, 0.119] | 0.004 | 0.000 | reference better |
| gat_tuned | 52 | -0.18 [-0.29, -0.09] | -0.13 [-0.22, -0.04] | -0.08 [-0.16, -0.02] | 0.024 [-0.017, 0.058] | 0.000 | 0.004 | reference better |
| flusight_baseline | 52 | -0.30 [-0.39, -0.20] | -0.66 [-0.74, -0.56] | -0.27 [-0.35, -0.18] | 0.133 [0.108, 0.169] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.30 [-0.39, -0.20] | -0.66 [-0.74, -0.56] | -0.25 [-0.31, -0.18] | 0.133 [0.108, 0.169] | 0.000 | 0.000 | reference better |
| dualtopo_tuned | 52 | -0.53 [-0.92, -0.23] | -0.58 [-1.01, -0.23] | -0.35 [-0.65, -0.14] | 0.148 [0.045, 0.226] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_tuned | 0.814 |
| gnn_st | 0.818 |
| colagnn_tuned | 0.828 |
| lstm_s10 | 0.837 |
| lstm | 0.844 |
| lstm_tuned | 0.846 |
| xgboost_parity | 0.855 |
| gnn_st_nograph_tuned | 0.857 |
| xgboost_tuned | 0.858 |
| gnn_st_nograph | 0.859 |
| xgboost | 0.873 |
| gat_parity | 0.874 |
| gat_tuned | 0.874 |
| sarima | 0.879 |
| blend_baseline | 0.886 |
| arima | 0.914 |
| climatology | 0.958 |
| lstm_parity | 0.958 |
| persistence | 1.000 |
| flusight_baseline | 1.015 |
| dualtopo_tuned | 1.077 |
| seasonal_naive | 1.226 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
