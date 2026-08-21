"""Graph construction: nodes, edge types and the weighted adjacency.

Edge semantics are documented in docs/EDGES_AND_NODES_NOTES.txt section 3. All
edges are undirected and every node gets a self-loop of weight 1.0.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .cities import City
from .config import GraphSpec


@dataclass
class Graph:
    """A built graph, ready for either the PyG or the dense model path."""

    node_names: list[str]
    n_nodes: int
    n_neigh: int
    W: np.ndarray
    A: np.ndarray                       # binary, for plotting only
    counts: dict[str, int] = field(default_factory=dict)
    W_corr: np.ndarray | None = None    # second topology when spec.dual

    @property
    def n_anchors(self) -> int:
        return self.n_nodes - self.n_neigh

    def edge_tensors(self):
        """(edge_index, edge_weight) for torch_geometric, with self-loops."""
        import torch

        src, dst, weights = [], [], []
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                if i != j and self.W[i, j] > 0:
                    src.append(i)
                    dst.append(j)
                    weights.append(float(self.W[i, j]))
        for i in range(self.n_nodes):
            src.append(i)
            dst.append(i)
            weights.append(1.0)
        edge_index = torch.tensor([src, dst], dtype=torch.long)
        edge_weight = torch.tensor(weights, dtype=torch.float32)
        return edge_index, edge_weight

    def normalized(self, matrix: np.ndarray | None = None) -> np.ndarray:
        """Symmetric normalisation D^-1/2 (A + I) D^-1/2, for the dense path."""
        source = self.W if matrix is None else matrix
        adjacency = source + np.eye(self.n_nodes)
        degree = adjacency.sum(axis=1)
        scale = np.where(degree > 0, 1.0 / np.sqrt(degree), 0.0)
        return adjacency * scale[:, None] * scale[None, :]

    def summary(self) -> str:
        undirected = int((np.triu(self.W, 1) > 0).sum())
        parts = ", ".join(f"{k}={v}" for k, v in sorted(self.counts.items()))
        return (f"{self.n_nodes} nodes ({self.n_neigh} scored + {self.n_anchors} anchors), "
                f"{undirected} undirected edges, weights "
                f"[{self.W.min():.3f}, {self.W.max():.3f}]\n  {parts}")


def node_names(spec: GraphSpec, city: City) -> list[str]:
    if spec.anchors == "none":
        return list(city.short_names)
    if spec.anchors == "single":
        return [*city.short_names, city.background_short]
    return [*city.short_names, *city.anchor_short]


def _anchor_edges(spec: GraphSpec, city: City) -> list[tuple[str, str]]:
    if spec.anchors == "none":
        return []
    if spec.anchors == "single":
        return list(city.geo_edges_background)
    return list(city.geo_edges_anchor)


def _hop_distances(adjacency: dict[int, set[int]], source: int) -> dict[int, int]:
    """BFS over neighborhood edges only, so anchors are not pass-through shortcuts."""
    distance = {source: 0}
    queue = collections.deque([source])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance


def build_graph(
    spec: GraphSpec,
    *,
    city: City,
    flu_history: pd.DataFrame,
    static: np.ndarray | None = None,
    mbta: np.ndarray | None = None,
) -> Graph:
    """Assemble the weighted adjacency from the active edge types.

    `flu_history` must already be sliced to weeks strictly before the test
    window. The caller does that slicing so the leakage guard stays visible at
    the call site rather than hidden in here.

    `city` is required rather than defaulting to Boston: a silently-defaulted
    city would build a 14-node Boston graph for a 17-node Columbus dataset and
    the shape mismatch would surface somewhere far less obvious.
    """
    names = node_names(spec, city)
    n_nodes = len(names)
    n_neigh = city.n_neigh
    index = {name: i for i, name in enumerate(names)}
    counts: dict[str, int] = {}

    W = np.zeros((n_nodes, n_nodes), dtype=np.float64)
    anchor_pairs = _anchor_edges(spec, city)

    # --- 1. Geographic -----------------------------------------------------
    if spec.geo:
        adjacency: dict[int, set[int]] = collections.defaultdict(set)
        for a, b in city.geo_edges:
            adjacency[index[a]].add(index[b])
            adjacency[index[b]].add(index[a])

        one_hop = city.geo_edges if not spec.uniform_complete else []
        for a, b in [*one_hop, *anchor_pairs]:
            i, j = index[a], index[b]
            W[i, j] += 1.0
            W[j, i] += 1.0
        counts["geo_1hop"] = len(one_hop) + len(anchor_pairs)
        counts["anchor_edges"] = len(anchor_pairs)

        if spec.geo_max_hop >= 2 and not spec.uniform_complete:
            hop_counts: collections.Counter = collections.Counter()
            for i in range(n_neigh):
                for node, distance in _hop_distances(adjacency, i).items():
                    if node < n_neigh and 2 <= distance <= spec.geo_max_hop:
                        W[i, node] += spec.geo_decay ** (distance - 1)
                        if i < node:
                            hop_counts[distance] += 1
            for hop, count in sorted(hop_counts.items()):
                counts[f"geo_{hop}hop"] = count

    # --- 2. Uniform complete control ---------------------------------------
    if spec.uniform_complete:
        for i in range(n_neigh):
            for j in range(i + 1, n_neigh):
                W[i, j] += 1.0
                W[j, i] += 1.0
        counts["uniform"] = n_neigh * (n_neigh - 1) // 2

    # --- 3. Correlation / functional ---------------------------------------
    W_corr = None
    if spec.corr:
        corr_matrix = _correlation_matrix(flu_history)
        target = np.zeros_like(W) if spec.dual else W
        n_corr = 0
        for i in range(n_neigh):
            for j in range(i + 1, n_neigh):
                r = corr_matrix[i, j]
                if np.isfinite(r) and r > spec.corr_threshold:
                    weight = spec.corr_coef * (1.0 if spec.corr_binary else float(r))
                    target[i, j] += weight
                    target[j, i] += weight
                    n_corr += 1
        counts["corr"] = n_corr
        if spec.dual:
            # Anchors carry no flu series, so they get geographic edges only.
            for a, b in anchor_pairs:
                i, j = index[a], index[b]
                target[i, j] += 1.0
                target[j, i] += 1.0
            W_corr = target

    # --- 4. Demographic similarity -----------------------------------------
    if spec.demo:
        if static is None:
            raise ValueError("GraphSpec.demo is set but no static demographics were provided.")
        from scipy.spatial.distance import pdist, squareform

        distances = squareform(pdist(static.astype(np.float64)))
        bandwidth = np.median(distances[distances > 0])
        similarity = np.exp(-(distances ** 2) / (2 * bandwidth ** 2))
        np.fill_diagonal(similarity, 0.0)
        n_demo = 0
        for i in range(n_neigh):
            for j in range(i + 1, n_neigh):
                if similarity[i, j] > spec.demo_threshold:
                    weight = spec.demo_coef * float(similarity[i, j])
                    W[i, j] += weight
                    W[j, i] += weight
                    n_demo += 1
        counts["demo"] = n_demo

    # --- 5. Transit / mobility ---------------------------------------------
    if spec.transit:
        if mbta is None:
            raise ValueError("GraphSpec.transit is set but no MBTA matrix was provided.")
        n_transit = 0
        for i in range(n_neigh):
            for j in range(i + 1, n_neigh):
                if mbta[i, j] > spec.transit_threshold:
                    weight = spec.transit_coef * float(mbta[i, j])
                    W[i, j] += weight
                    W[j, i] += weight
                    n_transit += 1
        counts["transit"] = n_transit

    # 'seven' is Boston's anchor count and survives as the historical spelling in
    # saved run_config.json files; 'full' is the city-neutral synonym. Both mean
    # "use this city's complete anchor set", which is 7 nodes / 21 edges in Boston
    # and 3 nodes / 10 edges in Columbus.
    if spec.anchors in ("seven", "full") and \
            counts.get("anchor_edges", 0) != len(city.geo_edges_anchor):
        raise ValueError(
            f"Expected {len(city.geo_edges_anchor)} anchor edges for {city.label}, built "
            f"{counts.get('anchor_edges', 0)}. Anchors differ only by their edge "
            "sets -- identical edges would make them indistinguishable."
        )

    binary = (W > 0).astype(float)
    np.fill_diagonal(binary, 1.0)
    return Graph(node_names=names, n_nodes=n_nodes, n_neigh=n_neigh,
                 W=W, A=binary, counts=counts, W_corr=W_corr)


def _correlation_matrix(flu_history: pd.DataFrame) -> np.ndarray:
    """Pairwise Pearson correlation of neighborhood ILI series.

    Uses pandas rather than np.corrcoef so that suppressed weeks (NaN) are
    handled pairwise instead of poisoning the whole matrix.
    """
    matrix = flu_history.corr(method="pearson", min_periods=12).to_numpy(dtype=np.float64)
    np.fill_diagonal(matrix, 0.0)
    return matrix
