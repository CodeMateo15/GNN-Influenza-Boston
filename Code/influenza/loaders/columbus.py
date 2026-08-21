"""Columbus / Franklin County loaders.

Boston's sources arrive pre-aggregated: the BPHC dashboard publishes a weekly ILI
ED-visit *rate per 100,000* per neighborhood, and `data.py` mostly has to reshape
it. Columbus arrives as three line-level extracts -- one row per emergency
department visit, per hospitalisation, per COVID case -- keyed to a 5-digit home
ZIP. Everything the Boston loaders can read off a `value` column has to be built
here: the weekly grid, the node aggregation, and the population denominator.

Three consequences worth stating up front, because they are the honest limits of
any Boston/Columbus comparison:

1. **Zeros are real.** Boston's absent (week, neighborhood) rows are BPHC
   suppressing a small count, so they must stay NaN and be dropped from the loss
   and the metrics. A Columbus area-week with no row had no qualifying ED visit,
   which is an observation of zero. Faking Boston-style NaNs here would discard
   real information; treating Boston's NaNs as zeros invented ~140 fake weeks and
   voided every result before August 2026 (see DATA_NOTES.md defect 2). The two
   cities genuinely differ, and `n_obs` in metrics.csv will show it.

2. **The denominator is ours, not an agency's.** Rates are counts divided by
   ACS ZCTA population, aggregated to areas by
   `Code/scrapers/scrape_acs_columbus.py`. Boston's rates were computed by its
   health department.

3. **ZCTA boundaries cross the county line** -- the 42 mapped ZCTAs span ~643
   square miles against Franklin County's ~540. That is the right denominator
   anyway: the ILI extract counts "residents of a ZIP code classified as being in
   Franklin County", so numerator and denominator cover the same population.
"""

from __future__ import annotations

import glob
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from .. import paths
from ..constants import STATIC_DEMO_COLS, WEATHER_COLS
from . import columbus_crosswalk as crosswalk

# Boston's flu weeks start on Sunday and the weather scraper aggregates on
# 'W-SUN'. Columbus timestamps are snapped to the same grid so that one
# `week_index` serves both cities and `valid_origins`' 7-day contiguity check
# means the same thing in each.

ILI_SHEET = 0
ILI_SYNDROME = "ILISpecified"


# ---------------------------------------------------------------------------
# Week grid
# ---------------------------------------------------------------------------

def snap_to_week(timestamps: pd.Series) -> pd.Series:
    """Floor each timestamp to the Sunday that starts its week.

    `dayofweek` is Monday=0, so Sunday is 6 and `(dayofweek + 1) % 7` is the
    number of days since the preceding Sunday.
    """
    stamps = pd.to_datetime(timestamps)
    return (stamps - pd.to_timedelta((stamps.dt.dayofweek + 1) % 7, unit="D")).dt.normalize()


def mmwr_week_start(year: int, week: int) -> pd.Timestamp:
    """First day (Sunday) of an MMWR epidemiological week.

    MMWR week 1 is the first Sunday-to-Saturday week with at least four days in
    the new year, which is equivalently the week containing January 4. That makes
    some years 53 weeks long -- 2020 and 2025 among them -- so a week number of
    53 is not by itself a defect. The IAH extract does contain 2025 week 53
    (2025-12-28 to 2026-01-03) and it is legitimate: MMWR 2026 week 1 begins
    2026-01-04, so the weeks tile with no gap and no overlap.
    """
    anchor = date(year, 1, 4)
    week1_start = anchor - timedelta(days=(anchor.weekday() + 1) % 7)
    return pd.Timestamp(week1_start + timedelta(days=(week - 1) * 7))


def mmwr_weeks_in_year(year: int) -> int:
    """52 or 53. Used to reject a genuinely impossible (year, week) pair."""
    return (mmwr_week_start(year + 1, 1) - mmwr_week_start(year, 1)).days // 7


def _full_weeks(weeks: pd.Series, span_start: pd.Timestamp,
                span_end: pd.Timestamp) -> pd.DatetimeIndex:
    """The contiguous weekly index, dropping partially observed edge weeks.

    The extract's first and last weeks are only fractionally covered -- the ILI
    file starts on a Saturday and ends on a Monday -- so their counts are
    spuriously low. Keeping them would put two artificial troughs at the ends of
    every series, one of which sits inside the evaluation window's tail.
    """
    first = weeks.min()
    if first < span_start:
        first = first + pd.Timedelta(days=7)
    last = weeks.max()
    if last + pd.Timedelta(days=6) > span_end:
        last = last - pd.Timedelta(days=7)
    return pd.date_range(first, last, freq="7D")


