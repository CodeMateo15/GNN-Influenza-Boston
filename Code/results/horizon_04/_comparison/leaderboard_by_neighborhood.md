# Per-neighborhood leaderboard — horizon 4

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| xgboost | 9 | 9 | 5 |
| gnn_st | 5 | 5 | 5 |
| gat | 0 | 0 | 2 |
| seasonal_naive | 0 | 0 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_st (post_covid)`: BackBay+, Fenway, JP, Mattapan, Roxbury; `xgboost (post_covid)`: Allston, Charles., Dorchest., E.Boston, HydePark, Roslind., S.Boston, S.End, W.Roxbury
- **Flu season (Oct–Mar)** — `gnn_st (post_covid)`: BackBay+, Fenway, JP, Mattapan, Roxbury; `xgboost (post_covid)`: Allston, Charles., Dorchest., E.Boston, HydePark, Roslind., S.Boston, S.End, W.Roxbury
- **Off-season (Apr–Sep)** — `gat (post_covid)`: Charles., W.Roxbury; `gnn_st (post_covid)`: Allston, BackBay+, E.Boston, HydePark, S.Boston; `seasonal_naive (exclude_covid)`: Dorchest., Roxbury; `xgboost (post_covid)`: Fenway, JP, Mattapan, Roslind., S.End

`xgboost (post_covid)` wins 9 of 14 neighborhoods. `xgboost (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 42.143 | 75.988 | 25.751 | 0.643 | 97.959 |
| gnn_st | post_covid | 43.231 | 71.655 | 25.649 | 0.625 | 93.878 |
| lstm | post_covid | 52.892 | 90.447 | 32.250 | 0.425 | 85.714 |
| arima | post_covid | 56.091 | 191.089 | 41.293 | 0.325 | 93.878 |
| dualtopo | post_covid | 56.928 | 260.418 | 43.972 | 0.584 | 57.143 |
| arima | exclude_covid | 58.307 | 130.557 | 37.547 | 0.318 | 91.837 |
| gat | post_covid | 61.782 | 133.663 | 40.293 | 0.212 | 77.551 |
| lstm | exclude_covid | 62.856 | 112.116 | 39.410 | 0.324 | 75.510 |
| persistence | exclude_covid | 64.708 | 77.731 | 36.261 | 0.303 | 91.837 |
| persistence | post_covid | 64.708 | 77.731 | 36.261 | 0.303 | 91.837 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 56.746 | 54.335 | 39.145 | 0.448 | 96.154 |
| gnn_st | post_covid | 58.308 | 63.105 | 40.271 | 0.433 | 88.462 |
| dualtopo | post_covid | 63.474 | 83.191 | 41.326 | 0.345 | 73.077 |
| lstm | post_covid | 66.628 | 50.704 | 42.325 | 0.327 | 80.769 |
| arima | post_covid | 69.938 | 84.191 | 48.840 | 0.204 | 88.462 |
| arima | exclude_covid | 75.747 | 72.875 | 50.400 | 0.190 | 84.615 |
| lstm | exclude_covid | 81.081 | 74.619 | 55.069 | 0.169 | 65.385 |
| gat | post_covid | 82.850 | 89.619 | 60.292 | -0.091 | 57.692 |
| persistence | exclude_covid | 87.420 | 76.765 | 57.735 | 0.089 | 84.615 |
| persistence | post_covid | 87.420 | 76.765 | 57.735 | 0.089 | 84.615 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| gnn_st | post_covid | 11.767 | 81.321 | 9.121 | 0.799 | 100.000 |
| xgboost | post_covid | 11.985 | 100.466 | 10.611 | 0.802 | 100.000 |
| persistence | exclude_covid | 16.774 | 78.824 | 11.987 | 0.727 | 100.000 |
| persistence | post_covid | 16.774 | 78.824 | 11.987 | 0.727 | 100.000 |
| gat | post_covid | 19.301 | 183.452 | 17.685 | 0.778 | 100.000 |
| arima | exclude_covid | 27.509 | 195.763 | 23.017 | 0.524 | 100.000 |
| lstm | post_covid | 30.687 | 135.375 | 20.862 | 0.670 | 91.304 |
| lstm | exclude_covid | 31.391 | 154.503 | 21.709 | 0.647 | 86.957 |
| arima | post_covid | 34.255 | 311.929 | 32.762 | 0.651 | 100.000 |
| dualtopo | post_covid | 48.476 | 460.761 | 46.963 | 0.797 | 39.130 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 40.616 | 74.963 | 24.933 | 0.600 | 93.878 |
| xgboost | post_covid | 40.892 | 78.901 | 24.937 | 0.593 | 97.959 |
| lstm | post_covid | 47.069 | 74.241 | 26.809 | 0.416 | 89.796 |
| arima | post_covid | 49.007 | 164.906 | 32.867 | 0.341 | 95.918 |
| arima | exclude_covid | 49.636 | 197.304 | 35.765 | 0.340 | 93.878 |
| dualtopo | post_covid | 51.336 | 238.163 | 38.338 | 0.522 | 65.306 |
| gat | post_covid | 56.926 | 125.199 | 35.300 | 0.167 | 81.633 |
| lstm | exclude_covid | 58.201 | 93.014 | 36.277 | 0.339 | 75.510 |
| persistence | exclude_covid | 58.963 | 83.882 | 34.992 | 0.314 | 91.837 |
| persistence | post_covid | 58.963 | 83.882 | 34.992 | 0.314 | 91.837 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 54.564 | 69.012 | 37.717 | 0.434 | 88.462 |
| xgboost | post_covid | 54.865 | 66.908 | 37.344 | 0.413 | 96.154 |
| lstm | post_covid | 59.816 | 46.223 | 35.199 | 0.350 | 80.769 |
| dualtopo | post_covid | 59.877 | 92.806 | 39.127 | 0.275 | 73.077 |
| arima | exclude_covid | 60.217 | 87.202 | 39.773 | 0.228 | 88.462 |
| arima | post_covid | 61.944 | 79.324 | 39.623 | 0.212 | 92.308 |
| lstm | exclude_covid | 74.697 | 78.977 | 51.408 | 0.195 | 65.385 |
| gat | post_covid | 76.868 | 103.080 | 54.989 | -0.126 | 65.385 |
| persistence | exclude_covid | 79.131 | 80.738 | 53.385 | 0.130 | 84.615 |
| persistence | post_covid | 79.131 | 80.738 | 53.385 | 0.130 | 84.615 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| gnn_st | post_covid | 12.203 | 81.690 | 10.481 | 0.587 | 100.000 |
| xgboost | post_covid | 12.639 | 92.459 | 10.913 | 0.539 | 100.000 |
| gat | post_covid | 14.984 | 150.204 | 13.043 | 0.698 | 100.000 |
| persistence | exclude_covid | 18.119 | 87.435 | 14.200 | 0.415 | 100.000 |
| persistence | post_covid | 18.119 | 87.435 | 14.200 | 0.415 | 100.000 |
| lstm | post_covid | 25.989 | 105.914 | 17.324 | 0.570 | 100.000 |
| arima | post_covid | 27.912 | 261.652 | 25.229 | 0.363 | 100.000 |
| lstm | exclude_covid | 30.151 | 108.882 | 19.172 | 0.574 | 86.957 |
| arima | exclude_covid | 33.909 | 321.767 | 31.234 | 0.285 | 100.000 |
| dualtopo | post_covid | 39.516 | 402.479 | 37.446 | 0.654 | 56.522 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 31.408 | 83.392 | 17.856 | 0.621 | 95.238 |
| gnn_st | post_covid | 33.037 | 85.571 | 19.292 | 0.532 | 95.238 |
| lstm | post_covid | 35.051 | 75.209 | 19.970 | 0.464 | 88.095 |
| dualtopo | post_covid | 38.755 | 168.256 | 26.128 | 0.445 | 90.476 |
| lstm | exclude_covid | 39.610 | 100.014 | 24.233 | 0.319 | 83.333 |
| gat | post_covid | 42.689 | 132.778 | 24.873 | 0.102 | 80.952 |
| arima | post_covid | 42.984 | 160.756 | 28.581 | 0.122 | 90.476 |
| arima | exclude_covid | 47.059 | 123.301 | 27.943 | 0.110 | 90.476 |
| persistence | exclude_covid | 52.201 | 116.971 | 28.979 | 0.113 | 90.476 |
| persistence | post_covid | 52.201 | 116.971 | 28.979 | 0.113 | 90.476 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 39.388 | 94.859 | 24.845 | 0.558 | 92.308 |
| gnn_st | post_covid | 41.452 | 101.624 | 27.217 | 0.437 | 92.308 |
| lstm | post_covid | 42.699 | 64.648 | 24.966 | 0.500 | 80.769 |
| dualtopo | post_covid | 46.400 | 121.921 | 30.572 | 0.301 | 84.615 |
| lstm | exclude_covid | 48.914 | 110.750 | 32.533 | 0.234 | 73.077 |
| arima | post_covid | 52.944 | 140.648 | 37.048 | 0.054 | 84.615 |
| gat | post_covid | 53.853 | 158.344 | 35.671 | -0.086 | 69.231 |
| arima | exclude_covid | 58.660 | 113.156 | 36.675 | 0.033 | 84.615 |
| persistence | exclude_covid | 65.810 | 150.159 | 41.946 | -0.006 | 84.615 |
| persistence | post_covid | 65.810 | 150.159 | 41.946 | -0.006 | 84.615 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 8.273 | 64.759 | 6.499 | 0.556 | 100.000 |
| gat | post_covid | 8.419 | 91.234 | 7.327 | 0.634 | 100.000 |
| gnn_st | post_covid | 8.532 | 59.485 | 6.414 | 0.546 | 100.000 |
| persistence | exclude_covid | 10.735 | 63.039 | 7.906 | 0.468 | 100.000 |
| persistence | post_covid | 10.735 | 63.039 | 7.906 | 0.468 | 100.000 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| arima | exclude_covid | 14.880 | 139.788 | 13.754 | -0.133 | 100.000 |
| lstm | exclude_covid | 15.183 | 82.568 | 10.744 | 0.513 | 100.000 |
| lstm | post_covid | 16.196 | 92.372 | 11.851 | 0.552 | 100.000 |
| arima | post_covid | 17.175 | 193.433 | 14.821 | 0.306 | 100.000 |
| dualtopo | post_covid | 21.071 | 243.549 | 18.908 | 0.610 | 100.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 22.369 | 89.643 | 13.963 | 0.719 | 100.000 |
| gnn_st | post_covid | 23.891 | 90.721 | 15.022 | 0.669 | 97.959 |
| lstm | post_covid | 26.851 | 101.505 | 15.779 | 0.564 | 91.837 |
| arima | post_covid | 30.275 | 164.618 | 21.576 | 0.379 | 97.959 |
| dualtopo | post_covid | 32.591 | 227.090 | 24.472 | 0.531 | 89.796 |
| lstm | exclude_covid | 33.690 | 97.098 | 21.323 | 0.404 | 87.755 |
| gat | post_covid | 34.625 | 130.337 | 21.753 | 0.191 | 85.714 |
| arima | exclude_covid | 35.980 | 108.764 | 21.985 | 0.313 | 91.837 |
| persistence | exclude_covid | 37.617 | 96.018 | 22.543 | 0.310 | 91.837 |
| persistence | post_covid | 37.617 | 96.018 | 22.543 | 0.310 | 91.837 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 30.186 | 104.774 | 21.580 | 0.619 | 100.000 |
| gnn_st | post_covid | 32.281 | 110.610 | 23.883 | 0.546 | 96.154 |
| lstm | post_covid | 35.449 | 74.585 | 21.823 | 0.474 | 84.615 |
| arima | post_covid | 38.840 | 117.493 | 27.995 | 0.250 | 96.154 |
| dualtopo | post_covid | 38.886 | 135.114 | 26.072 | 0.336 | 80.769 |
| lstm | exclude_covid | 44.085 | 93.684 | 31.318 | 0.288 | 80.769 |
| gat | post_covid | 46.572 | 126.859 | 33.215 | -0.073 | 73.077 |
| arima | exclude_covid | 48.309 | 104.044 | 33.861 | 0.156 | 84.615 |
| persistence | exclude_covid | 51.020 | 108.941 | 37.008 | 0.146 | 84.615 |
| persistence | post_covid | 51.020 | 108.941 | 37.008 | 0.146 | 84.615 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.002 | 72.538 | 5.352 | 0.524 | 100.000 |
| gnn_st | post_covid | 6.166 | 68.236 | 5.005 | 0.538 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| persistence | exclude_covid | 8.487 | 81.409 | 6.191 | 0.463 | 100.000 |
| persistence | post_covid | 8.487 | 81.409 | 6.191 | 0.463 | 100.000 |
| gat | post_covid | 10.114 | 134.270 | 8.796 | 0.389 | 100.000 |
| lstm | post_covid | 10.745 | 131.937 | 8.947 | 0.484 | 100.000 |
| arima | exclude_covid | 10.944 | 114.098 | 8.560 | 0.314 | 100.000 |
| lstm | exclude_covid | 14.871 | 100.956 | 10.024 | 0.525 | 95.652 |
| arima | post_covid | 15.729 | 217.889 | 14.321 | 0.333 | 100.000 |
| dualtopo | post_covid | 23.529 | 331.063 | 22.663 | 0.577 | 100.000 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 18.655 | 79.338 | 11.762 | 0.566 | 100.000 |
| lstm | post_covid | 20.947 | 67.396 | 11.862 | 0.353 | 91.429 |
| gnn_st | post_covid | 21.316 | 82.264 | 13.129 | 0.332 | 91.429 |
| dualtopo | post_covid | 21.905 | 122.202 | 14.198 | 0.363 | 88.571 |
| arima | post_covid | 23.505 | 114.756 | 15.553 | -0.010 | 91.429 |
| arima | exclude_covid | 24.293 | 111.306 | 15.787 | -0.017 | 91.429 |
| lstm | exclude_covid | 24.293 | 87.415 | 14.557 | 0.182 | 91.429 |
| gat | post_covid | 24.622 | 104.627 | 15.167 | 0.027 | 88.571 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| persistence | exclude_covid | 31.213 | 99.271 | 18.677 | -0.000 | 91.429 |
| persistence | post_covid | 31.213 | 99.271 | 18.677 | -0.000 | 91.429 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 23.754 | 107.058 | 16.995 | 0.513 | 100.000 |
| lstm | post_covid | 26.297 | 66.720 | 16.280 | 0.334 | 85.714 |
| dualtopo | post_covid | 26.944 | 112.069 | 17.461 | 0.191 | 80.952 |
| gnn_st | post_covid | 27.240 | 110.218 | 19.215 | 0.186 | 85.714 |
| arima | post_covid | 29.511 | 116.756 | 21.007 | -0.111 | 85.714 |
| lstm | exclude_covid | 30.711 | 98.372 | 20.926 | 0.077 | 85.714 |
| arima | exclude_covid | 30.727 | 119.517 | 21.930 | -0.139 | 85.714 |
| gat | post_covid | 31.560 | 138.475 | 22.857 | -0.174 | 80.952 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| persistence | exclude_covid | 40.062 | 138.038 | 28.448 | -0.136 | 85.714 |
| persistence | post_covid | 40.062 | 138.038 | 28.448 | -0.136 | 85.714 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 4.647 | 53.855 | 3.631 | 0.589 | 100.000 |
| gnn_st | post_covid | 4.790 | 40.333 | 3.999 | 0.598 | 100.000 |
| xgboost | post_covid | 4.866 | 37.758 | 3.912 | 0.508 | 100.000 |
| persistence | exclude_covid | 5.307 | 41.120 | 4.021 | 0.427 | 100.000 |
| persistence | post_covid | 5.307 | 41.120 | 4.021 | 0.427 | 100.000 |
| arima | exclude_covid | 7.690 | 98.989 | 6.573 | 0.164 | 100.000 |
| lstm | post_covid | 7.725 | 68.409 | 5.235 | 0.520 | 100.000 |
| lstm | exclude_covid | 7.788 | 70.978 | 5.004 | 0.452 | 100.000 |
| arima | post_covid | 8.650 | 111.756 | 7.371 | 0.024 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| dualtopo | post_covid | 10.518 | 137.402 | 9.303 | 0.623 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.059 | 107.180 | 12.012 | 0.692 | 100.000 |
| xgboost | post_covid | 23.019 | 88.465 | 14.467 | 0.447 | 85.106 |
| arima | post_covid | 23.127 | 203.704 | 17.364 | 0.295 | 97.872 |
| arima | exclude_covid | 23.214 | 199.196 | 17.192 | 0.298 | 95.745 |
| lstm | post_covid | 23.750 | 137.136 | 15.080 | 0.417 | 93.617 |
| lstm | exclude_covid | 24.080 | 122.701 | 15.818 | 0.438 | 93.617 |
| dualtopo | post_covid | 25.510 | 311.319 | 21.967 | 0.537 | 93.617 |
| persistence | exclude_covid | 26.829 | 89.927 | 15.589 | 0.299 | 93.617 |
| persistence | post_covid | 26.829 | 89.927 | 15.589 | 0.299 | 95.745 |
| gat | post_covid | 27.381 | 183.105 | 19.366 | 0.233 | 87.234 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 22.113 | 95.093 | 17.161 | 0.590 | 100.000 |
| lstm | post_covid | 22.638 | 68.684 | 15.167 | 0.545 | 88.462 |
| dualtopo | post_covid | 26.797 | 152.258 | 20.732 | 0.366 | 88.462 |
| arima | post_covid | 27.988 | 108.975 | 19.705 | 0.152 | 96.154 |
| arima | exclude_covid | 28.213 | 106.836 | 19.545 | 0.167 | 92.308 |
| lstm | exclude_covid | 28.639 | 80.705 | 19.987 | 0.380 | 88.462 |
| xgboost | post_covid | 30.432 | 88.316 | 22.039 | 0.258 | 92.308 |
| gat | post_covid | 35.470 | 146.986 | 26.732 | -0.000 | 76.923 |
| persistence | exclude_covid | 35.530 | 79.440 | 24.042 | 0.158 | 88.462 |
| persistence | post_covid | 35.530 | 79.440 | 24.042 | 0.158 | 92.308 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.270 | 88.649 | 5.092 | 0.611 | 76.190 |
| gnn_st | post_covid | 6.773 | 122.146 | 5.637 | 0.482 | 100.000 |
| persistence | exclude_covid | 6.931 | 102.911 | 5.124 | 0.348 | 100.000 |
| persistence | post_covid | 6.931 | 102.911 | 5.124 | 0.348 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gat | post_covid | 10.965 | 227.822 | 10.246 | 0.500 | 100.000 |
| arima | exclude_covid | 14.853 | 313.547 | 14.280 | 0.394 | 100.000 |
| arima | post_covid | 15.073 | 320.988 | 14.467 | 0.316 | 100.000 |
| lstm | exclude_covid | 16.802 | 174.695 | 10.656 | 0.504 | 100.000 |
| dualtopo | post_covid | 23.819 | 508.252 | 23.496 | 0.606 | 100.000 |
| lstm | post_covid | 25.059 | 221.888 | 14.972 | 0.515 | 100.000 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 17.020 | 92.659 | 10.163 | 0.567 | 100.000 |
| gnn_st | post_covid | 18.252 | 93.470 | 10.614 | 0.500 | 97.826 |
| lstm | post_covid | 20.124 | 108.727 | 12.626 | 0.349 | 93.478 |
| arima | post_covid | 20.825 | 185.075 | 15.487 | 0.430 | 100.000 |
| dualtopo | post_covid | 21.266 | 264.400 | 16.527 | 0.448 | 91.304 |
| arima | exclude_covid | 22.315 | 262.679 | 17.561 | 0.166 | 97.826 |
| lstm | exclude_covid | 23.885 | 114.433 | 14.646 | 0.263 | 89.130 |
| gat | post_covid | 25.182 | 157.501 | 16.202 | 0.069 | 86.957 |
| persistence | exclude_covid | 26.703 | 98.089 | 14.604 | 0.139 | 93.478 |
| persistence | post_covid | 26.703 | 98.089 | 14.604 | 0.139 | 95.652 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 22.696 | 102.882 | 15.613 | 0.413 | 100.000 |
| dualtopo | post_covid | 24.261 | 115.599 | 16.624 | 0.179 | 84.000 |
| lstm | post_covid | 24.430 | 75.549 | 15.449 | 0.307 | 88.000 |
| gnn_st | post_covid | 24.588 | 114.521 | 17.166 | 0.301 | 96.000 |
| arima | post_covid | 26.558 | 176.943 | 20.878 | 0.168 | 100.000 |
| arima | exclude_covid | 26.589 | 145.334 | 19.532 | 0.064 | 96.000 |
| lstm | exclude_covid | 30.209 | 111.193 | 19.935 | 0.116 | 80.000 |
| gat | post_covid | 33.667 | 152.851 | 25.054 | -0.220 | 76.000 |
| persistence | exclude_covid | 35.800 | 137.533 | 23.732 | -0.070 | 88.000 |
| persistence | post_covid | 35.800 | 137.533 | 23.732 | -0.070 | 92.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.169 | 68.410 | 2.815 | 0.773 | 100.000 |
| xgboost | post_covid | 4.623 | 80.489 | 3.676 | 0.445 | 100.000 |
| persistence | exclude_covid | 6.010 | 51.132 | 3.738 | 0.565 | 100.000 |
| persistence | post_covid | 6.010 | 51.132 | 3.738 | 0.565 | 100.000 |
| gat | post_covid | 6.300 | 163.036 | 5.663 | 0.801 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| arima | post_covid | 10.500 | 194.755 | 9.069 | 0.777 | 100.000 |
| lstm | exclude_covid | 12.777 | 118.290 | 8.350 | 0.691 | 100.000 |
| lstm | post_covid | 13.288 | 148.225 | 9.265 | 0.698 | 100.000 |
| arima | exclude_covid | 15.783 | 402.375 | 15.215 | 0.434 | 100.000 |
| dualtopo | post_covid | 17.026 | 441.543 | 16.411 | 0.683 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 13.004 | 77.236 | 7.806 | 0.698 | 100.000 |
| gnn_st | post_covid | 14.502 | 72.150 | 8.488 | 0.602 | 97.959 |
| lstm | post_covid | 16.278 | 98.743 | 9.825 | 0.456 | 93.878 |
| dualtopo | post_covid | 18.274 | 196.879 | 13.103 | 0.534 | 89.796 |
| lstm | exclude_covid | 18.535 | 80.292 | 10.898 | 0.321 | 89.796 |
| arima | post_covid | 18.631 | 153.286 | 12.552 | 0.179 | 97.959 |
| arima | exclude_covid | 18.891 | 126.625 | 11.750 | 0.180 | 93.878 |
| gat | post_covid | 19.497 | 109.569 | 12.089 | 0.183 | 91.837 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| persistence | exclude_covid | 23.294 | 100.265 | 13.241 | 0.182 | 95.918 |
| persistence | post_covid | 23.294 | 100.265 | 13.241 | 0.182 | 95.918 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 17.366 | 66.171 | 11.688 | 0.588 | 100.000 |
| gnn_st | post_covid | 19.584 | 70.832 | 13.334 | 0.426 | 96.154 |
| lstm | post_covid | 20.878 | 56.392 | 13.290 | 0.390 | 88.462 |
| dualtopo | post_covid | 22.117 | 73.896 | 14.133 | 0.313 | 80.769 |
| arima | post_covid | 24.106 | 86.090 | 16.305 | -0.028 | 96.154 |
| lstm | exclude_covid | 24.545 | 71.375 | 16.517 | 0.190 | 80.769 |
| arima | exclude_covid | 25.003 | 82.023 | 16.486 | -0.031 | 88.462 |
| gat | post_covid | 26.344 | 91.918 | 18.872 | -0.104 | 84.615 |
| persistence | exclude_covid | 31.289 | 105.846 | 20.465 | -0.028 | 92.308 |
| persistence | post_covid | 31.289 | 105.846 | 20.465 | -0.028 | 92.308 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.810 | 73.641 | 3.010 | 0.679 | 100.000 |
| xgboost | post_covid | 4.398 | 89.744 | 3.418 | 0.530 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| gat | post_covid | 5.037 | 129.522 | 4.422 | 0.686 | 100.000 |
| persistence | exclude_covid | 7.022 | 93.955 | 5.074 | 0.587 | 100.000 |
| persistence | post_covid | 7.022 | 93.955 | 5.074 | 0.587 | 100.000 |
| lstm | exclude_covid | 7.135 | 90.371 | 4.546 | 0.595 | 100.000 |
| arima | exclude_covid | 7.321 | 177.045 | 6.396 | 0.598 | 100.000 |
| lstm | post_covid | 8.474 | 146.618 | 5.908 | 0.522 | 100.000 |
| arima | post_covid | 9.088 | 229.247 | 8.310 | 0.550 | 100.000 |
| dualtopo | post_covid | 12.587 | 335.902 | 11.939 | 0.621 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 16.279 | 76.217 | 9.326 | 0.540 | 97.500 |
| gnn_st | post_covid | 18.088 | 72.778 | 9.939 | 0.375 | 95.000 |
| lstm | post_covid | 18.988 | 68.235 | 10.191 | 0.294 | 92.500 |
| dualtopo | post_covid | 19.257 | 114.009 | 11.001 | 0.389 | 92.500 |
| arima | exclude_covid | 20.359 | 104.766 | 11.640 | 0.017 | 92.500 |
| lstm | exclude_covid | 20.819 | 80.843 | 11.990 | 0.209 | 90.000 |
| gat | post_covid | 21.089 | 80.784 | 11.899 | 0.089 | 90.000 |
| arima | post_covid | 21.123 | 100.582 | 11.888 | 0.013 | 95.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| persistence | exclude_covid | 26.974 | 90.487 | 14.475 | 0.032 | 95.000 |
| persistence | post_covid | 26.974 | 90.487 | 14.475 | 0.032 | 95.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 20.349 | 91.545 | 12.943 | 0.470 | 96.000 |
| gnn_st | post_covid | 22.677 | 84.864 | 13.992 | 0.234 | 92.000 |
| dualtopo | post_covid | 23.422 | 79.877 | 12.938 | 0.274 | 88.000 |
| lstm | post_covid | 23.433 | 57.533 | 13.210 | 0.281 | 88.000 |
| arima | exclude_covid | 25.174 | 85.637 | 15.004 | -0.091 | 88.000 |
| lstm | exclude_covid | 25.762 | 78.788 | 15.997 | 0.124 | 84.000 |
| arima | post_covid | 26.238 | 86.808 | 15.811 | -0.084 | 92.000 |
| gat | post_covid | 26.512 | 88.908 | 16.962 | -0.077 | 84.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |
| persistence | exclude_covid | 33.868 | 109.469 | 21.116 | -0.084 | 92.000 |
| persistence | post_covid | 33.868 | 109.469 | 21.116 | -0.084 | 92.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 3.806 | 67.245 | 3.460 | 0.314 | 100.000 |
| gnn_st | post_covid | 3.926 | 52.634 | 3.185 | 0.329 | 100.000 |
| xgboost | post_covid | 4.070 | 50.670 | 3.299 | 0.273 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| persistence | exclude_covid | 5.331 | 58.850 | 3.407 | 0.322 | 100.000 |
| persistence | post_covid | 5.331 | 58.850 | 3.407 | 0.322 | 100.000 |
| arima | post_covid | 6.513 | 123.540 | 5.351 | 0.309 | 100.000 |
| lstm | post_covid | 6.804 | 86.073 | 5.161 | 0.354 | 100.000 |
| arima | exclude_covid | 7.006 | 136.647 | 6.033 | 0.340 | 100.000 |
| lstm | exclude_covid | 7.051 | 84.268 | 5.312 | 0.328 | 100.000 |
| dualtopo | post_covid | 8.636 | 170.896 | 7.774 | 0.251 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 8.962 | 88.239 | 6.317 | 0.737 | 97.619 |
| gnn_st | post_covid | 10.434 | 71.544 | 6.366 | 0.616 | 97.619 |
| lstm | post_covid | 12.315 | 62.190 | 7.184 | 0.456 | 92.857 |
| arima | post_covid | 13.027 | 156.570 | 9.031 | 0.218 | 100.000 |
| dualtopo | post_covid | 13.208 | 191.080 | 9.585 | 0.531 | 90.476 |
| arima | exclude_covid | 15.001 | 149.222 | 10.432 | 0.133 | 95.238 |
| gat | post_covid | 15.198 | 95.567 | 9.486 | 0.185 | 90.476 |
| lstm | exclude_covid | 15.199 | 95.601 | 9.743 | 0.342 | 90.476 |
| persistence | exclude_covid | 16.752 | 92.696 | 10.148 | 0.194 | 95.238 |
| persistence | post_covid | 16.752 | 92.696 | 10.148 | 0.194 | 95.238 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 11.046 | 91.661 | 8.372 | 0.683 | 100.000 |
| gnn_st | post_covid | 13.272 | 81.666 | 9.076 | 0.502 | 96.000 |
| dualtopo | post_covid | 15.458 | 139.748 | 10.360 | 0.388 | 84.000 |
| lstm | post_covid | 15.684 | 62.863 | 10.228 | 0.347 | 88.000 |
| arima | post_covid | 15.796 | 121.267 | 10.652 | 0.088 | 100.000 |
| arima | exclude_covid | 18.487 | 119.726 | 13.074 | 0.024 | 92.000 |
| lstm | exclude_covid | 19.233 | 108.085 | 13.962 | 0.213 | 88.000 |
| gat | post_covid | 19.519 | 110.349 | 14.054 | -0.050 | 84.000 |
| persistence | exclude_covid | 21.275 | 99.728 | 14.764 | 0.050 | 92.000 |
| persistence | post_covid | 21.275 | 99.728 | 14.764 | 0.050 | 92.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.154 | 56.659 | 2.379 | 0.426 | 100.000 |
| gat | post_covid | 3.216 | 73.828 | 2.770 | 0.405 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| lstm | post_covid | 3.597 | 61.201 | 2.707 | 0.474 | 100.000 |
| xgboost | post_covid | 4.358 | 83.207 | 3.295 | 0.328 | 94.118 |
| lstm | exclude_covid | 5.170 | 77.241 | 3.538 | 0.546 | 94.118 |
| persistence | exclude_covid | 5.262 | 82.356 | 3.359 | 0.298 | 100.000 |
| persistence | post_covid | 5.262 | 82.356 | 3.359 | 0.298 | 100.000 |
| arima | post_covid | 7.234 | 208.486 | 6.648 | 0.316 | 100.000 |
| arima | exclude_covid | 7.306 | 192.598 | 6.548 | 0.036 | 100.000 |
| dualtopo | post_covid | 8.920 | 266.568 | 8.446 | 0.316 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.038 | 61.661 | 5.467 | 0.694 | 100.000 |
| xgboost | post_covid | 10.516 | 75.632 | 6.581 | 0.604 | 100.000 |
| lstm | post_covid | 11.462 | 90.915 | 7.188 | 0.450 | 95.652 |
| arima | post_covid | 12.069 | 152.906 | 8.106 | 0.288 | 100.000 |
| dualtopo | post_covid | 12.407 | 194.959 | 8.534 | 0.587 | 93.478 |
| lstm | exclude_covid | 12.988 | 99.728 | 8.638 | 0.376 | 97.826 |
| gat | post_covid | 13.028 | 95.592 | 7.757 | 0.272 | 91.304 |
| arima | exclude_covid | 13.855 | 134.056 | 9.106 | 0.260 | 97.826 |
| persistence | exclude_covid | 14.883 | 86.512 | 8.693 | 0.294 | 97.826 |
| persistence | post_covid | 14.883 | 86.512 | 8.693 | 0.294 | 97.826 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 11.823 | 59.460 | 8.127 | 0.552 | 100.000 |
| xgboost | post_covid | 13.643 | 64.576 | 9.400 | 0.454 | 100.000 |
| dualtopo | post_covid | 14.770 | 80.592 | 9.141 | 0.383 | 88.462 |
| lstm | post_covid | 14.890 | 66.119 | 10.272 | 0.359 | 92.308 |
| arima | post_covid | 15.087 | 82.117 | 10.013 | 0.078 | 100.000 |
| lstm | exclude_covid | 16.750 | 86.853 | 12.572 | 0.235 | 96.154 |
| gat | post_covid | 17.149 | 86.931 | 11.927 | 0.003 | 84.615 |
| arima | exclude_covid | 17.602 | 86.768 | 12.125 | 0.082 | 96.154 |
| persistence | exclude_covid | 19.370 | 88.209 | 12.823 | 0.078 | 96.154 |
| persistence | post_covid | 19.370 | 88.209 | 12.823 | 0.078 | 96.154 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.476 | 64.523 | 2.009 | 0.665 | 100.000 |
| gat | post_covid | 2.840 | 106.850 | 2.335 | 0.760 | 100.000 |
| xgboost | post_covid | 3.520 | 90.005 | 2.916 | 0.499 | 100.000 |
| lstm | post_covid | 3.732 | 123.150 | 3.178 | 0.752 | 100.000 |
| persistence | exclude_covid | 4.660 | 84.306 | 3.325 | 0.557 | 100.000 |
| persistence | post_covid | 4.660 | 84.306 | 3.325 | 0.557 | 100.000 |
| lstm | exclude_covid | 4.818 | 116.466 | 3.524 | 0.652 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| arima | exclude_covid | 6.220 | 195.531 | 5.181 | 0.270 | 100.000 |
| arima | post_covid | 6.252 | 244.932 | 5.626 | 0.543 | 100.000 |
| dualtopo | post_covid | 8.395 | 343.636 | 7.746 | 0.679 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 10.365 | 114.763 | 6.960 | 0.634 | 86.364 |
| gnn_st | post_covid | 10.522 | 103.114 | 6.754 | 0.584 | 97.727 |
| lstm | post_covid | 11.196 | 95.804 | 6.979 | 0.513 | 93.182 |
| arima | post_covid | 12.838 | 182.436 | 9.034 | 0.232 | 97.727 |
| lstm | exclude_covid | 12.961 | 82.388 | 8.322 | 0.399 | 93.182 |
| dualtopo | post_covid | 12.980 | 216.785 | 9.506 | 0.504 | 90.909 |
| gat | post_covid | 14.550 | 127.091 | 9.453 | 0.181 | 93.182 |
| arima | exclude_covid | 15.246 | 124.799 | 9.087 | 0.250 | 97.727 |
| persistence | exclude_covid | 16.423 | 109.120 | 9.911 | 0.204 | 95.455 |
| persistence | post_covid | 16.423 | 109.120 | 9.911 | 0.204 | 95.455 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 13.449 | 148.069 | 10.308 | 0.486 | 100.000 |
| gnn_st | post_covid | 13.772 | 130.088 | 10.393 | 0.411 | 96.000 |
| lstm | post_covid | 14.160 | 82.425 | 9.237 | 0.468 | 88.000 |
| dualtopo | post_covid | 15.347 | 136.608 | 10.303 | 0.274 | 84.000 |
| arima | post_covid | 15.830 | 128.596 | 10.922 | 0.081 | 96.000 |
| lstm | exclude_covid | 16.434 | 83.302 | 11.701 | 0.296 | 88.000 |
| gat | post_covid | 19.070 | 139.294 | 14.298 | -0.075 | 88.000 |
| arima | exclude_covid | 19.737 | 114.583 | 13.264 | 0.082 | 96.000 |
| persistence | exclude_covid | 21.444 | 122.153 | 15.148 | 0.019 | 92.000 |
| persistence | post_covid | 21.444 | 122.153 | 15.148 | 0.019 | 92.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.614 | 67.621 | 1.966 | 0.653 | 100.000 |
| xgboost | post_covid | 3.285 | 70.938 | 2.556 | 0.634 | 68.421 |
| gat | post_covid | 3.425 | 111.034 | 3.078 | 0.578 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| persistence | exclude_covid | 4.418 | 91.972 | 3.021 | 0.555 | 100.000 |
| persistence | post_covid | 4.418 | 91.972 | 3.021 | 0.555 | 100.000 |
| arima | exclude_covid | 5.067 | 138.241 | 3.590 | 0.478 | 100.000 |
| lstm | post_covid | 5.146 | 113.409 | 4.007 | 0.702 | 100.000 |
| lstm | exclude_covid | 5.800 | 81.185 | 3.876 | 0.724 | 100.000 |
| arima | post_covid | 7.207 | 253.279 | 6.550 | 0.415 | 100.000 |
| dualtopo | post_covid | 8.959 | 322.281 | 8.459 | 0.621 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.683 | 88.254 | 6.031 | 0.634 | 97.826 |
| xgboost | post_covid | 10.789 | 89.906 | 6.337 | 0.636 | 100.000 |
| lstm | post_covid | 11.950 | 109.443 | 7.430 | 0.499 | 95.652 |
| lstm | exclude_covid | 13.530 | 114.069 | 8.704 | 0.378 | 95.652 |
| arima | post_covid | 13.571 | 178.821 | 9.415 | 0.243 | 100.000 |
| dualtopo | post_covid | 13.890 | 232.141 | 10.045 | 0.503 | 91.304 |
| gat | post_covid | 14.952 | 146.876 | 9.631 | 0.136 | 91.304 |
| arima | exclude_covid | 16.067 | 102.842 | 9.218 | 0.258 | 95.652 |
| persistence | exclude_covid | 17.016 | 89.321 | 9.226 | 0.245 | 97.826 |
| persistence | post_covid | 17.016 | 89.321 | 9.226 | 0.245 | 97.826 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.639 | 110.770 | 9.908 | 0.491 | 95.833 |
| xgboost | post_covid | 14.809 | 116.267 | 10.577 | 0.499 | 100.000 |
| lstm | post_covid | 15.606 | 93.677 | 10.251 | 0.450 | 91.667 |
| dualtopo | post_covid | 17.131 | 140.150 | 11.227 | 0.253 | 83.333 |
| arima | post_covid | 17.756 | 129.108 | 12.397 | 0.061 | 100.000 |
| lstm | exclude_covid | 17.907 | 113.864 | 12.742 | 0.243 | 91.667 |
| gat | post_covid | 20.361 | 154.958 | 15.282 | -0.166 | 83.333 |
| arima | exclude_covid | 22.028 | 132.199 | 15.807 | 0.069 | 91.667 |
| persistence | exclude_covid | 23.432 | 119.879 | 16.054 | 0.066 | 95.833 |
| persistence | post_covid | 23.432 | 119.879 | 16.054 | 0.066 | 95.833 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.035 | 61.150 | 1.712 | 0.731 | 100.000 |
| gnn_st | post_covid | 2.203 | 63.692 | 1.801 | 0.792 | 100.000 |
| persistence | exclude_covid | 2.537 | 55.985 | 1.777 | 0.765 | 100.000 |
| persistence | post_covid | 2.537 | 55.985 | 1.777 | 0.765 | 100.000 |
| arima | exclude_covid | 3.226 | 70.817 | 2.029 | 0.648 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gat | post_covid | 3.894 | 138.059 | 3.466 | 0.637 | 100.000 |
| lstm | post_covid | 5.735 | 126.643 | 4.354 | 0.714 | 100.000 |
| lstm | exclude_covid | 5.739 | 114.293 | 4.298 | 0.782 | 100.000 |
| arima | post_covid | 6.414 | 233.053 | 6.161 | 0.757 | 100.000 |
| dualtopo | post_covid | 9.125 | 332.495 | 8.756 | 0.747 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.134 | 77.041 | 2.868 | 0.691 | 100.000 |
| lstm | post_covid | 4.853 | 94.308 | 3.582 | 0.508 | 100.000 |
| arima | exclude_covid | 4.960 | 133.207 | 4.073 | 0.503 | 100.000 |
| arima | post_covid | 5.215 | 151.510 | 4.376 | 0.498 | 100.000 |
| persistence | exclude_covid | 5.380 | 75.246 | 3.819 | 0.511 | 100.000 |
| persistence | post_covid | 5.380 | 75.246 | 3.819 | 0.511 | 100.000 |
| dualtopo | post_covid | 5.775 | 177.489 | 4.978 | 0.710 | 100.000 |
| gat | post_covid | 5.854 | 105.062 | 4.471 | 0.460 | 100.000 |
| lstm | exclude_covid | 6.445 | 104.407 | 4.507 | 0.382 | 100.000 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| xgboost | post_covid | 11.893 | 112.778 | 7.865 | 0.510 | 81.395 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.980 | 51.760 | 3.499 | 0.512 | 100.000 |
| arima | post_covid | 5.125 | 63.959 | 3.904 | 0.362 | 100.000 |
| arima | exclude_covid | 5.143 | 57.530 | 3.901 | 0.355 | 100.000 |
| dualtopo | post_covid | 5.467 | 76.964 | 4.321 | 0.580 | 100.000 |
| lstm | post_covid | 5.674 | 51.529 | 4.108 | 0.369 | 100.000 |
| persistence | exclude_covid | 6.567 | 50.458 | 5.028 | 0.365 | 100.000 |
| persistence | post_covid | 6.567 | 50.458 | 5.028 | 0.365 | 100.000 |
| gat | post_covid | 7.186 | 66.633 | 5.716 | 0.245 | 100.000 |
| lstm | exclude_covid | 7.731 | 63.289 | 5.631 | 0.251 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| xgboost | post_covid | 15.498 | 138.114 | 12.446 | 0.292 | 80.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.068 | 77.588 | 1.503 | 0.570 | 83.333 |
| gnn_st | post_covid | 2.528 | 112.152 | 1.991 | 0.346 | 100.000 |
| persistence | exclude_covid | 3.040 | 109.675 | 2.139 | 0.352 | 100.000 |
| persistence | post_covid | 3.040 | 109.675 | 2.139 | 0.352 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| gat | post_covid | 3.185 | 158.437 | 2.740 | 0.229 | 100.000 |
| lstm | post_covid | 3.399 | 153.722 | 2.853 | 0.070 | 100.000 |
| lstm | exclude_covid | 4.026 | 161.515 | 2.945 | 0.091 | 100.000 |
| arima | exclude_covid | 4.694 | 238.314 | 4.313 | 0.369 | 100.000 |
| arima | post_covid | 5.339 | 273.109 | 5.031 | 0.401 | 100.000 |
| dualtopo | post_covid | 6.177 | 317.107 | 5.890 | 0.349 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
