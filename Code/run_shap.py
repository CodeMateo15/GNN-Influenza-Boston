"""Exact group-Shapley attribution for one forecast: a waterfall for the peak week.

    python -u Code/run_shap.py --experiment gnn_st --variant post_covid \
        --horizons 2 --checkpoint-dir Code/checkpoints/horizon_02

Answers "what drove THIS forecast, in this neighborhood, in this week" -- the one
question a retrain ablation structurally cannot answer, because an ablation
reports how the model scores over a whole test set without it, not what the
trained model leaned on for a single origin.

`run_ablation.py` remains the interpretability story for this project. This is
its per-week complement, and `Code/docs/METHODS.md` records where each applies.


Why this is not the old SHAP path restored
------------------------------------------
`influenza/shapley.py`, `influenza/importance.py` and `run_importance.py` were
removed. Two reasons, and both rule out simply bringing them back:

1. They used `shap.GradientExplainer` -- expected gradients, `phi ~= (x - x') .
   E[df/dx]` -- against a background of other forecast ORIGINS. Static
   demographics are identical at every origin (`samples.py:232-236`), so
   `x - x' = 0` and those eight columns scored exactly zero *by construction*.
   That is a property of the experiment, not a finding about the model.

2. They reached into `InfluenzaGNN` by attribute name, and the batching wrapper
   replicated the graph block-diagonally so one explainer call could cover many
   origins. That cannot be ported to `SpatioTemporalGNN`: its adaptive relation
   is `softmax(relu(adaptive_source @ adaptive_target.T))` built from two
   `(n_nodes, adaptive_dim)` parameters indexed by NODE ID (`models.py:287-297`).
   Replicate the graph and every copy past the first indexes the wrong rows.

So: no gradients, no batching wrapper. The game is collapsed to a handful of
group players and `shap.explainers.ExactExplainer` enumerates all `2^G`
coalitions. Exact, model-agnostic, and it calls the model the same way
`training.py:mc_dropout_stgnn` does.


How the degeneracy is actually fixed
------------------------------------
The fix is in the BACKGROUND, not the explainer. A background draw is one random
training-window origin with its scored-node rows randomly PERMUTED -- the same
permutation applied to `X`, `anchors` and `clim` so the draw stays internally
coherent (a node's flu history keeps the anchor its blend is measured from).

Demographics are constant across origins but differ across nodes, so permuting
nodes makes them vary and therefore measurable. The script asserts this rather
than assuming it: it prints the largest demographic delta it found across the
draws and refuses to run if that is zero.

Anchor nodes get no group, and that is the correct answer rather than a
limitation. `samples.py:239-246` fills EVERY anchor row, at every origin, with
one constant vector. They carry no information, so no method can attribute
anything to them.


What the numbers mean, and do not
---------------------------------
* Interventional. Masking a group swaps it for a value from a different
  node-week, producing input combinations that never occurred. That is the
  standard interventional assumption and it is what allows a
  constant-within-origin feature to be measured at all.
* The base value is "a generic node-week in the training window", NOT "this
  neighborhood at an average week". Each phi is a share of the gap between this
  node-week and that reference.
* Graph-coupled by construction. `f` rebuilds the whole node-feature matrix and
  runs one forward, so masking a neighbour's flu history propagates through
  message passing exactly as the model computes it. Neighbour effects are
  players here, not something folded into the base.
* One seed, `model.eval()`, deterministic. The checkpoint holds the first
  ensemble member, so this explains the mean-weight forward -- not the
  MC-Dropout ensemble behind the published intervals. The printed prediction
  will differ slightly from `predictions.csv` for that reason, and both are
  printed so the gap is visible rather than surprising.
* These are exact Shapley values OF THE GROUP GAME. The players are the groups,
  and the enumeration is over groups, so additivity is structural rather than an
  aggregation convention. The script asserts `base + sum(phi) == prediction`.


Which models this covers, and why not the rest
----------------------------------------------
    gnn_st and other `stgnn` arms   coalition enumeration (above)
    xgboost                         shap.TreeExplainer, exact and instant

    persistence, seasonal_naive     no features to attribute. Persistence IS
                                    the last observed value; a waterfall would
                                    have one bar equal to the whole forecast.
    arima                           per-node coefficients on its own lags and
                                    nothing else. `selected_orders.csv` beside
                                    its predictions already is its attribution.
    lstm, gat, dualtopo             supportable, not yet supported. Each needs
                                    its own `rebuild_model` branch; the
                                    background and grouping machinery here is
                                    model-agnostic and would carry over. gat and
                                    dualtopo would additionally want their
                                    52-week native window reflected in the lag
                                    groups, which is why they are not a
                                    copy-paste of the stgnn branch.

An `stgnn` arm whose checkpoint predates a graph or feature change is refused
by `guard()` rather than explained against the wrong topology -- that is what
the "checkpoint graph differs" error means, and the fix is to re-run the arm.
"""

from __future__ import annotations

import os, sys  # noqa: E401

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import json
from dataclasses import dataclass, replace
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import torch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install torch shap pandas "
                     f"numpy matplotlib.") from exc

from influenza import paths
from influenza.cli import (add_common_args, city_output_dirs, resolve_city,
                           resolve_window)
from influenza.config import EXPERIMENTS, Experiment
from influenza.constants import STATIC_DEMO_COLS, WEATHER_COLS
from influenza.graphs import build_graph
from influenza.models import DualTopoSTGCN, GATBaseline, SpatioTemporalGNN
from influenza.plots import ACTUAL_COLOUR, PREDICTED_COLOUR
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.windows import Window, split_origins, valid_origins, variant_data

# 2^12 coalitions x 20 draws x ~6ms is about eight minutes, which is past the
# point where a script described as "simple" should sit there silently.
MAX_PLAYERS = 12


# ---------------------------------------------------------------------------
# Checkpoint
# ---------------------------------------------------------------------------

def load_checkpoint(experiment: Experiment, checkpoint_dir: Path) -> dict:
    path = paths.require(
        checkpoint_dir / f"{experiment.name}_{experiment.variant}.pt",
        f"Checkpoint for {experiment.name}/{experiment.variant}",
    )
    # weights_only defaults to True in torch >= 2.6 and rejects the numpy arrays,
    # lists and nested dicts these checkpoints carry. This is our own file.
    return torch.load(path, map_location="cpu", weights_only=False)


def window_from_checkpoint(checkpoint: dict, experiment: Experiment) -> Window:
    """The sampling window the checkpoint was actually trained with.

    Every run serialises its resolved config, so a sweep checkpoint carries its
    own horizons and lookback even though the registry entry still says (1, 2).
    Falls back to the registry for checkpoints written before that was recorded.
    """
    recorded = (checkpoint.get("experiment") or {}).get("window") or {}
    changes = {}
    if recorded.get("horizons"):
        changes["horizons"] = tuple(int(h) for h in recorded["horizons"])
    if recorded.get("lookback"):
        changes["lookback"] = int(recorded["lookback"])
    return replace(experiment.window, **changes) if changes else experiment.window


