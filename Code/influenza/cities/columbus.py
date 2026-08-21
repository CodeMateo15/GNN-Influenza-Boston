"""Columbus / Franklin County profile: 17 areas, 3 anchors, hand-coded edges.

The node set is the `17 Areas` column of the Columbus Public Health ZIP
crosswalk, in alphabetical order -- see loaders/columbus_crosswalk.py for why
that resolution and not the 44 raw ZIPs. Alphabetical rather than source order
because the workbook's row order is not meaningful and a stable order is what
makes saved checkpoints and the `pred[:n_neigh]` slice reproducible.

Data notes, including where Columbus cannot match Boston, are in
Code/docs/COLUMBUS_DATA_NOTES.md.
"""

from __future__ import annotations

from . import City

# Alphabetical, fixing graph indices 0..16. Must match
# loaders.columbus_crosswalk.area_names(), which is asserted in
# run_columbus_data_check.py.
AREAS = [
    "Agler/Cassidy",
    "Bexley",
    "Clintonville/Near North",
    "Dublin",
    "Eastside",
    "Far East",
    "Far South",
    "Far Southeast",
    "Far Southwest",
    "Hilliard",
    "Linden",
    "NE Suburban",
    "Northland",
    "UA/Grandview",
    "West",
    "Westerville",
    "Worthington",
]

AREA_SHORT = [
    "Agler", "Bexley", "Clinton+", "Dublin", "Eastside",
    "FarEast", "FarSouth", "FarSE", "FarSW", "Hilliard",
    "Linden", "NESub", "Northland", "UA/Grand", "West",
    "Wville", "Worthing.",
]

# --- Anchor nodes ----------------------------------------------------------
# Boston's 7 anchors were designed by hand. Columbus's fall out of the data: the
# crosswalk lists 7 ZIPs it leaves unassigned, and they carry 147 of 63,103 ILI
# rows (0.23%) -- near-zero volume at the reporting boundary, which is exactly
# the anchor role.
#
# Six of the seven are genuinely peripheral and are grouped by direction below.
# The seventh, 43210, is Ohio State's campus and sits in the geographic MIDDLE of
# the city; it is unassigned because it is institutional (dormitories), not
# because it is on the fringe. Calling an interior ZIP a boundary sink would
# misrepresent what an anchor is, so 43210 is left out of the graph entirely --
# it is already excluded from the 17-area panel. Assigning it to
# Clintonville/Near North would mean inventing a crosswalk entry.
ANCHOR_NAMES = [
    "Amlin / NW Dublin fringe (43002)",
    "Lewis Center, Delaware Co. (43035)",
    "West Jefferson, Madison Co. (43140)",
    "Orient, Pickaway Co. (43146)",
    "Polaris, Delaware Co. (43240)",
]
ANCHOR_SHORT = ["Amlin", "LewisCtr", "W.Jeff", "Orient", "Polaris"]

# Which fringe ZIP each anchor is, for the record. One anchor per ZIP rather
# than my earlier grouping-by-compass-direction: the grouping was judgment and
# it was wrong. 43146 (Orient) borders Far Southeast as well as Far Southwest,
# so calling it "west" mis-wired it.
ANCHOR_ZIPS = {
    "Amlin": (43002,),
    "LewisCtr": (43035,),
    "W.Jeff": (43140,),
    "Orient": (43146,),
    "Polaris": (43240,),
}

# Two of the seven unassigned ZIPs are deliberately not nodes:
#   43210  Ohio State campus. It borders Clintonville/Near North and
#          UA/Grandview, i.e. it sits in the geographic MIDDLE of the city --
#          unassigned because it is institutional (dormitories), not because it
#          is peripheral. An interior ZIP is not a boundary sink, and dropping
#          it disconnects nothing: Clinton+ and UA/Grand border each other
#          directly anyway.
#   43126  Harrisburg. Shares no boundary with any of the 42 mapped ZIPs, so an
#          anchor for it would be an isolated node with only a self-loop.
EXCLUDED_ZIPS = {
    43210: "Ohio State campus -- interior, institutional, not a boundary",
    43126: "Harrisburg -- borders none of the 42 mapped ZIPs",
}

BACKGROUND_SHORT = "Background"

