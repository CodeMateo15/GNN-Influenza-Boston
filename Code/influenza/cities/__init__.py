"""City profiles: everything that differs between the cities on one object.

Before this existed, Boston's 14 node names, 7 anchors, hand-coded edge list and
name crosswalks were module-level constants in `influenza/constants.py`, imported
at import time by nine other modules. That is fine for one city and impossible
for two.

The alternative -- forking `Code/` into a second tree -- was rejected because
this repository has already been through that failure. `windows.py` opens with
"the two baseline scripts had two copies of this logic that differed only in...",
`config.py` with "the three notebooks this replaced differed in only six cells",
and DATA_NOTES.md records that the two defects which voided every result before
August 2026 "affected all eight notebooks and both baselines" -- eight copies to
fix. A shared code path also makes "the same models work on another city" a fact
rather than an assertion, which is the whole point of adding Columbus.

What is deliberately NOT here: the evaluation window, FLU_MONTHS, LOOKBACK,
SEED, WEATHER_COLS and STATIC_DEMO_COLS. Those are shared by construction -- both
cities are scored on the same weeks with the same feature definitions, and that
is what makes the comparison meaningful.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from types import ModuleType


@dataclass(frozen=True)
class City:
    """One city's geography, node set, graph topology and data provenance.

    Scored nodes occupy indices 0..n_neigh-1 and anchors n_neigh.., which is what
    makes the `pred[:n_neigh]` slice safe everywhere. That invariant is
    load-bearing across training, metrics and interpretability, so it is asserted
    in __post_init__ rather than trusted.
    """

    name: str                                   # slug, used in paths and CLI
    label: str                                  # display name
    node_label: str                             # "neighborhood" / "area"
    node_names: tuple[str, ...]                 # scored nodes, canonical order
    short_names: tuple[str, ...]                # plot labels, same order
    anchor_names: tuple[str, ...]
    anchor_short: tuple[str, ...]
    background_short: str
    geo_edges: tuple[tuple[str, str], ...]          # on SHORT names
    geo_edges_anchor: tuple[tuple[str, str], ...]
    geo_edges_background: tuple[tuple[str, str], ...]
    coords: dict[str, tuple[float, float]]
    loader_module: str                          # importable path, resolved lazily
    available_globals: tuple[str, ...]
    available_features: frozenset[str]
    variants: tuple[str, ...]                   # which time-filter variants exist
    suppresses_small_counts: bool               # True -> absent weeks are NaN
    notes: str = ""

    def __post_init__(self) -> None:
        if len(self.node_names) != len(self.short_names):
            raise ValueError(
                f"{self.name}: {len(self.node_names)} node names but "
                f"{len(self.short_names)} short names; they are positionally paired."
            )
        if len(self.anchor_names) != len(self.anchor_short):
            raise ValueError(f"{self.name}: anchor name/short-name counts differ.")
        overlap = set(self.short_names) & set(self.anchor_short)
        if overlap:
            raise ValueError(
                f"{self.name}: {sorted(overlap)} is both a scored node and an anchor. "
                "Node indices would be ambiguous."
            )
        known = set(self.short_names) | set(self.anchor_short) | {self.background_short}
        for label, edges in (("geo_edges", self.geo_edges),
                             ("geo_edges_anchor", self.geo_edges_anchor),
                             ("geo_edges_background", self.geo_edges_background)):
            unknown = {n for pair in edges for n in pair} - known
            if unknown:
                raise ValueError(f"{self.name}: {label} references unknown nodes {sorted(unknown)}.")

    @property
    def n_neigh(self) -> int:
        return len(self.node_names)

    @property
    def n_anchors(self) -> int:
        return len(self.anchor_names)

    @property
    def loaders(self) -> ModuleType:
        """The city's loader module. Imported lazily to avoid a cycle.

        `loaders.columbus` imports `paths` and `constants`, and `constants`
        imports `cities.boston`, so resolving this at class-definition time
        would deadlock the import graph.
        """
        return importlib.import_module(self.loader_module)

    def supports(self, feature: str) -> bool:
        return feature in self.available_features

    def require_feature(self, feature: str) -> None:
        """Fail loudly rather than feeding a model zeros for absent data.

        Columbus has no RSV series at all. Without this, `--rsv --city columbus`
        would z-score an all-NaN column to zeros and quietly train a model on a
        constant, which looks like a null result rather than a missing input.
        """
        if not self.supports(feature):
            raise ValueError(
                f"{self.label} has no {feature!r} data. Available for {self.label}: "
                f"{', '.join(sorted(self.available_features))}."
            )

    def short_of(self, node_name: str) -> str:
        return self.short_names[self.node_names.index(node_name)]


def get(name: str) -> City:
    """Look up a city by slug, with an actionable error."""
    from .boston import BOSTON
    from .columbus import COLUMBUS

    registry = {c.name: c for c in (BOSTON, COLUMBUS)}
    if name not in registry:
        raise ValueError(f"Unknown city {name!r}. Available: {', '.join(sorted(registry))}.")
    return registry[name]


def names() -> tuple[str, ...]:
    return ("boston", "columbus")


DEFAULT_CITY = "boston"
