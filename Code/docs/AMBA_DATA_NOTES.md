# Buenos Aires / AMBA data notes

What the third city's data is, where it comes from, and the four places it does
not line up with Boston and Columbus. Written in the same spirit as
`COLUMBUS_DATA_NOTES.md`: the differences are recorded rather than smoothed
over, because a difference that is hidden reads as a result.

## 1. The series

Argentina's Ministry of Health publishes national respiratory surveillance
(SNVS) as a snapshot workbook per release. Three vintages are committed:
`...hasta-20240405`, `...hasta-20250904`, `...hasta-20260310`.

`Code/scrapers/build_amba_panel.py` merges them, newest winning on any
overlapping key, and filters to `evento_nombre` containing **ETI** (*enfermedad
tipo influenza*, influenza-like illness) in the 24 partidos of the Conurbano
Bonaerense (`provincia_id == 6`).

Output: 2022-W1 onward, weekly, on the same Sunday-start grid Boston and
Columbus use. The MMWR week arithmetic is the same as
`loaders/columbus.py:69-86`.

**These are case counts, not a published rate.** Like Columbus, unlike Boston.

## 2. Node set: 19 scored, 5 anchors, from coverage

The split is measured, not hand-drawn. `amba_node_coverage.csv` records the
share of weeks each partido reported; the 19 at ≥90% are scored nodes and the 5
below are anchors:

| below 90% | coverage |
|---|---|
| Berazategui | 0.890 |
| Hurlingham | 0.876 |
| San Fernando | 0.839 |
| Ituzaingó | 0.752 |
| Esteban Echeverría | 0.500 |

This is the Columbus anchor logic — thin reporting at the boundary is exactly
the anchor role — with the difference that here it comes out of the panel
rather than off a crosswalk's unassigned list.

`cities/buenos_aires.py` reads the coverage file at import, so the 0.90 rule
lives in one place and a rebuilt panel cannot silently disagree with the node
list.

## 3. Zeros are not all the same thing

`build_amba_panel.py` distinguishes two kinds of absent partido-week:

* an **isolated** absence is a true zero, and becomes `0.0`;
* a run of **three or more** consecutive absences is a reporting blackout, and
  stays `NaN`.

So Buenos Aires behaves like **Boston** for suppression purposes
(`suppresses_small_counts=True`) even though its source is counts like
Columbus's. 1.5% of scored partido-weeks are NaN.

## 4. The four real differences

### 4.1 Southern hemisphere

Measured from the panel, not assumed. The citywide curve peaks in **epiweeks
20–23** every year (2022 SE21, 2023 SE20, 2024 SE21, 2025 SE23) and the monthly
mean rate is:

```
 1   20.9        7   62.7
 2   20.8        8   55.6
 3   32.6        9   52.1
 4   39.3       10   39.4
 5   79.8       11   27.8
 6   82.3       12   19.8
```

The season is **April–September**: an exact six-month mirror of Boston's
October–March. `City.flu_months` carries it.

`City.season_start_month` is **February**. The annual trough is flat —
December 19.8, January 20.9, February 20.8, a 6% spread — so which month is
lowest is noise. February is chosen because it is the mirror of Boston's
August: MEM defines a season as ISO week 30→29, and week 30 plus 26 weeks is
week 4, late January, which rounds to the February boundary.

`influenza/climatology.py` needs no change. Its day-of-year harmonic fit is
phase-free and transfers to the Southern Hemisphere as-is.

### 4.2 Five demographic columns, not eight

INDEC's 2022 definitive results are ~100 per-topic workbooks for the province,
and many are broken down per partido. `Code/scrapers/build_amba_static.py`
reads five of them:

| column | source cuadro | fit |
|---|---|---|
| `pop_density` | `est_c2_2` | exact; reconciles with INDEC's own density column to 0.1% |
| `pct_elderly` | `est_c7_2` | exact, share aged 65+ |
| `owner_rate` | `hogares_c6_2` | exact, owned households / all households |
| `pct_children` | `est_c9_2` + `est_c7_2` | **derived, and a different age cut**: `D/(100+D) - pct_elderly` from the dependency index `D` gives the **under-15** share; Boston and Columbus use under-20 |
| `poverty_rate` | `salud_c1_2` | **proxy**: share with no obra social, prepaga or state health plan. The census asks no income question |

Absent, and not fillable from this census:

* `transit_share`, `no_vehicle_rate` — the 2022 questionnaire asks neither
  commute mode nor vehicle availability.
* `nonwhite_share` — no equivalent construct. Foreign-born and afro-descendant
  shares are published per partido, but they measure something else, and
  putting them under this name would make the column meaningless to compare.

After the loader's within-city min-max scaling only the ordering of partidos
survives, so the under-15 cut and the coverage proxy behave like their US
counterparts inside the model. They should not be compared across cities in raw
units. Face validity holds: the deprivation proxy runs opposite to the elderly
share (Spearman −0.93), and Vicente López — the wealthiest partido — is the
least deprived.

**A correction on the record.** The first version of this note said Buenos
Aires had no demographics at all, having checked only the province-level
cuadros. That was wrong, and it would have left BA unable to run `gnn_st`. The
static block is now five columns wide, the loader returns the names, and
`samples._feature_names` labels the block from them.

`STATIC_DEMO_COLS` stays eight wide for Boston and Columbus. Shrinking it to
the intersection would have invalidated every existing checkpoint to align a
column set the cities can never fully share anyway.

### 4.3 The feed backfills for months

Unique to this city among the three. The revision table
(`amba_eti_revision.csv`) compares older vintages against the newest and gives
the median share of a week's eventual total that had arrived by each reporting
lag:

```
L0 0.00  L2 0.46  L4 0.77  L6 0.76  L8 0.87  L10 0.89  L12 0.93  L14 0.95  L16 0.95
```

Two consequences.

**The tail is trimmed.** `load_rates` drops trailing weeks using this curve.
Note the curve is *not* monotone — it reaches 0.95 at lag 14, falls back to 0.94
at 15 — so the loader takes the lag from which completeness **stays** above the
floor, not the first lag that touches it. The committed panel runs to
2026-03-01; the loader serves data to **2025-11-02**.

**The evaluation window is the city's own.** `City.test_start`/`test_end` are
`2024-11-03 → 2025-11-02`: a full year ending at the last complete week. The
shared 2025-06 → 2026-05 window would score four months of still-arriving
counts as model error. This window contains the whole 2025 season (peak
2025-06-08) and leaves 148 weeks of history to train on.

### 4.4 Adjacency is derived, and the file is the source

`Code/scrapers/derive_amba_adjacency.py` reads IGN boundary polygons and calls
two partidos adjacent when they share ≥2 boundary vertices — the rule
`derive_columbus_adjacency.py` uses, chosen because hand-coding was measured
there at 87% accurate. 48 edges over 24 partidos, degree 2–8, mean 4.0. The
edge count is identical at 4, 5 and 6 decimal places of rounding, which is the
check that the polygons share vertices exactly rather than merely closely.

Unlike Columbus — where the derived CSV is written and then read by nothing,
while the live edge list is a hand-synced literal — `cities/buenos_aires.py`
loads `amba_partido_edges.csv` at import. One source, no sync step.

Several scored partidos border the Autonomous City of Buenos Aires, which the
province's surveillance does not cover and which is not a node. Those
boundaries are absent by construction; the anchors and the `Outside` background
node carry them.

## 5. What Buenos Aires can and cannot run

| | available |
|---|---|
| features | `weather`, `seasonality`, `demographics` (5 columns) |
| globals | `ili_count` |
| variants | `post_covid` only (the series starts 2022-01-02) |

`gnn_st` runs here with 43 node features against Boston's 46 — three fewer
static columns. Arms needing wastewater, RSV, COVID or vaccination are refused
at argument-parse time by `cli.check_experiment_supported`, which names the
arms that do run.

## 6. Verification

`python -u Code/run_buenos_aires_data_check.py --strict` — 41 assertions
covering the node set, the graph, the week grid, the population denominator,
the season, the backfill trim, the evaluation window, weather alignment and the
feature gating. Two are worth naming because they catch errors no shape check
would:

* **July must be colder than January.** A sign-flipped longitude or latitude
  would still produce a plausible-looking weather series; a hemisphere check
  would not.
* **`season_start_month` must sit in the annual trough.** This one already
  caught a real mistake: the boundary was first set from the untrimmed *counts*,
  where February is the floor, but on *rates* December is. The check was then
  itself corrected — an exact-argmin test over a 6%-flat trough is testing
  noise, so it now asserts membership of the trough.
