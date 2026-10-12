Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 26.2, IT90 = 39.3, IT98 = 50.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 14 | 0.269 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.778 | 0.573 |
| lstm_tuned | post_covid | 14 | 0.269 | 11 | 3 | 3 | 0.786 | 0.214 | 0.647 | 0.786 | 0.707 | 0.571 |
| xgboost_tuned | post_covid | 14 | 0.269 | 10 | 4 | 1 | 0.714 | 0.091 | 0.667 | 0.800 | 0.688 | 0.570 |
| flusight_baseline | post_covid | 14 | 0.269 | 10 | 4 | 4 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.361 |
| persistence | post_covid | 14 | 0.269 | 10 | 4 | 4 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.410 |
| sarima | post_covid | 14 | 0.269 | 10 | 4 | 5 | 0.714 | 0.333 | 0.526 | 0.690 | 0.583 | 0.499 |
| colagnn_tuned | post_covid | 14 | 0.269 | 8 | 6 | 4 | 0.571 | 0.333 | 0.444 | 0.615 | 0.466 | 0.500 |
| gnn_st_nograph_tuned | post_covid | 14 | 0.269 | 6 | 8 | 1 | 0.429 | 0.143 | 0.400 | 0.571 | 0.402 | 0.547 |
| blend_baseline | post_covid | 14 | 0.269 | 4 | 10 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.528 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 7 | 0.135 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.340 | -0.090 |
| persistence | post_covid | 7 | 0.135 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.340 | -0.008 |
| blend_baseline | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.116 |
| colagnn_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.125 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.116 |
| gnn_st_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.096 |
| sarima | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.096 |
| xgboost_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.115 |
| lstm_tuned | post_covid | 7 | 0.135 | 0 | 7 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.044 | -0.108 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| flusight_baseline | post_covid | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.749 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.093 |
| persistence | post_covid | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.510 |
| sarima | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| xgboost_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 52 | 0.846 | 0.923 | 0.278 | -0.269 |
| gnn_st_tuned | post_covid | 52 | 0.808 | 0.923 | 0.424 | -0.192 |
| gnn_st_nograph_tuned | post_covid | 52 | 0.788 | 0.904 | 0.168 | -0.346 |
| blend_baseline | post_covid | 52 | 0.769 | 0.904 | 0.148 | -0.404 |
| lstm_tuned | post_covid | 52 | 0.769 | 0.904 | 0.379 | -0.173 |
| sarima | post_covid | 52 | 0.769 | 0.923 | 0.208 | -0.192 |
| colagnn_tuned | post_covid | 52 | 0.731 | 0.904 | 0.297 | -0.250 |
| flusight_baseline | post_covid | 52 | 0.712 | 0.846 | 0.488 | 0.000 |
| persistence | post_covid | 52 | 0.712 | 0.846 | 0.488 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 14 | 0.538 | 10 | 4 | 1 | 0.714 | 0.091 | 0.667 | 0.800 | 0.631 | 0.320 |
| gnn_st_tuned | post_covid | 14 | 0.538 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.607 | 0.326 |
| lstm_tuned | post_covid | 14 | 0.538 | 11 | 3 | 3 | 0.786 | 0.214 | 0.647 | 0.786 | 0.536 | 0.326 |
| flusight_baseline | post_covid | 14 | 0.538 | 10 | 4 | 3 | 0.714 | 0.231 | 0.588 | 0.741 | 0.464 | 0.188 |
| persistence | post_covid | 14 | 0.538 | 10 | 4 | 3 | 0.714 | 0.231 | 0.588 | 0.741 | 0.464 | 0.210 |
| gnn_st_nograph_tuned | post_covid | 14 | 0.538 | 6 | 8 | 1 | 0.429 | 0.143 | 0.400 | 0.571 | 0.345 | 0.284 |
| sarima | post_covid | 14 | 0.538 | 10 | 4 | 5 | 0.714 | 0.333 | 0.526 | 0.690 | 0.298 | 0.218 |
| blend_baseline | post_covid | 14 | 0.538 | 4 | 10 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.253 |
| colagnn_tuned | post_covid | 14 | 0.538 | 8 | 6 | 4 | 0.571 | 0.333 | 0.444 | 0.615 | 0.238 | 0.217 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 7 | 0.269 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.218 | -0.263 |
| persistence | post_covid | 7 | 0.269 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.218 | -0.174 |
| blend_baseline | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.322 |
| colagnn_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.332 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.321 |
| gnn_st_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.298 |
| sarima | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.298 |
| xgboost_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.321 |
| lstm_tuned | post_covid | 7 | 0.269 | 0 | 7 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.105 | -0.312 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| flusight_baseline | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.905 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.193 |
| persistence | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.645 |
| sarima | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| xgboost_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 26 | 0.692 | 0.846 | 0.108 | -0.538 |
| gnn_st_tuned | post_covid | 26 | 0.615 | 0.846 | 0.222 | -0.385 |
| gnn_st_nograph_tuned | post_covid | 26 | 0.577 | 0.808 | 0.052 | -0.692 |
| blend_baseline | post_covid | 26 | 0.538 | 0.808 | 0.084 | -0.808 |
| lstm_tuned | post_covid | 26 | 0.538 | 0.808 | 0.163 | -0.346 |
| sarima | post_covid | 26 | 0.538 | 0.846 | -0.069 | -0.385 |
| colagnn_tuned | post_covid | 26 | 0.462 | 0.808 | 0.112 | -0.500 |
| flusight_baseline | post_covid | 26 | 0.462 | 0.692 | 0.316 | -0.038 |
| persistence | post_covid | 26 | 0.462 | 0.692 | 0.316 | -0.038 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 248 | 0.281 | 146 | 102 | 101 | 0.589 | 0.409 | 0.418 | 0.590 | 0.430 | 0.142 |
| persistence | post_covid | 248 | 0.281 | 146 | 102 | 101 | 0.589 | 0.409 | 0.418 | 0.590 | 0.430 | 0.171 |
| lstm_tuned | post_covid | 248 | 0.281 | 127 | 121 | 61 | 0.512 | 0.324 | 0.411 | 0.583 | 0.416 | 0.293 |
| gnn_st_tuned | post_covid | 248 | 0.281 | 107 | 141 | 54 | 0.431 | 0.335 | 0.354 | 0.523 | 0.347 | 0.335 |
| xgboost_tuned | post_covid | 248 | 0.281 | 96 | 152 | 35 | 0.387 | 0.267 | 0.339 | 0.507 | 0.332 | 0.325 |
| sarima | post_covid | 248 | 0.281 | 109 | 139 | 86 | 0.440 | 0.441 | 0.326 | 0.492 | 0.304 | 0.249 |
| gnn_st_nograph_tuned | post_covid | 248 | 0.281 | 71 | 177 | 27 | 0.286 | 0.276 | 0.258 | 0.410 | 0.244 | 0.309 |
| blend_baseline | post_covid | 248 | 0.281 | 55 | 193 | 21 | 0.222 | 0.276 | 0.204 | 0.340 | 0.189 | 0.286 |
| colagnn_tuned | post_covid | 248 | 0.281 | 47 | 201 | 40 | 0.190 | 0.460 | 0.163 | 0.281 | 0.127 | 0.297 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.121 | 37 | 70 | 70 | 0.346 | 0.654 | 0.209 | 0.346 | 0.256 | -0.194 |
| persistence | post_covid | 107 | 0.121 | 37 | 70 | 70 | 0.346 | 0.654 | 0.209 | 0.346 | 0.256 | -0.089 |
| lstm_tuned | post_covid | 107 | 0.121 | 5 | 102 | 18 | 0.047 | 0.783 | 0.040 | 0.077 | 0.024 | -0.043 |
| gnn_st_tuned | post_covid | 107 | 0.121 | 2 | 105 | 2 | 0.019 | 0.500 | 0.018 | 0.036 | 0.016 | -0.041 |
| xgboost_tuned | post_covid | 107 | 0.121 | 1 | 106 | 0 | 0.009 | 0.000 | 0.009 | 0.019 | 0.009 | -0.043 |
| blend_baseline | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.053 |
| colagnn_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.081 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.056 |
| sarima | post_covid | 107 | 0.121 | 0 | 107 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.099 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 64 | 0.072 | 8 | 56 | 56 | 0.125 | 0.875 | 0.067 | 0.125 | 0.057 | -0.571 |
| persistence | post_covid | 64 | 0.072 | 8 | 56 | 56 | 0.125 | 0.875 | 0.067 | 0.125 | 0.057 | -0.366 |
| blend_baseline | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.064 |
| colagnn_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.071 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.066 |
| gnn_st_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.070 |
| sarima | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.064 |
| xgboost_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.058 |
| lstm_tuned | post_covid | 64 | 0.072 | 0 | 64 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.084 |

