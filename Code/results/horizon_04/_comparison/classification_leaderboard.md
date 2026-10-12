# Severity bands as a classification problem — horizon 4

One citywide set of cut points for every neighborhood-week (IT50 = 60.2, IT90 = 98.2, IT98 = 134.2 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 627 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| lstm | point | 0.901 | 0.388 | 0.447 | 0.365 |
| gnn_st_noglobals | upper95 | 0.691 | 0.366 | 0.347 | 0.612 |
| gnn_st | upper95 | 0.691 | 0.366 | 0.347 | 0.612 |
| xgb_severity | argmax | 0.868 | 0.334 | 0.366 | 0.347 |
| xgboost | point | 0.903 | 0.324 | 0.318 | 0.333 |
| gnn_st_lagsonly | upper95 | 0.630 | 0.323 | 0.327 | 0.542 |
| lstm | upper99 | 0.683 | 0.322 | 0.319 | 0.474 |
| lstm | upper95 | 0.764 | 0.307 | 0.303 | 0.376 |
| gnn_st_lagsonly | point | 0.901 | 0.298 | 0.307 | 0.294 |
| arima | point | 0.895 | 0.298 | 0.304 | 0.295 |
| gnn_st | point | 0.901 | 0.297 | 0.306 | 0.294 |
| gnn_st_noglobals | point | 0.901 | 0.297 | 0.306 | 0.294 |
| dualtopo | point | 0.877 | 0.280 | 0.271 | 0.297 |
| persistence | point | 0.871 | 0.280 | 0.280 | 0.280 |
| gnn_st_noglobals | upper99 | 0.553 | 0.277 | 0.306 | 0.494 |
| gnn_st | upper99 | 0.553 | 0.277 | 0.306 | 0.494 |
| lstm | lower95 | 0.928 | 0.274 | 0.482 | 0.268 |
| gat | lower95 | 0.917 | 0.266 | 0.287 | 0.265 |
| gnn_st | lower95 | 0.927 | 0.258 | 0.482 | 0.259 |
| gnn_st_noglobals | lower95 | 0.927 | 0.258 | 0.482 | 0.259 |
| gat | point | 0.874 | 0.252 | 0.252 | 0.253 |
| gnn_st_lagsonly | upper99 | 0.477 | 0.240 | 0.294 | 0.448 |
| gnn_st_noglobals | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| xgboost | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| xgboost | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| lstm | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| gnn_st_lagsonly | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| gnn_st_lagsonly | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| arima | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| gnn_st | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| dualtopo | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| dualtopo | lower99 | 0.925 | 0.240 | 0.231 | 0.250 |
| arima | lower95 | 0.925 | 0.240 | 0.231 | 0.250 |
| gat | lower99 | 0.923 | 0.240 | 0.231 | 0.250 |
| seasonal_naive | point | 0.842 | 0.240 | 0.244 | 0.236 |
| gat | upper95 | 0.687 | 0.232 | 0.255 | 0.239 |
| dualtopo | upper95 | 0.616 | 0.231 | 0.262 | 0.318 |
| gat | upper99 | 0.625 | 0.229 | 0.261 | 0.255 |
| dualtopo | upper99 | 0.616 | 0.228 | 0.260 | 0.318 |
| xgboost | upper95 | 0.421 | 0.216 | 0.287 | 0.413 |
| arima | upper95 | 0.287 | 0.178 | 0.288 | 0.485 |
| xgboost | upper99 | 0.308 | 0.153 | 0.268 | 0.329 |
| arima | upper99 | 0.057 | 0.059 | 0.274 | 0.365 |

## If it had raised an alert for 'moderate or worse', would it have been right?

47 such weeks, base rate 0.075. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.075, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | point | 0.525 | 0.447 | 0.483 | 0.918 | 0.534 |
| gnn_st_noglobals | point | 0.525 | 0.447 | 0.483 | 0.918 | 0.534 |
| gnn_st_noglobals | upper95 | 0.206 | 0.957 | 0.340 | 0.917 | 0.524 |
| gnn_st | upper95 | 0.206 | 0.957 | 0.340 | 0.917 | 0.524 |
| gnn_st | upper99 | 0.156 | 1.000 | 0.270 | 0.916 | 0.524 |
| gnn_st_noglobals | upper99 | 0.156 | 1.000 | 0.270 | 0.916 | 0.524 |
| gnn_st_lagsonly | point | 0.513 | 0.426 | 0.465 | 0.911 | 0.510 |
| gnn_st_lagsonly | upper95 | 0.182 | 0.979 | 0.307 | 0.909 | 0.501 |
| gnn_st_lagsonly | upper99 | 0.136 | 1.000 | 0.239 | 0.909 | 0.500 |
| xgboost | upper99 | 0.106 | 1.000 | 0.191 | 0.913 | 0.496 |
| xgboost | point | 0.524 | 0.468 | 0.494 | 0.913 | 0.496 |
| xgboost | upper95 | 0.124 | 1.000 | 0.221 | 0.913 | 0.496 |
| xgb_severity | argmax | 0.356 | 0.553 | 0.433 | 0.872 | 0.426 |
| lstm | upper95 | 0.248 | 0.809 | 0.380 | 0.880 | 0.388 |
| lstm | upper99 | 0.194 | 0.872 | 0.318 | 0.880 | 0.388 |
| lstm | point | 0.378 | 0.298 | 0.333 | 0.880 | 0.388 |
| arima | upper99 | 0.077 | 1.000 | 0.143 | 0.789 | 0.330 |
| arima | point | 0.378 | 0.298 | 0.333 | 0.789 | 0.330 |
| arima | upper95 | 0.098 | 0.979 | 0.178 | 0.789 | 0.330 |
| gnn_st | lower95 | 1.000 | 0.021 | 0.042 | 0.614 | 0.287 |
| gnn_st_noglobals | lower95 | 1.000 | 0.021 | 0.042 | 0.614 | 0.287 |
| dualtopo | point | 0.245 | 0.255 | 0.250 | 0.781 | 0.274 |
| dualtopo | upper99 | 0.140 | 0.702 | 0.233 | 0.781 | 0.274 |
| dualtopo | upper95 | 0.140 | 0.702 | 0.233 | 0.781 | 0.274 |
| seasonal_naive | point | 0.264 | 0.404 | 0.319 | 0.862 | 0.269 |
| persistence | point | 0.213 | 0.213 | 0.213 | 0.794 | 0.259 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.734 | 0.259 |
| lstm | lower95 | 1.000 | 0.043 | 0.082 | 0.639 | 0.249 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.659 | 0.227 |
| gnn_st_lagsonly | lower95 | 0.000 | 0.000 | 0.000 | 0.574 | 0.213 |
| gat | upper99 | 0.145 | 0.702 | 0.241 | 0.764 | 0.189 |
| gat | point | 0.209 | 0.191 | 0.200 | 0.764 | 0.189 |
| gat | upper95 | 0.155 | 0.596 | 0.246 | 0.764 | 0.189 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.562 | 0.184 |
| gnn_st_noglobals | lower99 | 0.000 | 0.000 | 0.000 | 0.553 | 0.173 |
| gnn_st | lower99 | 0.000 | 0.000 | 0.000 | 0.553 | 0.173 |
| gat | lower95 | 0.222 | 0.043 | 0.071 | 0.629 | 0.138 |
| gat | lower99 | 0.000 | 0.000 | 0.000 | 0.533 | 0.100 |
| arima | lower95 | 0.000 | 0.000 | 0.000 | 0.511 | 0.095 |
| gnn_st_lagsonly | lower99 | 0.000 | 0.000 | 0.000 | 0.511 | 0.095 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.075 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.075 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.500 | 0.075 |

## If it had raised an alert for 'high or worse', would it have been right?

19 such weeks, base rate 0.030. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.030, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | point | 0.400 | 0.211 | 0.276 | 0.963 | 0.369 |
| gnn_st_noglobals | point | 0.400 | 0.211 | 0.276 | 0.963 | 0.369 |
| gnn_st_noglobals | upper95 | 0.213 | 1.000 | 0.352 | 0.962 | 0.357 |
| gnn_st | upper95 | 0.213 | 1.000 | 0.352 | 0.962 | 0.357 |
| gnn_st_noglobals | upper99 | 0.152 | 1.000 | 0.264 | 0.962 | 0.355 |
| gnn_st | upper99 | 0.152 | 1.000 | 0.264 | 0.962 | 0.355 |
| gnn_st_lagsonly | point | 0.364 | 0.211 | 0.267 | 0.959 | 0.344 |
| xgboost | upper99 | 0.071 | 1.000 | 0.133 | 0.959 | 0.334 |
| xgboost | upper95 | 0.111 | 1.000 | 0.200 | 0.959 | 0.334 |
| xgboost | point | 0.333 | 0.263 | 0.294 | 0.959 | 0.334 |
| gnn_st_lagsonly | upper95 | 0.181 | 1.000 | 0.306 | 0.958 | 0.330 |
| gnn_st_lagsonly | upper99 | 0.132 | 1.000 | 0.233 | 0.958 | 0.329 |
| lstm | upper99 | 0.194 | 0.737 | 0.308 | 0.922 | 0.223 |
| lstm | upper95 | 0.189 | 0.526 | 0.278 | 0.922 | 0.223 |
| lstm | point | 0.333 | 0.158 | 0.214 | 0.922 | 0.223 |
| arima | point | 0.222 | 0.105 | 0.143 | 0.896 | 0.183 |
| arima | upper99 | 0.059 | 1.000 | 0.112 | 0.896 | 0.183 |
| arima | upper95 | 0.088 | 1.000 | 0.161 | 0.896 | 0.183 |
| xgb_severity | argmax | 0.143 | 0.105 | 0.121 | 0.906 | 0.175 |
| gnn_st | lower95 | 0.000 | 0.000 | 0.000 | 0.651 | 0.164 |
| gnn_st_noglobals | lower95 | 0.000 | 0.000 | 0.000 | 0.651 | 0.164 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.879 | 0.141 |
| dualtopo | upper95 | 0.149 | 0.579 | 0.237 | 0.879 | 0.141 |
| dualtopo | upper99 | 0.112 | 0.579 | 0.188 | 0.879 | 0.141 |
| dualtopo | point | 0.000 | 0.000 | 0.000 | 0.879 | 0.141 |
| seasonal_naive | point | 0.091 | 0.158 | 0.115 | 0.893 | 0.133 |
| lstm | lower95 | 0.000 | 0.000 | 0.000 | 0.658 | 0.133 |
| persistence | point | 0.158 | 0.158 | 0.158 | 0.859 | 0.111 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.727 | 0.107 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.575 | 0.096 |
| gnn_st_lagsonly | lower95 | 0.000 | 0.000 | 0.000 | 0.575 | 0.090 |
| gat | upper95 | 0.075 | 0.211 | 0.111 | 0.837 | 0.089 |
| gat | upper99 | 0.091 | 0.368 | 0.146 | 0.837 | 0.089 |
| gat | point | 0.000 | 0.000 | 0.000 | 0.837 | 0.089 |
| gnn_st | lower99 | 0.000 | 0.000 | 0.000 | 0.550 | 0.066 |
| gnn_st_noglobals | lower99 | 0.000 | 0.000 | 0.000 | 0.550 | 0.066 |
| gat | lower95 | 0.000 | 0.000 | 0.000 | 0.621 | 0.048 |
| gat | lower99 | 0.000 | 0.000 | 0.000 | 0.502 | 0.032 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.030 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.030 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.500 | 0.030 |
| arima | lower95 | 0.000 | 0.000 | 0.000 | 0.499 | 0.030 |
| gnn_st_lagsonly | lower99 | 0.000 | 0.000 | 0.000 | 0.499 | 0.030 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 543 | 25 | 6 | 6 |
| moderate | 22 | 2 | 1 | 3 |
| high | 7 | 0 | 1 | 1 |
| very high | 8 | 1 | 1 | 0 |

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
| low | 557 | 19 | 4 | 0 |
| moderate | 22 | 3 | 0 | 3 |
| high | 7 | 1 | 1 | 0 |
| very high | 4 | 5 | 1 | 0 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 557 | 20 | 3 | 0 |
| moderate | 20 | 5 | 1 | 2 |
| high | 7 | 0 | 2 | 0 |
| very high | 6 | 3 | 0 | 1 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 560 | 14 | 5 | 1 |
| moderate | 20 | 4 | 2 | 2 |
| high | 3 | 4 | 2 | 0 |
| very high | 2 | 5 | 3 | 0 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 561 | 17 | 2 | 0 |
| moderate | 21 | 3 | 1 | 3 |
| high | 3 | 4 | 0 | 2 |
| very high | 2 | 6 | 1 | 1 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 533 | 37 | 0 | 10 |
| moderate | 16 | 10 | 1 | 1 |
| high | 3 | 5 | 1 | 0 |
| very high | 2 | 7 | 1 | 0 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
