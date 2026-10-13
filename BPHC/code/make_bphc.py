"""Turn one archived live forecast into the BPHC tables and figures.

    python make_bphc.py --origin path/to/live/2026_27/boston/2026-10-11 --out path/to/BPHC

Inputs (all inside --origin, which `scripts/live_forecast.py` writes every week):
    forecast.csv            every model's forecast, 23 quantiles per row
    rates_asof.csv          the observed weekly rates the forecast started from
    meta.json               which backtest the trust check used
Optional:
    --backtest FILE         that backtest's predictions.csv (default: the path in
                            meta.json, if it exists). Without it, accuracy.csv keeps
                            only the live rows.
    sibling origin folders  earlier weeks' forecasts, scored against today's data.

Outputs (in --out):
    forecast_2week.csv      the forecast: one row per week ahead x area x model
    observed.csv            the observed rates, long format, with a Citywide row per week
    accuracy.csv            how close past forecasts came
    figures/citywide_forecast.png, figures/neighborhoods_forecast.png

From another program:
    import make_bphc
    tables = make_bphc.build("path/to/origin")       # dict of DataFrames
    make_bphc.write(tables, "out_dir")                # or use the frames directly

Needs only numpy, pandas and (for the figures) matplotlib.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --- vocabulary -------------------------------------------------------------------

# Package model name -> the name BPHC sees. Order is the order of every table.
MODELS = {"arima": "ARIMA", "lstm": "LSTM", "gnn_st": "GNN"}
AVERAGE = "Average"
REFERENCE = ("persistence", "Same as last week")
CITYWIDE = "Citywide"

# FluSight's 23 quantile levels, as written by the package.
LEVELS = (0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
          0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99)
QCOLS = [f"q{tau:.3f}" for tau in LEVELS]

# The quantiles each published column is read from.
BANDS = {"estimate": "q0.500", "low95": "q0.025", "low50": "q0.250",
         "high50": "q0.750", "high95": "q0.975"}

# The output contract. BPHC's pipeline may depend on these names and orders.
FORECAST_COLUMNS = ["origin_date", "target_date", "weeks_ahead", "area", "model",
                    "estimate", "low95", "low50", "high50", "high95"]
OBSERVED_COLUMNS = ["week", "area", "rate"]
ACCURACY_COLUMNS = ["source", "season", "weeks_ahead", "scope", "model", "n_forecasts",
                    "avg_error", "wis", "wis_vs_last_week", "in_95_range", "in_50_range"]

UNIT = "ILI emergency-department visits per 100,000 residents"


class InputError(ValueError):
    """A missing or malformed input. The command line prints it and exits with status 2."""


# --- building blocks ----------------------------------------------------------------

def _read(path: Path, **kwargs) -> pd.DataFrame:
    if not path.exists():
        raise InputError(f"missing input {path}")
    return pd.read_csv(path, **kwargs)


def read_forecast(path: Path) -> pd.DataFrame:
    """A forecast.csv as the package writes it (23 quantile columns per row)."""
    frame = _read(path, parse_dates=["origin_date", "target_date"], dtype={"area": str})
    missing = [c for c in QCOLS + ["model", "horizon", "area"] if c not in frame.columns]
    if missing:
        raise InputError(f"{path} lacks columns {missing}")
    return frame


def load_forecast(origin: Path) -> pd.DataFrame:
    return read_forecast(origin / "forecast.csv")


def load_observed(origin: Path) -> pd.DataFrame:
    """Weeks x areas of observed rates (blank = not reported)."""
    frame = _read(origin / "rates_asof.csv", index_col=0, parse_dates=True)
    frame.index.name = "week"
    return frame


def require_models(frame: pd.DataFrame, models: list[str], where: str) -> None:
    absent = [m for m in models if m not in set(frame["model"])]
    if absent:
        raise InputError(f"{where} has no {absent} rows (it has {sorted(set(frame['model']))}). "
                         "Rerun the live forecast with those models.")


def add_average(frame: pd.DataFrame, models: list[str], keys: list[str]) -> pd.DataFrame:
    """Append the equal-weight model average: each quantile is the mean of the models'.

    Averaging quantile by quantile (Vincent averaging) keeps every range nested.
    The average exists only where every model has a forecast.
    """
    part = frame[frame["model"].isin(models)]
    counts = part.groupby(keys)["model"].nunique()
    full = counts[counts == len(models)].index
    cols = QCOLS + (["actual"] if "actual" in part.columns else [])
    mean = part.groupby(keys)[cols].mean().loc[full].reset_index()
    if "actual" in cols:
        mean["actual"] = part.groupby(keys)["actual"].first().loc[full].to_numpy()
    return pd.concat([frame, mean.assign(model=AVERAGE)], ignore_index=True)


def add_citywide(frame: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Append a Citywide row per key: the plain mean over areas of every quantile.

    Every neighborhood counts equally (BPHC publishes no weekly population). When
    actuals are present, only areas observed that week enter both sides, so the
    citywide forecast and the citywide observation describe the same areas.
    """
    part = frame[frame["area"] != CITYWIDE]
    if "actual" in part.columns:
        part = part[np.isfinite(part["actual"])]
        cols = QCOLS + ["actual"]
    else:
        cols = QCOLS
    city = part.groupby(keys)[cols].mean().reset_index().assign(area=CITYWIDE)
    return pd.concat([frame, city], ignore_index=True)


