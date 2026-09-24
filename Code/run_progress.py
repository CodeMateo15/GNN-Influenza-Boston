#!/usr/bin/env python3
"""Progress bars for training runs, local or on the SLURM cluster.

A ten-seed ensemble at 300 epochs prints several thousand lines and finishes in
half an hour, which makes "is it nearly done?" surprisingly hard to answer. This
parses the two markers run_gnn.py already emits -- `--- seed S (i/n) ---` and
`Epoch N | ...` -- into a percentage, so no instrumentation had to be added to
the training loop.

    python Code/run_progress.py                      # local logs, once
    python Code/run_progress.py --watch              # refresh every 15s
    python Code/run_progress.py --remote             # squeue + logs on Explorer

Status-line contract
--------------------
Any entrypoint that runs longer than about a minute should print these four
lines, unbuffered (`python -u`), so this script can report a percentage:

    Budget: <N> epochs x <M> seeds        # the denominator, once at start
    --- seed <S> (<i>/<M>) ---            # at each seed boundary
    Epoch <N> | <metrics...>              # each epoch
    Outputs: <path>                       # completion marker

Task runners (sweep.py, run_all_horizons.py, run_ablation.py) express their
budget in tasks -- `Budget: <n_tasks> epochs x 1 seeds` -- so the same
arithmetic applies. A log missing `Budget:` renders as `(budget?)`.

Progress is (seeds_done * epochs + current_epoch) / (n_seeds * epochs). It is
honest about what it cannot see: a run that has finished its seeds but is still
in the MC-dropout pass reports 100% and a `finishing` state rather than
pretending to be done, because that phase emits no progress markers at all.
"""

from __future__ import annotations

import argparse
import os
import re
import tempfile
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# The label is captured and deliberately unused: run_gnn.py prints the seed
# number, but a task runner has no seed to name and prints the arm instead.
# Requiring digits here is what silently stopped run_ablation.py's marker
# from parsing, leaving its parent log stuck at 0% while the per-arm logs
# beside it advanced normally.
SEED_RE = re.compile(r"^--- seed (.+?) \((\d+)/(\d+)\) ---")
EPOCH_RE = re.compile(r"^Epoch\s+(\d+) \|")
PARAM_RE = re.compile(r"^Parameters: ([\d,]+)")
DONE_RE = re.compile(r"^Outputs: (.+)")
BUDGET_RE = re.compile(r"^Budget: (\d+) epochs x (\d+) seeds")

BAR_WIDTH = 28


@dataclass
class Run:
    name: str
    seed_index: int = 1
    n_seeds: int = 1
    epoch: int = 0
    budget: int = 0
    done: bool = False
    stale_seconds: float = 0.0

    @property
    def fraction(self) -> float:
        if self.done:
            return 1.0
        if not (self.n_seeds and self.budget):
            return 0.0
        total = self.n_seeds * self.budget
        seen = (self.seed_index - 1) * self.budget + self.epoch
        return min(seen / total, 1.0)

    @property
    def state(self) -> str:
        if self.done:
            return "done"
        # No marker for several minutes and already at the last seed: the run is
        # in MC-dropout / interval calibration, which prints nothing.
        if self.fraction >= 0.99 or (self.stale_seconds > 120 and self.seed_index == self.n_seeds):
            return "finishing"
        if self.stale_seconds > 600:
            return "STALLED?"
        return "training"

    def bar(self) -> str:
        filled = int(round(self.fraction * BAR_WIDTH))
        glyph = "#" * filled + "." * (BAR_WIDTH - filled)
        seeds = f"seed {self.seed_index}/{self.n_seeds}"
        epochs = f"ep {self.epoch}/{self.budget}" if self.budget else "ep ?"
        return (f"  {self.name:<34s} [{glyph}] {self.fraction * 100:5.1f}%  "
                f"{seeds:<12s} {epochs:<12s} {self.state}")


def parse_log(path: Path) -> Run:
    run = Run(name=path.stem)
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return run
    for line in text.splitlines():
        if m := SEED_RE.match(line):
            run.seed_index, run.n_seeds = int(m.group(2)), int(m.group(3))
            run.epoch = 0
        elif m := EPOCH_RE.match(line):
            run.epoch = int(m.group(1))
        elif m := BUDGET_RE.match(line):
            run.budget = int(m.group(1))
            run.n_seeds = max(run.n_seeds, int(m.group(2)))
        elif DONE_RE.match(line):
            run.done = True
    if not run.budget:
        # Older logs predate the Budget line. Fall back to the largest epoch
        # seen rather than reporting a fraction of an unknown denominator, and
        # mark it so the number is not mistaken for a real percentage.
        run.budget = max(run.epoch, 1)
        run.name += " (budget?)"
    try:
        run.stale_seconds = time.time() - path.stat().st_mtime
    except OSError:
        pass
    return run


