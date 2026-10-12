#!/usr/bin/env python3
"""Give every learned model the same tuning budget, chosen on validation only.

Why this exists. `gnn_st`'s settings came out of ~25 ablation arms and a sweep;
every baseline ran at one fixed setting. A reviewer can then say the graph model
won because it was tuned and the baselines were not. This removes that asymmetry:

  * every learned model gets K configurations -- configuration 0 is its current
    default, the other K-1 are drawn at random from a search space of
    comparable breadth (five to seven settings, two to four values each);
  * each configuration is trained ONCE (one seed) on every unseen backtest fold;
  * the configuration with the lowest validation MAE on that fold -- weeks
    before that fold's test season, never the test season itself -- is chosen;
  * the chosen configuration is re-run on that fold with the full ten-seed
    ensemble, as `<arm>_tuned`, and scored like everything else.

Tuning is nested per fold, so no fold's test weeks influence which setting is
used on it. The development season is not tuned: it is not evidence.

    python Code/tune.py list    --out Code/sweep/tasks_tune.jsonl       # stage 1
    python Code/tune.py select                                          # read validation
    python Code/tune.py finals  --out Code/sweep/tasks_tuned_final.jsonl  # stage 2

Stage 1 and 2 run on Explorer through Code/sweep/array.sbatch.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.cities import get as get_city  # noqa: E402
from run_backtest import (DEFAULT_SEASONS, DEFAULT_VARIANT, DEVELOPMENT_SEASONS,  # noqa: E402
                          ONE_WEEK_ONLY, season_label)
from sweep import Task  # noqa: E402

K = 12
HORIZONS = (1, 2, 4)
CITIES = ("boston", "columbus", "buenos_aires", "chicago")
TUNING_ROOT = paths.RESULTS_DIR / "_tuning"
SELECTION_FILE = Path(__file__).resolve().parent / "sweep" / "tuned_configs.json"

# arm -> (script, fixed flags, search space {flag: values}). Every space has a
# learning rate, a regulariser, a capacity setting and a training-length or
# history setting; the tree model gets its own equivalents.
_GNN_SPACE = {"--lr": [1e-3, 3e-3, 1e-2], "--weight-decay": [3e-4, 1e-3, 3e-3, 1e-2],
              "--dropout": [0.1, 0.25, 0.4], "--channels": [16, 24, 32],
              "--epochs": [80, 120, 200]}
SEARCH = {
    "gnn_st": ("run_gnn.py", [], _GNN_SPACE),
    "gnn_st_nograph": ("run_gnn.py", [], _GNN_SPACE),
    "lstm": ("run_lstm.py", [],
             {"--lr": [3e-4, 1e-3, 3e-3], "--weight-decay": [1e-5, 1e-4, 1e-3],
              "--dropout": [0.0, 0.1, 0.25], "--hidden-size": [32, 64, 128],
              "--lookback": [8, 16, 26], "--epochs": [80, 120, 200],
              "--target": ["level", "blend"]}),
    "xgboost": ("run_xgboost.py", [],
                {"--learning-rate": [0.01, 0.03, 0.1], "--max-depth": [2, 3, 4, 6],
                 "--min-child-weight": [1, 4, 8], "--subsample": [0.6, 0.8, 1.0],
                 "--colsample-bytree": [0.6, 0.8, 1.0], "--reg-lambda": [0.5, 2.0, 8.0],
                 "--target": ["climatology", "level", "blend"]}),
    "colagnn": ("run_colagnn.py", [],
                {"--lr": [3e-4, 1e-3, 3e-3], "--weight-decay": [0.0, 5e-4, 5e-3],
                 "--dropout": [0.1, 0.2, 0.4], "--hidden": [16, 32, 64],
                 "--lookback": [12, 20, 26], "--epochs": [100, 150, 200]}),
    "gat": ("run_gat.py", ["--batched"],
            {"--lr": [1e-3, 3e-3, 1e-2], "--weight-decay": [1e-5, 1e-4, 1e-3],
             "--dropout": [0.1, 0.2, 0.4], "--hidden": [32, 64], "--heads": [4, 8],
             "--epochs": [100, 200]}),
    "dualtopo": ("run_dualtopo.py", [],
                 {"--lr": [1e-3, 3e-3, 1e-2], "--weight-decay": [1e-5, 1e-4, 1e-3],
                  "--epochs": [100, 200], "--fusion": ["concat", "mean", "max"]}),
}


def configurations(arm: str, k: int = K) -> list[list[str]]:
    """K flag lists for one arm: [] (the default) then K-1 random draws, fixed seed."""
    space = SEARCH[arm][2]
    rng = np.random.default_rng(_stable_seed(arm))
    configs, seen = [[]], {()}
    while len(configs) < k:
        flags = []
        for flag, values in space.items():
            flags += [flag, str(values[rng.integers(len(values))])]
        key = tuple(flags)
        if key not in seen:
            seen.add(key)
            configs.append(flags)
    return configs


def _stable_seed(arm: str) -> int:
    """A seed that does not change between Python processes (hash() does)."""
    return int.from_bytes(arm.encode(), "little") % (2 ** 32)


def folds(city: str) -> list[int]:
    return [y for y in DEFAULT_SEASONS[city] if y not in DEVELOPMENT_SEASONS[city]]


def horizons_for(arm: str) -> tuple[int, ...]:
    return (1,) if arm in ONE_WEEK_ONLY else HORIZONS


def tuning_tasks(arms, cities) -> list[Task]:
    tasks = []
    for city in cities:
        variant = DEFAULT_VARIANT[city]
        for year in folds(city):
            start, end = get_city(city).backtest_window(year)
            season = season_label(year)
            for arm in arms:
                script, fixed, _ = SEARCH[arm]
                for horizon in horizons_for(arm):
                    root = (paths.city_root(city, TUNING_ROOT) / f"backtest_{season}"
                            / f"horizon_{horizon:02d}")
                    for index, flags in enumerate(configurations(arm)):
                        tasks.append(Task(
                            city=city, arm=arm, script=script, variant=variant,
                            horizon=horizon, season=season, test_start=start, test_end=end,
                            out_root=str(root.relative_to(paths.ROOT)),
                            name=f"{arm}__cfg{index:02d}",
                            extra=tuple(fixed + flags + ["--n-seeds", "1"])))
    return tasks


def validation_mae(path: Path, keys: pd.Index | None) -> float:
    frame = pd.read_csv(path, parse_dates=["target_date"])
    frame = frame[np.isfinite(frame["actual"]) & np.isfinite(frame["predicted"])]
    if keys is not None:
        frame = frame.set_index(["target_date", "neighborhood"]).loc[keys].reset_index()
    return float((frame["predicted"] - frame["actual"]).abs().mean())


def select(arms, cities) -> dict:
    """Lowest validation MAE per (city, fold, horizon, arm), on shared validation cells."""
    chosen: dict = {}
    for city in cities:
        variant = DEFAULT_VARIANT[city]
        for year in folds(city):
            season = season_label(year)
            for arm in arms:
                for horizon in horizons_for(arm):
                    root = (paths.city_root(city, TUNING_ROOT) / f"backtest_{season}"
                            / f"horizon_{horizon:02d}")
                    configs = configurations(arm)
                    files = {i: root / f"{arm}__cfg{i:02d}" / variant / "predictions_val.csv"
                             for i in range(len(configs))}
                    present = {i: f for i, f in files.items() if f.exists()}
                    if not present:
                        continue
                    # Configurations with different lookbacks can differ by a
                    # validation week at the edge; compare on the cells all share.
                    keys = None
                    for f in present.values():
                        idx = pd.read_csv(f, parse_dates=["target_date"]).dropna(
                            subset=["actual"]).set_index(["target_date", "neighborhood"]).index
                        keys = idx if keys is None else keys.intersection(idx)
                    scores = {i: validation_mae(f, keys) for i, f in present.items()}
                    best = min(scores, key=scores.get)
                    chosen.setdefault(city, {}).setdefault(season, {}).setdefault(
                        str(horizon), {})[arm] = {
                        "config": best, "flags": configs[best],
                        "val_mae": scores[best], "default_val_mae": scores.get(0),
                        "n_configs_scored": len(scores), "n_configs": len(configs),
                    }
    return chosen


def final_tasks(chosen: dict) -> list[Task]:
    tasks = []
    for city, seasons in chosen.items():
        variant = DEFAULT_VARIANT[city]
        for season, horizons in seasons.items():
            year = int(season.split("_")[0])
            start, end = get_city(city).backtest_window(year)
            for horizon, arms in horizons.items():
                for arm, pick in arms.items():
                    script, fixed, _ = SEARCH[arm]
                    tasks.append(Task(
                        city=city, arm=arm, script=script, variant=variant,
                        horizon=int(horizon), season=season, test_start=start, test_end=end,
                        name=f"{arm}_tuned",
                        extra=tuple(fixed + pick["flags"] + ["--n-seeds", "10"])))
    return tasks


def write(tasks: list[Task], out: Path, chunk: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(t.to_json()) for t in tasks) + "\n")
    elements = -(-len(tasks) // chunk)
    print(f"{len(tasks)} tasks -> {out}")
    print(f"Submit: sbatch --export=ALL,CHUNK={chunk},TASKS={paths.display(out, paths.ROOT)} "
          f"--array=0-{elements - 1}%50 Code/sweep/array.sbatch")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("list", "select", "finals"))
    parser.add_argument("--arms", default=",".join(SEARCH))
    parser.add_argument("--cities", default=",".join(CITIES))
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--chunk", type=int, default=4)
    args = parser.parse_args()
    arms = tuple(a for a in args.arms.split(",") if a)
    cities = tuple(c for c in args.cities.split(",") if c)
    unknown = [a for a in arms if a not in SEARCH]
    if unknown:
        raise SystemExit(f"No search space for {unknown}. Known: {', '.join(SEARCH)}")

    if args.mode == "list":
        write(tuning_tasks(arms, cities), args.out or Path("Code/sweep/tasks_tune.jsonl"),
              args.chunk)
    elif args.mode == "select":
        chosen = select(arms, cities)
        SELECTION_FILE.write_text(json.dumps(chosen, indent=2))
        n = sum(len(a) for s in chosen.values() for h in s.values() for a in h.values())
        print(f"{n} selections -> {paths.display(SELECTION_FILE)}")
        for city, seasons in chosen.items():
            for season, horizons in seasons.items():
                for horizon, picks in horizons.items():
                    for arm, pick in picks.items():
                        print(f"  {city:12s} {season} h={horizon} {arm:15s} cfg{pick['config']:02d} "
                              f"val MAE {pick['val_mae']:.3f} (default "
                              f"{pick['default_val_mae'] if pick['default_val_mae'] is None else round(pick['default_val_mae'], 3)}) "
                              f"[{pick['n_configs_scored']}/{pick['n_configs']} scored]")
    else:
        chosen = json.loads(SELECTION_FILE.read_text())
        write(final_tasks(chosen), args.out or Path("Code/sweep/tasks_tuned_final.jsonl"),
              args.chunk)


if __name__ == "__main__":
    main()
