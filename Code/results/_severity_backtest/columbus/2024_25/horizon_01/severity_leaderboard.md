Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2024-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 26.2, IT90 = 39.3, IT98 = 50.9 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 14 | 0.269 | 13 | 1 | 2 | 0.929 | 0.133 | 0.812 | 0.897 | 0.876 | 0.756 |
| gnn_st_tuned | post_covid | 14 | 0.269 | 13 | 1 | 3 | 0.929 | 0.188 | 0.765 | 0.867 | 0.850 | 0.682 |
| flusight_baseline | post_covid | 14 | 0.269 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.682 |
| persistence | post_covid | 14 | 0.269 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.671 |
| lstm_tuned | post_covid | 14 | 0.269 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.778 | 0.682 |
| sarima | post_covid | 14 | 0.269 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.778 | 0.741 |
| blend_baseline | post_covid | 14 | 0.269 | 11 | 3 | 1 | 0.786 | 0.083 | 0.733 | 0.846 | 0.759 | 0.721 |
| colagnn_tuned | post_covid | 14 | 0.269 | 10 | 4 | 1 | 0.714 | 0.091 | 0.667 | 0.800 | 0.688 | 0.673 |
| xgboost_tuned | post_covid | 14 | 0.269 | 5 | 9 | 1 | 0.357 | 0.167 | 0.333 | 0.500 | 0.331 | 0.314 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 7 | 0.135 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.692 | 0.605 |
| flusight_baseline | post_covid | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.533 |
| persistence | post_covid | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.564 |
| lstm_tuned | post_covid | 7 | 0.135 | 3 | 4 | 0 | 0.429 | 0.000 | 0.429 | 0.600 | 0.429 | 0.446 |
| blend_baseline | post_covid | 7 | 0.135 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.311 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.135 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.491 |
| sarima | post_covid | 7 | 0.135 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.324 |
| colagnn_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.027 |
| xgboost_tuned | post_covid | 7 | 0.135 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.111 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.020 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.081 |
| flusight_baseline | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.562 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.218 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.572 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.074 |
| persistence | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.614 |
| sarima | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.024 |
| xgboost_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.083 |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 52 | 0.827 | 1.000 | 0.881 | -0.019 |
| flusight_baseline | post_covid | 52 | 0.808 | 1.000 | 0.884 | 0.000 |
| gnn_st_nograph_tuned | post_covid | 52 | 0.808 | 0.962 | 0.732 | -0.154 |
| persistence | post_covid | 52 | 0.808 | 1.000 | 0.884 | 0.000 |
| blend_baseline | post_covid | 52 | 0.788 | 0.962 | 0.714 | -0.212 |
| colagnn_tuned | post_covid | 52 | 0.788 | 0.904 | 0.531 | -0.269 |
| lstm_tuned | post_covid | 52 | 0.788 | 0.962 | 0.724 | -0.135 |
| xgboost_tuned | post_covid | 52 | 0.788 | 0.885 | 0.113 | -0.365 |
| sarima | post_covid | 52 | 0.769 | 0.962 | 0.698 | -0.154 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 14 | 0.538 | 13 | 1 | 2 | 0.929 | 0.133 | 0.812 | 0.897 | 0.762 | 0.614 |
| blend_baseline | post_covid | 14 | 0.538 | 11 | 3 | 1 | 0.786 | 0.083 | 0.733 | 0.846 | 0.702 | 0.559 |
| flusight_baseline | post_covid | 14 | 0.538 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.690 | 0.547 |
| persistence | post_covid | 14 | 0.538 | 12 | 2 | 2 | 0.857 | 0.143 | 0.750 | 0.857 | 0.690 | 0.527 |
| gnn_st_tuned | post_covid | 14 | 0.538 | 13 | 1 | 3 | 0.929 | 0.188 | 0.765 | 0.867 | 0.679 | 0.515 |
| colagnn_tuned | post_covid | 14 | 0.538 | 10 | 4 | 1 | 0.714 | 0.091 | 0.667 | 0.800 | 0.631 | 0.483 |
| lstm_tuned | post_covid | 14 | 0.538 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.607 | 0.512 |
| sarima | post_covid | 14 | 0.538 | 12 | 2 | 3 | 0.857 | 0.200 | 0.706 | 0.828 | 0.607 | 0.590 |
| xgboost_tuned | post_covid | 14 | 0.538 | 5 | 9 | 1 | 0.357 | 0.167 | 0.333 | 0.500 | 0.274 | -0.086 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 7 | 0.269 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.662 | 0.532 |
| flusight_baseline | post_covid | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.447 |
| persistence | post_covid | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.484 |
| lstm_tuned | post_covid | 7 | 0.269 | 3 | 4 | 0 | 0.429 | 0.000 | 0.429 | 0.600 | 0.429 | 0.344 |
| blend_baseline | post_covid | 7 | 0.269 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.184 |
| gnn_st_nograph_tuned | post_covid | 7 | 0.269 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.397 |
| sarima | post_covid | 7 | 0.269 | 2 | 5 | 0 | 0.286 | 0.000 | 0.286 | 0.444 | 0.286 | 0.199 |
| colagnn_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.153 |
| xgboost_tuned | post_covid | 7 | 0.269 | 0 | 7 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.315 |

