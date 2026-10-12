# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 1, `post_covid`

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
| lstm_tuned | 52 | -0.92 [-2.52, 0.01] | -2.46 [-4.94, 0.11] | -1.07 [-2.81, -0.08] | 0.027 [-0.020, 0.050] | 0.052 | 0.074 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -1.01 [-2.26, -0.18] | -2.24 [-4.17, -0.26] | -0.64 [-1.58, -0.06] | 0.024 [0.004, 0.046] | 0.022 | 0.074 | reference better |
| flusight_baseline | 52 | -1.26 [-2.11, -0.32] | -0.81 [-2.89, 1.28] | -0.78 [-1.47, -0.07] | 0.048 [0.026, 0.150] | 0.011 | 0.053 | reference better |
| persistence | 52 | -1.26 [-2.11, -0.32] | -0.81 [-2.89, 1.28] | -0.60 [-1.13, 0.16] | 0.048 [0.026, 0.150] | 0.011 | 0.074 | reference better |
| blend_baseline | 52 | -1.63 [-3.62, -0.34] | -3.56 [-6.46, -0.45] | -0.98 [-2.52, -0.04] | 0.034 [0.004, 0.061] | 0.015 | 0.074 | reference better |
| sarima | 52 | -1.66 [-3.66, -0.36] | -4.17 [-7.52, -0.46] | -1.49 [-3.34, -0.30] | 0.111 [0.002, 0.156] | 0.015 | 0.024 | reference better |
| colagnn_tuned | 52 | -1.97 [-4.87, -0.16] | -5.23 [-9.61, -0.40] | -1.96 [-4.87, -0.23] | 0.064 [-0.014, 0.108] | 0.025 | 0.053 | reference better |
| xgboost_tuned | 52 | -3.63 [-8.09, -0.64] | -8.77 [-15.38, -0.95] | -2.90 [-7.04, -0.26] | 0.235 [-0.013, 0.384] | 0.015 | 0.052 | reference better |
| dualtopo_tuned | 52 | -3.82 [-8.19, -1.00] | -8.60 [-14.88, -1.65] | -4.65 [-9.49, -1.58] | 0.109 [-0.026, 0.169] | 0.010 | 0.003 | reference better |
| gat_tuned | 52 | -3.96 [-6.57, -2.07] | -6.54 [-10.32, -2.91] | -3.04 [-5.42, -1.42] | 0.059 [-0.015, 0.113] | 0.000 | 0.000 | reference better |
| lstm_s10 | 52 | -4.33 [-8.69, -1.19] | -8.99 [-15.06, -1.92] | -4.47 [-9.41, -1.12] | 0.078 [-0.013, 0.156] | 0.003 | 0.005 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_tuned | 0.870 |
| gnn_st | 0.877 |
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
