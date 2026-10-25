# Is `gnn_st_historyonly_tuned`'s lead bigger than chance? — horizon 2, `post_covid`

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
| sarima | 52 | -0.34 [-1.02, 0.18] | -0.54 [-1.35, 0.27] | -0.44 [-1.08, 0.02] | 0.062 [-0.006, 0.098] | 0.636 | 0.303 | not distinguishable |
| blend_baseline | 52 | -0.72 [-1.36, -0.27] | -1.26 [-2.11, -0.38] | -0.28 [-0.77, 0.02] | 0.006 [-0.019, 0.026] | 0.017 | 0.320 | reference better |
| lstm_tuned | 52 | -0.94 [-2.02, -0.21] | -1.85 [-3.21, -0.33] | -1.72 [-3.54, -0.45] | 0.034 [-0.017, 0.090] | 0.122 | 0.045 | reference better |
| flusight_baseline | 52 | -1.14 [-3.36, 1.15] | -0.08 [-5.41, 4.27] | -0.69 [-2.49, 1.33] | 0.057 [0.016, 0.174] | 0.636 | 0.888 | not distinguishable |
| persistence | 52 | -1.14 [-3.36, 1.15] | -0.08 [-5.41, 4.27] | -0.49 [-1.91, 1.45] | 0.057 [0.016, 0.174] | 0.636 | 0.888 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_zeroshot_from_pooled_others | 0.814 |
| transfer_zeroshot_from_pooled_all3 | 0.816 |
| transfer_finetune_from_pooled_others | 0.842 |
| transfer_finetune_from_pooled_all3 | 0.847 |
| gnn_st_tuned | 0.853 |
| transfer_zeroshot_from_boston | 0.861 |
| transfer_finetune_from_boston | 0.864 |
| gnn_st_nodemofeat_tuned | 0.871 |
| gnn_st | 0.872 |
| gnn_st_noadapt | 0.879 |
| gnn_st_noweather_tuned | 0.885 |
| gnn_st_nograph | 0.898 |
| gnn_st_nograph_tuned | 0.912 |
| gnn_st_historyonly_tuned | 0.917 |
| xgboost_tuned | 0.928 |
| xgboost_parity | 0.938 |
| blend_baseline | 0.964 |
| lstm_parity | 0.966 |
| seasonal_naive | 0.975 |
| sarima | 0.991 |
| persistence | 1.000 |
| flusight_baseline | 1.034 |
| climatology | 1.145 |
| colagnn_tuned | 1.146 |
| xgboost | 1.176 |
| lstm_tuned | 1.209 |
| arima | 1.390 |
| lstm_s10 | 1.497 |
| lstm | 1.526 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
