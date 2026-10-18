# Is `gnn_st_noadapt`'s lead bigger than chance? — horizon 4, `post_covid`

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
| transfer_zeroshot_from_pooled_others | 52 | 0.56 [-0.23, 1.58] | 1.43 [0.04, 2.40] | 0.53 [-0.12, 1.40] | -0.074 [-0.154, -0.010] | 0.988 | 0.368 | not distinguishable |
| transfer_zeroshot_from_pooled_all3 | 52 | 0.38 [-0.17, 1.07] | 0.78 [0.06, 1.40] | 0.48 [-0.00, 1.10] | -0.058 [-0.120, -0.008] | 0.988 | 0.368 | not distinguishable |
| transfer_finetune_from_pooled_all3 | 52 | 0.30 [-0.30, 1.03] | 0.81 [-0.14, 1.61] | 0.54 [-0.03, 1.33] | -0.072 [-0.144, -0.006] | 0.988 | 0.368 | not distinguishable |
| transfer_finetune_from_pooled_others | 52 | 0.25 [-0.27, 0.95] | 0.39 [-0.09, 1.11] | 0.42 [0.05, 0.96] | -0.068 [-0.134, -0.015] | 0.988 | 0.368 | not distinguishable |

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
| gnn_st_tuned | 0.747 |
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
