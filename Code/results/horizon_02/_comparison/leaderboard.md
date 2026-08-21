Ranked by **RMSE** within each segment, `scope=pooled`, horizon 2.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 19.981 | 74.423 | 10.729 | 0.769 | 95.215 | delta | train |
| lstm | post_covid | 21.361 | 76.895 | 10.944 | 0.731 | 94.418 | level | train |
| arima | post_covid | 21.552 | 111.014 | 12.120 | 0.739 | 95.853 | level | none |
| gnn_multiedge_covid_rsv_full | full | 22.853 | 86.341 | 12.712 | 0.760 | 88.517 | delta | train |
| persistence | exclude_covid | 23.840 | 74.191 | 12.070 | 0.706 | 92.823 | level | none |
| persistence | post_covid | 23.840 | 74.191 | 12.070 | 0.706 | 93.301 | level | none |
| gnn_multiedge_leaknorm | post_covid | 24.883 | 109.653 | 14.192 | 0.784 | 94.577 | delta | all |
| lstm | exclude_covid | 25.137 | 73.595 | 11.921 | 0.704 | 91.228 | level | train |
| gnn_multiedge | post_covid | 26.220 | 123.305 | 15.712 | 0.766 | 96.810 | delta | train |
| gnn_multiedge_full | full | 26.879 | 99.953 | 14.986 | 0.732 | 92.344 | delta | train |
| gnn_multiedge_rt | post_covid | 27.437 | 107.679 | 15.485 | 0.742 | 91.547 | delta | train |
| gnn_multiedge_season | post_covid | 28.387 | 115.062 | 16.607 | 0.747 | 94.896 | delta | train |
| dualtopo | post_covid | 29.104 | 205.431 | 18.133 | 0.400 | 87.081 | level | train |
| dualtopo_no_bg | post_covid | 29.239 | 211.103 | 18.444 | 0.400 | 87.081 | level | train |
| dualtopo_fullhistory | full | 30.509 | 69.365 | 14.071 | 0.363 | 86.443 | level | train |
| gnn_corrbinary | post_covid | 30.968 | 135.126 | 18.420 | 0.722 | 93.780 | delta | train |
| gnn_uniform | post_covid | 34.181 | 134.593 | 19.207 | 0.700 | 91.388 | delta | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| gnn_multiedge_season_level | post_covid | 40.480 | 176.501 | 24.074 | 0.646 | 77.671 | level | train |
| arima | exclude_covid | 42.766 | 120.113 | 15.046 | 0.467 | 93.142 | level | none |
| gnn_geo | post_covid | 45.315 | 207.129 | 26.064 | 0.640 | 85.008 | delta | train |
| gnn_multiedge_level | post_covid | 47.278 | 194.178 | 26.685 | 0.580 | 73.365 | level | train |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 25.691 | 70.152 | 15.059 | 0.749 | 92.045 | delta | train |
| arima | post_covid | 27.429 | 80.316 | 15.770 | 0.720 | 92.614 | level | none |
| lstm | post_covid | 27.783 | 62.935 | 15.443 | 0.702 | 90.057 | level | train |
| gnn_multiedge | post_covid | 28.384 | 99.778 | 18.223 | 0.784 | 96.023 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 28.850 | 89.107 | 17.073 | 0.785 | 92.898 | delta | all |
| gnn_multiedge_covid_rsv_full | full | 29.246 | 87.615 | 18.091 | 0.731 | 81.534 | delta | train |
| persistence | exclude_covid | 31.166 | 76.638 | 17.825 | 0.667 | 88.636 | level | none |
| persistence | post_covid | 31.166 | 76.638 | 17.825 | 0.667 | 89.489 | level | none |
| gnn_corrbinary | post_covid | 31.815 | 112.742 | 21.075 | 0.756 | 94.602 | delta | train |
| lstm | exclude_covid | 32.738 | 65.835 | 17.045 | 0.671 | 84.659 | level | train |
| gnn_multiedge_rt | post_covid | 33.072 | 97.518 | 19.916 | 0.728 | 88.068 | delta | train |
| gnn_multiedge_full | full | 33.072 | 95.812 | 19.858 | 0.711 | 88.636 | delta | train |
| dualtopo_no_bg | post_covid | 33.533 | 109.082 | 19.024 | 0.499 | 83.807 | level | train |
| dualtopo | post_covid | 33.653 | 106.322 | 18.898 | 0.499 | 83.807 | level | train |
| gnn_multiedge_season | post_covid | 33.827 | 106.996 | 21.444 | 0.734 | 92.898 | delta | train |
| gnn_uniform | post_covid | 35.183 | 104.007 | 21.531 | 0.737 | 92.045 | delta | train |
| dualtopo_fullhistory | full | 40.372 | 75.667 | 21.882 | 0.260 | 77.557 | level | train |
| gnn_geo | post_covid | 43.983 | 149.955 | 27.489 | 0.693 | 85.795 | delta | train |
| gnn_multiedge_season_level | post_covid | 44.806 | 158.871 | 29.372 | 0.641 | 72.443 | level | train |
| gnn_multiedge_level | post_covid | 46.793 | 160.385 | 29.777 | 0.615 | 70.739 | level | train |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| arima | exclude_covid | 56.387 | 108.370 | 21.196 | 0.419 | 88.920 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 6.000 | 61.297 | 4.074 | 0.748 | 97.818 | level | train |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| lstm | post_covid | 7.234 | 94.765 | 5.186 | 0.777 | 100.000 | level | train |
| persistence | exclude_covid | 7.249 | 71.059 | 4.704 | 0.732 | 98.182 | level | none |
| persistence | post_covid | 7.249 | 71.059 | 4.704 | 0.732 | 98.182 | level | none |
| gnn_multiedge_covid_rsv | post_covid | 8.089 | 79.890 | 5.185 | 0.728 | 99.273 | delta | train |
| lstm | exclude_covid | 8.297 | 83.527 | 5.361 | 0.790 | 99.636 | level | train |
| gnn_multiedge_covid_rsv_full | full | 9.791 | 84.711 | 5.828 | 0.738 | 97.455 | delta | train |
| arima | post_covid | 9.798 | 150.309 | 7.448 | 0.735 | 100.000 | level | none |
| arima | exclude_covid | 10.008 | 135.145 | 7.175 | 0.722 | 98.545 | level | none |
| gnn_multiedge_full | full | 15.723 | 105.253 | 8.750 | 0.741 | 97.091 | delta | train |
| gnn_multiedge_rt | post_covid | 17.786 | 120.685 | 9.813 | 0.736 | 96.000 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 18.611 | 135.953 | 10.504 | 0.744 | 96.727 | delta | all |
| gnn_multiedge_season | post_covid | 19.302 | 125.387 | 10.416 | 0.738 | 97.455 | delta | train |
| dualtopo | post_covid | 21.947 | 332.290 | 17.153 | 0.581 | 91.273 | level | train |
| dualtopo_no_bg | post_covid | 22.582 | 341.689 | 17.702 | 0.581 | 91.273 | level | train |
| gnn_multiedge | post_covid | 23.157 | 153.420 | 12.497 | 0.736 | 97.818 | delta | train |
| gnn_corrbinary | post_covid | 29.849 | 163.778 | 15.022 | 0.715 | 92.727 | delta | train |
| gnn_uniform | post_covid | 32.854 | 173.743 | 16.233 | 0.706 | 90.545 | delta | train |
| gnn_multiedge_season_level | post_covid | 34.153 | 199.067 | 17.292 | 0.725 | 84.364 | level | train |
| gnn_geo | post_covid | 46.965 | 280.312 | 24.240 | 0.723 | 84.000 | delta | train |
| gnn_multiedge_level | post_covid | 47.893 | 237.433 | 22.728 | 0.701 | 76.727 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_multiedge_covid_rsv (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_multiedge_covid_rsv (post_covid)`
- **Off-season (Apr–Sep)**: `dualtopo_fullhistory (full)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
