"""Derive Columbus area adjacency from real ZCTA boundaries.

Boston's 23 geographic edges are hand-coded from a map, and the first Columbus
version was too. Hand-coding turned out to be 87% accurate: of the 39 real
area-area borders it found 34, invented 4 that do not exist, and missed 5 that
do. That is a big enough error rate to matter for a graph model whose entire
premise is that the edges carry signal, so the edge list is now measured.

No new dependency. geopandas/shapely are not installed in this project's
environment, so instead of reading a shapefile this pulls ZCTA polygons as
GeoJSON from the Census TIGERweb REST service (keyless) and computes adjacency
in pure Python: TIGER is topologically consistent, meaning two polygons sharing
a border share the *identical* vertex coordinates, so two ZCTAs are adjacent
exactly when they share at least two boundary vertices. Two vertices rather than
one, because a single shared vertex is a corner touch, not a border.

Output: Data/Columbus Influenza Data/columbus_area_edges.csv

    python Code/scrapers/derive_columbus_adjacency.py
    python Code/scrapers/derive_columbus_adjacency.py --compare   # diff vs the profile
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths
from influenza.loaders import columbus_crosswalk as crosswalk

TIGERWEB = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
            "tigerWMS_ACS2023/MapServer/2/query")
# Franklin County ZIPs are all 430xx-432xx; the 450xx clause catches the two
# Cincinnati-area ZIPs the COVID extract reaches, so a future crosswalk revision
# covering them still resolves.
WHERE = "ZCTA5 LIKE '43%' OR ZCTA5 LIKE '450%'"
TIMEOUT = 180
PRECISION = 6          # decimal degrees; TIGER vertices are exact at this scale
MIN_SHARED_VERTICES = 2


def fetch_zcta_polygons() -> dict[int, list]:
    """ZCTA5 -> GeoJSON geometry, for the 43xxx/450xx range."""
    response = requests.get(TIGERWEB, timeout=TIMEOUT, params={
        "where": WHERE,
        "outFields": "ZCTA5",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    })
    response.raise_for_status()
    payload = response.json()
    if payload.get("exceededTransferLimit"):
        raise RuntimeError(
            "TIGERweb truncated the response; adjacency would be silently "
            "incomplete. Narrow WHERE and page the request."
        )
    features = payload.get("features") or []
    if not features:
        raise RuntimeError(f"TIGERweb returned no features. Response head: {response.text[:300]}")
    return {int(f["properties"]["ZCTA5"]): f["geometry"] for f in features}


def boundary_vertices(geometry: dict) -> set[tuple[float, float]]:
    coords = geometry["coordinates"]
    rings = coords if geometry["type"] == "Polygon" else [r for poly in coords for r in poly]
    return {(round(x, PRECISION), round(y, PRECISION)) for ring in rings for x, y in ring}


def zip_adjacency(vertices: dict[int, set]) -> dict[int, set[int]]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    codes = sorted(vertices)
    for i, a in enumerate(codes):
        for b in codes[i + 1:]:
            if len(vertices[a] & vertices[b]) >= MIN_SHARED_VERTICES:
                adjacency[a].add(b)
                adjacency[b].add(a)
    return adjacency


def derive(polygons: dict[int, list]) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """(area-area pairs, area-anchor pairs) on SHORT names, sorted."""
    from influenza.cities.columbus import ANCHOR_ZIPS, COLUMBUS

    zip_area = crosswalk.zip_to_area()
    short = dict(zip(COLUMBUS.node_names, COLUMBUS.short_names))
    anchor_of = {z: anchor for anchor, zips in ANCHOR_ZIPS.items() for z in zips}

    wanted = set(zip_area) | set(anchor_of)
    missing = sorted(wanted - set(polygons))
    if missing:
        raise RuntimeError(f"No ZCTA polygon for {missing}; adjacency would be incomplete.")

    vertices = {z: boundary_vertices(polygons[z]) for z in wanted}
    adjacency = zip_adjacency(vertices)

    areas: set[tuple[str, str]] = set()
    anchors: set[tuple[str, str]] = set()
    for a, neighbours in adjacency.items():
        for b in neighbours:
            if a in zip_area and b in zip_area:
                left, right = zip_area[a], zip_area[b]
                if left != right:
                    areas.add(tuple(sorted((short[left], short[right]))))
            elif a in zip_area and b in anchor_of:
                anchors.add((short[zip_area[a]], anchor_of[b]))
            elif b in zip_area and a in anchor_of:
                anchors.add((short[zip_area[b]], anchor_of[a]))
    return sorted(areas), sorted(anchors)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--compare", action="store_true",
                        help="Diff the derived edges against cities/columbus.py.")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    output = args.output or (paths.COLUMBUS_DIR / "columbus_area_edges.csv")

    print("Fetching ZCTA polygons from TIGERweb (no API key needed)...")
    polygons = fetch_zcta_polygons()
    print(f"  {len(polygons)} polygons")
    areas, anchors = derive(polygons)
    print(f"  {len(areas)} area-area pairs, {len(anchors)} area-anchor pairs")

    frame = pd.DataFrame(
        [{"kind": "area", "a": a, "b": b} for a, b in areas]
        + [{"kind": "anchor", "a": a, "b": b} for a, b in anchors])
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as handle:
        handle.write("# Columbus geographic adjacency, derived by "
                     "Code/scrapers/derive_columbus_adjacency.py\n"
                     "# Source: Census TIGERweb ACS2023 ZCTA polygons. Two ZCTAs are\n"
                     "# adjacent when they share >= 2 boundary vertices (a shared edge, not a\n"
                     "# corner touch). Aggregated ZIP -> area via the CPH crosswalk.\n")
        frame.to_csv(handle, index=False)
    print(f"\n-> {paths.display(output, paths.ROOT)}")

    if args.compare:
        from influenza.cities.columbus import GEO_EDGES_ANCHOR, GEO_EDGES_AREA
        for label, derived, current in (
            ("area-area", set(areas), {tuple(sorted(p)) for p in GEO_EDGES_AREA}),
            ("area-anchor", set(anchors), set(GEO_EDGES_ANCHOR)),
        ):
            print(f"\n{label}: {len(current & derived)} agree, "
                  f"{len(current - derived)} in profile only, {len(derived - current)} derived only")
            for pair in sorted(current - derived):
                print(f"   profile only (not a real border): {pair}")
            for pair in sorted(derived - current):
                print(f"   derived only (missing from profile): {pair}")


if __name__ == "__main__":
    main()
