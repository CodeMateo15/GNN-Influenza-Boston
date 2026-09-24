# Forecast timing at 4 weeks ahead

`variant=post_covid`, 627 neighborhood-weeks scored. A week counts as rising or falling when the truth moved more than 5 per 100,000.

## Is the curve in the right place on the calendar?

- **weeks late** — slide the forecast this many weeks earlier and it fits
  the truth best. 0 is on time.
- **share of error that is timing** — how much of the squared error goes away
  under that shift. High means the shape and height are right and only the
  placement is wrong.
- **miss vs. slope** — correlation between the miss and how fast the truth was
  moving. Near −1 is a pure phase shift; near 0 means the misses have nothing
  to do with timing.
- **typical weekly miss** — RMSE over the whole test window, in cases per
  100,000; the same number metrics.csv reports.
- **...on the compared weeks / ...once shifted earlier** — RMSE before and after
  the shift, both over the weeks every lead up to 4 can score, so the
  shift gets no credit for running off the end of the window.
- **in step with truth** — mean of the 14 per-neighborhood correlations.

Scopes follow the leaderboard convention in `compare_models.py`: RMSE is pooled
over all neighborhood-weeks, correlation is the unweighted mean of the 14. Both
reproduce `metrics.csv` exactly at lead 0, which is the check that this script
is reading the same predictions the leaderboard is.

| model | weeks late | share of error that is timing | miss vs. slope | typical weekly miss | ...on the compared weeks | ...once shifted earlier | in step with truth | peak weeks late |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st_slopeweight | 2 | 0.556 | -0.594 | 23.428 | 24.280 | 16.175 | 0.600 | 3.000 |
| gnn_st_trendblend | 3 | 0.531 | -0.552 | 23.009 | 23.838 | 16.322 | 0.583 | 3.000 |
| gnn_st | 3 | 0.574 | -0.570 | 23.070 | 23.906 | 15.598 | 0.582 | 3.000 |
| gnn_st_twosided | 3 | 0.574 | -0.570 | 23.070 | 23.906 | 15.598 | 0.582 | 3.000 |

> Sliding a forecast one week earlier is the same thing as relabelling an
> h=4 forecast as h=3: it buys the accuracy with a week of
> lead time. These columns measure what the lateness costs and bound what any
> phase correction could recover. They are not a result.

## Does the 95% band cover the weeks when the curve is climbing?

Every column should read 95%. A model at 95% overall but well below it on
rising weeks has a band that is not too narrow but pointed at the wrong weeks —
its width is a function of the predicted level, so a late centre drags a late
band with it. Width is in cases per 100,000, so it is the cost of any fix.

| model | all weeks | rising | flat | falling | mean band width |
| --- | --- | --- | --- | --- | --- |
| gnn_st_slopeweight | 95.694 | 88.591 | 99.240 | 94.839 | 48.695 |
| gnn_st_trendblend | 96.970 | 90.604 | 99.620 | 97.419 | 56.885 |
| gnn_st | 96.970 | 90.604 | 99.620 | 97.419 | 57.523 |
| gnn_st_twosided | 93.461 | 89.933 | 98.099 | 86.452 | 51.120 |

## Which way does the model miss when the curve is moving?

Mean over-prediction, in cases per 100,000; negative is under-prediction. A
late forecast is low on the way up and high on the way down by roughly the
same amount, which is how its annual bias can sit near zero while almost
every individual week is wrong.

| model | rising weeks | flat weeks | falling weeks |
| --- | --- | --- | --- |
| gnn_st_slopeweight | -11.334 | 4.308 | 10.115 |
| gnn_st_trendblend | -11.914 | 3.986 | 7.858 |
| gnn_st | -12.933 | 3.355 | 7.658 |
| gnn_st_twosided | -12.933 | 3.355 | 7.658 |

## Peak week, busiest neighborhoods first

Positive is late. `compare_severity.py` reports the threshold-crossing
version of this (`peak_week_error_weeks`); this one needs no fitted
threshold.

| model | neighborhood | peak_week_actual | peak_week_pred | peak_weeks_late | peak_actual | peak_pred |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_twosided | Dorchester | 2025-12-21 | 2026-01-11 | 3.000 | 256.150 | 195.675 |
| gnn_st_trendblend | Dorchester | 2025-12-21 | 2026-01-11 | 3.000 | 256.150 | 187.007 |
| gnn_st | Dorchester | 2025-12-21 | 2026-01-11 | 3.000 | 256.150 | 195.675 |
| gnn_st_slopeweight | Dorchester | 2025-12-21 | 2026-01-11 | 3.000 | 256.150 | 212.212 |
| gnn_st_slopeweight | Roxbury | 2025-12-21 | 2026-01-11 | 3.000 | 254.700 | 180.591 |
| gnn_st_twosided | Roxbury | 2025-12-21 | 2026-01-11 | 3.000 | 254.700 | 165.781 |
| gnn_st_trendblend | Roxbury | 2025-12-21 | 2026-01-11 | 3.000 | 254.700 | 159.189 |
| gnn_st | Roxbury | 2025-12-21 | 2026-01-11 | 3.000 | 254.700 | 165.781 |
| gnn_st_slopeweight | Roslindale | 2025-12-28 | 2026-01-11 | 2.000 | 170.100 | 102.162 |
| gnn_st_twosided | Roslindale | 2025-12-28 | 2026-01-11 | 2.000 | 170.100 | 92.632 |
| gnn_st | Roslindale | 2025-12-28 | 2026-01-11 | 2.000 | 170.100 | 92.632 |
| gnn_st_trendblend | Roslindale | 2025-12-28 | 2026-01-18 | 3.000 | 170.100 | 90.224 |
| gnn_st_slopeweight | South End | 2025-12-14 | 2026-01-11 | 4.000 | 132.300 | 116.561 |
| gnn_st | South End | 2025-12-14 | 2026-01-11 | 4.000 | 132.300 | 116.385 |
