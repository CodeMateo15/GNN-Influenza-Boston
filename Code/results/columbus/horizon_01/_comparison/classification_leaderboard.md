# Severity bands as a classification problem — horizon 1

One citywide set of cut points for every neighborhood-week (IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 901 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | point | 0.890 | 0.591 | 0.604 | 0.582 |
| gnn_st | point | 0.890 | 0.591 | 0.604 | 0.582 |
| persistence | point | 0.863 | 0.558 | 0.558 | 0.559 |
| lstm | point | 0.853 | 0.540 | 0.528 | 0.557 |
| xgboost | point | 0.861 | 0.521 | 0.713 | 0.488 |
| xgb_severity | argmax | 0.859 | 0.505 | 0.517 | 0.501 |
| gat | point | 0.841 | 0.477 | 0.475 | 0.485 |
| arima | upper95 | 0.701 | 0.477 | 0.445 | 0.586 |
| seasonal_naive | point | 0.822 | 0.473 | 0.460 | 0.500 |
| arima | point | 0.849 | 0.468 | 0.507 | 0.454 |
| xgboost | upper95 | 0.718 | 0.450 | 0.417 | 0.593 |
| gnn_st | upper95 | 0.694 | 0.415 | 0.389 | 0.555 |
| gnn_st_v2 | upper95 | 0.694 | 0.415 | 0.389 | 0.555 |
| arima | upper99 | 0.649 | 0.401 | 0.385 | 0.520 |
| gat | upper95 | 0.648 | 0.397 | 0.385 | 0.498 |
| gat | upper99 | 0.602 | 0.357 | 0.357 | 0.487 |
| lstm | upper95 | 0.638 | 0.356 | 0.349 | 0.507 |
| xgboost | upper99 | 0.593 | 0.351 | 0.351 | 0.508 |
| dualtopo | upper99 | 0.663 | 0.350 | 0.345 | 0.444 |
| arima | lower95 | 0.832 | 0.345 | 0.761 | 0.315 |
| gnn_st_v2 | upper99 | 0.617 | 0.342 | 0.339 | 0.492 |
| gnn_st | upper99 | 0.616 | 0.342 | 0.339 | 0.491 |
| dualtopo | upper95 | 0.659 | 0.329 | 0.336 | 0.395 |
| lstm | lower95 | 0.838 | 0.323 | 0.418 | 0.309 |
| lstm | upper99 | 0.562 | 0.310 | 0.324 | 0.475 |
| dualtopo | point | 0.794 | 0.291 | 0.282 | 0.300 |
| gat | lower95 | 0.830 | 0.283 | 0.362 | 0.284 |
| gnn_st_v2 | lower95 | 0.828 | 0.264 | 0.315 | 0.271 |
| gnn_st | lower95 | 0.827 | 0.261 | 0.309 | 0.268 |
| gat | lower99 | 0.826 | 0.245 | 0.250 | 0.260 |
| xgboost | lower95 | 0.825 | 0.240 | 0.266 | 0.257 |
| gnn_st_v2 | lower99 | 0.824 | 0.237 | 0.233 | 0.255 |
| arima | lower99 | 0.822 | 0.236 | 0.240 | 0.255 |
| lstm | lower99 | 0.822 | 0.233 | 0.221 | 0.252 |
| gnn_st | lower99 | 0.822 | 0.233 | 0.223 | 0.252 |
| xgboost | lower99 | 0.821 | 0.226 | 0.206 | 0.250 |
| dualtopo | lower95 | 0.821 | 0.225 | 0.205 | 0.250 |
| dualtopo | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |

## If it had raised an alert for 'moderate or worse', would it have been right?

161 such weeks, base rate 0.179. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.179, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | upper95 | 0.473 | 0.988 | 0.640 | 0.974 | 0.905 |
| gnn_st_v2 | upper99 | 0.410 | 0.988 | 0.579 | 0.974 | 0.904 |
| gnn_st | upper99 | 0.409 | 0.988 | 0.578 | 0.974 | 0.904 |
| gnn_st | upper95 | 0.473 | 0.988 | 0.640 | 0.973 | 0.904 |
| gnn_st_v2 | point | 0.845 | 0.814 | 0.829 | 0.973 | 0.904 |
| gnn_st | point | 0.845 | 0.814 | 0.829 | 0.973 | 0.903 |
| gnn_st | lower95 | 0.977 | 0.267 | 0.420 | 0.972 | 0.903 |
| gnn_st_v2 | lower95 | 0.978 | 0.273 | 0.427 | 0.972 | 0.903 |
| gnn_st | lower99 | 1.000 | 0.143 | 0.250 | 0.968 | 0.899 |
| gnn_st_v2 | lower99 | 1.000 | 0.155 | 0.269 | 0.968 | 0.899 |
| lstm | upper99 | 0.364 | 0.994 | 0.533 | 0.960 | 0.871 |
| lstm | upper95 | 0.421 | 0.988 | 0.590 | 0.960 | 0.871 |
| lstm | point | 0.746 | 0.783 | 0.764 | 0.960 | 0.871 |
| lstm | lower95 | 0.981 | 0.329 | 0.493 | 0.960 | 0.871 |
| lstm | lower99 | 1.000 | 0.155 | 0.269 | 0.957 | 0.868 |
| persistence | point | 0.765 | 0.770 | 0.768 | 0.962 | 0.856 |
| xgb_severity | argmax | 0.786 | 0.776 | 0.781 | 0.959 | 0.849 |
| xgboost | point | 0.823 | 0.634 | 0.716 | 0.959 | 0.835 |
| xgboost | upper95 | 0.485 | 0.988 | 0.650 | 0.959 | 0.835 |
| xgboost | upper99 | 0.379 | 0.994 | 0.549 | 0.959 | 0.835 |
| xgboost | lower95 | 1.000 | 0.087 | 0.160 | 0.956 | 0.832 |
| gat | lower99 | 1.000 | 0.161 | 0.278 | 0.943 | 0.824 |
| gat | lower95 | 0.902 | 0.286 | 0.434 | 0.944 | 0.824 |
| gat | point | 0.699 | 0.764 | 0.730 | 0.944 | 0.823 |
| gat | upper95 | 0.411 | 0.969 | 0.577 | 0.944 | 0.822 |
| gat | upper99 | 0.381 | 0.988 | 0.550 | 0.944 | 0.822 |
| arima | point | 0.750 | 0.689 | 0.718 | 0.949 | 0.819 |
| arima | upper99 | 0.415 | 0.975 | 0.583 | 0.949 | 0.819 |
| arima | lower95 | 0.947 | 0.224 | 0.362 | 0.949 | 0.819 |
| arima | upper95 | 0.448 | 0.957 | 0.610 | 0.949 | 0.819 |
| arima | lower99 | 0.944 | 0.106 | 0.190 | 0.945 | 0.816 |
| seasonal_naive | point | 0.674 | 0.758 | 0.713 | 0.941 | 0.788 |
| xgboost | lower99 | 1.000 | 0.019 | 0.037 | 0.880 | 0.751 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.874 | 0.593 |
| dualtopo | point | 0.500 | 0.329 | 0.397 | 0.874 | 0.593 |
| dualtopo | upper95 | 0.399 | 0.919 | 0.556 | 0.874 | 0.593 |
| dualtopo | upper99 | 0.399 | 0.919 | 0.556 | 0.874 | 0.593 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.874 | 0.593 |

## If it had raised an alert for 'high or worse', would it have been right?

58 such weeks, base rate 0.064. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.064, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_v2 | lower95 | 1.000 | 0.069 | 0.129 | 0.989 | 0.874 |
| gnn_st | lower95 | 1.000 | 0.069 | 0.129 | 0.989 | 0.874 |
| gnn_st | lower99 | 1.000 | 0.034 | 0.067 | 0.988 | 0.873 |
| gnn_st_v2 | lower99 | 1.000 | 0.034 | 0.067 | 0.988 | 0.871 |
| gnn_st | point | 0.782 | 0.741 | 0.761 | 0.989 | 0.871 |
| gnn_st_v2 | point | 0.782 | 0.741 | 0.761 | 0.989 | 0.870 |
| gnn_st_v2 | upper95 | 0.407 | 0.983 | 0.576 | 0.989 | 0.868 |
| gnn_st_v2 | upper99 | 0.326 | 1.000 | 0.492 | 0.989 | 0.867 |
| gnn_st | upper95 | 0.407 | 0.983 | 0.576 | 0.989 | 0.867 |
| gnn_st | upper99 | 0.324 | 1.000 | 0.489 | 0.988 | 0.866 |
| lstm | upper99 | 0.268 | 0.983 | 0.421 | 0.982 | 0.829 |
| lstm | upper95 | 0.337 | 0.966 | 0.500 | 0.982 | 0.829 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.982 | 0.829 |
| lstm | point | 0.685 | 0.862 | 0.763 | 0.982 | 0.829 |
| lstm | lower95 | 1.000 | 0.155 | 0.269 | 0.982 | 0.829 |
| persistence | point | 0.707 | 0.707 | 0.707 | 0.976 | 0.765 |
| arima | point | 0.784 | 0.500 | 0.611 | 0.972 | 0.731 |
| arima | upper95 | 0.439 | 0.862 | 0.581 | 0.972 | 0.731 |
| arima | upper99 | 0.354 | 0.966 | 0.519 | 0.972 | 0.731 |
| arima | lower99 | 1.000 | 0.034 | 0.067 | 0.972 | 0.731 |
| arima | lower95 | 1.000 | 0.103 | 0.188 | 0.972 | 0.731 |
| xgboost | upper99 | 0.320 | 1.000 | 0.485 | 0.976 | 0.702 |
| xgboost | upper95 | 0.403 | 0.966 | 0.569 | 0.976 | 0.702 |
| xgboost | point | 0.725 | 0.500 | 0.592 | 0.976 | 0.702 |
| xgboost | lower95 | 1.000 | 0.017 | 0.034 | 0.976 | 0.702 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.976 | 0.702 |
| gat | lower99 | 0.000 | 0.000 | 0.000 | 0.971 | 0.638 |
| gat | lower95 | 0.333 | 0.017 | 0.033 | 0.971 | 0.637 |
| gat | point | 0.653 | 0.552 | 0.598 | 0.971 | 0.635 |
| gat | upper99 | 0.329 | 0.983 | 0.494 | 0.971 | 0.635 |
| gat | upper95 | 0.412 | 0.931 | 0.571 | 0.971 | 0.634 |
| xgb_severity | argmax | 0.522 | 0.414 | 0.462 | 0.967 | 0.572 |
| seasonal_naive | point | 0.487 | 0.672 | 0.565 | 0.955 | 0.500 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.885 | 0.372 |
| dualtopo | upper95 | 0.245 | 0.224 | 0.234 | 0.885 | 0.372 |
| dualtopo | upper99 | 0.236 | 0.431 | 0.305 | 0.885 | 0.372 |
| dualtopo | point | 0.000 | 0.000 | 0.000 | 0.885 | 0.372 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.885 | 0.372 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 702 | 36 | 1 | 1 |
| moderate | 35 | 53 | 12 | 3 |
| high | 1 | 12 | 16 | 9 |
| very high | 1 | 3 | 9 | 7 |

**seasonal_naive**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 681 | 45 | 11 | 3 |
| moderate | 36 | 40 | 11 | 16 |
| high | 3 | 8 | 13 | 14 |
| very high | 0 | 8 | 5 | 7 |

**arima**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 703 | 35 | 2 | 0 |
| moderate | 48 | 49 | 6 | 0 |
| high | 0 | 22 | 11 | 5 |
| very high | 2 | 5 | 11 | 2 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 697 | 42 | 1 | 0 |
| moderate | 33 | 48 | 21 | 1 |
| high | 2 | 5 | 16 | 15 |
| very high | 0 | 1 | 11 | 8 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 718 | 21 | 1 | 0 |
| moderate | 56 | 37 | 10 | 0 |
| high | 2 | 18 | 18 | 0 |
| very high | 1 | 8 | 8 | 3 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 716 | 23 | 1 | 0 |
| moderate | 29 | 63 | 11 | 0 |
| high | 1 | 11 | 17 | 9 |
| very high | 0 | 3 | 11 | 6 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 706 | 28 | 4 | 2 |
| moderate | 34 | 53 | 10 | 6 |
| high | 1 | 20 | 9 | 8 |
| very high | 1 | 12 | 1 | 6 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
