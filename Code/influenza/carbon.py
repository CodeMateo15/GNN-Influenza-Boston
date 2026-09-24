"""codecarbon integration, in one place, for every model script.

Deliberately failure-tolerant: an emissions tracker must never be the reason a
model run dies. Power-measurement backends (RAPL on Linux, IPG on macOS) are
frequently unavailable or permission-gated, so every codecarbon interaction is
guarded and a failure downgrades to `enabled=False` rather than raising.
"""

from __future__ import annotations

import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from . import paths

# Kept as-is for Boston so the single appended emissions.csv stays continuous
# with every row logged before the second city existed.
PROJECT_PREFIX = "boston-flu"
CITY_PREFIX = {"boston": "boston-flu", "columbus": "columbus-flu"}

# Energy equivalences for the console report. Rough public averages, used only
# to make kWh legible -- not part of any result.
_KWH_PER_100KM_EV = 18.0
_KWH_PER_HOUR_TV = 0.1
_US_KWH_PER_CAPITA_YEAR = 12000.0


@dataclass
class EmissionsSummary:
    """What a tracked run cost. All fields are None when tracking is off."""

    run_name: str
    enabled: bool = False
    kg_co2: float | None = None
    kwh: float | None = None
    duration_s: float | None = None
    cpu_kwh: float | None = None
    gpu_kwh: float | None = None
    ram_kwh: float | None = None
    hardware: dict[str, str] = field(default_factory=dict)
    note: str | None = None

    def to_json(self) -> dict:
        return {
            "run_name": self.run_name,
            "enabled": self.enabled,
            "kg_co2": self.kg_co2,
            "kwh": self.kwh,
            "duration_s": self.duration_s,
            "cpu_kwh": self.cpu_kwh,
            "gpu_kwh": self.gpu_kwh,
            "ram_kwh": self.ram_kwh,
            "hardware": self.hardware,
            "note": self.note,
        }

    def format_report(self) -> str:
        if not self.enabled:
            return f"Emissions tracking off ({self.note or 'disabled'})."
        kwh = self.kwh or 0.0
        lines = [
            f"Energy: {kwh:.6f} kWh | Emissions: {(self.kg_co2 or 0.0) * 1000:.3f} g CO2eq"
            f" | Duration: {self.duration_s or 0.0:.1f}s",
            f"  equivalent to driving {kwh / _KWH_PER_100KM_EV * 100:.3f} km in an EV,"
            f" or {kwh / _KWH_PER_HOUR_TV:.2f} hours of television,"
            f" or {kwh / _US_KWH_PER_CAPITA_YEAR * 100:.5f}% of one US resident's annual electricity.",
        ]
        return "\n".join(lines)


@contextmanager
def track_emissions(
    run_name: str,
    *,
    enabled: bool = True,
    output_dir: Path | None = None,
) -> Iterator[EmissionsSummary]:
    """Measure energy and CO2 for the enclosed block.

    All runs append to a single results/_emissions/emissions.csv, continuous
    with the history the notebooks produced.
    """
    summary = EmissionsSummary(run_name=run_name)
    if not enabled:
        summary.note = "--no-carbon"
        yield summary
        return

    try:
        from codecarbon import OfflineEmissionsTracker
    except ImportError:
        summary.note = "codecarbon not installed"
        warnings.warn("codecarbon not installed; skipping emissions tracking.", stacklevel=2)
        yield summary
        return

    directory = output_dir or paths.EMISSIONS_DIR
    directory.mkdir(parents=True, exist_ok=True)

    tracker = None
    started = time.perf_counter()
    try:
        tracker = OfflineEmissionsTracker(
            country_iso_code="USA",
            log_level="error",
            project_name=f"{PROJECT_PREFIX}:{run_name}",
            output_dir=str(directory),
            output_file="emissions.csv",
        )
        tracker.start()
        summary.enabled = True
    except Exception as exc:  # pragma: no cover - hardware/permission dependent
        summary.note = f"tracker failed to start: {type(exc).__name__}: {exc}"
        warnings.warn(f"codecarbon could not start ({exc}); continuing untracked.", stacklevel=2)
        tracker = None

    try:
        yield summary
    finally:
        summary.duration_s = time.perf_counter() - started
        if tracker is not None:
            try:
                kg = tracker.stop()
                data = getattr(tracker, "final_emissions_data", None)
                summary.kg_co2 = float(kg) if kg is not None else None
                if data is not None:
                    summary.kwh = _maybe_float(getattr(data, "energy_consumed", None))
                    summary.cpu_kwh = _maybe_float(getattr(data, "cpu_energy", None))
                    summary.gpu_kwh = _maybe_float(getattr(data, "gpu_energy", None))
                    summary.ram_kwh = _maybe_float(getattr(data, "ram_energy", None))
                    summary.duration_s = _maybe_float(getattr(data, "duration", None)) or summary.duration_s
                    summary.hardware = {
                        "cpu_model": str(getattr(data, "cpu_model", "") or ""),
                        "gpu_model": str(getattr(data, "gpu_model", "") or ""),
                        "cpu_count": str(getattr(data, "cpu_count", "") or ""),
                        "os": str(getattr(data, "os", "") or ""),
                    }
            except Exception as exc:  # pragma: no cover
                summary.enabled = False
                summary.note = f"tracker failed to stop: {type(exc).__name__}: {exc}"


def _maybe_float(value) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None
