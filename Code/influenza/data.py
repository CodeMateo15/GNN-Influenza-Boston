"""Data loaders. Every source is read through exactly one function here.

Heavy or optional dependencies are imported lazily inside the loader that needs
them, so a script that only wants flu rates does not pay for openpyxl or torch.
See docs/DATA_NOTES.md for the per-file quirks these loaders work around.
"""

from __future__ import annotations

import glob
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

from . import paths
from .constants import (
    BPHC_KEYWORDS,
    GEOID_TO_IDX,
    NEIGHBORHOODS,
    N_NEIGH,
    STATIC_DEMO_COLS,
    WASTEWATER_TO_IDX,
    WEATHER_COLS,
    WEATHER_KEYWORDS,
)

ED_METRICS = ["ili_count", "ed_count", "ili_ed_perc", "flu_cases"]


def match_index(name: str, keywords: Sequence[tuple[str, int]]) -> int | None:
    """First keyword whose text appears in `name`, or None.

    Order matters: the keyword lists are sorted longest-first so that
    'west roxbury' is matched before the substring 'roxbury'.
    """
    value = str(name).lower().strip()
    return next((idx for key, idx in keywords if key in value), None)


def neighborhood_index(name: str) -> int | None:
    """Map a BPHC `demographic_value` to a canonical node index 0..13."""
    return match_index(name, BPHC_KEYWORDS)


