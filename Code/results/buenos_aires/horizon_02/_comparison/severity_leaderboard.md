Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 8 | 0.151 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.669 |
| xgboost | post_covid | 8 | 0.151 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.637 |
| xgboost_nodemo | post_covid | 8 | 0.151 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.623 |
| gnn_st | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.658 |
| persistence | post_covid | 8 | 0.151 | 5 | 3 | 3 | 0.625 | 0.375 | 0.455 | 0.625 | 0.558 | 0.491 |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.456 |
| arima | post_covid | 8 | 0.151 | 3 | 5 | 0 | 0.375 | 0.000 | 0.375 | 0.545 | 0.375 | 0.487 |
| dualtopo | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.380 |
| lstm | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.124 |
| gat | post_covid | 8 | 0.151 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | 0.455 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.046 |
| dualtopo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.146 |
| gat | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.180 |
| gnn_st | post_covid | 3 | 0.057 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.293 | 0.197 |
| gnn_st_nodemo | post_covid | 3 | 0.057 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.293 | 0.245 |
| lstm | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| persistence | post_covid | 3 | 0.057 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.293 | -0.060 |
| seasonal_naive | post_covid | 3 | 0.057 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.391 |
| xgboost | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.438 |
| xgboost_nodemo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.426 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.100 |
| dualtopo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.028 |
| gat | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.022 |
| gnn_st | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.312 |
| gnn_st_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.358 |
| lstm | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.026 |
| persistence | post_covid | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.019 | 0.098 |
| seasonal_naive | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.177 |
| xgboost | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.233 |
| xgboost_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.205 |

