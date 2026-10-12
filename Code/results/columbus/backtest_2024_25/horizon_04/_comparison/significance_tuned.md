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
| xgboost_tuned | 52 | -0.08 [-0.49, 0.32] | -0.53 [-0.99, 0.23] | -0.28 [-0.72, 0.09] | -0.029 [-0.070, 0.003] | 1.000 | 0.890 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.09 [-0.46, 0.29] | -0.41 [-0.80, 0.31] | -0.08 [-0.39, 0.21] | -0.022 [-0.053, 0.004] | 1.000 | 0.935 | not distinguishable |
| lstm_tuned | 52 | -0.16 [-0.70, 0.19] | -0.04 [-0.92, 0.33] | -0.26 [-0.52, -0.10] | 0.049 [0.019, 0.078] | 1.000 | 0.250 | not distinguishable |
| sarima | 52 | -0.23 [-0.58, 0.10] | -0.22 [-0.60, 0.23] | -0.19 [-0.44, 0.07] | 0.083 [0.025, 0.149] | 1.000 | 0.883 | not distinguishable |
| colagnn_tuned | 52 | -0.41 [-1.04, 0.00] | -0.42 [-1.21, -0.04] | -0.80 [-1.44, -0.35] | -0.028 [-0.103, 0.062] | 1.000 | 0.096 | not distinguishable |
| blend_baseline | 52 | -0.48 [-0.95, -0.01] | -0.80 [-1.23, -0.15] | -0.13 [-0.41, 0.13] | -0.023 [-0.050, 0.000] | 0.512 | 0.935 | reference better |
| lstm_s10 | 52 | -2.79 [-4.82, -1.02] | -4.04 [-5.80, -1.97] | -3.05 [-5.58, -1.10] | 0.033 [-0.148, 0.257] | 0.090 | 0.157 | reference better |
| flusight_baseline | 52 | -2.80 [-7.30, 0.57] | -3.38 [-12.51, 2.80] | -1.88 [-5.62, 1.05] | 0.151 [0.023, 0.300] | 1.000 | 0.935 | not distinguishable |
| persistence | 52 | -2.80 [-7.30, 0.57] | -3.38 [-12.51, 2.80] | -2.14 [-4.48, -0.18] | 0.151 [0.023, 0.300] | 1.000 | 0.398 | not distinguishable |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| seasonal_naive | 0.680 |
| gnn_st_tuned | 0.747 |
| gnn_st_nograph_tuned | 0.756 |
| gnn_st_nograph | 0.760 |
| blend_baseline | 0.763 |
| gnn_st | 0.766 |
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
