#!/usr/bin/env python3
"""LaTeX table bodies for the manuscript and supplement, from Code/results.

    /opt/anaconda3/bin/python Paper/scripts/make_tables.py > tables.txt

Prints tabular rows only; the surrounding table environments live in the
manuscript files so their captions can be edited there.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "Code" / "results"
UNSEEN = {"boston": ["2022_23", "2023_24", "2024_25"],
          "columbus": ["2024_25"],
          "chicago": ["2022_23", "2023_24", "2024_25", "2025_26"]}
CSV = {"boston": RESULTS / "_backtest" / "backtest.csv",
       "columbus": RESULTS / "columbus" / "_backtest" / "backtest.csv",
       "chicago": RESULTS / "chicago" / "_backtest" / "backtest.csv"}
# Every city now runs the same arms under the same tuning, so nothing is
# relabelled. DROP is for a run known to be broken; it is empty. (Chicago's
# gat_parity once diverged in 2022-23; the cause was a zero-std scaling bug,
# fixed in influenza/windows.py: safe_scale.)
DROP: dict[str, set[str]] = {}


def load(city: str) -> pd.DataFrame:
    d = pd.read_csv(CSV[city])
    d = d[d.season.isin(UNSEEN[city]) & ~d.arm.isin(DROP.get(city, set()))]
    return d


LABEL = {
    "gnn_st_tuned": "Graph neural network",
    "gnn_st_nograph_tuned": "Same model, map removed",
    "lstm_tuned": "LSTM",
    "colagnn_tuned": "Cola-GNN",
    "xgboost_tuned": "Gradient-boosted trees",
    "sarima": "Seasonal ARIMA",
    "blend_baseline": "Seasonal blend, no learning",
    "flusight_baseline": "FluSight baseline",
    "persistence": "Persistence",
    "gat_tuned": "Graph attention network$^{a}$",
    "dualtopo_tuned": "Dual-topology GCN$^{a}$",
    "climatology": "Climatology",
    "seasonal_naive": "Same week last year",
}
MAIN = ["gnn_st_tuned", "gnn_st_nograph_tuned", "lstm_tuned", "colagnn_tuned",
        "xgboost_tuned", "sarima", "blend_baseline", "flusight_baseline", "persistence"]
SUPP = MAIN + ["gat_tuned", "dualtopo_tuned", "climatology", "seasonal_naive"]


def fmt(x, nd=2):
    return "" if pd.isna(x) else f"{x:.{nd}f}"


def ama_p(v: float) -> str:
    """AMA style: 2 digits, 3 below .01, bounded at <.001 and >.99."""
    if v < 0.001:
        return "$<$.001"
    if v > 0.99:
        return "$>$.99"
    return (f"{v:.3f}" if v < 0.01 else f"{v:.2f}").lstrip("0")


def main_table(city: str, arms) -> None:
    d = load(city)
    wis = d.groupby(["arm", "horizon"]).WIS.mean().unstack()
    mae = d.groupby(["arm", "horizon"]).MAE.mean().unstack()
    rel = wis.div(wis.loc["persistence"], axis=1)
    print(f"% {city}: WIS h1 h2 h4 & relative WIS h1 h2 h4 & MAE h1 h2 h4")
    for a in arms:
        if a not in wis.index:
            continue
        cells = [fmt(wis.loc[a, h]) for h in (1, 2, 4)]
        cells += [fmt(rel.loc[a, h]) for h in (1, 2, 4)]
        cells += [fmt(mae.loc[a, h]) for h in (1, 2, 4)]
        print(f"{LABEL[a]} & " + " & ".join(cells) + r" \\")
    print()


def per_season(city: str) -> None:
    d = load(city)
    print(f"% {city}: per season WIS, columns season x horizon")
    for a in SUPP:
        sub = d[d.arm == a].set_index(["season", "horizon"]).WIS
        cells = [fmt(sub.get((s, h))) for s in UNSEEN[city] for h in (1, 2, 4)]
        if all(c == "" for c in cells):
            continue
        print(f"{LABEL[a]} & " + " & ".join(cells) + r" \\")
    print()


def significance(city: str) -> None:
    base = RESULTS if city == "boston" else RESULTS / city
    print(f"% {city}: graph model minus other, WIS [95% CI], Holm p")
    for s in UNSEEN[city]:
        for h in (1, 2, 4):
            t = pd.read_csv(base / f"backtest_{s}" / f"horizon_{h:02d}" / "_comparison"
                            / "significance_tuned.csv").set_index("model")
            for a in MAIN[1:]:
                if a not in t.index:
                    continue
                r = t.loc[a]
                label = f"{s[:4]}--20{s[5:]}"
                print(f"{label} & {h} & {LABEL[a]} & {r.dWIS:.2f} "
                      f"({r.dWIS_lo:.2f}, {r.dWIS_hi:.2f}) & {ama_p(r.DM_WIS_p_holm)} \\\\")
    print()


def point_metrics(city: str) -> None:
    d = load(city)
    print(f"% {city}: MAE h1 h2 h4 & RMSE h1 h2 h4 & Corr h1 h2 h4")
    t = {m: d.groupby(["arm", "horizon"])[m].mean().unstack() for m in ("MAE", "RMSE", "Corr")}
    for a in MAIN:
        if a not in t["MAE"].index:
            continue
        cells = [fmt(t[m].loc[a, h], 2) for m in ("MAE", "RMSE") for h in (1, 2, 4)]
        cells += [fmt(t["Corr"].loc[a, h], 2) for h in (1, 2, 4)]
        print(f"{LABEL[a]} & " + " & ".join(cells) + r" \\")
    print()


# Table 4. Each row is a (target, source) pair scored on the target's own
# 2024-25 fold, in the target's own units: the model trained on the target
# alone, the source model applied with no local training, the source model
# fine-tuned on the target, and persistence. "Trained locally" is
# gnn_st_noadapt at fixed settings -- the same architecture the transfer arms
# use -- not the tuned graph model of Table 2.
TRANSFER_SEASON = "2024_25"
TRANSFER_PAIRS = [("columbus", "boston"), ("chicago", "boston"),
                  ("boston", "columbus"), ("boston", "chicago")]


def transfer_table() -> None:
    print(f"% Table 4: target (source) & h & local & zero-shot & fine-tuned & persistence, "
          f"{TRANSFER_SEASON}")
    for target, source in TRANSFER_PAIRS:
        d = pd.read_csv(CSV[target])
        d = d[d.season.eq(TRANSFER_SEASON)].set_index(["arm", "horizon"]).WIS
        arms = ["gnn_st_noadapt", f"transfer_zeroshot_from_{source}",
                f"transfer_finetune_from_{source}", "persistence"]
        for i, h in enumerate((1, 2, 4)):
            head = f"{target.title()} (from {source.title()})" if i == 0 else ""
            print(f"{head} & {h} & " + " & ".join(fmt(d.get((a, h))) for a in arms) + r" \\")
    print()


if __name__ == "__main__":
    for c in UNSEEN:
        main_table(c, MAIN)
    for c in UNSEEN:
        per_season(c)
    for c in UNSEEN:
        significance(c)
    for c in UNSEEN:
        point_metrics(c)
    transfer_table()
