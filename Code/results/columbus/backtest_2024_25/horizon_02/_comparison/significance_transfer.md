# Is `gnn_st_noadapt`'s lead bigger than chance? — horizon 2, `post_covid`

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
| transfer_finetune_from_boston | 52 | 0.09 [-0.07, 0.26] | 0.08 [-0.14, 0.33] | 0.09 [0.00, 0.20] | -0.007 [-0.019, 0.010] | 0.643 | 0.384 | not distinguishable |
| transfer_zeroshot_from_boston | 52 | 0.01 [-0.40, 0.57] | 0.63 [-0.65, 1.79] | 0.11 [-0.29, 0.74] | -0.011 [-0.044, 0.050] | 0.967 | 0.690 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_tuned | 0.853 |
| transfer_zeroshot_from_boston | 0.861 |
| transfer_finetune_from_boston | 0.864 |
| gnn_st | 0.872 |
| gnn_st_noadapt | 0.879 |
| gnn_st_nograph | 0.898 |
| gnn_st_nograph_tuned | 0.912 |
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
