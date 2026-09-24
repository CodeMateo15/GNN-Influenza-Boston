#!/usr/bin/env python3
"""Leave-one-out ablation study, reported against a measured seed noise floor.

The point of this script is the last two columns. Ablation tables invite reading
a 0.01 difference as a finding, and on this dataset that is not safe. So:

  * Every arm runs at the SAME seed count as the reference, and the reference is
    re-run rather than quoted from a different configuration.
  * The noise floor is MEASURED, not inferred. Two extra reference ensembles are
    trained on disjoint seed blocks (`gnn_st_ref_b` at seed 142, `gnn_st_ref_c`
    at 242). The spread of those three identical-configuration ensembles is what
    run-to-run noise actually costs, and a delta smaller than it is not a
    finding. The previous version took the standard deviation of the arm deltas,
    which moved the floor whenever the arm list changed -- 0.007 to 0.013 in one
    regeneration, with no new measurement behind it.
  * Each arm is also compared to the reference neighborhood by neighborhood.
    `metrics.csv` carries a row per node, so "helped in 15 of 21 neighborhoods,
    p=0.03" is available and is a far better guide than one pooled number.

    python Code/run_ablation.py --horizons 2 --n-seeds 3
    python Code/run_ablation.py --arms gnn_st_noweather --horizons 1,2,4
    python Code/run_ablation.py --collect-only --horizons 1,2,4 --n-seeds 10

Feature groups are removed and the model REFIT, not permuted. Half of these
groups are constant within a forecast origin -- static demographics get exactly
zero from expected-gradient attribution by construction -- so permutation cannot
measure them and a retrain is the only rigorous test. METHODS.md makes the same
point about static covariates.
"""

from __future__ import annotations

# Thread pinning must happen before numpy or torch is imported: BLAS reads its
# thread count from the environment at import time. See influenza/threads.py.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import influenza.threads  # noqa: F401  (import for its side effect)

import argparse
import dataclasses
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from influenza import paths  # noqa: E402
from influenza.cities import get as get_city  # noqa: E402
from influenza.cli import add_city_arg  # noqa: E402
from influenza.config import EXPERIMENTS  # noqa: E402

REFERENCE = "gnn_st"

# Identical configuration to the reference, different seed block. run_gnn.py
# builds its seeds as `train.seed + i` (run_gnn.py:244), so a different --seed
# gives a disjoint ensemble. These exist only to measure the noise floor.
REPLICATES = (("gnn_st_ref_b", 142), ("gnn_st_ref_c", 242))

# Leave-one-out. `gnn_st_noglobals` and `gnn_st_noseason` used to live here and
# were removed: the default now has globals_=() and use_seasonality=False, so
# both arms were byte-identical to the reference and their rows were measuring
# nothing but seed noise. The questions they used to ask are now asked by the
# add-one-in arms `gnn_st_globals` and `gnn_st_season` below. IDENTITY_GUARD
# below stops that class of mistake coming back.
FEATURE_ARMS = ("gnn_st_noweather", "gnn_st_nodemofeat", "gnn_st_nodemoedge",
                "gnn_st_nodemo", "gnn_st_noimputedflag", "gnn_st_lagsonly",
                "gnn_st_lean")
ADD_IN_ARMS = ("gnn_st_covid_rsv", "gnn_st_wastewater", "gnn_st_vaccination",
               "gnn_st_globals", "gnn_st_season")
DESIGN_ARMS = ("gnn_st_delta", "gnn_st_level", "gnn_st_noadapt",
               "gnn_st_relations", "gnn_st_nopearson", "gnn_st_tiny",
               # Timing arms. `slopeweight` and `trendblend` are recorded
               # negatives; `joint` is the control that showed the gain in
               # `gnn_cascade` comes from training two horizons together rather
               # than from the cascade anchor, which is why it has to stay in the
               # table rather than being dropped as uninteresting.
               "gnn_st_slopeweight", "gnn_st_trendblend", "gnn_st_joint",
               # Named without the gnn_st_ prefix because it was briefly promoted
               # to the h=2 leaderboard; listing it here is what keeps
               # compare_models.py from ranking it against its own parent now
               # that the promotion has been withdrawn.
               "gnn_cascade", "gnn_cascade_h4", "gnn_st_joint_h4")
