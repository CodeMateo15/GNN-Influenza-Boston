# Per-neighborhood leaderboard — horizon 12

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_multiedge_season_level | 11 | 8 | 10 |
| gnn_multiedge_season | 3 | 5 | 0 |
| gnn_corrbinary | 0 | 1 | 0 |
| seasonal_naive | 0 | 0 | 4 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_multiedge_season (post_covid)`: Allston, Mattapan, S.Boston; `gnn_multiedge_season_level (post_covid)`: BackBay+, Charles., Dorchest., E.Boston, Fenway, HydePark, JP, Roslind., Roxbury, S.End, W.Roxbury
- **Flu season (Oct–Mar)** — `gnn_corrbinary (post_covid)`: HydePark; `gnn_multiedge_season (post_covid)`: Allston, Charles., Mattapan, Roxbury, S.Boston; `gnn_multiedge_season_level (post_covid)`: BackBay+, Dorchest., E.Boston, Fenway, JP, Roslind., S.End, W.Roxbury
- **Off-season (Apr–Sep)** — `gnn_multiedge_season_level (post_covid)`: Allston, BackBay+, Charles., E.Boston, Fenway, HydePark, JP, Roslind., S.Boston, W.Roxbury; `seasonal_naive (exclude_covid)`: Dorchest., Mattapan, Roxbury, S.End

`gnn_multiedge_season_level (post_covid)` wins 11 of 14 neighborhoods. `gnn_multiedge_season_level (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 41.749 | 104.472 | 28.383 | 0.659 | 95.918 |
| gnn_multiedge_season | post_covid | 43.387 | 67.835 | 29.190 | 0.640 | 83.673 |
| gnn_multiedge_level | post_covid | 46.498 | 128.214 | 28.121 | 0.587 | 97.959 |
| gnn_corrbinary | post_covid | 46.665 | 103.266 | 28.856 | 0.520 | 95.918 |
| gnn_multiedge | post_covid | 51.473 | 90.211 | 29.745 | 0.405 | 93.878 |
| gnn_geo | post_covid | 51.784 | 85.957 | 29.395 | 0.358 | 91.837 |
| gnn_multiedge_rt | post_covid | 52.170 | 91.090 | 36.321 | 0.602 | 89.796 |
| gnn_uniform | post_covid | 55.684 | 97.587 | 32.913 | 0.270 | 93.878 |
| dualtopo_no_bg | post_covid | 56.398 | 248.503 | 42.414 | 0.324 | 53.061 |
| dualtopo | post_covid | 56.488 | 250.190 | 42.618 | -0.175 | 53.061 |
| gnn_multiedge_full | full | 56.810 | 79.931 | 33.094 | 0.357 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 58.291 | 83.275 | 35.211 | 0.393 | 81.633 |
| dualtopo_fullhistory | full | 59.249 | 174.630 | 42.395 | 0.104 | 87.755 |
| gnn_multiedge_leaknorm | post_covid | 60.087 | 121.501 | 39.789 | 0.281 | 83.673 |
| arima | post_covid | 60.202 | 308.293 | 50.331 | -0.022 | 100.000 |
| lstm | exclude_covid | 63.250 | 169.926 | 46.338 | 0.237 | 79.592 |
| lstm | post_covid | 65.372 | 191.805 | 47.632 | 0.153 | 65.306 |
| gnn_multiedge_covid_rsv | post_covid | 66.722 | 233.173 | 54.137 | 0.406 | 83.673 |
| arima | exclude_covid | 67.347 | 204.241 | 46.778 | 0.005 | 89.796 |
| persistence | exclude_covid | 75.923 | 139.807 | 49.470 | 0.041 | 91.837 |
| persistence | post_covid | 75.923 | 139.807 | 49.470 | 0.041 | 93.878 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 55.260 | 63.667 | 40.696 | 0.477 | 92.308 |
| gnn_multiedge_season | post_covid | 56.308 | 53.021 | 41.533 | 0.470 | 96.154 |
| gnn_corrbinary | post_covid | 60.011 | 52.760 | 37.587 | 0.381 | 92.308 |
| gnn_multiedge_level | post_covid | 60.204 | 56.008 | 35.656 | 0.408 | 96.154 |
| arima | post_covid | 62.846 | 104.183 | 45.992 | 0.059 | 100.000 |
| dualtopo | post_covid | 64.039 | 79.202 | 40.630 | -0.618 | 69.231 |
| dualtopo_no_bg | post_covid | 64.104 | 78.650 | 40.550 | -0.037 | 69.231 |
| gnn_multiedge | post_covid | 67.169 | 48.404 | 40.284 | 0.195 | 88.462 |
| gnn_geo | post_covid | 68.894 | 53.116 | 43.407 | 0.104 | 84.615 |
| gnn_multiedge_rt | post_covid | 69.046 | 95.127 | 56.075 | 0.396 | 100.000 |
| gnn_uniform | post_covid | 73.190 | 50.706 | 45.342 | 0.015 | 88.462 |
| gnn_multiedge_full | full | 75.431 | 53.600 | 47.964 | 0.189 | 92.308 |
| dualtopo_fullhistory | full | 76.481 | 79.787 | 54.989 | -0.158 | 76.923 |
| gnn_multiedge_covid_rsv_full | full | 77.494 | 57.969 | 51.643 | 0.335 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 78.722 | 72.994 | 55.550 | 0.041 | 80.769 |
| gnn_multiedge_covid_rsv | post_covid | 79.909 | 193.273 | 69.350 | 0.214 | 88.462 |
| lstm | exclude_covid | 81.018 | 105.965 | 62.560 | -0.087 | 69.231 |
| lstm | post_covid | 81.895 | 101.105 | 58.848 | -0.090 | 65.385 |
| arima | exclude_covid | 82.043 | 61.440 | 52.711 | 0.080 | 80.769 |
| persistence | exclude_covid | 100.586 | 85.167 | 72.013 | -0.069 | 84.615 |
| persistence | post_covid | 100.586 | 85.167 | 72.013 | -0.069 | 88.462 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.165 | 150.600 | 14.464 | 0.634 | 100.000 |
| gnn_geo | post_covid | 18.641 | 123.082 | 13.556 | 0.495 | 100.000 |
| gnn_multiedge_rt | post_covid | 20.231 | 86.527 | 13.991 | -0.386 | 78.261 |
| gnn_multiedge_season | post_covid | 20.644 | 84.581 | 15.237 | -0.422 | 69.565 |
| gnn_multiedge_full | full | 21.063 | 109.697 | 16.285 | -0.388 | 91.304 |
| gnn_multiedge_covid_rsv_full | full | 21.219 | 111.883 | 16.636 | -0.379 | 78.261 |
| gnn_multiedge_level | post_covid | 22.558 | 209.837 | 19.604 | 0.499 | 100.000 |
| gnn_multiedge | post_covid | 23.332 | 137.471 | 17.830 | -0.361 | 100.000 |
| gnn_uniform | post_covid | 23.458 | 150.583 | 18.863 | -0.621 | 100.000 |
| gnn_corrbinary | post_covid | 23.835 | 160.358 | 18.986 | 0.436 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 26.199 | 176.336 | 21.972 | -0.586 | 86.957 |
| persistence | exclude_covid | 29.034 | 201.575 | 23.987 | 0.488 | 100.000 |
| persistence | post_covid | 29.034 | 201.575 | 23.987 | 0.488 | 100.000 |
| dualtopo_fullhistory | full | 29.439 | 281.844 | 28.157 | 0.711 | 100.000 |
| lstm | exclude_covid | 33.209 | 242.229 | 28.000 | 0.635 | 91.304 |
| lstm | post_covid | 39.023 | 294.334 | 34.953 | 0.602 | 65.217 |
| arima | exclude_covid | 45.319 | 365.668 | 40.071 | 0.177 | 100.000 |
| dualtopo_no_bg | post_covid | 46.163 | 440.511 | 44.521 | 0.062 | 34.783 |
| dualtopo | post_covid | 46.497 | 443.481 | 44.867 | 0.164 | 34.783 |
| gnn_multiedge_covid_rsv | post_covid | 47.603 | 278.278 | 36.939 | -0.201 | 78.261 |
| arima | post_covid | 57.065 | 539.027 | 55.237 | -0.585 | 100.000 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 39.502 | 102.692 | 24.850 | 0.627 | 93.878 |
| gnn_multiedge_season | post_covid | 40.514 | 88.642 | 27.735 | 0.621 | 77.551 |
| gnn_corrbinary | post_covid | 42.739 | 125.266 | 30.195 | 0.528 | 91.837 |
| gnn_multiedge_level | post_covid | 43.156 | 122.607 | 26.302 | 0.605 | 97.959 |
| gnn_multiedge | post_covid | 46.825 | 117.779 | 31.239 | 0.415 | 97.959 |
| gnn_geo | post_covid | 47.677 | 119.850 | 31.836 | 0.376 | 97.959 |
| gnn_multiedge_rt | post_covid | 47.973 | 115.115 | 33.508 | 0.572 | 85.714 |
| gnn_multiedge_full | full | 49.000 | 88.510 | 29.386 | 0.497 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 50.692 | 86.707 | 30.909 | 0.489 | 77.551 |
| dualtopo_no_bg | post_covid | 51.040 | 228.106 | 37.258 | 0.274 | 55.102 |
| dualtopo | post_covid | 51.100 | 229.659 | 37.413 | -0.247 | 55.102 |
| gnn_uniform | post_covid | 51.310 | 121.686 | 33.959 | 0.287 | 97.959 |
| arima | post_covid | 52.718 | 263.667 | 41.315 |  | 97.959 |
| gnn_multiedge_covid_rsv | post_covid | 52.975 | 222.502 | 43.360 | 0.526 | 87.755 |
| arima | exclude_covid | 54.656 | 293.254 | 44.990 |  | 95.918 |
| gnn_multiedge_leaknorm | post_covid | 55.324 | 143.988 | 38.567 | 0.294 | 87.755 |
| dualtopo_fullhistory | full | 55.992 | 181.333 | 39.982 | 0.037 | 85.714 |
| lstm | exclude_covid | 60.199 | 180.532 | 42.705 | 0.171 | 79.592 |
| lstm | post_covid | 60.453 | 189.122 | 41.823 | 0.088 | 69.388 |
| persistence | exclude_covid | 69.708 | 158.853 | 46.598 | 0.045 | 93.878 |
| persistence | post_covid | 69.708 | 158.853 | 46.598 | 0.045 | 93.878 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 87.755 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 51.584 | 66.555 | 37.042 | 0.496 | 96.154 |
| gnn_multiedge_season_level | post_covid | 52.532 | 70.580 | 35.925 | 0.467 | 88.462 |
| gnn_corrbinary | post_covid | 54.509 | 76.896 | 41.597 | 0.439 | 88.462 |
| gnn_multiedge_level | post_covid | 56.714 | 65.835 | 35.536 | 0.465 | 96.154 |
| arima | exclude_covid | 58.986 | 115.661 | 42.783 |  | 92.308 |
| arima | post_covid | 59.325 | 103.016 | 40.684 |  | 96.154 |
| dualtopo | post_covid | 60.354 | 88.968 | 38.676 | -0.691 | 65.385 |
| dualtopo_no_bg | post_covid | 60.416 | 88.395 | 38.629 | -0.096 | 65.385 |
| gnn_multiedge | post_covid | 61.270 | 72.326 | 43.716 | 0.262 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 62.126 | 194.694 | 54.028 | 0.441 | 96.154 |
| gnn_multiedge_rt | post_covid | 62.667 | 106.318 | 48.981 | 0.403 | 96.154 |
| gnn_geo | post_covid | 62.857 | 83.410 | 46.286 | 0.185 | 96.154 |
| gnn_multiedge_full | full | 63.965 | 57.405 | 40.011 | 0.449 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 66.504 | 60.999 | 43.093 | 0.468 | 80.769 |
| gnn_uniform | post_covid | 67.110 | 72.419 | 47.071 | 0.110 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 71.802 | 97.675 | 53.559 | 0.082 | 92.308 |
| dualtopo_fullhistory | full | 72.727 | 104.391 | 53.808 | -0.228 | 73.077 |
| lstm | post_covid | 78.238 | 115.710 | 55.921 | -0.153 | 65.385 |
| lstm | exclude_covid | 78.528 | 132.886 | 60.057 | -0.149 | 65.385 |
| persistence | exclude_covid | 91.696 | 96.992 | 66.585 | -0.064 | 88.462 |
| persistence | post_covid | 91.696 | 96.992 | 66.585 | -0.064 | 88.462 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 76.923 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| gnn_multiedge_season_level | post_covid | 14.309 | 138.993 | 12.331 | 0.462 | 100.000 |
| gnn_multiedge_level | post_covid | 18.217 | 186.784 | 15.865 | 0.509 | 100.000 |
| gnn_geo | post_covid | 19.398 | 161.042 | 15.501 | 0.382 | 100.000 |
| gnn_multiedge | post_covid | 20.675 | 169.159 | 17.134 | 0.002 | 100.000 |
| gnn_multiedge_rt | post_covid | 21.532 | 125.059 | 16.017 | -0.264 | 73.913 |
| gnn_multiedge_covid_rsv_full | full | 21.792 | 115.769 | 17.135 | -0.326 | 73.913 |
| gnn_multiedge_season | post_covid | 22.112 | 113.611 | 17.215 | -0.290 | 56.522 |
| gnn_multiedge_full | full | 22.136 | 123.671 | 17.376 | -0.362 | 86.957 |
| gnn_uniform | post_covid | 22.753 | 177.379 | 19.137 | -0.401 | 100.000 |
| gnn_corrbinary | post_covid | 23.078 | 179.945 | 17.306 | 0.432 | 95.652 |
| gnn_multiedge_leaknorm | post_covid | 26.319 | 196.343 | 21.620 | -0.374 | 82.609 |
| dualtopo_fullhistory | full | 26.460 | 268.311 | 24.352 | 0.628 | 100.000 |
| lstm | exclude_covid | 27.378 | 234.393 | 23.089 | 0.649 | 95.652 |
| persistence | exclude_covid | 29.110 | 228.783 | 24.004 | 0.441 | 100.000 |
| persistence | post_covid | 29.110 | 228.783 | 24.004 | 0.441 | 100.000 |
| lstm | post_covid | 29.431 | 272.109 | 25.886 | 0.555 | 73.913 |
| dualtopo_no_bg | post_covid | 37.733 | 386.040 | 35.709 | 0.193 | 43.478 |
| dualtopo | post_covid | 38.017 | 388.701 | 35.986 | 0.160 | 43.478 |
| gnn_multiedge_covid_rsv | post_covid | 40.195 | 253.937 | 31.300 | -0.147 | 78.261 |
| arima | post_covid | 44.074 | 445.272 | 42.027 |  | 100.000 |
| arima | exclude_covid | 49.304 | 494.010 | 47.484 |  | 100.000 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 32.013 | 96.363 | 18.893 | 0.624 | 92.857 |
| gnn_multiedge_season | post_covid | 34.519 | 105.959 | 23.311 | 0.479 | 90.476 |
| gnn_multiedge_level | post_covid | 36.732 | 95.148 | 20.083 | 0.444 | 95.238 |
| gnn_multiedge_rt | post_covid | 38.005 | 143.856 | 27.872 | 0.401 | 92.857 |
| dualtopo_no_bg | post_covid | 38.800 | 161.284 | 25.633 | 0.152 | 83.333 |
| dualtopo | post_covid | 38.804 | 162.403 | 25.718 | -0.464 | 80.952 |
| arima | exclude_covid | 39.165 | 193.817 | 28.442 |  | 92.857 |
| gnn_geo | post_covid | 39.174 | 104.837 | 24.020 | 0.217 | 95.238 |
| arima | post_covid | 39.238 | 182.808 | 28.133 | -0.041 | 97.619 |
| gnn_corrbinary | post_covid | 39.491 | 106.145 | 24.715 | 0.251 | 95.238 |
| gnn_multiedge_covid_rsv | post_covid | 40.068 | 203.597 | 32.139 | 0.319 | 88.095 |
| gnn_multiedge_leaknorm | post_covid | 40.651 | 142.265 | 27.215 | 0.216 | 92.857 |
| gnn_multiedge | post_covid | 40.690 | 104.564 | 25.207 | 0.188 | 95.238 |
| gnn_multiedge_full | full | 40.902 | 99.472 | 25.222 | 0.195 | 90.476 |
| dualtopo_fullhistory | full | 41.741 | 138.402 | 26.118 | 0.014 | 85.714 |
| lstm | exclude_covid | 41.787 | 163.995 | 27.891 | 0.097 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 42.452 | 91.326 | 25.737 | 0.147 | 80.952 |
| lstm | post_covid | 43.555 | 189.714 | 29.311 | 0.013 | 83.333 |
| gnn_uniform | post_covid | 43.959 | 115.291 | 28.075 | 0.086 | 95.238 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |
| persistence | exclude_covid | 56.020 | 140.016 | 34.907 | -0.042 | 95.238 |
| persistence | post_covid | 56.020 | 140.016 | 34.907 | -0.042 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 40.164 | 100.956 | 25.946 | 0.551 | 88.462 |
| gnn_multiedge_season | post_covid | 41.865 | 96.611 | 29.411 | 0.401 | 100.000 |
| arima | exclude_covid | 45.871 | 138.923 | 31.920 |  | 88.462 |
| gnn_multiedge_level | post_covid | 46.086 | 86.769 | 27.329 | 0.308 | 92.308 |
| gnn_multiedge_rt | post_covid | 46.416 | 145.892 | 36.246 | 0.280 | 100.000 |
| arima | post_covid | 46.501 | 131.749 | 32.622 | -0.097 | 96.154 |
| dualtopo | post_covid | 46.675 | 117.746 | 30.457 | -0.678 | 80.769 |
| dualtopo_no_bg | post_covid | 46.713 | 117.042 | 30.429 | -0.082 | 80.769 |
| gnn_multiedge_covid_rsv | post_covid | 46.867 | 191.116 | 39.095 | 0.221 | 96.154 |
| gnn_geo | post_covid | 48.534 | 89.287 | 31.480 | 0.102 | 92.308 |
| gnn_corrbinary | post_covid | 49.179 | 85.242 | 33.375 | 0.154 | 92.308 |
| gnn_multiedge_leaknorm | post_covid | 49.552 | 122.119 | 34.346 | 0.086 | 92.308 |
| gnn_multiedge_full | full | 49.933 | 66.600 | 31.081 | 0.137 | 100.000 |
| gnn_multiedge | post_covid | 50.285 | 75.226 | 32.561 | 0.080 | 92.308 |
| lstm | exclude_covid | 51.732 | 167.419 | 37.689 | -0.114 | 76.923 |
| gnn_multiedge_covid_rsv_full | full | 52.052 | 63.637 | 32.136 | 0.071 | 84.615 |
| dualtopo_fullhistory | full | 52.079 | 135.824 | 34.801 | -0.145 | 76.923 |
| lstm | post_covid | 53.135 | 166.604 | 36.714 | -0.095 | 73.077 |
| gnn_uniform | post_covid | 54.040 | 83.697 | 35.530 | -0.017 | 92.308 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |
| persistence | exclude_covid | 69.547 | 105.629 | 46.992 | -0.085 | 92.308 |
| persistence | post_covid | 69.547 | 105.629 | 46.992 | -0.085 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 8.294 | 88.900 | 7.432 | 0.632 | 100.000 |
| gnn_multiedge_level | post_covid | 9.507 | 108.763 | 8.307 | 0.712 | 100.000 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| gnn_corrbinary | post_covid | 12.795 | 140.114 | 10.644 | 0.081 | 100.000 |
| dualtopo_fullhistory | full | 12.890 | 142.593 | 12.007 | 0.521 | 100.000 |
| gnn_geo | post_covid | 14.167 | 130.105 | 11.898 | 0.045 | 100.000 |
| lstm | exclude_covid | 15.324 | 158.429 | 11.969 | 0.253 | 100.000 |
| gnn_multiedge | post_covid | 15.402 | 152.237 | 13.257 | -0.459 | 100.000 |
| gnn_multiedge_season | post_covid | 16.729 | 121.148 | 13.398 | -0.681 | 75.000 |
| gnn_multiedge_rt | post_covid | 17.044 | 140.547 | 14.263 | -0.684 | 81.250 |
| gnn_uniform | post_covid | 18.083 | 166.631 | 15.960 | -0.673 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 18.108 | 136.320 | 15.340 | -0.630 | 75.000 |
| gnn_multiedge_full | full | 18.438 | 152.888 | 15.700 | -0.754 | 75.000 |
| gnn_multiedge_leaknorm | post_covid | 18.653 | 175.002 | 15.628 | -0.657 | 93.750 |
| persistence | exclude_covid | 19.445 | 195.894 | 15.269 | 0.019 | 100.000 |
| persistence | post_covid | 19.445 | 195.894 | 15.269 | 0.019 | 100.000 |
| lstm | post_covid | 19.793 | 227.267 | 17.280 | 0.192 | 100.000 |
| dualtopo_no_bg | post_covid | 20.149 | 233.176 | 17.839 | 0.302 | 87.500 |
| dualtopo | post_covid | 20.307 | 234.971 | 18.017 | -0.025 | 81.250 |
| arima | post_covid | 22.972 | 265.779 | 20.838 | -0.258 | 100.000 |
| arima | exclude_covid | 24.642 | 283.021 | 22.792 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 25.396 | 223.880 | 20.836 | -0.412 | 75.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 25.365 | 106.299 | 15.808 | 0.632 | 97.959 |
| gnn_multiedge_season | post_covid | 26.146 | 79.096 | 15.913 | 0.589 | 87.755 |
| gnn_multiedge_level | post_covid | 29.105 | 124.639 | 17.787 | 0.463 | 100.000 |
| gnn_multiedge_rt | post_covid | 30.370 | 109.637 | 19.849 | 0.533 | 95.918 |
| gnn_corrbinary | post_covid | 32.220 | 128.680 | 22.042 | 0.281 | 93.878 |
| dualtopo_no_bg | post_covid | 32.433 | 216.907 | 23.832 | 0.278 | 85.714 |
| dualtopo | post_covid | 32.463 | 218.314 | 23.914 | -0.307 | 85.714 |
| gnn_multiedge_full | full | 32.568 | 87.740 | 18.541 | 0.285 | 91.837 |
| gnn_geo | post_covid | 32.766 | 112.132 | 20.864 | 0.205 | 97.959 |
| gnn_multiedge | post_covid | 32.779 | 107.128 | 20.301 | 0.201 | 97.959 |
| arima | post_covid | 33.536 | 256.947 | 26.647 |  | 100.000 |
| dualtopo_fullhistory | full | 34.371 | 146.645 | 23.297 | 0.040 | 89.796 |
| gnn_multiedge_covid_rsv_full | full | 34.446 | 93.032 | 20.351 | 0.177 | 81.633 |
| gnn_uniform | post_covid | 34.760 | 110.278 | 21.713 | 0.101 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 35.501 | 126.682 | 23.421 | 0.206 | 97.959 |
| lstm | post_covid | 36.178 | 196.413 | 26.689 | 0.123 | 83.673 |
| lstm | exclude_covid | 36.430 | 146.512 | 24.755 | 0.138 | 87.755 |
| gnn_multiedge_covid_rsv | post_covid | 37.190 | 276.291 | 29.749 | 0.326 | 89.796 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| arima | exclude_covid | 41.541 | 199.085 | 30.379 | 0.043 | 91.837 |
| persistence | exclude_covid | 46.676 | 135.366 | 30.329 | -0.049 | 91.837 |
| persistence | post_covid | 46.676 | 135.366 | 30.329 | -0.049 | 95.918 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 33.961 | 102.881 | 23.401 | 0.484 | 96.154 |
| gnn_multiedge_season | post_covid | 34.529 | 90.787 | 23.261 | 0.442 | 100.000 |
| gnn_multiedge_level | post_covid | 38.430 | 99.060 | 24.538 | 0.272 | 100.000 |
| arima | post_covid | 38.457 | 151.508 | 27.094 |  | 100.000 |
| dualtopo | post_covid | 39.199 | 130.041 | 25.943 | -0.726 | 76.923 |
| dualtopo_no_bg | post_covid | 39.235 | 129.354 | 25.942 | -0.069 | 76.923 |
| gnn_multiedge_rt | post_covid | 40.877 | 142.803 | 31.466 | 0.323 | 100.000 |
| gnn_corrbinary | post_covid | 41.262 | 120.806 | 29.685 | 0.133 | 88.462 |
| gnn_geo | post_covid | 43.395 | 108.542 | 30.583 | -0.024 | 96.154 |
| gnn_multiedge_full | full | 43.526 | 79.408 | 27.595 | 0.163 | 92.308 |
| gnn_multiedge | post_covid | 43.696 | 101.040 | 30.056 | -0.003 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 44.822 | 293.207 | 38.536 | 0.149 | 96.154 |
| dualtopo_fullhistory | full | 45.492 | 113.802 | 33.142 | -0.197 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 46.101 | 87.257 | 30.414 | 0.054 | 76.923 |
| lstm | post_covid | 46.269 | 151.231 | 35.855 | -0.092 | 69.231 |
| gnn_uniform | post_covid | 46.473 | 100.166 | 32.349 | -0.096 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 46.755 | 124.308 | 33.616 | -0.031 | 96.154 |
| lstm | exclude_covid | 47.973 | 121.803 | 36.148 | -0.094 | 76.923 |
| arima | exclude_covid | 51.676 | 156.030 | 38.440 | -0.022 | 84.615 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| persistence | exclude_covid | 60.923 | 117.969 | 44.042 | -0.139 | 84.615 |
| persistence | post_covid | 60.923 | 117.969 | 44.042 | -0.139 | 92.308 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| gnn_multiedge_season_level | post_covid | 8.180 | 110.163 | 7.225 | 0.484 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.725 | 72.145 | 6.717 | 0.361 | 91.304 |
| gnn_multiedge_season | post_covid | 10.425 | 65.880 | 7.607 | 0.038 | 73.913 |
| gnn_multiedge_full | full | 10.864 | 97.158 | 8.306 | -0.110 | 91.304 |
| gnn_multiedge_covid_rsv_full | full | 11.193 | 99.559 | 8.975 | -0.243 | 86.957 |
| gnn_multiedge | post_covid | 11.432 | 114.011 | 9.274 | 0.469 | 100.000 |
| gnn_uniform | post_covid | 11.515 | 121.709 | 9.689 | -0.105 | 100.000 |
| gnn_multiedge_level | post_covid | 11.627 | 153.553 | 10.155 | 0.249 | 100.000 |
| gnn_geo | post_covid | 12.588 | 116.190 | 9.877 | 0.707 | 100.000 |
| dualtopo_fullhistory | full | 13.317 | 183.771 | 12.168 | 0.564 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 14.623 | 129.366 | 11.897 | 0.039 | 100.000 |
| lstm | exclude_covid | 15.025 | 174.443 | 11.876 | 0.246 | 100.000 |
| gnn_corrbinary | post_covid | 16.942 | 137.580 | 13.401 | 0.732 | 100.000 |
| lstm | post_covid | 19.190 | 247.488 | 16.327 | 0.120 | 100.000 |
| persistence | exclude_covid | 21.113 | 155.032 | 14.826 | 0.577 | 100.000 |
| persistence | post_covid | 21.113 | 155.032 | 14.826 | 0.577 | 100.000 |
| dualtopo_no_bg | post_covid | 22.379 | 315.881 | 21.447 | 0.179 | 95.652 |
| dualtopo | post_covid | 22.545 | 318.101 | 21.620 | 0.100 | 95.652 |
| arima | exclude_covid | 25.643 | 247.756 | 21.266 | 0.488 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 25.990 | 257.168 | 19.816 | -0.286 | 82.609 |
| arima | post_covid | 26.911 | 376.139 | 26.141 |  | 100.000 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 18.991 | 77.271 | 11.746 | 0.513 | 97.143 |
| gnn_multiedge_season | post_covid | 19.555 | 85.710 | 13.570 | 0.477 | 88.571 |
| gnn_multiedge_rt | post_covid | 20.833 | 102.408 | 14.261 | 0.379 | 88.571 |
| gnn_multiedge_level | post_covid | 21.309 | 71.104 | 11.697 | 0.366 | 100.000 |
| dualtopo_no_bg | post_covid | 21.936 | 116.803 | 13.943 | 0.171 | 88.571 |
| dualtopo | post_covid | 21.937 | 117.638 | 13.986 | -0.389 | 88.571 |
| arima | post_covid | 22.066 | 139.191 | 15.331 |  | 100.000 |
| gnn_geo | post_covid | 22.110 | 81.933 | 13.010 | 0.187 | 100.000 |
| arima | exclude_covid | 22.301 | 154.977 | 16.493 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 22.848 | 164.474 | 18.061 | 0.280 | 100.000 |
| gnn_multiedge_full | full | 22.883 | 78.384 | 13.546 | 0.237 | 85.714 |
| gnn_corrbinary | post_covid | 23.016 | 100.519 | 14.799 | 0.182 | 94.286 |
| gnn_multiedge | post_covid | 23.133 | 91.935 | 14.878 | 0.150 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 23.234 | 110.254 | 15.781 | 0.171 | 97.143 |
| dualtopo_fullhistory | full | 23.276 | 126.817 | 16.085 | 0.151 | 88.571 |
| lstm | post_covid | 23.419 | 127.864 | 14.646 | 0.035 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 23.872 | 86.263 | 15.083 | 0.168 | 82.857 |
| gnn_uniform | post_covid | 23.996 | 84.791 | 14.661 | 0.089 | 100.000 |
| lstm | exclude_covid | 24.177 | 130.955 | 16.010 | 0.002 | 85.714 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| persistence | exclude_covid | 29.525 | 94.737 | 16.769 | -0.083 | 97.143 |
| persistence | post_covid | 29.525 | 94.737 | 16.769 | -0.083 | 97.143 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 23.235 | 92.812 | 17.070 | 0.500 | 100.000 |
| gnn_multiedge_season_level | post_covid | 24.273 | 101.691 | 17.229 | 0.418 | 95.238 |
| gnn_multiedge_rt | post_covid | 24.979 | 122.383 | 18.421 | 0.335 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 26.509 | 167.461 | 20.739 | 0.276 | 100.000 |
| arima | exclude_covid | 26.528 | 139.152 | 19.069 |  | 100.000 |
| arima | post_covid | 26.684 | 125.798 | 18.217 |  | 100.000 |
| dualtopo | post_covid | 27.093 | 107.848 | 17.331 | -0.594 | 80.952 |
| dualtopo_no_bg | post_covid | 27.113 | 107.167 | 17.307 | -0.086 | 80.952 |
| gnn_multiedge_level | post_covid | 27.248 | 83.407 | 17.018 | 0.232 | 100.000 |
| gnn_multiedge_full | full | 27.610 | 68.903 | 16.287 | 0.338 | 90.476 |
| gnn_multiedge_leaknorm | post_covid | 27.791 | 117.818 | 19.517 | 0.067 | 95.238 |
| gnn_geo | post_covid | 27.847 | 89.129 | 17.763 | 0.102 | 100.000 |
| gnn_corrbinary | post_covid | 28.103 | 100.113 | 19.148 | 0.153 | 90.476 |
| gnn_multiedge | post_covid | 28.226 | 94.015 | 18.978 | 0.118 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 29.226 | 83.975 | 19.046 | 0.273 | 85.714 |
| gnn_uniform | post_covid | 29.309 | 87.092 | 18.772 | 0.037 | 100.000 |
| lstm | post_covid | 29.318 | 142.143 | 19.267 | -0.100 | 76.190 |
| dualtopo_fullhistory | full | 29.461 | 161.219 | 22.942 | -0.075 | 80.952 |
| lstm | exclude_covid | 30.454 | 157.588 | 22.324 | -0.201 | 76.190 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| persistence | exclude_covid | 36.473 | 106.641 | 23.781 | -0.109 | 95.238 |
| persistence | post_covid | 36.473 | 106.641 | 23.781 | -0.109 | 95.238 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 4.226 | 40.642 | 3.523 | 0.643 | 100.000 |
| gnn_multiedge_level | post_covid | 4.634 | 52.650 | 3.714 | 0.673 | 100.000 |
| dualtopo_fullhistory | full | 7.245 | 75.214 | 5.801 | 0.551 | 100.000 |
| gnn_geo | post_covid | 7.676 | 71.138 | 5.881 | 0.197 | 100.000 |
| lstm | exclude_covid | 8.377 | 91.005 | 6.538 | 0.137 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| lstm | post_covid | 9.047 | 106.444 | 7.715 | -0.109 | 100.000 |
| dualtopo_no_bg | post_covid | 10.015 | 131.256 | 8.898 | 0.357 | 100.000 |
| dualtopo | post_covid | 10.101 | 132.324 | 8.970 | 0.256 | 100.000 |
| gnn_corrbinary | post_covid | 11.818 | 101.128 | 8.276 | 0.360 | 100.000 |
| gnn_multiedge | post_covid | 11.949 | 88.814 | 8.729 | -0.026 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 11.976 | 89.695 | 9.139 | -0.217 | 78.571 |
| gnn_multiedge_season | post_covid | 12.090 | 75.057 | 8.321 | -0.089 | 71.429 |
| gnn_multiedge_rt | post_covid | 12.212 | 72.446 | 8.021 | -0.162 | 71.429 |
| arima | post_covid | 12.216 | 159.280 | 11.003 |  | 100.000 |
| gnn_uniform | post_covid | 12.290 | 81.338 | 8.495 | -0.246 | 100.000 |
| gnn_multiedge_full | full | 12.870 | 92.604 | 9.433 | -0.206 | 78.571 |
| persistence | exclude_covid | 13.563 | 76.882 | 6.250 | 0.223 | 100.000 |
| persistence | post_covid | 13.563 | 76.882 | 6.250 | 0.223 | 100.000 |
| arima | exclude_covid | 13.698 | 178.713 | 12.629 |  | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 13.823 | 98.907 | 10.177 | -0.173 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 15.843 | 159.993 | 14.043 | -0.390 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 16.749 | 74.736 | 10.625 | 0.683 | 76.596 |
| gnn_multiedge_season_level | post_covid | 17.190 | 141.915 | 13.554 | 0.729 | 100.000 |
| gnn_multiedge_rt | post_covid | 19.284 | 118.207 | 14.447 | 0.608 | 87.234 |
| gnn_multiedge_level | post_covid | 20.980 | 175.016 | 15.535 | 0.441 | 100.000 |
| gnn_corrbinary | post_covid | 22.852 | 136.598 | 14.952 | 0.273 | 93.617 |
| gnn_multiedge | post_covid | 23.043 | 118.284 | 14.734 | 0.233 | 100.000 |
| gnn_multiedge_full | full | 23.215 | 106.724 | 13.869 | 0.300 | 93.617 |
| gnn_geo | post_covid | 23.291 | 138.732 | 15.463 | 0.183 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 23.883 | 133.556 | 15.640 | 0.268 | 100.000 |
| gnn_uniform | post_covid | 24.194 | 121.764 | 14.968 | 0.135 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 24.667 | 111.367 | 15.155 | 0.164 | 87.234 |
| dualtopo_no_bg | post_covid | 25.047 | 297.691 | 21.174 | 0.322 | 91.489 |
| dualtopo | post_covid | 25.116 | 299.664 | 21.286 | -0.258 | 91.489 |
| dualtopo_fullhistory | full | 25.667 | 198.358 | 19.183 | 0.076 | 91.489 |
| arima | post_covid | 26.731 | 341.236 | 23.630 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 27.910 | 288.470 | 22.232 | 0.351 | 97.872 |
| lstm | exclude_covid | 28.336 | 219.960 | 20.814 | 0.138 | 87.234 |
| lstm | post_covid | 29.976 | 265.270 | 22.759 | 0.079 | 85.106 |
| arima | exclude_covid | 32.537 | 156.987 | 21.278 | -0.115 | 89.362 |
| persistence | exclude_covid | 33.815 | 161.160 | 22.098 | -0.104 | 91.489 |
| persistence | post_covid | 33.815 | 161.160 | 22.098 | -0.104 | 93.617 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 21.313 | 63.527 | 13.825 | 0.610 | 100.000 |
| gnn_multiedge_season_level | post_covid | 21.568 | 104.135 | 17.683 | 0.647 | 100.000 |
| gnn_multiedge_rt | post_covid | 24.547 | 113.258 | 19.678 | 0.499 | 100.000 |
| gnn_multiedge_level | post_covid | 26.127 | 113.431 | 19.038 | 0.223 | 100.000 |
| dualtopo_no_bg | post_covid | 26.751 | 144.550 | 20.175 | 0.028 | 84.615 |
| dualtopo | post_covid | 26.760 | 145.566 | 20.248 | -0.630 | 84.615 |
| arima | post_covid | 27.142 | 167.104 | 21.788 |  | 100.000 |
| gnn_corrbinary | post_covid | 27.620 | 87.983 | 18.311 | 0.206 | 92.308 |
| gnn_geo | post_covid | 29.259 | 93.697 | 19.576 | 0.020 | 100.000 |
| gnn_multiedge | post_covid | 29.643 | 82.025 | 19.337 | 0.053 | 100.000 |
| gnn_multiedge_full | full | 30.137 | 72.963 | 18.670 | 0.196 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 30.652 | 97.745 | 20.943 | 0.058 | 100.000 |
| gnn_uniform | post_covid | 31.353 | 82.613 | 20.016 | -0.103 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 32.170 | 81.439 | 20.915 | 0.058 | 84.615 |
| dualtopo_fullhistory | full | 32.232 | 131.195 | 24.031 | -0.144 | 84.615 |
| gnn_multiedge_covid_rsv | post_covid | 33.177 | 254.436 | 27.931 | 0.208 | 100.000 |
| lstm | exclude_covid | 35.394 | 165.535 | 26.817 | -0.123 | 76.923 |
| lstm | post_covid | 36.060 | 179.286 | 26.708 | -0.128 | 73.077 |
| arima | exclude_covid | 41.749 | 115.790 | 29.099 | -0.196 | 80.769 |
| persistence | exclude_covid | 43.545 | 123.333 | 30.581 | -0.188 | 84.615 |
| persistence | post_covid | 43.545 | 123.333 | 30.581 | -0.188 | 88.462 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gnn_multiedge_season | post_covid | 8.093 | 88.613 | 6.664 | -0.093 | 47.619 |
| gnn_multiedge_covid_rsv_full | full | 8.967 | 148.422 | 8.023 | -0.381 | 90.476 |
| gnn_multiedge_full | full | 9.038 | 148.523 | 7.925 | -0.458 | 90.476 |
| gnn_multiedge_season_level | post_covid | 9.242 | 188.689 | 8.443 | 0.523 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.292 | 124.336 | 7.970 | -0.210 | 71.429 |
| gnn_uniform | post_covid | 9.647 | 170.237 | 8.719 | -0.365 | 100.000 |
| gnn_multiedge | post_covid | 10.022 | 163.175 | 9.036 | -0.131 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.647 | 177.893 | 9.075 | -0.318 | 100.000 |
| gnn_multiedge_level | post_covid | 11.829 | 251.266 | 11.198 | 0.450 | 100.000 |
| gnn_geo | post_covid | 12.416 | 194.490 | 10.370 | 0.364 | 100.000 |
| dualtopo_fullhistory | full | 13.718 | 281.512 | 13.179 | 0.608 | 100.000 |
| arima | exclude_covid | 14.542 | 207.993 | 11.595 | 0.557 | 100.000 |
| persistence | exclude_covid | 14.542 | 207.993 | 11.595 | 0.557 | 100.000 |
| persistence | post_covid | 14.542 | 207.993 | 11.595 | 0.557 | 100.000 |
| gnn_corrbinary | post_covid | 14.976 | 196.788 | 10.795 | 0.280 | 95.238 |
| lstm | exclude_covid | 15.683 | 287.344 | 13.381 | 0.261 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 19.509 | 330.608 | 15.176 | -0.386 | 95.238 |
| lstm | post_covid | 20.029 | 371.726 | 17.870 | 0.282 | 100.000 |
| dualtopo_no_bg | post_covid | 22.761 | 487.293 | 22.412 | 0.186 | 100.000 |
| dualtopo | post_covid | 22.918 | 490.453 | 22.571 | 0.039 | 100.000 |
| arima | post_covid | 26.213 | 556.827 | 25.911 |  | 100.000 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 16.792 | 117.004 | 11.110 | 0.573 | 100.000 |
| gnn_multiedge_season | post_covid | 17.143 | 115.065 | 12.558 | 0.569 | 80.435 |
| gnn_corrbinary | post_covid | 17.156 | 137.453 | 11.418 | 0.531 | 97.826 |
| gnn_multiedge_level | post_covid | 17.803 | 126.228 | 10.243 | 0.544 | 100.000 |
| gnn_multiedge | post_covid | 19.165 | 130.153 | 12.288 | 0.373 | 100.000 |
| gnn_geo | post_covid | 19.429 | 125.096 | 11.704 | 0.338 | 100.000 |
| gnn_multiedge_rt | post_covid | 19.448 | 155.834 | 15.302 | 0.546 | 91.304 |
| gnn_multiedge_full | full | 20.095 | 114.976 | 12.476 | 0.365 | 84.783 |
| gnn_multiedge_covid_rsv_full | full | 20.391 | 106.057 | 11.851 | 0.409 | 89.130 |
| gnn_uniform | post_covid | 20.619 | 135.593 | 13.001 | 0.238 | 100.000 |
| dualtopo_no_bg | post_covid | 21.051 | 252.769 | 15.951 | 0.201 | 91.304 |
| dualtopo | post_covid | 21.089 | 254.595 | 16.031 | -0.315 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 21.727 | 157.682 | 15.468 | 0.259 | 100.000 |
| arima | post_covid | 21.747 | 271.845 | 17.154 | 0.015 | 100.000 |
| dualtopo_fullhistory | full | 23.407 | 176.132 | 16.379 | 0.005 | 91.304 |
| gnn_multiedge_covid_rsv | post_covid | 23.519 | 292.335 | 19.966 | 0.436 | 89.130 |
| lstm | exclude_covid | 24.423 | 194.534 | 18.173 | 0.176 | 93.478 |
| lstm | post_covid | 25.057 | 205.459 | 17.916 | 0.120 | 84.783 |
| arima | exclude_covid | 26.884 | 242.178 | 18.866 | -0.040 | 93.478 |
| persistence | exclude_covid | 28.585 | 167.117 | 17.672 | 0.016 | 100.000 |
| persistence | post_covid | 28.585 | 167.117 | 17.672 | 0.016 | 100.000 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_corrbinary | post_covid | 21.736 | 75.887 | 14.805 | 0.464 | 96.000 |
| gnn_multiedge_season | post_covid | 21.891 | 102.344 | 17.079 | 0.449 | 96.000 |
| gnn_multiedge_season_level | post_covid | 22.313 | 110.404 | 16.846 | 0.398 | 100.000 |
| gnn_multiedge_level | post_covid | 23.151 | 68.431 | 13.295 | 0.393 | 100.000 |
| dualtopo | post_covid | 24.349 | 110.175 | 16.289 | -0.707 | 84.000 |
| dualtopo_no_bg | post_covid | 24.362 | 109.386 | 16.253 | -0.179 | 84.000 |
| gnn_multiedge | post_covid | 24.432 | 70.675 | 15.858 | 0.271 | 100.000 |
| arima | post_covid | 24.731 | 118.494 | 17.432 | -0.062 | 100.000 |
| gnn_multiedge_rt | post_covid | 25.092 | 151.791 | 21.780 | 0.407 | 100.000 |
| gnn_geo | post_covid | 25.173 | 70.614 | 16.072 | 0.239 | 100.000 |
| gnn_multiedge_full | full | 26.037 | 67.412 | 16.612 | 0.328 | 92.000 |
| gnn_uniform | post_covid | 26.452 | 72.368 | 17.123 | 0.098 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 26.493 | 56.304 | 15.735 | 0.461 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 27.785 | 229.599 | 24.791 | 0.349 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 27.791 | 107.791 | 21.029 | 0.069 | 100.000 |
| dualtopo_fullhistory | full | 30.351 | 120.282 | 22.453 | -0.236 | 84.000 |
| lstm | exclude_covid | 31.135 | 156.426 | 25.050 | -0.130 | 88.000 |
| lstm | post_covid | 31.737 | 140.832 | 23.375 | -0.094 | 76.000 |
| arima | exclude_covid | 33.158 | 134.750 | 22.672 | -0.119 | 88.000 |
| persistence | exclude_covid | 37.163 | 99.971 | 24.660 | -0.064 | 100.000 |
| persistence | post_covid | 37.163 | 99.971 | 24.660 | -0.064 | 100.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 4.996 | 124.861 | 4.283 | 0.684 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| gnn_multiedge_level | post_covid | 7.498 | 195.034 | 6.610 | 0.638 | 100.000 |
| gnn_geo | post_covid | 8.514 | 189.955 | 6.504 | -0.135 | 100.000 |
| gnn_multiedge_season | post_covid | 8.558 | 130.210 | 7.176 | -0.419 | 61.905 |
| gnn_multiedge_covid_rsv_full | full | 8.673 | 165.286 | 7.227 | -0.527 | 76.190 |
| gnn_multiedge_full | full | 8.801 | 171.600 | 7.553 | -0.545 | 76.190 |
| gnn_multiedge_rt | post_covid | 8.887 | 160.647 | 7.591 | -0.507 | 80.952 |
| gnn_corrbinary | post_covid | 9.071 | 210.745 | 7.386 | 0.066 | 100.000 |
| gnn_multiedge | post_covid | 9.692 | 200.960 | 8.037 | -0.474 | 100.000 |
| gnn_uniform | post_covid | 9.913 | 210.861 | 8.095 | -0.661 | 100.000 |
| dualtopo_fullhistory | full | 10.172 | 242.621 | 9.148 | 0.504 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.707 | 217.075 | 8.848 | -0.561 | 100.000 |
| persistence | exclude_covid | 12.072 | 247.053 | 9.352 | -0.179 | 100.000 |
| persistence | post_covid | 12.072 | 247.053 | 9.352 | -0.179 | 100.000 |
| lstm | exclude_covid | 12.349 | 239.901 | 9.986 | 0.440 | 100.000 |
| lstm | post_covid | 13.273 | 282.396 | 11.417 | 0.417 | 95.238 |
| dualtopo_no_bg | post_covid | 16.254 | 423.464 | 15.591 | 0.202 | 100.000 |
| dualtopo | post_covid | 16.381 | 426.523 | 15.723 | -0.021 | 100.000 |
| arima | exclude_covid | 16.561 | 370.069 | 14.336 | -0.193 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 17.105 | 367.021 | 14.222 | -0.256 | 76.190 |
| arima | post_covid | 17.544 | 454.406 | 16.823 | -0.199 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 14.171 | 97.222 | 9.241 | 0.639 | 81.633 |
| gnn_multiedge_season_level | post_covid | 14.237 | 88.111 | 8.374 | 0.661 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.979 | 118.671 | 11.027 | 0.607 | 87.755 |
| gnn_corrbinary | post_covid | 15.976 | 117.327 | 9.550 | 0.479 | 97.959 |
| gnn_multiedge_level | post_covid | 16.453 | 101.214 | 9.276 | 0.517 | 100.000 |
| gnn_geo | post_covid | 16.746 | 108.874 | 9.528 | 0.397 | 100.000 |
| gnn_multiedge | post_covid | 17.178 | 108.535 | 9.610 | 0.379 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 18.010 | 134.014 | 11.783 | 0.341 | 100.000 |
| gnn_multiedge_full | full | 18.073 | 99.441 | 10.501 | 0.352 | 91.837 |
| lstm | exclude_covid | 18.108 | 106.759 | 10.709 | 0.229 | 91.837 |
| gnn_uniform | post_covid | 18.204 | 108.852 | 10.230 | 0.294 | 100.000 |
| dualtopo_no_bg | post_covid | 18.258 | 189.721 | 12.798 | 0.217 | 89.796 |
| dualtopo | post_covid | 18.269 | 191.009 | 12.853 | -0.224 | 89.796 |
| dualtopo_fullhistory | full | 18.277 | 109.356 | 10.914 | 0.198 | 91.837 |
| arima | exclude_covid | 18.311 | 195.924 | 13.060 |  | 100.000 |
| arima | post_covid | 18.572 | 217.125 | 13.956 |  | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 18.792 | 90.876 | 10.392 | 0.295 | 97.959 |
| gnn_multiedge_covid_rsv | post_covid | 18.808 | 182.220 | 15.042 | 0.386 | 100.000 |
| lstm | post_covid | 19.592 | 178.006 | 13.519 | 0.159 | 89.796 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| persistence | exclude_covid | 24.349 | 158.676 | 15.161 | 0.099 | 100.000 |
| persistence | post_covid | 24.349 | 158.676 | 15.161 | 0.099 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 18.104 | 52.661 | 11.716 | 0.552 | 100.000 |
| gnn_multiedge_season_level | post_covid | 19.079 | 59.670 | 12.532 | 0.512 | 100.000 |
| gnn_multiedge_rt | post_covid | 19.566 | 83.529 | 15.750 | 0.457 | 100.000 |
| gnn_corrbinary | post_covid | 20.772 | 57.218 | 12.632 | 0.340 | 96.154 |
| arima | post_covid | 21.842 | 81.061 | 14.459 |  | 100.000 |
| gnn_multiedge_level | post_covid | 21.926 | 54.062 | 12.950 | 0.315 | 100.000 |
| arima | exclude_covid | 22.199 | 73.070 | 14.110 |  | 100.000 |
| gnn_geo | post_covid | 22.201 | 54.297 | 13.726 | 0.165 | 100.000 |
| dualtopo | post_covid | 22.296 | 71.223 | 14.029 | -0.637 | 80.769 |
| dualtopo_no_bg | post_covid | 22.322 | 70.741 | 14.008 | -0.132 | 80.769 |
| gnn_multiedge | post_covid | 22.639 | 50.127 | 13.161 | 0.192 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 23.253 | 71.234 | 15.783 | 0.119 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 23.296 | 150.529 | 19.488 | 0.189 | 100.000 |
| gnn_multiedge_full | full | 23.935 | 50.512 | 14.799 | 0.203 | 100.000 |
| gnn_uniform | post_covid | 23.959 | 45.363 | 13.980 | 0.109 | 100.000 |
| lstm | exclude_covid | 24.140 | 65.718 | 15.345 | -0.055 | 84.615 |
| dualtopo_fullhistory | full | 24.448 | 64.046 | 15.842 | -0.055 | 84.615 |
| lstm | post_covid | 24.851 | 88.671 | 16.991 | -0.046 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 25.051 | 51.084 | 15.110 | 0.146 | 96.154 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |
| persistence | exclude_covid | 31.748 | 73.860 | 21.212 | 0.015 | 100.000 |
| persistence | post_covid | 31.748 | 73.860 | 21.212 | 0.015 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 4.504 | 120.262 | 3.673 | 0.536 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| gnn_multiedge_level | post_covid | 5.771 | 154.516 | 5.122 | 0.562 | 100.000 |
| dualtopo_fullhistory | full | 6.000 | 160.577 | 5.343 | 0.662 | 100.000 |
| lstm | exclude_covid | 6.308 | 153.153 | 5.469 | 0.472 | 100.000 |
| gnn_geo | post_covid | 6.346 | 170.569 | 4.782 | 0.324 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.556 | 135.857 | 5.059 | -0.265 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.728 | 158.397 | 5.687 | -0.117 | 73.913 |
| gnn_multiedge_full | full | 6.949 | 154.754 | 5.643 | -0.254 | 82.609 |
| gnn_multiedge | post_covid | 7.021 | 174.561 | 5.595 | 0.027 | 100.000 |
| gnn_corrbinary | post_covid | 7.485 | 185.277 | 6.067 | 0.544 | 100.000 |
| gnn_uniform | post_covid | 7.555 | 180.621 | 5.992 | -0.317 | 100.000 |
| gnn_multiedge_season | post_covid | 7.572 | 147.594 | 6.443 | -0.473 | 60.870 |
| gnn_multiedge_leaknorm | post_covid | 8.933 | 204.982 | 7.261 | -0.450 | 100.000 |
| lstm | post_covid | 10.938 | 278.994 | 9.594 | 0.253 | 100.000 |
| persistence | exclude_covid | 11.120 | 254.555 | 8.322 | 0.243 | 100.000 |
| persistence | post_covid | 11.120 | 254.555 | 8.322 | 0.243 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.836 | 218.044 | 10.017 | -0.175 | 100.000 |
| dualtopo_no_bg | post_covid | 12.121 | 324.221 | 11.430 | -0.202 | 100.000 |
| dualtopo | post_covid | 12.208 | 326.420 | 11.522 | -0.068 | 100.000 |
| arima | exclude_covid | 12.540 | 334.801 | 11.874 |  | 100.000 |
| arima | post_covid | 13.982 | 370.937 | 13.387 |  | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 16.286 | 59.873 | 8.421 | 0.604 | 95.000 |
| gnn_multiedge_season | post_covid | 17.359 | 82.286 | 10.716 | 0.468 | 87.500 |
| gnn_multiedge_rt | post_covid | 17.716 | 92.888 | 11.502 | 0.429 | 95.000 |
| gnn_multiedge_level | post_covid | 19.007 | 63.994 | 9.069 | 0.367 | 100.000 |
| gnn_geo | post_covid | 19.231 | 79.680 | 10.599 | 0.224 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 19.242 | 162.750 | 14.933 | 0.329 | 100.000 |
| arima | post_covid | 19.303 | 130.525 | 11.866 |  | 100.000 |
| dualtopo | post_covid | 19.305 | 109.551 | 10.771 | -0.409 | 92.500 |
| dualtopo_no_bg | post_covid | 19.308 | 108.644 | 10.728 | 0.125 | 92.500 |
| arima | exclude_covid | 19.334 | 136.544 | 12.181 |  | 95.000 |
| gnn_multiedge_leaknorm | post_covid | 19.560 | 96.613 | 12.339 | 0.247 | 100.000 |
| gnn_corrbinary | post_covid | 19.975 | 104.181 | 12.210 | 0.207 | 95.000 |
| gnn_multiedge_full | full | 20.035 | 86.488 | 11.904 | 0.217 | 85.000 |
| gnn_multiedge | post_covid | 20.324 | 92.846 | 11.919 | 0.168 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 20.672 | 85.146 | 12.179 | 0.173 | 95.000 |
| dualtopo_fullhistory | full | 20.684 | 90.438 | 11.761 | 0.018 | 90.000 |
| lstm | post_covid | 20.724 | 103.701 | 12.246 | 0.056 | 90.000 |
| lstm | exclude_covid | 20.782 | 89.264 | 11.850 | 0.065 | 90.000 |
| gnn_uniform | post_covid | 20.979 | 89.606 | 12.146 | 0.140 | 100.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| persistence | exclude_covid | 25.928 | 109.133 | 14.745 | -0.027 | 100.000 |
| persistence | post_covid | 25.928 | 109.133 | 14.745 | -0.027 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 20.391 | 60.466 | 11.458 | 0.549 | 92.000 |
| gnn_multiedge_season | post_covid | 21.128 | 78.083 | 13.289 | 0.388 | 100.000 |
| gnn_multiedge_rt | post_covid | 21.695 | 91.173 | 14.620 | 0.335 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 22.975 | 171.525 | 18.487 | 0.234 | 100.000 |
| arima | exclude_covid | 23.074 | 94.527 | 13.634 |  | 92.000 |
| arima | post_covid | 23.161 | 90.530 | 13.445 |  | 100.000 |
| dualtopo | post_covid | 23.554 | 76.604 | 12.789 | -0.634 | 88.000 |
| dualtopo_no_bg | post_covid | 23.574 | 76.031 | 12.767 | -0.157 | 88.000 |
| gnn_multiedge_level | post_covid | 23.862 | 60.395 | 12.508 | 0.257 | 100.000 |
| gnn_geo | post_covid | 23.929 | 72.763 | 14.260 | 0.121 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 24.020 | 85.360 | 15.846 | 0.124 | 100.000 |
| gnn_corrbinary | post_covid | 24.377 | 87.960 | 15.504 | 0.158 | 92.000 |
| gnn_multiedge_full | full | 24.658 | 78.182 | 15.308 | 0.137 | 92.000 |
| gnn_multiedge | post_covid | 25.141 | 81.960 | 15.507 | 0.084 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 25.541 | 78.403 | 15.883 | 0.097 | 92.000 |
| lstm | post_covid | 25.632 | 96.851 | 16.163 | -0.072 | 84.000 |
| dualtopo_fullhistory | full | 25.725 | 80.488 | 15.777 | -0.112 | 84.000 |
| lstm | exclude_covid | 25.834 | 91.269 | 16.265 | -0.094 | 84.000 |
| gnn_uniform | post_covid | 25.890 | 79.202 | 15.551 | 0.030 | 100.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| persistence | exclude_covid | 32.145 | 90.836 | 19.644 | -0.058 | 100.000 |
| persistence | post_covid | 32.145 | 90.836 | 19.644 | -0.058 | 100.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.774 | 58.884 | 3.359 | 0.268 | 100.000 |
| gnn_multiedge_level | post_covid | 3.786 | 69.992 | 3.337 | 0.509 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| gnn_geo | post_covid | 5.648 | 91.208 | 4.498 | 0.282 | 100.000 |
| dualtopo_fullhistory | full | 6.156 | 107.021 | 5.068 | 0.204 | 100.000 |
| lstm | exclude_covid | 6.273 | 85.921 | 4.491 | 0.327 | 100.000 |
| gnn_multiedge | post_covid | 6.932 | 110.989 | 5.940 | -0.137 | 100.000 |
| lstm | post_covid | 7.094 | 115.117 | 5.718 | 0.445 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.234 | 96.383 | 6.005 | -0.196 | 100.000 |
| gnn_multiedge_rt | post_covid | 7.245 | 95.745 | 6.304 | -0.466 | 86.667 |
| gnn_uniform | post_covid | 7.513 | 106.944 | 6.470 | -0.320 | 100.000 |
| gnn_multiedge_full | full | 7.553 | 100.333 | 6.231 | -0.327 | 73.333 |
| gnn_multiedge_leaknorm | post_covid | 7.660 | 115.368 | 6.495 | -0.331 | 100.000 |
| gnn_multiedge_season | post_covid | 7.718 | 89.290 | 6.428 | -0.358 | 66.667 |
| dualtopo_no_bg | post_covid | 8.242 | 162.999 | 7.330 | 0.231 | 100.000 |
| dualtopo | post_covid | 8.316 | 164.462 | 7.409 | 0.141 | 100.000 |
| persistence | exclude_covid | 8.401 | 139.627 | 6.580 | -0.113 | 100.000 |
| persistence | post_covid | 8.401 | 139.627 | 6.580 | -0.113 | 100.000 |
| gnn_corrbinary | post_covid | 8.575 | 131.217 | 6.720 | 0.141 | 100.000 |
| arima | post_covid | 9.977 | 197.185 | 9.235 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.375 | 148.126 | 9.009 | -0.031 | 100.000 |
| arima | exclude_covid | 10.464 | 206.573 | 9.758 |  | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 10.364 | 89.537 | 6.890 | 0.643 | 80.952 |
| gnn_multiedge_season_level | post_covid | 10.481 | 84.785 | 6.195 | 0.630 | 97.619 |
| gnn_multiedge_rt | post_covid | 11.783 | 106.792 | 8.078 | 0.569 | 92.857 |
| gnn_multiedge_level | post_covid | 12.142 | 92.602 | 7.000 | 0.497 | 100.000 |
| gnn_corrbinary | post_covid | 12.909 | 118.292 | 8.587 | 0.342 | 95.238 |
| gnn_multiedge | post_covid | 12.927 | 92.343 | 7.739 | 0.343 | 100.000 |
| gnn_geo | post_covid | 12.967 | 88.937 | 7.953 | 0.312 | 100.000 |
| dualtopo_no_bg | post_covid | 13.202 | 180.704 | 9.319 | 0.198 | 90.476 |
| dualtopo | post_covid | 13.208 | 182.194 | 9.359 | -0.407 | 90.476 |
| arima | post_covid | 13.427 | 213.945 | 10.200 |  | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 13.472 | 107.297 | 9.169 | 0.340 | 100.000 |
| gnn_multiedge_full | full | 13.611 | 93.640 | 8.704 | 0.391 | 85.714 |
| gnn_uniform | post_covid | 13.987 | 92.962 | 8.687 | 0.238 | 100.000 |
| dualtopo_fullhistory | full | 14.105 | 136.100 | 9.870 | 0.087 | 90.476 |
| gnn_multiedge_covid_rsv_full | full | 14.390 | 92.342 | 9.212 | 0.304 | 100.000 |
| arima | exclude_covid | 14.654 | 133.831 | 9.948 | 0.226 | 97.619 |
| lstm | exclude_covid | 14.859 | 145.541 | 10.900 | 0.207 | 90.476 |
| gnn_multiedge_covid_rsv | post_covid | 15.061 | 237.259 | 11.270 | 0.324 | 100.000 |
| lstm | post_covid | 15.183 | 150.031 | 10.899 | 0.128 | 88.095 |
| persistence | exclude_covid | 18.732 | 128.210 | 12.424 | 0.019 | 100.000 |
| persistence | post_covid | 18.732 | 128.210 | 12.424 | 0.019 | 100.000 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 12.704 | 88.498 | 8.717 | 0.556 | 100.000 |
| gnn_multiedge_season_level | post_covid | 13.333 | 91.560 | 8.673 | 0.507 | 96.000 |
| gnn_multiedge_rt | post_covid | 14.747 | 123.559 | 11.156 | 0.416 | 100.000 |
| arima | post_covid | 15.261 | 153.984 | 10.523 |  | 100.000 |
| gnn_multiedge_level | post_covid | 15.450 | 88.675 | 9.477 | 0.333 | 100.000 |
| dualtopo | post_covid | 15.631 | 133.842 | 10.311 | -0.684 | 84.000 |
| dualtopo_no_bg | post_covid | 15.652 | 132.899 | 10.301 | -0.069 | 84.000 |
| gnn_corrbinary | post_covid | 15.971 | 122.231 | 11.302 | 0.207 | 96.000 |
| gnn_geo | post_covid | 16.448 | 99.572 | 11.275 | 0.092 | 100.000 |
| gnn_multiedge | post_covid | 16.487 | 99.458 | 11.072 | 0.122 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 16.896 | 109.551 | 12.758 | 0.122 | 100.000 |
| gnn_multiedge_full | full | 17.148 | 102.025 | 12.112 | 0.220 | 88.000 |
| dualtopo_fullhistory | full | 17.596 | 111.526 | 12.863 | -0.111 | 84.000 |
| arima | exclude_covid | 17.608 | 76.364 | 11.901 | 0.200 | 96.000 |
| gnn_uniform | post_covid | 17.687 | 98.901 | 12.123 | 0.023 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 18.249 | 108.105 | 13.178 | 0.133 | 100.000 |
| lstm | exclude_covid | 18.279 | 138.439 | 14.454 | -0.020 | 84.000 |
| gnn_multiedge_covid_rsv | post_covid | 18.352 | 312.085 | 14.888 | 0.101 | 100.000 |
| lstm | post_covid | 18.642 | 122.413 | 13.867 | -0.031 | 84.000 |
| persistence | exclude_covid | 23.331 | 98.232 | 16.900 | -0.055 | 100.000 |
| persistence | post_covid | 23.331 | 98.232 | 16.900 | -0.055 | 100.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.156 | 74.822 | 2.552 | 0.285 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| gnn_multiedge | post_covid | 3.622 | 81.879 | 2.836 | 0.339 | 100.000 |
| gnn_multiedge_level | post_covid | 3.633 | 98.377 | 3.358 | 0.482 | 100.000 |
| gnn_geo | post_covid | 4.193 | 73.296 | 3.066 | 0.463 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.675 | 69.161 | 3.380 | -0.107 | 100.000 |
| gnn_multiedge_rt | post_covid | 4.819 | 82.134 | 3.552 | -0.183 | 82.353 |
| gnn_uniform | post_covid | 4.827 | 84.227 | 3.635 | -0.336 | 100.000 |
| gnn_multiedge_full | full | 5.025 | 81.309 | 3.692 | -0.199 | 82.353 |
| gnn_multiedge_season | post_covid | 5.298 | 91.065 | 4.203 | -0.293 | 52.941 |
| gnn_multiedge_leaknorm | post_covid | 5.345 | 103.983 | 3.891 | -0.343 | 100.000 |
| dualtopo_fullhistory | full | 6.016 | 172.239 | 5.469 | 0.317 | 100.000 |
| gnn_corrbinary | post_covid | 6.051 | 112.501 | 4.594 | 0.554 | 94.118 |
| lstm | exclude_covid | 7.356 | 155.985 | 5.673 | 0.121 | 100.000 |
| lstm | post_covid | 7.645 | 190.644 | 6.535 | 0.171 | 94.118 |
| gnn_multiedge_covid_rsv | post_covid | 8.070 | 127.222 | 5.949 | 0.114 | 100.000 |
| persistence | exclude_covid | 8.150 | 172.294 | 5.841 | 0.080 | 100.000 |
| persistence | post_covid | 8.150 | 172.294 | 5.841 | 0.080 | 100.000 |
| dualtopo_no_bg | post_covid | 8.388 | 251.006 | 7.875 | -0.289 | 100.000 |
| dualtopo | post_covid | 8.466 | 253.299 | 7.958 | -0.254 | 100.000 |
| arima | exclude_covid | 8.636 | 218.343 | 7.075 | -0.013 | 100.000 |
| arima | post_covid | 10.145 | 302.122 | 9.725 |  | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 9.769 | 80.574 | 5.777 | 0.671 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.567 | 106.777 | 7.132 | 0.566 | 93.478 |
| gnn_multiedge_season | post_covid | 11.103 | 100.828 | 7.435 | 0.531 | 82.609 |
| gnn_multiedge_level | post_covid | 11.919 | 97.753 | 6.981 | 0.443 | 100.000 |
| gnn_geo | post_covid | 12.430 | 111.292 | 7.857 | 0.293 | 100.000 |
| dualtopo_no_bg | post_covid | 12.445 | 187.855 | 8.417 | 0.232 | 91.304 |
| dualtopo | post_covid | 12.446 | 189.175 | 8.437 | -0.259 | 93.478 |
| arima | post_covid | 12.567 | 220.549 | 9.075 |  | 100.000 |
| arima | exclude_covid | 12.623 | 227.615 | 9.220 |  | 100.000 |
| gnn_corrbinary | post_covid | 12.790 | 127.110 | 8.198 | 0.272 | 95.652 |
| lstm | exclude_covid | 12.912 | 125.993 | 8.641 | 0.271 | 95.652 |
| dualtopo_fullhistory | full | 12.954 | 137.049 | 8.747 | 0.194 | 93.478 |
| gnn_multiedge | post_covid | 13.189 | 114.596 | 8.257 | 0.211 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 13.243 | 137.633 | 8.880 | 0.284 | 100.000 |
| lstm | post_covid | 13.301 | 144.799 | 8.914 | 0.207 | 91.304 |
| gnn_multiedge_full | full | 13.308 | 104.682 | 8.749 | 0.256 | 91.304 |
| gnn_uniform | post_covid | 13.568 | 117.158 | 8.612 | 0.181 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.809 | 205.045 | 10.834 | 0.279 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 14.033 | 98.871 | 8.898 | 0.166 | 95.652 |
| persistence | exclude_covid | 17.653 | 152.287 | 11.530 | 0.016 | 97.826 |
| persistence | post_covid | 17.653 | 152.287 | 11.530 | 0.016 | 97.826 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 12.722 | 60.681 | 8.168 | 0.514 | 100.000 |
| gnn_multiedge_rt | post_covid | 13.036 | 73.545 | 9.056 | 0.390 | 100.000 |
| gnn_multiedge_season | post_covid | 13.761 | 69.764 | 9.452 | 0.355 | 100.000 |
| arima | exclude_covid | 14.320 | 90.559 | 9.048 |  | 100.000 |
| arima | post_covid | 14.416 | 88.364 | 9.077 |  | 100.000 |
| dualtopo | post_covid | 14.945 | 78.687 | 9.213 | -0.608 | 88.462 |
| dualtopo_no_bg | post_covid | 14.972 | 78.393 | 9.235 | -0.158 | 84.615 |
| gnn_multiedge_level | post_covid | 15.547 | 66.848 | 9.994 | 0.187 | 100.000 |
| gnn_corrbinary | post_covid | 15.561 | 73.291 | 10.064 | 0.120 | 96.154 |
| gnn_geo | post_covid | 15.894 | 77.866 | 10.729 | 0.058 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 16.409 | 84.381 | 11.423 | 0.066 | 100.000 |
| lstm | exclude_covid | 16.497 | 88.174 | 11.765 | 0.020 | 92.308 |
| dualtopo_fullhistory | full | 16.526 | 81.673 | 11.700 | -0.021 | 88.462 |
| lstm | post_covid | 16.702 | 80.075 | 11.502 | 0.021 | 84.615 |
| gnn_multiedge | post_covid | 16.886 | 77.266 | 11.462 | 0.001 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 16.905 | 172.993 | 13.720 | -0.001 | 100.000 |
| gnn_multiedge_full | full | 16.998 | 76.369 | 12.103 | 0.059 | 92.308 |
| gnn_uniform | post_covid | 17.218 | 72.841 | 11.494 | -0.030 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 18.046 | 72.329 | 12.412 | -0.026 | 96.154 |
| persistence | exclude_covid | 22.153 | 85.237 | 15.265 | -0.065 | 96.154 |
| persistence | post_covid | 22.153 | 85.237 | 15.265 | -0.065 | 96.154 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.012 | 106.434 | 2.669 | 0.495 | 100.000 |
| gnn_multiedge_level | post_covid | 3.536 | 137.930 | 3.064 | 0.554 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| gnn_geo | post_covid | 5.192 | 154.746 | 4.122 | 0.342 | 100.000 |
| gnn_multiedge | post_covid | 5.420 | 163.124 | 4.091 | -0.020 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.437 | 133.374 | 4.329 | -0.458 | 95.000 |
| lstm | exclude_covid | 5.446 | 175.157 | 4.578 | 0.457 | 100.000 |
| dualtopo_fullhistory | full | 5.561 | 209.039 | 4.908 | 0.488 | 100.000 |
| gnn_multiedge_full | full | 5.632 | 141.488 | 4.388 | -0.446 | 90.000 |
| gnn_multiedge_rt | post_covid | 5.991 | 149.978 | 4.631 | -0.426 | 85.000 |
| gnn_multiedge_season | post_covid | 6.115 | 141.211 | 4.814 | -0.434 | 60.000 |
| gnn_uniform | post_covid | 6.168 | 174.770 | 4.865 | -0.471 | 100.000 |
| lstm | post_covid | 6.653 | 228.940 | 5.549 | 0.350 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 7.301 | 206.861 | 5.574 | -0.494 | 100.000 |
| gnn_corrbinary | post_covid | 7.840 | 197.074 | 5.773 | 0.396 | 95.000 |
| dualtopo_no_bg | post_covid | 8.050 | 330.155 | 7.354 | 0.061 | 100.000 |
| dualtopo | post_covid | 8.118 | 332.811 | 7.427 | 0.144 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.192 | 246.711 | 7.082 | -0.243 | 100.000 |
| persistence | exclude_covid | 8.874 | 239.452 | 6.675 | 0.207 | 100.000 |
| persistence | post_covid | 8.874 | 239.452 | 6.675 | 0.207 | 100.000 |
| arima | post_covid | 9.646 | 392.388 | 9.073 |  | 100.000 |
| arima | exclude_covid | 9.995 | 405.787 | 9.443 |  | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 10.098 | 109.855 | 6.700 | 0.648 | 100.000 |
| gnn_multiedge_season | post_covid | 11.455 | 135.165 | 7.712 | 0.529 | 77.273 |
| gnn_multiedge_level | post_covid | 12.158 | 127.344 | 7.748 | 0.433 | 100.000 |
| dualtopo_fullhistory | full | 12.442 | 149.032 | 8.432 | 0.311 | 93.182 |
| gnn_multiedge_rt | post_covid | 12.798 | 183.237 | 8.936 | 0.429 | 90.909 |
| dualtopo_no_bg | post_covid | 12.965 | 206.974 | 9.343 | 0.198 | 88.636 |
| dualtopo | post_covid | 12.971 | 208.482 | 9.372 | -0.310 | 88.636 |
| arima | exclude_covid | 13.143 | 234.064 | 9.852 |  | 100.000 |
| arima | post_covid | 13.237 | 243.872 | 10.104 |  | 100.000 |
| gnn_corrbinary | post_covid | 13.456 | 174.176 | 8.714 | 0.235 | 93.182 |
| gnn_multiedge | post_covid | 13.572 | 155.967 | 8.318 | 0.178 | 100.000 |
| gnn_geo | post_covid | 13.939 | 131.097 | 8.457 | 0.123 | 100.000 |
| lstm | exclude_covid | 14.047 | 178.592 | 9.589 | 0.169 | 90.909 |
| gnn_multiedge_covid_rsv | post_covid | 14.103 | 242.778 | 11.225 | 0.338 | 100.000 |
| gnn_multiedge_full | full | 14.112 | 131.775 | 8.981 | 0.168 | 84.091 |
| gnn_multiedge_leaknorm | post_covid | 14.227 | 166.223 | 9.451 | 0.196 | 100.000 |
| gnn_uniform | post_covid | 14.479 | 151.270 | 8.920 | 0.086 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 14.710 | 136.314 | 9.445 | 0.079 | 100.000 |
| lstm | post_covid | 14.922 | 207.120 | 10.363 | 0.122 | 88.636 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| persistence | exclude_covid | 19.196 | 206.114 | 12.186 | -0.073 | 93.182 |
| persistence | post_covid | 19.196 | 206.114 | 12.186 | -0.073 | 97.727 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 13.111 | 120.325 | 9.782 | 0.515 | 100.000 |
| gnn_multiedge_season | post_covid | 14.307 | 150.514 | 10.063 | 0.362 | 100.000 |
| arima | post_covid | 15.108 | 150.524 | 10.374 |  | 100.000 |
| arima | exclude_covid | 15.191 | 144.963 | 10.290 |  | 100.000 |
| dualtopo | post_covid | 15.497 | 131.633 | 10.343 | -0.640 | 80.000 |
| dualtopo_no_bg | post_covid | 15.517 | 130.849 | 10.346 | -0.093 | 80.000 |
| gnn_multiedge_level | post_covid | 15.713 | 115.277 | 10.944 | 0.245 | 100.000 |
| dualtopo_fullhistory | full | 15.993 | 142.127 | 11.662 | 0.041 | 88.000 |
| gnn_multiedge_rt | post_covid | 16.278 | 238.256 | 12.567 | 0.180 | 100.000 |
| gnn_corrbinary | post_covid | 16.671 | 179.674 | 11.165 | 0.093 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 17.173 | 264.786 | 14.453 | 0.161 | 100.000 |
| gnn_multiedge | post_covid | 17.457 | 163.042 | 11.516 | -0.046 | 100.000 |
| lstm | exclude_covid | 17.837 | 174.951 | 13.306 | -0.113 | 84.000 |
| gnn_geo | post_covid | 17.879 | 153.701 | 12.022 | -0.131 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 18.050 | 184.247 | 13.100 | -0.067 | 100.000 |
| gnn_multiedge_full | full | 18.051 | 137.660 | 12.598 | 0.000 | 88.000 |
| gnn_uniform | post_covid | 18.575 | 172.186 | 12.464 | -0.165 | 100.000 |
| lstm | post_covid | 18.711 | 180.066 | 13.637 | -0.103 | 80.000 |
| gnn_multiedge_covid_rsv_full | full | 18.940 | 152.773 | 13.470 | -0.117 | 100.000 |
| persistence | exclude_covid | 24.253 | 233.430 | 17.212 | -0.187 | 88.000 |
| persistence | post_covid | 24.253 | 233.430 | 17.212 | -0.187 | 96.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.155 | 96.078 | 2.646 | 0.446 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gnn_multiedge_level | post_covid | 4.179 | 143.221 | 3.544 | 0.340 | 100.000 |
| dualtopo_fullhistory | full | 4.683 | 158.117 | 4.180 | 0.561 | 100.000 |
| gnn_multiedge | post_covid | 5.060 | 146.657 | 4.110 | 0.111 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.394 | 114.656 | 4.150 | -0.436 | 100.000 |
| gnn_geo | post_covid | 5.418 | 101.355 | 3.766 | 0.486 | 100.000 |
| gnn_multiedge_rt | post_covid | 5.535 | 110.843 | 4.159 | -0.306 | 78.947 |
| gnn_uniform | post_covid | 5.613 | 123.748 | 4.256 | -0.479 | 100.000 |
| gnn_multiedge_full | full | 5.698 | 124.032 | 4.221 | -0.436 | 78.947 |
| gnn_multiedge_season | post_covid | 5.876 | 114.970 | 4.617 | -0.416 | 47.368 |
| lstm | exclude_covid | 6.193 | 183.382 | 4.699 | 0.291 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 6.327 | 142.507 | 4.649 | -0.432 | 100.000 |
| gnn_corrbinary | post_covid | 7.324 | 166.942 | 5.491 | 0.552 | 89.474 |
| lstm | post_covid | 7.414 | 242.717 | 6.055 | 0.228 | 100.000 |
| dualtopo_no_bg | post_covid | 8.509 | 307.139 | 8.024 | -0.295 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.518 | 213.821 | 6.977 | -0.271 | 100.000 |
| dualtopo | post_covid | 8.581 | 309.600 | 8.094 | -0.184 | 100.000 |
| persistence | exclude_covid | 8.910 | 170.171 | 5.574 | 0.323 | 100.000 |
| persistence | post_covid | 8.910 | 170.171 | 5.574 | 0.323 | 100.000 |
| arima | exclude_covid | 9.817 | 351.302 | 9.275 |  | 100.000 |
| arima | post_covid | 10.269 | 366.700 | 9.748 |  | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 11.189 | 121.277 | 7.051 | 0.629 | 100.000 |
| gnn_multiedge_season | post_covid | 12.210 | 91.856 | 7.864 | 0.498 | 84.783 |
| gnn_multiedge_level | post_covid | 12.496 | 129.910 | 7.369 | 0.523 | 100.000 |
| gnn_multiedge_rt | post_covid | 13.528 | 126.961 | 9.247 | 0.437 | 89.130 |
| gnn_multiedge_covid_rsv | post_covid | 13.654 | 234.969 | 10.438 | 0.400 | 100.000 |
| dualtopo_no_bg | post_covid | 13.860 | 222.789 | 9.807 | 0.190 | 89.130 |
| dualtopo | post_covid | 13.869 | 224.228 | 9.843 | -0.333 | 89.130 |
| arima | post_covid | 14.128 | 257.549 | 10.712 |  | 100.000 |
| arima | exclude_covid | 14.241 | 268.169 | 10.999 |  | 100.000 |
| gnn_geo | post_covid | 14.346 | 109.737 | 8.770 | 0.164 | 100.000 |
| gnn_corrbinary | post_covid | 14.356 | 125.435 | 9.149 | 0.226 | 95.652 |
| dualtopo_fullhistory | full | 14.389 | 169.317 | 10.000 | 0.084 | 91.304 |
| gnn_multiedge_full | full | 14.441 | 96.196 | 8.181 | 0.205 | 93.478 |
| gnn_multiedge | post_covid | 14.713 | 111.974 | 8.906 | 0.149 | 100.000 |
| lstm | exclude_covid | 14.832 | 178.352 | 10.576 | 0.128 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 14.896 | 133.225 | 9.807 | 0.208 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 15.122 | 97.700 | 8.737 | 0.109 | 93.478 |
| lstm | post_covid | 15.178 | 192.066 | 10.847 | 0.065 | 89.130 |
| gnn_uniform | post_covid | 15.675 | 111.569 | 9.632 | 0.073 | 100.000 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| persistence | exclude_covid | 20.168 | 134.610 | 12.626 | -0.055 | 93.478 |
| persistence | post_covid | 20.168 | 134.610 | 12.626 | -0.055 | 95.652 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 15.172 | 125.773 | 11.045 | 0.474 | 100.000 |
| gnn_multiedge_season | post_covid | 16.404 | 117.800 | 12.330 | 0.254 | 100.000 |
| gnn_multiedge_level | post_covid | 16.746 | 104.285 | 10.521 | 0.353 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 16.807 | 246.449 | 13.246 | 0.251 | 100.000 |
| arima | exclude_covid | 16.851 | 159.552 | 11.576 |  | 100.000 |
| arima | post_covid | 16.928 | 153.595 | 11.458 |  | 100.000 |
| dualtopo | post_covid | 17.254 | 135.322 | 11.163 | -0.681 | 79.167 |
| dualtopo_no_bg | post_covid | 17.271 | 134.549 | 11.153 | -0.201 | 79.167 |
| gnn_multiedge_rt | post_covid | 18.342 | 169.478 | 14.953 | 0.146 | 100.000 |
| gnn_corrbinary | post_covid | 19.119 | 134.611 | 14.003 | 0.024 | 95.833 |
| dualtopo_fullhistory | full | 19.153 | 137.400 | 14.283 | -0.201 | 83.333 |
| gnn_geo | post_covid | 19.283 | 112.054 | 13.574 | -0.123 | 100.000 |
| gnn_multiedge_full | full | 19.462 | 90.508 | 12.268 | -0.052 | 100.000 |
| lstm | exclude_covid | 19.514 | 157.337 | 15.239 | -0.164 | 83.333 |
| lstm | post_covid | 19.758 | 147.843 | 14.751 | -0.135 | 79.167 |
| gnn_multiedge | post_covid | 19.874 | 120.517 | 13.900 | -0.113 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 20.104 | 147.452 | 15.206 | -0.117 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 20.437 | 100.460 | 13.541 | -0.095 | 87.500 |
| gnn_uniform | post_covid | 21.168 | 114.356 | 14.867 | -0.167 | 100.000 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| persistence | exclude_covid | 26.955 | 127.933 | 19.808 | -0.189 | 87.500 |
| persistence | post_covid | 26.955 | 127.933 | 19.808 | -0.189 | 91.667 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.266 | 116.371 | 2.695 | 0.650 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gnn_multiedge_rt | post_covid | 3.955 | 80.579 | 3.023 | 0.059 | 77.273 |
| gnn_multiedge_season | post_covid | 4.262 | 63.552 | 2.993 | -0.297 | 68.182 |
| gnn_multiedge_level | post_covid | 4.536 | 157.864 | 3.930 | 0.442 | 100.000 |
| gnn_multiedge | post_covid | 4.659 | 102.654 | 3.457 | 0.068 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.742 | 94.690 | 3.495 | -0.373 | 100.000 |
| gnn_multiedge_full | full | 4.780 | 102.401 | 3.723 | -0.346 | 86.364 |
| gnn_multiedge_leaknorm | post_covid | 4.802 | 117.705 | 3.917 | -0.285 | 100.000 |
| gnn_geo | post_covid | 4.967 | 107.210 | 3.530 | 0.406 | 100.000 |
| gnn_uniform | post_covid | 4.994 | 108.528 | 3.921 | -0.376 | 100.000 |
| gnn_corrbinary | post_covid | 5.671 | 115.423 | 3.854 | 0.591 | 95.455 |
| dualtopo_fullhistory | full | 5.722 | 204.135 | 5.327 | 0.610 | 100.000 |
| lstm | exclude_covid | 6.676 | 201.277 | 5.490 | 0.278 | 100.000 |
| lstm | post_covid | 7.472 | 240.309 | 6.589 | 0.413 | 100.000 |
| persistence | exclude_covid | 7.603 | 141.894 | 4.791 | 0.302 | 100.000 |
| persistence | post_covid | 7.603 | 141.894 | 4.791 | 0.302 | 100.000 |
| dualtopo_no_bg | post_covid | 8.735 | 319.051 | 8.338 | -0.082 | 100.000 |
| dualtopo | post_covid | 8.797 | 321.216 | 8.403 | -0.259 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.038 | 222.445 | 7.374 | -0.259 | 100.000 |
| arima | post_covid | 10.234 | 370.952 | 9.897 |  | 100.000 |
| arima | exclude_covid | 10.691 | 386.661 | 10.369 |  | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 3.925 | 88.571 | 2.967 | 0.717 | 100.000 |
| gnn_multiedge_season | post_covid | 4.602 | 61.836 | 3.311 | 0.652 | 76.744 |
| gnn_multiedge_rt | post_covid | 4.796 | 74.371 | 3.442 | 0.612 | 90.698 |
| gnn_multiedge_level | post_covid | 4.844 | 109.524 | 3.827 | 0.525 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.573 | 86.085 | 4.245 | 0.434 | 100.000 |
| dualtopo_fullhistory | full | 5.602 | 122.420 | 4.420 | 0.352 | 100.000 |
| dualtopo_no_bg | post_covid | 5.713 | 171.849 | 4.911 | 0.513 | 100.000 |
| dualtopo | post_covid | 5.727 | 172.886 | 4.926 | -0.086 | 100.000 |
| gnn_uniform | post_covid | 5.841 | 81.634 | 4.268 | 0.330 | 100.000 |
| gnn_multiedge | post_covid | 5.897 | 99.744 | 4.309 | 0.180 | 100.000 |
| gnn_geo | post_covid | 5.959 | 113.711 | 4.461 | 0.253 | 100.000 |
| gnn_multiedge_full | full | 6.043 | 80.736 | 4.469 | 0.366 | 86.047 |
| arima | post_covid | 6.091 | 196.525 | 5.335 |  | 100.000 |
| arima | exclude_covid | 6.151 | 199.918 | 5.404 |  | 100.000 |
| gnn_corrbinary | post_covid | 6.579 | 137.304 | 4.859 | 0.056 | 97.674 |
| gnn_multiedge_covid_rsv_full | full | 6.767 | 85.984 | 5.071 | 0.186 | 100.000 |
| lstm | exclude_covid | 6.819 | 126.383 | 5.089 | 0.200 | 95.349 |
| lstm | post_covid | 6.905 | 171.231 | 5.774 | 0.165 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.913 | 158.127 | 5.726 | 0.289 | 100.000 |
| persistence | exclude_covid | 7.864 | 139.157 | 6.249 | -0.050 | 100.000 |
| persistence | post_covid | 7.864 | 139.157 | 6.249 | -0.050 | 100.000 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 4.521 | 49.449 | 3.315 | 0.556 | 100.000 |
| arima | post_covid | 5.435 | 84.330 | 4.415 |  | 100.000 |
| arima | exclude_covid | 5.436 | 85.746 | 4.441 |  | 100.000 |
| gnn_multiedge_season | post_covid | 5.438 | 46.459 | 4.047 | 0.499 | 92.000 |
| dualtopo | post_covid | 5.526 | 75.416 | 4.354 | -0.349 | 100.000 |
| dualtopo_no_bg | post_covid | 5.534 | 75.057 | 4.355 | 0.238 | 100.000 |
| gnn_multiedge_level | post_covid | 5.582 | 56.639 | 4.205 | 0.324 | 100.000 |
| gnn_multiedge_rt | post_covid | 5.612 | 51.106 | 3.984 | 0.449 | 100.000 |
| dualtopo_fullhistory | full | 6.508 | 63.517 | 5.030 | 0.141 | 100.000 |
| gnn_geo | post_covid | 6.575 | 56.835 | 4.855 | 0.256 | 100.000 |
| gnn_corrbinary | post_covid | 6.601 | 56.811 | 4.931 | 0.130 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 6.705 | 58.110 | 5.322 | 0.286 | 100.000 |
| gnn_multiedge | post_covid | 6.929 | 53.234 | 4.978 | 0.148 | 100.000 |
| gnn_uniform | post_covid | 7.118 | 56.644 | 5.384 | 0.140 | 100.000 |
| lstm | post_covid | 7.420 | 87.583 | 5.916 | -0.032 | 100.000 |
| gnn_multiedge_full | full | 7.424 | 63.232 | 5.827 | 0.283 | 88.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.868 | 135.457 | 6.734 | 0.011 | 100.000 |
| lstm | exclude_covid | 8.145 | 70.906 | 6.001 | 0.006 | 92.000 |
| gnn_multiedge_covid_rsv_full | full | 8.392 | 70.305 | 6.741 | 0.047 | 100.000 |
| persistence | exclude_covid | 9.331 | 76.845 | 7.724 | -0.065 | 100.000 |
| persistence | post_covid | 9.331 | 76.845 | 7.724 | -0.065 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 2.902 | 142.907 | 2.484 | 0.241 | 100.000 |
| gnn_multiedge_season | post_covid | 3.087 | 83.192 | 2.288 | -0.206 | 55.556 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| gnn_multiedge_full | full | 3.270 | 105.048 | 2.584 | -0.182 | 83.333 |
| gnn_uniform | post_covid | 3.334 | 116.343 | 2.719 | -0.264 | 100.000 |
| gnn_multiedge_rt | post_covid | 3.346 | 106.683 | 2.688 | -0.313 | 77.778 |
| gnn_multiedge_covid_rsv_full | full | 3.401 | 107.761 | 2.751 | -0.209 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 3.429 | 124.938 | 2.749 | -0.165 | 100.000 |
| gnn_multiedge_level | post_covid | 3.576 | 182.977 | 3.302 | 0.398 | 100.000 |
| dualtopo_fullhistory | full | 4.018 | 204.230 | 3.573 | 0.445 | 100.000 |
| gnn_multiedge | post_covid | 4.047 | 164.342 | 3.378 | -0.409 | 100.000 |
| lstm | exclude_covid | 4.353 | 203.434 | 3.822 | 0.592 | 100.000 |
| gnn_geo | post_covid | 4.978 | 192.707 | 3.913 | -0.359 | 100.000 |
| persistence | exclude_covid | 5.177 | 225.701 | 4.200 | 0.007 | 100.000 |
| persistence | post_covid | 5.177 | 225.701 | 4.200 | 0.007 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.308 | 189.614 | 4.325 | -0.237 | 100.000 |
| dualtopo_no_bg | post_covid | 5.953 | 306.281 | 5.683 | 0.289 | 100.000 |
| dualtopo | post_covid | 5.994 | 308.261 | 5.722 | 0.175 | 100.000 |
| lstm | post_covid | 6.119 | 287.408 | 5.577 | 0.499 | 100.000 |
| gnn_corrbinary | post_covid | 6.549 | 249.099 | 4.760 | -0.233 | 94.444 |
| arima | post_covid | 6.899 | 352.352 | 6.613 |  | 100.000 |
| arima | exclude_covid | 7.024 | 358.491 | 6.743 |  | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
