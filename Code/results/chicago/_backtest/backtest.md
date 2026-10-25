# Rolling-origin backtest

Does the ranking hold on seasons the design never saw? Each fold trains on
everything before its test season (variant `full`, validation taken just
before the test window) and forecasts one full season. Folds 2022_23, 2023_24, 2024_25, 2025_26 are the evidence; no season of this city was used to choose anything, so none is held out.

MAE and WIS are in ILI activity levels, 1-10 (lower is better); Corr is the mean over
neighborhoods of the week-to-week correlation (higher is better).

## Horizon 1

### MAE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| gnn_st_noadapt                       |   nan     |   nan     |     1.622 |     1.55  |           1.586 |
| transfer_finetune_from_boston        |   nan     |   nan     |     1.627 |     1.558 |           1.592 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.613 |   nan     |           1.613 |
| gnn_st_noweather_tuned               |     1.73  |     1.612 |     1.614 |     1.495 |           1.613 |
| gnn_st_nodemofeat_tuned              |     1.722 |     1.62  |     1.608 |     1.508 |           1.614 |
| gnn_st                               |     1.729 |     1.624 |     1.614 |     1.522 |           1.622 |
| gnn_st_tuned                         |     1.729 |     1.626 |     1.614 |     1.522 |           1.623 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.623 |   nan     |           1.623 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     1.656 |   nan     |           1.656 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     1.737 |     1.625 |           1.681 |
| gnn_st_nograph_tuned                 |     1.814 |     1.706 |     1.741 |     1.645 |           1.727 |
| gnn_st_historyonly_tuned             |     1.839 |     1.703 |     1.783 |     1.641 |           1.741 |
| gnn_st_nograph                       |     1.84  |     1.714 |     1.766 |     1.658 |           1.744 |
| lstm_tuned                           |     1.879 |     1.723 |     1.778 |     1.605 |           1.746 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     1.756 |   nan     |           1.756 |
| lstm_s10                             |     1.905 |     1.746 |     1.778 |     1.64  |           1.767 |
| colagnn_tuned                        |     2.07  |     1.688 |     1.739 |     1.584 |           1.77  |
| lstm                                 |     1.895 |     1.782 |     1.765 |     1.662 |           1.776 |
| xgboost_parity                       |     1.892 |     1.732 |     1.859 |     1.716 |           1.8   |
| xgboost_tuned                        |     1.92  |     1.734 |     1.875 |     1.713 |           1.81  |
| sarima                               |     1.918 |     1.765 |     1.918 |     1.703 |           1.826 |
| blend_baseline                       |     1.98  |     1.767 |     1.999 |     1.675 |           1.855 |
| gat_parity                           |     2.257 |     1.806 |     1.746 |     1.626 |           1.859 |
| gat_tuned                            |     2.301 |     1.806 |     1.721 |     1.622 |           1.862 |
| xgboost                              |     2.076 |     1.778 |     1.877 |     1.743 |           1.868 |
| persistence                          |     1.929 |     1.922 |     1.864 |     1.782 |           1.874 |
| flusight_baseline                    |     1.929 |     1.922 |     1.864 |     1.782 |           1.874 |
| arima                                |     1.961 |     1.873 |     1.939 |     1.769 |           1.886 |
| lstm_parity                          |     2     |     1.918 |     2.017 |     1.792 |           1.932 |
| dualtopo_tuned                       |     2.434 |     2.16  |     1.842 |     1.673 |           2.027 |
| climatology                          |     2.358 |     1.968 |     2.412 |     1.877 |           2.154 |
| seasonal_naive                       |     2.422 |     2.293 |     2.323 |     1.963 |           2.25  |

