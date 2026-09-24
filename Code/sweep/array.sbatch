#!/bin/bash
# CPU job array for the model sweep on Explorer.
#
# Why CPU and not GPU: one arm is ~16k parameters trained on 122 origins over a
# 21-node graph, which is seconds of arithmetic. The cost here is BREADTH --
# seeds x horizons x arms x seasons x 2 cities -- which is embarrassingly
# parallel and belongs in an array, not on an accelerator.
#
# Discover the real partitions before trusting the values below; the RC docs do
# not publish them:
#     sinfo -o "%20P %10l %10L %6D %8G %10m %C"
#     scontrol show partition short
#
#     sbatch --export=ALL,CHUNK=20 Code/sweep/array.sbatch
#
# A different task list, sized to its own length:
#     sbatch --export=ALL,CHUNK=2,TASKS=Code/sweep/tasks_ablation.jsonl \
#            --array=0-37%50 Code/sweep/array.sbatch
#
#SBATCH --job-name=gnnflu
#SBATCH --partition=short
#SBATCH --array=0-19%50
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=03:00:00
#SBATCH --output=logs/out_%A_%a.log
#SBATCH --error=logs/err_%A_%a.log
set -euo pipefail

ROOT="${GNNFLU_ROOT:-/scratch/$USER/gnn-flu}"
# A plain venv, NOT a conda prefix: `conda create --prefix` fails silently on
# Explorer (Code/env/environment.yml:1-17), so the env is built with python -m
# venv and must be activated with its own activate script. The old default here
# pointed at /projects/$USER/gnn-flu/env, which does not exist.
ENVDIR="${GNNFLU_ENV:-$HOME/envs/gnn-flu}"
CHUNK="${CHUNK:-20}"
TASKS="${TASKS:-Code/sweep/tasks.jsonl}"

module purge
module load explorer anaconda3/2024.06
source "$ENVDIR/bin/activate"

# Single-threaded on purpose, for two reasons. At this model size torch's
# intra-op threading is pure overhead. More importantly, multithreaded
# reductions sum in a nondeterministic order, and because early stopping
# compares validation losses, a float tie broken differently selects a different
# epoch -- i.e. a different model -- with no visible sign in the metrics.
# Belt and braces: Code/influenza/threads.py pins these inside the process too,
# before numpy is imported, so a run launched any other way is also pinned.
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PYTHONHASHSEED=0
export MPLBACKEND=Agg          # compute nodes have no display

mkdir -p "$ROOT/logs"
cd "$ROOT"

# --no-carbon is MANDATORY here. influenza/carbon.py appends to one shared
# results/_emissions/emissions.csv; 50 concurrent writers corrupt it. Measure
# emissions in a single serial local run instead.
python -u Code/sweep.py run \
  --tasks   "$TASKS" \
  --start   "$(( SLURM_ARRAY_TASK_ID * CHUNK ))" \
  --count   "$CHUNK" \
  --log     "$ROOT/logs/task_${SLURM_ARRAY_TASK_ID}.csv" \
  --no-carbon \
  --skip-existing
