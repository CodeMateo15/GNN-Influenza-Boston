Severity thresholds from the 3 reference seasons 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31, levels IT50/IT90/IT98, 10 values per season (30 pooled). Horizon 4, ranked by **PSS**.

**PSS (Peirce skill score) leads these tables because it is 0 for both trivial forecasts.** At an 8% base rate, never alerting scores 92% accuracy and always alerting scores a perfect POD of 1.0; PSS gives both of them nothing. CSI and F1 sit beside it because PSS is measured against a large correct-negative count and moves little when a model raises many false alarms in absolute terms — CSI ignores correct negatives entirely and will show that.

Citywide thresholds: IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000.

# Citywide indicator

## Overall (full year)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.082 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | -0.104 |
| dualtopo | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| dualtopo_no_bg | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.076 |
| gnn_corrbinary | post_covid | 4 | 0.082 | 2 | 2 | 10 | 0.500 | 0.833 | 0.143 | 0.250 | 0.278 | -1.426 |
| gnn_geo | post_covid | 4 | 0.082 | 2 | 2 | 12 | 0.500 | 0.857 | 0.125 | 0.222 | 0.233 | -2.040 |
| gnn_multiedge | post_covid | 4 | 0.082 | 2 | 2 | 9 | 0.500 | 0.818 | 0.154 | 0.267 | 0.300 | -1.197 |
| gnn_multiedge_covid_rsv | post_covid | 4 | 0.082 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.326 |
| gnn_multiedge_leaknorm | post_covid | 4 | 0.082 | 1 | 3 | 11 | 0.250 | 0.917 | 0.067 | 0.125 | 0.006 | -1.716 |
| gnn_multiedge_level | post_covid | 4 | 0.082 | 2 | 2 | 11 | 0.500 | 0.846 | 0.133 | 0.235 | 0.256 | -1.925 |
| gnn_multiedge_rt | post_covid | 4 | 0.082 | 2 | 2 | 7 | 0.500 | 0.778 | 0.182 | 0.308 | 0.344 | -0.829 |
| gnn_multiedge_season | post_covid | 4 | 0.082 | 2 | 2 | 3 | 0.500 | 0.600 | 0.286 | 0.444 | 0.433 | -0.039 |
| gnn_multiedge_season_level | post_covid | 4 | 0.082 | 2 | 2 | 3 | 0.500 | 0.600 | 0.286 | 0.444 | 0.433 | -0.184 |
| gnn_uniform | post_covid | 4 | 0.082 | 2 | 2 | 10 | 0.500 | 0.833 | 0.143 | 0.250 | 0.278 | -1.610 |
| lstm | post_covid | 4 | 0.082 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.022 | -0.038 |
| persistence | post_covid | 4 | 0.082 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.089 | -0.420 |
| seasonal_naive | post_covid | 4 | 0.082 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.133 | -0.489 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.214 |
| dualtopo | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| dualtopo_no_bg | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.021 |
| gnn_corrbinary | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -1.179 |
| gnn_geo | post_covid | 1 | 0.020 | 0 | 1 | 10 | 0.000 | 1.000 | 0.000 | 0.000 | -0.208 | -5.144 |
| gnn_multiedge | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.394 |
| gnn_multiedge_covid_rsv | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.036 |
| gnn_multiedge_leaknorm | post_covid | 1 | 0.020 | 0 | 1 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.062 | -2.627 |
| gnn_multiedge_level | post_covid | 1 | 0.020 | 0 | 1 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.062 | -2.211 |
| gnn_multiedge_rt | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -0.934 |
| gnn_multiedge_season | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.666 |
| gnn_multiedge_season_level | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.294 |
| gnn_uniform | post_covid | 1 | 0.020 | 0 | 1 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.125 | -3.203 |
| lstm | post_covid | 1 | 0.020 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.041 |
| persistence | post_covid | 1 | 0.020 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.021 | -0.829 |
| seasonal_naive | post_covid | 1 | 0.020 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -1.502 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo_no_bg | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_corrbinary | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_geo | post_covid | 0 | 0.000 | 0 | 0 | 2 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_covid_rsv | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_leaknorm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_rt | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_season | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_season_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_uniform | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 49 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| dualtopo_no_bg | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| gnn_multiedge_covid_rsv | post_covid | 49 | 0.918 | 0.980 | 0.000 | -0.102 |
| arima | post_covid | 49 | 0.898 | 0.980 | -0.026 | -0.082 |
| gnn_multiedge_season | post_covid | 49 | 0.898 | 0.959 | 0.201 | 0.020 |
| gnn_multiedge_season_level | post_covid | 49 | 0.898 | 0.980 | 0.271 | 0.000 |
| lstm | post_covid | 49 | 0.898 | 0.980 | -0.026 | -0.082 |
| persistence | post_covid | 49 | 0.837 | 0.959 | -0.079 | 0.000 |
| gnn_multiedge_rt | post_covid | 49 | 0.816 | 0.939 | 0.089 | 0.122 |
| seasonal_naive | post_covid | 49 | 0.796 | 0.939 | -0.094 | 0.061 |
| gnn_multiedge | post_covid | 49 | 0.776 | 0.939 | 0.063 | 0.163 |
| gnn_corrbinary | post_covid | 49 | 0.755 | 0.980 | 0.094 | 0.143 |
| gnn_uniform | post_covid | 49 | 0.755 | 0.857 | 0.010 | 0.265 |
| gnn_multiedge_level | post_covid | 49 | 0.735 | 0.918 | 0.029 | 0.224 |
| gnn_geo | post_covid | 49 | 0.714 | 0.776 | -0.023 | 0.429 |
| gnn_multiedge_leaknorm | post_covid | 49 | 0.714 | 0.918 | -0.043 | 0.204 |