### WIS

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     1.084 |     1.006 |           1.045 |
| gnn_st_noadapt                       |   nan     |   nan     |     1.086 |     1.005 |           1.046 |
| gnn_st_noweather_tuned               |     1.15  |     1.085 |     1.081 |     0.993 |           1.077 |
| gnn_st_tuned                         |     1.161 |     1.085 |     1.087 |     1.001 |           1.083 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.085 |   nan     |           1.085 |
| gnn_st_nodemofeat_tuned              |     1.16  |     1.089 |     1.091 |     0.999 |           1.085 |
| gnn_st                               |     1.161 |     1.09  |     1.087 |     1.001 |           1.085 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.085 |   nan     |           1.085 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     1.097 |   nan     |           1.097 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     1.16  |     1.066 |           1.113 |
| lstm_tuned                           |     1.222 |     1.127 |     1.15  |     1.039 |           1.135 |
| lstm_s10                             |     1.233 |     1.116 |     1.15  |     1.056 |           1.139 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     1.14  |   nan     |           1.14  |
| lstm                                 |     1.229 |     1.125 |     1.143 |     1.074 |           1.143 |
| colagnn_tuned                        |     1.331 |     1.104 |     1.12  |     1.017 |           1.143 |
| gnn_st_nograph                       |     1.258 |     1.144 |     1.171 |     1.079 |           1.163 |
| gnn_st_nograph_tuned                 |     1.267 |     1.142 |     1.163 |     1.082 |           1.163 |
| gnn_st_historyonly_tuned             |     1.292 |     1.146 |     1.176 |     1.081 |           1.174 |
| xgboost_parity                       |     1.283 |     1.139 |     1.206 |     1.108 |           1.184 |
| xgboost_tuned                        |     1.291 |     1.143 |     1.214 |     1.107 |           1.189 |
| gat_parity                           |     1.457 |     1.164 |     1.128 |     1.073 |           1.205 |
| sarima                               |     1.308 |     1.171 |     1.245 |     1.098 |           1.206 |
| gat_tuned                            |     1.494 |     1.164 |     1.12  |     1.069 |           1.212 |
| xgboost                              |     1.396 |     1.163 |     1.217 |     1.122 |           1.224 |
| arima                                |     1.334 |     1.218 |     1.249 |     1.134 |           1.234 |
| blend_baseline                       |     1.366 |     1.18  |     1.284 |     1.149 |           1.245 |
| lstm_parity                          |     1.382 |     1.277 |     1.311 |     1.219 |           1.297 |
| dualtopo_tuned                       |     1.588 |     1.435 |     1.177 |     1.111 |           1.328 |
| flusight_baseline                    |     1.398 |     1.352 |     1.326 |     1.238 |           1.328 |
| persistence                          |     1.44  |     1.332 |     1.355 |     1.25  |           1.344 |
| climatology                          |     1.694 |     1.277 |     1.508 |     1.262 |           1.435 |
| seasonal_naive                       |     1.764 |     1.633 |     1.573 |     1.47  |           1.61  |

### RMSE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     2.312 |     2.126 |           2.219 |
| gnn_st_noadapt                       |   nan     |   nan     |     2.325 |     2.127 |           2.226 |
| gnn_st_noweather_tuned               |     2.411 |     2.32  |     2.308 |     2.122 |           2.29  |
| gnn_st_tuned                         |     2.442 |     2.322 |     2.331 |     2.13  |           2.306 |
| gnn_st                               |     2.442 |     2.331 |     2.331 |     2.13  |           2.308 |
| gnn_st_nodemofeat_tuned              |     2.449 |     2.332 |     2.343 |     2.125 |           2.312 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     2.313 |   nan     |           2.313 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     2.317 |   nan     |           2.317 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     2.319 |   nan     |           2.319 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     2.47  |     2.216 |           2.343 |
| lstm_tuned                           |     2.518 |     2.426 |     2.403 |     2.164 |           2.378 |
| colagnn_tuned                        |     2.744 |     2.33  |     2.313 |     2.131 |           2.38  |
| lstm_s10                             |     2.524 |     2.414 |     2.403 |     2.188 |           2.382 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     2.384 |   nan     |           2.384 |
| lstm                                 |     2.556 |     2.458 |     2.393 |     2.216 |           2.406 |
| gnn_st_nograph                       |     2.659 |     2.442 |     2.512 |     2.26  |           2.468 |
| xgboost_parity                       |     2.661 |     2.407 |     2.529 |     2.284 |           2.47  |
| xgboost_tuned                        |     2.685 |     2.41  |     2.536 |     2.283 |           2.478 |
| gnn_st_nograph_tuned                 |     2.702 |     2.426 |     2.507 |     2.299 |           2.484 |
| gnn_st_historyonly_tuned             |     2.744 |     2.453 |     2.516 |     2.258 |           2.493 |
| gat_parity                           |     2.97  |     2.45  |     2.354 |     2.243 |           2.504 |
| gat_tuned                            |     3.041 |     2.45  |     2.343 |     2.255 |           2.522 |
| sarima                               |     2.738 |     2.504 |     2.595 |     2.266 |           2.526 |
| xgboost                              |     2.873 |     2.418 |     2.543 |     2.301 |           2.534 |
| arima                                |     2.761 |     2.599 |     2.602 |     2.348 |           2.577 |
| blend_baseline                       |     2.754 |     2.544 |     2.766 |     2.403 |           2.617 |
| dualtopo_tuned                       |     3.348 |     2.899 |     2.422 |     2.276 |           2.736 |
| lstm_parity                          |     2.918 |     2.807 |     2.8   |     2.573 |           2.775 |
| persistence                          |     3.11  |     2.983 |     3.041 |     2.805 |           2.985 |
| flusight_baseline                    |     3.11  |     2.983 |     3.041 |     2.805 |           2.985 |
| climatology                          |     3.311 |     2.865 |     3.458 |     2.683 |           3.079 |
| seasonal_naive                       |     3.703 |     3.415 |     3.463 |     3.094 |           3.419 |