# --- Geographic adjacency, hand-coded from the Franklin County map ----------
# 38 area-area pairs. Hand-coded rather than derived from a ZCTA shapefile
# because geopandas/shapely are not installed in this project's environment;
# Boston's 23 pairs were hand-coded the same way. Density is higher than
# Boston's (average degree 4.5 against 3.3) because Franklin County is a
# contiguous inland partition, whereas Boston's harbour and river cut real
# adjacencies out of its map.
GEO_EDGES_AREA: list[tuple[str, str]] = [
    ("Agler", "Bexley"), ("Agler", "Clinton+"), ("Agler", "Eastside"),
    ("Agler", "FarEast"), ("Agler", "Linden"), ("Agler", "NESub"),
    ("Agler", "Northland"), ("Bexley", "Eastside"), ("Bexley", "FarEast"),
    ("Bexley", "FarSouth"), ("Clinton+", "Eastside"),
    ("Clinton+", "FarSouth"), ("Clinton+", "Linden"),
    ("Clinton+", "Northland"), ("Clinton+", "UA/Grand"),
    ("Clinton+", "West"), ("Clinton+", "Worthing."), ("Dublin", "Hilliard"),
    ("Dublin", "UA/Grand"), ("Dublin", "Worthing."),
    ("Eastside", "FarSouth"), ("FarEast", "FarSE"), ("FarEast", "FarSouth"),
    ("FarEast", "NESub"), ("FarSE", "FarSW"), ("FarSE", "FarSouth"),
    ("FarSW", "Hilliard"), ("FarSW", "West"), ("FarSouth", "West"),
    ("Hilliard", "UA/Grand"), ("Hilliard", "West"), ("Linden", "Northland"),
    ("NESub", "Northland"), ("NESub", "Wville"), ("Northland", "Worthing."),
    ("Northland", "Wville"), ("UA/Grand", "West"), ("UA/Grand", "Worthing."),
    ("Worthing.", "Wville"),
]

# 10 anchor pairs: each anchor -> the areas on the county edge it borders.
GEO_EDGES_ANCHOR: list[tuple[str, str]] = [
    ("Dublin", "Amlin"), ("Dublin", "LewisCtr"), ("FarSE", "Orient"),
    ("FarSW", "Orient"), ("FarSW", "W.Jeff"), ("Hilliard", "Amlin"),
    ("Worthing.", "LewisCtr"), ("Wville", "LewisCtr"), ("Wville", "Polaris"),
]

# Single-background scheme, kept only so the geo-only arm stays runnable.
GEO_EDGES_BACKGROUND: list[tuple[str, str]] = [
    ("FarSE", BACKGROUND_SHORT),
    ("FarSW", BACKGROUND_SHORT),
    ("Dublin", BACKGROUND_SHORT),
]

# --- Approximate centroids (lon, lat) for plotting only --------------------
# Land-area-weighted ZCTA internal points from columbus_area_geography.csv.
COORDS: dict[str, tuple[float, float]] = {
    "Agler":     (-82.9207, 40.0074),
    "Bexley":    (-82.9295, 39.9536),
    "Clinton+":  (-83.0124, 40.0116),
    "Dublin":    (-83.1210, 40.1385),
    "Eastside":  (-82.9689, 39.9541),
    "FarEast":   (-82.8344, 39.9489),
    "FarSouth":  (-82.9639, 39.8954),
    "FarSE":     (-82.8530, 39.8397),
    "FarSW":     (-83.1471, 39.8927),
    "Hilliard":  (-83.1775, 40.0205),
    "Linden":    (-82.9666, 40.0312),
    "NESub":     (-82.8272, 40.0474),
    "Northland": (-82.9652, 40.0838),
    "UA/Grand":  (-83.0686, 40.0248),
    "West":      (-83.0909, 39.9539),
    "Wville":    (-82.8906, 40.1104),
    "Worthing.": (-83.0589, 40.0863),
    # Anchors, at their ZCTA's real centroid.
    "Amlin":     (-83.1728, 40.0597),
    "LewisCtr":  (-82.9802, 40.1848),
    "W.Jeff":    (-83.4090, 39.8823),
    "Orient":    (-83.1339, 39.7675),
    "Polaris":   (-82.9835, 40.1501),
    BACKGROUND_SHORT: (-83.0000, 39.9600),
}

COLUMBUS = City(
    name="columbus",
    label="Columbus",
    node_label="area",
    node_names=tuple(AREAS),
    short_names=tuple(AREA_SHORT),
    anchor_names=tuple(ANCHOR_NAMES),
    anchor_short=tuple(ANCHOR_SHORT),
    background_short=BACKGROUND_SHORT,
    geo_edges=tuple(GEO_EDGES_AREA),
    geo_edges_anchor=tuple(GEO_EDGES_ANCHOR),
    geo_edges_background=tuple(GEO_EDGES_BACKGROUND),
    coords=dict(COORDS),
    loader_module="influenza.loaders.columbus",
    # Columbus has no ED-visit percentage, no confirmed-case count and no
    # monthly demographic series. It does have something Boston lacks: weekly
    # influenza-associated hospitalisations.
    available_globals=("ili_count", "hospitalizations"),
    # No wastewater, no RSV, and no vaccination series exists for Franklin
    # County in this repository. COVID exists but stops 62% of the way through
    # the evaluation window, so it is deliberately absent here -- see
    # COLUMBUS_DATA_NOTES.md section 7.
    available_features=frozenset({
        "weather", "demographics", "seasonality", "hospitalizations",
    }),
    # The ILI series starts 2022-01-01, so there is no pre-COVID and no
    # COVID-era history to include or exclude.
    variants=("post_covid",),
    # A Columbus area-week with no row had no qualifying ED visit. That is an
    # observed zero, not a suppressed count -- the opposite of Boston.
    suppresses_small_counts=False,
    notes="17 CPH areas from the Nov-2019 ZIP crosswalk; 238 weekly observations "
          "2022-01-02 to 2026-07-19.",
)
