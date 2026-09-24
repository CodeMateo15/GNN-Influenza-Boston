# Runs produced while MBTA transit edges were still active

MBTA transit edges were removed from the project in September 2026: the code
path, the `GraphSpec.transit` flag and the 102 MB `Data/MBTA/` tree are all gone.
See `Code/docs/METHODS.md`, section "Transit (retired)", for the measurement that
settled it.

Results committed before that removal record `"transit": true` and
`graph_counts.transit = 32`, and were fit on a 108-edge graph rather than the
107-edge graph the current code builds. **None of them is reproducible from the
current registry.**

## Resolved — refit 2026-09-17

| directory | arms | status |
|---|---|---|
| `horizon_01/`, `horizon_02/`, `horizon_04/` | `gnn_st_lagsonly`, `gnn_st_noglobals` | **refit** without transit at the registry's 120-epoch budget |
| `horizon_04/` | all 12 cells | **refit** on one commit, so the h=4 leaderboard is internally consistent |

Those two arms had been trained **with** transit edges *and* at the old 300-epoch
budget while the `gnn_st` reference beside them had neither, so a delta read off
those directories mixed three things at once. Both are now like-for-like with
`gnn_st` at all three horizons.

The whole `horizon_04/` directory was rebuilt at the same time because its
`gnn_st` was still at 300 epochs — fixing only the two arms would have replaced a
transit confound with a budget one.

## Still transit-era — read with care

| directory | arms | note |
|---|---|---|
| `_ablation/h02_s3/` | all 23 arms except `gnn_st_adaptiveonly`, `gnn_st_geoonly`, `gnn_st_nograph` | the three-seed ablation table |
| `_ablation/h04_s3/` | `gnn_st`, `gnn_st_delta` | |

`_ablation/h02_s3/gnn_st_notransit/` is the leave-one-out arm for transit. It no
longer exists in `Code/influenza/config.py` and cannot be re-run. It is kept
because it is the three-seed measurement the removal decision started from; its
reported delta was `+0.000` macro Corr, which should not be quoted on its own.

## Two things a reader should know

**`gnn_st_noglobals` is config-identical to `gnn_st`.** `DEFAULT_GLOBALS` is
already `()`, so "no city-wide covariates" removes nothing — `replace(gnn_st,
globals_=())` reproduces `gnn_st` exactly. The arm is a no-op and its row is a
duplicate of the reference. That is useful by accident: the gap between the two
rows is a direct read on run-to-run spread between identical configurations, and
it came out at 0.059 RMSE at h=1, 0.017 at h=2 and 0.000 at h=4. Any arm whose
advantage is smaller than that is not distinguishable from noise.

**Cluster runs do not record a commit.** `Code/sweep/sync.sh` excludes `.git/`
from the payload, so `run_gnn.py` cannot read a SHA on Explorer and every
`run_config.json` produced there has `"git_sha": null`. The h=4 cells refit on
2026-09-17 are all from one working tree, but the files do not say so themselves
— the `created` timestamps are the only provenance they carry.

## What to cite for the transit question

`_ablation/h01_s10/`, `h02_s10/` and `h04_s10/` hold the ten-seed
`gnn_st` vs `gnn_st_transit` comparison, both arms trained in the same batch on
the same hardware. That is the measurement of record.
