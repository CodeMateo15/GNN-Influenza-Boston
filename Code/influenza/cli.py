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
    # Default None, not TEST_START/TEST_END, so that an experiment can define its
    # own evaluation window and have it survive. Every other window field here is
    # already an opt-in override; these two were not, which silently overwrote a
    # registry Window with the constant on every single run. The resolved default
    # is unchanged, because Window itself defaults to the same constants.
    parser.add_argument("--test-start", type=pd.Timestamp, default=None,
                        help=f"First target week of the evaluation window "
                             f"(default: the experiment's own, usually {TEST_START.date()}).")
    parser.add_argument("--test-end", type=pd.Timestamp, default=None,
                        help=f"Last target week of the evaluation window "
                             f"(default: the experiment's own, usually {TEST_END.date()}).")
    parser.add_argument("--lookback", type=int, default=None,
                        help="Weeks of history per sample (default: model-specific).")
    parser.add_argument("--horizons", type=str, default=None,
                        help="Comma-separated forecast horizons in weeks, e.g. '1,2'.")
    parser.add_argument("--val-mode", choices=("tail", "pre_test"), default=None,
                        help="How the validation slice is chosen. 'tail' (default) "
                             "is correct when the test window ends the series; "
                             "'pre_test' is REQUIRED for a mid-series window, "
                             "which run_backtest.py uses.")
    parser.add_argument("--two-sided-intervals", action="store_true",
                        help="Fit the two edges of the 95%% band separately instead of "
                             "one symmetric width. Every model in this project forecasts "
                             "late, so a symmetric band under-covers the weeks when the "
                             "curve is climbing -- 83.9%% against 97.4%% falling, for "
                             "gnn_st at horizon 2. Off by default so committed numbers "
                             "reproduce; see influenza/intervals.py.")
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


def resolve_window(args: argparse.Namespace, base: Window, city=None) -> Window:
    """Apply the window-related CLI overrides onto a model's default Window.

    `city` is optional and only matters for a city that declares its own
    evaluation window. An explicit --test-start/--test-end still wins, so the
    precedence is CLI > city > shared default.
    """
    from dataclasses import replace

    changes: dict = {}
    if city is not None:
        for field in ("test_start", "test_end"):
            value = getattr(city, field, None)
            if value is not None:
                changes[field] = pd.Timestamp(value)
    for field in ("test_start", "test_end"):
        value = getattr(args, field, None)
        if value is not None:
            changes[field] = value
    if getattr(args, "val_mode", None) is not None:
        changes["val_mode"] = args.val_mode
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


# Which FeatureSpec flag corresponds to which City.available_features entry.
# Only the flags a city can actually lack are listed; flu lags are always on.
_FEATURE_FLAGS = (
    ("use_weather", "weather"),
    ("use_demographics", "demographics"),
    ("use_wastewater", "wastewater"),
    ("use_seasonality", "seasonality"),
)


def check_experiment_supported(experiment, city) -> None:
    """Fail at argument-parse time, not three loaders deep.

    `City.require_feature` already refuses an unavailable input, but the loaders
    are where it fires -- so `--city buenos_aires --experiment gnn_st` used to
    build a dataset, resolve a split and only then raise out of
    `load_static_demographics`. The message was right and the timing was wrong.

    Names a compatible arm rather than just refusing, because "this city has no
    demographics" is not actionable on its own: what the user wants to know is
    which arm to run instead.
    """
    from .config import EXPERIMENTS

    features = experiment.features
    missing = [name for flag, name in _FEATURE_FLAGS
               if getattr(features, flag, False) and not city.supports(name)]
    graph_demo = getattr(experiment.graph, "demo", False)
    if graph_demo and not city.supports("demographics") and "demographics" not in missing:
        missing.append("demographics")
    globals_missing = [g for g in getattr(features, "globals_", ())
                       if g not in city.available_globals]
    if not missing and not globals_missing:
        return

    def compatible(candidate) -> bool:
        if candidate.model != experiment.model:
            return False
        if any(getattr(candidate.features, flag, False) and not city.supports(name)
               for flag, name in _FEATURE_FLAGS):
            return False
        if getattr(candidate.graph, "demo", False) and not city.supports("demographics"):
            return False
        return all(g in city.available_globals
                   for g in getattr(candidate.features, "globals_", ()))

    alternatives = sorted(n for n, e in EXPERIMENTS.items()
                          if e.variant in city.variants and compatible(e))
    wanted = ", ".join(missing + [f"{g!r} covariate" for g in globals_missing])
    suggestion = (f"\n  Arms that do run on {city.label}: {', '.join(alternatives[:6])}"
                  if alternatives else "")
    raise SystemExit(
        f"error: experiment {experiment.name!r} needs {wanted}, which {city.label} "
        f"does not have.\n  Available for {city.label}: "
        f"{', '.join(sorted(city.available_features))}"
        f" (globals: {', '.join(city.available_globals)}).{suggestion}"
    )


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


def add_city_arg(parser: argparse.ArgumentParser) -> None:
    """`--city` for the analysis scripts, which do not take add_common_args.

    compare_horizons.py, compare_severity.py, plot_forecasts.py and
    run_rt_diagnostics.py read a results tree rather than training anything, so
    they never wanted the full common block -- and as a result they had no way
    to point at a second city at all. compare_models.py and compare_timing.py
    did take --city, but used it only to relabel rows, which meant
    `--city columbus` silently read Boston's numbers under Columbus's labels.
    """
    parser.add_argument("--city", choices=city_names(), default=DEFAULT_CITY,
                        help="Which city's results to read. Sets the default "
                             "--results-dir; an explicit path still wins.")


def city_results_dir(args: argparse.Namespace, city, *,
                     attr: str = "results_dir") -> Path:
    """The results root to read, honouring an explicit --results-dir.

    Same rule as city_output_dirs: the city segment is applied only when the
    argument is still at its default, so every existing invocation that passes
    a horizon directory explicitly keeps working untouched.
    """
    value = getattr(args, attr)
    if value is None or value == paths.RESULTS_DIR:
        return paths.city_root(city.name)
    return value
