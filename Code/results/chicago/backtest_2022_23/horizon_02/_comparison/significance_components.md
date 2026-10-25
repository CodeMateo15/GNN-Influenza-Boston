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
| gnn_st_nodemofeat_tuned | 52 | 0.00 [-0.04, 0.06] | 0.02 [-0.04, 0.09] | 0.00 [-0.02, 0.03] | -0.004 [-0.016, 0.010] | 1.000 | 0.699 | not distinguishable |
| gnn_st_noweather_tuned | 52 | -0.00 [-0.03, 0.03] | -0.01 [-0.05, 0.03] | -0.01 [-0.03, 0.00] | 0.003 [-0.011, 0.017] | 1.000 | 0.232 | not distinguishable |
| gnn_st_historyonly_tuned | 52 | -0.04 [-0.12, 0.05] | -0.12 [-0.21, -0.04] | -0.07 [-0.11, -0.02] | 0.054 [0.026, 0.087] | 1.000 | 0.031 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.05 [-0.13, 0.01] | -0.11 [-0.21, -0.04] | -0.06 [-0.12, -0.03] | 0.070 [0.035, 0.111] | 0.576 | 0.031 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| lstm | 0.860 |
| gnn_st_nodemofeat_tuned | 0.863 |
| gnn_st | 0.863 |
| gnn_st_tuned | 0.866 |
| gnn_st_noweather_tuned | 0.874 |
| lstm_s10 | 0.883 |
| lstm_tuned | 0.886 |
| sarima | 0.899 |
| gnn_st_nograph_tuned | 0.908 |
| gnn_st_historyonly_tuned | 0.909 |
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
