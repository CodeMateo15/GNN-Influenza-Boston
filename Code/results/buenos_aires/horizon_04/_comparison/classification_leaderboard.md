# Severity bands as a classification problem — horizon 4

One citywide set of cut points for every neighborhood-week (IT50 = 77.1, IT90 = 97.5, IT98 = 113.3 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2024-11-03). 992 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_st | point | 0.873 | 0.572 | 0.591 | 0.564 |
| gnn_st_nodemo | point | 0.871 | 0.558 | 0.574 | 0.551 |
| persistence | point | 0.862 | 0.530 | 0.530 | 0.530 |
| xgboost_nodemo | point | 0.855 | 0.510 | 0.555 | 0.487 |
| seasonal_naive | point | 0.847 | 0.497 | 0.529 | 0.475 |
| xgboost | point | 0.847 | 0.497 | 0.540 | 0.480 |
| gat | point | 0.832 | 0.481 | 0.483 | 0.480 |
| dualtopo | point | 0.836 | 0.461 | 0.549 | 0.432 |
| xgb_severity | argmax | 0.839 | 0.449 | 0.452 | 0.449 |
| arima | point | 0.834 | 0.430 | 0.431 | 0.432 |
| arima | upper95 | 0.710 | 0.405 | 0.393 | 0.487 |
| arima | upper99 | 0.660 | 0.402 | 0.396 | 0.495 |
| lstm | point | 0.804 | 0.398 | 0.457 | 0.401 |
| gnn_st | upper95 | 0.699 | 0.375 | 0.369 | 0.438 |
| gnn_st_nodemo | upper95 | 0.688 | 0.372 | 0.368 | 0.438 |
| arima | lower95 | 0.837 | 0.361 | 0.477 | 0.337 |
| gnn_st | upper99 | 0.611 | 0.341 | 0.353 | 0.428 |
| gnn_st_nodemo | upper99 | 0.603 | 0.339 | 0.352 | 0.426 |
| arima | lower99 | 0.830 | 0.338 | 0.486 | 0.319 |
| gat | upper95 | 0.625 | 0.330 | 0.333 | 0.394 |
| dualtopo | upper95 | 0.608 | 0.327 | 0.330 | 0.380 |
| xgboost | upper95 | 0.590 | 0.316 | 0.330 | 0.361 |
| gnn_st_nodemo | lower95 | 0.821 | 0.315 | 0.492 | 0.302 |
| gat | lower95 | 0.823 | 0.313 | 0.459 | 0.301 |
| gnn_st | lower95 | 0.820 | 0.312 | 0.506 | 0.300 |
| xgboost_nodemo | upper95 | 0.541 | 0.298 | 0.322 | 0.356 |
| gat | upper99 | 0.533 | 0.286 | 0.315 | 0.343 |
| gat | lower99 | 0.815 | 0.285 | 0.455 | 0.284 |
| xgboost | upper99 | 0.491 | 0.285 | 0.324 | 0.362 |
| xgboost | lower95 | 0.808 | 0.269 | 0.485 | 0.274 |
| dualtopo | upper99 | 0.488 | 0.263 | 0.297 | 0.323 |
| xgboost_nodemo | lower95 | 0.807 | 0.260 | 0.453 | 0.269 |
| gnn_st_nodemo | lower99 | 0.805 | 0.253 | 0.454 | 0.265 |
| lstm | lower95 | 0.802 | 0.250 | 0.578 | 0.264 |
| xgboost | lower99 | 0.803 | 0.244 | 0.451 | 0.261 |
| xgboost_nodemo | lower99 | 0.802 | 0.240 | 0.451 | 0.259 |
| gnn_st | lower99 | 0.801 | 0.237 | 0.454 | 0.256 |
| xgboost_nodemo | upper99 | 0.368 | 0.230 | 0.312 | 0.308 |
| lstm | upper95 | 0.358 | 0.227 | 0.308 | 0.293 |
| dualtopo | lower95 | 0.798 | 0.222 | 0.200 | 0.250 |
| lstm | lower99 | 0.798 | 0.222 | 0.200 | 0.250 |
| dualtopo | lower99 | 0.798 | 0.222 | 0.200 | 0.250 |
| lstm | upper99 | 0.107 | 0.086 | 0.052 | 0.238 |

## If it had raised an alert for 'moderate or worse', would it have been right?

