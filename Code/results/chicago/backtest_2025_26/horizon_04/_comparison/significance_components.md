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
| gnn_st_noweather_tuned | 53 | -0.00 [-0.03, 0.02] | -0.02 [-0.05, 0.01] | -0.01 [-0.03, 0.01] | 0.009 [-0.009, 0.027] | 1.000 | 1.000 | not distinguishable |
| gnn_st_historyonly_tuned | 53 | -0.01 [-0.12, 0.07] | -0.06 [-0.21, 0.06] | -0.03 [-0.06, 0.01] | 0.044 [0.001, 0.086] | 1.000 | 0.748 | not distinguishable |
| gnn_st_nodemofeat_tuned | 53 | -0.01 [-0.02, 0.01] | -0.01 [-0.03, 0.01] | -0.00 [-0.01, 0.01] | 0.003 [-0.009, 0.012] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph_tuned | 53 | -0.08 [-0.18, 0.02] | -0.05 [-0.20, 0.08] | -0.02 [-0.09, 0.04] | 0.064 [-0.024, 0.151] | 0.712 | 1.000 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.770 |
| transfer_zeroshot_from_boston | 0.783 |
| gnn_st_tuned | 0.783 |
| gnn_st_nodemofeat_tuned | 0.784 |
| gnn_st_noadapt | 0.785 |
| gnn_st | 0.787 |
| gnn_st_noweather_tuned | 0.788 |
| colagnn_tuned | 0.796 |
| gnn_st_nograph_tuned | 0.798 |
| sarima | 0.799 |
| gnn_st_historyonly_tuned | 0.800 |
| xgboost_tuned | 0.803 |
| gnn_st_nograph | 0.812 |
| xgboost | 0.819 |
| xgboost_parity | 0.830 |
| lstm_tuned | 0.846 |
| climatology | 0.849 |
| lstm_parity | 0.849 |
| blend_baseline | 0.849 |
| lstm_s10 | 0.867 |
| lstm | 0.872 |
| arima | 0.888 |
| seasonal_naive | 0.982 |
| flusight_baseline | 0.993 |
| persistence | 1.000 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
