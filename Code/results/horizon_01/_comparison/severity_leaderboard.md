Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.606 |
| arima | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.598 |
| dualtopo | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.078 |
| gat | post_covid | 4 | 0.082 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.228 | 0.178 |
| gnn_st | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.779 |
| gnn_st_lagsonly | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.712 |
| gnn_st_noglobals | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.782 |
| lstm | exclude_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.540 |
| lstm | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.595 |
| persistence | exclude_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.584 |
| persistence | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.584 |
| seasonal_naive | exclude_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.675 |
| seasonal_naive | post_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.489 |
| xgboost | post_covid | 4 | 0.082 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.594 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.203 |
| arima | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.212 |
| dualtopo | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gat | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.024 |
| gnn_st | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.108 |
| gnn_st_lagsonly | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.124 |
| gnn_st_noglobals | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.101 |
| lstm | exclude_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -0.350 |
| lstm | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.073 |
| persistence | exclude_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.297 |
| persistence | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.296 |
| seasonal_naive | exclude_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.528 |
| seasonal_naive | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.502 |
| xgboost | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.031 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_lagsonly | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_noglobals | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 49 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 49 | 0.959 | 0.980 | 0.418 | -0.061 |
| arima | exclude_covid | 49 | 0.939 | 1.000 | 0.705 | -0.020 |
| arima | post_covid | 49 | 0.939 | 1.000 | 0.705 | -0.020 |
| lstm | post_covid | 49 | 0.939 | 1.000 | 0.705 | -0.020 |
| dualtopo | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| gat | post_covid | 49 | 0.918 | 0.980 | 0.185 | -0.061 |
| gnn_st | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| gnn_st_lagsonly | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| gnn_st_noglobals | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| persistence | exclude_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| persistence | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| lstm | exclude_covid | 49 | 0.898 | 1.000 | 0.683 | 0.020 |
| seasonal_naive | exclude_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |
| seasonal_naive | post_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.572 |
| arima | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.564 |
| dualtopo | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.170 |
| gat | post_covid | 4 | 0.154 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.205 | 0.108 |
| gnn_st | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.760 |
| gnn_st_lagsonly | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.688 |
| gnn_st_noglobals | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.764 |
| lstm | exclude_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.501 |
| lstm | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.560 |
| persistence | exclude_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.548 |
| persistence | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.548 |
| seasonal_naive | exclude_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.817 |
| seasonal_naive | post_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.610 |
| xgboost | post_covid | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.560 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.226 |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.235 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.044 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.129 |
| gnn_st_lagsonly | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.145 |
| gnn_st_noglobals | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.122 |
| lstm | exclude_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -0.375 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.093 |
| persistence | exclude_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.321 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.321 |
| seasonal_naive | exclude_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.575 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.548 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.013 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_lagsonly | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_noglobals | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 26 | 0.923 | 0.962 | 0.393 | -0.115 |
| arima | exclude_covid | 26 | 0.885 | 1.000 | 0.683 | -0.038 |
| arima | post_covid | 26 | 0.885 | 1.000 | 0.683 | -0.038 |
| lstm | post_covid | 26 | 0.885 | 1.000 | 0.683 | -0.038 |
| dualtopo | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| gat | post_covid | 26 | 0.846 | 0.962 | 0.150 | -0.115 |
| gnn_st | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| gnn_st_lagsonly | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| gnn_st_noglobals | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| persistence | exclude_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| persistence | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| lstm | exclude_covid | 26 | 0.808 | 1.000 | 0.660 | 0.038 |
| seasonal_naive | exclude_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |
| seasonal_naive | post_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 51 | 0.081 | 40 | 11 | 10 | 0.784 | 0.200 | 0.656 | 0.792 | 0.767 | 0.709 |
| gnn_st_noglobals | post_covid | 51 | 0.081 | 40 | 11 | 10 | 0.784 | 0.200 | 0.656 | 0.792 | 0.767 | 0.712 |
| gnn_st_lagsonly | post_covid | 51 | 0.081 | 40 | 11 | 13 | 0.784 | 0.245 | 0.625 | 0.769 | 0.762 | 0.664 |
| lstm | exclude_covid | 51 | 0.081 | 40 | 11 | 16 | 0.784 | 0.286 | 0.597 | 0.748 | 0.757 | 0.554 |
| lstm | post_covid | 51 | 0.081 | 38 | 13 | 9 | 0.745 | 0.191 | 0.633 | 0.776 | 0.729 | 0.591 |
| persistence | exclude_covid | 51 | 0.081 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.680 | 0.528 |
| persistence | post_covid | 51 | 0.081 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.680 | 0.528 |
| arima | post_covid | 51 | 0.081 | 35 | 16 | 10 | 0.686 | 0.222 | 0.574 | 0.729 | 0.669 | 0.529 |
| arima | exclude_covid | 51 | 0.081 | 33 | 18 | 12 | 0.647 | 0.267 | 0.524 | 0.688 | 0.626 | 0.521 |
| xgboost | post_covid | 51 | 0.081 | 32 | 19 | 13 | 0.627 | 0.289 | 0.500 | 0.667 | 0.605 | 0.492 |
| gat | post_covid | 51 | 0.081 | 15 | 36 | 14 | 0.294 | 0.483 | 0.231 | 0.375 | 0.270 | 0.188 |
| dualtopo | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |
| seasonal_naive | exclude_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.667 |
| seasonal_naive | post_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.545 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 18 | 0.029 | 8 | 10 | 3 | 0.444 | 0.273 | 0.381 | 0.552 | 0.440 | 0.367 |
| gnn_st_noglobals | post_covid | 18 | 0.029 | 8 | 10 | 3 | 0.444 | 0.273 | 0.381 | 0.552 | 0.440 | 0.369 |
| persistence | exclude_covid | 18 | 0.029 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.428 | 0.205 |
| persistence | post_covid | 18 | 0.029 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.428 | 0.205 |
| gnn_st_lagsonly | post_covid | 18 | 0.029 | 7 | 11 | 3 | 0.389 | 0.300 | 0.333 | 0.500 | 0.384 | 0.345 |
| arima | post_covid | 18 | 0.029 | 6 | 12 | 7 | 0.333 | 0.538 | 0.240 | 0.387 | 0.322 | 0.183 |
| arima | exclude_covid | 18 | 0.029 | 4 | 14 | 3 | 0.222 | 0.429 | 0.190 | 0.320 | 0.217 | 0.186 |
| lstm | exclude_covid | 18 | 0.029 | 2 | 16 | 9 | 0.111 | 0.818 | 0.074 | 0.138 | 0.096 | 0.134 |
| dualtopo | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.030 |
| gat | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.003 |
| lstm | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.221 |
| xgboost | post_covid | 18 | 0.029 | 0 | 18 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.202 |
| seasonal_naive | exclude_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.972 |
| seasonal_naive | post_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.934 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.137 |
| arima | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.263 |
| dualtopo | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gat | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.004 |
| gnn_st | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.211 |
| gnn_st_lagsonly | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.199 |
| gnn_st_noglobals | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.213 |
| lstm | exclude_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.037 |
| lstm | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.024 |
| persistence | exclude_covid | 2 | 0.003 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.498 | -0.259 |
| persistence | post_covid | 2 | 0.003 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.498 | -0.260 |
| seasonal_naive | exclude_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.016 |
| seasonal_naive | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.871 |
| xgboost | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.183 |

