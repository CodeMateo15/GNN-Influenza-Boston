# Is `transfer_zeroshot_from_pooled_others`'s lead bigger than chance? — horizon 1, `post_covid`

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
| transfer_zeroshot_from_boston | 52 | -0.07 [-0.28, 0.16] | 0.09 [-0.36, 0.50] | -0.05 [-0.18, 0.08] | 0.006 [0.001, 0.034] | 0.564 | 0.521 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_zeroshot_from_pooled_others | 0.825 |
| transfer_zeroshot_from_pooled_all3 | 0.829 |
| transfer_zeroshot_from_boston | 0.836 |
| transfer_finetune_from_pooled_others | 0.846 |
| transfer_finetune_from_pooled_all3 | 0.856 |
| gnn_st_tuned | 0.870 |
| gnn_st | 0.877 |
| transfer_finetune_from_boston | 0.879 |
| gnn_st_noadapt | 0.880 |
| gnn_st_nograph | 0.944 |
| lstm_parity | 0.995 |
| xgboost_parity | 0.996 |
| persistence | 1.000 |
| gnn_st_nograph_tuned | 1.008 |
| flusight_baseline | 1.038 |
| blend_baseline | 1.081 |
| lstm_tuned | 1.099 |
| sarima | 1.189 |
| seasonal_naive | 1.232 |
| colagnn_tuned | 1.292 |
| arima | 1.386 |
| climatology | 1.446 |
| xgboost | 1.482 |
| xgboost_tuned | 1.492 |
| gat_tuned | 1.523 |
| gat_parity | 1.567 |
| lstm_s10 | 1.828 |
| dualtopo_tuned | 1.866 |
| lstm | 1.887 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
