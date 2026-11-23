# Generated copy of boston-flu-outlook/core/vocab.py. Edit it there and run vendor_bphc.py; changes made here are overwritten.
"""Wording per audience, and which tabs each one sees.

Briefing is for a health-department lead deciding what to say this week: plain
words, the graph model up front, no scoring jargon. Analyst keeps the same pages
and adds the numbers behind them (scores, p-values, the full forecast table).
"""

MODES = {"briefing": "Health department briefing", "analyst": "Analyst"}

TABS = {
    "briefing": ["outlook", "detail", "drivers", "severity", "all", "record", "chicago", "how"],
    "analyst": ["outlook", "detail", "drivers", "severity", "all", "record", "chicago", "table", "how"],
}

TAB_TITLES = {
    "outlook": "This week", "detail": "Neighborhood", "drivers": "What's driving it",
    "severity": "Severity",
    "all": "All neighborhoods",
    "record": "Track record", "chicago": "Chicago", "table": "Forecast table",
    "how": "How it works",
}

# Plain-language verdicts from the backtest, keyed by the package's verdict text.
VERDICT = {
    "better than persistence": ("Beats “same as last week”", "good", "✓"),
    "not clearly better than persistence": ("Slightly better, not clearly", "warning", "~"),
    "no better than persistence": ("No better than “same as last week”", "critical", "✕"),
    "worse than persistence": ("Worse than “same as last week”", "critical", "✕"),
    "not enough data": ("Not enough data", "warning", "?"),
    "not backtested": ("Not checked yet", "warning", "?"),
    "reference": ("Reference", "warning", "•"),
}

# What pushed a forecast up or down: (name, short column name, what it means).
DRIVER_LABELS = {
    "level": ("This week's reading", "This week",
              "The rate BPHC reported for the latest week, against a usual week at this "
              "time of year."),
    "trend": ("The three weeks before", "Recent weeks",
              "Whether the weeks just before the latest one were climbing or falling."),
    "history": ("Earlier weeks", "Earlier",
                "Weeks 4 to 15 back: how this season has built up so far."),
    "weather": ("Weather", "Weather",
                "Temperature, humidity, rain and wind in the latest week."),
    "calendar": ("Time of year", "Calendar",
                 "Where the forecast week sits on the usual seasonal curve, against the "
                 "weeks the comparison is made with."),
    "neighbor": ("Neighboring areas", "Neighbors",
                 "What the model picks up from the other neighborhoods' recent weeks, "
                 "through the neighborhood network."),
    "adjust": ("Averaging model runs", "Averaging",
               "The published median averages many randomized runs of the model; this is the "
               "small gap to the single averaged run explained here."),
}
BASE_LABEL = "A usual week at this time of year"