### All four bands — 627 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 627 | 0.946 | 0.997 | 0.783 | -0.016 |
| gnn_st_noglobals | post_covid | 627 | 0.946 | 0.997 | 0.783 | -0.016 |
| gnn_st_lagsonly | post_covid | 627 | 0.939 | 0.997 | 0.761 | -0.013 |
| lstm | post_covid | 627 | 0.939 | 0.994 | 0.670 | -0.038 |
| arima | post_covid | 627 | 0.936 | 0.990 | 0.661 | -0.021 |
| arima | exclude_covid | 627 | 0.935 | 0.989 | 0.604 | -0.030 |
| persistence | exclude_covid | 627 | 0.928 | 0.990 | 0.682 | 0.000 |
| persistence | post_covid | 627 | 0.928 | 0.990 | 0.682 | 0.000 |
| xgboost | post_covid | 627 | 0.928 | 0.989 | 0.535 | -0.040 |
| lstm | exclude_covid | 627 | 0.920 | 0.994 | 0.672 | -0.006 |
| dualtopo | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| gat | post_covid | 627 | 0.912 | 0.979 | 0.243 | -0.067 |
| seasonal_naive | exclude_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |
| seasonal_naive | post_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 51 | 0.145 | 40 | 11 | 10 | 0.784 | 0.200 | 0.656 | 0.792 | 0.751 | 0.688 |
| gnn_st_noglobals | post_covid | 51 | 0.145 | 40 | 11 | 10 | 0.784 | 0.200 | 0.656 | 0.792 | 0.751 | 0.690 |
| gnn_st_lagsonly | post_covid | 51 | 0.145 | 40 | 11 | 13 | 0.784 | 0.245 | 0.625 | 0.769 | 0.741 | 0.639 |
| lstm | exclude_covid | 51 | 0.145 | 40 | 11 | 16 | 0.784 | 0.286 | 0.597 | 0.748 | 0.731 | 0.521 |
| lstm | post_covid | 51 | 0.145 | 38 | 13 | 9 | 0.745 | 0.191 | 0.633 | 0.776 | 0.715 | 0.561 |
| persistence | exclude_covid | 51 | 0.145 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.656 | 0.494 |
| persistence | post_covid | 51 | 0.145 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.656 | 0.494 |
| arima | post_covid | 51 | 0.145 | 35 | 16 | 10 | 0.686 | 0.222 | 0.574 | 0.729 | 0.653 | 0.496 |
| arima | exclude_covid | 51 | 0.145 | 33 | 18 | 12 | 0.647 | 0.267 | 0.524 | 0.688 | 0.607 | 0.486 |
| xgboost | post_covid | 51 | 0.145 | 32 | 19 | 13 | 0.627 | 0.289 | 0.500 | 0.667 | 0.584 | 0.461 |
| gat | post_covid | 51 | 0.145 | 15 | 36 | 14 | 0.294 | 0.483 | 0.231 | 0.375 | 0.248 | 0.128 |
| dualtopo | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.131 |
| seasonal_naive | exclude_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.775 |
| seasonal_naive | post_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.625 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 18 | 0.051 | 8 | 10 | 3 | 0.444 | 0.273 | 0.381 | 0.552 | 0.435 | 0.352 |
| gnn_st_noglobals | post_covid | 18 | 0.051 | 8 | 10 | 3 | 0.444 | 0.273 | 0.381 | 0.552 | 0.435 | 0.354 |
| persistence | exclude_covid | 18 | 0.051 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.415 | 0.187 |
| persistence | post_covid | 18 | 0.051 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.415 | 0.187 |
| gnn_st_lagsonly | post_covid | 18 | 0.051 | 7 | 11 | 3 | 0.389 | 0.300 | 0.333 | 0.500 | 0.380 | 0.330 |
| arima | post_covid | 18 | 0.051 | 6 | 12 | 7 | 0.333 | 0.538 | 0.240 | 0.387 | 0.312 | 0.164 |
| arima | exclude_covid | 18 | 0.051 | 4 | 14 | 3 | 0.222 | 0.429 | 0.190 | 0.320 | 0.213 | 0.167 |
| lstm | exclude_covid | 18 | 0.051 | 2 | 16 | 9 | 0.111 | 0.818 | 0.074 | 0.138 | 0.084 | 0.113 |
| dualtopo | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| gat | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| lstm | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.202 |
| xgboost | post_covid | 18 | 0.051 | 0 | 18 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.183 |
| seasonal_naive | exclude_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -1.017 |
| seasonal_naive | post_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -0.974 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.140 |
| arima | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.267 |
| dualtopo | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gat | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gnn_st | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.209 |
| gnn_st_lagsonly | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.197 |
| gnn_st_noglobals | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.211 |
| lstm | exclude_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.035 |
| lstm | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.021 |
| persistence | exclude_covid | 2 | 0.006 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.497 | -0.263 |
| persistence | post_covid | 2 | 0.006 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.497 | -0.263 |
| seasonal_naive | exclude_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.026 |
| seasonal_naive | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.880 |
| xgboost | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.186 |

