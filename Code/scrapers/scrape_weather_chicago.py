"""Fetch weekly weather for each Chicago ZIP.

    python Code/scrapers/scrape_weather_chicago.py            # fetch missing files only
    python Code/scrapers/scrape_weather_chicago.py --refresh  # append weeks through yesterday

Thin for the same reason scrape_weather_buenos_aires.py is: `fetch_daily_weather`
and `aggregate_to_weekly` come from scrape_weather.py, so every city's weather
uses the same endpoint, the same Sunday-week rules and the same six column
names. (That includes the shared fetcher's America/New_York day boundary, an
hour off Chicago's; for daily means and sums over a week it is immaterial, and
a second copy of the fetcher would be the bigger risk.)

One thing is new, and it is forced by scale. Open-Meteo bills a long request
as many calls -- seven years of daily data is on the order of a hundred -- and
59 ZIPs at that weight would exhaust the free hourly quota and approach the
daily one. But the archive is gridded, and Chicago's 59 ZIP centroids fall in
only 12 grid cells, so 47 of those requests would be byte-identical repeats.
So the scraper first asks the API which cell each ZIP snaps to (a one-day,
one-variable request), fetches each cell once, and writes one file per ZIP.
Identical output to a per-ZIP pull -- checked directly on two cells -- at a
fifth of the quota. It also means Chicago's weather varies across only 12
distinct series, which is worth knowing before reading anything into it.

Files are written for all 59 ZIPs with a polygon, the anchor included; the
loader skips anchor files.

--refresh is append-only exactly as in scrape_weather.py: past weeks are never
rewritten (Open-Meteo revises its archive by small rounding amounts, and a
backtest must keep seeing the weather it was run on); only the old last week
and newer weeks come from the new download.

Output: Data/Chicago Weather/<zip>_weather_weekly.csv
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
import time
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "scrape_weather", Path(__file__).resolve().parent / "scrape_weather.py")
_boston_weather = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_boston_weather)

fetch_daily_weather = _boston_weather.fetch_daily_weather

# One week before the first panel week (2019-09-29), so it has all seven days.
START_DATE = "2019-09-22"
FIRST_WEEK = "2019-09-29"
REQUEST_DELAY = 5     # seconds between full-range requests
PROBE_DELAY = 0.5     # the cell probes are one-day, single-variable calls


def zip_centroids() -> dict[str, tuple[float, float]]:
    """ZIP -> (lat, lon), for every ZIP with a polygon (anchor included)."""
    path = paths.require(paths.CHICAGO_CENTROIDS_FILE, "Chicago ZIP centroids")
    with open(path, newline="") as handle:
        rows = csv.DictReader(line for line in handle if not line.startswith("#"))
        return {row["zip"]: (float(row["lat"]), float(row["lon"])) for row in rows}


def grid_cell(lat: float, lon: float) -> tuple[float, float]:
    """The archive grid point Open-Meteo snaps (lat, lon) to."""
    params = {"latitude": lat, "longitude": lon, "start_date": START_DATE,
              "end_date": START_DATE, "daily": "temperature_2m_mean",
              "timezone": "America/New_York"}
    for attempt in range(1, _boston_weather.MAX_RETRIES + 1):
        try:
            response = requests.get(_boston_weather.API_URL, params=params, timeout=60)
            response.raise_for_status()
            payload = response.json()
            return float(payload["latitude"]), float(payload["longitude"])
        except (requests.RequestException, ValueError, KeyError) as error:
            if attempt == _boston_weather.MAX_RETRIES:
                raise RuntimeError(f"cell probe failed for ({lat}, {lon}): {error}") from error
            time.sleep(_boston_weather.BACKOFF_BASE ** attempt)
    raise AssertionError("unreachable")


def aggregate_to_weekly(daily: pd.DataFrame, first_week: str) -> pd.DataFrame:
    """The shared aggregation, re-trimmed to the first full Chicago week."""
    weekly = _boston_weather.aggregate_to_weekly(daily)
    return weekly.loc[weekly.index >= first_week]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=paths.CHICAGO_WEATHER_DIR)
    parser.add_argument("--first-week", default=FIRST_WEEK,
                        help="Drop weeks before this; the first panel week.")
    parser.add_argument("--refresh", action="store_true",
                        help="append new weeks to files that already exist, unless "
                             "already written today (so a rate-limited run can resume)")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    end_date = (date.today() - timedelta(days=1)).isoformat()
    centroids = zip_centroids()

    def done(zip_code: str) -> bool:
        out = args.output_dir / f"{zip_code}_weather_weekly.csv"
        return out.exists() and (not args.refresh or
                                 date.fromtimestamp(out.stat().st_mtime) == date.today())

    todo = [z for z in sorted(centroids) if not done(z)]
    print(f"Weather for {len(centroids)} Chicago ZIPs ({START_DATE} to {end_date}); "
          f"{len(centroids) - len(todo)} already done\n")
    # Budget in ZIPs; see the status-line contract in run_progress.py.
    print(f"Budget: {len(centroids)} epochs x 1 seeds", flush=True)
    print("--- seed weather (1/1) ---", flush=True)
    finished = len(centroids) - len(todo)
    for z in sorted(set(centroids) - set(todo)):
        print(f"Epoch {sorted(centroids).index(z) + 1} | {z} - already done, skipping",
              flush=True)

    cells: dict[tuple[float, float], list[str]] = defaultdict(list)
    for z in todo:
        cells[grid_cell(*centroids[z])].append(z)
        time.sleep(PROBE_DELAY)
    print(f"{len(todo)} ZIPs fall in {len(cells)} grid cells", flush=True)

    # The shared fetcher reads its window from module-level constants.
    _boston_weather.START_DATE = START_DATE
    _boston_weather.END_DATE = end_date
    for k, ((lat, lon), members) in enumerate(sorted(cells.items())):
        if k > 0:
            time.sleep(REQUEST_DELAY)
        weekly = aggregate_to_weekly(fetch_daily_weather(lat, lon), args.first_week)
        for z in members:
            out_path = args.output_dir / f"{z}_weather_weekly.csv"
            frame = weekly
            if args.refresh and out_path.exists():
                old = pd.read_csv(out_path, index_col="week_start", parse_dates=True)
                frame = pd.concat([old.iloc[:-1], weekly.loc[weekly.index >= old.index[-1]]])
            frame.to_csv(out_path)
            finished += 1
            print(f"Epoch {finished} | {z} cell ({lat:.4f}, {lon:.4f}) "
                  f"{len(frame)} weeks -> {out_path.name}", flush=True)

    print(f"\n{len(todo)} written of {len(centroids)} ZIPs")
    print(f"Outputs: {paths.display(args.output_dir, paths.ROOT)}", flush=True)


if __name__ == "__main__":
    main()
