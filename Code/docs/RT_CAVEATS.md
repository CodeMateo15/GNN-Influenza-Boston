# Rt: what it is here, and what it is not

`influenza/rt.py` produces a per-neighborhood weekly quantity we call `Rt`. It is
computed with `epyestim`, the Python implementation of the Cori et al. method
that underlies the R package [EpiEstim](https://github.com/mrc-ide/EpiEstim).

**Call it a relative growth index, not a reproduction number.** The reasons are
below, in decreasing order of importance.

## 1. The input is weekly; the method wants daily

Rt asks "how many people does one infected person go on to infect?" Answering it
needs day-by-day incidence, because influenza's generation interval — infection
to onward infection — is only about 2.85 days. A single weekly observation
already blurs more than two generations of transmission together.

To use epyestim at all we interpolate the weekly series to daily. Within each
week that interpolation is an assumption, not data. Everything downstream
inherits it.

## 2. The input is a rate, not a case count

The series is ILI ED visits per 100,000. Rt is driven by the ratio between
successive incidence values, so a fixed population scale does not change the
point estimate — but the Poisson likelihood in the Cori posterior does depend on
counts, so the credible intervals are meaningless at an arbitrary scale.

**Only the posterior mean is kept.** The 2.5% and 97.5% quantiles epyestim can
produce are not reported anywhere, because they would imply a precision the
input cannot support.

## 3. `bagging_r` cannot be made causal, so we do not use it

Rt is used as a *feature* to predict later weeks, so `Rt(t)` must not depend on
anything after week `t`. epyestim's headline entry point, `bagging_r`, combines a
LOWESS smoother with a Richardson-Lucy deconvolution, and **both are fitted over
the whole series**. Measured on this data: dropping the last 12 weeks changed
earlier Rt values by up to **0.71**. That is a straightforward leak of the future
into the past.

`weekly_rt(..., causal=True)` — the default — instead calls
`epyestim.estimate_r.estimate_r`, the pure Cori estimator, in which `Rt(t)`
depends only on incidence up to `t` by construction. We pre-smooth with a
**trailing** 14-day mean and skip the delay deconvolution entirely. The same
truncation test now gives a maximum drift of exactly **0.00** across 2,646 cells.
`run_rt_diagnostics.py` re-runs that check every time.

The cost of dropping the deconvolution is that Rt is shifted later in time by
roughly the infection-to-report delay. For a feature, being causal matters more
than being correctly dated.

Set `causal=False` to get the full `bagging_r` pipeline. Do not then use the
result as a model feature.

## 4. Distributions are influenza's, not COVID's

epyestim ships COVID defaults. We substitute:

| distribution | mean | sd | source |
|---|---|---|---|
| generation interval | 2.85 d | 0.93 d | Cauchemez et al. 2004 |
| infection → ILI ED visit | 3.0 d | 2.0 d | assumed; only used when `causal=False` |

## 5. What the output actually looks like

Post-COVID, 14 neighborhoods, 201 weeks:

- median 1.15, 5th–95th percentile [0.93, 1.53]
- **86% of weeks sit above 1.0**

A genuinely endemic disease observed over four years should average close to 1.
The upward bias comes from the trailing smoother, which shifts the curve later
and so makes a series look like it is still rising. This is why the value should
be read comparatively (it is z-scored before the model sees it) rather than as
"Rt = 1.15, therefore the epidemic is growing 15% per generation".

Against the plain week-over-week log growth ratio, the causal Rt correlates only
weakly (Pearson 0.16, Spearman 0.15). Two readings, and the honest answer is that
both are partly true:

- **Good news**: it is not merely a re-encoding of the growth ratio, so it can
  carry information a lag feature does not.
- **Bad news**: a growth-style index that barely tracks growth is partly
  reflecting the interpolation and smoothing rather than the epidemic.

## 6. Does it help?

`USE_RT` defaults to `False`. The ablation is a registry entry, so the data
decides rather than the argument:

```
python Code/run_gnn.py --experiment gnn_multiedge       # Rt off
python Code/run_gnn.py --experiment gnn_multiedge_rt    # Rt on
```

Measured once, single seed, post-COVID, horizon 1, pooled `overall`:

| | RMSE | MAE | Corr |
|---|---|---|---|
| `gnn_multiedge` | 24.54 | 14.89 | 0.860 |
| `gnn_multiedge_rt` | 23.03 | 13.86 | 0.855 |

A ~1.5 RMSE improvement. Treat it as suggestive only: `docs/EDGES_AND_NODES_NOTES.txt`
section 11 puts this project's single-seed noise floor at 0.2–0.5 MAE on a
smaller scale, and this is one seed. Re-run with several seeds before claiming
the feature helps.

## Reproducing the checks

```
python Code/run_rt_diagnostics.py
```

Writes `results/_diagnostics/rt_by_neighborhood.png` and `rt_weekly.csv`, and
prints the distribution, the redundancy check against week-over-week growth, and
the causality check.
