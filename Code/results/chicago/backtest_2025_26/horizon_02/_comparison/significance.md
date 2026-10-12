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
| blend_baseline | 53 | -0.09 [-0.20, -0.02] | -0.22 [-0.32, -0.14] | -0.12 [-0.16, -0.08] | 0.097 [0.060, 0.143] | 0.093 | 0.000 | reference better |
| gnn_st_nograph | 53 | -0.12 [-0.25, -0.02] | -0.13 [-0.31, -0.01] | -0.07 [-0.14, -0.03] | 0.107 [0.022, 0.171] | 0.093 | 0.013 | reference better |
| sarima | 53 | -0.13 [-0.21, -0.07] | -0.10 [-0.18, -0.02] | -0.07 [-0.12, -0.04] | 0.061 [0.004, 0.103] | 0.005 | 0.002 | reference better |
| xgboost_parity | 53 | -0.15 [-0.28, -0.06] | -0.15 [-0.30, -0.04] | -0.10 [-0.15, -0.06] | 0.104 [0.041, 0.164] | 0.017 | 0.000 | reference better |
| lstm | 53 | -0.16 [-0.25, -0.08] | -0.11 [-0.20, -0.04] | -0.09 [-0.11, -0.05] | 0.017 [-0.043, 0.044] | 0.001 | 0.000 | reference better |
| lstm_parity | 53 | -0.18 [-0.24, -0.13] | -0.43 [-0.49, -0.36] | -0.18 [-0.21, -0.15] | 0.138 [0.092, 0.199] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -0.19 [-0.33, -0.09] | -0.16 [-0.33, -0.05] | -0.11 [-0.17, -0.06] | 0.118 [0.032, 0.190] | 0.010 | 0.002 | reference better |
| arima | 53 | -0.23 [-0.35, -0.12] | -0.22 [-0.37, -0.08] | -0.14 [-0.19, -0.08] | 0.159 [0.056, 0.245] | 0.000 | 0.000 | reference better |
| climatology | 53 | -0.24 [-0.61, -0.00] | -0.42 [-0.81, -0.11] | -0.20 [-0.27, -0.13] | 0.093 [-0.009, 0.201] | 0.093 | 0.000 | reference better |
| persistence | 53 | -0.26 [-0.33, -0.19] | -0.70 [-0.78, -0.62] | -0.25 [-0.30, -0.19] | 0.156 [0.096, 0.231] | 0.000 | 0.000 | reference better |
| seasonal_naive | 53 | -0.32 [-0.57, -0.07] | -0.83 [-1.10, -0.55] | -0.40 [-0.56, -0.25] | 0.047 [-0.030, 0.097] | 0.019 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st | 0.811 |
| sarima | 0.866 |
| gnn_st_nograph | 0.867 |
| lstm | 0.876 |
| xgboost_parity | 0.888 |
| xgboost | 0.893 |
| blend_baseline | 0.904 |
| arima | 0.915 |
| lstm_parity | 0.950 |
| climatology | 0.962 |
| persistence | 1.000 |
| seasonal_naive | 1.113 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
