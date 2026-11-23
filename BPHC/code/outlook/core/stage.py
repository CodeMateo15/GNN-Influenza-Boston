# Generated copy of boston-flu-outlook/core/stage.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Turn one archived live forecast into the files the app reads (data/<city>/).

Shared by publish.py (the live site) and export_html.py (the offline copy, also
shipped in the BPHC folder), so both show exactly the same numbers. Reads the
frozen folder that areaFluForecast's scripts/live_forecast.py writes; never edits it.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pandas as pd

# Files every archived forecast folder has; the rest are optional.
REQUIRED = ("meta.json", "forecast.csv", "backtest_comparison.csv", "backtest_scores.csv",
            "trust.md", "rates_asof.csv")


class StageError(Exception):
    """A missing or mismatched input, in words a scheduler log can show."""


def with_coverage50(scores: pd.DataFrame, meta: dict, base: Path) -> pd.DataFrame:
    """Archives made before the package scored the 50% range lack `coverage50`.
    Recompute it from the saved backtest predictions (25th-75th percentile),
    so the frozen archive itself is never edited. `meta["backtest"]` is relative
    to the folder live_forecast.py ran in (`base`)."""
    if "coverage50" in scores:
        return scores
    predictions = base / meta.get("backtest", "") / "predictions.csv"
    if not predictions.exists():
        print(f"  no {predictions}: the 50% coverage will be missing")
        return scores
    p = pd.read_csv(predictions, usecols=["model", "season", "horizon", "actual", "q0.250", "q0.750"])
    p = p[p["actual"].notna()]
    p["covered50"] = (p["actual"] >= p["q0.250"]) & (p["actual"] <= p["q0.750"])
    cover = p.groupby(["model", "season", "horizon"])["covered50"].mean().rename("coverage50")
    return scores.merge(cover.reset_index(), on=["model", "season", "horizon"], how="left")


def stage(city: str, folder: Path, out: Path, *, edges: Path, geo: dict) -> dict:
    """Write one city's app files into `out` from an archived forecast folder
    (live/<season>/<city>/<week>/), with the neighborhood network `edges` (a CSV
    with columns a, b) and the ready-to-draw boundaries `geo` (publish.build_geo).
    Returns the meta written."""
    missing = [n for n in REQUIRED if not (folder / n).exists()]
    if missing:
        raise StageError(f"{folder} is not an archived forecast folder: missing {', '.join(missing)}")
    if not Path(edges).exists():
        raise StageError(f"No neighborhood network at {edges}")
    out.mkdir(parents=True, exist_ok=True)
    meta = json.loads((folder / "meta.json").read_text())
    for name in ("forecast.csv", "backtest_comparison.csv", "trust.md"):
        shutil.copy(folder / name, out / name)
    # live/<season>/<city>/<week> sits three levels below where live_forecast.py ran.
    up = Path(folder).resolve().parents
    base = up[3] if len(up) > 3 else Path(folder)
    with_coverage50(pd.read_csv(folder / "backtest_scores.csv"), meta, base).to_csv(
        out / "backtest_scores.csv", index=False)
    history = pd.read_csv(folder / "rates_asof.csv", index_col=0)
    history.index.name = "week"
    history.round(3).to_csv(out / "history.csv")
    scores = folder.parent / "scores.csv"
    if scores.exists():
        shutil.copy(scores, out / "live_scores.csv")
    elif (out / "live_scores.csv").exists():
        (out / "live_scores.csv").unlink()
    # What drove the graph model (live_forecast.py explain); only frozen-model
    # forecasts have it.
    if (folder / "drivers.csv").exists():
        shutil.copy(folder / "drivers.csv", out / "drivers.csv")
    elif (out / "drivers.csv").exists():
        (out / "drivers.csv").unlink()
    # How long each model took, for every archived origin that recorded it.
    timed = [pd.read_csv(p / "runtime.csv").assign(origin=p.name)
             for p in sorted(folder.parent.iterdir()) if (p / "runtime.csv").exists()]
    if timed:
        pd.concat(timed, ignore_index=True).to_csv(out / "runtimes.csv", index=False)
    elif (out / "runtimes.csv").exists():
        (out / "runtimes.csv").unlink()
    edges = pd.read_csv(edges, dtype=str)
    areas = list(history.columns)
    edges = edges[edges["a"].isin(areas) & edges["b"].isin(areas)]
    edges.to_csv(out / "edges.csv", index=False)
    missing = sorted(set(areas) - set(geo["areas"]))
    if missing:
        raise StageError(f"{city}: no boundary for {missing}")
    (out / "geo.json").write_text(json.dumps(geo, separators=(",", ":")))
    # Every archived origin, newest last, so the app can show how many weeks are on record.
    origins = sorted(p.name for p in folder.parent.iterdir() if (p / "meta.json").exists())
    meta["archived_origins"] = origins
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta
