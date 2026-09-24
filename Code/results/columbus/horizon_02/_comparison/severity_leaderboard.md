Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 8 | 0.151 | 6 | 2 | 4 | 0.750 | 0.400 | 0.500 | 0.667 | 0.661 | 0.349 |
| gnn_cascade | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.596 |
| gnn_st | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.575 |
| gnn_st_v2 | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.562 |
| xgboost | post_covid | 8 | 0.151 | 4 | 4 | 2 | 0.500 | 0.333 | 0.400 | 0.571 | 0.456 | 0.397 |
| persistence | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.368 |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.233 |
| lstm | post_covid | 8 | 0.151 | 3 | 5 | 4 | 0.375 | 0.571 | 0.250 | 0.400 | 0.286 | 0.289 |
| arima | post_covid | 8 | 0.151 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.263 |
| dualtopo | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.172 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_v2 | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_v2 | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 53 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | post_covid | 53 | 0.925 | 1.000 | 0.672 | -0.038 |
| gnn_st | post_covid | 53 | 0.925 | 1.000 | 0.672 | -0.038 |
| gnn_st_v2 | post_covid | 53 | 0.925 | 1.000 | 0.672 | -0.038 |
| gat | post_covid | 53 | 0.887 | 1.000 | 0.599 | 0.038 |
| xgboost | post_covid | 53 | 0.887 | 1.000 | 0.508 | -0.038 |
| arima | post_covid | 53 | 0.868 | 1.000 | 0.195 | -0.132 |
| dualtopo | post_covid | 53 | 0.849 | 1.000 | 0.000 | -0.151 |
| persistence | post_covid | 53 | 0.849 | 1.000 | 0.411 | 0.000 |
| lstm | post_covid | 53 | 0.830 | 1.000 | 0.302 | -0.019 |
| seasonal_naive | post_covid | 53 | 0.830 | 0.943 | 0.209 | 0.094 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.505 |
| gnn_st | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.480 |
| gnn_st_v2 | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.463 |
| gat | post_covid | 8 | 0.308 | 6 | 2 | 4 | 0.750 | 0.400 | 0.500 | 0.667 | 0.528 | 0.201 |
| xgboost | post_covid | 8 | 0.308 | 4 | 4 | 2 | 0.500 | 0.333 | 0.400 | 0.571 | 0.389 | 0.261 |
| persistence | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.235 |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.099 |
| lstm | post_covid | 8 | 0.308 | 3 | 5 | 4 | 0.375 | 0.571 | 0.250 | 0.400 | 0.153 | 0.142 |
| arima | post_covid | 8 | 0.308 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.097 |
| dualtopo | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.437 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_v2 | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_v2 | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| xgboost | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | post_covid | 26 | 0.846 | 1.000 | 0.612 | -0.077 |
| gnn_st | post_covid | 26 | 0.846 | 1.000 | 0.612 | -0.077 |
| gnn_st_v2 | post_covid | 26 | 0.846 | 1.000 | 0.612 | -0.077 |
| gat | post_covid | 26 | 0.769 | 1.000 | 0.494 | 0.077 |
| xgboost | post_covid | 26 | 0.769 | 1.000 | 0.418 | -0.077 |
| arima | post_covid | 26 | 0.731 | 1.000 | 0.165 | -0.269 |
| dualtopo | post_covid | 26 | 0.692 | 1.000 | 0.000 | -0.308 |
| persistence | post_covid | 26 | 0.692 | 1.000 | 0.278 | 0.000 |
| lstm | post_covid | 26 | 0.654 | 1.000 | 0.158 | -0.038 |
| seasonal_naive | post_covid | 26 | 0.654 | 0.885 | 0.080 | 0.192 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gat | post_covid | 118 | 0.131 | 72 | 46 | 83 | 0.610 | 0.535 | 0.358 | 0.527 | 0.504 | 0.137 |
| gnn_st | post_covid | 118 | 0.131 | 60 | 58 | 28 | 0.508 | 0.318 | 0.411 | 0.583 | 0.473 | 0.415 |
| gnn_st_v2 | post_covid | 118 | 0.131 | 59 | 59 | 24 | 0.500 | 0.289 | 0.415 | 0.587 | 0.469 | 0.415 |
| persistence | post_covid | 118 | 0.131 | 62 | 56 | 55 | 0.525 | 0.470 | 0.358 | 0.528 | 0.455 | 0.158 |
| gnn_cascade | post_covid | 118 | 0.131 | 55 | 63 | 28 | 0.466 | 0.337 | 0.377 | 0.547 | 0.430 | 0.416 |
| seasonal_naive | post_covid | 118 | 0.131 | 62 | 56 | 87 | 0.525 | 0.584 | 0.302 | 0.464 | 0.414 | -0.074 |
| xgboost | post_covid | 118 | 0.131 | 36 | 82 | 37 | 0.305 | 0.507 | 0.232 | 0.377 | 0.258 | 0.216 |
| arima | post_covid | 118 | 0.131 | 32 | 86 | 19 | 0.271 | 0.373 | 0.234 | 0.379 | 0.247 | 0.209 |
| lstm | post_covid | 118 | 0.131 | 33 | 85 | 40 | 0.280 | 0.548 | 0.209 | 0.346 | 0.229 | 0.190 |
| dualtopo | post_covid | 118 | 0.131 | 0 | 118 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.113 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 0.019 | 2 | 15 | 15 | 0.118 | 0.882 | 0.062 | 0.118 | 0.101 | -0.518 |
| xgboost | post_covid | 17 | 0.019 | 1 | 16 | 7 | 0.059 | 0.875 | 0.042 | 0.080 | 0.051 | -0.143 |
| seasonal_naive | post_covid | 17 | 0.019 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | 0.001 | -1.629 |
| dualtopo | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |
| gat | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.010 |
| lstm | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.055 |
| arima | post_covid | 17 | 0.019 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.042 |
| gnn_cascade | post_covid | 17 | 0.019 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.091 |
| gnn_st | post_covid | 17 | 0.019 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.054 |
| gnn_st_v2 | post_covid | 17 | 0.019 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.050 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.095 |
| dualtopo | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.004 |
| gat | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gnn_cascade | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.045 |
| gnn_st | post_covid | 4 | 0.004 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.095 |
| gnn_st_v2 | post_covid | 4 | 0.004 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.097 |
| lstm | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.005 |
| persistence | post_covid | 4 | 0.004 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.867 |
| seasonal_naive | post_covid | 4 | 0.004 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.013 | -2.990 |
| xgboost | post_covid | 4 | 0.004 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.583 |

