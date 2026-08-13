"""Filesystem locations. Every path in the project resolves through here.

Paths are derived from this file's location, so scripts work from any cwd.
"""

from __future__ import annotations

from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
ROOT = CODE_DIR.parent

DATA_DIR = ROOT / "Data"
BPHC_FLU_DIR = DATA_DIR / "BPHC Flu Data"
BPHC_COVID_RSV_DIR = DATA_DIR / "BPHC Covid and RSV Data"
WEATHER_DIR = DATA_DIR / "Weather"
MBTA_DIR = DATA_DIR / "MBTA"
NEIGHBORHOOD_DIR = DATA_DIR / "Neighborhood Data"
VACCINATION_DIR = DATA_DIR / "Mass Flu Vaccination Data"

FLU_FILE = BPHC_FLU_DIR / "BPHC Dashboard Influenza Neighborhood.csv"
FLU_ED_TYPE1_FILE = BPHC_FLU_DIR / "BPHC Dashboard Influenza ED Visits-type 1.csv"
FLU_ED_TYPE2_FILE = BPHC_FLU_DIR / "BPHC Dashboard Influenza ED Visits-type 2.csv"
FLU_DEMOGRAPHICS_FILE = BPHC_FLU_DIR / "BPHC Dashboard Influenza Demographics.csv"
FLU_WASTEWATER_FILE = BPHC_FLU_DIR / "BPHC Dashboard Influenza Wastewater.csv"

COVID_CASES_FILE = BPHC_COVID_RSV_DIR / "COVID" / "BPHC Dashboard COVID Cases Neighborhood.csv"
COVID_TESTING_FILE = BPHC_COVID_RSV_DIR / "COVID" / "BPHC Dashboard COVID Testing Neighborhood.csv"
COVID_WASTEWATER_FILE = BPHC_COVID_RSV_DIR / "COVID" / "BPHC Dashboard COVID cases in Wastewater.csv"
RSV_CASES_FILE = BPHC_COVID_RSV_DIR / "RSV" / "BPHC Dashboard Confirmed RSV Cases - Neighborhood.csv"
RSV_WASTEWATER_FILE = BPHC_COVID_RSV_DIR / "RSV" / "BPHC Dashboard RSV cases in Wastewater.csv"

MBTA_ADJACENCY_FILE = MBTA_DIR / "mbta_adjacency_matrix.csv"

RESULTS_DIR = CODE_DIR / "results"
CHECKPOINT_DIR = CODE_DIR / "checkpoints"
EMISSIONS_DIR = RESULTS_DIR / "_emissions"
CACHE_DIR = RESULTS_DIR / "_cache"
COMPARISON_DIR = RESULTS_DIR / "_comparison"
DIAGNOSTICS_DIR = RESULTS_DIR / "_diagnostics"
DOCS_DIR = CODE_DIR / "docs"


def require(path: Path, what: str) -> Path:
    """Fail with an actionable message instead of a bare FileNotFoundError."""
    if not path.exists():
        raise FileNotFoundError(f"{what} not found: {path}")
    return path
