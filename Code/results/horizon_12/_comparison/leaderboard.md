Ranked by **RMSE** within each segment, `scope=pooled`, horizon 12.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 22.463 | 99.465 | 12.369 | 0.694 | 97.927 | level | train |
| gnn_multiedge_season | post_covid | 23.352 | 91.044 | 13.487 | 0.672 | 82.456 | delta | train |
| gnn_multiedge_level | post_covid | 25.311 | 113.410 | 13.189 | 0.594 | 99.362 | level | train |
| gnn_corrbinary | post_covid | 26.233 | 124.868 | 15.096 | 0.548 | 95.215 | delta | train |
| gnn_multiedge_rt | post_covid | 26.885 | 117.790 | 16.079 | 0.636 | 90.750 | delta | train |
| gnn_geo | post_covid | 27.728 | 108.783 | 14.841 | 0.476 | 98.724 | delta | train |
| gnn_multiedge | post_covid | 27.829 | 110.177 | 15.046 | 0.475 | 98.884 | delta | train |
| gnn_multiedge_full | full | 29.024 | 96.578 | 15.074 | 0.485 | 89.314 | delta | train |
| dualtopo_no_bg | post_covid | 29.028 | 202.681 | 17.980 | 0.400 | 84.530 | level | train |
| dualtopo | post_covid | 29.060 | 204.085 | 18.054 | 0.400 | 84.530 | level | train |
| gnn_uniform | post_covid | 29.913 | 110.730 | 16.111 | 0.379 | 99.043 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 30.100 | 96.220 | 15.840 | 0.450 | 90.112 | delta | train |
| arima | post_covid | 30.179 | 235.611 | 20.072 | 0.396 | 99.681 | level | none |
| gnn_multiedge_leaknorm | post_covid | 30.748 | 129.176 | 17.613 | 0.417 | 96.970 | delta | all |
| dualtopo_fullhistory | full | 30.910 | 148.183 | 18.080 | 0.343 | 90.750 | level | train |
| gnn_multiedge_covid_rsv | post_covid | 31.974 | 223.773 | 21.861 | 0.535 | 95.215 | delta | train |
| lstm | exclude_covid | 32.657 | 155.209 | 19.304 | 0.389 | 88.836 | level | train |
| arima | exclude_covid | 33.036 | 205.103 | 20.360 | 0.291 | 96.013 | level | none |
| lstm | post_covid | 33.385 | 181.492 | 20.019 | 0.342 | 85.008 | level | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.896 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| persistence | exclude_covid | 40.007 | 145.935 | 22.119 | 0.169 | 96.013 | level | none |
| persistence | post_covid | 40.007 | 145.935 | 22.119 | 0.169 | 97.129 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | post_covid | 29.137 | 86.892 | 17.477 | 0.650 | 96.307 | level | train |
| gnn_multiedge_season | post_covid | 29.401 | 83.068 | 17.916 | 0.640 | 98.580 | delta | train |
| gnn_multiedge_level | post_covid | 32.460 | 79.779 | 17.505 | 0.586 | 98.864 | level | train |
| gnn_corrbinary | post_covid | 32.935 | 93.199 | 19.731 | 0.533 | 93.750 | delta | train |
| arima | post_covid | 33.227 | 121.523 | 20.019 | 0.495 | 99.432 | level | none |
| dualtopo | post_covid | 33.685 | 105.686 | 18.872 | 0.499 | 81.534 | level | train |
| dualtopo_no_bg | post_covid | 33.715 | 105.030 | 18.849 | 0.499 | 81.250 | level | train |
| gnn_multiedge_rt | post_covid | 34.422 | 121.611 | 22.719 | 0.587 | 99.716 | delta | train |
| gnn_multiedge | post_covid | 35.613 | 84.496 | 20.342 | 0.439 | 98.011 | delta | train |
| gnn_geo | post_covid | 35.722 | 86.545 | 20.600 | 0.427 | 97.727 | delta | train |
| gnn_multiedge_full | full | 37.255 | 75.881 | 20.442 | 0.491 | 93.466 | delta | train |
| gnn_multiedge_covid_rsv | post_covid | 37.585 | 212.995 | 27.139 | 0.524 | 98.295 | delta | train |
| gnn_uniform | post_covid | 38.339 | 84.542 | 21.783 | 0.328 | 98.295 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 38.781 | 80.012 | 21.872 | 0.463 | 90.625 | delta | train |
| arima | exclude_covid | 38.793 | 112.780 | 22.507 | 0.311 | 92.898 | level | none |
| gnn_multiedge_leaknorm | post_covid | 39.073 | 105.316 | 23.670 | 0.354 | 96.875 | delta | all |
| dualtopo_fullhistory | full | 39.362 | 108.268 | 24.021 | 0.266 | 83.523 | level | train |
| lstm | exclude_covid | 41.379 | 127.614 | 26.197 | 0.304 | 80.966 | level | train |
| lstm | post_covid | 41.545 | 128.343 | 25.252 | 0.273 | 77.841 | level | train |
| persistence | exclude_covid | 51.357 | 108.482 | 30.802 | 0.119 | 92.898 | level | none |
| persistence | post_covid | 51.357 | 108.482 | 30.802 | 0.119 | 94.886 | level | none |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.477 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| gnn_multiedge_season_level | post_covid | 7.985 | 115.557 | 5.832 | 0.709 | 100.000 | level | train |
| gnn_multiedge_level | post_covid | 10.580 | 156.459 | 7.664 | 0.691 | 100.000 | level | train |
| gnn_geo | post_covid | 10.934 | 137.249 | 7.470 | 0.613 | 100.000 | delta | train |
| gnn_multiedge_rt | post_covid | 11.458 | 112.901 | 7.579 | 0.097 | 79.273 | delta | train |
| gnn_multiedge_season | post_covid | 11.701 | 101.253 | 7.818 | -0.002 | 61.818 | delta | train |
| gnn_multiedge_covid_rsv_full | full | 11.859 | 116.966 | 8.118 | 0.009 | 89.455 | delta | train |
| gnn_multiedge | post_covid | 11.933 | 143.047 | 8.266 | 0.260 | 100.000 | delta | train |
| gnn_multiedge_full | full | 12.005 | 123.069 | 8.203 | 0.014 | 84.000 | delta | train |
| gnn_uniform | post_covid | 12.597 | 144.251 | 8.852 | 0.049 | 100.000 | delta | train |
| gnn_corrbinary | post_covid | 13.440 | 165.403 | 9.162 | 0.618 | 97.091 | delta | train |
| dualtopo_fullhistory | full | 13.973 | 199.274 | 10.476 | 0.724 | 100.000 | level | train |
| gnn_multiedge_leaknorm | post_covid | 14.195 | 159.717 | 9.859 | 0.063 | 97.091 | delta | all |
| lstm | exclude_covid | 15.489 | 190.531 | 10.480 | 0.708 | 98.909 | level | train |
| persistence | exclude_covid | 16.528 | 193.874 | 11.005 | 0.596 | 100.000 | level | none |
| persistence | post_covid | 16.528 | 193.874 | 11.005 | 0.596 | 100.000 | level | none |
| lstm | post_covid | 18.220 | 249.522 | 13.321 | 0.679 | 94.182 | level | train |
| dualtopo_no_bg | post_covid | 21.590 | 327.674 | 16.868 | 0.582 | 88.727 | level | train |
| dualtopo | post_covid | 21.750 | 330.036 | 17.006 | 0.582 | 88.364 | level | train |
| gnn_multiedge_covid_rsv | post_covid | 22.864 | 237.568 | 15.104 | 0.111 | 91.273 | delta | train |
| arima | exclude_covid | 23.708 | 323.278 | 17.612 | 0.594 | 100.000 | level | none |
| arima | post_covid | 25.756 | 381.644 | 20.139 | 0.564 | 100.000 | level | none |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_multiedge_season_level (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_multiedge_season_level (post_covid)`
- **Off-season (Apr–Sep)**: `seasonal_naive (exclude_covid)`

The leader changes between segments. Off-season and flu-season are close to different problems — the off-season is flat and near zero, the flu season has the peak that actually matters operationally — so a model tuned on a full-year average is not necessarily the one you would deploy for a surge.

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