## Flu season (Oct–Mar)

### Crossing IT50 — **underpowered: 4 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | -0.113 |
| dualtopo | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| dualtopo_no_bg | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| gnn_corrbinary | post_covid | 4 | 0.154 | 2 | 2 | 5 | 0.500 | 0.714 | 0.222 | 0.364 | 0.273 | -0.616 |
| gnn_geo | post_covid | 4 | 0.154 | 2 | 2 | 7 | 0.500 | 0.778 | 0.182 | 0.308 | 0.182 | -1.160 |
| gnn_multiedge | post_covid | 4 | 0.154 | 2 | 2 | 5 | 0.500 | 0.714 | 0.222 | 0.364 | 0.273 | -0.600 |
| gnn_multiedge_covid_rsv | post_covid | 4 | 0.154 | 0 | 4 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.292 |
| gnn_multiedge_leaknorm | post_covid | 4 | 0.154 | 1 | 3 | 6 | 0.250 | 0.857 | 0.100 | 0.182 | -0.023 | -0.857 |
| gnn_multiedge_level | post_covid | 4 | 0.154 | 2 | 2 | 6 | 0.500 | 0.750 | 0.200 | 0.333 | 0.227 | -1.071 |
| gnn_multiedge_rt | post_covid | 4 | 0.154 | 2 | 2 | 6 | 0.500 | 0.750 | 0.200 | 0.333 | 0.227 | -0.838 |
| gnn_multiedge_season | post_covid | 4 | 0.154 | 2 | 2 | 3 | 0.500 | 0.600 | 0.286 | 0.444 | 0.364 | -0.099 |
| gnn_multiedge_season_level | post_covid | 4 | 0.154 | 2 | 2 | 3 | 0.500 | 0.600 | 0.286 | 0.444 | 0.364 | -0.262 |
| gnn_uniform | post_covid | 4 | 0.154 | 2 | 2 | 5 | 0.500 | 0.714 | 0.222 | 0.364 | 0.273 | -0.480 |
| lstm | post_covid | 4 | 0.154 | 0 | 4 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.045 | -0.096 |
| persistence | post_covid | 4 | 0.154 | 0 | 4 | 4 | 0.000 | 1.000 | 0.000 | 0.000 | -0.182 | -0.518 |
| seasonal_naive | post_covid | 4 | 0.154 | 0 | 4 | 6 | 0.000 | 1.000 | 0.000 | 0.000 | -0.273 | -0.610 |

