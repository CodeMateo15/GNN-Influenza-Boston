# Rolling-origin backtest

Does the ranking hold on seasons the design never saw? Each fold trains on
everything before its test season (variant `full`, validation taken just
before the test window) and forecasts one full season. Folds 2022_23, 2023_24, 2024_25 are the evidence; 2025_26 is the season the design was chosen on and is shown for reference only.

MAE and WIS are in rate per 100,000 (lower is better); Corr is the mean over
neighborhoods of the week-to-week correlation (higher is better).

## Horizon 1

### MAE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_columbus |   nan     |   nan     |     7.348 |     6.956 |           7.348 |
| gnn_st_noadapt                  |   nan     |   nan     |     7.487 |     6.896 |           7.487 |
| transfer_finetune_from_chicago  |   nan     |   nan     |     7.575 |     6.785 |           7.575 |
| gnn_st                          |     8.361 |     7.314 |     7.415 |     6.623 |           7.696 |
| gnn_st_geofixed                 |     8.337 |     7.444 |     7.607 |     7.075 |           7.796 |
| gnn_st_tuned                    |     8.297 |     7.345 |     7.911 |   nan     |           7.851 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     7.912 |     7.1   |           7.912 |
| lstm_tuned                      |     8.342 |     7.519 |     8.019 |   nan     |           7.96  |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     8.013 |     7.744 |           8.013 |
| lstm_s10                        |     8.825 |     7.549 |     8.126 |     7.184 |           8.166 |
| colagnn_tuned                   |     8.874 |     7.59  |     8.115 |   nan     |           8.193 |
| gat_parity                      |     9.12  |     7.885 |     7.81  |     9.057 |           8.272 |
| lstm                            |     9.056 |     7.796 |     8.243 |     7.6   |           8.365 |
| gat_tuned                       |     9.355 |     7.891 |     7.851 |   nan     |           8.366 |
| gnn_st_nograph                  |     9.176 |     7.746 |     8.517 |     8.387 |           8.48  |
| gnn_st_nograph_tuned            |     9.555 |     7.894 |     8.816 |   nan     |           8.755 |
| xgboost_parity                  |     9.609 |     8.237 |     8.525 |     8.442 |           8.79  |
| lstm_parity                     |     9.378 |     8.434 |     8.607 |     7.515 |           8.806 |
| blend_baseline                  |     9.525 |     8.649 |     8.991 |     8.28  |           9.055 |
| arima                           |     9.313 |     8.568 |     9.657 |     8.518 |           9.179 |
| xgboost_tuned                   |     9.615 |     8.147 |     9.876 |   nan     |           9.213 |
| persistence                     |     9.789 |     8.949 |     9.709 |     8.937 |           9.482 |
| flusight_baseline               |     9.789 |     8.949 |     9.764 |     8.969 |           9.5   |
| sarima                          |     9.643 |     8.322 |    11.118 |     8.196 |           9.694 |
| xgboost                         |    14.045 |     8.172 |    10.027 |     9.318 |          10.748 |
| dualtopo_tuned                  |    15.54  |     7.857 |     9.785 |   nan     |          11.061 |
| climatology                     |    19.306 |    11.792 |    14.547 |    10.986 |          15.215 |
| seasonal_naive                  |    16.028 |    17.409 |    15.794 |    19.81  |          16.41  |

