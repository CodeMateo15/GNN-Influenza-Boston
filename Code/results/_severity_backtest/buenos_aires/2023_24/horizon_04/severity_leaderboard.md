Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2023-12-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 66.9, IT90 = 90.5, IT98 = 109.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sarima | post_covid | 9 | 0.173 | 7 | 2 | 5 | 0.778 | 0.417 | 0.500 | 0.667 | 0.661 | 0.405 |
| gnn_st_tuned | post_covid | 9 | 0.173 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.620 | 0.463 |
| xgboost_tuned | post_covid | 9 | 0.173 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.597 | 0.494 |
| gnn_st_nograph_tuned | post_covid | 9 | 0.173 | 5 | 4 | 2 | 0.556 | 0.286 | 0.455 | 0.625 | 0.509 | 0.430 |
| blend_baseline | post_covid | 9 | 0.173 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.398 | 0.265 |
| lstm_tuned | post_covid | 9 | 0.173 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.398 | 0.436 |
| flusight_baseline | post_covid | 9 | 0.173 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.328 | -0.082 |
| persistence | post_covid | 9 | 0.173 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.328 | -0.083 |
| colagnn_tuned | post_covid | 9 | 0.173 | 0 | 9 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.339 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.133 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.086 |
| flusight_baseline | post_covid | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.479 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.161 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.226 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.142 |
| persistence | post_covid | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.449 |
| sarima | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.339 |
| xgboost_tuned | post_covid | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.543 |

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
| blend_baseline | post_covid | 52 | 0.827 | 0.942 | 0.321 | -0.115 |
| colagnn_tuned | post_covid | 52 | 0.827 | 0.923 | 0.000 | -0.250 |
| gnn_st_nograph_tuned | post_covid | 52 | 0.827 | 0.981 | 0.510 | -0.115 |
| gnn_st_tuned | post_covid | 52 | 0.827 | 1.000 | 0.640 | -0.096 |
| xgboost_tuned | post_covid | 52 | 0.827 | 1.000 | 0.679 | -0.058 |
| lstm_tuned | post_covid | 52 | 0.808 | 0.981 | 0.458 | -0.135 |
| sarima | post_covid | 52 | 0.788 | 1.000 | 0.593 | -0.019 |
| flusight_baseline | post_covid | 52 | 0.750 | 0.904 | 0.211 | 0.000 |
| persistence | post_covid | 52 | 0.750 | 0.904 | 0.211 | 0.000 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 9 | 0.346 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.549 | 0.327 |
| xgboost_tuned | post_covid | 9 | 0.346 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.490 | 0.364 |
| sarima | post_covid | 9 | 0.346 | 7 | 2 | 5 | 0.778 | 0.417 | 0.500 | 0.667 | 0.484 | 0.257 |
| gnn_st_nograph_tuned | post_covid | 9 | 0.346 | 5 | 4 | 2 | 0.556 | 0.286 | 0.455 | 0.625 | 0.438 | 0.285 |
| blend_baseline | post_covid | 9 | 0.346 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.327 | 0.086 |
| lstm_tuned | post_covid | 9 | 0.346 | 4 | 5 | 2 | 0.444 | 0.333 | 0.364 | 0.533 | 0.327 | 0.288 |
| flusight_baseline | post_covid | 9 | 0.346 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.150 | -0.214 |
| persistence | post_covid | 9 | 0.346 | 4 | 5 | 5 | 0.444 | 0.556 | 0.286 | 0.444 | 0.150 | -0.296 |
| colagnn_tuned | post_covid | 9 | 0.346 | 0 | 9 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.176 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | -0.236 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.003 |
| flusight_baseline | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.575 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.085 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.156 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.064 |
| persistence | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.579 |
| sarima | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.279 |
| xgboost_tuned | post_covid | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.501 |

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
| blend_baseline | post_covid | 26 | 0.654 | 0.885 | 0.217 | -0.231 |
| colagnn_tuned | post_covid | 26 | 0.654 | 0.846 | 0.000 | -0.500 |
| gnn_st_nograph_tuned | post_covid | 26 | 0.654 | 0.962 | 0.429 | -0.231 |
| gnn_st_tuned | post_covid | 26 | 0.654 | 1.000 | 0.571 | -0.192 |
| xgboost_tuned | post_covid | 26 | 0.654 | 1.000 | 0.609 | -0.115 |
| lstm_tuned | post_covid | 26 | 0.615 | 0.962 | 0.381 | -0.269 |
| sarima | post_covid | 26 | 0.577 | 1.000 | 0.476 | -0.038 |
| flusight_baseline | post_covid | 26 | 0.500 | 0.808 | 0.034 | 0.000 |
| persistence | post_covid | 26 | 0.500 | 0.808 | 0.034 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 183 | 0.188 | 111 | 72 | 68 | 0.607 | 0.380 | 0.442 | 0.613 | 0.520 | 0.272 |
| persistence | post_covid | 183 | 0.188 | 111 | 72 | 68 | 0.607 | 0.380 | 0.442 | 0.613 | 0.520 | 0.295 |
| blend_baseline | post_covid | 183 | 0.188 | 104 | 79 | 45 | 0.568 | 0.302 | 0.456 | 0.627 | 0.511 | 0.406 |
| sarima | post_covid | 183 | 0.188 | 116 | 67 | 114 | 0.634 | 0.496 | 0.391 | 0.562 | 0.489 | 0.174 |
| gnn_st_tuned | post_covid | 183 | 0.188 | 98 | 85 | 46 | 0.536 | 0.319 | 0.428 | 0.599 | 0.477 | 0.385 |
| lstm_tuned | post_covid | 183 | 0.188 | 89 | 94 | 33 | 0.486 | 0.270 | 0.412 | 0.584 | 0.445 | 0.405 |
| gnn_st_nograph_tuned | post_covid | 183 | 0.188 | 89 | 94 | 41 | 0.486 | 0.315 | 0.397 | 0.569 | 0.434 | 0.389 |
| xgboost_tuned | post_covid | 183 | 0.188 | 73 | 110 | 95 | 0.399 | 0.565 | 0.263 | 0.416 | 0.279 | -0.003 |
| colagnn_tuned | post_covid | 183 | 0.188 | 30 | 153 | 6 | 0.164 | 0.167 | 0.159 | 0.274 | 0.156 | 0.229 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 76 | 0.078 | 30 | 46 | 46 | 0.395 | 0.605 | 0.246 | 0.395 | 0.343 | -0.059 |
| persistence | post_covid | 76 | 0.078 | 30 | 46 | 46 | 0.395 | 0.605 | 0.246 | 0.395 | 0.343 | -0.051 |
| sarima | post_covid | 76 | 0.078 | 25 | 51 | 53 | 0.329 | 0.679 | 0.194 | 0.325 | 0.270 | 0.031 |
| blend_baseline | post_covid | 76 | 0.078 | 20 | 56 | 23 | 0.263 | 0.535 | 0.202 | 0.336 | 0.237 | 0.110 |
| gnn_st_tuned | post_covid | 76 | 0.078 | 7 | 69 | 12 | 0.092 | 0.632 | 0.080 | 0.147 | 0.079 | 0.171 |
| gnn_st_nograph_tuned | post_covid | 76 | 0.078 | 6 | 70 | 12 | 0.079 | 0.667 | 0.068 | 0.128 | 0.066 | 0.154 |
| xgboost_tuned | post_covid | 76 | 0.078 | 6 | 70 | 21 | 0.079 | 0.778 | 0.062 | 0.117 | 0.056 | -0.022 |
| lstm_tuned | post_covid | 76 | 0.078 | 5 | 71 | 10 | 0.066 | 0.667 | 0.058 | 0.110 | 0.055 | 0.131 |
| colagnn_tuned | post_covid | 76 | 0.078 | 0 | 76 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.041 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.041 | 10 | 30 | 30 | 0.250 | 0.750 | 0.143 | 0.250 | 0.218 | -0.277 |
| persistence | post_covid | 40 | 0.041 | 10 | 30 | 30 | 0.250 | 0.750 | 0.143 | 0.250 | 0.218 | -0.229 |
| sarima | post_covid | 40 | 0.041 | 8 | 32 | 13 | 0.200 | 0.619 | 0.151 | 0.262 | 0.186 | -0.122 |
| blend_baseline | post_covid | 40 | 0.041 | 3 | 37 | 12 | 0.075 | 0.800 | 0.058 | 0.109 | 0.062 | 0.008 |
| colagnn_tuned | post_covid | 40 | 0.041 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.004 |
| gnn_st_tuned | post_covid | 40 | 0.041 | 0 | 40 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.073 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.041 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.065 |
| lstm_tuned | post_covid | 40 | 0.041 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.012 |
| xgboost_tuned | post_covid | 40 | 0.041 | 0 | 40 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.029 |

