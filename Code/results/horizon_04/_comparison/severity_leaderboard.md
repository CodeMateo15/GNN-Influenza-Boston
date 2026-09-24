Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.082 | 0 | 4 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.067 | -0.200 |
| arima | post_covid | 4 | 0.082 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | -0.104 |
| dualtopo | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| gat | post_covid | 4 | 0.082 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.089 | -0.528 |
| gnn_st | post_covid | 4 | 0.082 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.044 | 0.110 |
| gnn_st_lagsonly | post_covid | 4 | 0.082 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.044 | 0.102 |
| gnn_st_noglobals | post_covid | 4 | 0.082 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.044 | 0.110 |
| lstm | exclude_covid | 4 | 0.082 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.089 | -0.484 |
| lstm | post_covid | 4 | 0.082 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | -0.038 |
| persistence | exclude_covid | 4 | 0.082 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.089 | -0.450 |
| persistence | post_covid | 4 | 0.082 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.089 | -0.420 |
| seasonal_naive | exclude_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.672 |
| seasonal_naive | post_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.489 |
| xgboost | post_covid | 4 | 0.082 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | 0.143 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.290 |
| arima | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.214 |
| dualtopo | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gat | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |
| gnn_st | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.141 |
| gnn_st_lagsonly | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.146 |
| gnn_st_noglobals | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.141 |
| lstm | exclude_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.327 |
| lstm | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.041 |
| persistence | exclude_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.811 |
| persistence | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.829 |
| seasonal_naive | exclude_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.527 |
| seasonal_naive | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.502 |
| xgboost | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.212 |

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
| dualtopo | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| arima | post_covid | 49 | 0.898 | 0.980 | -0.026 | -0.082 |
| lstm | post_covid | 49 | 0.898 | 0.980 | -0.026 | -0.082 |
| xgboost | post_covid | 49 | 0.898 | 0.980 | -0.026 | -0.082 |
| gnn_st | post_covid | 49 | 0.878 | 0.980 | -0.048 | -0.061 |
| gnn_st_lagsonly | post_covid | 49 | 0.878 | 0.980 | -0.048 | -0.061 |
| gnn_st_noglobals | post_covid | 49 | 0.878 | 0.980 | -0.048 | -0.061 |
| arima | exclude_covid | 49 | 0.857 | 0.980 | -0.065 | -0.041 |
| gat | post_covid | 49 | 0.837 | 0.980 | -0.080 | -0.020 |
| lstm | exclude_covid | 49 | 0.837 | 0.980 | -0.080 | -0.020 |
| persistence | exclude_covid | 49 | 0.837 | 0.959 | -0.079 | 0.000 |
| persistence | post_covid | 49 | 0.837 | 0.959 | -0.079 | 0.000 |
| seasonal_naive | exclude_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |
| seasonal_naive | post_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.154 | 0 | 4 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.136 | -0.278 |
| arima | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | -0.113 |
| dualtopo | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| gat | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.658 |
| gnn_st | post_covid | 4 | 0.154 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.091 | 0.034 |
| gnn_st_lagsonly | post_covid | 4 | 0.154 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.091 | 0.027 |
| gnn_st_noglobals | post_covid | 4 | 0.154 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.091 | 0.034 |
| lstm | exclude_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.578 |
| lstm | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | -0.096 |
| persistence | exclude_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.557 |
| persistence | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.518 |
| seasonal_naive | exclude_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.813 |
| seasonal_naive | post_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.610 |
| xgboost | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | 0.079 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.314 |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.234 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.163 |
| gnn_st_lagsonly | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| gnn_st_noglobals | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.163 |
| lstm | exclude_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.352 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.060 |
| persistence | exclude_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.844 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.862 |
| seasonal_naive | exclude_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.574 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.548 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.235 |

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
| dualtopo | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| arima | post_covid | 26 | 0.808 | 0.962 | -0.051 | -0.154 |
| lstm | post_covid | 26 | 0.808 | 0.962 | -0.051 | -0.154 |
| xgboost | post_covid | 26 | 0.808 | 0.962 | -0.051 | -0.154 |
| gnn_st | post_covid | 26 | 0.769 | 0.962 | -0.093 | -0.115 |
| gnn_st_lagsonly | post_covid | 26 | 0.769 | 0.962 | -0.093 | -0.115 |
| gnn_st_noglobals | post_covid | 26 | 0.769 | 0.962 | -0.093 | -0.115 |
| arima | exclude_covid | 26 | 0.731 | 0.962 | -0.130 | -0.077 |
| gat | post_covid | 26 | 0.692 | 0.962 | -0.163 | -0.038 |
| lstm | exclude_covid | 26 | 0.692 | 0.962 | -0.163 | -0.038 |
| persistence | exclude_covid | 26 | 0.692 | 0.923 | -0.159 | 0.000 |
| persistence | post_covid | 26 | 0.692 | 0.923 | -0.159 | 0.000 |
| seasonal_naive | exclude_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |
| seasonal_naive | post_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 51 | 0.081 | 9 | 42 | 24 | 0.176 | 0.727 | 0.120 | 0.214 | 0.135 | 0.014 |
| lstm | post_covid | 51 | 0.081 | 2 | 49 | 8 | 0.039 | 0.800 | 0.034 | 0.066 | 0.025 | -0.023 |
| gnn_st | post_covid | 51 | 0.081 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | 0.017 | 0.067 |
| gnn_st_lagsonly | post_covid | 51 | 0.081 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | 0.017 | 0.044 |
| gnn_st_noglobals | post_covid | 51 | 0.081 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | 0.017 | 0.067 |
| dualtopo | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.056 |
| seasonal_naive | exclude_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.665 |
| seasonal_naive | post_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.545 |
| arima | post_covid | 51 | 0.081 | 0 | 51 | 20 | 0.000 | 1.000 | 0.000 | 0.000 | -0.035 | -0.280 |
| arima | exclude_covid | 51 | 0.081 | 1 | 50 | 32 | 0.020 | 0.970 | 0.012 | 0.024 | -0.036 | -0.321 |
| lstm | exclude_covid | 51 | 0.081 | 2 | 49 | 46 | 0.039 | 0.958 | 0.021 | 0.040 | -0.041 | -0.428 |
| persistence | exclude_covid | 51 | 0.081 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.046 | -0.494 |
| persistence | post_covid | 51 | 0.081 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.046 | -0.481 |
| gat | post_covid | 51 | 0.081 | 0 | 51 | 41 | 0.000 | 1.000 | 0.000 | 0.000 | -0.071 | -0.497 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.200 |
| dualtopo | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| gat | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.082 |
| gnn_st | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| gnn_st_lagsonly | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.039 |
| gnn_st_noglobals | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| lstm | exclude_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.209 |
| lstm | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |
| arima | exclude_covid | 18 | 0.029 | 0 | 18 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.008 | -0.292 |
| xgboost | post_covid | 18 | 0.029 | 0 | 18 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.008 | -0.114 |
| persistence | exclude_covid | 18 | 0.029 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.030 | -0.607 |
| persistence | post_covid | 18 | 0.029 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.030 | -0.615 |
| seasonal_naive | exclude_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.971 |
| seasonal_naive | post_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.934 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.658 |
| arima | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.415 |
| dualtopo | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gat | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gnn_st | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.094 |
| gnn_st_lagsonly | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.141 |
| gnn_st_noglobals | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.094 |
| lstm | exclude_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.104 |
| lstm | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| persistence | exclude_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.945 |
| persistence | post_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -2.121 |
| seasonal_naive | exclude_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.028 |
| seasonal_naive | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.871 |
| xgboost | post_covid | 2 | 0.003 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -1.183 |

