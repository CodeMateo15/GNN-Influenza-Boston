Severity thresholds from the 2 reference seasons 2022-23, 2023-24, fitted on weeks before 2023-12-01, levels IT50/IT90/IT98, 15 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 66.9, IT90 = 90.5, IT98 = 109.7 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 9 | 0.173 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.643 | 0.563 |
| gnn_st_tuned | post_covid | 9 | 0.173 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.643 | 0.587 |
| xgboost_tuned | post_covid | 9 | 0.173 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.643 | 0.566 |
| blend_baseline | post_covid | 9 | 0.173 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.620 | 0.581 |
| sarima | post_covid | 9 | 0.173 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.620 | 0.594 |
| flusight_baseline | post_covid | 9 | 0.173 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.597 | 0.519 |
| persistence | post_covid | 9 | 0.173 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.597 | 0.545 |
| colagnn_tuned | post_covid | 9 | 0.173 | 5 | 4 | 1 | 0.556 | 0.167 | 0.500 | 0.667 | 0.532 | 0.543 |
| lstm_tuned | post_covid | 9 | 0.173 | 4 | 5 | 0 | 0.444 | 0.000 | 0.444 | 0.615 | 0.444 | 0.515 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.599 |
| colagnn_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.464 |
| flusight_baseline | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.582 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.077 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.574 |
| gnn_st_tuned | post_covid | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.588 |
| lstm_tuned | post_covid | 4 | 0.077 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.321 |
| persistence | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.588 |
| sarima | post_covid | 4 | 0.077 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.687 |
| xgboost_tuned | post_covid | 4 | 0.077 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.677 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 52 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 52 | 0.904 | 1.000 | 0.844 | -0.058 |
| xgboost_tuned | post_covid | 52 | 0.904 | 1.000 | 0.844 | -0.058 |
| gnn_st_nograph_tuned | post_covid | 52 | 0.885 | 1.000 | 0.797 | -0.077 |
| blend_baseline | post_covid | 52 | 0.865 | 1.000 | 0.800 | -0.019 |
| sarima | post_covid | 52 | 0.865 | 1.000 | 0.800 | -0.019 |
| flusight_baseline | post_covid | 52 | 0.846 | 1.000 | 0.775 | 0.000 |
| lstm_tuned | post_covid | 52 | 0.846 | 0.981 | 0.522 | -0.173 |
| persistence | post_covid | 52 | 0.846 | 1.000 | 0.775 | 0.000 |
| colagnn_tuned | post_covid | 52 | 0.827 | 1.000 | 0.625 | -0.135 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nograph_tuned | post_covid | 9 | 0.346 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.608 | 0.448 |
| gnn_st_tuned | post_covid | 9 | 0.346 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.608 | 0.478 |
| xgboost_tuned | post_covid | 9 | 0.346 | 6 | 3 | 1 | 0.667 | 0.143 | 0.600 | 0.750 | 0.608 | 0.452 |
| blend_baseline | post_covid | 9 | 0.346 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.549 | 0.471 |
| sarima | post_covid | 9 | 0.346 | 6 | 3 | 2 | 0.667 | 0.250 | 0.545 | 0.706 | 0.549 | 0.487 |
| colagnn_tuned | post_covid | 9 | 0.346 | 5 | 4 | 1 | 0.556 | 0.167 | 0.500 | 0.667 | 0.497 | 0.424 |
| flusight_baseline | post_covid | 9 | 0.346 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.490 | 0.411 |
| persistence | post_covid | 9 | 0.346 | 6 | 3 | 3 | 0.667 | 0.333 | 0.500 | 0.667 | 0.490 | 0.430 |
| lstm_tuned | post_covid | 9 | 0.346 | 4 | 5 | 0 | 0.444 | 0.000 | 0.444 | 0.615 | 0.444 | 0.387 |

### Crossing IT90 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.562 |
| colagnn_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.415 |
| flusight_baseline | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.545 |
| gnn_st_nograph_tuned | post_covid | 4 | 0.154 | 2 | 2 | 0 | 0.500 | 0.000 | 0.500 | 0.667 | 0.500 | 0.535 |
| gnn_st_tuned | post_covid | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.551 |
| lstm_tuned | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.259 |
| persistence | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.550 |
| sarima | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.659 |
| xgboost_tuned | post_covid | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.647 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| colagnn_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| flusight_baseline | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_nograph_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_st_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| sarima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| xgboost_tuned | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 26 | 0.808 | 1.000 | 0.815 | -0.115 |
| xgboost_tuned | post_covid | 26 | 0.808 | 1.000 | 0.815 | -0.115 |
| gnn_st_nograph_tuned | post_covid | 26 | 0.769 | 1.000 | 0.760 | -0.154 |
| blend_baseline | post_covid | 26 | 0.731 | 1.000 | 0.759 | -0.038 |
| sarima | post_covid | 26 | 0.731 | 1.000 | 0.759 | -0.038 |
| flusight_baseline | post_covid | 26 | 0.692 | 1.000 | 0.724 | 0.000 |
| lstm_tuned | post_covid | 26 | 0.692 | 0.962 | 0.476 | -0.346 |
| persistence | post_covid | 26 | 0.692 | 1.000 | 0.724 | 0.000 |
| colagnn_tuned | post_covid | 26 | 0.654 | 1.000 | 0.571 | -0.269 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 183 | 0.188 | 145 | 38 | 32 | 0.792 | 0.181 | 0.674 | 0.806 | 0.752 | 0.652 |
| flusight_baseline | post_covid | 183 | 0.188 | 146 | 37 | 37 | 0.798 | 0.202 | 0.664 | 0.798 | 0.751 | 0.625 |
| persistence | post_covid | 183 | 0.188 | 146 | 37 | 37 | 0.798 | 0.202 | 0.664 | 0.798 | 0.751 | 0.633 |
| gnn_st_tuned | post_covid | 183 | 0.188 | 136 | 47 | 23 | 0.743 | 0.145 | 0.660 | 0.795 | 0.714 | 0.655 |
| gnn_st_nograph_tuned | post_covid | 183 | 0.188 | 134 | 49 | 25 | 0.732 | 0.157 | 0.644 | 0.784 | 0.701 | 0.654 |
| lstm_tuned | post_covid | 183 | 0.188 | 124 | 59 | 21 | 0.678 | 0.145 | 0.608 | 0.756 | 0.651 | 0.617 |
| colagnn_tuned | post_covid | 183 | 0.188 | 115 | 68 | 14 | 0.628 | 0.109 | 0.584 | 0.737 | 0.611 | 0.548 |
| sarima | post_covid | 183 | 0.188 | 124 | 59 | 72 | 0.678 | 0.367 | 0.486 | 0.654 | 0.586 | 0.241 |
| xgboost_tuned | post_covid | 183 | 0.188 | 106 | 77 | 57 | 0.579 | 0.350 | 0.442 | 0.613 | 0.507 | 0.323 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 76 | 0.078 | 57 | 19 | 19 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.537 |
| persistence | post_covid | 76 | 0.078 | 57 | 19 | 19 | 0.750 | 0.250 | 0.600 | 0.750 | 0.729 | 0.549 |
| blend_baseline | post_covid | 76 | 0.078 | 55 | 21 | 17 | 0.724 | 0.236 | 0.591 | 0.743 | 0.705 | 0.566 |
| gnn_st_nograph_tuned | post_covid | 76 | 0.078 | 49 | 27 | 13 | 0.645 | 0.210 | 0.551 | 0.710 | 0.630 | 0.558 |
| gnn_st_tuned | post_covid | 76 | 0.078 | 48 | 28 | 13 | 0.632 | 0.213 | 0.539 | 0.701 | 0.617 | 0.561 |
| lstm_tuned | post_covid | 76 | 0.078 | 45 | 31 | 9 | 0.592 | 0.167 | 0.529 | 0.692 | 0.582 | 0.547 |
| sarima | post_covid | 76 | 0.078 | 41 | 35 | 49 | 0.539 | 0.544 | 0.328 | 0.494 | 0.485 | -0.012 |
| xgboost_tuned | post_covid | 76 | 0.078 | 20 | 56 | 9 | 0.263 | 0.310 | 0.235 | 0.381 | 0.253 | 0.234 |
| colagnn_tuned | post_covid | 76 | 0.078 | 14 | 62 | 2 | 0.184 | 0.125 | 0.179 | 0.304 | 0.182 | 0.341 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.041 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.609 | 0.401 |
| persistence | post_covid | 40 | 0.041 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.609 | 0.429 |
| blend_baseline | post_covid | 40 | 0.041 | 22 | 18 | 13 | 0.550 | 0.371 | 0.415 | 0.587 | 0.536 | 0.435 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.041 | 19 | 21 | 11 | 0.475 | 0.367 | 0.373 | 0.543 | 0.463 | 0.398 |
| gnn_st_tuned | post_covid | 40 | 0.041 | 17 | 23 | 7 | 0.425 | 0.292 | 0.362 | 0.531 | 0.417 | 0.396 |
| lstm_tuned | post_covid | 40 | 0.041 | 16 | 24 | 8 | 0.400 | 0.333 | 0.333 | 0.500 | 0.391 | 0.372 |
| sarima | post_covid | 40 | 0.041 | 14 | 26 | 44 | 0.350 | 0.759 | 0.167 | 0.286 | 0.303 | -0.448 |
| xgboost_tuned | post_covid | 40 | 0.041 | 3 | 37 | 2 | 0.075 | 0.400 | 0.071 | 0.133 | 0.073 | 0.139 |
| colagnn_tuned | post_covid | 40 | 0.041 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.211 |

### All four bands — 972 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 972 | 0.874 | 0.986 | 0.822 | -0.015 |
| flusight_baseline | post_covid | 972 | 0.872 | 0.985 | 0.823 | 0.000 |
| gnn_st_tuned | post_covid | 972 | 0.872 | 0.986 | 0.804 | -0.057 |
| persistence | post_covid | 972 | 0.872 | 0.985 | 0.823 | 0.000 |
| gnn_st_nograph_tuned | post_covid | 972 | 0.869 | 0.984 | 0.800 | -0.049 |
| lstm_tuned | post_covid | 972 | 0.863 | 0.984 | 0.782 | -0.078 |
| colagnn_tuned | post_covid | 972 | 0.845 | 0.966 | 0.628 | -0.158 |
| sarima | post_covid | 972 | 0.813 | 0.935 | 0.506 | 0.046 |
| xgboost_tuned | post_covid | 972 | 0.812 | 0.959 | 0.506 | -0.105 |

## Flu season (Apr–Sep)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 165 | 0.334 | 133 | 32 | 24 | 0.806 | 0.153 | 0.704 | 0.826 | 0.733 | 0.621 |
| flusight_baseline | post_covid | 165 | 0.334 | 134 | 31 | 27 | 0.812 | 0.168 | 0.698 | 0.822 | 0.730 | 0.611 |
| persistence | post_covid | 165 | 0.334 | 134 | 31 | 27 | 0.812 | 0.168 | 0.698 | 0.822 | 0.730 | 0.615 |
| gnn_st_tuned | post_covid | 165 | 0.334 | 126 | 39 | 20 | 0.764 | 0.137 | 0.681 | 0.810 | 0.703 | 0.613 |
| gnn_st_nograph_tuned | post_covid | 165 | 0.334 | 124 | 41 | 21 | 0.752 | 0.145 | 0.667 | 0.800 | 0.688 | 0.614 |
| lstm_tuned | post_covid | 165 | 0.334 | 114 | 51 | 15 | 0.691 | 0.116 | 0.633 | 0.776 | 0.645 | 0.576 |
| colagnn_tuned | post_covid | 165 | 0.334 | 112 | 53 | 14 | 0.679 | 0.111 | 0.626 | 0.770 | 0.636 | 0.512 |
| sarima | post_covid | 165 | 0.334 | 119 | 46 | 55 | 0.721 | 0.316 | 0.541 | 0.702 | 0.554 | 0.221 |
| xgboost_tuned | post_covid | 165 | 0.334 | 99 | 66 | 52 | 0.600 | 0.344 | 0.456 | 0.627 | 0.442 | 0.231 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 74 | 0.150 | 55 | 19 | 18 | 0.743 | 0.247 | 0.598 | 0.748 | 0.700 | 0.510 |
| persistence | post_covid | 74 | 0.150 | 55 | 19 | 18 | 0.743 | 0.247 | 0.598 | 0.748 | 0.700 | 0.529 |
| blend_baseline | post_covid | 74 | 0.150 | 53 | 21 | 16 | 0.716 | 0.232 | 0.589 | 0.741 | 0.678 | 0.535 |
| gnn_st_nograph_tuned | post_covid | 74 | 0.150 | 48 | 26 | 13 | 0.649 | 0.213 | 0.552 | 0.711 | 0.618 | 0.521 |
| gnn_st_tuned | post_covid | 74 | 0.150 | 48 | 26 | 13 | 0.649 | 0.213 | 0.552 | 0.711 | 0.618 | 0.527 |
| lstm_tuned | post_covid | 74 | 0.150 | 43 | 31 | 8 | 0.581 | 0.157 | 0.524 | 0.688 | 0.562 | 0.509 |
| sarima | post_covid | 74 | 0.150 | 41 | 33 | 38 | 0.554 | 0.481 | 0.366 | 0.536 | 0.464 | 0.063 |
| xgboost_tuned | post_covid | 74 | 0.150 | 20 | 54 | 9 | 0.270 | 0.310 | 0.241 | 0.388 | 0.249 | 0.204 |
| colagnn_tuned | post_covid | 74 | 0.150 | 14 | 60 | 2 | 0.189 | 0.125 | 0.184 | 0.311 | 0.184 | 0.309 |

### Crossing IT98

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| flusight_baseline | post_covid | 40 | 0.081 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.592 | 0.388 |
| persistence | post_covid | 40 | 0.081 | 25 | 15 | 15 | 0.625 | 0.375 | 0.455 | 0.625 | 0.592 | 0.415 |
| blend_baseline | post_covid | 40 | 0.081 | 22 | 18 | 13 | 0.550 | 0.371 | 0.415 | 0.587 | 0.521 | 0.412 |
| gnn_st_nograph_tuned | post_covid | 40 | 0.081 | 19 | 21 | 11 | 0.475 | 0.367 | 0.373 | 0.543 | 0.451 | 0.372 |
| gnn_st_tuned | post_covid | 40 | 0.081 | 17 | 23 | 7 | 0.425 | 0.292 | 0.362 | 0.531 | 0.410 | 0.370 |
| lstm_tuned | post_covid | 40 | 0.081 | 16 | 24 | 8 | 0.400 | 0.333 | 0.333 | 0.500 | 0.382 | 0.345 |
| sarima | post_covid | 40 | 0.081 | 14 | 26 | 35 | 0.350 | 0.714 | 0.187 | 0.315 | 0.273 | -0.279 |
| xgboost_tuned | post_covid | 40 | 0.081 | 3 | 37 | 2 | 0.075 | 0.400 | 0.071 | 0.133 | 0.071 | 0.109 |
| colagnn_tuned | post_covid | 40 | 0.081 | 0 | 40 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.179 |

### All four bands — 494 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| blend_baseline | post_covid | 494 | 0.783 | 0.972 | 0.803 | -0.036 |
| flusight_baseline | post_covid | 494 | 0.783 | 0.970 | 0.805 | -0.010 |
| persistence | post_covid | 494 | 0.783 | 0.970 | 0.805 | -0.010 |
| gnn_st_tuned | post_covid | 494 | 0.775 | 0.972 | 0.783 | -0.097 |
| gnn_st_nograph_tuned | post_covid | 494 | 0.769 | 0.968 | 0.778 | -0.087 |
| lstm_tuned | post_covid | 494 | 0.761 | 0.968 | 0.761 | -0.152 |
| colagnn_tuned | post_covid | 494 | 0.729 | 0.933 | 0.595 | -0.277 |
| sarima | post_covid | 494 | 0.692 | 0.899 | 0.493 | 0.047 |
| xgboost_tuned | post_covid | 494 | 0.662 | 0.923 | 0.445 | -0.190 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_tuned | post_covid | 15 | 1.000 | -1.000 | 0.933 | 1.000 | -5.843 |
| flusight_baseline | post_covid | 16 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| gnn_st_nograph_tuned | post_covid | 15 | 1.000 | -1.000 | 1.000 | 1.000 | -3.555 |
| persistence | post_covid | 16 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| blend_baseline | post_covid | 16 | 1.000 | -1.000 | 1.062 | 1.000 | -2.286 |
| lstm_tuned | post_covid | 15 | 1.000 | -1.000 | 1.267 | 1.000 | -4.053 |
| colagnn_tuned | post_covid | 14 | 1.000 | -1.000 | 2.000 | 1.000 | -12.380 |
| sarima | post_covid | 14 | 0.000 | 0.000 | 2.500 | 1.000 | -2.911 |
| xgboost_tuned | post_covid | 15 | 0.000 | 0.000 | 3.467 | 1.000 | -7.439 |

# Notes

- 25 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