# ---------------------------------------------------------------------------
# The target series
# ---------------------------------------------------------------------------

def _read_ili(path=None) -> pd.DataFrame:
    """Line-level ILI ED visits with an `area` column attached."""
    file = paths.require(path or paths.COLUMBUS_ILI_FILE, "Columbus ILI data")
    frame = pd.read_excel(file, sheet_name=ILI_SHEET)

    expected = {"Syndrome", "Date", "Zipcode"}
    if not expected.issubset(frame.columns):
        raise ValueError(f"{file.name}: expected columns {sorted(expected)}, "
                         f"found {list(frame.columns)}.")

    syndromes = set(frame["Syndrome"].unique())
    if syndromes != {ILI_SYNDROME}:
        raise ValueError(
            f"{file.name}: expected only {ILI_SYNDROME!r} rows, found {sorted(syndromes)}. "
            "A second syndrome would need an explicit filter before aggregation."
        )

    frame = frame.dropna(subset=["Date", "Zipcode"]).copy()
    frame["zip"] = frame["Zipcode"].astype(int)
    frame["week"] = snap_to_week(frame["Date"])

    zip_area = crosswalk.zip_to_area()
    frame["area"] = frame["zip"].map(zip_area)

    unmapped = sorted(set(frame.loc[frame["area"].isna(), "zip"]))
    anchors = set(crosswalk.load_anchor_zips())
    unexpected = [z for z in unmapped if z not in anchors
                  and z not in crosswalk.KNOWN_UNMAPPED_ZIPS]
    if unexpected:
        raise ValueError(
            f"{file.name}: ZIPs {unexpected} appear in the ILI data but are not in the "
            f"crosswalk and are not known fringe ZIPs. Update "
            f"columbus_crosswalk.KNOWN_UNMAPPED_ZIPS after checking whether they belong "
            f"to one of the 17 areas -- silently dropping them would bias the denominator."
        )
    return frame


def load_counts(path=None) -> pd.DataFrame:
    """Weekly ILI ED-visit COUNTS, one column per area.

    Returns a (weeks x 17) frame on a contiguous Sunday-start index. Missing
    (week, area) combinations become 0.0, not NaN: see this module's docstring.
    """
    frame = _read_ili(path)
    span_start, span_end = frame["Date"].min(), frame["Date"].max()

    mapped = frame.dropna(subset=["area"])
    panel = mapped.groupby(["week", "area"]).size().unstack("area")

    index = _full_weeks(pd.Series(panel.index), span_start, span_end)
    areas = crosswalk.area_names()
    # Reindex to every area and every week, then fill: a zero here is an
    # observed absence of qualifying visits, which is a real measurement.
    return panel.reindex(index=index, columns=areas).fillna(0.0).astype(float)


def load_area_population(path=None) -> pd.Series:
    """Per-area population from the scraped ACS table, indexed by area name."""
    file = path or paths.COLUMBUS_STATIC_FILE
    if not file.exists():
        raise FileNotFoundError(
            f"{file} not found.\n\n"
            "Columbus case files carry no population denominator, so rates per "
            "100,000 cannot be computed without it. Generate it with:\n\n"
            "    export CENSUS_API_KEY=...   # https://api.census.gov/data/key_signup.html\n"
            "    python Code/scrapers/scrape_acs_columbus.py\n\n"
            "load_counts() works without it if you only need visit counts."
        )
    frame = pd.read_csv(file, comment="#", index_col=0)
    return frame["population"].astype(float)


def load_rates(path=None, *, population_file=None) -> pd.DataFrame:
    """Weekly ILI ED-visit rates per 100,000, one column per area.

    The Boston counterpart of this function, `data.load_rates`, reads a published
    rate. Here the rate is constructed, so the population denominator is a
    modelling input with its own provenance -- see load_area_population().
    """
    counts = load_counts(path)
    population = load_area_population(population_file)

    missing = [area for area in counts.columns if area not in population.index]
    if missing:
        raise ValueError(
            f"No population for areas {missing}. The ACS table and the crosswalk "
            "disagree; regenerate columbus_area_static.csv."
        )
    return counts.div(population.reindex(counts.columns), axis=1) * 100_000.0


