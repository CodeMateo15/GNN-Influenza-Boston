"""Cola-GNN: an established spatio-temporal GNN for regional ILI, as an external baseline.

Deng, Wang, Rangwala, Wang & Ning (2020), "Cola-GNN: Cross-location Attention
based Graph Neural Networks for Long-term ILI Prediction", CIKM 2020. It is the
most-cited GNN built specifically for ILI forecasting across regions, and a
reviewer comparing a new graph model against only LSTM/ARIMA/boosted trees -- or
against the two models of one paper (Luo et al.) -- will ask why it is missing.

This is OUR reimplementation from the paper's description, not the authors'
code, and should be reported as such. The components, in the paper's order:

  1. A GRU shared across locations encodes each location's own history -> h_i.
  2. Cross-location attention a_ij = v' elu(W_s h_i + W_t h_j + b), rows
     L2-normalised, gated against the geographic adjacency:
         M = (1 - S) * A_geo + S * A_att,  S = sigmoid(W_g A_att + b_g)
     so the model learns how far to trust learned links over borders.
  3. Dilated 1-D convolutions over each location's raw series, one short- and
     one long-range dilation, concatenated -> the initial node features.
  4. Two graph layers H' = elu(M H W + b) over those features.
  5. Readout from [H ; h_i], one output per horizon.

Inputs are the ILI series alone, as in the paper -- the same information the
LSTM baseline gets, plus geographic adjacency between the scored nodes (no
anchor nodes: Cola-GNN has no notion of them). Everything else -- train-only
normalisation, the masked loss on suppressed weeks, early stopping on
validation, the seed ensemble, the shared interval and quantile recipe, the
validation predictions tune.py selects on -- is the LSTM runner's, so the two
differ only in architecture.

    python Code/run_colagnn.py --variant post_covid --horizons 2
    python Code/run_colagnn.py --variant full --horizons 2 --n-seeds 10
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import copy
import random

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

from influenza import (
    SEED,
    impute_causal,
    Window,
    finish_run,
    normalization,
    split_origins,
    track_emissions,
    valid_origins,
    variant_data,
)
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                          resolve_variants, resolve_window, run_tag)
from influenza.config import GraphSpec
from influenza.graphs import build_graph
from influenza.intervals import attach_intervals, empirical_coverage, fit_intervals
from run_lstm import arrays, masked_mse

MODEL = "colagnn"
DEFAULT_LOOKBACK = 20   # the paper's window
PATIENCE = 25


class ColaGNN(nn.Module):
    def __init__(self, n_nodes: int, lookback: int, n_horizons: int, adjacency: np.ndarray,
                 hidden: int = 32, conv_channels: int = 16, gnn_hidden: int = 32,
                 dropout: float = 0.2, kernel: int = 3, long_dilation: int = 2) -> None:
        super().__init__()
        self.n_nodes, self.n_horizons = n_nodes, n_horizons
        self.register_buffer("a_geo", torch.tensor(adjacency, dtype=torch.float32))
        # 1. Shared temporal encoder.
        self.rnn = nn.GRU(input_size=1, hidden_size=hidden, batch_first=True)
        # 2. Cross-location attention and its gate against geography.
        self.w_s = nn.Linear(hidden, hidden, bias=False)
        self.w_t = nn.Linear(hidden, hidden)
        self.v = nn.Linear(hidden, 1)
        self.gate = nn.Linear(n_nodes, n_nodes)
        # 3. Short- and long-range dilated convolutions over the raw series.
        self.conv_short = nn.Conv1d(1, conv_channels, kernel, dilation=1)
        self.conv_long = nn.Conv1d(1, conv_channels, kernel, dilation=long_dilation)
        short_len = lookback - (kernel - 1)
        long_len = lookback - long_dilation * (kernel - 1)
        if long_len < 1:
            raise ValueError(f"lookback {lookback} too short for dilation {long_dilation}")
        conv_features = conv_channels * 2
        self.conv_proj = nn.Linear(conv_channels * (short_len + long_len), conv_features)
        # 4. Two graph layers.
        self.gnn1 = nn.Linear(conv_features, gnn_hidden)
        self.gnn2 = nn.Linear(gnn_hidden, gnn_hidden)
        # 5. Readout from graph output and the location's own encoding.
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(gnn_hidden + hidden, n_horizons)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, T, N) normalised rates -> (B, H, N)."""
        B, T, N = x.shape
        series = x.permute(0, 2, 1).reshape(B * N, T, 1)
        _, h_last = self.rnn(series)
        h = h_last[-1].view(B, N, -1)                                   # (B, N, d)

        scores = self.v(F.elu(self.w_s(h)[:, :, None, :] + self.w_t(h)[:, None, :, :]))
        attention = F.normalize(scores.squeeze(-1), p=2, dim=-1)        # (B, N, N)
        gate = torch.sigmoid(self.gate(attention))
        mixing = (1.0 - gate) * self.a_geo[None] + gate * attention

        raw = series.permute(0, 2, 1)                                   # (B*N, 1, T)
        conv = torch.cat([F.relu(self.conv_short(raw)).flatten(1),
                          F.relu(self.conv_long(raw)).flatten(1)], dim=1)
        features = F.relu(self.conv_proj(conv)).view(B, N, -1)

        g = F.elu(mixing @ self.gnn1(self.dropout(features)))
        g = F.elu(mixing @ self.gnn2(self.dropout(g)))
        out = self.out(self.dropout(torch.cat([g, h], dim=-1)))         # (B, N, H)
        return out.permute(0, 2, 1)


