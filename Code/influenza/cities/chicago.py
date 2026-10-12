"""Chicago profile: 58 scored ZIPs, 1 anchor, edges and centroids derived.

The node set is the 59 ZIPs that both the City of Chicago's "Influenza Risk
Level by ZIP Code" table and its ZIP polygons cover (60106, which has rows but
no polygon, is dropped by the panel builder). The scored/anchor split is the
Buenos Aires coverage rule unchanged -- at least 90% of panel weeks reported --
read from the coverage table the builder writes. It makes exactly one anchor:
60827 (Riverdale / Calumet Park), on the southern city limit, which only joined
the feed in September 2020 (0.858 coverage). Within the post-COVID window it is
complete, so the split would be 59/0 if coverage were measured there instead;
the rule was kept as Buenos Aires defines it rather than re-tuned per city.

ZIP codes serve as both node names and plot labels: there is no shorter name.

Three things differ from the other cities, and all three are load-bearing:

  * THE TARGET IS AN INDEX, NOT A RATE. Each value is a 1-10 ILI activity
    level -- a ZIP's ED-visit ILI share against its own summer mean, about one
    SD per level, capped at 10. The loader passes it through unchanged. MAE,
    RMSE and WIS are therefore in levels, not per 100,000, and the cap makes
    the top of every strong season a plateau of 10s.

  * MISSING IS MISSING. No count means no "zero cases" reading, so every absent
    ZIP-week is NaN (`suppresses_small_counts=True`), like Boston's suppressed
    cells. In practice that is the 19-week city-wide gap of May-September 2020
    and 60827's late start.

  * HISTORY BEFORE COVID, BUT BARELY. The panel starts 2019-09-29: half of one
    pre-COVID season. `post_covid` is the modelling variant, as everywhere
    else. `full` is also allowed, because it is the only variant that can
    train the 2022-23 and 2023-24 backtest folds -- the same reason Boston's
    backtest runs on `full`.

Data notes are in Code/docs/CHICAGO_DATA_NOTES.md.
"""

from __future__ import annotations

import csv

from .. import paths
from . import City


def _read(path) -> list[dict]:
    with open(path, newline="") as handle:
        return list(csv.DictReader(row for row in handle if not row.startswith("#")))


# --- Node set ---------------------------------------------------------------
# From the coverage table, so the 0.90 rule lives in build_chicago_panel.py only.


def _coverage_split() -> tuple[list[str], list[str]]:
    core: list[str] = []
    fringe: list[str] = []
    for row in _read(paths.CHICAGO_COVERAGE_FILE):
        (core if row["keep_core"].strip().lower() == "true" else fringe).append(row["zip"])
    return sorted(core), sorted(fringe)


ZIPS, ANCHOR_ZIPS = _coverage_split()
SHORT_NAMES = list(ZIPS)
ANCHOR_SHORT = list(ANCHOR_ZIPS)

# Everything past the city limit, and the lake.
BACKGROUND_SHORT = "Outside"


# --- Geographic adjacency, derived --------------------------------------------
# From Code/scrapers/derive_chicago_adjacency.py (shared-boundary rule on the
# City's polygons), read at import as Buenos Aires does: one edge list, no
# hand-synced literal.


def _load_edges() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(scored-scored pairs, scored-anchor pairs)."""
    scored = set(ZIPS)
    neighbourhood: list[tuple[str, str]] = []
    anchored: list[tuple[str, str]] = []
    for row in _read(paths.CHICAGO_EDGES_FILE):
        a, b = row["zip_a"], row["zip_b"]
        if a in scored and b in scored:
            neighbourhood.append((a, b))
        elif a in scored or b in scored:
            anchored.append((a, b) if a in scored else (b, a))
    return sorted(neighbourhood), sorted(anchored)


GEO_EDGES_ZIP, GEO_EDGES_ANCHOR = _load_edges()


# --- Centroids and the city edge ------------------------------------------------
# Same derive script. COORDS is (lon, lat), the convention every city uses.
_CENTROIDS = _read(paths.CHICAGO_CENTROIDS_FILE)
COORDS: dict[str, tuple[float, float]] = {
    row["zip"]: (float(row["lon"]), float(row["lat"])) for row in _CENTROIDS}
COORDS[BACKGROUND_SHORT] = (-87.6800, 41.8400)

# The "single" anchor scheme drains the SCORED ZIPs on the city edge into the
# background node, as Boston's and Columbus's background edges do. These must
# name scored nodes only: under "single" the anchors are not in the graph.
GEO_EDGES_BACKGROUND = sorted(
    (row["zip"], BACKGROUND_SHORT) for row in _CENTROIDS
    if row["on_city_edge"].strip().lower() == "true" and row["zip"] in set(ZIPS))


CHICAGO = City(
    name="chicago",
    label="Chicago",
    node_label="ZIP",
    node_names=tuple(ZIPS),
    short_names=tuple(SHORT_NAMES),
    anchor_names=tuple(ANCHOR_ZIPS),
    anchor_short=tuple(ANCHOR_SHORT),
    background_short=BACKGROUND_SHORT,
    geo_edges=tuple(GEO_EDGES_ZIP),
    geo_edges_anchor=tuple(GEO_EDGES_ANCHOR),
    geo_edges_background=tuple(GEO_EDGES_BACKGROUND),
    coords=dict(COORDS),
    loader_module="influenza.loaders.chicago",
    # The portal publishes the activity level and nothing else: no counts, no
    # ED-visit denominator, so there is no honest city-wide `ili_count`.
    available_globals=(),
    # ACS demographics (scrape_acs_chicago.py) because four frozen backtest
    # arms read them; no RSV, COVID, wastewater or vaccination series.
    available_features=frozenset({"weather", "seasonality", "demographics"}),
    variants=("post_covid", "full"),
    suppresses_small_counts=True,
    # Northern-hemisphere defaults: Oct-Mar season, named from August.
    flu_months=frozenset({10, 11, 12, 1, 2, 3}),
    season_start_month=8,
    # The shared 2025-06..2026-05 window. The feed runs to 2026-09-20, so the
    # window's last week is sixteen weeks old: unlike Buenos Aires, there is no
    # still-arriving tail to score as model error. (The portal calls all of its
    # data provisional; nothing here measures how much it is later revised.)
    test_start=None,
    test_end=None,
    notes="58 of 59 Chicago ZIPs at >=90% reporting coverage; weekly 1-10 ILI "
          "activity level 2019-09-29 onward from CDPH / Illinois ESSENCE.",
)
