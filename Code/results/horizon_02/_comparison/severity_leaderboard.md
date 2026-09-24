Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.346 |
| arima | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.311 |
| dualtopo | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.077 |
| gat | post_covid | 4 | 0.082 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.044 | -0.159 |
| gnn_cascade | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.479 |
| gnn_st | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.496 |
| gnn_st_lagsonly | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.475 |
| gnn_st_noglobals | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.500 |
| lstm | exclude_covid | 4 | 0.082 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.456 | 0.033 |
| lstm | post_covid | 4 | 0.082 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.456 | 0.212 |
| persistence | exclude_covid | 4 | 0.082 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.456 | 0.136 |
| persistence | post_covid | 4 | 0.082 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.456 | 0.143 |
| seasonal_naive | exclude_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.672 |
| seasonal_naive | post_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.489 |
| xgboost | post_covid | 4 | 0.082 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.478 | 0.302 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.859 |
| arima | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.348 |
| dualtopo | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gat | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.025 |
| gnn_cascade | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.467 |
| gnn_st | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.495 |
| gnn_st_lagsonly | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.264 |
| gnn_st_noglobals | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.512 |
| lstm | exclude_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -0.932 |
| lstm | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.087 |
| persistence | exclude_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.691 |
| persistence | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.695 |
| seasonal_naive | exclude_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.527 |
| seasonal_naive | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.502 |
| xgboost | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.174 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| arima | post_covid | 49 | 0.939 | 0.980 | 0.361 | -0.041 |
| gnn_st_lagsonly | post_covid | 49 | 0.939 | 0.980 | 0.361 | -0.041 |
| xgboost | post_covid | 49 | 0.939 | 0.980 | 0.361 | -0.041 |
| arima | exclude_covid | 49 | 0.918 | 0.980 | 0.425 | -0.020 |
| dualtopo | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| gnn_cascade | post_covid | 49 | 0.918 | 0.980 | 0.425 | -0.020 |
| gnn_st | post_covid | 49 | 0.918 | 0.980 | 0.425 | -0.020 |
| gnn_st_noglobals | post_covid | 49 | 0.918 | 0.980 | 0.425 | -0.020 |
| lstm | post_covid | 49 | 0.918 | 0.980 | 0.313 | -0.020 |
| lstm | exclude_covid | 49 | 0.898 | 0.959 | 0.303 | 0.020 |
| persistence | exclude_covid | 49 | 0.898 | 0.980 | 0.384 | 0.000 |
| persistence | post_covid | 49 | 0.898 | 0.980 | 0.384 | 0.000 |
| gat | post_covid | 49 | 0.878 | 0.980 | -0.048 | -0.061 |
| seasonal_naive | exclude_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |
| seasonal_naive | post_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.290 |
| arima | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.254 |
| dualtopo | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.169 |
| gat | post_covid | 4 | 0.154 | 0 | 4 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.091 | -0.258 |
| gnn_cascade | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.434 |
| gnn_st | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.453 |
| gnn_st_lagsonly | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.431 |
| gnn_st_noglobals | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.457 |
| lstm | exclude_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | -0.049 |
| lstm | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.145 |
| persistence | exclude_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.063 |
| persistence | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.070 |
| seasonal_naive | exclude_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.813 |
| seasonal_naive | post_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.610 |
| xgboost | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.246 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.893 |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.373 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gat | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.044 |
| gnn_cascade | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.495 |
| gnn_st | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.523 |
| gnn_st_lagsonly | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.288 |
| gnn_st_noglobals | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.541 |
| lstm | exclude_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -0.968 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.108 |
| persistence | exclude_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.722 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.727 |
| seasonal_naive | exclude_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.574 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.548 |
| xgboost | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.196 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gat | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_cascade | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
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
| arima | post_covid | 26 | 0.885 | 0.962 | 0.322 | -0.077 |
| gnn_st_lagsonly | post_covid | 26 | 0.885 | 0.962 | 0.322 | -0.077 |
| xgboost | post_covid | 26 | 0.885 | 0.962 | 0.322 | -0.077 |
| arima | exclude_covid | 26 | 0.846 | 0.962 | 0.389 | -0.038 |
| dualtopo | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| gnn_cascade | post_covid | 26 | 0.846 | 0.962 | 0.389 | -0.038 |
| gnn_st | post_covid | 26 | 0.846 | 0.962 | 0.389 | -0.038 |
| gnn_st_noglobals | post_covid | 26 | 0.846 | 0.962 | 0.389 | -0.038 |
| lstm | post_covid | 26 | 0.846 | 0.962 | 0.260 | -0.038 |
| lstm | exclude_covid | 26 | 0.808 | 0.923 | 0.251 | 0.038 |
| persistence | exclude_covid | 26 | 0.808 | 0.962 | 0.338 | 0.000 |
| persistence | post_covid | 26 | 0.808 | 0.962 | 0.338 | 0.000 |
| gat | post_covid | 26 | 0.769 | 0.962 | -0.093 | -0.115 |
| seasonal_naive | exclude_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |
| seasonal_naive | post_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 51 | 0.081 | 30 | 21 | 15 | 0.588 | 0.333 | 0.455 | 0.625 | 0.562 | 0.445 |
| gnn_st_noglobals | post_covid | 51 | 0.081 | 30 | 21 | 15 | 0.588 | 0.333 | 0.455 | 0.625 | 0.562 | 0.449 |
| gnn_cascade | post_covid | 51 | 0.081 | 27 | 24 | 13 | 0.529 | 0.325 | 0.422 | 0.593 | 0.507 | 0.442 |
| gnn_st_lagsonly | post_covid | 51 | 0.081 | 26 | 25 | 16 | 0.510 | 0.381 | 0.388 | 0.559 | 0.482 | 0.425 |
| lstm | exclude_covid | 51 | 0.081 | 27 | 24 | 29 | 0.529 | 0.518 | 0.338 | 0.505 | 0.479 | 0.051 |
| lstm | post_covid | 51 | 0.081 | 24 | 27 | 20 | 0.471 | 0.455 | 0.338 | 0.505 | 0.436 | 0.220 |
| persistence | exclude_covid | 51 | 0.081 | 23 | 28 | 28 | 0.451 | 0.549 | 0.291 | 0.451 | 0.402 | 0.069 |
| persistence | post_covid | 51 | 0.081 | 23 | 28 | 28 | 0.451 | 0.549 | 0.291 | 0.451 | 0.402 | 0.074 |
| arima | exclude_covid | 51 | 0.081 | 21 | 30 | 23 | 0.412 | 0.523 | 0.284 | 0.442 | 0.372 | 0.098 |
| arima | post_covid | 51 | 0.081 | 19 | 32 | 19 | 0.373 | 0.500 | 0.271 | 0.427 | 0.340 | 0.175 |
| xgboost | post_covid | 51 | 0.081 | 16 | 35 | 21 | 0.314 | 0.568 | 0.222 | 0.364 | 0.277 | 0.195 |
| gat | post_covid | 51 | 0.081 | 2 | 49 | 22 | 0.039 | 0.917 | 0.027 | 0.053 | 0.001 | -0.126 |
| dualtopo | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.058 |
| seasonal_naive | exclude_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.665 |
| seasonal_naive | post_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.545 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 18 | 0.029 | 6 | 12 | 12 | 0.333 | 0.667 | 0.200 | 0.333 | 0.314 | -0.065 |
| persistence | post_covid | 18 | 0.029 | 6 | 12 | 12 | 0.333 | 0.667 | 0.200 | 0.333 | 0.314 | -0.065 |
| gnn_cascade | post_covid | 18 | 0.029 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.271 | 0.201 |
| gnn_st | post_covid | 18 | 0.029 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.271 | 0.207 |
| gnn_st_noglobals | post_covid | 18 | 0.029 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.271 | 0.206 |
| gnn_st_lagsonly | post_covid | 18 | 0.029 | 3 | 15 | 0 | 0.167 | 0.000 | 0.167 | 0.286 | 0.167 | 0.228 |
| arima | post_covid | 18 | 0.029 | 2 | 16 | 4 | 0.111 | 0.667 | 0.091 | 0.167 | 0.105 | 0.065 |
| dualtopo | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| gat | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.027 |
| lstm | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.067 |
| xgboost | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.007 |
| arima | exclude_covid | 18 | 0.029 | 0 | 18 | 9 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.268 |
| lstm | exclude_covid | 18 | 0.029 | 0 | 18 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.250 |
| seasonal_naive | exclude_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.971 |
| seasonal_naive | post_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.934 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.003 | 0 | 2 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.008 | -2.304 |
| arima | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.382 |
| dualtopo | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gat | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.005 |
| gnn_cascade | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.119 |
| gnn_st | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.200 |
| gnn_st_lagsonly | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.115 |
| gnn_st_noglobals | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.208 |
| lstm | exclude_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.189 |
| lstm | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.005 |
| persistence | exclude_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.006 |
| persistence | post_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.035 |
| seasonal_naive | exclude_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.028 |
| seasonal_naive | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.871 |
| xgboost | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.569 |

