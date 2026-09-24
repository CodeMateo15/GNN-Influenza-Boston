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

import pandas as pd
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

    # --- Season geometry ----------------------------------------------------
    # These were module constants in constants.py, which was fine for two
    # Northern-Hemisphere cities and wrong the moment a Southern one arrived.
    # Buenos Aires peaks in epiweeks 22-24 -- an exact six-month mirror of
    # Boston -- so every one of these flips for it.
    #
    # `flu_months` splits the year into the two reporting segments.
    # `season_start_month` is the boundary a season is NAMED from: the month
    # the series is at its annual floor, so no observed week moves between
    # seasons. August for the US cities (MEM's ISO week 30, rounded to a month
    # boundary); February for Buenos Aires, whose floor is December-February.
    flu_months: frozenset[int] = frozenset({10, 11, 12, 1, 2, 3})
    season_start_month: int = 8

    # Evaluation window, when this city cannot use the shared one. None means
    # "use constants.TEST_START/TEST_END", which is what both US cities do --
    # scoring them on the same weeks is the point of a shared window.
    #
    # Buenos Aires cannot: its surveillance backfills for months, so its last
    # fully-reported week is well before Boston's. Scoring it on the shared
    # window would score a model against weeks that were still filling in, and
    # report the resulting under-prediction as model error.
    test_start: str | None = None
    test_end: str | None = None
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

    # --- Season helpers ---------------------------------------------------------
    # Every consumer that used to hardcode "Oct-Mar", June-May backtest folds or
    # the shared test window reads these instead, so a city with a different
    # season geometry cannot be half-configured.

    @property
    def season_first_month(self) -> int:
        """First calendar month of the flu season (Oct for Boston, Apr for AMBA)."""
        months = set(self.flu_months)
        return next(m for m in range(1, 13)
                    if m in months and ((m - 2) % 12) + 1 not in months)

    def _span_label(self, first: int, length: int) -> str:
        import calendar
        last = ((first - 1 + length - 1) % 12) + 1
        return f"{calendar.month_abbr[first]}–{calendar.month_abbr[last]}"

    @property
    def flu_season_label(self) -> str:
        """"Oct–Mar" style label for the flu season."""
        return self._span_label(self.season_first_month, len(self.flu_months))

    @property
    def off_season_label(self) -> str:
        first = ((self.season_first_month - 1 + len(self.flu_months)) % 12) + 1
        return self._span_label(first, 12 - len(self.flu_months))

    @property
    def segment_labels(self) -> dict[str, str]:
        return {"overall": "Overall (full year)",
                "flu_season": f"Flu season ({self.flu_season_label})",
                "off_season": f"Off-season ({self.off_season_label})"}

    def backtest_window(self, year: int) -> tuple[str, str]:
        """(start, end) of a one-season backtest fold labelled `year`.

        The fold opens four months before the flu season starts, so it carries
        the whole off-season run-up: June-May for Boston and Columbus (whose
        season starts in October) -- exactly the fold run_backtest.py always
        used -- and December-November for Buenos Aires.
        """
        start = ((self.season_first_month - 1 - 4) % 12) + 1
        begin = pd.Timestamp(year=year, month=start, day=1)
        end = begin + pd.DateOffset(years=1) - pd.Timedelta(days=1)
        return str(begin.date()), str(end.date())

    def evaluation_window(self) -> tuple[pd.Timestamp, pd.Timestamp]:
        """This city's test window: its own if declared, else the shared one."""
        from ..constants import TEST_END, TEST_START
        return (pd.Timestamp(self.test_start) if self.test_start else TEST_START,
                pd.Timestamp(self.test_end) if self.test_end else TEST_END)

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


# One list, used by both `get` and `names`. These were two separate literals
# that had to be edited together; adding a third city is exactly the moment
# that kind of duplication bites.
_CITY_MODULES = (("boston", "BOSTON"), ("columbus", "COLUMBUS"),
                 ("buenos_aires", "BUENOS_AIRES"))


def get(name: str) -> City:
    """Look up a city by slug, with an actionable error."""
    registry = {slug: getattr(importlib.import_module(f"{__name__}.{slug}"), attr)
                for slug, attr in _CITY_MODULES}
    if name not in registry:
        raise ValueError(f"Unknown city {name!r}. Available: {', '.join(sorted(registry))}.")
    return registry[name]


def names() -> tuple[str, ...]:
    return tuple(slug for slug, _ in _CITY_MODULES)


DEFAULT_CITY = "boston"
