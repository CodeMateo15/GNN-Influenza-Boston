"""Build the Chicago weekly ILI-activity panel from the City's open-data portal.

    python Code/scrapers/build_chicago_panel.py
    python Code/scrapers/build_chicago_panel.py --download   # refetch from Socrata

The Chicago Department of Public Health publishes "Influenza Risk Level by ZIP
Code" (data.cityofchicago.org, dataset 8vvr-jv2g), compiled from Illinois
ESSENCE emergency-department syndromic surveillance, and the City publishes the
ZIP polygons separately ("Boundaries - ZIP Codes", unjd-c2ca). Both are keyless
Socrata endpoints. By default this reads the copies the areaFluForecast example
notebook already cached; `--download` refetches both.

Outputs, all under Data/Chicago/:
  * chicago_ili_level_long.csv    one row per ZIP-week, complete weekly grid
  * chicago_ili_level_wide.csv    weeks x ZIPs
  * chicago_zip_coverage.csv      reporting coverage per ZIP, and keep_core
  * chicago_zip_boundaries.geojson  the polygons (unjd-c2ca), as downloaded
  * source/8vvr-jv2g.csv          the raw table this panel was built from

Three things worth knowing before using the output:

  * THE VALUE IS AN INDEX, NOT A RATE. `ili_level` runs 1-10: a ZIP's share of
    ED visits for ILI against that same ZIP's summer mean, roughly one standard
    deviation per level, capped at 10. There is no count and no denominator to
    recover, so nothing here is per-100,000 -- and the cap flattens every
    strong season into a run of 10s.
  * MISSING WEEKS ARE MISSING, NOT ZERO. The portal publishes 346 of the 365
    weeks between 2019-09-29 and 2026-09-20; all 19 absent weeks fall in
    May-September 2020, when the whole city is absent at once. The grid is
    completed and those weeks stay NaN. A ZIP absent while others report is
    also NaN -- an index has no "zero cases" reading to fall back on, which is
    the difference from Buenos Aires's isolated-absence rule.
  * ONE ZIP IS DROPPED. 60106 (Bensenville, mostly outside the city) has rows
    but no polygon in unjd-c2ca, so it can have no borders; it is also the
    thinnest series in the table.

The scored/anchor split is the Buenos Aires coverage rule unchanged: a ZIP
reporting in at least 90% of panel weeks is a scored node, anything below is an
anchor. See Code/docs/CHICAGO_DATA_NOTES.md.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

SOCRATA = "https://data.cityofchicago.org/resource/{dataset}.{fmt}"
ILI_DATASET = "8vvr-jv2g"
ZIP_DATASET = "unjd-c2ca"
TIMEOUT = 300

# Where the areaFluForecast example notebook caches both downloads. Used only
# when --download is not given; on a machine without the package the builder
# falls back to the copy it wrote into Data/Chicago/source/ last time.
PACKAGE_CACHE = Path.home() / "Developer/areaFluForecast/examples/data/chicago_cache"

# Same threshold as build_amba_panel.py, so "anchor" means the same thing in
# both cities.
CORE_COVERAGE = 0.90


def download(dataset: str, fmt: str, params: dict, out: Path) -> Path:
    """One Socrata table to disk. Keyless; $limit is set well above the row count."""
    import requests

    response = requests.get(SOCRATA.format(dataset=dataset, fmt=fmt),
                            params=params, timeout=TIMEOUT)
    response.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(response.text)
    print(f"  downloaded {dataset}.{fmt}: {len(response.content):,} bytes")
    return out


def locate_sources(refetch: bool) -> tuple[Path, Path]:
    """(ILI csv, ZIP geojson), downloaded or taken from a cache."""
    source_dir = paths.CHICAGO_SOURCE_DIR
    if refetch:
        ili = download(ILI_DATASET, "csv",
                       {"$limit": 500_000,
                        "$select": "week_start,zip_code,ili_activity_level"},
                       source_dir / f"{ILI_DATASET}.csv")
        zips = download(ZIP_DATASET, "geojson", {"$limit": 1000},
                        paths.CHICAGO_BOUNDARIES_FILE)
        return ili, zips
    for ili, zips in ((PACKAGE_CACHE / f"{ILI_DATASET}.csv",
                       PACKAGE_CACHE / f"{ZIP_DATASET}.geojson"),
                      (source_dir / f"{ILI_DATASET}.csv", paths.CHICAGO_BOUNDARIES_FILE)):
        if ili.exists() and zips.exists():
            return ili, zips
    raise SystemExit(f"No cached {ILI_DATASET}.csv / {ZIP_DATASET}.geojson in "
                     f"{PACKAGE_CACHE} or {paths.CHICAGO_DIR}; rerun with --download.")


def to_sunday(stamps: pd.Series) -> pd.Series:
    """Floor to the Sunday that starts the week, the grid every city uses."""
    stamps = pd.to_datetime(stamps).dt.tz_localize(None).dt.normalize()
    return stamps - pd.to_timedelta((stamps.dt.dayofweek + 1) % 7, unit="D")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--download", action="store_true",
                        help="Refetch both tables from the Chicago Data Portal.")
    args = parser.parse_args()

    ili_path, zip_path = locate_sources(args.download)
    print(f"ILI table:  {ili_path}\nZIP shapes: {zip_path}")

    raw = pd.read_csv(ili_path, dtype={"zip_code": str})
    raw["zip_code"] = raw["zip_code"].str.strip().str.zfill(5)
    raw["week_start"] = to_sunday(raw["week_start"])
    moved = int((pd.to_datetime(pd.read_csv(ili_path, usecols=["week_start"])
                                ["week_start"]).dt.normalize() != raw["week_start"]).sum())
    raw = raw.rename(columns={"zip_code": "zip", "ili_activity_level": "ili_level"})
    raw["ili_level"] = pd.to_numeric(raw["ili_level"], errors="coerce")
    duplicated = raw.duplicated(["zip", "week_start"])
    if duplicated.any():
        raise SystemExit(f"{int(duplicated.sum())} duplicate ZIP-weeks after snapping "
                         "to Sunday; the source changed shape.")
    out_of_range = raw["ili_level"].notna() & ~raw["ili_level"].between(1, 10)
    if out_of_range.any():
        raise SystemExit(f"{int(out_of_range.sum())} levels outside 1-10; the index "
                         "definition changed and every downstream caveat with it.")
    print(f"  {len(raw):,} ZIP-weeks, {raw.zip.nunique()} ZIPs, "
          f"{raw.week_start.nunique()} distinct weeks "
          f"({moved} dates moved to their Sunday)")

    with open(zip_path) as handle:
        polygons = json.load(handle)
    with_polygon = {str(f["properties"]["zip"]).zfill(5) for f in polygons["features"]}
    dropped = sorted(set(raw.zip) - with_polygon)
    unreported = sorted(with_polygon - set(raw.zip))
    if unreported:
        raise SystemExit(f"Polygons with no ILI series: {unreported}. They would be "
                         "graph nodes with nothing to score.")
    print(f"  dropped (no polygon): {dropped or 'none'}")
    raw = raw[raw.zip.isin(with_polygon)]

    # A complete weekly grid. Weeks the portal never published become rows of
    # NaN rather than disappearing, so `valid_origins` sees consecutive weeks and
    # the gap is handled as missing data instead of silently splicing May 2020
    # onto October 2020.
    grid = pd.date_range(raw.week_start.min(), raw.week_start.max(), freq="7D")
    zips = sorted(with_polygon)
    wide = (raw.pivot(index="week_start", columns="zip", values="ili_level")
            .reindex(index=grid, columns=zips))
    wide.index.name = "week_start"
    wide.columns.name = None
    long = (wide.stack(future_stack=True).rename("ili_level").reset_index()
            .rename(columns={"level_1": "zip"})[["zip", "week_start", "ili_level"]]
            .sort_values(["zip", "week_start"]))

    reported = wide.notna().any(axis=1)
    post = wide.loc[wide.index >= "2022-07-01"]
    coverage = pd.DataFrame({
        "zip": zips,
        "coverage": wide.notna().mean().round(3).values,
        # Not used by the rule; recorded because it is the number that explains
        # the one anchor -- see CHICAGO_DATA_NOTES.md.
        "coverage_post_covid": post.notna().mean().round(3).values,
        "first_week": [wide[z].first_valid_index().date() for z in zips],
        "mean_level": wide.mean().round(2).values,
    })
    coverage["keep_core"] = coverage["coverage"] >= CORE_COVERAGE
    coverage = coverage.sort_values(["coverage", "zip"], ascending=[False, True])

    out = paths.CHICAGO_DIR
    out.mkdir(parents=True, exist_ok=True)
    long.to_csv(paths.CHICAGO_PANEL_FILE, index=False, date_format="%Y-%m-%d")
    wide.reset_index().to_csv(paths.CHICAGO_WIDE_FILE, index=False, date_format="%Y-%m-%d")
    coverage.to_csv(paths.CHICAGO_COVERAGE_FILE, index=False)
    # Keep the exact inputs beside the outputs, so the panel can be rebuilt
    # without the package cache or the portal.
    paths.CHICAGO_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for source, target in ((ili_path, paths.CHICAGO_SOURCE_DIR / ili_path.name),
                           (zip_path, paths.CHICAGO_BOUNDARIES_FILE)):
        if source.resolve() != target.resolve():
            shutil.copyfile(source, target)

    print(f"\npanel: {len(grid)} weeks x {len(zips)} ZIPs "
          f"({grid[0].date()} .. {grid[-1].date()})")
    print(f"  weeks with no ZIP reported: {int((~reported).sum())} "
          f"({', '.join(sorted({str(d.year) for d in grid[~reported.values]})) or '-'})")
    print(f"  ZIP-weeks NaN: {int(long.ili_level.isna().sum()):,} "
          f"({long.ili_level.isna().mean():.1%})")
    print(f"  core ZIPs (>= {CORE_COVERAGE:.0%} coverage): {int(coverage.keep_core.sum())}, "
          f"anchors: {coverage.loc[~coverage.keep_core, 'zip'].tolist()}")
    print(coverage.head(3).to_string(index=False))
    print("  ...")
    print(coverage.tail(3).to_string(index=False))
    print(f"Outputs: {paths.display(out, paths.ROOT)}")


if __name__ == "__main__":
    main()