# Removing the hand-built edges is not enough to make the model graph-free: the
# adaptive adjacency is itself a learned dense graph. So `gnn_st_nograph` turns
# off spatial mixing altogether and is the arm the project's central claim rests
# on -- it is what makes "having a graph is worth X" a measurement rather
# than an assertion. It belongs in the default table, not in a side invocation.
GRAPH_ARMS = ("gnn_st_nocorr", "gnn_st_geoonly", "gnn_st_adaptiveonly",
              "gnn_st_nograph")

GROUPS = {"feature (leave one out)": FEATURE_ARMS,
          "feature (add one in)": ADD_IN_ARMS,
          "design": DESIGN_ARMS,
          "graph": GRAPH_ARMS}

ALL_ARMS = FEATURE_ARMS + ADD_IN_ARMS + DESIGN_ARMS + GRAPH_ARMS


def spec_of(arm: str) -> dict:
    """Every field of an Experiment except its name and prose, flattened."""
    experiment = EXPERIMENTS[arm]
    flat: dict = {}
    for field in dataclasses.fields(experiment):
        if field.name in ("name", "note"):
            continue
        value = getattr(experiment, field.name)
        if dataclasses.is_dataclass(value):
            for sub in dataclasses.fields(value):
                flat[f"{field.name}.{sub.name}"] = getattr(value, sub.name)
        else:
            flat[field.name] = value
    return flat


def identity_guard(arms: tuple[str, ...]) -> None:
    """Refuse to run an arm that is config-identical to the reference.

    This is the check that was missing. When a group is dropped from the default
    the corresponding leave-one-out arm silently becomes a no-op -- the
    `dataclasses.replace` still succeeds, the run still trains, and its row still
    lands in the table looking like a result. `gnn_st_noglobals` sat in the
    default table for weeks reporting +0.024 "better without it" against a model
    it was identical to. Also catch arms identical to EACH OTHER, which is how
    gnn_st_nodemo, gnn_st_nodemo_noglobals and gnn_st_minimal became three names
    for one experiment.
    """
    reference = spec_of(REFERENCE)
    degenerate = [a for a in arms if spec_of(a) == reference]
    if degenerate:
        raise SystemExit(
            f"These arms are config-identical to {REFERENCE}, so they measure "
            f"nothing: {', '.join(degenerate)}.\n"
            f"The default already has that group switched off. Use the "
            f"corresponding add-one-in arm instead, or drop the arm.")

    seen: dict[tuple, str] = {}
    for arm in arms:
        key = tuple(sorted((k, repr(v)) for k, v in spec_of(arm).items()))
        if key in seen:
            raise SystemExit(
                f"`{arm}` is config-identical to `{seen[key]}`. Two names, one "
                f"experiment -- running both would report the same model twice "
                f"and pass seed noise off as a difference between them.")
        seen[key] = arm


def ablation_root(horizon: int, n_seeds: int, study: str,
                  city: str = "boston") -> Path:
    """results/[<city>/]_ablation/<study>/hNN_sM/.

    Boston keeps the historical top-level path, so every committed arm under
    results/_ablation/ stays exactly where it is.
    """
    return (paths.city_root(city) / "_ablation" / study
            / f"h{horizon:02d}_s{n_seeds}")


def read_metrics(name: str, horizon: int, n_seeds: int, study: str,
                 variant: str, city: str = "boston") -> dict | None:
    directory = ablation_root(horizon, n_seeds, study, city) / name / variant
    path = directory / "metrics.csv"
    if not path.exists():
        return None
    frame = pd.read_csv(path)
    overall = frame[frame["segment"].eq("overall")]
    row: dict = {"arm": name, "horizon": horizon}
    for scope in ("macro", "pooled"):
        subset = overall[overall["scope"].eq(scope)]
        if not subset.empty:
            row[f"Corr_{scope}"] = float(subset["Corr"].iloc[0])
            row[f"RMSE_{scope}"] = float(subset["RMSE"].iloc[0])
    spread = directory / "seed_spread.csv"
    if spread.exists():
        seeds = pd.read_csv(spread)
        row["n_seeds"] = int(len(seeds))
        row["best_epoch_range"] = f"{seeds['best_epoch'].min()}-{seeds['best_epoch'].max()}"
    config = directory / "run_config.json"
    if config.exists():
        import json
        payload = json.loads(config.read_text())
        row["epochs_run"] = payload.get("epochs_run")
        row["n_node_features"] = payload.get("n_node_features")
        row["n_global"] = payload.get("n_global")
        counts = payload.get("graph_counts") or {}
        row["n_edges"] = sum(counts.values()) if counts else None
    return row


