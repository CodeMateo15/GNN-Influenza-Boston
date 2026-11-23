# Generated copy of boston-flu-outlook/export_html.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Write the whole site as one HTML file that opens offline, with no server.

    python export_html.py --out boston_flu_outlook.html
    python export_html.py --data path/to/data --out site.html    # another published data folder

The Shiny app computes each view when it is asked for. Here every view is
rendered ahead of time instead (each neighborhood, weeks-ahead step, sort order,
severity line and audience) through the app's own layout (`app.build_tabs`), and a
small page script shows the one that matches the controls. Styles, scripts and
the two download files are inlined, so the file makes no network requests: open it
straight from disk, a shared drive or an email attachment.

Differences from the live site, all small: the model ticks on the Neighborhood tab
hide lines rather than redraw the chart, so its scale fits every model; and the
forecast table has no column filters.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERIES = ("s1", "s2", "s3", "s4", "s5", "sref")

STATIC_CSS = """
.mode-root[hidden], .variant[hidden] { display: none !important; }
""" + "".join(f".hide-{s} svg .{s}, .hide-{s} [data-series=\"{s}\"] {{ display: none; }}\n"
              for s in SERIES) + """
.static-slider { display: flex; align-items: center; gap: 10px; }
.static-range { flex: 1; min-width: 160px; }
.static-range .form-range { accent-color: var(--s1, var(--series-1)); }
.static-ticks { display: flex; justify-content: space-between; padding: 0 4px;
                font-size: 12px; color: var(--text-muted); }
.static-play { width: 34px; height: 30px; border: 1px solid var(--border); border-radius: 6px;
               background: var(--surface-1); color: var(--text-primary); line-height: 1; }
.static-theme { border: 1px solid var(--border); border-radius: 6px; padding: 4px 10px;
                background: var(--surface-1); color: var(--text-primary); font-size: 13px; }
.static-table { max-height: 520px; overflow: auto; }
.offline-note { color: var(--text-muted); font-size: 13px; margin: -8px 0 16px; }
"""

