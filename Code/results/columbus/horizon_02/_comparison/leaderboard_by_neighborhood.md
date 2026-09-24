# Per-neighborhood leaderboard — horizon 2

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks, in every neighborhood (53 weeks each), so the tables are directly comparable. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

> **MAPE is not usable in this table** (it reaches 35,573,258%). It divides by the observed rate, and this city reports observed zeros and near-zeros rather than suppressing small counts, so the denominator goes to zero. Rank on RMSE or MAE. The column is kept so the two cities' tables have the same shape.

## Summary — neighborhoods won, out of 17

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| gnn_st | 13 | 13 | 2 |
| gat | 2 | 1 | 9 |
| gnn_st_v2 | 1 | 1 | 2 |
| xgboost | 1 | 1 | 1 |
| arima | 0 | 0 | 1 |
| lstm | 0 | 1 | 1 |
| seasonal_naive | 0 | 0 | 1 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `gat (post_covid)`: Dublin, Worthing.; `gnn_st (post_covid)`: Agler, Clinton+, Eastside, FarEast, FarSE, FarSW, FarSouth, Hilliard, Linden, NESub, Northland, UA/Grand, West; `gnn_st_v2 (post_covid)`: Bexley; `xgboost (post_covid)`: Wville
- **Flu season (Oct–Mar)** — `gat (post_covid)`: Dublin; `gnn_st (post_covid)`: Agler, Clinton+, Eastside, FarEast, FarSW, FarSouth, Hilliard, Linden, NESub, Northland, UA/Grand, West, Worthing.; `gnn_st_v2 (post_covid)`: Bexley; `lstm (post_covid)`: FarSE; `xgboost (post_covid)`: Wville
- **Off-season (Apr–Sep)** — `arima (post_covid)`: Dublin; `gat (post_covid)`: Agler, Bexley, FarEast, FarSE, Linden, NESub, Northland, West, Wville; `gnn_st (post_covid)`: FarSW, Hilliard; `gnn_st_v2 (post_covid)`: Clinton+, FarSouth; `lstm (post_covid)`: Worthing.; `seasonal_naive (post_covid)`: Eastside; `xgboost (post_covid)`: UA/Grand

