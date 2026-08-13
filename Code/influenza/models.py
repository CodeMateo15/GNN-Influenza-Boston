"""Model architectures.

`InfluenzaGNN` is the project's own design: two graph convolutions over a fused
multi-type adjacency, with city-wide covariates concatenated before the head.

`DualTopoSTGCN` reimplements Luo et al. (2025), BMC Public Health 25:408. It is
deliberately written without torch_geometric -- dense einsum message passing
means the paper model runs on a machine that only has torch installed.
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