### All four bands — 884 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 884 | 0.745 | 0.900 | 0.210 | -0.325 |
| gnn_st_nograph_tuned | post_covid | 884 | 0.735 | 0.898 | 0.151 | -0.363 |
| blend_baseline | post_covid | 884 | 0.733 | 0.893 | 0.114 | -0.388 |
| gnn_st_tuned | post_covid | 884 | 0.729 | 0.905 | 0.225 | -0.287 |
| lstm_tuned | post_covid | 884 | 0.717 | 0.906 | 0.294 | -0.233 |
| colagnn_tuned | post_covid | 884 | 0.708 | 0.891 | 0.064 | -0.376 |
| sarima | post_covid | 884 | 0.699 | 0.902 | 0.164 | -0.250 |
| flusight_baseline | post_covid | 884 | 0.661 | 0.869 | 0.389 | -0.001 |
| persistence | post_covid | 884 | 0.661 | 0.869 | 0.389 | -0.001 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm_tuned | post_covid | 234 | 0.529 | 127 | 107 | 59 | 0.543 | 0.317 | 0.433 | 0.605 | 0.259 | -0.010 |
| xgboost_tuned | post_covid | 234 | 0.529 | 96 | 138 | 35 | 0.410 | 0.267 | 0.357 | 0.526 | 0.242 | 0.033 |
| flusight_baseline | post_covid | 234 | 0.529 | 145 | 89 | 82 | 0.620 | 0.361 | 0.459 | 0.629 | 0.225 | -0.081 |
| persistence | post_covid | 234 | 0.529 | 145 | 89 | 82 | 0.620 | 0.361 | 0.459 | 0.629 | 0.225 | -0.063 |
| gnn_st_tuned | post_covid | 234 | 0.529 | 107 | 127 | 54 | 0.457 | 0.335 | 0.372 | 0.542 | 0.198 | 0.045 |
| gnn_st_nograph_tuned | post_covid | 234 | 0.529 | 71 | 163 | 27 | 0.303 | 0.276 | 0.272 | 0.428 | 0.174 | 0.002 |
| blend_baseline | post_covid | 234 | 0.529 | 55 | 179 | 21 | 0.235 | 0.276 | 0.216 | 0.355 | 0.134 | -0.036 |
| sarima | post_covid | 234 | 0.529 | 108 | 126 | 72 | 0.462 | 0.400 | 0.353 | 0.522 | 0.115 | -0.022 |
| colagnn_tuned | post_covid | 234 | 0.529 | 47 | 187 | 40 | 0.201 | 0.460 | 0.172 | 0.293 | 0.009 | -0.013 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.242 | 37 | 70 | 67 | 0.346 | 0.644 | 0.213 | 0.351 | 0.146 | -0.338 |
| persistence | post_covid | 107 | 0.242 | 37 | 70 | 67 | 0.346 | 0.644 | 0.213 | 0.351 | 0.146 | -0.209 |
| gnn_st_tuned | post_covid | 107 | 0.242 | 2 | 105 | 2 | 0.019 | 0.500 | 0.018 | 0.036 | 0.013 | -0.207 |
| xgboost_tuned | post_covid | 107 | 0.242 | 1 | 106 | 0 | 0.009 | 0.000 | 0.009 | 0.019 | 0.009 | -0.208 |
| blend_baseline | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.221 |
| colagnn_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.254 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.225 |
| lstm_tuned | post_covid | 107 | 0.242 | 5 | 102 | 18 | 0.047 | 0.783 | 0.040 | 0.077 | -0.007 | -0.209 |
| sarima | post_covid | 107 | 0.242 | 0 | 107 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -0.256 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.154 |
| colagnn_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.162 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.156 |
| gnn_st_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.161 |
| sarima | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.152 |
| xgboost_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.147 |
| lstm_tuned | post_covid | 64 | 0.145 | 0 | 64 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -0.176 |
| flusight_baseline | post_covid | 64 | 0.145 | 8 | 56 | 56 | 0.125 | 0.875 | 0.067 | 0.125 | -0.023 | -0.694 |
| persistence | post_covid | 64 | 0.145 | 8 | 56 | 56 | 0.125 | 0.875 | 0.067 | 0.125 | -0.023 | -0.463 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | post_covid | 442 | 0.523 | 0.801 | 0.094 | -0.618 |
| gnn_st_nograph_tuned | post_covid | 442 | 0.502 | 0.796 | 0.061 | -0.695 |
| blend_baseline | post_covid | 442 | 0.498 | 0.785 | 0.043 | -0.744 |
| gnn_st_tuned | post_covid | 442 | 0.489 | 0.810 | 0.077 | -0.543 |
| lstm_tuned | post_covid | 442 | 0.471 | 0.812 | 0.127 | -0.439 |
| sarima | post_covid | 442 | 0.459 | 0.803 | -0.002 | -0.502 |
| colagnn_tuned | post_covid | 442 | 0.448 | 0.783 | -0.024 | -0.719 |
| flusight_baseline | post_covid | 442 | 0.394 | 0.744 | 0.206 | -0.023 |
| persistence | post_covid | 442 | 0.394 | 0.744 | 0.206 | -0.023 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 18 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| persistence | post_covid | 18 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| sarima | post_covid | 17 | 4.000 | -4.000 | 6.000 | -0.500 | -9.341 |
| lstm_tuned | post_covid | 17 | 5.000 | -5.000 | 7.235 | 4.000 | -6.035 |
| xgboost_tuned | post_covid | 17 | 7.000 | -7.000 | 8.765 | -2.500 | -9.833 |
| gnn_st_tuned | post_covid | 17 | 9.000 | -9.000 | 9.059 | 4.000 | -8.310 |
| colagnn_tuned | post_covid | 15 | 8.000 | -8.000 | 9.267 | -6.500 | -8.830 |
| gnn_st_nograph_tuned | post_covid | 16 | 11.500 | -11.500 | 11.562 | 1.000 | -9.469 |
| blend_baseline | post_covid | 16 | 11.500 | -11.500 | 12.188 | 3.000 | -10.308 |

# Notes

- 12 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
