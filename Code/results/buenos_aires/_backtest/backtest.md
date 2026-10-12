# Rolling-origin backtest

Does the ranking hold on seasons the design never saw? Each fold trains on
everything before its test season (variant `post_covid`, validation taken just
before the test window) and forecasts one full season. Folds 2023_24 are the evidence; 2024_25 is the season the design was chosen on and is shown for reference only.

MAE and WIS are in rate per 100,000 (lower is better); Corr is the mean over
neighborhoods of the week-to-week correlation (higher is better).

## Horizon 1

### MAE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| gnn_st_nograph       |    10.797 |    11.342 |          10.797 |
| gnn_st_tuned         |    10.803 |   nan     |          10.803 |
| gnn_st_nograph_tuned |    10.805 |   nan     |          10.805 |
| gnn_st               |    10.81  |    10.823 |          10.81  |
| blend_baseline       |    10.835 |    10.772 |          10.835 |
| persistence          |    11.117 |    11.071 |          11.117 |
| flusight_baseline    |    11.155 |    11.073 |          11.155 |
| lstm_parity          |    11.633 |    10.926 |          11.633 |
| lstm_tuned           |    11.79  |   nan     |          11.79  |
| arima                |    11.943 |    11.951 |          11.943 |
| colagnn_tuned        |    14.083 |   nan     |          14.083 |
| sarima               |    17.44  |    11.685 |          17.44  |
| xgboost_tuned        |    18.085 |   nan     |          18.085 |
| xgboost_parity       |    18.415 |    14.063 |          18.415 |
| gat_parity           |    21.795 |    18.733 |          21.795 |
| gat_tuned            |    21.906 |   nan     |          21.906 |
| dualtopo_tuned       |    22.428 |   nan     |          22.428 |
| lstm_s10             |    22.924 |    23.749 |          22.924 |
| lstm                 |    23.155 |    24.16  |          23.155 |
| xgboost              |    24.024 |    21.257 |          24.024 |
| seasonal_naive       |    25.066 |    26.134 |          25.066 |
| climatology          |    25.395 |    25.566 |          25.395 |

### WIS

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| blend_baseline       |     7.481 |     7.336 |           7.481 |
| gnn_st               |     7.484 |     7.396 |           7.484 |
| gnn_st_tuned         |     7.497 |   nan     |           7.497 |
| gnn_st_nograph       |     7.565 |     7.758 |           7.565 |
| persistence          |     7.598 |     7.522 |           7.598 |
| gnn_st_nograph_tuned |     7.623 |   nan     |           7.623 |
| flusight_baseline    |     7.767 |     7.683 |           7.767 |
| lstm_parity          |     8.223 |     7.389 |           8.223 |
| lstm_tuned           |     8.287 |   nan     |           8.287 |
| arima                |     8.465 |     8.268 |           8.465 |
| colagnn_tuned        |    10.054 |   nan     |          10.054 |
| xgboost_tuned        |    12.575 |   nan     |          12.575 |
| xgboost_parity       |    12.974 |     9.654 |          12.974 |
| sarima               |    13.655 |     8.026 |          13.655 |
| gat_parity           |    15.416 |    12.848 |          15.416 |
| gat_tuned            |    15.56  |   nan     |          15.56  |
| xgboost              |    16.773 |    15.329 |          16.773 |
| dualtopo_tuned       |    17.463 |   nan     |          17.463 |
| climatology          |    17.971 |    19.222 |          17.971 |
| seasonal_naive       |    18.018 |    19.536 |          18.018 |
| lstm_s10             |    18.626 |    17.382 |          18.626 |
| lstm                 |    18.83  |    17.733 |          18.83  |

### RMSE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| blend_baseline       |    21.458 |    23.807 |          21.458 |
| gnn_st_nograph       |    21.524 |    25.616 |          21.524 |
| gnn_st_nograph_tuned |    21.542 |   nan     |          21.542 |
| gnn_st               |    21.542 |    24.414 |          21.542 |
| gnn_st_tuned         |    21.559 |   nan     |          21.559 |
| persistence          |    22.371 |    24.31  |          22.371 |
| flusight_baseline    |    22.401 |    24.31  |          22.401 |
| lstm_parity          |    23.064 |    23.952 |          23.064 |
| arima                |    23.289 |    24.01  |          23.289 |
| lstm_tuned           |    23.546 |   nan     |          23.546 |
| colagnn_tuned        |    26.643 |   nan     |          26.643 |
| xgboost_tuned        |    33.475 |   nan     |          33.475 |
| xgboost_parity       |    34.024 |    31.487 |          34.024 |
| gat_parity           |    39.159 |    37.379 |          39.159 |
| gat_tuned            |    39.186 |   nan     |          39.186 |
| sarima               |    39.791 |    23.63  |          39.791 |
| dualtopo_tuned       |    41.57  |   nan     |          41.57  |
| lstm_s10             |    44.526 |    55.132 |          44.526 |
| lstm                 |    44.91  |    58.288 |          44.91  |
| xgboost              |    45.431 |    51.114 |          45.431 |
| climatology          |    46.591 |    59.832 |          46.591 |
| seasonal_naive       |    47.622 |    58.723 |          47.622 |

