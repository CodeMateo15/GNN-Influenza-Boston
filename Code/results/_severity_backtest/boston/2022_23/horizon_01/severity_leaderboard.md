Severity thresholds from the 2 reference seasons 2017-18, 2018-19, fitted on weeks before 2022-06-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 46.7, IT90 = 80.3, IT98 = 113.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.135 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.835 | 0.722 |
| gnn_st_tuned | full | 7 | 0.135 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.835 | 0.752 |
| lstm_tuned | full | 7 | 0.135 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.835 | 0.750 |
| persistence | full | 7 | 0.135 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.835 | 0.737 |
| blend_baseline | full | 7 | 0.135 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.692 | 0.722 |
| gnn_st_nograph_tuned | full | 7 | 0.135 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.692 | 0.709 |
| xgboost_tuned | full | 7 | 0.135 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.692 | 0.704 |
| colagnn_tuned | full | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.655 |
| sarima | full | 7 | 0.135 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.670 | 0.716 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.635 |
| colagnn_tuned | full | 4 | 0.077 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.443 |
| flusight_baseline | full | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.670 |
| gnn_st_nograph_tuned | full | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.582 |
| gnn_st_tuned | full | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.676 |
| lstm_tuned | full | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.630 |
| persistence | full | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.677 |
| sarima | full | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.614 |
| xgboost_tuned | full | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.585 |

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
| gnn_st_tuned | full | 52 | 0.942 | 1.000 | 0.902 | -0.019 |
| lstm_tuned | full | 52 | 0.942 | 1.000 | 0.902 | -0.019 |
| blend_baseline | full | 52 | 0.923 | 1.000 | 0.868 | -0.038 |
| flusight_baseline | full | 52 | 0.923 | 1.000 | 0.880 | 0.000 |
| gnn_st_nograph_tuned | full | 52 | 0.923 | 1.000 | 0.868 | -0.038 |
| persistence | full | 52 | 0.923 | 1.000 | 0.880 | 0.000 |
| xgboost_tuned | full | 52 | 0.923 | 1.000 | 0.868 | -0.038 |
| sarima | full | 52 | 0.885 | 1.000 | 0.820 | 0.000 |
| colagnn_tuned | full | 52 | 0.865 | 1.000 | 0.727 | -0.058 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 7 | 0.269 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.673 |
| gnn_st_tuned | full | 7 | 0.269 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.706 |
| lstm_tuned | full | 7 | 0.269 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.704 |
| persistence | full | 7 | 0.269 | 6 | 1 | 1 | 0.857 | 0.143 | 0.750 | 0.857 | 0.805 | 0.688 |
| blend_baseline | full | 7 | 0.269 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.662 | 0.671 |
| gnn_st_nograph_tuned | full | 7 | 0.269 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.662 | 0.656 |
| xgboost_tuned | full | 7 | 0.269 | 5 | 2 | 1 | 0.714 | 0.167 | 0.625 | 0.769 | 0.662 | 0.649 |
| colagnn_tuned | full | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.591 |
| sarima | full | 7 | 0.269 | 5 | 2 | 2 | 0.714 | 0.286 | 0.556 | 0.714 | 0.609 | 0.664 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.602 |
| colagnn_tuned | full | 4 | 0.154 | 1 | 3 | 0 | 0.250 | 0.000 | 0.250 | 0.400 | 0.250 | 0.392 |
| flusight_baseline | full | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.640 |
| gnn_st_nograph_tuned | full | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.544 |
| gnn_st_tuned | full | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.647 |
| lstm_tuned | full | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.596 |
| persistence | full | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.648 |
| sarima | full | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.579 |
| xgboost_tuned | full | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.547 |

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
| gnn_st_tuned | full | 26 | 0.885 | 1.000 | 0.887 | -0.038 |
| lstm_tuned | full | 26 | 0.885 | 1.000 | 0.887 | -0.038 |
| blend_baseline | full | 26 | 0.846 | 1.000 | 0.848 | -0.077 |
| flusight_baseline | full | 26 | 0.846 | 1.000 | 0.861 | 0.000 |
| gnn_st_nograph_tuned | full | 26 | 0.846 | 1.000 | 0.848 | -0.077 |
| persistence | full | 26 | 0.846 | 1.000 | 0.861 | 0.000 |
| xgboost_tuned | full | 26 | 0.846 | 1.000 | 0.848 | -0.077 |
| sarima | full | 26 | 0.769 | 1.000 | 0.791 | 0.000 |
| colagnn_tuned | full | 26 | 0.731 | 1.000 | 0.685 | -0.115 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 99 | 0.138 | 75 | 24 | 24 | 0.758 | 0.242 | 0.610 | 0.758 | 0.719 | 0.557 |
| persistence | full | 99 | 0.138 | 75 | 24 | 24 | 0.758 | 0.242 | 0.610 | 0.758 | 0.719 | 0.572 |
| lstm_tuned | full | 99 | 0.138 | 73 | 26 | 16 | 0.737 | 0.180 | 0.635 | 0.777 | 0.711 | 0.653 |
| gnn_st_tuned | full | 99 | 0.138 | 73 | 26 | 17 | 0.737 | 0.189 | 0.629 | 0.772 | 0.710 | 0.657 |
| blend_baseline | full | 99 | 0.138 | 71 | 28 | 18 | 0.717 | 0.202 | 0.607 | 0.755 | 0.688 | 0.579 |
| sarima | full | 99 | 0.138 | 71 | 28 | 21 | 0.717 | 0.228 | 0.592 | 0.743 | 0.683 | 0.567 |
| xgboost_tuned | full | 99 | 0.138 | 70 | 29 | 17 | 0.707 | 0.195 | 0.603 | 0.753 | 0.680 | 0.571 |
| gnn_st_nograph_tuned | full | 99 | 0.138 | 69 | 30 | 15 | 0.697 | 0.179 | 0.605 | 0.754 | 0.673 | 0.578 |
| colagnn_tuned | full | 99 | 0.138 | 70 | 29 | 28 | 0.707 | 0.286 | 0.551 | 0.711 | 0.662 | 0.597 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.056 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.603 | 0.375 |
| persistence | full | 40 | 0.056 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.603 | 0.412 |
| gnn_st_tuned | full | 40 | 0.056 | 20 | 20 | 8 | 0.500 | 0.286 | 0.417 | 0.588 | 0.488 | 0.440 |
| blend_baseline | full | 40 | 0.056 | 19 | 21 | 7 | 0.475 | 0.269 | 0.404 | 0.576 | 0.465 | 0.419 |
| sarima | full | 40 | 0.056 | 19 | 21 | 11 | 0.475 | 0.367 | 0.373 | 0.543 | 0.459 | 0.355 |
| lstm_tuned | full | 40 | 0.056 | 17 | 23 | 11 | 0.425 | 0.393 | 0.333 | 0.500 | 0.409 | 0.386 |
| gnn_st_nograph_tuned | full | 40 | 0.056 | 16 | 24 | 5 | 0.400 | 0.238 | 0.356 | 0.525 | 0.393 | 0.406 |
| xgboost_tuned | full | 40 | 0.056 | 16 | 24 | 5 | 0.400 | 0.238 | 0.356 | 0.525 | 0.393 | 0.402 |
| colagnn_tuned | full | 40 | 0.056 | 5 | 35 | 3 | 0.125 | 0.375 | 0.116 | 0.208 | 0.121 | 0.335 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 8 | 0.011 | 2 | 6 | 4 | 0.250 | 0.667 | 0.167 | 0.286 | 0.244 | 0.027 |
| flusight_baseline | full | 8 | 0.011 | 2 | 6 | 6 | 0.250 | 0.750 | 0.143 | 0.250 | 0.242 | -0.244 |
| persistence | full | 8 | 0.011 | 2 | 6 | 6 | 0.250 | 0.750 | 0.143 | 0.250 | 0.242 | -0.147 |
| gnn_st_nograph_tuned | full | 8 | 0.011 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.086 |
| xgboost_tuned | full | 8 | 0.011 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.084 |
| gnn_st_tuned | full | 8 | 0.011 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.124 | 0.091 |
| lstm_tuned | full | 8 | 0.011 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.124 | -0.030 |
| sarima | full | 8 | 0.011 | 1 | 7 | 2 | 0.125 | 0.667 | 0.100 | 0.182 | 0.122 | -0.035 |
| colagnn_tuned | full | 8 | 0.011 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.062 |

