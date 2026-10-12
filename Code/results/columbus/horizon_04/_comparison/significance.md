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
| xgboost | 53 | 0.16 [-0.24, 0.65] | 0.27 [-0.35, 0.86] | 0.09 [-0.08, 0.32] | -0.068 [-0.130, -0.001] | 1.000 | 0.543 | not distinguishable |
| dualtopo | 53 | -0.08 [-1.06, 0.73] | 0.01 [-1.06, 1.07] | -0.36 [-1.06, 0.14] | -0.046 [-0.131, 0.038] | 1.000 | 0.543 | not distinguishable |
| arima | 53 | -1.53 [-3.05, -0.37] | -2.51 [-4.52, -0.57] | -0.76 [-1.51, -0.19] | 0.259 [0.087, 0.432] | 0.191 | 0.188 | reference better |
| lstm | 53 | -2.02 [-3.76, -0.50] | -2.57 [-4.57, -0.49] | -0.89 [-1.64, -0.23] | 0.210 [-0.000, 0.433] | 0.129 | 0.126 | reference better |
| seasonal_naive | 53 | -2.52 [-6.78, 0.07] | -6.42 [-14.46, 0.51] | -1.09 [-2.75, 0.02] | 0.097 [-0.055, 0.181] | 0.610 | 0.506 | not distinguishable |
| gat | 53 | -2.84 [-6.08, -0.58] | -5.52 [-9.90, -1.55] | -1.74 [-3.78, -0.34] | 0.173 [-0.131, 0.367] | 0.278 | 0.273 | reference better |
| persistence | 53 | -3.26 [-5.18, -1.85] | -4.61 [-6.75, -2.65] | -1.47 [-2.23, -0.90] | 0.268 [0.100, 0.441] | 0.003 | 0.001 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| xgboost | 0.649 |
| gnn_st | 0.670 |
| dualtopo | 0.750 |
| arima | 0.840 |
| lstm | 0.870 |
| seasonal_naive | 0.916 |
| persistence | 1.000 |
| gat | 1.062 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
