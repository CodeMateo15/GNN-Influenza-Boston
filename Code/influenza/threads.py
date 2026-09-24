"""Pin BLAS and OpenMP to one thread. Must be imported BEFORE numpy or torch.

`training.seed_everything` calls `torch.set_num_threads(1)`, which caps torch's
own intra-op pool and nothing else. numpy's linear algebra goes through a
separate BLAS -- Accelerate on macOS, OpenBLAS or MKL on Linux -- whose thread
count is read from the environment *at import time*. Setting it afterwards has
no effect, which is why this is a module imported first rather than a function
called later.

Two reasons it matters, and the second is the one that bites quietly:

1. Oversubscription. Each run was spawning about 20 threads, so a dozen
   concurrent arms on a 10-core machine drove the load average past 25 and made
   the machine unusable while running roughly as fast as four well-behaved jobs.

2. Reproducibility. Multithreaded reductions sum in a nondeterministic order, so
   two runs of the same seed can differ in the last bits. Because early stopping
   compares validation losses, a float tie broken differently selects a
   different epoch -- a different model -- with nothing in the metrics to show
   it. The SLURM script already exported these; local runs did not, so only the
   cluster was actually getting the guarantee.

Respects values already set, so a caller who genuinely wants threads can ask.
"""

from __future__ import annotations

import os

VARS = (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",   # Accelerate, i.e. numpy on macOS
)


def pin(n: int = 1) -> None:
    for name in VARS:
        os.environ.setdefault(name, str(n))


pin()
