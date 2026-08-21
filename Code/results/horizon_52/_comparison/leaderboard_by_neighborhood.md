# Per-neighborhood leaderboard — horizon 52

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_multiedge_level | 8 | 1 | 0 |
| lstm | 3 | 4 | 0 |
| dualtopo_fullhistory | 2 | 0 | 10 |
| gnn_geo | 1 | 0 | 0 |
| arima | 0 | 1 | 2 |
| dualtopo_no_bg | 0 | 8 | 0 |
| persistence | 0 | 0 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `dualtopo_fullhistory (full)`: Charles., Fenway; `gnn_geo (post_covid)`: Mattapan; `gnn_multiedge_level (post_covid)`: BackBay+, Dorchest., HydePark, JP, Roslind., Roxbury, S.End, W.Roxbury; `lstm (exclude_covid)`: Allston, E.Boston; `lstm (post_covid)`: S.Boston
- **Flu season (Oct–Mar)** — `arima (exclude_covid)`: Charles.; `dualtopo_no_bg (post_covid)`: Allston, Dorchest., HydePark, JP, Mattapan, Roslind., Roxbury, S.End; `gnn_multiedge_level (post_covid)`: Fenway; `lstm (post_covid)`: BackBay+, E.Boston, S.Boston, W.Roxbury
- **Off-season (Apr–Sep)** — `arima (exclude_covid)`: Mattapan; `arima (post_covid)`: JP; `dualtopo_fullhistory (full)`: Allston, BackBay+, Charles., E.Boston, Fenway, HydePark, Roslind., S.Boston, S.End, W.Roxbury; `persistence (exclude_covid)`: Dorchest., Roxbury

