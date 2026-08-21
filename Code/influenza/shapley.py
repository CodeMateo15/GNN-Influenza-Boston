"""SHAP explanations for the graph models, in units a reader can act on.

Permutation importance in `importance.py` answers "which features does this
model rely on, overall?". This answers the narrower and more useful question:
"why did it say *that*, for *that neighborhood*, on *that week*?" -- which is
what a waterfall plot shows.

Three design choices carry the module, each with a cheaper alternative that was
rejected for a stated reason.

**The explained input is every node's features, not just the target's.** A GCN
prediction for Dorchester depends on all 21 nodes through the graph. Explaining
only Dorchester's own columns, with neighbors held at a background value, would
fold the entire graph contribution into the base value -- and whether the graph
earns its keep is precisely the claim this project exists to test (`gnn_uniform`
is the control built to probe it). Expected-gradient cost is O(nsamples) and
independent of input width, so the wide input is free.

**GradientExplainer, never DeepExplainer.** shap's `_PyTorchGradient` is pure
`torch.autograd.grad` and registers no module hooks, so PyG's scatter ops just
work. `PyTorchDeep` instead walks to every leaf module and attaches
`register_full_backward_hook`, including to `GCNConv`'s `SumAggregation`, which
has no `op_handler` entry (silent degradation to plain gradients) and wraps an
in-place `index_add_` (the classic "output is a view and is being modified
inplace" error). KernelExplainer is exposed only as a single-instance
cross-check, since it needs thousands of coalition evaluations per instance.

**Attributions are converted to ILI rate per 100,000.** The conversion is affine
with a strictly positive per-node scale, so Shapley additivity survives exactly,
and the waterfall then reads in the units the forecast is published in rather
than in normalized-delta space.

One consequence that looks like a bug and is not: expected gradients compute
phi ~ (x - x') * E[df/dx], so any column that is *constant across forecast
origins* gets exactly zero. That is all 8 static demographics and every anchor
column. The anchor case is asserted on as a free correctness check of the column
bookkeeping; the demographics case is reported in a footnote, because the only
rigorous test of a static covariate is a retrain ablation.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Literal

import numpy as np
import torch
import torch.nn as nn

from .constants import N_NEIGH
from .samples import Normalization, Samples

Z95 = 1.959964


class GraphBatch(nn.Module):
    """InfluenzaGNN reduced to a plain f(x_flat, g) -> (B, n_neigh * n_horizons).

    The explainer needs a batched, edge-free signature. This closes over the
    trained edge_index / edge_weight and replicates them block-diagonally, so a
    batch of B forecast origins becomes one disjoint graph of B * n_nodes nodes.
    GCNConv's symmetric normalisation is degree-based and strictly local, so each
    block reproduces the single-graph forward exactly -- which `check_batching`
    asserts before any SHAP value is computed.
    """

    def __init__(self, model: nn.Module, edge_index: torch.Tensor,
                 edge_weight: torch.Tensor, *, n_nodes: int, n_feat: int,
                 n_neigh: int = N_NEIGH) -> None:
        super().__init__()
        self.model = model
        self.register_buffer("_edge_index", edge_index)
        self.register_buffer("_edge_weight", edge_weight)
        self.n_nodes = n_nodes
        self.n_feat = n_feat
        self.n_neigh = n_neigh
        self._cache: dict[int, tuple[torch.Tensor, torch.Tensor]] = {}

    def _batched_edges(self, batch: int) -> tuple[torch.Tensor, torch.Tensor]:
        if batch not in self._cache:
            offsets = (torch.arange(batch, device=self._edge_index.device)
                       * self.n_nodes).repeat_interleave(self._edge_index.size(1))
            index = self._edge_index.repeat(1, batch) + offsets
            weight = self._edge_weight.repeat(batch)
            self._cache[batch] = (index, weight)
        return self._cache[batch]

    def forward(self, x_flat: torch.Tensor, g: torch.Tensor) -> torch.Tensor:
        batch = x_flat.shape[0]
        x = x_flat.reshape(batch * self.n_nodes, self.n_feat)
        index, weight = self._batched_edges(batch)

        import torch.nn.functional as F

        h = F.relu(self.model.gcn1(x, index, weight))
        h = F.relu(self.model.gcn2(h, index, weight))
        if g.numel():
            h = torch.cat([h, g.repeat_interleave(self.n_nodes, dim=0)], dim=1)
        out = self.model.output(F.relu(self.model.fusion(h)))
        return out.reshape(batch, self.n_nodes, -1)[:, :self.n_neigh].reshape(batch, -1)


@dataclass
class ShapResult:
    """SHAP attributions for one horizon, in the units named by `units`."""

    values: np.ndarray            # (S, n_neigh, D)
    variances: np.ndarray         # (S, n_neigh, D) -- Monte Carlo error
    base_values: np.ndarray       # (S, n_neigh)
    data: np.ndarray              # (S, D) the flattened, z-scored inputs
    column_names: list[str]       # "Dorchest.|flu_lag0", "city|ili_count"
    node_of_column: np.ndarray    # (D,) node index; -1 for globals
    feature_of_column: np.ndarray # (D,) index into feature_names; -1 for globals
    horizon: int
    origin_dates: np.ndarray
    units: Literal["normalized_delta", "rate_per_100k"]

    @property
    def anchor_columns(self) -> np.ndarray:
        return np.flatnonzero(self.node_of_column >= N_NEIGH)


def flatten_inputs(samples: Samples) -> tuple[np.ndarray, np.ndarray]:
    """(S, n_nodes*n_feat) node block and (S, n_global) globals."""
    return (samples.X.reshape(samples.X.shape[0], -1).astype(np.float32),
            samples.g.astype(np.float32))


def column_metadata(samples: Samples, node_names: list[str]) -> tuple[list[str], np.ndarray, np.ndarray]:
    """Names and provenance for the flattened (nodes x features) + globals axis."""
    names: list[str] = []
    node_of: list[int] = []
    feature_of: list[int] = []
    for node, node_name in enumerate(node_names):
        for feature, feature_name in enumerate(samples.feature_names):
            names.append(f"{node_name}|{feature_name}")
            node_of.append(node)
            feature_of.append(feature)
    for global_name in samples.global_names:
        names.append(f"city|{global_name}")
        node_of.append(-1)
        feature_of.append(-1)
    return names, np.asarray(node_of), np.asarray(feature_of)


def check_batching(wrapper: GraphBatch, model: nn.Module, samples: Samples,
                   edge_index: torch.Tensor, edge_weight: torch.Tensor,
                   device: torch.device, *, n_check: int = 4) -> float:
    """Max abs difference between the batched wrapper and the per-sample forward.

    If this is not ~0 the block-diagonal replication is wrong and every SHAP
    value downstream is meaningless, so the caller treats it as a hard failure.
    """
    model.eval()
    rows = min(n_check, samples.X.shape[0])
    x_flat, g = flatten_inputs(samples)
    with torch.no_grad():
        batched = wrapper(
            torch.tensor(x_flat[:rows], device=device),
            torch.tensor(g[:rows], device=device),
        ).cpu().numpy()
        single = []
        for row in range(rows):
            out = model(torch.tensor(samples.X[row], device=device), edge_index,
                        torch.tensor(samples.g[row], device=device), edge_weight)
            single.append(out[:wrapper.n_neigh].cpu().numpy().reshape(-1))
    return float(np.max(np.abs(batched - np.stack(single))))


def explain(
    wrapper: GraphBatch,
    background: Samples,
    explain_set: Samples,
    *,
    horizon_index: int,
    n_horizons: int,
    device: torch.device,
    nsamples: int = 200,
    batch_size: int = 64,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Expected-gradient attributions -> (values, variances, base_values).

    values/variances are (S, n_neigh, D); base_values is (n_neigh,) -- the mean
    prediction over the background set, which GradientExplainer does not provide
    (shap leaves `expected_value` unset for it) and which must be computed here.
    """
    import shap

    bg_x, bg_g = flatten_inputs(background)
    ex_x, ex_g = flatten_inputs(explain_set)
    bg = [torch.tensor(bg_x, device=device), torch.tensor(bg_g, device=device)]
    ex = [torch.tensor(ex_x, device=device), torch.tensor(ex_g, device=device)]

    explainer = shap.GradientExplainer(wrapper, bg, batch_size=batch_size)
    raw, variances = explainer.shap_values(ex, nsamples=nsamples, rseed=seed,
                                           return_variances=True)

    def select(combined: np.ndarray) -> np.ndarray:
        """(S, D, n_outputs) -> (S, n_neigh, D) for the requested horizon."""
        n_neigh = combined.shape[2] // n_horizons
        reshaped = combined.reshape(combined.shape[0], combined.shape[1], n_neigh, n_horizons)
        return np.transpose(reshaped[:, :, :, horizon_index], (0, 2, 1))

    # shap returns the two quantities in different nestings: values as one array
    # per *input* with the outputs on the last axis, variances as a list per
    # *output* of a list per input. Normalising both to (S, D, n_outputs) here
    # keeps the difference from leaking into the rest of the module.
    values = select(np.concatenate([np.asarray(p) for p in raw], axis=1))
    variance_stack = np.stack(
        [np.concatenate([np.asarray(p) for p in per_output], axis=1)
         for per_output in variances],
        axis=-1,
    )
    variances_out = select(variance_stack)

    with torch.no_grad():
        base = wrapper(bg[0], bg[1]).mean(dim=0).cpu().numpy()
    base = base.reshape(-1, n_horizons)[:, horizon_index]

    return values, variances_out, base


