"""Feature importance and SHAP explanations for a trained model.

The leaderboard says which model wins. This says why -- which inputs it leans
on across the test window (permutation importance), and which inputs produced
one specific forecast for one neighborhood on one week (a SHAP waterfall).

Loads the checkpoint a run already wrote rather than retraining, so the
explanation is provably of the model whose numbers are in the leaderboard.

    python Code/run_importance.py --experiment gnn_multiedge --variant post_covid
    python Code/run_importance.py --experiment gnn_multiedge \
           --waterfall "Dorchester:2026-01-03" --waterfall "Roxbury:2026-01-10"
    python Code/run_importance.py --experiment gnn_multiedge --skip-shap

Two results that look like bugs and are not, both stated again in the figure
footnotes: the 8 static demographic columns and every anchor-node column get
*exactly* zero SHAP and zero origin-permutation importance, because they do not
vary across forecast origins. That means "this experiment cannot measure them",
not "the model ignores them" -- the only rigorous test of a static covariate is
a retrain ablation, which the registry already supports.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
import time
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import torch
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        f"Missing dependency: {exc.name}. Install torch shap pandas numpy matplotlib."
    ) from exc

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import palette, paths
from influenza.artifacts import git_sha, run_dir
from dataclasses import replace

from influenza.config import EXPERIMENTS, Experiment
from influenza.constants import SEED
from influenza.data import load_rates
from influenza.graphs import build_graph
from influenza.importance import (
    DualTopoPredictor,
    GCNPredictor,
    PermutationSpec,
    feature_groups,
    permutation_importance,
)
from influenza.models import InfluenzaGNN
from influenza.samples import build_samples, load_dataset, positions_to_rows
from influenza.windows import split_origins, valid_origins, variant_data

UNSUPPORTED = {
    "arima": "statsmodels ARIMA has no learned feature map",
    "persistence": "persistence has no features",
    "seasonal_naive": "seasonal_naive has no features",
}


# ---------------------------------------------------------------------------
# Loading the trained model
# ---------------------------------------------------------------------------

def load_checkpoint(experiment: Experiment, checkpoint_dir: Path) -> dict:
    path = paths.require(
        checkpoint_dir / f"{experiment.name}_{experiment.variant}.pt",
        f"Checkpoint for {experiment.name}/{experiment.variant}",
    )
    # weights_only defaults to True in torch >= 2.6 and rejects the numpy arrays,
    # lists and nested dicts these checkpoints carry. This is our own file.
    return torch.load(path, map_location="cpu", weights_only=False)


def window_from_checkpoint(checkpoint: dict, experiment: Experiment):
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
    """
    rerun = (f"python Code/run_gnn.py --experiment {experiment.name} "
             f"--variant {experiment.variant}")
    if checkpoint.get("feature_names") != samples.feature_names:
        raise SystemExit(
            f"error: checkpoint feature names differ from the current config "
            f"({len(checkpoint.get('feature_names', []))} vs {len(samples.feature_names)}). "
            f"Re-run: {rerun}"
        )
    if checkpoint.get("global_names") != samples.global_names:
        raise SystemExit(f"error: checkpoint global names differ. Re-run: {rerun}")
    if not torch.equal(checkpoint["edge_index"], edge_index):
        raise SystemExit(f"error: checkpoint graph differs from the rebuilt graph. Re-run: {rerun}")
    if not np.allclose(checkpoint["flu_means"], norm.flu_mean):
        raise SystemExit(f"error: checkpoint normalisation differs. Re-run: {rerun}")
    head = checkpoint["model_state_dict"]["output.weight"].shape[0]
    if head != n_horizons:
        raise SystemExit(
            f"error: checkpoint has a {head}-horizon head but the window asks for "
            f"{n_horizons}. Drop --horizons, or re-run: {rerun} --horizons ..."
        )


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_permutation(frame: pd.DataFrame, path: Path, title: str) -> None:
    """Group importance above, per-feature below, both as ranked bars."""
    fig, axes = plt.subplots(2, 1, figsize=(7.5, 8.5),
                             gridspec_kw={"height_ratios": [1, 2]})
    for ax, scope, label in ((axes[0], "group", "Feature group (permuted together)"),
                             (axes[1], "feature", "Single feature (marginal, given the rest)")):
        view = frame.loc[frame["scope"].eq(scope)].sort_values("delta_RMSE")
        if view.empty:
            ax.set_visible(False)
            continue
        y = np.arange(len(view))
        ax.barh(y, view["delta_RMSE"], xerr=view["permuted_RMSE_std"],
                color=palette.SERIES[0], height=0.7,
                error_kw={"ecolor": palette.INK_MUTED, "elinewidth": 0.8, "capsize": 2})
        ax.set_yticks(y)
        ax.set_yticklabels(view["name"], fontsize=7)
        ax.set_title(label, color=palette.INK_PRIMARY, fontsize=9, loc="left")
        ax.set_xlabel("Increase in RMSE when shuffled (ILI per 100,000)",
                      color=palette.INK_SECONDARY, fontsize=8)
        palette.style_axes(ax, grid_axis="x")

    fig.suptitle(title, color=palette.INK_PRIMARY, fontsize=10, x=0.01, ha="left")
    fig.patch.set_facecolor(palette.SURFACE)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)


def plot_group_bar(labels: list[str], values: np.ndarray, path: Path, title: str) -> None:
    """Mean |SHAP| per group, pooled over origins and target neighborhoods."""
    order = np.argsort(values)
    fig, ax = plt.subplots(figsize=(7.0, 0.42 * len(labels) + 1.6))
    ax.barh(np.arange(len(labels)), values[order], color=palette.SERIES[0], height=0.7)
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels([labels[i] for i in order], fontsize=8)
    ax.set_xlabel("Mean |SHAP| (ILI per 100,000)", color=palette.INK_SECONDARY, fontsize=8)
    ax.set_title(title, color=palette.INK_PRIMARY, fontsize=10, loc="left")
    palette.style_axes(ax, grid_axis="x")
    fig.patch.set_facecolor(palette.SURFACE)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)


def plot_beeswarm(labels: list[str], values: np.ndarray, colour_by: np.ndarray,
                  path: Path, title: str) -> None:
    """One dot per (origin, target neighborhood) per group.

    Written directly rather than through shap.plots.beeswarm because the rows
    here are grouped columns, which an Explanation cannot carry a sensible
    `data` value for.
    """
    order = np.argsort(np.abs(values).mean(axis=0))
    fig, ax = plt.subplots(figsize=(7.5, 0.5 * len(labels) + 1.6))
    rng = np.random.default_rng(SEED)
    for row, group in enumerate(order):
        y = row + rng.uniform(-0.16, 0.16, size=values.shape[0])
        scatter = ax.scatter(values[:, group], y, c=colour_by[:, group], s=5,
                             cmap="coolwarm", alpha=0.6, linewidths=0)
    ax.axvline(0, color=palette.INK_MUTED, linewidth=0.8)
    ax.set_yticks(np.arange(len(order)))
    ax.set_yticklabels([labels[i] for i in order], fontsize=8)
    ax.set_xlabel("SHAP value (ILI per 100,000)", color=palette.INK_SECONDARY, fontsize=8)
    ax.set_title(title, color=palette.INK_PRIMARY, fontsize=10, loc="left")
    bar = fig.colorbar(scatter, ax=ax, pad=0.02, fraction=0.03)
    bar.set_label("Feature value (z-scored)", color=palette.INK_SECONDARY, fontsize=7)
    bar.ax.tick_params(labelsize=6, colors=palette.INK_MUTED)
    palette.style_axes(ax, grid_axis="x")
    fig.patch.set_facecolor(palette.SURFACE)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)