`gnn_multiedge_level (post_covid)` wins 8 of 14 neighborhoods. `gnn_multiedge_level (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 52.018 | 109.769 | 35.463 | 0.423 | 67.347 |
| gnn_multiedge_leaknorm | post_covid | 55.383 | 76.048 | 33.719 | 0.340 | 75.510 |
| lstm | exclude_covid | 55.449 | 98.642 | 37.289 | 0.405 | 93.878 |
| gnn_geo | post_covid | 56.021 | 59.965 | 29.820 | 0.289 | 77.551 |
| lstm | post_covid | 59.117 | 291.136 | 51.009 | 0.329 | 42.857 |
| gnn_multiedge_full | full | 59.428 | 97.751 | 36.399 | 0.401 | 87.755 |
| gnn_multiedge | post_covid | 59.987 | 89.290 | 38.112 | 0.343 | 71.429 |
| gnn_multiedge_season | post_covid | 60.020 | 74.781 | 36.190 | 0.269 | 69.388 |
| dualtopo_no_bg | post_covid | 60.099 | 303.639 | 49.748 | 0.041 | 55.102 |
| gnn_uniform | post_covid | 60.116 | 67.756 | 35.260 | 0.278 | 71.429 |
| gnn_multiedge_season_level | post_covid | 60.668 | 111.944 | 41.905 | 0.415 | 71.429 |
| gnn_multiedge_rt | post_covid | 62.224 | 70.530 | 36.859 | 0.224 | 65.306 |
| gnn_corrbinary | post_covid | 63.687 | 79.415 | 37.095 | 0.134 | 73.469 |
| dualtopo_fullhistory | full | 65.027 | 88.546 | 36.600 | 0.255 | 87.755 |
| gnn_multiedge_covid_rsv | post_covid | 65.080 | 85.199 | 37.592 | 0.115 | 71.429 |
| gnn_multiedge_covid_rsv_full | full | 65.156 | 99.237 | 36.488 | 0.037 | 79.592 |
| arima | exclude_covid | 74.909 | 97.803 | 42.890 | 0.348 | 89.796 |
| persistence | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| persistence | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 71.429 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 71.429 |
| arima | post_covid | 83.026 | 100.465 | 43.184 | 0.367 | 63.265 |
| dualtopo | post_covid | 209.417 | 211.430 | 98.139 | 0.086 | 65.306 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 62.815 | 98.688 | 44.614 | 0.012 | 73.077 |
| lstm | post_covid | 64.063 | 107.862 | 50.270 | 0.010 | 61.538 |
| gnn_multiedge_level | post_covid | 69.024 | 88.033 | 53.044 | 0.040 | 53.846 |
| lstm | exclude_covid | 72.492 | 71.764 | 54.645 | 0.116 | 88.462 |
| gnn_multiedge_leaknorm | post_covid | 74.600 | 72.498 | 54.089 | -0.046 | 57.692 |
| gnn_geo | post_covid | 75.265 | 56.560 | 47.976 | -0.064 | 69.231 |
| gnn_multiedge_season | post_covid | 79.077 | 67.181 | 54.738 | -0.021 | 53.846 |
| gnn_multiedge_full | full | 80.411 | 88.688 | 59.104 | 0.100 | 76.923 |
| gnn_multiedge_season_level | post_covid | 80.451 | 102.697 | 64.331 | 0.079 | 50.000 |
| gnn_multiedge | post_covid | 80.502 | 89.358 | 61.083 | -0.015 | 50.000 |
| gnn_uniform | post_covid | 80.823 | 76.564 | 56.870 | -0.121 | 65.385 |
| gnn_multiedge_rt | post_covid | 81.528 | 66.411 | 55.180 | -0.060 | 53.846 |
| gnn_corrbinary | post_covid | 85.023 | 76.833 | 58.537 | -0.329 | 61.538 |
| gnn_multiedge_covid_rsv_full | full | 88.362 | 79.618 | 57.545 | -0.188 | 61.538 |
| gnn_multiedge_covid_rsv | post_covid | 88.516 | 78.698 | 61.283 | -0.223 | 53.846 |
| dualtopo_fullhistory | full | 88.598 | 80.826 | 60.304 | -0.054 | 76.923 |
| arima | exclude_covid | 102.386 | 109.438 | 73.277 | 0.087 | 80.769 |
| persistence | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |
| persistence | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 46.154 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 46.154 |
| arima | post_covid | 113.212 | 109.180 | 71.472 | 0.154 | 46.154 |
| dualtopo | post_covid | 287.077 | 275.208 | 171.974 | -0.150 | 42.308 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| persistence | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| arima | exclude_covid | 10.220 | 84.649 | 8.539 | 0.735 | 100.000 |
| dualtopo_fullhistory | full | 11.621 | 97.272 | 9.803 | 0.827 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 12.892 | 92.547 | 10.811 | 0.676 | 91.304 |
| arima | post_covid | 14.039 | 90.614 | 11.206 | 0.578 | 82.609 |
| gnn_multiedge_full | full | 14.650 | 107.997 | 10.733 | 0.746 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 14.768 | 121.415 | 12.683 | 0.514 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 15.606 | 80.062 | 10.691 | 0.786 | 95.652 |
| dualtopo | post_covid | 16.389 | 139.334 | 14.674 | 0.848 | 91.304 |
| gnn_geo | post_covid | 16.803 | 63.815 | 9.296 | 0.706 | 86.957 |
| gnn_uniform | post_covid | 17.745 | 57.799 | 10.833 | 0.777 | 78.261 |
| gnn_multiedge | post_covid | 18.445 | 89.213 | 12.145 | 0.786 | 95.652 |
| gnn_multiedge_level | post_covid | 19.470 | 134.341 | 15.588 | 0.847 | 82.609 |
| gnn_corrbinary | post_covid | 21.660 | 82.333 | 12.857 | 0.748 | 86.957 |
| gnn_multiedge_season_level | post_covid | 22.907 | 122.397 | 16.555 | 0.838 | 95.652 |
| gnn_multiedge_season | post_covid | 24.611 | 83.372 | 15.222 | 0.802 | 86.957 |
| lstm | exclude_covid | 24.694 | 129.025 | 17.668 | 0.807 | 100.000 |
| gnn_multiedge_rt | post_covid | 27.109 | 75.187 | 16.149 | 0.786 | 78.261 |
| lstm | post_covid | 52.972 | 498.316 | 51.845 | 0.868 | 21.739 |
| dualtopo_no_bg | post_covid | 56.872 | 535.323 | 55.553 | 0.391 | 34.783 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 47.986 | 110.866 | 31.366 | 0.386 | 67.347 |
| gnn_multiedge_leaknorm | post_covid | 52.198 | 72.690 | 31.313 | 0.309 | 67.347 |
| gnn_geo | post_covid | 52.846 | 67.511 | 29.996 | 0.254 | 71.429 |
| lstm | post_covid | 53.129 | 248.647 | 42.289 | 0.193 | 59.184 |
| dualtopo_no_bg | post_covid | 53.712 | 279.654 | 43.308 | -0.075 | 57.143 |
| gnn_multiedge_full | full | 54.426 | 88.074 | 32.692 | 0.370 | 87.755 |
| lstm | exclude_covid | 54.462 | 112.795 | 36.435 | 0.324 | 91.837 |
| gnn_multiedge_covid_rsv_full | full | 55.520 | 73.556 | 27.464 | 0.143 | 83.673 |
| gnn_multiedge | post_covid | 55.727 | 82.079 | 34.275 | 0.318 | 71.429 |
| gnn_multiedge_season | post_covid | 55.977 | 77.714 | 35.159 | 0.248 | 59.184 |
| gnn_multiedge_season_level | post_covid | 56.147 | 116.869 | 37.028 | 0.345 | 77.551 |
| gnn_uniform | post_covid | 56.149 | 79.740 | 34.384 | 0.254 | 71.429 |
| gnn_multiedge_rt | post_covid | 57.497 | 82.017 | 36.401 | 0.218 | 61.224 |
| gnn_corrbinary | post_covid | 59.046 | 79.272 | 34.470 | 0.130 | 69.388 |
| dualtopo_fullhistory | full | 59.898 | 108.272 | 35.750 | 0.206 | 91.837 |
| gnn_multiedge_covid_rsv | post_covid | 60.699 | 76.099 | 34.424 | 0.097 | 73.469 |
| persistence | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| persistence | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 69.388 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 69.388 |
| arima | post_covid | 70.901 | 96.037 | 39.222 | 0.295 | 65.306 |
| arima | exclude_covid | 70.952 | 91.609 | 38.648 | 0.323 | 91.837 |
| dualtopo | post_covid | 173.883 | 233.231 | 84.737 | 0.012 | 65.306 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 59.088 | 109.785 | 41.825 | -0.106 | 69.231 |
| lstm | post_covid | 62.952 | 116.676 | 46.671 | -0.127 | 61.538 |
| gnn_multiedge_level | post_covid | 64.184 | 99.614 | 47.583 | 0.021 | 46.154 |
| gnn_multiedge_leaknorm | post_covid | 70.981 | 94.650 | 52.143 | -0.091 | 42.308 |
| gnn_geo | post_covid | 71.464 | 82.941 | 48.492 | -0.126 | 65.385 |
| lstm | exclude_covid | 71.726 | 99.181 | 54.299 | 0.017 | 84.615 |
| gnn_multiedge_full | full | 74.252 | 111.021 | 55.698 | 0.053 | 76.923 |
| gnn_multiedge_season | post_covid | 74.832 | 89.742 | 54.989 | -0.072 | 46.154 |
| gnn_multiedge_season_level | post_covid | 75.031 | 120.321 | 57.389 | 0.003 | 61.538 |
| gnn_multiedge_covid_rsv_full | full | 75.659 | 77.894 | 45.296 | -0.103 | 73.077 |
| gnn_multiedge | post_covid | 75.681 | 108.435 | 57.294 | -0.052 | 46.154 |
| gnn_uniform | post_covid | 76.063 | 97.770 | 55.506 | -0.157 | 65.385 |
| gnn_multiedge_rt | post_covid | 76.438 | 92.056 | 55.914 | -0.097 | 53.846 |
| gnn_corrbinary | post_covid | 79.720 | 102.838 | 56.146 | -0.350 | 61.538 |
| dualtopo_fullhistory | full | 81.386 | 104.185 | 57.205 | -0.089 | 84.615 |
| gnn_multiedge_covid_rsv | post_covid | 82.777 | 92.358 | 57.953 | -0.256 | 57.692 |
| persistence | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |
| persistence | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 50.000 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 50.000 |
| arima | post_covid | 96.953 | 129.404 | 67.415 | 0.031 | 46.154 |
| arima | exclude_covid | 97.037 | 127.833 | 66.687 | 0.072 | 84.615 |
| dualtopo | post_covid | 238.326 | 319.194 | 148.309 | -0.219 | 34.615 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| persistence | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 91.304 |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 91.304 |
| gnn_multiedge_full | full | 8.850 | 62.134 | 6.686 | 0.815 | 100.000 |
| arima | exclude_covid | 8.981 | 50.661 | 6.952 | 0.771 | 100.000 |
| arima | post_covid | 9.137 | 58.319 | 7.351 | 0.747 | 86.957 |
| gnn_multiedge_covid_rsv_full | full | 9.808 | 68.653 | 7.306 | 0.687 | 95.652 |
| gnn_multiedge_covid_rsv | post_covid | 10.176 | 57.718 | 7.826 | 0.719 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 10.449 | 47.867 | 7.765 | 0.812 | 95.652 |
| gnn_multiedge | post_covid | 11.891 | 52.285 | 8.253 | 0.817 | 100.000 |
| dualtopo_fullhistory | full | 12.487 | 112.893 | 11.495 | 0.676 | 100.000 |
| gnn_geo | post_covid | 13.283 | 50.069 | 9.086 | 0.785 | 78.261 |
| gnn_uniform | post_covid | 13.289 | 59.358 | 10.505 | 0.815 | 78.261 |
| dualtopo | post_covid | 14.376 | 136.055 | 12.873 | 0.723 | 100.000 |
| gnn_corrbinary | post_covid | 15.598 | 52.633 | 9.966 | 0.782 | 78.261 |
| gnn_multiedge_level | post_covid | 15.775 | 123.585 | 13.034 | 0.757 | 91.304 |
| gnn_multiedge_season | post_covid | 18.585 | 64.118 | 12.742 | 0.781 | 73.913 |
| gnn_multiedge_season_level | post_covid | 18.765 | 112.966 | 14.011 | 0.723 | 95.652 |
| gnn_multiedge_rt | post_covid | 20.929 | 70.669 | 14.344 | 0.747 | 69.565 |
| lstm | exclude_covid | 22.441 | 128.185 | 16.242 | 0.726 | 100.000 |
| lstm | post_covid | 39.162 | 397.831 | 37.336 | 0.726 | 56.522 |
| dualtopo_no_bg | post_covid | 46.899 | 471.680 | 44.985 | 0.233 | 43.478 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 37.536 | 121.054 | 23.498 | 0.291 | 76.190 |
| lstm | post_covid | 38.919 | 187.150 | 27.621 | 0.107 | 88.095 |
| lstm | exclude_covid | 39.197 | 112.943 | 23.914 | 0.263 | 90.476 |
| dualtopo_no_bg | post_covid | 39.250 | 197.678 | 28.803 | -0.056 | 90.476 |
| gnn_multiedge_season_level | post_covid | 40.409 | 140.708 | 26.905 | 0.281 | 78.571 |
| dualtopo_fullhistory | full | 42.369 | 104.951 | 23.177 | 0.169 | 90.476 |
| gnn_multiedge_full | full | 42.578 | 149.481 | 27.227 | 0.247 | 80.952 |
| gnn_geo | post_covid | 42.720 | 126.499 | 24.835 | 0.096 | 73.810 |
| gnn_multiedge_leaknorm | post_covid | 43.205 | 142.489 | 26.169 | 0.106 | 76.190 |
| gnn_multiedge_season | post_covid | 43.835 | 142.910 | 27.579 | 0.141 | 66.667 |
| gnn_multiedge_rt | post_covid | 44.315 | 131.482 | 27.161 | 0.107 | 69.048 |
| gnn_multiedge | post_covid | 44.397 | 157.952 | 28.998 | 0.163 | 73.810 |
| gnn_multiedge_covid_rsv_full | full | 44.592 | 104.433 | 24.715 | 0.014 | 85.714 |
| gnn_uniform | post_covid | 44.997 | 144.365 | 27.563 | 0.104 | 71.429 |
| gnn_multiedge_covid_rsv | post_covid | 46.010 | 135.250 | 26.925 | 0.048 | 69.048 |
| gnn_corrbinary | post_covid | 46.969 | 148.602 | 28.055 | -0.029 | 69.048 |
| arima | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 90.476 |
| persistence | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |
| persistence | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 66.667 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 66.667 |
| arima | post_covid | 54.977 | 172.497 | 31.966 | 0.215 | 59.524 |
| dualtopo | post_covid | 108.670 | 331.968 | 57.596 | -0.035 | 66.667 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 45.809 | 141.580 | 32.145 | -0.045 | 84.615 |
| lstm | post_covid | 46.302 | 144.742 | 32.190 | -0.088 | 80.769 |
| gnn_multiedge_level | post_covid | 47.122 | 146.031 | 32.850 | 0.055 | 65.385 |
| lstm | exclude_covid | 48.806 | 132.963 | 32.802 | 0.082 | 84.615 |
| gnn_multiedge_season_level | post_covid | 50.566 | 181.839 | 37.929 | 0.073 | 65.385 |
| gnn_geo | post_covid | 53.225 | 150.308 | 33.730 | -0.110 | 69.231 |
| gnn_multiedge_full | full | 53.239 | 183.118 | 38.050 | 0.079 | 76.923 |
| dualtopo_fullhistory | full | 53.500 | 134.010 | 33.583 | -0.020 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 53.961 | 176.849 | 35.854 | -0.121 | 69.231 |
| gnn_multiedge_season | post_covid | 54.147 | 164.090 | 36.242 | -0.014 | 57.692 |
| gnn_multiedge_rt | post_covid | 54.679 | 155.635 | 35.496 | -0.064 | 69.231 |
| gnn_multiedge | post_covid | 55.451 | 200.285 | 40.238 | -0.045 | 65.385 |
| gnn_multiedge_covid_rsv_full | full | 55.911 | 117.610 | 34.454 | -0.121 | 84.615 |
| gnn_uniform | post_covid | 56.078 | 179.325 | 37.394 | -0.116 | 69.231 |
| gnn_multiedge_covid_rsv | post_covid | 57.643 | 174.271 | 37.824 | -0.133 | 61.538 |
| gnn_corrbinary | post_covid | 58.546 | 178.598 | 37.933 | -0.273 | 69.231 |
| arima | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 88.462 |
| persistence | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |
| persistence | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 53.846 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 53.846 |
| arima | post_covid | 68.960 | 213.320 | 44.674 | 0.081 | 53.846 |
| dualtopo | post_covid | 137.933 | 482.540 | 87.951 | -0.181 | 46.154 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 7.819 | 57.729 | 6.268 | 0.555 | 100.000 |
| dualtopo | post_covid | 9.077 | 87.289 | 8.269 | 0.525 | 100.000 |
| gnn_multiedge_level | post_covid | 9.506 | 80.465 | 8.299 | 0.579 | 93.750 |
| gnn_multiedge_season_level | post_covid | 11.457 | 73.871 | 8.990 | 0.552 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 11.833 | 83.022 | 8.889 | 0.192 | 87.500 |
| gnn_multiedge_full | full | 12.370 | 94.820 | 9.640 | 0.224 | 87.500 |
| arima | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 93.750 |
| persistence | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| persistence | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| gnn_multiedge_covid_rsv | post_covid | 12.549 | 71.841 | 9.214 | 0.186 | 81.250 |
| lstm | exclude_covid | 12.733 | 80.411 | 9.471 | 0.536 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 12.973 | 86.655 | 10.432 | 0.311 | 87.500 |
| gnn_multiedge | post_covid | 13.330 | 89.162 | 10.734 | 0.334 | 87.500 |
| gnn_geo | post_covid | 13.678 | 87.811 | 10.380 | 0.334 | 81.250 |
| gnn_uniform | post_covid | 14.308 | 87.556 | 11.588 | 0.341 | 75.000 |
| arima | post_covid | 14.365 | 106.160 | 11.314 | 0.023 | 68.750 |
| gnn_corrbinary | post_covid | 14.863 | 99.859 | 12.003 | 0.338 | 68.750 |
| gnn_multiedge_season | post_covid | 16.723 | 108.493 | 13.501 | 0.433 | 81.250 |
| gnn_multiedge_rt | post_covid | 17.223 | 92.235 | 13.618 | 0.367 | 68.750 |
| lstm | post_covid | 22.186 | 256.063 | 20.195 | 0.277 | 100.000 |
| dualtopo_no_bg | post_covid | 25.179 | 288.838 | 23.373 | 0.140 | 100.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 31.107 | 129.573 | 20.037 | 0.333 | 77.551 |
| lstm | post_covid | 32.717 | 238.610 | 26.599 | 0.292 | 89.796 |
| gnn_geo | post_covid | 33.118 | 117.254 | 20.741 | 0.234 | 79.592 |
| gnn_multiedge_full | full | 33.149 | 142.393 | 22.779 | 0.392 | 93.878 |
| gnn_multiedge_leaknorm | post_covid | 33.632 | 132.575 | 22.696 | 0.267 | 73.469 |
| gnn_multiedge_covid_rsv_full | full | 33.726 | 131.382 | 19.180 | 0.103 | 91.837 |
| dualtopo_no_bg | post_covid | 33.896 | 266.800 | 27.418 | -0.022 | 89.796 |
| gnn_multiedge_season_level | post_covid | 34.164 | 129.881 | 22.845 | 0.350 | 77.551 |
| lstm | exclude_covid | 34.493 | 116.202 | 22.963 | 0.330 | 91.837 |
| gnn_multiedge_season | post_covid | 34.979 | 117.422 | 22.835 | 0.227 | 79.592 |
| gnn_multiedge | post_covid | 35.381 | 145.206 | 23.617 | 0.288 | 77.551 |
| dualtopo_fullhistory | full | 35.667 | 95.904 | 20.014 | 0.206 | 91.837 |
| gnn_uniform | post_covid | 35.699 | 126.688 | 23.458 | 0.214 | 81.633 |
| gnn_multiedge_rt | post_covid | 36.366 | 110.210 | 23.070 | 0.168 | 83.673 |
| gnn_multiedge_covid_rsv | post_covid | 36.521 | 122.538 | 22.622 | 0.115 | 83.673 |
| gnn_corrbinary | post_covid | 37.218 | 139.108 | 24.321 | 0.100 | 75.510 |
| arima | exclude_covid | 40.018 | 133.802 | 24.305 | 0.341 | 97.959 |
| arima | post_covid | 40.752 | 132.956 | 24.163 | 0.335 | 77.551 |
| persistence | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| persistence | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 79.592 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 79.592 |
| dualtopo | post_covid | 95.379 | 222.591 | 49.362 | 0.029 | 69.388 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 38.355 | 157.219 | 27.541 | -0.052 | 80.769 |
| lstm | post_covid | 39.125 | 160.726 | 29.952 | -0.003 | 80.769 |
| gnn_multiedge_level | post_covid | 41.403 | 145.930 | 30.157 | -0.018 | 61.538 |
| lstm | exclude_covid | 44.502 | 126.660 | 34.511 | 0.085 | 84.615 |
| gnn_geo | post_covid | 44.505 | 156.201 | 33.040 | -0.178 | 65.385 |
| gnn_multiedge_full | full | 44.566 | 175.269 | 35.894 | 0.066 | 88.462 |
| gnn_multiedge_covid_rsv_full | full | 45.243 | 140.505 | 28.064 | -0.269 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 45.263 | 175.014 | 36.242 | -0.171 | 57.692 |
| gnn_multiedge_season_level | post_covid | 45.373 | 156.948 | 35.321 | 0.049 | 61.538 |
| gnn_multiedge_season | post_covid | 46.431 | 140.273 | 35.249 | -0.118 | 69.231 |
| gnn_multiedge | post_covid | 47.560 | 194.524 | 37.652 | -0.128 | 57.692 |
| gnn_uniform | post_covid | 48.183 | 177.266 | 38.053 | -0.239 | 73.077 |
| gnn_multiedge_rt | post_covid | 48.349 | 137.135 | 35.690 | -0.172 | 76.923 |
| dualtopo_fullhistory | full | 48.564 | 113.200 | 32.815 | -0.066 | 84.615 |
| gnn_multiedge_covid_rsv | post_covid | 49.479 | 153.550 | 36.425 | -0.285 | 69.231 |
| gnn_corrbinary | post_covid | 50.008 | 193.407 | 39.360 | -0.428 | 61.538 |
| arima | exclude_covid | 54.496 | 182.986 | 40.244 | 0.058 | 96.154 |
| arima | post_covid | 55.514 | 182.351 | 40.090 | 0.058 | 57.692 |
| persistence | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| persistence | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 65.385 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 65.385 |
| dualtopo | post_covid | 130.588 | 308.097 | 85.343 | -0.186 | 42.308 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 6.643 | 76.352 | 5.545 | 0.491 | 100.000 |
| arima | post_covid | 7.371 | 77.118 | 6.158 | 0.365 | 100.000 |
| arima | exclude_covid | 7.379 | 78.202 | 6.287 | 0.328 | 100.000 |
| persistence | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| persistence | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 95.652 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 95.652 |
| gnn_multiedge_covid_rsv | post_covid | 8.604 | 87.480 | 7.019 | 0.290 | 100.000 |
| gnn_uniform | post_covid | 9.527 | 69.514 | 6.959 | 0.440 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 9.685 | 84.600 | 7.383 | 0.405 | 91.304 |
| gnn_multiedge_full | full | 9.788 | 105.229 | 7.953 | 0.257 | 100.000 |
| gnn_geo | post_covid | 9.882 | 73.227 | 6.839 | 0.327 | 95.652 |
| dualtopo | post_covid | 10.173 | 125.931 | 8.688 | 0.583 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 10.457 | 121.068 | 9.138 | -0.085 | 100.000 |
| gnn_multiedge | post_covid | 10.485 | 89.455 | 7.751 | 0.434 | 100.000 |
| gnn_multiedge_level | post_covid | 11.124 | 111.082 | 8.598 | 0.560 | 95.652 |
| gnn_corrbinary | post_covid | 11.134 | 77.726 | 7.321 | 0.419 | 91.304 |
| gnn_multiedge_season_level | post_covid | 12.626 | 99.284 | 8.742 | 0.579 | 95.652 |
| gnn_multiedge_season | post_covid | 13.021 | 91.590 | 8.802 | 0.461 | 91.304 |
| gnn_multiedge_rt | post_covid | 13.231 | 79.773 | 8.804 | 0.519 | 91.304 |
| lstm | exclude_covid | 17.204 | 104.380 | 9.908 | 0.486 | 100.000 |
| lstm | post_covid | 23.452 | 326.652 | 22.808 | 0.603 | 100.000 |
| dualtopo_no_bg | post_covid | 28.015 | 390.675 | 27.279 | 0.468 | 100.000 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 21.860 | 92.057 | 13.635 | 0.344 | 94.286 |
| arima | post_covid | 21.939 | 114.763 | 13.838 | 0.213 | 88.571 |
| lstm | post_covid | 22.049 | 132.117 | 15.058 | 0.060 | 88.571 |
| gnn_multiedge_level | post_covid | 22.099 | 104.035 | 14.158 | 0.195 | 82.857 |
| dualtopo_no_bg | post_covid | 22.167 | 146.909 | 15.901 | -0.052 | 88.571 |
| arima | exclude_covid | 22.191 | 148.540 | 16.019 |  | 97.143 |
| gnn_geo | post_covid | 23.593 | 112.156 | 15.568 | 0.195 | 74.286 |
| gnn_multiedge_full | full | 23.706 | 132.935 | 15.902 | 0.215 | 91.429 |
| gnn_multiedge_season_level | post_covid | 23.782 | 126.270 | 16.465 | 0.194 | 82.857 |
| gnn_corrbinary | post_covid | 24.153 | 122.557 | 16.089 | 0.169 | 80.000 |
| gnn_multiedge_leaknorm | post_covid | 24.186 | 126.925 | 16.477 | 0.157 | 77.143 |
| lstm | exclude_covid | 24.938 | 113.798 | 16.441 | 0.085 | 91.429 |
| gnn_multiedge_season | post_covid | 25.128 | 133.475 | 17.248 | 0.155 | 77.143 |
| gnn_multiedge | post_covid | 25.207 | 139.589 | 17.012 | 0.163 | 80.000 |
| gnn_multiedge_rt | post_covid | 25.675 | 132.067 | 17.676 | 0.131 | 74.286 |
| gnn_multiedge_covid_rsv_full | full | 25.681 | 113.752 | 16.676 | -0.099 | 74.286 |
| gnn_multiedge_covid_rsv | post_covid | 26.350 | 124.881 | 17.150 | 0.045 | 80.000 |
| gnn_uniform | post_covid | 26.631 | 139.550 | 17.933 | 0.062 | 80.000 |
| persistence | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| persistence | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 80.000 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 80.000 |
| dualtopo | post_covid | 44.221 | 220.119 | 25.252 | -0.119 | 74.286 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 26.580 | 133.708 | 18.721 |  | 95.238 |
| dualtopo_no_bg | post_covid | 26.597 | 132.340 | 18.636 | -0.156 | 80.952 |
| lstm | post_covid | 27.158 | 129.240 | 18.956 | -0.138 | 80.952 |
| arima | post_covid | 27.168 | 105.487 | 17.248 | 0.067 | 80.952 |
| dualtopo_fullhistory | full | 27.969 | 122.134 | 20.064 | 0.194 | 90.476 |
| gnn_multiedge_level | post_covid | 28.144 | 136.839 | 20.629 | -0.066 | 71.429 |
| gnn_geo | post_covid | 29.577 | 140.109 | 21.125 | 0.089 | 61.905 |
| gnn_multiedge_full | full | 29.680 | 172.578 | 21.831 | 0.075 | 85.714 |
| gnn_multiedge_leaknorm | post_covid | 30.074 | 159.359 | 22.282 | 0.025 | 66.667 |
| gnn_corrbinary | post_covid | 30.091 | 154.244 | 21.600 | 0.015 | 71.429 |
| gnn_multiedge_season_level | post_covid | 30.137 | 172.038 | 23.878 | -0.046 | 71.429 |
| gnn_multiedge_season | post_covid | 30.937 | 160.411 | 22.661 | 0.042 | 66.667 |
| gnn_multiedge | post_covid | 31.336 | 177.406 | 22.943 | 0.013 | 71.429 |
| gnn_multiedge_rt | post_covid | 31.605 | 156.364 | 22.985 | 0.023 | 66.667 |
| lstm | exclude_covid | 31.734 | 155.865 | 24.395 | -0.144 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 32.395 | 138.987 | 23.377 | -0.174 | 57.143 |
| gnn_multiedge_covid_rsv | post_covid | 33.012 | 151.812 | 23.394 | -0.072 | 71.429 |
| gnn_uniform | post_covid | 33.208 | 173.569 | 23.901 | -0.098 | 71.429 |
| persistence | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| persistence | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 66.667 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 66.667 |
| dualtopo | post_covid | 56.891 | 327.003 | 39.180 | -0.264 | 57.143 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 4.602 | 46.943 | 3.992 | 0.530 | 100.000 |
| gnn_multiedge_level | post_covid | 5.727 | 54.831 | 4.450 | 0.543 | 100.000 |
| dualtopo | post_covid | 5.821 | 59.793 | 4.361 | 0.534 | 100.000 |
| lstm | exclude_covid | 6.647 | 50.697 | 4.510 | 0.477 | 100.000 |
| gnn_multiedge_season_level | post_covid | 7.184 | 57.617 | 5.345 | 0.535 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 8.638 | 75.899 | 6.624 | 0.373 | 100.000 |
| persistence | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| persistence | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| gnn_geo | post_covid | 8.912 | 70.226 | 7.233 | 0.528 | 92.857 |
| gnn_multiedge_full | full | 9.143 | 73.471 | 7.008 | 0.490 | 100.000 |
| arima | post_covid | 9.809 | 128.677 | 8.723 | 0.448 | 100.000 |
| gnn_corrbinary | post_covid | 10.012 | 75.026 | 7.822 | 0.535 | 92.857 |
| gnn_multiedge_covid_rsv | post_covid | 10.057 | 84.484 | 7.783 | 0.407 | 92.857 |
| gnn_multiedge_leaknorm | post_covid | 10.284 | 78.275 | 7.770 | 0.498 | 92.857 |
| lstm | post_covid | 10.442 | 136.432 | 9.210 | 0.372 | 100.000 |
| gnn_multiedge | post_covid | 10.751 | 82.865 | 8.116 | 0.498 | 92.857 |
| gnn_uniform | post_covid | 10.905 | 88.521 | 8.982 | 0.524 | 92.857 |
| gnn_multiedge_season | post_covid | 11.951 | 93.071 | 9.128 | 0.585 | 92.857 |
| gnn_multiedge_rt | post_covid | 12.233 | 95.622 | 9.713 | 0.523 | 85.714 |
| dualtopo_no_bg | post_covid | 12.935 | 168.764 | 11.799 | 0.437 | 100.000 |
| arima | exclude_covid | 13.090 | 170.790 | 11.966 |  | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 23.040 | 124.638 | 15.215 | 0.309 | 80.851 |
| gnn_multiedge_leaknorm | post_covid | 23.647 | 146.038 | 16.814 | 0.423 | 82.979 |
| gnn_multiedge_level | post_covid | 24.167 | 176.939 | 18.526 | 0.357 | 76.596 |
| gnn_multiedge_rt | post_covid | 24.241 | 124.551 | 16.823 | 0.348 | 80.851 |
| gnn_multiedge_season | post_covid | 24.652 | 144.212 | 17.802 | 0.370 | 80.851 |
| gnn_uniform | post_covid | 24.924 | 132.049 | 17.278 | 0.367 | 85.106 |
| lstm | exclude_covid | 25.059 | 137.553 | 17.450 | 0.375 | 95.745 |
| gnn_multiedge_covid_rsv_full | full | 25.208 | 137.704 | 15.166 | 0.258 | 91.489 |
| gnn_multiedge_covid_rsv | post_covid | 25.952 | 135.589 | 16.658 | 0.304 | 85.106 |
| gnn_multiedge_full | full | 26.048 | 161.799 | 17.848 | 0.491 | 100.000 |
| gnn_multiedge | post_covid | 26.311 | 164.248 | 18.996 | 0.419 | 76.596 |
| lstm | post_covid | 26.447 | 305.185 | 23.749 | 0.340 | 91.489 |
| gnn_corrbinary | post_covid | 26.643 | 149.688 | 18.396 | 0.234 | 78.723 |
| dualtopo_fullhistory | full | 26.994 | 129.033 | 16.822 | 0.276 | 93.617 |
| dualtopo_no_bg | post_covid | 27.389 | 356.135 | 24.486 | -0.034 | 93.617 |
| gnn_multiedge_season_level | post_covid | 28.921 | 179.470 | 20.893 | 0.349 | 78.723 |
| arima | post_covid | 35.960 | 153.457 | 20.620 | 0.436 | 78.723 |
| persistence | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| persistence | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 80.851 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 80.851 |
| arima | exclude_covid | 36.457 | 148.743 | 20.273 | 0.449 | 100.000 |
| dualtopo | post_covid | 83.458 | 332.439 | 42.416 | -0.027 | 72.340 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 27.379 | 174.816 | 22.365 | -0.047 | 88.462 |
| lstm | post_covid | 29.812 | 182.927 | 25.715 | 0.087 | 84.615 |
| gnn_geo | post_covid | 30.025 | 109.515 | 21.800 | 0.064 | 73.077 |
| gnn_multiedge_level | post_covid | 30.497 | 161.128 | 25.152 | 0.038 | 61.538 |
| gnn_multiedge_leaknorm | post_covid | 30.811 | 132.769 | 24.119 | 0.206 | 69.231 |
| gnn_multiedge_rt | post_covid | 30.911 | 116.229 | 23.697 | 0.172 | 69.231 |
| gnn_multiedge_season | post_covid | 31.221 | 122.533 | 24.079 | 0.200 | 73.077 |
| lstm | exclude_covid | 31.383 | 126.801 | 24.291 | 0.153 | 92.308 |
| gnn_uniform | post_covid | 32.633 | 139.066 | 25.743 | 0.124 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 32.929 | 101.419 | 21.684 | 0.137 | 84.615 |
| gnn_multiedge_full | full | 34.016 | 138.355 | 25.775 | 0.322 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 34.130 | 120.993 | 24.951 | 0.125 | 73.077 |
| gnn_multiedge | post_covid | 34.238 | 153.231 | 27.317 | 0.201 | 57.692 |
| gnn_corrbinary | post_covid | 34.659 | 142.136 | 26.462 | -0.037 | 69.231 |
| dualtopo_fullhistory | full | 35.648 | 119.746 | 25.183 | 0.040 | 88.462 |
| gnn_multiedge_season_level | post_covid | 36.838 | 185.047 | 29.757 | 0.066 | 61.538 |
| arima | post_covid | 47.848 | 148.851 | 31.755 | 0.282 | 61.538 |
| persistence | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| persistence | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 65.385 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 65.385 |
| arima | exclude_covid | 48.575 | 142.743 | 31.484 | 0.306 | 100.000 |
| dualtopo | post_covid | 111.749 | 429.069 | 68.409 | -0.241 | 50.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 7.311 | 156.171 | 6.393 | -0.035 | 100.000 |
| dualtopo_fullhistory | full | 7.578 | 140.532 | 6.470 | 0.557 | 100.000 |
| arima | post_covid | 7.718 | 159.161 | 6.834 | 0.195 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.071 | 153.661 | 6.389 | 0.175 | 100.000 |
| persistence | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| persistence | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gnn_uniform | post_covid | 8.472 | 123.362 | 6.797 | 0.477 | 90.476 |
| gnn_geo | post_covid | 8.481 | 143.362 | 7.062 | 0.372 | 90.476 |
| gnn_multiedge_leaknorm | post_covid | 8.728 | 162.466 | 7.769 | 0.408 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 8.928 | 182.629 | 7.096 | -0.039 | 100.000 |
| gnn_multiedge_full | full | 9.272 | 190.825 | 8.034 | 0.174 | 100.000 |
| gnn_multiedge | post_covid | 9.902 | 177.888 | 8.694 | 0.458 | 100.000 |
| gnn_corrbinary | post_covid | 10.073 | 159.037 | 8.409 | 0.474 | 90.476 |
| dualtopo | post_covid | 11.299 | 212.801 | 10.235 | 0.615 | 100.000 |
| gnn_multiedge_rt | post_covid | 11.497 | 134.854 | 8.311 | 0.564 | 95.238 |
| gnn_multiedge_season | post_covid | 12.383 | 171.054 | 10.029 | 0.543 | 90.476 |
| gnn_multiedge_level | post_covid | 12.477 | 196.516 | 10.323 | 0.658 | 95.238 |
| lstm | exclude_covid | 13.639 | 150.865 | 8.981 | 0.680 | 100.000 |
| gnn_multiedge_season_level | post_covid | 13.852 | 172.567 | 9.918 | 0.628 | 100.000 |
| lstm | post_covid | 21.564 | 456.552 | 21.313 | 0.572 | 100.000 |
| dualtopo_no_bg | post_covid | 27.400 | 580.625 | 27.112 | 0.417 | 100.000 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 21.211 | 143.401 | 14.538 | 0.282 | 80.435 |
| lstm | post_covid | 21.869 | 271.776 | 18.005 | 0.185 | 93.478 |
| dualtopo_no_bg | post_covid | 22.701 | 316.312 | 19.045 | -0.045 | 93.478 |
| lstm | exclude_covid | 23.733 | 146.486 | 16.547 | 0.234 | 93.478 |
| gnn_multiedge_covid_rsv_full | full | 24.095 | 123.298 | 14.462 | -0.091 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 24.257 | 125.551 | 15.594 | 0.158 | 78.261 |
| gnn_geo | post_covid | 24.262 | 114.729 | 14.957 | 0.102 | 73.913 |
| gnn_multiedge_season_level | post_covid | 24.910 | 146.415 | 17.183 | 0.283 | 82.609 |
| gnn_multiedge_full | full | 25.574 | 149.313 | 17.190 | 0.235 | 95.652 |
| gnn_multiedge_season | post_covid | 25.783 | 127.632 | 17.044 | 0.121 | 67.391 |
| gnn_multiedge_rt | post_covid | 25.905 | 122.040 | 17.102 | 0.094 | 73.913 |
| gnn_uniform | post_covid | 25.982 | 128.144 | 16.736 | 0.105 | 76.087 |
| gnn_multiedge | post_covid | 26.257 | 144.870 | 17.632 | 0.167 | 76.087 |
| gnn_multiedge_covid_rsv | post_covid | 26.649 | 131.975 | 16.893 | -0.005 | 80.435 |
| dualtopo_fullhistory | full | 26.904 | 136.272 | 15.854 | 0.103 | 93.478 |
| gnn_corrbinary | post_covid | 27.565 | 137.748 | 17.250 | -0.047 | 71.739 |
| arima | exclude_covid | 31.975 | 159.082 | 19.262 | 0.156 | 97.826 |
| arima | post_covid | 32.686 | 158.562 | 19.149 | 0.161 | 76.087 |
| persistence | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| persistence | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 76.087 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 76.087 |
| dualtopo | post_covid | 80.050 | 276.163 | 38.651 | 0.008 | 73.913 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 24.323 | 139.338 | 18.171 | -0.108 | 88.000 |
| lstm | post_covid | 25.540 | 143.029 | 19.763 | -0.124 | 88.000 |
| gnn_multiedge_level | post_covid | 27.792 | 146.298 | 21.393 | -0.097 | 64.000 |
| lstm | exclude_covid | 30.659 | 143.084 | 24.114 | -0.061 | 88.000 |
| gnn_geo | post_covid | 31.817 | 126.747 | 22.837 | -0.209 | 64.000 |
| gnn_multiedge_covid_rsv_full | full | 31.974 | 102.894 | 21.461 | -0.399 | 84.000 |
| gnn_multiedge_leaknorm | post_covid | 32.034 | 145.438 | 24.219 | -0.214 | 64.000 |
| gnn_multiedge_season_level | post_covid | 32.683 | 172.708 | 26.132 | -0.049 | 68.000 |
| gnn_multiedge_season | post_covid | 33.231 | 128.145 | 24.961 | -0.159 | 64.000 |
| gnn_multiedge_rt | post_covid | 33.446 | 127.276 | 25.258 | -0.174 | 72.000 |
| gnn_multiedge_full | full | 33.909 | 164.274 | 26.714 | -0.089 | 92.000 |
| gnn_uniform | post_covid | 34.289 | 152.889 | 26.213 | -0.275 | 76.000 |
| gnn_multiedge | post_covid | 34.603 | 172.060 | 27.408 | -0.195 | 60.000 |
| gnn_multiedge_covid_rsv | post_covid | 35.558 | 142.535 | 26.472 | -0.307 | 68.000 |
| gnn_corrbinary | post_covid | 36.126 | 154.877 | 26.359 | -0.447 | 68.000 |
| dualtopo_fullhistory | full | 36.245 | 164.468 | 25.666 | -0.202 | 88.000 |
| arima | exclude_covid | 43.007 | 210.937 | 31.671 | -0.143 | 96.000 |
| arima | post_covid | 44.023 | 215.428 | 31.746 | -0.128 | 56.000 |
| persistence | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| persistence | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 56.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 56.000 |
| dualtopo | post_covid | 108.402 | 387.055 | 66.171 | -0.200 | 52.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 4.651 | 102.704 | 4.173 | 0.685 | 100.000 |
| arima | post_covid | 5.751 | 90.865 | 4.151 | 0.538 | 100.000 |
| arima | exclude_covid | 6.126 | 97.349 | 4.490 | 0.559 | 100.000 |
| persistence | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| persistence | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| dualtopo | post_covid | 6.885 | 144.149 | 5.889 | 0.596 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.101 | 119.403 | 5.489 | 0.401 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 7.393 | 147.589 | 6.130 | 0.313 | 100.000 |
| gnn_multiedge_full | full | 7.987 | 131.503 | 5.852 | 0.438 | 100.000 |
| gnn_multiedge_level | post_covid | 8.124 | 139.951 | 6.377 | 0.619 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 8.202 | 101.876 | 5.326 | 0.510 | 95.238 |
| gnn_uniform | post_covid | 8.887 | 98.686 | 5.455 | 0.517 | 76.190 |
| gnn_geo | post_covid | 9.178 | 100.422 | 5.575 | 0.396 | 85.714 |
| gnn_multiedge | post_covid | 9.207 | 112.501 | 5.993 | 0.526 | 95.238 |
| gnn_multiedge_season_level | post_covid | 9.354 | 115.114 | 6.529 | 0.629 | 100.000 |
| gnn_corrbinary | post_covid | 10.522 | 117.356 | 6.407 | 0.449 | 76.190 |
| lstm | exclude_covid | 10.715 | 150.536 | 7.538 | 0.488 | 100.000 |
| gnn_multiedge_rt | post_covid | 11.759 | 115.808 | 7.393 | 0.518 | 76.190 |
| gnn_multiedge_season | post_covid | 11.894 | 127.021 | 7.620 | 0.569 | 71.429 |
| lstm | post_covid | 16.464 | 425.046 | 15.913 | 0.537 | 100.000 |
| dualtopo_no_bg | post_covid | 20.603 | 526.994 | 20.085 | 0.196 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 16.838 | 71.706 | 9.553 | 0.413 | 91.837 |
| gnn_multiedge_level | post_covid | 16.960 | 98.869 | 10.690 | 0.380 | 89.796 |
| gnn_geo | post_covid | 17.802 | 92.066 | 10.442 | 0.339 | 83.673 |
| dualtopo_fullhistory | full | 17.997 | 60.246 | 9.714 | 0.314 | 91.837 |
| gnn_multiedge_season_level | post_covid | 18.217 | 102.833 | 11.889 | 0.391 | 91.837 |
| lstm | post_covid | 18.297 | 206.467 | 13.702 | 0.237 | 91.837 |
| gnn_multiedge_leaknorm | post_covid | 18.666 | 106.308 | 11.341 | 0.291 | 83.673 |
| dualtopo_no_bg | post_covid | 18.805 | 231.365 | 14.616 | 0.057 | 91.837 |
| gnn_multiedge_full | full | 18.883 | 115.136 | 11.802 | 0.365 | 93.878 |
| gnn_multiedge_season | post_covid | 19.320 | 113.648 | 12.444 | 0.283 | 77.551 |
| gnn_multiedge | post_covid | 19.567 | 117.545 | 12.390 | 0.305 | 83.673 |
| gnn_multiedge_rt | post_covid | 19.594 | 106.310 | 12.476 | 0.261 | 79.592 |
| gnn_uniform | post_covid | 19.805 | 102.536 | 11.905 | 0.247 | 83.673 |
| gnn_multiedge_covid_rsv_full | full | 20.236 | 104.129 | 11.362 | 0.078 | 89.796 |
| gnn_corrbinary | post_covid | 20.523 | 109.039 | 12.211 | 0.163 | 83.673 |
| gnn_multiedge_covid_rsv | post_covid | 20.816 | 102.010 | 11.499 | 0.131 | 83.673 |
| arima | exclude_covid | 21.762 | 120.085 | 12.994 | 0.294 | 97.959 |
| arima | post_covid | 22.995 | 125.094 | 13.472 | 0.288 | 77.551 |
| persistence | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| persistence | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 75.510 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 75.510 |
| dualtopo | post_covid | 57.317 | 178.514 | 27.946 | 0.107 | 73.469 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 21.661 | 86.942 | 14.827 | 0.046 | 84.615 |
| lstm | post_covid | 21.908 | 81.455 | 14.742 | -0.085 | 84.615 |
| lstm | exclude_covid | 22.708 | 58.292 | 14.677 | 0.164 | 84.615 |
| gnn_multiedge_level | post_covid | 22.720 | 83.514 | 16.299 | 0.022 | 80.769 |
| gnn_geo | post_covid | 23.764 | 93.655 | 15.922 | 0.037 | 76.923 |
| gnn_multiedge_season_level | post_covid | 24.340 | 99.534 | 18.403 | 0.080 | 84.615 |
| dualtopo_fullhistory | full | 24.559 | 67.239 | 16.308 | 0.021 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 24.945 | 109.942 | 17.456 | -0.059 | 76.923 |
| gnn_multiedge_season | post_covid | 25.323 | 105.701 | 17.980 | 0.023 | 73.077 |
| gnn_multiedge_full | full | 25.439 | 121.908 | 18.665 | 0.063 | 88.462 |
| gnn_multiedge_rt | post_covid | 25.697 | 102.683 | 18.234 | 0.001 | 73.077 |
| gnn_multiedge | post_covid | 26.102 | 126.076 | 19.126 | -0.030 | 73.077 |
| gnn_uniform | post_covid | 26.472 | 110.181 | 18.285 | -0.115 | 80.769 |
| gnn_corrbinary | post_covid | 27.255 | 111.238 | 18.523 | -0.231 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 27.446 | 103.058 | 18.156 | -0.231 | 80.769 |
| gnn_multiedge_covid_rsv | post_covid | 28.187 | 107.057 | 18.332 | -0.188 | 73.077 |
| arima | exclude_covid | 29.546 | 135.254 | 21.122 | 0.000 | 96.154 |
| arima | post_covid | 31.314 | 150.071 | 22.443 | 0.009 | 57.692 |
| persistence | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |
| persistence | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 61.538 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 61.538 |
| dualtopo | post_covid | 78.579 | 243.969 | 49.338 | -0.106 | 50.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.877 | 52.341 | 2.261 | 0.741 | 100.000 |
| arima | post_covid | 4.243 | 96.858 | 3.332 | 0.627 | 100.000 |
| dualtopo | post_covid | 4.338 | 104.522 | 3.764 | 0.791 | 100.000 |
| persistence | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| persistence | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 91.304 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 91.304 |
| gnn_multiedge_covid_rsv_full | full | 4.568 | 105.340 | 3.683 | 0.621 | 100.000 |
| lstm | exclude_covid | 4.588 | 86.870 | 3.762 | 0.660 | 100.000 |
| arima | exclude_covid | 4.699 | 102.937 | 3.805 | 0.646 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.999 | 96.303 | 3.775 | 0.627 | 95.652 |
| gnn_multiedge_full | full | 5.304 | 107.481 | 4.044 | 0.647 | 100.000 |
| gnn_multiedge_level | post_covid | 5.410 | 116.226 | 4.350 | 0.715 | 100.000 |
| gnn_geo | post_covid | 6.060 | 90.270 | 4.247 | 0.648 | 91.304 |
| gnn_multiedge_season_level | post_covid | 6.107 | 106.561 | 4.525 | 0.718 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 6.230 | 102.199 | 4.427 | 0.640 | 91.304 |
| gnn_uniform | post_covid | 6.591 | 93.895 | 4.693 | 0.670 | 86.957 |
| gnn_multiedge | post_covid | 6.745 | 107.901 | 4.774 | 0.651 | 95.652 |
| gnn_corrbinary | post_covid | 7.590 | 106.552 | 5.074 | 0.645 | 86.957 |
| gnn_multiedge_season | post_covid | 8.386 | 122.632 | 6.186 | 0.674 | 82.609 |
| gnn_multiedge_rt | post_covid | 8.450 | 110.410 | 5.966 | 0.702 | 86.957 |
| lstm | post_covid | 13.063 | 347.784 | 12.526 | 0.667 | 100.000 |
| dualtopo_no_bg | post_covid | 14.932 | 394.625 | 14.377 | 0.147 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 18.873 | 84.299 | 10.748 | 0.246 | 90.000 |
| lstm | post_covid | 19.188 | 140.372 | 12.412 | 0.221 | 92.500 |
| dualtopo_no_bg | post_covid | 19.351 | 138.836 | 12.301 | -0.078 | 92.500 |
| arima | post_covid | 19.382 | 105.287 | 10.711 | -0.025 | 90.000 |
| gnn_multiedge_full | full | 19.391 | 97.607 | 11.719 | 0.270 | 95.000 |
| dualtopo_fullhistory | full | 19.802 | 65.216 | 10.506 | 0.199 | 92.500 |
| gnn_multiedge_season_level | post_covid | 19.818 | 97.218 | 12.603 | 0.241 | 92.500 |
| lstm | exclude_covid | 20.136 | 97.171 | 12.703 | 0.184 | 92.500 |
| gnn_geo | post_covid | 20.214 | 88.381 | 11.172 | 0.158 | 87.500 |
| gnn_multiedge | post_covid | 20.449 | 106.760 | 12.652 | 0.198 | 87.500 |
| gnn_multiedge_leaknorm | post_covid | 20.463 | 97.314 | 11.909 | 0.148 | 82.500 |
| gnn_multiedge_season | post_covid | 20.515 | 97.943 | 12.199 | 0.181 | 80.000 |
| gnn_multiedge_rt | post_covid | 20.833 | 98.424 | 12.500 | 0.161 | 77.500 |
| gnn_uniform | post_covid | 21.195 | 100.782 | 12.363 | 0.109 | 85.000 |
| gnn_multiedge_covid_rsv_full | full | 21.338 | 85.928 | 11.638 | 0.004 | 85.000 |
| gnn_multiedge_covid_rsv | post_covid | 21.559 | 95.577 | 12.553 | 0.080 | 85.000 |
| gnn_corrbinary | post_covid | 21.690 | 98.076 | 12.351 | 0.047 | 85.000 |
| arima | exclude_covid | 22.951 | 105.810 | 14.391 | 0.156 | 95.000 |
| persistence | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| persistence | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 75.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 75.000 |
| dualtopo | post_covid | 42.283 | 169.543 | 22.374 | -0.044 | 77.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 22.883 | 101.082 | 13.986 | 0.042 | 88.000 |
| dualtopo_no_bg | post_covid | 23.045 | 96.010 | 13.705 | -0.052 | 88.000 |
| gnn_multiedge_level | post_covid | 23.504 | 89.929 | 14.611 | 0.047 | 84.000 |
| arima | post_covid | 23.724 | 74.016 | 12.893 | -0.099 | 84.000 |
| gnn_multiedge_full | full | 24.178 | 113.635 | 16.269 | 0.119 | 92.000 |
| gnn_multiedge_season_level | post_covid | 24.487 | 107.983 | 17.073 | 0.067 | 88.000 |
| lstm | exclude_covid | 24.818 | 98.844 | 17.036 | 0.026 | 88.000 |
| dualtopo_fullhistory | full | 24.870 | 74.174 | 14.820 | 0.028 | 88.000 |
| gnn_multiedge_season | post_covid | 25.015 | 100.585 | 15.732 | 0.067 | 76.000 |
| gnn_geo | post_covid | 25.054 | 101.955 | 15.141 | -0.005 | 80.000 |
| gnn_multiedge | post_covid | 25.412 | 126.735 | 17.477 | 0.029 | 80.000 |
| gnn_multiedge_leaknorm | post_covid | 25.474 | 115.644 | 16.461 | -0.025 | 72.000 |
| gnn_multiedge_rt | post_covid | 25.511 | 99.749 | 16.152 | 0.042 | 76.000 |
| gnn_uniform | post_covid | 26.226 | 114.034 | 16.585 | -0.084 | 84.000 |
| gnn_multiedge_covid_rsv_full | full | 26.683 | 94.367 | 16.125 | -0.115 | 76.000 |
| gnn_corrbinary | post_covid | 26.892 | 112.493 | 16.767 | -0.155 | 80.000 |
| gnn_multiedge_covid_rsv | post_covid | 26.941 | 109.401 | 17.499 | -0.064 | 76.000 |
| arima | exclude_covid | 28.823 | 133.157 | 20.961 | -0.023 | 92.000 |
| persistence | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| persistence | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 60.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 60.000 |
| dualtopo | post_covid | 53.348 | 222.519 | 33.350 | -0.164 | 64.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.853 | 50.286 | 3.315 | 0.269 | 100.000 |
| arima | exclude_covid | 4.477 | 60.231 | 3.442 | 0.309 | 100.000 |
| persistence | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| persistence | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| dualtopo | post_covid | 4.927 | 81.251 | 4.080 | 0.247 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.241 | 71.862 | 4.160 | 0.155 | 100.000 |
| gnn_multiedge_full | full | 5.329 | 70.894 | 4.137 | 0.170 | 100.000 |
| gnn_multiedge_level | post_covid | 5.399 | 74.918 | 4.310 | 0.358 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.453 | 72.539 | 4.310 | 0.233 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.923 | 66.766 | 4.324 | 0.265 | 100.000 |
| gnn_multiedge | post_covid | 6.235 | 73.469 | 4.612 | 0.274 | 100.000 |
| gnn_geo | post_covid | 6.591 | 65.758 | 4.557 | 0.145 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.923 | 79.277 | 5.153 | 0.297 | 100.000 |
| gnn_corrbinary | post_covid | 7.019 | 74.047 | 4.992 | 0.211 | 93.333 |
| gnn_uniform | post_covid | 7.183 | 78.695 | 5.327 | 0.244 | 86.667 |
| lstm | exclude_covid | 7.394 | 94.382 | 5.482 | 0.209 | 100.000 |
| arima | post_covid | 7.985 | 157.406 | 7.075 | 0.199 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.525 | 96.216 | 6.412 | 0.217 | 80.000 |
| gnn_multiedge_season | post_covid | 8.908 | 93.541 | 6.311 | 0.196 | 86.667 |
| lstm | post_covid | 10.444 | 205.856 | 9.789 | 0.302 | 100.000 |
| dualtopo_no_bg | post_covid | 10.653 | 210.212 | 9.961 | -0.072 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 12.884 | 193.940 | 9.934 | 0.336 | 90.476 |
| gnn_multiedge_level | post_covid | 12.889 | 103.142 | 8.388 | 0.348 | 90.476 |
| arima | post_covid | 13.243 | 190.677 | 9.583 |  | 90.476 |
| dualtopo_no_bg | post_covid | 13.560 | 225.418 | 10.536 | 0.053 | 90.476 |
| lstm | exclude_covid | 13.828 | 112.626 | 9.631 | 0.345 | 95.238 |
| gnn_multiedge_season_level | post_covid | 14.609 | 110.372 | 10.240 | 0.371 | 92.857 |
| gnn_geo | post_covid | 15.129 | 85.303 | 9.540 | 0.150 | 80.952 |
| dualtopo_fullhistory | full | 15.574 | 90.053 | 9.406 | 0.203 | 95.238 |
| gnn_multiedge_leaknorm | post_covid | 15.725 | 91.044 | 9.865 | 0.173 | 80.952 |
| gnn_multiedge_full | full | 16.158 | 104.080 | 10.016 | 0.257 | 95.238 |
| gnn_multiedge_season | post_covid | 16.340 | 93.937 | 10.520 | 0.138 | 83.333 |
| gnn_multiedge_covid_rsv_full | full | 16.646 | 105.980 | 10.543 | -0.093 | 80.952 |
| gnn_multiedge | post_covid | 16.771 | 102.819 | 10.472 | 0.188 | 83.333 |
| gnn_multiedge_rt | post_covid | 16.838 | 98.292 | 11.169 | 0.120 | 76.190 |
| gnn_uniform | post_covid | 16.999 | 96.605 | 10.796 | 0.115 | 80.952 |
| gnn_corrbinary | post_covid | 17.611 | 110.554 | 11.047 | 0.013 | 80.952 |
| gnn_multiedge_covid_rsv | post_covid | 17.982 | 94.533 | 11.024 | 0.056 | 80.952 |
| arima | exclude_covid | 20.371 | 106.595 | 11.566 | 0.211 | 97.619 |
| persistence | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |
| persistence | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 83.333 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 83.333 |
| dualtopo | post_covid | 47.629 | 189.569 | 24.411 | 0.084 | 66.667 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 15.118 | 151.390 | 11.141 | 0.098 | 84.000 |
| dualtopo_no_bg | post_covid | 15.176 | 161.390 | 10.659 | 0.062 | 84.000 |
| arima | post_covid | 15.513 | 139.219 | 10.367 |  | 84.000 |
| gnn_multiedge_level | post_covid | 16.199 | 121.312 | 11.878 | 0.070 | 84.000 |
| lstm | exclude_covid | 16.800 | 108.812 | 13.178 | 0.156 | 92.000 |
| gnn_multiedge_season_level | post_covid | 18.244 | 128.767 | 14.483 | 0.130 | 92.000 |
| gnn_geo | post_covid | 19.093 | 100.022 | 13.898 | -0.059 | 72.000 |
| dualtopo_fullhistory | full | 20.025 | 109.819 | 14.170 | -0.038 | 92.000 |
| gnn_multiedge_leaknorm | post_covid | 20.073 | 108.939 | 14.658 | -0.055 | 68.000 |
| gnn_multiedge_season | post_covid | 20.375 | 98.235 | 14.884 | -0.036 | 76.000 |
| gnn_multiedge_full | full | 20.673 | 123.480 | 14.705 | 0.048 | 92.000 |
| gnn_multiedge_rt | post_covid | 21.006 | 96.137 | 15.451 | -0.056 | 64.000 |
| gnn_multiedge_covid_rsv_full | full | 21.326 | 125.055 | 15.630 | -0.265 | 68.000 |
| gnn_multiedge | post_covid | 21.374 | 124.276 | 15.566 | -0.043 | 72.000 |
| gnn_uniform | post_covid | 21.591 | 113.187 | 15.834 | -0.124 | 76.000 |
| gnn_corrbinary | post_covid | 22.247 | 133.666 | 16.216 | -0.229 | 72.000 |
| gnn_multiedge_covid_rsv | post_covid | 23.133 | 110.889 | 16.585 | -0.129 | 68.000 |
| arima | exclude_covid | 26.280 | 140.509 | 17.770 | 0.006 | 96.000 |
| persistence | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |
| persistence | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 72.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 72.000 |
| dualtopo | post_covid | 61.649 | 269.800 | 39.195 | -0.092 | 44.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.083 | 60.986 | 2.401 | 0.464 | 100.000 |
| arima | exclude_covid | 3.089 | 56.721 | 2.444 | 0.283 | 100.000 |
| persistence | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| persistence | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 3.450 | 70.481 | 2.846 | 0.429 | 100.000 |
| dualtopo | post_covid | 3.948 | 71.584 | 2.669 | 0.398 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.963 | 77.928 | 3.061 | 0.170 | 100.000 |
| gnn_multiedge_full | full | 4.070 | 75.550 | 3.122 | 0.208 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 4.289 | 64.728 | 2.815 | 0.334 | 100.000 |
| gnn_multiedge | post_covid | 4.801 | 71.266 | 2.982 | 0.339 | 100.000 |
| gnn_multiedge_level | post_covid | 4.951 | 76.422 | 3.254 | 0.416 | 100.000 |
| gnn_uniform | post_covid | 5.326 | 72.222 | 3.388 | 0.266 | 88.235 |
| gnn_geo | post_covid | 5.422 | 63.656 | 3.130 | 0.074 | 94.118 |
| gnn_multiedge_season_level | post_covid | 6.145 | 83.320 | 4.001 | 0.410 | 94.118 |
| gnn_corrbinary | post_covid | 6.198 | 76.565 | 3.445 | 0.173 | 94.118 |
| gnn_multiedge_season | post_covid | 7.008 | 87.616 | 4.103 | 0.247 | 94.118 |
| gnn_multiedge_rt | post_covid | 7.182 | 101.462 | 4.873 | 0.322 | 94.118 |
| lstm | exclude_covid | 7.574 | 118.236 | 4.413 | 0.237 | 100.000 |
| lstm | post_covid | 8.603 | 256.513 | 8.158 | 0.346 | 100.000 |
| arima | post_covid | 8.911 | 266.350 | 8.430 |  | 100.000 |
| dualtopo_no_bg | post_covid | 10.751 | 319.577 | 10.356 | 0.023 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 10.992 | 81.373 | 6.338 | 0.475 | 89.130 |
| gnn_multiedge_season_level | post_covid | 11.780 | 81.518 | 7.665 | 0.480 | 95.652 |
| lstm | exclude_covid | 12.234 | 111.618 | 8.197 | 0.402 | 95.652 |
| lstm | post_covid | 12.316 | 222.493 | 9.094 | 0.327 | 95.652 |
| arima | post_covid | 12.483 | 205.731 | 8.771 |  | 91.304 |
| dualtopo_fullhistory | full | 12.655 | 65.191 | 7.000 | 0.348 | 95.652 |
| dualtopo_no_bg | post_covid | 12.693 | 234.827 | 9.366 | -0.095 | 95.652 |
| gnn_geo | post_covid | 14.222 | 110.226 | 9.458 | 0.220 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 14.515 | 119.349 | 9.591 | 0.224 | 86.957 |
| gnn_multiedge_full | full | 14.558 | 133.776 | 9.740 | 0.300 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 14.701 | 128.009 | 9.295 | 0.021 | 82.609 |
| gnn_multiedge | post_covid | 15.197 | 129.506 | 9.932 | 0.262 | 86.957 |
| gnn_multiedge_season | post_covid | 15.334 | 118.857 | 10.196 | 0.221 | 80.435 |
| gnn_corrbinary | post_covid | 15.375 | 126.719 | 10.199 | 0.176 | 86.957 |
| gnn_multiedge_rt | post_covid | 15.702 | 109.459 | 10.463 | 0.195 | 76.087 |
| gnn_multiedge_covid_rsv | post_covid | 16.046 | 122.749 | 10.322 | 0.115 | 80.435 |
| gnn_uniform | post_covid | 16.097 | 111.530 | 10.444 | 0.161 | 82.609 |
| arima | exclude_covid | 17.223 | 129.697 | 10.338 | 0.250 | 97.826 |
| persistence | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| persistence | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 78.261 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 78.261 |
| dualtopo | post_covid | 33.226 | 157.958 | 18.026 | 0.160 | 71.739 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 14.080 | 96.619 | 9.126 | 0.051 | 92.308 |
| dualtopo_no_bg | post_covid | 14.232 | 92.690 | 9.014 | 0.031 | 92.308 |
| gnn_multiedge_level | post_covid | 14.254 | 70.987 | 9.041 | 0.171 | 80.769 |
| arima | post_covid | 14.645 | 83.761 | 9.136 |  | 84.615 |
| lstm | exclude_covid | 15.083 | 75.547 | 10.800 | 0.183 | 92.308 |
| gnn_multiedge_season_level | post_covid | 15.136 | 81.870 | 11.121 | 0.215 | 92.308 |
| dualtopo_fullhistory | full | 16.713 | 71.556 | 10.943 | 0.079 | 92.308 |
| gnn_geo | post_covid | 18.145 | 101.406 | 13.512 | 0.005 | 65.385 |
| gnn_multiedge_leaknorm | post_covid | 18.639 | 106.390 | 13.631 | -0.041 | 76.923 |
| gnn_multiedge_full | full | 18.720 | 119.048 | 13.910 | 0.060 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 19.038 | 111.139 | 13.258 | -0.197 | 69.231 |
| gnn_multiedge_season | post_covid | 19.365 | 99.453 | 14.239 | 0.028 | 69.231 |
| gnn_multiedge | post_covid | 19.476 | 116.703 | 14.069 | 0.003 | 76.923 |
| gnn_corrbinary | post_covid | 19.580 | 119.215 | 14.430 | -0.096 | 76.923 |
| gnn_multiedge_rt | post_covid | 19.895 | 96.932 | 14.762 | 0.010 | 69.231 |
| gnn_uniform | post_covid | 20.721 | 108.321 | 15.106 | -0.099 | 80.769 |
| gnn_multiedge_covid_rsv | post_covid | 20.843 | 114.319 | 15.086 | -0.113 | 69.231 |
| arima | exclude_covid | 22.599 | 133.712 | 15.568 | -0.017 | 96.154 |
| persistence | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| persistence | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 65.385 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 65.385 |
| dualtopo | post_covid | 44.065 | 181.929 | 29.420 | -0.041 | 50.000 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.287 | 56.917 | 1.875 | 0.735 | 100.000 |
| gnn_multiedge_level | post_covid | 3.705 | 94.874 | 2.825 | 0.662 | 100.000 |
| dualtopo | post_covid | 3.856 | 126.797 | 3.214 | 0.625 | 100.000 |
| arima | exclude_covid | 4.279 | 124.477 | 3.539 | 0.439 | 100.000 |
| gnn_multiedge_season_level | post_covid | 4.618 | 81.061 | 3.172 | 0.651 | 100.000 |
| persistence | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| persistence | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 95.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 95.000 |
| gnn_multiedge_covid_rsv_full | full | 5.088 | 149.941 | 4.142 | 0.186 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.235 | 133.709 | 4.130 | 0.313 | 95.000 |
| gnn_multiedge_full | full | 5.642 | 152.921 | 4.318 | 0.288 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.737 | 136.195 | 4.339 | 0.394 | 100.000 |
| gnn_geo | post_covid | 6.100 | 121.693 | 4.187 | 0.332 | 95.000 |
| gnn_uniform | post_covid | 6.146 | 115.700 | 4.385 | 0.413 | 85.000 |
| gnn_multiedge | post_covid | 6.175 | 146.151 | 4.554 | 0.410 | 100.000 |
| gnn_corrbinary | post_covid | 6.734 | 136.475 | 4.698 | 0.368 | 100.000 |
| lstm | exclude_covid | 6.965 | 158.511 | 4.814 | 0.525 | 100.000 |
| gnn_multiedge_rt | post_covid | 7.248 | 125.745 | 4.874 | 0.440 | 85.000 |
| gnn_multiedge_season | post_covid | 7.299 | 144.083 | 4.940 | 0.472 | 95.000 |
| arima | post_covid | 8.920 | 364.292 | 8.297 |  | 100.000 |
| lstm | post_covid | 9.546 | 386.128 | 9.053 | 0.477 | 100.000 |
| dualtopo_no_bg | post_covid | 10.356 | 419.606 | 9.824 | -0.085 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 12.570 | 121.770 | 8.265 | 0.362 | 93.182 |
| gnn_multiedge_level | post_covid | 12.666 | 138.029 | 8.152 | 0.316 | 88.636 |
| dualtopo_fullhistory | full | 12.759 | 95.140 | 7.814 | 0.387 | 95.455 |
| lstm | post_covid | 13.013 | 243.609 | 10.125 | 0.321 | 93.182 |
| dualtopo_no_bg | post_covid | 13.384 | 256.663 | 10.442 | 0.069 | 93.182 |
| gnn_geo | post_covid | 13.535 | 100.856 | 8.348 | 0.267 | 86.364 |
| gnn_multiedge_season_level | post_covid | 14.169 | 151.654 | 9.843 | 0.329 | 90.909 |
| gnn_multiedge_covid_rsv_full | full | 14.479 | 112.362 | 8.638 | 0.091 | 88.636 |
| gnn_multiedge_leaknorm | post_covid | 14.513 | 143.518 | 9.645 | 0.181 | 88.636 |
| gnn_multiedge_full | full | 14.576 | 147.230 | 9.885 | 0.296 | 95.455 |
| gnn_multiedge_season | post_covid | 14.713 | 130.560 | 9.635 | 0.190 | 86.364 |
| gnn_multiedge | post_covid | 15.269 | 163.284 | 10.631 | 0.204 | 90.909 |
| gnn_multiedge_rt | post_covid | 15.343 | 129.447 | 9.987 | 0.132 | 81.818 |
| gnn_multiedge_covid_rsv | post_covid | 15.534 | 118.512 | 9.666 | 0.082 | 86.364 |
| gnn_uniform | post_covid | 15.657 | 134.693 | 10.053 | 0.123 | 86.364 |
| gnn_corrbinary | post_covid | 15.879 | 142.524 | 10.243 | 0.047 | 88.636 |
| arima | exclude_covid | 17.089 | 151.094 | 11.015 | 0.262 | 100.000 |
| arima | post_covid | 17.513 | 146.814 | 10.953 | 0.277 | 81.818 |
| persistence | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| persistence | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 81.818 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 81.818 |
| dualtopo | post_covid | 45.762 | 332.873 | 23.466 | -0.004 | 70.455 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 14.959 | 161.129 | 10.654 | 0.044 | 88.000 |
| dualtopo_no_bg | post_covid | 15.022 | 157.856 | 10.498 | -0.052 | 88.000 |
| lstm | exclude_covid | 16.093 | 144.140 | 12.156 | 0.120 | 88.000 |
| gnn_multiedge_level | post_covid | 16.440 | 174.864 | 12.179 | -0.064 | 80.000 |
| dualtopo_fullhistory | full | 16.801 | 123.700 | 12.377 | 0.162 | 92.000 |
| gnn_geo | post_covid | 17.478 | 107.895 | 12.268 | 0.017 | 80.000 |
| gnn_multiedge_season_level | post_covid | 18.287 | 204.818 | 14.777 | 0.008 | 84.000 |
| gnn_multiedge_season | post_covid | 18.745 | 143.988 | 13.880 | -0.068 | 80.000 |
| gnn_multiedge_covid_rsv_full | full | 18.877 | 110.113 | 12.584 | -0.122 | 80.000 |
| gnn_multiedge_leaknorm | post_covid | 18.898 | 174.585 | 14.682 | -0.150 | 80.000 |
| gnn_multiedge_full | full | 18.957 | 165.025 | 14.729 | 0.039 | 92.000 |
| gnn_multiedge_rt | post_covid | 19.710 | 158.863 | 14.898 | -0.138 | 80.000 |
| gnn_multiedge | post_covid | 19.829 | 201.310 | 16.161 | -0.121 | 84.000 |
| gnn_uniform | post_covid | 20.329 | 177.036 | 15.601 | -0.218 | 80.000 |
| gnn_multiedge_covid_rsv | post_covid | 20.382 | 144.403 | 15.079 | -0.186 | 76.000 |
| gnn_corrbinary | post_covid | 20.490 | 174.204 | 15.604 | -0.309 | 80.000 |
| arima | exclude_covid | 22.458 | 189.639 | 17.296 | 0.000 | 100.000 |
| arima | post_covid | 23.047 | 183.359 | 17.225 | 0.031 | 68.000 |
| persistence | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |
| persistence | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 68.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 68.000 |
| dualtopo | post_covid | 60.633 | 515.063 | 39.280 | -0.219 | 48.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.355 | 57.562 | 1.811 | 0.722 | 100.000 |
| arima | post_covid | 3.371 | 98.728 | 2.701 | 0.497 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 3.494 | 84.445 | 2.543 | 0.576 | 100.000 |
| dualtopo | post_covid | 3.514 | 93.150 | 2.658 | 0.640 | 100.000 |
| arima | exclude_covid | 3.561 | 100.375 | 2.751 | 0.533 | 100.000 |
| persistence | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| persistence | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gnn_multiedge_level | post_covid | 3.986 | 89.561 | 2.853 | 0.676 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.076 | 115.321 | 3.447 | 0.270 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 4.221 | 102.640 | 3.017 | 0.531 | 100.000 |
| gnn_multiedge_full | full | 4.375 | 123.816 | 3.511 | 0.325 | 100.000 |
| gnn_geo | post_covid | 4.719 | 91.594 | 3.191 | 0.244 | 94.737 |
| gnn_multiedge | post_covid | 4.748 | 113.250 | 3.356 | 0.544 | 100.000 |
| gnn_uniform | post_covid | 4.890 | 78.980 | 2.753 | 0.489 | 94.737 |
| gnn_multiedge_season_level | post_covid | 4.988 | 81.702 | 3.352 | 0.667 | 100.000 |
| lstm | exclude_covid | 5.011 | 92.335 | 3.146 | 0.530 | 100.000 |
| gnn_corrbinary | post_covid | 5.611 | 100.840 | 3.190 | 0.393 | 100.000 |
| gnn_multiedge_rt | post_covid | 5.828 | 90.740 | 3.524 | 0.589 | 84.211 |
| gnn_multiedge_season | post_covid | 6.244 | 112.891 | 4.050 | 0.528 | 94.737 |
| lstm | post_covid | 9.885 | 352.135 | 9.429 | 0.606 | 100.000 |
| dualtopo_no_bg | post_covid | 10.858 | 386.672 | 10.368 | 0.449 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 13.400 | 136.752 | 8.573 | 0.299 | 86.957 |
| lstm | exclude_covid | 13.730 | 128.431 | 9.077 | 0.291 | 95.652 |
| dualtopo_no_bg | post_covid | 14.226 | 266.687 | 10.961 | -0.085 | 93.478 |
| lstm | post_covid | 14.310 | 269.425 | 11.324 | 0.092 | 93.478 |
| gnn_multiedge_season_level | post_covid | 14.474 | 140.378 | 9.815 | 0.303 | 93.478 |
| gnn_multiedge_leaknorm | post_covid | 14.868 | 122.115 | 9.397 | 0.186 | 82.609 |
| gnn_multiedge_full | full | 14.948 | 148.167 | 9.773 | 0.269 | 97.826 |
| gnn_geo | post_covid | 15.067 | 117.471 | 9.216 | 0.137 | 82.609 |
| dualtopo_fullhistory | full | 15.280 | 121.332 | 9.051 | 0.177 | 95.652 |
| gnn_multiedge_season | post_covid | 15.445 | 116.723 | 9.791 | 0.159 | 76.087 |
| gnn_uniform | post_covid | 15.563 | 115.416 | 9.501 | 0.156 | 84.783 |
| gnn_multiedge_covid_rsv_full | full | 15.649 | 128.925 | 9.658 | -0.031 | 86.957 |
| gnn_multiedge | post_covid | 15.717 | 142.020 | 10.118 | 0.199 | 80.435 |
| gnn_multiedge_rt | post_covid | 15.894 | 113.464 | 9.923 | 0.130 | 73.913 |
| gnn_corrbinary | post_covid | 16.203 | 126.562 | 9.724 | 0.064 | 82.609 |
| gnn_multiedge_covid_rsv | post_covid | 16.566 | 123.672 | 10.012 | 0.049 | 80.435 |
| arima | post_covid | 16.792 | 131.304 | 10.233 | 0.233 | 73.913 |
| arima | exclude_covid | 17.502 | 139.288 | 10.412 | 0.259 | 100.000 |
| persistence | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| persistence | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 73.913 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 73.913 |
| dualtopo | post_covid | 35.564 | 241.978 | 19.233 | -0.009 | 71.739 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_no_bg | post_covid | 16.863 | 158.660 | 11.562 | -0.138 | 87.500 |
| lstm | post_covid | 17.104 | 170.455 | 12.411 | -0.237 | 87.500 |
| gnn_multiedge_level | post_covid | 18.090 | 154.980 | 13.416 | -0.110 | 75.000 |
| lstm | exclude_covid | 18.444 | 140.211 | 14.457 | -0.026 | 91.667 |
| gnn_multiedge_season_level | post_covid | 19.533 | 178.052 | 15.845 | -0.062 | 87.500 |
| gnn_multiedge_leaknorm | post_covid | 20.356 | 153.017 | 15.486 | -0.153 | 70.833 |
| gnn_multiedge_full | full | 20.357 | 182.151 | 15.708 | -0.026 | 95.833 |
| gnn_geo | post_covid | 20.585 | 148.618 | 14.914 | -0.157 | 70.833 |
| dualtopo_fullhistory | full | 21.008 | 151.734 | 15.323 | -0.137 | 91.667 |
| gnn_multiedge_season | post_covid | 21.084 | 150.581 | 16.087 | -0.120 | 62.500 |
| gnn_multiedge_covid_rsv_full | full | 21.190 | 132.952 | 14.986 | -0.259 | 75.000 |
| gnn_uniform | post_covid | 21.361 | 162.667 | 16.093 | -0.195 | 79.167 |
| gnn_multiedge | post_covid | 21.523 | 185.605 | 16.770 | -0.130 | 66.667 |
| gnn_multiedge_rt | post_covid | 21.749 | 154.614 | 16.626 | -0.136 | 58.333 |
| gnn_corrbinary | post_covid | 22.224 | 168.011 | 16.236 | -0.280 | 75.000 |
| gnn_multiedge_covid_rsv | post_covid | 22.651 | 150.917 | 16.501 | -0.223 | 66.667 |
| arima | post_covid | 23.147 | 187.682 | 17.766 | -0.066 | 50.000 |
| arima | exclude_covid | 24.047 | 195.532 | 17.607 | -0.004 | 100.000 |
| persistence | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| persistence | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 50.000 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 50.000 |
| dualtopo | post_covid | 49.090 | 344.541 | 33.705 | -0.241 | 45.833 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2.257 | 69.800 | 2.016 | 0.589 | 100.000 |
| dualtopo_fullhistory | full | 2.594 | 88.167 | 2.208 | 0.769 | 100.000 |
| gnn_uniform | post_covid | 2.940 | 63.870 | 2.310 | 0.473 | 90.909 |
| arima | exclude_covid | 3.109 | 77.930 | 2.563 | 0.051 | 100.000 |
| gnn_corrbinary | post_covid | 3.182 | 81.345 | 2.621 | 0.403 | 90.909 |
| gnn_multiedge_leaknorm | post_covid | 3.188 | 88.403 | 2.755 | 0.407 | 95.455 |
| gnn_multiedge | post_covid | 3.341 | 94.473 | 2.861 | 0.441 | 95.455 |
| gnn_multiedge_rt | post_covid | 3.491 | 68.573 | 2.611 | 0.647 | 90.909 |
| gnn_geo | post_covid | 3.524 | 83.492 | 3.001 | 0.140 | 95.455 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| persistence | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| persistence | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gnn_multiedge_season | post_covid | 3.716 | 79.788 | 2.923 | 0.577 | 90.909 |
| gnn_multiedge_covid_rsv | post_covid | 3.751 | 93.951 | 2.934 | 0.187 | 95.455 |
| gnn_multiedge_full | full | 3.887 | 111.095 | 3.298 | 0.069 | 100.000 |
| dualtopo | post_covid | 3.954 | 130.092 | 3.444 | 0.715 | 100.000 |
| gnn_multiedge_level | post_covid | 4.296 | 116.866 | 3.290 | 0.647 | 100.000 |
| gnn_multiedge_season_level | post_covid | 4.669 | 99.279 | 3.238 | 0.698 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.714 | 124.533 | 3.845 | -0.138 | 100.000 |
| lstm | exclude_covid | 4.801 | 115.580 | 3.209 | 0.528 | 100.000 |
| lstm | post_covid | 10.442 | 377.392 | 10.138 | 0.585 | 100.000 |
| dualtopo_no_bg | post_covid | 10.628 | 384.534 | 10.306 | 0.270 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 4.534 | 68.687 | 3.129 | 0.579 | 100.000 |
| gnn_multiedge_level | post_covid | 4.707 | 106.371 | 3.799 | 0.605 | 97.674 |
| lstm | exclude_covid | 5.720 | 104.142 | 4.233 | 0.500 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.824 | 108.893 | 4.612 | 0.588 | 100.000 |
| arima | post_covid | 6.210 | 203.160 | 5.471 | 0.464 | 100.000 |
| dualtopo_no_bg | post_covid | 6.254 | 205.518 | 5.521 | -0.012 | 100.000 |
| lstm | post_covid | 6.320 | 211.449 | 5.619 | 0.686 | 100.000 |
| gnn_geo | post_covid | 6.445 | 96.554 | 4.661 | 0.347 | 88.372 |
| gnn_multiedge_full | full | 6.676 | 101.222 | 4.680 | 0.440 | 97.674 |
| gnn_multiedge_covid_rsv_full | full | 6.778 | 102.303 | 4.676 | 0.091 | 90.698 |
| gnn_multiedge_leaknorm | post_covid | 6.987 | 96.919 | 4.806 | 0.374 | 93.023 |
| gnn_multiedge_season | post_covid | 7.008 | 111.834 | 5.222 | 0.371 | 83.721 |
| gnn_corrbinary | post_covid | 7.119 | 103.648 | 4.924 | 0.367 | 93.023 |
| gnn_multiedge_rt | post_covid | 7.148 | 102.539 | 5.211 | 0.354 | 83.721 |
| gnn_multiedge | post_covid | 7.374 | 101.770 | 5.065 | 0.400 | 93.023 |
| gnn_uniform | post_covid | 7.402 | 102.545 | 5.288 | 0.346 | 86.047 |
| gnn_multiedge_covid_rsv | post_covid | 7.503 | 94.846 | 5.007 | 0.288 | 90.698 |
| arima | exclude_covid | 9.318 | 99.588 | 5.734 | 0.454 | 100.000 |
| persistence | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| persistence | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 93.023 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 93.023 |
| dualtopo | post_covid | 16.335 | 167.408 | 9.203 | 0.180 | 81.395 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 5.373 | 66.804 | 4.506 | 0.351 | 96.000 |
| lstm | post_covid | 5.390 | 91.596 | 4.509 | 0.549 | 100.000 |
| arima | post_covid | 5.439 | 87.099 | 4.465 | 0.226 | 100.000 |
| dualtopo_no_bg | post_covid | 5.442 | 87.989 | 4.484 | 0.112 | 100.000 |
| dualtopo_fullhistory | full | 5.618 | 41.339 | 4.001 | 0.369 | 100.000 |
| lstm | exclude_covid | 6.253 | 59.348 | 4.883 | 0.297 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.847 | 77.166 | 5.938 | 0.347 | 100.000 |
| gnn_geo | post_covid | 8.117 | 85.091 | 6.459 | 0.047 | 84.000 |
| gnn_multiedge_full | full | 8.398 | 88.893 | 6.457 | 0.155 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 8.553 | 91.466 | 6.422 | -0.227 | 84.000 |
| gnn_multiedge_season | post_covid | 8.662 | 83.307 | 7.002 | 0.125 | 88.000 |
| gnn_multiedge_leaknorm | post_covid | 8.823 | 85.721 | 6.742 | 0.088 | 88.000 |
| gnn_multiedge_rt | post_covid | 8.922 | 75.550 | 7.065 | 0.111 | 84.000 |
| gnn_corrbinary | post_covid | 8.977 | 92.003 | 6.915 | 0.057 | 92.000 |
| gnn_multiedge | post_covid | 9.340 | 92.901 | 7.272 | 0.107 | 88.000 |
| gnn_uniform | post_covid | 9.372 | 86.687 | 7.381 | 0.039 | 88.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.536 | 81.036 | 7.006 | 0.038 | 84.000 |
| arima | exclude_covid | 12.008 | 102.713 | 8.386 | 0.220 | 100.000 |
| persistence | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| persistence | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 88.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 88.000 |
| dualtopo | post_covid | 21.186 | 156.053 | 13.499 | -0.031 | 68.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.297 | 106.670 | 1.918 | 0.277 | 100.000 |
| arima | exclude_covid | 2.670 | 95.247 | 2.051 | 0.118 | 100.000 |
| gnn_geo | post_covid | 2.783 | 112.476 | 2.165 | 0.366 | 94.444 |
| gnn_multiedge_covid_rsv_full | full | 2.856 | 117.355 | 2.251 | -0.020 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 2.864 | 114.027 | 2.232 | 0.008 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 2.915 | 112.471 | 2.118 | 0.153 | 100.000 |
| gnn_multiedge_full | full | 2.919 | 118.346 | 2.211 | 0.100 | 100.000 |
| gnn_multiedge | post_covid | 2.955 | 114.088 | 1.999 | 0.217 | 100.000 |
| gnn_uniform | post_covid | 2.980 | 124.570 | 2.381 | 0.307 | 83.333 |
| gnn_corrbinary | post_covid | 3.026 | 119.823 | 2.158 | 0.307 | 94.444 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| persistence | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| persistence | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| gnn_multiedge_rt | post_covid | 3.395 | 140.022 | 2.637 | 0.312 | 83.333 |
| gnn_multiedge_level | post_covid | 3.583 | 161.326 | 2.816 | 0.464 | 100.000 |
| gnn_multiedge_season | post_covid | 3.621 | 151.456 | 2.749 | 0.282 | 77.778 |
| dualtopo | post_covid | 3.749 | 183.179 | 3.235 | 0.527 | 100.000 |
| gnn_multiedge_season_level | post_covid | 3.988 | 152.959 | 2.770 | 0.451 | 100.000 |
| lstm | exclude_covid | 4.884 | 166.356 | 3.331 | 0.588 | 100.000 |
| arima | post_covid | 7.144 | 364.356 | 6.868 | 0.197 | 100.000 |
| dualtopo_no_bg | post_covid | 7.233 | 368.751 | 6.961 | 0.253 | 100.000 |
| lstm | post_covid | 7.420 | 377.912 | 7.160 | 0.196 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