def to_rate_units(values: np.ndarray, base: np.ndarray, anchors: np.ndarray,
                  norm: Normalization, target: str) -> tuple[np.ndarray, np.ndarray]:
    """Rescale attributions from model space to ILI per 100,000.

    Affine with a strictly positive per-node scale (`normalization` adds 1e-8 to
    every std), so `base + sum(phi)` still equals the prediction exactly.

    For a delta target the base absorbs the origin-week level, which varies by
    sample -- so base_values becomes (S, n_neigh) and must not be averaged.
    """
    scale = norm.flu_std.flatten()[None, :, None]          # (1, n_neigh, 1)
    offset = norm.flu_mean.flatten()[None, :]              # (1, n_neigh)
    scaled = values * scale
    base_rate = base[None, :] * norm.flu_std.flatten()[None, :] + offset
    if target == "delta":
        anchor_level = anchors * norm.flu_std.flatten()[None, :] + offset
        # The base is "the average predicted change" plus "where we started".
        base_rate = base[None, :] * norm.flu_std.flatten()[None, :] + anchor_level
    return scaled, np.broadcast_to(base_rate, (values.shape[0], values.shape[1])).copy()


def locality_of(node: int, target_node: int, weights: np.ndarray) -> str:
    """How a node relates to the one being explained, per the trained graph."""
    if node < 0:
        return "citywide"  # source_of already separates seasonality from the rest
    if node == target_node:
        return "own"
    if node >= N_NEIGH:
        return "anchor"
    return "connected" if weights[target_node, node] > 0 else "unconnected"


