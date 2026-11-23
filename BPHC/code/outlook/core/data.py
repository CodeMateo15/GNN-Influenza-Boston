# Generated copy of boston-flu-outlook/core/data.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Everything the app shows, loaded once at import from data/ (written by publish.py).

Loaded at import rather than per session: the files are small and identical for
every visitor, so the first page view should not pay for reading them.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

# OUTLOOK_DATA_DIR points the app (or export_html.py) at another published data
# folder, laid out like data/: one subfolder per city.
DATA_DIR = Path(os.environ.get("OUTLOOK_DATA_DIR") or Path(__file__).resolve().parents[1] / "data")
QUANTILES = [f"q{q:.3f}" for q in (0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                                   0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95,
                                   0.975, 0.99)]

# Plain names first: the audience is a health department, not a methods section.
MODEL_NAMES = {
    "gnn_st": "Neighborhood graph model",
    "lstm": "LSTM (sequence model)",
    "colagnn": "Cola-GNN (graph model from the literature)",
    "arima": "ARIMA (seasonal statistical model)",
    "avg": "Average of the four models",
    "persistence": "Same as last week",
}
MODEL_SHORT = {"gnn_st": "Graph model", "lstm": "LSTM", "colagnn": "Cola-GNN", "arima": "ARIMA",
               "avg": "Average", "persistence": "Same as last week"}
# Colour follows the model, never its rank: categorical slots 1-5 (slot 4 also
# dashed, slot 5 dotted), and the reference in neutral ink so it never reads as a
# competitor.
MODEL_CLASS = {"gnn_st": "s1", "lstm": "s2", "colagnn": "s3", "arima": "s4", "avg": "s5",
               "persistence": "sref"}
PRIMARY = "gnn_st"

CITY_INFO = {
    "boston": dict(
        label="Boston", area_word="neighborhood", areas_word="neighborhoods",
        unit="emergency-department visits for flu-like illness per 100,000 residents",
        unit_short="visits per 100k", fmt="{:.1f}", min_change=2.0,
        source="Boston Public Health Commission, public influenza dashboard (weekly ED "
               "visits for influenza-like illness by neighborhood)"),
    "chicago": dict(
        label="Chicago", area_word="ZIP code", areas_word="ZIP codes",
        unit="flu-like illness activity level, 1 (minimal) to 10 (very high)",
        unit_short="activity level", fmt="{:.1f}", cap=10,
        # CDC's ILI activity-level bands (minimal 1-3, low 4-5, moderate 6-7,
        # high 8-10), shifted onto the four names this app uses everywhere.
        fixed_levels=(4, 6, 8), min_change=1.0,
        source="Chicago Department of Public Health, “Influenza Risk Level by ZIP "
               "Code” on the City of Chicago Data Portal (Illinois ESSENCE ED data)",
        # Required by the City of Chicago Data Portal terms of use.
        disclaimer="This site provides applications using data that has been modified for "
                   "use from its original source, www.cityofchicago.org, the official website "
                   "of the City of Chicago. The City of Chicago makes no claims as to the "
                   "content, accuracy, timeliness, or completeness of any of the data provided "
                   "at this site. The data provided at this site is subject to change at any "
                   "time. It is understood that the data provided at this site is being used "
                   "at one's own risk."),
}

# What the graph model's forecast is split into (publish.py copies the package's
# drivers.csv): the area's own inputs, then everything the other areas add.
OWN_DRIVERS = ("level", "trend", "history", "weather", "calendar")
DRIVERS = OWN_DRIVERS + ("neighbor",)

LEVELS = ("Low", "Moderate", "High", "Very high")
LEVEL_STATUS = {"Low": "good", "Moderate": "warning", "High": "serious", "Very high": "critical"}
# Intensity lines (the moving epidemic method, at CDC's 50/90/98% levels): a week
# at or above IT50 is moderate, IT90 high, IT98 very high. z = Phi^-1(p).
SEVERITY_Z = {"IT50": 0.0, "IT90": 1.2816, "IT98": 2.0537}
# Seasons the lines are never fitted on: COVID-19 truncated 2019-20 and
# suppressed the next two, as in the paper's severity analysis.
COVID_SEASONS = ("2019-20", "2020-21", "2021-22")
MEM_POOL = 30  # values pooled across seasons, as the mem R package sizes it


