# Per-neighborhood leaderboard — horizon 1

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Apr–Sep), Off-season (Oct–Mar).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* them -- LOMAS DE ZAMORA has 12 fewer scored weeks than the best-covered node (41 against 53) -- so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

> **MAPE is not usable in this table** (it reaches 1,148%). It divides by the observed rate, and this city reports observed zeros and near-zeros rather than suppressing small counts, so the denominator goes to zero. Rank on RMSE or MAE. The column is kept so the two cities' tables have the same shape.

## Summary — neighborhoods won, out of 19

| model | Overall (full year) | Flu season (Apr–Sep) | Off-season (Oct–Mar) |
| --- | --- | --- | --- |
| gnn_st | 12 | 6 | 9 |
| persistence | 5 | 5 | 6 |
| arima | 1 | 3 | 1 |
| xgboost | 1 | 1 | 2 |
| dualtopo | 0 | 1 | 0 |
| gat | 0 | 1 | 0 |
| lstm | 0 | 0 | 1 |
| seasonal_naive | 0 | 1 | 0 |
| xgboost_nodemo | 0 | 1 | 0 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `arima (post_covid)`: J.C.Paz; `gnn_st (post_covid)`: AlmBrown, Avellan., Ezeiza, F.Varela, LaMatanza, Lanús, MalvArg., Merlo, Morón, Quilmes, S.Isidro, TresFeb.; `persistence (post_covid)`: LomasZam., Moreno, S.Miguel, Tigre, V.López; `xgboost (post_covid)`: S.Martín
- **Flu season (Apr–Sep)** — `arima (post_covid)`: AlmBrown, J.C.Paz, Merlo; `dualtopo (post_covid)`: Avellan.; `gat (post_covid)`: Quilmes; `gnn_st (post_covid)`: Ezeiza, F.Varela, LaMatanza, Lanús, MalvArg., Morón; `persistence (post_covid)`: LomasZam., Moreno, S.Miguel, Tigre, V.López; `seasonal_naive (post_covid)`: S.Isidro; `xgboost (post_covid)`: S.Martín; `xgboost_nodemo (post_covid)`: TresFeb.
- **Off-season (Oct–Mar)** — `arima (post_covid)`: MalvArg.; `gnn_st (post_covid)`: AlmBrown, F.Varela, LaMatanza, Morón, Quilmes, S.Isidro, S.Martín, S.Miguel, TresFeb.; `lstm (post_covid)`: Lanús; `persistence (post_covid)`: J.C.Paz, LomasZam., Merlo, Moreno, Tigre, V.López; `xgboost (post_covid)`: Avellan., Ezeiza

