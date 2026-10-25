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
    "gnn_st_noweather_tuned": "No environment",
    "gnn_st_nodemofeat_tuned": "No demographics",
    "gnn_st_historyonly_tuned": "None of the three (past rates only)",
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


# Table 3. What each component adds: relative WIS by city and horizon for the
# full model, each version with one component removed, the version with none,
# and the 2 history-only models it should resemble.
COMPONENTS = ["gnn_st_tuned", "gnn_st_noweather_tuned", "gnn_st_nodemofeat_tuned",
              "gnn_st_nograph_tuned", "gnn_st_historyonly_tuned", "blend_baseline", "sarima"]
COMPONENT_LABEL = {"gnn_st_tuned": "Full model", "gnn_st_noweather_tuned": "No environment",
                   "gnn_st_nodemofeat_tuned": "No demographics",
                   "gnn_st_nograph_tuned": "No map",
                   "gnn_st_historyonly_tuned": "None of the three",
                   "blend_baseline": "Seasonal blend", "sarima": "Seasonal ARIMA"}


def _clear_counts(city: str, tag: str, arm: str, h: int) -> tuple[int, int]:
    """Seasons in which the comparison is clear: (arm worse than gnn_st_tuned, arm better)."""
    base = RESULTS if city == "boston" else RESULTS / city
    worse = better = 0
    for s in UNSEEN[city]:
        t = pd.read_csv(base / f"backtest_{s}" / f"horizon_{h:02d}" / "_comparison"
                        / f"significance_{tag}.csv").set_index("model")
        if arm in t.index and t.loc[arm, "DM_WIS_p_holm"] < 0.05:
            worse += t.loc[arm, "dWIS"] < 0
            better += t.loc[arm, "dWIS"] > 0
    return worse, better


def component_table() -> None:
    """Table 3: % more mean WIS than the full model, and seasons with a clear difference.

    Mean WIS is the mean of season means, as in Table 2. The component rows use
    the components family (significance_components.csv); the 2 history-only
    rows use the comparison-model family (significance_tuned.csv).
    """
    print("% Table 3: % change in mean WIS vs full model (seasons clearly worse; ^b if any clearly better),"
          " Boston h1 h2 h4 & Columbus h1 h2 h4 & Chicago h1 h2 h4")
    wis = {c: load(c).groupby(["arm", "horizon"]).WIS.mean().unstack() for c in UNSEEN}
    for a in COMPONENTS[1:]:
        tag = "tuned" if a in ("blend_baseline", "sarima") else "components"
        cells = []
        for c in UNSEEN:
            for h in (1, 2, 4):
                pct = 100 * (wis[c].loc[a, h] - wis[c].loc["gnn_st_tuned", h]) / wis[c].loc["gnn_st_tuned", h]
                worse, better = _clear_counts(c, tag, a, h)
                mark = "$^{b}$" if better else ""
                cells.append(f"{pct:.1f} ({worse}){mark}".replace("-", "$-$", 1))
        print(f"{COMPONENT_LABEL[a]} & " + " & ".join(cells) + r" \\")
    print("% relative WIS of the full model, for the footnote:")
    print(" & ".join(f"{wis[c].loc['gnn_st_tuned', h] / wis[c].loc['persistence', h]:.2f}"
                     for c in UNSEEN for h in (1, 2, 4)))
    print()


def _signed(x: float) -> str:
    return f"$-${abs(x):.1f}" if round(x, 1) < 0 else f"{abs(x) if round(x, 1) == 0 else x:.1f}"


def component_significance(tag: str, models) -> None:
    """Supplement: one row per city, season, horizon and model, from significance_<tag>.csv."""
    print(f"% significance_{tag}: % more mean WIS than the reference (95% CI), Holm p")
    for c in UNSEEN:
        base = RESULTS if c == "boston" else RESULTS / c
        for s in UNSEEN[c]:
            for h in (1, 2, 4):
                t = pd.read_csv(base / f"backtest_{s}" / f"horizon_{h:02d}" / "_comparison"
                                / f"significance_{tag}.csv").set_index("model")
                for a in models:
                    if a not in t.index:
                        continue
                    r = t.loc[a]
                    label = f"{c.capitalize()} {s[:4]}--20{s[5:]}"
                    # % more WIS than the reference (positive: the other model is worse),
                    # with the block-bootstrap interval carried over to the same scale.
                    pct = 100 / r.WIS_ref
                    est, lo, hi = -r.dWIS * pct, -r.dWIS_hi * pct, -r.dWIS_lo * pct
                    print(f"{label} & {h} & {COMPONENT_LABEL.get(a, LABEL.get(a, a))} & "
                          f"{_signed(est)} ({_signed(lo)}, {_signed(hi)}) & "
                          f"{ama_p(r.DM_WIS_p_holm)} \\\\")
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


# Table S15: the same no-learned-links model trained on several cities at once
# (run_gnn.py --pool-cities). "All 3" includes the target's own pre-test weeks;
# "other 2" leaves the target out. A cell is marked when its week-level
# difference from the locally trained model is clear (significance_transfer_pooled).
POOLED = ["transfer_zeroshot_from_pooled_all3", "transfer_finetune_from_pooled_all3",
          "transfer_zeroshot_from_pooled_others", "transfer_finetune_from_pooled_others"]
SIG_ROOT = {"boston": RESULTS, "columbus": RESULTS / "columbus",
            "chicago": RESULTS / "chicago"}


