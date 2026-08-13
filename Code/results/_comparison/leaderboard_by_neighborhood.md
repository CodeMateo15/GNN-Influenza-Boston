# Per-neighborhood leaderboard — horizon 1

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| lstm | 12 | 9 | 9 |
| arima | 2 | 4 | 1 |
| dualtopo_fullhistory | 0 | 0 | 1 |
| gnn_multiedge_covid_rsv | 0 | 1 | 0 |
| persistence | 0 | 0 | 1 |
| seasonal_naive | 0 | 0 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `arima (exclude_covid)`: Roxbury; `arima (post_covid)`: Dorchest.; `lstm (exclude_covid)`: BackBay+, Charles., E.Boston, JP, Mattapan, Roslind., S.Boston, W.Roxbury; `lstm (post_covid)`: Allston, Fenway, HydePark, S.End
- **Flu season (Oct–Mar)** — `arima (exclude_covid)`: Dorchest., Roxbury; `arima (post_covid)`: Fenway, S.Boston; `gnn_multiedge_covid_rsv (post_covid)`: HydePark; `lstm (exclude_covid)`: BackBay+, Charles., E.Boston, JP, Mattapan, Roslind., W.Roxbury; `lstm (post_covid)`: Allston, S.End
- **Off-season (Apr–Sep)** — `arima (post_covid)`: JP; `dualtopo_fullhistory (full)`: W.Roxbury; `lstm (exclude_covid)`: Allston, BackBay+, Charles., E.Boston, Fenway, HydePark, Roslind., S.Boston, S.End; `persistence (exclude_covid)`: Mattapan; `seasonal_naive (exclude_covid)`: Dorchest., Roxbury

