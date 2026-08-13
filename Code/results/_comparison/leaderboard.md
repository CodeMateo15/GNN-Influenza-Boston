Ranked by **RMSE** within each segment, `scope=pooled`, horizon 1.

## Overall (full year) — 614–627 cells scored (models differ)

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 15.267 | 85.374 | 8.785 | 0.875 | 95.765 | level | none |
| arima | post_covid | 15.590 | 82.437 | 9.112 | 0.872 | 96.417 | level | none |
| lstm | exclude_covid | 15.936 | 65.152 | 8.246 | 0.871 | 94.300 | level | train |
| persistence | exclude_covid | 15.948 | 66.909 | 9.035 | 0.871 | 95.114 | level | none |
| persistence | post_covid | 15.948 | 66.909 | 9.035 | 0.871 | 95.277 | level | none |
| lstm | post_covid | 16.186 | 68.413 | 8.494 | 0.863 | 94.300 | level | train |
| gnn_multiedge_covid_rsv | post_covid | 16.780 | 93.791 | 10.741 | 0.867 | 94.463 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 18.552 | 93.458 | 11.535 | 0.883 | 95.114 | delta | all |
| dualtopo_fullhistory | full | 19.552 | 88.228 | 10.563 | 0.804 | 90.909 | level | train |
| gnn_multiedge_covid_rsv_full | full | 19.945 | 92.026 | 12.305 | 0.876 | 91.205 | delta | train |
| gnn_multiedge_full | full | 20.525 | 91.879 | 12.208 | 0.866 | 90.554 | delta | train |
| gnn_multiedge_rt | post_covid | 23.029 | 105.160 | 13.860 | 0.855 | 91.205 | delta | train |
| gnn_multiedge | post_covid | 24.535 | 113.100 | 14.891 | 0.860 | 89.251 | delta | train |
| dualtopo | post_covid | 28.915 | 206.272 | 18.202 | 0.417 | 86.922 | level | train |
| dualtopo_no_bg | post_covid | 29.030 | 208.851 | 18.327 | 0.412 | 86.922 | level | train |
| gnn_corrbinary | post_covid | 31.028 | 129.878 | 18.191 | 0.808 | 87.948 | delta | train |
| gnn_uniform | post_covid | 31.899 | 130.022 | 18.632 | 0.810 | 83.225 | delta | train |
| gnn_geo | post_covid | 33.824 | 140.071 | 19.651 | 0.804 | 85.016 | delta | train |
| seasonal_naive | exclude_covid | 40.232 | 132.367 | 20.105 | 0.416 | 94.788 | level | none |
| seasonal_naive | post_covid | 40.232 | 132.367 | 20.105 | 0.416 | 97.394 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 18.778 | 63.467 | 11.038 | 0.872 | 93.466 | level | none |
| arima | post_covid | 19.396 | 64.092 | 11.539 | 0.866 | 94.318 | level | none |
| gnn_multiedge_covid_rsv | post_covid | 19.643 | 80.062 | 13.193 | 0.869 | 93.182 | delta | train |
| persistence | exclude_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| persistence | post_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| lstm | exclude_covid | 20.412 | 51.759 | 11.139 | 0.860 | 90.341 | level | train |
| lstm | post_covid | 20.618 | 53.703 | 11.304 | 0.852 | 90.341 | level | train |
| gnn_multiedge_leaknorm | post_covid | 20.966 | 81.006 | 13.752 | 0.892 | 95.170 | delta | all |
| gnn_multiedge_full | full | 23.067 | 78.065 | 14.464 | 0.877 | 90.625 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 23.947 | 86.861 | 15.865 | 0.873 | 90.341 | delta | train |
| dualtopo_fullhistory | full | 24.965 | 60.289 | 13.931 | 0.795 | 85.795 | level | train |
| gnn_multiedge_rt | post_covid | 26.228 | 95.437 | 16.907 | 0.863 | 89.489 | delta | train |
| gnn_multiedge | post_covid | 26.938 | 100.656 | 17.743 | 0.878 | 89.489 | delta | train |
| gnn_corrbinary | post_covid | 33.107 | 117.330 | 21.497 | 0.834 | 88.636 | delta | train |
| dualtopo_no_bg | post_covid | 33.359 | 108.399 | 18.967 | 0.505 | 83.523 | level | train |
| dualtopo | post_covid | 33.359 | 108.234 | 18.961 | 0.505 | 83.523 | level | train |
| gnn_uniform | post_covid | 34.507 | 117.604 | 22.269 | 0.834 | 81.818 | delta | train |
| gnn_geo | post_covid | 36.685 | 125.474 | 23.557 | 0.827 | 83.807 | delta | train |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |

## Off-season (Apr–Sep) — 262–275 cells scored (models differ)

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 5.949 | 83.146 | 4.358 | 0.797 | 99.618 | level | train |
| lstm | post_covid | 6.548 | 88.175 | 4.719 | 0.783 | 99.618 | level | train |
| seasonal_naive | exclude_covid | 6.775 | 94.886 | 4.987 | 0.714 | 99.618 | level | none |
| seasonal_naive | post_covid | 6.775 | 94.886 | 4.987 | 0.714 | 100.000 | level | none |
| persistence | exclude_covid | 7.179 | 75.013 | 4.982 | 0.681 | 97.710 | level | none |
| persistence | post_covid | 7.179 | 75.013 | 4.982 | 0.681 | 98.092 | level | none |
| arima | post_covid | 8.012 | 107.084 | 5.851 | 0.654 | 99.237 | level | none |
| arima | exclude_covid | 8.517 | 114.806 | 5.759 | 0.664 | 98.855 | level | none |
| dualtopo_fullhistory | full | 8.590 | 123.990 | 6.252 | 0.740 | 97.455 | level | train |
| gnn_multiedge_covid_rsv | post_covid | 11.895 | 112.237 | 7.446 | 0.723 | 96.183 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 12.720 | 98.965 | 7.521 | 0.721 | 92.366 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 14.696 | 110.187 | 8.557 | 0.709 | 95.038 | delta | all |
| gnn_multiedge_full | full | 16.505 | 110.438 | 9.177 | 0.706 | 90.458 | delta | train |
| gnn_multiedge_rt | post_covid | 17.849 | 118.223 | 9.767 | 0.703 | 93.511 | delta | train |
| gnn_multiedge | post_covid | 20.876 | 129.820 | 11.059 | 0.697 | 88.931 | delta | train |
| dualtopo | post_covid | 21.950 | 331.761 | 17.230 | 0.599 | 91.273 | level | train |
| dualtopo_no_bg | post_covid | 22.294 | 337.430 | 17.508 | 0.593 | 91.273 | level | train |
| gnn_corrbinary | post_covid | 27.994 | 146.736 | 13.750 | 0.682 | 87.023 | delta | train |
| gnn_uniform | post_covid | 28.017 | 146.705 | 13.745 | 0.688 | 85.115 | delta | train |
| gnn_geo | post_covid | 29.547 | 159.683 | 14.402 | 0.692 | 86.641 | delta | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `arima (exclude_covid)`
- **Flu season (Oct–Mar)**: `arima (exclude_covid)`
- **Off-season (Apr–Sep)**: `lstm (exclude_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- 'off_season': most models were scored on 262 cells, but — 275 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall': most models were scored on 614 cells, but — 627 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_rt, gnn_uniform, lstm). Differences here are not purely model quality.
