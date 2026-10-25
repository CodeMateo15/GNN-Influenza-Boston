# Is `gnn_st_historyonly_tuned`'s lead bigger than chance? — horizon 1, `full`

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
| lstm_tuned | 52 | -0.04 [-0.13, 0.03] | 0.23 [0.14, 0.29] | 0.07 [-0.00, 0.12] | -0.136 [-0.191, -0.113] | 0.311 | 0.038 | not distinguishable |
| sarima | 52 | -0.08 [-0.14, -0.01] | 0.01 [-0.05, 0.06] | -0.02 [-0.05, 0.03] | -0.011 [-0.038, 0.019] | 0.018 | 0.358 | reference better |
| flusight_baseline | 52 | -0.09 [-0.20, 0.07] | -0.37 [-0.44, -0.27] | -0.11 [-0.18, -0.01] | 0.021 [-0.009, 0.039] | 0.074 | 0.001 | not distinguishable |
| persistence | 52 | -0.09 [-0.20, 0.07] | -0.37 [-0.44, -0.27] | -0.15 [-0.21, -0.06] | 0.021 [-0.009, 0.039] | 0.074 | 0.000 | not distinguishable |
| blend_baseline | 52 | -0.14 [-0.36, 0.00] | -0.01 [-0.17, 0.13] | -0.07 [-0.24, 0.05] | 0.016 [-0.029, 0.037] | 0.034 | 0.148 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_noweather_tuned | 0.799 |
| gnn_st_nodemofeat_tuned | 0.806 |
| gnn_st | 0.806 |
| gnn_st_tuned | 0.806 |
| lstm_tuned | 0.849 |
| lstm | 0.854 |
| lstm_s10 | 0.856 |
| gnn_st_nograph | 0.874 |
| gnn_st_nograph_tuned | 0.880 |
| xgboost_parity | 0.891 |
| xgboost_tuned | 0.897 |
| gnn_st_historyonly_tuned | 0.897 |
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
