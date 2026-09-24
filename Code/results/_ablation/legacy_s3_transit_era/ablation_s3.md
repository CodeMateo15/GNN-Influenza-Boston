# Feature and design ablations

Each arm is `gnn_st` with exactly one change, refit from scratch. Feature groups are removed and the model retrained rather than permuted, because several groups are constant within a forecast origin and permutation cannot measure them.

## Horizon 2

Reference `gnn_st`: macro Corr 0.798, pooled 0.827, RMSE 18.22. Every arm below is the same configuration with one change, refit at the same seed count.

**Noise floor: +/-0.013 macro Corr.** Estimated as the pooled per-seed standard deviation across arms at this horizon. A delta smaller than this is not a finding.

### feature (leave one out)

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_noweather` | 0.780 | -0.018 | 0.825 | -0.001 | 17.67 | **earns its place** |
| `gnn_st_noimputedflag` | 0.792 | -0.006 | 0.832 | +0.005 | 17.73 | inside noise |
| `gnn_st_noseason` | 0.799 | +0.001 | 0.835 | +0.008 | 18.14 | inside noise |
| `gnn_st_nodemo` | 0.804 | +0.006 | 0.834 | +0.007 | 17.96 | inside noise |
| `gnn_st_lagsonly` | 0.816 | +0.018 | 0.848 | +0.022 | 16.60 | **better without it** |
| `gnn_st_noglobals` | 0.821 | +0.024 | 0.855 | +0.028 | 16.52 | **better without it** |

### feature (add one in)

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_covid_rsv` | 0.679 | -0.119 | 0.740 | -0.087 | 21.89 | **adding it HURTS** |
| `gnn_st_vaccination` | 0.781 | -0.017 | 0.821 | -0.006 | 18.41 | **adding it HURTS** |
| `gnn_st_wastewater` | 0.816 | +0.018 | 0.855 | +0.028 | 17.41 | **adding it helps** |

### design

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_level` | 0.747 | -0.050 | 0.779 | -0.048 | 20.34 | **earns its place** |
| `gnn_st_relations` | 0.786 | -0.012 | 0.818 | -0.009 | 18.68 | inside noise |
| `gnn_st_delta` | 0.795 | -0.003 | 0.830 | +0.003 | 18.45 | inside noise |
| `gnn_st_nopearson` | 0.795 | -0.003 | 0.830 | +0.003 | 17.96 | inside noise |
| `gnn_st_noadapt` | 0.801 | +0.004 | 0.842 | +0.015 | 17.34 | inside noise |
| `gnn_st_tiny` | 0.809 | +0.011 | 0.839 | +0.012 | 17.55 | inside noise |

### graph

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_nograph` | 0.708 | -0.090 | 0.772 | -0.054 | 20.07 | **earns its place** |
| `gnn_st_adaptiveonly` | 0.781 | -0.017 | 0.817 | -0.010 | 19.04 | **earns its place** |
| `gnn_st_nocorr` | 0.783 | -0.015 | 0.816 | -0.011 | 18.90 | **earns its place** |
| `gnn_st_geoonly` | 0.791 | -0.007 | 0.825 | -0.002 | 18.20 | inside noise |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.
