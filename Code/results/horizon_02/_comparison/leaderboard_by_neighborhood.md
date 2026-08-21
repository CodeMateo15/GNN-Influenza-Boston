# Per-neighborhood leaderboard — horizon 2

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| lstm | 8 | 5 | 2 |
| gnn_multiedge_covid_rsv | 5 | 3 | 1 |
| arima | 1 | 3 | 0 |
| dualtopo_fullhistory | 0 | 0 | 8 |
| gnn_multiedge | 0 | 2 | 0 |
| gnn_multiedge_full | 0 | 1 | 0 |
| persistence | 0 | 0 | 1 |
| seasonal_naive | 0 | 0 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `arima (exclude_covid)`: BackBay+; `gnn_multiedge_covid_rsv (post_covid)`: Dorchest., HydePark, Roxbury, S.Boston, S.End; `lstm (post_covid)`: Allston, Charles., E.Boston, Fenway, JP, Mattapan, Roslind., W.Roxbury
- **Flu season (Oct–Mar)** — `arima (post_covid)`: Fenway, S.Boston, S.End; `gnn_multiedge (post_covid)`: Allston, JP; `gnn_multiedge_covid_rsv (post_covid)`: Dorchest., HydePark, Roxbury; `gnn_multiedge_full (full)`: BackBay+; `lstm (exclude_covid)`: Roslind.; `lstm (post_covid)`: Charles., E.Boston, Mattapan, W.Roxbury
- **Off-season (Apr–Sep)** — `dualtopo_fullhistory (full)`: Allston, BackBay+, Charles., Fenway, HydePark, JP, Roslind., S.End; `gnn_multiedge_covid_rsv (post_covid)`: E.Boston; `lstm (post_covid)`: S.Boston, W.Roxbury; `persistence (exclude_covid)`: Mattapan; `seasonal_naive (exclude_covid)`: Dorchest., Roxbury

