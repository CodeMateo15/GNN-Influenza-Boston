# Pre-refactor results — kept for the record, not comparable

These are the ARIMA and LSTM outputs as they stood before the standardisation
work. They are preserved because they are what `docs/EDGES_AND_NODES_NOTES.txt`
and the earlier writeups refer to. **Do not compare them against anything in
`results/`.** Two independent reasons:

1. **Different evaluation window.** These use `2025-10-01 -> 2026-05-31`
   (30 target weeks, Oct-May). Current results use `2025-05-31 -> 2026-05-31`
   (48 target weeks) and report a flu-season segment of Oct-Mar (26 weeks).
   The old window is neither.
2. **Different input data.** They were produced by the pre-fix loader, which
   averaged an ILI visit *count* row together with the *rate per 100,000* row,
   and imputed suppressed neighborhood-weeks as `0.0`. See `docs/DATA_NOTES.md`.

`compare_models.py` skips any directory starting with `_`, so these are excluded
from the leaderboard automatically. They also predate the `segment` column, so
loading them would raise without `--allow-legacy`.
