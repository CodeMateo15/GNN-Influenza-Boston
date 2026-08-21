Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 1, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.598 |
| dualtopo | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.078 |
| dualtopo_no_bg | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.077 |
| gnn_corrbinary | post_covid | 4 | 0.082 | 3 | 1 | 7 | 0.750 | 0.700 | 0.273 | 0.429 | 0.594 | -0.117 |
| gnn_geo | post_covid | 4 | 0.082 | 3 | 1 | 12 | 0.750 | 0.800 | 0.188 | 0.316 | 0.483 | -0.838 |
| gnn_multiedge | post_covid | 4 | 0.082 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.486 |
| gnn_multiedge_covid_rsv | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.720 |
| gnn_multiedge_leaknorm | post_covid | 4 | 0.082 | 4 | 0 | 10 | 1.000 | 0.714 | 0.286 | 0.444 | 0.778 | -0.743 |
| gnn_multiedge_level | post_covid | 4 | 0.082 | 3 | 1 | 17 | 0.750 | 0.850 | 0.143 | 0.250 | 0.372 | -2.857 |
| gnn_multiedge_rt | post_covid | 4 | 0.082 | 3 | 1 | 8 | 0.750 | 0.727 | 0.250 | 0.400 | 0.572 | -0.301 |
| gnn_multiedge_season | post_covid | 4 | 0.082 | 3 | 1 | 3 | 0.750 | 0.500 | 0.429 | 0.600 | 0.683 | 0.232 |
| gnn_multiedge_season_level | post_covid | 4 | 0.082 | 4 | 0 | 14 | 1.000 | 0.778 | 0.222 | 0.364 | 0.689 | -2.697 |
| gnn_uniform | post_covid | 4 | 0.082 | 3 | 1 | 3 | 0.750 | 0.500 | 0.429 | 0.600 | 0.683 | 0.216 |
| lstm | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.595 |
| persistence | post_covid | 4 | 0.082 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.728 | 0.584 |
| seasonal_naive | post_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.489 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.212 |
| dualtopo | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| dualtopo_no_bg | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gnn_corrbinary | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.502 |
| gnn_geo | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.679 |
| gnn_multiedge | post_covid | 1 | 0.020 | 1 | 0 | 1 | 1.000 | 0.500 | 0.500 | 0.667 | 0.979 | -0.230 |
| gnn_multiedge_covid_rsv | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.350 |
| gnn_multiedge_leaknorm | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.866 |
| gnn_multiedge_level | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -2.481 |
| gnn_multiedge_rt | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.628 |
| gnn_multiedge_season | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.426 |
| gnn_multiedge_season_level | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -2.087 |
| gnn_uniform | post_covid | 1 | 0.020 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.958 | -0.763 |
| lstm | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.073 |
| persistence | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.296 |
| seasonal_naive | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.502 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo_no_bg | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_corrbinary | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_geo | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_covid_rsv | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_leaknorm | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_rt | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_season | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_season_level | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_uniform | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 49 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge | post_covid | 49 | 0.959 | 0.980 | 0.747 | 0.020 |
| arima | post_covid | 49 | 0.939 | 1.000 | 0.705 | -0.020 |
| lstm | post_covid | 49 | 0.939 | 1.000 | 0.705 | -0.020 |
| dualtopo | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| dualtopo_no_bg | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| gnn_multiedge_covid_rsv | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| persistence | post_covid | 49 | 0.918 | 1.000 | 0.692 | 0.000 |
| gnn_multiedge_season | post_covid | 49 | 0.878 | 0.980 | 0.639 | 0.102 |
| gnn_uniform | post_covid | 49 | 0.878 | 0.980 | 0.639 | 0.102 |
| gnn_corrbinary | post_covid | 49 | 0.796 | 0.980 | 0.538 | 0.184 |
| seasonal_naive | post_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |
| gnn_multiedge_rt | post_covid | 49 | 0.776 | 0.980 | 0.516 | 0.204 |
| gnn_multiedge_leaknorm | post_covid | 49 | 0.755 | 0.980 | 0.521 | 0.265 |
| gnn_geo | post_covid | 49 | 0.694 | 0.980 | 0.440 | 0.286 |
| gnn_multiedge_season_level | post_covid | 49 | 0.673 | 0.980 | 0.449 | 0.347 |
| gnn_multiedge_level | post_covid | 49 | 0.592 | 1.000 | 0.222 | 0.327 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.564 |
| dualtopo | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.170 |
| dualtopo_no_bg | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.169 |
| gnn_corrbinary | post_covid | 4 | 0.154 | 3 | 1 | 5 | 0.750 | 0.625 | 0.333 | 0.500 | 0.523 | 0.154 |
| gnn_geo | post_covid | 4 | 0.154 | 3 | 1 | 7 | 0.750 | 0.700 | 0.273 | 0.429 | 0.432 | -0.330 |
| gnn_multiedge | post_covid | 4 | 0.154 | 3 | 1 | 0 | 0.750 | 0.000 | 0.750 | 0.857 | 0.750 | 0.590 |
| gnn_multiedge_covid_rsv | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.700 |
| gnn_multiedge_leaknorm | post_covid | 4 | 0.154 | 4 | 0 | 5 | 1.000 | 0.556 | 0.444 | 0.615 | 0.773 | -0.057 |
| gnn_multiedge_level | post_covid | 4 | 0.154 | 3 | 1 | 12 | 0.750 | 0.800 | 0.188 | 0.316 | 0.205 | -1.778 |
| gnn_multiedge_rt | post_covid | 4 | 0.154 | 3 | 1 | 5 | 0.750 | 0.625 | 0.333 | 0.500 | 0.523 | -0.007 |
| gnn_multiedge_season | post_covid | 4 | 0.154 | 3 | 1 | 3 | 0.750 | 0.500 | 0.429 | 0.600 | 0.614 | 0.334 |
| gnn_multiedge_season_level | post_covid | 4 | 0.154 | 4 | 0 | 9 | 1.000 | 0.692 | 0.308 | 0.471 | 0.591 | -1.651 |
| gnn_uniform | post_covid | 4 | 0.154 | 3 | 1 | 2 | 0.750 | 0.400 | 0.500 | 0.667 | 0.659 | 0.422 |
| lstm | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.560 |
| persistence | post_covid | 4 | 0.154 | 3 | 1 | 1 | 0.750 | 0.250 | 0.600 | 0.750 | 0.705 | 0.548 |
| seasonal_naive | post_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.610 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.235 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| dualtopo_no_bg | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gnn_corrbinary | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.527 |
| gnn_geo | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.700 |
| gnn_multiedge | post_covid | 1 | 0.038 | 1 | 0 | 1 | 1.000 | 0.500 | 0.500 | 0.667 | 0.960 | -0.253 |
| gnn_multiedge_covid_rsv | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.376 |
| gnn_multiedge_leaknorm | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.825 |
| gnn_multiedge_level | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -1.510 |
| gnn_multiedge_rt | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.657 |
| gnn_multiedge_season | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.452 |
| gnn_multiedge_season_level | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -1.708 |
| gnn_uniform | post_covid | 1 | 0.038 | 1 | 0 | 2 | 1.000 | 0.667 | 0.333 | 0.500 | 0.920 | -0.795 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.093 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.321 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.548 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo_no_bg | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_corrbinary | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_geo | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_covid_rsv | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_leaknorm | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_rt | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_season | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge_season_level | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_uniform | post_covid | 0 | 0.000 | 0 | 0 | 1 |  | 1.000 | 0.000 | 0.000 |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge | post_covid | 26 | 0.923 | 0.962 | 0.733 | 0.038 |
| arima | post_covid | 26 | 0.885 | 1.000 | 0.683 | -0.038 |
| lstm | post_covid | 26 | 0.885 | 1.000 | 0.683 | -0.038 |
| dualtopo | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| dualtopo_no_bg | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| gnn_multiedge_covid_rsv | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| persistence | post_covid | 26 | 0.846 | 1.000 | 0.669 | 0.000 |
| gnn_uniform | post_covid | 26 | 0.808 | 0.962 | 0.645 | 0.154 |
| gnn_multiedge_season | post_covid | 26 | 0.769 | 0.962 | 0.611 | 0.192 |
| gnn_multiedge_leaknorm | post_covid | 26 | 0.731 | 0.962 | 0.600 | 0.308 |
| gnn_corrbinary | post_covid | 26 | 0.692 | 0.962 | 0.549 | 0.269 |
| gnn_multiedge_rt | post_covid | 26 | 0.692 | 0.962 | 0.549 | 0.269 |
| gnn_geo | post_covid | 26 | 0.615 | 0.962 | 0.492 | 0.346 |
| seasonal_naive | post_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |
| gnn_multiedge_season_level | post_covid | 26 | 0.577 | 0.962 | 0.490 | 0.462 |
| gnn_multiedge_level | post_covid | 26 | 0.423 | 1.000 | 0.204 | 0.423 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 51 | 0.081 | 44 | 7 | 56 | 0.863 | 0.560 | 0.411 | 0.583 | 0.766 | 0.045 |
| gnn_uniform | post_covid | 51 | 0.081 | 43 | 8 | 55 | 0.843 | 0.561 | 0.406 | 0.577 | 0.748 | 0.092 |
| gnn_multiedge | post_covid | 51 | 0.081 | 41 | 10 | 34 | 0.804 | 0.453 | 0.482 | 0.651 | 0.745 | 0.271 |
| lstm | post_covid | 51 | 0.081 | 38 | 13 | 9 | 0.745 | 0.191 | 0.633 | 0.776 | 0.729 | 0.591 |
| gnn_multiedge_covid_rsv | post_covid | 51 | 0.081 | 38 | 13 | 12 | 0.745 | 0.240 | 0.603 | 0.752 | 0.724 | 0.538 |
| gnn_corrbinary | post_covid | 51 | 0.081 | 45 | 6 | 97 | 0.882 | 0.683 | 0.304 | 0.466 | 0.714 | -0.270 |
| persistence | post_covid | 51 | 0.081 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.680 | 0.528 |
| arima | post_covid | 51 | 0.081 | 35 | 16 | 10 | 0.686 | 0.222 | 0.574 | 0.729 | 0.669 | 0.529 |
| gnn_multiedge_rt | post_covid | 51 | 0.081 | 43 | 8 | 101 | 0.843 | 0.701 | 0.283 | 0.441 | 0.668 | -0.397 |
| gnn_multiedge_leaknorm | post_covid | 51 | 0.081 | 45 | 6 | 129 | 0.882 | 0.741 | 0.250 | 0.400 | 0.658 | -0.811 |
| gnn_multiedge_season_level | post_covid | 51 | 0.081 | 49 | 2 | 199 | 0.961 | 0.802 | 0.196 | 0.328 | 0.615 | -2.696 |
| gnn_geo | post_covid | 51 | 0.081 | 44 | 7 | 150 | 0.863 | 0.773 | 0.219 | 0.359 | 0.602 | -0.864 |
| gnn_multiedge_level | post_covid | 51 | 0.081 | 41 | 10 | 228 | 0.804 | 0.848 | 0.147 | 0.256 | 0.408 | -2.827 |
| dualtopo | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |
| dualtopo_no_bg | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.057 |
| seasonal_naive | post_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.545 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 18 | 0.029 | 15 | 3 | 23 | 0.833 | 0.605 | 0.366 | 0.536 | 0.796 | -0.779 |
| gnn_multiedge_leaknorm | post_covid | 18 | 0.029 | 15 | 3 | 24 | 0.833 | 0.615 | 0.357 | 0.526 | 0.794 | -0.368 |
| gnn_multiedge_season | post_covid | 18 | 0.029 | 12 | 6 | 18 | 0.667 | 0.600 | 0.333 | 0.500 | 0.637 | -0.011 |
| gnn_corrbinary | post_covid | 18 | 0.029 | 12 | 6 | 19 | 0.667 | 0.613 | 0.324 | 0.490 | 0.635 | -0.053 |
| gnn_geo | post_covid | 18 | 0.029 | 11 | 7 | 18 | 0.611 | 0.621 | 0.306 | 0.468 | 0.582 | -0.144 |
| gnn_multiedge_rt | post_covid | 18 | 0.029 | 10 | 8 | 18 | 0.556 | 0.643 | 0.278 | 0.435 | 0.526 | -0.083 |
| gnn_uniform | post_covid | 18 | 0.029 | 10 | 8 | 21 | 0.556 | 0.677 | 0.256 | 0.408 | 0.521 | -0.095 |
| gnn_multiedge_covid_rsv | post_covid | 18 | 0.029 | 9 | 9 | 9 | 0.500 | 0.500 | 0.333 | 0.500 | 0.485 | 0.213 |
| gnn_multiedge | post_covid | 18 | 0.029 | 9 | 9 | 13 | 0.500 | 0.591 | 0.290 | 0.450 | 0.479 | 0.129 |
| persistence | post_covid | 18 | 0.029 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.428 | 0.205 |
| arima | post_covid | 18 | 0.029 | 6 | 12 | 7 | 0.333 | 0.538 | 0.240 | 0.387 | 0.322 | 0.183 |
| gnn_multiedge_level | post_covid | 18 | 0.029 | 5 | 13 | 16 | 0.278 | 0.762 | 0.147 | 0.256 | 0.252 | -0.878 |
| dualtopo | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.030 |
| dualtopo_no_bg | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| lstm | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.221 |
| seasonal_naive | post_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.934 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.263 |
| dualtopo | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| dualtopo_no_bg | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gnn_corrbinary | post_covid | 2 | 0.003 | 1 | 1 | 10 | 0.500 | 0.909 | 0.083 | 0.154 | 0.484 | -2.773 |
| gnn_geo | post_covid | 2 | 0.003 | 1 | 1 | 11 | 0.500 | 0.917 | 0.077 | 0.143 | 0.482 | -2.499 |
| gnn_multiedge | post_covid | 2 | 0.003 | 1 | 1 | 6 | 0.500 | 0.857 | 0.125 | 0.222 | 0.490 | -1.301 |
| gnn_multiedge_covid_rsv | post_covid | 2 | 0.003 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.498 | -0.114 |
| gnn_multiedge_leaknorm | post_covid | 2 | 0.003 | 1 | 1 | 15 | 0.500 | 0.938 | 0.059 | 0.111 | 0.476 | -5.397 |
| gnn_multiedge_level | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gnn_multiedge_rt | post_covid | 2 | 0.003 | 1 | 1 | 12 | 0.500 | 0.923 | 0.071 | 0.133 | 0.481 | -3.342 |
| gnn_multiedge_season | post_covid | 2 | 0.003 | 1 | 1 | 10 | 0.500 | 0.909 | 0.083 | 0.154 | 0.484 | -2.929 |
| gnn_multiedge_season_level | post_covid | 2 | 0.003 | 1 | 1 | 11 | 0.500 | 0.917 | 0.077 | 0.143 | 0.482 | -3.059 |
| gnn_uniform | post_covid | 2 | 0.003 | 1 | 1 | 12 | 0.500 | 0.923 | 0.071 | 0.133 | 0.481 | -3.469 |
| lstm | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.024 |
| persistence | post_covid | 2 | 0.003 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.498 | -0.260 |
| seasonal_naive | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.871 |

### All four bands — 627 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 627 | 0.939 | 0.994 | 0.670 | -0.038 |
| arima | post_covid | 627 | 0.936 | 0.990 | 0.661 | -0.021 |
| gnn_multiedge_covid_rsv | post_covid | 627 | 0.936 | 0.992 | 0.742 | -0.002 |
| persistence | post_covid | 627 | 0.928 | 0.990 | 0.682 | 0.000 |
| dualtopo | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| dualtopo_no_bg | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| gnn_multiedge | post_covid | 627 | 0.893 | 0.990 | 0.682 | 0.053 |
| gnn_multiedge_season | post_covid | 627 | 0.856 | 0.987 | 0.653 | 0.112 |
| gnn_uniform | post_covid | 627 | 0.850 | 0.982 | 0.625 | 0.113 |
| seasonal_naive | post_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |
| gnn_corrbinary | post_covid | 627 | 0.791 | 0.987 | 0.573 | 0.180 |
| gnn_multiedge_rt | post_covid | 627 | 0.778 | 0.986 | 0.547 | 0.182 |
| gnn_multiedge_leaknorm | post_covid | 627 | 0.740 | 0.976 | 0.521 | 0.252 |
| gnn_geo | post_covid | 627 | 0.703 | 0.987 | 0.479 | 0.262 |
| gnn_multiedge_season_level | post_covid | 627 | 0.636 | 0.984 | 0.440 | 0.362 |
| gnn_multiedge_level | post_covid | 627 | 0.584 | 0.987 | 0.253 | 0.349 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_uniform | post_covid | 51 | 0.145 | 43 | 8 | 36 | 0.843 | 0.456 | 0.494 | 0.662 | 0.724 | 0.294 |
| lstm | post_covid | 51 | 0.145 | 38 | 13 | 9 | 0.745 | 0.191 | 0.633 | 0.776 | 0.715 | 0.561 |
| gnn_multiedge | post_covid | 51 | 0.145 | 41 | 10 | 28 | 0.804 | 0.406 | 0.519 | 0.683 | 0.711 | 0.385 |
| gnn_multiedge_covid_rsv | post_covid | 51 | 0.145 | 38 | 13 | 12 | 0.745 | 0.240 | 0.603 | 0.752 | 0.705 | 0.527 |
| gnn_multiedge_season | post_covid | 51 | 0.145 | 44 | 7 | 49 | 0.863 | 0.527 | 0.440 | 0.611 | 0.700 | 0.159 |
| gnn_multiedge_leaknorm | post_covid | 51 | 0.145 | 45 | 6 | 68 | 0.882 | 0.602 | 0.378 | 0.549 | 0.656 | -0.197 |
| persistence | post_covid | 51 | 0.145 | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.706 | 0.656 | 0.494 |
| arima | post_covid | 51 | 0.145 | 35 | 16 | 10 | 0.686 | 0.222 | 0.574 | 0.729 | 0.653 | 0.496 |
| gnn_corrbinary | post_covid | 51 | 0.145 | 45 | 6 | 73 | 0.882 | 0.619 | 0.363 | 0.533 | 0.640 | -0.022 |
| gnn_multiedge_rt | post_covid | 51 | 0.145 | 43 | 8 | 70 | 0.843 | 0.619 | 0.355 | 0.524 | 0.611 | -0.129 |
| gnn_geo | post_covid | 51 | 0.145 | 44 | 7 | 97 | 0.863 | 0.688 | 0.297 | 0.458 | 0.540 | -0.421 |
| gnn_multiedge_season_level | post_covid | 51 | 0.145 | 49 | 2 | 133 | 0.961 | 0.731 | 0.266 | 0.421 | 0.519 | -1.698 |
| gnn_multiedge_level | post_covid | 51 | 0.145 | 41 | 10 | 162 | 0.804 | 0.798 | 0.192 | 0.323 | 0.266 | -1.772 |
| dualtopo | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.131 |
| dualtopo_no_bg | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.130 |
| seasonal_naive | post_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.625 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 18 | 0.051 | 15 | 3 | 23 | 0.833 | 0.605 | 0.366 | 0.536 | 0.764 | -0.587 |
| gnn_multiedge_leaknorm | post_covid | 18 | 0.051 | 15 | 3 | 24 | 0.833 | 0.615 | 0.357 | 0.526 | 0.761 | -0.307 |
| gnn_multiedge_season | post_covid | 18 | 0.051 | 12 | 6 | 18 | 0.667 | 0.600 | 0.333 | 0.500 | 0.613 | -0.029 |
| gnn_corrbinary | post_covid | 18 | 0.051 | 12 | 6 | 19 | 0.667 | 0.613 | 0.324 | 0.490 | 0.610 | -0.060 |
| gnn_geo | post_covid | 18 | 0.051 | 11 | 7 | 18 | 0.611 | 0.621 | 0.306 | 0.468 | 0.557 | -0.143 |
| gnn_multiedge_rt | post_covid | 18 | 0.051 | 10 | 8 | 18 | 0.556 | 0.643 | 0.278 | 0.435 | 0.502 | -0.094 |
| gnn_uniform | post_covid | 18 | 0.051 | 10 | 8 | 21 | 0.556 | 0.677 | 0.256 | 0.408 | 0.493 | -0.111 |
| gnn_multiedge_covid_rsv | post_covid | 18 | 0.051 | 9 | 9 | 9 | 0.500 | 0.500 | 0.333 | 0.500 | 0.473 | 0.195 |
| gnn_multiedge | post_covid | 18 | 0.051 | 9 | 9 | 13 | 0.500 | 0.591 | 0.290 | 0.450 | 0.461 | 0.113 |
| persistence | post_covid | 18 | 0.051 | 8 | 10 | 10 | 0.444 | 0.556 | 0.286 | 0.444 | 0.415 | 0.187 |
| arima | post_covid | 18 | 0.051 | 6 | 12 | 7 | 0.333 | 0.538 | 0.240 | 0.387 | 0.312 | 0.164 |
| gnn_multiedge_level | post_covid | 18 | 0.051 | 5 | 13 | 12 | 0.278 | 0.706 | 0.167 | 0.286 | 0.242 | -0.398 |
| dualtopo | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| dualtopo_no_bg | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| lstm | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.202 |
| seasonal_naive | post_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -0.974 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.267 |
| dualtopo | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| dualtopo_no_bg | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gnn_corrbinary | post_covid | 2 | 0.006 | 1 | 1 | 10 | 0.500 | 0.909 | 0.083 | 0.154 | 0.471 | -2.780 |
| gnn_geo | post_covid | 2 | 0.006 | 1 | 1 | 11 | 0.500 | 0.917 | 0.077 | 0.143 | 0.469 | -2.504 |
| gnn_multiedge | post_covid | 2 | 0.006 | 1 | 1 | 6 | 0.500 | 0.857 | 0.125 | 0.222 | 0.483 | -1.306 |
| gnn_multiedge_covid_rsv | post_covid | 2 | 0.006 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.497 | -0.117 |
| gnn_multiedge_leaknorm | post_covid | 2 | 0.006 | 1 | 1 | 15 | 0.500 | 0.938 | 0.059 | 0.111 | 0.457 | -5.397 |
| gnn_multiedge_level | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.014 |
| gnn_multiedge_rt | post_covid | 2 | 0.006 | 1 | 1 | 12 | 0.500 | 0.923 | 0.071 | 0.133 | 0.466 | -3.351 |
| gnn_multiedge_season | post_covid | 2 | 0.006 | 1 | 1 | 10 | 0.500 | 0.909 | 0.083 | 0.154 | 0.471 | -2.938 |
| gnn_multiedge_season_level | post_covid | 2 | 0.006 | 1 | 1 | 11 | 0.500 | 0.917 | 0.077 | 0.143 | 0.469 | -3.055 |
| gnn_uniform | post_covid | 2 | 0.006 | 1 | 1 | 12 | 0.500 | 0.923 | 0.071 | 0.133 | 0.466 | -3.478 |
| lstm | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.021 |
| persistence | post_covid | 2 | 0.006 | 1 | 1 | 1 | 0.500 | 0.500 | 0.333 | 0.500 | 0.497 | -0.263 |
| seasonal_naive | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.880 |

### All four bands — 352 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 352 | 0.892 | 0.989 | 0.650 | -0.068 |
| arima | post_covid | 352 | 0.886 | 0.983 | 0.641 | -0.037 |
| gnn_multiedge_covid_rsv | post_covid | 352 | 0.886 | 0.986 | 0.726 | -0.003 |
| persistence | post_covid | 352 | 0.872 | 0.983 | 0.662 | 0.000 |
| dualtopo | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| dualtopo_no_bg | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| gnn_multiedge | post_covid | 352 | 0.827 | 0.983 | 0.678 | 0.077 |
| gnn_uniform | post_covid | 352 | 0.787 | 0.969 | 0.643 | 0.148 |
| gnn_multiedge_season | post_covid | 352 | 0.764 | 0.977 | 0.642 | 0.179 |
| gnn_multiedge_leaknorm | post_covid | 352 | 0.710 | 0.957 | 0.588 | 0.276 |
| gnn_corrbinary | post_covid | 352 | 0.696 | 0.977 | 0.586 | 0.253 |
| gnn_multiedge_rt | post_covid | 352 | 0.693 | 0.974 | 0.571 | 0.236 |
| seasonal_naive | post_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |
| gnn_geo | post_covid | 352 | 0.622 | 0.977 | 0.524 | 0.315 |
| gnn_multiedge_season_level | post_covid | 352 | 0.540 | 0.972 | 0.478 | 0.457 |
| gnn_multiedge_level | post_covid | 352 | 0.446 | 0.989 | 0.261 | 0.423 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 14 | 0.000 | 0.000 | 0.143 | 0.000 | 1.804 |
| gnn_corrbinary | post_covid | 14 | 0.000 | 0.000 | 0.429 | 1.000 | 6.570 |
| gnn_multiedge_leaknorm | post_covid | 14 | 0.000 | 0.000 | 0.429 | 1.000 | 10.854 |
| gnn_geo | post_covid | 14 | 0.500 | -0.500 | 0.500 | 1.000 | 6.388 |
| gnn_multiedge_season | post_covid | 14 | 0.500 | -0.500 | 0.500 | 1.000 | 7.088 |
| gnn_multiedge | post_covid | 14 | 1.000 | -1.000 | 0.571 | 1.000 | 5.563 |
| gnn_multiedge_rt | post_covid | 14 | 1.000 | -1.000 | 0.571 | 1.000 | 7.555 |
| gnn_uniform | post_covid | 14 | 1.000 | -1.000 | 0.571 | 1.000 | 7.299 |
| gnn_multiedge_level | post_covid | 14 | 1.000 | -1.000 | 0.714 | 0.000 | -0.145 |
| gnn_multiedge_covid_rsv | post_covid | 14 | 1.000 | -1.000 | 0.786 | 1.000 | 3.584 |
| lstm | post_covid | 13 | 1.000 | -1.000 | 0.846 | 0.000 | -4.406 |
| persistence | post_covid | 14 | 1.000 | -1.000 | 1.000 | 1.000 | 0.000 |
| arima | post_covid | 13 | 1.000 | -1.000 | 1.077 | 1.000 | 0.000 |
| seasonal_naive | post_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| dualtopo | post_covid | 0 |  |  |  | 3.000 | -4.281 |
| dualtopo_no_bg | post_covid | 0 |  |  |  | 3.000 | -4.258 |

# Notes

- IT98 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
