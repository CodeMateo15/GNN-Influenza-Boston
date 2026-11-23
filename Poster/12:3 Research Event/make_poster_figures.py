"""Poster-sized figures, drawn from the paper's own code and backtest outputs.

- p_relative_wis: paper Figure 2 (`make_figures.relative_wis`)
- p_forecast_paths: forecasts made on single weeks of Dorchester's 2024-25 season, each drawn 1, 2
  and 4 weeks ahead from the same `predictions.csv` files as paper Figure 4
- p_map_benefit: paper Figure 6 (`make_figures.map_benefit`)
- p_fig1a_map, p_fig1c_model: cropped from paper Figure 1's vector PDF at 600 dpi

Text is set in Avenir Next to match the poster. Nothing is retrained.

    /opt/anaconda3/bin/python "Poster/12:3 Research Event/make_poster_figures.py"
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "Paper" / "scripts"))

import make_figures as mf  # noqa: E402
import matplotlib.dates as mdates  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from PIL import Image  # noqa: E402

plt = mf.plt
OUT = HERE / "figures"
PAPER_FIG = ROOT / "Paper" / "overleaf_v2" / "figures"
INK, TEAL, AMBER = "#1E2A32", "#0B5D5E", "#D9822B"


def _avenir() -> None:
    """matplotlib loads only one face from a .ttc, so write the faces we use out as .ttf files."""
    from fontTools.ttLib import TTCollection
    from matplotlib import font_manager
    ttc = Path("/System/Library/Fonts/Avenir Next.ttc")
    if not ttc.exists():
        return
    tmp = Path(tempfile.mkdtemp())
    for k, font in enumerate(TTCollection(str(ttc)).fonts):
        if font["name"].getDebugName(1) == "Avenir Next" and font["name"].getDebugName(2) in ("Regular", "Bold", "Italic"):
            font.save(tmp / f"avenir_{k}.ttf")
            font_manager.fontManager.addfont(str(tmp / f"avenir_{k}.ttf"))
    plt.rcParams["font.family"] = "Avenir Next"


_avenir()
plt.rcParams.update({
    "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.edgecolor": "#5E6B73",
    "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11, "xtick.labelsize": 10,
    "ytick.labelsize": 10, "legend.fontsize": 10,
})


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.png", dpi=400, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"wrote figures/{name}.png")


def relative_wis_poster() -> None:
    rel = mf.relative_wis()
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.2), sharey=True)
    offsets = np.linspace(-0.27, 0.27, len(mf.MODELS))
    for ax, city in zip(axes, mf.BACKTEST_CSV):
        ax.axhline(1.0, color="black", lw=0.9, ls=":")
        for (arm, label, color, marker), off in zip(mf.MODELS, offsets):
            sub = rel[(rel.city == city) & (rel.arm == arm)]
            xs = [mf.HORIZONS.index(h) + off for h in sub.horizon]
            ms = 8 if arm == "gnn_st_tuned" else 6
            ax.plot(xs, sub.rel, marker=marker, color=color, ls="none", ms=ms, label=label,
                    zorder=4 if arm == "gnn_st_tuned" else 3)
        ax.set_xticks(range(3), ["1", "2", "4"])
        ax.set_xlabel("Weeks ahead")
        ax.set_title(mf.CITY_LABEL[city], fontweight="bold", color=TEAL)
    axes[0].set_ylabel("Error vs persistence\n(relative WIS)")
    axes[0].set_ylim(0.6, 1.4)
    axes[0].text(0.02, 0.97, "dotted line: persistence", transform=axes[0].transAxes, fontsize=9,
                 va="top", ha="left")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.01),
               handletextpad=0.3, columnspacing=1.0)
    fig.subplots_adjust(bottom=0.33, wspace=0.08)
    save(fig, "p_relative_wis")


def forecast_paths_poster() -> None:
    """What the model said on single weeks of Dorchester's 2024-25 season, against persistence.

    Each path starts at the week the forecast was made and joins its 1-, 2- and 4-week medians, with
    the 95% range shaded. Persistence would be a flat line from the same starting point.
    """
    hood, season = "Dorchester", "2024_25"
    preds = {}
    for h in mf.HORIZONS:
        d = mf.predictions("boston", season, h, "gnn_st_tuned")
        preds[h] = d[d.neighborhood == hood].set_index("origin_date")
    obs = (preds[1].reset_index()[["target_date", "actual"]].dropna()
           .set_index("target_date").actual.sort_index())
    peak = obs.idxmax()
    origins = [peak - pd.Timedelta(weeks=w) for w in (6, 2, 0)] + \
              [peak + pd.Timedelta(weeks=3)]
    fig, ax = plt.subplots(figsize=(10.4, 2.9))
    ax.plot(obs.index, obs.values, "o-", color=INK, ms=3.6, lw=0.9, label="Observed", zorder=5)
    for k, o in enumerate(origins):
        t = [o] + [preds[h].loc[o, "target_date"] for h in mf.HORIZONS]
        med = [obs[o]] + [preds[h].loc[o, "q0.500"] for h in mf.HORIZONS]
        lo = [obs[o]] + [preds[h].loc[o, "q0.025"] for h in mf.HORIZONS]
        hi = [obs[o]] + [preds[h].loc[o, "q0.975"] for h in mf.HORIZONS]
        ax.fill_between(t, lo, hi, color=mf.C["graph"], alpha=0.13, lw=0,
                        label="95% range" if k == 0 else None)
        ax.plot(t, med, "-", color=mf.C["graph"], lw=2.4, marker="o", ms=4.5, markevery=[1, 2, 3],
                label="Graph model: 1, 2, 4 weeks ahead" if k == 0 else None, zorder=4)
        ax.plot([o, t[-1]], [obs[o]] * 2, ls=(0, (2, 2)), color=AMBER, lw=1.8,
                label="Persistence (repeats this week)" if k == 0 else None, zorder=3)
        ax.plot(o, obs[o], "o", ms=9, mfc="white", mec=mf.C["graph"], mew=2, zorder=6)
    ax.set_xlim(peak - pd.Timedelta(weeks=10), peak + pd.Timedelta(weeks=10))
    ax.set_ylim(0, 340)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_ylabel("ED visits for ILI\nper 100,000")
    ax.legend(loc="upper left", frameon=False, ncol=1, handlelength=2.2)
    save(fig, "p_forecast_paths")


def map_benefit_poster() -> None:
    geo = json.loads((mf.NEIGH_DIR / "boston_polygons_tract_neighborhoods.geojson").read_text())
    ben = {h: mf.map_benefit(h) for h in mf.HORIZONS}
    assert min(b.min() for b in ben.values()) > 0, "map no longer helps every neighborhood"
    cmap, norm = plt.get_cmap("Blues"), plt.Normalize(0, 20)
    fig, axes = plt.subplots(1, 3, figsize=(6.0, 2.9))
    for ax, h in zip(axes, mf.HORIZONS):
        polys, colors = [], []
        for feat in geo["features"]:
            idx = mf.GEOID_TO_IDX.get(feat["properties"]["neighborhood"])
            if idx is None:
                continue
            v = ben[h].get(mf.NEIGHBORHOODS[idx], np.nan)
            for ring in mf.rings(feat["geometry"]):
                polys.append(ring)
                colors.append(cmap(norm(v)))
        ax.add_collection(PolyCollection(polys, facecolors=colors, edgecolors="white", linewidths=0.4))
        ax.set_xlim(-71.20, -70.98)
        ax.set_ylim(42.225, 42.40)
        ax.set_aspect(1 / np.cos(np.deg2rad(42.3)))
        ax.axis("off")
        ax.set_title(f"{h} week{'s' if h > 1 else ''} ahead", fontweight="bold", color=TEAL)
    mf.north_arrow(axes[0], 0.10, 0.92, length=0.08, fontsize=9)
    mf.scale_bar(axes[0], 5, 0.62, 0.06, fontsize=8.5)
    cax = fig.add_axes([0.3, 0.1, 0.4, 0.035])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
    cb.set_ticks([0, 5, 10, 15, 20])
    cb.set_label("% less forecast error with the map")
    fig.subplots_adjust(bottom=0.16, wspace=0.02, top=0.92)
    save(fig, "p_map_benefit")
    for h, b in ben.items():
        print(f"  map benefit h{h}: {b.min():.1f}% to {b.max():.1f}%")


def model_simple_poster() -> None:
    """A three-step picture of the model for a general audience: recent weeks -> neighbors -> range.

    The curve in step 1 is Dorchester's real 2024-25 rise (16 weeks up to the peak) and step 3 is the
    model's real forecast made at that peak, so the icons are not invented data.
    """
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
    hood, season = "Dorchester", "2024_25"
    preds = {}
    for h in mf.HORIZONS:
        d = mf.predictions("boston", season, h, "gnn_st_tuned")
        preds[h] = d[d.neighborhood == hood].set_index("origin_date")
    obs = (preds[1].reset_index()[["target_date", "actual"]].dropna()
           .set_index("target_date").actual.sort_index())
    peak = obs.idxmax()
    past = obs[(obs.index > peak - pd.Timedelta(weeks=16)) & (obs.index <= peak)]

    fig = plt.figure(figsize=(8.8, 2.3))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 8.8)
    ax.set_ylim(0, 2.3)
    ax.axis("off")
    boxes = [(0.05, "1  Recent weeks", "each area’s past 16 weeks,\nplus weather and demographics"),
             (3.05, "2  Ask the neighbors", "areas that share a border\npass their signals along"),
             (6.05, "3  Forecast a range", "1, 2 and 4 weeks ahead,\nwith 50% and 95% ranges")]
    bw, bh, by = 2.7, 2.2, 0.05
    for x, title, sub in boxes:
        ax.add_patch(FancyBboxPatch((x, by), bw, bh, boxstyle="round,pad=0,rounding_size=0.12",
                                    fc="#E4EFEE", ec="none"))
        ax.text(x + 0.12, by + bh - 0.12, title, fontsize=14.5, fontweight="bold", color=TEAL,
                va="top", ha="left")
        ax.text(x + 0.12, by + 0.1, sub, fontsize=12, color=INK, va="bottom", ha="left",
                linespacing=1.15)
    for x in (2.78, 5.78):
        ax.add_patch(FancyArrowPatch((x, 1.2), (x + 0.24, 1.2), arrowstyle="-|>", mutation_scale=18,
                                     color=AMBER, lw=2.2))

    # icon areas: x0..x0+2.4, y 0.75..1.95
    def to_icon(x0, xs, ys, xlim, ylim):
        X = x0 + 0.15 + (np.asarray(xs) - xlim[0]) / (xlim[1] - xlim[0]) * 2.4
        Y = 0.74 + (np.asarray(ys) - ylim[0]) / (ylim[1] - ylim[0]) * 0.98
        return X, Y

    # 1: the real rise
    t = np.arange(len(past))
    X, Y = to_icon(0.05, t, past.values, (0, len(past) - 1), (0, 320))
    ax.plot(X, Y, "-o", color=INK, lw=1.4, ms=2.6)

    # 2: a centre area and its neighbors
    cx, cy = 3.05 + 1.35, 1.22
    nb = [(-0.85, 0.27), (-0.55, -0.34), (0.15, 0.43), (0.75, 0.22), (0.65, -0.32)]
    for dx, dy in nb:
        ax.add_patch(FancyArrowPatch((cx + dx, cy + dy), (cx + dx * 0.22, cy + dy * 0.22), arrowstyle="-|>",
                                     mutation_scale=10, color="#5E6B73", lw=1.3))
        ax.plot(cx + dx, cy + dy, "o", ms=11, color=mf.C["nograph"], mec="white", mew=1.2)
    ax.plot(cx, cy, "o", ms=17, color=mf.C["graph"], mec="white", mew=1.5)

    # 3: the real forecast made at the peak
    t = [0] + list(mf.HORIZONS)
    med = [obs[peak]] + [preds[h].loc[peak, "q0.500"] for h in mf.HORIZONS]
    lo = [obs[peak]] + [preds[h].loc[peak, "q0.025"] for h in mf.HORIZONS]
    hi = [obs[peak]] + [preds[h].loc[peak, "q0.975"] for h in mf.HORIZONS]
    lim = ((0, 4), (0, 380))
    X, M_ = to_icon(6.05, t, med, *lim)
    _, L = to_icon(6.05, t, lo, *lim)
    _, H = to_icon(6.05, t, hi, *lim)
    _, L50 = to_icon(6.05, t, [obs[peak]] + [preds[h].loc[peak, "q0.250"] for h in mf.HORIZONS], *lim)
    _, H50 = to_icon(6.05, t, [obs[peak]] + [preds[h].loc[peak, "q0.750"] for h in mf.HORIZONS], *lim)
    ax.fill_between(X, L, H, color=mf.C["graph"], alpha=0.16, lw=0)
    ax.fill_between(X, L50, H50, color=mf.C["graph"], alpha=0.3, lw=0)
    ax.plot(X, M_, "-o", color=mf.C["graph"], lw=2.2, ms=4)
    ax.plot(X[0], M_[0], "o", ms=8, mfc="white", mec=mf.C["graph"], mew=1.8)
    save(fig, "p_model_simple")


def figure1_crops() -> None:
    """Fig 1A (map) and 1C (model diagram), cropped from the 600-dpi vector render."""
    with tempfile.TemporaryDirectory() as td:
        stem = Path(td) / "f1"
        subprocess.run(["pdftoppm", "-r", "600", "-png", "-singlefile",
                        str(PAPER_FIG / "figure1_study_design.pdf"), str(stem)], check=True)
        im = Image.open(f"{stem}.png").convert("RGB")
    W, H = im.size
    # Blank the panel letters ("A)" top left, "C)" above the diagram); the poster titles the panels.
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, int(0.05 * W), int(0.065 * H)), fill="white")
    d.rectangle((0, int(0.64 * H), int(0.05 * W), int(0.685 * H)), fill="white")
    # Fractions of the full figure, read off the paper PNG: A) occupies the top-left half (its
    # "A)" label sits above the map's top edge), C) the bottom 31% (below its "C)" label).
    boxes = {"p_fig1a_map": (0.0, 0.050, 0.52, 0.640), "p_fig1c_model": (0.0, 0.690, 1.0, 1.0)}
    for name, (x0, y0, x1, y1) in boxes.items():
        crop = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
        a = np.asarray(crop.convert("L"))
        ys, xs = np.where(a < 245)
        crop = crop.crop((max(xs.min() - 20, 0), max(ys.min() - 20, 0),
                          min(xs.max() + 20, crop.width), min(ys.max() + 20, crop.height)))
        OUT.mkdir(parents=True, exist_ok=True)
        crop.save(OUT / f"{name}.png", dpi=(600, 600))
        print(f"wrote figures/{name}.png {crop.size}")


if __name__ == "__main__":
    relative_wis_poster()
    forecast_paths_poster()
    map_benefit_poster()
    model_simple_poster()
    figure1_crops()
