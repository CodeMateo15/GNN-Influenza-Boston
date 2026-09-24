"""Merge the SNVS respiratory workbooks into one AMBA weekly ETI panel.

    python Code/scrapers/build_amba_panel.py

Argentina's Ministry of Health publishes national respiratory surveillance as a
snapshot workbook per release. Three vintages are committed; they overlap, and
the newer ones carry backfill for weeks the older ones reported low, so the
merge takes the newest value on any overlapping key rather than the first.

Outputs, all written beside the workbooks under Data/:
  * amba_eti_weekly_long.csv   one row per partido-week
  * amba_eti_weekly_wide.csv   weeks x 24 partidos
  * amba_node_coverage.csv     reporting coverage per partido, and keep_core
  * amba_eti_revision.csv      completeness by reporting lag, per vintage

Two things worth knowing before using the output:

  * These are CASE COUNTS, not rates. The per-100,000 denominator comes from
    the committed INDEC table (paths.AMBA_STATIC_FILE); there is no Census-API
    equivalent for Argentina.
  * An absent partido-week is a genuine zero only when it is isolated. A run of
    three or more consecutive absences is a reporting blackout and stays NaN,
    which makes Buenos Aires behave like Boston (suppression) rather than like
    Columbus (observed zeros).

Originally written in a different environment against /mnt/user-data paths; it
now resolves everything through influenza.paths so it runs in place.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from influenza import paths  # noqa: E402

UP = str(paths.AMBA_DIR) + "/"
OUT = str(paths.AMBA_DIR) + "/"

# vintage label -> (filename, snapshot date)
SOURCES = {
    "20240405": ("informacion-publica-respiratorias-nacional-hasta-20240405.xlsx", date(2024, 4, 5)),
    "20250904": ("informacion-publica-respiratorias-nacional-hasta-20250904.xlsx", date(2025, 9, 4)),
    "20260310": ("informacion-publica-respiratorias-nacional-hasta-20260310.xlsx", date(2026, 3, 10)),
}
# precedence: last wins
PRECEDENCE = ["20240405", "20250904", "20260310"]

CONURBANO = {
    28: "ALMIRANTE BROWN", 35: "AVELLANEDA", 91: "BERAZATEGUI",
    260: "ESTEBAN ECHEVERRÍA", 270: "EZEIZA", 274: "FLORENCIO VARELA",
    371: "GENERAL SAN MARTÍN", 408: "HURLINGHAM", 410: "ITUZAINGÓ",
    412: "JOSÉ C. PAZ", 427: "LA MATANZA", 434: "LANÚS",
    490: "LOMAS DE ZAMORA", 515: "MALVINAS ARGENTINAS", 539: "MERLO",
    560: "MORENO", 568: "MORÓN", 658: "QUILMES", 749: "SAN FERNANDO",
    756: "SAN ISIDRO", 760: "SAN MIGUEL", 805: "TIGRE",
    840: "TRES DE FEBRERO", 861: "VICENTE LÓPEZ",
}
KEY = ["indec", "anio", "semana", "grupo_edad_id"]


def week1_start(y):
    j = date(y, 1, 4)
    return j - timedelta(days=(j.weekday() + 1) % 7)


def weeks_in_year(y):
    return (week1_start(y + 1) - week1_start(y)).days // 7


def week_start(y, w):
    return week1_start(y) + timedelta(weeks=w - 1)


def week_grid(y0, w0, y1, w1):
    rows, y, w = [], y0, w0
    while (y, w) <= (y1, w1):
        rows.append((y, w, week_start(y, w)))
        w += 1
        if w > weeks_in_year(y):
            y, w = y + 1, 1
    g = pd.DataFrame(rows, columns=["anio", "semana", "week_start"])
    g["t"] = np.arange(len(g))
    return g


def load(tag):
    fn, snap = SOURCES[tag]
    d = pd.read_excel(UP + fn, sheet_name=0, engine="openpyxl")
    d = d.rename(columns={"año": "anio", "semanas_epidemiologicas": "semana"})
    for c in ["departamento_id", "provincia_id", "anio", "semana",
              "grupo_edad_id", "cantidad_casos"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[d.semana.between(1, 53) & d.anio.notna()]
    d["indec"] = (d.provincia_id * 1000 + d.departamento_id).astype(int)
    d = d[d.evento_nombre.str.contains("ETI", na=False)]
    d = d[(d.provincia_id == 6) & (d.departamento_id.isin(CONURBANO))]
    d = d.groupby(KEY, as_index=False).cantidad_casos.sum()
    d["vintage"] = tag
    d["snapshot"] = snap
    return d


print("loading...")
frames = {t: load(t) for t in PRECEDENCE}
for t, d in frames.items():
    print(f"  {t}: {len(d):>7,} keys  "
          f"{int(d.anio.min())}-SE{int(d[d.anio == d.anio.min()].semana.min()):02d} .. "
          f"{int(d.anio.max())}-SE{int(d[d.anio == d.anio.max()].semana.max()):02d}")

# ---------------- revision table (all pairwise vs newest) ----------------
newest = frames["20260310"].set_index(KEY).cantidad_casos
rev_rows = []
for t in ["20240405", "20250904"]:
    old = frames[t].set_index(KEY).cantidad_casos
    j = pd.concat([old.rename("as_reported"), newest.rename("final")], axis=1)
    j = j[j.index.get_level_values("anio").isin(
        frames[t].anio.unique()) & j.final.notna()]
    j = j.fillna(0).reset_index()
    wk = j.groupby(["anio", "semana"], as_index=False)[["as_reported", "final"]].sum()
    snap = SOURCES[t][1]
    wk["week_start"] = [week_start(int(a), int(s)) for a, s in zip(wk.anio, wk.semana)]
    wk = wk[wk.week_start <= snap]
    wk["lag_weeks"] = ((pd.Timestamp(snap) - pd.to_datetime(wk.week_start)).dt.days // 7)
    wk["completeness"] = (wk.as_reported / wk.final.replace(0, np.nan)).round(4)
    wk["vintage"] = t
    rev_rows.append(wk)
rev = pd.concat(rev_rows, ignore_index=True)
rev = rev[["vintage", "anio", "semana", "week_start", "lag_weeks",
           "as_reported", "final", "completeness"]]
rev.to_csv(OUT + "amba_eti_revision.csv", index=False)

curve = (rev[rev.lag_weeks.between(0, 40)]
         .groupby("lag_weeks").completeness.median().round(3))
print("\nbackfill (median completeness by lag, weeks):")
print("  " + "  ".join(f"L{int(k)}={v:.2f}" for k, v in curve.head(14).items()))

# ---------------- merged panel ----------------
stacked = pd.concat([frames[t] for t in PRECEDENCE], ignore_index=True)
stacked["prio"] = stacked.vintage.map({t: i for i, t in enumerate(PRECEDENCE)})
stacked = stacked.sort_values("prio").drop_duplicates(KEY, keep="last")
print(f"\nmerged: {len(stacked):,} unique keys")
print(stacked.vintage.value_counts().to_string())

obs = stacked.groupby(["indec", "anio", "semana"], as_index=False).cantidad_casos.sum()

y0, w0 = 2022, 1
last = obs[obs.anio == obs.anio.max()]
y1, w1 = int(last.anio.iloc[0]), int(last.semana.max())
grid = week_grid(y0, w0, y1, w1)
nodes = pd.DataFrame({"indec": [6000 + k for k in CONURBANO],
                      "partido": list(CONURBANO.values())})
panel = nodes.merge(grid, how="cross").merge(
    obs, on=["indec", "anio", "semana"], how="left")

# province reported that week at all -> absent means true zero
prov_weeks = set(map(tuple, obs[["anio", "semana"]].drop_duplicates().values))
panel["prov_reported"] = [
    (a, s) in prov_weeks for a, s in zip(panel.anio, panel.semana)]
panel["cases"] = panel.cantidad_casos.astype(float)
panel = panel.sort_values(["indec", "t"]).reset_index(drop=True)

# An absent node-week is a genuine zero if isolated, but a run of >= RUN
# consecutive absences is a reporting blackout and stays NaN.
RUN = 3
panel["absent"] = panel.cantidad_casos.isna()
grp = panel.groupby("indec", sort=False)
blk = grp.absent.transform(
    lambda s: s.groupby((s != s.shift()).cumsum()).transform("size").where(s, 0))
panel["blackout"] = panel.absent & (blk >= RUN)
panel.loc[panel.absent & ~panel.blackout, "cases"] = 0.0
panel.loc[panel.blackout, "cases"] = np.nan

long = panel[["indec", "partido", "anio", "semana", "week_start", "t", "cases"]]

wide = long.pivot(index=["t", "anio", "semana", "week_start"],
                  columns="partido", values="cases").reset_index()
wide.columns.name = None

cov = (long.groupby(["indec", "partido"])
       .cases.apply(lambda s: s.notna().mean()).round(3)
       .rename("coverage").reset_index()
       .sort_values("coverage", ascending=False))
cov["cases_total"] = long.groupby("indec").cases.sum().reindex(cov.indec).values
cov["keep_core"] = cov.coverage >= 0.90

long.to_csv(OUT + "amba_eti_weekly_long.csv", index=False)
wide.to_csv(OUT + "amba_eti_weekly_wide.csv", index=False)
cov.to_csv(OUT + "amba_node_coverage.csv", index=False)

print(f"\npanel: {wide.shape[0]} weeks x {len(nodes)} nodes")
print(f"  {int(long.cases.isna().sum()):,} node-weeks NaN "
      f"({long.cases.isna().mean():.1%})")
print(f"  core nodes (>=90% coverage): {int(cov.keep_core.sum())}")
print(cov.to_string(index=False))