### WIS

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_columbus |   nan     |   nan     |     4.783 |     4.567 |           4.783 |
| transfer_finetune_from_chicago  |   nan     |   nan     |     4.871 |     4.35  |           4.871 |
| gnn_st_noadapt                  |   nan     |   nan     |     4.876 |     4.511 |           4.876 |
| gnn_st                          |     5.589 |     4.679 |     4.805 |     4.31  |           5.024 |
| gnn_st_geofixed                 |     5.599 |     4.749 |     4.953 |     4.635 |           5.1   |
| gnn_st_tuned                    |     5.556 |     4.704 |     5.144 |   nan     |           5.134 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     5.153 |     4.659 |           5.153 |
| lstm_tuned                      |     5.495 |     4.847 |     5.203 |   nan     |           5.182 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     5.277 |     5.086 |           5.277 |
| lstm_s10                        |     5.89  |     4.847 |     5.272 |     4.687 |           5.336 |
| colagnn_tuned                   |     6.007 |     4.791 |     5.239 |   nan     |           5.346 |
| gat_parity                      |     6.051 |     5.083 |     4.989 |     6.307 |           5.374 |
| gat_tuned                       |     6.319 |     5.082 |     5.02  |   nan     |           5.474 |
| lstm                            |     6.039 |     5.038 |     5.367 |     4.984 |           5.481 |
| gnn_st_nograph                  |     6.06  |     4.991 |     5.572 |     5.657 |           5.541 |
| gnn_st_nograph_tuned            |     6.234 |     5.042 |     5.793 |   nan     |           5.69  |
| xgboost_parity                  |     6.278 |     5.335 |     5.541 |     5.587 |           5.718 |
| lstm_parity                     |     6.139 |     5.463 |     5.567 |     4.953 |           5.723 |
| blend_baseline                  |     6.256 |     5.63  |     5.975 |     5.518 |           5.953 |
| arima                           |     6.217 |     5.562 |     6.335 |     5.598 |           6.038 |
| xgboost_tuned                   |     6.286 |     5.275 |     6.681 |   nan     |           6.081 |
| persistence                     |     6.507 |     5.856 |     6.363 |     5.91  |           6.242 |
| flusight_baseline               |     6.646 |     5.831 |     6.692 |     6.141 |           6.39  |
| sarima                          |     6.293 |     5.43  |     7.843 |     5.325 |           6.522 |
| xgboost                         |     9.256 |     5.486 |     6.806 |     6.149 |           7.183 |
| dualtopo_tuned                  |    11.364 |     5.376 |     6.455 |   nan     |           7.732 |
| climatology                     |    13.251 |     6.592 |    11.095 |     7.638 |          10.313 |
| seasonal_naive                  |    12.195 |    13.71  |    10.611 |    13.719 |          12.172 |

### RMSE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_columbus |   nan     |   nan     |    12.241 |    13.006 |          12.241 |
| transfer_finetune_from_chicago  |   nan     |   nan     |    12.335 |    11.616 |          12.335 |
| gnn_st                          |    14.452 |    10.848 |    12.325 |    11.879 |          12.542 |
| gnn_st_noadapt                  |   nan     |   nan     |    12.588 |    12.681 |          12.588 |
| gnn_st_geofixed                 |    14.482 |    10.931 |    12.833 |    13.023 |          12.749 |
| gnn_st_tuned                    |    14.326 |    10.814 |    13.491 |   nan     |          12.877 |
| lstm_tuned                      |    14.59  |    11.365 |    13.582 |   nan     |          13.179 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    13.27  |    13.099 |          13.27  |
| lstm_s10                        |    16.036 |    11.265 |    13.682 |    13.157 |          13.661 |
| colagnn_tuned                   |    16.482 |    11.226 |    13.597 |   nan     |          13.768 |
| gnn_st_nograph                  |    15.794 |    11.517 |    14.61  |    15.641 |          13.973 |
| gat_parity                      |    17.27  |    11.647 |    13.054 |    18.32  |          13.99  |
| lstm                            |    16.654 |    11.992 |    13.979 |    13.655 |          14.208 |
| lstm_parity                     |    15.728 |    12.492 |    14.501 |    13.215 |          14.241 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    14.242 |    14.085 |          14.242 |
| gat_tuned                       |    18.259 |    11.666 |    13.09  |   nan     |          14.339 |
| xgboost_parity                  |    16.348 |    12.333 |    14.428 |    15.258 |          14.37  |
| gnn_st_nograph_tuned            |    16.271 |    11.616 |    15.446 |   nan     |          14.445 |
| arima                           |    15.792 |    12.937 |    16     |    15.172 |          14.91  |
| blend_baseline                  |    16.054 |    12.922 |    16.242 |    14.992 |          15.072 |
| persistence                     |    16.258 |    13.425 |    16.225 |    15.806 |          15.303 |
| flusight_baseline               |    16.258 |    13.425 |    16.245 |    15.812 |          15.309 |
| xgboost_tuned                   |    16.356 |    12.194 |    18.131 |   nan     |          15.56  |
| sarima                          |    16.006 |    12.675 |    20.664 |    14.428 |          16.448 |
| xgboost                         |    23.775 |    12.51  |    18.518 |    16.711 |          18.267 |
| dualtopo_tuned                  |    31.704 |    11.699 |    16.556 |   nan     |          19.986 |
| climatology                     |    35.432 |    18.324 |    31.798 |    22.521 |          28.518 |
| seasonal_naive                  |    29.332 |    30.22  |    28.279 |    39.835 |          29.277 |