### Corr

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_pooled_others |   nan     |   nan     |     0.669 |   nan     |           0.669 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     0.668 |   nan     |           0.668 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     0.668 |   nan     |           0.668 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     0.662 |   nan     |           0.662 |
| transfer_finetune_from_boston        |   nan     |   nan     |     0.669 |     0.614 |           0.641 |
| gnn_st_noadapt                       |   nan     |   nan     |     0.666 |     0.613 |           0.639 |
| lstm_tuned                           |     0.608 |     0.564 |     0.683 |     0.635 |           0.622 |
| lstm_s10                             |     0.599 |     0.577 |     0.683 |     0.627 |           0.621 |
| lstm                                 |     0.586 |     0.568 |     0.677 |     0.619 |           0.612 |
| gnn_st_noweather_tuned               |     0.584 |     0.556 |     0.671 |     0.616 |           0.607 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     0.632 |     0.58  |           0.606 |
| gnn_st_nodemofeat_tuned              |     0.573 |     0.554 |     0.665 |     0.613 |           0.601 |
| gnn_st_tuned                         |     0.573 |     0.555 |     0.664 |     0.61  |           0.601 |
| gnn_st                               |     0.573 |     0.552 |     0.664 |     0.61  |           0.6   |
| colagnn_tuned                        |     0.472 |     0.561 |     0.677 |     0.62  |           0.582 |
| gat_parity                           |     0.428 |     0.531 |     0.683 |     0.594 |           0.559 |
| gat_tuned                            |     0.37  |     0.531 |     0.684 |     0.599 |           0.546 |
| sarima                               |     0.483 |     0.485 |     0.581 |     0.54  |           0.522 |
| gnn_st_historyonly_tuned             |     0.472 |     0.481 |     0.601 |     0.521 |           0.519 |
| xgboost_parity                       |     0.474 |     0.502 |     0.581 |     0.512 |           0.517 |
| gnn_st_nograph                       |     0.47  |     0.482 |     0.594 |     0.519 |           0.516 |
| xgboost_tuned                        |     0.47  |     0.495 |     0.577 |     0.515 |           0.514 |
| gnn_st_nograph_tuned                 |     0.471 |     0.482 |     0.596 |     0.507 |           0.514 |
| blend_baseline                       |     0.456 |     0.477 |     0.576 |     0.504 |           0.503 |
| xgboost                              |     0.395 |     0.499 |     0.575 |     0.512 |           0.495 |
| lstm_parity                          |     0.454 |     0.445 |     0.545 |     0.471 |           0.479 |
| persistence                          |     0.451 |     0.423 |     0.547 |     0.464 |           0.471 |
| flusight_baseline                    |     0.451 |     0.423 |     0.547 |     0.464 |           0.471 |
| arima                                |     0.434 |     0.422 |     0.511 |     0.477 |           0.461 |
| climatology                          |     0.218 |     0.458 |     0.442 |     0.465 |           0.396 |
| seasonal_naive                       |     0.2   |     0.354 |     0.394 |     0.511 |           0.365 |
| dualtopo_tuned                       |    -0.294 |     0.407 |     0.654 |     0.58  |           0.337 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 4 of 4 |
| blend_baseline | 4 of 4 |
| climatology | 4 of 4 |
| colagnn_tuned | 4 of 4 |
| dualtopo_tuned | 4 of 4 |
| flusight_baseline | 4 of 4 |
| gat_parity | 4 of 4 |
| gat_tuned | 4 of 4 |
| gnn_st_historyonly_tuned | 4 of 4 |
| gnn_st_noadapt | 2 of 2 |
| gnn_st_nodemofeat_tuned | 0 of 4 |
| gnn_st_nograph | 4 of 4 |
| gnn_st_nograph_tuned | 4 of 4 |
| gnn_st_noweather_tuned | 1 of 4 |
| gnn_st_tuned | 1 of 4 |
| lstm | 4 of 4 |
| lstm_parity | 4 of 4 |
| lstm_s10 | 4 of 4 |
| lstm_tuned | 4 of 4 |
| persistence | 4 of 4 |
| sarima | 4 of 4 |
| seasonal_naive | 4 of 4 |
| transfer_finetune_from_boston | 2 of 2 |
| transfer_finetune_from_pooled_all3 | 0 of 1 |
| transfer_finetune_from_pooled_others | 1 of 1 |
| transfer_zeroshot_from_boston | 2 of 2 |
| transfer_zeroshot_from_pooled_all3 | 1 of 1 |
| transfer_zeroshot_from_pooled_others | 1 of 1 |
| xgboost | 4 of 4 |
| xgboost_parity | 4 of 4 |
| xgboost_tuned | 4 of 4 |

## Horizon 2