# Shows the pre-rendered variant that matches the controls; mirrors the server's
# reactive wiring in app.py (shared neighborhood across tabs, clicks on map shapes,
# the play button, downloads).
STATIC_JS = r"""
(function () {
  var CFG = JSON.parse(document.getElementById("outlook-config").textContent);
  var AREA_INPUTS = ["area", "drv_area", "sev_area"];
  function root() { return document.querySelector(".mode-root:not([hidden])"); }
  function find(r, id) { return r ? r.querySelector('[id="' + id + '"]') : null; }
  function value(r, id) {
    var el = find(r, id);
    if (!el) return null;
    if (el.tagName === "SELECT" || el.type === "range") return el.value;
    if (el.type === "checkbox") return el.checked ? "on" : "off";
    if (el.classList.contains("shiny-input-checkboxgroup"))
      return Array.prototype.map.call(el.querySelectorAll("input:checked"),
                                      function (i) { return i.value; });
    if (el.classList.contains("shiny-input-radiogroup")) {
      var c = el.querySelector("input:checked");
      return c ? c.value : null;
    }
    return null;
  }
  function ticked(r) {
    var v = value(r, "models");
    return v && v.length ? v : [CFG.primary];
  }
  // Same order as app.lead_first: the first ticked model gets the bands and the sentence.
  function lead(models) {
    for (var i = 0; i < CFG.order.length; i++)
      if (models.indexOf(CFG.order[i]) >= 0) return CFG.order[i];
    return CFG.primary;
  }
  function keyOf(r, spec) {
    return spec.split(",").map(function (id) {
      if (id === "models") return lead(ticked(r));
      var v = value(r, id);
      return v == null ? "" : v;
    }).join("|");
  }
  function update(r) {
    if (!r) return;
    r.querySelectorAll(".slot[data-for]").forEach(function (slot) {
      var k = keyOf(r, slot.getAttribute("data-for")), hit = null;
      var kids = slot.querySelectorAll(":scope > .variant");
      kids.forEach(function (v) { if (v.getAttribute("data-key") === k) hit = v; });
      hit = hit || kids[0];
      if (hit && hit.hasAttribute("data-ref")) {
        hit.appendChild(document.getElementById("t-" + hit.getAttribute("data-ref"))
                        .content.cloneNode(true));
        hit.removeAttribute("data-ref");
      }
      kids.forEach(function (v) { v.hidden = v !== hit; });
    });
    var shown = ticked(r);
    r.querySelectorAll('.slot[data-for="area,models"]').forEach(function (slot) {
      Object.keys(CFG.classes).forEach(function (m) {
        slot.classList.toggle("hide-" + CFG.classes[m], shown.indexOf(m) < 0);
      });
    });
    // What the server draws as "selected" for the chosen area, done here instead.
    [["sev_click", "sev_area", ""], ["chi_click", "chi_area", "path"],
     ["drv_click", "drv_area", "svg.matrix "]].forEach(function (x) {
      var chosen = value(r, x[1]);
      r.querySelectorAll(x[2] + '[data-input="' + x[0] + '"]').forEach(function (el) {
        if (el.tagName === "LI") return;
        el.classList.toggle("selected", el.getAttribute("data-area") === chosen);
      });
    });
  }
  function setSelect(r, id, v) {
    var el = find(r, id);
    if (el && el.tagName === "SELECT" &&
        Array.prototype.some.call(el.options, function (o) { return o.value === v; })) el.value = v;
  }
  function showTab(r, name) {
    var a = r && r.querySelector('.nav-link[data-value="' + name + '"]');
    if (a && window.bootstrap) window.bootstrap.Tab.getOrCreateInstance(a).show();
  }
  function pick(name, area) {
    var r = root();
    if (name === "chi_click") {
      setSelect(r, "chi_area", area);
    } else {
      AREA_INPUTS.forEach(function (id) { setSelect(r, id, area); });
      if (name === "area_click") showTab(r, "detail");
    }
    update(r);
  }
  function switchMode(m) {
    var old = root(), next = document.querySelector('.mode-root[data-mode="' + m + '"]');
    if (!next || next === old) return;
    var area = value(old, "area"), tab = old && old.querySelector(".nav-link.active");
    if (old) old.hidden = true;
    next.hidden = false;
    if (area) AREA_INPUTS.forEach(function (id) { setSelect(next, id, area); });
    if (tab) showTab(next, tab.getAttribute("data-value"));
    update(next);
  }
  function themeLabel() {
    var b = document.getElementById("theme-toggle");
    if (b) b.textContent = document.documentElement.getAttribute("data-bs-theme") === "dark"
      ? "Light mode" : "Dark mode";
  }
  function stop(p) { clearInterval(p._timer); p._timer = null; p.textContent = "▶"; }

  document.addEventListener("change", function (e) {
    var t = e.target;
    if (t.id === "audience") { switchMode(t.value); return; }
    var r = t.closest && t.closest(".mode-root");
    if (!r) return;
    if (AREA_INPUTS.indexOf(t.id) >= 0)
      AREA_INPUTS.forEach(function (id) { setSelect(r, id, t.value); });
    update(r);
  });
  document.addEventListener("input", function (e) {
    if (e.target.type === "range") update(e.target.closest(".mode-root"));
  });
  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t.closest) return;
    if (t.closest('[id="to_drivers"]')) { e.preventDefault(); showTab(root(), "drivers"); return; }
    if (t.closest("#theme-toggle")) {
      var html = document.documentElement;
      html.setAttribute("data-bs-theme",
                        html.getAttribute("data-bs-theme") === "dark" ? "light" : "dark");
      themeLabel();
      return;
    }
    var d = t.closest(".static-download");
    if (d) {
      e.preventDefault();
      var src = document.getElementById("file-" + d.getAttribute("data-file"));
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([src.textContent], { type: "text/csv" }));
      a.download = src.getAttribute("data-filename");
      document.body.appendChild(a);
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 0);
      return;
    }
    var p = t.closest(".static-play");
    if (p) {
      var r = root(), s = find(r, p.getAttribute("data-for"));
      if (!s) return;
      if (p._timer) { stop(p); return; }
      if (+s.value >= +s.max) s.value = s.min;
      update(r);
      p.textContent = "❚❚";
      p._timer = setInterval(function () {
        if (+s.value >= +s.max) { stop(p); return; }
        s.value = +s.value + 1;
        update(r);
      }, +p.getAttribute("data-interval"));
    }
  });
  window.OutlookStatic = { pick: pick };
  document.querySelectorAll(".mode-root").forEach(update);
  themeLabel();
})();
"""


class ExportError(Exception):
    """A missing input; the command line turns it into exit status 2."""


def _shiny_file(rel: str) -> Path:
    return Path(importlib.util.find_spec("shiny").origin).parent / rel


def _bootstrap_css() -> str:
    """Bootstrap plus the two stylesheets the app's cards and tabs pull in as
    dependencies (bslib's components, htmltools' fill layout)."""
    css = "\n".join(_shiny_file(f"www/shared/{rel}").read_text() for rel in (
        "bootstrap/bootstrap.min.css", "bslib/components/components.css",
        "htmltools/fill/fill.css"))
    # Bootstrap's bundle pulls in web fonts and glyph icons from files beside it.
    # The page sets its own system fonts and uses no icons, so drop them rather than
    # leave requests for files that are not there.
    css = re.sub(r'@import\s+url\([^)]*\)\s*;?', "", css)
    css = re.sub(r"@font-face\s*\{[^}]*\}", "", css)
    return css


def _script_text(text: str) -> str:
    if "</script" in text.lower():
        raise ExportError("an inlined file contains '</script', which would end the page early")
    return text


def build(data_dir: Path | None = None, *, made: dt.date | None = None) -> str:
    """The whole site as one HTML string, from a published data folder (one
    subfolder per city, as publish.py writes); default: the app's data/."""
    if data_dir is not None:
        data_dir = Path(data_dir).resolve()
        if not (data_dir / "boston" / "meta.json").exists():
            raise ExportError(f"No published Boston data in {data_dir} (expected boston/meta.json).")
        os.environ["OUTLOOK_DATA_DIR"] = str(data_dir)
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    from core import data as D
    if D.BOSTON is None:
        raise ExportError(f"No published Boston data in {D.DATA_DIR}.")
    import app as A
    from shiny import ui

    B, CHI = A.B, A.CHI
    hmax = max(B.horizons)
    order = A.lead_first(B.models)

    # Each variant's content is stored once as a <template> (inert until used; views
    # that come out the same for both audiences are shared) and copied in the first
    # time the controls ask for it, so the page opens without building every view.
    templates: dict[str, str] = {}

    def slot(spec: str, items):
        cells = []
        for key, body in items:
            html = str(body)
            ref = hashlib.sha1(html.encode()).hexdigest()[:16]
            templates.setdefault(ref, html)
            cells.append(ui.div(class_="variant", hidden="",
                                **{"data-key": key, "data-ref": ref}))
        return ui.div(*cells, class_="slot", **{"data-for": spec})

    def table_html(city, model):
        if model not in city.models:
            return ui.p(f"{A.D.MODEL_SHORT.get(model, model)} has no {city.label} forecast.",
                        class_="empty")
        df = A.table_frame(city, model)
        return ui.div(ui.tags.table(
            ui.tags.thead(ui.tags.tr(*[ui.tags.th(c) for c in df.columns])),
            ui.tags.tbody(*[ui.tags.tr(*[ui.tags.td(str(v)) for v in row])
                            for row in df.itertuples(index=False)]),
            class_="score-table"), class_="static-table")

    def outputs(m: str):
        analyst = m == "analyst"

        def out(name: str):
            if name in ("boston_map", "boston_ranked"):
                block = A.map_block if name == "boston_map" else A.ranked_block
                args = (None, "area_click") if name == "boston_map" else ("area_click",)
                return slot("h", ((str(h), block(B, h, *args)) for h in range(0, hmax + 1)))
            if name == "boston_citywide":
                return A.citywide_block(m)
            if name == "detail_body":
                return slot("area,models", (
                    (f"{a}|{lead}", A.detail_html(a, order[order.index(lead):]))
                    for a in B.areas for lead in order))
            if name == "detail_ribbons":
                if B.season_roles():
                    return slot("area,ribbon_set", ((f"{a}|{w}", A.ribbons_block(B, a, w))
                                                    for a in B.areas for w in A.RIBBON_SETS))
                return slot("area", ((a, A.ribbons_block(B, a)) for a in B.areas))
            if name == "drv_body":
                # Same pieces as app.drivers_body; the matrix depends only on the week
                # ahead, and the page script marks the chosen row.
                pairs = [(a, h) for a in B.areas for h in B.horizons]
                return ui.div(
                    slot("drv_area,drv_h", ((f"{a}|{h}", A.drivers_top(a, h, analyst))
                                            for a, h in pairs)),
                    slot("drv_h", ((str(h), A.matrix_block(B, None, h, "drv_click"))
                                   for h in B.horizons)),
                    slot("drv_area,drv_h", ((f"{a}|{h}", A.drivers_bottom(a, h, analyst))
                                            for a, h in pairs)))
            if name == "multiples":
                return slot("sort,shared", ((f"{s}|{'on' if on else 'off'}", A.multiples_html(s, on))
                                            for s in A.SORTS for on in (True, False)))
            if name == "sev_overview":
                # Same pieces as app.severity_overview; the grid is the same for every
                # line and week, and the page script marks the chosen neighborhood.
                return ui.div(
                    slot("sev_line,sev_h", ((f"{line}|{h}", A.severity_table(B, None, line, h))
                                            for line, _ in A.C.SEV_LINES for h in B.horizons)),
                    A.severity_grid_block(B, None))
            if name == "sev_detail":
                return slot("sev_area", ((a, A.severity_area_block(B, a)) for a in B.areas))
            if name == "record":
                return A.record_body(B, m)
            if name in ("chi_map", "chi_ranked"):
                hc = max(CHI.horizons)
                if name == "chi_map":
                    return slot("chi_h", ((str(h), A.map_block(CHI, h, None, "chi_click"))
                                          for h in range(0, hc + 1)))
                return slot("chi_h", ((str(h), A.ranked_block(CHI, h, "chi_click", limit=12))
                                      for h in range(0, hc + 1)))
            if name == "chi_zip":
                return slot("chi_area", ((z, A.chicago_zip(z)) for z in sorted(CHI.areas)))
            if name == "table":
                return slot("tbl_city,tbl_model", ((f"{k}|{mdl}", table_html(c, mdl))
                                                   for k, c in A.D.CITIES.items()
                                                   for mdl in B.models))
            raise ExportError(f"export_html.py does not know the output {name!r}; add it.")

        return out

    def slider(id, label, lo, hi, value, interval):
        return ui.div(
            ui.tags.label(label, class_="control-label", for_=id),
            ui.div(ui.tags.button("▶", type="button", class_="static-play",
                                  **{"data-for": id, "data-interval": str(interval),
                                     "aria-label": f"Play {label.lower()}"}),
                   ui.div(ui.tags.input(type="range", id=id, min=str(lo), max=str(hi),
                                        value=str(value), step="1", class_="form-range"),
                          ui.div(*[ui.span(str(i)) for i in range(lo, hi + 1)],
                                 class_="static-ticks"),
                          class_="static-range"),
                   class_="static-slider"),
            class_="form-group shiny-input-container")

    def download(id, label):
        return ui.tags.a(label, href="#", class_="btn btn-default static-download",
                         **{"data-file": id})

    roots = []
    for m in A.V.MODES:
        tabs = A.build_tabs(m, B.areas[0], "all", out=outputs(m), slider=slider,
                            download=download, table_out=outputs(m))
        html = str(ui.div(tabs))
        # Two audiences share a page: keep their radio and checkbox groups, and the
        # tab panes their tabs point at (#tab-nav-0, ...), apart.
        html = re.sub(r' name="([^"]+)"', lambda g: f' name="{m}-{g.group(1)}"', html)
        html = re.sub(r'(["#])tab-nav-(\d+)"', lambda g: f'{g.group(1)}tab-nav-{m}-{g.group(2)}"',
                      html)
        roots.append(f'<div class="mode-root" data-mode="{m}"{"" if m == "briefing" else " hidden"}>'
                     f"{html}</div>")
    body = "".join(roots)
    # bslib's card script needs the Shiny runtime; the cards look the same without it.
    body = re.sub(r'<script data-bslib-card-init="">.*?</script>', "", body, flags=re.S)

    made = made or dt.date.today()
    note = (f"Offline copy, made {made:%b %-d, %Y} from the forecast of week "
            f"{A.week_span(B.origin)}. It does not update: make a new one each week.")
    theme = ui.tags.button("Dark mode", type="button", id="theme-toggle", class_="static-theme")
    config = {"primary": A.D.PRIMARY, "order": order,
              "classes": {mdl: A.D.MODEL_CLASS.get(mdl, "s1") for mdl in B.models}}
    files = {"dl_csv": (A.download_name("csv"), B.forecast.to_csv(index=False)),
             "dl_flusight": (A.download_name("flusight"), A.D.flusight(B).to_csv(index=False))}
    template_tags = "".join(f'<template id="t-{ref}">{html}</template>'
                            for ref, html in templates.items())
    file_tags = "".join(
        f'<script type="text/csv" id="file-{k}" data-filename="{A.C.esc(name)}">'
        f"{_script_text(text)}</script>" for k, (name, text) in files.items())

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Boston Flu Outlook</title>
<style>{_bootstrap_css()}</style>
<style>{(HERE / "www" / "styles.css").read_text()}</style>
<style>{STATIC_CSS}</style>
<script>{A.THEME_SCRIPT}</script>
</head>
<body>
<div class="container-fluid">
{A.topbar(theme=theme)}
<p class="offline-note">{A.C.esc(note)}</p>
{body}
{A.footer()}
</div>
<noscript><p class="banner">This page needs JavaScript switched on to show its charts.</p></noscript>
{template_tags}
<script type="application/json" id="outlook-config">{json.dumps(config)}</script>
{file_tags}
<script>{_script_text(_shiny_file("www/shared/bootstrap/bootstrap.bundle.min.js").read_text())}</script>
<script>{_script_text((HERE / "www" / "app.js").read_text())}</script>
<script>{STATIC_JS}</script>
</body>
</html>
"""
    # The file must stand alone: nothing fetched from anywhere when it opens.
    external = re.findall(r'<(?:script|link|img|iframe)\b[^>]*\b(?:src|href)="(?!#|data:)[^"]*"',
                          page) + re.findall(r"@import|url\((?![\"']?(?:data:|#))", page)
    if external:
        raise ExportError(f"the page would load outside files: {external[:3]}")
    return page


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--data", type=Path, help="published data folder (default: data/ here)")
    parser.add_argument("--out", type=Path, required=True, help="the .html file to write")
    args = parser.parse_args()
    try:
        page = build(args.data)
    except ExportError as err:
        print(f"export_html.py: {err}", file=sys.stderr)
        raise SystemExit(2)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(page, encoding="utf-8")
    print(f"{len(page.encode()) / 1e6:.1f} MB")
    print(f"Outputs: {args.out}")


if __name__ == "__main__":
    main()