### All four bands — 627 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | post_covid | 627 | 0.928 | 0.984 | 0.532 | -0.035 |
| gnn_st | post_covid | 627 | 0.927 | 0.987 | 0.571 | -0.027 |
| gnn_st_noglobals | post_covid | 627 | 0.927 | 0.987 | 0.571 | -0.027 |
| gnn_st_lagsonly | post_covid | 627 | 0.923 | 0.986 | 0.487 | -0.041 |
| dualtopo | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| lstm | post_covid | 627 | 0.911 | 0.986 | 0.376 | -0.043 |
| arima | post_covid | 627 | 0.907 | 0.979 | 0.336 | -0.043 |
| xgboost | post_covid | 627 | 0.903 | 0.979 | 0.234 | -0.054 |
| arima | exclude_covid | 627 | 0.901 | 0.970 | 0.247 | -0.021 |
| persistence | exclude_covid | 627 | 0.901 | 0.970 | 0.374 | 0.000 |
| persistence | post_covid | 627 | 0.901 | 0.970 | 0.374 | 0.000 |
| lstm | exclude_covid | 627 | 0.895 | 0.971 | 0.348 | -0.005 |
| gat | post_covid | 627 | 0.887 | 0.971 | -0.011 | -0.075 |
| seasonal_naive | exclude_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |
| seasonal_naive | post_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 51 | 0.145 | 30 | 21 | 15 | 0.588 | 0.333 | 0.455 | 0.625 | 0.538 | 0.405 |
| gnn_st_noglobals | post_covid | 51 | 0.145 | 30 | 21 | 15 | 0.588 | 0.333 | 0.455 | 0.625 | 0.538 | 0.409 |
| gnn_cascade | post_covid | 51 | 0.145 | 27 | 24 | 13 | 0.529 | 0.325 | 0.422 | 0.593 | 0.486 | 0.401 |
| gnn_st_lagsonly | post_covid | 51 | 0.145 | 26 | 25 | 16 | 0.510 | 0.381 | 0.388 | 0.559 | 0.457 | 0.383 |
| lstm | exclude_covid | 51 | 0.145 | 27 | 24 | 29 | 0.529 | 0.518 | 0.338 | 0.505 | 0.433 | -0.018 |
| lstm | post_covid | 51 | 0.145 | 24 | 27 | 20 | 0.471 | 0.455 | 0.338 | 0.505 | 0.404 | 0.163 |
| persistence | exclude_covid | 51 | 0.145 | 23 | 28 | 28 | 0.451 | 0.549 | 0.291 | 0.451 | 0.358 | 0.006 |
| persistence | post_covid | 51 | 0.145 | 23 | 28 | 28 | 0.451 | 0.549 | 0.291 | 0.451 | 0.358 | 0.011 |
| arima | exclude_covid | 51 | 0.145 | 21 | 30 | 23 | 0.412 | 0.523 | 0.284 | 0.442 | 0.335 | 0.038 |
| arima | post_covid | 51 | 0.145 | 19 | 32 | 19 | 0.373 | 0.500 | 0.271 | 0.427 | 0.309 | 0.131 |
| xgboost | post_covid | 51 | 0.145 | 16 | 35 | 21 | 0.314 | 0.568 | 0.222 | 0.364 | 0.244 | 0.154 |
| dualtopo | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.130 |
| gat | post_covid | 51 | 0.145 | 2 | 49 | 22 | 0.039 | 0.917 | 0.027 | 0.053 | -0.034 | -0.209 |
| seasonal_naive | exclude_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.772 |
| seasonal_naive | post_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.625 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 18 | 0.051 | 6 | 12 | 12 | 0.333 | 0.667 | 0.200 | 0.333 | 0.297 | -0.090 |
| persistence | post_covid | 18 | 0.051 | 6 | 12 | 12 | 0.333 | 0.667 | 0.200 | 0.333 | 0.297 | -0.090 |
| gnn_cascade | post_covid | 18 | 0.051 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.266 | 0.183 |
| gnn_st | post_covid | 18 | 0.051 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.266 | 0.188 |
| gnn_st_noglobals | post_covid | 18 | 0.051 | 5 | 13 | 4 | 0.278 | 0.444 | 0.227 | 0.370 | 0.266 | 0.187 |
| gnn_st_lagsonly | post_covid | 18 | 0.051 | 3 | 15 | 0 | 0.167 | 0.000 | 0.167 | 0.286 | 0.167 | 0.210 |
| arima | post_covid | 18 | 0.051 | 2 | 16 | 4 | 0.111 | 0.667 | 0.091 | 0.167 | 0.099 | 0.044 |
| dualtopo | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| gat | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.051 |
| lstm | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.045 |
| xgboost | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| arima | exclude_covid | 18 | 0.051 | 0 | 18 | 9 | 0.000 | 1.000 | 0.000 | 0.000 | -0.027 | -0.298 |
| lstm | exclude_covid | 18 | 0.051 | 0 | 18 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.036 | -0.280 |
| seasonal_naive | exclude_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -1.016 |
| seasonal_naive | post_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -0.974 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 2 | 0.006 | 0 | 2 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.014 | -2.312 |
| arima | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.385 |
| dualtopo | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gat | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.007 |
| gnn_cascade | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.122 |
| gnn_st | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.203 |
| gnn_st_lagsonly | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.118 |
| gnn_st_noglobals | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.211 |
| lstm | exclude_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.192 |
| lstm | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.008 |
| persistence | exclude_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -1.011 |
| persistence | post_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -1.040 |
| seasonal_naive | exclude_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.038 |
| seasonal_naive | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.880 |
| xgboost | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.572 |

