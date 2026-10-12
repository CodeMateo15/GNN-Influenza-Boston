Severity thresholds from the 2 reference seasons 2017-18, 2018-19, fitted on weeks before 2022-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 46.7, IT90 = 80.3, IT98 = 113.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.135 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.340 | -0.101 |
| persistence | full | 7 | 0.135 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.340 | 0.092 |
| sarima | full | 7 | 0.135 | 2 | 5 | 4 | 0.286 | 0.667 | 0.182 | 0.308 | 0.197 | 0.076 |
| gnn_st_nograph_tuned | full | 7 | 0.135 | 1 | 6 | 3 | 0.143 | 0.750 | 0.100 | 0.182 | 0.076 | -0.022 |
| blend_baseline | full | 7 | 0.135 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | 0.054 | 0.013 |
| gnn_st_tuned | full | 7 | 0.135 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | 0.054 | -0.050 |
| xgboost_tuned | full | 7 | 0.135 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | 0.054 | -0.080 |
| colagnn_tuned | full | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.055 |
| lstm_tuned | full | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.087 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.194 |
| colagnn_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| flusight_baseline | full | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.472 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.115 |
| gnn_st_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.118 |
| lstm_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |
| persistence | full | 4 | 0.077 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.083 | -0.250 |
| sarima | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.127 |
| xgboost_tuned | full | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.139 |

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
| colagnn_tuned | full | 52 | 0.865 | 0.923 | 0.000 | -0.212 |
| lstm_tuned | full | 52 | 0.865 | 0.923 | 0.000 | -0.212 |
| gnn_st_nograph_tuned | full | 52 | 0.827 | 0.923 | 0.014 | -0.135 |
| blend_baseline | full | 52 | 0.808 | 0.923 | -0.005 | -0.115 |
| gnn_st_tuned | full | 52 | 0.808 | 0.923 | -0.005 | -0.115 |
| sarima | full | 52 | 0.808 | 0.942 | 0.154 | -0.096 |
| xgboost_tuned | full | 52 | 0.808 | 0.923 | -0.005 | -0.115 |
| flusight_baseline | full | 52 | 0.788 | 0.904 | 0.220 | 0.000 |
| persistence | full | 52 | 0.788 | 0.904 | 0.220 | 0.000 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.269 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.218 | -0.194 |
| persistence | full | 7 | 0.269 | 3 | 4 | 4 | 0.429 | 0.571 | 0.273 | 0.429 | 0.218 | -0.034 |
| sarima | full | 7 | 0.269 | 2 | 5 | 4 | 0.286 | 0.667 | 0.182 | 0.308 | 0.075 | -0.090 |
| colagnn_tuned | full | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.246 |
| lstm_tuned | full | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.284 |
| gnn_st_nograph_tuned | full | 7 | 0.269 | 1 | 6 | 3 | 0.143 | 0.750 | 0.100 | 0.182 | -0.015 | -0.209 |
| blend_baseline | full | 7 | 0.269 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | -0.068 | -0.163 |
| gnn_st_tuned | full | 7 | 0.269 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | -0.068 | -0.241 |
| xgboost_tuned | full | 7 | 0.269 | 1 | 6 | 4 | 0.143 | 0.800 | 0.091 | 0.167 | -0.068 | -0.277 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.302 |
| colagnn_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| flusight_baseline | full | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.605 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.216 |
| gnn_st_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.220 |
| lstm_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |
| persistence | full | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.363 |
| sarima | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.229 |
| xgboost_tuned | full | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.243 |

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
| colagnn_tuned | full | 26 | 0.731 | 0.846 | 0.000 | -0.423 |
| lstm_tuned | full | 26 | 0.731 | 0.846 | 0.000 | -0.423 |
| gnn_st_nograph_tuned | full | 26 | 0.654 | 0.846 | -0.071 | -0.269 |
| blend_baseline | full | 26 | 0.615 | 0.846 | -0.113 | -0.231 |
| gnn_st_tuned | full | 26 | 0.615 | 0.846 | -0.113 | -0.231 |
| sarima | full | 26 | 0.615 | 0.885 | 0.046 | -0.192 |
| xgboost_tuned | full | 26 | 0.615 | 0.846 | -0.113 | -0.231 |
| flusight_baseline | full | 26 | 0.577 | 0.808 | 0.094 | 0.000 |
| persistence | full | 26 | 0.577 | 0.808 | 0.094 | 0.000 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 99 | 0.138 | 40 | 59 | 63 | 0.404 | 0.612 | 0.247 | 0.396 | 0.302 | -0.136 |
| persistence | full | 99 | 0.138 | 40 | 59 | 63 | 0.404 | 0.612 | 0.247 | 0.396 | 0.302 | 0.010 |
| blend_baseline | full | 99 | 0.138 | 23 | 76 | 54 | 0.232 | 0.701 | 0.150 | 0.261 | 0.145 | -0.001 |
| sarima | full | 99 | 0.138 | 22 | 77 | 53 | 0.222 | 0.707 | 0.145 | 0.253 | 0.136 | 0.051 |
| xgboost_tuned | full | 99 | 0.138 | 19 | 80 | 58 | 0.192 | 0.753 | 0.121 | 0.216 | 0.098 | -0.078 |
| gnn_st_tuned | full | 99 | 0.138 | 15 | 84 | 47 | 0.152 | 0.758 | 0.103 | 0.186 | 0.075 | -0.025 |
| gnn_st_nograph_tuned | full | 99 | 0.138 | 14 | 85 | 46 | 0.141 | 0.767 | 0.097 | 0.176 | 0.067 | -0.006 |
| colagnn_tuned | full | 99 | 0.138 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.041 |
| lstm_tuned | full | 99 | 0.138 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.068 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 40 | 0.056 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.053 |
| lstm_tuned | full | 40 | 0.056 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |
| gnn_st_tuned | full | 40 | 0.056 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.101 |
| gnn_st_nograph_tuned | full | 40 | 0.056 | 0 | 40 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.099 |
| xgboost_tuned | full | 40 | 0.056 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.004 | -0.128 |
| flusight_baseline | full | 40 | 0.056 | 2 | 38 | 38 | 0.050 | 0.950 | 0.026 | 0.050 | -0.006 | -0.565 |
| persistence | full | 40 | 0.056 | 2 | 38 | 38 | 0.050 | 0.950 | 0.026 | 0.050 | -0.006 | -0.377 |
| sarima | full | 40 | 0.056 | 0 | 40 | 10 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.148 |
| blend_baseline | full | 40 | 0.056 | 0 | 40 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.018 | -0.196 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.230 |
| colagnn_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |
| gnn_st_nograph_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.059 |
| gnn_st_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.051 |
| lstm_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.011 |
| xgboost_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.084 |
| sarima | full | 8 | 0.011 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.001 | -0.183 |
| flusight_baseline | full | 8 | 0.011 | 0 | 8 | 8 | 0.000 | 1.000 | 0.000 | 0.000 | -0.011 | -0.760 |
| persistence | full | 8 | 0.011 | 0 | 8 | 8 | 0.000 | 1.000 | 0.000 | 0.000 | -0.011 | -0.885 |

