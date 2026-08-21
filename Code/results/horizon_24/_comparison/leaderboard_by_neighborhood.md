# Per-neighborhood leaderboard — horizon 24

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_multiedge_season | 6 | 2 | 0 |
| gnn_multiedge_season_level | 3 | 1 | 0 |
| gnn_geo | 2 | 4 | 0 |
| gnn_multiedge_level | 2 | 0 | 2 |
| gnn_multiedge_covid_rsv_full | 1 | 4 | 0 |
| dualtopo_fullhistory | 0 | 0 | 7 |
| gnn_multiedge_rt | 0 | 1 | 0 |
| gnn_uniform | 0 | 2 | 0 |
| seasonal_naive | 0 | 0 | 5 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_geo (post_covid)`: E.Boston, W.Roxbury; `gnn_multiedge_covid_rsv_full (full)`: HydePark; `gnn_multiedge_level (post_covid)`: Charles., S.Boston; `gnn_multiedge_season (post_covid)`: Dorchest., Fenway, JP, Mattapan, Roxbury, S.End; `gnn_multiedge_season_level (post_covid)`: Allston, BackBay+, Roslind.
- **Flu season (Oct–Mar)** — `gnn_geo (post_covid)`: Charles., E.Boston, Roslind., W.Roxbury; `gnn_multiedge_covid_rsv_full (full)`: Dorchest., HydePark, Mattapan, Roxbury; `gnn_multiedge_rt (post_covid)`: Fenway; `gnn_multiedge_season (post_covid)`: Allston, BackBay+; `gnn_multiedge_season_level (post_covid)`: S.Boston; `gnn_uniform (post_covid)`: JP, S.End
- **Off-season (Apr–Sep)** — `dualtopo_fullhistory (full)`: Allston, BackBay+, Fenway, JP, Mattapan, S.End, W.Roxbury; `gnn_multiedge_level (post_covid)`: Charles., Roslind.; `seasonal_naive (exclude_covid)`: Dorchest., E.Boston, HydePark, Roxbury, S.Boston

`gnn_multiedge_season (post_covid)` wins 6 of 14 neighborhoods. `gnn_multiedge_season (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.2 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 45.044 | 98.498 | 32.840 | 0.735 | 85.714 |
| gnn_multiedge_full | full | 45.739 | 112.093 | 36.129 | 0.677 | 100.000 |
| gnn_uniform | post_covid | 45.805 | 127.792 | 34.561 | 0.739 | 97.959 |
| gnn_multiedge_covid_rsv_full | full | 45.821 | 133.614 | 33.807 | 0.584 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 47.650 | 100.956 | 35.889 | 0.727 | 77.551 |
| gnn_multiedge_leaknorm | post_covid | 47.763 | 129.408 | 35.546 | 0.723 | 95.918 |
| gnn_multiedge_season_level | post_covid | 48.742 | 105.495 | 35.997 | 0.747 | 93.878 |
| gnn_geo | post_covid | 48.798 | 149.130 | 37.350 | 0.741 | 89.796 |
| arima | post_covid | 51.021 | 159.036 | 40.330 | 0.469 | 87.755 |
| gnn_multiedge_level | post_covid | 51.039 | 133.262 | 38.725 | 0.750 | 97.959 |
| gnn_multiedge | post_covid | 53.125 | 116.071 | 36.893 | 0.742 | 91.837 |
| dualtopo_fullhistory | full | 55.970 | 70.206 | 27.897 | 0.245 | 85.714 |
| gnn_multiedge_rt | post_covid | 57.066 | 141.702 | 43.292 | 0.645 | 87.755 |
| arima | exclude_covid | 57.833 | 273.046 | 45.523 |  | 95.918 |
| dualtopo_no_bg | post_covid | 61.033 | 314.848 | 51.417 | 0.435 | 44.898 |
| dualtopo | post_covid | 61.112 | 315.736 | 51.535 | 0.435 | 44.898 |
| lstm | exclude_covid | 64.673 | 185.278 | 52.719 | 0.654 | 89.796 |
| gnn_corrbinary | post_covid | 68.369 | 130.281 | 47.616 | 0.743 | 67.347 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| lstm | post_covid | 85.206 | 206.865 | 64.116 | 0.571 | 61.224 |
| persistence | exclude_covid | 111.589 | 557.692 | 77.574 | -0.421 | 79.592 |
| persistence | post_covid | 111.589 | 557.692 | 77.574 | -0.421 | 79.592 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 56.600 | 84.985 | 45.324 | 0.471 | 100.000 |
| gnn_uniform | post_covid | 58.902 | 88.303 | 49.387 | 0.640 | 100.000 |
| gnn_multiedge_full | full | 59.408 | 101.212 | 52.345 | 0.514 | 100.000 |
| gnn_multiedge_season | post_covid | 60.205 | 97.777 | 50.984 | 0.612 | 100.000 |
| arima | post_covid | 60.504 | 99.867 | 47.575 | 0.346 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 61.082 | 94.550 | 50.630 | 0.618 | 100.000 |
| gnn_geo | post_covid | 61.566 | 103.073 | 52.241 | 0.663 | 96.154 |
| dualtopo_no_bg | post_covid | 62.786 | 103.516 | 45.833 | 0.254 | 65.385 |
| dualtopo | post_covid | 62.788 | 103.796 | 45.905 | 0.207 | 65.385 |
| arima | exclude_covid | 63.292 | 87.181 | 42.024 |  | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 63.806 | 111.042 | 56.880 | 0.614 | 96.154 |
| gnn_multiedge_season_level | post_covid | 64.501 | 99.150 | 54.447 | 0.635 | 96.154 |
| gnn_multiedge_level | post_covid | 67.573 | 112.277 | 58.310 | 0.633 | 96.154 |
| gnn_multiedge | post_covid | 70.453 | 102.967 | 55.625 | 0.629 | 100.000 |
| gnn_multiedge_rt | post_covid | 71.874 | 103.118 | 58.628 | 0.490 | 100.000 |
| dualtopo_fullhistory | full | 76.191 | 43.850 | 44.368 | 0.029 | 73.077 |
| lstm | exclude_covid | 76.366 | 129.736 | 67.722 | 0.521 | 88.462 |
| persistence | exclude_covid | 90.182 | 73.887 | 62.702 | -0.537 | 84.615 |
| persistence | post_covid | 90.182 | 73.887 | 62.702 | -0.537 | 84.615 |
| gnn_corrbinary | post_covid | 91.949 | 158.183 | 77.631 | 0.640 | 65.385 |
| lstm | post_covid | 103.499 | 150.266 | 84.367 | 0.383 | 46.154 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| dualtopo_fullhistory | full | 10.561 | 99.999 | 9.276 | 0.763 | 100.000 |
| gnn_multiedge_season | post_covid | 15.006 | 99.314 | 12.329 | 0.686 | 69.565 |
| gnn_multiedge_covid_rsv | post_covid | 15.332 | 89.555 | 12.160 | 0.755 | 56.522 |
| gnn_multiedge_season_level | post_covid | 18.930 | 112.667 | 15.139 | 0.722 | 91.304 |
| gnn_multiedge_level | post_covid | 19.703 | 156.985 | 16.585 | 0.690 | 100.000 |
| gnn_corrbinary | post_covid | 20.019 | 98.739 | 13.686 | 0.715 | 69.565 |
| gnn_multiedge | post_covid | 20.043 | 130.884 | 15.716 | 0.527 | 82.609 |
| gnn_multiedge_full | full | 21.618 | 124.394 | 17.797 | 0.819 | 100.000 |
| gnn_uniform | post_covid | 23.408 | 172.432 | 17.802 | 0.332 | 95.652 |
| gnn_multiedge_leaknorm | post_covid | 25.346 | 168.812 | 18.494 | 0.395 | 91.304 |
| gnn_geo | post_covid | 28.076 | 201.194 | 20.517 | 0.272 | 82.609 |
| gnn_multiedge_covid_rsv_full | full | 29.181 | 188.585 | 20.789 | 0.384 | 100.000 |
| gnn_multiedge_rt | post_covid | 33.137 | 185.318 | 25.956 | 0.568 | 73.913 |
| arima | post_covid | 37.518 | 225.923 | 32.140 | 0.719 | 78.261 |
| lstm | exclude_covid | 48.151 | 248.065 | 35.759 | 0.777 | 91.304 |
| arima | exclude_covid | 50.962 | 483.155 | 49.480 |  | 100.000 |
| lstm | post_covid | 57.947 | 270.846 | 41.223 | 0.695 | 78.261 |
| dualtopo_no_bg | post_covid | 58.990 | 553.744 | 57.729 | 0.701 | 21.739 |
| dualtopo | post_covid | 59.161 | 555.321 | 57.899 | 0.676 | 21.739 |
| persistence | exclude_covid | 131.663 | 1104.601 | 94.387 | -0.580 | 73.913 |
| persistence | post_covid | 131.663 | 1104.601 | 94.387 | -0.580 | 73.913 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 42.586 | 128.630 | 31.242 | 0.695 | 93.878 |
| gnn_multiedge_covid_rsv_full | full | 42.714 | 151.069 | 31.069 | 0.573 | 97.959 |
| gnn_multiedge_season_level | post_covid | 43.736 | 109.305 | 32.615 | 0.712 | 93.878 |
| gnn_multiedge_leaknorm | post_covid | 43.961 | 155.027 | 32.580 | 0.714 | 97.959 |
| gnn_uniform | post_covid | 44.130 | 165.759 | 33.788 | 0.695 | 97.959 |
| gnn_multiedge_covid_rsv | post_covid | 44.714 | 118.679 | 34.049 | 0.678 | 77.551 |
| gnn_multiedge_level | post_covid | 44.855 | 134.803 | 34.011 | 0.725 | 97.959 |
| gnn_multiedge_full | full | 46.579 | 143.446 | 35.188 | 0.615 | 97.959 |
| gnn_multiedge | post_covid | 47.553 | 134.313 | 33.540 | 0.728 | 97.959 |
| gnn_geo | post_covid | 49.392 | 160.836 | 37.014 | 0.741 | 91.837 |
| arima | post_covid | 51.143 | 234.207 | 38.014 | 0.337 | 95.918 |
| dualtopo_fullhistory | full | 51.560 | 76.737 | 26.748 | 0.194 | 83.673 |
| gnn_multiedge_rt | post_covid | 52.188 | 178.351 | 39.459 | 0.572 | 89.796 |
| arima | exclude_covid | 53.186 | 271.532 | 42.292 |  | 95.918 |
| dualtopo_no_bg | post_covid | 54.280 | 288.162 | 44.381 | 0.419 | 57.143 |
| dualtopo | post_covid | 54.324 | 288.738 | 44.443 | 0.432 | 57.143 |
| gnn_corrbinary | post_covid | 62.016 | 148.648 | 44.578 | 0.706 | 85.714 |
| lstm | exclude_covid | 64.729 | 204.474 | 51.806 | 0.587 | 79.592 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 91.837 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| lstm | post_covid | 74.903 | 208.680 | 57.684 | 0.492 | 67.347 |
| persistence | exclude_covid | 99.096 | 527.975 | 67.135 | -0.397 | 81.633 |
| persistence | post_covid | 99.096 | 527.975 | 67.135 | -0.397 | 83.673 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 54.802 | 96.868 | 43.612 | 0.421 | 100.000 |
| gnn_uniform | post_covid | 56.091 | 98.151 | 46.553 | 0.614 | 100.000 |
| gnn_multiedge_season | post_covid | 56.220 | 105.274 | 46.870 | 0.592 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 56.876 | 103.709 | 46.852 | 0.628 | 100.000 |
| gnn_multiedge_season_level | post_covid | 58.116 | 115.231 | 49.801 | 0.612 | 96.154 |
| dualtopo | post_covid | 59.001 | 113.891 | 42.488 | 0.412 | 69.231 |
| dualtopo_no_bg | post_covid | 59.003 | 113.741 | 42.463 | 0.249 | 69.231 |
| arima | exclude_covid | 59.186 | 106.377 | 41.242 |  | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 59.583 | 117.745 | 52.057 | 0.563 | 84.615 |
| gnn_multiedge_level | post_covid | 59.729 | 124.584 | 51.703 | 0.628 | 96.154 |
| arima | post_covid | 59.985 | 92.676 | 39.077 | 0.170 | 92.308 |
| gnn_multiedge_full | full | 60.838 | 126.466 | 51.662 | 0.445 | 100.000 |
| gnn_multiedge | post_covid | 63.322 | 110.866 | 51.213 | 0.634 | 100.000 |
| gnn_geo | post_covid | 64.870 | 128.040 | 54.919 | 0.675 | 96.154 |
| gnn_multiedge_rt | post_covid | 65.724 | 110.985 | 52.315 | 0.424 | 100.000 |
| dualtopo_fullhistory | full | 70.001 | 51.308 | 41.819 | -0.052 | 69.231 |
| lstm | exclude_covid | 77.479 | 167.483 | 68.242 | 0.445 | 69.231 |
| persistence | exclude_covid | 80.881 | 63.004 | 52.392 | -0.259 | 88.462 |
| persistence | post_covid | 80.881 | 63.004 | 52.392 | -0.259 | 88.462 |
| gnn_corrbinary | post_covid | 83.539 | 174.793 | 72.592 | 0.612 | 84.615 |
| lstm | post_covid | 91.605 | 176.965 | 78.035 | 0.290 | 53.846 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 84.615 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| dualtopo_fullhistory | full | 11.148 | 105.483 | 9.713 | 0.667 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 15.693 | 119.736 | 13.692 | 0.600 | 69.565 |
| gnn_multiedge_level | post_covid | 15.922 | 146.354 | 14.012 | 0.647 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.039 | 102.607 | 13.188 | 0.649 | 91.304 |
| gnn_multiedge | post_covid | 16.879 | 160.818 | 13.562 | 0.480 | 95.652 |
| gnn_multiedge_season | post_covid | 17.050 | 155.031 | 13.576 | 0.384 | 86.957 |
| gnn_corrbinary | post_covid | 17.454 | 119.092 | 12.909 | 0.646 | 86.957 |
| gnn_multiedge_full | full | 20.931 | 162.640 | 16.564 | 0.627 | 95.652 |
| gnn_geo | post_covid | 20.983 | 197.910 | 16.774 | 0.337 | 86.957 |
| gnn_multiedge_leaknorm | post_covid | 21.455 | 213.039 | 16.446 | 0.265 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 22.179 | 212.340 | 16.889 | 0.377 | 95.652 |
| gnn_uniform | post_covid | 24.339 | 242.186 | 19.357 | 0.074 | 95.652 |
| gnn_multiedge_rt | post_covid | 30.320 | 254.504 | 24.926 | 0.283 | 78.261 |
| arima | post_covid | 38.791 | 394.200 | 36.812 | 0.500 | 100.000 |
| arima | exclude_covid | 45.459 | 458.229 | 43.478 |  | 100.000 |
| lstm | exclude_covid | 46.262 | 246.290 | 33.227 | 0.621 | 91.304 |
| dualtopo_no_bg | post_covid | 48.389 | 485.333 | 46.549 | 0.649 | 43.478 |
| dualtopo | post_covid | 48.495 | 486.390 | 46.653 | 0.633 | 43.478 |
| lstm | post_covid | 49.667 | 244.531 | 34.679 | 0.532 | 82.609 |
| persistence | exclude_covid | 116.300 | 1053.594 | 83.800 | -0.587 | 73.913 |
| persistence | post_covid | 116.300 | 1053.594 | 83.800 | -0.587 | 78.261 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 31.383 | 125.530 | 22.268 | 0.637 | 97.619 |
| gnn_multiedge_level | post_covid | 31.920 | 141.707 | 23.411 | 0.637 | 100.000 |
| gnn_multiedge_season | post_covid | 32.146 | 147.756 | 23.370 | 0.608 | 95.238 |
| gnn_multiedge | post_covid | 32.579 | 160.540 | 25.380 | 0.632 | 97.619 |
| gnn_geo | post_covid | 32.958 | 180.851 | 26.077 | 0.641 | 97.619 |
| gnn_multiedge_leaknorm | post_covid | 33.038 | 162.700 | 24.909 | 0.622 | 97.619 |
| gnn_multiedge_covid_rsv | post_covid | 33.145 | 143.184 | 24.755 | 0.594 | 90.476 |
| gnn_uniform | post_covid | 33.295 | 163.784 | 25.530 | 0.610 | 97.619 |
| gnn_multiedge_full | full | 34.912 | 167.884 | 26.322 | 0.523 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 35.605 | 158.065 | 24.692 | 0.428 | 100.000 |
| gnn_multiedge_rt | post_covid | 36.114 | 174.866 | 26.688 | 0.495 | 97.619 |
| arima | post_covid | 37.010 | 137.129 | 24.043 | 0.306 | 92.857 |
| gnn_corrbinary | post_covid | 37.945 | 193.677 | 30.430 | 0.612 | 97.619 |
| lstm | exclude_covid | 38.042 | 190.209 | 30.930 | 0.517 | 95.238 |
| arima | exclude_covid | 38.882 | 174.998 | 26.708 |  | 92.857 |
| dualtopo_no_bg | post_covid | 39.410 | 204.693 | 29.447 | 0.307 | 90.476 |
| dualtopo | post_covid | 39.429 | 205.325 | 29.504 | 0.318 | 90.476 |
| dualtopo_fullhistory | full | 40.620 | 81.815 | 20.508 | 0.084 | 88.095 |
| lstm | post_covid | 50.311 | 233.305 | 38.849 | 0.457 | 76.190 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 88.095 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |
| persistence | exclude_covid | 61.125 | 266.788 | 39.576 | -0.289 | 85.714 |
| persistence | post_covid | 61.125 | 266.788 | 39.576 | -0.289 | 92.857 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 38.793 | 184.603 | 32.867 | 0.628 | 100.000 |
| gnn_multiedge | post_covid | 38.884 | 171.378 | 32.198 | 0.598 | 100.000 |
| gnn_multiedge_season | post_covid | 39.116 | 166.755 | 31.154 | 0.565 | 100.000 |
| gnn_uniform | post_covid | 39.244 | 169.966 | 32.452 | 0.587 | 100.000 |
| gnn_multiedge_season_level | post_covid | 39.260 | 165.416 | 31.515 | 0.588 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 39.857 | 182.021 | 32.881 | 0.580 | 100.000 |
| gnn_multiedge_level | post_covid | 40.034 | 181.616 | 33.047 | 0.582 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 41.087 | 184.516 | 34.691 | 0.552 | 92.308 |
| gnn_multiedge_full | full | 41.835 | 170.393 | 33.509 | 0.461 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 42.091 | 144.541 | 30.527 | 0.431 | 100.000 |
| gnn_multiedge_rt | post_covid | 42.219 | 172.032 | 33.114 | 0.448 | 100.000 |
| lstm | exclude_covid | 44.925 | 207.039 | 38.504 | 0.443 | 92.308 |
| arima | post_covid | 45.461 | 127.895 | 31.045 | 0.289 | 92.308 |
| dualtopo | post_covid | 45.698 | 147.017 | 32.587 | 0.362 | 84.615 |
| dualtopo_no_bg | post_covid | 45.705 | 146.635 | 32.556 | 0.257 | 84.615 |
| arima | exclude_covid | 46.284 | 125.869 | 30.842 |  | 88.462 |
| gnn_corrbinary | post_covid | 46.406 | 237.787 | 41.501 | 0.581 | 100.000 |
| dualtopo_fullhistory | full | 51.159 | 82.488 | 28.549 | -0.058 | 80.769 |
| persistence | exclude_covid | 57.103 | 71.405 | 34.908 | -0.201 | 88.462 |
| persistence | post_covid | 57.103 | 71.405 | 34.908 | -0.201 | 92.308 |
| lstm | post_covid | 59.353 | 274.587 | 49.139 | 0.345 | 69.231 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 8.369 | 76.856 | 7.753 | 0.718 | 100.000 |
| dualtopo_fullhistory | full | 8.841 | 80.719 | 7.441 | 0.588 | 100.000 |
| gnn_multiedge_season_level | post_covid | 8.985 | 60.717 | 7.242 | 0.656 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.855 | 76.019 | 8.609 | 0.572 | 87.500 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 93.750 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| gnn_multiedge_season | post_covid | 15.043 | 116.882 | 10.723 | 0.332 | 87.500 |
| arima | post_covid | 15.401 | 152.136 | 12.665 | 0.452 | 93.750 |
| gnn_corrbinary | post_covid | 16.737 | 121.998 | 12.441 | 0.390 | 93.750 |
| gnn_multiedge_leaknorm | post_covid | 16.848 | 131.304 | 11.954 | 0.298 | 93.750 |
| gnn_multiedge | post_covid | 18.144 | 142.929 | 14.302 | 0.245 | 93.750 |
| gnn_multiedge_full | full | 18.852 | 163.807 | 14.643 | 0.278 | 100.000 |
| gnn_geo | post_covid | 20.147 | 174.754 | 15.043 | 0.106 | 93.750 |
| gnn_uniform | post_covid | 20.181 | 153.738 | 14.282 | 0.154 | 93.750 |
| gnn_multiedge_covid_rsv_full | full | 21.186 | 180.043 | 15.210 | 0.146 | 100.000 |
| arima | exclude_covid | 22.077 | 254.833 | 19.991 |  | 100.000 |
| lstm | exclude_covid | 22.786 | 162.860 | 18.622 | 0.584 | 100.000 |
| gnn_multiedge_rt | post_covid | 22.959 | 179.471 | 16.245 | 0.223 | 93.750 |
| dualtopo_no_bg | post_covid | 26.123 | 299.037 | 24.395 | 0.519 | 100.000 |
| dualtopo | post_covid | 26.219 | 300.076 | 24.494 | 0.508 | 100.000 |
| lstm | post_covid | 30.330 | 166.222 | 22.127 | 0.579 | 87.500 |
| persistence | exclude_covid | 67.148 | 584.284 | 47.163 | -0.404 | 81.250 |
| persistence | post_covid | 67.148 | 584.284 | 47.163 | -0.404 | 93.750 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 24.809 | 142.667 | 19.098 | 0.713 | 95.918 |
| gnn_multiedge_season_level | post_covid | 25.978 | 115.122 | 19.308 | 0.710 | 100.000 |
| gnn_uniform | post_covid | 26.427 | 170.079 | 21.235 | 0.695 | 97.959 |
| gnn_multiedge_covid_rsv | post_covid | 26.664 | 139.357 | 20.133 | 0.668 | 89.796 |
| gnn_multiedge_level | post_covid | 27.100 | 147.315 | 21.049 | 0.708 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 27.209 | 156.197 | 20.937 | 0.691 | 95.918 |
| gnn_multiedge_covid_rsv_full | full | 27.386 | 169.555 | 20.207 | 0.552 | 97.959 |
| gnn_multiedge_full | full | 27.993 | 158.069 | 22.699 | 0.620 | 100.000 |
| gnn_multiedge | post_covid | 28.222 | 154.755 | 21.797 | 0.699 | 95.918 |
| gnn_geo | post_covid | 28.633 | 175.428 | 22.523 | 0.715 | 97.959 |
| gnn_multiedge_rt | post_covid | 29.929 | 173.348 | 22.809 | 0.602 | 95.918 |
| arima | post_covid | 32.438 | 216.284 | 23.801 | -0.305 | 100.000 |
| dualtopo_fullhistory | full | 32.717 | 64.019 | 16.628 | 0.270 | 85.714 |
| arima | exclude_covid | 32.832 | 233.918 | 24.948 |  | 97.959 |
| dualtopo_no_bg | post_covid | 34.176 | 274.355 | 28.022 | 0.360 | 85.714 |
| dualtopo | post_covid | 34.197 | 274.806 | 28.055 | 0.376 | 85.714 |
| gnn_corrbinary | post_covid | 36.095 | 188.572 | 27.690 | 0.683 | 93.878 |
| lstm | exclude_covid | 37.811 | 202.005 | 29.750 | 0.584 | 100.000 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| lstm | post_covid | 44.006 | 235.408 | 33.873 | 0.511 | 75.510 |
| persistence | exclude_covid | 58.396 | 430.187 | 41.241 | -0.346 | 91.837 |
| persistence | post_covid | 58.396 | 430.187 | 41.241 | -0.346 | 95.918 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_uniform | post_covid | 32.032 | 124.950 | 27.140 | 0.660 | 100.000 |
| gnn_multiedge_season | post_covid | 32.072 | 141.046 | 27.219 | 0.656 | 100.000 |
| gnn_multiedge_season_level | post_covid | 34.181 | 143.771 | 29.670 | 0.639 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 34.336 | 142.967 | 28.898 | 0.630 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 34.379 | 160.424 | 27.963 | 0.499 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 34.759 | 182.903 | 30.212 | 0.606 | 100.000 |
| gnn_multiedge_full | full | 34.884 | 149.601 | 30.879 | 0.552 | 100.000 |
| gnn_multiedge | post_covid | 35.339 | 132.196 | 29.454 | 0.647 | 100.000 |
| gnn_multiedge_level | post_covid | 35.673 | 166.722 | 31.553 | 0.626 | 100.000 |
| gnn_geo | post_covid | 35.730 | 168.334 | 30.843 | 0.681 | 100.000 |
| gnn_multiedge_rt | post_covid | 37.084 | 147.502 | 30.697 | 0.501 | 100.000 |
| dualtopo | post_covid | 38.291 | 162.242 | 27.958 | 0.467 | 76.923 |
| dualtopo_no_bg | post_covid | 38.292 | 162.065 | 27.944 | 0.263 | 76.923 |
| arima | exclude_covid | 38.831 | 138.367 | 26.249 |  | 96.154 |
| arima | post_covid | 39.273 | 128.743 | 25.945 | -0.232 | 100.000 |
| dualtopo_fullhistory | full | 44.621 | 60.993 | 27.003 | 0.058 | 73.077 |
| lstm | exclude_covid | 44.839 | 207.862 | 40.090 | 0.487 | 100.000 |
| gnn_corrbinary | post_covid | 47.191 | 242.279 | 42.507 | 0.628 | 100.000 |
| persistence | exclude_covid | 50.425 | 80.349 | 33.377 | -0.283 | 92.308 |
| persistence | post_covid | 50.425 | 80.349 | 33.377 | -0.283 | 100.000 |
| lstm | post_covid | 51.545 | 229.140 | 44.605 | 0.377 | 69.231 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 5.448 | 67.439 | 4.900 | 0.607 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| gnn_multiedge_season_level | post_covid | 10.816 | 82.735 | 7.596 | 0.475 | 100.000 |
| gnn_multiedge_level | post_covid | 11.226 | 125.377 | 9.176 | 0.367 | 100.000 |
| gnn_multiedge_season | post_covid | 12.184 | 144.499 | 9.916 | 0.157 | 91.304 |
| gnn_multiedge_covid_rsv | post_covid | 12.200 | 90.131 | 8.738 | 0.347 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 15.636 | 171.153 | 11.938 | 0.074 | 91.304 |
| gnn_corrbinary | post_covid | 16.067 | 127.859 | 10.940 | 0.239 | 86.957 |
| gnn_multiedge_covid_rsv_full | full | 16.178 | 179.877 | 11.439 | 0.204 | 95.652 |
| gnn_multiedge | post_covid | 16.885 | 180.256 | 13.141 | -0.013 | 91.304 |
| gnn_multiedge_full | full | 17.141 | 167.642 | 13.452 | 0.276 | 100.000 |
| gnn_geo | post_covid | 17.421 | 183.448 | 13.119 | 0.048 | 95.652 |
| gnn_uniform | post_covid | 18.110 | 221.095 | 14.559 | -0.105 | 95.652 |
| gnn_multiedge_rt | post_covid | 18.807 | 202.565 | 13.891 | 0.266 | 91.304 |
| arima | post_covid | 22.318 | 315.243 | 21.377 | -0.234 | 100.000 |
| arima | exclude_covid | 24.330 | 341.932 | 23.476 |  | 100.000 |
| lstm | exclude_covid | 27.805 | 195.384 | 18.061 | 0.533 | 100.000 |
| dualtopo_no_bg | post_covid | 28.824 | 401.292 | 28.110 | 0.313 | 95.652 |
| dualtopo | post_covid | 28.879 | 402.051 | 28.165 | 0.300 | 95.652 |
| lstm | post_covid | 33.499 | 242.495 | 21.740 | 0.464 | 82.609 |
| persistence | exclude_covid | 66.262 | 825.656 | 50.130 | -0.341 | 91.304 |
| persistence | post_covid | 66.262 | 825.656 | 50.130 | -0.341 | 91.304 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 19.534 | 127.495 | 14.677 | 0.527 | 97.143 |
| gnn_geo | post_covid | 19.631 | 146.481 | 15.865 | 0.538 | 91.429 |
| gnn_multiedge_season_level | post_covid | 19.655 | 124.375 | 14.854 | 0.524 | 97.143 |
| gnn_multiedge_season | post_covid | 19.928 | 144.753 | 16.176 | 0.521 | 91.429 |
| gnn_multiedge_leaknorm | post_covid | 20.475 | 152.245 | 16.647 | 0.507 | 91.429 |
| gnn_multiedge_covid_rsv | post_covid | 20.715 | 159.223 | 17.438 | 0.518 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 20.853 | 150.650 | 16.937 | 0.427 | 94.286 |
| gnn_multiedge | post_covid | 20.911 | 152.234 | 16.803 | 0.499 | 94.286 |
| gnn_corrbinary | post_covid | 21.063 | 162.775 | 17.512 | 0.509 | 94.286 |
| gnn_multiedge_rt | post_covid | 21.397 | 154.933 | 17.570 | 0.447 | 91.429 |
| lstm | post_covid | 21.564 | 156.105 | 17.554 | 0.408 | 91.429 |
| dualtopo_fullhistory | full | 21.663 | 78.417 | 11.750 | 0.215 | 88.571 |
| arima | post_covid | 21.945 | 112.697 | 13.732 |  | 100.000 |
| arima | exclude_covid | 22.086 | 140.889 | 15.456 |  | 100.000 |
| gnn_uniform | post_covid | 22.165 | 173.254 | 18.474 | 0.514 | 94.286 |
| dualtopo_no_bg | post_covid | 22.288 | 154.630 | 16.467 | 0.311 | 88.571 |
| dualtopo | post_covid | 22.295 | 154.815 | 16.481 | 0.327 | 88.571 |
| gnn_multiedge_full | full | 22.697 | 180.916 | 18.949 | 0.442 | 94.286 |
| lstm | exclude_covid | 23.046 | 168.431 | 18.794 | 0.444 | 100.000 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| persistence | exclude_covid | 31.334 | 141.784 | 19.720 | -0.166 | 100.000 |
| persistence | post_covid | 31.334 | 141.784 | 19.720 | -0.166 | 100.000 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 22.764 | 161.312 | 19.379 | 0.592 | 95.238 |
| gnn_multiedge_season | post_covid | 23.726 | 163.698 | 20.356 | 0.535 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 24.040 | 168.921 | 20.526 | 0.515 | 95.238 |
| gnn_multiedge | post_covid | 24.519 | 170.021 | 20.502 | 0.492 | 100.000 |
| gnn_multiedge_season_level | post_covid | 24.837 | 170.813 | 21.501 | 0.464 | 95.238 |
| gnn_multiedge_level | post_covid | 24.873 | 176.704 | 21.507 | 0.465 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 25.033 | 178.145 | 21.736 | 0.451 | 100.000 |
| gnn_corrbinary | post_covid | 25.130 | 194.193 | 22.231 | 0.500 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 25.180 | 195.420 | 22.849 | 0.541 | 95.238 |
| gnn_multiedge_rt | post_covid | 25.317 | 170.252 | 22.065 | 0.420 | 100.000 |
| gnn_uniform | post_covid | 25.891 | 197.512 | 22.798 | 0.521 | 100.000 |
| lstm | post_covid | 26.281 | 182.798 | 23.243 | 0.308 | 85.714 |
| dualtopo | post_covid | 26.529 | 139.064 | 19.063 | 0.554 | 80.952 |
| dualtopo_no_bg | post_covid | 26.529 | 138.994 | 19.058 | 0.389 | 80.952 |
| arima | exclude_covid | 26.662 | 127.235 | 18.309 |  | 100.000 |
| gnn_multiedge_full | full | 27.073 | 216.087 | 24.408 | 0.396 | 100.000 |
| arima | post_covid | 27.225 | 103.792 | 17.189 |  | 100.000 |
| dualtopo_fullhistory | full | 27.653 | 90.862 | 16.624 | 0.009 | 80.952 |
| lstm | exclude_covid | 27.938 | 208.944 | 25.320 | 0.349 | 100.000 |
| persistence | exclude_covid | 30.573 | 54.757 | 17.910 | 0.184 | 100.000 |
| persistence | post_covid | 30.573 | 54.757 | 17.910 | 0.184 | 100.000 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 5.094 | 53.680 | 4.431 | 0.497 | 100.000 |
| dualtopo_fullhistory | full | 5.114 | 59.749 | 4.439 | 0.525 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.365 | 54.718 | 4.882 | 0.568 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| arima | post_covid | 9.601 | 126.055 | 8.546 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.033 | 104.928 | 9.321 | 0.361 | 71.429 |
| lstm | post_covid | 11.244 | 116.064 | 9.021 | 0.496 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 12.131 | 109.406 | 9.738 | 0.403 | 85.714 |
| gnn_multiedge_season | post_covid | 12.184 | 116.336 | 9.906 | 0.270 | 78.571 |
| arima | exclude_covid | 12.373 | 161.371 | 11.178 |  | 100.000 |
| lstm | exclude_covid | 12.529 | 107.662 | 9.003 | 0.583 | 100.000 |
| gnn_corrbinary | post_covid | 12.722 | 115.649 | 10.433 | 0.209 | 85.714 |
| gnn_multiedge_leaknorm | post_covid | 13.460 | 127.231 | 10.829 | 0.185 | 85.714 |
| gnn_multiedge_rt | post_covid | 13.534 | 131.954 | 10.828 | 0.318 | 78.571 |
| gnn_geo | post_covid | 13.644 | 124.235 | 10.593 | 0.120 | 85.714 |
| dualtopo_no_bg | post_covid | 13.648 | 178.085 | 12.579 | 0.492 | 100.000 |
| dualtopo | post_covid | 13.677 | 178.441 | 12.607 | 0.465 | 100.000 |
| gnn_multiedge_full | full | 13.729 | 128.159 | 10.759 | 0.318 | 85.714 |
| gnn_multiedge | post_covid | 13.833 | 125.553 | 11.254 | 0.129 | 85.714 |
| gnn_uniform | post_covid | 14.925 | 136.866 | 11.988 | 0.133 | 85.714 |
| persistence | exclude_covid | 32.442 | 272.326 | 22.436 | -0.191 | 100.000 |
| persistence | post_covid | 32.442 | 272.326 | 22.436 | -0.191 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 21.571 | 188.464 | 16.763 | 0.707 | 87.234 |
| dualtopo_fullhistory | full | 22.293 | 101.739 | 12.619 | 0.229 | 91.489 |
| gnn_multiedge_covid_rsv_full | full | 22.606 | 227.951 | 17.591 | 0.472 | 95.745 |
| gnn_multiedge_full | full | 23.176 | 222.299 | 19.298 | 0.597 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 23.287 | 219.299 | 17.970 | 0.667 | 91.489 |
| gnn_multiedge_covid_rsv | post_covid | 23.550 | 189.245 | 18.926 | 0.681 | 80.851 |
| gnn_multiedge_season_level | post_covid | 24.370 | 154.534 | 18.677 | 0.718 | 100.000 |
| gnn_uniform | post_covid | 24.383 | 216.693 | 18.597 | 0.700 | 93.617 |
| gnn_multiedge | post_covid | 24.411 | 191.990 | 18.103 | 0.709 | 93.617 |
| gnn_geo | post_covid | 24.570 | 230.872 | 19.394 | 0.710 | 93.617 |
| arima | post_covid | 24.597 | 284.002 | 20.402 |  | 100.000 |
| arima | exclude_covid | 25.032 | 297.244 | 21.149 |  | 100.000 |
| gnn_multiedge_level | post_covid | 25.347 | 195.198 | 20.220 | 0.718 | 100.000 |
| gnn_multiedge_rt | post_covid | 26.496 | 244.102 | 20.921 | 0.570 | 87.234 |
| dualtopo_no_bg | post_covid | 28.015 | 369.897 | 25.300 | 0.348 | 93.617 |
| dualtopo | post_covid | 28.057 | 370.800 | 25.351 | 0.372 | 93.617 |
| lstm | exclude_covid | 29.650 | 247.788 | 24.678 | 0.582 | 100.000 |
| gnn_corrbinary | post_covid | 30.760 | 234.343 | 24.115 | 0.683 | 87.234 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| persistence | exclude_covid | 50.310 | 537.272 | 32.440 | -0.305 | 93.617 |
| persistence | post_covid | 50.310 | 537.272 | 32.440 | -0.305 | 95.745 |
| lstm | post_covid | 50.566 | 319.655 | 37.959 | 0.562 | 65.957 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 23.373 | 125.210 | 19.893 | 0.607 | 100.000 |
| gnn_multiedge_season | post_covid | 25.818 | 136.480 | 21.959 | 0.685 | 100.000 |
| gnn_multiedge_full | full | 25.837 | 145.475 | 23.127 | 0.589 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 26.135 | 133.734 | 22.022 | 0.662 | 100.000 |
| arima | post_covid | 26.722 | 137.439 | 19.666 |  | 100.000 |
| arima | exclude_covid | 26.750 | 144.303 | 20.157 |  | 100.000 |
| dualtopo_no_bg | post_covid | 27.644 | 182.405 | 22.966 | 0.116 | 88.462 |
| dualtopo | post_covid | 27.659 | 182.803 | 22.997 | 0.412 | 88.462 |
| gnn_geo | post_covid | 28.296 | 151.112 | 24.258 | 0.711 | 100.000 |
| gnn_uniform | post_covid | 28.350 | 137.022 | 23.642 | 0.683 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 29.134 | 170.623 | 26.089 | 0.655 | 100.000 |
| gnn_multiedge | post_covid | 29.287 | 138.204 | 24.029 | 0.675 | 100.000 |
| dualtopo_fullhistory | full | 29.358 | 70.169 | 17.953 | 0.031 | 84.615 |
| gnn_multiedge_rt | post_covid | 29.534 | 147.524 | 24.569 | 0.529 | 100.000 |
| gnn_multiedge_season_level | post_covid | 31.234 | 171.103 | 27.218 | 0.653 | 100.000 |
| gnn_multiedge_level | post_covid | 32.563 | 198.074 | 28.605 | 0.635 | 100.000 |
| lstm | exclude_covid | 34.002 | 202.930 | 30.272 | 0.490 | 100.000 |
| persistence | exclude_covid | 34.832 | 67.084 | 22.731 | -0.102 | 100.000 |
| persistence | post_covid | 34.832 | 67.084 | 22.731 | -0.102 | 100.000 |
| gnn_corrbinary | post_covid | 38.623 | 212.287 | 34.116 | 0.634 | 100.000 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| lstm | post_covid | 60.098 | 300.919 | 50.075 | 0.449 | 57.692 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 6.725 | 140.826 | 6.015 | 0.617 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gnn_multiedge_season_level | post_covid | 11.017 | 134.020 | 8.103 | 0.655 | 100.000 |
| gnn_multiedge_level | post_covid | 11.181 | 191.638 | 9.838 | 0.725 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.800 | 212.300 | 10.057 | 0.249 | 57.143 |
| gnn_multiedge_season | post_covid | 14.702 | 252.825 | 10.329 | 0.103 | 71.429 |
| gnn_corrbinary | post_covid | 16.452 | 261.650 | 11.732 | 0.187 | 71.429 |
| gnn_multiedge | post_covid | 16.486 | 258.583 | 10.766 | 0.115 | 85.714 |
| gnn_uniform | post_covid | 18.317 | 315.333 | 12.350 | 0.013 | 85.714 |
| gnn_geo | post_covid | 18.968 | 329.623 | 13.373 | 0.004 | 85.714 |
| gnn_multiedge_leaknorm | post_covid | 19.185 | 325.237 | 12.953 | 0.016 | 80.952 |
| gnn_multiedge_full | full | 19.381 | 317.414 | 14.557 | 0.185 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 21.618 | 355.154 | 14.740 | -0.015 | 90.476 |
| arima | post_covid | 21.680 | 465.461 | 21.314 |  | 100.000 |
| gnn_multiedge_rt | post_covid | 22.165 | 363.676 | 16.404 | 0.146 | 71.429 |
| arima | exclude_covid | 22.727 | 486.600 | 22.377 |  | 100.000 |
| lstm | exclude_covid | 23.157 | 303.325 | 17.751 | 0.591 | 100.000 |
| dualtopo_no_bg | post_covid | 28.467 | 602.030 | 28.191 | 0.316 | 100.000 |
| dualtopo | post_covid | 28.542 | 603.559 | 28.265 | 0.295 | 100.000 |
| lstm | post_covid | 35.369 | 342.853 | 22.958 | 0.563 | 76.190 |
| persistence | exclude_covid | 64.519 | 1119.410 | 44.462 | -0.367 | 85.714 |
| persistence | post_covid | 64.519 | 1119.410 | 44.462 | -0.367 | 90.476 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 19.957 | 205.431 | 15.685 | 0.436 | 100.000 |
| gnn_multiedge_season | post_covid | 20.227 | 182.059 | 15.910 | 0.603 | 93.478 |
| gnn_multiedge_leaknorm | post_covid | 20.667 | 211.558 | 16.635 | 0.607 | 100.000 |
| arima | post_covid | 20.898 | 244.667 | 15.593 |  | 100.000 |
| gnn_multiedge_season_level | post_covid | 20.906 | 141.091 | 15.638 | 0.623 | 93.478 |
| gnn_geo | post_covid | 20.917 | 212.156 | 16.842 | 0.643 | 100.000 |
| gnn_multiedge_level | post_covid | 21.246 | 177.319 | 16.356 | 0.634 | 100.000 |
| gnn_multiedge_full | full | 21.375 | 218.256 | 17.603 | 0.511 | 100.000 |
| arima | exclude_covid | 21.562 | 276.014 | 17.063 |  | 100.000 |
| dualtopo_fullhistory | full | 21.573 | 95.191 | 12.213 | 0.068 | 86.957 |
| gnn_multiedge_covid_rsv | post_covid | 21.806 | 193.574 | 17.424 | 0.579 | 89.130 |
| gnn_uniform | post_covid | 22.078 | 220.846 | 17.564 | 0.603 | 97.826 |
| gnn_multiedge | post_covid | 22.215 | 200.117 | 17.141 | 0.621 | 95.652 |
| dualtopo_no_bg | post_covid | 22.934 | 323.637 | 19.413 | 0.394 | 91.304 |
| dualtopo | post_covid | 22.964 | 324.568 | 19.458 | 0.395 | 91.304 |
| gnn_multiedge_rt | post_covid | 23.642 | 213.821 | 18.235 | 0.493 | 100.000 |
| lstm | exclude_covid | 25.790 | 231.644 | 21.152 | 0.533 | 100.000 |
| gnn_corrbinary | post_covid | 28.061 | 219.823 | 20.967 | 0.623 | 93.478 |
| lstm | post_covid | 32.672 | 265.599 | 25.618 | 0.466 | 86.957 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| persistence | exclude_covid | 39.356 | 548.076 | 26.507 | -0.398 | 100.000 |
| persistence | post_covid | 39.356 | 548.076 | 26.507 | -0.398 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 24.054 | 155.108 | 20.475 | 0.310 | 100.000 |
| arima | exclude_covid | 24.249 | 120.210 | 16.914 |  | 100.000 |
| dualtopo_no_bg | post_covid | 24.370 | 143.145 | 18.418 | 0.347 | 84.000 |
| dualtopo | post_covid | 24.376 | 143.516 | 18.448 | 0.324 | 84.000 |
| arima | post_covid | 24.428 | 105.816 | 16.087 |  | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 25.632 | 165.277 | 22.575 | 0.528 | 100.000 |
| gnn_multiedge_full | full | 25.835 | 163.237 | 23.233 | 0.394 | 100.000 |
| gnn_multiedge_season | post_covid | 26.044 | 175.858 | 22.935 | 0.496 | 100.000 |
| gnn_geo | post_covid | 26.378 | 181.517 | 23.285 | 0.581 | 100.000 |
| gnn_multiedge_season_level | post_covid | 27.518 | 180.265 | 23.801 | 0.501 | 100.000 |
| gnn_uniform | post_covid | 27.532 | 173.728 | 23.855 | 0.523 | 100.000 |
| gnn_multiedge_level | post_covid | 27.916 | 190.802 | 24.432 | 0.518 | 100.000 |
| gnn_multiedge | post_covid | 28.075 | 168.401 | 23.560 | 0.539 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 28.130 | 216.807 | 25.537 | 0.484 | 100.000 |
| dualtopo_fullhistory | full | 28.432 | 65.388 | 17.105 | -0.113 | 76.000 |
| gnn_multiedge_rt | post_covid | 29.213 | 179.210 | 24.669 | 0.339 | 100.000 |
| lstm | exclude_covid | 30.984 | 206.754 | 27.314 | 0.381 | 100.000 |
| persistence | exclude_covid | 31.930 | 67.150 | 19.768 | -0.308 | 100.000 |
| persistence | post_covid | 31.930 | 67.150 | 19.768 | -0.308 | 100.000 |
| gnn_corrbinary | post_covid | 36.751 | 260.799 | 31.731 | 0.550 | 100.000 |
| lstm | post_covid | 39.906 | 272.355 | 34.244 | 0.253 | 76.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| gnn_multiedge_season_level | post_covid | 7.475 | 94.455 | 5.920 | 0.597 | 85.714 |
| dualtopo_fullhistory | full | 7.558 | 130.670 | 6.390 | 0.642 | 100.000 |
| gnn_multiedge_level | post_covid | 7.813 | 161.267 | 6.741 | 0.444 | 100.000 |
| gnn_multiedge_season | post_covid | 9.417 | 189.442 | 7.547 | 0.188 | 85.714 |
| gnn_multiedge_covid_rsv | post_covid | 9.976 | 165.917 | 7.766 | 0.271 | 76.190 |
| gnn_corrbinary | post_covid | 10.814 | 171.041 | 8.153 | 0.153 | 85.714 |
| gnn_geo | post_covid | 11.404 | 248.631 | 9.173 | -0.119 | 100.000 |
| gnn_multiedge | post_covid | 11.946 | 237.875 | 9.500 | -0.107 | 90.476 |
| gnn_multiedge_leaknorm | post_covid | 12.391 | 266.654 | 9.562 | -0.127 | 100.000 |
| gnn_uniform | post_covid | 12.859 | 276.939 | 10.075 | -0.178 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 13.550 | 265.340 | 9.983 | 0.050 | 100.000 |
| gnn_multiedge_full | full | 14.360 | 283.754 | 10.900 | 0.156 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.436 | 255.025 | 10.574 | 0.196 | 100.000 |
| arima | post_covid | 15.693 | 409.965 | 15.005 |  | 100.000 |
| lstm | exclude_covid | 17.723 | 261.275 | 13.817 | 0.647 | 100.000 |
| arima | exclude_covid | 17.842 | 461.495 | 17.240 |  | 100.000 |
| lstm | post_covid | 21.033 | 257.557 | 15.350 | 0.661 | 100.000 |
| dualtopo_no_bg | post_covid | 21.097 | 538.508 | 20.597 | 0.789 | 100.000 |
| dualtopo | post_covid | 21.161 | 540.106 | 20.661 | 0.772 | 100.000 |
| persistence | exclude_covid | 46.681 | 1120.607 | 34.529 | -0.704 | 100.000 |
| persistence | post_covid | 46.681 | 1120.607 | 34.529 | -0.704 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 13.930 | 98.488 | 10.004 | 0.700 | 100.000 |
| gnn_multiedge_season | post_covid | 14.205 | 128.144 | 10.059 | 0.668 | 91.837 |
| gnn_multiedge_level | post_covid | 14.263 | 113.724 | 10.254 | 0.703 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.617 | 129.133 | 10.803 | 0.658 | 87.755 |
| gnn_multiedge_leaknorm | post_covid | 14.717 | 143.581 | 10.882 | 0.667 | 95.918 |
| gnn_uniform | post_covid | 14.856 | 146.668 | 11.067 | 0.664 | 95.918 |
| gnn_multiedge | post_covid | 14.911 | 136.671 | 10.997 | 0.681 | 95.918 |
| lstm | exclude_covid | 15.094 | 116.122 | 10.717 | 0.593 | 97.959 |
| gnn_multiedge_full | full | 15.934 | 163.461 | 12.031 | 0.543 | 97.959 |
| gnn_geo | post_covid | 15.942 | 180.346 | 12.661 | 0.682 | 95.918 |
| gnn_multiedge_rt | post_covid | 16.565 | 155.653 | 12.155 | 0.566 | 93.878 |
| gnn_multiedge_covid_rsv_full | full | 16.685 | 167.316 | 11.484 | 0.416 | 97.959 |
| arima | exclude_covid | 18.178 | 176.127 | 12.244 |  | 100.000 |
| arima | post_covid | 18.225 | 184.974 | 12.598 |  | 100.000 |
| dualtopo_fullhistory | full | 18.822 | 66.375 | 9.538 | 0.253 | 87.755 |
| dualtopo_no_bg | post_covid | 18.917 | 237.484 | 14.907 | 0.415 | 91.837 |
| dualtopo | post_covid | 18.946 | 238.929 | 14.974 | 0.415 | 91.837 |
| gnn_corrbinary | post_covid | 19.033 | 167.847 | 14.408 | 0.667 | 91.837 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| lstm | post_covid | 23.160 | 179.431 | 17.104 | 0.534 | 97.959 |
| persistence | exclude_covid | 32.624 | 437.969 | 22.994 | -0.392 | 100.000 |
| persistence | post_covid | 32.624 | 437.969 | 22.994 | -0.392 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 18.162 | 90.676 | 14.344 | 0.572 | 100.000 |
| gnn_uniform | post_covid | 18.213 | 90.985 | 14.699 | 0.589 | 100.000 |
| gnn_multiedge_season_level | post_covid | 18.440 | 95.931 | 14.943 | 0.593 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 18.481 | 94.307 | 15.078 | 0.575 | 100.000 |
| gnn_multiedge_level | post_covid | 18.962 | 101.383 | 15.528 | 0.582 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 18.973 | 107.649 | 15.830 | 0.564 | 100.000 |
| gnn_multiedge | post_covid | 19.033 | 94.094 | 15.345 | 0.580 | 100.000 |
| lstm | exclude_covid | 19.141 | 81.893 | 14.502 | 0.461 | 96.154 |
| gnn_multiedge_full | full | 19.293 | 84.095 | 14.853 | 0.441 | 100.000 |
| gnn_geo | post_covid | 19.572 | 121.169 | 16.899 | 0.619 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 20.191 | 78.656 | 14.083 | 0.369 | 100.000 |
| gnn_multiedge_rt | post_covid | 20.518 | 99.235 | 16.387 | 0.430 | 100.000 |
| dualtopo | post_covid | 21.581 | 90.327 | 15.039 | 0.245 | 84.615 |
| dualtopo_no_bg | post_covid | 21.595 | 89.729 | 15.001 | 0.319 | 84.615 |
| arima | post_covid | 22.421 | 68.943 | 13.929 |  | 100.000 |
| arima | exclude_covid | 22.623 | 65.746 | 13.814 |  | 100.000 |
| gnn_corrbinary | post_covid | 25.066 | 168.106 | 21.965 | 0.552 | 100.000 |
| dualtopo_fullhistory | full | 25.616 | 48.523 | 15.348 | 0.084 | 76.923 |
| lstm | post_covid | 28.100 | 159.513 | 23.304 | 0.356 | 96.154 |
| persistence | exclude_covid | 29.159 | 71.479 | 19.481 | -0.366 | 100.000 |
| persistence | post_covid | 29.159 | 71.479 | 19.481 | -0.366 | 100.000 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.602 | 86.556 | 2.970 | 0.625 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| gnn_multiedge_level | post_covid | 5.195 | 127.675 | 4.293 | 0.632 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.388 | 101.378 | 4.420 | 0.576 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.946 | 153.418 | 5.120 | 0.467 | 73.913 |
| gnn_multiedge_season | post_covid | 7.549 | 170.500 | 5.216 | 0.338 | 82.609 |
| gnn_corrbinary | post_covid | 7.841 | 167.555 | 5.867 | 0.482 | 82.609 |
| gnn_multiedge | post_covid | 8.013 | 184.801 | 6.081 | 0.303 | 91.304 |
| lstm | exclude_covid | 8.439 | 154.815 | 6.437 | 0.651 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 8.681 | 199.282 | 6.139 | 0.242 | 91.304 |
| gnn_uniform | post_covid | 9.759 | 209.615 | 6.962 | 0.168 | 91.304 |
| gnn_geo | post_covid | 10.412 | 247.241 | 7.871 | 0.131 | 91.304 |
| gnn_multiedge_rt | post_covid | 10.426 | 219.430 | 7.371 | 0.338 | 86.957 |
| gnn_multiedge_full | full | 10.959 | 253.178 | 8.841 | 0.298 | 95.652 |
| arima | exclude_covid | 11.201 | 300.906 | 10.468 |  | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 11.500 | 267.540 | 8.547 | 0.130 | 95.652 |
| arima | post_covid | 11.803 | 316.139 | 11.092 |  | 100.000 |
| dualtopo_no_bg | post_covid | 15.338 | 404.511 | 14.802 | 0.643 | 100.000 |
| dualtopo | post_covid | 15.435 | 406.914 | 14.902 | 0.633 | 100.000 |
| lstm | post_covid | 15.815 | 201.948 | 10.096 | 0.585 | 100.000 |
| persistence | exclude_covid | 36.144 | 852.262 | 26.965 | -0.458 | 100.000 |
| persistence | post_covid | 36.144 | 852.262 | 26.965 | -0.458 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 15.119 | 108.501 | 11.057 | 0.662 | 97.500 |
| gnn_multiedge_season | post_covid | 15.347 | 105.602 | 11.057 | 0.629 | 92.500 |
| gnn_multiedge | post_covid | 15.360 | 100.561 | 10.924 | 0.636 | 97.500 |
| gnn_multiedge_leaknorm | post_covid | 15.476 | 106.933 | 11.192 | 0.628 | 95.000 |
| gnn_multiedge_level | post_covid | 16.120 | 100.899 | 10.942 | 0.572 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.256 | 102.909 | 11.396 | 0.559 | 97.500 |
| gnn_uniform | post_covid | 16.375 | 112.522 | 12.030 | 0.626 | 97.500 |
| gnn_multiedge_covid_rsv_full | full | 16.382 | 105.679 | 11.014 | 0.551 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 16.395 | 125.693 | 12.647 | 0.591 | 90.000 |
| gnn_multiedge_rt | post_covid | 16.474 | 108.092 | 11.754 | 0.553 | 95.000 |
| gnn_multiedge_full | full | 16.973 | 131.485 | 12.604 | 0.563 | 100.000 |
| gnn_corrbinary | post_covid | 17.163 | 128.189 | 13.245 | 0.603 | 95.000 |
| lstm | exclude_covid | 18.571 | 136.607 | 13.826 | 0.449 | 97.500 |
| arima | exclude_covid | 19.282 | 120.909 | 11.364 |  | 95.000 |
| arima | post_covid | 19.354 | 102.170 | 10.497 |  | 97.500 |
| dualtopo_no_bg | post_covid | 19.397 | 144.650 | 12.604 | 0.292 | 92.500 |
| dualtopo | post_covid | 19.404 | 145.379 | 12.642 | 0.313 | 92.500 |
| dualtopo_fullhistory | full | 20.045 | 55.139 | 9.319 | 0.100 | 90.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| lstm | post_covid | 24.198 | 179.999 | 18.349 | 0.421 | 97.500 |
| persistence | exclude_covid | 25.245 | 150.178 | 14.935 | -0.185 | 100.000 |
| persistence | post_covid | 25.245 | 150.178 | 14.935 | -0.185 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 18.159 | 124.242 | 14.472 | 0.677 | 100.000 |
| gnn_multiedge | post_covid | 18.272 | 108.951 | 14.045 | 0.631 | 100.000 |
| gnn_multiedge_season | post_covid | 18.574 | 112.730 | 14.338 | 0.634 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 18.615 | 116.690 | 14.527 | 0.626 | 100.000 |
| gnn_uniform | post_covid | 19.668 | 130.425 | 15.995 | 0.612 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 19.746 | 139.879 | 16.560 | 0.615 | 100.000 |
| gnn_multiedge_rt | post_covid | 19.762 | 109.435 | 15.053 | 0.527 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 19.767 | 112.069 | 14.259 | 0.607 | 100.000 |
| gnn_multiedge_season_level | post_covid | 19.949 | 115.455 | 15.112 | 0.516 | 100.000 |
| gnn_multiedge_level | post_covid | 20.042 | 121.296 | 15.272 | 0.518 | 100.000 |
| gnn_multiedge_full | full | 20.053 | 131.129 | 15.890 | 0.558 | 100.000 |
| gnn_corrbinary | post_covid | 20.676 | 154.261 | 17.728 | 0.608 | 100.000 |
| lstm | exclude_covid | 21.927 | 138.133 | 17.416 | 0.392 | 96.000 |
| dualtopo | post_covid | 22.966 | 100.445 | 13.913 | 0.561 | 88.000 |
| dualtopo_no_bg | post_covid | 22.974 | 99.973 | 13.891 | 0.273 | 88.000 |
| arima | exclude_covid | 23.324 | 84.143 | 13.144 |  | 92.000 |
| arima | post_covid | 23.751 | 72.420 | 12.740 |  | 96.000 |
| dualtopo_fullhistory | full | 25.205 | 52.712 | 12.912 | -0.099 | 84.000 |
| persistence | exclude_covid | 26.801 | 57.477 | 14.952 | 0.067 | 100.000 |
| persistence | post_covid | 26.801 | 57.477 | 14.952 | 0.067 | 100.000 |
| lstm | post_covid | 28.137 | 191.299 | 23.244 | 0.339 | 96.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.565 | 59.185 | 3.331 | 0.351 | 100.000 |
| gnn_multiedge_level | post_covid | 4.848 | 66.903 | 3.726 | 0.245 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.436 | 81.998 | 5.203 | 0.193 | 93.333 |
| gnn_multiedge_season | post_covid | 7.283 | 93.724 | 5.588 | 0.337 | 80.000 |
| arima | post_covid | 7.660 | 151.755 | 6.757 |  | 100.000 |
| gnn_geo | post_covid | 7.748 | 82.265 | 5.364 | 0.313 | 93.333 |
| gnn_multiedge_leaknorm | post_covid | 7.820 | 90.673 | 5.632 | 0.336 | 86.667 |
| gnn_multiedge_covid_rsv_full | full | 8.029 | 95.030 | 5.606 | 0.448 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.182 | 102.051 | 6.125 | 0.364 | 73.333 |
| gnn_uniform | post_covid | 8.382 | 82.684 | 5.422 | 0.237 | 93.333 |
| gnn_multiedge | post_covid | 8.526 | 86.577 | 5.722 | 0.318 | 93.333 |
| gnn_multiedge_rt | post_covid | 8.535 | 105.854 | 6.256 | 0.369 | 86.667 |
| gnn_corrbinary | post_covid | 8.548 | 84.735 | 5.774 | 0.315 | 86.667 |
| arima | exclude_covid | 9.208 | 182.186 | 8.398 |  | 100.000 |
| gnn_multiedge_full | full | 9.898 | 132.079 | 7.127 | 0.347 | 100.000 |
| lstm | exclude_covid | 10.879 | 134.064 | 7.843 | 0.285 | 100.000 |
| dualtopo_no_bg | post_covid | 11.120 | 219.112 | 10.460 | 0.420 | 100.000 |
| dualtopo | post_covid | 11.180 | 220.269 | 10.524 | 0.426 | 100.000 |
| lstm | post_covid | 15.557 | 161.166 | 10.190 | 0.307 | 100.000 |
| persistence | exclude_covid | 22.413 | 304.680 | 14.907 | -0.167 | 100.000 |
| persistence | post_covid | 22.413 | 304.680 | 14.907 | -0.167 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 10.562 | 121.862 | 8.089 | 0.716 | 100.000 |
| gnn_multiedge_season_level | post_covid | 10.598 | 120.424 | 8.285 | 0.695 | 95.238 |
| gnn_multiedge_season | post_covid | 11.867 | 140.021 | 8.995 | 0.623 | 95.238 |
| gnn_multiedge_covid_rsv | post_covid | 11.908 | 155.722 | 9.688 | 0.632 | 92.857 |
| gnn_multiedge_covid_rsv_full | full | 12.083 | 157.381 | 8.997 | 0.501 | 97.619 |
| gnn_multiedge_full | full | 12.336 | 168.864 | 10.157 | 0.604 | 97.619 |
| gnn_geo | post_covid | 12.819 | 176.399 | 10.081 | 0.611 | 97.619 |
| gnn_multiedge_leaknorm | post_covid | 12.901 | 157.378 | 10.289 | 0.646 | 95.238 |
| gnn_multiedge | post_covid | 13.077 | 152.154 | 10.323 | 0.635 | 92.857 |
| gnn_uniform | post_covid | 13.113 | 155.380 | 9.982 | 0.601 | 95.238 |
| arima | post_covid | 13.184 | 169.240 | 9.092 |  | 100.000 |
| dualtopo_fullhistory | full | 13.668 | 68.678 | 7.284 | 0.178 | 88.095 |
| dualtopo_no_bg | post_covid | 13.711 | 236.799 | 10.883 | 0.365 | 90.476 |
| dualtopo | post_covid | 13.723 | 237.478 | 10.904 | 0.374 | 90.476 |
| gnn_multiedge_rt | post_covid | 13.825 | 155.544 | 10.467 | 0.532 | 92.857 |
| lstm | exclude_covid | 14.701 | 186.990 | 12.138 | 0.596 | 100.000 |
| lstm | post_covid | 14.881 | 164.385 | 11.580 | 0.551 | 100.000 |
| gnn_corrbinary | post_covid | 16.200 | 214.650 | 13.308 | 0.642 | 92.857 |
| arima | exclude_covid | 21.447 | 286.776 | 14.215 | -0.256 | 90.476 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |
| persistence | exclude_covid | 24.985 | 291.993 | 16.205 | -0.271 | 100.000 |
| persistence | post_covid | 24.985 | 291.993 | 16.205 | -0.271 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 13.029 | 135.264 | 11.231 | 0.638 | 100.000 |
| gnn_multiedge_season | post_covid | 13.119 | 138.916 | 11.026 | 0.623 | 100.000 |
| gnn_geo | post_covid | 13.143 | 149.959 | 11.237 | 0.663 | 100.000 |
| gnn_multiedge_level | post_covid | 13.194 | 142.946 | 11.481 | 0.653 | 100.000 |
| gnn_uniform | post_covid | 13.373 | 128.649 | 11.268 | 0.642 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 13.617 | 161.337 | 11.098 | 0.501 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.995 | 167.544 | 12.329 | 0.602 | 100.000 |
| gnn_multiedge | post_covid | 14.140 | 128.703 | 12.065 | 0.639 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.581 | 130.252 | 12.269 | 0.524 | 100.000 |
| gnn_multiedge_full | full | 14.591 | 176.175 | 12.933 | 0.535 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 14.645 | 151.469 | 12.734 | 0.624 | 100.000 |
| dualtopo | post_covid | 15.117 | 169.761 | 10.843 | 0.353 | 84.000 |
| dualtopo_no_bg | post_covid | 15.119 | 169.373 | 10.834 | 0.317 | 84.000 |
| arima | post_covid | 15.848 | 125.984 | 10.327 |  | 100.000 |
| lstm | exclude_covid | 16.649 | 187.003 | 15.148 | 0.535 | 100.000 |
| lstm | post_covid | 17.000 | 163.834 | 14.643 | 0.457 | 100.000 |
| dualtopo_fullhistory | full | 17.386 | 57.084 | 10.124 | 0.059 | 80.000 |
| arima | exclude_covid | 18.592 | 142.148 | 12.799 | -0.352 | 88.000 |
| gnn_corrbinary | post_covid | 19.076 | 234.839 | 17.379 | 0.618 | 100.000 |
| persistence | exclude_covid | 20.038 | 79.936 | 13.616 | -0.236 | 100.000 |
| persistence | post_covid | 20.038 | 79.936 | 13.616 | -0.236 | 100.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| dualtopo_fullhistory | full | 4.125 | 85.729 | 3.107 | 0.380 | 100.000 |
| gnn_multiedge_level | post_covid | 4.428 | 90.856 | 3.099 | 0.254 | 100.000 |
| gnn_multiedge_season_level | post_covid | 5.280 | 98.601 | 3.953 | 0.143 | 88.235 |
| arima | post_covid | 7.753 | 232.852 | 7.275 |  | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.894 | 138.338 | 5.804 | 0.042 | 82.353 |
| gnn_multiedge_full | full | 7.931 | 158.111 | 6.074 | 0.043 | 94.118 |
| gnn_multiedge_covid_rsv_full | full | 9.382 | 151.565 | 5.908 | 0.050 | 94.118 |
| gnn_multiedge_season | post_covid | 9.738 | 141.645 | 6.008 | -0.043 | 88.235 |
| gnn_multiedge_leaknorm | post_covid | 9.786 | 166.067 | 6.695 | -0.066 | 88.235 |
| gnn_corrbinary | post_covid | 10.639 | 184.961 | 7.321 | -0.021 | 82.353 |
| lstm | post_covid | 11.049 | 165.195 | 7.076 | 0.397 | 100.000 |
| lstm | exclude_covid | 11.241 | 186.970 | 7.712 | 0.374 | 100.000 |
| dualtopo_no_bg | post_covid | 11.327 | 335.954 | 10.955 | 0.423 | 100.000 |
| gnn_multiedge | post_covid | 11.336 | 186.642 | 7.762 | -0.139 | 82.353 |
| dualtopo | post_covid | 11.365 | 337.060 | 10.994 | 0.427 | 100.000 |
| gnn_geo | post_covid | 12.328 | 215.281 | 8.382 | -0.178 | 94.118 |
| gnn_multiedge_rt | post_covid | 12.633 | 192.738 | 7.816 | 0.025 | 82.353 |
| gnn_uniform | post_covid | 12.721 | 194.689 | 8.092 | -0.136 | 88.235 |
| arima | exclude_covid | 25.061 | 499.464 | 16.298 | -0.132 | 94.118 |
| persistence | exclude_covid | 30.850 | 603.841 | 20.012 | -0.291 | 100.000 |
| persistence | post_covid | 30.850 | 603.841 | 20.012 | -0.291 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 8.975 | 78.777 | 5.889 | 0.729 | 95.652 |
| gnn_multiedge_level | post_covid | 9.102 | 95.361 | 6.231 | 0.731 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.848 | 139.043 | 7.179 | 0.688 | 91.304 |
| gnn_multiedge_season | post_covid | 10.011 | 147.156 | 6.903 | 0.660 | 89.130 |
| gnn_multiedge_leaknorm | post_covid | 10.591 | 156.787 | 7.486 | 0.651 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 10.659 | 153.887 | 7.363 | 0.552 | 93.478 |
| gnn_multiedge | post_covid | 10.730 | 162.302 | 7.963 | 0.663 | 89.130 |
| gnn_multiedge_full | full | 11.023 | 174.977 | 8.436 | 0.612 | 97.826 |
| gnn_uniform | post_covid | 11.107 | 171.920 | 8.097 | 0.641 | 91.304 |
| gnn_geo | post_covid | 11.346 | 166.362 | 8.553 | 0.690 | 95.652 |
| gnn_multiedge_rt | post_covid | 11.589 | 170.198 | 8.391 | 0.544 | 93.478 |
| arima | post_covid | 12.451 | 180.440 | 8.310 |  | 100.000 |
| gnn_corrbinary | post_covid | 12.697 | 176.389 | 10.119 | 0.690 | 93.478 |
| dualtopo_no_bg | post_covid | 12.745 | 240.024 | 9.474 | 0.482 | 95.652 |
| dualtopo_fullhistory | full | 12.752 | 77.360 | 7.333 | 0.439 | 91.304 |
| dualtopo | post_covid | 12.760 | 241.245 | 9.499 | 0.491 | 95.652 |
| lstm | exclude_covid | 13.510 | 164.986 | 10.689 | 0.637 | 100.000 |
| lstm | post_covid | 14.838 | 147.772 | 11.132 | 0.598 | 100.000 |
| arima | exclude_covid | 16.023 | 148.214 | 11.000 | -0.276 | 78.261 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| persistence | exclude_covid | 24.769 | 459.589 | 17.565 | -0.397 | 100.000 |
| persistence | post_covid | 24.769 | 459.589 | 17.565 | -0.397 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 10.985 | 71.594 | 7.635 | 0.637 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.103 | 73.871 | 8.245 | 0.647 | 100.000 |
| gnn_multiedge | post_covid | 11.214 | 70.759 | 8.646 | 0.658 | 100.000 |
| gnn_uniform | post_covid | 11.226 | 73.520 | 8.636 | 0.657 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.396 | 85.428 | 8.749 | 0.654 | 100.000 |
| gnn_multiedge_season_level | post_covid | 11.428 | 68.503 | 8.147 | 0.619 | 100.000 |
| gnn_multiedge_level | post_covid | 11.651 | 77.540 | 8.704 | 0.615 | 100.000 |
| gnn_multiedge_full | full | 11.856 | 96.052 | 9.395 | 0.597 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 12.074 | 78.370 | 8.184 | 0.572 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.388 | 78.923 | 9.115 | 0.497 | 100.000 |
| gnn_geo | post_covid | 12.485 | 96.560 | 10.408 | 0.659 | 100.000 |
| dualtopo | post_covid | 14.158 | 94.867 | 8.992 | 0.609 | 92.308 |
| dualtopo_no_bg | post_covid | 14.170 | 94.509 | 8.996 | 0.349 | 92.308 |
| gnn_corrbinary | post_covid | 14.631 | 118.613 | 13.146 | 0.646 | 100.000 |
| arima | post_covid | 15.132 | 76.742 | 9.363 |  | 100.000 |
| lstm | exclude_covid | 15.486 | 116.731 | 12.893 | 0.508 | 100.000 |
| dualtopo_fullhistory | full | 16.747 | 56.711 | 10.793 | 0.198 | 84.615 |
| lstm | post_covid | 16.857 | 112.036 | 13.685 | 0.466 | 100.000 |
| arima | exclude_covid | 20.242 | 88.007 | 14.885 | -0.274 | 80.769 |
| persistence | exclude_covid | 20.242 | 88.007 | 14.885 | -0.274 | 100.000 |
| persistence | post_covid | 20.242 | 88.007 | 14.885 | -0.274 | 100.000 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.071 | 104.204 | 2.836 | 0.482 | 100.000 |
| gnn_multiedge_level | post_covid | 3.755 | 118.529 | 3.016 | 0.481 | 100.000 |
| gnn_multiedge_season_level | post_covid | 3.935 | 92.133 | 2.954 | 0.558 | 90.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.364 | 208.741 | 5.139 | 0.310 | 80.000 |
| arima | exclude_covid | 7.605 | 226.483 | 5.951 | 0.187 | 75.000 |
| arima | post_covid | 7.676 | 315.248 | 6.942 |  | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 8.475 | 252.060 | 6.295 | 0.322 | 85.000 |
| gnn_multiedge_season | post_covid | 8.581 | 245.386 | 5.951 | 0.245 | 75.000 |
| gnn_corrbinary | post_covid | 9.618 | 251.497 | 6.184 | 0.222 | 85.000 |
| gnn_geo | post_covid | 9.667 | 257.104 | 6.142 | 0.107 | 90.000 |
| gnn_multiedge_full | full | 9.836 | 277.579 | 7.190 | 0.328 | 95.000 |
| gnn_multiedge_leaknorm | post_covid | 9.886 | 264.578 | 6.500 | 0.171 | 90.000 |
| gnn_multiedge | post_covid | 10.066 | 281.307 | 7.075 | 0.110 | 75.000 |
| lstm | exclude_covid | 10.392 | 227.717 | 7.825 | 0.674 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.460 | 288.854 | 7.451 | 0.259 | 85.000 |
| dualtopo_no_bg | post_covid | 10.610 | 429.195 | 10.095 | 0.750 | 100.000 |
| dualtopo | post_covid | 10.671 | 431.537 | 10.158 | 0.746 | 100.000 |
| gnn_uniform | post_covid | 10.951 | 299.840 | 7.395 | 0.097 | 80.000 |
| lstm | post_covid | 11.704 | 194.228 | 7.812 | 0.713 | 100.000 |
| persistence | exclude_covid | 29.637 | 942.646 | 21.050 | -0.420 | 100.000 |
| persistence | post_covid | 29.637 | 942.646 | 21.050 | -0.420 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 10.787 | 180.947 | 7.741 | 0.565 | 97.727 |
| gnn_multiedge_season_level | post_covid | 10.815 | 155.973 | 8.456 | 0.666 | 93.182 |
| gnn_multiedge_season | post_covid | 10.821 | 171.405 | 8.339 | 0.650 | 95.455 |
| gnn_multiedge_level | post_covid | 10.862 | 171.817 | 8.501 | 0.676 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.280 | 198.285 | 8.822 | 0.635 | 95.455 |
| gnn_multiedge | post_covid | 11.765 | 201.810 | 9.150 | 0.644 | 93.182 |
| gnn_multiedge_covid_rsv | post_covid | 11.798 | 199.198 | 9.288 | 0.610 | 86.364 |
| gnn_uniform | post_covid | 12.097 | 210.268 | 9.485 | 0.634 | 95.455 |
| gnn_multiedge_full | full | 12.361 | 224.785 | 9.448 | 0.485 | 97.727 |
| gnn_multiedge_covid_rsv_full | full | 12.425 | 209.182 | 8.870 | 0.378 | 97.727 |
| lstm | exclude_covid | 12.538 | 198.779 | 10.105 | 0.552 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.900 | 197.742 | 9.484 | 0.529 | 95.455 |
| arima | exclude_covid | 12.981 | 210.789 | 9.415 |  | 100.000 |
| dualtopo_fullhistory | full | 13.129 | 118.703 | 8.170 | 0.141 | 90.909 |
| arima | post_covid | 13.281 | 230.834 | 9.914 | -0.229 | 100.000 |
| dualtopo_no_bg | post_covid | 13.521 | 267.199 | 10.719 | 0.378 | 93.182 |
| dualtopo | post_covid | 13.540 | 268.444 | 10.753 | 0.375 | 93.182 |
| gnn_corrbinary | post_covid | 13.895 | 237.103 | 10.795 | 0.640 | 88.636 |
| lstm | post_covid | 17.058 | 243.975 | 13.576 | 0.523 | 100.000 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| persistence | exclude_covid | 23.700 | 358.180 | 15.584 | -0.316 | 100.000 |
| persistence | post_covid | 23.700 | 358.180 | 15.584 | -0.316 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_geo | post_covid | 11.431 | 108.899 | 8.330 | 0.690 | 100.000 |
| gnn_multiedge_season | post_covid | 12.737 | 162.285 | 10.665 | 0.605 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 12.948 | 176.083 | 10.861 | 0.600 | 100.000 |
| gnn_multiedge | post_covid | 13.642 | 185.688 | 11.518 | 0.599 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 13.747 | 153.909 | 10.211 | 0.412 | 100.000 |
| gnn_multiedge_full | full | 13.761 | 178.120 | 10.775 | 0.434 | 100.000 |
| gnn_multiedge_season_level | post_covid | 13.780 | 202.141 | 12.173 | 0.564 | 100.000 |
| gnn_uniform | post_covid | 13.833 | 192.708 | 11.795 | 0.598 | 100.000 |
| gnn_multiedge_level | post_covid | 13.905 | 211.394 | 12.306 | 0.572 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.253 | 217.215 | 12.118 | 0.538 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.337 | 174.118 | 11.554 | 0.468 | 100.000 |
| dualtopo | post_covid | 14.963 | 164.708 | 10.616 | 0.261 | 88.000 |
| dualtopo_no_bg | post_covid | 14.968 | 164.029 | 10.603 | 0.323 | 88.000 |
| lstm | exclude_covid | 14.972 | 220.537 | 12.984 | 0.401 | 100.000 |
| arima | post_covid | 15.397 | 139.456 | 10.450 | -0.098 | 100.000 |
| arima | exclude_covid | 15.465 | 132.831 | 10.338 |  | 100.000 |
| gnn_corrbinary | post_covid | 16.856 | 260.100 | 14.450 | 0.578 | 100.000 |
| dualtopo_fullhistory | full | 16.908 | 104.525 | 11.197 | -0.053 | 84.000 |
| persistence | exclude_covid | 20.289 | 62.617 | 13.528 | -0.164 | 100.000 |
| persistence | post_covid | 20.289 | 62.617 | 13.528 | -0.164 | 100.000 |
| lstm | post_covid | 20.373 | 287.246 | 17.810 | 0.339 | 100.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gnn_multiedge_level | post_covid | 4.337 | 119.741 | 3.494 | 0.379 | 100.000 |
| gnn_multiedge_season_level | post_covid | 4.584 | 95.227 | 3.566 | 0.482 | 84.211 |
| dualtopo_fullhistory | full | 4.794 | 137.359 | 4.187 | 0.675 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.418 | 175.491 | 5.565 | 0.305 | 68.421 |
| gnn_multiedge_season | post_covid | 7.597 | 183.406 | 5.277 | 0.257 | 89.474 |
| lstm | exclude_covid | 8.312 | 170.150 | 6.317 | 0.659 | 100.000 |
| gnn_corrbinary | post_covid | 8.560 | 206.844 | 5.987 | 0.147 | 73.684 |
| gnn_multiedge_leaknorm | post_covid | 8.606 | 227.498 | 6.140 | 0.134 | 89.474 |
| arima | exclude_covid | 8.692 | 313.366 | 8.201 |  | 100.000 |
| gnn_multiedge | post_covid | 8.699 | 223.023 | 6.033 | 0.043 | 89.474 |
| gnn_uniform | post_covid | 9.334 | 233.372 | 6.446 | 0.052 | 89.474 |
| arima | post_covid | 9.825 | 351.068 | 9.208 | -0.327 | 100.000 |
| gnn_geo | post_covid | 9.876 | 275.747 | 6.966 | -0.066 | 94.737 |
| gnn_multiedge_full | full | 10.230 | 286.186 | 7.702 | 0.206 | 94.737 |
| gnn_multiedge_covid_rsv_full | full | 10.433 | 281.910 | 7.107 | 0.077 | 94.737 |
| gnn_multiedge_rt | post_covid | 10.719 | 228.828 | 6.760 | 0.267 | 89.474 |
| lstm | post_covid | 11.300 | 187.040 | 8.004 | 0.673 | 100.000 |
| dualtopo_no_bg | post_covid | 11.340 | 402.949 | 10.873 | 0.521 | 100.000 |
| dualtopo | post_covid | 11.398 | 404.938 | 10.933 | 0.518 | 100.000 |
| persistence | exclude_covid | 27.551 | 747.078 | 18.289 | -0.337 | 100.000 |
| persistence | post_covid | 27.551 | 747.078 | 18.289 | -0.337 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 10.836 | 148.609 | 7.942 | 0.647 | 89.130 |
| gnn_multiedge_season_level | post_covid | 10.932 | 132.198 | 7.728 | 0.677 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 11.135 | 144.040 | 8.296 | 0.627 | 84.783 |
| gnn_multiedge_level | post_covid | 11.241 | 160.457 | 8.214 | 0.678 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.268 | 163.323 | 8.613 | 0.664 | 91.304 |
| gnn_multiedge | post_covid | 11.271 | 163.457 | 8.727 | 0.662 | 91.304 |
| gnn_geo | post_covid | 11.585 | 190.149 | 9.110 | 0.652 | 93.478 |
| gnn_uniform | post_covid | 11.632 | 174.596 | 8.823 | 0.617 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 11.673 | 144.713 | 8.200 | 0.535 | 93.478 |
| gnn_multiedge_full | full | 11.862 | 164.437 | 9.121 | 0.574 | 97.826 |
| gnn_multiedge_rt | post_covid | 12.481 | 165.123 | 9.278 | 0.537 | 91.304 |
| gnn_corrbinary | post_covid | 13.277 | 206.307 | 10.497 | 0.619 | 89.130 |
| lstm | exclude_covid | 13.514 | 188.420 | 10.674 | 0.559 | 100.000 |
| arima | post_covid | 13.831 | 216.698 | 9.652 |  | 100.000 |
| dualtopo_fullhistory | full | 13.874 | 93.707 | 7.447 | 0.175 | 89.130 |
| dualtopo_no_bg | post_covid | 14.342 | 276.823 | 11.234 | 0.384 | 93.478 |
| dualtopo | post_covid | 14.354 | 277.702 | 11.257 | 0.402 | 93.478 |
| lstm | post_covid | 15.385 | 203.330 | 11.732 | 0.498 | 100.000 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| arima | exclude_covid | 23.380 | 423.509 | 16.053 | -0.287 | 91.304 |
| persistence | exclude_covid | 23.980 | 413.921 | 16.320 | -0.328 | 100.000 |
| persistence | post_covid | 23.980 | 413.921 | 16.320 | -0.328 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_uniform | post_covid | 13.825 | 148.611 | 11.412 | 0.615 | 100.000 |
| gnn_multiedge_season | post_covid | 13.830 | 148.098 | 11.081 | 0.604 | 100.000 |
| gnn_multiedge | post_covid | 13.990 | 147.590 | 11.745 | 0.628 | 100.000 |
| gnn_geo | post_covid | 14.109 | 181.567 | 12.043 | 0.653 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 14.360 | 170.292 | 12.131 | 0.616 | 100.000 |
| gnn_multiedge_season_level | post_covid | 14.679 | 170.851 | 12.196 | 0.598 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.745 | 173.524 | 12.403 | 0.559 | 100.000 |
| gnn_multiedge_level | post_covid | 14.983 | 183.913 | 12.657 | 0.588 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 15.344 | 156.453 | 12.045 | 0.448 | 100.000 |
| gnn_multiedge_full | full | 15.430 | 172.877 | 13.316 | 0.456 | 100.000 |
| gnn_multiedge_rt | post_covid | 15.530 | 146.609 | 12.621 | 0.431 | 100.000 |
| dualtopo | post_covid | 16.792 | 165.025 | 11.684 | 0.551 | 87.500 |
| dualtopo_no_bg | post_covid | 16.796 | 164.580 | 11.675 | 0.239 | 87.500 |
| lstm | exclude_covid | 16.823 | 205.619 | 14.695 | 0.420 | 100.000 |
| gnn_corrbinary | post_covid | 16.966 | 239.969 | 15.248 | 0.581 | 100.000 |
| arima | post_covid | 17.345 | 131.240 | 11.107 |  | 100.000 |
| dualtopo_fullhistory | full | 18.963 | 83.587 | 11.814 | -0.075 | 79.167 |
| lstm | post_covid | 19.275 | 234.371 | 16.498 | 0.287 | 100.000 |
| arima | exclude_covid | 20.780 | 94.734 | 13.769 | -0.023 | 83.333 |
| persistence | exclude_covid | 22.056 | 86.723 | 14.508 | -0.317 | 100.000 |
| persistence | post_covid | 22.056 | 86.723 | 14.508 | -0.317 | 100.000 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.194 | 104.746 | 2.684 | 0.720 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gnn_multiedge_season_level | post_covid | 3.847 | 90.031 | 2.854 | 0.578 | 100.000 |
| gnn_multiedge_level | post_covid | 4.391 | 134.868 | 3.368 | 0.410 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.695 | 111.874 | 3.816 | 0.361 | 68.182 |
| gnn_multiedge_covid_rsv_full | full | 5.300 | 131.906 | 4.005 | 0.323 | 86.364 |
| gnn_multiedge_full | full | 5.873 | 155.230 | 4.544 | 0.433 | 95.455 |
| gnn_multiedge_season | post_covid | 6.069 | 149.166 | 4.517 | 0.182 | 77.273 |
| gnn_multiedge_leaknorm | post_covid | 6.368 | 155.721 | 4.774 | 0.160 | 81.818 |
| gnn_multiedge | post_covid | 7.219 | 180.767 | 5.435 | -0.048 | 81.818 |
| gnn_corrbinary | post_covid | 7.387 | 169.584 | 5.313 | 0.119 | 77.273 |
| gnn_multiedge_rt | post_covid | 7.911 | 185.320 | 5.631 | 0.241 | 81.818 |
| gnn_geo | post_covid | 7.966 | 199.511 | 5.909 | -0.026 | 86.364 |
| arima | post_covid | 8.473 | 309.925 | 8.064 |  | 100.000 |
| lstm | exclude_covid | 8.550 | 169.658 | 6.288 | 0.759 | 100.000 |
| gnn_uniform | post_covid | 8.624 | 202.943 | 5.998 | -0.080 | 90.909 |
| lstm | post_covid | 9.468 | 169.467 | 6.532 | 0.744 | 100.000 |
| dualtopo_no_bg | post_covid | 11.061 | 399.271 | 10.753 | 0.621 | 100.000 |
| dualtopo | post_covid | 11.100 | 400.624 | 10.792 | 0.614 | 100.000 |
| persistence | exclude_covid | 25.916 | 770.865 | 18.295 | -0.477 | 100.000 |
| persistence | post_covid | 25.916 | 770.865 | 18.295 | -0.477 | 100.000 |
| arima | exclude_covid | 25.921 | 782.173 | 18.544 | -0.508 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 4.124 | 81.278 | 3.406 | 0.778 | 93.023 |
| gnn_multiedge_rt | post_covid | 4.292 | 94.683 | 3.612 | 0.757 | 93.023 |
| gnn_multiedge_covid_rsv_full | full | 4.302 | 97.325 | 3.680 | 0.710 | 93.023 |
| gnn_multiedge_covid_rsv | post_covid | 4.531 | 91.605 | 3.827 | 0.770 | 83.721 |
| gnn_multiedge_leaknorm | post_covid | 4.588 | 94.403 | 3.772 | 0.743 | 93.023 |
| dualtopo_fullhistory | full | 4.888 | 67.386 | 3.224 | 0.582 | 100.000 |
| gnn_multiedge | post_covid | 4.980 | 86.809 | 3.924 | 0.751 | 90.698 |
| gnn_uniform | post_covid | 5.040 | 94.704 | 4.000 | 0.777 | 90.698 |
| gnn_multiedge_season_level | post_covid | 5.063 | 99.660 | 3.985 | 0.799 | 100.000 |
| gnn_multiedge_level | post_covid | 5.282 | 114.955 | 4.292 | 0.800 | 100.000 |
| gnn_multiedge_full | full | 5.516 | 129.512 | 4.719 | 0.730 | 97.674 |
| arima | post_covid | 5.672 | 168.530 | 4.863 |  | 100.000 |
| arima | exclude_covid | 5.892 | 184.255 | 5.092 |  | 100.000 |
| gnn_geo | post_covid | 6.230 | 103.753 | 4.767 | 0.782 | 95.349 |
| dualtopo | post_covid | 6.405 | 213.230 | 5.678 | 0.501 | 100.000 |
| dualtopo_no_bg | post_covid | 6.407 | 213.322 | 5.680 | 0.442 | 100.000 |
| gnn_corrbinary | post_covid | 6.683 | 119.163 | 5.346 | 0.758 | 90.698 |
| lstm | exclude_covid | 7.999 | 178.626 | 6.370 | 0.718 | 100.000 |
| lstm | post_covid | 8.479 | 182.604 | 6.674 | 0.612 | 100.000 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| persistence | exclude_covid | 10.274 | 227.099 | 7.649 | -0.390 | 100.000 |
| persistence | post_covid | 10.274 | 227.099 | 7.649 | -0.390 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_rt | post_covid | 4.668 | 52.604 | 3.925 | 0.683 | 96.000 |
| gnn_multiedge_season | post_covid | 4.826 | 59.106 | 4.071 | 0.680 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.929 | 68.922 | 4.220 | 0.567 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.391 | 74.340 | 4.697 | 0.655 | 96.000 |
| arima | exclude_covid | 5.461 | 79.323 | 4.335 |  | 100.000 |
| dualtopo | post_covid | 5.468 | 91.339 | 4.544 | 0.574 | 100.000 |
| dualtopo_no_bg | post_covid | 5.469 | 91.443 | 4.546 | 0.063 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.471 | 63.929 | 4.555 | 0.610 | 100.000 |
| arima | post_covid | 5.562 | 73.918 | 4.361 |  | 100.000 |
| gnn_multiedge_season_level | post_covid | 6.083 | 80.669 | 5.204 | 0.688 | 100.000 |
| gnn_uniform | post_covid | 6.118 | 68.672 | 4.975 | 0.669 | 96.000 |
| gnn_multiedge | post_covid | 6.122 | 66.616 | 5.006 | 0.608 | 96.000 |
| dualtopo_fullhistory | full | 6.134 | 46.319 | 4.263 | 0.317 | 100.000 |
| gnn_multiedge_full | full | 6.354 | 90.978 | 5.477 | 0.612 | 100.000 |
| gnn_multiedge_level | post_covid | 6.414 | 90.735 | 5.508 | 0.662 | 100.000 |
| gnn_geo | post_covid | 7.824 | 93.254 | 6.426 | 0.651 | 100.000 |
| gnn_corrbinary | post_covid | 8.333 | 108.061 | 7.176 | 0.608 | 96.000 |
| lstm | exclude_covid | 8.415 | 108.224 | 7.183 | 0.676 | 100.000 |
| lstm | post_covid | 8.700 | 101.622 | 7.521 | 0.545 | 100.000 |
| persistence | exclude_covid | 8.972 | 65.972 | 7.240 | 0.110 | 100.000 |
| persistence | post_covid | 8.972 | 65.972 | 7.240 | 0.110 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.197 | 96.645 | 1.781 | -0.034 | 100.000 |
| gnn_multiedge | post_covid | 2.684 | 114.855 | 2.422 | 0.356 | 83.333 |
| gnn_geo | post_covid | 2.775 | 118.334 | 2.464 | 0.395 | 88.889 |
| gnn_multiedge_season | post_covid | 2.876 | 112.074 | 2.483 | 0.195 | 83.333 |
| gnn_multiedge_covid_rsv | post_covid | 2.945 | 115.583 | 2.618 | 0.347 | 66.667 |
| gnn_uniform | post_covid | 2.952 | 130.861 | 2.646 | 0.232 | 83.333 |
| gnn_multiedge_leaknorm | post_covid | 2.953 | 136.727 | 2.685 | 0.219 | 83.333 |
| gnn_multiedge_level | post_covid | 3.082 | 148.594 | 2.603 | 0.625 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| gnn_multiedge_season_level | post_covid | 3.137 | 126.038 | 2.293 | 0.488 | 100.000 |
| gnn_corrbinary | post_covid | 3.201 | 134.583 | 2.803 | 0.388 | 83.333 |
| gnn_multiedge_covid_rsv_full | full | 3.235 | 136.773 | 2.929 | 0.307 | 83.333 |
| gnn_multiedge_rt | post_covid | 3.707 | 153.127 | 3.178 | 0.236 | 88.889 |
| gnn_multiedge_full | full | 4.074 | 183.033 | 3.666 | 0.286 | 94.444 |
| arima | post_covid | 5.822 | 299.936 | 5.560 |  | 100.000 |
| arima | exclude_covid | 6.443 | 329.994 | 6.143 |  | 100.000 |
| lstm | exclude_covid | 7.381 | 276.407 | 5.241 | 0.287 | 100.000 |
| dualtopo | post_covid | 7.516 | 382.524 | 7.254 | 0.205 | 100.000 |
| dualtopo_no_bg | post_covid | 7.517 | 382.597 | 7.256 | 0.207 | 100.000 |
| lstm | post_covid | 8.161 | 295.078 | 5.497 | 0.196 | 100.000 |
| persistence | exclude_covid | 11.847 | 450.887 | 8.217 | -0.317 | 100.000 |
| persistence | post_covid | 11.847 | 450.887 | 8.217 | -0.317 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
