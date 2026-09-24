# Per-neighborhood leaderboard — horizon 4

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Apr–Sep), Off-season (Oct–Mar).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* them -- LOMAS DE ZAMORA has 12 fewer scored weeks than the best-covered node (41 against 53) -- so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

> **MAPE is not usable in this table** (it reaches 8,151,166%). It divides by the observed rate, and this city reports observed zeros and near-zeros rather than suppressing small counts, so the denominator goes to zero. Rank on RMSE or MAE. The column is kept so the two cities' tables have the same shape.

## Summary — neighborhoods won, out of 19

| model | Overall (full year) | Flu season (Apr–Sep) | Off-season (Oct–Mar) |
| --- | --- | --- | --- |
| gnn_st | 8 | 5 | 9 |
| arima | 4 | 4 | 1 |
| dualtopo | 2 | 2 | 1 |
| xgboost | 2 | 3 | 2 |
| gat | 1 | 2 | 0 |
| persistence | 1 | 1 | 3 |
| xgboost_nodemo | 1 | 1 | 1 |
| seasonal_naive | 0 | 1 | 2 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `arima (post_covid)`: J.C.Paz, LaMatanza, LomasZam., V.López; `dualtopo (post_covid)`: AlmBrown, Avellan.; `gat (post_covid)`: Moreno; `gnn_st (post_covid)`: Ezeiza, Lanús, MalvArg., Merlo, Quilmes, S.Isidro, Tigre, TresFeb.; `persistence (post_covid)`: S.Miguel; `xgboost (post_covid)`: F.Varela, S.Martín; `xgboost_nodemo (post_covid)`: Morón
- **Flu season (Apr–Sep)** — `arima (post_covid)`: J.C.Paz, LomasZam., Merlo, V.López; `dualtopo (post_covid)`: AlmBrown, Avellan.; `gat (post_covid)`: LaMatanza, Moreno; `gnn_st (post_covid)`: Ezeiza, MalvArg., Quilmes, Tigre, TresFeb.; `persistence (post_covid)`: S.Miguel; `seasonal_naive (post_covid)`: S.Isidro; `xgboost (post_covid)`: F.Varela, Lanús, S.Martín; `xgboost_nodemo (post_covid)`: Morón
- **Off-season (Oct–Mar)** — `arima (post_covid)`: LaMatanza; `dualtopo (post_covid)`: AlmBrown; `gnn_st (post_covid)`: F.Varela, Lanús, MalvArg., Merlo, Morón, S.Isidro, S.Martín, S.Miguel, TresFeb.; `persistence (post_covid)`: J.C.Paz, LomasZam., V.López; `seasonal_naive (post_covid)`: Quilmes, Tigre; `xgboost (post_covid)`: Ezeiza, Moreno; `xgboost_nodemo (post_covid)`: Avellan.