### All four bands — 352 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | post_covid | 352 | 0.872 | 0.972 | 0.507 | -0.062 |
| gnn_st | post_covid | 352 | 0.869 | 0.977 | 0.546 | -0.048 |
| gnn_st_noglobals | post_covid | 352 | 0.869 | 0.977 | 0.546 | -0.048 |
| gnn_st_lagsonly | post_covid | 352 | 0.864 | 0.974 | 0.459 | -0.074 |
| dualtopo | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| lstm | post_covid | 352 | 0.841 | 0.974 | 0.342 | -0.077 |
| arima | post_covid | 352 | 0.835 | 0.963 | 0.302 | -0.077 |
| xgboost | post_covid | 352 | 0.827 | 0.963 | 0.198 | -0.097 |
| arima | exclude_covid | 352 | 0.824 | 0.946 | 0.206 | -0.037 |
| persistence | exclude_covid | 352 | 0.824 | 0.946 | 0.335 | 0.000 |
| persistence | post_covid | 352 | 0.824 | 0.946 | 0.335 | 0.000 |
| lstm | exclude_covid | 352 | 0.812 | 0.949 | 0.304 | -0.009 |
| gat | post_covid | 352 | 0.798 | 0.949 | -0.044 | -0.134 |
| seasonal_naive | exclude_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |
| seasonal_naive | post_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14 | 2.000 | -2.000 | 1.571 | 1.500 | -2.656 |
| gnn_st_noglobals | post_covid | 14 | 2.000 | -2.000 | 1.571 | 1.500 | -2.483 |
| gnn_cascade | post_covid | 14 | 2.000 | -2.000 | 1.786 | 1.000 | -3.191 |
| gnn_st_lagsonly | post_covid | 14 | 2.000 | -2.000 | 1.786 | 2.000 | -5.753 |
| lstm | exclude_covid | 14 | 2.000 | -2.000 | 1.786 | 3.000 | -1.588 |
| lstm | post_covid | 13 | 2.000 | -2.000 | 1.923 | 2.000 | -9.789 |
| persistence | exclude_covid | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | post_covid | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| arima | post_covid | 13 | 2.000 | -2.000 | 2.231 | 2.000 | 1.873 |
| xgboost | post_covid | 11 | 2.000 | -2.000 | 2.273 | 0.500 | -3.751 |
| arima | exclude_covid | 13 | 2.000 | -2.000 | 2.769 | 2.000 | 0.866 |
| seasonal_naive | exclude_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| seasonal_naive | post_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| gat | post_covid | 13 | 4.000 | -4.000 | 4.077 | 3.000 | -2.476 |
| dualtopo | post_covid | 0 |  |  |  | -5.500 | -4.547 |

# Notes

- 13 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- --plot-models listed 7 models but only 4 validated colours exist; plotting the first 4.