def plot_waterfall(labels: list[str], contributions: np.ndarray, errors: np.ndarray,
                   base: float, prediction: float, path: Path, title: str,
                   subtitle: str, max_display: int = 10) -> None:
    """One forecast, decomposed additively from the base value.

    shap.plots.waterfall takes no `ax` and draws on plt.gcf(), and its
    Explanation wants a scalar base with per-column `data` values that a grouped
    bar does not have. Drawing it here keeps the units, the ordering and the
    project palette under our control.
    """
    order = np.argsort(np.abs(contributions))[::-1]
    shown, rest = order[:max_display], order[max_display:]
    labels_shown = [labels[i] for i in shown]
    values, bars = contributions[shown], errors[shown]
    if len(rest):
        labels_shown.append(f"{len(rest)} smaller groups")
        values = np.append(values, contributions[rest].sum())
        bars = np.append(bars, np.sqrt(np.sum(errors[rest] ** 2)))

    n = len(labels_shown)
    fig, ax = plt.subplots(figsize=(9.0, 0.52 * n + 2.6))

    # Largest contribution on top; each bar starts where the previous one ended,
    # so the row order is also the cumulative path from base to prediction.
    starts = base + np.concatenate([[0.0], np.cumsum(values)[:-1]])
    span = max(abs(prediction - base), float(np.abs(values).max()), 1e-6)
    pad = span * 0.06

    for row in range(n):
        y = n - 1 - row
        value, start = values[row], starts[row]
        colour = palette.SERIES[1] if value >= 0 else palette.SERIES[0]
        ax.barh(y, value, left=start, color=colour, height=0.6,
                xerr=bars[row], error_kw={"ecolor": palette.INK_MUTED,
                                          "elinewidth": 0.7, "capsize": 2})
        end = start + value
        ax.text(end + (pad * 0.3 if value >= 0 else -pad * 0.3), y, f"{value:+.1f}",
                va="center", ha="left" if value >= 0 else "right",
                fontsize=7.5, color=palette.INK_SECONDARY)

    ax.axvline(base, color=palette.INK_MUTED, linestyle="--", linewidth=1.0, zorder=0)
    ax.axvline(prediction, color=palette.INK_PRIMARY, linewidth=1.4, zorder=0)
    ax.set_yticks(np.arange(n))
    ax.set_yticklabels(labels_shown[::-1], fontsize=8.5)
    ax.set_ylim(-0.9, n - 0.4)
    low = min(base, prediction, float((starts + values).min()), float(starts.min()))
    high = max(base, prediction, float((starts + values).max()), float(starts.max()))
    ax.set_xlim(low - pad * 3, high + pad * 3)
    ax.set_xlabel("Predicted ILI ED visits per 100,000",
                  color=palette.INK_SECONDARY, fontsize=8)
    ax.annotate(f"base\n{base:.1f}", xy=(base, -0.8), fontsize=7,
                color=palette.INK_MUTED, ha="center", va="center")
    ax.annotate(f"prediction\n{prediction:.1f}", xy=(prediction, -0.8), fontsize=7,
                color=palette.INK_PRIMARY, ha="center", va="center")
    palette.style_axes(ax, grid_axis="x")

    # Title and the wrapped footnote live on the figure, not the axes, so a long
    # subtitle cannot collide with the title or run off the canvas.
    fig.suptitle(title, color=palette.INK_PRIMARY, fontsize=11, x=0.01, ha="left",
                 y=0.995, va="top")
    wrapped = "\n".join(textwrap.wrap(subtitle, width=118))
    fig.text(0.01, 0.965, wrapped, fontsize=7.5, color=palette.INK_SECONDARY,
             ha="left", va="top")
    fig.patch.set_facecolor(palette.SURFACE)
    top = 0.955 - 0.018 * (wrapped.count("\n") + 1)
    fig.tight_layout(rect=(0, 0, 1, top))
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=palette.SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Which forecasts to explain
# ---------------------------------------------------------------------------

