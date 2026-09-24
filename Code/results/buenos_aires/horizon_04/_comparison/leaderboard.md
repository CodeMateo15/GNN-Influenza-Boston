Ranked by **RMSE** within each segment, `scope=pooled`, horizon 4.

## Overall (full year) — 992 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 38.800 | 86.421 | 18.599 | 0.860 | 91.129 | level | none |
| arima | post_covid | 38.854 | 103.033 | 20.282 | 0.854 | 90.625 | level | none |
| gnn_st | post_covid | 39.556 | 112.664 | 17.005 | 0.862 | 94.859 | blend | train |
| gat | post_covid | 45.510 | 440563.377 | 23.158 | 0.784 | 91.230 | level | None |
| xgboost | post_covid | 53.763 | 146.675 | 23.151 | 0.696 | 93.145 | climatology | None |
| xgboost_nodemo | post_covid | 54.495 | 132.442 | 23.376 | 0.683 | 93.448 | climatology | None |
| seasonal_naive | post_covid | 57.423 | 118.566 | 25.483 | 0.645 | 94.456 | level | none |
| lstm | post_covid | 64.801 | 170.987 | 28.049 | 0.495 | 92.137 | level | train |
| dualtopo | post_covid | 66.120 | 432776.607 | 27.289 | 0.481 | 90.121 | level | train |

## Flu season (Apr–Sep) — 494 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 49.268 | 102.815 | 24.827 | 0.848 | 86.235 | level | none |
| persistence | post_covid | 50.074 | 99.880 | 24.591 | 0.846 | 87.854 | level | none |
| gnn_st | post_covid | 50.594 | 141.430 | 22.793 | 0.852 | 92.713 | blend | train |
| gat | post_covid | 51.851 | 287.989 | 28.696 | 0.820 | 90.688 | level | None |
| xgboost | post_covid | 67.430 | 167.857 | 30.888 | 0.684 | 91.296 | climatology | None |
| xgboost_nodemo | post_covid | 67.809 | 153.791 | 31.050 | 0.679 | 92.105 | climatology | None |
| seasonal_naive | post_covid | 73.421 | 119.415 | 33.900 | 0.615 | 92.105 | level | none |
| dualtopo | post_covid | 83.773 | 210.583 | 35.998 | 0.465 | 89.879 | level | train |
| lstm | post_covid | 84.320 | 209.880 | 38.151 | 0.439 | 89.474 | level | train |

## Off-season (Oct–Mar) — 498 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 22.619 | 73.181 | 12.656 | 0.875 | 94.378 | level | none |
| gnn_st | post_covid | 24.035 | 84.363 | 11.264 | 0.845 | 96.988 | blend | train |
| arima | post_covid | 24.480 | 103.247 | 15.774 | 0.875 | 94.980 | level | none |
| seasonal_naive | post_covid | 34.943 | 117.732 | 17.133 | 0.615 | 96.787 | level | none |
| xgboost | post_covid | 35.318 | 125.836 | 15.477 | 0.577 | 94.980 | climatology | None |
| lstm | post_covid | 36.219 | 132.723 | 18.028 | 0.547 | 94.779 | level | train |
| xgboost_nodemo | post_covid | 36.802 | 111.438 | 15.764 | 0.523 | 94.779 | climatology | None |
| gat | post_covid | 38.194 | 872833.757 | 17.664 | 0.480 | 91.767 | level | None |
| dualtopo | post_covid | 41.797 | 857477.795 | 18.650 | 0.350 | 90.361 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `persistence (post_covid)`
- **Flu season (Apr–Sep)**: `arima (post_covid)`
- **Off-season (Oct–Mar)**: `persistence (post_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
