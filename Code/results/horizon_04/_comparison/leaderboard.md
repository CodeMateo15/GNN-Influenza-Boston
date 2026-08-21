Ranked by **RMSE** within each segment, `scope=pooled`, horizon 4.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 23.907 | 100.392 | 13.861 | 0.648 | 92.823 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 24.901 | 86.980 | 13.122 | 0.610 | 90.271 | delta | train |
| lstm | post_covid | 26.670 | 91.985 | 13.612 | 0.540 | 92.663 | level | train |
| gnn_multiedge_season | post_covid | 28.537 | 102.330 | 15.327 | 0.631 | 93.301 | delta | train |
| arima | post_covid | 28.919 | 163.108 | 17.265 | 0.467 | 97.129 | level | none |
| dualtopo_no_bg | post_covid | 29.024 | 207.528 | 18.250 | 0.410 | 87.081 | level | train |
| dualtopo | post_covid | 29.199 | 211.716 | 18.487 | 0.405 | 87.081 | level | train |
| gnn_multiedge_season_level | post_covid | 29.211 | 102.808 | 16.165 | 0.602 | 92.026 | level | train |
| dualtopo_fullhistory | full | 29.754 | 68.721 | 13.387 | 0.371 | 87.241 | level | train |
| arima | exclude_covid | 30.627 | 144.647 | 17.399 | 0.421 | 94.737 | level | none |
| lstm | exclude_covid | 31.559 | 99.254 | 16.712 | 0.460 | 89.314 | level | train |
| persistence | post_covid | 34.910 | 92.984 | 17.464 | 0.372 | 94.737 | level | none |
| persistence | exclude_covid | 34.910 | 92.984 | 17.464 | 0.372 | 94.418 | level | none |
| gnn_multiedge_full | full | 35.456 | 133.227 | 19.755 | 0.556 | 87.879 | delta | train |
| gnn_multiedge_rt | post_covid | 38.704 | 143.252 | 21.364 | 0.447 | 86.284 | delta | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| gnn_multiedge | post_covid | 41.341 | 151.372 | 23.433 | 0.485 | 82.616 | delta | train |
| gnn_corrbinary | post_covid | 42.354 | 173.955 | 23.759 | 0.459 | 83.732 | delta | train |
| gnn_multiedge_level | post_covid | 46.106 | 216.796 | 26.284 | 0.493 | 74.003 | level | train |
| gnn_multiedge_leaknorm | post_covid | 47.607 | 184.510 | 26.426 | 0.415 | 80.542 | delta | all |
| gnn_uniform | post_covid | 49.164 | 198.323 | 26.089 | 0.445 | 82.456 | delta | train |
| gnn_geo | post_covid | 63.665 | 224.130 | 33.855 | 0.374 | 88.038 | delta | train |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | post_covid | 30.103 | 86.732 | 18.969 | 0.659 | 87.216 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 32.454 | 80.668 | 18.947 | 0.561 | 83.807 | delta | train |
| lstm | post_covid | 32.853 | 65.364 | 17.423 | 0.556 | 87.500 | level | train |
| dualtopo_no_bg | post_covid | 33.441 | 108.322 | 18.968 | 0.503 | 83.807 | level | train |
| dualtopo | post_covid | 33.441 | 109.861 | 19.058 | 0.501 | 83.807 | level | train |
| arima | post_covid | 35.925 | 108.401 | 21.251 | 0.434 | 94.886 | level | none |
| gnn_multiedge_season | post_covid | 35.989 | 102.342 | 21.178 | 0.588 | 89.205 | delta | train |
| gnn_multiedge_season_level | post_covid | 36.558 | 105.575 | 22.256 | 0.550 | 87.216 | level | train |
| arima | exclude_covid | 38.529 | 101.501 | 22.414 | 0.377 | 90.625 | level | none |
| dualtopo_fullhistory | full | 39.401 | 73.275 | 20.815 | 0.249 | 78.125 | level | train |
| lstm | exclude_covid | 39.794 | 89.307 | 23.098 | 0.412 | 83.239 | level | train |
| gnn_uniform | post_covid | 41.205 | 129.047 | 25.073 | 0.548 | 84.943 | delta | train |
| gnn_corrbinary | post_covid | 41.354 | 129.480 | 25.775 | 0.502 | 82.386 | delta | train |
| gnn_multiedge_full | full | 43.050 | 130.672 | 26.000 | 0.509 | 82.670 | delta | train |
| gnn_multiedge | post_covid | 44.095 | 123.857 | 27.698 | 0.502 | 79.261 | delta | train |
| persistence | exclude_covid | 45.891 | 104.267 | 26.733 | 0.284 | 90.057 | level | none |
| persistence | post_covid | 45.891 | 104.267 | 26.733 | 0.284 | 90.625 | level | none |
| gnn_multiedge_level | post_covid | 47.236 | 162.484 | 28.594 | 0.506 | 73.011 | level | train |
| gnn_multiedge_rt | post_covid | 47.870 | 150.284 | 29.577 | 0.384 | 80.398 | delta | train |
| gnn_multiedge_leaknorm | post_covid | 47.924 | 142.092 | 29.547 | 0.438 | 78.125 | delta | all |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| gnn_geo | post_covid | 65.562 | 188.175 | 38.432 | 0.358 | 86.932 | delta | train |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 5.594 | 62.891 | 3.878 | 0.755 | 98.909 | level | train |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| gnn_multiedge_covid_rsv_full | full | 8.097 | 95.060 | 5.665 | 0.598 | 98.545 | delta | train |
| persistence | exclude_covid | 9.111 | 78.541 | 5.600 | 0.674 | 100.000 | level | none |
| persistence | post_covid | 9.111 | 78.541 | 5.600 | 0.674 | 100.000 | level | none |
| gnn_multiedge_covid_rsv | post_covid | 11.964 | 117.878 | 7.323 | 0.657 | 100.000 | delta | train |
| gnn_multiedge_season | post_covid | 14.104 | 102.315 | 7.839 | 0.690 | 98.545 | delta | train |
| gnn_multiedge_season_level | post_covid | 15.321 | 99.266 | 8.369 | 0.735 | 98.182 | level | train |
| arima | exclude_covid | 15.445 | 199.873 | 10.979 | 0.607 | 100.000 | level | none |
| lstm | post_covid | 15.498 | 126.061 | 8.735 | 0.675 | 99.273 | level | train |
| lstm | exclude_covid | 15.614 | 111.987 | 8.538 | 0.692 | 97.091 | level | train |
| arima | post_covid | 15.961 | 233.134 | 12.163 | 0.690 | 100.000 | level | none |
| gnn_multiedge_rt | post_covid | 21.962 | 134.251 | 10.853 | 0.468 | 93.818 | delta | train |
| dualtopo_no_bg | post_covid | 22.119 | 334.513 | 17.331 | 0.589 | 91.273 | level | train |
| gnn_multiedge_full | full | 22.226 | 136.498 | 11.761 | 0.680 | 94.545 | delta | train |
| dualtopo | post_covid | 22.637 | 342.090 | 17.755 | 0.585 | 91.273 | level | train |
| gnn_multiedge | post_covid | 37.523 | 186.590 | 17.973 | 0.642 | 86.909 | delta | train |
| gnn_corrbinary | post_covid | 43.601 | 230.882 | 21.179 | 0.668 | 85.455 | delta | train |
| gnn_multiedge_level | post_covid | 44.619 | 286.315 | 23.328 | 0.674 | 75.273 | level | train |
| gnn_multiedge_leaknorm | post_covid | 47.198 | 238.804 | 22.431 | 0.632 | 83.636 | delta | all |
| gnn_uniform | post_covid | 57.773 | 286.996 | 27.390 | 0.672 | 79.273 | delta | train |
| gnn_geo | post_covid | 61.152 | 270.152 | 27.996 | 0.654 | 89.455 | delta | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_multiedge_covid_rsv (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_multiedge_covid_rsv (post_covid)`
- **Off-season (Apr–Sep)**: `dualtopo_fullhistory (full)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
