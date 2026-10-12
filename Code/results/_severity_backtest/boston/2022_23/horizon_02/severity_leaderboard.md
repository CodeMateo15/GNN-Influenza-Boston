Severity thresholds from the 2 reference seasons 2017-18, 2018-19, fitted on weeks before 2022-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 46.7, IT90 = 80.3, IT98 = 113.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.479 |
| persistence | full | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.535 |
| blend_baseline | full | 7 | 0.135 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.527 | 0.494 |
| gnn_st_nograph_tuned | full | 7 | 0.135 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.527 | 0.498 |
| gnn_st_tuned | full | 7 | 0.135 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.527 | 0.451 |
| lstm_tuned | full | 7 | 0.135 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.527 | 0.430 |
| xgboost_tuned | full | 7 | 0.135 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.527 | 0.446 |
| sarima | full | 7 | 0.135 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.505 | 0.467 |
| colagnn_tuned | full | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.001 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.479 | 0.279 |
| colagnn_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| flusight_baseline | full | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.241 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.229 | 0.277 |
| gnn_st_tuned | full | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.267 |
| lstm_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.113 |
| persistence | full | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.316 |
| sarima | full | 4 | 0.077 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.229 | 0.248 |
| xgboost_tuned | full | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.230 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 52 | 0.865 | 0.981 | 0.669 | -0.038 |
| colagnn_tuned | full | 52 | 0.865 | 0.923 | 0.000 | -0.212 |
| flusight_baseline | full | 52 | 0.865 | 0.981 | 0.700 | 0.000 |
| gnn_st_tuned | full | 52 | 0.865 | 0.981 | 0.601 | -0.077 |
| persistence | full | 52 | 0.865 | 0.981 | 0.700 | 0.000 |
| xgboost_tuned | full | 52 | 0.865 | 0.981 | 0.601 | -0.077 |
| gnn_st_nograph_tuned | full | 52 | 0.846 | 0.981 | 0.602 | -0.058 |
| lstm_tuned | full | 52 | 0.846 | 0.981 | 0.510 | -0.096 |
| sarima | full | 52 | 0.827 | 0.981 | 0.574 | -0.038 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.399 |
| persistence | full | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.451 |
| blend_baseline | full | 7 | 0.269 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.400 |
| gnn_st_nograph_tuned | full | 7 | 0.269 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.406 |
| gnn_st_tuned | full | 7 | 0.269 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.350 |
| lstm_tuned | full | 7 | 0.269 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.325 |
| xgboost_tuned | full | 7 | 0.269 | 4 | 3 | 2 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.344 |
| sarima | full | 7 | 0.269 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.414 | 0.369 |
| colagnn_tuned | full | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.181 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 2 | 2 | 1 | 0.500 | 0.333 | 0.400 | 0.571 | 0.455 | 0.214 |
| colagnn_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| flusight_baseline | full | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.173 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.205 | 0.211 |
| gnn_st_tuned | full | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.200 |
| lstm_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.032 |
| persistence | full | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.253 |
| sarima | full | 4 | 0.154 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.205 | 0.180 |
| xgboost_tuned | full | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.160 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | full | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 26 | 0.731 | 0.962 | 0.621 | -0.077 |
| colagnn_tuned | full | 26 | 0.731 | 0.846 | 0.000 | -0.423 |
| flusight_baseline | full | 26 | 0.731 | 0.962 | 0.651 | 0.000 |
| gnn_st_tuned | full | 26 | 0.731 | 0.962 | 0.547 | -0.154 |
| persistence | full | 26 | 0.731 | 0.962 | 0.651 | 0.000 |
| xgboost_tuned | full | 26 | 0.731 | 0.962 | 0.547 | -0.154 |
| gnn_st_nograph_tuned | full | 26 | 0.692 | 0.962 | 0.546 | -0.115 |
| lstm_tuned | full | 26 | 0.692 | 0.962 | 0.448 | -0.192 |
| sarima | full | 26 | 0.654 | 0.962 | 0.508 | -0.077 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 99 | 0.138 | 63 | 36 | 37 | 0.636 | 0.370 | 0.463 | 0.633 | 0.576 | 0.341 |
| persistence | full | 99 | 0.138 | 63 | 36 | 37 | 0.636 | 0.370 | 0.463 | 0.633 | 0.576 | 0.387 |
| blend_baseline | full | 99 | 0.138 | 55 | 44 | 31 | 0.556 | 0.360 | 0.423 | 0.595 | 0.505 | 0.383 |
| lstm_tuned | full | 99 | 0.138 | 53 | 46 | 28 | 0.535 | 0.346 | 0.417 | 0.589 | 0.490 | 0.407 |
| gnn_st_nograph_tuned | full | 99 | 0.138 | 52 | 47 | 29 | 0.525 | 0.358 | 0.406 | 0.578 | 0.478 | 0.390 |
| gnn_st_tuned | full | 99 | 0.138 | 51 | 48 | 26 | 0.515 | 0.338 | 0.408 | 0.580 | 0.473 | 0.393 |
| xgboost_tuned | full | 99 | 0.138 | 51 | 48 | 28 | 0.515 | 0.354 | 0.402 | 0.573 | 0.470 | 0.350 |
| sarima | full | 99 | 0.138 | 51 | 48 | 32 | 0.515 | 0.386 | 0.389 | 0.560 | 0.463 | 0.367 |
| colagnn_tuned | full | 99 | 0.138 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.019 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.056 | 15 | 25 | 25 | 0.375 | 0.625 | 0.231 | 0.375 | 0.338 | -0.040 |
| persistence | full | 40 | 0.056 | 15 | 25 | 25 | 0.375 | 0.625 | 0.231 | 0.375 | 0.338 | 0.038 |
| blend_baseline | full | 40 | 0.056 | 9 | 31 | 12 | 0.225 | 0.571 | 0.173 | 0.295 | 0.207 | 0.090 |
| gnn_st_nograph_tuned | full | 40 | 0.056 | 8 | 32 | 12 | 0.200 | 0.600 | 0.154 | 0.267 | 0.182 | 0.103 |
| sarima | full | 40 | 0.056 | 7 | 33 | 16 | 0.175 | 0.696 | 0.125 | 0.222 | 0.151 | 0.064 |
| gnn_st_tuned | full | 40 | 0.056 | 6 | 34 | 8 | 0.150 | 0.571 | 0.125 | 0.222 | 0.138 | 0.141 |
| xgboost_tuned | full | 40 | 0.056 | 6 | 34 | 10 | 0.150 | 0.625 | 0.120 | 0.214 | 0.135 | 0.104 |
| lstm_tuned | full | 40 | 0.056 | 1 | 39 | 5 | 0.025 | 0.833 | 0.022 | 0.043 | 0.018 | 0.076 |
| colagnn_tuned | full | 40 | 0.056 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.051 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 8 | 0.011 | 1 | 7 | 7 | 0.125 | 0.875 | 0.067 | 0.125 | 0.115 | -0.502 |
| persistence | full | 8 | 0.011 | 1 | 7 | 7 | 0.125 | 0.875 | 0.067 | 0.125 | 0.115 | -0.366 |
| colagnn_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |
| gnn_st_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.033 |
| lstm_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gnn_st_nograph_tuned | full | 8 | 0.011 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.057 |
| sarima | full | 8 | 0.011 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.168 |
| xgboost_tuned | full | 8 | 0.011 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.010 |
| blend_baseline | full | 8 | 0.011 | 0 | 8 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.093 |

