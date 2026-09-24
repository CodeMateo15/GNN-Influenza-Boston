Ranked by **RMSE** within each segment, `scope=pooled`, horizon 4.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 22.901 | 87.296 | 12.339 | 0.681 | 95.694 | climatology | None |
| gnn_st | post_covid | 23.070 | 82.356 | 12.069 | 0.676 | 96.970 | blend | train |
| lstm | post_covid | 26.670 | 91.985 | 13.612 | 0.540 | 92.663 | level | train |
| arima | post_covid | 28.919 | 163.122 | 17.266 | 0.467 | 97.129 | level | none |
| dualtopo | post_covid | 29.199 | 211.716 | 18.487 | 0.405 | 87.081 | level | train |
| arima | exclude_covid | 30.627 | 144.647 | 17.399 | 0.421 | 94.737 | level | none |
| lstm | exclude_covid | 31.559 | 99.254 | 16.712 | 0.460 | 89.314 | level | train |
| gat | post_covid | 31.992 | 124.462 | 17.346 | 0.366 | 88.198 | level | None |
| persistence | exclude_covid | 34.910 | 92.984 | 17.464 | 0.372 | 94.418 | level | none |
| persistence | post_covid | 34.910 | 92.984 | 17.464 | 0.372 | 94.737 | level | none |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 29.995 | 94.840 | 18.238 | 0.622 | 96.591 | climatology | None |
| gnn_st | post_covid | 30.262 | 89.087 | 18.054 | 0.619 | 94.602 | blend | train |
| lstm | post_covid | 32.853 | 65.364 | 17.423 | 0.556 | 87.500 | level | train |
| dualtopo | post_covid | 33.441 | 109.861 | 19.058 | 0.501 | 83.807 | level | train |
| arima | post_covid | 35.925 | 108.408 | 21.252 | 0.434 | 94.886 | level | none |
| arima | exclude_covid | 38.529 | 101.501 | 22.414 | 0.377 | 90.625 | level | none |
| lstm | exclude_covid | 39.794 | 89.307 | 23.098 | 0.412 | 83.239 | level | train |
| gat | post_covid | 41.934 | 117.827 | 25.662 | 0.261 | 78.977 | level | None |
| persistence | exclude_covid | 45.891 | 104.267 | 26.733 | 0.284 | 90.057 | level | none |
| persistence | post_covid | 45.891 | 104.267 | 26.733 | 0.284 | 90.625 | level | none |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.425 | 73.740 | 4.409 | 0.777 | 100.000 | blend | train |
| xgboost | post_covid | 6.645 | 77.639 | 4.788 | 0.758 | 94.545 | climatology | None |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| gat | post_covid | 9.097 | 132.955 | 6.701 | 0.743 | 100.000 | level | None |
| persistence | exclude_covid | 9.111 | 78.541 | 5.600 | 0.674 | 100.000 | level | none |
| persistence | post_covid | 9.111 | 78.541 | 5.600 | 0.674 | 100.000 | level | none |
| arima | exclude_covid | 15.445 | 199.873 | 10.979 | 0.607 | 100.000 | level | none |
| lstm | post_covid | 15.498 | 126.061 | 8.735 | 0.675 | 99.273 | level | train |
| lstm | exclude_covid | 15.614 | 111.987 | 8.538 | 0.692 | 97.091 | level | train |
| arima | post_covid | 15.962 | 233.156 | 12.164 | 0.690 | 100.000 | level | none |
| dualtopo | post_covid | 22.637 | 342.090 | 17.755 | 0.585 | 91.273 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `xgboost (post_covid)`
- **Flu season (Oct–Mar)**: `xgboost (post_covid)`
- **Off-season (Apr–Sep)**: `gnn_st (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