### MAE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     1.714 |     1.641 |           1.678 |
| gnn_st_noadapt                       |   nan     |   nan     |     1.719 |     1.654 |           1.686 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.718 |   nan     |           1.718 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.729 |   nan     |           1.729 |
| gnn_st_noweather_tuned               |     1.953 |     1.69  |     1.687 |     1.61  |           1.735 |
| gnn_st_nodemofeat_tuned              |     1.948 |     1.684 |     1.746 |     1.605 |           1.746 |
| gnn_st_tuned                         |     1.953 |     1.685 |     1.734 |     1.64  |           1.753 |
| gnn_st                               |     1.985 |     1.695 |     1.741 |     1.64  |           1.765 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     1.886 |     1.691 |           1.788 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     1.791 |   nan     |           1.791 |
| gnn_st_historyonly_tuned             |     1.99  |     1.759 |     1.868 |     1.727 |           1.836 |
| gnn_st_nograph_tuned                 |     2.004 |     1.801 |     1.883 |     1.721 |           1.852 |
| gnn_st_nograph                       |     2.045 |     1.811 |     1.908 |     1.755 |           1.88  |
| sarima                               |     2.036 |     1.798 |     1.98  |     1.771 |           1.896 |
| lstm_tuned                           |     2.128 |     1.841 |     1.88  |     1.741 |           1.898 |
| colagnn_tuned                        |     2.227 |     1.844 |     1.844 |     1.697 |           1.903 |
| xgboost_parity                       |     2.099 |     1.815 |     1.972 |     1.791 |           1.919 |
| blend_baseline                       |     2.08  |     1.819 |     2.069 |     1.732 |           1.925 |
| xgboost_tuned                        |     2.119 |     1.835 |     1.984 |     1.779 |           1.929 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     1.944 |   nan     |           1.944 |
| xgboost                              |     2.228 |     1.838 |     1.966 |     1.827 |           1.965 |
| lstm_s10                             |     2.124 |     1.866 |     2.105 |     1.78  |           1.969 |
| lstm                                 |     2.064 |     1.883 |     2.189 |     1.798 |           1.983 |
| flusight_baseline                    |     2.062 |     2.026 |     1.972 |     1.901 |           1.99  |
| persistence                          |     2.062 |     2.026 |     1.972 |     1.901 |           1.99  |
| lstm_parity                          |     2.101 |     1.925 |     2.24  |     1.822 |           2.022 |
| arima                                |     2.107 |     1.979 |     2.141 |     1.875 |           2.025 |
| climatology                          |     2.358 |     1.968 |     2.412 |     1.877 |           2.154 |
| seasonal_naive                       |     2.422 |     2.293 |     2.323 |     1.963 |           2.25  |

### WIS

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     1.117 |     1.071 |           1.094 |
| gnn_st_noadapt                       |   nan     |   nan     |     1.122 |     1.072 |           1.097 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.117 |   nan     |           1.117 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.127 |   nan     |           1.127 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     1.152 |   nan     |           1.152 |
| gnn_st                               |     1.311 |     1.133 |     1.136 |     1.072 |           1.163 |
| gnn_st_noweather_tuned               |     1.328 |     1.143 |     1.114 |     1.071 |           1.164 |
| gnn_st_tuned                         |     1.315 |     1.14  |     1.134 |     1.072 |           1.165 |
| gnn_st_nodemofeat_tuned              |     1.311 |     1.137 |     1.151 |     1.065 |           1.166 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     1.235 |     1.129 |           1.182 |
| colagnn_tuned                        |     1.405 |     1.165 |     1.163 |     1.09  |           1.206 |
| lstm_tuned                           |     1.346 |     1.182 |     1.195 |     1.123 |           1.211 |
| gnn_st_historyonly_tuned             |     1.38  |     1.18  |     1.211 |     1.143 |           1.229 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     1.23  |   nan     |           1.23  |
| gnn_st_nograph_tuned                 |     1.379 |     1.196 |     1.219 |     1.146 |           1.235 |
| gnn_st_nograph                       |     1.38  |     1.196 |     1.238 |     1.147 |           1.24  |
| sarima                               |     1.366 |     1.194 |     1.269 |     1.146 |           1.244 |
| xgboost_parity                       |     1.403 |     1.183 |     1.263 |     1.174 |           1.256 |
| lstm_s10                             |     1.341 |     1.178 |     1.367 |     1.145 |           1.258 |
| xgboost_tuned                        |     1.411 |     1.202 |     1.27  |     1.152 |           1.259 |
| lstm                                 |     1.306 |     1.185 |     1.432 |     1.159 |           1.271 |
| xgboost                              |     1.505 |     1.198 |     1.262 |     1.18  |           1.286 |
| blend_baseline                       |     1.439 |     1.204 |     1.322 |     1.195 |           1.29  |
| arima                                |     1.408 |     1.264 |     1.372 |     1.21  |           1.314 |
| lstm_parity                          |     1.445 |     1.301 |     1.457 |     1.256 |           1.365 |
| flusight_baseline                    |     1.484 |     1.418 |     1.391 |     1.315 |           1.402 |
| persistence                          |     1.519 |     1.386 |     1.417 |     1.322 |           1.411 |
| climatology                          |     1.694 |     1.277 |     1.508 |     1.272 |           1.438 |
| seasonal_naive                       |     1.764 |     1.633 |     1.573 |     1.471 |           1.61  |