200 such weeks, base rate 0.202. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.202, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | upper99 | 0.386 | 0.985 | 0.555 | 0.961 | 0.909 |
| gnn_st_nodemo | upper95 | 0.465 | 0.975 | 0.630 | 0.961 | 0.909 |
| gnn_st_nodemo | point | 0.840 | 0.790 | 0.814 | 0.961 | 0.909 |
| gnn_st | upper95 | 0.478 | 0.975 | 0.641 | 0.961 | 0.909 |
| gnn_st | upper99 | 0.392 | 0.985 | 0.561 | 0.961 | 0.909 |
| gnn_st | point | 0.839 | 0.780 | 0.808 | 0.961 | 0.908 |
| gnn_st_nodemo | lower95 | 1.000 | 0.170 | 0.291 | 0.944 | 0.890 |
| gnn_st | lower95 | 1.000 | 0.160 | 0.276 | 0.943 | 0.886 |
| persistence | point | 0.784 | 0.780 | 0.782 | 0.958 | 0.886 |
| arima | point | 0.761 | 0.780 | 0.770 | 0.949 | 0.860 |
| arima | upper95 | 0.479 | 0.975 | 0.643 | 0.949 | 0.860 |
| arima | upper99 | 0.426 | 0.980 | 0.594 | 0.949 | 0.860 |
| arima | lower95 | 1.000 | 0.355 | 0.524 | 0.950 | 0.858 |
| xgb_severity | argmax | 0.779 | 0.740 | 0.759 | 0.921 | 0.831 |
| xgboost | point | 0.815 | 0.685 | 0.745 | 0.897 | 0.813 |
| xgboost | upper95 | 0.367 | 0.865 | 0.515 | 0.897 | 0.813 |
| xgboost | upper99 | 0.313 | 0.930 | 0.469 | 0.897 | 0.813 |
| arima | lower99 | 1.000 | 0.210 | 0.347 | 0.905 | 0.810 |
| xgboost_nodemo | point | 0.844 | 0.650 | 0.734 | 0.879 | 0.800 |
| xgboost_nodemo | upper95 | 0.333 | 0.870 | 0.481 | 0.879 | 0.800 |
| xgboost_nodemo | upper99 | 0.268 | 0.960 | 0.419 | 0.879 | 0.800 |
| gat | upper99 | 0.332 | 0.890 | 0.484 | 0.866 | 0.793 |
| gat | upper95 | 0.387 | 0.855 | 0.533 | 0.865 | 0.792 |
| gat | point | 0.702 | 0.695 | 0.698 | 0.861 | 0.790 |
| xgboost | lower95 | 1.000 | 0.090 | 0.165 | 0.869 | 0.770 |
| gat | lower95 | 1.000 | 0.230 | 0.374 | 0.861 | 0.765 |
| gnn_st_nodemo | lower99 | 1.000 | 0.110 | 0.198 | 0.850 | 0.756 |
| seasonal_naive | point | 0.782 | 0.610 | 0.685 | 0.843 | 0.747 |
| dualtopo | upper99 | 0.292 | 0.815 | 0.430 | 0.783 | 0.713 |
| dualtopo | upper95 | 0.365 | 0.795 | 0.500 | 0.783 | 0.713 |
| dualtopo | point | 0.840 | 0.525 | 0.646 | 0.783 | 0.713 |
| xgboost_nodemo | lower95 | 1.000 | 0.075 | 0.140 | 0.822 | 0.709 |
| gat | lower99 | 1.000 | 0.125 | 0.222 | 0.819 | 0.706 |
| lstm | upper95 | 0.260 | 0.935 | 0.407 | 0.854 | 0.705 |
| lstm | upper99 | 0.202 | 1.000 | 0.336 | 0.854 | 0.705 |
| lstm | point | 0.714 | 0.525 | 0.605 | 0.854 | 0.705 |
| gnn_st | lower99 | 1.000 | 0.100 | 0.182 | 0.812 | 0.700 |
| lstm | lower95 | 1.000 | 0.085 | 0.157 | 0.735 | 0.557 |
| dualtopo | lower95 | 1.000 | 0.020 | 0.039 | 0.707 | 0.526 |
| xgboost | lower99 | 1.000 | 0.045 | 0.086 | 0.689 | 0.504 |
| xgboost_nodemo | lower99 | 1.000 | 0.040 | 0.077 | 0.670 | 0.473 |
| lstm | lower99 | 1.000 | 0.015 | 0.030 | 0.602 | 0.365 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.560 | 0.297 |

## If it had raised an alert for 'high or worse', would it have been right?

