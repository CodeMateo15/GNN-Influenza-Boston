# Severity bands as a classification problem — horizon 1

One citywide set of cut points for every neighborhood-week (IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03). 992 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_st | point | 0.904 | 0.646 | 0.645 | 0.651 |
| gnn_st_nodemo | point | 0.903 | 0.640 | 0.639 | 0.643 |
| persistence | point | 0.908 | 0.637 | 0.638 | 0.636 |
| xgboost | point | 0.867 | 0.579 | 0.631 | 0.555 |
| xgboost_nodemo | point | 0.868 | 0.572 | 0.606 | 0.556 |
| gat | point | 0.870 | 0.563 | 0.606 | 0.533 |
| arima | point | 0.861 | 0.551 | 0.577 | 0.542 |
| dualtopo | point | 0.864 | 0.503 | 0.549 | 0.478 |
| seasonal_naive | point | 0.847 | 0.497 | 0.529 | 0.475 |
| lstm | point | 0.830 | 0.489 | 0.538 | 0.492 |
| xgb_severity | argmax | 0.856 | 0.485 | 0.484 | 0.486 |
| dualtopo | upper95 | 0.753 | 0.440 | 0.424 | 0.482 |
| arima | upper95 | 0.806 | 0.439 | 0.416 | 0.497 |
| gnn_st | upper95 | 0.793 | 0.428 | 0.408 | 0.482 |
| gat | upper95 | 0.750 | 0.428 | 0.408 | 0.487 |
| gnn_st_nodemo | upper95 | 0.791 | 0.427 | 0.407 | 0.482 |
| gnn_st_nodemo | lower95 | 0.851 | 0.412 | 0.526 | 0.377 |
| arima | upper99 | 0.723 | 0.401 | 0.391 | 0.471 |
| gnn_st | lower95 | 0.850 | 0.401 | 0.501 | 0.369 |
| gnn_st | upper99 | 0.748 | 0.397 | 0.383 | 0.462 |
| arima | lower95 | 0.850 | 0.395 | 0.493 | 0.365 |
| gnn_st_nodemo | upper99 | 0.748 | 0.393 | 0.380 | 0.457 |
| dualtopo | upper99 | 0.704 | 0.389 | 0.380 | 0.444 |
| dualtopo | lower95 | 0.834 | 0.378 | 0.538 | 0.347 |
| gat | upper99 | 0.681 | 0.368 | 0.362 | 0.438 |
| arima | lower99 | 0.838 | 0.361 | 0.478 | 0.336 |
| gnn_st | lower99 | 0.833 | 0.343 | 0.465 | 0.323 |
| gnn_st_nodemo | lower99 | 0.833 | 0.343 | 0.464 | 0.323 |
| xgboost_nodemo | upper95 | 0.642 | 0.332 | 0.339 | 0.382 |
| dualtopo | lower99 | 0.824 | 0.321 | 0.472 | 0.306 |
| xgboost_nodemo | upper99 | 0.535 | 0.301 | 0.333 | 0.369 |
| xgboost_nodemo | lower95 | 0.809 | 0.278 | 0.505 | 0.279 |
| gat | lower95 | 0.808 | 0.266 | 0.458 | 0.271 |
| lstm | lower95 | 0.807 | 0.260 | 0.453 | 0.269 |
| gat | lower99 | 0.805 | 0.252 | 0.453 | 0.265 |
| xgboost_nodemo | lower99 | 0.805 | 0.252 | 0.452 | 0.265 |
| lstm | lower99 | 0.799 | 0.227 | 0.451 | 0.252 |
| lstm | upper95 | 0.355 | 0.222 | 0.306 | 0.290 |
| xgboost | lower99 | 0.798 | 0.222 | 0.200 | 0.250 |
| xgboost | lower95 | 0.798 | 0.222 | 0.200 | 0.250 |
| lstm | upper99 | 0.108 | 0.087 | 0.053 | 0.246 |
| xgboost | upper95 | 0.167 | 0.084 | 0.281 | 0.265 |
| xgboost | upper99 | 0.167 | 0.084 | 0.281 | 0.265 |

## If it had raised an alert for 'moderate or worse', would it have been right?

