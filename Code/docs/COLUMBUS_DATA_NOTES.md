# Columbus data notes — sources, quirks and what each loader does about them

The Columbus counterpart to [`DATA_NOTES.md`](DATA_NOTES.md). Everything here is
handled in `influenza/loaders/columbus.py` and
`influenza/loaders/columbus_crosswalk.py`. Read this before adding a source or
trusting a number.

Verify the whole layer with:

```bash
python Code/run_columbus_data_check.py
```

21 checks currently pass; the one skip is the rate conversion, which needs a
Census API key (see [The denominator is ours](#the-denominator-is-ours)).

## Why Columbus at all

Boston's findings rest on one city, one test season, one seed. Columbus is the
second city, chosen because Franklin County publishes ILI emergency-department
surveillance at a sub-city geography with enough history to reach Boston's
evaluation window. The question is whether the model *ordering* reproduces, not
whether Columbus forecasts better.

## The fundamental difference from Boston

Boston's sources arrive **pre-aggregated**: BPHC publishes a weekly ILI ED-visit
rate per 100,000 per neighborhood, and `data.py` mostly reshapes it. Columbus
arrives as **three line-level extracts** — one row per ED visit, per
hospitalisation, per COVID case — keyed to a 5-digit home ZIP. The weekly grid,
the node aggregation and the population denominator all have to be constructed.

## Source inventory

| file | resolution | coverage | geography | notes |
|---|---|---|---|---|
| `ILI Specified Data-Franklin_final.xlsx` | **line-level**, minute timestamps | 2022-01-01 → 2026-07-27, 63,103 rows | 44 ZIPs | the target series; `Syndrome` is constant `ILISpecified` |
| `IAH Data CPH Franklin_final.csv` | line-level, MMWR year/week | 2022-W01 → 2026-W28, 3,713 rows | 41 ZIPs (`ZIP5`) | flu hospitalisations; **Boston has no equivalent** |
| `COVID Data CPH Franklin_final.csv` | line-level, MMWR year/week | 2021-W52 → **2025-W43**, 220,555 rows | 59 ZIPs (`zip_5`) | ends inside the evaluation window |
| `Columbus_FC_Zip_Areas_Nov2019.xlsx` | static | Nov 2019 | 49 ZIPs → 17 areas | header on row 2; see below |
| `columbus_area_geography.csv` | static | — | 17 areas | **generated**, `scrape_gazetteer_columbus.py`, keyless |
| `columbus_area_static.csv` | static | ACS 2023 5-year | 17 areas | **generated**, `scrape_acs_columbus.py`, needs an API key |
| `Data/Columbus Weather/*.csv` | weekly | 2022-01-02 → | 17 areas | **generated**, `scrape_weather_columbus.py` |

The last three are derived by this project, not published by an agency. Boston's
equivalents were published by its health department and the City of Boston. That
provenance difference is recorded in each generated file's comment header.

## The node geography: 17 areas, not 44 ZIPs

The crosswalk offers two resolutions: a fine `Area*` column (45 labels) and a
coarse `17 Areas` column. We use the coarse one, for two reasons.

**Data per node.** 17 nodes against ~3.5 seasons of weekly history is the same
regime as Boston's 14. The 44 ZIPs that actually appear would be three times the
nodes on the same history.

**Missingness.** At ZIP level 23.3% of cells are zero. Aggregated to the 17
areas, 3.0% are:

| area | mean visits/week | zero weeks (of 238) |
|---|---|---|
| Far East | 67.1 | 0 |
| West | 46.4 | 0 |
| Northland | 23.1 | 0 |
| … | … | … |
| UA/Grandview | 3.2 | 22 (9.2%) |
| Bexley | 3.1 | 29 (12.2%) |

The four low-volume areas are still thin, and their rates will be coarsely
quantised — the direct analogue of Boston's Fenway, whose best RMSE of 3.67
against a mean rate of 7.0 "looks better and fits relatively worse". Expect the
same artefact and read the per-area tables with the scale in view.

## Quirks each loader works around

### 1. The crosswalk header has a trailing space

The column is `'17 Areas '`, not `'17 Areas'`, and the real header is on the
**second** row (the first is blank; the last four rows are footnotes). Reading it
by exact name is a silent `KeyError` waiting to happen, so `load_crosswalk()`
lower-cases and strips every header rather than hardcoding the typo.

### 2. Three ZIP column spellings, three ZIP universes

`Zipcode` (ILI), `ZIP5` (IAH), `zip_5` (COVID) — same meaning, three names, which
is why `_read_line_level_weekly()` takes the column name as an argument. The ZIP
sets also differ: 44 / 41 / 59. The COVID file reaches as far as Cincinnati-area
ZIPs (45040, 45140); those simply do not map to an area and are dropped.

### 3. Row accounting must close

Of 63,103 ILI visits:

```
    147  in the 7 fringe ZIPs the crosswalk lists but leaves unassigned
    107  in 4 ZIPs absent from the crosswalk entirely (43086, 43109, 43216, 43234)
     72  in the two partially observed edge weeks
 62,777  retained in the 17-area panel (99.48%)
```

`KNOWN_UNMAPPED_ZIPS` names those four so a future crosswalk revision that covers
them fails an assertion rather than silently shifting the denominator.

### 4. Partial edge weeks are dropped

The extract starts on a Saturday and ends on a Monday, so its first and last
weeks are fractionally covered and their counts are spuriously low. Keeping them
would put two artificial troughs at the ends of every series, one of which sits
in the evaluation window's tail. `_full_weeks()` drops both, giving **238
contiguous Sunday-start weeks, 2022-01-02 → 2026-07-19**, every gap exactly 7
days.

### 5. Zeros are real here, unlike Boston

This is the most important asymmetry in the project.

Boston's absent `(week, neighborhood)` rows are BPHC **suppressing a small
count**; the file contains no genuine zeros, so imputing 0.0 invented ~140 fake
zero-rate weeks and helped void every result before August 2026
(`DATA_NOTES.md` defect 2). Boston's missing weeks must stay `NaN`.

A Columbus area-week with no row had **no qualifying ED visit** — an observation
of zero. Faking `NaN`s to look like Boston would discard real information.

So `load_counts()` fills with `0.0` and asserts no `NaN` survives. The
consequence is that `n_obs` in `metrics.csv` is not comparable across the two
cities, and neither is MAPE, which divides by an actual that can now be exactly
zero. Any cross-city table must footnote this.

### 6. MMWR week 53 is legitimate

An earlier pass flagged `IAH`'s MMWR 2025 week 53 as an impossible week. **That
was wrong.** MMWR week 1 is the first Sunday-to-Saturday week with at least four
days in the new year — equivalently, the week containing January 4 — which makes
some years 53 weeks long. 2025 is one:

```
MMWR 2025 week  1   2024-12-29 .. 2025-01-04    (CDC's published anchor)
MMWR 2025 week 52   2025-12-21 .. 2025-12-27
MMWR 2025 week 53   2025-12-28 .. 2026-01-03
MMWR 2026 week  1   2026-01-04 .. 2026-01-10
```

The weeks tile with no gap and no overlap, 2025-W53 is the only week-53 in the
file, and it falls in exactly the year that has one. It carries 56 real
hospitalisations. `mmwr_weeks_in_year()` computes each year's true length, and
`_read_line_level_weekly()` rejects only weeks past that length.

The doubled 2025 row count (1,544 against 2024's 709) is also signal: weekly
hospitalisations correlate **r = 0.815** with the weekly ILI series, and 2024-25
was Columbus's record season, peaking at 1,109 visits in the week of 2025-02-09.

### 7. COVID runs out 62% of the way through the evaluation window

The COVID extract's last observed week is **2025-10-19**. The evaluation window
is 2025-05-31 → 2026-05-31, so **33 of its 53 weeks have no COVID covariate at
all**, and there is no Columbus RSV data whatsoever.

Boston's single largest improvement is adding COVID and RSV co-circulation
(`gnn_multiedge` 24.5 → 16.8 RMSE, the most promising direction in the
repository). That arm has **no honest Columbus counterpart**.
`load_covid_counts()` therefore leaves the gap as `NaN` and does *not* carry the
last value forward — Boston's `_carry_forward()` covers a 17-week tail, which is
defensible; 33 weeks of a 53-week window is not.

### 8. The denominator is ours

Columbus case files carry no population. `load_rates()` divides counts by ACS
5-year ZCTA population aggregated to areas, from `scrape_acs_columbus.py`.

**The Census API no longer serves keyless requests** — it redirects to
`missing_key.html` — so a free key is required:

```bash
export CENSUS_API_KEY=...        # https://api.census.gov/data/key_signup.html
python Code/scrapers/scrape_gazetteer_columbus.py   # keyless: land area, centroids
python Code/scrapers/scrape_acs_columbus.py         # needs the key
```

Counts are summed per area **before** any ratio is taken, mirroring
`data.py::_load_city_csv`. A per-ZIP ratio averaged across an area would weight a
2,000-person ZIP the same as a 40,000-person one.

**ZCTAs cross the county line.** The 42 mapped ZCTAs span ~643 square miles
against Franklin County's ~540. That is nevertheless the right denominator: the
ILI extract counts "residents of a ZIP code classified as being in Franklin
County", so numerator and denominator cover the same population.

### 9. The crosswalk predates the data

`Columbus_FC_Zip_Areas_Nov2019.xlsx` is dated **November 2019** and the case data
begins 2022. Any ZIP boundary or area-definition change since then is invisible
to us.

## Geographic adjacency is measured, not hand-coded

Boston's 23 geographic edges are hand-coded from a map. The first Columbus
version was too, and then it was checked: **hand-coding got 34 of the 39 real
borders, invented 4 that do not exist, and missed 5 that do — 87% accurate.**
For a model whose entire premise is that the edges carry signal, that error rate
is not acceptable, so the edge list is now derived.

`Code/scrapers/derive_columbus_adjacency.py` pulls ZCTA polygons from the Census
**TIGERweb** REST service as GeoJSON (no API key) and computes adjacency in pure
Python. No new dependency: `geopandas`/`shapely` are absent from this project's
environment, but TIGER is topologically consistent — two polygons sharing a
border share the *identical* vertex coordinates — so two ZCTAs are adjacent
exactly when they share **at least two** boundary vertices. Two rather than one,
because a single shared vertex is a corner touch, not a border.

Result: **39 area-area borders and 9 area-anchor borders**, average degree 4.59
against Boston's 3.29. Higher because Franklin County is a contiguous inland
partition, whereas Boston's harbour and river cut real adjacencies out of its
map. `--compare` re-derives and diffs against the committed profile, so drift
fails loudly.

The four borders hand-coding invented were `Eastside–Linden`, `Eastside–West`,
`FarSE–NESub` and `FarSW–FarSouth`; the five it missed were `Agler–Clinton+`,
`Agler–Eastside`, `Bexley–FarSouth`, `Clinton+–FarSouth` and `FarSE–FarSW`.
Figure: `Code/results/columbus/_diagnostics/columbus_adjacency.png`.

## Anchor nodes

Boston's 7 anchors — Cambridge/Somerville, the Charles, the Harbor — are
hand-designed regions: feature-less boundary sinks so that edge neighborhoods do
not have their border treated as a wall.

Columbus's fall out of the data. The crosswalk lists **7 ZIPs it leaves
unassigned**, carrying 147 of 63,103 ILI rows (0.23%) — near-zero volume at the
reporting boundary, which is exactly the anchor role. **Five become anchors, one
per ZIP:**

| anchor | ZIP | borders |
|---|---|---|
| `Amlin` | 43002 | Dublin, Hilliard |
| `LewisCtr` | 43035 | Dublin, Worthington, Westerville |
| `W.Jeff` | 43140 | Far Southwest |
| `Orient` | 43146 | Far Southeast, Far Southwest |
| `Polaris` | 43240 | Westerville |

One anchor per ZIP rather than grouped by compass direction, which was an
earlier attempt and was wrong: **43146 (Orient) borders Far *Southeast* as well
as Far Southwest**, so filing it under "west suburbs" mis-wired it.

Two of the seven are deliberately **not** nodes:

- **43210, Ohio State's campus.** It borders Clintonville/Near North and
  UA/Grandview — it sits in the geographic *middle* of the city. It is unassigned
  because it is institutional (dormitories), not because it is peripheral, and an
  interior ZIP is not a boundary sink. Excluding it disconnects nothing:
  Clinton+ and UA/Grand border each other directly anyway.
- **43126, Harrisburg.** Shares no boundary with any of the 42 mapped ZIPs, so an
  anchor for it would be an isolated node carrying only a self-loop.

## What Columbus does not have

No pre-COVID history (the series starts 2022-01-01), so **only the `post_covid`
variant transfers**; `full` and `exclude_covid` are Boston-only. No wastewater,
no RSV, no vaccination series, no published transit adjacency, and no spatial
boundary file in the repo — the geographic edges are derived from a Census ZCTA
shapefile in Stage 3.

## Seasonality, for comparison with Boston

All figures below use `severity.citywide_series()` — the unweighted mean across
nodes, matching the `macro` scope — so the two cities are measured by the same
function on the same definition.

| | Boston (post-COVID) | Columbus |
|---|---|---|
| citywide mean rate | 25.1 per 100,000 | 17.9 per 100,000 |
| per-node mean range | 8.70 (Fenway) → 63.44 (Dorchester), **7.3x** | 3.67 (UA/Grandview) → 40.08 (Far East), **10.9x** |
| annual floor | Jul–Aug | Jun–Jul |
| mean temp vs week-of-year | R² = 0.93 | R² = 0.878 |

**The premise holds at least as strongly in Columbus.** This project exists
because "citywide forecasts are the wrong unit for public health action" — the
sub-city units do not move together. Columbus's 10.9x spread across areas is
*wider* than Boston's 7.3x, so there is at least as much for a graph to exploit.

Note that count and rate rank areas differently. Bexley averages only 3.1 visits
a week but 10.88 per 100,000 (population 28,431), while UA/Grandview averages 3.2
visits and just 3.67 per 100,000 (population 87,844). Read the per-area tables
with the denominator in view.

### Peak timing is synchronised between the cities

An earlier draft of these notes claimed Columbus's peak timing was "far more
variable than Boston's" and predicted `seasonal_naive` would therefore do worse
there. **That was wrong.** Peak timing varies a great deal from season to season
— but it does so almost identically in both cities:

| season | Boston peak | Columbus peak | Boston / Columbus amplitude |
|---|---|---|---|
| 2022-23 | 106.2 on **2022-12-04** | 44.9 on **2022-11-27** | 0.42 |
| 2023-24 | 63.4 on **2023-12-24** | 44.7 on **2023-12-24** | 0.71 |
| 2024-25 | 127.2 on **2025-02-02** | 75.8 on **2025-02-09** | 0.60 |
| 2025-26 | 101.9 on **2025-12-21** | 52.2 on **2025-12-21** | 0.51 |

Peaks land **within one week of each other in all four shared seasons**, and in
two of the four on the identical week. Columbus is a lower-amplitude version of
the same national curve, at roughly half to three-quarters the peak rate.

Two consequences, and the second is uncomfortable:

- `seasonal_naive` should fail in Columbus for the *same* reason and to a
  *similar* degree as in Boston, not worse. Any prediction to the contrary was
  unfounded.
- **This sharpens the limitation rather than the finding.** The two cities share a
  common national driver, so agreement between them is weaker evidence than two
  genuinely independent replications would be. If the model ordering reproduces
  in Columbus, that is real but partly expected; if it *fails* to reproduce
  despite this much synchrony, that is the more informative outcome.

The June–July floor does confirm `severity.season_label`'s August season boundary
is defensible for Columbus, though August already averages 156.7 visits/week and
so sits slightly on the rising limb.

## The feature spaces are not on the same scale

The eight static features are min-max normalised **within each city**, by
`load_static_demographics()` in both loaders. That is the same method, but it has
a consequence for the demographic-similarity edge type that the cross-city
comparison has to state:

| raw feature | Boston range | Columbus range |
|---|---|---|
| `transit_share` | 0.128 – 0.433 | **0.002 – 0.047** |
| `pop_density` | 6,112 – 185,247 /sq mi | **734 – 6,353** /sq mi |
| `poverty_rate` | 0.067 – 0.353 | 0.049 – 0.266 |

Columbus is a car-dependent city: its highest-transit area (Linden, 4.7%) is
below Boston's *lowest* (12.8%), and its densest area is thinner than Boston's
sparsest. Min-max normalisation then stretches Columbus's 4.5-percentage-point
transit spread to fill [0, 1] exactly as it does Boston's 30-point spread, and
`build_graph`'s Gaussian kernel — whose bandwidth is the median of the pairwise
distances in that normalised space — treats them as equivalent.

So Columbus's demographic-similarity edges are partly built on amplified
near-noise in two of the eight columns. Keeping per-city normalisation is still
right (a shared scale across two different geographies would be meaningless), but
the `gnn_multiedge` comparison should carry this caveat, and a demo-edge ablation
on the Columbus side is worth running.

The same reasoning applies with more force to the transit edge type itself: COTA
carries a far smaller share of trips than the MBTA, so a Columbus transit
adjacency is a weaker mobility proxy even when correctly built.
