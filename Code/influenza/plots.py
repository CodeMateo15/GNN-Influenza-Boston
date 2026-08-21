"""Shared plotting. Matplotlib is configured headless so scripts work over ssh."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from .constants import FLU_MONTHS, NEIGHBORHOODS, SHORT_NAMES  # noqa: E402

ACTUAL_COLOUR = "#2c3e50"
PREDICTED_COLOUR = "#e74c3c"
SEASON_COLOUR = "#f1c40f"


def _flu_season_spans(dates: pd.DatetimeIndex) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """Contiguous runs of flu-season weeks, for axvspan shading."""
    dates = pd.DatetimeIndex(sorted(pd.to_datetime(dates)))
    in_season = np.isin(dates.month, list(FLU_MONTHS))
    spans: list[tuple[pd.Timestamp, pd.Timestamp]] = []
    start: pd.Timestamp | None = None
    for date, flag in zip(dates, in_season):
        if flag and start is None:
            start = date
        elif not flag and start is not None:
            spans.append((start, date))
            start = None
    if start is not None:
        spans.append((start, dates[-1]))
    return spans


# One style per severity boundary, matching plot_forecasts.py so the two figure
# families read the same way.
THRESHOLD_STYLES = [((0, (1, 3)), 0.8, 0.50), ((0, (4, 3)), 1.0, 0.65),
                    ((0, (7, 2)), 1.2, 0.80)]
THRESHOLD_INK = "#52514e"


@lru_cache(maxsize=1)
def _fixed_axes():
    """(shared y ceiling, shared thresholds), or (None, None) on any failure.

    Cached: replot_grids.py redraws 138 charts in one process, and reloading the
    BPHC series and refitting the thresholds for each one dominated the runtime.

    One ceiling and one threshold set for every panel, computed from the observed
    series rather than the predictions. That makes panels comparable both across
    neighborhoods and across models -- the same chart from two runs can be laid
    side by side. Imported lazily and guarded: a plot is not worth failing a
    completed training run over.
    """
    try:
        from .constants import TEST_END, TEST_START
        from .data import load_rates
        from .severity import (CITYWIDE, REFERENCE_SEASON_SETS, fit_thresholds,
                               shared_ceiling)

        rates = load_rates()
        fitted = fit_thresholds(rates, reference_seasons=REFERENCE_SEASON_SETS["post_covid"])
        thresholds = fitted[CITYWIDE]
        return shared_ceiling(rates, thresholds, window=(TEST_START, TEST_END)), thresholds
    except Exception as exc:  # pragma: no cover
        print(f"warning: falling back to autoscaled axes ({type(exc).__name__}: {exc})")
        return None, None


def save_grid_plot(
    predictions: pd.DataFrame,
    path: Path,
    title: str,
    *,
    horizon: int = 1,
    bands: bool = False,
    shade_flu_season: bool = True,
    fixed_axes: bool = True,
) -> None:
    """4x4 grid of actual vs predicted, one panel per neighborhood."""
    data = predictions.loc[predictions["horizon"].eq(horizon)].copy()
    data["target_date"] = pd.to_datetime(data["target_date"])
    spans = _flu_season_spans(data["target_date"].unique()) if shade_flu_season else []
    show_bands = bands and {"lower", "upper"}.issubset(data.columns)
    ceiling, thresholds = _fixed_axes() if fixed_axes else (None, None)
    entries = []
    if thresholds is not None:
        from .severity import band_entry_labels
        entries = band_entry_labels(thresholds)

    fig, axes = plt.subplots(4, 4, figsize=(18, 14), sharex=True, sharey=True)
    clipped: list[str] = []
    for ax, neighborhood in zip(axes.flat, NEIGHBORHOODS):
        part = data.loc[data["neighborhood"].eq(neighborhood)].sort_values("target_date")
        for lo, hi in spans:
            ax.axvspan(lo, hi, color=SEASON_COLOUR, alpha=0.15, lw=0)
        for index, (value, band) in enumerate(entries):
            dashes, width, alpha = THRESHOLD_STYLES[min(index, len(THRESHOLD_STYLES) - 1)]
            ax.axhline(value, color=THRESHOLD_INK, lw=width, ls=dashes, alpha=alpha,
                       zorder=2, label=f"{band} (≥{value:.0f})" if ax is axes.flat[0] else None)
        if show_bands:
            ax.fill_between(part["target_date"], part["lower"], part["upper"],
                            color=PREDICTED_COLOUR, alpha=0.18, lw=0, label="95% PI")
        ax.plot(part["target_date"], part["actual"], color=ACTUAL_COLOUR, label="Actual")
        ax.plot(part["target_date"], part["predicted"], "--", color=PREDICTED_COLOUR,
                label="Predicted")
        short = SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)]
        if ceiling:
            ax.set_ylim(0, ceiling)
            highest = float(np.nanmax(part["predicted"].to_numpy(dtype=float), initial=0.0))
            if highest > ceiling:
                clipped.append(short)
                ax.annotate("↑ clipped", xy=(0.98, 0.94), xycoords="axes fraction",
                            ha="right", fontsize=7, color="#898781")
        ax.set_title(short, fontsize=9)
        ax.tick_params(axis="x", rotation=35, labelsize=7)
    for ax in axes.flat[len(NEIGHBORHOODS):]:
        ax.axis("off")
    axes.flat[0].legend(fontsize=8, ncol=2)
    if clipped:
        fig.suptitle(f"{title}\nForecasts run off the top in: {', '.join(clipped)}",
                     fontsize=12, linespacing=1.6)
    else:
        fig.suptitle(title)
    fig.supxlabel("Target week")
    fig.supylabel("ILI ED visit rate per 100,000")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def save_loss_curve(train_losses, val_losses, path: Path, title: str = "Training") -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(1, len(train_losses) + 1), train_losses, label="Train")
    ax.plot(range(1, len(val_losses) + 1), val_losses, label="Validation")
    best = int(np.argmin(val_losses)) + 1
    ax.axvline(best, color="gray", ls=":", label=f"Best epoch ({best})")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE (normalized)")
    ax.set_title(title)
    ax.legend(fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
