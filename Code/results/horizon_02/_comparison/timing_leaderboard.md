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
| gnn_st | 1 | 0.631 | -0.802 | 17.197 | 17.772 | 10.795 | 0.801 | 2.000 |

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
| gnn_st | 95.534 | 83.893 | 100.000 | 97.419 | 39.372 |

## Which way does the model miss when the curve is moving?

Mean over-prediction, in cases per 100,000; negative is under-prediction. A
late forecast is low on the way up and high on the way down by roughly the
same amount, which is how its annual bias can sit near zero while almost
every individual week is wrong.

| model | rising weeks | flat weeks | falling weeks |
| --- | --- | --- | --- |
| gnn_st | -11.505 | 1.895 | 9.363 |

## Peak week, busiest neighborhoods first

Positive is late. `compare_severity.py` reports the threshold-crossing
version of this (`peak_week_error_weeks`); this one needs no fitted
threshold.

| model | neighborhood | peak_week_actual | peak_week_pred | peak_weeks_late | peak_actual | peak_pred |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | Dorchester | 2025-12-21 | 2026-01-04 | 2.000 | 256.150 | 268.455 |
| gnn_st | Roxbury | 2025-12-21 | 2026-01-04 | 2.000 | 254.700 | 245.403 |
| gnn_st | Roslindale | 2025-12-28 | 2026-01-04 | 1.000 | 170.100 | 145.639 |
| gnn_st | South End | 2025-12-14 | 2025-12-28 | 2.000 | 132.300 | 138.673 |
| gnn_st | Mattapan | 2025-12-28 | 2026-01-04 | 1.000 | 110.300 | 100.915 |
| gnn_st | Hyde Park | 2025-12-21 | 2026-01-04 | 2.000 | 94.600 | 97.355 |
| gnn_st | Charlestown | 2025-12-14 | 2025-12-28 | 2.000 | 92.800 | 86.354 |
| gnn_st | West Roxbury | 2025-12-21 | 2026-01-04 | 2.000 | 88.000 | 72.912 |
| gnn_st | Allston/Brighton | 2025-12-21 | 2026-01-04 | 2.000 | 80.600 | 77.569 |
| gnn_st | Jamaica Plain | 2025-12-21 | 2026-01-04 | 2.000 | 61.100 | 56.363 |
| gnn_st | East Boston | 2025-12-28 | 2026-01-04 | 1.000 | 59.300 | 52.320 |
| gnn_st | Back Bay/Beacon Hill/Downtown/North End/West End | 2025-12-21 | 2026-01-04 | 2.000 | 58.100 | 54.724 |
| gnn_st | South Boston | 2025-12-28 | 2025-12-28 | 0.000 | 57.000 | 54.353 |
| gnn_st | Fenway | 2026-01-04 | 2025-12-28 | -1.000 | 21.100 | 25.783 |
