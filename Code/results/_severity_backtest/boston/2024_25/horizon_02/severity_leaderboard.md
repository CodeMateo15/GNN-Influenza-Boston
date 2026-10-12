Severity thresholds from the 4 reference seasons 2017-18, 2018-19, 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 8 values per season (32 pooled). Horizon 2, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.8, IT90 = 91.6, IT98 = 118.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 6 | 0.115 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.645 | 0.582 |
| gnn_st_nograph_tuned | full | 6 | 0.115 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.645 | 0.640 |
| gnn_st_tuned | full | 6 | 0.115 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.645 | 0.705 |
| lstm_tuned | full | 6 | 0.115 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.645 | 0.691 |
| flusight_baseline | full | 6 | 0.115 | 4 | 2 | 2 | 0.667 | 0.333 | 0.500 | 0.667 | 0.623 | 0.498 |
| persistence | full | 6 | 0.115 | 4 | 2 | 2 | 0.667 | 0.333 | 0.500 | 0.667 | 0.623 | 0.528 |
| sarima | full | 6 | 0.115 | 3 | 3 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.517 |
| blend_baseline | full | 6 | 0.115 | 3 | 3 | 1 | 0.500 | 0.250 | 0.429 | 0.600 | 0.478 | 0.524 |
| xgboost_tuned | full | 6 | 0.115 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.445 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.101 |
| colagnn_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.091 |
| flusight_baseline | full | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.144 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.148 |
| gnn_st_tuned | full | 4 | 0.077 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | 0.164 |
| lstm_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.138 |
| persistence | full | 4 | 0.077 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.458 | 0.207 |
| sarima | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.042 |
| xgboost_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.009 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.402 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.002 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.008 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.244 |
| sarima | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| sarima | full | 52 | 0.904 | 0.942 | 0.434 | -0.154 |
| blend_baseline | full | 52 | 0.885 | 0.942 | 0.407 | -0.135 |
| colagnn_tuned | full | 52 | 0.885 | 0.962 | 0.536 | -0.115 |
| gnn_st_nograph_tuned | full | 52 | 0.885 | 0.962 | 0.536 | -0.115 |
| lstm_tuned | full | 52 | 0.885 | 0.962 | 0.536 | -0.115 |
| xgboost_tuned | full | 52 | 0.885 | 0.923 | 0.000 | -0.212 |
| flusight_baseline | full | 52 | 0.865 | 0.942 | 0.613 | 0.000 |
| gnn_st_tuned | full | 52 | 0.865 | 0.962 | 0.543 | -0.096 |
| persistence | full | 52 | 0.865 | 0.942 | 0.613 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 6 | 0.231 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.617 | 0.520 |
| gnn_st_nograph_tuned | full | 6 | 0.231 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.617 | 0.586 |
| gnn_st_tuned | full | 6 | 0.231 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.617 | 0.661 |
| lstm_tuned | full | 6 | 0.231 | 4 | 2 | 1 | 0.667 | 0.200 | 0.571 | 0.727 | 0.617 | 0.645 |
| flusight_baseline | full | 6 | 0.231 | 4 | 2 | 2 | 0.667 | 0.333 | 0.500 | 0.667 | 0.567 | 0.423 |
| persistence | full | 6 | 0.231 | 4 | 2 | 2 | 0.667 | 0.333 | 0.500 | 0.667 | 0.567 | 0.458 |
| sarima | full | 6 | 0.231 | 3 | 3 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.445 |
| blend_baseline | full | 6 | 0.231 | 3 | 3 | 1 | 0.500 | 0.250 | 0.429 | 0.600 | 0.450 | 0.452 |
| xgboost_tuned | full | 6 | 0.231 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.362 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.020 |
| colagnn_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.009 |
| flusight_baseline | full | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.066 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.071 |
| gnn_st_tuned | full | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | 0.088 |
| lstm_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.060 |
| persistence | full | 4 | 0.154 | 2 | 2 | 2 | 0.500 | 0.500 | 0.333 | 0.500 | 0.409 | 0.135 |
| sarima | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.136 |
| xgboost_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.153 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| colagnn_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.035 |
| flusight_baseline | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.430 |
| gnn_st_nograph_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.017 |
| gnn_st_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.023 |
| lstm_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| persistence | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.269 |
| sarima | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| xgboost_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| sarima | full | 26 | 0.808 | 0.885 | 0.403 | -0.308 |
| blend_baseline | full | 26 | 0.769 | 0.885 | 0.365 | -0.269 |
| colagnn_tuned | full | 26 | 0.769 | 0.923 | 0.495 | -0.231 |
| gnn_st_nograph_tuned | full | 26 | 0.769 | 0.923 | 0.495 | -0.231 |
| lstm_tuned | full | 26 | 0.769 | 0.923 | 0.495 | -0.231 |
| xgboost_tuned | full | 26 | 0.769 | 0.846 | 0.000 | -0.423 |
| flusight_baseline | full | 26 | 0.731 | 0.885 | 0.564 | 0.000 |
| gnn_st_tuned | full | 26 | 0.731 | 0.923 | 0.499 | -0.192 |
| persistence | full | 26 | 0.731 | 0.885 | 0.564 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 81 | 0.120 | 51 | 30 | 12 | 0.630 | 0.190 | 0.548 | 0.708 | 0.609 | 0.552 |
| lstm_tuned | full | 81 | 0.120 | 51 | 30 | 13 | 0.630 | 0.203 | 0.543 | 0.703 | 0.608 | 0.558 |
| flusight_baseline | full | 81 | 0.120 | 51 | 30 | 30 | 0.630 | 0.370 | 0.459 | 0.630 | 0.579 | 0.375 |
| persistence | full | 81 | 0.120 | 51 | 30 | 30 | 0.630 | 0.370 | 0.459 | 0.630 | 0.579 | 0.396 |
| colagnn_tuned | full | 81 | 0.120 | 47 | 34 | 15 | 0.580 | 0.242 | 0.490 | 0.657 | 0.555 | 0.497 |
| gnn_st_nograph_tuned | full | 81 | 0.120 | 46 | 35 | 13 | 0.568 | 0.220 | 0.489 | 0.657 | 0.546 | 0.504 |
| blend_baseline | full | 81 | 0.120 | 35 | 46 | 13 | 0.432 | 0.271 | 0.372 | 0.543 | 0.410 | 0.414 |
| xgboost_tuned | full | 81 | 0.120 | 20 | 61 | 5 | 0.247 | 0.200 | 0.233 | 0.377 | 0.239 | 0.354 |
| sarima | full | 81 | 0.120 | 19 | 62 | 11 | 0.235 | 0.367 | 0.207 | 0.342 | 0.216 | 0.234 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.059 | 11 | 29 | 29 | 0.275 | 0.725 | 0.159 | 0.275 | 0.229 | -0.216 |
| persistence | full | 40 | 0.059 | 11 | 29 | 29 | 0.275 | 0.725 | 0.159 | 0.275 | 0.229 | -0.057 |
| blend_baseline | full | 40 | 0.059 | 2 | 38 | 6 | 0.050 | 0.750 | 0.043 | 0.083 | 0.041 | 0.029 |
| gnn_st_tuned | full | 40 | 0.059 | 2 | 38 | 7 | 0.050 | 0.778 | 0.043 | 0.082 | 0.039 | 0.071 |
| gnn_st_nograph_tuned | full | 40 | 0.059 | 1 | 39 | 3 | 0.025 | 0.750 | 0.023 | 0.045 | 0.020 | 0.072 |
| colagnn_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.076 |
| lstm_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.107 |
| xgboost_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.008 |
| sarima | full | 40 | 0.059 | 0 | 40 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.008 | -0.047 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 12 | 0.018 | 2 | 10 | 10 | 0.167 | 0.833 | 0.091 | 0.167 | 0.152 | -0.466 |
| persistence | full | 12 | 0.018 | 2 | 10 | 10 | 0.167 | 0.833 | 0.091 | 0.167 | 0.152 | -0.326 |
| blend_baseline | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.004 |
| colagnn_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.005 |
| gnn_st_nograph_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.030 |
| gnn_st_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.013 |
| lstm_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.019 |
| sarima | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.053 |
| xgboost_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |

