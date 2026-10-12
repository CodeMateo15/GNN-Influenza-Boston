# Classify the week, or forecast the rate? — horizons 1, 2, 4

Every rate model is banded by its point forecast; `xgb_severity` is trained to output the band directly. Same cut points, same weeks, same metrics.

## Across all four bands, how often was the band right? (macro F1)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| seasonal_naive | point | 0.473 | 0.473 | 0.473 |
| xgboost | point | 0.521 | 0.457 | 0.470 |
| gnn_st | point | 0.591 | 0.536 | 0.465 |
| lstm | point | 0.540 | 0.493 | 0.438 |
| xgb_severity | argmax | 0.505 | 0.439 | 0.428 |
| arima | point | 0.468 | 0.429 | 0.413 |
| persistence | point | 0.558 | 0.502 | 0.395 |

## How well does it rank the weeks that turned out moderate or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| xgboost | point | 0.835 | 0.828 | 0.847 |
| gnn_st | point | 0.903 | 0.875 | 0.837 |
| seasonal_naive | point | 0.788 | 0.788 | 0.788 |
| xgb_severity | argmax | 0.849 | 0.792 | 0.785 |
| arima | point | 0.819 | 0.757 | 0.735 |
| lstm | point | 0.871 | 0.803 | 0.699 |
| persistence | point | 0.856 | 0.797 | 0.696 |

## How well does it rank the weeks that turned out high or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| xgboost | point | 0.702 | 0.572 | 0.740 |
| gnn_st | point | 0.871 | 0.760 | 0.678 |
| xgb_severity | argmax | 0.572 | 0.496 | 0.611 |
| seasonal_naive | point | 0.500 | 0.500 | 0.500 |
| arima | point | 0.731 | 0.509 | 0.452 |
| lstm | point | 0.829 | 0.660 | 0.446 |
| persistence | point | 0.765 | 0.569 | 0.381 |

## Every model and band edge (macro F1)

The lower edge is the optimistic call, the upper edge the cautious one.

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| arima | lower95 | 0.345 | 0.245 | 0.225 |
| arima | lower99 | 0.236 | 0.231 | 0.225 |
| arima | point | 0.468 | 0.429 | 0.413 |
| arima | upper95 | 0.477 | 0.389 | 0.279 |
| arima | upper99 | 0.401 | 0.328 | 0.214 |
| dualtopo | lower95 | 0.225 | 0.225 | 0.259 |
| dualtopo | lower99 | 0.225 | 0.225 | 0.240 |
| dualtopo | point | 0.291 | 0.305 | 0.540 |
| dualtopo | upper95 | 0.329 | 0.329 | 0.469 |
| dualtopo | upper99 | 0.350 | 0.347 | 0.440 |
| gat | lower95 | 0.283 | 0.395 | 0.366 |
| gat | lower99 | 0.245 | 0.272 | 0.417 |
| gat | point | 0.477 | 0.482 | 0.330 |
| gat | upper95 | 0.397 | 0.371 | 0.326 |
| gat | upper99 | 0.357 | 0.327 | 0.292 |
| gnn_cascade | lower95 |  | 0.241 |  |
| gnn_cascade | lower99 |  | 0.231 |  |
| gnn_cascade | point |  | 0.574 |  |
| gnn_cascade | upper95 |  | 0.409 |  |
| gnn_cascade | upper99 |  | 0.346 |  |
| gnn_st | lower95 | 0.261 | 0.245 | 0.231 |
| gnn_st | lower99 | 0.233 | 0.226 | 0.225 |
| gnn_st | point | 0.591 | 0.536 | 0.465 |
| gnn_st | upper95 | 0.415 | 0.399 | 0.402 |
| gnn_st | upper99 | 0.342 | 0.336 | 0.326 |
| gnn_st_v2 | lower95 | 0.264 | 0.245 |  |
| gnn_st_v2 | lower99 | 0.237 | 0.226 |  |
| gnn_st_v2 | point | 0.591 | 0.539 |  |
| gnn_st_v2 | upper95 | 0.415 | 0.400 |  |
| gnn_st_v2 | upper99 | 0.342 | 0.345 |  |
| lstm | lower95 | 0.323 | 0.260 | 0.225 |
| lstm | lower99 | 0.233 | 0.226 | 0.225 |
| lstm | point | 0.540 | 0.493 | 0.438 |
| lstm | upper95 | 0.356 | 0.344 | 0.290 |
| lstm | upper99 | 0.310 | 0.292 | 0.232 |
| persistence | point | 0.558 | 0.502 | 0.395 |
| seasonal_naive | point | 0.473 | 0.473 | 0.473 |
| xgb_severity | argmax | 0.505 | 0.439 | 0.428 |
| xgboost | lower95 | 0.240 | 0.245 | 0.226 |
| xgboost | lower99 | 0.226 | 0.226 | 0.225 |
| xgboost | point | 0.521 | 0.457 | 0.470 |
| xgboost | upper95 | 0.450 | 0.414 | 0.434 |
| xgboost | upper99 | 0.351 | 0.342 | 0.319 |
