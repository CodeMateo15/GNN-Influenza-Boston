# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 4, `post_covid`

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
| gnn_st_noweather_tuned | 52 | 0.03 [-0.12, 0.22] | -0.03 [-0.18, 0.20] | 0.02 [-0.09, 0.14] | -0.014 [-0.032, 0.004] | 1.000 | 1.000 | not distinguishable |
| gnn_st_historyonly_tuned | 52 | -0.04 [-0.39, 0.31] | -0.32 [-0.69, 0.33] | -0.04 [-0.33, 0.21] | -0.023 [-0.052, 0.001] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nodemofeat_tuned | 52 | -0.06 [-0.28, 0.18] | -0.21 [-0.41, 0.15] | -0.06 [-0.23, 0.12] | -0.009 [-0.024, 0.006] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.09 [-0.50, 0.30] | -0.41 [-0.83, 0.31] | -0.08 [-0.41, 0.21] | -0.022 [-0.054, 0.004] | 1.000 | 1.000 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| seasonal_naive | 0.680 |
| transfer_finetune_from_pooled_all3 | 0.705 |
| transfer_zeroshot_from_pooled_others | 0.706 |
| transfer_zeroshot_from_pooled_all3 | 0.712 |
| transfer_finetune_from_pooled_others | 0.719 |
| gnn_st_noweather_tuned | 0.745 |
| gnn_st_tuned | 0.747 |
| gnn_st_historyonly_tuned | 0.752 |
| gnn_st_nodemofeat_tuned | 0.754 |
| gnn_st_nograph_tuned | 0.756 |
| gnn_st_nograph | 0.760 |
| blend_baseline | 0.763 |
| transfer_zeroshot_from_boston | 0.764 |
| gnn_st | 0.766 |
| transfer_finetune_from_boston | 0.768 |
| gnn_st_noadapt | 0.768 |
| sarima | 0.769 |
| lstm_tuned | 0.777 |
| xgboost_tuned | 0.780 |
| xgboost_parity | 0.783 |
| lstm_parity | 0.792 |
| climatology | 0.798 |
| xgboost | 0.817 |
| colagnn_tuned | 0.842 |
| flusight_baseline | 0.970 |
| persistence | 1.000 |
| arima | 1.102 |
| lstm_s10 | 1.107 |
| lstm | 1.126 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