### All four bands — 677 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| lstm_tuned | full | 677 | 0.892 | 0.969 | 0.530 | -0.102 |
| colagnn_tuned | full | 677 | 0.889 | 0.966 | 0.468 | -0.105 |
| gnn_st_nograph_tuned | full | 677 | 0.889 | 0.966 | 0.466 | -0.103 |
| gnn_st_tuned | full | 677 | 0.888 | 0.970 | 0.532 | -0.090 |
| blend_baseline | full | 677 | 0.886 | 0.953 | 0.347 | -0.114 |
| xgboost_tuned | full | 677 | 0.883 | 0.951 | 0.247 | -0.160 |
| sarima | full | 677 | 0.873 | 0.947 | 0.199 | -0.145 |
| flusight_baseline | full | 677 | 0.852 | 0.953 | 0.519 | 0.000 |
| persistence | full | 677 | 0.852 | 0.953 | 0.519 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | full | 81 | 0.224 | 51 | 30 | 12 | 0.630 | 0.190 | 0.548 | 0.708 | 0.587 | 0.491 |
| lstm_tuned | full | 81 | 0.224 | 51 | 30 | 13 | 0.630 | 0.203 | 0.543 | 0.703 | 0.583 | 0.498 |
| colagnn_tuned | full | 81 | 0.224 | 47 | 34 | 15 | 0.580 | 0.242 | 0.490 | 0.657 | 0.527 | 0.430 |
| flusight_baseline | full | 81 | 0.224 | 51 | 30 | 30 | 0.630 | 0.370 | 0.459 | 0.630 | 0.522 | 0.296 |
| persistence | full | 81 | 0.224 | 51 | 30 | 30 | 0.630 | 0.370 | 0.459 | 0.630 | 0.522 | 0.319 |
| gnn_st_nograph_tuned | full | 81 | 0.224 | 46 | 35 | 13 | 0.568 | 0.220 | 0.489 | 0.657 | 0.521 | 0.437 |
| blend_baseline | full | 81 | 0.224 | 35 | 46 | 13 | 0.432 | 0.271 | 0.372 | 0.543 | 0.386 | 0.336 |
| xgboost_tuned | full | 81 | 0.224 | 20 | 61 | 5 | 0.247 | 0.200 | 0.233 | 0.377 | 0.229 | 0.267 |
| sarima | full | 81 | 0.224 | 19 | 62 | 11 | 0.235 | 0.367 | 0.207 | 0.342 | 0.195 | 0.131 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.111 | 11 | 29 | 29 | 0.275 | 0.725 | 0.159 | 0.275 | 0.185 | -0.287 |
| persistence | full | 40 | 0.111 | 11 | 29 | 29 | 0.275 | 0.725 | 0.159 | 0.275 | 0.185 | -0.119 |
| blend_baseline | full | 40 | 0.111 | 2 | 38 | 6 | 0.050 | 0.750 | 0.043 | 0.083 | 0.031 | -0.028 |
| gnn_st_tuned | full | 40 | 0.111 | 2 | 38 | 7 | 0.050 | 0.778 | 0.043 | 0.082 | 0.028 | 0.017 |
| gnn_st_nograph_tuned | full | 40 | 0.111 | 1 | 39 | 3 | 0.025 | 0.750 | 0.023 | 0.045 | 0.016 | 0.018 |
| colagnn_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.022 |
| lstm_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.056 |
| xgboost_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.050 |
| sarima | full | 40 | 0.111 | 0 | 40 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.016 | -0.107 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 12 | 0.033 | 2 | 10 | 10 | 0.167 | 0.833 | 0.091 | 0.167 | 0.138 | -0.489 |
| persistence | full | 12 | 0.033 | 2 | 10 | 10 | 0.167 | 0.833 | 0.091 | 0.167 | 0.138 | -0.347 |
| blend_baseline | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.012 |
| colagnn_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |
| gnn_st_nograph_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.014 |
| gnn_st_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| lstm_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.003 |
| sarima | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.070 |
| xgboost_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.027 |

