# Data notes — quirks, defects and what each loader does about them

Everything here is handled in `influenza/data.py`. Read this before adding a
source or trusting a number.

## Two defects that invalidated every earlier result

Both were found in August 2026 while standardising the metrics, and both had
been silently affecting the two `.py` baselines and all eight notebooks since
the project started.

### 1. An ILI count row was averaged with the rate row

The weekly block of `BPHC Dashboard Influenza Neighborhood.csv` contains
**exactly two rows for every (week, neighborhood)** — the integer ILI ED-visit
count and the rate per 100,000 — and **both are labelled
`unit="per 100,000 residents"`**. Verified across all 6,108 pairs: the lower
value is an integer in 100% of pairs, the upper in only 6%.

```
Roxbury, week of 2017-12-31:   value = 20.0     <- count
Roxbury, week of 2017-12-31:   value = 65.3     <- rate per 100,000
```

20 / 65.3 × 100,000 implies a population of about 30,600, which is right for
Roxbury. The old loaders did `groupby([date, node])['value'].mean()` — a comment
in the notebook says *"For Dorchester: multiple rows may map to same index →
average them"* — so every model trained and scored on `(count + rate) / 2`.

Because each neighborhood's population is fixed, that quantity is a constant
multiple of the truth: `(pop + 100000) / 200000`, or about 0.65× for Roxbury.
So per-neighborhood MAPE and Corr were unaffected, but **MAE and RMSE were
wrong, and wrong by a different factor in each neighborhood**, which also
distorts every pooled metric.

`load_rates()` now takes the maximum of each pair (always the rate) and asserts
that each pair has exactly two rows, so a change in the upstream layout fails
loudly instead of silently.

### 2. Suppressed weeks became zero-rate weeks

Coverage is uneven — Charlestown has 340 of 436 weeks — and the old loaders
called `fillna(0)`. In the post-COVID window that invented **140 fake zero-rate
neighborhood-weeks**:

| neighborhood | missing weeks (of 201) |
|---|---|
| Charlestown | 35 (17.4%) |
| West Roxbury | 28 (13.9%) |
| South Boston | 19 (9.5%) |
| Fenway | 13 (6.5%) |
| others | 2–8 each |

The file contains **zero** genuine zeros in 2,875 post-COVID observations, so a
missing week is BPHC suppressing a small count, not an absence of influenza.
Treating those as 0.0 is what produced Charlestown's 74% MAPE and the
`MAPE_n = 24/30` in the old metrics files.

Now: missing weeks are `NaN`. Targets stay `NaN` and are dropped from the loss
and from every metric (`n_obs` in `metrics.csv` reports how many cells were
actually scored). Features must be finite, so `impute_causal()` fills them by
carrying the last observation forward, then falling back to an expanding
(causal) median.

**Interpolation is deliberately not used for features.** A sample's lookback
window ends at the forecast origin, so interpolating the origin week's value
would read the following week — which is the target.

## Two more defects found while porting

### 3. ARIMA order selection compared the wrong shapes

`np.asarray(preds)` is `(n, 1)` and the actuals are `(n,)`, so subtracting them
broadcast into an `(n, n)` outer difference instead of comparing elementwise.
Fixed in `run_arima.py::_selection_rmse`, which now ravels and asserts equal
lengths.

Fixing it changed which orders get selected, and one of the new selections
(Dorchester, `(3, 0, 1)`) had an explosive AR root — `enforce_stationarity=False`
permits that — producing forecasts of 1e34 that grew 1.5× per week. An
`isfinite()` check does not catch a finite-but-absurd number, so
`forecast_bound()` now rejects any forecast beyond 10× the observed historical
maximum and an order that needs the fallback path on validation is disqualified.

### 4. Under-covered covariates were filled with zero

The type-1 ED file ends 2026-01-04 and the demographics file 2025-12-07, while
the evaluation window runs to 2026-05-03. Filling the gap with `0.0` put
`ed_count` **9.3 standard deviations below its training mean**, and the GNN
extrapolated wildly. `_carry_forward()` now forward-fills and prints how many
weeks were carried. Whole-series normalisation had masked this, because the same
zeros inflated the standard deviation used to judge the shift.

