# Is `gnn_st_historyonly_tuned`'s lead bigger than chance? — horizon 4, `full`

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
| blend_baseline | 52 | -0.02 [-0.16, 0.09] | 0.03 [-0.14, 0.21] | -0.05 [-0.21, 0.09] | -0.002 [-0.042, 0.032] | 1.000 | 1.000 | not distinguishable |
| sarima | 52 | -0.11 [-0.22, 0.03] | -0.05 [-0.22, 0.10] | -0.02 [-0.05, 0.03] | -0.003 [-0.042, 0.041] | 0.679 | 1.000 | not distinguishable |
| flusight_baseline | 52 | -0.14 [-0.46, 0.27] | -0.51 [-0.95, -0.10] | -0.18 [-0.45, 0.10] | 0.021 [-0.018, 0.056] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | -0.14 [-0.46, 0.27] | -0.51 [-0.95, -0.10] | -0.17 [-0.42, 0.10] | 0.021 [-0.018, 0.056] | 1.000 | 1.000 | not distinguishable |
| lstm_tuned | 52 | -0.17 [-0.41, 0.04] | -0.01 [-0.36, 0.27] | -0.06 [-0.31, 0.15] | -0.013 [-0.132, 0.058] | 0.754 | 1.000 | not distinguishable |

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
