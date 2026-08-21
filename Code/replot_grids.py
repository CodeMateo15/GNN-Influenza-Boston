"""Redraw every run's actual_vs_predicted grid from the predictions already on disk.

The per-run grids are written by `finish_run` at the end of a training run, so a
change to the plotting code -- such as pinning the y-axis per neighborhood so two
models can be compared by eye -- otherwise only reaches a chart the next time
that model is retrained. This redraws them all from predictions.csv, which costs
seconds and retrains nothing:

    python Code/replot_grids.py                          # every horizon, every run
    python Code/replot_grids.py --results-dir Code/results/horizon_01
    python Code/replot_grids.py --models arima,lstm --dry-run
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas.") from exc

from influenza import paths
from influenza.plots import save_grid_plot


def discover(results_root: Path) -> list[Path]:
    """Every run directory holding a predictions.csv, '_' directories skipped."""
    found = sorted(
        path for path in results_root.rglob("predictions.csv")
        if not any(part.startswith("_") for part in path.relative_to(results_root).parts)
    )
    return [path.parent for path in found]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--models", default=None, help="Comma-separated subset.")
    parser.add_argument("--variant", default=None)
    parser.add_argument("--dry-run", action="store_true",
                        help="List what would be redrawn without writing anything.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.results_dir.resolve()
    runs = discover(root)
    if args.models:
        wanted = {m.strip() for m in args.models.split(",")}
        runs = [d for d in runs if d.parent.name in wanted]
    if args.variant:
        runs = [d for d in runs if d.name == args.variant]
    if not runs:
        raise SystemExit(f"error: no predictions.csv under {root} matched the filters.")

    written = 0
    for run in runs:
        model, variant = run.parent.name, run.name
        predictions = pd.read_csv(run / "predictions.csv", parse_dates=["target_date"])
        # One chart per horizon present, matching finish_run's naming so the new
        # file replaces the old one rather than sitting beside it.
        for horizon in sorted(int(h) for h in predictions["horizon"].unique()):
            path = run / f"actual_vs_predicted_horizon{horizon}.png"
            if args.dry_run:
                print(f"  would write {paths.display(path)}")
                continue
            save_grid_plot(
                predictions, path,
                f"{model} ({variant}) — {horizon} week{'s' if horizon > 1 else ''} ahead",
                horizon=horizon, bands=True,
            )
            written += 1
            print(f"  wrote {paths.display(path)}")

    verb = "would redraw" if args.dry_run else "redrew"
    print(f"{verb} {len(runs)} runs" + ("" if args.dry_run else f", {written} charts"))


if __name__ == "__main__":
    main()
