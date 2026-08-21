"""Argument-parser pieces shared by every model script, so flags like
--variant and --no-carbon are declared exactly once.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from . import paths
from .constants import TEST_END, TEST_START
from .windows import VARIANTS, Window

ALL_VARIANTS = ("all", *VARIANTS)


def add_common_args(parser: argparse.ArgumentParser, *, variants=("all", "exclude_covid", "post_covid")) -> None:
    parser.add_argument("--variant", choices=variants, default="all",
                        help="Which time-filter experiment to run.")
    parser.add_argument("--output-dir", type=Path, default=paths.RESULTS_DIR,
                        help="Root directory for results/<model>/<variant>/.")
    parser.add_argument("--checkpoint-dir", type=Path, default=paths.CHECKPOINT_DIR,
                        help="Where model .pt files are written. Checkpoint names carry "
                             "no horizon, so a multi-horizon sweep must vary this or "
                             "each horizon silently overwrites the last.")
    parser.add_argument("--test-start", type=pd.Timestamp, default=TEST_START,
                        help="First target week of the evaluation window.")
    parser.add_argument("--test-end", type=pd.Timestamp, default=TEST_END,
                        help="Last target week of the evaluation window.")
    parser.add_argument("--lookback", type=int, default=None,
                        help="Weeks of history per sample (default: model-specific).")
    parser.add_argument("--horizons", type=str, default=None,
                        help="Comma-separated forecast horizons in weeks, e.g. '1,2'.")
    parser.add_argument("--no-carbon", action="store_true",
                        help="Skip codecarbon emissions tracking.")


def resolve_variants(choice: str, *, default=("exclude_covid", "post_covid")) -> tuple[str, ...]:
    return tuple(default) if choice == "all" else (choice,)


def run_tag(model: str, variant: str, window: Window) -> str:
    """codecarbon project name for one run.

    Every run appends to the single results/_emissions/emissions.csv, so the
    name is the only thing distinguishing rows. Without the horizon, a sweep's
    95 rows would be indistinguishable from each other.
    """
    return f"{model}:{variant}:h{window.min_horizon}"


def resolve_window(args: argparse.Namespace, base: Window) -> Window:
    """Apply the window-related CLI overrides onto a model's default Window."""
    from dataclasses import replace

    changes: dict = {"test_start": args.test_start, "test_end": args.test_end}
    if getattr(args, "lookback", None) is not None:
        if args.lookback < 1:
            raise SystemExit("--lookback must be positive")
        changes["lookback"] = args.lookback
    if getattr(args, "horizons", None):
        try:
            horizons = tuple(int(h) for h in str(args.horizons).split(","))
        except ValueError:
            raise SystemExit("--horizons must be comma-separated integers, e.g. '1,2'") from None
        if not horizons or min(horizons) < 1:
            raise SystemExit("--horizons must be positive integers")
        changes["horizons"] = horizons
    return replace(base, **changes)