### All four bands — 716 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 716 | 0.862 | 0.944 | -0.000 | -0.205 |
| lstm_tuned | full | 716 | 0.862 | 0.944 | -0.000 | -0.205 |
| gnn_st_nograph_tuned | full | 716 | 0.811 | 0.947 | 0.035 | -0.119 |
| gnn_st_tuned | full | 716 | 0.811 | 0.948 | 0.041 | -0.117 |
| sarima | full | 716 | 0.810 | 0.939 | 0.062 | -0.085 |
| blend_baseline | full | 716 | 0.809 | 0.937 | 0.070 | -0.081 |
| xgboost_tuned | full | 716 | 0.802 | 0.946 | 0.042 | -0.094 |
| flusight_baseline | full | 716 | 0.797 | 0.918 | 0.191 | 0.006 |
| persistence | full | 716 | 0.797 | 0.918 | 0.191 | 0.006 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 99 | 0.273 | 40 | 59 | 58 | 0.404 | 0.592 | 0.255 | 0.406 | 0.184 | -0.196 |
| persistence | full | 99 | 0.273 | 40 | 59 | 58 | 0.404 | 0.592 | 0.255 | 0.406 | 0.184 | -0.051 |
| blend_baseline | full | 99 | 0.273 | 23 | 76 | 54 | 0.232 | 0.701 | 0.150 | 0.261 | 0.028 | -0.142 |
| sarima | full | 99 | 0.273 | 22 | 77 | 53 | 0.222 | 0.707 | 0.145 | 0.253 | 0.021 | -0.087 |
| colagnn_tuned | full | 99 | 0.273 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.193 |
| lstm_tuned | full | 99 | 0.273 | 0 | 99 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.225 |
| gnn_st_tuned | full | 99 | 0.273 | 15 | 84 | 47 | 0.152 | 0.758 | 0.103 | 0.186 | -0.027 | -0.196 |
| xgboost_tuned | full | 99 | 0.273 | 19 | 80 | 58 | 0.192 | 0.753 | 0.121 | 0.216 | -0.028 | -0.241 |
| gnn_st_nograph_tuned | full | 99 | 0.273 | 14 | 85 | 46 | 0.141 | 0.767 | 0.097 | 0.176 | -0.033 | -0.174 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 40 | 0.110 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.117 |
| lstm_tuned | full | 40 | 0.110 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.121 |
| gnn_st_tuned | full | 40 | 0.110 | 0 | 40 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.168 |
| gnn_st_nograph_tuned | full | 40 | 0.110 | 0 | 40 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.166 |
| xgboost_tuned | full | 40 | 0.110 | 0 | 40 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -0.197 |
| sarima | full | 40 | 0.110 | 0 | 40 | 10 | 0.000 | 1.000 | 0.000 | 0.000 | -0.031 | -0.217 |
| blend_baseline | full | 40 | 0.110 | 0 | 40 | 12 | 0.000 | 1.000 | 0.000 | 0.000 | -0.037 | -0.267 |
| flusight_baseline | full | 40 | 0.110 | 2 | 38 | 38 | 0.050 | 0.950 | 0.026 | 0.050 | -0.068 | -0.654 |
| persistence | full | 40 | 0.110 | 2 | 38 | 38 | 0.050 | 0.950 | 0.026 | 0.050 | -0.068 | -0.446 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.244 |
| colagnn_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.022 |
| gnn_st_nograph_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.070 |
| gnn_st_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.063 |
| lstm_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.023 |
| xgboost_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.096 |
| sarima | full | 8 | 0.022 | 0 | 8 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.196 |
| flusight_baseline | full | 8 | 0.022 | 0 | 8 | 8 | 0.000 | 1.000 | 0.000 | 0.000 | -0.023 | -0.779 |
| persistence | full | 8 | 0.022 | 0 | 8 | 8 | 0.000 | 1.000 | 0.000 | 0.000 | -0.023 | -0.903 |

