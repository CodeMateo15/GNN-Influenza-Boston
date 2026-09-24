Ranked by **RMSE** within each segment, `scope=pooled`, horizon 2.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 17.197 | 66.040 | 8.850 | 0.840 | 95.534 | blend | train |
| xgboost | post_covid | 20.292 | 81.345 | 11.070 | 0.758 | 97.289 | climatology | None |
| lstm | post_covid | 21.361 | 76.895 | 10.944 | 0.731 | 94.418 | level | train |
| arima | post_covid | 21.552 | 111.014 | 12.120 | 0.739 | 95.853 | level | none |
| persistence | exclude_covid | 23.840 | 74.191 | 12.070 | 0.706 | 92.823 | level | none |
| persistence | post_covid | 23.840 | 74.191 | 12.070 | 0.706 | 93.301 | level | none |
| lstm | exclude_covid | 25.137 | 73.595 | 11.921 | 0.704 | 91.228 | level | train |
| gat | post_covid | 27.537 | 135.886 | 15.840 | 0.520 | 88.836 | level | None |
| dualtopo | post_covid | 29.104 | 205.431 | 18.133 | 0.400 | 87.081 | level | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |
| arima | exclude_covid | 42.766 | 120.113 | 15.046 | 0.467 | 93.142 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 22.312 | 64.183 | 12.489 | 0.820 | 92.614 | blend | train |
| xgboost | post_covid | 26.483 | 80.813 | 15.991 | 0.721 | 96.307 | climatology | None |
| arima | post_covid | 27.429 | 80.316 | 15.770 | 0.720 | 92.614 | level | none |
| lstm | post_covid | 27.783 | 62.935 | 15.443 | 0.702 | 90.057 | level | train |
| persistence | exclude_covid | 31.166 | 76.638 | 17.825 | 0.667 | 88.636 | level | none |
| persistence | post_covid | 31.166 | 76.638 | 17.825 | 0.667 | 89.489 | level | none |
| lstm | exclude_covid | 32.738 | 65.835 | 17.045 | 0.671 | 84.659 | level | train |
| dualtopo | post_covid | 33.653 | 106.322 | 18.898 | 0.499 | 83.807 | level | train |
| gat | post_covid | 35.028 | 98.831 | 20.872 | 0.469 | 81.534 | level | None |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |
| arima | exclude_covid | 56.387 | 108.370 | 21.196 | 0.419 | 88.920 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 6.088 | 68.417 | 4.193 | 0.804 | 99.273 | blend | train |
| xgboost | post_covid | 6.410 | 82.027 | 4.772 | 0.798 | 98.545 | climatology | None |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| lstm | post_covid | 7.234 | 94.765 | 5.186 | 0.777 | 100.000 | level | train |
| persistence | exclude_covid | 7.249 | 71.059 | 4.704 | 0.732 | 98.182 | level | none |
| persistence | post_covid | 7.249 | 71.059 | 4.704 | 0.732 | 98.182 | level | none |
| lstm | exclude_covid | 8.297 | 83.527 | 5.361 | 0.790 | 99.636 | level | train |
| arima | post_covid | 9.798 | 150.309 | 7.448 | 0.735 | 100.000 | level | none |
| arima | exclude_covid | 10.008 | 135.145 | 7.175 | 0.722 | 98.545 | level | none |
| gat | post_covid | 12.583 | 183.316 | 9.399 | 0.705 | 98.182 | level | None |
| dualtopo | post_covid | 21.947 | 332.290 | 17.153 | 0.581 | 91.273 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_st (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_st (post_covid)`
- **Off-season (Apr–Sep)**: `gnn_st (post_covid)`

The same model leads every segment, so the ranking is robust to which part of the year you score.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
