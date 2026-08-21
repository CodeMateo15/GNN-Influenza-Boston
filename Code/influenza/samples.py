"""Turning the aligned weekly tables into model tensors.

One sample per forecast origin t: node features from the lookback window ending
at t, city-wide covariates at t, and targets at t+h for each horizon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from .config import FeatureSpec
from .constants import N_NEIGH, WEATHER_COLS
from .data import impute_causal
from .graphs import Graph
from .windows import Split, Window, normalization

# Anchor nodes carry no data. Temporal features are zero and static features sit
# at the midpoint of the normalised range, so an anchor is a neutral boundary
# sink whose only distinguishing property is which neighborhoods it borders.
ANCHOR_STATIC_VALUE = 0.5


@dataclass
class Dataset:
    """Every aligned input table, on one common weekly index."""

    week_index: pd.DatetimeIndex
    rates: pd.DataFrame                       # raw, NaN where suppressed
    flu_features: pd.DataFrame                # causally imputed
    flu_imputed: pd.DataFrame                 # bool mask
    weather: dict[str, np.ndarray]
    static: np.ndarray | None
    globals_: pd.DataFrame                    # (weeks, n_global)
    per_node: dict[str, pd.DataFrame]         # extra per-neighborhood features
    mbta: np.ndarray | None = None


@dataclass
class Normalization:
    flu_mean: np.ndarray
    flu_std: np.ndarray

    def to_level(self, values: np.ndarray) -> np.ndarray:
        return values * self.flu_std.flatten()[None, :, None] + self.flu_mean.flatten()[None, :, None]


@dataclass
class Samples:
    X: np.ndarray            # (S, n_nodes, n_feat)
    g: np.ndarray            # (S, n_global)
    y: np.ndarray            # (S, N_NEIGH, n_horizons) -- NaN where suppressed
    anchors: np.ndarray      # (S, N_NEIGH) normalized level at origin
    positions: list[int]
    feature_names: list[str]
    global_names: list[str]

    @property
    def n_feat(self) -> int:
        return self.X.shape[2]

    @property
    def n_global(self) -> int:
        return self.g.shape[1]

    def subset(self, indices: list[int]) -> "Samples":
        return Samples(
            X=self.X[indices], g=self.g[indices], y=self.y[indices],
            anchors=self.anchors[indices],
            positions=[self.positions[i] for i in indices],
            feature_names=self.feature_names, global_names=self.global_names,
        )


def _zscore(values: np.ndarray, *, end: int | None, per_column: bool) -> np.ndarray:
    """Normalise, optionally using only rows up to `end` (leakage-free)."""
    reference = values if end is None else values[:end]
    axis = 0 if per_column else None
    mean = np.nanmean(reference, axis=axis, keepdims=per_column)
    std = np.nanstd(reference, axis=axis, keepdims=per_column) + 1e-8
    return (values - mean) / std


def build_samples(
    dataset: Dataset,
    split: Split,
    features: FeatureSpec,
    window: Window,
    graph: Graph,
    *,
    target: Literal["delta", "level"],
    normalize: Literal["all", "train"],
) -> tuple[Samples, Normalization]:
    """Assemble tensors for every origin in `split`.

    Normalisation reference: `'train'` uses rows up to the last training target
    only. `'all'` reproduces the notebooks, which normalised across the test
    window too -- kept available so parity runs are possible, but it does leak.
    """
    n_weeks = len(dataset.week_index)
    end = None if normalize == "all" else split.train[-1] + window.max_horizon + 1

    flu_mean, flu_std = normalization(dataset.rates, split, mode=normalize)
    flu_features = (dataset.flu_features.to_numpy(dtype=np.float32) - flu_mean) / flu_std
    flu_targets = (dataset.rates.to_numpy(dtype=np.float32) - flu_mean) / flu_std

    # Weather is normalised per neighborhood per column (axis=0), matching the
    # notebook cell that overwrote an earlier global normalisation.
    weather_norm = {
        col: _zscore(dataset.weather[col], end=end, per_column=True)
        for col in WEATHER_COLS
    } if features.use_weather else {}

    per_node_norm = {
        name: _zscore(frame.to_numpy(dtype=np.float32), end=end, per_column=True)
        for name, frame in dataset.per_node.items()
    }
    # Extra per-node sources have their own coverage gaps (no sewershed for
    # Fenway / South Boston / South End); zero after z-scoring is the mean.
    per_node_norm = {name: np.nan_to_num(values) for name, values in per_node_norm.items()}

    global_values = _zscore(dataset.globals_.to_numpy(dtype=np.float32), end=end, per_column=True)
    global_values = np.nan_to_num(global_values)

    # Calendar position rides with the city-wide covariates rather than the node
    # features: it is identical for all 21 nodes, and the GCN's degree-normalised
    # neighbourhood averaging cannot differentiate a constant, so as a node
    # feature it would survive only as a bias term. It would also break
    # run_dualtopo.to_sequence, which asserts n_feat == lookback exactly.
    season_names = ["woy_sin", "woy_cos"] if features.use_seasonality else []

    imputed_mask = dataset.flu_imputed.to_numpy(dtype=np.float32)

    feature_names = _feature_names(features, window, per_node_norm.keys())
    n_feat = len(feature_names)

    positions = split.train + split.val + split.test
    positions = sorted(set(positions))
    n_samples = len(positions)

    X = np.zeros((n_samples, graph.n_nodes, n_feat), dtype=np.float32)
    g = np.zeros((n_samples, global_values.shape[1] + len(season_names)), dtype=np.float32)
    y = np.zeros((n_samples, N_NEIGH, len(window.horizons)), dtype=np.float32)
    anchors = np.zeros((n_samples, N_NEIGH), dtype=np.float32)

    for row, t in enumerate(positions):
        if t - window.lookback + 1 < 0 or t + window.max_horizon >= n_weeks:
            raise ValueError(
                f"Origin {t} ({dataset.week_index[t].date()}) does not have a full "
                f"lookback of {window.lookback} weeks and {window.max_horizon} target "
                "weeks. valid_origins() is the only gatekeeper -- it should have "
                "excluded this position rather than the sample builder clamping it."
            )
        for node in range(N_NEIGH):
            values: list[float] = []
            for lag in range(window.lookback):
                week = t - lag
                values.append(flu_features[week, node])
                for name in per_node_norm:
                    values.append(per_node_norm[name][week, node])
                if features.use_imputed_flag:
                    values.append(imputed_mask[week, node])
            if features.use_weather:
                values.extend(weather_norm[col][t, node] for col in WEATHER_COLS)
            row_values = np.asarray(values, dtype=np.float32)
            if features.use_demographics and dataset.static is not None:
                row_values = np.concatenate([row_values, dataset.static[node]])
            X[row, node] = row_values

        if graph.n_anchors:
            temporal_len = n_feat - (dataset.static.shape[1]
                                     if features.use_demographics and dataset.static is not None
                                     else 0)
            anchor_row = np.zeros(n_feat, dtype=np.float32)
            if features.use_demographics and dataset.static is not None:
                anchor_row[temporal_len:] = ANCHOR_STATIC_VALUE
            X[row, N_NEIGH:] = anchor_row

        if season_names:
            # Keyed to the *target* week, which is known at forecast time and is
            # the week the model is being asked about. Day-of-year rather than
            # ISO week: week 53 exists every five or six years and would put a
            # discontinuity in an otherwise smooth encoding.
            target_week = dataset.week_index[t + window.min_horizon]
            angle = 2.0 * np.pi * target_week.dayofyear / 365.2425
            g[row] = np.concatenate([global_values[t],
                                     [np.sin(angle), np.cos(angle)]]).astype(np.float32)
        else:
            g[row] = global_values[t]
        # The anchor is an INPUT (the level the delta is measured from), so it
        # uses the causally imputed series. Targets stay raw, so a suppressed
        # target is dropped from the loss and metrics -- but a suppressed
        # *origin* week no longer discards an otherwise-scorable target.
        anchors[row] = flu_features[t]
        for h_idx, horizon in enumerate(window.horizons):
            level = flu_targets[t + horizon]
            y[row, :, h_idx] = level - flu_features[t] if target == "delta" else level

    return (
        Samples(X=X, g=g, y=y, anchors=anchors, positions=positions,
                feature_names=feature_names,
                global_names=list(dataset.globals_.columns) + season_names),
        Normalization(flu_mean=flu_mean, flu_std=flu_std),
    )


def _feature_names(features: FeatureSpec, window: Window, per_node: object) -> list[str]:
    names: list[str] = []
    for lag in range(window.lookback):
        names.append(f"flu_lag{lag}")
        for source in per_node:
            names.append(f"{source}_lag{lag}")
        if features.use_imputed_flag:
            names.append(f"flu_imputed_lag{lag}")
    if features.use_weather:
        names.extend(WEATHER_COLS)
    if features.use_demographics:
        from .constants import STATIC_DEMO_COLS
        names.extend(STATIC_DEMO_COLS)
    return names


def positions_to_rows(samples: Samples, positions: list[int]) -> list[int]:
    """Row indices in `samples` for the given origin positions."""
    lookup = {position: row for row, position in enumerate(samples.positions)}
    return [lookup[p] for p in positions]


def load_dataset(features: FeatureSpec, *, rates=None, need_mbta: bool = False) -> Dataset:
    """Load and align only the sources the feature spec actually turns on.

    Keeping this demand-driven is what lets run_arima.py avoid openpyxl and
    run_dualtopo.py avoid the City of Boston files entirely.
    """
    from . import data as data_module

    rates = data_module.load_rates() if rates is None else rates
    week_index = rates.index
    flu_features, flu_imputed = impute_causal(rates)

    weather = data_module.load_weather(week_index) if features.use_weather else {}
    static = data_module.load_static_demographics()[0] if features.use_demographics else None

    per_node: dict[str, pd.DataFrame] = {}
    for source in features.wastewater_sources:
        per_node[f"ww_{source}"] = data_module.load_wastewater(week_index, source)
    if features.use_covid_cases:
        per_node["covid_cases"] = data_module.load_monthly_neighborhood(
            week_index, source="covid_cases", indicator="New Cases")
    if features.use_covid_testing:
        per_node["covid_positivity"] = data_module.load_monthly_neighborhood(
            week_index, source="covid_testing", indicator="Positivity", unit="percent")
    if features.use_rsv_cases:
        per_node["rsv_cases"] = data_module.load_monthly_neighborhood(
            week_index, source="rsv_cases", unit="per 1,000,000 residents")
    if features.use_rt:
        from .rt import weekly_rt
        per_node["rt"] = weekly_rt(rates)

    columns: dict[str, pd.Series] = {}
    if features.globals_:
        ed = data_module.load_ed_metrics(week_index)
        for name in features.globals_:
            if name in ed.columns:
                columns[name] = ed[name]
            elif name == "monthly_cases":
                columns[name] = data_module.load_monthly_cases(week_index)
            elif name == "vaccination":
                columns[name] = data_module.load_vaccination_global(week_index)
            else:
                raise ValueError(f"Unhandled global covariate: {name!r}")
    globals_frame = pd.DataFrame(columns, index=week_index) if columns else pd.DataFrame(index=week_index)

    return Dataset(
        week_index=week_index,
        rates=rates,
        flu_features=flu_features,
        flu_imputed=flu_imputed,
        weather=weather,
        static=static,
        globals_=globals_frame,
        per_node=per_node,
        mbta=data_module.load_mbta_matrix() if need_mbta else None,
    )
