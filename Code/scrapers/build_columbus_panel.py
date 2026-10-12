"""Aggregate the Columbus line-level extracts to weekly per-area counts.

Columbus Public Health supplied three line-level extracts (one row per ED visit,
hospitalisation or COVID case, with a home ZIP). CPH cleared the data for public
release at the aggregate level but asked that the line-level files stay with the
project, so they are gitignored and this script is the only thing that reads
them. It writes the weekly per-area counts that the loader
(influenza/loaders/columbus.py) and every model use, and those ARE committed:

    Data/Columbus Influenza Data/columbus_ili_weekly_counts.csv
    Data/Columbus Influenza Data/columbus_iah_weekly_counts.csv
    Data/Columbus Influenza Data/columbus_covid_weekly_counts.csv

Each is week_start (Sunday) x the 17 crosswalk areas. The aggregation is exactly
what the loaders used to compute inline, so rebuilding changes no result.

    python Code/scrapers/build_columbus_panel.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402
from influenza.loaders import columbus  # noqa: E402

HEADER = ("# Weekly per-area counts aggregated from Columbus Public Health line-level "
          "extracts by Code/scrapers/build_columbus_panel.py.\n"
          "# Areas: the 17-area Columbus/Franklin County ZIP crosswalk. {note}\n")


def write(frame, path: Path, note: str) -> None:
    out = frame.copy()
    out.index.name = "week_start"
    with path.open("w") as handle:
        handle.write(HEADER.format(note=note))
        out.to_csv(handle, date_format="%Y-%m-%d")
    print(f"  {path.name}: {out.shape[0]} weeks x {out.shape[1]} areas, "
          f"{int(out.sum().sum()):,} cases")


def main() -> None:
    print("Aggregating Columbus line-level extracts...")
    write(columbus.build_counts(), paths.COLUMBUS_ILI_WEEKLY_FILE,
          "ILI ED visits; partial first/last weeks dropped; 0 = no qualifying visit.")
    write(columbus.build_weekly_cases("iah"), paths.COLUMBUS_IAH_WEEKLY_FILE,
          "Influenza-associated hospitalisations by MMWR week; blank = no case that week.")
    write(columbus.build_weekly_cases("covid"), paths.COLUMBUS_COVID_WEEKLY_FILE,
          "COVID cases by MMWR week; blank = no case that week.")


if __name__ == "__main__":
    main()
