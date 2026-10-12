Severity thresholds from the 3 reference seasons 2017-18, 2018-19, 2022-23, fitted on weeks before 2023-06-01, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 58.4, IT90 = 94.5, IT98 = 128.6 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.810 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.451 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -1.079 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.583 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.603 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.537 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -1.286 |
| sarima | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.648 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.807 |

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
| blend_baseline | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| gnn_st_nograph_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| gnn_st_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| sarima | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| xgboost_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| colagnn_tuned | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| flusight_baseline | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| lstm_tuned | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| persistence | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.835 |
| colagnn_tuned | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.477 |
| flusight_baseline | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -1.100 |
| gnn_st_nograph_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.612 |
| gnn_st_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.630 |
| lstm_tuned | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.565 |
| persistence | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -1.306 |
| sarima | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.675 |
| xgboost_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.838 |

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
| blend_baseline | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| gnn_st_nograph_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| gnn_st_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| sarima | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| xgboost_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| colagnn_tuned | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| flusight_baseline | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| lstm_tuned | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| persistence | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 52 | 0.073 | 21 | 31 | 31 | 0.404 | 0.596 | 0.253 | 0.404 | 0.357 | 0.026 |
| persistence | full | 52 | 0.073 | 21 | 31 | 31 | 0.404 | 0.596 | 0.253 | 0.404 | 0.357 | 0.018 |
| xgboost_tuned | full | 52 | 0.073 | 19 | 33 | 17 | 0.365 | 0.472 | 0.275 | 0.432 | 0.340 | 0.163 |
| blend_baseline | full | 52 | 0.073 | 17 | 35 | 15 | 0.327 | 0.469 | 0.254 | 0.405 | 0.304 | 0.120 |
| gnn_st_tuned | full | 52 | 0.073 | 15 | 37 | 10 | 0.288 | 0.400 | 0.242 | 0.390 | 0.273 | 0.224 |
| lstm_tuned | full | 52 | 0.073 | 15 | 37 | 14 | 0.288 | 0.483 | 0.227 | 0.370 | 0.267 | 0.168 |
| sarima | full | 52 | 0.073 | 14 | 38 | 18 | 0.269 | 0.562 | 0.200 | 0.333 | 0.242 | 0.156 |
| gnn_st_nograph_tuned | full | 52 | 0.073 | 13 | 39 | 9 | 0.250 | 0.409 | 0.213 | 0.351 | 0.236 | 0.193 |
| colagnn_tuned | full | 52 | 0.073 | 5 | 47 | 10 | 0.096 | 0.667 | 0.081 | 0.149 | 0.081 | 0.161 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.003 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.703 |
| colagnn_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.163 |
| flusight_baseline | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.513 |
| gnn_st_nograph_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.215 |
| gnn_st_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.067 |
| lstm_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.529 |
| persistence | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -1.613 |
| sarima | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.641 |
| xgboost_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.996 |

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
| gnn_st_nograph_tuned | full | 710 | 0.931 | 0.999 | 0.322 | -0.045 |
| gnn_st_tuned | full | 710 | 0.931 | 1.000 | 0.381 | -0.041 |
| blend_baseline | full | 710 | 0.928 | 0.997 | 0.352 | -0.030 |
| xgboost_tuned | full | 710 | 0.928 | 0.999 | 0.390 | -0.025 |
| lstm_tuned | full | 710 | 0.927 | 0.999 | 0.334 | -0.035 |
| colagnn_tuned | full | 710 | 0.920 | 0.997 | 0.109 | -0.055 |
| sarima | full | 710 | 0.920 | 0.999 | 0.295 | -0.031 |
| flusight_baseline | full | 710 | 0.908 | 0.999 | 0.369 | 0.000 |
| persistence | full | 710 | 0.908 | 0.999 | 0.369 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | full | 52 | 0.138 | 19 | 33 | 17 | 0.365 | 0.472 | 0.275 | 0.432 | 0.313 | 0.116 |
| flusight_baseline | full | 52 | 0.138 | 21 | 31 | 31 | 0.404 | 0.596 | 0.253 | 0.404 | 0.309 | -0.016 |
| persistence | full | 52 | 0.138 | 21 | 31 | 31 | 0.404 | 0.596 | 0.253 | 0.404 | 0.309 | 0.002 |
| blend_baseline | full | 52 | 0.138 | 17 | 35 | 15 | 0.327 | 0.469 | 0.254 | 0.405 | 0.281 | 0.089 |
| gnn_st_tuned | full | 52 | 0.138 | 15 | 37 | 10 | 0.288 | 0.400 | 0.242 | 0.390 | 0.258 | 0.174 |
| lstm_tuned | full | 52 | 0.138 | 15 | 37 | 14 | 0.288 | 0.483 | 0.227 | 0.370 | 0.246 | 0.120 |
| gnn_st_nograph_tuned | full | 52 | 0.138 | 13 | 39 | 9 | 0.250 | 0.409 | 0.213 | 0.351 | 0.222 | 0.147 |
| sarima | full | 52 | 0.138 | 14 | 38 | 18 | 0.269 | 0.562 | 0.200 | 0.333 | 0.214 | 0.112 |
| colagnn_tuned | full | 52 | 0.138 | 5 | 47 | 10 | 0.096 | 0.667 | 0.081 | 0.149 | 0.065 | 0.104 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.005 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.685 |
| colagnn_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.166 |
| flusight_baseline | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -0.516 |
| gnn_st_nograph_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.215 |
| gnn_st_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.069 |
| lstm_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.530 |
| persistence | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -1.563 |
| sarima | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.641 |
| xgboost_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.998 |

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
| gnn_st_nograph_tuned | full | 378 | 0.870 | 0.997 | 0.295 | -0.085 |
| gnn_st_tuned | full | 378 | 0.870 | 1.000 | 0.354 | -0.077 |
| blend_baseline | full | 378 | 0.865 | 0.995 | 0.318 | -0.056 |
| xgboost_tuned | full | 378 | 0.865 | 0.997 | 0.355 | -0.048 |
| lstm_tuned | full | 378 | 0.862 | 0.997 | 0.301 | -0.066 |
| colagnn_tuned | full | 378 | 0.849 | 0.995 | 0.083 | -0.103 |
| sarima | full | 378 | 0.849 | 0.997 | 0.258 | -0.058 |
| flusight_baseline | full | 378 | 0.828 | 0.997 | 0.324 | 0.000 |
| persistence | full | 378 | 0.828 | 0.997 | 0.324 | 0.000 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 13 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | full | 13 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| xgboost_tuned | full | 10 | 2.000 | -2.000 | 2.400 | 1.500 | -3.457 |
| lstm_tuned | full | 12 | 2.000 | -2.000 | 2.667 | 2.000 | -0.287 |
| colagnn_tuned | full | 7 | 2.000 | -2.000 | 2.714 | 1.000 | -5.777 |
| blend_baseline | full | 10 | 2.000 | -2.000 | 2.800 | 2.000 | -4.055 |
| sarima | full | 10 | 2.000 | -2.000 | 3.200 | 2.000 | -4.108 |
| gnn_st_nograph_tuned | full | 9 | 3.000 | -3.000 | 3.444 | 2.000 | -5.247 |
| gnn_st_tuned | full | 10 | 2.500 | -2.500 | 3.600 | 2.000 | -7.529 |

# Notes

- IT90 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- IT98 was crossed on only 0 neighborhood-weeks in this window, so its scores are reported but not ranked.