### All four bands — 627 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| lstm | post_covid | 627 | 0.909 | 0.971 | 0.014 | -0.097 |
| xgboost | post_covid | 627 | 0.892 | 0.967 | 0.083 | -0.051 |
| arima | post_covid | 627 | 0.887 | 0.971 | -0.035 | -0.081 |
| gnn_st | post_covid | 627 | 0.885 | 0.971 | -0.001 | -0.070 |
| gnn_st_noglobals | post_covid | 627 | 0.885 | 0.971 | -0.001 | -0.070 |
| gnn_st_lagsonly | post_covid | 627 | 0.884 | 0.973 | 0.014 | -0.070 |
| arima | exclude_covid | 627 | 0.869 | 0.963 | -0.043 | -0.053 |
| gat | post_covid | 627 | 0.853 | 0.971 | -0.063 | -0.048 |
| lstm | exclude_covid | 627 | 0.848 | 0.971 | -0.045 | -0.037 |
| persistence | exclude_covid | 627 | 0.844 | 0.943 | -0.056 | 0.000 |
| persistence | post_covid | 627 | 0.844 | 0.943 | -0.056 | 0.000 |
| seasonal_naive | exclude_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |
| seasonal_naive | post_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 51 | 0.145 | 9 | 42 | 24 | 0.176 | 0.727 | 0.120 | 0.214 | 0.097 | -0.027 |
| lstm | post_covid | 51 | 0.145 | 2 | 49 | 8 | 0.039 | 0.800 | 0.034 | 0.066 | 0.013 | -0.053 |
| dualtopo | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.128 |
| gnn_st | post_covid | 51 | 0.145 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | -0.021 | 0.004 |
| gnn_st_lagsonly | post_covid | 51 | 0.145 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | -0.021 | -0.017 |
| gnn_st_noglobals | post_covid | 51 | 0.145 | 3 | 48 | 24 | 0.059 | 0.889 | 0.040 | 0.077 | -0.021 | 0.004 |
| arima | post_covid | 51 | 0.145 | 0 | 51 | 20 | 0.000 | 1.000 | 0.000 | 0.000 | -0.066 | -0.213 |
| arima | exclude_covid | 51 | 0.145 | 1 | 50 | 32 | 0.020 | 0.970 | 0.012 | 0.024 | -0.087 | -0.338 |
| lstm | exclude_covid | 51 | 0.145 | 2 | 49 | 46 | 0.039 | 0.958 | 0.021 | 0.040 | -0.114 | -0.498 |
| persistence | exclude_covid | 51 | 0.145 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.124 | -0.554 |
| persistence | post_covid | 51 | 0.145 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.124 | -0.531 |
| gat | post_covid | 51 | 0.145 | 0 | 51 | 41 | 0.000 | 1.000 | 0.000 | 0.000 | -0.136 | -0.607 |
| seasonal_naive | exclude_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.772 |
| seasonal_naive | post_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.625 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.197 |
| dualtopo | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| gat | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.108 |
| gnn_st | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.059 |
| gnn_st_lagsonly | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.063 |
| gnn_st_noglobals | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.059 |
| lstm | exclude_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.237 |
| lstm | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.042 |
| arima | exclude_covid | 18 | 0.051 | 0 | 18 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.313 |
| xgboost | post_covid | 18 | 0.051 | 0 | 18 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.136 |
| persistence | exclude_covid | 18 | 0.051 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.054 | -0.636 |
| persistence | post_covid | 18 | 0.051 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.054 | -0.640 |
| seasonal_naive | exclude_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -1.016 |
| seasonal_naive | post_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -0.974 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.658 |
| arima | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.393 |
| dualtopo | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gat | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.024 |
| gnn_st | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.097 |
| gnn_st_lagsonly | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.143 |
| gnn_st_noglobals | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.097 |
| lstm | exclude_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.107 |
| lstm | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.018 |
| persistence | exclude_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -1.947 |
| persistence | post_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -2.121 |
| seasonal_naive | exclude_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.038 |
| seasonal_naive | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.880 |
| xgboost | post_covid | 2 | 0.006 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.186 |

