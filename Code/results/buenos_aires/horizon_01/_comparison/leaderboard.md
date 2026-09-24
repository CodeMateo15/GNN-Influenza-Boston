Ranked by **RMSE** within each segment, `scope=pooled`, horizon 1.

## Overall (full year) — 992 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 22.811 | 61.837 | 10.235 | 0.953 | 96.069 | blend | train |
| persistence | post_covid | 23.505 | 43.133 | 10.693 | 0.948 | 94.657 | level | none |
| arima | post_covid | 25.767 | 61.559 | 13.797 | 0.937 | 90.726 | level | none |
| gat | post_covid | 43.937 | 104.819 | 20.145 | 0.827 | 86.391 | level | None |
| dualtopo | post_covid | 44.914 | 158.716 | 20.761 | 0.805 | 82.258 | level | train |
| xgboost | post_covid | 48.834 | 87.307 | 20.352 | 0.764 | 95.363 | climatology | None |
| xgboost_nodemo | post_covid | 50.789 | 108.818 | 21.344 | 0.733 | 93.548 | climatology | None |
| seasonal_naive | post_covid | 57.413 | 118.556 | 25.473 | 0.645 | 94.456 | level | none |
| lstm | post_covid | 61.444 | 140.179 | 24.252 | 0.561 | 93.347 | level | train |

## Flu season (Apr–Sep) — 494 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 29.884 | 72.655 | 13.892 | 0.946 | 94.332 | blend | train |
| persistence | post_covid | 31.218 | 42.678 | 14.824 | 0.940 | 93.320 | level | none |
| arima | post_covid | 32.744 | 55.398 | 17.690 | 0.936 | 87.247 | level | none |
| dualtopo | post_covid | 53.600 | 163.267 | 24.869 | 0.826 | 81.579 | level | train |
| gat | post_covid | 57.113 | 112.317 | 26.585 | 0.809 | 82.996 | level | None |
| xgboost | post_covid | 62.226 | 88.432 | 28.125 | 0.745 | 94.332 | climatology | None |
| xgboost_nodemo | post_covid | 63.856 | 113.536 | 28.651 | 0.723 | 92.308 | climatology | None |
| seasonal_naive | post_covid | 73.421 | 119.415 | 33.900 | 0.615 | 92.105 | level | none |
| lstm | post_covid | 79.817 | 158.371 | 33.241 | 0.503 | 91.700 | level | train |

## Off-season (Oct–Mar) — 498 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 11.568 | 43.581 | 6.594 | 0.963 | 95.984 | level | none |
| gnn_st | post_covid | 12.274 | 51.194 | 6.608 | 0.961 | 97.791 | blend | train |
| arima | post_covid | 16.091 | 67.621 | 9.937 | 0.934 | 94.177 | level | none |
| gat | post_covid | 24.691 | 97.441 | 13.757 | 0.827 | 89.759 | level | None |
| xgboost | post_covid | 30.156 | 86.199 | 12.642 | 0.729 | 96.386 | climatology | None |
| xgboost_nodemo | post_covid | 33.067 | 104.176 | 14.095 | 0.640 | 94.779 | climatology | None |
| dualtopo | post_covid | 34.184 | 154.239 | 16.685 | 0.598 | 82.932 | level | train |
| lstm | post_covid | 34.653 | 122.283 | 15.336 | 0.586 | 94.980 | level | train |
| seasonal_naive | post_covid | 34.910 | 117.710 | 17.114 | 0.615 | 96.787 | level | none |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_st (post_covid)`
- **Flu season (Apr–Sep)**: `gnn_st (post_covid)`
- **Off-season (Oct–Mar)**: `persistence (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
