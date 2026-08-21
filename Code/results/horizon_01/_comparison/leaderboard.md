Ranked by **RMSE** within each segment, `scope=pooled`, horizon 1.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 14.657 | 65.959 | 7.846 | 0.883 | 94.577 | level | train |
| arima | exclude_covid | 15.160 | 86.129 | 8.855 | 0.877 | 95.056 | level | none |
| lstm | exclude_covid | 15.438 | 62.326 | 7.888 | 0.885 | 94.896 | level | train |
| arima | post_covid | 15.506 | 82.881 | 9.092 | 0.871 | 95.853 | level | none |
| persistence | exclude_covid | 15.806 | 66.533 | 8.937 | 0.871 | 95.056 | level | none |
| persistence | post_covid | 15.806 | 66.533 | 8.937 | 0.871 | 95.056 | level | none |
| gnn_multiedge_covid_rsv_full | full | 15.987 | 76.368 | 9.862 | 0.875 | 93.780 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 18.553 | 102.990 | 12.014 | 0.869 | 90.750 | delta | train |
| dualtopo_fullhistory | full | 19.552 | 88.228 | 10.563 | 0.804 | 90.909 | level | train |
| gnn_multiedge | post_covid | 24.898 | 117.799 | 15.366 | 0.835 | 87.400 | delta | train |
| dualtopo | post_covid | 28.915 | 206.272 | 18.202 | 0.417 | 86.922 | level | train |
| gnn_multiedge_season | post_covid | 28.928 | 129.956 | 17.645 | 0.836 | 85.965 | delta | train |
| gnn_uniform | post_covid | 28.953 | 120.498 | 16.729 | 0.830 | 84.530 | delta | train |
| dualtopo_no_bg | post_covid | 29.030 | 208.851 | 18.327 | 0.412 | 86.922 | level | train |
| gnn_corrbinary | post_covid | 31.788 | 138.629 | 19.132 | 0.816 | 83.892 | delta | train |
| gnn_multiedge_full | full | 32.221 | 141.038 | 19.449 | 0.743 | 80.861 | delta | train |
| gnn_multiedge_rt | post_covid | 32.978 | 139.007 | 19.328 | 0.790 | 80.223 | delta | train |
| gnn_geo | post_covid | 36.452 | 152.553 | 21.707 | 0.787 | 74.801 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 37.767 | 151.454 | 21.474 | 0.802 | 80.702 | delta | all |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| gnn_multiedge_level | post_covid | 50.202 | 201.237 | 28.276 | 0.623 | 64.274 | level | train |
| gnn_multiedge_season_level | post_covid | 50.619 | 193.411 | 28.300 | 0.700 | 62.679 | level | train |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 18.868 | 49.632 | 10.517 | 0.874 | 91.193 | level | train |
| arima | exclude_covid | 19.043 | 65.157 | 11.368 | 0.871 | 92.330 | level | none |
| arima | post_covid | 19.475 | 64.992 | 11.676 | 0.865 | 93.750 | level | none |
| gnn_multiedge_covid_rsv_full | full | 19.878 | 73.734 | 13.266 | 0.868 | 91.193 | delta | train |
| lstm | exclude_covid | 19.958 | 51.537 | 10.743 | 0.875 | 91.761 | level | train |
| persistence | exclude_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| persistence | post_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| gnn_multiedge_covid_rsv | post_covid | 21.117 | 86.720 | 14.384 | 0.876 | 89.205 | delta | train |
| dualtopo_fullhistory | full | 24.965 | 60.289 | 13.931 | 0.795 | 85.795 | level | train |
| gnn_multiedge | post_covid | 26.300 | 100.998 | 17.702 | 0.861 | 88.068 | delta | train |
| gnn_uniform | post_covid | 31.076 | 97.564 | 19.138 | 0.857 | 84.375 | delta | train |
| gnn_multiedge_season | post_covid | 32.655 | 119.929 | 21.629 | 0.849 | 84.091 | delta | train |
| dualtopo_no_bg | post_covid | 33.359 | 108.399 | 18.967 | 0.505 | 83.523 | level | train |
| dualtopo | post_covid | 33.359 | 108.234 | 18.961 | 0.505 | 83.523 | level | train |
| gnn_corrbinary | post_covid | 34.614 | 125.023 | 22.838 | 0.839 | 82.670 | delta | train |
| gnn_multiedge_full | full | 35.494 | 127.140 | 23.481 | 0.754 | 78.977 | delta | train |
| gnn_multiedge_rt | post_covid | 36.157 | 124.386 | 22.979 | 0.810 | 78.125 | delta | train |
| gnn_geo | post_covid | 39.393 | 138.510 | 25.979 | 0.813 | 71.875 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 39.723 | 126.393 | 24.416 | 0.841 | 81.534 | delta | all |
| gnn_multiedge_level | post_covid | 51.506 | 184.336 | 32.878 | 0.651 | 56.818 | level | train |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| gnn_multiedge_season_level | post_covid | 54.929 | 186.075 | 34.320 | 0.720 | 55.398 | level | train |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 5.794 | 76.136 | 4.235 | 0.793 | 98.909 | level | train |
| lstm | post_covid | 5.838 | 86.857 | 4.427 | 0.796 | 98.909 | level | train |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| persistence | exclude_covid | 7.132 | 73.771 | 4.950 | 0.688 | 97.455 | level | none |
| persistence | post_covid | 7.132 | 73.771 | 4.950 | 0.688 | 97.455 | level | none |
| arima | exclude_covid | 7.732 | 112.973 | 5.638 | 0.699 | 98.545 | level | none |
| arima | post_covid | 7.921 | 105.779 | 5.785 | 0.670 | 98.545 | level | none |
| dualtopo_fullhistory | full | 8.590 | 123.990 | 6.252 | 0.740 | 97.455 | level | train |
| gnn_multiedge_covid_rsv_full | full | 8.772 | 79.741 | 5.506 | 0.687 | 97.091 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 14.629 | 123.815 | 8.979 | 0.721 | 92.727 | delta | train |
| dualtopo | post_covid | 21.950 | 331.761 | 17.230 | 0.599 | 91.273 | level | train |
| dualtopo_no_bg | post_covid | 22.294 | 337.430 | 17.508 | 0.593 | 91.273 | level | train |
| gnn_multiedge | post_covid | 22.980 | 139.304 | 12.375 | 0.700 | 86.545 | delta | train |
| gnn_multiedge_season | post_covid | 23.303 | 142.791 | 12.547 | 0.707 | 88.364 | delta | train |
| gnn_uniform | post_covid | 25.984 | 149.853 | 13.645 | 0.698 | 84.727 | delta | train |
| gnn_multiedge_full | full | 27.467 | 158.828 | 14.287 | 0.697 | 83.273 | delta | train |
| gnn_corrbinary | post_covid | 27.753 | 156.045 | 14.389 | 0.698 | 85.455 | delta | train |
| gnn_multiedge_rt | post_covid | 28.394 | 157.722 | 14.655 | 0.690 | 82.909 | delta | train |
| gnn_geo | post_covid | 32.298 | 170.527 | 16.239 | 0.690 | 78.545 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 35.103 | 183.532 | 17.708 | 0.685 | 79.636 | delta | all |
| gnn_multiedge_season_level | post_covid | 44.498 | 202.802 | 20.595 | 0.681 | 72.000 | level | train |
| gnn_multiedge_level | post_covid | 48.481 | 222.870 | 22.385 | 0.682 | 73.818 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `lstm (post_covid)`
- **Flu season (Oct–Mar)**: `lstm (post_covid)`
- **Off-season (Apr–Sep)**: `lstm (exclude_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
