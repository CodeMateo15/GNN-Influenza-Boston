# Severity bands as a classification problem — horizon 2

One citywide set of cut points for every neighborhood-week (IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03). 992 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | point | 0.883 | 0.590 | 0.595 | 0.594 |
| gnn_st | point | 0.883 | 0.582 | 0.591 | 0.579 |
| persistence | point | 0.887 | 0.576 | 0.577 | 0.575 |
| dualtopo | point | 0.850 | 0.535 | 0.570 | 0.518 |
| xgboost_nodemo | point | 0.855 | 0.534 | 0.573 | 0.513 |
| xgboost | point | 0.854 | 0.528 | 0.572 | 0.509 |
| gat | point | 0.850 | 0.520 | 0.571 | 0.497 |
| xgb_severity | argmax | 0.860 | 0.511 | 0.498 | 0.534 |
| seasonal_naive | point | 0.847 | 0.497 | 0.529 | 0.475 |
| arima | point | 0.840 | 0.466 | 0.492 | 0.457 |
| arima | upper95 | 0.782 | 0.464 | 0.440 | 0.520 |
| gnn_st | upper95 | 0.806 | 0.446 | 0.423 | 0.501 |
| lstm | point | 0.820 | 0.444 | 0.517 | 0.442 |
| gnn_st_nodemo | upper95 | 0.803 | 0.440 | 0.417 | 0.494 |
| arima | lower95 | 0.847 | 0.408 | 0.534 | 0.372 |
| gnn_st | upper99 | 0.754 | 0.404 | 0.389 | 0.466 |
| gnn_st_nodemo | upper99 | 0.747 | 0.402 | 0.387 | 0.464 |
| arima | upper99 | 0.699 | 0.401 | 0.394 | 0.467 |
| gnn_st_nodemo | lower95 | 0.847 | 0.399 | 0.509 | 0.366 |
| gnn_st | lower95 | 0.844 | 0.392 | 0.510 | 0.360 |
| arima | lower99 | 0.835 | 0.361 | 0.501 | 0.335 |
| dualtopo | upper95 | 0.682 | 0.356 | 0.350 | 0.392 |
| dualtopo | upper99 | 0.642 | 0.355 | 0.352 | 0.413 |
| gnn_st | lower99 | 0.832 | 0.349 | 0.488 | 0.326 |
| xgboost | upper95 | 0.636 | 0.345 | 0.349 | 0.401 |
| gnn_st_nodemo | lower99 | 0.832 | 0.339 | 0.455 | 0.321 |
| gat | upper95 | 0.610 | 0.337 | 0.348 | 0.406 |
| xgboost_nodemo | upper95 | 0.602 | 0.318 | 0.331 | 0.360 |
| gat | upper99 | 0.530 | 0.302 | 0.335 | 0.391 |
| lstm | lower95 | 0.812 | 0.295 | 0.517 | 0.290 |
| xgboost | upper99 | 0.520 | 0.295 | 0.331 | 0.359 |
| xgboost_nodemo | lower95 | 0.808 | 0.273 | 0.516 | 0.277 |
| dualtopo | lower95 | 0.808 | 0.265 | 0.456 | 0.271 |
| xgboost_nodemo | upper99 | 0.442 | 0.262 | 0.323 | 0.332 |
| xgboost | lower95 | 0.807 | 0.260 | 0.453 | 0.269 |
| xgboost_nodemo | lower99 | 0.805 | 0.251 | 0.451 | 0.265 |
| dualtopo | lower99 | 0.804 | 0.248 | 0.452 | 0.263 |
| xgboost | lower99 | 0.804 | 0.247 | 0.451 | 0.263 |
| lstm | lower99 | 0.802 | 0.241 | 0.453 | 0.259 |
| gat | lower95 | 0.801 | 0.235 | 0.451 | 0.256 |
| gat | lower99 | 0.798 | 0.222 | 0.200 | 0.250 |
| lstm | upper95 | 0.122 | 0.106 | 0.308 | 0.233 |
| lstm | upper99 | 0.117 | 0.071 | 0.041 | 0.264 |

## If it had raised an alert for 'moderate or worse', would it have been right?

