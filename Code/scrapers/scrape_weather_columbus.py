"""Fetch weekly weather for each of the 17 Columbus areas.

Deliberately thin: it imports `fetch_daily_weather` and `aggregate_to_weekly`
from scrape_weather.py rather than reimplementing them, so both cities'
weather is fetched from the same Open-Meteo endpoint, aggregated with the same
rules, and written with the same six column names. A second copy of that logic
would be the fork-and-drift failure this project has already been through once.

Only three things differ from Boston: the coordinates (read from
columbus_area_geography.csv instead of hand-typed), the start date (the Columbus
ILI series begins 2022-01-01, not 2017-12-31), and the output directory.

Output: Data/Columbus Weather/<area_slug>_weather_weekly.csv (one per area)

    python Code/scrapers/scrape_gazetteer_columbus.py   # centroids first
    python Code/scrapers/scrape_weather_columbus.py
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths
from influenza.loaders.columbus import area_slug

# scrape_weather.py is a script, not a module in a package, so it is loaded by
# path rather than imported by name.
_spec = importlib.util.spec_from_file_location(
    "scrape_weather", Path(__file__).resolve().parent / "scrape_weather.py")
_boston_weather = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_boston_weather)

fetch_daily_weather = _boston_weather.fetch_daily_weather

# One week before the first full Columbus ILI week (2022-01-02), so the first
# Sunday-start week has all seven days of data.
START_DATE = "2021-12-20"
GEOGRAPHY_FILE = "columbus_area_geography.csv"
REQUEST_DELAY = 5  # seconds between areas, to stay under Open-Meteo's rate limit


def aggregate_to_weekly(daily: pd.DataFrame, first_week: str) -> pd.DataFrame:
    """Reuse Boston's aggregation, then trim to Columbus's first full week.

    Boston's version hardcodes its own 2017-12-31 start in the final trim, so
    only that one line is redone here.
    """
    weekly = _boston_weather.aggregate_to_weekly(daily)
    return weekly.loc[weekly.index >= first_week]


def load_centroids() -> pd.DataFrame:
    path = paths.COLUMBUS_DIR / GEOGRAPHY_FILE
    if not path.exists():
        raise SystemExit(
            f"{path} not found.\n\n"
            "Area centroids come from the keyless geography scraper:\n\n"
            "    python Code/scrapers/scrape_gazetteer_columbus.py\n")
    return pd.read_csv(path, comment="#", index_col=0)[["lat", "lon"]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=paths.COLUMBUS_WEATHER_DIR)
    parser.add_argument("--first-week", default="2022-01-02",
                        help="Drop weeks before this; the first full ILI week.")
    args = parser.parse_args()

    centroids = load_centroids()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    end_date = (date.today() - timedelta(days=1)).isoformat()
    print(f"Fetching weather for {len(centroids)} Columbus areas "
          f"({START_DATE} to {end_date})\n")

    written = 0
    for i, (area, row) in enumerate(centroids.iterrows()):
        out_path = args.output_dir / f"{area_slug(area)}_weather_weekly.csv"
        if out_path.exists():
            print(f"{area} - already exists, skipping")
            continue
        if i > 0:
            time.sleep(REQUEST_DELAY)

        print(f"{area} ({row.lat:.4f}, {row.lon:.4f})...")
        # The shared fetcher reads its window from module-level constants.
        _boston_weather.START_DATE = START_DATE
        _boston_weather.END_DATE = end_date
        daily = fetch_daily_weather(row.lat, row.lon)
        weekly = aggregate_to_weekly(daily, args.first_week)
        weekly.to_csv(out_path)
        written += 1
        print(f"  {len(weekly)} weeks -> {out_path.name}")

    print(f"\nDone. {written} new of {len(centroids)} areas in "
          f"{paths.display(args.output_dir, paths.ROOT)}")


if __name__ == "__main__":
    main()
