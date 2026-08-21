"""Run every model at every forecast horizon, one results tree per horizon.

At one week ahead the leaderboard is a tie: nothing beats persistence, because
next week's ILI is almost this week's ILI and there is no room for a model to
distinguish itself. That is a fact about the task, not about the models. This
script asks the harder question -- 2, 4, 12, 24 and 52 weeks ahead -- where the
models have somewhere to separate.

Each horizon gets its own root, `results/horizon_24/<model>/<variant>/`, so
`metrics.csv` still sits two levels below it and compare_models.py works
unchanged when pointed at one. The top-level `results/` tree is untouched.

Three things this enforces that are easy to get wrong by hand:

  * **One horizon per invocation.** With `--horizons 1,52` test membership is
    decided by horizon 1 while `valid_origins` requires t+52 to exist, so the
    test set silently shrinks and the two horizons score different weeks.
  * **An explicit variant, always.** run_gnn.py and run_dualtopo.py read
    `--variant all` as "use the registry's variant" and run exactly one, unlike
    the other three scripts which expand it.
  * **A per-horizon checkpoint directory.** Checkpoint filenames carry no
    horizon, so a sweep sharing one directory overwrites the same file five
    times and leaves whichever horizon finished last.

    python Code/run_all_horizons.py --horizons 2,4,12,24,52 --dry-run
    python Code/run_all_horizons.py --horizons 2,4,12,24,52
"""

from __future__ import annotations

import argparse
import json
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
from influenza.constants import TEST_END, TEST_START
from influenza.windows import Window, split_origins, valid_origins, variant_data

DEFAULT_HORIZONS = (2, 4, 12, 24, 52)
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


def build_matrix(variants: tuple[str, ...]) -> tuple[Job, ...]:
    """The run matrix, mirroring the directories already in Code/results/.

    The `full`-variant arms are pinned to `full` regardless of --variants: they
    exist precisely to contrast against the post_covid ones, so filtering them
    by variant would silently drop the contrast rather than narrowing it.
    """
    jobs: list[Job] = []

    for variant in variants:
        jobs.append(Job("persistence", "run_seasonal_naive.py", variant, ("--season-lag", "1")))
        jobs.append(Job("seasonal_naive", "run_seasonal_naive.py", variant, ("--season-lag", "52")))
        jobs.append(Job("arima", "run_arima.py", variant))
        jobs.append(Job("lstm", "run_lstm.py", variant))

    # The GCN registry entries are all defined on post_covid; run them there
    # regardless, and add the `full` arms as their own contrast.
    for name in ("gnn_geo", "gnn_corrbinary", "gnn_multiedge", "gnn_uniform",
                 "gnn_multiedge_rt", "gnn_multiedge_covid_rsv",
                 # The long-horizon corrections, run at every horizon so their
                 # cost at 1-2 weeks is visible alongside their benefit at 24-52.
                 "gnn_multiedge_season", "gnn_multiedge_level",
                 "gnn_multiedge_season_level"):
        jobs.append(Job(name, "run_gnn.py", "post_covid", ("--experiment", name)))

    jobs.append(Job("gnn_multiedge_full", "run_gnn.py", "full",
                    ("--experiment", "gnn_multiedge", "--name", "gnn_multiedge_full")))
    # The leakage demonstration: normalising over the whole series instead of the
    # training window only. Not a registry entry because it is a deliberately
    # wrong configuration kept for the contrast it provides.
    jobs.append(Job("gnn_multiedge_leaknorm", "run_gnn.py", "post_covid",
                    ("--experiment", "gnn_multiedge", "--normalize", "all",
                     "--name", "gnn_multiedge_leaknorm")))
    jobs.append(Job("gnn_multiedge_covid_rsv_full", "run_gnn.py", "full",
                    ("--experiment", "gnn_multiedge_covid_rsv",
                     "--name", "gnn_multiedge_covid_rsv_full")))

    jobs.append(Job("dualtopo", "run_dualtopo.py", "post_covid",
                    ("--experiment", "dualtopo"), native_lookback=52))
    jobs.append(Job("dualtopo_no_bg", "run_dualtopo.py", "post_covid",
                    ("--experiment", "dualtopo_no_bg"), native_lookback=52))
    jobs.append(Job("dualtopo_fullhistory", "run_dualtopo.py", "full",
                    ("--experiment", "dualtopo", "--name", "dualtopo_fullhistory"),
                    native_lookback=52))
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
        sys.executable, str(Path(__file__).resolve().parent / job.script),
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


