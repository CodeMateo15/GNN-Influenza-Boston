# Per-neighborhood leaderboard — horizon 2

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Apr–Sep), Off-season (Oct–Mar).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* them -- LOMAS DE ZAMORA has 12 fewer scored weeks than the best-covered node (41 against 53) -- so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

> **MAPE is not usable in this table** (it reaches 1,455%). It divides by the observed rate, and this city reports observed zeros and near-zeros rather than suppressing small counts, so the denominator goes to zero. Rank on RMSE or MAE. The column is kept so the two cities' tables have the same shape.

## Summary — neighborhoods won, out of 19

| model | Overall (full year) | Flu season (Apr–Sep) | Off-season (Oct–Mar) |
| --- | --- | --- | --- |
| gnn_st | 12 | 6 | 6 |
| persistence | 4 | 3 | 5 |
| dualtopo | 1 | 1 | 2 |
| lstm | 1 | 0 | 1 |
| xgboost | 1 | 1 | 1 |
| arima | 0 | 3 | 1 |
| gat | 0 | 1 | 1 |
| seasonal_naive | 0 | 1 | 1 |
| xgboost_nodemo | 0 | 3 | 1 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `dualtopo (post_covid)`: Avellan.; `gnn_st (post_covid)`: AlmBrown, Ezeiza, F.Varela, LaMatanza, Lanús, MalvArg., Merlo, Quilmes, S.Isidro, Tigre, TresFeb., V.López; `lstm (post_covid)`: Morón; `persistence (post_covid)`: J.C.Paz, LomasZam., Moreno, S.Miguel; `xgboost (post_covid)`: S.Martín
- **Flu season (Apr–Sep)** — `arima (post_covid)`: AlmBrown, LomasZam., Merlo; `dualtopo (post_covid)`: Avellan.; `gat (post_covid)`: Ezeiza; `gnn_st (post_covid)`: LaMatanza, Lanús, MalvArg., Quilmes, Tigre, V.López; `persistence (post_covid)`: J.C.Paz, Moreno, S.Miguel; `seasonal_naive (post_covid)`: S.Isidro; `xgboost (post_covid)`: S.Martín; `xgboost_nodemo (post_covid)`: F.Varela, Morón, TresFeb.
- **Off-season (Oct–Mar)** — `arima (post_covid)`: MalvArg.; `dualtopo (post_covid)`: AlmBrown, S.Martín; `gat (post_covid)`: Lanús; `gnn_st (post_covid)`: F.Varela, Merlo, S.Isidro, S.Miguel, Tigre, TresFeb.; `lstm (post_covid)`: Morón; `persistence (post_covid)`: J.C.Paz, LaMatanza, LomasZam., Moreno, V.López; `seasonal_naive (post_covid)`: Quilmes; `xgboost (post_covid)`: Ezeiza; `xgboost_nodemo (post_covid)`: Avellan.

