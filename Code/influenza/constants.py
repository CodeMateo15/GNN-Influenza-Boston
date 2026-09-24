"""Node definitions, graph topology, name crosswalks and shared date constants.

Single source of truth for everything that used to be copy-pasted between the
two baseline scripts and the eight notebooks. See docs/EDGES_AND_NODES_NOTES.txt
for the reasoning behind the anchor nodes and each edge type.
"""

from __future__ import annotations

import pandas as pd

# --- Boston's profile ------------------------------------------------------
# These names now physically live in cities/boston.py and are re-exported here so
# that every pre-existing `from .constants import NEIGHBORHOODS` keeps working
# untouched. Anything genuinely shared between cities -- the evaluation window,
# the feature column lists, the seeds -- stays defined below.
from .cities.boston import (  # noqa: E402,F401
    ANCHOR_NAMES,
    ANCHOR_SHORT,
    BACKGROUND_SHORT,
    BPHC_KEYWORDS,
    COORDS,
    GEOID_TO_IDX,
    GEO_EDGES_ANCHOR,
    GEO_EDGES_BACKGROUND,
    GEO_EDGES_NEIGHBORHOOD,
    NEIGHBORHOODS,
    N_NEIGH,
    SHORT_NAMES,
    WASTEWATER_TO_IDX,
    WEATHER_KEYWORDS,
)

# --- Dates -----------------------------------------------------------------
# Unified evaluation window: a full year, so the test set contains both an
# off-season and a flu season. Segments are computed from these same
# predictions rather than by re-running on a narrower window.
TEST_START = pd.Timestamp("2025-05-31")
TEST_END = pd.Timestamp("2026-05-31")

COVID_START = pd.Timestamp("2020-03-01")
COVID_END = pd.Timestamp("2022-06-30")
POST_COVID_START = pd.Timestamp("2022-07-01")

# End of flu season set to March; see docs/EDGES_AND_NODES_NOTES.txt section 6.
FLU_MONTHS = frozenset({10, 11, 12, 1, 2, 3})
SEGMENTS = ("overall", "flu_season", "off_season")

# --- Modelling defaults ----------------------------------------------------
LOOKBACK = 8
HORIZONS = (1, 2)
SEED = 42
MC_SEED = 123

WEATHER_COLS = [
    "temp_mean_c", "temp_max_c", "temp_min_c",
    "relative_humidity_mean", "precipitation_sum_mm", "wind_speed_max_kmh",
]

STATIC_DEMO_COLS = [
    "pop_density", "poverty_rate", "transit_share", "pct_children",
    "pct_elderly", "owner_rate", "no_vehicle_rate", "nonwhite_share",
]
