# Is `gnn_st`'s lead bigger than chance? — horizon 4, `post_covid`

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
| xgboost | 49 | -0.27 [-2.04, 1.17] | 0.17 [-2.93, 2.15] | -0.12 [-1.03, 0.99] | -0.026 [-0.088, 0.070] | 0.765 | 0.786 | not distinguishable |
| lstm | 49 | -1.54 [-4.37, 1.81] | -3.60 [-6.94, 2.54] | -1.40 [-3.89, 0.60] | 0.142 [-0.012, 0.352] | 0.739 | 0.522 | not distinguishable |
| arima | 49 | -5.20 [-7.18, -2.86] | -5.85 [-7.82, -3.84] | -2.18 [-2.95, -1.34] | 0.328 [0.129, 0.452] | 0.000 | 0.000 | reference better |
| gat | 49 | -5.28 [-10.59, -1.48] | -8.92 [-14.92, -3.22] | -3.78 [-8.06, -0.88] | 0.403 [-0.002, 0.616] | 0.196 | 0.322 | reference better |
| persistence | 49 | -5.39 [-11.83, -0.50] | -11.84 [-20.50, -1.73] | -2.67 [-5.48, -0.35] | 0.358 [0.072, 0.501] | 0.384 | 0.322 | reference better |
| dualtopo | 49 | -6.42 [-11.09, -0.97] | -6.13 [-11.33, -0.75] | -3.90 [-7.27, -1.03] | 0.069 [-0.185, 0.212] | 0.086 | 0.096 | reference better |
| seasonal_naive | 49 | -7.74 [-19.30, -0.85] | -16.77 [-35.73, -1.32] | -2.92 [-7.35, -0.31] | 0.286 [0.057, 0.442] | 0.479 | 0.469 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st | 0.676 |
| gnn_st_noglobals | 0.676 |
| xgboost | 0.691 |
| gnn_st_lagsonly | 0.693 |
| lstm | 0.846 |
| arima | 0.941 |
| persistence | 1.000 |
| seasonal_naive | 1.030 |
| gat | 1.135 |
| dualtopo | 1.149 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
