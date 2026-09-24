Ranked by **RMSE** within each segment, `scope=pooled`, horizon 2.

## Overall (full year) — 992 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 27.206 | 48.117 | 12.984 | 0.931 | 93.145 | level | none |
| gnn_st | post_covid | 27.220 | 65.171 | 12.171 | 0.934 | 93.448 | blend | train |
| arima | post_covid | 31.057 | 79.095 | 17.358 | 0.907 | 85.282 | level | none |
| gat | post_covid | 48.521 | 120.919 | 21.475 | 0.781 | 91.230 | level | None |
| xgboost | post_covid | 53.030 | 110.795 | 21.857 | 0.705 | 93.347 | climatology | None |
| xgboost_nodemo | post_covid | 53.680 | 135.701 | 22.450 | 0.694 | 93.044 | climatology | None |
| seasonal_naive | post_covid | 57.416 | 118.559 | 25.476 | 0.645 | 94.456 | level | none |
| dualtopo | post_covid | 59.894 | 186.988 | 25.532 | 0.591 | 82.762 | level | train |
| lstm | post_covid | 63.900 | 144.856 | 26.002 | 0.512 | 93.246 | level | train |

## Flu season (Apr–Sep) — 494 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 34.804 | 77.161 | 16.522 | 0.929 | 91.296 | blend | train |
| persistence | post_covid | 35.197 | 48.222 | 17.813 | 0.924 | 91.498 | level | none |
| arima | post_covid | 39.154 | 70.477 | 22.018 | 0.909 | 79.352 | level | none |
| gat | post_covid | 61.530 | 151.111 | 28.662 | 0.767 | 90.283 | level | None |
| xgboost | post_covid | 66.924 | 106.427 | 29.676 | 0.691 | 91.093 | climatology | None |
| xgboost_nodemo | post_covid | 67.276 | 146.471 | 29.922 | 0.685 | 91.093 | climatology | None |
| seasonal_naive | post_covid | 73.421 | 119.415 | 33.900 | 0.615 | 92.105 | level | none |
| dualtopo | post_covid | 74.355 | 213.605 | 31.852 | 0.596 | 83.401 | level | train |
| lstm | post_covid | 82.900 | 170.353 | 35.521 | 0.451 | 91.093 | level | train |

## Off-season (Oct–Mar) — 498 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 15.668 | 48.014 | 8.194 | 0.932 | 94.779 | level | none |
| gnn_st | post_covid | 16.561 | 53.376 | 7.855 | 0.928 | 95.582 | blend | train |
| arima | post_covid | 20.014 | 87.574 | 12.735 | 0.897 | 91.165 | level | none |
| gat | post_covid | 30.563 | 91.216 | 14.346 | 0.735 | 92.169 | level | None |
| xgboost | post_covid | 34.041 | 115.092 | 14.102 | 0.612 | 95.582 | climatology | None |
| seasonal_naive | post_covid | 34.920 | 117.717 | 17.120 | 0.615 | 96.787 | level | none |
| xgboost_nodemo | post_covid | 35.360 | 125.105 | 15.038 | 0.565 | 94.980 | climatology | None |
| lstm | post_covid | 36.282 | 119.771 | 16.561 | 0.541 | 95.382 | level | train |
| dualtopo | post_covid | 40.760 | 160.803 | 19.262 | 0.402 | 82.129 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `persistence (post_covid)`
- **Flu season (Apr–Sep)**: `gnn_st (post_covid)`
- **Off-season (Oct–Mar)**: `persistence (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