`gnn_st (post_covid)` wins 12 of 19 neighborhoods. The pooled leaderboard is led by `persistence (post_covid)` instead, and `gnn_st (post_covid)` ranks 2 there. That is not a contradiction: the pooled metric flattens all 14 neighborhoods into one set of cells, so it is dominated by the high-rate ones (Dorchester and Roxbury average roughly five times Fenway's rate). Winning most neighborhoods and winning the pooled error are different achievements, and which one you want depends on whether you are allocating city-wide capacity or advising a specific neighborhood.

## JOSÉ C. PAZ

*mean observed 257.3, peak 740.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 257.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 90.269 | 22.718 | 58.884 | 0.808 | 77.358 |
| arima | post_covid | 91.749 | 21.455 | 60.179 | 0.800 | 69.811 |
| gnn_st | post_covid | 97.735 | 22.937 | 66.349 | 0.825 | 60.377 |
| gat | post_covid | 187.706 | 62.308 | 154.381 | 0.688 | 16.981 |
| xgboost | post_covid | 212.119 | 69.826 | 182.513 | 0.806 | 9.434 |
| xgboost_nodemo | post_covid | 214.922 | 73.723 | 187.422 | 0.822 | 3.774 |
| seasonal_naive | post_covid | 218.750 | 67.905 | 167.196 | 0.318 | 33.962 |
| dualtopo | post_covid | 237.779 | 77.480 | 195.005 | 0.373 | 3.774 |
| lstm | post_covid | 255.778 | 82.131 | 214.668 | 0.321 | 9.434 |

### Flu season (Apr–Sep), 26 weeks scored, mean 362.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 119.833 | 23.305 | 85.535 | 0.582 | 65.385 |
| arima | post_covid | 122.013 | 22.626 | 90.089 | 0.551 | 57.692 |
| gnn_st | post_covid | 126.392 | 23.269 | 92.991 | 0.613 | 50.000 |
| gat | post_covid | 239.210 | 54.230 | 201.536 | 0.341 | 23.077 |
| xgboost | post_covid | 267.743 | 67.900 | 246.359 | 0.692 | 0.000 |
| xgboost_nodemo | post_covid | 269.448 | 68.702 | 248.457 | 0.687 | 0.000 |
| seasonal_naive | post_covid | 281.790 | 59.246 | 224.270 | -0.208 | 26.923 |
| dualtopo | post_covid | 302.600 | 69.812 | 258.973 | -0.052 | 0.000 |
| lstm | post_covid | 335.100 | 80.025 | 301.095 | -0.636 | 0.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 156.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 46.551 | 22.152 | 33.221 | 0.724 | 88.889 |
| arima | post_covid | 46.780 | 20.327 | 31.376 | 0.718 | 81.481 |
| gnn_st | post_covid | 58.027 | 22.616 | 40.694 | 0.740 | 70.370 |
| gat | post_covid | 118.577 | 70.086 | 108.973 | 0.790 | 11.111 |
| seasonal_naive | post_covid | 132.161 | 76.242 | 112.235 | 0.507 | 40.741 |
| xgboost | post_covid | 138.894 | 71.681 | 121.033 | -0.364 | 18.519 |
| lstm | post_covid | 142.439 | 84.159 | 131.442 | 0.721 | 18.519 |
| xgboost_nodemo | post_covid | 144.080 | 78.559 | 128.648 | -0.038 | 7.407 |
| dualtopo | post_covid | 151.025 | 84.864 | 133.406 | 0.060 | 7.407 |

## AVELLANEDA

*mean observed 143.6, peak 323.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 143.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 35.111 | 15.395 | 23.922 | 0.848 | 94.340 |
| gnn_st | post_covid | 35.390 | 18.727 | 26.604 | 0.798 | 94.340 |
| gat | post_covid | 40.572 | 21.685 | 30.966 | 0.811 | 98.113 |
| xgboost | post_covid | 40.713 | 19.628 | 29.397 | 0.831 | 98.113 |
| arima | post_covid | 41.007 | 23.648 | 31.842 | 0.688 | 86.792 |
| xgboost_nodemo | post_covid | 41.227 | 19.296 | 28.987 | 0.825 | 96.226 |
| persistence | post_covid | 43.503 | 21.872 | 31.673 | 0.699 | 84.906 |
| seasonal_naive | post_covid | 46.153 | 26.007 | 35.405 | 0.858 | 96.226 |
| lstm | post_covid | 49.654 | 28.237 | 39.662 | 0.653 | 90.566 |

### Flu season (Apr–Sep), 26 weeks scored, mean 185.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 42.026 | 16.204 | 30.474 | 0.786 | 96.154 |
| gnn_st | post_covid | 42.083 | 19.825 | 34.399 | 0.528 | 92.308 |
| gat | post_covid | 44.536 | 19.359 | 35.264 | 0.601 | 100.000 |
| arima | post_covid | 47.125 | 18.714 | 36.009 | 0.353 | 80.769 |
| persistence | post_covid | 51.511 | 21.738 | 39.900 | 0.380 | 76.923 |
| xgboost | post_covid | 53.808 | 25.364 | 43.668 | 0.624 | 96.154 |
| seasonal_naive | post_covid | 54.852 | 22.597 | 42.265 | 0.810 | 92.308 |
| xgboost_nodemo | post_covid | 55.179 | 25.724 | 44.255 | 0.610 | 92.308 |
| lstm | post_covid | 59.152 | 28.864 | 50.025 | -0.042 | 84.615 |

### Off-season (Oct–Mar), 27 weeks scored, mean 103.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 20.111 | 13.105 | 14.284 | 0.787 | 100.000 |
| xgboost | post_covid | 21.577 | 14.104 | 15.654 | 0.784 | 100.000 |
| dualtopo | post_covid | 26.816 | 14.616 | 17.613 | 0.537 | 92.593 |
| gnn_st | post_covid | 27.443 | 17.669 | 19.099 | 0.556 | 96.296 |
| persistence | post_covid | 34.055 | 22.002 | 23.751 | 0.404 | 92.593 |
| arima | post_covid | 34.093 | 28.399 | 27.830 | 0.351 | 92.593 |
| seasonal_naive | post_covid | 35.833 | 29.290 | 28.799 | 0.505 | 100.000 |
| gat | post_covid | 36.348 | 23.926 | 26.828 | 0.487 | 96.296 |
| lstm | post_covid | 38.346 | 27.633 | 29.683 | 0.368 | 96.296 |

## EZEIZA

*mean observed 83.5, peak 186.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 83.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 13.467 | 15.818 | 10.401 | 0.949 | 100.000 |
| xgboost_nodemo | post_covid | 14.567 | 16.067 | 11.766 | 0.939 | 100.000 |
| xgboost | post_covid | 15.608 | 16.046 | 12.449 | 0.932 | 100.000 |
| dualtopo | post_covid | 16.672 | 22.909 | 13.814 | 0.927 | 100.000 |
| persistence | post_covid | 17.439 | 19.513 | 13.801 | 0.915 | 100.000 |
| gat | post_covid | 18.503 | 29.812 | 14.629 | 0.923 | 100.000 |
| seasonal_naive | post_covid | 28.077 | 28.828 | 21.442 | 0.782 | 100.000 |
| lstm | post_covid | 32.536 | 32.150 | 24.783 | 0.722 | 96.226 |
| arima | post_covid | 42.249 | 62.858 | 37.071 |  | 52.830 |

### Flu season (Apr–Sep), 26 weeks scored, mean 119.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 13.855 | 8.598 | 10.157 | 0.877 | 100.000 |
| gnn_st | post_covid | 14.373 | 9.638 | 11.122 | 0.858 | 100.000 |
| xgboost_nodemo | post_covid | 17.339 | 12.351 | 14.455 | 0.814 | 100.000 |
| dualtopo | post_covid | 17.459 | 12.015 | 14.259 | 0.876 | 100.000 |
| xgboost | post_covid | 19.724 | 14.093 | 16.595 | 0.769 | 100.000 |
| persistence | post_covid | 19.820 | 14.346 | 16.682 | 0.756 | 100.000 |
| seasonal_naive | post_covid | 35.148 | 23.853 | 28.668 | 0.633 | 100.000 |
| lstm | post_covid | 42.496 | 27.699 | 35.264 | -0.296 | 92.308 |
| arima | post_covid | 44.850 | 28.476 | 37.392 |  | 61.538 |

### Off-season (Oct–Mar), 27 weeks scored, mean 48.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 10.179 | 17.926 | 8.456 | 0.821 | 100.000 |
| xgboost_nodemo | post_covid | 11.271 | 19.646 | 9.177 | 0.789 | 100.000 |
| gnn_st | post_covid | 12.533 | 21.769 | 9.707 | 0.769 | 100.000 |
| persistence | post_covid | 14.789 | 24.488 | 11.028 | 0.704 | 100.000 |
| dualtopo | post_covid | 15.878 | 33.400 | 13.387 | 0.659 | 100.000 |
| lstm | post_covid | 18.412 | 36.436 | 14.691 | 0.418 | 100.000 |
| seasonal_naive | post_covid | 18.915 | 33.620 | 14.483 | 0.600 | 100.000 |
| gat | post_covid | 22.072 | 50.239 | 18.935 | 0.440 | 100.000 |
| arima | post_covid | 39.582 | 95.966 | 36.763 |  | 44.444 |

## MORENO

*mean observed 74.1, peak 197.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 74.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 21.861 | 29.352 | 16.194 | 0.898 | 94.340 |
| gnn_st | post_covid | 22.344 | 25.221 | 14.545 | 0.910 | 92.453 |
| lstm | post_covid | 23.408 | 31.171 | 16.408 | 0.882 | 100.000 |
| gat | post_covid | 32.032 | 38.718 | 22.723 | 0.779 | 98.113 |
| dualtopo | post_covid | 35.479 | 41.413 | 27.225 | 0.827 | 75.472 |
| xgboost | post_covid | 36.737 | 46.170 | 27.244 | 0.690 | 92.453 |
| arima | post_covid | 39.092 | 72.016 | 30.915 | 0.784 | 58.491 |
| xgboost_nodemo | post_covid | 39.399 | 44.147 | 29.839 | 0.669 | 88.679 |
| seasonal_naive | post_covid | 41.066 | 62.099 | 32.407 | 0.593 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 112.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 29.214 | 22.749 | 25.146 | 0.714 | 96.154 |
| gnn_st | post_covid | 29.553 | 17.022 | 20.531 | 0.688 | 88.462 |
| lstm | post_covid | 30.007 | 18.860 | 21.810 | 0.663 | 100.000 |
| gat | post_covid | 43.821 | 30.450 | 35.533 | 0.524 | 96.154 |
| dualtopo | post_covid | 45.583 | 33.081 | 37.454 | 0.597 | 65.385 |
| xgboost | post_covid | 50.479 | 35.842 | 43.132 | 0.201 | 84.615 |
| arima | post_covid | 50.547 | 34.095 | 42.135 | 0.556 | 42.308 |
| xgboost_nodemo | post_covid | 53.291 | 38.237 | 45.989 | 0.159 | 76.923 |
| seasonal_naive | post_covid | 54.343 | 39.429 | 45.983 | 0.241 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 37.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 10.782 | 35.711 | 7.573 | 0.877 | 92.593 |
| gnn_st | post_covid | 11.790 | 33.116 | 8.781 | 0.889 | 96.296 |
| gat | post_covid | 12.842 | 46.680 | 10.387 | 0.835 | 100.000 |
| xgboost | post_covid | 13.983 | 56.115 | 11.945 | 0.806 | 100.000 |
| lstm | post_covid | 14.438 | 43.025 | 11.205 | 0.890 | 100.000 |
| xgboost_nodemo | post_covid | 17.672 | 49.837 | 14.287 | 0.791 | 100.000 |
| seasonal_naive | post_covid | 21.601 | 83.929 | 19.333 | 0.462 | 100.000 |
| dualtopo | post_covid | 21.681 | 49.436 | 17.375 | 0.548 | 85.185 |
| arima | post_covid | 23.226 | 108.532 | 20.111 | 0.656 | 74.074 |

## LANÚS

*mean observed 70.6, peak 171.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 70.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 15.890 | 17.323 | 11.870 | 0.897 | 100.000 |
| gat | post_covid | 18.815 | 18.453 | 13.414 | 0.882 | 100.000 |
| xgboost | post_covid | 18.995 | 18.843 | 12.813 | 0.882 | 100.000 |
| xgboost_nodemo | post_covid | 20.468 | 20.726 | 14.357 | 0.867 | 100.000 |
| persistence | post_covid | 20.869 | 21.615 | 15.315 | 0.836 | 94.340 |
| arima | post_covid | 21.912 | 22.693 | 16.182 | 0.828 | 86.792 |
| seasonal_naive | post_covid | 23.021 | 22.954 | 16.624 | 0.820 | 100.000 |
| lstm | post_covid | 27.979 | 26.526 | 18.885 | 0.620 | 98.113 |
| dualtopo | post_covid | 31.484 | 51.627 | 20.961 | 0.594 | 90.566 |

### Flu season (Apr–Sep), 26 weeks scored, mean 98.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 19.558 | 15.113 | 15.131 | 0.734 | 100.000 |
| dualtopo | post_covid | 21.460 | 15.837 | 16.239 | 0.687 | 100.000 |
| xgboost | post_covid | 22.047 | 14.787 | 14.496 | 0.747 | 100.000 |
| xgboost_nodemo | post_covid | 23.382 | 16.990 | 16.554 | 0.714 | 100.000 |
| gat | post_covid | 25.155 | 19.545 | 19.675 | 0.700 | 100.000 |
| persistence | post_covid | 26.184 | 19.570 | 20.070 | 0.597 | 96.154 |
| arima | post_covid | 27.364 | 20.900 | 21.244 | 0.592 | 80.769 |
| seasonal_naive | post_covid | 28.794 | 22.776 | 23.214 | 0.719 | 100.000 |
| lstm | post_covid | 38.236 | 27.109 | 27.938 | -0.815 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 43.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 9.249 | 17.402 | 7.386 | 0.813 | 100.000 |
| gnn_st | post_covid | 11.283 | 19.452 | 8.730 | 0.785 | 100.000 |
| lstm | post_covid | 11.350 | 25.964 | 10.168 | 0.874 | 100.000 |
| persistence | post_covid | 13.953 | 23.585 | 10.735 | 0.698 | 92.593 |
| arima | post_covid | 14.881 | 24.420 | 11.308 | 0.687 | 92.593 |
| xgboost | post_covid | 15.499 | 22.750 | 11.192 | 0.772 | 100.000 |
| seasonal_naive | post_covid | 15.553 | 23.126 | 10.278 | 0.468 | 100.000 |
| xgboost_nodemo | post_covid | 17.203 | 24.323 | 12.241 | 0.771 | 100.000 |
| dualtopo | post_covid | 38.760 | 86.091 | 25.507 | -0.331 | 81.481 |

## FLORENCIO VARELA

*mean observed 53.7, peak 146.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 53.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.055 | 18.050 | 9.852 | 0.892 | 94.340 |
| xgboost_nodemo | post_covid | 14.082 | 21.804 | 10.923 | 0.898 | 100.000 |
| xgboost | post_covid | 14.445 | 23.230 | 11.464 | 0.882 | 100.000 |
| persistence | post_covid | 17.677 | 23.231 | 12.607 | 0.830 | 94.340 |
| dualtopo | post_covid | 19.026 | 38.981 | 14.796 | 0.791 | 100.000 |
| lstm | post_covid | 19.799 | 21.804 | 12.721 | 0.803 | 100.000 |
| seasonal_naive | post_covid | 21.981 | 32.443 | 17.099 | 0.811 | 100.000 |
| gat | post_covid | 22.225 | 29.859 | 16.665 | 0.834 | 100.000 |
| arima | post_covid | 31.104 | 54.192 | 23.811 |  | 83.019 |

### Flu season (Apr–Sep), 26 weeks scored, mean 76.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 16.628 | 17.401 | 13.171 | 0.794 | 100.000 |
| xgboost | post_covid | 18.027 | 21.304 | 15.522 | 0.748 | 100.000 |
| gnn_st | post_covid | 18.465 | 17.569 | 13.995 | 0.745 | 92.308 |
| dualtopo | post_covid | 20.533 | 21.634 | 15.631 | 0.708 | 100.000 |
| persistence | post_covid | 23.488 | 23.305 | 18.385 | 0.639 | 92.308 |
| lstm | post_covid | 26.223 | 20.456 | 17.888 | 0.515 | 100.000 |
| seasonal_naive | post_covid | 28.006 | 30.369 | 22.886 | 0.603 | 100.000 |
| gat | post_covid | 29.070 | 28.865 | 23.426 | 0.609 | 100.000 |
| arima | post_covid | 39.870 | 35.904 | 31.389 |  | 65.385 |

### Off-season (Oct–Mar), 27 weeks scored, mean 32.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.710 | 18.513 | 5.863 | 0.812 | 96.296 |
| persistence | post_covid | 9.063 | 23.160 | 7.043 | 0.777 | 96.296 |
| xgboost | post_covid | 9.832 | 25.085 | 7.556 | 0.657 | 100.000 |
| lstm | post_covid | 10.360 | 23.101 | 7.746 | 0.808 | 100.000 |
| xgboost_nodemo | post_covid | 11.091 | 26.044 | 8.758 | 0.663 | 100.000 |
| gat | post_covid | 12.484 | 30.816 | 10.154 | 0.627 | 100.000 |
| seasonal_naive | post_covid | 13.899 | 34.439 | 11.527 | 0.731 | 100.000 |
| dualtopo | post_covid | 17.452 | 55.686 | 13.992 | -0.090 | 100.000 |
| arima | post_covid | 19.193 | 71.802 | 16.513 |  | 100.000 |

## TRES DE FEBRERO

*mean observed 45.7, peak 114.5 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 45.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 12.973 | 21.210 | 9.390 | 0.825 | 96.226 |
| xgboost_nodemo | post_covid | 13.515 | 25.018 | 10.388 | 0.812 | 100.000 |
| xgboost | post_covid | 13.689 | 25.132 | 10.568 | 0.810 | 100.000 |
| lstm | post_covid | 14.018 | 22.976 | 10.121 | 0.800 | 100.000 |
| dualtopo | post_covid | 14.588 | 24.170 | 10.590 | 0.805 | 98.113 |
| arima | post_covid | 15.039 | 30.510 | 11.730 | 0.751 | 96.226 |
| persistence | post_covid | 15.991 | 25.411 | 11.352 | 0.752 | 96.226 |
| gat | post_covid | 18.620 | 27.968 | 12.648 | 0.684 | 100.000 |
| seasonal_naive | post_covid | 23.033 | 43.261 | 16.973 | 0.752 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 63.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 16.231 | 20.852 | 13.039 | 0.490 | 100.000 |
| xgboost | post_covid | 16.586 | 21.892 | 13.574 | 0.498 | 100.000 |
| gnn_st | post_covid | 17.102 | 22.119 | 13.843 | 0.416 | 96.154 |
| dualtopo | post_covid | 18.337 | 24.232 | 14.165 | 0.569 | 96.154 |
| lstm | post_covid | 18.480 | 21.902 | 14.449 | 0.239 | 100.000 |
| arima | post_covid | 18.947 | 22.968 | 15.086 | 0.277 | 92.308 |
| persistence | post_covid | 20.826 | 25.468 | 16.011 | 0.272 | 96.154 |
| gat | post_covid | 24.989 | 29.859 | 18.757 | 0.273 | 100.000 |
| seasonal_naive | post_covid | 28.763 | 33.979 | 21.344 | 0.673 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 28.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.979 | 20.335 | 5.102 | 0.807 | 96.296 |
| lstm | post_covid | 7.539 | 24.010 | 5.953 | 0.761 | 100.000 |
| gat | post_covid | 8.903 | 26.148 | 6.766 | 0.688 | 100.000 |
| persistence | post_covid | 9.179 | 25.357 | 6.865 | 0.767 | 96.296 |
| dualtopo | post_covid | 9.694 | 24.110 | 7.147 | 0.573 | 100.000 |
| arima | post_covid | 9.915 | 37.771 | 8.498 | 0.763 | 100.000 |
| xgboost | post_covid | 10.145 | 28.252 | 7.674 | 0.517 | 100.000 |
| xgboost_nodemo | post_covid | 10.239 | 29.030 | 7.834 | 0.523 | 100.000 |
| seasonal_naive | post_covid | 15.644 | 52.199 | 12.763 | 0.255 | 100.000 |

## GENERAL SAN MARTÍN

*mean observed 38.6, peak 99.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 13.130 | 33.183 | 10.390 | 0.851 | 100.000 |
| gnn_st | post_covid | 14.401 | 30.530 | 9.926 | 0.774 | 96.226 |
| dualtopo | post_covid | 14.457 | 35.223 | 10.233 | 0.754 | 98.113 |
| xgboost_nodemo | post_covid | 14.891 | 42.681 | 12.374 | 0.832 | 100.000 |
| arima | post_covid | 16.366 | 45.705 | 12.608 | 0.675 | 92.453 |
| lstm | post_covid | 17.525 | 43.809 | 13.084 | 0.657 | 100.000 |
| persistence | post_covid | 17.757 | 35.139 | 12.212 | 0.673 | 94.340 |
| gat | post_covid | 21.100 | 50.205 | 14.356 | 0.528 | 92.453 |
| seasonal_naive | post_covid | 24.468 | 62.580 | 17.527 | 0.798 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 50.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 15.728 | 34.332 | 12.932 | 0.799 | 100.000 |
| xgboost_nodemo | post_covid | 17.588 | 39.947 | 14.936 | 0.766 | 100.000 |
| gnn_st | post_covid | 18.185 | 33.461 | 13.133 | 0.643 | 96.154 |
| dualtopo | post_covid | 18.571 | 35.814 | 12.969 | 0.585 | 96.154 |
| arima | post_covid | 20.260 | 37.333 | 15.531 | 0.512 | 88.462 |
| persistence | post_covid | 22.746 | 38.376 | 16.673 | 0.516 | 92.308 |
| lstm | post_covid | 23.319 | 55.862 | 19.386 | 0.278 | 100.000 |
| gat | post_covid | 28.649 | 66.707 | 21.478 | 0.314 | 84.615 |
| seasonal_naive | post_covid | 33.317 | 75.213 | 26.636 | 0.721 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 8.841 | 34.676 | 7.598 | 0.737 | 100.000 |
| lstm | post_covid | 8.900 | 32.649 | 7.016 | 0.741 | 100.000 |
| gat | post_covid | 9.144 | 34.926 | 7.499 | 0.764 | 100.000 |
| gnn_st | post_covid | 9.416 | 27.817 | 6.838 | 0.749 | 96.296 |
| xgboost | post_covid | 10.010 | 32.118 | 7.943 | 0.735 | 100.000 |
| seasonal_naive | post_covid | 10.312 | 50.882 | 8.755 | 0.650 | 100.000 |
| persistence | post_covid | 10.987 | 32.143 | 7.917 | 0.707 | 96.296 |
| arima | post_covid | 11.422 | 53.457 | 9.793 | 0.710 | 96.296 |
| xgboost_nodemo | post_covid | 11.720 | 45.212 | 9.906 | 0.732 | 100.000 |

## SAN MIGUEL

*mean observed 38.1, peak 93.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 38.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 11.369 | 28.136 | 8.188 | 0.896 | 96.226 |
| gnn_st | post_covid | 12.034 | 28.496 | 8.106 | 0.898 | 94.340 |
| xgboost_nodemo | post_covid | 16.597 | 47.110 | 13.161 | 0.778 | 100.000 |
| xgboost | post_covid | 19.581 | 46.558 | 14.286 | 0.726 | 96.226 |
| lstm | post_covid | 19.740 | 49.385 | 14.710 | 0.835 | 100.000 |
| dualtopo | post_covid | 20.678 | 44.766 | 15.181 | 0.884 | 90.566 |
| arima | post_covid | 20.959 | 60.463 | 16.472 | 0.829 | 81.132 |
| gat | post_covid | 21.155 | 45.932 | 15.041 | 0.745 | 96.226 |
| seasonal_naive | post_covid | 26.908 | 60.244 | 19.371 | 0.183 | 98.113 |

### Flu season (Apr–Sep), 26 weeks scored, mean 53.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 14.070 | 18.986 | 10.106 | 0.809 | 96.154 |
| gnn_st | post_covid | 15.757 | 19.469 | 10.887 | 0.791 | 92.308 |
| xgboost_nodemo | post_covid | 21.546 | 32.055 | 17.856 | 0.619 | 100.000 |
| lstm | post_covid | 25.317 | 29.516 | 19.001 | 0.593 | 100.000 |
| xgboost | post_covid | 26.038 | 31.945 | 19.832 | 0.348 | 92.308 |
| arima | post_covid | 26.508 | 33.514 | 20.976 | 0.744 | 65.385 |
| dualtopo | post_covid | 26.724 | 33.040 | 20.893 | 0.771 | 80.769 |
| gat | post_covid | 27.240 | 30.660 | 20.132 | 0.470 | 92.308 |
| seasonal_naive | post_covid | 33.796 | 39.406 | 24.995 | -0.320 | 96.154 |

### Off-season (Oct–Mar), 27 weeks scored, mean 23.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.724 | 37.190 | 5.428 | 0.916 | 96.296 |
| persistence | post_covid | 7.944 | 36.946 | 6.341 | 0.909 | 96.296 |
| xgboost_nodemo | post_covid | 9.678 | 61.606 | 8.641 | 0.863 | 100.000 |
| xgboost | post_covid | 9.990 | 60.629 | 8.944 | 0.875 | 100.000 |
| lstm | post_covid | 12.154 | 68.519 | 10.578 | 0.894 | 100.000 |
| dualtopo | post_covid | 12.311 | 56.057 | 9.681 | 0.875 | 100.000 |
| gat | post_covid | 12.806 | 60.638 | 10.138 | 0.894 | 100.000 |
| arima | post_covid | 13.625 | 86.413 | 12.134 | 0.801 | 96.296 |
| seasonal_naive | post_covid | 17.927 | 80.311 | 13.955 | -0.152 | 100.000 |

## MALVINAS ARGENTINAS

*mean observed 25.7, peak 137.4 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 25.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 27.119 | 97.837 | 13.597 | 0.728 | 83.019 |
| persistence | post_covid | 28.617 | 116.306 | 13.467 | 0.726 | 90.566 |
| arima | post_covid | 30.034 | 142.255 | 16.442 | 0.641 | 77.358 |
| xgboost_nodemo | post_covid | 36.706 | 220.000 | 20.745 | 0.456 | 83.019 |
| xgboost | post_covid | 37.723 | 126.286 | 18.688 | 0.599 | 83.019 |
| dualtopo | post_covid | 38.118 | 119.929 | 22.724 | 0.443 | 30.189 |
| gat | post_covid | 38.417 | 84.893 | 20.599 | 0.642 | 64.151 |
| seasonal_naive | post_covid | 41.056 | 95.301 | 20.161 | 0.389 | 84.906 |
| lstm | post_covid | 42.388 | 72.824 | 20.550 | 0.402 | 86.792 |

### Flu season (Apr–Sep), 26 weeks scored, mean 46.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 38.576 | 81.458 | 24.872 | 0.624 | 65.385 |
| persistence | post_covid | 40.704 | 97.954 | 24.480 | 0.624 | 80.769 |
| arima | post_covid | 42.759 | 122.839 | 30.786 | 0.473 | 53.846 |
| xgboost_nodemo | post_covid | 51.630 | 74.339 | 34.412 | 0.272 | 65.385 |
| xgboost | post_covid | 53.605 | 57.254 | 33.726 | 0.468 | 65.385 |
| dualtopo | post_covid | 53.968 | 135.382 | 40.909 | 0.234 | 30.769 |
| gat | post_covid | 54.561 | 79.459 | 37.961 | 0.466 | 42.308 |
| seasonal_naive | post_covid | 58.446 | 69.056 | 37.784 | 0.115 | 69.231 |
| lstm | post_covid | 60.377 | 60.920 | 38.850 | -0.086 | 73.077 |

### Off-season (Oct–Mar), 27 weeks scored, mean 5.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3.170 | 160.952 | 2.629 | 0.737 | 100.000 |
| gnn_st | post_covid | 3.265 | 113.609 | 2.740 | 0.697 | 100.000 |
| persistence | post_covid | 3.470 | 133.979 | 2.862 | 0.703 | 100.000 |
| lstm | post_covid | 4.077 | 84.286 | 2.928 | 0.737 | 100.000 |
| seasonal_naive | post_covid | 4.395 | 120.575 | 3.190 | 0.437 | 100.000 |
| xgboost | post_covid | 5.133 | 192.760 | 4.206 | 0.380 | 100.000 |
| gat | post_covid | 5.516 | 90.126 | 3.879 | 0.237 | 85.185 |
| dualtopo | post_covid | 6.882 | 105.048 | 5.213 | -0.202 | 29.630 |
| xgboost_nodemo | post_covid | 8.824 | 360.267 | 7.584 | 0.543 | 100.000 |

## LA MATANZA

*mean observed 23.5, peak 53.2 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 23.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.581 | 21.359 | 5.492 | 0.839 | 100.000 |
| persistence | post_covid | 7.728 | 25.390 | 6.023 | 0.805 | 100.000 |
| arima | post_covid | 8.052 | 24.001 | 5.988 | 0.781 | 96.226 |
| xgboost_nodemo | post_covid | 9.403 | 36.807 | 7.483 | 0.714 | 100.000 |
| xgboost | post_covid | 9.812 | 28.635 | 7.149 | 0.736 | 100.000 |
| gat | post_covid | 10.557 | 41.324 | 9.071 | 0.897 | 100.000 |
| seasonal_naive | post_covid | 11.545 | 48.375 | 9.945 | 0.754 | 100.000 |
| lstm | post_covid | 13.638 | 47.876 | 11.319 | 0.752 | 100.000 |
| dualtopo | post_covid | 17.578 | 65.736 | 15.204 | 0.752 | 49.057 |

### Flu season (Apr–Sep), 26 weeks scored, mean 33.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.811 | 23.472 | 7.947 | 0.572 | 100.000 |
| persistence | post_covid | 10.187 | 29.770 | 9.022 | 0.497 | 100.000 |
| arima | post_covid | 10.663 | 27.402 | 8.978 | 0.483 | 92.308 |
| xgboost_nodemo | post_covid | 11.937 | 37.398 | 10.201 | 0.408 | 100.000 |
| gat | post_covid | 12.434 | 30.215 | 10.614 | 0.751 | 100.000 |
| xgboost | post_covid | 12.621 | 33.616 | 10.492 | 0.490 | 100.000 |
| seasonal_naive | post_covid | 13.062 | 37.986 | 11.282 | 0.559 | 100.000 |
| lstm | post_covid | 16.831 | 40.962 | 14.644 | 0.511 | 100.000 |
| dualtopo | post_covid | 21.914 | 56.474 | 19.768 | 0.444 | 50.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 4.157 | 21.173 | 3.136 | 0.494 | 100.000 |
| arima | post_covid | 4.216 | 20.726 | 3.109 | 0.484 | 100.000 |
| gnn_st | post_covid | 4.485 | 19.324 | 3.127 | 0.584 | 100.000 |
| xgboost | post_covid | 5.965 | 23.838 | 3.931 | 0.073 | 100.000 |
| xgboost_nodemo | post_covid | 6.028 | 36.239 | 4.866 | -0.027 | 100.000 |
| gat | post_covid | 8.360 | 52.022 | 7.584 | 0.648 | 100.000 |
| lstm | post_covid | 9.607 | 54.534 | 8.118 | 0.053 | 100.000 |
| seasonal_naive | post_covid | 9.866 | 58.379 | 8.658 | -0.021 | 100.000 |
| dualtopo | post_covid | 12.004 | 74.654 | 10.809 | 0.067 | 48.148 |

## QUILMES

*mean observed 21.4, peak 39.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.977 | 20.195 | 3.916 | 0.807 | 98.113 |
| arima | post_covid | 6.426 | 22.723 | 4.498 | 0.771 | 96.226 |
| persistence | post_covid | 6.643 | 23.814 | 4.686 | 0.760 | 98.113 |
| gat | post_covid | 6.806 | 24.913 | 4.994 | 0.790 | 100.000 |
| lstm | post_covid | 7.181 | 24.334 | 5.205 | 0.703 | 100.000 |
| xgboost | post_covid | 7.699 | 30.356 | 5.892 | 0.721 | 100.000 |
| seasonal_naive | post_covid | 8.571 | 29.645 | 6.536 | 0.630 | 100.000 |
| xgboost_nodemo | post_covid | 8.610 | 32.153 | 6.529 | 0.693 | 100.000 |
| dualtopo | post_covid | 9.194 | 49.633 | 8.033 | 0.493 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 28.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.239 | 15.832 | 3.763 | 0.628 | 100.000 |
| arima | post_covid | 5.249 | 16.753 | 4.342 | 0.603 | 100.000 |
| persistence | post_covid | 5.606 | 17.711 | 4.524 | 0.561 | 100.000 |
| gat | post_covid | 5.984 | 18.789 | 4.909 | 0.762 | 100.000 |
| lstm | post_covid | 7.655 | 20.257 | 6.101 | 0.196 | 100.000 |
| xgboost | post_covid | 8.152 | 25.046 | 6.510 | 0.379 | 100.000 |
| dualtopo | post_covid | 9.317 | 29.708 | 7.997 | 0.076 | 100.000 |
| xgboost_nodemo | post_covid | 9.643 | 28.435 | 7.608 | 0.368 | 100.000 |
| seasonal_naive | post_covid | 10.574 | 29.418 | 8.708 | 0.354 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 15.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 6.042 | 29.864 | 4.444 | 0.623 | 100.000 |
| gnn_st | post_covid | 6.610 | 24.396 | 4.062 | 0.566 | 96.296 |
| lstm | post_covid | 6.693 | 28.259 | 4.342 | 0.437 | 100.000 |
| xgboost | post_covid | 7.236 | 35.469 | 5.298 | 0.488 | 100.000 |
| arima | post_covid | 7.384 | 28.472 | 4.647 | 0.472 | 92.593 |
| xgboost_nodemo | post_covid | 7.482 | 35.733 | 5.491 | 0.459 | 100.000 |
| persistence | post_covid | 7.507 | 29.692 | 4.842 | 0.473 | 96.296 |
| gat | post_covid | 7.513 | 30.810 | 5.076 | 0.397 | 100.000 |
| dualtopo | post_covid | 9.074 | 68.821 | 8.067 | 0.276 | 100.000 |

## VICENTE LÓPEZ

*mean observed 21.4, peak 114.8 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 21.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.905 | 97.419 | 11.720 | 0.725 | 88.679 |
| persistence | post_covid | 18.026 | 76.156 | 11.390 | 0.642 | 88.679 |
| gat | post_covid | 23.031 | 162.526 | 18.851 | 0.674 | 100.000 |
| xgboost | post_covid | 28.237 | 190.249 | 22.910 | 0.690 | 96.226 |
| xgboost_nodemo | post_covid | 28.694 | 193.806 | 23.286 | 0.687 | 98.113 |
| arima | post_covid | 29.757 | 216.630 | 25.647 | 0.644 | 77.358 |
| lstm | post_covid | 47.919 | 348.759 | 42.135 | 0.518 | 92.453 |
| dualtopo | post_covid | 50.714 | 365.893 | 40.121 | -0.116 | 67.925 |
| seasonal_naive | post_covid | 56.458 | 318.031 | 41.996 | 0.690 | 84.906 |

### Flu season (Apr–Sep), 26 weeks scored, mean 32.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 24.478 | 124.516 | 17.785 | 0.610 | 76.923 |
| persistence | post_covid | 24.819 | 100.212 | 17.440 | 0.520 | 84.615 |
| gat | post_covid | 29.786 | 182.707 | 25.408 | 0.536 | 100.000 |
| arima | post_covid | 35.704 | 211.673 | 31.774 | 0.524 | 69.231 |
| xgboost | post_covid | 36.677 | 233.501 | 32.082 | 0.582 | 92.308 |
| xgboost_nodemo | post_covid | 37.547 | 240.536 | 33.237 | 0.581 | 96.154 |
| dualtopo | post_covid | 39.055 | 199.528 | 32.031 | -0.243 | 80.769 |
| lstm | post_covid | 60.799 | 386.355 | 56.537 | 0.205 | 84.615 |
| seasonal_naive | post_covid | 74.772 | 366.496 | 60.714 | 0.622 | 69.231 |

### Off-season (Oct–Mar), 27 weeks scored, mean 11.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 6.687 | 52.101 | 5.563 | 0.404 | 92.593 |
| gnn_st | post_covid | 7.233 | 70.323 | 5.880 | 0.622 | 100.000 |
| gat | post_covid | 13.670 | 142.345 | 12.536 | 0.716 | 100.000 |
| xgboost_nodemo | post_covid | 16.084 | 147.076 | 13.703 | 0.490 | 100.000 |
| xgboost | post_covid | 16.423 | 146.996 | 14.077 | 0.505 | 100.000 |
| arima | post_covid | 22.596 | 221.587 | 19.747 | 0.457 | 85.185 |
| seasonal_naive | post_covid | 29.549 | 269.567 | 23.971 | 0.291 | 100.000 |
| lstm | post_covid | 30.788 | 311.163 | 28.267 | 0.368 | 100.000 |
| dualtopo | post_covid | 59.831 | 532.257 | 47.911 | 0.238 | 55.556 |

## ALMIRANTE BROWN

*mean observed 19.6, peak 41.6 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.125 | 39.552 | 5.446 | 0.714 | 92.453 |
| gat | post_covid | 7.488 | 56.608 | 6.091 | 0.719 | 100.000 |
| persistence | post_covid | 7.993 | 45.051 | 6.233 | 0.606 | 94.340 |
| dualtopo | post_covid | 8.447 | 55.102 | 6.699 | 0.688 | 100.000 |
| arima | post_covid | 8.640 | 81.623 | 7.108 | 0.528 | 100.000 |
| xgboost | post_covid | 10.605 | 50.241 | 8.333 | 0.726 | 100.000 |
| lstm | post_covid | 11.486 | 64.037 | 9.793 | 0.624 | 100.000 |
| xgboost_nodemo | post_covid | 12.164 | 59.404 | 9.638 | 0.696 | 100.000 |
| seasonal_naive | post_covid | 13.236 | 61.022 | 10.627 | 0.690 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 25.4

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 6.512 | 21.575 | 5.306 | 0.358 | 100.000 |
| gnn_st | post_covid | 6.961 | 24.827 | 5.469 | 0.500 | 100.000 |
| gat | post_covid | 7.490 | 26.172 | 6.004 | 0.645 | 100.000 |
| persistence | post_covid | 7.864 | 27.289 | 6.557 | 0.337 | 100.000 |
| dualtopo | post_covid | 10.126 | 33.484 | 8.111 | 0.494 | 100.000 |
| lstm | post_covid | 12.990 | 51.785 | 11.534 | 0.227 | 100.000 |
| xgboost | post_covid | 13.280 | 48.318 | 10.909 | 0.480 | 100.000 |
| xgboost_nodemo | post_covid | 15.743 | 57.943 | 13.413 | 0.405 | 100.000 |
| seasonal_naive | post_covid | 16.082 | 51.663 | 12.857 | 0.576 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 14.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 6.427 | 75.920 | 5.340 | 0.431 | 100.000 |
| xgboost | post_covid | 7.139 | 52.093 | 5.852 | 0.437 | 100.000 |
| xgboost_nodemo | post_covid | 7.196 | 60.812 | 6.002 | 0.517 | 100.000 |
| gnn_st | post_covid | 7.279 | 53.732 | 5.424 | 0.389 | 85.185 |
| gat | post_covid | 7.485 | 85.915 | 6.175 | 0.147 | 100.000 |
| persistence | post_covid | 8.116 | 62.155 | 5.921 | 0.305 | 88.889 |
| seasonal_naive | post_covid | 9.737 | 70.034 | 8.480 | 0.258 | 100.000 |
| lstm | post_covid | 9.821 | 75.834 | 8.117 | 0.240 | 100.000 |
| arima | post_covid | 10.280 | 139.448 | 8.843 | 0.380 | 100.000 |

## MORÓN

*mean observed 19.1, peak 54.0 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 19.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 6.104 | 28.244 | 4.697 | 0.818 | 100.000 |
| gnn_st | post_covid | 7.134 | 29.594 | 5.105 | 0.740 | 96.226 |
| xgboost | post_covid | 7.328 | 40.567 | 5.996 | 0.751 | 100.000 |
| xgboost_nodemo | post_covid | 7.536 | 45.826 | 6.028 | 0.745 | 100.000 |
| arima | post_covid | 7.712 | 37.404 | 5.889 | 0.678 | 98.113 |
| gat | post_covid | 8.047 | 34.454 | 5.936 | 0.786 | 100.000 |
| persistence | post_covid | 8.322 | 35.716 | 5.800 | 0.678 | 96.226 |
| dualtopo | post_covid | 9.388 | 45.690 | 7.936 | 0.712 | 90.566 |
| seasonal_naive | post_covid | 14.587 | 51.899 | 9.691 | 0.720 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 7.251 | 24.328 | 5.424 | 0.707 | 100.000 |
| lstm | post_covid | 7.272 | 24.596 | 5.751 | 0.672 | 100.000 |
| gnn_st | post_covid | 8.339 | 24.976 | 6.224 | 0.557 | 100.000 |
| xgboost | post_covid | 8.528 | 29.837 | 6.710 | 0.683 | 100.000 |
| arima | post_covid | 9.201 | 26.978 | 7.045 | 0.472 | 96.154 |
| persistence | post_covid | 9.720 | 29.813 | 6.945 | 0.472 | 100.000 |
| gat | post_covid | 9.821 | 35.257 | 7.625 | 0.569 | 100.000 |
| dualtopo | post_covid | 10.519 | 36.280 | 9.161 | 0.357 | 100.000 |
| seasonal_naive | post_covid | 19.405 | 51.883 | 13.785 | 0.616 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 4.714 | 31.757 | 3.683 | 0.405 | 100.000 |
| gnn_st | post_covid | 5.739 | 34.040 | 4.027 | 0.255 | 92.593 |
| gat | post_covid | 5.851 | 33.680 | 4.309 | 0.343 | 100.000 |
| arima | post_covid | 5.935 | 47.444 | 4.777 | 0.207 | 100.000 |
| xgboost | post_covid | 5.949 | 50.899 | 5.309 | 0.264 | 100.000 |
| persistence | post_covid | 6.707 | 41.400 | 4.697 | 0.207 | 92.593 |
| seasonal_naive | post_covid | 7.424 | 51.915 | 5.748 | 0.031 | 100.000 |
| xgboost_nodemo | post_covid | 7.800 | 66.527 | 6.609 | 0.231 | 100.000 |
| dualtopo | post_covid | 8.151 | 54.752 | 6.756 | 0.302 | 81.481 |

## MERLO

*mean observed 17.9, peak 60.1 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 17.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 9.262 | 52.433 | 6.872 | 0.806 | 98.113 |
| persistence | post_covid | 10.751 | 53.822 | 7.551 | 0.703 | 96.226 |
| arima | post_covid | 12.039 | 127.044 | 10.188 | 0.741 | 98.113 |
| lstm | post_covid | 13.295 | 110.205 | 11.540 | 0.789 | 100.000 |
| xgboost_nodemo | post_covid | 16.728 | 91.289 | 12.131 | 0.801 | 100.000 |
| xgboost | post_covid | 19.711 | 118.218 | 14.780 | 0.802 | 100.000 |
| dualtopo | post_covid | 25.667 | 146.423 | 20.911 | 0.823 | 92.453 |
| seasonal_naive | post_covid | 26.507 | 241.783 | 20.679 | 0.234 | 100.000 |
| gat | post_covid | 35.836 | 173.209 | 27.114 | 0.790 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 26.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 11.517 | 45.018 | 8.915 | 0.616 | 96.154 |
| gnn_st | post_covid | 11.584 | 45.708 | 9.242 | 0.694 | 100.000 |
| persistence | post_covid | 13.354 | 37.288 | 10.004 | 0.572 | 100.000 |
| lstm | post_covid | 15.061 | 84.928 | 13.654 | 0.751 | 100.000 |
| xgboost_nodemo | post_covid | 22.720 | 77.199 | 17.915 | 0.697 | 100.000 |
| xgboost | post_covid | 26.483 | 94.466 | 21.555 | 0.701 | 100.000 |
| seasonal_naive | post_covid | 30.963 | 164.549 | 23.282 | -0.168 | 100.000 |
| dualtopo | post_covid | 34.776 | 139.820 | 32.203 | 0.829 | 96.154 |
| gat | post_covid | 49.752 | 200.407 | 45.375 | 0.679 | 100.000 |

### Off-season (Oct–Mar), 27 weeks scored, mean 9.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.260 | 59.158 | 4.590 | 0.396 | 96.296 |
| xgboost_nodemo | post_covid | 7.224 | 105.380 | 6.561 | 0.507 | 100.000 |
| persistence | post_covid | 7.427 | 70.356 | 5.188 | 0.366 | 92.593 |
| xgboost | post_covid | 9.340 | 141.970 | 8.256 | 0.486 | 100.000 |
| dualtopo | post_covid | 11.337 | 153.026 | 10.038 | -0.212 | 88.889 |
| lstm | post_covid | 11.338 | 135.482 | 9.504 | 0.605 | 100.000 |
| gat | post_covid | 11.716 | 146.010 | 9.529 | 0.214 | 100.000 |
| arima | post_covid | 12.521 | 209.070 | 11.414 | 0.433 | 100.000 |
| seasonal_naive | post_covid | 21.355 | 319.017 | 18.172 | -0.181 | 100.000 |

## TIGRE

*mean observed 8.0, peak 40.7 per 100,000 over the full year*

### Overall (full year), 53 weeks scored, mean 8.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.377 | 70.605 | 3.320 | 0.868 | 98.113 |
| persistence | post_covid | 6.028 | 56.663 | 3.390 | 0.834 | 98.113 |
| arima | post_covid | 6.118 | 67.004 | 3.637 | 0.839 | 90.566 |
| xgboost | post_covid | 6.803 | 233.356 | 5.753 | 0.824 | 100.000 |
| xgboost_nodemo | post_covid | 7.600 | 279.813 | 6.506 | 0.837 | 100.000 |
| lstm | post_covid | 8.541 | 178.157 | 6.331 | 0.599 | 100.000 |
| gat | post_covid | 8.773 | 90.202 | 5.232 | 0.659 | 73.585 |
| seasonal_naive | post_covid | 10.366 | 102.643 | 5.902 | 0.332 | 100.000 |
| dualtopo | post_covid | 13.559 | 272.377 | 9.556 | 0.227 | 96.226 |

### Flu season (Apr–Sep), 26 weeks scored, mean 14.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.517 | 74.325 | 5.684 | 0.794 | 96.154 |
| xgboost | post_covid | 8.229 | 98.525 | 6.727 | 0.743 | 100.000 |
| arima | post_covid | 8.411 | 60.768 | 5.997 | 0.780 | 88.462 |
| persistence | post_covid | 8.449 | 53.777 | 5.791 | 0.757 | 96.154 |
| xgboost_nodemo | post_covid | 8.874 | 135.271 | 7.304 | 0.761 | 100.000 |
| lstm | post_covid | 11.414 | 176.987 | 9.740 | 0.430 | 100.000 |
| gat | post_covid | 12.361 | 79.291 | 8.888 | 0.561 | 84.615 |
| seasonal_naive | post_covid | 14.669 | 100.571 | 10.464 | -0.031 | 100.000 |
| dualtopo | post_covid | 18.903 | 325.369 | 16.256 | -0.445 | 92.308 |

### Off-season (Oct–Mar), 27 weeks scored, mean 1.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 1.529 | 67.022 | 1.043 | 0.580 | 100.000 |
| persistence | post_covid | 1.612 | 59.443 | 1.077 | 0.508 | 100.000 |
| seasonal_naive | post_covid | 1.935 | 104.638 | 1.508 | -0.101 | 100.000 |
| gat | post_covid | 1.982 | 100.710 | 1.711 | 0.140 | 62.963 |
| arima | post_covid | 2.314 | 73.010 | 1.364 | 0.420 | 92.593 |
| dualtopo | post_covid | 4.095 | 221.347 | 3.104 | 0.079 | 100.000 |
| lstm | post_covid | 4.213 | 179.284 | 3.048 | 0.564 | 100.000 |
| xgboost | post_covid | 5.063 | 363.192 | 4.814 | 0.041 | 100.000 |
| xgboost_nodemo | post_covid | 6.128 | 419.002 | 5.737 | 0.226 | 100.000 |

## SAN ISIDRO

*mean observed 5.0, peak 29.9 per 100,000 over the full year*

### Overall (full year), 50 weeks scored, mean 5.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.912 | 378.614 | 4.656 | 0.488 | 94.000 |
| arima | post_covid | 7.189 | 336.808 | 4.563 | 0.359 | 88.000 |
| persistence | post_covid | 7.237 | 184.910 | 4.124 | 0.459 | 82.000 |
| gat | post_covid | 8.938 | 725.977 | 7.397 | 0.101 | 96.000 |
| xgboost | post_covid | 9.709 | 657.450 | 7.457 | 0.286 | 100.000 |
| xgboost_nodemo | post_covid | 9.888 | 754.343 | 7.340 | 0.209 | 100.000 |
| seasonal_naive | post_covid | 9.932 | 391.779 | 5.792 | 0.441 | 100.000 |
| lstm | post_covid | 10.440 | 890.163 | 7.782 | 0.367 | 100.000 |
| dualtopo | post_covid | 14.546 | 1454.528 | 12.892 | 0.647 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 2.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 3.508 | 161.575 | 2.174 | 0.201 | 100.000 |
| arima | post_covid | 8.188 | 549.943 | 4.881 | -0.219 | 84.615 |
| gnn_st | post_covid | 8.513 | 530.837 | 5.480 | -0.139 | 88.462 |
| persistence | post_covid | 8.804 | 267.808 | 4.709 | -0.091 | 73.077 |
| xgboost | post_covid | 9.638 | 930.763 | 7.460 | -0.438 | 100.000 |
| gat | post_covid | 10.098 | 1072.237 | 8.380 | 0.082 | 92.308 |
| xgboost_nodemo | post_covid | 10.902 | 1206.726 | 8.105 | -0.471 | 100.000 |
| lstm | post_covid | 11.143 | 1131.378 | 7.137 | -0.389 | 100.000 |
| dualtopo | post_covid | 15.814 | 1925.779 | 13.575 | -0.429 | 100.000 |

### Off-season (Oct–Mar), 24 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 4.584 | 233.010 | 3.764 | 0.896 | 100.000 |
| persistence | post_covid | 5.012 | 105.616 | 3.490 | 0.880 | 91.667 |
| arima | post_covid | 5.920 | 132.940 | 4.218 | 0.895 | 91.667 |
| gat | post_covid | 7.483 | 394.771 | 6.332 | 0.708 | 100.000 |
| xgboost_nodemo | post_covid | 8.657 | 321.628 | 6.512 | 0.487 | 100.000 |
| lstm | post_covid | 9.620 | 659.436 | 8.481 | 0.761 | 100.000 |
| xgboost | post_covid | 9.785 | 396.020 | 7.453 | 0.456 | 100.000 |
| dualtopo | post_covid | 13.034 | 1003.767 | 12.153 | 0.902 | 100.000 |
| seasonal_naive | post_covid | 13.863 | 611.975 | 9.713 | 0.357 | 100.000 |

## LOMAS DE ZAMORA

*mean observed 0.6, peak 1.6 per 100,000 over the full year*

### Overall (full year), 41 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.618 | 108.746 | 0.470 | 0.036 | 92.683 |
| arima | post_covid | 0.629 | 102.665 | 0.480 | -0.029 | 92.683 |
| gnn_st | post_covid | 1.394 | 371.984 | 1.160 | 0.040 | 100.000 |
| gat | post_covid | 3.195 | 907.711 | 2.924 | -0.044 | 100.000 |
| seasonal_naive | post_covid | 3.278 | 739.566 | 2.317 | -0.099 | 100.000 |
| lstm | post_covid | 3.666 | 1030.678 | 3.530 | 0.132 | 100.000 |
| xgboost | post_covid | 3.777 | 544.855 | 1.866 | -0.129 | 100.000 |
| dualtopo | post_covid | 3.824 | 1088.833 | 3.620 | 0.035 | 100.000 |
| xgboost_nodemo | post_covid | 4.184 | 866.933 | 2.216 | -0.291 | 100.000 |

### Flu season (Apr–Sep), 26 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0.647 | 74.535 | 0.462 | 0.030 | 92.308 |
| persistence | post_covid | 0.647 | 84.318 | 0.462 | 0.072 | 92.308 |
| gnn_st | post_covid | 1.622 | 454.251 | 1.410 | 0.002 | 100.000 |
| xgboost | post_covid | 3.578 | 356.185 | 1.558 | -0.071 | 100.000 |
| gat | post_covid | 3.686 | 1107.077 | 3.449 | -0.189 | 100.000 |
| seasonal_naive | post_covid | 3.846 | 994.581 | 2.791 | -0.178 | 100.000 |
| lstm | post_covid | 4.144 | 1211.871 | 4.087 | 0.052 | 100.000 |
| dualtopo | post_covid | 4.278 | 1296.531 | 4.125 | -0.076 | 100.000 |
| xgboost_nodemo | post_covid | 4.653 | 871.147 | 2.191 | -0.286 | 100.000 |

### Off-season (Oct–Mar), 15 weeks scored, mean 0.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 0.565 | 148.878 | 0.483 | -0.050 | 93.333 |
| arima | post_covid | 0.597 | 148.878 | 0.512 | -0.161 | 93.333 |
| gnn_st | post_covid | 0.867 | 236.830 | 0.726 | 0.110 | 100.000 |
| seasonal_naive | post_covid | 1.928 | 320.612 | 1.497 | 0.183 | 100.000 |
| gat | post_covid | 2.086 | 580.180 | 2.013 | 0.382 | 100.000 |
| lstm | post_covid | 2.640 | 733.003 | 2.564 | 0.390 | 100.000 |
| dualtopo | post_covid | 2.872 | 747.614 | 2.743 | 0.256 | 100.000 |
| xgboost_nodemo | post_covid | 3.212 | 860.009 | 2.259 | -0.313 | 100.000 |
| xgboost | post_covid | 4.100 | 854.813 | 2.402 | -0.240 | 100.000 |

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost, xgboost_nodemo; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