### Crossing IT98 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.069 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.179 |
| flusight_baseline | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.522 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.147 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.533 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.010 |
| persistence | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.578 |
| sarima | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.118 |
| xgboost_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.182 |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 26 | 0.654 | 1.000 | 0.830 | -0.038 |
| flusight_baseline | post_covid | 26 | 0.615 | 1.000 | 0.839 | 0.000 |
| gnn_st_nograph_tuned | post_covid | 26 | 0.615 | 0.923 | 0.631 | -0.308 |
| persistence | post_covid | 26 | 0.615 | 1.000 | 0.839 | 0.000 |
| blend_baseline | post_covid | 26 | 0.577 | 0.923 | 0.631 | -0.423 |
| colagnn_tuned | post_covid | 26 | 0.577 | 0.808 | 0.420 | -0.538 |
| lstm_tuned | post_covid | 26 | 0.577 | 0.923 | 0.617 | -0.269 |
| xgboost_tuned | post_covid | 26 | 0.577 | 0.769 | 0.009 | -0.731 |
| sarima | post_covid | 26 | 0.538 | 0.923 | 0.584 | -0.308 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 248 | 0.281 | 191 | 57 | 56 | 0.770 | 0.227 | 0.628 | 0.772 | 0.682 | 0.546 |
| lstm_tuned | post_covid | 248 | 0.281 | 182 | 66 | 44 | 0.734 | 0.195 | 0.623 | 0.768 | 0.665 | 0.538 |
| gnn_st_nograph_tuned | post_covid | 248 | 0.281 | 166 | 82 | 37 | 0.669 | 0.182 | 0.582 | 0.736 | 0.611 | 0.513 |
| flusight_baseline | post_covid | 248 | 0.281 | 177 | 71 | 70 | 0.714 | 0.283 | 0.557 | 0.715 | 0.604 | 0.421 |
| persistence | post_covid | 248 | 0.281 | 177 | 71 | 70 | 0.714 | 0.283 | 0.557 | 0.715 | 0.604 | 0.427 |
| sarima | post_covid | 248 | 0.281 | 156 | 92 | 43 | 0.629 | 0.216 | 0.536 | 0.698 | 0.561 | 0.417 |
| blend_baseline | post_covid | 248 | 0.281 | 139 | 109 | 25 | 0.560 | 0.152 | 0.509 | 0.675 | 0.521 | 0.486 |
| colagnn_tuned | post_covid | 248 | 0.281 | 129 | 119 | 22 | 0.520 | 0.146 | 0.478 | 0.647 | 0.486 | 0.463 |
| xgboost_tuned | post_covid | 248 | 0.281 | 57 | 191 | 32 | 0.230 | 0.360 | 0.204 | 0.338 | 0.180 | 0.187 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.121 | 74 | 33 | 33 | 0.692 | 0.308 | 0.529 | 0.692 | 0.649 | 0.421 |
| persistence | post_covid | 107 | 0.121 | 74 | 33 | 33 | 0.692 | 0.308 | 0.529 | 0.692 | 0.649 | 0.437 |
| gnn_st_tuned | post_covid | 107 | 0.121 | 57 | 50 | 15 | 0.533 | 0.208 | 0.467 | 0.637 | 0.513 | 0.516 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.121 | 37 | 70 | 4 | 0.346 | 0.098 | 0.333 | 0.500 | 0.341 | 0.380 |
| sarima | post_covid | 107 | 0.121 | 23 | 84 | 6 | 0.215 | 0.207 | 0.204 | 0.338 | 0.207 | 0.178 |
| lstm_tuned | post_covid | 107 | 0.121 | 18 | 89 | 4 | 0.168 | 0.182 | 0.162 | 0.279 | 0.163 | 0.363 |
| blend_baseline | post_covid | 107 | 0.121 | 15 | 92 | 2 | 0.140 | 0.118 | 0.138 | 0.242 | 0.138 | 0.255 |
| colagnn_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.022 |
| xgboost_tuned | post_covid | 107 | 0.121 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 64 | 0.072 | 44 | 20 | 20 | 0.688 | 0.312 | 0.524 | 0.688 | 0.663 | 0.480 |
| persistence | post_covid | 64 | 0.072 | 44 | 20 | 20 | 0.688 | 0.312 | 0.524 | 0.688 | 0.663 | 0.495 |
| gnn_st_tuned | post_covid | 64 | 0.072 | 30 | 34 | 7 | 0.469 | 0.189 | 0.423 | 0.594 | 0.460 | 0.457 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.072 | 5 | 59 | 0 | 0.078 | 0.000 | 0.078 | 0.145 | 0.078 | 0.196 |
| sarima | post_covid | 64 | 0.072 | 4 | 60 | 2 | 0.062 | 0.333 | 0.061 | 0.114 | 0.060 | 0.069 |
| blend_baseline | post_covid | 64 | 0.072 | 1 | 63 | 0 | 0.016 | 0.000 | 0.016 | 0.031 | 0.016 | 0.076 |
| colagnn_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.050 |
| lstm_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.030 |
| xgboost_tuned | post_covid | 64 | 0.072 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.047 |

