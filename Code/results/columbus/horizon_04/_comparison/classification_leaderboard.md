# Severity bands as a classification problem — horizon 4

One citywide set of cut points for every neighborhood-week (IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 901 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| dualtopo | point | 0.876 | 0.540 | 0.664 | 0.495 |
| seasonal_naive | point | 0.822 | 0.473 | 0.460 | 0.500 |
| xgboost | point | 0.865 | 0.470 | 0.483 | 0.461 |
| dualtopo | upper95 | 0.751 | 0.469 | 0.440 | 0.538 |
| gnn_st | point | 0.858 | 0.465 | 0.513 | 0.453 |
| dualtopo | upper99 | 0.666 | 0.440 | 0.420 | 0.551 |
| lstm | point | 0.815 | 0.438 | 0.422 | 0.459 |
| xgboost | upper95 | 0.698 | 0.434 | 0.405 | 0.570 |
| xgb_severity | argmax | 0.825 | 0.428 | 0.434 | 0.455 |
| gat | lower99 | 0.846 | 0.417 | 0.759 | 0.367 |
| arima | point | 0.841 | 0.413 | 0.449 | 0.402 |
| gnn_st | upper95 | 0.673 | 0.402 | 0.383 | 0.541 |
| persistence | point | 0.802 | 0.395 | 0.394 | 0.396 |
| gat | lower95 | 0.838 | 0.366 | 0.470 | 0.342 |
| gat | point | 0.796 | 0.330 | 0.325 | 0.341 |
| gat | upper95 | 0.624 | 0.326 | 0.332 | 0.390 |
| gnn_st | upper99 | 0.574 | 0.326 | 0.336 | 0.473 |
| xgboost | upper99 | 0.573 | 0.319 | 0.331 | 0.468 |
| gat | upper99 | 0.559 | 0.292 | 0.313 | 0.370 |
| lstm | upper95 | 0.516 | 0.290 | 0.320 | 0.414 |
| arima | upper95 | 0.494 | 0.279 | 0.313 | 0.399 |
| dualtopo | lower95 | 0.830 | 0.259 | 0.266 | 0.269 |
| dualtopo | lower99 | 0.825 | 0.240 | 0.246 | 0.257 |
| lstm | upper99 | 0.420 | 0.232 | 0.296 | 0.371 |
| gnn_st | lower95 | 0.822 | 0.231 | 0.269 | 0.252 |
| xgboost | lower95 | 0.821 | 0.226 | 0.206 | 0.250 |
| arima | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |
| lstm | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |
| lstm | lower95 | 0.821 | 0.225 | 0.205 | 0.250 |
| xgboost | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |
| arima | lower95 | 0.821 | 0.225 | 0.205 | 0.250 |
| gnn_st | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |
| arima | upper99 | 0.372 | 0.214 | 0.290 | 0.374 |

## If it had raised an alert for 'moderate or worse', would it have been right?

161 such weeks, base rate 0.179. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.179, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| xgboost | upper99 | 0.370 | 0.994 | 0.540 | 0.959 | 0.847 |
| xgboost | upper95 | 0.463 | 0.975 | 0.628 | 0.959 | 0.847 |
| xgboost | point | 0.828 | 0.658 | 0.734 | 0.959 | 0.847 |
| xgboost | lower95 | 1.000 | 0.006 | 0.012 | 0.956 | 0.845 |
| gnn_st | upper99 | 0.371 | 0.994 | 0.541 | 0.955 | 0.840 |
| gnn_st | upper95 | 0.444 | 0.988 | 0.613 | 0.955 | 0.839 |
| dualtopo | lower95 | 1.000 | 0.248 | 0.398 | 0.944 | 0.837 |
| dualtopo | upper99 | 0.412 | 0.957 | 0.576 | 0.944 | 0.837 |
| dualtopo | point | 0.907 | 0.609 | 0.729 | 0.944 | 0.837 |
| dualtopo | upper95 | 0.509 | 0.901 | 0.650 | 0.944 | 0.837 |
| dualtopo | lower99 | 1.000 | 0.130 | 0.231 | 0.943 | 0.837 |
| gnn_st | point | 0.800 | 0.696 | 0.744 | 0.955 | 0.837 |
| gnn_st | lower95 | 1.000 | 0.025 | 0.048 | 0.948 | 0.827 |
| seasonal_naive | point | 0.674 | 0.758 | 0.713 | 0.941 | 0.788 |
| xgb_severity | argmax | 0.722 | 0.708 | 0.715 | 0.921 | 0.785 |
| gat | lower95 | 0.906 | 0.298 | 0.449 | 0.916 | 0.747 |
| gat | point | 0.650 | 0.646 | 0.648 | 0.916 | 0.745 |
| gnn_st | lower99 | 0.000 | 0.000 | 0.000 | 0.878 | 0.745 |
| gat | upper95 | 0.394 | 0.925 | 0.553 | 0.915 | 0.742 |
| gat | upper99 | 0.356 | 0.950 | 0.518 | 0.915 | 0.741 |
| gat | lower99 | 0.932 | 0.255 | 0.400 | 0.906 | 0.741 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.863 | 0.739 |
| arima | point | 0.727 | 0.596 | 0.655 | 0.916 | 0.735 |
| arima | upper95 | 0.317 | 0.969 | 0.478 | 0.916 | 0.735 |
| arima | upper99 | 0.267 | 0.988 | 0.420 | 0.916 | 0.735 |
| lstm | point | 0.606 | 0.677 | 0.639 | 0.905 | 0.699 |
| lstm | upper95 | 0.327 | 0.975 | 0.490 | 0.905 | 0.699 |
| lstm | upper99 | 0.287 | 0.994 | 0.445 | 0.905 | 0.699 |
| persistence | point | 0.622 | 0.634 | 0.628 | 0.902 | 0.696 |
| lstm | lower95 | 0.000 | 0.000 | 0.000 | 0.873 | 0.675 |
| arima | lower95 | 0.000 | 0.000 | 0.000 | 0.779 | 0.593 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.720 | 0.501 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.537 | 0.240 |

## If it had raised an alert for 'high or worse', would it have been right?

58 such weeks, base rate 0.064. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.064, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo | point | 0.853 | 0.500 | 0.630 | 0.977 | 0.775 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.977 | 0.775 |
| dualtopo | upper95 | 0.565 | 0.897 | 0.693 | 0.977 | 0.775 |
| dualtopo | upper99 | 0.524 | 0.931 | 0.671 | 0.977 | 0.775 |
| dualtopo | lower95 | 1.000 | 0.017 | 0.034 | 0.977 | 0.775 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.977 | 0.740 |
| xgboost | upper99 | 0.309 | 1.000 | 0.472 | 0.977 | 0.740 |
| xgboost | upper95 | 0.390 | 0.983 | 0.559 | 0.977 | 0.740 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.977 | 0.740 |
| xgboost | point | 0.806 | 0.431 | 0.562 | 0.977 | 0.740 |
| gnn_st | upper99 | 0.274 | 1.000 | 0.430 | 0.970 | 0.696 |
| gnn_st | upper95 | 0.343 | 1.000 | 0.511 | 0.970 | 0.694 |
| gnn_st | point | 0.686 | 0.414 | 0.516 | 0.969 | 0.678 |
| gnn_st | lower95 | 0.000 | 0.000 | 0.000 | 0.965 | 0.648 |
| gnn_st | lower99 | 0.000 | 0.000 | 0.000 | 0.954 | 0.621 |
| xgb_severity | argmax | 0.545 | 0.724 | 0.622 | 0.969 | 0.611 |
| seasonal_naive | point | 0.487 | 0.672 | 0.565 | 0.955 | 0.500 |
| gat | lower99 | 0.800 | 0.207 | 0.329 | 0.925 | 0.491 |
| gat | lower95 | 0.556 | 0.259 | 0.353 | 0.925 | 0.491 |
| gat | point | 0.403 | 0.431 | 0.417 | 0.924 | 0.489 |
| gat | upper95 | 0.292 | 0.724 | 0.416 | 0.923 | 0.478 |
| gat | upper99 | 0.249 | 0.862 | 0.386 | 0.923 | 0.477 |
| arima | point | 0.600 | 0.207 | 0.308 | 0.920 | 0.452 |
| arima | upper95 | 0.206 | 1.000 | 0.341 | 0.920 | 0.452 |
| arima | upper99 | 0.156 | 1.000 | 0.270 | 0.920 | 0.452 |
| lstm | upper95 | 0.215 | 0.966 | 0.351 | 0.925 | 0.446 |
| lstm | point | 0.535 | 0.397 | 0.455 | 0.925 | 0.446 |
| lstm | upper99 | 0.168 | 1.000 | 0.287 | 0.925 | 0.446 |
| lstm | lower95 | 0.000 | 0.000 | 0.000 | 0.925 | 0.446 |
| arima | lower95 | 0.000 | 0.000 | 0.000 | 0.821 | 0.405 |
| persistence | point | 0.379 | 0.379 | 0.379 | 0.905 | 0.381 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.762 | 0.356 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.567 | 0.168 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 678 | 51 | 9 | 2 |
| moderate | 44 | 34 | 16 | 9 |
| high | 9 | 13 | 9 | 7 |
| very high | 6 | 8 | 4 | 2 |

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
| low | 704 | 36 | 0 | 0 |
| moderate | 49 | 46 | 7 | 1 |
| high | 10 | 18 | 8 | 2 |
| very high | 6 | 12 | 2 | 0 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 669 | 64 | 7 | 0 |
| moderate | 43 | 47 | 13 | 0 |
| high | 4 | 16 | 18 | 0 |
| very high | 5 | 10 | 5 | 0 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 718 | 22 | 0 | 0 |
| moderate | 53 | 44 | 6 | 0 |
| high | 2 | 19 | 17 | 0 |
| very high | 0 | 12 | 8 | 0 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 712 | 26 | 2 | 0 |
| moderate | 47 | 47 | 8 | 1 |
| high | 2 | 21 | 13 | 2 |
| very high | 0 | 11 | 8 | 1 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 696 | 35 | 6 | 3 |
| moderate | 44 | 33 | 10 | 16 |
| high | 2 | 5 | 6 | 25 |
| very high | 1 | 8 | 3 | 8 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