def guard(checkpoint: dict, samples, edge_index, norm, n_horizons: int,
          experiment: Experiment) -> None:
    """Refuse to explain a model the current config would not have produced.

    Every mismatch here means the attributions would be labelled with the wrong
    feature names or computed over the wrong graph, which is worse than no
    explanation at all.

    Checks only what the checkpoint actually recorded, and says what it could
    not check. The three checkpoint writers disagree about provenance:
    `run_gnn.py` stores feature_names, global_names and edge_index;
    `run_gat.py` stores edge_index but no feature names; `run_dualtopo.py`
    stores dense adjacencies instead of an edge_index; `run_lstm.py` stores
    neither. Demanding the full set would refuse three of the four families
    over a key they were never asked to write, which is a false alarm, not
    safety.
    """
    rerun = (f"python Code/{ {'gat': 'run_gat.py', 'dualtopo': 'run_dualtopo.py'}
                             .get(experiment.model, 'run_gnn.py') } "
             f"--experiment {experiment.name} --variant {experiment.variant}")
    unchecked: list[str] = []

    if checkpoint.get("feature_names") is not None:
        if checkpoint["feature_names"] != samples.feature_names:
            raise SystemExit(
                f"error: checkpoint feature names differ from the current config "
                f"({len(checkpoint['feature_names'])} vs {len(samples.feature_names)}). "
                f"Re-run: {rerun}"
            )
    else:
        unchecked.append("feature names")

    if checkpoint.get("global_names") is not None:
        if checkpoint["global_names"] != samples.global_names:
            raise SystemExit(f"error: checkpoint global names differ. Re-run: {rerun}")

    if checkpoint.get("edge_index") is not None:
        if not torch.equal(checkpoint["edge_index"], edge_index):
            raise SystemExit(f"error: checkpoint graph differs from the rebuilt graph. "
                             f"Re-run: {rerun}")
    elif "a_geo" not in checkpoint:
        unchecked.append("graph topology")

    if checkpoint.get("flu_means") is not None:
        if not np.allclose(checkpoint["flu_means"], norm.flu_mean):
            raise SystemExit(f"error: checkpoint normalisation differs. Re-run: {rerun}")
    else:
        unchecked.append("normalisation")

    state = checkpoint["model_state_dict"]
    head_key = next((k for k in ("output.weight", "readout.weight") if k in state), None)
    if head_key and state[head_key].shape[0] != n_horizons:
        raise SystemExit(
            f"error: checkpoint has a {state[head_key].shape[0]}-horizon head but the "
            f"window asks for {n_horizons}. Drop --horizons, or re-run: {rerun} --horizons ..."
        )
    if unchecked:
        print(f"note: this checkpoint records no {', '.join(unchecked)}, so that "
              f"could not be verified against the current config. Weights still load "
              f"strictly, which catches an architecture change but not a feature one.")


def rebuild_model(checkpoint: dict, experiment: Experiment, samples, graph,
                  window: Window, relations) -> torch.nn.Module:
    """Reconstruct the architecture, then load weights strictly.

    Mirrors run_gnn.py:214-235, which is the source of truth. Duplicated rather
    than factored out because run_gnn's version closes over a dozen locals from
    its own setup; the guard against drift is `strict=True` below, not shared
    code. That guard matters: `models.py:427-432` registers `trend_logit` only
    when `trend_anchor` is on, so building the wrong variant produces a model
    that silently lacks a parameter the checkpoint has.
    """
    model = SpatioTemporalGNN(
        lookback=samples.lookback,
        temporal_channels=samples.temporal_channels,
        n_static_feat=samples.n_static_feat,
        n_global=samples.n_global,
        n_nodes=graph.n_nodes,
        n_horizons=len(window.horizons),
        relation_names=[name for name, _, _ in relations],
        hidden=experiment.train.channels,
        dropout=experiment.train.dropout,
        dilations=experiment.train.dilations,
        adaptive_dim=experiment.train.adaptive_dim if experiment.train.adaptive else 0,
        dropedge=experiment.train.drop_edge,
        horizon_steps=tuple(int(h) for h in window.horizons),
        trend_anchor=experiment.target == "trendblend",
        cascade=experiment.target == "cascade",
        n_blocks=experiment.train.n_blocks,
        conv=experiment.train.conv,
        heads=experiment.train.heads,
    )
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    model.eval()
    return model


# ---------------------------------------------------------------------------
# Which week, which node
# ---------------------------------------------------------------------------

def peak_week(test_set, norm, h_idx: int) -> tuple[int, int]:
    """(row into test_set, node) for the observed citywide peak target week.

    Citywide rather than per-node on purpose: per-node peaks scatter over six or
    more different weeks, so "the peak week" would be ambiguous and the figure
    would have to become fourteen figures. The citywide mean is also the series
    `severity.py` fits its MEM thresholds against, so the week chosen here is the
    one the severity tables already point at.

    `samples.y` is the normalised level for every target except `delta`, so it
    has to go through `to_level` before the peaks are comparable across nodes.
    """
    levels = norm.to_level(test_set.y)                       # (S, n_neigh, n_h)
    citywide = np.nanmean(levels[:, :, h_idx], axis=1)
    row = int(np.nanargmax(citywide))
    node = int(np.nanargmax(levels[row, :, h_idx]))
    return row, node


# ---------------------------------------------------------------------------
# Players
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Player:
    """One group in the collapsed game.

    Exactly one of the flags is set, or `xmask` is not None. The masks are
    disjoint and their union is every column that can vary, which is what makes
    `base + sum(phi) == prediction` structural rather than approximate.
    """
    label: str
    xmask: np.ndarray | None = None     # (n_nodes, n_feat) bool
    anchor: bool = False
    clim: bool = False
    g: bool = False


def _column_blocks(samples) -> tuple[np.ndarray, np.ndarray]:
    """(is_flu, is_demo) masks over the flat feature axis.

    Derived from `lookback * temporal_channels` and the recorded feature names
    rather than hardcoded, so an arm with extra temporal sources (wastewater, Rt)
    or with demographics switched off still groups correctly.
    """
    span = samples.lookback * samples.temporal_channels
    names = samples.feature_names
    is_flu = np.zeros(samples.n_feat, dtype=bool)
    is_demo = np.zeros(samples.n_feat, dtype=bool)
    for col, name in enumerate(names):
        if col < span:
            base = name.rsplit("_lag", 1)[0]
            is_flu[col] = base in ("flu", "flu_imputed")
        else:
            is_demo[col] = name in STATIC_DEMO_COLS
    return is_flu, is_demo


def build_players(samples, node: int, n_neigh: int, *, blended: bool) -> list[Player]:
    """The group decomposition, six or seven players for `gnn_st`.

    Own inputs are split from neighbours' because that is the question the graph
    arm exists to answer. Weather and demographics are kept apart from the flu
    lags for the same reason: a waterfall whose only bar is "features" says
    nothing.

    Anchor rows (index >= n_neigh) are deliberately absent -- see the module
    docstring. Empty groups are dropped rather than plotted as a zero bar,
    because a zero bar and an absent input look identical on a chart.
    """
    span = samples.lookback * samples.temporal_channels
    is_flu, is_demo = _column_blocks(samples)
    is_weather = np.zeros(samples.n_feat, dtype=bool)
    for col, name in enumerate(samples.feature_names):
        if col >= span and name in WEATHER_COLS:
            is_weather[col] = True
    is_other_temporal = np.zeros(samples.n_feat, dtype=bool)
    is_other_temporal[:span] = ~is_flu[:span]
    is_other_static = np.zeros(samples.n_feat, dtype=bool)
    is_other_static[span:] = ~(is_demo[span:] | is_weather[span:])

    def own(mask: np.ndarray) -> np.ndarray:
        full = np.zeros((samples.X.shape[1], samples.n_feat), dtype=bool)
        full[node] = mask
        return full

    def neighbours(mask: np.ndarray) -> np.ndarray:
        full = np.zeros((samples.X.shape[1], samples.n_feat), dtype=bool)
        full[:n_neigh] = mask
        full[node] = False
        return full

    candidates = [
        Player("Own flu history", own(is_flu)),
        Player("Own weather", own(is_weather)),
        Player("Own demographics", own(is_demo)),
        Player("Own other inputs", own(is_other_temporal | is_other_static)),
        Player("Neighbours' flu history", neighbours(is_flu)),
        Player("Neighbours' other inputs",
               neighbours(is_weather | is_demo | is_other_temporal | is_other_static)),
    ]
    players = [p for p in candidates if p.xmask.any()]
    if blended:
        # Not features: with target="blend" the forward returns
        # share*anchor + (1-share)*clim + residual (models.py:505-525) and these
        # two arrive as kwargs. Leaving them out would hide the entire
        # persistence-plus-climatology baseline inside the base value and make
        # the flu lags look far weaker than they are.
        players.append(Player("Persistence anchor", anchor=True))
        players.append(Player("Climatology", clim=True))
    if samples.n_global:
        players.append(Player("Citywide covariates", g=True))
    return players


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

