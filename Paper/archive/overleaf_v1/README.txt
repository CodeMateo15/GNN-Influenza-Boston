Overleaf package for the AJE submission (Practice of Epidemiology)
==================================================================

SUPERSEDED (2026-10-23): this is the first draft, kept as a record. The second
draft, with the new Introduction and the component ablations, is in
Paper/overleaf_v2/. Paper/scripts now build the second draft's figures; the
figures here came from the scripts as of commit 2d1e3b3a.

Files
  main.txt         Anonymized manuscript: abstract, text, references, tables,
                   figure legends with alt text, figures.
  titlepage.txt    Title page (authors, affiliations, acknowledgments, funding,
                   conflicts, data availability). AJE wants it as a separate file.
  supplement.txt   Appendix S1 with Tables S1-S14 and Figures S1-S5.
  references.bib   Only the entries cited in main.txt and supplement.txt.
  vancouver-aje.bst  vancouver.bst edited for AJE (3 authors then et al., full
                   page ranges, DOIs). Keep it in the project root.
  figures/         figures 1-5 and S1-S5 as PDF (vector, for submission) and PNG (preview).

Uploading to Overleaf
  1. Zip this folder and use New Project > Upload Project.
  2. Rename main.txt -> main.tex, titlepage.txt -> titlepage.tex,
     supplement.txt -> supplement.tex.
  3. Set main.tex as the main document (Menu > Main document). Compile
     titlepage.tex and supplement.tex by switching the main document.
  4. Compiler: pdfLaTeX. Bibliography: BibTeX with vancouver-aje.bst (included). Citations are superscript, AMA style.

Red text in [brackets] marks items to fill in or confirm (affiliations, full
author names, funding numbers, ethics statement, word counts, code release tag).

Regenerating figures and tables (from the repository root)
  /opt/anaconda3/bin/python Paper/scripts/make_figures.py
  /opt/anaconda3/bin/python Paper/scripts/make_tables.py
  /opt/anaconda3/bin/python Paper/scripts/make_severity.py   (after Code/compare_severity.py has scored each unseen fold)
Both read only files already in Code/results and Data/; nothing is retrained.
