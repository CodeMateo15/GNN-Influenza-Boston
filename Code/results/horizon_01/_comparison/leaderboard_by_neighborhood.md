# Per-neighborhood leaderboard — horizon 1

Ranked by **RMSE**. One section per neighborhood, ordered by mean observed rate (highest burden first), and within each neighborhood one sub-table per segment: Overall (full year), Flu season (Oct–Mar), Off-season (Apr–Sep).

Every model is scored on the same weeks within a neighborhood, but coverage differs *between* neighborhoods (Charlestown has 35 suppressed weeks of 201), so the week count is reported per sub-table. Compare models down a sub-table; do not compare error magnitudes across neighborhoods or across segments without also reading the mean rate.

## Summary — neighborhoods won, out of 14

| model | Overall (full year) | Flu season (Oct–Mar) | Off-season (Apr–Sep) |
| --- | --- | --- | --- |
| lstm | 13 | 11 | 9 |
| arima | 1 | 3 | 0 |
| dualtopo_fullhistory | 0 | 0 | 2 |
| persistence | 0 | 0 | 2 |
| seasonal_naive | 0 | 0 | 1 |

Variants of the same model are pooled here. Which neighborhoods each one takes, per segment:

- **Overall (full year)** — `arima (exclude_covid)`: Dorchest.; `lstm (exclude_covid)`: BackBay+, JP, Roslind., W.Roxbury; `lstm (post_covid)`: Allston, Charles., E.Boston, Fenway, HydePark, Mattapan, Roxbury, S.Boston, S.End
- **Flu season (Oct–Mar)** — `arima (exclude_covid)`: Dorchest., Roxbury; `arima (post_covid)`: Fenway; `lstm (exclude_covid)`: BackBay+, JP, Roslind., W.Roxbury; `lstm (post_covid)`: Allston, Charles., E.Boston, HydePark, Mattapan, S.Boston, S.End
- **Off-season (Apr–Sep)** — `dualtopo_fullhistory (full)`: BackBay+, W.Roxbury; `lstm (exclude_covid)`: Allston, E.Boston, Fenway, JP, S.End; `lstm (post_covid)`: Charles., HydePark, Roslind., S.Boston; `persistence (exclude_covid)`: Dorchest., Mattapan; `seasonal_naive (exclude_covid)`: Roxbury

`lstm (post_covid)` wins 9 of 14 neighborhoods. `lstm (post_covid)` also leads the pooled leaderboard, so the ranking is consistent across both views.

## Dorchester

*mean observed 48.8, peak 256.1 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 48.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 19.712 | 52.684 | 13.266 | 0.934 | 97.959 |
| arima | post_covid | 20.278 | 55.144 | 13.935 | 0.931 | 97.959 |
| persistence | exclude_covid | 23.552 | 37.122 | 14.139 | 0.907 | 95.918 |
| persistence | post_covid | 23.552 | 37.122 | 14.139 | 0.907 | 95.918 |
| gnn_multiedge_covid_rsv_full | full | 23.816 | 44.686 | 17.329 | 0.913 | 95.918 |
| lstm | post_covid | 27.449 | 56.733 | 16.682 | 0.878 | 91.837 |
| lstm | exclude_covid | 31.197 | 59.619 | 17.606 | 0.875 | 89.796 |
| gnn_multiedge_covid_rsv | post_covid | 31.756 | 69.482 | 23.153 | 0.895 | 75.510 |
| dualtopo_fullhistory | full | 38.404 | 98.036 | 25.814 | 0.779 | 73.469 |
| gnn_multiedge | post_covid | 47.611 | 78.453 | 30.685 | 0.839 | 75.510 |
| dualtopo | post_covid | 56.200 | 252.525 | 43.196 | 0.498 | 55.102 |
| dualtopo_no_bg | post_covid | 56.471 | 255.515 | 43.439 | 0.432 | 55.102 |
| gnn_multiedge_season | post_covid | 57.043 | 88.860 | 37.072 | 0.840 | 69.388 |
| gnn_uniform | post_covid | 57.151 | 81.838 | 34.847 | 0.835 | 73.469 |
| gnn_multiedge_full | full | 60.799 | 96.628 | 40.760 | 0.739 | 67.347 |
| gnn_corrbinary | post_covid | 63.348 | 96.511 | 40.474 | 0.817 | 67.347 |
| gnn_multiedge_rt | post_covid | 65.276 | 94.661 | 40.816 | 0.783 | 73.469 |
| gnn_multiedge_leaknorm | post_covid | 74.247 | 98.064 | 44.131 | 0.796 | 75.510 |
| gnn_geo | post_covid | 75.964 | 110.817 | 50.049 | 0.786 | 59.184 |
| seasonal_naive | exclude_covid | 77.557 | 92.328 | 42.198 | 0.334 | 85.714 |
| seasonal_naive | post_covid | 77.557 | 92.328 | 42.198 | 0.334 | 89.796 |
| gnn_multiedge_level | post_covid | 103.928 | 164.129 | 66.457 | 0.587 | 61.224 |
| gnn_multiedge_season_level | post_covid | 106.231 | 153.703 | 68.051 | 0.689 | 61.224 |

### Flu season (Oct–Mar), 26 weeks scored, mean 75.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 24.898 | 21.337 | 16.724 | 0.923 | 96.154 |
| arima | post_covid | 25.342 | 21.401 | 17.016 | 0.921 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 30.134 | 33.689 | 24.370 | 0.890 | 96.154 |
| persistence | exclude_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| persistence | post_covid | 31.212 | 23.224 | 20.102 | 0.879 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 34.616 | 38.625 | 26.793 | 0.893 | 73.077 |
| lstm | post_covid | 36.664 | 31.355 | 24.308 | 0.854 | 84.615 |
| lstm | exclude_covid | 41.904 | 33.563 | 25.776 | 0.849 | 80.769 |
| gnn_multiedge | post_covid | 48.768 | 50.293 | 34.298 | 0.859 | 76.923 |
| dualtopo_fullhistory | full | 50.129 | 45.918 | 35.159 | 0.751 | 65.385 |
| gnn_uniform | post_covid | 60.697 | 49.932 | 39.492 | 0.856 | 73.077 |
| dualtopo | post_covid | 63.243 | 81.380 | 41.060 | 0.294 | 69.231 |
| dualtopo_no_bg | post_covid | 63.273 | 81.113 | 41.009 | 0.263 | 69.231 |
| gnn_multiedge_season | post_covid | 64.492 | 65.404 | 45.813 | 0.835 | 61.538 |
| gnn_multiedge_full | full | 66.070 | 72.139 | 49.967 | 0.716 | 61.538 |
| gnn_corrbinary | post_covid | 68.652 | 70.041 | 48.340 | 0.826 | 61.538 |
| gnn_multiedge_rt | post_covid | 71.081 | 69.180 | 48.751 | 0.783 | 73.077 |
| gnn_multiedge_leaknorm | post_covid | 78.177 | 64.989 | 50.279 | 0.825 | 76.923 |
| gnn_geo | post_covid | 83.625 | 91.804 | 62.809 | 0.786 | 46.154 |
| seasonal_naive | exclude_covid | 106.113 | 107.208 | 72.600 | 0.076 | 73.077 |
| seasonal_naive | post_covid | 106.113 | 107.208 | 72.600 | 0.076 | 80.769 |
| gnn_multiedge_level | post_covid | 107.398 | 128.945 | 79.669 | 0.550 | 46.154 |
| gnn_multiedge_season_level | post_covid | 117.693 | 135.120 | 86.976 | 0.663 | 46.154 |

### Off-season (Apr–Sep), 23 weeks scored, mean 18.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 8.971 | 52.834 | 7.398 | 0.828 | 95.652 |
| persistence | post_covid | 8.971 | 52.834 | 7.398 | 0.828 | 95.652 |
| lstm | post_covid | 9.249 | 85.421 | 8.061 | 0.820 | 100.000 |
| seasonal_naive | exclude_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| seasonal_naive | post_covid | 9.266 | 75.506 | 7.830 | 0.777 | 100.000 |
| lstm | exclude_covid | 9.403 | 89.074 | 8.370 | 0.816 | 100.000 |
| arima | exclude_covid | 11.270 | 88.120 | 9.357 | 0.773 | 100.000 |
| arima | post_covid | 12.248 | 93.287 | 10.451 | 0.725 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 13.485 | 57.118 | 9.370 | 0.820 | 95.652 |
| dualtopo_fullhistory | full | 17.363 | 156.953 | 15.249 | 0.653 | 82.609 |
| gnn_multiedge_covid_rsv | post_covid | 28.175 | 104.365 | 19.037 | 0.830 | 78.261 |
| gnn_multiedge | post_covid | 46.267 | 110.287 | 26.601 | 0.819 | 73.913 |
| dualtopo | post_covid | 46.986 | 445.993 | 45.612 | 0.689 | 39.130 |
| gnn_multiedge_season | post_covid | 47.227 | 115.375 | 27.190 | 0.827 | 78.261 |
| dualtopo_no_bg | post_covid | 47.626 | 452.664 | 46.187 | 0.635 | 39.130 |
| gnn_uniform | post_covid | 52.856 | 117.905 | 29.596 | 0.820 | 73.913 |
| gnn_multiedge_full | full | 54.226 | 124.312 | 30.352 | 0.812 | 73.913 |
| gnn_corrbinary | post_covid | 56.758 | 126.433 | 31.581 | 0.816 | 73.913 |
| gnn_multiedge_rt | post_covid | 58.019 | 123.465 | 31.845 | 0.810 | 73.913 |
| gnn_geo | post_covid | 66.245 | 132.310 | 35.625 | 0.809 | 73.913 |
| gnn_multiedge_leaknorm | post_covid | 69.537 | 135.452 | 37.182 | 0.813 | 73.913 |
| gnn_multiedge_season_level | post_covid | 91.562 | 174.710 | 46.657 | 0.777 | 78.261 |
| gnn_multiedge_level | post_covid | 99.860 | 203.901 | 51.522 | 0.772 | 78.261 |

## Roxbury

*mean observed 44.7, peak 254.7 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 44.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 27.796 | 57.435 | 16.381 | 0.835 | 85.714 |
| arima | exclude_covid | 28.039 | 95.072 | 17.786 | 0.835 | 89.796 |
| arima | post_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| persistence | exclude_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| persistence | post_covid | 28.650 | 78.843 | 18.598 | 0.837 | 87.755 |
| gnn_multiedge_covid_rsv_full | full | 30.181 | 90.524 | 22.431 | 0.829 | 77.551 |
| lstm | exclude_covid | 31.315 | 65.470 | 17.966 | 0.837 | 87.755 |
| gnn_multiedge_covid_rsv | post_covid | 35.176 | 112.669 | 26.863 | 0.817 | 65.306 |
| dualtopo_fullhistory | full | 38.226 | 105.083 | 23.977 | 0.738 | 79.592 |
| gnn_multiedge | post_covid | 46.330 | 123.486 | 34.012 | 0.780 | 65.306 |
| dualtopo | post_covid | 50.807 | 231.367 | 37.698 | 0.436 | 65.306 |
| dualtopo_no_bg | post_covid | 51.053 | 234.665 | 38.012 | 0.357 | 65.306 |
| gnn_multiedge_season | post_covid | 53.698 | 132.474 | 37.881 | 0.779 | 59.184 |
| gnn_uniform | post_covid | 55.395 | 126.935 | 37.032 | 0.762 | 63.265 |
| gnn_corrbinary | post_covid | 59.214 | 141.837 | 41.738 | 0.748 | 61.224 |
| gnn_multiedge_rt | post_covid | 62.271 | 141.732 | 42.705 | 0.711 | 59.184 |
| gnn_multiedge_full | full | 63.263 | 147.822 | 44.274 | 0.618 | 59.184 |
| gnn_geo | post_covid | 66.956 | 152.120 | 46.670 | 0.712 | 55.102 |
| gnn_multiedge_leaknorm | post_covid | 69.720 | 145.393 | 45.014 | 0.737 | 65.306 |
| seasonal_naive | exclude_covid | 70.506 | 90.748 | 38.590 | 0.317 | 85.714 |
| seasonal_naive | post_covid | 70.506 | 90.748 | 38.590 | 0.317 | 93.878 |
| gnn_multiedge_level | post_covid | 90.971 | 174.213 | 60.052 | 0.515 | 55.102 |
| gnn_multiedge_season_level | post_covid | 92.249 | 166.273 | 60.084 | 0.609 | 51.020 |

