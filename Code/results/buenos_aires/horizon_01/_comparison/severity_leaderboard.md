Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 8 | 0.151 | 6 | 2 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.602 |
| xgboost | post_covid | 8 | 0.151 | 6 | 2 | 1 | 0.750 | 0.143 | 0.667 | 0.800 | 0.728 | -0.951 |
| dualtopo | post_covid | 8 | 0.151 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.706 | 0.505 |
| persistence | post_covid | 8 | 0.151 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.706 | 0.594 |
| gnn_st | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.667 |
| gnn_st_nodemo | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.657 |
| arima | post_covid | 8 | 0.151 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.617 |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.456 |
| gat | post_covid | 8 | 0.151 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.267 |
| lstm | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.230 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.057 | 1 | 2 | 0 | 0.333 | 0.000 | 0.333 | 0.500 | 0.333 | 0.373 |
| dualtopo | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.145 |
| gat | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.111 |
| gnn_st | post_covid | 3 | 0.057 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.647 | 0.498 |
| gnn_st_nodemo | post_covid | 3 | 0.057 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.647 | 0.500 |
| lstm | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.079 |
| persistence | post_covid | 3 | 0.057 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.647 | 0.370 |
| seasonal_naive | post_covid | 3 | 0.057 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.391 |
| xgboost | post_covid | 3 | 0.057 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -3.682 |
| xgboost_nodemo | post_covid | 3 | 0.057 | 1 | 2 | 0 | 0.333 | 0.000 | 0.333 | 0.500 | 0.333 | 0.508 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.291 |
| dualtopo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.053 |
| gat | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.112 |
| gnn_st | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.212 |
| gnn_st_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.223 |
| lstm | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.054 |
| persistence | post_covid | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.019 | 0.059 |
| seasonal_naive | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.177 |
| xgboost | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -12.505 |
| xgboost_nodemo | post_covid | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.278 |

### All four bands — 53 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 53 | 0.906 | 0.981 | 0.727 | -0.113 |
| xgboost_nodemo | post_covid | 53 | 0.906 | 1.000 | 0.820 | -0.094 |
| arima | post_covid | 53 | 0.887 | 0.981 | 0.663 | -0.132 |
| dualtopo | post_covid | 53 | 0.887 | 0.962 | 0.545 | -0.075 |
| xgboost | post_covid | 53 | 0.887 | 0.981 | 0.652 | -0.094 |
| gnn_st | post_covid | 53 | 0.868 | 1.000 | 0.787 | -0.057 |
| gnn_st_nodemo | post_covid | 53 | 0.868 | 1.000 | 0.787 | -0.057 |
| persistence | post_covid | 53 | 0.868 | 0.981 | 0.741 | 0.000 |
| gat | post_covid | 53 | 0.849 | 0.943 | 0.246 | -0.208 |
| lstm | post_covid | 53 | 0.849 | 0.943 | 0.000 | -0.226 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_nodemo | post_covid | 8 | 0.308 | 6 | 2 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.517 |
| xgboost | post_covid | 8 | 0.308 | 6 | 2 | 1 | 0.750 | 0.143 | 0.667 | 0.800 | 0.694 | -0.174 |
| dualtopo | post_covid | 8 | 0.308 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.639 | 0.393 |
| persistence | post_covid | 8 | 0.308 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.639 | 0.504 |
| gnn_st | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.593 |
| gnn_st_nodemo | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.580 |
| arima | post_covid | 8 | 0.308 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.530 |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.401 |
| gat | post_covid | 8 | 0.308 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.103 |
| lstm | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.102 |

