# Rolling-origin backtest

Does the ranking hold on seasons the design never saw? Each fold trains on
everything before its test season (variant `post_covid`, validation taken just
before the test window) and forecasts one full season. Folds 2024_25 are the evidence; 2025_26 is the season the design was chosen on and is shown for reference only.

MAE and WIS are in rate per 100,000 (lower is better); Corr is the mean over
neighborhoods of the week-to-week correlation (higher is better).

## Horizon 1

### MAE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| transfer_zeroshot_from_boston |     5.936 |     5.245 |           5.936 |
| gnn_st_tuned                  |     6.025 |   nan     |           6.025 |
| gnn_st                        |     6.066 |     5.02  |           6.066 |
| transfer_finetune_from_boston |     6.093 |     5.065 |           6.093 |
| gnn_st_noadapt                |     6.107 |     5.067 |           6.107 |
| gnn_st_nograph                |     6.588 |     5.612 |           6.588 |
| xgboost_parity                |     6.884 |     5.633 |           6.884 |
| lstm_parity                   |     6.91  |     5.766 |           6.91  |
| lstm_tuned                    |     6.945 |   nan     |           6.945 |
| gnn_st_nograph_tuned          |     7.038 |   nan     |           7.038 |
| flusight_baseline             |     7.283 |     6.188 |           7.283 |
| persistence                   |     7.283 |     6.188 |           7.283 |
| blend_baseline                |     7.658 |     5.805 |           7.658 |
| sarima                        |     7.689 |     6.18  |           7.689 |
| colagnn_tuned                 |     7.993 |   nan     |           7.993 |
| arima                         |     8.625 |     6.002 |           8.625 |
| seasonal_naive                |     9.044 |     9.093 |           9.044 |
| xgboost                       |     9.627 |     6.635 |           9.627 |
| xgboost_tuned                 |     9.66  |   nan     |           9.66  |
| dualtopo_tuned                |     9.849 |   nan     |           9.849 |
| gat_parity                    |     9.987 |     6.723 |           9.987 |
| gat_tuned                     |     9.989 |   nan     |           9.989 |
| lstm_s10                      |    10.35  |     5.464 |          10.35  |
| climatology                   |    10.551 |     8.083 |          10.551 |
| lstm                          |    10.76  |     5.465 |          10.76  |

### WIS

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| transfer_zeroshot_from_boston |     3.9   |     3.64  |           3.9   |
| gnn_st_tuned                  |     4.062 |   nan     |           4.062 |
| gnn_st                        |     4.094 |     3.31  |           4.094 |
| transfer_finetune_from_boston |     4.101 |     3.416 |           4.101 |
| gnn_st_noadapt                |     4.108 |     3.338 |           4.108 |
| gnn_st_nograph                |     4.405 |     3.698 |           4.405 |
| lstm_parity                   |     4.643 |     3.816 |           4.643 |
| xgboost_parity                |     4.647 |     3.749 |           4.647 |
| persistence                   |     4.667 |     4.033 |           4.667 |
| gnn_st_nograph_tuned          |     4.705 |   nan     |           4.705 |
| flusight_baseline             |     4.844 |     4.025 |           4.844 |
| blend_baseline                |     5.047 |     3.791 |           5.047 |
| lstm_tuned                    |     5.13  |   nan     |           5.13  |
| sarima                        |     5.551 |     3.995 |           5.551 |
| seasonal_naive                |     5.748 |     9.123 |           5.748 |
| colagnn_tuned                 |     6.027 |   nan     |           6.027 |
| arima                         |     6.468 |     3.914 |           6.468 |
| climatology                   |     6.748 |     5.206 |           6.748 |
| xgboost                       |     6.915 |     4.954 |           6.915 |
| xgboost_tuned                 |     6.963 |   nan     |           6.963 |
| gat_tuned                     |     7.106 |   nan     |           7.106 |
| gat_parity                    |     7.311 |     4.229 |           7.311 |
| lstm_s10                      |     8.529 |     3.799 |           8.529 |
| dualtopo_tuned                |     8.709 |   nan     |           8.709 |
| lstm                          |     8.805 |     3.841 |           8.805 |