### Flu season (Oct–Mar), 26 weeks scored, mean 67.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 35.807 | 49.600 | 22.907 | 0.806 | 84.615 |
| arima | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | exclude_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| persistence | post_covid | 36.817 | 48.894 | 23.985 | 0.806 | 88.462 |
| lstm | post_covid | 37.106 | 36.117 | 23.649 | 0.794 | 76.923 |
| gnn_multiedge_covid_rsv_full | full | 37.505 | 66.339 | 29.608 | 0.801 | 73.077 |
| gnn_multiedge_covid_rsv | post_covid | 41.151 | 72.494 | 32.628 | 0.800 | 57.692 |
| lstm | exclude_covid | 41.950 | 43.188 | 26.339 | 0.796 | 76.923 |
| dualtopo_fullhistory | full | 50.124 | 51.775 | 32.255 | 0.701 | 73.077 |
| gnn_multiedge | post_covid | 50.646 | 89.323 | 39.868 | 0.783 | 65.385 |
| dualtopo | post_covid | 59.754 | 91.283 | 38.998 | 0.212 | 73.077 |
| dualtopo_no_bg | post_covid | 59.760 | 91.331 | 39.031 | 0.177 | 73.077 |
| gnn_uniform | post_covid | 62.437 | 88.272 | 43.239 | 0.760 | 61.538 |
| gnn_multiedge_season | post_covid | 62.610 | 104.015 | 46.927 | 0.760 | 53.846 |
| gnn_corrbinary | post_covid | 66.851 | 111.347 | 50.820 | 0.736 | 50.000 |
| gnn_multiedge_rt | post_covid | 71.163 | 110.331 | 52.073 | 0.687 | 57.692 |
| gnn_multiedge_full | full | 72.437 | 117.918 | 54.925 | 0.557 | 57.692 |
| gnn_geo | post_covid | 74.395 | 123.181 | 56.805 | 0.698 | 50.000 |
| gnn_multiedge_leaknorm | post_covid | 76.311 | 107.002 | 51.812 | 0.747 | 65.385 |
| seasonal_naive | exclude_covid | 96.460 | 128.746 | 66.950 | 0.060 | 73.077 |
| seasonal_naive | post_covid | 96.460 | 128.746 | 66.950 | 0.060 | 88.462 |
| gnn_multiedge_level | post_covid | 96.587 | 158.297 | 73.261 | 0.445 | 42.308 |
| gnn_multiedge_season_level | post_covid | 103.739 | 164.217 | 76.744 | 0.554 | 42.308 |

### Off-season (Apr–Sep), 23 weeks scored, mean 19.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| seasonal_naive | exclude_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| seasonal_naive | post_covid | 8.508 | 47.794 | 6.530 | 0.793 | 100.000 |
| lstm | post_covid | 9.463 | 81.533 | 8.166 | 0.729 | 95.652 |
| lstm | exclude_covid | 9.993 | 90.659 | 8.501 | 0.736 | 100.000 |
| arima | post_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| persistence | exclude_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| persistence | post_covid | 14.709 | 112.700 | 12.509 | 0.422 | 86.957 |
| arima | exclude_covid | 15.015 | 146.475 | 11.998 | 0.429 | 95.652 |
| dualtopo_fullhistory | full | 16.521 | 165.344 | 14.619 | 0.558 | 86.957 |
| gnn_multiedge_covid_rsv_full | full | 18.721 | 117.863 | 14.318 | 0.446 | 82.609 |
| gnn_multiedge_covid_rsv | post_covid | 26.866 | 158.083 | 20.345 | 0.548 | 73.913 |
| dualtopo | post_covid | 38.252 | 389.722 | 36.228 | 0.544 | 56.522 |
| dualtopo_no_bg | post_covid | 38.933 | 396.694 | 36.860 | 0.470 | 56.522 |
| gnn_multiedge | post_covid | 40.905 | 162.105 | 27.391 | 0.593 | 65.217 |
| gnn_multiedge_season | post_covid | 41.373 | 164.644 | 27.655 | 0.604 | 65.217 |
| gnn_uniform | post_covid | 46.158 | 170.642 | 30.016 | 0.601 | 65.217 |
| gnn_corrbinary | post_covid | 49.172 | 176.303 | 31.472 | 0.603 | 73.913 |
| gnn_multiedge_rt | post_covid | 50.362 | 177.229 | 32.115 | 0.593 | 60.870 |
| gnn_multiedge_full | full | 50.942 | 181.625 | 32.233 | 0.590 | 60.870 |
| gnn_geo | post_covid | 57.397 | 184.834 | 35.213 | 0.604 | 60.870 |
| gnn_multiedge_leaknorm | post_covid | 61.424 | 188.792 | 37.330 | 0.609 | 65.217 |
| gnn_multiedge_season_level | post_covid | 77.230 | 168.597 | 41.251 | 0.627 | 60.870 |
| gnn_multiedge_level | post_covid | 84.173 | 192.204 | 45.120 | 0.627 | 69.565 |

## Roslindale

*mean observed 32.7, peak 170.1 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 32.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 15.130 | 56.088 | 10.681 | 0.937 | 83.333 |
| lstm | post_covid | 19.728 | 58.355 | 12.418 | 0.924 | 85.714 |
| gnn_multiedge_covid_rsv_full | full | 21.916 | 94.187 | 14.441 | 0.838 | 85.714 |
| gnn_multiedge_covid_rsv | post_covid | 22.937 | 113.262 | 16.189 | 0.847 | 83.333 |
| persistence | exclude_covid | 23.222 | 85.124 | 14.843 | 0.822 | 85.714 |
| persistence | post_covid | 23.222 | 85.124 | 14.843 | 0.822 | 85.714 |
| arima | exclude_covid | 23.415 | 94.070 | 15.413 | 0.818 | 80.952 |
| dualtopo_fullhistory | full | 23.977 | 69.503 | 14.755 | 0.788 | 88.095 |
| arima | post_covid | 24.994 | 105.711 | 16.384 | 0.786 | 83.333 |
| gnn_multiedge | post_covid | 27.472 | 129.941 | 20.566 | 0.831 | 76.190 |
| gnn_uniform | post_covid | 30.225 | 124.196 | 22.893 | 0.836 | 69.048 |
| gnn_multiedge_season | post_covid | 30.911 | 144.186 | 23.111 | 0.835 | 76.190 |
| gnn_corrbinary | post_covid | 33.076 | 147.323 | 24.753 | 0.819 | 71.429 |
| gnn_multiedge_rt | post_covid | 34.940 | 149.054 | 25.362 | 0.791 | 69.048 |
| gnn_multiedge_full | full | 35.938 | 150.987 | 26.357 | 0.736 | 66.667 |
| gnn_geo | post_covid | 36.060 | 156.013 | 25.991 | 0.771 | 69.048 |
| dualtopo | post_covid | 38.582 | 164.949 | 25.822 | 0.354 | 90.476 |
| dualtopo_no_bg | post_covid | 38.627 | 166.551 | 25.947 | 0.323 | 90.476 |
| gnn_multiedge_leaknorm | post_covid | 42.749 | 155.511 | 29.714 | 0.801 | 69.048 |
| gnn_multiedge_season_level | post_covid | 49.340 | 192.338 | 32.950 | 0.650 | 61.905 |
| gnn_multiedge_level | post_covid | 50.856 | 191.570 | 34.801 | 0.531 | 59.524 |
| seasonal_naive | exclude_covid | 52.934 | 174.227 | 31.467 | 0.211 | 85.714 |
| seasonal_naive | post_covid | 52.934 | 174.227 | 31.467 | 0.211 | 95.238 |

### Flu season (Oct–Mar), 26 weeks scored, mean 43.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 18.077 | 54.783 | 13.299 | 0.938 | 84.615 |
| lstm | post_covid | 24.275 | 54.271 | 16.224 | 0.922 | 80.769 |
| gnn_multiedge_covid_rsv | post_covid | 26.413 | 119.277 | 18.264 | 0.847 | 80.769 |
| gnn_multiedge_covid_rsv_full | full | 26.746 | 107.192 | 18.046 | 0.823 | 80.769 |
| persistence | exclude_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| persistence | post_covid | 28.508 | 99.558 | 19.292 | 0.804 | 80.769 |
| arima | exclude_covid | 28.626 | 99.575 | 19.382 | 0.802 | 73.077 |
| gnn_multiedge | post_covid | 29.364 | 140.619 | 22.392 | 0.849 | 76.923 |
| dualtopo_fullhistory | full | 29.776 | 58.827 | 19.309 | 0.768 | 80.769 |
| arima | post_covid | 30.480 | 102.622 | 20.643 | 0.773 | 73.077 |
| gnn_uniform | post_covid | 32.239 | 127.549 | 25.260 | 0.854 | 69.231 |
| gnn_multiedge_season | post_covid | 34.398 | 163.487 | 26.505 | 0.845 | 76.923 |
| gnn_corrbinary | post_covid | 35.551 | 161.831 | 27.636 | 0.839 | 73.077 |
| gnn_geo | post_covid | 37.848 | 170.278 | 28.248 | 0.798 | 69.231 |
| gnn_multiedge_rt | post_covid | 38.062 | 164.693 | 28.453 | 0.803 | 69.231 |
| gnn_multiedge_full | full | 39.775 | 167.637 | 30.278 | 0.737 | 65.385 |
| gnn_multiedge_leaknorm | post_covid | 44.148 | 159.436 | 31.781 | 0.837 | 69.231 |
| dualtopo_no_bg | post_covid | 46.297 | 121.027 | 30.400 | 0.219 | 84.615 |
| dualtopo | post_covid | 46.324 | 120.650 | 30.390 | 0.227 | 84.615 |
| gnn_multiedge_season_level | post_covid | 52.425 | 226.235 | 37.209 | 0.661 | 61.538 |
| gnn_multiedge_level | post_covid | 52.544 | 218.377 | 38.993 | 0.532 | 57.692 |
| seasonal_naive | exclude_covid | 66.564 | 227.287 | 45.304 | 0.065 | 84.615 |
| seasonal_naive | post_covid | 66.564 | 227.287 | 45.304 | 0.065 | 92.308 |

### Off-season (Apr–Sep), 16 weeks scored, mean 15.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 8.000 | 64.992 | 6.234 | 0.521 | 93.750 |
| dualtopo_fullhistory | full | 8.268 | 86.852 | 7.354 | 0.632 | 100.000 |
| lstm | exclude_covid | 8.364 | 58.209 | 6.427 | 0.482 | 81.250 |
| persistence | exclude_covid | 9.741 | 61.670 | 7.612 | 0.488 | 93.750 |
| persistence | post_covid | 9.741 | 61.670 | 7.612 | 0.488 | 93.750 |
| gnn_multiedge_covid_rsv_full | full | 9.918 | 73.054 | 8.582 | 0.520 | 93.750 |
| arima | exclude_covid | 10.371 | 85.124 | 8.963 | 0.389 | 93.750 |
| arima | post_covid | 11.411 | 110.729 | 9.464 | 0.249 | 100.000 |
| seasonal_naive | exclude_covid | 12.466 | 88.004 | 8.981 | 0.115 | 87.500 |
| seasonal_naive | post_covid | 12.466 | 88.004 | 8.981 | 0.115 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 15.729 | 103.488 | 12.818 | 0.553 | 87.500 |
| dualtopo | post_covid | 20.504 | 236.934 | 18.398 | 0.523 | 100.000 |
| dualtopo_no_bg | post_covid | 20.823 | 240.528 | 18.712 | 0.493 | 100.000 |
| gnn_multiedge | post_covid | 24.084 | 112.591 | 17.600 | 0.586 | 75.000 |
| gnn_multiedge_season | post_covid | 24.193 | 112.821 | 17.594 | 0.590 | 75.000 |
| gnn_uniform | post_covid | 26.630 | 118.746 | 19.045 | 0.594 | 68.750 |
| gnn_corrbinary | post_covid | 28.600 | 123.747 | 20.069 | 0.590 | 68.750 |
| gnn_multiedge_full | full | 28.628 | 123.932 | 19.985 | 0.595 | 68.750 |
| gnn_multiedge_rt | post_covid | 29.163 | 123.640 | 20.340 | 0.587 | 68.750 |
| gnn_geo | post_covid | 32.949 | 132.833 | 22.323 | 0.589 | 68.750 |
| gnn_multiedge_leaknorm | post_covid | 40.373 | 149.133 | 26.356 | 0.594 | 68.750 |
| gnn_multiedge_season_level | post_covid | 43.865 | 137.255 | 26.029 | 0.611 | 62.500 |
| gnn_multiedge_level | post_covid | 47.988 | 148.008 | 27.987 | 0.611 | 62.500 |

## South End

*mean observed 27.0, peak 132.3 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 27.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 15.708 | 78.245 | 9.613 | 0.880 | 97.959 |
| lstm | exclude_covid | 15.773 | 59.526 | 9.509 | 0.884 | 97.959 |
| arima | exclude_covid | 16.730 | 59.722 | 9.531 | 0.862 | 93.878 |
| arima | post_covid | 16.744 | 73.483 | 9.904 | 0.853 | 97.959 |
| persistence | exclude_covid | 17.341 | 56.834 | 10.129 | 0.853 | 93.878 |
| persistence | post_covid | 17.341 | 56.834 | 10.129 | 0.853 | 93.878 |
| gnn_multiedge_covid_rsv_full | full | 17.862 | 67.337 | 11.384 | 0.848 | 89.796 |
| dualtopo_fullhistory | full | 18.023 | 77.735 | 11.087 | 0.827 | 93.878 |
| gnn_multiedge_covid_rsv | post_covid | 20.108 | 97.136 | 14.417 | 0.841 | 89.796 |
| gnn_multiedge | post_covid | 26.754 | 108.453 | 18.627 | 0.787 | 77.551 |
| gnn_uniform | post_covid | 30.752 | 115.087 | 20.826 | 0.785 | 73.469 |
| gnn_multiedge_season | post_covid | 30.782 | 122.532 | 21.957 | 0.787 | 75.510 |
| dualtopo | post_covid | 32.298 | 221.112 | 24.109 | 0.443 | 89.796 |
| dualtopo_no_bg | post_covid | 32.410 | 223.485 | 24.269 | 0.393 | 89.796 |
| gnn_corrbinary | post_covid | 33.727 | 131.111 | 23.699 | 0.760 | 71.429 |
| gnn_multiedge_full | full | 34.150 | 136.234 | 23.323 | 0.694 | 69.388 |
| gnn_multiedge_rt | post_covid | 35.072 | 131.596 | 23.753 | 0.732 | 71.429 |
| gnn_geo | post_covid | 38.669 | 147.310 | 27.381 | 0.732 | 65.306 |
| gnn_multiedge_leaknorm | post_covid | 39.662 | 140.870 | 26.539 | 0.750 | 71.429 |
| seasonal_naive | exclude_covid | 40.823 | 134.332 | 24.163 | 0.349 | 95.918 |
| seasonal_naive | post_covid | 40.823 | 134.332 | 24.163 | 0.349 | 97.959 |
| gnn_multiedge_level | post_covid | 52.549 | 200.245 | 33.581 | 0.510 | 67.347 |
| gnn_multiedge_season_level | post_covid | 52.949 | 194.977 | 34.576 | 0.596 | 61.224 |

