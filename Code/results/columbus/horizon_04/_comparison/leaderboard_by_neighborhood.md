# Per-neighborhood leaderboard — horizon 4

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 17

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| xgboost | 10 | 8 | 5 |
| dualtopo | 4 | 5 | 0 |
| gnn_st | 2 | 2 | 1 |
| gat | 1 | 1 | 6 |
| lstm | 0 | 0 | 1 |
| seasonal_naive | 0 | 1 | 4 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `dualtopo (post_covid)`: Linden, Northland, UA/Grand, West; `gat (post_covid)`: Worthing.; `gnn_st (post_covid)`: Bexley, FarSouth; `xgboost (post_covid)`: Agler, Clinton+, Dublin, Eastside, FarEast, FarSE, FarSW, Hilliard, NESub, Wville
- **Flu season (Oct–Mar)** — `dualtopo (post_covid)`: Linden, NESub, Northland, UA/Grand, West; `gat (post_covid)`: Worthing.; `gnn_st (post_covid)`: Bexley, FarSouth; `seasonal_naive (post_covid)`: Clinton+; `xgboost (post_covid)`: Agler, Dublin, Eastside, FarEast, FarSE, FarSW, Hilliard, Wville
- **Off-season (Apr–Sep)** — `gat (post_covid)`: Bexley, FarSE, Hilliard, Linden, Northland, UA/Grand; `gnn_st (post_covid)`: FarSouth; `lstm (post_covid)`: Worthing.; `seasonal_naive (post_covid)`: Agler, Eastside, FarEast, West; `xgboost (post_covid)`: Clinton+, Dublin, FarSW, NESub, Wville

