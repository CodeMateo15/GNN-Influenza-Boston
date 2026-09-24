#!/usr/bin/env python3
"""Rolling-origin backtest: the same model re-fitted on one season after another.

Why this exists. Every number in `docs/METHODS.md` comes from a single test
season, 2025-06-01 to 2026-05-03. That is enough to rank models on one year and
not enough to claim a margin, because the per-seed spread of macro Corr at four
weeks ahead is about 0.05 -- so a one-season, one-seed result cannot be told
apart from a favourable draw. This script re-runs an arm with the test window
slid back a year at a time and reports the spread across seasons.

Two constraints make the numbers mean something, and both are enforced here:

1. **`val_mode="pre_test"` is mandatory.** `Window`'s default "tail" mode takes
   validation from the last slice of all non-test origins, which for a
   non-terminal window sits AFTER the test period; the purge then empties it.
   Five of the seven candidate seasons raise outright, and 2024-25 silently
   yields six validation origins while discarding 49 post-test ones. See the
   comment on `Window.val_mode`.

2. **The variant is held fixed across seasons and is not `post_covid`.** Only
   `full` reaches back far enough to construct a 2021-22 fold. That matters
   because `full` measures WORSE than `post_covid` on the shipped season -- it
   spends 40% of its training origins on the near-zero-flu COVID trough. So the
   backtest is a consistency check across seasons, not a replacement for the
   headline number, and the two must never be averaged together.

    python Code/run_backtest.py --experiment gnn_st --seasons 2022,2023,2024,2025
    python Code/run_backtest.py --experiment gnn_st --horizons 1,2,4 --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.cities import get as get_city  # noqa: E402
from influenza.cli import add_city_arg  # noqa: E402
from influenza.config import EXPERIMENTS  # noqa: E402

# 2019-20 has only ~49 training origins and 2020-21 is the COVID null season, in
# which every model scores near zero because there is no epidemic to forecast.
# Both are still runnable and are printed; they are excluded from the headline
# mean, and saying why is the point of reporting them at all.
DEFAULT_SEASONS = (2022, 2023, 2024, 2025)
EXCLUDED_FROM_MEAN = (2019, 2020)
DEFAULT_HORIZONS = (1, 2, 4)


def season_label(year: int) -> str:
    return f"{year}_{str(year + 1)[2:]}"


def season_window(year: int, city=None) -> tuple[str, str]:
    """Test targets spanning one influenza season.

    June through May for the two US cities, December through November for
    Buenos Aires -- see City.backtest_window, which derives the fold from the
    city's own flu season so a Southern-Hemisphere fold is not cut through the
    middle of its epidemic.
    """
    from influenza.cities import get as _get
    return (city or _get("boston")).backtest_window(year)


def build_jobs(experiment: str, seasons: tuple[int, ...], horizons: tuple[int, ...],
               variant: str, city=None) -> list[dict]:
    jobs = []
    for year in seasons:
        start, end = season_window(year, city)
        for horizon in horizons:
            jobs.append({
                "season": season_label(year),
                "year": year,
                "horizon": horizon,
                "test_start": start,
                "test_end": end,
                "variant": variant,
            })
    return jobs


def command_for(job: dict, experiment: str, script: str,
                city: str = "boston") -> list[str]:
    root = (paths.backtest_dir(job["season"], paths.city_root(city))
            / f"horizon_{job['horizon']:02d}")
    return [
        sys.executable, str(Path(__file__).resolve().parent / script),
        "--experiment", experiment,
        "--city", city,
        "--variant", job["variant"],
        "--horizons", str(job["horizon"]),
        "--test-start", job["test_start"],
        "--test-end", job["test_end"],
        "--val-mode", "pre_test",
        "--output-dir", str(root),
        "--checkpoint-dir", str(paths.city_root(city, paths.CHECKPOINT_DIR)
                                / "backtest" / job["season"]),
        "--no-carbon",
    ]


def collect(experiment: str, jobs: list[dict], variant: str,
            city: str = "boston") -> pd.DataFrame:
    rows = []
    for job in jobs:
        metrics = (paths.backtest_dir(job["season"], paths.city_root(city))
                   / f"horizon_{job['horizon']:02d}"
                   / experiment / variant / "metrics.csv")
        if not metrics.exists():
            continue
        frame = pd.read_csv(metrics)
        frame = frame[frame["segment"].eq("overall") & frame["scope"].isin(["macro", "pooled"])]
        for _, row in frame.iterrows():
            rows.append({
                "season": job["season"], "year": job["year"],
                "horizon": job["horizon"], "scope": row["scope"],
                "Corr": row["Corr"], "RMSE": row["RMSE"], "n_obs": row["n_obs"],
            })
    return pd.DataFrame(rows)


def report(table: pd.DataFrame) -> str:
    if table.empty:
        return "No metrics found. Run without --collect-only first."
    lines = ["# Rolling-origin backtest", ""]
    lines.append("Test targets span June-May. `variant=full` throughout, which is "
                 "required to construct the earliest folds and is NOT the variant "
                 "the headline numbers use -- do not average the two.")
    lines.append("")
    for scope in ("macro", "pooled"):
        subset = table[table["scope"].eq(scope)]
        if subset.empty:
            continue
        pivot = subset.pivot_table(index="season", columns="horizon", values="Corr")
        lines.append(f"## Corr, scope={scope}")
        lines.append("")
        lines.append(pivot.round(3).to_markdown())
        lines.append("")
        kept = subset[~subset["year"].isin(EXCLUDED_FROM_MEAN)]
        summary = kept.groupby("horizon")["Corr"].agg(["mean", "min", "max", "count"])
        lines.append(f"Across seasons excluding {list(EXCLUDED_FROM_MEAN)} "
                     "(too few training origins, and the COVID null season):")
        lines.append("")
        lines.append(summary.round(3).to_markdown())
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--experiment", default="gnn_st")
    parser.add_argument("--script", default="run_gnn.py")
    parser.add_argument("--variant", default="full",
                        help="Held fixed across seasons. Only 'full' reaches the "
                             "earliest folds; see the module docstring.")
    parser.add_argument("--seasons", default=",".join(str(s) for s in DEFAULT_SEASONS),
                        help="Start years of each June-May test season.")
    parser.add_argument("--horizons", default=",".join(str(h) for h in DEFAULT_HORIZONS))
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the commands and the split geometry, run nothing.")
    parser.add_argument("--collect-only", action="store_true",
                        help="Skip training, just re-read metrics.csv and report.")
    args = parser.parse_args()

    city = get_city(args.city)
    if args.variant not in city.variants:
        raise SystemExit(f"--variant {args.variant} is not available for {city.label}. "
                         f"{city.label} supports: {', '.join(city.variants)}.")
    if args.experiment not in EXPERIMENTS:
        raise SystemExit(f"Unknown experiment {args.experiment!r}. "
                         f"Available: {', '.join(sorted(EXPERIMENTS))}")

    seasons = tuple(int(s) for s in args.seasons.split(","))
    horizons = tuple(int(h) for h in args.horizons.split(","))
    jobs = build_jobs(args.experiment, seasons, horizons, args.variant, city)

    if not args.collect_only:
        for i, job in enumerate(jobs, 1):
            command = command_for(job, args.experiment, args.script, city.name)
            label = f"[{i}/{len(jobs)}] {job['season']} h={job['horizon']}"
            if args.dry_run:
                print(f"{label}\n  {' '.join(command)}")
                continue
            print(f"\n{'=' * 72}\n{label}\n{'=' * 72}", flush=True)
            completed = subprocess.run(command)
            if completed.returncode != 0:
                print(f"  FAILED ({completed.returncode}); continuing.", flush=True)
        if args.dry_run:
            return

    table = collect(args.experiment, jobs, args.variant, city.name)
    out = paths.city_root(city.name) / "_backtest"
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / f"{args.experiment}_backtest.csv", index=False)
    text = report(table)
    (out / f"{args.experiment}_backtest.md").write_text(text)
    print("\n" + text)
    print(f"\nWrote {paths.display(out)}/{args.experiment}_backtest.{{csv,md}}")


if __name__ == "__main__":
    main()
