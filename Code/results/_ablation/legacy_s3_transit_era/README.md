# Three-seed ablation, superseded — do not cite

Formerly `_ablation/ablation_s3.{csv,md}` and `_ablation/h{02,04}_s3/`.
Superseded by `_ablation/ablation_main_s10.{csv,md}`. Kept only as a record that
the study was run. Four faults, all of which the current driver now prevents:

1. **Two arms measured nothing.** `gnn_st_noglobals` and `gnn_st_noseason` were
   config-identical to `gnn_st` — the default already had `globals_=()` and
   `use_seasonality=False`. Their rows, including the table's strongest feature
   verdict (`noglobals`, +0.024, "better without it"), are seed noise between two
   identical models. `run_ablation.identity_guard` now refuses to run such an arm.
2. **The reference was not one model.** 20 of 23 arms were fit on the 108-edge
   transit-era graph with 3 global covariates; the four graph arms were fit on
   the current 107-edge graph with none. Every arm ran a 300-epoch budget that
   the V2 promotion has since cut to 120. `run_ablation.check_comparability` now
   asserts these match across arms and warns in the report if they do not.
3. **The noise floor was inferred from the arm list**, not measured, so it moved
   from 0.007 to 0.013 when arms were added. The study is now run with two extra
   reference ensembles on disjoint seed blocks and the floor is their spread.
4. **Five trained arms were invisible** — `nodemofeat`, `nodemoedge`,
   `nodemo_noglobals`, `lean`, `minimal` were in no group tuple, so they landed
   in the CSV and were dropped from the markdown. Three were nonetheless quoted
   in METHODS.md. `nodemo_noglobals` and `minimal` are also duplicates of
   `nodemo` now that globals are empty; the duplicate check catches that.

Three seeds was in any case too few to conclude anything about a feature group
here — the original study said so itself, and that judgement stands.