# ---------------------------------------------------------------------------
# Covariates
# ---------------------------------------------------------------------------

def _read_line_level_weekly(path, what: str, zip_column: str) -> pd.DataFrame:
    """One row per case, keyed by MMWR year/week and ZIP -> weekly area counts."""
    file = paths.require(path, what)
    frame = pd.read_csv(file)
    if zip_column not in frame.columns:
        raise ValueError(f"{file.name}: expected a {zip_column!r} column, "
                         f"found {list(frame.columns)}.")

    frame = frame.dropna(subset=["mmwryear", "mmwrweek", zip_column]).copy()
    frame["mmwryear"] = frame["mmwryear"].astype(int)
    frame["mmwrweek"] = frame["mmwrweek"].astype(int)

    # 53 is legitimate in a 53-week year; anything past the year's real length is
    # a genuine encoding error and should not be silently folded into week 1.
    limits = {year: mmwr_weeks_in_year(year) for year in frame["mmwryear"].unique()}
    overflow = frame.loc[frame.apply(
        lambda row: row["mmwrweek"] < 1 or row["mmwrweek"] > limits[row["mmwryear"]], axis=1)]
    if len(overflow):
        offenders = sorted(set(zip(overflow["mmwryear"], overflow["mmwrweek"])))
        raise ValueError(
            f"{file.name}: {len(overflow)} rows carry an MMWR week outside their "
            f"year's real length: {offenders}. MMWR years are 52 or 53 weeks "
            f"({', '.join(f'{y}={n}' for y, n in sorted(limits.items()))})."
        )

    frame["week"] = [mmwr_week_start(y, w)
                     for y, w in zip(frame["mmwryear"], frame["mmwrweek"])]
    frame["area"] = frame[zip_column].astype(int).map(crosswalk.zip_to_area())
    return frame.dropna(subset=["area"])


def load_hospitalizations(week_index: pd.DatetimeIndex, path=None) -> pd.DataFrame:
    """Weekly influenza-associated hospitalisation counts per area.

    Boston has no hospitalisation file at all, so this is Columbus-only and
    cannot appear in a like-for-like cross-city feature set. It is a severity
    signal rather than a volume one: weekly counts correlate r = 0.82 with the
    ILI series but the hospitalisations-per-ILI-visit ratio moves season to
    season, peaking in 2024-25.
    """
    frame = _read_line_level_weekly(
        path or paths.COLUMBUS_IAH_FILE, "Columbus IAH data", "ZIP5")
    panel = frame.groupby(["week", "area"]).size().unstack("area")
    return panel.reindex(index=week_index, columns=crosswalk.area_names()).fillna(0.0)


def load_covid_counts(week_index: pd.DatetimeIndex, path=None) -> pd.DataFrame:
    """Weekly COVID case counts per area.

    Note the column is `zip_5` here and `ZIP5` in the IAH file -- same meaning,
    two spellings, which is why the reader takes the name as an argument.

    This series ends in MMWR 2025 week 43, roughly five months into the
    evaluation window, so it cannot support an honest Columbus counterpart to
    Boston's `gnn_multiedge_covid_rsv`. The loader does not carry it forward:
    that decision belongs to the caller, visibly.
    """
    frame = _read_line_level_weekly(
        path or paths.COLUMBUS_COVID_FILE, "Columbus COVID data", "zip_5")
    panel = frame.groupby(["week", "area"]).size().unstack("area")
    return panel.reindex(index=week_index, columns=crosswalk.area_names())


