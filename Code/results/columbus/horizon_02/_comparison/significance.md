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
| gat | 53 | -0.87 [-2.07, 0.12] | -1.48 [-3.12, -0.08] | -0.45 [-1.12, -0.00] | 0.045 [-0.069, 0.117] | 0.109 | 0.112 | not distinguishable |
| xgboost | 53 | -1.07 [-1.83, -0.38] | -1.88 [-3.10, -0.74] | -0.52 [-1.00, -0.16] | 0.083 [-0.027, 0.162] | 0.017 | 0.043 | reference better |
| lstm | 53 | -1.43 [-2.69, -0.35] | -1.95 [-3.62, -0.34] | -0.62 [-1.19, -0.14] | 0.105 [-0.021, 0.241] | 0.023 | 0.043 | reference better |
| arima | 53 | -1.68 [-2.79, -0.76] | -2.92 [-4.73, -1.20] | -0.97 [-1.86, -0.35] | 0.183 [0.117, 0.274] | 0.003 | 0.037 | reference better |
| persistence | 53 | -1.86 [-2.83, -1.08] | -2.98 [-4.34, -1.61] | -0.91 [-1.43, -0.54] | 0.152 [0.069, 0.253] | 0.000 | 0.000 | reference better |
| seasonal_naive | 53 | -3.28 [-7.14, -0.95] | -7.85 [-15.05, -1.51] | -1.49 [-2.98, -0.57] | 0.188 [0.002, 0.290] | 0.055 | 0.041 | reference better |
| dualtopo | 53 | -3.67 [-6.26, -1.53] | -5.65 [-8.91, -2.44] | -2.73 [-5.18, -1.01] | 0.091 [-0.054, 0.192] | 0.003 | 0.016 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_cascade | 0.725 |
| gnn_st | 0.738 |
| gnn_st_v2 | 0.744 |
| gat | 0.867 |
| xgboost | 0.887 |
| lstm | 0.915 |
| persistence | 1.000 |
| arima | 1.015 |
| seasonal_naive | 1.164 |
| dualtopo | 1.520 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
