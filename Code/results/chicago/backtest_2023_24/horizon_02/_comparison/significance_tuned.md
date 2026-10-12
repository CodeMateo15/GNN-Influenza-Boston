# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 2, `full`

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
| sarima | 52 | -0.11 [-0.18, -0.04] | -0.09 [-0.15, -0.04] | -0.05 [-0.09, -0.02] | 0.036 [0.013, 0.066] | 0.004 | 0.007 | reference better |
| gnn_st_nograph_tuned | 52 | -0.12 [-0.18, -0.06] | -0.09 [-0.16, -0.04] | -0.06 [-0.10, -0.02] | 0.080 [0.046, 0.117] | 0.001 | 0.018 | reference better |
| blend_baseline | 52 | -0.13 [-0.26, -0.04] | -0.15 [-0.29, -0.04] | -0.06 [-0.11, -0.02] | 0.065 [0.041, 0.096] | 0.018 | 0.018 | reference better |
| xgboost_tuned | 52 | -0.15 [-0.26, -0.05] | -0.04 [-0.14, 0.04] | -0.06 [-0.13, -0.01] | 0.037 [-0.005, 0.088] | 0.009 | 0.086 | reference better |
| lstm_tuned | 52 | -0.16 [-0.29, -0.05] | -0.07 [-0.25, 0.05] | -0.04 [-0.11, 0.01] | -0.015 [-0.067, 0.027] | 0.018 | 0.298 | reference better |
| colagnn_tuned | 52 | -0.16 [-0.30, -0.03] | -0.02 [-0.10, 0.06] | -0.02 [-0.07, 0.02] | 0.023 [-0.012, 0.059] | 0.018 | 0.298 | reference better |
| lstm_s10 | 52 | -0.18 [-0.29, -0.07] | -0.07 [-0.19, 0.04] | -0.04 [-0.09, 0.01] | -0.018 [-0.068, 0.016] | 0.004 | 0.298 | reference better |
| flusight_baseline | 52 | -0.34 [-0.44, -0.23] | -0.65 [-0.76, -0.53] | -0.28 [-0.38, -0.18] | 0.136 [0.098, 0.170] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.34 [-0.44, -0.23] | -0.65 [-0.76, -0.53] | -0.25 [-0.32, -0.17] | 0.136 [0.098, 0.170] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.817 |
| gnn_st_tuned | 0.822 |
| colagnn_tuned | 0.840 |
| lstm_s10 | 0.850 |
| lstm_tuned | 0.853 |
| xgboost_parity | 0.853 |
| lstm | 0.855 |
| sarima | 0.862 |
| gnn_st_nograph | 0.863 |
| gnn_st_nograph_tuned | 0.863 |
| xgboost | 0.864 |
| xgboost_tuned | 0.867 |
| blend_baseline | 0.868 |
| arima | 0.912 |
| climatology | 0.921 |
| lstm_parity | 0.939 |
| persistence | 1.000 |
| flusight_baseline | 1.023 |
| seasonal_naive | 1.178 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
