"""Argument-parser pieces shared by every model script, so flags like
--variant and --no-carbon are declared exactly once.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from . import paths
from .cities import DEFAULT_CITY, get as get_city, names as city_names
from .constants import TEST_END, TEST_START
from .windows import VARIANTS, Window

ALL_VARIANTS = ("all", *VARIANTS)


def add_common_args(parser: argparse.ArgumentParser, *, variants=("all", "exclude_covid", "post_covid")) -> None:
    parser.add_argument("--city", choices=city_names(), default=DEFAULT_CITY,
                        help="Which city to model. Boston writes to results/, other "
                             "cities to results/<city>/.")
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


def resolve_city(args: argparse.Namespace):
    """The City for this run, with its variant choice validated against it.

    Columbus has no pre-COVID history, so `--city columbus --variant full` is not
    a thing that exists. Failing here beats training on a silently empty slice.
    """
    city = get_city(getattr(args, "city", None) or DEFAULT_CITY)
    variant = getattr(args, "variant", "all")
    if variant not in ("all", *city.variants):
        raise SystemExit(
            f"--variant {variant} is not available for {city.label}. "
            f"{city.label} supports: {', '.join(city.variants)}."
        )
    return city


def city_output_dirs(args: argparse.Namespace, city) -> tuple[Path, Path]:
    """(results_root, checkpoint_root) for a run, honouring explicit overrides.

    If the user passed --output-dir/--checkpoint-dir we respect it verbatim; the
    per-city subdirectory is only applied to the defaults, so a horizon sweep
    that already redirects both keeps working unchanged.
    """
    results = args.output_dir
    checkpoints = args.checkpoint_dir
    if results == paths.RESULTS_DIR:
        results = paths.city_root(city.name)
    if checkpoints == paths.CHECKPOINT_DIR:
        checkpoints = paths.city_root(city.name, paths.CHECKPOINT_DIR)
    return results, checkpoints