### All four bands — 884 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 884 | 0.781 | 0.972 | 0.776 | -0.071 |
| gnn_st_nograph_tuned | post_covid | 884 | 0.765 | 0.955 | 0.653 | -0.192 |
| flusight_baseline | post_covid | 884 | 0.759 | 0.965 | 0.768 | -0.001 |
| persistence | post_covid | 884 | 0.759 | 0.965 | 0.768 | -0.001 |
| lstm_tuned | post_covid | 884 | 0.758 | 0.941 | 0.604 | -0.193 |
| sarima | post_covid | 884 | 0.757 | 0.937 | 0.529 | -0.209 |
| blend_baseline | post_covid | 884 | 0.747 | 0.931 | 0.533 | -0.268 |
| colagnn_tuned | post_covid | 884 | 0.747 | 0.907 | 0.442 | -0.303 |
| xgboost_tuned | post_covid | 884 | 0.729 | 0.890 | 0.087 | -0.373 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm_tuned | post_covid | 234 | 0.529 | 182 | 52 | 44 | 0.778 | 0.195 | 0.655 | 0.791 | 0.566 | 0.375 |
| gnn_st_tuned | post_covid | 234 | 0.529 | 191 | 43 | 56 | 0.816 | 0.227 | 0.659 | 0.794 | 0.547 | 0.390 |
| gnn_st_nograph_tuned | post_covid | 234 | 0.529 | 166 | 68 | 37 | 0.709 | 0.182 | 0.613 | 0.760 | 0.532 | 0.337 |
| flusight_baseline | post_covid | 234 | 0.529 | 177 | 57 | 58 | 0.756 | 0.247 | 0.606 | 0.755 | 0.478 | 0.279 |
| persistence | post_covid | 234 | 0.529 | 177 | 57 | 58 | 0.756 | 0.247 | 0.606 | 0.755 | 0.478 | 0.289 |
| blend_baseline | post_covid | 234 | 0.529 | 139 | 95 | 25 | 0.594 | 0.152 | 0.537 | 0.698 | 0.474 | 0.295 |
| sarima | post_covid | 234 | 0.529 | 155 | 79 | 40 | 0.662 | 0.205 | 0.566 | 0.723 | 0.470 | 0.206 |
| colagnn_tuned | post_covid | 234 | 0.529 | 129 | 105 | 22 | 0.551 | 0.146 | 0.504 | 0.670 | 0.446 | 0.250 |
| xgboost_tuned | post_covid | 234 | 0.529 | 57 | 177 | 32 | 0.244 | 0.360 | 0.214 | 0.353 | 0.090 | -0.183 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 107 | 0.242 | 74 | 33 | 33 | 0.692 | 0.308 | 0.529 | 0.692 | 0.593 | 0.338 |
| persistence | post_covid | 107 | 0.242 | 74 | 33 | 33 | 0.692 | 0.308 | 0.529 | 0.692 | 0.593 | 0.368 |
| gnn_st_tuned | post_covid | 107 | 0.242 | 57 | 50 | 15 | 0.533 | 0.208 | 0.467 | 0.637 | 0.488 | 0.439 |
| gnn_st_nograph_tuned | post_covid | 107 | 0.242 | 37 | 70 | 4 | 0.346 | 0.098 | 0.333 | 0.500 | 0.334 | 0.282 |
| sarima | post_covid | 107 | 0.242 | 23 | 84 | 6 | 0.215 | 0.207 | 0.204 | 0.338 | 0.197 | 0.052 |
| lstm_tuned | post_covid | 107 | 0.242 | 18 | 89 | 4 | 0.168 | 0.182 | 0.162 | 0.279 | 0.156 | 0.262 |
| blend_baseline | post_covid | 107 | 0.242 | 15 | 92 | 2 | 0.140 | 0.118 | 0.138 | 0.242 | 0.134 | 0.137 |
| colagnn_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.134 |
| xgboost_tuned | post_covid | 107 | 0.242 | 0 | 107 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.220 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 64 | 0.145 | 44 | 20 | 20 | 0.688 | 0.312 | 0.524 | 0.688 | 0.635 | 0.437 |
| persistence | post_covid | 64 | 0.145 | 44 | 20 | 20 | 0.688 | 0.312 | 0.524 | 0.688 | 0.635 | 0.458 |
| gnn_st_tuned | post_covid | 64 | 0.145 | 30 | 34 | 7 | 0.469 | 0.189 | 0.423 | 0.594 | 0.450 | 0.411 |
| gnn_st_nograph_tuned | post_covid | 64 | 0.145 | 5 | 59 | 0 | 0.078 | 0.000 | 0.078 | 0.145 | 0.078 | 0.128 |
| sarima | post_covid | 64 | 0.145 | 4 | 60 | 2 | 0.062 | 0.333 | 0.061 | 0.114 | 0.057 | -0.010 |
| blend_baseline | post_covid | 64 | 0.145 | 1 | 63 | 0 | 0.016 | 0.000 | 0.016 | 0.031 | 0.016 | -0.002 |
| colagnn_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.139 |
| lstm_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.052 |
| xgboost_tuned | post_covid | 64 | 0.145 | 0 | 64 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.136 |

