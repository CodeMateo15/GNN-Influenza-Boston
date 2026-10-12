#!/usr/bin/env python3
"""Severity-alert skill on the unseen seasons: tables, intervals, and Figure S5.

Reads the per-cell bands written by Code/compare_severity.py for each unseen
fold (Code/results/_severity_backtest/<city>/<season>/horizon_0H/), which were
produced with thresholds fitted only on seasons before each fold:

    Boston 2022-23: 2017-18, 2018-19            (cutoff 2022-06-01)
    Boston 2023-24: + 2022-23                   (cutoff 2023-06-01)
    Boston 2024-25: + 2023-24                   (cutoff 2024-06-01)
    Columbus 2024-25: 2022-23, 2023-24          (cutoff 2024-06-01)

Chicago is not scored: its target is already the health department's graded
1-10 activity level, not a rate to be banded.

    /opt/anaconda3/bin/python Paper/scripts/make_severity.py

Two readings of each forecast are scored, pooled over neighborhood-weeks:
- probability: Brier skill score of the forecast's probability of being at or
  above the threshold, against always forecasting the pooled share of such
  weeks (BSS, higher is better, 0 = no better than that constant);
- yes/no: Peirce skill score of "the best-guess forecast is at or above the
  threshold" (hit rate minus false-alarm rate; 0 = no skill).
Differences against the graph model get 95% intervals from a moving-block
bootstrap over weeks (blocks of 4, within each season, 2,000 resamples).
"""

from __future__ import annotations

import glob
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SEV = ROOT / "Code" / "results" / "_severity_backtest"
FIG = ROOT / "Paper" / "overleaf" / "figures"
B, BLOCK, SEED = 2000, 4, 0
LEVELS = {"IT50": (1, "p_exceed_50", "Moderate or higher"), "IT90": (2, "p_exceed_90", "High or higher")}
MODELS = [("gnn_st_tuned", "Graph neural network", "#0072B2", "o"),
          ("gnn_st_nograph_tuned", "Same model, map removed", "#56B4E9", "s"),
          ("lstm_tuned", "LSTM", "#E69F00", "^"),
          ("colagnn_tuned", "Cola-GNN", "#009E73", "D"),
          ("flusight_baseline", "FluSight baseline", "#999999", "P"),
          ("persistence", "Persistence", "#000000", "X")]
COLS = ["bs", "ev", "hit", "fa", "miss", "cn", "n"]
CITIES = ["boston", "columbus"]


def weekly(city: str, h: int) -> dict[str, pd.DataFrame]:
    files = sorted(glob.glob(str(SEV / city / "*" / f"horizon_0{h}" / "severity_bands.csv")))
    d = pd.concat([pd.read_csv(f).assign(fold=Path(f).parts[-3]) for f in files])
    d = d[d.indicator != "CITYWIDE"].dropna(subset=["actual"])
    out = {}
    for lab, (k, pcol, _) in LEVELS.items():
        ev = (d.true_band >= k).astype(float)
        alert = (d.pred_band >= k).astype(float)
        x = d.assign(ev=ev, bs=(d[pcol] - ev) ** 2, hit=alert * ev, fa=alert * (1 - ev),
                     miss=(1 - alert) * ev, cn=(1 - alert) * (1 - ev), n=1.0)
        out[lab] = x.groupby(["model", "fold", "target_date"])[COLS].sum()
    return out


def skill(a: np.ndarray) -> tuple[float, float, float, float]:
    bs, ev, hit, fa, miss, cn, n = a.sum(axis=0)
    rate = ev / n
    ref = n * rate * (1 - rate)
    bss = 1 - bs / ref if ref > 0 else np.nan
    pod = hit / (hit + miss) if hit + miss else np.nan
    pofd = fa / (fa + cn) if fa + cn else np.nan
    far = fa / (hit + fa) if hit + fa else np.nan
    return bss, pod - pofd, pod, far


