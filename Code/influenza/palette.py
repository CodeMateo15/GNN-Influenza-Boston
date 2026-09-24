"""Chart colours and axis styling, shared by every figure in the project.

This module used to hold a designed palette -- an off-white surface, a validated
four-slot categorical ramp, marker double-encoding, a sequential severity ramp,
recessive gridlines and hidden spines. It produced figures that read as a
template rather than as plots, and it disagreed with `influenza/plots.py`, which
had quietly kept its own three flat-UI colours and plain matplotlib chrome.

Two styles in one repository is the actual defect. This module is now the plain
one, and `plots.py` imports its colours from here instead of redeclaring them,
so the comparison figures and the per-run grids finally look like the same
project.

What "plain" means here, concretely, and why each choice:

  * Default white figure background. Matplotlib's default; nothing to justify.
  * All four spines, in default black. The box is a frame, not decoration.
  * No gridlines. The grids in `plots.py` never had them and the figures read
    fine without; a gridline behind every bar is noise, not information.
  * Default tick and label colours. Text wears black, not a tuned grey.
  * One centred `fig.suptitle` per figure. No left-anchored axes titles, and no
    separate `fig.text()` subtitle paragraph -- caveats belong in stdout and in
    the CSV beside the figure, where they can be read and quoted, not baked into
    a PNG at 8pt.

The colourblind-safety argument the old docstring made was real, and it is not
discarded: SERIES is still a fixed-order list that is never cycled, series 1
always takes SERIES[0], and `series_colour` still raises past the end rather
than wrapping. What changed is the hues, which now match the ones the grid plots
have always used, and the loss of marker double-encoding -- the liked reference
figure distinguishes its two series by line style alone, and every figure here
carries a legend.
"""

from __future__ import annotations

# Plain matplotlib default. Kept as a name because five call sites pass it to
# savefig(facecolor=...); "white" there is a no-op rather than a special case.
SURFACE = "white"

# Fixed categorical order, never cycled.
#
# Slot 2 is the red influenza/plots.py has always used for the predicted series,
# so a model line in a comparison figure is the same colour as that model's own
# grid plot. Slot 1 is deliberately NOT the slate below: ACTUAL and SERIES[0]
# were briefly the same value, which drew "Observed" and "persistence" as one
# colour on the overlay -- the observed series is the reference every model is
# judged against, so it must never share a categorical slot.
#
# Slot 4 is purple rather than the yellow the old ramp used there. Yellow was
# already the one slot the old docstring flagged as failing contrast against the
# surface (2.11:1), and it got away with it because every series also carried a
# marker shape. Dropping the markers removes that second channel, so a
# sub-3:1 line colour is no longer defensible -- and slot 4 is not a corner
# case: with four models plotted, gnn_st lands there.
SERIES = ["#1f77b4", "#e74c3c", "#2e7d32", "#7d3c98"]

# Identity rests on hue plus line style. The old marker ramp is kept only so
# `palette.marker(i)` call sites keep working; it returns no marker.
MARKERS = [None, None, None, None]

# Ink. All three are plain black now: the figures use default text colour, and
# these names survive so the call sites that pass `color=INK_SECONDARY` do not
# all need editing. Greys are kept only where they carry meaning -- a muted
# reference line is genuinely recessive, a muted axis label is just faint.
INK_PRIMARY = "black"
INK_SECONDARY = "black"
INK_MUTED = "#666666"
GRIDLINE = "#e0e0e0"
AXIS = "black"

# The observed series is the reference the models are judged against, not a peer
# series, so it wears primary ink instead of taking a categorical slot.
ACTUAL = "#2c3e50"

# Flu-season shading, matching influenza/plots.py:21 exactly.
SEASON = "#f1c40f"
SEASON_ALPHA = 0.15

# Ordinal severity bands: low, moderate, high, very high. Was a four-step orange
# ramp that flooded every panel. The bands are now carried by the dashed
# threshold lines in THRESHOLD_STYLES below -- the same encoding the grid plots
# use -- and these greys are only a hint behind them.
#
# Deliberately near-white. The top band runs from its threshold to the shared
# ceiling, so on a 0-300 axis "very high" is the LARGEST area on the panel: any
# appreciable tint there fills the empty upper half of every chart and pulls the
# eye away from the curve. A sequential ramp is the right encoding for an
# ordered variable, but it has to stay under the data.
SEVERITY_WASH = ["#ffffff", "#fbfbfb", "#f6f6f6", "#f1f1f1"]

BAND_ALPHA = 0.15
LINE_WIDTH = 1.5
ACTUAL_WIDTH = 2.0

# One style per severity boundary. This list was typed out verbatim in BOTH
# influenza/plots.py:43-45 and plot_forecasts.py:62-67, with a comment in each
# saying it matched the other. One definition, imported by both.
THRESHOLD_STYLES = [((0, (1, 3)), 0.8, 0.50), ((0, (4, 3)), 1.0, 0.65),
                    ((0, (7, 2)), 1.2, 0.80)]
THRESHOLD_INK = "#52514e"


# The observed series must never share a categorical slot with a model, or the
# reference and one of the things being judged against it draw as one colour.
# This is not hypothetical -- it happened during the restyle.
assert ACTUAL not in SERIES, "ACTUAL collides with a SERIES slot"


def series_colour(index: int) -> str:
    """Colour for the nth series, in fixed order.

    A fifth series is a design decision, not a generated hue: fold models into
    a subset, or facet. Raising here rather than cycling keeps that honest.
    """
    if index >= len(SERIES):
        raise ValueError(
            f"Only {len(SERIES)} categorical slots are available, asked for "
            f"index {index}. Plot a subset with --models, or add a facet -- do not "
            "cycle the palette, which would make two models share a colour."
        )
    return SERIES[index]


def marker(index: int):
    """No marker. Kept so existing `marker=palette.marker(i)` calls still work.

    Matplotlib treats marker=None as "no marker", which is what the reference
    figure does: it separates its two series by line style, not by glyph.
    """
    return MARKERS[index % len(MARKERS)]


def style_axes(ax, *, grid_axis: str = "y") -> None:
    """Plain axes: all four spines, no grid, default tick colours.

    `grid_axis` is accepted and ignored. Callers pass it positionally in a few
    places and removing the parameter would be a wider edit than the behaviour
    change is worth; there is no grid to choose an axis for.
    """
    del grid_axis
    ax.set_axisbelow(True)