### Crossing IT90 — **underpowered: 3 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 3 | 0.115 | 1 | 2 | 0 | 0.333 | 0.000 | 0.333 | 0.500 | 0.333 | 0.331 |
| dualtopo | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.088 |
| gat | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.052 |
| gnn_st | post_covid | 3 | 0.115 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.623 | 0.464 |
| gnn_st_nodemo | post_covid | 3 | 0.115 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.623 | 0.467 |
| lstm | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.029 |
| persistence | post_covid | 3 | 0.115 | 2 | 1 | 1 | 0.667 | 0.333 | 0.500 | 0.667 | 0.623 | 0.328 |
| seasonal_naive | post_covid | 3 | 0.115 | 2 | 1 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.374 |
| xgboost | post_covid | 3 | 0.115 | 0 | 3 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.449 |
| xgboost_nodemo | post_covid | 3 | 0.115 | 1 | 2 | 0 | 0.333 | 0.000 | 0.333 | 0.500 | 0.333 | 0.476 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.277 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.034 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.094 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.196 |
| gnn_st_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.207 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.039 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | 0.040 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.190 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -5.760 |
| xgboost_nodemo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.263 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | post_covid | 26 | 0.808 | 0.962 | 0.698 | -0.231 |
| xgboost_nodemo | post_covid | 26 | 0.808 | 1.000 | 0.796 | -0.192 |
| arima | post_covid | 26 | 0.769 | 0.962 | 0.631 | -0.269 |
| dualtopo | post_covid | 26 | 0.769 | 0.923 | 0.469 | -0.154 |
| xgboost | post_covid | 26 | 0.769 | 0.962 | 0.601 | -0.192 |
| gnn_st | post_covid | 26 | 0.731 | 1.000 | 0.756 | -0.115 |
| gnn_st_nodemo | post_covid | 26 | 0.731 | 1.000 | 0.756 | -0.115 |
| persistence | post_covid | 26 | 0.731 | 0.962 | 0.696 | 0.000 |
| gat | post_covid | 26 | 0.692 | 0.885 | 0.230 | -0.423 |
| lstm | post_covid | 26 | 0.692 | 0.885 | 0.000 | -0.462 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 143 | 0.144 | 115 | 28 | 26 | 0.804 | 0.184 | 0.680 | 0.810 | 0.774 | 0.661 |
| gnn_st | post_covid | 143 | 0.144 | 108 | 35 | 17 | 0.755 | 0.136 | 0.675 | 0.806 | 0.735 | 0.663 |
| gnn_st_nodemo | post_covid | 143 | 0.144 | 108 | 35 | 17 | 0.755 | 0.136 | 0.675 | 0.806 | 0.735 | 0.660 |
| arima | post_covid | 143 | 0.144 | 89 | 54 | 20 | 0.622 | 0.183 | 0.546 | 0.706 | 0.599 | 0.535 |
| xgboost_nodemo | post_covid | 143 | 0.144 | 91 | 52 | 60 | 0.636 | 0.397 | 0.448 | 0.619 | 0.566 | 0.234 |
| xgboost | post_covid | 143 | 0.144 | 82 | 61 | 41 | 0.573 | 0.333 | 0.446 | 0.617 | 0.525 | -0.926 |
| dualtopo | post_covid | 143 | 0.144 | 64 | 79 | 29 | 0.448 | 0.312 | 0.372 | 0.542 | 0.413 | 0.350 |
| seasonal_naive | post_covid | 143 | 0.144 | 65 | 78 | 50 | 0.455 | 0.435 | 0.337 | 0.504 | 0.396 | 0.004 |
| gat | post_covid | 143 | 0.144 | 47 | 96 | 14 | 0.329 | 0.230 | 0.299 | 0.461 | 0.312 | 0.314 |
| lstm | post_covid | 143 | 0.144 | 39 | 104 | 22 | 0.273 | 0.361 | 0.236 | 0.382 | 0.247 | 0.008 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 37 | 0.037 | 28 | 9 | 9 | 0.757 | 0.243 | 0.609 | 0.757 | 0.747 | 0.564 |
| gnn_st | post_covid | 37 | 0.037 | 21 | 16 | 1 | 0.568 | 0.045 | 0.553 | 0.712 | 0.567 | 0.583 |
| gnn_st_nodemo | post_covid | 37 | 0.037 | 21 | 16 | 1 | 0.568 | 0.045 | 0.553 | 0.712 | 0.567 | 0.582 |
| arima | post_covid | 37 | 0.037 | 14 | 23 | 4 | 0.378 | 0.222 | 0.341 | 0.509 | 0.374 | 0.470 |
| xgboost_nodemo | post_covid | 37 | 0.037 | 13 | 24 | 21 | 0.351 | 0.618 | 0.224 | 0.366 | 0.329 | -0.015 |
| xgboost | post_covid | 37 | 0.037 | 3 | 34 | 5 | 0.081 | 0.625 | 0.071 | 0.133 | 0.076 | -5.618 |
| gat | post_covid | 37 | 0.037 | 2 | 35 | 2 | 0.054 | 0.500 | 0.051 | 0.098 | 0.052 | 0.082 |
| seasonal_naive | post_covid | 37 | 0.037 | 1 | 36 | 22 | 0.027 | 0.957 | 0.017 | 0.033 | 0.004 | -0.594 |
| dualtopo | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.103 |
| lstm | post_covid | 37 | 0.037 | 0 | 37 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.174 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.012 | 10 | 2 | 2 | 0.833 | 0.167 | 0.714 | 0.833 | 0.831 | 0.640 |
| gnn_st | post_covid | 12 | 0.012 | 8 | 4 | 1 | 0.667 | 0.111 | 0.615 | 0.762 | 0.666 | 0.586 |
| gnn_st_nodemo | post_covid | 12 | 0.012 | 8 | 4 | 1 | 0.667 | 0.111 | 0.615 | 0.762 | 0.666 | 0.579 |
| arima | post_covid | 12 | 0.012 | 3 | 9 | 1 | 0.250 | 0.250 | 0.231 | 0.375 | 0.249 | 0.355 |
| xgboost_nodemo | post_covid | 12 | 0.012 | 3 | 9 | 3 | 0.250 | 0.500 | 0.200 | 0.333 | 0.247 | 0.078 |
| dualtopo | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.089 |
| gat | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.177 |
| lstm | post_covid | 12 | 0.012 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.220 |
| xgboost | post_covid | 12 | 0.012 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -18.886 |
| seasonal_naive | post_covid | 12 | 0.012 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.755 |

