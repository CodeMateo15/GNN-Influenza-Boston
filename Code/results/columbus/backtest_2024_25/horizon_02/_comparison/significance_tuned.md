# Is `gnn_st_tuned`'s lead bigger than chance? — horizon 2, `post_covid`

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
| gnn_st_nograph_tuned | 52 | -0.32 [-1.19, 0.38] | -1.21 [-2.39, 0.34] | -0.35 [-1.14, 0.22] | -0.003 [-0.021, 0.019] | 0.660 | 0.628 | not distinguishable |
| xgboost_tuned | 52 | -0.35 [-1.19, 0.33] | -1.26 [-2.41, 0.22] | -0.44 [-1.29, 0.12] | -0.005 [-0.031, 0.025] | 0.660 | 0.628 | not distinguishable |
| sarima | 52 | -0.68 [-1.98, 0.20] | -1.85 [-3.58, 0.17] | -0.81 [-2.10, 0.02] | 0.058 [-0.019, 0.103] | 0.611 | 0.628 | not distinguishable |
| blend_baseline | 52 | -1.05 [-2.56, 0.02] | -2.57 [-4.61, -0.19] | -0.66 [-1.93, 0.14] | 0.002 [-0.042, 0.045] | 0.599 | 0.628 | not distinguishable |
| colagnn_tuned | 52 | -1.23 [-3.00, -0.07] | -3.09 [-5.53, -0.26] | -1.73 [-3.91, -0.30] | 0.039 [-0.031, 0.102] | 0.599 | 0.226 | reference better |
| lstm_tuned | 52 | -1.28 [-3.15, -0.06] | -3.16 [-5.66, -0.18] | -2.10 [-4.72, -0.33] | 0.029 [-0.025, 0.089] | 0.599 | 0.214 | reference better |
| flusight_baseline | 52 | -1.48 [-3.36, 0.10] | -1.38 [-5.44, 1.99] | -1.07 [-2.64, 0.23] | 0.053 [0.025, 0.161] | 0.599 | 0.628 | not distinguishable |
| persistence | 52 | -1.48 [-3.36, 0.10] | -1.38 [-5.44, 1.99] | -0.87 [-1.90, 0.27] | 0.053 [0.025, 0.161] | 0.599 | 0.628 | not distinguishable |
| lstm_s10 | 52 | -3.39 [-6.52, -0.84] | -6.51 [-10.57, -1.55] | -3.80 [-7.61, -0.94] | 0.039 [-0.065, 0.152] | 0.055 | 0.069 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| gnn_st_tuned | 0.853 |
| gnn_st | 0.872 |
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
