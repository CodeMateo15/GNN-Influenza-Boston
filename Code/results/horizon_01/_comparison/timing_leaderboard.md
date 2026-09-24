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

| model | weeks late | share of error that is timing | miss vs. slope | typical weekly miss | ...on the compared weeks | ...once shifted earlier | in step with truth | peak weeks late |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | 1 | 0.619 | -0.904 | 11.770 | 12.132 | 7.486 | 0.892 | 1.000 |
| lstm | 1 | 0.540 | -0.791 | 14.657 | 15.174 | 10.294 | 0.867 | 1.000 |
| persistence | 1 | 1.000 | -1.000 | 15.806 | 16.328 | 0.000 | 0.798 | 1.000 |

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
| gnn_st | 96.810 | 89.933 | 100.000 | 96.774 | 33.018 |
| lstm | 94.577 | 81.879 | 99.620 | 96.774 | 31.478 |
| persistence | 95.056 | 82.550 | 100.000 | 97.419 | 40.090 |

## Which way does the model miss when the curve is moving?

Mean over-prediction, in cases per 100,000; negative is under-prediction. A
late forecast is low on the way up and high on the way down by roughly the
same amount, which is how its annual bias can sit near zero while almost
every individual week is wrong.

| model | rising weeks | flat weeks | falling weeks |
| --- | --- | --- | --- |
| gnn_st | -10.231 | 1.017 | 9.733 |
| lstm | -12.871 | 0.847 | 6.616 |
| persistence | -16.303 | -0.024 | 15.229 |

## Peak week, busiest neighborhoods first

Positive is late. `compare_severity.py` reports the threshold-crossing
version of this (`peak_week_error_weeks`); this one needs no fitted
threshold.

| model | neighborhood | peak_week_actual | peak_week_pred | peak_weeks_late | peak_actual | peak_pred |
| --- | --- | --- | --- | --- | --- | --- |
| persistence | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 256.150 |
| lstm | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 258.951 |
| gnn_st | Dorchester | 2025-12-21 | 2025-12-28 | 1.000 | 256.150 | 269.207 |
| persistence | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 254.700 |
| lstm | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 202.460 |
| gnn_st | Roxbury | 2025-12-21 | 2025-12-28 | 1.000 | 254.700 | 246.328 |
| gnn_st | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 143.461 |
| lstm | Roslindale | 2025-12-28 | 2025-12-28 | 0.000 | 170.100 | 110.185 |
| persistence | Roslindale | 2025-12-28 | 2026-01-04 | 1.000 | 170.100 | 170.100 |
| gnn_st | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 130.976 |
| lstm | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 116.567 |
| persistence | South End | 2025-12-14 | 2025-12-21 | 1.000 | 132.300 | 132.300 |
| gnn_st | Mattapan | 2025-12-28 | 2026-01-04 | 1.000 | 110.300 | 101.605 |
| persistence | Mattapan | 2025-12-28 | 2026-01-04 | 1.000 | 110.300 | 110.300 |
