#!/usr/bin/env python3
"""Enumerate and run the model sweep. One source of truth for the task matrix.

`run_all_horizons.py` enumerates the matrix and executes it in the same process,
which is fine on a laptop and useless on a scheduler: a SLURM array needs to
address task N without running tasks 0..N-1. This module separates the two, so
the laptop and the cluster read the same list rather than two copies that drift
-- the same argument `windows.py` makes about its own duplicated split logic.

    python Code/sweep.py list --arms gnn_st,gnn_st_delta --horizons 1,2,4
    python Code/sweep.py list --out Code/sweep/tasks.jsonl
    python Code/sweep.py run  --tasks Code/sweep/tasks.jsonl --start 0 --count 20

Tasks are addressed by LINE INDEX in the jsonl, so the file must be regenerated
and re-synced whenever the matrix changes -- never edited by hand mid-sweep.
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.config import EXPERIMENTS  # noqa: E402

HERE = Path(__file__).resolve().parent

# Which entry point runs which model family.
SCRIPT_FOR_MODEL = {"gcn_fusion": "run_gnn.py", "stgnn": "run_gnn.py",
                    "dualtopo": "run_dualtopo.py", "gat": "run_gat.py"}
BASELINE_SCRIPTS = {
    "persistence": ("run_seasonal_naive.py", ("--season-lag", "1")),
    "seasonal_naive": ("run_seasonal_naive.py", ("--season-lag", "52")),
    "arima": ("run_arima.py", ()),
    "lstm": ("run_lstm.py", ()),
    "xgboost": ("run_xgboost.py", ()),
}


@dataclass(frozen=True)
class Task:
    city: str
    arm: str
    script: str
    variant: str
    horizon: int
    extra: tuple[str, ...] = field(default_factory=tuple)
    season: str | None = None
    test_start: str | None = None
    test_end: str | None = None
    # Set by the ablation task list, which needs its runs kept out of
    # results/horizon_*/ and its reference replicates kept apart from each
    # other. `name` is the directory run_gnn.py writes under (--name), which
    # for a replicate differs from the experiment it is built from.
    out_root: str | None = None
    name: str | None = None
    seed: int | None = None

    @property
    def task_id(self) -> str:
        parts = [self.city, self.name or self.arm, self.variant,
                 f"h{self.horizon:02d}"]
        if self.season:
            parts.append(self.season)
        return "__".join(parts)

    def to_json(self) -> dict:
        payload = {"city": self.city, "arm": self.arm, "script": self.script,
                   "variant": self.variant, "horizon": self.horizon,
                   "extra": list(self.extra), "task_id": self.task_id}
        if self.season:
            payload.update(season=self.season, test_start=self.test_start,
                           test_end=self.test_end)
        for key in ("out_root", "name", "seed"):
            if getattr(self, key) is not None:
                payload[key] = getattr(self, key)
        return payload

    @classmethod
    def from_json(cls, payload: dict) -> "Task":
        return cls(city=payload["city"], arm=payload["arm"], script=payload["script"],
                   variant=payload["variant"], horizon=payload["horizon"],
                   extra=tuple(payload.get("extra", ())),
                   season=payload.get("season"),
                   test_start=payload.get("test_start"),
                   test_end=payload.get("test_end"),
                   out_root=payload.get("out_root"),
                   name=payload.get("name"),
                   seed=payload.get("seed"))

    def output_dir(self) -> Path:
        """Where this task writes, with the city segment applied.

        `city_root` is NOT optional here. Without it a `--cities columbus` task
        wrote to results/horizon_02/<arm>/post_covid/ -- Boston's directory --
        and silently overwrote Boston's results with Columbus numbers. The only
        Columbus task list in Code/sweep/ carries a hand-set `out_root` to work
        around exactly that.
        """
        if self.out_root:
            return Path(self.out_root)
        root = paths.city_root(self.city)
        if self.season:
            return paths.backtest_dir(self.season, root) / f"horizon_{self.horizon:02d}"
        return paths.horizon_dir(self.horizon, root)

    @property
    def run_name(self) -> str:
        return self.name or self.arm

    def command(self) -> list[str]:
        out = self.output_dir()
        command = [sys.executable, "-u", str(HERE / self.script)]
        if self.arm in EXPERIMENTS:
            command += ["--experiment", self.arm]
        else:
            command += list(BASELINE_SCRIPTS[self.arm][1])
        command += ["--city", self.city, "--variant", self.variant,
                    "--horizons", str(self.horizon),
                    "--output-dir", str(out)]
        if self.name:
            command += ["--name", self.name]
        if self.seed is not None:
            command += ["--seed", str(self.seed)]
        if self.script != "run_seasonal_naive.py":
            # Same city segment as output_dir: checkpoint filenames carry no
            # city, so two cities sharing one directory overwrite each other.
            ck_base = paths.city_root(self.city, paths.CHECKPOINT_DIR)
            root = (Path(self.out_root.replace("/results/", "/checkpoints/"))
                    if self.out_root else
                    ck_base / (f"backtest_{self.season}" if self.season
                               else f"horizon_{self.horizon:02d}"))
            command += ["--checkpoint-dir", str(root)]
        if self.season:
            command += ["--test-start", self.test_start, "--test-end", self.test_end,
                        "--val-mode", "pre_test"]
        return command + list(self.extra)

    def is_done(self) -> bool:
        return (self.output_dir() / self.run_name / self.variant / "metrics.csv").exists()


def enumerate_tasks(*, cities: tuple[str, ...], arms: tuple[str, ...],
                    horizons: tuple[int, ...], variant: str,
                    seasons: tuple[int, ...] = ()) -> list[Task]:
    tasks: list[Task] = []
    for city in cities:
        for arm in arms:
            if arm in EXPERIMENTS:
                experiment = EXPERIMENTS[arm]
                script = SCRIPT_FOR_MODEL[experiment.model]
                arm_variant = variant or experiment.variant
            elif arm in BASELINE_SCRIPTS:
                script = BASELINE_SCRIPTS[arm][0]
                arm_variant = variant or "post_covid"
            else:
                raise SystemExit(
                    f"Unknown arm {arm!r}. Registry arms: {', '.join(sorted(EXPERIMENTS))}. "
                    f"Baselines: {', '.join(sorted(BASELINE_SCRIPTS))}.")
            for horizon in horizons:
                if not seasons:
                    tasks.append(Task(city=city, arm=arm, script=script,
                                      variant=arm_variant, horizon=horizon))
                    continue
                for year in seasons:
                    tasks.append(Task(
                        city=city, arm=arm, script=script, variant=arm_variant,
                        horizon=horizon, season=f"{year}_{str(year + 1)[2:]}",
                        test_start=f"{year}-06-01", test_end=f"{year + 1}-05-31"))
    return tasks


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)

    lister = sub.add_parser("list", help="Enumerate tasks; optionally write a jsonl.")
    lister.add_argument("--cities", default="boston")
    lister.add_argument("--arms", default="gnn_st")
    lister.add_argument("--horizons", default="1,2,4")
    lister.add_argument("--variant", default="")
    lister.add_argument("--seasons", default="")
    lister.add_argument("--out", type=Path, default=None)

    runner = sub.add_parser("run", help="Run a contiguous block of tasks.")
    runner.add_argument("--tasks", type=Path, required=True)
    runner.add_argument("--start", type=int, default=0)
    runner.add_argument("--count", type=int, default=1)
    runner.add_argument("--log", type=Path, default=None)
    runner.add_argument("--no-carbon", action="store_true")
    runner.add_argument("--skip-existing", action="store_true")
    runner.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.mode == "list":
        tasks = enumerate_tasks(
            cities=tuple(args.cities.split(",")),
            arms=tuple(args.arms.split(",")),
            horizons=tuple(int(h) for h in args.horizons.split(",")),
            variant=args.variant,
            seasons=tuple(int(s) for s in args.seasons.split(",")) if args.seasons else (),
        )
        for index, task in enumerate(tasks):
            print(f"{index:5d}  {task.task_id}")
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text("\n".join(json.dumps(t.to_json()) for t in tasks) + "\n")
            print(f"\n{len(tasks)} tasks -> {args.out}")
        else:
            print(f"\n{len(tasks)} tasks")
        return

    lines = [json.loads(line) for line in args.tasks.read_text().splitlines() if line.strip()]
    block = lines[args.start:args.start + args.count]
    rows = []
    for offset, payload in enumerate(block):
        task = Task.from_json(payload)
        index = args.start + offset
        if args.skip_existing and task.is_done():
            print(f"[{index}] SKIP (metrics.csv exists) {task.task_id}", flush=True)
            rows.append({"index": index, "task_id": task.task_id, "status": "skipped",
                         "seconds": 0.0})
            continue
        command = task.command() + (["--no-carbon"] if args.no_carbon else [])
        print(f"\n[{index}] {task.task_id}\n  {' '.join(command)}", flush=True)
        if args.dry_run:
            continue
        started = time.time()
        completed = subprocess.run(command)
        elapsed = time.time() - started
        status = "ok" if completed.returncode == 0 else f"exit{completed.returncode}"
        # Never abort the block on one failure: a single bad arm should not cost
        # the other nineteen tasks in this array element.
        print(f"[{index}] {status} in {elapsed:.1f}s", flush=True)
        rows.append({"index": index, "task_id": task.task_id, "status": status,
                     "seconds": round(elapsed, 1)})

    if args.log and rows:
        import pandas as pd
        args.log.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(args.log, index=False)
        print(f"\nlog -> {args.log}")


if __name__ == "__main__":
    main()
