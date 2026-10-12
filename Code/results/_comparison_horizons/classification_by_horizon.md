# Classify the week, or forecast the rate? — horizons 1, 2, 4

Every rate model is banded by its point forecast; `xgb_severity` is trained to output the band directly. Same cut points, same weeks, same metrics.

## Across all four bands, how often was the band right? (macro F1)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| lstm | point | 0.602 | 0.404 | 0.388 |
| xgb_severity | argmax | 0.393 | 0.313 | 0.334 |
| xgboost | point | 0.546 | 0.385 | 0.324 |
| arima | point | 0.639 | 0.460 | 0.298 |
| gnn_st | point | 0.716 | 0.532 | 0.297 |
| persistence | point | 0.638 | 0.458 | 0.280 |
| seasonal_naive | point | 0.240 | 0.240 | 0.240 |

## How well does it rank the weeks that turned out moderate or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| gnn_st | point | 0.915 | 0.783 | 0.534 |
| xgboost | point | 0.778 | 0.597 | 0.496 |
| xgb_severity | argmax | 0.683 | 0.563 | 0.426 |
| lstm | point | 0.862 | 0.627 | 0.388 |
| arima | point | 0.804 | 0.628 | 0.330 |
| seasonal_naive | point | 0.269 | 0.269 | 0.269 |
| persistence | point | 0.835 | 0.608 | 0.259 |

## How well does it rank the weeks that turned out high or worse? (PR-AUC)

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| gnn_st | point | 0.883 | 0.746 | 0.369 |
| xgboost | point | 0.780 | 0.530 | 0.334 |
| lstm | point | 0.815 | 0.489 | 0.223 |
| arima | point | 0.801 | 0.642 | 0.183 |
| xgb_severity | argmax | 0.644 | 0.460 | 0.175 |
| seasonal_naive | point | 0.133 | 0.133 | 0.133 |
| persistence | point | 0.761 | 0.508 | 0.111 |

## Every model and band edge (macro F1)

The lower edge is the optimistic call, the upper edge the cautious one.

| model | bound | h=1 | h=2 | h=4 |
| --- | --- | --- | --- | --- |
| arima | lower95 | 0.398 | 0.349 | 0.240 |
| arima | lower99 | 0.287 | 0.241 | 0.240 |
| arima | point | 0.639 | 0.460 | 0.298 |
| arima | upper95 | 0.454 | 0.367 | 0.178 |
| arima | upper99 | 0.379 | 0.305 | 0.059 |
| dualtopo | lower95 | 0.240 | 0.240 | 0.240 |
| dualtopo | lower99 | 0.240 | 0.240 | 0.240 |
| dualtopo | point | 0.280 | 0.280 | 0.280 |
| dualtopo | upper95 | 0.234 | 0.219 | 0.231 |
| dualtopo | upper99 | 0.228 | 0.228 | 0.228 |
| gat | lower95 | 0.313 | 0.292 | 0.266 |
| gat | lower99 | 0.270 | 0.288 | 0.240 |
| gat | point | 0.338 | 0.327 | 0.252 |
| gat | upper95 | 0.426 | 0.303 | 0.232 |
| gat | upper99 | 0.404 | 0.294 | 0.229 |
| gnn_cascade | lower95 |  | 0.319 |  |
| gnn_cascade | lower99 |  | 0.349 |  |
| gnn_cascade | point |  | 0.540 |  |
| gnn_cascade | upper95 |  | 0.430 |  |
| gnn_cascade | upper99 |  | 0.391 |  |
| gnn_st | lower95 | 0.390 | 0.319 | 0.258 |
| gnn_st | lower99 | 0.379 | 0.348 | 0.240 |
| gnn_st | point | 0.716 | 0.532 | 0.297 |
| gnn_st | upper95 | 0.500 | 0.439 | 0.366 |
| gnn_st | upper99 | 0.461 | 0.403 | 0.277 |
| gnn_st_lagsonly | lower95 | 0.445 | 0.348 | 0.240 |
| gnn_st_lagsonly | lower99 | 0.383 | 0.241 | 0.240 |
| gnn_st_lagsonly | point | 0.718 | 0.517 | 0.298 |
| gnn_st_lagsonly | upper95 | 0.475 | 0.438 | 0.323 |
| gnn_st_lagsonly | upper99 | 0.452 | 0.384 | 0.240 |
| gnn_st_noglobals | lower95 | 0.390 | 0.319 | 0.258 |
| gnn_st_noglobals | lower99 | 0.379 | 0.348 | 0.240 |
| gnn_st_noglobals | point | 0.716 | 0.532 | 0.297 |
| gnn_st_noglobals | upper95 | 0.487 | 0.437 | 0.366 |
| gnn_st_noglobals | upper99 | 0.463 | 0.403 | 0.277 |
| lstm | lower95 | 0.418 | 0.303 | 0.274 |
| lstm | lower99 | 0.364 | 0.257 | 0.240 |
| lstm | point | 0.602 | 0.404 | 0.388 |
| lstm | upper95 | 0.495 | 0.415 | 0.307 |
| lstm | upper99 | 0.446 | 0.375 | 0.322 |
| persistence | point | 0.638 | 0.458 | 0.280 |
| seasonal_naive | point | 0.240 | 0.240 | 0.240 |
| xgb_severity | argmax | 0.393 | 0.313 | 0.334 |
| xgboost | lower95 | 0.241 | 0.240 | 0.240 |
| xgboost | lower99 | 0.240 | 0.240 | 0.240 |
| xgboost | point | 0.546 | 0.385 | 0.324 |
| xgboost | upper95 | 0.336 | 0.285 | 0.216 |
| xgboost | upper99 | 0.256 | 0.199 | 0.153 |