### Corr

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_chicago  |   nan     |   nan     |     0.912 |     0.89  |           0.912 |
| transfer_finetune_from_columbus |   nan     |   nan     |     0.909 |     0.883 |           0.909 |
| gnn_st_noadapt                  |   nan     |   nan     |     0.903 |     0.881 |           0.903 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     0.898 |     0.853 |           0.898 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     0.892 |     0.845 |           0.892 |
| lstm_tuned                      |     0.872 |     0.805 |     0.918 |   nan     |           0.865 |
| lstm_s10                        |     0.855 |     0.803 |     0.917 |     0.893 |           0.858 |
| lstm                            |     0.849 |     0.8   |     0.913 |     0.88  |           0.854 |
| colagnn_tuned                   |     0.85  |     0.795 |     0.915 |   nan     |           0.853 |
| gat_parity                      |     0.849 |     0.79  |     0.919 |     0.79  |           0.853 |
| gat_tuned                       |     0.84  |     0.784 |     0.92  |   nan     |           0.848 |
| gnn_st                          |     0.838 |     0.797 |     0.908 |     0.892 |           0.848 |
| gnn_st_tuned                    |     0.842 |     0.794 |     0.898 |   nan     |           0.845 |
| gnn_st_geofixed                 |     0.838 |     0.788 |     0.903 |     0.875 |           0.843 |
| gnn_st_nograph                  |     0.796 |     0.755 |     0.874 |     0.804 |           0.808 |
| lstm_parity                     |     0.792 |     0.734 |     0.881 |     0.855 |           0.802 |
| gnn_st_nograph_tuned            |     0.783 |     0.751 |     0.868 |   nan     |           0.801 |
| xgboost_tuned                   |     0.782 |     0.736 |     0.876 |   nan     |           0.798 |
| xgboost_parity                  |     0.782 |     0.731 |     0.879 |     0.804 |           0.797 |
| blend_baseline                  |     0.787 |     0.713 |     0.859 |     0.804 |           0.786 |
| persistence                     |     0.792 |     0.705 |     0.848 |     0.798 |           0.782 |
| flusight_baseline               |     0.792 |     0.705 |     0.847 |     0.798 |           0.781 |
| sarima                          |     0.783 |     0.74  |     0.805 |     0.813 |           0.776 |
| arima                           |     0.769 |     0.707 |     0.835 |     0.784 |           0.77  |
| xgboost                         |     0.539 |     0.731 |     0.873 |     0.772 |           0.715 |
| dualtopo_tuned                  |     0.213 |     0.78  |     0.919 |   nan     |           0.637 |
| climatology                     |     0.017 |     0.755 |     0.687 |     0.66  |           0.486 |
| seasonal_naive                  |     0.424 |     0.339 |     0.58  |     0.296 |           0.448 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 3 of 3 |
| blend_baseline | 3 of 3 |
| climatology | 3 of 3 |
| colagnn_tuned | 3 of 3 |
| dualtopo_tuned | 3 of 3 |
| flusight_baseline | 3 of 3 |
| gat_parity | 3 of 3 |
| gat_tuned | 3 of 3 |
| gnn_st_geofixed | 2 of 3 |
| gnn_st_noadapt | 1 of 1 |
| gnn_st_nograph | 3 of 3 |
| gnn_st_nograph_tuned | 3 of 3 |
| gnn_st_tuned | 2 of 3 |
| lstm | 3 of 3 |
| lstm_parity | 3 of 3 |
| lstm_s10 | 3 of 3 |
| lstm_tuned | 2 of 3 |
| persistence | 3 of 3 |
| sarima | 3 of 3 |
| seasonal_naive | 3 of 3 |
| transfer_finetune_from_chicago | 1 of 1 |
| transfer_finetune_from_columbus | 0 of 1 |
| transfer_zeroshot_from_chicago | 1 of 1 |
| transfer_zeroshot_from_columbus | 1 of 1 |
| xgboost | 3 of 3 |
| xgboost_parity | 3 of 3 |
| xgboost_tuned | 3 of 3 |

## Horizon 2