151 such weeks, base rate 0.152. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.152, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_nodemo | upper95 | 0.463 | 0.954 | 0.623 | 0.962 | 0.886 |
| gnn_st_nodemo | upper99 | 0.390 | 0.967 | 0.556 | 0.962 | 0.886 |
| gnn_st_nodemo | point | 0.869 | 0.702 | 0.777 | 0.962 | 0.885 |
| gnn_st | upper99 | 0.399 | 0.967 | 0.565 | 0.963 | 0.885 |
| gnn_st | upper95 | 0.462 | 0.954 | 0.622 | 0.963 | 0.885 |
| gnn_st | point | 0.882 | 0.695 | 0.778 | 0.963 | 0.885 |
| gnn_st_nodemo | lower95 | 1.000 | 0.185 | 0.313 | 0.954 | 0.877 |
| persistence | point | 0.778 | 0.788 | 0.783 | 0.962 | 0.873 |
| gnn_st | lower95 | 1.000 | 0.166 | 0.284 | 0.952 | 0.872 |
| arima | upper95 | 0.552 | 0.914 | 0.688 | 0.951 | 0.825 |
| arima | upper99 | 0.406 | 0.974 | 0.573 | 0.951 | 0.825 |
| arima | point | 0.750 | 0.636 | 0.688 | 0.951 | 0.825 |
| arima | lower95 | 0.978 | 0.291 | 0.449 | 0.951 | 0.824 |
| arima | lower99 | 1.000 | 0.219 | 0.359 | 0.928 | 0.803 |
| xgb_severity | argmax | 0.750 | 0.695 | 0.722 | 0.932 | 0.800 |
| gnn_st_nodemo | lower99 | 1.000 | 0.093 | 0.170 | 0.889 | 0.797 |
| gat | upper99 | 0.314 | 0.841 | 0.458 | 0.864 | 0.779 |
| gat | upper95 | 0.394 | 0.821 | 0.532 | 0.863 | 0.779 |
| gat | point | 0.686 | 0.695 | 0.691 | 0.859 | 0.776 |
| gnn_st | lower99 | 1.000 | 0.053 | 0.101 | 0.865 | 0.762 |
| gat | lower95 | 1.000 | 0.212 | 0.350 | 0.866 | 0.760 |
| xgboost | upper99 | 0.310 | 0.854 | 0.455 | 0.889 | 0.758 |
| xgboost | upper95 | 0.395 | 0.834 | 0.536 | 0.889 | 0.758 |
| xgboost | point | 0.845 | 0.543 | 0.661 | 0.889 | 0.758 |
| xgboost_nodemo | upper95 | 0.340 | 0.808 | 0.478 | 0.869 | 0.744 |
| xgboost_nodemo | point | 0.844 | 0.536 | 0.656 | 0.869 | 0.744 |
| xgboost_nodemo | upper99 | 0.264 | 0.861 | 0.404 | 0.869 | 0.744 |
| gat | lower99 | 1.000 | 0.132 | 0.234 | 0.844 | 0.728 |
| xgboost | lower95 | 1.000 | 0.066 | 0.124 | 0.865 | 0.727 |
| seasonal_naive | point | 0.724 | 0.589 | 0.650 | 0.829 | 0.711 |
| xgboost_nodemo | lower95 | 1.000 | 0.060 | 0.113 | 0.830 | 0.687 |
| dualtopo | point | 0.819 | 0.391 | 0.529 | 0.770 | 0.660 |
| dualtopo | upper95 | 0.343 | 0.748 | 0.471 | 0.770 | 0.660 |
| dualtopo | upper99 | 0.288 | 0.775 | 0.420 | 0.770 | 0.660 |
| lstm | upper95 | 0.270 | 0.848 | 0.410 | 0.835 | 0.596 |
| lstm | point | 0.766 | 0.325 | 0.456 | 0.835 | 0.596 |
| lstm | upper99 | 0.199 | 0.940 | 0.328 | 0.835 | 0.596 |
| xgboost | lower99 | 1.000 | 0.033 | 0.064 | 0.736 | 0.539 |
| dualtopo | lower95 | 1.000 | 0.013 | 0.026 | 0.735 | 0.532 |
| xgboost_nodemo | lower99 | 1.000 | 0.033 | 0.064 | 0.714 | 0.505 |
| lstm | lower95 | 1.000 | 0.033 | 0.064 | 0.719 | 0.482 |
| lstm | lower99 | 1.000 | 0.007 | 0.013 | 0.616 | 0.347 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.579 | 0.287 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 749 | 22 | 10 | 11 |
| moderate | 24 | 12 | 7 | 6 |
| high | 10 | 3 | 6 | 15 |
| very high | 10 | 9 | 10 | 88 |

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
| low | 743 | 34 | 7 | 8 |
| moderate | 26 | 6 | 3 | 14 |
| high | 9 | 14 | 0 | 11 |
| very high | 9 | 23 | 7 | 78 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 750 | 36 | 5 | 1 |
| moderate | 21 | 19 | 4 | 5 |
| high | 15 | 10 | 1 | 8 |
| very high | 59 | 18 | 12 | 28 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 761 | 27 | 4 | 0 |
| moderate | 23 | 15 | 7 | 4 |
| high | 7 | 14 | 5 | 8 |
| very high | 33 | 15 | 10 | 59 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 762 | 24 | 6 | 0 |
| moderate | 21 | 20 | 5 | 3 |
| high | 8 | 7 | 8 | 11 |
| very high | 15 | 16 | 10 | 76 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 750 | 23 | 4 | 15 |
| moderate | 24 | 9 | 3 | 13 |
| high | 4 | 6 | 2 | 22 |
| very high | 24 | 12 | 10 | 71 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
