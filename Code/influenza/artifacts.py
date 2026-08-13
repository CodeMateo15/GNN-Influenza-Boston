"""Writing a run's outputs. Every model script ends in one finish_run() call,
so all models produce the same artifact shape and compare_models.py needs no
per-model special cases.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd

from . import paths
from .carbon import EmissionsSummary
from .metrics import build_metrics, summary_table
from .plots import save_grid_plot

PREDICTION_SORT = ["horizon", "target_date", "neighborhood"]


def git_sha() -> str | None:
    """Short commit hash, so a result can be traced back to the code that made it."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=paths.ROOT, capture_output=True, text=True, timeout=5, check=True,
        )
        return out.stdout.strip() or None
    except Exception:
        return None


def run_dir(model: str, variant: str, results_root: Path | None = None) -> Path:
    directory = (results_root or paths.RESULTS_DIR) / model / variant
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def finish_run(
    *,
    model: str,
    variant: str,
    predictions: pd.DataFrame,
    config: dict,
    extras: bool = False,
    bands: bool = False,
    carbon: EmissionsSummary | None = None,
    extra_tables: dict[str, pd.DataFrame] | None = None,
    results_root: Path | None = None,
    title: str | None = None,
) -> Path:
    """Write predictions, metrics, config, emissions and the horizon-1 plot."""
    out = run_dir(model, variant, results_root)

    predictions = predictions.sort_values(PREDICTION_SORT).reset_index(drop=True)
    predictions.to_csv(out / "predictions.csv", index=False)

    metrics = build_metrics(predictions, model=model, variant=variant, extras=extras)
    metrics.to_csv(out / "metrics.csv", index=False)

    payload = {
        "model": model,
        "variant": variant,
        "git_sha": git_sha(),
        "created": pd.Timestamp.now().isoformat(timespec="seconds"),
        **config,
    }
    (out / "run_config.json").write_text(json.dumps(payload, indent=2, default=str) + "\n")

    if carbon is not None:
        (out / "emissions.json").write_text(json.dumps(carbon.to_json(), indent=2) + "\n")

    for name, table in (extra_tables or {}).items():
        table.to_csv(out / f"{name}.csv", index=False)

    save_grid_plot(
        predictions,
        out / "actual_vs_predicted_horizon1.png",
        title or f"{model} ({variant}) — horizon 1",
        bands=bands,
    )

    print("\nMetrics by segment and scope (horizon 1 and 2):")
    print(summary_table(metrics))
    if carbon is not None:
        print(carbon.format_report())
    print(f"Outputs: {out}")
    return out
