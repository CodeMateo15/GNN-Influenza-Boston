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
| `code/` | Four short scripts that run the weekly steps (see [Run it every week](#run-it-every-week)) |

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

All three models retrain from scratch every week on every week of data BPHC has
published since 2018.

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
2. Train + forecast             live_forecast.py         (about 4 CPU-hours: ~1 hour per
        │                                                 week ahead; can run in parallel)
        ▼
3. Tables + figures             make_bphc.py             (seconds, any computer)
```

**Set up once** (Python 3.10 or newer):

```bash
cd code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

This installs the forecasting models from PyPI
([areaFluForecast](https://pypi.org/project/areaFluForecast/) 1.1.0, pinned so
results don't change under you).

**Each week:**

```bash
# 1. Download "Influenza Neighborhood" from the BPHC dashboard, then:
python bphc_export_to_city.py --export "BPHC Dashboard Influenza Neighborhood.csv" --out live/boston

# 2. Train and forecast. Archives the forecast under live/<season>/boston/<week>/.
#    The first run also backtests 3 past seasons (about 12 CPU-hours, once).
python live_forecast.py run --city boston --models gnn_st lstm arima

# 3. Build this folder's tables and figures from that week's forecast
python make_bphc.py --origin live/2026_27/boston/<week> --out ..
```

`make_bphc.py --add-forecast FILE` adds models that an archived forecast
lacks, if they were made later from the same data. The current folder used it
once: the 2026-09-27 forecast predates ARIMA, so ARIMA's rows for that week
were made afterwards from that week's exact data. `forecast_info.json` records
this. New weeks include all three models and don't need it.

To check step 2 end to end before a long run, set `AREAFLU_QUICK=1`. This makes
every model tiny; the numbers are meaningless but every file gets written.

## Put it in your reporting pipeline

- **If you only display our forecasts,** you need step 3 and
  `requirements-report.txt` (numpy, pandas, matplotlib), nothing else. Point
  `--origin` at an archived forecast folder.
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
  after a forecast is made.
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
