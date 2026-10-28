# Paper plan

Status as of 2026-09-27; cities updated 2026-10-09 (Chicago replaced Buenos Aires
as the third city, and Buenos Aires is out of the paper). Target: a complete draft
by **2026-10-14**. Open city items live in `Paper/notes/chicagoAndNextSteps.md`.

The evidence is ready to write from. It supports a narrower paper than the one
first planned: the GNN does **not** beat strong baselines by a wide margin. What
it does show is a reliable graph effect in Boston, a pipeline that ports to new
cities from data alone, and informative null results. Write that paper.

---

## Working title and framing

> **When does a neighborhood graph help? Rolling-origin evaluation of
> neighborhood-scale influenza forecasting in three cities**

Contributions, in the order the evidence supports them:

1. **Forecasting, not nowcasting, at neighborhood scale.** ED-based influenza
   rates for 14 Boston neighborhoods, 1-4 weeks ahead, scored the way CDC
   FluSight scores forecasts, on seasons the design never saw.
2. **Adding a neighborhood graph reliably improves the model, but the model
   does not beat a well-tuned non-graph model by much.** See the claims below.
3. **The pipeline ports by data alone.** The graph comes from boundary
   polygons, and a model trained in one city is a usable forecaster in
   another.
4. **Replication and null results.** Luo et al.'s claims (the background node
   and the choice of topology) do not replicate. Transit edges and demographics
   add nothing. Columbus shows no clear graph benefit in its single unseen
   season.
5. **An evaluation protocol others can reuse.** Frozen configurations, nested
   validation-only tuning with an equal budget for every model, week-level
   significance tests and the weighted interval score (WIS, FluSight's scoring
   rule).

Target venue: public-health or epidemiology forecasting (e.g. *AJE*,
*Epidemics*, *PLOS Comput Biol*). The framing suits an epidemiology audience
better than an ML venue, because the value is the honest evaluation and the
"when does it help" question.

---

## What the evidence supports

Every number below is from seasons the design never saw. The 2025-26 season was
used to choose the design, so it is a **development season**: never quote it as
evidence.

**Unseen folds:**

| City | Unseen seasons | Development season |
|---|---|---|
| Boston | 2022-23, 2023-24, 2024-25 | 2025-26 |
| Columbus | 2024-25 | 2025-26 |
| Chicago | 2022-23, 2023-24, 2024-25, 2025-26 | none (added after the design was fixed) |

### Claim 1: Adding the graph reliably improves the model in Boston

- The graph model beats the same model with the graph removed, when both are
  equally tuned:
  - at 1 week, in all 3 unseen seasons, clearing the multiple-comparison-corrected
    week-level test;
  - at 2 and 4 weeks, in 2 of 3 seasons.
- Mean WIS in Boston (lower is better):

  | | 1 week | 2 weeks | 4 weeks |
  |---|---|---|---|
  | graph model | 5.13 | 6.47 | 8.22 |
  | no graph | 5.69 | 6.72 | 8.68 |

- **Source:** `Code/results/backtest_20??_??/horizon_*/_comparison/significance_tuned.md`;
  METHODS § "With every model tuned the same way".

### Claim 2: No wide margin over strong baselines (state this plainly)

Every learned model got the same tuning budget: 12 configurations each, chosen on
validation weeks only, then 10 seeds. Tuning helped the baselines far more than
the GNN: on validation weeks, across the 3 cities, the LSTM improved 7%
(6.8%), the GNN 2% (2.4%).

Mean WIS in Boston:

| | 1 week | 2 weeks | 4 weeks |
|---|---|---|---|
| graph model | 5.13 | 6.47 | 8.22 |
| tuned LSTM | 5.18 | 6.83 | 9.16 |
| tuned Cola-GNN | 5.35 | 7.61 | 8.77 |
| persistence | 6.24 | 7.94 | 11.44 |

- **Against the tuned LSTM and the tuned Cola-GNN:**
  - At 1 week, they are tied in all 3 seasons.
  - At 2 and 4 weeks, the graph model is ahead on average. It is clearly ahead
    in only one season against the LSTM, and never clearly against Cola-GNN.
- **Against persistence** ("next week looks like this week"), the graph model's
  WIS is 18-28% lower.

### Claim 3: The graph can come from boundary files

- Boston's hand-drawn map was about 85% right. It had 4 invented borders and
  about 5 missing ones, the same accuracy measured for Columbus.
- Replacing it with a polygon-derived map changes nothing. Of 36 week-level
  comparisons (2 derived maps × 3 seasons × 3 horizons × 2 models), 33 are
  ties, 2 favour a derived map and 1 favours the hand map. This holds even for
  a borders-only model, where the map is its only spatial information.
