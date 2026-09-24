"""Run every model at every forecast horizon, one results tree per horizon.

One week ahead, no model can win by much: next week's ILI is almost this
week's ILI, so persistence is already near the ceiling. That is a fact about
the task, not about the models. Horizon 1 is still run -- it is the number the
paper reports -- but 2 and 4 weeks are where the models have somewhere to
separate, and where the margin over the baselines is worth quoting.

Each horizon gets its own root, `results/horizon_04/<model>/<variant>/`, so
`metrics.csv` still sits two levels below it and compare_models.py works
unchanged when pointed at one. The top-level `results/` tree is untouched.

Three things this enforces that are easy to get wrong by hand:

  * **One horizon per invocation.** With `--horizons 1,4` test membership is
    decided by horizon 1 while `valid_origins` requires t+4 to exist, so the
    test set silently shrinks and the two horizons score different weeks.
  * **An explicit variant, always.** run_gnn.py and run_dualtopo.py read
    `--variant all` as "use the registry's variant" and run exactly one, unlike
    the other three scripts which expand it.
  * **A per-horizon checkpoint directory.** Checkpoint filenames carry no
    horizon, so a sweep sharing one directory overwrites the same file three
    times and leaves whichever horizon finished last.

    python Code/run_all_horizons.py --horizons 1,2,4 --dry-run
    python Code/run_all_horizons.py --horizons 1,2,4
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas numpy.") from exc

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths
from influenza.cities import DEFAULT_CITY, City, get as get_city, names as city_names
from influenza.constants import TEST_END, TEST_START
from influenza.windows import Window, split_origins, valid_origins, variant_data

DEFAULT_HORIZONS = (1, 2, 4)


def default_log_dir() -> Path:
    """Where run_progress.py looks by default; see CLAUDE.md rule 3."""
    return Path(os.environ.get(
        "CLAUDE_SCRATCHPAD",
        "/private/tmp/claude-501/-Users-mateobiggs-GNN-Influenza-Boston")) / "horizon_logs"
DEFAULT_VARIANTS = ("exclude_covid", "post_covid")


@dataclass(frozen=True)
class Job:
    """One model run. `model` is the results directory the script will create."""

    model: str
    script: str
    variant: str
    extra: tuple[str, ...] = field(default_factory=tuple)
    # dualtopo's Window carries lookback=52 of its own; leave it alone.
    native_lookback: int | None = None

    @property
    def key(self) -> str:
        return f"{self.model}/{self.variant}"


def build_matrix(variants: tuple[str, ...], city: City) -> tuple[Job, ...]:
    """The run matrix: the eight arms on the leaderboard, nothing else.

    Ablations of `gnn_st` are deliberately absent -- they are a separate axis
    with its own runner and its own noise-floor accounting. See run_ablation.py.

    `variants` is intersected with the city's own list by the caller, so a city
    with only post_covid history does not enqueue exclude_covid jobs that
    cli.resolve_city would reject one subprocess later.
    """
    jobs: list[Job] = []

    for variant in variants:
        jobs.append(Job("persistence", "run_seasonal_naive.py", variant, ("--season-lag", "1")))
        jobs.append(Job("seasonal_naive", "run_seasonal_naive.py", variant, ("--season-lag", "52")))
        jobs.append(Job("arima", "run_arima.py", variant))
        jobs.append(Job("lstm", "run_lstm.py", variant))
        # Boosted trees over the same per-node columns the graph model reads, with
        # no edges. The strongest non-graph baseline at four weeks.
        jobs.append(Job("xgboost", "run_xgboost.py", variant))

    # The headline arm. 16-week lookback natively, and its 10-seed ensemble makes
    # it roughly 10x the cost of a baseline -- which is why the sweep is a
    # job-array candidate rather than a laptop loop. See Code/sweep.py.
    jobs.append(Job("gnn_st", "run_gnn.py", "post_covid",
                    ("--experiment", "gnn_st"), native_lookback=16))

    # The two Luo et al. 2025 models, both standalone with a 52-week native
    # window, so both are excluded from shorter-lookback sweeps.
    jobs.append(Job("gat", "run_gat.py", "post_covid",
                    ("--experiment", "gat"), native_lookback=52))
    jobs.append(Job("dualtopo", "run_dualtopo.py", "post_covid",
                    ("--experiment", "dualtopo"), native_lookback=52))
    return tuple(jobs)


def run_config_horizons(directory: Path) -> list[int] | None:
    """Horizons recorded by a finished run, or None if it did not finish.

    The baselines write a top-level "window"; run_gnn and run_dualtopo nest it
    under "experiment". Both shapes are read here so `--skip-existing` does not
    quietly re-run half the matrix.
    """
    config = directory / "run_config.json"
    if not all((directory / name).exists()
               for name in ("metrics.csv", "predictions.csv", "run_config.json")):
        return None
    try:
        payload = json.loads(config.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    window = payload.get("window") or payload.get("experiment", {}).get("window", {})
    horizons = window.get("horizons")
    return [int(h) for h in horizons] if horizons else None


def is_complete(directory: Path, horizon: int) -> bool:
    return run_config_horizons(directory) == [horizon]


def build_command(job: Job, horizon: int, args: argparse.Namespace) -> list[str]:
    out_root = paths.horizon_dir(horizon, args.results_dir)
    ckpt_root = paths.horizon_dir(horizon, args.checkpoint_root)
    command = [
        # -u so the child's own status lines reach the tee'd log as they are
        # printed rather than at exit. See CLAUDE.md "Status-line contract".
        sys.executable, "-u", str(Path(__file__).resolve().parent / job.script),
        "--city", args.city,
        "--variant", job.variant,
        "--horizons", str(horizon),
        "--output-dir", str(out_root),
        "--checkpoint-dir", str(ckpt_root),
        *job.extra,
    ]
    if job.native_lookback is None and args.lookback is not None:
        command += ["--lookback", str(args.lookback)]
    if args.no_carbon:
        command.append("--no-carbon")
    if job.script == "run_arima.py" and args.max_d is not None:
        command += ["--max-d", str(args.max_d)]
    return command


def run_job(job: Job, horizon: int, args: argparse.Namespace, log_dir: Path) -> dict:
    """Run one model at one horizon, tee-ing its output to a watchable log.

    Output goes to a file rather than into a pipe so that run_progress.py can
    read the child's own `Budget:` / `Epoch` / `--- seed ---` markers while the
    job is still running. Capturing it in memory, as this used to, meant a
    ten-seed gnn_st job was a single silent hour.
    """
    out_dir = paths.horizon_dir(horizon, args.results_dir) / job.model / job.variant
    if args.skip_existing and is_complete(out_dir, horizon):
        return {"status": "skipped", "seconds": 0.0, "returncode": 0, "stderr": "",
                "log": ""}

    command = build_command(job, horizon, args)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"h{horizon:02d}_{job.model}_{job.variant}.log"
    started = time.perf_counter()
    with log_path.open("w") as handle:
        completed = subprocess.run(command, stdout=handle,
                                   stderr=subprocess.STDOUT, text=True)
    elapsed = time.perf_counter() - started
    lines = log_path.read_text(errors="replace").splitlines()

    if completed.returncode != 0:
        return {"status": "failed", "seconds": elapsed,
                "returncode": completed.returncode,
                "stderr": "\n".join(line for line in lines[-20:]),
                "log": str(log_path)}

    # A zero exit with no artifacts means the script wrote somewhere unexpected.
    if not is_complete(out_dir, horizon):
        return {"status": "failed", "seconds": elapsed, "returncode": 0,
                "stderr": f"exited 0 but {out_dir} has no run_config.json for horizon {horizon}",
                "log": str(log_path)}

    warning = [line for line in lines if line.startswith("warning:")]
    return {"status": "ok", "seconds": elapsed, "returncode": 0,
            "stderr": "\n".join(warning[-3:]), "log": str(log_path)}


def check_geometry(horizons: tuple[int, ...], variants: tuple[str, ...],
                   city: City) -> list[str]:
    """Assert every horizon scores the same test weeks, before anything trains.

    Test membership is decided by target date, so all horizons should land on
    the same 49 origins covering 2025-06-01..2026-05-03. If they do not, the
    error-growth curve would be comparing different evaluation sets and every
    number downstream would be meaningless.
    """
    rates = city.loaders.load_rates()
    problems: list[str] = []
    spans: set[tuple[str, str]] = set()
    print(f"\n{'variant':>14} {'H':>3} {'origins':>8} {'train':>6} {'val':>5} {'test':>5}  "
          f"test target span")
    for variant in variants:
        index = variant_data(rates, variant).index
        for horizon in horizons:
            window = Window(horizons=(horizon,))
            origins = valid_origins(index, window)
            try:
                split = split_origins(index, origins, window)
            except ValueError as exc:
                problems.append(f"{variant} h={horizon}: {exc}")
                continue
            first, last = split.test_target_span()
            spans.add((str(first.date()), str(last.date())))
            print(f"{variant:>14} {horizon:>3} {len(origins):>8} {len(split.train):>6} "
                  f"{len(split.val):>5} {len(split.test):>5}  {first.date()} -> {last.date()}")
            if not (TEST_START <= first <= TEST_END):
                problems.append(f"{variant} h={horizon}: first test target {first.date()} "
                                f"outside the evaluation window")
    if len(spans) > 1:
        problems.append(f"test target spans differ across runs: {sorted(spans)}; "
                        f"the horizons would not be comparable")
    return problems


def main() -> None:
    args = parse_args()
    city = get_city(args.city)
    horizons = args.horizons
    # Only the variants this city actually has. Columbus and Buenos Aires start
    # in 2022, so exclude_covid is not a window they can express.
    variants = tuple(v for v in args.variants if v in city.variants)
    dropped = tuple(v for v in args.variants if v not in city.variants)
    if dropped:
        print(f"note: {city.label} has no {', '.join(dropped)} history; "
              f"running {', '.join(variants) or '(nothing)'}")
    if not variants:
        raise SystemExit(f"error: none of {args.variants} exist for {city.label}. "
                         f"Available: {', '.join(city.variants)}.")
    matrix = build_matrix(variants, city)
    if args.models:
        wanted = {m.strip() for m in args.models.split(",") if m.strip()}
        unknown = wanted - {job.model for job in matrix}
        if unknown:
            raise SystemExit(f"error: unknown models {sorted(unknown)}. "
                             f"Available: {sorted({j.model for j in matrix})}")
        matrix = tuple(job for job in matrix if job.model in wanted)

    print(f"{city.label}: {len(matrix)} runs x {len(horizons)} horizons = "
          f"{len(matrix) * len(horizons)} jobs")
    print(f"Results root: {paths.display(args.results_dir)}")

    problems = check_geometry(horizons, variants, city)
    for problem in problems:
        print(f"\nerror: {problem}", file=sys.stderr)
    if problems:
        raise SystemExit(1)
    print("\nSplit geometry OK: every horizon scores the same test weeks.")

    if args.dry_run:
        print("\nCommands:")
        for horizon in horizons:
            for job in matrix:
                print("  " + " ".join(build_command(job, horizon, args)))
        return

    log: list[dict] = []
    log_dir = args.log_dir or default_log_dir()
    # run_progress.py denominator. This is a task runner, so the budget is
    # expressed in tasks and each finished job advances the epoch axis -- the
    # convention CLAUDE.md sets out under "Status-line contract", and the same
    # one run_ablation.py uses. Without these lines a three-horizon sweep was
    # invisible to the reporter.
    total = len(matrix) * len(horizons)
    print(f"Budget: {total} epochs x 1 seeds", flush=True)
    print(f"Per-job logs: {log_dir}", flush=True)
    done = 0
    for horizon in horizons:
        print(f"\n{'=' * 78}\nHORIZON {horizon}\n{'=' * 78}", flush=True)
        for job in matrix:
            outcome = run_job(job, horizon, args, log_dir)
            done += 1
            log.append({"horizon": horizon, "model": job.model, "variant": job.variant,
                        **outcome})
            mark = {"ok": "ok", "skipped": "--", "failed": "FAIL"}[outcome["status"]]
            print(f"Epoch {done} | {job.key} h={horizon} [{mark}] "
                  f"{outcome['seconds']:.1f}s", flush=True)
            print(f"  [{mark:>4}] {job.key:<40} {outcome['seconds']:6.1f}s", flush=True)
            if outcome["stderr"]:
                for line in outcome["stderr"].splitlines():
                    print(f"         {line}")
            if outcome["status"] == "failed" and args.stop_on_error:
                raise SystemExit(f"stopping: {job.key} at horizon {horizon} failed")

    frame = pd.DataFrame(log)
    cross_horizon = args.results_dir / paths.CROSS_HORIZON_DIR.name
    cross_horizon.mkdir(parents=True, exist_ok=True)
    destination = cross_horizon / "sweep_log.csv"
    frame.to_csv(destination, index=False)

    counts = frame["status"].value_counts()
    print(f"\n{'=' * 78}")
    print(f"{int(counts.get('ok', 0))} ok | {int(counts.get('skipped', 0))} skipped | "
          f"{int(counts.get('failed', 0))} failed | "
          f"{frame['seconds'].sum() / 60:.1f} min total")
    print(f"Log: {destination}")
    # Completion marker for run_progress.py.
    print(f"Outputs: {paths.display(destination)}", flush=True)

    if args.compare:
        for horizon in horizons:
            root = paths.horizon_dir(horizon, args.results_dir)
            subprocess.run([sys.executable,
                            str(Path(__file__).resolve().parent / "compare_models.py"),
                            "--city", args.city,
                            "--results-dir", str(root)], check=False)

    if int(counts.get("failed", 0)):
        raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--city", choices=city_names(), default=DEFAULT_CITY,
                        help="Which city to sweep. Results and checkpoints land under "
                             "the city's root; Boston keeps the historical top-level "
                             "layout. Variants are intersected with the city's own list.")
    parser.add_argument("--horizons", default=",".join(str(h) for h in DEFAULT_HORIZONS),
                        help="Comma-separated. Each runs as its own single-horizon job.")
    parser.add_argument("--variants", default=",".join(DEFAULT_VARIANTS),
                        help="Comma-separated variants for the baselines.")
    parser.add_argument("--models", default=None, help="Comma-separated subset of the matrix.")
    # Default None, then resolved through city_root below, so that an explicit
    # --results-dir is still honoured verbatim -- matching cli.city_output_dirs.
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--checkpoint-root", type=Path, default=None)
    parser.add_argument("--lookback", type=int, default=None,
                        help="Override the lookback for models that do not set their own. "
                             "Left unset for the headline sweep so the error-growth curve "
                             "varies only the horizon.")
    parser.add_argument("--max-d", type=int, default=None, help="Passed to run_arima.py.")
    parser.add_argument("--skip-existing", action="store_true", default=True)
    parser.add_argument("--no-skip-existing", dest="skip_existing", action="store_false",
                        help="Re-run everything, even completed jobs.")
    parser.add_argument("--stop-on-error", action="store_true",
                        help="Abort on the first failure instead of logging and continuing.")
    parser.add_argument("--no-carbon", action="store_true")
    parser.add_argument("--compare", action="store_true",
                        help="Run compare_models.py per horizon when the sweep finishes.")
    parser.add_argument("--log-dir", type=Path, default=None,
                        help="Where per-job stdout is tee'd. Defaults to the "
                             "session scratchpad that run_progress.py watches.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check split geometry and print commands; run nothing.")
    args = parser.parse_args()

    try:
        args.horizons = tuple(int(h) for h in str(args.horizons).split(","))
    except ValueError:
        parser.error("--horizons must be comma-separated integers, e.g. '2,4,12'")
    if not args.horizons or min(args.horizons) < 1:
        parser.error("--horizons must be positive integers")
    args.variants = tuple(v.strip() for v in args.variants.split(",") if v.strip())
    if args.results_dir is None:
        args.results_dir = paths.city_root(args.city, paths.RESULTS_DIR)
    if args.checkpoint_root is None:
        args.checkpoint_root = paths.city_root(args.city, paths.CHECKPOINT_DIR)
    return args


if __name__ == "__main__":
    main()
