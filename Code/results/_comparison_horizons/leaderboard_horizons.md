# Leaderboard by forecast horizon — post_covid

`segment=overall`, `scope=pooled`. RMSE is ILI ED visits per 100,000. Every horizon scores the same 49 target weeks, so the columns are directly comparable.

## Does the horizon separate the models?

| horizon | n_models | RMSE_std | max_minus_min | min | max |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 9.108 | 28.124 | 11.711 | 39.835 |
| 2 | 10 | 7.108 | 22.829 | 17.007 | 39.835 |
| 4 | 10 | 5.782 | 16.934 | 22.901 | 39.835 |

If `RMSE_std` does not grow with the horizon, the models are still indistinguishable and the longer horizon did not help.

## Skill against the two floors

| model | beats persistence at | beats seasonal_naive at | best horizon (lowest RMSE÷floor) |
| --- | --- | --- | --- |
| arima | 1, 2, 4 | 1, 2, 4 | 1 |
| dualtopo | 4 | 1, 2, 4 | 1 |
| gat | 4 | 1, 2, 4 | 1 |
| gnn_st | 1, 2, 4 | 1, 2, 4 | 1 |
| gnn_st_lagsonly | 1, 2, 4 | 1, 2, 4 | 1 |
| gnn_st_noglobals | 1, 2, 4 | 1, 2, 4 | 1 |
| lstm | 1, 2, 4 | 1, 2, 4 | 1 |
| xgboost | 1, 2, 4 | 1, 2, 4 | 1 |

## Horizon 1

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_st_noglobals | 11.711 | 6.709 | 0.927 | 627 |  |
| gnn_st | 11.770 | 6.735 | 0.927 | 627 |  |
| gnn_st_lagsonly | 12.342 | 6.893 | 0.919 | 627 |  |
| lstm | 14.657 | 7.846 | 0.883 | 627 |  |
| arima | 15.506 | 9.092 | 0.871 | 627 |  |
| xgboost | 15.618 | 8.883 | 0.866 | 627 |  |
| persistence | 15.806 | 8.937 | 0.871 | 627 |  |
| gat | 22.450 | 13.214 | 0.698 | 627 |  |
| dualtopo | 28.915 | 18.202 | 0.417 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |

## Horizon 2

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_st_lagsonly | 17.007 | 8.761 | 0.838 | 627 |  |
| gnn_st | 17.197 | 8.850 | 0.840 | 627 |  |
| gnn_st_noglobals | 17.214 | 8.856 | 0.840 | 627 |  |
| xgboost | 20.292 | 11.070 | 0.758 | 627 |  |
| lstm | 21.361 | 10.944 | 0.731 | 627 |  |
| arima | 21.552 | 12.120 | 0.739 | 627 |  |
| persistence | 23.840 | 12.070 | 0.706 | 627 |  |
| gat | 27.537 | 15.840 | 0.520 | 627 |  |
| dualtopo | 29.104 | 18.133 | 0.400 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |

## Horizon 4

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| xgboost | 22.901 | 12.339 | 0.681 | 627 |  |
| gnn_st | 23.070 | 12.069 | 0.676 | 627 |  |
| gnn_st_noglobals | 23.070 | 12.069 | 0.676 | 627 |  |
| gnn_st_lagsonly | 23.513 | 12.450 | 0.662 | 627 |  |
| lstm | 26.670 | 13.612 | 0.540 | 627 |  |
| arima | 28.919 | 17.266 | 0.467 | 627 |  |
| dualtopo | 29.199 | 18.487 | 0.405 | 627 |  |
| gat | 31.992 | 17.346 | 0.366 | 627 |  |
| persistence | 34.910 | 17.464 | 0.372 | 627 |  |
| seasonal_naive | 39.835 | 19.810 | 0.417 | 627 |  |

### Reading the naive baselines

`persistence` predicts the last value the forecaster could actually see, so at horizon *h* it reaches back *h* weeks. `seasonal_naive` reaches back 52. At horizon 52 those are the same week, so the two models are identical there by construction — not a bug, and not two independent baselines.

