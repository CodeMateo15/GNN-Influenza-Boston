# Leaderboard by forecast horizon — post_covid

`segment=overall`, `scope=pooled`. RMSE is ILI ED visits per 100,000. Every horizon scores the same 49 target weeks, so the columns are directly comparable.

## Does the horizon separate the models?

| horizon | n_models | RMSE_std | max_minus_min | min | max |
| --- | --- | --- | --- | --- | --- |
| 1 | 16 | 11.108 | 35.963 | 14.657 | 50.619 |
| 2 | 16 | 8.513 | 27.298 | 19.981 | 47.278 |
| 4 | 16 | 10.690 | 39.759 | 23.907 | 63.665 |
| 12 | 16 | 4.961 | 17.544 | 22.463 | 40.007 |
| 24 | 16 | 8.218 | 30.111 | 23.880 | 53.991 |
| 52 | 16 | 16.247 | 68.698 | 27.507 | 96.205 |

If `RMSE_std` does not grow with the horizon, the models are still indistinguishable and the longer horizon did not help.

## Skill against the two floors

| model | beats persistence at | beats seasonal_naive at | best horizon (lowest RMSE÷floor) |
| --- | --- | --- | --- |
| arima | 1, 2, 4, 12, 24 | 1, 2, 4, 12, 24 | 1 |
| dualtopo | 4, 12, 24 | 1, 2, 4, 12, 24 | 1 |
| dualtopo_no_bg | 4, 12, 24, 52 | 1, 2, 4, 12, 24, 52 | 4 |
| gnn_corrbinary | 12, 24, 52 | 1, 2, 12, 24, 52 | 12 |
| gnn_geo | 12, 24, 52 | 1, 12, 24, 52 | 24 |
| gnn_multiedge | 12, 24, 52 | 1, 2, 12, 24, 52 | 1 |
| gnn_multiedge_covid_rsv | 2, 4, 12, 24, 52 | 1, 2, 4, 12, 24, 52 | 1 |
| gnn_multiedge_leaknorm | 12, 24, 52 | 1, 2, 12, 24, 52 | 2 |
| gnn_multiedge_level | 12, 24, 52 | 12, 24, 52 | 12 |
| gnn_multiedge_rt | 12, 24, 52 | 1, 2, 4, 12, 24, 52 | 12 |
| gnn_multiedge_season | 4, 12, 24, 52 | 1, 2, 4, 12, 24, 52 | 12 |
| gnn_multiedge_season_level | 4, 12, 24, 52 | 4, 12, 24, 52 | 12 |
| gnn_uniform | 12, 24, 52 | 1, 2, 12, 24, 52 | 24 |
| lstm | 1, 2, 4, 12, 24, 52 | 1, 2, 4, 12, 52 | 1 |

## Horizon 1

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| lstm | 14.657 | 7.846 | 0.883 | 627 |  |
| arima | 15.506 | 9.092 | 0.871 | 627 |  |
| persistence | 15.806 | 8.937 | 0.871 | 627 |  |
| gnn_multiedge_covid_rsv | 18.553 | 12.014 | 0.869 | 627 |  |
| gnn_multiedge | 24.898 | 15.366 | 0.835 | 627 |  |
| dualtopo | 28.915 | 18.202 | 0.417 | 627 |  |
| gnn_multiedge_season | 28.928 | 17.645 | 0.836 | 627 |  |
| gnn_uniform | 28.953 | 16.729 | 0.830 | 627 |  |
| dualtopo_no_bg | 29.030 | 18.327 | 0.412 | 627 |  |
| gnn_corrbinary | 31.788 | 19.132 | 0.816 | 627 |  |
| gnn_multiedge_rt | 32.978 | 19.328 | 0.790 | 627 |  |
| gnn_geo | 36.452 | 21.707 | 0.787 | 627 |  |
| gnn_multiedge_leaknorm | 37.767 | 21.474 | 0.802 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |
| gnn_multiedge_level | 50.202 | 28.276 | 0.623 | 627 |  |
| gnn_multiedge_season_level | 50.619 | 28.300 | 0.700 | 627 |  |

## Horizon 2

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | 19.981 | 10.729 | 0.769 | 627 |  |
| lstm | 21.361 | 10.944 | 0.731 | 627 |  |
| arima | 21.552 | 12.120 | 0.739 | 627 |  |
| persistence | 23.840 | 12.070 | 0.706 | 627 |  |
| gnn_multiedge_leaknorm | 24.883 | 14.192 | 0.784 | 627 |  |
| gnn_multiedge | 26.220 | 15.712 | 0.766 | 627 |  |
| gnn_multiedge_rt | 27.437 | 15.485 | 0.742 | 627 |  |
| gnn_multiedge_season | 28.387 | 16.607 | 0.747 | 627 |  |
| dualtopo | 29.104 | 18.133 | 0.400 | 627 |  |
| dualtopo_no_bg | 29.239 | 18.444 | 0.400 | 627 |  |
| gnn_corrbinary | 30.968 | 18.420 | 0.722 | 627 |  |
| gnn_uniform | 34.181 | 19.207 | 0.700 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |
| gnn_multiedge_season_level | 40.480 | 24.074 | 0.646 | 627 |  |
| gnn_geo | 45.315 | 26.064 | 0.640 | 627 |  |
| gnn_multiedge_level | 47.278 | 26.685 | 0.580 | 627 |  |