### RMSE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     2.366 |     2.253 |           2.309 |
| gnn_st_noadapt                       |   nan     |   nan     |     2.386 |     2.258 |           2.322 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     2.365 |   nan     |           2.365 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     2.391 |   nan     |           2.391 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     2.432 |   nan     |           2.432 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     2.6   |     2.289 |           2.444 |
| gnn_st                               |     2.728 |     2.429 |     2.409 |     2.264 |           2.458 |
| gnn_st_noweather_tuned               |     2.766 |     2.447 |     2.375 |     2.265 |           2.463 |
| gnn_st_tuned                         |     2.758 |     2.445 |     2.407 |     2.264 |           2.469 |
| gnn_st_nodemofeat_tuned              |     2.739 |     2.435 |     2.461 |     2.247 |           2.47  |
| colagnn_tuned                        |     2.903 |     2.461 |     2.387 |     2.27  |           2.505 |
| lstm_tuned                           |     2.717 |     2.518 |     2.5   |     2.304 |           2.51  |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     2.573 |   nan     |           2.573 |
| gnn_st_historyonly_tuned             |     2.879 |     2.531 |     2.571 |     2.369 |           2.588 |
| lstm_s10                             |     2.71  |     2.511 |     2.81  |     2.35  |           2.595 |
| sarima                               |     2.86  |     2.538 |     2.639 |     2.359 |           2.599 |
| gnn_st_nograph_tuned                 |     2.872 |     2.539 |     2.582 |     2.423 |           2.604 |
| xgboost_tuned                        |     2.91  |     2.487 |     2.653 |     2.367 |           2.604 |
| xgboost_parity                       |     2.892 |     2.485 |     2.646 |     2.413 |           2.609 |
| gnn_st_nograph                       |     2.888 |     2.54  |     2.625 |     2.394 |           2.612 |
| lstm                                 |     2.694 |     2.539 |     2.969 |     2.374 |           2.644 |
| xgboost                              |     3.08  |     2.481 |     2.644 |     2.426 |           2.658 |
| blend_baseline                       |     2.867 |     2.598 |     2.854 |     2.481 |           2.7   |
| arima                                |     2.9   |     2.683 |     2.952 |     2.479 |           2.754 |
| lstm_parity                          |     3.013 |     2.84  |     3.119 |     2.69  |           2.916 |
| climatology                          |     3.311 |     2.865 |     3.458 |     2.683 |           3.079 |
| persistence                          |     3.273 |     3.097 |     3.17  |     2.965 |           3.126 |
| flusight_baseline                    |     3.273 |     3.097 |     3.17  |     2.965 |           3.126 |
| seasonal_naive                       |     3.703 |     3.415 |     3.463 |     3.094 |           3.419 |

### Corr

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_pooled_others |   nan     |   nan     |     0.655 |   nan     |           0.655 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     0.643 |   nan     |           0.643 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     0.643 |   nan     |           0.643 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     0.631 |   nan     |           0.631 |
| transfer_finetune_from_boston        |   nan     |   nan     |     0.652 |     0.567 |           0.609 |
| gnn_st_noadapt                       |   nan     |   nan     |     0.647 |     0.562 |           0.604 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     0.598 |     0.555 |           0.577 |
| lstm_tuned                           |     0.526 |     0.529 |     0.66  |     0.57  |           0.572 |
| lstm_s10                             |     0.511 |     0.533 |     0.629 |     0.549 |           0.555 |
| lstm                                 |     0.537 |     0.527 |     0.591 |     0.541 |           0.549 |
| gnn_st_noweather_tuned               |     0.457 |     0.516 |     0.655 |     0.564 |           0.548 |
| gnn_st_nodemofeat_tuned              |     0.464 |     0.516 |     0.638 |     0.571 |           0.547 |
| gnn_st                               |     0.463 |     0.514 |     0.642 |     0.558 |           0.544 |
| gnn_st_tuned                         |     0.46  |     0.515 |     0.641 |     0.558 |           0.544 |
| colagnn_tuned                        |     0.388 |     0.491 |     0.664 |     0.565 |           0.527 |
| sarima                               |     0.439 |     0.478 |     0.567 |     0.497 |           0.496 |
| gnn_st_historyonly_tuned             |     0.406 |     0.453 |     0.579 |     0.474 |           0.478 |
| xgboost_tuned                        |     0.361 |     0.477 |     0.549 |     0.479 |           0.467 |
| blend_baseline                       |     0.402 |     0.449 |     0.55  |     0.461 |           0.466 |
| gnn_st_nograph_tuned                 |     0.39  |     0.434 |     0.57  |     0.445 |           0.46  |
| xgboost_parity                       |     0.369 |     0.454 |     0.553 |     0.454 |           0.457 |
| gnn_st_nograph                       |     0.37  |     0.43  |     0.55  |     0.451 |           0.45  |
| xgboost                              |     0.293 |     0.478 |     0.553 |     0.44  |           0.441 |
| persistence                          |     0.395 |     0.378 |     0.509 |     0.402 |           0.421 |
| flusight_baseline                    |     0.395 |     0.378 |     0.509 |     0.402 |           0.421 |
| lstm_parity                          |     0.385 |     0.397 |     0.455 |     0.42  |           0.414 |
| arima                                |     0.35  |     0.372 |     0.5   |     0.399 |           0.405 |
| climatology                          |     0.218 |     0.458 |     0.442 |     0.465 |           0.396 |
| seasonal_naive                       |     0.2   |     0.354 |     0.394 |     0.511 |           0.365 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 4 of 4 |
| blend_baseline | 4 of 4 |
| climatology | 4 of 4 |
| colagnn_tuned | 4 of 4 |
| flusight_baseline | 4 of 4 |
| gnn_st_historyonly_tuned | 4 of 4 |
| gnn_st_noadapt | 1 of 2 |
| gnn_st_nodemofeat_tuned | 1 of 4 |
| gnn_st_nograph | 4 of 4 |
| gnn_st_nograph_tuned | 4 of 4 |
| gnn_st_noweather_tuned | 0 of 4 |
| gnn_st_tuned | 0 of 4 |
| lstm | 4 of 4 |
| lstm_parity | 4 of 4 |
| lstm_s10 | 4 of 4 |
| lstm_tuned | 4 of 4 |
| persistence | 4 of 4 |
| sarima | 4 of 4 |
| seasonal_naive | 4 of 4 |
| transfer_finetune_from_boston | 1 of 2 |
| transfer_finetune_from_pooled_all3 | 0 of 1 |
| transfer_finetune_from_pooled_others | 0 of 1 |
| transfer_zeroshot_from_boston | 2 of 2 |
| transfer_zeroshot_from_pooled_all3 | 1 of 1 |
| transfer_zeroshot_from_pooled_others | 1 of 1 |
| xgboost | 4 of 4 |
| xgboost_parity | 4 of 4 |
| xgboost_tuned | 4 of 4 |