### All four bands — 716 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | full | 716 | 0.902 | 0.986 | 0.714 | -0.057 |
| gnn_st_tuned | full | 716 | 0.899 | 0.992 | 0.759 | -0.038 |
| xgboost_tuned | full | 716 | 0.899 | 0.987 | 0.718 | -0.053 |
| blend_baseline | full | 716 | 0.898 | 0.986 | 0.734 | -0.036 |
| lstm_tuned | full | 716 | 0.898 | 0.985 | 0.730 | -0.039 |
| flusight_baseline | full | 716 | 0.891 | 0.985 | 0.747 | 0.000 |
| persistence | full | 716 | 0.891 | 0.985 | 0.747 | 0.000 |
| sarima | full | 716 | 0.891 | 0.985 | 0.713 | -0.031 |
| colagnn_tuned | full | 716 | 0.869 | 0.987 | 0.641 | -0.057 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lstm_tuned | full | 99 | 0.273 | 73 | 26 | 16 | 0.737 | 0.180 | 0.635 | 0.777 | 0.677 | 0.589 |
| gnn_st_tuned | full | 99 | 0.273 | 73 | 26 | 17 | 0.737 | 0.189 | 0.629 | 0.772 | 0.673 | 0.594 |
| flusight_baseline | full | 99 | 0.273 | 75 | 24 | 23 | 0.758 | 0.235 | 0.615 | 0.761 | 0.670 | 0.496 |
| persistence | full | 99 | 0.273 | 75 | 24 | 23 | 0.758 | 0.235 | 0.615 | 0.761 | 0.670 | 0.510 |
| blend_baseline | full | 99 | 0.273 | 71 | 28 | 18 | 0.717 | 0.202 | 0.607 | 0.755 | 0.649 | 0.511 |
| xgboost_tuned | full | 99 | 0.273 | 70 | 29 | 17 | 0.707 | 0.195 | 0.603 | 0.753 | 0.643 | 0.499 |
| gnn_st_nograph_tuned | full | 99 | 0.273 | 69 | 30 | 15 | 0.697 | 0.179 | 0.605 | 0.754 | 0.640 | 0.507 |
| sarima | full | 99 | 0.273 | 71 | 28 | 21 | 0.717 | 0.228 | 0.592 | 0.743 | 0.638 | 0.495 |
| colagnn_tuned | full | 99 | 0.273 | 70 | 29 | 28 | 0.707 | 0.286 | 0.551 | 0.711 | 0.601 | 0.524 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 40 | 0.110 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.579 | 0.337 |
| persistence | full | 40 | 0.110 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.579 | 0.376 |
| gnn_st_tuned | full | 40 | 0.110 | 20 | 20 | 8 | 0.500 | 0.286 | 0.417 | 0.588 | 0.475 | 0.406 |
| blend_baseline | full | 40 | 0.110 | 19 | 21 | 7 | 0.475 | 0.269 | 0.404 | 0.576 | 0.453 | 0.384 |
| sarima | full | 40 | 0.110 | 19 | 21 | 11 | 0.475 | 0.367 | 0.373 | 0.543 | 0.441 | 0.316 |
| lstm_tuned | full | 40 | 0.110 | 17 | 23 | 11 | 0.425 | 0.393 | 0.333 | 0.500 | 0.391 | 0.349 |
| gnn_st_nograph_tuned | full | 40 | 0.110 | 16 | 24 | 5 | 0.400 | 0.238 | 0.356 | 0.525 | 0.385 | 0.370 |
| xgboost_tuned | full | 40 | 0.110 | 16 | 24 | 5 | 0.400 | 0.238 | 0.356 | 0.525 | 0.385 | 0.365 |
| colagnn_tuned | full | 40 | 0.110 | 5 | 35 | 3 | 0.125 | 0.375 | 0.116 | 0.208 | 0.116 | 0.295 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | full | 8 | 0.022 | 2 | 6 | 4 | 0.250 | 0.667 | 0.167 | 0.286 | 0.239 | 0.017 |
| flusight_baseline | full | 8 | 0.022 | 2 | 6 | 6 | 0.250 | 0.750 | 0.143 | 0.250 | 0.233 | -0.257 |
| persistence | full | 8 | 0.022 | 2 | 6 | 6 | 0.250 | 0.750 | 0.143 | 0.250 | 0.233 | -0.159 |
| gnn_st_nograph_tuned | full | 8 | 0.022 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.076 |
| xgboost_tuned | full | 8 | 0.022 | 1 | 7 | 0 | 0.125 | 0.000 | 0.125 | 0.222 | 0.125 | 0.074 |
| gnn_st_tuned | full | 8 | 0.022 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.122 | 0.081 |
| lstm_tuned | full | 8 | 0.022 | 1 | 7 | 1 | 0.125 | 0.500 | 0.111 | 0.200 | 0.122 | -0.041 |
| sarima | full | 8 | 0.022 | 1 | 7 | 2 | 0.125 | 0.667 | 0.100 | 0.182 | 0.119 | -0.047 |
| colagnn_tuned | full | 8 | 0.022 | 0 | 8 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.052 |

