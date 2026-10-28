# Columbus and Chicago: status and next steps

Open issues for the two non-Boston cities. First written 2026-10-07, after Buenos
Aires was replaced with Chicago in the AJE draft (`Paper/overleaf/`). Updated
2026-10-09, when Chicago was brought up to the same comparison standard as
Boston and Columbus. Buenos Aires stays out of the paper (decision 2026-10-09).

The per-city analysis matrix the paper now reports is Appendix S1, Table S14
("Analyses performed in each city"). Every blank cell there has a stated reason.

---

## 1. Chicago: standardizing with Boston and Columbus (2026-10-09)

| Issue | Status | Runs |
|---|---|---|
| **No equal-budget tuning in Chicago.** Every Chicago model ran at default settings. | **Done 2026-10-11.** All 816 configurations ran; 54 were rerun after the log loss. Selections were merged into `tuned_configs.json` (other cities verified unchanged), then 68 ten-seed finals. 2022–23 was re-tuned and re-finaled after the scaling fix; the same configurations were chosen. Paper, Figures 2C, 3B/C and S2, and Tables S5, S8 and S11 are regenerated. | Jobs 10945307, 10974879 (retry), 10975151 (finals), 10985374 and 10986165 (2022–23 after the fix) |
| **The Chicago LSTM and gradient-boosted trees were trained once.** | **Done.** `lstm_tuned` and `xgboost_tuned` are 10-seed. `make_tables.py` no longer relabels the 1-seed runs. | as above |
| **Cola-GNN, FluSight baseline and the 10-seed LSTM were not run in Chicago.** | **Done.** `colagnn_tuned` comes from tuning; `flusight_baseline` and `lstm_s10` from the parity job (`lstm_s10` 2022–23 was rerun after the fix). | Jobs 10945308, 10985373 |
| **`gat_parity` diverged in Chicago 2022–23** (MAE about 2.7 million). | **Fixed: the cause was the scaling bug (row below).** After the fix, `gat_parity` 2022–23 is normal (largest forecast 6.1). `DROP` in `make_tables.py` can be emptied; the paper tables use `gat_tuned` anyway. | Jobs 10945308, 10985373 |
| **Chicago is not in the transfer test.** | **Done.** Logs show all 27 of 27 tensors loaded. Table 4 now has Boston→Chicago and Chicago→Boston rows. Zero-shot into Chicago is clearly worse than local at 1–2 weeks; into Boston it is worse, clearly only at 4 weeks; fine-tuning ties in all 12. | Job 10945308, then a transfer job |
| **Scaling bug corrupted Chicago 2022–23** (found 2026-10-11). ZIP 60707 is flat (all level 1) before June 2022, so its training std was 0, and `std + 1e-8` turned test inputs into about 9e8. This explains the diverged GAT and Cola-GNN, and probably part of the "no map benefit in 2022–23". | **Fixed** with `safe_scale` in `influenza/windows.py`: a flat column is scaled by 1. This is bit-identical for every other column, and a scan found no Boston or Columbus fold with a flat column. Every learned 2022–23 Chicago run is rerun, and the paper's 2022–23 text is rewritten from the corrected results. Documented in `Code/docs/CHICAGO_DATA_NOTES.md` and the supplement's Chicago data note. | Jobs 10985373, 10985374, 10986165 |
| **The Chicago target is an index, not a rate.** CDPH's level is 1–10, capped at 10; 13% of ZIP-weeks sit at 10. | Disclosed (Methods, limitations, Table 4 note c, Table S14). | — |
| **Chicago 2022–23 shows no map benefit.** | **Superseded.** After the scaling fix, the map helps clearly at 1 week in 2022–23 too. The "short history" explanation was removed from the paper. | — |

### Chicago: still open after the runs

- **Severity alerts.** Chicago is excluded because its measure is already a graded level (Table S14, note d). Option: score CDPH's own level bands as the alert (`Code/compare_severity.py`).
- **Cap sensitivity.** Rerun the evidence with ZIP-weeks at level 10 dropped from scoring. This is local and cheap, from existing `predictions.csv`.
- **Training window.** See section 4.
- **Main-leaderboard outputs.** Boston and Columbus also have `horizon_0X/_comparison` (development-season leaderboards, timing, classification). Chicago has none and needs none: it has no development season, and the paper reads only the backtest.

## 2. Columbus

Columbus already runs the same arms, tuning and seeds as Boston on its evidence
fold. What limits it is the data, not the runs.