def wis(actual: np.ndarray, quantiles: np.ndarray) -> np.ndarray:
    """Weighted interval score per row: 2 x the mean pinball loss over the 23
    quantiles. Same formula as areafluforecast.scoring.wis_from_quantiles."""
    diff = actual[:, None] - quantiles
    tau = np.asarray(LEVELS)[None, :]
    return 2.0 * np.maximum(tau * diff, (tau - 1.0) * diff).mean(axis=1)


def score(frame: pd.DataFrame) -> pd.DataFrame:
    """Per-forecast scores, using exactly what BPHC is shown: the median as the
    estimate and the 2.5-97.5 / 25-75 percentile ranges."""
    out = frame[np.isfinite(frame["actual"])].copy()
    y = out["actual"].to_numpy(float)
    out["abs_error"] = np.abs(out["q0.500"].to_numpy(float) - y)
    out["wis"] = wis(y, out[QCOLS].to_numpy(float))
    out["in95"] = (y >= out["q0.025"]) & (y <= out["q0.975"])
    out["in50"] = (y >= out["q0.250"]) & (y <= out["q0.750"])
    return out


def summarise(scored: pd.DataFrame, source: str, by_season: bool) -> pd.DataFrame:
    """One row per (season, weeks ahead, scope, model). WIS vs last week is the
    model's mean WIS over the persistence mean WIS on the same forecasts (< 1 is
    better than assuming next week looks like this week)."""
    scored = scored.assign(scope=np.where(scored["area"] == CITYWIDE, "citywide", "neighborhoods"))
    groups = [scored.assign(season="all")]
    if by_season:
        groups.append(scored)
    rows = []
    for frame in groups:
        cell = ["season", "horizon", "scope", "origin_date", "target_date", "area"]
        ref = frame[frame["model"] == REFERENCE[0]].set_index(cell)["wis"]
        for (season, h, scope, model), part in frame.groupby(["season", "horizon", "scope", "model"]):
            mine = part.set_index(cell)["wis"]
            common = mine.index.intersection(ref.index)
            ratio = (mine.loc[common].mean() / ref.loc[common].mean()
                     if len(common) and ref.loc[common].mean() > 0 else np.nan)
            rows.append({"source": source, "season": season, "weeks_ahead": int(h), "scope": scope,
                         "model": model, "n_forecasts": len(part),
                         "avg_error": part["abs_error"].mean(), "wis": part["wis"].mean(),
                         "wis_vs_last_week": ratio, "in_95_range": part["in95"].mean(),
                         "in_50_range": part["in50"].mean()})
    return pd.DataFrame(rows)


def _label(frame: pd.DataFrame) -> pd.DataFrame:
    names = {**MODELS, REFERENCE[0]: REFERENCE[1]}
    return frame.assign(model=frame["model"].map(lambda m: names.get(m, m)))


def _order(frame: pd.DataFrame, areas: list[str]) -> pd.DataFrame:
    models = list(MODELS.values()) + [AVERAGE, REFERENCE[1]]
    frame = frame.copy()
    frame["model"] = pd.Categorical(frame["model"], models, ordered=True)
    if "area" in frame.columns:
        frame["area"] = pd.Categorical(frame["area"], areas + [CITYWIDE], ordered=True)
    return frame


# --- the three tables ---------------------------------------------------------------------

