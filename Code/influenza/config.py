"""Experiment configuration.

The three notebooks this replaced differed in only six cells, so model variants
are a configuration problem, not an abstraction problem. Each variant is one
frozen `Experiment` in the `EXPERIMENTS` registry below; the CLI applies
`dataclasses.replace` for the handful of knobs worth exposing, and the resolved
object is serialised into every run's `run_config.json`.

Every feature added after the original 22-feature baseline defaults to OFF, so
the baseline stays reproducible and each addition is a clean ablation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Literal

import pandas as pd

from .constants import HORIZONS, LOOKBACK, MC_SEED, SEED, TEST_END, TEST_START
from .windows import Window

# No city-wide covariate by default.
#
# Two rounds of measurement got here. Four of the five city-wide files stop on
# 2025-12-28, one week past the season peak, and leave 15-16 of the 49
# evaluation weeks unobserved; they were retired first. That left `ili_ed_perc`,
# which after defect 6 is fixed does cover the whole series -- and which then
# measured as doing nothing: +0.010 macro Corr at two weeks ahead and about zero
# at one and four, as a 10-seed ensemble.
#
# It is dropped on parsimony rather than accuracy. In this repository the
# city-wide covariates are where the bugs live: four of the five defects in
# DATA_NOTES.md were in covariate loading and none touched `load_rates`. A group
# that contributes nothing measurable but has already carried a frozen tail, a
# look-ahead and a forward-matching error is a bad trade at 122 training
# origins. `gnn_st_globals` adds it back as an ablation, so the decision stays
# testable rather than baked in.
DEFAULT_GLOBALS: tuple[str, ...] = ()

# The five city-wide covariates as they were before any of this. Kept so
# GLOBAL_CHOICES still validates their names and an ablation can ask for them.
LEGACY_GLOBALS = ("ili_count", "ed_count", "ili_ed_perc", "flu_cases", "monthly_cases")
# The UNION across cities. FeatureSpec only checks that a name is spelled
# correctly; whether a given city can actually supply it is checked against
# City.available_globals in samples.load_dataset, which is where the failure is
# actionable ("Columbus has no ed_count") rather than merely syntactic.
GLOBAL_CHOICES = (*LEGACY_GLOBALS, "vaccination", "hospitalizations")

# 'seven' is Boston's anchor count and survives as the historical spelling in
# every committed run_config.json; 'full' is the city-neutral synonym for the
# same thing -- use this city's complete anchor set, whatever its size.
AnchorScheme = Literal["none", "single", "seven", "full"]


@dataclass(frozen=True)
class FeatureSpec:
    """Which node features and city-wide covariates are active.

    Flu lags are always on -- they are the autoregressive signal.
    """

    # Original baseline feature groups.
    use_weather: bool = True
    use_demographics: bool = True
    use_wastewater: bool = False

    # Added later; default OFF so each is an ablation against the baseline.
    use_covid_cases: bool = False
    use_covid_testing: bool = False
    use_covid_wastewater: bool = False
    use_rsv_cases: bool = False
    use_rsv_wastewater: bool = False
    use_rt: bool = False

    # Sine and cosine of the target week's position in the year, added to the
    # city-wide covariates. Not a prediction -- the calendar is known at forecast
    # time -- but at horizons of a quarter-cycle or more it is the only thing
    # telling the model which side of the peak it is aiming at. An 8-week
    # lookback cannot distinguish a rising November from a falling February.
    use_seasonality: bool = False

    # Marks weeks whose flu rate was imputed because BPHC suppressed the count.
    use_imputed_flag: bool = False

    globals_: tuple[str, ...] = DEFAULT_GLOBALS

    def __post_init__(self) -> None:
        unknown = set(self.globals_) - set(GLOBAL_CHOICES)
        if unknown:
            raise ValueError(f"Unknown global covariates: {sorted(unknown)}")

    @property
    def monthly_sources(self) -> tuple[str, ...]:
        active = []
        if self.use_covid_cases:
            active.append("covid_cases")
        if self.use_covid_testing:
            active.append("covid_testing")
        if self.use_rsv_cases:
            active.append("rsv_cases")
        return tuple(active)

    @property
    def wastewater_sources(self) -> tuple[str, ...]:
        active = []
        if self.use_wastewater:
            active.append("influenza")
        if self.use_covid_wastewater:
            active.append("covid")
        if self.use_rsv_wastewater:
            active.append("rsv")
        return tuple(active)


@dataclass(frozen=True)
class GraphSpec:
    """Which edge types exist and how they are weighted.

    Overlapping edge types accumulate into one weight matrix W, except when
    `dual` is set, in which case the geographic and correlation topologies are
    kept as two separate adjacencies (the paper's dual-channel design).
    """

    anchors: AnchorScheme = "seven"

    geo: bool = True
    geo_max_hop: int = 1
    geo_decay: float = 0.5

    corr: bool = False
    corr_threshold: float = 0.85
    corr_binary: bool = True
    corr_coef: float = 1.0

    demo: bool = False
    demo_threshold: float = 0.5
    demo_coef: float = 1.0

    uniform_complete: bool = False
    dual: bool = False

    def n_anchors(self, city=None) -> int:
        """How many anchor nodes this scheme yields for a given city.

        Was a property returning a hardcoded 7. Boston has 7 anchors and
        Columbus 3, so the count has to come from the city. Nothing in the
        codebase read the old property -- Graph.n_anchors is computed from the
        built node list -- so this is a widening, not a breaking change.
        """
        if self.anchors == "none":
            return 0
        if self.anchors == "single":
            return 1
        if city is None:
            raise ValueError("n_anchors needs a city for the 'seven'/'full' schemes.")
        return city.n_anchors


@dataclass(frozen=True)
class TrainSpec:
    lr: float = 3e-3
    weight_decay: float = 1e-5
    epochs: int = 120
    batch_size: int | None = None  # None = per-sample updates (notebook parity)
    plateau_factor: float = 0.5
    plateau_patience: int = 10
    early_stop_patience: int = 25
    grad_clip: float = 1.0
    dropout: float = 0.2
    hidden: tuple[int, ...] = (64, 32, 32)  # gcn1, gcn2, fusion
    seed: int = SEED
    mc_samples: int = 100
    mc_seed: int = MC_SEED

    # --- SpatioTemporalGNN only. Every default reproduces existing behaviour, so
    # --- adding these fields moves no committed number.
    optimizer: Literal["adam", "adamw"] = "adam"
    schedule: Literal["plateau", "cosine"] = "plateau"
    channels: int = 24
    dilations: tuple[int, ...] = (1, 2, 4, 8)
    adaptive_dim: int = 8
    adaptive: bool = True
    drop_edge: float = 0.0
    n_blocks: int = 2
    # 0.0 = plain masked MSE, which is what every legacy arm uses.
    huber_delta: float = 0.0
    pearson_weight: float = 0.0
    # Weight rising with how far the epidemic moved over the horizon, to make
    # being late expensive. A squared-error loss prices height and not timing,
    # so when the turn date is uncertain the risk-minimising forecast is a
    # smoothed, slightly late peak -- and every model here is one to two weeks
    # late (Code/compare_timing.py). 0.0 is the unweighted loss every committed
    # arm uses; 1.0 gives an average-sized move twice the weight of a
    # stationary week. Model selection stays unweighted either way.
    slope_weight: float = 0.0
    # Members are seed .. seed + n_seeds - 1. The h=4 per-seed standard deviation
    # is 0.052 macro Corr -- larger than any single architecture change measured
    # -- so a one-seed number at that horizon is not separable from a lucky draw.
    n_seeds: int = 1
    # Which Graph.relations to feed the mixer. ("all",) is the summed adjacency.
    relations: tuple[str, ...] = ("all",)
    # Graph convolution. "gat" swaps degree-normalised averaging for learned
    # attention. No registry arm uses it: the ablation was run once and attention
    # measured inside the noise floor of GCN at every horizon (see METHODS.md),
    # so carrying an arm for it only clutters the leaderboard. The code path
    # stays so the recorded number is reproducible with
    # `--experiment gnn_st` plus a TrainSpec override. The paper's GAT is a
    # separate standalone baseline, `gat` / run_gat.py -- not this.
    conv: Literal["gcn", "gat"] = "gcn"
    heads: int = 4


@dataclass(frozen=True)
class Experiment:
    name: str
    model: Literal["gcn_fusion", "stgnn", "dualtopo", "gat"] = "gcn_fusion"
    variant: str = "post_covid"
    target: Literal["delta", "level", "blend", "trendblend", "cascade"] = "delta"
    normalize: Literal["all", "train"] = "train"
    features: FeatureSpec = field(default_factory=FeatureSpec)
    graph: GraphSpec = field(default_factory=GraphSpec)
    train: TrainSpec = field(default_factory=TrainSpec)
    window: Window = field(default_factory=Window)
    note: str = ""

    def to_json(self) -> dict:
        payload = asdict(self)
        payload["window"] = self.window.to_json()
        payload["features"]["globals_"] = list(self.features.globals_)
        payload["train"]["hidden"] = list(self.train.hidden)
        payload["train"]["dilations"] = list(self.train.dilations)
        payload["train"]["relations"] = list(self.train.relations)
        return payload


# ---------------------------------------------------------------------------
# Registry. Each name becomes a results/<name>/<variant>/ directory.
# ---------------------------------------------------------------------------

def _experiments() -> dict[str, Experiment]:
    dualtopo = Experiment(
        name="dualtopo",
        model="dualtopo",
        target="level",
        normalize="train",
        features=FeatureSpec(use_weather=False, use_demographics=False, globals_=()),
        graph=GraphSpec(anchors="seven", geo_max_hop=1, corr=True, corr_binary=False,
                        dual=True),
        train=TrainSpec(lr=3e-3, batch_size=26, plateau_factor=0.2, plateau_patience=5,
                        early_stop_patience=20, hidden=(16, 64)),
        window=Window(lookback=52, horizons=(1,)),
        note="Paper-faithful Dual-Topo-STGCN (Luo et al. 2025, BMC Public Health "
             "25:408). ILI rates only, two separate topologies, 52-week input.",
    )

    # The paper's OTHER graph comparison model, standalone in the same sense
    # dualtopo is. Luo et al. place it last at Corr 0.5994. ILI rates only, the
    # same 52-week window they state they used for every comparison model, and
    # no temporal encoder -- which is the whole point of keeping it separate from
    # gnn_st_gat, the ablation that puts attention *inside* our architecture.
    gat = Experiment(
        name="gat",
        model="gat",
        target="level",
        normalize="train",
        features=FeatureSpec(use_weather=False, use_demographics=False, globals_=()),
        graph=GraphSpec(anchors="seven", geo_max_hop=1, corr=True, corr_binary=False),
        train=TrainSpec(lr=3e-3, batch_size=26, plateau_factor=0.2, plateau_patience=5,
                        early_stop_patience=20, hidden=(64, 8)),  # hidden width, heads
        window=Window(lookback=52, horizons=(1,)),
        note="Graph Attention Network baseline (Luo et al. 2025 comparison model, "
             "reported Corr 0.5994). Plain spatial GAT over ILI history with no "
             "temporal encoder, 52-week input, level target.",
    )

    registry = {
        experiment.name: experiment
        for experiment in (dualtopo, gat)
    }


    # ------------------------------------------------------------------
    # Cross-city arms. Boston's published arms use five BPHC city-wide
    # covariates that Columbus has no equivalent for, so running a Boston arm
    # unchanged in both cities would compare two different models and call the
    # difference a city effect. These arms are restricted to what BOTH cities can supply
    # identically -- flu lags, weather, static demographics, and `ili_count` as
    # the single city-wide covariate -- so a Boston/Columbus difference is
    # attributable to the city rather than to the feature set.
    #
    # They deliberately do NOT replace the Boston arms in METHODS.md, which stay
    # as the best Boston model rather than the most portable one.
    # ------------------------------------------------------------------
    xcity_features = FeatureSpec(use_weather=True, use_demographics=True,
                                 globals_=("ili_count",))
    xcity_note = ("Cross-city arm: only features Boston and Columbus can both "
                  "supply (flu lags, weather, demographics, ili_count). ")
    registry["xcity_geo"] = Experiment(
        name="xcity_geo", features=xcity_features,
        graph=GraphSpec(anchors="single", geo_max_hop=1),
        note=xcity_note + "Geographic 1-hop adjacency only.",
    )
    registry["xcity_corrbinary"] = Experiment(
        name="xcity_corrbinary", features=xcity_features,
        graph=GraphSpec(anchors="full", geo_max_hop=1, corr=True, corr_binary=True),
        note=xcity_note + "Geographic plus binary thresholded correlation edges.",
    )
    registry["xcity_multiedge"] = Experiment(
        name="xcity_multiedge", features=xcity_features,
        graph=GraphSpec(anchors="full", geo_max_hop=3, corr=True, corr_binary=False,
                        demo=True),
        note=xcity_note + "Hop-graded geographic, weighted correlation and "
                          "demographic-similarity edges.",
    )
    registry["xcity_uniform"] = Experiment(
        name="xcity_uniform", features=xcity_features,
        graph=GraphSpec(anchors="full", uniform_complete=True),
        note=xcity_note + "Control: every pair connected at weight 1.",
    )
    registry["xcity_dualtopo"] = replace(
        dualtopo, name="xcity_dualtopo",
        graph=replace(dualtopo.graph, anchors="full"),
        note=xcity_note + "Dual-Topo-STGCN, ILI rates only, 52-week input.",
    )

    # ------------------------------------------------------------------
    # SpatioTemporalGNN. The headline arm, and the reason this file grew a
    # second model type. Its differences from the superseded gcn_fusion arms are,
    # in measured order of value: a real temporal axis over the lookback; an
    # optimisation
    # setup that actually trains (the old arm early-stopped at epoch 4 of 29);
    # and a target measured from a blend of the origin level and the seasonal
    # climatology rather than from the origin level alone.
    #
    # Three things deliberately left OFF because they measured negative:
    #   - separate per-relation adjacencies (-0.023 macro at h=2) -> relations=("all",)
    #   - a joint multi-horizon head (-0.027 at h=2, -0.045 at h=4) -> horizons=(1,)
    #   - the `full` variant's extra history (-0.097 macro at h=2) -> post_covid
    # Each ships as an ablation arm below so the negative results are recorded.
    # ------------------------------------------------------------------
    # No calendar sin/cos either. Unlike the city-wide covariate this one is
    # redundant by construction, not just by measurement: the blended target
    # already subtracts a harmonic regression on day-of-year at k = 1, 2, 3, and
    # woy_sin/woy_cos are the k = 1 terms of exactly that basis. Measured at
    # +0.001 macro Corr, which is what a strict subset should score.
    st_features = FeatureSpec(use_weather=True, use_demographics=True,
                              use_imputed_flag=True, use_seasonality=False,
                              globals_=DEFAULT_GLOBALS)
    st = Experiment(
        name="gnn_st", model="stgnn", target="blend", normalize="train",
        variant="post_covid",
        features=st_features,
        # Three edge types: hop-graded geographic, weighted correlation, and
        # demographic similarity. A fourth -- MBTA transit -- was measured and
        # retired; see docs/METHODS.md, "Transit (retired)".
        graph=GraphSpec(anchors="seven", geo_max_hop=3, corr=True, corr_binary=False,
                        demo=True),
        # Budget, dropout and weight decay are the V2 settings, promoted after
        # measuring them in two cities at two horizons. Against the previous
        # 300 / 0.15 / 1e-3: macro Corr unchanged everywhere (within 0.006), but
        # RMSE improved in 4 of 4 city-horizon cells (-0.31 and -1.16 in Boston,
        # -0.05 and -0.22 in Columbus) and interval coverage improved in 4 of 4.
        # Runtime fell about 2.5x.
        #
        # The motivation was the loss curves, not a test-set search: the median
        # best epoch was 55-66 of 300, so ~80% of the old budget ran after the
        # checkpoint that was kept and while validation was rising, and train
        # loss sat 4-5x below validation on 115 training origins.
        #
        # Columbus gained less than Boston, which is the predicted direction --
        # it has 28% more training cells, so less overfitting for the extra
        # regularisation to remove. An effect that scales with the problem it
        # claims to fix is more believable than one that does not.
        train=TrainSpec(lr=3e-3, weight_decay=3e-3, epochs=120, batch_size=16,
                        dropout=0.25, optimizer="adamw", schedule="cosine",
                        channels=24, dilations=(1, 2, 4, 8), adaptive=True,
                        huber_delta=1.0, pearson_weight=0.3, n_seeds=10,
                        early_stop_patience=10_000, relations=("all",)),
        window=Window(lookback=16, horizons=(1,)),
        note="Multi-relational spatio-temporal GNN: dilated causal temporal "
             "convolutions per node, graph mixing with a learned adaptive "
             "adjacency, and a residual measured from a learned blend of the "
             "origin level and a train-only harmonic climatology.",
    )
    registry[st.name] = st

    registry["gnn_st_1seed"] = replace(
        st, name="gnn_st_1seed", train=replace(st.train, n_seeds=1),
        note=st.note + " Single seed, to show the per-seed spread the ensemble hides.")
    registry["gnn_st_noadapt"] = replace(
        st, name="gnn_st_noadapt", train=replace(st.train, adaptive=False),
        note=st.note + " Adaptive adjacency removed.")
    registry["gnn_st_relations"] = replace(
        st, name="gnn_st_relations",
        train=replace(st.train, relations=("geo", "corr", "demo")),
        note=st.note + " Edge types kept as separate gated relations instead of "
             "summed. Measured WORSE than summing; kept so that is on the record.")
    # --- timing arms -----------------------------------------------------
    # Both attack the same measured defect from opposite ends: at h=2 `gnn_st`
    # fits the truth best when slid one week earlier, 63% of its squared error
    # goes away under that shift, and its residual correlates -0.80 with the
    # week-over-week change in the truth. `slopeweight` changes what the loss
    # charges for; `trendblend` changes what the residual is measured from.
    # Kept as two arms rather than one so it stays readable which of the two
    # moved the timing.
    registry["gnn_st_slopeweight"] = replace(
        st, name="gnn_st_slopeweight",
        train=replace(st.train, slope_weight=1.0),
        note=st.note + " Loss weighted by how far the epidemic moved over the "
             "horizon, so standing still stops being the cheap hedge against an "
             "uncertain turn date. Measured WORSE and is kept so that is on the "
             "record: at h=2 it went from one week late to two, RMSE 17.21 -> "
             "18.37 and macro Corr 0.802 -> 0.785, while the lag fingerprint "
             "barely moved (-0.801 -> -0.794). The mechanism is visible in its "
             "own run_config: the learned origin share ROSE from 0.674 to 0.713, "
             "so charging more for the moving cells made the model lean harder "
             "on persistence -- the opposite of the intent.")
    registry["gnn_st_trendblend"] = replace(
        st, name="gnn_st_trendblend", target="trendblend",
        note=st.note + " The origin half of the blended baseline is extrapolated "
             "along the recent trend instead of held flat, by a learned and "
             "sigmoid-bounded share -- so the anchor is not h weeks stale. "
             "Measured as a NULL result and kept for the record: at h=2 the lag "
             "fingerprint is -0.807 against the reference's -0.801, still one "
             "week late, RMSE 17.39 against 17.21. The bound did its job -- the "
             "model learned a trend share of only 0.167, i.e. it largely declined "
             "to extrapolate, which agrees with the separate finding that adding "
             "the observed slope to the forecast directly makes RMSE worse at "
             "every weight.")
    # The h=2 arm. Trains horizons 1 and 2 together and anchors the h=2 baseline
    # on the model's own h=1 forecast instead of the origin level -- one week
    # fresher, from the same origin, at no extra cost. Aimed squarely at the
    # finding that 63% of the squared error at h=2 is timing rather than height.
    #
    # Note this scores 48 target weeks, not 49: test membership is decided by the
    # SHORTEST horizon, so with horizons=(1, 2) the last h=2 target falls outside
    # the window. Compare it against `gnn_st` re-scored on the same 48 weeks, not
    # against the committed 49-week number.
    # The evaluation window is shifted one week EARLIER than the project default,
    # and that is what keeps this arm comparable. Test membership is decided by
    # the shortest horizon, so a horizons=(1, 2) arm on the default window scores
    # 48 h=2 target weeks instead of the canonical 49 and the error-growth curve
    # stops comparing like with like. Moving the window back one week puts the
    # h=2 targets exactly on 2025-06-01..2026-05-03, which is asserted in the
    # verification notes and checked directly against the committed predictions.
    cascade_window = replace(st.window, horizons=(1, 2),
                             test_start=TEST_START - pd.Timedelta(weeks=1),
                             test_end=TEST_END - pd.Timedelta(weeks=1))
    registry["gnn_cascade"] = replace(
        st, name="gnn_cascade", target="cascade",
        window=cascade_window,
        note=st.note + " Horizons 1 and 2 trained jointly, with the h=2 baseline "
             "anchored on the model's own h=1 forecast rather than the two-week-old "
             "origin level. DID NOT REPLICATE: a first batch scored 16.66 RMSE / 0.822 "
             "macro against the reference's 17.38 / 0.800, but re-trained with the "
             "window shifted one week -- one fewer training origin -- the same arm "
             "scores 17.43 / 0.801 on those same weeks, i.e. the reference. A 10-seed "
             "ensemble at h=2 moves ~0.7 RMSE between runs, which is the whole claimed "
             "effect. Kept as the measured noise floor, not as an improvement. The lag "
             "is untouched either way.")
    registry["gnn_st_joint"] = replace(
        st, name="gnn_st_joint", target="blend",
        window=cascade_window,
        note=st.note + " Horizons 1 and 2 trained jointly with the ordinary blended "
             "baseline. The control for gnn_st_cascade: without it, a cascade gain "
             "cannot be told apart from whatever training two horizons together does "
             "on its own. Its first-batch 16.79 RMSE / 0.817 macro looked like it "
             "carried the whole gain, but the cascade arm failed to replicate at that "
             "level, so this number is subject to the same caveat. At h=4 the joint "
             "arms are clearly worse (see gnn_st_joint_h4), which agrees with the older "
             "finding that a joint multi-horizon head costs 0.03 to 0.05.")
    # The same idea one horizon further out: anchor h=4 on the model's own h=2
    # forecast. The window shifts by TWO weeks here, because test membership is
    # decided by the shortest horizon in the arm and that is now 2, so this is
    # what puts the h=4 targets back on the canonical 49 weeks.
    cascade4_window = replace(st.window, horizons=(2, 4),
                              test_start=TEST_START - pd.Timedelta(weeks=2),
                              test_end=TEST_END - pd.Timedelta(weeks=2))
    registry["gnn_cascade_h4"] = replace(
        st, name="gnn_cascade_h4", target="cascade", window=cascade4_window,
        note=st.note + " Horizons 2 and 4 trained jointly, with the h=4 baseline "
             "anchored on the model's own h=2 forecast rather than the four-week-old "
             "origin level.")
    registry["gnn_st_joint_h4"] = replace(
        st, name="gnn_st_joint_h4", target="blend", window=cascade4_window,
        note=st.note + " Horizons 2 and 4 trained jointly with the ordinary blended "
             "baseline. The control for gnn_cascade_h4.")
    registry["gnn_st_delta"] = replace(
        st, name="gnn_st_delta", target="delta",
        note=st.note + " Residual from the origin level only -- the old "
             "parameterisation, for comparison against the blend.")
    registry["gnn_st_level"] = replace(
        st, name="gnn_st_level", target="level",
        note=st.note + " Level target, no baseline at all.")
    registry["gnn_st_noglobals"] = replace(
        st, name="gnn_st_noglobals",
        features=replace(st_features, globals_=()),
        note=st.note + " No city-wide covariate. Tests whether ili_ed_perc earns "
             "its place now that it is read from the file that covers the whole "
             "series rather than carried forward from the shorter one.")
    registry["gnn_st_nopearson"] = replace(
        st, name="gnn_st_nopearson", train=replace(st.train, pearson_weight=0.0),
        note=st.note + " Plain Huber loss, no correlation term.")
    registry["gnn_st_tiny"] = replace(
        st, name="gnn_st_tiny", train=replace(st.train, channels=16),
        note=st.note + " Narrower still, for the capacity curve.")
    registry["gnn_st_full"] = replace(
        st, name="gnn_st_full", variant="full",
        note=st.note + " Trained on the whole 436-week series including the COVID "
             "trough. More origins, measured worse.")
    registry["gnn_st_nodemo"] = replace(
        st, name="gnn_st_nodemo",
        features=replace(st_features, use_demographics=False),
        graph=replace(st.graph, demo=False),
        note=st.note + " No static demographics as features or as edges.")
    # ------------------------------------------------------------------
    # Feature ablations: leave one group out of `gnn_st`, plus a floor.
    #
    # Retrain-and-rescore rather than permutation importance, because several of
    # these groups are constant within a forecast origin -- static demographics
    # get exactly zero from expected-gradient attribution by construction, as
    # METHODS.md already notes, so the only rigorous test is to remove the group
    # and refit. Every arm below differs from `gnn_st` in one feature group.
    #
    # Two are expected to come out near zero, and the reason is recorded here so
    # the prediction is on the record before the run: mean temperature correlates
    # with week-of-year at R^2 = 0.93, and the calendar sin/cos pair is a strict
    # subset of the harmonic climatology the blended target already subtracts.
    # Both were standing in for a seasonal clock the model now has explicitly.
    # ------------------------------------------------------------------
    registry["gnn_st_noweather"] = replace(
        st, name="gnn_st_noweather",
        features=replace(st_features, use_weather=False),
        note=st.note + " Weather removed (6 of 30 feature columns). Expected to "
             "cost little: temp_mean_c correlates with week-of-year at R^2=0.93, so "
             "weather was an implicit seasonal clock the climatology baseline now "
             "supplies directly.")
    registry["gnn_st_noseason"] = replace(
        st, name="gnn_st_noseason",
        features=replace(st_features, use_seasonality=False),
        note=st.note + " Calendar sin/cos removed. Expected to cost nothing: it is "
             "a subset of the harmonic climatology the target already subtracts.")
    registry["gnn_st_noimputedflag"] = replace(
        st, name="gnn_st_noimputedflag",
        features=replace(st_features, use_imputed_flag=False),
        note=st.note + " Suppression flag removed, so the model can no longer tell "
             "an imputed lag from an observed one.")
    registry["gnn_st_lagsonly"] = replace(
        st, name="gnn_st_lagsonly",
        features=FeatureSpec(use_weather=False, use_demographics=False,
                             use_imputed_flag=False, use_seasonality=False,
                             globals_=()),
        graph=replace(st.graph, demo=False),
        note=st.note + " Flu lags and the graph only -- no weather, demographics, "
             "calendar or city-wide covariate. The floor each feature group is "
             "measured against.")

    # Add-one-in arms for groups that default OFF. Worth re-measuring rather than
    # trusting the old numbers: covid wastewater carried a one-day look-ahead
    # (DATA_NOTES defect 7) and the monthly citywide series read the following
    # month on 89 of 436 weeks (defect 8), so the previously reported COVID/RSV
    # gain was measured on contaminated inputs.
    registry["gnn_st_covid_rsv"] = replace(
        st, name="gnn_st_covid_rsv",
        features=replace(st_features, use_covid_cases=True, use_rsv_cases=True,
                         use_covid_wastewater=True),
        note=st.note + " Plus monthly neighborhood COVID/RSV rates and COVID "
             "wastewater, re-measured after the look-ahead fixes.")
    # Decomposes gnn_st_covid_rsv. That arm adds three per-node channels at once
    # -- covid cases, rsv cases and covid WASTEWATER -- and measured a large
    # harm. Two explanations are live and the combined arm cannot separate them:
    # (a) the covid wastewater series was the one carrying the one-day
    # look-ahead of DATA_NOTES defect 7, so removing the leak removed a benefit
    # that was never real; (b) going from 2 to 5 temporal channels is 32 -> 80
    # temporal features on 122 training origins, i.e. plain overfitting.
    # This arm keeps the cases and drops the wastewater. If the harm persists it
    # is capacity; if it disappears it was the leak.
    registry["gnn_st_covid_rsv_cases"] = replace(
        st, name="gnn_st_covid_rsv_cases",
        features=replace(st_features, use_covid_cases=True, use_rsv_cases=True),
        note=st.note + " Monthly neighborhood COVID/RSV case rates only, without "
             "covid wastewater. Separates the leak explanation from the capacity "
             "explanation for gnn_st_covid_rsv's measured harm.")
    registry["gnn_st_covid_ww"] = replace(
        st, name="gnn_st_covid_ww",
        features=replace(st_features, use_covid_wastewater=True),
        note=st.note + " Covid wastewater only. The other half of the same split; "
             "this is the series that carried the one-day look-ahead.")

    registry["gnn_st_wastewater"] = replace(
        st, name="gnn_st_wastewater",
        features=replace(st_features, use_wastewater=True),
        note=st.note + " Plus flu wastewater. Coverage starts 2024-07-28, so it is "
             "present for all of test and under half of training -- read the result "
             "as underpowered rather than as a null.")
    registry["gnn_st_vaccination"] = replace(
        st, name="gnn_st_vaccination",
        features=replace(st_features, globals_=("vaccination",)),
        note=st.note + " Plus statewide vaccination uptake. Already implemented and "
             "already in GLOBAL_CHOICES, but no arm had ever switched it on.")


    # `gnn_st_nodemo` removes the demographic NODE FEATURES and the demographic
    # EDGES together, so its number cannot say which of the two mattered. These
    # two arms split it. Worth splitting because the edges and the features
    # answer different questions: whether *whose* demographics they are carries
    # signal, versus whether demographic similarity is a useful way to wire the
    # graph.
    # Add-backs for the two groups just dropped from the default, so both
    # decisions remain measurable rather than assumed.
    registry["gnn_st_globals"] = replace(
        st, name="gnn_st_globals",
        features=replace(st_features, globals_=("ili_ed_perc",)),
        note=st.note + " Adds the city-wide ILI share back. Dropped from the "
             "default on parsimony after measuring +0.010 macro at h=2 and about "
             "zero at h=1 and h=4 as a 10-seed ensemble.")
    registry["gnn_st_season"] = replace(
        st, name="gnn_st_season",
        features=replace(st_features, use_seasonality=True),
        note=st.note + " Adds the calendar sin/cos back. Redundant by "
             "construction with the harmonic climatology in the target.")

    # Edge-type ablations. The feature arms above ask what the NODE inputs are
    # worth; these ask what the WIRING is worth, which is the question the
    # project was set up to answer. The edge types are summed into one
    # adjacency, so a type's marginal effect is invisible in the default
    # configuration and only an arm that removes it can measure it.
    registry["gnn_st_nocorr"] = replace(
        st, name="gnn_st_nocorr",
        graph=replace(st.graph, corr=False),
        note=st.note + " Correlation edges removed (39 pairs). Also the arm that "
             "bounds how much of the result depends on graph structure fitted "
             "from the ILI series itself.")
    registry["gnn_st_geoonly"] = replace(
        st, name="gnn_st_geoonly",
        graph=replace(st.graph, corr=False, demo=False),
        note=st.note + " Geographic edges only -- shared borders, hop-decayed to 3 "
             "hops. The floor the other three edge types are measured against.")
    # Removing the hand-built edges is NOT enough to make the model graph-free:
    # the adaptive adjacency is itself a learned dense graph, so an arm with
    # geo/corr/demo all off still does spatial mixing. These two arms
    # split what that conflates.
    registry["gnn_st_adaptiveonly"] = replace(
        st, name="gnn_st_adaptiveonly",
        graph=replace(st.graph, geo=False, corr=False, demo=False,
                      anchors="none"),
        note=st.note + " No hand-built edges, but the learned adaptive adjacency "
             "stays. Asks whether the five hand-built edge types add anything "
             "over a graph the model infers for itself.")
    registry["gnn_st_nograph"] = replace(
        st, name="gnn_st_nograph",
        graph=replace(st.graph, geo=False, corr=False, demo=False,
                      anchors="none"),
        train=replace(st.train, adaptive=False),
        note=st.note + " Genuinely no spatial term: no hand-built edges AND no "
             "adaptive adjacency, so each neighborhood is forecast from its own "
             "history with shared weights. The honest floor for 'does the graph "
             "help at all', and the number that decides whether this is a graph "
             "problem. Removing the hand-built edges alone does not get here -- "
             "the adaptive adjacency would still be a learned graph.")

    registry["gnn_st_nodemofeat"] = replace(
        st, name="gnn_st_nodemofeat",
        features=replace(st_features, use_demographics=False),
        note=st.note + " Demographic node features removed, demographic edges KEPT. "
             "The half of gnn_st_nodemo that asks whether the 8 static columns "
             "carry signal as inputs.")
    registry["gnn_st_nodemoedge"] = replace(
        st, name="gnn_st_nodemoedge",
        graph=replace(st.graph, demo=False),
        note=st.note + " Demographic edges removed (60 of 247), node features KEPT. "
             "The half of gnn_st_nodemo that asks whether demographic similarity is "
             "a useful way to wire the graph.")

    # The two arms that measured best, combined. Not implied by either on its own:
    # the citywide covariate and the demographic block could easily have been
    # redundant with EACH OTHER, in which case removing both gains less than the
    # sum of removing each.
    registry["gnn_st_nodemo_noglobals"] = replace(
        st, name="gnn_st_nodemo_noglobals",
        features=replace(st_features, use_demographics=False, globals_=()),
        graph=replace(st.graph, demo=False),
        note=st.note + " No demographics (features or edges) and no citywide "
             "covariate. Keeps flu lags, the suppression flag, weather, the "
             "calendar, and the geographic/correlation edges.")

    # And the same minus weather, i.e. everything the leave-one-out arms found
    # dispensable removed at once, keeping only what earned its place.
    registry["gnn_st_lean"] = replace(
        st, name="gnn_st_lean",
        features=FeatureSpec(use_weather=False, use_demographics=False,
                             use_imputed_flag=True, use_seasonality=False,
                             globals_=()),
        graph=replace(st.graph, demo=False),
        note=st.note + " Flu lags, the suppression flag, and the "
             "geographic/correlation graph. Everything the leave-one-out "
             "study could not show earning its place is gone.")


    # Everything the ablations could not show earning its place, removed at once.
    # Keeps what did or is unresolved-but-positive: flu lags, the suppression
    # flag, weather, and the geographic and correlation edges.
    #
    # Note the inconsistency this arm exists to resolve. The city-wide covariate
    # was cut from the default on parsimony after measuring about zero, while
    # demographics measured +0.013 (features) / -0.001 (edges) and were left in.
    # The only distinction was that the city-wide files had a demonstrated defect
    # history. Transit was the third case and has since been removed outright.
    registry["gnn_st_minimal"] = replace(
        st, name="gnn_st_minimal",
        features=replace(st_features, use_demographics=False),
        graph=replace(st.graph, demo=False),
        note=st.note + " No demographics, as features or as edges. Everything "
             "else matches gnn_st, which already excludes city-wide "
             "covariates. Flu lags, suppression flag, weather, and geographic "
             "plus correlation edges.")

    # The pre-V2 settings, kept so the promotion is checkable rather than
    # asserted. Its numbers are in results/horizon_*/ under gnn_st from before
    # the change; this arm reproduces them.
    registry["gnn_st_v1"] = replace(
        st, name="gnn_st_v1",
        train=replace(st.train, epochs=300, dropout=0.15, weight_decay=1e-3),
        note=st.note + " Pre-V2 training settings: 300 epochs, dropout 0.15, "
             "weight decay 1e-3. Same accuracy, worse RMSE and calibration, and "
             "2.5x the runtime.")

    return registry


EXPERIMENTS: dict[str, Experiment] = _experiments()

GCN_EXPERIMENTS = tuple(n for n, e in EXPERIMENTS.items() if e.model == "gcn_fusion")
DUALTOPO_EXPERIMENTS = tuple(n for n, e in EXPERIMENTS.items() if e.model == "dualtopo")
GAT_EXPERIMENTS = tuple(n for n, e in EXPERIMENTS.items() if e.model == "gat")