def t_quantile(z: float, df: int) -> float:
    """Student t quantile from the normal one (Cornish-Fisher series); within
    1e-4 of the exact value from 5 degrees of freedom up."""
    v = float(df)
    return (z + (z**3 + z) / (4 * v) + (5 * z**5 + 16 * z**3 + 3 * z) / (96 * v**2)
            + (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / (384 * v**3)
            + (79 * z**9 + 776 * z**7 + 1482 * z**5 - 1920 * z**3 - 945 * z) / (92160 * v**4))


@dataclass
class CityData:
    key: str
    info: dict
    meta: dict
    forecast: pd.DataFrame
    history: pd.DataFrame
    comparison: pd.DataFrame
    bt_scores: pd.DataFrame
    live_scores: pd.DataFrame | None
    trust_notes: list[str]
    geo: dict
    edges: list[tuple[str, str]]
    runtimes: pd.DataFrame | None = None  # seconds per model, horizon and weekly origin
    drivers: pd.DataFrame | None = None   # graph-model attributions, one row per driver
    _severity: dict = field(default_factory=dict, repr=False)  # thresholds, by area (None = city)

    # --- basics ------------------------------------------------------------
    @property
    def label(self) -> str:
        return self.info["label"]

    @property
    def areas(self) -> list[str]:
        return list(self.history.columns)

    @property
    def origin(self) -> pd.Timestamp:
        return pd.Timestamp(self.meta["origin"])

    @property
    def horizons(self) -> list[int]:
        return sorted(int(h) for h in self.forecast["horizon"].unique())

    @property
    def models(self) -> list[str]:
        order = list(MODEL_NAMES)
        found = list(self.forecast["model"].unique())
        return sorted(found, key=lambda m: order.index(m) if m in order else 99)

    @property
    def preview(self) -> bool:
        return bool(self.meta.get("quick"))

    def fmt(self, value) -> str:
        if value is None or not np.isfinite(value):
            return "—"
        return self.info["fmt"].format(value)

    # --- observed ------------------------------------------------------------
    def latest(self) -> pd.Series:
        """Each area's value in the origin week, or its last reported week if BPHC
        suppressed that one."""
        hist = self.history.loc[:self.origin]
        return hist.ffill().iloc[-1]

    def citywide(self) -> pd.Series:
        return self.history.mean(axis=1, skipna=True)

    # --- forecast ------------------------------------------------------------
    def rows(self, model: str, area: str | None = None) -> pd.DataFrame:
        f = self.forecast[self.forecast["model"] == model]
        if area is not None:
            f = f[f["area"] == area]
        return f.sort_values("horizon")

    def at(self, model: str, horizon: int) -> pd.Series:
        """Median forecast per area at one horizon (horizon 0 = the latest observation)."""
        if horizon == 0:
            return self.latest()
        f = self.forecast[(self.forecast["model"] == model) & (self.forecast["horizon"] == horizon)]
        return f.set_index("area")["predicted"].reindex(self.areas)

    def citywide_forecast(self, model: str) -> pd.DataFrame:
        """Average over areas of each forecast column, per horizon. The band of an
        average is narrower than the average of bands; this is the readable
        approximation, and the page says it is an average of area forecasts."""
        f = self.forecast[self.forecast["model"] == model]
        cols = ["predicted", "lower", "upper", "q0.250", "q0.750"]
        out = f.groupby(["horizon", "target_date"])[cols].mean().reset_index()
        return out.sort_values("horizon")

    def trust(self, model: str, horizon: int) -> str:
        f = self.forecast[(self.forecast["model"] == model) & (self.forecast["horizon"] == horizon)]
        return str(f["trust"].iloc[0]) if len(f) and "trust" in f else "not backtested"

    # --- context ---------------------------------------------------------------
    def level(self, area: str | None, value: float) -> str | None:
        """A week's level: against this area's intensity lines (the same ones the
        Severity tab draws), or the city's fixed cut points where it publishes a
        graded scale."""
        if value is None or not np.isfinite(value):
            return None
        if "fixed_levels" in self.info:
            cuts = self.info["fixed_levels"]
            return LEVELS[sum(value >= c for c in cuts)]
        if area is not None and area not in self.history.columns:
            return None
        return self.severity_class(value, area)

    def seasons(self, series: pd.Series | None = None) -> dict[str, pd.Series]:
        """A weekly series (default: the citywide average) by week of season, per
        season. Seasons open on 1 August."""
        city = (self.citywide() if series is None else series).dropna()
        out: dict[str, pd.Series] = {}
        for week, value in city.items():
            year = week.year if week.month >= 8 else week.year - 1
            start = pd.Timestamp(year=year, month=8, day=1)
            label = f"{year}-{str(year + 1)[2:]}"
            out.setdefault(label, {})[(week - start).days // 7] = value
        return {k: pd.Series(v).sort_index() for k, v in out.items()}

    def season_label(self, week: pd.Timestamp) -> str:
        year = week.year if week.month >= 8 else week.year - 1
        return f"{year}-{str(year + 1)[2:]}"

    def season_roles(self) -> dict[str, str]:
        """Each season's part in the archived model: "training" if the graph model fit
        on any of its weeks, "validation" if they were only held out (to choose when
        to stop training and how wide to draw the ranges), "current" for this one.
        Empty when the archive predates meta["training"]."""
        window = self.meta.get("training")
        if not window:
            return {}
        t0, t1 = (pd.Timestamp(d) for d in window["train_targets"])
        current = self.season_label(self.origin)
        roles = {}
        for label, s in self.seasons().items():
            year = int(label[:4])
            weeks = pd.Timestamp(year=year, month=8, day=1) + pd.to_timedelta(s.index * 7, unit="D")
            fit = ((weeks >= t0) & (weeks <= t1)).any()
            roles[label] = "current" if label == current else "training" if fit else "validation"
        return roles

    # --- what drove the graph model ----------------------------------------------
    @property
    def has_drivers(self) -> bool:
        return self.drivers is not None and (self.drivers["origin_date"] == self.origin).any()

    def _drivers(self, area: str | None, h: int, origin=None) -> pd.DataFrame:
        d = self.drivers
        d = d[(d["horizon"] == h) & (d["origin_date"] == (self.origin if origin is None else origin))]
        return d if area is None else d[d["area"] == area]

    def waterfall(self, area: str, h: int) -> dict:
        """Base (a usual week at this time of year), each driver's push, and the
        forecast they add up to. `adjust` takes the explained forecast to the
        published median."""
        d = self._drivers(area, h)
        own = d[d["driver"].isin(OWN_DRIVERS)].set_index("driver")
        nbr = d[d["driver"] == "neighbor"].set_index("source_area")
        adjust = d.loc[d["driver"] == "adjust", "value"].sum()
        steps = [(k, float(own.at[k, "value"]), float(own.at[k, "se"])) for k in OWN_DRIVERS
                 if k in own.index]
        steps.append(("neighbor", float(nbr["value"].sum()),
                      float(np.sqrt((nbr["se"] ** 2).sum()))))
        first = d.iloc[0]
        return {"base": float(first["base"]), "steps": steps, "adjust": float(adjust),
                "output": float(first["output"]), "total": float(first["output"] + adjust),
                "neighbors": nbr["value"].sort_values(key=abs, ascending=False),
                "blend_share": float(first["blend_share"]),
                "target_date": pd.Timestamp(first["target_date"])}

    def spillover(self, area: str, h: int) -> pd.Series:
        """What every other area adds to `area`'s forecast, by source area."""
        d = self._drivers(area, h)
        return d[d["driver"] == "neighbor"].set_index("source_area")["value"]

    def driver_matrix(self, h: int) -> pd.DataFrame:
        """Areas x drivers (neighbors summed), plus base and forecast, at the live origin."""
        d = self._drivers(None, h)
        out = (d[d["driver"].isin(DRIVERS)].groupby(["area", "driver"])["value"].sum()
               .unstack("driver").reindex(columns=list(DRIVERS)))
        firsts = d.groupby("area")[["base", "output"]].first()
        adjust = d[d["driver"] == "adjust"].groupby("area")["value"].sum()
        out["base"] = firsts["base"]
        out["total"] = firsts["output"] + adjust.reindex(firsts.index).fillna(0)
        return out.reindex(self.areas)

    def driver_history(self, area: str, h: int) -> pd.DataFrame:
        """Per origin since the season start: each driver, base, forecast and what
        happened, for one area and horizon."""
        d = self.drivers
        d = d[(d["area"] == area) & (d["horizon"] == h)]
        out = (d[d["driver"].isin(DRIVERS)].groupby(["origin_date", "driver"])["value"].sum()
               .unstack("driver").reindex(columns=list(DRIVERS)))
        firsts = d.groupby("origin_date")[["target_date", "base", "output", "actual"]].first()
        return out.join(firsts).sort_index()

    def past_seasons(self, area: str | None = None) -> dict[str, pd.Series]:
        """Complete past seasons, skipping 2020-21, the season flu did not circulate.
        What every season-level comparison is made with. A season is complete when
        the city has 40+ weeks of it: a neighborhood's missing weeks are BPHC
        suppressing small counts, so they are never its peak."""
        current = self.season_label(self.origin)
        full = {label for label, s in self.seasons().items()
                if label not in (current, "2020-21") and len(s) >= 40}
        series = self.seasons(None if area is None else self.history[area])
        return {label: s for label, s in series.items() if label in full}

    def typical_peak(self) -> float:
        """Median of past complete seasons' citywide peaks."""
        peaks = [s.max() for s in self.past_seasons().values()]
        return float(np.median(peaks)) if peaks else float("nan")

    # --- how severe the season is ----------------------------------------------------
    # Citywide when `area` is None, otherwise against that area's own history.
    def reference_seasons(self, area: str | None = None) -> dict[str, pd.Series]:
        """The seasons the intensity lines are fitted on: every earlier season with
        data, less the COVID-19 ones."""
        current = self.season_label(self.origin)
        series = self.seasons(None if area is None else self.history[area])
        return {label: s for label, s in series.items()
                if label < current and label not in COVID_SEASONS}

    def severity_thresholds(self, area: str | None = None) -> dict:
        """Intensity thresholds by the moving epidemic method, following the mem R
        package's defaults as the paper does: pool each reference season's k
        highest weeks, k = round(30 / seasons); in logs, IT_p = exp(mean +
        t_p(m-1) * sqrt(1 + 1/m) * SD), the one-sided upper limit for one more
        week, at CDC's levels (Vega et al. 2013; Biggerstaff et al. 2018)."""
        if area not in self._severity:
            ref = self.reference_seasons(area)
            k = max(1, round(MEM_POOL / len(ref)))
            top = {label: s.nlargest(k) for label, s in ref.items()}
            pooled = np.concatenate([t.to_numpy() for t in top.values()])
            shift = 1.0 if (pooled <= 0).any() else 0.0  # mem adds 1 rather than drop zeros
            logs = np.log(pooled + shift)
            m = len(logs)
            mu, sigma = float(logs.mean()), float(logs.std(ddof=1))
            mult = {key: t_quantile(z, m - 1) * np.sqrt(1 + 1 / m) for key, z in SEVERITY_Z.items()}
            self._severity[area] = {
                "top": top, "k": k, "mu": mu, "sigma": sigma, "n": m, "mult": mult,
                "its": {key: float(np.exp(mu + c * sigma) - shift) for key, c in mult.items()}}
        return self._severity[area]

    def severity_class(self, value: float, area: str | None = None) -> str | None:
        if value is None or not np.isfinite(value):
            return None
        its = self.severity_thresholds(area)["its"]
        return LEVELS[sum(value >= its[k] for k in SEVERITY_Z)]

    def season_severity(self, area: str | None = None) -> pd.DataFrame:
        """Every season's peak, when it came, and its class. `role` is "used" (in
        the thresholds), "current", or "skipped"."""
        series = (self.citywide() if area is None else self.history[area]).dropna()
        used, current = self.reference_seasons(area), self.season_label(self.origin)
        rows = []
        for label, s in self.seasons(series).items():
            year = int(label[:4])
            span = series[(series.index >= f"{year}-08-01") & (series.index < f"{year + 1}-08-01")]
            rows.append({"season": label, "peak": float(s.max()), "peak_week": int(s.idxmax()),
                         "peak_date": span.idxmax(), "weeks": len(s),
                         "cls": self.severity_class(s.max(), area),
                         "role": "current" if label == current else "used" if label in used
                         else "skipped"})
        return pd.DataFrame(rows).sort_values("season").reset_index(drop=True)

    def exceed_prob(self, threshold: float, model: str = PRIMARY,
                    area: str | None = None) -> pd.Series:
        """Chance the value is above `threshold`, per horizon, with the CDF
        interpolated between the quantiles; outside the 1%-99% quantiles it stays at
        1% / 99%. Citywide, the area quantiles are averaged (Vincentized), as
        citywide_forecast does."""
        f = self.forecast[self.forecast["model"] == model]
        if area is not None:
            f = f[f["area"] == area]
        cols = [c for c in QUANTILES if c in f]
        levels = np.array([float(c[1:]) for c in cols])
        q = f.groupby("horizon")[cols].mean()
        return pd.Series({h: 1 - float(np.interp(threshold, np.maximum.accumulate(row.to_numpy()),
                                                 levels))
                          for h, row in q.iterrows()}).sort_index()

    def analogs(self, n: int = 3) -> list[dict]:
        """Past seasons closest to this one so far (plus the graph model's medians),
        by RMSE of log(1 + value) over the same weeks since 1 August."""
        current = self.season_label(self.origin)
        path = self.seasons().get(current, pd.Series(dtype=float)).copy()
        start = pd.Timestamp(year=int(current[:4]), month=8, day=1)
        for r in self.citywide_forecast(PRIMARY).itertuples():
            path[(pd.Timestamp(r.target_date) - start).days // 7] = r.predicted
        out = []
        for label, s in self.past_seasons().items():
            common = path.index.intersection(s.index)
            if len(common) < 4:
                continue
            gap = np.log1p(path[common]) - np.log1p(s[common])
            out.append({"season": label, "rmse": float(np.sqrt((gap ** 2).mean())),
                        "weeks": len(common), "series": s,
                        "peak": float(s.max()), "peak_week": int(s.idxmax()),
                        "cls": self.severity_class(s.max()),
                        "ahead": float(s.get(path.index.max(), np.nan))})
        return sorted(out, key=lambda a: a["rmse"])[:n]


def _load(key: str) -> CityData | None:
    folder = DATA_DIR / key
    if not (folder / "meta.json").exists():
        return None
    meta = json.loads((folder / "meta.json").read_text())
    forecast = pd.read_csv(folder / "forecast.csv", parse_dates=["origin_date", "target_date"],
                           dtype={"area": str})
    history = pd.read_csv(folder / "history.csv", index_col="week", parse_dates=True)
    history.columns = [str(c) for c in history.columns]
    live = folder / "live_scores.csv"
    live_scores = (pd.read_csv(live, parse_dates=["origin_date", "target_date"], dtype={"area": str})
                   if live.exists() else None)
    runtime = folder / "runtimes.csv"
    runtimes = pd.read_csv(runtime) if runtime.exists() else None
    trust_notes = [line[2:].strip() for line in (folder / "trust.md").read_text().splitlines()
                   if line.startswith("- ")]
    edges = pd.read_csv(folder / "edges.csv", dtype=str)
    driver_file = folder / "drivers.csv"
    drivers = (pd.read_csv(driver_file, parse_dates=["origin_date", "target_date"],
                           dtype={"area": str, "source_area": str}).fillna({"source_area": ""})
               if driver_file.exists() else None)
    city = CityData(
        key=key, info=CITY_INFO[key], meta=meta, forecast=forecast, history=history,
        comparison=pd.read_csv(folder / "backtest_comparison.csv"),
        bt_scores=pd.read_csv(folder / "backtest_scores.csv"), live_scores=live_scores,
        trust_notes=trust_notes, geo=json.loads((folder / "geo.json").read_text()),
        edges=list(zip(edges["a"], edges["b"])), runtimes=runtimes, drivers=drivers)
    return city


CITIES: dict[str, CityData] = {k: c for k in CITY_INFO if (c := _load(k)) is not None}
BOSTON = CITIES.get("boston")
CHICAGO = CITIES.get("chicago")


def flusight(city: CityData, model: str | None = None) -> pd.DataFrame:
    """FluSight hub layout: one row per quantile."""
    f = city.forecast if model is None else city.forecast[city.forecast["model"] == model]
    cols = [c for c in QUANTILES if c in f.columns]
    long = f.melt(id_vars=["model", "origin_date", "target_date", "horizon", "area"],
                  value_vars=cols, var_name="q", value_name="value")
    return pd.DataFrame({
        "model": long["model"], "reference_date": long["origin_date"].dt.date,
        "target": "wk inc flu rate" if city.key == "boston" else "wk ili activity level",
        "horizon": long["horizon"], "target_end_date": long["target_date"].dt.date,
        "location": long["area"], "output_type": "quantile",
        "output_type_id": long["q"].str[1:].astype(float), "value": long["value"].round(3),
    }).sort_values(["model", "location", "horizon", "output_type_id"])
