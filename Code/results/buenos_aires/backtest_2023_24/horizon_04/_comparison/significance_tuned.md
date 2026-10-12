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
| lstm_tuned | 52 | 1.27 [0.45, 2.33] | 0.55 [-0.71, 1.92] | 0.28 [-0.36, 0.95] | -0.010 [-0.029, 0.027] | 0.094 | 1.000 | other better |
| blend_baseline | 52 | 1.27 [-0.46, 2.92] | 1.85 [-1.44, 5.48] | 0.31 [-1.18, 1.64] | 0.054 [0.003, 0.091] | 0.650 | 1.000 | not distinguishable |
| gnn_st_nograph_tuned | 52 | -0.12 [-0.54, 0.33] | -0.13 [-0.77, 0.61] | -0.04 [-0.25, 0.19] | 0.007 [-0.003, 0.014] | 1.000 | 1.000 | not distinguishable |
| persistence | 52 | -1.44 [-5.10, 2.07] | -3.80 [-10.46, 3.86] | -1.59 [-5.19, 1.23] | 0.176 [0.033, 0.284] | 1.000 | 1.000 | not distinguishable |
| flusight_baseline | 52 | -1.52 [-5.17, 1.96] | -3.84 [-10.48, 3.81] | -0.92 [-3.87, 1.76] | 0.176 [0.034, 0.285] | 1.000 | 1.000 | not distinguishable |
| colagnn_tuned | 52 | -1.87 [-2.90, -0.67] | -3.20 [-4.90, -1.54] | -1.85 [-2.79, -0.96] | 0.010 [-0.058, 0.091] | 0.016 | 0.004 | reference better |
| sarima | 52 | -5.28 [-8.14, -2.63] | -13.46 [-19.99, -6.94] | -4.43 [-7.18, -2.03] | 0.079 [0.004, 0.153] | 0.005 | 0.020 | reference better |
| lstm_s10 | 52 | -6.43 [-8.62, -4.19] | -10.50 [-15.07, -6.05] | -6.76 [-11.43, -3.16] | 0.344 [0.125, 0.533] | 0.000 | 0.027 | reference better |
| xgboost_tuned | 52 | -6.86 [-8.80, -5.27] | -12.53 [-18.03, -7.78] | -4.98 [-6.64, -3.59] | 0.139 [0.054, 0.208] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS is the
model's mean WIS divided by persistence's on the same cells: below 1 is
better than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS |
| --- | --- |
| blend_baseline | 0.869 |
| lstm_tuned | 0.871 |
| gnn_st_tuned | 0.890 |
| lstm_parity | 0.891 |
| gnn_st_nograph_tuned | 0.893 |
| gnn_st | 0.939 |
| gnn_st_nograph | 0.943 |
| flusight_baseline | 0.953 |
| persistence | 1.000 |
| colagnn_tuned | 1.018 |
| arima | 1.149 |
| sarima | 1.195 |
| xgboost_parity | 1.229 |
| xgboost_tuned | 1.233 |
| climatology | 1.236 |
| seasonal_naive | 1.239 |
| xgboost | 1.259 |
| lstm_s10 | 1.355 |
| lstm | 1.399 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
