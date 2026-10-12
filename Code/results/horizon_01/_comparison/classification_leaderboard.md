# Severity bands as a classification problem — horizon 1

One citywide set of cut points for every neighborhood-week (IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 627 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_st_lagsonly | point | 0.962 | 0.718 | 0.737 | 0.702 |
| gnn_st_noglobals | point | 0.962 | 0.716 | 0.731 | 0.702 |
| gnn_st | point | 0.962 | 0.716 | 0.731 | 0.702 |
| arima | point | 0.941 | 0.639 | 0.649 | 0.629 |
| persistence | point | 0.941 | 0.638 | 0.638 | 0.638 |
| lstm | point | 0.954 | 0.602 | 0.684 | 0.554 |
| xgboost | point | 0.936 | 0.546 | 0.599 | 0.509 |
| gnn_st | upper95 | 0.863 | 0.500 | 0.444 | 0.637 |
| lstm | upper95 | 0.888 | 0.495 | 0.458 | 0.566 |
| gnn_st_noglobals | upper95 | 0.866 | 0.487 | 0.435 | 0.611 |
| gnn_st_lagsonly | upper95 | 0.863 | 0.475 | 0.424 | 0.602 |
| gnn_st_noglobals | upper99 | 0.834 | 0.463 | 0.414 | 0.613 |
| gnn_st | upper99 | 0.831 | 0.461 | 0.412 | 0.612 |
| arima | upper95 | 0.820 | 0.454 | 0.406 | 0.617 |
| gnn_st_lagsonly | upper99 | 0.828 | 0.452 | 0.405 | 0.602 |
| lstm | upper99 | 0.856 | 0.446 | 0.404 | 0.555 |
| gnn_st_lagsonly | lower95 | 0.935 | 0.445 | 0.640 | 0.387 |
| gat | upper95 | 0.833 | 0.426 | 0.398 | 0.516 |
| lstm | lower95 | 0.933 | 0.418 | 0.519 | 0.378 |
| gat | upper99 | 0.766 | 0.404 | 0.378 | 0.536 |
| arima | lower95 | 0.933 | 0.398 | 0.668 | 0.346 |
| xgb_severity | argmax | 0.901 | 0.393 | 0.370 | 0.429 |
| gnn_st_noglobals | lower95 | 0.933 | 0.390 | 0.468 | 0.359 |
| gnn_st | lower95 | 0.933 | 0.390 | 0.468 | 0.359 |
| gnn_st_lagsonly | lower99 | 0.931 | 0.383 | 0.630 | 0.337 |
| arima | upper99 | 0.761 | 0.379 | 0.352 | 0.548 |
| gnn_st | lower99 | 0.931 | 0.379 | 0.598 | 0.337 |
| gnn_st_noglobals | lower99 | 0.931 | 0.379 | 0.590 | 0.337 |
| lstm | lower99 | 0.930 | 0.364 | 0.547 | 0.328 |
| gat | point | 0.904 | 0.338 | 0.357 | 0.328 |
| xgboost | upper95 | 0.667 | 0.336 | 0.333 | 0.487 |
| gat | lower95 | 0.928 | 0.313 | 0.401 | 0.295 |
| arima | lower99 | 0.927 | 0.287 | 0.483 | 0.275 |
| dualtopo | point | 0.877 | 0.280 | 0.271 | 0.297 |
| gat | lower99 | 0.928 | 0.270 | 0.306 | 0.268 |
| xgboost | upper99 | 0.544 | 0.256 | 0.293 | 0.418 |
| xgboost | lower95 | 0.925 | 0.241 | 0.232 | 0.250 |
| dualtopo | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| xgboost | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| dualtopo | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| seasonal_naive | point | 0.842 | 0.240 | 0.244 | 0.236 |
| dualtopo | upper95 | 0.644 | 0.234 | 0.261 | 0.299 |
| dualtopo | upper99 | 0.616 | 0.228 | 0.260 | 0.318 |

## If it had raised an alert for 'moderate or worse', would it have been right?

47 such weeks, base rate 0.075. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.075, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_noglobals | lower95 | 1.000 | 0.298 | 0.459 | 0.990 | 0.916 |
| gnn_st | lower95 | 1.000 | 0.298 | 0.459 | 0.990 | 0.915 |
| gnn_st_noglobals | upper95 | 0.442 | 0.979 | 0.609 | 0.990 | 0.915 |
| gnn_st_noglobals | upper99 | 0.379 | 1.000 | 0.550 | 0.990 | 0.915 |
| gnn_st | point | 0.884 | 0.809 | 0.844 | 0.990 | 0.915 |
| gnn_st_noglobals | point | 0.884 | 0.809 | 0.844 | 0.990 | 0.915 |
| gnn_st_lagsonly | lower95 | 1.000 | 0.319 | 0.484 | 0.990 | 0.914 |
| gnn_st | upper99 | 0.373 | 1.000 | 0.543 | 0.990 | 0.914 |
| gnn_st | upper95 | 0.430 | 0.979 | 0.597 | 0.990 | 0.914 |
| gnn_st_lagsonly | upper99 | 0.370 | 1.000 | 0.540 | 0.989 | 0.913 |
| gnn_st_lagsonly | upper95 | 0.438 | 0.979 | 0.605 | 0.989 | 0.913 |
| gnn_st_lagsonly | point | 0.881 | 0.787 | 0.831 | 0.989 | 0.913 |
| gnn_st_noglobals | lower99 | 1.000 | 0.255 | 0.407 | 0.981 | 0.909 |
| gnn_st | lower99 | 1.000 | 0.234 | 0.379 | 0.981 | 0.906 |
| gnn_st_lagsonly | lower99 | 1.000 | 0.191 | 0.321 | 0.971 | 0.898 |
| lstm | point | 0.912 | 0.660 | 0.765 | 0.984 | 0.862 |
| lstm | lower95 | 1.000 | 0.255 | 0.407 | 0.984 | 0.862 |
| lstm | upper95 | 0.506 | 0.957 | 0.662 | 0.984 | 0.862 |
| lstm | upper99 | 0.418 | 0.979 | 0.586 | 0.984 | 0.862 |
| lstm | lower99 | 1.000 | 0.170 | 0.291 | 0.965 | 0.846 |
| persistence | point | 0.723 | 0.723 | 0.723 | 0.974 | 0.835 |
| arima | point | 0.727 | 0.681 | 0.703 | 0.968 | 0.804 |
| arima | upper99 | 0.277 | 0.979 | 0.432 | 0.968 | 0.804 |
| arima | upper95 | 0.346 | 0.979 | 0.511 | 0.968 | 0.804 |
| xgboost | upper99 | 0.157 | 1.000 | 0.272 | 0.970 | 0.778 |
| xgboost | upper95 | 0.210 | 1.000 | 0.347 | 0.970 | 0.778 |
| xgboost | point | 0.800 | 0.596 | 0.683 | 0.970 | 0.778 |
| arima | lower95 | 1.000 | 0.213 | 0.351 | 0.930 | 0.776 |
| xgb_severity | argmax | 0.509 | 0.617 | 0.558 | 0.952 | 0.683 |
| arima | lower99 | 1.000 | 0.128 | 0.226 | 0.805 | 0.622 |
| gat | point | 0.500 | 0.404 | 0.447 | 0.915 | 0.560 |
| gat | upper95 | 0.328 | 0.809 | 0.466 | 0.915 | 0.560 |
| gat | upper99 | 0.250 | 0.872 | 0.389 | 0.915 | 0.560 |
| gat | lower95 | 0.889 | 0.170 | 0.286 | 0.911 | 0.560 |
| gat | lower99 | 1.000 | 0.170 | 0.291 | 0.866 | 0.538 |
| xgboost | lower95 | 1.000 | 0.043 | 0.082 | 0.691 | 0.426 |
| seasonal_naive | point | 0.264 | 0.404 | 0.319 | 0.862 | 0.269 |
| dualtopo | upper95 | 0.152 | 0.702 | 0.250 | 0.778 | 0.241 |
| dualtopo | upper99 | 0.140 | 0.702 | 0.233 | 0.778 | 0.241 |
| dualtopo | point | 0.245 | 0.255 | 0.250 | 0.778 | 0.241 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.727 | 0.226 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.656 | 0.194 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.553 | 0.173 |

## If it had raised an alert for 'high or worse', would it have been right?

19 such weeks, base rate 0.030. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.030, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_noglobals | upper95 | 0.450 | 0.947 | 0.610 | 0.995 | 0.888 |
| gnn_st | lower99 | 1.000 | 0.316 | 0.480 | 0.995 | 0.887 |
| gnn_st_noglobals | point | 0.833 | 0.789 | 0.811 | 0.995 | 0.886 |
| gnn_st_noglobals | lower99 | 1.000 | 0.316 | 0.480 | 0.995 | 0.885 |
| gnn_st_noglobals | lower95 | 1.000 | 0.316 | 0.480 | 0.995 | 0.884 |
| gnn_st_noglobals | upper99 | 0.380 | 1.000 | 0.551 | 0.994 | 0.883 |
| gnn_st | point | 0.833 | 0.789 | 0.811 | 0.994 | 0.883 |
| gnn_st | lower95 | 1.000 | 0.316 | 0.480 | 0.995 | 0.882 |
| gnn_st | upper99 | 0.365 | 1.000 | 0.535 | 0.994 | 0.880 |
| gnn_st | upper95 | 0.463 | 1.000 | 0.633 | 0.994 | 0.877 |
| gnn_st_lagsonly | lower99 | 1.000 | 0.263 | 0.417 | 0.994 | 0.865 |
| gnn_st_lagsonly | lower95 | 1.000 | 0.316 | 0.480 | 0.994 | 0.863 |
| gnn_st_lagsonly | point | 0.833 | 0.789 | 0.811 | 0.993 | 0.857 |
| gnn_st_lagsonly | upper95 | 0.429 | 0.947 | 0.590 | 0.993 | 0.857 |
| gnn_st_lagsonly | upper99 | 0.373 | 1.000 | 0.543 | 0.993 | 0.857 |
| lstm | point | 0.917 | 0.579 | 0.710 | 0.986 | 0.815 |
| lstm | lower95 | 0.875 | 0.368 | 0.519 | 0.986 | 0.815 |
| lstm | upper95 | 0.500 | 0.842 | 0.627 | 0.986 | 0.815 |
| lstm | upper99 | 0.410 | 0.842 | 0.552 | 0.986 | 0.815 |
| lstm | lower99 | 0.833 | 0.263 | 0.400 | 0.986 | 0.815 |
| arima | point | 0.778 | 0.737 | 0.757 | 0.987 | 0.801 |
| arima | upper99 | 0.261 | 0.947 | 0.409 | 0.987 | 0.801 |
| arima | upper95 | 0.310 | 0.947 | 0.468 | 0.987 | 0.801 |
| arima | lower95 | 1.000 | 0.263 | 0.417 | 0.987 | 0.801 |
| xgboost | upper95 | 0.202 | 1.000 | 0.336 | 0.991 | 0.780 |
| xgboost | point | 0.714 | 0.526 | 0.606 | 0.991 | 0.780 |
| xgboost | upper99 | 0.151 | 1.000 | 0.262 | 0.991 | 0.780 |
| arima | lower99 | 1.000 | 0.105 | 0.190 | 0.941 | 0.775 |
| persistence | point | 0.737 | 0.737 | 0.737 | 0.985 | 0.761 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.865 | 0.647 |
| xgb_severity | argmax | 0.769 | 0.526 | 0.625 | 0.977 | 0.644 |
| gat | point | 0.500 | 0.263 | 0.345 | 0.956 | 0.438 |
| gat | upper99 | 0.310 | 0.684 | 0.426 | 0.956 | 0.438 |
| gat | upper95 | 0.353 | 0.632 | 0.453 | 0.956 | 0.438 |
| gat | lower95 | 0.667 | 0.105 | 0.182 | 0.956 | 0.438 |
| gat | lower99 | 0.000 | 0.000 | 0.000 | 0.936 | 0.431 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.632 | 0.285 |
| seasonal_naive | point | 0.091 | 0.158 | 0.115 | 0.893 | 0.133 |
| dualtopo | upper99 | 0.112 | 0.579 | 0.188 | 0.876 | 0.125 |
| dualtopo | upper95 | 0.108 | 0.368 | 0.167 | 0.876 | 0.125 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.876 | 0.125 |
| dualtopo | point | 0.000 | 0.000 | 0.000 | 0.876 | 0.125 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.722 | 0.091 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 567 | 13 | 0 | 0 |
| moderate | 11 | 12 | 3 | 2 |
| high | 2 | 2 | 4 | 1 |
| very high | 0 | 1 | 2 | 7 |

**seasonal_naive**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 527 | 29 | 10 | 14 |
| moderate | 21 | 1 | 2 | 4 |
| high | 5 | 3 | 0 | 1 |
| very high | 2 | 6 | 2 | 0 |

**arima**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 568 | 12 | 0 | 0 |
| moderate | 13 | 11 | 2 | 2 |
| high | 2 | 2 | 4 | 1 |
| very high | 0 | 1 | 2 | 7 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 577 | 3 | 0 | 0 |
| moderate | 13 | 14 | 0 | 1 |
| high | 3 | 2 | 2 | 2 |
| very high | 0 | 3 | 2 | 5 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 573 | 7 | 0 | 0 |
| moderate | 18 | 6 | 3 | 1 |
| high | 1 | 4 | 3 | 1 |
| very high | 0 | 4 | 1 | 5 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 575 | 5 | 0 | 0 |
| moderate | 9 | 16 | 2 | 1 |
| high | 0 | 4 | 4 | 1 |
| very high | 0 | 0 | 2 | 8 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 552 | 27 | 1 | 0 |
| moderate | 17 | 9 | 2 | 0 |
| high | 1 | 4 | 4 | 0 |
| very high | 0 | 4 | 6 | 0 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