LOCALITIES = ("own", "connected", "unconnected", "anchor")


def group_labels(result: ShapResult, source_of: dict[str, str]) -> list[str]:
    """The canonical 'source - locality' label list, shared by every target node.

    Built from the full cross product rather than from whatever one node happens
    to have, because a node connected to all its peers has no 'unconnected'
    bucket and a per-node list would not line up with its neighbours' -- which
    is exactly what makes the pooled beeswarm incoherent.
    """
    sources: list[str] = []
    for column, name in enumerate(result.column_names):
        if result.node_of_column[column] < 0:
            continue  # citywide covariates have no locality; they are one bucket
        source = source_of.get(name.split("|", 1)[1], "other")
        if source not in sources:
            sources.append(source)
    city = []
    for column, name in enumerate(result.column_names):
        if result.node_of_column[column] < 0:
            source = source_of.get(name.split("|", 1)[1], "citywide")
            if source not in city:
                city.append(source)
    labels = [f"{source} — {place}" for source in sources for place in LOCALITIES]
    return labels + city


def group_columns(result: ShapResult, target_node: int, weights: np.ndarray,
                  source_of: dict[str, str],
                  labels: list[str] | None = None) -> tuple[list[str], np.ndarray]:
    """Map every column to a 'source - locality' bucket.

    Shapley values are additive, so summing the members of a disjoint set keeps
    `base + sum(groups) == prediction`. (A sum of members is not in general the
    Shapley value of a merged player in the collapsed game -- that would be an
    Owen value -- but it is the standard aggregation and it is what makes a
    plot with 462 columns readable.)
    """
    labels = labels if labels is not None else group_labels(result, source_of)
    lookup = {label: i for i, label in enumerate(labels)}
    index = np.zeros(len(result.column_names), dtype=int)
    for column, name in enumerate(result.column_names):
        node = int(result.node_of_column[column])
        source = source_of.get(name.split("|", 1)[1], "other")
        place = locality_of(node, target_node, weights)
        # City-wide columns keep their source name (citywide / seasonality);
        # only per-node columns get a locality suffix.
        label = source if place == "citywide" else f"{source} — {place}"
        index[column] = lookup[label]
    return labels, index


def aggregate(values: np.ndarray, group_index: np.ndarray, n_groups: int) -> np.ndarray:
    """Sum attributions within each group along the last axis."""
    out = np.zeros((*values.shape[:-1], n_groups), dtype=values.dtype)
    np.add.at(out, (..., group_index), values)
    return out


@contextlib.contextmanager
def shap_style():
    """Use the project palette inside shap's plots when its style API exists.

    `shap.plots._style` is private and not re-exported, so this is best-effort:
    a version without it still produces correct figures, just in shap's colours.
    """
    try:
        from shap.plots._style import get_style, set_style
    except ImportError:
        yield
        return

    from . import palette

    style = get_style()
    previous = {name: getattr(style, name, None)
                for name in ("primary_color_positive", "primary_color_negative",
                             "text_color", "tick_labels_color")}
    try:
        style.primary_color_positive = palette.SERIES[1]
        style.primary_color_negative = palette.SERIES[0]
        style.text_color = palette.INK_PRIMARY
        style.tick_labels_color = palette.INK_MUTED
        set_style(style)
        yield
    finally:
        for name, value in previous.items():
            if value is not None:
                setattr(style, name, value)
        set_style(style)
