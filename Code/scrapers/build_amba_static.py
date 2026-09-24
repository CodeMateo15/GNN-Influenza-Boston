"""Build the Buenos Aires per-partido static table from the INDEC 2022 census.

    python Code/scrapers/build_amba_static.py
    python Code/scrapers/build_amba_static.py --cache-dir <dir with the xlsx>

Boston's static features come from City of Boston indicator tables; Columbus's
are reconstructed from the US Census ACS API. Argentina has no API, but INDEC's
2022 definitive results are published as ~100 per-topic workbooks per province,
and a good share of them are broken down PER PARTIDO. This script downloads the
five that map onto the project's demographic columns and reduces them to the 24
AMBA districts the ETI panel covers.

Output: Data/Buenos Aires Acute Respiratory Infections/amba_partido_static.csv,
raw ratios with a provenance header. Min-max normalisation happens in the
loader, as it does for both other cities.

Column by column
----------------
    population, area_km2, pop_density   est_c2_2   exact
    pct_elderly                         est_c7_2   exact: share aged 65+
    owner_rate                          hogares_c6_2  exact: owned / all households
    pct_children                        est_c9_2 + est_c7_2   DERIVED, and a
        different age cut. INDEC publishes the potential dependency index
        D = 100 * (pop 0-14 + pop 65+) / pop 15-64 per partido, but not the
        0-14 share itself. With e = share 65+, the young share is
        c = D / (100 + D) - e. That is UNDER-15, where Boston and Columbus use
        under-20. After the loader's within-city min-max scaling only the
        ordering of partidos survives, and the two cuts order districts almost
        identically, but the column is not the same quantity and should not be
        compared across cities in raw units.
    poverty_rate                        salud_c1_2   PROXY: share of the
        population with neither an obra social / prepaga nor a state health
        plan. The census has no income or poverty question; lack of any
        coverage is the standard census-based deprivation measure in
        Argentina. It is not the US poverty line.

Deliberately absent
-------------------
    transit_share, no_vehicle_rate   the 2022 questionnaire asks neither commute
                                     mode nor vehicle availability.
    nonwhite_share                   no equivalent construct. Foreign-born and
                                     afro-descendant shares exist per partido,
                                     but they measure something else, and
                                     putting them under this name would make a
                                     cross-city comparison of that column
                                     silently meaningless.

So Buenos Aires carries five of the eight demographic columns, and the loader
returns exactly those five, named.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

BASE = "https://censo.gob.ar/wp-content/uploads/2023/11/"
TABLES = {
    "est_c2_2": "c2022_bsas_est_c2_2.xlsx",          # population, area, density
    "est_c7_2": "c2022_bsas_est_c7_2.xlsx",          # % aged 65+, 1970-2022
    "est_c9_2": "c2022_bsas_est_c9_2.xlsx",          # potential dependency index
    "hogares_c6_2": "c2022_bsas_hogares_c6_2.xlsx",  # household tenure
    "salud_c1_2": "c2022_bsas_salud_c1_2.xlsx",      # health coverage
}
# The five columns this city actually has, in STATIC_DEMO_COLS order.
DEMO_COLUMNS = ("pop_density", "poverty_rate", "pct_children", "pct_elderly",
                "owner_rate")
TIMEOUT = 120
_CODE = re.compile(r"^0?6\d{3}$")


def fetch(name: str, cache: Path) -> Path:
    """The workbook, from the cache if it is there, else from INDEC."""
    import requests

    path = cache / TABLES[name]
    if path.exists():
        return path
    response = requests.get(BASE + TABLES[name], timeout=TIMEOUT,
                            headers={"User-Agent": "Mozilla/5.0"}, verify=False)
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


def partido_rows(workbook: Path, sheet: str | None = None) -> pd.DataFrame:
    """Rows keyed by INDEC department code, from any of these cuadros.

    Every per-partido INDEC table puts a code like "06028" (or 6028) in the
    first column, then the name, then data. Totals and the "24 partidos"
    subtotal carry the bare province code "06" or no code at all, so matching
    four digits after the 6 is what separates districts from aggregates.
    """
    book = pd.ExcelFile(workbook)
    if sheet is None:
        sheet = next(s for s in book.sheet_names
                     if s.lower().startswith("cuadro") or "N°" in s)
    frame = pd.read_excel(book, sheet_name=sheet, header=None)
    codes = frame.iloc[:, 0].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    frame = frame[codes.str.match(_CODE)].copy()
    frame.index = codes[codes.str.match(_CODE)].astype(int)
    return frame


def _last_numeric(row: pd.Series) -> float:
    """The 2022 value in a 1970-2022 time-series cuadro: its last number."""
    values = pd.to_numeric(row.iloc[2:], errors="coerce").dropna()
    return float(values.iloc[-1])


def build(cache: Path, coverage: Path) -> pd.DataFrame:
    names = pd.read_csv(coverage)
    wanted = dict(zip(names.indec, names.partido))

    base = partido_rows(fetch("est_c2_2", cache))
    table = pd.DataFrame({
        "population": pd.to_numeric(base.iloc[:, 3]),
        "area_km2": pd.to_numeric(base.iloc[:, 2]),
    })
    table["pop_density"] = table.population / table.area_km2
    reported = pd.to_numeric(base.iloc[:, 4])
    if not np.allclose(table.pop_density, reported, rtol=1e-3):
        raise SystemExit("population / area does not reconcile with INDEC's own "
                         "density column; the sheet layout has changed.")

    elderly = partido_rows(fetch("est_c7_2", cache)).apply(_last_numeric, axis=1) / 100.0
    dependency = partido_rows(fetch("est_c9_2", cache)).apply(_last_numeric, axis=1)
    table["pct_elderly"] = elderly
    table["pct_children"] = dependency / (100.0 + dependency) - elderly

    tenure = partido_rows(fetch("hogares_c6_2", cache))
    # col 2 = all households, col 3 = "Propia" (owned, any documentation).
    table["owner_rate"] = (pd.to_numeric(tenure.iloc[:, 3])
                           / pd.to_numeric(tenure.iloc[:, 2]))

    health = partido_rows(fetch("salud_c1_2", cache), sheet="Cobertura de Salud N°1.2")
    # col 2 = population, cols 3-5 = obra social/prepaga, state plan, none.
    parts = health.iloc[:, 2:6].apply(pd.to_numeric)
    if not np.allclose(parts.iloc[:, 1:].sum(axis=1), parts.iloc[:, 0], rtol=1e-3):
        raise SystemExit("health-coverage categories do not sum to the population "
                         "column; the sheet layout has changed.")
    table["poverty_rate"] = parts.iloc[:, 3] / parts.iloc[:, 0]

    table = table.loc[table.index.isin(wanted)].copy()
    missing = set(wanted) - set(table.index)
    if missing:
        raise SystemExit(f"INDEC tables are missing partidos {sorted(missing)}; "
                         "refusing to write a table with nodes lacking values.")
    table.insert(0, "partido", table.index.map(wanted))
    table.index.name = "indec"

    ratios = ["pct_children", "pct_elderly", "owner_rate", "poverty_rate"]
    bad = table[ratios].lt(0).any(axis=1) | table[ratios].gt(1).any(axis=1)
    if bad.any():
        raise SystemExit(f"ratio outside [0, 1] for {list(table.partido[bad])}")
    return table.reset_index().sort_values("partido")[
        ["indec", "partido", "population", "area_km2", *DEMO_COLUMNS]]


HEADER = """# Buenos Aires / AMBA per-partido static table.
#
# SOURCE: INDEC, Censo Nacional de Poblacion, Hogares y Viviendas 2022,
# resultados definitivos, Provincia de Buenos Aires, per-partido cuadros:
#   est_c2_2      population, area, density
#   est_c7_2      % of population aged 65+
#   est_c9_2      potential dependency index
#   hogares_c6_2  household tenure regime
#   salud_c1_2    health coverage
#   {base}
# Built by Code/scrapers/build_amba_static.py on {today}.
#
# FIVE of the eight STATIC_DEMO_COLS. Raw ratios; the loader min-max scales.
#   pop_density    exact (reconciles with INDEC's own density column to 0.1%)
#   pct_elderly    exact, share aged 65+
#   owner_rate     exact, owned households / all households
#   pct_children   DERIVED, UNDER-15 (Boston and Columbus use under-20):
#                  c = D / (100 + D) - pct_elderly, D = dependency index
#   poverty_rate   PROXY: share with no obra social, prepaga or state health
#                  plan. The census asks no income question.
# Absent: transit_share and no_vehicle_rate (not asked by the 2022 census) and
# nonwhite_share (no equivalent construct; foreign-born or afro-descendant
# share would measure something else under the same name).
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cache-dir", type=Path, default=paths.AMBA_DIR / "indec",
                        help="Where the INDEC workbooks are kept. Downloaded into "
                             "it when absent.")
    args = parser.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    table = build(args.cache_dir, paths.AMBA_COVERAGE_FILE)
    with open(paths.AMBA_STATIC_FILE, "w") as handle:
        handle.write(HEADER.format(base=BASE, today=datetime.date.today()))
        table.to_csv(handle, index=False)
    print(f"Wrote {len(table)} partidos x {len(DEMO_COLUMNS)} demographic columns")
    print(table[["partido", *DEMO_COLUMNS]].round(3).to_string(index=False))
    print(f"Outputs: {paths.display(paths.AMBA_STATIC_FILE)}")


if __name__ == "__main__":
    main()