### All four bands — 901 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 901 | 0.892 | 0.990 | 0.497 | -0.059 |
| gnn_st | post_covid | 901 | 0.889 | 0.990 | 0.492 | -0.053 |
| gnn_cascade | post_covid | 901 | 0.885 | 0.990 | 0.460 | -0.060 |
| arima | post_covid | 901 | 0.878 | 0.984 | 0.251 | -0.095 |
| dualtopo | post_covid | 901 | 0.869 | 0.981 | 0.000 | -0.154 |
| persistence | post_covid | 901 | 0.859 | 0.978 | 0.411 | -0.001 |
| lstm | post_covid | 901 | 0.858 | 0.983 | 0.215 | -0.073 |
| xgboost | post_covid | 901 | 0.858 | 0.980 | 0.278 | -0.060 |
| gat | post_covid | 901 | 0.847 | 0.989 | 0.399 | 0.018 |
| seasonal_naive | post_covid | 901 | 0.817 | 0.943 | 0.246 | 0.082 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 114 | 0.258 | 59 | 55 | 24 | 0.518 | 0.289 | 0.428 | 0.599 | 0.444 | 0.343 |
| gnn_st | post_covid | 114 | 0.258 | 60 | 54 | 28 | 0.526 | 0.318 | 0.423 | 0.594 | 0.441 | 0.343 |
| gnn_cascade | post_covid | 114 | 0.258 | 55 | 59 | 28 | 0.482 | 0.337 | 0.387 | 0.558 | 0.397 | 0.342 |
| persistence | post_covid | 114 | 0.258 | 62 | 52 | 51 | 0.544 | 0.451 | 0.376 | 0.546 | 0.388 | 0.107 |
| gat | post_covid | 114 | 0.258 | 72 | 42 | 83 | 0.632 | 0.535 | 0.365 | 0.535 | 0.379 | 0.001 |
| seasonal_naive | post_covid | 114 | 0.258 | 62 | 52 | 87 | 0.544 | 0.584 | 0.308 | 0.471 | 0.279 | -0.152 |
| arima | post_covid | 114 | 0.258 | 32 | 82 | 18 | 0.281 | 0.360 | 0.242 | 0.390 | 0.226 | 0.110 |
| xgboost | post_covid | 114 | 0.258 | 36 | 78 | 37 | 0.316 | 0.507 | 0.238 | 0.385 | 0.203 | 0.107 |
| lstm | post_covid | 114 | 0.258 | 33 | 81 | 40 | 0.289 | 0.548 | 0.214 | 0.353 | 0.168 | 0.086 |
| dualtopo | post_covid | 114 | 0.258 | 0 | 114 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.302 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 0.038 | 2 | 15 | 15 | 0.118 | 0.882 | 0.062 | 0.118 | 0.082 | -0.518 |
| xgboost | post_covid | 17 | 0.038 | 1 | 16 | 7 | 0.059 | 0.875 | 0.042 | 0.080 | 0.042 | -0.166 |
| dualtopo | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gat | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.010 |
| lstm | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.036 |
| arima | post_covid | 17 | 0.038 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -0.062 |
| gnn_cascade | post_covid | 17 | 0.038 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | 0.073 |
| gnn_st | post_covid | 17 | 0.038 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | 0.035 |
| gnn_st_v2 | post_covid | 17 | 0.038 | 0 | 17 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | 0.031 |
| seasonal_naive | post_covid | 17 | 0.038 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | -0.061 | -1.612 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.100 |
| dualtopo | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.009 |
| gat | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.010 |
| gnn_cascade | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.050 |
| gnn_st | post_covid | 4 | 0.009 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.100 |
| gnn_st_v2 | post_covid | 4 | 0.009 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.102 |
| lstm | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.000 |
| persistence | post_covid | 4 | 0.009 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -0.867 |
| seasonal_naive | post_covid | 4 | 0.009 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.027 | -2.978 |
| xgboost | post_covid | 4 | 0.009 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -0.590 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | post_covid | 442 | 0.790 | 0.980 | 0.448 | -0.111 |
| gnn_st | post_covid | 442 | 0.783 | 0.980 | 0.440 | -0.100 |
| gnn_cascade | post_covid | 442 | 0.774 | 0.980 | 0.406 | -0.113 |
| arima | post_covid | 442 | 0.762 | 0.968 | 0.202 | -0.188 |
| dualtopo | post_covid | 442 | 0.742 | 0.962 | 0.000 | -0.305 |
| persistence | post_covid | 442 | 0.731 | 0.955 | 0.342 | -0.002 |
| lstm | post_covid | 442 | 0.719 | 0.966 | 0.138 | -0.140 |
| xgboost | post_covid | 442 | 0.719 | 0.959 | 0.208 | -0.113 |
| gat | post_covid | 442 | 0.697 | 0.977 | 0.291 | 0.045 |
| seasonal_naive | post_covid | 442 | 0.636 | 0.885 | 0.133 | 0.176 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| gnn_cascade | post_covid | 16 | 1.000 | -1.000 | 2.062 | 1.500 | -4.892 |
| gnn_st | post_covid | 17 | 2.000 | -2.000 | 2.176 | 1.500 | -4.496 |
| gnn_st_v2 | post_covid | 17 | 2.000 | -2.000 | 2.294 | 1.000 | -4.569 |
| seasonal_naive | post_covid | 17 | 1.000 | -1.000 | 2.647 | 5.000 | 3.079 |
| gat | post_covid | 17 | 2.000 | -2.000 | 3.235 | 4.000 | -4.559 |
| arima | post_covid | 14 | 2.000 | -2.000 | 3.929 | 1.500 | -2.518 |
| lstm | post_covid | 15 | 3.000 | -3.000 | 4.067 | 1.000 | -4.107 |
| xgboost | post_covid | 16 | 3.000 | -3.000 | 4.688 | 2.000 | -8.043 |
| dualtopo | post_covid | 0 |  |  |  | 1.000 | -6.170 |

# Notes

- 22 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 4 neighborhood-weeks in this window, so its scores are reported but not ranked.