### Corr

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| colagnn_tuned        |     0.831 |   nan     |           0.831 |
| gnn_st               |     0.83  |     0.825 |           0.83  |
| gnn_st_tuned         |     0.827 |   nan     |           0.827 |
| gnn_st_nograph_tuned |     0.821 |   nan     |           0.821 |
| gnn_st_nograph       |     0.82  |     0.825 |           0.82  |
| blend_baseline       |     0.818 |     0.811 |           0.818 |
| persistence          |     0.808 |     0.791 |           0.808 |
| flusight_baseline    |     0.808 |     0.797 |           0.808 |
| lstm_parity          |     0.802 |     0.801 |           0.802 |
| lstm_tuned           |     0.797 |   nan     |           0.797 |
| arima                |     0.764 |     0.77  |           0.764 |
| sarima               |     0.695 |     0.79  |           0.695 |
| xgboost_tuned        |     0.691 |   nan     |           0.691 |
| xgboost_parity       |     0.668 |     0.811 |           0.668 |
| lstm                 |     0.614 |     0.677 |           0.614 |
| climatology          |     0.608 |     0.68  |           0.608 |
| lstm_s10             |     0.6   |     0.688 |           0.6   |
| gat_parity           |     0.581 |     0.733 |           0.581 |
| xgboost              |     0.581 |     0.718 |           0.581 |
| gat_tuned            |     0.569 |   nan     |           0.569 |
| seasonal_naive       |     0.56  |     0.556 |           0.56  |
| dualtopo_tuned       |     0.477 |   nan     |           0.477 |

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
| gnn_st_nograph | 0 of 1 |
| gnn_st_nograph_tuned | 0 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 1 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 1 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 1 of 1 |
| xgboost_tuned | 1 of 1 |

## Horizon 2

### MAE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| gnn_st_tuned         |    13.083 |   nan     |          13.083 |
| blend_baseline       |    13.128 |    12.545 |          13.128 |
| gnn_st_nograph_tuned |    13.157 |   nan     |          13.157 |
| gnn_st_nograph       |    13.442 |    12.566 |          13.442 |
| lstm_tuned           |    13.926 |   nan     |          13.926 |
| gnn_st               |    14.076 |    12.54  |          14.076 |
| persistence          |    14.187 |    13.336 |          14.187 |
| lstm_parity          |    14.192 |    12.525 |          14.192 |
| flusight_baseline    |    14.261 |    13.34  |          14.261 |
| colagnn_tuned        |    16.571 |   nan     |          16.571 |
| arima                |    17.234 |    13.816 |          17.234 |
| sarima               |    19.539 |    14.503 |          19.539 |
| xgboost_parity       |    22.849 |    18.463 |          22.849 |
| xgboost_tuned        |    23.019 |   nan     |          23.019 |
| lstm_s10             |    24.523 |    25.55  |          24.523 |
| xgboost              |    24.85  |    22.632 |          24.85  |
| lstm                 |    24.896 |    25.811 |          24.896 |
| seasonal_naive       |    25.066 |    26.136 |          25.066 |
| climatology          |    25.395 |    25.566 |          25.395 |

### WIS

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| blend_baseline       |     9.437 |     8.745 |           9.437 |
| gnn_st_tuned         |     9.452 |   nan     |           9.452 |
| gnn_st_nograph_tuned |     9.571 |   nan     |           9.571 |
| gnn_st_nograph       |     9.764 |     8.797 |           9.764 |
| lstm_tuned           |     9.831 |   nan     |           9.831 |
| persistence          |     9.96  |     9.138 |           9.96  |
| flusight_baseline    |     9.969 |     9.278 |           9.969 |
| gnn_st               |     9.992 |     8.786 |           9.992 |
| lstm_parity          |    10.121 |     8.706 |          10.121 |
| colagnn_tuned        |    12.061 |   nan     |          12.061 |
| arima                |    12.955 |     9.502 |          12.955 |
| sarima               |    14.826 |     9.924 |          14.826 |
| xgboost_parity       |    16.228 |    13.044 |          16.228 |
| xgboost_tuned        |    16.296 |   nan     |          16.296 |
| xgboost              |    17.647 |    16.532 |          17.647 |
| climatology          |    17.971 |    19.222 |          17.971 |
| seasonal_naive       |    18.018 |    19.538 |          18.018 |
| lstm_s10             |    20.878 |    18.876 |          20.878 |
| lstm                 |    21.353 |    19.617 |          21.353 |

