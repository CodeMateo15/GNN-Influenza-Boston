# Methods, results and limitations

The full write-up for GNN-Influenza-Boston. See the [README](../../README.md) for a short overview of the project and its data.

Week-ahead influenza forecasting for the 14 neighborhoods of Boston, framed as a
problem on a graph.

Citywide forecasts are the wrong unit for public health action. Emergency
departments, vaccination clinics and outreach campaigns are all sited locally,
and Boston's neighborhoods do not move together: post-COVID, mean weekly ILI
rates range from about 9 per 100,000 in Fenway to 63 in Dorchester. The question
this repository asks is whether **the structure connecting neighborhoods** —
shared borders, correlated histories, similar demographics —
carries forecasting signal beyond each neighborhood's own history.

The answer, on the corrected data, is **yes at one and two weeks ahead, in
both cities tested so far — and not reliably at four.** Against the four
original baselines (persistence, seasonal naive, ARIMA, LSTM) the margin widens
with horizon. Against boosted trees it does not: at h=4 `gnn_st` is tied with
`xgboost` in Boston (macro RMSE 19.63 vs 19.81) and behind it in Columbus
(9.03 vs 8.68). See [Cities](#cities) for the full table and
[Results](#results) for Boston in detail.

Two caveats belong next to that sentence rather than at the bottom. First, five
data defects were fixed in September 2026, and two of them were the largest
single source of error in the graph models: fixing the data alone, with no model
change, moved the then-current graph arm from RMSE 24.90 to 19.12 at one week
ahead. Every
number predating that is void; see [Data notes](DATA_NOTES.md) defects 5-9.
Second, the four baselines are unaffected by those fixes and reproduce their
previous numbers to six decimals, so the comparison below is like-for-like.

---

## Quickstart

```bash
pip install -r requirements.txt

python Code/run_seasonal_naive.py --season-lag 1      # persistence reference
python Code/run_arima.py --variant post_covid
python Code/run_lstm.py  --variant post_covid
python Code/run_xgboost.py --variant post_covid        # strongest non-graph baseline
python Code/run_gnn.py   --experiment gnn_st           # the current design
python Code/run_gat.py   --variant post_covid          # paper comparison model
python Code/run_dualtopo.py --variant post_covid       # paper reference model

python Code/run_all_horizons.py                       # every model at 1, 2 and 4 weeks
python Code/run_ablation.py --horizons 2 --n-seeds 3  # what each piece of gnn_st is worth

python Code/compare_models.py    --results-dir Code/results/horizon_01   # leaderboard at one horizon
python Code/compare_timing.py    --results-dir Code/results/horizon_02   # is the forecast late?
python Code/plot_forecasts.py    --results-dir Code/results/horizon_01 --horizon 1
python Code/compare_horizons.py                       # error growth across horizons
```

Results are organised **one tree per forecast horizon**
(`Code/results/horizon_02/<model>/<variant>/`), so `compare_models.py` and
`plot_forecasts.py` need `--results-dir` pointed at one of them. Both print the
available trees if you forget.

Scripts live in `Code/` and work from any working directory. Only
`pandas numpy scipy matplotlib` are needed for the naive baseline; `run_arima.py`
adds `statsmodels`, `run_xgboost.py` adds `xgboost`,
`run_lstm.py`/`run_dualtopo.py` add `torch`, and `run_gnn.py` also needs
`torch-geometric`.

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
[`Code/docs/EDGES_AND_NODES_NOTES.txt`](../../Code/docs/EDGES_AND_NODES_NOTES.txt):

| edge type | definition | pairs |
|---|---|---|
| geographic | hand-coded shared borders; optionally hop-graded at `0.5^(hop-1)` out to 3 hops | 23 + 21 anchor |
| correlation ("functional") | Pearson r of ILI histories above 0.85, computed on **pre-test weeks only** | 39 |
| demographic similarity | Gaussian kernel on 8 socio-economic features, median-heuristic bandwidth | 63 |
| uniform complete | control: every pair at weight 1 | 91 |

Overlapping types accumulate into one weighted adjacency (the default arm
reaches a maximum edge weight of 2.822), except in the paper model, which keeps the
geographic and correlation topologies as two separate channels.

---

## Models

| model | idea | features |
|---|---|---|
| `persistence` | next week equals this week | — |
| `seasonal_naive` | next week equals the same week last year | — |
| `arima` | per-neighborhood ARIMA, order chosen by walk-forward validation RMSE | own history |
| `lstm` | one LSTM over all 14 series jointly, no graph | 14 series |
| `xgboost` | boosted trees over the same per-node columns, pooled across nodes, no edges | 46 node features + node id |
| `dualtopo` | **Luo et al. 2025 Dual-Topo-STGCN.** The paper reference model, ILI rates only | 52 ILI lags |
| `gat` | **Luo et al. 2025 comparison model.** Standalone spatial GAT, no temporal encoder | 52 ILI lags |
| `gnn_st` | **the current design.** Dilated causal temporal convolutions per node, graph mixing with a learned adaptive adjacency, residual from a learned persistence/climatology blend, 10-seed ensemble | 16 lags × 2 channels + 6 weather + 8 demographics |

**Eight arms, and that is the whole leaderboard.** Five baselines, two models
from the paper being replicated, and one current design. Anything else named
`gnn_st_*` in the registry is an *ablation* — the same model with one piece
switched off — and belongs to [Ablations](#ablations), not here. Earlier
revisions of this document compared a family of superseded `gcn_fusion` arms
(`gnn_geo`, `gnn_corrbinary`, `gnn_multiedge`, `gnn_uniform` and five feature
variants); they were retired once `gnn_st` beat all of them at every horizon,
and their numbers live in git history rather than in this table.

Node features are 8 ILI lags, 6 weather variables and 8 static demographics.
Citywide covariates are ILI count, ED count, ILI/ED percentage, confirmed flu
cases and monthly cases. Everything added later — COVID and RSV cases,
wastewater, Rt, vaccination — defaults to **off**, so the baseline stays
reproducible and each addition is a clean ablation.

`gnn_st` predicts a residual from a learned persistence/climatology blend rather
than the level directly. That is deliberate: predicting the level makes
persistence an attractor, since "no change" scores well in the flat off-season.

### The current design: `gnn_st`

`InfluenzaGNN` — two `GCNConv` layers over the summed adjacency — is superseded
and no longer has a Boston arm. It survives in `influenza/models.py` only
because the five `xcity_*` cross-city arms still use it; when the cross-city
comparison is rebuilt it can go.

`SpatioTemporalGNN` differs in three ways, listed in measured order of value.

**1. It has a temporal axis at all.** `build_samples` hands the lookback over
flattened into the feature vector, so the old model saw eight lags as eight
unordered columns and had no way to represent "rising" versus "falling". The new
model reshapes them back into a sequence and runs a stack of gated, *causal*,
dilated 1-D convolutions along it — kernel 2 at dilations 1, 2, 4, 8, which
covers a 16-week lookback in four layers. Causal by left-padding, because a
centred kernel at the origin week would read the weeks after it, which is the
target. This one change is worth more than everything else here combined.

**2. It actually trains.** The old arm's own `run_config.json` records
`best_epoch=4, epochs_run=29`: with 122 per-sample updates at lr 3e-3 it
early-stopped almost immediately, and its 83–91% interval coverage was the same
underfitting seen from a second angle. The new path uses mini-batches of 16,
AdamW with 100× the weight decay, cosine annealing over a fixed 300-epoch
budget, and no early stopping — while keeping best-validation-state restore, so
the selected weights are still the best epoch rather than the last.

**3. It predicts a residual from a learned blend of two baselines**, not from the
origin week alone:

```
base_h     = σ(a_h) · level_at_origin + (1 − σ(a_h)) · climatology(target_week)
prediction = base_h + network_output
```

`a_h` is one scalar per horizon. The motivation is a measurement: on the test
season, Boston's citywide rate correlates 0.906 with its own value one week
earlier but only **0.271** four weeks earlier, while a plain harmonic
climatology holds **0.697 at every horizon** — it does not decay, because it is
the same curve however far ahead you ask. So the origin level is the right
anchor at h=1 and close to noise at h=4, and the old `delta` target was fighting
its own baseline there.

The sigmoid confines `a_h` to [0, 1], so the worst case is that it collapses onto
one of the two fixed baselines and cannot do worse than the better of them. That
is what makes one extra parameter per horizon safe on 122 training origins. The
learned values are recorded in `run_config.json` as
`blend_origin_share_per_horizon` and are a result in their own right.

The climatology is a per-neighborhood harmonic regression (3 harmonics on
day-of-year) on `log1p(rate)`, fitted in `influenza/climatology.py` on **training
rows only**, using the same row bound as the normalisation reference so the two
share one leakage boundary. Suppressed weeks are dropped per node rather than
imputed, because a seasonal mean built from invented zeros sits below the truth
everywhere.

**Edge types stay summed, and that is a measured choice, not an oversight.**
`Graph.relations` now carries one adjacency per edge type alongside their sum, so
the multi-relational path exists and `gnn_st_relations` uses it — but keeping the
types separate measured **worse** (−0.023 macro Corr at h=2, −0.021 at h=4) than
summing them. With 14 scored nodes and roughly 5,300 finite training cells, three
relation channels widen the mixer and overfit. The arm ships so the negative
result is on the record rather than assumed. What *does* help is a learned
**adaptive adjacency** from node embeddings, `softmax(relu(E₁E₂ᵀ))`, worth about
+0.02 to +0.03 macro for 336 parameters; `gnn_st_noadapt` is its ablation.

**A joint multi-horizon head also measured worse** (−0.03 to −0.05), so each
horizon is a separate direct model — which is what `run_all_horizons.py` already
assumed, and it keeps every horizon scoring the identical 49 target weeks.

**Loss.** Huber on the observed cells plus 0.3 × a soft-Pearson term. Corr is one
of the four reported `CORE_METRICS`, so training toward it is metric-aligned, and
two guard rails keep that claim honest: RMSE, MAE and MAPE come from the same
predictions and are reported unchanged, and **model selection on the validation
split stays plain masked MSE**, so the restored checkpoint is never
Pearson-selected. `gnn_st_nopearson` is the ablation. Reported honestly, the term
is a variance reducer more than an accuracy gain — it moves single-seed macro
Corr at h=2 by roughly +0.03 and barely moves the ensemble.

**Ten seeds, always.** The per-seed standard deviation of macro Corr at h=4 is
about 0.05 — wider than any single architecture change measured here — so a
one-seed number at that horizon cannot be told apart from a lucky draw. The
headline arm averages 10 seeds, splits the MC-Dropout budget across them so the
epistemic band also carries seed variance, and writes `seed_spread.csv` beside
the metrics. `gnn_st_1seed` shows what a single draw looks like.

MC-Dropout validity is preserved and enforced rather than assumed: all dropout is
functional, `LayerNorm` is the only normalisation (it keeps no running statistics,
so `model.train()` at inference still enables dropout only), and `run_gnn.py`
raises if any `nn.Dropout` or BatchNorm module appears in the graph.

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

### How good can any model get here? A measured ceiling

Before reading the correlation numbers, it is worth knowing what they are being
read against, because it is not 1.0.

Take the citywide mean rate **at the target week** — i.e. cheat completely — and
distribute it across neighborhoods by each one's historical share of the
citywide mean, fitted on pre-test weeks only. That oracle scores:

| | macro Corr | pooled Corr | RMSE |
|---|---|---|---|
| oracle: exact citywide × static neighborhood share | **0.938** | **0.966** | 8.10 |
| oracle: exact HHS-1 (New England) %ILI × per-neighborhood scale | 0.918 | — | 16.57 |
| oracle: exact Massachusetts %ILI × per-neighborhood scale | 0.922 | — | 17.67 |

The two regional rows are new and answer a question worth separating from the
first: *how much of Boston is just New England?* Almost all of it. Knowing the
region's curve exactly places Boston's neighborhoods at 0.918 macro, barely below
the 0.938 that Boston's own citywide curve buys. The RMSE is twice as bad
because FluView reports weighted percent-ILI among outpatient visits while the
target is an ED-visit rate per 100,000 residents — two different measurands, so
the mapping is a per-neighborhood scale fitted by least squares through the
origin on pre-test weeks only. It gets the shape right and the level
approximately. Fetch the data with `Code/scrapers/scrape_fluview.py`.

**Why regional ILI is not a leaderboard baseline.** As an oracle it is a ceiling;
as a forecast it is poor, and for a reason that matters to this project. The
regional series is *synchronous* with Boston — over 436 shared weeks it
correlates best at zero lag, HHS-1 at r=0.927 and Massachusetts at r=0.887,
falling away symmetrically on both sides — and FluView publishes about a week
behind. So at origin *t* a real-time forecaster holds a week-old copy of a signal
that moves with Boston rather than ahead of it. At h=2 that is a three-week-old
number, and it scores like one: macro Corr 0.444 and RMSE 36.31 against
persistence's 0.618 and 23.84, with `compare_timing.py` reporting it three weeks
late. Two further objections are practical rather than conceptual: the fitted
per-neighborhood scale makes it a fitted model, unlike the parameter-free naive
baselines it would sit beside, and the real-time vintage archive covers only 43
of the 49 target weeks for HHS-1 and 33 for Massachusetts, so it cannot be scored
on the same cells as everything else.

Use the revised values instead and the numbers improve to 0.461 and 34.70 — still
far below persistence, and a look-ahead, since all 19 recent HHS-1 weeks checked
were revised after first publication by up to 7.9%. `--first-release` on the
scraper is what keeps that honest.

So Boston's 14 neighborhoods co-move almost perfectly: knowing the citywide curve
is worth 0.938 macro **at every horizon**, and there is very little
neighborhood-idiosyncratic signal left for a graph to find. Per-node correlation
with the citywide mean over the test window runs 0.776 to 0.987, median 0.959.

The consequence is that **macro Corr ≈ 0.94 × (how well the citywide curve is
forecast)**, and citywide forecastability is what actually binds:

| h | citywide persistence | citywide climatology | ridge on lags + climatology | + MA/HHS-1 surveillance |
|---|---|---|---|---|
| 1 | 0.906 | 0.697 | 0.901 | **0.912** |
| 2 | 0.695 | 0.697 | 0.740 | **0.765** |
| 4 | 0.271 | **0.697** | 0.413 | 0.453 |

Three things follow, and they are stated here so the numbers in
[Results](#results) are read correctly:

- **macro Corr of 0.90 at two or four weeks ahead is not attainable on this
  data.** It would require forecasting the citywide curve at ~0.96 correlation at
  that horizon. Four-week-ahead citywide persistence is 0.271, and nothing in the
  influenza forecasting literature reaches 0.96 at four weeks. This is a property
  of how predictable the epidemic curve is, not of the model.
- **One week ahead is not a hard question and no model can win by much there.**
  Citywide persistence is already 0.906. That is why the interesting margin is at
  h=2 and h=4, where the naive baselines collapse.
- **At four weeks the seasonal climatology beats every autoregressive model
  tried** (0.697 against 0.413–0.453), which is what motivates the blended target
  described above. It was the largest unclaimed win in the repository.

The oracle row also puts a floor under RMSE: 8.10 per 100,000 with perfect
citywide knowledge, against roughly 5 per 100,000 of off-season mean rate. Weekly
Poisson noise and BPHC suppression account for the rest.

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

### Forecast timing: the models are late

Every model here gets the shape of the season right and arrives behind it. That
is the largest remaining source of error at two weeks ahead, and until
`Code/compare_timing.py` was written nothing in the repository measured it.

The measurement is a shift. Slide the whole predicted series one week earlier on
the calendar — nothing retrained, only the dates relabelled — and score it again:

| `gnn_st`, h=2 | typical weekly miss | in step with the truth |
|---|---|---|
| as shipped | 17.20 per 100k | 0.801 |
| **slid one week earlier** | **10.79 per 100k** | **0.908** |

**63% of the squared error at h=2 is bad timing, not wrong height.** Three
readings agree:

- **The lag fingerprint.** Correlation between the residual and the truth's
  week-over-week change is **−0.80** at h=2 (−0.90 at h=1, −0.57 at h=4). Near
  −1 is the algebraic signature of a pure phase shift — low exactly while the
  curve climbs, high exactly while it falls. `persistence` scores −1.000 at h=1,
  which is the calibration check: it *is* a lag-1 copy, and the diagnostic says
  so.
- **Peak week.** At h=2, 9 of 14 neighborhoods peak two weeks late and 3 one week
  late. Dorchester's observed peak is 2025-12-21 at 256.1; `gnn_st` peaks
  2026-01-04 at 268.5 — the height is right to within 5%, the timing is two weeks
  out.
- **Coverage by regime.** 95.5% overall but **83.9% on weeks when the curve is
  climbing** against 97.4% when it is falling. The band is not too narrow; it is
  pointed at the wrong weeks, because its width is a function of the (late)
  predicted level.

**The shift is a diagnostic, never a result.** Sliding an h=2 forecast a week
earlier is exactly relabelling it as h=1: it buys the accuracy with a week of
lead time. The columns bound what a phase correction could recover; they are not
a score.

#### Where it comes from, and four things that do not fix it

Two causes, both measured. The learned origin share at h=2 is **0.68**, so more
than two thirds of the baseline is the level from two weeks *before* the target
week — a stale anchor is a phase lag the residual then has to undo. And the loss
prices height but never timing: under squared error, when the turn date is
uncertain, a smoothed slightly-late peak is the risk-minimising forecast. Being
late is the cheap hedge.

Four remedies were measured and none of them moved it. They are listed because
each one rules out an explanation:

| tried | result |
|---|---|
| **any existing ablation arm** | The lag fingerprint sits between −0.79 and −0.81 for all 25 arms at h=2 — `noadapt`, `relations`, `lagsonly`, `nograph`, `delta`, `wastewater`. No architecture or feature switch touches timing. |
| **`gnn_st_slopeweight`** — weight the loss by how far the epidemic moved | **Worse.** One week late became two; RMSE 17.21 → 18.37, macro Corr 0.802 → 0.785. Its learned origin share *rose* to 0.713: charging more for the moving cells made it lean harder on persistence. |
| **`gnn_st_trendblend`** — extrapolate the anchor along the recent trend | **Null.** Fingerprint −0.807 against −0.801, still one week late, RMSE 17.39 against 17.21. The sigmoid bound worked as designed: the model learned a trend share of only **0.167**, i.e. it declined. Consistent with the separate finding that adding the observed slope to the forecast directly makes RMSE worse at every weight (19.1 → 20.5 → 24.0 per 100,000 as the weight goes 0 → 0.5 → 1.0) — the weekly difference is mostly Poisson noise and suppression. |
| **regional surveillance as a leading indicator** | **Not built, because it does not lead.** Over 436 shared weeks, CDC FluView ILINet correlates with Boston's citywide curve best at **zero** lag — HHS Region 1 r=0.927, Massachusetts r=0.887 — and falls away symmetrically on both sides. FluView also publishes about a week behind, so at a given origin it would arrive as a *lagged* copy of a synchronous signal. It carries level information, not phase information, which is why the ridge row above gains only 0.740 → 0.765 from it. |

The honest summary is that the lag is not a bug in any one component. It is what
this loss, on this information set, is choosing — and the information that would
fix it does not appear to be in the data the project currently has. That last
clause is a measurement, not a shrug: every candidate signal in the repository
was cross-correlated against Boston's citywide curve, and **none of them lead
it**.

| candidate | best alignment | r |
|---|---|---|
| influenza wastewater | synchronous | 0.937 |
| ED ILI count | synchronous | 0.985 |
| ED ILI share | synchronous | 0.984 |
| confirmed flu cases | synchronous | 0.870 |
| HHS-1 / Massachusetts %ILI | synchronous | 0.927 / 0.887 |
| COVID wastewater | lags by 1 | 0.335 |
| RSV wastewater | leads by 3 | 0.693 |

Wastewater is the one that looks most promising a priori and it is synchronous,
which explains why `gnn_st_wastewater` never moved the timing. RSV wastewater is
the only candidate that leads, and its r of 0.693 is within noise of the 0.697 a
plain harmonic climatology scores at every horizon — it is the seasonal curve in
disguise, RSV season simply running ahead of flu season, and the blended target
already subtracts that curve. `gnn_st_covid_rsv` measuring worse is consistent.

#### The one correction that does work

`compare_timing.py --delag` advances the phase using the model's own slope
**across horizons from a single origin**. At origin *t* the h-week and the
nearest shorter-horizon model have both run, so

    slope_per_week = (p_h(t+h) - p_s(t+s)) / (h - s)

is an estimate of one week of movement assembled entirely from forecasts made at
origin *t* — no look-ahead — and far less noisy than the observed weekly
difference, which is what made the naive version fail. The corrected forecast is
`p_h + gamma * slope_per_week`.

`gamma` is fitted by least squares on the **validation** split — `run_gnn.py`
writes `predictions_val.csv` for exactly this — and applied unchanged to test,
the same boundary the interval parameters respect. At h=2 the fitted value is
**0.383**, from 280 validation rows:

| `gnn_st`, h=2 | typical weekly miss | in step with truth | share of error that is timing |
|---|---|---|---|
| as shipped | 17.21 | 0.802 | 0.63 |
| + de-lag, gamma fitted on validation | **16.75** | **0.815** | 0.58 |

The size of that gap is itself the argument for fitting it. Scanning `gamma` over
the *test* weeks picks 1.0 and reports 16.13 and 0.826 — roughly twice the gain.
None of that extra is real; it is the scan reading the answer it is being scored
against. Quote the fitted row.

Three caveats. **It is not universal**: it helps `gnn_st`, but at `gamma = 1` it
makes `lstm` and `arima` worse at h=2, because it relies on the gap between two of
the model's own forecasts being signal rather than noise, and for a
near-persistence model that gap is noise. **It shaves the lag rather than
removing it**: the fingerprint moves from −0.801 to −0.778 and the forecast is
still one week late. **It does not move the peak.** Peak-week error stays at two
weeks at h=2 even under the correction — the cross-horizon slope is near zero
exactly at the turn, so extrapolating it advances the limbs of the curve and not
its apex. Getting the peak week right remains unsolved here.

#### The h=2 noise floor, measured

Before any h=2 architecture claim: how much does a 10-seed ensemble move between
runs? Three disjoint seed blocks (42-51, 142-151, 242-251) on the canonical 49
weeks:

| arm | RMSE | macro Corr |
|---|---|---|
| `gnn_st` | 17.07 ± 0.13 | 0.806 ± 0.004 |
| `gnn_cascade` | 17.11 ± 0.29 | 0.804 ± 0.006 |

Two things follow. **A difference below about 0.01 macro at h=2 is not a
difference**, and several numbers previously quoted in this document sit in that
range. And **the committed `gnn_st` headline of 0.801 / 17.20 is a slightly
unlucky draw** — the arm's mean over three blocks is 0.806 / 17.07. The headline
is kept as the reproducible single block, but it should not be read as the arm's
central value.

#### Joint horizons and the cascade: no effect at h=2, worse at h=4

`gnn_cascade` trains horizons 1 and 2 together and anchors the h=2 baseline on
the model's **own h=1 forecast** instead of the origin level. `gnn_st_joint` is
the control: joint training with the ordinary blended baseline.

A first batch looked like a clear win — 16.66 RMSE and 0.822 macro against the
reference's 17.38 and 0.800 on their 48 shared weeks. It did not hold. Against
the measured floor above, the cascade's mean is **0.804 against the reference's
0.806**: nothing, and if anything the wrong way. The first batch was a low draw
of its own arm's distribution, on a train/validation split shifted by one origin.

**At h=4 the joint arms are clearly worse**, and there the gap does outrun the
noise: `gnn_cascade_h4` scores 23.83 RMSE and 0.548 macro and its control
`gnn_st_joint_h4` 24.12 and 0.534, against the single-horizon `gnn_st`'s 23.07
and 0.582. That is consistent with the older finding that a joint multi-horizon
head measured 0.03 to 0.05 worse, and it withdraws the suggestion made earlier in
this document that the older finding was stale. It was not.

**On Columbus the cascade is ahead** — 8.43 RMSE and 0.761 macro against 8.80 and
0.740 at h=2. That margin is 0.021 macro, several times the Boston floor, so it
is the one place this idea looks alive. It has not been replicated with a second
seed block, and it should be before it is believed.

The lag is untouched by all of it: the fingerprint stays at −0.80 and Dorchester's
peak stays two weeks late in every arm.

#### What the de-lag is actually worth

Re-measured against the floor, on three disjoint seed blocks of `gnn_cascade`,
with gamma fitted on each block's own validation split:

| block | fitted gamma | RMSE | macro Corr |
|---|---|---|---|
| 42-51 | 0.155 | 17.25 → 16.83 | 0.802 → 0.812 |
| 142-151 | 0.097 | 17.31 → 17.03 | 0.800 → 0.807 |
| 242-251 | 0.014 | 16.78 → 16.74 | 0.811 → 0.812 |

**+0.006 ± 0.005 macro, improving 3 of 3 blocks.** Small, and smaller than the
0.013 quoted earlier from a single run of the single-horizon arm, but consistent
in sign across independent draws, which is the evidence that matters. The fitted
gamma itself varies a lot between blocks (0.014 to 0.155), so the size of the
correction is not stable even where its direction is.

**Ensembling is not the missing ingredient either.** At h=2 the test residuals of
`gnn_st` correlate 0.797 with `xgboost`, 0.851 with `lstm`, 0.897 with `arima`
and 0.910 with `persistence`: the models are wrong in the same weeks, in the same
direction, because they are all late. Every equal-weight blend with `gnn_st`
scores worse than `gnn_st` alone (RMSE 17.78 to 20.06 against 17.20). There is no
decorrelated error left to average away.

#### What the band can do about it

The point forecast stays late, but the interval does not have to inherit that.
`--two-sided-intervals` fits the two edges separately by quantile regression of
the signed residual on the predicted level, instead of one symmetric width
(`influenza/intervals.py`). A symmetric band cannot represent a skewed residual,
and a late forecast's residuals are skewed.

At h=2, on the 10-seed `gnn_st`:

| | all weeks | rising | flat | falling | worst regime off 95% | mean width |
|---|---|---|---|---|---|---|
| symmetric | 95.9% | 85.2% | 100.0% | 97.4% | 9.8 pt | 39.4 |
| **two-sided** | 94.7% | **90.6%** | 98.9% | 90.3% | **4.7 pt** | 43.8 |

Through Dorchester's peak it covers 6 of 8 weeks against 4 of 8. It is a flag
and not the new default, for two measured reasons. It helps **only where the
symmetric band was actually broken**: at h=1 it is a wash (worst regime 5.1 pt →
6.6 pt) and at h=4 it is worse (4.6 pt → 8.5 pt), because at those horizons the
symmetric band was already close to uniform. And `seasonal_naive` degrades badly
under it (97.4% → 89.5% overall, 98.1% → 80.6% on falling weeks): both edges are
linear in the model's *own* predicted level, which only describes its residual
spread if the prediction is about this season, and the seasonal baseline predicts
last year's. Turn it on for every model or none, so the widths stay comparable.

### Severity bands

RMSE says how close the number was. It does not say whether the model would have
raised the alert in the week that mattered. `Code/compare_severity.py` scores
that separately, using CDC-style
[in-season severity](https://www.cdc.gov/flu-burden/php/surveillance/in-season-severity.html)
intensity thresholds built by the Moving Epidemic Method:

```bash
python Code/compare_severity.py --results-dir Code/results/horizon_01 --variant post_covid
python Code/compare_severity.py --reference-seasons exclude_covid    # threshold sensitivity
python Code/compare_severity.py --rank-by CSI                        # re-rank by hit rate
```

Each week is banded `low / moderate / high / very high` against thresholds fitted
per neighborhood on the three post-COVID reference seasons, using only weeks
before `TEST_START`. Citywide the 2025-26 season peaked at 101.9 per 100,000 in
the week of 2025-12-21, between IT90 (98.2) and IT98 (134.2) — **a high severity
season**. Four things are then scored: whether the crossing was called, whether
the right band was called, whether the exceedance probabilities were honest, and
whether the onset week was called on time.

**Accuracy is meaningless here and the tables do not lead with it.** Only 51 of
627 neighborhood-weeks crossed IT50, so a forecast that never alerts scores 91.9%
— and `dualtopo`, which never crosses IT50 in this window, duly does. The
headline is the Peirce skill score, which is 0 for both a never-alert and an
always-alert forecast.

<!-- BEGIN SEVERITY -->
Horizon 1, all neighborhood-weeks pooled, full year. Thresholds from 2022-23, 2023-24, 2024-25, fitted on weeks before 2025-05-31.

| model | variant | PSS (IT50) | CSI (IT50) | PSS (IT90) | CSI (IT90) | band exact |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | post_covid | 0.767 | 0.656 | 0.440 | 0.381 | 0.946 |
| lstm | post_covid | 0.729 | 0.633 | 0.000 | 0.000 | 0.939 |
| persistence | post_covid | 0.680 | 0.545 | 0.428 | 0.286 | 0.928 |
| arima | post_covid | 0.669 | 0.574 | 0.322 | 0.240 | 0.936 |
| xgboost | post_covid | 0.605 | 0.500 | -0.002 | 0.000 | 0.928 |
| gat | post_covid | 0.270 | 0.231 | 0.000 | 0.000 | 0.912 |
| dualtopo | post_covid | 0.000 | 0.000 | 0.000 | 0.000 | 0.919 |
| seasonal_naive | post_covid | -0.016 | 0.047 | -0.056 | 0.000 | 0.801 |

PSS (Peirce skill score) is 0 for both a never-alert and an always-alert forecast, so it cannot be gamed by the 8% base rate. Method and caveats: [`Code/docs/SEVERITY.md`](Code/docs/SEVERITY.md). Full tables: [`Code/results/horizon_01/_comparison/severity_leaderboard.md`](Code/results/horizon_01/_comparison/severity_leaderboard.md).
<!-- END SEVERITY -->

Method, the reference-season sensitivity and the limitations are in
[`Code/docs/SEVERITY.md`](../../Code/docs/SEVERITY.md). Read the limitations before
quoting the numbers: one test season, one seed, and IT98 is crossed twice.

### Looking at the forecasts

```bash
python Code/plot_forecasts.py                                  # 4 models, all 14 neighborhoods
python Code/plot_forecasts.py --models persistence,arima,lstm,gnn_st
python Code/plot_forecasts.py --horizon 2 --no-ci
python Code/plot_forecasts.py --neighborhoods Dorchester,Roxbury --shared-y
```

Writes `results/horizon_01/_comparison/forecast_overlay_h1.png` (one panel per
neighborhood) and `forecast_citywide_h1.png` (the 14-neighborhood mean in one
large panel). Observed is the black line; each model gets a fixed categorical
colour plus its own marker shape, and the shaded ribbon is its 95% interval.

The overlay is worth reading before trusting any table, because it separates
two kinds of error that one RMSE number adds together.

The superseded `gcn_fusion` arms failed here in a way no metric flagged: they
tracked the December peak, then sat at roughly 50 per 100,000 from February
onward while the observed series fell back to about 20 — a sustained
over-prediction across nearly every neighborhood. **`gnn_st` does not do this.**
Over the 14 weeks from February 2026 its citywide mean is 19.4 against an
observed 19.3, a bias of +0.1; across the whole window it is +0.3. Learning a
residual from a persistence/climatology blend, rather than the level, is what
removed it.

What is left instead is **peak under-shoot**. At the 2025-12-21 peak the
observed citywide mean is 101.9 and `gnn_st` predicts 83.0 — it is roughly
unbiased on average and short at the top, which is the opposite failure and the
more useful one to have if the alternative is a flat 50 all spring. It is also
invisible in an annual RMSE, which is the argument for the
[severity bands](#severity-bands) above.

Four models is the cap, because four is the number of categorical colours
validated as distinguishable under colour-vision deficiency; the script refuses a
fifth rather than silently reusing a hue.

---

### Figure style

Every figure uses one plain style, defined in `influenza/palette.py` and
matching the per-run grid (`plots.save_grid_plot`): white background, all four
spines, no gridlines, default black text, one centred `fig.suptitle`, the legend
inside the axes, dpi 160. Caveats that used to be drawn as 8pt subtitle
paragraphs are printed to stdout instead, where they can be quoted.

The palette's four categorical slots are fixed-order and never cycled
(`series_colour` raises past four). Slot 2 is the grid plot's predicted red, so
a model is the same colour in its own grid and in a comparison figure. The
observed series never shares a slot with a model — asserted at import, because
it briefly did during the restyle and "Observed" and "persistence" drew as one
line. Slot 4 is purple rather than yellow: yellow failed contrast on white, and
the markers that used to compensate were removed.

`THRESHOLD_STYLES` (the three dashed severity lines) is defined once in
`palette.py`; it used to be copied verbatim into `plots.py` and
`plot_forecasts.py`.

## Results

<!-- BEGIN LEADERBOARD -->
`variant=post_covid`, `segment=overall`, 627 neighborhood-weeks, test targets
2025-06-01 to 2026-05-03. Graph models are 10-seed ensembles. **macro** is the
mean of the 14 per-neighborhood correlations and is the metric comparable to Luo
et al.'s 0.8202; **pooled** is higher by construction because it also gets credit
for knowing which neighborhoods are busy -- a model predicting each
neighborhood's flat historical average scores pooled 0.402 and macro 0.000.

| model | h=1 macro | h=1 RMSE | h=2 macro | h=2 RMSE | h=4 macro | h=4 RMSE |
| --- | --- | --- | --- | --- | --- | --- |
| gnn_st | **0.892** | **11.77** | **0.801** | **17.20** | **0.598** | **23.14** |
| xgboost | 0.821 | 15.62 | 0.675 | 20.29 | 0.595 | 23.43 |
| lstm | 0.867 | 14.66 | 0.684 | 21.36 | 0.440 | 26.67 |
| arima | 0.788 | 15.51 | 0.625 | 21.55 | 0.254 | 28.92 |
| persistence | 0.798 | 15.81 | 0.618 | 23.84 | 0.224 | 34.91 |
| gat (paper comparison) | 0.644 | 22.45 | 0.391 | 27.54 | 0.179 | 31.99 |
| dualtopo (paper) | 0.426 | 28.91 | -0.334 | 29.10 | 0.513 | 29.20 |
| seasonal_naive | 0.296 | 39.84 | 0.296 | 39.84 | 0.296 | 39.84 |

**Horizon 2 is the defensible headline.** The margin over the best baseline is
**+0.117 macro** there (0.801 against the LSTM's 0.684), far outside the ±0.015
noise floor. At horizon 1 no model can win by much -- citywide persistence
already correlates 0.906 with next week -- and at horizon 4 the margin over
`xgboost` is **+0.003**, deep *inside* that horizon's ±0.05 floor, so h=4 is a
dead tie with a gradient booster rather than a win. An earlier draft of this
section claimed +0.112 at h=4; that was measured against `dualtopo` before a
competent tabular baseline existed.

**Against the paper.** Luo et al. report mean-across-counties Corr **0.8202** at
h=1 (nowcast). `gnn_st` scores 0.892 at h=1, beating it by 0.072. At h=2 it
scores 0.801, which is 0.019 *short* of the paper's h=1 figure -- close, at double
the horizon, but not clearing it.

**Both Luo et al. models are in this table, and both place last.** `gat` is the
paper's own comparison model and `dualtopo` its main one; see
[The paper reference](#the-paper-reference) for why reimplementing them faithfully
still leaves them behind a 2018-vintage LSTM, and
[Attention](#attention-two-different-questions-two-different-answers) for the
arm that isolates why.

**Read these against 0.94, not 1.0** -- see
[the measured ceiling](#how-good-can-any-model-get-here-a-measured-ceiling).

**`dualtopo` placing third at h=4 on macro while last on pooled is not a
comeback.** It barely responds to its inputs: fatal at h=1, accidentally
protective at h=4 when every other model overreacts to a stale origin week.
<!-- END LEADERBOARD -->

Regenerate with `python Code/compare_models.py --update-readme`. Full table,
plot and per-segment breakdown in `Code/results/horizon_01/_comparison/`.

### Per-neighborhood leaderboard

The table above pools all 14 neighborhoods into one set of cells, which hides a
lot. `Code/compare_models.py` also writes
[`results/horizon_01/_comparison/leaderboard_by_neighborhood.md`](../../Code/results/horizon_01/_comparison/leaderboard_by_neighborhood.md)
(and `comparison_by_neighborhood.csv`): a win-count summary broken out by
segment, then one section per neighborhood ordered by disease burden — each with
three sub-tables (overall, flu season, off-season) carrying that segment's mean
rate and week count. 14 neighborhoods × 3 segments = 42 ranked tables.

Neighborhoods won at horizon 1, by segment:

| model | overall | flu season | off-season |
|---|---|---|---|
| `gnn_st` | 14 | 13 | 5 |
| `lstm` | 0 | 0 | 5 |
| `xgboost` | 0 | 0 | 2 |
| `arima` | 0 | 1 | 0 |
| `persistence` | 0 | 0 | 1 |
| `seasonal_naive` | 0 | 0 | 1 |

**Here the per-neighborhood view agrees with the pooled one, which was not
always true.** `gnn_st` wins all 14 neighborhoods overall and 32 of the 42
segment-by-neighborhood cells. An earlier revision of this section reported the
opposite — the LSTM taking 12 of 14 while the graph models won 2 cells out of 42
— and called that "the clearest single statement of where this project currently
stands". That statement was true of the superseded `gcn_fusion` arms and is no
longer true of `gnn_st`; it is recorded here because the reversal is the result,
not a footnote to it.

What survives from that earlier reading is the **off-season**, where `gnn_st`
takes only 5 of 14 and the split is nearly even between it, the LSTM and
`xgboost`. Off-season rates are low and flat, so every model is close to the
floor and the ranking there is close to noise. The flu season is where the
ordering is real: 13 of 14, with ARIMA taking only Fenway.

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

**Among the baselines, nothing beats persistence at one week ahead.** ARIMA
(15.51) and persistence (15.81) are statistically indistinguishable, and ARIMA's
selected orders are mostly `(0,1,x)` — a differenced random walk, which *is*
persistence with extra steps. Any claim about a model "working" here has to clear
15.81, and for a long time the project had no naive baseline to notice that.

**`gnn_st` does clear it: 11.77 against persistence's 15.81, a 26% reduction.**
An earlier revision of this section said flatly that nothing beats persistence at
one week; that was true when the graph arms were `gcn_fusion` and is no longer
true. The margin is still smallest here and largest at h=4, for the reason given
in the leaderboard above.

**Having a graph helps; how it is wired barely matters.** This is now measured on
`gnn_st` by retraining rather than inferred from a ranking of separate arms.
Removing spatial mixing altogether costs **0.090 macro Corr**; removing the
correlation edges costs 0.015, using the adaptive adjacency alone costs 0.017,
and geography alone costs 0.007 — the last of which is inside the noise floor.
See [Which edges earn their place](#which-edges-earn-their-place). An earlier
revision made this argument from the ordering of four superseded `gcn_fusion`
arms, which confounded the edge set with every other difference between them.

**RETRACTED: "COVID and RSV data is the single biggest improvement."** This
section used to report that adding monthly neighborhood COVID/RSV rates plus
COVID wastewater took MultiEdge from 24.5 to 16.8 RMSE, and called respiratory
co-circulation "the most promising direction in the repository."

That gain does not survive the September 2026 data fixes. Re-measured on
`gnn_st` at two weeks ahead, the same feature group now **costs** 0.119 macro
Corr and adds 3.67 RMSE — the largest harm of any group tested. Two of the five
defects landed directly on these inputs: the COVID wastewater series carried a
one-day look-ahead into the horizon-1 target week (defect 7), and the monthly
citywide series read the *following* month on 89 of 436 weeks (defect 8). The
original improvement was measured on inputs that could see the answer.

A capacity explanation is also live and is not excluded by the combined arm:
these are three extra per-node channels, taking the temporal block from 32 to 80
features on 122 training origins. `gnn_st_covid_rsv_cases` (cases, no
wastewater) and `gnn_st_covid_ww` (wastewater only) split the two.

The lesson generalises past this one feature: **every result in this repository
that depended on a covariate rather than on the target series should be treated
as provisional until re-measured**, because four of the five defects were in
covariate loading and none of them touched `load_rates`.

**More history matters more than architecture.** Training on the full 436-week
series instead of the 201 post-COVID weeks improved the superseded graph arms
from 24.5 to 20.5 RMSE and Dual-Topo from 28.9 to 19.6. The 52-week input window
in particular is starved on the post-COVID slice: 85 training origins against the
paper's 364. (Those two `full`-variant arms have been retired along with the rest
of the `gcn_fusion` family; the finding stands on the numbers above and the
`gnn_st_full` arm still tests it for the current design, where it measured
*worse*.)

**The paper's background-node claim does not replicate.** Luo et al. report that
adding an ocean/open-land node lifted Corr by 0.135. On Boston, `dualtopo` versus
`dualtopo_no_bg` gave 0.4169 versus 0.4122 — a difference of 0.005, well inside
noise. The `dualtopo_no_bg` arm has since been retired to keep the leaderboard to
one arm per model; this number is therefore archival. Restoring it is a
six-line registry entry (`replace(dualtopo, name="dualtopo_no_bg",
graph=replace(dualtopo.graph, anchors="none"))`) if the claim needs re-testing.

**Horizon 2 is where the graph model earns its place.** Persistence degrades
from 15.81 to 23.84 while `gnn_st` goes 11.77 to 17.20, so the gap widens from
4.0 to 6.6 RMSE. Two weeks ahead is a harder problem where "assume no change"
stops being a good answer, and by four weeks persistence is at 34.91 against
`gnn_st`'s 23.14. See [Forecast horizons](#forecast-horizons).

**The ranking is not the same in every segment**, which is the main reason all
three are reported. ARIMA is competitive overall and in the flu season but falls
to sixth in the off-season (7.92), behind even persistence. Most striking is the
seasonal naive: **last in the flu season by a wide margin (52.81) and fourth in
the off-season (6.91)**. That is the model behaving exactly as its assumption
dictates — "the same week last year" is a reasonable guess when the series is
flat, and hopeless when peak timing and magnitude move. A single full-year number
averages those two opposite behaviours into one uninformative figure.

**The off-season is also where the old graph arms were worst, and where `gnn_st`
is no longer.** The superseded `gcn_fusion` arms posted 20.88 against
persistence's 7.13, nearly three times worse — spending capacity tracking noise
in a flat series. `gnn_st` posts **5.68 against persistence's 7.13**, the best of
any arm. That reversal is the clearest single effect of learning a residual from
a persistence/climatology blend instead of predicting the level: when there is
nothing to track, the model falls back on the blend rather than inventing
movement.

---

## Is the comparison fair? The models do not see the same data

The headline table gives `gnn_st` strictly more information than any baseline,
and that has to be said before the numbers are read:

| model | what it sees |
| --- | --- |
| `persistence` / `seasonal_naive` | one past value of the own series |
| `arima` | **the own neighborhood's history only** — univariate, 14 separate models |
| `lstm` | **all 14 ILI series** — no weather, demographics, covariates or graph |
| `gnn_st_lagsonly` | all 14 series **plus the graph** |
| `gnn_st` | the above plus weather and static demographics |

So `gnn_st` versus `lstm` conflates two things — a better model and more inputs —
and `arima` is not a peer at all: it cannot see any other neighborhood.

`gnn_st_lagsonly` exists to break that confound. It takes 16 flu lags and
nothing else: no weather, no demographics, no city-wide covariate, no calendar,
no demographic edges. Its inputs are the same 14 ILI series the LSTM reads, so
the only remaining differences are the architecture and the graph.

### The controlled comparison, 10-seed ensembles

| macro Corr | `gnn_st_lagsonly` (16 inputs) | `lstm` (same data) | Δ |
| --- | --- | --- | --- |
| h=1 | 0.880 | 0.867 | +0.013 |
| h=2 | 0.794 | 0.684 | **+0.110** |
| h=4 | 0.559 | 0.440 | **+0.119** |

**The margin survives stripping every covariate.** On matched inputs the graph
model still beats the LSTM by 0.110 at two weeks and 0.119 at four. Whatever the
improvement is, it is not a data advantage — which is the claim this table exists
to support, and the row to quote when the comparison is challenged.

### What the extra 30 inputs actually buy

| `lagsonly` − `gnn_st`, macro | h=1 | h=2 | h=4 |
| --- | --- | --- | --- |
| Δ | −0.012 | −0.008 | −0.023 |
| neighborhoods improved | 0/14 | 2/14 | 1/14 |

**The extra inputs earn their place, and this row used to say the opposite.** The
previous version read −0.012 / **+0.009** / −0.032 and concluded "a model with a
third of the inputs performs the same". That +0.009 was measured against a
transit-era reference carrying three global covariates the default no longer has,
so the comparison was never `lagsonly` versus `gnn_st` alone. Re-measured
like-for-like at ten seeds, stripping the covariates costs accuracy at all three
horizons and improves at most 2 of 14 neighborhoods.

**But it is weather doing essentially all of that work.** Dropping weather alone
costs 0.031 at h=2 with 0/14 neighborhoods preferring it gone, while the
demographic block measures at or below zero everywhere and is actively harmful at
h=4. So the correct reading is not "the covariates are worth 0.008" but "weather
is worth having and the rest of the block is not" — see
[the ablations](#what-the-ablations-settle) for the split. The city-wide
covariate and the calendar were moved out of `DEFAULT_GLOBALS` and `FeatureSpec`
on that basis and the ten-seed study agrees at h=1 and h=2; both help at h=4.

### One caveat that stays even in the matched comparison

39 of the 107 undirected edges are correlation edges, thresholded on the ILI
series itself. That is done on pre-test weeks only and is not leakage, but it
does mean the graph hands the model structure derived from the training data that
the LSTM has to learn from scratch. `gnn_st_noadapt` and the geographic-only arms
bound how much of the result depends on it. Reported rather than argued away.

## Ablations

`Code/run_ablation.py` runs each arm as `gnn_st` with exactly one change, refits
from scratch, and re-runs the reference at the same seed count. Feature groups
are **removed and the model retrained**, not permuted: several groups are
constant within a forecast origin, so expected-gradient attribution gives them
exactly zero by construction and cannot measure them at all.

**How big does a difference have to be before it counts?** It is measured, not
assumed. Every study runs the reference three times on disjoint seed blocks
(`gnn_st`, `gnn_st_ref_b` at seed 142, `gnn_st_ref_c` at 242) -- identical
configurations differing only in which seeds they drew -- and the full range of
those three is the threshold. At ten seeds:

| horizon | reference ensembles (macro Corr) | floor |
| --- | --- | --- |
| 1 | 0.893, 0.895, 0.892 | **0.003** |
| 2 | 0.802, 0.807, 0.808 | **0.006** |
| 4 | 0.582, 0.613, 0.587 | **0.031** |

An earlier version of this section quoted 0.015 at h=2 and 0.05 at h=4. Those
were *per-seed* spreads, and every arm in the table is a *ten-seed ensemble*;
averaging ten models shrinks the spread by roughly the square root of ten. Using
the per-seed number as an ensemble threshold was too conservative by a factor of
two to five and buried real effects as "inside noise".

**Read the paired column alongside the floor, especially at h=4.** The macro
number is a mean over 14 neighborhoods, so each arm is also differenced against
the reference neighborhood by neighborhood and tested with a Wilcoxon signed-rank
test. The two disagree usefully. At h=4 the floor is 0.031 -- inflated by one
reference ensemble landing at 0.613 against 0.582 and 0.587 -- so almost nothing
clears it, while the paired test shows several effects moving 13 or 14 of 14
neighborhoods the same way. An effect that is consistent across every
neighborhood but small on average is a real effect measured against a noisy
average, not noise.

### What the ablations settle

Ten seeds, horizons 1/2/4, one code version, one graph, 22 arms plus three
reference ensembles -- 75 runs. Full tables in
`Code/results/_ablation/ablation_main_s10.md`; Δ is macro Corr against the
reference, and `n/14` is how many neighborhoods the arm improved.

**Keep, at every horizon:**

| group | h=1 | h=2 | h=4 | |
| --- | --- | --- | --- | --- |
| weather (6 columns) | −0.012, 0/14 | −0.031, 0/14 | −0.025, 0/14 | removing it hurts everywhere |
| everything except flu lags | −0.012, 0/14 | −0.008, 2/14 | −0.023, 1/14 | the non-lag block earns its place as a block |
| the blended target vs. origin level | −0.010, 0/14 | −0.019, 1/14 | −0.096, 0/14 | the largest design effect at h=4 |
| the blended target vs. no baseline | −0.000, 7/14 | −0.059, 2/14 | −0.029, 3/14 | |

Weather is the clearest single result in the study: not one of the 14
neighborhoods was better off without it, at any horizon.

**Drop:**

| group | h=1 | h=2 | h=4 | |
| --- | --- | --- | --- | --- |
| **add** COVID + RSV + covid wastewater | −0.031, 0/14 | −0.155, 0/14 | −0.159, 0/14 | harmful at a scale nothing else reaches |
| demographic node features | −0.000, 6/14 | −0.003, 4/14 | **+0.027, 14/14** | neutral near, harmful far |
| demographic edges | +0.003, 13/14 | +0.002, 9/14 | −0.001, 4/14 | neutral to mildly harmful |
| both demographic halves together | +0.001, 9/14 | −0.002, 5/14 | +0.008, 13/14 | |

The demographic block does no measurable work at h=1 or h=2 and is actively
harmful at h=4, where removing the 8 static columns improved **all 14**
neighborhoods. This is the third study to find nothing there; it should come out
of the default.

**Add, for h>=2:**

| group | h=1 | h=2 | h=4 | |
| --- | --- | --- | --- | --- |
| **add** flu wastewater | −0.017, 3/14 | +0.013, 11/14 | **+0.089, 14/14** | the largest positive effect in the study |
| **add** statewide vaccination | +0.000, 7/14 | +0.008, 13/14 | **+0.041, 14/14** | |

Both hurt or do nothing at one week and help substantially at four. Flu
wastewater at h=4 is worth more than the entire graph is at h=2.

> **The vaccination verdict is a reversal.** The three-seed study recorded it as
> "adding it hurts" at −0.017. That arm was differenced against a transit-era
> reference carrying three global covariates the current default does not have,
> so it was never measuring vaccination alone. Read the old row as void rather
> than as a contradicted finding.

> **Wastewater coverage is still asymmetric.** The series starts 2024-07-28, so
> it covers all of the test window and under half of training. That flatters it,
> and the h=4 figure should be read as an upper bound until the arm is re-run on
> a season where the coverage is even.

**Horizon-dependent, do not set a single default from these:**

| group | h=1 | h=2 | h=4 |
| --- | --- | --- | --- |
| **add** city-wide `ili_ed_perc` | −0.004, 4/14 | −0.006, 2/14 | +0.021, 14/14 |
| **add** calendar sin/cos | −0.001, 6/14 | −0.001, 8/14 | +0.025, 13/14 |
| the adaptive adjacency | −0.011, 0/14 | −0.007, 4/14 | +0.016, 14/14 |
| correlation edges | +0.000, 9/14 | −0.003, 3/14 | +0.028, 13/14 |
| the suppression flag | −0.002, 5/14 | +0.006, 12/14 | +0.002, 8/14 |

Each of these flips sign between h=1/2 and h=4, and the flip is consistent across
neighborhoods at both ends rather than being noise. `ili_ed_perc` staying out of
`DEFAULT_GLOBALS` is right for the horizons the project leads on and wrong for
h=4. An earlier version of this section said it "stays in `DEFAULT_GLOBALS`",
which the code has not matched for some time; `DEFAULT_GLOBALS` is `()`.

**What this adds up to.** As the horizon lengthens the model stops being able to
use structure and starts needing exogenous signal. At h=4 removing the graph, the
adaptive adjacency, the correlation edges or the demographic features all help or
do nothing, while every slow-moving external series added -- wastewater,
vaccination, city-wide ILI, even the calendar -- helps in 13 or 14 of 14
neighborhoods. Four weeks out there is little left in a neighborhood's own
recent history or its neighbors' for the graph to exploit.
### Attention: two different questions, two different answers

There are two GAT arms and conflating them is easy, so they are named apart.

**`gat` is the paper's baseline** — a standalone plain spatial Graph Attention
Network over ILI history with no temporal encoder, 52-week input, level target.
It is standalone in exactly the sense `dualtopo` is, because that is what Luo et
al. compare against. `Code/run_gat.py`, `models.GATBaseline`.

**`gnn_st_gat` is an ablation** — `gnn_st` with `GCNConv` swapped for `GATConv`
and everything else held fixed. It asks whether attention beats
degree-normalised averaging *given* a temporal stack, which is not the paper's
question.

> **`gnn_st_gat` has since been removed from `EXPERIMENTS`.** The numbers below
> are kept as the measurement of record — they are what retired the arm — but
> `Code/run_ablation.py` cannot regenerate them and the arm is not in the current
> ablation table. `gat`, the paper baseline, is still live.

| macro Corr | h=1 | h=2 | h=4 |
| --- | --- | --- | --- |
| `gat` (paper baseline, no temporal encoder) | 0.644 | 0.391 | 0.179 |
| `gnn_st_gat` (attention inside our architecture) | 0.902 | 0.799 | 0.603 |
| `gnn_st` (GCN inside our architecture) | 0.897 | 0.804 | 0.616 |

These three were measured on the transit-era graph before the V2 training
settings were promoted, so the `gnn_st` row here will not match the ablation
table above. The comparison between them is still like-for-like -- all three ran
in the same configuration as each other -- which is what the section's claims
rest on.

Two results, and the second only exists because the first is a separate model:

**The reimplementation is sound.** Luo et al. report GAT at **0.5994**; ours
scores **0.644** at the same horizon on a different city. Close enough to trust,
with the gap attributable to Boston's 14 neighborhoods against Taiwan's 19
counties.

**The temporal encoder is worth +0.258, and that is now measured rather than
argued.** The convolution is identical between `gat` and `gnn_st_gat`; the
difference is the dilated causal temporal stack and the blended target. So the
paper's GAT result is evidence about a missing temporal encoder, not evidence
against attention for this task -- consistent with this repository's own ablation
putting the temporal axis ahead of every graph detail.

**Attention itself does nothing.** `gnn_st_gat` against `gnn_st` differs by
0.005 to 0.013 at every horizon, inside the noise floor. That is the third
independent confirmation of one pattern: the adaptive adjacency, separate
per-relation gating and now attention are all substitutable, while removing
spatial mixing altogether costs 0.090. **Having a graph matters; how it is wired
does not.**

An earlier version of this section drew the +0.258 conclusion from the ablation
arm alone, without ever building the paper's model. That was an inference
presented as a measurement, and the standalone `gat` arm exists to make it one.

### Boosted trees are the baseline that was missing

`run_xgboost.py` fits one pooled model over all nodes -- node index as a feature,
rather than 14 models on 122 rows each -- over the same per-node columns the
graph model reads, with no edges. It predicts the residual from the train-only
harmonic climatology, because trees cannot extrapolate past their training range
and would otherwise produce a flat-topped forecast in any season higher than the
training maximum.

It is the strongest non-graph baseline at four weeks by a wide margin (0.595
against the LSTM's 0.440) and it is what turns the h=4 result from a win into a
tie. Adding it was the single largest correction to the leaderboard's story.

### Two cities

Moved, and extended to three cities and three horizons: see [Cities](#cities).

### Which edges earn their place

The feature arms ask what the node inputs are worth. These ask what the *wiring*
is worth, which is the question the repository was set up to answer. Ten seeds,
one code version; floors 0.003 / 0.006 / 0.031 at h=1/2/4; `n/14` is how many
neighborhoods the arm improved.

| change | h=1 Δ | h=2 Δ | h=4 Δ |
| --- | --- | --- | --- |
| no spatial term at all (self-loops only) | **−0.075**, 0/14 | **−0.093**, 0/14 | −0.009, 6/14 |
| no hand-built edges, learned adjacency kept | +0.006, 11/14 | −0.006, 3/14 | +0.006, 9/14 |
| correlation edges removed (39 pairs) | +0.000, 9/14 | −0.003, 3/14 | +0.028, 13/14 |
| geographic edges only (drop corr, demo) | +0.001, 9/14 | −0.004, 2/14 | −0.009, 0/14 |
| demographic edges removed (60 pairs) | +0.003, 13/14 | +0.002, 9/14 | −0.001, 4/14 |

**The graph is worth 0.093 macro Corr at h=2 — fifteen times the floor, and not
one of the 14 neighborhoods was better off without it.** At h=1 it is worth
0.075 on the same unanimous evidence. That is the affirmative answer to the
question in the README, and the margin over the baselines decomposes:

| | macro at h=2 | attributable to |
| --- | --- | --- |
| `persistence` | 0.618 | — |
| `lstm` | 0.684 | +0.066, modelling all 14 series jointly |
| temporal architecture, no graph | 0.709 | +0.025, the temporal conv and the blended target |
| **+ graph** | **0.802** | **+0.093, spatial mixing** |

**At four weeks the graph stops paying, and that is a limit of the result rather
than a detail.** `gnn_st_nograph` costs 0.009 at h=4 against a floor of 0.031,
and the neighborhoods split 6 against 8 — the one place in this study where the
paired test agrees with the floor that there is nothing to see (p=0.46). Removing
the correlation edges at h=4 *improves* 13 of 14 neighborhoods. So the honest
statement is that spatial mixing is what makes this a graph problem at one and
two weeks, and by four weeks the graph is carrying approximately nothing. Any
claim that the graph is what wins at long horizons is not supported here.

**And hand-engineering the graph is close to worthless at every horizon.** No
hand-built edge type clears its floor anywhere: dropping all of them for the
learned adaptive adjacency alone is +0.006 / −0.006 / +0.006. Geography alone
recovers essentially everything the full five-type graph achieves. **Having**
spatial mixing matters enormously at h<=2 while **how it is wired** does not
matter at all — consistent with the design ablations, where the multi-relational
option and separate per-relation gating were also inside noise.

> The previous version of this table read 0.090 for the graph at h=2 and was
> quoted as "six times the noise floor". The number barely moved, but it had been
> measured across a boundary: the graph arms were fit on the current 107-edge
> graph while the reference they were differenced against was transit-era and
> carried three global covariates. It is now a like-for-like measurement, and the
> floor it is compared against is measured rather than inferred.

#### Transit (retired)

MBTA transit edges were removed from the project in September 2026 and
`Data/MBTA/` was deleted. The measurement that settled it, at ten seeds with
both arms trained in the same batch on the same hardware so that thread-order
effects could not be mistaken for a result, is preserved at
`Code/results/_ablation/transit_retirement/` -- `gnn_st_transit` is gone from
`EXPERIMENTS`, so this table cannot be regenerated by any current code path:

| weeks ahead | macro without MBTA | macro with MBTA | Δ macro | Δ RMSE |
| --- | --- | --- | --- | --- |
| 1 | 0.893 | 0.892 | −0.001 | +0.14 |
| 2 | 0.802 | 0.795 | −0.007 | +0.24 |
| 4 | 0.582 | 0.597 | **+0.015** | −0.27 |

Three reasons that gain at four weeks is not a finding:

1. **The sign flips across horizons** — worse at one and two weeks, better at
   four. A real mechanism does not reverse direction.
2. **It flips against the previous ten-seed measurement too**, which recorded
   −0.018 at h=4. A 0.033 swing between two nominally identical measurements puts
   the h=4 uncertainty above the size of the effect; the per-seed spread there is
   about 0.05.
3. **There is almost nothing for it to add.** The 32 MBTA pairs take the graph
   from 107 to **108** undirected edges. Thirty-one of them reweight connections
   the hand-coded border graph already carries, and the one genuinely new pair —
   Back Bay+ ↔ Hyde Park — has weight 0.000. Transit could only be informative
   where it links *distant* neighborhoods, and that is exactly where its weight
   vanishes. This is a fact about Boston's transit geometry rather than a defect
   in the scrape.

Results committed before the removal still record `"transit": true`, including
two arms sitting in the headline `horizon_0N/` directories next to a reference
that does not. `Code/results/TRANSIT_ERA_RUNS.md` lists them and says which
comparisons are therefore not like-for-like.

The cost of the null is worth recording: `Data/MBTA/` was 102 MB of GTFS, about
30% of the repository, reduced to a 2 KB matrix. A COTA equivalent for Columbus
should be weighed against this result before it is built.

#### Two caveats

- The edge types are **summed** into one adjacency, so removing one lets the
  others compensate. Every single-type row above is therefore a marginal
  contribution *given the others*, not a standalone value.
- `gnn_st_nograph` drops the seven anchor nodes along with the edges, since
  anchors are meaningless without them. The 0.090 therefore bundles spatial
  mixing with the boundary nodes; an arm with edges but no anchors would separate
  the two, and `anchors="single"` already exists for it.

### Design choices

Ten seeds, floors 0.003 / 0.006 / 0.031, `n/14` neighborhoods improved.

| change | h=1 Δ | h=2 Δ | h=4 Δ |
| --- | --- | --- | --- |
| level target — no baseline at all | −0.000, 7/14 | **−0.059**, 2/14 | −0.029, 3/14 |
| blend target → delta (origin level only) | −0.010, 0/14 | **−0.019**, 1/14 | **−0.096**, 0/14 |
| edge types kept separate instead of summed | +0.000, 9/14 | **−0.011**, 0/14 | −0.004, 5/14 |
| adaptive adjacency removed | **−0.011**, 0/14 | −0.007, 4/14 | +0.016, 14/14 |
| channels 24 → 16 | −0.005, 3/14 | −0.007, 2/14 | −0.003, 6/14 |
| soft-Pearson loss term removed | −0.001, 3/14 | −0.006, 1/14 | +0.007, 11/14 |

**Predicting a residual from *some* baseline is still the design choice that
matters most**, and at h=4 it is the largest single effect in the whole study:
dropping the learned blend for a plain delta target costs 0.096 macro and makes
every one of the 14 neighborhoods worse.

**The rest of the design column is no longer uniformly "inside noise", and that
is a consequence of measuring the floor rather than assuming it.** Against the
measured 0.006 at h=2, summing the edge types beats gating them separately
(−0.011, 0/14), the soft-Pearson term earns its place (−0.006, 1/14), and 24
channels beat 16 (−0.007, 2/14). Each was reported as inside noise when the
threshold was the per-seed 0.015. None of them is large, but each moves almost
every neighborhood the same way, which noise does not do.

**The adaptive adjacency reverses with horizon.** It earns its place at h=1
(−0.011, 0/14) and is worth little at h=2, but at h=4 removing it *improves all
14 neighborhoods* (+0.016). Read together with the graph table, where h=4 also
prefers no correlation edges and is indifferent to having a graph at all, the
pattern is that learned spatial structure is useful exactly as far ahead as
spatial structure is informative, and past that it is a source of variance.

### The blend target at horizon 4

Measured where its justification lies, ten seeds:

| target | macro | pooled | RMSE |
| --- | --- | --- | --- |
| blend (learned mix) | **0.582** | **0.676** | **23.07** |
| delta (origin level only) | 0.486 | 0.590 | 26.85 |
| Δ | −0.096 | −0.086 | +3.78 |

**−0.096 macro is 3× the measured horizon-4 floor and unanimous across
neighborhoods, so this one is not in doubt.** Set beside −0.019 at h=2 and
−0.010 at h=1, the choice does a little where the theory says it should do little
and a great deal where it says it should: the origin level carries 0.271
correlation with the target four weeks out while the climatology holds 0.697, and
the learned weight moves from 0.629 to 0.457 across exactly that range.

An ablation grid run only at short horizons would have called this component
nearly worthless. That is a reason to keep a long horizon in the grid, not a
reason to trust the short-horizon rows less.
and moved all three down:

| horizon | learned weight on the origin level |
| --- | --- |
| 1 | 0.873 |
| 2 | 0.629 |
| 4 | 0.457 |

That is the same shape as the measured autocorrelations — 0.906, 0.695, 0.271,
against a climatology flat at 0.697 — recovered from the training data alone. An
interpretable parameter landing where the measurements independently say it
should is a result; it is not by itself evidence that the blend beats a fixed
anchor, which is a separate question answered by the table above.

## Cities

The same code path runs three cities. Everything that differs between them
lives on one `City` object (`Code/influenza/cities/`), and every entry point
takes `--city boston|columbus|buenos_aires`.

### What differs, city by city

| | Boston | Columbus OH | Buenos Aires (AMBA) |
|---|---|---|---|
| scored nodes | 14 neighborhoods | 17 CPH areas | 19 partidos |
| anchors | 7, hand-designed | 5, the crosswalk's unassigned fringe ZIPs | 5, partidos below 90% reporting coverage |
| geo edges | hand-coded (23) | hand-coded, checked against ZCTA polygons | **derived** from IGN polygons (48), read at import |
| source | published rate per 100,000 | line-level ED visits / ACS population | SNVS ETI counts / INDEC population |
| small counts | suppressed → NaN | observed zero | isolated gap → 0, blackout of ≥3 weeks → NaN |
| flu season | Oct–Mar | Oct–Mar | **Apr–Sep** |
| season boundary | August | August | **February** |
| test window | 2025-05-31 → 2026-05-31 | same | **2024-11-03 → 2025-11-02** |
| demographic columns | 8 (BPDA tables) | 8 (ACS 5-year, ZCTA) | **5** (INDEC 2022 per-partido) |
| variants | exclude_covid, post_covid, full | post_covid | post_covid |
| notes | [DATA_NOTES](DATA_NOTES.md) | [COLUMBUS_DATA_NOTES](COLUMBUS_DATA_NOTES.md) | [AMBA_DATA_NOTES](AMBA_DATA_NOTES.md) |

Per-city data provenance, column by column, is in
[DATA_NOTES § Three cities](DATA_NOTES.md#three-cities-side-by-side).

**Season geometry is per-city.** `City.flu_months` drives the flu/off-season
segments (`metrics.segment_labels`) and the chart shading
(`plots._flu_season_spans`); `City.season_start_month` names seasons for the
MEM severity thresholds (`severity.season_label`). Both default to Boston's
values, so every existing call is unchanged. Buenos Aires peaks in epiweeks
20–23 every year, so without this its whole epidemic would have been scored as
"off-season". `climatology.py` needed no change — its day-of-year harmonic fit
is phase-free.

**Evaluation windows are shared unless a city cannot use the shared one.**
`City.test_start`/`test_end` override it, and `cli.resolve_window` applies them
with precedence CLI > city > shared default. Only Buenos Aires overrides: its
surveillance backfills for ~4 months, so its last fully reported week is
2025-11-02. Its window is a full year ending there, covering the 2025 season
peak with 148 training weeks before it. **Buenos Aires numbers are therefore
not on the same weeks as Boston's and Columbus's**; compare margins over
baselines within a city, not raw errors across cities.

**Demographic columns are per-city.** `STATIC_DEMO_COLS` stays eight wide for
Boston and Columbus. Buenos Aires's loader returns the five it has, by name,
and `samples._feature_names` labels the static block from what the loader
returned, so `gnn_st` runs there with 43 node features against Boston's 46.
Shrinking the shared list to the intersection was considered and rejected: it
would have invalidated every Boston and Columbus checkpoint to align a column
set the cities can never fully share.

**Unavailable inputs fail at argument-parse time.**
`cli.check_experiment_supported` compares an experiment's FeatureSpec with
`City.available_features` and `available_globals` before any data is loaded,
and names the arms that do run. Previously the error surfaced three loaders
deep.

### Orchestration had no city axis

This, not neglect, is why Columbus lagged Boston:

* `run_all_horizons.py` had no `--city`, so its 3-horizon matrix could only
  produce Boston.
* `sweep.py` had `--cities`, but `Task.output_dir()` omitted `paths.city_root()`,
  so `--cities columbus` wrote into **Boston's** `results/horizon_*/`, silently
  overwriting it. Fixed for results and checkpoints.
* `compare_horizons`, `compare_severity`, `plot_forecasts`,
  `run_rt_diagnostics`, `run_ablation` and `run_backtest` took no `--city`;
  `compare_models --city` only relabelled rows and `compare_timing --city` only
  validated the spelling. All now route through `cli.add_city_arg` and
  `cli.city_results_dir`: `--city` sets the default results root, an explicit
  `--results-dir` still wins.

Boston output is byte-identical before and after (every CSV and PNG from
`compare_models`, `compare_severity` and `plot_forecasts` at h=2 was diffed
against the pre-change working tree).

### Results, three horizons

Macro correlation and macro RMSE (per-node metrics, then averaged — the
comparable columns across cities; see the pooled-Corr warning below), overall
segment, `post_covid`, one run per arm from the Explorer sweeps:

| macro Corr | Boston h1 | h2 | h4 | Columbus h1 | h2 | h4 |
|---|---|---|---|---|---|---|
| `gnn_st` | **0.892** | **0.801** | 0.582 | **0.821** | **0.749** | 0.658 |
| `xgboost` | 0.821 | 0.675 | **0.608** | 0.736 | 0.666 | **0.726** |
| `lstm` | 0.867 | 0.684 | 0.440 | 0.770 | 0.644 | 0.449 |
| `arima` | 0.788 | 0.625 | 0.254 | 0.698 | 0.566 | 0.399 |
| `persistence` | 0.798 | 0.618 | 0.224 | 0.737 | 0.597 | 0.390 |
| `seasonal_naive` | 0.296 | 0.296 | 0.296 | 0.561 | 0.561 | 0.561 |
| `gat` | 0.644 | 0.390 | 0.179 | 0.675 | 0.705 | 0.486 |
| `dualtopo` | 0.426 | −0.334 | 0.513 | 0.656 | 0.659 | 0.704 |

| macro RMSE | Boston h1 | h2 | h4 | Columbus h1 | h2 | h4 |
|---|---|---|---|---|---|---|
| `gnn_st` | **10.24** | **14.49** | **19.63** | **6.56** | **7.73** | 9.03 |
| `xgboost` | 13.72 | 17.76 | 19.81 | 8.62 | 9.36 | **8.68** |
| `lstm` | 12.33 | 17.94 | 22.41 | 7.91 | 9.44 | 11.17 |
| `arima` | 13.87 | 18.63 | 24.45 | 8.46 | 10.12 | 11.16 |
| `persistence` | 14.12 | 20.61 | 29.93 | 8.28 | 10.37 | 13.09 |
| `seasonal_naive` | 33.71 | 33.71 | 33.71 | 14.29 | 14.29 | 14.29 |
| `gat` | 18.87 | 23.12 | 26.96 | 9.07 | 9.05 | 13.62 |
| `dualtopo` | 24.36 | 24.51 | 24.58 | 12.72 | 12.55 | 9.04 |

Regenerate with `compare_models.py --city <c> --results-dir <root>/horizon_0N
--horizon N --scope macro`.

**What reproduces.** At one and two weeks `gnn_st` wins in both cities on both
metrics, by clear margins over the best baseline.

**What does not.** At four weeks the graph model's lead over boosted trees is
gone: tied in Boston, behind in Columbus. [SHAP](#interpretability) shows why —
by h=4 `gnn_st` has fallen back almost entirely on its climatology term, which
is the same seasonal curve `xgboost` is built around. This is the horizon the
project's win condition is weakest at.

**Baseline ordering is city-specific.** `gat` sits below persistence in Boston
and above `xgboost` and `lstm` in Columbus at h=2. Any ranking of baselines
fitted in one city is fragile, including the one in Luo et al.

**`dualtopo` is not a working model here.** Its Boston h=2 macro Corr is
negative. SHAP independently shows its predictions are a per-node constant
(standard deviation 0.03 per 100,000 across 53 test weeks for Dorchester).

**Do not compare pooled Corr across cities.** Columbus has a 10.9x spread in
area mean rates against Boston's 7.3x, so pooled Corr collects more free credit
there for knowing which areas are busy.

**Do not read MAPE for Columbus.** MAPE divides by the observed rate, and
Columbus reports observed zeros and near-zeros rather than suppressing small
counts; pooled MAPE reaches the millions of percent. `compare_models` now
prints a warning into the leaderboard when MAPE exceeds 1,000%. The column is
kept so the cities' tables share a shape. Rank Columbus on RMSE or MAE.

**Buenos Aires** runs the same matrix (`sweep/tasks_buenos_aires*.jsonl`), plus
the ablation pair `gnn_st_nodemo` / `xgboost_nodemo` that ran before its
demographics were built. Results land in `results/buenos_aires/`; add them here
once pulled.

Earlier, from a 10-seed h=2 comparison: the leaner `gnn_st_minimal` (no
demographics, no city-wide covariate) was the top arm in Columbus and within
noise of `gnn_st` in Boston — the same direction the Boston ablations point.

### Where the per-city artifacts are

```
results/horizon_0N/                 Boston (historical top-level layout)
results/columbus/horizon_0N/        Columbus
results/buenos_aires/horizon_0N/    Buenos Aires
   <model>/post_covid/              metrics, predictions, run_config, grid plot,
                                    shap/ (waterfall + importance)
   _comparison/                     leaderboard, per-neighborhood leaderboard,
                                    severity and timing tables and figures
results/<city>/_comparison_horizons/  error growth across horizons
```

Data-layer checks run before any training:
`run_columbus_data_check.py` and `run_buenos_aires_data_check.py --strict`
(41 assertions, including "July is colder than January" as a hemisphere check).

---

## Honest limitations

- **Every result predating August 2026 is void.** Two data-loading defects — an
  ILI count row averaged with the rate row, and suppressed weeks imputed as zero
  — affected all eight notebooks and both baselines. See
  [`Code/docs/DATA_NOTES.md`](../../Code/docs/DATA_NOTES.md). The old numbers are kept
  in `Code/results/_legacy_pre_refactor/` for the record and are excluded from
  the leaderboard.
- **Normalisation was leaking.** The notebooks computed normalisation statistics
  over the whole series, test window included, while the LSTM used training rows
  only. `normalize='train'` is now the default; `run_config.json` records which
  was used and `compare_models.py` warns when a table mixes them.

  The *size* of the effect, however, does not replicate. An earlier
  two-horizon-head run put a leak-normalised arm at 18.55 against 24.54
  leak-free, suggesting the leak supplied about a third of the graph models'
  apparent quality. Re-run as single-horizon models across six horizons, the sign
  flipped repeatedly — the leak cost 12.9 RMSE at one week, gained 1.3 at two,
  cost 6.3 at four, gained 1.9 at fifty-two. On one test season the leak effect is
  not separable from seed and configuration noise, so treat 'a third of the quality'
  as unsupported. Leak-free normalisation is still the right default; the case
  for it is methodological, not empirical.
- **One seed.** Section 11 of the notes puts the noise floor at 0.2–0.5 MAE.
  Differences smaller than that mean nothing, which includes the Rt result.
- **Three post-COVID seasons.** 201 weeks, 121 training origins at an 8-week
  lookback. This is a small-data problem and behaves like one.
- **Citywide covariates run out mid-evaluation.** The ED file ends 2026-01-04 and
  the demographics file 2025-12-07; the last 17 and 21 weeks are carried forward,
  and the loaders say so on every run.
- **Rt is a growth index, not a reproduction number** — computed from an
  interpolated weekly rate. See [`Code/docs/RT_CAVEATS.md`](../../Code/docs/RT_CAVEATS.md).
- **`dualtopo` is scored on 627 cells, not 614**, because a horizon-1-only model
  keeps one extra origin. `compare_models.py` flags this; it is about 2%.
- **COVID and RSV neighborhood data is monthly**, held flat across weeks. The
  resolution mismatch is why those features default to off despite helping.

---

## Forecast horizons

One week ahead is not a hard question. Next week's ILI is almost this week's, so
every model lands close to persistence and the margins are small — that is a
fact about the task, not about the models. The sweep therefore runs each model at
**1, 2 and 4 weeks ahead**, one results tree per horizon:

```bash
python Code/run_all_horizons.py --horizons 1,2,4 --dry-run   # check geometry
python Code/run_all_horizons.py --horizons 1,2,4             # ~1 h
python Code/compare_horizons.py                              # the reports
```

Horizons 12, 24 and 52 were swept earlier and have been retired. They were never
answering a forecasting question: at a quarter-cycle or more the lookback carries
no information about where in the season the target sits, so the arms that won
there won by *predicting the climatology*, which is what `seasonal_naive`
already does for free. Four weeks is the edge of where neighborhood-level ILI
history still constrains the answer.

Each horizon is a separate *direct* model — one trained per horizon, never a
recursive roll-forward. Recursion is not available here: the models consume
weather and city-wide ED counts at the origin week, so stepping a prediction
forward would need forecasts of four other series first.

Results land in `Code/results/horizon_02/<model>/<variant>/`, which keeps
`metrics.csv` two levels below the root, so `compare_models.py --results-dir
Code/results/horizon_02` produces a full per-horizon leaderboard with no other
changes. Cross-horizon output goes to `Code/results/_comparison_horizons/`:
`error_growth.png`, `skill_vs_seasonal.png`, `error_growth_facets.png`,
`horizon_matrix.csv` and `leaderboard_horizons.md`.

**Every horizon scores exactly the same 49 target weeks** (2025-06-01 →
2026-05-03), because test membership is decided by target date rather than by
origin. That is what makes an error-growth curve a comparison of difficulty
rather than of evaluation sets, and `--dry-run` asserts it before anything
trains.

Three things worth knowing before reading the numbers:

- **`seasonal_naive` is a flat line across horizons.** Its effective lag is
  `max(52, h)`, so its prediction depends only on the target date — and the
  target dates never change. Its RMSE is 39.84 at every horizon in the table
  above; if it is not flat, the split is wrong.
- **`gnn_st`'s target is a residual from a learned persistence/climatology
  blend**, not from the origin level alone. The origin level is the right frame
  at 1 week and progressively worse as the horizon grows, which is exactly what
  the learned blend weight absorbs — see
  [The learned blend weight](#the-learned-blend-weight). The `gnn_st_delta` arm
  measures what the blend is worth against the origin-only parameterisation.

### The calendar feature

An 8-week lookback says nothing about where in the season a target 6 months out
sits — the model cannot tell a rising November from a falling February.
`FeatureSpec.use_seasonality` (default off, `--seasonality` on `run_gnn.py`) adds
sine and cosine of the **target** week's position in the year to the city-wide
covariates. That is not leakage: when you sit down in June to forecast January,
you already know it is January.

It rides with the globals rather than the node features deliberately — as a node
feature it would be identical across all 21 nodes, and the GCN's degree-normalised
averaging cannot differentiate a constant. `gnn_st_season` turns it on and
`gnn_st_noseason` turns it off relative to whatever the default is.

**Measured, it earns much less than expected.** The leave-one-out ablation puts
`gnn_st_noseason` at +0.001 macro Corr — removing the calendar changes nothing,
inside a ±0.015 noise floor. The reason is that the model already had a calendar:
mean temperature correlates with week-of-year at **R² = 0.93**, so the six
weather columns were an implicit seasonal clock all along. At the horizons this
project now reports, sin/cos is redundant with weather and the harmonic
climatology the target already subtracts.

## Interpretability

**Ablations are the headline method; `run_shap.py` is a narrow complement.**
The original attribution stack -- `run_importance.py`, `influenza/importance.py`
and `influenza/shapley.py` -- was removed along with the
`gcn_fusion` arms it was written against: every predictor wrapper reached into
`InfluenzaGNN` by attribute name, and porting them to `SpatioTemporalGNN` would
have rebuilt a method that could not answer the questions that actually matter
here.

The reason is in the numbers that path produced. SHAP used `GradientExplainer`
(expected gradients), which computes `φ ≈ (x − x′) · E[∂f/∂x]`. Static
demographics and anchor-node columns are identical for every forecast origin, so
`x − x′ = 0` and **those groups got exactly zero by construction** — which means
"this experiment cannot measure them", not "the model ignores them". Half the
feature groups in this project are of that kind.

[Ablations](#ablations) answer the same question by removing a group and
**retraining**, which works for static and time-varying inputs alike and lets the
model compensate for what is gone. That is the stronger question — "can it do as
well without this?" rather than "how much does it currently lean on this?" — and
it is reported against a measured per-seed noise floor, so a 0.005 difference
cannot be read as a finding. `run_ablation.py` is the interpretability story for
this repository.

What was lost with the SHAP path is genuine but narrow: per-week,
per-neighborhood attribution for a *single* forecast (the waterfall plots), which
a retrain ablation cannot produce.

### `run_shap.py` — the per-week complement

That gap is now filled by `Code/run_shap.py`, rebuilt against
`SpatioTemporalGNN` rather than restored from git. It produces one waterfall for
one node in one week — by default the observed citywide peak inside the test
window — and nothing else.

It is **not** the old implementation with a new explainer. Two things changed.

**The game is collapsed to ~7 group players** — own flu history, own weather,
own demographics, neighbours' flu history, neighbours' other inputs, the
persistence anchor and the climatology baseline — and
`shap.explainers.ExactExplainer` enumerates all `2^G` coalitions. The values are
therefore exact Shapley values *of the group game*, not a sum of per-column
attributions aggregated afterwards, and `base + Σφ = prediction` is asserted at
runtime rather than claimed. `GradientExplainer` was not an option regardless of
the degeneracy below: the adaptive relation is built from two `(n_nodes,
adaptive_dim)` parameters indexed by node id (`models.py:287-297`), so the old
block-diagonal batching wrapper would index the wrong rows for every replica
past the first.

**The `x − x′ = 0` degeneracy is fixed in the background, not the explainer.**
A background draw is one random training origin with its scored-node rows
*permuted*. Demographics are constant across origins but differ across nodes, so
permuting nodes makes them vary and therefore measurable. The script prints the
largest demographic spread it found and refuses to run if it is zero, so the
defect cannot silently return. Measured on Boston h=2: own demographics score
+0.15 per 100,000 at the 2025-12-21 peak — small, which is consistent with the
[ablations](#ablations), but *measured* small rather than zero by construction.

Anchor nodes still get no group, and that is now the correct answer rather than a
limitation: `samples.py:239-246` fills every anchor row at every origin with one
constant vector, so they carry no information for any method to attribute.

What it does not answer: it explains the mean-weight forward of a single seed
under `model.eval()`, not the MC-Dropout ensemble behind the published
intervals, so its point forecast differs from `predictions.csv`. And it is a
local attribution — "what did the trained model lean on here", not "could it do
as well without this". The second question is the ablation's, and the ablation
is still the stronger one.

### Which models it covers

| model | method | groups |
|---|---|---|
| `gnn_st` and other `stgnn` arms | exact coalition enumeration, `ExactExplainer` | own flu history, own weather, own demographics, neighbours' flu history, neighbours' other inputs, persistence anchor, climatology |
| `gat`, `dualtopo` | same | own and neighbours' flu history only — these models read ILI lags and nothing else |
| `lstm` | same | own and neighbours' flu history. One multivariate model over all nodes, so neighbours are input columns, not graph neighbours |
| `xgboost` | `shap.TreeExplainer`, exact and instant | own flu history, weather, demographics, node identity, climatology. No neighbour groups: it has no edges |
| `persistence`, `seasonal_naive`, `arima` | not applicable | no features to attribute; ARIMA's `selected_orders.csv` is its attribution |

One masking loop serves all four torch families: `make_predict` takes a
model-agnostic `forward(X, g, anchor, clim)`, and each family's adapter handles
its own tensor layout at the boundary (the LSTM is node-minor and oldest-first;
`dualtopo` wants `(batch, 1, nodes, time)`). Every family's reconstructed
prediction was checked against its own `predictions.csv` — the LSTM and
XGBoost reproduce to six decimals.

`guard()` checks only the provenance each checkpoint actually recorded:
`run_gnn.py` stores feature and global names and the edge index, `run_gat.py`
the edge index only, `run_dualtopo.py` dense adjacencies, `run_lstm.py`
neither. It prints what it could not verify rather than refusing a family over
a key its writer never wrote. `run_xgboost.py` now saves its booster
(`checkpoints/.../xgboost_<variant>_hNN.json` plus a `.meta.json`); it used to
fit, predict and discard it.

### Global importance: `--importance`

`run_shap.py --importance` writes `shap_importance.{png,csv}`: the mean
**absolute** contribution of each group over many node-weeks, with the mean
**signed** contribution drawn over it. Both are reported because they
disagree in a way that matters — a group that pushes some forecasts up and
others down by the same amount is influential but has no consistent direction.

The node-weeks are every scored node at `--importance-weeks` (default 12) weeks
spread **evenly** across the test year, with the observed peak forced in. Not
random: a random sample of a mostly off-season year is mostly off-season, where
every model reduces to "near zero again" and no input drives anything.

Cost is dominated by `gnn_st`: 2^7 coalitions × background draws × node-weeks,
about 35 minutes per horizon at the defaults. The tree path is one vectorised
call.

### What the waterfalls say, Boston, 2025-12-21 peak, Dorchester

Contributions in ILI visits per 100,000 (observed 256.1):

| | `gnn_st` h1 | h2 | h4 | `xgboost` h1 | h2 | h4 |
|---|---|---|---|---|---|---|
| neighbours' flu history | +71.4 | +37.3 | −15.9 | — | — | — |
| persistence anchor | +103.8 | +31.4 | −6.3 | — | — | — |
| climatology | +7.4 | +15.1 | +31.1 | +84.2 | +84.2 | +86.8 |
| own flu history | −27.5 | −10.8 | −0.6 | +37.7 | −2.5 | −20.8 |
| own demographics | +0.0 | +0.1 | −0.3 | +16.1 | +3.5 | −1.9 |
| **predicted** | 226.2 | 146.7 | 82.4 | 158.8 | 108.0 | 84.0 |

**The graph model degrades in a readable order.** At one week it is mostly
"where Dorchester is now" (the anchor). At two weeks neighbours overtake the
anchor. At four weeks every local term is negative and climatology is the only
thing pushing up — the model has fallen back on the seasonal curve, which is
why its lead over `xgboost` vanishes there (see [Cities](#cities)).

**`xgboost` collapses onto climatology at the peak.** Own flu history
contributes −2.5 at the peak against −16.6 in an off-season week and −30.2 on
the rising limb. The peak residual is outside what the trees saw in training, so
they saturate and the forecast lands on the baseline.

**"Demographics do nothing" is a `gnn_st` result, not a universal one.** For
the pooled tree model own demographics are +16.1 at h=1: with one model across
all nodes they act as a node-identity proxy. The graph model does not need them
for that, because per-node normalisation and the adaptive adjacency already
carry identity — consistent with `gnn_st_nodemofeat` sitting inside noise in
the [ablations](#ablations).

**`dualtopo` attributes ~0 to everything** because its forecasts do not vary in
time (see [Cities](#cities)). The attribution was right; the model was
degenerate.

A negative own-flu-history term for `gnn_st` at the peak is real, not a masking
bug: a direct leave-one-out gives the same sign (−6.9), and it turns positive
in an off-season week. With the anchor already carrying "Dorchester is at
109.7", the 16-week shape — two flat months before the surge — reads as less
explosive than a typical training node-week.

## Layout

```
Code/
├── influenza/         shared library: data, windows, graphs, samples, models,
│                      training, metrics, intervals, plots, palette, carbon, rt
│   ├── cities/        one City profile per city: boston, columbus, buenos_aires
│   └── loaders/       per-city data access (Boston's is influenza/data.py)
├── run_*.py           one entry point per model family; all take --city
├── run_all_horizons.py   sweep all eight arms at horizons 1, 2 and 4, per city
├── run_ablation.py       leave-one-out ablations of gnn_st vs the noise floor
├── run_shap.py           group-Shapley waterfall for one node-week, or
│                         --importance over many; all five model families
├── run_columbus_data_check.py, run_buenos_aires_data_check.py
├── compare_models.py  leaderboard across everything in a results tree
├── compare_horizons.py   error growth and skill-vs-floor across horizons
├── compare_severity.py, compare_timing.py
├── plot_forecasts.py  overlay forecasts + 95% intervals on the observed series
├── run_rt_diagnostics.py
├── sweep.py, sweep/   Explorer job-array task lists and sbatch script
├── checkpoints/       [<city>/]horizon_NN/, ablation/hNN/, xgboost boosters
├── results/           [<city>/]horizon_NN/<model>/<variant>/  one tree per
│                      horizon per city, with {predictions,metrics}.csv,
│                      run_config.json, plots and shap/
│                      [<city>/]_comparison_horizons/  error growth
│                      _ablation/hNN_sS/              ablation arms
├── notebooks/         frozen; superseded by the scripts
├── scrapers/          weather, ACS, INDEC, adjacency and panel builders
└── docs/              METHODS.md, DATA_NOTES.md, COLUMBUS_DATA_NOTES.md,
                       AMBA_DATA_NOTES.md, SEVERITY.md, RT_CAVEATS.md,
                       METRICS_PLAIN.md, EDGES_AND_NODES_NOTES.txt
Data/                  BPHC, Columbus Public Health and SNVS surveillance,
                       weather per city, census tables, MA vaccination
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
