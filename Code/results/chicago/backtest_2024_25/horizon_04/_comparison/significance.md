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
| sarima | 52 | -0.08 [-0.27, 0.05] | -0.15 [-0.37, 0.03] | -0.07 [-0.22, 0.03] | 0.051 [-0.022, 0.128] | 0.815 | 0.284 | not distinguishable |
| gnn_st_nograph | 52 | -0.08 [-0.17, -0.01] | -0.17 [-0.27, -0.08] | -0.07 [-0.12, -0.03] | 0.090 [0.036, 0.141] | 0.451 | 0.086 | reference better |
| blend_baseline | 52 | -0.12 [-0.35, 0.05] | -0.32 [-0.53, -0.11] | -0.09 [-0.17, -0.04] | 0.058 [0.034, 0.084] | 0.815 | 0.097 | not distinguishable |
| persistence | 52 | -0.13 [-0.36, 0.18] | -0.71 [-0.93, -0.46] | -0.25 [-0.36, -0.13] | 0.128 [0.071, 0.204] | 0.815 | 0.002 | not distinguishable |
| xgboost_parity | 52 | -0.14 [-0.26, -0.03] | -0.22 [-0.37, -0.08] | -0.10 [-0.19, -0.03] | 0.111 [0.046, 0.167] | 0.246 | 0.097 | reference better |
| xgboost | 52 | -0.15 [-0.30, -0.02] | -0.25 [-0.46, -0.07] | -0.12 [-0.23, -0.04] | 0.138 [0.049, 0.218] | 0.451 | 0.129 | reference better |
| arima | 52 | -0.27 [-0.39, -0.13] | -0.27 [-0.39, -0.14] | -0.16 [-0.23, -0.08] | 0.167 [0.110, 0.226] | 0.004 | 0.003 | reference better |
| seasonal_naive | 52 | -0.29 [-0.66, 0.07] | -0.82 [-1.21, -0.44] | -0.30 [-0.52, -0.10] | 0.192 [0.017, 0.354] | 0.769 | 0.096 | not distinguishable |
| lstm_parity | 52 | -0.35 [-0.73, -0.06] | -0.66 [-1.05, -0.29] | -0.27 [-0.54, -0.06] | 0.168 [0.110, 0.213] | 0.451 | 0.178 | reference better |
| climatology | 52 | -0.38 [-0.98, 0.03] | -0.82 [-1.46, -0.22] | -0.24 [-0.49, -0.06] | 0.144 [-0.024, 0.352] | 0.769 | 0.178 | not distinguishable |
| lstm | 52 | -0.45 [-0.82, -0.11] | -0.70 [-1.11, -0.27] | -0.33 [-0.65, -0.07] | 0.218 [0.090, 0.327] | 0.246 | 0.178 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.838 |
| gnn_st_nograph | 0.885 |
| sarima | 0.887 |
| blend_baseline | 0.898 |
| xgboost_parity | 0.907 |
| xgboost | 0.919 |
| arima | 0.941 |
| climatology | 0.994 |
| persistence | 1.000 |
| lstm_parity | 1.014 |
| seasonal_naive | 1.035 |
| lstm | 1.052 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
