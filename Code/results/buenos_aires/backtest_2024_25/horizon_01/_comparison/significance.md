# Is `gnn_st`'s lead bigger than chance? — horizon 1, `post_covid`

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
| blend_baseline | 49 | 0.05 [-0.60, 0.54] | 0.61 [-0.85, 1.74] | 0.06 [-0.37, 0.38] | 0.014 [0.003, 0.029] | 1.000 | 1.000 | not distinguishable |
| lstm_parity | 49 | -0.10 [-0.76, 0.42] | 0.46 [-1.10, 1.65] | 0.01 [-0.45, 0.39] | 0.023 [0.010, 0.049] | 1.000 | 1.000 | not distinguishable |
| persistence | 49 | -0.25 [-1.24, 0.46] | 0.10 [-2.76, 2.42] | -0.13 [-0.78, 0.35] | 0.033 [0.021, 0.050] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 49 | -0.52 [-0.85, -0.17] | -1.20 [-1.65, -0.76] | -0.36 [-0.56, -0.15] | -0.001 [-0.012, 0.010] | 0.009 | 0.006 | reference better |
| sarima | 49 | -0.86 [-1.64, -0.28] | 0.78 [-2.05, 3.10] | -0.63 [-1.29, -0.12] | 0.034 [0.018, 0.058] | 0.177 | 0.207 | reference better |
| arima | 49 | -1.13 [-2.10, -0.42] | 0.40 [-1.62, 1.96] | -0.87 [-1.65, -0.34] | 0.055 [0.031, 0.088] | 0.079 | 0.046 | reference better |
| xgboost_parity | 49 | -3.24 [-4.16, -2.32] | -7.07 [-8.79, -4.91] | -2.26 [-2.95, -1.58] | 0.014 [-0.006, 0.029] | 0.000 | 0.000 | reference better |
| gat_parity | 49 | -7.91 [-9.76, -6.68] | -12.97 [-16.87, -9.91] | -5.45 [-6.69, -4.64] | 0.092 [0.033, 0.135] | 0.000 | 0.000 | reference better |
| xgboost | 49 | -10.43 [-13.61, -7.74] | -26.70 [-33.31, -20.80] | -7.93 [-10.28, -5.99] | 0.107 [0.063, 0.152] | 0.000 | 0.000 | reference better |
| lstm | 49 | -13.34 [-17.62, -10.09] | -33.87 [-47.36, -21.41] | -10.34 [-14.41, -7.37] | 0.147 [0.069, 0.221] | 0.000 | 0.000 | reference better |
| climatology | 49 | -14.74 [-18.47, -11.00] | -35.42 [-41.96, -28.89] | -11.83 [-14.49, -9.23] | 0.144 [0.055, 0.212] | 0.000 | 0.000 | reference better |
| seasonal_naive | 49 | -15.31 [-21.39, -11.08] | -34.31 [-48.14, -20.65] | -12.14 [-17.28, -8.57] | 0.268 [0.165, 0.371] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.975 |
| lstm_parity | 0.982 |
| gnn_st | 0.983 |
| persistence | 1.000 |
| gnn_st_nograph | 1.031 |
| sarima | 1.067 |
| arima | 1.099 |
| xgboost_parity | 1.283 |
| gat_parity | 1.708 |
| xgboost | 2.038 |
| lstm | 2.358 |
| climatology | 2.555 |
| seasonal_naive | 2.597 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
