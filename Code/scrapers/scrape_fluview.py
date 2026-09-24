"""Fetch CDC FluView ILINet for HHS Region 1 and Massachusetts.

Output: Data/FluView/fluview_regional_weekly.csv, one row per region-week, on
the same Sunday-start week boundaries as the BPHC flu data.

    python Code/scrapers/scrape_fluview.py
    python Code/scrapers/scrape_fluview.py --first-release   # real-time vintage

Two things about this source are easy to get wrong and both change the answer.

**Week 53.** FluView is indexed by MMWR week, where week 1 is the week
containing January 4 and weeks start on Sunday. Converting with
`Jan 1 + (week - 1) * 7` and snapping back to Sunday collapses week 53 of one
year onto week 1 of the next: 2014w53/2015w01, 2020w53/2021w01 and
2025w53/2026w01 all land on the same Sunday. That last pair sits on the peak of
the season this project evaluates.

**Revisions.** ILINet is revised after first publication, and the endpoint
returns the LATEST issue for each week unless a vintage is requested. Using a
revised value in a forecasting baseline is a look-ahead: nobody had that number
at forecast time. Measured on HHS-1 over 2025w40-2026w10, all 19 weeks were
revised, by up to 7.9%. `--first-release` asks for `lag=0`, the issue published
in the same week, which is what a real-time baseline must use. The default keeps
the latest revision, which is right for a retrospective oracle and wrong for a
baseline.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths

API_URL = "https://api.delphi.cmu.edu/epidata/fluview/"
# HHS Region 1 is New England: CT, ME, MA, NH, RI, VT. `ma` is the state alone --
# narrower and so closer to Boston, but built from fewer reporting providers.
REGIONS = ("hhs1", "ma")
FIRST_EPIWEEK = 201001
LAST_EPIWEEK = 202652


def epiweek_to_sunday(epiweek: int) -> pd.Timestamp:
    """MMWR YYYYWW -> the Sunday that starts it, matching BPHC date_value_start."""
    year, week = divmod(int(epiweek), 100)
    jan4 = pd.Timestamp(year=year, month=1, day=4)
    week1_start = jan4 - pd.Timedelta(days=(jan4.dayofweek + 1) % 7)
    return week1_start + pd.Timedelta(weeks=week - 1)


def fetch(region: str, *, first_release: bool = False) -> pd.DataFrame:
    params = {"regions": region, "epiweeks": f"{FIRST_EPIWEEK}-{LAST_EPIWEEK}"}
    if first_release:
        # `lag=0` selects the issue published in the same week as the data --
        # the first release. Without it the endpoint hands back the latest
        # revision, which no forecaster had at the time.
        params["lag"] = 0
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{API_URL}?{query}", timeout=60) as response:
        payload = json.load(response)
    if payload.get("result") != 1:
        raise SystemExit(f"error: FluView returned {payload.get('result')}: "
                         f"{payload.get('message')}")
    frame = pd.DataFrame(payload["epidata"])
    frame["region"] = region
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--first-release", action="store_true",
                        help="Keep each week's FIRST published issue instead of its "
                             "final revision. Required for a real-time baseline.")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    keep = "first" if args.first_release else "last"
    frames = []
    for region in REGIONS:
        frame = fetch(region, first_release=args.first_release)
        before = len(frame)
        # Belt and braces: `lag=0` should already return one row per week, but a
        # duplicate here would silently double-count a week in the join.
        frame = (frame.sort_values("release_date")
                      .drop_duplicates("epiweek", keep="first" if args.first_release else "last"))
        frame["week"] = frame["epiweek"].map(epiweek_to_sunday)
        if frame["week"].duplicated().any():
            raise SystemExit("error: epiweek -> Sunday is not injective; the week 53 "
                             "conversion in epiweek_to_sunday is wrong.")
        print(f"{region:6s}: {before} issues -> {len(frame)} weeks "
              f"({frame['week'].min().date()} .. {frame['week'].max().date()}), "
              f"keeping the {keep} release")
        frames.append(frame[["week", "region", "epiweek", "wili", "ili"]])

    suffix = "_first_release" if args.first_release else ""
    out = args.out or (paths.DATA_DIR / "FluView" / f"fluview_regional_weekly{suffix}.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    combined = pd.concat(frames, ignore_index=True).sort_values(["region", "week"])
    combined["release"] = keep
    combined.to_csv(out, index=False)
    print(f"\nOutputs: {paths.display(out, paths.ROOT)}")


if __name__ == "__main__":
    main()