### All four bands — 716 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 716 | 0.863 | 0.966 | 0.472 | -0.078 |
| colagnn_tuned | full | 716 | 0.862 | 0.944 | -0.000 | -0.205 |
| xgboost_tuned | full | 716 | 0.856 | 0.965 | 0.479 | -0.071 |
| blend_baseline | full | 716 | 0.855 | 0.968 | 0.516 | -0.052 |
| lstm_tuned | full | 716 | 0.855 | 0.972 | 0.460 | -0.084 |
| gnn_st_nograph_tuned | full | 716 | 0.853 | 0.968 | 0.507 | -0.063 |
| sarima | full | 716 | 0.852 | 0.958 | 0.446 | -0.056 |
| flusight_baseline | full | 716 | 0.848 | 0.965 | 0.566 | 0.001 |
| persistence | full | 716 | 0.848 | 0.965 | 0.566 | 0.001 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 99 | 0.273 | 63 | 36 | 35 | 0.636 | 0.357 | 0.470 | 0.640 | 0.504 | 0.262 |
| persistence | full | 99 | 0.273 | 63 | 36 | 35 | 0.636 | 0.357 | 0.470 | 0.640 | 0.504 | 0.311 |
| blend_baseline | full | 99 | 0.273 | 55 | 44 | 31 | 0.556 | 0.360 | 0.423 | 0.595 | 0.438 | 0.288 |
| lstm_tuned | full | 99 | 0.273 | 53 | 46 | 28 | 0.535 | 0.346 | 0.417 | 0.589 | 0.429 | 0.303 |
| gnn_st_tuned | full | 99 | 0.273 | 51 | 48 | 26 | 0.515 | 0.338 | 0.408 | 0.580 | 0.417 | 0.287 |
| gnn_st_nograph_tuned | full | 99 | 0.273 | 52 | 47 | 29 | 0.525 | 0.358 | 0.406 | 0.578 | 0.415 | 0.296 |
| xgboost_tuned | full | 99 | 0.273 | 51 | 48 | 28 | 0.515 | 0.354 | 0.402 | 0.573 | 0.409 | 0.246 |
| sarima | full | 99 | 0.273 | 51 | 48 | 32 | 0.515 | 0.386 | 0.389 | 0.560 | 0.394 | 0.262 |
| colagnn_tuned | full | 99 | 0.273 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.138 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.110 | 15 | 25 | 25 | 0.375 | 0.625 | 0.231 | 0.375 | 0.298 | -0.103 |
| persistence | full | 40 | 0.110 | 15 | 25 | 25 | 0.375 | 0.625 | 0.231 | 0.375 | 0.298 | -0.019 |
| blend_baseline | full | 40 | 0.110 | 9 | 31 | 12 | 0.225 | 0.571 | 0.173 | 0.295 | 0.188 | 0.035 |
| gnn_st_nograph_tuned | full | 40 | 0.110 | 8 | 32 | 12 | 0.200 | 0.600 | 0.154 | 0.267 | 0.163 | 0.048 |
| sarima | full | 40 | 0.110 | 7 | 33 | 16 | 0.175 | 0.696 | 0.125 | 0.222 | 0.125 | 0.007 |
| gnn_st_tuned | full | 40 | 0.110 | 6 | 34 | 8 | 0.150 | 0.571 | 0.125 | 0.222 | 0.125 | 0.089 |
| xgboost_tuned | full | 40 | 0.110 | 6 | 34 | 10 | 0.150 | 0.625 | 0.120 | 0.214 | 0.119 | 0.050 |
| lstm_tuned | full | 40 | 0.110 | 1 | 39 | 5 | 0.025 | 0.833 | 0.022 | 0.043 | 0.010 | 0.020 |
| colagnn_tuned | full | 40 | 0.110 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.115 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 8 | 0.022 | 1 | 7 | 7 | 0.125 | 0.875 | 0.067 | 0.125 | 0.105 | -0.519 |
| persistence | full | 8 | 0.022 | 1 | 7 | 7 | 0.125 | 0.875 | 0.067 | 0.125 | 0.105 | -0.382 |
| colagnn_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.022 |
| gnn_st_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.022 |
| lstm_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.014 |
| gnn_st_nograph_tuned | full | 8 | 0.022 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.069 |
| sarima | full | 8 | 0.022 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.181 |
| xgboost_tuned | full | 8 | 0.022 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.021 |
| blend_baseline | full | 8 | 0.022 | 0 | 8 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.008 | -0.105 |