## Horizon 4

### MAE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     1.945 |     1.805 |           1.875 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     2.013 |     1.752 |           1.883 |
| gnn_st_noadapt                       |   nan     |   nan     |     1.986 |     1.849 |           1.918 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.963 |   nan     |           1.963 |
| gnn_st_tuned                         |     2.215 |     1.86  |     1.995 |     1.789 |           1.965 |
| gnn_st_noweather_tuned               |     2.32  |     1.872 |     1.925 |     1.79  |           1.977 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.977 |   nan     |           1.977 |
| gnn_st_historyonly_tuned             |     2.227 |     1.856 |     2.083 |     1.794 |           1.99  |
| gnn_st_nodemofeat_tuned              |     2.327 |     1.821 |     2.033 |     1.797 |           1.994 |
| gnn_st                               |     2.305 |     1.858 |     2.035 |     1.85  |           2.012 |
| sarima                               |     2.332 |     1.803 |     2.116 |     1.865 |           2.029 |
| gnn_st_nograph_tuned                 |     2.314 |     1.876 |     2.079 |     1.865 |           2.033 |
| gnn_st_nograph                       |     2.252 |     1.905 |     2.118 |     1.872 |           2.037 |
| blend_baseline                       |     2.245 |     1.886 |     2.156 |     1.862 |           2.037 |
| xgboost_tuned                        |     2.218 |     1.908 |     2.164 |     1.874 |           2.041 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     2.043 |   nan     |           2.043 |
| xgboost_parity                       |     2.221 |     1.919 |     2.175 |     1.911 |           2.057 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     2.081 |   nan     |           2.081 |
| xgboost                              |     2.365 |     1.931 |     2.185 |     1.911 |           2.098 |
| lstm_parity                          |     2.283 |     1.91  |     2.381 |     1.871 |           2.111 |
| climatology                          |     2.358 |     1.968 |     2.412 |     1.877 |           2.154 |
| lstm_tuned                           |     2.396 |     1.913 |     2.435 |     1.871 |           2.154 |
| colagnn_tuned                        |     2.379 |     2.231 |     2.275 |     1.892 |           2.194 |
| arima                                |     2.381 |     2.157 |     2.307 |     2.075 |           2.23  |
| persistence                          |     2.372 |     2.226 |     2.161 |     2.2   |           2.24  |
| flusight_baseline                    |     2.372 |     2.226 |     2.161 |     2.2   |           2.24  |
| lstm_s10                             |     2.423 |     2.065 |     2.483 |     1.998 |           2.242 |
| seasonal_naive                       |     2.422 |     2.293 |     2.323 |     1.963 |           2.25  |
| lstm                                 |     2.534 |     2.057 |     2.481 |     2.007 |           2.27  |

