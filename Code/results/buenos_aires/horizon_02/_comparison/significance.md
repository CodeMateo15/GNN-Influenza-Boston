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
| persistence | 53 | -0.81 [-1.89, 0.02] | 0.01 [-4.28, 3.31] | -0.08 [-0.66, 0.46] | 0.051 [0.029, 0.070] | 0.176 | 0.823 | not distinguishable |
| arima | 53 | -5.19 [-7.06, -3.59] | -3.84 [-6.26, -1.74] | -2.48 [-3.80, -1.46] | 0.169 [0.141, 0.196] | 0.000 | 0.000 | reference better |
| gat | 53 | -9.30 [-12.72, -6.74] | -21.30 [-28.91, -13.65] | -5.35 [-7.61, -3.55] | 0.086 [0.027, 0.167] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -9.69 [-12.20, -7.18] | -25.81 [-31.69, -19.45] | -7.13 [-9.13, -5.04] | 0.058 [0.015, 0.101] | 0.000 | 0.000 | reference better |
| xgboost_nodemo | 53 | -10.28 [-12.63, -7.78] | -26.46 [-31.99, -20.32] | -7.53 [-9.41, -5.50] | 0.081 [0.042, 0.125] | 0.000 | 0.000 | reference better |
| seasonal_naive | 53 | -13.31 [-18.46, -9.70] | -30.20 [-42.35, -18.27] | -7.89 [-11.51, -5.21] | 0.201 [0.110, 0.293] | 0.000 | 0.000 | reference better |
| dualtopo | 53 | -13.36 [-17.25, -10.40] | -32.67 [-43.85, -22.55] | -10.25 [-13.84, -7.45] | 0.159 [0.076, 0.229] | 0.000 | 0.000 | reference better |
| lstm | 53 | -13.83 [-17.93, -10.21] | -36.68 [-48.79, -25.00] | -9.47 [-12.93, -6.55] | 0.133 [0.031, 0.224] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st | 0.988 |
| gnn_st_nodemo | 0.999 |
| persistence | 1.000 |
| arima | 1.381 |
| gat | 1.834 |
| xgboost | 2.116 |
| xgboost_nodemo | 2.179 |
| seasonal_naive | 2.236 |
| lstm | 2.487 |
| dualtopo | 2.610 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
