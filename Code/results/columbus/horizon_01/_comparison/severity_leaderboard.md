Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 8 | 0.151 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.706 | 0.597 |
| lstm | post_covid | 8 | 0.151 | 6 | 2 | 3 | 0.750 | 0.333 | 0.545 | 0.706 | 0.683 | 0.522 |
| gnn_st | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.682 |
| gnn_st_v2 | post_covid | 8 | 0.151 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.603 | 0.682 |
| xgboost | post_covid | 8 | 0.151 | 4 | 4 | 1 | 0.500 | 0.200 | 0.444 | 0.615 | 0.478 | 0.489 |
| gat | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.230 |
| seasonal_naive | post_covid | 8 | 0.151 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.411 | 0.233 |
| arima | post_covid | 8 | 0.151 | 3 | 5 | 0 | 0.375 | 0.000 | 0.375 | 0.545 | 0.375 | 0.477 |
| dualtopo | post_covid | 8 | 0.151 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.177 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| gnn_st | post_covid | 53 | 0.925 | 1.000 | 0.672 | -0.038 |
| gnn_st_v2 | post_covid | 53 | 0.925 | 1.000 | 0.672 | -0.038 |
| persistence | post_covid | 53 | 0.925 | 1.000 | 0.706 | 0.000 |
| arima | post_covid | 53 | 0.906 | 1.000 | 0.505 | -0.094 |
| lstm | post_covid | 53 | 0.906 | 1.000 | 0.650 | 0.019 |
| xgboost | post_covid | 53 | 0.906 | 1.000 | 0.565 | -0.057 |
| dualtopo | post_covid | 53 | 0.849 | 1.000 | 0.000 | -0.151 |
| gat | post_covid | 53 | 0.849 | 1.000 | 0.411 | 0.000 |
| seasonal_naive | post_covid | 53 | 0.830 | 0.943 | 0.209 | 0.094 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 8 | 0.308 | 6 | 2 | 2 | 0.750 | 0.250 | 0.600 | 0.750 | 0.639 | 0.509 |
| lstm | post_covid | 8 | 0.308 | 6 | 2 | 3 | 0.750 | 0.333 | 0.545 | 0.706 | 0.583 | 0.416 |
| gnn_st | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.610 |
| gnn_st_v2 | post_covid | 8 | 0.308 | 5 | 3 | 1 | 0.625 | 0.167 | 0.556 | 0.714 | 0.569 | 0.611 |
| xgboost | post_covid | 8 | 0.308 | 4 | 4 | 1 | 0.500 | 0.200 | 0.444 | 0.615 | 0.444 | 0.373 |
| arima | post_covid | 8 | 0.308 | 3 | 5 | 0 | 0.375 | 0.000 | 0.375 | 0.545 | 0.375 | 0.359 |
| gat | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.056 |
| seasonal_naive | post_covid | 8 | 0.308 | 4 | 4 | 4 | 0.500 | 0.500 | 0.333 | 0.500 | 0.278 | 0.099 |
| dualtopo | post_covid | 8 | 0.308 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.444 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| gnn_st | post_covid | 26 | 0.846 | 1.000 | 0.612 | -0.077 |
| gnn_st_v2 | post_covid | 26 | 0.846 | 1.000 | 0.612 | -0.077 |
| persistence | post_covid | 26 | 0.846 | 1.000 | 0.639 | 0.000 |
| arima | post_covid | 26 | 0.808 | 1.000 | 0.454 | -0.192 |
| lstm | post_covid | 26 | 0.808 | 1.000 | 0.564 | 0.038 |
| xgboost | post_covid | 26 | 0.808 | 1.000 | 0.496 | -0.115 |
| dualtopo | post_covid | 26 | 0.692 | 1.000 | 0.000 | -0.308 |
| gat | post_covid | 26 | 0.692 | 1.000 | 0.278 | 0.000 |
| seasonal_naive | post_covid | 26 | 0.654 | 0.885 | 0.080 | 0.192 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 118 | 0.131 | 71 | 47 | 26 | 0.602 | 0.268 | 0.493 | 0.660 | 0.568 | 0.508 |
| gnn_st_v2 | post_covid | 118 | 0.131 | 71 | 47 | 27 | 0.602 | 0.276 | 0.490 | 0.657 | 0.567 | 0.507 |
| lstm | post_covid | 118 | 0.131 | 72 | 46 | 59 | 0.610 | 0.450 | 0.407 | 0.578 | 0.535 | 0.346 |
| persistence | post_covid | 118 | 0.131 | 69 | 49 | 49 | 0.585 | 0.415 | 0.413 | 0.585 | 0.522 | 0.323 |
| seasonal_naive | post_covid | 118 | 0.131 | 62 | 56 | 87 | 0.525 | 0.584 | 0.302 | 0.464 | 0.414 | -0.074 |
| arima | post_covid | 118 | 0.131 | 49 | 69 | 28 | 0.415 | 0.364 | 0.336 | 0.503 | 0.379 | 0.313 |
| xgboost | post_covid | 118 | 0.131 | 43 | 75 | 20 | 0.364 | 0.317 | 0.312 | 0.475 | 0.339 | 0.346 |
| gat | post_covid | 118 | 0.131 | 37 | 81 | 62 | 0.314 | 0.626 | 0.206 | 0.341 | 0.234 | 0.142 |
| dualtopo | post_covid | 118 | 0.131 | 0 | 118 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.134 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 0.019 | 6 | 11 | 11 | 0.353 | 0.647 | 0.214 | 0.353 | 0.340 | -0.077 |
| gnn_st | post_covid | 17 | 0.019 | 4 | 13 | 3 | 0.235 | 0.429 | 0.200 | 0.333 | 0.232 | 0.204 |
| gnn_st_v2 | post_covid | 17 | 0.019 | 4 | 13 | 3 | 0.235 | 0.429 | 0.200 | 0.333 | 0.232 | 0.204 |
| arima | post_covid | 17 | 0.019 | 2 | 15 | 2 | 0.118 | 0.500 | 0.105 | 0.190 | 0.115 | 0.150 |
| xgboost | post_covid | 17 | 0.019 | 2 | 15 | 5 | 0.118 | 0.714 | 0.091 | 0.167 | 0.112 | 0.064 |
| seasonal_naive | post_covid | 17 | 0.019 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | 0.001 | -1.629 |
| dualtopo | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |
| gat | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.043 |
| lstm | post_covid | 17 | 0.019 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.133 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.154 |
| dualtopo | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.004 |
| gat | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gnn_st | post_covid | 4 | 0.004 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.255 |
| gnn_st_v2 | post_covid | 4 | 0.004 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.256 |
| lstm | post_covid | 4 | 0.004 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.053 |
| persistence | post_covid | 4 | 0.004 | 1 | 3 | 3 | 0.250 | 0.750 | 0.143 | 0.250 | 0.247 | -0.135 |
| seasonal_naive | post_covid | 4 | 0.004 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.013 | -2.990 |
| xgboost | post_covid | 4 | 0.004 | 1 | 3 | 3 | 0.250 | 0.750 | 0.143 | 0.250 | 0.247 | -0.470 |

