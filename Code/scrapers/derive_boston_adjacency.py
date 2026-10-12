"""Derive Boston's neighborhood graph from boundary polygons, two ways.

    python Code/scrapers/derive_boston_adjacency.py
    python Code/scrapers/derive_boston_adjacency.py --compare

Why. Boston's 23 neighborhood edges and 21 anchor edges were hand-coded from a
map. Columbus's were too, and when measured against Census polygons they were
87% right (Code/scrapers/derive_columbus_adjacency.py). Buenos Aires's were
derived from the start. For the graph to be something a new city gets from its
boundary files rather than from someone's reading of a map, Boston needs the
same treatment -- and the models then need to be shown not to depend on which
version of the map they were given.

Same rule as the other two cities: two areas are adjacent when their boundaries
share at least two vertices (a shared edge, not a corner touch). Boston makes it
harder than Columbus or Buenos Aires in one specific way -- water -- and there
is no single right answer, so both answers are written:

  tract  Neighborhoods from "Boston Neighborhood Boundaries Approximated by 2020
         Census Tracts" (Analyze Boston), towns from Census TIGERweb county
         subdivisions. Both are built from TIGER, so vertices are shared exactly
         and the result is identical at 4, 5 and 6 decimal places: no tolerance.
         Water tracts ride along with whichever neighborhood the city assigned
         them to, which keeps real harbor and river crossings (Charlestown-East
         Boston, Back Bay-Cambridge) but also creates artefacts: Fenway's polygon
         includes the Charles River tract, so it "borders" Watertown and Newton.
  land   Neighborhood-neighborhood edges from the official BPDA neighborhood
         polygons, which follow land and share vertices exactly with each other.
         They are not built from TIGER, so they share no exact vertices with the
         towns: neighborhood-town edges need a snapping tolerance, and the count
         moves with it (8 pairs at ~1 m, 18 at ~10 m, 23 at ~100 m). 100 m
         (3 decimal places) is used. Water crossings disappear.

The two water anchors -- Charles River and Boston Harbor -- are not land and are
absent from every polygon source used here; both versions keep their
hand-coded edges, and the city profiles say so.

Mapping to the 14 BPHC neighborhoods is `boston.GEOID_TO_IDX`. The official
layer has three names it does not cover: Bay Village (ZIP 02116, grouped with
Back Bay), Leather District (ZIP 02111, grouped with Chinatown in the South End
node) and Harbor Islands (dropped: water, not a BPHC neighborhood).

Output: Data/Neighborhood Data/boston_edges_tract.csv, boston_edges_land.csv,
and the raw polygons beside them for reproducibility.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402
from influenza.cities.boston import (GEO_EDGES_ANCHOR, GEO_EDGES_NEIGHBORHOOD,  # noqa: E402
                                     GEOID_TO_IDX, SHORT_NAMES)

TRACT_NEIGHBORHOODS = (
    "https://data.boston.gov/dataset/5997399b-c665-4600-848f-a2a32834f009/resource/"
    "42a271c9-486d-4f9e-adc2-63e4bf47fe3e/download/"
    "boston_neighborhood_boundaries_approximated_by_2020_census_tracts.geojson")
OFFICIAL_NEIGHBORHOODS = ("https://gis.bostonplans.org/hosting/rest/services/Hosted/"
                          "Boston_Neighborhood_Boundaries/FeatureServer/5/query")
TIGER_TOWNS = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
               "tigerWMS_ACS2023/MapServer/22/query")
TIMEOUT = 180
MIN_SHARED_VERTICES = 2
EXACT_PRECISION = 6        # TIGER-consistent sources: identical at 4-6
LAND_TOWN_PRECISION = 3    # ~100 m; cross-source, see the module docstring

# Anchor membership, by town. The anchors' own names say what they cover;
# Everett, Watertown, Needham and Canton border Boston but are not named in any
# anchor, so each goes to the anchor on its side of the city.
TOWN_TO_ANCHOR = {
    "Cambridge": "Camb/Somer", "Somerville": "Camb/Somer",
    "Chelsea": "Chelsea+", "Revere": "Chelsea+", "Winthrop": "Chelsea+", "Everett": "Chelsea+",
    "Brookline": "Brookline",
    "Milton": "S.Suburbs", "Quincy": "S.Suburbs", "Canton": "S.Suburbs",
    "Newton": "W.Suburbs", "Dedham": "W.Suburbs", "Needham": "W.Suburbs",
    "Watertown": "W.Suburbs",
}
EXTRA_MEMBERS = {"Bay Village": 1, "Leather District": 12}
WATER_ANCHORS = ("CharlesR", "Harbor")
OUT_DIR = paths.NEIGHBORHOOD_DIR


def fetch(url: str, params: dict | None = None) -> dict:
    response = requests.get(url, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def fetch_all() -> tuple[dict, dict, dict]:
    tract = fetch(TRACT_NEIGHBORHOODS)
    official = fetch(OFFICIAL_NEIGHBORHOODS, {"where": "1=1", "outFields": "name",
                                              "outSR": "4326", "f": "geojson"})
    quoted = ",".join(f"'{t}'" for t in TOWN_TO_ANCHOR)
    towns = fetch(TIGER_TOWNS, {"where": f"STATE='25' AND BASENAME IN ({quoted})",
                                "outFields": "BASENAME,GEOID", "returnGeometry": "true",
                                "outSR": "4326", "f": "geojson"})
    return tract, official, towns


def rings(geometry: dict):
    polygons = ([geometry["coordinates"]] if geometry["type"] == "Polygon"
                else geometry["coordinates"])
    for polygon in polygons:
        yield from polygon


def node_of(name: str) -> str | None:
    index = GEOID_TO_IDX.get(name, EXTRA_MEMBERS.get(name))
    return None if index is None else SHORT_NAMES[index]


def vertex_owners(layers: list[tuple[dict, str, callable]], precision: int) -> dict:
    """Rounded vertex -> set of node labels, over several polygon layers."""
    owners: dict[tuple[float, float], set[str]] = defaultdict(set)
    for collection, field, label in layers:
        for feature in collection["features"]:
            node = label(feature["properties"][field])
            if node is None:
                continue
            for ring in rings(feature["geometry"]):
                for x, y in ring:
                    owners[(round(x, precision), round(y, precision))].add(node)
    return owners


def shared_pairs(owners: dict) -> set[tuple[str, str]]:
    counts: dict[tuple[str, str], int] = defaultdict(int)
    for nodes in owners.values():
        for a, b in itertools.combinations(sorted(nodes), 2):
            counts[(a, b)] += 1
    return {pair for pair, n in counts.items() if n >= MIN_SHARED_VERTICES}


def split(pairs: set[tuple[str, str]]) -> tuple[set, set]:
    """(neighborhood-neighborhood, neighborhood-anchor) with the anchor second."""
    anchors = set(TOWN_TO_ANCHOR.values())
    between, anchored = set(), set()
    for a, b in pairs:
        a_anchor, b_anchor = a in anchors, b in anchors
        if not a_anchor and not b_anchor:
            between.add(tuple(sorted((a, b))))
        elif a_anchor != b_anchor:
            anchored.add((b, a) if a_anchor else (a, b))
    return between, anchored


def derive(tract: dict, official: dict, towns: dict) -> dict[str, tuple[set, set]]:
    town_layer = (towns, "BASENAME", lambda n: TOWN_TO_ANCHOR.get(n))
    tract_pairs = shared_pairs(vertex_owners(
        [(tract, "neighborhood", node_of), town_layer], EXACT_PRECISION))
    tract_between, tract_anchor = split(tract_pairs)

    land_between, _ = split(shared_pairs(vertex_owners(
        [(official, "name", node_of)], EXACT_PRECISION)))
    _, land_anchor = split(shared_pairs(vertex_owners(
        [(official, "name", node_of), town_layer], LAND_TOWN_PRECISION)))
    return {"tract": (tract_between, tract_anchor), "land": (land_between, land_anchor)}


def write(version: str, between: set, anchored: set) -> Path:
    out = OUT_DIR / f"boston_edges_{version}.csv"
    lines = [f"# Boston geographic adjacency, '{version}' version, derived by "
             "Code/scrapers/derive_boston_adjacency.py. Water anchors (Charles River, "
             "Boston Harbor) are not in this file; the city profile adds their "
             "hand-coded edges.",
             "kind,a,b"]
    lines += [f"neighborhood,{a},{b}" for a, b in sorted(between)]
    lines += [f"anchor,{a},{b}" for a, b in sorted(anchored)]
    out.write_text("\n".join(lines) + "\n")
    return out


def compare(version: str, between: set, anchored: set) -> None:
    hand_between = {tuple(sorted(p)) for p in GEO_EDGES_NEIGHBORHOOD}
    hand_anchor = {p for p in GEO_EDGES_ANCHOR if p[1] not in WATER_ANCHORS}
    for label, hand, derived in (("neighborhood", hand_between, between),
                                 ("land anchor", hand_anchor, anchored)):
        agree = hand & derived
        print(f"  {version} {label}: derived {len(derived)}, hand {len(hand)}, agree "
              f"{len(agree)} | hand-only {sorted(hand - derived)} | derived-only "
              f"{sorted(derived - hand)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--compare", action="store_true",
                        help="Also print each version against the hand-coded edges.")
    args = parser.parse_args()
    tract, official, towns = fetch_all()
    for name, payload in (("tract_neighborhoods", tract), ("official_neighborhoods", official),
                          ("tiger_towns", towns)):
        (OUT_DIR / f"boston_polygons_{name}.geojson").write_text(json.dumps(payload))
    for version, (between, anchored) in derive(tract, official, towns).items():
        out = write(version, between, anchored)
        print(f"{version}: {len(between)} neighborhood + {len(anchored)} anchor edges -> "
              f"{paths.display(out, paths.ROOT)}")
        if args.compare:
            compare(version, between, anchored)


if __name__ == "__main__":
    main()
