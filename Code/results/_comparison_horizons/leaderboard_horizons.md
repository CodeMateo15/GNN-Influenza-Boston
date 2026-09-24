# Leaderboard by forecast horizon — post_covid

`segment=overall`, `scope=pooled`. RMSE is ILI ED visits per 100,000. Every horizon scores the same 49 target weeks, so the columns are directly comparable.

## Does the horizon separate the models?

| horizon | n_models | RMSE_std | max_minus_min | min | max |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 | 3.105 | 9.136 | 7.230 | 16.366 |
| 2 | 9 | 2.557 | 7.850 | 8.516 | 16.366 |
| 4 | 8 | 2.643 | 6.689 | 9.677 | 16.366 |

If `RMSE_std` does not grow with the horizon, the models are still indistinguishable and the longer horizon did not help.

## Skill against the two floors

| model | beats persistence at | beats seasonal_naive at | best horizon (lowest RMSE÷floor) |
| --- | --- | --- | --- |
| arima | 2, 4 | 1, 2, 4 | 1 |
| dualtopo | 4 | 1, 2, 4 | 4 |
| gat | 2 | 1, 2, 4 | 2 |
| gnn_st | 1, 2, 4 | 1, 2, 4 | 1 |
| gnn_st_v2 | 1, 2 | 1, 2 | 1 |
| lstm | 1, 2, 4 | 1, 2, 4 | 1 |
| xgboost | 2, 4 | 1, 2, 4 | 1 |

## Horizon 1

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_st | 7.230 | 4.905 | 0.928 | 901 |  |
| gnn_st_v2 | 7.240 | 4.908 | 0.928 | 901 |  |
| lstm | 8.723 | 6.123 | 0.901 | 901 |  |
| persistence | 9.195 | 6.188 | 0.887 | 901 |  |
| arima | 9.481 | 6.340 | 0.873 | 901 |  |
| xgboost | 9.532 | 6.421 | 0.883 | 901 |  |
| gat | 10.051 | 6.776 | 0.857 | 901 |  |
| dualtopo | 14.368 | 9.436 | 0.686 | 901 |  |
| seasonal_naive | 16.366 | 9.093 | 0.765 | 901 |  |

## Horizon 2

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| gnn_st | 8.516 | 5.811 | 0.902 | 901 |  |
| gnn_st_v2 | 8.579 | 5.842 | 0.901 | 901 |  |
| gat | 9.998 | 6.676 | 0.874 | 901 |  |
| xgboost | 10.394 | 6.877 | 0.855 | 901 |  |
| lstm | 10.465 | 7.241 | 0.847 | 901 |  |
| arima | 11.432 | 7.489 | 0.809 | 901 |  |
| persistence | 11.499 | 7.671 | 0.824 | 901 |  |
| dualtopo | 14.169 | 9.476 | 0.687 | 901 |  |
| seasonal_naive | 16.366 | 9.093 | 0.765 | 901 |  |

## Horizon 4

| model | RMSE | MAE | Corr | n_obs | note |
| --- | --- | --- | --- | --- | --- |
| xgboost | 9.677 | 6.413 | 0.887 | 901 |  |
| dualtopo | 9.939 | 6.653 | 0.870 | 901 |  |
| gnn_st | 9.948 | 6.576 | 0.868 | 901 |  |
| arima | 12.462 | 8.108 | 0.769 | 901 |  |
| lstm | 12.516 | 8.593 | 0.769 | 901 |  |
| persistence | 14.560 | 9.836 | 0.718 | 901 |  |
| gat | 15.464 | 9.415 | 0.735 | 901 |  |
| seasonal_naive | 16.366 | 9.093 | 0.765 | 901 |  |

### Reading the naive baselines

`persistence` predicts the last value the forecaster could actually see, so at horizon *h* it reaches back *h* weeks. `seasonal_naive` reaches back 52. At horizon 52 those are the same week, so the two models are identical there by construction — not a bug, and not two independent baselines.

