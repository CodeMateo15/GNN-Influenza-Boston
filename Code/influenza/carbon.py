"""codecarbon integration and run timing, in one place, for every model script.

Deliberately failure-tolerant: an emissions tracker must never be the reason a
model run dies. Power-measurement backends (RAPL on Linux, powermetrics on
macOS) are frequently unavailable or permission-gated, so every codecarbon
interaction is guarded and a failure downgrades to `enabled=False` rather than
raising. Wall-clock time and per-phase time are recorded either way, including
under --no-carbon.

Reference for every field and caveat: Code/docs/COMPUTE.md.
"""

from __future__ import annotations

import math
import os
import sys
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
CITY_PREFIX = {
    "boston": "boston-flu",
    "columbus": "columbus-flu",
    "chicago": "chicago-flu",
    "buenos_aires": "buenos-aires-flu",
}

# Grid carbon intensity: the Mac (Boston) and Explorer (MGHPCC, Holyoke) both
# draw from the Massachusetts grid. Rows logged before 2026-10-13 used the US
# national average -- see COMPUTE.md, "Grid region".
DEFAULT_REGION = "massachusetts"

# Energy equivalences for the receipt. Rough public figures, used only to make
# kWh legible -- not part of any result. Derivations in COMPUTE.md.
_KWH_PER_100KM_EV = 18.0
_KWH_PER_PHONE_CHARGE = 0.015
_KWH_PER_CUP_OF_TEA = 0.027

# Set when the influenza package is first imported -- i.e. near process start for
# every entrypoint -- and moved to the end of each tracked block, so the receipt
# can show the data loading / graph building that happens before a block opens
# (per variant, when one process runs several). Setup is timed, not metered.
_SETUP_MARK = time.perf_counter()

# codecarbon CPU modes -> how the power figure was obtained.
_MEASURED_MODES = {"intel_rapl", "intel_power_gadget", "apple_powermetrics"}


@dataclass
class EmissionsSummary:
    """What a run cost. Energy fields are None when tracking is off; time never is."""

    run_name: str
    city: str | None = None
    enabled: bool = False
    kg_co2: float | None = None
    kwh: float | None = None
    duration_s: float | None = None
    setup_s: float | None = None
    cpu_kwh: float | None = None
    gpu_kwh: float | None = None
    ram_kwh: float | None = None
    hardware: dict[str, str] = field(default_factory=dict)
    phases: dict[str, float] = field(default_factory=dict)
    epochs: int | None = None
    region: str | None = None
    tracking_mode: str | None = None
    measured: str | None = None
    emissions_file: str | None = None
    slurm_job: str | None = None
    codecarbon_version: str | None = None
    cpu_share_correction: float | None = None
    raw_kwh: float | None = None
    raw_kg_co2: float | None = None
    git_sha: str | None = None
    note: str | None = None

    @contextmanager
    def phase(self, name: str) -> Iterator[None]:
        """Time a named block (data / train / eval). Re-entering a name adds to it."""
        started = time.perf_counter()
        try:
            yield
        finally:
            self.phases[name] = self.phases.get(name, 0.0) + time.perf_counter() - started

    def add_epochs(self, n: int) -> None:
        """Count trained epochs (summed across seeds) for the seconds-per-epoch figure."""
        self.epochs = (self.epochs or 0) + int(n)

    @property
    def wall_s(self) -> float | None:
        """Whole-process time: untracked setup plus the tracked block."""
        if self.duration_s is None:
            return None
        return (self.setup_s or 0.0) + self.duration_s

    @property
    def seconds_per_epoch(self) -> float | None:
        if not self.epochs:
            return None
        return (self.phases.get("train") or self.duration_s or 0.0) / self.epochs

    def phase_kwh(self, name: str) -> float | None:
        """A phase's energy, estimated by its share of wall-clock time."""
        if self.kwh is None or not self.duration_s or name not in self.phases:
            return None
        return self.kwh * self.phases[name] / self.duration_s

    def to_json(self) -> dict:
        return {
            "run_name": self.run_name,
            "city": self.city,
            "enabled": self.enabled,
            "kg_co2": self.kg_co2,
            "kwh": self.kwh,
            "duration_s": self.duration_s,
            "setup_s": self.setup_s,
            "wall_s": self.wall_s,
            "cpu_kwh": self.cpu_kwh,
            "gpu_kwh": self.gpu_kwh,
            "ram_kwh": self.ram_kwh,
            "phases": {k: round(v, 3) for k, v in self.phases.items()},
            "epochs": self.epochs,
            "seconds_per_epoch": self.seconds_per_epoch,
            "region": self.region,
            "tracking_mode": self.tracking_mode,
            "measured": self.measured,
            "hardware": self.hardware,
            "emissions_file": self.emissions_file,
            "slurm_job": self.slurm_job,
            "codecarbon_version": self.codecarbon_version,
            "cpu_share_correction": self.cpu_share_correction,
            "raw_kwh": self.raw_kwh,
            "raw_kg_co2": self.raw_kg_co2,
            "git_sha": self.git_sha,
            "note": self.note,
        }

    def format_report(self, previous: dict | None = None) -> str:
        """The end-of-run receipt. `previous` is the last emissions.json for this run dir."""
        return _receipt(self, previous)