### RMSE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| transfer_zeroshot_from_boston |     9.321 |     7.718 |           9.321 |
| gnn_st_tuned                  |    10.17  |   nan     |          10.17  |
| gnn_st                        |    10.274 |     7.398 |          10.274 |
| gnn_st_noadapt                |    10.333 |     7.475 |          10.333 |
| transfer_finetune_from_boston |    10.438 |     7.506 |          10.438 |
| flusight_baseline             |    10.982 |     9.195 |          10.982 |
| persistence                   |    10.982 |     9.195 |          10.982 |
| lstm_parity                   |    11.104 |     8.54  |          11.104 |
| gnn_st_nograph                |    11.189 |     8.408 |          11.189 |
| xgboost_parity                |    12.038 |     8.613 |          12.038 |
| gnn_st_nograph_tuned          |    12.408 |   nan     |          12.408 |
| lstm_tuned                    |    12.632 |   nan     |          12.632 |
| blend_baseline                |    13.73  |     8.625 |          13.73  |
| sarima                        |    14.345 |     9.133 |          14.345 |
| colagnn_tuned                 |    15.401 |   nan     |          15.401 |
| arima                         |    15.69  |     9.022 |          15.69  |
| seasonal_naive                |    15.834 |    16.366 |          15.834 |
| gat_tuned                     |    16.709 |   nan     |          16.709 |
| gat_parity                    |    17.03  |    10.374 |          17.03  |
| dualtopo_tuned                |    18.774 |   nan     |          18.774 |
| xgboost                       |    18.866 |    10.163 |          18.866 |
| xgboost_tuned                 |    18.945 |   nan     |          18.945 |
| lstm_s10                      |    19.158 |     7.915 |          19.158 |
| lstm                          |    19.746 |     7.905 |          19.746 |
| climatology                   |    19.781 |    12.21  |          19.781 |

### Corr

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| transfer_zeroshot_from_boston |     0.84  |     0.806 |           0.84  |
| transfer_finetune_from_boston |     0.834 |     0.814 |           0.834 |
| gnn_st_tuned                  |     0.834 |   nan     |           0.834 |
| gnn_st                        |     0.832 |     0.808 |           0.832 |
| gnn_st_noadapt                |     0.829 |     0.806 |           0.829 |
| gnn_st_nograph                |     0.814 |     0.757 |           0.814 |
| gnn_st_nograph_tuned          |     0.81  |   nan     |           0.81  |
| xgboost_parity                |     0.808 |     0.784 |           0.808 |
| lstm_tuned                    |     0.806 |   nan     |           0.806 |
| blend_baseline                |     0.8   |     0.751 |           0.8   |
| persistence                   |     0.786 |     0.737 |           0.786 |
| flusight_baseline             |     0.786 |     0.737 |           0.786 |
| lstm_parity                   |     0.783 |     0.754 |           0.783 |
| gat_tuned                     |     0.775 |   nan     |           0.775 |
| colagnn_tuned                 |     0.77  |   nan     |           0.77  |
| gat_parity                    |     0.759 |     0.684 |           0.759 |
| lstm_s10                      |     0.755 |     0.8   |           0.755 |
| dualtopo_tuned                |     0.724 |   nan     |           0.724 |
| sarima                        |     0.722 |     0.734 |           0.722 |
| lstm                          |     0.693 |     0.801 |           0.693 |
| seasonal_naive                |     0.649 |     0.561 |           0.649 |
| xgboost                       |     0.6   |     0.722 |           0.6   |
| xgboost_tuned                 |     0.598 |   nan     |           0.598 |
| climatology                   |     0.586 |     0.678 |           0.586 |
| arima                         |     0.585 |     0.73  |           0.585 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 1 of 1 |
| blend_baseline | 1 of 1 |
| climatology | 1 of 1 |
| colagnn_tuned | 1 of 1 |
| dualtopo_tuned | 1 of 1 |
| flusight_baseline | 1 of 1 |
| gat_parity | 1 of 1 |
| gat_tuned | 1 of 1 |
| gnn_st_noadapt | 1 of 1 |
| gnn_st_nograph | 1 of 1 |
| gnn_st_nograph_tuned | 1 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 1 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 1 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| transfer_finetune_from_boston | 1 of 1 |
| transfer_zeroshot_from_boston | 0 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 1 of 1 |
| xgboost_tuned | 1 of 1 |

## Horizon 2

