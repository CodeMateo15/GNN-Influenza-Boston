# Generated copy of boston-flu-outlook/app.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Boston Flu Outlook: neighborhood flu forecasts, 1-4 weeks ahead, for BPHC.

    shiny run --reload app.py

Reads only the precomputed files in data/ (publish.py writes them from the live
forecast archive), so the app needs no model code and starts in about a second.
One audience selector decides which tabs exist and how much of the scoring is
shown; everything else is shared.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from shiny import App, reactive, render, ui

from core import charts as C
from core import data as D
from core import vocab as V

# Resolved from this file, not the working directory: the deploy target does
# not necessarily launch the app from its own folder.
APP_DIR = Path(__file__).parent
B, CHI = D.BOSTON, D.CHICAGO

# Same theme persistence as the NCAA app: restore the stored choice before first
# paint, re-apply after the dark-mode component upgrades, then save changes.
THEME_SCRIPT = """
(function () {
  var KEY = "flu-outlook-theme";
  var root = document.documentElement;
  var read = function () {
    try { return window.localStorage.getItem(KEY); } catch (e) { return null; }
  };
  var stored = read();
  var initial = (stored === "dark" || stored === "light") ? stored : "light";
  root.setAttribute("data-bs-theme", initial);
  window.addEventListener("load", function () {
    if (root.getAttribute("data-bs-theme") !== initial) {
      root.setAttribute("data-bs-theme", initial);
    }
    new MutationObserver(function () {
      var mode = root.getAttribute("data-bs-theme");
      if (mode !== "dark" && mode !== "light") return;
      try { window.localStorage.setItem(KEY, mode); } catch (e) {}
    }).observe(root, { attributes: true, attributeFilter: ["data-bs-theme"] });
  });
})();
"""

SHORT_AREA = {"Back Bay/Beacon Hill/Downtown/North End/West End": "Back Bay & Downtown",
              "Allston/Brighton": "Allston-Brighton"}


def short(city: D.CityData, area: str) -> str:
    return SHORT_AREA.get(area, area) if city.key == "boston" else f"ZIP {area}"


def date(d) -> str:
    return pd.Timestamp(d).strftime("%b %-d")


def week_end(d) -> str:
    """BPHC and CDPH label a week by its Sunday; it runs through the Saturday after."""
    return date(pd.Timestamp(d) + pd.Timedelta(days=6))


def week_span(d) -> str:
    start, end = pd.Timestamp(d), pd.Timestamp(d) + pd.Timedelta(days=6)
    return f"{date(start)}–{end.day if end.month == start.month else date(end)}"


def duration(seconds: float) -> str:
    if not np.isfinite(seconds):
        return "—"
    seconds = round(seconds)
    if seconds < 60:
        return f"{max(seconds, 1)} s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} min {seconds} s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours} h {minutes} min"


def map_bins(city: D.CityData) -> list[float]:
    recent = city.history.iloc[-104:].to_numpy().ravel().tolist()
    return C.bins_for(recent + city.forecast["predicted"].tolist(), city.info.get("cap"))


BINS = {k: map_bins(c) for k, c in D.CITIES.items()}


# --- small pieces -----------------------------------------------------------------

def tile(label: str, value, sub: str | None = None):
    return ui.div(ui.div(label, class_="tile-label"), ui.div(value, class_="tile-value"),
                  ui.div(sub or "", class_="tile-sub"), class_="tile")


def level_pill(level: str | None):
    if not level:
        return ui.span("not reported", class_="pill pill-sm pill-none")
    return ui.span(level, class_=f"pill pill-sm pill-{D.LEVEL_STATUS[level]}")


def trust_badge(verdict: str):
    text, status, icon = V.VERDICT.get(verdict, (verdict, "warning", "?"))
    return ui.span(f"{icon} {text}", class_=f"trust trust-{status}")


def legend(models: list[str], bands: bool = True, observed: bool = True):
    keys = []
    if observed:
        keys.append(ui.span(ui.span(class_="sw obs"), "Reported", class_="key"))
    # Same rule as C.fan_chart: the bands belong to the first model that is not
    # "same as last week". data-series lets the offline copy (export_html.py) hide
    # a model's keys when its box is unticked.
    banded = next((m for m in models if m != "persistence"), None)
    for m in models:
        cls = D.MODEL_CLASS.get(m, "s1")
        keys.append(ui.span(ui.span(class_=f"sw {cls}"), D.MODEL_SHORT.get(m, m), class_="key",
                            **{"data-series": cls}))
        if m == banded and bands:
            keys.append(ui.span(ui.span(class_=f"sw-band {cls} b50"), "likely range (50%)",
                                class_="key", **{"data-series": cls}))
            keys.append(ui.span(ui.span(class_=f"sw-band {cls} b95"), "plausible range (95%)",
                                class_="key", **{"data-series": cls}))
    return ui.div(*keys, class_="legend")


def direction(change: float) -> tuple[str, str]:
    if not np.isfinite(change):
        return "—", "hold"
    if change > 0.15:
        return "↑", "rise"
    if change < -0.15:
        return "↓", "fall"
    return "→", "hold steady"


def preview_banner(city: D.CityData):
    if not city.preview:
        return None
    return ui.div(ui.tags.b("Preview numbers."),
                  f"These {city.label} forecasts come from a quick test run (tiny models, "
                  f"data through {week_end(city.origin)}), not the production run. They show "
                  "how the page works; don't quote them.", class_="banner")


# --- blocks shared by Boston and Chicago -----------------------------------------------

def map_block(city: D.CityData, h: int, selected: str | None, input_id: str):
    values = city.at(D.PRIMARY, h)
    latest = city.latest()
    rows = city.rows(D.PRIMARY)
    tips = {}
    for area in city.areas:
        v = values.get(area, np.nan)
        lines = [short(city, area)]
        if h == 0:
            lines.append(f"Reported {week_span(city.origin)}: {city.fmt(v)}")
        else:
            r = rows[(rows["area"] == area) & (rows["horizon"] == h)]
            if len(r):
                r = r.iloc[0]
                lines.append(f"Forecast for {week_span(r['target_date'])}: {city.fmt(r['predicted'])}")
                lines.append(f"95% range {city.fmt(r['lower'])}–{city.fmt(r['upper'])}")
                lines.append(f"Now: {city.fmt(latest.get(area))}")
        lvl = city.level(area, v)
        if lvl:
            lines.append(f"Level: {lvl}")
        lines.append("Click for details")
        tips[area] = "\n".join(lines)
    target = city.origin + pd.Timedelta(weeks=h)
    when = (f"<strong>Week of {date(target)}</strong> · reported" if h == 0 else
            f"<strong>Week of {date(target)}</strong> · forecast, {h} week{'s' if h > 1 else ''} ahead")
    svg = C.choropleth(city.geo, values.to_dict(), BINS[city.key], tips=tips, selected=selected,
                       input_id=input_id)
    return ui.div(ui.div(ui.HTML(when), class_="when"), ui.HTML(svg),
                  ui.HTML(C.legend_bins(BINS[city.key], city.fmt, city.info["unit_short"])))


def ranked_block(city: D.CityData, h: int, input_id: str, limit: int | None = None):
    values = city.at(D.PRIMARY, h)
    latest = city.latest()
    order = values.sort_values(ascending=False, na_position="last")
    top = max(order.max(), 1e-9)
    items = []
    for area, v in list(order.items())[:limit]:
        width = 0 if not np.isfinite(v) else max(2, 100 * v / top)
        change = (v / latest[area] - 1) if h and np.isfinite(v) and latest.get(area, 0) > 0 else np.nan
        chg = "" if not np.isfinite(change) else f"{change * 100:+.0f}%"
        lvl = city.level(area, v)
        items.append(ui.tags.li(
            ui.span(short(city, area), class_="nm"),
            ui.div(ui.div(class_="bar", style=f"width:{width:.0f}%"), class_="bar-track"),
            ui.span(city.fmt(v), class_="val"),
            ui.span(chg, class_="chg"),
            ui.span(level_pill(lvl), class_="lvl"),
            **{"data-area": area, "data-input": input_id, "tabindex": "0",
               "data-tip": f"{short(city, area)}\n{city.fmt(v)} {city.info['unit_short']}"
                           + (f"\n{chg} vs now" if chg else "")
                           + (f"\nLevel: {lvl}" if lvl else "")}))
    more = (ui.p(f"Top {limit} of {len(order)} shown; the map has them all.", class_="note")
            if limit and len(order) > limit else None)
    return ui.div(ui.tags.ul(*items, class_="ranked"), more)


def fan_block(city: D.CityData, area: str | None, models: list[str], title: str, blurb: str):
    hist = city.citywide() if area is None else city.history[area]
    if area is None:
        forecasts = {m: city.citywide_forecast(m) for m in models}
    else:
        forecasts = {m: city.rows(m, area) for m in models}
    svg = C.fan_chart(hist, forecasts, unit=city.info["unit_short"], fmt=city.fmt,
                      cap=city.info.get("cap"))
    return ui.div(ui.h3(title), ui.p(blurb, class_="blurb"), legend(models), ui.HTML(svg),
                  class_="chart-card")


RIBBON_SETS = {"all": "All seasons", "train": "Training seasons only"}


def season_span(labels: list[str]) -> str:
    labels = sorted(labels)
    return labels[0] if len(labels) == 1 else f"{labels[0]} to {labels[-1]}"


