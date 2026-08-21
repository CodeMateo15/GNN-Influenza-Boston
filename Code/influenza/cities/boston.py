"""Boston's city profile: the 14 BPHC neighborhoods, 7 anchors and their edges.

Every literal below was moved verbatim out of `influenza/constants.py` when the
second city was added -- not retyped -- so the values are provably the ones every
committed result was produced with. `constants.py` imports them back under their
original names, which is why no existing call site had to change.

The name crosswalks (BPHC_KEYWORDS, WEATHER_KEYWORDS, WASTEWATER_TO_IDX,
GEOID_TO_IDX) live here rather than as City fields because they describe how to
read *Boston's specific source files*. Columbus has no analogue: its geography
arrives as a ZIP code resolved through an explicit crosswalk table rather than by
substring matching. See loaders/columbus_crosswalk.py.
"""

from __future__ import annotations

from . import City

# --- 14 canonical neighborhoods used as graph nodes (indices 0..13) ----------
# Only these are predicted and scored. Anchors live at index 14.. so the
# pred[:N_NEIGH] slice used throughout stays safe.
NEIGHBORHOODS = [
    "Allston/Brighton",
    "Back Bay/Beacon Hill/Downtown/North End/West End",
    "Charlestown",
    "Dorchester",
    "East Boston",
    "Fenway",
    "Hyde Park",
    "Jamaica Plain",
    "Mattapan",
    "Roslindale",
    "Roxbury",
    "South Boston",
    "South End",
    "West Roxbury",
]

# Short labels for plots. This is the notebook set (documented in docs/), which
# differs cosmetically from the one the baselines used ('Charles.' vs
# 'Charlestown', 'JP' vs 'JamaicaPlain'). Always join on NEIGHBORHOODS.
SHORT_NAMES = [
    "Allston", "BackBay+", "Charles.", "Dorchest.", "E.Boston",
    "Fenway", "HydePark", "JP", "Mattapan", "Roslind.",
    "Roxbury", "S.Boston", "S.End", "W.Roxbury",
]

N_NEIGH = len(NEIGHBORHOODS)

# --- Surrounding-area anchor nodes ------------------------------------------
# Feature-less boundary "sinks" that smooth edge-of-city neighborhoods. They
# carry no flu data and are excluded from the loss and every metric.
ANCHOR_NAMES = [
    "Cambridge/Somerville",
    "Charles River",
    "Chelsea/Revere/Winthrop",
    "Boston Harbor",
    "South Suburbs (Milton/Quincy)",
    "West Suburbs (Newton/Dedham)",
    "Brookline",
]
ANCHOR_SHORT = [
    "Camb/Somer", "CharlesR", "Chelsea+", "Harbor",
    "S.Suburbs", "W.Suburbs", "Brookline",
]

# The older single-anchor scheme, kept so the geo-only baseline stays runnable.
BACKGROUND_SHORT = "Background"

# --- BPHC CSV name -> canonical index --------------------------------------
# Ordered longest-first so "west roxbury" matches before "roxbury". The two
# Dorchester ZIP rows both map to 3 and are averaged.
BPHC_KEYWORDS: list[tuple[str, int]] = [
    ("west roxbury", 13),
    ("south boston", 11),
    ("south end", 12),
    ("east boston", 4),
    ("hyde park", 6),
    ("jamaica plain", 7),
    ("bb/bh/dt/ne/we", 1),
    ("back bay", 1),
    ("beacon hill", 1),
    ("downtown", 1),
    ("north end", 1),
    ("west end", 1),
    ("allston", 0),
    ("brighton", 0),
    ("charlestown", 2),
    ("dorchester", 3),
    ("dor ", 3),
    ("dor(", 3),
    ("fenway", 5),
    ("mattapan", 8),
    ("roslindale", 9),
    ("roxbury", 10),
]

# Weather filenames use underscores instead of spaces/slashes.
WEATHER_KEYWORDS: list[tuple[str, int]] = [
    ("west_roxbury", 13), ("south_boston", 11), ("south_end", 12),
    ("east_boston", 4), ("hyde_park", 6), ("jamaica_plain", 7),
    ("back_bay", 1), ("beacon_hill", 1), ("downtown", 1),
    ("north_end", 1), ("west_end", 1), ("bb_bh_dt_ne_we", 1),
    ("allston", 0), ("brighton", 0), ("charlestown", 2),
    ("dorchester", 3), ("fenway", 5), ("mattapan", 8),
    ("roslindale", 9), ("roxbury", 10),
]

# --- Wastewater sewershed -> canonical indices ------------------------------
# Sewersheds do not align with neighborhood boundaries, so one zone can cover
# several nodes. The Back Bay zone is the established stand-in for Fenway,
# South Boston and South End, which have no sewershed of their own; without it
# those three nodes would have no wastewater signal at all. Shared by all three
# wastewater files (influenza, COVID, RSV) -- their geography sets are equal.
WASTEWATER_TO_IDX: dict[str, list[int]] = {
    "Allston/Brighton": [0],
    "Back Bay": [1, 5, 11, 12],
    "Charlestown": [2],
    "Dorchester": [3],
    "East Boston": [4],
    "Hyde Park": [6],
    "Jamaica Plain": [7],
    "Mattapan": [8],
    "Roslindale/West Roxbury": [9, 13],
    "Roxbury": [10],
}
# 'Boston' (citywide aggregate) and 'NA' are deliberately absent -> dropped.

