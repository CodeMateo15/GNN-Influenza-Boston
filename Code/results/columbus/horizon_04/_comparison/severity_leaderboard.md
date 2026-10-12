Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.233 |
| gat | post_covid | 8 | 0.151 | 3 | 5 | 5 | 0.375 | 0.625 | 0.231 | 0.375 | 0.264 | -0.298 |
| persistence | post_covid | 8 | 0.151 | 3 | 5 | 5 | 0.375 | 0.625 | 0.231 | 0.375 | 0.264 | 0.056 |
| dualtopo | post_covid | 8 | 0.151 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.292 |
| gnn_st | post_covid | 8 | 0.151 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.103 | 0.371 |
| arima | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.126 |
| xgboost | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.415 |
| lstm | post_covid | 8 | 0.151 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | 0.086 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 4 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 4 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 53 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 53 | 0.868 | 1.000 | 0.195 | -0.132 |
| arima | post_covid | 53 | 0.849 | 1.000 | 0.000 | -0.151 |
| gnn_st | post_covid | 53 | 0.849 | 1.000 | 0.149 | -0.113 |
| xgboost | post_covid | 53 | 0.849 | 1.000 | 0.000 | -0.151 |
| lstm | post_covid | 53 | 0.830 | 1.000 | -0.035 | -0.132 |
| seasonal_naive | post_covid | 53 | 0.830 | 0.943 | 0.209 | 0.094 |
| persistence | post_covid | 53 | 0.811 | 1.000 | 0.264 | 0.000 |
| gat | post_covid | 53 | 0.774 | 0.962 | 0.262 | 0.075 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.099 |
| dualtopo | post_covid | 8 | 0.308 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.132 |
| gat | post_covid | 8 | 0.308 | 3 | 5 | 5 | 0.375 | 0.625 | 0.231 | 0.375 | 0.097 | -0.592 |
| persistence | post_covid | 8 | 0.308 | 3 | 5 | 5 | 0.375 | 0.625 | 0.231 | 0.375 | 0.097 | -0.097 |
| gnn_st | post_covid | 8 | 0.308 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.069 | 0.230 |
| arima | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.043 |
| xgboost | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.283 |
| lstm | post_covid | 8 | 0.308 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.050 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 4 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 4 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 26 | 0.731 | 1.000 | 0.165 | -0.269 |
| arima | post_covid | 26 | 0.692 | 1.000 | 0.000 | -0.308 |
| gnn_st | post_covid | 26 | 0.692 | 1.000 | 0.088 | -0.231 |
| xgboost | post_covid | 26 | 0.692 | 1.000 | 0.000 | -0.308 |
| lstm | post_covid | 26 | 0.654 | 1.000 | -0.073 | -0.269 |
| seasonal_naive | post_covid | 26 | 0.654 | 0.885 | 0.080 | 0.192 |
| persistence | post_covid | 26 | 0.615 | 1.000 | 0.097 | 0.000 |
| gat | post_covid | 26 | 0.538 | 0.923 | 0.127 | 0.154 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 118 | 0.131 | 62 | 56 | 87 | 0.525 | 0.584 | 0.302 | 0.464 | 0.414 | -0.074 |
| gat | post_covid | 118 | 0.131 | 37 | 81 | 93 | 0.314 | 0.715 | 0.175 | 0.298 | 0.195 | -0.408 |
| persistence | post_covid | 118 | 0.131 | 32 | 86 | 84 | 0.271 | 0.724 | 0.158 | 0.274 | 0.164 | -0.154 |
| gnn_st | post_covid | 118 | 0.131 | 18 | 100 | 23 | 0.153 | 0.561 | 0.128 | 0.226 | 0.123 | 0.246 |
| xgboost | post_covid | 118 | 0.131 | 10 | 108 | 8 | 0.085 | 0.444 | 0.079 | 0.147 | 0.075 | 0.289 |
| arima | post_covid | 118 | 0.131 | 9 | 109 | 15 | 0.076 | 0.625 | 0.068 | 0.127 | 0.057 | 0.029 |
| dualtopo | post_covid | 118 | 0.131 | 6 | 112 | 7 | 0.051 | 0.538 | 0.048 | 0.092 | 0.042 | 0.144 |
| lstm | post_covid | 118 | 0.131 | 6 | 112 | 8 | 0.051 | 0.571 | 0.048 | 0.091 | 0.041 | 0.017 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 17 | 0.019 | 3 | 14 | 48 | 0.176 | 0.941 | 0.046 | 0.088 | 0.122 | -1.283 |
| persistence | post_covid | 17 | 0.019 | 1 | 16 | 16 | 0.059 | 0.941 | 0.030 | 0.059 | 0.041 | -0.749 |
| seasonal_naive | post_covid | 17 | 0.019 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | 0.001 | -1.629 |
| arima | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.037 |
| dualtopo | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.007 |
| lstm | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.007 |
| xgboost | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.087 |
| gnn_st | post_covid | 17 | 0.019 | 0 | 17 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | 0.052 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.074 |
| dualtopo | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.004 |
| gat | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.514 |
| gnn_st | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.007 |
| lstm | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.028 |
| persistence | post_covid | 4 | 0.004 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -1.166 |
| seasonal_naive | post_covid | 4 | 0.004 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.013 | -2.990 |
| xgboost | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.029 |

