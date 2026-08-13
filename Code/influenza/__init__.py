"""Shared library for the Boston neighborhood influenza forecasting project.

Entry-point scripts live one level up in Code/ so that `python Code/run_gnn.py`
works from any working directory without sys.path manipulation.

Typical use from a model script:

    from influenza import (
        NEIGHBORHOODS, Window, load_rates, variant_data, valid_origins,
        split_origins, finish_run, track_emissions,
    )
"""

from __future__ import annotations

from . import paths
from .artifacts import finish_run, run_dir
from .carbon import EmissionsSummary, track_emissions
from .constants import (
    FLU_MONTHS,
    HORIZONS,
    LOOKBACK,
    NEIGHBORHOODS,
    N_NEIGH,
    SEED,
    SEGMENTS,
    SHORT_NAMES,
    TEST_END,
    TEST_START,
)
from .data import coverage_report, impute_causal, load_rates, neighborhood_index
from .metrics import CORE_METRICS, build_metrics, metric_values, summary_table
from .plots import save_grid_plot, save_loss_curve
from .windows import (
    Split,
    VariantData,
    Window,
    normalization,
    split_origins,
    valid_origins,
    variant_data,
)

__all__ = [
    "CORE_METRICS", "EmissionsSummary", "FLU_MONTHS", "HORIZONS", "LOOKBACK",
    "NEIGHBORHOODS", "N_NEIGH", "SEED", "SEGMENTS", "SHORT_NAMES", "Split",
    "TEST_END", "TEST_START", "VariantData", "Window", "build_metrics",
    "coverage_report", "finish_run", "impute_causal", "load_rates",
    "metric_values", "neighborhood_index", "normalization", "paths", "run_dir",
    "save_grid_plot", "save_loss_curve", "split_origins", "summary_table",
    "track_emissions", "valid_origins", "variant_data",
]