### Crossing IT90 — **underpowered: 1 observed event**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.234 |
| dualtopo | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| dualtopo_no_bg | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.040 |
| gnn_corrbinary | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.663 |
| gnn_geo | post_covid | 1 | 0.038 | 0 | 1 | 5 | 0.000 | 1.000 | 0.000 | 0.000 | -0.200 | -3.096 |
| gnn_multiedge | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.228 |
| gnn_multiedge_covid_rsv | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.055 |
| gnn_multiedge_leaknorm | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.612 |
| gnn_multiedge_level | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.520 |
| gnn_multiedge_rt | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -0.967 |
| gnn_multiedge_season | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.698 |
| gnn_multiedge_season_level | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.319 |
| gnn_uniform | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -1.007 |
| lstm | post_covid | 1 | 0.038 | 0 | 1 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.060 |
| persistence | post_covid | 1 | 0.038 | 0 | 1 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.040 | -0.862 |
| seasonal_naive | post_covid | 1 | 0.038 | 0 | 1 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.080 | -1.548 |

### Crossing IT98 — **underpowered: 0 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| dualtopo_no_bg | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_corrbinary | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_geo | post_covid | 0 | 0.000 | 0 | 0 | 2 |  | 1.000 | 0.000 | 0.000 |  |  |
| gnn_multiedge | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_covid_rsv | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_leaknorm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_rt | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_season | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_multiedge_season_level | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| gnn_uniform | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| lstm | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| persistence | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |
| seasonal_naive | post_covid | 0 | 0.000 | 0 | 0 | 0 |  |  |  |  |  |  |

### All four bands — 26 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| dualtopo_no_bg | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| gnn_multiedge_covid_rsv | post_covid | 26 | 0.846 | 0.962 | 0.000 | -0.192 |
| arima | post_covid | 26 | 0.808 | 0.962 | -0.051 | -0.154 |
| gnn_multiedge_season | post_covid | 26 | 0.808 | 0.923 | 0.133 | 0.038 |
| gnn_multiedge_season_level | post_covid | 26 | 0.808 | 0.962 | 0.206 | 0.000 |
| lstm | post_covid | 26 | 0.808 | 0.962 | -0.051 | -0.154 |
| gnn_corrbinary | post_covid | 26 | 0.731 | 0.962 | 0.116 | 0.077 |
| gnn_multiedge | post_covid | 26 | 0.731 | 0.885 | 0.033 | 0.154 |
| gnn_uniform | post_covid | 26 | 0.731 | 0.923 | 0.066 | 0.115 |
| gnn_multiedge_level | post_covid | 26 | 0.692 | 0.885 | 0.009 | 0.192 |
| gnn_multiedge_rt | post_covid | 26 | 0.692 | 0.885 | 0.009 | 0.192 |
| persistence | post_covid | 26 | 0.692 | 0.923 | -0.159 | 0.000 |
| gnn_geo | post_covid | 26 | 0.654 | 0.769 | -0.062 | 0.423 |
| gnn_multiedge_leaknorm | post_covid | 26 | 0.654 | 0.885 | -0.088 | 0.154 |
| seasonal_naive | post_covid | 26 | 0.615 | 0.885 | -0.193 | 0.115 |

# All neighborhood-weeks pooled

