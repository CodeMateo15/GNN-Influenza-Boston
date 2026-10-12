# Is `gnn_st_noadapt`'s lead bigger than chance? — horizon 2, `full`

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
| transfer_finetune_from_boston | 52 | 0.00 [-0.02, 0.03] | 0.02 [-0.00, 0.05] | 0.00 [-0.01, 0.02] | -0.005 [-0.012, 0.000] | 0.732 | 0.451 | not distinguishable |
| transfer_zeroshot_from_boston | 52 | -0.17 [-0.36, -0.04] | -0.21 [-0.36, -0.09] | -0.11 [-0.21, -0.04] | 0.049 [0.027, 0.082] | 0.032 | 0.004 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.788 |
| gnn_st_noadapt | 0.792 |
| gnn_st | 0.801 |
| transfer_zeroshot_from_boston | 0.872 |
| gnn_st_nograph | 0.873 |
| xgboost | 0.891 |
| xgboost_parity | 0.891 |
| sarima | 0.895 |
| blend_baseline | 0.933 |
| lstm_s10 | 0.965 |
| arima | 0.968 |
| flusight_baseline | 0.982 |
| persistence | 1.000 |
| lstm | 1.010 |
| lstm_parity | 1.028 |
| climatology | 1.064 |
| seasonal_naive | 1.110 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
