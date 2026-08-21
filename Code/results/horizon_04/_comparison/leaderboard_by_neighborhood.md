# Per-neighborhood leaderboard — horizon 4

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | 7 | 6 | 0 |
| dualtopo_fullhistory | 5 | 4 | 13 |
| gnn_multiedge_covid_rsv_full | 1 | 0 | 0 |
| gnn_multiedge_season_level | 1 | 1 | 0 |
| arima | 0 | 1 | 0 |
| gnn_multiedge_season | 0 | 1 | 0 |
| lstm | 0 | 1 | 0 |
| seasonal_naive | 0 | 0 | 1 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `dualtopo_fullhistory (full)`: Allston, BackBay+, Charles., E.Boston, W.Roxbury; `gnn_multiedge_covid_rsv (post_covid)`: Dorchest., HydePark, JP, Mattapan, Roxbury, S.Boston, S.End; `gnn_multiedge_covid_rsv_full (full)`: Fenway; `gnn_multiedge_season_level (post_covid)`: Roslind.
- **Flu season (Oct–Mar)** — `arima (post_covid)`: Fenway; `dualtopo_fullhistory (full)`: BackBay+, Charles., E.Boston, W.Roxbury; `gnn_multiedge_covid_rsv (post_covid)`: Dorchest., HydePark, JP, Roxbury, S.Boston, S.End; `gnn_multiedge_season (post_covid)`: Allston; `gnn_multiedge_season_level (post_covid)`: Roslind.; `lstm (post_covid)`: Mattapan
- **Off-season (Apr–Sep)** — `dualtopo_fullhistory (full)`: Allston, BackBay+, Charles., Dorchest., E.Boston, Fenway, HydePark, JP, Mattapan, Roslind., S.Boston, S.End, W.Roxbury; `seasonal_naive (exclude_covid)`: Roxbury

