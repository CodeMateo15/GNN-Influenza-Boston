"""Shared plotting. Matplotlib is configured headless so scripts work over ssh."""

from __future__ import annotations

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


def save_grid_plot(
    predictions: pd.DataFrame,
    path: Path,
    title: str,
    *,
    horizon: int = 1,
    bands: bool = False,
    shade_flu_season: bool = True,
) -> None:
    """4x4 grid of actual vs predicted, one panel per neighborhood."""
    data = predictions.loc[predictions["horizon"].eq(horizon)].copy()
    data["target_date"] = pd.to_datetime(data["target_date"])
    spans = _flu_season_spans(data["target_date"].unique()) if shade_flu_season else []
    show_bands = bands and {"lower", "upper"}.issubset(data.columns)

    fig, axes = plt.subplots(4, 4, figsize=(18, 14), sharex=True, sharey=True)
    for ax, neighborhood in zip(axes.flat, NEIGHBORHOODS):
        part = data.loc[data["neighborhood"].eq(neighborhood)].sort_values("target_date")
        for lo, hi in spans:
            ax.axvspan(lo, hi, color=SEASON_COLOUR, alpha=0.15, lw=0)
        if show_bands:
            ax.fill_between(part["target_date"], part["lower"], part["upper"],
                            color=PREDICTED_COLOUR, alpha=0.18, lw=0, label="95% PI")
        ax.plot(part["target_date"], part["actual"], color=ACTUAL_COLOUR, label="Actual")
        ax.plot(part["target_date"], part["predicted"], "--", color=PREDICTED_COLOUR,
                label="Predicted")
        ax.set_title(SHORT_NAMES[NEIGHBORHOODS.index(neighborhood)], fontsize=9)
        ax.tick_params(axis="x", rotation=35, labelsize=7)
    for ax in axes.flat[len(NEIGHBORHOODS):]:
        ax.axis("off")
    axes.flat[0].legend(fontsize=8)
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