### MAE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| gnn_st_tuned                  |     7.321 |   nan     |           7.321 |
| transfer_finetune_from_boston |     7.417 |     5.947 |           7.417 |
| gnn_st                        |     7.426 |     5.953 |           7.426 |
| transfer_zeroshot_from_boston |     7.493 |     6.256 |           7.493 |
| gnn_st_noadapt                |     7.504 |     5.8   |           7.504 |
| gnn_st_nograph                |     7.636 |     6.619 |           7.636 |
| gnn_st_nograph_tuned          |     7.646 |   nan     |           7.646 |
| xgboost_tuned                 |     7.671 |   nan     |           7.671 |
| xgboost_parity                |     7.734 |     6.323 |           7.734 |
| sarima                        |     8.001 |     7.216 |           8.001 |
| lstm_parity                   |     8.07  |     6.799 |           8.07  |
| blend_baseline                |     8.375 |     6.671 |           8.375 |
| colagnn_tuned                 |     8.55  |   nan     |           8.55  |
| lstm_tuned                    |     8.603 |   nan     |           8.603 |
| persistence                   |     8.802 |     7.671 |           8.802 |
| flusight_baseline             |     8.802 |     7.671 |           8.802 |
| seasonal_naive                |     9.044 |     9.093 |           9.044 |
| xgboost                       |     9.647 |     7.031 |           9.647 |
| arima                         |    10.125 |     7.176 |          10.125 |
| climatology                   |    10.551 |     8.083 |          10.551 |
| lstm_s10                      |    10.713 |     6.666 |          10.713 |
| lstm                          |    10.882 |     6.734 |          10.882 |

### WIS

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| gnn_st_tuned                  |     5.028 |   nan     |           5.028 |
| transfer_zeroshot_from_boston |     5.076 |     4.601 |           5.076 |
| transfer_finetune_from_boston |     5.094 |     4.028 |           5.094 |
| gnn_st                        |     5.138 |     3.956 |           5.138 |
| gnn_st_noadapt                |     5.182 |     3.863 |           5.182 |
| gnn_st_nograph                |     5.294 |     4.361 |           5.294 |
| gnn_st_nograph_tuned          |     5.373 |   nan     |           5.373 |
| xgboost_tuned                 |     5.468 |   nan     |           5.468 |
| xgboost_parity                |     5.529 |     4.265 |           5.529 |
| blend_baseline                |     5.684 |     4.354 |           5.684 |
| lstm_parity                   |     5.694 |     4.558 |           5.694 |
| seasonal_naive                |     5.748 |     9.123 |           5.748 |
| sarima                        |     5.841 |     4.758 |           5.841 |
| persistence                   |     5.894 |     4.963 |           5.894 |
| flusight_baseline             |     6.096 |     5.049 |           6.096 |
| climatology                   |     6.748 |     5.206 |           6.748 |
| colagnn_tuned                 |     6.755 |   nan     |           6.755 |
| xgboost                       |     6.93  |     5.075 |           6.93  |
| lstm_tuned                    |     7.126 |   nan     |           7.126 |
| arima                         |     8.194 |     4.724 |           8.194 |
| lstm_s10                      |     8.826 |     4.529 |           8.826 |
| lstm                          |     8.996 |     4.532 |           8.996 |

### RMSE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| transfer_zeroshot_from_boston |    12.91  |     9.2   |          12.91  |
| gnn_st_tuned                  |    13.207 |   nan     |          13.207 |
| gnn_st                        |    13.381 |     8.874 |          13.381 |
| transfer_finetune_from_boston |    13.46  |     9.043 |          13.46  |
| gnn_st_noadapt                |    13.535 |     8.691 |          13.535 |
| gnn_st_nograph                |    13.783 |     9.969 |          13.783 |
| lstm_parity                   |    14.323 |    10.209 |          14.323 |
| gnn_st_nograph_tuned          |    14.415 |   nan     |          14.415 |
| xgboost_tuned                 |    14.47  |   nan     |          14.47  |
| xgboost_parity                |    14.587 |     9.857 |          14.587 |
| persistence                   |    14.59  |    11.499 |          14.59  |
| flusight_baseline             |    14.59  |    11.499 |          14.59  |
| sarima                        |    15.054 |    10.681 |          15.054 |
| blend_baseline                |    15.773 |    10.106 |          15.773 |
| seasonal_naive                |    15.834 |    16.366 |          15.834 |
| colagnn_tuned                 |    16.294 |   nan     |          16.294 |
| lstm_tuned                    |    16.364 |   nan     |          16.364 |
| xgboost                       |    18.896 |    10.771 |          18.896 |
| arima                         |    19.014 |    10.952 |          19.014 |
| lstm_s10                      |    19.714 |     9.716 |          19.714 |
| climatology                   |    19.781 |    12.21  |          19.781 |
| lstm                          |    19.953 |     9.823 |          19.953 |