### All four bands — 992 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 992 | 0.928 | 0.997 | 0.837 | -0.036 |
| gnn_st_nodemo | post_covid | 992 | 0.928 | 0.997 | 0.837 | -0.036 |
| persistence | post_covid | 992 | 0.926 | 0.997 | 0.852 | -0.002 |
| arima | post_covid | 992 | 0.902 | 0.986 | 0.689 | -0.061 |
| dualtopo | post_covid | 992 | 0.870 | 0.976 | 0.404 | -0.100 |
| gat | post_covid | 992 | 0.870 | 0.976 | 0.362 | -0.128 |
| xgboost | post_covid | 992 | 0.868 | 0.980 | 0.503 | -0.060 |
| lstm | post_covid | 992 | 0.865 | 0.966 | 0.229 | -0.132 |
| xgboost_nodemo | post_covid | 992 | 0.852 | 0.981 | 0.581 | -0.001 |
| seasonal_naive | post_covid | 992 | 0.848 | 0.963 | 0.290 | -0.052 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 130 | 0.263 | 103 | 27 | 16 | 0.792 | 0.134 | 0.705 | 0.827 | 0.748 | 0.634 |
| persistence | post_covid | 130 | 0.263 | 105 | 25 | 23 | 0.808 | 0.180 | 0.686 | 0.814 | 0.745 | 0.631 |
| gnn_st | post_covid | 130 | 0.263 | 102 | 28 | 16 | 0.785 | 0.136 | 0.699 | 0.823 | 0.741 | 0.636 |
| arima | post_covid | 130 | 0.263 | 83 | 47 | 17 | 0.638 | 0.170 | 0.565 | 0.722 | 0.592 | 0.483 |
| xgboost_nodemo | post_covid | 130 | 0.263 | 85 | 45 | 50 | 0.654 | 0.370 | 0.472 | 0.642 | 0.516 | 0.234 |
| xgboost | post_covid | 130 | 0.263 | 77 | 53 | 36 | 0.592 | 0.319 | 0.464 | 0.634 | 0.493 | -0.208 |
| dualtopo | post_covid | 130 | 0.263 | 64 | 66 | 29 | 0.492 | 0.312 | 0.403 | 0.574 | 0.413 | 0.299 |
| seasonal_naive | post_covid | 130 | 0.263 | 63 | 67 | 48 | 0.485 | 0.432 | 0.354 | 0.523 | 0.353 | 0.031 |
| gat | post_covid | 130 | 0.263 | 47 | 83 | 14 | 0.362 | 0.230 | 0.326 | 0.492 | 0.323 | 0.238 |
| lstm | post_covid | 130 | 0.263 | 39 | 91 | 21 | 0.300 | 0.350 | 0.258 | 0.411 | 0.242 | 0.025 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 35 | 0.071 | 27 | 8 | 7 | 0.771 | 0.206 | 0.643 | 0.783 | 0.756 | 0.565 |
| gnn_st | post_covid | 35 | 0.071 | 20 | 15 | 1 | 0.571 | 0.048 | 0.556 | 0.714 | 0.569 | 0.581 |
| gnn_st_nodemo | post_covid | 35 | 0.071 | 20 | 15 | 1 | 0.571 | 0.048 | 0.556 | 0.714 | 0.569 | 0.579 |
| arima | post_covid | 35 | 0.071 | 14 | 21 | 4 | 0.400 | 0.222 | 0.359 | 0.528 | 0.391 | 0.464 |
| xgboost_nodemo | post_covid | 35 | 0.071 | 11 | 24 | 17 | 0.314 | 0.607 | 0.212 | 0.349 | 0.277 | -0.046 |
| xgboost | post_covid | 35 | 0.071 | 3 | 32 | 4 | 0.086 | 0.571 | 0.077 | 0.143 | 0.077 | -2.559 |
| gat | post_covid | 35 | 0.071 | 2 | 33 | 2 | 0.057 | 0.500 | 0.054 | 0.103 | 0.053 | 0.044 |
| dualtopo | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.076 |
| lstm | post_covid | 35 | 0.071 | 0 | 35 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.134 |
| seasonal_naive | post_covid | 35 | 0.071 | 1 | 34 | 22 | 0.029 | 0.957 | 0.018 | 0.034 | -0.019 | -0.551 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 12 | 0.024 | 10 | 2 | 2 | 0.833 | 0.167 | 0.714 | 0.833 | 0.829 | 0.688 |
| gnn_st | post_covid | 12 | 0.024 | 8 | 4 | 1 | 0.667 | 0.111 | 0.615 | 0.762 | 0.665 | 0.603 |
| gnn_st_nodemo | post_covid | 12 | 0.024 | 8 | 4 | 1 | 0.667 | 0.111 | 0.615 | 0.762 | 0.665 | 0.595 |
| arima | post_covid | 12 | 0.024 | 3 | 9 | 1 | 0.250 | 0.250 | 0.231 | 0.375 | 0.248 | 0.348 |
| xgboost_nodemo | post_covid | 12 | 0.024 | 3 | 9 | 2 | 0.250 | 0.400 | 0.214 | 0.353 | 0.246 | 0.177 |
| dualtopo | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.078 |
| gat | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.167 |
| lstm | post_covid | 12 | 0.024 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.059 |
| xgboost | post_covid | 12 | 0.024 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -8.886 |
| seasonal_naive | post_covid | 12 | 0.024 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.580 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | post_covid | 494 | 0.877 | 0.994 | 0.831 | -0.057 |
| gnn_st | post_covid | 494 | 0.874 | 0.994 | 0.829 | -0.059 |
| persistence | post_covid | 494 | 0.870 | 0.994 | 0.841 | -0.006 |
| arima | post_covid | 494 | 0.826 | 0.974 | 0.672 | -0.111 |
| xgboost | post_covid | 494 | 0.767 | 0.960 | 0.453 | -0.113 |
| dualtopo | post_covid | 494 | 0.765 | 0.955 | 0.371 | -0.170 |
| gat | post_covid | 494 | 0.765 | 0.955 | 0.340 | -0.227 |
| lstm | post_covid | 494 | 0.757 | 0.935 | 0.196 | -0.237 |
| xgboost_nodemo | post_covid | 494 | 0.743 | 0.966 | 0.539 | -0.018 |
| seasonal_naive | post_covid | 494 | 0.721 | 0.929 | 0.218 | -0.083 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| gnn_st_nodemo | post_covid | 14 | 1.000 | -1.000 | 1.071 | 1.000 | -3.317 |
| arima | post_covid | 12 | 1.000 | -1.000 | 1.333 | 1.000 | -0.289 |
| gnn_st | post_covid | 14 | 1.000 | -1.000 | 1.357 | 1.000 | -3.080 |
| xgboost | post_covid | 12 | 0.000 | 0.000 | 1.750 | 1.000 | 1.437 |
| xgboost_nodemo | post_covid | 12 | -2.000 | 2.000 | 2.167 | 0.500 | 1.039 |
| lstm | post_covid | 8 | 2.000 | -2.000 | 3.625 | 0.000 | -7.077 |
| dualtopo | post_covid | 13 | 2.000 | -2.000 | 3.923 | 1.000 | -6.420 |
| seasonal_naive | post_covid | 13 | -1.000 | 1.000 | 3.923 | -0.500 | 4.544 |
| gat | post_covid | 6 | 5.000 | -5.000 | 6.167 | 0.500 | -8.173 |

# Notes

- 101 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