`gnn_st (post_covid)` wins 8 of 19 neighborhoods. The pooled leaderboard is led by `persistence (post_covid)` instead, and `gnn_st (post_covid)` ranks 3 there. That is not a contradiction: the pooled metric flattens all 14 neighborhoods into one set of cells, so it is dominated by the high-rate ones (Dorchester and Roxbury average roughly five times Fenway's rate). Winning most neighborhoods and winning the pooled error are different achievements, and which one you want depends on whether you are allocating city-wide capacity or advising a specific neighborhood.

## JOSÉ C. PAZ

*mean observed 257.3, peak 740.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 257.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 130.182 | 35.884 | 91.570 | 0.587 | 67.925 |
| persistence | post_covid | 132.011 | 35.158 | 90.337 | 0.588 | 69.811 |
| gnn_st | post_covid | 151.161 | 40.540 | 111.158 | 0.715 | 41.509 |
| gat | post_covid | 166.447 | 64.222 | 136.823 | 0.749 | 24.528 |
| xgboost | post_covid | 213.673 | 74.271 | 187.629 | 0.856 | 3.774 |
| xgboost_nodemo | post_covid | 217.291 | 78.286 | 193.064 | 0.862 | 1.887 |
| seasonal_naive | post_covid | 218.785 | 68.043 | 167.317 | 0.319 | 33.962 |
| lstm | post_covid | 253.406 | 80.220 | 210.760 | 0.254 | 3.774 |
| dualtopo | post_covid | 268.093 | 92.169 | 232.802 | 0.494 | 0.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 362.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 172.786 | 32.056 | 126.730 | 0.114 | 61.538 |
| persistence | post_covid | 175.981 | 32.096 | 126.420 | 0.129 | 61.538 |
| gat | post_covid | 181.676 | 38.815 | 135.676 | 0.487 | 50.000 |
| gnn_st | post_covid | 194.537 | 37.779 | 148.621 | 0.341 | 30.769 |
| xgboost | post_covid | 268.088 | 68.838 | 248.606 | 0.747 | 0.000 |
| xgboost_nodemo | post_covid | 270.117 | 69.805 | 251.241 | 0.751 | 0.000 |
| seasonal_naive | post_covid | 281.790 | 59.246 | 224.270 | -0.208 | 26.923 |
| lstm | post_covid | 333.938 | 79.288 | 298.987 | -0.533 | 0.000 |
| dualtopo | post_covid | 343.821 | 86.917 | 316.928 | 0.034 | 0.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 156.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 66.227 | 38.106 | 55.591 | 0.555 | 77.778 |
| arima | post_covid | 67.214 | 39.569 | 57.713 | 0.545 | 74.074 |
| gnn_st | post_covid | 91.707 | 43.199 | 75.082 | 0.580 | 51.852 |
| seasonal_naive | post_covid | 132.274 | 76.514 | 112.473 | 0.510 | 40.741 |
| lstm | post_covid | 136.624 | 81.117 | 125.801 | 0.645 | 7.407 |
| xgboost | post_covid | 142.871 | 79.502 | 128.910 | 0.343 | 7.407 |
| xgboost_nodemo | post_covid | 149.738 | 86.453 | 137.043 | 0.458 | 3.704 |
| gat | post_covid | 150.330 | 88.688 | 137.927 | 0.372 | 0.000 |
| dualtopo | post_covid | 165.078 | 97.227 | 151.792 | 0.034 | 0.000 |

## AVELLANEDA

*mean observed 143.6, peak 323.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 143.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 30.242 | 15.195 | 22.711 | 0.895 | 100.000 |
| gnn_st | post_covid | 36.650 | 20.710 | 28.746 | 0.793 | 98.113 |
| gat | post_covid | 37.991 | 23.296 | 30.934 | 0.788 | 96.226 |
| xgboost_nodemo | post_covid | 40.436 | 20.351 | 30.246 | 0.831 | 100.000 |
| xgboost | post_covid | 40.902 | 21.275 | 31.635 | 0.828 | 100.000 |
| seasonal_naive | post_covid | 46.153 | 26.007 | 35.405 | 0.858 | 96.226 |
| arima | post_covid | 50.166 | 32.471 | 40.276 | 0.474 | 90.566 |
| lstm | post_covid | 57.473 | 28.997 | 42.386 | 0.390 | 92.453 |
| persistence | post_covid | 57.562 | 31.470 | 43.644 | 0.475 | 84.906 |

### Flu season (Apr–Sep), 26 weeks scored, mean 185.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 33.771 | 14.111 | 27.363 | 0.862 | 100.000 |
| gat | post_covid | 40.876 | 19.127 | 33.228 | 0.617 | 100.000 |
| gnn_st | post_covid | 44.069 | 21.211 | 35.939 | 0.521 | 100.000 |
| xgboost_nodemo | post_covid | 52.102 | 24.707 | 42.727 | 0.626 | 100.000 |
| xgboost | post_covid | 52.180 | 25.346 | 44.059 | 0.612 | 100.000 |
| arima | post_covid | 53.384 | 19.000 | 37.684 | 0.056 | 88.462 |
| seasonal_naive | post_covid | 54.852 | 22.597 | 42.265 | 0.810 | 92.308 |
| persistence | post_covid | 64.642 | 25.250 | 47.371 | 0.043 | 84.615 |
| lstm | post_covid | 70.138 | 27.266 | 51.819 | -0.561 | 88.462 |

### Off-season (Oct–Mar), 27 weeks scored, mean 103.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 24.405 | 16.157 | 18.226 | 0.730 | 100.000 |
| xgboost | post_covid | 25.730 | 17.356 | 19.670 | 0.752 | 100.000 |
| dualtopo | post_covid | 26.401 | 16.239 | 18.231 | 0.495 | 100.000 |
| gnn_st | post_covid | 27.688 | 20.228 | 21.819 | 0.465 | 96.296 |
| gat | post_covid | 34.988 | 27.309 | 28.725 | 0.222 | 92.593 |
| seasonal_naive | post_covid | 35.833 | 29.290 | 28.799 | 0.505 | 100.000 |
| lstm | post_covid | 41.796 | 30.663 | 33.302 | 0.256 | 96.296 |
| arima | post_covid | 46.858 | 45.443 | 42.772 | -0.031 | 92.593 |
| persistence | post_covid | 49.803 | 37.461 | 40.055 | -0.027 | 85.185 |

## EZEIZA

*mean observed 83.5, peak 186.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 83.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 15.088 | 17.639 | 11.220 | 0.938 | 100.000 |
| xgboost | post_covid | 15.499 | 16.079 | 12.392 | 0.937 | 100.000 |
| xgboost_nodemo | post_covid | 16.480 | 18.505 | 13.575 | 0.924 | 100.000 |
| dualtopo | post_covid | 19.266 | 25.104 | 16.795 | 0.912 | 100.000 |
| gat | post_covid | 23.976 | 31.260 | 19.817 | 0.947 | 100.000 |
| persistence | post_covid | 27.815 | 30.666 | 21.226 | 0.784 | 98.113 |
| seasonal_naive | post_covid | 28.077 | 28.828 | 21.442 | 0.782 | 100.000 |
| lstm | post_covid | 41.553 | 42.183 | 31.563 | 0.340 | 90.566 |
| arima | post_covid | 42.254 | 63.146 | 37.078 |  | 84.906 |

### Flu season (Apr–Sep), 26 weeks scored, mean 119.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.784 | 8.867 | 10.855 | 0.884 | 100.000 |
| xgboost | post_covid | 19.354 | 13.112 | 16.270 | 0.802 | 100.000 |
| xgboost_nodemo | post_covid | 19.513 | 13.339 | 16.709 | 0.794 | 100.000 |
| dualtopo | post_covid | 22.855 | 18.129 | 20.850 | 0.899 | 100.000 |
| gat | post_covid | 28.724 | 19.459 | 23.755 | 0.893 | 100.000 |
| persistence | post_covid | 29.253 | 18.308 | 22.866 | 0.534 | 96.154 |
| seasonal_naive | post_covid | 35.148 | 23.853 | 28.668 | 0.633 | 100.000 |
| arima | post_covid | 44.551 | 28.192 | 37.047 |  | 80.769 |
| lstm | post_covid | 54.088 | 33.609 | 44.144 | -0.571 | 80.769 |

### Off-season (Oct–Mar), 27 weeks scored, mean 48.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 10.527 | 18.937 | 8.659 | 0.808 | 100.000 |
| xgboost_nodemo | post_covid | 12.902 | 23.479 | 10.557 | 0.712 | 100.000 |
| dualtopo | post_covid | 15.020 | 31.820 | 12.889 | 0.767 | 100.000 |
| gnn_st | post_covid | 15.375 | 26.087 | 11.572 | 0.690 | 100.000 |
| gat | post_covid | 18.274 | 42.623 | 16.024 | 0.776 | 100.000 |
| seasonal_naive | post_covid | 18.915 | 33.620 | 14.483 | 0.600 | 100.000 |
| lstm | post_covid | 23.919 | 50.439 | 19.448 | 0.213 | 100.000 |
| persistence | post_covid | 26.356 | 42.567 | 19.648 | 0.466 | 100.000 |
| arima | post_covid | 39.918 | 96.806 | 37.109 |  | 88.889 |

## MORENO

*mean observed 74.1, peak 197.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 74.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 25.520 | 35.265 | 20.734 | 0.905 | 98.113 |
| arima | post_covid | 30.497 | 53.279 | 23.467 | 0.784 | 92.453 |
| persistence | post_covid | 31.622 | 44.665 | 23.127 | 0.787 | 86.792 |
| lstm | post_covid | 33.772 | 43.199 | 24.439 | 0.730 | 96.226 |
| gnn_st | post_covid | 34.094 | 35.272 | 23.619 | 0.788 | 92.453 |
| xgboost | post_covid | 38.623 | 47.939 | 28.543 | 0.672 | 96.226 |
| seasonal_naive | post_covid | 41.066 | 62.099 | 32.407 | 0.593 | 98.113 |
| dualtopo | post_covid | 41.388 | 49.362 | 34.188 | 0.884 | 84.906 |
| xgboost_nodemo | post_covid | 41.930 | 45.320 | 31.123 | 0.625 | 92.453 |

### Flu season (Apr–Sep), 26 weeks scored, mean 112.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 30.857 | 25.536 | 25.912 | 0.774 | 96.154 |
| arima | post_covid | 39.513 | 27.336 | 32.239 | 0.492 | 88.462 |
| persistence | post_covid | 40.965 | 29.449 | 32.356 | 0.519 | 84.615 |
| lstm | post_covid | 44.059 | 27.716 | 33.680 | 0.197 | 92.308 |
| gnn_st | post_covid | 45.431 | 26.580 | 33.883 | 0.227 | 88.462 |
| dualtopo | post_covid | 52.805 | 42.724 | 48.173 | 0.826 | 76.923 |
| xgboost | post_covid | 53.235 | 37.974 | 44.829 | 0.137 | 92.308 |
| seasonal_naive | post_covid | 54.343 | 39.429 | 45.983 | 0.241 | 96.154 |
| xgboost_nodemo | post_covid | 57.559 | 41.319 | 49.386 | 0.066 | 84.615 |

### Off-season (Oct–Mar), 27 weeks scored, mean 37.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 14.112 | 57.534 | 12.860 | 0.767 | 100.000 |
| xgboost_nodemo | post_covid | 16.148 | 49.172 | 13.537 | 0.760 | 100.000 |
| gnn_st | post_covid | 17.151 | 43.642 | 13.735 | 0.800 | 96.296 |
| arima | post_covid | 17.950 | 78.262 | 15.021 | 0.720 | 96.296 |
| persistence | post_covid | 18.625 | 59.317 | 14.240 | 0.754 | 88.889 |
| gat | post_covid | 19.013 | 44.635 | 15.747 | 0.860 | 100.000 |
| lstm | post_covid | 19.225 | 58.108 | 15.541 | 0.852 | 100.000 |
| seasonal_naive | post_covid | 21.601 | 83.929 | 19.333 | 0.462 | 100.000 |
| dualtopo | post_covid | 26.025 | 55.754 | 20.721 | 0.201 | 92.593 |

## LANÚS

*mean observed 70.6, peak 171.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 70.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 16.122 | 19.187 | 12.335 | 0.895 | 100.000 |
| xgboost | post_covid | 16.721 | 19.148 | 12.679 | 0.911 | 100.000 |
| xgboost_nodemo | post_covid | 17.287 | 19.470 | 13.128 | 0.902 | 100.000 |
| dualtopo | post_covid | 19.387 | 28.577 | 14.699 | 0.850 | 100.000 |
| gat | post_covid | 20.016 | 31.937 | 16.583 | 0.854 | 100.000 |
| seasonal_naive | post_covid | 23.021 | 22.954 | 16.624 | 0.820 | 100.000 |
| persistence | post_covid | 28.701 | 30.608 | 21.577 | 0.689 | 94.340 |
| arima | post_covid | 30.868 | 34.894 | 23.810 | 0.675 | 86.792 |
| lstm | post_covid | 33.565 | 30.832 | 23.708 | 0.449 | 94.340 |

### Flu season (Apr–Sep), 26 weeks scored, mean 98.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 17.798 | 14.231 | 13.792 | 0.833 | 100.000 |
| xgboost_nodemo | post_covid | 18.028 | 14.504 | 14.170 | 0.820 | 100.000 |
| gnn_st | post_covid | 18.436 | 14.184 | 13.888 | 0.770 | 100.000 |
| dualtopo | post_covid | 21.477 | 15.893 | 16.580 | 0.708 | 100.000 |
| gat | post_covid | 22.772 | 21.135 | 19.564 | 0.665 | 100.000 |
| seasonal_naive | post_covid | 28.794 | 22.776 | 23.214 | 0.719 | 100.000 |
| persistence | post_covid | 36.318 | 28.589 | 28.608 | 0.293 | 92.308 |
| arima | post_covid | 38.423 | 31.370 | 30.806 | 0.313 | 88.462 |
| lstm | post_covid | 44.746 | 32.164 | 34.398 | -0.453 | 88.462 |

### Off-season (Oct–Mar), 27 weeks scored, mean 43.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.525 | 24.004 | 10.839 | 0.743 | 100.000 |
| seasonal_naive | post_covid | 15.553 | 23.126 | 10.278 | 0.468 | 100.000 |
| xgboost | post_covid | 15.613 | 23.883 | 11.608 | 0.776 | 100.000 |
| xgboost_nodemo | post_covid | 16.542 | 24.251 | 12.125 | 0.767 | 100.000 |
| lstm | post_covid | 16.838 | 29.549 | 13.414 | 0.685 | 100.000 |
| gat | post_covid | 16.943 | 42.339 | 13.714 | 0.468 | 100.000 |
| dualtopo | post_covid | 17.134 | 40.791 | 12.887 | 0.506 | 100.000 |
| persistence | post_covid | 18.624 | 32.552 | 14.806 | 0.551 | 96.296 |
| arima | post_covid | 21.182 | 38.288 | 17.072 | 0.535 | 85.185 |

## FLORENCIO VARELA

*mean observed 53.7, peak 146.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 53.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 14.026 | 22.660 | 10.699 | 0.889 | 100.000 |
| gnn_st | post_covid | 15.411 | 18.117 | 10.661 | 0.886 | 100.000 |
| xgboost_nodemo | post_covid | 15.707 | 22.492 | 12.053 | 0.876 | 100.000 |
| dualtopo | post_covid | 20.366 | 28.958 | 15.758 | 0.777 | 100.000 |
| gat | post_covid | 21.124 | 29.944 | 15.657 | 0.757 | 98.113 |
| seasonal_naive | post_covid | 21.981 | 32.443 | 17.099 | 0.811 | 100.000 |
| persistence | post_covid | 24.814 | 28.398 | 15.917 | 0.667 | 92.453 |
| lstm | post_covid | 28.906 | 28.494 | 18.214 | 0.540 | 96.226 |
| arima | post_covid | 31.217 | 53.718 | 23.846 |  | 83.019 |

### Flu season (Apr–Sep), 26 weeks scored, mean 76.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 17.392 | 19.057 | 13.752 | 0.769 | 100.000 |
| xgboost_nodemo | post_covid | 18.494 | 19.748 | 14.874 | 0.742 | 100.000 |
| gnn_st | post_covid | 20.331 | 19.182 | 15.533 | 0.728 | 100.000 |
| dualtopo | post_covid | 26.978 | 30.775 | 23.274 | 0.534 | 100.000 |
| seasonal_naive | post_covid | 28.006 | 30.369 | 22.886 | 0.603 | 100.000 |
| gat | post_covid | 28.346 | 29.119 | 23.118 | 0.350 | 96.154 |
| persistence | post_covid | 33.514 | 29.489 | 23.297 | 0.316 | 88.462 |
| lstm | post_covid | 39.822 | 32.531 | 28.791 | -0.435 | 92.308 |
| arima | post_covid | 40.221 | 36.318 | 31.751 |  | 65.385 |

### Off-season (Oct–Mar), 27 weeks scored, mean 32.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.258 | 17.091 | 5.969 | 0.841 | 100.000 |
| xgboost | post_covid | 9.742 | 26.131 | 7.759 | 0.654 | 100.000 |
| gat | post_covid | 10.108 | 30.738 | 8.473 | 0.629 | 100.000 |
| lstm | post_covid | 10.635 | 24.607 | 8.028 | 0.799 | 100.000 |
| dualtopo | post_covid | 10.645 | 27.209 | 8.521 | 0.656 | 100.000 |
| persistence | post_covid | 11.271 | 27.348 | 8.811 | 0.755 | 96.296 |
| xgboost_nodemo | post_covid | 12.448 | 25.135 | 9.336 | 0.659 | 100.000 |
| seasonal_naive | post_covid | 13.899 | 34.439 | 11.527 | 0.731 | 100.000 |
| arima | post_covid | 18.843 | 70.473 | 16.233 |  | 100.000 |

## TRES DE FEBRERO

*mean observed 45.7, peak 114.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 45.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.017 | 24.416 | 9.770 | 0.848 | 100.000 |
| xgboost_nodemo | post_covid | 13.188 | 24.766 | 10.386 | 0.830 | 100.000 |
| xgboost | post_covid | 14.102 | 23.035 | 10.474 | 0.814 | 100.000 |
| dualtopo | post_covid | 15.303 | 27.534 | 11.983 | 0.794 | 100.000 |
| lstm | post_covid | 15.742 | 23.915 | 10.814 | 0.747 | 100.000 |
| arima | post_covid | 17.917 | 42.130 | 14.354 | 0.628 | 96.226 |
| gat | post_covid | 18.680 | 34.815 | 14.324 | 0.831 | 100.000 |
| persistence | post_covid | 19.482 | 36.980 | 15.248 | 0.633 | 100.000 |
| seasonal_naive | post_covid | 23.033 | 43.261 | 16.973 | 0.752 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 63.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.858 | 19.941 | 12.627 | 0.542 | 100.000 |
| xgboost_nodemo | post_covid | 16.225 | 22.042 | 13.486 | 0.562 | 100.000 |
| xgboost | post_covid | 17.692 | 21.775 | 14.209 | 0.513 | 100.000 |
| dualtopo | post_covid | 19.601 | 24.594 | 16.426 | 0.492 | 100.000 |
| lstm | post_covid | 20.468 | 20.253 | 14.480 | 0.074 | 100.000 |
| arima | post_covid | 20.857 | 23.541 | 16.141 | 0.137 | 92.308 |
| persistence | post_covid | 23.608 | 31.134 | 19.486 | 0.148 | 100.000 |
| gat | post_covid | 24.856 | 35.954 | 21.326 | 0.578 | 100.000 |
| seasonal_naive | post_covid | 28.763 | 33.979 | 21.344 | 0.673 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 28.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.419 | 28.725 | 7.019 | 0.693 | 100.000 |
| lstm | post_covid | 9.111 | 27.442 | 7.284 | 0.731 | 100.000 |
| xgboost_nodemo | post_covid | 9.375 | 27.389 | 7.401 | 0.599 | 100.000 |
| xgboost | post_covid | 9.431 | 24.249 | 6.878 | 0.622 | 100.000 |
| dualtopo | post_covid | 9.473 | 30.365 | 7.705 | 0.558 | 100.000 |
| gat | post_covid | 9.487 | 33.718 | 7.582 | 0.574 | 100.000 |
| persistence | post_covid | 14.434 | 42.609 | 11.167 | 0.602 | 100.000 |
| arima | post_covid | 14.534 | 60.030 | 12.633 | 0.597 | 100.000 |
| seasonal_naive | post_covid | 15.644 | 52.199 | 12.763 | 0.255 | 100.000 |

## GENERAL SAN MARTÍN

*mean observed 38.6, peak 99.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 14.343 | 34.259 | 11.051 | 0.818 | 100.000 |
| gnn_st | post_covid | 15.019 | 38.461 | 11.302 | 0.757 | 100.000 |
| xgboost_nodemo | post_covid | 15.160 | 38.327 | 11.618 | 0.808 | 100.000 |
| dualtopo | post_covid | 17.666 | 48.498 | 13.653 | 0.615 | 100.000 |
| lstm | post_covid | 18.178 | 47.698 | 13.717 | 0.599 | 100.000 |
| arima | post_covid | 20.960 | 66.766 | 16.699 | 0.371 | 90.566 |
| gat | post_covid | 24.122 | 64.988 | 18.506 | 0.700 | 98.113 |
| seasonal_naive | post_covid | 24.468 | 62.580 | 17.527 | 0.798 | 100.000 |
| persistence | post_covid | 24.636 | 58.166 | 18.742 | 0.371 | 88.679 |

### Flu season (Apr–Sep), 26 weeks scored, mean 50.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 16.672 | 36.955 | 13.367 | 0.759 | 100.000 |
| xgboost_nodemo | post_covid | 18.642 | 40.654 | 14.504 | 0.720 | 100.000 |
| gnn_st | post_covid | 19.298 | 44.798 | 15.823 | 0.587 | 100.000 |
| dualtopo | post_covid | 22.163 | 40.910 | 17.198 | 0.370 | 100.000 |
| lstm | post_covid | 23.661 | 49.778 | 18.545 | 0.117 | 100.000 |
| arima | post_covid | 25.518 | 50.285 | 20.126 | 0.016 | 80.769 |
| persistence | post_covid | 31.851 | 64.464 | 25.979 | 0.019 | 80.769 |
| gat | post_covid | 32.115 | 68.925 | 27.030 | 0.575 | 96.154 |
| seasonal_naive | post_covid | 33.317 | 75.213 | 26.636 | 0.721 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.173 | 32.593 | 6.948 | 0.740 | 100.000 |
| seasonal_naive | post_covid | 10.312 | 50.882 | 8.755 | 0.650 | 100.000 |
| lstm | post_covid | 10.464 | 45.773 | 9.067 | 0.706 | 100.000 |
| xgboost_nodemo | post_covid | 10.794 | 36.173 | 8.838 | 0.705 | 100.000 |
| xgboost | post_covid | 11.669 | 31.763 | 8.822 | 0.670 | 100.000 |
| dualtopo | post_covid | 11.817 | 55.525 | 10.240 | 0.408 | 100.000 |
| gat | post_covid | 12.207 | 61.343 | 10.298 | 0.349 | 100.000 |
| persistence | post_covid | 14.645 | 52.335 | 11.772 | 0.560 | 96.296 |
| arima | post_covid | 15.340 | 82.026 | 13.399 | 0.560 | 100.000 |

## SAN MIGUEL

*mean observed 38.1, peak 93.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 16.093 | 32.946 | 11.522 | 0.793 | 94.340 |
| arima | post_covid | 18.215 | 56.063 | 14.364 | 0.778 | 94.340 |
| gnn_st | post_covid | 18.310 | 37.046 | 12.290 | 0.789 | 94.340 |
| gat | post_covid | 19.438 | 46.035 | 14.228 | 0.723 | 96.226 |
| xgboost_nodemo | post_covid | 21.377 | 51.117 | 15.828 | 0.576 | 98.113 |
| lstm | post_covid | 21.697 | 53.207 | 16.102 | 0.811 | 100.000 |
| xgboost | post_covid | 22.981 | 51.135 | 16.661 | 0.493 | 90.566 |
| dualtopo | post_covid | 25.116 | 50.967 | 18.278 | 0.843 | 94.340 |
| seasonal_naive | post_covid | 26.908 | 60.244 | 19.371 | 0.183 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 53.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 20.517 | 25.549 | 15.287 | 0.618 | 92.308 |
| arima | post_covid | 21.951 | 31.408 | 17.264 | 0.534 | 88.462 |
| gat | post_covid | 23.533 | 27.311 | 17.429 | 0.445 | 92.308 |
| gnn_st | post_covid | 24.806 | 27.512 | 17.759 | 0.467 | 88.462 |
| lstm | post_covid | 28.150 | 31.917 | 21.074 | 0.604 | 100.000 |
| xgboost_nodemo | post_covid | 29.032 | 40.588 | 23.543 | 0.234 | 96.154 |
| xgboost | post_covid | 31.005 | 40.720 | 24.597 | -0.009 | 80.769 |
| dualtopo | post_covid | 32.091 | 39.182 | 25.379 | 0.827 | 88.462 |
| seasonal_naive | post_covid | 33.796 | 39.406 | 24.995 | -0.320 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 23.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.095 | 46.227 | 7.023 | 0.906 | 100.000 |
| xgboost_nodemo | post_covid | 9.239 | 61.256 | 8.399 | 0.884 | 100.000 |
| persistence | post_covid | 10.150 | 40.069 | 7.895 | 0.884 | 96.296 |
| xgboost | post_covid | 10.533 | 61.165 | 9.019 | 0.849 | 100.000 |
| lstm | post_covid | 12.688 | 73.709 | 11.313 | 0.824 | 100.000 |
| arima | post_covid | 13.685 | 79.804 | 11.571 | 0.765 | 100.000 |
| gat | post_covid | 14.436 | 64.065 | 11.146 | 0.892 | 100.000 |
| dualtopo | post_covid | 15.700 | 62.316 | 11.440 | 0.652 | 100.000 |
| seasonal_naive | post_covid | 17.927 | 80.311 | 13.955 | -0.152 | 100.000 |

## MALVINAS ARGENTINAS

*mean observed 25.7, peak 137.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 25.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 36.011 | 129.206 | 19.777 | 0.483 | 81.132 |
| xgboost_nodemo | post_covid | 37.439 | 146.634 | 19.628 | 0.539 | 84.906 |
| gat | post_covid | 38.338 | 84.137 | 20.669 | 0.543 | 67.925 |
| xgboost | post_covid | 39.529 | 102.674 | 19.814 | 0.595 | 83.019 |
| persistence | post_covid | 40.217 | 221.720 | 19.811 | 0.461 | 83.019 |
| seasonal_naive | post_covid | 41.056 | 95.301 | 20.161 | 0.389 | 84.906 |
| arima | post_covid | 41.441 | 227.046 | 22.785 | 0.352 | 81.132 |
| lstm | post_covid | 43.233 | 79.951 | 21.009 | 0.260 | 83.019 |
| dualtopo | post_covid | 44.934 | 81.216 | 23.347 | 0.088 | 47.170 |

### Flu season (Apr–Sep), 26 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 51.290 | 134.005 | 37.549 | 0.283 | 61.538 |
| xgboost_nodemo | post_covid | 53.235 | 82.862 | 36.158 | 0.368 | 69.231 |
| gat | post_covid | 54.358 | 86.008 | 37.385 | 0.272 | 57.692 |
| xgboost | post_covid | 56.289 | 65.776 | 36.878 | 0.441 | 65.385 |
| persistence | post_covid | 57.300 | 230.866 | 37.379 | 0.265 | 65.385 |
| seasonal_naive | post_covid | 58.446 | 69.056 | 37.784 | 0.115 | 69.231 |
| arima | post_covid | 59.039 | 248.996 | 43.283 | 0.079 | 61.538 |
| lstm | post_covid | 61.606 | 62.918 | 39.907 | -0.301 | 65.385 |
| dualtopo | post_covid | 63.768 | 72.714 | 42.203 | -0.353 | 50.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 3.518 | 124.585 | 2.664 | 0.750 | 100.000 |
| persistence | post_covid | 3.639 | 212.913 | 2.894 | 0.735 | 100.000 |
| lstm | post_covid | 3.779 | 96.354 | 2.810 | 0.747 | 100.000 |
| arima | post_covid | 3.836 | 205.908 | 3.047 | 0.742 | 100.000 |
| xgboost | post_covid | 4.010 | 138.205 | 3.381 | 0.606 | 100.000 |
| seasonal_naive | post_covid | 4.395 | 120.575 | 3.190 | 0.437 | 100.000 |
| xgboost_nodemo | post_covid | 4.730 | 208.044 | 3.710 | 0.679 | 100.000 |
| gat | post_covid | 6.312 | 82.335 | 4.573 | 0.020 | 77.778 |
| dualtopo | post_covid | 6.895 | 89.404 | 5.190 | -0.079 | 44.444 |

## LA MATANZA

*mean observed 23.5, peak 53.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 23.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 9.514 | 29.089 | 7.001 | 0.675 | 98.113 |
| persistence | post_covid | 9.645 | 33.551 | 7.292 | 0.693 | 98.113 |
| xgboost_nodemo | post_covid | 9.673 | 37.272 | 7.921 | 0.779 | 100.000 |
| gnn_st | post_covid | 9.738 | 28.483 | 7.400 | 0.825 | 100.000 |
| gat | post_covid | 9.939 | 42.026 | 8.513 | 0.882 | 96.226 |
| seasonal_naive | post_covid | 11.545 | 48.375 | 9.945 | 0.754 | 100.000 |
| xgboost | post_covid | 12.038 | 49.021 | 10.041 | 0.812 | 100.000 |
| lstm | post_covid | 16.321 | 52.242 | 13.105 | 0.530 | 100.000 |
| dualtopo | post_covid | 17.581 | 65.328 | 15.307 | 0.858 | 96.226 |

### Flu season (Apr–Sep), 26 weeks scored, mean 33.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 10.245 | 25.845 | 8.521 | 0.760 | 100.000 |
| xgboost_nodemo | post_covid | 11.560 | 30.978 | 9.731 | 0.520 | 100.000 |
| gnn_st | post_covid | 12.371 | 29.643 | 10.358 | 0.569 | 100.000 |
| persistence | post_covid | 12.659 | 37.154 | 10.332 | 0.224 | 96.154 |
| arima | post_covid | 12.745 | 34.201 | 10.587 | 0.184 | 96.154 |
| seasonal_naive | post_covid | 13.062 | 37.986 | 11.282 | 0.559 | 100.000 |
| xgboost | post_covid | 13.808 | 33.880 | 11.131 | 0.587 | 100.000 |
| lstm | post_covid | 21.099 | 50.582 | 18.388 | 0.130 | 100.000 |
| dualtopo | post_covid | 22.561 | 60.148 | 20.761 | 0.663 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4.611 | 24.167 | 3.547 | 0.254 | 100.000 |
| persistence | post_covid | 5.317 | 30.081 | 4.365 | 0.195 | 100.000 |
| gnn_st | post_covid | 6.227 | 27.367 | 4.551 | 0.258 | 100.000 |
| xgboost_nodemo | post_covid | 7.416 | 43.333 | 6.177 | 0.394 | 100.000 |
| gat | post_covid | 9.635 | 57.607 | 8.506 | 0.270 | 92.593 |
| lstm | post_covid | 9.707 | 53.841 | 8.019 | -0.019 | 100.000 |
| seasonal_naive | post_covid | 9.866 | 58.379 | 8.658 | -0.021 | 100.000 |
| xgboost | post_covid | 10.043 | 63.603 | 8.991 | 0.528 | 100.000 |
| dualtopo | post_covid | 10.798 | 70.317 | 10.056 | 0.511 | 96.296 |

## QUILMES

*mean observed 21.4, peak 39.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.631 | 26.963 | 5.153 | 0.769 | 100.000 |
| dualtopo | post_covid | 7.334 | 35.788 | 6.236 | 0.657 | 100.000 |
| arima | post_covid | 7.776 | 29.077 | 5.777 | 0.662 | 96.226 |
| persistence | post_covid | 8.059 | 30.932 | 6.074 | 0.650 | 98.113 |
| gat | post_covid | 8.394 | 37.121 | 6.978 | 0.761 | 100.000 |
| seasonal_naive | post_covid | 8.571 | 29.645 | 6.536 | 0.630 | 100.000 |
| lstm | post_covid | 9.247 | 33.789 | 7.060 | 0.409 | 100.000 |
| xgboost_nodemo | post_covid | 9.310 | 37.466 | 7.493 | 0.729 | 100.000 |
| xgboost | post_covid | 9.556 | 38.670 | 7.490 | 0.680 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 28.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.406 | 22.414 | 5.394 | 0.506 | 100.000 |
| arima | post_covid | 6.471 | 20.490 | 5.480 | 0.344 | 100.000 |
| persistence | post_covid | 6.844 | 21.796 | 5.829 | 0.335 | 100.000 |
| dualtopo | post_covid | 7.711 | 23.184 | 6.511 | 0.405 | 100.000 |
| gat | post_covid | 9.613 | 30.024 | 7.945 | 0.600 | 100.000 |
| lstm | post_covid | 9.892 | 27.288 | 7.999 | -0.207 | 100.000 |
| xgboost_nodemo | post_covid | 10.263 | 35.675 | 8.771 | 0.387 | 100.000 |
| xgboost | post_covid | 10.312 | 34.433 | 8.363 | 0.271 | 100.000 |
| seasonal_naive | post_covid | 10.574 | 29.418 | 8.708 | 0.354 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 15.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 6.042 | 29.864 | 4.444 | 0.623 | 100.000 |
| gnn_st | post_covid | 6.840 | 31.344 | 4.922 | 0.456 | 100.000 |
| dualtopo | post_covid | 6.953 | 47.925 | 5.970 | 0.518 | 100.000 |
| gat | post_covid | 7.024 | 43.956 | 6.046 | 0.383 | 100.000 |
| xgboost_nodemo | post_covid | 8.289 | 39.190 | 6.263 | 0.413 | 100.000 |
| lstm | post_covid | 8.581 | 40.049 | 6.156 | 0.121 | 100.000 |
| xgboost | post_covid | 8.767 | 42.749 | 6.649 | 0.389 | 100.000 |
| arima | post_covid | 8.852 | 37.347 | 6.063 | 0.086 | 92.593 |
| persistence | post_covid | 9.075 | 39.730 | 6.309 | 0.084 | 96.296 |

## VICENTE LÓPEZ

*mean observed 21.4, peak 114.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 24.965 | 164.435 | 19.120 | 0.253 | 92.453 |
| persistence | post_covid | 26.069 | 98.556 | 16.236 | 0.255 | 83.019 |
| gnn_st | post_covid | 26.299 | 165.998 | 20.276 | 0.632 | 96.226 |
| xgboost_nodemo | post_covid | 28.411 | 202.873 | 23.752 | 0.689 | 100.000 |
| xgboost | post_covid | 28.502 | 213.645 | 24.027 | 0.670 | 98.113 |
| dualtopo | post_covid | 38.775 | 8007535.127 | 32.697 | 0.051 | 98.113 |
| lstm | post_covid | 46.518 | 364.967 | 41.971 | 0.384 | 96.226 |
| gat | post_covid | 46.893 | 8151166.178 | 39.577 | 0.729 | 77.358 |
| seasonal_naive | post_covid | 56.458 | 318.031 | 41.996 | 0.690 | 84.906 |

### Flu season (Apr–Sep), 26 weeks scored, mean 32.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 30.600 | 133.410 | 21.853 | 0.023 | 84.615 |
| dualtopo | post_covid | 33.269 | 186.159 | 30.032 | -0.225 | 96.154 |
| gnn_st | post_covid | 34.912 | 204.474 | 29.262 | 0.444 | 92.308 |
| xgboost | post_covid | 35.742 | 237.417 | 31.437 | 0.547 | 96.154 |
| persistence | post_covid | 36.045 | 138.804 | 26.024 | 0.001 | 73.077 |
| xgboost_nodemo | post_covid | 36.096 | 234.192 | 32.326 | 0.605 | 100.000 |
| lstm | post_covid | 54.030 | 345.808 | 50.033 | -0.065 | 92.308 |
| gat | post_covid | 58.577 | 304.009 | 51.685 | 0.653 | 57.692 |
| seasonal_naive | post_covid | 74.772 | 366.496 | 60.714 | 0.622 | 69.231 |

### Off-season (Oct–Mar), 27 weeks scored, mean 11.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 9.103 | 58.309 | 6.810 | 0.216 | 92.593 |
| gnn_st | post_covid | 13.562 | 127.522 | 11.622 | 0.596 | 100.000 |
| arima | post_covid | 17.938 | 195.461 | 16.488 | 0.221 | 100.000 |
| xgboost_nodemo | post_covid | 18.159 | 171.554 | 15.495 | 0.449 | 100.000 |
| xgboost | post_covid | 19.091 | 189.874 | 16.891 | 0.498 | 100.000 |
| seasonal_naive | post_covid | 29.549 | 269.567 | 23.971 | 0.291 | 100.000 |
| gat | post_covid | 31.817 | 16000144.563 | 27.918 | 0.450 | 96.296 |
| lstm | post_covid | 37.901 | 384.125 | 34.206 | 0.130 | 100.000 |
| dualtopo | post_covid | 43.423 | 15718315.615 | 35.263 | 0.282 | 100.000 |

## ALMIRANTE BROWN

*mean observed 19.6, peak 41.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 5.606 | 47.412 | 4.575 | 0.799 | 100.000 |
| gnn_st | post_covid | 8.578 | 56.333 | 7.198 | 0.687 | 100.000 |
| arima | post_covid | 9.239 | 81.774 | 6.948 | 0.332 | 100.000 |
| gat | post_covid | 9.604 | 65.199 | 7.882 | 0.737 | 100.000 |
| persistence | post_covid | 10.678 | 80.212 | 8.724 | 0.332 | 96.226 |
| lstm | post_covid | 12.068 | 69.408 | 9.984 | 0.422 | 100.000 |
| xgboost | post_covid | 12.514 | 61.961 | 10.411 | 0.710 | 100.000 |
| xgboost_nodemo | post_covid | 13.079 | 60.296 | 10.382 | 0.677 | 100.000 |
| seasonal_naive | post_covid | 13.236 | 61.022 | 10.627 | 0.690 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 25.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 5.119 | 18.356 | 4.275 | 0.702 | 100.000 |
| arima | post_covid | 7.606 | 24.149 | 5.826 | 0.090 | 100.000 |
| gnn_st | post_covid | 8.591 | 33.950 | 7.301 | 0.623 | 100.000 |
| persistence | post_covid | 9.300 | 30.431 | 7.510 | 0.090 | 100.000 |
| gat | post_covid | 11.668 | 43.853 | 10.321 | 0.648 | 100.000 |
| lstm | post_covid | 12.116 | 44.757 | 10.074 | -0.330 | 100.000 |
| xgboost | post_covid | 14.776 | 58.430 | 13.018 | 0.481 | 100.000 |
| seasonal_naive | post_covid | 16.082 | 51.663 | 12.857 | 0.576 | 100.000 |
| xgboost_nodemo | post_covid | 16.223 | 61.702 | 13.687 | 0.377 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 6.037 | 75.392 | 4.864 | 0.538 | 100.000 |
| gat | post_covid | 7.068 | 85.755 | 5.533 | 0.230 | 100.000 |
| gnn_st | post_covid | 8.566 | 77.887 | 7.099 | 0.135 | 100.000 |
| xgboost_nodemo | post_covid | 9.074 | 58.942 | 7.200 | 0.292 | 100.000 |
| seasonal_naive | post_covid | 9.737 | 70.034 | 8.480 | 0.258 | 100.000 |
| xgboost | post_covid | 9.857 | 65.362 | 7.900 | 0.358 | 100.000 |
| arima | post_covid | 10.576 | 137.265 | 8.029 | -0.157 | 100.000 |
| persistence | post_covid | 11.854 | 128.149 | 9.892 | -0.157 | 92.593 |
| lstm | post_covid | 12.022 | 93.146 | 9.896 | 0.166 | 100.000 |

## MORÓN

*mean observed 19.1, peak 54.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 7.008 | 38.393 | 5.676 | 0.776 | 100.000 |
| xgboost | post_covid | 7.041 | 27.241 | 5.275 | 0.780 | 100.000 |
| gnn_st | post_covid | 7.434 | 29.355 | 5.420 | 0.752 | 100.000 |
| lstm | post_covid | 7.732 | 37.461 | 6.122 | 0.698 | 100.000 |
| dualtopo | post_covid | 8.981 | 39.177 | 7.198 | 0.804 | 100.000 |
| arima | post_covid | 9.042 | 46.001 | 7.026 | 0.530 | 98.113 |
| gat | post_covid | 9.088 | 41.550 | 7.348 | 0.760 | 98.113 |
| persistence | post_covid | 10.030 | 47.339 | 8.044 | 0.530 | 100.000 |
| seasonal_naive | post_covid | 14.587 | 51.899 | 9.691 | 0.720 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 6.414 | 20.936 | 5.303 | 0.757 | 100.000 |
| xgboost | post_covid | 8.304 | 21.210 | 6.274 | 0.711 | 100.000 |
| gnn_st | post_covid | 9.136 | 23.591 | 6.677 | 0.599 | 100.000 |
| lstm | post_covid | 9.434 | 28.744 | 7.524 | 0.558 | 100.000 |
| dualtopo | post_covid | 10.315 | 32.324 | 8.574 | 0.619 | 100.000 |
| gat | post_covid | 10.943 | 43.335 | 9.471 | 0.521 | 100.000 |
| arima | post_covid | 11.055 | 28.869 | 8.145 | 0.246 | 96.154 |
| persistence | post_covid | 12.108 | 40.137 | 10.069 | 0.246 | 100.000 |
| seasonal_naive | post_covid | 19.405 | 51.883 | 13.785 | 0.616 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.303 | 34.904 | 4.209 | 0.289 | 100.000 |
| xgboost | post_covid | 5.560 | 33.049 | 4.312 | 0.388 | 100.000 |
| lstm | post_covid | 5.626 | 45.856 | 4.772 | 0.262 | 100.000 |
| arima | post_covid | 6.542 | 62.499 | 5.948 | 0.204 | 100.000 |
| gat | post_covid | 6.842 | 39.831 | 5.303 | 0.191 | 96.296 |
| seasonal_naive | post_covid | 7.424 | 51.915 | 5.748 | 0.031 | 100.000 |
| dualtopo | post_covid | 7.475 | 45.776 | 5.873 | 0.370 | 100.000 |
| persistence | post_covid | 7.502 | 54.274 | 6.095 | 0.204 | 100.000 |
| xgboost_nodemo | post_covid | 7.536 | 55.203 | 6.036 | 0.323 | 100.000 |

## MERLO

*mean observed 17.9, peak 60.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 17.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.743 | 67.988 | 8.462 | 0.823 | 100.000 |
| persistence | post_covid | 12.234 | 68.225 | 8.934 | 0.614 | 94.340 |
| arima | post_covid | 15.928 | 185.027 | 13.939 | 0.620 | 98.113 |
| lstm | post_covid | 17.987 | 137.401 | 14.494 | 0.404 | 100.000 |
| xgboost_nodemo | post_covid | 20.824 | 104.747 | 14.645 | 0.785 | 100.000 |
| xgboost | post_covid | 23.093 | 123.901 | 16.569 | 0.793 | 100.000 |
| dualtopo | post_covid | 24.784 | 105.857 | 17.842 | 0.858 | 94.340 |
| seasonal_naive | post_covid | 26.507 | 241.783 | 20.679 | 0.234 | 100.000 |
| gat | post_covid | 42.451 | 167.278 | 31.396 | 0.798 | 86.792 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 13.275 | 62.128 | 10.612 | 0.481 | 96.154 |
| gnn_st | post_covid | 14.061 | 65.266 | 12.186 | 0.734 | 100.000 |
| persistence | post_covid | 15.316 | 45.446 | 11.720 | 0.482 | 92.308 |
| lstm | post_covid | 21.300 | 115.643 | 17.712 | -0.418 | 100.000 |
| xgboost_nodemo | post_covid | 28.723 | 99.991 | 22.924 | 0.663 | 100.000 |
| seasonal_naive | post_covid | 30.963 | 164.549 | 23.282 | -0.168 | 100.000 |
| xgboost | post_covid | 31.460 | 109.409 | 25.280 | 0.677 | 100.000 |
| dualtopo | post_covid | 34.126 | 103.817 | 28.391 | 0.857 | 100.000 |
| gat | post_covid | 58.856 | 227.106 | 54.045 | 0.695 | 76.923 |

### Off-season (Oct–Mar), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.014 | 70.711 | 4.876 | 0.353 | 100.000 |
| xgboost_nodemo | post_covid | 7.533 | 109.503 | 6.673 | 0.492 | 100.000 |
| persistence | post_covid | 8.240 | 91.005 | 6.250 | 0.344 | 96.296 |
| dualtopo | post_covid | 9.184 | 107.898 | 7.684 | -0.245 | 88.889 |
| xgboost | post_covid | 9.685 | 138.392 | 8.180 | 0.486 | 100.000 |
| lstm | post_covid | 14.078 | 159.160 | 11.395 | 0.516 | 100.000 |
| gat | post_covid | 14.201 | 107.449 | 9.586 | 0.319 | 96.296 |
| arima | post_covid | 18.119 | 307.927 | 17.142 | 0.385 | 100.000 |
| seasonal_naive | post_covid | 21.355 | 319.017 | 18.172 | -0.181 | 100.000 |

## TIGRE

*mean observed 8.0, peak 40.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 8.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.223 | 124.105 | 4.876 | 0.759 | 100.000 |
| arima | post_covid | 8.277 | 103.667 | 5.313 | 0.708 | 92.453 |
| persistence | post_covid | 8.759 | 98.348 | 5.382 | 0.648 | 96.226 |
| xgboost_nodemo | post_covid | 9.765 | 299.013 | 8.183 | 0.554 | 100.000 |
| xgboost | post_covid | 9.786 | 288.126 | 8.061 | 0.525 | 100.000 |
| seasonal_naive | post_covid | 10.366 | 102.643 | 5.902 | 0.332 | 100.000 |
| gat | post_covid | 10.825 | 196.493 | 7.220 | 0.576 | 98.113 |
| lstm | post_covid | 11.414 | 210.956 | 7.970 | 0.140 | 100.000 |
| dualtopo | post_covid | 11.451 | 169.892 | 7.231 | 0.316 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 10.029 | 111.627 | 8.041 | 0.624 | 100.000 |
| arima | post_covid | 11.426 | 85.408 | 8.993 | 0.602 | 88.462 |
| persistence | post_covid | 12.248 | 85.592 | 9.234 | 0.503 | 92.308 |
| xgboost_nodemo | post_covid | 12.402 | 185.289 | 10.769 | 0.253 | 100.000 |
| xgboost | post_covid | 12.539 | 174.561 | 10.716 | 0.237 | 100.000 |
| seasonal_naive | post_covid | 14.669 | 100.571 | 10.464 | -0.031 | 100.000 |
| gat | post_covid | 15.295 | 267.149 | 12.842 | 0.201 | 100.000 |
| lstm | post_covid | 15.660 | 251.407 | 13.034 | -0.521 | 100.000 |
| dualtopo | post_covid | 16.219 | 242.791 | 13.157 | -0.223 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 1.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 1.935 | 104.638 | 1.508 | -0.101 | 100.000 |
| dualtopo | post_covid | 2.014 | 99.693 | 1.524 | 0.599 | 100.000 |
| gat | post_covid | 2.181 | 128.453 | 1.806 | 0.255 | 96.296 |
| gnn_st | post_covid | 2.360 | 136.121 | 1.828 | 0.348 | 100.000 |
| persistence | post_covid | 2.474 | 110.631 | 1.674 | 0.309 | 100.000 |
| arima | post_covid | 2.963 | 121.250 | 1.770 | 0.163 | 96.296 |
| lstm | post_covid | 4.424 | 172.004 | 3.095 | 0.542 | 100.000 |
| xgboost | post_covid | 6.050 | 397.484 | 5.504 | 0.205 | 100.000 |
| xgboost_nodemo | post_covid | 6.250 | 408.525 | 5.692 | 0.206 | 100.000 |

## SAN ISIDRO

*mean observed 5.0, peak 29.9 per 100,000 over the full year*

### Overall (full year), 50 weeks scored, mean 5.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.710 | 803.679 | 7.099 | 0.244 | 100.000 |
| arima | post_covid | 8.915 | 620.148 | 6.195 | 0.003 | 86.000 |
| persistence | post_covid | 9.336 | 577.685 | 6.136 | 0.100 | 80.000 |
| seasonal_naive | post_covid | 9.932 | 391.779 | 5.792 | 0.441 | 100.000 |
| lstm | post_covid | 12.336 | 1255.396 | 9.296 | 0.149 | 100.000 |
| xgboost_nodemo | post_covid | 12.584 | 939.289 | 7.989 | 0.068 | 100.000 |
| xgboost | post_covid | 13.155 | 1043.657 | 8.367 | 0.063 | 100.000 |
| dualtopo | post_covid | 15.780 | 1522.935 | 13.579 | 0.642 | 100.000 |
| gat | post_covid | 17.468 | 1833.779 | 13.938 | -0.026 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 2.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 3.508 | 161.575 | 2.174 | 0.201 | 100.000 |
| arima | post_covid | 9.575 | 1070.872 | 6.589 | -0.412 | 92.308 |
| gnn_st | post_covid | 9.750 | 1137.329 | 8.329 | -0.351 | 100.000 |
| persistence | post_covid | 10.695 | 950.377 | 6.702 | -0.290 | 80.769 |
| xgboost_nodemo | post_covid | 14.010 | 1446.856 | 7.998 | -0.311 | 100.000 |
| xgboost | post_covid | 14.287 | 1585.293 | 8.105 | -0.323 | 100.000 |
| lstm | post_covid | 14.688 | 1853.562 | 10.146 | -0.508 | 100.000 |
| dualtopo | post_covid | 16.281 | 2146.778 | 13.934 | -0.502 | 100.000 |
| gat | post_covid | 23.118 | 3099.981 | 20.849 | 0.088 | 100.000 |

### Off-season (Oct–Mar), 24 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.421 | 484.536 | 5.766 | 0.582 | 100.000 |
| gat | post_covid | 7.531 | 622.629 | 6.451 | 0.654 | 100.000 |
| persistence | post_covid | 7.593 | 221.197 | 5.522 | 0.703 | 79.167 |
| arima | post_covid | 8.139 | 189.020 | 5.768 | 0.742 | 79.167 |
| lstm | post_covid | 9.130 | 683.238 | 8.376 | 0.764 | 100.000 |
| xgboost_nodemo | post_covid | 10.829 | 453.791 | 7.980 | 0.246 | 100.000 |
| xgboost | post_covid | 11.806 | 525.571 | 8.650 | 0.210 | 100.000 |
| seasonal_naive | post_covid | 13.863 | 611.975 | 9.713 | 0.357 | 100.000 |
| dualtopo | post_covid | 15.219 | 926.215 | 13.194 | 0.845 | 100.000 |

## LOMAS DE ZAMORA

*mean observed 0.6, peak 1.6 per 100,000 over the full year*

### Overall (full year), 41 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0.657 | 117.432 | 0.523 | -0.106 | 92.683 |
| persistence | post_covid | 0.949 | 148.682 | 0.643 | 0.027 | 92.683 |
| gnn_st | post_covid | 2.721 | 753.700 | 2.485 | 0.045 | 100.000 |
| seasonal_naive | post_covid | 3.278 | 739.566 | 2.317 | -0.099 | 100.000 |
| xgboost_nodemo | post_covid | 3.537 | 591.039 | 1.667 | -0.142 | 100.000 |
| dualtopo | post_covid | 3.575 | 1022.367 | 3.430 | 0.129 | 100.000 |
| lstm | post_covid | 3.822 | 1061.710 | 3.625 | 0.082 | 100.000 |
| gat | post_covid | 4.568 | 1238.177 | 4.016 | -0.133 | 100.000 |
| xgboost | post_covid | 5.119 | 885.177 | 2.559 | -0.117 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0.706 | 113.613 | 0.551 | -0.161 | 88.462 |
| persistence | post_covid | 1.117 | 170.406 | 0.758 | 0.012 | 88.462 |
| gnn_st | post_covid | 3.186 | 947.313 | 3.036 | -0.081 | 100.000 |
| seasonal_naive | post_covid | 3.846 | 994.581 | 2.791 | -0.178 | 100.000 |
| dualtopo | post_covid | 4.022 | 1208.018 | 3.944 | 0.060 | 100.000 |
| xgboost_nodemo | post_covid | 4.110 | 693.731 | 1.640 | -0.203 | 100.000 |
| lstm | post_covid | 4.255 | 1237.823 | 4.131 | -0.161 | 100.000 |
| gat | post_covid | 5.478 | 1639.205 | 5.131 | -0.283 | 100.000 |
| xgboost | post_covid | 5.730 | 886.863 | 2.184 | -0.119 | 100.000 |

### Off-season (Oct–Mar), 15 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.544 | 112.993 | 0.444 | 0.132 | 100.000 |
| arima | post_covid | 0.563 | 123.707 | 0.473 | 0.077 | 100.000 |
| gnn_st | post_covid | 1.624 | 435.621 | 1.532 | 0.382 | 100.000 |
| seasonal_naive | post_covid | 1.928 | 320.612 | 1.497 | 0.183 | 100.000 |
| xgboost_nodemo | post_covid | 2.217 | 422.330 | 1.714 | 0.127 | 100.000 |
| gat | post_covid | 2.245 | 579.346 | 2.083 | 0.037 | 100.000 |
| dualtopo | post_covid | 2.627 | 717.369 | 2.538 | 0.340 | 100.000 |
| lstm | post_covid | 2.923 | 772.381 | 2.748 | 0.463 | 100.000 |
| xgboost | post_covid | 3.837 | 882.406 | 3.210 | -0.105 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
