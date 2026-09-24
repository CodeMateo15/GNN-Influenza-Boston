# Boston vs Columbus — do the models transfer?

Horizon 1, variant `post_covid`, the **49 target weeks common to both cities** (2025-06-01 → 2026-05-03), all nodes pooled.

`xcity_*` arms use only features BOTH cities can supply — flu lags, weather,
static demographics and `ili_count`. Boston's published `gnn_*` arms also use
four more city-wide covariates that Columbus has no equivalent for; comparing
those directly would attribute a feature-set difference to the city.

**Skill** is RMSE ÷ persistence's RMSE in the same city. Below 1.00 beats
"next week equals this week". Raw RMSE is not comparable across the cities
(Columbus's mean rate is 17.9 per 100,000 against Boston's 25.1); skill is.

| model | Boston RMSE | Boston skill | Columbus RMSE | Columbus skill |
| --- | --- | --- | --- | --- |
| `lstm` | 14.66 | 0.927 | 8.87 | 0.946 |
| `arima` | 15.51 | 0.981 | 9.68 | 1.031 |
| `persistence` | 15.81 | 1.000 | 9.38 | 1.000 |
| `xcity_corrbinary` | 16.92 | 1.070 | 9.43 | 1.005 |
| `xcity_geo` | 17.66 | 1.117 | 9.48 | 1.011 |
| `xcity_uniform` | 20.37 | 1.289 | 9.18 | 0.979 |
| `xcity_multiedge` | 20.89 | 1.322 | 9.74 | 1.038 |
| `xcity_dualtopo` | 28.91 | 1.829 | 14.79 | 1.577 |
| `seasonal_naive` | 39.84 | 2.520 | 16.89 | 1.800 |

Cells scored: Boston 627 (14 neighborhoods, suppressed weeks dropped), Columbus 833 (17 areas, no suppression).
The counts differ because Boston suppresses small counts and Columbus does not,
which is also why MAPE is not comparable across the two.
