| Model | Hardware | h=1 time | h=1 energy | h=1 CO2 | h=2 time | h=2 energy | h=2 CO2 | h=4 time | h=4 energy | h=4 CO2 |
|---|---|---|---|---|---|---|---|---|---|---|
| gnn_st_tuned | Explorer (Xeon E5-2680 v4) | 1h 10m | 21.7 | 8.08 | 1h 16m | 23.6 | 8.77 | 1h 03m | 16.6 | 6.18 |
| gnn_st_noadapt | Explorer (Xeon E5-2680 v4) | 43m 01s | 13.1 | 4.88 | 39m 48s | 12.2 | 4.56 | 29m 38s | 7.78 | 2.9 |
| gnn_st | Explorer (Xeon E5-2680 v4) | 48m 54s | 14.9 | 5.56 | 42m 50s | 13.1 | 4.89 | 54m 37s | 16.7 | 6.22 |
| gnn_st_median_tuned | – | – | – | – | – | – | – | – | – | – |
| transfer_finetune_from_columbus | Explorer (Xeon E5-2680 v4) | 52m 43s | 16.2 | 6.02 | 47m 19s | 14.5 | 5.4 | 40m 18s | 12.4 | 4.61 |
| transfer_finetune_from_chicago | Explorer (Xeon Platinum 8276) | 39m 46s | 10.4 | 3.86 | 45m 02s | 13.7 | 5.12 | 46m 24s | 14.1 | 5.26 |
| gnn_st_geofixed | Explorer (Xeon E5-2680 v4) | 45m 09s | 13.9 | 5.17 | 42m 29s | 13 | 4.83 | 46m 23s | 14.1 | 5.26 |
| gnn_st_rt_tuned | – | – | – | – | – | – | – | – | – | – |
| colagnn_tuned | Explorer (Xeon E5-2680 v4) | 2m 34s | 0.671 | 0.25 | 1m 39s | 0.461 | 0.172 | 2m 07s | 0.621 | 0.231 |
| gnn_st_nograph | Explorer (Xeon Gold 6132) | 34m 52s | 11.5 | 4.28 | 36m 32s | 11.1 | 4.14 | 34m 05s | 10.4 | 3.87 |
| lstm_parity | Explorer (Xeon E5-2680 v4) | 32.9s | 0.136 | 0.0507 | 24.0s | 0.0922 | 0.0343 | 30.3s | 0.0895 | 0.0333 |
| gnn_st_nograph_tuned | Explorer (Xeon E5-2680 v4) | 1h 13m | 22.7 | 8.44 | 54m 37s | 16.8 | 6.25 | 54m 10s | 16.6 | 6.2 |
| xgboost | Explorer (Xeon E5-2680 v4) | 4.4s | 0.00201 | 0.000749 | 4.4s | 0.00175 | 0.000652 | 8.7s | 0.00226 | 0.000843 |
| lstm_tuned | Explorer (Xeon E5-2680 v4) | 38.1s | 0.0806 | 0.03 | 16.5s | 0.0565 | 0.021 | 25.7s | 0.0764 | 0.0285 |
| lstm | Explorer (Xeon E5-2680 v4) | 15.7s | 0.0229 | 0.00853 | 11.1s | 0.0192 | 0.00717 | 8.1s | 0.0101 | 0.00374 |
| xgboost_tuned | Explorer (Xeon E5-2680 v4) | 5.2s | 0.0119 | 0.00442 | 5.9s | 0.00769 | 0.00287 | 9.1s | 0.0192 | 0.00717 |
| lstm_s10 | Explorer (Xeon E5-2680 v4) | 20.0s | 0.0761 | 0.0284 | 25.7s | 0.0717 | 0.0267 | 15.3s | 0.0437 | 0.0163 |
| xgboost_parity | Explorer (Xeon E5-2680 v4) | 10.7s | 0.013 | 0.00483 | 10.9s | 0.0119 | 0.00444 | 7.2s | 0.0106 | 0.00396 |
| transfer_zeroshot_from_columbus | Explorer (Xeon E5-2680 v4) | 48.3s | 0.207 | 0.0772 | 2m 03s | 0.303 | 0.113 | 2m 03s | 0.305 | 0.114 |
| transfer_zeroshot_from_chicago | Explorer (Xeon E5-2680 v4) | 45.3s | 0.185 | 0.069 | 49.4s | 0.191 | 0.0713 | 49.4s | 0.19 | 0.071 |
| sarima | Explorer (Xeon E5-2680 v4) | 20m 09s | 6.18 | 2.3 | 21m 26s | 6.59 | 2.46 | 19m 44s | 6.08 | 2.26 |
| seasonal_naive | Explorer (Xeon Platinum 8276) | 1.8s | 0.00047 | 0.000175 | 2.5s | 0.00062 | 0.000231 | 1.8s | 0.000676 | 0.000252 |
| blend_baseline | Explorer (Xeon E5-2680 v4) | 1.9s | 0.000206 | 7.68e-05 | 2.5s | 0.000225 | 8.39e-05 | 2.0s | 0.000223 | 8.33e-05 |
| gat_parity | Explorer (Xeon E5-2680 v4) | 7m 55s | 2.36 | 0.878 | – | – | – | – | – | – |
| climatology | Explorer (Xeon E5-2680 v4) | 1.9s | 0.000206 | 7.68e-05 | 2.5s | 0.000225 | 8.39e-05 | 2.0s | 0.000223 | 8.33e-05 |
| gat_tuned | Explorer (Xeon E5-2680 v4) | 6m 49s | 2.06 | 0.766 | – | – | – | – | – | – |
| arima | Explorer (Xeon E5-2680 v4) | 17m 40s | 5.43 | 2.02 | 17m 31s | 5.38 | 2.01 | 18m 31s | 5.68 | 2.12 |
| persistence | Explorer (Xeon Platinum 8276) | 1.5s | 0.000426 | 0.000159 | 2.3s | 0.000693 | 0.000258 | 2.3s | 0.000668 | 0.000249 |
| flusight_baseline | Explorer (Xeon E5-2680 v4) | 2.1s | 0.000881 | 0.000328 | 2.1s | 0.000852 | 0.000317 | 2.1s | 0.000868 | 0.000323 |
| dualtopo_tuned | Explorer (Xeon E5-2680 v4) | 31m 25s | 9.66 | 3.6 | – | – | – | – | – | – |
