# Is `gnn_st`'s lead bigger than chance? — horizon 1, `post_covid`

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
| lstm | 53 | -1.22 [-1.90, -0.58] | -1.49 [-2.35, -0.76] | -0.46 [-0.71, -0.24] | 0.051 [0.010, 0.093] | 0.000 | 0.000 | reference better |
| persistence | 53 | -1.28 [-1.75, -0.88] | -1.97 [-2.74, -1.19] | -0.64 [-0.92, -0.43] | 0.084 [0.048, 0.154] | 0.000 | 0.000 | reference better |
| arima | 53 | -1.43 [-2.15, -0.80] | -2.25 [-3.44, -1.04] | -0.79 [-1.36, -0.35] | 0.122 [0.092, 0.183] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -1.52 [-2.31, -0.78] | -2.30 [-3.37, -1.23] | -0.66 [-1.01, -0.36] | 0.085 [0.043, 0.146] | 0.000 | 0.000 | reference better |
| gat | 53 | -1.87 [-3.31, -0.56] | -2.82 [-4.72, -0.80] | -1.03 [-2.01, -0.25] | 0.146 [0.017, 0.239] | 0.000 | 0.001 | reference better |
| seasonal_naive | 53 | -4.19 [-8.44, -1.62] | -9.14 [-16.75, -2.39] | -1.87 [-3.50, -0.88] | 0.260 [0.105, 0.369] | 0.001 | 0.000 | reference better |
| dualtopo | 53 | -4.53 [-7.72, -2.09] | -7.14 [-11.04, -3.34] | -3.41 [-6.39, -1.38] | 0.165 [0.050, 0.267] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st | 0.775 |
| gnn_st_v2 | 0.776 |
| lstm | 0.939 |
| persistence | 1.000 |
| xgboost | 1.008 |
| arima | 1.053 |
| gat | 1.138 |
| seasonal_naive | 1.437 |
| dualtopo | 1.980 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