def forecast_table(fc: pd.DataFrame, models: list[str], weeks: int, areas: list[str]) -> pd.DataFrame:
    keys = ["origin_date", "target_date", "horizon", "area"]
    part = fc[fc["model"].isin(models) & (fc["horizon"] <= weeks)][keys + ["model"] + QCOLS]
    part = add_average(part, models, keys)
    part = add_citywide(part, ["origin_date", "target_date", "horizon", "model"])
    part = _order(_label(part), areas)
    out = part.rename(columns={"horizon": "weeks_ahead", **{v: k for k, v in BANDS.items()}})
    out = out.sort_values(["weeks_ahead", "model", "area"])[FORECAST_COLUMNS]
    out["model"] = out["model"].astype(str)
    out["area"] = out["area"].astype(str)
    return out.reset_index(drop=True)


def observed_table(observed: pd.DataFrame) -> pd.DataFrame:
    wide = observed.assign(**{CITYWIDE: observed.mean(axis=1, skipna=True)})
    out = wide.rename_axis("week").reset_index().melt("week", var_name="area", value_name="rate")
    return out.dropna(subset=["rate"])[OBSERVED_COLUMNS].reset_index(drop=True)


def _with_actuals(fc: pd.DataFrame, observed: pd.DataFrame) -> pd.DataFrame:
    actual = (observed.stack().rename("actual").rename_axis(["target_date", "area"])
              .reset_index())
    return fc.drop(columns=["actual"], errors="ignore").merge(
        actual, on=["target_date", "area"], how="left")


def accuracy_table(origin: Path, backtest: Path | None, observed: pd.DataFrame,
                   models: list[str]) -> tuple[pd.DataFrame, list[str]]:
    """Backtest rows (past seasons, forecast as if live) plus live rows (this
    season's archived forecasts whose target weeks have now been observed)."""
    notes, parts = [], []
    keep = models + [REFERENCE[0]]
    keys = ["origin_date", "target_date", "horizon", "area"]
    if backtest is not None and backtest.exists():
        bt = pd.read_csv(backtest, parse_dates=["origin_date", "target_date"], dtype={"area": str})
        require_models(bt, keep, str(backtest))
        bt = bt[bt["model"].isin(keep)]
        bt = add_average(bt, models, keys + ["season"])
        bt = add_citywide(bt, ["season", "origin_date", "target_date", "horizon", "model"])
        parts.append(summarise(score(bt), "backtest", by_season=True))
    else:
        notes.append("No backtest predictions found, so accuracy.csv has no backtest rows "
                     "(pass --backtest).")

    live = []
    for folder in sorted(p for p in origin.parent.iterdir() if (p / "forecast.csv").exists()):
        frame = load_forecast(folder)
        if set(keep) <= set(frame["model"]):
            live.append(frame[frame["model"].isin(keep)])
    if live:
        lv = _with_actuals(pd.concat(live, ignore_index=True)[keys + ["model"] + QCOLS], observed)
        lv = lv[np.isfinite(lv["actual"])]
        if len(lv):
            lv = add_average(lv, models, keys)
            lv = add_citywide(lv, ["origin_date", "target_date", "horizon", "model"])
            parts.append(summarise(score(lv), "live", by_season=False))
    if not any(p["source"].eq("live").any() for p in parts):
        notes.append("No live forecast has reached its target week yet, so there are no live rows.")
    if not parts:
        return pd.DataFrame(columns=ACCURACY_COLUMNS), notes
    out = _order(_label(pd.concat(parts, ignore_index=True)), [])
    out = out.sort_values(["source", "season", "weeks_ahead", "scope", "model"])[ACCURACY_COLUMNS]
    out["model"] = out["model"].astype(str)
    return out.reset_index(drop=True), notes


# --- public API -------------------------------------------------------------------------

