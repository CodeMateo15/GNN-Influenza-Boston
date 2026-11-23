# Boston flu forecast — BPHC folder

Weekly forecasts of flu-like illness in Boston, by neighborhood and citywide,
1 and 2 weeks ahead, from three models and their average. This folder holds the
latest forecast, how accurate past forecasts were, and the code that makes them,
set up so it can be dropped into a reporting pipeline.

| File | What it is |
|---|---|
| `forecast_2week.csv` | The forecast: 14 neighborhoods + Citywide × 4 models × 1–2 weeks ahead |
| `observed.csv` | The observed weekly rates the forecast started from (with a Citywide row) |
| `accuracy.csv` | How close past forecasts came, by model and weeks ahead |
| `forecast_info.json` | Forecast date, unit, models, and any notes from the last build |
| `figures/citywide_forecast.png` | Citywide forecast, one panel per model |
| `figures/neighborhoods_forecast.png` | GNN forecast for each neighborhood |
| `code/` | Short scripts that run the weekly steps (see [Run it every week](#run-it-every-week)) and make the [offline website](#offline-website) |

## What the numbers mean

**Unit:** flu-like illness (ILI) emergency-department visits per 100,000
residents, per week. This is the rate BPHC publishes on its dashboard. It is
not a count of flu cases.

Each forecast row gives five numbers for one neighborhood, one model and one
target week:

| Column | Plain meaning |
|---|---|
| `estimate` | The single best guess (the middle of the forecast) |
| `low50`, `high50` | The **likely range**: the real value should land inside about 1 week in 2 |
| `low95`, `high95` | The **wide range**: the real value should land inside about 19 weeks in 20 |

The ranges always nest: `low95 ≤ low50 ≤ estimate ≤ high50 ≤ high95`. A wide
range means the model is unsure. Ranges are widest at the start of a season,
when rates can turn quickly.

## The models

- **ARIMA** is a classic statistical forecast. It fits each neighborhood on its
  own, from that neighborhood's recent weeks and the usual time of year.
- **LSTM** is a neural network that learns from all neighborhoods' recent weeks
  together.
- **GNN** (graph neural network) is a neural network that also knows which
  neighborhoods border each other and which neighboring towns sit at the city's
  edge. It is built to catch flu moving from one area to the next.
- **Average** gives the three models equal weight, range by range. The average
  estimate is the mean of the three estimates, the average `low95` is the mean
  of the three `low95` values, and so on.
  - It's included because one model can run high while another runs low, and
    then the middle is closer to the truth. That doesn't always happen.
    `accuracy.csv` shows whether it did.

The GNN and LSTM are trained once a season, on every week of data BPHC has
published since 2018 up to the season start (June 1), and saved in `models/`;
each week they are loaded and fed that week's data. ARIMA's settings (which
lags and trends each neighborhood's model uses) are chosen at the same time and
saved too; each week it refits with those settings on every week up to the
newest. This is how the accuracy in `accuracy.csv` was measured (one model per
past season, trained before it opened), and loading the saved models gives the
forecast that retraining them from the season start would.

## How "Citywide" is calculated

Citywide is the **simple average of the 14 neighborhoods' rates**, with each
neighborhood counting equally, so Fenway counts as much as Dorchester. The
citywide ranges are averaged the same way: citywide `low95` is the mean of the
neighborhoods' `low95`.

- **Why equal weights:** BPHC's export has no weekly population for each
  neighborhood, so a population-weighted rate can't be computed from it.
- **Why the ranges can be averaged:** neighborhoods tend to rise and fall
  together, so averaging their ranges gives an honest citywide range. Treating
  them as independent would make the range look far more certain than the
  models are.
- **Two-part neighborhoods:** BPHC publishes Dorchester as two ZIP groups. The
  model's Dorchester is their average.

This is not BPHC's own citywide figure, if one is published. Compare trends,
not levels.

## How accurate it has been

`accuracy.csv` answers "how far off were the forecasts, and how often did the
ranges catch the real value?" It does that for each model, each number of weeks
ahead, neighborhoods vs citywide, and each season.

| Column | Question it answers |
|---|---|
| `source` | `backtest`: past seasons, forecast as if live using only data available at the time. `live`: this season's real forecasts, once their target week is observed. |
| `season` | Which flu season; `all` pools them |
| `scope` | `neighborhoods` (every neighborhood-week) or `citywide` |
| `n_forecasts` | How many forecasts the row is based on |
| `avg_error` | On average, how far the estimate was from the real rate (same unit as the forecast) |
| `wis` | One overall score of how good the whole forecast was, estimate and ranges together. Lower is better. |
| `wis_vs_last_week` | That score compared with the simplest guess, "next week looks like this week". **Below 1 means the model beat that guess**; 0.75 means 25% better. |
| `in_95_range`, `in_50_range` | How often the real value fell inside the wide / likely range (aim: 0.95 and 0.50) |

The `wis` score is the weighted interval score that the CDC's FluSight
forecasting challenge uses.

The "Same as last week" rows are that simple guess, kept as the yardstick.

**In the last three seasons (2023-24 to 2025-26),** each model was forecast as
if live, using only data available at the time. Rows are neighborhood-weeks
(2,063 per column).

| | Off by, on average (1 wk / 2 wk) | Score vs "same as last week" (1 wk / 2 wk) | Wide range caught it (1 wk / 2 wk) |
|---|---|---|---|
| GNN | 7.1 / 8.6 | 0.77 / 0.73 | 95% / 93% |
| Average | 7.4 / 9.0 | 0.81 / 0.78 | 95% / 93% |
| LSTM | 7.5 / 9.7 | 0.82 / 0.84 | 96% / 92% |
| ARIMA | 9.0 / 10.5 | 1.02 / 0.92 | 93% / 92% |
| Same as last week | 9.1 / 11.6 | 1.00 / 1.00 | 94% / 94% |

- **GNN was the most accurate at both 1 and 2 weeks ahead:** 23% and 27%
  better than "same as last week".
- **The Average came second, not first.** ARIMA, the weakest model, pulls it
  toward ARIMA's misses more often than the three models' errors cancel out.
- **ARIMA alone was no better than "same as last week" at 1 week ahead.**
- **The wide ranges were about right,** catching the real value about 19 times
  in 20.
- **Citywide likely ranges are deliberately cautious.** They caught the real
  value 74–85% of the time, against an aim of 50%. Averaging neighborhood ranges
  errs on the wide side.

## Output columns

These names and orders don't change from week to week, so a pipeline can depend
on them.

`forecast_2week.csv`, one row per target week × area × model:

```
origin_date, target_date, weeks_ahead, area, model, estimate, low95, low50, high50, high95
```

- `origin_date` is the last observed week the forecast starts from.
- `target_date` is the week being forecast.
- Weeks are dated by their Sunday start, as on the BPHC dashboard.
- `area` is one of the 14 neighborhoods or `Citywide`.
- `model` is `ARIMA`, `LSTM`, `GNN` or `Average`.

`observed.csv`: `week, area, rate`. Weeks BPHC didn't report (small counts are
suppressed) are left out. They are not zeros.

`accuracy.csv`: `source, season, weeks_ahead, scope, model, n_forecasts,
avg_error, wis, wis_vs_last_week, in_95_range, in_50_range`.

All files are long ("tidy") CSV, one fact per row, which Power BI, Tableau, R or
Excel read directly.

## Run it every week

There are three steps. Only the middle one is heavy.

```
1. BPHC dashboard export        bphc_export_to_city.py   (seconds, any computer)
        │
2. Forecast                     live_forecast.py         (a few minutes with the
        │                                                 saved models in models/)
        ▼
3. Tables + figures             make_bphc.py             (seconds, any computer)
```

**Set up once** (Python 3.10 or newer):

ALSO NOTE, use this if still in (.venv):
```bash
deactivate
```

If all is working, then:
```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

This installs the forecasting models from PyPI
([areaFluForecast](https://pypi.org/project/areaFluForecast/) 1.3.0, which
loads the saved LSTM and ARIMA as well as the GNN). If `.venv` was set up
earlier with 1.2.0, run `pip install -r requirements.txt` again inside it.

### Each week

**Run every command from `code/`,** with the virtual environment active. The
steps pass files to each other through `code/live/`, and every path below is
relative to `code/`. Run step 1 from one folder and step 2 from another, and
step 2 won't find step 1's output.

```
code/live/boston/                   step 1 writes it; step 2 reads it
code/live/2026_27/boston/<week>/    step 2 writes it; steps 3 and 4 read it
code/live/runs/boston/              the past-season backtest, shipped in this folder; step 2 reuses it
```

**Step 1: turn the dashboard export into model input** (seconds)

Download "Influenza Neighborhood" from the BPHC dashboard (save it anywhere, but change /path/to), then:

```bash
python bphc_export_to_city.py --export "/path/to/BPHC Dashboard Confirmed Influenza Cases and ILI Emergency Department (ED) Visits - Neighborhood.csv" --out live/boston
```

- **Reads** the export CSV.
- **Writes** `live/boston/`: the weekly rates (`rates.csv`), the neighborhood
  map and borders (`city.json`, `centroids.csv`, `edges.csv`) and the weather
  (`weather.csv`).
- **Needs internet** to download the weather from Open-Meteo.
- Run it **every week, before step 2**. Step 2 forecasts from whatever is in
  `live/boston/`, so skipping this step forecasts last week's data again.

**Step 2: forecast** (a few minutes)

```bash
python live_forecast.py run --city boston --models gnn_st lstm arima \
    --models-dir ../models/2026_27/boston
```

- **Reads** `live/boston/` (from step 1) and `../models/2026_27/boston/` (this
  season's saved GNN, LSTM and ARIMA settings, shipped in this folder). Each
  model prints `... wk: 23.6s (loaded)`.
- **Writes** `live/2026_27/boston/<week>/`, one folder per forecast, named by the
  newest week in the data (for example `2026-11-08`). The last line it prints,
  `Outputs: ...`, is that folder.
- **Reuses the backtest** in `live/runs/boston/backtest_20261013-arima/`: our
  replay of the 2023-24 to 2025-26 seasons, which gives the "past-season check"
  badges and the backtest rows of `accuracy.csv`. It must say
  `Reusing backtest live/runs/boston/backtest_20261013-arima` near the start. If
  it says `Backtesting seasons [2023, 2024, 2025]` instead, the folder is missing
  (for example, not copied to this computer): stop it with Ctrl-C and copy the
  folder in. Otherwise it recomputes the backtest, about 12-17 CPU-hours.
- `--jobs 2` forecasts two weeks-ahead at a time if 2 or more cores are free
  (same numbers, about half the time).
- Before a long run, set `AREAFLU_QUICK=1` to check that everything runs end to
  end: every model is made tiny, so the numbers are meaningless but every file
  gets written. Then delete `live/2026_27/` before the real run, or the real
  run refuses to overwrite the quick forecast's week folder. Don't delete
  `live/runs/`: that would remove the shipped backtest.

**Step 3: this folder's tables and figures** (seconds)

```bash
python make_bphc.py --origin live/2026_27/boston/<week> --out ..
```

- **Reads** the folder step 2 wrote (`<week>` is its name), plus earlier weeks
  beside it for the live accuracy.
- **Writes** into the BPHC folder (`..`): `forecast_2week.csv`, `observed.csv`,
  `accuracy.csv`, `forecast_info.json` and `figures/`.

**Step 4 (optional): the website as one offline HTML file** (seconds; see
[Offline website](#offline-website))

```bash
python make_site.py --origin live/2026_27/boston/<week> --out ../boston_flu_outlook.html
```

- **Reads** the same folder as step 3.
- **Writes** one `.html` file.

### Common errors

| Message | What it means | Fix |
|---|---|---|
| `No city data in live/boston/ (no city.json)`, or in older copies `FileNotFoundError: ... 'live/boston/city.json'` | Step 2 can't find step 1's output: step 1 hasn't been run yet, or it was run from another folder or with a different `--out` | Run step 1 from `code/` with `--out live/boston`, then step 2 from `code/` |
| `../models/2026_27/boston/manifest.json not found` | Step 2 was run from a folder other than `code/`, so `../models/...` points somewhere else | `cd` into `code/` and run it again |
| `... holds boston 2026_27 models, but this forecast is boston 2027_28` | The data has reached a new season; the saved models are for the last one | Ask us for the new `models/<season>/` folder, or see "Once a season" below |
| `live/2026_27/boston/<week> exists. Archived forecasts are never overwritten` | That week was already forecast. Usually step 1 wasn't re-run with the new export. The check comes at the end of step 2, so the run's time is spent first | Download the new export, re-run step 1, then step 2 |
| Step 1 stops while fetching the weather | The computer can't reach Open-Meteo | Run step 1 on a computer with internet access, then copy `live/boston/` across |
| `DataError: The weekly rates before 2026-06-01 differ from the ones ../models/2026_27/boston/gnn_st_h1.pt was trained on` | BPHC revised an old week, and `live_forecast.py` or `models/2026_27/boston/pinned_rates.csv` is an older copy without the fix | Copy both from this folder and run step 2 again |
| Step 2 shows `2wk arima <neighborhood>` lines a minute or more apart, and an hour or more left | ARIMA is searching for its settings because the saved ones weren't loaded: an older `live_forecast.py`, or `models/2026_27/boston/` without the `arima_h*.pt` files | Copy `code/live_forecast.py` and `models/2026_27/boston/` from this folder, run `pip install -r requirements.txt`, run step 2 again |
| `ImportError: cannot import name 'is_freezable'` | `.venv` still has areaFluForecast 1.2.0 | `pip install -r requirements.txt`, then run step 2 again |
| `../models/2026_27/boston is missing ['arima_h1.pt', ...]` | The `models/` folder is an older copy that holds only the GNN | Copy `models/2026_27/boston/` from this folder |
| Step 2 prints `Backtesting seasons [2023, 2024, 2025]` and estimates many hours left | The shipped backtest isn't in `live/runs/boston/` | Ctrl-C, copy `code/live/runs/boston/backtest_20261013-arima/` from this folder, run again |
| `make_bphc: missing input ...` or `make_site: missing input ...` | `--origin` doesn't point at a folder step 2 wrote | Use the folder on step 2's `Outputs:` line |

### Other options

`make_bphc.py --add-forecast FILE` adds models that an archived forecast
lacks, if they were made later from the same data. The current folder used it
once: the 2026-09-27 forecast predates ARIMA, so ARIMA's rows for that week
were made afterwards from that week's exact data. `forecast_info.json` records
this. New weeks include all three models and don't need it.

**Once a season** (we normally do this and send you the new `models/<season>/`
folder; it is about 2.5 CPU-hours):

```bash
python live_forecast.py train --city boston --models gnn_st lstm arima --out ../models/2026_27/boston
```

`--models lstm arima` adds those to a folder that already holds the GNN.

Step 2 stops with a message, rather than quietly retraining, if the saved models
are for another season or are missing a week ahead. Leave out `--models-dir` to
retrain every model every week instead (about 4 CPU-hours).

**When BPHC revises old weeks.** `models/<season>/boston/pinned_rates.csv` holds
the weeks before the season start exactly as the saved models learned them. Step 2
uses those, not the new export, for every week before the season start. It
lists any old week the export changed (`The export revised 1 rate(s) before
2026-06-01; keeping ...`) and carries on. Every week from the season start on
comes from the new export, revisions included, so each new export just adds its
new week. Without that file, any revision to an old week stops step 2 with
`The weekly rates before 2026-06-01 differ from the ones ... was trained on`.
`train` writes the file each season.

## Offline website

`make_site.py` writes the whole [Boston Flu Outlook](https://codemateo15-boston-flu-outlook.share.connect.posit.cloud/)
site as **one HTML file**, from the same archived forecast folder step 3 reads:

```bash
python make_site.py --origin live/2026_27/boston/<week> --out ../boston_flu_outlook.html
python make_site.py --origin live/2026_27/boston --out ../boston_flu_outlook.html   # newest week
```

- **Private and offline.** Open the file in any browser (Chrome, Edge, Firefox,
  Safari). It needs no internet connection and no server, loads nothing from
  anywhere, and sends nothing anywhere. It can sit on a shared drive or go out as an
  email attachment like any other file.
- **What's in it:** every tab of the public site for Boston (This week with the
  map you can step through, Neighborhood, Severity, All neighborhoods, Track record,
  How it works), both the briefing and analyst views, dark mode, and the forecast
  and FluSight CSV downloads.
- **What's left out:** the Chicago tab (this folder forecasts Boston only) and
  "What's driving it" (it needs a step this folder's `live_forecast.py` doesn't
  run). On the Neighborhood tab, unticking a model hides its line rather than
  redrawing the chart, so the scale fits every model.
- **It is a snapshot.** It shows the week it was made from and doesn't update; make
  a new one after each weekly forecast. It takes a few seconds and is about 3 MB.
- **Needs** `requirements-report.txt` (numpy, pandas, shiny). No PyTorch.
- The site's code is a copy in `code/outlook/`, kept in step with the public site;
  don't edit it there. A missing or incomplete forecast folder exits with status 2
  and a plain message, as `make_bphc.py` does.

## Put it in your reporting pipeline

- **If you only display our forecasts,** you need step 3 and
  `requirements-report.txt` (numpy, pandas, matplotlib, and shiny for the offline
  website), nothing else. Point `--origin` at an archived forecast folder.
- **If you make the forecasts yourself,** step 2 needs the full
  `requirements.txt` (PyTorch etc.). No GPU is needed.
- **Paths:** every path is a command-line argument; nothing points at our
  machines.
- **Failures:** a missing input or model exits with status 2 and a
  plain-English message, so a scheduler can tell when a week failed. From
  Python, it raises `make_bphc.InputError`.

Use it from Python instead of the command line:

```python
import sys; sys.path.insert(0, "path/to/BPHC/code")
import make_bphc

tables = make_bphc.build("live/2026_27/boston/2026-10-11")
forecast = tables["forecast"]                       # pandas DataFrame, columns above
city = forecast[forecast["area"] == "Citywide"]
make_bphc.write(tables, "out/", figures=False)      # or skip files and use the frames
```

`build()` returns `forecast`, `observed`, `accuracy` (DataFrames) and `meta`.
`meta` is a dict with the forecast date, the unit, and any notes, such as "no
live forecast has reached its target week yet".

## Things to know

- **BPHC revises past weeks.** About 0.6% of past neighborhood-weeks changed
  between two exports this year. Recent observed numbers can shift a little
  after a forecast is made. Revisions to weeks before the season start are
  ignored (see "When BPHC revises old weeks").
- **Suppressed weeks.** When a neighborhood has very few visits, BPHC leaves the
  week blank. The models treat it as unknown, not zero, and it is never scored.
- **Early season.** The first weeks of a season are low and noisy, so ranges are
  wide relative to the estimate. That's expected.
- These are research forecasts to support judgement, not replace it.

## Credit

The models are the `areaFluForecast` package by Mateo Biggs (Northeastern
University), MIT licence: [source code](https://github.com/CodeMateo15/areaFluForecast).
Cite it with DOI [10.5281/zenodo.23327109](https://doi.org/10.5281/zenodo.23327109).
`code/live_forecast.py` is a standalone copy of the package's weekly script.

Data: Boston Public Health Commission dashboard. Weather: Open-Meteo.