### All four bands — 361 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| lstm_tuned | full | 361 | 0.798 | 0.942 | 0.493 | -0.191 |
| colagnn_tuned | full | 361 | 0.792 | 0.936 | 0.427 | -0.197 |
| gnn_st_nograph_tuned | full | 361 | 0.792 | 0.936 | 0.426 | -0.194 |
| gnn_st_tuned | full | 361 | 0.789 | 0.945 | 0.493 | -0.169 |
| blend_baseline | full | 361 | 0.787 | 0.911 | 0.304 | -0.213 |
| xgboost_tuned | full | 361 | 0.781 | 0.909 | 0.223 | -0.299 |
| sarima | full | 361 | 0.762 | 0.900 | 0.165 | -0.271 |
| flusight_baseline | full | 361 | 0.723 | 0.911 | 0.467 | 0.000 |
| persistence | full | 361 | 0.723 | 0.911 | 0.467 | 0.000 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| persistence | full | 14 | 2.000 | -2.000 | 2.000 | 2.000 | 0.000 |
| gnn_st_tuned | full | 14 | 2.000 | -2.000 | 2.143 | 2.000 | -16.222 |
| gnn_st_nograph_tuned | full | 14 | 2.000 | -2.000 | 2.357 | 2.000 | -13.658 |
| lstm_tuned | full | 14 | 2.000 | -2.000 | 2.357 | 0.500 | -18.562 |
| xgboost_tuned | full | 7 | 3.000 | -3.000 | 2.429 | -0.500 | -22.344 |
| colagnn_tuned | full | 14 | 3.000 | -3.000 | 2.714 | 1.000 | -16.931 |
| blend_baseline | full | 14 | 3.000 | -3.000 | 3.429 | 2.000 | -13.126 |
| sarima | full | 8 | 4.000 | -4.000 | 4.125 | -0.500 | -15.523 |
