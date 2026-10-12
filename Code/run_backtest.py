#!/usr/bin/env python3
"""Rolling-origin backtest: every model re-fitted on one season after another.

Why this exists. Every number in `docs/METHODS.md` comes from a single test
season, 2025-06-01 to 2026-05-03, and that season was also the one the design
was chosen on: the ablations that set the defaults, the V2 training settings
and the blend target were all measured on it. So it can rank models on one
year but it cannot certify a margin. This re-runs a FROZEN set of arms -- the
graph model and every baseline, with no further changes -- with the test window
slid back a year at a time, and reports each season separately and together.

Folds 2022-23, 2023-24 and 2024-25 were never used to choose anything and are
the evidence. 2025-26 is run too, on the same variant, and reported as the
disclosed development season -- never pooled into the headline mean.

Three constraints make the numbers mean something, and all are enforced here:

1. **`val_mode="pre_test"` is mandatory.** `Window`'s default "tail" mode takes
   validation from the last slice of all non-test origins, which for a
   non-terminal window sits AFTER the test period; the purge then empties it.
   See the comment on `Window.val_mode`.

2. **The variant is held fixed across seasons and models, and is `full`.** Only
   `full` reaches back far enough to train the 2022-23 fold. `full` measures
   worse than `post_covid` on the shipped season, so a backtest number and a
   leaderboard number must never be averaged together.

3. **Every arm is frozen before the first fold is scored.** FROZEN_ARMS below is
   the list; changing it after seeing a fold turns the backtest back into a
   development set. Record the commit it was run from.

    python Code/run_backtest.py --write-tasks Code/sweep/tasks_backtest_all.jsonl
    python Code/run_backtest.py --collect-only
    python Code/run_backtest.py --arms persistence,climatology --horizons 2   # local, cheap

Heavy arms (anything neural, multi-seed) run on Explorer through the written
task list, not here -- see CLAUDE.md section 2.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.cities import get as get_city  # noqa: E402
from influenza.cli import add_city_arg  # noqa: E402
from sweep import enumerate_tasks  # noqa: E402

# Per city, because the histories differ. Boston's `full` series reaches 2017, so
# three unseen folds fit before the development season. Columbus and Buenos
# Aires only have `post_covid` (from 2022-07): a Columbus 2023-24 fold would
# train on under a year, and Buenos Aires's feed ends 2025-11, so each has ONE
# unseen fold. That is a real limit of the multi-city evidence, stated here
# rather than papered over with folds too short to train.
#
# Chicago's feed starts 2019-09-29, so like Boston it runs on `full`: under
# `post_covid` the 2022-23 fold would have no training weeks at all. Its early
# history is thin and odd (half a pre-COVID season, the COVID years, and a
# 19-week city-wide gap in 2020 that stays NaN), and that is stated rather than
# hidden by dropping the folds.
DEFAULT_SEASONS = {"boston": (2022, 2023, 2024, 2025),
                   "columbus": (2024, 2025),
                   "buenos_aires": (2023, 2024),
                   "chicago": (2022, 2023, 2024, 2025)}
# The season each city's design was chosen on (its committed leaderboard
# window). Run and printed, never in the headline mean. Empty for Chicago:
# nothing was tuned on it, so every fold is evidence.
DEVELOPMENT_SEASONS = {"boston": (2025,), "columbus": (2025,), "buenos_aires": (2024,),
                       "chicago": ()}
DEFAULT_VARIANT = {"boston": "full", "columbus": "post_covid", "buenos_aires": "post_covid",
                   "chicago": "full"}
# Boston with polygon-derived edges (the map test) shares Boston's history.
for _derived in ("boston_geo_tract", "boston_geo_land"):
    DEFAULT_SEASONS[_derived] = DEFAULT_SEASONS["boston"]
    DEVELOPMENT_SEASONS[_derived] = DEVELOPMENT_SEASONS["boston"]
    DEFAULT_VARIANT[_derived] = DEFAULT_VARIANT["boston"]
DEFAULT_HORIZONS = (1, 2, 4)

# The comparison set, frozen. Order is the order rows print in.
FROZEN_ARMS = (
    "gnn_st",            # the proposed model
    "gnn_st_nograph",    # same pipeline, graph removed: isolates the graph
    "lstm_parity",       # 16-week window, blend target, 10 seeds
    "xgboost_parity",    # same 46 columns, blend target, 10 seeds
    "blend_baseline",    # gnn_st's prior with the network switched off
    "climatology",
    "sarima",
    "persistence",
    "seasonal_naive",
    "lstm",              # as committed: 8 weeks, level target, 1 seed
    "xgboost",           # as committed: climatology target, 1 seed
    "arima",
    "gat_parity",
)
# Added after the first backtest, from the review that asked for equal tuning
# and external baselines. `<arm>_tuned` rows come from tune.py (per-fold
# validation-only search, K configurations each, then ten seeds); the others
# are ordinary sweep arms.
ADDED_ARMS = ("lstm_s10", "flusight_baseline", "gnn_st_tuned", "gnn_st_nograph_tuned",
              "lstm_tuned", "xgboost_tuned", "colagnn_tuned", "gat_tuned", "dualtopo_tuned",
              # The portability tests: borders-only graph, and cross-city transfer.
              "gnn_st_geofixed", "gnn_st_noadapt",
              "transfer_zeroshot_from_boston", "transfer_finetune_from_boston",
              "transfer_zeroshot_from_columbus", "transfer_finetune_from_columbus",
              "transfer_zeroshot_from_chicago", "transfer_finetune_from_chicago")
# Every arm the report reads. Tasks are only built from --arms.
REPORTED_ARMS = FROZEN_ARMS + ADDED_ARMS

# One run of run_climatology.py writes both of these.
WRITTEN_BY = {"blend_baseline": "climatology"}
# Luo et al. ran their comparison models one week ahead only. Scoring them at 2
# and 4 weeks would test them outside the setting they were designed for.
ONE_WEEK_ONLY = {"gat_parity", "gat", "dualtopo", "gat_tuned", "dualtopo_tuned"}


def season_label(year: int) -> str:
    return f"{year}_{str(year + 1)[2:]}"


def build_tasks(city: str, arms, seasons, horizons, variant: str):
    runnable = tuple(dict.fromkeys(WRITTEN_BY.get(a, a) for a in arms))
    tasks = enumerate_tasks(cities=(city,), arms=runnable, horizons=tuple(horizons),
                            variant=variant, seasons=tuple(seasons))
    return [t for t in tasks if t.arm not in ONE_WEEK_ONLY or t.horizon == 1]


def fold_root(city: str, season: str, horizon: int) -> Path:
    return paths.backtest_dir(season, paths.city_root(city)) / f"horizon_{horizon:02d}"


def collect(city: str, arms, seasons, horizons, variant: str) -> pd.DataFrame:
    """One row per (arm, season, horizon): pooled MAE/RMSE, macro Corr, WIS if written."""
    from influenza import scoring

    rows = []
    for year in seasons:
        season = season_label(year)
        for horizon in horizons:
            root = fold_root(city, season, horizon)
            for arm in arms:
                path = root / arm / variant / "predictions.csv"
                if not path.exists():
                    continue
                frame = pd.read_csv(path, parse_dates=["target_date"])
                frame = frame[np.isfinite(frame["actual"]) & np.isfinite(frame["predicted"])]
                error = frame["predicted"] - frame["actual"]
                row = {"arm": arm, "season": season, "year": year, "horizon": horizon,
                       "n_cells": len(frame), "MAE": float(error.abs().mean()),
                       "RMSE": float(np.sqrt((error ** 2).mean()))}
                pair = frame.rename(columns={"predicted": "predicted_a"})
                row["Corr"] = scoring.macro_corr(pair, "a")
                if set(scoring.QUANTILE_COLUMNS).issubset(frame.columns):
                    row["WIS"] = float(np.mean(scoring.wis_from_quantiles(
                        frame["actual"], frame[list(scoring.QUANTILE_COLUMNS)])))
                rows.append(row)
    return pd.DataFrame(rows)


def report(table: pd.DataFrame, city: str, variant: str, reference: str = "gnn_st") -> str:
    if table.empty:
        return "No backtest results found. Run the task list first."
    development = DEVELOPMENT_SEASONS.get(city, ())
    evidence = table[~table["year"].isin(development)]
    lines = [
        "# Rolling-origin backtest",
        "",
        "Does the ranking hold on seasons the design never saw? Each fold trains on",
        f"everything before its test season (variant `{variant}`, validation taken just",
        "before the test window) and forecasts one full season. Folds "
        + ", ".join(season_label(y) for y in sorted(set(evidence["year"])))
        + " are the evidence"
        + ("; " + ", ".join(season_label(y) for y in development)
           + " is the season the design was chosen on and is shown for reference only."
           if development else
           "; no season of this city was used to choose anything, so none is held out."),
        "",
        ("MAE and WIS are in ILI activity levels, 1-10 (lower is better); Corr is the mean over"
         if city == "chicago" else
         "MAE and WIS are in rate per 100,000 (lower is better); Corr is the mean over"),
        "neighborhoods of the week-to-week correlation (higher is better).",
        "",
    ]
    metrics = [m for m in ("MAE", "WIS", "RMSE", "Corr") if m in table and table[m].notna().any()]
    for horizon, part in table.groupby("horizon"):
        lines += [f"## Horizon {horizon}", ""]
        for metric in metrics:
            pivot = part.pivot_table(index="arm", columns="season", values=metric)
            kept = evidence[evidence["horizon"].eq(horizon)]
            pivot["evidence mean"] = kept.pivot_table(index="arm", values=metric)[metric]
            ascending = metric != "Corr"
            pivot = pivot.sort_values("evidence mean", ascending=ascending)
            lines += [f"### {metric}", "", pivot.round(3).to_markdown(), ""]
        if reference in set(part["arm"]):
            wins = []
            for arm in sorted(set(part["arm"]) - {reference}):
                a = evidence[evidence["horizon"].eq(horizon) & evidence["arm"].eq(reference)]
                b = evidence[evidence["horizon"].eq(horizon) & evidence["arm"].eq(arm)]
                merged = a.merge(b, on="season", suffixes=("_ref", "_other"))
                if merged.empty:
                    continue
                won = int((merged["MAE_ref"] < merged["MAE_other"]).sum())
                wins.append(f"| {arm} | {won} of {len(merged)} |")
            if wins:
                lines += [f"Evidence seasons in which `{reference}` has the lower MAE:", "",
                          "| other arm | seasons won |", "| --- | --- |", *wins, ""]
    lines += [
        "Per-fold significance (block bootstrap and Diebold-Mariano) is in each fold's",
        "`_comparison/significance.md`, written by compare_significance.py.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--arms", default=",".join(FROZEN_ARMS))
    parser.add_argument("--variant", default=None,
                        help="Held fixed across seasons and arms. Default 'full' for Boston "
                             "(only it reaches the earliest folds) and 'post_covid' for the "
                             "cities that have nothing else.")
    parser.add_argument("--seasons", default=None,
                        help="Start years of each test season (default per city).")
    parser.add_argument("--horizons", default=",".join(str(h) for h in DEFAULT_HORIZONS))
    parser.add_argument("--write-tasks", type=Path, default=None,
                        help="Write the task list for Code/sweep/array.sbatch and stop.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the commands, run nothing.")
    parser.add_argument("--collect-only", action="store_true",
                        help="Skip training, just re-read predictions and report.")
    parser.add_argument("--no-carbon", action="store_true")
    args = parser.parse_args()

    city = get_city(args.city)
    args.variant = args.variant or DEFAULT_VARIANT[city.name]
    args.seasons = args.seasons or ",".join(str(s) for s in DEFAULT_SEASONS[city.name])
    if args.variant not in city.variants:
        raise SystemExit(f"--variant {args.variant} is not available for {city.label}. "
                         f"{city.label} supports: {', '.join(city.variants)}.")
    arms = tuple(a.strip() for a in args.arms.split(",") if a.strip())
    seasons = tuple(int(s) for s in args.seasons.split(","))
    horizons = tuple(int(h) for h in args.horizons.split(","))
    tasks = build_tasks(city.name, arms, seasons, horizons, args.variant)

    if args.write_tasks:
        args.write_tasks.parent.mkdir(parents=True, exist_ok=True)
        args.write_tasks.write_text("\n".join(json.dumps(t.to_json()) for t in tasks) + "\n")
        print(f"{len(tasks)} tasks -> {args.write_tasks}")
        print(f"Submit: sbatch --export=ALL,CHUNK=1,TASKS={args.write_tasks} "
              f"--array=0-{len(tasks) - 1}%50 Code/sweep/array.sbatch")
        return

    if not args.collect_only:
        # The run_progress.py contract, in tasks.
        print(f"Budget: {len(tasks)} epochs x 1 seeds", flush=True)
        print("--- seed 0 (1/1) ---", flush=True)
        for i, task in enumerate(tasks, 1):
            command = task.command() + (["--no-carbon"] if args.no_carbon else [])
            if args.dry_run:
                print(f"[{i}/{len(tasks)}] {task.task_id}\n  {' '.join(command)}")
                continue
            completed = subprocess.run(command, stdout=subprocess.DEVNULL)
            status = "ok" if completed.returncode == 0 else f"FAILED ({completed.returncode})"
            print(f"Epoch {i} | {task.task_id} {status}", flush=True)
        if args.dry_run:
            return

    table = collect(city.name, REPORTED_ARMS, seasons, horizons, args.variant)
    out = paths.city_root(city.name) / "_backtest"
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "backtest.csv", index=False)
    text = report(table, city.name, args.variant)
    (out / "backtest.md").write_text(text)
    print("\n" + text)
    print(f"Outputs: {paths.display(out / 'backtest.md')}", flush=True)


if __name__ == "__main__":
    main()