### RMSE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| gnn_st_tuned         |    25.623 |   nan     |          25.623 |
| blend_baseline       |    25.673 |    27.108 |          25.673 |
| gnn_st_nograph_tuned |    25.85  |   nan     |          25.85  |
| gnn_st_nograph       |    26.12  |    27.817 |          26.12  |
| gnn_st               |    27.33  |    27.8   |          27.33  |
| persistence          |    27.793 |    28     |          27.793 |
| flusight_baseline    |    27.843 |    28.001 |          27.843 |
| lstm_parity          |    28.107 |    27.471 |          28.107 |
| lstm_tuned           |    28.229 |   nan     |          28.229 |
| colagnn_tuned        |    30.531 |   nan     |          30.531 |
| arima                |    32.167 |    27.778 |          32.167 |
| sarima               |    37.981 |    28.224 |          37.981 |
| xgboost_parity       |    42.144 |    42.262 |          42.144 |
| xgboost_tuned        |    42.275 |   nan     |          42.275 |
| xgboost              |    46.528 |    54.435 |          46.528 |
| climatology          |    46.591 |    59.832 |          46.591 |
| lstm_s10             |    47.319 |    58.71  |          47.319 |
| seasonal_naive       |    47.622 |    58.725 |          47.622 |
| lstm                 |    47.873 |    62.625 |          47.873 |

### Corr

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| gnn_st               |     0.773 |     0.763 |           0.773 |
| colagnn_tuned        |     0.766 |   nan     |           0.766 |
| gnn_st_nograph       |     0.762 |     0.763 |           0.762 |
| gnn_st_tuned         |     0.76  |   nan     |           0.76  |
| gnn_st_nograph_tuned |     0.756 |   nan     |           0.756 |
| blend_baseline       |     0.745 |     0.748 |           0.745 |
| lstm_tuned           |     0.735 |   nan     |           0.735 |
| lstm_parity          |     0.725 |     0.753 |           0.725 |
| persistence          |     0.716 |     0.721 |           0.716 |
| flusight_baseline    |     0.716 |     0.721 |           0.716 |
| arima                |     0.611 |     0.7   |           0.611 |
| climatology          |     0.608 |     0.68  |           0.608 |
| sarima               |     0.602 |     0.721 |           0.602 |
| xgboost_parity       |     0.574 |     0.753 |           0.574 |
| seasonal_naive       |     0.56  |     0.556 |           0.56  |
| xgboost_tuned        |     0.554 |   nan     |           0.554 |
| xgboost              |     0.539 |     0.692 |           0.539 |
| lstm                 |     0.481 |     0.618 |           0.481 |
| lstm_s10             |     0.47  |     0.624 |           0.47  |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 1 of 1 |
| blend_baseline | 0 of 1 |
| climatology | 1 of 1 |
| colagnn_tuned | 1 of 1 |
| flusight_baseline | 1 of 1 |
| gnn_st_nograph | 0 of 1 |
| gnn_st_nograph_tuned | 0 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 1 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 0 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 1 of 1 |
| xgboost_tuned | 1 of 1 |

## Horizon 4

### MAE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| lstm_tuned           |    17.044 |   nan     |          17.044 |
| blend_baseline       |    17.045 |    16.239 |          17.045 |
| lstm_parity          |    17.905 |    17.31  |          17.905 |
| gnn_st_tuned         |    18.311 |   nan     |          18.311 |
| gnn_st_nograph_tuned |    18.427 |   nan     |          18.427 |
| gnn_st_nograph       |    19.447 |    17.513 |          19.447 |
| gnn_st               |    19.63  |    17.149 |          19.63  |
| persistence          |    19.755 |    18.961 |          19.755 |
| flusight_baseline    |    19.83  |    18.963 |          19.83  |
| colagnn_tuned        |    20.176 |   nan     |          20.176 |
| arima                |    21.183 |    21.679 |          21.183 |
| sarima               |    23.59  |    18.515 |          23.59  |
| lstm_s10             |    24.737 |    26.713 |          24.737 |
| seasonal_naive       |    25.066 |    26.14  |          25.066 |
| xgboost_parity       |    25.115 |    22.444 |          25.115 |
| lstm                 |    25.132 |    28.21  |          25.132 |
| xgboost_tuned        |    25.168 |   nan     |          25.168 |
| climatology          |    25.395 |    25.566 |          25.395 |
| xgboost              |    25.998 |    23.867 |          25.998 |

