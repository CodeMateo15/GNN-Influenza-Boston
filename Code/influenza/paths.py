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

# --- Columbus OH / Franklin County -----------------------------------------
# The three case extracts are line-level (one row per ED visit or per case), so
# unlike the BPHC files they carry no rate and no denominator. COLUMBUS_STATIC_FILE
# is the scraped ACS/Gazetteer table that supplies the per-100,000 denominator;
# it is written by Code/scrapers/scrape_acs_columbus.py, not shipped by an agency.
COLUMBUS_DIR = DATA_DIR / "Columbus Influenza Data"
COLUMBUS_ILI_FILE = COLUMBUS_DIR / "ILI Specified Data-Franklin_final.xlsx"
COLUMBUS_IAH_FILE = COLUMBUS_DIR / "IAH Data CPH Franklin_final.csv"
COLUMBUS_COVID_FILE = COLUMBUS_DIR / "COVID Data CPH Franklin_final.csv"
COLUMBUS_ZIP_AREAS_FILE = COLUMBUS_DIR / "Columbus_FC_Zip_Areas_Nov2019.xlsx"
COLUMBUS_STATIC_FILE = COLUMBUS_DIR / "columbus_area_static.csv"
COLUMBUS_WEATHER_DIR = DATA_DIR / "Columbus Weather"
COLUMBUS_COTA_ADJACENCY_FILE = COLUMBUS_DIR / "cota_adjacency_matrix.csv"

RESULTS_DIR = CODE_DIR / "results"
CHECKPOINT_DIR = CODE_DIR / "checkpoints"
EMISSIONS_DIR = RESULTS_DIR / "_emissions"
CACHE_DIR = RESULTS_DIR / "_cache"
COMPARISON_DIR = RESULTS_DIR / "_comparison"
DIAGNOSTICS_DIR = RESULTS_DIR / "_diagnostics"
CROSS_HORIZON_DIR = RESULTS_DIR / "_comparison_horizons"
DOCS_DIR = CODE_DIR / "docs"


def city_root(city_name: str, base: Path | None = None) -> Path:
    """Results/checkpoint root for one city.

    Boston keeps the historical top-level layout so that the many relative links
    in docs/METHODS.md and every committed artifact path stay valid; a second
    city gets a subdirectory. Renaming Boston's tree would have been tidier and
    would have broken ~40 doc links and every path in the committed
    run_config.json files for no analytical gain.
    """
    base = base or RESULTS_DIR
    return base if city_name == "boston" else base / city_name


def horizon_dir(horizon: int, root: Path | None = None) -> Path:
    """results/horizon_04/ -- the output root for one forecast horizon.

    Zero-padded so a directory listing sorts numerically, and two levels above
    metrics.csv so compare_models.py's `*/*/metrics.csv` glob works unchanged
    when pointed at one of these, and cannot see them when pointed at the root.
    """
    return (root or RESULTS_DIR) / f"horizon_{horizon:02d}"


def comparison_dir(results_root: Path | None = None) -> Path:
    """The _comparison directory belonging to a given results root.

    Without this, every horizon's leaderboard would overwrite the same six
    files in the top-level _comparison/.
    """
    return (results_root or RESULTS_DIR) / "_comparison"


def display(path: Path, base: Path | None = None) -> str:
    """Path relative to `base` for logging, falling back to absolute.

    `Path.relative_to` raises when the target sits outside the base, which any
    --checkpoint-dir or --output-dir outside the repo does. A run_config field
    is not worth crashing a completed run over.
    """
    try:
        return str(path.relative_to(base or CODE_DIR))
    except ValueError:
        return str(path)


def require(path: Path, what: str) -> Path:
    """Fail with an actionable message instead of a bare FileNotFoundError."""
    if not path.exists():
        raise FileNotFoundError(f"{what} not found: {path}")
    return path