### All four bands — 53 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 53 | 0.906 | 0.981 | 0.727 | -0.113 |
| arima | post_covid | 53 | 0.887 | 0.943 | 0.366 | -0.170 |
| xgboost | post_covid | 53 | 0.887 | 0.981 | 0.636 | -0.132 |
| xgboost_nodemo | post_covid | 53 | 0.887 | 0.981 | 0.636 | -0.132 |
| dualtopo | post_covid | 53 | 0.849 | 0.943 | 0.000 | -0.226 |
| gnn_st_nodemo | post_covid | 53 | 0.849 | 1.000 | 0.753 | -0.075 |
| lstm | post_covid | 53 | 0.849 | 0.943 | 0.000 | -0.226 |
| gat | post_covid | 53 | 0.830 | 0.943 | -0.020 | -0.208 |
| gnn_st | post_covid | 53 | 0.830 | 1.000 | 0.727 | -0.057 |
| persistence | post_covid | 53 | 0.811 | 0.962 | 0.585 | 0.000 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 8 | 0.308 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.594 |
| xgboost | post_covid | 8 | 0.308 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.557 |
| xgboost_nodemo | post_covid | 8 | 0.308 | 5 | 3 | 0 | 0.625 | 0.000 | 0.625 | 0.769 | 0.625 | 0.543 |
| gnn_st | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.580 |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.401 |
| persistence | post_covid | 8 | 0.308 | 5 | 3 | 3 | 0.625 | 0.375 | 0.455 | 0.625 | 0.458 | 0.379 |
| arima | post_covid | 8 | 0.308 | 3 | 5 | 0 | 0.375 | 0.000 | 0.375 | 0.545 | 0.375 | 0.372 |
| dualtopo | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.240 |
| lstm | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.003 |
| gat | post_covid | 8 | 0.308 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | 0.334 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.017 |
| dualtopo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.089 |
| gat | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.125 |
| gnn_st | post_covid | 3 | 0.115 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.246 | 0.144 |
| gnn_st_nodemo | post_covid | 3 | 0.115 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.246 | 0.195 |
| lstm | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.069 |
| persistence | post_covid | 3 | 0.115 | 1 | 2 | 2 | 0.333 | 0.667 | 0.200 | 0.333 | 0.246 | -0.130 |
| seasonal_naive | post_covid | 3 | 0.115 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.374 |
| xgboost | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.401 |
| xgboost_nodemo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.389 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.081 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.008 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.002 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.298 |
| gnn_st_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.345 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.031 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | 0.080 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.190 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.218 |
| xgboost_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.189 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 26 | 0.808 | 0.962 | 0.698 | -0.231 |
| arima | post_covid | 26 | 0.769 | 0.885 | 0.325 | -0.346 |
| xgboost | post_covid | 26 | 0.769 | 0.962 | 0.598 | -0.269 |
| xgboost_nodemo | post_covid | 26 | 0.769 | 0.962 | 0.598 | -0.269 |
| dualtopo | post_covid | 26 | 0.692 | 0.885 | 0.000 | -0.462 |
| gnn_st_nodemo | post_covid | 26 | 0.692 | 1.000 | 0.720 | -0.154 |
| lstm | post_covid | 26 | 0.692 | 0.885 | 0.000 | -0.462 |
| gat | post_covid | 26 | 0.654 | 0.885 | -0.042 | -0.423 |
| gnn_st | post_covid | 26 | 0.654 | 1.000 | 0.686 | -0.115 |
| persistence | post_covid | 26 | 0.615 | 0.923 | 0.514 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 143 | 0.144 | 105 | 38 | 34 | 0.734 | 0.245 | 0.593 | 0.745 | 0.694 | 0.555 |
| gnn_st_nodemo | post_covid | 143 | 0.144 | 95 | 48 | 17 | 0.664 | 0.152 | 0.594 | 0.745 | 0.644 | 0.566 |
| gnn_st | post_covid | 143 | 0.144 | 92 | 51 | 19 | 0.643 | 0.171 | 0.568 | 0.724 | 0.621 | 0.565 |
| xgboost_nodemo | post_covid | 143 | 0.144 | 86 | 57 | 52 | 0.601 | 0.377 | 0.441 | 0.612 | 0.540 | 0.135 |
| arima | post_covid | 143 | 0.144 | 64 | 79 | 21 | 0.448 | 0.247 | 0.390 | 0.561 | 0.423 | 0.375 |
| xgboost | post_covid | 143 | 0.144 | 63 | 80 | 35 | 0.441 | 0.357 | 0.354 | 0.523 | 0.399 | 0.203 |
| seasonal_naive | post_covid | 143 | 0.144 | 65 | 78 | 50 | 0.455 | 0.435 | 0.337 | 0.504 | 0.396 | 0.004 |
| gat | post_covid | 143 | 0.144 | 50 | 93 | 26 | 0.350 | 0.342 | 0.296 | 0.457 | 0.319 | 0.243 |
| dualtopo | post_covid | 143 | 0.144 | 40 | 103 | 43 | 0.280 | 0.518 | 0.215 | 0.354 | 0.229 | 0.084 |
| lstm | post_covid | 143 | 0.144 | 24 | 119 | 16 | 0.168 | 0.400 | 0.151 | 0.262 | 0.149 | -0.094 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 37 | 0.037 | 25 | 12 | 12 | 0.676 | 0.324 | 0.510 | 0.676 | 0.663 | 0.451 |
| gnn_st | post_covid | 37 | 0.037 | 16 | 21 | 2 | 0.432 | 0.111 | 0.410 | 0.582 | 0.430 | 0.454 |
| gnn_st_nodemo | post_covid | 37 | 0.037 | 16 | 21 | 2 | 0.432 | 0.111 | 0.410 | 0.582 | 0.430 | 0.448 |
| arima | post_covid | 37 | 0.037 | 4 | 33 | 5 | 0.108 | 0.556 | 0.095 | 0.174 | 0.103 | 0.223 |
| gat | post_covid | 37 | 0.037 | 2 | 35 | 0 | 0.054 | 0.000 | 0.054 | 0.103 | 0.054 | -0.004 |
| seasonal_naive | post_covid | 37 | 0.037 | 1 | 36 | 22 | 0.027 | 0.957 | 0.017 | 0.033 | 0.004 | -0.594 |
| dualtopo | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.089 |
| lstm | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.284 |
| xgboost | post_covid | 37 | 0.037 | 0 | 37 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.014 |
| xgboost_nodemo | post_covid | 37 | 0.037 | 0 | 37 | 9 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -0.058 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.012 | 8 | 4 | 4 | 0.667 | 0.333 | 0.500 | 0.667 | 0.663 | 0.412 |
| gnn_st | post_covid | 12 | 0.012 | 5 | 7 | 1 | 0.417 | 0.167 | 0.385 | 0.556 | 0.416 | 0.428 |
| gnn_st_nodemo | post_covid | 12 | 0.012 | 5 | 7 | 1 | 0.417 | 0.167 | 0.385 | 0.556 | 0.416 | 0.424 |
| arima | post_covid | 12 | 0.012 | 1 | 11 | 2 | 0.083 | 0.667 | 0.071 | 0.133 | 0.081 | 0.013 |
| dualtopo | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.114 |
| gat | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.118 |
| lstm | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.390 |
| xgboost | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.036 |
| xgboost_nodemo | post_covid | 12 | 0.012 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | 0.016 |
| seasonal_naive | post_covid | 12 | 0.012 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.755 |

