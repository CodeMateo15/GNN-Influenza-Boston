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
| blend_baseline | 53 | -0.07 [-0.17, 0.01] | -0.19 [-0.32, -0.07] | -0.10 [-0.14, -0.05] | 0.103 [0.052, 0.148] | 0.489 | 0.000 | not distinguishable |
| sarima | 53 | -0.08 [-0.17, 0.01] | -0.01 [-0.12, 0.08] | -0.02 [-0.08, 0.03] | 0.013 [-0.028, 0.061] | 0.489 | 0.897 | not distinguishable |
| gnn_st_nograph_tuned | 53 | -0.08 [-0.18, 0.02] | -0.05 [-0.20, 0.08] | -0.02 [-0.09, 0.04] | 0.064 [-0.024, 0.151] | 0.489 | 0.897 | not distinguishable |
| lstm_tuned | 53 | -0.08 [-0.18, 0.00] | -0.18 [-0.31, -0.07] | -0.09 [-0.13, -0.05] | 0.098 [0.043, 0.144] | 0.489 | 0.000 | not distinguishable |
| xgboost_tuned | 53 | -0.09 [-0.18, 0.01] | -0.03 [-0.15, 0.08] | -0.03 [-0.08, 0.03] | 0.046 [-0.014, 0.107] | 0.489 | 0.897 | not distinguishable |
| colagnn_tuned | 53 | -0.10 [-0.18, -0.04] | -0.03 [-0.12, 0.04] | -0.02 [-0.05, 0.01] | 0.006 [-0.022, 0.042] | 0.059 | 0.795 | reference better |
| lstm_s10 | 53 | -0.21 [-0.39, -0.03] | -0.20 [-0.43, 0.02] | -0.13 [-0.20, -0.03] | 0.109 [-0.027, 0.224] | 0.234 | 0.051 | reference better |
| flusight_baseline | 53 | -0.41 [-0.52, -0.29] | -0.85 [-0.98, -0.69] | -0.31 [-0.44, -0.20] | 0.199 [0.085, 0.306] | 0.000 | 0.000 | reference better |
| persistence | 53 | -0.41 [-0.52, -0.29] | -0.85 [-0.98, -0.69] | -0.32 [-0.42, -0.23] | 0.199 [0.085, 0.306] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.770 |
| transfer_zeroshot_from_boston | 0.783 |
| gnn_st_tuned | 0.783 |
| gnn_st_noadapt | 0.785 |
| gnn_st | 0.787 |
| colagnn_tuned | 0.796 |
| gnn_st_nograph_tuned | 0.798 |
| sarima | 0.799 |
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
