"""Model architectures.

`SpatioTemporalGNN` is the project's current design. `InfluenzaGNN` is the
earlier one it replaces, kept so pre-existing checkpoints still load.

`DualTopoSTGCN` reimplements Luo et al. (2025), BMC Public Health 25:408. It is
deliberately written without torch_geometric -- dense einsum message passing
means the paper model runs on a machine that only has torch installed. It is the
reference the project measures itself against and is not to be modified.

Every model here keeps dropout in functional form (`F.dropout` with
`training=self.training`) and uses no `nn.Dropout` or BatchNorm submodules, so
`model.train()` at inference enables *only* dropout. That is the invariant
MC-Dropout depends on, and `influenza/intervals.py` depends on MC-Dropout.
LayerNorm is safe under it: it has no train/eval-dependent behaviour.
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class InfluenzaGNN(nn.Module):
    """Two GCN layers -> concat city-wide covariates -> fusion -> per-horizon head.

    Dropout is applied through F.dropout with `training=self.training` and there
    are no BatchNorm or nn.Dropout submodules, so calling model.train() at
    inference enables *only* dropout. That is what makes MC-Dropout valid here.
    """

    def __init__(
        self,
        n_node_feat: int,
        n_global: int,
        n_horizons: int = 1,
        hidden1: int = 64,
        hidden2: int = 32,
        fusion_out: int = 32,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        from torch_geometric.nn import GCNConv

        self.gcn1 = GCNConv(n_node_feat, hidden1)
        self.gcn2 = GCNConv(hidden1, hidden2)
        self.fusion = nn.Linear(hidden2 + n_global, fusion_out)
        self.output = nn.Linear(fusion_out, n_horizons)
        self.dropout = dropout
        self.n_horizons = n_horizons

    def forward(self, x, edge_index, g_vec, edge_weight=None):
        """x: (n_nodes, n_feat); g_vec: (n_global,) -> (n_nodes, n_horizons)."""
        h = F.relu(self.gcn1(x, edge_index, edge_weight))
        h = F.dropout(h, p=self.dropout, training=self.training)
        h = F.relu(self.gcn2(h, edge_index, edge_weight))
        h = F.dropout(h, p=self.dropout, training=self.training)
        if g_vec.numel():
            h = torch.cat([h, g_vec.unsqueeze(0).expand(h.size(0), -1)], dim=1)
        return self.output(F.relu(self.fusion(h)))


# ---------------------------------------------------------------------------
# Dual-Topo-STGCN (Luo et al. 2025)
# ---------------------------------------------------------------------------

class GatedTemporalConv(nn.Module):
    """Gated causal temporal convolution, equation 3 of the paper.

        X = ReLU(P * sigmoid(Q) + H)

    P, Q and H are three parallel 1x3 convolutions: P and Q form a gated linear
    unit and H is a projected residual. The kernel is `valid`, so each layer
    shortens the time axis by kernel_size - 1.
    """

    KERNEL = 3

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.conv = nn.Conv2d(in_channels, 3 * out_channels, kernel_size=(1, self.KERNEL))
        self.out_channels = out_channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (batch, channels, nodes, time) -> (batch, out, nodes, time - 2)."""
        p, q, h = torch.split(self.conv(x), self.out_channels, dim=1)
        return F.relu(p * torch.sigmoid(q) + h)


class DenseGCN(nn.Module):
    """Graph convolution against a pre-normalised dense adjacency, equation 4.

        X = ReLU(D^-1/2 A D^-1/2 X Theta)
    """

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.theta = nn.Linear(in_channels, out_channels)

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        """x: (batch, channels, nodes, time); adjacency: (nodes, nodes)."""
        aggregated = torch.einsum("bcnt,nm->bcmt", x, adjacency)
        projected = self.theta(aggregated.permute(0, 2, 3, 1))
        return F.relu(projected.permute(0, 3, 1, 2))


class STBlock(nn.Module):
    """Temporal conv -> graph conv -> temporal conv. Costs 4 time steps."""

    def __init__(self, in_channels: int, spatial_channels: int, out_channels: int) -> None:
        super().__init__()
        self.temporal_in = GatedTemporalConv(in_channels, spatial_channels)
        self.spatial = DenseGCN(spatial_channels, spatial_channels)
        self.temporal_out = GatedTemporalConv(spatial_channels, out_channels)

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        return self.temporal_out(self.spatial(self.temporal_in(x), adjacency))