### Flu season (Oct–Mar), 26 weeks scored, mean 41.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 20.394 | 58.336 | 12.342 | 0.857 | 96.154 |
| lstm | exclude_covid | 20.902 | 53.939 | 13.396 | 0.861 | 96.154 |
| arima | post_covid | 21.417 | 48.565 | 12.098 | 0.830 | 96.154 |
| arima | exclude_covid | 21.641 | 44.852 | 12.330 | 0.840 | 92.308 |
| persistence | exclude_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| persistence | post_covid | 22.440 | 41.314 | 13.219 | 0.830 | 92.308 |
| gnn_multiedge_covid_rsv_full | full | 22.791 | 56.697 | 15.484 | 0.821 | 88.462 |
| gnn_multiedge_covid_rsv | post_covid | 23.192 | 72.194 | 16.919 | 0.837 | 92.308 |
| dualtopo_fullhistory | full | 23.533 | 55.202 | 14.733 | 0.806 | 88.462 |
| gnn_multiedge | post_covid | 28.897 | 80.036 | 21.852 | 0.803 | 76.923 |
| gnn_uniform | post_covid | 33.602 | 81.260 | 24.614 | 0.803 | 69.231 |
| gnn_multiedge_season | post_covid | 35.457 | 101.586 | 27.840 | 0.783 | 69.231 |
| gnn_corrbinary | post_covid | 37.560 | 106.498 | 29.305 | 0.766 | 65.385 |
| gnn_multiedge_full | full | 37.976 | 110.486 | 28.369 | 0.685 | 65.385 |
| dualtopo_no_bg | post_covid | 38.789 | 132.939 | 25.974 | 0.236 | 80.769 |
| dualtopo | post_covid | 38.797 | 133.128 | 25.967 | 0.264 | 80.769 |
| gnn_multiedge_rt | post_covid | 39.405 | 106.365 | 29.133 | 0.730 | 65.385 |
| gnn_multiedge_leaknorm | post_covid | 42.328 | 101.607 | 31.402 | 0.782 | 69.231 |
| gnn_geo | post_covid | 42.832 | 122.221 | 34.300 | 0.740 | 57.692 |
| gnn_multiedge_level | post_covid | 54.508 | 174.596 | 39.780 | 0.489 | 57.692 |
| seasonal_naive | exclude_covid | 55.553 | 182.741 | 39.950 | 0.083 | 92.308 |
| seasonal_naive | post_covid | 55.553 | 182.741 | 39.950 | 0.083 | 96.154 |
| gnn_multiedge_season_level | post_covid | 58.233 | 177.718 | 42.979 | 0.574 | 53.846 |

### Off-season (Apr–Sep), 23 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.014 | 65.841 | 5.114 | 0.505 | 100.000 |
| lstm | post_covid | 7.451 | 100.751 | 6.529 | 0.547 | 100.000 |
| seasonal_naive | exclude_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| seasonal_naive | post_covid | 7.865 | 79.609 | 6.317 | 0.266 | 100.000 |
| dualtopo_fullhistory | full | 8.122 | 103.207 | 6.965 | 0.471 | 100.000 |
| arima | exclude_covid | 8.178 | 76.531 | 6.366 | 0.333 | 95.652 |
| persistence | exclude_covid | 8.449 | 74.377 | 6.635 | 0.277 | 95.652 |
| persistence | post_covid | 8.449 | 74.377 | 6.635 | 0.277 | 95.652 |
| arima | post_covid | 8.877 | 101.652 | 7.423 | 0.277 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 9.621 | 79.365 | 6.748 | 0.374 | 91.304 |
| gnn_multiedge_covid_rsv | post_covid | 15.917 | 125.332 | 11.589 | 0.432 | 86.957 |
| dualtopo | post_covid | 22.821 | 320.572 | 22.008 | 0.561 | 100.000 |
| dualtopo_no_bg | post_covid | 23.173 | 325.842 | 22.342 | 0.532 | 100.000 |
| gnn_multiedge | post_covid | 24.104 | 140.577 | 14.981 | 0.458 | 78.261 |
| gnn_multiedge_season | post_covid | 24.444 | 146.209 | 15.308 | 0.458 | 82.609 |
| gnn_uniform | post_covid | 27.172 | 153.325 | 16.544 | 0.456 | 78.261 |
| gnn_corrbinary | post_covid | 28.785 | 158.933 | 17.363 | 0.469 | 78.261 |
| gnn_multiedge_full | full | 29.227 | 165.341 | 17.619 | 0.460 | 73.913 |
| gnn_multiedge_rt | post_covid | 29.414 | 160.117 | 17.670 | 0.467 | 78.261 |
| gnn_geo | post_covid | 33.343 | 175.670 | 19.560 | 0.466 | 73.913 |
| gnn_multiedge_leaknorm | post_covid | 36.414 | 185.255 | 21.041 | 0.470 | 73.913 |
| gnn_multiedge_season_level | post_covid | 46.254 | 214.487 | 25.076 | 0.473 | 69.565 |
| gnn_multiedge_level | post_covid | 50.242 | 229.240 | 26.573 | 0.482 | 78.261 |

## Charlestown

*mean observed 19.3, peak 92.8 per 100,000 over the full year*

### Overall (full year), 35 weeks scored, mean 19.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 14.175 | 59.612 | 8.092 | 0.768 | 94.286 |
| lstm | exclude_covid | 14.593 | 58.663 | 7.946 | 0.749 | 94.286 |
| arima | exclude_covid | 16.430 | 93.918 | 9.760 | 0.667 | 97.143 |
| arima | post_covid | 17.061 | 83.159 | 10.089 | 0.629 | 97.143 |
| persistence | exclude_covid | 17.774 | 82.365 | 10.434 | 0.674 | 91.429 |
| persistence | post_covid | 17.774 | 82.365 | 10.434 | 0.674 | 91.429 |
| gnn_multiedge_covid_rsv_full | full | 17.922 | 100.071 | 11.213 | 0.675 | 91.429 |
| gnn_multiedge_covid_rsv | post_covid | 18.352 | 114.454 | 12.284 | 0.702 | 85.714 |
| dualtopo_fullhistory | full | 18.843 | 75.860 | 10.403 | 0.555 | 88.571 |
| gnn_multiedge | post_covid | 21.692 | 135.659 | 15.668 | 0.693 | 85.714 |
| dualtopo | post_covid | 21.819 | 119.644 | 14.006 | 0.303 | 88.571 |
| dualtopo_no_bg | post_covid | 21.854 | 120.109 | 14.039 | 0.237 | 88.571 |
| gnn_uniform | post_covid | 23.097 | 131.481 | 17.005 | 0.701 | 88.571 |
| gnn_multiedge_season | post_covid | 24.468 | 153.792 | 17.936 | 0.691 | 82.857 |
| gnn_corrbinary | post_covid | 26.183 | 163.898 | 19.348 | 0.680 | 82.857 |
| gnn_multiedge_full | full | 26.560 | 172.770 | 19.126 | 0.579 | 80.000 |
| gnn_multiedge_rt | post_covid | 26.696 | 162.739 | 19.596 | 0.650 | 71.429 |
| gnn_geo | post_covid | 27.758 | 176.159 | 20.922 | 0.651 | 68.571 |
| seasonal_naive | exclude_covid | 28.331 | 139.281 | 18.537 | 0.221 | 94.286 |
| seasonal_naive | post_covid | 28.331 | 139.281 | 18.537 | 0.221 | 97.143 |
| gnn_multiedge_leaknorm | post_covid | 29.287 | 174.713 | 21.211 | 0.670 | 68.571 |
| gnn_multiedge_season_level | post_covid | 35.017 | 224.343 | 25.868 | 0.543 | 57.143 |
| gnn_multiedge_level | post_covid | 35.650 | 228.859 | 25.861 | 0.441 | 57.143 |

### Flu season (Oct–Mar), 21 weeks scored, mean 25.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 17.924 | 68.644 | 11.054 | 0.742 | 90.476 |
| lstm | exclude_covid | 18.447 | 69.107 | 10.795 | 0.720 | 90.476 |
| arima | exclude_covid | 20.198 | 94.520 | 12.042 | 0.647 | 95.238 |
| arima | post_covid | 21.375 | 86.881 | 13.295 | 0.593 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 22.062 | 116.177 | 14.629 | 0.651 | 85.714 |
| persistence | exclude_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| persistence | post_covid | 22.112 | 92.586 | 13.486 | 0.650 | 90.476 |
| gnn_multiedge_covid_rsv | post_covid | 22.201 | 129.368 | 15.910 | 0.685 | 80.952 |
| dualtopo_fullhistory | full | 23.973 | 85.740 | 14.662 | 0.494 | 80.952 |
| gnn_multiedge | post_covid | 25.017 | 146.948 | 19.316 | 0.691 | 80.952 |
| gnn_uniform | post_covid | 26.089 | 131.537 | 20.654 | 0.709 | 85.714 |
| dualtopo | post_covid | 26.923 | 111.043 | 17.378 | 0.112 | 80.952 |
| dualtopo_no_bg | post_covid | 26.941 | 110.860 | 17.372 | 0.064 | 80.952 |
| gnn_multiedge_season | post_covid | 28.914 | 175.034 | 22.970 | 0.678 | 76.190 |
| gnn_multiedge_full | full | 30.205 | 192.026 | 23.415 | 0.565 | 71.429 |
| gnn_corrbinary | post_covid | 30.284 | 183.357 | 24.214 | 0.675 | 76.190 |
| gnn_multiedge_rt | post_covid | 30.705 | 178.588 | 24.399 | 0.642 | 57.143 |
| gnn_geo | post_covid | 31.260 | 192.829 | 25.633 | 0.653 | 61.905 |
| gnn_multiedge_leaknorm | post_covid | 32.278 | 181.986 | 25.148 | 0.684 | 61.905 |
| seasonal_naive | exclude_covid | 35.862 | 191.219 | 26.738 | 0.072 | 90.476 |
| seasonal_naive | post_covid | 35.862 | 191.219 | 26.738 | 0.072 | 95.238 |
| gnn_multiedge_level | post_covid | 37.441 | 256.656 | 29.976 | 0.425 | 47.619 |
| gnn_multiedge_season_level | post_covid | 38.028 | 255.637 | 30.847 | 0.540 | 47.619 |

### Off-season (Apr–Sep), 14 weeks scored, mean 10.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 4.522 | 46.064 | 3.649 | 0.529 | 100.000 |
| lstm | exclude_covid | 4.683 | 42.995 | 3.671 | 0.517 | 100.000 |
| dualtopo_fullhistory | full | 5.058 | 61.040 | 4.015 | 0.571 | 100.000 |
| arima | post_covid | 6.506 | 77.576 | 5.279 | 0.062 | 100.000 |
| persistence | exclude_covid | 7.510 | 67.032 | 5.857 | -0.140 | 92.857 |
| persistence | post_covid | 7.510 | 67.032 | 5.857 | -0.140 | 92.857 |
| arima | exclude_covid | 7.932 | 93.016 | 6.339 | -0.101 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 8.541 | 75.912 | 6.089 | 0.119 | 100.000 |
| seasonal_naive | exclude_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| seasonal_naive | post_covid | 8.799 | 61.373 | 6.236 | 0.462 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.134 | 92.084 | 6.847 | 0.322 | 92.857 |
| dualtopo | post_covid | 10.143 | 132.546 | 8.948 | 0.606 | 100.000 |
| dualtopo_no_bg | post_covid | 10.259 | 133.983 | 9.040 | 0.577 | 100.000 |
| gnn_multiedge | post_covid | 15.411 | 118.724 | 10.195 | 0.426 | 92.857 |
| gnn_multiedge_season | post_covid | 15.579 | 121.928 | 10.387 | 0.426 | 92.857 |
| gnn_uniform | post_covid | 17.685 | 131.397 | 11.532 | 0.434 | 92.857 |
| gnn_corrbinary | post_covid | 18.391 | 134.709 | 12.049 | 0.450 | 92.857 |
| gnn_multiedge_rt | post_covid | 19.173 | 138.967 | 12.391 | 0.448 | 92.857 |
| gnn_multiedge_full | full | 19.874 | 143.887 | 12.694 | 0.443 | 92.857 |
| gnn_geo | post_covid | 21.459 | 151.155 | 13.856 | 0.469 | 78.571 |
| gnn_multiedge_leaknorm | post_covid | 24.113 | 163.804 | 15.305 | 0.476 | 78.571 |
| gnn_multiedge_season_level | post_covid | 29.938 | 177.401 | 18.399 | 0.573 | 71.429 |
| gnn_multiedge_level | post_covid | 32.779 | 187.165 | 19.689 | 0.575 | 71.429 |

## Mattapan

*mean observed 18.8, peak 110.3 per 100,000 over the full year*

