# Per-neighborhood leaderboard — horizon 1

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 17

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_st | 9 | 11 | 7 |
| gnn_st_v2 | 8 | 6 | 4 |
| arima | 0 | 0 | 1 |
| gat | 0 | 0 | 2 |
| seasonal_naive | 0 | 0 | 1 |
| xgboost | 0 | 0 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gnn_st (post_covid)`: Bexley, Clinton+, Eastside, FarSouth, Linden, Northland, UA/Grand, West, Worthing.; `gnn_st_v2 (post_covid)`: Agler, Dublin, FarEast, FarSE, FarSW, Hilliard, NESub, Wville
- **Flu season (Oct–Mar)** — `gnn_st (post_covid)`: Bexley, Clinton+, Eastside, FarSE, FarSouth, Hilliard, Linden, Northland, UA/Grand, West, Worthing.; `gnn_st_v2 (post_covid)`: Agler, Dublin, FarEast, FarSW, NESub, Wville
- **Off-season (Apr–Sep)** — `arima (post_covid)`: Dublin; `gat (post_covid)`: FarSE, Worthing.; `gnn_st (post_covid)`: Clinton+, Eastside, FarEast, FarSouth, Linden, UA/Grand, West; `gnn_st_v2 (post_covid)`: Agler, Hilliard, NESub, Northland; `seasonal_naive (post_covid)`: Bexley; `xgboost (post_covid)`: FarSW, Wville

`gnn_st (post_covid)` wins 9 of 17 neighborhoods. `gnn_st (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Far East

*mean observed 46.6, peak 123.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 9.861 | 16.874 | 7.176 | 0.917 | 96.226 |
| gnn_st | post_covid | 9.885 | 16.962 | 7.218 | 0.917 | 96.226 |
| persistence | post_covid | 12.736 | 21.742 | 9.432 | 0.866 | 96.226 |
| arima | post_covid | 13.545 | 25.492 | 10.278 | 0.840 | 83.019 |
| lstm | post_covid | 13.752 | 26.999 | 10.746 | 0.832 | 92.453 |
| xgboost | post_covid | 14.352 | 23.341 | 10.905 | 0.849 | 90.566 |
| gat | post_covid | 17.552 | 34.105 | 12.503 | 0.712 | 77.358 |
| dualtopo | post_covid | 25.144 | 45.189 | 17.866 | 0.729 | 58.491 |
| seasonal_naive | post_covid | 25.434 | 31.470 | 14.807 | 0.648 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 62.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 11.844 | 14.762 | 8.788 | 0.883 | 96.154 |
| gnn_st | post_covid | 11.889 | 14.961 | 8.888 | 0.882 | 96.154 |
| persistence | post_covid | 16.357 | 22.161 | 13.162 | 0.785 | 96.154 |
| lstm | post_covid | 16.645 | 22.294 | 13.154 | 0.744 | 92.308 |
| arima | post_covid | 16.974 | 22.443 | 13.631 | 0.778 | 76.923 |
| xgboost | post_covid | 16.993 | 21.004 | 12.941 | 0.753 | 92.308 |
| gat | post_covid | 22.082 | 23.736 | 15.170 | 0.497 | 73.077 |
| dualtopo | post_covid | 32.481 | 30.884 | 23.316 | 0.572 | 50.000 |
| seasonal_naive | post_covid | 35.221 | 39.470 | 22.764 | 0.352 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 31.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.463 | 18.890 | 5.610 | 0.769 | 96.296 |
| gnn_st_v2 | post_covid | 7.469 | 18.908 | 5.624 | 0.769 | 96.296 |
| persistence | post_covid | 7.796 | 21.338 | 5.840 | 0.772 | 96.296 |
| seasonal_naive | post_covid | 8.677 | 23.766 | 7.145 | 0.697 | 100.000 |
| arima | post_covid | 9.094 | 28.429 | 7.049 | 0.702 | 88.889 |
| lstm | post_covid | 10.219 | 31.530 | 8.427 | 0.582 | 92.593 |
| xgboost | post_covid | 11.235 | 25.590 | 8.943 | 0.792 | 88.889 |
| gat | post_covid | 11.626 | 44.089 | 9.935 | 0.553 | 81.481 |
| dualtopo | post_covid | 15.004 | 58.963 | 12.618 | 0.358 | 66.667 |

## Far South

*mean observed 41.1, peak 100.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 41.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.180 | 26.852 | 10.106 | 0.812 | 90.566 |
| gnn_st_v2 | post_covid | 13.219 | 26.979 | 10.143 | 0.812 | 90.566 |
| lstm | post_covid | 14.067 | 28.106 | 10.661 | 0.806 | 84.906 |
| gat | post_covid | 14.119 | 33.348 | 10.910 | 0.767 | 79.245 |
| arima | post_covid | 16.203 | 33.991 | 12.715 | 0.683 | 75.472 |
| persistence | post_covid | 16.227 | 32.646 | 12.092 | 0.725 | 86.792 |
| xgboost | post_covid | 16.715 | 29.299 | 12.723 | 0.804 | 79.245 |
| dualtopo | post_covid | 23.082 | 48.410 | 17.137 | 0.746 | 54.717 |
| seasonal_naive | post_covid | 30.505 | 49.524 | 18.179 | 0.608 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 57.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 16.075 | 20.478 | 12.536 | 0.594 | 88.462 |
| gnn_st_v2 | post_covid | 16.111 | 20.578 | 12.583 | 0.594 | 88.462 |
| gat | post_covid | 16.273 | 21.293 | 12.612 | 0.593 | 80.769 |
| lstm | post_covid | 17.400 | 23.994 | 14.196 | 0.658 | 84.615 |
| xgboost | post_covid | 20.408 | 23.367 | 15.318 | 0.500 | 69.231 |
| persistence | post_covid | 20.572 | 27.569 | 15.694 | 0.377 | 84.615 |
| arima | post_covid | 20.586 | 28.270 | 16.789 | 0.367 | 61.538 |
| dualtopo | post_covid | 29.719 | 34.332 | 23.274 | 0.553 | 38.462 |
| seasonal_naive | post_covid | 41.762 | 48.281 | 26.293 | 0.316 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.599 | 33.227 | 7.765 | 0.592 | 92.593 |
| gnn_st_v2 | post_covid | 9.645 | 33.379 | 7.793 | 0.589 | 92.593 |
| lstm | post_covid | 9.842 | 32.217 | 7.257 | 0.534 | 85.185 |
| arima | post_covid | 10.356 | 39.713 | 8.791 | 0.528 | 88.889 |
| persistence | post_covid | 10.458 | 37.723 | 8.624 | 0.548 | 88.889 |
| gat | post_covid | 11.674 | 45.404 | 9.271 | 0.398 | 77.778 |
| seasonal_naive | post_covid | 12.134 | 50.768 | 10.365 | 0.328 | 100.000 |
| xgboost | post_covid | 12.139 | 35.231 | 10.224 | 0.741 | 88.889 |
| dualtopo | post_covid | 13.976 | 62.488 | 11.228 | 0.263 | 70.370 |

## West

*mean observed 38.3, peak 84.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.923 | 16.451 | 5.266 | 0.937 | 100.000 |
| gnn_st_v2 | post_covid | 6.955 | 16.486 | 5.286 | 0.937 | 100.000 |
| persistence | post_covid | 8.203 | 18.893 | 6.310 | 0.907 | 98.113 |
| xgboost | post_covid | 9.986 | 22.813 | 8.138 | 0.873 | 98.113 |
| arima | post_covid | 10.650 | 27.013 | 7.915 | 0.854 | 92.453 |
| lstm | post_covid | 11.442 | 29.258 | 9.225 | 0.912 | 100.000 |
| gat | post_covid | 12.090 | 37.618 | 10.094 | 0.848 | 77.358 |
| dualtopo | post_covid | 19.092 | 51.946 | 15.715 | 0.835 | 52.830 |
| seasonal_naive | post_covid | 25.121 | 34.662 | 13.749 | 0.725 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 51.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.925 | 13.360 | 6.087 | 0.902 | 100.000 |
| gnn_st_v2 | post_covid | 7.974 | 13.424 | 6.124 | 0.901 | 100.000 |
| persistence | post_covid | 9.844 | 15.620 | 7.683 | 0.845 | 100.000 |
| xgboost | post_covid | 11.252 | 21.984 | 9.751 | 0.778 | 100.000 |
| arima | post_covid | 12.622 | 17.553 | 9.206 | 0.771 | 92.308 |
| lstm | post_covid | 12.784 | 21.285 | 10.074 | 0.893 | 100.000 |
| gat | post_covid | 12.969 | 24.237 | 10.958 | 0.729 | 80.769 |
| dualtopo | post_covid | 22.792 | 32.968 | 18.859 | 0.797 | 46.154 |
| seasonal_naive | post_covid | 35.169 | 43.590 | 22.071 | 0.490 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.797 | 19.428 | 4.475 | 0.781 | 100.000 |
| gnn_st_v2 | post_covid | 5.807 | 19.436 | 4.479 | 0.781 | 100.000 |
| persistence | post_covid | 6.226 | 22.044 | 4.988 | 0.727 | 96.296 |
| seasonal_naive | post_covid | 6.907 | 26.064 | 5.736 | 0.656 | 100.000 |
| arima | post_covid | 8.322 | 36.123 | 6.672 | 0.605 | 92.593 |
| xgboost | post_covid | 8.592 | 23.612 | 6.585 | 0.685 | 96.296 |
| lstm | post_covid | 9.980 | 36.936 | 8.407 | 0.570 | 100.000 |
| gat | post_covid | 11.178 | 50.503 | 9.262 | 0.652 | 74.074 |
| dualtopo | post_covid | 14.671 | 70.221 | 12.687 | 0.327 | 59.259 |

## Northland

*mean observed 33.4, peak 87.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 33.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.570 | 19.554 | 5.889 | 0.886 | 100.000 |
| gnn_st_v2 | post_covid | 7.590 | 19.548 | 5.897 | 0.886 | 100.000 |
| persistence | post_covid | 9.518 | 24.521 | 7.061 | 0.830 | 98.113 |
| lstm | post_covid | 9.666 | 28.758 | 8.057 | 0.828 | 100.000 |
| arima | post_covid | 10.204 | 27.518 | 7.780 | 0.813 | 90.566 |
| xgboost | post_covid | 11.878 | 28.241 | 9.469 | 0.724 | 100.000 |
| gat | post_covid | 12.073 | 33.007 | 9.027 | 0.698 | 84.906 |
| dualtopo | post_covid | 16.520 | 40.099 | 11.827 | 0.667 | 71.698 |
| seasonal_naive | post_covid | 21.192 | 41.586 | 14.073 | 0.549 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.975 | 17.579 | 7.122 | 0.868 | 100.000 |
| gnn_st_v2 | post_covid | 9.010 | 17.592 | 7.140 | 0.867 | 100.000 |
| lstm | post_covid | 11.034 | 23.762 | 9.205 | 0.823 | 100.000 |
| persistence | post_covid | 11.319 | 19.878 | 8.146 | 0.807 | 96.154 |
| arima | post_covid | 12.222 | 21.486 | 9.730 | 0.807 | 88.462 |
| xgboost | post_covid | 14.463 | 29.512 | 11.983 | 0.589 | 100.000 |
| gat | post_covid | 15.190 | 28.415 | 11.642 | 0.541 | 80.769 |
| dualtopo | post_covid | 21.125 | 30.636 | 15.049 | 0.526 | 65.385 |
| seasonal_naive | post_covid | 28.830 | 54.815 | 21.340 | 0.284 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 5.908 | 21.432 | 4.700 | 0.722 | 100.000 |
| gnn_st | post_covid | 5.908 | 21.456 | 4.701 | 0.722 | 100.000 |
| persistence | post_covid | 7.380 | 28.991 | 6.016 | 0.637 | 100.000 |
| arima | post_covid | 7.781 | 33.327 | 5.901 | 0.579 | 92.593 |
| gat | post_covid | 7.997 | 37.428 | 6.509 | 0.596 | 88.889 |
| lstm | post_covid | 8.135 | 33.568 | 6.951 | 0.473 | 100.000 |
| xgboost | post_covid | 8.690 | 27.017 | 7.048 | 0.606 | 100.000 |
| seasonal_naive | post_covid | 9.013 | 28.847 | 7.074 | 0.552 | 100.000 |
| dualtopo | post_covid | 10.294 | 49.212 | 8.725 | 0.395 | 77.778 |

## Linden

*mean observed 31.0, peak 76.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 31.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.507 | 25.579 | 5.863 | 0.885 | 96.226 |
| gnn_st_v2 | post_covid | 7.509 | 25.565 | 5.857 | 0.885 | 96.226 |
| arima | post_covid | 9.164 | 31.668 | 7.566 | 0.820 | 96.226 |
| lstm | post_covid | 9.225 | 34.695 | 7.725 | 0.823 | 94.340 |
| persistence | post_covid | 9.582 | 30.351 | 7.677 | 0.820 | 98.113 |
| gat | post_covid | 10.645 | 40.171 | 8.107 | 0.757 | 79.245 |
| xgboost | post_covid | 10.771 | 32.480 | 8.804 | 0.782 | 98.113 |
| dualtopo | post_covid | 16.271 | 53.857 | 12.280 | 0.728 | 60.377 |
| seasonal_naive | post_covid | 17.087 | 39.050 | 10.714 | 0.640 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.788 | 18.387 | 6.834 | 0.812 | 96.154 |
| gnn_st_v2 | post_covid | 8.790 | 18.351 | 6.819 | 0.812 | 96.154 |
| lstm | post_covid | 10.026 | 22.244 | 8.494 | 0.746 | 96.154 |
| arima | post_covid | 11.158 | 23.207 | 9.548 | 0.703 | 92.308 |
| persistence | post_covid | 11.713 | 25.029 | 9.744 | 0.703 | 100.000 |
| xgboost | post_covid | 12.478 | 25.512 | 10.237 | 0.586 | 100.000 |
| gat | post_covid | 12.601 | 24.414 | 9.622 | 0.559 | 73.077 |
| dualtopo | post_covid | 20.412 | 31.922 | 15.669 | 0.592 | 50.000 |
| seasonal_naive | post_covid | 22.995 | 39.434 | 15.133 | 0.376 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 20.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.020 | 32.504 | 4.927 | 0.698 | 96.296 |
| gnn_st_v2 | post_covid | 6.023 | 32.512 | 4.931 | 0.698 | 96.296 |
| arima | post_covid | 6.706 | 39.815 | 5.657 | 0.639 | 100.000 |
| persistence | post_covid | 6.937 | 35.476 | 5.685 | 0.639 | 96.296 |
| seasonal_naive | post_covid | 7.995 | 38.679 | 6.458 | 0.461 | 100.000 |
| gat | post_covid | 8.339 | 55.344 | 6.647 | 0.600 | 85.185 |
| lstm | post_covid | 8.382 | 46.685 | 6.985 | 0.411 | 92.593 |
| xgboost | post_covid | 8.820 | 39.189 | 7.425 | 0.409 | 96.296 |
| dualtopo | post_covid | 10.882 | 74.980 | 9.017 | 0.163 | 70.370 |

## Eastside

*mean observed 30.9, peak 91.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.780 | 29.801 | 7.864 | 0.829 | 90.566 |
| gnn_st_v2 | post_covid | 10.840 | 29.890 | 7.907 | 0.827 | 90.566 |
| lstm | post_covid | 11.593 | 40.535 | 8.847 | 0.810 | 92.453 |
| gat | post_covid | 13.559 | 47.350 | 9.403 | 0.702 | 77.358 |
| xgboost | post_covid | 13.595 | 34.107 | 9.748 | 0.761 | 88.679 |
| arima | post_covid | 14.698 | 42.357 | 10.118 | 0.642 | 81.132 |
| persistence | post_covid | 14.841 | 38.544 | 10.535 | 0.695 | 92.453 |
| dualtopo | post_covid | 19.653 | 66.834 | 14.002 | 0.675 | 62.264 |
| seasonal_naive | post_covid | 20.062 | 45.181 | 12.400 | 0.628 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.406 | 21.657 | 9.709 | 0.709 | 88.462 |
| gnn_st_v2 | post_covid | 13.502 | 21.845 | 9.786 | 0.705 | 88.462 |
| lstm | post_covid | 13.963 | 25.954 | 10.553 | 0.711 | 92.308 |
| xgboost | post_covid | 15.602 | 22.943 | 10.870 | 0.633 | 96.154 |
| gat | post_covid | 16.756 | 23.444 | 11.306 | 0.492 | 73.077 |
| arima | post_covid | 18.710 | 24.994 | 12.323 | 0.433 | 76.923 |
| persistence | post_covid | 18.809 | 31.198 | 13.787 | 0.490 | 92.308 |
| dualtopo | post_covid | 25.140 | 33.081 | 17.707 | 0.594 | 57.692 |
| seasonal_naive | post_covid | 27.211 | 42.027 | 17.853 | 0.426 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 19.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.420 | 37.644 | 6.087 | 0.758 | 92.593 |
| gnn_st_v2 | post_covid | 7.425 | 37.638 | 6.097 | 0.758 | 92.593 |
| lstm | post_covid | 8.722 | 54.575 | 7.204 | 0.600 | 92.593 |
| seasonal_naive | post_covid | 8.778 | 48.219 | 7.149 | 0.625 | 100.000 |
| arima | post_covid | 9.324 | 59.077 | 7.994 | 0.563 | 85.185 |
| gat | post_covid | 9.512 | 70.371 | 7.571 | 0.590 | 81.481 |
| persistence | post_covid | 9.577 | 45.618 | 7.404 | 0.602 | 92.593 |
| xgboost | post_covid | 11.330 | 44.858 | 8.668 | 0.508 | 81.481 |
| dualtopo | post_covid | 12.230 | 99.336 | 10.433 | 0.071 | 66.667 |

## Agler/Cassidy

*mean observed 30.4, peak 86.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 10.155 | 43.349 | 7.775 | 0.855 | 92.453 |
| gnn_st | post_covid | 10.166 | 43.469 | 7.795 | 0.855 | 92.453 |
| lstm | post_covid | 12.092 | 59.411 | 9.346 | 0.787 | 90.566 |
| xgboost | post_covid | 12.450 | 43.664 | 9.250 | 0.802 | 92.453 |
| persistence | post_covid | 13.189 | 52.310 | 9.162 | 0.770 | 92.453 |
| gat | post_covid | 14.759 | 74.603 | 10.607 | 0.659 | 71.698 |
| arima | post_covid | 14.878 | 65.288 | 11.261 | 0.653 | 71.698 |
| dualtopo | post_covid | 19.787 | 96.004 | 15.262 | 0.658 | 50.943 |
| seasonal_naive | post_covid | 20.038 | 58.165 | 13.627 | 0.579 | 96.226 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 12.021 | 24.495 | 9.129 | 0.766 | 92.308 |
| gnn_st | post_covid | 12.022 | 24.595 | 9.149 | 0.766 | 92.308 |
| lstm | post_covid | 13.881 | 25.970 | 9.992 | 0.664 | 88.462 |
| xgboost | post_covid | 14.886 | 26.426 | 10.867 | 0.662 | 96.154 |
| persistence | post_covid | 15.438 | 26.517 | 10.402 | 0.652 | 92.308 |
| gat | post_covid | 17.705 | 27.588 | 11.730 | 0.377 | 76.923 |
| arima | post_covid | 17.806 | 28.243 | 12.831 | 0.518 | 73.077 |
| dualtopo | post_covid | 24.427 | 37.838 | 18.189 | 0.454 | 50.000 |
| seasonal_naive | post_covid | 27.003 | 54.578 | 20.687 | 0.236 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 7.955 | 61.504 | 6.472 | 0.712 | 92.593 |
| gnn_st | post_covid | 7.979 | 61.643 | 6.492 | 0.709 | 92.593 |
| seasonal_naive | post_covid | 9.277 | 61.618 | 6.830 | 0.620 | 96.296 |
| xgboost | post_covid | 9.533 | 60.264 | 7.694 | 0.600 | 88.889 |
| lstm | post_covid | 10.074 | 91.614 | 8.723 | 0.519 | 92.593 |
| persistence | post_covid | 10.581 | 77.148 | 7.968 | 0.580 | 92.593 |
| gat | post_covid | 11.213 | 119.877 | 9.526 | 0.564 | 66.667 |
| arima | post_covid | 11.366 | 100.960 | 9.750 | 0.456 | 70.370 |
| dualtopo | post_covid | 13.926 | 152.015 | 12.443 | 0.307 | 51.852 |

## Far Southwest

*mean observed 18.0, peak 47.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 18.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 5.448 | 24.881 | 3.751 | 0.861 | 96.226 |
| gnn_st | post_covid | 5.450 | 24.864 | 3.757 | 0.861 | 96.226 |
| arima | post_covid | 5.868 | 29.037 | 4.375 | 0.834 | 96.226 |
| persistence | post_covid | 6.111 | 29.410 | 4.530 | 0.834 | 98.113 |
| xgboost | post_covid | 6.624 | 27.643 | 4.790 | 0.796 | 100.000 |
| lstm | post_covid | 7.056 | 35.970 | 5.366 | 0.807 | 98.113 |
| gat | post_covid | 8.821 | 48.337 | 6.707 | 0.598 | 86.792 |
| dualtopo | post_covid | 10.634 | 53.902 | 8.222 | 0.656 | 66.038 |
| seasonal_naive | post_covid | 13.223 | 46.109 | 8.174 | 0.603 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 6.391 | 25.139 | 4.462 | 0.831 | 96.154 |
| gnn_st | post_covid | 6.401 | 25.284 | 4.492 | 0.831 | 96.154 |
| arima | post_covid | 6.787 | 25.884 | 5.100 | 0.805 | 96.154 |
| persistence | post_covid | 7.089 | 28.267 | 5.340 | 0.805 | 100.000 |
| xgboost | post_covid | 8.490 | 36.559 | 6.976 | 0.704 | 100.000 |
| lstm | post_covid | 8.870 | 37.725 | 7.103 | 0.720 | 96.154 |
| gat | post_covid | 10.960 | 44.155 | 8.282 | 0.353 | 76.923 |
| dualtopo | post_covid | 13.372 | 40.437 | 10.229 | 0.493 | 53.846 |
| seasonal_naive | post_covid | 18.209 | 64.254 | 12.929 | 0.352 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 4.087 | 19.057 | 2.685 | 0.714 | 100.000 |
| gnn_st | post_covid | 4.343 | 24.460 | 3.049 | 0.483 | 96.296 |
| gnn_st_v2 | post_covid | 4.350 | 24.632 | 3.066 | 0.482 | 96.296 |
| lstm | post_covid | 4.687 | 34.280 | 3.693 | 0.539 | 100.000 |
| arima | post_covid | 4.821 | 32.074 | 3.678 | 0.278 | 96.296 |
| seasonal_naive | post_covid | 4.892 | 28.637 | 3.596 | 0.368 | 100.000 |
| persistence | post_covid | 4.991 | 30.510 | 3.751 | 0.278 | 96.296 |
| gat | post_covid | 6.087 | 52.365 | 5.191 | 0.266 | 96.296 |
| dualtopo | post_covid | 7.056 | 66.868 | 6.290 | 0.297 | 77.778 |

## NE Suburban

*mean observed 14.8, peak 50.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 14.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 5.237 | 28.204 | 3.513 | 0.834 | 98.113 |
| gnn_st | post_covid | 5.251 | 28.283 | 3.522 | 0.833 | 98.113 |
| xgboost | post_covid | 6.170 | 32.859 | 4.195 | 0.760 | 98.113 |
| lstm | post_covid | 6.304 | 39.611 | 4.771 | 0.784 | 98.113 |
| persistence | post_covid | 6.444 | 31.413 | 4.468 | 0.767 | 96.226 |
| arima | post_covid | 6.541 | 37.742 | 4.396 | 0.722 | 94.340 |
| gat | post_covid | 6.606 | 46.564 | 4.845 | 0.764 | 96.226 |
| dualtopo | post_covid | 9.454 | 58.911 | 6.603 | 0.683 | 73.585 |
| seasonal_naive | post_covid | 9.674 | 41.354 | 6.137 | 0.651 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 20.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 6.712 | 22.694 | 4.428 | 0.757 | 96.154 |
| gnn_st | post_covid | 6.732 | 22.727 | 4.440 | 0.756 | 96.154 |
| lstm | post_covid | 7.897 | 33.248 | 6.129 | 0.675 | 96.154 |
| xgboost | post_covid | 8.043 | 30.257 | 5.491 | 0.640 | 96.154 |
| gat | post_covid | 8.182 | 29.825 | 5.853 | 0.606 | 92.308 |
| arima | post_covid | 8.445 | 27.904 | 5.576 | 0.626 | 88.462 |
| persistence | post_covid | 8.498 | 30.515 | 6.288 | 0.662 | 96.154 |
| dualtopo | post_covid | 12.032 | 33.828 | 8.208 | 0.532 | 69.231 |
| seasonal_naive | post_covid | 13.332 | 49.722 | 9.626 | 0.436 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 3.233 | 33.509 | 2.631 | 0.571 | 100.000 |
| gnn_st | post_covid | 3.239 | 33.632 | 2.639 | 0.569 | 100.000 |
| persistence | post_covid | 3.459 | 32.278 | 2.715 | 0.567 | 96.296 |
| xgboost | post_covid | 3.525 | 35.364 | 2.948 | 0.347 | 100.000 |
| seasonal_naive | post_covid | 3.542 | 33.296 | 2.778 | 0.566 | 100.000 |
| arima | post_covid | 3.912 | 47.215 | 3.260 | 0.500 | 100.000 |
| lstm | post_covid | 4.238 | 45.738 | 3.462 | 0.512 | 100.000 |
| gat | post_covid | 4.605 | 62.684 | 3.874 | 0.693 | 100.000 |
| dualtopo | post_covid | 6.002 | 83.065 | 5.057 | 0.348 | 77.778 |

## Westerville

*mean observed 13.9, peak 45.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 13.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 6.334 | 45.927 | 4.697 | 0.757 | 92.453 |
| gnn_st | post_covid | 6.342 | 45.917 | 4.693 | 0.757 | 92.453 |
| lstm | post_covid | 7.276 | 58.251 | 5.679 | 0.661 | 90.566 |
| xgboost | post_covid | 7.372 | 44.094 | 5.133 | 0.687 | 94.340 |
| arima | post_covid | 7.749 | 58.900 | 5.705 | 0.605 | 86.792 |
| persistence | post_covid | 7.931 | 64.945 | 6.307 | 0.664 | 92.453 |
| gat | post_covid | 7.935 | 70.657 | 6.076 | 0.594 | 84.906 |
| dualtopo | post_covid | 9.785 | 75.519 | 6.922 | 0.566 | 71.698 |
| seasonal_naive | post_covid | 10.196 | 78.064 | 7.188 | 0.502 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 18.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 7.487 | 30.395 | 5.473 | 0.722 | 88.462 |
| gnn_st | post_covid | 7.498 | 30.309 | 5.468 | 0.721 | 88.462 |
| lstm | post_covid | 8.838 | 40.624 | 7.021 | 0.575 | 84.615 |
| persistence | post_covid | 9.184 | 44.711 | 7.475 | 0.639 | 88.462 |
| xgboost | post_covid | 9.256 | 33.642 | 6.571 | 0.574 | 92.308 |
| arima | post_covid | 9.646 | 37.607 | 7.230 | 0.502 | 76.923 |
| gat | post_covid | 9.755 | 42.684 | 7.405 | 0.431 | 76.923 |
| dualtopo | post_covid | 12.524 | 36.090 | 8.598 | 0.360 | 65.385 |
| seasonal_naive | post_covid | 13.045 | 58.895 | 9.688 | 0.335 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 4.916 | 53.772 | 3.748 | 0.531 | 96.296 |
| gnn_st_v2 | post_covid | 4.976 | 60.308 | 3.949 | 0.387 | 96.296 |
| gnn_st | post_covid | 4.980 | 60.369 | 3.948 | 0.385 | 96.296 |
| arima | post_covid | 5.318 | 78.615 | 4.237 | 0.311 | 96.296 |
| lstm | post_covid | 5.356 | 74.572 | 4.387 | 0.239 | 96.296 |
| gat | post_covid | 5.652 | 96.559 | 4.796 | 0.332 | 92.593 |
| dualtopo | post_covid | 6.076 | 112.027 | 5.309 | 0.398 | 77.778 |
| seasonal_naive | post_covid | 6.341 | 95.813 | 4.780 | 0.157 | 100.000 |
| persistence | post_covid | 6.501 | 83.680 | 5.183 | 0.236 | 96.296 |

## Bexley

*mean observed 12.4, peak 49.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 12.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.214 | 59.080 | 5.567 | 0.717 | 90.566 |
| gnn_st_v2 | post_covid | 7.226 | 59.227 | 5.575 | 0.715 | 90.566 |
| lstm | post_covid | 7.488 | 62.627 | 5.407 | 0.699 | 90.566 |
| xgboost | post_covid | 8.252 | 59.606 | 6.181 | 0.627 | 90.566 |
| gat | post_covid | 8.678 | 74.343 | 6.534 | 0.552 | 79.245 |
| arima | post_covid | 9.064 | 73.490 | 6.978 | 0.482 | 81.132 |
| persistence | post_covid | 9.602 | 72.811 | 7.499 | 0.562 | 81.132 |
| dualtopo | post_covid | 10.409 | 75.985 | 7.782 | 0.598 | 67.925 |
| seasonal_naive | post_covid | 12.792 | 84.257 | 8.561 | 0.297 | 90.566 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.274 | 66.202 | 6.910 | 0.664 | 92.308 |
| gnn_st_v2 | post_covid | 8.299 | 66.477 | 6.929 | 0.662 | 92.308 |
| lstm | post_covid | 8.890 | 67.898 | 6.642 | 0.595 | 88.462 |
| xgboost | post_covid | 9.853 | 72.982 | 7.842 | 0.479 | 88.462 |
| arima | post_covid | 10.714 | 69.322 | 8.458 | 0.401 | 80.769 |
| gat | post_covid | 10.831 | 77.739 | 8.195 | 0.285 | 73.077 |
| persistence | post_covid | 11.563 | 72.928 | 9.605 | 0.457 | 84.615 |
| dualtopo | post_covid | 12.890 | 62.071 | 9.436 | 0.416 | 61.538 |
| seasonal_naive | post_covid | 17.369 | 106.375 | 12.716 | -0.074 | 92.308 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 5.541 | 58.117 | 4.559 | 0.606 | 88.889 |
| lstm | post_covid | 5.828 | 56.397 | 4.218 | 0.461 | 92.593 |
| gat | post_covid | 5.905 | 70.330 | 4.934 | 0.561 | 85.185 |
| gnn_st_v2 | post_covid | 6.014 | 50.660 | 4.270 | 0.306 | 88.889 |
| gnn_st | post_covid | 6.018 | 50.662 | 4.274 | 0.304 | 88.889 |
| xgboost | post_covid | 6.339 | 43.798 | 4.582 | 0.287 | 92.593 |
| arima | post_covid | 7.123 | 78.416 | 5.553 | 0.179 | 81.481 |
| persistence | post_covid | 7.227 | 72.673 | 5.471 | 0.319 | 77.778 |
| dualtopo | post_covid | 7.257 | 92.428 | 6.189 | 0.314 | 74.074 |

## Worthington

*mean observed 11.8, peak 44.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 11.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.290 | 52.025 | 4.428 | 0.728 | 94.340 |
| gnn_st_v2 | post_covid | 6.297 | 52.118 | 4.434 | 0.728 | 94.340 |
| arima | post_covid | 6.824 | 64.400 | 4.763 | 0.648 | 94.340 |
| xgboost | post_covid | 7.197 | 51.812 | 4.810 | 0.672 | 94.340 |
| lstm | post_covid | 7.234 | 52.508 | 4.899 | 0.737 | 88.679 |
| persistence | post_covid | 7.285 | 76.285 | 5.529 | 0.648 | 96.226 |
| gat | post_covid | 7.326 | 58.913 | 4.982 | 0.692 | 86.792 |
| seasonal_naive | post_covid | 8.559 | 61.813 | 5.793 | 0.451 | 90.566 |
| dualtopo | post_covid | 9.841 | 70.612 | 6.718 | 0.667 | 69.811 |

### Flu season (Oct–Mar), 26 weeks scored, mean 16.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.795 | 34.707 | 5.358 | 0.664 | 92.308 |
| gnn_st_v2 | post_covid | 7.800 | 34.710 | 5.361 | 0.664 | 92.308 |
| arima | post_covid | 8.691 | 45.471 | 6.191 | 0.569 | 88.462 |
| persistence | post_covid | 9.078 | 59.133 | 7.226 | 0.569 | 92.308 |
| xgboost | post_covid | 9.109 | 39.392 | 6.134 | 0.563 | 88.462 |
| lstm | post_covid | 9.398 | 38.128 | 6.596 | 0.671 | 80.769 |
| gat | post_covid | 9.644 | 42.220 | 6.835 | 0.567 | 76.923 |
| seasonal_naive | post_covid | 10.943 | 42.107 | 7.442 | 0.291 | 92.308 |
| dualtopo | post_covid | 13.339 | 53.113 | 9.962 | 0.579 | 46.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 3.974 | 74.988 | 3.197 | 0.459 | 96.296 |
| lstm | post_covid | 4.205 | 66.355 | 3.265 | 0.367 | 96.296 |
| arima | post_covid | 4.320 | 82.627 | 3.388 | 0.300 | 100.000 |
| dualtopo | post_covid | 4.332 | 87.463 | 3.595 | 0.070 | 92.593 |
| gnn_st | post_covid | 4.375 | 68.702 | 3.531 | 0.325 | 96.296 |
| gnn_st_v2 | post_covid | 4.387 | 68.882 | 3.541 | 0.321 | 96.296 |
| xgboost | post_covid | 4.667 | 63.773 | 3.536 | 0.207 | 100.000 |
| persistence | post_covid | 4.983 | 92.802 | 3.895 | 0.300 | 100.000 |
| seasonal_naive | post_covid | 5.335 | 80.790 | 4.206 | 0.112 | 88.889 |

## Hilliard

*mean observed 10.3, peak 34.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 4.233 | 27248831.171 | 3.293 | 0.860 | 98.113 |
| gnn_st | post_covid | 4.234 | 27347741.568 | 3.291 | 0.859 | 98.113 |
| lstm | post_covid | 5.403 | 82.868 | 4.321 | 0.780 | 98.113 |
| xgboost | post_covid | 5.537 | 33038622.787 | 4.310 | 0.758 | 96.226 |
| persistence | post_covid | 6.158 | 74.408 | 4.612 | 0.718 | 92.453 |
| arima | post_covid | 6.271 | 85.836 | 4.715 | 0.656 | 84.906 |
| gat | post_covid | 6.466 | 108.105 | 5.384 | 0.643 | 86.792 |
| dualtopo | post_covid | 8.305 | 115.727 | 6.742 | 0.632 | 62.264 |
| seasonal_naive | post_covid | 9.588 | 126.365 | 7.238 | 0.508 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.889 | 34095595.016 | 4.010 | 0.835 | 100.000 |
| gnn_st_v2 | post_covid | 4.891 | 34029925.774 | 4.014 | 0.835 | 100.000 |
| lstm | post_covid | 6.123 | 59.851 | 5.192 | 0.753 | 100.000 |
| xgboost | post_covid | 6.412 | 52793820.825 | 5.305 | 0.708 | 100.000 |
| persistence | post_covid | 7.121 | 53.820 | 5.771 | 0.665 | 96.154 |
| arima | post_covid | 7.503 | 51.396 | 5.810 | 0.605 | 80.769 |
| gat | post_covid | 7.730 | 67.968 | 6.417 | 0.482 | 84.615 |
| dualtopo | post_covid | 10.475 | 67.171 | 8.633 | 0.628 | 50.000 |
| seasonal_naive | post_covid | 12.263 | 89.764 | 9.758 | 0.346 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 3.485 | 20718888.220 | 2.600 | 0.691 | 96.296 |
| gnn_st | post_covid | 3.488 | 20849808.617 | 2.599 | 0.688 | 96.296 |
| xgboost | post_covid | 4.537 | 14015098.751 | 3.353 | 0.472 | 92.593 |
| lstm | post_covid | 4.604 | 105.000 | 3.482 | 0.414 | 96.296 |
| arima | post_covid | 4.795 | 118.951 | 3.660 | 0.354 | 88.889 |
| gat | post_covid | 4.953 | 146.699 | 4.389 | 0.356 | 88.889 |
| persistence | post_covid | 5.061 | 94.203 | 3.495 | 0.421 | 88.889 |
| dualtopo | post_covid | 5.452 | 162.416 | 4.920 | -0.027 | 74.074 |
| seasonal_naive | post_covid | 5.969 | 161.559 | 4.813 | 0.067 | 100.000 |

## Clintonville/Near North

*mean observed 10.2, peak 27.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.247 | 34.913 | 2.474 | 0.894 | 100.000 |
| gnn_st_v2 | post_covid | 3.252 | 34.855 | 2.477 | 0.894 | 100.000 |
| arima | post_covid | 3.725 | 42.684 | 2.952 | 0.831 | 100.000 |
| lstm | post_covid | 3.808 | 48.356 | 3.014 | 0.837 | 100.000 |
| persistence | post_covid | 3.958 | 43.000 | 3.198 | 0.825 | 98.113 |
| seasonal_naive | post_covid | 4.314 | 41.975 | 3.353 | 0.789 | 100.000 |
| gat | post_covid | 4.605 | 59.973 | 3.384 | 0.789 | 94.340 |
| dualtopo | post_covid | 7.155 | 76.306 | 5.129 | 0.834 | 69.811 |
| xgboost | post_covid | 7.252 | 49.282 | 4.367 | 0.744 | 96.226 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.881 | 23.003 | 3.047 | 0.852 | 100.000 |
| gnn_st_v2 | post_covid | 3.888 | 22.969 | 3.050 | 0.852 | 100.000 |
| persistence | post_covid | 4.464 | 30.147 | 3.753 | 0.781 | 100.000 |
| arima | post_covid | 4.541 | 29.504 | 3.726 | 0.755 | 100.000 |
| lstm | post_covid | 4.690 | 29.240 | 3.748 | 0.755 | 100.000 |
| seasonal_naive | post_covid | 4.810 | 30.657 | 3.714 | 0.704 | 100.000 |
| gat | post_covid | 5.770 | 30.688 | 4.351 | 0.680 | 88.462 |
| dualtopo | post_covid | 9.511 | 42.669 | 7.315 | 0.767 | 50.000 |
| xgboost | post_covid | 9.802 | 43.037 | 6.306 | 0.647 | 92.308 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.489 | 46.382 | 1.922 | 0.727 | 100.000 |
| gnn_st_v2 | post_covid | 2.491 | 46.301 | 1.925 | 0.727 | 100.000 |
| lstm | post_covid | 2.698 | 66.764 | 2.307 | 0.614 | 100.000 |
| arima | post_covid | 2.717 | 55.376 | 2.206 | 0.634 | 100.000 |
| gat | post_covid | 3.094 | 88.174 | 2.453 | 0.514 | 100.000 |
| xgboost | post_covid | 3.273 | 55.295 | 2.500 | 0.583 | 100.000 |
| persistence | post_covid | 3.401 | 55.377 | 2.663 | 0.543 | 96.296 |
| dualtopo | post_covid | 3.659 | 108.698 | 3.025 | 0.583 | 88.889 |
| seasonal_naive | post_covid | 3.777 | 52.874 | 3.006 | 0.373 | 100.000 |

## Far Southeast

*mean observed 5.6, peak 14.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 2.655 | 61.457 | 2.174 | 0.658 | 100.000 |
| gnn_st | post_covid | 2.656 | 61.552 | 2.177 | 0.658 | 100.000 |
| xgboost | post_covid | 2.890 | 67.716 | 2.263 | 0.558 | 100.000 |
| lstm | post_covid | 2.893 | 72.395 | 2.303 | 0.583 | 100.000 |
| arima | post_covid | 2.997 | 73.257 | 2.443 | 0.513 | 100.000 |
| gat | post_covid | 3.192 | 80.207 | 2.414 | 0.460 | 96.226 |
| persistence | post_covid | 3.246 | 68.824 | 2.622 | 0.567 | 92.453 |
| dualtopo | post_covid | 3.480 | 76.711 | 2.735 | 0.315 | 90.566 |
| seasonal_naive | post_covid | 6.079 | 118.809 | 4.209 | 0.365 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.082 | 56.896 | 2.492 | 0.597 | 100.000 |
| gnn_st_v2 | post_covid | 3.083 | 56.936 | 2.492 | 0.597 | 100.000 |
| lstm | post_covid | 3.439 | 68.304 | 2.764 | 0.473 | 100.000 |
| xgboost | post_covid | 3.524 | 63.623 | 2.759 | 0.405 | 100.000 |
| arima | post_covid | 3.564 | 57.627 | 2.997 | 0.435 | 100.000 |
| persistence | post_covid | 3.794 | 56.625 | 3.163 | 0.518 | 92.308 |
| gat | post_covid | 4.145 | 85.795 | 3.315 | 0.127 | 92.308 |
| dualtopo | post_covid | 4.335 | 55.986 | 3.468 | 0.179 | 80.769 |
| seasonal_naive | post_covid | 8.088 | 148.154 | 6.035 | 0.164 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 4.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 1.858 | 74.825 | 1.547 | 0.582 | 100.000 |
| xgboost | post_covid | 2.105 | 71.658 | 1.786 | 0.118 | 100.000 |
| gnn_st_v2 | post_covid | 2.163 | 65.811 | 1.868 | 0.237 | 100.000 |
| gnn_st | post_covid | 2.166 | 66.035 | 1.873 | 0.235 | 100.000 |
| lstm | post_covid | 2.246 | 76.334 | 1.858 | 0.161 | 100.000 |
| arima | post_covid | 2.323 | 88.307 | 1.910 | 0.211 | 100.000 |
| dualtopo | post_covid | 2.383 | 96.669 | 2.030 | -0.020 | 100.000 |
| persistence | post_covid | 2.611 | 80.572 | 2.100 | 0.336 | 92.593 |
| seasonal_naive | post_covid | 3.087 | 90.550 | 2.450 | 0.185 | 96.296 |

## Dublin

*mean observed 5.4, peak 16.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 2.469 | 17041012.187 | 1.922 | 0.773 | 100.000 |
| gnn_st | post_covid | 2.472 | 17117099.281 | 1.926 | 0.772 | 100.000 |
| arima | post_covid | 2.509 | 49.208 | 1.931 | 0.725 | 100.000 |
| xgboost | post_covid | 2.638 | 24360478.456 | 2.104 | 0.689 | 100.000 |
| persistence | post_covid | 2.640 | 49.984 | 1.984 | 0.725 | 98.113 |
| lstm | post_covid | 2.692 | 50.184 | 2.081 | 0.712 | 100.000 |
| gat | post_covid | 2.742 | 58.062 | 2.006 | 0.661 | 94.340 |
| seasonal_naive | post_covid | 3.619 | 54.484 | 2.775 | 0.632 | 96.226 |
| dualtopo | post_covid | 4.027 | 74.411 | 3.043 | 0.628 | 83.019 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 2.695 | 34.077 | 2.228 | 0.698 | 100.000 |
| gnn_st | post_covid | 2.698 | 34.169 | 2.231 | 0.696 | 100.000 |
| arima | post_covid | 2.912 | 30.504 | 2.138 | 0.634 | 100.000 |
| persistence | post_covid | 2.955 | 33.802 | 2.140 | 0.634 | 100.000 |
| xgboost | post_covid | 3.051 | 34.856 | 2.441 | 0.566 | 100.000 |
| lstm | post_covid | 3.223 | 39.148 | 2.529 | 0.551 | 100.000 |
| gat | post_covid | 3.300 | 35.423 | 2.445 | 0.476 | 92.308 |
| seasonal_naive | post_covid | 4.582 | 57.247 | 3.752 | 0.479 | 100.000 |
| dualtopo | post_covid | 5.249 | 50.690 | 4.161 | 0.479 | 69.231 |

### Off-season (Apr–Sep), 27 weeks scored, mean 3.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2.047 | 67.912 | 1.732 | 0.502 | 100.000 |
| lstm | post_covid | 2.054 | 61.221 | 1.649 | 0.547 | 100.000 |
| gat | post_covid | 2.069 | 80.701 | 1.583 | 0.492 | 96.296 |
| xgboost | post_covid | 2.167 | 47818683.405 | 1.779 | 0.370 | 100.000 |
| gnn_st_v2 | post_covid | 2.231 | 33450842.960 | 1.626 | 0.513 | 100.000 |
| gnn_st | post_covid | 2.232 | 33600199.018 | 1.631 | 0.508 | 100.000 |
| persistence | post_covid | 2.296 | 66.166 | 1.835 | 0.502 | 96.296 |
| dualtopo | post_covid | 2.304 | 98.132 | 1.965 | 0.096 | 96.296 |
| seasonal_naive | post_covid | 2.342 | 51.722 | 1.835 | 0.494 | 92.593 |

## UA/Grandview

*mean observed 4.4, peak 15.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 4.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.333 | 39.214 | 1.555 | 0.755 | 98.113 |
| gnn_st_v2 | post_covid | 2.344 | 39.271 | 1.559 | 0.752 | 98.113 |
| lstm | post_covid | 2.542 | 45.388 | 1.647 | 0.698 | 98.113 |
| xgboost | post_covid | 2.786 | 56.525 | 1.964 | 0.625 | 98.113 |
| arima | post_covid | 2.961 | 53.838 | 1.887 | 0.553 | 96.226 |
| gat | post_covid | 2.999 | 62.768 | 2.201 | 0.585 | 96.226 |
| persistence | post_covid | 3.139 | 57.877 | 2.169 | 0.602 | 94.340 |
| dualtopo | post_covid | 3.583 | 67.092 | 2.430 | 0.529 | 90.566 |
| seasonal_naive | post_covid | 5.480 | 87.113 | 3.608 | 0.364 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 6.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.960 | 29.037 | 1.895 | 0.664 | 96.154 |
| gnn_st_v2 | post_covid | 2.976 | 29.132 | 1.900 | 0.660 | 96.154 |
| lstm | post_covid | 3.281 | 36.195 | 2.241 | 0.551 | 96.154 |
| xgboost | post_covid | 3.639 | 47.889 | 2.671 | 0.405 | 96.154 |
| gat | post_covid | 3.812 | 46.460 | 2.806 | 0.370 | 92.308 |
| arima | post_covid | 3.826 | 32.210 | 2.353 | 0.449 | 92.308 |
| persistence | post_covid | 4.031 | 40.900 | 2.715 | 0.483 | 96.154 |
| dualtopo | post_covid | 4.700 | 42.595 | 3.206 | 0.348 | 80.769 |
| seasonal_naive | post_covid | 7.535 | 96.068 | 5.736 | 0.113 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 2.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 1.499 | 49.799 | 1.228 | 0.282 | 100.000 |
| gnn_st_v2 | post_covid | 1.501 | 49.816 | 1.231 | 0.282 | 100.000 |
| lstm | post_covid | 1.523 | 54.948 | 1.075 | 0.393 | 100.000 |
| xgboost | post_covid | 1.576 | 65.507 | 1.284 | 0.199 | 100.000 |
| arima | post_covid | 1.764 | 76.331 | 1.439 | 0.299 | 100.000 |
| gat | post_covid | 1.912 | 79.728 | 1.618 | 0.143 | 100.000 |
| persistence | post_covid | 1.922 | 75.533 | 1.644 | 0.184 | 92.593 |
| dualtopo | post_covid | 1.982 | 92.568 | 1.683 | 0.049 | 100.000 |
| seasonal_naive | post_covid | 2.067 | 77.800 | 1.560 | 0.161 | 96.296 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st, gnn_st_v2; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, gnn_st_v2, lstm). Differences here are not purely model quality.