### All four bands — 901 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 901 | 0.902 | 0.996 | 0.642 | -0.038 |
| gnn_st_v2 | post_covid | 901 | 0.901 | 0.996 | 0.640 | -0.037 |
| xgboost | post_covid | 901 | 0.880 | 0.988 | 0.441 | -0.072 |
| arima | post_covid | 901 | 0.878 | 0.992 | 0.462 | -0.064 |
| lstm | post_covid | 901 | 0.870 | 0.990 | 0.485 | -0.009 |
| dualtopo | post_covid | 901 | 0.869 | 0.981 | 0.000 | -0.154 |
| persistence | post_covid | 901 | 0.866 | 0.994 | 0.594 | 0.000 |
| gat | post_covid | 901 | 0.836 | 0.986 | 0.215 | -0.044 |
| seasonal_naive | post_covid | 901 | 0.817 | 0.943 | 0.246 | 0.082 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 114 | 0.258 | 71 | 43 | 26 | 0.623 | 0.268 | 0.507 | 0.673 | 0.544 | 0.453 |
| gnn_st_v2 | post_covid | 114 | 0.258 | 71 | 43 | 27 | 0.623 | 0.276 | 0.504 | 0.670 | 0.540 | 0.452 |
| persistence | post_covid | 114 | 0.258 | 69 | 45 | 45 | 0.605 | 0.395 | 0.434 | 0.605 | 0.468 | 0.278 |
| lstm | post_covid | 114 | 0.258 | 72 | 42 | 59 | 0.632 | 0.450 | 0.416 | 0.588 | 0.452 | 0.260 |
| arima | post_covid | 114 | 0.258 | 49 | 65 | 27 | 0.430 | 0.355 | 0.348 | 0.516 | 0.348 | 0.231 |
| xgboost | post_covid | 114 | 0.258 | 43 | 71 | 20 | 0.377 | 0.317 | 0.321 | 0.486 | 0.316 | 0.266 |
| seasonal_naive | post_covid | 114 | 0.258 | 62 | 52 | 87 | 0.544 | 0.584 | 0.308 | 0.471 | 0.279 | -0.152 |
| gat | post_covid | 114 | 0.258 | 37 | 77 | 62 | 0.325 | 0.626 | 0.210 | 0.347 | 0.136 | 0.006 |
| dualtopo | post_covid | 114 | 0.258 | 0 | 114 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.328 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 0.038 | 6 | 11 | 11 | 0.353 | 0.647 | 0.214 | 0.353 | 0.327 | -0.080 |
| gnn_st | post_covid | 17 | 0.038 | 4 | 13 | 3 | 0.235 | 0.429 | 0.200 | 0.333 | 0.228 | 0.188 |
| gnn_st_v2 | post_covid | 17 | 0.038 | 4 | 13 | 3 | 0.235 | 0.429 | 0.200 | 0.333 | 0.228 | 0.188 |
| arima | post_covid | 17 | 0.038 | 2 | 15 | 2 | 0.118 | 0.500 | 0.105 | 0.190 | 0.113 | 0.133 |
| xgboost | post_covid | 17 | 0.038 | 2 | 15 | 5 | 0.118 | 0.714 | 0.091 | 0.167 | 0.106 | 0.046 |
| dualtopo | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gat | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.023 |
| lstm | post_covid | 17 | 0.038 | 0 | 17 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.115 |
| seasonal_naive | post_covid | 17 | 0.038 | 1 | 16 | 51 | 0.059 | 0.981 | 0.015 | 0.029 | -0.061 | -1.612 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.150 |
| dualtopo | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.009 |
| gat | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.008 |
| gnn_st | post_covid | 4 | 0.009 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.252 |
| gnn_st_v2 | post_covid | 4 | 0.009 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.252 |
| lstm | post_covid | 4 | 0.009 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.048 |
| persistence | post_covid | 4 | 0.009 | 1 | 3 | 3 | 0.250 | 0.750 | 0.143 | 0.250 | 0.243 | -0.137 |
| seasonal_naive | post_covid | 4 | 0.009 | 0 | 4 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.027 | -2.978 |
| xgboost | post_covid | 4 | 0.009 | 1 | 3 | 3 | 0.250 | 0.750 | 0.143 | 0.250 | 0.243 | -0.477 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 442 | 0.810 | 0.991 | 0.606 | -0.068 |
| gnn_st_v2 | post_covid | 442 | 0.808 | 0.991 | 0.603 | -0.066 |
| xgboost | post_covid | 442 | 0.765 | 0.975 | 0.397 | -0.138 |
| arima | post_covid | 442 | 0.762 | 0.984 | 0.416 | -0.124 |
| lstm | post_covid | 442 | 0.744 | 0.980 | 0.407 | -0.009 |
| persistence | post_covid | 442 | 0.744 | 0.989 | 0.555 | 0.000 |
| dualtopo | post_covid | 442 | 0.742 | 0.962 | 0.000 | -0.305 |
| gat | post_covid | 442 | 0.674 | 0.971 | 0.114 | -0.081 |
| seasonal_naive | post_covid | 442 | 0.636 | 0.885 | 0.133 | 0.176 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | post_covid | 17 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| gnn_st | post_covid | 17 | 1.000 | -1.000 | 1.706 | 0.000 | -2.647 |
| gnn_st_v2 | post_covid | 17 | 1.000 | -1.000 | 1.706 | 0.000 | -2.650 |
| lstm | post_covid | 17 | 1.000 | -1.000 | 2.176 | 0.000 | -2.226 |
| seasonal_naive | post_covid | 17 | 1.000 | -1.000 | 2.647 | 5.000 | 3.079 |
| arima | post_covid | 17 | 2.000 | -2.000 | 2.765 | 1.000 | -2.002 |
| xgboost | post_covid | 15 | 2.000 | -2.000 | 3.333 | 1.000 | -8.372 |
| gat | post_covid | 17 | 5.000 | -5.000 | 5.294 | 2.500 | -3.686 |
| dualtopo | post_covid | 0 |  |  |  | 1.000 | -6.595 |

# Notes

- 21 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 4 neighborhood-weeks in this window, so its scores are reported but not ranked.