### Corr

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| xgboost_tuned                 |     0.747 |   nan     |           0.747 |
| gnn_st_nograph_tuned          |     0.745 |   nan     |           0.745 |
| gnn_st_tuned                  |     0.742 |   nan     |           0.742 |
| xgboost_parity                |     0.74  |     0.714 |           0.74  |
| blend_baseline                |     0.74  |     0.647 |           0.74  |
| transfer_zeroshot_from_boston |     0.739 |     0.736 |           0.739 |
| transfer_finetune_from_boston |     0.735 |     0.738 |           0.735 |
| gnn_st                        |     0.732 |     0.718 |           0.732 |
| gnn_st_noadapt                |     0.728 |     0.734 |           0.728 |
| gnn_st_nograph                |     0.723 |     0.646 |           0.723 |
| lstm_tuned                    |     0.713 |   nan     |           0.713 |
| colagnn_tuned                 |     0.703 |   nan     |           0.703 |
| lstm_s10                      |     0.703 |     0.691 |           0.703 |
| flusight_baseline             |     0.689 |     0.597 |           0.689 |
| persistence                   |     0.689 |     0.597 |           0.689 |
| sarima                        |     0.684 |     0.635 |           0.684 |
| lstm_parity                   |     0.68  |     0.634 |           0.68  |
| seasonal_naive                |     0.649 |     0.561 |           0.649 |
| lstm                          |     0.648 |     0.686 |           0.648 |
| xgboost                       |     0.602 |     0.685 |           0.602 |
| climatology                   |     0.586 |     0.678 |           0.586 |
| arima                         |     0.538 |     0.598 |           0.538 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 1 of 1 |
| blend_baseline | 1 of 1 |
| climatology | 1 of 1 |
| colagnn_tuned | 1 of 1 |
| flusight_baseline | 1 of 1 |
| gnn_st_noadapt | 1 of 1 |
| gnn_st_nograph | 1 of 1 |
| gnn_st_nograph_tuned | 1 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 1 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 1 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| transfer_finetune_from_boston | 0 of 1 |
| transfer_zeroshot_from_boston | 1 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 1 of 1 |
| xgboost_tuned | 1 of 1 |

## Horizon 4

### MAE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| gnn_st_tuned                  |     8.618 |   nan     |           8.618 |
| xgboost_tuned                 |     8.698 |   nan     |           8.698 |
| xgboost_parity                |     8.706 |     6.792 |           8.706 |
| gnn_st_nograph_tuned          |     8.71  |   nan     |           8.71  |
| lstm_tuned                    |     8.782 |   nan     |           8.782 |
| gnn_st                        |     8.797 |     6.472 |           8.797 |
| gnn_st_noadapt                |     8.834 |     6.241 |           8.834 |
| gnn_st_nograph                |     8.836 |     6.89  |           8.836 |
| sarima                        |     8.851 |     7.486 |           8.851 |
| transfer_finetune_from_boston |     8.87  |     6.092 |           8.87  |
| lstm_parity                   |     8.92  |     7.257 |           8.92  |
| colagnn_tuned                 |     9.026 |   nan     |           9.026 |
| seasonal_naive                |     9.044 |     9.093 |           9.044 |
| transfer_zeroshot_from_boston |     9.045 |     7.555 |           9.045 |
| blend_baseline                |     9.102 |     7.286 |           9.102 |
| xgboost                       |     9.507 |     6.866 |           9.507 |
| climatology                   |    10.551 |     8.083 |          10.551 |
| lstm_s10                      |    11.404 |     8.106 |          11.404 |
| flusight_baseline             |    11.418 |     9.836 |          11.418 |
| persistence                   |    11.418 |     9.836 |          11.418 |
| arima                         |    11.569 |     8.261 |          11.569 |
| lstm                          |    11.702 |     8.088 |          11.702 |

### WIS

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| seasonal_naive                |     5.748 |     9.123 |           5.748 |
| gnn_st_tuned                  |     6.312 |   nan     |           6.312 |
| gnn_st_nograph_tuned          |     6.391 |   nan     |           6.391 |
| gnn_st_nograph                |     6.426 |     4.739 |           6.426 |
| blend_baseline                |     6.445 |     4.818 |           6.445 |
| transfer_zeroshot_from_boston |     6.454 |     5.875 |           6.454 |
| gnn_st                        |     6.474 |     4.44  |           6.474 |
| transfer_finetune_from_boston |     6.491 |     4.531 |           6.491 |
| gnn_st_noadapt                |     6.494 |     4.258 |           6.494 |
| sarima                        |     6.502 |     5.527 |           6.502 |
| lstm_tuned                    |     6.57  |   nan     |           6.57  |
| xgboost_tuned                 |     6.595 |   nan     |           6.595 |
| xgboost_parity                |     6.613 |     5.2   |           6.613 |
| lstm_parity                   |     6.694 |     5.041 |           6.694 |
| climatology                   |     6.748 |     5.206 |           6.748 |
| xgboost                       |     6.907 |     5.959 |           6.907 |
| colagnn_tuned                 |     7.116 |   nan     |           7.116 |
| flusight_baseline             |     8.196 |     6.422 |           8.196 |
| persistence                   |     8.451 |     6.264 |           8.451 |
| arima                         |     9.314 |     5.661 |           9.314 |
| lstm_s10                      |     9.358 |     5.533 |           9.358 |
| lstm                          |     9.518 |     5.51  |           9.518 |