200 such weeks, base rate 0.202. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.202, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | upper99 | 0.551 | 0.995 | 0.709 | 0.984 | 0.954 |
| gnn_st_nodemo | upper99 | 0.541 | 0.995 | 0.701 | 0.984 | 0.954 |
| gnn_st | point | 0.867 | 0.850 | 0.859 | 0.984 | 0.954 |
| gnn_st | upper95 | 0.637 | 0.990 | 0.775 | 0.984 | 0.954 |
| gnn_st_nodemo | upper95 | 0.635 | 0.990 | 0.773 | 0.984 | 0.954 |
| gnn_st_nodemo | point | 0.857 | 0.870 | 0.864 | 0.984 | 0.954 |
| gnn_st | lower95 | 1.000 | 0.400 | 0.571 | 0.984 | 0.954 |
| gnn_st | lower99 | 1.000 | 0.305 | 0.467 | 0.985 | 0.954 |
| gnn_st_nodemo | lower95 | 1.000 | 0.410 | 0.582 | 0.984 | 0.953 |
| gnn_st_nodemo | lower99 | 1.000 | 0.305 | 0.467 | 0.984 | 0.953 |
| persistence | point | 0.859 | 0.850 | 0.854 | 0.983 | 0.945 |
| xgb_severity | argmax | 0.774 | 0.840 | 0.806 | 0.955 | 0.893 |
| arima | point | 0.769 | 0.750 | 0.759 | 0.959 | 0.875 |
| arima | upper95 | 0.578 | 0.925 | 0.712 | 0.959 | 0.875 |
| arima | upper99 | 0.472 | 0.975 | 0.636 | 0.959 | 0.875 |
| arima | lower95 | 1.000 | 0.395 | 0.566 | 0.959 | 0.875 |
| arima | lower99 | 1.000 | 0.320 | 0.485 | 0.960 | 0.875 |
| xgboost | upper99 | 0.338 | 0.960 | 0.500 | 0.920 | 0.829 |
| xgboost | upper95 | 0.411 | 0.905 | 0.566 | 0.920 | 0.829 |
| xgboost | point | 0.811 | 0.665 | 0.731 | 0.920 | 0.829 |
| gat | upper99 | 0.339 | 0.975 | 0.503 | 0.927 | 0.824 |
| gat | upper95 | 0.393 | 0.950 | 0.556 | 0.927 | 0.824 |
| gat | point | 0.817 | 0.625 | 0.708 | 0.924 | 0.819 |
| xgboost_nodemo | upper95 | 0.380 | 0.875 | 0.530 | 0.907 | 0.819 |
| xgboost_nodemo | point | 0.815 | 0.660 | 0.729 | 0.907 | 0.819 |
| xgboost_nodemo | upper99 | 0.304 | 0.985 | 0.464 | 0.907 | 0.819 |
| xgboost | lower95 | 1.000 | 0.080 | 0.148 | 0.868 | 0.775 |
| xgboost_nodemo | lower95 | 1.000 | 0.095 | 0.174 | 0.864 | 0.771 |
| dualtopo | point | 0.793 | 0.650 | 0.714 | 0.828 | 0.751 |
| dualtopo | upper95 | 0.437 | 0.795 | 0.564 | 0.828 | 0.751 |
| dualtopo | upper99 | 0.397 | 0.835 | 0.538 | 0.828 | 0.751 |
| seasonal_naive | point | 0.782 | 0.610 | 0.685 | 0.843 | 0.747 |
| dualtopo | lower95 | 1.000 | 0.145 | 0.253 | 0.854 | 0.744 |
| lstm | upper95 | 0.206 | 1.000 | 0.342 | 0.864 | 0.725 |
| lstm | point | 0.758 | 0.595 | 0.667 | 0.864 | 0.725 |
| lstm | upper99 | 0.202 | 1.000 | 0.336 | 0.864 | 0.725 |
| dualtopo | lower99 | 1.000 | 0.055 | 0.104 | 0.839 | 0.716 |
| gat | lower95 | 1.000 | 0.035 | 0.068 | 0.763 | 0.617 |
| xgboost_nodemo | lower99 | 1.000 | 0.045 | 0.086 | 0.747 | 0.597 |
| xgboost | lower99 | 1.000 | 0.045 | 0.086 | 0.741 | 0.587 |
| lstm | lower95 | 1.000 | 0.125 | 0.222 | 0.755 | 0.575 |
| lstm | lower99 | 1.000 | 0.080 | 0.148 | 0.610 | 0.377 |
| gat | lower99 | 1.000 | 0.010 | 0.020 | 0.588 | 0.341 |

## If it had raised an alert for 'high or worse', would it have been right?

