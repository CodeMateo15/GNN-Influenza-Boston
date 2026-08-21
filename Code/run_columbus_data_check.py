"""Verify the Columbus data layer before any model is trained on it.

Stage 1 of the two-city work is "data first, models after", and this is the
gate. It asserts the properties the loaders promise and prints the coverage
report that belongs next to Boston's in the docs. Everything here is cheap:
no torch, no graph, no training.

    python Code/run_columbus_data_check.py
    python Code/run_columbus_data_check.py --strict   # fail on a blocked check

Checks that need the ACS denominator (rates, static demographics) are reported
as SKIP rather than failing, so this is runnable before a Census API key exists.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths
from influenza.constants import POST_COVID_START, TEST_END, TEST_START, WEATHER_COLS
from influenza.loaders import columbus as cbus
from influenza.loaders import columbus_crosswalk as crosswalk

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


class Checks:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def record(self, status: str, name: str, detail: str = "") -> None:
        self.rows.append((status, name, detail))
        print(f"  [{status}] {name}" + (f" -- {detail}" if detail else ""))

    def check(self, name: str, condition: bool, detail: str = "") -> bool:
        self.record(PASS if condition else FAIL, name, detail)
        return condition

    def counts(self, status: str) -> int:
        return sum(1 for s, _, _ in self.rows if s == status)


def check_crosswalk(checks: Checks) -> list[str]:
    print("\nCrosswalk")
    areas = crosswalk.area_names()
    anchors = crosswalk.load_anchor_zips()
    mapping = crosswalk.zip_to_area()

    checks.check("17 areas", len(areas) == 17, f"{len(areas)} found")
    checks.check("area names are unique and sorted", areas == sorted(set(areas)))
    checks.check("7 unassigned fringe ZIPs become anchors", len(anchors) == 7, str(anchors))
    checks.check("every mapped ZIP resolves to a named area",
                 set(mapping.values()) == set(areas))
    checks.check("anchors and mapped ZIPs are disjoint",
                 not (set(anchors) & set(mapping)))
    return areas


def check_week_grid(checks: Checks, counts: pd.DataFrame) -> None:
    print("\nWeek grid")
    gaps = np.diff(counts.index.values).astype("timedelta64[D]").astype(int)
    checks.check("every week is exactly 7 days after the last",
                 set(gaps.tolist()) == {7}, f"gaps seen: {sorted(set(gaps.tolist()))}")
    checks.check("index starts on a Sunday",
                 bool((counts.index.dayofweek == 6).all()))
    checks.check("no NaN in the target panel -- Columbus zeros are real",
                 int(counts.isna().sum().sum()) == 0)
    checks.check("evaluation window is fully covered",
                 counts.index.min() < TEST_START and counts.index.max() > TEST_END,
                 f"{counts.index.min().date()} -> {counts.index.max().date()}")

    # Columbus starts 2022-01, so only the post_covid variant has any data.
    pre = counts.loc[counts.index < POST_COVID_START]
    checks.record(PASS, "no pre-COVID history, as expected",
                  f"{len(pre)} weeks before {POST_COVID_START.date()} "
                  f"-- 'full' and 'exclude_covid' variants are Boston-only")


def check_row_accounting(checks: Checks, counts: pd.DataFrame) -> None:
    print("\nRow accounting")
    raw = cbus._read_ili()
    total = len(raw)
    anchors = set(crosswalk.load_anchor_zips())
    unmapped = sorted(set(raw.loc[raw["area"].isna(), "zip"]) - anchors)

    in_anchor = int(raw["zip"].isin(anchors).sum())
    in_unmapped = int(raw["zip"].isin(unmapped).sum())
    kept = int(counts.to_numpy().sum())
    edge = int(raw["area"].notna().sum()) - kept

    checks.check("unmapped ZIPs are exactly the known set",
                 set(unmapped) == set(crosswalk.KNOWN_UNMAPPED_ZIPS), str(unmapped))
    checks.check("accounting closes exactly",
                 in_anchor + in_unmapped + edge + kept == total,
                 f"{in_anchor} anchor + {in_unmapped} unmapped + {edge} partial-week "
                 f"+ {kept} kept = {total}")
    checks.record(PASS, "retention", f"{kept:,}/{total:,} ILI visits ({kept/total*100:.2f}%)")


def check_mmwr(checks: Checks, counts: pd.DataFrame) -> None:
    print("\nMMWR calendar")
    lengths = {y: cbus.mmwr_weeks_in_year(y) for y in range(2020, 2028)}
    checks.check("2020 and 2025 are 53-week years, the rest 52",
                 [y for y, n in lengths.items() if n == 53] == [2020, 2025],
                 ", ".join(f"{y}={n}" for y, n in lengths.items()))
    checks.check("MMWR 2025 week 1 ends 2025-01-04 (CDC anchor)",
                 cbus.mmwr_week_start(2025, 1) + pd.Timedelta(days=6)
                 == pd.Timestamp("2025-01-04"))
    checks.check("MMWR weeks tile with no gap across the 2025/26 boundary",
                 cbus.mmwr_week_start(2025, 53) + pd.Timedelta(days=7)
                 == cbus.mmwr_week_start(2026, 1))

    iah = cbus.load_hospitalizations(counts.index)
    checks.check("hospitalisations land on the ILI Sunday grid",
                 iah.index.equals(counts.index))
    checks.record(PASS, "2025-W53 retained",
                  f"week of {cbus.mmwr_week_start(2025, 53).date()}, "
                  f"{int(iah.loc[cbus.mmwr_week_start(2025, 53)].sum())} hospitalisations")


def check_covariates(checks: Checks, counts: pd.DataFrame) -> None:
    print("\nCovariates")
    covid = cbus.load_covid_counts(counts.index)
    window = covid.loc[(covid.index >= TEST_START) & (covid.index <= TEST_END)]
    blank = int(window.isna().all(axis=1).sum())
    checks.record(PASS, "COVID coverage gap is measured, not hidden",
                  f"{blank}/{len(window)} evaluation weeks ({blank/len(window)*100:.0f}%) "
                  f"have no COVID data; last observed "
                  f"{covid.dropna(how='all').index.max().date()}")

    if paths.COLUMBUS_WEATHER_DIR.exists():
        weather = cbus.load_weather(counts.index)
        finite = all(np.isfinite(weather[c]).all() for c in WEATHER_COLS)
        checks.check("all 6 weather columns finite for every area-week", finite)
        checks.check("weather shape matches the target panel",
                     weather["temp_mean_c"].shape == counts.shape)
    else:
        checks.record(SKIP, "weather", "run Code/scrapers/scrape_weather_columbus.py")


def check_rates(checks: Checks) -> pd.DataFrame | None:
    print("\nRates per 100,000")
    if not paths.COLUMBUS_STATIC_FILE.exists():
        checks.record(SKIP, "rates and static demographics",
                      "needs CENSUS_API_KEY; see Code/scrapers/scrape_acs_columbus.py")
        return None
    rates = cbus.load_rates()
    citywide = rates.mean(axis=1)
    checks.check("rates are non-negative and finite",
                 bool(np.isfinite(rates.to_numpy()).all()) and bool((rates >= 0).all().all()))
    checks.check("citywide mean rate is within 2x of Boston's ~21 per 100,000",
                 5 < citywide.mean() < 45, f"{citywide.mean():.1f} per 100,000")
    static, names, _ = cbus.load_static_demographics()
    checks.check("static demographics are (17, 8) in [0, 1]",
                 static.shape == (17, 8) and float(static.min()) >= 0
                 and float(static.max()) <= 1, f"shape {static.shape}")
    return rates


def coverage_table(counts: pd.DataFrame, rates: pd.DataFrame | None) -> str:
    """Per-area coverage, in the shape of data.coverage_report()."""
    frame = pd.DataFrame({
        "weeks": len(counts),
        "zero_weeks": (counts == 0).sum(),
        "pct_zero": ((counts == 0).sum() / len(counts) * 100).round(1),
        "mean_visits": counts.mean().round(1),
        "peak_visits": counts.max().astype(int),
    })
    if rates is not None:
        frame["mean_rate"] = rates.mean().round(2)
        frame["peak_rate"] = rates.max().round(1)
    return frame.sort_values("mean_visits", ascending=False).to_string()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero if any check is skipped as well as failed.")
    args = parser.parse_args()

    print("=" * 72)
    print("Columbus data check")
    print("=" * 72)

    checks = Checks()
    check_crosswalk(checks)
    counts = cbus.load_counts()
    check_week_grid(checks, counts)
    check_row_accounting(checks, counts)
    check_mmwr(checks, counts)
    check_covariates(checks, counts)
    rates = check_rates(checks)

    print(f"\nCoverage, {len(counts)} weeks "
          f"{counts.index.min().date()} -> {counts.index.max().date()}")
    print(coverage_table(counts, rates))

    failed, skipped = checks.counts(FAIL), checks.counts(SKIP)
    print(f"\n{checks.counts(PASS)} passed, {failed} failed, {skipped} skipped")
    if failed or (args.strict and skipped):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
