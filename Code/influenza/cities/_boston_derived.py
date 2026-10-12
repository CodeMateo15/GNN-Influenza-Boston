"""Shared builder for the two derived-edge Boston profiles.

Same data, nodes, anchors and loaders as `boston.BOSTON`; only the geographic
edges differ, read from the CSVs Code/scrapers/derive_boston_adjacency.py
writes. The water anchors (Charles River, Boston Harbor) are absent from every
land polygon source, so their hand-coded edges are carried over unchanged --
the one part of Boston's graph that still comes from a map.
"""

from __future__ import annotations

import csv
from dataclasses import replace

from .. import paths
from .boston import BOSTON, GEO_EDGES_ANCHOR

WATER_ANCHORS = ("CharlesR", "Harbor")


def derived_boston(version: str):
    between, anchored = [], []
    path = paths.NEIGHBORHOOD_DIR / f"boston_edges_{version}.csv"
    with open(path, newline="") as handle:
        for row in csv.DictReader(line for line in handle if not line.startswith("#")):
            (between if row["kind"] == "neighborhood" else anchored).append((row["a"], row["b"]))
    anchored += [pair for pair in GEO_EDGES_ANCHOR if pair[1] in WATER_ANCHORS]
    return replace(BOSTON, name=f"boston_geo_{version}",
                   label=f"Boston (derived edges, {version})",
                   geo_edges=tuple(sorted(between)), geo_edges_anchor=tuple(sorted(anchored)))
