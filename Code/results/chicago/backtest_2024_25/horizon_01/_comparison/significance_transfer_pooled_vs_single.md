# Is `transfer_zeroshot_from_pooled_others`'s lead bigger than chance? — horizon 1, `full`

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
| transfer_zeroshot_from_boston | 52 | 0.02 [-0.04, 0.11] | -0.09 [-0.13, -0.04] | -0.02 [-0.04, 0.01] | 0.030 [0.023, 0.046] | 0.467 | 0.038 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.800 |
| transfer_finetune_from_pooled_all3 | 0.800 |
| transfer_finetune_from_pooled_others | 0.801 |
| gnn_st_noadapt | 0.802 |
| gnn_st | 0.803 |
| gnn_st_tuned | 0.803 |
| transfer_zeroshot_from_pooled_all3 | 0.810 |
| gat_tuned | 0.827 |
| colagnn_tuned | 0.827 |
| gat_parity | 0.833 |
| transfer_zeroshot_from_pooled_others | 0.841 |
| lstm | 0.844 |
| lstm_s10 | 0.849 |
| lstm_tuned | 0.849 |
| transfer_zeroshot_from_boston | 0.856 |
| gnn_st_nograph_tuned | 0.858 |
| gnn_st_nograph | 0.864 |
| dualtopo_tuned | 0.869 |
| xgboost_parity | 0.890 |
| xgboost_tuned | 0.896 |
| xgboost | 0.899 |
| sarima | 0.919 |
| arima | 0.922 |
| blend_baseline | 0.948 |
| lstm_parity | 0.968 |
| flusight_baseline | 0.979 |
| persistence | 1.000 |
| climatology | 1.113 |
| seasonal_naive | 1.161 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