### All four bands — 363 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 363 | 0.730 | 0.934 | 0.408 | -0.154 |
| colagnn_tuned | full | 363 | 0.727 | 0.890 | 0.000 | -0.405 |
| xgboost_tuned | full | 363 | 0.716 | 0.931 | 0.416 | -0.140 |
| blend_baseline | full | 363 | 0.713 | 0.937 | 0.452 | -0.102 |
| lstm_tuned | full | 363 | 0.713 | 0.945 | 0.395 | -0.165 |
| gnn_st_nograph_tuned | full | 363 | 0.711 | 0.937 | 0.445 | -0.124 |
| sarima | full | 363 | 0.708 | 0.917 | 0.375 | -0.110 |
| flusight_baseline | full | 363 | 0.705 | 0.931 | 0.506 | -0.003 |
| persistence | full | 363 | 0.705 | 0.931 | 0.506 | -0.003 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | full | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| blend_baseline | full | 14 | 3.000 | -3.000 | 3.071 | 2.000 | -6.142 |
| gnn_st_nograph_tuned | full | 14 | 3.000 | -3.000 | 3.214 | 2.000 | -6.481 |
| xgboost_tuned | full | 14 | 3.000 | -3.000 | 3.429 | 2.000 | -8.123 |
| gnn_st_tuned | full | 14 | 4.000 | -4.000 | 4.000 | 2.000 | -9.994 |
| lstm_tuned | full | 14 | 4.500 | -4.500 | 4.000 | 1.000 | -7.303 |
| sarima | full | 14 | 4.000 | -4.000 | 4.000 | 2.000 | -9.557 |
| colagnn_tuned | full | 0 |  |  |  | 1.500 | -15.524 |

# Notes

- 6 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