def pooled_table() -> None:
    print(f"% Table S15: target & h & local & all3 & all3 fine-tuned & other2 & "
          f"other2 fine-tuned & persistence, {TRANSFER_SEASON}; ^{{a}} = clear vs local")
    for target in ("boston", "columbus", "chicago"):
        d = pd.read_csv(CSV[target])
        d = d[d.season.eq(TRANSFER_SEASON)].set_index(["arm", "horizon"]).WIS
        for i, h in enumerate((1, 2, 4)):
            sig = pd.read_csv(SIG_ROOT[target] / f"backtest_{TRANSFER_SEASON}" / f"horizon_{h:02d}"
                              / "_comparison" / "significance_transfer_pooled.csv")
            clear = set(sig.loc[sig.DM_WIS_p_holm < 0.05, "model"])
            cells = [fmt(d.get(("gnn_st_noadapt", h)))]
            cells += [fmt(d.get((a, h))) + (r"$^{a}$" if a in clear else "") for a in POOLED]
            cells.append(fmt(d.get(("persistence", h))))
            print(f"{target.title() if i == 0 else ''} & {h} & " + " & ".join(cells) + r" \\")
    print()


# Table S16: the development-season ablation study (Code/results/_ablation,
# study "main", 10 seeds, Boston 2025-26). Each arm is gnn_st with one change.
# Cells are the change in mean per-neighborhood correlation (arm minus default)
# with the number of the 14 neighborhoods in which the arm's correlation was
# higher, as in run_ablation.py's paired_verdict. Transit comes from the
# archived transit_retirement study, which has no per-neighborhood files here.
ABLATION = RESULTS / "_ablation"
ABLATION_ROWS = [
    ("Removed", [
        ("gnn_st_nograph", "All links between neighborhoods (map and learned)"),
        ("gnn_st_adaptiveonly", "Hand-built links, keeping learned links"),
        ("gnn_st_noadapt", "Learned links, keeping hand-built links"),
        ("gnn_st_geoonly", "Correlation and demographic links (borders only)"),
        ("gnn_st_nocorr", "Correlation links"),
        ("gnn_st_nodemoedge", "Demographic links"),
        ("gnn_st_nodemofeat", "Demographic measures as inputs"),
        ("gnn_st_nodemo", "Demographic measures and links"),
        ("gnn_st_noweather", "Weather"),
        ("gnn_st_noimputedflag", "Flag for suppressed weeks"),
        ("gnn_st_lagsonly", "All inputs except past rates"),
        ("gnn_st_nopearson", "Correlation term in the training loss"),
    ]),
    ("Changed", [
        ("gnn_st_delta", "Baseline: current week only"),
        ("gnn_st_level", "No baseline"),
        ("gnn_st_relations", "Link types kept separate"),
        ("gnn_st_tiny", "Smaller model"),
    ]),
    ("Added", [
        ("gnn_st_wastewater", "Influenza wastewater"),
        ("gnn_st_vaccination", "Statewide vaccination uptake"),
        ("gnn_st_globals", "Citywide ILI share"),
        ("gnn_st_season", "Calendar terms"),
        ("gnn_st_covid_rsv", "COVID-19 and RSV rates, COVID-19 wastewater"),
        ("gnn_st_transit", "Transit ridership links"),
    ]),
]


def _nbhd_corr(arm: str, h: int) -> pd.Series | None:
    path = ABLATION / "main" / f"h{h:02d}_s10" / arm / "post_covid" / "metrics.csv"
    if not path.exists():
        return None
    m = pd.read_csv(path)
    m = m[m.segment.eq("overall") & m.scope.eq("neighborhood")]
    return m.set_index("neighborhood").Corr


def ablation_table() -> None:
    main = pd.read_csv(ABLATION / "ablation_main_s10.csv").set_index(["arm", "horizon"]).Corr_macro
    transit = pd.read_csv(ABLATION / "transit_retirement" / "transit_retirement_s10.csv")
    transit = transit.set_index(["arm", "horizon"]).Corr_macro
    print("% Table S16: change & delta corr (nbhds improved/14) at h1 h2 h4; "
          "development season 2025-26, 10 seeds")
    floor = []
    for h in (1, 2, 4):
        refs = [main[(a, h)] for a in ("gnn_st", "gnn_st_ref_b", "gnn_st_ref_c")]
        floor.append(max(refs) - min(refs))
    print("% default " + " ".join(f"{main[('gnn_st', h)]:.3f}" for h in (1, 2, 4))
          + " | run-to-run spread " + " ".join(f"{f:.3f}" for f in floor))
    for group, rows in ABLATION_ROWS:
        print(rf"\multicolumn{{4}}{{l}}{{\textit{{{group}}}}} \\")
        for arm, label in rows:
            cells = []
            for h in (1, 2, 4):
                src = transit if arm == "gnn_st_transit" else main
                d = src[(arm, h)] - src[("gnn_st", h)]
                cell = ("0.000" if abs(d) < 0.0005 else
                        f"{d:+.3f}".replace("-", "$-$").replace("+", "$+$"))
                arm_c, ref_c = _nbhd_corr(arm, h), _nbhd_corr("gnn_st", h)
                if arm_c is not None and ref_c is not None:
                    shared = arm_c.index.intersection(ref_c.index)
                    cell += f" ({int((arm_c[shared] > ref_c[shared]).sum())})"
                cells.append(cell)
            print(f"\\quad {label} & " + " & ".join(cells) + r" \\")
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
    pooled_table()
    ablation_table()
    component_table()
    component_significance("components", COMPONENTS[1:5])
    component_significance("historyonly", ["blend_baseline", "sarima", "persistence",
                                           "flusight_baseline", "lstm_tuned"])