## Overall (full year)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 51 | 0.081 | 27 | 24 | 42 | 0.529 | 0.609 | 0.290 | 0.450 | 0.456 | -0.176 |
| gnn_multiedge_season_level | post_covid | 51 | 0.081 | 27 | 24 | 46 | 0.529 | 0.630 | 0.278 | 0.435 | 0.450 | -0.188 |
| gnn_multiedge_level | post_covid | 51 | 0.081 | 27 | 24 | 150 | 0.529 | 0.847 | 0.134 | 0.237 | 0.269 | -1.862 |
| gnn_multiedge_rt | post_covid | 51 | 0.081 | 19 | 32 | 85 | 0.373 | 0.817 | 0.140 | 0.245 | 0.225 | -0.895 |
| gnn_uniform | post_covid | 51 | 0.081 | 22 | 29 | 137 | 0.431 | 0.862 | 0.117 | 0.210 | 0.194 | -1.592 |
| gnn_multiedge | post_covid | 51 | 0.081 | 21 | 30 | 126 | 0.412 | 0.857 | 0.119 | 0.212 | 0.193 | -1.175 |
| gnn_corrbinary | post_covid | 51 | 0.081 | 20 | 31 | 142 | 0.392 | 0.877 | 0.104 | 0.188 | 0.146 | -1.420 |
| gnn_multiedge_leaknorm | post_covid | 51 | 0.081 | 19 | 32 | 142 | 0.373 | 0.882 | 0.098 | 0.179 | 0.126 | -1.688 |
| gnn_geo | post_covid | 51 | 0.081 | 19 | 32 | 174 | 0.373 | 0.902 | 0.084 | 0.156 | 0.070 | -2.009 |
| gnn_multiedge_covid_rsv | post_covid | 51 | 0.081 | 4 | 47 | 10 | 0.078 | 0.714 | 0.066 | 0.123 | 0.061 | 0.156 |
| lstm | post_covid | 51 | 0.081 | 2 | 49 | 8 | 0.039 | 0.800 | 0.034 | 0.066 | 0.025 | -0.023 |
| dualtopo | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.056 |
| dualtopo_no_bg | post_covid | 51 | 0.081 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.056 |
| seasonal_naive | post_covid | 51 | 0.081 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.016 | -0.545 |
| arima | post_covid | 51 | 0.081 | 0 | 51 | 20 | 0.000 | 1.000 | 0.000 | 0.000 | -0.035 | -0.280 |
| persistence | post_covid | 51 | 0.081 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.046 | -0.481 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 18 | 0.029 | 1 | 17 | 7 | 0.056 | 0.875 | 0.040 | 0.077 | 0.044 | -0.201 |
| gnn_multiedge | post_covid | 18 | 0.029 | 1 | 17 | 21 | 0.056 | 0.955 | 0.026 | 0.050 | 0.021 | -0.803 |
| arima | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.200 |
| dualtopo | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| dualtopo_no_bg | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.029 |
| gnn_multiedge_covid_rsv | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.029 |
| gnn_multiedge_season_level | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.025 |
| lstm | post_covid | 18 | 0.029 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.019 |
| gnn_corrbinary | post_covid | 18 | 0.029 | 0 | 18 | 9 | 0.000 | 1.000 | 0.000 | 0.000 | -0.015 | -0.752 |
| gnn_multiedge_leaknorm | post_covid | 18 | 0.029 | 1 | 17 | 50 | 0.056 | 0.980 | 0.015 | 0.029 | -0.027 | -1.563 |
| persistence | post_covid | 18 | 0.029 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.030 | -0.615 |
| gnn_multiedge_rt | post_covid | 18 | 0.029 | 0 | 18 | 23 | 0.000 | 1.000 | 0.000 | 0.000 | -0.038 | -0.675 |
| gnn_multiedge_level | post_covid | 18 | 0.029 | 0 | 18 | 28 | 0.000 | 1.000 | 0.000 | 0.000 | -0.046 | -0.994 |
| seasonal_naive | post_covid | 18 | 0.029 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.056 | -0.934 |
| gnn_uniform | post_covid | 18 | 0.029 | 0 | 18 | 69 | 0.000 | 1.000 | 0.000 | 0.000 | -0.113 | -1.824 |
| gnn_geo | post_covid | 18 | 0.029 | 0 | 18 | 124 | 0.000 | 1.000 | 0.000 | 0.000 | -0.204 | -3.166 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.415 |
| dualtopo | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| dualtopo_no_bg | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.003 |
| gnn_corrbinary | post_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.768 |
| gnn_geo | post_covid | 2 | 0.003 | 0 | 2 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.029 | -9.654 |
| gnn_multiedge | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -1.276 |
| gnn_multiedge_covid_rsv | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.168 |
| gnn_multiedge_leaknorm | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -2.285 |
| gnn_multiedge_level | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.394 |
| gnn_multiedge_rt | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.703 |
| gnn_multiedge_season | post_covid | 2 | 0.003 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.002 | -0.627 |
| gnn_multiedge_season_level | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.032 |
| gnn_uniform | post_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -2.339 |
| lstm | post_covid | 2 | 0.003 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.015 |
| persistence | post_covid | 2 | 0.003 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -2.121 |
| seasonal_naive | post_covid | 2 | 0.003 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.005 | -3.871 |

