#### Horizon 1 week ahead

| Model | How close to the truth, vs persistence (rel. WIS; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| transfer_finetune_from_columbus | 0.75 | 52m 43s | 2.58s | 16.2 Wh | 6.02 g | 0.0413 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st | 0.76 | 48m 54s | 2.39s | 14.9 Wh | 5.56 g | 0.044 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_finetune_from_chicago | 0.77 | 39m 46s | 1.93s | 10.4 Wh | 3.86 g | 0.0607 | yes | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| gnn_st_noadapt | 0.77 | 43m 01s | 2.09s | 13.1 Wh | 4.88 g | 0.0479 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_geofixed | 0.78 | 45m 09s | 2.22s | 13.9 Wh | 5.17 g | 0.0429 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gat_parity | 0.78 | 7m 55s | 0.89s | 2.36 Wh | 878 mg | 0.246 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gat_tuned | 0.79 | 6m 49s | 0.82s | 2.06 Wh | 766 mg | 0.276 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_rt_tuned | 0.81 | – | – | – | – | – |  | – | not measured |
| gnn_st_tuned | 0.81 | 1h 10m | 2.09s | 21.7 Wh | 8.08 g | 0.0237 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_chicago | 0.81 | 45.3s | – | 185 mWh | 69.0 mg | 2.76 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_tuned | 0.82 | 38.1s | 0.06s | 80.6 mWh | 30.0 mg | 6.07 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| colagnn_tuned | 0.82 | 2m 34s | 0.21s | 671 mWh | 250 mg | 0.707 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_median_tuned | 0.83 | – | – | – | – | – |  | – | not measured |
| lstm_s10 | 0.83 | 20.0s | 0.04s | 76.1 mWh | 28.4 mg | 6.05 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_columbus | 0.83 | 48.3s | – | 207 mWh | 77.2 mg | 2.21 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm | 0.84 | 15.7s | 0.15s | 22.9 mWh | 8.53 mg | 18.4 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost_parity | 0.87 | 10.7s | 0.25s | 13.0 mWh | 4.83 mg | 26.8 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_parity | 0.87 | 32.9s | 0.05s | 136 mWh | 50.7 mg | 2.47 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_nograph | 0.88 | 34m 52s | 1.71s | 11.5 Wh | 4.28 g | 0.029 |  | Explorer (Xeon Gold 6132) | measurement pass (current code) |
| gnn_st_nograph_tuned | 0.91 | 1h 13m | 2.19s | 22.7 Wh | 8.44 g | 0.0106 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| blend_baseline | 0.94 | 1.9s | – | 0.206 mWh | 0.0768 mg | 796 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| arima | 1.00 | 17m 40s | – | 5.43 Wh | 2.02 g | 0.00223 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| persistence | 1.00 | 1.5s | – | 0.426 mWh | 0.159 mg | reference |  | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| dualtopo_tuned | 1.01 | 31m 25s | 4.95s | 9.66 Wh | 3.60 g | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost_tuned | 1.05 | 5.2s | 0.22s | 11.9 mWh | 4.42 mg | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| flusight_baseline | 1.05 | 2.1s | – | 0.881 mWh | 0.328 mg | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost | 1.07 | 4.4s | 0.30s | 2.01 mWh | 0.749 mg | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| sarima | 1.23 | 20m 09s | – | 6.18 Wh | 2.30 g | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| seasonal_naive | 1.67 | 1.8s | – | 0.470 mWh | 0.175 mg | reference |  | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| climatology | 1.74 | 1.9s | – | 0.206 mWh | 0.0768 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |

#### Horizon 2 weeks ahead

| Model | How close to the truth, vs persistence (rel. WIS; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| transfer_finetune_from_chicago | 0.68 | 45m 02s | 2.19s | 13.7 Wh | 5.12 g | 0.0618 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_noadapt | 0.69 | 39m 48s | 1.96s | 12.2 Wh | 4.56 g | 0.0687 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st | 0.69 | 42m 50s | 2.10s | 13.1 Wh | 4.89 g | 0.0637 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_finetune_from_columbus | 0.70 | 47m 19s | 2.32s | 14.5 Wh | 5.40 g | 0.0553 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_median_tuned | 0.71 | – | – | – | – | – |  | – | not measured |
| gnn_st_geofixed | 0.71 | 42m 29s | 2.08s | 13.0 Wh | 4.83 g | 0.059 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_rt_tuned | 0.73 | – | – | – | – | – |  | – | not measured |
| gnn_st_tuned | 0.74 | 1h 16m | 2.27s | 23.6 Wh | 8.77 g | 0.0294 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_chicago | 0.77 | 49.4s | – | 191 mWh | 71.3 mg | 3.26 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_nograph | 0.77 | 36m 32s | 1.77s | 11.1 Wh | 4.14 g | 0.055 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_nograph_tuned | 0.78 | 54m 37s | 1.62s | 16.8 Wh | 6.25 g | 0.0358 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_tuned | 0.78 | 16.5s | 0.04s | 56.5 mWh | 21.0 mg | 10.5 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost_parity | 0.78 | 10.9s | 0.23s | 11.9 mWh | 4.44 mg | 48.8 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_parity | 0.79 | 24.0s | 0.05s | 92.2 mWh | 34.3 mg | 6.05 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_columbus | 0.79 | 2m 03s | – | 303 mWh | 113 mg | 1.82 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| colagnn_tuned | 0.80 | 1m 39s | 0.19s | 461 mWh | 172 mg | 1.15 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_s10 | 0.84 | 25.7s | 0.05s | 71.7 mWh | 26.7 mg | 5.8 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm | 0.86 | 11.1s | 0.13s | 19.2 mWh | 7.17 mg | 19.3 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| blend_baseline | 0.88 | 2.5s | – | 0.225 mWh | 0.0839 mg | 1.47e+03 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost | 0.89 | 4.4s | 0.31s | 1.75 mWh | 0.652 mg | 167 |  | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| xgboost_tuned | 0.92 | 5.9s | 0.14s | 7.69 mWh | 2.87 mg | 26.5 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| arima | 0.98 | 17m 31s | – | 5.38 Wh | 2.01 g | 0.012 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| persistence | 1.00 | 2.3s | – | 0.693 mWh | 0.258 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| sarima | 1.03 | 21m 26s | – | 6.59 Wh | 2.46 g | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| flusight_baseline | 1.05 | 2.1s | – | 0.852 mWh | 0.317 mg | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| seasonal_naive | 1.19 | 2.5s | – | 0.620 mWh | 0.231 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| climatology | 1.24 | 2.5s | – | 0.225 mWh | 0.0839 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |

#### Horizon 4 weeks ahead

| Model | How close to the truth, vs persistence (rel. WIS; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| gnn_st_tuned | 0.58 | 1h 03m | 1.87s | 16.6 Wh | 6.18 g | 0.0677 | yes | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| gnn_st_noadapt | 0.59 | 29m 38s | 1.45s | 7.78 Wh | 2.90 g | 0.143 | yes | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| gnn_st | 0.59 | 54m 37s | 2.67s | 16.7 Wh | 6.22 g | 0.0659 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_median_tuned | 0.59 | – | – | – | – | – |  | – | not measured |
| transfer_finetune_from_columbus | 0.60 | 40m 18s | 1.98s | 12.4 Wh | 4.61 g | 0.0878 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_finetune_from_chicago | 0.60 | 46m 24s | 2.25s | 14.1 Wh | 5.26 g | 0.0766 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_geofixed | 0.60 | 46m 23s | 2.25s | 14.1 Wh | 5.26 g | 0.0757 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_rt_tuned | 0.60 | – | – | – | – | – |  | – | not measured |
| colagnn_tuned | 0.63 | 2m 07s | 0.20s | 621 mWh | 231 mg | 1.58 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_nograph | 0.64 | 34m 05s | 1.65s | 10.4 Wh | 3.87 g | 0.0925 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_parity | 0.65 | 30.3s | 0.05s | 89.5 mWh | 33.3 mg | 10.5 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_nograph_tuned | 0.65 | 54m 10s | 1.60s | 16.6 Wh | 6.20 g | 0.0558 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost | 0.66 | 8.7s | 0.45s | 2.26 mWh | 0.843 mg | 403 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_tuned | 0.66 | 25.7s | 0.06s | 76.4 mWh | 28.5 mg | 11.8 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm | 0.67 | 8.1s | 0.08s | 10.1 mWh | 3.74 mg | 88.2 |  | Explorer (EPYC 7702) | measurement pass (current code) |
| xgboost_tuned | 0.67 | 9.1s | 0.32s | 19.2 mWh | 7.17 mg | 45.4 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm_s10 | 0.68 | 15.3s | 0.03s | 43.7 mWh | 16.3 mg | 19.9 |  | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| xgboost_parity | 0.69 | 7.2s | 0.20s | 10.6 mWh | 3.96 mg | 77.8 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_columbus | 0.72 | 2m 03s | – | 305 mWh | 114 mg | 2.5 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| transfer_zeroshot_from_chicago | 0.74 | 49.4s | – | 190 mWh | 71.0 mg | 3.71 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| sarima | 0.75 | 19m 44s | – | 6.08 Wh | 2.26 g | 0.109 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| seasonal_naive | 0.75 | 1.8s | – | 0.676 mWh | 0.252 mg | reference | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| blend_baseline | 0.78 | 2.0s | – | 0.223 mWh | 0.0833 mg | 2.65e+03 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| climatology | 0.79 | 2.0s | – | 0.223 mWh | 0.0833 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| arima | 0.91 | 18m 31s | – | 5.68 Wh | 2.12 g | 0.0446 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| persistence | 1.00 | 2.3s | – | 0.668 mWh | 0.249 mg | reference |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| flusight_baseline | 1.01 | 2.1s | – | 0.868 mWh | 0.323 mg | no skill |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