@dataclass
class Draw:
    X: np.ndarray
    anchor: np.ndarray
    clim: np.ndarray | None
    g: np.ndarray


def background_draws(train_set, n_neigh: int, n_draws: int,
                     rng: np.random.Generator) -> list[Draw]:
    """Random training origins with their scored-node rows permuted.

    The permutation is the whole point: it is what makes a column that is
    constant across origins vary across the background, and therefore
    measurable. It is applied identically to X, anchors and clim so that a
    background "neighborhood" is internally consistent.

    Anchor rows are left in place. They are the same constant vector at every
    origin, so permuting them would change nothing.
    """
    draws: list[Draw] = []
    for _ in range(n_draws):
        i = int(rng.integers(len(train_set.positions)))
        order = rng.permutation(n_neigh)
        X = train_set.X[i].copy()
        X[:n_neigh] = X[order]
        anchor = train_set.anchors[i][order].copy()
        clim = None if train_set.clim is None else train_set.clim[i][order].copy()
        draws.append(Draw(X=X, anchor=anchor, clim=clim, g=train_set.g[i].copy()))
    return draws


def demographic_spread(draws: list[Draw], obs_X: np.ndarray, node: int,
                       is_demo: np.ndarray) -> float:
    """Largest demographic difference between the observed row and the draws.

    This is the receipt for the whole design. If it is zero, the background does
    not vary demographics and any zero attribution for them would be an artifact
    -- exactly the defect that retired the previous implementation. Reported, and
    enforced, rather than assumed.
    """
    if not is_demo.any():
        return float("nan")
    observed = obs_X[node][is_demo]
    return max(float(np.abs(d.X[node][is_demo] - observed).max()) for d in draws)


# ---------------------------------------------------------------------------
# The game
# ---------------------------------------------------------------------------

def _rate(value: float, norm, node: int) -> float:
    """Normalised output -> rate per 100,000 for one node.

    Affine with a strictly positive scale (`flu_std` carries a +1e-8 floor), so
    additivity survives the conversion exactly and every waterfall reads in the
    units of the forecast chart beside it.
    """
    return value * float(norm.flu_std.flatten()[node]) + float(norm.flu_mean.flatten()[node])


def stgnn_forward(model, relations, node, h_idx, norm, blended):
    """SpatioTemporalGNN: model(x, relations, g_vec, anchor=, clim=)."""
    def forward(X, g, anchor, clim) -> float:
        with torch.no_grad():
            kwargs = {}
            if blended:
                kwargs["anchor"] = torch.from_numpy(anchor)
                kwargs["clim"] = torch.from_numpy(clim)
            out = model(torch.from_numpy(X), relations, torch.from_numpy(g), **kwargs)
        return _rate(float(out[node, h_idx]), norm, node)
    return forward


def gat_forward(model, edge_index, edge_weight, node, h_idx, norm):
    """GATBaseline: model(x, edge_index, g_vec=None, edge_weight=...).

    Takes the ILI lags as its whole node feature vector -- no weather,
    demographics or covariates -- so the player list collapses to own and
    neighbours' history. That is the paper's model, not a stripped version of
    ours, and the short bar list is the honest picture of what it can see.
    """
    def forward(X, g, anchor, clim) -> float:
        with torch.no_grad():
            out = model(torch.from_numpy(X), edge_index, None, edge_weight)
        return _rate(float(out[node, h_idx]), norm, node)
    return forward


def dualtopo_forward(model, a_geo, a_corr, node, h_idx, norm):
    """DualTopoSTGCN: model(x, a_geo, a_corr) with x (batch, 1, nodes, time).

    build_samples emits lags most-recent-first, so the time axis is reversed
    here exactly as run_dualtopo.to_sequence does. Getting that backwards would
    run the temporal convolutions over a time-reversed series and quietly
    produce a plausible-looking wrong answer.
    """
    def forward(X, g, anchor, clim) -> float:
        seq = torch.from_numpy(X[None, None, :, ::-1].copy())
        with torch.no_grad():
            out = model(seq, a_geo, a_corr)
        return _rate(float(out[0, node, h_idx]), norm, node)
    return forward


def lstm_forward(model, node, h_idx, norm_mean, norm_std):
    """MultivariateLSTM: model(x) with x (batch, lookback, n_nodes).

    The one model here whose input is node-minor rather than node-major, so the
    adapter stores X as (n_nodes, lookback) like everything else and transposes
    at the boundary. Doing it here rather than in the masking loop is what keeps
    one grouping implementation valid for all four families.

    It also normalises per node with its own mean/std vectors rather than a
    Normalization object, so the un-scaling is spelled out instead of reusing
    `_rate`.
    """
    def forward(X, g, anchor, clim) -> float:
        seq = torch.from_numpy(X.T[None, ::-1].copy())
        with torch.no_grad():
            out = model(seq)
        return float(out[0, h_idx, node]) * float(norm_std[node]) + float(norm_mean[node])
    return forward


def make_predict(forward, players, draws, observed, node, progress):
    """f(coalition) -> predicted rate at `node`, averaged over the background.

    A masked (0) group is replaced by the background draw's value; an unmasked
    (1) group keeps the observed value. Every call rebuilds the full node-feature
    matrix and hands it to `forward`, so graph coupling -- where the model has
    any -- is inside the measurement rather than around it.

    `forward(X, g, anchor, clim) -> rate at this node` is supplied by the
    caller's adapter. Keeping it model-agnostic is what lets one masking loop
    serve the graph model, the two Luo comparison models and the LSTM, whose
    call signatures and tensor layouts all differ.
    """
    obs_X, obs_anchor, obs_clim, obs_g = observed

    def predict(Z: np.ndarray) -> np.ndarray:
        Z = np.atleast_2d(np.asarray(Z))
        out = np.empty(len(Z), dtype=float)
        for m, z in enumerate(Z):
            total = 0.0
            for draw in draws:
                X = obs_X.copy()
                anchor = obs_anchor.copy()
                clim = None if obs_clim is None else obs_clim.copy()
                g = obs_g
                for j, on in enumerate(z):
                    if on:
                        continue
                    player = players[j]
                    if player.xmask is not None:
                        X[player.xmask] = draw.X[player.xmask]
                    if player.anchor:
                        anchor[node] = draw.anchor[node]
                    if player.clim and clim is not None and draw.clim is not None:
                        clim[node] = draw.clim[node]
                    if player.g:
                        g = draw.g
                total += forward(X, g, anchor, clim)
            out[m] = total / len(draws)
            progress()
        return out

    return predict


def explain(predict, n_players: int) -> tuple[np.ndarray, float, float]:
    """Exact Shapley values over the group game.

    `shap.maskers.Independent` over a single all-zeros row makes "masked" mean
    "switch this group off", which `predict` reads as "take the background
    value". ExactExplainer then enumerates all 2^G coalitions, so there is no
    sampling error and no nsamples to justify.
    """
    try:
        import shap
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("Missing dependency: shap. pip install 'shap>=0.45'") from exc

    masker = shap.maskers.Independent(np.zeros((1, n_players)), max_samples=1)
    explainer = shap.explainers.ExactExplainer(predict, masker)
    # silent=True: shap's tqdm bar writes to stdout, where it interleaves with
    # the `Epoch N |` status lines run_progress.py parses.
    result = explainer(np.ones((1, n_players)), silent=True)
    values = np.asarray(result.values).reshape(-1)
    base = float(np.asarray(result.base_values).reshape(-1)[0])
    return values, base, base + float(values.sum())


