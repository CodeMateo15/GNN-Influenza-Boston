# Classify the week, or forecast the rate? — horizons 1, 2, 4

Every rate model is banded by its point forecast; `xgb_severity` is trained to output the band directly. Same cut points, same weeks, same metrics.

## Across all four bands, how often was the band right? (macro F1)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| gnn_st | point | 0.646 | 0.582 | 0.572 |
| persistence | point | 0.637 | 0.576 | 0.530 |
| seasonal_naive | point | 0.497 | 0.497 | 0.497 |
| xgboost | point | 0.579 | 0.528 | 0.497 |
| xgb_severity | argmax | 0.485 | 0.511 | 0.449 |
| arima | point | 0.551 | 0.466 | 0.430 |
| lstm | point | 0.489 | 0.444 | 0.398 |

## How well does it rank the weeks that turned out moderate or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| gnn_st | point | 0.965 | 0.954 | 0.908 |
| persistence | point | 0.963 | 0.945 | 0.886 |
| arima | point | 0.908 | 0.875 | 0.860 |
| xgb_severity | argmax | 0.904 | 0.893 | 0.831 |
| xgboost | point | 0.861 | 0.829 | 0.813 |
| seasonal_naive | point | 0.747 | 0.747 | 0.747 |
| lstm | point | 0.758 | 0.725 | 0.705 |

## How well does it rank the weeks that turned out high or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| gnn_st | point | 0.958 | 0.943 | 0.885 |
| persistence | point | 0.955 | 0.937 | 0.873 |
| arima | point | 0.875 | 0.838 | 0.825 |
| xgb_severity | argmax | 0.900 | 0.893 | 0.800 |
| xgboost | point | 0.809 | 0.767 | 0.758 |
| seasonal_naive | point | 0.711 | 0.711 | 0.711 |
| lstm | point | 0.696 | 0.642 | 0.596 |

## Every model and band edge (macro F1)

The lower edge is the optimistic call, the upper edge the cautious one.

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| arima | lower95 | 0.395 | 0.408 | 0.361 |
| arima | lower99 | 0.361 | 0.361 | 0.338 |
| arima | point | 0.551 | 0.466 | 0.430 |
| arima | upper95 | 0.439 | 0.464 | 0.405 |
| arima | upper99 | 0.401 | 0.401 | 0.402 |
| dualtopo | lower95 | 0.378 | 0.265 | 0.222 |
| dualtopo | lower99 | 0.321 | 0.248 | 0.222 |
| dualtopo | point | 0.503 | 0.535 | 0.461 |
| dualtopo | upper95 | 0.440 | 0.356 | 0.327 |
| dualtopo | upper99 | 0.389 | 0.355 | 0.263 |
| gat | lower95 | 0.266 | 0.235 | 0.313 |
| gat | lower99 | 0.252 | 0.222 | 0.285 |
| gat | point | 0.563 | 0.520 | 0.481 |
| gat | upper95 | 0.428 | 0.337 | 0.330 |
| gat | upper99 | 0.368 | 0.302 | 0.286 |
| gnn_st | lower95 | 0.401 | 0.392 | 0.312 |
| gnn_st | lower99 | 0.343 | 0.349 | 0.237 |
| gnn_st | point | 0.646 | 0.582 | 0.572 |
| gnn_st | upper95 | 0.428 | 0.446 | 0.375 |
| gnn_st | upper99 | 0.397 | 0.404 | 0.341 |
| gnn_st_nodemo | lower95 | 0.412 | 0.399 | 0.315 |
| gnn_st_nodemo | lower99 | 0.343 | 0.339 | 0.253 |
| gnn_st_nodemo | point | 0.640 | 0.590 | 0.558 |
| gnn_st_nodemo | upper95 | 0.427 | 0.440 | 0.372 |
| gnn_st_nodemo | upper99 | 0.393 | 0.402 | 0.339 |
| lstm | lower95 | 0.260 | 0.295 | 0.250 |
| lstm | lower99 | 0.227 | 0.241 | 0.222 |
| lstm | point | 0.489 | 0.444 | 0.398 |
| lstm | upper95 | 0.222 | 0.106 | 0.227 |
| lstm | upper99 | 0.087 | 0.071 | 0.086 |
| persistence | point | 0.637 | 0.576 | 0.530 |
| seasonal_naive | point | 0.497 | 0.497 | 0.497 |
| xgb_severity | argmax | 0.485 | 0.511 | 0.449 |
| xgboost | lower95 | 0.222 | 0.260 | 0.269 |
| xgboost | lower99 | 0.222 | 0.247 | 0.244 |
| xgboost | point | 0.579 | 0.528 | 0.497 |
| xgboost | upper95 | 0.084 | 0.345 | 0.316 |
| xgboost | upper99 | 0.084 | 0.295 | 0.285 |
| xgboost_nodemo | lower95 | 0.278 | 0.273 | 0.260 |
| xgboost_nodemo | lower99 | 0.252 | 0.251 | 0.240 |
| xgboost_nodemo | point | 0.572 | 0.534 | 0.510 |
| xgboost_nodemo | upper95 | 0.332 | 0.318 | 0.298 |
| xgboost_nodemo | upper99 | 0.301 | 0.262 | 0.230 |
