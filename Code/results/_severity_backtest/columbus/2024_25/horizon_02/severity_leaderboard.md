Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 26.2, IT90 = 39.3, IT98 = 50.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 14 | 0.269 | 14 | 0 | 2 | 1.000 | 0.125 | 0.875 | 0.933 | 0.947 | 0.724 |
| gnn_st_nograph_tuned | post_covid | 14 | 0.269 | 13 | 1 | 0 | 0.929 | 0.000 | 0.929 | 0.963 | 0.929 | 0.744 |
| sarima | post_covid | 14 | 0.269 | 14 | 0 | 3 | 1.000 | 0.176 | 0.824 | 0.903 | 0.921 | 0.708 |
| xgboost_tuned | post_covid | 14 | 0.269 | 12 | 2 | 0 | 0.857 | 0.000 | 0.857 | 0.923 | 0.857 | 0.744 |
| flusight_baseline | post_covid | 14 | 0.269 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.636 |
| persistence | post_covid | 14 | 0.269 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.627 |
| blend_baseline | post_covid | 14 | 0.269 | 9 | 5 | 0 | 0.643 | 0.000 | 0.643 | 0.783 | 0.643 | 0.693 |
| lstm_tuned | post_covid | 14 | 0.269 | 7 | 7 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.509 |
| colagnn_tuned | post_covid | 14 | 0.269 | 7 | 7 | 2 | 0.500 | 0.222 | 0.438 | 0.609 | 0.447 | 0.553 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 7 | 0.135 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.505 | 0.264 |
| persistence | post_covid | 7 | 0.135 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.505 | 0.343 |
| gnn_st_tuned | post_covid | 7 | 0.135 | 3 | 4 | 1 | 0.429 | 0.250 | 0.375 | 0.545 | 0.406 | 0.359 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.135 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.259 |
| xgboost_tuned | post_covid | 7 | 0.135 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.256 |
| blend_baseline | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.065 |
| colagnn_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.030 |
| lstm_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| sarima | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.143 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.073 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.081 |
| flusight_baseline | post_covid | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.055 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.000 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.229 | 0.114 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.080 |
| persistence | post_covid | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.196 |
| sarima | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.071 |
| xgboost_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.004 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 52 | 0.885 | 0.923 | 0.698 | -0.192 |
| xgboost_tuned | post_covid | 52 | 0.865 | 0.923 | 0.681 | -0.212 |
| blend_baseline | post_covid | 52 | 0.827 | 0.885 | 0.422 | -0.308 |
| gnn_st_tuned | post_covid | 52 | 0.827 | 0.962 | 0.791 | -0.058 |
| sarima | post_covid | 52 | 0.808 | 0.923 | 0.605 | -0.154 |
| flusight_baseline | post_covid | 52 | 0.788 | 0.942 | 0.767 | 0.000 |
| lstm_tuned | post_covid | 52 | 0.788 | 0.885 | 0.385 | -0.346 |
| persistence | post_covid | 52 | 0.788 | 0.942 | 0.767 | 0.000 |
| colagnn_tuned | post_covid | 52 | 0.731 | 0.885 | 0.422 | -0.308 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 14 | 0.538 | 13 | 1 | 0 | 0.929 | 0.000 | 0.929 | 0.963 | 0.929 | 0.595 |
| xgboost_tuned | post_covid | 14 | 0.538 | 12 | 2 | 0 | 0.857 | 0.000 | 0.857 | 0.923 | 0.857 | 0.595 |
| gnn_st_tuned | post_covid | 14 | 0.538 | 14 | 0 | 2 | 1.000 | 0.125 | 0.875 | 0.933 | 0.833 | 0.575 |
| sarima | post_covid | 14 | 0.538 | 14 | 0 | 3 | 1.000 | 0.176 | 0.824 | 0.903 | 0.750 | 0.539 |
| flusight_baseline | post_covid | 14 | 0.538 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.690 | 0.511 |
| persistence | post_covid | 14 | 0.538 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.690 | 0.489 |
| blend_baseline | post_covid | 14 | 0.538 | 9 | 5 | 0 | 0.643 | 0.000 | 0.643 | 0.783 | 0.643 | 0.514 |
| lstm_tuned | post_covid | 14 | 0.538 | 7 | 7 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.238 |
| colagnn_tuned | post_covid | 14 | 0.538 | 7 | 7 | 2 | 0.500 | 0.222 | 0.438 | 0.609 | 0.333 | 0.296 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 7 | 0.269 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.414 | 0.130 |
| persistence | post_covid | 7 | 0.269 | 4 | 3 | 3 | 0.571 | 0.429 | 0.400 | 0.571 | 0.414 | 0.224 |
| gnn_st_tuned | post_covid | 7 | 0.269 | 3 | 4 | 1 | 0.429 | 0.250 | 0.375 | 0.545 | 0.376 | 0.241 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.269 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.123 |
| xgboost_tuned | post_covid | 7 | 0.269 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.119 |
| blend_baseline | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.107 |
| colagnn_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.220 |
| lstm_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.208 |
| sarima | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.171 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.180 |
| flusight_baseline | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | -0.030 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.090 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 1 | 3 | 1 | 0.250 | 0.500 | 0.200 | 0.333 | 0.205 | 0.033 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.178 |
| persistence | post_covid | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.123 |
| sarima | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.169 |
| xgboost_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.086 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 26 | 0.769 | 0.846 | 0.601 | -0.385 |
| xgboost_tuned | post_covid | 26 | 0.731 | 0.846 | 0.588 | -0.423 |
| blend_baseline | post_covid | 26 | 0.654 | 0.769 | 0.315 | -0.615 |
| gnn_st_tuned | post_covid | 26 | 0.654 | 0.923 | 0.704 | -0.115 |
| sarima | post_covid | 26 | 0.615 | 0.846 | 0.440 | -0.308 |
| flusight_baseline | post_covid | 26 | 0.577 | 0.885 | 0.677 | 0.000 |
| lstm_tuned | post_covid | 26 | 0.577 | 0.769 | 0.300 | -0.692 |
| persistence | post_covid | 26 | 0.577 | 0.885 | 0.677 | 0.000 |
| colagnn_tuned | post_covid | 26 | 0.462 | 0.769 | 0.315 | -0.615 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 248 | 0.281 | 180 | 68 | 46 | 0.726 | 0.204 | 0.612 | 0.759 | 0.653 | 0.511 |
| flusight_baseline | post_covid | 248 | 0.281 | 172 | 76 | 75 | 0.694 | 0.304 | 0.533 | 0.695 | 0.576 | 0.358 |
| persistence | post_covid | 248 | 0.281 | 172 | 76 | 75 | 0.694 | 0.304 | 0.533 | 0.695 | 0.576 | 0.371 |
| xgboost_tuned | post_covid | 248 | 0.281 | 153 | 95 | 38 | 0.617 | 0.199 | 0.535 | 0.697 | 0.557 | 0.477 |
| gnn_st_nograph_tuned | post_covid | 248 | 0.281 | 145 | 103 | 30 | 0.585 | 0.171 | 0.522 | 0.686 | 0.538 | 0.475 |
| sarima | post_covid | 248 | 0.281 | 146 | 102 | 58 | 0.589 | 0.284 | 0.477 | 0.646 | 0.498 | 0.399 |
| blend_baseline | post_covid | 248 | 0.281 | 114 | 134 | 20 | 0.460 | 0.149 | 0.425 | 0.597 | 0.428 | 0.430 |
| colagnn_tuned | post_covid | 248 | 0.281 | 96 | 152 | 31 | 0.387 | 0.244 | 0.344 | 0.512 | 0.338 | 0.365 |
| lstm_tuned | post_covid | 248 | 0.281 | 84 | 164 | 11 | 0.339 | 0.116 | 0.324 | 0.490 | 0.321 | 0.355 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.121 | 62 | 45 | 45 | 0.579 | 0.421 | 0.408 | 0.579 | 0.522 | 0.216 |
| persistence | post_covid | 107 | 0.121 | 62 | 45 | 45 | 0.579 | 0.421 | 0.408 | 0.579 | 0.522 | 0.260 |
| gnn_st_tuned | post_covid | 107 | 0.121 | 41 | 66 | 18 | 0.383 | 0.305 | 0.328 | 0.494 | 0.360 | 0.299 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.121 | 15 | 92 | 8 | 0.140 | 0.348 | 0.130 | 0.231 | 0.130 | 0.200 |
| xgboost_tuned | post_covid | 107 | 0.121 | 11 | 96 | 6 | 0.103 | 0.353 | 0.097 | 0.177 | 0.095 | 0.207 |
| sarima | post_covid | 107 | 0.121 | 11 | 96 | 9 | 0.103 | 0.450 | 0.095 | 0.173 | 0.091 | 0.103 |
| blend_baseline | post_covid | 107 | 0.121 | 3 | 104 | 1 | 0.028 | 0.250 | 0.028 | 0.054 | 0.027 | 0.062 |
| colagnn_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |
| lstm_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.013 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 64 | 0.072 | 31 | 33 | 33 | 0.484 | 0.516 | 0.320 | 0.484 | 0.444 | 0.053 |
| persistence | post_covid | 64 | 0.072 | 31 | 33 | 33 | 0.484 | 0.516 | 0.320 | 0.484 | 0.444 | 0.158 |
| gnn_st_tuned | post_covid | 64 | 0.072 | 9 | 55 | 9 | 0.141 | 0.500 | 0.123 | 0.220 | 0.130 | 0.140 |
| sarima | post_covid | 64 | 0.072 | 2 | 62 | 3 | 0.031 | 0.600 | 0.030 | 0.058 | 0.028 | -0.021 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.072 | 1 | 63 | 1 | 0.016 | 0.500 | 0.015 | 0.030 | 0.014 | 0.033 |
| xgboost_tuned | post_covid | 64 | 0.072 | 1 | 63 | 1 | 0.016 | 0.500 | 0.015 | 0.030 | 0.014 | 0.037 |
| blend_baseline | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.024 |
| colagnn_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.058 |
| lstm_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.058 |

