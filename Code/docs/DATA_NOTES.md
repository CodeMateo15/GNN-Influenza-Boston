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

## Five defects found during the v2 rebuild

Numbered 5 to 9, continuing the list above. All five were live in every result
committed before this branch. The first two dominate: together they were the
largest single source of error in the graph models, and fixing them alone --
with no model change at all -- moved the then-current graph arm from RMSE 24.90
to 19.12 at one week ahead and from 41.34 to 31.49 at four weeks.

(The `gcn_fusion` arms named throughout this section -- `gnn_multiedge`,
`gnn_corrbinary` and their variants -- have since been retired from the registry.
They are named here because that is where the defects were measured; the numbers
are reproducible only from git history.)

### 5. Every city-wide covariate froze one week after the season peak

`_carry_forward` forward-filled without a limit. All five city-wide covariates
stop on 2025-12-28 -- one week after the 2025-26 peak of 2025-12-21 -- so for the
last 19 of the 49 evaluation weeks the model was fed:

```
ili_count      = 1355.0     ed_count      = 13112.0
ili_ed_perc    = 10.33      flu_cases     = 404.0
monthly_cases  = 2071.0   (frozen from 2025-11-30, 23 weeks)
```

Those are near-peak values held flat through the entire spring decline: 39% of
the evaluation window told the model the epidemic had not ended. It is the
mechanism behind the over-prediction `METHODS.md` describes as *"sits at roughly
50 per 100,000 from February onward while the observed series falls back to about
20"*, and behind the accidental ablation in commit `1709a20` where dropping four
of the five covariates improved `gnn_corrbinary` from RMSE 31.788 to 16.918 with
no model change.

**Fixed** by bounding the fill. `data.CARRY_FORWARD_LIMIT_WEEKS` declares, per
covariate, how stale it may get -- roughly its real publication lag. Past that it
stays NaN, which z-scores to the training mean, and `data.coverage_report()`
counts the affected weeks into `run_config.json`. A fabricated value is now a
visible gap.

### 6. The file that fixes defect 5 was already in the repo, unread

`paths.FLU_ED_TYPE2_FILE` had no consumers. The type-2 export carries the same
ILI-share-of-ED-visits series as type 1's `ili ed perc` row but runs 101 weeks
longer, through 2026-05-03 -- the whole evaluation window.

Verified identical wherever they overlap: **Pearson 1.000000 over 335 shared
weeks, maximum absolute difference 0.0.** So it is strictly the longer view of
one series, not a second measurement. Where type 1 was frozen at 10.33 for 19
weeks, type 2 records the real collapse:

```
7.82  4.98  3.81  2.78  2.90  2.67 ... 1.53  1.30  1.28
```

**Fixed.** `load_ed_metrics` now sources `ili_ed_perc` from type 2 and asserts
the two still agree on their overlap, so a future re-export that changes one
definition fails loudly instead of silently preferring the longer file.
`ili_ed_perc` went from 19 missing evaluation weeks to **0**, and is now the only
city-wide covariate in `DEFAULT_GLOBALS`.

### 7. Wastewater was snapped to Monday weeks, leaking one day

`load_wastewater` floored samples with `date - dayofweek`, i.e. to Monday-start
weeks, while the flu grid is Sunday-start. `_align_weekly` then matched with
`method="nearest"`, so the flu week beginning Sunday *S* took the Monday window
*S+1 … S+7* -- whose last day is the first day of the horizon-1 **target** week.
A one-day look-ahead on all 93 covered weeks, inside `use_covid_wastewater` and
therefore inside every arm that enabled it -- including the one METHODS.md then
called the single biggest improvement. That claim has since been **retracted**:
re-measured on `gnn_st`, the same feature group costs 0.119 macro Corr. This
defect is half the reason why.

**Fixed** by flooring to Sunday with `(dayofweek + 1) % 7`, the same expression
`columbus.snap_to_week` already used.

### 8. `_align_weekly` could match forward in time

Independently of defect 7, `method="nearest"` with a 7-day tolerance was free to
take a value from *after* the target week when it was the closer of the two
candidates. Measured: the flu week beginning 2024-07-28 drew its wastewater from
the week beginning 2024-08-04, and **`monthly_cases` read the following month's
citywide count on 89 of 436 weeks**.

**Fixed** by switching to `method="pad"`, which considers only observations at or
before the flu week. Weather and the ED metrics were unaffected (0 cells moved);
wastewater moved 13-14 cells and `monthly_cases` 89.

### 9. `pop_density` summed planning-district densities

`_load_city_csv` sums its value columns across the districts making up a node,
which is right for counts and wrong for a ratio. Six of the fourteen nodes are
multi-district, so the published *density* column was being added up:

```
Back Bay/Beacon Hill/Downtown/North End/West End   185,247 per sq mi
```

That is roughly three times Manhattan and physically impossible -- five
districts' densities summed. It corrupted the `pop_density` node feature and,
because `graphs.build_graph` sets the demographic-similarity bandwidth from the
median pairwise distance, the demographic edge weights as well.

**Fixed** by `data._population_density()`, which recovers each district's land
area as population ÷ density, sums numerators and denominators separately, then
divides. No new data required. The range becomes a plausible 6,112 (West
Roxbury) to 42,854 (South End), and the demographic edge count moves 63 → 60.

## Three cities, side by side

This file records Boston's data and the defects found in it. The other two
cities have their own notes: [COLUMBUS_DATA_NOTES.md](COLUMBUS_DATA_NOTES.md)
and [AMBA_DATA_NOTES.md](AMBA_DATA_NOTES.md). This section is the one place
that lines all three up; [METHODS § Cities](METHODS.md#cities) covers the
modelling consequences.

### Target series

| | Boston | Columbus OH | Buenos Aires (AMBA) |
|---|---|---|---|
| publisher | Boston Public Health Commission | Columbus Public Health | Argentina Ministry of Health, SNVS |
| measure | ILI ED visit rate | ILI ED visits, line-level | ETI (influenza-like illness) cases |
| unit as shipped | rate per 100,000 | one row per visit | weekly count per partido |
| denominator | built in | ACS 5-year population, summed ZCTA → area | INDEC 2022 census population |
| geography | 14 neighborhoods | 17 areas, ZIP crosswalk | 19 partidos (+5 anchors) |
| starts | 2017-12-31 | 2022-01-02 | 2022-01-02 |
| small counts | suppressed → NaN | absent visit = observed zero | isolated gap → 0; ≥3-week blackout → NaN |
| revision | none recorded | none recorded | **backfills ~4 months**; tail trimmed from the completeness curve |
| last week used | 2026-05 | 2026-07 | 2025-11-02 (after trimming) |

### Demographic columns

Raw values are ratios; every loader min-max scales within its own city, so
inside the model only the ordering of nodes within a city carries.

| column | Boston | Columbus | Buenos Aires |
|---|---|---|---|
| `pop_density` | BPDA population / area, re-derived per district ([defect 9](#9-pop_density-summed-planning-district-densities)) | ACS population / Gazetteer land area | INDEC `est_c2_2`, exact |
| `pct_children` | BPDA, ages 0–19 | ACS B01001, under 20 | INDEC `est_c9_2` + `est_c7_2`, **under 15, derived** |
| `pct_elderly` | BPDA, 65+ | ACS B01001, 65+ | INDEC `est_c7_2`, 65+ |
| `owner_rate` | BPDA tenure | ACS B25003 | INDEC `hogares_c6_2` |
| `poverty_rate` | BPDA poverty status | ACS B17001 | INDEC `salud_c1_2` **no-health-coverage proxy** |
| `transit_share` | BPDA commute mode | ACS B08301 | not asked by the 2022 census |
| `no_vehicle_rate` | BPDA vehicles available | ACS B08201 | not asked by the 2022 census |
| `nonwhite_share` | BPDA race/ethnicity | ACS B03002 | no equivalent construct |
| provenance | published by the agency | derived by this project | derived by this project |

Two of the Buenos Aires columns are not the same quantity as their US
namesakes: `pct_children` is a narrower age band and `poverty_rate` is a
coverage measure, not an income line. They behave like the originals after
within-city scaling (the deprivation proxy runs opposite to the elderly share,
Spearman −0.93, as poverty and age do in the US cities), but should never be
compared across cities in raw units.

### Covariates and features each city can supply

| | Boston | Columbus | Buenos Aires |
|---|---|---|---|
| weather | yes | yes | yes |
| demographics | 8 columns | 8 columns | 5 columns |
| wastewater, RSV, COVID, vaccination | yes | no | no |
| hospitalisations | no | yes | no |
| city-wide globals | ili_count, ed_count, ili_ed_perc, flu_cases, … | ili_count, hospitalizations | ili_count |

A run asking for an input its city lacks is refused before any data loads
(`cli.check_experiment_supported`), with a list of arms that do run.

### Weather

All three come from the same Open-Meteo endpoint through the same fetcher and
weekly aggregation (`scrapers/scrape_weather.py`), one file per node, the same
six `WEATHER_COLS`. Buenos Aires's series runs in antiphase to the US cities'
— cold in July — and nothing corrects for that, deliberately: the model reads
weather per city, and the climatology term is phase-free.

---

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