`gnn_st (post_covid)` wins 12 of 19 neighborhoods. `gnn_st (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## JOSÉ C. PAZ

*mean observed 257.3, peak 740.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 257.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 76.416 | 16.567 | 46.592 | 0.859 | 83.019 |
| gnn_st | post_covid | 82.234 | 18.260 | 51.971 | 0.867 | 75.472 |
| persistence | post_covid | 82.563 | 17.266 | 48.204 | 0.839 | 75.472 |
| gat | post_covid | 164.720 | 49.853 | 123.241 | 0.606 | 24.528 |
| dualtopo | post_covid | 174.595 | 58.042 | 140.787 | 0.699 | 13.208 |
| xgboost | post_covid | 194.067 | 64.374 | 165.886 | 0.847 | 100.000 |
| xgboost_nodemo | post_covid | 203.413 | 70.136 | 176.929 | 0.847 | 3.774 |
| seasonal_naive | post_covid | 218.736 | 67.845 | 167.144 | 0.317 | 33.962 |
| lstm | post_covid | 248.341 | 80.209 | 207.402 | 0.354 | 3.774 |

### Flu season (Apr–Sep), 26 weeks scored, mean 362.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 103.076 | 17.352 | 69.501 | 0.671 | 76.923 |
| gnn_st | post_covid | 109.701 | 17.479 | 73.004 | 0.685 | 69.231 |
| persistence | post_covid | 113.018 | 18.629 | 74.478 | 0.631 | 65.385 |
| dualtopo | post_covid | 211.865 | 46.441 | 171.495 | 0.400 | 19.231 |
| gat | post_covid | 217.888 | 41.066 | 167.363 | 0.024 | 34.615 |
| xgboost | post_covid | 247.272 | 61.523 | 224.366 | 0.676 | 100.000 |
| xgboost_nodemo | post_covid | 256.403 | 64.880 | 234.802 | 0.686 | 0.000 |
| seasonal_naive | post_covid | 281.790 | 59.246 | 224.270 | -0.208 | 26.923 |
| lstm | post_covid | 325.046 | 76.246 | 288.216 | -0.419 | 0.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 156.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 32.877 | 15.953 | 22.902 | 0.869 | 85.185 |
| arima | post_covid | 35.091 | 15.810 | 24.532 | 0.846 | 88.889 |
| gnn_st | post_covid | 41.057 | 19.011 | 31.718 | 0.885 | 81.481 |
| gat | post_covid | 86.853 | 58.314 | 80.752 | 0.868 | 14.815 |
| xgboost | post_covid | 122.678 | 67.120 | 109.572 | 0.683 | 100.000 |
| dualtopo | post_covid | 128.895 | 69.213 | 111.216 | 0.214 | 7.407 |
| seasonal_naive | post_covid | 132.113 | 76.125 | 112.133 | 0.506 | 40.741 |
| xgboost_nodemo | post_covid | 133.842 | 75.198 | 121.199 | 0.649 | 7.407 |
| lstm | post_covid | 138.998 | 84.025 | 129.581 | 0.793 | 7.407 |

## AVELLANEDA

*mean observed 143.6, peak 323.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 143.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 27.342 | 15.434 | 20.789 | 0.890 | 96.226 |
| arima | post_covid | 29.677 | 17.491 | 23.576 | 0.852 | 90.566 |
| dualtopo | post_covid | 29.827 | 17.914 | 23.941 | 0.871 | 88.679 |
| persistence | post_covid | 30.351 | 17.387 | 24.609 | 0.854 | 94.340 |
| lstm | post_covid | 36.372 | 20.183 | 28.172 | 0.810 | 100.000 |
| gat | post_covid | 38.682 | 20.085 | 29.127 | 0.848 | 90.566 |
| xgboost_nodemo | post_covid | 40.364 | 19.034 | 28.624 | 0.834 | 98.113 |
| xgboost | post_covid | 40.530 | 19.177 | 29.191 | 0.835 | 100.000 |
| seasonal_naive | post_covid | 46.153 | 26.007 | 35.405 | 0.858 | 96.226 |

### Flu season (Apr–Sep), 26 weeks scored, mean 185.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 31.182 | 15.890 | 26.899 | 0.765 | 92.308 |
| gnn_st | post_covid | 32.785 | 14.799 | 25.323 | 0.761 | 96.154 |
| arima | post_covid | 33.904 | 15.157 | 27.858 | 0.695 | 92.308 |
| persistence | post_covid | 35.434 | 17.314 | 30.744 | 0.704 | 96.154 |
| lstm | post_covid | 43.484 | 20.379 | 35.601 | 0.537 | 100.000 |
| gat | post_covid | 44.628 | 17.822 | 34.305 | 0.656 | 96.154 |
| xgboost_nodemo | post_covid | 53.874 | 25.462 | 43.692 | 0.633 | 96.154 |
| xgboost | post_covid | 54.140 | 25.932 | 44.835 | 0.647 | 100.000 |
| seasonal_naive | post_covid | 54.852 | 22.597 | 42.265 | 0.810 | 92.308 |

### Off-season (Oct–Mar), 27 weeks scored, mean 103.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 20.051 | 12.672 | 14.126 | 0.803 | 100.000 |
| xgboost_nodemo | post_covid | 20.082 | 12.844 | 14.114 | 0.786 | 100.000 |
| gnn_st | post_covid | 20.795 | 16.046 | 16.423 | 0.761 | 96.296 |
| persistence | post_covid | 24.477 | 17.458 | 18.702 | 0.649 | 92.593 |
| arima | post_covid | 24.938 | 19.739 | 19.453 | 0.643 | 88.889 |
| lstm | post_covid | 27.857 | 19.993 | 21.018 | 0.566 | 100.000 |
| dualtopo | post_covid | 28.463 | 19.864 | 21.093 | 0.584 | 85.185 |
| gat | post_covid | 31.927 | 22.264 | 24.141 | 0.660 | 85.185 |
| seasonal_naive | post_covid | 35.833 | 29.290 | 28.799 | 0.505 | 100.000 |

## EZEIZA

*mean observed 83.5, peak 186.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 83.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.666 | 15.419 | 10.395 | 0.955 | 100.000 |
| xgboost_nodemo | post_covid | 15.314 | 15.937 | 12.396 | 0.935 | 100.000 |
| xgboost | post_covid | 16.541 | 16.119 | 13.264 | 0.926 | 100.000 |
| persistence | post_covid | 16.654 | 17.596 | 13.109 | 0.922 | 100.000 |
| dualtopo | post_covid | 18.757 | 29.359 | 16.207 | 0.909 | 98.113 |
| gat | post_covid | 24.690 | 36.706 | 20.472 | 0.882 | 100.000 |
| seasonal_naive | post_covid | 28.077 | 28.828 | 21.442 | 0.782 | 100.000 |
| lstm | post_covid | 31.605 | 29.336 | 23.213 | 0.785 | 96.226 |
| arima | post_covid | 42.247 | 62.712 | 37.068 |  | 52.830 |

### Flu season (Apr–Sep), 26 weeks scored, mean 119.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.177 | 9.370 | 11.556 | 0.852 | 100.000 |
| dualtopo | post_covid | 16.784 | 11.968 | 14.346 | 0.846 | 100.000 |
| xgboost_nodemo | post_covid | 19.190 | 13.714 | 16.940 | 0.798 | 100.000 |
| persistence | post_covid | 20.130 | 12.708 | 15.975 | 0.736 | 100.000 |
| xgboost | post_covid | 21.545 | 15.402 | 19.029 | 0.755 | 100.000 |
| gat | post_covid | 22.329 | 13.656 | 16.041 | 0.616 | 100.000 |
| seasonal_naive | post_covid | 35.148 | 23.853 | 28.668 | 0.633 | 100.000 |
| lstm | post_covid | 41.933 | 26.324 | 33.971 | 0.134 | 92.308 |
| arima | post_covid | 45.002 | 28.620 | 37.566 |  | 61.538 |

### Off-season (Oct–Mar), 27 weeks scored, mean 48.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 9.490 | 16.808 | 7.714 | 0.847 | 100.000 |
| xgboost_nodemo | post_covid | 10.283 | 18.078 | 8.021 | 0.828 | 100.000 |
| gnn_st | post_covid | 11.017 | 21.244 | 9.278 | 0.838 | 100.000 |
| persistence | post_covid | 12.419 | 22.303 | 10.348 | 0.770 | 100.000 |
| lstm | post_covid | 16.354 | 32.236 | 12.852 | 0.540 | 100.000 |
| seasonal_naive | post_covid | 18.915 | 33.620 | 14.483 | 0.600 | 100.000 |
| dualtopo | post_covid | 20.477 | 46.107 | 17.999 | 0.439 | 96.296 |
| gat | post_covid | 26.767 | 58.902 | 24.740 | 0.678 | 100.000 |
| arima | post_covid | 39.413 | 95.542 | 36.588 |  | 44.444 |

## MORENO

*mean observed 74.1, peak 197.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 74.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 15.607 | 21.144 | 11.573 | 0.948 | 98.113 |
| gnn_st | post_covid | 18.258 | 20.523 | 12.136 | 0.935 | 94.340 |
| lstm | post_covid | 18.803 | 28.005 | 13.485 | 0.924 | 100.000 |
| dualtopo | post_covid | 25.645 | 38.401 | 22.004 | 0.900 | 83.019 |
| arima | post_covid | 26.045 | 45.201 | 19.540 | 0.909 | 84.906 |
| gat | post_covid | 27.248 | 37.481 | 20.245 | 0.841 | 96.226 |
| xgboost_nodemo | post_covid | 34.628 | 36.789 | 26.237 | 0.745 | 92.453 |
| xgboost | post_covid | 34.737 | 43.251 | 24.974 | 0.712 | 100.000 |
| seasonal_naive | post_covid | 41.066 | 62.099 | 32.407 | 0.593 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 112.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 20.632 | 14.615 | 16.608 | 0.847 | 96.154 |
| lstm | post_covid | 23.531 | 15.633 | 17.073 | 0.769 | 100.000 |
| gnn_st | post_covid | 24.328 | 15.288 | 17.980 | 0.782 | 88.462 |
| dualtopo | post_covid | 31.536 | 27.138 | 28.602 | 0.841 | 84.615 |
| arima | post_covid | 33.881 | 22.213 | 26.730 | 0.756 | 73.077 |
| gat | post_covid | 35.851 | 26.194 | 28.802 | 0.532 | 92.308 |
| xgboost_nodemo | post_covid | 46.781 | 35.445 | 41.379 | 0.281 | 88.462 |
| xgboost | post_covid | 48.090 | 34.142 | 40.559 | 0.190 | 100.000 |
| seasonal_naive | post_covid | 54.343 | 39.429 | 45.983 | 0.241 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 37.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 8.259 | 27.431 | 6.725 | 0.928 | 100.000 |
| gnn_st | post_covid | 9.190 | 25.565 | 6.509 | 0.924 | 100.000 |
| xgboost | post_covid | 11.901 | 52.022 | 9.966 | 0.881 | 100.000 |
| lstm | post_covid | 12.681 | 39.920 | 10.030 | 0.922 | 100.000 |
| gat | post_covid | 14.821 | 48.351 | 12.005 | 0.758 | 100.000 |
| arima | post_covid | 15.039 | 67.337 | 12.617 | 0.869 | 96.296 |
| xgboost_nodemo | post_covid | 15.695 | 38.084 | 11.656 | 0.831 | 96.296 |
| dualtopo | post_covid | 18.257 | 49.246 | 15.651 | 0.729 | 81.481 |
| seasonal_naive | post_covid | 21.601 | 83.929 | 19.333 | 0.462 | 100.000 |

## LANÚS

*mean observed 70.6, peak 171.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 70.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.798 | 14.752 | 10.200 | 0.926 | 98.113 |
| xgboost | post_covid | 16.862 | 17.828 | 12.156 | 0.905 | 100.000 |
| persistence | post_covid | 17.135 | 17.852 | 12.770 | 0.887 | 98.113 |
| xgboost_nodemo | post_covid | 17.699 | 19.044 | 12.905 | 0.906 | 100.000 |
| arima | post_covid | 17.932 | 20.415 | 13.495 | 0.880 | 96.226 |
| gat | post_covid | 21.460 | 19.456 | 14.705 | 0.893 | 96.226 |
| lstm | post_covid | 22.051 | 19.514 | 14.586 | 0.798 | 100.000 |
| seasonal_naive | post_covid | 23.021 | 22.954 | 16.624 | 0.820 | 100.000 |
| dualtopo | post_covid | 24.339 | 33.727 | 18.613 | 0.847 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 98.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.557 | 14.640 | 14.449 | 0.802 | 100.000 |
| xgboost | post_covid | 19.244 | 13.993 | 13.867 | 0.805 | 100.000 |
| xgboost_nodemo | post_covid | 19.474 | 15.647 | 14.655 | 0.805 | 100.000 |
| persistence | post_covid | 22.051 | 18.084 | 18.286 | 0.708 | 100.000 |
| arima | post_covid | 23.006 | 18.924 | 18.829 | 0.702 | 96.154 |
| seasonal_naive | post_covid | 28.794 | 22.776 | 23.214 | 0.719 | 100.000 |
| gat | post_covid | 29.383 | 20.131 | 22.174 | 0.674 | 92.308 |
| dualtopo | post_covid | 30.062 | 25.518 | 24.199 | 0.749 | 96.154 |
| lstm | post_covid | 30.443 | 22.017 | 22.759 | -0.041 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 43.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 7.873 | 17.103 | 6.715 | 0.936 | 100.000 |
| gat | post_covid | 8.520 | 18.805 | 7.513 | 0.855 | 100.000 |
| gnn_st | post_covid | 8.770 | 14.860 | 6.108 | 0.874 | 96.296 |
| persistence | post_covid | 10.396 | 17.628 | 7.459 | 0.808 | 96.296 |
| arima | post_covid | 11.024 | 21.851 | 8.357 | 0.788 | 96.296 |
| xgboost | post_covid | 14.195 | 21.520 | 10.508 | 0.797 | 100.000 |
| seasonal_naive | post_covid | 15.553 | 23.126 | 10.278 | 0.468 | 100.000 |
| xgboost_nodemo | post_covid | 15.802 | 22.314 | 11.220 | 0.795 | 100.000 |
| dualtopo | post_covid | 17.105 | 41.631 | 13.234 | 0.428 | 100.000 |

## FLORENCIO VARELA

*mean observed 53.7, peak 146.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 53.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 11.262 | 16.444 | 8.418 | 0.930 | 100.000 |
| xgboost | post_covid | 12.796 | 21.754 | 10.329 | 0.909 | 100.000 |
| xgboost_nodemo | post_covid | 13.302 | 19.979 | 9.998 | 0.914 | 100.000 |
| persistence | post_covid | 13.856 | 20.225 | 10.209 | 0.895 | 100.000 |
| lstm | post_covid | 13.881 | 17.001 | 9.610 | 0.891 | 100.000 |
| dualtopo | post_covid | 15.761 | 28.403 | 11.753 | 0.866 | 98.113 |
| gat | post_covid | 20.128 | 26.728 | 14.938 | 0.872 | 94.340 |
| seasonal_naive | post_covid | 21.981 | 32.443 | 17.099 | 0.811 | 100.000 |
| arima | post_covid | 31.112 | 54.153 | 23.811 |  | 83.019 |

### Flu season (Apr–Sep), 26 weeks scored, mean 76.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.458 | 14.879 | 11.602 | 0.850 | 100.000 |
| xgboost_nodemo | post_covid | 15.076 | 16.064 | 11.760 | 0.842 | 100.000 |
| xgboost | post_covid | 15.635 | 18.604 | 13.166 | 0.816 | 100.000 |
| persistence | post_covid | 17.680 | 16.892 | 13.163 | 0.793 | 100.000 |
| lstm | post_covid | 17.948 | 17.225 | 13.328 | 0.759 | 100.000 |
| dualtopo | post_covid | 18.829 | 16.515 | 13.273 | 0.761 | 96.154 |
| gat | post_covid | 26.456 | 25.656 | 21.078 | 0.781 | 92.308 |
| seasonal_naive | post_covid | 28.006 | 30.369 | 22.886 | 0.603 | 100.000 |
| arima | post_covid | 39.896 | 35.928 | 31.412 |  | 65.385 |

### Off-season (Oct–Mar), 27 weeks scored, mean 32.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.904 | 17.951 | 5.351 | 0.845 | 100.000 |
| lstm | post_covid | 8.248 | 16.784 | 6.030 | 0.842 | 100.000 |
| persistence | post_covid | 8.709 | 23.435 | 7.364 | 0.801 | 100.000 |
| xgboost | post_covid | 9.273 | 24.787 | 7.597 | 0.717 | 100.000 |
| gat | post_covid | 11.014 | 27.761 | 9.026 | 0.687 | 96.296 |
| xgboost_nodemo | post_covid | 11.335 | 23.749 | 8.302 | 0.657 | 100.000 |
| dualtopo | post_covid | 12.092 | 39.851 | 10.290 | 0.381 | 100.000 |
| seasonal_naive | post_covid | 13.899 | 34.439 | 11.527 | 0.731 | 100.000 |
| arima | post_covid | 19.168 | 71.703 | 16.492 |  | 100.000 |

## TRES DE FEBRERO

*mean observed 45.7, peak 114.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 45.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.411 | 20.480 | 9.106 | 0.844 | 100.000 |
| lstm | post_covid | 13.481 | 23.616 | 9.988 | 0.837 | 100.000 |
| xgboost_nodemo | post_covid | 13.563 | 25.761 | 10.395 | 0.829 | 100.000 |
| arima | post_covid | 13.666 | 24.603 | 10.286 | 0.803 | 100.000 |
| xgboost | post_covid | 14.046 | 24.502 | 10.717 | 0.821 | 100.000 |
| dualtopo | post_covid | 14.532 | 25.377 | 10.686 | 0.789 | 96.226 |
| persistence | post_covid | 14.643 | 23.172 | 10.776 | 0.793 | 100.000 |
| gat | post_covid | 16.978 | 28.711 | 12.184 | 0.708 | 96.226 |
| seasonal_naive | post_covid | 23.033 | 43.261 | 16.973 | 0.752 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 63.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 16.577 | 21.779 | 12.993 | 0.570 | 100.000 |
| gnn_st | post_covid | 16.749 | 22.882 | 13.752 | 0.493 | 100.000 |
| xgboost | post_covid | 17.367 | 22.743 | 14.177 | 0.589 | 100.000 |
| lstm | post_covid | 17.740 | 20.920 | 13.946 | 0.484 | 100.000 |
| arima | post_covid | 17.770 | 23.600 | 14.400 | 0.451 | 100.000 |
| dualtopo | post_covid | 19.258 | 25.820 | 15.198 | 0.318 | 92.308 |
| persistence | post_covid | 19.429 | 26.410 | 15.990 | 0.374 | 100.000 |
| gat | post_covid | 22.595 | 25.572 | 17.314 | 0.168 | 92.308 |
| seasonal_naive | post_covid | 28.763 | 33.979 | 21.344 | 0.673 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 28.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.675 | 18.167 | 4.633 | 0.881 | 100.000 |
| lstm | post_covid | 7.328 | 26.213 | 6.177 | 0.802 | 100.000 |
| persistence | post_covid | 7.574 | 20.054 | 5.756 | 0.831 | 100.000 |
| dualtopo | post_covid | 7.578 | 24.950 | 6.342 | 0.772 | 100.000 |
| arima | post_covid | 7.907 | 25.569 | 6.325 | 0.806 | 100.000 |
| gat | post_covid | 8.615 | 31.734 | 7.245 | 0.703 | 100.000 |
| xgboost_nodemo | post_covid | 9.821 | 29.595 | 7.892 | 0.565 | 100.000 |
| xgboost | post_covid | 9.840 | 26.196 | 7.385 | 0.563 | 100.000 |
| seasonal_naive | post_covid | 15.644 | 52.199 | 12.763 | 0.255 | 100.000 |

## GENERAL SAN MARTÍN

*mean observed 38.6, peak 99.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 14.540 | 32.182 | 10.760 | 0.829 | 100.000 |
| gnn_st | post_covid | 14.683 | 34.154 | 10.701 | 0.771 | 88.679 |
| dualtopo | post_covid | 15.854 | 38.584 | 11.774 | 0.700 | 92.453 |
| xgboost_nodemo | post_covid | 16.448 | 38.858 | 12.184 | 0.813 | 100.000 |
| arima | post_covid | 16.763 | 39.599 | 12.452 | 0.675 | 88.679 |
| persistence | post_covid | 17.623 | 36.987 | 12.476 | 0.678 | 86.792 |
| lstm | post_covid | 17.733 | 45.004 | 12.878 | 0.718 | 100.000 |
| seasonal_naive | post_covid | 24.468 | 62.580 | 17.527 | 0.798 | 100.000 |
| gat | post_covid | 26.302 | 52.428 | 19.914 | 0.157 | 79.245 |

### Flu season (Apr–Sep), 26 weeks scored, mean 50.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 18.478 | 37.435 | 14.922 | 0.743 | 100.000 |
| gnn_st | post_covid | 19.511 | 42.985 | 15.430 | 0.613 | 76.923 |
| dualtopo | post_covid | 20.036 | 42.712 | 16.329 | 0.516 | 88.462 |
| xgboost_nodemo | post_covid | 20.151 | 41.161 | 16.015 | 0.720 | 100.000 |
| arima | post_covid | 22.329 | 47.591 | 18.234 | 0.473 | 76.923 |
| persistence | post_covid | 23.764 | 50.680 | 18.978 | 0.469 | 76.923 |
| lstm | post_covid | 23.823 | 56.439 | 19.208 | 0.480 | 100.000 |
| seasonal_naive | post_covid | 33.317 | 75.213 | 26.636 | 0.721 | 100.000 |
| gat | post_covid | 34.957 | 57.654 | 28.745 | -0.039 | 61.538 |

### Off-season (Oct–Mar), 27 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.522 | 25.978 | 6.147 | 0.835 | 100.000 |
| persistence | post_covid | 8.113 | 24.309 | 6.215 | 0.821 | 96.296 |
| lstm | post_covid | 8.413 | 34.415 | 6.783 | 0.776 | 100.000 |
| arima | post_covid | 8.453 | 32.199 | 6.884 | 0.808 | 100.000 |
| xgboost | post_covid | 9.286 | 27.318 | 6.751 | 0.780 | 100.000 |
| seasonal_naive | post_covid | 10.312 | 50.882 | 8.755 | 0.650 | 100.000 |
| dualtopo | post_covid | 10.334 | 34.763 | 7.387 | 0.609 | 96.296 |
| xgboost_nodemo | post_covid | 11.833 | 36.725 | 8.496 | 0.769 | 100.000 |
| gat | post_covid | 13.462 | 47.589 | 11.409 | 0.222 | 96.296 |

## SAN MIGUEL

*mean observed 38.1, peak 93.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 8.742 | 22.512 | 6.174 | 0.938 | 96.226 |
| gnn_st | post_covid | 9.804 | 23.881 | 6.621 | 0.934 | 98.113 |
| xgboost_nodemo | post_covid | 13.460 | 38.071 | 10.687 | 0.842 | 100.000 |
| arima | post_covid | 15.304 | 44.786 | 11.968 | 0.917 | 98.113 |
| xgboost | post_covid | 16.259 | 37.897 | 11.917 | 0.785 | 100.000 |
| lstm | post_covid | 18.454 | 47.185 | 13.477 | 0.889 | 100.000 |
| gat | post_covid | 19.758 | 48.580 | 15.468 | 0.863 | 90.566 |
| dualtopo | post_covid | 20.033 | 51.428 | 15.185 | 0.848 | 77.358 |
| seasonal_naive | post_covid | 26.908 | 60.244 | 19.371 | 0.183 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 53.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 10.572 | 14.460 | 7.135 | 0.887 | 96.154 |
| gnn_st | post_covid | 12.639 | 15.608 | 8.501 | 0.868 | 96.154 |
| xgboost_nodemo | post_covid | 16.604 | 28.126 | 13.986 | 0.694 | 100.000 |
| arima | post_covid | 19.205 | 24.388 | 14.929 | 0.865 | 96.154 |
| xgboost | post_covid | 21.737 | 29.003 | 17.299 | 0.517 | 100.000 |
| lstm | post_covid | 23.452 | 25.161 | 16.818 | 0.762 | 100.000 |
| dualtopo | post_covid | 24.594 | 28.546 | 18.697 | 0.775 | 61.538 |
| gat | post_covid | 24.905 | 33.929 | 20.614 | 0.812 | 80.769 |
| seasonal_naive | post_covid | 33.796 | 39.406 | 24.995 | -0.320 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 23.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.904 | 31.848 | 4.811 | 0.937 | 100.000 |
| persistence | post_covid | 6.510 | 30.266 | 5.249 | 0.928 | 96.296 |
| xgboost | post_covid | 7.996 | 46.461 | 6.734 | 0.901 | 100.000 |
| xgboost_nodemo | post_covid | 9.494 | 47.647 | 7.511 | 0.883 | 100.000 |
| arima | post_covid | 10.227 | 64.429 | 9.117 | 0.886 | 100.000 |
| lstm | post_covid | 11.785 | 68.394 | 10.259 | 0.928 | 100.000 |
| gat | post_covid | 12.999 | 62.688 | 10.513 | 0.822 | 100.000 |
| dualtopo | post_covid | 14.331 | 73.463 | 11.803 | 0.740 | 92.593 |
| seasonal_naive | post_covid | 17.927 | 80.311 | 13.955 | -0.152 | 100.000 |

## MALVINAS ARGENTINAS

*mean observed 25.7, peak 137.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 25.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 21.307 | 92.069 | 10.308 | 0.840 | 88.679 |
| persistence | post_covid | 21.912 | 108.854 | 10.503 | 0.839 | 90.566 |
| arima | post_covid | 25.325 | 136.287 | 13.187 | 0.763 | 86.792 |
| dualtopo | post_covid | 33.240 | 99.908 | 19.226 | 0.782 | 33.962 |
| xgboost_nodemo | post_covid | 34.276 | 295.393 | 23.636 | 0.463 | 86.792 |
| xgboost | post_covid | 36.502 | 166.616 | 21.189 | 0.414 | 98.113 |
| gat | post_covid | 36.597 | 85.460 | 18.563 | 0.661 | 75.472 |
| seasonal_naive | post_covid | 41.056 | 95.301 | 20.161 | 0.389 | 84.906 |
| lstm | post_covid | 42.092 | 81.725 | 20.347 | 0.441 | 83.019 |

### Flu season (Apr–Sep), 26 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 30.180 | 58.855 | 18.149 | 0.781 | 80.769 |
| persistence | post_covid | 30.968 | 66.627 | 18.064 | 0.781 | 88.462 |
| arima | post_covid | 35.973 | 117.663 | 23.986 | 0.658 | 73.077 |
| xgboost_nodemo | post_covid | 46.704 | 133.104 | 37.326 | 0.239 | 73.077 |
| dualtopo | post_covid | 47.049 | 81.774 | 34.497 | 0.719 | 19.231 |
| xgboost | post_covid | 51.510 | 100.715 | 37.142 | 0.133 | 96.154 |
| gat | post_covid | 52.073 | 69.105 | 34.736 | 0.492 | 65.385 |
| seasonal_naive | post_covid | 58.446 | 69.056 | 37.784 | 0.115 | 69.231 |
| lstm | post_covid | 59.964 | 61.154 | 38.544 | -0.017 | 65.385 |

### Off-season (Oct–Mar), 27 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3.576 | 154.222 | 2.788 | 0.692 | 100.000 |
| gnn_st | post_covid | 3.747 | 124.053 | 2.757 | 0.600 | 96.296 |
| lstm | post_covid | 3.927 | 101.533 | 2.824 | 0.732 | 100.000 |
| gat | post_covid | 4.232 | 101.208 | 2.988 | 0.528 | 85.185 |
| persistence | post_covid | 4.359 | 149.516 | 3.221 | 0.580 | 92.593 |
| seasonal_naive | post_covid | 4.395 | 120.575 | 3.190 | 0.437 | 100.000 |
| dualtopo | post_covid | 6.111 | 117.370 | 4.520 | 0.042 | 48.148 |
| xgboost | post_covid | 7.777 | 230.076 | 5.826 | 0.563 | 100.000 |
| xgboost_nodemo | post_covid | 14.341 | 451.672 | 10.454 | 0.556 | 100.000 |

## LA MATANZA

*mean observed 23.5, peak 53.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 23.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.583 | 16.300 | 3.940 | 0.910 | 100.000 |
| persistence | post_covid | 5.857 | 17.982 | 4.070 | 0.888 | 100.000 |
| arima | post_covid | 5.989 | 17.402 | 4.025 | 0.879 | 98.113 |
| xgboost | post_covid | 8.543 | 29.681 | 6.753 | 0.831 | 100.000 |
| gat | post_covid | 10.062 | 31.778 | 7.807 | 0.861 | 98.113 |
| seasonal_naive | post_covid | 11.545 | 48.375 | 9.945 | 0.754 | 100.000 |
| xgboost_nodemo | post_covid | 12.079 | 38.743 | 8.501 | 0.794 | 100.000 |
| lstm | post_covid | 12.892 | 45.253 | 10.797 | 0.849 | 100.000 |
| dualtopo | post_covid | 13.184 | 49.322 | 11.223 | 0.858 | 64.151 |

### Flu season (Apr–Sep), 26 weeks scored, mean 33.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.246 | 16.130 | 5.509 | 0.773 | 100.000 |
| persistence | post_covid | 7.537 | 18.225 | 5.751 | 0.734 | 100.000 |
| arima | post_covid | 7.712 | 16.784 | 5.616 | 0.724 | 96.154 |
| xgboost | post_covid | 9.820 | 27.661 | 8.357 | 0.701 | 100.000 |
| seasonal_naive | post_covid | 13.062 | 37.986 | 11.282 | 0.559 | 100.000 |
| gat | post_covid | 13.113 | 29.776 | 10.884 | 0.665 | 96.154 |
| xgboost_nodemo | post_covid | 15.697 | 40.536 | 12.363 | 0.614 | 100.000 |
| lstm | post_covid | 16.049 | 39.442 | 14.101 | 0.687 | 100.000 |
| dualtopo | post_covid | 16.213 | 39.981 | 14.121 | 0.664 | 65.385 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.260 | 16.463 | 2.429 | 0.772 | 100.000 |
| persistence | post_covid | 3.553 | 17.747 | 2.452 | 0.673 | 100.000 |
| arima | post_covid | 3.622 | 17.997 | 2.492 | 0.659 | 100.000 |
| gat | post_covid | 5.760 | 33.707 | 4.844 | 0.675 | 100.000 |
| xgboost_nodemo | post_covid | 7.008 | 37.017 | 4.782 | 0.092 | 100.000 |
| xgboost | post_covid | 7.098 | 31.627 | 5.208 | -0.042 | 100.000 |
| lstm | post_covid | 8.844 | 50.849 | 7.614 | 0.234 | 100.000 |
| dualtopo | post_covid | 9.383 | 58.316 | 8.432 | 0.453 | 62.963 |
| seasonal_naive | post_covid | 9.866 | 58.379 | 8.658 | -0.021 | 100.000 |

## QUILMES

*mean observed 21.4, peak 39.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.333 | 20.117 | 3.771 | 0.852 | 98.113 |
| arima | post_covid | 5.375 | 19.232 | 3.695 | 0.836 | 98.113 |
| persistence | post_covid | 5.596 | 20.523 | 3.944 | 0.827 | 98.113 |
| gat | post_covid | 5.875 | 19.813 | 3.913 | 0.825 | 98.113 |
| xgboost | post_covid | 6.894 | 24.933 | 5.171 | 0.708 | 100.000 |
| xgboost_nodemo | post_covid | 7.131 | 27.940 | 5.489 | 0.757 | 100.000 |
| dualtopo | post_covid | 7.348 | 34.124 | 5.861 | 0.745 | 100.000 |
| lstm | post_covid | 7.491 | 25.052 | 5.768 | 0.774 | 100.000 |
| seasonal_naive | post_covid | 8.571 | 29.645 | 6.536 | 0.630 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 28.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 4.439 | 11.227 | 3.171 | 0.769 | 100.000 |
| arima | post_covid | 5.032 | 15.647 | 4.072 | 0.645 | 100.000 |
| gnn_st | post_covid | 5.274 | 16.467 | 4.073 | 0.654 | 100.000 |
| persistence | post_covid | 5.451 | 16.161 | 4.269 | 0.612 | 100.000 |
| xgboost_nodemo | post_covid | 7.294 | 24.957 | 6.231 | 0.320 | 100.000 |
| xgboost | post_covid | 7.419 | 23.515 | 6.345 | 0.217 | 100.000 |
| dualtopo | post_covid | 8.400 | 25.055 | 6.698 | 0.490 | 100.000 |
| lstm | post_covid | 8.593 | 26.302 | 7.702 | 0.563 | 100.000 |
| seasonal_naive | post_covid | 10.574 | 29.418 | 8.708 | 0.354 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 15.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.389 | 23.631 | 3.480 | 0.732 | 96.296 |
| arima | post_covid | 5.685 | 22.683 | 3.332 | 0.694 | 96.296 |
| persistence | post_covid | 5.731 | 24.724 | 3.631 | 0.708 | 96.296 |
| seasonal_naive | post_covid | 6.042 | 29.864 | 4.444 | 0.623 | 100.000 |
| dualtopo | post_covid | 6.167 | 42.857 | 5.055 | 0.665 | 100.000 |
| lstm | post_covid | 6.248 | 23.849 | 3.907 | 0.589 | 100.000 |
| xgboost | post_covid | 6.347 | 26.300 | 4.041 | 0.631 | 100.000 |
| xgboost_nodemo | post_covid | 6.970 | 30.812 | 4.774 | 0.642 | 100.000 |
| gat | post_covid | 6.984 | 28.080 | 4.626 | 0.513 | 96.296 |

## VICENTE LÓPEZ

*mean observed 21.4, peak 114.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 15.720 | 56.377 | 9.946 | 0.728 | 92.453 |
| gnn_st | post_covid | 15.964 | 79.630 | 10.733 | 0.790 | 94.340 |
| arima | post_covid | 17.942 | 111.307 | 13.726 | 0.680 | 90.566 |
| xgboost | post_covid | 24.879 | 149.156 | 18.800 | 0.715 | 100.000 |
| xgboost_nodemo | post_covid | 26.904 | 173.717 | 21.651 | 0.729 | 98.113 |
| gat | post_covid | 29.865 | 200.915 | 23.608 | 0.576 | 84.906 |
| dualtopo | post_covid | 39.223 | 324.554 | 33.590 | 0.349 | 54.717 |
| lstm | post_covid | 47.888 | 334.399 | 41.435 | 0.590 | 92.453 |
| seasonal_naive | post_covid | 56.458 | 318.031 | 41.996 | 0.690 | 84.906 |

### Flu season (Apr–Sep), 26 weeks scored, mean 32.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 21.411 | 62.627 | 14.729 | 0.643 | 92.308 |
| gnn_st | post_covid | 21.564 | 94.242 | 15.984 | 0.714 | 88.462 |
| arima | post_covid | 21.707 | 86.721 | 15.925 | 0.618 | 80.769 |
| dualtopo | post_covid | 31.477 | 178.452 | 27.049 | 0.526 | 61.538 |
| xgboost | post_covid | 33.074 | 202.389 | 28.848 | 0.642 | 100.000 |
| xgboost_nodemo | post_covid | 35.218 | 220.230 | 32.004 | 0.677 | 96.154 |
| gat | post_covid | 36.500 | 200.250 | 28.595 | 0.397 | 73.077 |
| lstm | post_covid | 62.346 | 396.023 | 58.105 | 0.369 | 84.615 |
| seasonal_naive | post_covid | 74.772 | 366.496 | 60.714 | 0.622 | 69.231 |

### Off-season (Oct–Mar), 27 weeks scored, mean 11.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 6.605 | 50.128 | 5.340 | 0.447 | 92.593 |
| gnn_st | post_covid | 7.244 | 65.018 | 5.675 | 0.643 | 100.000 |
| xgboost | post_covid | 12.713 | 95.922 | 9.123 | 0.472 | 100.000 |
| arima | post_covid | 13.349 | 135.893 | 11.609 | 0.252 | 100.000 |
| xgboost_nodemo | post_covid | 15.048 | 127.204 | 11.681 | 0.514 | 100.000 |
| gat | post_covid | 21.631 | 201.580 | 18.805 | 0.737 | 96.296 |
| lstm | post_covid | 27.543 | 272.774 | 25.382 | 0.513 | 100.000 |
| seasonal_naive | post_covid | 29.549 | 269.567 | 23.971 | 0.291 | 100.000 |
| dualtopo | post_covid | 45.452 | 470.656 | 39.889 | 0.095 | 48.148 |

## ALMIRANTE BROWN

*mean observed 19.6, peak 41.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.532 | 29.093 | 3.823 | 0.833 | 98.113 |
| persistence | post_covid | 5.580 | 29.674 | 4.039 | 0.807 | 98.113 |
| arima | post_covid | 6.140 | 55.838 | 5.170 | 0.773 | 100.000 |
| gat | post_covid | 6.250 | 48.172 | 5.022 | 0.742 | 100.000 |
| dualtopo | post_covid | 6.577 | 55.084 | 5.269 | 0.748 | 100.000 |
| lstm | post_covid | 9.085 | 50.471 | 7.878 | 0.732 | 100.000 |
| xgboost | post_covid | 10.236 | 50.394 | 8.299 | 0.732 | 100.000 |
| xgboost_nodemo | post_covid | 11.987 | 53.496 | 9.356 | 0.689 | 100.000 |
| seasonal_naive | post_covid | 13.236 | 61.022 | 10.627 | 0.690 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 25.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 5.360 | 18.663 | 4.452 | 0.644 | 100.000 |
| gat | post_covid | 5.566 | 17.938 | 4.115 | 0.634 | 100.000 |
| persistence | post_covid | 5.894 | 18.867 | 4.354 | 0.641 | 100.000 |
| gnn_st | post_covid | 5.985 | 18.830 | 4.035 | 0.683 | 100.000 |
| dualtopo | post_covid | 6.229 | 21.847 | 4.971 | 0.681 | 100.000 |
| lstm | post_covid | 9.932 | 39.758 | 8.690 | 0.585 | 100.000 |
| xgboost | post_covid | 12.650 | 48.298 | 11.237 | 0.468 | 100.000 |
| xgboost_nodemo | post_covid | 15.186 | 53.653 | 12.709 | 0.385 | 100.000 |
| seasonal_naive | post_covid | 16.082 | 51.663 | 12.857 | 0.576 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.057 | 38.975 | 3.618 | 0.707 | 96.296 |
| persistence | post_covid | 5.260 | 40.081 | 3.736 | 0.701 | 96.296 |
| arima | post_covid | 6.807 | 91.636 | 5.862 | 0.676 | 100.000 |
| gat | post_covid | 6.845 | 77.286 | 5.895 | 0.374 | 100.000 |
| dualtopo | post_covid | 6.895 | 87.089 | 5.556 | 0.287 | 100.000 |
| xgboost | post_covid | 7.181 | 52.412 | 5.470 | 0.524 | 100.000 |
| xgboost_nodemo | post_covid | 7.744 | 53.346 | 6.129 | 0.590 | 100.000 |
| lstm | post_covid | 8.187 | 60.787 | 7.095 | 0.405 | 100.000 |
| seasonal_naive | post_covid | 9.737 | 70.034 | 8.480 | 0.258 | 100.000 |

## MORÓN

*mean observed 19.1, peak 54.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.517 | 26.797 | 4.424 | 0.849 | 100.000 |
| lstm | post_covid | 6.313 | 27.787 | 5.034 | 0.841 | 100.000 |
| gat | post_covid | 6.582 | 32.111 | 4.988 | 0.824 | 100.000 |
| arima | post_covid | 6.820 | 36.845 | 5.455 | 0.759 | 100.000 |
| persistence | post_covid | 6.910 | 33.480 | 5.560 | 0.777 | 100.000 |
| xgboost | post_covid | 7.895 | 39.650 | 6.213 | 0.714 | 100.000 |
| xgboost_nodemo | post_covid | 8.710 | 46.201 | 6.634 | 0.759 | 100.000 |
| dualtopo | post_covid | 9.358 | 46.326 | 7.719 | 0.679 | 88.679 |
| seasonal_naive | post_covid | 14.587 | 51.899 | 9.691 | 0.720 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.534 | 22.342 | 5.399 | 0.735 | 100.000 |
| gat | post_covid | 7.099 | 25.812 | 5.285 | 0.746 | 100.000 |
| lstm | post_covid | 7.520 | 27.649 | 6.612 | 0.747 | 100.000 |
| arima | post_covid | 7.845 | 25.622 | 6.408 | 0.584 | 100.000 |
| persistence | post_covid | 8.281 | 28.862 | 7.096 | 0.606 | 100.000 |
| xgboost | post_covid | 9.074 | 26.087 | 6.800 | 0.696 | 100.000 |
| xgboost_nodemo | post_covid | 9.702 | 28.300 | 6.786 | 0.690 | 100.000 |
| dualtopo | post_covid | 10.703 | 39.224 | 8.869 | 0.278 | 96.154 |
| seasonal_naive | post_covid | 19.405 | 51.883 | 13.785 | 0.616 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.317 | 31.087 | 3.484 | 0.539 | 100.000 |
| lstm | post_covid | 4.877 | 27.921 | 3.514 | 0.462 | 100.000 |
| persistence | post_covid | 5.263 | 37.927 | 4.082 | 0.492 | 100.000 |
| arima | post_covid | 5.661 | 47.651 | 4.537 | 0.468 | 100.000 |
| gat | post_covid | 6.042 | 38.176 | 4.703 | 0.346 | 100.000 |
| xgboost | post_covid | 6.562 | 52.711 | 5.648 | 0.200 | 100.000 |
| seasonal_naive | post_covid | 7.424 | 51.915 | 5.748 | 0.031 | 100.000 |
| xgboost_nodemo | post_covid | 7.634 | 63.438 | 6.487 | 0.337 | 100.000 |
| dualtopo | post_covid | 7.848 | 53.165 | 6.611 | 0.266 | 81.481 |

## MERLO

*mean observed 17.9, peak 60.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 17.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.665 | 62.440 | 7.062 | 0.832 | 98.113 |
| persistence | post_covid | 8.867 | 44.671 | 6.511 | 0.797 | 94.340 |
| arima | post_covid | 9.437 | 86.985 | 7.818 | 0.810 | 98.113 |
| lstm | post_covid | 15.432 | 134.028 | 13.688 | 0.818 | 100.000 |
| xgboost_nodemo | post_covid | 16.705 | 79.943 | 11.123 | 0.794 | 100.000 |
| xgboost | post_covid | 19.601 | 101.931 | 13.587 | 0.790 | 100.000 |
| dualtopo | post_covid | 22.198 | 117.869 | 17.096 | 0.788 | 83.019 |
| seasonal_naive | post_covid | 26.507 | 241.783 | 20.679 | 0.234 | 100.000 |
| gat | post_covid | 36.442 | 256.720 | 30.842 | 0.681 | 81.132 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 9.991 | 34.223 | 7.555 | 0.712 | 96.154 |
| gnn_st | post_covid | 10.470 | 44.092 | 8.879 | 0.757 | 100.000 |
| persistence | post_covid | 11.012 | 28.027 | 8.128 | 0.699 | 96.154 |
| lstm | post_covid | 17.915 | 96.167 | 16.305 | 0.740 | 100.000 |
| xgboost_nodemo | post_covid | 22.951 | 71.002 | 16.951 | 0.673 | 100.000 |
| xgboost | post_covid | 26.807 | 90.266 | 20.455 | 0.663 | 100.000 |
| dualtopo | post_covid | 30.025 | 112.847 | 26.039 | 0.715 | 80.769 |
| seasonal_naive | post_covid | 30.963 | 164.549 | 23.282 | -0.168 | 100.000 |
| gat | post_covid | 47.360 | 240.007 | 44.378 | 0.456 | 61.538 |

### Off-season (Oct–Mar), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 6.128 | 61.315 | 4.953 | 0.557 | 92.593 |
| xgboost_nodemo | post_covid | 6.367 | 88.884 | 5.511 | 0.652 | 100.000 |
| gnn_st | post_covid | 6.467 | 80.789 | 5.312 | 0.411 | 96.296 |
| xgboost | post_covid | 7.886 | 113.595 | 6.973 | 0.602 | 100.000 |
| arima | post_covid | 8.870 | 139.747 | 8.071 | 0.572 | 100.000 |
| dualtopo | post_covid | 9.958 | 122.891 | 8.483 | -0.135 | 85.185 |
| lstm | post_covid | 12.585 | 171.888 | 11.168 | 0.613 | 100.000 |
| gat | post_covid | 21.141 | 273.432 | 17.807 | 0.152 | 100.000 |
| seasonal_naive | post_covid | 21.355 | 319.017 | 18.172 | -0.181 | 100.000 |

## TIGRE

*mean observed 8.0, peak 40.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 8.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 3.784 | 46.927 | 2.246 | 0.935 | 100.000 |
| arima | post_covid | 4.307 | 49.921 | 2.447 | 0.916 | 94.340 |
| gnn_st | post_covid | 4.374 | 78.744 | 2.808 | 0.926 | 100.000 |
| dualtopo | post_covid | 5.715 | 231.786 | 4.697 | 0.877 | 100.000 |
| xgboost | post_covid | 7.022 | 187.836 | 5.496 | 0.783 | 98.113 |
| xgboost_nodemo | post_covid | 7.122 | 226.185 | 5.901 | 0.890 | 100.000 |
| lstm | post_covid | 7.996 | 187.696 | 6.314 | 0.707 | 100.000 |
| gat | post_covid | 9.741 | 84.651 | 5.795 | 0.646 | 41.509 |
| seasonal_naive | post_covid | 10.366 | 102.643 | 5.902 | 0.332 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 5.233 | 34.552 | 3.683 | 0.906 | 100.000 |
| arima | post_covid | 5.842 | 40.452 | 3.934 | 0.885 | 96.154 |
| gnn_st | post_covid | 5.981 | 65.066 | 4.388 | 0.898 | 100.000 |
| dualtopo | post_covid | 6.181 | 89.382 | 5.265 | 0.874 | 100.000 |
| xgboost_nodemo | post_covid | 8.771 | 116.925 | 7.224 | 0.848 | 100.000 |
| xgboost | post_covid | 9.098 | 88.804 | 7.200 | 0.698 | 96.154 |
| lstm | post_covid | 10.552 | 139.456 | 9.218 | 0.695 | 100.000 |
| gat | post_covid | 13.787 | 83.700 | 10.210 | 0.567 | 42.308 |
| seasonal_naive | post_covid | 14.669 | 100.571 | 10.464 | -0.031 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 1.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 1.317 | 58.843 | 0.862 | 0.423 | 100.000 |
| gnn_st | post_covid | 1.765 | 91.915 | 1.287 | 0.466 | 100.000 |
| gat | post_covid | 1.793 | 85.568 | 1.543 | 0.458 | 40.741 |
| arima | post_covid | 1.886 | 59.039 | 1.015 | 0.431 | 92.593 |
| seasonal_naive | post_covid | 1.935 | 104.638 | 1.508 | -0.101 | 100.000 |
| xgboost | post_covid | 4.135 | 283.201 | 3.855 | 0.284 | 100.000 |
| lstm | post_covid | 4.275 | 234.150 | 3.518 | 0.463 | 100.000 |
| xgboost_nodemo | post_covid | 5.050 | 331.398 | 4.627 | 0.296 | 100.000 |
| dualtopo | post_covid | 5.227 | 368.916 | 4.149 | -0.460 | 100.000 |

## SAN ISIDRO

*mean observed 5.0, peak 29.9 per 100,000 over the full year*

### Overall (full year), 50 weeks scored, mean 5.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.459 | 398.184 | 3.848 | 0.699 | 98.000 |
| persistence | post_covid | 5.659 | 194.558 | 3.202 | 0.670 | 84.000 |
| arima | post_covid | 5.801 | 256.489 | 3.730 | 0.592 | 90.000 |
| gat | post_covid | 6.298 | 425.870 | 4.643 | 0.549 | 98.000 |
| xgboost | post_covid | 7.489 | 437.806 | 5.682 | 0.466 | 74.000 |
| xgboost_nodemo | post_covid | 7.983 | 521.701 | 5.949 | 0.440 | 100.000 |
| lstm | post_covid | 9.053 | 819.248 | 7.626 | 0.427 | 100.000 |
| seasonal_naive | post_covid | 9.932 | 391.779 | 5.792 | 0.441 | 100.000 |
| dualtopo | post_covid | 11.886 | 1148.189 | 10.980 | 0.547 | 98.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 2.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 3.508 | 161.575 | 2.174 | 0.201 | 100.000 |
| xgboost | post_covid | 6.405 | 505.127 | 4.720 | -0.175 | 80.769 |
| arima | post_covid | 6.759 | 394.296 | 4.115 | -0.100 | 88.462 |
| gnn_st | post_covid | 6.790 | 593.209 | 4.783 | 0.002 | 96.154 |
| persistence | post_covid | 6.900 | 265.520 | 3.687 | 0.059 | 76.923 |
| xgboost_nodemo | post_covid | 6.907 | 620.422 | 4.917 | -0.261 | 100.000 |
| gat | post_covid | 7.143 | 469.140 | 4.502 | 0.039 | 96.154 |
| lstm | post_covid | 9.350 | 936.923 | 7.377 | -0.428 | 100.000 |
| dualtopo | post_covid | 12.974 | 1404.347 | 12.087 | 0.147 | 96.154 |

### Off-season (Oct–Mar), 24 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.484 | 211.639 | 2.835 | 0.931 | 100.000 |
| persistence | post_covid | 3.890 | 126.680 | 2.677 | 0.911 | 91.667 |
| arima | post_covid | 4.540 | 124.674 | 3.312 | 0.927 | 91.667 |
| gat | post_covid | 5.230 | 384.481 | 4.796 | 0.863 | 100.000 |
| xgboost | post_covid | 8.508 | 373.413 | 6.725 | 0.542 | 66.667 |
| lstm | post_covid | 8.719 | 706.689 | 7.896 | 0.855 | 100.000 |
| xgboost_nodemo | post_covid | 9.006 | 427.272 | 7.067 | 0.518 | 100.000 |
| dualtopo | post_covid | 10.581 | 903.168 | 9.780 | 0.857 | 100.000 |
| seasonal_naive | post_covid | 13.863 | 611.975 | 9.713 | 0.357 | 100.000 |

## LOMAS DE ZAMORA

*mean observed 0.6, peak 1.6 per 100,000 over the full year*

### Overall (full year), 41 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.624 | 117.941 | 0.509 | 0.008 | 90.244 |
| arima | post_covid | 0.642 | 122.670 | 0.540 | -0.063 | 90.244 |
| gnn_st | post_covid | 1.145 | 321.021 | 0.947 | 0.081 | 100.000 |
| xgboost | post_covid | 2.296 | 316.122 | 1.123 | -0.255 | 24.390 |
| gat | post_covid | 2.559 | 725.591 | 2.382 | -0.058 | 100.000 |
| seasonal_naive | post_covid | 3.278 | 739.566 | 2.317 | -0.099 | 100.000 |
| dualtopo | post_covid | 3.529 | 986.577 | 3.349 | -0.040 | 100.000 |
| lstm | post_covid | 3.576 | 1016.503 | 3.445 | 0.126 | 100.000 |
| xgboost_nodemo | post_covid | 3.660 | 500.556 | 1.587 | -0.280 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.671 | 125.797 | 0.546 | 0.018 | 88.462 |
| arima | post_covid | 0.692 | 129.058 | 0.579 | -0.068 | 88.462 |
| gnn_st | post_covid | 1.339 | 399.996 | 1.144 | 0.085 | 100.000 |
| xgboost | post_covid | 2.096 | 407.528 | 1.049 | -0.197 | 19.231 |
| gat | post_covid | 2.904 | 865.039 | 2.797 | -0.228 | 100.000 |
| xgboost_nodemo | post_covid | 3.625 | 732.387 | 1.630 | -0.231 | 100.000 |
| seasonal_naive | post_covid | 3.846 | 994.581 | 2.791 | -0.178 | 100.000 |
| dualtopo | post_covid | 4.016 | 1171.226 | 3.887 | -0.083 | 100.000 |
| lstm | post_covid | 4.046 | 1202.111 | 4.007 | 0.076 | 100.000 |

### Off-season (Oct–Mar), 15 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.531 | 105.034 | 0.444 | -0.022 | 93.333 |
| arima | post_covid | 0.543 | 112.177 | 0.473 | -0.046 | 93.333 |
| gnn_st | post_covid | 0.689 | 191.276 | 0.605 | 0.049 | 100.000 |
| gat | post_covid | 1.813 | 496.497 | 1.662 | 0.080 | 100.000 |
| seasonal_naive | post_covid | 1.928 | 320.612 | 1.497 | 0.183 | 100.000 |
| dualtopo | post_covid | 2.467 | 683.225 | 2.415 | -0.175 | 100.000 |
| lstm | post_covid | 2.567 | 711.574 | 2.469 | 0.320 | 100.000 |
| xgboost | post_covid | 2.606 | 165.956 | 1.250 | -0.365 | 33.333 |
| xgboost_nodemo | post_covid | 3.720 | 119.690 | 1.513 | -0.387 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