### MAE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_chicago  |   nan     |   nan     |     9.288 |     9.134 |           9.288 |
| gnn_st_noadapt                  |   nan     |   nan     |     9.323 |     9.366 |           9.323 |
| transfer_finetune_from_columbus |   nan     |   nan     |     9.452 |     9.432 |           9.452 |
| gnn_st                          |    11.492 |     7.773 |     9.349 |     9.098 |           9.538 |
| gnn_st_tuned                    |    11.36  |     7.748 |     9.771 |   nan     |           9.626 |
| gnn_st_geofixed                 |    11.469 |     7.848 |     9.646 |     9.745 |           9.654 |
| gnn_st_nograph_tuned            |    11.779 |     8.228 |    10.304 |   nan     |          10.103 |
| gnn_st_nograph                  |    11.771 |     8.268 |    10.318 |    10.832 |          10.119 |
| lstm                            |    10.944 |     8.315 |    11.225 |    10.005 |          10.161 |
| lstm_tuned                      |    11.309 |     8.997 |    10.271 |   nan     |          10.192 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    10.279 |     9.455 |          10.279 |
| lstm_s10                        |    11.561 |     8.247 |    11.032 |    10.172 |          10.28  |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    10.3   |     9.948 |          10.3   |
| xgboost_parity                  |    12.119 |     8.331 |    10.572 |    11.346 |          10.341 |
| lstm_parity                     |    11.68  |     9.051 |    10.66  |     9.801 |          10.464 |
| xgboost_tuned                   |    12.117 |     8.476 |    11.854 |   nan     |          10.816 |
| blend_baseline                  |    11.968 |     9.261 |    11.418 |    10.569 |          10.882 |
| colagnn_tuned                   |    14.426 |     8.336 |    10.359 |   nan     |          11.04  |
| sarima                          |    12.129 |     8.665 |    12.713 |    10.527 |          11.169 |
| arima                           |    11.808 |     9.436 |    12.824 |    11.521 |          11.356 |
| persistence                     |    12.345 |     9.981 |    13.331 |    12.07  |          11.885 |
| flusight_baseline               |    12.345 |     9.981 |    13.35  |    12.063 |          11.892 |
| xgboost                         |    16.614 |     8.337 |    11.496 |    12.052 |          12.149 |
| climatology                     |    19.306 |    11.791 |    14.547 |    10.986 |          15.215 |
| seasonal_naive                  |    16.028 |    17.409 |    15.794 |    19.81  |          16.41  |

### WIS

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_chicago  |   nan     |   nan     |     6.115 |     6.215 |           6.115 |
| gnn_st_noadapt                  |   nan     |   nan     |     6.145 |     6.46  |           6.145 |
| transfer_finetune_from_columbus |   nan     |   nan     |     6.274 |     6.525 |           6.274 |
| gnn_st                          |     7.662 |     5.019 |     6.164 |     6.234 |           6.282 |
| gnn_st_geofixed                 |     7.658 |     5.096 |     6.396 |     6.754 |           6.383 |
| gnn_st_tuned                    |     7.698 |     5.068 |     6.635 |   nan     |           6.467 |
| gnn_st_nograph                  |     7.822 |     5.388 |     6.912 |     7.54  |           6.708 |
| gnn_st_nograph_tuned            |     7.827 |     5.37  |     6.948 |   nan     |           6.715 |
| lstm_tuned                      |     7.666 |     5.846 |     6.961 |   nan     |           6.825 |
| lstm                            |     7.36  |     5.415 |     7.709 |     6.978 |           6.828 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     6.865 |     6.395 |           6.865 |
| xgboost_parity                  |     8.091 |     5.55  |     7.005 |     7.888 |           6.882 |
| lstm_parity                     |     7.751 |     5.869 |     7.089 |     6.726 |           6.903 |
| lstm_s10                        |     8.028 |     5.28  |     7.56  |     7.171 |           6.956 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     7.106 |     6.684 |           7.106 |
| blend_baseline                  |     7.947 |     6.08  |     7.841 |     7.317 |           7.289 |
| xgboost_tuned                   |     8.089 |     5.609 |     8.266 |   nan     |           7.322 |
| colagnn_tuned                   |    10.37  |     5.293 |     7.174 |   nan     |           7.612 |
| sarima                          |     8.019 |     5.75  |     9.222 |     7.025 |           7.664 |
| arima                           |     8.133 |     6.138 |     8.731 |     7.654 |           7.667 |
| persistence                     |     8.298 |     6.566 |     8.947 |     8.417 |           7.937 |
| flusight_baseline               |     8.55  |     6.52  |     9.412 |     8.733 |           8.161 |
| xgboost                         |    11.343 |     5.915 |     7.972 |     8.296 |           8.41  |
| climatology                     |    13.251 |     6.602 |    11.095 |     7.638 |          10.316 |
| seasonal_naive                  |    12.195 |    13.793 |    10.611 |    13.719 |          12.199 |