### All four bands — 352 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| lstm | post_covid | 352 | 0.838 | 0.949 | -0.000 | -0.173 |
| xgboost | post_covid | 352 | 0.807 | 0.940 | 0.041 | -0.091 |
| arima | post_covid | 352 | 0.798 | 0.949 | -0.064 | -0.145 |
| gnn_st | post_covid | 352 | 0.795 | 0.949 | -0.037 | -0.125 |
| gnn_st_noglobals | post_covid | 352 | 0.795 | 0.949 | -0.037 | -0.125 |
| gnn_st_lagsonly | post_covid | 352 | 0.793 | 0.952 | -0.022 | -0.125 |
| arima | exclude_covid | 352 | 0.767 | 0.935 | -0.090 | -0.094 |
| gat | post_covid | 352 | 0.739 | 0.949 | -0.119 | -0.085 |
| lstm | exclude_covid | 352 | 0.730 | 0.949 | -0.107 | -0.065 |
| persistence | exclude_covid | 352 | 0.722 | 0.898 | -0.122 | 0.000 |
| persistence | post_covid | 352 | 0.722 | 0.898 | -0.122 | 0.000 |
| seasonal_naive | exclude_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |
| seasonal_naive | post_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 8 | 3.000 | -3.000 | 2.625 | 2.000 | -6.730 |
| seasonal_naive | exclude_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| seasonal_naive | post_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| gnn_st | post_covid | 14 | 4.000 | -4.000 | 3.643 | 2.000 | -9.621 |
| gnn_st_lagsonly | post_covid | 14 | 4.000 | -4.000 | 3.643 | 2.500 | -9.821 |
| gnn_st_noglobals | post_covid | 14 | 4.000 | -4.000 | 3.643 | 2.000 | -9.621 |
| lstm | exclude_covid | 14 | 4.000 | -4.000 | 3.786 | 4.000 | -5.426 |
| lstm | post_covid | 7 | 4.000 | -4.000 | 4.000 | 3.000 | -10.503 |
| persistence | exclude_covid | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| persistence | post_covid | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| arima | exclude_covid | 12 | 4.000 | -4.000 | 4.333 | 4.000 | 0.000 |
| arima | post_covid | 10 | 5.000 | -5.000 | 4.600 | 4.000 | -3.144 |
| gat | post_covid | 14 | 6.000 | -6.000 | 6.357 | 4.000 | -6.694 |
| dualtopo | post_covid | 0 |  |  |  | 2.000 | -4.295 |

# Notes

- 20 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- --plot-models listed 7 models but only 4 validated colours exist; plotting the first 4.