- **Source:** `Code/scrapers/derive_boston_adjacency.py`;
  `Code/results/boston_geo_{tract,land}/`; METHODS § Portability.

### Claim 4: A model trained in one city transfers where data is scarce

WIS on the unseen 2024-25 season:

| Target city | Model trained locally | Transferred model, no local training | Persistence |
|---|---|---|---|
| Columbus (model from Boston) | 4.11 / 5.18 / 6.49 | 3.90 / 5.08 / 6.45 | 4.67 / 5.89 / 8.45 |
| Boston (model from Columbus) | 4.88 / 6.15 / 8.25 | 5.28 / 7.11 / 10.07 | 6.36 / 8.95 / 14.07 |
| Chicago (model from Boston; levels) | 1.09 / 1.12 / 1.25 | 1.16 / 1.24 / 1.29 | 1.35 / 1.42 / 1.52 |
| Boston (model from Chicago) | 4.88 / 6.15 / 8.25 | 5.15 / 6.86 / 10.36 | 6.36 / 8.95 / 14.07 |

Values are for 1 / 2 / 4 weeks ahead.

- **Boston → Columbus** with no local training ties a model trained on Columbus
  itself.
- **Columbus → Boston** is worse at every horizon, clearly only at 4 weeks. Columbus has about a third of
  Boston's training history.
- **Against persistence**, a transferred model with no local training has lower
  error in every case. That comparison is on the mean, not tested week by week.
- **Fine-tuning** on the target city is not clearly better or worse than
  training from scratch in any of the 12 comparisons (unseen 2024-25 fold).
- **Source:** METHODS § Portability.

### Claim 5: What does not generalize

- **Columbus.** In its one unseen season no lead is clear after the Holm
  adjustment: over persistence p = .07/.63/.40, and over the no-map model
  p = .07 at 1 week. "Same week last year" beats it at 4 weeks.
- **Chicago:** with equal tuning the graph model is ahead everywhere. The map
  helps at 1 week in all 4 seasons and fades by 4 weeks (the earlier 2022-23
  null was a scaling bug, fixed 2026-10-11).
- **Luo et al.'s claims do not replicate:**
  - the background node gives +0.005 here against their +0.135;
  - the "functional topology matters" claim fails: how the graph is wired does
    not matter here.
- **Transit edges and demographics are null.**
- **Source:** METHODS § Ablations, § Transit (retired), § Cities.

---

## What the paper must not claim

- **"Beats all baselines" or "wide margin".** Not true against tuned baselines.
- **"Works in all three cities".** Columbus is not clear in its single season.
- **"Transfer always works."** Into Chicago and into Boston, a local model was
  better; transfer matched local only Boston to Columbus.
- **Any 2025-26 number as evidence.** It is the development season.
- **The early leaderboard gaps** (e.g. "+0.117 Corr over LSTM at 2 weeks").
  They came from untuned, single-seed baselines.
- **A head-to-head win over Luo et al.'s published 0.8202.** Different data and
  a different measure; report it as a non-replication instead.

---

## Limitations to state

- **One unseen season for Columbus.** Its history starts in 2022.
- **Chicago's target is a capped 1-10 index**, not a rate; errors are in levels.
- **Reporting delay is not simulated in the inputs.** An h-week forecast made
  with an L-week delay equals the (h+L)-week result, so the 4-week rows stand in
  for a delayed real-time forecast. Boston data revisions were never checked.
- **Cola-GNN is our reimplementation** from the paper, not the authors' code.
- **Boston's two water anchors are hand-coded.** The Charles River and Harbor
  edges are in no land boundary file.
- **The GNN's architecture was designed on the development season.** Only its
  training settings were re-tuned per fold.
- **Run-to-run noise** on the cluster is up to 0.03 MAE, far below the gaps
  reported.
- **No prospective season.** A live 2026-27 forecast is out of scope before
  2026-10-14; list it as future work.

---

## Include

