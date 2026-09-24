"""Buenos Aires / AMBA data access. Same duck-typed surface as the other cities.

`samples.load_dataset` calls `load_rates`, `load_weather`,
`load_static_demographics` and `load_globals` on whatever module a City names,
so this file's job is to present those four and nothing else.

Three honest limits, all of which are properties of the source rather than of
the work done so far:

  1. SNVS publishes ETI case COUNTS. The per-100,000 denominator is the INDEC
     2022 census population, committed as amba_partido_static.csv.
  2. Five of the eight demographic columns, not eight. The 2022 census asks
     neither commute mode nor vehicle availability, and has no construct that
     matches `nonwhite_share`. `load_static_demographics` returns the five it
     has, by name; two of them are a derived age cut and a proxy (see the CSV
     header).
  3. The panel's last weeks are still backfilling. `load_rates` trims them
     using the revision table the builder already computes, so a run does not
     silently score a model against half-reported weeks.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd

from .. import paths
from ..cities.buenos_aires import PARTIDOS, SHORT_OF
from ..constants import STATIC_DEMO_COLS, WEATHER_COLS

# A week whose reported total is below this share of its eventual value is
# still filling in. 0.95 rather than 1.0 because the revision table's own
# median completeness never quite reaches 1 even at long lags -- late
# corrections are open-ended -- so demanding exactness would trim forever.
COMPLETENESS_FLOOR = 0.95


def _read_panel() -> pd.DataFrame:
    """Long panel -> weeks x partidos, NaN preserved."""
    path = paths.require(paths.AMBA_PANEL_FILE, "AMBA weekly ETI panel")
    frame = pd.read_csv(path, parse_dates=["week_start"])
    wide = frame.pivot(index="week_start", columns="partido", values="cases")
    wide.columns.name = None
    wide.index.name = "date"
    return wide.sort_index()


def _trim_incomplete_tail(wide: pd.DataFrame) -> pd.DataFrame:
    """Drop trailing weeks that the newest vintage had not finished reporting.

    The builder writes a revision table giving, for each reporting lag, the
    median share of a week's eventual total that had arrived by then. The tail
    of the panel sits at short lags, so its counts are systematically low --
    2026-02-22 came in at 1,019 and 2026-03-01 at 500 against a ~1,600 January
    baseline, which is backfill, not an epidemic collapse.

    Trimming from the curve rather than by a fixed number of weeks means this
    stays right when a newer vintage is dropped in.
    """
    revision = pd.read_csv(paths.require(paths.AMBA_REVISION_FILE,
                                         "AMBA revision table"))
    curve = (revision[revision.lag_weeks.between(0, 52)]
             .groupby("lag_weeks").completeness.median().sort_index())
    # The curve is NOT monotone -- it runs 0.93 at lag 12, dips to 0.89 at 13,
    # recovers to 0.95 at 14 and dips again to 0.94 at 15. Taking the first lag
    # that touches the floor would therefore accept weeks that are still
    # filling in. Take the lag from which it STAYS at or above the floor.
    below = curve[curve < COMPLETENESS_FLOOR]
    if below.empty:
        return wide
    lag_needed = int(below.index.max()) + 1
    if lag_needed > int(curve.index.max()):
        raise ValueError("the backfill curve never settles above "
                         f"{COMPLETENESS_FLOOR}; refusing to guess a cutoff.")
    cutoff = wide.index.max() - pd.Timedelta(weeks=lag_needed)
    return wide.loc[wide.index <= cutoff]


def load_partido_population() -> pd.Series:
    """INDEC 2022 census population per partido, the rate denominator."""
    path = paths.require(paths.AMBA_STATIC_FILE, "AMBA static table")
    frame = pd.read_csv(path, comment="#").set_index("partido")
    return frame["population"].astype(float)


def load_counts() -> pd.DataFrame:
    """Weekly ETI counts, scored partidos only, blackout weeks left NaN."""
    wide = _trim_incomplete_tail(_read_panel())
    return wide.reindex(columns=PARTIDOS)


def load_rates() -> pd.DataFrame:
    """Weekly ETI cases per 100,000, weeks x 19 scored partidos.

    NaN where the builder judged a reporting blackout (three or more
    consecutive absent weeks). Those stay NaN rather than becoming zero, so
    they are masked out of the loss and the metrics the same way Boston's
    suppressed cells are -- a blackout is missing data, not an absence of flu.
    """
    counts = load_counts()
    population = load_partido_population().reindex(counts.columns)
    if population.isna().any():
        missing = list(population[population.isna()].index)
        raise ValueError(
            f"No INDEC population for {missing}. Every scored partido needs a "
            "denominator; run Code/scrapers/build_amba_static.py."
        )
    return counts.div(population, axis=1) * 100_000.0


def load_static_demographics(path=None) -> tuple[np.ndarray, list[str], dict]:
    """Min-max scaled demographics for the scored partidos: FIVE columns.

    Same scaling as Boston and Columbus, so the three cities' static blocks are
    comparable in the sense that matters to the model -- each column spans 0-1
    within its own city. Returns the column NAMES alongside the matrix because
    they are a subset of STATIC_DEMO_COLS here, and `samples._feature_names`
    labels the static block from what the loader says it returned.

    `pct_children` is under-15 (derived from the dependency index) and
    `poverty_rate` is the no-health-coverage share; see the CSV header.
    """
    path = paths.require(path or paths.AMBA_STATIC_FILE, "AMBA static table")
    frame = pd.read_csv(path, comment="#").set_index("partido")
    columns = [c for c in STATIC_DEMO_COLS if c in frame.columns]
    static = frame.reindex(PARTIDOS)[columns]
    if static.isna().any().any():
        raise ValueError(f"missing demographic values for "
                         f"{list(static.index[static.isna().any(axis=1)])}")
    span = (static.max() - static.min()).replace(0, 1.0)
    normalized = (static - static.min()) / span
    return normalized.to_numpy(dtype=np.float32), columns, {}


def partido_slug(partido: str) -> str:
    """Filename-safe key for a partido, used by the weather scraper."""
    import unicodedata

    stripped = "".join(c for c in unicodedata.normalize("NFD", partido)
                       if unicodedata.category(c) != "Mn")
    return stripped.lower().replace(" ", "_").replace(".", "")


def load_weather(week_index: pd.DatetimeIndex) -> dict[str, np.ndarray]:
    """Per-partido weekly weather. Returns column -> (weeks, n_nodes) array.

    Mirrors the Columbus loader, including the city-wide-median fill for gaps:
    the files come from our own scraper, so their names are canonical rather
    than something to pattern-match.
    """
    directory = paths.require(paths.AMBA_WEATHER_DIR, "Buenos Aires weather directory")
    files = sorted(glob.glob(str(directory / "*_weather_weekly.csv")))
    if not files:
        raise FileNotFoundError(
            f"No '*_weather_weekly.csv' files in {directory}. Run "
            "Code/scrapers/scrape_weather_buenos_aires.py first."
        )

    slug_to_index = {partido_slug(p): i for i, p in enumerate(PARTIDOS)}
    by_node: dict[int, pd.DataFrame] = {}
    unmapped: list[str] = []
    for path in files:
        slug = Path(path).name.removesuffix("_weather_weekly.csv")
        node = slug_to_index.get(slug)
        if node is None:
            unmapped.append(Path(path).name)
            continue
        by_node[node] = (pd.read_csv(path, parse_dates=["week_start"])
                         .set_index("week_start").sort_index()[WEATHER_COLS])
    if unmapped:
        raise ValueError(f"Weather files not mapped to a partido: {unmapped}")
    missing = [p for i, p in enumerate(PARTIDOS) if i not in by_node]
    if missing:
        raise ValueError(f"No weather file for {missing}.")

    arrays: dict[str, np.ndarray] = {}
    for column in WEATHER_COLS:
        stacked = np.column_stack([
            by_node[i][column].reindex(week_index).to_numpy(dtype=float)
            for i in range(len(PARTIDOS))
        ])
        # Same fill as the other two cities: a city-wide median for the week,
        # so a single missing station does not punch a hole in every node.
        medians = np.nanmedian(stacked, axis=1)
        gaps = np.isnan(stacked)
        stacked[gaps] = np.take(medians, np.where(gaps)[0])
        arrays[column] = stacked
    return arrays


def load_globals(week_index: pd.DatetimeIndex, names) -> pd.DataFrame:
    """City-wide covariates. Only `ili_count` exists for Buenos Aires."""
    columns: dict[str, pd.Series] = {}
    for name in names:
        if name == "ili_count":
            counts = load_counts().sum(axis=1, min_count=1)
            columns[name] = counts.reindex(week_index)
        else:
            raise ValueError(
                f"Buenos Aires has no {name!r} covariate. Available: ili_count."
            )
    return pd.DataFrame(columns, index=week_index)
