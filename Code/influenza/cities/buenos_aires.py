"""Buenos Aires / AMBA profile: 19 scored partidos, 5 anchors, derived edges.

The node set is the 24 partidos of the Conurbano Bonaerense that Argentina's
SNVS respiratory surveillance reports ETI (enfermedad tipo influenza) for. They
split on reporting coverage rather than by hand: the 19 partidos that reported
in at least 90% of weeks are scored nodes, the 5 below that are anchors. That
is the same rule Columbus uses -- thin, peripheral reporting is exactly the
anchor role -- except that here it is measured from the panel rather than read
off a crosswalk's unassigned list.

Alphabetical within each group, so the node indices that saved checkpoints and
the `pred[:n_neigh]` slice depend on are stable.

Three things differ from the two US cities, and all three are load-bearing:

  * SOUTHERN HEMISPHERE. Verified from the panel, not assumed: the citywide
    curve peaks in epiweeks 22-24 every year (2022 SE22, 2023 SE23, 2024 SE22,
    2025 SE24) and monthly means put the season at April-September -- an exact
    six-month mirror of Boston's October-March. `flu_months` and
    `season_start_month` carry that; nothing else in the project needs to know.

  * FIVE DEMOGRAPHIC COLUMNS, NOT EIGHT. INDEC publishes density, age
    structure, tenure and health coverage per partido; the 2022 census asks
    nothing about commute mode or vehicles, and has no construct matching
    `nonwhite_share`. So the static block is five columns wide here --
    pop_density, poverty_rate (no-health-coverage proxy), pct_children
    (under-15, derived), pct_elderly, owner_rate -- and the loader names them
    so the feature labels line up.

  * COUNTS, NOT A PUBLISHED RATE. Like Columbus and unlike Boston, the source
    is case counts. Unlike Columbus, an absent partido-week is not
    automatically a zero: the builder treats an isolated absence as a true zero
    but a run of three or more as a reporting blackout and leaves it NaN. That
    makes Buenos Aires behave like Boston for suppression purposes.

Data notes are in Code/docs/AMBA_DATA_NOTES.md.
"""

from __future__ import annotations

import csv

from .. import paths
from . import City

# --- Node set ---------------------------------------------------------------
# Read from the coverage table the panel builder writes, so the 0.90 rule lives
# in exactly one place. A hand-copied list here would drift the first time the
# panel is rebuilt with a newer SNVS vintage.


def _coverage_split() -> tuple[list[str], list[str]]:
    core: list[str] = []
    fringe: list[str] = []
    with open(paths.AMBA_COVERAGE_FILE, newline="") as handle:
        for row in csv.DictReader(handle):
            (core if row["keep_core"].strip().lower() == "true" else fringe).append(
                row["partido"])
    return sorted(core), sorted(fringe)


PARTIDOS, ANCHOR_NAMES = _coverage_split()

# Plot labels. Accents kept -- they are part of the names, matplotlib renders
# them, and stripping them would make the labels disagree with every table.
SHORT_OF = {
    "ALMIRANTE BROWN": "AlmBrown",
    "AVELLANEDA": "Avellan.",
    "BERAZATEGUI": "Berazat.",
    "ESTEBAN ECHEVERRÍA": "E.Echev.",
    "EZEIZA": "Ezeiza",
    "FLORENCIO VARELA": "F.Varela",
    "GENERAL SAN MARTÍN": "S.Martín",
    "HURLINGHAM": "Hurling.",
    "ITUZAINGÓ": "Ituzaingó",
    "JOSÉ C. PAZ": "J.C.Paz",
    "LA MATANZA": "LaMatanza",
    "LANÚS": "Lanús",
    "LOMAS DE ZAMORA": "LomasZam.",
    "MALVINAS ARGENTINAS": "MalvArg.",
    "MERLO": "Merlo",
    "MORENO": "Moreno",
    "MORÓN": "Morón",
    "QUILMES": "Quilmes",
    "SAN FERNANDO": "S.Fernando",
    "SAN ISIDRO": "S.Isidro",
    "SAN MIGUEL": "S.Miguel",
    "TIGRE": "Tigre",
    "TRES DE FEBRERO": "TresFeb.",
    "VICENTE LÓPEZ": "V.López",
}

SHORT_NAMES = [SHORT_OF[name] for name in PARTIDOS]
ANCHOR_SHORT = [SHORT_OF[name] for name in ANCHOR_NAMES]

# Everything outside the 24 conurbano partidos: the rest of the province, and
# the Autonomous City of Buenos Aires, which the province's surveillance does
# not cover and which is not a node here. Several scored partidos border CABA
# directly, so this is a real sink rather than a formality.
BACKGROUND_SHORT = "Outside"


# --- Geographic adjacency, derived --------------------------------------------
# From Code/scrapers/derive_amba_adjacency.py, which reads IGN boundary
# polygons and calls two partidos adjacent when they share at least two
# boundary vertices.
#
# Read from the CSV at import rather than pasted in as a literal. Columbus does
# the opposite -- its scraper writes columbus_area_edges.csv and then nothing
# reads it, while the live edge list is a hand-synced literal whose docstring
# has already gone stale relative to the scraper. One source, no sync step.


