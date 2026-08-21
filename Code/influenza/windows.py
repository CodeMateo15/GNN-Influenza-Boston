"""Experiment variants, sample origins and the train/val/test split.

The two baseline scripts had two copies of this logic that differed only in
whether they returned week timestamps (ARIMA) or integer positions (LSTM).
Integer positions are the primitive here because a position can always produce
its date, while a date cannot produce its position without a lookup -- and the
date form silently invents a target week when it steps across the COVID gap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd

from .constants import (
    COVID_END,
    COVID_START,
    HORIZONS,
    LOOKBACK,
    POST_COVID_START,
    TEST_END,
    TEST_START,
)

VARIANTS = ("exclude_covid", "post_covid", "full")


@dataclass(frozen=True)
class Window:
    """Sampling geometry and the evaluation window."""

    lookback: int = LOOKBACK
    horizons: tuple[int, ...] = HORIZONS
    test_start: pd.Timestamp = TEST_START
    test_end: pd.Timestamp = TEST_END
    val_fraction: float = 0.15

    @property
    def max_horizon(self) -> int:
        return max(self.horizons)

    @property
    def min_horizon(self) -> int:
        """The first target week a sample produces.

        Test membership and the split boundaries key off this rather than a
        hardcoded 1. Both shipped windows start at horizon 1, so this changes
        nothing today -- but a horizon-52-only run has no week t+1 target at
        all, and treating t+1 as one silently evaluates the wrong weeks.
        """
        return min(self.horizons)

    def to_json(self) -> dict:
        return {
            "lookback": self.lookback,
            "horizons": list(self.horizons),
            "test_start": str(self.test_start.date()),
            "test_end": str(self.test_end.date()),
            "val_fraction": self.val_fraction,
        }


@dataclass(frozen=True)
class VariantData:
    """The two views of a variant's data that downstream code needs.

    `available` drops excluded weeks entirely and its index defines every
    integer position used elsewhere. `calendar` keeps the original weekly grid
    with excluded weeks set to NaN, which ARIMA needs so that statsmodels sees
    true week spacing across a hole rather than a false contiguous series.
    """

    variant: str
    available: pd.DataFrame
    calendar: pd.DataFrame

    @property
    def index(self) -> pd.DatetimeIndex:
        return self.available.index


@dataclass(frozen=True)
class Split:
    """Train/validation/test origins as integer positions into `index`."""

    index: pd.DatetimeIndex
    train: list[int]
    val: list[int]
    test: list[int]
    window: Window

    def origin_dates(self, positions: list[int]) -> pd.DatetimeIndex:
        return self.index[positions]

    def target_dates(self, positions: list[int], horizon: int) -> pd.DatetimeIndex:
        return self.index[[p + horizon for p in positions]]

    def test_target_span(self) -> tuple[pd.Timestamp, pd.Timestamp]:
        """First and last target week actually scored, for the run banner."""
        return (self.index[self.test[0] + self.window.min_horizon],
                self.index[self.test[-1] + self.window.max_horizon])

    def to_json(self) -> dict:
        first_target, last_target = self.test_target_span()
        return {
            "n_train": len(self.train),
            "n_val": len(self.val),
            "n_test": len(self.test),
            "first_test_target": str(first_target.date()),
            "last_test_target": str(last_target.date()),
        }


def variant_data(rates: pd.DataFrame, variant: str) -> VariantData:
    """Slice the full weekly series down to one experiment variant."""
    if variant == "exclude_covid":
        in_covid = rates.index.to_series().between(COVID_START, COVID_END)
        calendar = rates.copy()
        calendar.loc[COVID_START:COVID_END] = np.nan
        available = rates.loc[~in_covid].copy()
    elif variant == "post_covid":
        available = rates.loc[rates.index >= POST_COVID_START].copy()
        calendar = available.copy()
    elif variant == "full":
        available = rates.copy()
        calendar = rates.copy()
    else:
        raise ValueError(f"Unknown variant: {variant!r}. Expected one of {VARIANTS}.")
    return VariantData(variant=variant, available=available, calendar=calendar)


def valid_origins(index: pd.DatetimeIndex, window: Window) -> list[int]:
    """Positions whose full lookback window and every horizon target are
    consecutive weeks, so no sample straddles a gap in the calendar."""
    max_h = window.max_horizon
    span_len = window.lookback + max_h
    week = np.timedelta64(7, "D")
    positions: list[int] = []
    for t in range(window.lookback, len(index) - max_h):
        span = index[t - window.lookback + 1 : t + max_h + 1]
        if len(span) == span_len and np.all(np.diff(span.values).astype("timedelta64[D]") == week):
            positions.append(t)
    return positions


def split_origins(index: pd.DatetimeIndex, origins: list[int], window: Window) -> Split:
    """Chronological split: test by target date, validation as the last slice of
    the remainder, and a purge so no training target leaks into a later split."""
    first = window.min_horizon
    test = [t for t in origins if window.test_start <= index[t + first] <= window.test_end]
    if not test:
        raise ValueError(
            f"No test origins: window {window.test_start.date()}..{window.test_end.date()} "
            f"does not overlap the data ({index.min().date()}..{index.max().date()})."
        )
    test_set = set(test)
    non_test = [t for t in origins if t not in test_set]
    n_val = max(1, int(window.val_fraction * len(non_test)))
    train, val = non_test[:-n_val], non_test[-n_val:]

    # Purge boundary samples whose furthest target overlaps the following split.
    val_target_start = index[val[0] + first]
    test_target_start = index[test[0] + first]
    train = [t for t in train if index[t + window.max_horizon] < val_target_start]
    val = [t for t in val if index[t + window.max_horizon] < test_target_start]
    if not train or not val:
        raise ValueError("The configured date ranges do not yield non-empty train/validation sets.")
    return Split(index=index, train=train, val=val, test=test, window=window)


def normalization(
    frame: pd.DataFrame,
    split: Split,
    *,
    mode: Literal["train", "all"] = "train",
) -> tuple[np.ndarray, np.ndarray]:
    """Per-column mean and standard deviation, shaped (1, n_columns).

    `mode='train'` uses only rows up to the last training target, which is the
    leakage-free choice. `mode='all'` uses the whole series and exists only to
    reproduce the notebooks, which normalized across the test window too.
    """
    if mode == "train":
        end = split.train[-1] + split.window.max_horizon + 1
        rows = frame.to_numpy(dtype=np.float32)[:end]
    elif mode == "all":
        rows = frame.to_numpy(dtype=np.float32)
    else:
        raise ValueError(f"Unknown normalization mode: {mode!r}")
    mean = np.nanmean(rows, axis=0, keepdims=True)
    std = np.nanstd(rows, axis=0, keepdims=True) + 1e-8
    return mean, std
