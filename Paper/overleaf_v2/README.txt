Overleaf package for the AJE submission (Practice of Epidemiology), second draft
==================================================================================

Second draft, 2026-10-25. New Introduction (coauthor), component ablations on
the unseen seasons (Table 3, Figure 5; Appendix S1 Tables S15-S16), Results
reordered as performance -> what each component adds -> transferability, and
a model schematic (Figure 1C). The first draft is archived in Paper/archive/overleaf_v1/.

Files
  main.txt         Anonymized manuscript: abstract, text, references, tables,
                   figure legends with alt text, figures. This is the file to submit.
  main_inline.txt  Reading copy of main.txt with each table and figure after the
                   paragraph that first cites it. Generated; do not edit or submit.
  titlepage.txt    Title page (authors, affiliations, acknowledgments, funding,
                   conflicts, data availability). AJE wants it as a separate file.
  supplement.txt   Appendix S1 with Tables S1-S18 and Figures S1-S6.
  references.bib   Only the entries cited in main.txt and supplement.txt.
  vancouver-aje.bst  vancouver.bst edited for AJE (3 authors then et al., full
                   page ranges, DOIs). Keep it in the project root.
  figures/         figures 1-6 and S1-S6 as PDF (vector, for submission) and PNG (preview).

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
  /opt/anaconda3/bin/python Paper/scripts/make_figures.py            (writes Paper/overleaf_v2/figures; --out DIR to change)
  /opt/anaconda3/bin/python Paper/scripts/make_tables.py
  python3 Paper/scripts/make_inline.py      (rebuild main_inline.txt after any edit to main.txt)
  /opt/anaconda3/bin/python Paper/scripts/make_severity.py   (after Code/compare_severity.py has scored each unseen fold)
They read only files already in Code/results and Data/; nothing is retrained.
Paper/scripts/README.md lists the script, function and input files for every figure and table.
The component-ablation runs and their week-level tests are documented in
Code/results/_components/README.md (including the Boston data version used).

After review, unblind the package reference (areaflu2026package) in references.bib with:
  author={Biggs, Mateo}, title={{areaFluForecast}: neighborhood-scale influenza forecasting for public health departments}, version={1.2.0}, publisher={Zenodo}, year={2026}, doi={10.5281/zenodo.23449348}, url={https://pypi.org/project/areaFluForecast/}

After review, unblind the code reference (code2026release) in references.bib with:
  author: Biggs M, Yu D; url: https://github.com/CodeMateo15/GNN-Influenza-Boston

Paths blinded in supplement.txt for review (restore after acceptance):
  tuned configurations       Code/sweep/tuned_configs.json
  severity-alert analysis    Code/compare_severity.py, Paper/scripts/make_severity.py
  component ablations        Code/results/_components/README.md
  table bodies               Paper/scripts/make_tables.py (from Code/results)