`xgboost (post_covid)` wins 10 of 17 neighborhoods. `xgboost (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Far East

*mean observed 46.6, peak 123.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 16.045 | 23.428 | 11.520 | 0.812 | 90.566 |
| dualtopo | post_covid | 16.464 | 30.523 | 12.331 | 0.779 | 69.811 |
| gnn_st | post_covid | 16.664 | 23.316 | 11.476 | 0.757 | 92.453 |
| lstm | post_covid | 21.825 | 41.512 | 16.280 | 0.464 | 94.340 |
| arima | post_covid | 22.035 | 29.039 | 15.004 | 0.533 | 92.453 |
| seasonal_naive | post_covid | 25.434 | 31.470 | 14.807 | 0.648 | 98.113 |
| persistence | post_covid | 25.737 | 40.217 | 18.571 | 0.450 | 92.453 |
| gat | post_covid | 26.101 | 36.633 | 17.366 | 0.514 | 83.019 |

### Flu season (Oct–Mar), 26 weeks scored, mean 62.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 20.073 | 22.237 | 14.625 | 0.703 | 88.462 |
| dualtopo | post_covid | 20.611 | 22.322 | 15.206 | 0.691 | 65.385 |
| gnn_st | post_covid | 21.709 | 25.550 | 16.375 | 0.523 | 88.462 |
| lstm | post_covid | 26.862 | 28.499 | 18.981 | 0.170 | 88.462 |
| arima | post_covid | 29.902 | 33.644 | 22.961 | 0.096 | 84.615 |
| persistence | post_covid | 33.906 | 42.564 | 26.210 | 0.081 | 88.462 |
| seasonal_naive | post_covid | 35.221 | 39.470 | 22.764 | 0.352 | 96.154 |
| gat | post_covid | 35.754 | 39.010 | 26.453 | 0.193 | 69.231 |

### Off-season (Apr–Sep), 27 weeks scored, mean 31.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 8.677 | 23.766 | 7.145 | 0.697 | 100.000 |
| gnn_st | post_covid | 9.555 | 21.164 | 6.758 | 0.663 | 96.296 |
| arima | post_covid | 9.594 | 24.605 | 7.341 | 0.596 | 100.000 |
| gat | post_covid | 10.309 | 34.344 | 8.615 | 0.449 | 96.296 |
| xgboost | post_covid | 10.833 | 24.574 | 8.531 | 0.789 | 92.593 |
| dualtopo | post_covid | 11.092 | 38.420 | 9.562 | 0.333 | 74.074 |
| persistence | post_covid | 13.901 | 37.956 | 11.215 | 0.401 | 96.296 |
| lstm | post_covid | 15.498 | 54.043 | 13.679 | 0.182 | 100.000 |

## Far South

*mean observed 41.1, peak 100.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 41.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.946 | 26.941 | 10.945 | 0.787 | 83.019 |
| dualtopo | post_covid | 15.695 | 31.727 | 11.640 | 0.753 | 71.698 |
| xgboost | post_covid | 16.187 | 28.249 | 12.174 | 0.836 | 83.019 |
| lstm | post_covid | 17.643 | 42.435 | 14.741 | 0.607 | 94.340 |
| arima | post_covid | 18.666 | 40.981 | 14.378 | 0.534 | 96.226 |
| persistence | post_covid | 21.030 | 45.576 | 17.010 | 0.534 | 92.453 |
| gat | post_covid | 24.177 | 37.684 | 16.794 | 0.615 | 73.585 |
| seasonal_naive | post_covid | 30.505 | 49.524 | 18.179 | 0.608 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 57.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 18.582 | 21.411 | 13.682 | 0.463 | 76.923 |
| dualtopo | post_covid | 19.304 | 26.681 | 15.186 | 0.650 | 73.077 |
| lstm | post_covid | 19.412 | 26.626 | 16.096 | 0.415 | 96.154 |
| xgboost | post_covid | 19.722 | 21.980 | 14.487 | 0.584 | 73.077 |
| arima | post_covid | 22.965 | 28.418 | 17.724 | 0.106 | 92.308 |
| persistence | post_covid | 25.474 | 38.019 | 21.445 | 0.106 | 96.154 |
| gat | post_covid | 32.728 | 45.452 | 26.492 | 0.327 | 61.538 |
| seasonal_naive | post_covid | 41.762 | 48.281 | 26.293 | 0.316 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.295 | 32.472 | 8.309 | 0.566 | 88.889 |
| gat | post_covid | 10.769 | 29.915 | 7.455 | 0.354 | 85.185 |
| dualtopo | post_covid | 11.166 | 36.773 | 8.225 | 0.196 | 70.370 |
| xgboost | post_covid | 11.822 | 34.518 | 9.948 | 0.744 | 92.593 |
| seasonal_naive | post_covid | 12.134 | 50.768 | 10.365 | 0.328 | 100.000 |
| arima | post_covid | 13.268 | 53.545 | 11.155 | 0.294 | 100.000 |
| persistence | post_covid | 15.596 | 53.134 | 12.739 | 0.294 | 88.889 |
| lstm | post_covid | 15.753 | 58.244 | 13.436 | 0.136 | 92.593 |

## West

*mean observed 38.3, peak 84.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 9.106 | 26.330 | 6.912 | 0.885 | 84.906 |
| gnn_st | post_covid | 9.607 | 22.862 | 7.831 | 0.870 | 98.113 |
| xgboost | post_covid | 10.037 | 22.729 | 8.097 | 0.868 | 100.000 |
| arima | post_covid | 14.250 | 35.236 | 10.833 | 0.667 | 96.226 |
| persistence | post_covid | 15.544 | 34.229 | 11.830 | 0.667 | 96.226 |
| lstm | post_covid | 16.847 | 48.872 | 14.100 | 0.609 | 98.113 |
| gat | post_covid | 22.494 | 40.106 | 15.334 | 0.654 | 79.245 |
| seasonal_naive | post_covid | 25.121 | 34.662 | 13.749 | 0.725 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 51.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 9.302 | 13.054 | 6.624 | 0.878 | 88.462 |
| gnn_st | post_covid | 10.970 | 20.505 | 9.317 | 0.824 | 100.000 |
| xgboost | post_covid | 11.621 | 22.900 | 10.039 | 0.777 | 100.000 |
| arima | post_covid | 16.783 | 22.753 | 12.052 | 0.492 | 92.308 |
| lstm | post_covid | 17.104 | 30.175 | 13.788 | 0.436 | 96.154 |
| persistence | post_covid | 18.377 | 27.585 | 14.129 | 0.492 | 96.154 |
| gat | post_covid | 31.143 | 47.211 | 24.764 | 0.402 | 57.692 |
| seasonal_naive | post_covid | 35.169 | 43.590 | 22.071 | 0.490 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 6.907 | 26.064 | 5.736 | 0.656 | 100.000 |
| gat | post_covid | 7.699 | 33.264 | 6.253 | 0.518 | 100.000 |
| gnn_st | post_covid | 8.080 | 25.131 | 6.399 | 0.510 | 96.296 |
| xgboost | post_covid | 8.227 | 22.564 | 6.226 | 0.681 | 100.000 |
| dualtopo | post_covid | 8.914 | 39.114 | 7.190 | 0.305 | 81.481 |
| arima | post_covid | 11.286 | 47.256 | 9.660 | 0.278 | 100.000 |
| persistence | post_covid | 12.208 | 40.627 | 9.615 | 0.278 | 96.296 |
| lstm | post_covid | 16.596 | 66.876 | 14.400 | 0.175 | 100.000 |

## Northland

*mean observed 33.4, peak 87.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 33.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 11.236 | 26.537 | 8.222 | 0.742 | 84.906 |
| xgboost | post_covid | 11.938 | 27.761 | 9.140 | 0.713 | 96.226 |
| gnn_st | post_covid | 12.941 | 29.064 | 9.316 | 0.636 | 94.340 |
| lstm | post_covid | 15.180 | 41.100 | 11.738 | 0.432 | 94.340 |
| arima | post_covid | 15.905 | 35.730 | 10.692 | 0.281 | 92.453 |
| persistence | post_covid | 19.650 | 45.154 | 14.195 | 0.281 | 92.453 |
| gat | post_covid | 20.299 | 40.478 | 13.746 | 0.401 | 83.019 |
| seasonal_naive | post_covid | 21.192 | 41.586 | 14.073 | 0.549 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 13.787 | 20.408 | 9.940 | 0.672 | 80.769 |
| xgboost | post_covid | 14.719 | 29.158 | 11.560 | 0.608 | 92.308 |
| gnn_st | post_covid | 16.473 | 28.537 | 12.214 | 0.411 | 88.462 |
| lstm | post_covid | 18.268 | 32.238 | 13.792 | 0.193 | 88.462 |
| arima | post_covid | 20.614 | 29.793 | 14.182 | 0.000 | 84.615 |
| persistence | post_covid | 25.739 | 45.266 | 19.791 | 0.000 | 84.615 |
| gat | post_covid | 27.940 | 50.057 | 21.452 | 0.087 | 65.385 |
| seasonal_naive | post_covid | 28.830 | 54.815 | 21.340 | 0.284 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 7.559 | 31.253 | 6.326 | 0.457 | 100.000 |
| dualtopo | post_covid | 8.048 | 32.439 | 6.567 | 0.395 | 88.889 |
| gnn_st | post_covid | 8.210 | 29.571 | 6.525 | 0.472 | 100.000 |
| xgboost | post_covid | 8.433 | 26.416 | 6.809 | 0.608 | 100.000 |
| seasonal_naive | post_covid | 9.013 | 28.847 | 7.074 | 0.552 | 100.000 |
| arima | post_covid | 9.348 | 41.448 | 7.331 | 0.289 | 100.000 |
| persistence | post_covid | 10.955 | 45.047 | 8.807 | 0.289 | 100.000 |
| lstm | post_covid | 11.444 | 49.633 | 9.760 | 0.128 | 100.000 |

## Linden

*mean observed 31.0, peak 76.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 31.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 10.368 | 36.791 | 8.194 | 0.779 | 73.585 |
| xgboost | post_covid | 10.651 | 31.311 | 8.452 | 0.795 | 98.113 |
| gnn_st | post_covid | 11.060 | 33.283 | 8.791 | 0.750 | 96.226 |
| arima | post_covid | 13.837 | 45.147 | 10.603 | 0.506 | 98.113 |
| lstm | post_covid | 14.586 | 52.351 | 11.796 | 0.437 | 94.340 |
| persistence | post_covid | 15.996 | 47.546 | 12.710 | 0.510 | 96.226 |
| seasonal_naive | post_covid | 17.087 | 39.050 | 10.714 | 0.640 | 100.000 |
| gat | post_covid | 17.414 | 44.556 | 12.091 | 0.552 | 83.019 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 12.216 | 23.268 | 9.900 | 0.700 | 73.077 |
| xgboost | post_covid | 12.428 | 24.032 | 9.839 | 0.636 | 96.154 |
| gnn_st | post_covid | 12.887 | 25.055 | 10.296 | 0.548 | 100.000 |
| lstm | post_covid | 16.331 | 29.458 | 12.497 | 0.186 | 88.462 |
| arima | post_covid | 16.998 | 30.342 | 13.343 | 0.177 | 96.154 |
| persistence | post_covid | 19.458 | 41.941 | 16.508 | 0.191 | 100.000 |
| seasonal_naive | post_covid | 22.995 | 39.434 | 15.133 | 0.376 | 100.000 |
| gat | post_covid | 23.681 | 45.495 | 18.517 | 0.229 | 69.231 |

### Off-season (Apr–Sep), 27 weeks scored, mean 20.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 7.431 | 43.652 | 5.903 | 0.434 | 96.296 |
| seasonal_naive | post_covid | 7.995 | 38.679 | 6.458 | 0.461 | 100.000 |
| dualtopo | post_covid | 8.206 | 49.814 | 6.551 | 0.198 | 74.074 |
| xgboost | post_covid | 8.599 | 38.319 | 7.117 | 0.403 | 100.000 |
| gnn_st | post_covid | 8.955 | 41.205 | 7.342 | 0.261 | 92.593 |
| arima | post_covid | 9.879 | 59.405 | 7.964 | 0.124 | 100.000 |
| persistence | post_covid | 11.735 | 52.945 | 9.052 | 0.123 | 92.593 |
| lstm | post_covid | 12.682 | 74.395 | 11.122 | -0.038 | 100.000 |

## Eastside

*mean observed 30.9, peak 91.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 12.984 | 32.913 | 9.261 | 0.812 | 88.679 |
| gnn_st | post_covid | 13.218 | 36.398 | 9.344 | 0.756 | 84.906 |
| dualtopo | post_covid | 13.486 | 46.042 | 9.977 | 0.758 | 66.038 |
| arima | post_covid | 16.690 | 54.749 | 11.776 | 0.505 | 92.453 |
| lstm | post_covid | 17.487 | 66.388 | 13.271 | 0.447 | 92.453 |
| persistence | post_covid | 19.077 | 56.711 | 14.524 | 0.505 | 92.453 |
| seasonal_naive | post_covid | 20.062 | 45.181 | 12.400 | 0.628 | 100.000 |
| gat | post_covid | 20.209 | 51.873 | 14.377 | 0.523 | 79.245 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 14.513 | 19.560 | 9.842 | 0.755 | 96.154 |
| gnn_st | post_covid | 15.140 | 21.142 | 10.030 | 0.634 | 92.308 |
| dualtopo | post_covid | 15.831 | 24.004 | 11.390 | 0.706 | 76.923 |
| lstm | post_covid | 18.899 | 29.763 | 13.304 | 0.269 | 92.308 |
| arima | post_covid | 20.905 | 29.240 | 14.361 | 0.208 | 84.615 |
| persistence | post_covid | 23.593 | 44.440 | 18.471 | 0.208 | 96.154 |
| gat | post_covid | 27.066 | 46.500 | 21.022 | 0.232 | 69.231 |
| seasonal_naive | post_covid | 27.211 | 42.027 | 17.853 | 0.426 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 19.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 8.778 | 48.219 | 7.149 | 0.625 | 100.000 |
| gat | post_covid | 9.809 | 57.047 | 7.978 | 0.460 | 88.889 |
| dualtopo | post_covid | 10.756 | 67.264 | 8.618 | 0.064 | 55.556 |
| gnn_st | post_covid | 11.056 | 51.089 | 8.683 | 0.368 | 77.778 |
| arima | post_covid | 11.223 | 79.313 | 9.287 | 0.168 | 100.000 |
| xgboost | post_covid | 11.318 | 45.772 | 8.701 | 0.533 | 81.481 |
| persistence | post_covid | 13.355 | 68.528 | 10.723 | 0.168 | 88.889 |
| lstm | post_covid | 16.009 | 101.657 | 13.240 | -0.133 | 92.593 |

## Agler/Cassidy

*mean observed 30.4, peak 86.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 13.861 | 45.803 | 10.087 | 0.781 | 90.566 |
| gnn_st | post_covid | 14.519 | 54.249 | 10.814 | 0.689 | 90.566 |
| dualtopo | post_covid | 14.823 | 68.811 | 11.151 | 0.702 | 69.811 |
| lstm | post_covid | 17.363 | 81.102 | 13.034 | 0.463 | 92.453 |
| arima | post_covid | 17.646 | 80.794 | 13.149 | 0.434 | 92.453 |
| seasonal_naive | post_covid | 20.038 | 58.165 | 13.627 | 0.579 | 96.226 |
| gat | post_covid | 20.676 | 70.803 | 14.609 | 0.469 | 77.358 |
| persistence | post_covid | 20.806 | 87.545 | 16.991 | 0.416 | 92.453 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 17.093 | 27.996 | 12.340 | 0.608 | 92.308 |
| gnn_st | post_covid | 17.680 | 31.034 | 12.694 | 0.425 | 92.308 |
| dualtopo | post_covid | 17.752 | 26.945 | 12.410 | 0.575 | 80.769 |
| lstm | post_covid | 20.777 | 33.884 | 14.326 | 0.075 | 88.462 |
| arima | post_covid | 21.329 | 35.608 | 15.002 | 0.119 | 84.615 |
| persistence | post_covid | 25.229 | 52.611 | 20.805 | 0.113 | 88.462 |
| seasonal_naive | post_covid | 27.003 | 54.578 | 20.687 | 0.236 | 96.154 |
| gat | post_covid | 27.557 | 44.611 | 20.375 | 0.105 | 65.385 |

### Off-season (Apr–Sep), 27 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 9.277 | 61.618 | 6.830 | 0.620 | 96.296 |
| xgboost | post_covid | 9.787 | 62.950 | 7.918 | 0.584 | 88.889 |
| gat | post_covid | 10.386 | 96.026 | 9.057 | 0.410 | 88.889 |
| gnn_st | post_covid | 10.621 | 76.603 | 9.004 | 0.373 | 88.889 |
| dualtopo | post_covid | 11.307 | 109.126 | 9.939 | 0.324 | 59.259 |
| arima | post_covid | 13.159 | 124.307 | 11.363 | 0.199 | 100.000 |
| lstm | post_covid | 13.268 | 126.571 | 11.789 | 0.268 | 96.296 |
| persistence | post_covid | 15.390 | 121.185 | 13.318 | 0.179 | 96.296 |

## Far Southwest

*mean observed 18.0, peak 47.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 18.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.540 | 27.937 | 4.667 | 0.794 | 100.000 |
| gnn_st | post_covid | 7.580 | 29.961 | 5.245 | 0.710 | 96.226 |
| dualtopo | post_covid | 7.969 | 33.330 | 5.475 | 0.690 | 86.792 |
| arima | post_covid | 9.906 | 44.936 | 7.164 | 0.391 | 96.226 |
| lstm | post_covid | 10.143 | 52.742 | 7.843 | 0.430 | 96.226 |
| persistence | post_covid | 11.699 | 48.035 | 8.430 | 0.391 | 96.226 |
| gat | post_covid | 12.895 | 51.198 | 9.093 | 0.433 | 83.019 |
| seasonal_naive | post_covid | 13.223 | 46.109 | 8.174 | 0.603 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 8.498 | 37.794 | 6.913 | 0.716 | 100.000 |
| gnn_st | post_covid | 10.094 | 40.965 | 8.069 | 0.478 | 92.308 |
| dualtopo | post_covid | 10.262 | 31.081 | 7.458 | 0.557 | 76.923 |
| lstm | post_covid | 12.558 | 49.079 | 9.732 | 0.065 | 92.308 |
| arima | post_covid | 12.996 | 45.663 | 9.985 | 0.078 | 92.308 |
| persistence | post_covid | 15.690 | 61.199 | 12.728 | 0.078 | 92.308 |
| gat | post_covid | 17.771 | 70.080 | 14.954 | 0.105 | 69.231 |
| seasonal_naive | post_covid | 18.209 | 64.254 | 12.929 | 0.352 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.796 | 18.446 | 2.504 | 0.714 | 100.000 |
| gnn_st | post_covid | 3.828 | 19.364 | 2.527 | 0.655 | 100.000 |
| gat | post_covid | 4.719 | 33.015 | 3.449 | 0.291 | 96.296 |
| dualtopo | post_covid | 4.820 | 35.495 | 3.564 | 0.248 | 96.296 |
| seasonal_naive | post_covid | 4.892 | 28.637 | 3.596 | 0.368 | 100.000 |
| arima | post_covid | 5.474 | 44.236 | 4.447 | 0.367 | 100.000 |
| persistence | post_covid | 5.622 | 35.359 | 4.292 | 0.367 | 100.000 |
| lstm | post_covid | 7.078 | 56.269 | 6.023 | 0.290 | 100.000 |

## NE Suburban

*mean observed 14.8, peak 50.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 14.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.457 | 36.169 | 4.604 | 0.733 | 98.113 |
| dualtopo | post_covid | 6.530 | 39.837 | 4.564 | 0.758 | 94.340 |
| gnn_st | post_covid | 7.356 | 34.714 | 5.072 | 0.634 | 98.113 |
| lstm | post_covid | 8.646 | 58.150 | 6.554 | 0.480 | 98.113 |
| arima | post_covid | 9.034 | 50.948 | 6.147 | 0.310 | 96.226 |
| gat | post_covid | 9.238 | 44.719 | 6.116 | 0.582 | 92.453 |
| seasonal_naive | post_covid | 9.674 | 41.354 | 6.137 | 0.651 | 100.000 |
| persistence | post_covid | 11.082 | 50.312 | 7.521 | 0.310 | 96.226 |

### Flu season (Oct–Mar), 26 weeks scored, mean 20.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 8.374 | 24.892 | 5.719 | 0.643 | 88.462 |
| xgboost | post_covid | 8.557 | 35.909 | 6.426 | 0.599 | 96.154 |
| gnn_st | post_covid | 9.778 | 34.226 | 7.108 | 0.335 | 96.154 |
| lstm | post_covid | 10.187 | 37.200 | 7.312 | 0.260 | 96.154 |
| arima | post_covid | 11.821 | 33.605 | 7.889 | -0.020 | 92.308 |
| gat | post_covid | 12.736 | 46.785 | 9.655 | 0.337 | 84.615 |
| seasonal_naive | post_covid | 13.332 | 49.722 | 9.626 | 0.436 | 100.000 |
| persistence | post_covid | 14.927 | 50.390 | 10.890 | -0.020 | 92.308 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.364 | 36.419 | 2.850 | 0.402 | 100.000 |
| gat | post_covid | 3.367 | 42.729 | 2.708 | 0.592 | 100.000 |
| seasonal_naive | post_covid | 3.542 | 33.296 | 2.778 | 0.566 | 100.000 |
| gnn_st | post_covid | 3.763 | 35.184 | 3.111 | 0.292 | 100.000 |
| dualtopo | post_covid | 4.022 | 54.229 | 3.451 | 0.358 | 100.000 |
| arima | post_covid | 5.061 | 67.648 | 4.470 | 0.174 | 100.000 |
| persistence | post_covid | 5.146 | 50.238 | 4.276 | 0.174 | 100.000 |
| lstm | post_covid | 6.842 | 78.324 | 5.824 | 0.144 | 100.000 |

## Westerville

*mean observed 13.9, peak 45.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 13.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 7.461 | 45.968 | 5.177 | 0.670 | 94.340 |
| gnn_st | post_covid | 8.404 | 51.079 | 5.883 | 0.528 | 92.453 |
| dualtopo | post_covid | 8.730 | 59.285 | 5.936 | 0.542 | 81.132 |
| lstm | post_covid | 8.915 | 67.062 | 6.310 | 0.389 | 94.340 |
| arima | post_covid | 9.805 | 74.180 | 6.879 | 0.188 | 94.340 |
| seasonal_naive | post_covid | 10.196 | 78.064 | 7.188 | 0.502 | 100.000 |
| gat | post_covid | 10.652 | 69.210 | 7.388 | 0.353 | 83.019 |
| persistence | post_covid | 12.036 | 80.787 | 8.566 | 0.212 | 94.340 |

### Flu season (Oct–Mar), 26 weeks scored, mean 18.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 9.487 | 34.237 | 6.734 | 0.573 | 92.308 |
| gnn_st | post_covid | 10.841 | 40.273 | 7.711 | 0.267 | 88.462 |
| dualtopo | post_covid | 11.276 | 34.121 | 7.717 | 0.369 | 69.231 |
| lstm | post_covid | 11.498 | 44.511 | 8.422 | 0.019 | 88.462 |
| arima | post_covid | 12.660 | 45.626 | 8.933 | -0.076 | 88.462 |
| seasonal_naive | post_covid | 13.045 | 58.895 | 9.688 | 0.335 | 100.000 |
| gat | post_covid | 14.245 | 60.968 | 10.721 | 0.077 | 69.231 |
| persistence | post_covid | 15.718 | 67.956 | 11.781 | -0.031 | 88.462 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 4.755 | 56.831 | 3.677 | 0.562 | 96.296 |
| gnn_st | post_covid | 5.046 | 61.084 | 4.124 | 0.367 | 96.296 |
| dualtopo | post_covid | 5.212 | 82.586 | 4.220 | 0.409 | 92.593 |
| gat | post_covid | 5.227 | 76.841 | 4.178 | 0.189 | 96.296 |
| lstm | post_covid | 5.358 | 87.943 | 4.276 | 0.367 | 100.000 |
| arima | post_covid | 5.862 | 100.619 | 4.901 | 0.187 | 100.000 |
| seasonal_naive | post_covid | 6.341 | 95.813 | 4.780 | 0.157 | 100.000 |
| persistence | post_covid | 6.817 | 92.668 | 5.471 | 0.196 | 100.000 |

## Bexley

*mean observed 12.4, peak 49.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 12.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.403 | 52.127 | 5.971 | 0.607 | 86.792 |
| xgboost | post_covid | 8.538 | 60.221 | 6.099 | 0.581 | 92.453 |
| dualtopo | post_covid | 8.733 | 58.253 | 6.372 | 0.596 | 71.698 |
| lstm | post_covid | 9.462 | 72.090 | 7.268 | 0.408 | 92.453 |
| arima | post_covid | 9.517 | 69.560 | 7.254 | 0.395 | 94.340 |
| persistence | post_covid | 11.382 | 70.522 | 8.295 | 0.386 | 84.906 |
| gat | post_covid | 12.077 | 84.073 | 8.482 | 0.310 | 81.132 |
| seasonal_naive | post_covid | 12.792 | 84.257 | 8.561 | 0.297 | 90.566 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.860 | 64.653 | 7.600 | 0.485 | 88.462 |
| xgboost | post_covid | 10.457 | 75.655 | 7.860 | 0.353 | 92.308 |
| dualtopo | post_covid | 10.739 | 55.548 | 7.779 | 0.467 | 69.231 |
| lstm | post_covid | 11.501 | 71.096 | 8.722 | 0.135 | 88.462 |
| arima | post_covid | 11.646 | 62.052 | 8.581 | 0.181 | 88.462 |
| persistence | post_covid | 13.640 | 74.241 | 10.146 | 0.244 | 88.462 |
| gat | post_covid | 16.319 | 115.488 | 12.956 | -0.062 | 69.231 |
| seasonal_naive | post_covid | 17.369 | 106.375 | 12.716 | -0.074 | 92.308 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 5.464 | 46.946 | 4.173 | 0.563 | 92.593 |
| seasonal_naive | post_covid | 5.541 | 58.117 | 4.559 | 0.606 | 88.889 |
| xgboost | post_covid | 6.148 | 41.980 | 4.404 | 0.312 | 92.593 |
| dualtopo | post_covid | 6.217 | 61.451 | 5.018 | 0.221 | 74.074 |
| gnn_st | post_covid | 6.706 | 37.324 | 4.402 | 0.079 | 85.185 |
| arima | post_covid | 6.871 | 78.433 | 5.976 | 0.009 | 100.000 |
| lstm | post_covid | 6.955 | 73.265 | 5.868 | 0.232 | 96.296 |
| persistence | post_covid | 8.669 | 66.126 | 6.513 | -0.040 | 81.481 |

## Worthington

*mean observed 11.8, peak 44.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 11.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 7.974 | 52.383 | 5.010 | 0.522 | 86.792 |
| xgboost | post_covid | 8.114 | 56.151 | 5.431 | 0.627 | 88.679 |
| lstm | post_covid | 8.289 | 63.595 | 5.439 | 0.485 | 96.226 |
| gnn_st | post_covid | 8.332 | 61.868 | 5.996 | 0.479 | 88.679 |
| seasonal_naive | post_covid | 8.559 | 61.813 | 5.793 | 0.451 | 90.566 |
| arima | post_covid | 8.607 | 74.194 | 6.070 | 0.327 | 96.226 |
| dualtopo | post_covid | 9.057 | 58.372 | 6.182 | 0.708 | 62.264 |
| persistence | post_covid | 10.342 | 94.985 | 7.301 | 0.295 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 16.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 10.481 | 39.910 | 6.650 | 0.306 | 80.769 |
| xgboost | post_covid | 10.633 | 46.303 | 7.534 | 0.538 | 80.769 |
| gnn_st | post_covid | 10.850 | 54.911 | 8.330 | 0.228 | 84.615 |
| seasonal_naive | post_covid | 10.943 | 42.107 | 7.442 | 0.291 | 92.308 |
| lstm | post_covid | 11.173 | 48.293 | 7.793 | 0.211 | 92.308 |
| arima | post_covid | 11.493 | 56.388 | 8.656 | 0.123 | 92.308 |
| dualtopo | post_covid | 12.056 | 45.388 | 8.797 | 0.620 | 42.308 |
| persistence | post_covid | 13.453 | 85.347 | 10.138 | 0.103 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.830 | 78.331 | 3.172 | 0.469 | 100.000 |
| arima | post_covid | 4.268 | 91.340 | 3.580 | 0.278 | 100.000 |
| gat | post_covid | 4.363 | 64.394 | 3.432 | 0.504 | 92.593 |
| xgboost | post_covid | 4.511 | 65.635 | 3.406 | 0.249 | 96.296 |
| dualtopo | post_covid | 4.588 | 70.875 | 3.664 | 0.492 | 81.481 |
| gnn_st | post_covid | 4.788 | 68.566 | 3.748 | 0.208 | 92.593 |
| seasonal_naive | post_covid | 5.335 | 80.790 | 4.206 | 0.112 | 88.889 |
| persistence | post_covid | 5.973 | 104.265 | 4.570 | 0.191 | 100.000 |

## Hilliard

*mean observed 10.3, peak 34.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 5.739 | 62.185 | 4.424 | 0.743 | 96.226 |
| gnn_st | post_covid | 6.407 | 68.137 | 4.897 | 0.652 | 92.453 |
| dualtopo | post_covid | 6.682 | 82.966 | 5.267 | 0.746 | 81.132 |
| lstm | post_covid | 7.716 | 123.472 | 6.117 | 0.386 | 96.226 |
| arima | post_covid | 7.760 | 110.016 | 6.139 | 0.347 | 98.113 |
| gat | post_covid | 8.978 | 95.779 | 6.919 | 0.445 | 84.906 |
| persistence | post_covid | 9.301 | 113.040 | 7.005 | 0.347 | 94.340 |
| seasonal_naive | post_covid | 9.588 | 126.365 | 7.238 | 0.508 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 6.793 | 50.643 | 5.497 | 0.711 | 100.000 |
| gnn_st | post_covid | 7.529 | 58.607 | 5.958 | 0.559 | 96.154 |
| dualtopo | post_covid | 8.252 | 47.560 | 6.434 | 0.716 | 73.077 |
| lstm | post_covid | 8.722 | 75.860 | 6.825 | 0.233 | 96.154 |
| arima | post_covid | 9.562 | 66.854 | 7.492 | 0.186 | 96.154 |
| persistence | post_covid | 11.126 | 94.666 | 8.865 | 0.186 | 96.154 |
| gat | post_covid | 11.994 | 82.454 | 10.097 | 0.180 | 73.077 |
| seasonal_naive | post_covid | 12.263 | 89.764 | 9.758 | 0.346 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 4.437 | 108.590 | 3.859 | 0.295 | 96.296 |
| xgboost | post_covid | 4.498 | 73.283 | 3.391 | 0.377 | 92.593 |
| dualtopo | post_covid | 4.699 | 117.010 | 4.144 | -0.042 | 88.889 |
| gnn_st | post_covid | 5.097 | 77.299 | 3.875 | 0.066 | 88.889 |
| arima | post_covid | 5.491 | 151.517 | 4.836 | -0.112 | 100.000 |
| seasonal_naive | post_covid | 5.969 | 161.559 | 4.813 | 0.067 | 100.000 |
| lstm | post_covid | 6.605 | 169.252 | 5.436 | -0.115 | 96.296 |
| persistence | post_covid | 7.114 | 130.707 | 5.214 | -0.112 | 92.593 |

## Clintonville/Near North

*mean observed 10.2, peak 27.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 4.206 | 45.773 | 3.192 | 0.814 | 100.000 |
| seasonal_naive | post_covid | 4.314 | 41.975 | 3.353 | 0.789 | 100.000 |
| gnn_st | post_covid | 4.327 | 44.108 | 3.264 | 0.828 | 100.000 |
| dualtopo | post_covid | 5.198 | 54.705 | 3.879 | 0.830 | 86.792 |
| lstm | post_covid | 5.559 | 65.287 | 4.020 | 0.587 | 96.226 |
| arima | post_covid | 5.584 | 65.972 | 4.018 | 0.613 | 98.113 |
| gat | post_covid | 5.821 | 54.426 | 4.025 | 0.585 | 94.340 |
| persistence | post_covid | 5.892 | 67.813 | 4.535 | 0.613 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 4.810 | 30.657 | 3.714 | 0.704 | 100.000 |
| gnn_st | post_covid | 5.129 | 27.109 | 3.814 | 0.813 | 100.000 |
| xgboost | post_covid | 5.154 | 32.964 | 4.106 | 0.745 | 100.000 |
| dualtopo | post_covid | 6.602 | 31.756 | 5.182 | 0.788 | 76.923 |
| arima | post_covid | 7.133 | 33.854 | 5.234 | 0.441 | 96.154 |
| persistence | post_covid | 7.162 | 43.440 | 5.610 | 0.441 | 100.000 |
| lstm | post_covid | 7.183 | 37.018 | 5.398 | 0.343 | 92.308 |
| gat | post_covid | 7.676 | 38.826 | 5.681 | 0.335 | 88.462 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.022 | 58.108 | 2.311 | 0.731 | 100.000 |
| gat | post_covid | 3.125 | 69.448 | 2.431 | 0.498 | 100.000 |
| lstm | post_covid | 3.314 | 92.509 | 2.693 | 0.438 | 100.000 |
| dualtopo | post_covid | 3.328 | 76.804 | 2.625 | 0.555 | 96.296 |
| gnn_st | post_covid | 3.381 | 60.478 | 2.735 | 0.494 | 100.000 |
| arima | post_covid | 3.494 | 96.900 | 2.847 | 0.273 | 100.000 |
| seasonal_naive | post_covid | 3.777 | 52.874 | 3.006 | 0.373 | 100.000 |
| persistence | post_covid | 4.331 | 91.284 | 3.500 | 0.273 | 100.000 |

## Far Southeast

*mean observed 5.6, peak 14.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.026 | 80.936 | 2.450 | 0.529 | 100.000 |
| dualtopo | post_covid | 3.149 | 66.023 | 2.498 | 0.465 | 94.340 |
| gnn_st | post_covid | 3.272 | 68.236 | 2.545 | 0.431 | 100.000 |
| lstm | post_covid | 3.490 | 86.290 | 2.806 | 0.235 | 100.000 |
| arima | post_covid | 3.555 | 84.412 | 2.839 | 0.090 | 100.000 |
| persistence | post_covid | 4.722 | 106.083 | 3.692 | 0.081 | 100.000 |
| gat | post_covid | 4.876 | 93.400 | 3.527 | 0.313 | 94.340 |
| seasonal_naive | post_covid | 6.079 | 118.809 | 4.209 | 0.365 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.675 | 79.298 | 2.993 | 0.336 | 100.000 |
| gnn_st | post_covid | 3.851 | 71.688 | 3.071 | 0.241 | 100.000 |
| dualtopo | post_covid | 3.960 | 61.507 | 3.282 | 0.285 | 88.462 |
| lstm | post_covid | 4.028 | 72.300 | 3.261 | -0.006 | 100.000 |
| arima | post_covid | 4.334 | 69.278 | 3.435 | -0.095 | 100.000 |
| persistence | post_covid | 5.680 | 106.951 | 4.544 | -0.077 | 100.000 |
| gat | post_covid | 6.647 | 125.410 | 5.474 | 0.008 | 88.462 |
| seasonal_naive | post_covid | 8.088 | 148.154 | 6.035 | 0.164 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 4.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 2.030 | 62.575 | 1.652 | 0.261 | 100.000 |
| dualtopo | post_covid | 2.087 | 70.371 | 1.743 | 0.021 | 100.000 |
| xgboost | post_covid | 2.229 | 82.514 | 1.927 | 0.032 | 100.000 |
| arima | post_covid | 2.591 | 98.985 | 2.264 | -0.296 | 100.000 |
| gnn_st | post_covid | 2.594 | 64.911 | 2.039 | -0.156 | 100.000 |
| lstm | post_covid | 2.878 | 99.762 | 2.368 | -0.215 | 100.000 |
| seasonal_naive | post_covid | 3.087 | 90.550 | 2.450 | 0.185 | 96.296 |
| persistence | post_covid | 3.565 | 105.248 | 2.871 | -0.229 | 100.000 |

## Dublin

*mean observed 5.4, peak 16.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.720 | 28140036.291 | 2.046 | 0.672 | 100.000 |
| gnn_st | post_covid | 3.383 | 16049400.155 | 2.467 | 0.538 | 98.113 |
| gat | post_covid | 3.384 | 55.082 | 2.430 | 0.551 | 92.453 |
| arima | post_covid | 3.480 | 72.799 | 2.688 | 0.362 | 100.000 |
| lstm | post_covid | 3.481 | 67.843 | 2.598 | 0.404 | 98.113 |
| seasonal_naive | post_covid | 3.619 | 54.484 | 2.775 | 0.632 | 96.226 |
| dualtopo | post_covid | 3.628 | 58.367 | 2.743 | 0.639 | 83.019 |
| persistence | post_covid | 4.026 | 87.649 | 3.235 | 0.361 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 3.198 | 32.106 | 2.255 | 0.486 | 100.000 |
| gnn_st | post_covid | 4.044 | 41.797 | 2.909 | 0.199 | 96.154 |
| gat | post_covid | 4.253 | 41.246 | 3.088 | 0.331 | 92.308 |
| lstm | post_covid | 4.294 | 46.552 | 3.213 | 0.083 | 96.154 |
| arima | post_covid | 4.345 | 51.445 | 3.344 | -0.022 | 100.000 |
| dualtopo | post_covid | 4.549 | 44.316 | 3.572 | 0.524 | 73.077 |
| seasonal_naive | post_covid | 4.582 | 57.247 | 3.752 | 0.479 | 100.000 |
| persistence | post_covid | 4.903 | 74.565 | 3.928 | -0.015 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 3.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 2.162 | 55237818.099 | 1.844 | 0.455 | 100.000 |
| gat | post_covid | 2.247 | 68.918 | 1.796 | 0.485 | 92.593 |
| seasonal_naive | post_covid | 2.342 | 51.722 | 1.835 | 0.494 | 92.593 |
| arima | post_covid | 2.365 | 94.152 | 2.057 | 0.165 | 100.000 |
| dualtopo | post_covid | 2.431 | 72.419 | 1.943 | 0.249 | 92.593 |
| lstm | post_covid | 2.456 | 89.134 | 2.005 | 0.122 | 100.000 |
| gnn_st | post_covid | 2.592 | 31504337.833 | 2.041 | 0.228 | 100.000 |
| persistence | post_covid | 2.944 | 100.733 | 2.568 | 0.190 | 96.296 |

## UA/Grandview

*mean observed 4.4, peak 15.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 4.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 2.877 | 42.520 | 1.755 | 0.600 | 94.340 |
| xgboost | post_covid | 3.005 | 69.416 | 2.207 | 0.567 | 100.000 |
| gnn_st | post_covid | 3.059 | 45.097 | 1.932 | 0.538 | 96.226 |
| lstm | post_covid | 3.311 | 63.167 | 2.170 | 0.361 | 96.226 |
| arima | post_covid | 3.455 | 58.167 | 2.201 | 0.295 | 94.340 |
| persistence | post_covid | 4.265 | 69.563 | 2.792 | 0.276 | 90.566 |
| gat | post_covid | 4.275 | 57.121 | 2.746 | 0.434 | 94.340 |
| seasonal_naive | post_covid | 5.480 | 87.113 | 3.608 | 0.364 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 6.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 3.805 | 28.728 | 2.274 | 0.418 | 88.462 |
| xgboost | post_covid | 3.885 | 59.952 | 3.030 | 0.216 | 100.000 |
| gnn_st | post_covid | 4.073 | 38.690 | 2.612 | 0.187 | 92.308 |
| lstm | post_covid | 4.200 | 39.506 | 2.581 | 0.039 | 92.308 |
| arima | post_covid | 4.583 | 40.158 | 2.894 | -0.015 | 88.462 |
| persistence | post_covid | 5.692 | 61.771 | 3.941 | -0.027 | 88.462 |
| gat | post_covid | 5.933 | 68.300 | 4.458 | 0.130 | 88.462 |
| seasonal_naive | post_covid | 7.535 | 96.068 | 5.736 | 0.113 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 2.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 1.402 | 45.495 | 1.098 | 0.357 | 100.000 |
| dualtopo | post_covid | 1.518 | 56.865 | 1.255 | 0.026 | 100.000 |
| gnn_st | post_covid | 1.548 | 51.761 | 1.278 | 0.243 | 100.000 |
| xgboost | post_covid | 1.788 | 79.258 | 1.414 | 0.192 | 100.000 |
| arima | post_covid | 1.791 | 76.897 | 1.533 | 0.147 | 100.000 |
| seasonal_naive | post_covid | 2.067 | 77.800 | 1.560 | 0.161 | 96.296 |
| persistence | post_covid | 2.124 | 77.667 | 1.686 | 0.144 | 92.593 |
| lstm | post_covid | 2.129 | 87.775 | 1.774 | 0.028 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
