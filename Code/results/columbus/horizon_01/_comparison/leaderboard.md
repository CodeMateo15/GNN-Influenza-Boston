Ranked by **RMSE** within each segment, `scope=pooled`, horizon 1.

## Overall (full year) — 901 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 7.230 | 2641999.908 | 4.905 | 0.928 | 96.115 | blend | train |
| gnn_st_v2 | post_covid | 7.240 | 2631602.081 | 4.908 | 0.928 | 96.115 | blend | train |
| lstm | post_covid | 8.723 | 46.656 | 6.123 | 0.901 | 95.117 | level | train |
| persistence | post_covid | 9.195 | 46.103 | 6.188 | 0.887 | 94.229 | level | none |
| arima | post_covid | 9.481 | 48.101 | 6.340 | 0.873 | 89.678 | level | none |
| xgboost | post_covid | 9.532 | 3410520.029 | 6.421 | 0.883 | 95.006 | climatology | None |
| gat | post_covid | 10.051 | 56.733 | 6.776 | 0.857 | 85.239 | level | None |
| dualtopo | post_covid | 14.368 | 67.350 | 9.436 | 0.686 | 68.036 | level | train |
| seasonal_naive | post_covid | 16.366 | 60.842 | 9.093 | 0.765 | 97.891 | level | none |

## Flu season (Oct–Mar) — 442 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 8.680 | 2010197.794 | 5.922 | 0.924 | 95.475 | blend | train |
| gnn_st_v2 | post_covid | 8.694 | 2006326.151 | 5.924 | 0.924 | 95.475 | blend | train |
| lstm | post_covid | 10.381 | 36.164 | 7.390 | 0.897 | 93.891 | level | train |
| persistence | post_covid | 11.319 | 36.343 | 7.770 | 0.875 | 94.570 | level | none |
| xgboost | post_covid | 11.470 | 3112594.570 | 7.910 | 0.869 | 94.570 | climatology | None |
| arima | post_covid | 11.696 | 33.694 | 7.861 | 0.870 | 86.199 | level | none |
| gat | post_covid | 12.206 | 39.699 | 8.173 | 0.844 | 81.448 | level | None |
| dualtopo | post_covid | 18.218 | 42.093 | 12.075 | 0.785 | 57.919 | level | train |
| seasonal_naive | post_covid | 22.319 | 62.620 | 13.384 | 0.712 | 98.190 | level | none |

## Off-season (Apr–Sep) — 459 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.483 | 3259793.105 | 3.927 | 0.882 | 96.732 | blend | train |
| gnn_st_v2 | post_covid | 5.488 | 3243013.799 | 3.930 | 0.881 | 96.732 | blend | train |
| persistence | post_covid | 6.527 | 55.668 | 4.663 | 0.841 | 93.900 | level | none |
| arima | post_covid | 6.687 | 62.220 | 4.875 | 0.845 | 93.028 | level | none |
| lstm | post_covid | 6.753 | 56.939 | 4.903 | 0.834 | 96.296 | level | train |
| seasonal_naive | post_covid | 6.789 | 59.100 | 4.961 | 0.818 | 97.603 | level | none |
| xgboost | post_covid | 7.187 | 3701839.602 | 4.987 | 0.860 | 95.425 | climatology | None |
| gat | post_covid | 7.406 | 73.425 | 5.430 | 0.838 | 88.889 | level | None |
| dualtopo | post_covid | 9.254 | 92.101 | 6.895 | 0.777 | 77.778 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_st (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_st (post_covid)`
- **Off-season (Apr–Sep)**: `gnn_st (post_covid)`

The same model leads every segment, so the ranking is robust to which part of the year you score.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st, gnn_st_v2; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, gnn_st_v2, lstm). Differences here are not purely model quality.