# ---------------------------------------------------------------------------
# LSTM: the one model outside the Experiment registry
# ---------------------------------------------------------------------------

def default_variant(args, city) -> str:
    """The era to explain when --variant was not given.

    `city.variants[0]` is exclude_covid for Boston, but every graph arm and
    every saved checkpoint in this project is post_covid -- so falling back to
    the first entry asks for a file that was never written. Prefer post_covid
    where the city has it, which is all three cities.
    """
    if args.variant not in (None, "all"):
        return args.variant
    return "post_covid" if "post_covid" in city.variants else city.variants[0]


def explain_lstm(args, city, results_root, checkpoint_root) -> None:
    """Attribution for the multivariate LSTM baseline.

    `run_lstm.py` is not registry-driven: it has no Experiment, builds its own
    sliding windows with `arrays()`, and normalises with plain mean/std vectors
    rather than a Normalization object. So this path rebuilds the inputs from
    the same helpers `run_lstm` uses instead of going through `build_samples`.

    It is a single multivariate model over all scored nodes at once -- every
    node's history is an input column for every node's forecast -- so
    "neighbours' flu history" is a real group here even though there is no
    graph. That is the interesting contrast with GAT and dualtopo: same
    information, no topology.
    """
    from influenza import impute_causal, normalization
    from run_lstm import HIDDEN_SIZE, MultivariateLSTM, arrays

    variant = default_variant(args, city)
    path = paths.require(checkpoint_root / f"lstm_{variant}.pt", "LSTM checkpoint")
    checkpoint = torch.load(path, map_location="cpu", weights_only=False)

    horizons = tuple(int(h) for h in checkpoint["horizons"])
    window = replace(Window(), horizons=horizons, lookback=int(checkpoint["lookback"]))
    horizon = int(args.horizon or horizons[0])
    if horizon not in horizons:
        raise SystemExit(f"--horizon {horizon} not in {list(horizons)}")
    h_idx = list(horizons).index(horizon)

    rates = variant_data(city.loaders.load_rates(), variant).available
    origins = valid_origins(rates.index, window)
    split = split_origins(rates.index, origins, window)
    features, _ = impute_causal(rates)
    mean, std = normalization(rates, split, mode="train")
    x_train, _ = arrays(features, rates, split.train, mean, std, window)
    x_test, _ = arrays(features, rates, split.test, mean, std, window)

    n_series = x_test.shape[2]
    model = MultivariateLSTM(n_series, len(horizons), HIDDEN_SIZE)
    model.load_state_dict(checkpoint["model_state_dict"], strict=True)
    model.eval()

    # Store node-major like every other family so the masking code is shared;
    # lstm_forward transposes back at the boundary. arrays() emits oldest-first,
    # the others emit most-recent-first, so reverse here too -- one convention
    # inside the attribution code, converted at each adapter's edge.
    X_test = np.ascontiguousarray(x_test.transpose(0, 2, 1)[:, :, ::-1])
    X_train = np.ascontiguousarray(x_train.transpose(0, 2, 1)[:, :, ::-1])

    mean_v = np.asarray(mean, dtype=np.float64).flatten()
    std_v = np.asarray(std, dtype=np.float64).flatten()
    actual = rates.to_numpy(dtype=float)

    def observed_rate(row: int, node: int) -> float:
        return float(actual[split.test[row] + horizon, node])

    chose_peak = not args.target_date
    if args.target_date:
        wanted = pd.Timestamp(args.target_date)
        cands = [r for r, pos in enumerate(split.test) if rates.index[pos + horizon] == wanted]
        if not cands:
            raise SystemExit(f"no test origin targets {wanted.date()} at horizon {horizon}.")
        row = cands[0]
    else:
        citywide = [np.nanmean([observed_rate(r, n) for n in range(n_series)])
                    for r in range(len(split.test))]
        row = int(np.nanargmax(citywide))
    node = (city.node_names.index(args.node) if args.node
            else int(np.nanargmax([observed_rate(row, n) for n in range(n_series)])))

    origin_date = rates.index[split.test[row]]
    target_date = rates.index[split.test[row] + horizon]
    obs = observed_rate(row, node)

    print(f"\n{'=' * 72}\n{city.label} | lstm | {variant} | horizon {horizon}\n{'=' * 72}")
    which = "Peak target week" if chose_peak else "Target week"
    print(f"{which}: {target_date.date()} (origin {origin_date.date()}), citywide mean "
          f"{np.nanmean([observed_rate(row, n) for n in range(n_series)]):.1f} per 100,000")
    print(f"Explaining: {city.node_names[node]}, observed {obs:.1f} per 100,000")

    # Only two groups exist: this is a rates-only model with no weather,
    # demographics, covariates or baseline terms.
    own = np.zeros((n_series, window.lookback), dtype=bool); own[node] = True
    nbr = np.ones((n_series, window.lookback), dtype=bool); nbr[node] = False
    players = [Player("Own flu history", own), Player("Neighbours' flu history", nbr)]
    labels = [p.label for p in players]

    rng = np.random.default_rng(args.seed)
    draws = []
    for _ in range(args.n_background):
        i = int(rng.integers(len(X_train)))
        order = rng.permutation(n_series)
        draws.append(Draw(X=X_train[i][order].copy(), anchor=np.zeros(1, dtype=np.float32),
                          clim=None, g=np.zeros(0, dtype=np.float32)))

    total = 2 ** len(players) + 1
    print(f"Players: {len(players)} -> {2 ** len(players)} coalitions "
          f"x {args.n_background} background draws")

    if args.importance:
        targets = importance_targets(len(split.test), n_series,
                                     args.importance_weeks, row)
        print(f"Budget: {len(targets)} epochs x 1 seeds", flush=True)
        print("--- seed importance (1/1) ---", flush=True)
        per_target = []
        for i, (t_row, t_node) in enumerate(targets, 1):
            t_own = np.zeros((n_series, window.lookback), dtype=bool); t_own[t_node] = True
            t_nbr = np.ones((n_series, window.lookback), dtype=bool); t_nbr[t_node] = False
            t_players = [Player("Own flu history", t_own),
                         Player("Neighbours' flu history", t_nbr)]
            t_obs = (X_test[t_row], np.zeros(1, dtype=np.float32), None,
                     np.zeros(0, dtype=np.float32))
            t_predict = make_predict(lstm_forward(model, t_node, h_idx, mean_v, std_v),
                                     t_players, draws, t_obs, t_node, lambda: None)
            t_values, _, _ = explain(t_predict, len(t_players))
            per_target.append(t_values)
            print(f"Epoch {i} | {city.node_names[t_node]} "
                  f"{rates.index[split.test[t_row] + horizon].date()}", flush=True)
        finish_importance(city=city, model_name="lstm", variant=variant,
                          horizon=horizon, results_root=results_root, labels=labels,
                          per_target=per_target, n_targets=len(targets),
                          n_weeks=len({r for r, _ in targets}))
        return

    print(f"Budget: {total} epochs x 1 seeds", flush=True)
    print("--- seed shap (1/1) ---", flush=True)
    state = {"n": 0}

    def progress() -> None:
        state["n"] += 1

    forward = lstm_forward(model, node, h_idx, mean_v, std_v)
    observed = (X_test[row], np.zeros(1, dtype=np.float32), None, np.zeros(0, dtype=np.float32))
    predict = make_predict(forward, players, draws, observed, node, progress)
    values, base, prediction = explain(predict, len(players))
    drift = abs(base + values.sum() - prediction)
    assert drift < 1e-4 * max(1.0, abs(prediction)), f"additivity violated by {drift}"
    print(f"Additivity: base {base:.2f} + sum(phi) {values.sum():+.2f} "
          f"= {prediction:.2f} (drift {drift:.2e})")

    report(city=city, model_name="lstm", variant=variant, horizon=horizon,
           results_root=results_root, node=node, origin_date=origin_date,
           target_date=target_date, labels=labels, values=values, base=base,
           prediction=max(0.0, prediction), actual=obs,
           n_background=args.n_background, seed=args.seed,
           footnote="A single multivariate LSTM over all nodes: neighbours are "
                    "input columns, not graph neighbours. No weather, "
                    "demographics or baseline terms exist for it to use.")