### All four bands — 627 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| dualtopo_no_bg | post_covid | 627 | 0.919 | 0.971 | 0.000 | -0.113 |
| lstm | post_covid | 627 | 0.909 | 0.971 | 0.014 | -0.097 |
| gnn_multiedge_covid_rsv | post_covid | 627 | 0.907 | 0.973 | 0.054 | -0.091 |
| arima | post_covid | 627 | 0.887 | 0.971 | -0.035 | -0.081 |
| gnn_multiedge_season | post_covid | 627 | 0.879 | 0.976 | 0.329 | 0.011 |
| gnn_multiedge_season_level | post_covid | 627 | 0.872 | 0.986 | 0.347 | 0.003 |
| persistence | post_covid | 627 | 0.844 | 0.943 | -0.056 | 0.000 |
| gnn_multiedge_rt | post_covid | 627 | 0.804 | 0.944 | 0.082 | 0.089 |
| seasonal_naive | post_covid | 627 | 0.801 | 0.922 | -0.032 | 0.078 |
| gnn_multiedge | post_covid | 627 | 0.738 | 0.952 | 0.082 | 0.161 |
| gnn_uniform | post_covid | 627 | 0.719 | 0.877 | 0.027 | 0.254 |
| gnn_corrbinary | post_covid | 627 | 0.715 | 0.967 | 0.047 | 0.163 |
| gnn_multiedge_leaknorm | post_covid | 627 | 0.710 | 0.906 | 0.029 | 0.230 |
| gnn_multiedge_level | post_covid | 627 | 0.707 | 0.941 | 0.090 | 0.214 |
| gnn_geo | post_covid | 627 | 0.657 | 0.788 | -0.029 | 0.421 |

## Flu season (Oct–Mar)

### Crossing IT50

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 51 | 0.145 | 27 | 24 | 41 | 0.529 | 0.603 | 0.293 | 0.454 | 0.393 | -0.189 |
| gnn_multiedge_season_level | post_covid | 51 | 0.145 | 27 | 24 | 46 | 0.529 | 0.630 | 0.278 | 0.435 | 0.377 | -0.239 |
| gnn_multiedge_level | post_covid | 51 | 0.145 | 27 | 24 | 84 | 0.529 | 0.757 | 0.200 | 0.333 | 0.250 | -1.046 |
| gnn_uniform | post_covid | 51 | 0.145 | 22 | 29 | 71 | 0.431 | 0.763 | 0.180 | 0.306 | 0.195 | -0.520 |
| gnn_multiedge | post_covid | 51 | 0.145 | 21 | 30 | 71 | 0.412 | 0.772 | 0.172 | 0.294 | 0.176 | -0.619 |
| gnn_corrbinary | post_covid | 51 | 0.145 | 20 | 31 | 76 | 0.392 | 0.792 | 0.157 | 0.272 | 0.140 | -0.676 |
| gnn_multiedge_rt | post_covid | 51 | 0.145 | 19 | 32 | 77 | 0.373 | 0.802 | 0.148 | 0.259 | 0.117 | -0.880 |
| gnn_multiedge_leaknorm | post_covid | 51 | 0.145 | 19 | 32 | 78 | 0.373 | 0.804 | 0.147 | 0.257 | 0.113 | -0.876 |
| gnn_multiedge_covid_rsv | post_covid | 51 | 0.145 | 4 | 47 | 10 | 0.078 | 0.714 | 0.066 | 0.123 | 0.045 | 0.147 |
| gnn_geo | post_covid | 51 | 0.145 | 19 | 32 | 108 | 0.373 | 0.850 | 0.119 | 0.213 | 0.014 | -1.167 |
| lstm | post_covid | 51 | 0.145 | 2 | 49 | 8 | 0.039 | 0.800 | 0.034 | 0.066 | 0.013 | -0.053 |
| dualtopo | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.128 |
| dualtopo_no_bg | post_covid | 51 | 0.145 | 0 | 51 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.128 |
| arima | post_covid | 51 | 0.145 | 0 | 51 | 20 | 0.000 | 1.000 | 0.000 | 0.000 | -0.066 | -0.213 |
| persistence | post_covid | 51 | 0.145 | 2 | 49 | 49 | 0.039 | 0.961 | 0.020 | 0.039 | -0.124 | -0.531 |
| seasonal_naive | post_covid | 51 | 0.145 | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | 0.090 | -0.138 | -0.625 |

