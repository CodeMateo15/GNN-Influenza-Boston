# Backtest: boston

Seasons: 2023-24, 2024-25, 2025-26. Every number is from weeks the models never trained on.

**Relative WIS** is the model's weighted interval score divided by persistence's on the same weeks: below 1 means it beat "next week looks like this week". **p (Holm)** asks whether the weekly gap is bigger than week-to-week noise, adjusted for the number of comparisons.

| weeks ahead | model | WIS | relative WIS | p (Holm) | verdict |
|---|---|---|---|---|---|
| 1 | gnn_st | 4.60 | 0.77 | 0.000 | better than persistence |
| 1 | lstm | 4.89 | 0.82 | 0.000 | better than persistence |
| 1 | colagnn | 4.90 | 0.82 | 0.000 | better than persistence |
| 1 | arima | 6.10 | 1.02 | 1.000 | no better than persistence |
| 1 | seasonal_naive | 12.52 | 2.09 | 0.000 | worse than persistence |
| 2 | gnn_st | 5.74 | 0.73 | 0.000 | better than persistence |
| 2 | lstm | 6.57 | 0.84 | 0.032 | better than persistence |
| 2 | arima | 7.21 | 0.92 | 0.977 | not clearly better than persistence |
| 2 | colagnn | 7.26 | 0.92 | 1.000 | not clearly better than persistence |
| 2 | seasonal_naive | 12.52 | 1.59 | 0.013 | worse than persistence |
| 3 | gnn_st | 7.04 | 0.73 | 0.004 | better than persistence |
| 3 | lstm | 7.71 | 0.80 | 0.069 | not clearly better than persistence |
| 3 | arima | 7.84 | 0.81 | 0.191 | not clearly better than persistence |
| 3 | colagnn | 8.89 | 0.92 | 1.000 | not clearly better than persistence |
| 3 | seasonal_naive | 12.52 | 1.30 | 0.559 | no better than persistence |
| 4 | gnn_st | 7.56 | 0.67 | 0.013 | better than persistence |
| 4 | arima | 8.23 | 0.73 | 0.082 | not clearly better than persistence |
| 4 | lstm | 8.31 | 0.74 | 0.069 | not clearly better than persistence |
| 4 | colagnn | 9.44 | 0.84 | 0.648 | not clearly better than persistence |
| 4 | seasonal_naive | 12.52 | 1.12 | 1.000 | no better than persistence |

**Timing.** Is the forecast late? *Weeks behind the curve* is how far the forecast would have to be slid earlier to fit best; persistence is exactly h weeks behind by construction. See areafluforecast.timing for why every model here tends to run late.

- arima, 1 wk ahead: 1 week(s) behind the curve (no earlier than persistence); 65% of its squared error is timing; peaks a median 1 week(s) late
- colagnn, 1 wk ahead: 1 week(s) behind the curve (no earlier than persistence); 49% of its squared error is timing; peaks a median 1 week(s) late
- gnn_st, 1 wk ahead: 1 week(s) behind the curve (no earlier than persistence); 60% of its squared error is timing; peaks a median 1 week(s) late
- lstm, 1 wk ahead: 1 week(s) behind the curve (no earlier than persistence); 31% of its squared error is timing; peaks a median 1 week(s) late
- persistence, 1 wk ahead: 1 week(s) behind the curve (exactly 1 by construction)
- seasonal_naive, 1 wk ahead: does not follow the recent curve (it copies an earlier season), so 'weeks behind' does not apply; its peak is a median -4 week(s) off
- arima, 2 wk ahead: 2 week(s) behind the curve (no earlier than persistence); 60% of its squared error is timing; peaks a median 2 week(s) late
- colagnn, 2 wk ahead: 2 week(s) behind the curve (no earlier than persistence); 45% of its squared error is timing; peaks a median 2 week(s) late
- gnn_st, 2 wk ahead: 2 week(s) behind the curve (no earlier than persistence); 57% of its squared error is timing; peaks a median 2 week(s) late
- lstm, 2 wk ahead: 2 week(s) behind the curve (no earlier than persistence); 47% of its squared error is timing; peaks a median 2 week(s) late
- persistence, 2 wk ahead: 2 week(s) behind the curve (exactly 2 by construction)
- seasonal_naive, 2 wk ahead: does not follow the recent curve (it copies an earlier season), so 'weeks behind' does not apply; its peak is a median -4 week(s) off
- arima, 3 wk ahead: 3 week(s) behind the curve (no earlier than persistence); 42% of its squared error is timing; peaks a median 3 week(s) late
- colagnn, 3 wk ahead: 3 week(s) behind the curve (no earlier than persistence); 40% of its squared error is timing; peaks a median 3 week(s) late
- gnn_st, 3 wk ahead: 3 week(s) behind the curve (no earlier than persistence); 53% of its squared error is timing; peaks a median 3 week(s) late
- lstm, 3 wk ahead: 3 week(s) behind the curve (no earlier than persistence); 46% of its squared error is timing; peaks a median 3 week(s) late
- persistence, 3 wk ahead: 3 week(s) behind the curve (exactly 3 by construction)
- seasonal_naive, 3 wk ahead: does not follow the recent curve (it copies an earlier season), so 'weeks behind' does not apply; its peak is a median -4 week(s) off
- arima, 4 wk ahead: 3 week(s) behind the curve (recovers 1 of the 4 week(s) persistence loses); 25% of its squared error is timing; peaks a median 4 week(s) late
- colagnn, 4 wk ahead: 3 week(s) behind the curve (recovers 1 of the 4 week(s) persistence loses); 40% of its squared error is timing; peaks a median 4 week(s) late
- gnn_st, 4 wk ahead: 3 week(s) behind the curve (recovers 1 of the 4 week(s) persistence loses); 40% of its squared error is timing; peaks a median 4 week(s) late
- lstm, 4 wk ahead: 3 week(s) behind the curve (recovers 1 of the 4 week(s) persistence loses); 44% of its squared error is timing; peaks a median 3 week(s) late
- persistence, 4 wk ahead: 4 week(s) behind the curve (exactly 4 by construction)
- seasonal_naive, 4 wk ahead: does not follow the recent curve (it copies an earlier season), so 'weeks behind' does not apply; its peak is a median -4 week(s) off

Coverage of the 95% band (should be near 95%):

- arima, 1 wk: 93.9%
- colagnn, 1 wk: 95.0%
- gnn_st, 1 wk: 95.4%
- lstm, 1 wk: 95.3%
- persistence, 1 wk: 94.9%
- seasonal_naive, 1 wk: 95.6%
- arima, 2 wk: 94.2%
- colagnn, 2 wk: 91.5%
- gnn_st, 2 wk: 93.9%
- lstm, 2 wk: 93.2%
- persistence, 2 wk: 93.3%
- seasonal_naive, 2 wk: 95.6%
- arima, 3 wk: 93.7%
- colagnn, 3 wk: 88.8%
- gnn_st, 3 wk: 92.8%
- lstm, 3 wk: 92.3%
- persistence, 3 wk: 91.9%
- seasonal_naive, 3 wk: 95.6%
- arima, 4 wk: 94.0%
- colagnn, 4 wk: 90.3%
- gnn_st, 4 wk: 93.1%
- lstm, 4 wk: 92.9%
- persistence, 4 wk: 92.6%
- seasonal_naive, 4 wk: 95.6%
