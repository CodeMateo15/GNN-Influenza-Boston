# Severity — what the bands mean, and what they can and cannot tell you

`influenza/severity.py` turns a weekly ILI ED visit rate into one of four
severity bands, following CDC's
[in-season severity assessment](https://www.cdc.gov/flu-burden/php/surveillance/in-season-severity.html).
`compare_severity.py` then asks of every model on disk: **did the forecast say
the week would be bad, and did it say so in time?**

**If you only want to know what POD, FAR, CSI, PSS and BSS mean, read
[`METRICS_PLAIN.md`](METRICS_PLAIN.md) instead** — it is the same material with
worked examples and no method.

That is a different question from the one `compare_models.py` answers. RMSE tells
you how close the number was. It does not tell you whether the model would have
triggered an alert in the week that mattered, and a model can be good at one and
bad at the other. Section 8 shows this happening.

Everything below is measured on the 2025-26 season, one seed, horizon 1 unless
stated. Read section 9 before quoting any of it.

## 1. The method, exactly

CDC compares each week's indicator value against **intensity thresholds** built
from previous seasons by the Moving Epidemic Method (MEM), and bands the result:

| band | condition |
| --- | --- |
| low | below IT50 |
| moderate | IT50 to IT90 |
| high | IT90 to IT98 |
| very high | at or above IT98 |

The recipe implemented in `mem_intensity_thresholds()` is the one in the
[`mem` R package](https://github.com/lozalojo/mem) under its own defaults
(`i.type.intensity=6`, `i.tails.intensity=1`, `i.n.max=-1`):

1. A season runs August to July.
2. Take the `values_per_season` highest weekly values of each reference season
   and pool them. MEM's rule is `max(1, round(30 / n_seasons))`, which holds the
   pooled sample near 30 however many seasons are available.
3. Work in logs: `mu = mean(log x)`, `sd = sd(log x)` with `ddof=1`.
4. The threshold at level `p` is the one-sided upper limit

   ```
   IT_p = exp(mu + k_p * sd),    k_p = qt(p, m-1) * sqrt(1 + 1/m)
   ```

CDC uses levels 0.50 / 0.90 / 0.98. MEM's own default is 0.40 / 0.90 / 0.975;
pass `--levels 0.40,0.90,0.975` for that.

### Two details that are easy to get wrong

**It is `sd`, not `sd / sqrt(m)`.** mem's `iconfianza.logx` builds an interval
for a *future observation*, not a confidence interval for the mean. The
`sd / sqrt(m)` form is a different function in the same package
(`iconfianza.geometrica`, reached with `i.type.intensity=2`) and it gives far
tighter thresholds. Published MEM figures use the wider one. Note that the
literature often calls these "confidence intervals"; "prediction interval" is
the accurate term, and the distinction is the whole difference between the two
functions.

**IT50 is exactly the geometric mean.** `qt(0.50, df)` is 0, so the 50th
percentile threshold reduces to `exp(mu)`. The output confirms this: the
`geometric_mean` and the IT50 column of `severity_thresholds.csv` are identical
to every decimal place. It is the cheapest check that an implementation is right.

## 2. Reference seasons: the choice that moves the thresholds most

**Which seasons feed the thresholds matters more than any other setting here.**
The default is `post_covid` — the three complete seasons since the disruption.
The same citywide indicator, three ways:

| `--reference-seasons` | seasons | values each | pooled | IT50 | IT90 | IT98 |
| --- | --- | --- | --- | --- | --- | --- |
| `post_covid` (default) | 3 | 10 | 30 | 60.2 | 98.2 | 134.2 |
| `exclude_covid` | 5 | 6 | 30 | 71.3 | 108.9 | 142.7 |
| `all` | 8 | 4 | 32 | 58.9 | 150.4 | 273.2 |

`all` is available and is a bad idea. The 2020-21 season peaked citywide at
**12.6 per 100,000 against a normal of roughly 100**, because non-pharmaceutical
interventions suppressed influenza almost entirely. Including it takes the
citywide log-SD from 0.37 to 0.71 — near enough double — which barely moves IT50
but pushes IT90 and IT98 so high that the upper bands become unreachable.
Measured per neighborhood over the whole 2025-26 season, the bands come out
579 low / 47 moderate / **1 high** / **0 very high**. A threshold no season can
cross classifies nothing.

`exclude_covid` drops 2019-20 (COVID truncated its tail), 2020-21 and 2021-22
(suppressed, then recovering), keeping two pre-pandemic anchors. It is the more
defensible statistical choice — 30 pooled values drawn from five winters rather
than three. The project runs `post_covid` as the default to stay consistent with
the `post_covid` model variant everything else is evaluated on, at the cost of no
pre-2020 anchor. **If you only report one set of thresholds, say which.**

### Why `values_per_season` is not 1

CDC's wording — "the geometric mean of peak weekly values in previous seasons" —
reads like one value per season. With three seasons that gives `m = 3`, and a
log-SD from three points:

```
--values-per-season 1  ->  citywide IT50 95.0, IT90 208.8, IT98 719.8
```

An IT98 of **719.8 per 100,000** is seven times the highest citywide week ever
observed. This is exactly what MEM's `30 / n_seasons` rule exists to prevent, and
the script warns whenever the pooled sample falls below 10. The cost of the rule
is a matter of interpretation: at 10 values per season the pool reaches past the
peak into the shoulder weeks, so **"moderate" here means "the epidemic is
underway", not "this season peaked at moderate"**.

## 3. The fitted thresholds

Default settings, per 100,000 residents. `severity_thresholds.csv` and
`severity_thresholds.json` carry these plus full provenance.

| indicator | IT50 | IT90 | IT98 | 2025-26 peak | season band |
| --- | --- | --- | --- | --- | --- |
| CITYWIDE | 60.2 | 98.2 | 134.2 | 101.9 | high |
| Allston/Brighton | 43.2 | 72.8 | 101.7 | 80.6 | high |
| Back Bay/Beacon Hill/… | 32.4 | 56.4 | 80.4 | 58.1 | high |
| Charlestown | 44.5 | 75.5 | 105.8 | 92.8 | high |
| Dorchester | 157.0 | 264.3 | 368.7 | 256.2 | moderate |
| East Boston | 32.4 | 57.0 | 81.8 | 59.3 | high |
| Fenway | 19.8 | 31.7 | 42.9 | 21.1 | moderate |
| Hyde Park | 59.7 | 98.7 | 136.1 | 94.6 | moderate |
| Jamaica Plain | 30.1 | 48.9 | 66.7 | 61.1 | high |
| Mattapan | 75.4 | 114.4 | 149.5 | 110.3 | moderate |
| Roslindale | 83.1 | 133.7 | 181.1 | 170.1 | high |
| Roxbury | 138.9 | 232.0 | 322.0 | 254.7 | high |
| South Boston | 31.6 | 60.2 | 90.8 | 57.0 | moderate |
| South End | 82.0 | 134.0 | 183.5 | 132.3 | moderate |
| West Roxbury | 37.4 | 59.6 | 80.4 | 88.0 | very high |

**Thresholds are per neighborhood because the scale is not shared.** Season peaks
run from about 48 per 100,000 in Fenway to 320 in Dorchester — nearly sevenfold.
A single citywide cut point would label Dorchester severe every winter and Fenway
never, which would say more about the denominator than the epidemic.

The citywide indicator is the unweighted mean across the 14 neighborhoods,
matching the `macro` scope in `metrics.py`. Unweighted, so Fenway counts as much
as Dorchester; a population-weighted version would be a different indicator and
would need a weekly population denominator this project does not carry.

## 4. No test week is in the thresholds

`fit_thresholds()` takes `threshold_end` and it is **exclusive**, defaulting to
`TEST_START` (2025-05-31).

This is not a formality. The 2024-25 season, as MEM defines a season, runs to
July 2025 — which is inside the evaluation window. Without the cutoff, the
thresholds a forecast is scored against would be fitted partly on the period
being scored. With it, the last week feeding any threshold is **2025-05-25**, six
days before the window opens. `fitted_through` is written into both output files
so a reader can check rather than trust.

## 5. From a forecast to a severity statement

Two readings of the same forecast are scored.

**Deterministic**: band the point forecast with the same thresholds used on the
observation. Simple, and it is what an operational rule would do.

**Probabilistic**: `exceedance_probability()` reads the calibrated 95% interval
already in `predictions.csv` as a Gaussian predictive distribution and integrates
above the threshold. Since `intervals.py` writes a half-width of
`kappa * Z95 * sqrt(variance)`, dividing by `Z95` recovers the scale it was built
from. This adds no assumption the band did not already make, and it reuses the
one interval recipe shared by every model, so the probabilities are comparable.

Two implementation notes:

- **The upper bound only.** `intervals.py:83` clips the lower bound at zero
  because a rate cannot be negative, so at low levels it sits nearer the
  prediction than the upper bound does. Using it, or averaging the two, would
  understate the spread exactly where most weeks are.
- Where a band has collapsed to zero width there is no distribution to
  integrate, and the probability is a hard 0 or 1. The run reports how many rows
  hit that path — 6 rows across the 16 horizon-4 runs, none at horizon 1.

For the citywide indicator the predictive spread is the **mean** of the
per-neighborhood spreads, not `sigma / sqrt(14)`. Neighborhood forecast errors
here move together, driven by the same citywide epidemic; treating them as
independent would shrink the band by nearly a factor of four and manufacture
confidence the models have not earned. `--citywide-sigma independent` exposes the
alternative for anyone who wants to see it.

## 6. The four things that get scored

| layer | question | key columns |
| --- | --- | --- |
| crossing | did it call the threshold crossing? | `POD FAR CSI F1 PSS HSS MCC` |
| bands | did it get the right one of four? | `exact_band within_one_band kappa_quadratic mean_band_error` |
| probability | was its confidence honest? | `brier brier_ref BSS` |
| timing | did it call it at the right week? | `onset_error_weeks lead_time_weeks peak_week_error_weeks` |

### The headline metric, and why it is not accuracy

**Exceedance is a rare event, so accuracy is worthless here.** Across the
2025-26 window there are 627 scored neighborhood-weeks: 51 crossings of IT50
(8.1%), 18 of IT90 (2.9%), 2 of IT98 (0.3%).

A forecast that never alerts scores **91.9% accuracy**. That is not a
hypothetical: `dualtopo` never crosses IT50 in this window at all, and duly
records 0.919 exact-band accuracy — ahead of `gat` (0.912) and within 0.03 of
every arm except `seasonal_naive`. Its `kappa_quadratic` is **0.000**, which is
the number that gives it away.

So **PSS (Peirce skill score, `POD - FPR`) leads the tables**. It is 0 for both
degenerate forecasts — never alert and always alert — so neither the base rate
nor an indiscriminate alarm can buy a score.

PSS has its own blind spot, which is why **CSI and F1 sit beside it**: PSS is
measured against roughly 576 correct negatives and barely moves when a model
raises many false alarms in absolute terms. CSI ignores correct negatives
entirely and exposes that. Section 8 shows the two disagreeing.

For the probabilistic layer the reference is **climatology**, not zero: a
constant 8% forecast is already well calibrated and already scores a low Brier at
a low base rate, so BSS measures improvement over that rather than over nothing.

Every denominator that can empty out returns `NaN`, never 0 — POD with no
events, FAR with no alerts, MCC with any empty marginal, quadratic kappa when
one band accounts for every week. Zero would read as "no skill"; the truth is
"not measurable", and conflating them lets an unmeasurable model outrank a
measured one. Rows with fewer than five observed events are flagged
`underpowered` and are reported but not ranked.

## 7. What the 2025-26 season looks like

Citywide, the season peaked at **101.9 per 100,000 in the week of 2025-12-21**,
between IT90 (98.2) and IT98 (134.2). **By CDC's peak-week rule that is a high
severity season.** Of 49 citywide weeks, 45 were low, 3 moderate, 1 high.

Per neighborhood, of 627 scored weeks: 576 low, 33 moderate, 16 high, 2 very
high. Both very-high weeks are West Roxbury, the only neighborhood whose 2025-26
peak (88.0) exceeded its own IT98 (80.4).

`severity_bands.png` is the CDC-style figure: observed rate against intensity
bands. **The figures are standardised and the scores are not, and the two can
disagree.** Every panel is drawn on one shared y-scale (0-300) against the
citywide bands, so the panels can be read against each other; the scores in
`severity_long.csv` always use each neighborhood's own thresholds. Dorchester's
peak of 256 therefore reads *very high* on the chart and scores as *moderate*,
because 256 is a routine December for Dorchester and would be a record anywhere
else. Pass `--per-neighborhood-scale` to draw the figure the way the scoring
works.

The citywide set is the shared one because pooling all 14 neighborhoods instead
would draw every pooled value from Dorchester and Roxbury: 12 of the 14 would
then read *low* even at their own season peak.

## 8. What the models actually did

Horizon 1, `post_covid`, all neighborhood-weeks pooled, full year, IT50
(51 events, base rate 0.081). Full tables in
`results/horizon_01/_comparison/severity_leaderboard.md`.

| model | hits | misses | false alarms | POD | FAR | CSI | PSS | BSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gnn_st | 40 | 11 | 10 | 0.784 | 0.200 | **0.656** | **0.767** | **0.709** |
| lstm | 38 | 13 | 9 | 0.745 | 0.191 | 0.633 | 0.729 | 0.591 |
| persistence | 36 | 15 | 15 | 0.706 | 0.294 | 0.545 | 0.680 | 0.528 |
| arima | 35 | 16 | 10 | 0.686 | 0.222 | 0.574 | 0.669 | 0.529 |
| xgboost | 32 | 19 | 13 | 0.627 | 0.289 | 0.500 | 0.605 | 0.492 |
| gat | 15 | 36 | 14 | 0.294 | 0.483 | 0.231 | 0.270 | 0.188 |
| dualtopo | 0 | 51 | 0 | 0.000 | — | 0.000 | 0.000 | -0.057 |
| seasonal_naive | 6 | 45 | 77 | 0.118 | 0.928 | 0.047 | -0.016 | -0.545 |

**`gnn_st` leads every column at once, which is new.** An earlier revision of
this section reported the opposite and made the disagreement the finding: the
best-PSS arm then (`gnn_multiedge_season`) bought 44 hits with **56 false
alarms** against 51 real events, while the LSTM caught six fewer events with nine
false alarms and led CSI, F1 and BSS. You had to choose which metric you
believed.

That trade-off is gone. `gnn_st` catches 40 of 51 events with **10** false
alarms, so it tops PSS (0.767), CSI (0.656) and BSS (0.709) simultaneously.
Nothing about the metrics changed — the previous graph arms were simply
over-alerting, and predicting a residual from a persistence/climatology blend
stopped it.

**Read the PSS column together with FAR anyway.** The reason PSS alone is unsafe
has not changed: it is insensitive to the 8% base rate, so an over-alerting model
can score well on it while being unusable. `seasonal_naive` is the demonstration
— 77 false alarms for 6 hits, PSS −0.016.

Note also that `persistence` and `arima` — the two trivial baselines — still sit
within **0.09 PSS** of the best model (0.680 and 0.669 against 0.767). **At one
week ahead, the severity crossings are largely predictable by carrying last week
forward**, and that remains true even now that a model beats them.

### Bands, calibration and timing

Over all four bands (627 weeks): `gnn_st` 0.946 exact and 0.997 within one band,
`lstm` 0.939, `arima` 0.936, `persistence` 0.928, `xgboost` 0.928, `dualtopo`
0.919, `gat` 0.912, `seasonal_naive` 0.801. `gnn_st` also leads
`kappa_quadratic` at 0.783, which is the one to read here: it credits being
*close* on an ordered scale rather than exactly right, and `dualtopo` scores
0.000 on it while holding 0.919 exact accuracy — the signature of a model that
just always says "low" in a series that is usually low.

`mean_band_error` separates the failure modes. `gnn_st` is −0.016 and
`persistence` 0.000, both essentially unbiased; `dualtopo` is −0.113 and never
calls severity at all; `seasonal_naive` is +0.078, the only arm that
systematically over-calls. The superseded graph arms sat at +0.112 — over-calling
harder than the seasonal naive — which is the same over-alerting visible in the
contingency table above.

**The over-confidence problem was real and is worth keeping on the record.**
`severity_reliability.png` used to show the graph arm badly miscalibrated in the
middle of the range: weeks it gave roughly a 30% chance of crossing IT50 crossed
about 4% of the time. Only part of that was interval width — its pooled
test-window `CI_coverage` was 87.4% against the 95% it was calibrated to, and a
7.6-point coverage shortfall does not account for a 30% forecast landing at 4%.
**Magnitude calibration and exceedance calibration are different properties, and
passing one does not buy the other.** `gnn_st` holds 96.8% coverage at h=1, so
check its reliability curve rather than assuming the problem left with the old
arm.

### Skill decays with horizon, as it must

`persistence` at IT50, pooled, full year — the same 51 events scored at each
horizon:

| horizon | PSS | CSI |
| --- | --- | --- |
| 1 | 0.680 | 0.545 |
| 2 | 0.402 | 0.291 |
| 4 | -0.046 | 0.020 |
| 12 | -0.085 | 0.000 |

**Beyond about two weeks, carrying last week forward has no severity skill at
all** — negative PSS means it is worse than chance at separating crossing weeks
from quiet ones. This is the check to run first on any new model: a severity
score that does not decay with horizon indicates a leak, not a discovery.

### Timing

Timing at IT50, median over neighborhood-seasons: most models cross **one week
late**, which is what a one-week-ahead forecast tracking a rising curve does.
`seasonal_naive` is four weeks late. `dualtopo` never crosses, so it has no
timing at all — a blank, not a zero.

## 9. Honest limitations

1. **One test season.** Every number here comes from 2025-26. There is one
   citywide epidemic in the window, so the citywide indicator has 4 IT50
   crossings and 1 IT90 crossing — flagged `underpowered` and not ranked. The
   pooled per-neighborhood view has 51, which is why it is the headline scope,
   but its 14 series are far from independent: they share one epidemic wave.
   Treat the pooled `n` as optimistic.
2. **IT98 is not evaluated.** Two events in 627 weeks. The rows are written and
   flagged; they are not evidence about anything.
3. **Single seed.** `docs/EDGES_AND_NODES_NOTES.txt` section 11 puts this
   project's single-seed noise floor at 0.2-0.5 MAE. Nobody has established the
   equivalent floor for PSS, and it is likely to be worse, because one flipped
   week out of 51 events moves POD by 0.02. **The ordering of the top few models
   should be assumed unstable until re-run with several seeds.**
4. **Three reference seasons.** The default thresholds rest on three winters. The
   `exclude_covid` set moves citywide IT50 by 11 points, or 18% — larger than
   most of the differences between models in section 8.
5. **One indicator, not three.** CDC combines outpatient ILI, hospitalisation
   rate and mortality, and calls a season by what at least two of the three do.
   This project has only ILI ED visit rates, so there is no cross-indicator
   confirmation. A band here is a statement about one surveillance stream.
6. **No MEM epidemic threshold.** MEM also defines an epidemic onset threshold
   from pre-epidemic weeks via an optimised sliding window. That is not
   implemented; the "onset" in `severity_timing.csv` is the first crossing of an
   *intensity* threshold, which is a later and different event. Do not cite it as
   a MEM epidemic onset.
7. **Bands are not calendar-adjusted.** A week is banded on its rate alone. An
   August week reaching IT50 would be called moderate, which is arguably right
   and arguably an artefact — no such week occurs in this window, so it has not
   been tested.
8. **The exceedance probabilities inherit the interval's assumptions.** They are
   a Gaussian reading of a band calibrated for 95% coverage of the *magnitude*.
   Section 8 shows that coverage being right while exceedance is over-confident.

## Reproducing the checks

```bash
python Code/compare_severity.py --results-dir Code/results/horizon_01 --variant post_covid
python Code/compare_severity.py --results-dir Code/results/horizon_04 --variant post_covid
python Code/compare_severity.py --reference-seasons exclude_covid    # section 2 sensitivity
python Code/compare_severity.py --values-per-season 1                # warns, pool of 3
python Code/compare_severity.py --rank-by CSI                        # re-rank section 8
```

Writes into a `_comparison/` beside the results being read, so each horizon keeps
its own set:

| file | contents |
| --- | --- |
| `severity_thresholds.csv` / `.json` | the thresholds and their full provenance |
| `severity_long.csv` | every metric, per model / scope / segment / level |
| `severity_bands.csv` | per week and indicator: observed band, forecast band, exceedance probabilities |
| `severity_timing.csv` | onset, peak and lead time per indicator-season |
| `severity_leaderboard.md` | the ranked tables |
| `severity_bands.png` | observed rate against its intensity bands |
| `severity_skill.png` | skill by threshold, with the no-skill line |
| `severity_reliability.png` | forecast probability against observed frequency |
| `severity_timing.png` | onset error in weeks, per model |

Related: [`METRICS_PLAIN.md`](METRICS_PLAIN.md) for what the score columns mean
in plain terms, [`DATA_NOTES.md`](DATA_NOTES.md) for what the underlying series is and
where it is suppressed, [`RT_CAVEATS.md`](RT_CAVEATS.md) for the other
derived quantity in this project that needs reading with care.
