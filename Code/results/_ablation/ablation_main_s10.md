# Feature and design ablations

Each arm is `gnn_st` with exactly one change, refit from scratch. Feature groups are removed and the model retrained rather than permuted, because several groups are constant within a forecast origin and permutation cannot measure them.

All arms ran on the same budget and the reference ensembles agree on the inputs (120 epochs, 215 edges, 46 node features, 0 global covariates), so the deltas below isolate the one change named in each row. Feature and graph arms differ from the reference in their own feature or edge count by design; that is what they measure.

## Horizon 1

Reference `gnn_st`: macro Corr 0.893, pooled 0.927, RMSE 11.71. Every arm below is the same configuration with one change, refit at the same seed count.

**How big does a difference have to be before it means anything? 0.003 macro Corr.** Measured as the full range across 3 reference ensembles: identical configurations differing only in which seeds they drew. A delta smaller than that is seed luck, not a finding.
Reference ensembles at this horizon scored 0.893, 0.895, 0.892.

### feature (leave one out)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_lagsonly` | 0.880 | -0.012 | 0.919 | 12.34 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_noweather` | 0.881 | -0.012 | 0.920 | 12.30 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_lean` | 0.882 | -0.010 | 0.921 | 12.18 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_noimputedflag` | 0.890 | -0.002 | 0.925 | 11.87 | 5/14 | 0.068 | inside noise |
| `gnn_st_nodemofeat` | 0.892 | -0.000 | 0.927 | 11.75 | 6/14 | 0.855 | inside noise |
| `gnn_st_nodemo` | 0.894 | +0.001 | 0.928 | 11.70 | 9/14 | 0.217 | inside noise |
| `gnn_st_nodemoedge` | 0.896 | +0.003 | 0.929 | 11.57 | 13/14 | <0.001 | **better without it** |

### feature (add one in)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_covid_rsv` | 0.862 | -0.031 | 0.902 | 13.55 | 0/14 | <0.001 | **adding it HURTS** |
| `gnn_st_wastewater` | 0.875 | -0.017 | 0.923 | 12.10 | 3/14 | 0.002 | **adding it HURTS** |
| `gnn_st_globals` | 0.888 | -0.004 | 0.920 | 12.56 | 4/14 | 0.013 | **adding it HURTS** |
| `gnn_st_season` | 0.892 | -0.001 | 0.926 | 11.80 | 6/14 | 0.358 | inside noise |
| `gnn_st_vaccination` | 0.893 | +0.000 | 0.928 | 11.71 | 7/14 | 0.903 | inside noise |

### design

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_noadapt` | 0.882 | -0.011 | 0.922 | 12.20 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_delta` | 0.882 | -0.010 | 0.919 | 12.52 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_tiny` | 0.887 | -0.005 | 0.924 | 12.04 | 3/14 | 0.017 | **earns its place** |
| `gnn_st_nopearson` | 0.891 | -0.001 | 0.926 | 11.87 | 3/14 | 0.091 | inside noise |
| `gnn_st_level` | 0.892 | -0.000 | 0.914 | 12.89 | 7/14 | 1.000 | inside noise |
| `gnn_st_relations` | 0.893 | +0.000 | 0.928 | 11.72 | 9/14 | 0.715 | inside noise |

### graph

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_nograph` | 0.818 | -0.075 | 0.871 | 15.36 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_nocorr` | 0.893 | +0.000 | 0.927 | 11.82 | 9/14 | 0.761 | inside noise |
| `gnn_st_geoonly` | 0.894 | +0.001 | 0.928 | 11.73 | 9/14 | 0.091 | inside noise |
| `gnn_st_adaptiveonly` | 0.899 | +0.006 | 0.929 | 11.60 | 11/14 | 0.017 | **better without it** |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

`nbhds improved` counts how many of the scored neighborhoods this arm beat the reference in, and `p` is a Wilcoxon signed-rank test on those paired per-neighborhood differences. A verdict backed by a lopsided count and a small p is worth more than one that rests on the macro average alone, because the macro average can be moved by one node.

## Horizon 2

Reference `gnn_st`: macro Corr 0.802, pooled 0.840, RMSE 17.21. Every arm below is the same configuration with one change, refit at the same seed count.

**How big does a difference have to be before it means anything? 0.006 macro Corr.** Measured as the full range across 3 reference ensembles: identical configurations differing only in which seeds they drew. A delta smaller than that is seed luck, not a finding.
Reference ensembles at this horizon scored 0.802, 0.807, 0.808.

### feature (leave one out)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_lean` | 0.768 | -0.034 | 0.817 | 18.07 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_noweather` | 0.772 | -0.031 | 0.819 | 17.97 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_lagsonly` | 0.794 | -0.008 | 0.838 | 17.01 | 2/14 | 0.003 | **earns its place** |
| `gnn_st_nodemofeat` | 0.799 | -0.003 | 0.839 | 17.19 | 4/14 | 0.035 | inside noise |
| `gnn_st_nodemo` | 0.800 | -0.002 | 0.838 | 17.30 | 5/14 | 0.153 | inside noise |
| `gnn_st_nodemoedge` | 0.804 | +0.002 | 0.841 | 17.18 | 9/14 | 0.091 | inside noise |
| `gnn_st_noimputedflag` | 0.809 | +0.006 | 0.845 | 16.81 | 12/14 | 0.002 | **better without it** |

### feature (add one in)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_covid_rsv` | 0.647 | -0.155 | 0.724 | 22.50 | 0/14 | <0.001 | **adding it HURTS** |
| `gnn_st_globals` | 0.796 | -0.006 | 0.832 | 17.85 | 2/14 | 0.003 | **adding it HURTS** |
| `gnn_st_season` | 0.802 | -0.001 | 0.841 | 16.99 | 8/14 | 0.670 | inside noise |
| `gnn_st_vaccination` | 0.810 | +0.008 | 0.847 | 16.83 | 13/14 | <0.001 | **adding it helps** |
| `gnn_st_wastewater` | 0.816 | +0.013 | 0.860 | 16.25 | 11/14 | 0.042 | **adding it helps** |

