# Is `gnn_st`'s lead bigger than chance? — horizon 2, `post_covid`

Each row asks: on the weeks of this test season, is the reference model's error
really lower than this model's, or could the gap come from which weeks the season
happened to contain? Differences are **reference minus other**, so for MAE, RMSE
and WIS a negative number means the reference is better; for Corr, positive does.
The bracket is a 95% confidence interval from resampling whole weeks in blocks of
4 (all neighborhoods kept together inside a week). A gap whose interval crosses 0
is not distinguishable from chance on this season.

`p (MAE)` and `p (WIS)` are Diebold-Mariano tests on the weekly loss, Holm-adjusted
across the rows of this table. WIS-95 scores the point forecast and its 95% band
together (lower is better, units are rate per 100,000); it is the one-band version
of FluSight's weighted interval score.

| other model | weeks | ΔMAE [95% CI] | ΔRMSE [95% CI] | ΔWIS-95 [95% CI] | ΔCorr [95% CI] | p (MAE) | p (WIS) | verdict on MAE |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm | 49 | -2.09 [-4.31, -0.52] | -4.16 [-7.45, -0.60] | -1.34 [-3.27, -0.18] | 0.117 [0.009, 0.203] | 0.092 | 0.085 | reference better |
| xgboost | 49 | -2.22 [-4.12, -0.64] | -3.10 [-5.78, 0.06] | -0.93 [-1.54, -0.35] | 0.127 [0.026, 0.215] | 0.092 | 0.069 | reference better |
| persistence | 49 | -3.22 [-6.84, -0.59] | -6.64 [-10.64, -1.32] | -1.65 [-3.40, -0.33] | 0.184 [0.051, 0.312] | 0.092 | 0.069 | reference better |
| arima | 49 | -3.27 [-5.09, -1.87] | -4.36 [-6.43, -2.48] | -1.50 [-2.33, -0.91] | 0.176 [0.067, 0.321] | 0.000 | 0.001 | reference better |
| gat | 49 | -6.99 [-11.15, -3.54] | -10.34 [-15.79, -4.46] | -4.11 [-8.12, -1.40] | 0.411 [0.091, 0.620] | 0.002 | 0.069 | reference better |
| dualtopo | 49 | -9.28 [-14.31, -4.36] | -11.91 [-17.61, -5.63] | -5.19 [-9.78, -2.10] | 1.135 [0.848, 1.449] | 0.000 | 0.023 | reference better |
| seasonal_naive | 49 | -10.96 [-23.88, -2.55] | -22.64 [-41.86, -5.59] | -4.35 [-9.24, -1.25] | 0.505 [0.130, 0.675] | 0.092 | 0.069 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st_lagsonly | 0.709 |
| gnn_st_noglobals | 0.715 |
| gnn_st | 0.715 |
| gnn_cascade | 0.717 |
| xgboost | 0.876 |
| lstm | 0.947 |
| arima | 0.974 |
| persistence | 1.000 |
| gat | 1.425 |
| seasonal_naive | 1.467 |
| dualtopo | 1.612 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