def per_neighborhood(name: str, horizon: int, n_seeds: int, study: str,
                     variant: str, city: str = "boston") -> pd.Series | None:
    """Corr for each scored neighborhood, indexed by name.

    The macro number is a mean over these. Keeping them lets an arm be tested
    against the reference as 21 paired observations instead of one.
    """
    path = ablation_root(horizon, n_seeds, study, city) / name / variant / "metrics.csv"
    if not path.exists():
        return None
    frame = pd.read_csv(path)
    subset = frame[frame["segment"].eq("overall") & frame["scope"].eq("neighborhood")]
    if subset.empty:
        return None
    return subset.set_index("neighborhood")["Corr"].sort_index()


def paired_verdict(arm_corr: pd.Series | None,
                   ref_corr: pd.Series | None) -> tuple[str, float | None]:
    """How consistently did this arm differ from the reference, across nodes?"""
    if arm_corr is None or ref_corr is None:
        return "", None
    shared = arm_corr.index.intersection(ref_corr.index)
    if len(shared) < 6:
        return "", None
    delta = (arm_corr[shared] - ref_corr[shared]).astype(float)
    better = int((delta > 0).sum())
    total = int(len(delta))
    try:
        from scipy.stats import wilcoxon
        p = float(wilcoxon(delta).pvalue) if delta.abs().sum() > 0 else 1.0
    except Exception:
        p = None
    return f"{better}/{total}", p


def noise_floor(table: pd.DataFrame, horizon: int) -> tuple[float | None, str]:
    """Spread of identical-configuration ensembles at this horizon.

    Returns (floor, how_it_was_obtained). The replicates differ from the
    reference only in their seed block, so any spread between them is exactly
    the run-to-run noise an arm's delta has to clear.
    """
    names = [REFERENCE] + [n for n, _ in REPLICATES]
    values = [float(v) for v in
              table[table["arm"].isin(names)]["Corr_macro"].dropna().tolist()]
    if len(values) >= 2:
        # The full observed range across identical configurations, used as the
        # threshold directly. Three ensembles is too few to estimate a standard
        # deviation worth quoting, but the range is a statement of fact: these
        # models differ only in seed and they still spanned this much. An arm
        # that moves the metric less than that has not been shown to do
        # anything. This is deliberately conservative -- with n=3 the true
        # spread is more likely wider than this than narrower.
        label = f"{len(values)} reference ensembles"
        if len(values) == 2:
            label += " (thin -- two is barely a range)"
        return max(values) - min(values), label

    subset = table[~table["arm"].isin(names[1:])]
    if len(subset) > 3 and not subset[subset["arm"].eq(REFERENCE)].empty:
        deltas = subset["Corr_macro"] - float(
            subset[subset["arm"].eq(REFERENCE)]["Corr_macro"].iloc[0])
        near = deltas[np.abs(deltas) < 0.05]
        if len(near) > 2:
            return float(np.std(near)), "across-arm spread (FALLBACK, not a measurement)"
    return None, "unavailable"