## Horizon 4

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_multiedge_covid_rsv | 23.907 | 13.861 | 0.648 | 627 |  |
| lstm | 26.670 | 13.612 | 0.540 | 627 |  |
| gnn_multiedge_season | 28.537 | 15.327 | 0.631 | 627 |  |
| arima | 28.919 | 17.265 | 0.467 | 627 |  |
| dualtopo_no_bg | 29.024 | 18.250 | 0.410 | 627 |  |
| dualtopo | 29.199 | 18.487 | 0.405 | 627 |  |
| gnn_multiedge_season_level | 29.211 | 16.165 | 0.602 | 627 |  |
| persistence | 34.910 | 17.464 | 0.372 | 627 |  |
| gnn_multiedge_rt | 38.704 | 21.364 | 0.447 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |
| gnn_multiedge | 41.341 | 23.433 | 0.485 | 627 |  |
| gnn_corrbinary | 42.354 | 23.759 | 0.459 | 627 |  |
| gnn_multiedge_level | 46.106 | 26.284 | 0.493 | 627 |  |
| gnn_multiedge_leaknorm | 47.607 | 26.426 | 0.415 | 627 |  |
| gnn_uniform | 49.164 | 26.089 | 0.445 | 627 |  |
| gnn_geo | 63.665 | 33.855 | 0.374 | 627 |  |

## Horizon 12

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season_level | 22.463 | 12.369 | 0.694 | 627 |  |
| gnn_multiedge_season | 23.352 | 13.487 | 0.672 | 627 |  |
| gnn_multiedge_level | 25.311 | 13.189 | 0.594 | 627 |  |
| gnn_corrbinary | 26.233 | 15.096 | 0.548 | 627 |  |
| gnn_multiedge_rt | 26.885 | 16.079 | 0.636 | 627 |  |
| gnn_geo | 27.728 | 14.841 | 0.476 | 627 |  |
| gnn_multiedge | 27.829 | 15.046 | 0.475 | 627 |  |
| dualtopo_no_bg | 29.028 | 17.980 | 0.400 | 627 |  |
| dualtopo | 29.060 | 18.054 | 0.400 | 627 |  |
| gnn_uniform | 29.913 | 16.111 | 0.379 | 627 |  |
| arima | 30.179 | 20.072 | 0.396 | 627 |  |
| gnn_multiedge_leaknorm | 30.748 | 17.613 | 0.417 | 627 |  |
| gnn_multiedge_covid_rsv | 31.974 | 21.861 | 0.535 | 627 |  |
| lstm | 33.385 | 20.019 | 0.342 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |
| persistence | 40.007 | 22.119 | 0.169 | 627 |  |

## Horizon 24

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_multiedge_season | 23.880 | 15.395 | 0.742 | 627 |  |
| gnn_multiedge_season_level | 24.824 | 15.669 | 0.751 | 627 |  |
| gnn_multiedge_leaknorm | 25.039 | 16.438 | 0.741 | 627 |  |
| gnn_uniform | 25.092 | 16.907 | 0.740 | 627 |  |
| gnn_multiedge_covid_rsv | 25.179 | 16.717 | 0.729 | 627 |  |
| gnn_multiedge_level | 25.584 | 16.424 | 0.751 | 627 |  |
| gnn_geo | 26.230 | 17.430 | 0.755 | 627 |  |
| gnn_multiedge | 26.627 | 16.844 | 0.751 | 627 |  |
| arima | 28.064 | 17.643 | 0.470 | 627 |  |
| gnn_multiedge_rt | 28.804 | 18.534 | 0.662 | 627 |  |
| dualtopo_no_bg | 30.807 | 21.248 | 0.401 | 627 |  |
| dualtopo | 30.837 | 21.291 | 0.401 | 627 |  |
| gnn_corrbinary | 33.521 | 21.230 | 0.742 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |
| lstm | 42.138 | 26.844 | 0.613 | 627 |  |
| persistence | 53.991 | 30.600 | -0.146 | 627 |  |

## Horizon 52

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_multiedge_level | 27.507 | 15.618 | 0.518 | 627 |  |
| lstm | 29.917 | 20.284 | 0.445 | 627 |  |
| gnn_geo | 29.981 | 15.509 | 0.385 | 627 |  |
| gnn_multiedge_leaknorm | 30.069 | 16.639 | 0.428 | 627 |  |
| dualtopo_no_bg | 30.462 | 20.700 | 0.400 | 627 |  |
| gnn_multiedge_season_level | 31.331 | 18.211 | 0.497 | 627 |  |
| gnn_multiedge_season | 31.741 | 17.712 | 0.377 | 627 |  |
| gnn_multiedge | 31.974 | 18.154 | 0.435 | 627 |  |
| gnn_uniform | 32.189 | 17.620 | 0.370 | 627 |  |
| gnn_multiedge_rt | 32.546 | 17.925 | 0.335 | 627 |  |
| gnn_corrbinary | 33.593 | 17.916 | 0.284 | 627 |  |
| gnn_multiedge_covid_rsv | 33.931 | 17.596 | 0.267 | 627 |  |
| persistence | 39.835 | 19.810 | 0.417 | 627 | identical at this horizon by construction |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 | identical at this horizon by construction |
| arima | 39.992 | 19.109 | 0.412 | 627 |  |
| dualtopo | 96.205 | 39.690 | 0.152 | 627 |  |

### Reading the naive baselines

`persistence` predicts the last value the forecaster could actually see, so at horizon *h* it reaches back *h* weeks. `seasonal_naive` reaches back 52. At horizon 52 those are the same week, so the two models are identical there by construction — not a bug, and not two independent baselines.