# ---------------------------------------------------------------------------
# XGBoost: exact tree Shapley
# ---------------------------------------------------------------------------

def xgboost_players(feature_names, lookback, temporal_channels) -> list[tuple[str, np.ndarray]]:
    """Column groups for the pooled tree design matrix.

    Same split as the graph model's OWN-node groups, with two differences that
    are structural rather than cosmetic:

      * No neighbour groups. XGBoost sees one row per (origin, node) and has no
        edges, so there is nothing to attribute spillover to. That absence is
        the comparison this project exists to make -- it should read as an empty
        space on the chart, not be papered over.
      * A `node identity` group, for the trailing node-id column `flatten()`
        appends. Trees split on it directly, so "which neighborhood this is" is
        a real, separable input here in a way it is not for the GNN.
    """
    span = lookback * temporal_channels
    n = len(feature_names)
    flu = np.zeros(n, dtype=bool)
    weather = np.zeros(n, dtype=bool)
    demo = np.zeros(n, dtype=bool)
    node_id = np.zeros(n, dtype=bool)
    other = np.zeros(n, dtype=bool)
    for col, name in enumerate(feature_names):
        if name == "node_id":
            node_id[col] = True
        elif col < span:
            flu[col] = name.rsplit("_lag", 1)[0] in ("flu", "flu_imputed")
            other[col] = not flu[col]
        elif name in WEATHER_COLS:
            weather[col] = True
        elif name in STATIC_DEMO_COLS:
            demo[col] = True
        else:
            other[col] = True
    groups = [("Own flu history", flu), ("Own weather", weather),
              ("Own demographics", demo), ("Own other inputs", other),
              ("Node identity", node_id)]
    return [(label, mask) for label, mask in groups if mask.any()]


def explain_xgboost(args, city, results_root, checkpoint_root) -> None:
    """Exact Shapley values for the tree baseline, via TreeExplainer.

    Trees are the one family here with an exact, instant Shapley algorithm, so
    this path needs no coalition enumeration and no background averaging loop.
    It is also the model most worth explaining after the GNN: `METHODS.md`
    records XGBoost as the strongest non-graph baseline at four weeks.

    The climatology offset is an explicit player rather than part of the base.
    With `--target climatology` the booster predicts `rate - climatology` and
    the script adds the baseline back, exactly as the GNN's `clim` kwarg enters
    after the mixer. Folding it into the base value would hide the single
    largest term at long horizons.
    """
    try:
        import shap
        import xgboost as xgb
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(f"Missing dependency: {exc.name}.") from exc

    from influenza.climatology import fit_climatology
    from run_xgboost import flatten

    name = args.name or "xgboost"
    variant = default_variant(args, city)
    horizons = args.horizons or (2,)
    horizon = int(args.horizon or list(horizons)[0])

    booster_path = checkpoint_root / f"{name}_{variant}_h{horizon:02d}.json"
    meta_path = booster_path.with_suffix(".meta.json")
    if not booster_path.exists() or not meta_path.exists():
        raise SystemExit(
            f"no saved booster at {paths.display(booster_path)}. run_xgboost.py only "
            f"started persisting its model recently -- re-run it:\n"
            f"  python Code/run_xgboost.py --city {city.name} --variant {variant} "
            f"--horizons {horizon} --output-dir <results>/horizon_{horizon:02d} "
            f"--checkpoint-dir {paths.display(checkpoint_root)}"
        )
    meta = json.loads(meta_path.read_text())
    model = xgb.XGBRegressor()
    model.load_model(booster_path)

    # Rebuild exactly the design matrix run_xgboost.py trained on.
    features = EXPERIMENTS[args.features_from].features
    window = resolve_window(args, replace(EXPERIMENTS[args.features_from].window,
                                          horizons=(horizon,)))
    data = variant_data(city.loaders.load_rates(), variant)
    dataset = load_dataset(features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)
    history = dataset.rates.loc[dataset.rates.index < window.test_start]
    graph_static = dataset.static
    graph = build_graph(EXPERIMENTS[args.features_from].graph, city=city,
                        flu_history=history, static=graph_static)
    samples, norm = build_samples(dataset, split, features, window, graph,
                                  target="level", normalize="train")
    if [*samples.feature_names, "node_id"] != meta["feature_names"]:
        raise SystemExit("saved booster's feature names differ from the current config. "
                         "Re-run run_xgboost.py.")

    n_neigh = city.n_neigh
    X_all, rows_meta = flatten(samples, n_neigh)
    # Same fit window run_xgboost.py uses: training origins only, so the
    # seasonal baseline never sees a test week.
    end = split.train[-1] + window.max_horizon + 1
    climatology = fit_climatology(dataset.rates, end=end)
    clim_rate = climatology.level(dataset.week_index)

    train_rows = set(positions_to_rows(samples, split.train))
    test_rows = set(positions_to_rows(samples, split.test))

    def clim_for(r: int) -> float:
        s, node = rows_meta[r]
        return float(clim_rate[samples.positions[s] + horizon, node])

    # Pick the week the same way the graph path does: observed citywide peak.
    levels = norm.to_level(samples.y)
    test_sample_idx = sorted(test_rows)
    chose_peak = not args.target_date
    if args.target_date:
        wanted = pd.Timestamp(args.target_date)
        cands = [s for s in test_sample_idx
                 if split.index[samples.positions[s] + horizon] == wanted]
        if not cands:
            raise SystemExit(f"no test origin targets {wanted.date()} at horizon {horizon}.")
        s_star = cands[0]
    else:
        citywide = {s: np.nanmean(levels[s, :, 0]) for s in test_sample_idx}
        s_star = max(citywide, key=citywide.get)
    node = (city.node_names.index(args.node) if args.node
            else int(np.nanargmax(levels[s_star, :, 0])))
    if args.node and args.node not in city.node_names:
        raise SystemExit(f"unknown node {args.node!r}")

    row = next(r for r, (s, nd) in enumerate(rows_meta) if s == s_star and nd == node)
    origin_date = split.index[samples.positions[s_star]]
    target_date = split.index[samples.positions[s_star] + horizon]
    actual = float(levels[s_star, node, 0])

    print(f"\n{'=' * 72}\n{city.label} | {name} | {variant} | horizon {horizon}"
          f"\n{'=' * 72}")
    which = "Peak target week" if chose_peak else "Target week"
    print(f"{which}: {target_date.date()} (origin {origin_date.date()}), "
          f"citywide mean {np.nanmean(levels[s_star, :, 0]):.1f} per 100,000")
    print(f"Explaining: {city.node_names[node]}, observed {actual:.1f} per 100,000")

    # Interventional against the training rows, so the reference is the same
    # concept as the graph path's: a generic training node-week. Tree-path-
    # dependent would need no background but would answer a different question
    # and could not be compared with the GNN waterfall beside it.
    background = X_all[[r for r, (s, _) in enumerate(rows_meta) if s in train_rows]]
    if len(background) > args.n_background * n_neigh:
        rng = np.random.default_rng(args.seed)
        background = background[rng.choice(len(background),
                                           args.n_background * n_neigh, replace=False)]
    print(f"Background: {len(background)} training node-weeks (exact TreeExplainer, "
          f"no coalition sampling)")

    explainer = shap.TreeExplainer(model, data=background,
                                   feature_perturbation="interventional")

    if args.importance:
        # Trees are exact and vectorised, so every sampled row goes through in
        # one call -- no per-node-week loop and no coalition budget.
        test_sorted = sorted(test_rows)
        peak_pos = test_sorted.index(s_star)
        picks = importance_targets(len(test_sorted), n_neigh,
                                   args.importance_weeks, peak_pos)
        idx = [next(r for r, (s, nd) in enumerate(rows_meta)
                    if s == test_sorted[w] and nd == nd_) for w, nd_ in picks]
        print(f"Budget: 1 epochs x 1 seeds", flush=True)
        print("--- seed importance (1/1) ---", flush=True)
        phi_all = np.asarray(shap.TreeExplainer(
            model, data=background,
            feature_perturbation="interventional")(X_all[idx]).values)
        groups_i = xgboost_players(meta["feature_names"], meta["lookback"],
                                   meta["temporal_channels"])
        labels_i = [lb for lb, _ in groups_i]
        per_target = np.stack([phi_all[:, m].sum(axis=1) for _, m in groups_i], axis=1)
        if meta["target"] == "climatology":
            bg_rows = [r for r, (s, _) in enumerate(rows_meta) if s in train_rows]
            clim_bg = float(np.mean([clim_for(r) for r in bg_rows]))
            labels_i.append("Climatology")
            per_target = np.column_stack(
                [per_target, np.array([clim_for(r) - clim_bg for r in idx])])
        print("Epoch 1 | tree shapley, all rows in one pass", flush=True)
        finish_importance(city=city, model_name=name, variant=variant,
                          horizon=horizon, results_root=results_root,
                          labels=labels_i, per_target=per_target,
                          n_targets=len(idx), n_weeks=len({w for w, _ in picks}))
        return

    raw = explainer(X_all[row:row + 1])
    phi = np.asarray(raw.values).reshape(-1)
    base_model = float(np.asarray(raw.base_values).reshape(-1)[0])

    groups = xgboost_players(meta["feature_names"], meta["lookback"],
                             meta["temporal_channels"])
    labels = [label for label, _ in groups]
    values = np.array([phi[mask].sum() for _, mask in groups], dtype=float)

    if meta["target"] == "climatology":
        # The booster predicts a residual from climatology, so the seasonal
        # baseline is an input to the forecast that the model never sees. It
        # gets its own bar, measured against the background's mean climatology
        # so that base + sum(phi) still lands on the prediction.
        bg_rows = [r for r, (s, _) in enumerate(rows_meta) if s in train_rows]
        clim_bg = float(np.mean([clim_for(r) for r in bg_rows]))
        labels.append("Climatology")
        values = np.append(values, clim_for(row) - clim_bg)
        base = base_model + clim_bg
        prediction = float(model.predict(X_all[row:row + 1])[0]) + clim_for(row)
    else:
        base = base_model
        prediction = float(model.predict(X_all[row:row + 1])[0])
    prediction = max(0.0, prediction)

    drift = abs(base + values.sum() - prediction)
    assert drift < 1e-3 * max(1.0, abs(prediction)), f"additivity violated by {drift}"
    print(f"Additivity: base {base:.2f} + sum(phi) {values.sum():+.2f} "
          f"= {prediction:.2f} (drift {drift:.2e})")

    report(city=city, model_name=name, variant=variant, horizon=horizon,
           results_root=results_root, node=node, origin_date=origin_date,
           target_date=target_date, labels=labels, values=values, base=base,
           prediction=prediction, actual=actual, n_background=len(background),
           seed=args.seed,
           footnote="No neighbour groups: XGBoost has no edges, so it cannot "
                    "attribute anything to other neighborhoods. That gap is the "
                    "comparison, not an omission.")