151 such weeks, base rate 0.152. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.152, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | lower99 | 1.000 | 0.278 | 0.435 | 0.988 | 0.943 |
| gnn_st | lower95 | 1.000 | 0.371 | 0.541 | 0.988 | 0.943 |
| gnn_st | point | 0.896 | 0.801 | 0.846 | 0.988 | 0.943 |
| gnn_st | upper95 | 0.610 | 0.974 | 0.750 | 0.988 | 0.943 |
| gnn_st | upper99 | 0.540 | 0.993 | 0.699 | 0.988 | 0.943 |
| gnn_st_nodemo | upper95 | 0.601 | 0.967 | 0.741 | 0.988 | 0.943 |
| gnn_st_nodemo | upper99 | 0.540 | 0.993 | 0.699 | 0.988 | 0.943 |
| gnn_st_nodemo | point | 0.896 | 0.801 | 0.846 | 0.988 | 0.943 |
| gnn_st_nodemo | lower95 | 1.000 | 0.397 | 0.569 | 0.988 | 0.943 |
| gnn_st_nodemo | lower99 | 1.000 | 0.285 | 0.443 | 0.988 | 0.943 |
| persistence | point | 0.849 | 0.854 | 0.851 | 0.986 | 0.937 |
| xgb_severity | argmax | 0.839 | 0.795 | 0.816 | 0.965 | 0.893 |
| arima | upper99 | 0.524 | 0.940 | 0.673 | 0.961 | 0.838 |
| arima | lower99 | 1.000 | 0.291 | 0.451 | 0.961 | 0.838 |
| arima | point | 0.809 | 0.589 | 0.682 | 0.961 | 0.838 |
| arima | lower95 | 0.984 | 0.411 | 0.579 | 0.961 | 0.838 |
| arima | upper95 | 0.592 | 0.934 | 0.725 | 0.961 | 0.838 |
| gat | upper99 | 0.316 | 0.947 | 0.474 | 0.934 | 0.821 |
| gat | upper95 | 0.408 | 0.914 | 0.564 | 0.934 | 0.820 |
| gat | point | 0.885 | 0.609 | 0.722 | 0.931 | 0.814 |
| xgboost | upper99 | 0.330 | 0.874 | 0.479 | 0.905 | 0.767 |
| xgboost | upper95 | 0.413 | 0.834 | 0.553 | 0.905 | 0.767 |
| xgboost | point | 0.876 | 0.563 | 0.685 | 0.905 | 0.767 |
| xgboost_nodemo | upper95 | 0.369 | 0.808 | 0.506 | 0.891 | 0.753 |
| xgboost_nodemo | point | 0.829 | 0.576 | 0.680 | 0.891 | 0.753 |
| xgboost_nodemo | upper99 | 0.302 | 0.848 | 0.445 | 0.891 | 0.753 |
| dualtopo | point | 0.821 | 0.609 | 0.700 | 0.824 | 0.742 |
| dualtopo | upper95 | 0.440 | 0.781 | 0.563 | 0.824 | 0.742 |
| dualtopo | upper99 | 0.361 | 0.808 | 0.499 | 0.824 | 0.742 |
| dualtopo | lower95 | 1.000 | 0.079 | 0.147 | 0.860 | 0.740 |
| xgboost | lower95 | 1.000 | 0.073 | 0.136 | 0.867 | 0.733 |
| xgboost_nodemo | lower95 | 1.000 | 0.086 | 0.159 | 0.864 | 0.725 |
| dualtopo | lower99 | 1.000 | 0.053 | 0.101 | 0.857 | 0.725 |
| seasonal_naive | point | 0.724 | 0.589 | 0.650 | 0.829 | 0.711 |
| gat | lower95 | 1.000 | 0.020 | 0.039 | 0.809 | 0.666 |
| lstm | upper99 | 0.152 | 1.000 | 0.264 | 0.847 | 0.642 |
| lstm | upper95 | 0.224 | 0.894 | 0.358 | 0.847 | 0.642 |
| lstm | point | 0.716 | 0.351 | 0.471 | 0.847 | 0.642 |
| xgboost | lower99 | 1.000 | 0.046 | 0.089 | 0.782 | 0.616 |
| xgboost_nodemo | lower99 | 1.000 | 0.046 | 0.089 | 0.781 | 0.614 |
| lstm | lower95 | 1.000 | 0.132 | 0.234 | 0.755 | 0.536 |
| lstm | lower99 | 1.000 | 0.060 | 0.113 | 0.638 | 0.384 |
| gat | lower99 | 1.000 | 0.013 | 0.026 | 0.616 | 0.349 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 764 | 19 | 6 | 3 |
| moderate | 22 | 13 | 7 | 7 |
| high | 3 | 7 | 9 | 15 |
| very high | 5 | 7 | 11 | 94 |

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
| low | 747 | 40 | 5 | 0 |
| moderate | 24 | 9 | 6 | 10 |
| high | 11 | 12 | 2 | 9 |
| very high | 15 | 24 | 3 | 75 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 754 | 24 | 14 | 0 |
| moderate | 21 | 21 | 5 | 2 |
| high | 11 | 14 | 3 | 6 |
| very high | 49 | 24 | 9 | 35 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 761 | 27 | 4 | 0 |
| moderate | 23 | 18 | 4 | 4 |
| high | 5 | 13 | 6 | 10 |
| very high | 39 | 9 | 7 | 62 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 766 | 23 | 3 | 0 |
| moderate | 21 | 17 | 10 | 1 |
| high | 4 | 9 | 10 | 11 |
| very high | 5 | 12 | 17 | 83 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 743 | 37 | 4 | 8 |
| moderate | 18 | 20 | 2 | 9 |
| high | 3 | 9 | 1 | 21 |
| very high | 11 | 8 | 9 | 89 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