### All four bands — 352 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 352 | 0.903 | 0.994 | 0.769 | -0.028 |
| gnn_st_noglobals | post_covid | 352 | 0.903 | 0.994 | 0.769 | -0.028 |
| gnn_st_lagsonly | post_covid | 352 | 0.892 | 0.994 | 0.745 | -0.023 |
| lstm | post_covid | 352 | 0.892 | 0.989 | 0.650 | -0.068 |
| arima | post_covid | 352 | 0.886 | 0.983 | 0.641 | -0.037 |
| arima | exclude_covid | 352 | 0.884 | 0.980 | 0.581 | -0.054 |
| persistence | exclude_covid | 352 | 0.872 | 0.983 | 0.662 | 0.000 |
| persistence | post_covid | 352 | 0.872 | 0.983 | 0.662 | 0.000 |
| xgboost | post_covid | 352 | 0.872 | 0.980 | 0.508 | -0.071 |
| lstm | exclude_covid | 352 | 0.858 | 0.989 | 0.650 | -0.011 |
| dualtopo | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| gat | post_covid | 352 | 0.844 | 0.963 | 0.214 | -0.119 |
| seasonal_naive | exclude_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |
| seasonal_naive | post_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14 | 1.000 | -1.000 | 0.786 | 1.000 | -3.080 |
| gnn_st_lagsonly | post_covid | 14 | 1.000 | -1.000 | 0.786 | 1.000 | -3.240 |
| gnn_st_noglobals | post_covid | 14 | 1.000 | -1.000 | 0.786 | 1.000 | -3.178 |
| lstm | exclude_covid | 14 | 1.000 | -1.000 | 0.786 | 1.000 | -1.645 |
| lstm | post_covid | 13 | 1.000 | -1.000 | 0.846 | 0.000 | -4.406 |
| persistence | exclude_covid | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| persistence | post_covid | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| arima | post_covid | 13 | 1.000 | -1.000 | 1.077 | 1.000 | 0.000 |
| arima | exclude_covid | 13 | 1.000 | -1.000 | 1.154 | 1.000 | 0.000 |
| xgboost | post_covid | 14 | 1.000 | -1.000 | 1.357 | 0.500 | -3.825 |
| gat | post_covid | 14 | 3.000 | -3.000 | 2.714 | 1.500 | -2.311 |
| seasonal_naive | exclude_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| seasonal_naive | post_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| dualtopo | post_covid | 0 |  |  |  | 3.000 | -4.281 |

# Notes

- 6 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- --plot-models listed 7 models but only 4 validated colours exist; plotting the first 4.