### All four bands — 992 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 992 | 0.914 | 0.989 | 0.742 | -0.056 |
| gnn_st | post_covid | 992 | 0.909 | 0.989 | 0.731 | -0.057 |
| persistence | post_covid | 992 | 0.901 | 0.994 | 0.790 | -0.004 |
| arima | post_covid | 992 | 0.875 | 0.979 | 0.462 | -0.096 |
| xgboost | post_covid | 992 | 0.872 | 0.969 | 0.298 | -0.091 |
| gat | post_covid | 992 | 0.867 | 0.975 | 0.311 | -0.115 |
| lstm | post_covid | 992 | 0.864 | 0.963 | 0.096 | -0.153 |
| xgboost_nodemo | post_covid | 992 | 0.859 | 0.976 | 0.456 | -0.044 |
| seasonal_naive | post_covid | 992 | 0.848 | 0.963 | 0.290 | -0.052 |
| dualtopo | post_covid | 992 | 0.840 | 0.972 | 0.224 | -0.110 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 130 | 0.263 | 97 | 33 | 31 | 0.746 | 0.242 | 0.602 | 0.752 | 0.661 | 0.509 |
| gnn_st_nodemo | post_covid | 130 | 0.263 | 90 | 40 | 17 | 0.692 | 0.159 | 0.612 | 0.759 | 0.646 | 0.532 |
| gnn_st | post_covid | 130 | 0.263 | 87 | 43 | 19 | 0.669 | 0.179 | 0.584 | 0.737 | 0.617 | 0.530 |
| xgboost_nodemo | post_covid | 130 | 0.263 | 81 | 49 | 46 | 0.623 | 0.362 | 0.460 | 0.630 | 0.497 | 0.132 |
| arima | post_covid | 130 | 0.263 | 63 | 67 | 19 | 0.485 | 0.232 | 0.423 | 0.594 | 0.432 | 0.296 |
| xgboost | post_covid | 130 | 0.263 | 60 | 70 | 34 | 0.462 | 0.362 | 0.366 | 0.536 | 0.368 | 0.154 |
| seasonal_naive | post_covid | 130 | 0.263 | 63 | 67 | 48 | 0.485 | 0.432 | 0.354 | 0.523 | 0.353 | 0.031 |
| gat | post_covid | 130 | 0.263 | 50 | 80 | 26 | 0.385 | 0.342 | 0.321 | 0.485 | 0.313 | 0.158 |
| dualtopo | post_covid | 130 | 0.263 | 40 | 90 | 34 | 0.308 | 0.459 | 0.244 | 0.392 | 0.214 | 0.004 |
| lstm | post_covid | 130 | 0.263 | 24 | 106 | 15 | 0.185 | 0.385 | 0.166 | 0.284 | 0.143 | -0.054 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 35 | 0.071 | 23 | 12 | 10 | 0.657 | 0.303 | 0.511 | 0.676 | 0.635 | 0.436 |
| gnn_st | post_covid | 35 | 0.071 | 15 | 20 | 2 | 0.429 | 0.118 | 0.405 | 0.577 | 0.424 | 0.434 |
| gnn_st_nodemo | post_covid | 35 | 0.071 | 15 | 20 | 2 | 0.429 | 0.118 | 0.405 | 0.577 | 0.424 | 0.426 |
| arima | post_covid | 35 | 0.071 | 4 | 31 | 5 | 0.114 | 0.556 | 0.100 | 0.182 | 0.103 | 0.199 |
| gat | post_covid | 35 | 0.071 | 2 | 33 | 0 | 0.057 | 0.000 | 0.057 | 0.108 | 0.057 | -0.048 |
| dualtopo | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.052 |
| lstm | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.199 |
| xgboost | post_covid | 35 | 0.071 | 0 | 35 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.007 | -0.051 |
| xgboost_nodemo | post_covid | 35 | 0.071 | 0 | 35 | 7 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.071 |
| seasonal_naive | post_covid | 35 | 0.071 | 1 | 34 | 22 | 0.029 | 0.957 | 0.018 | 0.034 | -0.019 | -0.551 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.024 | 8 | 4 | 3 | 0.667 | 0.273 | 0.533 | 0.696 | 0.660 | 0.486 |
| gnn_st | post_covid | 12 | 0.024 | 5 | 7 | 1 | 0.417 | 0.167 | 0.385 | 0.556 | 0.415 | 0.446 |
| gnn_st_nodemo | post_covid | 12 | 0.024 | 5 | 7 | 1 | 0.417 | 0.167 | 0.385 | 0.556 | 0.415 | 0.441 |
| arima | post_covid | 12 | 0.024 | 1 | 11 | 2 | 0.083 | 0.667 | 0.071 | 0.133 | 0.079 | 0.001 |
| dualtopo | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.103 |
| gat | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.112 |
| lstm | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| xgboost | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.062 |
| xgboost_nodemo | post_covid | 12 | 0.024 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.100 |
| seasonal_naive | post_covid | 12 | 0.024 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.580 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 494 | 0.846 | 0.978 | 0.720 | -0.095 |
| gnn_st | post_covid | 494 | 0.836 | 0.978 | 0.707 | -0.097 |
| persistence | post_covid | 494 | 0.824 | 0.988 | 0.769 | -0.010 |
| arima | post_covid | 494 | 0.777 | 0.962 | 0.440 | -0.168 |
| xgboost | post_covid | 494 | 0.767 | 0.941 | 0.233 | -0.162 |
| gat | post_covid | 494 | 0.759 | 0.953 | 0.274 | -0.200 |
| lstm | post_covid | 494 | 0.755 | 0.929 | 0.066 | -0.279 |
| xgboost_nodemo | post_covid | 494 | 0.753 | 0.951 | 0.391 | -0.085 |
| dualtopo | post_covid | 494 | 0.723 | 0.947 | 0.193 | -0.209 |
| seasonal_naive | post_covid | 494 | 0.721 | 0.929 | 0.218 | -0.083 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost | post_covid | 11 | -1.000 | 1.000 | 1.727 | 0.000 | -3.604 |
| xgboost_nodemo | post_covid | 11 | -1.000 | 1.000 | 1.727 | 1.000 | -1.759 |
| persistence | post_covid | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| gnn_st_nodemo | post_covid | 14 | 2.000 | -2.000 | 2.143 | 2.000 | -1.969 |
| gnn_st | post_covid | 14 | 2.000 | -2.000 | 2.429 | 2.000 | -2.567 |
| arima | post_covid | 12 | 2.000 | -2.000 | 3.500 | 2.000 | -0.038 |
| seasonal_naive | post_covid | 13 | -1.000 | 1.000 | 3.923 | -0.500 | 4.544 |
| lstm | post_covid | 6 | 3.000 | -3.000 | 4.333 | -1.000 | -4.854 |
| gat | post_covid | 9 | 3.000 | -3.000 | 4.889 | 1.000 | -7.704 |
| dualtopo | post_covid | 13 | 0.000 | 0.000 | 5.769 | 0.000 | -8.059 |

# Notes

- 60 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
