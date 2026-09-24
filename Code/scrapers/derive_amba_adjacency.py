"""Derive AMBA partido adjacency from IGN boundary polygons.

    python Code/scrapers/derive_amba_adjacency.py
    python Code/scrapers/derive_amba_adjacency.py --compare

Same method as Code/scrapers/derive_columbus_adjacency.py, and for the same
reason: hand-coding a border list from a map was measured there at 87% accurate
-- of 39 real borders it found 34, invented 4 and missed 5. There is no reason
to expect better on 24 unfamiliar districts.

Two partidos are adjacent exactly when their boundaries share at least two
vertices. Two rather than one, because a single shared vertex is a corner
touch, not a border. The Argentine IGN polygons turn out to be topologically
clean in the same way the US TIGER ones are: the derived edge count is
identical at 4, 5 and 6 decimal places of rounding, so the vertices really are
shared rather than merely close.

Source: IGN (Instituto Geografico Nacional) WFS, layer ign:departamento, which
carries the INDEC department code in `in1` -- the same integer the ETI panel
and the INDEC population table are keyed on, so nothing is joined by name.

Unlike the Columbus equivalent, whose output CSV is written but never read at
runtime, `influenza/cities/buenos_aires.py` loads this file at import. There is
one edge list, not a generated one plus a hand-synced literal that can drift.

Output: Data/Buenos Aires Acute Respiratory Infections/amba_partido_edges.csv
"""

from __future__ import annotations

import argparse
import datetime
import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

IGN_WFS = "https://wms.ign.gob.ar/geoserver/ows"
PROVINCE = "06"           # Buenos Aires
TIMEOUT = 180
PRECISION = 6
MIN_SHARED_VERTICES = 2


def fetch_polygons() -> dict[int, dict]:
    """INDEC department code -> GeoJSON geometry, for Buenos Aires province."""
    import requests

    response = requests.get(IGN_WFS, timeout=TIMEOUT, params={
        "service": "WFS", "version": "1.0.0", "request": "GetFeature",
        "typeName": "ign:departamento", "outputFormat": "application/json",
        "CQL_FILTER": f"in1 LIKE '{PROVINCE}%'", "maxFeatures": 200,
    })
    response.raise_for_status()
    features = response.json().get("features") or []
    if not features:
        raise SystemExit(f"IGN returned no features. Head: {response.text[:300]}")
    return {int(f["properties"]["in1"]): f["geometry"] for f in features}


def boundary_vertices(geometry: dict) -> set[tuple[float, float]]:
    coords = geometry["coordinates"]
    rings = (coords if geometry["type"] == "Polygon"
             else [ring for poly in coords for ring in poly])
    return {(round(x, PRECISION), round(y, PRECISION))
            for ring in rings for x, y in ring}


def adjacency(vertices: dict[int, set]) -> dict[int, set[int]]:
    pairs: dict[int, set[int]] = defaultdict(set)
    for a, b in itertools.combinations(sorted(vertices), 2):
        if len(vertices[a] & vertices[b]) >= MIN_SHARED_VERTICES:
            pairs[a].add(b)
            pairs[b].add(a)
    return pairs


def derive() -> pd.DataFrame:
    coverage = pd.read_csv(paths.AMBA_COVERAGE_FILE)
    wanted = dict(zip(coverage.indec, coverage.partido))

    polygons = {code: geom for code, geom in fetch_polygons().items()
                if code in wanted}
    missing = set(wanted) - set(polygons)
    if missing:
        raise SystemExit(
            f"IGN has no polygon for INDEC codes {sorted(missing)}; the graph "
            "would be built with a node that has no borders."
        )

    vertices = {code: boundary_vertices(geom) for code, geom in polygons.items()}
    pairs = adjacency(vertices)
    isolated = [wanted[c] for c in sorted(polygons) if not pairs[c]]
    if isolated:
        raise SystemExit(
            f"{isolated} came out with no neighbours at all. A disconnected node "
            "cannot receive spatial information, so this is a geometry failure, "
            "not a finding."
        )

    rows = [{"indec_a": a, "partido_a": wanted[a],
             "indec_b": b, "partido_b": wanted[b]}
            for a in sorted(pairs) for b in sorted(pairs[a]) if a < b]
    return pd.DataFrame(rows).sort_values(["partido_a", "partido_b"])


HEADER = """# AMBA partido adjacency, derived from boundary geometry.
#
# SOURCE: IGN (Instituto Geografico Nacional) WFS, layer ign:departamento,
# joined on the INDEC department code (`in1`), not on names.
#   {url}
# Built by Code/scrapers/derive_amba_adjacency.py on {today}.
#
# RULE: two partidos are adjacent when their boundaries share at least
# {shared} vertices at {precision} decimal places. One shared vertex is a corner
# touch, not a border. The edge count is identical at 4, 5 and 6 decimals, which
# is the check that the polygons share vertices exactly rather than approximately.
#
# Partidos on the edge of the conurbano border districts outside the 24 (and
# several border the Autonomous City of Buenos Aires, which is not a node here).
# Those boundaries are absent by construction; the anchor nodes carry them, the
# same role Boston's anchors play.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--compare", action="store_true",
                        help="Diff the derived edges against the committed CSV "
                             "instead of overwriting it.")
    args = parser.parse_args()

    edges = derive()
    if args.compare:
        if not paths.AMBA_EDGES_FILE.exists():
            raise SystemExit(f"nothing to compare against: {paths.AMBA_EDGES_FILE}")
        committed = pd.read_csv(paths.AMBA_EDGES_FILE, comment="#")
        new = set(map(tuple, edges[["partido_a", "partido_b"]].values))
        old = set(map(tuple, committed[["partido_a", "partido_b"]].values))
        print(f"derived {len(new)} edges, committed {len(old)}")
        for label, diff in (("only derived", new - old), ("only committed", old - new)):
            print(f"  {label}: {sorted(diff) if diff else 'none'}")
        return

    with open(paths.AMBA_EDGES_FILE, "w") as handle:
        handle.write(HEADER.format(url=IGN_WFS, today=datetime.date.today(),
                                   shared=MIN_SHARED_VERTICES, precision=PRECISION))
        edges.to_csv(handle, index=False)

    degree = pd.concat([edges.partido_a, edges.partido_b]).value_counts()
    print(f"{len(edges)} edges over {degree.size} partidos "
          f"(degree {degree.min()}-{degree.max()}, mean {degree.mean():.1f})")
    print(f"Outputs: {paths.display(paths.AMBA_EDGES_FILE)}")


if __name__ == "__main__":
    main()
