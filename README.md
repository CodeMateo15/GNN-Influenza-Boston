# GNN-Influenza-Boston

Week-ahead influenza forecasting for the 14 neighborhoods of Boston, framed as a
problem on a graph.

Citywide forecasts are the wrong unit for public health action. Emergency
departments, vaccination clinics and outreach campaigns are all sited locally,
and Boston's neighborhoods do not move together: post-COVID, mean weekly ILI
rates range from about 9 per 100,000 in Fenway to 63 in Dorchester. The question
this repository asks is whether **the structure connecting neighborhoods** —
shared borders, correlated histories, similar demographics, transit flows —
carries forecasting signal beyond each neighborhood's own history.

The honest short answer, on the current data, is *not yet at one week ahead*.
See [Results](#results).

---

## Quickstart

```bash
pip install -r requirements.txt

python Code/run_seasonal_naive.py --season-lag 1      # persistence reference
python Code/run_arima.py --variant post_covid
python Code/run_lstm.py  --variant post_covid
python Code/run_gnn.py   --experiment gnn_multiedge
python Code/run_dualtopo.py --variant full            # paper reference model

python Code/compare_models.py                         # leaderboard across everything
python Code/plot_forecasts.py                         # overlay forecasts on the observed series
```

Scripts live in `Code/` and work from any working directory. Only
`pandas numpy scipy matplotlib` are needed for the naive baseline; `run_arima.py`
adds `statsmodels`, `run_lstm.py`/`run_dualtopo.py` add `torch`, and `run_gnn.py`
also needs `torch-geometric`.

`python Code/run_gnn.py --list` prints every configured experiment.

---

## The graph

**14 nodes** are the canonical BPHC neighborhoods (indices 0–13), and they are
the only nodes ever predicted or scored.

**7 anchor nodes** (indices 14–20) represent what surrounds the city —
Cambridge/Somerville, the Charles River, Chelsea/Revere/Winthrop, Boston Harbor,
the southern and western suburbs, and Brookline. They carry no influenza data and
are excluded from the loss and from every metric; they exist so that
edge-of-the-city neighborhoods have somewhere for signal to flow, instead of
having their boundary treated as a wall. Keeping neighborhoods at indices 0–13 is
what makes the `pred[:14]` slice safe everywhere.

Five edge types, documented in full in
[`Code/docs/EDGES_AND_NODES_NOTES.txt`](Code/docs/EDGES_AND_NODES_NOTES.txt):

| edge type | definition | pairs |
|---|---|---|
| geographic | hand-coded shared borders; optionally hop-graded at `0.5^(hop-1)` out to 3 hops | 23 + 21 anchor |
| correlation ("functional") | Pearson r of ILI histories above 0.85, computed on **pre-test weeks only** | 39 |
| demographic similarity | Gaussian kernel on 8 socio-economic features, median-heuristic bandwidth | 63 |
| transit | MBTA cross-boundary trip volume from GTFS | 32 |
| uniform complete | control: every pair at weight 1 | 91 |

Overlapping types accumulate into one weighted adjacency (MultiEdge reaches a
maximum edge weight of 3.506), except in the paper model, which keeps the
geographic and correlation topologies as two separate channels.

---

## Models

| model | idea | features |
|---|---|---|
| `persistence` | next week equals this week | — |
| `seasonal_naive` | next week equals the same week last year | — |
| `arima` | per-neighborhood ARIMA, order chosen by walk-forward validation RMSE | own history |
| `lstm` | one LSTM over all 14 series jointly, no graph | 14 series |
| `gnn_geo` | 2× GCN over geographic adjacency only | 22 node + 5 citywide |
| `gnn_corrbinary` | geographic + binary correlation edges | 22 node + 5 citywide |
| `gnn_multiedge` | all four edge types, weighted and fused | 22 node + 5 citywide |
| `gnn_uniform` | control: connect everything equally | 22 node + 5 citywide |
| `dualtopo` | Luo et al. 2025 Dual-Topo-STGCN, ILI rates only | 52 ILI lags |

Node features are 8 ILI lags, 6 weather variables and 8 static demographics.
Citywide covariates are ILI count, ED count, ILI/ED percentage, confirmed flu
cases and monthly cases. Everything added later — COVID and RSV cases,
wastewater, Rt, vaccination — defaults to **off**, so the baseline stays
reproducible and each addition is a clean ablation.

The GNNs predict the week-over-week **change** and reconstruct the level from the
last observed week. That is deliberate: predicting the level makes persistence an
attractor, since "no change" scores well in the flat off-season.

### The paper reference

`dualtopo` reimplements Luo J. et al., *"A novel graph neural network based
approach for influenza-like illness nowcasting: exploring the interplay of
temporal, geographical, and functional spatial features"*, **BMC Public Health**
25:408 (2025), [doi:10.1186/s12889-025-21618-6](https://doi.org/10.1186/s12889-025-21618-6).

Two parallel pathways, one per topology, each `[gated 1×3 temporal conv → GCN →
gated temporal conv] × 2`; fuse; final temporal conv; fully-connected readout.
With a 52-week input the valid convolutions leave exactly 42 time steps before
the head, which the implementation asserts.

The paper leaves three things unstated, and our choices are recorded in each
run's `run_config.json`: the fusion operator (we concatenate), the correlation
threshold (we reuse 0.85), and the optimizer (we use Adam).

---

## Evaluation

One window, **2025-05-31 → 2026-05-31**, giving 48 target weeks from 2025-06-01
to 2026-04-26. Predictions are generated once and then sliced into segments, so
nothing is retrained per segment:

- `overall` — all 48 weeks
- `flu_season` — target month in Oct–Mar (26 weeks)
- `off_season` — target month in Apr–Sep (22 weeks)

Every model reports the same four metrics — **RMSE, MAPE, MAE and Pearson
correlation (Corr)** — at four aggregation scopes: `neighborhood`, `macro`
(unweighted mean of the 14), `pooled` (all cells together) and `cross_week` (does
the model rank the neighborhoods correctly within a week?). The GNNs additionally
report R², Spearman, Lin's CCC and 95% interval coverage.

`n_obs` is always reported alongside, because suppressed neighborhood-weeks are
dropped rather than scored: 614 of 672 cells are real at horizon 1.

**Off-season MAPE is not a ranking metric.** The off-season mean rate is about 5
per 100,000, so percentage errors there are large and unstable by construction.

### Predictive intervals

Every model carries a 95% predictive interval, built by one shared recipe
(`influenza/intervals.py`) so the widths are comparable rather than each model
grading its own homework:

1. Residual variance is fitted as affine in the predicted level,
   `Var ≈ α_h + β_h · level`, on the **validation** split. A single absolute
   width would be far too wide through the flat off-season and far too narrow at
   the winter peak.
2. Where a model supplies its own uncertainty — MC-Dropout spread for the GCNs —
   that variance is added on top.
3. A per-horizon scalar rescales the band to hit 95% coverage on validation, so
   nothing depends on the residuals being Gaussian.

`CI_coverage` in `metrics.csv` is then the honest out-of-sample check. It is
revealing: the baselines land at 94–97%, but the GNNs only reach 83–91%. Their
validation residuals systematically understate their test residuals — the same
generalisation gap that shows up in the point metrics, seen from a second angle.

### Looking at the forecasts

```bash
python Code/plot_forecasts.py                                  # 4 models, all 14 neighborhoods
python Code/plot_forecasts.py --models persistence,arima,lstm,gnn_multiedge_covid_rsv
python Code/plot_forecasts.py --horizon 2 --no-ci
python Code/plot_forecasts.py --neighborhoods Dorchester,Roxbury --shared-y
```

Writes `results/_comparison/forecast_overlay_h1.png` (one panel per
neighborhood) and `forecast_citywide_h1.png` (the 14-neighborhood mean in one
large panel). Observed is the black line; each model gets a fixed categorical
colour plus its own marker shape, and the shaded ribbon is its 95% interval.

The overlay is worth reading before trusting any table. It shows, for instance,
that `gnn_multiedge` tracks the December peak reasonably but then sits at roughly
50 per 100,000 from February onward while the observed series falls back to about
20 — a sustained over-prediction across nearly every neighborhood that a single
RMSE number does not convey.

Four models is the cap, because four is the number of categorical colours
validated as distinguishable under colour-vision deficiency; the script refuses a
fifth rather than silently reusing a hue.

---

## Results

<!-- BEGIN LEADERBOARD -->
Horizon 1, `scope=pooled`, sorted by overall RMSE. `all` = full year (48 weeks), `flu` = Oct–Mar (26), `off` = Apr–Sep (22).

| model | variant | RMSE (all) | RMSE (flu) | RMSE (off) | Corr (all) | Corr (flu) | Corr (off) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arima | exclude_covid | 15.267 | 18.778 | 8.517 | 0.875 | 0.872 | 0.664 |
| arima | post_covid | 15.590 | 19.396 | 8.012 | 0.872 | 0.866 | 0.654 |
| lstm | exclude_covid | 15.936 | 20.412 | 5.949 | 0.871 | 0.860 | 0.797 |
| persistence | post_covid | 15.948 | 20.132 | 7.179 | 0.871 | 0.861 | 0.681 |
| persistence | exclude_covid | 15.948 | 20.132 | 7.179 | 0.871 | 0.861 | 0.681 |
| lstm | post_covid | 16.186 | 20.618 | 6.548 | 0.863 | 0.852 | 0.783 |
| gnn_multiedge_covid_rsv | post_covid | 16.780 | 19.643 | 11.895 | 0.867 | 0.869 | 0.723 |
| gnn_multiedge_leaknorm | post_covid | 18.552 | 20.966 | 14.696 | 0.883 | 0.892 | 0.709 |
| dualtopo_fullhistory | full | 19.552 | 24.965 | 8.590 | 0.804 | 0.795 | 0.740 |
| gnn_multiedge_covid_rsv_full | full | 19.945 | 23.947 | 12.720 | 0.876 | 0.873 | 0.721 |
| gnn_multiedge_full | full | 20.525 | 23.067 | 16.505 | 0.866 | 0.877 | 0.706 |
| gnn_multiedge_rt | post_covid | 23.029 | 26.228 | 17.849 | 0.855 | 0.863 | 0.703 |
| gnn_multiedge | post_covid | 24.535 | 26.938 | 20.876 | 0.860 | 0.878 | 0.697 |
| dualtopo | post_covid | 28.915 | 33.359 | 21.950 | 0.417 | 0.505 | 0.599 |
| dualtopo_no_bg | post_covid | 29.030 | 33.359 | 22.294 | 0.412 | 0.505 | 0.593 |
| gnn_corrbinary | post_covid | 31.028 | 33.107 | 27.994 | 0.808 | 0.834 | 0.682 |
| gnn_uniform | post_covid | 31.899 | 34.507 | 28.017 | 0.810 | 0.834 | 0.688 |
| gnn_geo | post_covid | 33.824 | 36.685 | 29.547 | 0.804 | 0.827 | 0.692 |
| seasonal_naive | exclude_covid | 40.232 | 52.813 | 6.775 | 0.416 | 0.315 | 0.714 |
| seasonal_naive | post_covid | 40.232 | 52.813 | 6.775 | 0.416 | 0.315 | 0.714 |

Per-segment rankings with MAPE, MAE and interval coverage are in [`Code/results/_comparison/leaderboard.md`](Code/results/_comparison/leaderboard.md); per-neighborhood breakdowns in [`leaderboard_by_neighborhood.md`](Code/results/_comparison/leaderboard_by_neighborhood.md).
<!-- END LEADERBOARD -->

Regenerate with `python Code/compare_models.py --update-readme`. Full table,
plot and per-segment breakdown in `Code/results/_comparison/`.

### Per-neighborhood leaderboard

The table above pools all 14 neighborhoods into one set of cells, which hides a
lot. `Code/compare_models.py` also writes
[`results/_comparison/leaderboard_by_neighborhood.md`](Code/results/_comparison/leaderboard_by_neighborhood.md)
(and `comparison_by_neighborhood.csv`): a win-count summary broken out by
segment, then one section per neighborhood ordered by disease burden — each with
three sub-tables (overall, flu season, off-season) carrying that segment's mean
rate and week count. 14 neighborhoods × 3 segments = 42 ranked tables.

It changes the story. **The LSTM wins 12 of the 14 neighborhoods overall, but
comes third in the pooled table**; ARIMA wins only Dorchester and Roxbury — yet
leads pooled. Those two are the highest-rate neighborhoods in the city, and the
pooled metric is dominated by them. Which view you want depends on the decision:
allocating city-wide capacity is a pooled question, advising one neighborhood's
health centre is not.

Neighborhoods won, by segment:

| model | overall | flu season | off-season |
|---|---|---|---|
| `lstm` | 12 | 9 | 9 |
| `arima` | 2 | 4 | 1 |
| `seasonal_naive` | 0 | 0 | 2 |
| `gnn_multiedge_covid_rsv` | 0 | 1 | 0 |
| `persistence` | 0 | 0 | 1 |
| `dualtopo_fullhistory` | 0 | 0 | 1 |

Two things only this view shows. **The seasonal naive wins Dorchester and Roxbury
in the off-season** — the two busiest neighborhoods, where the summer baseline is
stable year to year — having lost Dorchester's flu season by a factor of four
(106.11 against ARIMA's 24.48). And **the graph models win just 2 of the 42
segment-by-neighborhood cells**: `gnn_multiedge_covid_rsv` takes Hyde Park's flu
season, and `dualtopo_fullhistory` takes West Roxbury's off-season. Two cells out
of 42 is the clearest single statement of where this project currently stands.

(Counts are from the default run, which includes both the `exclude_covid` and
`post_covid` variants; the summary reports them split by variant and pooled per
model. Restrict with `--variant post_covid` for a single-variant view.)

Two other things only visible per neighborhood:

- **Errors are not comparable across sections without the scale.** The best
  Fenway RMSE is 3.67 against a mean rate of 7.0; the best Dorchester RMSE is
  20.49 against a mean of 49.2. Fenway looks better and fits relatively worse.
- **ARIMA and persistence are numerically identical in Roxbury** under
  `post_covid` — RMSE 28.912184, MAE 18.781250, Corr 0.836747, equal to six
  decimals — because ARIMA selected order `(0,1,0)` for that neighborhood, which
  is a random walk, which *is* persistence. (The `exclude_covid` run picked
  `(2,0,3)` and does differ.) The pooled table cannot show you that.

Note that per-neighborhood interval coverage runs to 100% in the low-rate
neighborhoods: the variance floor makes the band wide relative to rates near
zero, so coverage there is not evidence of good calibration.

### What this actually says

**Nothing beats persistence at one week ahead.** ARIMA (15.59) and persistence
(15.95) are statistically indistinguishable, and ARIMA's selected orders are
mostly `(0,1,x)` — a differenced random walk, which *is* persistence with extra
steps. Any claim about a model "working" here has to clear 15.95, and until this
round the project had no naive baseline to notice that.

**Graph structure does help, among the graph models.** The ordering
`gnn_multiedge` (24.5) < `gnn_corrbinary` (31.0) < `gnn_uniform` (31.9) <
`gnn_geo` (33.8) reproduces the earlier qualitative finding: weighted multi-type
edges beat binary correlation edges, which beat connecting everything equally,
which beats geography alone. Weighting, not mere connectivity, is what helps.

**The new COVID and RSV data is the single biggest improvement.** Adding monthly
neighborhood COVID and RSV rates plus COVID wastewater takes MultiEdge from 24.5
to 16.8 RMSE — enough to reach the persistence/ARIMA cluster. Respiratory
co-circulation appears to carry real signal, and this is the most promising
direction in the repository.

**More history matters more than architecture.** Training on the full 436-week
series instead of the 201 post-COVID weeks improves MultiEdge from 24.5 to 20.5
and Dual-Topo from 28.9 to 19.6. The 52-week input window in particular is
starved on the post-COVID slice: 85 training origins against the paper's 364.

**The paper's background-node claim does not replicate.** Luo et al. report that
adding an ocean/open-land node lifted Corr by 0.135. On Boston, `dualtopo` versus
`dualtopo_no_bg` gives 0.4169 versus 0.4122 — a difference of 0.005, well inside
noise.

**Horizon 2 is where the graph models start to earn their place.** Persistence
degrades from 15.95 to 24.09 while `gnn_multiedge_leaknorm` reaches 22.26 and the
LSTM 21.54. Two weeks ahead is a harder problem where "assume no change" stops
being a good answer.

**The ranking is not the same in every segment**, which is the main reason all
three are reported. ARIMA leads overall and in the flu season but falls to
seventh in the off-season, where the LSTM wins (5.95 vs 8.01). Most striking is
the seasonal naive: **last in the flu season by a wide margin (52.81) and third
in the off-season (6.78)**. That is the model behaving exactly as its assumption
dictates — "the same week last year" is a reasonable guess when the series is
flat, and hopeless when peak timing and magnitude move. A single full-year number
averages those two opposite behaviours into one uninformative figure.

The gap between GNNs and baselines is also widest in the off-season:
`gnn_multiedge` posts 20.88 against persistence's 7.18, nearly three times worse,
while in the flu season the same pair is 26.94 against 20.13. Whatever the graph
models are doing, it hurts most when there is little signal to track.

---

## Honest limitations

- **Every result predating August 2026 is void.** Two data-loading defects — an
  ILI count row averaged with the rate row, and suppressed weeks imputed as zero
  — affected all eight notebooks and both baselines. See
  [`Code/docs/DATA_NOTES.md`](Code/docs/DATA_NOTES.md). The old numbers are kept
  in `Code/results/_legacy_pre_refactor/` for the record and are excluded from
  the leaderboard.
- **Normalisation was leaking.** The notebooks computed normalisation statistics
  over the whole series, test window included, while the LSTM used training rows
  only. `gnn_multiedge_leaknorm` quantifies the effect: 18.55 RMSE with the leak
  versus 24.54 without. Roughly a third of the GNNs' apparent quality came from
  that leak. `normalize='train'` is now the default; `run_config.json` records
  which was used and `compare_models.py` warns when a table mixes them.
- **One seed.** Section 11 of the notes puts the noise floor at 0.2–0.5 MAE.
  Differences smaller than that mean nothing, which includes the Rt result.
- **Three post-COVID seasons.** 201 weeks, 121 training origins at an 8-week
  lookback. This is a small-data problem and behaves like one.
- **Citywide covariates run out mid-evaluation.** The ED file ends 2026-01-04 and
  the demographics file 2025-12-07; the last 17 and 21 weeks are carried forward,
  and the loaders say so on every run.
- **Rt is a growth index, not a reproduction number** — computed from an
  interpolated weekly rate. See [`Code/docs/RT_CAVEATS.md`](Code/docs/RT_CAVEATS.md).
- **`dualtopo` is scored on 627 cells, not 614**, because a horizon-1-only model
  keeps one extra origin. `compare_models.py` flags this; it is about 2%.
- **COVID and RSV neighborhood data is monthly**, held flat across weeks. The
  resolution mismatch is why those features default to off despite helping.

---

## Layout

```
Code/
├── influenza/         shared library: data, windows, graphs, samples, models,
│                      training, metrics, intervals, plots, palette, carbon, rt
├── run_*.py           one entry point per model family
├── compare_models.py  leaderboard across everything in results/
├── plot_forecasts.py  overlay forecasts + 95% intervals on the observed series
├── run_rt_diagnostics.py
├── checkpoints/       all .pt files (legacy/ holds the pre-refactor eight)
├── results/           <model>/<variant>/{predictions,metrics}.csv,
│                      run_config.json, emissions.json, plots
├── notebooks/         frozen; superseded by the scripts
├── scrapers/          weather, MBTA GTFS, neighborhood data collection
└── docs/              EDGES_AND_NODES_NOTES.txt, DATA_NOTES.md, RT_CAVEATS.md
Data/                  BPHC influenza / COVID / RSV, weather, MBTA,
                       census, MA vaccination
Citation Papers/       literature, nearest-neighbour first
```

Every run records its own energy use and CO₂ via
[codecarbon](https://github.com/mlco2/codecarbon), appended to
`Code/results/_emissions/emissions.csv` and summarised per run in
`emissions.json`. Tracking degrades gracefully: it never fails a model run, and
`--no-carbon` disables it.

---

## Reproducing a result

Every `results/<model>/<variant>/run_config.json` records the resolved
configuration, the git SHA, the split sizes, the graph edge counts and the seed.
`--experiment` names in `influenza/config.py` map one-to-one onto results
directories, so a number in the leaderboard can always be traced to the exact
command that produced it.