### Overall (full year), 47 weeks scored, mean 18.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 8.603 | 79.630 | 6.342 | 0.940 | 100.000 |
| lstm | exclude_covid | 9.391 | 68.537 | 6.508 | 0.925 | 100.000 |
| arima | post_covid | 11.883 | 93.526 | 8.428 | 0.858 | 97.872 |
| persistence | exclude_covid | 12.005 | 64.837 | 8.191 | 0.859 | 97.872 |
| persistence | post_covid | 12.005 | 64.837 | 8.191 | 0.859 | 97.872 |
| dualtopo_fullhistory | full | 12.093 | 106.193 | 9.267 | 0.869 | 97.872 |
| gnn_multiedge_covid_rsv_full | full | 12.768 | 75.276 | 9.177 | 0.849 | 95.745 |
| arima | exclude_covid | 12.829 | 90.731 | 8.566 | 0.831 | 97.872 |
| gnn_multiedge_covid_rsv | post_covid | 15.025 | 110.839 | 11.350 | 0.848 | 91.489 |
| gnn_multiedge | post_covid | 21.184 | 133.291 | 15.153 | 0.793 | 85.106 |
| gnn_uniform | post_covid | 24.050 | 134.280 | 16.488 | 0.809 | 82.979 |
| gnn_multiedge_season | post_covid | 24.720 | 146.446 | 17.737 | 0.803 | 78.723 |
| dualtopo | post_covid | 25.200 | 303.733 | 21.651 | 0.434 | 93.617 |
| dualtopo_no_bg | post_covid | 25.365 | 307.943 | 21.845 | 0.400 | 93.617 |
| gnn_corrbinary | post_covid | 27.909 | 158.114 | 19.681 | 0.772 | 80.851 |
| gnn_multiedge_full | full | 28.072 | 155.601 | 19.561 | 0.666 | 78.723 |
| gnn_multiedge_rt | post_covid | 28.338 | 153.064 | 19.261 | 0.759 | 76.596 |
| gnn_geo | post_covid | 32.515 | 176.558 | 23.083 | 0.751 | 68.085 |
| gnn_multiedge_leaknorm | post_covid | 33.590 | 177.296 | 22.555 | 0.757 | 76.596 |
| seasonal_naive | exclude_covid | 36.152 | 154.800 | 20.647 | 0.459 | 97.872 |
| seasonal_naive | post_covid | 36.152 | 154.800 | 20.647 | 0.459 | 100.000 |
| gnn_multiedge_level | post_covid | 50.381 | 284.474 | 33.669 | 0.527 | 63.830 |
| gnn_multiedge_season_level | post_covid | 50.495 | 273.269 | 34.492 | 0.640 | 63.830 |

### Flu season (Oct–Mar), 26 weeks scored, mean 28.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 9.660 | 49.868 | 6.948 | 0.938 | 100.000 |
| lstm | exclude_covid | 10.818 | 47.880 | 7.437 | 0.923 | 100.000 |
| dualtopo_fullhistory | full | 14.174 | 48.787 | 10.054 | 0.861 | 96.154 |
| arima | post_covid | 14.832 | 59.112 | 10.855 | 0.832 | 96.154 |
| persistence | exclude_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| persistence | post_covid | 15.526 | 51.869 | 11.427 | 0.833 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 16.172 | 67.594 | 12.762 | 0.819 | 92.308 |
| arima | exclude_covid | 16.265 | 56.064 | 11.389 | 0.799 | 96.154 |
| gnn_multiedge_covid_rsv | post_covid | 17.029 | 82.775 | 13.529 | 0.846 | 92.308 |
| gnn_multiedge | post_covid | 22.190 | 105.954 | 17.274 | 0.818 | 88.462 |
| gnn_uniform | post_covid | 25.215 | 97.586 | 18.594 | 0.843 | 88.462 |
| dualtopo | post_covid | 26.701 | 150.093 | 20.630 | 0.277 | 88.462 |
| dualtopo_no_bg | post_covid | 26.704 | 150.675 | 20.666 | 0.264 | 88.462 |
| gnn_multiedge_season | post_covid | 27.964 | 126.077 | 21.825 | 0.806 | 76.923 |
| gnn_corrbinary | post_covid | 30.619 | 133.143 | 23.725 | 0.787 | 84.615 |
| gnn_multiedge_rt | post_covid | 30.933 | 121.903 | 22.721 | 0.774 | 76.923 |
| gnn_multiedge_full | full | 31.425 | 130.568 | 23.859 | 0.644 | 80.769 |
| gnn_multiedge_leaknorm | post_covid | 34.820 | 137.665 | 25.714 | 0.807 | 76.923 |
| gnn_geo | post_covid | 35.430 | 149.291 | 28.142 | 0.773 | 61.538 |
| seasonal_naive | exclude_covid | 48.062 | 148.801 | 31.773 | 0.315 | 96.154 |
| seasonal_naive | post_covid | 48.062 | 148.801 | 31.773 | 0.315 | 100.000 |
| gnn_multiedge_level | post_covid | 52.114 | 241.647 | 39.202 | 0.524 | 53.846 |
| gnn_multiedge_season_level | post_covid | 54.851 | 244.774 | 42.359 | 0.649 | 53.846 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | exclude_covid | 4.910 | 80.893 | 4.186 | 0.235 | 100.000 |
| persistence | post_covid | 4.910 | 80.893 | 4.186 | 0.235 | 100.000 |
| arima | exclude_covid | 6.387 | 133.653 | 5.070 | 0.293 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.404 | 84.787 | 4.738 | 0.425 | 100.000 |
| arima | post_covid | 6.605 | 136.133 | 5.423 | 0.181 | 100.000 |
| lstm | post_covid | 7.079 | 116.480 | 5.590 | 0.612 | 100.000 |
| lstm | exclude_covid | 7.246 | 94.113 | 5.359 | 0.617 | 100.000 |
| seasonal_naive | exclude_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| seasonal_naive | post_covid | 8.075 | 162.226 | 6.871 | -0.047 | 100.000 |
| dualtopo_fullhistory | full | 8.865 | 177.268 | 8.294 | 0.706 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 12.091 | 145.585 | 8.653 | 0.524 | 90.476 |
| gnn_multiedge | post_covid | 19.869 | 167.138 | 12.527 | 0.561 | 80.952 |
| gnn_multiedge_season | post_covid | 19.988 | 171.664 | 12.675 | 0.566 | 80.952 |
| gnn_uniform | post_covid | 22.525 | 179.712 | 13.881 | 0.579 | 76.190 |
| dualtopo | post_covid | 23.208 | 493.955 | 22.916 | 0.558 | 100.000 |
| gnn_multiedge_full | full | 23.260 | 186.594 | 14.240 | 0.567 | 76.190 |
| dualtopo_no_bg | post_covid | 23.602 | 502.657 | 23.305 | 0.599 | 100.000 |
| gnn_corrbinary | post_covid | 24.135 | 189.030 | 14.674 | 0.569 | 76.190 |
| gnn_multiedge_rt | post_covid | 24.750 | 191.645 | 14.977 | 0.557 | 76.190 |
| gnn_geo | post_covid | 28.497 | 210.318 | 16.820 | 0.568 | 76.190 |
| gnn_multiedge_leaknorm | post_covid | 32.001 | 226.364 | 18.644 | 0.578 | 76.190 |
| gnn_multiedge_season_level | post_covid | 44.515 | 308.548 | 24.751 | 0.583 | 76.190 |
| gnn_multiedge_level | post_covid | 48.149 | 337.497 | 26.818 | 0.585 | 76.190 |

## Hyde Park

*mean observed 16.9, peak 94.6 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 9.397 | 65.862 | 6.157 | 0.888 | 97.826 |
| lstm | exclude_covid | 9.620 | 64.495 | 6.362 | 0.892 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 11.120 | 65.479 | 7.925 | 0.855 | 95.652 |
| arima | exclude_covid | 11.414 | 88.245 | 7.575 | 0.829 | 97.826 |
| persistence | exclude_covid | 11.663 | 55.428 | 7.276 | 0.834 | 95.652 |
| persistence | post_covid | 11.663 | 55.428 | 7.276 | 0.834 | 95.652 |
| arima | post_covid | 11.870 | 101.297 | 8.222 | 0.836 | 97.826 |
| gnn_multiedge_covid_rsv | post_covid | 13.708 | 99.449 | 10.552 | 0.847 | 95.652 |
| dualtopo_fullhistory | full | 14.765 | 105.769 | 9.777 | 0.750 | 89.130 |
| gnn_multiedge | post_covid | 19.537 | 108.077 | 13.824 | 0.801 | 86.957 |
| dualtopo | post_covid | 21.060 | 257.213 | 16.294 | 0.372 | 91.304 |
| dualtopo_no_bg | post_covid | 21.146 | 260.090 | 16.393 | 0.302 | 91.304 |
| gnn_multiedge_season | post_covid | 22.773 | 121.295 | 16.063 | 0.806 | 86.957 |
| gnn_uniform | post_covid | 22.991 | 112.550 | 15.021 | 0.792 | 78.261 |
| gnn_multiedge_full | full | 24.208 | 134.388 | 17.568 | 0.669 | 73.913 |
| gnn_corrbinary | post_covid | 25.240 | 134.193 | 17.602 | 0.770 | 76.087 |
| gnn_multiedge_rt | post_covid | 25.917 | 138.006 | 17.583 | 0.740 | 73.913 |
| gnn_geo | post_covid | 28.156 | 153.430 | 19.718 | 0.714 | 71.739 |
| gnn_multiedge_leaknorm | post_covid | 29.729 | 137.114 | 19.518 | 0.766 | 78.261 |
| seasonal_naive | exclude_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| seasonal_naive | post_covid | 33.381 | 168.632 | 19.320 | 0.174 | 97.826 |
| gnn_multiedge_level | post_covid | 42.862 | 221.740 | 28.950 | 0.508 | 63.043 |
| gnn_multiedge_season_level | post_covid | 43.156 | 212.789 | 29.069 | 0.629 | 58.696 |

### Flu season (Oct–Mar), 25 weeks scored, mean 25.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 12.119 | 45.116 | 8.149 | 0.870 | 96.000 |
| lstm | exclude_covid | 12.418 | 49.022 | 8.569 | 0.874 | 92.000 |
| gnn_multiedge_covid_rsv_full | full | 13.791 | 66.947 | 10.956 | 0.838 | 92.000 |
| arima | exclude_covid | 14.399 | 57.631 | 9.842 | 0.807 | 96.000 |
| arima | post_covid | 14.797 | 80.587 | 10.721 | 0.806 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 14.866 | 80.954 | 12.472 | 0.860 | 96.000 |
| persistence | exclude_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| persistence | post_covid | 14.963 | 53.553 | 10.440 | 0.810 | 92.000 |
| dualtopo_fullhistory | full | 19.292 | 73.349 | 13.358 | 0.714 | 80.000 |
| gnn_multiedge | post_covid | 19.819 | 97.884 | 15.894 | 0.837 | 96.000 |
| gnn_uniform | post_covid | 24.069 | 96.609 | 17.048 | 0.824 | 80.000 |
| dualtopo | post_covid | 24.232 | 114.511 | 16.598 | 0.124 | 84.000 |
| dualtopo_no_bg | post_covid | 24.234 | 114.224 | 16.597 | 0.106 | 84.000 |
| gnn_multiedge_season | post_covid | 25.257 | 117.410 | 19.898 | 0.819 | 88.000 |
| gnn_multiedge_full | full | 26.358 | 135.843 | 21.765 | 0.657 | 72.000 |
| gnn_corrbinary | post_covid | 26.945 | 131.386 | 21.205 | 0.796 | 76.000 |
| gnn_multiedge_rt | post_covid | 27.789 | 137.888 | 20.919 | 0.756 | 72.000 |
| gnn_geo | post_covid | 29.443 | 157.476 | 23.593 | 0.741 | 68.000 |
| gnn_multiedge_leaknorm | post_covid | 30.819 | 119.779 | 22.409 | 0.811 | 80.000 |
| seasonal_naive | exclude_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| seasonal_naive | post_covid | 44.872 | 213.390 | 31.396 | -0.091 | 96.000 |
| gnn_multiedge_level | post_covid | 45.652 | 236.011 | 35.363 | 0.453 | 52.000 |
| gnn_multiedge_season_level | post_covid | 48.291 | 233.688 | 36.992 | 0.601 | 44.000 |