### All four bands — 884 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 884 | 0.765 | 0.946 | 0.651 | -0.131 |
| gnn_st_nograph_tuned | post_covid | 884 | 0.753 | 0.923 | 0.500 | -0.248 |
| xgboost_tuned | post_covid | 884 | 0.752 | 0.923 | 0.487 | -0.236 |
| blend_baseline | post_covid | 884 | 0.751 | 0.907 | 0.368 | -0.318 |
| lstm_tuned | post_covid | 884 | 0.740 | 0.898 | 0.295 | -0.367 |
| flusight_baseline | post_covid | 884 | 0.733 | 0.933 | 0.657 | -0.001 |
| persistence | post_covid | 884 | 0.733 | 0.933 | 0.657 | -0.001 |
| sarima | post_covid | 884 | 0.733 | 0.919 | 0.415 | -0.215 |
| colagnn_tuned | post_covid | 884 | 0.721 | 0.902 | 0.321 | -0.330 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 234 | 0.529 | 180 | 54 | 46 | 0.769 | 0.204 | 0.643 | 0.783 | 0.548 | 0.337 |
| gnn_st_nograph_tuned | post_covid | 234 | 0.529 | 145 | 89 | 30 | 0.620 | 0.171 | 0.549 | 0.709 | 0.475 | 0.271 |
| xgboost_tuned | post_covid | 234 | 0.529 | 153 | 81 | 38 | 0.654 | 0.199 | 0.562 | 0.720 | 0.471 | 0.278 |
| flusight_baseline | post_covid | 234 | 0.529 | 171 | 63 | 61 | 0.731 | 0.263 | 0.580 | 0.734 | 0.437 | 0.189 |
| persistence | post_covid | 234 | 0.529 | 171 | 63 | 61 | 0.731 | 0.263 | 0.580 | 0.734 | 0.437 | 0.218 |
| blend_baseline | post_covid | 234 | 0.529 | 114 | 120 | 20 | 0.487 | 0.149 | 0.449 | 0.620 | 0.391 | 0.198 |
| sarima | post_covid | 234 | 0.529 | 146 | 88 | 54 | 0.624 | 0.270 | 0.507 | 0.673 | 0.364 | 0.176 |
| lstm_tuned | post_covid | 234 | 0.529 | 84 | 150 | 11 | 0.359 | 0.116 | 0.343 | 0.511 | 0.306 | 0.085 |
| colagnn_tuned | post_covid | 234 | 0.529 | 96 | 138 | 31 | 0.410 | 0.244 | 0.362 | 0.532 | 0.261 | 0.092 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.242 | 62 | 45 | 45 | 0.579 | 0.421 | 0.408 | 0.579 | 0.445 | 0.103 |
| persistence | post_covid | 107 | 0.242 | 62 | 45 | 45 | 0.579 | 0.421 | 0.408 | 0.579 | 0.445 | 0.174 |
| gnn_st_tuned | post_covid | 107 | 0.242 | 41 | 66 | 18 | 0.383 | 0.305 | 0.328 | 0.494 | 0.329 | 0.187 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.242 | 15 | 92 | 8 | 0.140 | 0.348 | 0.130 | 0.231 | 0.116 | 0.073 |
| xgboost_tuned | post_covid | 107 | 0.242 | 11 | 96 | 6 | 0.103 | 0.353 | 0.097 | 0.177 | 0.085 | 0.081 |
| sarima | post_covid | 107 | 0.242 | 11 | 96 | 9 | 0.103 | 0.450 | 0.095 | 0.173 | 0.076 | -0.036 |
| blend_baseline | post_covid | 107 | 0.242 | 3 | 104 | 1 | 0.028 | 0.250 | 0.028 | 0.054 | 0.025 | -0.088 |
| colagnn_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.173 |
| lstm_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.174 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 64 | 0.145 | 31 | 33 | 33 | 0.484 | 0.516 | 0.320 | 0.484 | 0.397 | -0.026 |
| persistence | post_covid | 64 | 0.145 | 31 | 33 | 33 | 0.484 | 0.516 | 0.320 | 0.484 | 0.397 | 0.096 |
| gnn_st_tuned | post_covid | 64 | 0.145 | 9 | 55 | 9 | 0.141 | 0.500 | 0.123 | 0.220 | 0.117 | 0.067 |
| sarima | post_covid | 64 | 0.145 | 2 | 62 | 3 | 0.031 | 0.600 | 0.030 | 0.058 | 0.023 | -0.107 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.145 | 1 | 63 | 1 | 0.016 | 0.500 | 0.015 | 0.030 | 0.013 | -0.049 |
| xgboost_tuned | post_covid | 64 | 0.145 | 1 | 63 | 1 | 0.016 | 0.500 | 0.015 | 0.030 | 0.013 | -0.044 |
| blend_baseline | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.111 |
| colagnn_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.147 |
| lstm_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.147 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 442 | 0.561 | 0.891 | 0.547 | -0.231 |
| gnn_st_nograph_tuned | post_covid | 442 | 0.538 | 0.846 | 0.393 | -0.464 |
| xgboost_tuned | post_covid | 442 | 0.536 | 0.846 | 0.368 | -0.441 |
| blend_baseline | post_covid | 442 | 0.534 | 0.814 | 0.275 | -0.604 |
| flusight_baseline | post_covid | 442 | 0.527 | 0.867 | 0.558 | -0.005 |
| persistence | post_covid | 442 | 0.527 | 0.867 | 0.558 | -0.005 |
| lstm_tuned | post_covid | 442 | 0.511 | 0.796 | 0.226 | -0.701 |
| sarima | post_covid | 442 | 0.507 | 0.837 | 0.272 | -0.407 |
| colagnn_tuned | post_covid | 442 | 0.473 | 0.803 | 0.228 | -0.629 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 18 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | post_covid | 18 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| sarima | post_covid | 16 | 5.000 | -5.000 | 6.312 | 0.500 | -8.361 |
| gnn_st_tuned | post_covid | 17 | 7.000 | -7.000 | 7.412 | 2.000 | -6.459 |
| xgboost_tuned | post_covid | 17 | 7.000 | -7.000 | 8.000 | 2.000 | -8.465 |
| gnn_st_nograph_tuned | post_covid | 17 | 10.000 | -10.000 | 9.235 | 2.000 | -8.104 |
| blend_baseline | post_covid | 17 | 10.000 | -10.000 | 10.000 | 2.000 | -10.473 |
| lstm_tuned | post_covid | 15 | 15.000 | -15.000 | 14.333 | 0.000 | -7.508 |
| colagnn_tuned | post_covid | 17 | 15.000 | -15.000 | 15.882 | 2.000 | -7.596 |

# Notes

- 9 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