def main() -> None:
    rng = np.random.default_rng(SEED)
    level_rows, diff_rows = [], []
    for city in CITIES:
        for h in (1, 2, 4):
            for lab, w in weekly(city, h).items():
                weeks = w.loc["gnn_st_tuned"].index
                folds = weeks.get_level_values(0)
                blocks = {f: np.where(folds == f)[0] for f in folds.unique()}

                def draw():
                    pick = []
                    for ix in blocks.values():
                        n = len(ix)
                        starts = rng.integers(0, n - BLOCK + 1, size=int(np.ceil(n / BLOCK)))
                        pick.extend(np.concatenate([ix[s:s + BLOCK] for s in starts])[:n])
                    return np.array(pick)

                arrays = {m: w.loc[m].reindex(weeks)[COLS].to_numpy() for m, *_ in MODELS}
                for m, *_ in MODELS:
                    bss, pss, pod, far = skill(arrays[m])
                    level_rows.append(dict(city=city, horizon=h, level=lab, model=m,
                                           events=int(arrays[m][:, 1].sum()), n=int(arrays[m][:, 6].sum()),
                                           BSS=bss, PSS=pss, POD=pod, FAR=far))
                boots = [draw() for _ in range(B)]
                g = arrays["gnn_st_tuned"]
                for m, *_ in MODELS[1:]:
                    o = arrays[m]
                    db = [skill(g[ix])[0] - skill(o[ix])[0] for ix in boots]
                    dp = [skill(g[ix])[1] - skill(o[ix])[1] for ix in boots]
                    diff_rows.append(dict(city=city, horizon=h, level=lab, other=m,
                                          dBSS=skill(g)[0] - skill(o)[0],
                                          dBSS_lo=np.nanpercentile(db, 2.5), dBSS_hi=np.nanpercentile(db, 97.5),
                                          dPSS=skill(g)[1] - skill(o)[1],
                                          dPSS_lo=np.nanpercentile(dp, 2.5), dPSS_hi=np.nanpercentile(dp, 97.5)))
    lv = pd.DataFrame(level_rows)
    df = pd.DataFrame(diff_rows)
    lv.to_csv(SEV / "skill_by_model.csv", index=False)
    df.to_csv(SEV / "skill_differences.csv", index=False)

    # Onset timing: weeks late in first crossing the moderate threshold.
    t = pd.concat([pd.read_csv(f).assign(city=Path(f).parts[-4])
                   for f in glob.glob(str(SEV / "*" / "*" / "horizon_0*" / "severity_timing.csv"))])
    t = t[(t.label == "IT50") & (t.indicator != "CITYWIDE")]
    onset = t.groupby(["city", "horizon", "model"]).onset_error_weeks.agg(["median", "count"]).reset_index()
    onset.to_csv(SEV / "onset_by_model.csv", index=False)

    figure_s5(lv)
    latex(lv, df, onset)


def figure_s5(lv: pd.DataFrame) -> None:
    plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                         "pdf.fonttype": 42, "savefig.dpi": 300})
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.0), sharex=True)
    panels = [("BSS", "IT50"), ("BSS", "IT90"), ("PSS", "IT50"), ("PSS", "IT90")]
    ylab = {"BSS": "Brier skill score\n(probability of crossing)", "PSS": "Peirce skill score\n(yes/no from best guess)"}
    offs = np.linspace(-0.25, 0.25, len(MODELS))
    for ax, (metric, lab), letter in zip(axes.flat, panels, "ABCD"):
        ax.axhline(0, color="grey", lw=0.7, ls=":")
        for (m, name, col, mk), off in zip(MODELS, offs):
            s = lv[(lv.city == "boston") & (lv.level == lab) & (lv.model == m)].sort_values("horizon")
            ax.plot(np.arange(3) + off, s[metric], marker=mk, ls="none", color=col, ms=4.5, label=name)
        ax.set_xticks(range(3), ["1", "2", "4"])
        ax.set_title(f"{LEVELS[lab][2]} weeks", fontsize=8)
        ax.set_ylabel(ylab[metric])
        ax.text(-0.18, 1.06, f"{letter})", transform=ax.transAxes, fontsize=9, fontweight="bold")
    for ax in axes[1]:
        ax.set_xlabel("Weeks ahead")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.06))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"figureS5_severity_skill.{ext}", bbox_inches="tight")
    plt.close(fig)
    print("wrote figureS5_severity_skill")


def latex(lv: pd.DataFrame, df: pd.DataFrame, onset: pd.DataFrame) -> None:
    f = lambda v: "" if pd.isna(v) else f"{v:.2f}".replace("-", "$-$")
    print("\n% Table S12 rows (Boston): model & BSS mod h1 h2 h4 & BSS high & PSS mod & PSS high")
    for city in CITIES:
        print(f"% --- {city}")
        for m, name, *_ in MODELS:
            cells = []
            for metric in ("BSS", "PSS"):
                for lab in ("IT50", "IT90"):
                    s = lv[(lv.city == city) & (lv.model == m) & (lv.level == lab)].set_index("horizon")[metric]
                    cells += [f(s.get(h)) for h in (1, 2, 4)]
            print(f"{name} & " + " & ".join(cells) + r" \\")
        ev = lv[(lv.city == city) & (lv.model == "gnn_st_tuned") & (lv.horizon == 1)]
        print(f"% events: {dict(zip(ev.level, ev.events))}, cells: {int(ev.n.iloc[0])}")
    print("\n% Differences, graph model minus other, [95% CI]")
    for _, r in df.iterrows():
        print(f"% {r.city} h{r.horizon} {r.level} vs {r.other}: dBSS {r.dBSS:.3f} [{r.dBSS_lo:.3f}, {r.dBSS_hi:.3f}]  "
              f"dPSS {r.dPSS:.3f} [{r.dPSS_lo:.3f}, {r.dPSS_hi:.3f}]")
    print("\n% Onset error (weeks late, median) for moderate threshold")
    print(onset.pivot_table(index=["city", "model"], columns="horizon", values="median").to_string())


if __name__ == "__main__":
    main()