def load_rates(path=None, *, strict: bool = True) -> pd.DataFrame:
    """Weekly influenza ED-visit rates per 100,000, one column per neighborhood.

    Returns a (weeks x 14) frame indexed by week start, columns NEIGHBORHOODS.
    Weeks with no observation for a neighborhood are NaN, not zero.

    Two quirks of the source file are handled here; both silently corrupted
    every result in this project before they were found (docs/DATA_NOTES.md):

    1. Each (week, neighborhood) appears **twice** -- once as an integer ILI
       ED-visit count and once as the rate per 100,000 -- and both rows are
       labelled `unit="per 100,000 residents"`. We keep the rate (the larger of
       the pair). Averaging them, as the original loader did, produced
       `(count + rate) / 2`: a per-neighborhood rescaling of the truth.
    2. Coverage is uneven across neighborhoods (Charlestown has 340 of 436
       weeks). The file contains no genuine zeros, so a missing week is BPHC
       suppressing a small count, not an absence of influenza. Imputing 0.0
       invented ~140 fake zero-rate weeks in the post-COVID period alone.
    """
    file = paths.require(path or paths.FLU_FILE, "Boston influenza data")
    frame = pd.read_csv(file)
    frame = frame.loc[frame["date_type"].eq("Weekly")].copy()
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["rate"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.dropna(subset=["date", "rate"])

    pair_sizes = frame.groupby(["date", "demographic_value"]).size().unique()
    if strict and not (len(pair_sizes) == 1 and pair_sizes[0] == 2):
        raise ValueError(
            f"{file.name}: expected exactly 2 rows (count and rate) per "
            f"(week, neighborhood); found group sizes {sorted(pair_sizes)}. "
            "The upstream file layout changed -- re-check which row is the rate "
            "before trusting load_rates()."
        )
    # Rate = count / population * 100000, and every neighborhood's population is
    # far below 100,000, so the rate is always the larger of the two rows.
    rates_long = frame.groupby(["date", "demographic_value"])["rate"].max().reset_index()

    rates_long["node"] = rates_long["demographic_value"].map(neighborhood_index)
    rates_long = rates_long.dropna(subset=["node"])
    rates_long["node"] = rates_long["node"].astype(int)

    # The only legitimate averaging: the two Dorchester ZIP groups share node 3.
    rates = (
        rates_long.groupby(["date", "node"])["rate"].mean().unstack("node").sort_index()
    )
    rates = rates.reindex(columns=range(N_NEIGH))
    rates.columns = NEIGHBORHOODS
    return rates.astype(float)


def impute_causal(frame: pd.DataFrame, *, ffill_limit: int = 4) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fill missing values using only past observations.

    Models need finite inputs, but targets must stay NaN so they are excluded
    from the loss and the metrics rather than scored as zeros.

    Interpolation is deliberately *not* used. A sample's lookback window ends at
    the forecast origin, so interpolating the value at the origin would read the
    following week -- which is the target. Carrying the last observation forward
    keeps every feature strictly causal.

    Returns the filled frame and a boolean frame marking what was imputed, so
    the fact of imputation can itself become a model feature.
    """
    was_missing = frame.isna()
    filled = frame.ffill(limit=ffill_limit)
    # Long gaps and leading NaNs: expanding median is causal (row t sees 0..t).
    fallback = frame.expanding(min_periods=1).median()
    filled = filled.fillna(fallback)
    return filled.fillna(0.0), was_missing


def coverage_report(rates: pd.DataFrame, *, since=None) -> pd.DataFrame:
    """Observed vs missing weeks per neighborhood. Used by docs and diagnostics."""
    view = rates.loc[rates.index >= since] if since is not None else rates
    return pd.DataFrame({
        "weeks": len(view),
        "observed": view.notna().sum(),
        "missing": view.isna().sum(),
        "pct_missing": (view.isna().sum() / max(len(view), 1) * 100).round(1),
        "mean_rate": view.mean().round(2),
    }).sort_values("missing", ascending=False)


# ---------------------------------------------------------------------------
# City-wide weekly covariates
# ---------------------------------------------------------------------------

def _map_ed_metric(name: str) -> str | None:
    """The type-1 ED file stores several series in `demographic_category`."""
    if "ili count" in name:
        return "ili_count"
    if "ed count" in name:
        return "ed_count"
    if "ili ed perc" in name or "ili ed percent" in name or "ili ed %" in name:
        return "ili_ed_perc"
    if "flu cases" in name:
        return "flu_cases"
    return None


def load_ili_share_type2() -> pd.Series:
    """ILI as a share of all ED visits, from the type-2 file. 436 weeks.

    The type-1 file carries this same quantity as its `ili ed perc` row, but
    stops 101 weeks earlier. The two are identical wherever they overlap --
    Pearson 1.0 and max absolute difference 0.0 across 335 weeks -- so type 2 is
    strictly the longer view of one series, not a second measurement of it.

    That matters because type 1 ends 2025-12-28, one week after the 2025-26 peak,
    while the evaluation window runs to 2026-05-03. Reading type 1 and carrying
    it forward pinned the covariate at its near-peak value of 10.33% for the last
    19 of 49 test weeks, while the truth fell to 1.28% -- an eight-fold collapse
    the model was told did not happen. See DATA_NOTES.md defect 3.
    """
    file = paths.require(paths.FLU_ED_TYPE2_FILE, "Influenza ED visits (type 2)")
    frame = pd.read_csv(file)
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["value_num"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.dropna(subset=["date", "value_num"])
    return frame.groupby("date")["value_num"].mean().sort_index()


def load_ed_metrics(week_index: pd.DatetimeIndex) -> pd.DataFrame:
    """City-wide weekly ILI/ED counts and percentages, aligned to `week_index`.

    `ili_ed_perc` comes from the type-2 file, which covers the whole series;
    every other column comes from type 1, which is the only source for them.
    """
    file = paths.require(paths.FLU_ED_TYPE1_FILE, "Influenza ED visits (type 1)")
    frame = pd.read_csv(file)
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["value_num"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["metric"] = (
        frame["demographic_category"].astype(str).str.strip().str.lower().map(_map_ed_metric)
    )
    frame = frame.dropna(subset=["date", "value_num", "metric"])
    wide = (
        frame.groupby(["date", "metric"])["value_num"].mean()
        .unstack("metric").sort_index()
        .reindex(columns=ED_METRICS)
    )

    # Swap in the longer series, and assert the two still agree where they
    # overlap. The assert is free today (they match exactly) and is what would
    # catch a future re-export that changed one file's definition but not the
    # other's -- at which point silently preferring type 2 would be wrong.
    share = load_ili_share_type2()
    if "ili_ed_perc" in wide.columns:
        both = pd.concat({"t1": wide["ili_ed_perc"], "t2": share}, axis=1).dropna()
        if len(both) and not np.allclose(both["t1"], both["t2"], atol=1e-6):
            worst = (both["t1"] - both["t2"]).abs().max()
            raise ValueError(
                "The type-1 and type-2 ED files disagree about ILI-as-a-share-of-ED-visits "
                f"by up to {worst:.4f} over {len(both)} shared weeks. They were identical "
                "when this path was written, so one of the two files has been re-exported "
                "with a different definition. Decide which is authoritative before "
                "trusting either -- do not just relax this tolerance."
            )
    # Widen onto the union of both indices first: type 2 runs 101 weeks past
    # type 1, and those weeks must exist as rows before the share can be written
    # into them, or the extra coverage is silently discarded.
    wide = wide.reindex(wide.index.union(share.index)).sort_index()
    wide["ili_ed_perc"] = share.reindex(wide.index)

    return _carry_forward(_align_weekly(wide, week_index), "ED visit metrics")


def load_monthly_cases(week_index: pd.DatetimeIndex) -> pd.Series:
    """City-wide monthly confirmed flu cases (Gender total), broadcast to weeks."""
    file = paths.require(paths.FLU_DEMOGRAPHICS_FILE, "Influenza demographics")
    frame = pd.read_csv(file)
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["value_num"] = pd.to_numeric(frame["value"], errors="coerce")
    gender = frame.loc[frame["demographic_category"].eq("Gender")].dropna(subset=["date", "value_num"])
    monthly = gender.groupby("date")["value_num"].sum().sort_index()
    aligned = _align_weekly(monthly.to_frame("monthly_cases"), week_index)
    return _carry_forward(aligned, "monthly demographic cases")["monthly_cases"]


def load_vaccination_global(week_index: pd.DatetimeIndex) -> pd.Series:
    """Statewide weekly cumulative influenza vaccination coverage (percent).

    Weekly resolution exists only statewide; Boston town-level data is one
    cumulative figure per season. The uptake curve resets each season, so this
    is a within-season ramp rather than a monotone series over the whole index.
    Values censored upstream as '< 1.0%' are read as 0.5%.
    """
    files = sorted(paths.VACCINATION_DIR.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No vaccination workbooks in {paths.VACCINATION_DIR}")

    frames: list[pd.DataFrame] = []
    for file in files:
        book = pd.ExcelFile(file)
        sheets = [s for s in book.sheet_names
                  if "Statewide Influenza" in s or "Previous Seasons Flu" in s]
        for sheet in sheets:
            part = book.parse(sheet)
            # Column order differs between workbook years; names do not.
            needed = {"Group", "Subgroup", "End Date", "Percent of MA residents vaccinated"}
            if not needed.issubset(part.columns):
                continue
            frames.append(part[list(needed)])
    if not frames:
        raise ValueError("No usable 'Statewide Influenza' sheets found in the vaccination workbooks.")

    combined = pd.concat(frames, ignore_index=True)
    # MA data uses inconsistent casing across years ('Total' vs 'total').
    combined["group_clean"] = combined["Group"].astype(str).str.strip().str.lower()
    combined["sub_clean"] = combined["Subgroup"].astype(str).str.strip().str.lower()
    total = combined.loc[combined["group_clean"].eq("total") | combined["sub_clean"].eq("total")]
    if total.empty:
        total = combined

    total = total.assign(
        date=pd.to_datetime(total["End Date"], errors="coerce"),
        pct=_parse_censored_percent(total["Percent of MA residents vaccinated"]),
    ).dropna(subset=["date", "pct"])

    weekly = total.groupby("date")["pct"].max().sort_index()
    aligned = _align_weekly(weekly.to_frame("vaccination"), week_index)["vaccination"]
    # Off-season weeks sit before each season's first report; 0 coverage is correct.
    return aligned.ffill().fillna(0.0)


def _parse_censored_percent(values: pd.Series) -> pd.Series:
    """'< 1.0%' -> 0.5, '12.3' -> 12.3, prose footnotes -> NaN."""
    text = values.astype(str).str.strip().str.replace("%", "", regex=False)
    censored = text.str.startswith("<")
    numeric = pd.to_numeric(text.where(~censored), errors="coerce")
    return numeric.mask(censored, 0.5)


# ---------------------------------------------------------------------------
# Per-neighborhood weekly features
# ---------------------------------------------------------------------------

def _align_weekly(frame: pd.DataFrame, week_index: pd.DatetimeIndex) -> pd.DataFrame:
    """Snap a series onto the flu week grid, tolerating a few days of offset.

    Backward-only. `method="nearest"` used to be allowed to reach FORWARD when a
    source observation was closer on the far side: with a 7-day tolerance the flu
    week beginning 2024-07-28 took its wastewater value from the week beginning
    2024-08-04, a full week in the future. `method="pad"` matches only source
    observations at or before the flu week, which is the causal direction and the
    only one a forecaster could use.

    Monthly sources relying on this to spread a value across a month are
    unaffected: they either ffill themselves before calling here
    (load_monthly_neighborhood) or are wrapped in _carry_forward afterwards
    (load_monthly_cases), and pad plus ffill is the same step function.
    """
    return frame.sort_index().reindex(week_index, method="pad", tolerance=pd.Timedelta("7D"))


# How stale a city-wide covariate is allowed to be before the loader stops
# pretending to know it. Values are weeks. A source may be carried forward this
# far past its last real observation -- roughly its publication lag, i.e. the
# staleness a forecaster would genuinely be working with -- and no further.
#
# The motivating failure: every city-wide covariate stopped on 2025-12-28, one
# week after the 2025-26 peak, and the old unbounded ffill pinned all five at
# their near-peak values for the last 19 of 49 test weeks. The model was told the
# epidemic held at its peak for 19 weeks while it fell eight-fold. Bounding the
# fill turns that from an invisible fabrication into a visible gap that z-scores
# to the training mean and is reported in run_config.json.
CARRY_FORWARD_LIMIT_WEEKS: dict[str, int] = {
    "ili_count": 2,
    "ed_count": 2,
    "ili_ed_perc": 2,
    "flu_cases": 2,
    "monthly_cases": 6,     # monthly source: one month of staleness is normal
    "vaccination": 2,
    "ED visit metrics": 2,
    "monthly demographic cases": 6,
    "influenza wastewater": 2,
    "covid wastewater": 2,
    "rsv wastewater": 2,
}
DEFAULT_CARRY_FORWARD_LIMIT_WEEKS = 2


def carry_forward_limit(what: str) -> int:
    return CARRY_FORWARD_LIMIT_WEEKS.get(what, DEFAULT_CARRY_FORWARD_LIMIT_WEEKS)


def _carry_forward(frame: pd.DataFrame, what: str, *, warn: bool = True,
                   limit: int | None = None) -> pd.DataFrame:
    """Forward-fill an under-covered covariate, but only so far, and say so.

    Several city-wide files stop short of the flu series. Filling those weeks
    with 0.0 is actively harmful -- these are large positive counts, so zero
    lands about nine standard deviations below the training mean and the model
    extrapolates wildly. Carrying the last observation forward is causal and
    keeps the covariate on-scale.

    But carrying it forward *without limit* is its own fabrication. The fill is
    therefore capped at `limit` weeks (default from CARRY_FORWARD_LIMIT_WEEKS);
    beyond that the covariate stays NaN, which downstream z-scoring maps to the
    training mean and which `coverage_report` counts.
    """
    if limit is None:
        limit = carry_forward_limit(what)
    missing_tail = int(frame.iloc[::-1].isna().all(axis=1).cumprod().sum())
    filled = frame.ffill(limit=limit) if limit else frame.copy()
    if warn and missing_tail:
        last = frame.dropna(how="all").index.max()
        beyond = max(0, missing_tail - limit)
        print(f"  note: {what} ends {last.date()}; {min(missing_tail, limit)} week(s) "
              f"carried forward and {beyond} week(s) left missing (limit {limit}w). "
              f"Treat covariate-dependent results in that span with care.")
    # bfill only at the head, where there is no earlier observation to carry.
    return filled.bfill(limit=limit) if limit else filled


def coverage_report(week_index: pd.DatetimeIndex, frame: pd.DataFrame,
                    *, test_start=None, test_end=None) -> dict[str, dict]:
    """Per-column coverage audit, for run_config.json.

    Records, per covariate, the last week with a real observation and how many
    weeks inside the evaluation window are missing after the bounded fill. This
    is the number that would have exposed the frozen-covariate defect on the
    first run rather than after three seasons of results.
    """
    report: dict[str, dict] = {}
    in_test = None
    if test_start is not None and test_end is not None:
        in_test = (week_index >= test_start) & (week_index <= test_end)
    for col in frame.columns:
        series = frame[col]
        real = series.dropna()
        entry = {
            "last_observed": str(real.index.max().date()) if len(real) else None,
            "n_missing_total": int(series.isna().sum()),
            "carry_forward_limit_weeks": carry_forward_limit(str(col)),
        }
        if in_test is not None:
            entry["n_missing_in_test_window"] = int(series[in_test].isna().sum())
            entry["n_test_weeks"] = int(in_test.sum())
        report[str(col)] = entry
    return report


def load_wastewater(week_index: pd.DatetimeIndex, source: str = "influenza") -> pd.DataFrame:
    """Weekly mean wastewater concentration index per neighborhood.

    `source` selects influenza, covid or rsv. Sampling is irregular (roughly
    every 2-4 days) so values are averaged within each week. Sewershed zones do
    not align with neighborhoods; see WASTEWATER_TO_IDX.

    Values are a concentration index, not a case count, despite `unit='count'`
    in the BPHC files. Weeks with no sample are NaN, not zero.
    """
    if source == "influenza":
        frame = _read_bphc_wastewater(paths.FLU_WASTEWATER_FILE, "Influenza wastewater")
    elif source == "rsv":
        frame = _read_bphc_wastewater(paths.RSV_WASTEWATER_FILE, "RSV wastewater")
    elif source == "covid":
        frame = _read_mwra_wastewater(paths.COVID_WASTEWATER_FILE)
    else:
        raise ValueError(f"Unknown wastewater source: {source!r}")

    rows: list[dict] = []
    for zone, group in frame.groupby("zone"):
        for node in WASTEWATER_TO_IDX.get(str(zone), []):
            rows.append(group.assign(node=node))
    if not rows:
        raise ValueError(f"No wastewater zones for source {source!r} matched WASTEWATER_TO_IDX.")
    expanded = pd.concat(rows, ignore_index=True)

    # Snap each sample to its SUNDAY-start week before averaging, matching the flu
    # week grid. Flooring to Monday (the pandas dayofweek origin) put the sample
    # window one day out of phase, and because _align_weekly matches with
    # method="nearest" the flu week beginning Sunday S was paired with the
    # Monday week S+1..S+7 -- whose last day is the first day of the horizon-1
    # TARGET week. That was a one-day look-ahead on all 93 covered weeks, inside
    # use_covid_wastewater, and so inside any arm enabling it. Same
    # expression as columbus.snap_to_week; see DATA_NOTES.md defect 4.
    expanded["week"] = expanded["date"] - pd.to_timedelta(
        (expanded["date"].dt.dayofweek + 1) % 7, unit="D")
    weekly = expanded.groupby(["week", "node"])["value"].mean().unstack("node")
    weekly = weekly.reindex(columns=range(N_NEIGH))
    aligned = _align_weekly(weekly, week_index)
    aligned.columns = NEIGHBORHOODS
    return aligned


def _read_bphc_wastewater(path: Path, what: str) -> pd.DataFrame:
    frame = pd.read_csv(paths.require(path, what))
    return pd.DataFrame({
        "date": pd.to_datetime(frame["date_value_start"], errors="coerce"),
        "value": pd.to_numeric(frame["value"], errors="coerce"),
        "zone": frame["demographic_value"].astype(str),
    }).dropna(subset=["date", "value"])


def _read_mwra_wastewater(path: Path) -> pd.DataFrame:
    """COVID wastewater uses an MWRA-style layout, not the BPHC long format.

    Columns are `date, site, eff, smooth, ...`. We take `eff` (the raw effective
    concentration): `smooth` is centred-smoothed, so using it would leak later
    weeks into each observation.
    """
    frame = pd.read_csv(paths.require(path, "COVID wastewater"))
    return pd.DataFrame({
        "date": pd.to_datetime(frame["date"], errors="coerce"),
        "value": pd.to_numeric(frame["eff"], errors="coerce"),
        "zone": frame["site"].astype(str),
    }).dropna(subset=["date", "value"])


def load_monthly_neighborhood(
    week_index: pd.DatetimeIndex,
    *,
    source: str,
    indicator: str | None = None,
    unit: str = "per 100,000 residents",
) -> pd.DataFrame:
    """Monthly per-neighborhood COVID or RSV series, broadcast onto weeks.

    These files are MONTHLY at neighborhood level, unlike the weekly influenza
    rates. The month's value is held flat across its weeks: a step function
    fabricates nothing, whereas interpolating would invent a within-month slope
    that the data does not contain.

    `unit` matters -- each COVID indicator appears in both count and rate units,
    distinguished only by that column, and RSV rates are per MILLION residents.
    """
    files = {
        "covid_cases": (paths.COVID_CASES_FILE, "COVID cases"),
        "covid_testing": (paths.COVID_TESTING_FILE, "COVID testing"),
        "rsv_cases": (paths.RSV_CASES_FILE, "RSV cases"),
    }
    if source not in files:
        raise ValueError(f"Unknown monthly source: {source!r}. Expected one of {sorted(files)}.")
    path, what = files[source]

    frame = pd.read_csv(paths.require(path, what))
    frame["date"] = pd.to_datetime(frame["date_value_start"], errors="coerce")
    frame["value_num"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.loc[frame["unit"].astype(str).str.strip().eq(unit)]
    if indicator is not None:
        frame = frame.loc[frame["indicator"].astype(str).str.strip().eq(indicator)]
    if frame.empty:
        raise ValueError(f"{what}: no rows with unit={unit!r} indicator={indicator!r}")

    frame["node"] = frame["demographic_value"].map(neighborhood_index)
    frame = frame.dropna(subset=["date", "value_num", "node"])
    frame["node"] = frame["node"].astype(int)

    monthly = frame.groupby(["date", "node"])["value_num"].mean().unstack("node")
    monthly = monthly.reindex(columns=range(N_NEIGH))
    # Hold each month's value flat over its weeks; ffill is the step function.
    stepped = monthly.reindex(monthly.index.union(week_index)).sort_index().ffill()
    aligned = stepped.reindex(week_index)
    aligned.columns = NEIGHBORHOODS
    return aligned


def load_weather(week_index: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    """Per-neighborhood weekly weather. Returns column -> (weeks, 14) array.

    Values are raw; normalisation is the caller's job so that the choice of
    train-only versus whole-series statistics stays visible at the call site.
    """
    directory = paths.require(paths.WEATHER_DIR, "Weather directory")
    files = sorted(glob.glob(str(directory / "*_weather_weekly.csv")))
    if not files:
        raise FileNotFoundError(f"No '*_weather_weekly.csv' files in {directory}")

    by_node: dict[int, list[pd.DataFrame]] = defaultdict(list)
    unmapped: list[str] = []
    for path in files:
        node = match_index(Path(path).name, WEATHER_KEYWORDS)
        if node is None:
            unmapped.append(Path(path).name)
            continue
        frame = pd.read_csv(path, parse_dates=["week_start"]).set_index("week_start").sort_index()
        by_node[node].append(frame[WEATHER_COLS])
    if unmapped:
        raise ValueError(f"Weather files not mapped to a neighborhood: {unmapped}")

    arrays: dict[str, np.ndarray] = {}
    for col in WEATHER_COLS:
        values = np.full((len(week_index), N_NEIGH), np.nan, dtype=np.float32)
        for node, frames in by_node.items():
            # Several files can map to one node (allston + brighton); average them.
            merged = pd.concat([f[[col]] for f in frames], axis=1).mean(axis=1)
            values[:, node] = _align_weekly(merged.to_frame(col), week_index)[col].to_numpy()
        # Weather is spatially smooth, so a city-wide median is a safe fill.
        arrays[col] = np.where(np.isnan(values), np.nanmedian(values), values)
    return arrays


# ---------------------------------------------------------------------------
# Static per-neighborhood demographics
# ---------------------------------------------------------------------------

def _load_city_csv(filename: str, value_cols: list[str]) -> tuple[pd.DataFrame, int]:
    """Read a City of Boston planning CSV and aggregate districts to our 14 nodes.

    These files carry a metadata preamble, so the real header row is located by
    finding the line containing 'GEOID'. The most recent YEAR is used.
    """
    path = paths.require(paths.NEIGHBORHOOD_DIR / filename, f"City of Boston file {filename}")
    skiprows = 0
    with open(path, "r") as handle:
        for i, line in enumerate(handle):
            if "GEOID" in line:
                skiprows = i
                break

    frame = pd.read_csv(path, skiprows=skiprows)
    frame["node"] = frame["GEOID"].map(GEOID_TO_IDX)
    frame = frame.dropna(subset=["node"])
    frame["node"] = frame["node"].astype(int)
    latest = frame["YEAR"].max()
    aggregated = frame.loc[frame["YEAR"].eq(latest)].groupby("node")[value_cols].sum()
    return aggregated, int(latest)


def _population_density() -> tuple[pd.Series, int]:
    """Correct per-node population density, and the source year.

    `_load_city_csv` sums its value columns across the planning districts that
    make up a node, which is right for counts and wrong for a ratio. Six of the
    fourteen nodes are multi-district, so summing the published
    'Population per square mile' column produced a number that is not a density:
    Back Bay/Beacon Hill/Downtown/North End/West End came out at 185,247 per
    square mile, roughly three times Manhattan and physically impossible, because
    it is five districts' densities added together.

    Land area is recoverable without any new data -- area = population / density
    per district -- so the density is rebuilt the only way a ratio of extensive
    quantities can be: sum the numerators, sum the denominators, then divide.

    This corrupted both the pop_density node feature and, through the
    median-pairwise-distance bandwidth in graphs.build_graph, the
    demographic-similarity edge weights. See DATA_NOTES.md defect 5.
    """
    path = paths.require(paths.NEIGHBORHOOD_DIR / "Population_in_Boston.csv",
                         "City of Boston file Population_in_Boston.csv")
    skiprows = 0
    with open(path, "r") as handle:
        for i, line in enumerate(handle):
            if "GEOID" in line:
                skiprows = i
                break
    frame = pd.read_csv(path, skiprows=skiprows)
    frame["node"] = frame["GEOID"].map(GEOID_TO_IDX)
    frame = frame.dropna(subset=["node"])
    frame["node"] = frame["node"].astype(int)
    latest = int(frame["YEAR"].max())
    frame = frame.loc[frame["YEAR"].eq(latest)].copy()

    frame["pop"] = frame["Male"] + frame["Female"]
    density = pd.to_numeric(frame["Population per square mile"], errors="coerce")
    # A district with zero recorded density carries no recoverable area; it also
    # contributes no meaningful population, so dropping it is safe. Guarding here
    # rather than dividing by zero keeps the failure visible if that changes.
    frame["area"] = (frame["pop"] / density.where(density > 0))
    totals = frame.groupby("node")[["pop", "area"]].sum(min_count=1)
    return totals["pop"] / totals["area"], latest


def load_static_demographics() -> tuple[np.ndarray, list[str], dict[str, int]]:
    """(14, 8) min-max normalised socio-economic matrix, plus source years."""
    years: dict[str, int] = {}

    pop, years["population"] = _load_city_csv(
        "Population_in_Boston.csv", ["Male", "Female", "Population per square mile"])
    age, years["age"] = _load_city_csv(
        "Age_in_Boston.csv",
        ["0-9 years", "10-19 years", "20-34 years", "35-54 years",
         "55-64 years", "65 years and over"])
    commute, years["commute"] = _load_city_csv(
        "Commute_Mode_in_Boston.csv",
        ["Public transit", "Walked", "Car, truck, or van - drove alone",
         "Car, truck, or van - carpooled", "Worked from home"])
    poverty, years["poverty"] = _load_city_csv(
        "Poverty_Status_in_Boston.csv", ["Below poverty line", "Above poverty line"])
    tenure, years["tenure"] = _load_city_csv(
        "Housing_Tenure_in_Boston.csv", ["Owner-occupied", "Renter-occupied"])
    vehicles, years["vehicles"] = _load_city_csv(
        "Vehicles_Available_in_Boston.csv", ["0 vehicles", "1+ vehicles"])
    race, years["race"] = _load_city_csv(
        "Race_and_Ethnicity_in_Boston.csv",
        ["White", "Black/African American", "Hispanic/Latino", "Asian/Pacific Islander"])

    age_total = age.sum(axis=1)
    commute_total = commute.sum(axis=1)
    race_total = race.sum(axis=1)

    density, years["population_density"] = _population_density()

    static = pd.DataFrame(index=range(N_NEIGH))
    static["pop_density"] = density
    static["poverty_rate"] = poverty["Below poverty line"] / (
        poverty["Below poverty line"] + poverty["Above poverty line"])
    static["transit_share"] = commute["Public transit"] / commute_total
    static["pct_children"] = (age["0-9 years"] + age["10-19 years"]) / age_total
    static["pct_elderly"] = age["65 years and over"] / age_total
    static["owner_rate"] = tenure["Owner-occupied"] / (
        tenure["Owner-occupied"] + tenure["Renter-occupied"])
    static["no_vehicle_rate"] = vehicles["0 vehicles"] / (
        vehicles["0 vehicles"] + vehicles["1+ vehicles"])
    static["nonwhite_share"] = 1 - (race["White"] / race_total)

    static = static[STATIC_DEMO_COLS].fillna(static.median())
    span = static.max() - static.min()
    normalized = ((static - static.min()) / span.where(span > 0)).fillna(0.5)
    return normalized.to_numpy(dtype=np.float32), STATIC_DEMO_COLS, years


def load_globals(week_index: pd.DatetimeIndex, names: Sequence[str]) -> pd.DataFrame:
    """City-wide weekly covariates for Boston, in the order requested.

    Factored out of samples.load_dataset so that each city owns the mapping from
    covariate name to source file. Boston's five all come from the BPHC
    dashboard exports; Columbus has an entirely different (and shorter) list.
    """
    if not names:
        return pd.DataFrame(index=week_index)
    columns: dict[str, pd.Series] = {}
    ed = load_ed_metrics(week_index)
    for name in names:
        if name in ed.columns:
            columns[name] = ed[name]
        elif name == "monthly_cases":
            columns[name] = load_monthly_cases(week_index)
        elif name == "vaccination":
            columns[name] = load_vaccination_global(week_index)
        else:
            raise ValueError(f"Unhandled global covariate for Boston: {name!r}")
    return pd.DataFrame(columns, index=week_index)