### RMSE

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| seasonal_naive                |    15.834 |    16.366 |          15.834 |
| gnn_st_tuned                  |    16.816 |   nan     |          16.816 |
| gnn_st                        |    16.832 |     9.902 |          16.832 |
| lstm_tuned                    |    16.853 |   nan     |          16.853 |
| transfer_finetune_from_boston |    16.873 |     9.029 |          16.873 |
| gnn_st_noadapt                |    16.905 |     9.468 |          16.905 |
| transfer_zeroshot_from_boston |    16.911 |    11.048 |          16.911 |
| sarima                        |    17.038 |    10.868 |          17.038 |
| gnn_st_nograph                |    17.041 |    10.669 |          17.041 |
| lstm_parity                   |    17.169 |    11.25  |          17.169 |
| gnn_st_nograph_tuned          |    17.228 |   nan     |          17.228 |
| colagnn_tuned                 |    17.239 |   nan     |          17.239 |
| xgboost_tuned                 |    17.342 |   nan     |          17.342 |
| xgboost_parity                |    17.363 |    10.514 |          17.363 |
| blend_baseline                |    17.62  |    11.353 |          17.62  |
| xgboost                       |    18.49  |    10.495 |          18.49  |
| climatology                   |    19.781 |    12.21  |          19.781 |
| persistence                   |    20.192 |    14.56  |          20.192 |
| flusight_baseline             |    20.192 |    14.56  |          20.192 |
| lstm_s10                      |    20.852 |    12.139 |          20.852 |
| lstm                          |    21.286 |    12.129 |          21.286 |
| arima                         |    21.4   |    12.599 |          21.4   |

### Corr

| arm                           |   2024_25 |   2025_26 |   evidence mean |
|:------------------------------|----------:|----------:|----------------:|
| seasonal_naive                |     0.649 |     0.561 |           0.649 |
| xgboost_tuned                 |     0.647 |   nan     |           0.647 |
| colagnn_tuned                 |     0.645 |   nan     |           0.645 |
| xgboost_parity                |     0.644 |     0.688 |           0.644 |
| blend_baseline                |     0.64  |     0.564 |           0.64  |
| gnn_st_nograph_tuned          |     0.639 |   nan     |           0.639 |
| gnn_st_tuned                  |     0.617 |   nan     |           0.617 |
| xgboost                       |     0.601 |     0.695 |           0.601 |
| gnn_st                        |     0.589 |     0.704 |           0.589 |
| transfer_finetune_from_boston |     0.588 |     0.755 |           0.588 |
| gnn_st_nograph                |     0.588 |     0.604 |           0.588 |
| climatology                   |     0.586 |     0.678 |           0.586 |
| gnn_st_noadapt                |     0.585 |     0.725 |           0.585 |
| lstm_s10                      |     0.584 |     0.481 |           0.584 |
| transfer_zeroshot_from_boston |     0.578 |     0.628 |           0.578 |
| lstm_tuned                    |     0.569 |   nan     |           0.569 |
| lstm_parity                   |     0.562 |     0.567 |           0.562 |
| sarima                        |     0.534 |     0.61  |           0.534 |
| persistence                   |     0.466 |     0.39  |           0.466 |
| flusight_baseline             |     0.466 |     0.39  |           0.466 |
| lstm                          |     0.403 |     0.485 |           0.403 |
| arima                         |     0.225 |     0.398 |           0.225 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 1 of 1 |
| blend_baseline | 1 of 1 |
| climatology | 1 of 1 |
| colagnn_tuned | 1 of 1 |
| flusight_baseline | 1 of 1 |
| gnn_st_noadapt | 1 of 1 |
| gnn_st_nograph | 1 of 1 |
| gnn_st_nograph_tuned | 0 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 1 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 0 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| transfer_finetune_from_boston | 1 of 1 |
| transfer_zeroshot_from_boston | 1 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 0 of 1 |
| xgboost_tuned | 0 of 1 |

Per-fold significance (block bootstrap and Diebold-Mariano) is in each fold's
`_comparison/significance.md`, written by compare_significance.py.
