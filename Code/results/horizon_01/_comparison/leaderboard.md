Ranked by **RMSE** within each segment, `scope=pooled`, horizon 1.

## Overall (full year) — 627 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 11.770 | 60.904 | 6.735 | 0.927 | 96.810 | blend | train |
| lstm | post_covid | 14.657 | 65.959 | 7.846 | 0.883 | 94.577 | level | train |
| arima | exclude_covid | 15.160 | 86.129 | 8.855 | 0.877 | 95.056 | level | none |
| lstm | exclude_covid | 15.438 | 62.326 | 7.888 | 0.885 | 94.896 | level | train |
| arima | post_covid | 15.506 | 82.881 | 9.092 | 0.871 | 95.853 | level | none |
| xgboost | post_covid | 15.618 | 73.172 | 8.883 | 0.866 | 97.927 | climatology | None |
| persistence | exclude_covid | 15.806 | 66.533 | 8.937 | 0.871 | 95.056 | level | none |
| persistence | post_covid | 15.806 | 66.533 | 8.937 | 0.871 | 95.056 | level | none |
| gat | post_covid | 22.450 | 119.686 | 13.214 | 0.698 | 86.603 | level | None |
| dualtopo | post_covid | 28.915 | 206.272 | 18.202 | 0.417 | 86.922 | level | train |
| seasonal_naive | exclude_covid | 39.835 | 130.621 | 19.810 | 0.417 | 94.737 | level | none |
| seasonal_naive | post_covid | 39.835 | 130.621 | 19.810 | 0.417 | 97.448 | level | none |

## Flu season (Oct–Mar) — 352 cells scored

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 14.884 | 53.157 | 8.721 | 0.922 | 95.455 | blend | train |
| lstm | post_covid | 18.868 | 49.632 | 10.517 | 0.874 | 91.193 | level | train |
| arima | exclude_covid | 19.043 | 65.157 | 11.368 | 0.871 | 92.330 | level | none |
| arima | post_covid | 19.475 | 64.992 | 11.676 | 0.865 | 93.750 | level | none |
| lstm | exclude_covid | 19.958 | 51.537 | 10.743 | 0.875 | 91.761 | level | train |
| xgboost | post_covid | 20.069 | 67.750 | 12.200 | 0.853 | 96.307 | climatology | None |
| persistence | exclude_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| persistence | post_covid | 20.132 | 60.877 | 12.051 | 0.861 | 93.182 | level | none |
| gat | post_covid | 28.125 | 80.209 | 16.735 | 0.678 | 80.966 | level | None |
| dualtopo | post_covid | 33.359 | 108.234 | 18.961 | 0.505 | 83.523 | level | train |
| seasonal_naive | exclude_covid | 52.813 | 160.265 | 31.358 | 0.315 | 91.193 | level | none |
| seasonal_naive | post_covid | 52.813 | 160.265 | 31.358 | 0.315 | 95.455 | level | none |

## Off-season (Apr–Sep) — 275 cells scored

*Mean rate is about 5 per 100,000 here, so MAPE is large and unstable by construction — rank on RMSE or MAE, not MAPE.*

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage | target_kind | normalize |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 5.682 | 70.820 | 4.192 | 0.789 | 98.545 | blend | train |
| lstm | exclude_covid | 5.794 | 76.136 | 4.235 | 0.793 | 98.909 | level | train |
| lstm | post_covid | 5.838 | 86.857 | 4.427 | 0.796 | 98.909 | level | train |
| xgboost | post_covid | 6.375 | 80.113 | 4.636 | 0.788 | 100.000 | climatology | None |
| seasonal_naive | exclude_covid | 6.914 | 92.677 | 5.029 | 0.694 | 99.273 | level | none |
| seasonal_naive | post_covid | 6.914 | 92.677 | 5.029 | 0.694 | 100.000 | level | none |
| persistence | exclude_covid | 7.132 | 73.771 | 4.950 | 0.688 | 97.455 | level | none |
| persistence | post_covid | 7.132 | 73.771 | 4.950 | 0.688 | 97.455 | level | none |
| arima | exclude_covid | 7.732 | 112.973 | 5.638 | 0.699 | 98.545 | level | none |
| arima | post_covid | 7.921 | 105.779 | 5.785 | 0.670 | 98.545 | level | none |
| gat | post_covid | 11.687 | 170.217 | 8.707 | 0.699 | 93.818 | level | None |
| dualtopo | post_covid | 21.950 | 331.761 | 17.230 | 0.599 | 91.273 | level | train |

## Does the ranking agree across segments?

- **Overall (full year)**: `gnn_st (post_covid)`
- **Flu season (Oct–Mar)**: `gnn_st (post_covid)`
- **Off-season (Apr–Sep)**: `gnn_st (post_covid)`

The same model leads every segment, so the ranking is robust to which part of the year you score.

## Comparability notes

- mixed target parameterisation in this table (blend: gnn_st; climatology: xgboost; level: arima, dualtopo, gat, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (none: arima, persistence, seasonal_naive; train: dualtopo, gnn_st, lstm). Differences here are not purely model quality.