### All four bands — 442 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 442 | 0.593 | 0.943 | 0.707 | -0.111 |
| flusight_baseline | post_covid | 442 | 0.577 | 0.930 | 0.707 | 0.002 |
| persistence | post_covid | 442 | 0.577 | 0.930 | 0.707 | 0.002 |
| gnn_st_nograph_tuned | post_covid | 442 | 0.561 | 0.910 | 0.566 | -0.353 |
| sarima | post_covid | 442 | 0.550 | 0.873 | 0.416 | -0.396 |
| lstm_tuned | post_covid | 442 | 0.548 | 0.882 | 0.493 | -0.355 |
| blend_baseline | post_covid | 442 | 0.525 | 0.862 | 0.444 | -0.505 |
| colagnn_tuned | post_covid | 442 | 0.525 | 0.814 | 0.351 | -0.575 |
| xgboost_tuned | post_covid | 442 | 0.489 | 0.781 | -0.001 | -0.715 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 18 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| persistence | post_covid | 18 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| gnn_st_tuned | post_covid | 17 | 3.000 | -3.000 | 6.118 | 1.000 | -4.780 |
| xgboost_tuned | post_covid | 13 | 7.000 | -7.000 | 7.154 | -6.000 | -11.949 |
| lstm_tuned | post_covid | 17 | 8.000 | -8.000 | 7.294 | 1.000 | -8.078 |
| gnn_st_nograph_tuned | post_covid | 17 | 7.000 | -7.000 | 7.647 | 1.000 | -8.156 |
| sarima | post_covid | 16 | 6.500 | -6.500 | 7.688 | 1.000 | -10.479 |
| blend_baseline | post_covid | 17 | 7.000 | -7.000 | 7.941 | 1.000 | -9.558 |
| colagnn_tuned | post_covid | 17 | 14.000 | -14.000 | 12.882 | 0.500 | -8.186 |

# Notes

- 10 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
