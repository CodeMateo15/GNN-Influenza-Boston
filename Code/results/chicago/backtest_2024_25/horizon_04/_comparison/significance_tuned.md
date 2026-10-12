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
| gnn_st_nograph_tuned | 52 | -0.08 [-0.19, 0.02] | -0.09 [-0.24, 0.04] | -0.06 [-0.13, 0.01] | 0.067 [0.013, 0.121] | 0.467 | 0.287 | not distinguishable |
| sarima | 52 | -0.12 [-0.28, -0.00] | -0.15 [-0.36, 0.02] | -0.09 [-0.22, -0.00] | 0.063 [-0.011, 0.142] | 0.467 | 0.287 | reference better |
| blend_baseline | 52 | -0.16 [-0.36, -0.01] | -0.32 [-0.52, -0.13] | -0.11 [-0.16, -0.06] | 0.069 [0.046, 0.095] | 0.467 | 0.002 | reference better |
| flusight_baseline | 52 | -0.17 [-0.40, 0.16] | -0.72 [-0.93, -0.47] | -0.25 [-0.40, -0.11] | 0.140 [0.077, 0.213] | 0.568 | 0.013 | not distinguishable |
| persistence | 52 | -0.17 [-0.40, 0.16] | -0.72 [-0.93, -0.47] | -0.26 [-0.37, -0.14] | 0.140 [0.077, 0.213] | 0.568 | 0.001 | not distinguishable |
| xgboost_tuned | 52 | -0.17 [-0.27, -0.08] | -0.20 [-0.35, -0.06] | -0.11 [-0.19, -0.05] | 0.112 [0.046, 0.175] | 0.020 | 0.019 | reference better |
| colagnn_tuned | 52 | -0.28 [-0.36, -0.20] | -0.21 [-0.33, -0.10] | -0.14 [-0.18, -0.10] | 0.023 [-0.021, 0.082] | 0.000 | 0.000 | reference better |
| lstm_tuned | 52 | -0.44 [-0.83, -0.12] | -0.69 [-1.12, -0.27] | -0.28 [-0.56, -0.07] | 0.085 [-0.020, 0.174] | 0.187 | 0.145 | reference better |
| lstm_s10 | 52 | -0.49 [-0.93, -0.14] | -0.77 [-1.26, -0.30] | -0.34 [-0.68, -0.09] | 0.153 [0.044, 0.213] | 0.187 | 0.145 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| transfer_finetune_from_boston | 0.811 |
| gnn_st_noadapt | 0.823 |
| gnn_st_tuned | 0.828 |
| gnn_st | 0.838 |
| transfer_zeroshot_from_boston | 0.846 |
| gnn_st_nograph_tuned | 0.865 |
| gnn_st_nograph | 0.885 |
| sarima | 0.887 |
| blend_baseline | 0.898 |
| xgboost_tuned | 0.902 |
| xgboost_parity | 0.907 |
| colagnn_tuned | 0.918 |
| xgboost | 0.919 |
| arima | 0.941 |
| flusight_baseline | 0.994 |
| climatology | 0.994 |
| persistence | 1.000 |
| lstm_parity | 1.014 |
| lstm_tuned | 1.016 |
| seasonal_naive | 1.035 |
| lstm | 1.052 |
| lstm_s10 | 1.054 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