def run_job(job: Job, horizon: int, args: argparse.Namespace) -> dict:
    out_dir = paths.horizon_dir(horizon, args.results_dir) / job.model / job.variant
    if args.skip_existing and is_complete(out_dir, horizon):
        return {"status": "skipped", "seconds": 0.0, "returncode": 0, "stderr": ""}

    command = build_command(job, horizon, args)
    started = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True)
    elapsed = time.perf_counter() - started

    if completed.returncode != 0:
        tail = "\n".join(completed.stderr.strip().splitlines()[-20:])
        return {"status": "failed", "seconds": elapsed,
                "returncode": completed.returncode, "stderr": tail}

    # A zero exit with no artifacts means the script wrote somewhere unexpected.
    if not is_complete(out_dir, horizon):
        return {"status": "failed", "seconds": elapsed, "returncode": 0,
                "stderr": f"exited 0 but {out_dir} has no run_config.json for horizon {horizon}"}

    warning = [line for line in completed.stderr.splitlines() if line.startswith("warning:")]
    return {"status": "ok", "seconds": elapsed, "returncode": 0,
            "stderr": "\n".join(warning[-3:])}


def check_geometry(horizons: tuple[int, ...], variants: tuple[str, ...]) -> list[str]:
    """Assert every horizon scores the same test weeks, before anything trains.

    Test membership is decided by target date, so all horizons should land on
    the same 49 origins covering 2025-06-01..2026-05-03. If they do not, the
    error-growth curve would be comparing different evaluation sets and every
    number downstream would be meaningless.
    """
    from influenza.data import load_rates

    rates = load_rates()
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
    horizons = args.horizons
    variants = args.variants
    matrix = build_matrix(variants)
    if args.models:
        wanted = {m.strip() for m in args.models.split(",") if m.strip()}
        unknown = wanted - {job.model for job in matrix}
        if unknown:
            raise SystemExit(f"error: unknown models {sorted(unknown)}. "
                             f"Available: {sorted({j.model for j in matrix})}")
        matrix = tuple(job for job in matrix if job.model in wanted)

    print(f"{len(matrix)} runs x {len(horizons)} horizons = {len(matrix) * len(horizons)} jobs")

    problems = check_geometry(horizons, variants)
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
    for horizon in horizons:
        print(f"\n{'=' * 78}\nHORIZON {horizon}\n{'=' * 78}")
        for job in matrix:
            outcome = run_job(job, horizon, args)
            log.append({"horizon": horizon, "model": job.model, "variant": job.variant,
                        **outcome})
            mark = {"ok": "ok", "skipped": "--", "failed": "FAIL"}[outcome["status"]]
            print(f"  [{mark:>4}] {job.key:<40} {outcome['seconds']:6.1f}s")
            if outcome["stderr"]:
                for line in outcome["stderr"].splitlines():
                    print(f"         {line}")
            if outcome["status"] == "failed" and args.stop_on_error:
                raise SystemExit(f"stopping: {job.key} at horizon {horizon} failed")

    frame = pd.DataFrame(log)
    paths.CROSS_HORIZON_DIR.mkdir(parents=True, exist_ok=True)
    destination = paths.CROSS_HORIZON_DIR / "sweep_log.csv"
    frame.to_csv(destination, index=False)

    counts = frame["status"].value_counts()
    print(f"\n{'=' * 78}")
    print(f"{int(counts.get('ok', 0))} ok | {int(counts.get('skipped', 0))} skipped | "
          f"{int(counts.get('failed', 0))} failed | "
          f"{frame['seconds'].sum() / 60:.1f} min total")
    print(f"Log: {destination}")

    if args.compare:
        for horizon in horizons:
            root = paths.horizon_dir(horizon, args.results_dir)
            subprocess.run([sys.executable,
                            str(Path(__file__).resolve().parent / "compare_models.py"),
                            "--results-dir", str(root)], check=False)

    if int(counts.get("failed", 0)):
        raise SystemExit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--horizons", default=",".join(str(h) for h in DEFAULT_HORIZONS),
                        help="Comma-separated. Each runs as its own single-horizon job.")
    parser.add_argument("--variants", default=",".join(DEFAULT_VARIANTS),
                        help="Comma-separated variants for the baselines.")
    parser.add_argument("--models", default=None, help="Comma-separated subset of the matrix.")
    parser.add_argument("--results-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--checkpoint-root", type=Path, default=paths.CHECKPOINT_DIR)
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
    return args


if __name__ == "__main__":
    main()
