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

from .constants import HORIZONS, LOOKBACK, MC_SEED, SEED
from .windows import Window

DEFAULT_GLOBALS = ("ili_count", "ed_count", "ili_ed_perc", "flu_cases", "monthly_cases")
# The UNION across cities. FeatureSpec only checks that a name is spelled
# correctly; whether a given city can actually supply it is checked against
# City.available_globals in samples.load_dataset, which is where the failure is
# actionable ("Columbus has no ed_count") rather than merely syntactic.
GLOBAL_CHOICES = (*DEFAULT_GLOBALS, "vaccination", "hospitalizations")

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

    transit: bool = False
    transit_threshold: float = 0.0
    transit_coef: float = 1.0

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


@dataclass(frozen=True)
class Experiment:
    name: str
    model: Literal["gcn_fusion", "dualtopo"] = "gcn_fusion"
    variant: str = "post_covid"
    target: Literal["delta", "level"] = "delta"
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
        return payload


# ---------------------------------------------------------------------------
# Registry. Each name becomes a results/<name>/<variant>/ directory.
# ---------------------------------------------------------------------------

def _experiments() -> dict[str, Experiment]:
    geo_only = Experiment(
        name="gnn_geo",
        graph=GraphSpec(anchors="single", geo_max_hop=1),
        note="Geographic 1-hop adjacency only, single background anchor. "
             "Replaces Boston_Influenza_GNN_PostCovid.ipynb.",
    )
    corr_binary = Experiment(
        name="gnn_corrbinary",
        graph=GraphSpec(anchors="seven", geo_max_hop=1, corr=True, corr_binary=True),
        note="Luo et al. dual topology: geographic plus binary thresholded "
             "correlation edges. Replaces Boston_Influenza_GNN_V2_CorrBinary.ipynb.",
    )
    multiedge = Experiment(
        name="gnn_multiedge",
        graph=GraphSpec(anchors="seven", geo_max_hop=3, corr=True, corr_binary=False,
                        demo=True, transit=True),
        note="Multi-type weighted graph: hop-graded geographic, correlation, "
             "demographic similarity and MBTA transit, summed into one weighted "
             "adjacency. Replaces Boston_Influenza_GNN_V2_MultiEdge.ipynb.",
    )
    uniform = Experiment(
        name="gnn_uniform",
        graph=GraphSpec(anchors="seven", uniform_complete=True),
        note="Control: every neighborhood pair connected at weight 1. Tests "
             "whether structure and weighting help beyond mere connectivity.",
    )
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

    registry = {
        experiment.name: experiment
        for experiment in (geo_only, corr_binary, multiedge, uniform, dualtopo)
    }

    # Ablation arms. Named separately so each gets its own results directory.
    registry["gnn_multiedge_rt"] = replace(
        multiedge, name="gnn_multiedge_rt",
        features=replace(multiedge.features, use_rt=True),
        note=multiedge.note + " Plus the epyestim growth-index feature (see docs/RT_CAVEATS.md).",
    )
    registry["gnn_multiedge_covid_rsv"] = replace(
        multiedge, name="gnn_multiedge_covid_rsv",
        features=replace(multiedge.features, use_covid_cases=True, use_rsv_cases=True,
                         use_covid_wastewater=True),
        note=multiedge.note + " Plus monthly COVID/RSV neighborhood rates and COVID wastewater.",
    )
    registry["gnn_multiedge_season"] = replace(
        multiedge, name="gnn_multiedge_season",
        features=replace(multiedge.features, use_seasonality=True),
        note=multiedge.note + " Plus sin/cos of the target week's calendar position. "
             "At horizons of a quarter-cycle or more the lookback carries no "
             "information about where in the season the target week sits.",
    )
    registry["gnn_multiedge_level"] = replace(
        multiedge, name="gnn_multiedge_level", target="level",
        note=multiedge.note + " Level target instead of delta-from-origin. The delta "
             "parameterisation means the model learns the residual from persistence, "
             "which is the right frame at 1 week and again at 52 (where the origin is "
             "the same calendar week as the target). At 12 to 24 weeks the origin level "
             "is anti-correlated with the target, so this is the fair arm there.",
    )
    registry["gnn_multiedge_season_level"] = replace(
        multiedge, name="gnn_multiedge_season_level", target="level",
        features=replace(multiedge.features, use_seasonality=True),
        note="Both long-horizon corrections at once: calendar position and a level "
             "target. The arm to beat at 24 and 52 weeks.",
    )
    registry["dualtopo_no_bg"] = replace(
        dualtopo, name="dualtopo_no_bg",
        graph=replace(dualtopo.graph, anchors="none"),
        note="Dual-Topo-STGCN without boundary anchor nodes. Tests the paper's "
             "claim that a background node is worth ~0.135 Corr.",
    )
    return registry


EXPERIMENTS: dict[str, Experiment] = _experiments()

GCN_EXPERIMENTS = tuple(n for n, e in EXPERIMENTS.items() if e.model == "gcn_fusion")
DUALTOPO_EXPERIMENTS = tuple(n for n, e in EXPERIMENTS.items() if e.model == "dualtopo")
