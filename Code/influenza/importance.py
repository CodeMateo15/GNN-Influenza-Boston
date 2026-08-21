"""Permutation feature importance, on one axis every model shares.

The project's existing answer to "which features matter?" is to retrain without
them -- that is what the `gnn_multiedge_covid_rsv` and `gnn_multiedge_rt`
registry arms are. Retraining is the rigorous answer, but it costs a run per
question and it cannot say anything about an *individual* forecast. This module
adds the cheap complement: shuffle a feature in the already-trained model and
measure how much worse the test forecasts get.

Every model is reduced to one `Predictor` interface expressed in `build_samples`
coordinates, so `flu_lag3` means the same column whether the model behind it is
a graph convolution, a dual-topology stack or an LSTM. That is what makes the
resulting CSVs comparable across architectures rather than three separate
vocabularies.

Two properties of this data make a naive permutation study lie, and both are
handled here rather than left for the reader to notice:

  * **Static features do not vary across origins.** The 8 demographic columns
    hold the same value for every forecast origin, so shuffling the origin order
    leaves them untouched and reports exactly zero -- which reads as "the model
    ignores demographics" when it means "this experiment cannot see them". Such
    columns are permuted across *nodes* instead, and the axis used is recorded.
  * **Lagged features are near-duplicates.** `flu_lag0` and `flu_lag1` carry
    almost the same information, so permuting either alone barely moves RMSE and
    the flu history looks unimportant. Group permutation -- all 8 lags shuffled
    together under one permutation -- is therefore the headline number, and the
    per-feature rows are explicitly the marginal contribution given the rest.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Protocol

import numpy as np
import pandas as pd

from .constants import N_NEIGH, SEED, STATIC_DEMO_COLS, WEATHER_COLS
from .metrics import metric_values, segment_labels
from .samples import Normalization, Samples

PermuteScheme = Literal["shared", "per_node"]
GROUP_ORDER = ("flu_lags", "wastewater", "covid", "rsv", "rt", "imputed_flag",
               "weather", "demographics", "seasonality", "citywide")

# The calendar columns ride with the city-wide covariates in the tensor, but
# they answer a different question -- "where in the season is the target?"
# rather than "how much flu is around now?" -- and lumping them together would
# hide the one signal the seasonality arm exists to measure.
SEASONALITY_GLOBALS = ("woy_sin", "woy_cos")


class Predictor(Protocol):
    """A trained model reduced to the one thing importance needs.

    `X` is always `(S, n_nodes, n_feat)` in `build_samples` order (lag 0 first),
    even for the LSTM whose native layout is `(S, lookback, N_NEIGH)` with time
    ascending. Adapting inside the adapter rather than at the call site is what
    lets one permutation loop serve every architecture, and what puts `flu_lag3`
    on the same CSV row for all of them.
    """

    def __call__(self, X: np.ndarray, g: np.ndarray, anchors: np.ndarray) -> np.ndarray:
        """-> (S, N_NEIGH, n_horizons) in ILI-rate units per 100,000."""


def _to_level(normalized: np.ndarray, anchors: np.ndarray, norm: Normalization,
              target: str) -> np.ndarray:
    """Model output -> ILI rate per 100,000, mirroring mc_dropout_forward.

    Kept identical to training.mc_dropout_forward's reconstruction (lines
    177-185) so a permutation baseline is on the same scale as metrics.csv.
    """
    if target == "delta":
        normalized = normalized + anchors[:, :, None]
    return np.maximum(0.0, norm.to_level(normalized))


@dataclass
class GCNPredictor:
    """InfluenzaGNN in eval mode (dropout off, so the mapping is deterministic)."""

    model: object
    edge_index: object
    edge_weight: object
    norm: Normalization
    target: str
    device: object
    n_neigh: int = N_NEIGH

    def __call__(self, X: np.ndarray, g: np.ndarray, anchors: np.ndarray) -> np.ndarray:
        import torch

        self.model.eval()
        out = []
        with torch.no_grad():
            for row in range(X.shape[0]):
                x_t = torch.tensor(X[row], dtype=torch.float32, device=self.device)
                g_t = torch.tensor(g[row], dtype=torch.float32, device=self.device)
                pred = self.model(x_t, self.edge_index, g_t, self.edge_weight)
                out.append(pred[:self.n_neigh].cpu().numpy())
        return _to_level(np.stack(out), anchors, self.norm, self.target)


@dataclass
class DualTopoPredictor:
    """DualTopoSTGCN. Reverses the lag axis, as run_dualtopo.to_sequence does."""

    model: object
    a_geo: object
    a_corr: object
    norm: Normalization
    target: str
    device: object
    batch_size: int = 64
    n_neigh: int = N_NEIGH

    def __call__(self, X: np.ndarray, g: np.ndarray, anchors: np.ndarray) -> np.ndarray:
        import torch

        self.model.eval()
        # (S, nodes, lookback) -> (S, 1, nodes, lookback) with time ascending.
        sequence = np.ascontiguousarray(X[:, None, :, ::-1])
        out = []
        with torch.no_grad():
            for start in range(0, sequence.shape[0], self.batch_size):
                chunk = torch.tensor(sequence[start:start + self.batch_size],
                                     dtype=torch.float32, device=self.device)
                pred = self.model(chunk, self.a_geo, self.a_corr)
                out.append(pred[:, :self.n_neigh].cpu().numpy())
        return _to_level(np.concatenate(out), anchors, self.norm, self.target)


@dataclass
class LSTMPredictor:
    """MultivariateLSTM. Consumes the 14 flu-lag series only, time ascending."""

    model: object
    norm: Normalization
    target: str
    device: object
    lookback: int
    n_horizons: int
    n_neigh: int = N_NEIGH

    def __call__(self, X: np.ndarray, g: np.ndarray, anchors: np.ndarray) -> np.ndarray:
        import torch

        self.model.eval()
        # (S, nodes, feat) -> (S, lookback, N_NEIGH), oldest week first.
        window = X[:, :self.n_neigh, :self.lookback][:, :, ::-1]
        sequence = np.ascontiguousarray(window.transpose(0, 2, 1))
        with torch.no_grad():
            tensor = torch.tensor(sequence, dtype=torch.float32, device=self.device)
            pred = self.model(tensor).cpu().numpy()
        # MultivariateLSTM emits (S, n_horizons, n_inputs) -- horizons before
        # nodes, the opposite of every other model here. Transpose, do not
        # reshape: reshaping would silently interleave the two axes.
        return _to_level(pred.transpose(0, 2, 1), anchors, self.norm, self.target)


def feature_groups(feature_names: list[str], global_names: list[str]) -> dict[str, list[str]]:
    """Bucket columns into the groups worth permuting together.

    Matched on the name prefixes `samples._feature_names` emits, so a new lagged
    source lands in the right bucket without an edit here.
    """
    groups: dict[str, list[str]] = {}
    for name in feature_names:
        base = name.rsplit("_lag", 1)[0] if "_lag" in name else name
        if base == "flu":
            key = "flu_lags"
        elif base.startswith("ww_"):
            key = "wastewater"
        elif base.startswith("covid_"):
            key = "covid"
        elif base.startswith("rsv_"):
            key = "rsv"
        elif base == "rt":
            key = "rt"
        elif base == "flu_imputed":
            key = "imputed_flag"
        elif name in WEATHER_COLS:
            key = "weather"
        elif name in STATIC_DEMO_COLS:
            key = "demographics"
        else:
            key = "other"
        groups.setdefault(key, []).append(name)
    for name in global_names:
        key = "seasonality" if name in SEASONALITY_GLOBALS else "citywide"
        groups.setdefault(key, []).append(name)
    order = {name: index for index, name in enumerate(GROUP_ORDER)}
    return {key: groups[key] for key in sorted(groups, key=lambda k: order.get(k, 99))}


@dataclass(frozen=True)
class PermutationSpec:
    n_repeats: int = 20
    seed: int = SEED
    scheme: PermuteScheme = "shared"


@dataclass
class _Target:
    """One thing to permute: a group, a single feature, or a global column."""

    scope: Literal["group", "feature", "global"]
    name: str
    group: str
    node_columns: list[int] = field(default_factory=list)
    global_columns: list[int] = field(default_factory=list)


def _build_targets(samples: Samples, groups: dict[str, list[str]]) -> list[_Target]:
    feature_index = {name: i for i, name in enumerate(samples.feature_names)}
    global_index = {name: i for i, name in enumerate(samples.global_names)}
    targets: list[_Target] = []

    for group, members in groups.items():
        node_columns = [feature_index[m] for m in members if m in feature_index]
        global_columns = [global_index[m] for m in members if m in global_index]
        targets.append(_Target("group", group, group, node_columns, global_columns))

    for group, members in groups.items():
        for member in members:
            if member in feature_index:
                targets.append(_Target("feature", member, group, [feature_index[member]], []))
            elif member in global_index:
                targets.append(_Target("global", member, group, [], [global_index[member]]))
    return targets


def _constant_across_origins(X: np.ndarray, columns: list[int]) -> bool:
    """True when every listed column is identical for every forecast origin.

    The 8 static demographics are exactly this, and shuffling the origin order
    would leave them bit-identical -- a measured zero that means "not measurable
    this way", not "not used".
    """
    if not columns:
        return False
    block = X[:, :, columns]
    return bool(np.all(block == block[0][None, ...]))


def _permute(X: np.ndarray, g: np.ndarray, target: _Target, rng: np.random.Generator,
             *, scheme: PermuteScheme, by_node: bool) -> tuple[np.ndarray, np.ndarray, str]:
    X_out, g_out = X.copy(), g.copy()
    n_samples, n_nodes = X.shape[0], X.shape[1]

    if by_node:
        # A static covariate's null is "does the model use *whose* it is?",
        # which is a shuffle across nodes within each origin.
        for row in range(n_samples):
            order = rng.permutation(n_nodes)
            X_out[row][:, target.node_columns] = X[row][order][:, target.node_columns]
        axis = "nodes"
    elif scheme == "shared":
        # One permutation of the origin order, applied identically to every
        # node: the sample unit is a forecast origin, and permuting per node
        # would additionally destroy the within-week spatial pattern, which is a
        # different question and invents neighborhood combinations never seen.
        order = rng.permutation(n_samples)
        if target.node_columns:
            X_out[:, :, target.node_columns] = X[order][:, :, target.node_columns]
        if target.global_columns:
            g_out[:, target.global_columns] = g[order][:, target.global_columns]
        axis = "origins"
    else:
        for node in range(n_nodes):
            order = rng.permutation(n_samples)
            if target.node_columns:
                X_out[:, node, target.node_columns] = X[order][:, node, target.node_columns]
        if target.global_columns:
            g_out[:, target.global_columns] = g[rng.permutation(n_samples)][:, target.global_columns]
        axis = "origins_per_node"

    return X_out, g_out, axis


def _rmse_by_segment(actual: np.ndarray, predicted: np.ndarray,
                     segments: np.ndarray, horizons: np.ndarray) -> dict[tuple[str, int], float]:
    """Masked RMSE per (segment, horizon), via the project's own metric code.

    Calling metric_values rather than a local sqrt-mean keeps the NaN-dropping
    convention byte-identical to metrics.csv, so a baseline here is directly
    comparable to a number in the leaderboard.
    """
    out: dict[tuple[str, int], float] = {}
    for horizon in np.unique(horizons):
        at_h = horizons == horizon
        for segment in ("overall", "flu_season", "off_season"):
            mask = at_h if segment == "overall" else (at_h & (segments == segment))
            if not mask.any():
                continue
            out[(segment, int(horizon))] = metric_values(actual[mask], predicted[mask])["RMSE"]
    return out


def permutation_importance(
    predictor: Predictor,
    samples: Samples,
    actual: np.ndarray,
    target_dates: np.ndarray,
    horizons: tuple[int, ...],
    *,
    spec: PermutationSpec,
    groups: dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    """How much worse the forecasts get when a feature is shuffled.

    `actual` is (S, N_NEIGH, n_horizons) in rate units with NaN where BPHC
    suppressed the week; `target_dates` is the same shape, used only to split
    the rows into flu-season and off-season without re-running the model.
    """
    groups = groups or feature_groups(samples.feature_names, samples.global_names)
    targets = _build_targets(samples, groups)

    flat_actual = actual.ravel()
    segments = segment_labels(pd.to_datetime(target_dates.ravel()))
    horizon_grid = np.broadcast_to(np.asarray(horizons), actual.shape).ravel()

    baseline_pred = predictor(samples.X, samples.g, samples.anchors)
    baseline = _rmse_by_segment(flat_actual, baseline_pred.ravel(), segments, horizon_grid)

    records: list[dict] = []
    for index, target in enumerate(targets):
        by_node = _constant_across_origins(samples.X, target.node_columns) \
            and not target.global_columns
        scores: dict[tuple[str, int], list[float]] = {}
        axis = "origins"
        for repeat in range(spec.n_repeats):
            # Seeded per (target, repeat) so re-running one feature reproduces
            # the sweep's numbers exactly, rather than depending on call order.
            rng = np.random.default_rng([spec.seed, index, repeat])
            X_p, g_p, axis = _permute(samples.X, samples.g, target, rng,
                                      scheme=spec.scheme, by_node=by_node)
            predicted = predictor(X_p, g_p, samples.anchors).ravel()
            for key, value in _rmse_by_segment(flat_actual, predicted, segments,
                                               horizon_grid).items():
                scores.setdefault(key, []).append(value)

        for (segment, horizon), values in scores.items():
            base = baseline[(segment, horizon)]
            mean = float(np.mean(values))
            records.append({
                "scope": target.scope,
                "name": target.name,
                "group": target.group,
                "segment": segment,
                "horizon": horizon,
                "permutation_axis": axis,
                "n_columns": len(target.node_columns) + len(target.global_columns),
                "baseline_RMSE": base,
                "permuted_RMSE_mean": mean,
                "permuted_RMSE_std": float(np.std(values)),
                "delta_RMSE": mean - base,
                "delta_RMSE_pct": (mean - base) / base * 100 if base else np.nan,
                "n_repeats": spec.n_repeats,
            })

    frame = pd.DataFrame(records)
    frame["rank"] = (frame.groupby(["scope", "segment", "horizon"])["delta_RMSE"]
                     .rank(ascending=False, method="min").astype(int))
    return frame.sort_values(["scope", "segment", "horizon", "delta_RMSE"],
                             ascending=[True, True, True, False]).reset_index(drop=True)
