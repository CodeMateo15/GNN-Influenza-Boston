Ranked by **RMSE** within each segment, `scope=pooled`, horizon 2.

## Overall (full year) — 901 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.516 | 2841561.123 | 5.811 | 0.902 | 94.784 | blend | train |
| gnn_st_v2 | post_covid | 8.579 | 2816237.197 | 5.842 | 0.901 | 94.784 | blend | train |
| gat | post_covid | 9.998 | 49.076 | 6.676 | 0.874 | 90.122 | level | None |
| xgboost | post_covid | 10.394 | 3302099.906 | 6.877 | 0.855 | 94.673 | climatology | None |
| lstm | post_covid | 10.465 | 54.898 | 7.241 | 0.847 | 94.340 | level | train |
| arima | post_covid | 11.432 | 55.378 | 7.489 | 0.809 | 91.010 | level | none |
| persistence | post_covid | 11.499 | 55.533 | 7.671 | 0.824 | 93.341 | level | none |
| dualtopo | post_covid | 14.169 | 71.552 | 9.476 | 0.687 | 72.919 | level | train |
| seasonal_naive | post_covid | 16.366 | 60.842 | 9.093 | 0.765 | 97.891 | level | none |

## Flu season (Oct–Mar) — 442 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.320 | 2714980.403 | 7.158 | 0.893 | 94.796 | blend | train |
| gnn_st_v2 | post_covid | 10.428 | 2659188.277 | 7.225 | 0.892 | 94.570 | blend | train |
| lstm | post_covid | 12.373 | 40.657 | 8.538 | 0.841 | 93.213 | level | train |
| gat | post_covid | 12.875 | 48.035 | 9.139 | 0.853 | 85.294 | level | None |
| xgboost | post_covid | 12.896 | 2989536.402 | 8.859 | 0.828 | 93.665 | climatology | None |
| arima | post_covid | 14.168 | 38.171 | 9.214 | 0.808 | 85.973 | level | none |
| persistence | post_covid | 14.306 | 45.997 | 9.821 | 0.801 | 93.439 | level | none |
| dualtopo | post_covid | 17.437 | 41.653 | 11.516 | 0.786 | 63.575 | level | train |
| seasonal_naive | post_covid | 22.319 | 62.620 | 13.384 | 0.712 | 98.190 | level | none |

## Off-season (Apr–Sep) — 459 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 6.050 | 50.097 | 4.305 | 0.852 | 94.771 | level | None |
| gnn_st_v2 | post_covid | 6.306 | 2969803.879 | 4.510 | 0.847 | 94.989 | blend | train |
| gnn_st | post_covid | 6.308 | 2965335.175 | 4.514 | 0.847 | 94.771 | blend | train |
| seasonal_naive | post_covid | 6.789 | 59.100 | 4.961 | 0.818 | 97.603 | level | none |
| xgboost | post_covid | 7.206 | 3607732.955 | 4.967 | 0.859 | 95.643 | climatology | None |
| persistence | post_covid | 7.904 | 64.878 | 5.601 | 0.774 | 93.246 | level | none |
| arima | post_covid | 7.954 | 72.240 | 5.828 | 0.798 | 95.861 | level | none |
| lstm | post_covid | 8.220 | 68.853 | 5.992 | 0.780 | 95.425 | level | train |
| dualtopo | post_covid | 10.066 | 100.852 | 7.512 | 0.776 | 81.917 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_st (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_st (post_covid)`
- **Off-season (Apr–Sep)**: `gat (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st, gnn_st_v2; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, gnn_st_v2, lstm). Differences here are not purely model quality.
