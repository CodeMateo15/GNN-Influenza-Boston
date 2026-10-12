Severity thresholds from the 4 reference seasons 2017-18, 2018-19, 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 8 values per season (32 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.8, IT90 = 91.6, IT98 = 118.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 6 | 0.115 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.760 |
| colagnn_tuned | full | 6 | 0.115 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.872 |
| gnn_st_nograph_tuned | full | 6 | 0.115 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.782 |
| gnn_st_tuned | full | 6 | 0.115 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.854 |
| lstm_tuned | full | 6 | 0.115 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.848 |
| flusight_baseline | full | 6 | 0.115 | 5 | 1 | 1 | 0.833 | 0.167 | 0.714 | 0.833 | 0.812 | 0.761 |
| persistence | full | 6 | 0.115 | 5 | 1 | 1 | 0.833 | 0.167 | 0.714 | 0.833 | 0.812 | 0.774 |
| sarima | full | 6 | 0.115 | 4 | 2 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.734 |
| xgboost_tuned | full | 6 | 0.115 | 4 | 2 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.750 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.442 |
| colagnn_tuned | full | 4 | 0.077 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.654 |
| flusight_baseline | full | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.639 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.478 |
| gnn_st_tuned | full | 4 | 0.077 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.586 |
| lstm_tuned | full | 4 | 0.077 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.636 |
| persistence | full | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.672 |
| sarima | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.134 |
| xgboost_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.114 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.078 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.172 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.026 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.070 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.097 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.148 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | 0.170 |
| sarima | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.014 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.012 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 52 | 0.923 | 0.981 | 0.754 | -0.096 |
| colagnn_tuned | full | 52 | 0.923 | 1.000 | 0.871 | -0.077 |
| gnn_st_nograph_tuned | full | 52 | 0.923 | 0.981 | 0.754 | -0.096 |
| gnn_st_tuned | full | 52 | 0.923 | 1.000 | 0.871 | -0.077 |
| lstm_tuned | full | 52 | 0.923 | 1.000 | 0.871 | -0.077 |
| sarima | full | 52 | 0.904 | 0.962 | 0.565 | -0.135 |
| xgboost_tuned | full | 52 | 0.904 | 0.962 | 0.565 | -0.135 |
| flusight_baseline | full | 52 | 0.885 | 1.000 | 0.855 | 0.000 |
| persistence | full | 52 | 0.885 | 1.000 | 0.855 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 6 | 0.231 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.724 |
| colagnn_tuned | full | 6 | 0.231 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.853 |
| gnn_st_nograph_tuned | full | 6 | 0.231 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.749 |
| gnn_st_tuned | full | 6 | 0.231 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.832 |
| lstm_tuned | full | 6 | 0.231 | 5 | 1 | 0 | 0.833 | 0.000 | 0.833 | 0.909 | 0.833 | 0.825 |
| flusight_baseline | full | 6 | 0.231 | 5 | 1 | 1 | 0.833 | 0.167 | 0.714 | 0.833 | 0.783 | 0.725 |
| persistence | full | 6 | 0.231 | 5 | 1 | 1 | 0.833 | 0.167 | 0.714 | 0.833 | 0.783 | 0.740 |
| sarima | full | 6 | 0.231 | 4 | 2 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.694 |
| xgboost_tuned | full | 6 | 0.231 | 4 | 2 | 0 | 0.667 | 0.000 | 0.667 | 0.800 | 0.667 | 0.712 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.391 |
| colagnn_tuned | full | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.623 |
| flusight_baseline | full | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.606 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.430 |
| gnn_st_tuned | full | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.549 |
| lstm_tuned | full | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.603 |
| persistence | full | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.642 |
| sarima | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.055 |
| xgboost_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.034 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.059 |
| colagnn_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.155 |
| flusight_baseline | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.047 |
| gnn_st_nograph_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.052 |
| gnn_st_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.079 |
| lstm_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.131 |
| persistence | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | 0.153 |
| sarima | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| xgboost_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.032 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 26 | 0.846 | 0.962 | 0.730 | -0.192 |
| colagnn_tuned | full | 26 | 0.846 | 1.000 | 0.858 | -0.154 |
| gnn_st_nograph_tuned | full | 26 | 0.846 | 0.962 | 0.730 | -0.192 |
| gnn_st_tuned | full | 26 | 0.846 | 1.000 | 0.858 | -0.154 |
| lstm_tuned | full | 26 | 0.846 | 1.000 | 0.858 | -0.154 |
| sarima | full | 26 | 0.808 | 0.923 | 0.534 | -0.269 |
| xgboost_tuned | full | 26 | 0.808 | 0.923 | 0.534 | -0.269 |
| flusight_baseline | full | 26 | 0.769 | 1.000 | 0.836 | 0.000 |
| persistence | full | 26 | 0.769 | 1.000 | 0.836 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 81 | 0.120 | 66 | 15 | 6 | 0.815 | 0.083 | 0.759 | 0.863 | 0.805 | 0.734 |
| lstm_tuned | full | 81 | 0.120 | 66 | 15 | 8 | 0.815 | 0.108 | 0.742 | 0.852 | 0.801 | 0.729 |
| gnn_st_tuned | full | 81 | 0.120 | 60 | 21 | 8 | 0.741 | 0.118 | 0.674 | 0.805 | 0.727 | 0.709 |
| flusight_baseline | full | 81 | 0.120 | 61 | 20 | 20 | 0.753 | 0.247 | 0.604 | 0.753 | 0.720 | 0.599 |
| persistence | full | 81 | 0.120 | 61 | 20 | 20 | 0.753 | 0.247 | 0.604 | 0.753 | 0.720 | 0.613 |
| gnn_st_nograph_tuned | full | 81 | 0.120 | 58 | 23 | 10 | 0.716 | 0.147 | 0.637 | 0.779 | 0.699 | 0.637 |
| blend_baseline | full | 81 | 0.120 | 52 | 29 | 9 | 0.642 | 0.148 | 0.578 | 0.732 | 0.627 | 0.619 |
| xgboost_tuned | full | 81 | 0.120 | 48 | 33 | 6 | 0.593 | 0.111 | 0.552 | 0.711 | 0.583 | 0.584 |
| sarima | full | 81 | 0.120 | 35 | 46 | 7 | 0.432 | 0.167 | 0.398 | 0.569 | 0.420 | 0.411 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.059 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.601 | 0.300 |
| persistence | full | 40 | 0.059 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.601 | 0.374 |
| colagnn_tuned | full | 40 | 0.059 | 17 | 23 | 7 | 0.425 | 0.292 | 0.362 | 0.531 | 0.414 | 0.451 |
| gnn_st_tuned | full | 40 | 0.059 | 13 | 27 | 7 | 0.325 | 0.350 | 0.277 | 0.433 | 0.314 | 0.366 |
| lstm_tuned | full | 40 | 0.059 | 11 | 29 | 6 | 0.275 | 0.353 | 0.239 | 0.386 | 0.266 | 0.404 |
| gnn_st_nograph_tuned | full | 40 | 0.059 | 11 | 29 | 8 | 0.275 | 0.421 | 0.229 | 0.373 | 0.262 | 0.293 |
| blend_baseline | full | 40 | 0.059 | 8 | 32 | 6 | 0.200 | 0.429 | 0.174 | 0.296 | 0.191 | 0.288 |
| sarima | full | 40 | 0.059 | 6 | 34 | 5 | 0.150 | 0.455 | 0.133 | 0.235 | 0.142 | 0.126 |
| xgboost_tuned | full | 40 | 0.059 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.123 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 12 | 0.018 | 4 | 8 | 8 | 0.333 | 0.667 | 0.200 | 0.333 | 0.321 | -0.142 |
| persistence | full | 12 | 0.018 | 4 | 8 | 8 | 0.333 | 0.667 | 0.200 | 0.333 | 0.321 | 0.016 |
| colagnn_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.194 |
| lstm_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.198 |
| sarima | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.001 |
| xgboost_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.028 |
| blend_baseline | full | 12 | 0.018 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | 0.109 |
| gnn_st_nograph_tuned | full | 12 | 0.018 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.098 |
| gnn_st_tuned | full | 12 | 0.018 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.127 |

### All four bands — 677 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 677 | 0.914 | 0.993 | 0.801 | -0.055 |
| lstm_tuned | full | 677 | 0.908 | 0.988 | 0.754 | -0.062 |
| gnn_st_tuned | full | 677 | 0.904 | 0.982 | 0.722 | -0.064 |
| gnn_st_nograph_tuned | full | 677 | 0.897 | 0.979 | 0.690 | -0.065 |
| xgboost_tuned | full | 677 | 0.897 | 0.969 | 0.534 | -0.115 |
| blend_baseline | full | 677 | 0.895 | 0.973 | 0.631 | -0.084 |
| flusight_baseline | full | 677 | 0.892 | 0.981 | 0.762 | 0.000 |
| persistence | full | 677 | 0.892 | 0.981 | 0.762 | 0.000 |
| sarima | full | 677 | 0.891 | 0.963 | 0.448 | -0.118 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 81 | 0.224 | 66 | 15 | 6 | 0.815 | 0.083 | 0.759 | 0.863 | 0.793 | 0.698 |
| lstm_tuned | full | 81 | 0.224 | 66 | 15 | 8 | 0.815 | 0.108 | 0.742 | 0.852 | 0.786 | 0.693 |
| gnn_st_tuned | full | 81 | 0.224 | 60 | 21 | 8 | 0.741 | 0.118 | 0.674 | 0.805 | 0.712 | 0.669 |
| flusight_baseline | full | 81 | 0.224 | 61 | 20 | 20 | 0.753 | 0.247 | 0.604 | 0.753 | 0.682 | 0.548 |
| persistence | full | 81 | 0.224 | 61 | 20 | 20 | 0.753 | 0.247 | 0.604 | 0.753 | 0.682 | 0.562 |
| gnn_st_nograph_tuned | full | 81 | 0.224 | 58 | 23 | 10 | 0.716 | 0.147 | 0.637 | 0.779 | 0.680 | 0.588 |
| blend_baseline | full | 81 | 0.224 | 52 | 29 | 9 | 0.642 | 0.148 | 0.578 | 0.732 | 0.610 | 0.568 |
| xgboost_tuned | full | 81 | 0.224 | 48 | 33 | 6 | 0.593 | 0.111 | 0.552 | 0.711 | 0.571 | 0.528 |
| sarima | full | 81 | 0.224 | 35 | 46 | 7 | 0.432 | 0.167 | 0.398 | 0.569 | 0.407 | 0.332 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.111 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.578 | 0.259 |
| persistence | full | 40 | 0.111 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.578 | 0.337 |
| colagnn_tuned | full | 40 | 0.111 | 17 | 23 | 7 | 0.425 | 0.292 | 0.362 | 0.531 | 0.403 | 0.419 |
| gnn_st_tuned | full | 40 | 0.111 | 13 | 27 | 7 | 0.325 | 0.350 | 0.277 | 0.433 | 0.303 | 0.330 |
| lstm_tuned | full | 40 | 0.111 | 11 | 29 | 6 | 0.275 | 0.353 | 0.239 | 0.386 | 0.256 | 0.369 |
| gnn_st_nograph_tuned | full | 40 | 0.111 | 11 | 29 | 8 | 0.275 | 0.421 | 0.229 | 0.373 | 0.250 | 0.252 |
| blend_baseline | full | 40 | 0.111 | 8 | 32 | 6 | 0.200 | 0.429 | 0.174 | 0.296 | 0.181 | 0.246 |
| sarima | full | 40 | 0.111 | 6 | 34 | 5 | 0.150 | 0.455 | 0.133 | 0.235 | 0.134 | 0.075 |
| xgboost_tuned | full | 40 | 0.111 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.072 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 12 | 0.033 | 4 | 8 | 8 | 0.333 | 0.667 | 0.200 | 0.333 | 0.310 | -0.161 |
| persistence | full | 12 | 0.033 | 4 | 8 | 8 | 0.333 | 0.667 | 0.200 | 0.333 | 0.310 | 0.000 |
| colagnn_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.181 |
| lstm_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.185 |
| sarima | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| xgboost_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.012 |
| blend_baseline | full | 12 | 0.033 | 0 | 12 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | 0.094 |
| gnn_st_nograph_tuned | full | 12 | 0.033 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | 0.084 |
| gnn_st_tuned | full | 12 | 0.033 | 0 | 12 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | 0.113 |

### All four bands — 361 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 361 | 0.839 | 0.986 | 0.782 | -0.102 |
| lstm_tuned | full | 361 | 0.828 | 0.978 | 0.730 | -0.116 |
| gnn_st_tuned | full | 361 | 0.820 | 0.967 | 0.696 | -0.119 |
| gnn_st_nograph_tuned | full | 361 | 0.806 | 0.961 | 0.661 | -0.122 |
| xgboost_tuned | full | 361 | 0.806 | 0.942 | 0.503 | -0.216 |
| blend_baseline | full | 361 | 0.803 | 0.950 | 0.601 | -0.158 |
| flusight_baseline | full | 361 | 0.798 | 0.964 | 0.736 | 0.000 |
| persistence | full | 361 | 0.798 | 0.964 | 0.736 | 0.000 |
| sarima | full | 361 | 0.795 | 0.931 | 0.414 | -0.222 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| persistence | full | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| colagnn_tuned | full | 14 | 1.000 | -1.000 | 1.071 | 1.000 | -8.106 |
| gnn_st_tuned | full | 14 | 1.000 | -1.000 | 1.143 | 1.000 | -12.750 |
| lstm_tuned | full | 14 | 1.000 | -1.000 | 1.143 | 0.000 | -12.924 |
| blend_baseline | full | 14 | 1.000 | -1.000 | 1.429 | 1.000 | -10.404 |
| gnn_st_nograph_tuned | full | 14 | 1.000 | -1.000 | 1.714 | 1.000 | -11.631 |
| xgboost_tuned | full | 14 | 2.000 | -2.000 | 2.071 | 0.000 | -19.540 |
| sarima | full | 10 | 1.500 | -1.500 | 2.200 | 1.000 | -16.153 |
