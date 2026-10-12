# Severity bands as a classification problem — horizon 2

One citywide set of cut points for every neighborhood-week (IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 627 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_cascade | point | 0.939 | 0.540 | 0.563 | 0.531 |
| gnn_st_noglobals | point | 0.939 | 0.532 | 0.549 | 0.522 |
| gnn_st | point | 0.939 | 0.532 | 0.549 | 0.522 |
| gnn_st_lagsonly | point | 0.935 | 0.517 | 0.553 | 0.491 |
| arima | point | 0.917 | 0.460 | 0.482 | 0.443 |
| persistence | point | 0.909 | 0.458 | 0.458 | 0.458 |
| gnn_st | upper95 | 0.833 | 0.439 | 0.394 | 0.580 |
| gnn_st_lagsonly | upper95 | 0.812 | 0.438 | 0.396 | 0.583 |
| gnn_st_noglobals | upper95 | 0.831 | 0.437 | 0.392 | 0.580 |
| gnn_cascade | upper95 | 0.825 | 0.430 | 0.392 | 0.545 |
| lstm | upper95 | 0.844 | 0.415 | 0.380 | 0.513 |
| lstm | point | 0.914 | 0.404 | 0.439 | 0.382 |
| gnn_st_noglobals | upper99 | 0.781 | 0.403 | 0.367 | 0.588 |
| gnn_st | upper99 | 0.781 | 0.403 | 0.367 | 0.588 |
| gnn_cascade | upper99 | 0.780 | 0.391 | 0.361 | 0.538 |
| xgboost | point | 0.917 | 0.385 | 0.419 | 0.364 |
| gnn_st_lagsonly | upper99 | 0.766 | 0.384 | 0.354 | 0.575 |
| lstm | upper99 | 0.793 | 0.375 | 0.351 | 0.488 |
| arima | upper95 | 0.708 | 0.367 | 0.350 | 0.529 |
| arima | lower95 | 0.930 | 0.349 | 0.733 | 0.312 |
| gnn_cascade | lower99 | 0.930 | 0.349 | 0.692 | 0.312 |
| gnn_st_noglobals | lower99 | 0.930 | 0.348 | 0.671 | 0.312 |
| gnn_st_lagsonly | lower95 | 0.930 | 0.348 | 0.671 | 0.312 |
| gnn_st | lower99 | 0.930 | 0.348 | 0.671 | 0.312 |
| gat | point | 0.892 | 0.327 | 0.341 | 0.318 |
| gnn_st_noglobals | lower95 | 0.928 | 0.319 | 0.402 | 0.300 |
| gnn_st | lower95 | 0.928 | 0.319 | 0.402 | 0.300 |
| gnn_cascade | lower95 | 0.928 | 0.319 | 0.402 | 0.300 |
| xgb_severity | argmax | 0.893 | 0.313 | 0.311 | 0.320 |
| arima | upper99 | 0.565 | 0.305 | 0.323 | 0.532 |
| gat | upper95 | 0.748 | 0.303 | 0.305 | 0.355 |
| lstm | lower95 | 0.928 | 0.303 | 0.547 | 0.284 |
| gat | upper99 | 0.687 | 0.294 | 0.301 | 0.372 |
| gat | lower95 | 0.925 | 0.292 | 0.325 | 0.284 |
| gat | lower99 | 0.928 | 0.288 | 0.420 | 0.276 |
| xgboost | upper95 | 0.558 | 0.285 | 0.310 | 0.503 |
| dualtopo | point | 0.877 | 0.280 | 0.271 | 0.297 |
| lstm | lower99 | 0.927 | 0.257 | 0.316 | 0.259 |
| gnn_st_lagsonly | lower99 | 0.925 | 0.241 | 0.233 | 0.250 |
| arima | lower99 | 0.925 | 0.241 | 0.232 | 0.250 |
| dualtopo | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| dualtopo | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| xgboost | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| xgboost | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| seasonal_naive | point | 0.842 | 0.240 | 0.244 | 0.236 |
| dualtopo | upper99 | 0.616 | 0.228 | 0.260 | 0.318 |
| dualtopo | upper95 | 0.614 | 0.219 | 0.256 | 0.253 |
| xgboost | upper99 | 0.386 | 0.199 | 0.282 | 0.392 |

## If it had raised an alert for 'moderate or worse', would it have been right?

47 such weeks, base rate 0.075. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.075, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | point | 0.762 | 0.681 | 0.719 | 0.969 | 0.791 |
| gnn_cascade | upper99 | 0.295 | 0.979 | 0.453 | 0.969 | 0.789 |
| gnn_cascade | upper95 | 0.347 | 0.915 | 0.503 | 0.969 | 0.789 |
| gnn_st | point | 0.780 | 0.681 | 0.727 | 0.969 | 0.783 |
| gnn_st_noglobals | point | 0.780 | 0.681 | 0.727 | 0.969 | 0.782 |
| gnn_st_lagsonly | point | 0.750 | 0.638 | 0.690 | 0.968 | 0.778 |
| gnn_cascade | lower95 | 1.000 | 0.234 | 0.379 | 0.937 | 0.778 |
| gnn_st_noglobals | upper95 | 0.358 | 0.936 | 0.518 | 0.969 | 0.777 |
| gnn_st | upper95 | 0.361 | 0.936 | 0.521 | 0.969 | 0.776 |
| gnn_st | upper99 | 0.293 | 0.979 | 0.451 | 0.969 | 0.775 |
| gnn_st_noglobals | upper99 | 0.293 | 0.979 | 0.451 | 0.969 | 0.775 |
| gnn_st_lagsonly | upper95 | 0.333 | 0.979 | 0.497 | 0.968 | 0.774 |
| gnn_st_lagsonly | upper99 | 0.277 | 0.979 | 0.432 | 0.968 | 0.772 |
| gnn_st_noglobals | lower95 | 1.000 | 0.234 | 0.379 | 0.945 | 0.772 |
| gnn_st | lower95 | 1.000 | 0.234 | 0.379 | 0.936 | 0.765 |
| gnn_st_lagsonly | lower95 | 1.000 | 0.149 | 0.259 | 0.899 | 0.731 |
| gnn_cascade | lower99 | 1.000 | 0.128 | 0.226 | 0.857 | 0.693 |
| gnn_st_noglobals | lower99 | 1.000 | 0.149 | 0.259 | 0.844 | 0.667 |
| gnn_st | lower99 | 1.000 | 0.149 | 0.259 | 0.844 | 0.667 |
| arima | point | 0.590 | 0.489 | 0.535 | 0.918 | 0.628 |
| arima | upper95 | 0.214 | 0.894 | 0.346 | 0.918 | 0.628 |
| arima | upper99 | 0.157 | 0.979 | 0.271 | 0.918 | 0.628 |
| lstm | upper99 | 0.297 | 0.915 | 0.448 | 0.943 | 0.627 |
| lstm | upper95 | 0.360 | 0.851 | 0.506 | 0.943 | 0.627 |
| lstm | point | 0.571 | 0.426 | 0.488 | 0.943 | 0.627 |
| persistence | point | 0.511 | 0.511 | 0.511 | 0.928 | 0.608 |
| xgboost | upper99 | 0.117 | 1.000 | 0.210 | 0.932 | 0.597 |
| xgboost | upper95 | 0.158 | 1.000 | 0.273 | 0.932 | 0.597 |
| xgboost | point | 0.639 | 0.489 | 0.554 | 0.932 | 0.597 |
| lstm | lower95 | 1.000 | 0.170 | 0.291 | 0.882 | 0.589 |
| xgb_severity | argmax | 0.481 | 0.532 | 0.505 | 0.923 | 0.563 |
| gnn_st_lagsonly | lower99 | 1.000 | 0.085 | 0.157 | 0.763 | 0.539 |
| lstm | lower99 | 1.000 | 0.106 | 0.192 | 0.713 | 0.430 |
| arima | lower95 | 1.000 | 0.106 | 0.192 | 0.676 | 0.398 |
| gat | point | 0.350 | 0.298 | 0.322 | 0.831 | 0.360 |
| gat | upper95 | 0.206 | 0.681 | 0.317 | 0.831 | 0.358 |
| gat | upper99 | 0.181 | 0.766 | 0.293 | 0.831 | 0.358 |
| gat | lower95 | 0.636 | 0.149 | 0.241 | 0.780 | 0.338 |
| gat | lower99 | 0.750 | 0.064 | 0.118 | 0.699 | 0.289 |
| arima | lower99 | 1.000 | 0.064 | 0.120 | 0.606 | 0.272 |
| seasonal_naive | point | 0.264 | 0.404 | 0.319 | 0.862 | 0.269 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.564 | 0.193 |
| dualtopo | point | 0.245 | 0.255 | 0.250 | 0.749 | 0.159 |
| dualtopo | upper95 | 0.140 | 0.702 | 0.233 | 0.749 | 0.159 |
| dualtopo | upper99 | 0.140 | 0.702 | 0.233 | 0.749 | 0.159 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.692 | 0.140 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.591 | 0.098 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.075 |

## If it had raised an alert for 'high or worse', would it have been right?

19 such weeks, base rate 0.030. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.030, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | lower95 | 0.800 | 0.211 | 0.333 | 0.987 | 0.752 |
| gnn_st_noglobals | lower95 | 0.800 | 0.211 | 0.333 | 0.987 | 0.751 |
| gnn_cascade | point | 0.786 | 0.579 | 0.667 | 0.986 | 0.750 |
| gnn_st | lower95 | 0.800 | 0.211 | 0.333 | 0.987 | 0.749 |
| gnn_st | point | 0.733 | 0.579 | 0.647 | 0.986 | 0.746 |
| gnn_cascade | upper95 | 0.409 | 0.947 | 0.571 | 0.986 | 0.745 |
| gnn_st_noglobals | point | 0.733 | 0.579 | 0.647 | 0.986 | 0.744 |
| gnn_cascade | upper99 | 0.273 | 0.947 | 0.424 | 0.986 | 0.744 |
| gnn_cascade | lower99 | 1.000 | 0.158 | 0.273 | 0.965 | 0.743 |
| gnn_st_lagsonly | lower95 | 1.000 | 0.158 | 0.273 | 0.986 | 0.742 |
| gnn_st_noglobals | upper95 | 0.367 | 0.947 | 0.529 | 0.986 | 0.741 |
| gnn_st_noglobals | upper99 | 0.261 | 0.947 | 0.409 | 0.986 | 0.740 |
| gnn_st | upper95 | 0.375 | 0.947 | 0.537 | 0.986 | 0.739 |
| gnn_st | upper99 | 0.261 | 0.947 | 0.409 | 0.985 | 0.738 |
| gnn_st | lower99 | 1.000 | 0.158 | 0.273 | 0.964 | 0.737 |
| gnn_st_noglobals | lower99 | 1.000 | 0.158 | 0.273 | 0.964 | 0.737 |
| gnn_st_lagsonly | point | 0.786 | 0.579 | 0.667 | 0.986 | 0.734 |
| gnn_st_lagsonly | upper95 | 0.367 | 0.947 | 0.529 | 0.985 | 0.730 |
| gnn_st_lagsonly | upper99 | 0.243 | 0.947 | 0.387 | 0.985 | 0.730 |
| gnn_st_lagsonly | lower99 | 1.000 | 0.053 | 0.100 | 0.914 | 0.688 |
| arima | point | 0.688 | 0.579 | 0.629 | 0.975 | 0.642 |
| arima | upper99 | 0.168 | 1.000 | 0.288 | 0.975 | 0.642 |
| arima | upper95 | 0.236 | 0.895 | 0.374 | 0.975 | 0.642 |
| arima | lower95 | 1.000 | 0.158 | 0.273 | 0.809 | 0.535 |
| xgboost | upper95 | 0.161 | 1.000 | 0.277 | 0.973 | 0.530 |
| xgboost | point | 0.538 | 0.368 | 0.438 | 0.973 | 0.530 |
| xgboost | upper99 | 0.110 | 1.000 | 0.198 | 0.973 | 0.530 |
| persistence | point | 0.526 | 0.526 | 0.526 | 0.962 | 0.508 |
| lstm | upper99 | 0.259 | 0.737 | 0.384 | 0.965 | 0.489 |
| lstm | upper95 | 0.324 | 0.632 | 0.429 | 0.965 | 0.489 |
| lstm | point | 0.583 | 0.368 | 0.452 | 0.965 | 0.489 |
| lstm | lower95 | 0.500 | 0.105 | 0.174 | 0.943 | 0.482 |
| xgb_severity | argmax | 0.444 | 0.211 | 0.286 | 0.960 | 0.460 |
| lstm | lower99 | 0.500 | 0.053 | 0.095 | 0.803 | 0.402 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.709 | 0.388 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.631 | 0.235 |
| gat | upper99 | 0.145 | 0.421 | 0.216 | 0.906 | 0.195 |
| gat | upper95 | 0.175 | 0.368 | 0.237 | 0.906 | 0.195 |
| gat | point | 0.231 | 0.158 | 0.188 | 0.906 | 0.195 |
| gat | lower95 | 0.000 | 0.000 | 0.000 | 0.888 | 0.191 |
| gat | lower99 | 0.000 | 0.000 | 0.000 | 0.796 | 0.160 |
| seasonal_naive | point | 0.091 | 0.158 | 0.115 | 0.893 | 0.133 |
| dualtopo | upper95 | 0.102 | 0.263 | 0.147 | 0.852 | 0.101 |
| dualtopo | point | 0.000 | 0.000 | 0.000 | 0.852 | 0.101 |
| dualtopo | upper99 | 0.112 | 0.579 | 0.188 | 0.852 | 0.101 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.835 | 0.098 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.593 | 0.048 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.030 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 557 | 19 | 3 | 1 |
| moderate | 16 | 7 | 2 | 3 |
| high | 5 | 0 | 2 | 2 |
| very high | 2 | 2 | 2 | 4 |

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
| low | 564 | 15 | 1 | 0 |
| moderate | 19 | 5 | 2 | 2 |
| high | 4 | 1 | 2 | 2 |
| very high | 1 | 2 | 3 | 4 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 565 | 14 | 1 | 0 |
| moderate | 20 | 4 | 2 | 2 |
| high | 4 | 2 | 1 | 2 |
| very high | 3 | 3 | 1 | 3 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 567 | 10 | 3 | 0 |
| moderate | 20 | 5 | 2 | 1 |
| high | 3 | 4 | 0 | 2 |
| very high | 1 | 4 | 2 | 3 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 571 | 9 | 0 | 0 |
| moderate | 13 | 11 | 3 | 1 |
| high | 2 | 3 | 1 | 3 |
| very high | 0 | 3 | 1 | 6 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 553 | 24 | 2 | 1 |
| moderate | 20 | 6 | 1 | 1 |
| high | 1 | 7 | 1 | 0 |
| very high | 1 | 6 | 3 | 0 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