### Off-season (Apr–Sep), 21 weeks scored, mean 7.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 4.309 | 90.559 | 3.784 | 0.603 | 100.000 |
| lstm | exclude_covid | 4.374 | 82.915 | 3.736 | 0.567 | 100.000 |
| persistence | exclude_covid | 5.605 | 57.660 | 3.510 | 0.531 | 100.000 |
| persistence | post_covid | 5.605 | 57.660 | 3.510 | 0.531 | 100.000 |
| dualtopo_fullhistory | full | 5.869 | 144.365 | 5.515 | 0.593 | 100.000 |
| arima | exclude_covid | 6.208 | 124.690 | 4.875 | 0.503 | 100.000 |
| seasonal_naive | exclude_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| seasonal_naive | post_covid | 6.617 | 115.349 | 4.943 | 0.399 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 6.667 | 63.731 | 4.317 | 0.621 | 100.000 |
| arima | post_covid | 6.928 | 125.951 | 5.247 | 0.647 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 12.186 | 121.467 | 8.266 | 0.658 | 95.238 |
| dualtopo | post_covid | 16.507 | 427.095 | 15.932 | 0.582 | 100.000 |
| dualtopo_no_bg | post_covid | 16.743 | 433.740 | 16.151 | 0.505 | 100.000 |
| gnn_multiedge | post_covid | 19.196 | 120.212 | 11.360 | 0.688 | 76.190 |
| gnn_multiedge_season | post_covid | 19.407 | 125.920 | 11.497 | 0.691 | 85.714 |
| gnn_multiedge_full | full | 21.367 | 132.657 | 12.572 | 0.704 | 76.190 |
| gnn_uniform | post_covid | 21.638 | 131.528 | 12.607 | 0.688 | 76.190 |
| gnn_corrbinary | post_covid | 23.046 | 137.536 | 13.313 | 0.691 | 76.190 |
| gnn_multiedge_rt | post_covid | 23.496 | 138.146 | 13.612 | 0.697 | 76.190 |
| gnn_geo | post_covid | 26.543 | 148.614 | 15.106 | 0.699 | 76.190 |
| gnn_multiedge_leaknorm | post_covid | 28.377 | 157.751 | 16.076 | 0.694 | 76.190 |
| gnn_multiedge_season_level | post_covid | 36.104 | 187.908 | 19.638 | 0.715 | 76.190 |
| gnn_multiedge_level | post_covid | 39.283 | 204.751 | 21.316 | 0.710 | 76.190 |

## Allston/Brighton

*mean observed 15.8, peak 80.6 per 100,000 over the full year*

### Overall (full year), 49 weeks scored, mean 15.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 7.482 | 64.140 | 4.920 | 0.928 | 95.918 |
| lstm | exclude_covid | 8.049 | 46.144 | 4.993 | 0.920 | 93.878 |
| arima | exclude_covid | 10.035 | 71.097 | 6.651 | 0.834 | 97.959 |
| arima | post_covid | 10.106 | 75.352 | 6.781 | 0.832 | 100.000 |
| persistence | exclude_covid | 10.466 | 61.309 | 6.949 | 0.833 | 100.000 |
| persistence | post_covid | 10.466 | 61.309 | 6.949 | 0.833 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 10.552 | 67.369 | 7.371 | 0.835 | 100.000 |
| dualtopo_fullhistory | full | 10.621 | 70.988 | 6.832 | 0.816 | 91.837 |
| gnn_multiedge_covid_rsv | post_covid | 11.651 | 88.754 | 8.744 | 0.835 | 100.000 |
| gnn_multiedge | post_covid | 14.782 | 100.249 | 10.609 | 0.803 | 95.918 |
| gnn_uniform | post_covid | 16.495 | 103.528 | 10.673 | 0.805 | 85.714 |
| gnn_multiedge_full | full | 16.789 | 114.065 | 12.084 | 0.753 | 89.796 |
| gnn_multiedge_season | post_covid | 16.952 | 110.668 | 11.906 | 0.804 | 93.878 |
| gnn_corrbinary | post_covid | 18.053 | 116.390 | 12.328 | 0.783 | 87.755 |
| dualtopo | post_covid | 18.116 | 191.830 | 12.891 | 0.459 | 89.796 |
| dualtopo_no_bg | post_covid | 18.185 | 194.691 | 12.997 | 0.418 | 89.796 |
| gnn_multiedge_rt | post_covid | 18.906 | 121.103 | 12.806 | 0.757 | 85.714 |
| gnn_geo | post_covid | 20.183 | 129.856 | 13.888 | 0.752 | 81.633 |
| gnn_multiedge_leaknorm | post_covid | 22.250 | 127.676 | 14.103 | 0.766 | 85.714 |
| seasonal_naive | exclude_covid | 23.121 | 125.997 | 13.633 | 0.302 | 97.959 |
| seasonal_naive | post_covid | 23.121 | 125.997 | 13.633 | 0.302 | 100.000 |
| gnn_multiedge_season_level | post_covid | 26.613 | 154.028 | 16.851 | 0.651 | 65.306 |
| gnn_multiedge_level | post_covid | 26.846 | 162.931 | 17.419 | 0.565 | 67.347 |

### Flu season (Oct–Mar), 26 weeks scored, mean 24.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 9.662 | 31.318 | 6.482 | 0.921 | 92.308 |
| lstm | exclude_covid | 10.774 | 34.463 | 7.452 | 0.903 | 88.462 |
| arima | post_covid | 13.077 | 51.014 | 9.519 | 0.794 | 100.000 |
| arima | exclude_covid | 13.239 | 53.613 | 9.672 | 0.789 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 13.539 | 58.074 | 10.342 | 0.796 | 100.000 |
| persistence | exclude_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| persistence | post_covid | 13.915 | 54.823 | 10.350 | 0.789 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 13.951 | 70.463 | 11.507 | 0.811 | 100.000 |
| dualtopo_fullhistory | full | 14.133 | 50.059 | 10.158 | 0.789 | 84.615 |
| gnn_multiedge | post_covid | 16.308 | 76.140 | 12.994 | 0.802 | 100.000 |
| gnn_uniform | post_covid | 18.099 | 73.786 | 12.456 | 0.813 | 84.615 |
| gnn_multiedge_full | full | 18.767 | 92.845 | 15.263 | 0.740 | 92.308 |
| gnn_multiedge_season | post_covid | 19.776 | 94.434 | 15.390 | 0.786 | 92.308 |
| gnn_corrbinary | post_covid | 20.066 | 94.318 | 15.153 | 0.781 | 88.462 |
| gnn_multiedge_rt | post_covid | 21.221 | 100.116 | 15.841 | 0.746 | 84.615 |
| gnn_geo | post_covid | 21.995 | 108.592 | 17.058 | 0.754 | 84.615 |
| dualtopo_no_bg | post_covid | 22.053 | 72.853 | 14.050 | 0.255 | 80.769 |
| dualtopo | post_covid | 22.057 | 72.684 | 14.041 | 0.271 | 80.769 |
| gnn_multiedge_leaknorm | post_covid | 24.109 | 95.122 | 16.585 | 0.781 | 88.462 |
| gnn_multiedge_level | post_covid | 27.434 | 126.761 | 20.683 | 0.548 | 57.692 |
| gnn_multiedge_season_level | post_covid | 28.763 | 129.592 | 20.720 | 0.635 | 53.846 |
| seasonal_naive | exclude_covid | 31.452 | 152.372 | 22.473 | 0.033 | 96.154 |
| seasonal_naive | post_covid | 31.452 | 152.372 | 22.473 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 23 weeks scored, mean 6.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.610 | 59.350 | 2.214 | 0.767 | 100.000 |
| lstm | post_covid | 3.704 | 101.244 | 3.154 | 0.761 | 100.000 |
| persistence | exclude_covid | 3.802 | 68.641 | 3.104 | 0.615 | 100.000 |
| persistence | post_covid | 3.802 | 68.641 | 3.104 | 0.615 | 100.000 |
| dualtopo_fullhistory | full | 3.812 | 94.648 | 3.071 | 0.563 | 100.000 |
| arima | exclude_covid | 4.051 | 90.861 | 3.236 | 0.626 | 100.000 |
| seasonal_naive | exclude_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| seasonal_naive | post_covid | 4.550 | 96.181 | 3.639 | 0.613 | 100.000 |
| arima | post_covid | 4.927 | 102.865 | 3.686 | 0.505 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.477 | 77.877 | 4.013 | 0.513 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.317 | 109.432 | 5.621 | 0.629 | 100.000 |
| dualtopo | post_covid | 12.217 | 326.517 | 11.590 | 0.500 | 100.000 |
| dualtopo_no_bg | post_covid | 12.440 | 332.421 | 11.806 | 0.461 | 100.000 |
| gnn_multiedge | post_covid | 12.840 | 127.503 | 7.913 | 0.636 | 91.304 |
| gnn_multiedge_season | post_covid | 13.043 | 129.019 | 7.967 | 0.650 | 95.652 |
| gnn_multiedge_full | full | 14.227 | 138.052 | 8.490 | 0.609 | 86.957 |
| gnn_uniform | post_covid | 14.468 | 137.150 | 8.657 | 0.626 | 86.957 |
| gnn_corrbinary | post_covid | 15.465 | 141.340 | 9.135 | 0.640 | 86.957 |
| gnn_multiedge_rt | post_covid | 15.888 | 144.826 | 9.375 | 0.626 | 86.957 |
| gnn_geo | post_covid | 17.916 | 153.894 | 10.305 | 0.634 | 78.261 |
| gnn_multiedge_leaknorm | post_covid | 19.941 | 164.475 | 11.297 | 0.630 | 82.609 |
| gnn_multiedge_season_level | post_covid | 23.951 | 181.651 | 12.478 | 0.623 | 78.261 |
| gnn_multiedge_level | post_covid | 26.166 | 203.819 | 13.731 | 0.617 | 78.261 |

## West Roxbury

*mean observed 15.7, peak 88.0 per 100,000 over the full year*

### Overall (full year), 40 weeks scored, mean 15.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 10.497 | 49.054 | 6.381 | 0.875 | 95.000 |
| lstm | post_covid | 11.753 | 50.587 | 7.117 | 0.860 | 92.500 |
| gnn_multiedge_covid_rsv_full | full | 13.878 | 75.679 | 8.214 | 0.737 | 95.000 |
| dualtopo_fullhistory | full | 14.217 | 58.806 | 7.375 | 0.683 | 92.500 |
| arima | post_covid | 14.324 | 85.746 | 8.560 | 0.680 | 95.000 |
| arima | exclude_covid | 14.371 | 87.626 | 8.497 | 0.667 | 95.000 |
| persistence | exclude_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| persistence | post_covid | 14.426 | 68.768 | 8.340 | 0.722 | 92.500 |
| gnn_multiedge_covid_rsv | post_covid | 14.539 | 100.925 | 9.751 | 0.746 | 95.000 |
| gnn_multiedge | post_covid | 16.560 | 120.401 | 11.946 | 0.743 | 90.000 |
| gnn_uniform | post_covid | 17.220 | 119.080 | 12.121 | 0.756 | 87.500 |
| gnn_multiedge_season | post_covid | 18.153 | 131.687 | 13.209 | 0.750 | 92.500 |
| gnn_corrbinary | post_covid | 18.970 | 137.564 | 13.963 | 0.739 | 92.500 |
| dualtopo | post_covid | 19.198 | 111.346 | 10.863 | 0.289 | 92.500 |
| dualtopo_no_bg | post_covid | 19.212 | 113.366 | 10.970 | 0.284 | 92.500 |
| gnn_multiedge_rt | post_covid | 19.543 | 138.186 | 14.302 | 0.722 | 82.500 |
| gnn_geo | post_covid | 19.648 | 145.262 | 14.235 | 0.710 | 82.500 |
| gnn_multiedge_full | full | 19.994 | 136.616 | 14.598 | 0.656 | 85.000 |
| gnn_multiedge_leaknorm | post_covid | 22.959 | 161.309 | 16.098 | 0.725 | 85.000 |
| seasonal_naive | exclude_covid | 23.197 | 111.178 | 14.205 | 0.253 | 95.000 |
| seasonal_naive | post_covid | 23.197 | 111.178 | 14.205 | 0.253 | 97.500 |
| gnn_multiedge_season_level | post_covid | 24.354 | 173.027 | 17.079 | 0.599 | 65.000 |
| gnn_multiedge_level | post_covid | 25.597 | 179.284 | 18.156 | 0.474 | 62.500 |

### Flu season (Oct–Mar), 25 weeks scored, mean 20.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 12.894 | 45.954 | 8.105 | 0.870 | 92.000 |
| lstm | post_covid | 14.549 | 48.447 | 9.252 | 0.852 | 88.000 |
| gnn_multiedge_covid_rsv_full | full | 17.075 | 79.486 | 10.765 | 0.710 | 92.000 |
| gnn_multiedge_covid_rsv | post_covid | 17.299 | 97.508 | 12.078 | 0.732 | 92.000 |
| arima | post_covid | 17.618 | 78.684 | 10.757 | 0.655 | 92.000 |
| arima | exclude_covid | 17.666 | 78.247 | 10.717 | 0.638 | 92.000 |
| dualtopo_fullhistory | full | 17.735 | 54.882 | 9.730 | 0.651 | 88.000 |
| persistence | exclude_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| persistence | post_covid | 17.756 | 73.667 | 10.856 | 0.697 | 88.000 |
| gnn_multiedge | post_covid | 18.649 | 110.146 | 14.120 | 0.749 | 88.000 |
| gnn_uniform | post_covid | 19.093 | 102.600 | 13.928 | 0.770 | 84.000 |
| gnn_multiedge_season | post_covid | 20.850 | 126.463 | 16.055 | 0.750 | 92.000 |
| gnn_corrbinary | post_covid | 21.190 | 126.926 | 16.572 | 0.749 | 92.000 |
| gnn_geo | post_covid | 21.211 | 128.731 | 16.234 | 0.732 | 80.000 |
| gnn_multiedge_rt | post_covid | 21.894 | 125.952 | 16.989 | 0.730 | 80.000 |
| gnn_multiedge_full | full | 22.625 | 124.199 | 17.473 | 0.652 | 80.000 |
| dualtopo_no_bg | post_covid | 23.375 | 79.485 | 12.918 | 0.197 | 88.000 |
| dualtopo | post_covid | 23.400 | 78.674 | 12.878 | 0.192 | 88.000 |
| gnn_multiedge_leaknorm | post_covid | 24.528 | 139.574 | 18.132 | 0.756 | 84.000 |
| gnn_multiedge_season_level | post_covid | 25.020 | 156.634 | 18.920 | 0.640 | 64.000 |
| gnn_multiedge_level | post_covid | 25.827 | 157.432 | 20.013 | 0.509 | 56.000 |
| seasonal_naive | exclude_covid | 29.094 | 143.500 | 20.532 | 0.116 | 92.000 |
| seasonal_naive | post_covid | 29.094 | 143.500 | 20.532 | 0.116 | 96.000 |

