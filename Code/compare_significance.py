"""Is one model's lead over another bigger than chance on this test season?

compare_models.py ranks models on one number each. A ranking cannot say whether
the gap between first and second would survive a different mix of weeks, and
on one season of ~49 weeks it often would not. This script answers that, for a
reference model (default `gnn_st`) against every other model at each horizon:

  * the difference in pooled MAE, RMSE, WIS-95 and macro Corr, each with a 95%
    confidence interval from a moving-block bootstrap over target weeks;
  * a Diebold-Mariano p-value on the weekly absolute error and on weekly WIS-95,
    Holm-adjusted across the comparisons at that horizon;
  * each model's skill against persistence, as relative WIS (below 1 = better
    than carrying this week forward).

The method and why the unit is the week, not the cell, is in
influenza/scoring.py. Reads committed predictions.csv only -- no retraining:

    python Code/compare_significance.py
    python Code/compare_significance.py --city columbus --reference gnn_st
    python Code/compare_significance.py --results-dir results/backtest_2023_24

Writes significance.csv and significance.md beside each horizon's leaderboard.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from influenza import paths
from influenza import scoring
from influenza.cities import get as get_city
from influenza.cli import add_city_arg, city_results_dir

METRICS = ("MAE", "RMSE", "WIS", "WIS95", "Corr")


def horizon_roots(results_root: Path) -> list[tuple[int, Path]]:
    """(h, results/horizon_XX) pairs; a root that is itself one tree counts as h=None."""
    found = []
    for directory in sorted(results_root.glob("horizon_*")):
        try:
            found.append((int(directory.name.split("_")[1]), directory))
        except (IndexError, ValueError):
            continue
    if not found and any(results_root.glob("*/*/predictions.csv")):
        found.append((None, results_root))
    return found


def load_predictions(root: Path, variant: str) -> dict[str, pd.DataFrame]:
    """model -> predictions frame, for every <model>/<variant>/predictions.csv under root."""
    out = {}
    for path in sorted(root.glob(f"*/{variant}/predictions.csv")):
        model = path.parents[1].name
        if model.startswith("_"):
            continue
        frame = pd.read_csv(path, parse_dates=["target_date"])
        out[model] = frame
    return out


def compare_pair(reference: pd.DataFrame, other: pd.DataFrame, horizon: int,
                 n_boot: int, seed: int) -> dict:
    pair = scoring.align(reference, other)
    has_bands = {"lower_a", "upper_a", "lower_b", "upper_b"}.issubset(pair.columns)
    row: dict = {"n_weeks": int(pair["target_date"].nunique()), "n_cells": len(pair)}
    has_quantiles = scoring.has_quantiles(pair)
    for metric in METRICS:
        if (metric == "WIS95" and not has_bands) or (metric == "WIS" and not has_quantiles):
            continue
        result = scoring.block_bootstrap_difference(pair, metric, n_boot=n_boot, seed=seed)
        function = scoring.METRIC_FUNCTIONS[metric]
        row[f"{metric}_ref"] = function(pair, "a")
        row[f"{metric}_other"] = function(pair, "b")
        row[f"d{metric}"] = result.estimate
        row[f"d{metric}_lo"] = result.low
        row[f"d{metric}_hi"] = result.high
        row["block"] = result.block
    for loss, label in (("abs", "MAE"), ("wisq", "WIS"), ("wis", "WIS95")):
        if (loss == "wis" and not has_bands) or (loss == "wisq" and not has_quantiles):
            continue
        test = scoring.diebold_mariano(scoring.weekly_loss(pair, "a", loss),
                                       scoring.weekly_loss(pair, "b", loss), horizon)
        row[f"DM_{label}_stat"] = test.statistic
        row[f"DM_{label}_p"] = test.p_value
    return row


def relative_wis(frames: dict[str, pd.DataFrame], baseline: str = "persistence"
                 ) -> tuple[dict[str, float], str]:
    """Mean WIS of each model / mean WIS of the baseline, on shared cells.

    Uses the 23-quantile WIS when every model carries quantiles, else WIS-95 for
    all of them -- never a mix, since the two are on different scales.
    """
    if baseline not in frames:
        return {}, ""
    banded = {m: f for m, f in frames.items() if {"lower", "upper"}.issubset(f.columns)}
    full = all(set(scoring.QUANTILE_COLUMNS).issubset(f.columns) for f in banded.values())
    function, label = ((scoring.pooled_wis_quantiles, "WIS") if full
                       else (scoring.pooled_wis, "WIS-95"))
    out = {}
    for model, frame in banded.items():
        pair = scoring.align(frame, frames[baseline])
        out[model] = function(pair, "a") / function(pair, "b")
    return out, label


def _fmt(value: float, digits: int = 2) -> str:
    return "–" if value is None or not np.isfinite(value) else f"{value:.{digits}f}"


def _ci(row: pd.Series, metric: str, digits: int = 2) -> str:
    return (f"{_fmt(row[f'd{metric}'], digits)} "
            f"[{_fmt(row[f'd{metric}_lo'], digits)}, {_fmt(row[f'd{metric}_hi'], digits)}]")


def _verdict(row: pd.Series) -> str:
    """Plain-language call on the MAE gap: whose side the whole interval sits on."""
    low, high = row["dMAE_lo"], row["dMAE_hi"]
    if high < 0:
        return "reference better"
    if low > 0:
        return "other better"
    return "not distinguishable"


def markdown(table: pd.DataFrame, horizon, reference: str, variant: str,
             rel: dict[str, float], rel_label: str) -> str:
    lines = [
        f"# Is `{reference}`'s lead bigger than chance? — horizon {horizon}, `{variant}`",
        "",
        "Each row asks: on the weeks of this test season, is the reference model's error",
        "really lower than this model's, or could the gap come from which weeks the season",
        "happened to contain? Differences are **reference minus other**, so for MAE, RMSE",
        "and WIS a negative number means the reference is better; for Corr, positive does.",
        "The bracket is a 95% confidence interval from resampling whole weeks in blocks of",
        f"{int(table['block'].iloc[0]) if 'block' in table and len(table) else '?'} "
        "(all neighborhoods kept together inside a week). A gap whose interval crosses 0",
        "is not distinguishable from chance on this season.",
        "",
        "`p (MAE)` and `p (WIS)` are Diebold-Mariano tests on the weekly loss, Holm-adjusted",
        "across the rows of this table. WIS scores the whole forecast distribution -- point",
        "and spread together -- in rate per 100,000, lower is better. It is FluSight's",
        "weighted interval score over 23 quantiles where both runs wrote them, else the",
        "one-band version from the 95% interval (WIS-95); the column says which.",
        "",
    ]
    wis_key = "WIS" if "dWIS" in table and table["dWIS"].notna().any() else "WIS95"
    wis_name = "WIS" if wis_key == "WIS" else "WIS-95"
    lines += [
        f"| other model | weeks | ΔMAE [95% CI] | ΔRMSE [95% CI] | Δ{wis_name} [95% CI] "
        f"| ΔCorr [95% CI] | p (MAE) | p ({wis_name}) | verdict on MAE |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for _, row in table.iterrows():
        wis = _ci(row, wis_key) if pd.notna(row.get(f"d{wis_key}")) else "–"
        lines.append(
            f"| {row['model']} | {row['n_weeks']} | {_ci(row, 'MAE')} | {_ci(row, 'RMSE')} "
            f"| {wis} | {_ci(row, 'Corr', 3)} | {_fmt(row.get('DM_MAE_p_holm'), 3)} "
            f"| {_fmt(row.get(f'DM_{wis_key}_p_holm'), 3)} | {_verdict(row)} |"
        )
    if rel:
        lines += [
            "",
            "## Skill against persistence",
            "",
            f"Does the model beat \"next week looks like this week\"? Relative {rel_label} is the",
            f"model's mean {rel_label} divided by persistence's on the same cells: below 1 is",
            "better than persistence, and 0.8 means 20% less forecast error.",
            "",
            f"| model | relative {rel_label} |",
            "| --- | --- |",
        ]
        for model, value in sorted(rel.items(), key=lambda kv: kv[1]):
            lines.append(f"| {model} | {_fmt(value, 3)} |")
    lines += [
        "",
        "One season is one season: an interval that excludes 0 here says the gap held across",
        "this season's weeks, not that it will hold next season. The backtest folds are what",
        "test that.",
        "",
    ]
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None,
                        help="A city root (with horizon_XX/ below it) or one horizon tree.")
    parser.add_argument("--reference", default="gnn_st")
    parser.add_argument("--variant", default="post_covid")
    parser.add_argument("--models", default=None, help="Comma-separated subset to compare against.")
    parser.add_argument("--include-variants", action="store_true",
                        help="Also compare against the reference's own ablation arms "
                             "(gnn_*); they then join the Holm family.")
    parser.add_argument("--tag", default="",
                        help="Suffix for the output files (significance_<tag>.md), so a "
                             "second comparison set does not overwrite the first.")
    parser.add_argument("--n-boot", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def is_family_member(model: str, reference: str, include_variants: bool) -> bool:
    """Which models enter the Holm family by default: the baselines, not the reference's own arms.

    Ablation arms of the reference (gnn_st_*, gnn_cascade) answer a different
    question -- what a design choice buys -- and folding them into the same
    family would spend the multiplicity correction on comparisons nobody reads
    as "does the GNN beat the baselines".
    """
    # The one ablation arm that IS a headline comparison: the same pipeline with
    # the graph removed, which answers the repository's actual question.
    return (include_variants or not model.startswith("gnn_")
            or model.startswith("gnn_st_nograph"))


def main() -> None:
    args = parse_args()
    results_root = city_results_dir(args, get_city(args.city)).resolve()
    roots = horizon_roots(results_root)
    if not roots:
        raise SystemExit(f"error: no predictions.csv under {results_root}")
    wanted = None if args.models is None else {m.strip() for m in args.models.split(",")}

    # Plan every comparison first so the Budget line has its denominator.
    plan = []
    for horizon, root in roots:
        frames = load_predictions(root, args.variant)
        if args.reference not in frames:
            print(f"warning: no {args.reference}/{args.variant} under {root}; skipped",
                  file=sys.stderr)
            continue
        h = horizon or int(frames[args.reference]["horizon"].iloc[0])
        others = [m for m in frames if m != args.reference
                  and (m in wanted if wanted else
                       is_family_member(m, args.reference, args.include_variants))]
        if others:
            plan.append((h, root, frames, others))
    if not plan:
        raise SystemExit("error: nothing compared; check --reference and --variant")

    # The run_progress.py contract, expressed in comparisons.
    total = sum(len(others) for *_, others in plan)
    print(f"Budget: {total} epochs x 1 seeds", flush=True)
    print("--- seed 0 (1/1) ---", flush=True)
    done = 0
    written = []
    for h, root, frames, others in plan:
        rows = []
        for model in others:
            rows.append({"model": model, "horizon": h,
                         **compare_pair(frames[args.reference], frames[model], h,
                                        args.n_boot, args.seed)})
            done += 1
            print(f"Epoch {done} | h={h} vs {model}", flush=True)
        table = pd.DataFrame(rows).sort_values("MAE_other").reset_index(drop=True)
        for label in ("MAE", "WIS", "WIS95"):
            column = f"DM_{label}_p"
            if column in table:
                table[f"{column}_holm"] = scoring.holm(table[column])
        rel, rel_label = relative_wis(frames)

        out = paths.comparison_dir(root)
        out.mkdir(parents=True, exist_ok=True)
        table.insert(0, "reference", args.reference)
        stem = f"significance_{args.tag}" if args.tag else "significance"
        table.to_csv(out / f"{stem}.csv", index=False)
        (out / f"{stem}.md").write_text(markdown(table, h, args.reference, args.variant, rel, rel_label))
        written.append(out / f"{stem}.md")
        print(f"h={h}: {paths.display(out / f'{stem}.md')}")
        for _, row in table.iterrows():
            print(f"  vs {row['model']:<16} ΔMAE {_ci(row, 'MAE')}  "
                  f"p(MAE)={_fmt(row.get('DM_MAE_p_holm'), 3)}  {_verdict(row)}")

    print(f"Outputs: {', '.join(paths.display(p) for p in written)}", flush=True)


if __name__ == "__main__":
    main()