def report(table: pd.DataFrame, horizon: int, noise: float | None, source: str,
           paired: dict[str, tuple[str, float | None]]) -> str:
    reference = table[table["arm"].eq(REFERENCE)]
    if reference.empty:
        return f"No {REFERENCE} row at h={horizon}; nothing to compare against."
    base_macro = float(reference["Corr_macro"].iloc[0])
    base_pooled = float(reference["Corr_pooled"].iloc[0])
    base_rmse = float(reference["RMSE_pooled"].iloc[0])

    lines = [f"## Horizon {horizon}", "",
             f"Reference `{REFERENCE}`: macro Corr {base_macro:.3f}, "
             f"pooled {base_pooled:.3f}, RMSE {base_rmse:.2f}. "
             f"Every arm below is the same configuration with one change, "
             f"refit at the same seed count."]
    if noise is not None:
        if source.startswith("across-arm"):
            basis = (f"Inferred from the {source} -- no reference replicates were "
                     f"run, so this is a guess at the noise, not a measurement of "
                     f"it, and it moves when the arm list moves.")
        else:
            basis = (f"Measured as the full range across {source}: identical "
                     f"configurations differing only in which seeds they drew.")
        lines += ["", f"**How big does a difference have to be before it means "
                      f"anything? {noise:.3f} macro Corr.** {basis} A delta "
                      f"smaller than that is seed luck, not a finding."]
        replicates = table[table["arm"].isin([n for n, _ in REPLICATES])]
        if not replicates.empty:
            spread = ", ".join(f"{float(v):.3f}" for v in
                               [base_macro] + replicates["Corr_macro"].tolist())
            lines.append(f"Reference ensembles at this horizon scored {spread}.")
    lines.append("")

    for label, arms in GROUPS.items():
        subset = table[table["arm"].isin(arms)]
        if subset.empty:
            continue
        lines += [f"### {label}", "",
                  "| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        ordered = subset.assign(_d=subset["Corr_macro"] - base_macro).sort_values("_d")
        for _, row in ordered.iterrows():
            d_macro = row["Corr_macro"] - base_macro
            # The sign means opposite things in the two kinds of arm, and getting
            # this backwards is the easiest way to publish a wrong conclusion.
            # Leave-one-out: the arm REMOVES a group, so a negative delta means
            # removing it hurt -- the group was doing something. Add-one-in: the
            # arm ADDS a group, so a negative delta means adding it hurt.
            added = label.startswith("feature (add")
            if noise is None:
                verdict = ""
            elif abs(d_macro) < noise:
                verdict = "inside noise"
            elif added:
                verdict = ("**adding it helps**" if d_macro > 0
                           else "**adding it HURTS**")
            else:
                verdict = ("**earns its place**" if d_macro < 0
                           else "**better without it**")
            share, p = paired.get(row["arm"], ("", None))
            p_text = "" if p is None else (f"{p:.3f}" if p >= 0.001 else "<0.001")
            lines.append(f"| `{row['arm']}` | {row['Corr_macro']:.3f} | {d_macro:+.3f} | "
                         f"{row['Corr_pooled']:.3f} | "
                         f"{row['RMSE_pooled']:.2f} | {share} | {p_text} | {verdict} |")
        lines.append("")

    lines += ["`Δ macro` is this arm minus the reference. In a **leave-one-out** row "
              "the arm removes a group, so a negative Δ means the model got worse "
              "without it and the group was earning its place. In an **add-one-in** "
              "row the arm adds a group, so a negative Δ means adding it made things "
              "worse. Same sign, opposite meaning -- read the section heading.", "",
              "`nbhds improved` counts how many of the scored neighborhoods this arm "
              "beat the reference in, and `p` is a Wilcoxon signed-rank test on those "
              "paired per-neighborhood differences. A verdict backed by a lopsided "
              "count and a small p is worth more than one that rests on the macro "
              "average alone, because the macro average can be moved by one node.", ""]
    return "\n".join(lines)


def train(names: list[tuple[str, str, int | None]], horizon: int, n_seeds: int,
          study: str, jobs: int, log_dir: Path, done: int, total: int,
          city: str = "boston") -> int:
    """Launch run_gnn.py per arm, tee-ing stdout so progress stays visible."""
    for start in range(0, len(names), jobs):
        batch = names[start:start + jobs]
        processes = []
        for name, arm, seed in batch:
            done += 1
            # run_progress.py parses this; see the status-line contract in run_progress.py.
            # A task runner counts tasks on the epoch axis, not the seed axis --
            # `Budget: <n_tasks> epochs x 1 seeds` above is the matching
            # denominator. Printing `--- seed <arm> (done/total) ---` here instead
            # set n_seeds to the task count and squared the denominator.
            print(f"Epoch {done} | arm {name} h={horizon}", flush=True)
            command = [
                sys.executable, "-u",
                str(Path(__file__).resolve().parent / "run_gnn.py"),
                "--experiment", arm, "--name", name,
                "--city", city,
                "--variant", EXPERIMENTS[arm].variant,
                "--horizons", str(horizon), "--n-seeds", str(n_seeds),
                "--output-dir", str(ablation_root(horizon, n_seeds, study, city)),
                "--checkpoint-dir",
                str(paths.city_root(city, paths.CHECKPOINT_DIR) / "ablation" / study
                    / f"h{horizon:02d}_s{n_seeds}"),
                "--no-carbon"]
            if seed is not None:
                command += ["--seed", str(seed)]
            log_dir.mkdir(parents=True, exist_ok=True)
            handle = (log_dir / f"h{horizon:02d}_{name}.log").open("w")
            processes.append((name, handle, subprocess.Popen(
                command, stdout=handle, stderr=subprocess.STDOUT, text=True)))
        for name, handle, process in processes:
            process.wait()
            handle.close()
            status = "ok" if process.returncode == 0 else f"exit{process.returncode}"
            print(f"    {name}: {status}", flush=True)
            if process.returncode != 0:
                tail = (log_dir / f"h{horizon:02d}_{name}.log").read_text().splitlines()
                for line in tail[-3:]:
                    print(f"      {line}", flush=True)
    return done


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--arms", default="",
                        help="Comma-separated. Default: every ablation arm. The "
                             "reference is always included.")
    parser.add_argument("--horizons", default="2")
    parser.add_argument("--n-seeds", type=int, default=3,
                        help="Same count for every arm including the reference. "
                             "Three is enough to rank; the headline uses ten.")
    parser.add_argument("--study", default="main",
                        help="Names the output tree and the summary files. Keep "
                             "distinct studies apart: the seed count alone is "
                             "not a unique key, and reusing it once overwrote a "
                             "measurement that could not be regenerated.")
    add_city_arg(parser)
    parser.add_argument("--jobs", type=int, default=4,
                        help="Arms to train concurrently. torch is pinned to one "
                             "thread per process, so this scales with cores.")
    parser.add_argument("--no-replicates", action="store_true",
                        help="Skip the two extra reference ensembles. The noise "
                             "floor then falls back to an inferred estimate, "
                             "which is labelled as such in the report.")
    parser.add_argument("--collect-only", action="store_true")
    parser.add_argument("--log-dir", default=None,
                        help="Where per-arm stdout is tee'd. Defaults to the "
                             "session scratchpad that run_progress.py watches.")
    args = parser.parse_args()

    city = get_city(args.city)
    horizons = tuple(int(h) for h in args.horizons.split(","))
    arms = tuple(a for a in args.arms.split(",") if a) if args.arms else ALL_ARMS
    unknown = [a for a in arms if a not in EXPERIMENTS]
    if unknown:
        raise SystemExit(f"Unknown arms: {unknown}. Available: "
                         f"{', '.join(sorted(EXPERIMENTS))}")
    arms = tuple(a for a in arms if a != REFERENCE)
    identity_guard(arms)

    variant = EXPERIMENTS[REFERENCE].variant
    if variant not in city.variants:
        raise SystemExit(f"the ablation reference runs on --variant {variant}, which "
                         f"{city.label} does not have. {city.label} supports: "
                         f"{', '.join(city.variants)}.")
    replicates = () if args.no_replicates else REPLICATES
    # (output name, experiment to build, seed override)
    jobs: list[tuple[str, str, int | None]] = [(REFERENCE, REFERENCE, None)]
    jobs += [(name, REFERENCE, seed) for name, seed in replicates]
    jobs += [(a, a, None) for a in arms]

    log_dir = Path(args.log_dir) if args.log_dir else paths.LOG_DIR / "ablation_logs"

    rows: list[dict] = []
    if not args.collect_only:
        pending_by_h = {
            h: [j for j in jobs
                if read_metrics(j[0], h, args.n_seeds, args.study, variant,
                                city.name) is None]
            for h in horizons}
        total = sum(len(v) for v in pending_by_h.values())
        # run_progress.py denominator; tasks expressed as epochs x 1 seeds so its
        # arithmetic works unchanged. See the status-line contract in run_progress.py.
        print(f"Budget: {total} epochs x 1 seeds", flush=True)
        done = 0
        for horizon in horizons:
            root = ablation_root(horizon, args.n_seeds, args.study, city.name)
            root.mkdir(parents=True, exist_ok=True)
            pending = pending_by_h[horizon]
            print(f"\nh={horizon}: {len(pending)} of {len(jobs)} runs to train "
                  f"({args.n_seeds} seeds each, {args.jobs} at a time)", flush=True)
            done = train(pending, horizon, args.n_seeds, args.study, args.jobs,
                         log_dir, done, total, city.name)

    for horizon in horizons:
        for name, _, _ in jobs:
            row = read_metrics(name, horizon, args.n_seeds, args.study, variant,
                               city.name)
            if row:
                rows.append(row)

    if not rows:
        raise SystemExit("No metrics found.")
    table = pd.DataFrame(rows)
    out = paths.city_root(city.name) / "_ablation"
    out.mkdir(parents=True, exist_ok=True)
    stem = f"ablation_{args.study}_s{args.n_seeds}"
    table.to_csv(out / f"{stem}.csv", index=False)

    provenance = check_comparability(table)

    sections = ["# Feature and design ablations", "",
                "Each arm is `gnn_st` with exactly one change, refit from scratch. "
                "Feature groups are removed and the model retrained rather than "
                "permuted, because several groups are constant within a forecast "
                "origin and permutation cannot measure them.", ""]
    if provenance:
        sections += provenance + [""]
    for horizon in horizons:
        subset = table[table["horizon"].eq(horizon)]
        noise, source = noise_floor(subset, horizon)
        ref_corr = per_neighborhood(REFERENCE, horizon, args.n_seeds, args.study, variant,
                                    city.name)
        paired = {
            name: paired_verdict(
                per_neighborhood(name, horizon, args.n_seeds, args.study, variant,
                                 city.name),
                ref_corr)
            for name in subset["arm"].tolist()}
        sections.append(report(subset, horizon, noise, source, paired))
    text = "\n".join(sections)
    (out / f"{stem}.md").write_text(text)
    print("\n" + text)
    print(f"Wrote {paths.display(out)}/{stem}.{{csv,md}}")
    # run_progress.py completion marker; see the status-line contract in run_progress.py.
    print(f"Outputs: {paths.display(out)}/{stem}.md", flush=True)