### Crossing IT90

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 18 | 0.051 | 1 | 17 | 7 | 0.056 | 0.875 | 0.040 | 0.077 | 0.035 | -0.220 |
| arima | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.197 |
| dualtopo | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| dualtopo_no_bg | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.054 |
| gnn_multiedge_covid_rsv | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.012 |
| gnn_multiedge_season_level | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | 0.002 |
| lstm | post_covid | 18 | 0.051 | 0 | 18 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.042 |
| gnn_multiedge | post_covid | 18 | 0.051 | 1 | 17 | 21 | 0.056 | 0.955 | 0.026 | 0.050 | -0.007 | -0.664 |
| gnn_corrbinary | post_covid | 18 | 0.051 | 0 | 18 | 8 | 0.000 | 1.000 | 0.000 | 0.000 | -0.024 | -0.428 |
| gnn_multiedge_leaknorm | post_covid | 18 | 0.051 | 1 | 17 | 31 | 0.056 | 0.969 | 0.020 | 0.040 | -0.037 | -0.944 |
| gnn_uniform | post_covid | 18 | 0.051 | 0 | 18 | 14 | 0.000 | 1.000 | 0.000 | 0.000 | -0.042 | -0.514 |
| gnn_multiedge_level | post_covid | 18 | 0.051 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.054 | -0.609 |
| persistence | post_covid | 18 | 0.051 | 0 | 18 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.054 | -0.640 |
| gnn_multiedge_rt | post_covid | 18 | 0.051 | 0 | 18 | 23 | 0.000 | 1.000 | 0.000 | 0.000 | -0.069 | -0.701 |
| seasonal_naive | post_covid | 18 | 0.051 | 0 | 18 | 34 | 0.000 | 1.000 | 0.000 | 0.000 | -0.102 | -0.974 |
| gnn_geo | post_covid | 18 | 0.051 | 0 | 18 | 61 | 0.000 | 1.000 | 0.000 | 0.000 | -0.183 | -1.874 |

### Crossing IT98 — **underpowered: 2 observed events**, not ranked

| model | variant | n_events | base_rate | hits | misses | false_alarms | POD | FAR | CSI | F1 | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.393 |
| dualtopo | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| dualtopo_no_bg | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.006 |
| gnn_corrbinary | post_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.573 |
| gnn_geo | post_covid | 2 | 0.006 | 0 | 2 | 18 | 0.000 | 1.000 | 0.000 | 0.000 | -0.051 | -6.337 |
| gnn_multiedge | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -1.181 |
| gnn_multiedge_covid_rsv | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.169 |
| gnn_multiedge_leaknorm | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -1.716 |
| gnn_multiedge_level | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.262 |
| gnn_multiedge_rt | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.700 |
| gnn_multiedge_season | post_covid | 2 | 0.006 | 0 | 2 | 1 | 0.000 | 1.000 | 0.000 | 0.000 | -0.003 | -0.626 |
| gnn_multiedge_season_level | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.035 |
| gnn_uniform | post_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -0.979 |
| lstm | post_covid | 2 | 0.006 | 0 | 2 | 0 | 0.000 |  | 0.000 | 0.000 | 0.000 | -0.018 |
| persistence | post_covid | 2 | 0.006 | 0 | 2 | 2 | 0.000 | 1.000 | 0.000 | 0.000 | -0.006 | -2.121 |
| seasonal_naive | post_covid | 2 | 0.006 | 0 | 2 | 3 | 0.000 | 1.000 | 0.000 | 0.000 | -0.009 | -3.880 |

### All four bands — 352 weeks scored

*`mean_band_error` above zero means the model calls severity higher than it turned out to be.*

