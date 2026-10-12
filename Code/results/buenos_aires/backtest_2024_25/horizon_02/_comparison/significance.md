# Is `gnn_st`'s lead bigger than chance? — horizon 2, `post_covid`

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
| lstm_parity | 49 | 0.02 [-0.29, 0.30] | 0.33 [-0.06, 0.69] | 0.08 [-0.11, 0.26] | 0.010 [-0.000, 0.025] | 1.000 | 1.000 | not distinguishable |
| blend_baseline | 49 | -0.00 [-0.44, 0.28] | 0.69 [-0.86, 1.73] | 0.04 [-0.28, 0.27] | 0.016 [0.008, 0.022] | 1.000 | 1.000 | not distinguishable |
| gnn_st_nograph | 49 | -0.03 [-0.08, 0.03] | -0.02 [-0.12, 0.07] | -0.01 [-0.05, 0.02] | 0.000 [-0.002, 0.003] | 1.000 | 1.000 | not distinguishable |
| persistence | 49 | -0.80 [-1.79, -0.10] | -0.20 [-4.18, 2.66] | -0.35 [-1.05, 0.10] | 0.043 [0.023, 0.059] | 0.402 | 1.000 | reference better |
| arima | 49 | -1.28 [-2.41, -0.19] | 0.02 [-2.21, 1.88] | -0.72 [-1.69, 0.08] | 0.064 [0.041, 0.085] | 0.109 | 0.430 | reference better |
| sarima | 49 | -1.96 [-3.04, -1.07] | -0.42 [-4.37, 2.67] | -1.14 [-2.04, -0.37] | 0.043 [0.014, 0.075] | 0.007 | 0.109 | reference better |
| xgboost_parity | 49 | -5.92 [-7.53, -4.29] | -14.46 [-17.82, -10.54] | -4.26 [-5.31, -3.05] | 0.011 [-0.018, 0.037] | 0.000 | 0.000 | reference better |
| xgboost | 49 | -10.09 [-12.96, -7.35] | -26.64 [-33.65, -19.98] | -7.75 [-9.80, -5.71] | 0.072 [0.017, 0.120] | 0.000 | 0.000 | reference better |
| climatology | 49 | -13.03 [-16.26, -9.63] | -32.03 [-38.61, -25.83] | -10.44 [-12.57, -8.21] | 0.083 [-0.002, 0.147] | 0.000 | 0.000 | reference better |
| lstm | 49 | -13.27 [-18.47, -9.59] | -34.82 [-48.45, -23.03] | -10.83 [-15.90, -7.40] | 0.145 [0.045, 0.259] | 0.000 | 0.000 | reference better |
| seasonal_naive | 49 | -13.60 [-18.79, -9.86] | -30.93 [-44.22, -18.09] | -10.75 [-15.12, -7.68] | 0.207 [0.107, 0.312] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| lstm_parity | 0.953 |
| blend_baseline | 0.957 |
| gnn_st | 0.961 |
| gnn_st_nograph | 0.963 |
| persistence | 1.000 |
| arima | 1.040 |
| sarima | 1.086 |
| xgboost_parity | 1.428 |
| xgboost | 1.809 |
| climatology | 2.104 |
| seasonal_naive | 2.138 |
| lstm | 2.147 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
