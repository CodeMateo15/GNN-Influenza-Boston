"""Build the 12/3 research-event poster (36 x 24 in) from scratch with python-pptx.

Numbers come from `Paper/scripts/make_tables.py` (the code that writes the paper's tables). Each one is
checked against the value printed in the submitted paper (AJE_main.pdf, Tables 2, 3 and 5), and the
build stops on any difference. Figures come from `make_poster_figures.py`, so run that first:

    /opt/anaconda3/bin/python "Poster/12:3 Research Event/make_poster_figures.py"
    /opt/anaconda3/bin/python "Poster/12:3 Research Event/build_poster.py"

Layout is a flow: each card measures its own text with the real Avenir Next font files, cards stack
down their column, and the build stops if any text box is too small for its words, any element pokes
out of its card, or a column runs past the bottom of the poster.
"""

import re
import subprocess
from pathlib import Path

from lxml import etree
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "GNN_Flu_Poster_36x24.pptx"
FIG = HERE / "figures"
SEAL_DECK = Path.home() / "ncaaBaseballDraft-Predictor" / "CSV+Code Files" / "CMSAC Poster Material" / \
    "CMSAC_2026_MLB_Draft_Poster_48x36.pptx"   # only the NU seal image is read from this deck

# ---------------------------------------------------------------- palette and type
BG, CARD, CARD_LINE = "F4F2ED", "FFFFFF", "DCD7CC"
INK, MUTED = "1E2A32", "5B6770"
TEAL, TEAL_DARK, TEAL_LIGHT = "0B5D5E", "083F40", "E4EFEE"
AMBER, AMBER_SOFT, AMBER_LIGHT = "C96F1C", "F2A65A", "FBEBDC"
FONT = "Avenir Next"
TTC = "/System/Library/Fonts/Avenir Next.ttc"
FACE = {(False, False): 7, (True, False): 0, (False, True): 4, (True, True): 1}  # (bold, italic) -> ttc index
LINE = 1.366          # Avenir Next ascent + descent (hhea, OS/2 win and typo agree), in em
SAFE_H, SAFE_W = 1.05, 0.97   # measure 5% taller and 3% narrower than nominal, for renderer differences

# ---------------------------------------------------------------- grid (inches)
W_SLIDE, H_SLIDE = 36.0, 24.0
M = 0.75
GAP = 0.375
COL_W = [9.5, 14.75, 9.5]
COL_X = [M, M + COL_W[0] + GAP, M + COL_W[0] + GAP + COL_W[1] + GAP]
PAD = 0.35            # inside a card
BODY_TOP = 3.7
BODY_BOTTOM = 21.3
STRIP_Y, STRIP_H = 21.6, 1.45   # key-findings strip, between the columns and the footer
PAD_B = 0.3          # below a card's last element
BODY = 18             # body text, pt


# ---------------------------------------------------------------- numbers
# Values as printed in AJE_main.pdf. make_tables.py must reproduce them exactly.
PAPER = {
    "boston_wis": {  # Table 2: mean WIS h1 h2 h4, relative WIS h1 h2 h4
        "Graph neural network": (5.13, 6.47, 8.22, 0.82, 0.81, 0.72),
        "LSTM": (5.18, 6.82, 9.16, 0.83, 0.86, 0.80),
        "Cola-GNN": (5.35, 7.61, 8.77, 0.86, 0.96, 0.77),
        "Seasonal ARIMA": (6.52, 7.66, 9.15, 1.04, 0.97, 0.80),
        "Seasonal blend, no learning": (5.95, 7.29, 9.57, 0.95, 0.92, 0.84),
        "Persistence": (6.24, 7.94, 11.44, 1.00, 1.00, 1.00),
    },
    "chicago_rel": (0.81, 0.83, 0.83),
    "table3": {  # % more WIS (seasons clearly worse): Boston h1 h2 h4, Columbus h1 h2 h4, Chicago h1 h2 h4
        "No environment": ["0.1 (0)", "-0.9 (0)", "2.1 (0)", "0.9 (0)", "3.7 (0)", "-0.3 (0)",
                           "-0.6 (0)b", "-0.1 (0)b", "1.7 (1)"],
        "No demographics": ["1.9 (1)", "-0.9 (0)", "0.3 (0)", "-1.3 (0)", "2.1 (0)", "0.9 (0)",
                            "0.1 (0)", "0.1 (0)", "2.3 (0)"],
        "No map": ["10.8 (3)", "3.8 (2)", "5.6 (2)", "15.8 (0)", "6.9 (0)", "1.2 (0)",
                   "7.4 (4)", "6.0 (3)", "3.6 (0)"],
    },
    "columbus_transfer_h1": (4.11, 3.90),   # Table 5: trained locally, transferred from Boston
}


def paper_tables() -> str:
    r = subprocess.run(["/opt/anaconda3/bin/python", str(ROOT / "Paper" / "scripts" / "make_tables.py")],
                       capture_output=True, text=True, check=True, cwd=ROOT)
    return r.stdout


def section(txt: str, header: str) -> list[str]:
    lines = txt.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(header))
    out = []
    for l in lines[i + 1:]:
        if not l.strip() or l.startswith("%"):
            break
        out.append(l)
    return out


def cells(line: str) -> list[str]:
    line = line.replace("$-$", "-").replace("$^{b}$", "b").rstrip("\\ ").strip()
    return [c.strip() for c in line.split("&")]


def load_numbers() -> dict:
    txt = paper_tables()
    t2 = {cells(l)[0]: tuple(float(v) for v in cells(l)[1:7])
          for l in section(txt, "% boston: WIS h1 h2 h4")}
    for model, vals in PAPER["boston_wis"].items():
        assert t2[model] == vals, f"Table 2 {model}: code {t2[model]} != paper {vals}"
    chi = {cells(l)[0]: tuple(float(v) for v in cells(l)[4:7]) for l in section(txt, "% chicago: WIS h1 h2 h4")}
    assert chi["Graph neural network"] == PAPER["chicago_rel"], chi["Graph neural network"]
    t3 = {cells(l)[0]: cells(l)[1:] for l in section(txt, "% Table 3:")}
    for row, vals in PAPER["table3"].items():
        assert t3[row] == vals, f"Table 3 {row}: code {t3[row]} != paper {vals}"
    t5 = section(txt, "% Table 5:")
    col = cells(t5[0])
    assert col[0] == "Columbus (from Boston)" and col[1] == "1"
    assert (float(col[2]), float(col[3])) == PAPER["columbus_transfer_h1"], col
    print("all poster numbers match AJE_main.pdf Tables 2, 3 and 5")
    return {"t2": t2, "t3": t3}


# ---------------------------------------------------------------- text measurement
_fonts: dict = {}


def font(bold: bool, italic: bool, pt: float):
    key = (bold, italic, pt)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(TTC, size=round(pt * 20), index=FACE[(bold, italic)])
    return _fonts[key]


def text_w(s: str, bold=False, italic=False, pt=BODY) -> float:
    """Width in inches."""
    return font(bold, italic, pt).getlength(s) / 20 / 72


def runs_of(para) -> list[tuple[str, str]]:
    return [(para, "")] if isinstance(para, str) else para


def para_lines(para, width: float, pt: float, hang: float) -> int:
    """Greedy word wrap, as PowerPoint does; wrapped lines are `hang` inches narrower."""
    words = []           # (word, trailing-space width, bold, italic)
    for txt, st in runs_of(para):
        b, i = "b" in st, "i" in st
        for tok in re.split(r"(?<= )", txt):
            if tok:
                n_sp = len(tok) - len(tok.rstrip(" "))
                words.append((tok.rstrip(" "), text_w(" ", b, i, pt) * n_sp, b, i))
    lines, x, avail = 1, 0.0, width * SAFE_W
    for w, sp, b, i in words:
        ww = text_w(w, b, i, pt)
        assert ww <= (width - hang) * SAFE_W, f"word too wide for its box: {w!r}"
        if x > 0 and x + ww > avail:
            lines += 1
            avail = (width - hang) * SAFE_W
            x = 0.0
        x += ww + sp
    return lines


def text_height(paras, width, pt, spacing=1.0, space_after=0.0, hangs=None) -> float:
    h = 0.0
    for k, p in enumerate(paras):
        n = para_lines(p, width, pt, (hangs or [0] * len(paras))[k])
        h += n * pt * LINE * spacing / 72 * SAFE_H
        if k < len(paras) - 1:
            h += space_after / 72
    return h


# ---------------------------------------------------------------- pptx helpers
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W_SLIDE), Inches(H_SLIDE)
slide = prs.slides.add_slide(prs.slide_layouts[6])
CHECK: list = []      # [shape, containing card box or None]


def rgb(h):
    return RGBColor.from_string(h)


def rect(x, y, w, h, fill, line=None, radius=0.0, line_w=1.0):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                                Inches(x), Inches(y), Inches(w), Inches(h))
    st = sh._element.find(qn("p:style"))     # drop the theme style: no shadow, no theme line
    if st is not None:
        sh._element.remove(st)
    if radius:
        sh.adjustments[0] = radius / min(w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb(fill)
    if line:
        sh.line.color.rgb = rgb(line)
        sh.line.width = Pt(line_w)
    else:
        sh.line.fill.background()
    return sh


def run_style(r, st, pt, color):
    f = r.font
    f.name, f.size = FONT, Pt(pt)
    f.bold, f.italic = "b" in st, "i" in st
    f.color.rgb = rgb(AMBER if "a" in st else TEAL if "t" in st else color)


def text(x, y, w, paras, pt=BODY, color=INK, spacing=1.0, space_after=0.0, align=PP_ALIGN.LEFT,
         bullets=False, h=None, anchor=MSO_ANCHOR.TOP):
    """Text box sized to its measured height (or `h`, which must be enough). Returns its bottom.

    paras: list of str or [(text, style)] runs; style letters b bold, i italic, t teal, a amber.
    bullets: paragraphs that start with '•  ' or 'N.  ' get a hanging indent under that prefix.
    """
    hangs = []
    for p in paras:
        first = runs_of(p)[0]
        m = re.match(r"(•  |\d\.  )", first[0]) if bullets else None
        hangs.append(text_w(m.group(1), "b" in first[1], "i" in first[1], pt) if m else 0.0)
    need = text_height(paras, w, pt, spacing, space_after, hangs)
    if h is None:
        h = need + 0.04
    assert h >= need, f"text needs {need:.2f} in, box is {h:.2f}: {str(paras[0])[:60]}"
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap, tf.auto_size = True, MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for k, p in enumerate(paras):
        para = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        if k < len(paras) - 1 and space_after:
            para.space_after = Pt(space_after)
        if hangs[k]:
            ppr = para._p.get_or_add_pPr()
            ppr.set("marL", str(Inches(hangs[k])))
            ppr.set("indent", str(-Inches(hangs[k])))
        for txt, st in runs_of(p):
            r = para.add_run()
            r.text = txt
            run_style(r, st, pt, color)
    CHECK.append([tb, None])
    return y + h


def picture(path, x, y, w):
    im = Image.open(path)
    h = w * im.height / im.width
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    CHECK.append([pic, None])
    return y + h


def cell_border(cell, color, w_pt):
    """Only a bottom rule; the other three sides get no line."""
    tcPr = cell._tc.get_or_add_tcPr()
    for k, side in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        bottom = side == "a:lnB"
        ln = etree.Element(qn(side), w=str(Pt(w_pt) if bottom else 0))
        if bottom:
            etree.SubElement(etree.SubElement(ln, qn("a:solidFill")), qn("a:srgbClr"), val=color)
        else:
            etree.SubElement(ln, qn("a:noFill"))
        tcPr.insert(k, ln)


def table(x, y, widths, rows, pt=15, row_h=0.44, styles=None, fills=None):
    """Native table, every cell styled explicitly. styles[r]/fills[r] style row r; row 0 is the header."""
    styles, fills = styles or {}, fills or {}
    mar_lr, mar_tb = 0.08, 0.05
    assert row_h >= pt * LINE / 72 * SAFE_H + 2 * mar_tb, "rows too short for the font"
    shp = slide.shapes.add_table(len(rows), len(widths), Inches(x), Inches(y),
                                 Inches(sum(widths)), Inches(row_h * len(rows)))
    tbl = shp.table
    tbl.first_row = tbl.horz_banding = False
    sid = tbl._tbl.tblPr.find(qn("a:tableStyleId"))
    if sid is not None:
        sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"   # "No Style, No Grid"
    for j, wd in enumerate(widths):
        tbl.columns[j].width = Inches(wd)
    for i, row in enumerate(rows):
        tbl.rows[i].height = Inches(row_h)
        head = i == 0
        for j, val in enumerate(row):
            c = tbl.cell(i, j)
            c.margin_left = c.margin_right = Inches(mar_lr)
            c.margin_top = c.margin_bottom = Inches(mar_tb)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            st = "b" if head else styles.get(i, "")
            assert text_w(val, "b" in st, "i" in st, pt) <= (widths[j] - 2 * mar_lr) * SAFE_W, \
                f"table cell too narrow: {val!r}"
            tf = c.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = val
            run_style(r, st, pt, "FFFFFF" if head else INK)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(TEAL if head else fills.get(i, "FFFFFF"))
            cell_border(c, TEAL if head else CARD_LINE, 0.75)
    CHECK.append([shp, None])
    return y + row_h * len(rows)


def callout(card, y, paras, pt=16):
    """A light-teal box inside a card, for a definition or an example. Returns its bottom."""
    pad = 0.18
    bg = rect(card.cx, y, card.cw, 1.0, TEAL_LIGHT, radius=0.1)
    CHECK.append([bg, None])
    b = text(card.cx + pad, y + pad * 0.8, card.cw - 2 * pad, paras, pt=pt)
    bg.height = Inches(b + pad - y)
    bg.adjustments[0] = 0.1 / min(card.cw, b + pad - y)
    return b + pad


class Card:
    """White rounded card with a teal question heading and a short amber underline."""

    def __init__(self, col, y, title, head_pt=28):
        self.x, self.y, self.w = COL_X[col], y, COL_W[col]
        self.first = len(CHECK)
        self.bg = rect(self.x, y, self.w, 1.0, CARD, CARD_LINE, radius=0.18)
        self.cx, self.cw = self.x + PAD, self.w - 2 * PAD
        head = text(self.cx, y + 0.24, self.cw, [[(title, "b")]], pt=head_pt, color=TEAL)
        self.bar = rect(self.cx + 0.02, head + 0.06, 1.2, 0.07, AMBER)
        self.top = head + 0.26           # where content starts

    def members(self):
        return CHECK[self.first:self.last]

    def close(self, bottom, extra=0.0):
        self.last = len(CHECK) if not hasattr(self, "last") else self.last
        self.h = bottom + PAD_B - self.y + extra
        self.bg.height = Inches(self.h)
        self.bg.adjustments[0] = 0.18 / min(self.w, self.h)   # corner radius is relative to the short side
        return self.y + self.h

    def shift(self, dy):
        for sh in [self.bg, self.bar] + [m[0] for m in self.members()]:
            sh.top = sh.top + Inches(dy)
        self.y += dy


def flow(col, builders):
    """Stack a column's cards; give each an equal share of the leftover height as bottom padding."""
    y, made = BODY_TOP, []
    for build in builders:
        c, bottom = build(col, y)
        made.append([c, bottom])
        y = c.close(bottom) + GAP
    slack = BODY_BOTTOM - (y - GAP)
    print(f"column {col + 1} card heights:", ", ".join(f"{c.h:.2f}" for c, _ in made))
    assert slack >= -1e-6, f"column {col + 1} runs {-slack:.2f} in past the bottom"
    extra = slack / len(made)
    for k, (c, bottom) in enumerate(made):
        c.shift(extra * k)
        c.close(bottom + extra * k, extra)
        for m in c.members():
            m[1] = (c.x, c.y, c.w, c.h)
    print(f"column {col + 1}: {slack:.2f} in to spare, spread across {len(made)} cards")


def seal_image() -> Path:
    """The NU seal picture from the CMSAC deck, saved once to figures/."""
    out = FIG / "nu_seal.png"
    if not out.exists():
        deck = Presentation(SEAL_DECK)
        pic = next(s for s in deck.slides[0].shapes if s.shape_id == 86)
        out.write_bytes(pic.image.blob)
    return out


def check():
    E = 914400
    for sh, box in CHECK:
        x, y, w, h = sh.left / E, sh.top / E, sh.width / E, sh.height / E
        assert x >= 0 and y >= 0 and x + w <= W_SLIDE + 1e-3 and y + h <= H_SLIDE + 1e-3, f"{sh.name} off the slide"
        if box:
            bx, by, bw, bh = box
            assert bx + 0.1 <= x and x + w <= bx + bw - 0.1 and by + 0.1 <= y and y + h <= by + bh - 0.1, \
                f"{sh.name} pokes out of its card ({x:.2f},{y:.2f},{w:.2f},{h:.2f}) vs {box}"
    print(f"all {len(CHECK)} text boxes, tables and pictures sit inside their cards and the slide")


# ---------------------------------------------------------------- build
def main():
    nums = load_numbers()
    t2, t3 = nums["t2"], nums["t3"]

    rect(0, 0, W_SLIDE, H_SLIDE, BG)

    # ---- header: title, authors, QR codes, seal
    y = text(M, 0.32, 20.5, [[("Forecasting Influenza by Neighborhood", "b")],
                             [("with a Graph Neural Network", "bt")]], pt=56, spacing=0.92)
    y = text(M, y + 0.06, 20.5, [[("Mateo Biggs, Deahan Yu", "b")]], pt=28)
    text(M, y, 20.5, ["Advisor: Prof. Ariel Hamlin  ·  Khoury College of Computer Sciences, "
                      "Northeastern University"], pt=19, color=MUTED)
    qr = 2.35
    for k, (path, head, lines) in enumerate((
            (FIG / "qr_app.png", "Boston Flu Outlook",
             ["Live app: this season’s forecasts, updated weekly", [("Not part of the paper’s evidence", "i")]]),
            (FIG / "qr_package.png", "areaFluForecast",
             ["Python package: run it on your own city’s data", [("pip install areaFluForecast", "i")]]))):
        qx = 21.6 + k * 5.2
        rect(qx - 0.08, 0.42 - 0.08, qr + 0.16, qr + 0.16, "FFFFFF", CARD_LINE, radius=0.08)
        picture(path, qx, 0.42, qr)
        text(qx + qr + 0.22, 0.45, 2.45, [[(head, "bt")]] + lines, pt=15, space_after=3)
    picture(seal_image(), W_SLIDE - M - 2.75, 0.38, 2.75)

    # ---- key-findings strip
    sy, sh_ = STRIP_Y, STRIP_H
    tiles = [
        ("18–28%", "less forecast error than assuming next week = this week (Boston, unseen seasons)"),
        ("14 of 14", "Boston neighborhoods forecast better with the neighbor map, at every lead time"),
        ("93–94%", "of what happened fell inside the model’s 95% forecast range"),
        ("~1 min", "a week on a laptop with the open-source package"),
    ]
    tw = (W_SLIDE - 2 * M - 3 * GAP) / 4
    nw = 3.3
    for k, (num, desc) in enumerate(tiles):
        tx = M + k * (tw + GAP)
        rect(tx, sy, tw, sh_, TEAL_DARK, radius=0.18)
        text(tx + 0.3, sy, nw, [[(num, "b")]], pt=50, color=AMBER_SOFT, h=sh_, anchor=MSO_ANCHOR.MIDDLE)
        text(tx + 0.3 + nw + 0.1, sy, tw - nw - 0.7, [desc], pt=17, color="FFFFFF", h=sh_,
             anchor=MSO_ANCHOR.MIDDLE)
    assert sy >= BODY_BOTTOM + 0.25 and BODY_TOP >= 3.6

    # ================= column 1
    def why(col, y):
        c = Card(col, y, "Why neighborhoods?")
        b = text(c.cx, c.top, c.cw, [
            "Health departments act neighborhood by neighborhood (vaccine clinics, school outreach), "
            "but most flu forecasts cover whole states or regions.",
            [("In Boston, emergency department (ED) visits for influenza-like illness (ILI) run ", ""),
             ("7× higher", "b"), (" in Dorchester than in Fenway (67 vs 9 per 100,000 a week).", "")],
            [("We asked:", "b")],
            [("1.  Does a ", ""), ("graph neural network", "b"), (" beat simpler forecasts?", "")],
            [("2.  Which inputs help: a ", ""), ("map of neighboring areas", "b"), (", weather, or demographics?", "")],
            [("3.  Can the map be built automatically, and does a model ", ""), ("carry over to a new city", "b"),
             ("?", "")],
        ], pt=BODY, space_after=6, bullets=True)
        return c, b

    def data(col, y):
        c = Card(col, y, "Data: three cities")
        map_w = 4.0
        b1 = text(c.cx, c.top, c.cw - map_w - 0.25, [
            [("Boston: ", "bt"), ("14 neighborhoods, weekly ED visits for ILI per 100,000, 2017–2026", "")],
            [("Chicago: ", "bt"), ("58 ZIP codes, weekly flu activity level (1–10)", "")],
            [("Columbus, OH: ", "bt"), ("17 planning areas, ED visits", "")],
            [("Inputs, each area and week:", "b")],
            "•  its past 16 weeks",
            "•  6 weather variables",
            "•  8 demographic measures",
            "•  a map of which areas share a border",
        ], pt=17, space_after=4, bullets=True)
        b2 = picture(FIG / "p_fig1a_map.png", c.cx + c.cw - map_w, c.top - 0.05, map_w)
        b2 = text(c.cx + c.cw - map_w, b2 + 0.02, map_w,
                  [[("Boston’s map. Lines join areas that share a border; dashed links cross water.", "i")]],
                  pt=12, color=MUTED)
        return c, max(b1, b2)

    def model(col, y):
        c = Card(col, y, "How the model works")
        b = picture(FIG / "p_model_simple.png", c.cx, c.top + 0.05, c.cw)
        b = text(c.cx, b + 0.2, c.cw, [
            [("Forecast", "b"), (" = this week blended with the usual seasonal curve, plus a learned correction "
                                 "that mixes in neighbors’ signals.", "")],
            [("A fair test: ", "bt"), ("scored only on seasons never used to design it; every learned model got "
                                       "the same tuning budget; each forecast averages 10 training runs.", "")],
        ], pt=17, space_after=6)
        return c, b

    # ================= column 2
    def beats(col, y):
        c = Card(col, y, "Does it beat simpler forecasts?")
        b = text(c.cx, c.top, c.cw, [
            [("How far off is a forecast, counting its uncertainty? ", "b"),
             ("The weighted interval score (WIS) scores the whole forecast range; lower is better. Dividing "
              "by persistence’s score gives relative error: ", ""),
             ("below 1 beats persistence.", "b")]], pt=BODY)
        b = callout(c, b + 0.2, [
            [("What is persistence? ", "bt"),
             ("The simplest forecast there is: whatever happened this week happens again. ", ""),
             ("Example: ", "b"),
             ("in the week of Feb 2, 2025, Dorchester had 294 ED visits for ILI per 100,000, its peak. "
              "Persistence forecast 294 for every week ahead. The real rate fell to 217 a week later and "
              "84 four weeks later; the graph model forecast 252 and 135.", "")]])
        b = text(c.cx, b + 0.22, c.cw, [[("Boston, 3 unseen seasons: average error per 100,000 "
                                          "(relative to persistence)", "b")]], pt=15, color=MUTED)
        fmt = lambda m, k: f"{t2[m][k]:.2f}  ({t2[m][k + 3]:.2f})"
        show = [("Graph neural network", "Graph neural network"), ("LSTM (no map)", "LSTM"),
                ("Cola-GNN", "Cola-GNN"), ("Seasonal ARIMA", "Seasonal ARIMA"),
                ("Seasonal blend", "Seasonal blend, no learning"), ("Persistence", "Persistence")]
        widths = [4.55, 3.15, 3.15, 3.15]
        b = table(c.cx + (c.cw - sum(widths)) / 2, b + 0.08, widths,
                  [["Model", "1 week", "2 weeks", "4 weeks"]] +
                  [[lab] + [fmt(m, k) for k in range(3)] for lab, m in show],
                  pt=15, row_h=0.4, styles={1: "bt"}, fills={1: TEAL_LIGHT})
        fw = 9.6
        b = picture(FIG / "p_relative_wis.png", c.cx + (c.cw - fw) / 2, b + 0.25, fw)
        lo, hi = 100 - 100 * max(PAPER["chicago_rel"]), 100 - 100 * min(PAPER["chicago_rel"])
        b = text(c.cx, b + 0.15, c.cw, [
            f"•  Chicago: {lo:.0f}–{hi:.0f}% less error than persistence. A tuned LSTM tied it at 1 week in Boston.",
        ], pt=BODY, space_after=3, bullets=True)
        return c, b

    def paths(col, y):
        c = Card(col, y, "What did the forecasts look like?")
        fw = 11.6
        b = picture(FIG / "p_forecast_paths.png", c.cx + (c.cw - fw) / 2, c.top + 0.05, fw)
        b = text(c.cx, b + 0.12, c.cw, [[
            ("Dorchester, 2024–25. ", "b"),
            ("Each blue path is one forecast made on the circled week, drawn 1, 2 and 4 weeks ahead. "
             "At the peak the model forecast the drop while persistence stayed flat; in the January surge "
             "it climbed too slowly.", "")]], pt=15)
        return c, b

    # ================= column 3
    def inputs(col, y):
        c = Card(col, y, "Which inputs help? Remove one")
        b = text(c.cx, c.top, c.cw, [[("The map carries the gain. ", "ba"),
                                      ("Retrain without one input and see how much error rises. "
                                       "Without weather or demographics it barely moved.", "")]], pt=17)
        b = text(c.cx, b + 0.2, c.cw, [[("% more error with the input removed "
                                         "(seasons clearly worse)", "b")]], pt=14, color=MUTED)
        sgn = lambda v: v if v.startswith("-") else "+" + v

        def row(name, key, city):
            lo, n = (0, 3) if city == "Boston" else (6, 4)
            out = []
            for v in t3[key][lo:lo + 3]:
                m = re.match(r"(-?[\d.]+) \((\d)\)(b?)", v)
                out.append(f"{sgn(m.group(1))} ({m.group(2)}/{n}){'†' if m.group(3) else ''}")
            return [name, city] + out
        widths = [2.05, 1.5, 1.75, 1.75, 1.75]
        b = table(c.cx + (c.cw - sum(widths)) / 2, b + 0.06, widths,
                  [["Removed", "City", "1 week", "2 weeks", "4 weeks"],
                   row("Map", "No map", "Boston"), row("Map", "No map", "Chicago"),
                   row("Weather", "No environment", "Boston"), row("Weather", "No environment", "Chicago"),
                   row("Demographics", "No demographics", "Boston"),
                   row("Demographics", "No demographics", "Chicago")],
                  pt=13.5, row_h=0.38, styles={1: "b", 2: "b"}, fills={1: AMBER_LIGHT, 2: AMBER_LIGHT})
        b = text(c.cx, b + 0.08, c.cw, [[("Clearly worse = Holm-adjusted Diebold–Mariano P < .05. "
                                          "† Chicago without weather was clearly better in some seasons.", "i")]],
                 pt=11.5, color=MUTED)
        fw = 6.7
        b = picture(FIG / "p_map_benefit.png", c.cx + (c.cw - fw) / 2, b + 0.2, fw)
        b = text(c.cx, b + 0.05, c.cw, [[("The map lowered error in all 14 Boston neighborhoods at every lead "
                                          "time (3 unseen seasons averaged).", "i")]], pt=13, color=MUTED)
        return c, b

    def carry(col, y):
        c = Card(col, y, "Does it carry over?")
        t5 = PAPER["columbus_transfer_h1"]
        b = text(c.cx, c.top, c.cw, [
            [("•  Automatic maps work: ", "b"), ("built from public boundary files, they matched the hand-drawn "
                                                  "map (no clear difference in 36 comparisons)", "")],
            [("•  Borrowed models: ", "b"), (f"a Boston-trained model forecast Columbus as well as a local one "
                                              f"(error {t5[1]:.2f} vs {t5[0]:.2f} at 1 week)", "")],
            [("•  Ready to use: ", "b"), ("the open-source package reproduces the Boston results within 0.4%", "")],
        ], pt=17, space_after=6, bullets=True)
        return c, b

    def takeaways(col, y):
        c = Card(col, y, "Takeaways & next steps")
        b = text(c.cx, c.top, c.cw, [
            [("1.  ", "bt"), ("The ", ""), ("neighbor map", "b"),
             (", not weather or demographics, carries the gain", "")],
            [("2.  ", "bt"), ("A health department needs only weekly area rates and public boundary files", "")],
            [("3.  ", "bt"), ("Next: a live test this season, wastewater as an earlier signal, "
                              "Buenos Aires", "")],
        ], pt=17, space_after=6, bullets=True)
        return c, b

    for col, builders in ((0, [why, data, model]), (1, [beats, paths]), (2, [inputs, carry, takeaways])):
        flow(col, builders)

    # ---- footer: references and event line
    fy = STRIP_Y + STRIP_H + 0.2
    rect(0, fy, W_SLIDE, H_SLIDE - fy, TEAL_DARK)
    refs = ("[1] Kipf & Welling (2017). Semi-supervised classification with graph convolutional networks. ICLR.   "
            "[2] Bracher et al. (2021). Evaluating epidemic forecasts in an interval format. PLoS Comput Biol.   "
            "[3] Deng et al. (2020). Cola-GNN: cross-location attention for long-term ILI prediction. CIKM.   "
            "[4] Yang, Olson & Shaman (2016). Forecasting influenza in boroughs and neighborhoods of NYC. "
            "PLoS Comput Biol.   [5] Boston Public Health Commission. Influenza surveillance dashboard, 2026.")
    text(M, fy, 24.0, [refs], pt=11, color="D5E4E2", h=H_SLIDE - fy, anchor=MSO_ANCHOR.MIDDLE)
    text(W_SLIDE - M - 9.5, fy, 9.5, [[("December 3, 2026  ·  Northeastern University", "b")],
                                       "github.com/CodeMateo15/GNN-Influenza-Boston"],
         pt=15, color="FFFFFF", h=H_SLIDE - fy, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

    prs.save(OUT)
    print(f"saved {OUT}")
    check()


if __name__ == "__main__":
    main()