### Off-season (Apr–Sep), 15 weeks scored, mean 7.3

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.841 | 65.348 | 3.449 | 0.294 | 100.000 |
| lstm | post_covid | 3.952 | 54.154 | 3.559 | 0.205 | 100.000 |
| lstm | exclude_covid | 4.095 | 54.220 | 3.506 | 0.269 | 100.000 |
| seasonal_naive | exclude_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| seasonal_naive | post_covid | 4.910 | 57.308 | 3.660 | 0.182 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.255 | 69.335 | 3.962 | 0.177 | 100.000 |
| persistence | exclude_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| persistence | post_covid | 5.430 | 60.604 | 4.147 | -0.069 | 100.000 |
| arima | post_covid | 5.459 | 97.514 | 4.898 | -0.265 | 100.000 |
| arima | exclude_covid | 5.528 | 103.256 | 4.796 | -0.219 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 8.055 | 106.619 | 5.872 | 0.139 | 100.000 |
| dualtopo | post_covid | 8.382 | 165.800 | 7.505 | 0.177 | 100.000 |
| dualtopo_no_bg | post_covid | 8.582 | 169.833 | 7.723 | 0.174 | 100.000 |
| gnn_multiedge | post_covid | 12.316 | 137.494 | 8.321 | 0.188 | 93.333 |
| gnn_multiedge_season | post_covid | 12.418 | 140.394 | 8.465 | 0.195 | 93.333 |
| gnn_uniform | post_covid | 13.533 | 146.546 | 9.110 | 0.222 | 93.333 |
| gnn_corrbinary | post_covid | 14.536 | 155.292 | 9.616 | 0.212 | 93.333 |
| gnn_multiedge_full | full | 14.588 | 157.310 | 9.806 | 0.242 | 93.333 |
| gnn_multiedge_rt | post_covid | 14.818 | 158.576 | 9.824 | 0.216 | 86.667 |
| gnn_geo | post_covid | 16.721 | 172.813 | 10.902 | 0.239 | 86.667 |
| gnn_multiedge_leaknorm | post_covid | 20.073 | 197.535 | 12.710 | 0.246 | 86.667 |
| gnn_multiedge_season_level | post_covid | 23.202 | 200.347 | 14.012 | 0.309 | 66.667 |
| gnn_multiedge_level | post_covid | 25.211 | 215.704 | 15.062 | 0.300 | 73.333 |

## South Boston

*mean observed 12.0, peak 57.0 per 100,000 over the full year*

### Overall (full year), 42 weeks scored, mean 12.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 6.927 | 43.440 | 4.041 | 0.864 | 92.857 |
| lstm | exclude_covid | 7.539 | 57.942 | 4.468 | 0.865 | 97.619 |
| arima | exclude_covid | 8.225 | 82.565 | 5.499 | 0.784 | 97.619 |
| dualtopo_fullhistory | full | 8.382 | 81.457 | 5.724 | 0.791 | 95.238 |
| persistence | exclude_covid | 8.667 | 52.202 | 5.379 | 0.785 | 95.238 |
| persistence | post_covid | 8.667 | 52.202 | 5.379 | 0.785 | 95.238 |
| gnn_multiedge_covid_rsv_full | full | 8.750 | 60.235 | 5.903 | 0.789 | 95.238 |
| arima | post_covid | 8.919 | 77.581 | 5.732 | 0.746 | 92.857 |
| gnn_multiedge_covid_rsv | post_covid | 9.397 | 90.233 | 6.964 | 0.801 | 97.619 |
| gnn_multiedge | post_covid | 12.116 | 102.464 | 8.693 | 0.763 | 97.619 |
| dualtopo | post_covid | 13.099 | 186.090 | 9.438 | 0.427 | 90.476 |
| dualtopo_no_bg | post_covid | 13.126 | 187.245 | 9.487 | 0.401 | 90.476 |
| gnn_uniform | post_covid | 13.533 | 108.590 | 9.519 | 0.771 | 95.238 |
| gnn_multiedge_season | post_covid | 13.789 | 114.365 | 10.146 | 0.778 | 100.000 |
| gnn_corrbinary | post_covid | 15.081 | 123.301 | 10.895 | 0.744 | 97.619 |
| gnn_multiedge_rt | post_covid | 15.420 | 124.574 | 10.916 | 0.722 | 85.714 |
| gnn_multiedge_full | full | 16.196 | 130.863 | 11.572 | 0.638 | 85.714 |
| gnn_geo | post_covid | 17.170 | 140.082 | 12.649 | 0.721 | 83.333 |
| gnn_multiedge_leaknorm | post_covid | 18.726 | 141.506 | 12.763 | 0.738 | 88.095 |
| seasonal_naive | exclude_covid | 21.966 | 110.135 | 11.810 | 0.233 | 95.238 |
| seasonal_naive | post_covid | 21.966 | 110.135 | 11.810 | 0.233 | 97.619 |
| gnn_multiedge_level | post_covid | 22.119 | 176.532 | 15.027 | 0.556 | 64.286 |
| gnn_multiedge_season_level | post_covid | 22.184 | 168.453 | 15.392 | 0.656 | 66.667 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 8.619 | 40.667 | 5.249 | 0.846 | 92.000 |
| lstm | exclude_covid | 9.423 | 53.650 | 5.879 | 0.848 | 96.000 |
| arima | exclude_covid | 9.893 | 61.045 | 6.358 | 0.757 | 96.000 |
| dualtopo_fullhistory | full | 10.366 | 64.721 | 7.409 | 0.771 | 92.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.605 | 71.419 | 8.308 | 0.792 | 96.000 |
| persistence | exclude_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| persistence | post_covid | 10.648 | 45.561 | 6.916 | 0.752 | 92.000 |
| gnn_multiedge_covid_rsv_full | full | 10.891 | 60.305 | 8.114 | 0.742 | 92.000 |
| arima | post_covid | 10.993 | 62.474 | 7.091 | 0.710 | 88.000 |
| gnn_multiedge | post_covid | 12.858 | 79.299 | 10.059 | 0.777 | 96.000 |
| gnn_uniform | post_covid | 14.453 | 81.285 | 11.007 | 0.789 | 96.000 |
| gnn_multiedge_season | post_covid | 15.367 | 96.467 | 12.403 | 0.778 | 100.000 |
| dualtopo_no_bg | post_covid | 15.402 | 136.425 | 10.302 | 0.295 | 84.000 |
| dualtopo | post_covid | 15.407 | 136.737 | 10.300 | 0.320 | 84.000 |
| gnn_corrbinary | post_covid | 16.396 | 100.847 | 13.026 | 0.751 | 100.000 |
| gnn_multiedge_rt | post_covid | 16.840 | 102.961 | 12.987 | 0.722 | 84.000 |
| gnn_multiedge_full | full | 17.992 | 112.255 | 14.061 | 0.609 | 88.000 |
| gnn_geo | post_covid | 18.654 | 117.457 | 15.304 | 0.728 | 84.000 |
| gnn_multiedge_leaknorm | post_covid | 19.601 | 104.138 | 14.575 | 0.773 | 92.000 |
| gnn_multiedge_level | post_covid | 22.245 | 146.438 | 17.160 | 0.568 | 60.000 |
| gnn_multiedge_season_level | post_covid | 23.469 | 145.740 | 18.365 | 0.669 | 64.000 |
| seasonal_naive | exclude_covid | 28.341 | 147.167 | 18.064 | 0.058 | 92.000 |
| seasonal_naive | post_covid | 28.341 | 147.167 | 18.064 | 0.058 | 96.000 |

### Off-season (Apr–Sep), 17 weeks scored, mean 4.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.049 | 47.519 | 2.264 | 0.332 | 94.118 |
| lstm | exclude_covid | 3.139 | 64.253 | 2.394 | 0.325 | 100.000 |
| seasonal_naive | exclude_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| seasonal_naive | post_covid | 3.295 | 55.676 | 2.612 | 0.223 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.834 | 60.132 | 2.652 | 0.339 | 100.000 |
| dualtopo_fullhistory | full | 3.948 | 106.070 | 3.247 | 0.270 | 100.000 |
| arima | post_covid | 4.335 | 99.798 | 3.732 | -0.044 | 100.000 |
| persistence | exclude_covid | 4.341 | 61.969 | 3.118 | 0.004 | 100.000 |
| persistence | post_covid | 4.341 | 61.969 | 3.118 | 0.004 | 100.000 |
| arima | exclude_covid | 4.816 | 114.212 | 4.236 | -0.098 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 7.266 | 117.902 | 4.987 | 0.241 | 100.000 |
| dualtopo | post_covid | 8.650 | 258.666 | 8.171 | 0.205 | 100.000 |
| dualtopo_no_bg | post_covid | 8.762 | 261.979 | 8.288 | 0.229 | 100.000 |
| gnn_multiedge | post_covid | 10.935 | 136.531 | 6.684 | 0.307 | 100.000 |
| gnn_multiedge_season | post_covid | 11.066 | 140.685 | 6.826 | 0.318 | 100.000 |
| gnn_uniform | post_covid | 12.052 | 148.745 | 7.330 | 0.328 | 94.118 |
| gnn_corrbinary | post_covid | 12.907 | 156.323 | 7.760 | 0.330 | 94.118 |
| gnn_multiedge_rt | post_covid | 13.053 | 156.359 | 7.870 | 0.345 | 88.235 |
| gnn_multiedge_full | full | 13.116 | 158.228 | 7.912 | 0.356 | 82.353 |
| gnn_geo | post_covid | 14.719 | 173.353 | 8.744 | 0.341 | 82.353 |
| gnn_multiedge_leaknorm | post_covid | 17.359 | 196.460 | 10.098 | 0.356 | 82.353 |
| gnn_multiedge_season_level | post_covid | 20.145 | 201.855 | 11.022 | 0.396 | 70.588 |
| gnn_multiedge_level | post_covid | 21.932 | 220.789 | 11.889 | 0.389 | 70.588 |

## Back Bay/Beacon Hill/Downtown/North End/West End

*mean observed 11.9, peak 58.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 6.133 | 71.266 | 4.662 | 0.874 | 100.000 |
| lstm | post_covid | 7.442 | 74.714 | 5.287 | 0.850 | 93.478 |
| dualtopo_fullhistory | full | 8.036 | 83.010 | 5.741 | 0.774 | 95.652 |
| arima | exclude_covid | 9.092 | 92.208 | 5.794 | 0.691 | 95.652 |
| arima | post_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| persistence | exclude_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| persistence | post_covid | 9.764 | 67.561 | 6.089 | 0.693 | 97.826 |
| gnn_multiedge_covid_rsv_full | full | 9.830 | 72.344 | 6.548 | 0.700 | 95.652 |
| gnn_multiedge_covid_rsv | post_covid | 10.924 | 101.564 | 8.025 | 0.692 | 95.652 |
| dualtopo | post_covid | 12.290 | 188.995 | 8.371 | 0.511 | 93.478 |
| dualtopo_no_bg | post_covid | 12.341 | 193.734 | 8.475 | 0.466 | 93.478 |
| gnn_multiedge | post_covid | 13.523 | 110.688 | 9.637 | 0.656 | 97.826 |
| gnn_uniform | post_covid | 14.449 | 113.199 | 9.836 | 0.662 | 97.826 |
| gnn_multiedge_season | post_covid | 14.812 | 118.121 | 10.374 | 0.678 | 97.826 |
| gnn_multiedge_full | full | 15.261 | 131.366 | 11.155 | 0.617 | 93.478 |
| gnn_corrbinary | post_covid | 15.768 | 127.517 | 11.178 | 0.664 | 97.826 |
| gnn_multiedge_rt | post_covid | 16.183 | 129.574 | 11.162 | 0.628 | 91.304 |
| gnn_geo | post_covid | 17.336 | 138.901 | 12.355 | 0.625 | 84.783 |
| seasonal_naive | exclude_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| seasonal_naive | post_covid | 18.077 | 140.285 | 10.824 | 0.266 | 97.826 |
| gnn_multiedge_leaknorm | post_covid | 18.870 | 138.670 | 12.501 | 0.639 | 89.130 |
| gnn_multiedge_season_level | post_covid | 20.388 | 144.075 | 13.596 | 0.619 | 60.870 |
| gnn_multiedge_level | post_covid | 20.591 | 151.665 | 14.224 | 0.561 | 65.217 |