### All four bands — 972 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | post_covid | 972 | 0.824 | 0.925 | 0.128 | -0.271 |
| blend_baseline | post_covid | 972 | 0.819 | 0.939 | 0.476 | -0.095 |
| lstm_tuned | post_covid | 972 | 0.818 | 0.940 | 0.390 | -0.164 |
| gnn_st_tuned | post_covid | 972 | 0.814 | 0.940 | 0.403 | -0.138 |
| gnn_st_nograph_tuned | post_covid | 972 | 0.812 | 0.939 | 0.372 | -0.152 |
| flusight_baseline | post_covid | 972 | 0.797 | 0.923 | 0.496 | -0.004 |
| persistence | post_covid | 972 | 0.797 | 0.923 | 0.496 | -0.004 |
| xgboost_tuned | post_covid | 972 | 0.755 | 0.921 | 0.212 | -0.101 |
| sarima | post_covid | 972 | 0.753 | 0.919 | 0.456 | 0.031 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 165 | 0.334 | 93 | 72 | 38 | 0.564 | 0.290 | 0.458 | 0.628 | 0.448 | 0.291 |
| flusight_baseline | post_covid | 165 | 0.334 | 97 | 68 | 52 | 0.588 | 0.349 | 0.447 | 0.618 | 0.430 | 0.205 |
| persistence | post_covid | 165 | 0.334 | 97 | 68 | 52 | 0.588 | 0.349 | 0.447 | 0.618 | 0.430 | 0.215 |
| gnn_st_tuned | post_covid | 165 | 0.334 | 92 | 73 | 43 | 0.558 | 0.319 | 0.442 | 0.613 | 0.427 | 0.281 |
| lstm_tuned | post_covid | 165 | 0.334 | 83 | 82 | 31 | 0.503 | 0.272 | 0.423 | 0.595 | 0.409 | 0.301 |
| gnn_st_nograph_tuned | post_covid | 165 | 0.334 | 85 | 80 | 39 | 0.515 | 0.315 | 0.417 | 0.588 | 0.397 | 0.285 |
| sarima | post_covid | 165 | 0.334 | 110 | 55 | 98 | 0.667 | 0.471 | 0.418 | 0.590 | 0.369 | 0.110 |
| colagnn_tuned | post_covid | 165 | 0.334 | 30 | 135 | 6 | 0.182 | 0.167 | 0.175 | 0.299 | 0.164 | 0.158 |
| xgboost_tuned | post_covid | 165 | 0.334 | 68 | 97 | 88 | 0.412 | 0.564 | 0.269 | 0.424 | 0.145 | -0.160 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 74 | 0.150 | 28 | 46 | 39 | 0.378 | 0.582 | 0.248 | 0.397 | 0.286 | -0.083 |
| persistence | post_covid | 74 | 0.150 | 28 | 46 | 39 | 0.378 | 0.582 | 0.248 | 0.397 | 0.286 | -0.064 |
| sarima | post_covid | 74 | 0.150 | 25 | 49 | 41 | 0.338 | 0.621 | 0.217 | 0.357 | 0.240 | 0.078 |
| blend_baseline | post_covid | 74 | 0.150 | 20 | 54 | 21 | 0.270 | 0.512 | 0.211 | 0.348 | 0.220 | 0.053 |
| gnn_st_tuned | post_covid | 74 | 0.150 | 7 | 67 | 11 | 0.095 | 0.611 | 0.082 | 0.152 | 0.068 | 0.123 |
| gnn_st_nograph_tuned | post_covid | 74 | 0.150 | 6 | 68 | 11 | 0.081 | 0.647 | 0.071 | 0.132 | 0.055 | 0.104 |
| lstm_tuned | post_covid | 74 | 0.150 | 5 | 69 | 9 | 0.068 | 0.643 | 0.060 | 0.114 | 0.046 | 0.074 |
| xgboost_tuned | post_covid | 74 | 0.150 | 6 | 68 | 20 | 0.081 | 0.769 | 0.064 | 0.120 | 0.033 | -0.066 |
| colagnn_tuned | post_covid | 74 | 0.150 | 0 | 74 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.010 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.081 | 10 | 30 | 26 | 0.250 | 0.722 | 0.152 | 0.263 | 0.193 | -0.250 |
| persistence | post_covid | 40 | 0.081 | 10 | 30 | 26 | 0.250 | 0.722 | 0.152 | 0.263 | 0.193 | -0.194 |
| sarima | post_covid | 40 | 0.081 | 8 | 32 | 11 | 0.200 | 0.579 | 0.157 | 0.271 | 0.176 | -0.063 |
| blend_baseline | post_covid | 40 | 0.081 | 3 | 37 | 12 | 0.075 | 0.800 | 0.058 | 0.109 | 0.049 | -0.025 |
| colagnn_tuned | post_covid | 40 | 0.081 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.009 |
| gnn_st_tuned | post_covid | 40 | 0.081 | 0 | 40 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | 0.039 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.081 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.007 | 0.030 |
| lstm_tuned | post_covid | 40 | 0.081 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.007 | -0.027 |
| xgboost_tuned | post_covid | 40 | 0.081 | 0 | 40 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.013 | -0.053 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | post_covid | 494 | 0.690 | 0.856 | 0.105 | -0.492 |
| blend_baseline | post_covid | 494 | 0.678 | 0.883 | 0.407 | -0.186 |
| lstm_tuned | post_covid | 494 | 0.672 | 0.887 | 0.328 | -0.300 |
| gnn_st_tuned | post_covid | 494 | 0.664 | 0.889 | 0.335 | -0.251 |
| gnn_st_nograph_tuned | post_covid | 494 | 0.662 | 0.887 | 0.308 | -0.273 |
| flusight_baseline | post_covid | 494 | 0.654 | 0.856 | 0.425 | -0.055 |
| persistence | post_covid | 494 | 0.654 | 0.856 | 0.425 | -0.055 |
| sarima | post_covid | 494 | 0.575 | 0.864 | 0.398 | 0.028 |
| xgboost_tuned | post_covid | 494 | 0.559 | 0.850 | 0.100 | -0.184 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| sarima | post_covid | 13 | -2.000 | 2.000 | 3.308 | 2.000 | -11.175 |
| gnn_st_tuned | post_covid | 14 | 1.500 | -1.500 | 3.500 | 1.000 | -10.661 |
| gnn_st_nograph_tuned | post_covid | 14 | 2.000 | -2.000 | 3.714 | 0.000 | -11.543 |
| flusight_baseline | post_covid | 15 | 4.000 | -4.000 | 3.800 | 4.000 | 0.000 |
| persistence | post_covid | 15 | 4.000 | -4.000 | 3.800 | 4.000 | 0.000 |
| blend_baseline | post_covid | 15 | 4.000 | -4.000 | 4.000 | 1.000 | -10.042 |
| lstm_tuned | post_covid | 14 | 3.000 | -3.000 | 4.143 | 1.000 | -14.310 |
| colagnn_tuned | post_covid | 6 | 4.000 | -4.000 | 5.500 | 2.000 | -18.856 |
| xgboost_tuned | post_covid | 12 | -2.000 | 2.000 | 5.917 | 0.000 | -14.579 |

# Notes

- 23 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
