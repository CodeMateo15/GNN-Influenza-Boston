Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 8 | 0.151 | 8 | 0 | 5 | 1.000 | 0.385 | 0.615 | 0.762 | 0.889 | 0.462 |
| gnn_st_nodemo | post_covid | 8 | 0.151 | 6 | 2 | 1 | 0.750 | 0.143 | 0.667 | 0.800 | 0.728 | 0.572 |
| xgboost | post_covid | 8 | 0.151 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.583 |
| xgboost_nodemo | post_covid | 8 | 0.151 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.558 |
| gnn_st | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.561 |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.456 |
| persistence | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.161 |
| arima | post_covid | 8 | 0.151 | 2 | 6 | 1 | 0.250 | 0.333 | 0.222 | 0.364 | 0.228 | 0.264 |
| dualtopo | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.299 |
| lstm | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.039 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.245 |
| dualtopo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.185 |
| gat | post_covid | 3 | 0.057 | 3 | 0 | 2 | 1.000 | 0.400 | 0.600 | 0.750 | 0.960 | 0.089 |
| gnn_st | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.230 |
| gnn_st_nodemo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.261 |
| lstm | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| persistence | post_covid | 3 | 0.057 | 0 | 3 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.060 | -0.619 |
| seasonal_naive | post_covid | 3 | 0.057 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.391 |
| xgboost | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.522 |
| xgboost_nodemo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.502 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.166 |
| dualtopo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.089 |
| gat | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.377 |
| gnn_st | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.071 |
| gnn_st_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.091 |
| lstm | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.062 |
| persistence | post_covid | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.019 | -0.807 |
| seasonal_naive | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.177 |
| xgboost | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.153 |
| xgboost_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.142 |

