"""Is the forecast late, and how much does that cost?

`compare_models.py` ranks models on how close the number was. This one asks a
question those metrics add together and hide: **is the curve the right shape but
drawn in the wrong place on the calendar?**

Every model in this project tracks the season's rise and fall but arrives a week
or two behind it, and an annual RMSE charges that to "error" without saying that
the error is timing rather than height. At h=2 the shipped `gnn_st` forecast,
slid one week earlier with nothing retrained, drops its typical weekly miss from
17.2 to 10.6 per 100,000 -- so most of the error is misplacement.

Everything is read from the predictions.csv files already on disk, so no model
is re-run:

    python Code/compare_timing.py --results-dir Code/results/horizon_02
    python Code/compare_timing.py --results-dir Code/results/horizon_02 --variant post_covid
    python Code/compare_timing.py --delag            # the cross-horizon correction
    python Code/compare_timing.py --all-horizons     # one table per horizon tree

Outputs land in a `_comparison/` beside the results being read, so each horizon
keeps its own set.

A warning about the headline number, stated here because it is the easiest thing
in this file to misread: sliding a forecast one week earlier is **exactly
equivalent to relabelling an h-week forecast as an (h-1)-week forecast**. It buys
the accuracy with a week of lead time. `weeks_late` and `phase_share_of_mse` are
a measurement of what the lateness costs, and an upper bound on what any phase
correction could recover -- never a result in their own right.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit(f"Missing dependency: {exc.name}. Install pandas numpy.") from exc

from compare_models import _markdown_table, ablation_arms, horizon_roots
from influenza import paths
from influenza.cities import get as get_city
from influenza.cli import add_city_arg, city_results_dir

# How far ahead to look when asking "how many weeks late is this?". Four is
# enough to catch seasonal_naive's 52-week lag folding back onto the season, and
# short enough that every lead keeps most of the 49 test weeks.
MAX_LEAD = 4

# A week counts as "rising" or "falling" when the truth moved by more than this,
# in cases per 100,000. Below it the curve is flat and being late is invisible,
# which is why a single full-year coverage number hides the problem: the flat
# off-season is most of the year and the band covers it perfectly.
SLOPE_THRESHOLD = 5.0

REGIMES = ("rising", "flat", "falling")

# Ceiling on the fitted de-lag weight. gamma = 1 means "carry the model's own
# per-week slope forward one week", which is the parameter-free reading; 3 is
# already well past anything the measurements support.
MAX_DELAG_GAMMA = 3.0


# ---------------------------------------------------------------------------
# Reshaping
# ---------------------------------------------------------------------------

def weekly_grid(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """(week x neighborhood) table on a complete 7-day index.

    Reindexing onto a complete week grid matters and is not cosmetic. BPHC
    suppresses low-count neighborhood-weeks and those rows are dropped rather
    than imputed, so positions in the CSV are not weeks. Shifting by position
    would silently compare weeks that are three apart in a neighborhood with a
    gap -- which is exactly the error this script exists to measure.
    """
    table = frame.pivot_table(index="target_date", columns="neighborhood",
                              values=column, aggfunc="mean")
    weeks = pd.date_range(table.index.min(), table.index.max(), freq="7D")
    return table.reindex(weeks)


def shifted(table: pd.DataFrame, lead: int) -> pd.DataFrame:
    """`table` moved `lead` weeks earlier, re-indexed to line up with the truth."""
    if lead == 0:
        return table
    moved = table.iloc[lead:]
    moved.index = table.index[:len(moved)]
    return moved


def regime(truth: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Label each observed week rising / flat / falling by its own change."""
    change = truth.diff()
    labels = pd.DataFrame("flat", index=change.index, columns=change.columns)
    labels[change > threshold] = "rising"
    labels[change < -threshold] = "falling"
    return labels.where(change.notna())


# ---------------------------------------------------------------------------
# The four questions
# ---------------------------------------------------------------------------

