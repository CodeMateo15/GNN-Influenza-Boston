# Leaderboard by forecast horizon — post_covid

`segment=overall`, `scope=pooled`. RMSE is ILI ED visits per 100,000. Every horizon scores the same 49 target weeks, so the columns are directly comparable.

## Does the horizon separate the models?

| horizon | n_models | RMSE_std | max_minus_min | min | max |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 15.093 | 38.633 | 22.811 | 61.444 |
| 2 | 10 | 14.981 | 36.694 | 27.206 | 63.900 |
| 4 | 10 | 10.886 | 27.320 | 38.800 | 66.120 |

If `RMSE_std` does not grow with the horizon, the models are still indistinguishable and the longer horizon did not help.

## Skill against the two floors

| model | beats persistence at | beats seasonal_naive at | best horizon (lowest RMSE÷floor) |
| --- | --- | --- | --- |
| arima | never | 1, 2, 4 | 1 |
| dualtopo | never | 1 | 1 |
| gat | never | 1, 2, 4 | 1 |
| gnn_st | 1 | 1, 2, 4 | 1 |
| gnn_st_nodemo | 1 | 1, 2, 4 | 1 |
| lstm | never | never | 1 |
| xgboost | never | 1, 2, 4 | 1 |
| xgboost_nodemo | never | 1, 2, 4 | 1 |

## Horizon 1

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_st | 22.811 | 10.235 | 0.953 | 992 |  |
| gnn_st_nodemo | 23.161 | 10.291 | 0.951 | 992 |  |
| persistence | 23.505 | 10.693 | 0.948 | 992 |  |
| arima | 25.767 | 13.797 | 0.937 | 992 |  |
| gat | 43.937 | 20.145 | 0.827 | 992 |  |
| dualtopo | 44.914 | 20.761 | 0.805 | 992 |  |
| xgboost | 48.834 | 20.352 | 0.764 | 992 |  |
| xgboost_nodemo | 50.789 | 21.344 | 0.733 | 992 |  |
| seasonal_naive | 57.413 | 25.473 | 0.645 | 992 |  |
| lstm | 61.444 | 24.252 | 0.561 | 992 |  |

## Horizon 2

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| persistence | 27.206 | 12.984 | 0.931 | 992 |  |
| gnn_st | 27.220 | 12.171 | 0.934 | 992 |  |
| gnn_st_nodemo | 27.467 | 12.286 | 0.933 | 992 |  |
| arima | 31.057 | 17.358 | 0.907 | 992 |  |
| gat | 48.521 | 21.475 | 0.781 | 992 |  |
| xgboost | 53.030 | 21.857 | 0.705 | 992 |  |
| xgboost_nodemo | 53.680 | 22.450 | 0.694 | 992 |  |
| seasonal_naive | 57.416 | 25.476 | 0.645 | 992 |  |
| dualtopo | 59.894 | 25.532 | 0.591 | 992 |  |
| lstm | 63.900 | 26.002 | 0.512 | 992 |  |

## Horizon 4

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| persistence | 38.800 | 18.599 | 0.860 | 992 |  |
| arima | 38.854 | 20.282 | 0.854 | 992 |  |
| gnn_st_nodemo | 39.072 | 17.106 | 0.864 | 992 |  |
| gnn_st | 39.556 | 17.005 | 0.862 | 992 |  |
| gat | 45.510 | 23.158 | 0.784 | 992 |  |
| xgboost | 53.763 | 23.151 | 0.696 | 992 |  |
| xgboost_nodemo | 54.495 | 23.376 | 0.683 | 992 |  |
| seasonal_naive | 57.423 | 25.483 | 0.645 | 992 |  |
| lstm | 64.801 | 28.049 | 0.495 | 992 |  |
| dualtopo | 66.120 | 27.289 | 0.481 | 992 |  |

### Reading the naive baselines

`persistence` predicts the last value the forecaster could actually see, so at horizon *h* it reaches back *h* weeks. `seasonal_naive` reaches back 52. At horizon 52 those are the same week, so the two models are identical there by construction — not a bug, and not two independent baselines.