def local_runs(log_dir: Path, pattern: str) -> list[Run]:
    return sorted((parse_log(p) for p in log_dir.glob(pattern)),
                  key=lambda r: (r.done, r.name))


def remote_status(host: str, root: str, total: int | None = None,
                  subdir: str = "") -> str:
    """squeue plus per-array-task progress, in one ssh round trip.

    `total` is the number of runs the submitted task list contains. squeue can
    say how many array elements are alive but not how far through their chunk
    they are, so without a denominator there is no percentage -- and a bare
    "still running" is not a progress report. `subdir` narrows
    the completed-run count to one study's output tree.
    """
    script = f"""
    echo "### queue"
    squeue -u $USER -o "%.10i %.20j %.9P %.8T %.10M %.6D %R" 2>/dev/null | head -20
    echo "### tasks"
    for f in {root}/logs/task_*.csv; do
      [ -f "$f" ] || continue
      n=$(($(wc -l < "$f") - 1))
      echo "$(basename $f .csv) $n"
    done 2>/dev/null
    echo "### results"
    find {root}/Code/results/{subdir} -name metrics.csv 2>/dev/null | wc -l
    """
    out = subprocess.run(["ssh", "-o", "BatchMode=yes", host, script],
                         capture_output=True, text=True, timeout=60)
    text = out.stdout or out.stderr
    if total:
        done = 0
        tail = text.rsplit("### results", 1)
        if len(tail) == 2:
            digits = tail[1].strip().splitlines()
            done = int(digits[0]) if digits and digits[0].strip().isdigit() else 0
        fraction = min(done / total, 1.0) if total else 0.0
        filled = int(round(fraction * BAR_WIDTH))
        text += (f"\n  {'OVERALL':<34s} [{'#' * filled}{'.' * (BAR_WIDTH - filled)}] "
                 f"{fraction * 100:5.1f}%  {done}/{total} runs complete\n")
    return text


def render(runs: list[Run], total_tasks: int | None = None) -> str:
    if not runs:
        return "  (no runs found)"
    lines = [r.bar() for r in runs]
    active = [r for r in runs if not r.done]
    finished = len(runs) - len(active)
    overall = sum(r.fraction for r in runs) / len(runs)
    filled = int(round(overall * BAR_WIDTH))
    lines.append("")
    lines.append(f"  {'OVERALL':<34s} [{'#' * filled}{'.' * (BAR_WIDTH - filled)}] "
                 f"{overall * 100:5.1f}%  {finished}/{len(runs)} runs complete")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--log-dir", type=Path,
                        default=None,
                        help="Default: paths.LOG_DIR (set GNNFLU_LOG_DIR to change).")
    parser.add_argument("--pattern", default="**/*.log")
    parser.add_argument("--watch", action="store_true", help="Refresh until everything is done.")
    parser.add_argument("--interval", type=int, default=15)
    parser.add_argument("--remote", action="store_true", help="Show Explorer queue and task progress.")
    parser.add_argument("--host", default="explorer")
    parser.add_argument("--root", default="/scratch/$USER/gnn-flu")
    parser.add_argument("--total", type=int, default=None,
                        help="Runs in the submitted task list, so --remote can "
                             "print a percentage instead of just a queue dump.")
    parser.add_argument("--subdir", default="",
                        help="Narrow the completed-run count to one results "
                             "subtree, e.g. _ablation/main.")
    args = parser.parse_args()

    if args.remote:
        print(remote_status(args.host, args.root, args.total, args.subdir))
        return

    while True:
        # Same default as influenza.paths.LOG_DIR, repeated rather than imported
        # so this script stays runnable without the package on the path.
        log_dir = args.log_dir or Path(os.environ.get("GNNFLU_LOG_DIR")
                                       or Path(tempfile.gettempdir()) / "gnn-flu-logs")
        runs = local_runs(log_dir, args.pattern)
        stamp = time.strftime("%H:%M:%S")
        block = f"\nTraining progress  {stamp}\n" + "-" * 78 + "\n" + render(runs)
        if args.watch:
            print("\033[2J\033[H" + block, flush=True)
            if runs and all(r.done for r in runs):
                print("\n  all runs complete")
                return
            time.sleep(args.interval)
        else:
            print(block)
            return


if __name__ == "__main__":
    main()