### Flu season (Oct–Mar), 26 weeks scored, mean 17.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.660 | 44.593 | 6.091 | 0.862 | 100.000 |
| lstm | post_covid | 9.534 | 48.260 | 7.242 | 0.835 | 88.462 |
| dualtopo_fullhistory | full | 10.354 | 56.345 | 8.184 | 0.736 | 92.308 |
| arima | exclude_covid | 11.576 | 53.205 | 7.766 | 0.594 | 92.308 |
| arima | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | exclude_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| persistence | post_covid | 12.565 | 51.438 | 8.600 | 0.594 | 96.154 |
| gnn_multiedge_covid_rsv_full | full | 12.705 | 62.822 | 9.450 | 0.577 | 92.308 |
| gnn_multiedge_covid_rsv | post_covid | 13.383 | 71.442 | 10.469 | 0.591 | 92.308 |
| dualtopo_no_bg | post_covid | 14.686 | 79.577 | 9.044 | 0.303 | 88.462 |
| dualtopo | post_covid | 14.713 | 78.624 | 9.041 | 0.339 | 88.462 |
| gnn_multiedge | post_covid | 15.682 | 84.655 | 11.992 | 0.570 | 96.154 |
| gnn_uniform | post_covid | 16.500 | 82.315 | 11.811 | 0.598 | 96.154 |
| gnn_multiedge_full | full | 17.258 | 106.762 | 13.757 | 0.519 | 92.308 |
| gnn_multiedge_season | post_covid | 17.570 | 96.298 | 13.280 | 0.585 | 96.154 |
| gnn_corrbinary | post_covid | 18.181 | 103.759 | 13.927 | 0.578 | 96.154 |
| gnn_multiedge_rt | post_covid | 18.634 | 105.757 | 13.736 | 0.533 | 88.462 |
| gnn_geo | post_covid | 19.574 | 113.447 | 15.216 | 0.533 | 84.615 |
| gnn_multiedge_level | post_covid | 20.713 | 127.710 | 16.444 | 0.515 | 61.538 |
| gnn_multiedge_leaknorm | post_covid | 21.013 | 102.696 | 14.733 | 0.580 | 88.462 |
| gnn_multiedge_season_level | post_covid | 21.627 | 129.548 | 16.111 | 0.569 | 53.846 |
| seasonal_naive | exclude_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |
| seasonal_naive | post_covid | 23.642 | 145.363 | 16.119 | 0.027 | 96.154 |

### Off-season (Apr–Sep), 20 weeks scored, mean 4.5

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| dualtopo_fullhistory | full | 3.029 | 117.673 | 2.565 | 0.660 | 100.000 |
| lstm | post_covid | 3.033 | 109.106 | 2.746 | 0.542 | 100.000 |
| lstm | exclude_covid | 3.199 | 105.941 | 2.804 | 0.476 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.519 | 84.722 | 2.775 | 0.623 | 100.000 |
| arima | post_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| persistence | exclude_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| persistence | post_covid | 3.742 | 88.521 | 2.825 | 0.381 | 100.000 |
| arima | exclude_covid | 3.992 | 142.912 | 3.230 | 0.387 | 100.000 |
| seasonal_naive | exclude_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| seasonal_naive | post_covid | 4.998 | 133.684 | 3.940 | 0.232 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 6.452 | 140.722 | 4.849 | 0.604 | 100.000 |
| dualtopo | post_covid | 8.122 | 332.478 | 7.500 | 0.586 | 100.000 |
| dualtopo_no_bg | post_covid | 8.361 | 342.137 | 7.736 | 0.550 | 100.000 |
| gnn_multiedge | post_covid | 10.046 | 144.531 | 6.577 | 0.657 | 100.000 |
| gnn_multiedge_season | post_covid | 10.161 | 146.490 | 6.596 | 0.663 | 100.000 |
| gnn_uniform | post_covid | 11.235 | 153.348 | 7.269 | 0.677 | 100.000 |
| gnn_corrbinary | post_covid | 11.923 | 158.402 | 7.605 | 0.675 | 100.000 |
| gnn_multiedge_full | full | 12.185 | 163.351 | 7.773 | 0.689 | 95.000 |
| gnn_multiedge_rt | post_covid | 12.286 | 160.536 | 7.816 | 0.683 | 95.000 |
| gnn_geo | post_covid | 13.898 | 171.991 | 8.637 | 0.686 | 85.000 |
| gnn_multiedge_leaknorm | post_covid | 15.652 | 185.436 | 9.599 | 0.688 | 90.000 |
| gnn_multiedge_season_level | post_covid | 18.653 | 162.960 | 10.327 | 0.725 | 70.000 |
| gnn_multiedge_level | post_covid | 20.431 | 182.806 | 11.338 | 0.719 | 70.000 |

## East Boston

*mean observed 11.6, peak 59.3 per 100,000 over the full year*

### Overall (full year), 44 weeks scored, mean 11.6

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 6.299 | 78.193 | 4.605 | 0.880 | 97.727 |
| lstm | exclude_covid | 6.784 | 79.056 | 4.733 | 0.868 | 95.455 |
| arima | post_covid | 7.778 | 114.838 | 6.031 | 0.801 | 97.727 |
| dualtopo_fullhistory | full | 7.988 | 98.272 | 5.669 | 0.797 | 95.455 |
| gnn_multiedge_covid_rsv_full | full | 7.999 | 108.838 | 5.910 | 0.815 | 100.000 |
| persistence | exclude_covid | 8.242 | 98.656 | 6.239 | 0.797 | 97.727 |
| persistence | post_covid | 8.242 | 98.656 | 6.239 | 0.797 | 97.727 |
| arima | exclude_covid | 8.884 | 122.953 | 7.092 | 0.752 | 93.182 |
| gnn_multiedge_covid_rsv | post_covid | 9.475 | 140.413 | 6.834 | 0.799 | 97.727 |
| gnn_multiedge | post_covid | 12.536 | 165.556 | 9.039 | 0.761 | 95.455 |
| dualtopo | post_covid | 12.874 | 211.771 | 9.356 | 0.434 | 90.909 |
| dualtopo_no_bg | post_covid | 12.908 | 213.362 | 9.402 | 0.387 | 90.909 |
| gnn_uniform | post_covid | 14.049 | 171.154 | 9.775 | 0.758 | 93.182 |
| gnn_multiedge_season | post_covid | 14.342 | 182.625 | 10.424 | 0.766 | 95.455 |
| gnn_multiedge_full | full | 14.750 | 180.114 | 10.449 | 0.666 | 93.182 |
| gnn_corrbinary | post_covid | 15.729 | 192.913 | 11.371 | 0.741 | 93.182 |
| gnn_multiedge_rt | post_covid | 16.168 | 191.231 | 11.582 | 0.713 | 86.364 |
| gnn_geo | post_covid | 18.410 | 212.043 | 13.523 | 0.720 | 77.273 |
| gnn_multiedge_leaknorm | post_covid | 18.440 | 214.854 | 12.880 | 0.734 | 88.636 |
| seasonal_naive | exclude_covid | 18.593 | 140.186 | 10.843 | 0.308 | 97.727 |
| seasonal_naive | post_covid | 18.593 | 140.186 | 10.843 | 0.308 | 100.000 |
| gnn_multiedge_season_level | post_covid | 23.570 | 246.484 | 16.299 | 0.616 | 63.636 |
| gnn_multiedge_level | post_covid | 23.849 | 257.705 | 16.278 | 0.525 | 63.636 |

### Flu season (Oct–Mar), 25 weeks scored, mean 16.8

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 7.996 | 82.302 | 6.392 | 0.866 | 96.000 |
| lstm | exclude_covid | 8.676 | 86.913 | 6.654 | 0.848 | 92.000 |
| arima | post_covid | 9.430 | 115.902 | 7.673 | 0.783 | 96.000 |
| gnn_multiedge_covid_rsv_full | full | 9.938 | 134.897 | 8.153 | 0.776 | 100.000 |
| dualtopo_fullhistory | full | 10.100 | 78.344 | 7.360 | 0.776 | 92.000 |
| persistence | exclude_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| persistence | post_covid | 10.229 | 115.447 | 8.480 | 0.770 | 96.000 |
| gnn_multiedge_covid_rsv | post_covid | 10.529 | 163.474 | 8.230 | 0.790 | 96.000 |
| arima | exclude_covid | 10.816 | 126.112 | 9.190 | 0.727 | 92.000 |
| gnn_multiedge | post_covid | 12.862 | 188.403 | 10.310 | 0.779 | 96.000 |
| gnn_uniform | post_covid | 14.537 | 191.531 | 11.058 | 0.780 | 96.000 |
| dualtopo_no_bg | post_covid | 15.315 | 135.402 | 10.241 | 0.189 | 84.000 |
| dualtopo | post_covid | 15.315 | 135.554 | 10.246 | 0.203 | 84.000 |
| gnn_multiedge_season | post_covid | 15.777 | 215.791 | 12.688 | 0.761 | 96.000 |
| gnn_multiedge_full | full | 16.150 | 207.906 | 12.457 | 0.636 | 92.000 |
| gnn_corrbinary | post_covid | 16.786 | 226.113 | 13.547 | 0.745 | 96.000 |
| gnn_multiedge_rt | post_covid | 17.312 | 220.244 | 13.738 | 0.710 | 88.000 |
| gnn_multiedge_leaknorm | post_covid | 18.813 | 244.290 | 14.638 | 0.765 | 92.000 |
| gnn_geo | post_covid | 20.068 | 251.004 | 16.570 | 0.713 | 72.000 |
| gnn_multiedge_level | post_covid | 24.435 | 299.574 | 18.734 | 0.481 | 56.000 |
| seasonal_naive | exclude_covid | 24.458 | 164.523 | 16.724 | 0.102 | 96.000 |
| seasonal_naive | post_covid | 24.458 | 164.523 | 16.724 | 0.102 | 100.000 |
| gnn_multiedge_season_level | post_covid | 25.300 | 293.980 | 19.602 | 0.584 | 56.000 |

### Off-season (Apr–Sep), 19 weeks scored, mean 4.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.744 | 68.718 | 2.205 | 0.570 | 100.000 |
| lstm | post_covid | 2.783 | 72.787 | 2.255 | 0.560 | 100.000 |
| seasonal_naive | exclude_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| seasonal_naive | post_covid | 3.673 | 108.164 | 3.105 | 0.352 | 100.000 |
| dualtopo_fullhistory | full | 3.681 | 124.494 | 3.444 | 0.606 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 4.271 | 74.549 | 2.958 | 0.581 | 100.000 |
| persistence | exclude_covid | 4.433 | 76.563 | 3.289 | 0.330 | 100.000 |
| persistence | post_covid | 4.433 | 76.563 | 3.289 | 0.330 | 100.000 |
| arima | post_covid | 4.805 | 113.437 | 3.870 | 0.310 | 100.000 |
| arima | exclude_covid | 5.372 | 118.797 | 4.333 | 0.237 | 94.737 |
| gnn_multiedge_covid_rsv | post_covid | 7.877 | 110.069 | 4.997 | 0.572 | 100.000 |
| dualtopo | post_covid | 8.672 | 312.057 | 8.184 | 0.562 | 100.000 |
| dualtopo_no_bg | post_covid | 8.790 | 315.942 | 8.299 | 0.592 | 100.000 |
| gnn_multiedge | post_covid | 12.095 | 135.495 | 7.367 | 0.610 | 94.737 |
| gnn_multiedge_season | post_covid | 12.200 | 138.985 | 7.445 | 0.615 | 94.737 |
| gnn_multiedge_full | full | 12.675 | 143.546 | 7.808 | 0.638 | 94.737 |
| gnn_uniform | post_covid | 13.380 | 144.343 | 8.086 | 0.632 | 89.474 |
| gnn_corrbinary | post_covid | 14.218 | 149.229 | 8.508 | 0.630 | 89.474 |
| gnn_multiedge_rt | post_covid | 14.527 | 153.056 | 8.745 | 0.639 | 84.211 |
| gnn_geo | post_covid | 15.967 | 160.778 | 9.513 | 0.644 | 84.211 |
| gnn_multiedge_leaknorm | post_covid | 17.938 | 176.121 | 10.566 | 0.651 | 84.211 |
| gnn_multiedge_season_level | post_covid | 21.079 | 183.990 | 11.952 | 0.692 | 73.684 |
| gnn_multiedge_level | post_covid | 23.055 | 202.615 | 13.046 | 0.685 | 73.684 |

## Jamaica Plain

*mean observed 11.0, peak 61.1 per 100,000 over the full year*

### Overall (full year), 46 weeks scored, mean 11.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 5.772 | 68.888 | 3.940 | 0.917 | 100.000 |
| lstm | post_covid | 6.115 | 75.146 | 4.123 | 0.914 | 100.000 |
| arima | exclude_covid | 7.587 | 90.832 | 4.923 | 0.836 | 95.652 |
| gnn_multiedge_covid_rsv_full | full | 7.793 | 66.495 | 4.949 | 0.842 | 95.652 |
| dualtopo_fullhistory | full | 7.868 | 107.343 | 5.315 | 0.823 | 95.652 |
| arima | post_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| persistence | exclude_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| persistence | post_covid | 7.874 | 58.857 | 4.800 | 0.837 | 97.826 |
| gnn_multiedge_covid_rsv | post_covid | 8.539 | 96.569 | 6.256 | 0.839 | 100.000 |
| gnn_multiedge | post_covid | 10.468 | 100.544 | 7.519 | 0.818 | 97.826 |
| gnn_uniform | post_covid | 11.863 | 102.134 | 8.248 | 0.818 | 100.000 |
| gnn_multiedge_season | post_covid | 11.937 | 115.377 | 8.768 | 0.818 | 100.000 |
| gnn_corrbinary | post_covid | 13.071 | 119.277 | 9.363 | 0.800 | 100.000 |
| gnn_multiedge_rt | post_covid | 13.362 | 119.736 | 9.368 | 0.778 | 97.826 |
| gnn_multiedge_full | full | 13.773 | 125.515 | 9.775 | 0.714 | 93.478 |
| dualtopo | post_covid | 13.794 | 226.490 | 9.919 | 0.418 | 91.304 |
| dualtopo_no_bg | post_covid | 13.844 | 230.226 | 10.013 | 0.366 | 91.304 |
| gnn_geo | post_covid | 14.110 | 130.689 | 10.112 | 0.763 | 86.957 |
| gnn_multiedge_leaknorm | post_covid | 16.252 | 133.086 | 10.978 | 0.775 | 91.304 |
| seasonal_naive | exclude_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| seasonal_naive | post_covid | 17.549 | 146.330 | 10.665 | 0.277 | 100.000 |
| gnn_multiedge_season_level | post_covid | 19.697 | 185.819 | 13.253 | 0.622 | 67.391 |
| gnn_multiedge_level | post_covid | 20.037 | 192.862 | 13.203 | 0.521 | 69.565 |