def check_comparability(table: pd.DataFrame) -> list[str]:
    """Assert the arms were produced by one code version on one dataset.

    The study this replaced was invalidated by exactly this going unchecked: 20
    of 23 arms were fit on a 108-edge transit-era graph with 3 global covariates
    and a 300-epoch budget, while the graph arms they were differenced against
    used the current 107-edge graph with none. Nothing in the table said so.

    Care is needed about WHICH columns must match. A feature arm is supposed to
    have fewer node features and a graph arm fewer edges -- that is the whole
    point of them -- so requiring those to be constant across all arms would fire
    on every valid run. Two things must hold instead:

      * The training budget is the same for everyone. Nothing in this study
        varies it, so a difference means the runs came from different code.
      * The reference and its replicates agree on everything. They are the same
        configuration by construction, so any disagreement between them means the
        graph or the input data changed underneath the study.
    """
    notes: list[str] = []
    replicate_names = [REFERENCE] + [n for n, _ in REPLICATES]
    references = table[table["arm"].isin(replicate_names)]

    if "epochs_run" in table.columns:
        budgets = sorted({int(v) for v in table["epochs_run"].dropna().tolist()})
        if len(budgets) > 1:
            notes.append(
                f"> **Warning: the training budget is not constant across arms** "
                f"({budgets} epochs). Nothing in this study varies the budget, so "
                f"these runs came from different versions of the code and the "
                f"deltas below mix more than one change.")

    for column, label in (("n_edges", "graph edge count"),
                          ("n_global", "global covariate count"),
                          ("n_node_features", "node feature count")):
        if column not in references.columns:
            continue
        values = sorted({v for v in references[column].dropna().tolist()})
        if len(values) > 1:
            notes.append(
                f"> **Warning: the {label} differs between the reference and its "
                f"replicates** ({values}). Those runs are the same configuration "
                f"by construction, so the graph or the input data changed while "
                f"the study was running. The noise floor below is not measuring "
                f"seed variation alone.")

    if not notes:
        shared = []
        if "epochs_run" in table.columns and table["epochs_run"].notna().any():
            shared.append(f"{int(table['epochs_run'].dropna().iloc[0])} epochs")
        for column, label in (("n_edges", "edges"), ("n_node_features", "node features"),
                              ("n_global", "global covariates")):
            if column in references.columns and references[column].notna().any():
                shared.append(f"{int(references[column].dropna().iloc[0])} {label}")
        if shared:
            notes.append(
                f"All arms ran on the same budget and the reference ensembles "
                f"agree on the inputs ({', '.join(shared)}), so the deltas below "
                f"isolate the one change named in each row. Feature and graph "
                f"arms differ from the reference in their own feature or edge "
                f"count by design; that is what they measure.")
    return notes


if __name__ == "__main__":
    main()