def ribbons_block(city: D.CityData, area: str | None, which: str = "all"):
    """The season-ribbon chart, its blurb and legend. The card and the
    all/training toggle live outside this, so the toggle keeps its state."""
    series = city.citywide() if area is None else city.history[area]
    seasons = city.seasons(series)
    current = city.season_label(city.origin)
    roles = city.season_roles()
    past = sorted(k for k in seasons if k != current)
    held = [k for k in past if roles.get(k) == "validation"]
    if which == "train" and roles:
        past = [k for k in past if roles.get(k) == "training"]
        seasons = {k: v for k, v in seasons.items() if k in past or k == current}
    start = pd.Timestamp(year=int(current[:4]), month=8, day=1)
    f = city.citywide_forecast(D.PRIMARY) if area is None else city.rows(D.PRIMARY, area)
    pts = [((pd.Timestamp(r.target_date) - start).days // 7, r.predicted) for r in f.itertuples()]
    svg = C.ribbons(seasons, current, pts, unit=city.info["unit_short"], fmt=city.fmt)
    where = "the city" if area is None else short(city, area)
    if which == "train" and roles:
        against = (f"only the seasons the model learned from ({season_span(past)})"
                   + (f". {', '.join(held)} was held back to decide when to stop training and "
                      "how wide to draw the forecast ranges, so it is left out here" if held else ""))
        key = "training seasons"
    else:
        against = f"every season since {past[0]}" if past else "past seasons"
        key = "past seasons"
    return ui.div(
        ui.p(f"{where} this season (blue, with the forecast as dots) against {against}. "
             "Past seasons are grey; hover one to name it. The x-axis counts weeks from 1 August.",
             class_="blurb"),
        ui.div(ui.span(ui.span(class_="sw s1"), f"{current}", class_="key"),
               ui.span(ui.span(class_="sw past"), key, class_="key"), class_="legend"),
        ui.HTML(svg))


def city_tiles(city: D.CityData):
    cw = city.citywide()
    now = cw.loc[:city.origin].dropna().iloc[-1]
    hmax = max(city.horizons)
    fc = city.citywide_forecast(D.PRIMARY).set_index("horizon")
    ahead = fc.loc[hmax]
    change = ahead["predicted"] / now - 1 if now > 0 else np.nan
    arrow, _ = direction(change)
    h_rise = 2 if 2 in city.horizons else hmax
    mid = city.at(D.PRIMARY, h_rise)
    latest = city.latest()
    # Up 10% and by a real amount: on Chicago's 1-10 scale a 1.0 -> 1.2 forecast
    # is noise, not a rise.
    floor = city.info.get("min_change", 0)
    rising = int(((mid > latest * 1.10) & (mid - latest >= floor) & (latest > 0)).sum())
    peak = city.typical_peak()
    words = city.info["areas_word"]
    return ui.div(
        tile("Citywide now", city.fmt(now),
             f"average of {len(city.areas)} {words}, week of {week_span(city.origin)}"),
        tile(f"In {hmax} weeks", f"{arrow} {city.fmt(ahead['predicted'])}",
             f"{change * 100:+.0f}% · 95% range {city.fmt(ahead['lower'])}–{city.fmt(ahead['upper'])}"
             if np.isfinite(change) else ""),
        tile(f"{words.capitalize()} rising", f"{rising} of {len(city.areas)}",
             f"forecast up more than 10% in {h_rise} weeks"
             + (f" (and by {city.fmt(floor)}+)" if floor else "")),
        tile("Against a typical peak", f"{100 * now / peak:.0f}%" if np.isfinite(peak) else "—",
             f"of a typical season's peak ({city.fmt(peak)})"),
        class_="tiles")


def headline(city: D.CityData) -> str:
    cw = city.citywide()
    now = cw.loc[:city.origin].dropna().iloc[-1]
    hmax = max(city.horizons)
    ahead = city.citywide_forecast(D.PRIMARY).set_index("horizon").loc[hmax]
    _, verb = direction(ahead["predicted"] / now - 1 if now > 0 else np.nan)
    share = now / city.typical_peak()
    return (f"Flu-like illness in {city.label} is at <strong>{share:.0%} of a typical season's "
            f"peak</strong> and is expected to <strong>{verb}</strong> over the next {hmax} weeks.")


# --- what drove the forecast -------------------------------------------------------------

# How each driver reads inside a sentence.
DRIVER_PHRASE = {"level": "this week's reading", "trend": "the three weeks before it",
                 "history": "earlier weeks", "weather": "the weather",
                 "calendar": "the time of year", "neighbor": "neighboring areas"}


def notable(steps, floor: float = 0.1) -> list[tuple[str, float, float]]:
    """Drivers big enough to mention: clear of their sampling error and of rounding."""
    return sorted([s for s in steps if abs(s[1]) >= max(2 * s[2], floor)],
                  key=lambda s: -abs(s[1]))


def neighbor_names(city: D.CityData, nbr: pd.Series, n: int = 2) -> str:
    names = [short(city, a) for a, v in nbr.items() if abs(v) >= 0.05][:n]
    return " and ".join(names)


def driver_sentence(city: D.CityData, area: str, h: int, wf: dict) -> str:
    total, base = wf["total"], wf["base"]
    gap = total - base
    where = "above" if gap > 0 else "below"
    head = (f"<strong>{short(city, area)}</strong>, {h} week{'s' if h > 1 else ''} ahead "
            f"(week of {week_span(wf['target_date'])}): the graph model expects "
            f"<strong>{city.fmt(total)}</strong> {city.info['unit_short']}, "
            f"<strong>{city.fmt(abs(gap))} {where}</strong> a usual week at this time of year "
            f"({city.fmt(base)}). ")
    top = notable(wf["steps"])[:3]
    if not top:
        return head + "No single input moves it far from a usual week."
    parts = []
    for key, value, _ in top:
        text = f"{DRIVER_PHRASE[key]} ({C.signed(value, city.fmt)})"
        if key == "neighbor":
            names = neighbor_names(city, wf["neighbors"])
            text += f", mostly {names}" if names else ""
        parts.append(text)
    lead = top[0]
    verb = "pushes it up" if lead[1] > 0 else "pulls it down"
    rest = (f", followed by {' and '.join(parts[1:])}" if len(parts) > 1 else "")
    return head + f"The biggest factor, {parts[0]}, {verb}{rest}."


def driver_teaser(city: D.CityData, area: str) -> str | None:
    """One line for the Neighborhood tab: what is behind next week's number."""
    if not city.has_drivers:
        return None
    wf = city.waterfall(area, min(city.horizons))
    top = notable(wf["steps"])[:2]
    if not top:
        return "Behind next week's number: nothing far from a usual week at this time of year."
    bits = [f"{DRIVER_PHRASE[k]} ({C.signed(v, city.fmt)})" for k, v, _ in top]
    return (f"Behind next week's number, against a usual week at this time of year "
            f"({city.fmt(wf['base'])}): mostly {' and '.join(bits)}.")


def waterfall_block(city: D.CityData, area: str, h: int, analyst: bool):
    wf = city.waterfall(area, h)
    unit = city.info["unit_short"]
    rows = []
    for key, value, se in wf["steps"]:
        name, _, meaning = V.DRIVER_LABELS[key]
        sub = ""
        if key == "neighbor":
            top = [(a, v) for a, v in wf["neighbors"].items() if abs(v) >= 0.05][:2]
            sub = ", ".join(f"{short(city, a)} {C.signed(v, city.fmt)}" for a, v in top)
        noise = f" (± {se:.2f} from sampling)" if se >= 0.01 else ""
        tip = f"{name}\n{C.signed(value, city.fmt)} {unit}{noise}\n{meaning}"
        rows.append({"label": name, "sub": sub, "value": value, "se": se, "tip": tip})
    if abs(wf["adjust"]) >= 0.005 or analyst:
        name, _, meaning = V.DRIVER_LABELS["adjust"]
        rows.append({"label": name, "sub": "", "value": wf["adjust"], "se": 0.0,
                     "tip": f"{name}\n{C.signed(wf['adjust'], city.fmt)} {unit}\n{meaning}"})
    r = city.rows(D.PRIMARY, area)
    r = r[r["horizon"] == h]
    whisker = (float(r["q0.250"].iloc[0]), float(r["q0.750"].iloc[0])) if len(r) else None
    base_tip = (f"{V.BASE_LABEL}\n{city.fmt(wf['base'])} {unit}\nWhat the model forecasts when "
                "every input is at its average for the same weeks of the year in the seasons it "
                "learned from (2018 to spring 2026).")
    total_tip = (f"Forecast (graph model median)\n{city.fmt(wf['total'])} {unit}"
                 + (f"\nLikely range (50%): {city.fmt(whisker[0])}–{city.fmt(whisker[1])}"
                    if whisker else ""))
    svg = C.waterfall(rows, base=wf["base"], total=wf["total"], base_label="Usual week",
                      total_label="Forecast", fmt=city.fmt, unit=unit, whisker=whisker,
                      base_tip=base_tip, total_tip=total_tip)
    return ui.div(
        ui.h3("From a usual week to this forecast"),
        ui.p("Start at what the model would forecast for a usual week at this time of year, "
             "then add what each input pushes up (warm) or pulls down (cool). The bars add up "
             "exactly to the forecast; the whisker on it is the likely (50%) range. Hover a "
             "bar for what it means.", class_="blurb"),
        ui.div(ui.span(ui.span(class_="sw-box wf-up"), "pushes the forecast up", class_="key"),
               ui.span(ui.span(class_="sw-box wf-down"), "pulls it down", class_="key"),
               class_="legend"),
        ui.HTML(svg), class_="card")


def spill_block(city: D.CityData, area: str, h: int, input_id: str):
    values = city.spillover(area, h)
    every = city.drivers
    every = every[(every["origin_date"] == city.origin) & (every["horizon"] == h)
                  & (every["driver"] == "neighbor")]["value"]
    edges = C.div_edges(every)
    unit = city.info["unit_short"]
    tips = {}
    for a in city.areas:
        if a == area:
            tips[a] = f"{short(city, a)}\nThe neighborhood being forecast"
            continue
        v = values.get(a, np.nan)
        verb = "adds" if v >= 0 else "takes off"
        tips[a] = (f"{short(city, a)}\n{verb} {city.fmt(abs(v))} {unit} to "
                   f"{short(city, area)}'s forecast\nClick to explain {short(city, a)} instead")
    arrows = [(a, v) for a, v in values.sort_values(key=abs, ascending=False).items()
              if abs(v) >= edges[0]][:3]
    svg = C.spillover_map(city.geo, values.to_dict(), area, edges, tips=tips, arrows=arrows,
                          input_id=input_id)
    total = values.sum()
    return ui.div(
        ui.h3("Spillover from other neighborhoods"),
        ui.p(f"How much each neighborhood's recent weeks move {short(city, area)}'s forecast "
             f"(outlined), {C.signed(total, city.fmt)} in all. Arrows mark the three biggest. "
             "Click any neighborhood to explain it instead.", class_="blurb"),
        ui.HTML(svg), ui.HTML(C.legend_div(edges, city.fmt, unit)), class_="card")


def matrix_block(city: D.CityData, area: str, h: int, input_id: str):
    table = city.driver_matrix(h)
    table = table.assign(_gap=table["total"] - table["base"]).sort_values("_gap", ascending=False)
    drivers = list(D.DRIVERS)
    edges = C.div_edges(table[drivers].to_numpy().ravel())
    unit = city.info["unit_short"]
    tips = {(a, d): f"{short(city, a)} · {V.DRIVER_LABELS[d][0]}\n"
                    f"{C.signed(row[d], city.fmt)} {unit}\n{V.DRIVER_LABELS[d][2]}"
            for a, row in table.iterrows() for d in drivers}
    svg = C.driver_matrix(table, drivers, {d: V.DRIVER_LABELS[d][1] for d in drivers},
                          names={a: short(city, a) for a in city.areas}, edges=edges,
                          fmt=city.fmt, tips=tips, selected=area, input_id=input_id)
    return ui.div(
        ui.h3("Every neighborhood, side by side"),
        ui.p(f"Each row is one neighborhood's forecast {h} week{'s' if h > 1 else ''} ahead, "
             "split the same way, highest above a usual week first. Read down a column: a "
             "rise that shows up under “This week” and “Recent weeks” everywhere is local "
             "momentum across the city; one that shows up under “Neighbors” is the model "
             "expecting spread. Click a row to explain it.", class_="blurb"),
        ui.HTML(svg), ui.HTML(C.legend_div(edges, city.fmt, unit)), class_="chart-card")


def timeline_block(city: D.CityData, area: str, h: int):
    hist = city.driver_history(area, h)
    if len(hist) < 2:
        return None
    drivers = list(D.DRIVERS)
    edges = C.div_edges(hist[drivers].to_numpy().ravel())
    svg = C.driver_timeline(hist, drivers, {d: V.DRIVER_LABELS[d][1] for d in drivers},
                            V.DRIVER_LABELS, edges=edges, fmt=city.fmt,
                            unit=city.info["unit_short"], latest=city.origin)
    first = hist.index.min()
    return ui.div(
        ui.h3("What drove it, week by week"),
        ui.p(f"Every {h}-week forecast the same saved model would have made for "
             f"{short(city, area)} since {date(first)} (the model never saw these weeks while "
             "training). Top: the forecast for each week against a usual week and what BPHC "
             "then reported. Below: which inputs pushed each one, in the same colours. Hover a "
             "week for the numbers.", class_="blurb"),
        ui.div(ui.span(ui.span(class_="sw obs"), "forecast", class_="key"),
               ui.span(ui.span(class_="sw usual"), "usual week", class_="key"),
               ui.span(ui.span(class_="sw-ring"), "reported", class_="key"), class_="legend"),
        ui.HTML(svg), ui.HTML(C.legend_div(edges, city.fmt, city.info["unit_short"])),
        class_="chart-card")


def method_block(city: D.CityData, area: str, h: int, analyst: bool):
    wf = city.waterfall(area, h)
    caveat = ui.p("These numbers describe what the model responds to, not what causes flu to "
                  "spread: a big “Neighbors” bar means the model reads its neighbors' recent "
                  "weeks as a signal, which is what it was built to do, not proof that illness "
                  "travelled between them.", class_="note")
    if not analyst:
        return ui.div(caveat, class_="card")
    meta = city.meta.get("frozen_models") or {}
    return ui.div(
        ui.h3("Method"),
        ui.tags.ul(
            ui.tags.li("Owen values (Shapley values with the other neighborhoods as one group, "
                       "split again between them) of the frozen graph-model ensemble, in rate "
                       "units. They add up exactly to the forecast minus the base."),
            ui.tags.li("Base: every input set to its mean over training origins within four "
                       "weeks of the same date. Inputs set to typical values while correlated "
                       "ones keep this week's form combinations the model never saw; read small "
                       "values with that in mind."),
            ui.tags.li("Estimated from sampled orderings (256 this week, 128 for earlier "
                       "weeks), each with its reverse. Hover a bar for its sampling error."),
            ui.tags.li(f"The model puts {wf['blend_share']:.0%} of its own baseline on this "
                       f"week's level and {1 - wf['blend_share']:.0%} on the seasonal curve at "
                       f"{h} week{'s' if h > 1 else ''} ahead; the network adds the rest."),
            ui.tags.li(f"“Averaging model runs” is {C.signed(wf['adjust'], city.fmt)} here: "
                       "the published median is the mean of MC-Dropout draws; this explains the "
                       "deterministic ensemble mean."),
            ui.tags.li(f"Saved models trained on weeks before {meta.get('anchor', 'the season')}"
                       f", loaded unchanged each week.")),
        caveat, class_="card")


# --- UI -------------------------------------------------------------------------------

def live_slider(id: str, label: str, lo: int, hi: int, value: int, interval: int):
    return ui.input_slider(id, label, lo, hi, value, step=1, ticks=True,
                           animate=ui.AnimationOptions(interval=interval, loop=False))


def topbar(theme=None):
    """`theme` replaces the dark-mode switch (export_html.py passes a plain button,
    since the switch is a bslib web component that needs the Shiny runtime)."""
    chips =[ui.span(ui.HTML(f"BPHC data through <strong>{week_end(B.origin)}</strong>"), class_="chip"),
             ui.span(ui.HTML(f"Forecast issued <strong>{date(B.meta.get('issued', B.origin))}</strong>"),
                     class_="chip"),
             ui.span(f"{len(B.meta.get('archived_origins', [1]))} weekly forecast(s) on record",
                     class_="chip")]
    return ui.div(
        ui.div(ui.h1(ui.span(class_="brand-mark"), "Boston Flu Outlook", class_="brand"),
               ui.p("Neighborhood flu forecasts for the next four weeks, built on how "
                    "illness spreads between neighboring areas.", class_="brand-sub"),
               ui.div(*chips, class_="fresh"), class_="brand-block"),
        ui.div(ui.input_select("audience", "I am viewing as", V.MODES, selected="briefing"),
               ui.div(ui.tags.label("Theme", class_="theme-label"),
                      theme if theme is not None else ui.input_dark_mode(id="theme", mode="light"),
                      class_="theme-block"),
               class_="audience-block"),
        class_="topbar")


def footer():
    return ui.div(
        ui.span(f"Forecast origin {B.meta['origin']}", class_="version-chip"),
        "Experimental research forecasts from the GNN-Influenza-Boston project at "
        "Northeastern University, built on the Boston Public Health Commission's public "
        "dashboard data. Not an official BPHC product, and not medical advice. Forecasts "
        "are archived unchanged every week and scored against what actually happened.",
        class_="disclaimer")


app_ui = ui.page_fluid(
    ui.head_content(
        ui.tags.title("Boston Flu Outlook"),
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.include_css(APP_DIR / "www" / "styles.css"),
        ui.tags.script(THEME_SCRIPT),
        ui.include_js(APP_DIR / "www" / "app.js"),
    ),
    topbar(),
    ui.output_ui("tabs"),
    footer(),
)


# --- tab shell -----------------------------------------------------------------------

def build_tabs(m: str, area: str, ribbon_set: str = "all", *, out=ui.output_ui,
               slider=live_slider, download=ui.download_button, table_out=ui.output_data_frame):
    """Every tab for one audience. The server passes Shiny's output placeholders;
    export_html.py passes pre-rendered content for each one, so the offline copy is
    built from this same layout."""
    hmax_b = max(B.horizons)
    panels = {
        "outlook": ui.nav_panel(
            V.TAB_TITLES["outlook"],
            preview_banner(B),
            ui.p(ui.HTML(headline(B)), class_="callout"),
            city_tiles(B),
            ui.div(
                ui.div(
                    ui.h3("Where flu-like illness is heading"),
                    ui.p("Drag the slider or press play to step the map from this week "
                         "through each forecast week. Click a neighborhood for its detail.",
                         class_="blurb"),
                    slider("h", "Weeks ahead", 0, hmax_b, 0, 1400),
                    out("boston_map"), class_="card"),
                ui.div(ui.h3("Ranked"),
                       ui.p("Same numbers as the map, highest first.", class_="blurb"),
                       out("boston_ranked"), class_="card"),
                class_="grid-2"),
            out("boston_citywide"),
            value="outlook"),
        "detail": ui.nav_panel(
            V.TAB_TITLES["detail"],
            preview_banner(B),
            ui.div(
                ui.input_select("area", "Neighborhood",
                                {a: short(B, a) for a in B.areas}, selected=area),
                ui.input_checkbox_group(
                    "models", "Models", {m: D.MODEL_SHORT.get(m, m) for m in B.models},
                    selected=[D.PRIMARY] + (["persistence"] if m == "analyst" else []),
                    inline=True),
                class_="controls"),
            out("detail_body"),
            ui.div(
                ui.h3("Is this season early, or big?"),
                ui.input_radio_buttons("ribbon_set", None, RIBBON_SETS, selected=ribbon_set,
                                       inline=True)
                if B.season_roles() else None,
                out("detail_ribbons"),
                class_="chart-card"),
            value="detail"),
        "drivers": ui.nav_panel(
            V.TAB_TITLES["drivers"],
            preview_banner(B),
            ui.h2("What's driving the forecast"),
            ui.p("The graph model reads each neighborhood's recent weeks, its weather, the "
                 "time of year and its neighbors' recent weeks. This page splits each "
                 "forecast into those pieces, so you can see whether a rise is local "
                 "momentum, spillover from next door, or just the season.", class_="blurb"),
            ui.div(
                ui.input_select("drv_area", "Neighborhood",
                                {a: short(B, a) for a in B.areas}, selected=area),
                slider("drv_h", "Weeks ahead", min(B.horizons), hmax_b, min(B.horizons), 1600),
                class_="controls"),
            ui.p("Press play to watch the picture change as the forecast looks further "
                 "ahead: this week's reading matters most next week, while the season and "
                 "the neighbors matter more by week four.", class_="note"),
            out("drv_body"),
            value="drivers") if B.has_drivers else None,
        "severity": ui.nav_panel(V.TAB_TITLES["severity"], severity_panel(B, m, area, out=out),
                                 value="severity"),
        "all": ui.nav_panel(
            V.TAB_TITLES["all"],
            preview_banner(B),
            ui.h2("Every neighborhood at once"),
            ui.p("The graph model's selling point is that neighboring areas move "
                 "together, so it helps to see them side by side. Each card shows the "
                 "last 12 reported weeks (black) and the next four (blue, with the "
                 "plausible range). Click a card for its detail.", class_="blurb"),
            ui.div(ui.input_select("sort", "Sort by", SORTS, selected="rise"),
                   ui.input_switch("shared", "Same scale for every card", True),
                   class_="controls"),
            out("multiples"),
            value="all"),
        "record": ui.nav_panel(V.TAB_TITLES["record"], out("record"), value="record"),
        "chicago": ui.nav_panel(V.TAB_TITLES["chicago"], chicago_panel(out=out, slider=slider), value="chicago"),
        "table": ui.nav_panel(
            V.TAB_TITLES["table"],
            ui.div(ui.input_select("tbl_city", "City", {k: c.label for k, c in D.CITIES.items()}),
                   ui.input_select("tbl_model", "Model",
                                   {m: D.MODEL_SHORT.get(m, m) for m in B.models}),
                   class_="controls"),
            table_out("table"),
            value="table"),
        "how": ui.nav_panel(V.TAB_TITLES["how"], how_panel(download=download), value="how"),
    }
    wanted = [t for t in V.TABS[m] if (t != "chicago" or CHI is not None)
              and panels[t] is not None]
    return ui.navset_card_tab(*[panels[t] for t in wanted], id="nav", selected=wanted[0])


# --- dynamic bodies, as plain functions of the inputs they read -------------------------

def lead_first(models: list[str]) -> list[str]:
    """Bands go to the graph model when it is shown, so they mean the same thing
    everywhere; "same as last week" goes last, since it has no range."""
    return sorted(models, key=lambda m: (m == "persistence", m != D.PRIMARY))


def detail_html(area: str, models: list[str]):
    models = lead_first(models)
    rows = B.rows(models[0], area)
    now = B.latest()[area]
    first, last = rows.iloc[0], rows.iloc[-1]
    lvl_now = B.level(area, now)
    reported = (
        f"In <strong>{short(B, area)}</strong>, {B.fmt(now)} {B.info['unit_short']} were "
        f"reported for the week of {week_span(B.origin)} ({(lvl_now or 'unrated').lower()} "
        f"for this neighborhood). ")
    if models[0] == "persistence":
        sentence = reported + (
            "“Same as last week” carries that number forward unchanged to every week "
            "ahead. It is not a forecast: it is the yardstick the models are scored "
            "against, so it has no range. Tick a model to see a forecast.")
    else:
        sentence = reported + (
            f"The {D.MODEL_SHORT.get(models[0], models[0]).lower()} expects "
            f"<strong>{B.fmt(first['predicted'])}</strong> next week, and would be "
            f"surprised by anything outside {B.fmt(first['lower'])}–{B.fmt(first['upper'])}. "
            f"For the week of {week_span(last['target_date'])}: {B.fmt(last['predicted'])} "
            f"({B.fmt(last['lower'])}–{B.fmt(last['upper'])}).")
    badges = ui.div(*[ui.span(ui.tags.b(D.MODEL_SHORT.get(m, m) + ": "),
                              trust_badge(B.trust(m, 1)), " ",
                              **{"data-series": D.MODEL_CLASS.get(m, "s1")})
                      for m in models if m != "persistence"],
                    class_="legend")
    teaser = driver_teaser(B, area)
    return ui.div(
        ui.p(ui.HTML(sentence), class_="callout"),
        ui.p(teaser, " ", ui.input_action_link("to_drivers", "See what's driving it →"),
             class_="teaser") if teaser else None,
        ui.div(ui.span("Past-season check, 1 week ahead:", class_="note"), badges),
        fan_block(B, area, models, f"{short(B, area)}: the next four weeks",
                  f"{B.info['unit'].capitalize()}. The vertical line is the latest "
                  "reported week; hover anywhere for that week's numbers."))


def drivers_top(area: str, h: int, analyst: bool):
    wf = B.waterfall(area, h)
    return ui.div(
        ui.p(ui.HTML(driver_sentence(B, area, h, wf)), class_="callout"),
        ui.div(waterfall_block(B, area, h, analyst), spill_block(B, area, h, "drv_click"),
               class_="grid-2"))


def drivers_bottom(area: str, h: int, analyst: bool):
    return ui.div(timeline_block(B, area, h), method_block(B, area, h, analyst))


def drivers_body(area: str, h: int, analyst: bool):
    # Three pieces so export_html.py can render the matrix once per week ahead
    # rather than once per neighborhood.
    return ui.div(drivers_top(area, h, analyst), matrix_block(B, area, h, "drv_click"),
                  drivers_bottom(area, h, analyst))


SORTS = {"rise": "Fastest rising", "now": "Highest now", "name": "A–Z"}


def multiples_html(sort: str, shared: bool):
    latest = B.latest()
    hmax = max(B.horizons)
    ahead = B.at(D.PRIMARY, hmax)
    growth = (ahead / latest.replace(0, np.nan)) - 1
    order = {"rise": growth.sort_values(ascending=False).index,
             "now": latest.sort_values(ascending=False).index,
             "name": sorted(B.areas, key=lambda a: short(B, a))}[sort]
    shared_top = max(B.history.iloc[-12:].max().max(),
                     B.forecast.loc[B.forecast["model"] == D.PRIMARY, "upper"].max())
    cards = []
    for area in order:
        f = B.rows(D.PRIMARY, area)
        top = shared_top if shared else max(B.history[area].iloc[-12:].max(), f["upper"].max())
        g = growth.get(area, np.nan)
        arrow, _ = direction(g)
        cards.append(ui.div(
            ui.div(ui.span(short(B, area), class_="mini-name"),
                   ui.span(f"{B.fmt(latest[area])} → {B.fmt(ahead[area])}", class_="mini-val"),
                   class_="mini-head"),
            ui.HTML(C.spark(B.history[area], f, ymax=top * 1.05)),
            ui.div(ui.span(level_pill(B.level(area, latest[area]))),
                   ui.span(f"{arrow} {g * 100:+.0f}% in {hmax} wk" if np.isfinite(g) else ""),
                   class_="mini-foot"),
            class_="mini", **{"data-area": area, "data-input": "area_click", "tabindex": "0",
                              "data-tip": f"{short(B, area)}\nNow {B.fmt(latest[area])}, "
                                          f"in {hmax} weeks {B.fmt(ahead[area])}"}))
    return ui.div(*cards, class_="multiples")


def chicago_zip(z: str):
    return fan_block(CHI, z, [D.PRIMARY], f"{short(CHI, z)}: the next weeks",
                     "Activity level, 1 to 10. Values are capped at 10, so a very "
                     "high peak and a merely high one can look the same.")


def citywide_block(m: str):
    models = [D.PRIMARY] + (["persistence"] if m == "analyst" else [])
    return fan_block(B, None, models, "Citywide",
                     f"Average across the {len(B.areas)} neighborhoods, "
                     f"{B.info['unit']}. Hover for weekly values.")


def table_frame(city: D.CityData, model: str) -> pd.DataFrame:
    f = city.rows(model)
    return pd.DataFrame({
        city.info["area_word"]: [short(city, a) for a in f["area"]],
        "weeks ahead": f["horizon"], "week of": f["target_date"].dt.strftime("%Y-%m-%d"),
        "median": f["predicted"].round(2), "95% low": f["lower"].round(2),
        "95% high": f["upper"].round(2), "past-season check": f["trust"]})


def download_name(kind: str) -> str:
    return f"boston_flu_forecast_{B.meta['origin']}{'_flusight' if kind == 'flusight' else ''}.csv"


# --- server ----------------------------------------------------------------------------

def server(input, output, session):
    sel_area = reactive.value(B.areas[0] if B else None)
    sel_zip = reactive.value(None)

    mode = reactive.calc(lambda: input.audience() or "briefing")

    # --- tab shell, rebuilt when the audience changes -------------------------
    @render.ui
    def tabs():
        m = mode()
        with reactive.isolate():
            area = sel_area()
            ribbon_set = input.ribbon_set() if "ribbon_set" in input else "all"
        return build_tabs(m, area, ribbon_set)

    # --- map clicks: every clickable area lands on the detail view ---------------
    @reactive.effect
    @reactive.event(input.area_click)
    def _go_area():
        area = input.area_click()
        if area in B.areas:
            sel_area.set(area)
            ui.update_select("area", selected=area)
            ui.update_select("drv_area", selected=area)
            ui.update_select("sev_area", selected=area)
            ui.update_navs("nav", selected="detail")

    # The Neighborhood, What's-driving-it and Severity tabs share one selected area.
    def _share_area(area: str, source: str):
        sel_area.set(area)
        for other in ("area", "drv_area", "sev_area"):
            if other != source and other in input and input[other]() != area:
                ui.update_select(other, selected=area)

    @reactive.effect
    @reactive.event(input.area)
    def _keep_area():
        _share_area(input.area(), "area")

    @reactive.effect
    @reactive.event(input.drv_area)
    def _keep_drv_area():
        _share_area(input.drv_area(), "drv_area")

    @reactive.effect
    @reactive.event(input.sev_area)
    def _keep_sev_area():
        _share_area(input.sev_area(), "sev_area")

    # Clicks on the severity table and grid pick that area, on the same tab.
    @reactive.effect
    @reactive.event(input.sev_click)
    def _sev_click():
        area = input.sev_click()
        if area in B.areas:
            ui.update_select("sev_area", selected=area)
            _share_area(area, "sev_area")

    # Clicks on the spillover map and the matrix explain that area, on the same tab.
    @reactive.effect
    @reactive.event(input.drv_click)
    def _drv_click():
        area = input.drv_click()
        if area in B.areas:
            sel_area.set(area)
            ui.update_select("drv_area", selected=area)
            ui.update_select("area", selected=area)
            ui.update_select("sev_area", selected=area)

    @reactive.effect
    @reactive.event(input.to_drivers)
    def _to_drivers():
        ui.update_navs("nav", selected="drivers")

    @reactive.effect
    @reactive.event(input.chi_click)
    def _go_zip():
        sel_zip.set(input.chi_click())
        ui.update_select("chi_area", selected=input.chi_click())

    # --- outlook ------------------------------------------------------------------
    @render.ui
    def boston_map():
        return map_block(B, int(input.h() or 0), None, "area_click")

    @render.ui
    def boston_ranked():
        return ranked_block(B, int(input.h() or 0), "area_click")

    @render.ui
    def boston_citywide():
        return citywide_block(mode())

    # --- detail -------------------------------------------------------------------
    @render.ui
    def detail_body():
        area = input.area() or sel_area()
        if area not in B.areas:
            area = B.areas[0]
        models = [m for m in (input.models() or [D.PRIMARY]) if m in B.models] or [D.PRIMARY]
        return detail_html(area, models)

    @render.ui
    def detail_ribbons():
        area = input.area() or sel_area()
        if area not in B.areas:
            area = B.areas[0]
        return ribbons_block(B, area, input.ribbon_set() if "ribbon_set" in input else "all")

    # --- what's driving it ------------------------------------------------------------
    if B.has_drivers:
        @render.ui
        def drv_body():
            area = input.drv_area() or sel_area()
            if area not in B.areas:
                area = B.areas[0]
            return drivers_body(area, int(input.drv_h() or min(B.horizons)),
                                mode() == "analyst")

    # --- small multiples -----------------------------------------------------------
    @render.ui
    def multiples():
        return multiples_html(input.sort() or "rise", bool(input.shared()))

    # --- severity, by neighborhood -------------------------------------------------------
    def sev_pick() -> str:
        area = input.sev_area() if "sev_area" in input else sel_area()
        return area if area in B.areas else B.areas[0]

    @render.ui
    def sev_overview():
        line = input.sev_line() if "sev_line" in input else "IT50"
        h = int(input.sev_h()) if "sev_h" in input else max(B.horizons)
        return severity_overview(B, sev_pick(), line, h)

    @render.ui
    def sev_detail():
        return severity_area_block(B, sev_pick())

    # --- track record ----------------------------------------------------------------
    @render.ui
    def record():
        return record_body(B, mode())

    # --- chicago ---------------------------------------------------------------------
    if CHI is not None:
        @render.ui
        def chi_map():
            return map_block(CHI, int(input.chi_h() or 0), sel_zip(), "chi_click")

        @render.ui
        def chi_ranked():
            return ranked_block(CHI, int(input.chi_h() or 0), "chi_click", limit=12)

        @render.ui
        def chi_zip():
            return chicago_zip(input.chi_area() or CHI.areas[0])

    # --- forecast table + downloads ---------------------------------------------------
    @render.data_frame
    def table():
        city = D.CITIES[input.tbl_city() or "boston"]
        return render.DataGrid(table_frame(city, input.tbl_model() or D.PRIMARY),
                               height="520px", filters=True)

    @render.download(filename=lambda: download_name("csv"))
    def dl_csv():
        yield B.forecast.to_csv(index=False)

    @render.download(filename=lambda: download_name("flusight"))
    def dl_flusight():
        yield D.flusight(B).to_csv(index=False)


# --- panels built once (static content) ---------------------------------------------------

def chicago_panel(out=ui.output_ui, slider=live_slider):
    if CHI is None:
        return ui.p("Chicago data is not published yet.", class_="empty")
    hmax = max(CHI.horizons)
    boston_share = B.citywide()
    chicago_share = CHI.citywide()
    series = {}
    for city, s in ((B, boston_share), (CHI, chicago_share)):
        current = city.season_label(city.origin)
        season = city.seasons(s).get(current, pd.Series(dtype=float))
        series[f"{city.label} {current}"] = 100 * season / city.typical_peak()
    return ui.div(
        preview_banner(CHI),
        ui.h2("Chicago: is the season arriving elsewhere?"),
        ui.p("The same forecasting pipeline, run on Chicago's ZIP-level data. Two reasons "
             "it's here: Chicago's data is often more current than Boston's, so it gives an "
             "early read on the season; and it shows the method working in a second city "
             "with no retuning.", class_="blurb"),
        ui.p(f"Chicago reports an activity level from 1 to 10 for each ZIP code, not a rate, "
             f"so its numbers can't be compared with Boston's directly. The chart below "
             f"puts both cities on one scale: each against its own typical peak.",
             class_="note"),
        city_tiles(CHI),
        ui.div(ui.h3("Each city against its own typical peak"),
               ui.p("100% is the median peak of past seasons in that city. Week 0 is 1 August.",
                    class_="blurb"),
               ui.div(*[ui.span(ui.span(class_=f"sw s{i + 1}"), name, class_="key")
                        for i, name in enumerate(series)], class_="legend"),
               ui.HTML(C.two_city(series)), class_="chart-card"),
        ui.div(
            ui.div(ui.h3("ZIP codes"),
                   slider("chi_h", "Weeks ahead", 0, hmax, 0, 1400),
                   out("chi_map"), class_="card"),
            ui.div(ui.h3("Highest"), out("chi_ranked"), class_="card"),
            class_="grid-2"),
        fan_block(CHI, None, [D.PRIMARY], "Chicago citywide",
                  f"Average activity level across {len(CHI.areas)} ZIP codes."),
        ui.div(ui.input_select("chi_area", "ZIP code", {a: a for a in sorted(CHI.areas)}),
               class_="controls"),
        out("chi_zip"),
        ui.p(f"Source: {CHI.info['source']}.", class_="note"),
        ui.p(CHI.info["disclaimer"], class_="note"),
    )


def record_body(city: D.CityData, m: str):
    comp = city.comparison[city.comparison["model"].isin(city.models)]
    seasons = ", ".join(city.meta.get("backtest_seasons") or []) or "past seasons"
    header = [ui.tags.th("Weeks ahead")] + [ui.tags.th(D.MODEL_SHORT.get(mdl, mdl))
                                            for mdl in city.models if mdl != "persistence"]
    body = []
    for h in city.horizons:
        cells = [ui.tags.td(f"{h}")]
        for mdl in city.models:
            if mdl == "persistence":
                continue
            r = comp[(comp["model"] == mdl) & (comp["horizon"] == h)]
            if not len(r):
                cells.append(ui.tags.td("—"))
                continue
            r = r.iloc[0]
            gain = (1 - r["relative_wis"]) * 100
            text = f"{abs(gain):.0f}% {'closer' if gain >= 0 else 'further off'}"
            extra = (ui.div(f"WIS {r['wis']:.2f} · relative {r['relative_wis']:.2f} · "
                            f"p(Holm) {r['p_holm']:.3f}", class_="note") if m == "analyst" else None)
            cells.append(ui.tags.td(ui.div(text), trust_badge(r["verdict"]), extra))
        body.append(ui.tags.tr(*cells))
    # "Same as last week" is shown without a range, so its coverage is left out too.
    cols = [c for c in ("coverage95", "coverage50") if c in city.bt_scores]
    shown = [mm for mm in city.models if mm != "persistence"]
    cover = (city.bt_scores[city.bt_scores["model"].isin(shown)]
             .groupby(["model", "horizon"])[cols].mean().reset_index())
    return ui.div(
        preview_banner(city),
        ui.h2("Would these forecasts have worked before?"),
        ui.p(f"Before trusting a forecast, we replay past seasons ({seasons}). Each model is "
             "trained only on data from before the season, then forecasts every week of it as "
             "if it were live. We compare it with the simplest possible rule: next week looks "
             "like this week.", class_="blurb"),
        ui.div(ui.h3("How much closer than “same as last week”?"),
               ui.p("The score counts both the miss and how honest the range was (a tight "
                    "range that misses is penalized more than a wide one). “20% closer” "
                    "means 20% less total error than the simple rule on the same weeks. The "
                    "badge says whether the gap is bigger than week-to-week luck.",
                    class_="blurb"),
               ui.div(ui.tags.table(ui.tags.thead(ui.tags.tr(*header)), ui.tags.tbody(*body),
                                    class_="score-table"), class_="table-scroll"),
               class_="chart-card"),
        ui.div(ui.h3("When it says “50% range” or “95% range”, is it right that often?"),
               ui.p("How often the real number landed inside each model's ranges in past "
                    "seasons. The likely range (50%) should catch it about half the time, the "
                    "plausible range (95%) about 19 times in 20. Well below the target means "
                    "overconfident; well above means the range is wider than it needs to be.",
                    class_="blurb"),
               ui.div(ui.span(ui.span(class_="sw-ring"), "likely range (50%)", class_="key"),
                      ui.span(ui.span(class_="sw-dot"), "plausible range (95%)", class_="key"),
                      class_="legend") if "coverage50" in cols else None,
               ui.HTML(C.coverage_dots(cover)), class_="chart-card"),
        live_block(city),
    )


def live_block(city: D.CityData):
    s = city.live_scores
    done = s[np.isfinite(s["wis"])] if s is not None else None
    title = ui.h3(f"This season, live ({city.season_label(city.origin)})")
    if done is None or done.empty:
        first = city.origin + pd.Timedelta(weeks=1)
        return ui.div(title, ui.p(
            f"Every weekly forecast is saved unchanged the day it is made. The first ones are "
            f"scored once BPHC reports the week of {date(first)}. This section then fills in "
            f"week by week: a prospective record nobody can tune after the fact.",
            class_="empty"), class_="chart-card")
    if "covered50" not in done:  # scored before the 50% range was recorded
        done = done.assign(covered50=np.nan)
    summary = done.groupby(["horizon", "model"]).agg(
        weeks=("origin_date", "nunique"), wis=("wis", "mean"), cover=("covered95", "mean"),
        cover50=("covered50", "mean")).reset_index()
    # "Same as last week" over the same weeks each model was scored on: a model
    # added mid-season (ARIMA) has fewer weeks than the reference.
    persist = done[done["model"] == "persistence"].groupby(["horizon", "origin_date"])["wis"].sum()
    persist_n = done[done["model"] == "persistence"].groupby(["horizon", "origin_date"])["wis"].size()
    rows = []
    for r in summary[summary["model"] != "persistence"].itertuples():
        weeks = done[(done["model"] == r.model) & (done["horizon"] == r.horizon)]["origin_date"].unique()
        keys = [(r.horizon, w) for w in weeks if (r.horizon, w) in persist.index]
        ref = persist.loc[keys].sum() / persist_n.loc[keys].sum() if keys else np.nan
        rel = r.wis / ref
        rows.append(ui.tags.tr(ui.tags.td(D.MODEL_SHORT.get(r.model, r.model)), ui.tags.td(r.horizon),
                               ui.tags.td(r.weeks),
                               ui.tags.td(f"{(1 - rel) * 100:+.0f}%" if np.isfinite(rel) else "—"),
                               ui.tags.td(f"{r.cover50 * 100:.0f}%" if np.isfinite(r.cover50) else "—"),
                               ui.tags.td(f"{r.cover * 100:.0f}%")))
    return ui.div(title, ui.p("Archived forecasts that have now met the real numbers.",
                              class_="blurb"),
                  ui.div(ui.tags.table(ui.tags.thead(ui.tags.tr(
                      *[ui.tags.th(t) for t in ("Model", "Weeks ahead", "Weeks scored",
                                                "Closer than “same as last week”",
                                                "Inside 50% range", "Inside 95% range")])),
                      ui.tags.tbody(*rows), class_="score-table"), class_="table-scroll"),
                  class_="chart-card")


# --- how severe the season is ------------------------------------------------------------

# Past seasons that stand in for this one, in the series colours the ribbons use.
ANALOG_CLASS = ("s2", "s3", "s4")


def month_part(d) -> str:
    d = pd.Timestamp(d)
    part = "early " if d.day <= 10 else "mid-" if d.day <= 20 else "late "
    return part + d.strftime("%b")


def severity_rules(city: D.CityData, its: dict[str, float]):
    cuts = [its[k] for k, _ in C.SEV_LINES]
    spans = [f"below {city.fmt(cuts[0])}", f"{city.fmt(cuts[0])} to {city.fmt(cuts[1])}",
             f"{city.fmt(cuts[1])} to {city.fmt(cuts[2])}", f"{city.fmt(cuts[2])} and up"]
    return ui.div(*[ui.span(level_pill(lvl), " ", span, class_="rule")
                    for lvl, span in zip(D.LEVELS, spans)], class_="rules")


def formula_block(city: D.CityData, th: dict, table: pd.DataFrame, analyst: bool):
    its, mu, sigma, n, k, mult = (th[x] for x in ("its", "mu", "sigma", "n", "k", "mult"))
    seasons = len(th["top"])
    left_out = [r.season for r in table.itertuples() if r.role == "skipped"]
    peaks = table.loc[table["role"] == "used", "peak"]
    chips = [ui.span(ui.tags.strong(s), " " + " · ".join(city.fmt(v) for v in t), class_="chip")
             for s, t in th["top"].items()]
    lines = []
    for key, name in C.SEV_LINES:
        lines.append(ui.tags.tr(
            ui.tags.td(ui.HTML(f"IT<sub>{key[2:]}</sub>")), ui.tags.td(f"{name} from"),
            ui.tags.td(f"{mult[key]:.3f}"),
            ui.tags.td(ui.HTML(f"e<sup>{mu:.3f} + {mult[key]:.3f} × {sigma:.3f}</sup> = "
                               f"<strong>{city.fmt(its[key])}</strong>")),
            ui.tags.td(f"{int((peaks >= its[key]).sum())} of {len(peaks)}")))
    analyst_notes = None
    if analyst:
        narrow = np.exp(mu + mult["IT90"] * sigma / np.sqrt(n))
        above = int((peaks >= narrow).sum())
        analyst_notes = ui.div(ui.h4("Method notes"), ui.tags.ul(
            ui.tags.li(f"t is Student's t quantile with m − 1 = {n - 1} degrees of freedom, at "
                       "p = 0.50, 0.90 and 0.98 (CDC's levels; mem's own default is 0.40, 0.90 "
                       f"and 0.975). σ is the sample SD of the {n} pooled logs. This is mem's "
                       "default intensity method (i.type.intensity = 6)."),
            ui.tags.li("The lines are ranges for one more top week, not for the mean of the top "
                       f"weeks. With σ/√m instead, the high line would sit at {city.fmt(narrow)} "
                       f"and {above} of the {len(peaks)} reference seasons would peak high or "
                       "worse."),
            ui.tags.li("CDC applies this to three indicators (outpatient ILI, hospitalizations, "
                       "deaths) and takes the class at least two agree on. BPHC publishes only "
                       "ED visits, so this is the one-indicator version."),
            ui.tags.li("A season's top weeks enter as they are, not smoothed, and the seasons are "
                       "weighted equally (no recency weighting). The same recipe fits the lines "
                       "in the paper's severity analysis; there each test season used only the "
                       "seasons before it.")),
            class_="note-card")
    return ui.div(
        ui.h3("The formula"),
        ui.p("CDC rates flu weeks and seasons with intensity thresholds from the moving epidemic "
             "method (Vega et al., 2013; Biggerstaff et al., 2018), with the settings of the mem "
             "R package, as in our paper. Here it is step by step, with this city's numbers in.",
             class_="blurb"),
        ui.tags.ol(
            ui.tags.li(ui.tags.strong(f"Take each past season's {k} highest weeks"),
                       f", citywide. The method pools about 30 values, so with {seasons} seasons "
                       f"that is 30 ÷ {seasons} ≈ {k} each, {n} in all. Left out: "
                       f"{', '.join(left_out)} (COVID-19 cut short or suppressed them) and "
                       f"{city.season_label(city.origin)} (still running).",
                       ui.div(*chips, class_="fresh")),
            ui.tags.li(ui.tags.strong("Average them on a log scale."),
                       " Flu seasons differ by multiples, not by fixed amounts, so the logs "
                       "are averaged: the result is the geometric mean.",
                       ui.div(ui.HTML(f"<var>μ</var> = mean of ln <var>x</var><sub>i</sub> = "
                                      f"{mu:.3f} &nbsp;&nbsp;→&nbsp;&nbsp; e<sup><var>μ</var></sup>"
                                      f" = {city.fmt(np.exp(mu))}"), class_="formula"),
                       ui.div(ui.HTML(f"<var>σ</var> = SD of ln <var>x</var><sub>i</sub> = "
                                      f"{sigma:.3f}"), class_="formula")),
            ui.tags.li(ui.tags.strong("Set three lines above the geometric mean."),
                       " Each is the upper end of a one-sided 50%, 90% or 98% range for one "
                       "more top week:",
                       ui.div(ui.HTML("IT<sub><var>p</var></sub> = e<sup><var>μ</var> + "
                                      "<var>t</var><sub><var>p</var></sub>(<var>m</var>−1)"
                                      "·√(1 + 1/<var>m</var>)·<var>σ</var></sup>, "
                                      f"&nbsp;<var>m</var> = {n}"), class_="formula"),
                       ui.div(ui.tags.table(
                           ui.tags.thead(ui.tags.tr(*[ui.tags.th(t) for t in (
                               "Line", "Level", "Multiplier", "Worked out",
                               "Seasons that reached it")])),
                           ui.tags.tbody(*lines), class_="score-table"), class_="table-scroll")),
            ui.tags.li(ui.tags.strong("Rate each week against the lines."),
                       " The season takes the level of its highest week. These are the levels "
                       "on every tab.", severity_rules(city, its)),
            class_="steps"),
        analyst_notes, class_="chart-card")


def analogs_block(city: D.CityData, analogs: list[dict], current: str, table: pd.DataFrame):
    start = pd.Timestamp(year=int(current[:4]), month=8, day=1)
    fc = city.citywide_forecast(D.PRIMARY)
    last = week_span(fc["target_date"].max())
    peak_dates = table.set_index("season")["peak_date"]
    classes = sorted({a["cls"] for a in analogs}, key=D.LEVELS.index)
    cards = []
    for a, cls in zip(analogs, ANALOG_CLASS):
        when = peak_dates[a["season"]]
        cards.append(ui.div(
            ui.div(ui.span(class_=f"sw {cls}"), ui.span(a["season"], class_="analog-name"),
                   class_="analog-head"),
            ui.p(f"Typically {np.expm1(a['rmse']):.0%} apart over the {a['weeks']} weeks so far, "
                 "forecast included.", class_="analog-sub"),
            ui.p(ui.HTML(f"Went on to peak at <strong>{city.fmt(a['peak'])}</strong> in "
                         f"{month_part(when)} "), level_pill(a["cls"])),
            ui.p(f"In the week matching {last}, it stood at {city.fmt(a['ahead'])}.",
                 class_="analog-sub"),
            class_="analog"))
    seasons = city.seasons()
    pts = [((pd.Timestamp(r.target_date) - start).days // 7, r.predicted) for r in fc.itertuples()]
    svg = C.ribbons(seasons, current, pts, unit=city.info["unit_short"], fmt=city.fmt,
                    highlight={a["season"]: cls for a, cls in zip(analogs, ANALOG_CLASS)})
    return ui.div(
        ui.h3("Which past season does this one look like?"),
        ui.p("The past seasons whose curve sits closest to this one's so far, with the graph "
             "model's next four weeks added on. Closeness is measured on a log scale, so being "
             "twice as high counts the same in October as in January.", class_="blurb"),
        ui.div(*cards, class_="analogs"),
        ui.div(ui.span(ui.span(class_="sw s1"), current, class_="key"),
               *[ui.span(ui.span(class_=f"sw {cls}"), a["season"], class_="key")
                 for a, cls in zip(analogs, ANALOG_CLASS)],
               ui.span(ui.span(class_="sw past"), "other seasons", class_="key"), class_="legend"),
        ui.HTML(svg),
        ui.p("Early in the season every curve is low and they look alike, so a close match "
             "says little about the peak to come"
             + (f": the {['', 'one', 'two', 'three'][len(analogs)]} closest went on to be "
                f"{', '.join(c.lower() for c in classes[:-1])} and {classes[-1].lower()} seasons"
                if len(classes) > 1 else "")
             + ". Read these as a reference, not a forecast.", class_="note"),
        class_="chart-card")


def skipped_notes(table: pd.DataFrame) -> dict[str, str]:
    """Why each grey season in a severity strip is left out of the lines."""
    return {r.season: ("Left out of the lines: COVID-19 cut it short" if r.season == "2019-20"
                       else "Left out of the lines: COVID-19 suppressed it")
            for r in table.itertuples() if r.role == "skipped"}


def severity_overview(city: D.CityData, selected: str, line: str = "IT50",
                      horizon: int | None = None):
    """Every area this season against its own lines, then every area and season."""
    return ui.div(severity_table(city, selected, line, horizon),
                  severity_grid_block(city, selected))


def severity_table(city: D.CityData, selected: str | None, line: str = "IT50",
                   horizon: int | None = None):
    horizon = horizon if horizon in city.horizons else max(city.horizons)
    name = dict(C.SEV_LINES)[line].lower()
    target = week_span(city.rows(D.PRIMARY).query("horizon == @horizon")["target_date"].max())
    rows = []
    for a in city.areas:
        its = city.severity_thresholds(a)["its"]
        t = city.season_severity(a)
        now = t[t["role"] == "current"].iloc[0]
        p = city.exceed_prob(its[line], area=a).get(horizon, np.nan)
        week = city.level(a, city.history[a].dropna().iloc[-1])
        rows.append((now.peak / its[line], a, now, its, p, week))
    trs = []
    for share, a, now, its, p, week in sorted(rows, key=lambda r: -r[0]):
        status = D.LEVEL_STATUS[now.cls]
        trs.append(ui.tags.tr(
            ui.tags.td(short(city, a)), ui.tags.td(city.fmt(now.peak)),
            ui.tags.td(ui.div(ui.div(ui.div(class_="share-bar",
                                            style=f"width:{min(share, 1) * 100:.0f}%"),
                                     class_=f"share-track sev-{status}"),
                              ui.span(f"{share:.0%}"), class_="share")),
            ui.tags.td(level_pill(now.cls)),
            ui.tags.td(level_pill(week) if week else "—"),
            ui.tags.td(" · ".join(city.fmt(its[k]) for k, _ in C.SEV_LINES)),
            ui.tags.td(C.chance(p)),
            class_="selected" if a == selected else None,
            **{"data-area": a, "data-input": "sev_click", "tabindex": "0"}))
    return ui.div(
        ui.div(ui.tags.table(
            ui.tags.thead(ui.tags.tr(*[ui.tags.th(t) for t in (
                city.info["area_word"].capitalize(), "Highest week so far",
                f"Share of its {name} line", "Season so far", "This week's level",
                "Its lines (moderate · high · very high)",
                f"Chance above its {name} line, week of {target}")])),
            ui.tags.tbody(*trs), class_="score-table sev-table"), class_="table-scroll"),
        ui.p(f"Sorted by how close each is to its own {name} line. The chances come straight "
             f"from each {city.info['area_word']}'s forecast ranges, so they need no averaging.",
             class_="note"),
        ui.p(f"This week's level is the pill on the other tabs: the latest week against the "
             "same lines. The season so far is its highest week against them, so it is never "
             "below this week's level.", class_="note"))


def severity_grid_block(city: D.CityData, selected: str | None):
    """Every area and season against its own lines; the same whatever line or week
    the table above is set to."""
    tables = {a: city.season_severity(a) for a in sorted(city.areas, key=lambda a: short(city, a))}
    # Which past season rated high or worse in the most areas, against their own lines.
    worst = (pd.concat([t.assign(area=a) for a, t in tables.items()])
             .query("role == 'used'").assign(bad=lambda d: d["cls"].isin(["High", "Very high"]))
             .groupby("season")["bad"].sum().sort_values(ascending=False))
    grid = C.severity_grid(tables, names={a: short(city, a) for a in city.areas}, fmt=city.fmt,
                           unit=city.info["unit_short"], input_id="sev_click", selected=selected)
    words = city.info["areas_word"]
    return ui.div(
        ui.h4("Every season, every " + city.info["area_word"]),
        ui.p(f"Each cell is one season against that {city.info['area_word']}'s own lines "
             "(L low, M moderate, H high, VH very high); the last column is this season so far. "
             f"Hover a cell for its peak. In {worst.index[0]}, {int(worst.iloc[0])} of "
             f"{len(tables)} {words} had a high or very high season by their own lines.",
             class_="blurb"),
        ui.HTML(grid))


def severity_area_block(city: D.CityData, area: str):
    """One area against its own lines: the sentence and the season strip."""
    th = city.severity_thresholds(area)
    its = th["its"]
    table = city.season_severity(area)
    now = table[table["role"] == "current"].iloc[0]
    unit = city.info["unit_short"]
    rows = city.rows(D.PRIMARY, area)
    last = rows.iloc[-1]
    name = short(city, area)
    nxt = next(((k, n) for k, n in C.SEV_LINES if now.peak < its[k]), None)
    head = (f"<strong>{name}</strong>: its highest week so far ({city.fmt(now.peak)} {unit}, week "
            f"of {week_span(now.peak_date)}) makes {now.season} a <strong>{now.cls.lower()}</strong> "
            "season there so far, against its own history")
    if nxt:
        key, line = nxt
        p = city.exceed_prob(its[key], area=area).get(last["horizon"], np.nan)
        head += (f": {now.peak / its[key]:.0%} of its {line.lower()} line ({city.fmt(its[key])}). "
                 f"The graph model gives a <strong>{C.chance(p)} chance</strong> that the week of "
                 f"{week_span(last['target_date'])} is above it.")
    else:
        head += ", above even its very-high line."
    ratio = its["IT50"] / city.severity_thresholds()["its"]["IT50"]
    top = rows.loc[rows["predicted"].idxmax()]
    strip = C.severity_strip(table, its, fmt=city.fmt, unit=unit, notes=skipped_notes(table),
                             outlook=(top["predicted"], top["lower"], top["upper"],
                                      f"week of {week_span(top['target_date'])}"))
    return ui.div(
        ui.p(ui.HTML(head), class_="callout"),
        ui.div(
            ui.h3(f"{name}: every season against its own lines"),
            ui.p(f"{name}'s lines come from its {th['k']} highest weeks in each of {len(th['top'])} "
                 f"seasons: geometric mean {city.fmt(np.exp(th['mu']))}, σ = {th['sigma']:.3f}. "
                 f"They sit at {ratio:.1f}× the citywide ones (moderate from "
                 f"{city.fmt(its['IT50'])}, high from {city.fmt(its['IT90'])}, very high from "
                 f"{city.fmt(its['IT98'])}). Same chart as the citywide one above.",
                 class_="blurb"),
            ui.HTML(strip), class_="chart-card"))


def severity_panel(city: D.CityData, m: str, area: str | None = None, out=ui.output_ui):
    th = city.severity_thresholds()
    its = th["its"]
    table = city.season_severity()
    now = table[table["role"] == "current"].iloc[0]
    unit = city.info["unit_short"]
    fc = city.citywide_forecast(D.PRIMARY).set_index("horizon")
    hmax = max(city.horizons)
    probs = pd.DataFrame({k: city.exceed_prob(v) for k, v in its.items()})
    analogs = city.analogs()
    used = table[table["role"] == "used"]
    start = pd.Timestamp(year=int(now.season[:4]), month=8, day=1)
    # Past peaks moved onto this season's calendar, to say when a peak usually comes.
    offsets = [(d - pd.Timestamp(year=int(s[:4]), month=8, day=1)).days
               for s, d in zip(used["season"], used["peak_date"])]
    early, late = (start + pd.Timedelta(days=d) for d in (min(offsets), max(offsets)))

    # The next line above this season's highest week so far, and the chance of crossing it.
    nxt = next(((k, name) for k, name in C.SEV_LINES if now.peak < its[k]), None)
    head = (f"Citywide, {now.season} is so far a <strong>{now.cls.lower()}-severity</strong> "
            f"season in {city.label}: its highest week yet ({city.fmt(now.peak)} {unit}, week of "
            f"{week_span(now.peak_date)})")
    if nxt:
        key, name = nxt
        p = probs[key].loc[hmax]
        head += (f" is {now.peak / its[key]:.0%} of the {name.lower()} line "
                 f"({city.fmt(its[key])}). The graph model gives a <strong>{C.chance(p)} "
                 f"chance</strong> that the week of {week_span(fc.loc[hmax, 'target_date'])} "
                 "is above it.")
    else:
        head += " is already above the very-high line."

    top = fc.loc[fc["predicted"].idxmax()]
    strip = C.severity_strip(table, its, fmt=city.fmt, unit=unit, notes=skipped_notes(table),
                             outlook=(top["predicted"], top["lower"], top["upper"],
                                      f"week of {week_span(top['target_date'])}"))
    weeks = [week_span(d) for d in fc["target_date"]]
    closest = analogs[0] if analogs else None
    chi_its = CHI.severity_thresholds()["its"] if CHI else None
    return ui.div(
        preview_banner(city),
        ui.h2("How bad is this season?"),
        ui.p("Severity rates a whole flu season, not a single week: how high its worst week "
             "climbs, against the spread of past seasons' worst weeks. The lines are the ones "
             "CDC's method would draw from Boston's own history. The top of the page rates the "
             f"city as a whole (the average of its {len(city.areas)} {city.info['areas_word']}); "
             f"further down, each {city.info['area_word']} is rated against its own history. "
             "The same lines give the Low to Very high level of each week on the other tabs; a "
             "season takes the level of its highest week.", class_="blurb"),
        ui.p(ui.HTML(head), class_="callout"),
        ui.div(
            tile("Season so far", ui.span(now.cls, class_=f"pill pill-{D.LEVEL_STATUS[now.cls]}"),
                 f"rated on its highest week yet, {city.fmt(now.peak)}"),
            tile("Moderate line", city.fmt(its["IT50"]),
                 f"high from {city.fmt(its['IT90'])}, very high from {city.fmt(its['IT98'])}"),
            tile(f"Chance above {nxt[1].lower()}" if nxt else "Above every line",
                 C.chance(probs[nxt[0]].loc[hmax]) if nxt else "—",
                 f"week of {week_span(fc.loc[hmax, 'target_date'])}, graph model"),
            tile("Closest past season", closest["season"] if closest else "—",
                 f"peaked at {city.fmt(closest['peak'])} ({closest['cls'].lower()})"
                 if closest else ""),
            class_="tiles"),
        ui.div(
            ui.h3("Citywide: every season against the lines"),
            ui.p(f"Each bar runs to a season's highest week, citywide. The shaded zones are the "
                 f"four classes, split at the lines worked out below. Grey seasons are left out "
                 f"of the lines; hover for why. {now.season}'s bar is its peak so far; the hollow "
                 f"part runs to the graph model's highest forecast week, with its 95% range.",
                 class_="blurb"),
            ui.div(ui.span(ui.span(class_="sw-box sev-ahead"), "forecast high", class_="key"),
                   ui.span(ui.span(class_="sw-box sev-skip"), "left out of the lines",
                           class_="key"), class_="legend"),
            ui.HTML(strip),
            ui.p(f"In the seasons behind the lines, the citywide peak came between "
                 f"{month_part(early)} and {month_part(late)}, so a season's class is rarely "
                 "settled before the new year.", class_="note"),
            class_="chart-card"),
        formula_block(city, th, table, m == "analyst"),
        ui.div(
            ui.h3("Chance of crossing each line"),
            ui.p("For each forecast week, the chance the citywide average lands above each "
                 "line, read off the graph model's forecast ranges. Each is the chance for that "
                 "week on its own, not for any of the four: that would need the weeks' joint "
                 "forecast, which the model doesn't give.", class_="blurb"),
            ui.HTML(C.odds_grid(probs, weeks)),
            ui.p("The model's ranges stop at 1% and 99%, so “<1%” means below the lowest range "
                 "it gives. The citywide range averages the neighborhoods' ranges, which is "
                 "wider than the true range of their average, so if anything these chances run "
                 "high.", class_="note"),
            class_="chart-card"),
        ui.div(
            ui.h3(f"{city.info['areas_word'].capitalize()}, each against its own lines"),
            ui.p(f"The same four steps, run on each {city.info['area_word']}'s own weeks. Their "
                 "usual levels differ several times over, so one set of citywide lines would "
                 f"rate some {city.info['areas_word']} high every year and others never; like the "
                 "levels on the other tabs, each is rated against itself. Click a row to see it "
                 "below.", class_="blurb"),
            ui.div(ui.input_select("sev_line", "Chance above its",
                                   {k: f"{n.lower()} line" for k, n in C.SEV_LINES}),
                   ui.input_select("sev_h", "Week",
                                   {str(h): f"{h} week{'s' if h > 1 else ''} ahead "
                                            f"({week_span(d)})"
                                    for h, d in zip(fc.index, fc["target_date"])},
                                   selected=str(hmax)),
                   class_="controls"),
            out("sev_overview"), class_="chart-card"),
        ui.div(
            ui.div(ui.input_select("sev_area", city.info["area_word"].capitalize(),
                                   {a: short(city, a) for a in city.areas},
                                   selected=area if area in city.areas else city.areas[0]),
                   class_="controls"),
            out("sev_detail")),
        analogs_block(city, analogs, now.season, table) if analogs else None,
        ui.div(
            ui.h3("How to read this"),
            ui.tags.ul(
                ui.tags.li("The levels on the other tabs (Low to Very high) are one week against "
                           "these same lines. A season is rated by its highest week, so it is "
                           "never below any of its weeks."),
                ui.tags.li(f"“Against a typical peak” on This week compares the latest week with "
                           f"the median past peak ({city.fmt(city.typical_peak())}). The severity "
                           "lines use the spread of past peaks as well as their middle."),
                ui.tags.li("One indicator only: ED visits for flu-like illness. CDC also weighs "
                           "hospitalizations and deaths, which BPHC does not publish by "
                           "neighborhood, so strictly this measures how intense the season is in "
                           "emergency departments, not how sick people get."),
                *([ui.tags.li(f"Not drawn for Chicago: its activity level is capped at "
                              f"{CHI.info['cap']}, so the same method puts the very-high line at "
                              f"{CHI.fmt(chi_its['IT98'])}, past the top of the scale, and the "
                              f"high line at {CHI.fmt(chi_its['IT90'])}, which needs most ZIP codes "
                              "at or near the cap at once.")] if chi_its else []),
                ui.tags.li("Method: M. Biggerstaff et al., “Systematic assessment of multiple "
                           "routine and near real-time indicators to classify the severity of "
                           "influenza seasons and pandemics in the United States,” American "
                           "Journal of Epidemiology 187(5), 2018, ",
                           ui.tags.a("doi:10.1093/aje/kwx334",
                                     href="https://doi.org/10.1093/aje/kwx334", target="_blank"),
                           ".")),
            class_="card"),
    )


def runtime_block(city: D.CityData):
    """Wall-clock time per model for each weekly forecast: training (or loading the
    season-start fit) plus forecasting all four weeks ahead. Recorded since the
    2026-10-04 forecast."""
    rt = city.runtimes
    if rt is None or rt.empty:
        return None
    if "loaded" not in rt:
        rt = rt.assign(loaded=False)
    rt = rt.assign(loaded=rt["loaded"].eq(True))  # blank (older archives) = trained
    per_run = rt.groupby(["origin", "model"]).agg(seconds=("seconds", "sum"),
                                                  loaded=("loaded", "all")).reset_index()
    latest = per_run["origin"].max()
    rows = []
    for m in city.models:
        mine = per_run[per_run["model"] == m]
        if m == "persistence" or mine.empty:
            continue
        now = mine.loc[mine["origin"] == latest, "seconds"]
        cfg = rt[(rt["model"] == m) & (rt["origin"] == latest)].iloc[0]
        trained = rt[(rt["model"] == m) & ~rt["loaded"] & (rt["epochs"].fillna(1) > 0)]
        fresh = trained.groupby("origin")["seconds"].sum()
        if cfg["loaded"]:
            settings = "loaded from the season-start fit"
        elif pd.notna(cfg.get("n_seeds")) and pd.notna(cfg.get("epochs")):
            settings = f"{int(cfg['n_seeds'])} seeds × {int(cfg['epochs'])} epochs"
        else:
            settings = "fitted per neighborhood, no training passes"
        rows.append(ui.tags.tr(ui.tags.td(D.MODEL_SHORT.get(m, m)),
                               ui.tags.td(duration(now.sum()) if len(now) else "—"),
                               ui.tags.td(duration(fresh.median()) if len(fresh) else "—"),
                               ui.tags.td(settings)))
    machines = sorted(rt.loc[rt["origin"] == latest, "machine"].dropna().unique())
    where = f" on {', '.join(machines)}" if machines else ""
    return ui.div(
        ui.h3("How long each model takes"),
        ui.p(f"Time to forecast all four weeks ahead from data through {week_end(latest)}"
             f"{where}. Every model is trained once at the start of the season and loaded "
             "unchanged each week, which gives the same numbers as retraining from the season "
             "start; “Training from scratch” is what a weekly retrain used to take. “Same as "
             "last week” needs no training, so it is left out.", class_="blurb"),
        ui.div(ui.tags.table(ui.tags.thead(ui.tags.tr(
            *[ui.tags.th(t) for t in ("Model", "This week", "Training from scratch",
                                      "Settings")])),
            ui.tags.tbody(*rows), class_="score-table"), class_="table-scroll"),
        class_="chart-card")


def n_members() -> str:
    """How many models the Average combines, in words (four on the site; the BPHC
    folder's weekly run has three)."""
    members = (B.meta.get("ensemble") or {}).get("members") or [
        m for m in B.models if m not in ("avg", "persistence")]
    return {2: "two", 3: "three", 4: "four", 5: "five"}.get(len(members), str(len(members)))


def how_panel(download=ui.download_button):
    shorts = {a: short(B, a) for a in B.areas}
    return ui.div(
        ui.h2("How the forecast works"),
        ui.tags.blockquote(
            ui.p("“All models are wrong, but some are useful.”"),
            ui.tags.footer("— George E. P. Box"),
            class_="epigraph"),
        ui.div(
            ui.div(ui.h4("What it forecasts"), ui.p(
                f"Weekly {B.info['unit']}, for each of BPHC's {len(B.areas)} reporting "
                "neighborhoods, one to four weeks past the latest reported week. Each "
                "forecast is a range, not a single number.", class_="blurb"), class_="note-card"),
            ui.div(ui.h4("Why neighbors matter"), ui.p(
                "Flu moves between people who live, work and commute near each other. The "
                "model is a graph neural network: it reads each neighborhood's recent weeks "
                "together with its neighbors' (the lines on the map), plus weather and the "
                "time of year.", class_="blurb"), class_="note-card"),
            ui.div(ui.h4("How to read the ranges"), ui.p(
                "The darker band is where the number will likely land (half the time); the "
                "lighter band is the plausible range (95% of the time). Ranges widen further "
                "ahead because the future is less certain, and the track record tab checks "
                "that they really hold.", class_="blurb"), class_="note-card"),
            class_="note-grid"),
        ui.div(ui.h3("The neighborhood network"),
               ui.p("Each line joins two neighborhoods that share a border; larger dots have "
                    "more neighbors. Hover a line or a dot.", class_="blurb"),
               ui.HTML(C.network(B.geo, B.edges, shorts)), class_="chart-card"),
        runtime_block(B),
        ui.div(ui.h3("Data and caveats"),
               ui.tags.ul(
                   ui.tags.li(f"Boston: {B.info['source']}. Small counts are suppressed by BPHC "
                              "and appear as “not reported”."),
                   ui.tags.li("Weather: Open-Meteo.com historical archive (CC BY 4.0)."),
                   *([ui.tags.li(f"Chicago: {CHI.info['source']}. {CHI.info['disclaimer']}")]
                     if CHI else []),
                   ui.tags.li("Reporting delays and later revisions are not modeled: a forecast "
                              "uses the numbers as published on the day it is made."),
                   ui.tags.li(f"“Average” is the {n_members()} models' forecasts averaged point by point "
                              "along each range (every quantile), the way CDC's forecasting hubs "
                              "combine teams. It is not trained on its own, and the Track record "
                              "tab scores it like the others."),
                   ui.tags.li("Levels (low to very high) compare a week with that "
                              "neighborhood's intensity lines from the moving epidemic method, "
                              "fitted on its past seasons as in the paper: moderate from the 50% "
                              "line, high from the 90%, very high from the 98%. The Severity tab "
                              "works them out."),
                   ui.tags.li("The 2025-26 season was used to design the model, so its numbers "
                              "are not independent evidence; the published evaluation uses "
                              "earlier seasons, and 2026-27 is scored live.")),
               class_="card"),
        ui.div(ui.h3("Get the numbers"),
               ui.p("The current forecast for every neighborhood, model and week, with 23 "
                    "quantiles. The FluSight file follows the CDC forecast-hub layout.",
                    class_="blurb"),
               ui.div(download("dl_csv", "Forecast (CSV)"),
                      download("dl_flusight", "FluSight format (CSV)"),
                      class_="controls"),
               class_="card"),
    )


app = App(app_ui, server, static_assets=None)