### design

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_level` | 0.743 | -0.059 | 0.783 | 19.97 | 2/14 | <0.001 | **earns its place** |
| `gnn_st_delta` | 0.783 | -0.019 | 0.825 | 18.39 | 1/14 | <0.001 | **earns its place** |
| `gnn_st_relations` | 0.792 | -0.011 | 0.830 | 17.62 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_noadapt` | 0.795 | -0.007 | 0.838 | 17.22 | 4/14 | 0.042 | **earns its place** |
| `gnn_st_tiny` | 0.796 | -0.007 | 0.837 | 17.25 | 2/14 | 0.002 | **earns its place** |
| `gnn_st_nopearson` | 0.796 | -0.006 | 0.834 | 17.52 | 1/14 | <0.001 | **earns its place** |

### graph

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_nograph` | 0.709 | -0.093 | 0.771 | 20.19 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_adaptiveonly` | 0.797 | -0.006 | 0.834 | 17.65 | 3/14 | 0.030 | inside noise |
| `gnn_st_geoonly` | 0.798 | -0.004 | 0.837 | 17.32 | 2/14 | 0.009 | inside noise |
| `gnn_st_nocorr` | 0.800 | -0.003 | 0.838 | 17.31 | 3/14 | 0.013 | inside noise |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

`nbhds improved` counts how many of the scored neighborhoods this arm beat the reference in, and `p` is a Wilcoxon signed-rank test on those paired per-neighborhood differences. A verdict backed by a lopsided count and a small p is worth more than one that rests on the macro average alone, because the macro average can be moved by one node.

## Horizon 4

Reference `gnn_st`: macro Corr 0.582, pooled 0.676, RMSE 23.07. Every arm below is the same configuration with one change, refit at the same seed count.

**How big does a difference have to be before it means anything? 0.031 macro Corr.** Measured as the full range across 3 reference ensembles: identical configurations differing only in which seeds they drew. A delta smaller than that is seed luck, not a finding.
Reference ensembles at this horizon scored 0.582, 0.613, 0.587.

### feature (leave one out)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_lean` | 0.550 | -0.032 | 0.655 | 23.67 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_noweather` | 0.557 | -0.025 | 0.661 | 23.54 | 0/14 | <0.001 | inside noise |
| `gnn_st_lagsonly` | 0.559 | -0.023 | 0.662 | 23.51 | 1/14 | <0.001 | inside noise |
| `gnn_st_nodemoedge` | 0.581 | -0.001 | 0.676 | 23.15 | 4/14 | 0.296 | inside noise |
| `gnn_st_noimputedflag` | 0.583 | +0.002 | 0.673 | 23.24 | 8/14 | 0.268 | inside noise |
| `gnn_st_nodemo` | 0.590 | +0.008 | 0.682 | 22.90 | 13/14 | <0.001 | inside noise |
| `gnn_st_nodemofeat` | 0.609 | +0.027 | 0.694 | 22.50 | 14/14 | <0.001 | inside noise |

### feature (add one in)

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_covid_rsv` | 0.423 | -0.159 | 0.573 | 26.14 | 0/14 | <0.001 | **adding it HURTS** |
| `gnn_st_globals` | 0.603 | +0.021 | 0.689 | 22.62 | 14/14 | <0.001 | inside noise |
| `gnn_st_season` | 0.607 | +0.025 | 0.693 | 22.48 | 13/14 | <0.001 | inside noise |
| `gnn_st_vaccination` | 0.623 | +0.041 | 0.702 | 22.23 | 14/14 | <0.001 | **adding it helps** |
| `gnn_st_wastewater` | 0.671 | +0.089 | 0.740 | 21.59 | 14/14 | <0.001 | **adding it helps** |

### design

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_delta` | 0.486 | -0.096 | 0.590 | 26.85 | 0/14 | <0.001 | **earns its place** |
| `gnn_st_level` | 0.553 | -0.029 | 0.632 | 24.87 | 3/14 | 0.058 | inside noise |
| `gnn_st_relations` | 0.578 | -0.004 | 0.672 | 23.20 | 5/14 | 0.119 | inside noise |
| `gnn_st_tiny` | 0.579 | -0.003 | 0.673 | 23.30 | 6/14 | 0.296 | inside noise |
| `gnn_st_nopearson` | 0.589 | +0.007 | 0.679 | 22.96 | 11/14 | 0.002 | inside noise |
| `gnn_st_noadapt` | 0.598 | +0.016 | 0.682 | 22.89 | 14/14 | <0.001 | inside noise |

### graph

| arm | macro | Δ macro | pooled | RMSE | nbhds improved | p | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_geoonly` | 0.572 | -0.009 | 0.670 | 23.37 | 0/14 | <0.001 | inside noise |
| `gnn_st_nograph` | 0.573 | -0.009 | 0.671 | 23.16 | 6/14 | 0.463 | inside noise |
| `gnn_st_adaptiveonly` | 0.588 | +0.006 | 0.678 | 22.98 | 9/14 | 0.153 | inside noise |
| `gnn_st_nocorr` | 0.610 | +0.028 | 0.694 | 22.46 | 13/14 | <0.001 | inside noise |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

`nbhds improved` counts how many of the scored neighborhoods this arm beat the reference in, and `p` is a Wilcoxon signed-rank test on those paired per-neighborhood differences. A verdict backed by a lopsided count and a small p is worth more than one that rests on the macro average alone, because the macro average can be moved by one node.
