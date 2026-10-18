#!/usr/bin/env python3
"""Publication figures for the AJE manuscript, from results already on disk.

Everything here reads files under Code/results and Data/; nothing is trained.
Run from anywhere:

    /opt/anaconda3/bin/python Paper/scripts/make_figures.py

Writes PDF and PNG copies of each figure to Paper/overleaf/figures/.
Only the unseen seasons are plotted as evidence; the development season
appears only in the Figure 1 timeline, labeled as such.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "Code" / "results"
NEIGH_DIR = ROOT / "Data" / "Neighborhood Data"
OUT = ROOT / "Paper" / "overleaf" / "figures"
sys.path.insert(0, str(ROOT / "Code"))

from influenza.cities.boston import (ANCHOR_SHORT, GEO_EDGES_ANCHOR,  # noqa: E402
                                     GEOID_TO_IDX, NEIGHBORHOODS, SHORT_NAMES)

UNSEEN = {"boston": ["2022_23", "2023_24", "2024_25"],
          "columbus": ["2024_25"],
          "chicago": ["2022_23", "2023_24", "2024_25", "2025_26"]}  # no Chicago season chose anything
CITY_LABEL = {"boston": "Boston", "columbus": "Columbus", "chicago": "Chicago"}
BACKTEST_CSV = {"boston": RESULTS / "_backtest" / "backtest.csv",
                "columbus": RESULTS / "columbus" / "_backtest" / "backtest.csv",
                "chicago": RESULTS / "chicago" / "_backtest" / "backtest.csv"}
HORIZONS = (1, 2, 4)

# Okabe-Ito, colorblind safe.
C = {"graph": "#0072B2", "nograph": "#56B4E9", "lstm": "#E69F00", "cola": "#009E73",
     "flusight": "#999999", "blend": "#CC79A7", "persist": "#000000", "red": "#D55E00"}
MODELS = [  # arm, label, color, marker
    ("gnn_st_tuned", "Graph neural network", C["graph"], "o"),
    ("gnn_st_nograph_tuned", "Same model, no map", C["nograph"], "s"),
    ("lstm_tuned", "LSTM", C["lstm"], "^"),
    ("colagnn_tuned", "Cola-GNN", C["cola"], "D"),
    ("blend_baseline", "Seasonal blend (no learning)", C["blend"], "v"),
    ("flusight_baseline", "FluSight baseline", C["flusight"], "P"),
]

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 8, "axes.titlesize": 8,
    "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5, "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "savefig.dpi": 300,
})


def season_text(city: str, season: str) -> str:
    return f"{season[:4]}\u2013{season[5:]}"


def locant(ax, letter: str, x: float = -0.12, y: float = 1.04) -> None:
    ax.text(x, y, f"{letter})", transform=ax.transAxes, fontsize=9, fontweight="bold",
            va="bottom", ha="left")


def km_per_degree_lon(lat: float) -> float:
    """Kilometers per degree of longitude on the WGS84 ellipsoid."""
    a, e2 = 6378.137, 0.00669438
    phi = np.deg2rad(lat)
    return np.pi / 180 * a * np.cos(phi) / np.sqrt(1 - e2 * np.sin(phi) ** 2)


def scale_bar(ax, km: float, x: float, y: float, fontsize: float = 6.5) -> None:
    """Scale bar of `km` kilometers, left end at axes fraction (x, y), on a lon/lat map."""
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    lon, lat = x0 + x * (x1 - x0), y0 + y * (y1 - y0)
    width = km / km_per_degree_lon(lat)
    tick = 0.012 * (y1 - y0)
    ax.plot([lon, lon + width], [lat, lat], color="black", lw=1.2, solid_capstyle="butt", zorder=5)
    for xx in (lon, lon + width / 2, lon + width):
        ax.plot([xx, xx], [lat, lat + tick], color="black", lw=0.8, zorder=5)
    for xx, lab in ((lon, "0"), (lon + width, f"{km:g} km")):
        ax.text(xx, lat - tick, lab, ha="center", va="top", fontsize=fontsize)


def north_arrow(ax, x: float, y: float, length: float = 0.09, fontsize: float = 7) -> None:
    """Arrow pointing north (up: these maps are unrotated lon/lat), tip at axes fraction (x, y)."""
    ax.annotate("", xy=(x, y), xytext=(x, y - length), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0, mutation_scale=8))
    ax.text(x, y + 0.01, "N", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=fontsize, fontweight="bold")


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {name}.pdf/.png")


def predictions(city: str, season: str, horizon: int, arm: str) -> pd.DataFrame:
    base = RESULTS if city == "boston" else RESULTS / city
    run = base / f"backtest_{season}" / f"horizon_{horizon:02d}" / arm
    (path,) = list(run.glob("*/predictions.csv"))
    return pd.read_csv(path, parse_dates=["origin_date", "target_date"])


# --------------------------------------------------------------------------- #
# Figure 1: study design                                                       #
# --------------------------------------------------------------------------- #
def rings(geometry: dict):
    polys = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    for poly in polys:
        yield np.asarray(poly[0])


def boston_mean_rates() -> pd.Series:
    frames = [predictions("boston", s, 1, "persistence") for s in UNSEEN["boston"]]
    d = pd.concat(frames).drop_duplicates(["target_date", "neighborhood"])
    return d.groupby("neighborhood")["actual"].mean()


def figure1() -> None:
    fig = plt.figure(figsize=(7.0, 3.5))
    ax_map = fig.add_axes([0.0, 0.0, 0.45, 0.95])
    ax_t = fig.add_axes([0.56, 0.12, 0.43, 0.78])

    geo = json.loads((NEIGH_DIR / "boston_polygons_tract_neighborhoods.geojson").read_text())
    rates = boston_mean_rates()
    cmap = plt.get_cmap("Blues")
    vmin, vmax = 0, float(np.ceil(rates.max() / 10) * 10)
    centroids: dict[int, list] = {}
    polys, colors = [], []
    for feat in geo["features"]:
        name = feat["properties"]["neighborhood"]
        idx = GEOID_TO_IDX.get(name)
        if idx is None:
            continue
        rate = rates.get(NEIGHBORHOODS[idx], np.nan)
        for ring in rings(feat["geometry"]):
            polys.append(ring)
            colors.append(cmap(0.15 + 0.8 * (rate - vmin) / (vmax - vmin)))
            centroids.setdefault(idx, []).append((ring.mean(axis=0), len(ring)))
    ax_map.add_collection(PolyCollection(polys, facecolors=colors, edgecolors="white",
                                         linewidths=0.4))
    center = {}
    for idx, parts in centroids.items():
        w = np.array([n for _, n in parts], float)
        pts = np.array([p for p, _ in parts])
        center[SHORT_NAMES[idx]] = (pts * w[:, None]).sum(0) / w.sum()

    # Polygon-derived borders between neighborhoods.
    with open(NEIGH_DIR / "boston_edges_land.csv") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")][1:]
    for kind, a, b in rows:
        if kind == "neighborhood":
            (x0, y0), (x1, y1) = center[a], center[b]
            ax_map.plot([x0, x1], [y0, y1], color="#333333", lw=0.9, zorder=3)
    # Hand-added water links (Charles River, Boston Harbor anchors).
    water = {"CharlesR": (-71.083, 42.362), "Harbor": (-70.99, 42.335)}
    for a, b in GEO_EDGES_ANCHOR:
        if b in water and a in center:
            (x0, y0), (x1, y1) = center[a], water[b]
            ax_map.plot([x0, x1], [y0, y1], color=C["red"], lw=0.9, ls="--", zorder=3)
    for name, (x, y) in water.items():
        ax_map.scatter([x], [y], marker="s", s=18, color=C["red"], zorder=4)
    for name, (x, y) in center.items():
        ax_map.scatter([x], [y], s=14, color="#333333", zorder=4)
    ax_map.set_xlim(-71.20, -70.96)
    ax_map.set_ylim(42.225, 42.40)
    ax_map.set_aspect(1 / np.cos(np.deg2rad(42.3)))
    ax_map.axis("off")
    north_arrow(ax_map, 0.10, 0.84)
    scale_bar(ax_map, 5, 0.74, 0.33)
    locant(ax_map, "A", x=0.0, y=0.98)
    sm = plt.cm.ScalarMappable(cmap=matplotlib.colors.LinearSegmentedColormap.from_list(
        "b", [cmap(0.15), cmap(0.95)]), norm=plt.Normalize(vmin, vmax))
    cax = fig.add_axes([0.03, 0.10, 0.16, 0.025])
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cb.set_label("Mean weekly rate per 100,000", fontsize=7)
    cb.ax.tick_params(labelsize=6.5)
    ax_map.legend(handles=[Line2D([], [], color="#333333", lw=0.9, label="Shared border (from boundary file)"),
                           Line2D([], [], color=C["red"], lw=0.9, ls="--", marker="s", ms=3,
                                  label="Water link (added by hand)")],
                  loc="lower right", bbox_to_anchor=(1.12, 0.12), frameon=False, fontsize=6.3)

    # Timeline of folds.
    seasons = [(2022, "2022-23"), (2023, "2023-24"), (2024, "2024-25"), (2025, "2025-26")]
    rows_t = [("Boston", {2022: "unseen", 2023: "unseen", 2024: "unseen", 2025: "dev"}),
              ("Columbus", {2024: "unseen", 2025: "dev"}),
              ("Chicago", {2022: "unseen", 2023: "unseen", 2024: "unseen", 2025: "unseen"})]
    fill = {"unseen": C["graph"], "dev": "#BBBBBB"}
    for i, (city, folds) in enumerate(rows_t):
        y = len(rows_t) - 1 - i
        start = {"Boston": 2017.95, "Columbus": 2022.5, "Chicago": 2019.75}[city]
        ax_t.barh(y, 2025.4 - start, left=start, height=0.18, color="#DDDDDD", zorder=1)
        for yr, kind in folds.items():
            x0 = yr + 0.42
            ax_t.barh(y, 1.0, left=x0, height=0.5, color=fill[kind], edgecolor="white",
                      zorder=2)
        ax_t.text(start - 0.1, y, city, ha="right", va="center", fontsize=7.5)
    ax_t.set_yticks([])
    ax_t.set_xlim(2016.2, 2026.6)
    ax_t.set_xticks(range(2018, 2027, 2))
    ax_t.spines["left"].set_visible(False)
    ax_t.set_xlabel("Year")
    ax_t.legend(handles=[Patch(color="#DDDDDD", label="Available history"),
                         Patch(color=C["graph"], label="Unseen test season (evidence)"),
                         Patch(color="#BBBBBB", label="Development season (not evidence)")],
                loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1, frameon=False)
    locant(ax_t, "B", x=-0.02, y=1.02)
    save(fig, "figure1_study_design")


# --------------------------------------------------------------------------- #
# Figure 2: error relative to persistence                                      #
# --------------------------------------------------------------------------- #
def relative_wis() -> pd.DataFrame:
    out = []
    for city, path in BACKTEST_CSV.items():
        d = pd.read_csv(path)
        d = d[d.season.isin(UNSEEN[city])]
        mean = d.groupby(["arm", "horizon"]).WIS.mean().unstack()
        rel = mean.div(mean.loc["persistence"], axis=1)
        for arm, *_ in MODELS:
            for h in HORIZONS:
                if arm in rel.index and h in rel.columns and pd.notna(rel.loc[arm, h]):
                    out.append({"city": city, "arm": arm, "horizon": h,
                                "WIS": mean.loc[arm, h], "rel": rel.loc[arm, h]})
    return pd.DataFrame(out)


def figure2() -> pd.DataFrame:
    rel = relative_wis()
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.6), sharey=True)
    offsets = np.linspace(-0.25, 0.25, len(MODELS))
    for ax, city, letter in zip(axes, BACKTEST_CSV, "ABC"):
        ax.axhline(1.0, color=C["persist"], lw=0.8, ls=":")
        for (arm, label, color, marker), off in zip(MODELS, offsets):
            sub = rel[(rel.city == city) & (rel.arm == arm)]
            xs = [HORIZONS.index(h) + off for h in sub.horizon]
            ax.plot(xs, sub.rel, marker=marker, color=color, ls="none", ms=4.5, label=label)
        ax.set_xticks(range(3), ["1", "2", "4"])
        ax.set_xlabel("Weeks ahead")
        ax.text(0.5, 1.02, CITY_LABEL[city], transform=ax.transAxes, ha="center",
                va="bottom", fontsize=8)
        locant(ax, letter, x=-0.02 if letter != "A" else -0.08, y=1.08)
    axes[0].set_ylabel("Relative WIS\n(below 1: less error than persistence)")
    axes[0].set_ylim(0.6, 1.5)
    axes[0].text(2.35, 1.01, "Persistence", fontsize=6.5, va="bottom", ha="right")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.1))
    fig.subplots_adjust(bottom=0.3, wspace=0.12)
    save(fig, "figure2_relative_wis")
    return rel


# --------------------------------------------------------------------------- #
# Figure 3: week-level differences with 95% intervals                          #
# --------------------------------------------------------------------------- #
def significance_rows() -> pd.DataFrame:
    rows = []
    for city, seasons in UNSEEN.items():
        base = RESULTS if city == "boston" else RESULTS / city
        for s in seasons:
            for h in HORIZONS:
                d = pd.read_csv(base / f"backtest_{s}" / f"horizon_{h:02d}" / "_comparison"
                                / "significance_tuned.csv")
                d["city"], d["season"] = city, s
                rows.append(d)
    return pd.concat(rows, ignore_index=True)


def figure3() -> pd.DataFrame:
    sig = significance_rows()
    # Panel titles are in the legend (AJE: no text on figures beyond locants and axes).
    comps = [("gnn_st_nograph_tuned", "A"), ("lstm_tuned", "B"), ("colagnn_tuned", "C")]
    order = [(c, s) for c, ss in UNSEEN.items() for s in ss]
    hcol = {1: "#0072B2", 2: "#E69F00", 4: "#009E73"}
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 3.9), sharey=True)
    for ax, (other, letter) in zip(axes, comps):
        ax.axvline(0, color="black", lw=0.7)
        for i, (city, s) in enumerate(order):
            for j, h in enumerate(HORIZONS):
                r = sig[(sig.city == city) & (sig.season == s) & (sig.horizon == h)
                        & (sig.model == other)]
                if r.empty:
                    continue
                r = r.iloc[0]
                y = len(order) - 1 - i + (0.22 - 0.22 * j)
                clear = r.DM_WIS_p_holm < 0.05
                # As a percentage of the comparison model's mean WIS, so Chicago's
                # levels and the other cities' rates share one axis.
                pct = 100.0 / r.WIS_other
                x, lo, hi = r.dWIS * pct, r.dWIS_lo * pct, r.dWIS_hi * pct
                ax.errorbar(x, y, xerr=[[x - lo], [hi - x]],
                            fmt="o", ms=3.8, color=hcol[h], mfc=hcol[h] if clear else "white",
                            elinewidth=0.9, capsize=0)
        ax.set_xlabel("Difference, % of\ncomparison WIS")
        locant(ax, letter, x=-0.02 if letter != "A" else -0.45, y=1.02)
    axes[0].set_yticks(range(len(order)),
                       [f"{CITY_LABEL[c]} {season_text(c, s)}" for c, s in reversed(order)])
    hz = [Line2D([], [], marker="o", ls="none", color=hcol[h], label=f"{h} week{'s' if h > 1 else ''} ahead")
          for h in HORIZONS]
    fill = [Line2D([], [], marker="o", ls="none", color="grey", mfc="grey",
                   label="Filled: clear after correction for multiple comparisons"),
            Line2D([], [], marker="o", ls="none", color="grey", mfc="white", label="Open: not clear")]
    fig.legend(handles=hz, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.55, -0.02))
    fig.legend(handles=fill, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.55, -0.075))
    fig.subplots_adjust(bottom=0.25, wspace=0.1)
    save(fig, "figure3_week_level_differences")
    return sig


# --------------------------------------------------------------------------- #
# Figure 4: example forecast and interval coverage                             #
# --------------------------------------------------------------------------- #
def coverage(city: str, arm: str, h: int) -> tuple[float, float]:
    d = pd.concat([predictions(city, s, h, arm) for s in UNSEEN[city]])
    d = d.dropna(subset=["actual"])
    c50 = ((d.actual >= d["q0.250"]) & (d.actual <= d["q0.750"])).mean()
    c95 = ((d.actual >= d["q0.025"]) & (d.actual <= d["q0.975"])).mean()
    return float(c50), float(c95)


def figure4() -> pd.DataFrame:
    # Paper Figure 5. A: calibration by horizon. B-D: one neighborhood-season
    # (Dorchester, the highest-rate neighborhood, 2024-25) at 1, 2 and 4 weeks,
    # so the reader sees persistence fall further behind as the lead grows.
    import matplotlib.dates as mdates
    fig = plt.figure(figsize=(7.0, 5.4))
    ax_b = fig.add_axes([0.08, 0.10, 0.25, 0.84])
    axes = [fig.add_axes([0.47, 0.10 + k * 0.29, 0.51, 0.23]) for k in (2, 1, 0)]

    hood, season = "Dorchester", "2024_25"
    rel = {}
    for k, (ax_a, h) in enumerate(zip(axes, HORIZONS)):
        g = predictions("boston", season, h, "gnn_st_tuned")
        g = g[g.neighborhood == hood].sort_values("target_date")
        p = predictions("boston", season, h, "persistence")
        p = p[p.neighborhood == hood].sort_values("target_date")
        ax_a.fill_between(g.target_date, g["q0.025"], g["q0.975"], color=C["graph"], alpha=0.18,
                          lw=0, label="95% interval")
        ax_a.fill_between(g.target_date, g["q0.250"], g["q0.750"], color=C["graph"], alpha=0.35,
                          lw=0, label="50% interval")
        ax_a.plot(g.target_date, g["q0.500"], color=C["graph"], lw=1.2, label="Graph model (median)")
        ax_a.plot(p.target_date, p.predicted, color=C["persist"], lw=0.8, ls=":",
                  label="Persistence")
        ax_a.plot(g.target_date, g.actual, "o", color="black", ms=2.0, label="Observed")
        ax_a.set_ylim(0, 330)
        ax_a.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[7, 10, 1, 4]))
        ax_a.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        if k < 2:
            ax_a.tick_params(labelbottom=False)
        if k == 0:
            ax_a.legend(loc="upper left", frameon=False, fontsize=6.3)
        locant(ax_a, "BCD"[k], x=-0.11, y=1.0)
        gg, pp = g.dropna(subset=["actual"]), p.dropna(subset=["actual"])
        rel[h] = (wis_from_quantiles(gg.actual, gg[list(QUANTILE_COLUMNS)]).mean()
                  / wis_from_quantiles(pp.actual, pp[list(QUANTILE_COLUMNS)]).mean())
    axes[-1].set_xlabel("Target week")
    fig.text(0.405, 0.10 + 0.29 + 0.115, "ED visits for ILI per 100,000", rotation=90,
             va="center", ha="center")
    print("  Figure 5 Dorchester 2024-25 relative WIS:",
          ", ".join(f"h{h} {v:.2f}" for h, v in rel.items()))

    rows = []
    arms = [("gnn_st_tuned", "Graph model", C["graph"]), ("lstm_tuned", "LSTM", C["lstm"]),
            ("colagnn_tuned", "Cola-GNN", C["cola"]), ("persistence", "Persistence", C["persist"])]
    for k, (arm, label, color) in enumerate(arms):
        for j, hh in enumerate(HORIZONS):
            c50, c95 = coverage("boston", arm, hh)
            rows.append({"arm": arm, "horizon": hh, "cov50": c50, "cov95": c95})
            x = j + (k - 1.5) * 0.17
            ax_b.plot(x, c95 * 100, marker="o", color=color, ms=3.8, ls="none",
                      label=label if j == 0 else None)
            ax_b.plot(x, c50 * 100, marker="o", color=color, mfc="white", ms=3.8, ls="none")
    ax_b.axhline(95, color="grey", lw=0.7, ls=":")
    ax_b.axhline(50, color="grey", lw=0.7, ls=":")
    ax_b.set_ylim(30, 100)
    ax_b.set_xticks(range(3), ["1", "2", "4"])
    ax_b.set_xlabel("Weeks ahead")
    ax_b.set_ylabel("Observed values inside interval, %")
    ax_b.legend(loc="center right", frameon=False, fontsize=6.5, bbox_to_anchor=(1.0, 0.72))
    # The legend says the dotted lines mark the stated coverage, so no labels on them.
    locant(ax_b, "A", x=-0.3, y=1.01)
    save(fig, "figure5_example_and_coverage")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# Figure 5: where the map helps, neighborhood by neighborhood                  #
# --------------------------------------------------------------------------- #
from influenza.scoring import FLUSIGHT_QUANTILES, pit_values, wis_from_quantiles  # noqa: E402
from influenza.intervals import QUANTILE_COLUMNS  # noqa: E402


def cell_wis(city: str, h: int, arm: str) -> pd.DataFrame:
    d = pd.concat([predictions(city, s, h, arm) for s in UNSEEN[city]])
    d = d.dropna(subset=["actual"]).copy()
    d["WIS"] = wis_from_quantiles(d.actual, d[list(QUANTILE_COLUMNS)])
    return d[["target_date", "neighborhood", "WIS"]]


def map_benefit(h: int) -> pd.Series:
    g = cell_wis("boston", h, "gnn_st_tuned")
    n = cell_wis("boston", h, "gnn_st_nograph_tuned")
    m = g.merge(n, on=["target_date", "neighborhood"], suffixes=("_g", "_n"))
    by = m.groupby("neighborhood")[["WIS_g", "WIS_n"]].mean()
    return 100 * (by.WIS_n - by.WIS_g) / by.WIS_n  # % less error with the map


def figure5() -> pd.DataFrame:
    geo = json.loads((NEIGH_DIR / "boston_polygons_tract_neighborhoods.geojson").read_text())
    ben = {h: map_benefit(h) for h in HORIZONS}
    lim = float(np.ceil(max(b.abs().max() for b in ben.values()) / 5) * 5)
    lo = min(0.0, float(min(b.min() for b in ben.values())))
    cmap = plt.get_cmap("Blues") if lo == 0 else plt.get_cmap("RdBu")
    norm = plt.Normalize(0 if lo == 0 else -lim, lim)
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 3.0))
    for ax, h, letter in zip(axes, HORIZONS, "ABC"):
        polys, colors = [], []
        for feat in geo["features"]:
            idx = GEOID_TO_IDX.get(feat["properties"]["neighborhood"])
            if idx is None:
                continue
            v = ben[h].get(NEIGHBORHOODS[idx], np.nan)
            for ring in rings(feat["geometry"]):
                polys.append(ring)
                colors.append(cmap(norm(v)))
        ax.add_collection(PolyCollection(polys, facecolors=colors, edgecolors="white", linewidths=0.3))
        ax.set_xlim(-71.20, -70.98)
        ax.set_ylim(42.225, 42.40)
        ax.set_aspect(1 / np.cos(np.deg2rad(42.3)))
        ax.axis("off")
        north_arrow(ax, 0.10, 0.92, length=0.08, fontsize=6.5)
        scale_bar(ax, 5, 0.62, 0.06, fontsize=6)
        locant(ax, letter, x=0.0, y=1.0)
    cax = fig.add_axes([0.3, 0.08, 0.4, 0.035])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
    cb.set_label("Less forecast error (WIS) with the map than without, %", fontsize=7)
    cb.ax.tick_params(labelsize=6.5)
    fig.subplots_adjust(bottom=0.2, wspace=0.02)
    save(fig, "figure4_map_benefit_by_neighborhood")
    return pd.DataFrame(ben).round(1)


# --------------------------------------------------------------------------- #
# Supplementary figures                                                        #
# --------------------------------------------------------------------------- #
def figure_s1_blend() -> pd.DataFrame:
    """Learned weight on the current week versus the seasonal curve."""
    rows = []
    for city, seasons in UNSEEN.items():
        base = RESULTS if city == "boston" else RESULTS / city
        for s in seasons:
            for h in HORIZONS:
                (cfg,) = list((base / f"backtest_{s}" / f"horizon_{h:02d}" / "gnn_st_tuned").glob("*/run_config.json"))
                share = json.loads(cfg.read_text())["blend_origin_share_per_horizon"][str(h)]
                rows.append({"city": city, "season": s, "horizon": h, "share": share})
    d = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    style = {("boston", "2022_23"): ("o", "#003f7f", "-"), ("boston", "2023_24"): ("o", C["graph"], "--"),
             ("boston", "2024_25"): ("o", C["nograph"], ":"),
             ("columbus", "2024_25"): ("s", C["lstm"], "-"),
             ("chicago", "2022_23"): ("D", "#005c45", "-"), ("chicago", "2023_24"): ("D", C["cola"], "--"),
             ("chicago", "2024_25"): ("D", "#5fc9a6", ":"), ("chicago", "2025_26"): ("D", "#9de0c8", "-.")}
    for (city, s), g in d.groupby(["city", "season"]):
        mk, col, ls = style[(city, s)]
        ax.plot([HORIZONS.index(h) for h in g.horizon], g.share, marker=mk, color=col, lw=1.0, ls=ls,
                ms=4, alpha=0.95, label=f"{CITY_LABEL[city]} {season_text(city, s)}")
    ax.axhline(0.5, color="grey", lw=0.6, ls=":")
    ax.set_xticks(range(3), ["1", "2", "4"])
    ax.set_xlabel("Weeks ahead")
    ax.set_ylabel("Weight on the current week\n(1 minus weight on the seasonal curve)")
    ax.set_ylim(0, 1)
    ax.legend(frameon=False, fontsize=6.3, loc="lower left")
    save(fig, "figureS1_blend_weight")
    return d


def figure_s2_tuning() -> pd.DataFrame:
    """How much equal-budget tuning improved each model on validation weeks."""
    cfg = json.loads((ROOT / "Code" / "sweep" / "tuned_configs.json").read_text())
    arms = [("gnn_st", "Graph neural network", C["graph"]), ("gnn_st_nograph", "Same model, map removed", C["nograph"]),
            ("lstm", "LSTM", C["lstm"]), ("xgboost", "Gradient-boosted trees", C["red"]),
            ("colagnn", "Cola-GNN", C["cola"])]
    rows = []
    tuned_cities = list(UNSEEN)
    for city in tuned_cities:
        for s in UNSEEN[city]:
            for h, arms_h in cfg[city][s].items():
                for a, v in arms_h.items():
                    rows.append({"city": city, "arm": a, "gain": 100 * (1 - v["val_mae"] / v["default_val_mae"])})
    d = pd.DataFrame(rows)
    fig, axes = plt.subplots(1, len(tuned_cities), figsize=(7.0, 2.4), sharey=True)
    for ax, city, letter in zip(axes, tuned_cities, "ABC"):
        for i, (a, label, col) in enumerate(arms):
            g = d[(d.city == city) & (d.arm == a)].gain
            y = len(arms) - 1 - i
            ax.scatter(g, np.full(len(g), y) + np.linspace(-0.12, 0.12, len(g)), s=10, color=col, alpha=0.6)
            ax.plot([g.mean()], [y], marker="|", ms=12, mew=2, color="black")
        ax.set_yticks(range(len(arms)), [lab for _, lab, _ in reversed(arms)])
        ax.text(0.5, 1.02, CITY_LABEL[city], transform=ax.transAxes, ha="center", fontsize=8)
        locant(ax, letter, x=-0.02 if letter != "A" else -0.9)
    fig.supxlabel("Reduction in validation error, %", fontsize=8, x=0.6, y=-0.06)
    save(fig, "figureS2_tuning_gains")
    return d.groupby(["city", "arm"]).gain.mean().unstack().round(1)


def figure_s3_pit() -> None:
    """PIT histograms: flat means calibrated forecast distributions."""
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.2), sharey=True)
    for ax, h, letter in zip(axes, HORIZONS, "ABC"):
        d = pd.concat([predictions("boston", s, h, "gnn_st_tuned") for s in UNSEEN["boston"]]).dropna(subset=["actual"])
        pit = pit_values(d.actual.values, d[list(QUANTILE_COLUMNS)].values, FLUSIGHT_QUANTILES)
        ax.hist(pit, bins=10, range=(0, 1), density=True, color=C["graph"], edgecolor="white")
        ax.axhline(1, color="black", lw=0.7, ls=":")
        ax.set_xlabel("Probability integral transform")
        ax.text(0.5, 1.02, f"{h} week{'s' if h > 1 else ''} ahead", transform=ax.transAxes, ha="center", fontsize=8)
        locant(ax, letter, x=-0.02 if letter != "A" else -0.2)
    axes[0].set_ylabel("Density")
    save(fig, "figureS3_pit")


def figure_s4_all_neighborhoods() -> None:
    """Two-week-ahead forecasts for all 14 neighborhoods, one unseen season."""
    season, h = "2024_25", 2
    g = predictions("boston", season, h, "gnn_st_tuned")
    fig, axes = plt.subplots(4, 4, figsize=(7.0, 7.0), sharex=True)
    import matplotlib.dates as mdates
    for ax, hood in zip(axes.flat, NEIGHBORHOODS):
        x = g[g.neighborhood == hood].sort_values("target_date")
        ax.fill_between(x.target_date, x["q0.025"], x["q0.975"], color=C["graph"], alpha=0.2, lw=0)
        ax.fill_between(x.target_date, x["q0.250"], x["q0.750"], color=C["graph"], alpha=0.35, lw=0)
        ax.plot(x.target_date, x["q0.500"], color=C["graph"], lw=0.9)
        ax.plot(x.target_date, x.actual, "o", color="black", ms=1.4)
        name = hood.replace("Back Bay/Beacon Hill/Downtown/North End/West End",
                            "Back Bay, Beacon Hill, Downtown,\nNorth End, West End")
        ax.set_title(name, fontsize=7 if "\n" in name else 7.5)
        ax.tick_params(labelsize=6)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[9, 1, 5]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    for ax in list(axes.flat)[len(NEIGHBORHOODS):]:
        ax.axis("off")
    fig.supylabel("ED visits for ILI per 100,000", fontsize=8)
    fig.tight_layout()
    save(fig, "figureS4_all_neighborhoods")


SEVERITY = RESULTS / "_severity_backtest"
BANDS = ["Low", "Moderate", "High", "Very high"]


def severity_confusion(arm: str, h: int = 2) -> np.ndarray:
    """Observed x forecast band counts, Boston unseen seasons, best-guess banding.

    Reads the per-cell bands compare_severity.py wrote for each fold (thresholds
    fitted only on seasons before it), the same rows Tables S12 and S13 score.
    """
    frames = [pd.read_csv(SEVERITY / "boston" / s / f"horizon_{h:02d}" / "severity_bands.csv")
              for s in UNSEEN["boston"]]
    d = pd.concat(frames)
    d = d[(d.model == arm) & (d.indicator != "CITYWIDE")].dropna(subset=["actual"])
    m = np.zeros((4, 4), dtype=int)
    for t, p in zip(d.true_band.astype(int), d.pred_band.astype(int)):
        m[t, p] += 1
    return m


def figure6() -> dict[str, np.ndarray]:
    """Severity band of each neighborhood-week: observed vs best-guess forecast, 2 weeks ahead."""
    arms = [("gnn_st_tuned", "A"), ("persistence", "B")]
    mats = {a: severity_confusion(a) for a, _ in arms}
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.1))
    cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list("blues", ["#FFFFFF", C["graph"]])
    for ax, (arm, letter) in zip(axes, arms):
        m = mats[arm]
        share = m / m.sum(axis=1, keepdims=True)  # shade by share of each observed band
        ax.imshow(share, cmap=cmap, vmin=0, vmax=1)
        for i in range(4):
            for j in range(4):
                ax.text(j, i, f"{m[i, j]:,}", ha="center", va="center", fontsize=7.5,
                        color="white" if share[i, j] > 0.55 else "black")
        ax.set_xticks(range(4), BANDS)
        ax.set_yticks(range(4), BANDS if letter == "A" else [""] * 4)
        ax.set_xlabel("Forecast band (best guess)")
        if letter == "A":
            ax.set_ylabel("Observed band")
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(length=0)
        locant(ax, letter, x=-0.32 if letter == "A" else -0.05)
    fig.tight_layout(w_pad=1.5)
    save(fig, "figure6_severity_confusion")
    return mats


def main() -> None:
    only = set(sys.argv[1:])  # e.g. `make_figures.py figure1 figure5` regenerates just those
    if only:
        for name in sorted(only):
            globals()[name]()
        return
    figure1()
    rel = figure2()
    figure3()
    cov = figure4()
    ben = figure5()
    blend = figure_s1_blend()
    tune = figure_s2_tuning()
    figure_s3_pit()
    figure_s4_all_neighborhoods()
    sev = figure6()
    # Numbers the text quotes, printed so the data check can compare against them.
    print("\nRelative WIS (unseen seasons):")
    print(rel.pivot_table(index=["city", "arm"], columns="horizon", values="rel").round(3).to_string())
    print("\nInterval coverage, Boston unseen seasons:")
    print(cov.pivot_table(index="arm", columns="horizon", values=["cov50", "cov95"]).round(3).to_string())
    print("\nPercent less WIS with the map, by neighborhood (Boston unseen seasons):")
    print(ben.to_string())
    print("\nLearned weight on the current week:")
    print(blend.pivot_table(index=["city", "season"], columns="horizon", values="share").round(2).to_string())
    print("\nMean tuning gain on validation MAE, %:")
    print(tune.to_string())
    print("\nSeverity bands, Boston unseen seasons, 2 weeks ahead (rows observed, columns forecast):")
    for arm, m in sev.items():
        print(arm)
        print(m)


if __name__ == "__main__":
    main()