def _load_edges() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(scored-scored pairs, scored-anchor pairs) on SHORT names."""
    scored = set(PARTIDOS)
    neighbourhood: list[tuple[str, str]] = []
    anchored: list[tuple[str, str]] = []
    with open(paths.AMBA_EDGES_FILE, newline="") as handle:
        rows = csv.DictReader(row for row in handle if not row.startswith("#"))
        for row in rows:
            a, b = row["partido_a"], row["partido_b"]
            pair = (SHORT_OF[a], SHORT_OF[b])
            if a in scored and b in scored:
                neighbourhood.append(pair)
            else:
                # Order anchor pairs scored-first, matching the other cities.
                anchored.append(pair if a in scored else (pair[1], pair[0]))
    return sorted(neighbourhood), sorted(anchored)


GEO_EDGES_PARTIDO, GEO_EDGES_ANCHOR = _load_edges()

# Every anchor also drains to the background, as in Boston and Columbus: an
# anchor is a boundary sink, and the boundary continues past it.
GEO_EDGES_BACKGROUND = [(short, BACKGROUND_SHORT) for short in ANCHOR_SHORT]


# --- Centroids ----------------------------------------------------------------
# From the Argentine government's georef API (apis.datos.gob.ar), keyed on the
# same INDEC department code as everything else. Used for the weather pull and
# for the diagnostic graph plot, not for adjacency -- that comes from the
# polygons, not from distances between centres.
COORDS: dict[str, tuple[float, float]] = {
    "AlmBrown":   (-58.3961, -34.8229),
    "Avellan.":   (-58.3630, -34.6773),
    "Berazat.":   (-58.1358, -34.8194),
    "E.Echev.":   (-58.4548, -34.8776),
    "Ezeiza":     (-58.5324, -34.8846),
    "F.Varela":   (-58.2107, -34.9519),
    "S.Martín":   (-58.5339, -34.5714),
    "Hurling.":   (-58.6394, -34.5928),
    "Ituzaingó":  (-58.6746, -34.6585),
    "J.C.Paz":    (-58.7599, -34.5147),
    "LaMatanza":  (-58.6297, -34.7705),
    "Lanús":      (-58.3946, -34.7062),
    "LomasZam.":  (-58.4066, -34.7626),
    "MalvArg.":   (-58.7078, -34.4914),
    "Merlo":      (-58.7284, -34.6820),
    "Moreno":     (-58.7896, -34.6396),
    "Morón":      (-58.6196, -34.6534),
    "Quilmes":    (-58.2639, -34.7404),
    "S.Fernando": (-58.5591, -34.4416),
    "S.Isidro":   (-58.5122, -34.4720),
    "S.Miguel":   (-58.7118, -34.5433),
    "Tigre":      (-58.5796, -34.4090),
    "TresFeb.":   (-58.5665, -34.6009),
    "V.López":    (-58.4781, -34.5261),
    BACKGROUND_SHORT: (-58.5000, -34.6600),
}


BUENOS_AIRES = City(
    name="buenos_aires",
    label="Buenos Aires",
    node_label="partido",
    node_names=tuple(PARTIDOS),
    short_names=tuple(SHORT_NAMES),
    anchor_names=tuple(ANCHOR_NAMES),
    anchor_short=tuple(ANCHOR_SHORT),
    background_short=BACKGROUND_SHORT,
    geo_edges=tuple(GEO_EDGES_PARTIDO),
    geo_edges_anchor=tuple(GEO_EDGES_ANCHOR),
    geo_edges_background=tuple(GEO_EDGES_BACKGROUND),
    coords=dict(COORDS),
    loader_module="influenza.loaders.buenos_aires",
    # SNVS reports ETI case counts and nothing else. No hospitalisation series,
    # no ED-visit denominator, no confirmed-case count.
    available_globals=("ili_count",),
    # No RSV, no COVID, no wastewater, no vaccination series for AMBA in this
    # repository. Demographics are available, five columns wide.
    available_features=frozenset({"weather", "seasonality", "demographics"}),
    # The panel starts 2022-01-02, so there is no pre-COVID history to include
    # or exclude -- the same situation as Columbus.
    variants=("post_covid",),
    # A run of >=3 absent weeks is a reporting blackout and stays NaN, so this
    # city behaves like Boston rather than like Columbus.
    suppresses_small_counts=True,
    # Southern hemisphere: the season runs April-September and the annual floor
    # is December-February, so a new season starts in February.
    flu_months=frozenset({4, 5, 6, 7, 8, 9}),
    season_start_month=2,
    # A full year ending at the last week the loader judges fully reported.
    # SNVS backfills for about four months, so the shared 2025-06..2026-05
    # window would score four months of still-arriving counts as model error.
    # This window covers the whole 2025 season (peak 2025-06-08) and leaves 148
    # weeks of history to train on.
    test_start="2024-11-03",
    test_end="2025-11-02",
    notes="19 of 24 AMBA partidos at >=90% reporting coverage; weekly ETI "
          "2022-01-02 onward from Argentina's SNVS.",
)
