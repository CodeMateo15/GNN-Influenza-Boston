# Feature and design ablations

Each arm is `gnn_st` with exactly one change, refit from scratch. Feature groups are removed and the model retrained rather than permuted, because several groups are constant within a forecast origin and permutation cannot measure them.

All arms ran on the same budget and the reference ensembles agree on the inputs (300 epochs, 247 edges, 46 node features, 3 global covariates), so the deltas below isolate the one change named in each row. Feature and graph arms differ from the reference in their own feature or edge count by design; that is what they measure.

## Horizon 2

Reference `gnn_st`: macro Corr 0.798, pooled 0.827, RMSE 18.22. Every arm below is the same configuration with one change, refit at the same seed count.

**How big does a difference have to be before it means anything? 0.011 macro Corr.** Inferred from the across-arm spread (FALLBACK, not a measurement) -- no reference replicates were run, so this is a guess at the noise, not a measurement of it, and it moves when the arm list moves. A delta smaller than that is seed luck, not a finding.

### feature (leave one out)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_noweather` | 0.780 | -0.018 | 0.825 | 17.67 | 4/14 | 0.058 | **earns its place** |
| `gnn_st_noimputedflag` | 0.792 | -0.006 | 0.832 | 17.73 | 4/14 | 0.119 | inside noise |
| `gnn_st_nodemoedge` | 0.797 | -0.001 | 0.825 | 18.66 | 7/14 | 0.761 | inside noise |
| `gnn_st_lean` | 0.798 | +0.000 | 0.836 | 17.25 | 7/14 | 0.855 | inside noise |
| `gnn_st_nodemo` | 0.804 | +0.006 | 0.834 | 17.96 | 11/14 | 0.025 | inside noise |
| `gnn_st_nodemofeat` | 0.811 | +0.013 | 0.843 | 17.39 | 12/14 | 0.001 | **better without it** |
| `gnn_st_lagsonly` | 0.816 | +0.018 | 0.848 | 16.60 | 12/14 | 0.003 | **better without it** |

### feature (add one in)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_covid_rsv` | 0.679 | -0.119 | 0.740 | 21.89 | 0/14 | <0.001 | **adding it HURTS** |
| `gnn_st_vaccination` | 0.781 | -0.017 | 0.821 | 18.41 | 1/14 | <0.001 | **adding it HURTS** |
| `gnn_st_wastewater` | 0.816 | +0.018 | 0.855 | 17.41 | 11/14 | 0.017 | **adding it helps** |

### design

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_level` | 0.747 | -0.050 | 0.779 | 20.34 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_relations` | 0.786 | -0.012 | 0.818 | 18.68 | 2/14 | 0.002 | **earns its place** |
| `gnn_st_delta` | 0.795 | -0.003 | 0.830 | 18.45 | 6/14 | 0.296 | inside noise |
| `gnn_st_nopearson` | 0.795 | -0.003 | 0.830 | 17.96 | 5/14 | 0.326 | inside noise |
| `gnn_st_noadapt` | 0.801 | +0.004 | 0.842 | 17.34 | 9/14 | 0.502 | inside noise |
| `gnn_st_tiny` | 0.809 | +0.011 | 0.839 | 17.55 | 13/14 | <0.001 | inside noise |

### graph

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_nograph` | 0.708 | -0.090 | 0.772 | 20.07 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_adaptiveonly` | 0.781 | -0.017 | 0.817 | 19.04 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_nocorr` | 0.783 | -0.015 | 0.816 | 18.90 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_geoonly` | 0.791 | -0.007 | 0.825 | 18.20 | 5/14 | 0.058 | inside noise |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

`nbhds improved` counts how many of the scored neighborhoods this arm beat the reference in, and `p` is a Wilcoxon signed-rank test on those paired per-neighborhood differences. A verdict backed by a lopsided count and a small p is worth more than one that rests on the macro average alone, because the macro average can be moved by one node.
