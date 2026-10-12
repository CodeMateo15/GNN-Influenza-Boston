"""Chicago data access. Same duck-typed surface as the other cities.

`samples.load_dataset` calls `load_rates`, `load_weather`,
`load_static_demographics` and `load_globals` on whatever module a City names,
so this file's job is to present those four and nothing else.

Two honest limits, both properties of the source:

  1. `load_rates` returns an ACTIVITY LEVEL (1-10), not a rate. The name is
     the shared contract, not a claim about units; there is no denominator to
     divide by, and inventing one would be worse than saying so.
  2. There is no city-wide covariate. Summing an index across ZIPs is not a
     count, so `load_globals` refuses every name rather than offering a
     look-alike `ili_count`.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd

from .. import paths
from ..cities.chicago import ANCHOR_ZIPS, ZIPS
from ..constants import STATIC_DEMO_COLS, WEATHER_COLS


def load_rates() -> pd.DataFrame:
    """Weekly ILI activity level, weeks x 58 scored ZIPs, NaN where unpublished.

    The panel builder already completed the weekly grid, so the 19 city-wide
    missing weeks of 2020 are rows of NaN rather than gaps in the index. They
    are masked out of the loss and the metrics the same way Boston's suppressed
    cells are.
    """
    path = paths.require(paths.CHICAGO_PANEL_FILE, "Chicago weekly ILI panel")
    frame = pd.read_csv(path, parse_dates=["week_start"], dtype={"zip": str})
    wide = frame.pivot(index="week_start", columns="zip", values="ili_level")
    wide.columns.name = None
    wide.index.name = "date"
    missing = [z for z in ZIPS if z not in wide.columns]
    if missing:
        raise ValueError(f"Scored ZIPs absent from the panel: {missing}. Rebuild "
                         "with Code/scrapers/build_chicago_panel.py.")
    return wide.sort_index().reindex(columns=ZIPS).astype(float)


def load_static_demographics(path=None) -> tuple[np.ndarray, list[str], dict]:
    """Min-max scaled ACS demographics for the scored ZIPs: all eight columns.

    Same scaling as the other cities. A missing value -- in practice O'Hare,
    60666, which has no ZCTA because nobody lives there -- is filled with the
    city median before scaling, which is Boston's rule in data.py.
    """
    path = paths.require(path or paths.CHICAGO_STATIC_FILE, "Chicago static table")
    frame = pd.read_csv(path, comment="#", dtype={"zip": str}).set_index("zip")
    columns = [c for c in STATIC_DEMO_COLS if c in frame.columns]
    static = frame.reindex(ZIPS)[columns]
    static = static.fillna(static.median())
    span = (static.max() - static.min()).replace(0, 1.0)
    normalized = (static - static.min()) / span
    return normalized.to_numpy(dtype=np.float32), columns, {}


def load_weather(week_index: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    """Per-ZIP weekly weather. Returns column -> (weeks, n_nodes) array.

    The scraper writes a file for every ZIP with a polygon, anchor included, so
    a rebuilt panel that promotes the anchor finds its weather already there.
    Anchor files are therefore expected and skipped; anything else unmapped is
    an error.
    """
    directory = paths.require(paths.CHICAGO_WEATHER_DIR, "Chicago weather directory")
    files = sorted(glob.glob(str(directory / "*_weather_weekly.csv")))
    if not files:
        raise FileNotFoundError(f"No '*_weather_weekly.csv' files in {directory}. Run "
                                "Code/scrapers/scrape_weather_chicago.py first.")

    node_of = {z: i for i, z in enumerate(ZIPS)}
    by_node: dict[int, pd.DataFrame] = {}
    unmapped: list[str] = []
    for path in files:
        key = Path(path).name.removesuffix("_weather_weekly.csv")
        if key in ANCHOR_ZIPS:
            continue
        if key not in node_of:
            unmapped.append(Path(path).name)
            continue
        by_node[node_of[key]] = (pd.read_csv(path, parse_dates=["week_start"])
                                 .set_index("week_start").sort_index()[WEATHER_COLS])
    if unmapped:
        raise ValueError(f"Weather files not mapped to a ZIP: {unmapped}")
    missing = [z for i, z in enumerate(ZIPS) if i not in by_node]
    if missing:
        raise ValueError(f"No weather file for {missing}.")

    arrays: dict[str, np.ndarray] = {}
    for column in WEATHER_COLS:
        stacked = np.column_stack([
            by_node[i][column].reindex(week_index).to_numpy(dtype=float)
            for i in range(len(ZIPS))
        ])
        # Same fill as every other city: the week's city-wide median.
        medians = np.nanmedian(stacked, axis=1)
        gaps = np.isnan(stacked)
        stacked[gaps] = np.take(medians, np.where(gaps)[0])
        arrays[column] = stacked
    return arrays


def load_globals(week_index: pd.DatetimeIndex, names) -> pd.DataFrame:
    """City-wide covariates. Chicago has none; see the module docstring."""
    names = list(names)
    if names:
        raise ValueError(f"Chicago has no city-wide covariate (asked for {names}). "
                         "The source is a per-ZIP index with no count behind it.")
    return pd.DataFrame(index=week_index)
