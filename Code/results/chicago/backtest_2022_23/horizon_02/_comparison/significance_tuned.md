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
| gnn_st_nograph_tuned | 52 | -0.05 [-0.13, 0.01] | -0.11 [-0.21, -0.04] | -0.06 [-0.12, -0.03] | 0.070 [0.035, 0.111] | 0.576 | 0.062 | not distinguishable |
| sarima | 52 | -0.08 [-0.21, 0.11] | -0.10 [-0.24, 0.07] | -0.05 [-0.12, 0.05] | 0.021 [-0.021, 0.067] | 0.720 | 0.630 | not distinguishable |
| flusight_baseline | 52 | -0.11 [-0.33, 0.20] | -0.51 [-0.74, -0.26] | -0.17 [-0.32, 0.02] | 0.065 [0.028, 0.107] | 0.720 | 0.095 | not distinguishable |
| persistence | 52 | -0.11 [-0.33, 0.20] | -0.51 [-0.74, -0.26] | -0.20 [-0.35, -0.02] | 0.065 [0.028, 0.107] | 0.720 | 0.024 | not distinguishable |
| blend_baseline | 52 | -0.13 [-0.29, -0.03] | -0.11 [-0.23, 0.00] | -0.12 [-0.25, -0.03] | 0.058 [0.012, 0.103] | 0.296 | 0.095 | reference better |
| xgboost_tuned | 52 | -0.17 [-0.35, -0.05] | -0.15 [-0.33, 0.01] | -0.10 [-0.22, -0.00] | 0.099 [0.019, 0.208] | 0.186 | 0.282 | reference better |
| lstm_s10 | 52 | -0.17 [-0.36, -0.00] | 0.05 [-0.13, 0.21] | -0.03 [-0.13, 0.05] | -0.051 [-0.126, 0.022] | 0.296 | 1.000 | reference better |
| lstm_tuned | 52 | -0.18 [-0.41, -0.01] | 0.04 [-0.20, 0.21] | -0.03 [-0.18, 0.06] | -0.066 [-0.151, 0.018] | 0.335 | 1.000 | reference better |
| colagnn_tuned | 52 | -0.27 [-0.53, -0.09] | -0.14 [-0.40, 0.07] | -0.09 [-0.27, 0.03] | 0.072 [-0.049, 0.156] | 0.043 | 0.630 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| lstm | 0.860 |
| gnn_st | 0.863 |
| gnn_st_tuned | 0.866 |
| lstm_s10 | 0.883 |
| lstm_tuned | 0.886 |
| sarima | 0.899 |
| gnn_st_nograph_tuned | 0.908 |
| gnn_st_nograph | 0.909 |
| xgboost_parity | 0.924 |
| colagnn_tuned | 0.925 |
| arima | 0.927 |
| xgboost_tuned | 0.929 |
| blend_baseline | 0.947 |
| lstm_parity | 0.952 |
| flusight_baseline | 0.977 |
| xgboost | 0.991 |
| persistence | 1.000 |
| climatology | 1.115 |
| seasonal_naive | 1.162 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
