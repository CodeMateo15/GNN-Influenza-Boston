Severity thresholds from the 3 reference seasons 2017-18, 2018-19, 2022-23, fitted on weeks before 2023-06-01, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 58.4, IT90 = 94.5, IT98 = 128.6 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.571 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.039 | -0.315 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.646 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.315 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.390 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.815 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.805 |
| sarima | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.414 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.437 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

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
| gnn_st_nograph_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| gnn_st_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| xgboost_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| blend_baseline | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| flusight_baseline | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| lstm_tuned | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| persistence | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| sarima | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| colagnn_tuned | full | 52 | 0.942 | 1.000 | -0.026 | 0.019 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.599 |
| colagnn_tuned | full | 1 | 0.037 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.077 | -0.340 |
| flusight_baseline | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.676 |
| gnn_st_nograph_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.340 |
| gnn_st_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.415 |
| lstm_tuned | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.849 |
| persistence | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.837 |
| sarima | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.440 |
| xgboost_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.463 |

### Crossing IT90 — **underpowered: 0 observed events**, not ranked

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

### All four bands — 27 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| gnn_st_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| xgboost_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| blend_baseline | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| flusight_baseline | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| lstm_tuned | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| persistence | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| sarima | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| colagnn_tuned | full | 27 | 0.889 | 1.000 | -0.052 | 0.037 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 52 | 0.073 | 27 | 25 | 25 | 0.519 | 0.481 | 0.351 | 0.519 | 0.481 | 0.237 |
| persistence | full | 52 | 0.073 | 27 | 25 | 25 | 0.519 | 0.481 | 0.351 | 0.519 | 0.481 | 0.219 |
| blend_baseline | full | 52 | 0.073 | 24 | 28 | 17 | 0.462 | 0.415 | 0.348 | 0.516 | 0.436 | 0.266 |
| gnn_st_nograph_tuned | full | 52 | 0.073 | 22 | 30 | 11 | 0.423 | 0.333 | 0.349 | 0.518 | 0.406 | 0.321 |
| xgboost_tuned | full | 52 | 0.073 | 22 | 30 | 15 | 0.423 | 0.405 | 0.328 | 0.494 | 0.400 | 0.296 |
| sarima | full | 52 | 0.073 | 20 | 32 | 21 | 0.385 | 0.512 | 0.274 | 0.430 | 0.353 | 0.273 |
| gnn_st_tuned | full | 52 | 0.073 | 18 | 34 | 6 | 0.346 | 0.250 | 0.310 | 0.474 | 0.337 | 0.354 |
| lstm_tuned | full | 52 | 0.073 | 11 | 41 | 7 | 0.212 | 0.389 | 0.186 | 0.314 | 0.201 | 0.264 |
| colagnn_tuned | full | 52 | 0.073 | 10 | 42 | 13 | 0.192 | 0.565 | 0.154 | 0.267 | 0.173 | 0.258 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.003 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.664 |
| colagnn_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.044 |
| flusight_baseline | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.682 |
| gnn_st_nograph_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.225 |
| gnn_st_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.027 |
| lstm_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.057 |
| persistence | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.080 |
| sarima | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.494 |
| xgboost_tuned | full | 2 | 0.003 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.378 |

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

