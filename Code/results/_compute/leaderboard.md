#### Horizon 1 week ahead

| Model | How close to the truth, vs persistence (rel. WIS-95; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| gnn_st_noglobals | 0.75 | 23m 58s | 1.16s | 7.27 Wh | 2.71 g | 0.0938 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st | 0.75 | 22m 54s | 1.08s | 6.87 Wh | 2.56 g | 0.0987 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_lagsonly | 0.77 | 23m 36s | 1.12s | 7.08 Wh | 2.64 g | 0.0883 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm | 0.93 | 23.2s | 0.11s | 48.9 mWh | 18.2 mg | 4.11 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| persistence | 1.00 | 34 ms | – | 0.450 mWh | 0.166 mg | reference | yes | Apple M5 | this run |
| xgboost | 1.01 | 1.8s | 0.14s | 2.27 mWh | 0.847 mg | no skill |  | Apple M5 | measurement pass (current code) |
| arima | 1.02 | 3m 41s | – | 2.98 Wh | 1.10 g | no skill |  | Apple M5 | this run |
| gat | 1.64 | – | – | – | – | no skill |  | – | not measured |
| seasonal_naive | 2.10 | 41 ms | – | 0.544 mWh | 0.201 mg | reference |  | Apple M5 | this run |
| dualtopo | 2.32 | – | – | – | – | no skill |  | – | not measured |

#### Horizon 2 weeks ahead

| Model | How close to the truth, vs persistence (rel. WIS-95; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| gnn_st_lagsonly | 0.71 | 24m 26s | 1.15s | 7.26 Wh | 2.71 g | 0.108 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_noglobals | 0.71 | 25m 56s | 1.24s | 7.80 Wh | 2.91 g | 0.0981 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st | 0.72 | 22m 00s | 1.07s | 6.74 Wh | 2.51 g | 0.114 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_cascade | 0.72 | 15m 21s | 0.74s | 3.99 Wh | 1.49 g | 0.19 | yes | Explorer (Xeon Platinum 8276) | measurement pass (current code) |
| xgboost | 0.88 | 1.5s | 0.15s | 2.37 mWh | 0.884 mg | 141 | yes | Apple M5 | measurement pass (current code) |
| lstm | 0.95 | 40.7s | 0.18s | 49.9 mWh | 18.6 mg | 2.83 |  | Explorer (EPYC 7702) | measurement pass (current code) |
| arima | 0.97 | 3m 41s | – | 2.98 Wh | 1.10 g | 0.0239 |  | Apple M5 | this run |
| persistence | 1.00 | 35 ms | – | 0.474 mWh | 0.175 mg | reference | yes | Apple M5 | this run |
| gat | 1.42 | – | – | – | – | no skill |  | – | not measured |
| seasonal_naive | 1.47 | 40 ms | – | 0.534 mWh | 0.197 mg | reference |  | Apple M5 | this run |
| dualtopo | 1.61 | – | – | – | – | no skill |  | – | not measured |

#### Horizon 4 weeks ahead

| Model | How close to the truth, vs persistence (rel. WIS-95; <1 better) | Time per run | Time per epoch | Energy | CO2 | Skill per gram | On frontier | Hardware | Energy from |
|---|---|---|---|---|---|---|---|---|---|
| gnn_st | 0.68 | 19m 18s | 0.94s | 5.91 Wh | 2.20 g | 0.147 | yes | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| gnn_st_noglobals | 0.68 | 23m 09s | 1.11s | 7.00 Wh | 2.61 g | 0.124 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| xgboost | 0.69 | 1.7s | 0.34s | 5.08 mWh | 1.89 mg | 164 | yes | Apple M5 | measurement pass (current code) |
| gnn_st_lagsonly | 0.69 | 20m 37s | 0.95s | 6.08 Wh | 2.27 g | 0.135 |  | Explorer (Xeon E5-2680 v4) | measurement pass (current code) |
| lstm | 0.85 | 18.1s | 0.10s | 24.5 mWh | 9.14 mg | 16.8 |  | Explorer (EPYC 7702) | measurement pass (current code) |
| arima | 0.94 | 3m 38s | – | 2.94 Wh | 1.09 g | 0.0543 |  | Apple M5 | this run |
| persistence | 1.00 | 33 ms | – | 0.439 mWh | 0.162 mg | reference | yes | Apple M5 | this run |
| seasonal_naive | 1.03 | 41 ms | – | 0.552 mWh | 0.204 mg | reference |  | Apple M5 | this run |
| gat | 1.13 | – | – | – | – | no skill |  | – | not measured |
| dualtopo | 1.15 | – | – | – | – | no skill |  | – | not measured |
