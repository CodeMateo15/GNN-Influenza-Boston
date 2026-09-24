"""Build the Columbus per-area static table: population and 8 demographics.

Boston's static features come from 22 City of Boston / BPDA indicator tables that
an agency publishes ready-aggregated to planning districts. Columbus has no
equivalent, so this script reconstructs the same eight columns from two federal
sources and aggregates them ZIP -> 17 areas:

  * Census ACS 5-year detailed tables, per ZCTA -- population and every count
    the eight features are ratios of. REQUIRES A FREE API KEY (see below).
  * columbus_area_geography.csv -- land area per area, the pop_density
    denominator. Produced keylessly by scrape_gazetteer_columbus.py, which must
    be run first.

The provenance difference is real and is recorded in the output file's header:
Boston's demographics were published by its health department, Columbus's are
derived by us. See Code/docs/COLUMBUS_DATA_NOTES.md.

Output: Data/Columbus Influenza Data/columbus_area_static.csv (17 rows).
Values are RAW ratios, not normalised -- min-max normalisation happens in
influenza/loaders/columbus.py::load_static_demographics(), matching Boston.

    export CENSUS_API_KEY=...        # https://api.census.gov/data/key_signup.html
    python Code/scrapers/scrape_acs_columbus.py
    python Code/scrapers/scrape_acs_columbus.py --acs-year 2023
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths
from influenza.loaders import columbus_crosswalk as crosswalk

ACS_URL = "https://api.census.gov/data/{year}/acs/acs5"
DEFAULT_ACS_YEAR = 2023
TIMEOUT = 120
GEOGRAPHY_FILE = "columbus_area_geography.csv"

# --- ACS variables ---------------------------------------------------------
# Grouped as numerator/denominator pairs so the aggregation below can sum counts
# per area FIRST and only then take the ratio. Taking per-ZIP ratios and
# averaging them would weight a 2,000-person ZIP the same as a 40,000-person one.
POPULATION = "B01003_001E"

# Boston's pct_children is "0-9 years" + "10-19 years", i.e. under 20, so the
# ACS age bands are chosen to match that cut rather than the more common under-18.
_MALE_UNDER_20 = ["B01001_003E", "B01001_004E", "B01001_005E", "B01001_006E", "B01001_007E"]
_FEMALE_UNDER_20 = ["B01001_027E", "B01001_028E", "B01001_029E", "B01001_030E", "B01001_031E"]
_MALE_65_PLUS = ["B01001_020E", "B01001_021E", "B01001_022E",
                 "B01001_023E", "B01001_024E", "B01001_025E"]
_FEMALE_65_PLUS = ["B01001_044E", "B01001_045E", "B01001_046E",
                   "B01001_047E", "B01001_048E", "B01001_049E"]

# feature -> (numerator variables, denominator variables, invert)
# `invert` produces 1 - ratio, used for nonwhite_share from "White alone, not
# Hispanic or Latino".
FEATURES: dict[str, tuple[list[str], list[str], bool]] = {
    "poverty_rate":    (["B17001_002E"], ["B17001_001E"], False),
    "transit_share":   (["B08301_010E"], ["B08301_001E"], False),
    "pct_children":    (_MALE_UNDER_20 + _FEMALE_UNDER_20, ["B01001_001E"], False),
    "pct_elderly":     (_MALE_65_PLUS + _FEMALE_65_PLUS, ["B01001_001E"], False),
    "owner_rate":      (["B25003_002E"], ["B25003_001E"], False),
    "no_vehicle_rate": (["B08201_002E"], ["B08201_001E"], False),
    "nonwhite_share":  (["B03002_003E"], ["B03002_001E"], True),
}

ACS_VARIABLES = sorted({POPULATION} | {
    v for numerator, denominator, _ in FEATURES.values() for v in (*numerator, *denominator)
})


def fetch_acs(year: int, key: str) -> pd.DataFrame:
    """Per-ZCTA ACS counts. Returns a frame indexed by 5-digit ZCTA string.

    ZCTA is a national-only geography in ACS 2020 and later -- it can no longer
    be filtered by state -- so this pulls all ~33,000 and filters afterwards.
    """
    # The API caps a single call at 50 variables; we need 33, so one call does it.
    if len(ACS_VARIABLES) > 50:
        raise RuntimeError(f"{len(ACS_VARIABLES)} variables exceeds the ACS 50-per-call limit.")

    params = {
        "get": ",".join(ACS_VARIABLES),
        "for": "zip code tabulation area:*",
        "key": key,
    }
    response = requests.get(ACS_URL.format(year=year), params=params, timeout=TIMEOUT)
    if response.status_code != 200 or not response.text.lstrip().startswith("["):
        raise RuntimeError(
            f"ACS {year} request failed (HTTP {response.status_code}). "
            f"First 300 chars of the response:\n{response.text[:300]}"
        )
    payload = response.json()
    frame = pd.DataFrame(payload[1:], columns=payload[0])
    zcta_column = next(c for c in frame.columns if "zip code" in c)
    frame["zcta"] = frame[zcta_column].astype(str).str.zfill(5)
    for column in ACS_VARIABLES:
        # ACS uses large negative sentinels (-666666666 and friends) for
        # suppressed or unavailable estimates. They must become NaN, not be
        # summed into a denominator.
        numeric = pd.to_numeric(frame[column], errors="coerce")
        frame[column] = numeric.where(numeric > -1e6)
    return frame.set_index("zcta")[ACS_VARIABLES]


def load_geography(path: Path) -> pd.DataFrame:
    """Per-area land area, from scrape_gazetteer_columbus.py."""
    if not path.exists():
        raise SystemExit(
            f"{path} not found.\n\n"
            "Run the keyless geography scraper first -- it supplies the land\n"
            "area that pop_density divides by:\n\n"
            "    python Code/scrapers/scrape_gazetteer_columbus.py\n")
    return pd.read_csv(path, comment="#", index_col=0)


def aggregate_to_areas(acs: pd.DataFrame, geography: pd.DataFrame,
                       zip_area: dict[int, str]) -> pd.DataFrame:
    """Sum counts per area, then take ratios. One row per area.

    Summing the counts before dividing is the point: a per-ZIP ratio averaged
    across an area would weight a 2,000-person ZIP the same as a 40,000-person
    one. This mirrors data.py::_load_city_csv, which also sums the constituent
    planning districts before computing any Boston ratio.
    """
    mapping = pd.Series({f"{z:05d}": area for z, area in zip_area.items()}, name="area")
    joined = acs.join(mapping, how="inner")
    if len(joined) != len(zip_area):
        missing = sorted(set(mapping.index) - set(acs.index))
        raise RuntimeError(f"No ACS row for ZCTAs {missing}.")

    counts = joined.groupby("area")[ACS_VARIABLES].sum(min_count=1)

    static = pd.DataFrame(index=counts.index)
    static["population"] = counts[POPULATION]
    static["land_sqmi"] = geography["land_sqmi"].reindex(counts.index)
    static["pop_density"] = static["population"] / static["land_sqmi"]
    for name, (numerator, denominator, invert) in FEATURES.items():
        ratio = counts[numerator].sum(axis=1) / counts[denominator].sum(axis=1)
        static[name] = (1.0 - ratio) if invert else ratio
    static["n_zips"] = joined.groupby("area").size()
    return static.sort_index()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--acs-year", type=int, default=DEFAULT_ACS_YEAR)
    parser.add_argument("--output", type=Path, default=paths.COLUMBUS_STATIC_FILE)
    args = parser.parse_args()

    key = os.environ.get("CENSUS_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "CENSUS_API_KEY is not set.\n\n"
            "The Census API no longer serves keyless requests -- it redirects to\n"
            "missing_key.html -- so population and the eight demographic columns\n"
            "cannot be fetched without one. Keys are free and issued instantly:\n\n"
            "    https://api.census.gov/data/key_signup.html\n\n"
            "Then:  export CENSUS_API_KEY=<your key>\n"
        )

    zip_area = crosswalk.zip_to_area()
    print(f"Crosswalk: {len(zip_area)} ZIPs -> {len(set(zip_area.values()))} areas")

    geography = load_geography(paths.COLUMBUS_DIR / GEOGRAPHY_FILE)
    print(f"Geography: {len(geography)} areas, "
          f"{geography['land_sqmi'].sum():.1f} sq mi total")

    print(f"ACS {args.acs_year} 5-year, {len(ACS_VARIABLES)} variables...")
    acs = fetch_acs(args.acs_year, key)
    print(f"  {len(acs):,} ZCTAs")

    static = aggregate_to_areas(acs, geography, zip_area)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as handle:
        handle.write(
            f"# Columbus per-area static features. Generated by Code/scrapers/"
            f"scrape_acs_columbus.py\n"
            f"# Sources: Census ACS {args.acs_year} 5-year (detailed tables, per ZCTA);\n"
            f"# land area from columbus_area_geography.csv.\n"
            f"# DERIVED BY THIS PROJECT, not published by a health department -- unlike\n"
            f"# Boston's equivalents in Data/Neighborhood Data/. Ratios are raw; min-max\n"
            f"# normalisation happens in influenza/loaders/columbus.py.\n")
        static.to_csv(handle)

    print(f"\n{len(static)} areas -> {paths.display(args.output, paths.ROOT)}")
    print(f"Total population across the {len(static)} areas: {static['population'].sum():,.0f}")
    print(static[["population", "pop_density", "poverty_rate", "transit_share",
                  "nonwhite_share", "n_zips"]].round(3).to_string())


if __name__ == "__main__":
    main()