### All four bands — 53 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 53 | 0.906 | 0.981 | 0.727 | -0.113 |
| gnn_st | post_covid | 53 | 0.887 | 0.962 | 0.525 | -0.113 |
| gnn_st_nodemo | post_covid | 53 | 0.887 | 0.981 | 0.652 | -0.094 |
| xgboost | post_covid | 53 | 0.887 | 0.981 | 0.636 | -0.132 |
| xgboost_nodemo | post_covid | 53 | 0.887 | 0.981 | 0.636 | -0.132 |
| arima | post_covid | 53 | 0.868 | 0.943 | 0.112 | -0.170 |
| gat | post_covid | 53 | 0.868 | 0.981 | 0.761 | 0.113 |
| dualtopo | post_covid | 53 | 0.849 | 0.943 | 0.000 | -0.226 |
| lstm | post_covid | 53 | 0.849 | 0.943 | 0.000 | -0.226 |
| persistence | post_covid | 53 | 0.811 | 0.906 | 0.222 | 0.000 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 8 | 0.308 | 8 | 0 | 5 | 1.000 | 0.385 | 0.615 | 0.762 | 0.722 | 0.340 |
| gnn_st_nodemo | post_covid | 8 | 0.308 | 6 | 2 | 1 | 0.750 | 0.143 | 0.667 | 0.800 | 0.694 | 0.479 |
| xgboost | post_covid | 8 | 0.308 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.493 |
| xgboost_nodemo | post_covid | 8 | 0.308 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.467 |
| gnn_st | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.466 |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.401 |
| persistence | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.011 |
| arima | post_covid | 8 | 0.308 | 2 | 6 | 1 | 0.250 | 0.333 | 0.222 | 0.364 | 0.194 | 0.112 |
| dualtopo | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.141 |
| lstm | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.205 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.327 |
| dualtopo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.131 |
| gat | post_covid | 3 | 0.115 | 3 | 0 | 2 | 1.000 | 0.400 | 0.600 | 0.750 | 0.913 | 0.029 |
| gnn_st | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.179 |
| gnn_st_nodemo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.212 |
| lstm | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.126 |
| persistence | post_covid | 3 | 0.115 | 0 | 3 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.130 | -0.722 |
| seasonal_naive | post_covid | 3 | 0.115 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.374 |
| xgboost | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.491 |
| xgboost_nodemo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.470 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.189 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.070 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.405 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.052 |
| gnn_st_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.072 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.073 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.843 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.190 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.136 |
| xgboost_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.124 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 26 | 0.808 | 0.962 | 0.698 | -0.231 |
| gnn_st | post_covid | 26 | 0.769 | 0.923 | 0.466 | -0.231 |
| gnn_st_nodemo | post_covid | 26 | 0.769 | 0.962 | 0.601 | -0.192 |
| xgboost | post_covid | 26 | 0.769 | 0.962 | 0.598 | -0.269 |
| xgboost_nodemo | post_covid | 26 | 0.769 | 0.962 | 0.598 | -0.269 |
| arima | post_covid | 26 | 0.731 | 0.885 | 0.055 | -0.346 |
| gat | post_covid | 26 | 0.731 | 0.962 | 0.700 | 0.231 |
| dualtopo | post_covid | 26 | 0.692 | 0.885 | 0.000 | -0.462 |
| lstm | post_covid | 26 | 0.692 | 0.885 | 0.000 | -0.462 |
| persistence | post_covid | 26 | 0.615 | 0.808 | 0.089 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 143 | 0.144 | 86 | 57 | 52 | 0.601 | 0.377 | 0.441 | 0.612 | 0.540 | 0.363 |
| gat | post_covid | 143 | 0.144 | 92 | 51 | 93 | 0.643 | 0.503 | 0.390 | 0.561 | 0.534 | 0.175 |
| arima | post_covid | 143 | 0.144 | 74 | 69 | 27 | 0.517 | 0.267 | 0.435 | 0.607 | 0.486 | 0.351 |
| seasonal_naive | post_covid | 143 | 0.144 | 65 | 78 | 50 | 0.455 | 0.435 | 0.337 | 0.504 | 0.396 | 0.004 |
| gnn_st_nodemo | post_covid | 143 | 0.144 | 58 | 85 | 16 | 0.406 | 0.216 | 0.365 | 0.535 | 0.387 | 0.354 |
| xgboost_nodemo | post_covid | 143 | 0.144 | 57 | 86 | 44 | 0.399 | 0.436 | 0.305 | 0.467 | 0.347 | 0.097 |
| gnn_st | post_covid | 143 | 0.144 | 48 | 95 | 14 | 0.336 | 0.226 | 0.306 | 0.468 | 0.319 | 0.345 |
| xgboost | post_covid | 143 | 0.144 | 44 | 99 | 37 | 0.308 | 0.457 | 0.244 | 0.393 | 0.264 | 0.151 |
| dualtopo | post_covid | 143 | 0.144 | 10 | 133 | 25 | 0.070 | 0.714 | 0.060 | 0.112 | 0.040 | 0.043 |
| lstm | post_covid | 143 | 0.144 | 7 | 136 | 11 | 0.049 | 0.611 | 0.045 | 0.087 | 0.036 | -0.118 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 37 | 0.037 | 20 | 17 | 16 | 0.541 | 0.444 | 0.377 | 0.548 | 0.524 | 0.213 |
| arima | post_covid | 37 | 0.037 | 9 | 28 | 11 | 0.243 | 0.550 | 0.188 | 0.316 | 0.232 | 0.176 |
| gnn_st_nodemo | post_covid | 37 | 0.037 | 3 | 34 | 0 | 0.081 | 0.000 | 0.081 | 0.150 | 0.081 | 0.221 |
| gat | post_covid | 37 | 0.037 | 3 | 34 | 8 | 0.081 | 0.727 | 0.067 | 0.125 | 0.073 | 0.024 |
| gnn_st | post_covid | 37 | 0.037 | 2 | 35 | 0 | 0.054 | 0.000 | 0.054 | 0.103 | 0.054 | 0.217 |
| xgboost_nodemo | post_covid | 37 | 0.037 | 2 | 35 | 6 | 0.054 | 0.750 | 0.047 | 0.089 | 0.048 | -0.122 |
| xgboost | post_covid | 37 | 0.037 | 1 | 36 | 4 | 0.027 | 0.800 | 0.024 | 0.048 | 0.023 | -0.088 |
| seasonal_naive | post_covid | 37 | 0.037 | 1 | 36 | 22 | 0.027 | 0.957 | 0.017 | 0.033 | 0.004 | -0.594 |
| dualtopo | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.007 |
| lstm | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.189 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.012 | 5 | 7 | 7 | 0.417 | 0.583 | 0.263 | 0.417 | 0.410 | 0.088 |
| dualtopo | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.072 |
| gat | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.076 |
| gnn_st | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.203 |
| gnn_st_nodemo | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.208 |
| lstm | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.260 |
| xgboost_nodemo | post_covid | 12 | 0.012 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.169 |
| seasonal_naive | post_covid | 12 | 0.012 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.755 |
| arima | post_covid | 12 | 0.012 | 0 | 12 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.006 |
| xgboost | post_covid | 12 | 0.012 | 0 | 12 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.118 |

