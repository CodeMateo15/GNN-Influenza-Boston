"""Derive Chicago ZIP adjacency, centroids and city-edge ZIPs from the polygons.

    python Code/scrapers/derive_chicago_adjacency.py
    python Code/scrapers/derive_chicago_adjacency.py --compare

Same rule as derive_columbus_adjacency.py and derive_amba_adjacency.py, for the
same reason: a hand-coded border list was measured at 87% accurate in Columbus,
and 59 ZIPs is more borders than anyone should type. Two ZIPs are adjacent
exactly when their boundaries share at least two vertices -- one shared vertex
is a corner touch, not a border. The City's polygons are topologically clean
in the way TIGER and IGN are: the edge count is identical at 4, 5, 6 and 7
decimal places, so the shared vertices are exact rather than merely close.

Reads the polygons build_chicago_panel.py already saved (unjd-c2ca), so there
is no network call here.

Two further outputs that the other cities hard-code and this one measures:

  * CENTROIDS. Area-weighted, from the same polygons (holes subtracted, every
    part of a MultiPolygon counted). Used for the weather pull and plots only.
  * CITY-EDGE ZIPS. The "single" anchor scheme drains the scored ZIPs on the
    city's edge into one background node, so the profile needs to know which
    they are. A ZIP is on the edge when more than MIN_EXTERIOR_KM of its
    perimeter lies against no other ZIP. Measured by length with a 10 m
    tolerance rather than by unshared vertices, because a shared border
    digitised with extra vertices on one side would otherwise read as exterior.
    The 1 km floor drops a handful of Loop slivers along the river (0.1-0.9
    km) and keeps every ZIP on the city limit or the lakefront -- the lake
    counts as outside, the way Boston's harbour does.

Output: Data/Chicago/chicago_zip_edges.csv, Data/Chicago/chicago_zip_centroids.csv
"""

from __future__ import annotations

import argparse
import datetime
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

PRECISION = 6
MIN_SHARED_VERTICES = 2
TOLERANCE_KM = 0.01
MIN_EXTERIOR_KM = 1.0
# km per degree at Chicago's latitude; planar is fine at city scale.
KM_X = float(np.cos(np.radians(41.84)) * 111.32)
KM_Y = 110.57


def load_polygons() -> dict[str, dict]:
    with open(paths.require(paths.CHICAGO_BOUNDARIES_FILE, "Chicago ZIP polygons")) as handle:
        features = json.load(handle)["features"]
    return {str(f["properties"]["zip"]).zfill(5): f["geometry"] for f in features}


def polygons_of(geometry: dict) -> list:
    return [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]


def boundary_vertices(geometry: dict) -> set[tuple[float, float]]:
    return {(round(x, PRECISION), round(y, PRECISION))
            for poly in polygons_of(geometry) for ring in poly for x, y, *_ in ring}


def adjacency(vertices: dict[str, set]) -> dict[str, set[str]]:
    pairs: dict[str, set[str]] = defaultdict(set)
    for a, b in itertools.combinations(sorted(vertices), 2):
        if len(vertices[a] & vertices[b]) >= MIN_SHARED_VERTICES:
            pairs[a].add(b)
            pairs[b].add(a)
    return pairs


def centroid(geometry: dict) -> tuple[float, float]:
    """Area-weighted (lon, lat). Holes enter with the opposite sign by orientation."""
    total = cx = cy = 0.0
    for poly in polygons_of(geometry):
        for k, ring in enumerate(poly):
            xy = np.asarray(ring, dtype=float)[:, :2]
            x, y = xy[:, 0], xy[:, 1]
            cross = x[:-1] * y[1:] - x[1:] * y[:-1]
            area = cross.sum() / 2.0
            # Outer ring adds, holes subtract, whatever winding the file uses.
            sign = (1.0 if k == 0 else -1.0) * np.sign(area)
            total += sign * area
            cx += sign * ((x[:-1] + x[1:]) * cross).sum() / 6.0
            cy += sign * ((y[:-1] + y[1:]) * cross).sum() / 6.0
    return cx / total, cy / total


def segments_km(geometry: dict) -> np.ndarray:
    """(n, 4) boundary segments x0, y0, x1, y1 in km."""
    rows = []
    for poly in polygons_of(geometry):
        for ring in poly:
            xy = np.asarray(ring, dtype=float)[:, :2] * [KM_X, KM_Y]
            rows.append(np.hstack([xy[:-1], xy[1:]]))
    return np.vstack(rows)


def _distance_to_segments(points: np.ndarray, segments: np.ndarray) -> np.ndarray:
    start, delta = segments[:, :2], segments[:, 2:] - segments[:, :2]
    length2 = np.maximum((delta ** 2).sum(axis=1), 1e-12)
    t = np.clip(((points[:, None, :] - start[None]) * delta[None]).sum(axis=2)
                / length2[None], 0.0, 1.0)
    nearest = start[None] + t[..., None] * delta[None]
    return np.sqrt(((points[:, None, :] - nearest) ** 2).sum(axis=2)).min(axis=1)


