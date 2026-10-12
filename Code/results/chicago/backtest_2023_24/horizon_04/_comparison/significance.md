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
| sarima | 52 | 0.05 [-0.04, 0.16] | 0.12 [0.06, 0.20] | 0.04 [0.01, 0.10] | -0.066 [-0.114, -0.023] | 1.000 | 0.443 | not distinguishable |
| blend_baseline | 52 | -0.03 [-0.15, 0.07] | -0.07 [-0.21, 0.05] | 0.01 [-0.02, 0.06] | -0.011 [-0.036, 0.015] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 52 | -0.05 [-0.07, -0.02] | -0.08 [-0.12, -0.05] | -0.02 [-0.04, -0.00] | 0.033 [0.013, 0.052] | 0.005 | 0.095 | reference better |
| lstm_parity | 52 | -0.05 [-0.08, -0.03] | -0.08 [-0.12, -0.05] | -0.03 [-0.04, -0.01] | 0.030 [0.009, 0.050] | 0.004 | 0.030 | reference better |
| xgboost_parity | 52 | -0.06 [-0.11, -0.00] | -0.01 [-0.05, 0.04] | -0.01 [-0.03, 0.01] | 0.021 [0.003, 0.040] | 0.210 | 1.000 | reference better |
| xgboost | 52 | -0.07 [-0.21, 0.05] | -0.02 [-0.17, 0.13] | -0.02 [-0.10, 0.04] | -0.051 [-0.109, 0.005] | 1.000 | 1.000 | not distinguishable |
| climatology | 52 | -0.11 [-0.34, 0.06] | -0.25 [-0.52, -0.01] | -0.02 [-0.09, 0.05] | -0.038 [-0.095, 0.017] | 1.000 | 1.000 | not distinguishable |
| lstm | 52 | -0.20 [-0.32, -0.05] | -0.11 [-0.23, -0.00] | -0.05 [-0.08, -0.01] | 0.015 [-0.044, 0.056] | 0.073 | 0.221 | reference better |
| arima | 52 | -0.30 [-0.51, -0.08] | -0.18 [-0.36, 0.01] | -0.08 [-0.16, 0.02] | 0.140 [0.066, 0.190] | 0.098 | 0.680 | reference better |
| persistence | 52 | -0.37 [-0.55, -0.19] | -0.67 [-0.89, -0.48] | -0.22 [-0.33, -0.12] | 0.115 [0.055, 0.161] | 0.004 | 0.002 | reference better |
| seasonal_naive | 52 | -0.44 [-0.67, -0.22] | -0.81 [-1.06, -0.54] | -0.38 [-0.55, -0.21] | 0.066 [-0.079, 0.177] | 0.008 | 0.001 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| sarima | 0.818 |
| blend_baseline | 0.839 |
| gnn_st | 0.848 |
| xgboost_parity | 0.856 |
| climatology | 0.863 |
| xgboost | 0.864 |
| gnn_st_nograph | 0.865 |
| lstm_parity | 0.867 |
| lstm | 0.880 |
| arima | 0.900 |
| persistence | 1.000 |
| seasonal_naive | 1.104 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