def build(origin: str | Path, *, backtest: str | Path | None = None,
          models: list[str] | None = None, weeks: int = 2,
          add_forecasts: list[str | Path] | None = None) -> dict:
    """All BPHC tables for one archived origin folder.

    Returns {"forecast": DataFrame, "observed": DataFrame, "accuracy": DataFrame,
    "meta": dict}. Raises InputError with a plain message when an input is
    missing or lacks a model.

    `add_forecasts` are extra forecast.csv-shaped files for models the archived
    forecast lacks (made later from the same data). They must share its origin
    week, and each one is named in meta["notes"].
    """
    origin = Path(origin)
    models = list(models or MODELS)
    meta_path = origin / "meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    fc = load_forecast(origin)
    notes = []
    for extra in add_forecasts or []:
        more = read_forecast(Path(extra))
        if set(more["origin_date"]) != set(fc["origin_date"]):
            raise InputError(f"{extra} starts from a different week than {origin}")
        clash = sorted(set(more["model"]) & set(fc["model"]))
        if clash:
            raise InputError(f"{extra} repeats models already in the forecast: {clash}")
        fc = pd.concat([fc, more], ignore_index=True)
        notes.append(f"{', '.join(MODELS.get(m, m) for m in sorted(set(more['model'])))} rows "
                     f"were added from {Path(extra).name}, made after the archived forecast "
                     "from the same data.")
    require_models(fc, models, str(origin / "forecast.csv"))
    observed = load_observed(origin)
    areas = list(observed.columns)
    if backtest is None and meta.get("backtest"):
        # meta.json stores the path relative to the package root, which is
        # four levels above an origin folder (<root>/live/<season>/<city>/<origin>).
        candidates = [Path(meta["backtest"]), origin.parents[3] / meta["backtest"]]
        backtest = next((p / "predictions.csv" for p in candidates
                         if (p / "predictions.csv").exists()), None)
    accuracy, acc_notes = accuracy_table(origin, Path(backtest) if backtest else None, observed,
                                         models)
    notes += acc_notes
    forecast = forecast_table(fc, models, weeks, areas)
    _check(forecast)
    return {"forecast": forecast, "observed": observed_table(observed), "accuracy": accuracy,
            "meta": {"origin": str(fc["origin_date"].max().date()), "city": meta.get("label", ""),
                     "unit": UNIT, "models": [MODELS.get(m, m) for m in models] + [AVERAGE],
                     "issued": meta.get("issued"), "notes": notes,
                     "backtest_seasons": meta.get("backtest_seasons")}}


def _check(forecast: pd.DataFrame) -> None:
    if list(forecast.columns) != FORECAST_COLUMNS:
        raise AssertionError(f"forecast columns drifted: {list(forecast.columns)}")
    values = forecast[["low95", "low50", "estimate", "high50", "high95"]].to_numpy(float)
    if not np.isfinite(values).all():
        raise AssertionError("forecast has missing values")
    if (np.diff(values, axis=1) < -1e-9).any():
        raise AssertionError("a forecast range is not nested around its estimate")


def write(tables: dict, out: str | Path, *, figures: bool = True,
          neighborhood_model: str = "GNN") -> list[Path]:
    """Write the tables (and figures) to `out`; returns the written paths."""
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for name, file in (("forecast", "forecast_2week.csv"), ("observed", "observed.csv"),
                       ("accuracy", "accuracy.csv")):
        path = out / file
        tables[name].to_csv(path, index=False, float_format="%.3f", date_format="%Y-%m-%d")
        written.append(path)
    path = out / "forecast_info.json"
    path.write_text(json.dumps(tables["meta"], indent=2) + "\n")
    written.append(path)
    if figures:
        from bphc_figures import plot_citywide, plot_neighborhoods
        (out / "figures").mkdir(exist_ok=True)
        written.append(plot_citywide(tables, out / "figures" / "citywide_forecast.png"))
        written.append(plot_neighborhoods(tables, out / "figures" / "neighborhoods_forecast.png",
                                          model=neighborhood_model))
    return written


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--origin", required=True, type=Path,
                        help="an archived forecast folder, e.g. live/2026_27/boston/2026-10-11")
    parser.add_argument("--out", required=True, type=Path, help="where to write the outputs")
    parser.add_argument("--backtest", type=Path, default=None,
                        help="backtest predictions.csv (default: the one meta.json names)")
    parser.add_argument("--weeks", type=int, default=2, help="weeks ahead to publish (default 2)")
    parser.add_argument("--models", nargs="+", default=list(MODELS), choices=list(MODELS),
                        help="models to publish and average (default: all three)")
    parser.add_argument("--neighborhood-model", default="GNN",
                        help="model drawn on the neighborhood figure (default GNN)")
    parser.add_argument("--add-forecast", nargs="+", type=Path, default=None, metavar="FILE",
                        help="extra forecast CSVs for models the archived forecast lacks")
    parser.add_argument("--no-figures", action="store_true", help="tables only (no matplotlib)")
    args = parser.parse_args(argv)
    try:
        tables = build(args.origin, backtest=args.backtest, models=args.models, weeks=args.weeks,
                       add_forecasts=args.add_forecast)
    except InputError as exc:
        print(f"make_bphc: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
    for path in write(tables, args.out, figures=not args.no_figures,
                      neighborhood_model=args.neighborhood_model):
        print(f"wrote {path}")
    for note in tables["meta"]["notes"]:
        print(f"note: {note}", file=sys.stderr)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