| model | variant | n_obs | exact_band | within_one_band | kappa_quadratic | mean_band_error |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| dualtopo_no_bg | post_covid | 352 | 0.855 | 0.949 | 0.000 | -0.202 |
| lstm | post_covid | 352 | 0.838 | 0.949 | -0.000 | -0.173 |
| gnn_multiedge_covid_rsv | post_covid | 352 | 0.835 | 0.952 | 0.035 | -0.162 |
| arima | post_covid | 352 | 0.798 | 0.949 | -0.064 | -0.145 |
| gnn_multiedge_season | post_covid | 352 | 0.787 | 0.957 | 0.282 | 0.017 |
| gnn_multiedge_season_level | post_covid | 352 | 0.773 | 0.974 | 0.294 | 0.006 |
| persistence | post_covid | 352 | 0.722 | 0.898 | -0.122 | 0.000 |
| gnn_multiedge | post_covid | 352 | 0.690 | 0.915 | 0.070 | 0.131 |
| gnn_uniform | post_covid | 352 | 0.688 | 0.938 | 0.093 | 0.108 |
| gnn_corrbinary | post_covid | 352 | 0.679 | 0.943 | 0.046 | 0.099 |
| gnn_multiedge_rt | post_covid | 352 | 0.673 | 0.901 | 0.009 | 0.136 |
| gnn_multiedge_leaknorm | post_covid | 352 | 0.665 | 0.886 | 0.025 | 0.173 |
| gnn_multiedge_level | post_covid | 352 | 0.665 | 0.923 | 0.105 | 0.165 |
| seasonal_naive | post_covid | 352 | 0.645 | 0.861 | -0.114 | 0.139 |
| gnn_geo | post_covid | 352 | 0.577 | 0.801 | -0.063 | 0.384 |

# Timing at IT50

Per neighborhood-season, over the neighborhood indicators. Negative onset error means the forecast crossed the threshold *before* the observation did, so positive lead time is a warning in advance.

| model | variant | n_seasons_crossed | median_onset_error_weeks | median_lead_time_weeks | mean_abs_onset_error | median_peak_week_error | median_peak_error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | post_covid | 14 | 2.000 | -2.000 | 1.786 | 4.500 | 1.398 |
| gnn_multiedge_season | post_covid | 14 | 2.000 | -2.000 | 1.786 | 2.000 | -0.186 |
| gnn_multiedge_season_level | post_covid | 14 | 2.000 | -2.000 | 1.786 | 1.500 | -11.218 |
| gnn_uniform | post_covid | 14 | 2.000 | -2.000 | 2.143 | 4.000 | 4.645 |
| gnn_multiedge | post_covid | 14 | 2.000 | -2.000 | 2.286 | 3.000 | 0.505 |
| gnn_corrbinary | post_covid | 14 | 2.000 | -2.000 | 2.357 | 4.000 | 1.673 |
| gnn_geo | post_covid | 14 | 2.500 | -2.500 | 2.429 | 5.500 | 4.996 |
| gnn_multiedge_leaknorm | post_covid | 14 | 2.500 | -2.500 | 2.429 | 4.000 | 2.522 |
| gnn_multiedge_rt | post_covid | 14 | 2.000 | -2.000 | 2.571 | 4.000 | 0.864 |
| seasonal_naive | post_covid | 14 | 4.000 | -4.000 | 3.571 | 4.500 | 8.550 |
| gnn_multiedge_covid_rsv | post_covid | 10 | 3.500 | -3.500 | 3.900 | 3.000 | -2.553 |
| lstm | post_covid | 7 | 4.000 | -4.000 | 4.000 | 3.000 | -10.503 |
| persistence | post_covid | 14 | 4.000 | -4.000 | 4.000 | 4.000 | 0.000 |
| arima | post_covid | 10 | 5.000 | -5.000 | 4.600 | 4.000 | -3.152 |
| dualtopo | post_covid | 0 |  |  |  | 2.000 | -4.295 |
| dualtopo_no_bg | post_covid | 0 |  |  |  | 2.500 | -4.373 |

# Notes

- 6 forecast rows had a zero-width interval, so their exceedance probability is a hard 0 or 1 rather than a distribution.
- IT98 was crossed on only 2 neighborhood-weeks in this window, so its scores are reported but not ranked.