### All four bands — 363 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| colagnn_tuned | full | 363 | 0.727 | 0.890 | 0.000 | -0.405 |
| lstm_tuned | full | 363 | 0.727 | 0.890 | 0.000 | -0.405 |
| gnn_st_nograph_tuned | full | 363 | 0.628 | 0.895 | -0.052 | -0.234 |
| gnn_st_tuned | full | 363 | 0.628 | 0.898 | -0.048 | -0.231 |
| sarima | full | 363 | 0.625 | 0.879 | -0.046 | -0.168 |
| blend_baseline | full | 363 | 0.623 | 0.876 | -0.040 | -0.160 |
| flusight_baseline | full | 363 | 0.614 | 0.837 | 0.080 | -0.003 |
| persistence | full | 363 | 0.614 | 0.837 | 0.080 | -0.003 |
| xgboost_tuned | full | 363 | 0.609 | 0.893 | -0.067 | -0.185 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 4.000 | -4.000 | 4.000 | 3.000 | 0.000 |
| persistence | full | 14 | 4.000 | -4.000 | 4.000 | 3.000 | 0.000 |
| blend_baseline | full | 14 | 5.500 | -5.500 | 5.929 | 3.000 | -7.965 |
| sarima | full | 14 | 6.500 | -6.500 | 6.286 | 4.000 | -9.719 |
| xgboost_tuned | full | 14 | 7.000 | -7.000 | 6.500 | 3.000 | -10.292 |
| gnn_st_tuned | full | 14 | 7.000 | -7.000 | 6.786 | 3.000 | -9.974 |
| gnn_st_nograph_tuned | full | 14 | 7.000 | -7.000 | 6.857 | 3.000 | -11.730 |
| colagnn_tuned | full | 0 |  |  |  | 2.500 | -16.675 |
| lstm_tuned | full | 0 |  |  |  | 2.000 | -17.236 |

# Notes

- 8 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
