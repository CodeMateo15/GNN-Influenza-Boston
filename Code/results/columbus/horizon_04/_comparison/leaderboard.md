Ranked by **RMSE** within each segment, `scope=pooled`, horizon 4.

## Overall (full year) — 901 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 9.677 | 1675795.756 | 6.413 | 0.887 | 95.117 | climatology | None |
| dualtopo | post_covid | 9.939 | 48.133 | 6.653 | 0.870 | 79.800 | level | train |
| gnn_st | post_covid | 9.948 | 955790.741 | 6.576 | 0.868 | 93.452 | blend | train |
| arima | post_covid | 12.462 | 60.238 | 8.108 | 0.769 | 95.782 | level | none |
| lstm | post_covid | 12.516 | 64.164 | 8.593 | 0.769 | 95.560 | level | train |
| persistence | post_covid | 14.560 | 67.260 | 9.836 | 0.718 | 94.562 | level | none |
| gat | post_covid | 15.464 | 57.398 | 9.415 | 0.735 | 85.017 | level | None |
| seasonal_naive | post_covid | 16.366 | 60.842 | 9.093 | 0.765 | 97.891 | level | none |

## Flu season (Oct–Mar) — 442 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 11.808 | 38.377 | 8.005 | 0.872 | 94.118 | climatology | None |
| dualtopo | post_covid | 12.163 | 32.998 | 8.169 | 0.879 | 75.566 | level | train |
| gnn_st | post_covid | 12.312 | 37.957 | 8.341 | 0.850 | 92.534 | blend | train |
| lstm | post_covid | 14.574 | 42.984 | 9.767 | 0.775 | 92.534 | level | train |
| arima | post_covid | 15.805 | 41.978 | 10.357 | 0.753 | 91.403 | level | none |
| persistence | post_covid | 18.339 | 59.487 | 12.937 | 0.671 | 93.665 | level | none |
| gat | post_covid | 21.018 | 59.226 | 14.283 | 0.670 | 74.208 | level | None |
| seasonal_naive | post_covid | 22.319 | 62.620 | 13.384 | 0.712 | 98.190 | level | none |

## Off-season (Apr–Sep) — 459 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 6.635 | 55.606 | 4.727 | 0.819 | 95.425 | level | None |
| seasonal_naive | post_covid | 6.789 | 59.100 | 4.961 | 0.818 | 97.603 | level | none |
| gnn_st | post_covid | 6.948 | 1890304.574 | 4.876 | 0.817 | 94.336 | blend | train |
| xgboost | post_covid | 7.040 | 3314314.083 | 4.881 | 0.860 | 96.078 | climatology | None |
| dualtopo | post_covid | 7.174 | 62.965 | 5.193 | 0.787 | 83.878 | level | train |
| arima | post_covid | 8.018 | 78.132 | 5.942 | 0.775 | 100.000 | level | none |
| persistence | post_covid | 9.607 | 74.877 | 6.849 | 0.689 | 95.425 | level | none |
| lstm | post_covid | 10.146 | 84.920 | 7.463 | 0.716 | 98.475 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `xgboost (post_covid)`
- **Flu season (Oct–Mar)**: `xgboost (post_covid)`
- **Off-season (Apr–Sep)**: `gat (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