`lstm (exclude_covid)` wins 8 of 14 neighborhoods. The pooled leaderboard is led by `arima (exclude_covid)` instead, and `lstm (exclude_covid)` ranks 3 there. That is not a contradiction: the pooled metric flattens all 14 neighborhoods into one set of cells, so it is dominated by the high-rate ones (Dorchester and Roxbury average roughly five times Fenway's rate). Winning most neighborhoods and winning the pooled error are different achievements, and which one you want depends on whether you are allocating city-wide capacity or advising a specific neighborhood.

## Dorchester

*mean observed 49.2, peak 256.1 per 100,000 over the full year*

### Overall (full year), 48–49 weeks scored (models differ), mean 49.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 20.486 | 56.161 | 14.185 | 0.931 | 97.917 |
| arima | exclude_covid | 21.106 | 50.967 | 13.274 | 0.924 | 93.750 |
| persistence | exclude_covid | 23.784 | 37.542 | 14.325 | 0.907 | 95.833 |
| persistence | post_covid | 23.784 | 37.542 | 14.325 | 0.907 | 95.833 |
| gnn_multiedge_covid_rsv | post_covid | 26.778 | 62.882 | 19.347 | 0.901 | 89.583 |
| lstm | post_covid | 31.265 | 59.998 | 18.896 | 0.863 | 89.583 |
| gnn_multiedge_leaknorm | post_covid | 31.567 | 56.036 | 20.128 | 0.910 | 83.333 |
| lstm | exclude_covid | 32.367 | 68.719 | 19.113 | 0.852 | 91.667 |
| gnn_multiedge_covid_rsv_full | full | 34.687 | 60.256 | 24.283 | 0.903 | 79.167 |
| gnn_multiedge_full | full | 35.421 | 56.800 | 22.472 | 0.891 | 79.167 |
| dualtopo_fullhistory | full | 38.404 | 98.036 | 25.814 | 0.779 | 73.469 |
| gnn_multiedge_rt | post_covid | 42.761 | 67.917 | 27.155 | 0.871 | 77.083 |
| gnn_multiedge | post_covid | 46.955 | 73.502 | 29.771 | 0.872 | 77.083 |
| dualtopo | post_covid | 56.200 | 252.525 | 43.196 | 0.498 | 55.102 |
| dualtopo_no_bg | post_covid | 56.471 | 255.515 | 43.439 | 0.432 | 55.102 |
| gnn_corrbinary | post_covid | 61.320 | 87.584 | 37.814 | 0.805 | 75.000 |
| gnn_uniform | post_covid | 64.202 | 91.459 | 40.226 | 0.808 | 68.750 |
| gnn_geo | post_covid | 70.396 | 106.097 | 45.147 | 0.806 | 72.917 |
| seasonal_naive | exclude_covid | 78.335 | 93.313 | 42.790 | 0.332 | 85.417 |
| seasonal_naive | post_covid | 78.335 | 93.313 | 42.790 | 0.332 | 89.583 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 24.479 | 18.354 | 15.175 | 0.925 | 92.308 |
| arima | post_covid | 25.342 | 21.401 | 17.016 | 0.921 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 29.957 | 33.156 | 22.575 | 0.895 | 96.154 |
| persistence | exclude_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| persistence | post_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 34.128 | 31.071 | 22.562 | 0.914 | 88.462 |
| gnn_multiedge_full | full | 37.991 | 32.379 | 25.588 | 0.898 | 80.769 |
| lstm | post_covid | 41.197 | 35.798 | 26.728 | 0.832 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 41.604 | 44.134 | 31.870 | 0.885 | 80.769 |
| lstm | exclude_covid | 42.877 | 35.581 | 27.265 | 0.823 | 84.615 |
| gnn_multiedge_rt | post_covid | 47.851 | 46.013 | 32.867 | 0.868 | 73.077 |
| dualtopo_fullhistory | full | 50.129 | 45.918 | 35.159 | 0.751 | 65.385 |
| gnn_multiedge | post_covid | 50.464 | 48.164 | 35.094 | 0.884 | 76.923 |
| dualtopo | post_covid | 63.243 | 81.380 | 41.060 | 0.294 | 69.231 |
| dualtopo_no_bg | post_covid | 63.273 | 81.113 | 41.009 | 0.263 | 69.231 |
| gnn_corrbinary | post_covid | 64.490 | 63.066 | 44.694 | 0.819 | 73.077 |
| gnn_uniform | post_covid | 69.331 | 69.013 | 49.047 | 0.815 | 61.538 |
| gnn_geo | post_covid | 77.579 | 83.532 | 56.793 | 0.806 | 65.385 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 22–23 weeks scored (models differ), mean 17.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.006 | 76.892 | 7.559 | 0.820 | 100.000 |
| seasonal_naive | post_covid | 9.006 | 76.892 | 7.559 | 0.820 | 100.000 |
| persistence | exclude_covid | 9.106 | 54.464 | 7.498 | 0.834 | 95.455 |
| persistence | post_covid | 9.106 | 54.464 | 7.498 | 0.834 | 95.455 |
| lstm | exclude_covid | 10.632 | 107.883 | 9.478 | 0.812 | 100.000 |
| lstm | post_covid | 11.266 | 88.598 | 9.640 | 0.802 | 100.000 |
| arima | post_covid | 12.517 | 97.241 | 10.838 | 0.723 | 95.455 |
| arima | exclude_covid | 16.240 | 89.510 | 11.029 | 0.590 | 95.455 |
| dualtopo_fullhistory | full | 17.363 | 156.953 | 15.249 | 0.653 | 82.609 |
| gnn_multiedge_covid_rsv | post_covid | 22.448 | 98.013 | 15.533 | 0.831 | 81.818 |
| gnn_multiedge_covid_rsv_full | full | 24.074 | 79.310 | 15.317 | 0.850 | 77.273 |
| gnn_multiedge_leaknorm | post_covid | 28.244 | 85.539 | 17.250 | 0.829 | 77.273 |
| gnn_multiedge_full | full | 32.120 | 85.660 | 18.789 | 0.831 | 77.273 |
| gnn_multiedge_rt | post_covid | 35.825 | 93.804 | 20.404 | 0.823 | 81.818 |
| gnn_multiedge | post_covid | 42.435 | 103.446 | 23.479 | 0.813 | 77.273 |
| dualtopo | post_covid | 46.986 | 445.993 | 45.612 | 0.689 | 39.130 |
| dualtopo_no_bg | post_covid | 47.626 | 452.664 | 46.187 | 0.635 | 39.130 |
| gnn_corrbinary | post_covid | 57.347 | 116.560 | 29.683 | 0.801 | 77.273 |
| gnn_uniform | post_covid | 57.554 | 117.986 | 29.801 | 0.809 | 77.273 |
| gnn_geo | post_covid | 60.823 | 132.764 | 31.384 | 0.801 | 81.818 |

## Roxbury

*mean observed 45.2, peak 254.7 per 100,000 over the full year*

### Overall (full year), 48–49 weeks scored (models differ), mean 45.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 28.283 | 96.035 | 17.924 | 0.835 | 89.583 |
| arima | post_covid | 28.912 | 79.595 | 18.781 | 0.837 | 91.667 |
| persistence | exclude_covid | 28.912 | 79.595 | 18.781 | 0.837 | 87.500 |
| persistence | post_covid | 28.912 | 79.595 | 18.781 | 0.837 | 89.583 |
| lstm | exclude_covid | 30.069 | 72.836 | 18.037 | 0.830 | 87.500 |
| lstm | post_covid | 30.724 | 54.453 | 17.450 | 0.813 | 81.250 |
| gnn_multiedge_covid_rsv | post_covid | 30.901 | 103.600 | 23.375 | 0.824 | 81.250 |
| gnn_multiedge_leaknorm | post_covid | 35.245 | 100.444 | 25.398 | 0.838 | 83.333 |
| dualtopo_fullhistory | full | 38.226 | 105.083 | 23.977 | 0.738 | 79.592 |
| gnn_multiedge_covid_rsv_full | full | 39.416 | 104.475 | 28.137 | 0.821 | 72.917 |
| gnn_multiedge_full | full | 40.725 | 101.566 | 27.350 | 0.803 | 68.750 |
| gnn_multiedge_rt | post_covid | 45.151 | 113.067 | 31.739 | 0.786 | 68.750 |
| gnn_multiedge | post_covid | 45.705 | 116.805 | 31.975 | 0.813 | 70.833 |
| dualtopo | post_covid | 50.807 | 231.367 | 37.698 | 0.436 | 65.306 |
| dualtopo_no_bg | post_covid | 51.053 | 234.665 | 38.012 | 0.357 | 65.306 |
| gnn_corrbinary | post_covid | 57.014 | 130.267 | 39.045 | 0.749 | 68.750 |
| gnn_uniform | post_covid | 59.274 | 135.287 | 40.805 | 0.753 | 62.500 |
| gnn_geo | post_covid | 61.022 | 142.578 | 41.260 | 0.747 | 70.833 |
| seasonal_naive | exclude_covid | 71.230 | 92.038 | 39.256 | 0.314 | 85.417 |
| seasonal_naive | post_covid | 71.230 | 92.038 | 39.256 | 0.314 | 93.750 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 35.807 | 49.600 | 22.907 | 0.806 | 84.615 |
| arima | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | exclude_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| gnn_multiedge_covid_rsv | post_covid | 36.988 | 66.755 | 29.008 | 0.801 | 76.923 |
| lstm | exclude_covid | 39.576 | 42.211 | 25.144 | 0.790 | 76.923 |
| lstm | post_covid | 40.622 | 36.528 | 24.829 | 0.769 | 69.231 |
| gnn_multiedge_leaknorm | post_covid | 41.717 | 67.103 | 30.777 | 0.823 | 80.769 |
| gnn_multiedge_full | full | 48.091 | 67.786 | 32.585 | 0.784 | 69.231 |
| gnn_multiedge_covid_rsv_full | full | 48.903 | 79.217 | 36.947 | 0.787 | 69.231 |
| dualtopo_fullhistory | full | 50.124 | 51.775 | 32.255 | 0.701 | 73.077 |
| gnn_multiedge | post_covid | 52.448 | 83.625 | 38.451 | 0.804 | 73.077 |
| gnn_multiedge_rt | post_covid | 54.185 | 85.194 | 40.242 | 0.757 | 57.692 |
| dualtopo | post_covid | 59.754 | 91.283 | 38.998 | 0.212 | 73.077 |
| dualtopo_no_bg | post_covid | 59.760 | 91.331 | 39.031 | 0.177 | 73.077 |
| gnn_corrbinary | post_covid | 63.335 | 101.561 | 47.007 | 0.740 | 69.231 |
| gnn_uniform | post_covid | 67.167 | 108.989 | 50.147 | 0.737 | 50.000 |
| gnn_geo | post_covid | 68.268 | 110.974 | 50.137 | 0.735 | 65.385 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 22–23 weeks scored (models differ), mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.584 | 48.656 | 6.527 | 0.794 | 100.000 |
| seasonal_naive | post_covid | 8.584 | 48.656 | 6.527 | 0.794 | 100.000 |
| lstm | post_covid | 10.457 | 75.637 | 8.729 | 0.700 | 95.455 |
| lstm | exclude_covid | 11.028 | 109.028 | 9.638 | 0.730 | 100.000 |
| arima | post_covid | 14.894 | 115.877 | 12.632 | 0.419 | 95.455 |
| persistence | exclude_covid | 14.894 | 115.877 | 12.632 | 0.419 | 86.364 |
| persistence | post_covid | 14.894 | 115.877 | 12.632 | 0.419 | 90.909 |
| arima | exclude_covid | 15.166 | 150.912 | 12.034 | 0.425 | 95.455 |
| dualtopo_fullhistory | full | 16.521 | 165.344 | 14.619 | 0.558 | 86.957 |
| gnn_multiedge_covid_rsv | post_covid | 21.599 | 147.144 | 16.719 | 0.545 | 86.364 |
| gnn_multiedge_covid_rsv_full | full | 23.736 | 134.325 | 17.726 | 0.588 | 77.273 |
| gnn_multiedge_leaknorm | post_covid | 25.563 | 139.848 | 19.041 | 0.595 | 86.364 |
| gnn_multiedge_full | full | 29.756 | 141.488 | 21.162 | 0.613 | 68.182 |
| gnn_multiedge_rt | post_covid | 31.273 | 146.006 | 21.689 | 0.599 | 81.818 |
| gnn_multiedge | post_covid | 36.149 | 156.017 | 24.322 | 0.611 | 68.182 |
| dualtopo | post_covid | 38.252 | 389.722 | 36.228 | 0.544 | 56.522 |
| dualtopo_no_bg | post_covid | 38.933 | 396.694 | 36.860 | 0.470 | 56.522 |
| gnn_uniform | post_covid | 48.311 | 166.365 | 29.765 | 0.637 | 77.273 |
| gnn_corrbinary | post_covid | 48.492 | 164.191 | 29.634 | 0.622 | 68.182 |
| gnn_geo | post_covid | 51.152 | 179.929 | 30.769 | 0.628 | 77.273 |

## Roslindale

*mean observed 32.8, peak 170.1 per 100,000 over the full year*

### Overall (full year), 41–42 weeks scored (models differ), mean 32.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 18.019 | 59.194 | 11.723 | 0.912 | 85.366 |
| lstm | post_covid | 20.216 | 64.128 | 13.190 | 0.893 | 87.805 |
| gnn_multiedge_covid_rsv | post_covid | 22.533 | 108.706 | 15.631 | 0.834 | 85.366 |
| arima | exclude_covid | 22.652 | 101.295 | 14.720 | 0.817 | 90.244 |
| gnn_multiedge_leaknorm | post_covid | 22.721 | 112.593 | 17.257 | 0.868 | 92.683 |
| persistence | exclude_covid | 23.464 | 86.505 | 14.993 | 0.823 | 85.366 |
| persistence | post_covid | 23.464 | 86.505 | 14.993 | 0.823 | 85.366 |
| gnn_multiedge_covid_rsv_full | full | 23.497 | 108.485 | 16.993 | 0.857 | 87.805 |
| dualtopo_fullhistory | full | 23.977 | 69.503 | 14.755 | 0.788 | 88.095 |
| gnn_multiedge_full | full | 24.549 | 106.936 | 18.156 | 0.853 | 85.366 |
| gnn_multiedge_rt | post_covid | 25.162 | 122.634 | 18.716 | 0.858 | 90.244 |
| arima | post_covid | 25.275 | 107.747 | 16.619 | 0.786 | 82.927 |
| gnn_multiedge | post_covid | 27.285 | 126.317 | 20.086 | 0.851 | 78.049 |
| gnn_corrbinary | post_covid | 33.698 | 143.125 | 24.074 | 0.799 | 75.610 |
| gnn_uniform | post_covid | 33.703 | 144.751 | 24.380 | 0.806 | 70.732 |
| gnn_geo | post_covid | 34.543 | 146.182 | 24.125 | 0.779 | 73.171 |
| dualtopo | post_covid | 38.582 | 164.949 | 25.822 | 0.354 | 90.476 |
| dualtopo_no_bg | post_covid | 38.627 | 166.551 | 25.947 | 0.323 | 90.476 |
| seasonal_naive | exclude_covid | 53.421 | 176.389 | 31.598 | 0.211 | 87.805 |
| seasonal_naive | post_covid | 53.421 | 176.389 | 31.598 | 0.211 | 95.122 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 21.907 | 55.498 | 15.138 | 0.905 | 80.769 |
| lstm | post_covid | 24.676 | 58.922 | 17.054 | 0.884 | 80.769 |
| gnn_multiedge_leaknorm | post_covid | 25.082 | 117.108 | 19.278 | 0.876 | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 26.308 | 114.409 | 18.176 | 0.828 | 80.769 |
| arima | exclude_covid | 27.097 | 94.524 | 17.809 | 0.804 | 84.615 |
| gnn_multiedge_full | full | 27.343 | 110.300 | 20.487 | 0.858 | 88.462 |
| gnn_multiedge_covid_rsv_full | full | 27.500 | 118.466 | 20.104 | 0.851 | 84.615 |
| gnn_multiedge_rt | post_covid | 28.023 | 133.085 | 21.215 | 0.864 | 92.308 |
| persistence | post_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| persistence | exclude_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| gnn_multiedge | post_covid | 29.686 | 131.524 | 22.311 | 0.864 | 80.769 |
| dualtopo_fullhistory | full | 29.776 | 58.827 | 19.309 | 0.768 | 80.769 |
| arima | post_covid | 30.480 | 102.622 | 20.643 | 0.773 | 73.077 |
| gnn_corrbinary | post_covid | 35.654 | 151.555 | 26.562 | 0.820 | 76.923 |
| gnn_uniform | post_covid | 35.805 | 155.509 | 27.171 | 0.827 | 69.231 |
| gnn_geo | post_covid | 36.320 | 154.030 | 26.471 | 0.803 | 73.077 |
| dualtopo_no_bg | post_covid | 46.297 | 121.027 | 30.400 | 0.219 | 84.615 |
| dualtopo | post_covid | 46.324 | 120.650 | 30.390 | 0.227 | 84.615 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 15–16 weeks scored (models differ), mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.458 | 65.601 | 5.804 | 0.547 | 93.333 |
| lstm | post_covid | 7.852 | 73.151 | 6.492 | 0.550 | 100.000 |
| dualtopo_fullhistory | full | 8.268 | 86.852 | 7.354 | 0.632 | 100.000 |
| persistence | exclude_covid | 9.806 | 63.879 | 7.540 | 0.447 | 93.333 |
| persistence | post_covid | 9.806 | 63.879 | 7.540 | 0.447 | 93.333 |
| seasonal_naive | exclude_covid | 10.970 | 88.166 | 7.840 | 0.283 | 93.333 |
| seasonal_naive | post_covid | 10.970 | 88.166 | 7.840 | 0.283 | 100.000 |
| arima | exclude_covid | 11.396 | 113.031 | 9.366 | 0.276 | 100.000 |
| arima | post_covid | 11.655 | 116.631 | 9.644 | 0.209 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.719 | 98.821 | 11.219 | 0.465 | 93.333 |
| gnn_multiedge_covid_rsv_full | full | 14.081 | 91.185 | 11.600 | 0.506 | 93.333 |
| gnn_multiedge_leaknorm | post_covid | 17.905 | 104.766 | 13.754 | 0.496 | 93.333 |
| gnn_multiedge_full | full | 18.746 | 101.104 | 14.114 | 0.503 | 80.000 |
| gnn_multiedge_rt | post_covid | 19.222 | 104.519 | 14.384 | 0.502 | 86.667 |
| dualtopo | post_covid | 20.504 | 236.934 | 18.398 | 0.523 | 100.000 |
| dualtopo_no_bg | post_covid | 20.823 | 240.528 | 18.712 | 0.493 | 100.000 |
| gnn_multiedge | post_covid | 22.527 | 117.291 | 16.228 | 0.497 | 73.333 |
| gnn_uniform | post_covid | 29.711 | 126.105 | 19.542 | 0.514 | 73.333 |
| gnn_corrbinary | post_covid | 30.005 | 128.512 | 19.760 | 0.501 | 73.333 |
| gnn_geo | post_covid | 31.224 | 132.577 | 20.060 | 0.502 | 73.333 |

## South End

*mean observed 27.3, peak 132.3 per 100,000 over the full year*

### Overall (full year), 48–49 weeks scored (models differ), mean 27.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 16.571 | 76.182 | 10.062 | 0.859 | 97.917 |
| lstm | exclude_covid | 16.583 | 57.596 | 9.414 | 0.866 | 93.750 |
| arima | exclude_covid | 16.899 | 60.435 | 9.675 | 0.861 | 95.833 |
| arima | post_covid | 16.917 | 74.736 | 10.082 | 0.852 | 97.917 |
| persistence | exclude_covid | 17.517 | 57.487 | 10.285 | 0.852 | 93.750 |
| persistence | post_covid | 17.517 | 57.487 | 10.285 | 0.852 | 93.750 |
| dualtopo_fullhistory | full | 18.023 | 77.735 | 11.087 | 0.827 | 93.878 |
| gnn_multiedge_covid_rsv | post_covid | 18.940 | 90.119 | 13.210 | 0.833 | 93.750 |
| gnn_multiedge_leaknorm | post_covid | 20.946 | 85.803 | 14.238 | 0.841 | 91.667 |
| gnn_multiedge_covid_rsv_full | full | 22.119 | 86.866 | 15.625 | 0.849 | 81.250 |
| gnn_multiedge_full | full | 22.334 | 84.159 | 15.109 | 0.839 | 83.333 |
| gnn_multiedge_rt | post_covid | 24.453 | 99.184 | 16.997 | 0.820 | 85.417 |
| gnn_multiedge | post_covid | 26.337 | 104.962 | 18.649 | 0.821 | 81.250 |
| dualtopo | post_covid | 32.298 | 221.112 | 24.109 | 0.443 | 89.796 |
| dualtopo_no_bg | post_covid | 32.410 | 223.485 | 24.269 | 0.393 | 89.796 |
| gnn_corrbinary | post_covid | 33.007 | 119.586 | 22.102 | 0.748 | 77.083 |
| gnn_uniform | post_covid | 34.327 | 121.105 | 23.379 | 0.752 | 75.000 |
| gnn_geo | post_covid | 36.223 | 131.672 | 24.573 | 0.746 | 77.083 |
| seasonal_naive | exclude_covid | 41.245 | 136.620 | 24.615 | 0.344 | 95.833 |
| seasonal_naive | post_covid | 41.245 | 136.620 | 24.615 | 0.344 | 97.917 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 21.272 | 59.125 | 12.886 | 0.833 | 96.154 |
| arima | post_covid | 21.417 | 48.565 | 12.098 | 0.830 | 96.154 |
| arima | exclude_covid | 21.641 | 44.852 | 12.330 | 0.840 | 96.154 |
| lstm | exclude_covid | 21.841 | 49.944 | 13.151 | 0.840 | 88.462 |
| persistence | exclude_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| persistence | post_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 22.530 | 66.189 | 15.934 | 0.820 | 96.154 |
| dualtopo_fullhistory | full | 23.533 | 55.202 | 14.733 | 0.806 | 88.462 |
| gnn_multiedge_leaknorm | post_covid | 24.213 | 64.091 | 17.111 | 0.838 | 96.154 |
| gnn_multiedge_full | full | 25.271 | 60.009 | 18.073 | 0.843 | 88.462 |
| gnn_multiedge_covid_rsv_full | full | 26.965 | 72.209 | 20.562 | 0.832 | 80.769 |
| gnn_multiedge_rt | post_covid | 28.158 | 80.257 | 21.026 | 0.816 | 84.615 |
| gnn_multiedge | post_covid | 29.339 | 83.017 | 22.794 | 0.829 | 80.769 |
| gnn_corrbinary | post_covid | 36.274 | 97.239 | 26.920 | 0.754 | 76.923 |
| gnn_uniform | post_covid | 37.970 | 99.089 | 29.080 | 0.757 | 69.231 |
| dualtopo_no_bg | post_covid | 38.789 | 132.939 | 25.974 | 0.236 | 80.769 |
| dualtopo | post_covid | 38.797 | 133.128 | 25.967 | 0.264 | 80.769 |
| gnn_geo | post_covid | 40.179 | 103.535 | 30.448 | 0.750 | 73.077 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 22–23 weeks scored (models differ), mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.021 | 66.639 | 4.998 | 0.548 | 100.000 |
| lstm | post_covid | 8.023 | 96.339 | 6.725 | 0.569 | 100.000 |
| seasonal_naive | exclude_covid | 8.024 | 82.113 | 6.491 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 8.024 | 82.113 | 6.491 | 0.266 | 100.000 |
| dualtopo_fullhistory | full | 8.122 | 103.207 | 6.965 | 0.471 | 100.000 |
| arima | exclude_covid | 8.344 | 78.851 | 6.537 | 0.333 | 95.455 |
| persistence | exclude_covid | 8.621 | 76.599 | 6.818 | 0.277 | 95.455 |
| persistence | post_covid | 8.621 | 76.599 | 6.818 | 0.277 | 95.455 |
| arima | post_covid | 9.072 | 105.666 | 7.698 | 0.277 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.520 | 118.400 | 9.991 | 0.411 | 90.909 |
| gnn_multiedge_covid_rsv_full | full | 14.427 | 104.188 | 9.790 | 0.442 | 81.818 |
| gnn_multiedge_leaknorm | post_covid | 16.261 | 111.463 | 10.843 | 0.456 | 86.364 |
| gnn_multiedge_full | full | 18.264 | 112.699 | 11.605 | 0.475 | 77.273 |
| gnn_multiedge_rt | post_covid | 19.172 | 121.552 | 12.236 | 0.472 | 86.364 |
| gnn_multiedge | post_covid | 22.272 | 130.898 | 13.750 | 0.483 | 81.818 |
| dualtopo | post_covid | 22.821 | 320.572 | 22.008 | 0.561 | 100.000 |
| dualtopo_no_bg | post_covid | 23.173 | 325.842 | 22.342 | 0.532 | 100.000 |
| gnn_corrbinary | post_covid | 28.669 | 145.996 | 16.408 | 0.502 | 77.273 |
| gnn_uniform | post_covid | 29.448 | 147.125 | 16.641 | 0.497 | 81.818 |
| gnn_geo | post_covid | 30.902 | 164.924 | 17.629 | 0.493 | 81.818 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 34–35 weeks scored (models differ), mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 15.319 | 58.958 | 8.281 | 0.727 | 94.118 |
| lstm | post_covid | 15.350 | 62.143 | 8.626 | 0.725 | 94.118 |
| arima | exclude_covid | 16.590 | 95.326 | 9.769 | 0.673 | 97.059 |
| arima | post_covid | 17.265 | 84.570 | 10.172 | 0.632 | 97.059 |
| gnn_multiedge_covid_rsv | post_covid | 17.701 | 108.228 | 11.183 | 0.685 | 94.118 |
| persistence | exclude_covid | 17.839 | 82.588 | 10.288 | 0.679 | 94.118 |
| persistence | post_covid | 17.839 | 82.588 | 10.288 | 0.679 | 94.118 |
| gnn_multiedge_leaknorm | post_covid | 18.825 | 112.310 | 13.159 | 0.721 | 97.059 |
| dualtopo_fullhistory | full | 18.843 | 75.860 | 10.403 | 0.555 | 88.571 |
| gnn_multiedge_covid_rsv_full | full | 19.695 | 115.862 | 13.443 | 0.706 | 88.235 |
| gnn_multiedge_full | full | 20.016 | 116.919 | 14.154 | 0.710 | 88.235 |
| gnn_multiedge_rt | post_covid | 21.248 | 130.749 | 15.172 | 0.707 | 88.235 |
| dualtopo | post_covid | 21.819 | 119.644 | 14.006 | 0.303 | 88.571 |
| dualtopo_no_bg | post_covid | 21.854 | 120.109 | 14.039 | 0.237 | 88.571 |
| gnn_multiedge | post_covid | 21.982 | 138.450 | 15.941 | 0.705 | 82.353 |
| gnn_uniform | post_covid | 25.226 | 154.464 | 18.266 | 0.662 | 85.294 |
| gnn_corrbinary | post_covid | 26.232 | 159.347 | 19.113 | 0.667 | 85.294 |
| gnn_geo | post_covid | 26.513 | 167.126 | 19.898 | 0.659 | 82.353 |
| seasonal_naive | exclude_covid | 28.690 | 141.907 | 18.779 | 0.223 | 94.118 |
| seasonal_naive | post_covid | 28.690 | 141.907 | 18.779 | 0.223 | 97.059 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 19.251 | 68.847 | 11.405 | 0.689 | 90.476 |
| lstm | post_covid | 19.272 | 71.192 | 11.952 | 0.693 | 90.476 |
| arima | exclude_covid | 20.198 | 94.520 | 12.042 | 0.647 | 95.238 |
| gnn_multiedge_covid_rsv | post_covid | 21.333 | 118.051 | 14.094 | 0.662 | 90.476 |
| arima | post_covid | 21.375 | 86.881 | 13.295 | 0.593 | 95.238 |
| persistence | exclude_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| persistence | post_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| gnn_multiedge_leaknorm | post_covid | 22.348 | 121.244 | 16.673 | 0.708 | 95.238 |
| gnn_multiedge_full | full | 23.497 | 123.832 | 17.749 | 0.700 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 23.775 | 130.475 | 17.459 | 0.683 | 85.714 |
| dualtopo_fullhistory | full | 23.973 | 85.740 | 14.662 | 0.494 | 80.952 |
| gnn_multiedge_rt | post_covid | 24.911 | 142.249 | 19.142 | 0.696 | 85.714 |
| gnn_multiedge | post_covid | 25.347 | 149.355 | 19.782 | 0.700 | 76.190 |
| dualtopo | post_covid | 26.923 | 111.043 | 17.378 | 0.112 | 80.952 |
| dualtopo_no_bg | post_covid | 26.941 | 110.860 | 17.372 | 0.064 | 80.952 |
| gnn_uniform | post_covid | 28.039 | 160.360 | 22.003 | 0.668 | 85.714 |
| gnn_corrbinary | post_covid | 29.499 | 167.884 | 23.387 | 0.669 | 80.952 |
| gnn_geo | post_covid | 29.518 | 175.050 | 24.309 | 0.664 | 76.190 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |

### Off-season (Apr–Sep), 13–14 weeks scored (models differ), mean 9.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 3.891 | 42.984 | 3.236 | 0.573 | 100.000 |
| lstm | post_covid | 4.032 | 47.525 | 3.252 | 0.613 | 100.000 |
| dualtopo_fullhistory | full | 5.058 | 61.040 | 4.015 | 0.571 | 100.000 |
| arima | post_covid | 6.445 | 80.836 | 5.128 | 0.087 | 100.000 |
| persistence | exclude_covid | 6.518 | 66.437 | 5.123 | -0.012 | 100.000 |
| persistence | post_covid | 6.518 | 66.437 | 5.123 | -0.012 | 100.000 |
| arima | exclude_covid | 7.800 | 96.628 | 6.096 | 0.092 | 100.000 |
| seasonal_naive | exclude_covid | 8.672 | 62.248 | 5.923 | 0.566 | 100.000 |
| seasonal_naive | post_covid | 8.672 | 62.248 | 5.923 | 0.566 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.182 | 92.361 | 6.481 | 0.212 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 10.067 | 92.257 | 6.955 | 0.294 | 92.308 |
| dualtopo | post_covid | 10.143 | 132.546 | 8.948 | 0.606 | 100.000 |
| dualtopo_no_bg | post_covid | 10.259 | 133.983 | 9.040 | 0.577 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.959 | 97.878 | 7.483 | 0.294 | 100.000 |
| gnn_multiedge_full | full | 12.489 | 105.752 | 8.346 | 0.320 | 92.308 |
| gnn_multiedge_rt | post_covid | 13.356 | 112.172 | 8.758 | 0.313 | 92.308 |
| gnn_multiedge | post_covid | 15.032 | 120.835 | 9.736 | 0.337 | 92.308 |
| gnn_corrbinary | post_covid | 19.848 | 145.557 | 12.208 | 0.360 | 92.308 |
| gnn_uniform | post_covid | 19.858 | 144.939 | 12.229 | 0.367 | 84.615 |
| gnn_geo | post_covid | 20.758 | 154.324 | 12.774 | 0.352 | 92.308 |

## Mattapan

*mean observed 19.0, peak 110.3 per 100,000 over the full year*

### Overall (full year), 46–47 weeks scored (models differ), mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 8.871 | 75.214 | 6.304 | 0.933 | 100.000 |
| lstm | post_covid | 10.303 | 82.368 | 7.043 | 0.914 | 100.000 |
| arima | post_covid | 12.001 | 94.905 | 8.537 | 0.857 | 97.826 |
| dualtopo_fullhistory | full | 12.093 | 106.193 | 9.267 | 0.869 | 97.872 |
| persistence | exclude_covid | 12.135 | 66.247 | 8.370 | 0.859 | 97.826 |
| persistence | post_covid | 12.135 | 66.247 | 8.370 | 0.859 | 97.826 |
| arima | exclude_covid | 12.868 | 90.198 | 8.875 | 0.833 | 97.826 |
| gnn_multiedge_covid_rsv | post_covid | 13.687 | 101.224 | 10.322 | 0.838 | 97.826 |
| gnn_multiedge_leaknorm | post_covid | 14.249 | 101.778 | 10.586 | 0.881 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 14.652 | 95.612 | 10.970 | 0.880 | 97.826 |
| gnn_multiedge_full | full | 15.749 | 98.491 | 11.002 | 0.863 | 91.304 |
| gnn_multiedge_rt | post_covid | 18.592 | 116.905 | 13.257 | 0.844 | 86.957 |
| gnn_multiedge | post_covid | 20.142 | 127.962 | 14.481 | 0.844 | 89.130 |
| dualtopo | post_covid | 25.200 | 303.733 | 21.651 | 0.434 | 93.617 |
| dualtopo_no_bg | post_covid | 25.365 | 307.943 | 21.845 | 0.400 | 93.617 |
| gnn_uniform | post_covid | 27.013 | 152.181 | 18.724 | 0.770 | 80.435 |
| gnn_corrbinary | post_covid | 27.492 | 152.311 | 18.825 | 0.773 | 84.783 |
| gnn_geo | post_covid | 30.018 | 165.445 | 20.952 | 0.779 | 80.435 |
| seasonal_naive | exclude_covid | 36.543 | 158.165 | 21.096 | 0.457 | 97.826 |
| seasonal_naive | post_covid | 36.543 | 158.165 | 21.096 | 0.457 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 10.431 | 47.053 | 7.276 | 0.925 | 100.000 |
| lstm | post_covid | 11.328 | 51.547 | 7.590 | 0.915 | 100.000 |
| dualtopo_fullhistory | full | 14.174 | 48.787 | 10.054 | 0.861 | 96.154 |
| arima | post_covid | 14.832 | 59.112 | 10.855 | 0.832 | 96.154 |
| persistence | exclude_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| persistence | post_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 15.744 | 76.391 | 12.368 | 0.888 | 96.154 |
| arima | exclude_covid | 16.199 | 56.847 | 11.732 | 0.801 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 16.294 | 75.066 | 12.927 | 0.819 | 96.154 |
| gnn_multiedge_full | full | 17.535 | 73.186 | 12.787 | 0.869 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 17.619 | 81.015 | 14.097 | 0.868 | 96.154 |
| gnn_multiedge_rt | post_covid | 21.031 | 94.599 | 16.063 | 0.845 | 84.615 |
| gnn_multiedge | post_covid | 21.877 | 100.789 | 17.166 | 0.863 | 92.308 |
| dualtopo | post_covid | 26.701 | 150.093 | 20.630 | 0.277 | 88.462 |
| dualtopo_no_bg | post_covid | 26.704 | 150.675 | 20.666 | 0.264 | 88.462 |
| gnn_uniform | post_covid | 29.013 | 126.245 | 22.436 | 0.791 | 80.769 |
| gnn_corrbinary | post_covid | 29.235 | 121.410 | 22.291 | 0.800 | 88.462 |
| gnn_geo | post_covid | 32.910 | 132.629 | 25.647 | 0.797 | 80.769 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 20–21 weeks scored (models differ), mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 5.032 | 84.938 | 4.395 | 0.195 | 100.000 |
| persistence | post_covid | 5.032 | 84.938 | 4.395 | 0.195 | 100.000 |
| lstm | exclude_covid | 6.289 | 111.824 | 5.041 | 0.613 | 100.000 |
| arima | exclude_covid | 6.304 | 133.553 | 5.160 | 0.263 | 100.000 |
| arima | post_covid | 6.726 | 141.437 | 5.525 | 0.142 | 100.000 |
| seasonal_naive | exclude_covid | 8.275 | 170.337 | 7.215 | -0.035 | 100.000 |
| seasonal_naive | post_covid | 8.275 | 170.337 | 7.215 | -0.035 | 100.000 |
| lstm | post_covid | 8.794 | 122.434 | 6.333 | 0.587 | 100.000 |
| dualtopo_fullhistory | full | 8.865 | 177.268 | 8.294 | 0.706 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.258 | 135.231 | 6.936 | 0.458 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 9.498 | 114.588 | 6.905 | 0.520 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 12.032 | 134.781 | 8.269 | 0.508 | 100.000 |
| gnn_multiedge_full | full | 13.068 | 131.387 | 8.680 | 0.520 | 90.000 |
| gnn_multiedge_rt | post_covid | 14.835 | 145.902 | 9.608 | 0.516 | 90.000 |
| gnn_multiedge | post_covid | 17.634 | 163.287 | 10.991 | 0.518 | 85.000 |
| dualtopo | post_covid | 23.208 | 493.955 | 22.916 | 0.558 | 100.000 |
| dualtopo_no_bg | post_covid | 23.602 | 502.657 | 23.305 | 0.599 | 100.000 |
| gnn_uniform | post_covid | 24.165 | 185.898 | 13.899 | 0.543 | 80.000 |
| gnn_corrbinary | post_covid | 25.046 | 192.482 | 14.320 | 0.523 | 80.000 |
| gnn_geo | post_covid | 25.779 | 208.106 | 14.849 | 0.528 | 80.000 |

## Hyde Park

*mean observed 17.0, peak 94.6 per 100,000 over the full year*

### Overall (full year), 45–46 weeks scored (models differ), mean 17.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 11.197 | 85.262 | 7.297 | 0.860 | 95.556 |
| arima | exclude_covid | 11.487 | 84.282 | 7.551 | 0.830 | 97.778 |
| arima | post_covid | 11.545 | 90.929 | 7.718 | 0.829 | 97.778 |
| persistence | exclude_covid | 11.792 | 56.660 | 7.438 | 0.834 | 95.556 |
| persistence | post_covid | 11.792 | 56.660 | 7.438 | 0.834 | 95.556 |
| gnn_multiedge_covid_rsv | post_covid | 12.096 | 92.413 | 9.075 | 0.844 | 97.778 |
| lstm | exclude_covid | 12.153 | 78.326 | 7.720 | 0.841 | 95.556 |
| gnn_multiedge_leaknorm | post_covid | 13.754 | 84.902 | 9.730 | 0.865 | 97.778 |
| gnn_multiedge_covid_rsv_full | full | 14.388 | 87.213 | 10.666 | 0.848 | 93.333 |
| dualtopo_fullhistory | full | 14.765 | 105.769 | 9.777 | 0.750 | 89.130 |
| gnn_multiedge_full | full | 15.420 | 81.194 | 10.376 | 0.833 | 95.556 |
| gnn_multiedge_rt | post_covid | 17.508 | 100.591 | 12.329 | 0.833 | 93.333 |
| gnn_multiedge | post_covid | 19.250 | 108.858 | 13.425 | 0.830 | 91.111 |
| dualtopo | post_covid | 21.060 | 257.213 | 16.294 | 0.372 | 91.304 |
| dualtopo_no_bg | post_covid | 21.146 | 260.090 | 16.393 | 0.302 | 91.304 |
| gnn_corrbinary | post_covid | 24.958 | 132.686 | 16.688 | 0.754 | 84.444 |
| gnn_uniform | post_covid | 25.378 | 127.313 | 17.045 | 0.763 | 80.000 |
| gnn_geo | post_covid | 26.594 | 146.795 | 17.874 | 0.732 | 80.000 |
| seasonal_naive | exclude_covid | 33.748 | 171.993 | 19.696 | 0.174 | 97.778 |
| seasonal_naive | post_covid | 33.748 | 171.993 | 19.696 | 0.174 | 97.778 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 13.632 | 73.007 | 10.888 | 0.849 | 96.000 |
| lstm | post_covid | 14.185 | 54.157 | 9.268 | 0.837 | 92.000 |
| arima | post_covid | 14.364 | 57.485 | 9.779 | 0.808 | 96.000 |
| arima | exclude_covid | 14.398 | 56.586 | 9.792 | 0.807 | 96.000 |
| gnn_multiedge_leaknorm | post_covid | 14.891 | 73.592 | 11.560 | 0.878 | 100.000 |
| persistence | exclude_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| persistence | post_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| lstm | exclude_covid | 15.756 | 59.404 | 10.617 | 0.809 | 92.000 |
| gnn_multiedge_full | full | 16.911 | 70.585 | 12.396 | 0.844 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 16.948 | 87.983 | 14.072 | 0.839 | 96.000 |
| dualtopo_fullhistory | full | 19.292 | 73.349 | 13.358 | 0.714 | 80.000 |
| gnn_multiedge_rt | post_covid | 19.307 | 95.455 | 15.139 | 0.843 | 92.000 |
| gnn_multiedge | post_covid | 20.557 | 98.819 | 16.089 | 0.854 | 92.000 |
| dualtopo | post_covid | 24.232 | 114.511 | 16.598 | 0.124 | 84.000 |
| dualtopo_no_bg | post_covid | 24.234 | 114.224 | 16.597 | 0.106 | 84.000 |
| gnn_corrbinary | post_covid | 25.986 | 129.990 | 19.770 | 0.784 | 88.000 |
| gnn_uniform | post_covid | 26.863 | 122.980 | 20.607 | 0.789 | 80.000 |
| gnn_geo | post_covid | 28.173 | 144.467 | 21.436 | 0.752 | 80.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |

### Off-season (Apr–Sep), 20–21 weeks scored (models differ), mean 6.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 4.689 | 101.978 | 4.099 | 0.584 | 100.000 |
| lstm | post_covid | 5.529 | 124.143 | 4.834 | 0.608 | 100.000 |
| persistence | exclude_covid | 5.743 | 60.543 | 3.685 | 0.499 | 100.000 |
| persistence | post_covid | 5.743 | 60.543 | 3.685 | 0.499 | 100.000 |
| dualtopo_fullhistory | full | 5.869 | 144.365 | 5.515 | 0.593 | 100.000 |
| arima | exclude_covid | 6.148 | 118.901 | 4.750 | 0.473 | 100.000 |
| arima | post_covid | 6.477 | 132.735 | 5.141 | 0.465 | 100.000 |
| seasonal_naive | exclude_covid | 6.759 | 120.246 | 5.070 | 0.353 | 100.000 |
| seasonal_naive | post_covid | 6.759 | 120.246 | 5.070 | 0.353 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.844 | 116.671 | 6.810 | 0.603 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 10.332 | 86.250 | 6.408 | 0.625 | 90.000 |
| gnn_multiedge_leaknorm | post_covid | 12.185 | 99.040 | 7.442 | 0.622 | 95.000 |
| gnn_multiedge_full | full | 13.324 | 94.454 | 7.851 | 0.633 | 95.000 |
| gnn_multiedge_rt | post_covid | 14.958 | 107.011 | 8.817 | 0.649 | 95.000 |
| dualtopo | post_covid | 16.507 | 427.095 | 15.932 | 0.582 | 100.000 |
| dualtopo_no_bg | post_covid | 16.743 | 433.740 | 16.151 | 0.505 | 100.000 |
| gnn_multiedge | post_covid | 17.479 | 121.407 | 10.095 | 0.639 | 90.000 |
| gnn_uniform | post_covid | 23.390 | 132.729 | 12.592 | 0.646 | 80.000 |
| gnn_corrbinary | post_covid | 23.611 | 136.056 | 12.835 | 0.652 | 80.000 |
| gnn_geo | post_covid | 24.477 | 149.705 | 13.421 | 0.657 | 80.000 |

## Allston/Brighton

*mean observed 16.0, peak 80.6 per 100,000 over the full year*

### Overall (full year), 48–49 weeks scored (models differ), mean 16.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 8.027 | 59.403 | 5.244 | 0.902 | 95.833 |
| lstm | exclude_covid | 8.561 | 47.410 | 5.205 | 0.911 | 93.750 |
| arima | exclude_covid | 10.112 | 70.040 | 6.683 | 0.833 | 97.917 |
| arima | post_covid | 10.158 | 73.347 | 6.772 | 0.832 | 100.000 |
| persistence | exclude_covid | 10.566 | 61.148 | 7.033 | 0.832 | 100.000 |
| persistence | post_covid | 10.566 | 61.148 | 7.033 | 0.832 | 100.000 |
| dualtopo_fullhistory | full | 10.621 | 70.988 | 6.832 | 0.816 | 91.837 |
| gnn_multiedge_covid_rsv | post_covid | 10.880 | 78.745 | 8.018 | 0.829 | 100.000 |
| gnn_multiedge_full | full | 11.199 | 71.435 | 7.707 | 0.865 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.376 | 75.043 | 8.030 | 0.855 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 11.937 | 75.354 | 8.197 | 0.844 | 97.917 |
| gnn_multiedge_rt | post_covid | 13.037 | 84.346 | 9.084 | 0.840 | 100.000 |
| gnn_multiedge | post_covid | 14.570 | 89.288 | 10.079 | 0.829 | 97.917 |
| gnn_corrbinary | post_covid | 17.233 | 99.155 | 11.664 | 0.780 | 95.833 |
| gnn_uniform | post_covid | 18.024 | 100.495 | 12.122 | 0.785 | 87.500 |
| dualtopo | post_covid | 18.116 | 191.830 | 12.891 | 0.459 | 89.796 |
| dualtopo_no_bg | post_covid | 18.185 | 194.691 | 12.997 | 0.418 | 89.796 |
| gnn_geo | post_covid | 18.436 | 108.926 | 12.277 | 0.771 | 89.583 |
| seasonal_naive | exclude_covid | 23.360 | 127.927 | 13.887 | 0.294 | 97.917 |
| seasonal_naive | post_covid | 23.360 | 127.927 | 13.887 | 0.294 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 10.453 | 36.472 | 7.351 | 0.886 | 92.308 |
| lstm | exclude_covid | 11.381 | 33.957 | 7.765 | 0.894 | 88.462 |
| arima | post_covid | 13.077 | 51.014 | 9.519 | 0.794 | 100.000 |
| gnn_multiedge_full | full | 13.132 | 56.087 | 9.592 | 0.854 | 100.000 |
| arima | exclude_covid | 13.239 | 53.613 | 9.672 | 0.789 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 13.461 | 66.321 | 10.990 | 0.795 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 13.480 | 62.469 | 10.306 | 0.838 | 100.000 |
| persistence | exclude_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| persistence | post_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| dualtopo_fullhistory | full | 14.133 | 50.059 | 10.158 | 0.789 | 84.615 |
| gnn_multiedge_covid_rsv_full | full | 14.963 | 67.819 | 11.290 | 0.810 | 96.154 |
| gnn_multiedge_rt | post_covid | 15.166 | 72.590 | 11.582 | 0.827 | 100.000 |
| gnn_multiedge | post_covid | 16.768 | 77.506 | 12.812 | 0.817 | 100.000 |
| gnn_corrbinary | post_covid | 18.939 | 86.483 | 14.414 | 0.776 | 100.000 |
| gnn_uniform | post_covid | 20.064 | 87.122 | 15.109 | 0.778 | 88.462 |
| gnn_geo | post_covid | 20.218 | 94.624 | 15.110 | 0.766 | 88.462 |
| dualtopo_no_bg | post_covid | 22.053 | 72.853 | 14.050 | 0.255 | 80.769 |
| dualtopo | post_covid | 22.057 | 72.684 | 14.041 | 0.271 | 80.769 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22–23 weeks scored (models differ), mean 6.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.613 | 63.310 | 2.179 | 0.785 | 100.000 |
| lstm | post_covid | 3.382 | 86.503 | 2.754 | 0.786 | 100.000 |
| dualtopo_fullhistory | full | 3.812 | 94.648 | 3.071 | 0.563 | 100.000 |
| persistence | exclude_covid | 3.838 | 68.622 | 3.114 | 0.620 | 100.000 |
| persistence | post_covid | 3.838 | 68.622 | 3.114 | 0.620 | 100.000 |
| arima | exclude_covid | 3.996 | 89.453 | 3.151 | 0.635 | 100.000 |
| seasonal_naive | exclude_covid | 4.642 | 99.038 | 3.741 | 0.606 | 100.000 |
| seasonal_naive | post_covid | 4.642 | 99.038 | 3.741 | 0.606 | 100.000 |
| arima | post_covid | 4.798 | 99.740 | 3.525 | 0.525 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.642 | 93.428 | 4.505 | 0.665 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.805 | 84.260 | 4.541 | 0.658 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 8.223 | 89.904 | 5.341 | 0.702 | 100.000 |
| gnn_multiedge_full | full | 8.359 | 89.573 | 5.479 | 0.709 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.949 | 98.240 | 6.133 | 0.690 | 100.000 |
| gnn_multiedge | post_covid | 11.439 | 103.212 | 6.849 | 0.709 | 95.455 |
| dualtopo | post_covid | 12.217 | 326.517 | 11.590 | 0.500 | 100.000 |
| dualtopo_no_bg | post_covid | 12.440 | 332.421 | 11.806 | 0.461 | 100.000 |
| gnn_corrbinary | post_covid | 14.967 | 114.132 | 8.414 | 0.709 | 90.909 |
| gnn_uniform | post_covid | 15.264 | 116.299 | 8.593 | 0.725 | 86.364 |
| gnn_geo | post_covid | 16.077 | 125.829 | 8.928 | 0.721 | 90.909 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 11.709 | 51.336 | 6.763 | 0.825 | 95.000 |
| lstm | post_covid | 12.997 | 55.865 | 7.498 | 0.787 | 90.000 |
| gnn_multiedge_covid_rsv_full | full | 13.988 | 89.219 | 9.208 | 0.772 | 95.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.038 | 93.333 | 8.928 | 0.730 | 92.500 |
| gnn_multiedge_leaknorm | post_covid | 14.131 | 100.352 | 9.900 | 0.779 | 92.500 |
| dualtopo_fullhistory | full | 14.217 | 58.806 | 7.375 | 0.683 | 92.500 |
| arima | post_covid | 14.359 | 83.004 | 8.524 | 0.677 | 95.000 |
| arima | exclude_covid | 14.371 | 87.626 | 8.497 | 0.667 | 95.000 |
| persistence | post_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| persistence | exclude_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| gnn_multiedge_full | full | 14.828 | 97.300 | 10.273 | 0.769 | 90.000 |
| gnn_multiedge_rt | post_covid | 15.424 | 109.446 | 11.196 | 0.772 | 95.000 |
| gnn_multiedge | post_covid | 16.515 | 119.090 | 11.638 | 0.757 | 92.500 |
| gnn_uniform | post_covid | 18.620 | 135.706 | 13.471 | 0.728 | 85.000 |
| gnn_geo | post_covid | 18.939 | 140.857 | 13.282 | 0.720 | 90.000 |
| dualtopo | post_covid | 19.198 | 111.346 | 10.863 | 0.289 | 92.500 |
| dualtopo_no_bg | post_covid | 19.212 | 113.366 | 10.970 | 0.284 | 92.500 |
| gnn_corrbinary | post_covid | 19.333 | 139.890 | 13.988 | 0.727 | 95.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 14.509 | 48.817 | 8.693 | 0.809 | 92.000 |
| lstm | post_covid | 16.141 | 53.509 | 9.893 | 0.773 | 84.000 |
| gnn_multiedge_leaknorm | post_covid | 16.422 | 93.584 | 12.010 | 0.777 | 88.000 |
| gnn_multiedge_covid_rsv_full | full | 16.795 | 87.096 | 11.554 | 0.757 | 92.000 |
| gnn_multiedge_covid_rsv | post_covid | 16.910 | 90.474 | 11.178 | 0.711 | 88.000 |
| gnn_multiedge_full | full | 17.146 | 85.884 | 12.359 | 0.770 | 88.000 |
| arima | exclude_covid | 17.666 | 78.247 | 10.717 | 0.638 | 92.000 |
| arima | post_covid | 17.710 | 77.152 | 10.817 | 0.648 | 92.000 |
| dualtopo_fullhistory | full | 17.735 | 54.882 | 9.730 | 0.651 | 88.000 |
| persistence | post_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| persistence | exclude_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| gnn_multiedge_rt | post_covid | 17.825 | 101.632 | 13.582 | 0.771 | 92.000 |
| gnn_multiedge | post_covid | 18.766 | 109.870 | 13.805 | 0.761 | 92.000 |
| gnn_uniform | post_covid | 20.120 | 117.736 | 15.397 | 0.750 | 84.000 |
| gnn_geo | post_covid | 20.215 | 119.473 | 14.753 | 0.746 | 92.000 |
| gnn_corrbinary | post_covid | 20.928 | 121.613 | 16.028 | 0.749 | 96.000 |
| dualtopo_no_bg | post_covid | 23.375 | 79.485 | 12.918 | 0.197 | 88.000 |
| dualtopo | post_covid | 23.400 | 78.674 | 12.878 | 0.192 | 88.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.841 | 65.348 | 3.449 | 0.294 | 100.000 |
| lstm | exclude_covid | 3.841 | 55.533 | 3.546 | 0.206 | 100.000 |
| lstm | post_covid | 4.029 | 59.792 | 3.506 | 0.277 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| arima | post_covid | 5.204 | 92.758 | 4.701 | -0.206 | 100.000 |
| persistence | exclude_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| persistence | post_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| arima | exclude_covid | 5.528 | 103.256 | 4.796 | -0.219 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.995 | 98.097 | 5.180 | 0.084 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 7.190 | 92.758 | 5.299 | 0.162 | 100.000 |
| dualtopo | post_covid | 8.382 | 165.800 | 7.505 | 0.177 | 100.000 |
| dualtopo_no_bg | post_covid | 8.582 | 169.833 | 7.723 | 0.174 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 9.110 | 111.632 | 6.383 | 0.140 | 100.000 |
| gnn_multiedge_full | full | 9.815 | 116.327 | 6.795 | 0.148 | 93.333 |
| gnn_multiedge_rt | post_covid | 10.240 | 122.470 | 7.219 | 0.182 | 100.000 |
| gnn_multiedge | post_covid | 11.847 | 134.456 | 8.026 | 0.184 | 93.333 |
| gnn_uniform | post_covid | 15.806 | 165.657 | 10.261 | 0.202 | 86.667 |
| gnn_corrbinary | post_covid | 16.333 | 170.351 | 10.589 | 0.213 | 93.333 |
| gnn_geo | post_covid | 16.595 | 176.498 | 10.830 | 0.206 | 86.667 |

## South Boston

*mean observed 12.2, peak 57.0 per 100,000 over the full year*

### Overall (full year), 41–42 weeks scored (models differ), mean 12.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.609 | 53.962 | 4.391 | 0.844 | 97.561 |
| arima | post_covid | 7.911 | 81.871 | 5.275 | 0.806 | 97.561 |
| lstm | post_covid | 8.016 | 49.138 | 4.571 | 0.823 | 97.561 |
| arima | exclude_covid | 8.288 | 81.686 | 5.512 | 0.784 | 97.561 |
| dualtopo_fullhistory | full | 8.382 | 81.457 | 5.724 | 0.791 | 95.238 |
| persistence | exclude_covid | 8.765 | 52.256 | 5.459 | 0.783 | 95.122 |
| persistence | post_covid | 8.765 | 52.256 | 5.459 | 0.783 | 95.122 |
| gnn_multiedge_covid_rsv | post_covid | 8.880 | 79.022 | 6.276 | 0.781 | 97.561 |
| gnn_multiedge_leaknorm | post_covid | 9.897 | 81.273 | 6.776 | 0.807 | 97.561 |
| gnn_multiedge_covid_rsv_full | full | 10.505 | 80.720 | 7.528 | 0.802 | 92.683 |
| gnn_multiedge_full | full | 10.887 | 79.458 | 7.307 | 0.789 | 95.122 |
| gnn_multiedge_rt | post_covid | 10.934 | 88.152 | 7.809 | 0.801 | 97.561 |
| gnn_multiedge | post_covid | 11.854 | 97.500 | 8.533 | 0.801 | 97.561 |
| dualtopo | post_covid | 13.099 | 186.090 | 9.438 | 0.427 | 90.476 |
| dualtopo_no_bg | post_covid | 13.126 | 187.245 | 9.487 | 0.401 | 90.476 |
| gnn_corrbinary | post_covid | 14.601 | 110.012 | 10.150 | 0.736 | 100.000 |
| gnn_uniform | post_covid | 15.142 | 110.939 | 10.587 | 0.739 | 87.805 |
| gnn_geo | post_covid | 16.027 | 121.846 | 11.350 | 0.732 | 90.244 |
| seasonal_naive | exclude_covid | 22.229 | 111.601 | 12.046 | 0.228 | 95.122 |
| seasonal_naive | post_covid | 22.229 | 111.601 | 12.046 | 0.228 | 97.561 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 9.302 | 74.444 | 6.045 | 0.788 | 96.000 |
| lstm | exclude_covid | 9.410 | 51.216 | 5.722 | 0.824 | 96.000 |
| lstm | post_covid | 9.866 | 45.992 | 5.924 | 0.800 | 96.000 |
| arima | exclude_covid | 9.893 | 61.045 | 6.358 | 0.757 | 96.000 |
| dualtopo_fullhistory | full | 10.366 | 64.721 | 7.409 | 0.771 | 92.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.374 | 68.323 | 7.790 | 0.755 | 96.000 |
| persistence | exclude_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| persistence | post_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| gnn_multiedge_leaknorm | post_covid | 11.161 | 69.152 | 8.146 | 0.799 | 96.000 |
| gnn_multiedge_full | full | 12.281 | 67.060 | 8.848 | 0.781 | 92.000 |
| gnn_multiedge_rt | post_covid | 12.381 | 79.312 | 9.608 | 0.791 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 12.530 | 78.245 | 9.831 | 0.774 | 92.000 |
| gnn_multiedge | post_covid | 13.064 | 84.811 | 10.318 | 0.804 | 96.000 |
| dualtopo_no_bg | post_covid | 15.402 | 136.425 | 10.302 | 0.295 | 84.000 |
| dualtopo | post_covid | 15.407 | 136.737 | 10.300 | 0.320 | 84.000 |
| gnn_corrbinary | post_covid | 15.904 | 95.744 | 12.184 | 0.734 | 100.000 |
| gnn_uniform | post_covid | 16.479 | 95.908 | 12.839 | 0.741 | 88.000 |
| gnn_geo | post_covid | 17.642 | 108.568 | 13.913 | 0.727 | 92.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 16–17 weeks scored (models differ), mean 4.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 3.162 | 58.253 | 2.311 | 0.298 | 100.000 |
| seasonal_naive | exclude_covid | 3.356 | 56.030 | 2.644 | 0.236 | 100.000 |
| seasonal_naive | post_covid | 3.356 | 56.030 | 2.644 | 0.236 | 100.000 |
| lstm | post_covid | 3.545 | 54.052 | 2.457 | 0.403 | 100.000 |
| dualtopo_fullhistory | full | 3.948 | 106.070 | 3.247 | 0.270 | 100.000 |
| persistence | exclude_covid | 4.443 | 62.717 | 3.181 | 0.010 | 100.000 |
| persistence | post_covid | 4.443 | 62.717 | 3.181 | 0.010 | 100.000 |
| arima | exclude_covid | 4.806 | 113.937 | 4.190 | -0.090 | 100.000 |
| arima | post_covid | 5.020 | 93.477 | 4.070 | -0.079 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.824 | 95.739 | 3.910 | 0.249 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.124 | 84.586 | 3.931 | 0.328 | 93.750 |
| gnn_multiedge_leaknorm | post_covid | 7.510 | 100.211 | 4.636 | 0.296 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.175 | 101.965 | 4.998 | 0.356 | 100.000 |
| gnn_multiedge_full | full | 8.249 | 98.831 | 4.899 | 0.326 | 100.000 |
| dualtopo | post_covid | 8.650 | 258.666 | 8.171 | 0.205 | 100.000 |
| dualtopo_no_bg | post_covid | 8.762 | 261.979 | 8.288 | 0.229 | 100.000 |
| gnn_multiedge | post_covid | 9.667 | 117.326 | 5.744 | 0.340 | 100.000 |
| gnn_corrbinary | post_covid | 12.291 | 132.306 | 6.972 | 0.393 | 100.000 |
| gnn_uniform | post_covid | 12.774 | 134.425 | 7.069 | 0.368 | 87.500 |
| gnn_geo | post_covid | 13.112 | 142.593 | 7.346 | 0.382 | 87.500 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 45–46 weeks scored (models differ), mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.551 | 67.812 | 4.899 | 0.864 | 93.333 |
| lstm | post_covid | 7.462 | 74.472 | 5.173 | 0.841 | 95.556 |
| dualtopo_fullhistory | full | 8.036 | 83.010 | 5.741 | 0.774 | 95.652 |
| arima | exclude_covid | 9.192 | 94.102 | 5.906 | 0.691 | 95.556 |
| arima | post_covid | 9.872 | 69.062 | 6.224 | 0.693 | 97.778 |
| persistence | exclude_covid | 9.872 | 69.062 | 6.224 | 0.693 | 97.778 |
| persistence | post_covid | 9.872 | 69.062 | 6.224 | 0.693 | 97.778 |
| gnn_multiedge_covid_rsv | post_covid | 10.509 | 95.042 | 7.452 | 0.662 | 95.556 |
| gnn_multiedge_covid_rsv_full | full | 10.941 | 90.008 | 7.776 | 0.738 | 97.778 |
| gnn_multiedge_full | full | 11.101 | 92.613 | 7.734 | 0.723 | 97.778 |
| gnn_multiedge_leaknorm | post_covid | 11.177 | 96.067 | 7.898 | 0.698 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.010 | 102.388 | 8.244 | 0.704 | 97.778 |
| dualtopo | post_covid | 12.290 | 188.995 | 8.371 | 0.511 | 93.478 |
| dualtopo_no_bg | post_covid | 12.341 | 193.734 | 8.475 | 0.466 | 93.478 |
| gnn_multiedge | post_covid | 13.354 | 112.134 | 9.474 | 0.686 | 97.778 |
| gnn_corrbinary | post_covid | 15.641 | 123.382 | 10.848 | 0.629 | 97.778 |
| gnn_uniform | post_covid | 16.040 | 125.191 | 11.014 | 0.626 | 95.556 |
| gnn_geo | post_covid | 16.325 | 135.593 | 11.501 | 0.616 | 93.333 |
| seasonal_naive | exclude_covid | 18.232 | 141.547 | 10.873 | 0.265 | 97.778 |
| seasonal_naive | post_covid | 18.232 | 141.547 | 10.873 | 0.265 | 97.778 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 8.289 | 45.279 | 6.640 | 0.849 | 88.462 |
| lstm | post_covid | 9.496 | 47.375 | 7.037 | 0.821 | 92.308 |
| dualtopo_fullhistory | full | 10.354 | 56.345 | 8.184 | 0.736 | 92.308 |
| arima | exclude_covid | 11.576 | 53.205 | 7.766 | 0.594 | 92.308 |
| arima | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | exclude_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 13.084 | 67.758 | 10.056 | 0.536 | 92.308 |
| gnn_multiedge_full | full | 13.187 | 67.937 | 9.834 | 0.653 | 96.154 |
| gnn_multiedge_leaknorm | post_covid | 13.584 | 70.895 | 10.318 | 0.605 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 13.622 | 74.149 | 10.607 | 0.645 | 100.000 |
| gnn_multiedge_rt | post_covid | 14.361 | 79.156 | 10.499 | 0.617 | 96.154 |
| dualtopo_no_bg | post_covid | 14.686 | 79.577 | 9.044 | 0.303 | 88.462 |
| dualtopo | post_covid | 14.713 | 78.624 | 9.041 | 0.339 | 88.462 |
| gnn_multiedge | post_covid | 15.759 | 83.700 | 12.056 | 0.599 | 96.154 |
| gnn_corrbinary | post_covid | 18.094 | 99.517 | 13.640 | 0.530 | 96.154 |
| gnn_uniform | post_covid | 18.342 | 96.901 | 13.717 | 0.540 | 96.154 |
| gnn_geo | post_covid | 18.556 | 105.702 | 14.397 | 0.523 | 92.308 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 19–20 weeks scored (models differ), mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.763 | 98.647 | 2.517 | 0.542 | 100.000 |
| lstm | post_covid | 2.914 | 111.553 | 2.623 | 0.583 | 100.000 |
| dualtopo_fullhistory | full | 3.029 | 117.673 | 2.565 | 0.660 | 100.000 |
| arima | post_covid | 3.839 | 93.180 | 2.974 | 0.269 | 100.000 |
| persistence | exclude_covid | 3.839 | 93.180 | 2.974 | 0.269 | 100.000 |
| persistence | post_covid | 3.839 | 93.180 | 2.974 | 0.269 | 100.000 |
| arima | exclude_covid | 4.092 | 150.066 | 3.362 | 0.277 | 100.000 |
| seasonal_naive | exclude_covid | 4.733 | 136.326 | 3.695 | 0.374 | 100.000 |
| seasonal_naive | post_covid | 4.733 | 136.326 | 3.695 | 0.374 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.224 | 132.379 | 3.888 | 0.500 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.437 | 111.710 | 3.903 | 0.578 | 94.737 |
| gnn_multiedge_leaknorm | post_covid | 6.585 | 130.513 | 4.586 | 0.536 | 100.000 |
| gnn_multiedge_full | full | 7.342 | 126.379 | 4.860 | 0.558 | 100.000 |
| gnn_multiedge_rt | post_covid | 7.709 | 134.179 | 5.158 | 0.585 | 100.000 |
| dualtopo | post_covid | 8.122 | 332.478 | 7.500 | 0.586 | 100.000 |
| dualtopo_no_bg | post_covid | 8.361 | 342.137 | 7.736 | 0.550 | 100.000 |
| gnn_multiedge | post_covid | 9.085 | 151.043 | 5.942 | 0.573 | 100.000 |
| gnn_corrbinary | post_covid | 11.462 | 156.039 | 7.027 | 0.626 | 100.000 |
| gnn_uniform | post_covid | 12.207 | 163.904 | 7.315 | 0.600 | 94.737 |
| gnn_geo | post_covid | 12.648 | 176.497 | 7.538 | 0.604 | 94.737 |

## East Boston

*mean observed 11.7, peak 59.3 per 100,000 over the full year*

### Overall (full year), 43–44 weeks scored (models differ), mean 11.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.553 | 78.314 | 4.763 | 0.868 | 95.349 |
| arima | exclude_covid | 7.815 | 114.069 | 5.957 | 0.802 | 97.674 |
| arima | post_covid | 7.845 | 116.035 | 6.080 | 0.801 | 97.674 |
| lstm | post_covid | 7.936 | 92.390 | 5.301 | 0.843 | 97.674 |
| dualtopo_fullhistory | full | 7.988 | 98.272 | 5.669 | 0.797 | 95.455 |
| persistence | exclude_covid | 8.323 | 99.751 | 6.309 | 0.798 | 97.674 |
| persistence | post_covid | 8.323 | 99.751 | 6.309 | 0.798 | 97.674 |
| gnn_multiedge_covid_rsv | post_covid | 8.606 | 128.592 | 6.333 | 0.793 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 9.309 | 133.399 | 6.656 | 0.824 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 9.430 | 125.491 | 6.541 | 0.815 | 100.000 |
| gnn_multiedge_full | full | 9.978 | 129.439 | 6.704 | 0.804 | 97.674 |
| gnn_multiedge_rt | post_covid | 11.423 | 150.038 | 8.174 | 0.787 | 100.000 |
| gnn_multiedge | post_covid | 12.058 | 162.551 | 8.611 | 0.800 | 95.349 |
| dualtopo | post_covid | 12.874 | 211.771 | 9.356 | 0.434 | 90.909 |
| dualtopo_no_bg | post_covid | 12.908 | 213.362 | 9.402 | 0.387 | 90.909 |
| gnn_uniform | post_covid | 15.297 | 186.367 | 10.842 | 0.738 | 93.023 |
| gnn_corrbinary | post_covid | 15.310 | 183.793 | 10.886 | 0.743 | 95.349 |
| gnn_geo | post_covid | 17.399 | 198.577 | 12.421 | 0.741 | 93.023 |
| seasonal_naive | exclude_covid | 18.808 | 143.446 | 11.095 | 0.304 | 97.674 |
| seasonal_naive | post_covid | 18.808 | 143.446 | 11.095 | 0.304 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 8.253 | 81.815 | 6.520 | 0.848 | 92.000 |
| arima | exclude_covid | 9.378 | 110.901 | 7.472 | 0.785 | 96.000 |
| arima | post_covid | 9.430 | 115.902 | 7.673 | 0.783 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 9.926 | 149.393 | 8.087 | 0.771 | 100.000 |
| lstm | post_covid | 9.983 | 97.420 | 7.265 | 0.821 | 96.000 |
| dualtopo_fullhistory | full | 10.100 | 78.344 | 7.360 | 0.776 | 92.000 |
| gnn_multiedge_leaknorm | post_covid | 10.211 | 155.330 | 8.046 | 0.822 | 100.000 |
| persistence | exclude_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| persistence | post_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| gnn_multiedge_full | full | 11.150 | 149.172 | 8.056 | 0.797 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 11.206 | 150.134 | 8.471 | 0.788 | 100.000 |
| gnn_multiedge_rt | post_covid | 12.734 | 175.401 | 10.021 | 0.774 | 100.000 |
| gnn_multiedge | post_covid | 12.897 | 192.444 | 10.306 | 0.807 | 96.000 |
| dualtopo_no_bg | post_covid | 15.315 | 135.402 | 10.241 | 0.189 | 84.000 |
| dualtopo | post_covid | 15.315 | 135.554 | 10.246 | 0.203 | 84.000 |
| gnn_uniform | post_covid | 15.969 | 218.130 | 12.871 | 0.748 | 96.000 |
| gnn_corrbinary | post_covid | 16.126 | 214.825 | 12.949 | 0.749 | 96.000 |
| gnn_geo | post_covid | 19.061 | 235.113 | 15.383 | 0.733 | 96.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 18–19 weeks scored (models differ), mean 4.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.824 | 73.451 | 2.322 | 0.567 | 100.000 |
| lstm | post_covid | 3.469 | 85.404 | 2.574 | 0.616 | 100.000 |
| dualtopo_fullhistory | full | 3.681 | 124.494 | 3.444 | 0.606 | 100.000 |
| seasonal_naive | exclude_covid | 3.773 | 114.173 | 3.278 | 0.351 | 100.000 |
| seasonal_naive | post_covid | 3.773 | 114.173 | 3.278 | 0.351 | 100.000 |
| persistence | exclude_covid | 4.491 | 77.949 | 3.294 | 0.315 | 100.000 |
| persistence | post_covid | 4.491 | 77.949 | 3.294 | 0.315 | 100.000 |
| arima | post_covid | 4.849 | 116.219 | 3.867 | 0.296 | 100.000 |
| arima | exclude_covid | 4.873 | 118.469 | 3.853 | 0.266 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.166 | 91.265 | 3.860 | 0.566 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.334 | 99.701 | 3.897 | 0.542 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 7.887 | 102.940 | 4.725 | 0.563 | 100.000 |
| gnn_multiedge_full | full | 8.072 | 102.031 | 4.826 | 0.567 | 100.000 |
| dualtopo | post_covid | 8.672 | 312.057 | 8.184 | 0.562 | 100.000 |
| dualtopo_no_bg | post_covid | 8.790 | 315.942 | 8.299 | 0.592 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.302 | 114.813 | 5.611 | 0.611 | 100.000 |
| gnn_multiedge | post_covid | 10.786 | 121.034 | 6.257 | 0.608 | 94.444 |
| gnn_corrbinary | post_covid | 14.100 | 140.692 | 8.022 | 0.648 | 94.444 |
| gnn_uniform | post_covid | 14.312 | 142.251 | 8.024 | 0.624 | 88.889 |
| gnn_geo | post_covid | 14.785 | 147.831 | 8.306 | 0.637 | 88.889 |

## Jamaica Plain

*mean observed 11.1, peak 61.1 per 100,000 over the full year*

### Overall (full year), 45–46 weeks scored (models differ), mean 11.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 5.936 | 74.323 | 4.096 | 0.915 | 100.000 |
| lstm | post_covid | 6.497 | 72.339 | 4.314 | 0.895 | 97.778 |
| arima | exclude_covid | 7.642 | 90.885 | 4.933 | 0.837 | 95.556 |
| dualtopo_fullhistory | full | 7.868 | 107.343 | 5.315 | 0.823 | 95.652 |
| gnn_multiedge_covid_rsv | post_covid | 7.941 | 86.624 | 5.442 | 0.839 | 97.778 |
| arima | post_covid | 7.945 | 58.684 | 4.831 | 0.837 | 97.778 |
| persistence | exclude_covid | 7.945 | 58.684 | 4.831 | 0.837 | 97.778 |
| persistence | post_covid | 7.945 | 58.684 | 4.831 | 0.837 | 97.778 |
| gnn_multiedge_leaknorm | post_covid | 8.106 | 81.345 | 5.703 | 0.871 | 100.000 |
| gnn_multiedge_full | full | 8.739 | 75.259 | 5.955 | 0.860 | 97.778 |
| gnn_multiedge_covid_rsv_full | full | 9.126 | 82.067 | 6.133 | 0.845 | 95.556 |
| gnn_multiedge_rt | post_covid | 9.401 | 89.577 | 6.536 | 0.849 | 100.000 |
| gnn_multiedge | post_covid | 10.275 | 98.103 | 7.348 | 0.844 | 100.000 |
| gnn_uniform | post_covid | 12.712 | 107.794 | 8.765 | 0.803 | 97.778 |
| gnn_corrbinary | post_covid | 12.743 | 110.311 | 8.922 | 0.801 | 100.000 |
| gnn_geo | post_covid | 12.771 | 114.211 | 8.846 | 0.794 | 100.000 |
| dualtopo | post_covid | 13.794 | 226.490 | 9.919 | 0.418 | 91.304 |
| dualtopo_no_bg | post_covid | 13.844 | 230.226 | 10.013 | 0.366 | 91.304 |
| seasonal_naive | exclude_covid | 17.743 | 149.581 | 10.902 | 0.273 | 100.000 |
| seasonal_naive | post_covid | 17.743 | 149.581 | 10.902 | 0.273 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.716 | 67.678 | 5.889 | 0.899 | 100.000 |
| lstm | post_covid | 8.520 | 70.122 | 6.373 | 0.875 | 95.833 |
| gnn_multiedge_leaknorm | post_covid | 9.717 | 81.117 | 7.580 | 0.861 | 100.000 |
| arima | exclude_covid | 10.013 | 81.598 | 6.905 | 0.800 | 91.667 |
| gnn_multiedge_covid_rsv | post_covid | 10.085 | 86.464 | 7.515 | 0.808 | 95.833 |
| dualtopo_fullhistory | full | 10.248 | 79.888 | 7.274 | 0.796 | 91.667 |
| gnn_multiedge_full | full | 10.382 | 72.985 | 7.884 | 0.851 | 95.833 |
| persistence | exclude_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| persistence | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| arima | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| gnn_multiedge_rt | post_covid | 11.319 | 95.553 | 8.814 | 0.834 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 11.672 | 92.212 | 8.883 | 0.812 | 91.667 |
| gnn_multiedge | post_covid | 12.057 | 102.533 | 9.825 | 0.835 | 100.000 |
| gnn_geo | post_covid | 14.093 | 113.016 | 11.264 | 0.800 | 100.000 |
| gnn_corrbinary | post_covid | 14.352 | 115.349 | 11.669 | 0.801 | 100.000 |
| gnn_uniform | post_covid | 14.389 | 112.006 | 11.488 | 0.802 | 100.000 |
| dualtopo_no_bg | post_covid | 17.099 | 139.259 | 11.222 | 0.135 | 83.333 |
| dualtopo | post_covid | 17.112 | 138.472 | 11.207 | 0.168 | 83.333 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 21–22 weeks scored (models differ), mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2.701 | 51.746 | 1.862 | 0.558 | 100.000 |
| persistence | exclude_covid | 2.701 | 51.746 | 1.862 | 0.558 | 100.000 |
| persistence | post_covid | 2.701 | 51.746 | 1.862 | 0.558 | 100.000 |
| lstm | exclude_covid | 2.731 | 81.918 | 2.047 | 0.604 | 100.000 |
| lstm | post_covid | 2.737 | 74.871 | 1.960 | 0.649 | 100.000 |
| arima | exclude_covid | 3.249 | 101.500 | 2.678 | 0.525 | 100.000 |
| seasonal_naive | exclude_covid | 3.616 | 96.984 | 3.157 | 0.076 | 100.000 |
| seasonal_naive | post_covid | 3.616 | 96.984 | 3.157 | 0.076 | 100.000 |
| dualtopo_fullhistory | full | 3.857 | 137.295 | 3.177 | 0.549 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.349 | 86.807 | 3.071 | 0.684 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.772 | 70.473 | 2.991 | 0.702 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.737 | 81.605 | 3.558 | 0.708 | 100.000 |
| gnn_multiedge_full | full | 6.362 | 77.857 | 3.749 | 0.727 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.554 | 82.746 | 3.933 | 0.739 | 100.000 |
| gnn_multiedge | post_covid | 7.751 | 93.040 | 4.518 | 0.734 | 100.000 |
| dualtopo | post_covid | 8.855 | 322.510 | 8.514 | 0.704 | 100.000 |
| dualtopo_no_bg | post_covid | 9.044 | 329.463 | 8.694 | 0.663 | 100.000 |
| gnn_uniform | post_covid | 10.471 | 102.981 | 5.652 | 0.744 | 95.238 |
| gnn_corrbinary | post_covid | 10.611 | 104.554 | 5.783 | 0.761 | 100.000 |
| gnn_geo | post_covid | 11.069 | 115.575 | 6.083 | 0.758 | 100.000 |

## Fenway

*mean observed 7.0, peak 21.1 per 100,000 over the full year*

### Overall (full year), 42–43 weeks scored (models differ), mean 7.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.666 | 66.843 | 2.560 | 0.740 | 100.000 |
| arima | exclude_covid | 3.899 | 87.650 | 2.807 | 0.711 | 100.000 |
| arima | post_covid | 3.917 | 91.112 | 2.860 | 0.709 | 100.000 |
| persistence | exclude_covid | 4.069 | 68.632 | 2.776 | 0.720 | 100.000 |
| persistence | post_covid | 4.069 | 68.632 | 2.776 | 0.720 | 100.000 |
| lstm | exclude_covid | 4.225 | 64.836 | 2.815 | 0.690 | 97.619 |
| gnn_multiedge_covid_rsv | post_covid | 4.761 | 91.951 | 3.665 | 0.687 | 100.000 |
| dualtopo_fullhistory | full | 5.348 | 88.238 | 3.318 | 0.571 | 97.674 |
| gnn_multiedge_leaknorm | post_covid | 5.375 | 98.771 | 4.203 | 0.717 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.487 | 97.201 | 4.115 | 0.747 | 100.000 |
| dualtopo | post_covid | 5.688 | 173.613 | 4.885 | 0.584 | 100.000 |
| dualtopo_no_bg | post_covid | 5.709 | 174.761 | 4.899 | 0.561 | 100.000 |
| gnn_multiedge_full | full | 6.008 | 107.852 | 4.660 | 0.710 | 100.000 |
| gnn_multiedge_rt | post_covid | 6.246 | 109.805 | 4.737 | 0.725 | 100.000 |
| gnn_multiedge | post_covid | 6.988 | 121.484 | 5.284 | 0.694 | 100.000 |
| gnn_uniform | post_covid | 8.729 | 140.998 | 6.387 | 0.610 | 100.000 |
| gnn_geo | post_covid | 8.768 | 148.020 | 6.407 | 0.631 | 100.000 |
| gnn_corrbinary | post_covid | 8.781 | 142.861 | 6.482 | 0.643 | 100.000 |
| seasonal_naive | exclude_covid | 9.903 | 102.730 | 5.914 | 0.434 | 100.000 |
| seasonal_naive | post_covid | 9.903 | 102.730 | 5.914 | 0.434 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4.276 | 43.921 | 3.031 | 0.627 | 100.000 |
| arima | exclude_covid | 4.310 | 43.269 | 3.041 | 0.627 | 100.000 |
| lstm | post_covid | 4.336 | 39.149 | 3.041 | 0.669 | 100.000 |
| persistence | exclude_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| persistence | post_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| lstm | exclude_covid | 5.205 | 42.812 | 3.581 | 0.608 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.320 | 54.668 | 4.315 | 0.590 | 100.000 |
| dualtopo_no_bg | post_covid | 5.416 | 75.214 | 4.252 | 0.463 | 100.000 |
| dualtopo | post_covid | 5.424 | 75.296 | 4.265 | 0.499 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 5.916 | 60.502 | 4.951 | 0.652 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.166 | 62.935 | 4.962 | 0.683 | 100.000 |
| gnn_multiedge_full | full | 6.445 | 65.970 | 5.407 | 0.669 | 100.000 |
| dualtopo_fullhistory | full | 6.572 | 47.268 | 3.942 | 0.487 | 96.000 |
| gnn_multiedge_rt | post_covid | 6.794 | 66.207 | 5.523 | 0.684 | 100.000 |
| gnn_multiedge | post_covid | 7.556 | 74.741 | 6.142 | 0.639 | 100.000 |
| gnn_geo | post_covid | 9.097 | 87.085 | 7.207 | 0.592 | 100.000 |
| gnn_uniform | post_covid | 9.246 | 86.306 | 7.353 | 0.553 | 100.000 |
| gnn_corrbinary | post_covid | 9.352 | 88.415 | 7.546 | 0.593 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 17–18 weeks scored (models differ), mean 3.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.065 | 97.225 | 1.688 | 0.505 | 100.000 |
| lstm | post_covid | 2.356 | 107.568 | 1.852 | 0.430 | 100.000 |
| persistence | exclude_covid | 2.696 | 106.290 | 2.041 | 0.211 | 100.000 |
| persistence | post_covid | 2.696 | 106.290 | 2.041 | 0.211 | 100.000 |
| dualtopo_fullhistory | full | 2.889 | 145.142 | 2.452 | 0.304 | 100.000 |
| seasonal_naive | exclude_covid | 3.133 | 101.845 | 2.265 | -0.041 | 100.000 |
| seasonal_naive | post_covid | 3.133 | 101.845 | 2.265 | -0.041 | 100.000 |
| arima | exclude_covid | 3.201 | 152.917 | 2.464 | 0.174 | 100.000 |
| arima | post_covid | 3.319 | 160.509 | 2.609 | 0.167 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 3.791 | 146.779 | 2.708 | 0.277 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.299 | 147.593 | 2.871 | 0.303 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 4.464 | 155.049 | 3.103 | 0.326 | 100.000 |
| gnn_multiedge_full | full | 5.301 | 169.444 | 3.560 | 0.338 | 100.000 |
| gnn_multiedge_rt | post_covid | 5.341 | 173.921 | 3.581 | 0.312 | 100.000 |
| dualtopo | post_covid | 6.036 | 310.165 | 5.745 | 0.316 | 100.000 |
| gnn_multiedge | post_covid | 6.057 | 190.223 | 4.022 | 0.330 | 100.000 |
| dualtopo_no_bg | post_covid | 6.092 | 313.020 | 5.798 | 0.297 | 100.000 |
| gnn_corrbinary | post_covid | 7.865 | 222.928 | 4.919 | 0.326 | 100.000 |
| gnn_uniform | post_covid | 7.909 | 221.427 | 4.967 | 0.354 | 100.000 |
| gnn_geo | post_covid | 8.261 | 237.632 | 5.231 | 0.336 | 100.000 |

## Comparability notes

- 'off_season/Allston/Brighton': most models were scored on 22 cells, but — 23 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Back Bay/Beacon Hill/Downtown/North End/West End': most models were scored on 19 cells, but — 20 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Charlestown': most models were scored on 13 cells, but — 14 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Dorchester': most models were scored on 22 cells, but — 23 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/East Boston': most models were scored on 18 cells, but — 19 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Fenway': most models were scored on 17 cells, but — 18 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Hyde Park': most models were scored on 20 cells, but — 21 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Jamaica Plain': most models were scored on 21 cells, but — 22 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Mattapan': most models were scored on 20 cells, but — 21 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Roslindale': most models were scored on 15 cells, but — 16 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/Roxbury': most models were scored on 22 cells, but — 23 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/South Boston': most models were scored on 16 cells, but — 17 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'off_season/South End': most models were scored on 22 cells, but — 23 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Allston/Brighton': most models were scored on 48 cells, but — 49 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Back Bay/Beacon Hill/Downtown/North End/West End': most models were scored on 45 cells, but — 46 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Charlestown': most models were scored on 34 cells, but — 35 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Dorchester': most models were scored on 48 cells, but — 49 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/East Boston': most models were scored on 43 cells, but — 44 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Fenway': most models were scored on 42 cells, but — 43 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Hyde Park': most models were scored on 45 cells, but — 46 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Jamaica Plain': most models were scored on 45 cells, but — 46 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Mattapan': most models were scored on 46 cells, but — 47 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Roslindale': most models were scored on 41 cells, but — 42 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/Roxbury': most models were scored on 48 cells, but — 49 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/South Boston': most models were scored on 41 cells, but — 42 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- 'overall/South End': most models were scored on 48 cells, but — 49 cells: dualtopo/post_covid, dualtopo_fullhistory/full, dualtopo_no_bg/post_covid. A horizon-1-only model keeps one extra forecast origin, so its errors are averaged over slightly different weeks.
- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_rt, gnn_uniform, lstm). Differences here are not purely model quality.