def _rmse(truth: pd.DataFrame, forecast: pd.DataFrame) -> tuple[float, int]:
    error = (truth - forecast).to_numpy(dtype=float)
    observed = np.isfinite(error)
    if not observed.any():
        return float("nan"), 0
    return float(np.sqrt(np.mean(error[observed] ** 2))), int(observed.sum())


def _macro_corr(truth: pd.DataFrame, forecast: pd.DataFrame) -> float:
    """Mean of the per-neighborhood correlations, the metric METHODS.md quotes."""
    scores = [truth[node].corr(forecast[node]) for node in truth.columns
              if truth[node].notna().sum() >= 3]
    return float(np.nanmean(scores)) if scores else float("nan")


def lead_sweep(truth: pd.DataFrame, forecast: pd.DataFrame, max_lead: int) -> pd.DataFrame:
    """Score the forecast at every lead, so the best one can be read off.

    Answers: *if this forecast were relabelled as being about an earlier week,
    would it fit the truth better?*

    Every lead is scored on the **same** weeks -- the first `len - max_lead` of
    them -- because a bigger shift otherwise runs off the end of the series and
    scores fewer weeks than a smaller one. Crediting a shift with having dropped
    the last few weeks of the test window would overstate it, and those weeks are
    April/May, where the curve is flat and a shift is nearly free. So the RMSE
    column here is not the one in metrics.csv; `score_one` reports that
    separately over the full window.
    """
    window = truth.index[:len(truth.index) - max_lead]
    rows = []
    for lead in range(max_lead + 1):
        moved = shifted(forecast, lead).reindex(window)
        aligned = truth.reindex(window)
        rmse, n = _rmse(aligned, moved)
        rows.append({"lead_weeks": lead, "RMSE": rmse,
                     "Corr_macro": _macro_corr(aligned, moved), "n_obs": n})
    return pd.DataFrame(rows)


def lag_fingerprint(truth: pd.DataFrame, forecast: pd.DataFrame) -> float:
    """Correlation between the miss and how fast the truth was moving.

    Answers: *does the model miss in a way explained purely by the slope of the
    curve?* Near -1 is the signature of a pure phase shift -- low exactly when
    the epidemic is climbing, high exactly when it is falling. Near 0 means the
    misses are unrelated to timing.
    """
    change = truth.diff().to_numpy(dtype=float).ravel()
    residual = (forecast - truth).to_numpy(dtype=float).ravel()
    usable = np.isfinite(change) & np.isfinite(residual)
    if usable.sum() < 10:
        return float("nan")
    return float(np.corrcoef(change[usable], residual[usable])[0, 1])


def regime_bias(truth: pd.DataFrame, forecast: pd.DataFrame,
                labels: pd.DataFrame) -> dict[str, float]:
    """Mean over- or under-prediction on rising, flat and falling weeks.

    A late forecast is low on the way up and high on the way down by roughly the
    same amount, which is why its annual bias can be ~0 while every individual
    week is wrong.
    """
    residual = (forecast - truth)
    out = {}
    for name in REGIMES:
        values = residual.where(labels.eq(name)).to_numpy(dtype=float).ravel()
        values = values[np.isfinite(values)]
        out[f"bias_{name}"] = float(values.mean()) if values.size else float("nan")
        out[f"n_{name}"] = int(values.size)
    return out


def regime_coverage(frame: pd.DataFrame, labels: pd.DataFrame) -> dict[str, float]:
    """Does the 95% band cover the weeks when the curve is climbing?

    It should read 95% in all three regimes. When it reads 95% overall but much
    less on rising weeks, the band is not too narrow -- it is pointed at the
    wrong weeks, because its width is a function of the (late) predicted level.
    """
    if not {"lower", "upper"}.issubset(frame.columns):
        return {f"coverage_{name}": float("nan") for name in REGIMES} | {
            "coverage_all": float("nan"), "mean_width": float("nan")}

    inside = weekly_grid(frame.assign(
        _hit=((frame["actual"] >= frame["lower"]) & (frame["actual"] <= frame["upper"]))
        .astype(float).where(frame["actual"].notna())), "_hit")
    width = weekly_grid(frame.assign(_w=frame["upper"] - frame["lower"]), "_w")

    out: dict[str, float] = {}
    flat = inside.to_numpy(dtype=float).ravel()
    flat = flat[np.isfinite(flat)]
    out["coverage_all"] = float(100 * flat.mean()) if flat.size else float("nan")
    widths = width.to_numpy(dtype=float).ravel()
    out["mean_width"] = float(np.nanmean(widths)) if np.isfinite(widths).any() else float("nan")
    for name in REGIMES:
        values = inside.where(labels.reindex_like(inside).eq(name)).to_numpy(dtype=float).ravel()
        values = values[np.isfinite(values)]
        out[f"coverage_{name}"] = float(100 * values.mean()) if values.size else float("nan")
    return out


