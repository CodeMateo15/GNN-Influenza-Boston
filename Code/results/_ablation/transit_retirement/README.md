# Transit retirement — measurement of record, do not regenerate

`gnn_st_transit` no longer exists. It was a temporary arm added to measure MBTA
transit edges one last time before the pipeline was deleted, and it was removed
from `Code/influenza/config.py` along with `GraphSpec.transit` and `Data/MBTA/`.
**These numbers cannot be reproduced by any current code path.**

Formerly `_ablation/ablation_s10.{csv,md}` and `_ablation/h{01,02,04}_s10/`.
They were moved here because `run_ablation.py` keyed its output filename on the
seed count alone, so the next `--n-seeds 10` run of any study would have
silently overwritten them. The driver now takes a `--study` flag and writes
`ablation_{study}_s{n}.{csv,md}`, so the collision cannot recur.

Read the deltas against a per-seed spread of about 0.015 macro Corr at h=2 and
0.05 at h=4. See `Code/docs/METHODS.md`, "Transit (retired)".

## Careful with `sync.sh pull`

The originals are still on Explorer at their pre-archive paths,
`/scratch/$USER/gnn-flu/Code/results/_ablation/h{01,02,04}_s10/`. A blanket
`Code/sweep/sync.sh pull` copies `Code/results/` wholesale and will recreate
`_ablation/h01_s10/` and friends at the top level, next to the archive rather
than inside it — which looks like a live study and is not one. Verified
identical to the copies here (24 leaf files, byte-for-byte), so nothing is at
risk; it is only confusing. Either delete the remote copies once you are happy,
or pull the one subtree you want:

    rsync -avz --include '*/' --include 'metrics.csv' --include 'predictions.csv' \
      --include 'run_config.json' --include 'seed_spread.csv' --exclude '*' \
      biggs.m@login.explorer.northeastern.edu:/scratch/biggs.m/gnn-flu/Code/results/_ablation/main/ \
      Code/results/_ablation/main/
