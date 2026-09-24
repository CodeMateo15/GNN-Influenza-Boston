"""Fetch weekly weather for each of the 19 scored AMBA partidos.

Deliberately thin, for the same reason scrape_weather_columbus.py is: it
imports `fetch_daily_weather` and `aggregate_to_weekly` from scrape_weather.py
rather than reimplementing them, so all three cities' weather comes from the
same Open-Meteo endpoint, is aggregated with the same rules, and is written
with the same six column names. A third copy of that logic would be the
fork-and-drift failure this repository has already been through once.

Three things differ from Columbus: the coordinates (partido centroids from the
Argentine government's georef API, already committed in
cities/buenos_aires.py), the start date, and the output directory.

One thing does NOT differ and is worth saying out loud: the six WEATHER_COLS
are the same, and they mean the same thing. Buenos Aires is in the Southern
Hemisphere, so its temperature series runs in antiphase to Boston's -- cold in
June, warm in December. Nothing here corrects for that, and nothing should:
the model reads weather per city, and `influenza/climatology.py` fits a
phase-free day-of-year harmonic. Flipping the calendar would be inventing a
transformation neither needs.

Output: Data/Buenos Aires Weather/<partido_slug>_weather_weekly.csv

    python Code/scrapers/scrape_weather_buenos_aires.py
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

from influenza import paths  # noqa: E402
from influenza.cities.buenos_aires import COORDS, PARTIDOS, SHORT_OF  # noqa: E402
from influenza.loaders.buenos_aires import partido_slug  # noqa: E402

# scrape_weather.py is a script, not a module in a package, so it is loaded by
# path rather than imported by name.
_spec = importlib.util.spec_from_file_location(
    "scrape_weather", Path(__file__).resolve().parent / "scrape_weather.py")
_boston_weather = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_boston_weather)

fetch_daily_weather = _boston_weather.fetch_daily_weather

# One week before the first full AMBA ETI week (2022-01-02), so that week has
# all seven days behind it.
START_DATE = "2021-12-19"
FIRST_WEEK = "2022-01-02"
REQUEST_DELAY = 5  # seconds between partidos, to stay under Open-Meteo's limit


def aggregate_to_weekly(daily: pd.DataFrame, first_week: str) -> pd.DataFrame:
    """Reuse the shared aggregation, then trim to the first full AMBA week.

    Boston's version hardcodes its own 2017-12-31 start in the final trim, so
    only that one line is redone here -- the same seam Columbus uses.
    """
    weekly = _boston_weather.aggregate_to_weekly(daily)
    return weekly.loc[weekly.index >= first_week]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path, default=paths.AMBA_WEATHER_DIR)
    parser.add_argument("--first-week", default=FIRST_WEEK,
                        help="Drop weeks before this; the first full ETI week.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    end_date = (date.today() - timedelta(days=1)).isoformat()
    print(f"Fetching weather for {len(PARTIDOS)} AMBA partidos "
          f"({START_DATE} to {end_date})\n")
    # Budget line so a run longer than a minute is watchable; see CLAUDE.md.
    print(f"Budget: {len(PARTIDOS)} epochs x 1 seeds", flush=True)
    print("--- seed weather (1/1) ---", flush=True)

    written = 0
    for i, partido in enumerate(PARTIDOS):
        lon, lat = COORDS[SHORT_OF[partido]]
        out_path = args.output_dir / f"{partido_slug(partido)}_weather_weekly.csv"
        if out_path.exists():
            print(f"Epoch {i + 1} | {partido} - already exists, skipping", flush=True)
            continue
        if i > 0:
            time.sleep(REQUEST_DELAY)

        # The shared fetcher reads its window from module-level constants.
        _boston_weather.START_DATE = START_DATE
        _boston_weather.END_DATE = end_date
        daily = fetch_daily_weather(lat, lon)
        weekly = aggregate_to_weekly(daily, args.first_week)
        weekly.to_csv(out_path)
        written += 1
        print(f"Epoch {i + 1} | {partido} ({lat:.4f}, {lon:.4f}) "
              f"{len(weekly)} weeks -> {out_path.name}", flush=True)

    print(f"\n{written} new of {len(PARTIDOS)} partidos")
    print(f"Outputs: {paths.display(args.output_dir, paths.ROOT)}", flush=True)


if __name__ == "__main__":
    main()
