# Generated copy of boston-flu-outlook/core/charts.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Inline-SVG charts. Every colour is a CSS class (www/styles.css), so light and
dark mode are handled by the token blocks there, not here.

Hover: any element with `data-tip` gets the shared tooltip (www/app.js); the
first line is the heading. Line charts put one invisible full-height column per
week under the pointer, so the whole plot is the hit target, not the 2px line.
"""

from __future__ import annotations

import math
from html import escape

import numpy as np
import pandas as pd

from .data import LEVEL_STATUS, LEVELS, MODEL_CLASS, MODEL_SHORT


def esc(text) -> str:
    return escape(str(text), quote=True)


def nice_ticks(hi: float, n: int = 4) -> list[float]:
    if not np.isfinite(hi) or hi <= 0:
        return [0.0, 1.0]
    raw = hi / n
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return [i * step for i in range(int(math.ceil(hi / step)) + 1)]


def _fmt_tick(v: float) -> str:
    return f"{v:.0f}" if v == int(v) else f"{v:.1f}"


def _date(d) -> str:
    return pd.Timestamp(d).strftime("%b %-d")


class Frame:
    """Plot geometry: maps dates and values to pixels."""

    def __init__(self, width, height, x0, x1, ymax, left=44, right=16, top=14, bottom=28):
        self.w, self.h = width, height
        self.l, self.r, self.t, self.b = left, right, top, bottom
        self.x0, self.x1 = pd.Timestamp(x0), pd.Timestamp(x1)
        self.ticks = nice_ticks(ymax)
        self.ymax = self.ticks[-1]

    def x(self, d) -> float:
        span = (self.x1 - self.x0).days or 1
        return self.l + (pd.Timestamp(d) - self.x0).days / span * (self.w - self.l - self.r)

    def y(self, v) -> float:
        return self.t + (1 - v / self.ymax) * (self.h - self.t - self.b)

    def grid(self, unit_label: str = "") -> str:
        parts = []
        for v in self.ticks:
            y = self.y(v)
            parts.append(f'<line class="grid" x1="{self.l}" x2="{self.w - self.r}" y1="{y:.1f}" y2="{y:.1f}"/>'
                         f'<text class="tick" x="{self.l - 6}" y="{y + 4:.1f}" text-anchor="end">{_fmt_tick(v)}</text>')
        parts.append(f'<line class="axis" x1="{self.l}" x2="{self.w - self.r}" y1="{self.y(0):.1f}" y2="{self.y(0):.1f}"/>')
        # Month ticks along the bottom.
        month = pd.Timestamp(self.x0.year, self.x0.month, 1) + pd.offsets.MonthBegin(1)
        while month <= self.x1:
            x = self.x(month)
            parts.append(f'<text class="tick" x="{x:.1f}" y="{self.h - 8}" text-anchor="middle">{month.strftime("%b")}</text>')
            month += pd.offsets.MonthBegin(1)
        if unit_label:
            parts.append(f'<text class="tick" x="{self.l}" y="{self.t - 3}">{esc(unit_label)}</text>')
        return "".join(parts)


def _path(points) -> str:
    pts = [(x, y) for x, y in points if np.isfinite(y)]
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) if pts else ""


def _band(fr: Frame, dates, lo, hi) -> str:
    top = [(fr.x(d), fr.y(v)) for d, v in zip(dates, hi)]
    bottom = [(fr.x(d), fr.y(v)) for d, v in zip(dates[::-1], lo[::-1])]
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in top + bottom) + "Z"


# --- fan chart ---------------------------------------------------------------------

def fan_chart(history: pd.Series, forecasts: dict[str, pd.DataFrame], *, unit: str, fmt,
              weeks: int = 20, width: int = 760, height: int = 300, cap: float | None = None) -> str:
    """Observed weeks, then each model's median for 1-4 weeks ahead. The first model
    in `forecasts` other than "same as last week" gets the 50% and 95% bands; the
    others are lines only, so the bands never pile up. "Same as last week" is a
    yardstick (the latest week carried forward), so it never carries a range."""
    origin = history.dropna().index.max()
    hist = history.loc[:origin].iloc[-weeks:]
    last = hist.dropna().iloc[-1]
    ends = [f["target_date"].max() for f in forecasts.values() if len(f)]
    x1 = max(ends) if ends else origin
    banded = next((m for m, f in forecasts.items() if m != "persistence" and len(f)), None)
    top = max([hist.max()] + [(f["upper"] if m == banded else f["predicted"]).max()
                              for m, f in forecasts.items() if len(f)])
    if cap:
        top = min(max(top, 1), cap)
    fr = Frame(width, height, hist.index.min(), x1, top * 1.05)
    out = [f'<svg class="chart fan" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Observed and forecast {esc(unit)}">', fr.grid(unit)]
    out.append(f'<line class="today" x1="{fr.x(origin):.1f}" x2="{fr.x(origin):.1f}" y1="{fr.t}" '
               f'y2="{fr.y(0):.1f}"/><text class="today-label" x="{fr.x(origin) + 4:.1f}" '
               f'y="{fr.t + 10}">latest data</text>')
    for model, f in forecasts.items():
        if not len(f):
            continue
        cls = MODEL_CLASS.get(model, "s1")
        dates = [origin] + list(f["target_date"])
        if model == banded:
            out.append(f'<path class="band95 {cls}" d="{_band(fr, dates, [last] + list(f["lower"]), [last] + list(f["upper"]))}"/>')
            out.append(f'<path class="band50 {cls}" d="{_band(fr, dates, [last] + list(f["q0.250"]), [last] + list(f["q0.750"]))}"/>')
        med = [(fr.x(d), fr.y(v)) for d, v in zip(dates, [last] + list(f["predicted"]))]
        out.append(f'<path class="line fc {cls}" d="{_path(med)}"/>')
        out += [f'<circle class="dot {cls}" cx="{x:.1f}" cy="{y:.1f}" r="4"/>' for x, y in med[1:]]
    obs = [(fr.x(d), fr.y(v)) for d, v in hist.items()]
    out.append(f'<path class="line obs" d="{_path(obs)}"/>')
    out.append(f'<circle class="dot obs" cx="{fr.x(origin):.1f}" cy="{fr.y(last):.1f}" r="4"/>')
    # Hover columns.
    weeks_all = list(hist.index) + sorted({d for f in forecasts.values() for d in f["target_date"]})
    step = (fr.x(weeks_all[1]) - fr.x(weeks_all[0])) if len(weeks_all) > 1 else 20
    for d in weeks_all:
        lines = [f"Week of {_date(d)}"]
        if d in hist.index and np.isfinite(hist.get(d, np.nan)):
            lines.append(f"Observed: {fmt(hist[d])}")
        elif d <= origin:
            lines.append("Observed: not reported")
        for model, f in forecasts.items():
            row = f[f["target_date"] == d]
            if len(row):
                r = row.iloc[0]
                lines.append(f"{MODEL_SHORT.get(model, model)}: {fmt(r['predicted'])}"
                             + ("" if model == "persistence"
                                else f" (95%: {fmt(r['lower'])}–{fmt(r['upper'])})"))
        x = fr.x(d)
        out.append(f'<g class="col" data-tip="{esc(chr(10).join(lines))}">'
                   f'<rect class="hit" x="{x - step / 2:.1f}" y="{fr.t}" width="{step:.1f}" height="{fr.y(0) - fr.t:.1f}"/>'
                   f'<line class="guide" x1="{x:.1f}" x2="{x:.1f}" y1="{fr.t}" y2="{fr.y(0):.1f}"/></g>')
    out.append("</svg>")
    return "".join(out)


# --- season ribbons ------------------------------------------------------------------

def ribbons(seasons: dict[str, pd.Series], current: str, forecast: list[tuple[int, float]], *,
            unit: str, fmt, width: int = 760, height: int = 280,
            highlight: dict[str, str] | None = None) -> str:
    """This season against every past one, by week since 1 August. Past seasons are
    recessive grey; the current one carries the colour (emphasis, not identity).
    `highlight` maps past seasons to a series class, drawn in colour and labelled."""
    highlight = highlight or {}
    top = max(s.max() for s in seasons.values())
    if forecast:
        top = max(top, max(v for _, v in forecast))
    ticks = nice_ticks(top * 1.05)
    ymax = ticks[-1]
    l, r, t, b = 44, 16, 14, 28
    X = lambda wk: l + wk / 52 * (width - l - r)
    Y = lambda v: t + (1 - v / ymax) * (height - t - b)
    out = [f'<svg class="chart ribbons" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="This season compared with past seasons">']
    for v in ticks:
        out.append(f'<line class="grid" x1="{l}" x2="{width - r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="tick" x="{l - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{_fmt_tick(v)}</text>')
    for i, m in enumerate(["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]):
        out.append(f'<text class="tick" x="{X(i * 52 / 12 + 2):.1f}" y="{height - 8}" text-anchor="middle">{m}</text>')
    out.append(f'<text class="tick" x="{l}" y="{t - 3}">{esc(unit)}</text>')
    for label, s in sorted(seasons.items(), key=lambda kv: (kv[0] in highlight, kv[0])):
        if label == current:
            continue
        pts = [(X(wk), Y(v)) for wk, v in s.items()]
        peak = s.idxmax()
        cls = f"line {highlight[label]}" if label in highlight else "past"
        out.append(f'<path class="{cls}" d="{_path(pts)}" data-tip="{esc(label)}&#10;Peak {esc(fmt(s.max()))}, '
                   f'week {int(peak)} of the season"/>')
        if label in highlight:
            out.append(f'<text class="direct" x="{X(peak) + 6:.1f}" y="{Y(s.max()) - 6:.1f}">'
                       f'{esc(label)}</text>')
    if current in seasons:
        s = seasons[current]
        pts = [(X(wk), Y(v)) for wk, v in s.items()]
        out.append(f'<path class="line now" d="{_path(pts)}"/>')
        if forecast and len(s):
            fpts = [(X(s.index[-1]), Y(s.iloc[-1]))] + [(X(wk), Y(v)) for wk, v in forecast]
            out.append(f'<path class="line now-fc" d="{_path(fpts)}"/>')
            out += [f'<circle class="dot now" cx="{x:.1f}" cy="{y:.1f}" r="4"/>' for x, y in fpts[1:]]
        if len(s):
            x, y = X(s.index[-1]), Y(s.iloc[-1])
            out.append(f'<text class="direct" x="{x + 8:.1f}" y="{y - 8:.1f}">{esc(current)}</text>')
    out.append("</svg>")
    return "".join(out)


# --- map --------------------------------------------------------------------------------

def bins_for(values: list[float], cap: float | None = None) -> list[float]:
    """Five upper edges for six classes, on rounded numbers, fixed across horizons so
    the animation compares like with like."""
    if cap:
        return [2, 4, 6, 8, 9.5]
    v = np.array([x for x in values if np.isfinite(x)])
    hi = np.nanpercentile(v, 97) if len(v) else 1
    edges = nice_ticks(hi, 6)[1:6]
    while len(edges) < 5:
        edges.append(edges[-1] * 1.5)
    return edges


def choropleth(geo: dict, values: dict[str, float], edges: list[float], *, tips: dict[str, str],
               selected: str | None = None, input_id: str = "area_click",
               labels: dict[str, tuple[float, float, str]] | None = None) -> str:
    vb = geo["viewBox"]
    out = [f'<svg class="chart map" viewBox="{vb}" role="img" aria-label="Map">']
    if geo.get("context"):
        out.append(f'<path class="context" d="{geo["context"]}"/>')
    for area, shape in geo["areas"].items():
        v = values.get(area, np.nan)
        cls = "bna" if not np.isfinite(v) else f"b{sum(v > e for e in edges)}"
        sel = " selected" if area == selected else ""
        out.append(f'<path class="area {cls}{sel}" d="{shape["d"]}" fill-rule="evenodd" '
                   f'data-area="{esc(area)}" data-input="{input_id}" data-tip="{esc(tips.get(area, area))}" '
                   f'tabindex="0"/>')
    if selected and selected in geo["areas"]:
        out.append(f'<path class="area-outline" d="{geo["areas"][selected]["d"]}" fill-rule="evenodd"/>')
    for area, (x, y, text) in (labels or {}).items():
        out.append(f'<text class="map-label" x="{x:.1f}" y="{y:.1f}" text-anchor="middle">{esc(text)}</text>')
    out.append("</svg>")
    return "".join(out)


def legend_bins(edges: list[float], fmt, unit: str) -> str:
    cells = []
    bounds = [0.0] + list(edges)
    for i in range(6):
        text = f"{fmt(bounds[i])}–{fmt(bounds[i + 1])}" if i < 5 else f"over {fmt(edges[-1])}"
        cells.append(f'<span class="lg-cell"><span class="lg-swatch b{i}"></span>{esc(text)}</span>')
    cells.append('<span class="lg-cell"><span class="lg-swatch bna"></span>not reported</span>')
    return f'<div class="legend-bins"><span class="lg-title">{esc(unit)}</span>{"".join(cells)}</div>'


# --- small multiple -------------------------------------------------------------------

def spark(history: pd.Series, f: pd.DataFrame, *, ymax: float, width=220, height=92) -> str:
    origin = history.dropna().index.max()
    hist = history.loc[:origin].iloc[-12:]
    last = hist.dropna().iloc[-1]
    x1 = f["target_date"].max() if len(f) else origin
    fr = Frame(width, height, hist.index.min(), x1, ymax, left=4, right=4, top=6, bottom=6)
    out = [f'<svg class="chart spark" viewBox="0 0 {width} {height}" aria-hidden="true">',
           f'<line class="axis" x1="4" x2="{width - 4}" y1="{fr.y(0):.1f}" y2="{fr.y(0):.1f}"/>']
    if len(f):
        dates = [origin] + list(f["target_date"])
        out.append(f'<path class="band95 s1" d="{_band(fr, dates, [last] + list(f["lower"]), [last] + list(f["upper"]))}"/>')
        out.append(f'<path class="line fc s1" d="{_path([(fr.x(d), fr.y(v)) for d, v in zip(dates, [last] + list(f["predicted"]))])}"/>')
    out.append(f'<path class="line obs" d="{_path([(fr.x(d), fr.y(v)) for d, v in hist.items()])}"/>')
    out.append(f'<line class="today" x1="{fr.x(origin):.1f}" x2="{fr.x(origin):.1f}" y1="6" y2="{fr.y(0):.1f}"/>')
    out.append("</svg>")
    return "".join(out)


# --- network ------------------------------------------------------------------------------

def network(geo: dict, edges: list[tuple[str, str]], short: dict[str, str]) -> str:
    out = [f'<svg class="chart network" viewBox="{geo["viewBox"]}" role="img" '
           f'aria-label="Which areas the model treats as neighbours">']
    for area, shape in geo["areas"].items():
        out.append(f'<path class="net-area" d="{shape["d"]}" fill-rule="evenodd"/>')
    cents = {a: s["c"] for a, s in geo["areas"].items()}
    for a, b in edges:
        if a in cents and b in cents:
            (x1, y1), (x2, y2) = cents[a], cents[b]
            out.append(f'<line class="net-edge" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                       f'data-tip="{esc(short.get(a, a))} ↔ {esc(short.get(b, b))}&#10;share a border"/>')
    degree = {a: sum(a in e for e in edges) for a in cents}
    for a, (x, y) in cents.items():
        out.append(f'<circle class="net-node" cx="{x}" cy="{y}" r="{5 + degree[a]:.0f}" '
                   f'data-tip="{esc(short.get(a, a))}&#10;{degree[a]} neighbouring areas"/>')
    out.append("</svg>")
    return "".join(out)


# --- track record ---------------------------------------------------------------------------

def coverage_dots(table: pd.DataFrame, width=560, height=None) -> str:
    """How often the truth fell inside the 50% and the 95% range, per model and
    horizon. A hollow ring marks the 50% range, a filled dot the 95% range; each
    has its own target line. Rows are model x horizon."""
    rows = table.sort_values(["model", "horizon"])
    has50 = "coverage50" in rows and rows["coverage50"].notna().any()
    height = height or 30 + 22 * len(rows)
    l, r = 200, 24
    lo = 25 if has50 else 50
    X = lambda p: l + (min(max(p, lo), 100) - lo) / (100 - lo) * (width - l - r)
    out = [f'<svg class="chart dots" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="How often the truth fell inside the 50% and 95% ranges">']
    for p in range(lo, 101, 25):
        out.append(f'<line class="grid" x1="{X(p):.1f}" x2="{X(p):.1f}" y1="14" y2="{height - 18}"/>'
                   f'<text class="tick" x="{X(p):.1f}" y="{height - 4}" text-anchor="middle">{p}%</text>')
    for target in ((50, 95) if has50 else (95,)):
        out.append(f'<line class="target" x1="{X(target):.1f}" x2="{X(target):.1f}" y1="14" '
                   f'y2="{height - 18}"/><text class="tick" x="{X(target):.1f}" y="10" '
                   f'text-anchor="middle">target {target}%</text>')
    for i, row in enumerate(rows.itertuples()):
        y = 26 + i * 22
        name = MODEL_SHORT.get(row.model, row.model)
        cls = MODEL_CLASS.get(row.model, "s1")
        p95 = 100 * row.coverage95
        p50 = 100 * row.coverage50 if has50 and np.isfinite(row.coverage50) else None
        tip = f"{name}, {row.horizon} week(s) ahead&#10;Inside the 95% range {p95:.0f}% of the time"
        if p50 is not None:
            tip += f"&#10;Inside the 50% range {p50:.0f}% of the time"
        out.append(f'<text class="row-label" x="{l - 10}" y="{y + 4}" text-anchor="end">'
                   f'{esc(name)}, {row.horizon} wk</text>')
        out.append(f'<g data-tip="{tip}"><rect class="hit" x="{l}" y="{y - 10}" '
                   f'width="{width - l - r}" height="20"/>')
        if p50 is not None:
            out.append(f'<circle class="ring {cls}" cx="{X(p50):.1f}" cy="{y}" r="5"/>')
        out.append(f'<circle class="dot {cls}" cx="{X(p95):.1f}" cy="{y}" r="5"/></g>')
    out.append("</svg>")
    return "".join(out)


def two_city(series: dict[str, pd.Series], *, width=760, height=260) -> str:
    """Each city as a share of its own typical peak, by week of season: one axis,
    two indexed series, so no dual scale is needed."""
    top = max(100, max(s.max() for s in series.values() if len(s)))
    ticks = nice_ticks(top * 1.05)
    ymax = ticks[-1]
    l, r, t, b = 44, 70, 14, 28
    X = lambda wk: l + wk / 52 * (width - l - r)
    Y = lambda v: t + (1 - v / ymax) * (height - t - b)
    out = [f'<svg class="chart twocity" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Each city against its own typical peak">']
    for v in ticks:
        out.append(f'<line class="grid" x1="{l}" x2="{width - r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                   f'<text class="tick" x="{l - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:.0f}%</text>')
    out.append(f'<line class="target" x1="{l}" x2="{width - r}" y1="{Y(100):.1f}" y2="{Y(100):.1f}"/>')
    for i, m in enumerate(["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]):
        out.append(f'<text class="tick" x="{X(i * 52 / 12 + 2):.1f}" y="{height - 8}" text-anchor="middle">{m}</text>')
    for i, (name, s) in enumerate(series.items()):
        if not len(s):
            continue
        cls = f"s{i + 1}"
        pts = [(X(wk), Y(v)) for wk, v in s.items()]
        out.append(f'<path class="line {cls}" d="{_path(pts)}"/>')
        x, y = pts[-1]
        out.append(f'<circle class="dot {cls}" cx="{x:.1f}" cy="{y:.1f}" r="4" '
                   f'data-tip="{esc(name)}&#10;{s.iloc[-1]:.0f}% of a typical peak"/>')
        out.append(f'<text class="direct" x="{x + 8:.1f}" y="{y + 4:.1f}">{esc(name)}</text>')
    out.append("</svg>")
    return "".join(out)


# --- what drove the forecast ---------------------------------------------------------------
# One encoding for every chart in this group: warm pushes the forecast up, cool
# pulls it down, grey is "about the same as a usual week". The sign is always
# printed too, so colour never carries it alone.

def signed(value: float, fmt) -> str:
    """+1.2 / −0.4 with a real minus sign."""
    text = fmt(abs(value))
    return ("+" if value >= 0 else "−") + text


def div_edges(values, floor: float = 0.05) -> list[float]:
    """Three upper edges for the |value| classes 0-3, from the biggest push shown,
    so a map or matrix keeps one scale across neighborhoods."""
    v = np.abs(np.asarray([x for x in values if np.isfinite(x)], dtype=float))
    top = float(np.percentile(v, 98)) if len(v) else 1.0
    step = nice_ticks(max(top, floor * 4), 3)
    e = [max(floor, step[1] / 4), step[1], step[2] if len(step) > 2 else step[1] * 2]
    return [round(x, 2) for x in e]


def div_class(value: float, edges: list[float]) -> str:
    if value is None or not np.isfinite(value):
        return "bna"
    k = sum(abs(value) >= e for e in edges)
    return "d0" if k == 0 else f"{'dp' if value > 0 else 'dn'}{k}"


def legend_div(edges: list[float], fmt, unit: str) -> str:
    e1, e2, e3 = edges
    cells = [("dn3", f"down {fmt(e3)}+"), ("dn2", f"down {fmt(e2)}–{fmt(e3)}"),
             ("dn1", f"down {fmt(e1)}–{fmt(e2)}"), ("d0", f"within ±{fmt(e1)}"),
             ("dp1", f"up {fmt(e1)}–{fmt(e2)}"), ("dp2", f"up {fmt(e2)}–{fmt(e3)}"),
             ("dp3", f"up {fmt(e3)}+")]
    body = "".join(f'<span class="lg-cell"><span class="lg-swatch {c}"></span>{esc(t)}</span>'
                   for c, t in cells)
    return f'<div class="legend-bins"><span class="lg-title">{esc(unit)}</span>{body}</div>'


def waterfall(rows: list[dict], *, base: float, total: float, base_label: str,
              total_label: str, fmt, unit: str, whisker: tuple[float, float] | None = None,
              base_tip: str = "", total_tip: str = "", width: int = 560) -> str:
    """Start at a usual week, add each driver's push, end on the forecast. Rows are
    {label, sub, value, se, tip}; bars float from the running total."""
    L, R, T, row_h, bar_h = 182, 46, 10, 34, 16
    n = len(rows) + 2
    height = T + n * row_h + 28
    running, ends = base, [0.0, base]
    for r in rows:
        running += r["value"]
        ends.append(running)
    ends += [total] + (list(whisker) if whisker else [])
    lo, hi = min(0.0, min(ends)), max(ends) * 1.04
    ticks = nice_ticks(hi)
    hi = ticks[-1]
    X = lambda v: L + (v - lo) / (hi - lo or 1) * (width - L - R)
    out = [f'<svg class="chart waterfall" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="What moved the forecast away from a usual week">']
    for v in ticks:
        out.append(f'<line class="grid" x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{T}" '
                   f'y2="{T + n * row_h:.1f}"/><text class="tick" x="{X(v):.1f}" '
                   f'y="{T + n * row_h + 14:.1f}" text-anchor="middle">{_fmt_tick(v)}</text>')
    out.append(f'<text class="tick" x="{width - R:.1f}" y="{height - 2}" '
               f'text-anchor="end">{esc(unit)}</text>')

    def row(i, label, sub, x0, x1, cls, value_text, tip, strong=False, label_at=None):
        y = T + i * row_h
        mid = y + row_h / 2
        parts = [f'<g class="wf-row" data-tip="{esc(tip)}">',
                 f'<rect class="hit" x="0" y="{y}" width="{width}" height="{row_h}"/>',
                 f'<text class="row-label{" strong" if strong else ""}" x="{L - 12}" '
                 f'y="{mid + (0 if sub else 4):.1f}" text-anchor="end">{esc(label)}</text>']
        if sub:
            parts.append(f'<text class="wf-sub" x="{L - 12}" y="{mid + 13:.1f}" '
                         f'text-anchor="end">{esc(sub)}</text>')
        a, b = sorted((X(x0), X(x1)))
        parts.append(f'<rect class="wf-bar {cls}" x="{a:.1f}" y="{mid - bar_h / 2:.1f}" '
                     f'width="{max(b - a, 2):.1f}" height="{bar_h}" rx="3"/>')
        parts.append(f'<text class="wf-val{" strong" if strong else ""}" x="{max(a, b, label_at or 0) + 6:.1f}" '
                     f'y="{mid + 4:.1f}">{esc(value_text)}</text></g>')
        return "".join(parts)

    out.append(row(0, base_label, "", 0, base, "wf-base", fmt(base), base_tip))
    running = base
    for i, r in enumerate(rows, start=1):
        y = T + i * row_h
        out.append(f'<line class="wf-link" x1="{X(running):.1f}" x2="{X(running):.1f}" '
                   f'y1="{y - row_h / 2 + bar_h / 2:.1f}" y2="{y + row_h / 2 - bar_h / 2:.1f}"/>')
        cls = "wf-up" if r["value"] > 0 else "wf-down"
        out.append(row(i, r["label"], r.get("sub", ""), running, running + r["value"], cls,
                       signed(r["value"], fmt), r["tip"]))
        running += r["value"]
    i = n - 1
    y = T + i * row_h
    out.append(f'<line class="wf-link" x1="{X(running):.1f}" x2="{X(running):.1f}" '
               f'y1="{y - row_h / 2 + bar_h / 2:.1f}" y2="{y + row_h / 2 - bar_h / 2:.1f}"/>')
    out.append(row(i, total_label, "", 0, total, "wf-total", fmt(total), total_tip, strong=True,
                   label_at=X(whisker[1]) if whisker else None))
    if whisker:
        mid = y + row_h / 2
        a, b = X(whisker[0]), X(whisker[1])
        out.append(f'<g class="wf-whisker"><line x1="{a:.1f}" x2="{b:.1f}" y1="{mid:.1f}" '
                   f'y2="{mid:.1f}"/><line x1="{a:.1f}" x2="{a:.1f}" y1="{mid - 6:.1f}" '
                   f'y2="{mid + 6:.1f}"/><line x1="{b:.1f}" x2="{b:.1f}" y1="{mid - 6:.1f}" '
                   f'y2="{mid + 6:.1f}"/></g>')
    out.append("</svg>")
    return "".join(out)


def spillover_map(geo: dict, values: dict[str, float], target: str, edges: list[float], *,
                  tips: dict[str, str], arrows: list[tuple[str, float]], input_id: str) -> str:
    """Each other area coloured by what it adds to `target`'s forecast; arrows from
    the biggest contributors, width by size."""
    out = [f'<svg class="chart map spill" viewBox="{geo["viewBox"]}" role="img" '
           f'aria-label="What each neighborhood adds to the selected one">',
           '<defs>'
           '<marker id="spill-up" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" '
           'markerHeight="4" orient="auto-start-reverse"><path class="head-up" d="M0,0L10,5L0,10Z"/></marker>'
           '<marker id="spill-down" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" '
           'markerHeight="4" orient="auto-start-reverse"><path class="head-down" d="M0,0L10,5L0,10Z"/></marker>'
           '</defs>']
    if geo.get("context"):
        out.append(f'<path class="context" d="{geo["context"]}"/>')
    for area, shape in geo["areas"].items():
        cls = "spill-target" if area == target else div_class(values.get(area, np.nan), edges)
        out.append(f'<path class="area {cls}" d="{shape["d"]}" fill-rule="evenodd" '
                   f'data-area="{esc(area)}" data-input="{input_id}" '
                   f'data-tip="{esc(tips.get(area, area))}" tabindex="0"/>')
    if target in geo["areas"]:
        out.append(f'<path class="area-outline" d="{geo["areas"][target]["d"]}" fill-rule="evenodd"/>')
    top = max([abs(v) for _, v in arrows] + [1e-9])
    tx, ty = geo["areas"][target]["c"] if target in geo["areas"] else (0, 0)
    for source, value in arrows:
        if source not in geo["areas"]:
            continue
        sx, sy = geo["areas"][source]["c"]
        dx, dy = tx - sx, ty - sy
        dist = math.hypot(dx, dy) or 1
        # Stop short of both centroids; bow the line so arrows into one target fan out.
        ex, ey = tx - dx / dist * 12, ty - dy / dist * 12
        bx, by = sx + dx / dist * 8, sy + dy / dist * 8
        cx, cy = (bx + ex) / 2 - dy * 0.18, (by + ey) / 2 + dx * 0.18
        kind = "up" if value > 0 else "down"
        out.append(f'<path class="spill-arrow {kind}" d="M{bx:.1f},{by:.1f}Q{cx:.1f},{cy:.1f} '
                   f'{ex:.1f},{ey:.1f}" stroke-width="{1.5 + 4.5 * abs(value) / top:.1f}" '
                   f'marker-end="url(#spill-{kind})"/>')
    out.append(f'<circle class="spill-dot" cx="{tx}" cy="{ty}" r="5"/>')
    out.append("</svg>")
    return "".join(out)


def driver_matrix(table: pd.DataFrame, drivers: list[str], heads: dict[str, str], *,
                  names: dict[str, str], edges: list[float], fmt, tips: dict, selected: str | None,
                  input_id: str, width: int = 760) -> str:
    """Neighborhoods x drivers, each cell coloured by its push. Rows are clickable;
    the right column is the forecast against a usual week."""
    L, R, T, row_h = 168, 118, 30, 26
    height = T + len(table) * row_h + 6
    cell_w = (width - L - R) / len(drivers)
    out = [f'<svg class="chart matrix" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="What drives each neighborhood\'s forecast">']
    for j, d in enumerate(drivers):
        out.append(f'<text class="col-head" x="{L + (j + 0.5) * cell_w:.1f}" y="{T - 10}" '
                   f'text-anchor="middle">{esc(heads[d])}</text>')
    out.append(f'<text class="col-head" x="{width - 6}" y="{T - 10}" text-anchor="end">'
               f'forecast (vs usual)</text>')
    for i, (area, row) in enumerate(table.iterrows()):
        y = T + i * row_h
        sel = " selected" if area == selected else ""
        out.append(f'<g class="mx-row{sel}" data-area="{esc(area)}" data-input="{input_id}" tabindex="0">'
                   f'<rect class="mx-hit" x="0" y="{y}" width="{width}" height="{row_h}"/>'
                   f'<text class="row-label" x="{L - 10}" y="{y + row_h / 2 + 4:.1f}" '
                   f'text-anchor="end">{esc(names.get(area, area))}</text>')
        for j, d in enumerate(drivers):
            v = row.get(d, np.nan)
            out.append(f'<rect class="mx-cell {div_class(v, edges)}" x="{L + j * cell_w + 1:.1f}" '
                       f'y="{y + 1}" width="{cell_w - 2:.1f}" height="{row_h - 2}" rx="3" '
                       f'data-tip="{esc(tips[(area, d)])}"/>')
        delta = row["total"] - row["base"]
        out.append(f'<text class="mx-total" x="{width - 6}" y="{y + row_h / 2 + 4:.1f}" '
                   f'text-anchor="end">{esc(fmt(row["total"]))} '
                   f'<tspan class="mx-delta">({esc(signed(delta, fmt))})</tspan></text></g>')
    out.append("</svg>")
    return "".join(out)


def driver_timeline(hist: pd.DataFrame, drivers: list[str], heads: dict[str, str], labels: dict, *,
                    edges: list[float], fmt, unit: str, latest, width: int = 760) -> str:
    """Top: the forecast for each week (made `h` weeks earlier) against a usual week
    and what happened. Below, aligned, one strip per driver: what pushed it."""
    hist = hist.dropna(subset=["output"])
    dates = list(hist["target_date"])
    top_h, strip_h = 150, 17
    height = top_h + 18 + strip_h * len(drivers) + 22
    vals = list(hist["output"]) + list(hist["base"]) + [v for v in hist["actual"] if np.isfinite(v)]
    fr = Frame(width, height, dates[0] - pd.Timedelta(days=4), dates[-1] + pd.Timedelta(days=4),
               max(vals) * 1.08, left=96, right=16, top=14, bottom=height - top_h)
    out = [f'<svg class="chart timeline" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="What drove the forecast each week this season">', fr.grid(unit)]
    usual = [(fr.x(d), fr.y(v)) for d, v in zip(dates, hist["base"])]
    fc = [(fr.x(d), fr.y(v)) for d, v in zip(dates, hist["output"])]
    out.append(f'<path class="line usual" d="{_path(usual)}"/>')
    out.append(f'<path class="line forecast" d="{_path(fc)}"/>')
    for d, v in zip(dates, hist["actual"]):
        if np.isfinite(v):
            out.append(f'<circle class="dot actual" cx="{fr.x(d):.1f}" cy="{fr.y(v):.1f}" r="3.5"/>')
    # Direct labels at the start of the season, clear of the latest week.
    above = usual[0][1] <= fc[0][1]
    out.append(f'<text class="direct" x="{fc[0][0]:.1f}" y="{fc[0][1] + (16 if above else -9):.1f}">'
               f'forecast</text>')
    out.append(f'<text class="direct muted" x="{usual[0][0]:.1f}" '
               f'y="{usual[0][1] + (-9 if above else 16):.1f}">usual week</text>')
    step = (fr.x(dates[1]) - fr.x(dates[0])) if len(dates) > 1 else 20
    y0 = top_h + 18
    for i, d in enumerate(drivers):
        y = y0 + i * strip_h
        out.append(f'<text class="row-label" x="{fr.l - 8}" y="{y + 12}" text-anchor="end">'
                   f'{esc(heads[d])}</text>')
        for date_, v in zip(dates, hist[d]):
            out.append(f'<rect class="mx-cell {div_class(v, edges)}" x="{fr.x(date_) - step / 2 + 1:.1f}" '
                       f'y="{y + 1}" width="{max(step - 2, 2):.1f}" height="{strip_h - 2}" rx="2"/>')
    bottom = y0 + strip_h * len(drivers)
    for (origin, r), d in zip(hist.iterrows(), dates):
        lines = [f"Week of {_date(d)}, forecast on {_date(origin)}",
                 f"Forecast: {fmt(r['output'])}", f"Usual week: {fmt(r['base'])}"]
        if np.isfinite(r["actual"]):
            lines.append(f"Reported: {fmt(r['actual'])}")
        lines += [f"{labels[k][0]}: {signed(r[k], fmt)}" for k in drivers if np.isfinite(r[k])]
        x = fr.x(d)
        cls = " latest" if origin == latest else ""
        out.append(f'<g class="col{cls}" data-tip="{esc(chr(10).join(lines))}">'
                   f'<rect class="hit" x="{x - step / 2:.1f}" y="{fr.t}" width="{step:.1f}" '
                   f'height="{bottom - fr.t:.1f}"/><line class="guide" x1="{x:.1f}" x2="{x:.1f}" '
                   f'y1="{fr.t}" y2="{bottom:.1f}"/></g>')
    out.append("</svg>")
    return "".join(out)


# --- how severe the season is -----------------------------------------------------------
# Class colours are the status tokens the level pills use, so "High" looks the same
# on a pill, a bar and a cell; the class name is always printed beside it.

SEV_LINES = (("IT50", "Moderate"), ("IT90", "High"), ("IT98", "Very high"))


def chance(p: float) -> str:
    """A probability read off the 1%-99% quantiles: never claims more than that."""
    if not np.isfinite(p):
        return "—"
    return "<1%" if p <= 0.0101 else ">99%" if p >= 0.9899 else f"{p:.0%}"


def severity_strip(table: pd.DataFrame, its: dict[str, float], *, fmt, unit: str,
                   notes: dict[str, str] | None = None,
                   outlook: tuple[float, float, float, str] | None = None,
                   width: int = 760) -> str:
    """Every season's peak week against the severity lines, the four classes as
    faint zones behind. The current season adds, hollow, the forecast's highest
    median in the weeks ahead, with its 95% range: (median, low, high, when)."""
    notes = notes or {}
    L, R, T, row_h, bar_h = 104, 96, 26, 26, 14
    n = len(table)
    bottom = T + n * row_h
    height = bottom + 24
    vals = list(table["peak"]) + list(its.values()) + (list(outlook[:3]) if outlook else [])
    hi = nice_ticks(max(vals) * 1.05)[-1]
    X = lambda v: L + min(max(v, 0), hi) / hi * (width - L - R)
    out = [f'<svg class="chart severity" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Every season\'s peak against the severity lines">']
    edges = [0.0] + [its[k] for k, _ in SEV_LINES] + [hi]
    for i, lvl in enumerate(LEVELS):
        a, b = X(edges[i]), X(edges[i + 1])
        out.append(f'<rect class="sev-zone sev-{LEVEL_STATUS[lvl]}" x="{a:.1f}" y="{T}" '
                   f'width="{b - a:.1f}" height="{n * row_h}"/>'
                   f'<text class="tick sev-name" x="{(a + b) / 2:.1f}" y="{T - 8}" '
                   f'text-anchor="middle">{esc(lvl)}</text>')
    out.append(f'<line class="axis" x1="{L}" x2="{width - R}" y1="{bottom}" y2="{bottom}"/>'
               f'<text class="tick" x="{L}" y="{bottom + 14}" text-anchor="middle">0</text>')
    for key, _ in SEV_LINES:
        x = X(its[key])
        out.append(f'<line class="sev-line" x1="{x:.1f}" x2="{x:.1f}" y1="{T - 2}" y2="{bottom}"/>'
                   f'<text class="tick strong" x="{x:.1f}" y="{bottom + 14}" '
                   f'text-anchor="middle">{esc(fmt(its[key]))}</text>')
    out.append(f'<text class="tick" x="{width - R}" y="{bottom + 14}" text-anchor="start" '
               f'dx="8">{esc(unit)}</text>')
    for i, r in enumerate(table.itertuples()):
        y = T + i * row_h
        mid = y + row_h / 2
        now = r.role == "current"
        cls = "sev-skip" if r.role == "skipped" else f"sev-{LEVEL_STATUS[r.cls]}"
        lines = [r.season + (", so far" if now else ""),
                 f"Peak {fmt(r.peak)} {unit}, week of {_date(r.peak_date)}",
                 f"{r.cls}" + (" so far" if now else "")]
        if r.season in notes:
            lines.append(notes[r.season])
        if now and outlook:
            med, lo, up, when = outlook
            lines.append(f"Forecast high {when}: {fmt(med)} (95% range {fmt(lo)}–{fmt(up)})")
        end = X(r.peak)
        parts = [f'<g class="sev-row{" now" if now else ""}" data-tip="{esc(chr(10).join(lines))}">',
                 f'<rect class="hit" x="0" y="{y}" width="{width}" height="{row_h}"/>',
                 f'<text class="row-label{" strong" if now else ""}" x="{L - 10}" y="{mid + 4:.1f}" '
                 f'text-anchor="end">{esc(r.season)}</text>',
                 f'<rect class="sev-bar {cls}" x="{L}" y="{mid - bar_h / 2:.1f}" '
                 f'width="{max(end - L, 2):.1f}" height="{bar_h}" rx="3"/>']
        text = fmt(r.peak)
        if now and outlook:
            if X(med) > end:
                parts.append(f'<rect class="sev-ahead" x="{end:.1f}" y="{mid - bar_h / 2 + 1:.1f}" '
                             f'width="{X(med) - end:.1f}" height="{bar_h - 2}" rx="3"/>')
            a, b = X(lo), X(up)
            parts.append(f'<g class="sev-whisker"><line x1="{a:.1f}" x2="{b:.1f}" y1="{mid:.1f}" '
                         f'y2="{mid:.1f}"/><line x1="{b:.1f}" x2="{b:.1f}" y1="{mid - 5:.1f}" '
                         f'y2="{mid + 5:.1f}"/></g>')
            end = max(end, X(med), b)
            text = f"{fmt(r.peak)} → {fmt(med)}" if med > r.peak else fmt(r.peak)
        parts.append(f'<text class="sev-val" x="{end + 6:.1f}" y="{mid + 4:.1f}">{esc(text)}</text></g>')
        out.append("".join(parts))
    out.append("</svg>")
    return "".join(out)


def odds_grid(probs: pd.DataFrame, weeks: list[str], *, width: int = 560) -> str:
    """Chance of each forecast week being above each severity line: rows are the
    lines, columns the weeks ahead; the cell fills with the chance."""
    L, T, row_h = 150, 26, 34
    cols = len(probs)
    cw = (width - L - 8) / max(cols, 1)
    height = T + row_h * len(SEV_LINES) + 6
    out = [f'<svg class="chart odds" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Chance of crossing each severity line">']
    for j, w in enumerate(weeks):
        out.append(f'<text class="tick" x="{L + (j + 0.5) * cw:.1f}" y="{T - 9}" '
                   f'text-anchor="middle">{esc(w)}</text>')
    for i, (key, name) in enumerate(SEV_LINES):
        y = T + i * row_h
        out.append(f'<text class="row-label" x="{L - 10}" y="{y + row_h / 2 + 4:.1f}" '
                   f'text-anchor="end">Above {esc(name.lower())}</text>')
        for j, (h, p) in enumerate(probs[key].items()):
            x = L + j * cw
            tip = f"{name} line, week of {weeks[j]}&#10;{chance(p)} chance the citywide average is above it"
            out.append(f'<g data-tip="{tip}"><rect class="odds-cell sev-{LEVEL_STATUS[name]}" '
                       f'x="{x + 2:.1f}" y="{y + 2}" width="{cw - 4:.1f}" height="{row_h - 4}" rx="4" '
                       f'fill-opacity="{0.06 + 0.6 * p:.2f}"/><text class="odds-val" '
                       f'x="{x + cw / 2:.1f}" y="{y + row_h / 2 + 4:.1f}" text-anchor="middle">'
                       f'{esc(chance(p))}</text></g>')
    out.append("</svg>")
    return "".join(out)


def severity_grid(tables: dict[str, pd.DataFrame], *, names: dict[str, str], fmt, unit: str,
                  input_id: str, selected: str | None = None, width: int = 760) -> str:
    """Neighborhoods x seasons: each cell is that season's class against the
    neighborhood's own lines. `tables` is season_severity() per area; seasons left
    out of the lines are left out here too, and the current one reads "so far"."""
    first = next(iter(tables.values()))
    seasons = list(first.loc[first["role"] != "skipped", "season"])
    L, T, row_h = 150, 24, 24
    cw = (width - L - 8) / len(seasons)
    height = T + row_h * len(tables) + 6
    short = {lvl: abbr for lvl, abbr in zip(LEVELS, ("L", "M", "H", "VH"))}
    out = [f'<svg class="chart matrix sevgrid" viewBox="0 0 {width} {height}" role="img" '
           f'aria-label="Each neighborhood\'s seasons against its own severity lines">']
    for j, s in enumerate(seasons):
        now = j == len(seasons) - 1 and first.iloc[-1]["role"] == "current"
        out.append(f'<text class="col-head{" strong" if now else ""}" x="{L + (j + 0.5) * cw:.1f}" '
                   f'y="{T - 8}" text-anchor="middle">{esc(s + (" so far" if now else ""))}</text>')
    for i, (area, table) in enumerate(tables.items()):
        y = T + i * row_h
        rows = table.set_index("season")
        sel = " selected" if area == selected else ""
        out.append(f'<g class="mx-row{sel}" data-area="{esc(area)}" data-input="{esc(input_id)}" '
                   f'tabindex="0"><rect class="mx-hit" x="0" y="{y}" width="{width}" '
                   f'height="{row_h}" rx="4"/><text class="row-label" x="{L - 10}" '
                   f'y="{y + row_h / 2 + 4:.1f}" text-anchor="end">{esc(names[area])}</text>')
        for j, s in enumerate(seasons):
            if s not in rows.index or rows.at[s, "cls"] is None:
                continue
            r = rows.loc[s]
            now = r["role"] == "current"
            tip = (f"{names[area]}, {s}{', so far' if now else ''}\n{r['cls']} against its own "
                   f"lines\nPeak {fmt(r['peak'])} {unit}, week of {_date(r['peak_date'])}")
            out.append(f'<g data-tip="{esc(tip)}"><rect class="odds-cell sev-{LEVEL_STATUS[r["cls"]]}'
                       f'{" now" if now else ""}" x="{L + j * cw + 2:.1f}" y="{y + 2}" '
                       f'width="{cw - 4:.1f}" height="{row_h - 4}" rx="3"/><text class="odds-val" '
                       f'x="{L + (j + 0.5) * cw:.1f}" y="{y + row_h / 2 + 4:.1f}" '
                       f'text-anchor="middle">{short[r["cls"]]}</text></g>')
        out.append("</g>")
    out.append("</svg>")
    return "".join(out)
