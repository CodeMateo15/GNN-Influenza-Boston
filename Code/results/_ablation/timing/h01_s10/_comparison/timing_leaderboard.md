# Forecast timing at 1 week ahead

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
| gnn_st | 1 | 0.611 | -0.903 | 11.711 | 12.072 | 7.527 | 0.893 | 1.000 |
| gnn_st_twosided | 1 | 0.611 | -0.903 | 11.711 | 12.072 | 7.527 | 0.893 | 1.000 |
| gnn_st_trendblend | 1 | 0.626 | -0.906 | 11.824 | 12.195 | 7.461 | 0.892 | 1.000 |
| gnn_st_slopeweight | 1 | 0.550 | -0.867 | 12.221 | 12.591 | 8.450 | 0.898 | 1.000 |

> Sliding a forecast one week earlier is the same thing as relabelling an
> h=1 forecast as h=0: it buys the accuracy with a week of
> lead time. These columns measure what the lateness costs and bound what any
> phase correction could recover. They are not a result.

## Does the 95% band cover the weeks when the curve is climbing?

Every column should read 95%. A model at 95% overall but well below it on
rising weeks has a band that is not too narrow but pointed at the wrong weeks —
its width is a function of the predicted level, so a late centre drags a late
band with it. Width is in cases per 100,000, so it is the cost of any fix.

| model | all weeks | rising | flat | falling | mean band width |
| --- | --- | --- | --- | --- | --- |
| gnn_st | 96.810 | 89.933 | 100.000 | 96.774 | 32.599 |
| gnn_st_twosided | 95.694 | 94.631 | 100.000 | 88.387 | 36.636 |
| gnn_st_trendblend | 96.810 | 89.933 | 100.000 | 96.774 | 33.070 |
| gnn_st_slopeweight | 96.491 | 91.275 | 100.000 | 95.484 | 32.179 |

## Which way does the model miss when the curve is moving?

Mean over-prediction, in cases per 100,000; negative is under-prediction. A
late forecast is low on the way up and high on the way down by roughly the
same amount, which is how its annual bias can sit near zero while almost
every individual week is wrong.

| model | rising weeks | flat weeks | falling weeks |
| --- | --- | --- | --- |
| gnn_st | -10.322 | 0.964 | 9.574 |
| gnn_st_twosided | -10.322 | 0.964 | 9.574 |
| gnn_st_trendblend | -9.949 | 1.137 | 10.182 |
| gnn_st_slopeweight | -8.582 | 1.376 | 11.434 |

## Peak week, busiest neighborhoods first

Positive is late. `compare_severity.py` reports the threshold-crossing
version of this (`peak_week_error_weeks`); this one needs no fitted
threshold.

| model | neighborhood | peak_week_actual | peak_week_pred | peak_weeks_late | peak_actual | peak_pred |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st_twosided | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 268.792 |
| gnn_st_trendblend | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 272.744 |
| gnn_st | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 268.792 |
| gnn_st_slopeweight | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 288.681 |
| gnn_st_slopeweight | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 259.579 |
| gnn_st_twosided | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 245.341 |
| gnn_st_trendblend | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 248.673 |
| gnn_st | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 245.341 |
| gnn_st_slopeweight | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 151.469 |
| gnn_st_twosided | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 143.161 |
| gnn_st | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 143.161 |
| gnn_st_trendblend | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 147.133 |
| gnn_st_slopeweight | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 142.404 |
| gnn_st | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 131.037 |
