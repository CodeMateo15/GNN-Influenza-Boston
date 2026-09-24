# Forecast timing at 2 weeks ahead

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
| gnn_st + de-lag | 1 | 0.576 | -0.778 | 16.748 | 17.303 | 11.272 | 0.815 | 2.000 |
| gnn_st | 1 | 0.630 | -0.801 | 17.214 | 17.787 | 10.823 | 0.802 | 2.000 |

> Sliding a forecast one week earlier is the same thing as relabelling an
> h=2 forecast as h=1: it buys the accuracy with a week of
> lead time. These columns measure what the lateness costs and bound what any
> phase correction could recover. They are not a result.

## Does the 95% band cover the weeks when the curve is climbing?

Every column should read 95%. A model at 95% overall but well below it on
rising weeks has a band that is not too narrow but pointed at the wrong weeks —
its width is a function of the predicted level, so a late centre drags a late
band with it. Width is in cases per 100,000, so it is the cost of any fix.

| model | all weeks | rising | flat | falling | mean band width |
| --- | --- | --- | --- | --- | --- |
| gnn_st + de-lag | 96.085 | 85.714 | 100.000 | 98.039 | 39.516 |
| gnn_st | 95.853 | 85.235 | 100.000 | 97.419 | 39.445 |

## Which way does the model miss when the curve is moving?

Mean over-prediction, in cases per 100,000; negative is under-prediction. A
late forecast is low on the way up and high on the way down by roughly the
same amount, which is how its annual bias can sit near zero while almost
every individual week is wrong.

| model | rising weeks | flat weeks | falling weeks |
| --- | --- | --- | --- |
| gnn_st + de-lag | -10.733 | 2.189 | 8.677 |
| gnn_st | -11.418 | 1.941 | 9.422 |

## Peak week, busiest neighborhoods first

Positive is late. `compare_severity.py` reports the threshold-crossing
version of this (`peak_week_error_weeks`); this one needs no fitted
threshold.

| model | neighborhood | peak_week_actual | peak_week_pred | peak_weeks_late | peak_actual | peak_pred |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | Dorchester | 2025-12-21 | 2026-01-04 | 2.000 | 256.150 | 270.062 |
| gnn_st + de-lag | Dorchester | 2025-12-21 | 2026-01-04 | 2.000 | 256.150 | 270.548 |
| gnn_st + de-lag | Roxbury | 2025-12-21 | 2026-01-04 | 2.000 | 254.700 | 247.315 |
| gnn_st | Roxbury | 2025-12-21 | 2026-01-04 | 2.000 | 254.700 | 246.769 |
| gnn_st + de-lag | Roslindale | 2025-12-28 | 2026-01-04 | 1.000 | 170.100 | 147.800 |
| gnn_st | Roslindale | 2025-12-28 | 2026-01-04 | 1.000 | 170.100 | 146.516 |
| gnn_st + de-lag | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 144.290 |
| gnn_st | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 139.608 |
| gnn_st | Mattapan | 2025-12-28 | 2026-01-04 | 1.000 | 110.300 | 101.457 |
| gnn_st + de-lag | Mattapan | 2025-12-28 | 2026-01-04 | 1.000 | 110.300 | 104.356 |
| gnn_st | Hyde Park | 2025-12-21 | 2026-01-04 | 2.000 | 94.600 | 97.920 |
| gnn_st + de-lag | Hyde Park | 2025-12-21 | 2026-01-04 | 2.000 | 94.600 | 98.241 |
| gnn_st + de-lag | Charlestown | 2025-12-14 | 2025-12-28 | 2.000 | 92.800 | 89.911 |
| gnn_st | Charlestown | 2025-12-14 | 2025-12-28 | 2.000 | 92.800 | 86.985 |
