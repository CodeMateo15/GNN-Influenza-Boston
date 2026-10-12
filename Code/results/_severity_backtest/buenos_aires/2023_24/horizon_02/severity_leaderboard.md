Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2023-12-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 66.9, IT90 = 90.5, IT98 = 109.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 9 | 0.173 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.597 | 0.486 |
| sarima | post_covid | 9 | 0.173 | 5 | 4 | 1 | 0.556 | 0.167 | 0.500 | 0.667 | 0.532 | 0.382 |
| colagnn_tuned | post_covid | 9 | 0.173 | 4 | 5 | 1 | 0.444 | 0.200 | 0.400 | 0.571 | 0.421 | 0.437 |
| gnn_st_nograph_tuned | post_covid | 9 | 0.173 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.398 | 0.313 |
| gnn_st_tuned | post_covid | 9 | 0.173 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.398 | 0.355 |
| blend_baseline | post_covid | 9 | 0.173 | 4 | 5 | 3 | 0.444 | 0.429 | 0.333 | 0.500 | 0.375 | 0.293 |
| flusight_baseline | post_covid | 9 | 0.173 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.328 | 0.191 |
| persistence | post_covid | 9 | 0.173 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.328 | 0.195 |
| lstm_tuned | post_covid | 9 | 0.173 | 3 | 6 | 1 | 0.333 | 0.250 | 0.300 | 0.462 | 0.310 | 0.311 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.308 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.275 |
| flusight_baseline | post_covid | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.245 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.308 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.479 | 0.344 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.169 |
| persistence | post_covid | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.260 |
| sarima | post_covid | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.447 |
| xgboost_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.561 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| sarima | post_covid | 52 | 0.846 | 1.000 | 0.698 | -0.115 |
| colagnn_tuned | post_covid | 52 | 0.827 | 0.981 | 0.489 | -0.154 |
| gnn_st_nograph_tuned | post_covid | 52 | 0.827 | 0.981 | 0.547 | -0.115 |
| gnn_st_tuned | post_covid | 52 | 0.827 | 0.981 | 0.619 | -0.077 |
| lstm_tuned | post_covid | 52 | 0.827 | 0.962 | 0.348 | -0.173 |
| blend_baseline | post_covid | 52 | 0.808 | 0.962 | 0.536 | -0.038 |
| xgboost_tuned | post_covid | 52 | 0.808 | 1.000 | 0.608 | -0.077 |
| flusight_baseline | post_covid | 52 | 0.769 | 0.962 | 0.493 | 0.000 |
| persistence | post_covid | 52 | 0.769 | 0.962 | 0.493 | 0.000 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sarima | post_covid | 9 | 0.346 | 5 | 4 | 1 | 0.556 | 0.167 | 0.500 | 0.667 | 0.497 | 0.242 |
| xgboost_tuned | post_covid | 9 | 0.346 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.490 | 0.353 |
| colagnn_tuned | post_covid | 9 | 0.346 | 4 | 5 | 1 | 0.444 | 0.200 | 0.400 | 0.571 | 0.386 | 0.291 |
| gnn_st_nograph_tuned | post_covid | 9 | 0.346 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.327 | 0.132 |
| gnn_st_tuned | post_covid | 9 | 0.346 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.327 | 0.188 |
| lstm_tuned | post_covid | 9 | 0.346 | 3 | 6 | 1 | 0.333 | 0.250 | 0.300 | 0.462 | 0.275 | 0.129 |
| blend_baseline | post_covid | 9 | 0.346 | 4 | 5 | 3 | 0.444 | 0.429 | 0.333 | 0.500 | 0.268 | 0.119 |
| flusight_baseline | post_covid | 9 | 0.346 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.150 | 0.041 |
| persistence | post_covid | 9 | 0.346 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.150 | 0.017 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.245 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.209 |
| flusight_baseline | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.182 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.246 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.285 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.093 |
| persistence | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.193 |
| sarima | post_covid | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.398 |
| xgboost_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.521 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| sarima | post_covid | 26 | 0.692 | 1.000 | 0.652 | -0.231 |
| colagnn_tuned | post_covid | 26 | 0.654 | 0.962 | 0.429 | -0.308 |
| gnn_st_nograph_tuned | post_covid | 26 | 0.654 | 0.962 | 0.478 | -0.231 |
| gnn_st_tuned | post_covid | 26 | 0.654 | 0.962 | 0.556 | -0.154 |
| lstm_tuned | post_covid | 26 | 0.654 | 0.923 | 0.286 | -0.346 |
| blend_baseline | post_covid | 26 | 0.615 | 0.923 | 0.448 | -0.077 |
| xgboost_tuned | post_covid | 26 | 0.615 | 1.000 | 0.524 | -0.154 |
| flusight_baseline | post_covid | 26 | 0.538 | 0.923 | 0.379 | 0.000 |
| persistence | post_covid | 26 | 0.538 | 0.923 | 0.379 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 183 | 0.188 | 136 | 47 | 46 | 0.743 | 0.253 | 0.594 | 0.745 | 0.685 | 0.512 |
| persistence | post_covid | 183 | 0.188 | 136 | 47 | 46 | 0.743 | 0.253 | 0.594 | 0.745 | 0.685 | 0.520 |
| blend_baseline | post_covid | 183 | 0.188 | 129 | 54 | 39 | 0.705 | 0.232 | 0.581 | 0.735 | 0.655 | 0.561 |
| gnn_st_tuned | post_covid | 183 | 0.188 | 121 | 62 | 32 | 0.661 | 0.209 | 0.563 | 0.720 | 0.621 | 0.568 |
| gnn_st_nograph_tuned | post_covid | 183 | 0.188 | 118 | 65 | 26 | 0.645 | 0.181 | 0.565 | 0.722 | 0.612 | 0.556 |
| lstm_tuned | post_covid | 183 | 0.188 | 105 | 78 | 19 | 0.574 | 0.153 | 0.520 | 0.684 | 0.550 | 0.526 |
| sarima | post_covid | 183 | 0.188 | 99 | 84 | 66 | 0.541 | 0.400 | 0.398 | 0.569 | 0.457 | 0.233 |
| colagnn_tuned | post_covid | 183 | 0.188 | 88 | 95 | 21 | 0.481 | 0.193 | 0.431 | 0.603 | 0.454 | 0.436 |
| xgboost_tuned | post_covid | 183 | 0.188 | 81 | 102 | 91 | 0.443 | 0.529 | 0.296 | 0.456 | 0.327 | 0.086 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 76 | 0.078 | 46 | 30 | 30 | 0.605 | 0.395 | 0.434 | 0.605 | 0.572 | 0.283 |
| persistence | post_covid | 76 | 0.078 | 46 | 30 | 30 | 0.605 | 0.395 | 0.434 | 0.605 | 0.572 | 0.300 |
| blend_baseline | post_covid | 76 | 0.078 | 43 | 33 | 22 | 0.566 | 0.338 | 0.439 | 0.610 | 0.541 | 0.350 |
| gnn_st_tuned | post_covid | 76 | 0.078 | 39 | 37 | 17 | 0.513 | 0.304 | 0.419 | 0.591 | 0.494 | 0.366 |
| gnn_st_nograph_tuned | post_covid | 76 | 0.078 | 36 | 40 | 14 | 0.474 | 0.280 | 0.400 | 0.571 | 0.458 | 0.352 |
| sarima | post_covid | 76 | 0.078 | 31 | 45 | 27 | 0.408 | 0.466 | 0.301 | 0.463 | 0.378 | 0.184 |
| lstm_tuned | post_covid | 76 | 0.078 | 28 | 48 | 8 | 0.368 | 0.222 | 0.333 | 0.500 | 0.359 | 0.355 |
| xgboost_tuned | post_covid | 76 | 0.078 | 3 | 73 | 11 | 0.039 | 0.786 | 0.034 | 0.067 | 0.027 | 0.035 |
| colagnn_tuned | post_covid | 76 | 0.078 | 0 | 76 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | 0.192 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.041 | 19 | 21 | 21 | 0.475 | 0.525 | 0.311 | 0.475 | 0.452 | 0.170 |
| persistence | post_covid | 40 | 0.041 | 19 | 21 | 21 | 0.475 | 0.525 | 0.311 | 0.475 | 0.452 | 0.220 |
| blend_baseline | post_covid | 40 | 0.041 | 16 | 24 | 11 | 0.400 | 0.407 | 0.314 | 0.478 | 0.388 | 0.269 |
| sarima | post_covid | 40 | 0.041 | 14 | 26 | 11 | 0.350 | 0.440 | 0.275 | 0.431 | 0.338 | 0.141 |
| gnn_st_tuned | post_covid | 40 | 0.041 | 13 | 27 | 8 | 0.325 | 0.381 | 0.271 | 0.426 | 0.316 | 0.272 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.041 | 12 | 28 | 7 | 0.300 | 0.368 | 0.255 | 0.407 | 0.292 | 0.251 |
| lstm_tuned | post_covid | 40 | 0.041 | 5 | 35 | 5 | 0.125 | 0.500 | 0.111 | 0.200 | 0.120 | 0.229 |
| colagnn_tuned | post_covid | 40 | 0.041 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.104 |
| xgboost_tuned | post_covid | 40 | 0.041 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.000 |

