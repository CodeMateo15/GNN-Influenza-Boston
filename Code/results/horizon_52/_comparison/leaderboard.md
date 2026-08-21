Ranked by **RMSE** within each segment, `scope=pooled`, horizon 52.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 27.507 | 118.067 | 15.618 | 0.518 | 82.616 | level | train |
| lstm | exclude_covid | 29.834 | 113.227 | 16.938 | 0.483 | 93.780 | level | train |
| lstm | post_covid | 29.917 | 229.326 | 20.284 | 0.445 | 85.965 | level | train |
| gnn_geo | post_covid | 29.981 | 100.572 | 15.509 | 0.385 | 79.904 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 30.069 | 113.821 | 16.639 | 0.428 | 80.542 | delta | all |
| dualtopo_no_bg | post_covid | 30.462 | 248.717 | 20.700 | 0.400 | 87.081 | level | train |
| gnn_multiedge_full | full | 31.053 | 126.322 | 17.277 | 0.488 | 93.461 | delta | train |
| gnn_multiedge_season_level | post_covid | 31.331 | 124.722 | 18.211 | 0.497 | 85.965 | level | train |
| gnn_multiedge_season | post_covid | 31.741 | 113.829 | 17.712 | 0.377 | 76.077 | delta | train |
| gnn_multiedge | post_covid | 31.974 | 127.296 | 18.154 | 0.435 | 80.702 | delta | train |
| gnn_uniform | post_covid | 32.189 | 112.236 | 17.620 | 0.370 | 80.383 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 32.451 | 110.954 | 15.935 | 0.253 | 86.124 | delta | train |
| gnn_multiedge_rt | post_covid | 32.546 | 108.646 | 17.925 | 0.335 | 75.439 | delta | train |
| dualtopo_fullhistory | full | 32.760 | 94.688 | 15.956 | 0.387 | 93.461 | level | train |
| gnn_corrbinary | post_covid | 33.593 | 119.270 | 17.916 | 0.284 | 79.745 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 33.931 | 111.361 | 17.596 | 0.267 | 80.702 | delta | train |
| arima | exclude_covid | 38.936 | 128.484 | 19.603 | 0.419 | 96.651 | level | none |
| persistence | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| persistence | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 77.352 | level | none |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 77.352 | level | none |
| arima | post_covid | 39.992 | 145.072 | 19.109 | 0.412 | 79.107 | level | none |
| dualtopo | post_covid | 96.205 | 233.498 | 39.690 | 0.152 | 71.292 | level | train |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 33.072 | 128.001 | 20.191 | 0.499 | 84.943 | level | train |
| lstm | post_covid | 34.127 | 131.184 | 21.655 | 0.462 | 82.955 | level | train |
| gnn_multiedge_level | post_covid | 35.668 | 120.027 | 22.547 | 0.423 | 71.591 | level | train |
| lstm | exclude_covid | 38.118 | 109.276 | 24.205 | 0.396 | 88.920 | level | train |
| gnn_geo | post_covid | 39.162 | 110.986 | 23.133 | 0.266 | 71.307 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 39.396 | 128.830 | 25.087 | 0.308 | 68.466 | delta | all |
| gnn_multiedge_season_level | post_covid | 40.560 | 140.076 | 26.853 | 0.394 | 76.136 | level | train |
| gnn_multiedge_full | full | 40.804 | 138.497 | 26.227 | 0.387 | 88.920 | delta | train |
| gnn_multiedge_season | post_covid | 40.846 | 117.478 | 25.423 | 0.272 | 68.182 | delta | train |
| gnn_multiedge_rt | post_covid | 41.794 | 116.130 | 25.755 | 0.225 | 69.034 | delta | train |
| gnn_multiedge | post_covid | 41.815 | 147.204 | 27.437 | 0.317 | 67.614 | delta | train |
| gnn_uniform | post_covid | 42.115 | 132.800 | 26.561 | 0.236 | 76.420 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 42.700 | 108.577 | 23.682 | 0.155 | 76.136 | delta | train |
| dualtopo_fullhistory | full | 43.341 | 105.124 | 24.744 | 0.279 | 88.352 | level | train |
| gnn_corrbinary | post_covid | 43.768 | 136.316 | 26.778 | 0.131 | 72.727 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 44.758 | 123.264 | 26.993 | 0.138 | 69.034 | delta | train |
| arima | exclude_covid | 51.575 | 154.730 | 30.834 | 0.319 | 94.318 | level | none |
| persistence | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| persistence | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 61.932 | level | none |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 61.932 | level | none |
| arima | post_covid | 52.843 | 143.858 | 28.885 | 0.331 | 66.193 | level | none |
| dualtopo | post_covid | 128.166 | 318.575 | 65.564 | 0.051 | 49.432 | level | train |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 6.514 | 81.329 | 4.708 | 0.788 | 100.000 | level | train |
| persistence | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| persistence | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 97.091 | level | none |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 97.091 | level | none |
| arima | exclude_covid | 7.192 | 94.890 | 5.228 | 0.686 | 99.636 | level | none |
| gnn_multiedge_covid_rsv | post_covid | 7.800 | 96.124 | 5.569 | 0.663 | 95.636 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 8.197 | 113.997 | 6.019 | 0.633 | 98.909 | delta | train |
| gnn_multiedge_full | full | 8.212 | 110.738 | 5.822 | 0.729 | 99.273 | delta | train |
| arima | post_covid | 8.497 | 146.626 | 6.595 | 0.588 | 95.636 | level | none |
| gnn_multiedge_leaknorm | post_covid | 8.647 | 94.609 | 5.827 | 0.728 | 96.000 | delta | all |
| dualtopo | post_covid | 8.733 | 124.599 | 6.572 | 0.802 | 99.273 | level | train |
| gnn_geo | post_covid | 9.295 | 87.241 | 5.750 | 0.667 | 90.909 | delta | train |
| gnn_uniform | post_covid | 9.594 | 85.914 | 6.176 | 0.685 | 85.455 | delta | train |
| gnn_multiedge | post_covid | 9.633 | 101.814 | 6.271 | 0.736 | 97.455 | delta | train |
| gnn_multiedge_level | post_covid | 9.833 | 115.557 | 6.748 | 0.809 | 96.727 | level | train |
| gnn_corrbinary | post_covid | 10.994 | 97.451 | 6.572 | 0.687 | 88.727 | delta | train |
| gnn_multiedge_season_level | post_covid | 11.506 | 105.070 | 7.148 | 0.785 | 98.545 | level | train |
| gnn_multiedge_season | post_covid | 12.711 | 109.158 | 7.841 | 0.714 | 86.182 | delta | train |
| lstm | exclude_covid | 13.019 | 118.283 | 7.636 | 0.756 | 100.000 | level | train |
| gnn_multiedge_rt | post_covid | 13.390 | 99.067 | 7.902 | 0.678 | 83.636 | delta | train |
| lstm | post_covid | 23.449 | 354.948 | 18.528 | 0.609 | 89.818 | level | train |
| dualtopo_no_bg | post_covid | 26.752 | 403.234 | 21.352 | 0.582 | 89.818 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_multiedge_level (post_covid)`
- **Flu season (Oct–Mar)**: `dualtopo_no_bg (post_covid)`
- **Off-season (Apr–Sep)**: `dualtopo_fullhistory (full)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