# ---------------------------------------------------------------------------
# Global feature importance
# ---------------------------------------------------------------------------

def importance_targets(n_rows: int, n_neigh: int, n_weeks: int,
                       peak_row: int) -> list[tuple[int, int]]:
    """(row, node) pairs to average over for a global importance chart.

    Every scored node, but only a sample of weeks: the coalition enumeration
    costs ~16s per node-week for the graph model, so all 53 test weeks x 14
    nodes would be three hours to draw one bar chart.

    The weeks are spread EVENLY across the test year rather than drawn at
    random, and the observed peak is forced in. A random sample of a year that
    is mostly off-season would be mostly off-season, and the off-season is the
    regime where every model reduces to "near zero again this week" -- exactly
    the weeks where nothing is driving anything. Averaging |phi| over those
    would report that no feature matters anywhere.
    """
    if n_weeks >= n_rows:
        weeks = list(range(n_rows))
    else:
        weeks = sorted({int(round(i)) for i in
                        np.linspace(0, n_rows - 1, n_weeks)} | {peak_row})
    return [(r, n) for r in weeks for n in range(n_neigh)]


def plot_importance(labels, mean_abs, mean_signed, path: Path, title: str,
                    subtitle_to_stdout: str) -> None:
    """Mean |phi| per group, with the signed mean drawn as a marker.

    Two numbers rather than one because they answer different questions and
    disagree in a way that matters: a group that pushes some forecasts up and
    others down by the same amount has a large mean |phi| and a mean near zero.
    Reporting only the magnitude would call that group influential without
    saying it has no consistent direction; reporting only the signed mean would
    call it irrelevant.
    """
    order = np.argsort(mean_abs)
    labels = [labels[i] for i in order]
    mean_abs = np.asarray(mean_abs)[order]
    mean_signed = np.asarray(mean_signed)[order]

    fig, ax = plt.subplots(figsize=(8.5, 0.5 * len(labels) + 2.0))
    rows = np.arange(len(labels))
    ax.barh(rows, mean_abs, height=0.6, color=PREDICTED_COLOUR,
            label="mean |contribution|")
    ax.plot(mean_signed, rows, linestyle="none", marker="|", markersize=14,
            markeredgewidth=2, color=ACTUAL_COLOUR, label="mean signed contribution")
    ax.axvline(0.0, color="gray", ls=":", lw=1.0)
    for row, (a, s) in enumerate(zip(mean_abs, mean_signed)):
        ax.text(a + max(mean_abs) * 0.015, row, f"{a:.1f}  ({s:+.1f})",
                va="center", fontsize=7.5)
    ax.set_yticks(rows)
    ax.set_yticklabels(labels, fontsize=9)
    ax.margins(x=0.22)
    ax.set_xlabel("ILI ED visit rate per 100,000")
    ax.legend(fontsize=8, loc="lower right")
    fig.suptitle(title)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(subtitle_to_stdout)


def finish_importance(*, city, model_name, variant, horizon, results_root,
                      labels, per_target, n_targets, n_weeks) -> None:
    """Aggregate per-node-week attributions into the importance artifacts."""
    values = np.asarray(per_target)                      # (n_targets, n_groups)
    mean_abs = np.abs(values).mean(axis=0)
    mean_signed = values.mean(axis=0)

    out_dir = paths.horizon_dir(horizon, results_root) / model_name / variant / "shap"
    frame = pd.DataFrame({
        "city": city.name, "model": model_name, "variant": variant,
        "horizon": horizon, "group": labels,
        "mean_abs_shap_rate_per_100k": mean_abs,
        "mean_signed_shap_rate_per_100k": mean_signed,
        "n_node_weeks": n_targets, "n_weeks": n_weeks,
    }).sort_values("mean_abs_shap_rate_per_100k", ascending=False)
    out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out_dir / "shap_importance.csv", index=False)

    plot_importance(
        labels, mean_abs, mean_signed, out_dir / "shap_importance.png",
        f"{model_name} — what the model leans on, {horizon} week"
        f"{'s' if horizon > 1 else ''} ahead\n"
        f"mean over {n_targets} node-weeks, {variant}",
        f"\nGlobal importance over {n_targets} node-weeks "
        f"({n_weeks} weeks x {city.n_neigh} {city.node_label}s):")
    for _, r in frame.iterrows():
        print(f"  {r['group']:<26} {r['mean_abs_shap_rate_per_100k']:8.2f}  "
              f"(signed {r['mean_signed_shap_rate_per_100k']:+8.2f})")
    print(f"Outputs: {paths.display(out_dir)}", flush=True)