### WIS

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     1.232 |     1.154 |           1.193 |
| gnn_st_noadapt                       |   nan     |   nan     |     1.25  |     1.176 |           1.213 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     1.286 |     1.173 |           1.229 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     1.237 |   nan     |           1.237 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     1.244 |   nan     |           1.244 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     1.278 |   nan     |           1.278 |
| gnn_st_tuned                         |     1.483 |     1.232 |     1.258 |     1.173 |           1.287 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     1.305 |   nan     |           1.305 |
| gnn_st_noweather_tuned               |     1.563 |     1.265 |     1.224 |     1.181 |           1.308 |
| gnn_st                               |     1.551 |     1.255 |     1.273 |     1.18  |           1.315 |
| gnn_st_nodemofeat_tuned              |     1.569 |     1.236 |     1.286 |     1.175 |           1.316 |
| gnn_st_historyonly_tuned             |     1.507 |     1.25  |     1.318 |     1.199 |           1.319 |
| sarima                               |     1.523 |     1.211 |     1.347 |     1.197 |           1.319 |
| gnn_st_nograph_tuned                 |     1.561 |     1.261 |     1.314 |     1.196 |           1.333 |
| xgboost_tuned                        |     1.505 |     1.272 |     1.37  |     1.204 |           1.338 |
| gnn_st_nograph                       |     1.516 |     1.279 |     1.344 |     1.216 |           1.339 |
| xgboost_parity                       |     1.506 |     1.266 |     1.378 |     1.243 |           1.348 |
| blend_baseline                       |     1.553 |     1.241 |     1.364 |     1.273 |           1.358 |
| colagnn_tuned                        |     1.547 |     1.378 |     1.394 |     1.192 |           1.378 |
| xgboost                              |     1.659 |     1.277 |     1.397 |     1.227 |           1.39  |
| lstm_parity                          |     1.53  |     1.282 |     1.54  |     1.273 |           1.406 |
| arima                                |     1.54  |     1.331 |     1.429 |     1.331 |           1.407 |
| lstm_tuned                           |     1.566 |     1.291 |     1.543 |     1.268 |           1.417 |
| lstm_s10                             |     1.521 |     1.294 |     1.601 |     1.299 |           1.429 |
| climatology                          |     1.694 |     1.277 |     1.509 |     1.272 |           1.438 |
| lstm                                 |     1.687 |     1.302 |     1.598 |     1.307 |           1.474 |
| persistence                          |     1.68  |     1.479 |     1.519 |     1.498 |           1.544 |
| flusight_baseline                    |     1.686 |     1.53  |     1.509 |     1.488 |           1.553 |
| seasonal_naive                       |     1.764 |     1.633 |     1.572 |     1.471 |           1.61  |

### RMSE

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_boston        |   nan     |   nan     |     2.553 |     2.382 |           2.468 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     2.691 |     2.304 |           2.497 |
| gnn_st_noadapt                       |   nan     |   nan     |     2.597 |     2.429 |           2.513 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     2.562 |   nan     |           2.562 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     2.581 |   nan     |           2.581 |
| gnn_st_tuned                         |     3.089 |     2.534 |     2.636 |     2.434 |           2.673 |
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     2.704 |   nan     |           2.704 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     2.714 |   nan     |           2.714 |
| sarima                               |     3.164 |     2.489 |     2.79  |     2.448 |           2.723 |
| gnn_st_noweather_tuned               |     3.243 |     2.635 |     2.567 |     2.45  |           2.724 |
| gnn_st                               |     3.239 |     2.61  |     2.642 |     2.445 |           2.734 |
| gnn_st_nodemofeat_tuned              |     3.271 |     2.544 |     2.696 |     2.442 |           2.739 |
| xgboost_tuned                        |     3.071 |     2.603 |     2.831 |     2.462 |           2.742 |
| gnn_st_historyonly_tuned             |     3.116 |     2.624 |     2.822 |     2.493 |           2.764 |
| xgboost_parity                       |     3.073 |     2.616 |     2.859 |     2.527 |           2.769 |
| gnn_st_nograph_tuned                 |     3.255 |     2.635 |     2.726 |     2.483 |           2.775 |
| gnn_st_nograph                       |     3.15  |     2.691 |     2.816 |     2.535 |           2.798 |
| xgboost                              |     3.23  |     2.625 |     2.897 |     2.508 |           2.815 |
| blend_baseline                       |     3.083 |     2.677 |     2.959 |     2.623 |           2.835 |
| colagnn_tuned                        |     3.279 |     2.851 |     2.848 |     2.465 |           2.861 |
| arima                                |     3.125 |     2.791 |     2.916 |     2.679 |           2.878 |
| lstm_tuned                           |     3.123 |     2.685 |     3.323 |     2.617 |           2.937 |
| lstm_parity                          |     3.153 |     2.692 |     3.297 |     2.62  |           2.941 |
| lstm_s10                             |     3.066 |     2.677 |     3.409 |     2.632 |           2.946 |
| lstm                                 |     3.302 |     2.717 |     3.339 |     2.643 |           3     |
| climatology                          |     3.311 |     2.865 |     3.457 |     2.683 |           3.079 |
| persistence                          |     3.63  |     3.283 |     3.355 |     3.28  |           3.387 |
| flusight_baseline                    |     3.63  |     3.283 |     3.355 |     3.28  |           3.387 |
| seasonal_naive                       |     3.703 |     3.415 |     3.463 |     3.094 |           3.419 |