def load_weather(week_index: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    """Per-area weekly weather. Returns column -> (weeks, 17) array.

    Mirrors `data.load_weather`, including the city-wide-median fill for gaps,
    but keys files to areas by slugified name rather than by keyword table --
    the Columbus weather files are written by our own scraper, so their names are
    ours to make canonical instead of something to pattern-match.
    """
    directory = paths.require(paths.COLUMBUS_WEATHER_DIR, "Columbus weather directory")
    files = sorted(glob.glob(str(directory / "*_weather_weekly.csv")))
    if not files:
        raise FileNotFoundError(
            f"No '*_weather_weekly.csv' files in {directory}. Run "
            "Code/scrapers/scrape_weather_columbus.py first."
        )

    areas = crosswalk.area_names()
    slug_to_index = {area_slug(area): i for i, area in enumerate(areas)}

    by_node: dict[int, pd.DataFrame] = {}
    unmapped: list[str] = []
    for path in files:
        slug = Path(path).name.removesuffix("_weather_weekly.csv")
        node = slug_to_index.get(slug)
        if node is None:
            unmapped.append(Path(path).name)
            continue
        by_node[node] = pd.read_csv(path, parse_dates=["week_start"]) \
            .set_index("week_start").sort_index()[WEATHER_COLS]
    if unmapped:
        raise ValueError(f"Weather files not mapped to an area: {unmapped}")

    arrays: dict[str, np.ndarray] = {}
    for col in WEATHER_COLS:
        values = np.full((len(week_index), len(areas)), np.nan, dtype=np.float32)
        for node, frame in by_node.items():
            aligned = frame[[col]].sort_index().reindex(
                week_index, method="nearest", tolerance=pd.Timedelta("7D"))
            values[:, node] = aligned[col].to_numpy()
        arrays[col] = np.where(np.isnan(values), np.nanmedian(values), values)
    return arrays


def area_slug(area: str) -> str:
    """'Clintonville/Near North' -> 'clintonville_near_north'. Filename-safe."""
    return (area.lower().replace("/", "_").replace(" ", "_")
            .replace("(", "").replace(")", "").replace(",", "").strip("_"))


def load_static_demographics(path=None) -> tuple[np.ndarray, list[str], dict[str, int]]:
    """(17, 8) min-max normalised socio-economic matrix, plus source years.

    Same eight columns and the same min-max scaling as
    `data.load_static_demographics`, so the demographic-similarity edge type uses
    a comparable feature space in both cities. The provenance differs and that is
    recorded in the CSV's comment header.
    """
    file = path or paths.COLUMBUS_STATIC_FILE
    if not file.exists():
        raise FileNotFoundError(
            f"{file} not found. Run Code/scrapers/scrape_acs_columbus.py "
            "(needs CENSUS_API_KEY)."
        )
    frame = pd.read_csv(file, comment="#", index_col=0)

    missing = [c for c in STATIC_DEMO_COLS if c not in frame.columns]
    if missing:
        raise ValueError(f"{file.name} is missing static columns {missing}.")

    static = frame.reindex(crosswalk.area_names())[STATIC_DEMO_COLS]
    static = static.fillna(static.median())
    span = static.max() - static.min()
    normalized = ((static - static.min()) / span.where(span > 0)).fillna(0.5)
    return normalized.to_numpy(dtype=np.float32), list(STATIC_DEMO_COLS), {}


def load_globals(week_index: pd.DatetimeIndex, names) -> pd.DataFrame:
    """City-wide weekly covariates for Columbus, in the order requested.

    Boston supplies five (`ili_count, ed_count, ili_ed_perc, flu_cases,
    monthly_cases`), all from the BPHC dashboard. Columbus can support only two,
    and one of them has no Boston analogue at all:

      * `ili_count`        -- countywide weekly ILI ED visits, summed over areas.
                              The direct counterpart of Boston's.
      * `hospitalizations` -- countywide weekly influenza-associated
                              hospitalisations. Boston publishes no
                              hospitalisation file, so any arm using this is
                              Columbus-only and cannot appear in a like-for-like
                              cross-city feature set.

    There is no ED-visit denominator (so no `ed_count` or `ili_ed_perc`), no
    confirmed-case count, and no monthly demographic series.
    """
    if not len(names):
        return pd.DataFrame(index=week_index)

    columns: dict[str, pd.Series] = {}
    for name in names:
        if name == "ili_count":
            counts = load_counts()
            columns[name] = counts.sum(axis=1).reindex(week_index)
        elif name == "hospitalizations":
            columns[name] = load_hospitalizations(week_index).sum(axis=1)
        else:
            raise ValueError(
                f"Unhandled global covariate for Columbus: {name!r}. "
                "Supported: ili_count, hospitalizations."
            )
    return pd.DataFrame(columns, index=week_index)
