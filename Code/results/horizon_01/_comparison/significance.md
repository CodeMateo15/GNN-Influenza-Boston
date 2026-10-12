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
| lstm | 49 | -1.11 [-2.56, -0.13] | -2.89 [-5.32, -0.07] | -0.72 [-1.87, -0.04] | 0.025 [-0.032, 0.069] | 0.016 | 0.043 | reference better |
| xgboost | 49 | -2.15 [-3.88, -0.80] | -3.85 [-6.80, -0.90] | -1.06 [-1.64, -0.57] | 0.071 [0.029, 0.175] | 0.002 | 0.000 | reference better |
| persistence | 49 | -2.20 [-4.11, -0.77] | -4.04 [-6.11, -1.57] | -1.02 [-1.88, -0.38] | 0.093 [0.054, 0.226] | 0.001 | 0.001 | reference better |
| arima | 49 | -2.36 [-3.90, -1.31] | -3.74 [-5.59, -2.02] | -1.11 [-1.88, -0.61] | 0.104 [0.054, 0.260] | 0.000 | 0.000 | reference better |
| gat | 49 | -6.48 [-10.38, -3.28] | -10.68 [-16.53, -4.59] | -3.62 [-7.17, -1.28] | 0.248 [0.050, 0.444] | 0.000 | 0.002 | reference better |
| dualtopo | 49 | -11.47 [-17.46, -6.62] | -17.14 [-25.64, -9.19] | -6.35 [-12.10, -2.84] | 0.466 [-0.057, 0.615] | 0.000 | 0.000 | reference better |
| seasonal_naive | 49 | -13.08 [-27.13, -3.70] | -28.07 [-46.78, -8.36] | -5.47 [-10.77, -1.89] | 0.596 [0.157, 0.780] | 0.002 | 0.001 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st_noglobals | 0.746 |
| gnn_st | 0.747 |
| gnn_st_lagsonly | 0.767 |
| lstm | 0.925 |
| persistence | 1.000 |
| xgboost | 1.010 |
| arima | 1.022 |
| gat | 1.643 |
| seasonal_naive | 2.101 |
| dualtopo | 2.321 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
