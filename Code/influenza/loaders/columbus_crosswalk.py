"""The Columbus ZIP -> area crosswalk, and the 17-area node definition.

Franklin County's public-health extracts are keyed by 5-digit ZIP. The
`Columbus_FC_Zip_Areas_Nov2019.xlsx` workbook supplies a ZIP -> area map at two
resolutions: a fine `Area*` column (45 labels, mostly one per ZIP) and a coarse
`17 Areas` column. We use the coarse one, because 17 nodes against ~3.5 seasons
of weekly data is the same data-per-node regime as Boston's 14, whereas the 44
ZIPs that actually appear in the ILI file are 3x more nodes on the same history.

Aggregating to the 17 areas is also what makes the panel usable: 23.3% of
ZIP-weeks are zero, against 3.1% of area-weeks.

This module is deliberately import-cheap (pandas + openpyxl only) so that the
scrapers can reuse it without pulling in the modelling stack.
"""

from __future__ import annotations

import pandas as pd

from .. import paths

# The workbook's real header is on the second row; the first is blank and the
# last four rows are footnotes ('*Area named by MShea', etc).
_HEADER_ROW = 1

# The '17 Areas' column header carries a TRAILING SPACE in the source file.
# Reading it by exact name is a silent KeyError waiting to happen, so the reader
# normalises every header instead of hardcoding the typo.
_ZIP_COLUMN = "zip code"
_AREA_COLUMN = "17 areas"
_FINE_AREA_COLUMN = "area*"

# ZIPs the ILI extract reports but the Nov-2019 crosswalk never lists. They are
# 107 of 63,103 ILI rows (0.17%); a further 147 rows sit in the seven fringe ZIPs
# that the crosswalk lists but leaves unassigned. They are named here so a future
# crosswalk revision that covers them shows up as a failed assertion rather
# than as a silent change in the denominator.
KNOWN_UNMAPPED_ZIPS = (43086, 43109, 43216, 43234)


def _normalise_headers(frame: pd.DataFrame) -> pd.DataFrame:
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    return frame


def load_crosswalk(path=None) -> pd.DataFrame:
    """ZIP -> (area, fine_area). One row per ZIP listed in the workbook.

    Returns only the ZIPs that carry a `17 Areas` label. The seven that do not
    are the county-fringe ZIPs and become anchor nodes; `load_anchor_zips()`
    returns those separately rather than dropping them on the floor.
    """
    file = paths.require(path or paths.COLUMBUS_ZIP_AREAS_FILE, "Columbus ZIP-area crosswalk")
    frame = _normalise_headers(pd.read_excel(file, header=_HEADER_ROW))

    missing = {_ZIP_COLUMN, _AREA_COLUMN} - set(frame.columns)
    if missing:
        raise ValueError(
            f"{file.name}: expected columns {sorted(missing)} after header "
            f"normalisation; found {list(frame.columns)}. The workbook layout changed."
        )

    frame = frame.dropna(subset=[_ZIP_COLUMN]).copy()
    frame["zip"] = frame[_ZIP_COLUMN].astype(int)
    frame["area"] = frame[_AREA_COLUMN].astype("string").str.strip()
    frame["fine_area"] = frame[_FINE_AREA_COLUMN].astype("string").str.strip()
    return frame[["zip", "area", "fine_area"]].reset_index(drop=True)


def zip_to_area(path=None) -> dict[int, str]:
    """ZIP -> one of the 17 area names, for the ZIPs that have one."""
    frame = load_crosswalk(path)
    assigned = frame.loc[frame["area"].notna()]
    return dict(zip(assigned["zip"], assigned["area"]))


def load_anchor_zips(path=None) -> list[int]:
    """The county-fringe ZIPs with no area assignment.

    These are the Columbus analogue of Boston's feature-less anchor nodes: they
    sit at the edge of the reporting geography and carry almost no ILI volume
    (147 rows between them), so they exist to give edge areas somewhere for
    signal to flow rather than treating the county line as a wall.
    """
    frame = load_crosswalk(path)
    return sorted(frame.loc[frame["area"].isna(), "zip"].tolist())


def area_names(path=None) -> list[str]:
    """The 17 area names, sorted, which fixes the canonical node order 0..16.

    Sorted rather than source-order because the workbook's row order is not
    meaningful and a stable order is what makes the `pred[:n_neigh]` slice and
    every saved checkpoint reproducible.
    """
    return sorted(set(zip_to_area(path).values()))