`gnn_multiedge_covid_rsv (post_covid)` wins 7 of 14 neighborhoods. `gnn_multiedge_covid_rsv (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 42.312 | 95.077 | 27.852 | 0.637 | 87.755 |
| gnn_multiedge_covid_rsv_full | full | 42.774 | 68.718 | 22.531 | 0.630 | 91.837 |
| lstm | post_covid | 52.892 | 90.447 | 32.250 | 0.425 | 85.714 |
| gnn_multiedge_season | post_covid | 55.121 | 81.980 | 33.490 | 0.588 | 81.633 |
| arima | post_covid | 56.091 | 191.089 | 41.293 | 0.325 | 93.878 |
| dualtopo_no_bg | post_covid | 56.489 | 254.880 | 43.326 | 0.579 | 57.143 |
| dualtopo | post_covid | 56.928 | 260.418 | 43.972 | 0.584 | 57.143 |
| arima | exclude_covid | 58.307 | 130.557 | 37.547 | 0.318 | 91.837 |
| dualtopo_fullhistory | full | 59.395 | 52.325 | 30.368 | 0.176 | 75.510 |
| gnn_multiedge_season_level | post_covid | 59.720 | 89.302 | 37.900 | 0.515 | 77.551 |
| lstm | exclude_covid | 62.856 | 112.116 | 39.410 | 0.324 | 75.510 |
| persistence | post_covid | 64.708 | 77.731 | 36.261 | 0.303 | 91.837 |
| persistence | exclude_covid | 64.708 | 77.731 | 36.261 | 0.303 | 91.837 |
| gnn_multiedge_full | full | 66.753 | 101.946 | 43.407 | 0.511 | 71.429 |
| gnn_multiedge_rt | post_covid | 75.325 | 119.371 | 47.036 | 0.372 | 73.469 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| gnn_multiedge | post_covid | 83.533 | 129.902 | 54.002 | 0.412 | 65.306 |
| gnn_corrbinary | post_covid | 85.355 | 150.786 | 52.575 | 0.372 | 73.469 |
| gnn_multiedge_leaknorm | post_covid | 94.008 | 147.035 | 57.728 | 0.325 | 73.469 |
| gnn_multiedge_level | post_covid | 95.372 | 210.668 | 62.963 | 0.382 | 65.306 |
| gnn_uniform | post_covid | 102.023 | 174.841 | 60.072 | 0.343 | 75.510 |
| gnn_geo | post_covid | 134.531 | 196.560 | 83.606 | 0.277 | 69.388 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 53.249 | 55.396 | 36.728 | 0.643 | 76.923 |
| gnn_multiedge_covid_rsv_full | full | 57.434 | 41.974 | 33.067 | 0.499 | 84.615 |
| dualtopo_no_bg | post_covid | 63.465 | 81.659 | 41.059 | 0.383 | 73.077 |
| dualtopo | post_covid | 63.474 | 83.191 | 41.326 | 0.345 | 73.077 |
| lstm | post_covid | 66.628 | 50.704 | 42.325 | 0.327 | 80.769 |
| arima | post_covid | 69.938 | 84.191 | 48.840 | 0.204 | 88.462 |
| gnn_multiedge_season | post_covid | 70.321 | 66.724 | 46.803 | 0.476 | 73.077 |
| arima | exclude_covid | 75.747 | 72.875 | 50.400 | 0.190 | 84.615 |
| gnn_multiedge_season_level | post_covid | 76.435 | 80.977 | 54.406 | 0.335 | 69.231 |
| gnn_corrbinary | post_covid | 79.310 | 83.393 | 54.745 | 0.376 | 69.231 |
| gnn_multiedge_full | full | 80.956 | 87.487 | 58.670 | 0.375 | 65.385 |
| lstm | exclude_covid | 81.081 | 74.619 | 55.069 | 0.169 | 65.385 |
| dualtopo_fullhistory | full | 81.119 | 54.154 | 50.977 | -0.099 | 53.846 |
| gnn_uniform | post_covid | 82.078 | 87.807 | 55.912 | 0.405 | 73.077 |
| persistence | exclude_covid | 87.420 | 76.765 | 57.735 | 0.089 | 84.615 |
| persistence | post_covid | 87.420 | 76.765 | 57.735 | 0.089 | 84.615 |
| gnn_multiedge | post_covid | 87.611 | 95.060 | 65.004 | 0.397 | 53.846 |
| gnn_multiedge_leaknorm | post_covid | 92.782 | 94.496 | 64.938 | 0.295 | 69.231 |
| gnn_multiedge_rt | post_covid | 93.954 | 105.082 | 66.026 | 0.188 | 65.385 |
| gnn_multiedge_level | post_covid | 98.983 | 121.370 | 68.838 | 0.289 | 65.385 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |
| gnn_geo | post_covid | 140.388 | 155.107 | 99.710 | 0.137 | 61.538 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 8.782 | 50.256 | 7.070 | 0.704 | 100.000 |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 12.999 | 98.949 | 10.621 | 0.594 | 100.000 |
| persistence | exclude_covid | 16.774 | 78.824 | 11.987 | 0.727 | 100.000 |
| persistence | post_covid | 16.774 | 78.824 | 11.987 | 0.727 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 24.673 | 139.934 | 17.820 | 0.716 | 100.000 |
| arima | exclude_covid | 27.509 | 195.763 | 23.017 | 0.524 | 100.000 |
| gnn_multiedge_season | post_covid | 29.714 | 99.226 | 18.441 | 0.758 | 91.304 |
| lstm | post_covid | 30.687 | 135.375 | 20.862 | 0.670 | 91.304 |
| lstm | exclude_covid | 31.391 | 154.503 | 21.709 | 0.647 | 86.957 |
| gnn_multiedge_season_level | post_covid | 31.525 | 98.713 | 19.241 | 0.777 | 86.957 |
| arima | post_covid | 34.255 | 311.929 | 32.762 | 0.651 | 100.000 |
| gnn_multiedge_full | full | 45.656 | 118.292 | 26.153 | 0.750 | 78.261 |
| gnn_multiedge_rt | post_covid | 45.925 | 135.523 | 25.570 | 0.394 | 82.609 |
| dualtopo_no_bg | post_covid | 47.383 | 450.694 | 45.889 | 0.711 | 39.130 |
| dualtopo | post_covid | 48.476 | 460.761 | 46.963 | 0.797 | 39.130 |
| gnn_multiedge | post_covid | 78.668 | 169.289 | 41.565 | 0.714 | 78.261 |
| gnn_multiedge_level | post_covid | 91.117 | 311.615 | 56.322 | 0.694 | 65.217 |
| gnn_corrbinary | post_covid | 91.710 | 226.970 | 50.122 | 0.735 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 95.374 | 206.427 | 49.576 | 0.697 | 78.261 |
| gnn_uniform | post_covid | 120.663 | 273.227 | 64.774 | 0.757 | 78.261 |
| gnn_geo | post_covid | 127.585 | 243.419 | 65.401 | 0.745 | 78.261 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 41.143 | 101.679 | 28.575 | 0.586 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 43.083 | 85.902 | 27.463 | 0.535 | 83.673 |
| lstm | post_covid | 47.069 | 74.241 | 26.809 | 0.416 | 89.796 |
| arima | post_covid | 49.007 | 164.906 | 32.867 | 0.341 | 95.918 |
| arima | exclude_covid | 49.636 | 197.304 | 35.765 | 0.340 | 93.878 |
| dualtopo_no_bg | post_covid | 51.007 | 233.134 | 37.804 | 0.519 | 65.306 |
| dualtopo | post_covid | 51.336 | 238.163 | 38.338 | 0.522 | 65.306 |
| gnn_multiedge_season | post_covid | 52.863 | 98.123 | 35.185 | 0.535 | 79.592 |
| gnn_multiedge_season_level | post_covid | 53.745 | 90.303 | 35.363 | 0.474 | 81.633 |
| dualtopo_fullhistory | full | 55.466 | 63.589 | 30.064 | 0.084 | 73.469 |
| lstm | exclude_covid | 58.201 | 93.014 | 36.277 | 0.339 | 75.510 |
| persistence | post_covid | 58.963 | 83.882 | 34.992 | 0.314 | 91.837 |
| persistence | exclude_covid | 58.963 | 83.882 | 34.992 | 0.314 | 91.837 |
| gnn_multiedge_full | full | 63.706 | 122.125 | 43.785 | 0.467 | 67.347 |
| gnn_multiedge_rt | post_covid | 69.957 | 135.477 | 46.483 | 0.329 | 69.388 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| gnn_multiedge | post_covid | 75.530 | 137.739 | 51.703 | 0.389 | 63.265 |
| gnn_corrbinary | post_covid | 76.701 | 159.587 | 51.606 | 0.341 | 65.306 |
| gnn_multiedge_level | post_covid | 84.235 | 204.490 | 55.766 | 0.334 | 65.306 |
| gnn_multiedge_leaknorm | post_covid | 86.045 | 162.530 | 56.826 | 0.300 | 63.265 |
| gnn_uniform | post_covid | 89.442 | 180.629 | 57.508 | 0.332 | 67.347 |
| gnn_geo | post_covid | 114.185 | 195.181 | 71.920 | 0.246 | 69.388 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 51.509 | 68.127 | 37.609 | 0.586 | 84.615 |
| gnn_multiedge_covid_rsv_full | full | 56.990 | 63.848 | 39.666 | 0.407 | 76.923 |
| lstm | post_covid | 59.816 | 46.223 | 35.199 | 0.350 | 80.769 |
| dualtopo | post_covid | 59.877 | 92.806 | 39.127 | 0.275 | 73.077 |
| dualtopo_no_bg | post_covid | 59.890 | 91.287 | 38.923 | 0.307 | 73.077 |
| arima | exclude_covid | 60.217 | 87.202 | 39.773 | 0.228 | 88.462 |
| arima | post_covid | 61.944 | 79.324 | 39.623 | 0.212 | 92.308 |
| gnn_multiedge_season | post_covid | 67.901 | 91.728 | 50.533 | 0.417 | 69.231 |
| gnn_multiedge_season_level | post_covid | 69.555 | 93.215 | 52.018 | 0.295 | 69.231 |
| lstm | exclude_covid | 74.697 | 78.977 | 51.408 | 0.195 | 65.385 |
| dualtopo_fullhistory | full | 75.397 | 62.001 | 48.846 | -0.178 | 57.692 |
| gnn_corrbinary | post_covid | 76.573 | 110.870 | 58.448 | 0.315 | 53.846 |
| gnn_uniform | post_covid | 77.022 | 114.209 | 58.697 | 0.366 | 57.692 |
| gnn_multiedge_full | full | 78.541 | 111.098 | 59.523 | 0.326 | 61.538 |
| persistence | exclude_covid | 79.131 | 80.738 | 53.385 | 0.130 | 84.615 |
| persistence | post_covid | 79.131 | 80.738 | 53.385 | 0.130 | 84.615 |
| gnn_multiedge | post_covid | 82.384 | 113.206 | 64.243 | 0.357 | 50.000 |
| gnn_multiedge_rt | post_covid | 88.064 | 134.157 | 65.334 | 0.152 | 57.692 |
| gnn_multiedge_leaknorm | post_covid | 88.696 | 121.535 | 67.002 | 0.258 | 50.000 |
| gnn_multiedge_level | post_covid | 89.011 | 135.686 | 63.616 | 0.235 | 61.538 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |
| gnn_geo | post_covid | 119.562 | 161.945 | 84.307 | 0.126 | 65.385 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| dualtopo_fullhistory | full | 11.324 | 65.384 | 8.833 | 0.538 | 91.304 |
| gnn_multiedge_covid_rsv_full | full | 16.817 | 110.832 | 13.669 | 0.099 | 91.304 |
| persistence | exclude_covid | 18.119 | 87.435 | 14.200 | 0.415 | 100.000 |
| persistence | post_covid | 18.119 | 87.435 | 14.200 | 0.415 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 24.637 | 139.606 | 18.362 | 0.273 | 100.000 |
| lstm | post_covid | 25.989 | 105.914 | 17.324 | 0.570 | 100.000 |
| gnn_multiedge_season_level | post_covid | 26.171 | 87.011 | 16.536 | 0.667 | 95.652 |
| gnn_multiedge_season | post_covid | 27.230 | 105.353 | 17.835 | 0.467 | 91.304 |
| arima | post_covid | 27.912 | 261.652 | 25.229 | 0.363 | 100.000 |
| lstm | exclude_covid | 30.151 | 108.882 | 19.172 | 0.574 | 86.957 |
| arima | exclude_covid | 33.909 | 321.767 | 31.234 | 0.285 | 100.000 |
| dualtopo_no_bg | post_covid | 38.577 | 393.482 | 36.538 | 0.587 | 56.522 |
| dualtopo | post_covid | 39.516 | 402.479 | 37.446 | 0.654 | 56.522 |
| gnn_multiedge_rt | post_covid | 40.738 | 136.968 | 25.172 | 0.219 | 82.609 |
| gnn_multiedge_full | full | 40.902 | 134.591 | 25.993 | 0.548 | 73.913 |
| gnn_multiedge | post_covid | 66.941 | 165.471 | 37.528 | 0.520 | 78.261 |
| gnn_corrbinary | post_covid | 76.846 | 214.659 | 43.872 | 0.552 | 78.261 |
| gnn_multiedge_level | post_covid | 78.487 | 282.268 | 46.893 | 0.542 | 69.565 |
| gnn_multiedge_leaknorm | post_covid | 82.946 | 208.871 | 45.322 | 0.499 | 78.261 |
| gnn_uniform | post_covid | 101.671 | 255.713 | 56.164 | 0.584 | 78.261 |
| gnn_geo | post_covid | 107.785 | 232.752 | 57.917 | 0.579 | 73.913 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 33.799 | 109.361 | 22.121 | 0.539 | 85.714 |
| lstm | post_covid | 35.051 | 75.209 | 19.970 | 0.464 | 88.095 |
| gnn_multiedge_season | post_covid | 37.035 | 116.948 | 23.284 | 0.501 | 90.476 |
| dualtopo_fullhistory | full | 37.066 | 77.977 | 19.532 | 0.390 | 83.333 |
| gnn_multiedge_covid_rsv | post_covid | 37.637 | 108.063 | 23.740 | 0.372 | 90.476 |
| gnn_multiedge_covid_rsv_full | full | 38.318 | 96.232 | 21.533 | 0.356 | 80.952 |
| dualtopo_no_bg | post_covid | 38.664 | 165.383 | 25.883 | 0.442 | 90.476 |
| dualtopo | post_covid | 38.755 | 168.256 | 26.128 | 0.445 | 90.476 |
| lstm | exclude_covid | 39.610 | 100.014 | 24.233 | 0.319 | 83.333 |
| arima | post_covid | 42.984 | 160.756 | 28.581 | 0.122 | 90.476 |
| arima | exclude_covid | 47.059 | 123.301 | 27.943 | 0.110 | 90.476 |
| gnn_multiedge_full | full | 47.498 | 152.109 | 28.472 | 0.366 | 85.714 |
| gnn_multiedge_level | post_covid | 47.739 | 208.159 | 33.718 | 0.393 | 66.667 |
| gnn_multiedge_rt | post_covid | 48.755 | 178.557 | 32.779 | 0.274 | 71.429 |
| gnn_multiedge | post_covid | 48.859 | 156.312 | 33.385 | 0.367 | 66.667 |
| gnn_corrbinary | post_covid | 49.423 | 169.869 | 33.284 | 0.323 | 71.429 |
| persistence | exclude_covid | 52.201 | 116.971 | 28.979 | 0.113 | 90.476 |
| persistence | post_covid | 52.201 | 116.971 | 28.979 | 0.113 | 90.476 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |
| gnn_uniform | post_covid | 53.577 | 175.153 | 35.256 | 0.322 | 69.048 |
| gnn_multiedge_leaknorm | post_covid | 57.584 | 191.121 | 38.405 | 0.295 | 64.286 |
| gnn_geo | post_covid | 66.755 | 208.516 | 43.943 | 0.265 | 76.190 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 41.473 | 131.076 | 29.180 | 0.464 | 76.923 |
| lstm | post_covid | 42.699 | 64.648 | 24.966 | 0.500 | 80.769 |
| gnn_multiedge_season | post_covid | 45.835 | 136.781 | 30.940 | 0.418 | 84.615 |
| dualtopo | post_covid | 46.400 | 121.921 | 30.572 | 0.301 | 84.615 |
| dualtopo_no_bg | post_covid | 46.405 | 120.480 | 30.466 | 0.323 | 84.615 |
| dualtopo_fullhistory | full | 46.695 | 93.466 | 27.912 | 0.242 | 76.923 |
| gnn_multiedge_covid_rsv | post_covid | 47.009 | 113.834 | 32.526 | 0.307 | 84.615 |
| gnn_multiedge_covid_rsv_full | full | 48.075 | 107.596 | 29.748 | 0.253 | 73.077 |
| lstm | exclude_covid | 48.914 | 110.750 | 32.533 | 0.234 | 73.077 |
| gnn_multiedge_level | post_covid | 49.733 | 211.949 | 36.856 | 0.383 | 61.538 |
| gnn_uniform | post_covid | 50.064 | 157.928 | 34.960 | 0.363 | 65.385 |
| gnn_corrbinary | post_covid | 51.948 | 172.293 | 36.479 | 0.305 | 69.231 |
| arima | post_covid | 52.944 | 140.648 | 37.048 | 0.054 | 84.615 |
| gnn_multiedge | post_covid | 54.363 | 166.670 | 38.995 | 0.339 | 61.538 |
| gnn_multiedge_full | full | 57.564 | 179.357 | 35.895 | 0.270 | 80.769 |
| arima | exclude_covid | 58.660 | 113.156 | 36.675 | 0.033 | 84.615 |
| gnn_multiedge_rt | post_covid | 58.985 | 222.350 | 42.852 | 0.156 | 65.385 |
| gnn_multiedge_leaknorm | post_covid | 59.365 | 194.344 | 41.940 | 0.280 | 57.692 |
| persistence | exclude_covid | 65.810 | 150.159 | 41.946 | -0.006 | 84.615 |
| persistence | post_covid | 65.810 | 150.159 | 41.946 | -0.006 | 84.615 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |
| gnn_geo | post_covid | 68.379 | 218.474 | 47.897 | 0.224 | 80.769 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 7.954 | 52.809 | 5.915 | 0.594 | 93.750 |
| gnn_multiedge_covid_rsv_full | full | 9.919 | 77.766 | 8.185 | 0.248 | 93.750 |
| persistence | exclude_covid | 10.735 | 63.039 | 7.906 | 0.468 | 100.000 |
| persistence | post_covid | 10.735 | 63.039 | 7.906 | 0.468 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.285 | 98.686 | 9.463 | 0.388 | 100.000 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| gnn_multiedge_season | post_covid | 13.658 | 84.721 | 10.843 | 0.511 | 100.000 |
| gnn_multiedge_season_level | post_covid | 14.276 | 74.074 | 10.650 | 0.626 | 100.000 |
| arima | exclude_covid | 14.880 | 139.788 | 13.754 | -0.133 | 100.000 |
| lstm | exclude_covid | 15.183 | 82.568 | 10.744 | 0.513 | 100.000 |
| lstm | post_covid | 16.196 | 92.372 | 11.851 | 0.552 | 100.000 |
| arima | post_covid | 17.175 | 193.433 | 14.821 | 0.306 | 100.000 |
| dualtopo_no_bg | post_covid | 20.613 | 238.352 | 18.437 | 0.554 | 100.000 |
| dualtopo | post_covid | 21.071 | 243.549 | 18.908 | 0.610 | 100.000 |
| gnn_multiedge_full | full | 23.186 | 107.830 | 16.409 | 0.523 | 93.750 |
| gnn_multiedge_rt | post_covid | 24.204 | 107.393 | 16.409 | 0.404 | 81.250 |
| gnn_multiedge | post_covid | 38.261 | 139.479 | 24.269 | 0.535 | 75.000 |
| gnn_multiedge_level | post_covid | 44.308 | 202.001 | 28.620 | 0.529 | 75.000 |
| gnn_corrbinary | post_covid | 45.020 | 165.932 | 28.092 | 0.560 | 75.000 |
| gnn_multiedge_leaknorm | post_covid | 54.566 | 185.884 | 32.661 | 0.539 | 75.000 |
| gnn_uniform | post_covid | 58.841 | 203.142 | 35.737 | 0.576 | 75.000 |
| gnn_geo | post_covid | 64.029 | 192.334 | 37.518 | 0.587 | 68.750 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 24.080 | 103.153 | 15.687 | 0.673 | 91.837 |
| lstm | post_covid | 26.851 | 101.505 | 15.779 | 0.564 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 28.090 | 96.686 | 17.831 | 0.515 | 87.755 |
| gnn_multiedge_season_level | post_covid | 29.427 | 97.411 | 19.164 | 0.570 | 89.796 |
| gnn_multiedge_season | post_covid | 30.033 | 102.202 | 18.148 | 0.596 | 89.796 |
| arima | post_covid | 30.275 | 164.618 | 21.576 | 0.379 | 97.959 |
| dualtopo_no_bg | post_covid | 32.410 | 222.505 | 24.161 | 0.519 | 89.796 |
| dualtopo | post_covid | 32.591 | 227.090 | 24.472 | 0.531 | 89.796 |
| lstm | exclude_covid | 33.690 | 97.098 | 21.323 | 0.404 | 87.755 |
| dualtopo_fullhistory | full | 35.436 | 59.635 | 18.500 | 0.052 | 81.633 |
| arima | exclude_covid | 35.980 | 108.764 | 21.985 | 0.313 | 91.837 |
| persistence | post_covid | 37.617 | 96.018 | 22.543 | 0.310 | 91.837 |
| persistence | exclude_covid | 37.617 | 96.018 | 22.543 | 0.310 | 91.837 |
| gnn_multiedge_full | full | 39.317 | 139.610 | 24.961 | 0.469 | 81.633 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| gnn_multiedge_rt | post_covid | 43.084 | 148.903 | 26.589 | 0.338 | 79.592 |
| gnn_multiedge | post_covid | 43.222 | 157.538 | 28.988 | 0.437 | 69.388 |
| gnn_corrbinary | post_covid | 44.447 | 182.879 | 29.667 | 0.365 | 75.510 |
| gnn_multiedge_level | post_covid | 47.150 | 217.261 | 31.105 | 0.402 | 73.469 |
| gnn_multiedge_leaknorm | post_covid | 50.650 | 192.894 | 33.184 | 0.331 | 73.469 |
| gnn_uniform | post_covid | 51.932 | 214.180 | 32.695 | 0.346 | 77.551 |
| gnn_geo | post_covid | 67.401 | 228.318 | 41.321 | 0.250 | 81.633 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 31.798 | 93.158 | 22.598 | 0.634 | 84.615 |
| lstm | post_covid | 35.449 | 74.585 | 21.823 | 0.474 | 84.615 |
| gnn_multiedge_season_level | post_covid | 37.194 | 97.307 | 27.236 | 0.466 | 84.615 |
| gnn_multiedge_covid_rsv_full | full | 37.887 | 95.001 | 27.717 | 0.386 | 76.923 |
| arima | post_covid | 38.840 | 117.493 | 27.995 | 0.250 | 96.154 |
| dualtopo | post_covid | 38.886 | 135.114 | 26.072 | 0.336 | 80.769 |
| dualtopo_no_bg | post_covid | 38.892 | 133.284 | 25.968 | 0.351 | 80.769 |
| gnn_multiedge_season | post_covid | 39.485 | 101.150 | 26.154 | 0.497 | 80.769 |
| lstm | exclude_covid | 44.085 | 93.684 | 31.318 | 0.288 | 80.769 |
| gnn_corrbinary | post_covid | 45.674 | 130.521 | 33.940 | 0.368 | 73.077 |
| gnn_uniform | post_covid | 46.006 | 136.166 | 33.241 | 0.419 | 76.923 |
| gnn_multiedge | post_covid | 48.210 | 125.983 | 36.138 | 0.425 | 61.538 |
| arima | exclude_covid | 48.309 | 104.044 | 33.861 | 0.156 | 84.615 |
| dualtopo_fullhistory | full | 48.347 | 69.551 | 30.841 | -0.201 | 65.385 |
| gnn_multiedge_level | post_covid | 48.490 | 163.626 | 34.216 | 0.370 | 69.231 |
| gnn_multiedge_full | full | 49.678 | 136.160 | 34.518 | 0.348 | 73.077 |
| persistence | exclude_covid | 51.020 | 108.941 | 37.008 | 0.146 | 84.615 |
| persistence | post_covid | 51.020 | 108.941 | 37.008 | 0.146 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 53.909 | 148.506 | 39.542 | 0.314 | 69.231 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| gnn_multiedge_rt | post_covid | 56.012 | 157.442 | 39.688 | 0.174 | 69.231 |
| gnn_geo | post_covid | 72.991 | 183.166 | 49.474 | 0.165 | 84.615 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 5.736 | 48.426 | 4.549 | 0.497 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.639 | 98.591 | 6.656 | 0.230 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| persistence | exclude_covid | 8.487 | 81.409 | 6.191 | 0.463 | 100.000 |
| persistence | post_covid | 8.487 | 81.409 | 6.191 | 0.463 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.607 | 114.452 | 7.875 | 0.549 | 100.000 |
| lstm | post_covid | 10.745 | 131.937 | 8.947 | 0.484 | 100.000 |
| arima | exclude_covid | 10.944 | 114.098 | 8.560 | 0.314 | 100.000 |
| gnn_multiedge_season | post_covid | 12.614 | 103.390 | 9.097 | 0.567 | 100.000 |
| lstm | exclude_covid | 14.871 | 100.956 | 10.024 | 0.525 | 95.652 |
| arima | post_covid | 15.729 | 217.889 | 14.321 | 0.333 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.765 | 97.528 | 10.040 | 0.501 | 95.652 |
| gnn_multiedge_rt | post_covid | 20.200 | 139.251 | 11.781 | 0.182 | 91.304 |
| gnn_multiedge_full | full | 22.436 | 143.509 | 14.158 | 0.497 | 91.304 |
| dualtopo_no_bg | post_covid | 22.977 | 323.365 | 22.118 | 0.578 | 100.000 |
| dualtopo | post_covid | 23.529 | 331.063 | 22.663 | 0.577 | 100.000 |
| gnn_multiedge | post_covid | 36.776 | 193.209 | 20.906 | 0.506 | 78.261 |
| gnn_corrbinary | post_covid | 43.018 | 242.066 | 24.836 | 0.481 | 78.261 |
| gnn_multiedge_level | post_covid | 45.587 | 277.891 | 27.588 | 0.530 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 46.694 | 243.073 | 25.998 | 0.489 | 78.261 |
| gnn_uniform | post_covid | 57.905 | 302.369 | 32.078 | 0.476 | 78.261 |
| gnn_geo | post_covid | 60.464 | 279.360 | 32.105 | 0.480 | 78.261 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 17.843 | 109.176 | 12.598 | 0.682 | 94.286 |
| lstm | post_covid | 20.947 | 67.396 | 11.862 | 0.353 | 91.429 |
| dualtopo_no_bg | post_covid | 21.849 | 119.699 | 14.039 | 0.332 | 88.571 |
| dualtopo | post_covid | 21.905 | 122.202 | 14.198 | 0.363 | 88.571 |
| gnn_multiedge_covid_rsv | post_covid | 22.116 | 80.511 | 13.902 | 0.318 | 88.571 |
| gnn_multiedge_covid_rsv_full | full | 23.316 | 83.216 | 14.376 | 0.233 | 85.714 |
| arima | post_covid | 23.505 | 114.756 | 15.553 | -0.010 | 91.429 |
| gnn_multiedge_season_level | post_covid | 23.752 | 121.696 | 15.451 | 0.343 | 91.429 |
| arima | exclude_covid | 24.293 | 111.306 | 15.787 | -0.017 | 91.429 |
| lstm | exclude_covid | 24.293 | 87.415 | 14.557 | 0.182 | 91.429 |
| gnn_multiedge_season | post_covid | 26.945 | 116.030 | 15.298 | 0.265 | 91.429 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| gnn_multiedge_full | full | 29.390 | 142.973 | 18.773 | 0.268 | 85.714 |
| persistence | exclude_covid | 31.213 | 99.271 | 18.677 | -0.000 | 91.429 |
| persistence | post_covid | 31.213 | 99.271 | 18.677 | -0.000 | 91.429 |
| gnn_multiedge_rt | post_covid | 32.159 | 168.890 | 20.953 | 0.106 | 85.714 |
| gnn_multiedge | post_covid | 33.128 | 156.910 | 21.093 | 0.177 | 82.857 |
| gnn_multiedge_level | post_covid | 33.578 | 203.194 | 23.347 | 0.243 | 68.571 |
| gnn_corrbinary | post_covid | 33.851 | 183.457 | 23.605 | 0.118 | 80.000 |
| gnn_uniform | post_covid | 36.238 | 203.362 | 24.407 | 0.160 | 77.143 |
| gnn_multiedge_leaknorm | post_covid | 37.177 | 193.398 | 24.112 | 0.112 | 77.143 |
| gnn_geo | post_covid | 45.287 | 244.174 | 30.852 | 0.078 | 88.571 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 22.776 | 153.650 | 18.643 | 0.664 | 90.476 |
| lstm | post_covid | 26.297 | 66.720 | 16.280 | 0.334 | 85.714 |
| dualtopo | post_covid | 26.944 | 112.069 | 17.461 | 0.191 | 80.952 |
| dualtopo_no_bg | post_covid | 26.958 | 110.876 | 17.405 | 0.145 | 80.952 |
| gnn_multiedge_covid_rsv | post_covid | 28.049 | 93.076 | 19.558 | 0.244 | 80.952 |
| gnn_multiedge_covid_rsv_full | full | 29.503 | 102.084 | 20.157 | 0.118 | 80.952 |
| arima | post_covid | 29.511 | 116.756 | 21.007 | -0.111 | 85.714 |
| gnn_multiedge_season_level | post_covid | 29.668 | 151.875 | 21.005 | 0.209 | 85.714 |
| lstm | exclude_covid | 30.711 | 98.372 | 20.926 | 0.077 | 85.714 |
| arima | exclude_covid | 30.727 | 119.517 | 21.930 | -0.139 | 85.714 |
| gnn_multiedge_season | post_covid | 34.567 | 160.559 | 22.839 | 0.135 | 85.714 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| gnn_uniform | post_covid | 36.643 | 190.510 | 25.943 | 0.134 | 80.952 |
| gnn_multiedge_level | post_covid | 36.880 | 221.006 | 27.811 | 0.157 | 66.667 |
| gnn_multiedge_full | full | 36.935 | 182.697 | 26.384 | 0.135 | 76.190 |
| gnn_corrbinary | post_covid | 38.865 | 198.121 | 28.851 | 0.003 | 71.429 |
| gnn_multiedge | post_covid | 39.368 | 174.370 | 26.615 | 0.089 | 76.190 |
| persistence | exclude_covid | 40.062 | 138.038 | 28.448 | -0.136 | 85.714 |
| persistence | post_covid | 40.062 | 138.038 | 28.448 | -0.136 | 85.714 |
| gnn_multiedge_rt | post_covid | 40.316 | 216.315 | 29.522 | -0.052 | 76.190 |
| gnn_multiedge_leaknorm | post_covid | 42.420 | 208.425 | 28.955 | 0.015 | 76.190 |
| gnn_geo | post_covid | 50.159 | 267.436 | 36.934 | -0.051 | 80.952 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 4.220 | 42.465 | 3.530 | 0.611 | 100.000 |
| gnn_multiedge_season | post_covid | 4.772 | 49.237 | 3.985 | 0.637 | 100.000 |
| persistence | exclude_covid | 5.307 | 41.120 | 4.021 | 0.427 | 100.000 |
| persistence | post_covid | 5.307 | 41.120 | 4.021 | 0.427 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.532 | 61.663 | 5.416 | 0.174 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.311 | 54.914 | 5.706 | -0.187 | 92.857 |
| arima | exclude_covid | 7.690 | 98.989 | 6.573 | 0.164 | 100.000 |
| lstm | post_covid | 7.725 | 68.409 | 5.235 | 0.520 | 100.000 |
| lstm | exclude_covid | 7.788 | 70.978 | 5.004 | 0.452 | 100.000 |
| arima | post_covid | 8.650 | 111.756 | 7.371 | 0.024 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| gnn_multiedge_season_level | post_covid | 9.491 | 76.429 | 7.120 | 0.578 | 100.000 |
| dualtopo_no_bg | post_covid | 10.167 | 132.935 | 8.991 | 0.624 | 100.000 |
| dualtopo | post_covid | 10.518 | 137.402 | 9.303 | 0.623 | 100.000 |
| gnn_multiedge_full | full | 10.634 | 83.388 | 7.355 | 0.560 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.141 | 97.754 | 8.098 | 0.296 | 100.000 |
| gnn_multiedge | post_covid | 20.467 | 130.720 | 12.811 | 0.577 | 92.857 |
| gnn_corrbinary | post_covid | 24.475 | 161.462 | 15.735 | 0.578 | 92.857 |
| gnn_multiedge_leaknorm | post_covid | 27.498 | 170.859 | 16.848 | 0.579 | 78.571 |
| gnn_multiedge_level | post_covid | 27.902 | 176.475 | 16.651 | 0.555 | 71.429 |
| gnn_uniform | post_covid | 35.624 | 222.640 | 22.105 | 0.576 | 71.429 |
| gnn_geo | post_covid | 36.788 | 209.282 | 21.727 | 0.580 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 18.332 | 119.818 | 13.021 | 0.594 | 93.617 |
| gnn_multiedge_covid_rsv_full | full | 18.683 | 96.767 | 12.290 | 0.574 | 91.489 |
| gnn_multiedge_season | post_covid | 20.349 | 112.121 | 12.623 | 0.644 | 93.617 |
| arima | post_covid | 23.127 | 203.704 | 17.364 | 0.295 | 97.872 |
| arima | exclude_covid | 23.214 | 199.196 | 17.192 | 0.298 | 95.745 |
| lstm | post_covid | 23.750 | 137.136 | 15.080 | 0.417 | 93.617 |
| lstm | exclude_covid | 24.080 | 122.701 | 15.818 | 0.438 | 93.617 |
| dualtopo_fullhistory | full | 24.192 | 80.472 | 12.993 | 0.060 | 89.362 |
| gnn_multiedge_season_level | post_covid | 24.857 | 148.792 | 17.635 | 0.606 | 93.617 |
| dualtopo_no_bg | post_covid | 25.270 | 305.462 | 21.671 | 0.522 | 93.617 |
| dualtopo | post_covid | 25.510 | 311.319 | 21.967 | 0.537 | 93.617 |
| persistence | post_covid | 26.829 | 89.927 | 15.589 | 0.299 | 95.745 |
| persistence | exclude_covid | 26.829 | 89.927 | 15.589 | 0.299 | 93.617 |
| gnn_multiedge_full | full | 27.893 | 135.826 | 16.969 | 0.544 | 89.362 |
| gnn_multiedge_rt | post_covid | 32.958 | 166.263 | 20.447 | 0.330 | 87.234 |
| gnn_multiedge | post_covid | 33.488 | 178.131 | 21.338 | 0.411 | 78.723 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| gnn_corrbinary | post_covid | 36.782 | 212.206 | 22.718 | 0.323 | 80.851 |
| gnn_multiedge_leaknorm | post_covid | 41.873 | 225.548 | 25.545 | 0.284 | 76.596 |
| gnn_uniform | post_covid | 42.381 | 241.265 | 24.336 | 0.299 | 78.723 |
| gnn_multiedge_level | post_covid | 44.413 | 316.479 | 30.996 | 0.402 | 74.468 |
| gnn_geo | post_covid | 58.407 | 280.434 | 35.647 | 0.236 | 78.723 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 22.638 | 68.684 | 15.167 | 0.545 | 88.462 |
| gnn_multiedge_covid_rsv | post_covid | 22.749 | 71.476 | 16.863 | 0.627 | 88.462 |
| gnn_multiedge_covid_rsv_full | full | 24.329 | 69.479 | 17.530 | 0.487 | 84.615 |
| gnn_multiedge_season | post_covid | 25.440 | 89.435 | 16.322 | 0.575 | 88.462 |
| dualtopo_no_bg | post_covid | 26.730 | 149.971 | 20.581 | 0.381 | 88.462 |
| dualtopo | post_covid | 26.797 | 152.258 | 20.732 | 0.366 | 88.462 |
| arima | post_covid | 27.988 | 108.975 | 19.705 | 0.152 | 96.154 |
| arima | exclude_covid | 28.213 | 106.836 | 19.545 | 0.167 | 92.308 |
| lstm | exclude_covid | 28.639 | 80.705 | 19.987 | 0.380 | 88.462 |
| gnn_multiedge_season_level | post_covid | 29.833 | 136.614 | 23.126 | 0.519 | 88.462 |
| dualtopo_fullhistory | full | 32.213 | 68.476 | 20.015 | -0.178 | 80.769 |
| gnn_uniform | post_covid | 32.297 | 123.021 | 19.922 | 0.437 | 80.769 |
| gnn_multiedge_full | full | 33.540 | 106.284 | 21.105 | 0.471 | 84.615 |
| gnn_multiedge | post_covid | 33.668 | 120.711 | 23.144 | 0.446 | 80.769 |
| gnn_corrbinary | post_covid | 34.770 | 131.332 | 22.570 | 0.347 | 84.615 |
| persistence | exclude_covid | 35.530 | 79.440 | 24.042 | 0.158 | 88.462 |
| persistence | post_covid | 35.530 | 79.440 | 24.042 | 0.158 | 92.308 |
| gnn_multiedge_leaknorm | post_covid | 40.227 | 145.482 | 26.288 | 0.302 | 76.923 |
| gnn_multiedge_rt | post_covid | 40.952 | 159.774 | 28.026 | 0.192 | 84.615 |
| gnn_multiedge_level | post_covid | 43.683 | 214.021 | 32.274 | 0.402 | 73.077 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| gnn_geo | post_covid | 60.694 | 215.673 | 39.871 | 0.162 | 80.769 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 5.012 | 95.324 | 4.299 | 0.558 | 100.000 |
| persistence | exclude_covid | 6.931 | 102.911 | 5.124 | 0.348 | 100.000 |
| persistence | post_covid | 6.931 | 102.911 | 5.124 | 0.348 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.955 | 130.552 | 5.804 | -0.115 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.557 | 179.669 | 8.264 | 0.112 | 100.000 |
| gnn_multiedge_season | post_covid | 11.202 | 140.208 | 8.044 | 0.424 | 100.000 |
| arima | exclude_covid | 14.853 | 313.547 | 14.280 | 0.394 | 100.000 |
| arima | post_covid | 15.073 | 320.988 | 14.467 | 0.316 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.760 | 163.870 | 10.836 | 0.606 | 100.000 |
| lstm | exclude_covid | 16.802 | 174.695 | 10.656 | 0.504 | 100.000 |
| gnn_multiedge_full | full | 18.670 | 172.401 | 11.848 | 0.533 | 95.238 |
| gnn_multiedge_rt | post_covid | 18.833 | 174.298 | 11.064 | 0.194 | 90.476 |
| dualtopo_no_bg | post_covid | 23.337 | 497.975 | 23.020 | 0.573 | 100.000 |
| dualtopo | post_covid | 23.819 | 508.252 | 23.496 | 0.606 | 100.000 |
| lstm | post_covid | 25.059 | 221.888 | 14.972 | 0.515 | 100.000 |
| gnn_multiedge | post_covid | 33.265 | 249.222 | 19.102 | 0.503 | 76.190 |
| gnn_corrbinary | post_covid | 39.131 | 312.337 | 22.901 | 0.536 | 76.190 |
| gnn_multiedge_leaknorm | post_covid | 43.824 | 324.678 | 24.624 | 0.497 | 76.190 |
| gnn_multiedge_level | post_covid | 45.301 | 443.332 | 29.413 | 0.492 | 76.190 |
| gnn_uniform | post_covid | 52.236 | 387.662 | 29.802 | 0.562 | 76.190 |
| gnn_geo | post_covid | 55.444 | 360.614 | 30.417 | 0.561 | 76.190 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 16.024 | 111.942 | 10.778 | 0.615 | 89.130 |
| gnn_multiedge_covid_rsv_full | full | 17.620 | 87.617 | 10.330 | 0.513 | 93.478 |
| lstm | post_covid | 20.124 | 108.727 | 12.626 | 0.349 | 93.478 |
| gnn_multiedge_season | post_covid | 20.532 | 90.706 | 12.147 | 0.554 | 93.478 |
| arima | post_covid | 20.819 | 184.888 | 15.477 | 0.430 | 100.000 |
| dualtopo_no_bg | post_covid | 21.113 | 258.765 | 16.288 | 0.448 | 91.304 |
| dualtopo | post_covid | 21.266 | 264.400 | 16.527 | 0.448 | 91.304 |
| dualtopo_fullhistory | full | 21.920 | 65.668 | 11.427 | 0.110 | 89.130 |
| arima | exclude_covid | 22.315 | 262.679 | 17.561 | 0.166 | 97.826 |
| lstm | exclude_covid | 23.885 | 114.433 | 14.646 | 0.263 | 89.130 |
| gnn_multiedge_season_level | post_covid | 24.175 | 112.426 | 15.955 | 0.444 | 91.304 |
| gnn_multiedge_full | full | 26.290 | 133.641 | 16.522 | 0.420 | 89.130 |
| persistence | exclude_covid | 26.703 | 98.089 | 14.604 | 0.139 | 93.478 |
| persistence | post_covid | 26.703 | 98.089 | 14.604 | 0.139 | 95.652 |
| gnn_multiedge_rt | post_covid | 28.143 | 142.266 | 18.038 | 0.318 | 86.957 |
| gnn_multiedge | post_covid | 31.606 | 142.466 | 20.423 | 0.367 | 78.261 |
| gnn_corrbinary | post_covid | 32.385 | 169.564 | 20.928 | 0.332 | 76.087 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| gnn_multiedge_leaknorm | post_covid | 36.469 | 174.764 | 23.263 | 0.280 | 76.087 |
| gnn_uniform | post_covid | 38.373 | 196.534 | 23.446 | 0.311 | 80.435 |
| gnn_multiedge_level | post_covid | 38.885 | 248.295 | 26.206 | 0.317 | 71.739 |
| gnn_geo | post_covid | 50.259 | 217.622 | 29.982 | 0.233 | 86.957 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 20.839 | 104.091 | 15.168 | 0.573 | 80.000 |
| gnn_multiedge_covid_rsv_full | full | 23.297 | 85.188 | 15.106 | 0.382 | 88.000 |
| dualtopo_no_bg | post_covid | 24.251 | 113.902 | 16.520 | 0.215 | 84.000 |
| dualtopo | post_covid | 24.261 | 115.599 | 16.624 | 0.179 | 84.000 |
| lstm | post_covid | 24.430 | 75.549 | 15.449 | 0.307 | 88.000 |
| arima | post_covid | 26.554 | 176.847 | 20.871 | 0.168 | 100.000 |
| arima | exclude_covid | 26.589 | 145.334 | 19.532 | 0.064 | 96.000 |
| gnn_multiedge_season | post_covid | 26.708 | 104.233 | 17.541 | 0.437 | 88.000 |
| dualtopo_fullhistory | full | 29.567 | 77.180 | 18.947 | -0.167 | 80.000 |
| lstm | exclude_covid | 30.209 | 111.193 | 19.935 | 0.116 | 80.000 |
| gnn_multiedge_season_level | post_covid | 30.948 | 137.369 | 23.041 | 0.267 | 84.000 |
| gnn_corrbinary | post_covid | 31.179 | 132.956 | 22.323 | 0.319 | 76.000 |
| gnn_uniform | post_covid | 31.575 | 136.885 | 22.118 | 0.374 | 84.000 |
| gnn_multiedge_full | full | 32.700 | 155.456 | 22.393 | 0.271 | 80.000 |
| gnn_multiedge | post_covid | 33.904 | 137.327 | 24.227 | 0.327 | 76.000 |
| gnn_multiedge_rt | post_covid | 35.155 | 162.547 | 25.578 | 0.121 | 80.000 |
| persistence | exclude_covid | 35.800 | 137.533 | 23.732 | -0.070 | 88.000 |
| persistence | post_covid | 35.800 | 137.533 | 23.732 | -0.070 | 92.000 |
| gnn_multiedge_leaknorm | post_covid | 36.912 | 151.994 | 26.097 | 0.228 | 76.000 |
| gnn_multiedge_level | post_covid | 41.002 | 205.622 | 29.597 | 0.213 | 68.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| gnn_geo | post_covid | 51.997 | 206.103 | 33.469 | 0.129 | 88.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.424 | 51.963 | 2.474 | 0.679 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.825 | 90.508 | 4.645 | 0.272 | 100.000 |
| persistence | exclude_covid | 6.010 | 51.132 | 3.738 | 0.565 | 100.000 |
| persistence | post_covid | 6.010 | 51.132 | 3.738 | 0.565 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.745 | 121.287 | 5.551 | 0.622 | 100.000 |
| gnn_multiedge_season | post_covid | 8.617 | 74.603 | 5.726 | 0.712 | 100.000 |
| arima | post_covid | 10.487 | 194.461 | 9.057 | 0.777 | 100.000 |
| gnn_multiedge_season_level | post_covid | 11.833 | 82.732 | 7.519 | 0.741 | 100.000 |
| lstm | exclude_covid | 12.777 | 118.290 | 8.350 | 0.691 | 100.000 |
| lstm | post_covid | 13.288 | 148.225 | 9.265 | 0.698 | 100.000 |
| gnn_multiedge_full | full | 15.525 | 107.670 | 9.532 | 0.671 | 100.000 |
| arima | exclude_covid | 15.783 | 402.375 | 15.215 | 0.434 | 100.000 |
| gnn_multiedge_rt | post_covid | 16.237 | 118.123 | 9.061 | 0.548 | 95.238 |
| dualtopo_no_bg | post_covid | 16.622 | 431.221 | 16.012 | 0.602 | 100.000 |
| dualtopo | post_covid | 17.026 | 441.544 | 16.411 | 0.683 | 100.000 |
| gnn_multiedge | post_covid | 28.631 | 148.584 | 15.895 | 0.693 | 80.952 |
| gnn_corrbinary | post_covid | 33.764 | 213.145 | 19.267 | 0.692 | 76.190 |
| gnn_multiedge_leaknorm | post_covid | 35.935 | 201.872 | 19.888 | 0.691 | 76.190 |
| gnn_multiedge_level | post_covid | 36.203 | 299.097 | 22.169 | 0.697 | 76.190 |
| gnn_uniform | post_covid | 45.151 | 267.545 | 25.026 | 0.703 | 76.190 |
| gnn_geo | post_covid | 48.108 | 231.337 | 25.831 | 0.698 | 85.714 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 15.688 | 57.133 | 9.051 | 0.579 | 91.837 |
| gnn_multiedge_season_level | post_covid | 15.897 | 83.666 | 9.886 | 0.576 | 95.918 |
| lstm | post_covid | 16.278 | 98.743 | 9.825 | 0.456 | 93.878 |
| gnn_multiedge_season | post_covid | 16.294 | 96.018 | 10.826 | 0.583 | 97.959 |
| gnn_multiedge_covid_rsv | post_covid | 16.829 | 95.789 | 11.023 | 0.426 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 17.437 | 86.965 | 10.575 | 0.400 | 87.755 |
| dualtopo_no_bg | post_covid | 18.200 | 193.456 | 12.954 | 0.530 | 89.796 |
| dualtopo | post_covid | 18.274 | 196.879 | 13.103 | 0.534 | 89.796 |
| lstm | exclude_covid | 18.535 | 80.292 | 10.898 | 0.321 | 89.796 |
| arima | post_covid | 18.631 | 153.286 | 12.552 | 0.179 | 97.959 |
| arima | exclude_covid | 18.891 | 126.625 | 11.750 | 0.180 | 93.878 |
| gnn_multiedge_full | full | 22.424 | 123.257 | 13.454 | 0.387 | 89.796 |
| gnn_multiedge_rt | post_covid | 22.921 | 130.773 | 15.154 | 0.335 | 89.796 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| persistence | exclude_covid | 23.294 | 100.265 | 13.241 | 0.182 | 95.918 |
| persistence | post_covid | 23.294 | 100.265 | 13.241 | 0.182 | 95.918 |
| gnn_multiedge | post_covid | 24.562 | 145.823 | 16.626 | 0.372 | 87.755 |
| gnn_corrbinary | post_covid | 24.679 | 155.322 | 16.167 | 0.335 | 87.755 |
| gnn_multiedge_level | post_covid | 25.235 | 183.468 | 16.502 | 0.393 | 77.551 |
| gnn_multiedge_leaknorm | post_covid | 28.472 | 169.628 | 18.577 | 0.294 | 87.755 |
| gnn_uniform | post_covid | 28.513 | 177.766 | 17.734 | 0.323 | 85.714 |
| gnn_geo | post_covid | 34.532 | 193.186 | 21.673 | 0.247 | 97.959 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 20.268 | 79.027 | 14.542 | 0.484 | 96.154 |
| gnn_multiedge_season_level | post_covid | 20.402 | 71.246 | 14.057 | 0.451 | 92.308 |
| lstm | post_covid | 20.878 | 56.392 | 13.290 | 0.390 | 88.462 |
| dualtopo_fullhistory | full | 21.286 | 58.931 | 14.611 | 0.395 | 84.615 |
| gnn_multiedge_covid_rsv | post_covid | 22.010 | 82.339 | 16.384 | 0.339 | 84.615 |
| dualtopo | post_covid | 22.117 | 73.896 | 14.133 | 0.313 | 80.769 |
| dualtopo_no_bg | post_covid | 22.127 | 72.887 | 14.075 | 0.352 | 80.769 |
| gnn_uniform | post_covid | 22.943 | 98.805 | 17.307 | 0.410 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 23.370 | 80.598 | 16.191 | 0.221 | 76.923 |
| gnn_corrbinary | post_covid | 23.584 | 97.079 | 17.677 | 0.339 | 92.308 |
| arima | post_covid | 24.106 | 86.090 | 16.305 | -0.028 | 96.154 |
| lstm | exclude_covid | 24.545 | 71.375 | 16.517 | 0.190 | 80.769 |
| arima | exclude_covid | 25.003 | 82.023 | 16.486 | -0.031 | 88.462 |
| gnn_multiedge | post_covid | 25.951 | 105.932 | 19.853 | 0.343 | 92.308 |
| gnn_multiedge_level | post_covid | 26.313 | 111.991 | 18.157 | 0.334 | 73.077 |
| gnn_multiedge_full | full | 27.990 | 111.019 | 17.769 | 0.217 | 80.769 |
| gnn_multiedge_leaknorm | post_covid | 28.291 | 116.667 | 21.315 | 0.258 | 92.308 |
| gnn_multiedge_rt | post_covid | 28.719 | 120.432 | 21.255 | 0.146 | 84.615 |
| persistence | exclude_covid | 31.289 | 105.846 | 20.465 | -0.028 | 92.308 |
| persistence | post_covid | 31.289 | 105.846 | 20.465 | -0.028 | 92.308 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |
| gnn_geo | post_covid | 33.629 | 132.160 | 23.962 | 0.161 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.484 | 55.101 | 2.765 | 0.603 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.506 | 94.163 | 4.226 | 0.546 | 100.000 |
| persistence | exclude_covid | 7.022 | 93.955 | 5.074 | 0.587 | 100.000 |
| persistence | post_covid | 7.022 | 93.955 | 5.074 | 0.587 | 100.000 |
| lstm | exclude_covid | 7.135 | 90.371 | 4.546 | 0.595 | 100.000 |
| arima | exclude_covid | 7.321 | 177.045 | 6.396 | 0.598 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.468 | 110.994 | 4.962 | 0.547 | 100.000 |
| gnn_multiedge_season_level | post_covid | 8.237 | 97.706 | 5.172 | 0.619 | 100.000 |
| lstm | post_covid | 8.474 | 146.618 | 5.908 | 0.522 | 100.000 |
| arima | post_covid | 9.088 | 229.247 | 8.310 | 0.550 | 100.000 |
| gnn_multiedge_season | post_covid | 10.061 | 115.226 | 6.626 | 0.605 | 100.000 |
| dualtopo_no_bg | post_covid | 12.338 | 329.751 | 11.686 | 0.509 | 100.000 |
| dualtopo | post_covid | 12.587 | 335.902 | 11.939 | 0.621 | 100.000 |
| gnn_multiedge_full | full | 13.626 | 137.090 | 8.575 | 0.639 | 100.000 |
| gnn_multiedge_rt | post_covid | 13.669 | 142.463 | 8.257 | 0.351 | 95.652 |
| gnn_multiedge | post_covid | 22.892 | 190.917 | 12.977 | 0.598 | 82.609 |
| gnn_multiedge_level | post_covid | 23.958 | 264.269 | 14.630 | 0.605 | 82.609 |
| gnn_corrbinary | post_covid | 25.861 | 221.162 | 14.461 | 0.617 | 82.609 |
| gnn_multiedge_leaknorm | post_covid | 28.675 | 229.497 | 15.481 | 0.580 | 82.609 |
| gnn_uniform | post_covid | 33.720 | 267.027 | 18.216 | 0.617 | 78.261 |
| gnn_geo | post_covid | 35.525 | 262.172 | 19.085 | 0.615 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 17.406 | 53.717 | 8.743 | 0.476 | 92.500 |
| gnn_multiedge_season_level | post_covid | 17.993 | 88.456 | 11.678 | 0.449 | 97.500 |
| lstm | post_covid | 18.988 | 68.235 | 10.191 | 0.294 | 92.500 |
| dualtopo_no_bg | post_covid | 19.232 | 111.622 | 10.873 | 0.380 | 92.500 |
| dualtopo | post_covid | 19.257 | 114.010 | 11.001 | 0.389 | 92.500 |
| gnn_multiedge_covid_rsv_full | full | 19.810 | 79.283 | 11.032 | 0.262 | 92.500 |
| gnn_multiedge_covid_rsv | post_covid | 20.070 | 88.505 | 11.694 | 0.254 | 90.000 |
| arima | exclude_covid | 20.359 | 104.766 | 11.640 | 0.017 | 92.500 |
| gnn_multiedge_season | post_covid | 20.704 | 106.153 | 12.966 | 0.345 | 97.500 |
| lstm | exclude_covid | 20.819 | 80.843 | 11.990 | 0.209 | 90.000 |
| arima | post_covid | 21.123 | 100.582 | 11.888 | 0.013 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| gnn_multiedge_full | full | 24.638 | 133.055 | 15.123 | 0.294 | 92.500 |
| gnn_multiedge_rt | post_covid | 25.018 | 134.401 | 15.932 | 0.172 | 90.000 |
| gnn_multiedge_level | post_covid | 25.751 | 175.063 | 17.166 | 0.273 | 70.000 |
| persistence | exclude_covid | 26.974 | 90.487 | 14.475 | 0.032 | 95.000 |
| persistence | post_covid | 26.974 | 90.487 | 14.475 | 0.032 | 95.000 |
| gnn_multiedge | post_covid | 27.115 | 157.816 | 17.962 | 0.192 | 85.000 |
| gnn_corrbinary | post_covid | 27.449 | 170.798 | 18.336 | 0.151 | 90.000 |
| gnn_uniform | post_covid | 28.974 | 190.455 | 19.124 | 0.162 | 80.000 |
| gnn_multiedge_leaknorm | post_covid | 31.234 | 194.727 | 20.503 | 0.131 | 75.000 |
| gnn_geo | post_covid | 34.689 | 214.270 | 22.974 | 0.135 | 97.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 21.830 | 57.589 | 12.067 | 0.368 | 88.000 |
| gnn_multiedge_season_level | post_covid | 21.863 | 89.389 | 15.047 | 0.378 | 96.000 |
| dualtopo | post_covid | 23.422 | 79.877 | 12.938 | 0.274 | 88.000 |
| lstm | post_covid | 23.433 | 57.533 | 13.210 | 0.281 | 88.000 |
| dualtopo_no_bg | post_covid | 23.435 | 78.567 | 12.870 | 0.295 | 88.000 |
| gnn_multiedge_covid_rsv_full | full | 24.755 | 81.729 | 15.396 | 0.154 | 88.000 |
| gnn_multiedge_covid_rsv | post_covid | 24.984 | 88.763 | 15.994 | 0.181 | 84.000 |
| arima | exclude_covid | 25.174 | 85.637 | 15.004 | -0.091 | 88.000 |
| gnn_multiedge_season | post_covid | 25.559 | 113.214 | 17.556 | 0.242 | 96.000 |
| lstm | exclude_covid | 25.762 | 78.788 | 15.997 | 0.124 | 84.000 |
| arima | post_covid | 26.238 | 86.808 | 15.811 | -0.084 | 92.000 |
| gnn_multiedge_level | post_covid | 26.709 | 137.871 | 18.715 | 0.269 | 68.000 |
| gnn_uniform | post_covid | 28.171 | 135.455 | 19.744 | 0.177 | 84.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| gnn_multiedge_full | full | 29.579 | 128.429 | 19.048 | 0.210 | 88.000 |
| gnn_corrbinary | post_covid | 29.851 | 137.379 | 20.885 | 0.103 | 88.000 |
| gnn_multiedge | post_covid | 30.597 | 134.356 | 21.295 | 0.144 | 80.000 |
| gnn_multiedge_rt | post_covid | 30.620 | 145.839 | 21.738 | 0.038 | 84.000 |
| gnn_multiedge_leaknorm | post_covid | 33.355 | 157.362 | 23.081 | 0.083 | 72.000 |
| persistence | exclude_covid | 33.868 | 109.469 | 21.116 | -0.084 | 92.000 |
| persistence | post_covid | 33.868 | 109.469 | 21.116 | -0.084 | 92.000 |
| gnn_geo | post_covid | 36.387 | 173.407 | 25.656 | 0.083 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.698 | 47.263 | 3.203 | 0.332 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.016 | 75.206 | 3.759 | 0.131 | 100.000 |
| persistence | exclude_covid | 5.331 | 58.850 | 3.407 | 0.322 | 100.000 |
| persistence | post_covid | 5.331 | 58.850 | 3.407 | 0.322 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.812 | 88.075 | 4.526 | 0.077 | 100.000 |
| arima | post_covid | 6.513 | 123.540 | 5.351 | 0.309 | 100.000 |
| lstm | post_covid | 6.804 | 86.073 | 5.161 | 0.354 | 100.000 |
| arima | exclude_covid | 7.006 | 136.647 | 6.033 | 0.340 | 100.000 |
| lstm | exclude_covid | 7.051 | 84.268 | 5.312 | 0.328 | 100.000 |
| gnn_multiedge_season | post_covid | 7.372 | 94.384 | 5.315 | 0.320 | 100.000 |
| gnn_multiedge_season_level | post_covid | 8.167 | 86.902 | 6.064 | 0.312 | 100.000 |
| dualtopo_no_bg | post_covid | 8.426 | 166.713 | 7.545 | 0.193 | 100.000 |
| dualtopo | post_covid | 8.636 | 170.896 | 7.774 | 0.251 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.321 | 115.337 | 6.255 | 0.203 | 100.000 |
| gnn_multiedge_full | full | 12.673 | 140.765 | 8.581 | 0.305 | 100.000 |
| gnn_multiedge | post_covid | 20.007 | 196.917 | 12.408 | 0.291 | 93.333 |
| gnn_corrbinary | post_covid | 22.892 | 226.496 | 14.090 | 0.285 | 93.333 |
| gnn_multiedge_level | post_covid | 24.070 | 237.050 | 14.585 | 0.279 | 73.333 |
| gnn_multiedge_leaknorm | post_covid | 27.334 | 257.003 | 16.206 | 0.285 | 80.000 |
| gnn_uniform | post_covid | 30.265 | 282.123 | 18.090 | 0.311 | 73.333 |
| gnn_geo | post_covid | 31.658 | 282.374 | 18.504 | 0.282 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 11.677 | 105.575 | 8.143 | 0.502 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 12.301 | 91.424 | 7.982 | 0.446 | 92.857 |
| lstm | post_covid | 12.315 | 62.190 | 7.184 | 0.456 | 92.857 |
| gnn_multiedge_season_level | post_covid | 12.442 | 91.236 | 8.389 | 0.563 | 95.238 |
| arima | post_covid | 13.027 | 156.570 | 9.031 | 0.218 | 100.000 |
| dualtopo_no_bg | post_covid | 13.147 | 186.738 | 9.459 | 0.512 | 90.476 |
| dualtopo | post_covid | 13.208 | 191.080 | 9.585 | 0.531 | 90.476 |
| gnn_multiedge_season | post_covid | 13.290 | 98.471 | 8.220 | 0.546 | 97.619 |
| dualtopo_fullhistory | full | 14.764 | 49.974 | 7.838 | 0.100 | 85.714 |
| arima | exclude_covid | 15.001 | 149.222 | 10.432 | 0.133 | 95.238 |
| lstm | exclude_covid | 15.199 | 95.601 | 9.743 | 0.342 | 90.476 |
| persistence | post_covid | 16.752 | 92.696 | 10.148 | 0.194 | 95.238 |
| persistence | exclude_covid | 16.752 | 92.696 | 10.148 | 0.194 | 95.238 |
| gnn_multiedge_full | full | 17.616 | 133.007 | 11.393 | 0.442 | 92.857 |
| gnn_multiedge_rt | post_covid | 18.042 | 130.841 | 11.703 | 0.326 | 92.857 |
| gnn_multiedge | post_covid | 19.001 | 146.761 | 12.836 | 0.367 | 92.857 |
| gnn_corrbinary | post_covid | 19.193 | 167.460 | 12.863 | 0.311 | 90.476 |
| gnn_multiedge_level | post_covid | 20.025 | 183.694 | 13.541 | 0.399 | 73.810 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |
| gnn_uniform | post_covid | 22.331 | 194.913 | 13.858 | 0.296 | 88.095 |
| gnn_multiedge_leaknorm | post_covid | 22.965 | 183.492 | 14.881 | 0.270 | 88.095 |
| gnn_geo | post_covid | 29.291 | 220.740 | 18.846 | 0.200 | 95.238 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 14.516 | 101.174 | 10.960 | 0.506 | 92.000 |
| gnn_multiedge_season_level | post_covid | 15.006 | 89.040 | 10.870 | 0.470 | 92.000 |
| dualtopo | post_covid | 15.458 | 139.749 | 10.360 | 0.388 | 84.000 |
| dualtopo_no_bg | post_covid | 15.465 | 137.244 | 10.319 | 0.406 | 84.000 |
| gnn_multiedge_covid_rsv_full | full | 15.500 | 85.743 | 10.865 | 0.351 | 88.000 |
| lstm | post_covid | 15.684 | 62.863 | 10.228 | 0.347 | 88.000 |
| arima | post_covid | 15.796 | 121.267 | 10.652 | 0.088 | 100.000 |
| gnn_multiedge_season | post_covid | 16.173 | 91.916 | 10.460 | 0.470 | 96.000 |
| gnn_corrbinary | post_covid | 18.395 | 113.688 | 13.529 | 0.337 | 92.000 |
| arima | exclude_covid | 18.487 | 119.726 | 13.074 | 0.024 | 92.000 |
| gnn_uniform | post_covid | 18.760 | 120.626 | 12.959 | 0.387 | 96.000 |
| dualtopo_fullhistory | full | 18.974 | 51.157 | 11.572 | -0.095 | 76.000 |
| lstm | exclude_covid | 19.233 | 108.085 | 13.962 | 0.213 | 88.000 |
| gnn_multiedge | post_covid | 20.005 | 113.011 | 14.709 | 0.367 | 92.000 |
| gnn_multiedge_level | post_covid | 20.234 | 143.547 | 14.857 | 0.374 | 72.000 |
| gnn_multiedge_full | full | 20.768 | 120.306 | 14.217 | 0.355 | 88.000 |
| persistence | exclude_covid | 21.275 | 99.728 | 14.764 | 0.050 | 92.000 |
| persistence | post_covid | 21.275 | 99.728 | 14.764 | 0.050 | 92.000 |
| gnn_multiedge_rt | post_covid | 22.245 | 137.038 | 16.174 | 0.181 | 88.000 |
| gnn_multiedge_leaknorm | post_covid | 22.783 | 129.882 | 15.986 | 0.271 | 88.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |
| gnn_geo | post_covid | 30.147 | 169.903 | 21.252 | 0.128 | 92.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.018 | 48.234 | 2.346 | 0.315 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| lstm | post_covid | 3.597 | 61.201 | 2.707 | 0.474 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.532 | 99.778 | 3.741 | 0.150 | 100.000 |
| lstm | exclude_covid | 5.170 | 77.241 | 3.538 | 0.546 | 94.118 |
| gnn_multiedge_covid_rsv | post_covid | 5.194 | 112.047 | 4.001 | 0.367 | 100.000 |
| persistence | exclude_covid | 5.262 | 82.356 | 3.359 | 0.298 | 100.000 |
| persistence | post_covid | 5.262 | 82.356 | 3.359 | 0.298 | 100.000 |
| gnn_multiedge_season_level | post_covid | 7.163 | 94.466 | 4.740 | 0.398 | 100.000 |
| gnn_multiedge_season | post_covid | 7.193 | 108.111 | 4.925 | 0.454 | 100.000 |
| arima | post_covid | 7.234 | 208.486 | 6.648 | 0.316 | 100.000 |
| arima | exclude_covid | 7.306 | 192.598 | 6.548 | 0.036 | 100.000 |
| dualtopo_no_bg | post_covid | 8.678 | 259.524 | 8.193 | 0.222 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.745 | 121.728 | 5.129 | 0.215 | 100.000 |
| dualtopo | post_covid | 8.920 | 266.568 | 8.446 | 0.316 | 100.000 |
| gnn_multiedge_full | full | 11.509 | 151.685 | 7.240 | 0.394 | 100.000 |
| gnn_multiedge | post_covid | 17.420 | 196.394 | 10.082 | 0.417 | 94.118 |
| gnn_multiedge_level | post_covid | 19.714 | 242.734 | 11.604 | 0.437 | 76.471 |
| gnn_corrbinary | post_covid | 20.310 | 246.537 | 11.883 | 0.380 | 88.235 |
| gnn_multiedge_leaknorm | post_covid | 23.231 | 262.330 | 13.257 | 0.408 | 88.235 |
| gnn_uniform | post_covid | 26.730 | 304.158 | 15.180 | 0.399 | 76.471 |
| gnn_geo | post_covid | 27.985 | 295.500 | 15.309 | 0.381 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 9.235 | 69.602 | 5.778 | 0.678 | 95.652 |
| gnn_multiedge_season | post_covid | 10.477 | 88.719 | 7.394 | 0.660 | 100.000 |
| gnn_multiedge_season_level | post_covid | 10.525 | 65.167 | 6.779 | 0.628 | 97.826 |
| lstm | post_covid | 11.462 | 90.915 | 7.188 | 0.450 | 95.652 |
| gnn_multiedge_covid_rsv | post_covid | 11.469 | 90.669 | 7.698 | 0.478 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 11.567 | 87.045 | 7.026 | 0.467 | 93.478 |
| arima | post_covid | 12.069 | 152.906 | 8.106 | 0.288 | 100.000 |
| dualtopo_no_bg | post_covid | 12.357 | 191.036 | 8.437 | 0.579 | 93.478 |
| dualtopo | post_covid | 12.407 | 194.959 | 8.534 | 0.587 | 93.478 |
| lstm | exclude_covid | 12.988 | 99.728 | 8.638 | 0.376 | 97.826 |
| arima | exclude_covid | 13.855 | 134.056 | 9.106 | 0.260 | 97.826 |
| persistence | post_covid | 14.883 | 86.512 | 8.693 | 0.294 | 97.826 |
| persistence | exclude_covid | 14.883 | 86.512 | 8.693 | 0.294 | 97.826 |
| gnn_multiedge_rt | post_covid | 15.464 | 122.015 | 10.195 | 0.441 | 97.826 |
| gnn_multiedge_full | full | 16.340 | 126.025 | 11.006 | 0.442 | 95.652 |
| gnn_multiedge | post_covid | 16.981 | 133.188 | 11.691 | 0.451 | 97.826 |
| gnn_corrbinary | post_covid | 17.786 | 151.705 | 11.874 | 0.393 | 97.826 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| gnn_multiedge_level | post_covid | 18.500 | 170.923 | 12.173 | 0.435 | 82.609 |
| gnn_multiedge_leaknorm | post_covid | 20.484 | 162.454 | 13.384 | 0.377 | 93.478 |
| gnn_uniform | post_covid | 20.684 | 172.679 | 12.986 | 0.377 | 91.304 |
| gnn_geo | post_covid | 26.742 | 200.055 | 16.701 | 0.278 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 12.080 | 65.431 | 8.490 | 0.532 | 92.308 |
| gnn_multiedge_season | post_covid | 12.768 | 75.283 | 9.785 | 0.556 | 100.000 |
| gnn_multiedge_season_level | post_covid | 13.080 | 60.548 | 9.124 | 0.511 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 14.750 | 69.423 | 10.811 | 0.388 | 96.154 |
| dualtopo | post_covid | 14.770 | 80.592 | 9.141 | 0.383 | 88.462 |
| dualtopo_no_bg | post_covid | 14.777 | 79.446 | 9.116 | 0.412 | 88.462 |
| lstm | post_covid | 14.890 | 66.119 | 10.272 | 0.359 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 15.024 | 74.849 | 9.996 | 0.286 | 88.462 |
| arima | post_covid | 15.087 | 82.117 | 10.013 | 0.078 | 100.000 |
| gnn_uniform | post_covid | 15.328 | 93.904 | 11.541 | 0.485 | 100.000 |
| gnn_corrbinary | post_covid | 16.354 | 96.186 | 12.170 | 0.382 | 100.000 |
| lstm | exclude_covid | 16.750 | 86.853 | 12.572 | 0.235 | 96.154 |
| gnn_multiedge | post_covid | 16.800 | 90.759 | 12.850 | 0.432 | 100.000 |
| arima | exclude_covid | 17.602 | 86.768 | 12.125 | 0.082 | 96.154 |
| gnn_multiedge_level | post_covid | 17.892 | 97.312 | 12.536 | 0.406 | 84.615 |
| gnn_multiedge_rt | post_covid | 18.991 | 110.417 | 13.715 | 0.245 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 19.173 | 103.824 | 13.892 | 0.362 | 96.154 |
| persistence | exclude_covid | 19.370 | 88.209 | 12.823 | 0.078 | 96.154 |
| persistence | post_covid | 19.370 | 88.209 | 12.823 | 0.078 | 96.154 |
| gnn_multiedge_full | full | 19.602 | 112.962 | 14.218 | 0.271 | 92.308 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| gnn_geo | post_covid | 26.217 | 154.506 | 17.715 | 0.178 | 100.000 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.540 | 75.024 | 2.252 | 0.641 | 100.000 |
| lstm | post_covid | 3.732 | 123.151 | 3.178 | 0.752 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.784 | 102.900 | 3.165 | 0.386 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.441 | 118.289 | 3.650 | 0.316 | 100.000 |
| persistence | exclude_covid | 4.660 | 84.306 | 3.325 | 0.557 | 100.000 |
| persistence | post_covid | 4.660 | 84.306 | 3.325 | 0.557 | 100.000 |
| lstm | exclude_covid | 4.818 | 116.466 | 3.524 | 0.652 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.691 | 71.173 | 3.730 | 0.747 | 100.000 |
| arima | exclude_covid | 6.220 | 195.531 | 5.181 | 0.270 | 100.000 |
| arima | post_covid | 6.252 | 244.932 | 5.626 | 0.543 | 100.000 |
| gnn_multiedge_season | post_covid | 6.367 | 106.187 | 4.285 | 0.630 | 100.000 |
| dualtopo_no_bg | post_covid | 8.206 | 336.104 | 7.555 | 0.583 | 100.000 |
| dualtopo | post_covid | 8.395 | 343.636 | 7.746 | 0.679 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.008 | 137.092 | 5.620 | 0.589 | 100.000 |
| gnn_multiedge_full | full | 10.703 | 143.008 | 6.830 | 0.640 | 100.000 |
| gnn_multiedge | post_covid | 17.213 | 188.347 | 10.184 | 0.665 | 95.000 |
| gnn_multiedge_level | post_covid | 19.262 | 266.618 | 11.702 | 0.656 | 80.000 |
| gnn_corrbinary | post_covid | 19.491 | 223.880 | 11.490 | 0.674 | 95.000 |
| gnn_multiedge_leaknorm | post_covid | 22.071 | 238.674 | 12.723 | 0.666 | 90.000 |
| gnn_uniform | post_covid | 26.049 | 275.087 | 14.864 | 0.706 | 80.000 |
| gnn_geo | post_covid | 27.409 | 259.268 | 15.383 | 0.683 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 8.128 | 92.390 | 5.749 | 0.808 | 97.727 |
| lstm | post_covid | 11.196 | 95.804 | 6.979 | 0.513 | 93.182 |
| gnn_multiedge_covid_rsv | post_covid | 11.924 | 121.441 | 7.990 | 0.457 | 93.182 |
| gnn_multiedge_season_level | post_covid | 12.208 | 114.722 | 8.517 | 0.573 | 95.455 |
| gnn_multiedge_covid_rsv_full | full | 12.616 | 106.016 | 7.686 | 0.383 | 90.909 |
| arima | post_covid | 12.838 | 182.436 | 9.034 | 0.232 | 97.727 |
| dualtopo_no_bg | post_covid | 12.921 | 212.791 | 9.405 | 0.472 | 90.909 |
| lstm | exclude_covid | 12.961 | 82.388 | 8.322 | 0.399 | 93.182 |
| dualtopo | post_covid | 12.980 | 216.785 | 9.506 | 0.504 | 90.909 |
| gnn_multiedge_season | post_covid | 13.023 | 129.935 | 8.986 | 0.527 | 97.727 |
| arima | exclude_covid | 15.246 | 124.799 | 9.087 | 0.250 | 97.727 |
| persistence | post_covid | 16.423 | 109.120 | 9.911 | 0.204 | 95.455 |
| persistence | exclude_covid | 16.423 | 109.120 | 9.911 | 0.204 | 95.455 |
| gnn_multiedge_full | full | 16.459 | 163.907 | 11.008 | 0.413 | 97.727 |
| gnn_multiedge_rt | post_covid | 18.371 | 160.039 | 11.566 | 0.283 | 93.182 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| gnn_multiedge | post_covid | 18.989 | 163.223 | 13.327 | 0.369 | 97.727 |
| gnn_corrbinary | post_covid | 20.421 | 208.053 | 14.104 | 0.275 | 90.909 |
| gnn_multiedge_level | post_covid | 21.260 | 231.788 | 15.018 | 0.387 | 75.000 |
| gnn_multiedge_leaknorm | post_covid | 22.642 | 199.468 | 15.549 | 0.277 | 86.364 |
| gnn_uniform | post_covid | 22.981 | 227.233 | 15.516 | 0.291 | 90.909 |
| gnn_geo | post_covid | 31.783 | 290.494 | 21.035 | 0.182 | 95.455 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 10.485 | 102.026 | 8.374 | 0.756 | 96.000 |
| lstm | post_covid | 14.160 | 82.425 | 9.237 | 0.468 | 88.000 |
| gnn_multiedge_season_level | post_covid | 15.140 | 139.803 | 11.646 | 0.453 | 92.000 |
| dualtopo | post_covid | 15.347 | 136.608 | 10.303 | 0.274 | 84.000 |
| dualtopo_no_bg | post_covid | 15.357 | 135.324 | 10.287 | 0.256 | 84.000 |
| gnn_multiedge_covid_rsv | post_covid | 15.406 | 121.376 | 11.636 | 0.393 | 88.000 |
| arima | post_covid | 15.830 | 128.596 | 10.922 | 0.081 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 16.369 | 107.094 | 11.151 | 0.216 | 84.000 |
| lstm | exclude_covid | 16.434 | 83.302 | 11.701 | 0.296 | 88.000 |
| gnn_multiedge_season | post_covid | 16.550 | 147.393 | 12.851 | 0.397 | 96.000 |
| gnn_uniform | post_covid | 18.897 | 188.985 | 15.281 | 0.339 | 100.000 |
| arima | exclude_covid | 19.737 | 114.583 | 13.264 | 0.082 | 96.000 |
| gnn_multiedge | post_covid | 20.241 | 146.551 | 15.582 | 0.320 | 96.000 |
| gnn_multiedge_full | full | 20.269 | 189.419 | 14.833 | 0.255 | 96.000 |
| gnn_corrbinary | post_covid | 20.449 | 193.532 | 15.637 | 0.208 | 92.000 |
| gnn_multiedge_level | post_covid | 21.315 | 215.106 | 16.490 | 0.330 | 76.000 |
| persistence | exclude_covid | 21.444 | 122.153 | 15.148 | 0.019 | 92.000 |
| persistence | post_covid | 21.444 | 122.153 | 15.148 | 0.019 | 92.000 |
| gnn_multiedge_leaknorm | post_covid | 22.977 | 175.627 | 17.494 | 0.216 | 84.000 |
| gnn_multiedge_rt | post_covid | 23.134 | 181.295 | 16.353 | 0.086 | 88.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |
| gnn_geo | post_covid | 33.824 | 305.985 | 24.545 | 0.024 | 92.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.891 | 79.712 | 2.294 | 0.512 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.004 | 104.597 | 3.127 | 0.391 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.116 | 121.526 | 3.193 | 0.405 | 100.000 |
| persistence | exclude_covid | 4.418 | 91.972 | 3.021 | 0.555 | 100.000 |
| persistence | post_covid | 4.418 | 91.972 | 3.021 | 0.555 | 100.000 |
| arima | exclude_covid | 5.067 | 138.241 | 3.590 | 0.478 | 100.000 |
| lstm | post_covid | 5.146 | 113.409 | 4.007 | 0.702 | 100.000 |
| gnn_multiedge_season | post_covid | 5.688 | 106.964 | 3.900 | 0.698 | 100.000 |
| lstm | exclude_covid | 5.800 | 81.185 | 3.876 | 0.724 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.600 | 81.720 | 4.400 | 0.681 | 100.000 |
| arima | post_covid | 7.207 | 253.279 | 6.550 | 0.415 | 100.000 |
| dualtopo_no_bg | post_covid | 8.737 | 314.720 | 8.244 | 0.501 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.797 | 132.071 | 5.267 | 0.575 | 100.000 |
| dualtopo | post_covid | 8.959 | 322.281 | 8.459 | 0.621 | 100.000 |
| gnn_multiedge_full | full | 9.313 | 130.339 | 5.974 | 0.701 | 100.000 |
| gnn_multiedge | post_covid | 17.203 | 185.161 | 10.359 | 0.721 | 100.000 |
| gnn_corrbinary | post_covid | 20.385 | 227.160 | 12.085 | 0.699 | 89.474 |
| gnn_multiedge_level | post_covid | 21.188 | 253.737 | 13.081 | 0.702 | 73.684 |
| gnn_multiedge_leaknorm | post_covid | 22.194 | 230.838 | 12.990 | 0.714 | 89.474 |
| gnn_uniform | post_covid | 27.444 | 277.560 | 15.825 | 0.715 | 78.947 |
| gnn_geo | post_covid | 28.877 | 270.112 | 16.417 | 0.695 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 11.355 | 97.999 | 7.517 | 0.575 | 97.826 |
| lstm | post_covid | 11.950 | 109.443 | 7.430 | 0.499 | 95.652 |
| gnn_multiedge_season | post_covid | 12.129 | 99.896 | 7.692 | 0.594 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 12.444 | 87.047 | 7.575 | 0.486 | 93.478 |
| gnn_multiedge_season_level | post_covid | 12.634 | 116.420 | 8.348 | 0.519 | 97.826 |
| lstm | exclude_covid | 13.530 | 114.069 | 8.704 | 0.378 | 95.652 |
| arima | post_covid | 13.571 | 178.821 | 9.415 | 0.243 | 100.000 |
| dualtopo_no_bg | post_covid | 13.835 | 227.946 | 9.939 | 0.500 | 91.304 |
| dualtopo | post_covid | 13.890 | 232.141 | 10.045 | 0.503 | 91.304 |
| dualtopo_fullhistory | full | 14.779 | 77.037 | 7.494 | 0.025 | 86.957 |
| arima | exclude_covid | 16.067 | 102.842 | 9.218 | 0.258 | 95.652 |
| gnn_multiedge_full | full | 16.548 | 127.027 | 10.278 | 0.452 | 95.652 |
| persistence | exclude_covid | 17.016 | 89.321 | 9.226 | 0.245 | 97.826 |
| persistence | post_covid | 17.016 | 89.321 | 9.226 | 0.245 | 97.826 |
| gnn_multiedge_rt | post_covid | 17.140 | 145.210 | 11.044 | 0.340 | 93.478 |
| gnn_multiedge | post_covid | 17.278 | 143.029 | 11.619 | 0.417 | 95.652 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| gnn_corrbinary | post_covid | 18.061 | 165.086 | 12.105 | 0.350 | 95.652 |
| gnn_multiedge_level | post_covid | 18.987 | 223.889 | 12.906 | 0.358 | 80.435 |
| gnn_uniform | post_covid | 19.852 | 184.821 | 12.882 | 0.359 | 93.478 |
| gnn_multiedge_leaknorm | post_covid | 20.435 | 180.884 | 13.626 | 0.329 | 93.478 |
| gnn_geo | post_covid | 24.704 | 205.719 | 15.832 | 0.248 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 15.387 | 102.239 | 11.955 | 0.494 | 95.833 |
| lstm | post_covid | 15.606 | 93.677 | 10.251 | 0.450 | 91.667 |
| gnn_multiedge_season | post_covid | 16.279 | 120.539 | 11.980 | 0.473 | 95.833 |
| gnn_multiedge_season_level | post_covid | 16.599 | 140.131 | 12.558 | 0.364 | 95.833 |
| gnn_multiedge_covid_rsv_full | full | 17.051 | 95.498 | 12.726 | 0.348 | 87.500 |
| dualtopo | post_covid | 17.131 | 140.150 | 11.227 | 0.253 | 83.333 |
| dualtopo_no_bg | post_covid | 17.140 | 138.473 | 11.200 | 0.286 | 83.333 |
| arima | post_covid | 17.756 | 129.108 | 12.397 | 0.061 | 100.000 |
| lstm | exclude_covid | 17.907 | 113.864 | 12.742 | 0.243 | 91.667 |
| gnn_uniform | post_covid | 18.467 | 153.693 | 13.985 | 0.388 | 100.000 |
| gnn_corrbinary | post_covid | 19.957 | 159.000 | 15.104 | 0.274 | 91.667 |
| gnn_multiedge | post_covid | 20.238 | 152.552 | 15.503 | 0.349 | 91.667 |
| dualtopo_fullhistory | full | 20.370 | 86.202 | 12.761 | -0.275 | 75.000 |
| gnn_multiedge_level | post_covid | 20.746 | 205.823 | 14.785 | 0.250 | 83.333 |
| gnn_multiedge_full | full | 21.582 | 145.211 | 15.159 | 0.304 | 91.667 |
| arima | exclude_covid | 22.028 | 132.199 | 15.807 | 0.069 | 91.667 |
| gnn_multiedge_leaknorm | post_covid | 22.251 | 180.485 | 16.980 | 0.262 | 87.500 |
| gnn_multiedge_rt | post_covid | 22.831 | 186.642 | 17.380 | 0.134 | 87.500 |
| persistence | exclude_covid | 23.432 | 119.879 | 16.054 | 0.066 | 95.833 |
| persistence | post_covid | 23.432 | 119.879 | 16.054 | 0.066 | 95.833 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| gnn_geo | post_covid | 26.473 | 209.532 | 19.436 | 0.135 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.006 | 67.039 | 1.747 | 0.758 | 100.000 |
| persistence | exclude_covid | 2.537 | 55.985 | 1.777 | 0.765 | 100.000 |
| persistence | post_covid | 2.537 | 55.985 | 1.777 | 0.765 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 2.574 | 77.827 | 1.956 | 0.532 | 100.000 |
| arima | exclude_covid | 3.226 | 70.817 | 2.029 | 0.648 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 3.365 | 93.373 | 2.676 | 0.679 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gnn_multiedge_season | post_covid | 4.300 | 77.376 | 3.015 | 0.809 | 100.000 |
| lstm | post_covid | 5.735 | 126.643 | 4.354 | 0.714 | 100.000 |
| lstm | exclude_covid | 5.739 | 114.293 | 4.298 | 0.782 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.757 | 90.554 | 3.756 | 0.742 | 100.000 |
| arima | post_covid | 6.414 | 233.053 | 6.161 | 0.757 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.752 | 100.011 | 4.132 | 0.669 | 100.000 |
| gnn_multiedge_full | full | 8.026 | 107.189 | 4.955 | 0.799 | 100.000 |
| dualtopo_no_bg | post_covid | 8.929 | 325.553 | 8.563 | 0.694 | 100.000 |
| dualtopo | post_covid | 9.125 | 332.495 | 8.756 | 0.747 | 100.000 |
| gnn_multiedge | post_covid | 13.318 | 132.641 | 7.382 | 0.811 | 100.000 |
| gnn_corrbinary | post_covid | 15.733 | 171.726 | 8.832 | 0.786 | 100.000 |
| gnn_multiedge_level | post_covid | 16.859 | 243.598 | 10.857 | 0.808 | 77.273 |
| gnn_multiedge_leaknorm | post_covid | 18.250 | 181.320 | 9.968 | 0.801 | 100.000 |
| gnn_uniform | post_covid | 21.260 | 218.778 | 11.679 | 0.770 | 86.364 |
| gnn_geo | post_covid | 22.618 | 201.560 | 11.900 | 0.762 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 4.594 | 63.827 | 3.232 | 0.619 | 97.674 |
| lstm | post_covid | 4.853 | 94.308 | 3.582 | 0.508 | 100.000 |
| arima | exclude_covid | 4.960 | 133.207 | 4.073 | 0.503 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.040 | 79.605 | 3.822 | 0.540 | 100.000 |
| arima | post_covid | 5.215 | 151.510 | 4.376 | 0.498 | 100.000 |
| persistence | exclude_covid | 5.380 | 75.246 | 3.819 | 0.511 | 100.000 |
| persistence | post_covid | 5.380 | 75.246 | 3.819 | 0.511 | 100.000 |
| dualtopo_fullhistory | full | 5.429 | 63.469 | 3.309 | 0.348 | 88.372 |
| dualtopo_no_bg | post_covid | 5.710 | 174.098 | 4.914 | 0.680 | 100.000 |
| dualtopo | post_covid | 5.775 | 177.489 | 4.978 | 0.710 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.440 | 116.254 | 4.644 | 0.571 | 100.000 |
| lstm | exclude_covid | 6.445 | 104.407 | 4.507 | 0.382 | 100.000 |
| gnn_multiedge_season | post_covid | 6.631 | 103.084 | 4.812 | 0.568 | 100.000 |
| gnn_multiedge_full | full | 8.550 | 139.271 | 6.379 | 0.581 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.553 | 131.456 | 5.864 | 0.487 | 100.000 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| gnn_multiedge | post_covid | 10.002 | 176.372 | 6.484 | 0.379 | 100.000 |
| gnn_corrbinary | post_covid | 10.566 | 194.609 | 6.847 | 0.347 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 12.111 | 215.197 | 7.448 | 0.303 | 100.000 |
| gnn_multiedge_level | post_covid | 12.133 | 249.404 | 8.475 | 0.396 | 90.698 |
| gnn_uniform | post_covid | 12.994 | 247.049 | 8.106 | 0.236 | 100.000 |
| gnn_geo | post_covid | 14.940 | 253.400 | 9.460 | 0.300 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 5.125 | 63.959 | 3.904 | 0.362 | 100.000 |
| arima | exclude_covid | 5.143 | 57.530 | 3.901 | 0.355 | 100.000 |
| dualtopo_no_bg | post_covid | 5.459 | 75.886 | 4.305 | 0.585 | 100.000 |
| dualtopo | post_covid | 5.467 | 76.964 | 4.321 | 0.580 | 100.000 |
| lstm | post_covid | 5.674 | 51.529 | 4.108 | 0.369 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.729 | 43.942 | 4.243 | 0.535 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.188 | 53.544 | 4.953 | 0.568 | 100.000 |
| persistence | exclude_covid | 6.567 | 50.458 | 5.028 | 0.365 | 100.000 |
| persistence | post_covid | 6.567 | 50.458 | 5.028 | 0.365 | 100.000 |
| dualtopo_fullhistory | full | 6.906 | 41.050 | 4.438 | 0.104 | 80.000 |
| gnn_multiedge_season_level | post_covid | 7.230 | 70.978 | 5.555 | 0.451 | 100.000 |
| lstm | exclude_covid | 7.731 | 63.289 | 5.631 | 0.251 | 100.000 |
| gnn_multiedge_season | post_covid | 7.897 | 67.893 | 6.207 | 0.484 | 100.000 |
| gnn_corrbinary | post_covid | 8.850 | 71.922 | 6.327 | 0.437 | 100.000 |
| gnn_multiedge | post_covid | 9.009 | 68.690 | 6.303 | 0.464 | 100.000 |
| gnn_multiedge_full | full | 9.273 | 75.239 | 7.509 | 0.549 | 100.000 |
| gnn_uniform | post_covid | 9.507 | 83.143 | 6.860 | 0.411 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.552 | 78.355 | 7.140 | 0.417 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.419 | 75.602 | 6.825 | 0.397 | 100.000 |
| gnn_multiedge_level | post_covid | 10.802 | 104.203 | 8.232 | 0.458 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| gnn_geo | post_covid | 12.824 | 98.435 | 9.058 | 0.369 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.039 | 94.608 | 1.742 | 0.363 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 2.199 | 91.445 | 1.829 | 0.399 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 2.739 | 115.800 | 2.252 | 0.096 | 100.000 |
| persistence | exclude_covid | 3.040 | 109.675 | 2.139 | 0.352 | 100.000 |
| persistence | post_covid | 3.040 | 109.675 | 2.139 | 0.352 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| lstm | post_covid | 3.399 | 153.722 | 2.853 | 0.070 | 100.000 |
| lstm | exclude_covid | 4.026 | 161.515 | 2.945 | 0.091 | 100.000 |
| gnn_multiedge_season | post_covid | 4.291 | 151.960 | 2.874 | 0.254 | 100.000 |
| arima | exclude_covid | 4.694 | 238.314 | 4.313 | 0.369 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.146 | 179.137 | 3.380 | 0.243 | 100.000 |
| arima | post_covid | 5.339 | 273.109 | 5.031 | 0.401 | 100.000 |
| dualtopo_no_bg | post_covid | 6.041 | 310.505 | 5.759 | 0.353 | 100.000 |
| dualtopo | post_covid | 6.177 | 317.107 | 5.890 | 0.349 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.931 | 205.208 | 4.091 | -0.027 | 100.000 |
| gnn_multiedge_full | full | 7.429 | 228.204 | 4.810 | 0.276 | 100.000 |
| gnn_multiedge | post_covid | 11.237 | 325.929 | 6.735 | 0.187 | 100.000 |
| gnn_corrbinary | post_covid | 12.566 | 365.008 | 7.569 | 0.232 | 100.000 |
| gnn_multiedge_level | post_covid | 13.771 | 451.073 | 8.811 | 0.138 | 77.778 |
| gnn_multiedge_leaknorm | post_covid | 14.130 | 409.079 | 8.312 | 0.154 | 100.000 |
| gnn_uniform | post_covid | 16.667 | 474.697 | 9.837 | 0.220 | 100.000 |
| gnn_geo | post_covid | 17.459 | 468.629 | 10.019 | 0.232 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
