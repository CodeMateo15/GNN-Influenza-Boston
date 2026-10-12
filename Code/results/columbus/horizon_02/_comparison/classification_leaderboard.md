# Severity bands as a classification problem — horizon 2

One citywide set of cut points for every neighborhood-week (IT50 = 35.2, IT90 = 56.1, IT98 = 75.5 per 100,000; CDC's Moving Epidemic Method on 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31). 901 neighborhood-weeks scored. `bound` is the rate that was banded; `argmax` is the direct classifier's most likely band.

## Across all four bands, how often was the band right?

Accuracy is carried by the ~92% of weeks that are low: a model that always says 'low' scores about 0.92. **Macro F1 is the column to rank by** — it averages the four bands equally, so missing every high week costs as much as missing every low one.

| model | bound | accuracy | f1_macro | precision_macro | recall_macro |
| --- | --- | --- | --- | --- | --- |
| gnn_cascade | point | 0.881 | 0.574 | 0.604 | 0.556 |
| gnn_st_v2 | point | 0.878 | 0.539 | 0.583 | 0.514 |
| gnn_st | point | 0.878 | 0.536 | 0.570 | 0.514 |
| persistence | point | 0.837 | 0.502 | 0.501 | 0.503 |
| lstm | point | 0.830 | 0.493 | 0.500 | 0.497 |
| gat | point | 0.826 | 0.482 | 0.467 | 0.505 |
| seasonal_naive | point | 0.822 | 0.473 | 0.460 | 0.500 |
| xgboost | point | 0.849 | 0.457 | 0.512 | 0.437 |
| xgb_severity | argmax | 0.835 | 0.439 | 0.470 | 0.439 |
| arima | point | 0.827 | 0.429 | 0.540 | 0.418 |
| xgboost | upper95 | 0.698 | 0.414 | 0.391 | 0.529 |
| gnn_cascade | upper95 | 0.686 | 0.409 | 0.384 | 0.565 |
| gnn_st_v2 | upper95 | 0.675 | 0.400 | 0.378 | 0.545 |
| gnn_st | upper95 | 0.676 | 0.399 | 0.378 | 0.552 |
| gat | lower95 | 0.855 | 0.395 | 0.457 | 0.371 |
| arima | upper95 | 0.648 | 0.389 | 0.378 | 0.484 |
| gat | upper95 | 0.675 | 0.371 | 0.359 | 0.498 |
| dualtopo | upper99 | 0.656 | 0.347 | 0.342 | 0.466 |
| gnn_cascade | upper99 | 0.599 | 0.346 | 0.346 | 0.509 |
| gnn_st_v2 | upper99 | 0.589 | 0.345 | 0.346 | 0.508 |
| lstm | upper95 | 0.595 | 0.344 | 0.347 | 0.487 |
| xgboost | upper99 | 0.573 | 0.342 | 0.348 | 0.498 |
| gnn_st | upper99 | 0.585 | 0.336 | 0.340 | 0.494 |
| dualtopo | upper95 | 0.659 | 0.329 | 0.336 | 0.395 |
| arima | upper99 | 0.585 | 0.328 | 0.338 | 0.435 |
| gat | upper99 | 0.607 | 0.327 | 0.332 | 0.473 |
| dualtopo | point | 0.782 | 0.305 | 0.291 | 0.328 |
| lstm | upper99 | 0.517 | 0.292 | 0.320 | 0.446 |
| gat | lower99 | 0.830 | 0.272 | 0.351 | 0.276 |
| lstm | lower95 | 0.830 | 0.260 | 0.275 | 0.269 |
| gnn_st | lower95 | 0.826 | 0.245 | 0.263 | 0.260 |
| gnn_st_v2 | lower95 | 0.826 | 0.245 | 0.266 | 0.260 |
| arima | lower95 | 0.826 | 0.245 | 0.308 | 0.260 |
| xgboost | lower95 | 0.826 | 0.245 | 0.285 | 0.260 |
| gnn_cascade | lower95 | 0.825 | 0.241 | 0.251 | 0.257 |
| gnn_cascade | lower99 | 0.822 | 0.231 | 0.256 | 0.252 |
| arima | lower99 | 0.822 | 0.231 | 0.331 | 0.252 |
| gnn_st | lower99 | 0.821 | 0.226 | 0.206 | 0.250 |
| gnn_st_v2 | lower99 | 0.821 | 0.226 | 0.206 | 0.250 |
| lstm | lower99 | 0.821 | 0.226 | 0.206 | 0.250 |
| xgboost | lower99 | 0.821 | 0.226 | 0.206 | 0.250 |
| dualtopo | lower95 | 0.821 | 0.225 | 0.205 | 0.250 |
| dualtopo | lower99 | 0.821 | 0.225 | 0.205 | 0.250 |

## If it had raised an alert for 'moderate or worse', would it have been right?

161 such weeks, base rate 0.179. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.179, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | moderate_plus_precision | moderate_plus_recall | moderate_plus_f1 | moderate_plus_roc_auc | moderate_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | upper99 | 0.388 | 0.994 | 0.558 | 0.966 | 0.880 |
| gnn_cascade | upper95 | 0.464 | 0.988 | 0.631 | 0.966 | 0.880 |
| gnn_cascade | point | 0.845 | 0.745 | 0.792 | 0.966 | 0.879 |
| gnn_st | upper99 | 0.381 | 0.994 | 0.551 | 0.966 | 0.877 |
| gnn_st | upper95 | 0.453 | 0.981 | 0.620 | 0.966 | 0.876 |
| gnn_st | point | 0.858 | 0.752 | 0.801 | 0.966 | 0.875 |
| gnn_st_v2 | upper99 | 0.383 | 0.994 | 0.553 | 0.965 | 0.875 |
| gnn_st_v2 | upper95 | 0.451 | 0.981 | 0.618 | 0.965 | 0.875 |
| gnn_cascade | lower95 | 1.000 | 0.118 | 0.211 | 0.965 | 0.875 |
| gnn_st_v2 | point | 0.857 | 0.745 | 0.797 | 0.965 | 0.874 |
| gnn_st | lower95 | 1.000 | 0.130 | 0.231 | 0.965 | 0.872 |
| gnn_st_v2 | lower95 | 1.000 | 0.124 | 0.221 | 0.964 | 0.871 |
| gnn_cascade | lower99 | 1.000 | 0.031 | 0.060 | 0.943 | 0.852 |
| gat | lower95 | 0.936 | 0.453 | 0.611 | 0.956 | 0.851 |
| gnn_st | lower99 | 1.000 | 0.025 | 0.048 | 0.944 | 0.851 |
| gat | lower99 | 0.976 | 0.248 | 0.396 | 0.954 | 0.850 |
| gat | point | 0.700 | 0.783 | 0.739 | 0.956 | 0.850 |
| gat | upper95 | 0.453 | 0.969 | 0.618 | 0.956 | 0.848 |
| gat | upper99 | 0.398 | 0.988 | 0.567 | 0.956 | 0.848 |
| gnn_st_v2 | lower99 | 1.000 | 0.019 | 0.037 | 0.939 | 0.844 |
| xgboost | point | 0.822 | 0.602 | 0.695 | 0.953 | 0.828 |
| xgboost | upper95 | 0.469 | 0.981 | 0.635 | 0.953 | 0.828 |
| xgboost | upper99 | 0.364 | 0.994 | 0.533 | 0.953 | 0.828 |
| xgboost | lower95 | 1.000 | 0.081 | 0.149 | 0.949 | 0.825 |
| lstm | upper95 | 0.379 | 0.988 | 0.548 | 0.938 | 0.803 |
| lstm | upper99 | 0.333 | 0.994 | 0.499 | 0.938 | 0.803 |
| lstm | point | 0.678 | 0.758 | 0.716 | 0.938 | 0.803 |
| lstm | lower95 | 1.000 | 0.199 | 0.332 | 0.937 | 0.802 |
| persistence | point | 0.701 | 0.714 | 0.708 | 0.941 | 0.797 |
| xgb_severity | argmax | 0.699 | 0.764 | 0.730 | 0.939 | 0.792 |
| seasonal_naive | point | 0.674 | 0.758 | 0.713 | 0.941 | 0.788 |
| lstm | lower99 | 1.000 | 0.012 | 0.025 | 0.902 | 0.776 |
| arima | upper99 | 0.375 | 0.975 | 0.541 | 0.925 | 0.757 |
| arima | point | 0.671 | 0.634 | 0.652 | 0.925 | 0.757 |
| arima | upper95 | 0.408 | 0.944 | 0.569 | 0.925 | 0.756 |
| arima | lower95 | 1.000 | 0.068 | 0.128 | 0.924 | 0.756 |
| xgboost | lower99 | 1.000 | 0.012 | 0.025 | 0.874 | 0.744 |
| arima | lower99 | 1.000 | 0.012 | 0.025 | 0.902 | 0.740 |
| dualtopo | upper99 | 0.399 | 0.919 | 0.556 | 0.874 | 0.592 |
| dualtopo | point | 0.509 | 0.503 | 0.506 | 0.874 | 0.592 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.874 | 0.592 |
| dualtopo | upper95 | 0.399 | 0.919 | 0.556 | 0.874 | 0.592 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.873 | 0.592 |

## If it had raised an alert for 'high or worse', would it have been right?

58 such weeks, base rate 0.064. Precision: of the alerts, the share that were real. Recall: of the real weeks, the share it caught. ROC-AUC: how well it ranks those weeks above the rest (0.5 is chance). PR-AUC: the same, judged only on the rare weeks — chance is the base rate, 0.064, not 0.5. The AUCs use the ranking alone, so a model's interval edges differ from its point forecast there only where the band width reorders weeks.

| model | bound | high_plus_precision | high_plus_recall | high_plus_f1 | high_plus_roc_auc | high_plus_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_cascade | upper95 | 0.381 | 0.966 | 0.546 | 0.984 | 0.767 |
| gnn_cascade | upper99 | 0.307 | 1.000 | 0.470 | 0.984 | 0.764 |
| gnn_cascade | point | 0.731 | 0.655 | 0.691 | 0.984 | 0.762 |
| gnn_st | point | 0.727 | 0.552 | 0.627 | 0.983 | 0.760 |
| gnn_cascade | lower95 | 1.000 | 0.017 | 0.034 | 0.983 | 0.758 |
| gnn_st_v2 | point | 0.756 | 0.534 | 0.626 | 0.982 | 0.758 |
| gnn_st_v2 | lower95 | 1.000 | 0.034 | 0.067 | 0.981 | 0.758 |
| gnn_st | lower95 | 1.000 | 0.034 | 0.067 | 0.981 | 0.758 |
| gnn_st | lower99 | 0.000 | 0.000 | 0.000 | 0.980 | 0.755 |
| gnn_st_v2 | upper95 | 0.379 | 1.000 | 0.550 | 0.983 | 0.755 |
| gnn_st_v2 | lower99 | 0.000 | 0.000 | 0.000 | 0.980 | 0.754 |
| gnn_st_v2 | upper99 | 0.287 | 1.000 | 0.446 | 0.983 | 0.753 |
| gnn_cascade | lower99 | 0.000 | 0.000 | 0.000 | 0.983 | 0.751 |
| gnn_st | upper99 | 0.287 | 1.000 | 0.446 | 0.984 | 0.748 |
| gnn_st | upper95 | 0.377 | 1.000 | 0.547 | 0.983 | 0.746 |
| lstm | point | 0.593 | 0.603 | 0.598 | 0.964 | 0.660 |
| lstm | upper95 | 0.303 | 0.983 | 0.463 | 0.964 | 0.660 |
| lstm | upper99 | 0.227 | 1.000 | 0.371 | 0.964 | 0.660 |
| lstm | lower99 | 0.000 | 0.000 | 0.000 | 0.964 | 0.660 |
| lstm | lower95 | 0.000 | 0.000 | 0.000 | 0.964 | 0.660 |
| gat | point | 0.531 | 0.741 | 0.619 | 0.973 | 0.641 |
| gat | upper95 | 0.363 | 0.983 | 0.530 | 0.973 | 0.639 |
| gat | lower99 | 0.333 | 0.017 | 0.033 | 0.973 | 0.639 |
| gat | lower95 | 0.778 | 0.241 | 0.368 | 0.973 | 0.639 |
| gat | upper99 | 0.309 | 1.000 | 0.472 | 0.973 | 0.638 |
| xgboost | point | 0.595 | 0.431 | 0.500 | 0.965 | 0.572 |
| xgboost | upper95 | 0.382 | 0.948 | 0.545 | 0.965 | 0.572 |
| xgboost | upper99 | 0.302 | 1.000 | 0.464 | 0.965 | 0.572 |
| xgboost | lower99 | 0.000 | 0.000 | 0.000 | 0.965 | 0.572 |
| xgboost | lower95 | 0.000 | 0.000 | 0.000 | 0.965 | 0.572 |
| persistence | point | 0.569 | 0.569 | 0.569 | 0.953 | 0.569 |
| arima | upper99 | 0.238 | 0.914 | 0.377 | 0.935 | 0.509 |
| arima | upper95 | 0.312 | 0.828 | 0.453 | 0.935 | 0.509 |
| arima | lower95 | 1.000 | 0.017 | 0.034 | 0.935 | 0.509 |
| arima | point | 0.607 | 0.293 | 0.395 | 0.935 | 0.509 |
| arima | lower99 | 0.000 | 0.000 | 0.000 | 0.931 | 0.508 |
| seasonal_naive | point | 0.487 | 0.672 | 0.565 | 0.955 | 0.500 |
| xgb_severity | argmax | 0.538 | 0.362 | 0.433 | 0.959 | 0.496 |
| dualtopo | upper99 | 0.239 | 0.655 | 0.350 | 0.884 | 0.370 |
| dualtopo | upper95 | 0.245 | 0.224 | 0.234 | 0.884 | 0.370 |
| dualtopo | lower95 | 0.000 | 0.000 | 0.000 | 0.884 | 0.370 |
| dualtopo | lower99 | 0.000 | 0.000 | 0.000 | 0.884 | 0.370 |
| dualtopo | point | 0.000 | 0.000 | 0.000 | 0.884 | 0.370 |

## Confusion matrices (rows = actual band, columns = forecast band)

**persistence**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 691 | 44 | 5 | 0 |
| moderate | 41 | 42 | 13 | 7 |
| high | 3 | 11 | 16 | 8 |
| very high | 2 | 9 | 4 | 5 |

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
| low | 690 | 49 | 1 | 0 |
| moderate | 49 | 44 | 9 | 1 |
| high | 5 | 23 | 10 | 0 |
| very high | 5 | 8 | 6 | 1 |

**lstm**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 682 | 54 | 4 | 0 |
| moderate | 37 | 46 | 19 | 1 |
| high | 1 | 14 | 16 | 7 |
| very high | 1 | 7 | 8 | 4 |

**xgboost**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 719 | 19 | 2 | 0 |
| moderate | 59 | 29 | 13 | 2 |
| high | 4 | 17 | 15 | 2 |
| very high | 1 | 11 | 6 | 2 |

**gnn_st**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 720 | 19 | 1 | 0 |
| moderate | 39 | 53 | 9 | 2 |
| high | 1 | 18 | 14 | 5 |
| very high | 0 | 7 | 9 | 4 |

**xgb_severity**

| actual \ forecast | low | moderate | high | very high |
| --- | --- | --- | --- | --- |
| low | 687 | 48 | 3 | 2 |
| moderate | 34 | 56 | 3 | 10 |
| high | 3 | 19 | 7 | 9 |
| very high | 1 | 14 | 3 | 2 |

## Notes

- 99% edges are the validation-calibrated 95% band stretched by 2.576/1.960 under a Gaussian reading; unlike the 95% band they were not calibrated on held-out weeks.
- persistence and seasonal_naive are scored on their point forecast only.