### All four bands — 363 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | full | 363 | 0.807 | 0.972 | 0.677 | -0.113 |
| gnn_st_tuned | full | 363 | 0.802 | 0.983 | 0.725 | -0.074 |
| xgboost_tuned | full | 363 | 0.802 | 0.975 | 0.681 | -0.105 |
| blend_baseline | full | 363 | 0.799 | 0.972 | 0.698 | -0.072 |
| lstm_tuned | full | 363 | 0.799 | 0.970 | 0.693 | -0.077 |
| flusight_baseline | full | 363 | 0.788 | 0.970 | 0.712 | -0.003 |
| persistence | full | 363 | 0.788 | 0.970 | 0.712 | -0.003 |
| sarima | full | 363 | 0.785 | 0.970 | 0.673 | -0.061 |
| colagnn_tuned | full | 363 | 0.741 | 0.975 | 0.590 | -0.113 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | full | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| persistence | full | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| blend_baseline | full | 14 | 1.000 | -1.000 | 1.786 | 1.000 | -3.048 |
| xgboost_tuned | full | 14 | 1.000 | -1.000 | 1.786 | 1.000 | -4.980 |
| gnn_st_nograph_tuned | full | 14 | 1.500 | -1.500 | 1.857 | 1.000 | -4.436 |
| gnn_st_tuned | full | 14 | 2.000 | -2.000 | 2.143 | 1.000 | -7.832 |
| sarima | full | 14 | 1.000 | -1.000 | 2.143 | 1.000 | -4.811 |
| colagnn_tuned | full | 14 | 3.000 | -3.000 | 2.357 | 0.000 | -6.377 |
| lstm_tuned | full | 14 | 2.500 | -2.500 | 2.500 | 0.000 | -5.645 |

# Notes

- 2 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
