"""Turning the aligned weekly tables into model tensors.

One sample per forecast origin t: node features from the lookback window ending
at t, city-wide covariates at t, and targets at t+h for each horizon.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd

from .cities import City, get as get_city
from .config import FeatureSpec
from .constants import WEATHER_COLS
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
    city: City | None = None
    # Names of the columns in `static`, in order. Not always STATIC_DEMO_COLS:
    # Buenos Aires publishes five of the eight, so the static block is narrower
    # there and the feature names have to say which five.
    static_cols: tuple[str, ...] = ()


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
    y: np.ndarray            # (S, n_neigh, n_horizons) -- NaN where suppressed
    anchors: np.ndarray      # (S, n_neigh) normalized level at origin
    positions: list[int]
    feature_names: list[str]
    global_names: list[str]
    # (S, n_neigh) normalized per-week slope of the recent history at the origin,
    # in the same units as `anchors`. A least-squares slope over TREND_WEEKS, not
    # a single difference: one week's difference is mostly Poisson noise and BPHC
    # suppression, and extrapolating it directly measured WORSE at every weight
    # tried. `trendblend` is the only consumer.
    trend: np.ndarray | None = None
    # Normalised seasonal baseline at each TARGET week, (S, n_neigh, n_horizons).
    # The second of the two baselines the blended target is measured from; unlike
    # `anchors` it does not decay as the horizon grows.
    clim: np.ndarray | None = None
    # How the flattened feature axis decomposes. The temporal block is the first
    # `lookback * temporal_channels` columns, lag-major and most-recent-first;
    # everything after it is static within a sample. SpatioTemporalGNN needs this
    # to reshape a sequence back out of the flat vector.
    lookback: int = 0
    temporal_channels: int = 0

    @property
    def n_feat(self) -> int:
        return self.X.shape[2]

    @property
    def n_global(self) -> int:
        return self.g.shape[1]

    @property
    def n_static_feat(self) -> int:
        return self.n_feat - self.lookback * self.temporal_channels

    def subset(self, indices: list[int]) -> "Samples":
        return Samples(
            X=self.X[indices], g=self.g[indices], y=self.y[indices],
            anchors=self.anchors[indices],
            trend=None if self.trend is None else self.trend[indices],
            positions=[self.positions[i] for i in indices],
            feature_names=self.feature_names, global_names=self.global_names,
            clim=None if self.clim is None else self.clim[indices],
            lookback=self.lookback, temporal_channels=self.temporal_channels,
        )


# Weeks of history the trend is fitted over. Three is the shortest window that
# averages out a single suppressed or spiky week; the slope is only ever used
# scaled by a learned coefficient, so the exact choice is not load-bearing.
TREND_WEEKS = 3


def _recent_slope(series: np.ndarray, origin: int, weeks: int) -> np.ndarray:
    """Per-week least-squares slope of the `weeks` values ending at `origin`.

    A fitted slope rather than `series[t] - series[t-1]`: the single difference
    is dominated by weekly Poisson noise and by BPHC suppression, and adding it
    to the forecast directly made the typical weekly miss worse at every weight
    tried (19.1 -> 20.5 -> 24.0 per 100,000 as the weight went 0 -> 0.5 -> 1.0).
    Reads only weeks at or before the origin, all of which the lag block already
    reads, so it introduces no new information and no look-ahead.
    """
    start = max(origin - weeks + 1, 0)
    rows = series[start:origin + 1]
    n = len(rows)
    if n < 2:
        return np.zeros(series.shape[1], dtype=np.float32)
    time = np.arange(n, dtype=np.float32)
    centred = time - time.mean()
    denominator = float((centred ** 2).sum())
    slope = (centred[:, None] * (rows - rows.mean(axis=0, keepdims=True))).sum(axis=0)
    return (slope / denominator).astype(np.float32)


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
    target: Literal["delta", "level", "blend", "trendblend", "cascade"],
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

    # Seasonal baseline, fitted on exactly the rows the normalisation reference
    # uses, so the two share one leakage boundary rather than each choosing its
    # own. Held in NORMALISED units because that is the space the targets and the
    # origin-level anchors live in.
    from .climatology import fit_climatology
    climatology = fit_climatology(dataset.rates, end=end)
    clim_level = (climatology.level(dataset.week_index) - flu_mean) / flu_std

    feature_names = _feature_names(features, window, per_node_norm.keys(),
                                   dataset.static_cols)
    n_feat = len(feature_names)

    positions = split.train + split.val + split.test
    positions = sorted(set(positions))
    n_samples = len(positions)

    # The graph is the authority on how many nodes are scored: it already
    # carried n_neigh as a field, so this reads it rather than a module global.
    n_neigh = graph.n_neigh

    X = np.zeros((n_samples, graph.n_nodes, n_feat), dtype=np.float32)
    g = np.zeros((n_samples, global_values.shape[1] + len(season_names)), dtype=np.float32)
    y = np.zeros((n_samples, n_neigh, len(window.horizons)), dtype=np.float32)
    anchors = np.zeros((n_samples, n_neigh), dtype=np.float32)
    trends = np.zeros((n_samples, n_neigh), dtype=np.float32)
    clim = np.zeros((n_samples, n_neigh, len(window.horizons)), dtype=np.float32)

    for row, t in enumerate(positions):
        if t - window.lookback + 1 < 0 or t + window.max_horizon >= n_weeks:
            raise ValueError(
                f"Origin {t} ({dataset.week_index[t].date()}) does not have a full "
                f"lookback of {window.lookback} weeks and {window.max_horizon} target "
                "weeks. valid_origins() is the only gatekeeper -- it should have "
                "excluded this position rather than the sample builder clamping it."
            )
        for node in range(n_neigh):
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
            X[row, n_neigh:] = anchor_row

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
        # Same causally imputed series and the same weeks the lag block reads,
        # so this adds no input the model did not already have -- it only makes
        # the slope available to the baseline as well as to the network.
        trends[row] = _recent_slope(flu_features, t, TREND_WEEKS)
        for h_idx, horizon in enumerate(window.horizons):
            level = flu_targets[t + horizon]
            y[row, :, h_idx] = level - flu_features[t] if target == "delta" else level
            # Keyed to the target week, which is known at forecast time -- the
            # calendar is not a prediction. Same argument as use_seasonality.
            clim[row, :, h_idx] = clim_level[t + horizon, :n_neigh]

    return (
        Samples(X=X, g=g, y=y, anchors=anchors, trend=trends, positions=positions,
                feature_names=feature_names,
                global_names=list(dataset.globals_.columns) + season_names,
                clim=clim, lookback=window.lookback,
                temporal_channels=_temporal_channels(features, per_node_norm.keys())),
        Normalization(flu_mean=flu_mean, flu_std=flu_std),
    )


def _temporal_channels(features: FeatureSpec, per_node: object) -> int:
    """How many values `_feature_names` emits per lag.

    Must stay in lockstep with the per-lag block in `_feature_names` and the
    writer loop in `build_samples`: flu rate, then one column per extra per-node
    source, then optionally the imputation flag.
    """
    return 1 + len(list(per_node)) + (1 if features.use_imputed_flag else 0)


def _feature_names(features: FeatureSpec, window: Window, per_node: object,
                   static_cols: tuple[str, ...] = ()) -> list[str]:
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
        # The columns the loader actually returned, not the global list: a city
        # with fewer published demographics has a narrower static block, and
        # labelling it with all eight names would misalign every name after the
        # first missing one.
        from .constants import STATIC_DEMO_COLS
        names.extend(static_cols or STATIC_DEMO_COLS)
    return names


def positions_to_rows(samples: Samples, positions: list[int]) -> list[int]:
    """Row indices in `samples` for the given origin positions."""
    lookup = {position: row for row, position in enumerate(samples.positions)}
    return [lookup[p] for p in positions]


def load_dataset(features: FeatureSpec, *, city: City | None = None,
                 rates=None) -> Dataset:
    """Load and align only the sources the feature spec actually turns on.

    Keeping this demand-driven is what lets run_arima.py avoid openpyxl and
    run_dualtopo.py avoid the City of Boston files entirely.

    `city` selects the loader module. It defaults to Boston so that every
    pre-existing call site keeps its exact behaviour; the model scripts pass it
    explicitly from --city.
    """
    city = city or get_city("boston")
    data_module = city.loaders

    rates = data_module.load_rates() if rates is None else rates
    week_index = rates.index
    flu_features, flu_imputed = impute_causal(rates)

    weather = data_module.load_weather(week_index) if features.use_weather else {}
    static, static_cols = None, ()
    if features.use_demographics:
        static, cols, _ = data_module.load_static_demographics()
        static_cols = tuple(cols)

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

    unknown = [n for n in features.globals_ if n not in city.available_globals]
    if unknown:
        raise ValueError(
            f"{city.label} has no city-wide covariate(s) {unknown}. Available for "
            f"{city.label}: {', '.join(city.available_globals)}. Requesting an absent "
            "covariate would z-score an all-NaN column to zeros and train the model "
            "on a constant, which reads as a null result rather than a missing input."
        )
    globals_frame = data_module.load_globals(week_index, features.globals_)

    return Dataset(
        week_index=week_index,
        rates=rates,
        flu_features=flu_features,
        flu_imputed=flu_imputed,
        weather=weather,
        static=static,
        globals_=globals_frame,
        per_node=per_node,
        city=city,
        static_cols=static_cols,
    )
