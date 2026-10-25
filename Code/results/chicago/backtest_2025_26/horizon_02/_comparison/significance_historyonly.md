# Is `gnn_st_historyonly_tuned`'s lead bigger than chance? — horizon 2, `full`

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
| blend_baseline | 53 | -0.01 [-0.05, 0.03] | -0.11 [-0.16, -0.07] | -0.05 [-0.08, -0.01] | 0.012 [-0.016, 0.057] | 1.000 | 0.011 | not distinguishable |
| lstm_tuned | 53 | -0.01 [-0.07, 0.06] | 0.07 [-0.01, 0.17] | 0.02 [-0.01, 0.06] | -0.097 [-0.147, -0.050] | 1.000 | 0.693 | not distinguishable |
| sarima | 53 | -0.04 [-0.11, 0.02] | 0.01 [-0.08, 0.11] | -0.00 [-0.04, 0.04] | -0.024 [-0.052, 0.013] | 0.431 | 0.883 | not distinguishable |
| flusight_baseline | 53 | -0.17 [-0.27, -0.05] | -0.60 [-0.70, -0.47] | -0.17 [-0.24, -0.10] | 0.071 [0.032, 0.127] | 0.014 | 0.000 | reference better |
| persistence | 53 | -0.17 [-0.27, -0.05] | -0.60 [-0.70, -0.47] | -0.18 [-0.24, -0.12] | 0.071 [0.032, 0.127] | 0.014 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_nodemofeat_tuned | 0.806 |
| gnn_st_noweather_tuned | 0.810 |
| transfer_finetune_from_boston | 0.810 |
| gnn_st | 0.811 |
| gnn_st_tuned | 0.811 |
| gnn_st_noadapt | 0.811 |
| colagnn_tuned | 0.824 |
| lstm_tuned | 0.849 |
| transfer_zeroshot_from_boston | 0.854 |
| gnn_st_historyonly_tuned | 0.865 |
| lstm_s10 | 0.866 |
| sarima | 0.866 |
| gnn_st_nograph_tuned | 0.867 |
| gnn_st_nograph | 0.867 |
| xgboost_tuned | 0.871 |
| lstm | 0.876 |
| xgboost_parity | 0.888 |
| xgboost | 0.893 |
| blend_baseline | 0.904 |
| arima | 0.915 |
| lstm_parity | 0.950 |
| climatology | 0.962 |
| flusight_baseline | 0.995 |
| persistence | 1.000 |
| seasonal_naive | 1.113 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