def exterior_km(segments: dict[str, np.ndarray]) -> dict[str, tuple[float, float]]:
    """ZIP -> (perimeter km, km of perimeter that borders no other ZIP)."""
    boxes = {z: (s.reshape(-1, 2).min(axis=0), s.reshape(-1, 2).max(axis=0))
             for z, s in segments.items()}
    out = {}
    for z, own in segments.items():
        midpoints = (own[:, :2] + own[:, 2:]) / 2.0
        lengths = np.sqrt(((own[:, 2:] - own[:, :2]) ** 2).sum(axis=1))
        nearest = np.full(len(own), np.inf)
        lo, hi = boxes[z][0] - 0.05, boxes[z][1] + 0.05
        for other, theirs in segments.items():
            olo, ohi = boxes[other]
            if other == z or (ohi < lo).any() or (olo > hi).any():
                continue
            nearest = np.minimum(nearest, _distance_to_segments(midpoints, theirs))
        out[z] = (float(lengths.sum()), float(lengths[nearest > TOLERANCE_KM].sum()))
    return out


def derive() -> tuple[pd.DataFrame, pd.DataFrame]:
    polygons = load_polygons()
    coverage = pd.read_csv(paths.require(paths.CHICAGO_COVERAGE_FILE, "Chicago coverage"),
                           dtype={"zip": str})
    wanted = set(coverage["zip"])
    missing = wanted - set(polygons)
    if missing:
        raise SystemExit(f"No polygon for ZIPs {sorted(missing)}; the graph would "
                         "have a node with no borders.")
    polygons = {z: polygons[z] for z in sorted(wanted)}

    pairs = adjacency({z: boundary_vertices(g) for z, g in polygons.items()})
    isolated = [z for z in polygons if not pairs[z]]
    if isolated:
        raise SystemExit(f"{isolated} came out with no neighbours at all. A "
                         "disconnected node cannot receive spatial information, so "
                         "this is a geometry failure, not a finding.")
    edges = pd.DataFrame([{"zip_a": a, "zip_b": b}
                          for a in sorted(pairs) for b in sorted(pairs[a]) if a < b])

    perimeter = exterior_km({z: segments_km(g) for z, g in polygons.items()})
    rows = []
    for z, geometry in polygons.items():
        lon, lat = centroid(geometry)
        total, outside = perimeter[z]
        rows.append({"zip": z, "lon": round(lon, 5), "lat": round(lat, 5),
                     "perimeter_km": round(total, 2), "exterior_km": round(outside, 2),
                     "on_city_edge": outside > MIN_EXTERIOR_KM})
    return edges, pd.DataFrame(rows)


EDGE_HEADER = """# Chicago ZIP adjacency, derived from boundary geometry.
#
# SOURCE: City of Chicago Data Portal, "Boundaries - ZIP Codes" (unjd-c2ca),
# saved as chicago_zip_boundaries.geojson by build_chicago_panel.py.
# Built by Code/scrapers/derive_chicago_adjacency.py on {today}.
#
# RULE: two ZIPs are adjacent when their boundaries share at least {shared}
# vertices at {precision} decimal places. One shared vertex is a corner touch,
# not a border. The edge count is identical at 4-7 decimals.
#
# ZIPs on the city limit border suburbs that are not nodes, and the lakefront
# ZIPs border the lake. Those boundaries are absent by construction; the
# background node carries them (see chicago_zip_centroids.csv, on_city_edge).
"""

CENTROID_HEADER = """# Chicago ZIP centroids and city-edge flags, derived from boundary geometry.
# Built by Code/scrapers/derive_chicago_adjacency.py on {today}.
# lon/lat: area-weighted centroid. exterior_km: perimeter bordering no other
# ZIP (10 m tolerance). on_city_edge: exterior_km > {floor} km.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--compare", action="store_true",
                        help="Diff the derived edges against the committed CSV "
                             "instead of overwriting it.")
    args = parser.parse_args()

    edges, centroids = derive()
    if args.compare:
        committed = pd.read_csv(paths.require(paths.CHICAGO_EDGES_FILE, "committed edges"),
                                comment="#", dtype=str)
        new = set(map(tuple, edges[["zip_a", "zip_b"]].values))
        old = set(map(tuple, committed[["zip_a", "zip_b"]].values))
        print(f"derived {len(new)} edges, committed {len(old)}")
        for label, diff in (("only derived", new - old), ("only committed", old - new)):
            print(f"  {label}: {sorted(diff) if diff else 'none'}")
        return

    today = datetime.date.today()
    with open(paths.CHICAGO_EDGES_FILE, "w") as handle:
        handle.write(EDGE_HEADER.format(today=today, shared=MIN_SHARED_VERTICES,
                                        precision=PRECISION))
        edges.to_csv(handle, index=False)
    with open(paths.CHICAGO_CENTROIDS_FILE, "w") as handle:
        handle.write(CENTROID_HEADER.format(today=today, floor=MIN_EXTERIOR_KM))
        centroids.to_csv(handle, index=False)

    degree = pd.concat([edges.zip_a, edges.zip_b]).value_counts()
    print(f"{len(edges)} edges over {degree.size} ZIPs "
          f"(degree {degree.min()}-{degree.max()}, mean {degree.mean():.1f})")
    print(f"{int(centroids.on_city_edge.sum())} ZIPs on the city edge")
    print(f"Outputs: {paths.display(paths.CHICAGO_EDGES_FILE, paths.ROOT)}, "
          f"{paths.display(paths.CHICAGO_CENTROIDS_FILE, paths.ROOT)}")


if __name__ == "__main__":
    main()
