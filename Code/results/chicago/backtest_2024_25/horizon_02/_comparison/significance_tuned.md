# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 2, `full`

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
| colagnn_tuned | 52 | -0.11 [-0.16, -0.06] | 0.02 [-0.02, 0.06] | -0.03 [-0.05, -0.01] | -0.023 [-0.041, -0.014] | 0.000 | 0.024 | reference better |
| lstm_tuned | 52 | -0.15 [-0.28, -0.03] | -0.09 [-0.23, 0.02] | -0.06 [-0.13, -0.00] | -0.019 [-0.055, 0.001] | 0.024 | 0.030 | reference better |
| gnn_st_nograph_tuned | 52 | -0.15 [-0.31, -0.03] | -0.17 [-0.33, -0.05] | -0.08 [-0.15, -0.03] | 0.071 [0.038, 0.109] | 0.024 | 0.014 | reference better |
| flusight_baseline | 52 | -0.24 [-0.36, -0.11] | -0.76 [-0.89, -0.64] | -0.26 [-0.35, -0.17] | 0.132 [0.102, 0.178] | 0.000 | 0.000 | reference better |
| persistence | 52 | -0.24 [-0.36, -0.11] | -0.76 [-0.89, -0.64] | -0.28 [-0.35, -0.21] | 0.132 [0.102, 0.178] | 0.000 | 0.000 | reference better |
| sarima | 52 | -0.25 [-0.48, -0.09] | -0.23 [-0.46, -0.06] | -0.13 [-0.27, -0.04] | 0.074 [0.020, 0.115] | 0.021 | 0.024 | reference better |
| xgboost_tuned | 52 | -0.25 [-0.50, -0.07] | -0.25 [-0.51, -0.03] | -0.14 [-0.27, -0.05] | 0.092 [0.033, 0.151] | 0.024 | 0.024 | reference better |
| blend_baseline | 52 | -0.34 [-0.71, -0.05] | -0.45 [-0.77, -0.17] | -0.19 [-0.31, -0.09] | 0.091 [0.062, 0.127] | 0.024 | 0.001 | reference better |
| lstm_s10 | 52 | -0.37 [-0.73, -0.08] | -0.40 [-0.74, -0.09] | -0.23 [-0.47, -0.05] | 0.012 [-0.033, 0.052] | 0.021 | 0.024 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.788 |
| gnn_st_noadapt | 0.792 |
| gnn_st_tuned | 0.800 |
| gnn_st | 0.801 |
| colagnn_tuned | 0.820 |
| lstm_tuned | 0.843 |
| gnn_st_nograph_tuned | 0.860 |
| transfer_zeroshot_from_boston | 0.872 |
| gnn_st_nograph | 0.873 |
| xgboost | 0.891 |
| xgboost_parity | 0.891 |
| sarima | 0.895 |
| xgboost_tuned | 0.896 |
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