### All four bands — 710 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 710 | 0.941 | 1.000 | 0.464 | -0.042 |
| gnn_st_nograph_tuned | full | 710 | 0.939 | 1.000 | 0.500 | -0.030 |
| blend_baseline | full | 710 | 0.932 | 1.000 | 0.498 | -0.017 |
| xgboost_tuned | full | 710 | 0.932 | 1.000 | 0.480 | -0.023 |
| lstm_tuned | full | 710 | 0.931 | 0.999 | 0.290 | -0.051 |
| flusight_baseline | full | 710 | 0.924 | 1.000 | 0.499 | 0.000 |
| persistence | full | 710 | 0.924 | 1.000 | 0.499 | 0.000 |
| sarima | full | 710 | 0.924 | 0.999 | 0.386 | -0.018 |
| colagnn_tuned | full | 710 | 0.923 | 0.997 | 0.213 | -0.044 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 52 | 0.138 | 27 | 25 | 25 | 0.519 | 0.481 | 0.351 | 0.519 | 0.443 | 0.197 |
| persistence | full | 52 | 0.138 | 27 | 25 | 25 | 0.519 | 0.481 | 0.351 | 0.519 | 0.443 | 0.191 |
| blend_baseline | full | 52 | 0.138 | 24 | 28 | 17 | 0.462 | 0.415 | 0.348 | 0.516 | 0.409 | 0.233 |
| gnn_st_nograph_tuned | full | 52 | 0.138 | 22 | 30 | 11 | 0.423 | 0.333 | 0.349 | 0.518 | 0.389 | 0.278 |
| xgboost_tuned | full | 52 | 0.138 | 22 | 30 | 15 | 0.423 | 0.405 | 0.328 | 0.494 | 0.377 | 0.253 |
| gnn_st_tuned | full | 52 | 0.138 | 18 | 34 | 6 | 0.346 | 0.250 | 0.310 | 0.474 | 0.328 | 0.306 |
| sarima | full | 52 | 0.138 | 20 | 32 | 21 | 0.385 | 0.512 | 0.274 | 0.430 | 0.320 | 0.228 |
| lstm_tuned | full | 52 | 0.138 | 11 | 41 | 7 | 0.212 | 0.389 | 0.186 | 0.314 | 0.190 | 0.209 |
| colagnn_tuned | full | 52 | 0.138 | 10 | 42 | 13 | 0.192 | 0.565 | 0.154 | 0.267 | 0.152 | 0.203 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.005 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.661 |
| colagnn_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.046 |
| flusight_baseline | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -0.686 |
| gnn_st_nograph_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.227 |
| gnn_st_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.024 |
| lstm_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.055 |
| persistence | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -1.071 |
| sarima | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.496 |
| xgboost_tuned | full | 2 | 0.005 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.381 |

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

### All four bands — 378 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 378 | 0.889 | 1.000 | 0.441 | -0.079 |
| gnn_st_nograph_tuned | full | 378 | 0.886 | 1.000 | 0.473 | -0.056 |
| blend_baseline | full | 378 | 0.873 | 1.000 | 0.467 | -0.032 |
| xgboost_tuned | full | 378 | 0.873 | 1.000 | 0.449 | -0.042 |
| lstm_tuned | full | 378 | 0.870 | 0.997 | 0.266 | -0.095 |
| flusight_baseline | full | 378 | 0.857 | 1.000 | 0.463 | 0.000 |
| persistence | full | 378 | 0.857 | 1.000 | 0.463 | 0.000 |
| sarima | full | 378 | 0.857 | 0.997 | 0.347 | -0.034 |
| colagnn_tuned | full | 378 | 0.854 | 0.995 | 0.180 | -0.082 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 13 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| persistence | full | 13 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| blend_baseline | full | 12 | 1.000 | -1.000 | 1.583 | 1.000 | -2.151 |
| xgboost_tuned | full | 10 | 1.000 | -1.000 | 1.800 | 1.000 | -2.856 |
| sarima | full | 11 | 1.000 | -1.000 | 2.182 | 1.000 | -2.972 |
| gnn_st_nograph_tuned | full | 9 | 1.000 | -1.000 | 2.333 | 1.000 | -4.916 |
| colagnn_tuned | full | 12 | 1.000 | -1.000 | 2.417 | 1.000 | -4.683 |
| lstm_tuned | full | 10 | 1.000 | -1.000 | 2.500 | 0.500 | -3.536 |
| gnn_st_tuned | full | 9 | 2.000 | -2.000 | 3.000 | 1.000 | -6.696 |

# Notes

- IT90 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- IT98 was crossed on only 0 neighborhood-weeks in this window, so its scores are reported but not ranked.