| Issue | Status |
|---|---|
| **One unseen season (2024–25).** The series starts January 2022, so only `post_covid` exists, and a 2023–24 fold would train on under a year. | Disclosed (Methods, limitations, Table S14 note a). Each new season, add a fold to `DEFAULT_SEASONS["columbus"]` in `Code/run_backtest.py` and re-tune. |
| **No clear lead in Columbus.** Over persistence the Holm-adjusted *P* values are .07, .63 and .40 (h=1/2/4); over the no-map model the h=1 *P* is .07. | Now stated in Results (it was missing before), and the Discussion sentence is reworded to match. |
| **Columbus at 4 weeks:** "same week last year" had lower WIS (5.75 vs 6.31) and RMSE (15.83 vs 16.82) than the graph model. | Now stated in Results. It is not in the Holm family (it is not in `significance_tuned`). |
| **No ablation, timing or SHAP outputs for Columbus.** | Not needed for the paper: the design was chosen on Boston (Table S14, note f). Run `run_ablation.py --city columbus` only if a reviewer asks. |
| **`gnn_st_v2` leftover** in `results/columbus/horizon_01,02` (an older duplicate of `gnn_st`). | Remove it from the leaderboard or document it. It is not used by the paper. |
| **Line-level data terms.** | Check the terms for the Columbus line-level extracts before any release; ship weekly aggregates only. |

## 3. Other issues found while checking the draft

| Issue | Fix |
|---|---|
| **Columbus at 4 weeks:** the "same week last year" forecast had lower WIS (5.75 vs 6.31) and RMSE (15.83 vs 16.82) than the graph model. The draft now limits the "lowest error" claims to the models shown. | Decide whether to show that model in Figure 2B or Table S10, or leave the limit as worded. |
| **`Code/docs/METHODS.md` has stale numbers:** the map test cell 8.27 (correct: 8.26); "10 of 12" fine-tuning ties (that count included the development season; on the unseen season none of the 6 are clear); "consistent in direction" for the lead over the LSTM (2022–23 at 2 weeks went the other way). | Update METHODS.md to match the paper. |
| **`Paper/PAPER_PLAN.md` still describes Buenos Aires** as the third city. | Done 2026-10-09. |
| **Chicago tables label the graph model "Graph model".** | Done 2026-10-09 (`make_tables.py` LABEL). |
| **Tuning-gain sentence:** the old "18% for the LSTM" included Buenos Aires. It is now 9% for the LSTM and 3% for the graph model (Boston and Columbus). | Recheck after Chicago tuning: the sentence now covers 3 cities (Figure S2 has a Chicago panel). |
| **Placeholders still in red** (`\NOTE{}`): ethics/IRB statement, software versions, author names and affiliations, funding numbers, word counts, code release tag, areaFluForecast DOI. | Fill in before submission. |
| **Missing reference PDFs:** `biggerstaff2018severity`, `vega2013mem`, `brier1950verification` (cited); `huddleston2020h3n2` (optional). | Download into `Citation Papers/`. |

## 4. Does training on all data from 2017 help or hurt?

**Question:** Boston's backtest models train on the full history from December
2017 (variant `full`), including the COVID years when influenza nearly
disappeared. Columbus starts in July 2022 (`post_covid`). Is the long history
helping or hurting the paper's numbers?

**What we already know:**
- A live-track test on Explorer (job 10874664, 2026-10-06) found that dropping
  March 2020–June 2022 made Boston 5–11% worse at every horizon, clearly at 1–2
  weeks, and that training on post-COVID weeks only was 2–16% worse. It used
  the live `gnn_st` settings on 2023–24, 2024–25 and 2025–26
  (`areaFluForecast/scripts/training_window.py`,
  `live/runs/boston/training_window/`). That is live-track evidence, not paper
  evidence, and 2025–26 is the paper's development season.
- `Code/docs/METHODS.md` records on the development season that more history
  improved the older graph models a lot, but `gnn_st_full` measured worse than
  `post_covid` for the current design.
- `run_backtest.py` notes that only `full` reaches back far enough to train
  the 2022–23 fold.

**What to run for the paper:** compare `full` against `post_covid` (and a
"drop 2020–2022" version) for `gnn_st_tuned` and the strongest comparison
models. Use the paper's unseen Boston seasons only, 2023–24 and 2024–25, since
2022–23 can't train on `post_covid`. Then do the same for Chicago's 2023–24 to
2025–26. Score with WIS and the week-level test. It needs the cluster
(`run_backtest.py` is heavy).

**Why it matters:** if the long history helps, it explains part of the Columbus
and Chicago 2022–23 weakness (short histories) and supports "use a model
trained elsewhere until you have history". If it hurts, Boston's numbers could
improve and the methods should say so.

## 5. Coauthor section

A placeholder for the ARIMA and LSTM methods is in
`Paper/overleaf/supplement.txt`, section "Comparison models: ARIMA and LSTM".

**Target: 250–350 words, hard limit 400.** About 120–170 words go to ARIMA and
130–180 to the LSTM. The comment block in that section lists what to cover.

It is in the supplement because the main text is at the AJE 4,000-word limit. Moving any of it into the main text means cutting the same number of
words elsewhere.