# ---------------------------------------------------------------------------
# Shared reporting
# ---------------------------------------------------------------------------

def report(*, city, model_name, variant, horizon, results_root, node,
           origin_date, target_date, labels, values, base, prediction, actual,
           n_background, seed, footnote) -> None:
    """Write the waterfall and the CSV, and echo the ranking to stdout."""
    out_dir = (paths.horizon_dir(horizon, results_root) / model_name / variant / "shap")
    title = (f"{model_name} — what drove {city.node_names[node]} "
             f"in the week of {target_date.date()}\n"
             f"{horizon} week{'s' if horizon > 1 else ''} ahead, {variant}")
    png = out_dir / "shap_waterfall_peak.png"
    plot_waterfall(labels, np.asarray(values), base, prediction, actual, png, title)

    frame = pd.DataFrame({
        "city": city.name, "model": model_name, "variant": variant,
        "horizon": horizon, "origin_date": origin_date, "target_date": target_date,
        "neighborhood": city.node_names[node], "group": labels,
        "shap_rate_per_100k": values, "base_rate_per_100k": base,
        "predicted_rate_per_100k": prediction, "actual_rate_per_100k": actual,
        "n_background": n_background, "seed": seed,
    })
    csv = out_dir / "shap_values.csv"
    csv.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(csv, index=False)

    print()
    for label, value in sorted(zip(labels, values), key=lambda kv: -abs(kv[1])):
        print(f"  {label:<26} {value:+8.2f}")
    print(f"\n{footnote}")
    print(f"Outputs: {paths.display(csv.parent)}", flush=True)


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