- include acknowlegments for help from Columbus Public Health, Boston Public Health Commission, and PEAK trailblazer fellowship, and Prof. Ariel Hamlin (https://www.khoury.northeastern.edu/people/ariel-hamlin-2/)

---

## Before drafting (reproducibility)

- [ ] Commit the current code and results, and tag the commit (e.g.
      `paper-v1`). Every number in the draft should cite that tag. Nothing is
      committed yet.
- [ ] Record the Explorer job IDs:
  - backtest: 10610260
  - tuning: 10612770 (search), 10613869 (final runs)
  - portability: 10637116, 10637117
  - Chicago backtest: 10856752, 10860453
  - Chicago standardization (2026-10-09 to 11): tuning search 10945307 and
    retry 10974879; parity 10945308; finals 10975151; transfer 10945488 and
    10974863; 2022-23 reruns after the scaling fix 10985373, 10985374 and
    10986165
- [ ] State data and code availability. BPHC, Columbus Public Health and CDPH
      are public or on request; check terms for the line-level Columbus
      extracts before publishing them.

## Figures and tables to produce

1. **Study design.** The three cities, the graph built from boundary polygons,
   and the rolling-origin folds.
2. **Main table.** WIS and MAE per horizon for all models on Boston's unseen
   folds, with 95% intervals. Source: `results/_backtest/backtest.csv` and the
   `significance_tuned` files.
3. **Graph effect.** The graph model against its no-graph version, per season
   and horizon, with bootstrap intervals.
4. **Error relative to persistence** (relative WIS), per city and horizon.
5. **Portability.** The map test table and the transfer table (above).
6. **Calibration.** Coverage of the forecast bands, or PIT histograms, for the
   main models. The code exists (`scoring.pit_values`); the figure does not.
7. **Supplement.**
   - the tuning search spaces;
   - the chosen configurations (`Code/sweep/tuned_configs.json`);
   - the full per-fold significance tables;
   - the data notes per city.

## Key files

| What | Where |
|---|---|
| Full methods and results log | `Code/docs/METHODS.md` |
| Backtest runner and frozen arms | `Code/run_backtest.py` |
| Equal-budget tuning | `Code/tune.py`, `Code/sweep/tuned_configs.json` |
| Scoring and significance tests | `Code/influenza/scoring.py`, `Code/compare_significance.py` |
| Graph from boundary polygons | `Code/scrapers/derive_*_adjacency.py` |
| Cross-city transfer | `Code/run_gnn.py --init-from / --zero-shot` |
| Per-city data notes | `Code/docs/DATA_NOTES.md`, `COLUMBUS_DATA_NOTES.md`, `AMBA_DATA_NOTES.md` |
| Related Papers | `nearest neighbours: Luo et al. 2025; Kraemer et al. 2025 review; the AJE dengue and Rt papers for evaluation standards` |

## Questions

- Is it better to remove Buenos Aires since it is southern hemisphere, and has a lot of issues with it?
  - **Keep it, but shrink it.** It was in the frozen evaluation from the start.
    Dropping it after it came back null looks like selective reporting, which
    is exactly what reviewers check for.
  - **The Southern Hemisphere is not the problem.** The code already handles
    its own season (Apr-Sep) and test window.
  - **Its data issues are part of the finding.** The ~4-month backfill and the
    near-empty recent weeks are candidate explanations for why the graph adds
    nothing there. That supports the "when does a graph help" framing.
  - **Decision 2026-10-09: left out of the paper.** Chicago replaced it as the
    third city. The advice above (keep it, shrink it) was not taken.
  - **In practice (superseded):** one paragraph and one row in the main table ("external
    test: the graph model is tied with persistence"), with the data caveats.
    The details go in the supplement. It has issues with data and how it doesnt align. there is a reference citation that ties into why there is differences in tropical and such.

- Is it possible to port this out to make it easy for public health departments to use (either train their own model, or use a pretrained Boston-variant)?
  - **Yes, the evidence supports it.** A city is set up from data alone:
    area-level rates, boundary polygons for the graph, a season definition
    and a loader. A model trained on Boston and applied with no local training
    had lower error than persistence in every case tested. "Use a pretrained
    model until you have history, then train your own" is defensible.
  - **Limit: the inputs must match.** A pretrained model needs the same inputs
    Boston's does: rate per 100k, the same weather variables, the same 8
    demographic columns. Buenos Aires could not use it for exactly that reason. Chicago can: it has
    all 8 columns, and the target is z-scored per area, so rate vs index does not
    block transfer.
  - **Limit: build the check in.** The tool should backtest against
    persistence on the department's own data before anyone trusts a forecast.
    Transfer worked Boston to Columbus, but not in reverse.
  - **Limit: real-time use.** Reporting delays are not simulated yet, and
    real-time use would hit them.
  - **For Oct 14, do the light version:** a documented "add your city"
    recipe, the released code, pretrained Boston weights and a one-command
    backtest. Describe it as code availability plus a short portability
    section. A full `pip`-installable package comes after the draft. (I would still like to try and make it work in time)