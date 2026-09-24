#!/bin/bash
# Push code and data to Explorer, and pull leaf artifacts back.
#
#   Code/sweep/sync.sh push <nuid>
#   Code/sweep/sync.sh pull <nuid>
#
# Code/results/ (128 MB, 1037 tracked files) is excluded INBOUND: the cluster
# produces results, it should not receive the laptop's.
set -euo pipefail
MODE="${1:?push or pull}"
NUID="${2:?your NU username}"
HOST="login.explorer.northeastern.edu"
REMOTE="/scratch/$NUID/gnn-flu"
LOCAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

case "$MODE" in
  push)
    rsync -avz --delete \
      --exclude '.git/' \
      --exclude 'Data/Weather copy/' \
      --exclude 'Code/results/' \
      --exclude 'Code/checkpoints/' \
      --exclude 'Citation Papers/' \
      --exclude 'Writings/' \
      --exclude '__pycache__/' \
      --exclude '.DS_Store' \
      "$LOCAL/" "$NUID@$HOST:$REMOTE/"
    ;;
  pull)
    # Leaf artifacts only. A full sweep is ~300 KB per run; at a few thousand
    # runs the checkpoints and plots are gigabytes that any run reproduces.
    rsync -avz \
      --include '*/' \
      --include 'metrics.csv' \
      --include 'predictions.csv' \
      --include 'predictions_val.csv' \
      --include 'run_config.json' \
      --include 'seed_spread.csv' \
      --exclude '*' \
      "$NUID@$HOST:$REMOTE/Code/results/" "$LOCAL/Code/results/"
    ;;
  *) echo "usage: sync.sh {push|pull} <nuid>" >&2; exit 2 ;;
esac
