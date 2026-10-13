"""The two BPHC figures, drawn from the tables `make_bphc.build` returns.

Every forecast panel uses one hue: the panel title names the model, so color
never has to tell models apart. The darker band is the 50% range, the lighter
band the 95% range, and the line is the estimate (the median).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

SURFACE = "#ffffff"
INK = "#1a1a1a"
INK_MUTED = "#666666"
GRID = "#e6e6e6"
OBSERVED = "#2c3e50"
FORECAST = "#2a78d6"
BAND50_ALPHA, BAND95_ALPHA = 0.38, 0.16
HISTORY_WEEKS = 20


def _style(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK_MUTED)
    ax.tick_params(colors=INK_MUTED, labelsize=8)


def _panel(ax, observed: pd.DataFrame, forecast: pd.DataFrame, history_weeks: int) -> None:
    """Recent observations, then the forecast fan anchored at the last observed week."""
    _style(ax)
    # A fixed window of calendar weeks, reindexed so weeks BPHC did not report
    # (suppressed small counts) show as gaps instead of being bridged.
    origin = forecast["origin_date"].max()
    weeks = pd.date_range(end=origin, periods=history_weeks, freq="7D")
    seen = (observed.set_index("week")["rate"].reindex(weeks).rename_axis("week")
            .reset_index())
    ax.plot(seen["week"], seen["rate"], color=OBSERVED, linewidth=2, marker="o", markersize=2.5,
            zorder=3)
    fc = forecast.sort_values("target_date")
    last = seen.iloc[-1]
    if pd.notna(last["rate"]):
        start = pd.DataFrame({"target_date": [last["week"]], "estimate": [last["rate"]],
                              "low95": [last["rate"]], "high95": [last["rate"]],
                              "low50": [last["rate"]], "high50": [last["rate"]]})
        fc = pd.concat([start, fc], ignore_index=True)
    ax.axvline(origin, color=INK_MUTED, linewidth=0.8, linestyle=(0, (3, 3)), zorder=1)
    ax.fill_between(fc["target_date"], fc["low95"], fc["high95"], color=FORECAST,
                    alpha=BAND95_ALPHA, linewidth=0, zorder=1)
    ax.fill_between(fc["target_date"], fc["low50"], fc["high50"], color=FORECAST,
                    alpha=BAND50_ALPHA, linewidth=0, zorder=2)
    ax.plot(fc["target_date"], fc["estimate"], color=FORECAST, linewidth=2, zorder=4)
    ax.plot(fc["target_date"].iloc[1:], fc["estimate"].iloc[1:], "o", color=FORECAST,
            markersize=4.5, markeredgecolor=SURFACE, markeredgewidth=1, zorder=5)
    ax.set_ylim(bottom=0)


def _legend(fig, **kwargs) -> None:
    handles = [Line2D([0], [0], color=OBSERVED, linewidth=2, label="Observed"),
               Line2D([0], [0], color=FORECAST, linewidth=2, marker="o", markersize=4.5,
                      label="Forecast estimate"),
               Patch(color=FORECAST, alpha=BAND50_ALPHA, linewidth=0, label="50% range"),
               Patch(color=FORECAST, alpha=BAND95_ALPHA, linewidth=0, label="95% range")]
    fig.legend(handles=handles, frameon=False, fontsize=9, labelcolor=INK, ncol=4, **kwargs)


def _header(fig, title: str, subtitle: str | None, legend_inches: float) -> None:
    """Title block and legend in fixed inches, so they never collide with the panels."""
    height = fig.get_size_inches()[1]
    top = 1 - (0.75 if subtitle else 0.5) / height
    fig.tight_layout(rect=(0, legend_inches / height, 1, top))
    fig.text(0.01, 1 - 0.15 / height, title, ha="left", va="top", fontsize=13, color=INK)
    if subtitle:
        fig.text(0.01, 1 - 0.45 / height, subtitle, ha="left", va="top", fontsize=9,
                 color=INK_MUTED)


def _dates(fig) -> None:
    for ax in fig.axes:
        ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b"))


def plot_citywide(tables: dict, path: Path, history_weeks: int = HISTORY_WEEKS) -> Path:
    """One panel per model (and the Average), citywide."""
    fc, obs, meta = tables["forecast"], tables["observed"], tables["meta"]
    models = list(dict.fromkeys(fc["model"]))
    city_obs = obs[obs["area"] == "Citywide"]
    ncols = 2 if len(models) == 4 else len(models)
    nrows = -(-len(models) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(5.2 * ncols, 3.4 * nrows), sharex=True,
                             sharey=True, squeeze=False)
    fig.patch.set_facecolor(SURFACE)
    for ax, model in zip(axes.flat, models):
        _panel(ax, city_obs, fc[(fc["area"] == "Citywide") & (fc["model"] == model)],
               history_weeks)
        ax.set_title(model, loc="left", fontsize=11, color=INK, fontweight="bold")
    for ax in list(axes.flat)[len(models):]:
        ax.set_visible(False)
    # Shared axis: size it to the widest range on any panel, not the last one drawn.
    city_fc = fc[fc["area"] == "Citywide"]
    top = max(city_fc["high95"].max(), city_obs.tail(history_weeks)["rate"].max())
    axes.flat[0].set_ylim(0, top * 1.05)
    _dates(fig)
    for ax in axes[:, 0]:
        ax.set_ylabel("Visits per 100,000", fontsize=9, color=INK)
    _header(fig, f"{meta.get('city') or 'Boston'} citywide flu forecast, from the week of "
                 f"{meta['origin']}",
            f"{meta['unit']}. Citywide = the average of the neighborhoods, each counting "
            "equally.", legend_inches=0.4)
    _legend(fig, loc="lower center", bbox_to_anchor=(0.5, 0.0))
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    return path


def plot_neighborhoods(tables: dict, path: Path, model: str = "GNN",
                       history_weeks: int = HISTORY_WEEKS) -> Path:
    """One small panel per neighborhood for one model."""
    fc, obs, meta = tables["forecast"], tables["observed"], tables["meta"]
    if model not in set(fc["model"]):
        raise ValueError(f"no {model!r} rows; choose from {sorted(set(fc['model']))}")
    areas = [a for a in dict.fromkeys(fc["area"]) if a != "Citywide"]
    ncols = 4
    nrows = -(-len(areas) // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(3.3 * ncols, 2.4 * nrows), sharex=True,
                             squeeze=False)
    fig.patch.set_facecolor(SURFACE)
    for ax, area in zip(axes.flat, areas):
        _panel(ax, obs[obs["area"] == area], fc[(fc["area"] == area) & (fc["model"] == model)],
               history_weeks)
        ax.set_title(textwrap.fill(area.replace("/", "/\u200b"), 44).replace("\u200b", ""),
                     loc="left", fontsize=9, color=INK)
    for ax in list(axes.flat)[len(areas):]:
        ax.set_visible(False)
    _dates(fig)
    _header(fig, f"{model} forecast by neighborhood, from the week of {meta['origin']}",
            f"{meta['unit']}. Each panel has its own scale.", legend_inches=0.4)
    _legend(fig, loc="lower center", bbox_to_anchor=(0.5, 0.0))
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return path