### RMSE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| gnn_st                          |    20.725 |    11.58  |    16.735 |    18.505 |          16.346 |
| gnn_st_geofixed                 |    20.744 |    11.76  |    17.288 |    19.988 |          16.597 |
| gnn_st_noadapt                  |   nan     |   nan     |    16.605 |    19.169 |          16.605 |
| transfer_finetune_from_chicago  |   nan     |   nan     |    16.687 |    18.32  |          16.687 |
| transfer_finetune_from_columbus |   nan     |   nan     |    16.875 |    19.302 |          16.875 |
| gnn_st_tuned                    |    21.056 |    11.635 |    18.288 |   nan     |          16.993 |
| gnn_st_nograph                  |    21.037 |    12.41  |    18.999 |    21.043 |          17.482 |
| gnn_st_nograph_tuned            |    21.082 |    12.296 |    19.289 |   nan     |          17.556 |
| xgboost_parity                  |    21.795 |    12.749 |    19.033 |    22.005 |          17.859 |
| lstm_parity                     |    20.83  |    13.474 |    19.315 |    18.963 |          17.873 |
| lstm_tuned                      |    21.901 |    13.448 |    18.69  |   nan     |          18.013 |
| lstm                            |    21.178 |    12.795 |    20.665 |    20.354 |          18.212 |
| lstm_s10                        |    23.02  |    12.104 |    20.364 |    21.084 |          18.496 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    18.772 |    18.855 |          18.772 |
| blend_baseline                  |    21.26  |    14.02  |    21.796 |    20.988 |          19.026 |
| xgboost_tuned                   |    21.796 |    12.869 |    23.018 |   nan     |          19.228 |
| sarima                          |    21.363 |    13.065 |    23.723 |    19.74  |          19.384 |
| arima                           |    21.43  |    14.14  |    22.926 |    21.402 |          19.499 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    19.984 |    19.075 |          19.984 |
| persistence                     |    21.76  |    14.983 |    23.88  |    23.84  |          20.207 |
| flusight_baseline               |    21.76  |    14.983 |    23.885 |    23.839 |          20.209 |
| colagnn_tuned                   |    29.443 |    12.326 |    19.904 |   nan     |          20.558 |
| xgboost                         |    29.787 |    12.917 |    21.954 |    23.655 |          21.553 |
| climatology                     |    35.432 |    18.323 |    31.798 |    22.521 |          28.517 |
| seasonal_naive                  |    29.332 |    30.22  |    28.279 |    39.835 |          29.277 |

### Corr

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_chicago  |   nan     |   nan     |     0.857 |     0.777 |           0.857 |
| gnn_st_noadapt                  |   nan     |   nan     |     0.847 |     0.769 |           0.847 |
| transfer_finetune_from_columbus |   nan     |   nan     |     0.839 |     0.771 |           0.839 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     0.813 |     0.719 |           0.813 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     0.797 |     0.719 |           0.797 |
| lstm                            |     0.749 |     0.757 |     0.823 |     0.723 |           0.776 |
| lstm_s10                        |     0.735 |     0.759 |     0.833 |     0.713 |           0.776 |
| gnn_st                          |     0.676 |     0.757 |     0.847 |     0.784 |           0.76  |
| gnn_st_tuned                    |     0.683 |     0.76  |     0.83  |   nan     |           0.758 |
| lstm_tuned                      |     0.721 |     0.685 |     0.861 |   nan     |           0.755 |
| gnn_st_geofixed                 |     0.677 |     0.752 |     0.835 |     0.744 |           0.755 |
| gnn_st_nograph_tuned            |     0.665 |     0.723 |     0.811 |   nan     |           0.733 |
| gnn_st_nograph                  |     0.666 |     0.72  |     0.811 |     0.667 |           0.732 |
| xgboost_tuned                   |     0.641 |     0.718 |     0.821 |   nan     |           0.726 |
| xgboost_parity                  |     0.64  |     0.715 |     0.808 |     0.621 |           0.721 |
| lstm_parity                     |     0.667 |     0.68  |     0.793 |     0.719 |           0.713 |
| sarima                          |     0.642 |     0.713 |     0.737 |     0.691 |           0.697 |
| colagnn_tuned                   |     0.505 |     0.744 |     0.839 |   nan     |           0.696 |
| blend_baseline                  |     0.663 |     0.655 |     0.753 |     0.648 |           0.69  |
| persistence                     |     0.678 |     0.635 |     0.721 |     0.618 |           0.678 |
| flusight_baseline               |     0.678 |     0.635 |     0.721 |     0.617 |           0.678 |
| arima                           |     0.6   |     0.642 |     0.702 |     0.611 |           0.648 |
| xgboost                         |     0.307 |     0.717 |     0.829 |     0.617 |           0.618 |
| climatology                     |     0.017 |     0.755 |     0.687 |     0.66  |           0.486 |
| seasonal_naive                  |     0.424 |     0.339 |     0.58  |     0.296 |           0.448 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 3 of 3 |
| blend_baseline | 3 of 3 |
| climatology | 3 of 3 |
| colagnn_tuned | 3 of 3 |
| flusight_baseline | 3 of 3 |
| gnn_st_geofixed | 2 of 3 |
| gnn_st_noadapt | 0 of 1 |
| gnn_st_nograph | 3 of 3 |
| gnn_st_nograph_tuned | 3 of 3 |
| gnn_st_tuned | 1 of 3 |
| lstm | 2 of 3 |
| lstm_parity | 3 of 3 |
| lstm_s10 | 3 of 3 |
| lstm_tuned | 2 of 3 |
| persistence | 3 of 3 |
| sarima | 3 of 3 |
| seasonal_naive | 3 of 3 |
| transfer_finetune_from_chicago | 0 of 1 |
| transfer_finetune_from_columbus | 1 of 1 |
| transfer_zeroshot_from_chicago | 1 of 1 |
| transfer_zeroshot_from_columbus | 1 of 1 |
| xgboost | 3 of 3 |
| xgboost_parity | 3 of 3 |
| xgboost_tuned | 3 of 3 |

