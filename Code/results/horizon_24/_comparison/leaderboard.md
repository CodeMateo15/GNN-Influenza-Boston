Ranked by **RMSE** within each segment, `scope=pooled`, horizon 24.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | post_covid | 23.880 | 139.794 | 15.395 | 0.742 | 92.026 | delta | train |
| gnn_multiedge_season_level | post_covid | 24.824 | 118.657 | 15.669 | 0.751 | 96.970 | level | train |
| gnn_multiedge_covid_rsv_full | full | 24.922 | 160.276 | 15.937 | 0.632 | 97.129 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 25.039 | 158.251 | 16.438 | 0.741 | 95.215 | delta | all |
| gnn_uniform | post_covid | 25.092 | 165.042 | 16.907 | 0.740 | 95.694 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 25.179 | 144.493 | 16.717 | 0.729 | 86.124 | delta | train |
| gnn_multiedge_level | post_covid | 25.584 | 138.909 | 16.424 | 0.751 | 99.522 | level | train |
| gnn_multiedge_full | full | 25.670 | 168.376 | 17.606 | 0.683 | 98.565 | delta | train |
| gnn_geo | post_covid | 26.230 | 169.897 | 17.430 | 0.755 | 95.375 | delta | train |
| gnn_multiedge | post_covid | 26.627 | 151.290 | 16.844 | 0.751 | 94.099 | delta | train |
| arima | post_covid | 28.064 | 191.553 | 17.643 | 0.470 | 98.086 | level | none |
| gnn_multiedge_rt | post_covid | 28.804 | 167.357 | 18.534 | 0.662 | 93.142 | delta | train |
| dualtopo_fullhistory | full | 29.154 | 79.762 | 13.148 | 0.410 | 88.995 | level | train |
| arima | exclude_covid | 30.492 | 233.019 | 19.930 | 0.368 | 95.534 | level | none |
| dualtopo_no_bg | post_covid | 30.807 | 257.329 | 21.248 | 0.401 | 85.805 | level | train |
| dualtopo | post_covid | 30.837 | 258.108 | 21.291 | 0.401 | 85.805 | level | train |
| lstm | exclude_covid | 33.224 | 186.401 | 22.262 | 0.664 | 96.970 | level | train |
| gnn_corrbinary | post_covid | 33.521 | 180.850 | 21.230 | 0.742 | 89.793 | delta | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 96.172 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| lstm | post_covid | 42.138 | 210.581 | 26.844 | 0.613 | 86.603 | level | train |
| persistence | exclude_covid | 53.991 | 392.896 | 30.600 | -0.146 | 94.896 | level | none |
| persistence | post_covid | 53.991 | 392.896 | 30.600 | -0.146 | 96.013 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv_full | full | 30.141 | 124.361 | 20.402 | 0.620 | 100.000 | delta | train |
| gnn_multiedge_season | post_covid | 30.289 | 125.750 | 21.232 | 0.711 | 100.000 | delta | train |
| gnn_uniform | post_covid | 30.572 | 129.046 | 21.918 | 0.726 | 99.716 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 30.868 | 130.468 | 21.799 | 0.720 | 99.716 | delta | all |
| gnn_multiedge_full | full | 31.746 | 141.714 | 23.153 | 0.644 | 100.000 | delta | train |
| gnn_multiedge_season_level | post_covid | 32.023 | 135.992 | 22.845 | 0.712 | 98.864 | level | train |
| gnn_geo | post_covid | 32.225 | 139.111 | 22.935 | 0.739 | 99.148 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 32.291 | 152.331 | 23.852 | 0.693 | 97.443 | delta | train |
| dualtopo | post_covid | 33.041 | 133.221 | 20.554 | 0.499 | 83.807 | level | train |
| dualtopo_no_bg | post_covid | 33.043 | 132.885 | 20.533 | 0.499 | 83.807 | level | train |
| gnn_multiedge_level | post_covid | 33.063 | 147.929 | 23.847 | 0.708 | 99.148 | level | train |
| arima | post_covid | 33.069 | 105.992 | 19.398 | 0.512 | 98.295 | level | none |
| gnn_multiedge | post_covid | 33.542 | 127.567 | 22.717 | 0.726 | 99.432 | delta | train |
| arima | exclude_covid | 33.780 | 109.557 | 20.093 | 0.486 | 93.750 | level | none |
| gnn_multiedge_rt | post_covid | 34.857 | 129.479 | 23.575 | 0.635 | 99.716 | delta | train |
| dualtopo_fullhistory | full | 38.485 | 64.858 | 19.472 | 0.349 | 80.398 | level | train |
| lstm | exclude_covid | 38.868 | 169.871 | 28.305 | 0.633 | 95.739 | level | train |
| gnn_corrbinary | post_covid | 43.249 | 197.165 | 31.063 | 0.707 | 96.023 | delta | train |
| persistence | exclude_covid | 44.397 | 70.897 | 24.728 | 0.136 | 96.591 | level | none |
| persistence | post_covid | 44.397 | 70.897 | 24.728 | 0.136 | 97.443 | level | none |
| lstm | post_covid | 50.048 | 202.732 | 34.784 | 0.569 | 81.818 | level | train |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 93.466 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 6.491 | 98.838 | 5.053 | 0.783 | 100.000 | level | train |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.636 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| gnn_multiedge_season_level | post_covid | 9.612 | 96.469 | 6.483 | 0.730 | 94.545 | level | train |
| gnn_multiedge_level | post_covid | 9.647 | 127.363 | 6.924 | 0.756 | 100.000 | level | train |
| gnn_multiedge_covid_rsv | post_covid | 10.528 | 134.460 | 7.585 | 0.603 | 71.636 | delta | train |
| gnn_multiedge_season | post_covid | 11.221 | 157.769 | 7.923 | 0.554 | 81.818 | delta | train |
| gnn_corrbinary | post_covid | 12.949 | 159.967 | 8.643 | 0.581 | 81.818 | delta | train |
| gnn_multiedge | post_covid | 13.279 | 181.655 | 9.326 | 0.496 | 87.273 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 14.486 | 193.813 | 9.576 | 0.494 | 89.455 | delta | all |
| gnn_multiedge_full | full | 14.574 | 202.502 | 10.505 | 0.660 | 96.727 | delta | train |
| gnn_uniform | post_covid | 15.464 | 211.117 | 10.494 | 0.417 | 90.545 | delta | train |
| gnn_geo | post_covid | 15.475 | 209.302 | 10.383 | 0.437 | 90.545 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 15.914 | 206.247 | 10.223 | 0.493 | 93.455 | delta | train |
| gnn_multiedge_rt | post_covid | 18.343 | 215.840 | 12.082 | 0.516 | 84.727 | delta | train |
| arima | post_covid | 19.898 | 301.072 | 15.396 | 0.652 | 97.818 | level | none |
| lstm | exclude_covid | 24.145 | 207.559 | 14.527 | 0.756 | 98.545 | level | train |
| arima | exclude_covid | 25.677 | 391.050 | 19.722 | 0.524 | 97.818 | level | none |
| dualtopo_no_bg | post_covid | 27.683 | 416.618 | 22.164 | 0.583 | 88.364 | level | train |
| dualtopo | post_covid | 27.760 | 417.962 | 22.235 | 0.582 | 88.364 | level | train |
| lstm | post_covid | 29.022 | 220.628 | 16.680 | 0.692 | 92.727 | level | train |
| persistence | exclude_covid | 64.212 | 805.054 | 38.115 | -0.004 | 92.727 | level | none |
| persistence | post_covid | 64.212 | 805.054 | 38.115 | -0.004 | 94.182 | level | none |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_multiedge_season (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_multiedge_covid_rsv_full (full)`
- **Off-season (Apr–Sep)**: `dualtopo_fullhistory (full)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