class DualTopoSTGCN(nn.Module):
    """Two parallel ST pathways -- one per topology -- fused before the readout.

    The paper lists the fusion operator as a menu (max, min, mean, weighted
    mean, concatenation) without saying which produced its results; we default
    to concatenation and record the choice in run_config.json.
    """

    def __init__(
        self,
        n_nodes: int,
        n_neigh: int,
        input_window: int = 52,
        spatial_channels: int = 16,
        out_channels: int = 64,
        n_horizons: int = 1,
        blocks: int = 2,
        fusion: str = "concat",
        in_channels: int = 1,
    ) -> None:
        super().__init__()
        steps_used = blocks * 2 * (GatedTemporalConv.KERNEL - 1) + (GatedTemporalConv.KERNEL - 1)
        if input_window <= steps_used:
            raise ValueError(
                f"input_window={input_window} is too short for {blocks} ST blocks: "
                f"the valid convolutions consume {steps_used} steps."
            )
        self.time_out = input_window - steps_used
        self.n_nodes = n_nodes
        self.n_neigh = n_neigh
        self.fusion = fusion

        def pathway() -> nn.ModuleList:
            layers = []
            channels = in_channels
            for _ in range(blocks):
                layers.append(STBlock(channels, spatial_channels, out_channels))
                channels = out_channels
            return nn.ModuleList(layers)

        self.geo_blocks = pathway()
        self.corr_blocks = pathway()
        fused_channels = out_channels * (2 if fusion == "concat" else 1)
        self.final_temporal = GatedTemporalConv(fused_channels, out_channels)

        flatten_dim = out_channels * self.time_out
        self.head = nn.Sequential(
            nn.Linear(flatten_dim, 128), nn.ReLU(),
            nn.Linear(128, 32), nn.ReLU(),
            nn.Linear(32, n_horizons),
        )

    def _run(self, blocks: nn.ModuleList, x: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        for block in blocks:
            x = block(x, adjacency)
        return x

    def forward(self, x: torch.Tensor, a_geo: torch.Tensor, a_corr: torch.Tensor) -> torch.Tensor:
        """x: (batch, 1, nodes, time) -> (batch, nodes, n_horizons)."""
        geo = self._run(self.geo_blocks, x, a_geo)
        corr = self._run(self.corr_blocks, x, a_corr)

        if self.fusion == "concat":
            fused = torch.cat([geo, corr], dim=1)
        elif self.fusion == "mean":
            fused = (geo + corr) / 2
        elif self.fusion == "max":
            fused = torch.maximum(geo, corr)
        else:
            raise ValueError(f"Unknown fusion operator: {self.fusion!r}")

        fused = self.final_temporal(fused)
        batch, channels, nodes, time = fused.shape
        flat = fused.permute(0, 2, 1, 3).reshape(batch, nodes, channels * time)
        return self.head(flat)


# ---------------------------------------------------------------------------
# SpatioTemporalGNN -- the current design
# ---------------------------------------------------------------------------

class DilatedTemporalBlock(nn.Module):
    """One gated, causal, dilated 1-D convolution with a residual connection.

    Causal by left-padding rather than centring: a centred kernel at the origin
    week would read weeks after it, which is the forecast target. Dilation is how
    a small stack reaches the whole lookback -- kernel 2 at dilations 1, 2, 4, 8
    covers 16 weeks in four layers and 4*3*H*H parameters, where a single
    16-wide kernel would cost four times as much and a plain stack of sixteen
    kernel-2 layers would be far deeper than 122 training origins can fit.
    """

    def __init__(self, in_channels: int, out_channels: int, dilation: int,
                 kernel_size: int = 2) -> None:
        super().__init__()
        self.pad = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_channels, 3 * out_channels, kernel_size, dilation=dilation)
        self.residual = (nn.Identity() if in_channels == out_channels
                         else nn.Conv1d(in_channels, out_channels, 1))
        self.out_channels = out_channels

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (nodes, channels, time) -> (nodes, out_channels, time)."""
        padded = F.pad(x, (self.pad, 0))
        filt, gate, skip = torch.split(self.conv(padded), self.out_channels, dim=1)
        return torch.tanh(filt) * torch.sigmoid(gate) + skip + self.residual(x)


class MultiRelationalMixer(nn.Module):
    """One graph convolution per edge type, combined by a learned gate.

    The older design summed the geographic, correlation and demographic
    edges into a single adjacency before convolving. That answers "does
    connectivity help" but not "which kind of connection helped", which is the
    question this project exists to ask. Keeping the relations separate makes the
    gate weights readable: they say what the model actually leaned on.

    A learned `adaptive` relation is appended -- a dense adjacency from node
    embeddings, `softmax(relu(E1 @ E2.T))`. It can express couplings none of the
    hand-built types encode, and in the spatio-temporal forecasting literature it
    is usually the single largest architectural win. It is also the one relation
    that could quietly memorise the training weeks, so it carries DropEdge.
    """

    def __init__(self, channels: int, relation_names: list[str], n_nodes: int,
                 *, adaptive_dim: int = 8, dropedge: float = 0.1,
                 conv: str = "gcn", heads: int = 4) -> None:
        super().__init__()
        from torch_geometric.nn import GATConv, GCNConv

        self.conv_type = conv
        self.relation_names = list(relation_names)
        # adaptive_dim=0 means OFF, not "zero-width embedding". A zero-width
        # matmul yields an all-zero score matrix whose softmax is uniform, which
        # would quietly add a uniform-complete relation -- the opposite of an
        # ablation that removes one.
        self.adaptive = adaptive_dim > 0
        # add_self_loops=False: Graph.relation_tensors already supplies one per
        # node per relation, and letting the conv add a second would silently
        # double a node's self-weight relative to its neighbours.
        #
        # GAT replaces the degree-normalised average with learned attention. The
        # edge weight is handed over as a one-dimensional edge FEATURE rather
        # than as a fixed multiplier (`edge_dim=1`), which is the honest way to
        # give attention the same information GCN gets: GCN is told how strongly
        # two nodes are connected, GAT is told and may disagree. `heads` must
        # divide `channels` so concatenation returns the same width.
        if conv == "gat":
            if channels % heads:
                raise ValueError(
                    f"channels={channels} must be divisible by heads={heads}; "
                    "GATConv concatenates head outputs and the mixer expects the "
                    "same width back.")
            self.convs = nn.ModuleList([
                GATConv(channels, channels // heads, heads=heads, concat=True,
                        edge_dim=1, add_self_loops=False)
                for _ in self.relation_names
            ])
        elif conv == "gcn":
            self.convs = nn.ModuleList([
                GCNConv(channels, channels, add_self_loops=False)
                for _ in self.relation_names
            ])
        else:
            raise ValueError(f"Unknown conv type {conv!r}. Expected 'gcn' or 'gat'.")
        if self.adaptive:
            self.adaptive_source = nn.Parameter(torch.randn(n_nodes, adaptive_dim) * 0.1)
            self.adaptive_target = nn.Parameter(torch.randn(n_nodes, adaptive_dim) * 0.1)
            self.adaptive_project = nn.Linear(channels, channels, bias=False)
        self.gate = nn.Parameter(torch.zeros(len(self.relation_names) + int(self.adaptive)))
        self.norm = nn.LayerNorm(channels)
        self.dropedge = dropedge

    def adaptive_adjacency(self) -> torch.Tensor | None:
        if not self.adaptive:
            return None
        return F.softmax(F.relu(self.adaptive_source @ self.adaptive_target.t()), dim=1)

    def forward(self, h: torch.Tensor, relations: list[tuple]) -> torch.Tensor:
        """h: (nodes, channels); relations: [(name, edge_index, edge_weight)]."""
        by_name = {name: (index, weight) for name, index, weight in relations}
        parts = []
        for name, conv in zip(self.relation_names, self.convs):
            edge_index, edge_weight = by_name[name]
            if self.conv_type == "gat":
                parts.append(conv(h, edge_index, edge_attr=edge_weight.unsqueeze(-1)))
            else:
                parts.append(conv(h, edge_index, edge_weight))

        adjacency = self.adaptive_adjacency()
        if adjacency is not None:
            if self.training and self.dropedge > 0:
                keep = torch.rand_like(adjacency) >= self.dropedge
                adjacency = adjacency * keep
            parts.append(self.adaptive_project(adjacency @ h))

        weights = F.softmax(self.gate, dim=0)
        mixed = sum(w * part for w, part in zip(weights, parts))
        return self.norm(h + F.relu(mixed))

    def gate_weights(self) -> dict[str, float]:
        """The learned relation mixture, for run_config.json."""
        values = F.softmax(self.gate.detach(), dim=0).tolist()
        names = [*self.relation_names] + (["adaptive"] if self.adaptive else [])
        return dict(zip(names, values))


class SpatioTemporalGNN(nn.Module):
    """Temporal conv stack -> multi-relational graph mixing -> blended head.

    Three things distinguish it from `InfluenzaGNN`:

    1. It has a temporal axis at all. `build_samples` hands the lookback over
       flattened into the feature vector, so the old model saw eight lags as
       eight unordered columns and had no way to represent a trend. This reshapes
       them back into a sequence and convolves along it.
    2. Edge types stay separate and are mixed by a learned gate, instead of being
       summed into one adjacency before the model sees them.
    3. It predicts a residual from a *learned blend* of two baselines rather than
       from the origin week alone. See `blend_weights`.
    """

    def __init__(
        self,
        *,
        lookback: int,
        temporal_channels: int,
        n_static_feat: int,
        n_global: int,
        n_nodes: int,
        n_horizons: int,
        relation_names: list[str],
        hidden: int = 24,
        dropout: float = 0.2,
        dilations: tuple[int, ...] = (1, 2, 4, 8),
        adaptive_dim: int = 8,
        dropedge: float = 0.1,
        blend_init: tuple[float, ...] | None = None,
        horizon_steps: tuple[int, ...] | None = None,
        trend_anchor: bool = False,
        trend_init: float = -1.0,
        cascade: bool = False,
        n_blocks: int = 2,
        conv: str = "gcn",
        heads: int = 4,
    ) -> None:
        super().__init__()
        self.lookback = lookback
        self.temporal_channels = temporal_channels
        self.n_static_feat = n_static_feat
        self.n_horizons = n_horizons
        self.dropout = dropout

        blocks = []
        channels = temporal_channels
        for dilation in dilations:
            blocks.append(DilatedTemporalBlock(channels, hidden, dilation))
            channels = hidden
        self.temporal = nn.ModuleList(blocks)

        self.static_fuse = nn.Linear(hidden + n_static_feat, hidden)
        self.mixers = nn.ModuleList([
            MultiRelationalMixer(hidden, relation_names, n_nodes,
                                 adaptive_dim=adaptive_dim, dropedge=dropedge,
                                 conv=conv, heads=heads)
            for _ in range(n_blocks)
        ])
        self.head_fuse = nn.Linear(hidden + n_global, hidden)
        self.output = nn.Linear(hidden, n_horizons)

        # One scalar per horizon, through a sigmoid, mixing the two baselines the
        # residual is measured from:
        #
        #   base_h = s * level_at_origin + (1 - s) * climatology(target_week)
        #
        # Initialised high for short horizons and low for long ones, which is the
        # prior the measurements support: citywide corr(rate_t, rate_{t-h}) is
        # 0.906 at h=1 but 0.271 at h=4, while the seasonal curve holds 0.697 at
        # every horizon. Because the sigmoid confines it to [0, 1], the worst case
        # is that it collapses onto one of the two fixed baselines -- so it cannot
        # do worse than the better of them, which is what makes one extra
        # parameter per horizon safe on 122 training origins.
        if blend_init is None:
            blend_init = tuple([2.0] * n_horizons)
        self.blend_logit = nn.Parameter(torch.tensor(blend_init, dtype=torch.float32))

        # One more scalar per horizon, for how much of the recent trend to carry
        # forward when setting the origin half of that baseline:
        #
        #   origin_h = level_at_origin + sigmoid(t_h) * h * slope_at_origin
        #
        # The motivation is a measurement. At h=2 the learned origin share above
        # is 0.68, so more than two thirds of the baseline is the level from two
        # weeks BEFORE the target week -- and a baseline that stale is a phase
        # lag the network then has to undo through its residual. Sliding the
        # shipped h=2 forecast one week earlier removes 63% of its squared error
        # (Code/compare_timing.py), which is how much of the error that lag is
        # worth.
        #
        # Sigmoid-bounded exactly as blend_logit is, and for the same reason: at
        # 0 it collapses to the flat origin level and cannot do worse than the
        # arm it is an ablation of. That is what makes one more parameter per
        # horizon safe on 122 training origins -- and it is a real risk here,
        # because extrapolating the RAW observed slope measured worse at every
        # weight. The bound means the model can decline.
        # Created only for the arm that uses it. Registering it unconditionally
        # added a parameter and a buffer to every arm's state_dict, which took
        # gnn_st's recorded n_params from 15702 to 15703 and -- the reason this
        # matters -- made every committed checkpoint fail to load against the
        # class that wrote it. An unused parameter is not free when the .pt
        # files are the artifact.
        self.trend_anchor = trend_anchor
        # Only meaningful with more than one horizon: with a single head there is
        # no previous forecast to anchor on and it reduces to the plain blend.
        self.cascade = cascade and n_horizons > 1
        if trend_anchor:
            self.register_buffer(
                "horizon_steps",
                torch.tensor(horizon_steps if horizon_steps is not None
                             else tuple(range(1, n_horizons + 1)), dtype=torch.float32))
            self.trend_logit = nn.Parameter(
                torch.full((n_horizons,), trend_init, dtype=torch.float32))

    def blend_weights(self) -> list[float]:
        """Learned weight on the origin level, per horizon. 1 = pure persistence."""
        return torch.sigmoid(self.blend_logit.detach()).tolist()

    def trend_weights(self) -> list[float]:
        """Learned share of the recent trend carried into the anchor, per horizon.

        0 means the anchor is the flat origin level, which is what every arm
        other than `gnn_st_trendblend` uses. 1 means the trend is extrapolated
        the full h weeks. All zeros when the arm has no trend anchor at all.
        """
        if not self.trend_anchor:
            return [0.0] * self.n_horizons
        return torch.sigmoid(self.trend_logit.detach()).tolist()

    def gate_weights(self) -> list[dict[str, float]]:
        return [mixer.gate_weights() for mixer in self.mixers]

    def _encode(self, x: torch.Tensor) -> torch.Tensor:
        n_nodes = x.size(0)
        span = self.lookback * self.temporal_channels
        # build_samples writes lag-major, most-recent-first: for each lag, one
        # value per temporal source. Reshape recovers (time, channel); the flip
        # puts oldest first so the causal convolution runs forwards in time.
        sequence = x[:, :span].view(n_nodes, self.lookback, self.temporal_channels)
        sequence = sequence.flip(1).transpose(1, 2)
        for block in self.temporal:
            sequence = block(sequence)
            sequence = F.dropout(sequence, p=self.dropout, training=self.training)
        # The last position is the origin week and the only one with the full
        # receptive field behind it.
        h = sequence[:, :, -1]
        if self.n_static_feat:
            h = torch.cat([h, x[:, span:]], dim=1)
        else:
            h = torch.cat([h, x[:, span:span]], dim=1)
        return F.relu(self.static_fuse(h))

    def forward(self, x, relations, g_vec, anchor=None, clim=None, trend=None):
        """x: (nodes, n_feat) -> (nodes, n_horizons).

        `anchor` (n_scored,) and `clim` (n_scored, n_horizons) turn on the blended
        baseline for the scored nodes. Passing neither returns the raw residual,
        which is what the `delta` and `level` parameterisations expect.

        `trend` (n_scored,) is optional and only the `trendblend` target passes
        it: the per-week slope of the recent history at the origin week, which
        lets the anchor be extrapolated forward instead of held flat.
        """
        h = self._encode(x)
        for mixer in self.mixers:
            h = mixer(h, relations)
            h = F.dropout(h, p=self.dropout, training=self.training)

        if g_vec.numel():
            h = torch.cat([h, g_vec.unsqueeze(0).expand(h.size(0), -1)], dim=1)
        else:
            h = torch.cat([h, g_vec.new_zeros((h.size(0), 0))], dim=1)
        residual = self.output(F.relu(self.head_fuse(h)))

        if anchor is None or clim is None:
            return residual

        n_scored = anchor.size(0)
        share = torch.sigmoid(self.blend_logit).unsqueeze(0)
        origin = anchor.unsqueeze(1)
        if trend is not None and self.trend_anchor:
            carry = torch.sigmoid(self.trend_logit).unsqueeze(0)
            origin = origin + carry * self.horizon_steps.unsqueeze(0) * trend.unsqueeze(1)

        if self.cascade:
            # Each horizon anchors on the PREVIOUS horizon's own forecast rather
            # than on the origin week. At h=2 the origin level is two weeks stale
            # and carries 0.68 of the baseline, which is a phase lag the residual
            # then has to undo; the h=1 forecast for the same origin is one week
            # fresher and costs nothing extra to produce, because it comes out of
            # the same forward pass.
            #
            # The chain is differentiable, so error at h=2 flows back into the
            # h=1 path. That is the point -- it is what makes this a cascade
            # rather than two models stapled together -- but it also means the
            # h=1 head is no longer trained only for h=1.
            columns = []
            previous = None
            for h_idx in range(self.n_horizons):
                anchor_h = origin[:, h_idx] if previous is None else previous
                base_h = (share[:, h_idx] * anchor_h
                          + (1.0 - share[:, h_idx]) * clim[:, h_idx])
                out_h = base_h + residual[:n_scored, h_idx]
                columns.append(out_h)
                previous = out_h
            blended = torch.stack(columns, dim=1)
        else:
            base = share * origin + (1.0 - share) * clim
            blended = base + residual[:n_scored]
        # Anchor nodes have no baseline and are never scored; leaving their rows
        # as the raw residual keeps the tensor one shape for the caller.
        return torch.cat([blended, residual[n_scored:]], dim=0)


# ---------------------------------------------------------------------------
# GAT baseline (Luo et al. 2025 comparison model)
# ---------------------------------------------------------------------------

class GATBaseline(nn.Module):
    """Plain spatial Graph Attention Network over ILI history. A BASELINE.

    This is the comparison model Luo et al. include alongside ARIMA, LSTM and
    Conv-LSTM, where it places last at Corr 0.5994. It is deliberately a
    standalone model in the same sense `DualTopoSTGCN` is, rather than a flag on
    `SpatioTemporalGNN`: the paper's GAT has no temporal encoder at all, and
    swapping GATConv into an architecture that does have one measures a
    different thing entirely -- whether attention beats degree-normalised
    averaging *given* a temporal stack. Both questions are worth asking; only
    this one is the paper's.

    The paper describes its GAT only as a standard multi-head attention network
    over the topology, so the unstated choices are recorded in run_config.json
    exactly as they are for `dualtopo`: layer count, head count, hidden width and
    the readout. The input window matches the other comparison models at 52
    weeks, because Luo et al. state they ensured "uniform sliding window sizes".

    Node features are the ILI lags and nothing else -- no weather, demographics
    or city-wide covariates -- so the comparison is against the paper's model
    rather than against a better-fed version of it.
    """

    def __init__(
        self,
        *,
        lookback: int = 52,
        hidden: int = 64,
        heads: int = 8,
        n_horizons: int = 1,
        n_layers: int = 2,
        dropout: float = 0.2,
    ) -> None:
        super().__init__()
        from torch_geometric.nn import GATConv

        if hidden % heads:
            raise ValueError(
                f"hidden={hidden} must be divisible by heads={heads}; GATConv "
                "concatenates head outputs and the next layer expects `hidden` back."
            )
        self.dropout = dropout
        self.n_layers = n_layers

        # add_self_loops=True here, unlike the multi-relational mixer: the dense
        # adjacency handed to this model comes straight from Graph.edge_tensors,
        # and a node must attend to itself or its own history cannot reach the
        # readout through an attention-weighted average.
        self.convs = nn.ModuleList()
        in_dim = lookback
        for _ in range(n_layers):
            self.convs.append(
                GATConv(in_dim, hidden // heads, heads=heads, concat=True,
                        edge_dim=1, add_self_loops=True)
            )
            in_dim = hidden
        self.readout = nn.Linear(hidden, n_horizons)

    def forward(self, x, edge_index, g_vec=None, edge_weight=None):
        """x: (n_nodes, lookback) ILI lags -> (n_nodes, n_horizons).

        `g_vec` is accepted and ignored so the model is a drop-in for
        `training.train_gcn`, which calls `model(X, edge_index, g, edge_weight)`.
        The paper's GAT has no city-wide covariates and the registry arm sets
        `globals_=()`, so the tensor is empty in every configured run; asserting
        that rather than silently dropping a populated one.
        """
        if g_vec is not None and g_vec.numel():
            raise ValueError(
                f"GATBaseline received {g_vec.numel()} city-wide covariate(s). The "
                "paper's GAT comparison model uses ILI history only; set globals_=() "
                "or use run_gnn.py if you want covariates."
            )
        edge_attr = None if edge_weight is None else edge_weight.unsqueeze(-1)
        h = x
        for conv in self.convs:
            h = F.elu(conv(h, edge_index, edge_attr=edge_attr))
            h = F.dropout(h, p=self.dropout, training=self.training)
        return self.readout(h)