def peak_offsets(truth: pd.DataFrame, forecast: pd.DataFrame) -> pd.DataFrame:
    """Weeks between the forecast peak and the observed peak, per neighborhood.

    Positive is late. Uses the argmax of each series rather than a threshold
    crossing; `compare_severity.py` already reports the crossing version
    (`peak_week_error_weeks` in severity_timing.csv) and the two answer slightly
    different questions -- this one needs no threshold to be fitted first.
    """
    rows = []
    for node in truth.columns:
        observed, predicted = truth[node].dropna(), forecast[node].dropna()
        if observed.empty or predicted.empty:
            continue
        actual_week, forecast_week = observed.idxmax(), predicted.idxmax()
        rows.append({
            "neighborhood": node,
            "peak_week_actual": actual_week,
            "peak_week_pred": forecast_week,
            "peak_weeks_late": (forecast_week - actual_week).days / 7.0,
            "peak_actual": float(observed.max()),
            "peak_pred": float(predicted.max()),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# One model
# ---------------------------------------------------------------------------

def score_one(frame: pd.DataFrame, label: str, args: argparse.Namespace) -> tuple[dict, pd.DataFrame]:
    truth = weekly_grid(frame, "actual")
    forecast = weekly_grid(frame, "predicted")
    labels = regime(truth, args.slope_threshold)

    sweep = lead_sweep(truth, forecast, args.max_lead)
    at_zero = sweep.loc[sweep["lead_weeks"].eq(0)].iloc[0]
    # Chosen on RMSE, not on correlation. Correlation is scale-free, so it barely
    # distinguishes a one-week from a two-week shift on a series this smooth --
    # gnn_st at h=2 scores 0.906 and 0.911 -- while RMSE separates them clearly
    # (10.6 against 11.1) because it also charges for the flattening a wrong
    # shift introduces. RMSE is also the project's primary metric, and it gives
    # persistence the exactly-h answer it must have by construction.
    best = sweep.loc[sweep["RMSE"].idxmin()]
    phase_share = (1.0 - (best["RMSE"] ** 2) / (at_zero["RMSE"] ** 2)
                   if at_zero["RMSE"] > 0 else float("nan"))

    full_rmse, full_n = _rmse(truth, forecast)
    row = {
        "model": label,
        "weeks_late": int(best["lead_weeks"]),
        "RMSE": full_rmse,
        "RMSE_if_shifted": float(best["RMSE"]),
        "RMSE_common_window": float(at_zero["RMSE"]),
        "Corr_macro": _macro_corr(truth, forecast),
        "Corr_macro_if_shifted": float(best["Corr_macro"]),
        "phase_share_of_mse": float(phase_share),
        "lag_fingerprint": lag_fingerprint(truth, forecast),
        "n_obs": full_n,
        "n_obs_common_window": int(at_zero["n_obs"]),
    }
    row |= regime_bias(truth, forecast, labels)
    row |= regime_coverage(frame, labels)

    peaks = peak_offsets(truth, forecast)
    row["median_peak_weeks_late"] = (float(peaks["peak_weeks_late"].median())
                                     if not peaks.empty else float("nan"))
    peaks.insert(0, "model", label)
    return row, peaks


# ---------------------------------------------------------------------------
# The cross-horizon de-lag
# ---------------------------------------------------------------------------

def delag(frame: pd.DataFrame, shorter: pd.DataFrame, gap: int,
          gamma: float) -> pd.DataFrame:
    """Push the forecast earlier using the model's own slope across horizons.

    At origin `t` both the h-week and the shorter-horizon model have run, so

        slope_per_week = (p_h(t+h) - p_s(t+s)) / (h - s)

    is the model's own estimate of one week of movement, assembled entirely from
    forecasts made at origin `t`. No look-ahead: nothing here reads a week after
    the origin. And far less noisy than the observed week-over-week difference,
    which is mostly Poisson noise and suppression and which made accuracy worse
    at every weight when added to the forecast directly.

    `prediction + gamma * slope_per_week` then extrapolates that slope forward,
    which advances the phase. Gamma must be fitted on validation, never on the
    weeks being reported -- `--delag-gamma` is a knob, not a fitted value.
    """
    joined = frame.merge(
        shorter[["origin_date", "neighborhood", "predicted"]],
        on=["origin_date", "neighborhood"], suffixes=("", "_shorter"), how="inner")
    if joined.empty:
        raise SystemExit("error: --delag found no shared origins between the two horizons.")
    slope = (joined["predicted"] - joined["predicted_shorter"]) / max(gap, 1)
    joined["predicted"] = np.maximum(joined["predicted"] + gamma * slope, 0.0)
    if {"lower", "upper"}.issubset(joined.columns):
        joined["lower"] = np.maximum(joined["lower"] + gamma * slope, 0.0)
        joined["upper"] = np.maximum(joined["upper"] + gamma * slope, 0.0)
    return joined


def sibling_root(results_root: Path, horizon: int) -> Path | None:
    """The tree beside `results_root` holding the same runs at `horizon`.

    Two layouts exist and both are load-bearing: the headline trees are
    `results/horizon_02/`, while run_ablation.py and sweep.py write
    `results/_ablation/<study>/h02_s10/`. Matching only the first meant the
    de-lag silently skipped every ablation study.
    """
    name = results_root.name
    for pattern in (f"horizon_{horizon:02d}",
                    re.sub(r"^h\d{2}", f"h{horizon:02d}", name) if name.startswith("h") else None):
        if pattern and (results_root.parent / pattern).is_dir():
            return results_root.parent / pattern
    return None


def validation_frames(results_root: Path, model: str, variant: str,
                      shorter_h: int) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """This run's validation forecasts and the shorter horizon's, if both exist."""
    sibling = sibling_root(results_root, shorter_h)
    here = results_root / model / variant / "predictions_val.csv"
    there = None if sibling is None else sibling / model / variant / "predictions_val.csv"
    if not here.exists() or there is None or not there.exists():
        return None
    return (pd.read_csv(here, parse_dates=["origin_date", "target_date"]),
            pd.read_csv(there, parse_dates=["origin_date", "target_date"]))


def fit_delag_gamma(frame: pd.DataFrame, shorter: pd.DataFrame, gap: int) -> float:
    """Least-squares gamma for the de-lag, on VALIDATION forecasts.

    Minimising `sum((actual - (p_h + g * slope))^2)` over g has a closed form,

        g* = sum(slope * (actual - p_h)) / sum(slope^2),

    which is just the regression of the forecast's remaining error on its own
    cross-horizon slope. If the model is late, its error is positively related to
    the direction it is already moving, and g* comes out positive.

    Fitted on the validation split and applied unchanged to test, the same
    boundary the interval parameters respect. Fitting it on the test weeks --
    which is all that was possible before run_gnn.py wrote predictions_val.csv --
    would be a look-ahead dressed up as a result.
    """
    joined = frame.merge(
        shorter[["origin_date", "neighborhood", "predicted"]],
        on=["origin_date", "neighborhood"], suffixes=("", "_shorter"), how="inner")
    joined = joined.dropna(subset=["actual", "predicted", "predicted_shorter"])
    if len(joined) < 30:
        return 0.0
    slope = ((joined["predicted"] - joined["predicted_shorter"]) / max(gap, 1)).to_numpy()
    residual = (joined["actual"] - joined["predicted"]).to_numpy()
    denominator = float((slope ** 2).sum())
    if denominator <= 1e-9:
        return 0.0
    gamma = float((slope * residual).sum() / denominator)
    # Clamped rather than trusted. A validation split of a few hundred cells can
    # produce a large gamma off a handful of steep weeks, and the correction is
    # linear in it, so an unbounded fit is a way to turn noise into a forecast.
    return float(np.clip(gamma, 0.0, MAX_DELAG_GAMMA))


def shorter_horizon_frame(results_root: Path, model: str, variant: str,
                          horizon: int) -> tuple[pd.DataFrame, int] | None:
    """The nearest shorter-horizon predictions for the same model, and its horizon.

    Nearest rather than exactly h-1, because the project trains 1, 2 and 4 and
    there is no horizon_03 for h=4 to lean on. The gap is returned so the caller
    can put the slope on a per-week footing.
    """
    for shorter in range(horizon - 1, 0, -1):
        root = sibling_root(results_root, shorter)
        if root is None:
            continue
        path = root / model / variant / "predictions.csv"
        if path.exists():
            return (pd.read_csv(path, parse_dates=["origin_date", "target_date"]), shorter)
    return None


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

HEADLINE = {
    "model": "model",
    "weeks_late": "weeks late",
    "phase_share_of_mse": "share of error that is timing",
    "lag_fingerprint": "miss vs. slope",
    "RMSE": "typical weekly miss",
    "RMSE_common_window": "...on the compared weeks",
    "RMSE_if_shifted": "...once shifted earlier",
    "Corr_macro": "in step with truth",
    "median_peak_weeks_late": "peak weeks late",
}
COVERAGE = {
    "model": "model",
    "coverage_all": "all weeks",
    "coverage_rising": "rising",
    "coverage_flat": "flat",
    "coverage_falling": "falling",
    "mean_width": "mean band width",
}
BIAS = {
    "model": "model",
    "bias_rising": "rising weeks",
    "bias_flat": "flat weeks",
    "bias_falling": "falling weeks",
}


def _view(table: pd.DataFrame, columns: dict[str, str]) -> pd.DataFrame:
    present = {k: v for k, v in columns.items() if k in table.columns}
    return table[list(present)].rename(columns=present)


def leaderboard_markdown(table: pd.DataFrame, peaks: pd.DataFrame,
                         args: argparse.Namespace, horizon: int) -> str:
    cells = int(table["n_obs"].max()) if not table["n_obs"].empty else 0
    lines = [
        f"# Forecast timing at {horizon} week{'s' if horizon != 1 else ''} ahead",
        "",
        f"`variant={args.variant or 'all'}`, {cells} neighborhood-weeks scored. "
        f"A week counts as rising or falling when the truth moved more than "
        f"{args.slope_threshold:g} per 100,000.",
        "",
        "## Is the curve in the right place on the calendar?",
        "",
        "- **weeks late** — slide the forecast this many weeks earlier and it fits",
        "  the truth best. 0 is on time.",
        "- **share of error that is timing** — how much of the squared error goes away",
        "  under that shift. High means the shape and height are right and only the",
        "  placement is wrong.",
        "- **miss vs. slope** — correlation between the miss and how fast the truth was",
        "  moving. Near −1 is a pure phase shift; near 0 means the misses have nothing",
        "  to do with timing.",
        "- **typical weekly miss** — RMSE over the whole test window, in cases per",
        "  100,000; the same number metrics.csv reports.",
        "- **...on the compared weeks / ...once shifted earlier** — RMSE before and after",
        f"  the shift, both over the weeks every lead up to {args.max_lead} can score, so the",
        "  shift gets no credit for running off the end of the window.",
        "- **in step with truth** — mean of the 14 per-neighborhood correlations.",
        "",
        "Scopes follow the leaderboard convention in `compare_models.py`: RMSE is pooled",
        "over all neighborhood-weeks, correlation is the unweighted mean of the 14. Both",
        "reproduce `metrics.csv` exactly at lead 0, which is the check that this script",
        "is reading the same predictions the leaderboard is.",
        "",
    ]
    lines += _markdown_table(_view(table, HEADLINE))
    lines += [
        "",
        "> Sliding a forecast one week earlier is the same thing as relabelling an",
        f"> h={horizon} forecast as h={horizon - 1}: it buys the accuracy with a week of",
        "> lead time. These columns measure what the lateness costs and bound what any",
        "> phase correction could recover. They are not a result.",
        "",
        "## Does the 95% band cover the weeks when the curve is climbing?",
        "",
        "Every column should read 95%. A model at 95% overall but well below it on",
        "rising weeks has a band that is not too narrow but pointed at the wrong weeks —",
        "its width is a function of the predicted level, so a late centre drags a late",
        "band with it. Width is in cases per 100,000, so it is the cost of any fix.",
        "",
    ]
    lines += _markdown_table(_view(table, COVERAGE))
    lines += [
        "",
        "## Which way does the model miss when the curve is moving?",
        "",
        "Mean over-prediction, in cases per 100,000; negative is under-prediction. A",
        "late forecast is low on the way up and high on the way down by roughly the",
        "same amount, which is how its annual bias can sit near zero while almost",
        "every individual week is wrong.",
        "",
    ]
    lines += _markdown_table(_view(table, BIAS))

    if not peaks.empty:
        worst = peaks.sort_values("peak_actual", ascending=False).head(14)
        lines += [
            "",
            "## Peak week, busiest neighborhoods first",
            "",
            "Positive is late. `compare_severity.py` reports the threshold-crossing",
            "version of this (`peak_week_error_weeks`); this one needs no fitted",
            "threshold.",
            "",
        ]
        view = worst[["model", "neighborhood", "peak_week_actual", "peak_week_pred",
                      "peak_weeks_late", "peak_actual", "peak_pred"]].copy()
        for column in ("peak_week_actual", "peak_week_pred"):
            view[column] = pd.to_datetime(view[column]).dt.date.astype(str)
        lines += _markdown_table(view)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def discover_runs(results_root: Path, *, include_ablation_arms: bool) -> list[tuple[str, str]]:
    skip = frozenset() if include_ablation_arms else ablation_arms()
    found = []
    for path in sorted(results_root.glob("*/*/predictions.csv")):
        relative = path.relative_to(results_root)
        if any(part.startswith("_") for part in relative.parts):
            continue
        if relative.parts[0] in skip:
            continue
        found.append((relative.parts[0], relative.parts[1]))
    return found


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None)
    parser.add_argument("--variant", default=None,
                        help="Score only this variant. Default: every one found.")
    parser.add_argument("--models", default=None, help="Comma-separated subset.")
    parser.add_argument("--include-ablation-arms", action="store_true",
                        help="Score gnn_st_* ablation arms too, not just the leaderboard.")
    parser.add_argument("--max-lead", type=int, default=MAX_LEAD,
                        help=f"How many weeks of shift to try. Default {MAX_LEAD}.")
    parser.add_argument("--slope-threshold", type=float, default=SLOPE_THRESHOLD,
                        help="Weekly change, per 100,000, above which a week counts as "
                             f"rising or falling. Default {SLOPE_THRESHOLD:g}.")
    parser.add_argument("--delag", action="store_true",
                        help="Also score the cross-horizon slope correction, using the "
                             "next-shorter horizon tree. Requires that tree to exist.")
    parser.add_argument("--delag-gamma", type=float, default=None,
                        help="Weight on the cross-horizon slope. Default: fitted by least "
                             "squares on the validation split, which is what "
                             "predictions_val.csv exists for. Setting it here overrides "
                             "that -- useful for a sensitivity check, but a value chosen "
                             "by looking at the test weeks is not a result.")
    parser.add_argument("--all-horizons", action="store_true",
                        help="Run once per horizon_* tree beneath --results-dir.")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Default: a _comparison/ beside the results being read.")
    return parser.parse_args()


def run_tree(results_root: Path, args: argparse.Namespace) -> None:
    runs = discover_runs(results_root, include_ablation_arms=args.include_ablation_arms)
    if args.models:
        wanted = {m.strip() for m in args.models.split(",")}
        runs = [(m, v) for m, v in runs if m in wanted]
    if args.variant:
        runs = [(m, v) for m, v in runs if v == args.variant]
    if not runs:
        nested = horizon_roots(results_root)
        if nested:
            listed = "\n".join(f"  python Code/compare_timing.py --results-dir {p}"
                               for p in nested)
            raise SystemExit(f"error: no runs directly under {results_root} — results "
                             f"are split by forecast horizon. Pick one:\n{listed}\n\n"
                             f"Or pass --all-horizons.")
        raise SystemExit(f"error: no predictions.csv under {results_root}")

    rows, peak_frames, horizons = [], [], set()
    for model, variant in runs:
        frame = pd.read_csv(results_root / model / variant / "predictions.csv",
                            parse_dates=["origin_date", "target_date"])
        horizons |= set(frame["horizon"].unique())
        label = model if len(set(v for _, v in runs)) == 1 else f"{model} ({variant})"
        row, peaks = score_one(frame, label, args)
        rows.append(row)
        peak_frames.append(peaks)

        if args.delag:
            horizon = int(frame["horizon"].iloc[0])
            if horizon < 2:
                continue
            found = shorter_horizon_frame(results_root, model, variant, horizon)
            if found is None:
                print(f"note: --delag skipped {model}: no shorter-horizon tree beside "
                      f"{results_root}.", file=sys.stderr)
                continue
            shorter, shorter_h = found
            gap = horizon - shorter_h
            gamma, source = args.delag_gamma, "set on the command line"
            if gamma is None:
                val = validation_frames(results_root, model, variant, shorter_h)
                if val is None:
                    print(f"note: --delag skipped {model}: no predictions_val.csv, so "
                          f"gamma cannot be fitted. Re-run the model, or pass "
                          f"--delag-gamma to set it explicitly.", file=sys.stderr)
                    continue
                gamma = fit_delag_gamma(val[0], val[1], gap)
                source = f"fitted on {len(val[0])} validation rows"
            corrected = delag(frame, shorter, gap, gamma)
            row, peaks = score_one(corrected, f"{label} + de-lag", args)
            row["delag_gamma"] = round(gamma, 4)
            print(f"  {label}: de-lag gamma = {gamma:.3f} ({source})")
            rows.append(row)
            peak_frames.append(peaks)

    if len(horizons) != 1:
        raise SystemExit(f"error: results mix horizons {sorted(horizons)}; "
                         f"point --results-dir at one horizon tree.")
    horizon = int(horizons.pop())

    table = pd.DataFrame(rows).sort_values(
        ["weeks_late", "RMSE"], ascending=[True, True]).reset_index(drop=True)
    peaks = pd.concat(peak_frames, ignore_index=True) if peak_frames else pd.DataFrame()

    out = (args.out_dir or paths.comparison_dir(results_root)).resolve()
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "timing_long.csv", index=False)
    if not peaks.empty:
        peaks.to_csv(out / "timing_peaks.csv", index=False)
    (out / "timing_leaderboard.md").write_text(
        leaderboard_markdown(table, peaks, args, horizon))

    print(f"\nForecast timing at horizon {horizon}, {len(table)} arms:\n")
    print(_view(table, HEADLINE).to_string(index=False,
                                           float_format=lambda v: f"{v:.3f}"))
    print("\nDoes the 95% band cover the weeks when the curve is climbing?\n")
    print(_view(table, COVERAGE).to_string(index=False,
                                           float_format=lambda v: f"{v:.1f}"))
    print(f"\nOutputs: {paths.display(out)}")


def main() -> None:
    args = parse_args()
    city = get_city(args.city)  # validates the name and fails early on a typo
    args.results_dir = city_results_dir(args, city)
    results_root = args.results_dir.resolve()
    trees = horizon_roots(results_root) if args.all_horizons else [results_root]
    for tree in trees:
        if len(trees) > 1:
            print(f"\n{'=' * 72}\n{tree}\n{'=' * 72}")
        run_tree(tree, args)


if __name__ == "__main__":
    main()