200 such weeks, base rate 0.202. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.202, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | lower99 | 1.000 | 0.340 | 0.507 | 0.990 | 0.966 |
| gnn_st_nodemo | lower95 | 1.000 | 0.415 | 0.587 | 0.990 | 0.966 |
| gnn_st_nodemo | point | 0.885 | 0.885 | 0.885 | 0.990 | 0.966 |
| gnn_st_nodemo | upper99 | 0.543 | 1.000 | 0.704 | 0.990 | 0.966 |
| gnn_st_nodemo | upper95 | 0.613 | 1.000 | 0.760 | 0.990 | 0.966 |
| gnn_st | upper99 | 0.542 | 1.000 | 0.703 | 0.990 | 0.965 |
| gnn_st | point | 0.885 | 0.885 | 0.885 | 0.990 | 0.965 |
| gnn_st | upper95 | 0.617 | 1.000 | 0.763 | 0.990 | 0.965 |
| gnn_st | lower95 | 1.000 | 0.420 | 0.592 | 0.990 | 0.965 |
| gnn_st | lower99 | 1.000 | 0.345 | 0.513 | 0.990 | 0.965 |
| persistence | point | 0.894 | 0.890 | 0.892 | 0.990 | 0.963 |
| arima | point | 0.796 | 0.820 | 0.808 | 0.974 | 0.908 |
| arima | lower95 | 1.000 | 0.410 | 0.582 | 0.974 | 0.908 |
| arima | upper99 | 0.505 | 0.995 | 0.670 | 0.974 | 0.908 |
| arima | upper95 | 0.627 | 0.940 | 0.752 | 0.974 | 0.908 |
| arima | lower99 | 1.000 | 0.330 | 0.496 | 0.974 | 0.908 |
| xgb_severity | argmax | 0.817 | 0.825 | 0.821 | 0.961 | 0.904 |
| xgboost | upper99 | 0.212 | 1.000 | 0.350 | 0.943 | 0.861 |
| xgboost | upper95 | 0.212 | 1.000 | 0.350 | 0.943 | 0.861 |
| xgboost | point | 0.835 | 0.710 | 0.768 | 0.943 | 0.861 |
| dualtopo | upper99 | 0.478 | 0.925 | 0.630 | 0.925 | 0.851 |
| dualtopo | upper95 | 0.537 | 0.875 | 0.665 | 0.925 | 0.851 |
| dualtopo | point | 0.864 | 0.665 | 0.751 | 0.925 | 0.851 |
| dualtopo | lower95 | 1.000 | 0.350 | 0.519 | 0.926 | 0.850 |
| gat | upper99 | 0.443 | 0.920 | 0.598 | 0.928 | 0.846 |
| xgboost_nodemo | upper95 | 0.429 | 0.930 | 0.587 | 0.928 | 0.846 |
| xgboost_nodemo | point | 0.842 | 0.720 | 0.776 | 0.928 | 0.846 |
| xgboost_nodemo | upper99 | 0.348 | 0.965 | 0.512 | 0.928 | 0.846 |
| gat | upper95 | 0.524 | 0.910 | 0.665 | 0.928 | 0.845 |
| dualtopo | lower99 | 1.000 | 0.245 | 0.394 | 0.920 | 0.843 |
| gat | point | 0.831 | 0.665 | 0.739 | 0.925 | 0.842 |
| gat | lower95 | 1.000 | 0.190 | 0.319 | 0.915 | 0.822 |
| xgboost_nodemo | lower95 | 1.000 | 0.135 | 0.238 | 0.884 | 0.806 |
| gat | lower99 | 1.000 | 0.085 | 0.157 | 0.867 | 0.762 |
| lstm | upper99 | 0.202 | 1.000 | 0.336 | 0.873 | 0.758 |
| lstm | upper95 | 0.260 | 0.940 | 0.407 | 0.873 | 0.758 |
| lstm | point | 0.742 | 0.660 | 0.698 | 0.873 | 0.758 |
| seasonal_naive | point | 0.782 | 0.610 | 0.685 | 0.843 | 0.747 |
| xgboost_nodemo | lower99 | 1.000 | 0.055 | 0.104 | 0.822 | 0.710 |
| lstm | lower95 | 1.000 | 0.095 | 0.174 | 0.787 | 0.636 |
| lstm | lower99 | 1.000 | 0.045 | 0.086 | 0.640 | 0.425 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.202 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.500 | 0.202 |

## If it had raised an alert for 'high or worse', would it have been right?

