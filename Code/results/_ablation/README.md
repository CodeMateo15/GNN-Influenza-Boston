# Ablations

## `ablation_main_s10.{csv,md}` — the current study, read this one

22 arms plus three reference ensembles, 10 seeds each, horizons 1/2/4, one code
version and one graph. 75 runs. Regenerate the tables from the artifacts without
retraining:

    python Code/run_ablation.py --collect-only --horizons 1,2,4 --n-seeds 10 --study main

Per-run artifacts are in `main/h{01,02,04}_s10/<arm>/post_covid/` —
`metrics.csv`, `predictions.csv`, `seed_spread.csv`, `run_config.json`,
`loss_curve.png` and the `actual_vs_predicted_horizon<N>.png` grid.

**The floor is measured, not assumed.** `gnn_st`, `gnn_st_ref_b` (seed 142) and
`gnn_st_ref_c` (seed 242) are the same configuration on disjoint seed blocks, and
the range of their three scores is the threshold: 0.003 at h=1, 0.006 at h=2,
0.031 at h=4. Earlier studies used a *per-seed* spread (0.015 / 0.05) as an
*ensemble* threshold, which is too conservative by 2-5x and hid real effects.

Read the `nbhds improved` and `p` columns next to the floor. At h=4 the floor is
inflated by one reference ensemble landing at 0.613 against 0.582 and 0.587, so
little clears it, while the paired per-neighborhood test finds several effects
moving 13 or 14 of 14 neighborhoods the same way.

## `_charts/` — side-by-side overlays

One directory per question, shared y-scale so they compare by eye. Built with the
existing plotter, e.g.

    python Code/plot_forecasts.py --results-dir Code/results/_ablation/main/h04_s10 \
      --out-dir Code/results/_ablation/_charts/does_the_graph_pay_h4 \
      --horizon 4 --models gnn_st,gnn_st_nograph,gnn_st_wastewater

| directory | question |
| --- | --- |
| `does_the_graph_pay_h2/` | Graph vs. no graph vs. no weather at 2 weeks. The graph is worth 0.093 here and no neighborhood prefers it gone. |
| `does_the_graph_pay_h4/` | Same at 4 weeks. `gnn_st` and `gnn_st_nograph` sit on top of each other — the graph has stopped paying. |
| `what_to_add_h4/` | Wastewater and vaccination against the default. Both turn up earlier than the default and track the rise better. |
| `what_to_drop_h4/` | Dropping demographic features and correlation edges. Both *improve* 13-14 of 14 neighborhoods at h=4. |
| `lagsonly_vs_default/` | Flu lags only, and lags+flag+graph, against the default at h=2. Both lose; weather is doing the work. |

## Archived, do not cite

`legacy_s3_transit_era/` — the three-seed study. Superseded and internally
inconsistent; see its README for the four specific faults.

`transit_retirement/` — the `gnn_st_transit` measurement of record. Cannot be
regenerated; the arm is gone from `EXPERIMENTS`.
