"""
Fetch historical daily weather data for each Boston neighborhood from
Open-Meteo Archive API and aggregate to Sunday-start weeks matching
the flu data boundaries.

Output: Data/Weather/<neighborhood_slug>_weather_weekly.csv (one per neighborhood)
"""

import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

# --- Config ---
API_URL = "https://archive-api.open-meteo.com/v1/archive"
# Start a week before the first flu week (2017-12-31) so the first full
# Sunday-start week has 7 days of data.
START_DATE = "2017-12-25"
END_DATE = (date.today() - timedelta(days=1)).isoformat()

DAILY_VARIABLES = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "relative_humidity_2m_mean",
    "precipitation_sum",
    "wind_speed_10m_max",
]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "Data" / "Weather"

MAX_RETRIES = 5
BACKOFF_BASE = 2  # seconds
REQUEST_DELAY = 5  # seconds between neighborhood requests to avoid rate limits

# Neighborhood name (matching flu data) -> (latitude, longitude)
NEIGHBORHOODS = {
    "Allston/Brighton":                              (42.3539, -71.1337),
    "Back Bay, Beacon Hill, Downtown, North End, West End": (42.3588, -71.0625),
    "Charlestown":                                   (42.3782, -71.0602),
    "Dorchester (02121, 02125)":                     (42.2973, -71.0668),
    "Dorchester (02122, 02124)":                     (42.2841, -71.0562),
    "East Boston":                                   (42.3702, -71.0389),
    "Fenway":                                        (42.3429, -71.1003),
    "Hyde Park":                                     (42.2565, -71.1241),
    "Jamaica Plain":                                 (42.3097, -71.1152),
    "Mattapan":                                      (42.2770, -71.0929),
    "Roslindale":                                    (42.2835, -71.1270),
    "Roxbury":                                       (42.3152, -71.0886),
    "South Boston":                                  (42.3381, -71.0476),
    "South End":                                     (42.3388, -71.0765),
    "West Roxbury":                                  (42.2798, -71.1581),
}


def slugify(name: str) -> str:
    """Convert neighborhood name to a filesystem-safe slug."""
    return (
        name.lower()
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace(" ", "_")
        .strip("_")
    )


def fetch_daily_weather(lat: float, lon: float) -> pd.DataFrame:
    """Fetch daily weather data from Open-Meteo Archive API."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": ",".join(DAILY_VARIABLES),
        "timezone": "America/New_York",
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(API_URL, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            break
        except (requests.RequestException, ValueError) as e:
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"Failed after {MAX_RETRIES} attempts: {e}") from e
            # Longer backoff for rate limits
            is_rate_limit = hasattr(e, "response") and getattr(e.response, "status_code", 0) == 429
            wait = (BACKOFF_BASE ** attempt) * (5 if is_rate_limit else 1)
            print(f"  Attempt {attempt} failed ({'rate limited' if is_rate_limit else e}), retrying in {wait}s...")
            time.sleep(wait)

    daily = data["daily"]
    df = pd.DataFrame(daily)
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")
    return df


def aggregate_to_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """Resample daily data to Sunday-start weeks matching flu data."""
    agg_rules = {
        "temperature_2m_mean": "mean",
        "temperature_2m_max": "mean",
        "temperature_2m_min": "mean",
        "relative_humidity_2m_mean": "mean",
        "precipitation_sum": "sum",
        "wind_speed_10m_max": "mean",
    }

    weekly = df.resample("W-SUN", label="left", closed="left").agg(agg_rules)

    # Rename columns for the output CSV
    weekly = weekly.rename(columns={
        "temperature_2m_mean": "temp_mean_c",
        "temperature_2m_max": "temp_max_c",
        "temperature_2m_min": "temp_min_c",
        "relative_humidity_2m_mean": "relative_humidity_mean",
        "precipitation_sum": "precipitation_sum_mm",
        "wind_speed_10m_max": "wind_speed_max_kmh",
    })

    weekly = weekly.round(1)

    # Drop partial first week before 2017-12-31
    weekly = weekly.loc[weekly.index >= "2017-12-31"]

    weekly.index.name = "week_start"
    return weekly


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Fetching weather for {len(NEIGHBORHOODS)} neighborhoods "
          f"({START_DATE} to {END_DATE})\n")

    for i, (name, (lat, lon)) in enumerate(NEIGHBORHOODS.items()):
        slug = slugify(name)
        out_path = OUTPUT_DIR / f"{slug}_weather_weekly.csv"

        # Skip if already downloaded (resume after rate-limit failures)
        if out_path.exists():
            print(f"{name} - already exists, skipping")
            continue

        if i > 0:
            time.sleep(REQUEST_DELAY)

        print(f"{name} ({lat}, {lon})...")
        daily = fetch_daily_weather(lat, lon)
        weekly = aggregate_to_weekly(daily)
        weekly.to_csv(out_path)
        print(f"  {len(weekly)} weeks -> {out_path.name}")

    # Print summary
    print(f"\nDone. {len(NEIGHBORHOODS)} CSVs saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