### All four bands — 992 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 992 | 0.878 | 0.979 | 0.431 | -0.116 |
| arima | post_covid | 992 | 0.876 | 0.973 | 0.538 | -0.069 |
| gnn_st | post_covid | 992 | 0.871 | 0.977 | 0.379 | -0.129 |
| persistence | post_covid | 992 | 0.865 | 0.980 | 0.628 | -0.006 |
| xgboost | post_covid | 992 | 0.857 | 0.964 | 0.193 | -0.104 |
| xgboost_nodemo | post_covid | 992 | 0.853 | 0.971 | 0.307 | -0.083 |
| lstm | post_covid | 992 | 0.852 | 0.963 | 0.022 | -0.175 |
| seasonal_naive | post_covid | 992 | 0.848 | 0.963 | 0.290 | -0.052 |
| dualtopo | post_covid | 992 | 0.839 | 0.965 | 0.031 | -0.158 |
| gat | post_covid | 992 | 0.828 | 0.975 | 0.439 | 0.004 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 130 | 0.263 | 70 | 60 | 24 | 0.538 | 0.255 | 0.455 | 0.625 | 0.473 | 0.294 |
| persistence | post_covid | 130 | 0.263 | 77 | 53 | 45 | 0.592 | 0.369 | 0.440 | 0.611 | 0.469 | 0.297 |
| gat | post_covid | 130 | 0.263 | 92 | 38 | 93 | 0.708 | 0.503 | 0.413 | 0.584 | 0.452 | 0.076 |
| gnn_st_nodemo | post_covid | 130 | 0.263 | 53 | 77 | 16 | 0.408 | 0.232 | 0.363 | 0.533 | 0.364 | 0.283 |
| seasonal_naive | post_covid | 130 | 0.263 | 63 | 67 | 48 | 0.485 | 0.432 | 0.354 | 0.523 | 0.353 | 0.031 |
| gnn_st | post_covid | 130 | 0.263 | 43 | 87 | 14 | 0.331 | 0.246 | 0.299 | 0.460 | 0.292 | 0.269 |
| xgboost_nodemo | post_covid | 130 | 0.263 | 52 | 78 | 42 | 0.400 | 0.447 | 0.302 | 0.464 | 0.285 | 0.062 |
| xgboost | post_covid | 130 | 0.263 | 41 | 89 | 37 | 0.315 | 0.474 | 0.246 | 0.394 | 0.214 | 0.084 |
| lstm | post_covid | 130 | 0.263 | 7 | 123 | 9 | 0.054 | 0.562 | 0.050 | 0.096 | 0.029 | -0.114 |
| dualtopo | post_covid | 130 | 0.263 | 10 | 120 | 18 | 0.077 | 0.643 | 0.068 | 0.127 | 0.027 | -0.045 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 35 | 0.071 | 18 | 17 | 13 | 0.514 | 0.419 | 0.375 | 0.545 | 0.486 | 0.189 |
| arima | post_covid | 35 | 0.071 | 9 | 26 | 11 | 0.257 | 0.550 | 0.196 | 0.327 | 0.233 | 0.148 |
| gnn_st_nodemo | post_covid | 35 | 0.071 | 3 | 32 | 0 | 0.086 | 0.000 | 0.086 | 0.158 | 0.086 | 0.183 |
| gat | post_covid | 35 | 0.071 | 3 | 32 | 8 | 0.086 | 0.727 | 0.070 | 0.130 | 0.068 | -0.013 |
| gnn_st | post_covid | 35 | 0.071 | 2 | 33 | 0 | 0.057 | 0.000 | 0.057 | 0.108 | 0.057 | 0.178 |
| xgboost_nodemo | post_covid | 35 | 0.071 | 2 | 33 | 4 | 0.057 | 0.667 | 0.051 | 0.098 | 0.048 | -0.134 |
| xgboost | post_covid | 35 | 0.071 | 1 | 34 | 4 | 0.029 | 0.800 | 0.026 | 0.050 | 0.020 | -0.116 |
| dualtopo | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.030 |
| lstm | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.140 |
| seasonal_naive | post_covid | 35 | 0.071 | 1 | 34 | 22 | 0.029 | 0.957 | 0.018 | 0.034 | -0.019 | -0.551 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.024 | 5 | 7 | 4 | 0.417 | 0.444 | 0.312 | 0.476 | 0.408 | 0.197 |
| dualtopo | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.065 |
| gat | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.065 |
| gnn_st | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.215 |
| gnn_st_nodemo | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.219 |
| lstm | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.093 |
| xgboost_nodemo | post_covid | 12 | 0.024 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.071 |
| seasonal_naive | post_covid | 12 | 0.024 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.580 |
| arima | post_covid | 12 | 0.024 | 0 | 12 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.018 |
| xgboost | post_covid | 12 | 0.024 | 0 | 12 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.083 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 494 | 0.775 | 0.949 | 0.511 | -0.121 |
| gnn_st_nodemo | post_covid | 494 | 0.775 | 0.957 | 0.381 | -0.213 |
| gnn_st | post_covid | 494 | 0.761 | 0.953 | 0.329 | -0.239 |
| persistence | post_covid | 494 | 0.761 | 0.962 | 0.579 | -0.030 |
| lstm | post_covid | 494 | 0.733 | 0.929 | 0.008 | -0.326 |
| xgboost | post_covid | 494 | 0.733 | 0.931 | 0.124 | -0.184 |
| xgboost_nodemo | post_covid | 494 | 0.733 | 0.941 | 0.223 | -0.154 |
| seasonal_naive | post_covid | 494 | 0.721 | 0.929 | 0.218 | -0.083 |
| dualtopo | post_covid | 494 | 0.717 | 0.933 | 0.013 | -0.302 |
| gat | post_covid | 494 | 0.680 | 0.953 | 0.364 | 0.038 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 12 | -1.500 | 1.500 | 2.167 | 0.000 | 3.148 |
| xgboost | post_covid | 12 | -1.000 | 1.000 | 2.750 | -0.500 | -1.673 |
| dualtopo | post_covid | 5 | -1.000 | 1.000 | 2.800 | -1.000 | -13.874 |
| gat | post_covid | 14 | -1.000 | 1.000 | 3.214 | 0.000 | -4.579 |
| gnn_st_nodemo | post_covid | 13 | 4.000 | -4.000 | 3.692 | 0.000 | -6.915 |
| seasonal_naive | post_covid | 13 | -1.000 | 1.000 | 3.923 | -0.500 | 4.544 |
| persistence | post_covid | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| gnn_st | post_covid | 11 | 4.000 | -4.000 | 4.182 | 0.000 | -8.183 |
| arima | post_covid | 8 | 4.000 | -4.000 | 4.500 | 4.000 | -0.647 |
| lstm | post_covid | 5 | -4.000 | 4.000 | 6.600 | -2.000 | -2.551 |

# Notes

- 57 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
