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
| persistence | 53 | -0.46 [-1.30, 0.25] | -0.69 [-3.07, 1.46] | -0.15 [-0.52, 0.17] | 0.034 [0.022, 0.050] | 0.304 | 0.525 | not distinguishable |
| arima | 53 | -3.56 [-4.78, -2.44] | -2.96 [-4.45, -1.83] | -1.67 [-2.46, -1.07] | 0.149 [0.131, 0.181] | 0.000 | 0.000 | reference better |
| gat | 53 | -9.91 [-13.57, -7.37] | -21.13 [-30.74, -12.72] | -5.87 [-9.11, -3.87] | 0.141 [0.087, 0.200] | 0.000 | 0.000 | reference better |
| xgboost | 53 | -10.12 [-13.18, -7.36] | -26.02 [-31.96, -19.71] | -340244.68 [-386158.65, -298817.11] | 0.116 [0.066, 0.160] | 0.000 | 0.000 | reference better |
| dualtopo | 53 | -10.53 [-12.81, -8.39] | -22.10 [-27.92, -15.71] | -7.38 [-9.62, -5.47] | 0.100 [0.051, 0.163] | 0.000 | 0.000 | reference better |
| xgboost_nodemo | 53 | -11.11 [-13.98, -8.25] | -27.98 [-33.55, -21.80] | -7.82 [-9.79, -5.72] | 0.103 [0.061, 0.146] | 0.000 | 0.000 | reference better |
| lstm | 53 | -14.02 [-18.27, -10.35] | -38.63 [-51.24, -26.46] | -9.88 [-13.58, -6.91] | 0.124 [0.053, 0.177] | 0.000 | 0.000 | reference better |
| seasonal_naive | 53 | -15.24 [-20.94, -11.16] | -34.60 [-47.86, -21.54] | -9.08 [-13.16, -5.96] | 0.262 [0.165, 0.354] | 0.000 | 0.000 | reference better |

## Skill against persistence

Does the model beat "next week looks like this week"? Relative WIS-95 is the
model's mean WIS-95 divided by persistence's on the same cells: below 1 is better
than persistence, and 0.8 means 20% less forecast error.

| model | relative WIS-95 |
| --- | --- |
| gnn_st | 0.971 |
| gnn_st_nodemo | 0.979 |
| persistence | 1.000 |
| arima | 1.293 |
| gat | 2.100 |
| dualtopo | 2.391 |
| xgboost_nodemo | 2.475 |
| seasonal_naive | 2.719 |
| lstm | 2.872 |
| xgboost | 65462.643 |

One season is one season: an interval that excludes 0 here says the gap held across
this season's weeks, not that it will hold next season. The backtest folds are what
test that.