### Flu season (Oct–Mar), 24 weeks scored, mean 17.1

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 7.630 | 68.141 | 5.848 | 0.900 | 100.000 |
| lstm | post_covid | 8.067 | 66.821 | 6.002 | 0.897 | 100.000 |
| arima | exclude_covid | 10.013 | 81.598 | 6.905 | 0.800 | 91.667 |
| dualtopo_fullhistory | full | 10.248 | 79.888 | 7.274 | 0.796 | 91.667 |
| gnn_multiedge_covid_rsv_full | full | 10.369 | 75.130 | 7.446 | 0.802 | 91.667 |
| gnn_multiedge_covid_rsv | post_covid | 10.495 | 94.890 | 8.427 | 0.818 | 100.000 |
| arima | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| persistence | exclude_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| persistence | post_covid | 10.581 | 64.754 | 7.429 | 0.801 | 95.833 |
| gnn_multiedge | post_covid | 11.713 | 99.235 | 9.599 | 0.822 | 95.833 |
| gnn_uniform | post_covid | 13.328 | 93.844 | 10.471 | 0.825 | 100.000 |
| gnn_multiedge_season | post_covid | 14.089 | 123.670 | 11.870 | 0.807 | 100.000 |
| gnn_corrbinary | post_covid | 14.943 | 123.069 | 12.317 | 0.798 | 100.000 |
| gnn_multiedge_rt | post_covid | 15.287 | 123.851 | 12.222 | 0.771 | 95.833 |
| gnn_geo | post_covid | 15.484 | 132.974 | 12.921 | 0.773 | 87.500 |
| gnn_multiedge_full | full | 15.864 | 131.222 | 12.915 | 0.688 | 87.500 |
| dualtopo_no_bg | post_covid | 17.099 | 139.259 | 11.222 | 0.135 | 83.333 |
| dualtopo | post_covid | 17.112 | 138.472 | 11.207 | 0.168 | 83.333 |
| gnn_multiedge_leaknorm | post_covid | 17.777 | 125.425 | 13.693 | 0.792 | 95.833 |
| gnn_multiedge_level | post_covid | 21.393 | 203.344 | 16.142 | 0.467 | 62.500 |
| gnn_multiedge_season_level | post_covid | 21.932 | 206.342 | 17.023 | 0.584 | 58.333 |
| seasonal_naive | exclude_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |
| seasonal_naive | post_covid | 24.059 | 195.604 | 17.679 | 0.033 | 100.000 |

### Off-season (Apr–Sep), 22 weeks scored, mean 4.2

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.482 | 69.702 | 1.859 | 0.598 | 100.000 |
| lstm | post_covid | 2.684 | 84.229 | 2.074 | 0.656 | 100.000 |
| arima | post_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| persistence | exclude_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| persistence | post_covid | 2.736 | 52.424 | 1.932 | 0.554 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.113 | 57.075 | 2.225 | 0.660 | 100.000 |
| arima | exclude_covid | 3.317 | 100.905 | 2.761 | 0.523 | 100.000 |
| seasonal_naive | exclude_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| seasonal_naive | post_covid | 3.533 | 92.576 | 3.014 | 0.079 | 100.000 |
| dualtopo_fullhistory | full | 3.857 | 137.295 | 3.177 | 0.549 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.682 | 98.401 | 3.888 | 0.671 | 100.000 |
| dualtopo | post_covid | 8.855 | 322.510 | 8.514 | 0.704 | 100.000 |
| gnn_multiedge | post_covid | 8.913 | 101.972 | 5.250 | 0.712 | 100.000 |
| gnn_multiedge_season | post_covid | 9.022 | 106.330 | 5.384 | 0.711 | 100.000 |
| dualtopo_no_bg | post_covid | 9.044 | 329.463 | 8.694 | 0.663 | 100.000 |
| gnn_uniform | post_covid | 10.024 | 111.177 | 5.823 | 0.712 | 100.000 |
| gnn_corrbinary | post_covid | 10.660 | 115.139 | 6.139 | 0.720 | 100.000 |
| gnn_multiedge_rt | post_covid | 10.880 | 115.247 | 6.256 | 0.731 | 100.000 |
| gnn_multiedge_full | full | 11.051 | 119.290 | 6.349 | 0.729 | 100.000 |
| gnn_geo | post_covid | 12.438 | 128.197 | 7.047 | 0.727 | 86.364 |
| gnn_multiedge_leaknorm | post_covid | 14.405 | 141.443 | 8.018 | 0.728 | 86.364 |
| gnn_multiedge_season_level | post_covid | 16.924 | 163.431 | 9.141 | 0.750 | 77.273 |
| gnn_multiedge_level | post_covid | 18.445 | 181.426 | 9.996 | 0.749 | 77.273 |

## Fenway

*mean observed 6.9, peak 21.1 per 100,000 over the full year*

### Overall (full year), 43 weeks scored, mean 6.9

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | post_covid | 3.752 | 76.593 | 2.588 | 0.725 | 97.674 |
| arima | exclude_covid | 3.902 | 92.755 | 2.835 | 0.714 | 100.000 |
| arima | post_covid | 3.922 | 96.417 | 2.890 | 0.712 | 100.000 |
| persistence | exclude_covid | 4.043 | 71.866 | 2.774 | 0.721 | 100.000 |
| persistence | post_covid | 4.043 | 71.866 | 2.774 | 0.721 | 100.000 |
| lstm | exclude_covid | 4.250 | 66.349 | 2.797 | 0.716 | 97.674 |
| gnn_multiedge_covid_rsv_full | full | 4.820 | 91.074 | 3.636 | 0.688 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.332 | 113.363 | 4.140 | 0.705 | 100.000 |
| dualtopo_fullhistory | full | 5.348 | 88.238 | 3.318 | 0.571 | 97.674 |
| dualtopo | post_covid | 5.688 | 173.613 | 4.885 | 0.584 | 100.000 |
| dualtopo_no_bg | post_covid | 5.709 | 174.761 | 4.899 | 0.561 | 100.000 |
| gnn_multiedge | post_covid | 7.368 | 143.623 | 5.617 | 0.646 | 100.000 |
| gnn_uniform | post_covid | 7.876 | 152.178 | 5.913 | 0.618 | 100.000 |
| gnn_multiedge_season | post_covid | 8.229 | 150.287 | 6.213 | 0.672 | 100.000 |
| gnn_corrbinary | post_covid | 8.940 | 164.272 | 6.726 | 0.665 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.947 | 163.991 | 6.629 | 0.640 | 100.000 |
| gnn_multiedge_full | full | 9.397 | 176.802 | 6.892 | 0.589 | 100.000 |
| gnn_geo | post_covid | 9.642 | 178.752 | 7.061 | 0.637 | 97.674 |
| seasonal_naive | exclude_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| seasonal_naive | post_covid | 9.796 | 105.171 | 5.840 | 0.439 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 10.668 | 191.559 | 7.661 | 0.588 | 97.674 |
| gnn_multiedge_season_level | post_covid | 13.682 | 230.472 | 9.683 | 0.612 | 74.419 |
| gnn_multiedge_level | post_covid | 13.758 | 241.906 | 9.642 | 0.550 | 79.070 |

### Flu season (Oct–Mar), 25 weeks scored, mean 9.7

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| arima | post_covid | 4.276 | 43.921 | 3.031 | 0.627 | 100.000 |
| arima | exclude_covid | 4.310 | 43.269 | 3.041 | 0.627 | 100.000 |
| lstm | post_covid | 4.407 | 38.574 | 2.906 | 0.641 | 96.000 |
| persistence | exclude_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| persistence | post_covid | 4.783 | 43.024 | 3.276 | 0.625 | 100.000 |
| lstm | exclude_covid | 5.283 | 41.728 | 3.589 | 0.635 | 96.000 |
| dualtopo_no_bg | post_covid | 5.416 | 75.214 | 4.252 | 0.463 | 100.000 |
| dualtopo | post_covid | 5.424 | 75.296 | 4.265 | 0.499 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 5.514 | 56.319 | 4.500 | 0.587 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 5.743 | 59.542 | 4.677 | 0.643 | 100.000 |
| dualtopo_fullhistory | full | 6.572 | 47.268 | 3.942 | 0.487 | 96.000 |
| gnn_multiedge | post_covid | 7.691 | 75.511 | 6.326 | 0.614 | 100.000 |
| gnn_uniform | post_covid | 8.036 | 76.370 | 6.533 | 0.608 | 100.000 |
| gnn_multiedge_season | post_covid | 9.055 | 85.369 | 7.317 | 0.623 | 100.000 |
| gnn_multiedge_rt | post_covid | 9.431 | 85.926 | 7.541 | 0.618 | 100.000 |
| gnn_corrbinary | post_covid | 9.549 | 90.708 | 7.780 | 0.638 | 100.000 |
| gnn_multiedge_full | full | 9.715 | 92.369 | 7.718 | 0.563 | 100.000 |
| gnn_geo | post_covid | 9.875 | 91.961 | 7.860 | 0.631 | 100.000 |
| gnn_multiedge_leaknorm | post_covid | 11.042 | 99.300 | 8.552 | 0.574 | 100.000 |
| seasonal_naive | exclude_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| seasonal_naive | post_covid | 12.573 | 103.331 | 8.396 | 0.214 | 100.000 |
| gnn_multiedge_level | post_covid | 13.435 | 121.808 | 10.617 | 0.582 | 84.000 |
| gnn_multiedge_season_level | post_covid | 14.059 | 121.576 | 11.071 | 0.639 | 76.000 |

### Off-season (Apr–Sep), 18 weeks scored, mean 3.0

| model | variant | RMSE | MAPE | MAE | Corr | CI_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| lstm | exclude_covid | 2.094 | 100.545 | 1.698 | 0.479 | 100.000 |
| lstm | post_covid | 2.578 | 129.397 | 2.147 | 0.463 | 100.000 |
| persistence | exclude_covid | 2.696 | 111.923 | 2.078 | 0.193 | 100.000 |
| persistence | post_covid | 2.696 | 111.923 | 2.078 | 0.193 | 100.000 |
| dualtopo_fullhistory | full | 2.889 | 145.142 | 2.452 | 0.304 | 100.000 |
| seasonal_naive | exclude_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| seasonal_naive | post_covid | 3.111 | 107.726 | 2.289 | -0.060 | 100.000 |
| arima | exclude_covid | 3.250 | 161.485 | 2.549 | 0.169 | 100.000 |
| arima | post_covid | 3.371 | 169.327 | 2.695 | 0.165 | 100.000 |
| gnn_multiedge_covid_rsv_full | full | 3.644 | 139.344 | 2.436 | 0.144 | 100.000 |
| gnn_multiedge_covid_rsv | post_covid | 4.701 | 188.115 | 3.393 | 0.222 | 100.000 |
| dualtopo | post_covid | 6.036 | 310.165 | 5.745 | 0.316 | 100.000 |
| dualtopo_no_bg | post_covid | 6.092 | 313.020 | 5.798 | 0.297 | 100.000 |
| gnn_multiedge | post_covid | 6.894 | 238.222 | 4.632 | 0.231 | 100.000 |
| gnn_multiedge_season | post_covid | 6.919 | 240.450 | 4.681 | 0.239 | 100.000 |
| gnn_uniform | post_covid | 7.648 | 257.466 | 5.052 | 0.236 | 100.000 |
| gnn_corrbinary | post_covid | 8.018 | 266.445 | 5.262 | 0.234 | 100.000 |
| gnn_multiedge_rt | post_covid | 8.228 | 272.415 | 5.363 | 0.215 | 100.000 |
| gnn_multiedge_full | full | 8.936 | 294.070 | 5.745 | 0.197 | 100.000 |
| gnn_geo | post_covid | 9.310 | 299.296 | 5.952 | 0.229 | 94.444 |
| gnn_multiedge_leaknorm | post_covid | 10.126 | 319.697 | 6.423 | 0.229 | 94.444 |
| gnn_multiedge_season_level | post_covid | 13.140 | 381.717 | 7.756 | 0.215 | 72.222 |
| gnn_multiedge_level | post_covid | 14.193 | 408.709 | 8.289 | 0.220 | 72.222 |

## Comparability notes

- mixed target parameterisation in this table (delta: gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_leaknorm, gnn_multiedge_rt, gnn_multiedge_season, gnn_uniform; level: arima, dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_multiedge_level, gnn_multiedge_season_level, lstm, persistence, seasonal_naive). Differences here are not purely model quality.
- mixed normalisation reference in this table (all: gnn_multiedge_leaknorm; none: arima, persistence, seasonal_naive; train: dualtopo, dualtopo_fullhistory, dualtopo_no_bg, gnn_corrbinary, gnn_geo, gnn_multiedge, gnn_multiedge_covid_rsv, gnn_multiedge_covid_rsv_full, gnn_multiedge_full, gnn_multiedge_level, gnn_multiedge_rt, gnn_multiedge_season, gnn_multiedge_season_level, gnn_uniform, lstm). Differences here are not purely model quality.