151 such weeks, base rate 0.152. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.152, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | lower95 | 1.000 | 0.411 | 0.582 | 0.991 | 0.959 |
| gnn_st_nodemo | point | 0.905 | 0.887 | 0.896 | 0.991 | 0.959 |
| gnn_st_nodemo | lower99 | 1.000 | 0.318 | 0.482 | 0.991 | 0.959 |
| gnn_st_nodemo | upper95 | 0.594 | 0.987 | 0.741 | 0.991 | 0.959 |
| gnn_st_nodemo | upper99 | 0.535 | 1.000 | 0.697 | 0.991 | 0.959 |
| gnn_st | upper99 | 0.537 | 1.000 | 0.699 | 0.991 | 0.958 |
| gnn_st | point | 0.900 | 0.894 | 0.897 | 0.991 | 0.958 |
| gnn_st | upper95 | 0.594 | 0.987 | 0.741 | 0.991 | 0.958 |
| gnn_st | lower95 | 1.000 | 0.424 | 0.595 | 0.991 | 0.958 |
| gnn_st | lower99 | 1.000 | 0.318 | 0.482 | 0.991 | 0.958 |
| persistence | point | 0.875 | 0.881 | 0.878 | 0.990 | 0.955 |
| xgb_severity | argmax | 0.830 | 0.841 | 0.836 | 0.970 | 0.900 |
| arima | lower99 | 1.000 | 0.318 | 0.482 | 0.972 | 0.875 |
| arima | point | 0.849 | 0.669 | 0.748 | 0.972 | 0.875 |
| arima | lower95 | 0.984 | 0.404 | 0.573 | 0.972 | 0.875 |
| arima | upper95 | 0.592 | 0.940 | 0.726 | 0.972 | 0.875 |
| arima | upper99 | 0.542 | 0.947 | 0.689 | 0.972 | 0.875 |
| gat | upper99 | 0.440 | 0.927 | 0.597 | 0.946 | 0.870 |
| gat | upper95 | 0.529 | 0.921 | 0.671 | 0.946 | 0.869 |
| gat | point | 0.901 | 0.662 | 0.763 | 0.944 | 0.865 |
| gat | lower95 | 1.000 | 0.132 | 0.234 | 0.934 | 0.846 |
| dualtopo | point | 0.904 | 0.623 | 0.737 | 0.930 | 0.834 |
| dualtopo | upper95 | 0.545 | 0.848 | 0.663 | 0.930 | 0.834 |
| dualtopo | upper99 | 0.473 | 0.861 | 0.610 | 0.930 | 0.834 |
| dualtopo | lower95 | 1.000 | 0.285 | 0.443 | 0.931 | 0.834 |
| dualtopo | lower99 | 1.000 | 0.192 | 0.322 | 0.927 | 0.829 |
| gat | lower99 | 1.000 | 0.046 | 0.089 | 0.913 | 0.815 |
| xgboost | upper99 | 0.160 | 1.000 | 0.276 | 0.935 | 0.809 |
| xgboost | upper95 | 0.160 | 1.000 | 0.276 | 0.935 | 0.809 |
| xgboost | point | 0.892 | 0.603 | 0.719 | 0.935 | 0.809 |
| xgboost_nodemo | upper95 | 0.394 | 0.828 | 0.534 | 0.916 | 0.788 |
| xgboost_nodemo | point | 0.860 | 0.609 | 0.713 | 0.916 | 0.788 |
| xgboost_nodemo | upper99 | 0.349 | 0.894 | 0.502 | 0.916 | 0.788 |
| xgboost_nodemo | lower95 | 1.000 | 0.099 | 0.181 | 0.874 | 0.758 |
| seasonal_naive | point | 0.724 | 0.589 | 0.650 | 0.829 | 0.711 |
| xgboost_nodemo | lower99 | 1.000 | 0.053 | 0.101 | 0.842 | 0.710 |
| lstm | upper99 | 0.197 | 0.940 | 0.326 | 0.859 | 0.696 |
| lstm | point | 0.800 | 0.450 | 0.576 | 0.859 | 0.696 |
| lstm | upper95 | 0.271 | 0.868 | 0.413 | 0.859 | 0.696 |
| lstm | lower95 | 1.000 | 0.073 | 0.136 | 0.795 | 0.617 |
| lstm | lower99 | 1.000 | 0.033 | 0.064 | 0.674 | 0.445 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.500 | 0.152 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.500 | 0.152 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 771 | 15 | 4 | 2 |
| moderate | 15 | 21 | 9 | 4 |
| high | 3 | 8 | 10 | 13 |
| very high | 4 | 3 | 11 | 99 |

**seasonal_naive**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 758 | 13 | 9 | 12 |
| moderate | 28 | 8 | 4 | 9 |
| high | 13 | 3 | 7 | 11 |
| very high | 37 | 9 | 4 | 67 |

**arima**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 750 | 37 | 3 | 2 |
| moderate | 22 | 14 | 7 | 6 |
| high | 7 | 15 | 8 | 4 |
| very high | 7 | 21 | 7 | 82 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 746 | 35 | 10 | 1 |
| moderate | 19 | 24 | 2 | 4 |
| high | 10 | 14 | 4 | 6 |
| very high | 39 | 20 | 9 | 49 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 764 | 24 | 3 | 1 |
| moderate | 23 | 19 | 2 | 5 |
| high | 5 | 10 | 10 | 9 |
| very high | 30 | 15 | 5 | 67 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 769 | 20 | 2 | 1 |
| moderate | 18 | 19 | 9 | 3 |
| high | 2 | 7 | 15 | 10 |
| very high | 3 | 4 | 16 | 94 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 755 | 25 | 6 | 6 |
| moderate | 21 | 14 | 3 | 11 |
| high | 5 | 5 | 1 | 23 |
| very high | 9 | 5 | 24 | 79 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
