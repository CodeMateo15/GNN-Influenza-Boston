"""Chart colours, validated as a set rather than chosen by eye.

The categorical slots are assigned in fixed order and never cycled: series 1
always gets SERIES[0], whatever else is on the chart. That ordering is the
colourblind-safety mechanism, not a cosmetic choice.

Validated for the light surface below (4 slots, adjacent pairlist, which is the
right pairlist for lines and bars):

    Lightness band      PASS   all inside L 0.43-0.77
    Chroma floor        PASS   all >= 0.1
    CVD separation      PASS   worst adjacent dE 9.1 (protan)
    Normal-vision floor PASS   worst adjacent dE 22.9
    Contrast vs surface WARN   aqua 2.74:1 and yellow 2.11:1 are below 3:1

The contrast warning is not dismissable: it obliges visible relief. We ship all
three available forms -- a legend on every figure, a distinct marker shape per
series, and a table view of the same numbers in
results/_comparison/comparison_wide.csv.

Figures render on the light surface only, so the dark steps are not used here.
"""

from __future__ import annotations

# Chart surface. Matplotlib's default is pure white; this is the surface the
# palette above was actually validated against.
SURFACE = "#fcfcfb"

# Fixed categorical order: blue, orange, aqua, yellow.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]

# Secondary encoding, so identity never rests on hue alone.
MARKERS = ["o", "s", "^", "D"]

# Ink and chrome. Text always wears an ink colour, never a series colour.
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
AXIS = "#c3c2b7"

# The observed series is the reference the models are judged against, not a peer
# series, so it wears primary ink instead of taking a categorical slot.
ACTUAL = INK_PRIMARY

# Flu-season shading. A background wash, deliberately weak.
SEASON = "#eda100"
SEASON_ALPHA = 0.10

# Ordinal severity bands: low, moderate, high, very high. A sequential
# single-hue ramp, deliberately NOT drawn from SERIES above -- the bands are
# ordered, and encoding an ordered variable with categorical hues loses the
# order. Single-hue sequential ramps are colourblind-safe by construction, since
# they vary in lightness rather than hue. Used as background washes only, with
# the observed series drawn on top in ACTUAL ink, so the sub-3:1 contrast of the
# lighter steps is not carrying any information on its own.
SEVERITY_WASH = ["#f4f3ee", "#fbe3cf", "#f4bd91", "#e28a55"]

BAND_ALPHA = 0.16
LINE_WIDTH = 1.8
ACTUAL_WIDTH = 2.2


def series_colour(index: int) -> str:
    """Colour for the nth series, in fixed order.

    A fifth series is a design decision, not a generated hue: fold models into
    a subset, or facet. Raising here rather than cycling keeps that honest.
    """
    if index >= len(SERIES):
        raise ValueError(
            f"Only {len(SERIES)} validated categorical slots are available, asked for "
            f"index {index}. Plot a subset with --models, or add a facet -- do not "
            "cycle the palette, which would make two models share a colour."
        )
    return SERIES[index]


def marker(index: int) -> str:
    return MARKERS[index % len(MARKERS)]


def style_axes(ax, *, grid_axis: str = "y") -> None:
    """Recessive grid and axes, muted tick labels."""
    ax.set_facecolor(SURFACE)
    ax.grid(axis=grid_axis, color=GRIDLINE, linewidth=0.6, alpha=1.0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(colors=INK_MUTED, labelsize=7, length=3, width=0.8)