### Corr

| arm                                  |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:-------------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_zeroshot_from_pooled_all3   |   nan     |   nan     |     0.617 |   nan     |           0.617 |
| transfer_zeroshot_from_pooled_others |   nan     |   nan     |     0.608 |   nan     |           0.608 |
| transfer_finetune_from_pooled_all3   |   nan     |   nan     |     0.606 |   nan     |           0.606 |
| transfer_finetune_from_pooled_others |   nan     |   nan     |     0.604 |   nan     |           0.604 |
| transfer_zeroshot_from_boston        |   nan     |   nan     |     0.61  |     0.551 |           0.581 |
| transfer_finetune_from_boston        |   nan     |   nan     |     0.608 |     0.502 |           0.555 |
| gnn_st_noadapt                       |   nan     |   nan     |     0.591 |     0.468 |           0.529 |
| gnn_st_tuned                         |     0.29  |     0.454 |     0.597 |     0.475 |           0.454 |
| sarima                               |     0.294 |     0.486 |     0.535 |     0.461 |           0.444 |
| gnn_st_nodemofeat_tuned              |     0.231 |     0.46  |     0.574 |     0.472 |           0.434 |
| gnn_st_noweather_tuned               |     0.235 |     0.415 |     0.607 |     0.466 |           0.431 |
| gnn_st                               |     0.24  |     0.42  |     0.585 |     0.462 |           0.427 |
| gnn_st_historyonly_tuned             |     0.291 |     0.424 |     0.543 |     0.431 |           0.422 |
| xgboost_tuned                        |     0.296 |     0.471 |     0.485 |     0.429 |           0.42  |
| blend_baseline                       |     0.294 |     0.431 |     0.528 |     0.372 |           0.406 |
| lstm_tuned                           |     0.304 |     0.392 |     0.513 |     0.377 |           0.396 |
| climatology                          |     0.218 |     0.458 |     0.442 |     0.465 |           0.396 |
| gnn_st_nograph_tuned                 |     0.215 |     0.412 |     0.53  |     0.411 |           0.392 |
| xgboost_parity                       |     0.293 |     0.399 |     0.475 |     0.384 |           0.388 |
| xgboost                              |     0.21  |     0.471 |     0.447 |     0.396 |           0.381 |
| gnn_st_nograph                       |     0.26  |     0.387 |     0.496 |     0.376 |           0.38  |
| lstm_s10                             |     0.279 |     0.414 |     0.444 |     0.366 |           0.376 |
| lstm_parity                          |     0.281 |     0.39  |     0.418 |     0.375 |           0.366 |
| seasonal_naive                       |     0.2   |     0.354 |     0.394 |     0.511 |           0.365 |
| lstm                                 |     0.245 |     0.405 |     0.367 |     0.361 |           0.345 |
| colagnn_tuned                        |     0.087 |     0.181 |     0.574 |     0.469 |           0.328 |
| persistence                          |     0.27  |     0.306 |     0.457 |     0.276 |           0.327 |
| flusight_baseline                    |     0.27  |     0.306 |     0.457 |     0.276 |           0.327 |
| arima                                |     0.147 |     0.28  |     0.418 |     0.282 |           0.282 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 4 of 4 |
| blend_baseline | 3 of 4 |
| climatology | 4 of 4 |
| colagnn_tuned | 4 of 4 |
| flusight_baseline | 4 of 4 |
| gnn_st_historyonly_tuned | 1 of 4 |
| gnn_st_noadapt | 0 of 2 |
| gnn_st_nodemofeat_tuned | 1 of 4 |
| gnn_st_nograph | 3 of 4 |
| gnn_st_nograph_tuned | 4 of 4 |
| gnn_st_noweather_tuned | 2 of 4 |
| gnn_st_tuned | 1 of 4 |
| lstm | 4 of 4 |
| lstm_parity | 3 of 4 |
| lstm_s10 | 4 of 4 |
| lstm_tuned | 4 of 4 |
| persistence | 4 of 4 |
| sarima | 3 of 4 |
| seasonal_naive | 4 of 4 |
| transfer_finetune_from_boston | 0 of 2 |
| transfer_finetune_from_pooled_all3 | 0 of 1 |
| transfer_finetune_from_pooled_others | 0 of 1 |
| transfer_zeroshot_from_boston | 0 of 2 |
| transfer_zeroshot_from_pooled_all3 | 1 of 1 |
| transfer_zeroshot_from_pooled_others | 1 of 1 |
| xgboost | 4 of 4 |
| xgboost_parity | 3 of 4 |
| xgboost_tuned | 3 of 4 |

Per-fold significance (block bootstrap and Diebold-Mariano) is in each fold's
`_comparison/significance.md`, written by compare_significance.py.
