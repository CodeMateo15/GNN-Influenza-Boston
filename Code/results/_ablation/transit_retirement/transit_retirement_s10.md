# Feature and design ablations

> **`gnn_st_transit` no longer exists.** It was a temporary arm added to measure
> MBTA transit edges one last time before the pipeline was deleted, and it was
> removed from `Code/influenza/config.py` along with `GraphSpec.transit` and
> `Data/MBTA/`. This table cannot be regenerated; it is the measurement of record
> for that decision. The verdict column is blank because the noise-floor estimate
> in `run_ablation.py` needs more than two arms per horizon — read the deltas
> against a per-seed spread of about 0.015 macro Corr at h=2 and 0.05 at h=4, and
> see `Code/docs/METHODS.md`, "Transit (retired)", for the full reading.

Each arm is `gnn_st` with exactly one change, refit from scratch. Feature groups are removed and the model retrained rather than permuted, because several groups are constant within a forecast origin and permutation cannot measure them.

## Horizon 1

Reference `gnn_st`: macro Corr 0.893, pooled 0.927, RMSE 11.71. Every arm below is the same configuration with one change, refit at the same seed count.

### feature (add one in)

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_transit` | 0.892 | -0.001 | 0.926 | -0.002 | 11.85 |  |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

## Horizon 2

Reference `gnn_st`: macro Corr 0.802, pooled 0.840, RMSE 17.21. Every arm below is the same configuration with one change, refit at the same seed count.

### feature (add one in)

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_transit` | 0.795 | -0.007 | 0.835 | -0.005 | 17.46 |  |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.

## Horizon 4

Reference `gnn_st`: macro Corr 0.582, pooled 0.676, RMSE 23.07. Every arm below is the same configuration with one change, refit at the same seed count.

### feature (add one in)

| arm | macro | Δ macro | pooled | Δ pooled | RMSE | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| `gnn_st_transit` | 0.597 | +0.015 | 0.685 | +0.009 | 22.80 |  |

`Δ macro` is this arm minus the reference. In a **leave-one-out** row the arm removes a group, so a negative Δ means the model got worse without it and the group was earning its place. In an **add-one-in** row the arm adds a group, so a negative Δ means adding it made things worse. Same sign, opposite meaning -- read the section heading.
