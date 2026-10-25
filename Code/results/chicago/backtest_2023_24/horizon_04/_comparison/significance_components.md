# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 4, `full`

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
| gnn_st_nodemofeat_tuned | 52 | 0.04 [-0.01, 0.09] | -0.01 [-0.05, 0.02] | -0.00 [-0.02, 0.01] | -0.006 [-0.021, 0.006] | 0.504 | 0.667 | not distinguishable |
| gnn_st_historyonly_tuned | 52 | 0.00 [-0.07, 0.07] | -0.09 [-0.16, -0.02] | -0.02 [-0.04, 0.01] | 0.030 [-0.001, 0.052] | 1.000 | 0.274 | not distinguishable |
| gnn_st_noweather_tuned | 52 | -0.01 [-0.06, 0.04] | -0.10 [-0.15, -0.05] | -0.03 [-0.05, -0.01] | 0.039 [0.007, 0.064] | 1.000 | 0.019 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.02 [-0.09, 0.05] | -0.10 [-0.18, -0.03] | -0.03 [-0.06, -0.00] | 0.042 [0.008, 0.069] | 1.000 | 0.145 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| sarima | 0.818 |
| gnn_st_tuned | 0.833 |
| gnn_st_nodemofeat_tuned | 0.836 |
| blend_baseline | 0.839 |
| gnn_st_historyonly_tuned | 0.845 |
| gnn_st | 0.848 |
| gnn_st_nograph_tuned | 0.852 |
| gnn_st_noweather_tuned | 0.855 |
| xgboost_parity | 0.856 |
| xgboost_tuned | 0.860 |
| climatology | 0.863 |
| xgboost | 0.864 |
| gnn_st_nograph | 0.865 |
| lstm_parity | 0.867 |
| lstm_tuned | 0.873 |
| lstm_s10 | 0.875 |
| lstm | 0.880 |
| arima | 0.900 |
| colagnn_tuned | 0.931 |
| persistence | 1.000 |
| flusight_baseline | 1.035 |
| seasonal_naive | 1.104 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