### WIS

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| blend_baseline       |    12.643 |    11.784 |          12.643 |
| lstm_tuned           |    12.665 |   nan     |          12.665 |
| gnn_st_tuned         |    12.948 |   nan     |          12.948 |
| lstm_parity          |    12.955 |    12.032 |          12.955 |
| gnn_st_nograph_tuned |    12.993 |   nan     |          12.993 |
| gnn_st               |    13.657 |    12.216 |          13.657 |
| gnn_st_nograph       |    13.718 |    12.469 |          13.718 |
| flusight_baseline    |    13.866 |    13.04  |          13.866 |
| persistence          |    14.542 |    13.234 |          14.542 |
| colagnn_tuned        |    14.802 |   nan     |          14.802 |
| arima                |    16.716 |    15.445 |          16.716 |
| sarima               |    17.375 |    12.629 |          17.375 |
| xgboost_parity       |    17.874 |    16.018 |          17.874 |
| xgboost_tuned        |    17.928 |   nan     |          17.928 |
| climatology          |    17.971 |    19.222 |          17.971 |
| seasonal_naive       |    18.018 |    19.541 |          18.018 |
| xgboost              |    18.31  |    17.454 |          18.31  |
| lstm_s10             |    19.712 |    19.921 |          19.712 |
| lstm                 |    20.345 |    21.104 |          20.345 |

### RMSE

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| blend_baseline       |    31.933 |    36.716 |          31.933 |
| lstm_tuned           |    33.231 |   nan     |          33.231 |
| gnn_st_tuned         |    33.783 |   nan     |          33.783 |
| lstm_parity          |    33.909 |    38.969 |          33.909 |
| gnn_st_nograph_tuned |    33.912 |   nan     |          33.912 |
| gnn_st_nograph       |    35.878 |    40.927 |          35.878 |
| gnn_st               |    36.597 |    40.154 |          36.597 |
| colagnn_tuned        |    36.985 |   nan     |          36.985 |
| persistence          |    37.584 |    39.618 |          37.584 |
| flusight_baseline    |    37.621 |    39.618 |          37.621 |
| arima                |    39.698 |    40.947 |          39.698 |
| lstm_s10             |    44.282 |    59.628 |          44.282 |
| lstm                 |    45.529 |    63.594 |          45.529 |
| xgboost_parity       |    46.106 |    52.327 |          46.106 |
| xgboost_tuned        |    46.314 |   nan     |          46.314 |
| climatology          |    46.591 |    59.832 |          46.591 |
| sarima               |    47.242 |    36.059 |          47.242 |
| xgboost              |    47.448 |    56.243 |          47.448 |
| seasonal_naive       |    47.622 |    58.729 |          47.622 |

### Corr

| arm                  |   2023_24 |   2024_25 |   evidence mean |
|:---------------------|----------:|----------:|----------------:|
| lstm_tuned           |     0.679 |   nan     |           0.679 |
| gnn_st               |     0.675 |     0.712 |           0.675 |
| gnn_st_tuned         |     0.669 |   nan     |           0.669 |
| gnn_st_nograph       |     0.665 |     0.709 |           0.665 |
| gnn_st_nograph_tuned |     0.663 |   nan     |           0.663 |
| colagnn_tuned        |     0.659 |   nan     |           0.659 |
| lstm_parity          |     0.658 |     0.685 |           0.658 |
| blend_baseline       |     0.615 |     0.636 |           0.615 |
| climatology          |     0.608 |     0.68  |           0.608 |
| sarima               |     0.591 |     0.612 |           0.591 |
| seasonal_naive       |     0.56  |     0.557 |           0.56  |
| xgboost_parity       |     0.544 |     0.675 |           0.544 |
| xgboost_tuned        |     0.53  |   nan     |           0.53  |
| xgboost              |     0.509 |     0.638 |           0.509 |
| persistence          |     0.494 |     0.539 |           0.494 |
| flusight_baseline    |     0.493 |     0.538 |           0.493 |
| arima                |     0.414 |     0.453 |           0.414 |
| lstm_s10             |     0.326 |     0.544 |           0.326 |
| lstm                 |     0.248 |     0.467 |           0.248 |

Evidence seasons in which `gnn_st` has the lower MAE:

| other arm | seasons won |
| --- | --- |
| arima | 1 of 1 |
| blend_baseline | 0 of 1 |
| climatology | 1 of 1 |
| colagnn_tuned | 1 of 1 |
| flusight_baseline | 1 of 1 |
| gnn_st_nograph | 0 of 1 |
| gnn_st_nograph_tuned | 0 of 1 |
| gnn_st_tuned | 0 of 1 |
| lstm | 1 of 1 |
| lstm_parity | 0 of 1 |
| lstm_s10 | 1 of 1 |
| lstm_tuned | 0 of 1 |
| persistence | 1 of 1 |
| sarima | 1 of 1 |
| seasonal_naive | 1 of 1 |
| xgboost | 1 of 1 |
| xgboost_parity | 1 of 1 |
| xgboost_tuned | 1 of 1 |

Per-fold significance (block bootstrap and Diebold-Mariano) is in each fold's
`_comparison/significance.md`, written by compare_significance.py.
