"""Build a reading copy of the manuscript with tables and figures inline.

AJE wants tables, figure legends and figures at the end of the manuscript, so
main.txt keeps them there and stays the file to submit. This writes
main_inline.txt next to it, with each table and figure (legend and alt text
under it) placed after the paragraph that first cites it. Rerun after editing
main.txt; never edit main_inline.txt by hand.

    python Paper/scripts/make_inline.py                  # Paper/overleaf_v2
    python Paper/scripts/make_inline.py --dir Paper/overleaf_v2
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = ROOT / "Paper" / "overleaf_v2"

HEADER = ("% main_inline.txt -- READING COPY, generated from main.txt by\n"
          "% Paper/scripts/make_inline.py. Tables and figures sit after the paragraph\n"
          "% that first cites them. Submit main.txt, not this file.\n")


def section(text: str, start: str, end: str | None) -> str:
    i = text.index(start)
    j = text.index(end, i) if end else len(text)
    return text[i:j]


def first_paragraph_end(body: str, pattern: str) -> int:
    """Index just past the paragraph holding the first match of `pattern`."""
    m = re.search(pattern, body)
    if m is None:
        raise SystemExit(f"no citation matching {pattern!r} in the text")
    end = body.find("\n\n", m.end())
    return len(body) if end < 0 else end


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR)
    args = parser.parse_args()
    text = (args.dir / "main.txt").read_text()

    tables_part = section(text, "\\section*{Tables}", "\\section*{Figure Legends}")
    legends_part = section(text, "\\section*{Figure Legends}", "\\section*{Figures}")
    figures_part = section(text, "\\section*{Figures}", "\\end{document}")

    tables = re.findall(r"\\begin\{table\}.*?\\end\{table\}", tables_part, flags=re.S)
    legends = {m.group(2): m.group(1) for m in re.finditer(
        r"(\\noindent\\textbf\{Figure (\d)\.\}.*?)(?=\\noindent\\textbf\{Figure \d\.\}|\\clearpage|\Z)",
        legends_part, flags=re.S)}
    graphics = dict((n, f) for f, n in re.findall(
        r"\\includegraphics\[[^\]]*\]\{([^}]+)\}\s*\\caption\*\{Figure (\d)\.\}", figures_part))

    # Body: from the start through the end of the Discussion (before the
    # reference list's \clearpage), then the reference list itself.
    refs_at = text.index("\\bibliographystyle")
    body_end = text.rfind("\\clearpage", 0, refs_at)
    preamble_and_body = text[:body_end]
    references = text[body_end:text.index("\\section*{Tables}")]
    references = references[:references.rfind("\\clearpage")]

    inserts: list[tuple[int, str]] = []
    for block in tables:
        label = re.search(r"\\label\{([^}]+)\}", block).group(1)
        at = first_paragraph_end(preamble_and_body, re.escape(f"\\ref{{{label}}}"))
        inserts.append((at, block.replace("\\begin{table}[h!]", "\\begin{table}[H]")))
    for n in sorted(legends):
        at = first_paragraph_end(preamble_and_body, rf"Figure\s+{n}(?![0-9])")
        figure = ("\\begin{figure}[H]\n\\centering\n"
                  f"\\includegraphics[width=\\textwidth]{{{graphics[n]}}}\n"
                  "\\end{figure}\n\n" + legends[n].strip() + "\n\n\\medskip")
        inserts.append((at, figure))

    out = preamble_and_body
    # Last first, so earlier offsets stay valid; blocks cited in the same
    # paragraph keep their table-then-figure, numbered order.
    for _, at, block in sorted(((i, at, block) for i, (at, block) in enumerate(inserts)),
                               key=lambda x: (x[1], x[0]), reverse=True):
        out = out[:at] + "\n\n" + block + out[at:]
    if "\\usepackage{float}" not in out:
        out = out.replace("\\usepackage{graphicx}", "\\usepackage{graphicx}\n\\usepackage{float}", 1)
    out = HEADER + out + references.rstrip() + "\n\n\\end{document}\n"
    (args.dir / "main_inline.txt").write_text(out)
    print(f"wrote {args.dir / 'main_inline.txt'}: {len(tables)} tables, {len(legends)} figures inline")


if __name__ == "__main__":
    main()