### All four bands — 972 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 972 | 0.855 | 0.966 | 0.689 | -0.088 |
| blend_baseline | post_covid | 972 | 0.853 | 0.965 | 0.710 | -0.040 |
| gnn_st_tuned | post_covid | 972 | 0.852 | 0.966 | 0.695 | -0.071 |
| lstm_tuned | post_covid | 972 | 0.851 | 0.960 | 0.611 | -0.133 |
| flusight_baseline | post_covid | 972 | 0.846 | 0.960 | 0.714 | -0.001 |
| persistence | post_covid | 972 | 0.846 | 0.960 | 0.714 | -0.001 |
| colagnn_tuned | post_covid | 972 | 0.831 | 0.938 | 0.406 | -0.194 |
| sarima | post_covid | 972 | 0.801 | 0.945 | 0.548 | -0.052 |
| xgboost_tuned | post_covid | 972 | 0.767 | 0.929 | 0.229 | -0.113 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 165 | 0.334 | 123 | 42 | 34 | 0.745 | 0.217 | 0.618 | 0.764 | 0.642 | 0.482 |
| persistence | post_covid | 165 | 0.334 | 123 | 42 | 34 | 0.745 | 0.217 | 0.618 | 0.764 | 0.642 | 0.490 |
| blend_baseline | post_covid | 165 | 0.334 | 118 | 47 | 30 | 0.715 | 0.203 | 0.605 | 0.754 | 0.624 | 0.507 |
| gnn_st_nograph_tuned | post_covid | 165 | 0.334 | 109 | 56 | 22 | 0.661 | 0.168 | 0.583 | 0.736 | 0.594 | 0.490 |
| gnn_st_tuned | post_covid | 165 | 0.334 | 111 | 54 | 26 | 0.673 | 0.190 | 0.581 | 0.735 | 0.594 | 0.509 |
| lstm_tuned | post_covid | 165 | 0.334 | 96 | 69 | 14 | 0.582 | 0.127 | 0.536 | 0.698 | 0.539 | 0.467 |
| colagnn_tuned | post_covid | 165 | 0.334 | 88 | 77 | 21 | 0.533 | 0.193 | 0.473 | 0.642 | 0.470 | 0.386 |
| sarima | post_covid | 165 | 0.334 | 94 | 71 | 41 | 0.570 | 0.304 | 0.456 | 0.627 | 0.445 | 0.224 |
| xgboost_tuned | post_covid | 165 | 0.334 | 72 | 93 | 79 | 0.436 | 0.523 | 0.295 | 0.456 | 0.196 | -0.043 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 74 | 0.150 | 44 | 30 | 27 | 0.595 | 0.380 | 0.436 | 0.607 | 0.530 | 0.255 |
| persistence | post_covid | 74 | 0.150 | 44 | 30 | 27 | 0.595 | 0.380 | 0.436 | 0.607 | 0.530 | 0.284 |
| blend_baseline | post_covid | 74 | 0.150 | 41 | 33 | 21 | 0.554 | 0.339 | 0.432 | 0.603 | 0.504 | 0.308 |
| gnn_st_tuned | post_covid | 74 | 0.150 | 38 | 36 | 16 | 0.514 | 0.296 | 0.422 | 0.594 | 0.475 | 0.320 |
| gnn_st_nograph_tuned | post_covid | 74 | 0.150 | 35 | 39 | 13 | 0.473 | 0.271 | 0.402 | 0.574 | 0.442 | 0.302 |
| sarima | post_covid | 74 | 0.150 | 31 | 43 | 16 | 0.419 | 0.340 | 0.344 | 0.512 | 0.381 | 0.250 |
| lstm_tuned | post_covid | 74 | 0.150 | 27 | 47 | 7 | 0.365 | 0.206 | 0.333 | 0.500 | 0.348 | 0.307 |
| xgboost_tuned | post_covid | 74 | 0.150 | 3 | 71 | 9 | 0.041 | 0.750 | 0.036 | 0.070 | 0.019 | 0.003 |
| colagnn_tuned | post_covid | 74 | 0.150 | 0 | 74 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.152 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.081 | 19 | 21 | 19 | 0.475 | 0.500 | 0.322 | 0.487 | 0.433 | 0.180 |
| persistence | post_covid | 40 | 0.081 | 19 | 21 | 19 | 0.475 | 0.500 | 0.322 | 0.487 | 0.433 | 0.235 |
| blend_baseline | post_covid | 40 | 0.081 | 16 | 24 | 9 | 0.400 | 0.360 | 0.327 | 0.492 | 0.380 | 0.255 |
| sarima | post_covid | 40 | 0.081 | 14 | 26 | 10 | 0.350 | 0.417 | 0.280 | 0.438 | 0.328 | 0.205 |
| gnn_st_tuned | post_covid | 40 | 0.081 | 13 | 27 | 8 | 0.325 | 0.381 | 0.271 | 0.426 | 0.307 | 0.249 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.081 | 12 | 28 | 7 | 0.300 | 0.368 | 0.255 | 0.407 | 0.285 | 0.224 |
| lstm_tuned | post_covid | 40 | 0.081 | 5 | 35 | 5 | 0.125 | 0.500 | 0.111 | 0.200 | 0.114 | 0.202 |
| colagnn_tuned | post_covid | 40 | 0.081 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.073 |
| xgboost_tuned | post_covid | 40 | 0.081 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.007 | -0.020 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 494 | 0.745 | 0.933 | 0.680 | -0.089 |
| gnn_st_nograph_tuned | post_covid | 494 | 0.743 | 0.935 | 0.655 | -0.164 |
| gnn_st_tuned | post_covid | 494 | 0.739 | 0.935 | 0.661 | -0.136 |
| flusight_baseline | post_covid | 494 | 0.737 | 0.923 | 0.682 | -0.026 |
| lstm_tuned | post_covid | 494 | 0.737 | 0.923 | 0.572 | -0.253 |
| persistence | post_covid | 494 | 0.737 | 0.923 | 0.682 | -0.026 |
| colagnn_tuned | post_covid | 494 | 0.704 | 0.883 | 0.365 | -0.342 |
| sarima | post_covid | 494 | 0.686 | 0.919 | 0.554 | -0.148 |
| xgboost_tuned | post_covid | 494 | 0.585 | 0.868 | 0.127 | -0.229 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 15 | 2.000 | -2.000 | 1.800 | 2.000 | -6.189 |
| blend_baseline | post_covid | 15 | 2.000 | -2.000 | 1.867 | 2.000 | -2.913 |
| gnn_st_nograph_tuned | post_covid | 15 | 2.000 | -2.000 | 1.933 | 2.000 | -6.755 |
| flusight_baseline | post_covid | 16 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | post_covid | 16 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| lstm_tuned | post_covid | 13 | 2.000 | -2.000 | 2.154 | 2.000 | -11.047 |
| sarima | post_covid | 13 | 1.000 | -1.000 | 2.692 | 0.000 | -2.413 |
| colagnn_tuned | post_covid | 14 | 2.000 | -2.000 | 3.357 | 2.000 | -14.503 |
| xgboost_tuned | post_covid | 14 | -1.000 | 1.000 | 6.214 | 0.000 | -10.896 |

# Notes

- 89 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