## Horizon 4

### MAE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| gnn_st_noadapt                  |   nan     |   nan     |    11.631 |    12.781 |          11.631 |
| transfer_finetune_from_columbus |   nan     |   nan     |    11.725 |    14.135 |          11.725 |
| transfer_finetune_from_chicago  |   nan     |   nan     |    11.791 |    13.336 |          11.791 |
| gnn_st_tuned                    |    15.904 |     8.318 |    11.565 |   nan     |          11.929 |
| gnn_st                          |    16.286 |     8.322 |    11.648 |    13.27  |          12.085 |
| gnn_st_geofixed                 |    16.166 |     8.546 |    11.896 |    13.15  |          12.203 |
| colagnn_tuned                   |    15.066 |     9.16  |    12.598 |   nan     |          12.275 |
| gnn_st_nograph                  |    16.18  |     8.77  |    12.594 |    12.994 |          12.515 |
| gnn_st_nograph_tuned            |    15.884 |     9.04  |    12.776 |   nan     |          12.567 |
| lstm_s10                        |    15.431 |     9.303 |    13.594 |    13.751 |          12.776 |
| lstm                            |    15.903 |     9.486 |    13.522 |    13.526 |          12.97  |
| xgboost_tuned                   |    16.475 |     9.342 |    13.157 |   nan     |          12.991 |
| xgboost_parity                  |    16.49  |     8.967 |    13.584 |    14.354 |          13.014 |
| lstm_tuned                      |    15.675 |    10.402 |    12.983 |   nan     |          13.02  |
| sarima                          |    16.55  |     8.632 |    14.077 |    13.125 |          13.086 |
| lstm_parity                     |    16.484 |    10.825 |    12.751 |    12.177 |          13.354 |
| xgboost                         |    18.61  |     8.927 |    13.034 |    14.004 |          13.524 |
| blend_baseline                  |    16.517 |     9.896 |    14.643 |    12.192 |          13.685 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    13.801 |    11.91  |          13.801 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    14.484 |    12.241 |          14.484 |
| arima                           |    15.425 |    11.124 |    17.6   |    15.659 |          14.716 |
| climatology                     |    19.288 |    11.791 |    14.547 |    10.986 |          15.209 |
| persistence                     |    17.534 |    11.752 |    19.384 |    17.464 |          16.224 |
| flusight_baseline               |    17.534 |    11.752 |    19.401 |    17.469 |          16.229 |
| seasonal_naive                  |    16.028 |    17.409 |    15.794 |    19.81  |          16.41  |