`gnn_st (post_covid)` wins 13 of 17 neighborhoods. `gnn_st (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Far East

*mean observed 46.6, peak 123.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.851 | 22.089 | 10.035 | 0.835 | 90.566 |
| gnn_st_v2 | post_covid | 13.987 | 22.114 | 10.106 | 0.833 | 90.566 |
| gat | post_covid | 16.167 | 26.824 | 11.209 | 0.771 | 88.679 |
| xgboost | post_covid | 16.437 | 23.912 | 11.624 | 0.787 | 90.566 |
| lstm | post_covid | 17.851 | 34.052 | 13.521 | 0.689 | 92.453 |
| persistence | post_covid | 18.947 | 29.894 | 13.567 | 0.702 | 94.340 |
| arima | post_covid | 20.207 | 36.949 | 14.438 | 0.588 | 86.792 |
| dualtopo | post_covid | 24.777 | 47.369 | 17.830 | 0.730 | 60.377 |
| seasonal_naive | post_covid | 25.434 | 31.470 | 14.807 | 0.648 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 62.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.591 | 21.475 | 13.574 | 0.718 | 88.462 |
| gnn_st_v2 | post_covid | 17.823 | 21.607 | 13.749 | 0.713 | 88.462 |
| xgboost | post_covid | 20.518 | 22.494 | 14.494 | 0.589 | 92.308 |
| gat | post_covid | 21.362 | 26.690 | 15.455 | 0.568 | 80.769 |
| lstm | post_covid | 21.919 | 26.211 | 16.185 | 0.513 | 92.308 |
| persistence | post_covid | 24.791 | 28.407 | 18.606 | 0.506 | 88.462 |
| arima | post_covid | 25.550 | 25.279 | 17.655 | 0.460 | 80.769 |
| dualtopo | post_covid | 31.176 | 29.715 | 22.187 | 0.570 | 53.846 |
| seasonal_naive | post_covid | 35.221 | 39.470 | 22.764 | 0.352 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 31.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 8.582 | 26.954 | 7.120 | 0.699 | 96.296 |
| seasonal_naive | post_covid | 8.677 | 23.766 | 7.145 | 0.697 | 100.000 |
| gnn_st_v2 | post_covid | 8.839 | 22.602 | 6.598 | 0.689 | 92.593 |
| gnn_st | post_covid | 8.868 | 22.680 | 6.627 | 0.687 | 92.593 |
| persistence | post_covid | 10.620 | 31.325 | 8.715 | 0.583 | 100.000 |
| xgboost | post_covid | 11.178 | 25.278 | 8.861 | 0.794 | 88.889 |
| lstm | post_covid | 12.761 | 41.601 | 10.956 | 0.381 | 92.593 |
| arima | post_covid | 13.148 | 48.187 | 11.341 | 0.352 | 92.593 |
| dualtopo | post_covid | 16.405 | 64.370 | 13.635 | 0.335 | 66.667 |

## Far South

*mean observed 41.1, peak 100.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 41.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.821 | 26.276 | 10.102 | 0.803 | 84.906 |
| gnn_st_v2 | post_covid | 13.945 | 26.293 | 10.181 | 0.801 | 84.906 |
| lstm | post_covid | 14.839 | 31.680 | 11.174 | 0.751 | 88.679 |
| gat | post_covid | 15.086 | 30.012 | 11.117 | 0.794 | 79.245 |
| arima | post_covid | 16.962 | 37.362 | 13.069 | 0.643 | 84.906 |
| xgboost | post_covid | 17.169 | 30.670 | 13.383 | 0.787 | 83.019 |
| persistence | post_covid | 18.431 | 38.257 | 13.906 | 0.643 | 84.906 |
| dualtopo | post_covid | 22.467 | 50.895 | 16.938 | 0.748 | 60.377 |
| seasonal_naive | post_covid | 30.505 | 49.524 | 18.179 | 0.608 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 57.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 16.846 | 19.578 | 12.309 | 0.563 | 84.615 |
| gnn_st_v2 | post_covid | 17.056 | 19.756 | 12.494 | 0.560 | 84.615 |
| lstm | post_covid | 17.475 | 23.450 | 13.426 | 0.558 | 88.462 |
| gat | post_covid | 18.526 | 28.517 | 14.510 | 0.548 | 76.923 |
| arima | post_covid | 20.958 | 27.926 | 16.145 | 0.243 | 80.769 |
| xgboost | post_covid | 21.171 | 26.351 | 16.723 | 0.466 | 76.923 |
| persistence | post_covid | 22.806 | 32.028 | 17.337 | 0.243 | 84.615 |
| dualtopo | post_covid | 27.977 | 31.245 | 21.452 | 0.553 | 46.154 |
| seasonal_naive | post_covid | 41.762 | 48.281 | 26.293 | 0.316 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 10.079 | 32.830 | 7.953 | 0.552 | 85.185 |
| gnn_st | post_covid | 10.085 | 32.975 | 7.977 | 0.554 | 85.185 |
| gat | post_covid | 10.783 | 31.506 | 7.850 | 0.405 | 81.481 |
| lstm | post_covid | 11.755 | 39.910 | 9.006 | 0.400 | 88.889 |
| arima | post_covid | 11.907 | 46.799 | 10.107 | 0.361 | 88.889 |
| xgboost | post_covid | 12.125 | 34.989 | 10.167 | 0.740 | 88.889 |
| seasonal_naive | post_covid | 12.134 | 50.768 | 10.365 | 0.328 | 100.000 |
| persistence | post_covid | 12.884 | 44.486 | 10.602 | 0.361 | 85.185 |
| dualtopo | post_covid | 15.398 | 70.545 | 12.592 | 0.230 | 74.074 |

## West

*mean observed 38.3, peak 84.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.280 | 17.729 | 5.997 | 0.926 | 100.000 |
| gnn_st_v2 | post_covid | 7.420 | 17.780 | 6.048 | 0.924 | 100.000 |
| persistence | post_covid | 10.181 | 23.136 | 7.764 | 0.857 | 98.113 |
| xgboost | post_covid | 10.949 | 24.182 | 9.065 | 0.846 | 98.113 |
| gat | post_covid | 13.017 | 31.112 | 10.082 | 0.881 | 94.340 |
| lstm | post_covid | 13.439 | 38.656 | 11.351 | 0.812 | 98.113 |
| arima | post_covid | 13.774 | 37.193 | 11.062 | 0.779 | 94.340 |
| dualtopo | post_covid | 19.091 | 56.404 | 16.295 | 0.833 | 56.604 |
| seasonal_naive | post_covid | 25.121 | 34.662 | 13.749 | 0.725 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 51.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.818 | 13.809 | 6.552 | 0.898 | 100.000 |
| gnn_st_v2 | post_covid | 8.079 | 13.869 | 6.657 | 0.894 | 100.000 |
| persistence | post_covid | 11.753 | 18.848 | 9.036 | 0.786 | 96.154 |
| xgboost | post_covid | 12.970 | 24.793 | 11.686 | 0.683 | 100.000 |
| lstm | post_covid | 14.018 | 25.130 | 11.178 | 0.732 | 96.154 |
| arima | post_covid | 16.039 | 22.482 | 12.493 | 0.698 | 88.462 |
| gat | post_covid | 17.347 | 34.819 | 14.907 | 0.780 | 88.462 |
| dualtopo | post_covid | 21.522 | 33.068 | 18.202 | 0.786 | 53.846 |
| seasonal_naive | post_covid | 35.169 | 43.590 | 22.071 | 0.490 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 6.546 | 27.542 | 5.434 | 0.674 | 100.000 |
| gnn_st | post_covid | 6.721 | 21.504 | 5.462 | 0.651 | 100.000 |
| gnn_st_v2 | post_covid | 6.724 | 21.546 | 5.462 | 0.649 | 100.000 |
| seasonal_naive | post_covid | 6.907 | 26.064 | 5.736 | 0.656 | 100.000 |
| persistence | post_covid | 8.393 | 27.266 | 6.540 | 0.545 | 100.000 |
| xgboost | post_covid | 8.563 | 23.594 | 6.542 | 0.681 | 96.296 |
| arima | post_covid | 11.169 | 51.358 | 9.685 | 0.453 | 100.000 |
| lstm | post_covid | 12.857 | 51.680 | 11.517 | 0.363 | 100.000 |
| dualtopo | post_covid | 16.414 | 78.876 | 14.458 | 0.305 | 59.259 |

## Northland

*mean observed 33.4, peak 87.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 33.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.438 | 25.432 | 8.158 | 0.777 | 100.000 |
| gnn_st_v2 | post_covid | 10.498 | 25.497 | 8.226 | 0.775 | 100.000 |
| lstm | post_covid | 12.319 | 33.834 | 9.773 | 0.678 | 94.340 |
| arima | post_covid | 12.382 | 30.699 | 9.338 | 0.653 | 94.340 |
| gat | post_covid | 13.182 | 31.387 | 9.818 | 0.692 | 84.906 |
| persistence | post_covid | 13.592 | 32.039 | 10.174 | 0.653 | 96.226 |
| xgboost | post_covid | 13.769 | 30.596 | 10.630 | 0.613 | 94.340 |
| dualtopo | post_covid | 16.350 | 42.280 | 11.904 | 0.669 | 73.585 |
| seasonal_naive | post_covid | 21.192 | 41.586 | 14.073 | 0.549 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.743 | 24.307 | 10.261 | 0.702 | 100.000 |
| gnn_st_v2 | post_covid | 12.856 | 24.480 | 10.423 | 0.698 | 100.000 |
| lstm | post_covid | 14.683 | 29.168 | 12.010 | 0.581 | 92.308 |
| arima | post_covid | 15.507 | 25.374 | 11.707 | 0.562 | 88.462 |
| persistence | post_covid | 17.083 | 30.465 | 13.094 | 0.562 | 92.308 |
| xgboost | post_covid | 17.527 | 34.363 | 14.355 | 0.326 | 88.462 |
| gat | post_covid | 17.781 | 40.112 | 15.080 | 0.499 | 69.231 |
| dualtopo | post_covid | 20.358 | 29.865 | 14.352 | 0.526 | 69.231 |
| seasonal_naive | post_covid | 28.830 | 54.815 | 21.340 | 0.284 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 25.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 6.053 | 22.986 | 4.750 | 0.745 | 100.000 |
| gnn_st_v2 | post_covid | 7.562 | 26.477 | 6.110 | 0.536 | 100.000 |
| gnn_st | post_covid | 7.583 | 26.515 | 6.132 | 0.534 | 100.000 |
| arima | post_covid | 8.328 | 35.828 | 7.056 | 0.468 | 100.000 |
| xgboost | post_covid | 8.735 | 26.968 | 7.043 | 0.591 | 100.000 |
| seasonal_naive | post_covid | 9.013 | 28.847 | 7.074 | 0.552 | 100.000 |
| persistence | post_covid | 9.034 | 33.554 | 7.363 | 0.468 | 100.000 |
| lstm | post_covid | 9.502 | 38.326 | 7.620 | 0.306 | 96.296 |
| dualtopo | post_covid | 11.208 | 54.236 | 9.547 | 0.395 | 77.778 |

## Linden

*mean observed 31.0, peak 76.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 31.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.763 | 28.461 | 7.002 | 0.848 | 98.113 |
| gnn_st_v2 | post_covid | 8.832 | 28.466 | 7.045 | 0.847 | 98.113 |
| gat | post_covid | 10.598 | 34.526 | 8.220 | 0.789 | 96.226 |
| arima | post_covid | 10.972 | 36.300 | 8.598 | 0.736 | 92.453 |
| persistence | post_covid | 11.681 | 37.559 | 9.336 | 0.736 | 98.113 |
| lstm | post_covid | 12.012 | 43.455 | 9.960 | 0.661 | 94.340 |
| xgboost | post_covid | 12.376 | 33.846 | 9.719 | 0.702 | 94.340 |
| dualtopo | post_covid | 16.032 | 56.682 | 12.281 | 0.731 | 64.151 |
| seasonal_naive | post_covid | 17.087 | 39.050 | 10.714 | 0.640 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.126 | 19.513 | 7.965 | 0.749 | 100.000 |
| gnn_st_v2 | post_covid | 10.263 | 19.579 | 8.065 | 0.746 | 100.000 |
| lstm | post_covid | 13.279 | 26.511 | 10.836 | 0.505 | 92.308 |
| arima | post_covid | 13.499 | 27.351 | 11.473 | 0.562 | 84.615 |
| gat | post_covid | 13.569 | 30.555 | 10.867 | 0.570 | 92.308 |
| persistence | post_covid | 14.292 | 31.891 | 12.324 | 0.562 | 100.000 |
| xgboost | post_covid | 15.164 | 28.741 | 12.134 | 0.384 | 92.308 |
| dualtopo | post_covid | 19.425 | 30.197 | 14.723 | 0.589 | 57.692 |
| seasonal_naive | post_covid | 22.995 | 39.434 | 15.133 | 0.376 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 20.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 6.573 | 38.349 | 5.670 | 0.610 | 100.000 |
| gnn_st_v2 | post_covid | 7.189 | 37.024 | 6.063 | 0.561 | 96.296 |
| gnn_st | post_covid | 7.210 | 37.078 | 6.074 | 0.560 | 96.296 |
| arima | post_covid | 7.800 | 44.918 | 5.829 | 0.487 | 100.000 |
| seasonal_naive | post_covid | 7.995 | 38.679 | 6.458 | 0.461 | 100.000 |
| persistence | post_covid | 8.435 | 43.018 | 6.458 | 0.487 | 96.296 |
| xgboost | post_covid | 8.901 | 38.762 | 7.394 | 0.373 | 96.296 |
| lstm | post_covid | 10.650 | 59.771 | 9.117 | 0.119 | 96.296 |
| dualtopo | post_covid | 11.883 | 82.187 | 9.930 | 0.163 | 70.370 |

## Eastside

*mean observed 30.9, peak 91.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 11.507 | 30.920 | 8.568 | 0.813 | 90.566 |
| gnn_st_v2 | post_covid | 11.564 | 30.885 | 8.566 | 0.812 | 90.566 |
| gat | post_covid | 13.074 | 41.249 | 10.110 | 0.747 | 86.792 |
| xgboost | post_covid | 14.449 | 35.108 | 10.488 | 0.722 | 84.906 |
| lstm | post_covid | 14.519 | 53.335 | 11.238 | 0.673 | 88.679 |
| persistence | post_covid | 16.168 | 39.530 | 11.272 | 0.638 | 90.566 |
| arima | post_covid | 17.144 | 52.049 | 11.680 | 0.460 | 86.792 |
| dualtopo | post_covid | 19.273 | 70.404 | 13.844 | 0.670 | 66.038 |
| seasonal_naive | post_covid | 20.062 | 45.181 | 12.400 | 0.628 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.551 | 21.555 | 9.994 | 0.704 | 96.154 |
| gnn_st_v2 | post_covid | 13.657 | 21.397 | 10.000 | 0.702 | 96.154 |
| gat | post_covid | 15.732 | 30.261 | 12.297 | 0.588 | 84.615 |
| lstm | post_covid | 16.425 | 29.724 | 12.357 | 0.531 | 96.154 |
| xgboost | post_covid | 17.107 | 25.024 | 12.362 | 0.552 | 88.462 |
| persistence | post_covid | 20.309 | 30.434 | 14.406 | 0.415 | 88.462 |
| arima | post_covid | 21.838 | 25.216 | 13.850 | 0.282 | 76.923 |
| dualtopo | post_covid | 24.082 | 30.797 | 16.588 | 0.573 | 65.385 |
| seasonal_naive | post_covid | 27.211 | 42.027 | 17.853 | 0.426 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 19.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 8.778 | 48.219 | 7.149 | 0.625 | 100.000 |
| gnn_st_v2 | post_covid | 9.105 | 40.022 | 7.186 | 0.639 | 85.185 |
| gnn_st | post_covid | 9.116 | 39.938 | 7.196 | 0.638 | 85.185 |
| gat | post_covid | 9.859 | 51.831 | 8.003 | 0.462 | 88.889 |
| persistence | post_covid | 10.769 | 48.290 | 8.255 | 0.511 | 92.593 |
| arima | post_covid | 10.851 | 77.888 | 9.591 | 0.424 | 96.296 |
| xgboost | post_covid | 11.314 | 44.817 | 8.684 | 0.530 | 81.481 |
| lstm | post_covid | 12.410 | 76.072 | 10.160 | 0.189 | 81.481 |
| dualtopo | post_covid | 13.064 | 108.544 | 11.202 | 0.055 | 66.667 |

## Agler/Cassidy

*mean observed 30.4, peak 86.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 30.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.385 | 48.183 | 9.453 | 0.782 | 88.679 |
| gnn_st_v2 | post_covid | 12.430 | 48.328 | 9.519 | 0.782 | 90.566 |
| gat | post_covid | 13.603 | 54.807 | 10.014 | 0.732 | 86.792 |
| xgboost | post_covid | 14.732 | 45.733 | 10.485 | 0.685 | 90.566 |
| lstm | post_covid | 14.754 | 68.188 | 10.669 | 0.653 | 88.679 |
| persistence | post_covid | 17.355 | 59.551 | 12.062 | 0.597 | 90.566 |
| arima | post_covid | 17.924 | 79.206 | 13.325 | 0.437 | 71.698 |
| dualtopo | post_covid | 19.551 | 100.684 | 15.091 | 0.671 | 50.943 |
| seasonal_naive | post_covid | 20.038 | 58.165 | 13.627 | 0.579 | 96.226 |

### Flu season (Oct–Mar), 26 weeks scored, mean 42.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.648 | 26.826 | 11.010 | 0.650 | 88.462 |
| gnn_st_v2 | post_covid | 14.708 | 26.873 | 11.109 | 0.653 | 88.462 |
| gat | post_covid | 17.289 | 32.048 | 12.448 | 0.442 | 84.615 |
| lstm | post_covid | 17.633 | 29.482 | 11.708 | 0.392 | 88.462 |
| xgboost | post_covid | 18.444 | 30.104 | 13.124 | 0.387 | 92.308 |
| persistence | post_covid | 21.053 | 31.312 | 14.421 | 0.381 | 92.308 |
| arima | post_covid | 21.566 | 31.025 | 14.901 | 0.294 | 69.231 |
| dualtopo | post_covid | 23.461 | 35.870 | 17.106 | 0.447 | 50.000 |
| seasonal_naive | post_covid | 27.003 | 54.578 | 20.687 | 0.236 | 96.154 |

### Off-season (Apr–Sep), 27 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 8.684 | 76.723 | 7.670 | 0.712 | 88.889 |
| seasonal_naive | post_covid | 9.277 | 61.618 | 6.830 | 0.620 | 96.296 |
| gnn_st | post_covid | 9.721 | 68.750 | 7.954 | 0.511 | 88.889 |
| gnn_st_v2 | post_covid | 9.745 | 68.989 | 7.988 | 0.508 | 92.593 |
| xgboost | post_covid | 9.922 | 60.784 | 7.945 | 0.540 | 88.889 |
| lstm | post_covid | 11.311 | 105.460 | 9.669 | 0.395 | 88.889 |
| persistence | post_covid | 12.823 | 86.744 | 9.789 | 0.397 | 88.889 |
| arima | post_covid | 13.520 | 125.603 | 11.806 | 0.199 | 74.074 |
| dualtopo | post_covid | 14.843 | 163.097 | 13.151 | 0.324 | 51.852 |

## Far Southwest

*mean observed 18.0, peak 47.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 18.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.330 | 29.506 | 4.799 | 0.806 | 98.113 |
| gnn_st_v2 | post_covid | 6.390 | 29.501 | 4.851 | 0.802 | 98.113 |
| xgboost | post_covid | 6.666 | 27.733 | 4.798 | 0.787 | 100.000 |
| arima | post_covid | 7.695 | 35.441 | 5.531 | 0.691 | 94.340 |
| persistence | post_covid | 8.349 | 37.695 | 6.264 | 0.691 | 98.113 |
| lstm | post_covid | 8.591 | 44.482 | 6.631 | 0.660 | 98.113 |
| gat | post_covid | 8.786 | 39.766 | 5.903 | 0.674 | 86.792 |
| dualtopo | post_covid | 10.604 | 58.969 | 8.566 | 0.658 | 83.019 |
| seasonal_naive | post_covid | 13.223 | 46.109 | 8.174 | 0.603 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.053 | 34.843 | 6.648 | 0.709 | 100.000 |
| gnn_st_v2 | post_covid | 8.141 | 34.809 | 6.750 | 0.704 | 100.000 |
| xgboost | post_covid | 8.578 | 36.862 | 7.003 | 0.678 | 100.000 |
| arima | post_covid | 9.841 | 36.871 | 7.512 | 0.552 | 92.308 |
| persistence | post_covid | 10.789 | 45.473 | 9.034 | 0.552 | 100.000 |
| lstm | post_covid | 10.976 | 44.743 | 8.515 | 0.438 | 96.154 |
| gat | post_covid | 11.659 | 54.682 | 9.117 | 0.438 | 76.923 |
| dualtopo | post_covid | 12.880 | 42.060 | 10.109 | 0.491 | 73.077 |
| seasonal_naive | post_covid | 18.209 | 64.254 | 12.929 | 0.352 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.025 | 24.367 | 3.019 | 0.559 | 96.296 |
| gnn_st_v2 | post_covid | 4.042 | 24.390 | 3.021 | 0.553 | 96.296 |
| xgboost | post_covid | 4.046 | 18.943 | 2.675 | 0.720 | 100.000 |
| gat | post_covid | 4.544 | 25.402 | 2.808 | 0.361 | 96.296 |
| arima | post_covid | 4.793 | 34.063 | 3.624 | 0.301 | 96.296 |
| seasonal_naive | post_covid | 4.892 | 28.637 | 3.596 | 0.368 | 100.000 |
| persistence | post_covid | 4.974 | 30.204 | 3.596 | 0.301 | 96.296 |
| lstm | post_covid | 5.372 | 44.230 | 4.818 | 0.495 | 100.000 |
| dualtopo | post_covid | 7.808 | 75.252 | 7.079 | 0.284 | 92.593 |

## NE Suburban

*mean observed 14.8, peak 50.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 14.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.480 | 34.205 | 4.560 | 0.730 | 96.226 |
| gnn_st_v2 | post_covid | 6.568 | 34.132 | 4.576 | 0.722 | 96.226 |
| xgboost | post_covid | 6.705 | 33.410 | 4.395 | 0.706 | 98.113 |
| gat | post_covid | 6.907 | 40.982 | 5.006 | 0.731 | 98.113 |
| lstm | post_covid | 7.390 | 48.154 | 5.658 | 0.665 | 98.113 |
| arima | post_covid | 8.015 | 48.709 | 5.481 | 0.535 | 94.340 |
| persistence | post_covid | 8.644 | 42.229 | 6.090 | 0.580 | 96.226 |
| dualtopo | post_covid | 9.426 | 63.401 | 6.798 | 0.685 | 81.132 |
| seasonal_naive | post_covid | 9.674 | 41.354 | 6.137 | 0.651 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 20.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.471 | 29.158 | 5.983 | 0.571 | 92.308 |
| gnn_st_v2 | post_covid | 8.607 | 29.034 | 6.021 | 0.556 | 92.308 |
| xgboost | post_covid | 8.904 | 32.294 | 5.966 | 0.496 | 96.154 |
| lstm | post_covid | 9.015 | 35.639 | 6.750 | 0.499 | 96.154 |
| gat | post_covid | 9.374 | 45.290 | 7.709 | 0.522 | 96.154 |
| arima | post_covid | 10.268 | 29.638 | 6.727 | 0.399 | 88.462 |
| persistence | post_covid | 11.561 | 39.484 | 8.654 | 0.380 | 96.154 |
| dualtopo | post_covid | 11.653 | 33.977 | 7.974 | 0.525 | 73.077 |
| seasonal_naive | post_covid | 13.332 | 49.722 | 9.626 | 0.436 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 3.003 | 36.833 | 2.402 | 0.665 | 100.000 |
| xgboost | post_covid | 3.448 | 34.484 | 2.882 | 0.390 | 100.000 |
| seasonal_naive | post_covid | 3.542 | 33.296 | 2.778 | 0.566 | 100.000 |
| gnn_st | post_covid | 3.652 | 39.065 | 3.190 | 0.354 | 100.000 |
| gnn_st_v2 | post_covid | 3.652 | 39.043 | 3.185 | 0.354 | 100.000 |
| persistence | post_covid | 4.242 | 44.872 | 3.621 | 0.340 | 96.296 |
| arima | post_covid | 4.958 | 67.073 | 4.282 | 0.274 | 100.000 |
| lstm | post_covid | 5.379 | 60.205 | 4.606 | 0.314 | 100.000 |
| dualtopo | post_covid | 6.608 | 91.735 | 5.665 | 0.353 | 88.889 |

## Westerville

*mean observed 13.9, peak 45.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 13.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 7.576 | 45.349 | 5.403 | 0.645 | 94.340 |
| gnn_st | post_covid | 7.769 | 53.306 | 5.862 | 0.615 | 92.453 |
| gnn_st_v2 | post_covid | 7.828 | 53.223 | 5.881 | 0.608 | 92.453 |
| lstm | post_covid | 8.153 | 63.695 | 6.184 | 0.540 | 92.453 |
| gat | post_covid | 8.184 | 60.350 | 5.997 | 0.578 | 86.792 |
| arima | post_covid | 9.021 | 65.356 | 6.579 | 0.428 | 83.019 |
| dualtopo | post_covid | 9.698 | 80.224 | 6.996 | 0.578 | 73.585 |
| persistence | post_covid | 10.043 | 67.840 | 7.657 | 0.457 | 90.566 |
| seasonal_naive | post_covid | 10.196 | 78.064 | 7.188 | 0.502 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 18.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 9.598 | 36.255 | 7.095 | 0.485 | 92.308 |
| gnn_st | post_covid | 9.745 | 41.571 | 7.633 | 0.485 | 88.462 |
| gnn_st_v2 | post_covid | 9.835 | 41.400 | 7.671 | 0.477 | 88.462 |
| lstm | post_covid | 10.362 | 45.923 | 8.145 | 0.321 | 88.462 |
| gat | post_covid | 10.799 | 53.783 | 8.669 | 0.318 | 76.923 |
| arima | post_covid | 11.535 | 45.992 | 8.965 | 0.258 | 69.231 |
| dualtopo | post_covid | 12.187 | 35.483 | 8.313 | 0.364 | 65.385 |
| persistence | post_covid | 12.702 | 56.211 | 10.346 | 0.321 | 88.462 |
| seasonal_naive | post_covid | 13.045 | 58.895 | 9.688 | 0.335 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 4.378 | 66.429 | 3.425 | 0.615 | 96.296 |
| xgboost | post_covid | 4.896 | 53.769 | 3.774 | 0.551 | 96.296 |
| gnn_st | post_covid | 5.199 | 64.172 | 4.157 | 0.294 | 96.296 |
| lstm | post_covid | 5.205 | 80.151 | 4.295 | 0.324 | 96.296 |
| gnn_st_v2 | post_covid | 5.208 | 64.169 | 4.158 | 0.290 | 96.296 |
| arima | post_covid | 5.622 | 83.286 | 4.282 | 0.261 | 96.296 |
| seasonal_naive | post_covid | 6.341 | 95.813 | 4.780 | 0.157 | 100.000 |
| dualtopo | post_covid | 6.451 | 121.650 | 5.728 | 0.441 | 81.481 |
| persistence | post_covid | 6.529 | 78.608 | 5.068 | 0.262 | 92.593 |

## Bexley

*mean observed 12.4, peak 49.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 12.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 8.233 | 58.894 | 6.236 | 0.619 | 90.566 |
| gnn_st | post_covid | 8.252 | 59.267 | 6.237 | 0.617 | 90.566 |
| lstm | post_covid | 8.401 | 67.295 | 6.374 | 0.590 | 90.566 |
| gat | post_covid | 8.536 | 73.645 | 6.381 | 0.605 | 79.245 |
| xgboost | post_covid | 8.921 | 62.691 | 6.371 | 0.541 | 92.453 |
| arima | post_covid | 9.174 | 69.423 | 6.911 | 0.462 | 88.679 |
| dualtopo | post_covid | 10.339 | 81.581 | 7.906 | 0.577 | 67.925 |
| persistence | post_covid | 11.217 | 95.593 | 8.694 | 0.404 | 75.472 |
| seasonal_naive | post_covid | 12.792 | 84.257 | 8.561 | 0.297 | 90.566 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 9.497 | 64.376 | 7.585 | 0.534 | 92.308 |
| gnn_st | post_covid | 9.536 | 65.146 | 7.599 | 0.528 | 92.308 |
| lstm | post_covid | 10.104 | 71.036 | 7.851 | 0.420 | 88.462 |
| arima | post_covid | 10.698 | 69.054 | 8.229 | 0.368 | 88.462 |
| gat | post_covid | 10.806 | 93.703 | 8.616 | 0.378 | 65.385 |
| xgboost | post_covid | 10.974 | 79.433 | 8.281 | 0.255 | 92.308 |
| dualtopo | post_covid | 12.526 | 64.154 | 9.208 | 0.347 | 61.538 |
| persistence | post_covid | 12.886 | 96.489 | 10.687 | 0.325 | 80.769 |
| seasonal_naive | post_covid | 17.369 | 106.375 | 12.716 | -0.074 | 92.308 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 5.532 | 49.940 | 4.228 | 0.471 | 92.593 |
| seasonal_naive | post_covid | 5.541 | 58.117 | 4.559 | 0.606 | 88.889 |
| lstm | post_covid | 6.342 | 62.872 | 4.952 | 0.338 | 92.593 |
| xgboost | post_covid | 6.346 | 42.904 | 4.532 | 0.275 | 92.593 |
| gnn_st | post_covid | 6.790 | 52.320 | 4.925 | 0.031 | 88.889 |
| gnn_st_v2 | post_covid | 6.796 | 52.415 | 4.936 | 0.025 | 88.889 |
| arima | post_covid | 7.416 | 69.859 | 5.642 | -0.084 | 88.889 |
| dualtopo | post_covid | 7.665 | 102.175 | 6.651 | 0.330 | 74.074 |
| persistence | post_covid | 9.330 | 94.535 | 6.774 | -0.088 | 70.370 |

## Worthington

*mean observed 11.8, peak 44.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 11.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 7.078 | 50.519 | 4.716 | 0.669 | 86.792 |
| gnn_st | post_covid | 7.114 | 50.363 | 4.822 | 0.630 | 90.566 |
| gnn_st_v2 | post_covid | 7.155 | 50.400 | 4.852 | 0.626 | 90.566 |
| xgboost | post_covid | 7.392 | 48.948 | 4.577 | 0.624 | 96.226 |
| arima | post_covid | 7.652 | 60.303 | 5.035 | 0.516 | 92.453 |
| lstm | post_covid | 7.656 | 56.824 | 5.067 | 0.655 | 90.566 |
| seasonal_naive | post_covid | 8.559 | 61.813 | 5.793 | 0.451 | 90.566 |
| persistence | post_covid | 8.773 | 73.621 | 6.111 | 0.491 | 96.226 |
| dualtopo | post_covid | 9.655 | 73.432 | 6.634 | 0.648 | 75.472 |

### Flu season (Oct–Mar), 26 weeks scored, mean 16.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.080 | 36.328 | 6.350 | 0.500 | 88.462 |
| gnn_st_v2 | post_covid | 9.149 | 36.620 | 6.418 | 0.493 | 88.462 |
| gat | post_covid | 9.174 | 41.604 | 6.313 | 0.507 | 88.462 |
| xgboost | post_covid | 9.525 | 39.200 | 5.993 | 0.436 | 92.308 |
| arima | post_covid | 10.039 | 40.423 | 6.790 | 0.358 | 88.462 |
| lstm | post_covid | 10.145 | 42.754 | 7.090 | 0.508 | 84.615 |
| seasonal_naive | post_covid | 10.943 | 42.107 | 7.442 | 0.291 | 92.308 |
| persistence | post_covid | 11.203 | 54.431 | 7.981 | 0.355 | 96.154 |
| dualtopo | post_covid | 13.064 | 53.064 | 9.743 | 0.583 | 53.846 |

### Off-season (Apr–Sep), 27 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.995 | 70.372 | 3.120 | 0.433 | 96.296 |
| gat | post_covid | 4.161 | 59.105 | 3.178 | 0.527 | 85.185 |
| arima | post_covid | 4.228 | 79.446 | 3.345 | 0.339 | 96.296 |
| dualtopo | post_covid | 4.318 | 93.046 | 3.641 | -0.161 | 96.296 |
| xgboost | post_covid | 4.460 | 58.335 | 3.213 | 0.357 | 100.000 |
| gnn_st_v2 | post_covid | 4.460 | 63.669 | 3.345 | 0.303 | 92.593 |
| gnn_st | post_covid | 4.466 | 63.878 | 3.350 | 0.301 | 92.593 |
| seasonal_naive | post_covid | 5.335 | 80.790 | 4.206 | 0.112 | 88.889 |
| persistence | post_covid | 5.497 | 92.101 | 4.310 | 0.236 | 96.296 |

## Hilliard

*mean observed 10.3, peak 34.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.159 | 35573257.986 | 3.892 | 0.784 | 94.340 |
| gnn_st_v2 | post_covid | 5.199 | 35190758.772 | 3.872 | 0.782 | 94.340 |
| xgboost | post_covid | 5.694 | 32207146.832 | 4.378 | 0.742 | 96.226 |
| gat | post_covid | 6.179 | 89.570 | 5.012 | 0.699 | 94.340 |
| lstm | post_covid | 6.626 | 102.893 | 5.193 | 0.617 | 94.340 |
| arima | post_covid | 6.934 | 101.113 | 5.588 | 0.612 | 94.340 |
| persistence | post_covid | 7.031 | 90.599 | 5.516 | 0.629 | 92.453 |
| dualtopo | post_covid | 8.225 | 123.929 | 6.754 | 0.649 | 79.245 |
| seasonal_naive | post_covid | 9.588 | 126.365 | 7.238 | 0.508 | 100.000 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.742 | 46049723.343 | 4.400 | 0.772 | 96.154 |
| gnn_st_v2 | post_covid | 5.810 | 45103403.662 | 4.350 | 0.768 | 96.154 |
| xgboost | post_covid | 6.600 | 50706488.849 | 5.383 | 0.689 | 96.154 |
| persistence | post_covid | 7.413 | 56.654 | 5.771 | 0.638 | 96.154 |
| gat | post_covid | 7.470 | 68.680 | 6.136 | 0.620 | 92.308 |
| lstm | post_covid | 7.471 | 70.671 | 6.093 | 0.535 | 96.154 |
| arima | post_covid | 8.175 | 54.253 | 6.558 | 0.692 | 88.462 |
| dualtopo | post_covid | 10.134 | 68.556 | 8.358 | 0.620 | 61.538 |
| seasonal_naive | post_covid | 12.263 | 89.764 | 9.758 | 0.346 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.528 | 25484809.864 | 3.404 | 0.309 | 92.593 |
| gnn_st_v2 | post_covid | 4.533 | 25645248.878 | 3.411 | 0.305 | 92.593 |
| gat | post_covid | 4.606 | 109.657 | 3.930 | 0.205 | 96.296 |
| xgboost | post_covid | 4.659 | 14392965.631 | 3.411 | 0.331 | 96.296 |
| arima | post_covid | 5.481 | 146.172 | 4.654 | 0.098 | 100.000 |
| lstm | post_covid | 5.695 | 133.875 | 4.325 | 0.109 | 92.593 |
| dualtopo | post_covid | 5.823 | 177.173 | 5.210 | -0.050 | 96.296 |
| seasonal_naive | post_covid | 5.969 | 161.559 | 4.813 | 0.067 | 100.000 |
| persistence | post_covid | 6.644 | 123.238 | 5.271 | 0.092 | 88.889 |

## Clintonville/Near North

*mean observed 10.2, peak 27.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 10.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.659 | 37.659 | 2.804 | 0.865 | 100.000 |
| gnn_st_v2 | post_covid | 3.693 | 37.598 | 2.819 | 0.865 | 100.000 |
| gat | post_covid | 3.983 | 45.351 | 2.994 | 0.818 | 94.340 |
| seasonal_naive | post_covid | 4.314 | 41.975 | 3.353 | 0.789 | 100.000 |
| arima | post_covid | 4.562 | 53.019 | 3.550 | 0.749 | 96.226 |
| lstm | post_covid | 4.589 | 54.410 | 3.414 | 0.750 | 100.000 |
| persistence | post_covid | 4.739 | 49.434 | 3.721 | 0.749 | 100.000 |
| xgboost | post_covid | 5.766 | 47.894 | 4.045 | 0.707 | 100.000 |
| dualtopo | post_covid | 7.008 | 80.030 | 5.088 | 0.822 | 79.245 |

### Flu season (Oct–Mar), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.436 | 26.625 | 3.547 | 0.799 | 100.000 |
| gnn_st_v2 | post_covid | 4.495 | 26.599 | 3.584 | 0.796 | 100.000 |
| seasonal_naive | post_covid | 4.810 | 30.657 | 3.714 | 0.704 | 100.000 |
| gat | post_covid | 4.927 | 32.526 | 3.941 | 0.717 | 92.308 |
| arima | post_covid | 5.785 | 34.102 | 4.642 | 0.625 | 92.308 |
| persistence | post_covid | 5.835 | 39.658 | 4.859 | 0.625 | 100.000 |
| lstm | post_covid | 5.862 | 33.237 | 4.533 | 0.598 | 100.000 |
| xgboost | post_covid | 7.584 | 41.809 | 5.662 | 0.522 | 100.000 |
| dualtopo | post_covid | 9.212 | 42.032 | 7.083 | 0.737 | 57.692 |

### Off-season (Apr–Sep), 27 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 2.706 | 48.188 | 2.082 | 0.703 | 100.000 |
| gnn_st | post_covid | 2.709 | 48.284 | 2.089 | 0.702 | 100.000 |
| gat | post_covid | 2.786 | 57.702 | 2.081 | 0.689 | 96.296 |
| lstm | post_covid | 2.871 | 74.798 | 2.337 | 0.560 | 100.000 |
| arima | post_covid | 2.937 | 71.236 | 2.498 | 0.557 | 100.000 |
| xgboost | post_covid | 3.142 | 53.754 | 2.488 | 0.770 | 100.000 |
| persistence | post_covid | 3.361 | 58.847 | 2.625 | 0.557 | 100.000 |
| seasonal_naive | post_covid | 3.777 | 52.874 | 3.006 | 0.373 | 100.000 |
| dualtopo | post_covid | 3.832 | 116.621 | 3.166 | 0.576 | 100.000 |

## Far Southeast

*mean observed 5.6, peak 14.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.174 | 70.565 | 2.624 | 0.499 | 100.000 |
| gnn_st_v2 | post_covid | 3.180 | 70.131 | 2.626 | 0.496 | 98.113 |
| lstm | post_covid | 3.239 | 81.137 | 2.599 | 0.423 | 100.000 |
| xgboost | post_covid | 3.434 | 76.451 | 2.685 | 0.438 | 100.000 |
| dualtopo | post_covid | 3.453 | 82.137 | 2.742 | 0.336 | 92.453 |
| arima | post_covid | 3.495 | 84.723 | 2.833 | 0.244 | 98.113 |
| gat | post_covid | 3.571 | 80.147 | 2.589 | 0.506 | 96.226 |
| persistence | post_covid | 4.282 | 101.809 | 3.495 | 0.246 | 94.340 |
| seasonal_naive | post_covid | 6.079 | 118.809 | 4.209 | 0.365 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.789 | 73.811 | 3.051 | 0.249 | 100.000 |
| gnn_st | post_covid | 3.801 | 69.940 | 3.177 | 0.348 | 100.000 |
| gnn_st_v2 | post_covid | 3.810 | 69.022 | 3.180 | 0.346 | 96.154 |
| dualtopo | post_covid | 4.172 | 57.199 | 3.330 | 0.189 | 84.615 |
| arima | post_covid | 4.229 | 69.231 | 3.540 | 0.099 | 96.154 |
| xgboost | post_covid | 4.385 | 82.412 | 3.591 | 0.218 | 100.000 |
| gat | post_covid | 4.681 | 104.059 | 3.539 | 0.208 | 92.308 |
| persistence | post_covid | 5.049 | 85.871 | 4.290 | 0.136 | 92.308 |
| seasonal_naive | post_covid | 8.088 | 148.154 | 6.035 | 0.164 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 4.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 1.982 | 57.120 | 1.674 | 0.370 | 100.000 |
| xgboost | post_covid | 2.152 | 70.710 | 1.813 | 0.074 | 100.000 |
| gnn_st | post_covid | 2.422 | 71.167 | 2.092 | 0.051 | 100.000 |
| gnn_st_v2 | post_covid | 2.423 | 71.199 | 2.093 | 0.046 | 100.000 |
| dualtopo | post_covid | 2.576 | 106.153 | 2.175 | -0.004 | 100.000 |
| arima | post_covid | 2.601 | 99.642 | 2.152 | -0.119 | 100.000 |
| lstm | post_covid | 2.602 | 88.191 | 2.165 | -0.074 | 100.000 |
| seasonal_naive | post_covid | 3.087 | 90.550 | 2.450 | 0.185 | 96.296 |
| persistence | post_covid | 3.384 | 117.158 | 2.731 | -0.153 | 96.296 |

## Dublin

*mean observed 5.4, peak 16.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 5.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 2.677 | 48.864 | 1.917 | 0.678 | 94.340 |
| gnn_st | post_covid | 2.734 | 12250181.777 | 2.124 | 0.718 | 100.000 |
| gnn_st_v2 | post_covid | 2.777 | 12206475.197 | 2.141 | 0.710 | 100.000 |
| arima | post_covid | 2.981 | 54.160 | 2.107 | 0.581 | 98.113 |
| lstm | post_covid | 3.088 | 59.488 | 2.354 | 0.579 | 98.113 |
| persistence | post_covid | 3.295 | 60.355 | 2.373 | 0.571 | 98.113 |
| xgboost | post_covid | 3.422 | 23367197.462 | 2.432 | 0.523 | 98.113 |
| seasonal_naive | post_covid | 3.619 | 54.484 | 2.775 | 0.632 | 96.226 |
| dualtopo | post_covid | 3.908 | 77.120 | 2.946 | 0.642 | 83.019 |

### Flu season (Oct–Mar), 26 weeks scored, mean 7.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 3.120 | 33.870 | 2.183 | 0.475 | 96.154 |
| gnn_st | post_covid | 3.194 | 39.127 | 2.575 | 0.545 | 100.000 |
| gnn_st_v2 | post_covid | 3.266 | 39.337 | 2.610 | 0.528 | 100.000 |
| lstm | post_covid | 3.789 | 45.648 | 2.916 | 0.317 | 96.154 |
| arima | post_covid | 3.810 | 44.099 | 2.727 | 0.231 | 96.154 |
| persistence | post_covid | 4.230 | 54.716 | 3.136 | 0.241 | 100.000 |
| xgboost | post_covid | 4.364 | 46.203 | 3.099 | 0.259 | 96.154 |
| seasonal_naive | post_covid | 4.582 | 57.247 | 3.752 | 0.479 | 100.000 |
| dualtopo | post_covid | 5.050 | 48.697 | 3.954 | 0.497 | 69.231 |

### Off-season (Apr–Sep), 27 weeks scored, mean 3.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1.861 | 64.221 | 1.511 | 0.613 | 100.000 |
| persistence | post_covid | 2.022 | 65.995 | 1.637 | 0.565 | 96.296 |
| xgboost | post_covid | 2.155 | 45868898.675 | 1.790 | 0.464 | 100.000 |
| gat | post_covid | 2.168 | 63.857 | 1.661 | 0.474 | 92.593 |
| gnn_st | post_covid | 2.201 | 24046615.441 | 1.690 | 0.610 | 100.000 |
| gnn_st_v2 | post_covid | 2.206 | 23960820.841 | 1.688 | 0.609 | 100.000 |
| lstm | post_covid | 2.212 | 73.327 | 1.813 | 0.352 | 100.000 |
| dualtopo | post_covid | 2.327 | 105.542 | 1.975 | 0.085 | 96.296 |
| seasonal_naive | post_covid | 2.342 | 51.722 | 1.835 | 0.494 | 92.593 |

## UA/Grandview

*mean observed 4.4, peak 15.9 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 4.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 2.610 | 44.904 | 1.748 | 0.687 | 96.226 |
| gnn_st_v2 | post_covid | 2.628 | 44.925 | 1.766 | 0.683 | 96.226 |
| lstm | post_covid | 2.957 | 54.470 | 1.940 | 0.549 | 96.226 |
| arima | post_covid | 3.105 | 62.564 | 2.193 | 0.508 | 96.226 |
| gat | post_covid | 3.173 | 59.268 | 2.417 | 0.615 | 98.113 |
| persistence | post_covid | 3.524 | 70.583 | 2.406 | 0.505 | 92.453 |
| dualtopo | post_covid | 3.542 | 73.731 | 2.483 | 0.552 | 92.453 |
| xgboost | post_covid | 3.602 | 63.372 | 2.421 | 0.469 | 98.113 |
| seasonal_naive | post_covid | 5.480 | 87.113 | 3.608 | 0.364 | 98.113 |

### Flu season (Oct–Mar), 26 weeks scored, mean 6.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.316 | 32.984 | 2.109 | 0.556 | 96.154 |
| gnn_st_v2 | post_covid | 3.350 | 33.406 | 2.155 | 0.549 | 96.154 |
| lstm | post_covid | 3.800 | 39.389 | 2.508 | 0.310 | 92.308 |
| arima | post_covid | 3.885 | 41.513 | 2.731 | 0.378 | 92.308 |
| gat | post_covid | 4.212 | 66.414 | 3.575 | 0.370 | 96.154 |
| persistence | post_covid | 4.375 | 50.374 | 2.977 | 0.391 | 96.154 |
| dualtopo | post_covid | 4.532 | 42.921 | 3.084 | 0.365 | 84.615 |
| xgboost | post_covid | 4.910 | 62.867 | 3.655 | 0.194 | 96.154 |
| seasonal_naive | post_covid | 7.535 | 96.068 | 5.736 | 0.113 | 100.000 |

### Off-season (Apr–Sep), 27 weeks scored, mean 2.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 1.501 | 63.898 | 1.233 | 0.318 | 100.000 |
| gat | post_covid | 1.635 | 51.837 | 1.303 | 0.137 | 100.000 |
| gnn_st_v2 | post_covid | 1.659 | 56.906 | 1.391 | 0.050 | 96.296 |
| gnn_st | post_covid | 1.669 | 57.301 | 1.400 | 0.036 | 96.296 |
| lstm | post_covid | 1.804 | 70.154 | 1.394 | 0.168 | 100.000 |
| seasonal_naive | post_covid | 2.067 | 77.800 | 1.560 | 0.161 | 96.296 |
| arima | post_covid | 2.097 | 84.456 | 1.676 | -0.357 | 100.000 |
| dualtopo | post_covid | 2.201 | 105.773 | 1.905 | 0.028 | 100.000 |
| persistence | post_covid | 2.440 | 91.600 | 1.855 | -0.260 | 88.889 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st, gnn_st_v2; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, gnn_st_v2, lstm). Differences here are not purely model quality.
