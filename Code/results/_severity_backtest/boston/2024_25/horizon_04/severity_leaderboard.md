Severity thresholds from the 4 reference seasons 2017-18, 2018-19, 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 8 values per season (32 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.8, IT90 = 91.6, IT98 = 118.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 6 | 0.115 | 2 | 4 | 1 | 0.333 | 0.333 | 0.286 | 0.444 | 0.312 | 0.260 |
| flusight_baseline | full | 6 | 0.115 | 2 | 4 | 4 | 0.333 | 0.667 | 0.200 | 0.333 | 0.246 | -0.143 |
| persistence | full | 6 | 0.115 | 2 | 4 | 4 | 0.333 | 0.667 | 0.200 | 0.333 | 0.246 | -0.148 |
| lstm_tuned | full | 6 | 0.115 | 1 | 5 | 2 | 0.167 | 0.667 | 0.125 | 0.222 | 0.123 | 0.159 |
| gnn_st_nograph_tuned | full | 6 | 0.115 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.179 |
| gnn_st_tuned | full | 6 | 0.115 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.318 |
| sarima | full | 6 | 0.115 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.107 |
| xgboost_tuned | full | 6 | 0.115 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.103 |
| blend_baseline | full | 6 | 0.115 | 0 | 6 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.043 | -0.014 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.096 |
| colagnn_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.062 |
| flusight_baseline | full | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.486 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.072 |
| gnn_st_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.071 |
| lstm_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.075 |
| persistence | full | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.449 |
| sarima | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.082 |
| xgboost_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.082 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| colagnn_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| flusight_baseline | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.653 |
| gnn_st_nograph_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| gnn_st_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| lstm_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| persistence | full | 1 | 0.019 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.020 | -0.670 |
| sarima | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |
| xgboost_tuned | full | 1 | 0.019 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.020 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 52 | 0.885 | 0.942 | 0.191 | -0.154 |
| gnn_st_nograph_tuned | full | 52 | 0.885 | 0.923 | 0.000 | -0.212 |
| gnn_st_tuned | full | 52 | 0.885 | 0.923 | 0.000 | -0.212 |
| sarima | full | 52 | 0.885 | 0.923 | 0.000 | -0.212 |
| xgboost_tuned | full | 52 | 0.885 | 0.923 | 0.000 | -0.212 |
| lstm_tuned | full | 52 | 0.865 | 0.923 | 0.030 | -0.154 |
| blend_baseline | full | 52 | 0.846 | 0.923 | -0.035 | -0.173 |
| flusight_baseline | full | 52 | 0.808 | 0.885 | 0.081 | 0.000 |
| persistence | full | 52 | 0.808 | 0.885 | 0.081 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 6 | 0.231 | 2 | 4 | 1 | 0.333 | 0.333 | 0.286 | 0.444 | 0.283 | 0.149 |
| flusight_baseline | full | 6 | 0.231 | 2 | 4 | 4 | 0.333 | 0.667 | 0.200 | 0.333 | 0.133 | -0.293 |
| persistence | full | 6 | 0.231 | 2 | 4 | 4 | 0.333 | 0.667 | 0.200 | 0.333 | 0.133 | -0.320 |
| lstm_tuned | full | 6 | 0.231 | 1 | 5 | 2 | 0.167 | 0.667 | 0.125 | 0.222 | 0.067 | 0.033 |
| gnn_st_nograph_tuned | full | 6 | 0.231 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.056 |
| gnn_st_tuned | full | 6 | 0.231 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.216 |
| sarima | full | 6 | 0.231 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.027 |
| xgboost_tuned | full | 6 | 0.231 | 0 | 6 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.031 |
| blend_baseline | full | 6 | 0.231 | 0 | 6 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.100 | -0.166 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.196 |
| colagnn_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.158 |
| flusight_baseline | full | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.621 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.170 |
| gnn_st_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| lstm_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.172 |
| persistence | full | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.581 |
| sarima | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.181 |
| xgboost_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.180 |

### Crossing IT98 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.042 |
| colagnn_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| flusight_baseline | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.686 |
| gnn_st_nograph_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gnn_st_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| lstm_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| persistence | full | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.704 |
| sarima | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| xgboost_tuned | full | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 26 | 0.769 | 0.885 | 0.148 | -0.308 |
| gnn_st_nograph_tuned | full | 26 | 0.769 | 0.846 | 0.000 | -0.423 |
| gnn_st_tuned | full | 26 | 0.769 | 0.846 | 0.000 | -0.423 |
| sarima | full | 26 | 0.769 | 0.846 | 0.000 | -0.423 |
| xgboost_tuned | full | 26 | 0.769 | 0.846 | 0.000 | -0.423 |
| lstm_tuned | full | 26 | 0.731 | 0.846 | -0.023 | -0.308 |
| blend_baseline | full | 26 | 0.692 | 0.846 | -0.073 | -0.346 |
| flusight_baseline | full | 26 | 0.615 | 0.769 | -0.036 | 0.000 |
| persistence | full | 26 | 0.615 | 0.769 | -0.036 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 81 | 0.120 | 25 | 56 | 56 | 0.309 | 0.691 | 0.182 | 0.309 | 0.215 | -0.195 |
| persistence | full | 81 | 0.120 | 25 | 56 | 56 | 0.309 | 0.691 | 0.182 | 0.309 | 0.215 | -0.165 |
| colagnn_tuned | full | 81 | 0.120 | 16 | 65 | 13 | 0.198 | 0.448 | 0.170 | 0.291 | 0.176 | 0.248 |
| lstm_tuned | full | 81 | 0.120 | 9 | 72 | 19 | 0.111 | 0.679 | 0.090 | 0.165 | 0.079 | 0.105 |
| gnn_st_tuned | full | 81 | 0.120 | 5 | 76 | 9 | 0.062 | 0.643 | 0.056 | 0.105 | 0.047 | 0.239 |
| gnn_st_nograph_tuned | full | 81 | 0.120 | 4 | 77 | 9 | 0.049 | 0.692 | 0.044 | 0.085 | 0.034 | 0.147 |
| blend_baseline | full | 81 | 0.120 | 6 | 75 | 30 | 0.074 | 0.833 | 0.054 | 0.103 | 0.024 | -0.006 |
| sarima | full | 81 | 0.120 | 2 | 79 | 13 | 0.025 | 0.867 | 0.021 | 0.042 | 0.003 | 0.019 |
| xgboost_tuned | full | 81 | 0.120 | 0 | 81 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.113 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.022 |
| gnn_st_nograph_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.049 |
| gnn_st_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.044 |
| lstm_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.059 |
| sarima | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.065 |
| xgboost_tuned | full | 40 | 0.059 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.047 |
| blend_baseline | full | 40 | 0.059 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.092 |
| flusight_baseline | full | 40 | 0.059 | 1 | 39 | 39 | 0.025 | 0.975 | 0.013 | 0.025 | -0.036 | -0.654 |
| persistence | full | 40 | 0.059 | 1 | 39 | 39 | 0.025 | 0.975 | 0.013 | 0.025 | -0.036 | -0.543 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| colagnn_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| gnn_st_nograph_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.017 |
| gnn_st_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.017 |
| lstm_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| sarima | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.018 |
| xgboost_tuned | full | 12 | 0.018 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.017 |
| flusight_baseline | full | 12 | 0.018 | 0 | 12 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.018 | -0.794 |
| persistence | full | 12 | 0.018 | 0 | 12 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.018 | -0.725 |

### All four bands — 677 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | full | 677 | 0.880 | 0.941 | 0.000 | -0.196 |
| colagnn_tuned | full | 677 | 0.877 | 0.945 | 0.124 | -0.154 |
| gnn_st_nograph_tuned | full | 677 | 0.871 | 0.942 | 0.018 | -0.177 |
| gnn_st_tuned | full | 677 | 0.871 | 0.942 | 0.039 | -0.176 |
| sarima | full | 677 | 0.864 | 0.941 | -0.007 | -0.174 |
| lstm_tuned | full | 677 | 0.863 | 0.944 | 0.040 | -0.155 |
| blend_baseline | full | 677 | 0.845 | 0.939 | -0.009 | -0.142 |
| flusight_baseline | full | 677 | 0.815 | 0.903 | 0.068 | 0.000 |
| persistence | full | 677 | 0.815 | 0.903 | 0.068 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 81 | 0.224 | 16 | 65 | 13 | 0.198 | 0.448 | 0.170 | 0.291 | 0.151 | 0.146 |
| flusight_baseline | full | 81 | 0.224 | 25 | 56 | 55 | 0.309 | 0.688 | 0.184 | 0.311 | 0.112 | -0.320 |
| persistence | full | 81 | 0.224 | 25 | 56 | 55 | 0.309 | 0.688 | 0.184 | 0.311 | 0.112 | -0.303 |
| lstm_tuned | full | 81 | 0.224 | 9 | 72 | 19 | 0.111 | 0.679 | 0.090 | 0.165 | 0.043 | -0.016 |
| gnn_st_tuned | full | 81 | 0.224 | 5 | 76 | 9 | 0.062 | 0.643 | 0.056 | 0.105 | 0.030 | 0.136 |
| gnn_st_nograph_tuned | full | 81 | 0.224 | 4 | 77 | 9 | 0.049 | 0.692 | 0.044 | 0.085 | 0.017 | 0.032 |
| xgboost_tuned | full | 81 | 0.224 | 0 | 81 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.005 |
| sarima | full | 81 | 0.224 | 2 | 79 | 13 | 0.025 | 0.867 | 0.021 | 0.042 | -0.022 | -0.112 |
| blend_baseline | full | 81 | 0.224 | 6 | 75 | 30 | 0.074 | 0.833 | 0.054 | 0.103 | -0.033 | -0.139 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.081 |
| gnn_st_nograph_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.110 |
| gnn_st_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.105 |
| lstm_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.121 |
| sarima | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.127 |
| xgboost_tuned | full | 40 | 0.111 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.108 |
| blend_baseline | full | 40 | 0.111 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.155 |
| flusight_baseline | full | 40 | 0.111 | 1 | 39 | 39 | 0.025 | 0.975 | 0.013 | 0.025 | -0.096 | -0.747 |
| persistence | full | 40 | 0.111 | 1 | 39 | 39 | 0.025 | 0.975 | 0.013 | 0.025 | -0.096 | -0.631 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.050 |
| colagnn_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.031 |
| gnn_st_nograph_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| gnn_st_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.034 |
| lstm_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.037 |
| sarima | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.035 |
| xgboost_tuned | full | 12 | 0.033 | 0 | 12 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.033 |
| flusight_baseline | full | 12 | 0.033 | 0 | 12 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.034 | -0.822 |
| persistence | full | 12 | 0.033 | 0 | 12 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.034 | -0.752 |

### All four bands — 361 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost_tuned | full | 361 | 0.776 | 0.889 | 0.000 | -0.368 |
| colagnn_tuned | full | 361 | 0.770 | 0.898 | 0.092 | -0.288 |
| gnn_st_nograph_tuned | full | 361 | 0.759 | 0.892 | 0.002 | -0.332 |
| gnn_st_tuned | full | 361 | 0.759 | 0.892 | 0.021 | -0.330 |
| sarima | full | 361 | 0.745 | 0.889 | -0.027 | -0.327 |
| lstm_tuned | full | 361 | 0.742 | 0.895 | 0.005 | -0.291 |
| blend_baseline | full | 361 | 0.709 | 0.886 | -0.056 | -0.266 |
| flusight_baseline | full | 361 | 0.657 | 0.817 | -0.031 | -0.003 |
| persistence | full | 361 | 0.657 | 0.817 | -0.031 | -0.003 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| persistence | full | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| colagnn_tuned | full | 11 | 5.000 | -5.000 | 4.545 | 2.000 | -22.035 |
| gnn_st_tuned | full | 9 | 4.000 | -4.000 | 4.778 | 1.000 | -23.170 |
| lstm_tuned | full | 12 | 5.000 | -5.000 | 5.083 | 2.000 | -18.026 |
| gnn_st_nograph_tuned | full | 8 | 5.500 | -5.500 | 6.000 | 2.000 | -21.856 |
| blend_baseline | full | 14 | 6.000 | -6.000 | 6.071 | 4.000 | -18.340 |
| sarima | full | 5 | 7.000 | -7.000 | 6.200 | -2.000 | -24.284 |
| xgboost_tuned | full | 0 |  |  |  | -1.000 | -27.376 |