`lstm (post_covid)` wins 8 of 14 neighborhoods. The pooled leaderboard is led by `gnn_multiedge_covid_rsv (post_covid)` instead, and `lstm (post_covid)` ranks 2 there. That is not a contradiction: the pooled metric flattens all 14 neighborhoods into one set of cells, so it is dominated by the high-rate ones (Dorchester and Roxbury average roughly five times Fenway's rate). Winning most neighborhoods and winning the pooled error are different achievements, and which one you want depends on whether you are allocating city-wide capacity or advising a specific neighborhood.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 32.903 | 51.756 | 19.224 | 0.804 | 95.918 |
| arima | post_covid | 35.619 | 95.828 | 23.673 | 0.777 | 93.878 |
| arima | exclude_covid | 35.798 | 106.740 | 24.376 | 0.775 | 93.878 |
| gnn_multiedge_covid_rsv_full | full | 39.472 | 65.569 | 25.344 | 0.775 | 77.551 |
| persistence | exclude_covid | 41.955 | 55.854 | 23.388 | 0.706 | 87.755 |
| persistence | post_covid | 41.955 | 55.854 | 23.388 | 0.706 | 87.755 |
| lstm | post_covid | 42.637 | 74.428 | 24.992 | 0.671 | 87.755 |
| gnn_multiedge_leaknorm | post_covid | 46.065 | 81.265 | 28.904 | 0.789 | 81.633 |
| gnn_multiedge_full | full | 49.353 | 75.854 | 31.818 | 0.729 | 83.673 |
| gnn_multiedge | post_covid | 49.495 | 95.981 | 33.216 | 0.766 | 89.796 |
| gnn_multiedge_rt | post_covid | 51.702 | 80.755 | 32.828 | 0.739 | 75.510 |
| gnn_multiedge_season | post_covid | 53.447 | 86.268 | 35.700 | 0.745 | 83.673 |
| lstm | exclude_covid | 54.278 | 76.524 | 28.926 | 0.631 | 87.755 |
| dualtopo | post_covid | 56.639 | 252.980 | 42.951 | -0.384 | 57.143 |
| dualtopo_no_bg | post_covid | 57.009 | 259.739 | 43.818 | -0.326 | 57.143 |
| dualtopo_fullhistory | full | 60.700 | 55.518 | 32.841 | 0.223 | 75.510 |
| gnn_corrbinary | post_covid | 60.815 | 103.936 | 40.471 | 0.704 | 81.633 |
| gnn_uniform | post_covid | 68.324 | 103.992 | 42.513 | 0.676 | 77.551 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| gnn_multiedge_season_level | post_covid | 83.388 | 161.008 | 59.006 | 0.607 | 59.184 |
| gnn_geo | post_covid | 95.021 | 188.389 | 63.240 | 0.603 | 73.469 |
| gnn_multiedge_level | post_covid | 96.990 | 169.789 | 64.064 | 0.534 | 63.265 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 42.991 | 33.247 | 26.647 | 0.760 | 92.308 |
| arima | exclude_covid | 45.508 | 47.631 | 30.276 | 0.728 | 88.462 |
| arima | post_covid | 45.927 | 45.470 | 30.458 | 0.728 | 88.462 |
| gnn_multiedge | post_covid | 50.286 | 50.310 | 36.759 | 0.777 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 51.176 | 51.524 | 36.429 | 0.703 | 65.385 |
| gnn_multiedge_leaknorm | post_covid | 52.192 | 42.124 | 33.621 | 0.773 | 80.769 |
| persistence | exclude_covid | 56.416 | 45.427 | 35.510 | 0.608 | 80.769 |
| persistence | post_covid | 56.416 | 45.427 | 35.510 | 0.608 | 80.769 |
| lstm | post_covid | 57.329 | 49.005 | 37.337 | 0.581 | 76.923 |
| gnn_corrbinary | post_covid | 59.045 | 61.845 | 45.017 | 0.730 | 88.462 |
| gnn_multiedge_full | full | 60.751 | 56.428 | 42.226 | 0.667 | 80.769 |
| gnn_multiedge_rt | post_covid | 61.689 | 54.229 | 41.828 | 0.695 | 73.077 |
| gnn_multiedge_season | post_covid | 62.740 | 61.897 | 46.151 | 0.703 | 84.615 |
| dualtopo_no_bg | post_covid | 63.686 | 82.489 | 41.182 | 0.055 | 73.077 |
| dualtopo | post_covid | 63.937 | 80.111 | 40.759 | -0.138 | 73.077 |
| gnn_uniform | post_covid | 68.126 | 59.204 | 47.090 | 0.698 | 80.769 |
| lstm | exclude_covid | 73.091 | 54.618 | 43.480 | 0.537 | 76.923 |
| dualtopo_fullhistory | full | 82.871 | 65.431 | 55.597 | -0.034 | 57.692 |
| gnn_geo | post_covid | 92.770 | 105.009 | 68.574 | 0.621 | 69.231 |
| gnn_multiedge_season_level | post_covid | 93.427 | 117.246 | 74.798 | 0.523 | 42.308 |
| gnn_multiedge_level | post_covid | 95.710 | 112.903 | 73.473 | 0.510 | 50.000 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| dualtopo_fullhistory | full | 9.281 | 44.311 | 7.116 | 0.785 | 95.652 |
| persistence | exclude_covid | 12.332 | 67.640 | 9.685 | 0.788 | 95.652 |
| persistence | post_covid | 12.332 | 67.640 | 9.685 | 0.788 | 95.652 |
| lstm | post_covid | 12.557 | 103.167 | 11.037 | 0.805 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.736 | 72.678 | 10.833 | 0.788 | 100.000 |
| lstm | exclude_covid | 15.407 | 101.288 | 12.473 | 0.824 | 100.000 |
| arima | post_covid | 17.847 | 152.754 | 16.002 | 0.684 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 18.937 | 81.445 | 12.812 | 0.796 | 91.304 |
| arima | exclude_covid | 19.721 | 173.558 | 17.705 | 0.689 | 100.000 |
| gnn_multiedge_full | full | 31.893 | 97.814 | 20.053 | 0.825 | 86.957 |
| gnn_multiedge_rt | post_covid | 37.324 | 110.741 | 22.655 | 0.815 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 37.966 | 125.511 | 23.572 | 0.818 | 82.609 |
| gnn_multiedge_season | post_covid | 40.446 | 113.818 | 23.886 | 0.817 | 82.609 |
| dualtopo | post_covid | 47.045 | 448.396 | 45.429 | -0.808 | 39.130 |
| dualtopo_no_bg | post_covid | 48.364 | 460.108 | 46.798 | -0.845 | 39.130 |
| gnn_multiedge | post_covid | 48.585 | 147.609 | 29.210 | 0.811 | 82.609 |
| gnn_corrbinary | post_covid | 62.754 | 151.518 | 35.331 | 0.804 | 73.913 |
| gnn_uniform | post_covid | 68.547 | 154.622 | 37.340 | 0.800 | 73.913 |
| gnn_multiedge_season_level | post_covid | 70.334 | 210.478 | 41.154 | 0.794 | 78.261 |
| gnn_geo | post_covid | 97.502 | 282.645 | 57.211 | 0.786 | 78.261 |
| gnn_multiedge_level | post_covid | 98.417 | 234.094 | 53.428 | 0.789 | 78.261 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 34.905 | 65.623 | 20.812 | 0.724 | 95.918 |
| lstm | post_covid | 38.168 | 58.915 | 22.186 | 0.662 | 87.755 |
| arima | post_covid | 39.165 | 102.880 | 23.377 | 0.662 | 93.878 |
| arima | exclude_covid | 39.202 | 118.012 | 24.667 | 0.661 | 91.837 |
| persistence | exclude_covid | 41.657 | 66.599 | 23.727 | 0.655 | 89.796 |
| persistence | post_covid | 41.657 | 66.599 | 23.727 | 0.655 | 89.796 |
| gnn_multiedge_covid_rsv_full | full | 42.971 | 82.869 | 27.169 | 0.691 | 73.469 |
| lstm | exclude_covid | 45.700 | 74.079 | 26.175 | 0.627 | 85.714 |
| gnn_multiedge_leaknorm | post_covid | 47.456 | 92.638 | 27.562 | 0.702 | 85.714 |
| gnn_multiedge | post_covid | 49.158 | 106.984 | 31.607 | 0.685 | 91.837 |
| dualtopo | post_covid | 51.156 | 231.030 | 37.547 | -0.332 | 65.306 |
| dualtopo_no_bg | post_covid | 51.403 | 237.241 | 38.205 | -0.204 | 65.306 |
| gnn_multiedge_full | full | 51.895 | 92.531 | 32.616 | 0.641 | 81.633 |
| gnn_multiedge_rt | post_covid | 52.910 | 97.958 | 32.463 | 0.641 | 75.510 |
| gnn_multiedge_season | post_covid | 54.396 | 102.506 | 34.872 | 0.645 | 87.755 |
| dualtopo_fullhistory | full | 55.587 | 60.757 | 30.040 | 0.190 | 69.388 |
| gnn_corrbinary | post_covid | 57.069 | 115.559 | 37.671 | 0.636 | 79.592 |
| gnn_uniform | post_covid | 64.588 | 119.166 | 40.356 | 0.598 | 77.551 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| gnn_multiedge_season_level | post_covid | 74.760 | 161.166 | 52.159 | 0.511 | 61.224 |
| gnn_geo | post_covid | 81.953 | 198.835 | 54.114 | 0.522 | 77.551 |
| gnn_multiedge_level | post_covid | 86.596 | 172.220 | 56.935 | 0.438 | 61.224 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 46.017 | 50.591 | 30.520 | 0.654 | 92.308 |
| arima | exclude_covid | 50.900 | 63.149 | 32.843 | 0.587 | 84.615 |
| lstm | post_covid | 51.084 | 45.746 | 32.898 | 0.567 | 76.923 |
| arima | post_covid | 51.677 | 59.721 | 32.582 | 0.584 | 88.462 |
| persistence | exclude_covid | 56.000 | 61.702 | 37.300 | 0.554 | 88.462 |
| persistence | post_covid | 56.000 | 61.702 | 37.300 | 0.554 | 88.462 |
| gnn_multiedge | post_covid | 56.259 | 74.267 | 38.040 | 0.649 | 88.462 |
| gnn_multiedge_covid_rsv_full | full | 56.579 | 78.748 | 40.925 | 0.602 | 61.538 |
| gnn_multiedge_leaknorm | post_covid | 58.000 | 61.939 | 34.172 | 0.651 | 84.615 |
| dualtopo_no_bg | post_covid | 60.060 | 91.907 | 38.989 | 0.114 | 73.077 |
| dualtopo | post_covid | 60.303 | 89.453 | 38.712 | -0.078 | 73.077 |
| lstm | exclude_covid | 61.053 | 56.044 | 38.690 | 0.533 | 73.077 |
| gnn_corrbinary | post_covid | 61.648 | 86.905 | 44.832 | 0.614 | 84.615 |
| gnn_multiedge_full | full | 66.372 | 83.794 | 45.687 | 0.553 | 73.077 |
| gnn_multiedge_rt | post_covid | 66.801 | 82.672 | 44.071 | 0.560 | 65.385 |
| gnn_multiedge_season | post_covid | 68.003 | 90.049 | 47.643 | 0.562 | 80.769 |
| gnn_uniform | post_covid | 70.635 | 87.130 | 47.469 | 0.573 | 80.769 |
| dualtopo_fullhistory | full | 75.439 | 61.340 | 48.091 | -0.040 | 53.846 |
| gnn_geo | post_covid | 81.744 | 126.269 | 57.558 | 0.515 | 76.923 |
| gnn_multiedge_season_level | post_covid | 86.459 | 140.108 | 67.978 | 0.388 | 46.154 |
| gnn_multiedge_level | post_covid | 89.717 | 138.010 | 67.496 | 0.359 | 46.154 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| dualtopo_fullhistory | full | 12.226 | 60.097 | 9.635 | 0.576 | 86.957 |
| persistence | exclude_covid | 12.327 | 72.136 | 8.383 | 0.644 | 91.304 |
| persistence | post_covid | 12.327 | 72.136 | 8.383 | 0.644 | 91.304 |
| lstm | post_covid | 12.395 | 73.803 | 10.076 | 0.691 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.207 | 82.617 | 9.837 | 0.628 | 100.000 |
| lstm | exclude_covid | 15.352 | 94.466 | 12.027 | 0.706 | 100.000 |
| arima | post_covid | 15.783 | 151.669 | 12.972 | 0.662 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 17.752 | 87.529 | 11.618 | 0.648 | 86.957 |
| arima | exclude_covid | 18.583 | 180.032 | 15.425 | 0.608 | 100.000 |
| gnn_multiedge_full | full | 27.526 | 102.408 | 17.841 | 0.698 | 91.304 |
| gnn_multiedge_rt | post_covid | 30.327 | 115.237 | 19.341 | 0.672 | 86.957 |
| gnn_multiedge_leaknorm | post_covid | 31.547 | 127.340 | 20.089 | 0.690 | 86.957 |
| gnn_multiedge_season | post_covid | 32.808 | 116.589 | 20.434 | 0.689 | 95.652 |
| dualtopo | post_covid | 38.268 | 391.073 | 36.230 | -0.646 | 56.522 |
| dualtopo_no_bg | post_covid | 39.389 | 401.531 | 37.319 | -0.676 | 56.522 |
| gnn_multiedge | post_covid | 39.627 | 143.968 | 24.336 | 0.682 | 95.652 |
| gnn_corrbinary | post_covid | 51.404 | 147.950 | 29.575 | 0.670 | 73.913 |
| gnn_uniform | post_covid | 56.985 | 155.381 | 32.315 | 0.660 | 73.913 |
| gnn_multiedge_season_level | post_covid | 58.796 | 184.971 | 34.276 | 0.660 | 78.261 |
| gnn_geo | post_covid | 82.189 | 280.866 | 50.220 | 0.660 | 78.261 |
| gnn_multiedge_level | post_covid | 82.927 | 210.892 | 44.998 | 0.651 | 78.261 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 27.654 | 68.823 | 16.471 | 0.743 | 88.095 |
| lstm | exclude_covid | 27.753 | 66.960 | 16.787 | 0.706 | 78.571 |
| gnn_multiedge_covid_rsv | post_covid | 30.751 | 77.138 | 19.117 | 0.632 | 88.095 |
| gnn_multiedge_leaknorm | post_covid | 31.889 | 112.559 | 23.374 | 0.720 | 85.714 |
| gnn_multiedge | post_covid | 32.113 | 118.800 | 24.043 | 0.701 | 92.857 |
| gnn_multiedge_covid_rsv_full | full | 32.714 | 100.426 | 21.107 | 0.643 | 69.048 |
| arima | post_covid | 33.967 | 130.086 | 23.334 | 0.592 | 88.095 |
| gnn_multiedge_rt | post_covid | 34.027 | 112.930 | 23.463 | 0.676 | 83.333 |
| arima | exclude_covid | 34.268 | 112.558 | 22.727 | 0.510 | 90.476 |
| gnn_multiedge_season | post_covid | 35.013 | 119.519 | 24.534 | 0.680 | 83.333 |
| gnn_corrbinary | post_covid | 35.295 | 127.475 | 26.092 | 0.674 | 85.714 |
| gnn_multiedge_full | full | 35.522 | 109.506 | 23.209 | 0.644 | 80.952 |
| persistence | exclude_covid | 36.145 | 92.139 | 22.529 | 0.570 | 78.571 |
| persistence | post_covid | 36.145 | 92.139 | 22.529 | 0.570 | 78.571 |
| gnn_uniform | post_covid | 38.359 | 123.952 | 27.757 | 0.654 | 78.571 |
| dualtopo | post_covid | 38.808 | 163.069 | 25.769 | -0.264 | 90.476 |
| dualtopo_no_bg | post_covid | 38.824 | 167.515 | 26.103 | -0.089 | 90.476 |
| dualtopo_fullhistory | full | 40.121 | 69.767 | 20.831 | 0.214 | 80.952 |
| gnn_multiedge_season_level | post_covid | 41.421 | 165.878 | 30.361 | 0.579 | 64.286 |
| gnn_geo | post_covid | 46.382 | 169.621 | 33.306 | 0.571 | 73.810 |
| gnn_multiedge_level | post_covid | 47.913 | 168.634 | 33.238 | 0.498 | 64.286 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 34.481 | 67.806 | 22.339 | 0.669 | 69.231 |
| lstm | post_covid | 34.533 | 68.633 | 22.336 | 0.710 | 80.769 |
| gnn_multiedge | post_covid | 36.002 | 115.388 | 28.148 | 0.698 | 92.308 |
| gnn_multiedge_leaknorm | post_covid | 36.630 | 108.567 | 27.953 | 0.711 | 80.769 |
| gnn_corrbinary | post_covid | 37.687 | 127.438 | 29.585 | 0.688 | 88.462 |
| gnn_multiedge_covid_rsv | post_covid | 37.916 | 78.261 | 25.466 | 0.593 | 84.615 |
| gnn_multiedge_covid_rsv_full | full | 40.244 | 113.430 | 28.203 | 0.600 | 57.692 |
| gnn_multiedge_rt | post_covid | 40.497 | 121.494 | 29.416 | 0.649 | 76.923 |
| gnn_uniform | post_covid | 40.811 | 118.305 | 31.399 | 0.670 | 84.615 |
| gnn_multiedge_season | post_covid | 41.376 | 130.296 | 30.777 | 0.653 | 80.769 |
| arima | post_covid | 41.618 | 118.630 | 29.984 | 0.568 | 80.769 |
| arima | exclude_covid | 42.302 | 95.090 | 29.148 | 0.463 | 84.615 |
| gnn_multiedge_full | full | 42.855 | 123.187 | 29.807 | 0.607 | 76.923 |
| gnn_geo | post_covid | 44.722 | 147.931 | 34.390 | 0.621 | 73.077 |
| persistence | exclude_covid | 45.027 | 105.865 | 31.369 | 0.517 | 73.077 |
| persistence | post_covid | 45.027 | 105.865 | 31.369 | 0.517 | 73.077 |
| gnn_multiedge_season_level | post_covid | 45.832 | 185.396 | 36.025 | 0.555 | 57.692 |
| dualtopo_no_bg | post_covid | 46.504 | 120.977 | 30.580 | 0.107 | 84.615 |
| dualtopo | post_covid | 46.655 | 118.147 | 30.475 | -0.120 | 84.615 |
| gnn_multiedge_level | post_covid | 48.324 | 175.641 | 36.384 | 0.510 | 57.692 |
| dualtopo_fullhistory | full | 50.592 | 79.850 | 29.847 | 0.067 | 73.077 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 8.138 | 53.381 | 6.179 | 0.518 | 93.750 |
| lstm | post_covid | 8.338 | 69.131 | 6.940 | 0.512 | 100.000 |
| lstm | exclude_covid | 9.477 | 65.584 | 7.765 | 0.513 | 93.750 |
| persistence | exclude_covid | 11.618 | 69.835 | 8.162 | 0.281 | 87.500 |
| persistence | post_covid | 11.618 | 69.835 | 8.162 | 0.281 | 87.500 |
| gnn_multiedge_covid_rsv | post_covid | 12.088 | 75.312 | 8.799 | 0.268 | 93.750 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| arima | exclude_covid | 13.216 | 140.943 | 12.293 | 0.222 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 13.323 | 79.295 | 9.574 | 0.336 | 87.500 |
| arima | post_covid | 14.627 | 148.704 | 12.527 | 0.101 | 100.000 |
| gnn_multiedge_full | full | 18.108 | 87.276 | 12.487 | 0.487 | 87.500 |
| gnn_multiedge_rt | post_covid | 19.346 | 99.013 | 13.790 | 0.483 | 93.750 |
| dualtopo | post_covid | 20.404 | 236.068 | 18.123 | -0.577 | 100.000 |
| gnn_multiedge_season | post_covid | 20.883 | 102.008 | 14.389 | 0.479 | 87.500 |
| dualtopo_no_bg | post_covid | 21.031 | 243.139 | 18.828 | -0.529 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 22.112 | 119.047 | 15.933 | 0.477 | 93.750 |
| gnn_multiedge | post_covid | 24.511 | 124.343 | 17.372 | 0.498 | 93.750 |
| gnn_corrbinary | post_covid | 31.017 | 127.537 | 20.416 | 0.531 | 81.250 |
| gnn_multiedge_season_level | post_covid | 33.021 | 134.161 | 21.157 | 0.621 | 75.000 |
| gnn_uniform | post_covid | 33.999 | 133.129 | 21.840 | 0.529 | 68.750 |
| gnn_multiedge_level | post_covid | 47.236 | 157.247 | 28.126 | 0.616 | 75.000 |
| gnn_geo | post_covid | 48.961 | 204.869 | 31.544 | 0.568 | 75.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 20.698 | 72.350 | 13.009 | 0.765 | 91.837 |
| arima | post_covid | 20.917 | 100.715 | 13.217 | 0.763 | 95.918 |
| lstm | post_covid | 22.295 | 91.860 | 13.686 | 0.717 | 95.918 |
| arima | exclude_covid | 22.642 | 70.316 | 13.021 | 0.744 | 93.878 |
| gnn_multiedge_covid_rsv_full | full | 23.953 | 81.637 | 15.896 | 0.747 | 87.755 |
| persistence | exclude_covid | 24.086 | 66.633 | 13.929 | 0.716 | 93.878 |
| persistence | post_covid | 24.086 | 66.633 | 13.929 | 0.716 | 93.878 |
| gnn_multiedge_leaknorm | post_covid | 24.932 | 114.321 | 18.203 | 0.783 | 95.918 |
| lstm | exclude_covid | 26.075 | 64.686 | 14.370 | 0.723 | 89.796 |
| gnn_multiedge_full | full | 26.765 | 96.988 | 18.115 | 0.734 | 93.878 |
| gnn_multiedge | post_covid | 27.402 | 126.761 | 19.550 | 0.736 | 97.959 |
| gnn_multiedge_rt | post_covid | 27.782 | 109.512 | 19.382 | 0.731 | 85.714 |
| gnn_multiedge_season | post_covid | 28.828 | 114.594 | 20.437 | 0.732 | 93.878 |
| dualtopo | post_covid | 32.513 | 220.492 | 24.040 | -0.356 | 89.796 |
| dualtopo_no_bg | post_covid | 32.640 | 226.223 | 24.413 | -0.197 | 89.796 |
| gnn_corrbinary | post_covid | 32.811 | 136.771 | 22.650 | 0.671 | 89.796 |
| dualtopo_fullhistory | full | 34.138 | 65.457 | 18.181 | 0.207 | 83.673 |
| gnn_uniform | post_covid | 35.815 | 137.682 | 24.636 | 0.660 | 83.673 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| gnn_multiedge_season_level | post_covid | 41.711 | 179.873 | 28.858 | 0.569 | 69.388 |
| gnn_geo | post_covid | 47.374 | 219.394 | 32.468 | 0.560 | 77.551 |
| gnn_multiedge_level | post_covid | 49.489 | 198.949 | 31.896 | 0.464 | 71.429 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 26.900 | 72.251 | 16.941 | 0.723 | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 27.468 | 68.333 | 18.940 | 0.715 | 84.615 |
| gnn_multiedge_leaknorm | post_covid | 29.015 | 92.688 | 22.715 | 0.774 | 96.154 |
| lstm | post_covid | 29.571 | 73.382 | 19.343 | 0.648 | 92.308 |
| arima | exclude_covid | 30.008 | 59.311 | 18.905 | 0.690 | 88.462 |
| gnn_multiedge | post_covid | 30.206 | 101.236 | 23.327 | 0.738 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 31.750 | 83.471 | 23.693 | 0.684 | 76.923 |
| persistence | exclude_covid | 32.215 | 63.326 | 20.865 | 0.652 | 88.462 |
| persistence | post_covid | 32.215 | 63.326 | 20.865 | 0.652 | 88.462 |
| gnn_multiedge_full | full | 33.256 | 88.877 | 24.540 | 0.694 | 88.462 |
| gnn_multiedge_rt | post_covid | 33.943 | 95.217 | 25.695 | 0.698 | 80.769 |
| gnn_corrbinary | post_covid | 34.735 | 108.936 | 26.678 | 0.684 | 92.308 |
| gnn_multiedge_season | post_covid | 34.942 | 102.717 | 27.168 | 0.698 | 88.462 |
| lstm | exclude_covid | 35.024 | 60.510 | 21.930 | 0.667 | 80.769 |
| gnn_uniform | post_covid | 37.669 | 101.645 | 29.059 | 0.682 | 84.615 |
| dualtopo_no_bg | post_covid | 38.999 | 134.120 | 26.040 | 0.089 | 80.769 |
| dualtopo | post_covid | 39.144 | 131.093 | 25.945 | -0.161 | 80.769 |
| gnn_multiedge_season_level | post_covid | 46.374 | 163.198 | 36.056 | 0.522 | 61.538 |
| dualtopo_fullhistory | full | 46.527 | 81.064 | 30.169 | -0.003 | 69.231 |
| gnn_geo | post_covid | 47.216 | 155.469 | 35.595 | 0.594 | 76.923 |
| gnn_multiedge_level | post_covid | 49.468 | 160.843 | 36.179 | 0.458 | 65.385 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 5.969 | 47.814 | 4.630 | 0.611 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.735 | 76.890 | 6.306 | 0.478 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| lstm | exclude_covid | 7.866 | 69.407 | 5.824 | 0.587 | 100.000 |
| persistence | exclude_covid | 7.924 | 70.371 | 6.087 | 0.412 | 100.000 |
| persistence | post_covid | 7.924 | 70.371 | 6.087 | 0.412 | 100.000 |
| lstm | post_covid | 8.396 | 112.747 | 7.291 | 0.596 | 100.000 |
| arima | exclude_covid | 8.613 | 82.755 | 6.368 | 0.380 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 9.098 | 79.564 | 7.082 | 0.548 | 100.000 |
| arima | post_covid | 10.684 | 132.891 | 9.009 | 0.347 | 100.000 |
| gnn_multiedge_full | full | 16.613 | 106.158 | 10.851 | 0.487 | 100.000 |
| gnn_multiedge_rt | post_covid | 18.494 | 125.672 | 12.246 | 0.470 | 91.304 |
| gnn_multiedge_leaknorm | post_covid | 19.304 | 138.776 | 13.103 | 0.490 | 95.652 |
| gnn_multiedge_season | post_covid | 19.757 | 128.021 | 12.829 | 0.506 | 100.000 |
| dualtopo | post_covid | 22.801 | 321.552 | 21.886 | -0.523 | 100.000 |
| dualtopo_no_bg | post_covid | 23.460 | 330.339 | 22.573 | -0.398 | 100.000 |
| gnn_multiedge | post_covid | 23.839 | 155.615 | 15.280 | 0.487 | 100.000 |
| gnn_corrbinary | post_covid | 30.491 | 168.236 | 18.097 | 0.486 | 86.957 |
| gnn_uniform | post_covid | 33.595 | 178.419 | 19.636 | 0.500 | 82.609 |
| gnn_multiedge_season_level | post_covid | 35.713 | 198.722 | 20.721 | 0.503 | 78.261 |
| gnn_geo | post_covid | 47.553 | 291.657 | 28.934 | 0.478 | 78.261 |
| gnn_multiedge_level | post_covid | 49.511 | 242.025 | 27.055 | 0.490 | 78.261 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 18.551 | 63.642 | 10.378 | 0.541 | 94.286 |
| gnn_multiedge_covid_rsv | post_covid | 19.597 | 71.733 | 10.626 | 0.535 | 88.571 |
| lstm | exclude_covid | 20.283 | 71.542 | 11.110 | 0.466 | 88.571 |
| arima | post_covid | 20.661 | 92.903 | 12.278 | 0.365 | 94.286 |
| dualtopo_fullhistory | full | 20.696 | 85.024 | 13.377 | 0.387 | 91.429 |
| gnn_multiedge_covid_rsv_full | full | 21.019 | 82.972 | 12.246 | 0.559 | 88.571 |
| dualtopo | post_covid | 21.938 | 118.760 | 14.045 | -0.216 | 88.571 |
| dualtopo_no_bg | post_covid | 21.943 | 122.186 | 14.221 | -0.088 | 88.571 |
| gnn_multiedge_leaknorm | post_covid | 22.517 | 104.662 | 14.635 | 0.585 | 88.571 |
| persistence | exclude_covid | 22.776 | 76.874 | 12.360 | 0.464 | 94.286 |
| persistence | post_covid | 22.776 | 76.874 | 12.360 | 0.464 | 94.286 |
| arima | exclude_covid | 22.799 | 90.996 | 13.073 | 0.299 | 94.286 |
| gnn_multiedge | post_covid | 22.808 | 122.790 | 16.175 | 0.575 | 91.429 |
| gnn_multiedge_full | full | 23.740 | 106.231 | 14.864 | 0.533 | 88.571 |
| gnn_multiedge_rt | post_covid | 24.178 | 112.108 | 15.704 | 0.540 | 91.429 |
| gnn_multiedge_season | post_covid | 24.763 | 122.284 | 16.813 | 0.558 | 91.429 |
| gnn_uniform | post_covid | 26.140 | 126.325 | 17.964 | 0.541 | 94.286 |
| gnn_corrbinary | post_covid | 26.258 | 143.802 | 19.146 | 0.537 | 94.286 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| gnn_multiedge_season_level | post_covid | 29.701 | 184.351 | 21.493 | 0.453 | 71.429 |
| gnn_geo | post_covid | 33.432 | 188.123 | 25.032 | 0.488 | 80.000 |
| gnn_multiedge_level | post_covid | 34.450 | 206.284 | 24.557 | 0.385 | 65.714 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 23.642 | 73.819 | 14.904 | 0.476 | 90.476 |
| gnn_multiedge_covid_rsv | post_covid | 24.905 | 91.278 | 15.285 | 0.485 | 80.952 |
| lstm | exclude_covid | 25.882 | 85.781 | 16.012 | 0.392 | 80.952 |
| arima | post_covid | 26.137 | 101.203 | 16.902 | 0.280 | 90.476 |
| dualtopo_fullhistory | full | 26.487 | 112.233 | 19.765 | 0.249 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 26.793 | 108.929 | 17.918 | 0.498 | 80.952 |
| gnn_multiedge | post_covid | 26.907 | 133.531 | 20.539 | 0.548 | 85.714 |
| dualtopo_no_bg | post_covid | 26.981 | 111.570 | 17.460 | 0.045 | 80.952 |
| dualtopo | post_covid | 27.065 | 108.755 | 17.363 | -0.045 | 80.952 |
| gnn_multiedge_leaknorm | post_covid | 27.573 | 116.303 | 19.294 | 0.549 | 80.952 |
| arima | exclude_covid | 28.866 | 97.139 | 17.942 | 0.224 | 90.476 |
| gnn_uniform | post_covid | 28.947 | 121.788 | 21.228 | 0.543 | 90.476 |
| persistence | exclude_covid | 28.952 | 97.493 | 17.910 | 0.401 | 90.476 |
| persistence | post_covid | 28.952 | 97.493 | 17.910 | 0.401 | 90.476 |
| gnn_multiedge_full | full | 29.534 | 130.093 | 20.631 | 0.480 | 80.952 |
| gnn_multiedge_rt | post_covid | 29.845 | 131.832 | 21.388 | 0.493 | 85.714 |
| gnn_corrbinary | post_covid | 30.082 | 158.405 | 24.066 | 0.510 | 90.476 |
| gnn_multiedge_season | post_covid | 30.401 | 144.118 | 22.838 | 0.511 | 85.714 |
| gnn_multiedge_season_level | post_covid | 33.522 | 215.008 | 26.588 | 0.401 | 61.905 |
| gnn_geo | post_covid | 34.917 | 181.270 | 28.860 | 0.494 | 80.952 |
| gnn_multiedge_level | post_covid | 35.413 | 219.148 | 27.875 | 0.366 | 61.905 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 4.296 | 44.211 | 3.795 | 0.609 | 100.000 |
| lstm | post_covid | 4.677 | 48.376 | 3.589 | 0.574 | 100.000 |
| lstm | exclude_covid | 4.863 | 50.182 | 3.758 | 0.529 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.259 | 44.038 | 3.739 | 0.517 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.451 | 42.417 | 3.636 | 0.391 | 100.000 |
| persistence | exclude_covid | 6.293 | 45.947 | 4.036 | 0.289 | 100.000 |
| persistence | post_covid | 6.293 | 45.947 | 4.036 | 0.289 | 100.000 |
| arima | post_covid | 6.516 | 80.454 | 5.343 | 0.277 | 100.000 |
| arima | exclude_covid | 7.047 | 81.782 | 5.769 | 0.115 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| gnn_multiedge_full | full | 10.029 | 70.437 | 6.213 | 0.523 | 100.000 |
| dualtopo | post_covid | 10.217 | 133.768 | 9.068 | -0.534 | 100.000 |
| dualtopo_no_bg | post_covid | 10.571 | 138.110 | 9.361 | -0.282 | 100.000 |
| gnn_multiedge_rt | post_covid | 11.197 | 82.521 | 7.179 | 0.511 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.275 | 87.200 | 7.647 | 0.512 | 100.000 |
| gnn_multiedge_season | post_covid | 12.113 | 89.534 | 7.777 | 0.504 | 100.000 |
| gnn_multiedge | post_covid | 14.647 | 106.679 | 9.628 | 0.517 | 100.000 |
| gnn_corrbinary | post_covid | 19.140 | 121.897 | 11.766 | 0.538 | 100.000 |
| gnn_uniform | post_covid | 21.246 | 133.131 | 13.069 | 0.549 | 100.000 |
| gnn_multiedge_season_level | post_covid | 22.800 | 138.366 | 13.851 | 0.581 | 85.714 |
| gnn_geo | post_covid | 31.074 | 198.402 | 19.289 | 0.553 | 78.571 |
| gnn_multiedge_level | post_covid | 32.954 | 186.987 | 19.578 | 0.573 | 71.429 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 15.127 | 99.008 | 10.486 | 0.788 | 95.745 |
| gnn_multiedge_covid_rsv | post_covid | 16.483 | 76.689 | 9.982 | 0.689 | 97.872 |
| lstm | exclude_covid | 16.611 | 83.802 | 10.296 | 0.772 | 93.617 |
| gnn_multiedge_covid_rsv_full | full | 17.310 | 86.982 | 11.188 | 0.731 | 95.745 |
| arima | post_covid | 17.456 | 130.553 | 12.170 | 0.663 | 95.745 |
| arima | exclude_covid | 17.459 | 120.047 | 11.408 | 0.669 | 95.745 |
| persistence | exclude_covid | 18.550 | 69.059 | 10.362 | 0.664 | 95.745 |
| persistence | post_covid | 18.550 | 69.059 | 10.362 | 0.664 | 95.745 |
| gnn_multiedge_leaknorm | post_covid | 19.020 | 120.907 | 13.356 | 0.768 | 100.000 |
| gnn_multiedge | post_covid | 21.134 | 139.435 | 15.170 | 0.720 | 100.000 |
| gnn_multiedge_full | full | 21.445 | 107.634 | 14.059 | 0.680 | 97.872 |
| gnn_multiedge_rt | post_covid | 21.610 | 116.737 | 14.488 | 0.711 | 93.617 |
| gnn_multiedge_season | post_covid | 22.735 | 125.835 | 15.539 | 0.720 | 100.000 |
| dualtopo_fullhistory | full | 23.113 | 76.784 | 12.503 | 0.275 | 91.489 |
| dualtopo | post_covid | 25.200 | 302.048 | 21.418 | -0.375 | 93.617 |
| dualtopo_no_bg | post_covid | 25.486 | 309.985 | 21.867 | -0.171 | 93.617 |
| gnn_corrbinary | post_covid | 26.400 | 157.308 | 18.252 | 0.643 | 95.745 |
| gnn_uniform | post_covid | 27.886 | 154.553 | 18.165 | 0.646 | 91.489 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| gnn_multiedge_season_level | post_covid | 39.847 | 256.363 | 27.693 | 0.591 | 68.085 |
| gnn_geo | post_covid | 41.464 | 252.034 | 27.304 | 0.540 | 78.723 |
| gnn_multiedge_level | post_covid | 47.007 | 277.394 | 30.774 | 0.486 | 70.213 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 18.233 | 66.385 | 12.933 | 0.755 | 92.308 |
| lstm | exclude_covid | 20.412 | 57.827 | 13.103 | 0.741 | 88.462 |
| gnn_multiedge_leaknorm | post_covid | 20.729 | 79.360 | 15.299 | 0.771 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 21.245 | 52.890 | 13.750 | 0.636 | 96.154 |
| gnn_multiedge | post_covid | 21.660 | 92.174 | 16.792 | 0.741 | 100.000 |
| arima | post_covid | 21.774 | 70.729 | 14.915 | 0.592 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 22.008 | 67.794 | 15.631 | 0.677 | 92.308 |
| arima | exclude_covid | 22.087 | 67.839 | 14.415 | 0.606 | 92.308 |
| persistence | exclude_covid | 24.428 | 52.898 | 15.238 | 0.594 | 92.308 |
| persistence | post_covid | 24.428 | 52.898 | 15.238 | 0.594 | 92.308 |
| gnn_multiedge_rt | post_covid | 25.672 | 86.004 | 18.081 | 0.678 | 88.462 |
| gnn_multiedge_full | full | 26.265 | 86.941 | 18.339 | 0.630 | 96.154 |
| gnn_corrbinary | post_covid | 26.329 | 113.165 | 20.154 | 0.673 | 100.000 |
| gnn_multiedge_season | post_covid | 26.489 | 95.172 | 19.296 | 0.692 | 100.000 |
| gnn_uniform | post_covid | 26.594 | 95.397 | 18.898 | 0.705 | 96.154 |
| dualtopo | post_covid | 26.772 | 146.767 | 20.332 | -0.213 | 88.462 |
| dualtopo_no_bg | post_covid | 26.816 | 150.894 | 20.628 | 0.139 | 88.462 |
| dualtopo_fullhistory | full | 30.526 | 58.688 | 18.363 | 0.115 | 84.615 |
| gnn_geo | post_covid | 40.488 | 156.824 | 28.214 | 0.579 | 80.769 |
| gnn_multiedge_season_level | post_covid | 43.259 | 207.451 | 32.329 | 0.565 | 61.538 |
| gnn_multiedge_level | post_covid | 46.153 | 208.179 | 33.333 | 0.503 | 65.385 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 5.598 | 89.067 | 4.324 | 0.447 | 100.000 |
| persistence | post_covid | 5.598 | 89.067 | 4.324 | 0.447 | 100.000 |
| dualtopo_fullhistory | full | 6.474 | 99.190 | 5.246 | 0.516 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.014 | 106.155 | 5.316 | 0.434 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 8.423 | 110.738 | 5.689 | 0.473 | 100.000 |
| arima | exclude_covid | 8.842 | 184.684 | 7.684 | 0.398 | 100.000 |
| arima | post_covid | 9.744 | 204.620 | 8.770 | 0.448 | 100.000 |
| lstm | post_covid | 10.028 | 139.399 | 7.457 | 0.604 | 100.000 |
| lstm | exclude_covid | 10.087 | 115.963 | 6.820 | 0.601 | 100.000 |
| gnn_multiedge_full | full | 13.235 | 133.253 | 8.760 | 0.609 | 100.000 |
| gnn_multiedge_rt | post_covid | 15.140 | 154.788 | 10.038 | 0.611 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 16.663 | 172.346 | 10.950 | 0.612 | 100.000 |
| gnn_multiedge_season | post_covid | 16.972 | 163.799 | 10.888 | 0.601 | 100.000 |
| gnn_multiedge | post_covid | 20.462 | 197.947 | 13.161 | 0.617 | 100.000 |
| dualtopo | post_covid | 23.107 | 494.300 | 22.762 | -0.630 | 100.000 |
| dualtopo_no_bg | post_covid | 23.736 | 506.956 | 23.401 | -0.506 | 100.000 |
| gnn_corrbinary | post_covid | 26.488 | 211.961 | 15.896 | 0.616 | 90.476 |
| gnn_uniform | post_covid | 29.407 | 227.795 | 17.259 | 0.601 | 85.714 |
| gnn_multiedge_season_level | post_covid | 35.166 | 316.920 | 21.952 | 0.594 | 76.190 |
| gnn_geo | post_covid | 42.642 | 369.913 | 26.176 | 0.599 | 76.190 |
| gnn_multiedge_level | post_covid | 48.044 | 363.090 | 27.606 | 0.598 | 76.190 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 15.304 | 77.973 | 9.484 | 0.666 | 97.826 |
| lstm | post_covid | 15.598 | 89.346 | 9.450 | 0.649 | 95.652 |
| arima | post_covid | 16.840 | 130.844 | 10.873 | 0.585 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 17.325 | 94.650 | 11.164 | 0.660 | 91.304 |
| lstm | exclude_covid | 18.148 | 82.126 | 10.214 | 0.629 | 91.304 |
| persistence | exclude_covid | 18.705 | 79.483 | 10.889 | 0.574 | 93.478 |
| persistence | post_covid | 18.705 | 79.483 | 10.889 | 0.574 | 95.652 |
| gnn_multiedge_leaknorm | post_covid | 19.581 | 107.340 | 12.046 | 0.699 | 97.826 |
| gnn_multiedge_full | full | 20.657 | 97.666 | 12.793 | 0.637 | 93.478 |
| gnn_multiedge | post_covid | 20.775 | 125.365 | 13.831 | 0.680 | 97.826 |
| dualtopo | post_covid | 21.121 | 256.170 | 16.098 | -0.222 | 91.304 |
| dualtopo_no_bg | post_covid | 21.273 | 263.453 | 16.447 | -0.158 | 91.304 |
| gnn_multiedge_rt | post_covid | 21.341 | 107.793 | 13.457 | 0.649 | 93.478 |
| gnn_multiedge_season | post_covid | 22.532 | 118.428 | 14.933 | 0.658 | 97.826 |
| dualtopo_fullhistory | full | 22.933 | 84.548 | 12.700 | 0.138 | 89.130 |
| gnn_corrbinary | post_covid | 24.543 | 135.111 | 16.706 | 0.629 | 97.826 |
| gnn_uniform | post_covid | 27.294 | 135.332 | 17.684 | 0.600 | 93.478 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| gnn_multiedge_season_level | post_covid | 34.614 | 201.294 | 24.363 | 0.522 | 60.870 |
| gnn_geo | post_covid | 36.423 | 225.064 | 24.469 | 0.500 | 78.261 |
| gnn_multiedge_level | post_covid | 40.397 | 215.856 | 27.192 | 0.445 | 63.043 |
| arima | exclude_covid | 136.748 | 319.274 | 50.229 | 0.367 | 65.217 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 19.925 | 78.658 | 13.632 | 0.610 | 96.000 |
| lstm | post_covid | 20.555 | 75.135 | 13.480 | 0.562 | 92.000 |
| arima | post_covid | 21.682 | 86.465 | 14.270 | 0.501 | 96.000 |
| gnn_multiedge | post_covid | 22.339 | 100.622 | 15.616 | 0.680 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 22.421 | 102.796 | 16.241 | 0.583 | 84.000 |
| gnn_multiedge_leaknorm | post_covid | 22.926 | 86.116 | 14.233 | 0.675 | 96.000 |
| lstm | exclude_covid | 23.667 | 67.420 | 14.253 | 0.558 | 84.000 |
| dualtopo_no_bg | post_covid | 24.296 | 114.233 | 16.524 | 0.088 | 84.000 |
| dualtopo | post_covid | 24.338 | 110.822 | 16.317 | 0.032 | 84.000 |
| gnn_corrbinary | post_covid | 24.775 | 118.362 | 18.869 | 0.649 | 96.000 |
| persistence | post_covid | 24.842 | 90.586 | 16.808 | 0.479 | 92.000 |
| persistence | exclude_covid | 24.842 | 90.586 | 16.808 | 0.479 | 88.000 |
| gnn_multiedge_full | full | 25.645 | 97.213 | 16.923 | 0.575 | 92.000 |
| gnn_multiedge_rt | post_covid | 25.849 | 100.511 | 17.160 | 0.598 | 88.000 |
| gnn_multiedge_season | post_covid | 26.957 | 113.391 | 19.306 | 0.608 | 96.000 |
| gnn_uniform | post_covid | 27.807 | 109.096 | 19.650 | 0.620 | 96.000 |
| dualtopo_fullhistory | full | 30.902 | 106.853 | 20.843 | -0.103 | 84.000 |
| gnn_geo | post_covid | 34.803 | 173.418 | 25.478 | 0.526 | 80.000 |
| gnn_multiedge_season_level | post_covid | 39.482 | 199.970 | 31.033 | 0.429 | 48.000 |
| gnn_multiedge_level | post_covid | 41.414 | 203.711 | 31.762 | 0.393 | 52.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| arima | exclude_covid | 185.389 | 523.801 | 88.180 | 0.267 | 52.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.901 | 57.996 | 3.006 | 0.642 | 95.238 |
| lstm | post_covid | 5.477 | 106.262 | 4.652 | 0.621 | 100.000 |
| persistence | exclude_covid | 5.633 | 66.266 | 3.843 | 0.592 | 100.000 |
| persistence | post_covid | 5.633 | 66.266 | 3.843 | 0.592 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.358 | 77.158 | 4.546 | 0.566 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| arima | exclude_covid | 6.826 | 75.790 | 5.048 | 0.421 | 80.952 |
| lstm | exclude_covid | 7.390 | 99.634 | 5.407 | 0.614 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.684 | 84.953 | 5.120 | 0.601 | 100.000 |
| arima | post_covid | 7.843 | 183.675 | 6.828 | 0.544 | 100.000 |
| gnn_multiedge_full | full | 12.319 | 98.205 | 7.875 | 0.672 | 95.238 |
| gnn_multiedge_rt | post_covid | 14.218 | 116.463 | 9.049 | 0.694 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 14.634 | 132.606 | 9.442 | 0.665 | 100.000 |
| gnn_multiedge_season | post_covid | 15.718 | 124.424 | 9.726 | 0.688 | 100.000 |
| dualtopo | post_covid | 16.491 | 429.202 | 15.837 | -0.634 | 100.000 |
| dualtopo_no_bg | post_covid | 16.988 | 441.096 | 16.355 | -0.683 | 100.000 |
| gnn_multiedge | post_covid | 18.742 | 154.822 | 11.706 | 0.685 | 100.000 |
| gnn_corrbinary | post_covid | 24.264 | 155.050 | 14.130 | 0.698 | 100.000 |
| gnn_uniform | post_covid | 26.671 | 166.565 | 15.344 | 0.694 | 90.476 |
| gnn_multiedge_season_level | post_covid | 27.725 | 202.871 | 16.422 | 0.707 | 76.190 |
| gnn_geo | post_covid | 38.262 | 286.546 | 23.268 | 0.718 | 76.190 |
| gnn_multiedge_level | post_covid | 39.150 | 230.313 | 21.752 | 0.707 | 76.190 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 12.822 | 73.746 | 7.546 | 0.711 | 95.918 |
| gnn_multiedge_covid_rsv | post_covid | 13.317 | 67.030 | 7.713 | 0.688 | 97.959 |
| lstm | exclude_covid | 13.597 | 59.265 | 7.785 | 0.682 | 91.837 |
| arima | post_covid | 14.080 | 104.047 | 9.011 | 0.638 | 95.918 |
| arima | exclude_covid | 14.135 | 85.932 | 8.336 | 0.634 | 95.918 |
| gnn_multiedge_covid_rsv_full | full | 14.258 | 77.311 | 8.791 | 0.702 | 93.878 |
| gnn_multiedge_leaknorm | post_covid | 14.463 | 98.013 | 9.613 | 0.762 | 97.959 |
| gnn_multiedge_full | full | 14.561 | 84.628 | 9.528 | 0.729 | 95.918 |
| gnn_multiedge_rt | post_covid | 15.292 | 95.705 | 10.325 | 0.734 | 95.918 |
| gnn_multiedge | post_covid | 15.359 | 107.194 | 10.244 | 0.733 | 100.000 |
| persistence | post_covid | 15.661 | 71.255 | 8.759 | 0.628 | 95.918 |
| persistence | exclude_covid | 15.661 | 71.255 | 8.759 | 0.628 | 93.878 |
| gnn_multiedge_season | post_covid | 15.722 | 98.034 | 10.804 | 0.740 | 100.000 |
| gnn_corrbinary | post_covid | 17.608 | 114.300 | 11.554 | 0.687 | 100.000 |
| dualtopo_fullhistory | full | 17.939 | 57.493 | 9.811 | 0.376 | 89.796 |
| dualtopo | post_covid | 18.276 | 191.757 | 12.884 | -0.342 | 89.796 |
| dualtopo_no_bg | post_covid | 18.321 | 196.876 | 13.100 | -0.316 | 89.796 |
| gnn_uniform | post_covid | 19.308 | 116.991 | 12.487 | 0.671 | 100.000 |
| gnn_multiedge_season_level | post_covid | 20.661 | 142.468 | 14.180 | 0.640 | 87.755 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| gnn_geo | post_covid | 24.754 | 176.462 | 15.957 | 0.567 | 85.714 |
| gnn_multiedge_level | post_covid | 24.889 | 158.880 | 15.875 | 0.547 | 81.633 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge | post_covid | 16.846 | 74.451 | 12.077 | 0.722 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 16.856 | 68.738 | 11.860 | 0.738 | 96.154 |
| lstm | post_covid | 17.190 | 52.293 | 11.352 | 0.640 | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 17.789 | 61.196 | 11.589 | 0.599 | 96.154 |
| gnn_corrbinary | post_covid | 17.983 | 77.985 | 13.080 | 0.701 | 100.000 |
| gnn_multiedge_full | full | 18.209 | 72.139 | 12.926 | 0.671 | 92.308 |
| arima | post_covid | 18.290 | 62.609 | 12.207 | 0.552 | 92.308 |
| lstm | exclude_covid | 18.366 | 52.636 | 12.235 | 0.608 | 84.615 |
| gnn_multiedge_rt | post_covid | 18.458 | 77.623 | 13.591 | 0.690 | 92.308 |
| gnn_multiedge_season | post_covid | 18.785 | 81.442 | 14.179 | 0.697 | 100.000 |
| arima | exclude_covid | 18.875 | 62.115 | 12.265 | 0.530 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 18.902 | 76.269 | 13.131 | 0.611 | 88.462 |
| gnn_uniform | post_covid | 19.866 | 78.069 | 14.221 | 0.688 | 100.000 |
| persistence | exclude_covid | 21.138 | 71.836 | 13.665 | 0.521 | 88.462 |
| persistence | post_covid | 21.138 | 71.836 | 13.665 | 0.521 | 92.308 |
| dualtopo_no_bg | post_covid | 22.181 | 73.422 | 14.125 | 0.004 | 80.769 |
| dualtopo | post_covid | 22.284 | 71.488 | 14.041 | -0.125 | 80.769 |
| gnn_multiedge_season_level | post_covid | 22.438 | 104.958 | 17.229 | 0.608 | 88.462 |
| gnn_geo | post_covid | 23.260 | 108.397 | 16.517 | 0.606 | 92.308 |
| gnn_multiedge_level | post_covid | 24.041 | 106.780 | 17.543 | 0.562 | 84.615 |
| dualtopo_fullhistory | full | 24.452 | 66.779 | 16.248 | 0.150 | 80.769 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.120 | 46.996 | 2.535 | 0.704 | 100.000 |
| lstm | exclude_covid | 3.543 | 66.759 | 2.754 | 0.740 | 100.000 |
| lstm | post_covid | 4.027 | 97.996 | 3.243 | 0.719 | 100.000 |
| persistence | exclude_covid | 4.175 | 70.597 | 3.213 | 0.719 | 100.000 |
| persistence | post_covid | 4.175 | 70.597 | 3.213 | 0.719 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.482 | 73.625 | 3.332 | 0.754 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| arima | exclude_covid | 4.785 | 112.856 | 3.896 | 0.729 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.405 | 78.489 | 3.885 | 0.765 | 100.000 |
| arima | post_covid | 6.648 | 150.890 | 5.398 | 0.516 | 100.000 |
| gnn_multiedge_full | full | 8.769 | 98.746 | 5.688 | 0.715 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.633 | 116.144 | 6.634 | 0.695 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.156 | 131.107 | 7.073 | 0.710 | 100.000 |
| gnn_multiedge_season | post_covid | 11.303 | 116.789 | 6.989 | 0.723 | 100.000 |
| dualtopo | post_covid | 12.259 | 327.714 | 11.575 | -0.656 | 100.000 |
| dualtopo_no_bg | post_covid | 12.605 | 336.432 | 11.941 | -0.829 | 100.000 |
| gnn_multiedge | post_covid | 13.482 | 144.208 | 8.172 | 0.692 | 100.000 |
| gnn_corrbinary | post_covid | 17.174 | 155.352 | 9.829 | 0.673 | 100.000 |
| gnn_multiedge_season_level | post_covid | 18.447 | 184.870 | 10.733 | 0.638 | 86.957 |
| gnn_uniform | post_covid | 18.658 | 160.989 | 10.527 | 0.685 | 100.000 |
| gnn_multiedge_level | post_covid | 25.815 | 217.776 | 13.989 | 0.629 | 78.261 |
| gnn_geo | post_covid | 26.341 | 253.405 | 15.325 | 0.670 | 78.261 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 15.888 | 57.571 | 8.707 | 0.607 | 92.500 |
| lstm | exclude_covid | 16.609 | 62.730 | 8.965 | 0.553 | 90.000 |
| arima | exclude_covid | 17.955 | 101.543 | 10.435 | 0.408 | 92.500 |
| gnn_multiedge_covid_rsv | post_covid | 18.621 | 97.692 | 11.232 | 0.450 | 92.500 |
| arima | post_covid | 18.723 | 103.324 | 10.730 | 0.405 | 92.500 |
| gnn_multiedge_covid_rsv_full | full | 18.973 | 105.920 | 11.664 | 0.505 | 90.000 |
| dualtopo_no_bg | post_covid | 19.291 | 113.320 | 10.968 | 0.039 | 92.500 |
| dualtopo | post_covid | 19.306 | 109.436 | 10.765 | -0.248 | 92.500 |
| gnn_multiedge_leaknorm | post_covid | 19.774 | 132.387 | 13.281 | 0.552 | 92.500 |
| gnn_multiedge | post_covid | 19.821 | 142.370 | 14.269 | 0.540 | 95.000 |
| gnn_multiedge_rt | post_covid | 20.564 | 129.730 | 14.047 | 0.521 | 95.000 |
| dualtopo_fullhistory | full | 20.616 | 59.720 | 10.425 | 0.117 | 90.000 |
| persistence | exclude_covid | 20.649 | 97.450 | 12.092 | 0.426 | 90.000 |
| persistence | post_covid | 20.649 | 97.450 | 12.092 | 0.426 | 90.000 |
| gnn_multiedge_full | full | 21.008 | 126.718 | 13.754 | 0.490 | 92.500 |
| gnn_multiedge_season | post_covid | 21.184 | 138.216 | 14.805 | 0.534 | 95.000 |
| gnn_corrbinary | post_covid | 21.377 | 155.776 | 15.930 | 0.524 | 92.500 |
| gnn_multiedge_season_level | post_covid | 21.423 | 143.454 | 14.902 | 0.500 | 82.500 |
| gnn_uniform | post_covid | 21.808 | 150.234 | 15.208 | 0.523 | 92.500 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| gnn_multiedge_level | post_covid | 24.848 | 163.367 | 16.941 | 0.425 | 75.000 |
| gnn_geo | post_covid | 25.466 | 193.337 | 18.020 | 0.466 | 85.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 19.866 | 56.676 | 11.920 | 0.563 | 88.000 |
| lstm | exclude_covid | 20.723 | 65.012 | 12.216 | 0.502 | 84.000 |
| arima | exclude_covid | 22.146 | 86.593 | 13.204 | 0.352 | 88.000 |
| gnn_multiedge | post_covid | 22.826 | 126.167 | 16.658 | 0.524 | 92.000 |
| gnn_multiedge_covid_rsv | post_covid | 22.980 | 96.396 | 14.512 | 0.405 | 88.000 |
| arima | post_covid | 23.126 | 90.555 | 13.524 | 0.358 | 88.000 |
| gnn_multiedge_season_level | post_covid | 23.219 | 129.363 | 17.056 | 0.500 | 80.000 |
| gnn_multiedge_leaknorm | post_covid | 23.284 | 118.230 | 15.695 | 0.531 | 88.000 |
| gnn_multiedge_covid_rsv_full | full | 23.343 | 106.185 | 15.040 | 0.455 | 84.000 |
| dualtopo_no_bg | post_covid | 23.473 | 79.098 | 12.906 | 0.162 | 88.000 |
| dualtopo | post_covid | 23.557 | 76.517 | 12.784 | -0.157 | 88.000 |
| gnn_uniform | post_covid | 23.626 | 118.945 | 16.569 | 0.543 | 88.000 |
| gnn_corrbinary | post_covid | 23.764 | 136.063 | 18.263 | 0.522 | 88.000 |
| gnn_multiedge_level | post_covid | 24.471 | 131.475 | 17.992 | 0.469 | 76.000 |
| gnn_multiedge_rt | post_covid | 24.682 | 123.022 | 17.349 | 0.486 | 92.000 |
| gnn_multiedge_season | post_covid | 25.203 | 130.864 | 18.145 | 0.500 | 92.000 |
| gnn_multiedge_full | full | 25.412 | 125.502 | 17.227 | 0.448 | 88.000 |
| persistence | exclude_covid | 25.686 | 103.436 | 16.132 | 0.370 | 84.000 |
| persistence | post_covid | 25.686 | 103.436 | 16.132 | 0.370 | 84.000 |
| gnn_geo | post_covid | 25.768 | 144.321 | 18.722 | 0.506 | 88.000 |
| dualtopo_fullhistory | full | 25.870 | 64.893 | 14.644 | -0.021 | 84.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.916 | 59.062 | 3.352 | 0.323 | 100.000 |
| dualtopo_fullhistory | full | 4.248 | 51.100 | 3.394 | 0.265 | 100.000 |
| lstm | exclude_covid | 4.457 | 58.928 | 3.547 | 0.320 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| persistence | exclude_covid | 6.116 | 87.474 | 5.360 | -0.052 | 100.000 |
| persistence | post_covid | 6.116 | 87.474 | 5.360 | -0.052 | 100.000 |
| arima | exclude_covid | 6.500 | 126.460 | 5.820 | -0.266 | 100.000 |
| arima | post_covid | 6.591 | 124.606 | 6.072 | -0.292 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.668 | 99.852 | 5.765 | -0.153 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.196 | 105.478 | 6.037 | -0.064 | 100.000 |
| dualtopo | post_covid | 8.308 | 164.300 | 7.399 | -0.254 | 100.000 |
| dualtopo_no_bg | post_covid | 8.610 | 170.355 | 7.738 | -0.204 | 100.000 |
| gnn_multiedge_full | full | 10.031 | 128.746 | 7.965 | 0.119 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.597 | 140.909 | 8.543 | 0.134 | 100.000 |
| gnn_multiedge_season | post_covid | 11.750 | 150.470 | 9.237 | 0.170 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.795 | 155.983 | 9.259 | 0.122 | 100.000 |
| gnn_multiedge | post_covid | 13.388 | 169.375 | 10.288 | 0.173 | 100.000 |
| gnn_corrbinary | post_covid | 16.656 | 188.632 | 12.041 | 0.209 | 100.000 |
| gnn_multiedge_season_level | post_covid | 18.038 | 166.941 | 11.311 | 0.309 | 86.667 |
| gnn_uniform | post_covid | 18.384 | 202.381 | 12.940 | 0.210 | 100.000 |
| gnn_geo | post_covid | 24.953 | 275.031 | 16.849 | 0.234 | 80.000 |
| gnn_multiedge_level | post_covid | 25.464 | 216.521 | 15.188 | 0.311 | 73.333 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 8.736 | 60.064 | 5.635 | 0.758 | 97.619 |
| arima | post_covid | 8.748 | 93.421 | 5.835 | 0.752 | 100.000 |
| arima | exclude_covid | 8.925 | 91.313 | 5.956 | 0.738 | 100.000 |
| lstm | post_covid | 9.936 | 57.083 | 5.888 | 0.682 | 97.619 |
| gnn_multiedge_covid_rsv_full | full | 10.011 | 69.795 | 6.291 | 0.744 | 95.238 |
| persistence | exclude_covid | 10.284 | 53.790 | 5.874 | 0.702 | 95.238 |
| persistence | post_covid | 10.284 | 53.790 | 5.874 | 0.702 | 95.238 |
| gnn_multiedge_leaknorm | post_covid | 10.445 | 95.087 | 7.100 | 0.793 | 100.000 |
| gnn_multiedge | post_covid | 11.015 | 104.130 | 7.711 | 0.761 | 100.000 |
| gnn_multiedge_rt | post_covid | 11.398 | 90.001 | 7.848 | 0.747 | 100.000 |
| gnn_multiedge_full | full | 11.743 | 82.841 | 7.572 | 0.726 | 95.238 |
| gnn_multiedge_season | post_covid | 11.898 | 93.623 | 8.533 | 0.756 | 97.619 |
| lstm | exclude_covid | 12.025 | 72.518 | 6.881 | 0.674 | 92.857 |
| dualtopo | post_covid | 13.216 | 184.262 | 9.413 | -0.347 | 90.476 |
| dualtopo_no_bg | post_covid | 13.241 | 190.194 | 9.571 | -0.224 | 90.476 |
| gnn_corrbinary | post_covid | 13.403 | 114.178 | 9.261 | 0.700 | 100.000 |
| dualtopo_fullhistory | full | 14.159 | 67.096 | 8.150 | 0.215 | 88.095 |
| gnn_uniform | post_covid | 14.698 | 116.318 | 9.900 | 0.681 | 97.619 |
| gnn_multiedge_season_level | post_covid | 17.413 | 150.662 | 12.448 | 0.603 | 95.238 |
| gnn_geo | post_covid | 20.055 | 187.286 | 13.610 | 0.587 | 95.238 |
| gnn_multiedge_level | post_covid | 20.711 | 169.185 | 13.843 | 0.504 | 78.571 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 10.658 | 74.222 | 7.146 | 0.718 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.685 | 57.029 | 7.631 | 0.732 | 96.000 |
| arima | exclude_covid | 10.932 | 74.317 | 7.476 | 0.694 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.953 | 72.418 | 8.023 | 0.813 | 100.000 |
| gnn_multiedge | post_covid | 11.133 | 80.345 | 8.596 | 0.788 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 12.262 | 71.578 | 8.614 | 0.700 | 92.000 |
| lstm | post_covid | 12.640 | 61.061 | 8.424 | 0.618 | 96.000 |
| persistence | exclude_covid | 12.941 | 55.862 | 8.264 | 0.644 | 92.000 |
| persistence | post_covid | 12.941 | 55.862 | 8.264 | 0.644 | 92.000 |
| gnn_multiedge_rt | post_covid | 13.051 | 78.220 | 9.762 | 0.730 | 100.000 |
| gnn_corrbinary | post_covid | 13.210 | 85.816 | 10.301 | 0.738 | 100.000 |
| gnn_multiedge_season | post_covid | 13.497 | 83.523 | 10.768 | 0.742 | 96.000 |
| gnn_multiedge_full | full | 13.645 | 73.122 | 9.565 | 0.702 | 92.000 |
| gnn_uniform | post_covid | 14.331 | 82.928 | 10.885 | 0.729 | 96.000 |
| lstm | exclude_covid | 15.314 | 76.434 | 9.910 | 0.618 | 88.000 |
| dualtopo_no_bg | post_covid | 15.519 | 138.903 | 10.364 | 0.045 | 84.000 |
| dualtopo | post_covid | 15.603 | 135.150 | 10.325 | -0.199 | 84.000 |
| dualtopo_fullhistory | full | 18.150 | 71.778 | 11.906 | 0.033 | 80.000 |
| gnn_multiedge_season_level | post_covid | 18.627 | 132.086 | 14.951 | 0.582 | 100.000 |
| gnn_geo | post_covid | 19.284 | 135.956 | 14.485 | 0.637 | 100.000 |
| gnn_multiedge_level | post_covid | 20.113 | 128.315 | 15.150 | 0.521 | 80.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 2.993 | 51.234 | 2.158 | 0.454 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| dualtopo_fullhistory | full | 3.301 | 60.210 | 2.628 | 0.372 | 100.000 |
| lstm | exclude_covid | 3.523 | 66.759 | 2.427 | 0.458 | 100.000 |
| persistence | exclude_covid | 3.874 | 50.743 | 2.359 | 0.321 | 100.000 |
| persistence | post_covid | 3.874 | 50.743 | 2.359 | 0.321 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.548 | 64.527 | 2.700 | 0.200 | 100.000 |
| arima | exclude_covid | 4.590 | 116.306 | 3.721 | 0.333 | 100.000 |
| arima | post_covid | 4.694 | 121.656 | 3.906 | 0.268 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.147 | 67.174 | 2.876 | 0.311 | 100.000 |
| gnn_multiedge_full | full | 8.177 | 97.132 | 4.641 | 0.341 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.395 | 107.326 | 5.034 | 0.363 | 100.000 |
| dualtopo | post_covid | 8.574 | 256.487 | 8.072 | -0.411 | 100.000 |
| dualtopo_no_bg | post_covid | 8.886 | 265.623 | 8.404 | -0.488 | 100.000 |
| gnn_multiedge_season | post_covid | 9.047 | 108.475 | 5.245 | 0.402 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 9.649 | 128.422 | 5.743 | 0.328 | 100.000 |
| gnn_multiedge | post_covid | 10.839 | 139.107 | 6.408 | 0.362 | 100.000 |
| gnn_corrbinary | post_covid | 13.681 | 155.888 | 7.733 | 0.376 | 100.000 |
| gnn_uniform | post_covid | 15.221 | 165.420 | 8.451 | 0.393 | 100.000 |
| gnn_multiedge_season_level | post_covid | 15.454 | 177.981 | 8.766 | 0.400 | 88.235 |
| gnn_geo | post_covid | 21.138 | 262.771 | 12.322 | 0.384 | 88.235 |
| gnn_multiedge_level | post_covid | 21.560 | 229.287 | 11.921 | 0.396 | 76.471 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 9.341 | 90.803 | 5.590 | 0.670 | 97.826 |
| arima | post_covid | 9.405 | 100.631 | 5.789 | 0.659 | 97.826 |
| lstm | post_covid | 9.457 | 86.323 | 6.079 | 0.694 | 97.826 |
| gnn_multiedge_covid_rsv | post_covid | 9.609 | 66.228 | 6.038 | 0.655 | 97.826 |
| lstm | exclude_covid | 9.726 | 75.295 | 6.249 | 0.707 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 9.765 | 73.498 | 6.152 | 0.713 | 97.826 |
| gnn_multiedge_full | full | 9.982 | 76.049 | 6.746 | 0.751 | 97.826 |
| persistence | exclude_covid | 10.448 | 58.464 | 5.574 | 0.650 | 97.826 |
| persistence | post_covid | 10.448 | 58.464 | 5.574 | 0.650 | 97.826 |
| gnn_multiedge_leaknorm | post_covid | 10.625 | 93.767 | 7.335 | 0.736 | 97.826 |
| gnn_multiedge_rt | post_covid | 10.648 | 88.220 | 7.332 | 0.735 | 97.826 |
| gnn_multiedge_season | post_covid | 11.765 | 95.612 | 8.254 | 0.724 | 97.826 |
| gnn_multiedge | post_covid | 11.787 | 106.459 | 8.275 | 0.694 | 97.826 |
| dualtopo_fullhistory | full | 12.291 | 59.757 | 7.057 | 0.388 | 91.304 |
| dualtopo | post_covid | 12.448 | 189.389 | 8.441 | -0.450 | 93.478 |
| dualtopo_no_bg | post_covid | 12.452 | 195.019 | 8.552 | -0.135 | 93.478 |
| gnn_corrbinary | post_covid | 13.894 | 112.379 | 9.512 | 0.649 | 97.826 |
| gnn_uniform | post_covid | 14.733 | 115.814 | 10.023 | 0.626 | 97.826 |
| gnn_multiedge_season_level | post_covid | 15.463 | 128.992 | 10.801 | 0.632 | 93.478 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| gnn_multiedge_level | post_covid | 19.212 | 146.945 | 12.640 | 0.531 | 82.609 |
| gnn_geo | post_covid | 19.304 | 188.510 | 12.982 | 0.513 | 93.478 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_full | full | 11.851 | 68.999 | 8.638 | 0.690 | 96.154 |
| arima | exclude_covid | 11.924 | 56.713 | 7.154 | 0.569 | 96.154 |
| arima | post_covid | 11.930 | 59.914 | 7.244 | 0.558 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 12.210 | 70.380 | 8.826 | 0.689 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 12.243 | 58.841 | 8.326 | 0.545 | 96.154 |
| lstm | post_covid | 12.245 | 56.388 | 8.475 | 0.634 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 12.341 | 70.777 | 8.360 | 0.618 | 96.154 |
| gnn_multiedge_rt | post_covid | 12.552 | 76.360 | 9.187 | 0.673 | 96.154 |
| lstm | exclude_covid | 12.600 | 57.731 | 8.845 | 0.652 | 96.154 |
| gnn_multiedge | post_covid | 13.094 | 81.003 | 9.681 | 0.641 | 96.154 |
| persistence | post_covid | 13.538 | 60.255 | 7.950 | 0.536 | 96.154 |
| persistence | exclude_covid | 13.538 | 60.255 | 7.950 | 0.536 | 96.154 |
| gnn_multiedge_season | post_covid | 13.853 | 85.867 | 10.574 | 0.656 | 96.154 |
| dualtopo_no_bg | post_covid | 14.833 | 80.428 | 9.180 | 0.094 | 88.462 |
| gnn_corrbinary | post_covid | 14.855 | 91.299 | 10.970 | 0.600 | 96.154 |
| dualtopo | post_covid | 14.944 | 78.749 | 9.214 | -0.261 | 88.462 |
| gnn_uniform | post_covid | 15.160 | 88.207 | 11.267 | 0.609 | 96.154 |
| dualtopo_fullhistory | full | 16.189 | 68.118 | 10.999 | 0.163 | 84.615 |
| gnn_multiedge_season_level | post_covid | 16.457 | 105.867 | 12.755 | 0.579 | 92.308 |
| gnn_multiedge_level | post_covid | 18.482 | 115.181 | 13.747 | 0.509 | 88.462 |
| gnn_geo | post_covid | 18.862 | 123.663 | 13.266 | 0.487 | 96.154 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.596 | 48.888 | 1.932 | 0.662 | 100.000 |
| lstm | post_covid | 3.283 | 125.238 | 2.964 | 0.532 | 100.000 |
| lstm | exclude_covid | 3.345 | 98.128 | 2.874 | 0.545 | 100.000 |
| persistence | exclude_covid | 3.577 | 56.135 | 2.485 | 0.548 | 100.000 |
| persistence | post_covid | 3.577 | 56.135 | 2.485 | 0.548 | 100.000 |
| arima | exclude_covid | 3.982 | 135.120 | 3.558 | 0.520 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.183 | 75.831 | 3.063 | 0.434 | 100.000 |
| arima | post_covid | 4.292 | 153.564 | 3.897 | 0.477 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.618 | 77.035 | 3.280 | 0.483 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| gnn_multiedge_full | full | 6.824 | 85.213 | 4.287 | 0.662 | 100.000 |
| gnn_multiedge_rt | post_covid | 7.481 | 103.638 | 4.921 | 0.679 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 8.113 | 124.170 | 5.396 | 0.636 | 100.000 |
| dualtopo | post_covid | 8.128 | 333.222 | 7.437 | -0.682 | 100.000 |
| gnn_multiedge_season | post_covid | 8.300 | 108.281 | 5.238 | 0.673 | 100.000 |
| dualtopo_no_bg | post_covid | 8.401 | 343.988 | 7.736 | -0.202 | 100.000 |
| gnn_multiedge | post_covid | 9.831 | 139.551 | 6.447 | 0.675 | 100.000 |
| gnn_corrbinary | post_covid | 12.536 | 139.783 | 7.615 | 0.697 | 100.000 |
| gnn_multiedge_season_level | post_covid | 14.065 | 159.054 | 8.261 | 0.733 | 95.000 |
| gnn_uniform | post_covid | 14.157 | 151.704 | 8.406 | 0.692 | 100.000 |
| gnn_geo | post_covid | 19.864 | 272.811 | 12.612 | 0.708 | 90.000 |
| gnn_multiedge_level | post_covid | 20.121 | 188.237 | 11.201 | 0.730 | 75.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 9.381 | 83.037 | 6.178 | 0.711 | 95.455 |
| dualtopo_fullhistory | full | 9.794 | 88.279 | 6.169 | 0.669 | 93.182 |
| gnn_multiedge_covid_rsv | post_covid | 9.832 | 100.526 | 6.149 | 0.660 | 97.727 |
| arima | post_covid | 10.057 | 136.185 | 7.339 | 0.633 | 97.727 |
| lstm | exclude_covid | 10.387 | 75.621 | 6.393 | 0.685 | 95.455 |
| gnn_multiedge_covid_rsv_full | full | 10.652 | 105.197 | 7.456 | 0.677 | 93.182 |
| arima | exclude_covid | 11.037 | 113.343 | 7.423 | 0.619 | 95.455 |
| persistence | exclude_covid | 11.313 | 93.912 | 7.400 | 0.619 | 93.182 |
| persistence | post_covid | 11.313 | 93.912 | 7.400 | 0.619 | 95.455 |
| gnn_multiedge_leaknorm | post_covid | 11.656 | 149.403 | 8.569 | 0.708 | 100.000 |
| gnn_multiedge_full | full | 12.090 | 128.143 | 8.707 | 0.663 | 95.455 |
| gnn_multiedge | post_covid | 12.724 | 170.423 | 9.523 | 0.669 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.837 | 139.639 | 9.376 | 0.662 | 97.727 |
| dualtopo | post_covid | 12.982 | 210.822 | 9.416 | -0.284 | 90.909 |
| dualtopo_no_bg | post_covid | 13.012 | 216.795 | 9.528 | 0.013 | 90.909 |
| gnn_multiedge_season | post_covid | 13.688 | 158.266 | 9.967 | 0.666 | 100.000 |
| gnn_corrbinary | post_covid | 15.203 | 189.562 | 11.145 | 0.611 | 100.000 |
| gnn_uniform | post_covid | 16.157 | 186.323 | 11.287 | 0.599 | 97.727 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| gnn_multiedge_season_level | post_covid | 18.618 | 215.962 | 13.587 | 0.567 | 86.364 |
| gnn_multiedge_level | post_covid | 22.646 | 244.524 | 15.570 | 0.463 | 79.545 |
| gnn_geo | post_covid | 23.967 | 276.815 | 16.952 | 0.501 | 93.182 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 12.199 | 82.443 | 9.117 | 0.653 | 92.000 |
| dualtopo_fullhistory | full | 12.753 | 93.142 | 9.060 | 0.562 | 88.000 |
| arima | post_covid | 12.760 | 133.236 | 9.831 | 0.545 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 12.874 | 131.420 | 9.376 | 0.559 | 96.000 |
| lstm | exclude_covid | 13.524 | 84.044 | 9.674 | 0.623 | 92.000 |
| gnn_multiedge_covid_rsv_full | full | 13.914 | 140.960 | 11.468 | 0.581 | 88.000 |
| gnn_multiedge_leaknorm | post_covid | 13.993 | 175.711 | 11.003 | 0.650 | 100.000 |
| arima | exclude_covid | 14.347 | 130.026 | 10.934 | 0.530 | 92.000 |
| gnn_multiedge | post_covid | 14.468 | 198.656 | 11.685 | 0.616 | 100.000 |
| persistence | exclude_covid | 14.820 | 127.042 | 11.532 | 0.515 | 88.000 |
| persistence | post_covid | 14.820 | 127.042 | 11.532 | 0.515 | 92.000 |
| gnn_multiedge_full | full | 15.268 | 166.403 | 12.305 | 0.576 | 92.000 |
| dualtopo_no_bg | post_covid | 15.385 | 135.951 | 10.325 | 0.243 | 84.000 |
| dualtopo | post_covid | 15.465 | 132.828 | 10.339 | -0.065 | 84.000 |
| gnn_multiedge_rt | post_covid | 15.779 | 169.767 | 12.683 | 0.584 | 96.000 |
| gnn_corrbinary | post_covid | 16.484 | 224.046 | 13.337 | 0.566 | 100.000 |
| gnn_multiedge_season | post_covid | 16.687 | 197.694 | 13.359 | 0.584 | 100.000 |
| gnn_uniform | post_covid | 17.053 | 214.495 | 13.036 | 0.581 | 96.000 |
| gnn_multiedge_season_level | post_covid | 20.375 | 248.255 | 16.609 | 0.498 | 88.000 |
| gnn_multiedge_level | post_covid | 22.506 | 269.707 | 17.533 | 0.420 | 84.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |
| gnn_geo | post_covid | 25.610 | 300.837 | 19.683 | 0.436 | 88.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 2.403 | 59.876 | 1.904 | 0.784 | 100.000 |
| persistence | exclude_covid | 2.721 | 50.321 | 1.963 | 0.753 | 100.000 |
| persistence | post_covid | 2.721 | 50.321 | 1.963 | 0.753 | 100.000 |
| lstm | post_covid | 2.822 | 83.819 | 2.312 | 0.700 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 2.830 | 58.140 | 2.176 | 0.801 | 100.000 |
| dualtopo_fullhistory | full | 2.854 | 81.880 | 2.366 | 0.585 | 100.000 |
| lstm | exclude_covid | 3.028 | 64.539 | 2.077 | 0.687 | 100.000 |
| arima | exclude_covid | 3.362 | 91.391 | 2.803 | 0.654 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| arima | post_covid | 4.470 | 140.065 | 4.061 | 0.637 | 100.000 |
| gnn_multiedge_full | full | 5.636 | 77.802 | 3.973 | 0.805 | 100.000 |
| gnn_multiedge_rt | post_covid | 7.348 | 99.996 | 5.023 | 0.797 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 7.548 | 114.788 | 5.366 | 0.796 | 100.000 |
| gnn_multiedge_season | post_covid | 8.215 | 106.388 | 5.503 | 0.805 | 100.000 |
| dualtopo | post_covid | 8.694 | 313.447 | 8.202 | -0.724 | 100.000 |
| dualtopo_no_bg | post_covid | 8.981 | 323.168 | 8.478 | -0.497 | 100.000 |
| gnn_multiedge | post_covid | 9.976 | 133.274 | 6.677 | 0.790 | 100.000 |
| gnn_corrbinary | post_covid | 13.331 | 144.189 | 8.261 | 0.770 | 100.000 |
| gnn_uniform | post_covid | 14.896 | 149.256 | 8.984 | 0.767 | 100.000 |
| gnn_multiedge_season_level | post_covid | 16.016 | 173.470 | 9.611 | 0.689 | 84.211 |
| gnn_geo | post_covid | 21.616 | 245.208 | 13.360 | 0.738 | 100.000 |
| gnn_multiedge_level | post_covid | 22.830 | 211.388 | 12.988 | 0.694 | 73.684 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 9.518 | 82.763 | 5.613 | 0.732 | 97.826 |
| gnn_multiedge_covid_rsv | post_covid | 10.062 | 90.265 | 6.427 | 0.693 | 95.652 |
| lstm | exclude_covid | 10.069 | 84.865 | 6.041 | 0.688 | 95.652 |
| gnn_multiedge_leaknorm | post_covid | 10.591 | 122.264 | 7.718 | 0.772 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 10.619 | 100.787 | 7.150 | 0.717 | 89.130 |
| arima | exclude_covid | 10.635 | 137.031 | 7.072 | 0.641 | 97.826 |
| arima | post_covid | 10.859 | 124.492 | 6.944 | 0.620 | 97.826 |
| gnn_multiedge | post_covid | 10.955 | 129.983 | 8.141 | 0.749 | 100.000 |
| gnn_multiedge_full | full | 11.268 | 109.629 | 8.020 | 0.728 | 100.000 |
| gnn_multiedge_rt | post_covid | 11.443 | 118.147 | 8.152 | 0.731 | 100.000 |
| gnn_multiedge_season | post_covid | 11.636 | 121.478 | 8.505 | 0.739 | 100.000 |
| persistence | post_covid | 11.661 | 92.158 | 7.198 | 0.643 | 95.652 |
| persistence | exclude_covid | 11.661 | 92.158 | 7.198 | 0.643 | 95.652 |
| gnn_corrbinary | post_covid | 12.884 | 138.435 | 9.369 | 0.698 | 100.000 |
| dualtopo | post_covid | 13.877 | 225.539 | 9.876 | -0.326 | 91.304 |
| gnn_uniform | post_covid | 13.905 | 137.476 | 9.851 | 0.683 | 100.000 |
| dualtopo_no_bg | post_covid | 13.911 | 231.331 | 10.024 | -0.220 | 91.304 |
| dualtopo_fullhistory | full | 13.992 | 79.383 | 7.551 | 0.224 | 89.130 |
| gnn_multiedge_season_level | post_covid | 15.946 | 179.487 | 11.761 | 0.586 | 91.304 |
| gnn_geo | post_covid | 17.394 | 200.184 | 12.139 | 0.592 | 100.000 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| gnn_multiedge_level | post_covid | 18.883 | 193.099 | 13.047 | 0.489 | 78.261 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge | post_covid | 12.628 | 113.227 | 10.175 | 0.736 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 12.798 | 106.095 | 9.988 | 0.750 | 100.000 |
| lstm | post_covid | 12.889 | 82.642 | 8.670 | 0.661 | 95.833 |
| lstm | exclude_covid | 13.543 | 89.449 | 9.311 | 0.611 | 91.667 |
| gnn_multiedge_covid_rsv | post_covid | 13.545 | 89.035 | 9.741 | 0.626 | 91.667 |
| arima | exclude_covid | 14.022 | 112.196 | 9.763 | 0.557 | 95.833 |
| gnn_multiedge_covid_rsv_full | full | 14.254 | 108.122 | 11.044 | 0.644 | 79.167 |
| gnn_corrbinary | post_covid | 14.273 | 123.384 | 11.461 | 0.690 | 100.000 |
| gnn_multiedge_full | full | 14.392 | 109.347 | 11.342 | 0.677 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.465 | 115.064 | 11.265 | 0.685 | 100.000 |
| arima | post_covid | 14.505 | 108.867 | 10.064 | 0.528 | 95.833 |
| gnn_multiedge_season | post_covid | 14.534 | 119.304 | 11.682 | 0.693 | 100.000 |
| gnn_uniform | post_covid | 15.208 | 116.359 | 11.905 | 0.685 | 100.000 |
| persistence | exclude_covid | 15.853 | 100.455 | 11.317 | 0.560 | 91.667 |
| persistence | post_covid | 15.853 | 100.455 | 11.317 | 0.560 | 91.667 |
| gnn_geo | post_covid | 16.938 | 154.657 | 13.109 | 0.629 | 100.000 |
| dualtopo_no_bg | post_covid | 17.174 | 139.153 | 11.216 | 0.026 | 83.333 |
| dualtopo | post_covid | 17.240 | 136.008 | 11.172 | -0.063 | 83.333 |
| gnn_multiedge_season_level | post_covid | 18.163 | 182.664 | 15.216 | 0.519 | 87.500 |
| dualtopo_fullhistory | full | 19.279 | 93.011 | 12.991 | -0.004 | 79.167 |
| gnn_multiedge_level | post_covid | 19.388 | 179.869 | 15.399 | 0.458 | 79.167 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 1.971 | 64.516 | 1.615 | 0.820 | 100.000 |
| lstm | post_covid | 2.858 | 82.895 | 2.278 | 0.719 | 100.000 |
| persistence | exclude_covid | 3.180 | 83.106 | 2.705 | 0.438 | 100.000 |
| persistence | post_covid | 3.180 | 83.106 | 2.705 | 0.438 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 3.395 | 91.606 | 2.811 | 0.403 | 100.000 |
| lstm | exclude_covid | 3.452 | 79.864 | 2.473 | 0.711 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.758 | 92.785 | 2.902 | 0.525 | 100.000 |
| arima | post_covid | 4.128 | 141.538 | 3.542 | 0.466 | 100.000 |
| arima | exclude_covid | 4.688 | 164.124 | 4.135 | 0.411 | 100.000 |
| gnn_multiedge_full | full | 6.286 | 109.935 | 4.396 | 0.607 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.747 | 121.511 | 4.756 | 0.625 | 100.000 |
| gnn_multiedge_season | post_covid | 7.258 | 123.849 | 5.039 | 0.665 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 7.475 | 139.903 | 5.241 | 0.614 | 100.000 |
| gnn_multiedge | post_covid | 8.774 | 148.262 | 5.921 | 0.649 | 100.000 |
| dualtopo | post_covid | 8.854 | 323.210 | 8.462 | -0.753 | 100.000 |
| dualtopo_no_bg | post_covid | 9.103 | 331.889 | 8.724 | -0.518 | 100.000 |
| gnn_corrbinary | post_covid | 11.174 | 154.855 | 7.086 | 0.679 | 100.000 |
| gnn_uniform | post_covid | 12.327 | 160.513 | 7.611 | 0.693 | 100.000 |
| gnn_multiedge_season_level | post_covid | 13.108 | 176.022 | 7.991 | 0.745 | 95.455 |
| gnn_geo | post_covid | 17.879 | 249.850 | 11.081 | 0.703 | 100.000 |
| gnn_multiedge_level | post_covid | 18.317 | 207.533 | 10.483 | 0.739 | 77.273 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 4.065 | 82.597 | 2.845 | 0.665 | 100.000 |
| arima | post_covid | 4.339 | 106.083 | 3.253 | 0.638 | 100.000 |
| arima | exclude_covid | 4.483 | 117.129 | 3.466 | 0.624 | 100.000 |
| persistence | exclude_covid | 4.646 | 71.644 | 3.200 | 0.629 | 100.000 |
| persistence | post_covid | 4.646 | 71.644 | 3.200 | 0.629 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.720 | 71.826 | 3.247 | 0.568 | 95.349 |
| gnn_multiedge_covid_rsv_full | full | 4.995 | 85.954 | 3.782 | 0.661 | 97.674 |
| dualtopo_fullhistory | full | 5.499 | 66.836 | 3.544 | 0.361 | 90.698 |
| lstm | exclude_covid | 5.657 | 79.264 | 3.413 | 0.578 | 97.674 |
| dualtopo | post_covid | 5.724 | 172.641 | 4.923 | -0.531 | 100.000 |
| dualtopo_no_bg | post_covid | 5.781 | 176.868 | 4.984 | -0.412 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.987 | 116.645 | 4.506 | 0.642 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.328 | 115.908 | 4.714 | 0.629 | 100.000 |
| gnn_multiedge_full | full | 6.683 | 114.515 | 4.878 | 0.590 | 95.349 |
| gnn_multiedge | post_covid | 6.889 | 136.106 | 5.144 | 0.596 | 100.000 |
| gnn_multiedge_season | post_covid | 7.004 | 125.647 | 5.295 | 0.641 | 100.000 |
| gnn_corrbinary | post_covid | 8.500 | 157.346 | 6.215 | 0.552 | 100.000 |
| gnn_uniform | post_covid | 8.725 | 165.473 | 6.201 | 0.495 | 100.000 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| gnn_multiedge_season_level | post_covid | 10.759 | 199.970 | 7.770 | 0.573 | 100.000 |
| gnn_geo | post_covid | 11.333 | 230.990 | 7.934 | 0.426 | 100.000 |
| gnn_multiedge_level | post_covid | 12.951 | 235.969 | 8.920 | 0.485 | 93.023 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4.727 | 47.947 | 3.308 | 0.507 | 100.000 |
| arima | exclude_covid | 4.736 | 51.880 | 3.388 | 0.498 | 100.000 |
| lstm | post_covid | 4.745 | 41.155 | 3.198 | 0.577 | 100.000 |
| dualtopo_no_bg | post_covid | 5.499 | 76.777 | 4.347 | 0.073 | 100.000 |
| dualtopo | post_covid | 5.529 | 75.338 | 4.355 | -0.390 | 100.000 |
| persistence | exclude_covid | 5.618 | 44.043 | 3.960 | 0.494 | 100.000 |
| persistence | post_covid | 5.618 | 44.043 | 3.960 | 0.494 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.689 | 42.600 | 4.047 | 0.421 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 5.844 | 53.108 | 4.674 | 0.548 | 96.000 |
| gnn_multiedge_leaknorm | post_covid | 6.293 | 57.852 | 5.016 | 0.595 | 100.000 |
| dualtopo_fullhistory | full | 6.965 | 44.645 | 4.885 | 0.145 | 84.000 |
| gnn_multiedge_rt | post_covid | 6.978 | 62.993 | 5.537 | 0.563 | 100.000 |
| gnn_multiedge | post_covid | 6.989 | 65.832 | 5.586 | 0.557 | 100.000 |
| lstm | exclude_covid | 7.098 | 52.664 | 4.507 | 0.467 | 96.000 |
| gnn_multiedge_full | full | 7.611 | 68.968 | 5.912 | 0.488 | 92.000 |
| gnn_multiedge_season | post_covid | 7.745 | 72.102 | 6.334 | 0.573 | 100.000 |
| gnn_uniform | post_covid | 8.148 | 71.876 | 6.381 | 0.522 | 100.000 |
| gnn_corrbinary | post_covid | 8.595 | 77.334 | 6.825 | 0.520 | 100.000 |
| gnn_geo | post_covid | 9.975 | 95.588 | 7.569 | 0.484 | 100.000 |
| gnn_multiedge_season_level | post_covid | 11.038 | 106.069 | 8.706 | 0.544 | 100.000 |
| gnn_multiedge_level | post_covid | 12.103 | 110.013 | 9.348 | 0.520 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 2.209 | 97.658 | 1.681 | 0.444 | 100.000 |
| lstm | exclude_covid | 2.544 | 116.210 | 1.894 | 0.401 | 100.000 |
| persistence | exclude_covid | 2.782 | 109.979 | 2.144 | 0.256 | 100.000 |
| persistence | post_covid | 2.782 | 109.979 | 2.144 | 0.256 | 100.000 |
| lstm | post_covid | 2.866 | 140.154 | 2.355 | 0.346 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 2.875 | 112.416 | 2.136 | 0.318 | 94.444 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.486 | 131.575 | 2.542 | 0.294 | 100.000 |
| arima | post_covid | 3.733 | 186.827 | 3.178 | 0.201 | 100.000 |
| arima | exclude_covid | 4.107 | 207.752 | 3.576 | 0.159 | 100.000 |
| gnn_multiedge_full | full | 5.124 | 177.775 | 3.443 | 0.326 | 100.000 |
| gnn_multiedge_rt | post_covid | 5.294 | 189.402 | 3.572 | 0.276 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.534 | 198.302 | 3.799 | 0.322 | 100.000 |
| gnn_multiedge_season | post_covid | 5.821 | 200.016 | 3.853 | 0.295 | 100.000 |
| dualtopo | post_covid | 5.984 | 307.784 | 5.713 | -0.296 | 100.000 |
| dualtopo_no_bg | post_covid | 6.151 | 315.883 | 5.870 | -0.308 | 100.000 |
| gnn_multiedge | post_covid | 6.748 | 233.709 | 4.531 | 0.295 | 100.000 |
| gnn_corrbinary | post_covid | 8.367 | 268.474 | 5.368 | 0.277 | 100.000 |
| gnn_uniform | post_covid | 9.468 | 295.469 | 5.951 | 0.262 | 100.000 |
| gnn_multiedge_season_level | post_covid | 10.358 | 330.389 | 6.471 | 0.252 | 100.000 |
| gnn_geo | post_covid | 12.985 | 419.047 | 8.442 | 0.259 | 100.000 |
| gnn_multiedge_level | post_covid | 14.045 | 410.908 | 8.327 | 0.244 | 83.333 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