### WIS

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| gnn_st_tuned                    |    10.949 |     5.531 |     8.183 |   nan     |           8.221 |
| gnn_st_noadapt                  |   nan     |   nan     |     8.254 |     9.041 |           8.254 |
| gnn_st                          |    11.091 |     5.53  |     8.303 |     9.483 |           8.308 |
| transfer_finetune_from_columbus |   nan     |   nan     |     8.37  |    10.117 |           8.37  |
| gnn_st_geofixed                 |    11.072 |     5.666 |     8.467 |     9.316 |           8.401 |
| transfer_finetune_from_chicago  |   nan     |   nan     |     8.405 |     9.495 |           8.405 |
| gnn_st_nograph                  |    11.093 |     5.836 |     9.03  |     9.132 |           8.653 |
| gnn_st_nograph_tuned            |    10.862 |     5.977 |     9.198 |   nan     |           8.679 |
| colagnn_tuned                   |    10.969 |     6.431 |     8.92  |   nan     |           8.773 |
| lstm_s10                        |    11.073 |     6.175 |     9.504 |     9.842 |           8.917 |
| lstm                            |    11.195 |     6.254 |     9.422 |     9.599 |           8.957 |
| xgboost_tuned                   |    11.313 |     6.342 |     9.492 |   nan     |           9.049 |
| xgboost_parity                  |    11.321 |     6.217 |     9.733 |     9.848 |           9.09  |
| lstm_parity                     |    11.259 |     6.999 |     9.147 |     8.564 |           9.135 |
| sarima                          |    10.939 |     5.91  |    10.597 |     8.488 |           9.149 |
| lstm_tuned                      |    11.294 |     6.84  |     9.334 |   nan     |           9.156 |
| blend_baseline                  |    11.301 |     6.436 |    10.963 |     8.459 |           9.567 |
| xgboost                         |    13.08  |     6.528 |     9.286 |     9.521 |           9.631 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    10.074 |     8.012 |          10.074 |
| climatology                     |    13.21  |     6.602 |    11.095 |     7.638 |          10.303 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    10.36  |     8.306 |          10.36  |
| arima                           |    11.263 |     7.291 |    12.736 |    10.148 |          10.43  |
| persistence                     |    12.381 |     7.869 |    14.065 |    12.35  |          11.438 |
| flusight_baseline               |    12.499 |     7.683 |    14.168 |    12.777 |          11.45  |
| seasonal_naive                  |    12.185 |    13.793 |    10.611 |    13.719 |          12.196 |

### RMSE

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| gnn_st_tuned                    |    30.071 |    12.354 |    23.542 |   nan     |          21.989 |
| gnn_st                          |    30.393 |    12.35  |    23.605 |    26.592 |          22.116 |
| gnn_st_geofixed                 |    30.303 |    12.766 |    24.024 |    25.877 |          22.364 |
| gnn_st_nograph                  |    30.301 |    13.241 |    25.682 |    25.626 |          23.075 |
| colagnn_tuned                   |    31.029 |    13.325 |    24.987 |   nan     |          23.114 |
| gnn_st_nograph_tuned            |    30.006 |    13.462 |    25.91  |   nan     |          23.126 |
| gnn_st_noadapt                  |   nan     |   nan     |    23.328 |    25.338 |          23.328 |
| lstm                            |    30.511 |    14.144 |    25.334 |    27.23  |          23.33  |
| lstm_s10                        |    30.709 |    14.174 |    25.322 |    27.444 |          23.402 |
| sarima                          |    30.23  |    13.25  |    26.733 |    23.926 |          23.404 |
| transfer_finetune_from_chicago  |   nan     |   nan     |    23.413 |    26.682 |          23.413 |
| transfer_finetune_from_columbus |   nan     |   nan     |    23.505 |    27.677 |          23.505 |
| xgboost_parity                  |    30.636 |    13.408 |    26.834 |    27.289 |          23.626 |
| xgboost_tuned                   |    30.624 |    13.827 |    26.739 |   nan     |          23.73  |
| lstm_tuned                      |    31.077 |    15.141 |    26.058 |   nan     |          24.092 |
| lstm_parity                     |    30.663 |    15.677 |    25.966 |    24.75  |          24.102 |
| xgboost                         |    34.249 |    13.381 |    25.605 |    25.995 |          24.412 |
| blend_baseline                  |    30.78  |    15.337 |    29.879 |    24.788 |          25.332 |
| arima                           |    31.365 |    16.528 |    32.827 |    28.534 |          26.907 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |    27.713 |    23.144 |          27.713 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |    28.117 |    24.725 |          28.117 |
| climatology                     |    35.4   |    18.323 |    31.798 |    22.521 |          28.507 |
| seasonal_naive                  |    29.332 |    30.22  |    28.279 |    39.835 |          29.277 |
| persistence                     |    33.297 |    17.596 |    37.222 |    34.91  |          29.372 |
| flusight_baseline               |    33.297 |    17.596 |    37.224 |    34.912 |          29.372 |

