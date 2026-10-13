"""Turn BPHC's dashboard export into the city folder the forecasting model reads.

    python bphc_export_to_city.py --export "BPHC Dashboard Influenza Neighborhood.csv" --out city/boston

Reads the weekly neighborhood rows of the export, writes `rates.csv` (one row per
week, one column per neighborhood) and copies the neighborhood map, borders and
outside anchors from the package's bundled Boston city. Weather is then fetched
from Open-Meteo (free, no key; skip with --no-weather).

Two quirks of the export are handled (both silently corrupt forecasts if missed):
1. Each (week, neighborhood) appears twice, once as the ED-visit count and once
   as the rate per 100,000, with the same unit label. The rate is the larger of
   the pair (every neighborhood has far fewer than 100,000 residents).
2. Dorchester is published as two ZIP groups; the model's Dorchester is their mean.
Weeks BPHC suppressed (small counts) stay blank; they are not zeros.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

# BPHC's `demographic_value` -> the model's area name.
AREAS = {
    "Allston/Brighton": "Allston/Brighton",
    "BB/BH/DT/NE/WE": "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown": "Charlestown",
    "Dor (02121, 02125)": "Dorchester",
    "Dor (02122, 02124)": "Dorchester",
    "East Boston": "East Boston",
    "Fenway": "Fenway",
    "Hyde Park": "Hyde Park",
    "Jamaica Plain": "Jamaica Plain",
    "Mattapan": "Mattapan",
    "Roslindale": "Roslindale",
    "Roxbury": "Roxbury",
    "South Boston": "South Boston",
    "South End": "South End",
    "West Roxbury": "West Roxbury",
}
ORDER = list(dict.fromkeys(AREAS.values()))


def read_bphc_export(path: str | Path) -> pd.DataFrame:
    """Weekly rates per 100,000: weeks (Sunday start) x the 14 model areas."""
    frame = pd.read_csv(path)
    frame = frame[frame["date_type"].eq("Weekly")].copy()
    frame["week"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["rate"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.dropna(subset=["week", "rate"])
    sizes = frame.groupby(["week", "demographic_value"]).size().unique()
    if not (len(sizes) == 1 and sizes[0] == 2):
        raise SystemExit(f"{path}: expected a count row and a rate row per week and "
                         f"neighborhood, found group sizes {sorted(sizes)}. The export layout "
                         "changed; check which row is the rate before forecasting.")
    unknown = sorted(set(frame["demographic_value"]) - set(AREAS))
    if unknown:
        raise SystemExit(f"{path}: unknown neighborhoods {unknown}; add them to AREAS.")
    rates = frame.groupby(["week", "demographic_value"])["rate"].max().reset_index()
    rates["area"] = rates["demographic_value"].map(AREAS)
    wide = rates.groupby(["week", "area"])["rate"].mean().unstack("area")
    return wide.reindex(columns=ORDER).sort_index().astype(float)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--export", required=True, type=Path,
                        help='BPHC "Influenza Neighborhood" CSV from the dashboard')
    parser.add_argument("--out", required=True, type=Path, help="city folder to write")
    parser.add_argument("--no-weather", action="store_true", help="skip the Open-Meteo fetch")
    args = parser.parse_args()

    import areafluforecast as af

    rates = read_bphc_export(args.export)
    city = af.load_sample("boston", weather=False).with_rates(rates)
    if not args.no_weather:
        city.fetch_weather()
    af.save_city(city, args.out)
    print(f"{len(rates)} weeks, {rates.index.min().date()} to {rates.index.max().date()}")
    print(f"Outputs: {args.out}")


if __name__ == "__main__":
    main()