def interesting_samples(predictions: pd.DataFrame, horizon: int,
                        k: int) -> list[tuple[str, pd.Timestamp]]:
    """Season peak, worst error, and best in-season forecast.

    Read off the run's own predictions.csv, so every chosen week is one the
    reader can find in the run's actual_vs_predicted plot.
    """
    view = predictions.loc[predictions["horizon"].eq(horizon)].dropna(subset=["actual"])
    if view.empty:
        return []
    picks: list[tuple[str, pd.Timestamp]] = []
    peak = view.loc[view["actual"].idxmax()]
    picks.append((peak["neighborhood"], pd.Timestamp(peak["target_date"])))
    worst = view.loc[view["error"].abs().idxmax()]
    picks.append((worst["neighborhood"], pd.Timestamp(worst["target_date"])))
    in_season = view.loc[pd.DatetimeIndex(view["target_date"]).month.isin([10, 11, 12, 1, 2, 3])]
    if not in_season.empty:
        best = in_season.loc[in_season["error"].abs().idxmin()]
        picks.append((best["neighborhood"], pd.Timestamp(best["target_date"])))
    seen: list[tuple[str, pd.Timestamp]] = []
    for pick in picks:
        if pick not in seen:
            seen.append(pick)
    return seen[:k]


def _slug(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def resolve_waterfall(spec: str, city) -> tuple[str, pd.Timestamp]:
    """'Dorchester:2026-01-03' -> (canonical node name, timestamp).

    Accepts either the canonical name or the short plot label, resolved against
    the city being modelled rather than against Boston's list.
    """
    if ":" not in spec:
        raise SystemExit(f"error: --waterfall wants 'NODE:YYYY-MM-DD', got {spec!r}")
    name, _, date = spec.partition(":")
    name = name.strip()
    if name not in city.node_names:
        matches = [n for n, short in zip(city.node_names, city.short_names)
                   if short.lower() == name.lower()]
        if not matches:
            raise SystemExit(f"error: unknown {city.node_label} {name!r}. "
                             f"One of: {', '.join(city.short_names)}")
        name = matches[0]
    return name, pd.Timestamp(date.strip())


# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()
    if args.experiment in UNSUPPORTED:
        raise SystemExit(
            f"error: {args.experiment} — {UNSUPPORTED[args.experiment]}, so feature "
            f"importance is undefined for it. Supported: "
            f"{', '.join(sorted(n for n, e in EXPERIMENTS.items() if e.model == 'gcn_fusion'))}."
        )
    if args.experiment not in EXPERIMENTS:
        raise SystemExit(f"error: unknown experiment {args.experiment!r}. "
                         f"Available: {', '.join(sorted(EXPERIMENTS))}")
    experiment = EXPERIMENTS[args.experiment]
    if experiment.model == "dualtopo" and not args.skip_shap:
        # DualTopoSTGCN takes two dense adjacencies rather than an edge list, so
        # GraphBatch's block-diagonal trick does not apply to it. Permutation
        # importance is architecture-agnostic and does work.
        print("note: SHAP is implemented for the GCN-fusion models only; running "
              "permutation importance for this dualtopo model.", file=sys.stderr)
        args.skip_shap = True
    if args.variant != "all":
        experiment = replace(experiment, variant=args.variant)

    started = time.perf_counter()
    device = torch.device("cpu")

    # The window has to match the checkpoint's, not the registry default: a run
    # trained with --horizons 24 has a different split, hence a different
    # normalisation reference, and rebuilding samples with (1, 2) would explain
    # a model against inputs it never saw. The checkpoint records what it used.
    experiment = replace(experiment, window=window_from_checkpoint(
        load_checkpoint(experiment, args.checkpoint_dir), experiment))
    window = experiment.window

    city = resolve_city(args)
    rates = city.loaders.load_rates()
    data = variant_data(rates, experiment.variant)
    dataset = load_dataset(experiment.features, city=city, rates=data.available,
                           need_mbta=experiment.graph.transit)
    origins = valid_origins(dataset.week_index, window)
    split = split_origins(dataset.week_index, origins, window)
    graph = build_graph(experiment.graph, city=city,
                        flu_history=dataset.rates.loc[dataset.rates.index < window.test_start],
                        static=dataset.static, mbta=dataset.mbta)
    samples, norm = build_samples(dataset, split, experiment.features, window, graph,
                                  target=experiment.target, normalize=experiment.normalize)
    edge_index, edge_weight = graph.edge_tensors()

    checkpoint = load_checkpoint(experiment, args.checkpoint_dir)
    if experiment.model == "dualtopo":
        from influenza.models import DualTopoSTGCN

        if not np.allclose(checkpoint["flu_means"], norm.flu_mean):
            raise SystemExit(
                f"error: checkpoint normalisation differs. Re-run: python "
                f"Code/run_dualtopo.py --experiment {experiment.name}"
            )
        model = DualTopoSTGCN(
            n_nodes=graph.n_nodes, n_neigh=graph.n_neigh,
            input_window=window.lookback, spatial_channels=experiment.train.hidden[0],
            out_channels=experiment.train.hidden[1], n_horizons=len(window.horizons),
            fusion=args.fusion,
        ).to(device)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()
    else:
        guard(checkpoint, samples, edge_index, norm, len(window.horizons), experiment)
        model = InfluenzaGNN(
            n_node_feat=samples.n_feat, n_global=samples.n_global,
            n_horizons=len(window.horizons), hidden1=experiment.train.hidden[0],
            hidden2=experiment.train.hidden[1], fusion_out=experiment.train.hidden[2],
            dropout=experiment.train.dropout,
        ).to(device)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()

    horizon = args.horizon if args.horizon is not None else window.min_horizon
    if horizon not in window.horizons:
        raise SystemExit(f"error: horizon {horizon} is not in {window.horizons}")
    horizon_index = list(window.horizons).index(horizon)

    test = samples.subset(positions_to_rows(samples, split.test))
    train = samples.subset(positions_to_rows(samples, split.train))

    out = run_dir(experiment.name, experiment.variant, args.output_dir) / "importance"
    out.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 72}\n{experiment.name} | {experiment.variant} | horizon {horizon}\n{'=' * 72}")
    print(f"Graph: {graph.summary()}")
    print(f"Test origins: {len(split.test)} | features: {samples.n_feat} "
          f"| globals: {samples.n_global} | target: {experiment.target}")

    config: dict = {
        "model": experiment.name, "variant": experiment.variant, "horizon": horizon,
        "git_sha": git_sha(), "created": pd.Timestamp.now().isoformat(timespec="seconds"),
        "checkpoint": paths.display(args.checkpoint_dir /
                                    f"{experiment.name}_{experiment.variant}.pt"),
        "n_test_origins": len(split.test), "n_background": len(split.train),
        "explains": "the deterministic eval-mode forward, not the MC-dropout mean "
                    "reported in predictions.csv, and before the max(0, .) clip",
    }

    # ---------------- permutation importance ----------------
    if not args.skip_permutation:
        print(f"\nPermutation importance ({args.repeats} repeats)...")
        if experiment.model == "dualtopo":
            predictor = DualTopoPredictor(
                model=model, a_geo=checkpoint["a_geo"].to(device),
                a_corr=checkpoint["a_corr"].to(device), norm=norm,
                target=experiment.target, device=device, n_neigh=graph.n_neigh)
        else:
            predictor = GCNPredictor(model=model, edge_index=edge_index,
                                     edge_weight=edge_weight, norm=norm,
                                     target=experiment.target, device=device,
                                     n_neigh=graph.n_neigh)
        actual = np.stack([
            np.stack([
                dataset.rates.to_numpy(dtype=np.float32)[p + h] for h in window.horizons
            ], axis=-1) for p in test.positions
        ])
        target_dates = np.stack([
            [dataset.week_index[p + h] for h in window.horizons] for p in test.positions
        ])
        target_dates = np.repeat(target_dates[:, None, :], graph.n_neigh, axis=1)

        groups = feature_groups(samples.feature_names, samples.global_names)
        spec = PermutationSpec(n_repeats=args.repeats, seed=args.seed,
                               scheme=args.permute_scheme)
        frame = permutation_importance(predictor, test, actual, target_dates,
                                       window.horizons, spec=spec, groups=groups)
        frame.insert(0, "variant", experiment.variant)
        frame.insert(0, "model", experiment.name)
        frame.to_csv(out / "permutation_importance.csv", index=False)

        headline = frame.loc[frame["scope"].eq("group") & frame["segment"].eq("overall")
                             & frame["horizon"].eq(horizon)]
        plot_permutation(frame.loc[frame["segment"].eq("overall")
                                   & frame["horizon"].eq(horizon)],
                         out / "permutation_importance.png",
                         f"{experiment.name} ({experiment.variant}) — permutation "
                         f"importance at horizon {horizon}")
        print(f"  baseline RMSE {headline['baseline_RMSE'].iloc[0]:.3f}")
        print("  top groups by RMSE increase when shuffled:")
        for _, row in headline.nlargest(5, "delta_RMSE").iterrows():
            print(f"    {row['name']:<26} +{row['delta_RMSE']:6.3f} "
                  f"({row['delta_RMSE_pct']:+5.1f}%)  [{row['permutation_axis']}]")
        config["permutation"] = {"repeats": args.repeats, "scheme": args.permute_scheme,
                                 "seed": args.seed,
                                 "baseline_RMSE": float(headline["baseline_RMSE"].iloc[0])}

    # ---------------- SHAP ----------------
    if not args.skip_shap:
        from influenza.shapley import (
            GraphBatch, ShapResult, aggregate, check_batching, column_metadata,
            explain, flatten_inputs, group_columns, group_labels, to_rate_units,
        )

        wrapper = GraphBatch(model, edge_index, edge_weight, n_nodes=graph.n_nodes,
                             n_feat=samples.n_feat, n_neigh=graph.n_neigh)
        difference = check_batching(wrapper, model, test, edge_index, edge_weight, device)
        print(f"\nBatching check: max abs difference {difference:.3e}")
        if difference > 1e-4:
            raise SystemExit("error: the batched wrapper does not reproduce the per-sample "
                             "forward; SHAP values would be meaningless.")

        print(f"SHAP (expected gradients, nsamples={args.nsamples})...")
        values, variances, base = explain(
            wrapper, train, test, horizon_index=horizon_index,
            n_horizons=len(window.horizons), device=device,
            nsamples=args.nsamples, batch_size=args.batch_size, seed=args.seed)

        names, node_of, feature_of = column_metadata(samples, graph.node_names)
        anchor_columns = np.flatnonzero(node_of >= graph.n_neigh)
        anchor_max = float(np.abs(values[:, :, anchor_columns]).max()) if anchor_columns.size else 0.0
        print(f"Anchor-column check: max |SHAP| over {anchor_columns.size} anchor columns "
              f"= {anchor_max:.3e}")
        if anchor_max > 0.0:
            raise SystemExit("error: anchor columns carry non-zero attribution, so the "
                             "column bookkeeping is wrong.")

        x_flat, g_flat = flatten_inputs(test)
        with torch.no_grad():
            raw_pred = wrapper(torch.tensor(x_flat, device=device),
                               torch.tensor(g_flat, device=device)).cpu().numpy()
        raw_pred = raw_pred.reshape(-1, graph.n_neigh, len(window.horizons))[:, :, horizon_index]
        reconstruction = np.abs(base[None, :] + values.sum(axis=2) - raw_pred)
        spread = float(np.abs(raw_pred - raw_pred.mean()).mean())
        share = float(np.median(reconstruction)) / spread * 100 if spread else np.nan
        print(f"Local accuracy: median reconstruction error is {share:.1f}% of the "
              f"prediction spread")
        if share > 20:
            print("warning: raise --nsamples; the attributions have not converged",
                  file=sys.stderr)

        if args.units == "rate":
            values, base_values = to_rate_units(values, base, test.anchors, norm,
                                                experiment.target)
            variances = variances * (norm.flu_std.flatten()[None, :, None] ** 2)
            unit_label = "rate_per_100k"
        else:
            base_values = np.broadcast_to(base[None, :], values.shape[:2]).copy()
            unit_label = "normalized_delta"

        origin_dates = np.asarray([dataset.week_index[p] for p in test.positions])
        result = ShapResult(values=values, variances=variances, base_values=base_values,
                            data=x_flat, column_names=names, node_of_column=node_of,
                            feature_of_column=feature_of, horizon=horizon,
                            origin_dates=origin_dates, units=unit_label)

        np.savez_compressed(
            out / "shap_values.npz", values=values, variances=variances,
            base_values=base_values, data=np.concatenate([x_flat, g_flat], axis=1),
            column_names=np.asarray(names), node_of_column=node_of,
            feature_of_column=feature_of, horizon=horizon,
            origin_dates=origin_dates.astype("datetime64[ns]").astype("int64"),
            flu_mean=norm.flu_mean, flu_std=norm.flu_std, anchors=test.anchors,
            units=unit_label,
        )

        source_of = {}
        for group, members in feature_groups(samples.feature_names,
                                             samples.global_names).items():
            for member in members:
                source_of[member] = group

        # Pooled view: re-index every target node into its own locality frame so
        # "flu lags — own" means the same thing in every row before pooling.
        pooled_labels = group_labels(result, source_of)
        pooled_values, pooled_colour = [], []
        all_data = np.concatenate([x_flat, g_flat], axis=1)
        for node in range(graph.n_neigh):
            _, index = group_columns(result, node, graph.W, source_of, pooled_labels)
            pooled_values.append(aggregate(values[:, node, :], index, len(pooled_labels)))
            counts = np.bincount(index, minlength=len(pooled_labels))
            summed = aggregate(all_data, index, len(pooled_labels))
            pooled_colour.append(summed / np.maximum(counts, 1))
        pooled = np.concatenate(pooled_values)
        colour = np.concatenate(pooled_colour)

        keep = np.flatnonzero(np.abs(pooled).max(axis=0) > 0)
        dropped = [pooled_labels[i] for i in range(len(pooled_labels)) if i not in keep]
        labels_kept = [pooled_labels[i] for i in keep]

        pd.DataFrame({"group": labels_kept,
                      "mean_abs_shap": np.abs(pooled[:, keep]).mean(axis=0)}
                     ).sort_values("mean_abs_shap", ascending=False
                                   ).to_csv(out / "shap_group_importance.csv", index=False)

        unit_note = ("ILI per 100,000" if unit_label == "rate_per_100k"
                     else "normalized delta")
        plot_group_bar(labels_kept, np.abs(pooled[:, keep]).mean(axis=0),
                       out / "shap_bar.png",
                       f"{experiment.name} ({experiment.variant}) — mean |SHAP| by group, "
                       f"horizon {horizon} ({unit_note})")
        plot_beeswarm(labels_kept, pooled[:, keep], colour[:, keep],
                      out / "shap_beeswarm_groups.png",
                      f"{experiment.name} ({experiment.variant}) — SHAP by group over "
                      f"{len(split.test)} origins x {graph.n_neigh} neighborhoods, "
                      f"horizon {horizon}")
        print(f"  {len(labels_kept)} groups plotted; {len(dropped)} constant across "
              f"origins and omitted: {', '.join(dropped) or 'none'}")

        # ---------------- waterfalls ----------------
        predictions_path = out.parent / "predictions.csv"
        picks: list[tuple[str, pd.Timestamp]] = [resolve_waterfall(s, city)
                                                 for s in (args.waterfall or [])]
        if predictions_path.exists() and args.auto_waterfalls:
            picks += interesting_samples(pd.read_csv(predictions_path, parse_dates=["target_date"]),
                                         horizon, args.auto_waterfalls)
        elif not picks:
            print(f"  (no {predictions_path} and no --waterfall; skipping waterfalls)")

        origin_lookup = {pd.Timestamp(d): i for i, d in enumerate(origin_dates)}
        written = 0
        for neighborhood, target_date in picks:
            origin = pd.Timestamp(target_date) - pd.Timedelta(weeks=horizon)
            if origin not in origin_lookup:
                print(f"  skipping {neighborhood} {target_date.date()}: origin "
                      f"{origin.date()} is not a test origin", file=sys.stderr)
                continue
            row = origin_lookup[origin]
            node = list(city.node_names).index(neighborhood)
            labels, index = group_columns(result, node, graph.W, source_of, pooled_labels)
            contributions = aggregate(values[row, node, :], index, len(labels))
            errors = np.sqrt(aggregate(variances[row, node, :], index, len(labels)))
            show = np.flatnonzero(np.abs(contributions) > 0)
            base_here = float(base_values[row, node])
            prediction = base_here + float(contributions.sum())

            anchor_level = float(test.anchors[row, node] * norm.flu_std.flatten()[node]
                                 + norm.flu_mean.flatten()[node])
            subtitle = (f"origin {origin.date()} → target {pd.Timestamp(target_date).date()} "
                        f"({horizon} week{'s' if horizon > 1 else ''} ahead). ")
            if experiment.target == "delta" and unit_label == "rate_per_100k":
                subtitle += (f"Base {base_here:.1f} = origin-week level {anchor_level:.1f} "
                             f"+ average predicted change {base_here - anchor_level:+.1f}. ")
            subtitle += ("Static demographics and anchor nodes are omitted: they do not vary "
                         "across origins, so SHAP is exactly zero for them.")

            path = out / f"waterfall_{_slug(city.short_names[node])}_{origin.date()}_h{horizon}.png"
            plot_waterfall([labels[i] for i in show], contributions[show], errors[show],
                           base_here, prediction, path,
                           f"{neighborhood} — {experiment.name} ({experiment.variant})",
                           subtitle, max_display=args.max_display)
            written += 1
            print(f"  {path.name}: base {base_here:.1f} → prediction {prediction:.1f}")

        config["shap"] = {
            "explainer": "gradient", "nsamples": args.nsamples, "seed": args.seed,
            "units": unit_label, "batching_max_abs_diff": difference,
            "anchor_max_abs_shap": anchor_max,
            "local_accuracy_pct_of_spread": share,
            "constant_groups_omitted": dropped,
            "waterfalls": written,
        }

    config["wall_clock_s"] = round(time.perf_counter() - started, 1)
    (out / "importance_config.json").write_text(
        json.dumps(config, indent=2, default=str) + "\n")
    print(f"\nOutputs: {out}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--experiment", default="gnn_multiedge")
    parser.add_argument("--variant", default="all",
                        help="Default: the experiment's registry variant.")
    parser.add_argument("--horizon", type=int, default=None,
                        help="Which horizon to explain. Default: the window's shortest.")
    parser.add_argument("--output-dir", type=Path, default=paths.RESULTS_DIR)
    parser.add_argument("--checkpoint-dir", type=Path, default=paths.CHECKPOINT_DIR)
    parser.add_argument("--waterfall", action="append", default=None,
                        metavar="NAME:YYYY-MM-DD",
                        help="Explain one forecast. The date is the TARGET week. Repeatable.")
    parser.add_argument("--auto-waterfalls", type=int, default=3,
                        help="Season peak, worst error and best in-season forecast.")
    parser.add_argument("--max-display", type=int, default=10,
                        help="Bars in a waterfall before the tail is collapsed.")
    parser.add_argument("--nsamples", type=int, default=500,
                        help="Expected-gradient draws. Reconstruction error falls as "
                             "1/sqrt(nsamples); 500 lands near 3%% of the prediction spread.")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--repeats", type=int, default=20, help="Permutation repeats.")
    parser.add_argument("--permute-scheme", default="shared", choices=["shared", "per_node"])
    parser.add_argument("--fusion", choices=["concat", "mean", "max"], default="concat",
                        help="Dual-Topo fusion operator; must match the trained run.")
    parser.add_argument("--units", default="rate", choices=["rate", "delta"])
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--skip-shap", action="store_true")
    parser.add_argument("--skip-permutation", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    main()