def geographic_adjacency(city, rates: pd.DataFrame) -> np.ndarray:
    """Row-normalised border adjacency between the scored nodes, with self-loops."""
    graph = build_graph(GraphSpec(anchors="none", geo=True, geo_max_hop=1, corr=False,
                                  demo=False),
                        city=city, flu_history=rates.iloc[:0], static=None)
    a = (np.asarray(graph.W)[:city.n_neigh, :city.n_neigh] > 0).astype(np.float64)
    a = a + np.eye(city.n_neigh)
    return a / a.sum(axis=1, keepdims=True)


def train_one(train, val, adjacency, device, args, window, n_nodes, seed):
    x_train, y_train, _ = train
    x_val, y_val, _ = val
    model = ColaGNN(n_nodes, window.lookback, len(window.horizons), adjacency,
                    hidden=args.hidden, conv_channels=args.conv_channels,
                    gnn_hidden=args.hidden, dropout=args.dropout).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    generator = torch.Generator().manual_seed(seed)
    loader = DataLoader(TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
                        batch_size=args.batch_size, shuffle=True, generator=generator)
    val_x = torch.from_numpy(x_val).to(device)
    val_y = torch.from_numpy(y_val).to(device)
    best_state, best_loss, best_epoch, patience = None, np.inf, 0, 0
    for epoch in range(1, args.epochs + 1):
        model.train()
        for xb, yb in loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            loss = masked_mse(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = float(masked_mse(model(val_x), val_y).item())
        if val_loss < best_loss - 1e-7:
            best_loss, best_epoch, patience = val_loss, epoch, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            patience += 1
        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:3d} | validation MSE {val_loss:.6f}", flush=True)
        if patience >= PATIENCE:
            break
    if best_state is not None:
        model.load_state_dict(best_state)
    return model, best_epoch, best_loss, epoch