@contextmanager
def track_emissions(
    run_name: str,
    *,
    enabled: bool = True,
    output_dir: Path | None = None,
    city: str | None = None,
) -> Iterator[EmissionsSummary]:
    """Time the enclosed block and, unless disabled, measure its energy and CO2.

    Serial runs append to results/_emissions/emissions.csv, continuous with the
    history the notebooks produced. Inside a SLURM array task (or when
    GNNFLU_EMISSIONS_FILE is set) rows go to a per-task file instead, so
    concurrent tasks never share a writer.
    """
    global _SETUP_MARK
    summary = EmissionsSummary(run_name=run_name, city=city)
    summary.slurm_job = _slurm_job()
    started = time.perf_counter()
    summary.setup_s = started - _SETUP_MARK

    tracker = None
    if not enabled:
        summary.note = "--no-carbon"
    else:
        tracker = _start_tracker(summary, run_name, city, output_dir)

    try:
        yield summary
    finally:
        summary.duration_s = time.perf_counter() - started
        if tracker is not None:
            _stop_tracker(tracker, summary)
        _SETUP_MARK = time.perf_counter()


def _start_tracker(summary: EmissionsSummary, run_name: str, city: str | None,
                   output_dir: Path | None):
    try:
        import codecarbon
        from codecarbon import OfflineEmissionsTracker
    except ImportError:
        summary.note = "codecarbon not installed"
        warnings.warn("codecarbon not installed; skipping emissions tracking.", stacklevel=3)
        return None

    target = _emissions_target(output_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    summary.region = os.environ.get("GNNFLU_GRID_REGION", DEFAULT_REGION) or None
    summary.emissions_file = str(target)
    summary.codecarbon_version = getattr(codecarbon, "__version__", None)
    summary.tracking_mode = _tracking_mode()
    prefix = CITY_PREFIX.get(city or "boston", f"{city}-flu")
    try:
        tracker = OfflineEmissionsTracker(
            country_iso_code="USA",
            region=summary.region,
            tracking_mode=summary.tracking_mode,
            log_level="error",
            project_name=f"{prefix}:{run_name}",
            output_dir=str(target.parent),
            output_file=target.name,
        )
        tracker.start()
        summary.enabled = True
        summary.measured = _measurement_mode(tracker)
        return tracker
    except Exception as exc:  # pragma: no cover - hardware/permission dependent
        summary.note = f"tracker failed to start: {type(exc).__name__}: {exc}"
        warnings.warn(f"codecarbon could not start ({exc}); continuing untracked.", stacklevel=3)
        return None


def _stop_tracker(tracker, summary: EmissionsSummary) -> None:
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
            _correct_slurm_cpu_share(summary)
    except Exception as exc:  # pragma: no cover
        summary.enabled = False
        summary.note = f"tracker failed to stop: {type(exc).__name__}: {exc}"


def slurm_cpu_share(allocated: int, node_cores: int) -> float:
    """Fraction of the node's rated CPU power one SLURM allocation can draw."""
    if allocated <= 0 or node_cores <= 0:
        return 1.0
    return min(1.0, allocated / node_cores)


def _correct_slurm_cpu_share(summary: EmissionsSummary) -> None:
    """Undo codecarbon 3.2.5's whole-node billing of a one-core SLURM process.

    In process mode with a load-based estimate, codecarbon divides the
    process's CPU load by the SLURM allocation (NumCPUs, e.g. 1) but multiplies
    by the TDP of the whole node (both sockets). One busy core is then billed as
    the entire node -- ~240 W on Explorer's E5-2680 v4 nodes instead of ~9 W.
    Scale CPU energy by allocated cores / node physical cores. The uncorrected
    values are kept in raw_kwh / raw_kg_co2, and the per-task CSV row (this
    process is its only writer) is patched to match.
    """
    if not (os.environ.get("SLURM_JOB_ID") and summary.tracking_mode == "process"
            and summary.measured and summary.measured.startswith("estimated (cpu load")
            and summary.cpu_kwh is not None and summary.kwh):
        return
    try:
        import psutil
        node_cores = psutil.cpu_count(logical=False) or os.cpu_count() or 0
        allocated = int(float(summary.hardware.get("cpu_count") or 0))
    except Exception:
        return
    share = slurm_cpu_share(allocated, node_cores)
    if share >= 1.0:
        return
    intensity = (summary.kg_co2 or 0.0) / summary.kwh
    summary.raw_kwh, summary.raw_kg_co2 = summary.kwh, summary.kg_co2
    summary.cpu_share_correction = share
    summary.cpu_kwh *= share
    summary.kwh = summary.cpu_kwh + (summary.ram_kwh or 0.0) + (summary.gpu_kwh or 0.0)
    summary.kg_co2 = summary.kwh * intensity
    summary.hardware["node_physical_cores"] = str(node_cores)
    _patch_task_row(summary, share)


def _patch_task_row(summary: EmissionsSummary, share: float) -> None:
    """Rewrite this run's row in its own per-task CSV with the corrected energy."""
    import csv
    if not summary.emissions_file:
        return
    path = Path(summary.emissions_file)
    if not path.is_file() or path.name == "emissions.csv":
        return            # never rewrite the shared ledger
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not rows[-1].get("project_name", "").endswith(summary.run_name):
        return
    row = rows[-1]
    for key in ("cpu_power", "cpu_energy"):
        if row.get(key):
            row[key] = str(float(row[key]) * share)
    row["energy_consumed"] = str(summary.kwh)
    row["emissions"] = str(summary.kg_co2)
    if summary.duration_s:
        row["emissions_rate"] = str(summary.kg_co2 / summary.duration_s)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _emissions_target(output_dir: Path | None) -> Path:
    """Which CSV this process appends to: the shared ledger, or a per-task file."""
    override = os.environ.get("GNNFLU_EMISSIONS_FILE")
    if override:
        return Path(override)
    directory = output_dir or paths.EMISSIONS_DIR
    task = os.environ.get("SLURM_ARRAY_TASK_ID")
    if task is not None:
        job = os.environ.get("SLURM_ARRAY_JOB_ID", "job")
        return directory / "tasks" / f"{job}_{task}.csv"
    return directory / "emissions.csv"


def _tracking_mode() -> str:
    """'machine' meters the whole computer; 'process' only this process's share.

    A serial run on your own machine is the whole machine's load, and machine
    mode keeps continuity with the existing history. On a shared cluster node,
    or with several tracked runs in parallel, machine mode would bill every run
    for its neighbours, so those default to process mode.
    """
    explicit = os.environ.get("GNNFLU_TRACKING_MODE")
    if explicit in ("machine", "process"):
        return explicit
    parallel = os.environ.get("SLURM_JOB_ID") or os.environ.get("GNNFLU_EMISSIONS_FILE")
    return "process" if parallel else "machine"


def _slurm_job() -> str | None:
    job = os.environ.get("SLURM_ARRAY_JOB_ID") or os.environ.get("SLURM_JOB_ID")
    task = os.environ.get("SLURM_ARRAY_TASK_ID")
    if job is None:
        return None
    return f"{job}_{task}" if task is not None else job


def _measurement_mode(tracker) -> str | None:
    """'measured' when a hardware power counter was read; else how it was estimated."""
    modes = {getattr(h, "_mode", None) for h in getattr(tracker, "_hardware", [])}
    modes.discard(None)
    if modes & _MEASURED_MODES:
        return "measured"
    if "cpu_load" in modes:
        return "estimated (cpu load x TDP)"
    if "constant" in modes:
        return "estimated (constant TDP)"
    return ",".join(sorted(map(str, modes))) or None


def _maybe_float(value) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


# --------------------------------------------------------------------- receipt

def format_seconds(seconds: float | None) -> str:
    if seconds is None:
        return "–"
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(int(round(seconds)), 60)
    if minutes < 60:
        return f"{minutes}m {secs:02d}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m"


def _sig(x: float) -> str:
    """Three significant figures, never scientific notation."""
    if x == 0:
        return "0"
    digits = max(0, 2 - int(math.floor(math.log10(abs(x)))))
    return f"{x:.{digits}f}"


def format_energy(kwh: float | None) -> str:
    if kwh is None:
        return "–"
    if kwh >= 1:
        return f"{_sig(kwh)} kWh"
    if kwh >= 1e-3:
        return f"{_sig(kwh * 1e3)} Wh"
    return f"{_sig(kwh * 1e6)} mWh"


def format_co2(kg: float | None) -> str:
    if kg is None:
        return "–"
    if kg >= 1:
        return f"{_sig(kg)} kg"
    if kg >= 1e-3:
        return f"{_sig(kg * 1e3)} g"
    return f"{_sig(kg * 1e6)} mg"


def _receipt(s: EmissionsSummary, previous: dict | None) -> str:
    parts = s.run_name.split(":") + ([s.city] if s.city else [])
    title = " · ".join(parts)

    phase_bits = []
    if s.setup_s is not None and s.setup_s >= 0.05:
        phase_bits.append(f"setup {format_seconds(s.setup_s)}")
    for name, secs in s.phases.items():
        bit = f"{name} {format_seconds(secs)}"
        if name == "train" and s.epochs:
            bit += f" ({s.epochs} ep, {s.seconds_per_epoch:.2f} s/ep)"
        phase_bits.append(bit)
    lines = []
    if phase_bits:
        lines.append("  |  ".join(phase_bits))

    total = f"total {format_seconds(s.wall_s)}"
    if s.enabled:
        lines.append(f"{total}    energy {format_energy(s.kwh)}    CO2 {format_co2(s.kg_co2)}")
        kwh = s.kwh or 0.0
        lines.append(
            f"≈ {_sig(kwh / _KWH_PER_PHONE_CHARGE)} phone charges · "
            f"{_sig(kwh / _KWH_PER_CUP_OF_TEA)} cups of tea · "
            f"{_sig(kwh / _KWH_PER_100KM_EV * 100_000)} m in an EV"
        )
        if s.phases and "train" in s.phases:
            lines.append(f"train share of energy ≈ {format_energy(s.phase_kwh('train'))}"
                         " (estimated by time share)")
    else:
        lines.append(f"{total}    energy not tracked ({s.note or 'disabled'})")

    versus = _versus(s, previous)
    if versus:
        lines.append(versus)

    if s.enabled:
        cpu = s.hardware.get("cpu_model") or "unknown CPU"
        scope = "this process" if s.tracking_mode == "process" else "whole machine"
        lines.append(f"power: {s.measured or '?'}, {scope}, on {cpu}"
                     f" · grid: {s.region or 'USA avg'}")

    return _box(title, "receipt", lines)


def _versus(s: EmissionsSummary, previous: dict | None) -> str | None:
    if not previous or not previous.get("duration_s") or not s.duration_s:
        return None
    ratio = s.duration_s / float(previous["duration_s"])
    speed = f"{ratio:.2f}× slower" if ratio >= 1 else f"{1 / ratio:.2f}× faster"
    bit = f"vs last run: {speed}"
    if s.kg_co2 is not None and previous.get("kg_co2") is not None:
        delta = s.kg_co2 - float(previous["kg_co2"])
        bit += f", {'+' if delta >= 0 else '-'}{format_co2(abs(delta))} CO2"
    old, new = previous.get("git_sha"), s.git_sha
    if old and new and old != new:
        bit += f"  (git {old} → {new})"
    return bit


def _box(title: str, tag: str, lines: list[str]) -> str:
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower()
    fancy = "utf" in encoding
    if not fancy:
        replace = {"·": "|", "≈": "~", "×": "x", "→": "->", "–": "-"}
        lines = ["".join(replace.get(c, c) for c in line) for line in lines]
        title = "".join(replace.get(c, c) for c in title)
    tl, tr, bl, br, h, v = ("┌", "┐", "└", "┘", "─", "│") if fancy else ("+", "+", "+", "+", "-", "|")
    width = max([len(line) for line in lines] + [len(title) + len(tag) + 6])
    head = f"{tl}{h} {title} " + h * (width - len(title) - len(tag) - 3) + f" {tag} {tr}"
    body = [f"{v} {line.ljust(width)} {v}" for line in lines]
    foot = bl + h * (width + 2) + br
    return "\n".join([head, *body, foot])
