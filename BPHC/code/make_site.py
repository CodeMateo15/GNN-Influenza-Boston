"""Make the offline website: the whole Boston Flu Outlook site as one HTML file.

    python make_site.py --origin live/2026_27/boston/2026-11-08 --out ../boston_flu_outlook.html
    python make_site.py --origin live/2026_27/boston --out ../boston_flu_outlook.html   # newest week

Input: one archived forecast folder, the same one make_bphc.py reads (written each
week by `live_forecast.py run`). Earlier weeks beside it and the season's
scores.csv, if present, fill in the live track record.

Output: a single .html file, about 3 MB, with every tab, neighborhood and chart of
the public site built in. Open it in any browser: it needs no internet connection
and no server, makes no network requests, and nothing in it leaves the computer.
Share it like any other file. It is a snapshot: make a new one each week.

Left out compared with the public site: the Chicago tab (BPHC's run has no Chicago
data) and "What's driving it" (that needs the package's `explain` step, which this
folder's live_forecast.py does not run). The site's code is in outlook/ (a copy;
see outlook/README.md).

Needs numpy, pandas and shiny (requirements-report.txt); no PyTorch.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTLOOK = HERE / "outlook"


class InputError(ValueError):
    """A missing or unusable input; the command line exits with status 2."""


def newest_week(origin: Path) -> Path:
    """Accept a week folder, or a city folder holding weeks (newest wins)."""
    if (origin / "meta.json").exists():
        return origin
    weeks = sorted(p for p in origin.glob("*") if (p / "meta.json").exists())
    if not weeks:
        raise InputError(f"{origin} is not an archived forecast folder (no meta.json), "
                         "and holds none")
    return weeks[-1]


def build(origin: str | Path) -> str:
    """The site as one HTML string, from an archived forecast folder."""
    origin = Path(origin)
    if not origin.exists():
        raise InputError(f"missing input {origin}")
    week = newest_week(origin)
    if str(OUTLOOK) not in sys.path:
        sys.path.insert(0, str(OUTLOOK))
    try:  # outlook/ is put on the path above
        from core.stage import StageError, stage
        import export_html
    except ModuleNotFoundError as exc:
        raise InputError(f"{exc.name} is not installed: pip install -r requirements-report.txt")
    geo = json.loads((OUTLOOK / "boston" / "geo.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        try:
            stage("boston", week, Path(tmp) / "boston", edges=OUTLOOK / "boston" / "edges.csv",
                  geo=geo)
            return export_html.build(Path(tmp))
        except (StageError, export_html.ExportError) as exc:
            raise InputError(str(exc)) from None


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--origin", required=True, type=Path,
                        help="an archived forecast folder, e.g. live/2026_27/boston/2026-11-08 "
                             "(or live/2026_27/boston for the newest week)")
    parser.add_argument("--out", required=True, type=Path, help="the .html file to write")
    args = parser.parse_args(argv)
    try:
        page = build(args.origin)
    except InputError as exc:
        print(f"make_site: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(page, encoding="utf-8")
    print(f"wrote {args.out} ({len(page.encode()) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