def run_variant(all_rates: pd.DataFrame, variant: str, window: Window,
                args: argparse.Namespace, city) -> None:
    results_root, _ = city_output_dirs(args, city)
    data = variant_data(all_rates, variant)
    rates = data.available
    origins = valid_origins(rates.index, window)
    split = split_origins(rates.index, origins, window)
    features, _ = impute_causal(rates)
    mean, std = normalization(rates, split, mode="train")
    train = arrays(features, rates, split.train, mean, std, window)
    val = arrays(features, rates, split.val, mean, std, window)
    x_test = arrays(features, rates, split.test, mean, std, window)[0]
    adjacency = geographic_adjacency(city, rates)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'=' * 72}\nCola-GNN | {city.label} | {variant}\n{'=' * 72}")
    print(f"Train: {len(split.train)} | Validation: {len(split.val)} | Test: {len(split.test)} | "
          f"lookback {window.lookback}")

    seeds = [SEED + i for i in range(args.n_seeds)]
    print(f"Budget: {args.epochs} epochs x {len(seeds)} seeds", flush=True)
    test_draws, val_draws, per_seed = [], [], []
    with track_emissions(run_tag(args.name, variant, window), enabled=not args.no_carbon,
                         city=city.name) as carbon:
        for i, seed in enumerate(seeds, start=1):
            print(f"--- seed {seed} ({i}/{len(seeds)}) ---", flush=True)
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            with carbon.phase("train"):
                model, best_epoch, best_loss, epochs_run = train_one(
                    train, val, adjacency, device, args, window, city.n_neigh, seed)
            carbon.add_epochs(epochs_run)
            model.eval()
            with carbon.phase("eval"), torch.no_grad():
                test_draws.append(model(torch.from_numpy(x_test).to(device)).cpu().numpy()
                                  * std[:, None, :] + mean[:, None, :])
                val_draws.append(model(torch.from_numpy(val[0]).to(device)).cpu().numpy()
                                 * std[:, None, :] + mean[:, None, :])
            per_seed.append({"seed": seed, "best_epoch": best_epoch, "best_val_mse": best_loss})
    predicted = np.maximum(0.0, np.mean(test_draws, axis=0))
    val_predicted = np.maximum(0.0, np.mean(val_draws, axis=0))

    def frame(positions, values):
        return pd.DataFrame([
            {"origin_date": split.index[position],
             "target_date": split.index[position + horizon],
             "horizon": horizon,
             "neighborhood": neighborhood,
             "actual": float(rates.iloc[position + horizon, node]),
             "predicted": float(values[s, h_idx, node])}
            for s, position in enumerate(positions)
            for h_idx, horizon in enumerate(window.horizons)
            for node, neighborhood in enumerate(city.node_names)
        ])

    test_frame = frame(split.test, predicted)
    test_frame["error"] = test_frame["predicted"] - test_frame["actual"]
    validation = frame(split.val, val_predicted)
    interval_model = fit_intervals(validation["predicted"], validation["actual"],
                                   validation["horizon"], two_sided=args.two_sided_intervals)
    predictions = attach_intervals(test_frame, interval_model)
    coverage = empirical_coverage(predictions["actual"], predictions["lower"], predictions["upper"])
    print(f"95% interval test coverage {coverage:.1f}%")

    finish_run(
        model=args.name,
        variant=variant,
        predictions=predictions,
        config={
            "model_class": "ColaGNN (reimplementation of Deng et al. 2020, CIKM)",
            "target_kind": "level",
            "normalize": "train",
            "window": window.to_json(),
            "split": split.to_json(),
            "hidden": args.hidden, "conv_channels": args.conv_channels,
            "dropout": args.dropout, "lr": args.lr, "weight_decay": args.weight_decay,
            "epochs": args.epochs, "batch_size": args.batch_size,
            "n_seeds": len(seeds), "seeds": seeds, "per_seed": per_seed,
            "n_params": sum(p.numel() for p in model.parameters()),
            "adjacency": "geographic borders between scored nodes, row-normalised, self-loops",
            "intervals": interval_model.to_json(),
            "test_interval_coverage": coverage,
        },
        bands=True,
        carbon=carbon,
        results_root=results_root,
        city=city,
        extra_tables={"predictions_val": validation},
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser, variants=("all", "exclude_covid", "post_covid", "full"))
    parser.add_argument("--name", default=MODEL)
    parser.add_argument("--epochs", type=int, default=150)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--hidden", type=int, default=32)
    parser.add_argument("--conv-channels", type=int, default=16)
    parser.add_argument("--dropout", type=float, default=0.2)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--n-seeds", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    city = resolve_city(args)
    window = resolve_window(args, Window(lookback=DEFAULT_LOOKBACK), city)
    rates = city.loaders.load_rates()
    for variant in resolve_variants(args.variant):
        run_variant(rates, variant, window, args, city)


if __name__ == "__main__":
    main()