### Corr

| arm                             |   2022_23 |   2023_24 |   2024_25 |   2025_26 |   evidence mean |
|:--------------------------------|----------:|----------:|----------:|----------:|----------------:|
| transfer_finetune_from_chicago  |   nan     |   nan     |     0.791 |     0.446 |           0.791 |
| gnn_st_noadapt                  |   nan     |   nan     |     0.777 |     0.491 |           0.777 |
| transfer_finetune_from_columbus |   nan     |   nan     |     0.765 |     0.423 |           0.765 |
| transfer_zeroshot_from_columbus |   nan     |   nan     |     0.628 |     0.574 |           0.628 |
| colagnn_tuned                   |     0.34  |     0.724 |     0.762 |   nan     |           0.608 |
| gnn_st_tuned                    |     0.306 |     0.738 |     0.778 |   nan     |           0.607 |
| gnn_st                          |     0.306 |     0.737 |     0.764 |     0.432 |           0.602 |
| transfer_zeroshot_from_chicago  |   nan     |   nan     |     0.599 |     0.48  |           0.599 |
| gnn_st_geofixed                 |     0.305 |     0.722 |     0.752 |     0.47  |           0.593 |
| lstm_s10                        |     0.345 |     0.704 |     0.729 |     0.405 |           0.593 |
| sarima                          |     0.351 |     0.733 |     0.674 |     0.562 |           0.586 |
| gnn_st_nograph                  |     0.298 |     0.713 |     0.706 |     0.413 |           0.572 |
| gnn_st_nograph_tuned            |     0.309 |     0.695 |     0.7   |   nan     |           0.568 |
| xgboost_tuned                   |     0.276 |     0.668 |     0.755 |   nan     |           0.566 |
| lstm                            |     0.237 |     0.689 |     0.734 |     0.416 |           0.553 |
| lstm_tuned                      |     0.32  |     0.634 |     0.672 |   nan     |           0.542 |
| lstm_parity                     |     0.289 |     0.614 |     0.697 |     0.486 |           0.533 |
| xgboost_parity                  |     0.275 |     0.683 |     0.641 |     0.338 |           0.533 |
| blend_baseline                  |     0.319 |     0.632 |     0.53  |     0.448 |           0.494 |
| xgboost                         |     0.028 |     0.671 |     0.779 |     0.386 |           0.493 |
| climatology                     |     0.018 |     0.755 |     0.687 |     0.66  |           0.486 |
| seasonal_naive                  |     0.424 |     0.339 |     0.58  |     0.296 |           0.448 |
| flusight_baseline               |     0.358 |     0.536 |     0.429 |     0.224 |           0.441 |
| persistence                     |     0.358 |     0.536 |     0.429 |     0.224 |           0.441 |
| arima                           |     0.078 |     0.509 |     0.407 |     0.233 |           0.331 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 2 of 3 |
| blend_baseline | 3 of 3 |
| climatology | 3 of 3 |
| colagnn_tuned | 2 of 3 |
| flusight_baseline | 3 of 3 |
| gnn_st_geofixed | 2 of 3 |
| gnn_st_noadapt | 0 of 1 |
| gnn_st_nograph | 2 of 3 |
| gnn_st_nograph_tuned | 2 of 3 |
| gnn_st_tuned | 0 of 3 |
| lstm | 2 of 3 |
| lstm_parity | 3 of 3 |
| lstm_s10 | 2 of 3 |
| lstm_tuned | 2 of 3 |
| persistence | 3 of 3 |
| sarima | 3 of 3 |
| seasonal_naive | 2 of 3 |
| transfer_finetune_from_chicago | 1 of 1 |
| transfer_finetune_from_columbus | 1 of 1 |
| transfer_zeroshot_from_chicago | 1 of 1 |
| transfer_zeroshot_from_columbus | 1 of 1 |
| xgboost | 3 of 3 |
| xgboost_parity | 3 of 3 |
| xgboost_tuned | 3 of 3 |

Per-fold significance (block bootstrap and Diebold-Mariano) is in each fold's
`_comparison/significance.md`, written by compare_significance.py.