# --- City of Boston planning-district name -> canonical index ---------------
GEOID_TO_IDX: dict[str, int] = {
    "Allston": 0, "Brighton": 0,
    "Back Bay": 1, "Beacon Hill": 1, "Downtown": 1, "North End": 1, "West End": 1,
    "Charlestown": 2,
    "Dorchester": 3,
    "East Boston": 4,
    "Fenway": 5, "Longwood": 5,
    "Hyde Park": 6,
    "Jamaica Plain": 7,
    "Mattapan": 8,
    "Roslindale": 9,
    "Mission Hill": 10, "Roxbury": 10,
    "South Boston": 11, "South Boston Waterfront": 11,
    "Chinatown": 12, "South End": 12,
    "West Roxbury": 13,
}

# --- Approximate centroids (lon, lat) for plotting only --------------------
COORDS: dict[str, tuple[float, float]] = {
    "Allston": (-71.1310, 42.3535),
    "BackBay+": (-71.0680, 42.3550),
    "Charles.": (-71.0600, 42.3780),
    "Dorchest.": (-71.0560, 42.3000),
    "E.Boston": (-71.0200, 42.3750),
    "Fenway": (-71.1000, 42.3430),
    "HydePark": (-71.1250, 42.2560),
    "JP": (-71.1150, 42.3100),
    "Mattapan": (-71.0940, 42.2720),
    "Roslind.": (-71.1350, 42.2830),
    "Roxbury": (-71.0870, 42.3270),
    "S.Boston": (-71.0380, 42.3350),
    "S.End": (-71.0700, 42.3400),
    "W.Roxbury": (-71.1580, 42.2790),
    "Camb/Somer": (-71.1000, 42.3950),
    "CharlesR": (-71.0750, 42.3680),
    "Chelsea+": (-71.0050, 42.4000),
    "Harbor": (-70.9850, 42.3450),
    "S.Suburbs": (-71.0850, 42.2350),
    "W.Suburbs": (-71.1900, 42.3100),
    "Brookline": (-71.1300, 42.3300),
    BACKGROUND_SHORT: (-71.0000, 42.3500),
}

# --- Geographic adjacency, hand-coded from the Boston map ------------------
# 23 neighborhood-neighborhood pairs.
GEO_EDGES_NEIGHBORHOOD: list[tuple[str, str]] = [
    ("Allston", "BackBay+"), ("Allston", "Fenway"), ("Allston", "JP"),
    ("BackBay+", "Fenway"), ("BackBay+", "S.End"), ("BackBay+", "Charles."),
    ("BackBay+", "S.Boston"),
    ("Charles.", "E.Boston"),
    ("Dorchest.", "S.Boston"), ("Dorchest.", "Roxbury"), ("Dorchest.", "Mattapan"),
    ("Dorchest.", "S.End"),
    ("Fenway", "S.End"), ("Fenway", "Roxbury"),
    ("HydePark", "Mattapan"), ("HydePark", "Roslind."), ("HydePark", "W.Roxbury"),
    ("JP", "Roxbury"), ("JP", "Roslind."),
    ("Mattapan", "Roxbury"),
    ("Roslind.", "W.Roxbury"),
    ("Roxbury", "S.End"),
    ("S.Boston", "S.End"),
]

# 21 anchor pairs: each anchor -> the Boston neighborhoods it borders.
GEO_EDGES_ANCHOR: list[tuple[str, str]] = [
    ("Allston", "Camb/Somer"), ("BackBay+", "Camb/Somer"), ("Charles.", "Camb/Somer"),
    ("Allston", "CharlesR"), ("BackBay+", "CharlesR"), ("Charles.", "CharlesR"),
    ("E.Boston", "Chelsea+"), ("Charles.", "Chelsea+"),
    ("E.Boston", "Harbor"), ("S.Boston", "Harbor"), ("Dorchest.", "Harbor"),
    ("HydePark", "S.Suburbs"), ("Mattapan", "S.Suburbs"), ("Dorchest.", "S.Suburbs"),
    ("Allston", "W.Suburbs"), ("W.Roxbury", "W.Suburbs"), ("Roslind.", "W.Suburbs"),
    ("Allston", "Brookline"), ("Fenway", "Brookline"), ("JP", "Brookline"),
    ("W.Roxbury", "Brookline"),
]

# 3 edges for the legacy single-background scheme.
GEO_EDGES_BACKGROUND: list[tuple[str, str]] = [
    ("E.Boston", BACKGROUND_SHORT),
    ("S.Boston", BACKGROUND_SHORT),
    ("Charles.", BACKGROUND_SHORT),
]


BOSTON = City(
    name="boston",
    label="Boston",
    node_label="neighborhood",
    node_names=tuple(NEIGHBORHOODS),
    short_names=tuple(SHORT_NAMES),
    anchor_names=tuple(ANCHOR_NAMES),
    anchor_short=tuple(ANCHOR_SHORT),
    background_short=BACKGROUND_SHORT,
    geo_edges=tuple(GEO_EDGES_NEIGHBORHOOD),
    geo_edges_anchor=tuple(GEO_EDGES_ANCHOR),
    geo_edges_background=tuple(GEO_EDGES_BACKGROUND),
    coords=dict(COORDS),
    loader_module="influenza.data",
    available_globals=("ili_count", "ed_count", "ili_ed_perc", "flu_cases",
                       "monthly_cases", "vaccination"),
    available_features=frozenset({
        "weather", "demographics", "wastewater", "covid_cases", "covid_testing",
        "covid_wastewater", "rsv_cases", "rsv_wastewater", "rt", "seasonality",
        "imputed_flag",
    }),
    variants=("exclude_covid", "post_covid", "full"),
    suppresses_small_counts=True,
)
