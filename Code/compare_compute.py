"""How long does each model take, what does it cost in energy and CO2, and is
the extra accuracy worth it?

Reads what the runs already wrote -- no training:

  * every <tree>/<model>/<variant>/emissions.json (written by finish_run, now
    with wall-clock and per-phase time even under --no-carbon);
  * the metered history in results/_emissions/emissions.csv plus the per-task
    files cluster array jobs write to results/_emissions/tasks/;
  * predictions.csv in each horizon tree, scored as relative WIS against
    persistence with compare_significance.relative_wis -- the paper's number.

and writes, under results/_compute/ (per city root):

  compute_ledger.csv   every metered run ever logged (notebook era included)
  compute_runs.csv     the latest run in each results directory, time + energy
  leaderboard.csv/.md  per horizon: accuracy, time, energy, CO2, skill per gram
  frontier.png         accuracy against energy, with the Pareto front drawn
  compute_table.md/.tex  the compact Appendix S1 table

and refreshes the auto section of Code/docs/COMPUTE.md (Boston only, unless
--update-doc is passed for another city).

    python Code/compare_compute.py
    python Code/compare_compute.py --city chicago --update-doc
    python Code/compare_compute.py --results-dir results/backtest_2023_24 --no-doc
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from compare_significance import horizon_roots, load_predictions, relative_wis  # noqa: E402
from influenza import paths  # noqa: E402
from influenza.carbon import (  # noqa: E402
    CITY_PREFIX,
    _KWH_PER_100KM_EV,
    _KWH_PER_CUP_OF_TEA,
    _KWH_PER_PHONE_CHARGE,
    format_co2,
    format_energy,
    format_seconds,
)
from influenza.cities import get as get_city  # noqa: E402
from influenza.cli import add_city_arg, city_results_dir  # noqa: E402
from influenza.palette import INK_MUTED, INK_PRIMARY, SERIES, SURFACE  # noqa: E402

DOC = paths.ROOT / "Code" / "docs" / "COMPUTE.md"
BEGIN, END = "<!-- compute:auto:begin -->", "<!-- compute:auto:end -->"

# Baselines that define the zero of "skill": they are shown, never ranked.
REFERENCE_MODELS = {"persistence", "climatology", "seasonal_naive"}

# The one-time measurement pass writes here (Code/sweep/tasks_compute.jsonl and
# local runs), kept apart so re-measuring cost never overwrites scored results.
MEASURE_DIR = "_measure"
HORIZON_RE = re.compile(r"^h(\d+)$")
PREFIX_TO_CITY = {prefix: city for city, prefix in CITY_PREFIX.items()}


# ------------------------------------------------------------------ reading

def parse_run_name(name: str) -> dict:
    """'gnn_st:post_covid:h2' -> model, variant, horizon. Older names lack the horizon."""
    parts = [p for p in str(name).split(":") if p]
    horizon = None
    if parts and HORIZON_RE.match(parts[-1]):
        horizon = int(HORIZON_RE.match(parts[-1]).group(1))
        parts = parts[:-1]
    if len(parts) >= 3 and parts[0] == "shap":          # shap:<model>:<variant>
        return {"model": f"shap:{parts[1]}", "variant": parts[2], "horizon": horizon}
    return {"model": parts[0] if parts else None,
            "variant": parts[1] if len(parts) > 1 else None,
            "horizon": horizon}


def hardware_label(cpu_model: str | None, slurm: bool = False) -> str:
    """Short, comparable hardware family: energy on different machines is not comparable."""
    cpu = cpu_model.strip() if isinstance(cpu_model, str) else ""
    cpu = re.sub(r"\(R\)|\(TM\)|\bCPU\b|\bProcessor\b|@ [\d.]+GHz|\d+-Core", "", cpu)
    cpu = re.sub(r"^(Intel|AMD)\s+", "", re.sub(r"\s+", " ", cpu)).strip()
    if slurm or cpu.lower().startswith(("intel(r) xeon", "amd epyc")):
        return f"Explorer ({cpu})" if cpu else "Explorer"
    return cpu or "unknown"


def read_ledger() -> pd.DataFrame:
    """Every metered row codecarbon ever appended, shared CSV plus per-task files."""
    files = [paths.EMISSIONS_DIR / "emissions.csv",
             *sorted((paths.EMISSIONS_DIR / "tasks").glob("*.csv"))]
    frames = []
    for path in files:
        if not path.exists():
            continue
        try:
            frame = pd.read_csv(path)
        except (pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
            print(f"warning: skipping unreadable {paths.display(path)} ({exc})")
            continue
        frame["source"] = paths.display(path)
        frames.append(frame)
    if not frames:
        return pd.DataFrame()
    raw = pd.concat(frames, ignore_index=True)

    rows = []
    for record in raw.to_dict("records"):
        project = str(record.get("project_name") or "")
        prefix, _, rest = project.partition(":")
        city = PREFIX_TO_CITY.get(prefix)
        if city is None:                       # the notebook era, or a blank row
            parsed = {"model": "notebook", "variant": None, "horizon": None}
            era = "notebook" if project else "unlabelled"
        else:
            parsed = parse_run_name(rest)
            era = "cluster" if "/tasks/" in record["source"] else "local"
        rows.append({
            "timestamp": record.get("timestamp"),
            "city": city,
            "era": era,
            **parsed,
            "duration_s": record.get("duration"),
            "kwh": record.get("energy_consumed"),
            "kg_co2": record.get("emissions"),
            "cpu_kwh": record.get("cpu_energy"),
            "ram_kwh": record.get("ram_energy"),
            "gpu_kwh": record.get("gpu_energy"),
            "region": record.get("region"),
            "hardware": hardware_label(record.get("cpu_model"), era == "cluster"),
            "project_name": project,
            "source": record["source"],
        })
    ledger = pd.DataFrame(rows)
    ledger["timestamp"] = pd.to_datetime(ledger["timestamp"], errors="coerce")
    return ledger.sort_values("timestamp").reset_index(drop=True)


def read_runs(results_root: Path) -> pd.DataFrame:
    """One row per results directory holding an emissions.json."""
    rows = []
    for path in sorted(results_root.rglob("emissions.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        parsed = parse_run_name(data.get("run_name", ""))
        directory = path.parent
        phases = data.get("phases") or {}
        hw = data.get("hardware") or {}
        rows.append({
            "tree": paths.display(directory.parents[1]) if len(directory.parents) > 1 else "",
            "dir_model": directory.parent.name,
            **parsed,
            "city": data.get("city"),
            "enabled": bool(data.get("enabled")),
            "wall_s": data.get("wall_s") or data.get("duration_s"),
            "tracked_s": data.get("duration_s"),
            "setup_s": data.get("setup_s"),
            "train_s": phases.get("train"),
            "eval_s": phases.get("eval"),
            "epochs": data.get("epochs"),
            "s_per_epoch": data.get("seconds_per_epoch"),
            "kwh": data.get("kwh"),
            "kg_co2": data.get("kg_co2"),
            "measured": data.get("measured"),
            "tracking_mode": data.get("tracking_mode"),
            "region": data.get("region"),
            "hardware": hardware_label(hw.get("cpu_model"), bool(data.get("slurm_job"))),
            "git_sha": data.get("git_sha"),
            "note": data.get("note"),
            "written": pd.Timestamp(path.stat().st_mtime, unit="s").floor("s"),
            "path": paths.display(directory),
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ joining

def cost_for(model: str, variant: str, horizon: int | None, run: dict | None,
             ledger: pd.DataFrame, city: str) -> dict:
    """Time and energy for one model at one horizon, with where each number came from.

    Prefers the run that produced the scored predictions. Energy falls back to
    the median of metered history for the same model/variant/horizon.
    """
    out = {"wall_s": None, "s_per_epoch": None, "kwh": None, "kg_co2": None,
           "hardware": None, "energy_source": "not measured", "measured": None}
    if run is not None:
        out.update(wall_s=run["wall_s"], s_per_epoch=run["s_per_epoch"],
                   hardware=run["hardware"] if run["enabled"] else None)
        if run["enabled"] and run["kwh"] is not None:
            out.update(kwh=run["kwh"], kg_co2=run["kg_co2"], measured=run["measured"],
                       energy_source="this run")
            return out
    if ledger.empty:
        return out
    pool = ledger[(ledger["model"] == model) & (ledger["variant"] == variant)
                  & (ledger["city"] == city) & ledger["kwh"].notna()]
    # Only same-horizon history. Rows logged before run names carried a horizon
    # (August 2026) include sub-2-second smoke tests of since-changed models;
    # borrowing them would put a near-free LSTM on the frontier.
    for subset, label in ((pool[pool["horizon"] == horizon], "history, same horizon"),):
        if len(subset):
            out.update(kwh=float(subset["kwh"].median()), kg_co2=float(subset["kg_co2"].median()),
                       energy_source=f"median of {len(subset)} ({label})")
            if out["hardware"] is None:
                out["hardware"] = subset["hardware"].mode().iat[0]
            if pd.isna(out["wall_s"]):
                out["wall_s"] = float(subset["duration_s"].median())
            return out
    return out


def leaderboard(results_root: Path, variant: str, runs: pd.DataFrame,
                ledger: pd.DataFrame, city: str) -> tuple[pd.DataFrame, str]:
    rows, label = [], "WIS"
    for horizon, root in horizon_roots(results_root):
        frames = load_predictions(root, variant)
        if not frames:
            continue
        rel, label = relative_wis(frames)
        tree = paths.display(root)
        for model in frames:
            # Cost: the scored run if it was metered, else the measurement pass,
            # else metered history at the same horizon.
            run = _latest_run(runs, tree, model, variant)
            measured = None if horizon is None else _latest_run(runs, paths.display(
                results_root / MEASURE_DIR / f"horizon_{horizon:02d}"), model, variant)
            if (run is None or not run["enabled"]) and measured is not None and measured["enabled"]:
                cost = cost_for(model, variant, horizon, measured, ledger, city)
                cost["energy_source"] = "measurement pass (current code)"
            else:
                cost = cost_for(model, variant, horizon, run, ledger, city)
            rel_wis = rel.get(model)
            skill = None if rel_wis is None else 1.0 - rel_wis
            grams = None if cost["kg_co2"] is None else cost["kg_co2"] * 1000
            per_gram = (skill / grams if skill is not None and grams and skill > 0
                        and model not in REFERENCE_MODELS else None)
            rows.append({"horizon": horizon, "model": model, "rel_wis": rel_wis,
                         "skill": skill, "g_co2": grams, "skill_per_gram": per_gram,
                         **cost})
    board = pd.DataFrame(rows)
    if board.empty:
        return board, label
    board["wh"] = board["kwh"] * 1000
    board["on_frontier"] = False
    for horizon, part in board.groupby("horizon", dropna=False):
        for idx in pareto_front(part):
            board.loc[idx, "on_frontier"] = True
    board = board.sort_values(["horizon", "rel_wis"]).reset_index(drop=True)
    return board, label


def _latest_run(runs: pd.DataFrame, tree: str, model: str, variant: str) -> dict | None:
    if runs.empty:
        return None
    match = runs[(runs["tree"] == tree) & (runs["dir_model"] == model)
                 & (runs["variant"] == variant)]
    return match.sort_values("written").iloc[-1].to_dict() if len(match) else None


def pareto_front(part: pd.DataFrame) -> list:
    """Indices no other model beats on both energy and accuracy (lower is better on both)."""
    known = part.dropna(subset=["kwh", "rel_wis"]).sort_values(["kwh", "rel_wis"])
    front, best = [], math.inf
    for idx, row in known.iterrows():
        if row["rel_wis"] < best:
            front.append(idx)
            best = row["rel_wis"]
    return front


def price_of_accuracy(board: pd.DataFrame) -> list[str]:
    """Walking up each headline frontier: extra CO2 paid per point of WIS removed."""
    lines = []
    headline = board[board["model"].isin(headline_models(board["model"]))]
    for horizon, part in headline.groupby("horizon", dropna=False):
        part = part.loc[pareto_front(part)].sort_values("kwh")
        steps = list(part.itertuples())
        for a, b in zip(steps, steps[1:]):
            points = (a.rel_wis - b.rel_wis) * 100
            extra = (b.kg_co2 or 0) - (a.kg_co2 or 0)
            if points <= 0:
                continue
            lines.append(f"- h={horizon}: **{a.model} → {b.model}** removes {points:.1f} points of "
                         f"relative WIS for {format_co2(extra)} more CO2 "
                         f"({format_co2(extra / points)} per point).")
    return lines


# ------------------------------------------------------------------ outputs

# Models that are not trained, so tuning does not apply to them.
UNTRAINED = {"persistence", "seasonal_naive", "climatology", "blend_baseline",
             "flusight_baseline", "arima", "sarima"}


def headline_models(models) -> set[str]:
    """Which models go on the frontier plot (every model stays in the tables).

    With equal-tuned arms present -- the paper's backtest set -- the headline is
    the tuned learners against the untrained baselines (PAPER_PLAN, Claim 2).
    Otherwise gnn_st's own ablation arms are dropped as design variants, not
    competitors, as in compare_significance.is_family_member.
    """
    models = set(models)
    tuned = {m for m in models if m.endswith("_tuned")}
    if tuned:
        return tuned | (models & UNTRAINED)
    return {m for m in models if m == "gnn_st" or not m.startswith("gnn_")}


def machine_family(hardware: str | None) -> str:
    hw = hardware or "unknown"
    return "Explorer (1 core)" if hw.startswith("Explorer") else f"laptop ({hw})"


def plot_frontier(board: pd.DataFrame, label: str, out: Path, city: str,
                  include_variants: bool = False) -> Path | None:
    known = board.dropna(subset=["wh", "rel_wis"])
    if not include_variants:
        known = known[known["model"].isin(headline_models(known["model"]))].copy()
    # Re-derive the front among the plotted models only.
    known["on_frontier"] = False
    for _, part in known.groupby("horizon", dropna=False):
        known.loc[pareto_front(part), "on_frontier"] = True
    known["family"] = known["hardware"].map(machine_family)
    if known.empty:
        return None
    horizons = sorted(known["horizon"].dropna().unique()) or [None]
    families = sorted(known["family"].unique())
    shapes = dict(zip(families, ["o", "s", "^", "D"]))
    fig, axes = plt.subplots(1, len(horizons), figsize=(5.2 * len(horizons), 4.6),
                             squeeze=False, sharey=True)
    for ax, horizon in zip(axes[0], horizons):
        part = known if horizon is None else known[known["horizon"] == horizon]
        for family in families:
            sub = part[part["family"] == family]
            for on, colour in ((False, INK_MUTED), (True, SERIES[1])):
                pts = sub[sub["on_frontier"] == on]
                ax.scatter(pts["wh"], pts["rel_wis"], s=46, marker=shapes[family],
                           color=colour, edgecolor=SURFACE, linewidth=1.2, zorder=3,
                           label=f"{family}{' · frontier' if on else ''}" if len(pts) else None)
        front = part[part["on_frontier"]].sort_values("wh")
        if len(front) > 1:
            ax.step(front["wh"], front["rel_wis"], where="post", color=SERIES[1], lw=1.5, zorder=2)
        for row in part.itertuples():
            ax.annotate(row.model, (row.wh, row.rel_wis), xytext=(5, 4),
                        textcoords="offset points", fontsize=8,
                        color=INK_PRIMARY if row.on_frontier else INK_MUTED)
        ax.axhline(1.0, color=INK_MUTED, lw=0.8, ls="--", zorder=1)
        ax.set_xscale("log")
        ax.set_xlabel("Energy per run (Wh, log scale)")
        ax.set_title(f"h = {horizon}" if horizon is not None else "")
    axes[0][0].set_ylabel(f"Relative {label} vs persistence (lower is better)")
    seen = {}
    for ax in axes[0]:
        for handle, text in zip(*ax.get_legend_handles_labels()):
            seen.setdefault(text, handle)
    axes[0][-1].legend(seen.values(), seen.keys(), fontsize=8, loc="upper right")
    fig.suptitle(f"{city.title()}: how much accuracy each watt-hour buys")
    fig.tight_layout()
    path = out / "frontier.png"
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    return path


def _fmt(value, kind: str) -> str:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return "–"
    return {"s": format_seconds, "kwh": format_energy, "kg": format_co2,
            "rel": lambda v: f"{v:.2f}", "spg": lambda v: f"{v:.3g}",
            "spe": lambda v: f"{v:.2f}s"}[kind](value)


def leaderboard_md(board: pd.DataFrame, label: str) -> str:
    lines = []
    for horizon, part in board.groupby("horizon", dropna=False):
        lines += [f"#### Horizon {horizon} week{'s' if horizon != 1 else ''} ahead", "",
                  f"| Model | How close to the truth, vs persistence (rel. {label}; <1 better) "
                  "| Time per run | Time per epoch | Energy | CO2 | Skill per gram | "
                  "On frontier | Hardware | Energy from |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for r in part.sort_values("rel_wis").itertuples():
            spg = ("reference" if r.model in REFERENCE_MODELS
                   else "no skill" if r.skill is not None and r.skill <= 0
                   else _fmt(r.skill_per_gram, "spg"))
            lines.append(f"| {r.model} | {_fmt(r.rel_wis, 'rel')} | {_fmt(r.wall_s, 's')} | "
                         f"{_fmt(r.s_per_epoch, 'spe')} | {_fmt(r.kwh, 'kwh')} | "
                         f"{_fmt(r.kg_co2, 'kg')} | {spg} | {'yes' if r.on_frontier else ''} | "
                         f"{r.hardware or '–'} | {r.energy_source} |")
        lines.append("")
    return "\n".join(lines)


def paper_tables(board: pd.DataFrame, out: Path) -> tuple[Path, Path]:
    horizons = sorted(board["horizon"].dropna().unique())
    models = list(dict.fromkeys(board.sort_values("rel_wis")["model"]))
    cell = {(r.model, r.horizon): r for r in board.itertuples()}

    md = ["| Model | Hardware | " + " | ".join(f"h={h} time | h={h} energy | h={h} CO2"
                                              for h in horizons) + " |",
          "|---|---|" + "---|" * (3 * len(horizons))]
    tex = [r"\begin{tabular}{ll" + "rrr" * len(horizons) + "}", r"\toprule",
           " & & " + " & ".join(rf"\multicolumn{{3}}{{c}}{{$h={h}$}}" for h in horizons) + r" \\",
           " ".join(rf"\cmidrule(lr){{{3 + 3 * i}-{5 + 3 * i}}}" for i in range(len(horizons))),
           "Model & Hardware & " + " & ".join(["Time & Wh & g CO$_2$"] * len(horizons)) + r" \\",
           r"\midrule"]
    for model in models:
        rows = [cell.get((model, h)) for h in horizons]
        hw = next((r.hardware for r in rows if r is not None and r.hardware), "–")
        md_cells, tex_cells = [], []
        for r in rows:
            t = _fmt(None if r is None else r.wall_s, "s")
            wh = "–" if r is None or r.kwh is None or not np.isfinite(r.kwh) else f"{r.kwh * 1000:.3g}"
            g = "–" if r is None or r.g_co2 is None or not np.isfinite(r.g_co2) else f"{r.g_co2:.3g}"
            md_cells += [t, wh, g]
            tex_cells += [t.replace("–", "--"), wh.replace("–", "--"), g.replace("–", "--")]
        md.append(f"| {model} | {hw} | " + " | ".join(md_cells) + " |")
        tex.append(f"{model.replace('_', chr(92) + '_')} & {hw.replace('_', chr(92) + '_')} & "
                   + " & ".join(tex_cells) + r" \\")
    tex += [r"\bottomrule", r"\end{tabular}"]
    md_path, tex_path = out / "compute_table.md", out / "compute_table.tex"
    md_path.write_text("\n".join(md) + "\n")
    tex_path.write_text("\n".join(tex) + "\n")
    return md_path, tex_path


def project_total(ledger: pd.DataFrame) -> str:
    if ledger.empty:
        return "No metered runs yet."
    kwh, kg = ledger["kwh"].sum(), ledger["kg_co2"].sum()
    by_era = ledger.groupby("era")["kwh"].agg(["count", "sum"])
    eras = ", ".join(f"{era} {int(r['count'])} runs / {format_energy(r['sum'])}"
                     for era, r in by_era.iterrows())
    return (f"Everything metered so far: **{format_energy(kwh)}**, **{format_co2(kg)} CO2** "
            f"across {len(ledger)} runs ({eras}) — about {kwh / _KWH_PER_PHONE_CHARGE:.0f} phone "
            f"charges, {kwh / _KWH_PER_CUP_OF_TEA:.0f} cups of tea, or "
            f"{kwh / _KWH_PER_100KM_EV * 100:.1f} km in an EV.")


def update_doc(section: str) -> None:
    if not DOC.exists():
        print(f"warning: {paths.display(DOC)} missing; auto section not written")
        return
    text = DOC.read_text()
    if BEGIN not in text or END not in text:
        print(f"warning: markers missing in {paths.display(DOC)}; auto section not written")
        return
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    DOC.write_text(f"{head}{BEGIN}\n{section.rstrip()}\n{END}{tail}")
    print(f"Updated {paths.display(DOC)}")


# ------------------------------------------------------------------ main

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    add_city_arg(parser)
    parser.add_argument("--results-dir", type=Path, default=None,
                        help="A city root (horizon_XX/ below it) or one horizon tree.")
    parser.add_argument("--variant", default="post_covid")
    parser.add_argument("--include-variants", action="store_true",
                        help="Also plot gnn_st's ablation arms on the frontier.")
    doc = parser.add_mutually_exclusive_group()
    doc.add_argument("--update-doc", action="store_true",
                     help="Refresh COMPUTE.md's auto section even for a non-Boston city.")
    doc.add_argument("--no-doc", action="store_true", help="Never touch COMPUTE.md.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    city = get_city(args.city)
    results_root = city_results_dir(args, city).resolve()
    out = results_root / "_compute"
    out.mkdir(parents=True, exist_ok=True)

    ledger = read_ledger()
    runs = read_runs(results_root)
    ledger.to_csv(out / "compute_ledger.csv", index=False)
    runs.to_csv(out / "compute_runs.csv", index=False)

    board, label = leaderboard(results_root, args.variant, runs, ledger, city.name)
    if board.empty:
        raise SystemExit(f"error: no {args.variant} predictions under {results_root}")
    board.drop(columns=["kwh"]).to_csv(out / "leaderboard.csv", index=False)
    table = leaderboard_md(board, label)
    (out / "leaderboard.md").write_text(table)
    figure = plot_frontier(board, label, out, city.name, args.include_variants)
    md_path, tex_path = paper_tables(board, out)

    missing = sorted(board.loc[board["kwh"].isna(), "model"].unique())
    price = price_of_accuracy(board)
    stamp = pd.Timestamp.now().isoformat(timespec="minutes")
    section = "\n".join([
        f"_Regenerated {stamp} by `python Code/compare_compute.py --city {city.name}` "
        f"from `{paths.display(results_root)}` ({args.variant})._", "",
        "### Project total", "", project_total(ledger), "",
        "### Leaderboard", "",
        "Skill per gram = (1 − relative WIS) ÷ grams of CO2: how much better than "
        "\"next week equals this week\" each gram buys. Higher is better; baselines "
        "are the zero point and are not ranked.", "",
        table,
        "### The price of accuracy, along the frontier", "",
        *(price or ["- Not enough metered models on any frontier yet."]), "",
        *( [f"**Not yet metered:** {', '.join(missing)}. Run them once with tracking on "
            "(see *Filling the gaps* above).", ""] if missing else []),
        "### Accuracy vs energy", "",
        (f"![frontier]({Path('..') / 'results' / figure.relative_to(paths.RESULTS_DIR)})"
         if figure is not None and figure.is_relative_to(paths.RESULTS_DIR)
         else f"`{paths.display(figure)}`" if figure else "_No metered model to plot yet._"), "",
        "### Paper table (Appendix S1)", "",
        md_path.read_text(),
        f"LaTeX: `{paths.display(tex_path)}`",
    ])
    if not args.no_doc and (city.name == "boston" or args.update_doc):
        update_doc(section)

    print(table)
    for line in price:
        print(line)
    if missing:
        print(f"\nNot yet metered: {', '.join(missing)}")
    print(f"\n{project_total(ledger)}")
    print(f"Outputs: {paths.display(out)}")


if __name__ == "__main__":
    main()