def plot_waterfall(labels, values, base, prediction, actual, path: Path,
                   title: str) -> None:
    """Cumulative horizontal waterfall, in the house style.

    Hand-rolled rather than `shap.plots.waterfall`, which imposes its own
    typography, colours and a boxed layout -- the look this project has just
    finished removing. Colours come from influenza/plots.py so this figure
    matches the forecast grid it explains.
    """
    order = np.argsort(-np.abs(values))
    labels = [labels[i] for i in order]
    values = values[order]

    fig, ax = plt.subplots(figsize=(9, 0.52 * len(values) + 2.4))
    cursor = base
    for row, value in enumerate(values):
        left = min(cursor, cursor + value)
        ax.barh(row, abs(value), left=left, height=0.62,
                color=PREDICTED_COLOUR if value >= 0 else ACTUAL_COLOUR)
        # Label on the outside of the bar, so a short bar's number does not sit
        # on top of it.
        edge = cursor + value
        ax.text(edge + (1.0 if value >= 0 else -1.0), row,
                f"{value:+.1f}", va="center",
                ha="left" if value >= 0 else "right", fontsize=7.5)
        cursor = edge

    ax.axvline(base, color="gray", ls=":", lw=1.0, label=f"Baseline {base:.1f}")
    ax.axvline(prediction, color="black", lw=1.2, label=f"Predicted {prediction:.1f}")
    if actual is not None and np.isfinite(actual):
        ax.axvline(actual, color=ACTUAL_COLOUR, lw=1.2, ls="--",
                   label=f"Observed {actual:.1f}")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.margins(x=0.16)
    ax.set_xlabel("ILI ED visit rate per 100,000")
    # Lower right: the bars march left-to-right and the observed line pushes the
    # axis out past them, so the bottom-right corner is the one reliably empty
    # region. "best" put the legend on top of the smallest bar's label.
    ax.legend(fontsize=8, loc="lower right")
    fig.suptitle(title)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_args(parser)
    parser.add_argument("--experiment", default="gnn_st",
                        help="Registry entry to explain. Must be an `stgnn` model.")
    parser.add_argument("--node", default=None,
                        help="Which node to explain. Default: the highest observed "
                             "rate in the chosen week.")
    parser.add_argument("--target-date", default=None,
                        help="YYYY-MM-DD target week. Default: the observed citywide "
                             "peak inside the test window.")
    parser.add_argument("--horizon", type=int, default=None,
                        help="Which horizon to explain. Required only when the "
                             "checkpoint carries more than one.")
    parser.add_argument("--name", default=None,
                        help="Results/checkpoint directory name. Defaults to "
                             "--experiment, or 'xgboost' on the tree path.")
    parser.add_argument("--features-from", default="gnn_st",
                        help="XGBoost only: which registry entry's FeatureSpec the "
                             "booster was trained on. Must match run_xgboost.py.")
    parser.add_argument("--n-background", type=int, default=20,
                        help="Graph path: background draws averaged per coalition. "
                             "Tree path: draws per node in the interventional "
                             "background.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--importance", action="store_true",
                        help="Global feature importance instead of a single "
                             "waterfall: mean |contribution| per group over many "
                             "node-weeks. Writes shap_importance.{png,csv}.")
    parser.add_argument("--importance-weeks", type=int, default=12,
                        help="Weeks sampled for --importance, spread evenly across "
                             "the test year with the observed peak forced in. Every "
                             "scored node is used at each week.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    city = resolve_city(args)
    results_root, checkpoint_root = city_output_dirs(args, city)

    # Trees get an exact, instant Shapley algorithm of their own; routing them
    # through the coalition enumeration would be slower and no more correct.
    if args.experiment == "xgboost" or args.name == "xgboost":
        explain_xgboost(args, city, results_root, checkpoint_root)
        return
    if args.experiment == "lstm":
        explain_lstm(args, city, results_root, checkpoint_root)
        return

    if args.experiment not in EXPERIMENTS:
        raise SystemExit(f"Unknown experiment {args.experiment!r}. "
                         f"Available: {', '.join(sorted(EXPERIMENTS))}")
    experiment = EXPERIMENTS[args.experiment]
    if experiment.model == "gcn_fusion":
        raise SystemExit(
            f"{args.experiment} is a retired `gcn_fusion` (InfluenzaGNN) arm. Those "
            "were removed along with the original attribution path; there is nothing "
            "to explain."
        )
    if experiment.variant not in city.variants:
        experiment = replace(experiment, variant=city.variants[0])
    if getattr(args, "variant", None) and args.variant != "all":
        experiment = replace(experiment, variant=args.variant)

    checkpoint = load_checkpoint(experiment, checkpoint_root)
    window = window_from_checkpoint(checkpoint, experiment)
    window = resolve_window(args, window)
    experiment = replace(experiment, window=window)

    # `delta` re-introduces the anchor through the un-normalisation rather than
    # through the forward pass, which is a different game structure. No shipped
    # arm uses it; failing beats quietly explaining the wrong quantity.
    if experiment.target == "delta":
        raise SystemExit("target='delta' is not supported: the anchor re-enters through "
                         "un-normalisation, so anchor and climatology cannot be players.")
    blended = experiment.target in ("blend", "trendblend", "cascade")

    rates = city.loaders.load_rates()
    data = variant_data(rates, experiment.variant)
    dataset = load_dataset(experiment.features, city=city, rates=data.available)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)
    history = dataset.rates.loc[dataset.rates.index < window.test_start]

    graph_static = dataset.static
    if experiment.graph.demo and graph_static is None:
        graph_static = city.loaders.load_static_demographics()[0]
    graph = build_graph(experiment.graph, city=city, flu_history=history,
                        static=graph_static)

    samples, norm = build_samples(dataset, split, experiment.features, window, graph,
                                  target=experiment.target, normalize=experiment.normalize)
    edge_index, _ = graph.edge_tensors()
    guard(checkpoint, samples, edge_index, norm, len(window.horizons), experiment)

    if experiment.model == "gat":
        model = GATBaseline(lookback=window.lookback, hidden=experiment.train.hidden[0],
                            heads=experiment.train.hidden[1],
                            n_horizons=len(window.horizons))
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        model.eval()
        edge_index_t, edge_weight_t = graph.edge_tensors()
        forward_factory = lambda node, h: gat_forward(  # noqa: E731
            model, edge_index_t, edge_weight_t, node, h, norm)
    elif experiment.model == "dualtopo":
        # Mirrors run_dualtopo.py:144-152. `fusion` is a CLI flag there, not a
        # TrainSpec field, and the run records its choice in run_config.json --
        # so read it back from the checkpoint's serialised experiment rather
        # than assuming the default.
        fusion = ((checkpoint.get("experiment") or {}).get("train") or {}).get("fusion")
        model = DualTopoSTGCN(
            n_nodes=graph.n_nodes, n_neigh=graph.n_neigh, input_window=window.lookback,
            spatial_channels=experiment.train.hidden[0],
            out_channels=experiment.train.hidden[1],
            n_horizons=len(window.horizons), fusion=fusion or "concat")
        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        model.eval()
        a_geo = checkpoint["a_geo"]
        a_corr = checkpoint["a_corr"]
        forward_factory = lambda node, h: dualtopo_forward(  # noqa: E731
            model, a_geo, a_corr, node, h, norm)
    else:
        relations = graph.relation_tensors(list(experiment.train.relations))
        model = rebuild_model(checkpoint, experiment, samples, graph, window, relations)
        forward_factory = lambda node, h: stgnn_forward(  # noqa: E731
            model, relations, node, h, norm, blended)

    train_set = samples.subset(positions_to_rows(samples, split.train))
    test_set = samples.subset(positions_to_rows(samples, split.test))

    if len(window.horizons) == 1:
        h_idx, horizon = 0, int(window.horizons[0])
    elif args.horizon is None:
        raise SystemExit(f"checkpoint covers horizons {list(window.horizons)}; "
                         f"pass --horizon to choose one.")
    else:
        horizon = int(args.horizon)
        if horizon not in window.horizons:
            raise SystemExit(f"--horizon {horizon} not in {list(window.horizons)}")
        h_idx = list(window.horizons).index(horizon)

    n_neigh = city.n_neigh
    chose_peak = not args.target_date
    if args.target_date:
        wanted = pd.Timestamp(args.target_date)
        matches = [r for r, pos in enumerate(test_set.positions)
                   if split.index[pos + horizon] == wanted]
        if not matches:
            raise SystemExit(f"no test origin targets {wanted.date()} at horizon {horizon}.")
        row = matches[0]
        node = int(np.nanargmax(norm.to_level(test_set.y)[row, :, h_idx]))
    else:
        row, node = peak_week(test_set, norm, h_idx)
    if args.node:
        if args.node not in city.node_names:
            raise SystemExit(f"unknown node {args.node!r}. Known: "
                             f"{', '.join(city.node_names)}")
        node = city.node_names.index(args.node)

    origin_date = split.index[test_set.positions[row]]
    target_date = split.index[test_set.positions[row] + horizon]
    levels = norm.to_level(test_set.y)
    actual = float(levels[row, node, h_idx])

    print(f"\n{'=' * 72}\n{city.label} | {experiment.name} | {experiment.variant} | "
          f"horizon {horizon}\n{'=' * 72}")
    which = "Peak target week" if chose_peak else "Target week"
    print(f"{which}: {target_date.date()} (origin {origin_date.date()}), "
          f"citywide mean {np.nanmean(levels[row, :, h_idx]):.1f} per 100,000")
    print(f"Explaining: {city.node_names[node]}, observed {actual:.1f} per 100,000")

    players = build_players(samples, node, n_neigh,
                            blended=blended and experiment.model == "stgnn")
    if len(players) > MAX_PLAYERS:
        raise SystemExit(f"{len(players)} players is 2^{len(players)} coalitions, which is "
                         f"too slow to be worth it. Merge groups in build_players().")
    print(f"Players: {len(players)} -> {2 ** len(players)} coalitions "
          f"x {args.n_background} background draws")

    rng = np.random.default_rng(args.seed)
    draws = background_draws(train_set, n_neigh, args.n_background, rng)
    _, is_demo = _column_blocks(samples)
    spread = demographic_spread(draws, test_set.X[row], node, is_demo)
    if is_demo.any():
        if not np.isfinite(spread) or spread == 0.0:
            raise SystemExit(
                "the background does not vary this node's demographics, so their "
                "attribution would be zero by construction -- the exact defect that "
                "retired the previous SHAP path. Raise --n-background."
            )
        print(f"Background varies own demographics: yes (max |dz| = {spread:.2f})")
    else:
        print("Background varies own demographics: n/a (this arm has none)")

    observed = (test_set.X[row], test_set.anchors[row],
                None if test_set.clim is None else test_set.clim[row], test_set.g[row])

    total = 2 ** len(players) + 1
    # Only the mode that actually runs emits the status-line contract:
    # run_progress.py takes the FIRST `Budget:` as the denominator, so printing
    # both a per-coalition and a per-node-week budget would peg the bar at the
    # wrong total.
    if not args.importance:
        print(f"Budget: {total} epochs x 1 seeds", flush=True)
        print("--- seed shap (1/1) ---", flush=True)
    state = {"n": 0}

    def progress() -> None:
        state["n"] += 1
        if state["n"] % 16 == 0 or state["n"] == total:
            print(f"Epoch {state['n']} | coalition {state['n']}/{total}", flush=True)

    labels = [p.label for p in players]

    if args.importance:
        targets = importance_targets(len(test_set.positions), n_neigh,
                                     args.importance_weeks, row)
        print(f"Budget: {len(targets)} epochs x 1 seeds", flush=True)
        print("--- seed importance (1/1) ---", flush=True)
        per_target = []
        for i, (t_row, t_node) in enumerate(targets, 1):
            t_players = build_players(samples, t_node, n_neigh,
                                      blended=blended and experiment.model == "stgnn")
            t_observed = (test_set.X[t_row], test_set.anchors[t_row],
                          None if test_set.clim is None else test_set.clim[t_row],
                          test_set.g[t_row])
            t_predict = make_predict(forward_factory(t_node, h_idx), t_players, draws,
                                     t_observed, t_node, lambda: None)
            t_values, _, _ = explain(t_predict, len(t_players))
            per_target.append(t_values)
            print(f"Epoch {i} | {city.node_names[t_node]} "
                  f"{split.index[test_set.positions[t_row] + horizon].date()}", flush=True)
        finish_importance(city=city, model_name=experiment.name,
                          variant=experiment.variant, horizon=horizon,
                          results_root=results_root, labels=labels,
                          per_target=per_target, n_targets=len(targets),
                          n_weeks=len({r for r, _ in targets}))
        return

    predict = make_predict(forward_factory(node, h_idx), players, draws,
                           observed, node, progress)
    values, base, prediction = explain(predict, len(players))

    # Additivity is structural for a disjoint group game; assert it rather than
    # claim it, because a silent violation would mean the masks overlap.
    drift = abs(base + values.sum() - prediction)
    assert drift < 1e-4 * max(1.0, abs(prediction)), f"additivity violated by {drift}"
    print(f"Additivity: base {base:.2f} + sum(phi) {values.sum():+.2f} "
          f"= {prediction:.2f} (drift {drift:.2e})")

    report(city=city, model_name=experiment.name, variant=experiment.variant,
           horizon=horizon, results_root=results_root, node=node,
           origin_date=origin_date, target_date=target_date, labels=labels,
           values=values, base=base, prediction=prediction, actual=actual,
           n_background=args.n_background, seed=args.seed,
           footnote=("The deterministic single-seed forward gives "
                     f"{prediction:.1f}; predictions.csv carries the 10-seed "
                     "MC-Dropout mean, so the two differ."))


if __name__ == "__main__":
    main()
