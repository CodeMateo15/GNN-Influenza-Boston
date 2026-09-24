# Per-neighborhood leaderboard — horizon 2

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* them -- Charlestown has 14 fewer scored weeks than the best-covered node (35 against 49) -- so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_st | 14 | 14 | 4 |
| lstm | 0 | 0 | 2 |
| persistence | 0 | 0 | 1 |
| seasonal_naive | 0 | 0 | 2 |
| xgboost | 0 | 0 | 5 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_st (post_covid)`: Allston, BackBay+, Charles., Dorchest., E.Boston, Fenway, HydePark, JP, Mattapan, Roslind., Roxbury, S.Boston, S.End, W.Roxbury
- **Flu season (Oct–Mar)** — `gnn_st (post_covid)`: Allston, BackBay+, Charles., Dorchest., E.Boston, Fenway, HydePark, JP, Mattapan, Roslind., Roxbury, S.Boston, S.End, W.Roxbury
- **Off-season (Apr–Sep)** — `gnn_st (post_covid)`: Allston, Charles., E.Boston, HydePark; `lstm (post_covid)`: S.Boston, W.Roxbury; `persistence (exclude_covid)`: Mattapan; `seasonal_naive (exclude_covid)`: Dorchest., Roxbury; `xgboost (post_covid)`: BackBay+, Fenway, JP, Roslind., S.End

`gnn_st (post_covid)` wins 14 of 14 neighborhoods. `gnn_st (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 31.026 | 49.932 | 17.721 | 0.838 | 91.837 |
| arima | post_covid | 35.619 | 95.828 | 23.673 | 0.777 | 93.878 |
| arima | exclude_covid | 35.798 | 106.740 | 24.376 | 0.775 | 93.878 |
| xgboost | post_covid | 35.854 | 78.575 | 22.670 | 0.763 | 97.959 |
| persistence | exclude_covid | 41.955 | 55.854 | 23.388 | 0.706 | 87.755 |
| persistence | post_covid | 41.955 | 55.854 | 23.388 | 0.706 | 87.755 |
| lstm | post_covid | 42.637 | 74.428 | 24.992 | 0.671 | 87.755 |
| gat | post_covid | 53.696 | 156.145 | 38.249 | 0.377 | 77.551 |
| lstm | exclude_covid | 54.278 | 76.524 | 28.926 | 0.631 | 87.755 |
| dualtopo | post_covid | 56.639 | 252.980 | 42.951 | -0.384 | 57.143 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 41.385 | 35.473 | 25.898 | 0.783 | 84.615 |
| arima | exclude_covid | 45.508 | 47.631 | 30.276 | 0.728 | 88.462 |
| arima | post_covid | 45.927 | 45.470 | 30.458 | 0.728 | 88.462 |
| xgboost | post_covid | 47.826 | 54.299 | 33.143 | 0.652 | 96.154 |
| persistence | exclude_covid | 56.416 | 45.427 | 35.510 | 0.608 | 80.769 |
| persistence | post_covid | 56.416 | 45.427 | 35.510 | 0.608 | 80.769 |
| lstm | post_covid | 57.329 | 49.005 | 37.337 | 0.581 | 76.923 |
| dualtopo | post_covid | 63.937 | 80.111 | 40.759 | -0.138 | 73.077 |
| gat | post_covid | 69.306 | 77.874 | 49.780 | 0.181 | 69.231 |
| lstm | exclude_covid | 73.091 | 54.618 | 43.480 | 0.537 | 76.923 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| gnn_st | post_covid | 10.705 | 66.278 | 8.478 | 0.843 | 100.000 |
| persistence | exclude_covid | 12.332 | 67.640 | 9.685 | 0.788 | 95.652 |
| persistence | post_covid | 12.332 | 67.640 | 9.685 | 0.788 | 95.652 |
| xgboost | post_covid | 12.373 | 106.018 | 10.830 | 0.855 | 100.000 |
| lstm | post_covid | 12.557 | 103.167 | 11.037 | 0.805 | 100.000 |
| lstm | exclude_covid | 15.407 | 101.288 | 12.473 | 0.824 | 100.000 |
| arima | post_covid | 17.847 | 152.754 | 16.002 | 0.684 | 100.000 |
| arima | exclude_covid | 19.721 | 173.558 | 17.705 | 0.689 | 100.000 |
| gat | post_covid | 26.698 | 244.625 | 25.213 | 0.708 | 86.957 |
| dualtopo | post_covid | 47.045 | 448.396 | 45.429 | -0.808 | 39.130 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 33.038 | 60.698 | 18.520 | 0.773 | 89.796 |
| xgboost | post_covid | 35.107 | 74.916 | 22.133 | 0.716 | 97.959 |
| lstm | post_covid | 38.168 | 58.915 | 22.186 | 0.662 | 87.755 |
| arima | post_covid | 39.165 | 102.880 | 23.377 | 0.662 | 93.878 |
| arima | exclude_covid | 39.202 | 118.012 | 24.667 | 0.661 | 91.837 |
| persistence | exclude_covid | 41.657 | 66.599 | 23.727 | 0.655 | 89.796 |
| persistence | post_covid | 41.657 | 66.599 | 23.727 | 0.655 | 89.796 |
| lstm | exclude_covid | 45.700 | 74.079 | 26.175 | 0.627 | 85.714 |
| gat | post_covid | 49.404 | 147.803 | 32.835 | 0.345 | 75.510 |
| dualtopo | post_covid | 51.156 | 231.030 | 37.547 | -0.332 | 65.306 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 44.328 | 50.915 | 27.739 | 0.704 | 80.769 |
| xgboost | post_covid | 47.043 | 60.722 | 32.990 | 0.607 | 96.154 |
| arima | exclude_covid | 50.900 | 63.149 | 32.843 | 0.587 | 84.615 |
| lstm | post_covid | 51.084 | 45.746 | 32.898 | 0.567 | 76.923 |
| arima | post_covid | 51.677 | 59.721 | 32.582 | 0.584 | 88.462 |
| persistence | exclude_covid | 56.000 | 61.702 | 37.300 | 0.554 | 88.462 |
| persistence | post_covid | 56.000 | 61.702 | 37.300 | 0.554 | 88.462 |
| dualtopo | post_covid | 60.303 | 89.453 | 38.712 | -0.078 | 73.077 |
| lstm | exclude_covid | 61.053 | 56.044 | 38.690 | 0.533 | 73.077 |
| gat | post_covid | 64.664 | 84.936 | 44.906 | 0.161 | 61.538 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| gnn_st | post_covid | 10.203 | 71.758 | 8.098 | 0.736 | 100.000 |
| xgboost | post_covid | 11.141 | 90.961 | 9.861 | 0.682 | 100.000 |
| persistence | exclude_covid | 12.327 | 72.136 | 8.383 | 0.644 | 91.304 |
| persistence | post_covid | 12.327 | 72.136 | 8.383 | 0.644 | 91.304 |
| lstm | post_covid | 12.395 | 73.803 | 10.076 | 0.691 | 100.000 |
| lstm | exclude_covid | 15.352 | 94.466 | 12.027 | 0.706 | 100.000 |
| arima | post_covid | 15.783 | 151.669 | 12.972 | 0.662 | 100.000 |
| arima | exclude_covid | 18.583 | 180.032 | 15.425 | 0.608 | 100.000 |
| gat | post_covid | 21.750 | 218.871 | 19.189 | 0.478 | 91.304 |
| dualtopo | post_covid | 38.268 | 391.073 | 36.230 | -0.646 | 56.522 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 23.929 | 69.791 | 15.539 | 0.789 | 85.714 |
| lstm | post_covid | 27.654 | 68.823 | 16.471 | 0.743 | 88.095 |
| lstm | exclude_covid | 27.753 | 66.960 | 16.787 | 0.706 | 78.571 |
| xgboost | post_covid | 29.269 | 74.394 | 17.032 | 0.745 | 95.238 |
| arima | post_covid | 33.967 | 130.086 | 23.334 | 0.592 | 88.095 |
| arima | exclude_covid | 34.268 | 112.558 | 22.727 | 0.510 | 90.476 |
| persistence | exclude_covid | 36.145 | 92.139 | 22.529 | 0.570 | 78.571 |
| persistence | post_covid | 36.145 | 92.139 | 22.529 | 0.570 | 78.571 |
| gat | post_covid | 36.468 | 122.030 | 22.635 | 0.365 | 80.952 |
| dualtopo | post_covid | 38.808 | 163.069 | 25.769 | -0.264 | 90.476 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 29.516 | 74.570 | 20.713 | 0.765 | 84.615 |
| lstm | exclude_covid | 34.481 | 67.806 | 22.339 | 0.669 | 69.231 |
| lstm | post_covid | 34.533 | 68.633 | 22.336 | 0.710 | 80.769 |
| xgboost | post_covid | 36.662 | 79.497 | 23.541 | 0.724 | 92.308 |
| arima | post_covid | 41.618 | 118.630 | 29.984 | 0.568 | 80.769 |
| arima | exclude_covid | 42.302 | 95.090 | 29.148 | 0.463 | 84.615 |
| persistence | exclude_covid | 45.027 | 105.865 | 31.369 | 0.517 | 73.077 |
| persistence | post_covid | 45.027 | 105.865 | 31.369 | 0.517 | 73.077 |
| gat | post_covid | 45.484 | 120.103 | 30.121 | 0.259 | 69.231 |
| dualtopo | post_covid | 46.655 | 118.147 | 30.475 | -0.120 | 84.615 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 8.038 | 66.101 | 6.456 | 0.607 | 100.000 |
| lstm | post_covid | 8.338 | 69.131 | 6.940 | 0.512 | 100.000 |
| gnn_st | post_covid | 9.352 | 62.024 | 7.131 | 0.429 | 87.500 |
| lstm | exclude_covid | 9.477 | 65.584 | 7.765 | 0.513 | 93.750 |
| gat | post_covid | 11.372 | 125.160 | 10.472 | 0.461 | 100.000 |
| persistence | exclude_covid | 11.618 | 69.835 | 8.162 | 0.281 | 87.500 |
| persistence | post_covid | 11.618 | 69.835 | 8.162 | 0.281 | 87.500 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| arima | exclude_covid | 13.216 | 140.943 | 12.293 | 0.222 | 100.000 |
| arima | post_covid | 14.627 | 148.704 | 12.527 | 0.101 | 100.000 |
| dualtopo | post_covid | 20.404 | 236.068 | 18.123 | -0.577 | 100.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.004 | 69.949 | 10.497 | 0.850 | 97.959 |
| xgboost | post_covid | 20.291 | 95.140 | 13.142 | 0.782 | 97.959 |
| arima | post_covid | 20.917 | 100.715 | 13.217 | 0.763 | 95.918 |
| lstm | post_covid | 22.295 | 91.860 | 13.686 | 0.717 | 95.918 |
| arima | exclude_covid | 22.642 | 70.316 | 13.021 | 0.744 | 93.878 |
| persistence | exclude_covid | 24.086 | 66.633 | 13.929 | 0.716 | 93.878 |
| persistence | post_covid | 24.086 | 66.633 | 13.929 | 0.716 | 93.878 |
| lstm | exclude_covid | 26.075 | 64.686 | 14.370 | 0.723 | 89.796 |
| gat | post_covid | 29.108 | 144.196 | 19.641 | 0.442 | 87.755 |
| dualtopo | post_covid | 32.513 | 220.492 | 24.040 | -0.356 | 89.796 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 22.445 | 73.412 | 15.028 | 0.813 | 96.154 |
| arima | post_covid | 26.900 | 72.251 | 16.941 | 0.723 | 92.308 |
| xgboost | post_covid | 27.138 | 106.447 | 19.528 | 0.713 | 96.154 |
| lstm | post_covid | 29.571 | 73.382 | 19.343 | 0.648 | 92.308 |
| arima | exclude_covid | 30.008 | 59.311 | 18.905 | 0.690 | 88.462 |
| persistence | exclude_covid | 32.215 | 63.326 | 20.865 | 0.652 | 88.462 |
| persistence | post_covid | 32.215 | 63.326 | 20.865 | 0.652 | 88.462 |
| lstm | exclude_covid | 35.024 | 60.510 | 21.930 | 0.667 | 80.769 |
| gat | post_covid | 37.956 | 111.573 | 26.603 | 0.297 | 76.923 |
| dualtopo | post_covid | 39.144 | 131.093 | 25.945 | -0.161 | 80.769 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.678 | 82.358 | 5.923 | 0.469 | 100.000 |
| gnn_st | post_covid | 6.820 | 66.035 | 5.376 | 0.525 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| lstm | exclude_covid | 7.866 | 69.407 | 5.824 | 0.587 | 100.000 |
| persistence | exclude_covid | 7.924 | 70.371 | 6.087 | 0.412 | 100.000 |
| persistence | post_covid | 7.924 | 70.371 | 6.087 | 0.412 | 100.000 |
| lstm | post_covid | 8.396 | 112.747 | 7.291 | 0.596 | 100.000 |
| arima | exclude_covid | 8.613 | 82.755 | 6.368 | 0.380 | 100.000 |
| arima | post_covid | 10.684 | 132.891 | 9.009 | 0.347 | 100.000 |
| gat | post_covid | 13.284 | 181.073 | 11.770 | 0.436 | 100.000 |
| dualtopo | post_covid | 22.801 | 321.552 | 21.886 | -0.523 | 100.000 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 16.741 | 59.117 | 9.160 | 0.668 | 94.286 |
| lstm | post_covid | 18.551 | 63.642 | 10.378 | 0.541 | 94.286 |
| xgboost | post_covid | 18.760 | 75.765 | 11.278 | 0.556 | 94.286 |
| lstm | exclude_covid | 20.283 | 71.542 | 11.110 | 0.466 | 88.571 |
| arima | post_covid | 20.661 | 92.903 | 12.278 | 0.365 | 94.286 |
| gat | post_covid | 21.768 | 92.463 | 13.239 | 0.248 | 91.429 |
| dualtopo | post_covid | 21.938 | 118.760 | 14.045 | -0.216 | 88.571 |
| persistence | exclude_covid | 22.776 | 76.874 | 12.360 | 0.464 | 94.286 |
| persistence | post_covid | 22.776 | 76.874 | 12.360 | 0.464 | 94.286 |
| arima | exclude_covid | 22.799 | 90.996 | 13.073 | 0.299 | 94.286 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 21.316 | 73.129 | 12.882 | 0.622 | 90.476 |
| lstm | post_covid | 23.642 | 73.819 | 14.904 | 0.476 | 90.476 |
| xgboost | post_covid | 23.914 | 98.542 | 16.234 | 0.480 | 90.476 |
| lstm | exclude_covid | 25.882 | 85.781 | 16.012 | 0.392 | 80.952 |
| arima | post_covid | 26.137 | 101.203 | 16.902 | 0.280 | 90.476 |
| dualtopo | post_covid | 27.065 | 108.755 | 17.363 | -0.045 | 80.952 |
| gat | post_covid | 27.744 | 108.497 | 18.957 | 0.109 | 85.714 |
| arima | exclude_covid | 28.866 | 97.139 | 17.942 | 0.224 | 90.476 |
| persistence | exclude_covid | 28.952 | 97.493 | 17.910 | 0.401 | 90.476 |
| persistence | post_covid | 28.952 | 97.493 | 17.910 | 0.401 | 90.476 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.377 | 38.098 | 3.578 | 0.631 | 100.000 |
| lstm | post_covid | 4.677 | 48.376 | 3.589 | 0.574 | 100.000 |
| xgboost | post_covid | 4.691 | 41.600 | 3.845 | 0.483 | 100.000 |
| lstm | exclude_covid | 4.863 | 50.182 | 3.758 | 0.529 | 100.000 |
| gat | post_covid | 5.479 | 68.410 | 4.663 | 0.519 | 100.000 |
| persistence | exclude_covid | 6.293 | 45.947 | 4.036 | 0.289 | 100.000 |
| persistence | post_covid | 6.293 | 45.947 | 4.036 | 0.289 | 100.000 |
| arima | post_covid | 6.516 | 80.454 | 5.343 | 0.277 | 100.000 |
| arima | exclude_covid | 7.047 | 81.782 | 5.769 | 0.115 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| dualtopo | post_covid | 10.217 | 133.768 | 9.068 | -0.534 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 11.154 | 80.508 | 8.251 | 0.888 | 100.000 |
| lstm | post_covid | 15.127 | 99.008 | 10.486 | 0.788 | 95.745 |
| lstm | exclude_covid | 16.611 | 83.802 | 10.296 | 0.772 | 93.617 |
| arima | post_covid | 17.456 | 130.553 | 12.170 | 0.663 | 95.745 |
| arima | exclude_covid | 17.459 | 120.047 | 11.408 | 0.669 | 95.745 |
| persistence | exclude_covid | 18.550 | 69.059 | 10.362 | 0.664 | 95.745 |
| persistence | post_covid | 18.550 | 69.059 | 10.362 | 0.664 | 95.745 |
| xgboost | post_covid | 19.440 | 75.289 | 11.491 | 0.616 | 95.745 |
| gat | post_covid | 22.274 | 195.900 | 17.756 | 0.505 | 93.617 |
| dualtopo | post_covid | 25.200 | 302.048 | 21.418 | -0.375 | 93.617 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.953 | 58.598 | 10.832 | 0.867 | 100.000 |
| lstm | post_covid | 18.233 | 66.385 | 12.933 | 0.755 | 92.308 |
| lstm | exclude_covid | 20.412 | 57.827 | 13.103 | 0.741 | 88.462 |
| arima | post_covid | 21.774 | 70.729 | 14.915 | 0.592 | 92.308 |
| arima | exclude_covid | 22.087 | 67.839 | 14.415 | 0.606 | 92.308 |
| persistence | exclude_covid | 24.428 | 52.898 | 15.238 | 0.594 | 92.308 |
| persistence | post_covid | 24.428 | 52.898 | 15.238 | 0.594 | 92.308 |
| xgboost | post_covid | 25.595 | 61.845 | 16.742 | 0.518 | 96.154 |
| dualtopo | post_covid | 26.772 | 146.767 | 20.332 | -0.213 | 88.462 |
| gat | post_covid | 27.018 | 119.473 | 20.890 | 0.386 | 88.462 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 5.598 | 89.067 | 4.324 | 0.447 | 100.000 |
| persistence | post_covid | 5.598 | 89.067 | 4.324 | 0.447 | 100.000 |
| xgboost | post_covid | 5.892 | 91.935 | 4.990 | 0.540 | 95.238 |
| gnn_st | post_covid | 6.114 | 107.635 | 5.056 | 0.528 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| arima | exclude_covid | 8.842 | 184.684 | 7.684 | 0.398 | 100.000 |
| arima | post_covid | 9.744 | 204.620 | 8.770 | 0.448 | 100.000 |
| lstm | post_covid | 10.028 | 139.399 | 7.457 | 0.604 | 100.000 |
| lstm | exclude_covid | 10.087 | 115.963 | 6.820 | 0.601 | 100.000 |
| gat | post_covid | 14.373 | 290.525 | 13.876 | 0.642 | 100.000 |
| dualtopo | post_covid | 23.107 | 494.300 | 22.762 | -0.630 | 100.000 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.376 | 72.411 | 7.792 | 0.779 | 95.652 |
| lstm | post_covid | 15.598 | 89.346 | 9.450 | 0.649 | 95.652 |
| xgboost | post_covid | 15.618 | 85.972 | 9.152 | 0.637 | 97.826 |
| arima | post_covid | 16.840 | 130.844 | 10.873 | 0.585 | 97.826 |
| lstm | exclude_covid | 18.148 | 82.126 | 10.214 | 0.629 | 91.304 |
| persistence | exclude_covid | 18.705 | 79.483 | 10.889 | 0.574 | 93.478 |
| persistence | post_covid | 18.705 | 79.483 | 10.889 | 0.574 | 95.652 |
| dualtopo | post_covid | 21.121 | 256.170 | 16.098 | -0.222 | 91.304 |
| gat | post_covid | 22.010 | 178.937 | 14.667 | 0.249 | 86.957 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| arima | exclude_covid | 136.748 | 319.274 | 50.229 | 0.367 | 65.217 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.741 | 72.871 | 11.427 | 0.723 | 92.000 |
| lstm | post_covid | 20.555 | 75.135 | 13.480 | 0.562 | 92.000 |
| xgboost | post_covid | 20.836 | 85.221 | 13.806 | 0.521 | 96.000 |
| arima | post_covid | 21.682 | 86.465 | 14.270 | 0.501 | 96.000 |
| lstm | exclude_covid | 23.667 | 67.420 | 14.253 | 0.558 | 84.000 |
| dualtopo | post_covid | 24.338 | 110.822 | 16.317 | 0.032 | 84.000 |
| persistence | exclude_covid | 24.842 | 90.586 | 16.808 | 0.479 | 88.000 |
| persistence | post_covid | 24.842 | 90.586 | 16.808 | 0.479 | 92.000 |
| gat | post_covid | 28.528 | 125.674 | 19.635 | 0.061 | 76.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| arima | exclude_covid | 185.389 | 523.801 | 88.180 | 0.267 | 52.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.150 | 71.864 | 3.464 | 0.676 | 100.000 |
| xgboost | post_covid | 4.182 | 86.866 | 3.612 | 0.551 | 100.000 |
| lstm | post_covid | 5.477 | 106.262 | 4.652 | 0.621 | 100.000 |
| persistence | exclude_covid | 5.633 | 66.266 | 3.843 | 0.592 | 100.000 |
| persistence | post_covid | 5.633 | 66.266 | 3.843 | 0.592 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| arima | exclude_covid | 6.826 | 75.790 | 5.048 | 0.421 | 80.952 |
| lstm | exclude_covid | 7.390 | 99.634 | 5.407 | 0.614 | 100.000 |
| arima | post_covid | 7.843 | 183.675 | 6.828 | 0.544 | 100.000 |
| gat | post_covid | 9.610 | 242.345 | 8.753 | 0.406 | 100.000 |
| dualtopo | post_covid | 16.491 | 429.202 | 15.837 | -0.634 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.862 | 55.208 | 5.731 | 0.840 | 93.878 |
| lstm | post_covid | 12.822 | 73.746 | 7.546 | 0.711 | 95.918 |
| xgboost | post_covid | 13.564 | 79.725 | 8.127 | 0.667 | 100.000 |
| lstm | exclude_covid | 13.597 | 59.265 | 7.785 | 0.682 | 91.837 |
| arima | post_covid | 14.080 | 104.047 | 9.011 | 0.638 | 95.918 |
| arima | exclude_covid | 14.135 | 85.932 | 8.336 | 0.634 | 95.918 |
| persistence | exclude_covid | 15.661 | 71.255 | 8.759 | 0.628 | 93.878 |
| persistence | post_covid | 15.661 | 71.255 | 8.759 | 0.628 | 95.918 |
| gat | post_covid | 16.788 | 127.727 | 10.885 | 0.403 | 89.796 |
| dualtopo | post_covid | 18.276 | 191.757 | 12.884 | -0.342 | 89.796 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.173 | 49.471 | 8.497 | 0.792 | 88.462 |
| lstm | post_covid | 17.190 | 52.293 | 11.352 | 0.640 | 92.308 |
| xgboost | post_covid | 18.153 | 63.166 | 11.938 | 0.551 | 100.000 |
| arima | post_covid | 18.290 | 62.609 | 12.207 | 0.552 | 92.308 |
| lstm | exclude_covid | 18.366 | 52.636 | 12.235 | 0.608 | 84.615 |
| arima | exclude_covid | 18.875 | 62.115 | 12.265 | 0.530 | 92.308 |
| persistence | exclude_covid | 21.138 | 71.836 | 13.665 | 0.521 | 88.462 |
| persistence | post_covid | 21.138 | 71.836 | 13.665 | 0.521 | 92.308 |
| gat | post_covid | 22.118 | 75.621 | 14.943 | 0.233 | 80.769 |
| dualtopo | post_covid | 22.284 | 71.488 | 14.041 | -0.125 | 80.769 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.322 | 61.694 | 2.605 | 0.757 | 100.000 |
| lstm | exclude_covid | 3.543 | 66.759 | 2.754 | 0.740 | 100.000 |
| lstm | post_covid | 4.027 | 97.996 | 3.243 | 0.719 | 100.000 |
| persistence | exclude_covid | 4.175 | 70.597 | 3.213 | 0.719 | 100.000 |
| persistence | post_covid | 4.175 | 70.597 | 3.213 | 0.719 | 100.000 |
| xgboost | post_covid | 4.410 | 98.445 | 3.818 | 0.610 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| arima | exclude_covid | 4.785 | 112.856 | 3.896 | 0.729 | 100.000 |
| arima | post_covid | 6.648 | 150.890 | 5.398 | 0.516 | 100.000 |
| gat | post_covid | 6.890 | 186.630 | 6.298 | 0.634 | 100.000 |
| dualtopo | post_covid | 12.259 | 327.714 | 11.575 | -0.656 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.350 | 69.772 | 8.078 | 0.674 | 95.000 |
| xgboost | post_covid | 15.729 | 72.309 | 8.549 | 0.628 | 97.500 |
| lstm | post_covid | 15.888 | 57.571 | 8.707 | 0.607 | 92.500 |
| lstm | exclude_covid | 16.609 | 62.730 | 8.965 | 0.553 | 90.000 |
| arima | exclude_covid | 17.955 | 101.543 | 10.435 | 0.408 | 92.500 |
| gat | post_covid | 18.711 | 82.550 | 10.576 | 0.301 | 90.000 |
| arima | post_covid | 18.723 | 103.324 | 10.730 | 0.405 | 92.500 |
| dualtopo | post_covid | 19.306 | 109.436 | 10.765 | -0.248 | 92.500 |
| persistence | exclude_covid | 20.649 | 97.450 | 12.092 | 0.426 | 90.000 |
| persistence | post_covid | 20.649 | 97.450 | 12.092 | 0.426 | 90.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.789 | 75.980 | 10.630 | 0.635 | 92.000 |
| xgboost | post_covid | 19.613 | 78.899 | 11.415 | 0.591 | 96.000 |
| lstm | post_covid | 19.866 | 56.676 | 11.920 | 0.563 | 88.000 |
| lstm | exclude_covid | 20.723 | 65.012 | 12.216 | 0.502 | 84.000 |
| arima | exclude_covid | 22.146 | 86.593 | 13.204 | 0.352 | 88.000 |
| arima | post_covid | 23.126 | 90.555 | 13.524 | 0.358 | 88.000 |
| gat | post_covid | 23.330 | 77.031 | 14.431 | 0.203 | 84.000 |
| dualtopo | post_covid | 23.557 | 76.517 | 12.784 | -0.157 | 88.000 |
| persistence | exclude_covid | 25.686 | 103.436 | 16.132 | 0.370 | 84.000 |
| persistence | post_covid | 25.686 | 103.436 | 16.132 | 0.370 | 84.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.916 | 59.062 | 3.352 | 0.323 | 100.000 |
| xgboost | post_covid | 4.312 | 61.326 | 3.772 | 0.202 | 100.000 |
| lstm | exclude_covid | 4.457 | 58.928 | 3.547 | 0.320 | 100.000 |
| gnn_st | post_covid | 4.658 | 59.425 | 3.825 | 0.170 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| gat | post_covid | 5.144 | 91.749 | 4.150 | 0.208 | 100.000 |
| persistence | exclude_covid | 6.116 | 87.474 | 5.360 | -0.052 | 100.000 |
| persistence | post_covid | 6.116 | 87.474 | 5.360 | -0.052 | 100.000 |
| arima | exclude_covid | 6.500 | 126.460 | 5.820 | -0.266 | 100.000 |
| arima | post_covid | 6.591 | 124.606 | 6.072 | -0.292 | 100.000 |
| dualtopo | post_covid | 8.308 | 164.300 | 7.399 | -0.254 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.132 | 55.882 | 4.381 | 0.844 | 97.619 |
| xgboost | post_covid | 8.196 | 79.942 | 5.503 | 0.801 | 100.000 |
| arima | post_covid | 8.748 | 93.421 | 5.835 | 0.752 | 100.000 |
| arima | exclude_covid | 8.925 | 91.313 | 5.956 | 0.738 | 100.000 |
| lstm | post_covid | 9.936 | 57.083 | 5.888 | 0.682 | 97.619 |
| persistence | exclude_covid | 10.284 | 53.790 | 5.874 | 0.702 | 95.238 |
| persistence | post_covid | 10.284 | 53.790 | 5.874 | 0.702 | 95.238 |
| lstm | exclude_covid | 12.025 | 72.518 | 6.881 | 0.674 | 92.857 |
| gat | post_covid | 12.615 | 112.456 | 8.502 | 0.401 | 92.857 |
| dualtopo | post_covid | 13.216 | 184.262 | 9.413 | -0.347 | 90.476 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.862 | 60.556 | 5.920 | 0.816 | 96.000 |
| xgboost | post_covid | 10.318 | 85.101 | 7.561 | 0.759 | 100.000 |
| arima | post_covid | 10.658 | 74.222 | 7.146 | 0.718 | 100.000 |
| arima | exclude_covid | 10.932 | 74.317 | 7.476 | 0.694 | 100.000 |
| lstm | post_covid | 12.640 | 61.061 | 8.424 | 0.618 | 96.000 |
| persistence | exclude_covid | 12.941 | 55.862 | 8.264 | 0.644 | 92.000 |
| persistence | post_covid | 12.941 | 55.862 | 8.264 | 0.644 | 92.000 |
| lstm | exclude_covid | 15.314 | 76.434 | 9.910 | 0.618 | 88.000 |
| dualtopo | post_covid | 15.603 | 135.150 | 10.325 | -0.199 | 84.000 |
| gat | post_covid | 15.924 | 107.316 | 11.772 | 0.263 | 88.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 2.993 | 51.234 | 2.158 | 0.454 | 100.000 |
| xgboost | post_covid | 3.066 | 72.355 | 2.476 | 0.500 | 100.000 |
| gnn_st | post_covid | 3.192 | 49.010 | 2.117 | 0.464 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| lstm | exclude_covid | 3.523 | 66.759 | 2.427 | 0.458 | 100.000 |
| persistence | exclude_covid | 3.874 | 50.743 | 2.359 | 0.321 | 100.000 |
| persistence | post_covid | 3.874 | 50.743 | 2.359 | 0.321 | 100.000 |
| gat | post_covid | 4.501 | 120.015 | 3.693 | 0.446 | 100.000 |
| arima | exclude_covid | 4.590 | 116.306 | 3.721 | 0.333 | 100.000 |
| arima | post_covid | 4.694 | 121.656 | 3.906 | 0.268 | 100.000 |
| dualtopo | post_covid | 8.574 | 256.487 | 8.072 | -0.411 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.529 | 52.518 | 4.306 | 0.854 | 97.826 |
| xgboost | post_covid | 8.648 | 68.782 | 5.327 | 0.721 | 100.000 |
| arima | exclude_covid | 9.341 | 90.803 | 5.590 | 0.670 | 97.826 |
| arima | post_covid | 9.405 | 100.631 | 5.789 | 0.659 | 97.826 |
| lstm | post_covid | 9.457 | 86.323 | 6.079 | 0.694 | 97.826 |
| lstm | exclude_covid | 9.726 | 75.295 | 6.249 | 0.707 | 97.826 |
| persistence | exclude_covid | 10.448 | 58.464 | 5.574 | 0.650 | 97.826 |
| persistence | post_covid | 10.448 | 58.464 | 5.574 | 0.650 | 97.826 |
| gat | post_covid | 11.054 | 117.098 | 7.152 | 0.473 | 93.478 |
| dualtopo | post_covid | 12.448 | 189.389 | 8.441 | -0.450 | 93.478 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.317 | 49.143 | 5.989 | 0.811 | 96.154 |
| xgboost | post_covid | 11.263 | 54.820 | 7.542 | 0.604 | 100.000 |
| arima | exclude_covid | 11.924 | 56.713 | 7.154 | 0.569 | 96.154 |
| arima | post_covid | 11.930 | 59.914 | 7.244 | 0.558 | 96.154 |
| lstm | post_covid | 12.245 | 56.388 | 8.475 | 0.634 | 96.154 |
| lstm | exclude_covid | 12.600 | 57.731 | 8.845 | 0.652 | 96.154 |
| persistence | exclude_covid | 13.538 | 60.255 | 7.950 | 0.536 | 96.154 |
| persistence | post_covid | 13.538 | 60.255 | 7.950 | 0.536 | 96.154 |
| gat | post_covid | 14.184 | 75.402 | 9.724 | 0.326 | 88.462 |
| dualtopo | post_covid | 14.944 | 78.749 | 9.214 | -0.261 | 88.462 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.661 | 86.932 | 2.448 | 0.680 | 100.000 |
| gnn_st | post_covid | 2.848 | 56.906 | 2.118 | 0.621 | 100.000 |
| lstm | post_covid | 3.283 | 125.238 | 2.964 | 0.532 | 100.000 |
| lstm | exclude_covid | 3.345 | 98.128 | 2.874 | 0.545 | 100.000 |
| persistence | exclude_covid | 3.577 | 56.135 | 2.485 | 0.548 | 100.000 |
| persistence | post_covid | 3.577 | 56.135 | 2.485 | 0.548 | 100.000 |
| arima | exclude_covid | 3.982 | 135.120 | 3.558 | 0.520 | 100.000 |
| arima | post_covid | 4.292 | 153.564 | 3.897 | 0.477 | 100.000 |
| gat | post_covid | 4.419 | 171.303 | 3.807 | 0.462 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| dualtopo | post_covid | 8.128 | 333.222 | 7.437 | -0.682 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.410 | 82.242 | 4.994 | 0.821 | 97.727 |
| lstm | post_covid | 9.381 | 83.037 | 6.178 | 0.711 | 95.455 |
| arima | post_covid | 10.057 | 136.185 | 7.339 | 0.633 | 97.727 |
| xgboost | post_covid | 10.133 | 108.065 | 7.162 | 0.679 | 95.455 |
| lstm | exclude_covid | 10.387 | 75.621 | 6.393 | 0.685 | 95.455 |
| arima | exclude_covid | 11.037 | 113.343 | 7.423 | 0.619 | 95.455 |
| persistence | exclude_covid | 11.313 | 93.912 | 7.400 | 0.619 | 93.182 |
| persistence | post_covid | 11.313 | 93.912 | 7.400 | 0.619 | 95.455 |
| gat | post_covid | 11.842 | 126.095 | 8.059 | 0.440 | 93.182 |
| dualtopo | post_covid | 12.982 | 210.822 | 9.416 | -0.284 | 90.909 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.665 | 103.381 | 7.569 | 0.769 | 96.000 |
| lstm | post_covid | 12.199 | 82.443 | 9.117 | 0.653 | 92.000 |
| arima | post_covid | 12.760 | 133.236 | 9.831 | 0.545 | 96.000 |
| xgboost | post_covid | 13.147 | 133.908 | 10.757 | 0.580 | 100.000 |
| lstm | exclude_covid | 13.524 | 84.044 | 9.674 | 0.623 | 92.000 |
| arima | exclude_covid | 14.347 | 130.026 | 10.934 | 0.530 | 92.000 |
| persistence | exclude_covid | 14.820 | 127.042 | 11.532 | 0.515 | 88.000 |
| persistence | post_covid | 14.820 | 127.042 | 11.532 | 0.515 | 92.000 |
| gat | post_covid | 15.239 | 110.654 | 11.141 | 0.293 | 88.000 |
| dualtopo | post_covid | 15.465 | 132.828 | 10.339 | -0.065 | 84.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.060 | 54.427 | 1.606 | 0.777 | 100.000 |
| persistence | exclude_covid | 2.721 | 50.321 | 1.963 | 0.753 | 100.000 |
| persistence | post_covid | 2.721 | 50.321 | 1.963 | 0.753 | 100.000 |
| lstm | post_covid | 2.822 | 83.819 | 2.312 | 0.700 | 100.000 |
| lstm | exclude_covid | 3.028 | 64.539 | 2.077 | 0.687 | 100.000 |
| xgboost | post_covid | 3.217 | 74.062 | 2.433 | 0.467 | 89.474 |
| arima | exclude_covid | 3.362 | 91.391 | 2.803 | 0.654 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gat | post_covid | 4.379 | 146.413 | 4.005 | 0.680 | 100.000 |
| arima | post_covid | 4.470 | 140.065 | 4.061 | 0.637 | 100.000 |
| dualtopo | post_covid | 8.694 | 313.447 | 8.202 | -0.724 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.380 | 77.644 | 4.870 | 0.844 | 100.000 |
| lstm | post_covid | 9.518 | 82.763 | 5.613 | 0.732 | 97.826 |
| lstm | exclude_covid | 10.069 | 84.865 | 6.041 | 0.688 | 95.652 |
| arima | exclude_covid | 10.635 | 137.031 | 7.072 | 0.641 | 97.826 |
| xgboost | post_covid | 10.802 | 86.591 | 6.238 | 0.640 | 97.826 |
| arima | post_covid | 10.859 | 124.492 | 6.944 | 0.620 | 97.826 |
| persistence | exclude_covid | 11.661 | 92.158 | 7.198 | 0.643 | 95.652 |
| persistence | post_covid | 11.661 | 92.158 | 7.198 | 0.643 | 95.652 |
| gat | post_covid | 12.822 | 157.476 | 8.597 | 0.390 | 93.478 |
| dualtopo | post_covid | 13.877 | 225.539 | 9.876 | -0.326 | 91.304 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.863 | 83.044 | 7.338 | 0.808 | 100.000 |
| lstm | post_covid | 12.889 | 82.642 | 8.670 | 0.661 | 95.833 |
| lstm | exclude_covid | 13.543 | 89.449 | 9.311 | 0.611 | 91.667 |
| arima | exclude_covid | 14.022 | 112.196 | 9.763 | 0.557 | 95.833 |
| arima | post_covid | 14.505 | 108.867 | 10.064 | 0.528 | 95.833 |
| xgboost | post_covid | 14.746 | 98.385 | 9.930 | 0.530 | 100.000 |
| persistence | exclude_covid | 15.853 | 100.455 | 11.317 | 0.560 | 91.667 |
| persistence | post_covid | 15.853 | 100.455 | 11.317 | 0.560 | 91.667 |
| gat | post_covid | 17.049 | 131.746 | 12.122 | 0.215 | 87.500 |
| dualtopo | post_covid | 17.240 | 136.008 | 11.172 | -0.063 | 83.333 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.599 | 73.726 | 2.211 | 0.683 | 95.455 |
| gnn_st | post_covid | 2.787 | 71.754 | 2.178 | 0.605 | 100.000 |
| lstm | post_covid | 2.858 | 82.895 | 2.278 | 0.719 | 100.000 |
| persistence | exclude_covid | 3.180 | 83.106 | 2.705 | 0.438 | 100.000 |
| persistence | post_covid | 3.180 | 83.106 | 2.705 | 0.438 | 100.000 |
| lstm | exclude_covid | 3.452 | 79.864 | 2.473 | 0.711 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| arima | post_covid | 4.128 | 141.538 | 3.542 | 0.466 | 100.000 |
| arima | exclude_covid | 4.688 | 164.124 | 4.135 | 0.411 | 100.000 |
| gat | post_covid | 5.165 | 185.545 | 4.752 | 0.638 | 100.000 |
| dualtopo | post_covid | 8.854 | 323.210 | 8.462 | -0.753 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.864 | 69.634 | 2.549 | 0.754 | 100.000 |
| lstm | post_covid | 4.065 | 82.597 | 2.845 | 0.665 | 100.000 |
| arima | post_covid | 4.339 | 106.083 | 3.253 | 0.638 | 100.000 |
| arima | exclude_covid | 4.483 | 117.129 | 3.466 | 0.624 | 100.000 |
| persistence | exclude_covid | 4.646 | 71.644 | 3.200 | 0.629 | 100.000 |
| persistence | post_covid | 4.646 | 71.644 | 3.200 | 0.629 | 100.000 |
| gat | post_covid | 5.170 | 115.796 | 3.965 | 0.528 | 100.000 |
| lstm | exclude_covid | 5.657 | 79.264 | 3.413 | 0.578 | 97.674 |
| dualtopo | post_covid | 5.724 | 172.641 | 4.923 | -0.531 | 100.000 |
| xgboost | post_covid | 7.290 | 81.219 | 4.930 | 0.494 | 93.023 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.608 | 42.516 | 3.151 | 0.652 | 100.000 |
| arima | post_covid | 4.727 | 47.947 | 3.308 | 0.507 | 100.000 |
| arima | exclude_covid | 4.736 | 51.880 | 3.388 | 0.498 | 100.000 |
| lstm | post_covid | 4.745 | 41.155 | 3.198 | 0.577 | 100.000 |
| dualtopo | post_covid | 5.529 | 75.338 | 4.355 | -0.390 | 100.000 |
| persistence | exclude_covid | 5.618 | 44.043 | 3.960 | 0.494 | 100.000 |
| persistence | post_covid | 5.618 | 44.043 | 3.960 | 0.494 | 100.000 |
| gat | post_covid | 5.952 | 61.675 | 4.497 | 0.383 | 100.000 |
| lstm | exclude_covid | 7.098 | 52.664 | 4.507 | 0.467 | 96.000 |
| xgboost | post_covid | 9.374 | 77.460 | 7.196 | 0.279 | 88.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.215 | 86.440 | 1.783 | 0.504 | 100.000 |
| gnn_st | post_covid | 2.485 | 107.298 | 1.714 | 0.394 | 100.000 |
| lstm | exclude_covid | 2.544 | 116.210 | 1.894 | 0.401 | 100.000 |
| persistence | exclude_covid | 2.782 | 109.979 | 2.144 | 0.256 | 100.000 |
| persistence | post_covid | 2.782 | 109.979 | 2.144 | 0.256 | 100.000 |
| lstm | post_covid | 2.866 | 140.154 | 2.355 | 0.346 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| arima | post_covid | 3.733 | 186.827 | 3.178 | 0.201 | 100.000 |
| gat | post_covid | 3.828 | 190.965 | 3.225 | 0.296 | 100.000 |
| arima | exclude_covid | 4.107 | 207.752 | 3.576 | 0.159 | 100.000 |
| dualtopo | post_covid | 5.984 | 307.784 | 5.713 | -0.296 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
