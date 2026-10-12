Severity thresholds from the 3 reference seasons 2017-18, 2018-19, 2022-23, fitted on weeks before 2023-06-01, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 58.4, IT90 = 94.5, IT98 = 128.6 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.934 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.605 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -1.714 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.622 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.799 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.670 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -1.991 |
| sarima | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.785 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.044 |

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
| colagnn_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| gnn_st_nograph_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| gnn_st_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| lstm_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| sarima | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| xgboost_tuned | full | 52 | 0.981 | 1.000 | 0.000 | -0.019 |
| flusight_baseline | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |
| persistence | full | 52 | 0.962 | 1.000 | -0.020 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.898 |
| colagnn_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.630 |
| flusight_baseline | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -1.581 |
| gnn_st_nograph_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.639 |
| gnn_st_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.824 |
| lstm_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.694 |
| persistence | full | 1 | 0.037 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -1.865 |
| sarima | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.795 |
| xgboost_tuned | full | 1 | 0.037 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.052 |

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
| colagnn_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| gnn_st_nograph_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| gnn_st_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| lstm_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| sarima | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| xgboost_tuned | full | 27 | 0.963 | 1.000 | 0.000 | -0.037 |
| flusight_baseline | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |
| persistence | full | 27 | 0.926 | 1.000 | -0.038 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 52 | 0.073 | 15 | 37 | 37 | 0.288 | 0.712 | 0.169 | 0.288 | 0.232 | -0.191 |
| persistence | full | 52 | 0.073 | 15 | 37 | 37 | 0.288 | 0.712 | 0.169 | 0.288 | 0.232 | -0.208 |
| xgboost_tuned | full | 52 | 0.073 | 12 | 40 | 17 | 0.231 | 0.586 | 0.174 | 0.296 | 0.205 | 0.039 |
| lstm_tuned | full | 52 | 0.073 | 7 | 45 | 6 | 0.135 | 0.462 | 0.121 | 0.215 | 0.125 | 0.123 |
| gnn_st_nograph_tuned | full | 52 | 0.073 | 4 | 48 | 3 | 0.077 | 0.429 | 0.073 | 0.136 | 0.072 | 0.134 |
| gnn_st_tuned | full | 52 | 0.073 | 4 | 48 | 3 | 0.077 | 0.429 | 0.073 | 0.136 | 0.072 | 0.133 |
| colagnn_tuned | full | 52 | 0.073 | 3 | 49 | 2 | 0.058 | 0.400 | 0.056 | 0.105 | 0.055 | 0.147 |
| blend_baseline | full | 52 | 0.073 | 2 | 50 | 4 | 0.038 | 0.667 | 0.036 | 0.069 | 0.032 | 0.044 |
| sarima | full | 52 | 0.073 | 0 | 52 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.109 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.236 |
| colagnn_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.657 |
| flusight_baseline | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.992 |
| gnn_st_nograph_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.610 |
| gnn_st_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.663 |
| lstm_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.599 |
| persistence | full | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -3.550 |
| sarima | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.801 |
| xgboost_tuned | full | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -2.458 |

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
| colagnn_tuned | full | 710 | 0.928 | 0.997 | 0.084 | -0.069 |
| gnn_st_nograph_tuned | full | 710 | 0.928 | 0.997 | 0.108 | -0.066 |
| gnn_st_tuned | full | 710 | 0.928 | 0.997 | 0.108 | -0.066 |
| lstm_tuned | full | 710 | 0.928 | 0.997 | 0.174 | -0.058 |
| sarima | full | 710 | 0.927 | 0.997 | 0.000 | -0.076 |
| blend_baseline | full | 710 | 0.924 | 0.997 | 0.049 | -0.068 |
| xgboost_tuned | full | 710 | 0.920 | 0.997 | 0.237 | -0.035 |
| flusight_baseline | full | 710 | 0.893 | 0.997 | 0.239 | 0.000 |
| persistence | full | 710 | 0.893 | 0.997 | 0.239 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 52 | 0.138 | 15 | 37 | 35 | 0.288 | 0.700 | 0.172 | 0.294 | 0.181 | -0.177 |
| persistence | full | 52 | 0.138 | 15 | 37 | 35 | 0.288 | 0.700 | 0.172 | 0.294 | 0.181 | -0.147 |
| xgboost_tuned | full | 52 | 0.138 | 12 | 40 | 17 | 0.231 | 0.586 | 0.174 | 0.296 | 0.179 | 0.025 |
| lstm_tuned | full | 52 | 0.138 | 7 | 45 | 6 | 0.135 | 0.462 | 0.121 | 0.215 | 0.116 | 0.085 |
| gnn_st_nograph_tuned | full | 52 | 0.138 | 4 | 48 | 3 | 0.077 | 0.429 | 0.073 | 0.136 | 0.068 | 0.115 |
| gnn_st_tuned | full | 52 | 0.138 | 4 | 48 | 3 | 0.077 | 0.429 | 0.073 | 0.136 | 0.068 | 0.098 |
| colagnn_tuned | full | 52 | 0.138 | 3 | 49 | 2 | 0.058 | 0.400 | 0.056 | 0.105 | 0.052 | 0.111 |
| blend_baseline | full | 52 | 0.138 | 2 | 50 | 4 | 0.038 | 0.667 | 0.036 | 0.069 | 0.026 | 0.052 |
| sarima | full | 52 | 0.138 | 0 | 52 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.082 |

### Crossing IT90 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.111 |
| colagnn_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.654 |
| flusight_baseline | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -0.966 |
| gnn_st_nograph_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.583 |
| gnn_st_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.653 |
| lstm_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.596 |
| persistence | full | 2 | 0.005 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.173 |
| sarima | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.781 |
| xgboost_tuned | full | 2 | 0.005 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -2.394 |

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
| colagnn_tuned | full | 378 | 0.865 | 0.995 | 0.074 | -0.130 |
| gnn_st_nograph_tuned | full | 378 | 0.865 | 0.995 | 0.095 | -0.124 |
| gnn_st_tuned | full | 378 | 0.865 | 0.995 | 0.095 | -0.124 |
| lstm_tuned | full | 378 | 0.865 | 0.995 | 0.153 | -0.108 |
| sarima | full | 378 | 0.862 | 0.995 | 0.000 | -0.143 |
| blend_baseline | full | 378 | 0.857 | 0.995 | 0.037 | -0.127 |
| xgboost_tuned | full | 378 | 0.849 | 0.995 | 0.200 | -0.066 |
| flusight_baseline | full | 378 | 0.804 | 0.995 | 0.193 | -0.005 |
| persistence | full | 378 | 0.804 | 0.995 | 0.193 | -0.005 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | full | 9 | 3.000 | -3.000 | 3.333 | 2.000 | -4.494 |
| lstm_tuned | full | 8 | 4.000 | -4.000 | 3.875 | 3.500 | -0.751 |
| flusight_baseline | full | 13 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| persistence | full | 13 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| blend_baseline | full | 3 | 6.000 | -6.000 | 7.000 | 4.000 | -11.695 |
| colagnn_tuned | full | 2 | 7.000 | -7.000 | 7.000 | 4.000 | -7.989 |
| gnn_st_nograph_tuned | full | 3 | 6.000 | -6.000 | 7.000 | 1.500 | -6.176 |
| gnn_st_tuned | full | 3 | 8.000 | -8.000 | 7.000 | 3.000 | -8.844 |
| sarima | full | 0 |  |  |  | 2.500 | -14.157 |

# Notes

- 4 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT90 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
- IT98 was crossed on only 0 neighborhood-weeks in this window, so its scores are reported but not ranked.
