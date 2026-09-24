# Per-neighborhood leaderboard — horizon 1

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_st | 12 | 11 | 3 |
| lstm | 2 | 2 | 8 |
| arima | 0 | 1 | 0 |
| persistence | 0 | 0 | 1 |
| seasonal_naive | 0 | 0 | 1 |
| xgboost | 0 | 0 | 1 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_st (post_covid)`: Allston, Charles., Dorchest., E.Boston, Fenway, HydePark, JP, Mattapan, Roxbury, S.Boston, S.End, W.Roxbury; `lstm (exclude_covid)`: BackBay+, Roslind.
- **Flu season (Oct–Mar)** — `arima (post_covid)`: Fenway; `gnn_st (post_covid)`: Allston, Charles., Dorchest., E.Boston, HydePark, JP, Mattapan, Roxbury, S.Boston, S.End, W.Roxbury; `lstm (exclude_covid)`: BackBay+, Roslind.
- **Off-season (Apr–Sep)** — `gnn_st (post_covid)`: BackBay+, Dorchest., HydePark; `lstm (exclude_covid)`: Allston, E.Boston, Fenway, S.End; `lstm (post_covid)`: Charles., Roslind., S.Boston, W.Roxbury; `persistence (exclude_covid)`: Mattapan; `seasonal_naive (exclude_covid)`: Roxbury; `xgboost (post_covid)`: JP

`gnn_st (post_covid)` wins 12 of 14 neighborhoods. `gnn_st (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 18.418 | 43.011 | 12.428 | 0.946 | 97.959 |
| arima | exclude_covid | 19.712 | 52.684 | 13.266 | 0.934 | 97.959 |
| arima | post_covid | 20.278 | 55.144 | 13.935 | 0.931 | 97.959 |
| persistence | exclude_covid | 23.552 | 37.122 | 14.139 | 0.907 | 95.918 |
| persistence | post_covid | 23.552 | 37.122 | 14.139 | 0.907 | 95.918 |
| xgboost | post_covid | 26.700 | 75.610 | 17.944 | 0.883 | 97.959 |
| lstm | post_covid | 27.449 | 56.733 | 16.682 | 0.878 | 91.837 |
| lstm | exclude_covid | 31.197 | 59.619 | 17.606 | 0.875 | 89.796 |
| gat | post_covid | 43.432 | 139.310 | 31.135 | 0.630 | 63.265 |
| dualtopo | post_covid | 56.200 | 252.525 | 43.196 | 0.498 | 55.102 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 23.993 | 24.383 | 16.943 | 0.931 | 96.154 |
| arima | exclude_covid | 24.898 | 21.337 | 16.724 | 0.923 | 96.154 |
| arima | post_covid | 25.342 | 21.401 | 17.016 | 0.921 | 100.000 |
| persistence | exclude_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| persistence | post_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| xgboost | post_covid | 34.801 | 45.342 | 24.331 | 0.836 | 96.154 |
| lstm | post_covid | 36.664 | 31.355 | 24.308 | 0.854 | 84.615 |
| lstm | exclude_covid | 41.904 | 33.563 | 25.776 | 0.849 | 80.769 |
| gat | post_covid | 54.890 | 60.535 | 38.434 | 0.518 | 73.077 |
| dualtopo | post_covid | 63.243 | 81.380 | 41.060 | 0.294 | 69.231 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.482 | 64.069 | 7.324 | 0.841 | 100.000 |
| persistence | exclude_covid | 8.971 | 52.834 | 7.398 | 0.828 | 95.652 |
| persistence | post_covid | 8.971 | 52.834 | 7.398 | 0.828 | 95.652 |
| lstm | post_covid | 9.249 | 85.421 | 8.061 | 0.820 | 100.000 |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| lstm | exclude_covid | 9.403 | 89.074 | 8.370 | 0.816 | 100.000 |
| arima | exclude_covid | 11.270 | 88.120 | 9.357 | 0.773 | 100.000 |
| xgboost | post_covid | 12.236 | 109.826 | 10.723 | 0.832 | 100.000 |
| arima | post_covid | 12.248 | 93.287 | 10.451 | 0.725 | 95.652 |
| gat | post_covid | 24.753 | 228.360 | 22.884 | 0.660 | 52.174 |
| dualtopo | post_covid | 46.986 | 445.993 | 45.612 | 0.689 | 39.130 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 23.186 | 63.271 | 13.896 | 0.891 | 89.796 |
| xgboost | post_covid | 27.130 | 69.844 | 17.094 | 0.844 | 100.000 |
| lstm | post_covid | 27.796 | 57.435 | 16.381 | 0.835 | 85.714 |
| arima | exclude_covid | 28.039 | 95.072 | 17.786 | 0.835 | 89.796 |
| arima | post_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| persistence | exclude_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| persistence | post_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| lstm | exclude_covid | 31.315 | 65.470 | 17.966 | 0.837 | 87.755 |
| gat | post_covid | 40.771 | 130.714 | 28.698 | 0.593 | 69.388 |
| dualtopo | post_covid | 50.807 | 231.367 | 37.698 | 0.436 | 65.306 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 30.194 | 38.015 | 18.315 | 0.867 | 84.615 |
| xgboost | post_covid | 35.704 | 48.281 | 23.608 | 0.799 | 100.000 |
| arima | exclude_covid | 35.807 | 49.600 | 22.907 | 0.806 | 84.615 |
| arima | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | exclude_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| lstm | post_covid | 37.106 | 36.117 | 23.649 | 0.794 | 76.923 |
| lstm | exclude_covid | 41.950 | 43.188 | 26.339 | 0.796 | 76.923 |
| gat | post_covid | 52.697 | 69.186 | 38.141 | 0.486 | 61.538 |
| dualtopo | post_covid | 59.754 | 91.283 | 38.998 | 0.212 | 73.077 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| lstm | post_covid | 9.463 | 81.533 | 8.166 | 0.729 | 95.652 |
| lstm | exclude_covid | 9.993 | 90.659 | 8.501 | 0.736 | 100.000 |
| gnn_st | post_covid | 10.711 | 91.822 | 8.901 | 0.650 | 95.652 |
| xgboost | post_covid | 11.272 | 94.220 | 9.729 | 0.658 | 100.000 |
| arima | post_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| persistence | exclude_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| persistence | post_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| arima | exclude_covid | 15.015 | 146.475 | 11.998 | 0.429 | 95.652 |
| gat | post_covid | 20.056 | 200.268 | 18.024 | 0.457 | 78.261 |
| dualtopo | post_covid | 38.252 | 389.722 | 36.228 | 0.544 | 56.522 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 15.130 | 56.088 | 10.681 | 0.937 | 83.333 |
| gnn_st | post_covid | 16.819 | 67.969 | 11.502 | 0.906 | 90.476 |
| lstm | post_covid | 19.728 | 58.355 | 12.418 | 0.924 | 85.714 |
| persistence | exclude_covid | 23.222 | 85.124 | 14.843 | 0.822 | 85.714 |
| persistence | post_covid | 23.222 | 85.124 | 14.843 | 0.822 | 85.714 |
| arima | exclude_covid | 23.415 | 94.070 | 15.413 | 0.818 | 80.952 |
| xgboost | post_covid | 23.713 | 73.547 | 15.005 | 0.880 | 97.619 |
| arima | post_covid | 24.994 | 105.711 | 16.384 | 0.786 | 83.333 |
| gat | post_covid | 29.759 | 110.190 | 19.188 | 0.659 | 80.952 |
| dualtopo | post_covid | 38.582 | 164.949 | 25.822 | 0.354 | 90.476 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 18.077 | 54.783 | 13.299 | 0.938 | 84.615 |
| gnn_st | post_covid | 20.428 | 74.282 | 14.726 | 0.900 | 88.462 |
| lstm | post_covid | 24.275 | 54.271 | 16.224 | 0.922 | 80.769 |
| persistence | exclude_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| persistence | post_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| arima | exclude_covid | 28.626 | 99.575 | 19.382 | 0.802 | 73.077 |
| xgboost | post_covid | 29.436 | 76.657 | 20.207 | 0.881 | 96.154 |
| arima | post_covid | 30.480 | 102.622 | 20.643 | 0.773 | 73.077 |
| gat | post_covid | 36.757 | 101.468 | 24.697 | 0.613 | 69.231 |
| dualtopo | post_covid | 46.324 | 120.650 | 30.390 | 0.227 | 84.615 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 8.000 | 64.992 | 6.234 | 0.521 | 93.750 |
| gnn_st | post_covid | 8.028 | 57.710 | 6.263 | 0.557 | 93.750 |
| xgboost | post_covid | 8.252 | 68.493 | 6.551 | 0.589 | 100.000 |
| lstm | exclude_covid | 8.364 | 58.209 | 6.427 | 0.482 | 81.250 |
| persistence | exclude_covid | 9.741 | 61.670 | 7.612 | 0.488 | 93.750 |
| persistence | post_covid | 9.741 | 61.670 | 7.612 | 0.488 | 93.750 |
| arima | exclude_covid | 10.371 | 85.124 | 8.963 | 0.389 | 93.750 |
| gat | post_covid | 11.368 | 124.364 | 10.235 | 0.365 | 100.000 |
| arima | post_covid | 11.411 | 110.729 | 9.464 | 0.249 | 100.000 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| dualtopo | post_covid | 20.504 | 236.934 | 18.398 | 0.523 | 100.000 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.074 | 64.768 | 8.120 | 0.927 | 95.918 |
| lstm | post_covid | 15.708 | 78.245 | 9.613 | 0.880 | 97.959 |
| lstm | exclude_covid | 15.773 | 59.526 | 9.509 | 0.884 | 97.959 |
| xgboost | post_covid | 16.134 | 85.443 | 10.405 | 0.871 | 97.959 |
| arima | exclude_covid | 16.730 | 59.722 | 9.531 | 0.862 | 93.878 |
| arima | post_covid | 16.744 | 73.483 | 9.904 | 0.853 | 97.959 |
| persistence | exclude_covid | 17.341 | 56.834 | 10.129 | 0.853 | 93.878 |
| persistence | post_covid | 17.341 | 56.834 | 10.129 | 0.853 | 93.878 |
| gat | post_covid | 23.546 | 125.186 | 16.083 | 0.696 | 91.837 |
| dualtopo | post_covid | 32.298 | 221.112 | 24.109 | 0.443 | 89.796 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 15.318 | 56.791 | 10.101 | 0.916 | 96.154 |
| lstm | post_covid | 20.394 | 58.336 | 12.342 | 0.857 | 96.154 |
| lstm | exclude_covid | 20.902 | 53.939 | 13.396 | 0.861 | 96.154 |
| xgboost | post_covid | 21.322 | 89.686 | 14.617 | 0.837 | 96.154 |
| arima | post_covid | 21.417 | 48.565 | 12.098 | 0.830 | 96.154 |
| arima | exclude_covid | 21.641 | 44.852 | 12.330 | 0.840 | 92.308 |
| persistence | exclude_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| persistence | post_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| gat | post_covid | 30.244 | 89.520 | 20.911 | 0.622 | 84.615 |
| dualtopo | post_covid | 38.797 | 133.128 | 25.967 | 0.264 | 80.769 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.014 | 65.841 | 5.114 | 0.505 | 100.000 |
| xgboost | post_covid | 6.376 | 80.648 | 5.643 | 0.551 | 100.000 |
| gnn_st | post_covid | 6.732 | 73.786 | 5.879 | 0.430 | 95.652 |
| lstm | post_covid | 7.451 | 100.751 | 6.529 | 0.547 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| arima | exclude_covid | 8.178 | 76.531 | 6.366 | 0.333 | 95.652 |
| persistence | exclude_covid | 8.449 | 74.377 | 6.635 | 0.277 | 95.652 |
| persistence | post_covid | 8.449 | 74.377 | 6.635 | 0.277 | 95.652 |
| arima | post_covid | 8.877 | 101.652 | 7.423 | 0.277 | 100.000 |
| gat | post_covid | 12.132 | 165.503 | 10.626 | 0.484 | 100.000 |
| dualtopo | post_covid | 22.821 | 320.572 | 22.008 | 0.561 | 100.000 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.007 | 56.816 | 7.033 | 0.807 | 91.429 |
| lstm | post_covid | 14.175 | 59.612 | 8.092 | 0.768 | 94.286 |
| lstm | exclude_covid | 14.593 | 58.663 | 7.946 | 0.749 | 94.286 |
| xgboost | post_covid | 15.444 | 65.978 | 9.419 | 0.780 | 97.143 |
| arima | exclude_covid | 16.430 | 93.918 | 9.760 | 0.667 | 97.143 |
| arima | post_covid | 17.061 | 83.159 | 10.089 | 0.629 | 97.143 |
| persistence | exclude_covid | 17.774 | 82.365 | 10.434 | 0.674 | 91.429 |
| persistence | post_covid | 17.774 | 82.365 | 10.434 | 0.674 | 91.429 |
| gat | post_covid | 19.182 | 82.717 | 11.244 | 0.485 | 88.571 |
| dualtopo | post_covid | 21.819 | 119.644 | 14.006 | 0.303 | 88.571 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 16.193 | 61.477 | 8.670 | 0.792 | 85.714 |
| lstm | post_covid | 17.924 | 68.644 | 11.054 | 0.742 | 90.476 |
| lstm | exclude_covid | 18.447 | 69.107 | 10.795 | 0.720 | 90.476 |
| xgboost | post_covid | 19.517 | 81.155 | 12.952 | 0.763 | 95.238 |
| arima | exclude_covid | 20.198 | 94.520 | 12.042 | 0.647 | 95.238 |
| arima | post_covid | 21.375 | 86.881 | 13.295 | 0.593 | 95.238 |
| persistence | exclude_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| persistence | post_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| gat | post_covid | 24.329 | 92.404 | 15.752 | 0.403 | 80.952 |
| dualtopo | post_covid | 26.923 | 111.043 | 17.378 | 0.112 | 80.952 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 4.522 | 46.064 | 3.649 | 0.529 | 100.000 |
| lstm | exclude_covid | 4.683 | 42.995 | 3.671 | 0.517 | 100.000 |
| xgboost | post_covid | 4.993 | 43.213 | 4.120 | 0.400 | 100.000 |
| gnn_st | post_covid | 5.445 | 49.825 | 4.577 | 0.263 | 100.000 |
| gat | post_covid | 5.664 | 68.185 | 4.482 | 0.399 | 100.000 |
| arima | post_covid | 6.506 | 77.576 | 5.279 | 0.062 | 100.000 |
| persistence | exclude_covid | 7.510 | 67.032 | 5.857 | -0.140 | 92.857 |
| persistence | post_covid | 7.510 | 67.032 | 5.857 | -0.140 | 92.857 |
| arima | exclude_covid | 7.932 | 93.016 | 6.339 | -0.101 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| dualtopo | post_covid | 10.143 | 132.546 | 8.948 | 0.606 | 100.000 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.428 | 69.656 | 5.674 | 0.957 | 100.000 |
| lstm | post_covid | 8.603 | 79.630 | 6.342 | 0.940 | 100.000 |
| lstm | exclude_covid | 9.391 | 68.537 | 6.508 | 0.925 | 100.000 |
| arima | post_covid | 11.883 | 93.526 | 8.428 | 0.858 | 97.872 |
| persistence | exclude_covid | 12.005 | 64.837 | 8.191 | 0.859 | 97.872 |
| persistence | post_covid | 12.005 | 64.837 | 8.191 | 0.859 | 97.872 |
| arima | exclude_covid | 12.829 | 90.731 | 8.566 | 0.831 | 97.872 |
| xgboost | post_covid | 12.945 | 67.118 | 8.382 | 0.823 | 95.745 |
| gat | post_covid | 17.255 | 175.310 | 14.449 | 0.757 | 89.362 |
| dualtopo | post_covid | 25.200 | 303.733 | 21.651 | 0.434 | 93.617 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.845 | 47.873 | 6.735 | 0.955 | 100.000 |
| lstm | post_covid | 9.660 | 49.868 | 6.948 | 0.938 | 100.000 |
| lstm | exclude_covid | 10.818 | 47.880 | 7.437 | 0.923 | 100.000 |
| arima | post_covid | 14.832 | 59.112 | 10.855 | 0.832 | 96.154 |
| persistence | exclude_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| persistence | post_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| arima | exclude_covid | 16.265 | 56.064 | 11.389 | 0.799 | 96.154 |
| xgboost | post_covid | 16.628 | 52.779 | 11.754 | 0.804 | 92.308 |
| gat | post_covid | 19.802 | 98.152 | 15.790 | 0.706 | 84.615 |
| dualtopo | post_covid | 26.701 | 150.093 | 20.630 | 0.277 | 88.462 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 4.910 | 80.893 | 4.186 | 0.235 | 100.000 |
| persistence | post_covid | 4.910 | 80.893 | 4.186 | 0.235 | 100.000 |
| gnn_st | post_covid | 5.162 | 96.627 | 4.359 | 0.537 | 100.000 |
| xgboost | post_covid | 5.722 | 84.870 | 4.206 | 0.430 | 100.000 |
| arima | exclude_covid | 6.387 | 133.653 | 5.070 | 0.293 | 100.000 |
| arima | post_covid | 6.605 | 136.133 | 5.423 | 0.181 | 100.000 |
| lstm | post_covid | 7.079 | 116.480 | 5.590 | 0.612 | 100.000 |
| lstm | exclude_covid | 7.246 | 94.113 | 5.359 | 0.617 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| gat | post_covid | 13.450 | 270.839 | 12.787 | 0.538 | 95.238 |
| dualtopo | post_covid | 23.208 | 493.955 | 22.916 | 0.558 | 100.000 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.142 | 59.760 | 5.784 | 0.922 | 100.000 |
| lstm | post_covid | 9.397 | 65.862 | 6.157 | 0.888 | 97.826 |
| lstm | exclude_covid | 9.620 | 64.495 | 6.362 | 0.892 | 95.652 |
| arima | exclude_covid | 11.414 | 88.245 | 7.575 | 0.829 | 97.826 |
| xgboost | post_covid | 11.656 | 77.237 | 7.501 | 0.821 | 100.000 |
| persistence | exclude_covid | 11.663 | 55.428 | 7.276 | 0.834 | 95.652 |
| persistence | post_covid | 11.663 | 55.428 | 7.276 | 0.834 | 95.652 |
| arima | post_covid | 11.870 | 101.297 | 8.222 | 0.836 | 97.826 |
| gat | post_covid | 17.673 | 150.533 | 12.362 | 0.552 | 86.957 |
| dualtopo | post_covid | 21.060 | 257.213 | 16.294 | 0.372 | 91.304 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.530 | 54.014 | 8.029 | 0.908 | 100.000 |
| lstm | post_covid | 12.119 | 45.116 | 8.149 | 0.870 | 96.000 |
| lstm | exclude_covid | 12.418 | 49.022 | 8.569 | 0.874 | 92.000 |
| arima | exclude_covid | 14.399 | 57.631 | 9.842 | 0.807 | 96.000 |
| arima | post_covid | 14.797 | 80.587 | 10.721 | 0.806 | 96.000 |
| persistence | exclude_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| persistence | post_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| xgboost | post_covid | 15.347 | 64.019 | 10.590 | 0.776 | 100.000 |
| gat | post_covid | 22.697 | 101.789 | 16.240 | 0.440 | 76.000 |
| dualtopo | post_covid | 24.232 | 114.511 | 16.598 | 0.124 | 84.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.636 | 66.600 | 3.111 | 0.683 | 100.000 |
| xgboost | post_covid | 4.152 | 92.972 | 3.824 | 0.589 | 100.000 |
| lstm | post_covid | 4.309 | 90.559 | 3.784 | 0.603 | 100.000 |
| lstm | exclude_covid | 4.374 | 82.915 | 3.736 | 0.567 | 100.000 |
| persistence | exclude_covid | 5.605 | 57.660 | 3.510 | 0.531 | 100.000 |
| persistence | post_covid | 5.605 | 57.660 | 3.510 | 0.531 | 100.000 |
| arima | exclude_covid | 6.208 | 124.690 | 4.875 | 0.503 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| arima | post_covid | 6.928 | 125.951 | 5.247 | 0.647 | 100.000 |
| gat | post_covid | 8.421 | 208.562 | 7.744 | 0.555 | 100.000 |
| dualtopo | post_covid | 16.507 | 427.095 | 15.932 | 0.582 | 100.000 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.008 | 50.699 | 4.898 | 0.923 | 97.959 |
| lstm | post_covid | 7.482 | 64.140 | 4.920 | 0.928 | 95.918 |
| lstm | exclude_covid | 8.049 | 46.144 | 4.993 | 0.920 | 93.878 |
| arima | exclude_covid | 10.035 | 71.097 | 6.651 | 0.834 | 97.959 |
| arima | post_covid | 10.106 | 75.352 | 6.781 | 0.832 | 100.000 |
| xgboost | post_covid | 10.294 | 69.386 | 6.410 | 0.829 | 100.000 |
| persistence | exclude_covid | 10.466 | 61.309 | 6.949 | 0.833 | 100.000 |
| persistence | post_covid | 10.466 | 61.309 | 6.949 | 0.833 | 100.000 |
| gat | post_covid | 13.639 | 114.520 | 9.159 | 0.674 | 89.796 |
| dualtopo | post_covid | 18.116 | 191.830 | 12.891 | 0.459 | 89.796 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.179 | 39.740 | 6.944 | 0.905 | 96.154 |
| lstm | post_covid | 9.662 | 31.318 | 6.482 | 0.921 | 92.308 |
| lstm | exclude_covid | 10.774 | 34.463 | 7.452 | 0.903 | 88.462 |
| arima | post_covid | 13.077 | 51.014 | 9.519 | 0.794 | 100.000 |
| arima | exclude_covid | 13.239 | 53.613 | 9.672 | 0.789 | 96.154 |
| xgboost | post_covid | 13.660 | 51.967 | 9.216 | 0.778 | 100.000 |
| persistence | exclude_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| persistence | post_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| gat | post_covid | 17.677 | 59.695 | 12.104 | 0.589 | 80.769 |
| dualtopo | post_covid | 22.057 | 72.684 | 14.041 | 0.271 | 80.769 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.610 | 59.350 | 2.214 | 0.767 | 100.000 |
| gnn_st | post_covid | 3.065 | 63.087 | 2.585 | 0.731 | 100.000 |
| lstm | post_covid | 3.704 | 101.244 | 3.154 | 0.761 | 100.000 |
| persistence | exclude_covid | 3.802 | 68.641 | 3.104 | 0.615 | 100.000 |
| persistence | post_covid | 3.802 | 68.641 | 3.104 | 0.615 | 100.000 |
| xgboost | post_covid | 3.850 | 89.077 | 3.239 | 0.619 | 100.000 |
| arima | exclude_covid | 4.051 | 90.861 | 3.236 | 0.626 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| arima | post_covid | 4.927 | 102.865 | 3.686 | 0.505 | 100.000 |
| gat | post_covid | 6.562 | 176.497 | 5.830 | 0.499 | 100.000 |
| dualtopo | post_covid | 12.217 | 326.517 | 11.590 | 0.500 | 100.000 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.298 | 54.909 | 5.729 | 0.847 | 95.000 |
| lstm | exclude_covid | 10.497 | 49.054 | 6.381 | 0.875 | 95.000 |
| lstm | post_covid | 11.753 | 50.587 | 7.117 | 0.860 | 92.500 |
| xgboost | post_covid | 13.294 | 64.152 | 7.520 | 0.789 | 97.500 |
| arima | post_covid | 14.324 | 85.746 | 8.560 | 0.680 | 95.000 |
| arima | exclude_covid | 14.371 | 87.626 | 8.497 | 0.667 | 95.000 |
| persistence | exclude_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| persistence | post_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| gat | post_covid | 15.787 | 72.939 | 8.946 | 0.587 | 87.500 |
| dualtopo | post_covid | 19.198 | 111.346 | 10.863 | 0.289 | 92.500 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.553 | 52.951 | 6.857 | 0.837 | 92.000 |
| lstm | exclude_covid | 12.894 | 45.954 | 8.105 | 0.870 | 92.000 |
| lstm | post_covid | 14.549 | 48.447 | 9.252 | 0.852 | 88.000 |
| xgboost | post_covid | 16.493 | 68.221 | 9.811 | 0.778 | 96.000 |
| arima | post_covid | 17.618 | 78.684 | 10.757 | 0.655 | 92.000 |
| arima | exclude_covid | 17.666 | 78.247 | 10.717 | 0.638 | 92.000 |
| persistence | exclude_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| persistence | post_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| gat | post_covid | 19.619 | 64.638 | 11.831 | 0.535 | 80.000 |
| dualtopo | post_covid | 23.400 | 78.674 | 12.878 | 0.192 | 88.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.952 | 54.154 | 3.559 | 0.205 | 100.000 |
| lstm | exclude_covid | 4.095 | 54.220 | 3.506 | 0.269 | 100.000 |
| xgboost | post_covid | 4.233 | 57.369 | 3.702 | 0.166 | 100.000 |
| gnn_st | post_covid | 4.492 | 58.171 | 3.847 | 0.046 | 100.000 |
| gat | post_covid | 4.805 | 86.774 | 4.136 | 0.182 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| persistence | exclude_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| persistence | post_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| arima | post_covid | 5.459 | 97.514 | 4.898 | -0.265 | 100.000 |
| arima | exclude_covid | 5.528 | 103.256 | 4.796 | -0.219 | 100.000 |
| dualtopo | post_covid | 8.382 | 165.800 | 7.505 | 0.177 | 100.000 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.913 | 48.186 | 3.710 | 0.895 | 95.238 |
| xgboost | post_covid | 6.889 | 70.952 | 4.374 | 0.864 | 100.000 |
| lstm | post_covid | 6.927 | 43.440 | 4.041 | 0.864 | 92.857 |
| lstm | exclude_covid | 7.539 | 57.942 | 4.468 | 0.865 | 97.619 |
| arima | exclude_covid | 8.225 | 82.565 | 5.499 | 0.784 | 97.619 |
| persistence | exclude_covid | 8.667 | 52.202 | 5.379 | 0.785 | 95.238 |
| persistence | post_covid | 8.667 | 52.202 | 5.379 | 0.785 | 95.238 |
| arima | post_covid | 8.919 | 77.581 | 5.732 | 0.746 | 92.857 |
| gat | post_covid | 9.834 | 92.733 | 6.680 | 0.667 | 95.238 |
| dualtopo | post_covid | 13.099 | 186.090 | 9.438 | 0.427 | 90.476 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.146 | 46.143 | 4.561 | 0.883 | 96.000 |
| xgboost | post_covid | 8.541 | 72.250 | 5.581 | 0.842 | 100.000 |
| lstm | post_covid | 8.619 | 40.667 | 5.249 | 0.846 | 92.000 |
| lstm | exclude_covid | 9.423 | 53.650 | 5.879 | 0.848 | 96.000 |
| arima | exclude_covid | 9.893 | 61.045 | 6.358 | 0.757 | 96.000 |
| persistence | exclude_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| persistence | post_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| arima | post_covid | 10.993 | 62.474 | 7.091 | 0.710 | 88.000 |
| gat | post_covid | 12.247 | 79.338 | 8.784 | 0.598 | 92.000 |
| dualtopo | post_covid | 15.407 | 136.737 | 10.300 | 0.320 | 84.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.049 | 47.519 | 2.264 | 0.332 | 94.118 |
| lstm | exclude_covid | 3.139 | 64.253 | 2.394 | 0.325 | 100.000 |
| xgboost | post_covid | 3.160 | 69.043 | 2.599 | 0.357 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| gnn_st | post_covid | 3.358 | 51.190 | 2.460 | 0.257 | 94.118 |
| gat | post_covid | 4.286 | 112.431 | 3.585 | 0.273 | 100.000 |
| arima | post_covid | 4.335 | 99.798 | 3.732 | -0.044 | 100.000 |
| persistence | exclude_covid | 4.341 | 61.969 | 3.118 | 0.004 | 100.000 |
| persistence | post_covid | 4.341 | 61.969 | 3.118 | 0.004 | 100.000 |
| arima | exclude_covid | 4.816 | 114.212 | 4.236 | -0.098 | 100.000 |
| dualtopo | post_covid | 8.650 | 258.666 | 8.171 | 0.205 | 100.000 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.133 | 71.266 | 4.662 | 0.874 | 100.000 |
| gnn_st | post_covid | 6.525 | 56.613 | 4.376 | 0.854 | 100.000 |
| lstm | post_covid | 7.442 | 74.714 | 5.287 | 0.850 | 93.478 |
| xgboost | post_covid | 7.826 | 70.953 | 5.364 | 0.781 | 100.000 |
| gat | post_covid | 8.930 | 103.255 | 5.984 | 0.709 | 91.304 |
| arima | exclude_covid | 9.092 | 92.208 | 5.794 | 0.691 | 95.652 |
| arima | post_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| persistence | exclude_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| persistence | post_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| dualtopo | post_covid | 12.290 | 188.995 | 8.371 | 0.511 | 93.478 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.660 | 44.593 | 6.091 | 0.862 | 100.000 |
| gnn_st | post_covid | 8.280 | 43.385 | 5.856 | 0.811 | 100.000 |
| lstm | post_covid | 9.534 | 48.260 | 7.242 | 0.835 | 88.462 |
| xgboost | post_covid | 10.010 | 55.443 | 7.310 | 0.705 | 100.000 |
| gat | post_covid | 11.311 | 59.017 | 7.855 | 0.636 | 84.615 |
| arima | exclude_covid | 11.576 | 53.205 | 7.766 | 0.594 | 92.308 |
| arima | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | exclude_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| dualtopo | post_covid | 14.713 | 78.624 | 9.041 | 0.339 | 88.462 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.965 | 73.809 | 2.453 | 0.526 | 100.000 |
| lstm | post_covid | 3.033 | 109.106 | 2.746 | 0.542 | 100.000 |
| lstm | exclude_covid | 3.199 | 105.941 | 2.804 | 0.476 | 100.000 |
| xgboost | post_covid | 3.260 | 91.116 | 2.835 | 0.387 | 100.000 |
| arima | post_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| persistence | exclude_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| persistence | post_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| arima | exclude_covid | 3.992 | 142.912 | 3.230 | 0.387 | 100.000 |
| gat | post_covid | 4.135 | 160.765 | 3.553 | 0.523 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| dualtopo | post_covid | 8.122 | 332.478 | 7.500 | 0.586 | 100.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.459 | 83.596 | 4.138 | 0.907 | 100.000 |
| lstm | post_covid | 6.299 | 78.193 | 4.605 | 0.880 | 97.727 |
| lstm | exclude_covid | 6.784 | 79.056 | 4.733 | 0.868 | 95.455 |
| xgboost | post_covid | 7.100 | 91.722 | 5.232 | 0.850 | 97.727 |
| arima | post_covid | 7.778 | 114.838 | 6.031 | 0.801 | 97.727 |
| persistence | exclude_covid | 8.242 | 98.656 | 6.239 | 0.797 | 97.727 |
| persistence | post_covid | 8.242 | 98.656 | 6.239 | 0.797 | 97.727 |
| arima | exclude_covid | 8.884 | 122.953 | 7.092 | 0.752 | 93.182 |
| gat | post_covid | 9.238 | 111.426 | 6.583 | 0.703 | 93.182 |
| dualtopo | post_covid | 12.874 | 211.771 | 9.356 | 0.434 | 90.909 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.799 | 100.286 | 5.570 | 0.891 | 100.000 |
| lstm | post_covid | 7.996 | 82.302 | 6.392 | 0.866 | 96.000 |
| lstm | exclude_covid | 8.676 | 86.913 | 6.654 | 0.848 | 92.000 |
| xgboost | post_covid | 9.030 | 107.377 | 7.350 | 0.818 | 96.000 |
| arima | post_covid | 9.430 | 115.902 | 7.673 | 0.783 | 96.000 |
| persistence | exclude_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| persistence | post_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| arima | exclude_covid | 10.816 | 126.112 | 9.190 | 0.727 | 92.000 |
| gat | post_covid | 11.751 | 93.844 | 8.784 | 0.628 | 88.000 |
| dualtopo | post_covid | 15.315 | 135.554 | 10.246 | 0.203 | 84.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.744 | 68.718 | 2.205 | 0.570 | 100.000 |
| lstm | post_covid | 2.783 | 72.787 | 2.255 | 0.560 | 100.000 |
| gnn_st | post_covid | 2.861 | 61.636 | 2.253 | 0.559 | 100.000 |
| xgboost | post_covid | 3.073 | 71.124 | 2.443 | 0.503 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| gat | post_covid | 3.993 | 134.561 | 3.687 | 0.683 | 100.000 |
| persistence | exclude_covid | 4.433 | 76.563 | 3.289 | 0.330 | 100.000 |
| persistence | post_covid | 4.433 | 76.563 | 3.289 | 0.330 | 100.000 |
| arima | post_covid | 4.805 | 113.437 | 3.870 | 0.310 | 100.000 |
| arima | exclude_covid | 5.372 | 118.797 | 4.333 | 0.237 | 94.737 |
| dualtopo | post_covid | 8.672 | 312.057 | 8.184 | 0.562 | 100.000 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.410 | 62.830 | 3.358 | 0.922 | 100.000 |
| lstm | exclude_covid | 5.772 | 68.888 | 3.940 | 0.917 | 100.000 |
| lstm | post_covid | 6.115 | 75.146 | 4.123 | 0.914 | 100.000 |
| xgboost | post_covid | 7.204 | 64.271 | 4.314 | 0.858 | 97.826 |
| arima | exclude_covid | 7.587 | 90.832 | 4.923 | 0.836 | 95.652 |
| arima | post_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| persistence | exclude_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| persistence | post_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| gat | post_covid | 10.446 | 137.866 | 7.110 | 0.676 | 91.304 |
| dualtopo | post_covid | 13.794 | 226.490 | 9.919 | 0.418 | 91.304 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.155 | 64.895 | 4.827 | 0.907 | 100.000 |
| lstm | exclude_covid | 7.630 | 68.141 | 5.848 | 0.900 | 100.000 |
| lstm | post_covid | 8.067 | 66.821 | 6.002 | 0.897 | 100.000 |
| xgboost | post_covid | 9.750 | 73.705 | 6.803 | 0.823 | 95.833 |
| arima | exclude_covid | 10.013 | 81.598 | 6.905 | 0.800 | 91.667 |
| arima | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| persistence | exclude_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| persistence | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| gat | post_covid | 13.753 | 109.724 | 9.674 | 0.582 | 83.333 |
| dualtopo | post_covid | 17.112 | 138.472 | 11.207 | 0.168 | 83.333 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.193 | 53.978 | 1.599 | 0.738 | 100.000 |
| gnn_st | post_covid | 2.316 | 60.577 | 1.755 | 0.658 | 100.000 |
| lstm | exclude_covid | 2.482 | 69.702 | 1.859 | 0.598 | 100.000 |
| lstm | post_covid | 2.684 | 84.229 | 2.074 | 0.656 | 100.000 |
| arima | post_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| persistence | exclude_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| persistence | post_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| arima | exclude_covid | 3.317 | 100.905 | 2.761 | 0.523 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| gat | post_covid | 4.669 | 168.566 | 4.314 | 0.727 | 100.000 |
| dualtopo | post_covid | 8.855 | 322.510 | 8.514 | 0.704 | 100.000 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.651 | 71.210 | 2.562 | 0.780 | 100.000 |
| lstm | post_covid | 3.752 | 76.593 | 2.588 | 0.725 | 97.674 |
| arima | exclude_covid | 3.902 | 92.755 | 2.835 | 0.714 | 100.000 |
| arima | post_covid | 3.922 | 96.417 | 2.890 | 0.712 | 100.000 |
| persistence | exclude_covid | 4.043 | 71.866 | 2.774 | 0.721 | 100.000 |
| persistence | post_covid | 4.043 | 71.866 | 2.774 | 0.721 | 100.000 |
| lstm | exclude_covid | 4.250 | 66.349 | 2.797 | 0.716 | 97.674 |
| gat | post_covid | 4.665 | 106.337 | 3.229 | 0.628 | 97.674 |
| dualtopo | post_covid | 5.688 | 173.613 | 4.885 | 0.584 | 100.000 |
| xgboost | post_covid | 5.757 | 75.754 | 3.951 | 0.617 | 90.698 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4.276 | 43.921 | 3.031 | 0.627 | 100.000 |
| arima | exclude_covid | 4.310 | 43.269 | 3.041 | 0.627 | 100.000 |
| gnn_st | post_covid | 4.346 | 43.665 | 3.051 | 0.688 | 100.000 |
| lstm | post_covid | 4.407 | 38.574 | 2.906 | 0.641 | 96.000 |
| persistence | exclude_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| persistence | post_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| gat | post_covid | 5.213 | 47.700 | 3.224 | 0.537 | 96.000 |
| lstm | exclude_covid | 5.283 | 41.728 | 3.589 | 0.635 | 96.000 |
| dualtopo | post_covid | 5.424 | 75.296 | 4.265 | 0.499 | 100.000 |
| xgboost | post_covid | 7.254 | 66.165 | 5.549 | 0.482 | 84.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.094 | 100.545 | 1.698 | 0.479 | 100.000 |
| gnn_st | post_covid | 2.368 | 109.467 | 1.883 | 0.252 | 100.000 |
| xgboost | post_covid | 2.468 | 89.073 | 1.732 | 0.327 | 100.000 |
| lstm | post_covid | 2.578 | 129.397 | 2.147 | 0.463 | 100.000 |
| persistence | exclude_covid | 2.696 | 111.923 | 2.078 | 0.193 | 100.000 |
| persistence | post_covid | 2.696 | 111.923 | 2.078 | 0.193 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| arima | exclude_covid | 3.250 | 161.485 | 2.549 | 0.169 | 100.000 |
| arima | post_covid | 3.371 | 169.327 | 2.695 | 0.165 | 100.000 |
| gat | post_covid | 3.774 | 187.777 | 3.236 | 0.182 | 100.000 |
| dualtopo | post_covid | 6.036 | 310.165 | 5.745 | 0.316 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
