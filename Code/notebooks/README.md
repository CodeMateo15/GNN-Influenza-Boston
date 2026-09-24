# Notebooks — frozen historical record

These notebooks produced the results recorded in
[`../docs/EDGES_AND_NODES_NOTES.txt`](../docs/EDGES_AND_NODES_NOTES.txt).
They are **no longer the source of truth** and are not maintained.

The Python scripts in `Code/` replaced them. Three notebooks that differed in
only six cells collapsed into one `run_gnn.py` plus an entry in the `EXPERIMENTS`
registry in `influenza/config.py`:

| Notebook | Was replaced by |
|---|---|
| `Boston_Influenza_GNN_PostCovid.ipynb` | `--experiment gnn_geo` |
| `Boston_Influenza_GNN_V2_CorrBinary.ipynb` | `--experiment gnn_corrbinary` |
| `Boston_Influenza_GNN_V2_MultiEdge.ipynb` | `--experiment gnn_multiedge` |
| `archive/Boston_Influenza_GNN_V2_UniformComplete.ipynb` | `--experiment gnn_uniform` |

**Those four arms no longer exist.** They were the `gcn_fusion` family, retired
once `gnn_st` beat all of them at every horizon; the table is kept so the
notebook lineage stays traceable through git history. The current graph model is
`run_gnn.py --experiment gnn_st`.

`archive/` holds earlier variants that predict normalized **levels** rather than
week-over-week **deltas**, so their numbers were never comparable with the three
active notebooks above.

## They will not run as-is

Two things break on re-execution, both deliberately left alone:

1. **Paths.** They resolve data with `os.path.join('..', 'Data')`, which was
   correct when they sat in `Code/`. From `Code/notebooks/` it needs to be
   `../../Data`. Fixing this would imply they are still maintained.
2. **Results would differ anyway.** The loader they share with the old baselines
   had two defects — it averaged an ILI *count* row together with the *rate* row,
   and it turned suppressed weeks into hard zeros. Both are fixed in
   `influenza/data.py`. See [`../docs/DATA_NOTES.md`](../docs/DATA_NOTES.md).

Read them for the modelling history and the visualisations. Run `Code/*.py` for
results.
