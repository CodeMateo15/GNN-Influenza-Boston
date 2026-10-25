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
| gnn_st_historyonly_tuned | 52 | -0.01 [-0.04, 0.03] | -0.03 [-0.06, 0.03] | -0.02 [-0.05, 0.01] | -0.001 [-0.013, 0.015] | 0.527 | 0.208 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.10 [-0.25, 0.01] | -0.17 [-0.32, -0.01] | -0.08 [-0.17, -0.00] | 0.075 [-0.013, 0.141] | 0.407 | 0.208 | not distinguishable |
| gnn_st_noweather_tuned | 52 | -0.11 [-0.22, -0.02] | -0.15 [-0.26, -0.05] | -0.08 [-0.15, -0.03] | 0.056 [-0.007, 0.105] | 0.223 | 0.103 | reference better |
| gnn_st_nodemofeat_tuned | 52 | -0.11 [-0.27, 0.00] | -0.18 [-0.34, -0.04] | -0.09 [-0.18, -0.01] | 0.059 [-0.014, 0.119] | 0.407 | 0.208 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_tuned | 0.883 |
| xgboost_tuned | 0.896 |
| xgboost_parity | 0.896 |
| gnn_st_historyonly_tuned | 0.898 |
| gnn_st_nograph | 0.903 |
| lstm_s10 | 0.906 |
| sarima | 0.907 |
| lstm_parity | 0.911 |
| arima | 0.917 |
| colagnn_tuned | 0.921 |
| gnn_st | 0.924 |
| blend_baseline | 0.925 |
| gnn_st_nograph_tuned | 0.929 |
| gnn_st_noweather_tuned | 0.931 |
| lstm_tuned | 0.932 |
| gnn_st_nodemofeat_tuned | 0.934 |
| xgboost | 0.988 |
| persistence | 1.000 |
| flusight_baseline | 1.004 |
| lstm | 1.005 |
| climatology | 1.008 |
| seasonal_naive | 1.050 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