## Source inventory

| file | resolution | coverage | geography | notes |
|---|---|---|---|---|
| `BPHC Dashboard Influenza Neighborhood.csv` | weekly | 2017-12-31 → 2026-05-03 | 15 BPHC names | two rows per cell; see defect 1 |
| `...Influenza ED Visits-type 1.csv` | weekly | → 2026-01-04 | citywide | series name lives in `demographic_category` |
| `...Influenza ED Visits-type 2.csv` | weekly | → 2026-05-03 | citywide | cleanest citywide weekly series |
| `...Influenza Demographics.csv` | monthly | → 2025-12-07 | 15 names + ZIP/age/race | the only neighborhood **counts** |
| `...Influenza Wastewater.csv` | ~2–4 daily | 2024-07-28 → | 12 sewersheds | concentration index, not counts |
| `COVID Cases Neighborhood.csv` | **monthly** | 2020-01 → 2026-07 | 15 names | both count and rate rows; filter on `unit` |
| `COVID Testing Neighborhood.csv` | **monthly** | 2020-01 → 2026-07 | 15 names | count / per-100k / percent |
| `COVID cases in Wastewater.csv` | ~2–4 daily | **2022-10 → 2026-08** | 11 sites | **different schema**; see below |
| `Confirmed RSV Cases - Neighborhood.csv` | **monthly** | 2018-01 → 2026-06 | 15 names | rates are **per MILLION** |
| `RSV cases in Wastewater.csv` | ~2–4 daily | 2024-08 → 2026-07 | 12 sewersheds | |
| `Mass Dashboard Vaccination Data *.xlsx` | weekly statewide | 3 seasons | statewide / town | `< 1.0%` read as 0.5% |
| `Neighborhood Data/*.csv` | annual | latest year (2025) | 23 planning districts | 7-line metadata preamble |
| `MBTA/mbta_adjacency_matrix.csv` | static | — | 14 canonical nodes | 32 non-zero pairs |

### Units are not implied by the column name

Each COVID indicator appears in **both** count and rate form, distinguished only
by the `unit` column, and RSV rates are per 1,000,000 while everything else is
per 100,000. `load_monthly_neighborhood()` therefore requires an explicit
`unit`. Never `groupby().mean()` across units — that is exactly defect 1.

### COVID wastewater uses a different schema

`BPHC Dashboard COVID cases in Wastewater.csv` is MWRA-style, not BPHC long
format: `date, site, eff, smooth, site_latest_val, site_latest_lab`. We read
**`eff`** (the raw effective concentration) and ignore `smooth`, which is
centred-smoothed and would leak later weeks into each observation.

It is also the most useful of the three wastewater files: it starts 2022-10 and
so spans the whole post-COVID training period, whereas the influenza and RSV
wastewater files only begin in mid-2024 and land almost entirely inside the
evaluation window.

### Sewersheds do not match neighborhoods

All three wastewater files share one 12-name geography. `WASTEWATER_TO_IDX` maps
zones to nodes, splitting `Roslindale/West Roxbury` across two nodes and
treating the Back Bay zone as the stand-in for Fenway, South Boston and South
End, which have no sewershed of their own. Without that, those three nodes would
have no wastewater signal at all. `Boston` (a citywide aggregate) and `NA` are
dropped.

### Monthly sources become weekly step functions

`load_monthly_neighborhood()` holds each month's value flat across its weeks. A
step function fabricates nothing; interpolating would invent a within-month
slope the data does not contain. The resolution mismatch is real and is the main
reason COVID and RSV features default to off.

## Miscellaneous

- `Data/Weather copy/` is a stale duplicate of `Data/Weather/` (16 files versus
  15, the extra being a citywide file). Everything reads `Data/Weather/`.
- The Boston planning-district CSVs use a 23-name geography that needs its own
  aggregation (`GEOID_TO_IDX`), e.g. Allston + Brighton → one node, Fenway +
  Longwood + Mission Hill → Fenway.
- Neighborhood names in the four BPHC COVID/RSV files match the influenza file
  **string for string**, including `BB/BH/DT/NE/WE` and both `Dor (…)` forms, so
  no crosswalk is needed there.