### All four bands — 901 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 901 | 0.869 | 0.982 | 0.101 | -0.134 |
| dualtopo | post_covid | 901 | 0.868 | 0.981 | 0.040 | -0.140 |
| lstm | post_covid | 901 | 0.866 | 0.982 | 0.049 | -0.139 |
| arima | post_covid | 901 | 0.861 | 0.982 | 0.061 | -0.128 |
| gnn_st | post_covid | 901 | 0.859 | 0.984 | 0.141 | -0.108 |
| seasonal_naive | post_covid | 901 | 0.817 | 0.943 | 0.246 | 0.082 |
| persistence | post_covid | 901 | 0.797 | 0.974 | 0.185 | -0.002 |
| gat | post_covid | 901 | 0.789 | 0.949 | 0.164 | 0.047 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 114 | 0.258 | 62 | 52 | 87 | 0.544 | 0.584 | 0.308 | 0.471 | 0.279 | -0.152 |
| gnn_st | post_covid | 114 | 0.258 | 18 | 96 | 23 | 0.158 | 0.561 | 0.131 | 0.232 | 0.088 | 0.137 |
| xgboost | post_covid | 114 | 0.258 | 10 | 104 | 8 | 0.088 | 0.444 | 0.082 | 0.152 | 0.063 | 0.193 |
| gat | post_covid | 114 | 0.258 | 37 | 77 | 93 | 0.325 | 0.715 | 0.179 | 0.303 | 0.041 | -0.661 |
| persistence | post_covid | 114 | 0.258 | 32 | 82 | 79 | 0.281 | 0.712 | 0.166 | 0.284 | 0.040 | -0.219 |
| arima | post_covid | 114 | 0.258 | 9 | 105 | 14 | 0.079 | 0.609 | 0.070 | 0.131 | 0.036 | -0.054 |
| dualtopo | post_covid | 114 | 0.258 | 6 | 108 | 7 | 0.053 | 0.538 | 0.050 | 0.094 | 0.031 | 0.009 |
| lstm | post_covid | 114 | 0.258 | 6 | 108 | 8 | 0.053 | 0.571 | 0.049 | 0.094 | 0.028 | -0.063 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 17 | 0.038 | 3 | 14 | 48 | 0.176 | 0.941 | 0.046 | 0.088 | 0.064 | -1.330 |
| persistence | post_covid | 17 | 0.038 | 1 | 16 | 16 | 0.059 | 0.941 | 0.030 | 0.059 | 0.021 | -0.692 |
| arima | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.039 |
| dualtopo | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.027 |
| lstm | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| xgboost | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.068 |
| gnn_st | post_covid | 17 | 0.038 | 0 | 17 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.033 |
| seasonal_naive | post_covid | 17 | 0.038 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | -0.061 | -1.612 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| dualtopo | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.009 |
| gat | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.521 |
| gnn_st | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.003 |
| lstm | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.030 |
| persistence | post_covid | 4 | 0.009 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -1.119 |
| seasonal_naive | post_covid | 4 | 0.009 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.027 | -2.978 |
| xgboost | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.024 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 442 | 0.742 | 0.964 | 0.078 | -0.265 |
| dualtopo | post_covid | 442 | 0.740 | 0.962 | 0.021 | -0.276 |
| lstm | post_covid | 442 | 0.735 | 0.964 | 0.029 | -0.274 |
| arima | post_covid | 442 | 0.729 | 0.964 | 0.031 | -0.253 |
| gnn_st | post_covid | 442 | 0.722 | 0.968 | 0.090 | -0.210 |
| seasonal_naive | post_covid | 442 | 0.636 | 0.885 | 0.133 | 0.176 |
| persistence | post_covid | 442 | 0.606 | 0.948 | 0.082 | -0.007 |
| gat | post_covid | 442 | 0.579 | 0.896 | 0.038 | 0.104 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 17 | 1.000 | -1.000 | 2.647 | 5.000 | 3.079 |
| dualtopo | post_covid | 6 | 3.500 | -3.500 | 3.333 | 0.000 | -6.694 |
| persistence | post_covid | 17 | 4.000 | -4.000 | 4.000 | 3.500 | 0.000 |
| gnn_st | post_covid | 15 | 4.000 | -4.000 | 5.333 | 2.000 | -6.075 |
| gat | post_covid | 17 | 5.000 | -5.000 | 6.235 | 5.000 | 0.728 |
| xgboost | post_covid | 5 | 3.000 | -3.000 | 6.400 | 0.000 | -9.644 |
| arima | post_covid | 11 | 5.000 | -5.000 | 6.818 | 4.000 | -3.799 |
| lstm | post_covid | 6 | 5.500 | -5.500 | 7.833 | 3.000 | -5.133 |

# Notes

- 23 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 4 neighborhood-weeks in this window, so its scores are reported but not ranked.
