# Citations for the paper

Compiled for the framing in `PAPER_PLAN.md`; PDFs re-checked against
`Citation Papers/`. Every entry was checked against PubMed or
Crossref/DataCite: the DOI resolves and the title/authors match. BibTeX keys are in `references.bib` (89 entries). The draft's own cleaned bibliography,
with the AJE fixes, is `overleaf/references.bib`.

**Columns and marks**
- **PDF file**: the file's path under `Citation Papers/`. **missing** means no
  PDF yet.
- Chapters of *Influenza Virus: Methods and Protocols* (2nd ed., Methods Mol
  Biol 2890, 2025) point to the whole book's PDF, with the chapter number.
- **✓**: cited in the current draft (`overleaf/main.txt` or `supplement.txt`).

---

## Introduction: burden, seasonality, why forecast

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `yamauchi2025book` ✓ | Yamauchi & Amorim (eds) 2025, *Influenza Virus: Methods and Protocols*, 2nd ed. doi:10.1007/978-1-0716-4326-6 | "Up to one billion individuals annually" is in the book's **Preface**. The draft cites the whole volume for it. | `2nd Closest/Influenza Virus Methods and Protocols.pdf` |
| `hutchinson2025understanding` | Hutchinson, Amorim & Yamauchi 2025, "Understanding Influenza", pp 1-26. doi:10.1007/978-1-0716-4326-6_1 | Winter epidemics in temperate regions; GISRS surveillance. It does **not** contain the 1-billion figure, so it was dropped from the draft. | `2nd Closest/Influenza Virus Methods and Protocols.pdf` (ch. 1) |
| `putri2018burden` ✓ | Putri et al. 2018, *Vaccine* 36:3960 | US economic burden, $11.2 billion. | `2nd Closest/Economic burden of seasonal influenza in the United State.pdf` |
| `lipsitch2011evidence` ✓ | Lipsitch et al. 2011, *Biosecur Bioterror* 9:89. doi:10.1089/bsp.2011.0007 | Decisions made on thin evidence during 2009 H1N1: the case for forecasting. | `Need for Forecasting/2011 Biosec Bioterr Lipsitch 2009pdm.pdf` |
| `frontiers2024surveillance` | "Infectious disease surveillance needs for the United States: lessons from Covid-19", *Front Public Health* 2024. doi:10.3389/fpubh.2024.1408193 | The need for local surveillance. Not cited in the draft. | `Need for Forecasting/2024 Frontiers PH Grad Surveillance.pdf` |
| `lutz2019applying` ✓ | Lutz et al. 2019, *BMC Public Health* 19:1659. doi:10.1186/s12889-019-7966-8 | The documented uses are CDC's: risk-communication talking points and planning. The draft wording was adjusted to match. | `Nearest Neighbors/Applying infectious disease forecasting to public health.pdf` |

## Related work: forecasting influenza

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `yang2016nyc` ✓ | Yang, Olson & Shaman 2016, *PLoS Comput Biol* 12:e1005201 | **The closest prior work.** Linking areas helped at the borough scale but degraded neighborhood forecasts. | `Nearest Neighbors/Forecasting Influenza Outbreaks in Boroughs and Neighborhoods of New York City.pdf` |
| `shaman2012forecasting` | Shaman & Karspeck 2012, *PNAS* 109:20425 | The founding real-time influenza forecast. Not cited in the draft; a good fit for the first Introduction paragraph on forecasting. | `2nd Closest/Forecasting seasonal outbreaks of inﬂuenza.pdf` |
| `reich2019collaborative` ✓ | Reich et al. 2019, *PNAS* 116:3146 | FluSight multiyear assessment. **Caution:** it found that over half the models beat the *historical* baseline. Do not cite it for "few models beat the baseline". The draft now cites it only for FluSight's history. | `2nd Closest/A collaborative multiyear, multimodel assessment ofseasonal inﬂuenza forecasting in the United States.pdf` |
| `mcgowan2019collaborative` ✓ | McGowan et al. 2019, *Sci Rep* 9:683 | The CDC challenge: short-term forecasts had the most skill. | `2nd Closest/Collaborative efforts to forecast seasonal influenza in the United States, 2015–2016.pdf` |
| `mathis2024flusight` ✓ | Mathis et al. 2024, *Nat Commun* 15:6289 | WIS, relative WIS, 23 quantiles. Also the FluSight baseline method, and "6 of 23 models outperform the baseline in 2021–22". | `3rd Closest/Evaluation of FluSight influenza.pdf` |
| `cramer2022covid` ✓ | Cramer et al. 2022, *PNAS* 119:e2113561119 | COVID Forecast Hub. Two-thirds of models beat the naive baseline; gains grow at longer horizons. | `3rd Closest/Evaluation of individual and ensemble probabilisticforecasts of COVID-19 mortality in the United States.pdf` |
| `brooks2018nonmechanistic` ✓ | Brooks et al. 2018, *PLoS Comput Biol* 14:e1006134 | Delphi. Models backfill and uses the data available at the time (Limitations). | `2nd Closest/Nonmechanistic forecasts of seasonal influenza with iterative one-week-ahead distributions.pdf` |
| `yang2015argo` ✓ / `lu2019statelevel` ✓ | Yang et al. 2015, *PNAS* 112:14473; Lu et al. 2019, *Nat Commun* 10:147 | Nowcasting versus forecasting. | `yang2015argo`: `3rd Closest/Accurate estimation of influenza epidemics using Google search data via ARGO.pdf`<br>`lu2019statelevel`: `3rd Closest/Improved state-level influenza nowcasting in the United States leveraging Internet-based data and network approaches.pdf` |
| `ginsberg2009detecting` ✓, `lazer2014parable` ✓ | Ginsberg et al. 2009; Lazer et al. 2014 | Google Flu Trends and why it failed. The folder has the working-paper version of Lazer; the published Science version is doi:10.1126/science.1248506. | `ginsberg2009detecting`: `2nd Closest/Detecting influenza epidemics using search engine query data.pdf`<br>`lazer2014parable`: `3rd Closest/The Parable of Google Flu (WP-Final).pdf` |
| `rodriguez2022datacentric` | Rodríguez et al. 2022 | Survey of epidemic forecasting. Not cited in the draft. | `3rd Closest/Data-Centric Epidemic Forecasting.pdf` |
| `kraemer2025ai` ✓ | Kraemer et al. 2025, *Nature* 638:623 | The main review of AI for epidemics. Cite it for "the added value is hard to evaluate", not for "backtests overstate". | `Nearest Neighbors/Artificial Intelligence for Modelling Infectious Disease Epidemics - PMC.pdf` |
| `kamyshnyi2026review` ✓ | Kamyshnyi et al. 2026, *Rev Med Virol* 36:e70107 ("Forecasting Influenza Epidemics and Pandemics in the Age of AI…") | Backtests "may overestimate actual performance in real-world settings". | `2nd Closest/Forecasting Influenza Epidemics and Pandemics in the Age of AI and Machine Learning.pdf` |
| `aje2022dengue`, `aje2024rt`, `aje2025primer` | *AJE* 2022, 2024, 2025 | Style models for AJE. Not cited. `aje2025primer` could back the one-line explanation of neural networks. | `aje2022dengue`: `AJE Papers/Machine-Learning–Based Forecasting of Dengue Fever.pdf`<br>`aje2024rt`: `AJE Papers/Using the near real-time effective reproduction number.pdf`<br>`aje2025primer`: `AJE Papers/A primer on neural networks.pdf` |

## Related work: graph models and spatial spread

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `luo2025novel` ✓ | Luo et al. 2025, *BMC Public Health* 25:408 | The paper that does not replicate: correlation 0.6849 → 0.8202 with the background node. | `Nearest Neighbors/A novel graph neural network influenza.pdf` |
| `deng2020colagnn` ✓ | Deng et al. 2020, Cola-GNN, CIKM '20 | Reimplemented as a baseline. | `Nearest Neighbors/Cola-GNN.pdf` |
| `kipf2017gcn` ✓ | Kipf & Welling, ICLR 2017 | Graph convolution. | `Related Work/Semi-supervised Classification with Graph Convolutional Networks.pdf.pdf` |
| `velickovic2018gat` ✓ | Veličković et al., ICLR 2018 | Graph attention (Luo's comparison model). | `3rd Closest/Graph attention networks.pdf` |
| `hochreiter1997lstm` ✓ | Hochreiter & Schmidhuber 1997, *Neural Comput* 9:1735 | The LSTM baseline. | `Related Work/Long Short-Term Memory.pdf` |
| `jin2023stgnn` ✓ | Jin et al. 2024, *IEEE Trans Knowl Data Eng* 36:5388 ("GNN Urban Computing") | Survey of graph models for city data. | `3rd Closest/GNN Urban Computing.pdf` |
| `gogovi2026spatial` ✓ | Gogovi 2026, *Appl Comput Intell Soft Comput* | **A parallel negative result.** A per-district LSTM beat every graph attention variant for dengue in Sri Lanka. | `2nd Closest/When Spatial Message Passing Fails to Help.pdf` |
| `viboud2006synchrony` ✓ | Viboud et al. 2006, *Science* 312:447 | Spread follows workflows (commuting) more than distance. Cite it with the commuting clause, not "nearby places". | `Related Work/Synchrony, Waves, and Spatial Hierarchies in the Spread of Influenza.pdf` |
| `charu2017mobility` ✓ | Charu et al. 2017, *PLoS Comput Biol* 13:e1005382 | Commuting flows explain spread. | `Related Work/Human mobility and the spatial transmission of influenza in the United States.pdf` |
| `pei2018spatial` ✓ | Pei et al. 2018, *PNAS* 115:2752 | Network model forecasting spread between areas. | `Related Work/Forecasting the spatial transmission of influenza in the United States.pdf` |
| `venkatramanan2021mobility` | Venkatramanan et al. 2021, *Nat Commun* 12:726 | A learned mobility map improves flu forecasts; contrast with the null transit result. Not cited; candidate for the Discussion's transit sentence. | `Related Work/Forecasting influenza activity using machine-learned mobility map.pdf` |
| `colizza2006airline`, `salathe2010contact`, `malik2022transit`, `guo2023transit` | Colizza et al. 2006; Salathé et al. 2010; Malik et al. 2022; Guo et al. 2023 | Mobility and contact networks, from the old transit framing. Not cited. | `colizza2006airline`: `3rd Closest/The role of the airline transportation network in the prediction and predictability of global epidemics.pdf`<br>`salathe2010contact`: `2nd Closest/A high-resolution human contact network forinfectious disease transmission.pdf`<br>`malik2022transit`: `2nd Closest/Modelling epidemic spread in cities using public transportation as a proxy for generalized mobility trends.pdf`<br>`guo2023transit`: `2nd Closest/Dynamic model of infectious public transportation systems.pdf` |
| `fritz2022combining` | Fritz, Dorigatti & Rügamer 2022, "Combining graph neural networks and spatio-temporal disease models to improve the prediction of weekly COVID-19 cases in Germany", *Sci Rep* 12:3930, doi:10.1038/s41598-022-07757-5 | A graph neural network combined with a statistical disease model for German districts. A close methodological neighbor; worth one sentence in the Introduction. | `Related Work/Combining graph neural networks and spatio‑temporal disease models to improve the prediction of weekly COVID‑19 cases in Germany.pdf` |

## Methods: features and data

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `shaman2009humidity` ✓ | Shaman & Kohn 2009, *PNAS* 106:3243 | Absolute humidity drives transmission. | `Methods/Absolute humidity modulates influenza survival, transmission, and seasonality.pdf` |
| `lowen2014humidity` ✓ | Lowen & Steel 2014, *J Virol* 88:7692. doi:10.1128/JVI.03544-13 (free: PMC4097773) | Humidity and temperature shape seasonality. | `Methods/Roles of Humidity and Temperature in Shaping Influenza Seasonality.pdf` |
| `dalziel2018urbanization` | Dalziel et al. 2018, *Science* 362:75 | Urbanization and humidity set epidemic intensity. Not cited; could join the weather sentence. | `Methods/Urbanization and humidity shape the intensity of influenza epidemics in U.S. cities.pdf` |
| `lemaitre2010age` ✓ | Lemaitre & Carrat 2010, *BMC Infect Dis* 10:162. doi:10.1186/1471-2334-10-162 | Age shapes who gets sick. | `Methods/Comparative age distribution of influenza morbidity and mortality during seasonal influenza epidemics and the 2009 H1N1 pandemic.pdf` |
| `olson2007ed` ✓ | Olson et al. 2007, *PLoS Med* 4:e247 | ED respiratory visits track lab-confirmed flu by age. | `Methods/Monitoring the Impact of Influenza by Age, Emergency Department Fever and Respiratory Complaint Surveillance in New York City.pdf` |
| `olsen2020decreased` ✓ | Olsen et al. 2020, *MMWR* 69:1305 | Flu nearly vanished in 2020, including in the Southern Hemisphere (Chile, Australia, South Africa). Backs the choice to start the Columbus series after COVID-19. | `Discussion/Decreased Influenza Activity During the COVID-19 Pandemic.pdf` |
| `carrat2008timelines` | Carrat et al. 2008, *Am J Epidemiol* 167:775 | Incubation and shedding times make weekly steps natural. Not cited. | `Methods/Time Lines of Infection and Disease in Human Influenza, A Review of Volunteer Challenge Studies.pdf` |
| `grohskopf2016vaccines`, `temte2022orchards` | Grohskopf et al. 2016; Temte et al. 2021 | Old framing. Not cited. | `grohskopf2016vaccines`: `3rd Closest/Prevention and Control of Seasonal Influenza with Vaccines _ MMWR.pdf`<br>`temte2022orchards`: `3rd Closest/The Oregon Child Absenteeism Due to Respiratory Disease Study (ORCHARDS).pdf` |

## Methods: evaluation and statistics

These match the code: `influenza/scoring.py` and `compare_significance.py`.

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `bracher2021interval` ✓ | Bracher et al. 2021, *PLoS Comput Biol* 17:e1008618 | Definition of WIS (Weighted Interval Score). | `Methods/Evaluating epidemic forecasts in an interval format.pdf` |
| `gneiting2007proper` ✓ | Gneiting & Raftery 2007, *JASA* 102:359 | Proper scoring rules. For calibration specifically, Gneiting, Balabdaoui & Raftery 2007 (*JRSS B* 69:243, doi:10.1111/j.1467-9868.2007.00587.x) fits better; it is not in the bib yet. | `Methods/Strictly Proper Scoring Rules, Prediction, and Estimation.pdf` |
| `tashman2000outofsample` ✓ | Tashman 2000, *Int J Forecast* 16:437 | Rolling-origin evaluation. | `Methods/Out-of-sample tests of forecasting accuracy, an analysis and review.pdf` |
| `diebold1995comparing` ✓ | Diebold & Mariano 1995, *J Bus Econ Stat* 13:253 | Week-level test. The folder copy is the 2002 reprint (*JBES* 20:134); the 1995 original is doi:10.1080/07350015.1995.10524599. | `Methods/Comparing Predictive Accuracy.pdf` |
| `harvey1997testing` ✓ | Harvey, Leybourne & Newbold 1997 | Small-sample correction. | `Methods/Testing the equality of prediction mean squared errors.pdf` |
| `newey1987hac` ✓ | Newey & West 1987 | Variance for overlapping multiweek errors. | `Methods/A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation ConsistentCovariance Matrix.pdf` |
| `kunsch1989bootstrap` ✓ | Künsch 1989 | Moving-block bootstrap. | `Methods/The Jackknift and the Bootstrap for General Stationary Observations.pdf` |
| `holm1979simple` ✓ | Holm 1979 | Multiple-comparison correction. | `Methods/A Simple Sequentially Rejective Multiple Test Procedure.pdf` |
| `bosse2023transformed` ✓ | Bosse et al. 2023, *PLoS Comput Biol* 19:e1011393 | WIS on the raw scale is dominated by high-rate cells (Limitations). | `3rd Closest/Scoring epidemiological forecasts on transformed scales.pdf` |

## Methods and Results: severity alerts

Added for the severity-alert analysis on the unseen seasons.

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `biggerstaff2018severity` ✓ | Biggerstaff et al. 2018, *Am J Epidemiol* 187:1040. doi:10.1093/aje/kwx334 | CDC's classification of season severity with Moving Epidemic Method thresholds; the basis for the moderate/high bands. | `Methods/Systematic Assessment of Multiple Routine and Near-Real Time Indicators to Classify the Severity of Influenza Seasons.pdf` |
| `vega2013mem` ✓ | Vega et al. 2013, *Influenza Other Respir Viruses* 7:546. doi:10.1111/j.1750-2659.2012.00422.x (free: PMC5855152) | The Moving Epidemic Method itself: how the intensity thresholds are computed. | `Methods/Influenza surveillance in Europe, establishing epidemic thresholds by the Moving Epidemic Method.pdf` |
| `brier1950verification` ✓ | Brier 1950, *Mon Weather Rev* 78:1. doi:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | The Brier score, used to score the probability of crossing a threshold. | `Methods/Verification Of Forecasts Expressed In Terms Of Probability.pdf` |

## Methods: building the graph from boundary polygons

The code (`scrapers/derive_*_adjacency.py`) treats 2 areas as neighbors when
they share a boundary edge (at least 2 vertices), not just a corner. This is
rook contiguity.

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `morris2019bym` ✓ | Morris et al. 2019, *Spat Spatiotemporal Epidemiol* 31:100301 | Neighbor lists from census boundary files, plus a hand-added link across Jamaica Bay. **Note:** `poly2nb` defaults to queen contiguity (corners count), so do not claim that Morris used "the same rule". | `Methods/Bayesian Hierarchical Spatial Models, Implementing the Besag York Mollié Model in Stan.pdf` |
| `besag1991bayesian` | Besag, York & Mollié 1991, "Bayesian image restoration, with two applications in spatial statistics", *Ann Inst Stat Math* 43(1):1-20, doi:10.1007/BF00116466 (the PDF runs to p. 59 with the published discussion) | The original neighborhood-adjacency disease-mapping model that Morris implements. Optional, as a second citation for adjacency-based spatial models. | `3rd Closest/Bayesian Image Restoration, With Two Applications in Spatial Statistics.pdf` |

## Discussion: portability and transfer

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `panagopoulos2021transfer` ✓ | Panagopoulos et al. 2021, AAAI 35:4838 | Graph model transferred between countries (COVID-19). | `Discussion/Transfer Graph Neural Networks for Pandemic Forecasting.pdf` |
| `shea2020multiple` | Shea et al. 2020 | Multiple models for outbreak management. Not cited. | `2nd Closest/Harnessing multiple models for outbreak management.pdf` |

## Buenos Aires (removed from the paper 2026-10-07)

Buenos Aires was replaced by Chicago, so these are no longer cited in the draft.
Kept in `references.bib` in case the city comes back.

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `hirve2016tropics` | Hirve et al. 2016, *PLoS One* 11:e0153003 | South American seasons start April to June. Backs the AMBA season. | `Discussion/Influenza Seasonality in the Tropics and Subtropics.pdf` |
| `caini2016temporal` | Caini et al. 2016, *PLoS One* 11:e0152310 | Longer, less defined seasons in the **tropics**. Temperate Southern Hemisphere sites (including Argentina) are as concentrated as northern ones, so don't use it for "outside the temperate north". | `Discussion/Temporal Patterns of Influenza A and B in Tropical and Temperate Countries.pdf` |
| `dave2019global` | Dave & Lee 2019, *Epidemiol Rev* 41:51 | Onset, duration and peaks differ between climate zones. | `Discussion/Global Geographical and Temporal Patterns of Seasonal Influenza and Associated Climatic Factors.pdf` |
| `kramer2019countries` | Kramer & Shaman 2019, *PLoS Comput Biol* 15:e1006742 | Forecasts are less accurate in tropical and subtropical countries. | `2nd Closest/Development and validation of influenza forecasting for 64 temperate and tropical countries.pdf` |
| `tamerius2013environmental` ✓ | Tamerius et al. 2013, *PLoS Pathog* 9:e1003194 | Climate rule for flu timing (cited for the weather features). | `2nd Closest/Environmental Predictors of Seasonal Influenza Epidemics across Temperate and Tropical Climates.pdf` |
| `olsen2020decreased` ✓ | (above) | Why the Columbus series starts after 2020–2021. | `Discussion/Decreased Influenza Activity During the COVID-19 Pandemic.pdf` |

## Limitations

| Key | Citation | Use it for | PDF file |
|---|---|---|---|
| `bracherfunk2026leakage` | Bracher & Funk 2026, arXiv:2608.05883 | A claimed AI gain came from revised data. AJE doesn't list preprints, so the draft cites it **in the text** ("unpublished preprint"). | `Discussion/Information leakage from data revisions in retrospective forecasts.pdf` |
| `brooks2018nonmechanistic` ✓ | (above) | Backfill. | `2nd Closest/Nonmechanistic forecasts of seasonal influenza with iterative one-week-ahead distributions.pdf` |

## Extra: interesting papers, sorted into sections

Each row now says which section it belongs to and whether the PDF is in the
folder.

| Key | Section | PDF file | Why it's interesting |
|---|---|---|---|
| `grantz2016chicago` ✓ | Introduction | `2nd Closest/Disparities in influenza mortality and transmission related to sociodemographic factors within Chicago in the pandemic of 1918.pdf` | 1918 Chicago: flu risk differed between census tracts. Used as the opening hook. |
| `hadler2016poverty` ✓ | Introduction | `2nd Closest/Influenza-Related Hospitalizations and Poverty Levels.pdf` | Hospitalization nearly twice as high in tracts with ≥20% poverty as in tracts with <5%. |
| `kandula2019autoregressive` ✓ | Related work: forecasting | `2nd Closest/Near-term forecasts of influenza-like illness An evaluation of autoregressive time series approaches.pdf` | Autoregressive models "remain competitive" 1-4 weeks ahead. |
| `farrow2017human` | Related work: forecasting | `2nd Closest/A human judgment approach to epidemiological forecasting.pdf` | Crowd forecasts often beat statistical models short-term. Not cited. |
| `osthus2019nowcasts` | Related work: forecasting | `2nd Closest/Even a good influenza forecasting model can benefit from internet-based nowcasts, but those benefits are limited.pdf` | Even perfect nowcasts help forecasts only a little. Not cited; fits the nowcasting sentence. |
| `nsoesie2014review` | Related work: forecasting | `2nd Closest/A systematic review of studies on forecasting thedynamics of inﬂuenza outbreaks.pdf` | Systematic review calling for real-time evaluation. Not cited. |
| `reich2019ensemble` ✓ | Discussion: future work | `2nd Closest/Accuracy of real-time multi-model ensemble forecasts for seasonal influenza in the U.S..pdf` | Ensembles beat individual models. |
| `sherratt2023european` ✓ | Discussion: future work | `2nd Closest/Predictive performance of multi-model ensemble forecasts of COVID-19 across European nations.pdf` | Same, for European COVID-19. |
| `boehm2023wastewater` ✓ | Discussion: future work | `2nd Closest/Wastewater concentrations of human influenza,metapneumovirus, parainfluenza.pdf` | Wastewater results within 24 h of sampling. |
| `bosse2023transformed` ✓ | Limitations | `3rd Closest/Scoring epidemiological forecasts on transformed scales.pdf` | Raw-scale WIS is dominated by high-rate cells. |
| `tamerius2013environmental` ✓ | Methods: weather | `2nd Closest/Environmental Predictors of Seasonal Influenza Epidemics across Temperate and Tropical Climates.pdf` | Climate rule for flu timing. |
| `kramer2019countries` | Buenos Aires (removed) | `2nd Closest/Development and validation of influenza forecasting for 64 temperate and tropical countries.pdf` | Forecasts worse in the tropics and subtropics. |
| `gog2014pandemic` ✓ | Introduction | `2nd Closest/Spatial Transmission of 2009 Pandemic Influenza in the US.pdf` | Short-distance spread dominated in 2009. |
| `baker2020npi` | Discussion / Limitations | `2nd Closest/The impact of COVID-19 nonpharmaceuticalinterventions on the future dynamics of endemic infections.pdf` | Post-COVID seasons behave oddly. Not cited; could go next to olsen. |
| `kissler2020nyc` | Discussion: transit | `3rd Closest/Reductions in commuting mobility correlate with geographic differences in SARS-CoV-2 prevalence in New York City.pdf` | Within-city mobility mattered for COVID in NYC. Not cited; contrast with the null transit result. |
| `worby2015age` | Methods: demographics | `3rd Closest/On the relative role of different age groups in influenza epidemics.pdf` | Ages 5-17 drive the largest epidemics. Not cited. (Its PDF title "On the relative role of different age groups…" is this paper, not Lemaitre.) |
| `morris2019bym` ✓ | Methods: graph | `Methods/Bayesian Hierarchical Spatial Models, Implementing the Besag York Mollié Model in Stan.pdf` | See above. |

## Optional or weak

- `anter2025ai` (the book's ch. 15): generic AI background. Not cited. PDF: `2nd Closest/Influenza Virus Methods and Protocols.pdf` (ch. 15)
- `huddleston2020h3n2`: forecasts viral evolution. Not cited. PDF: `3rd Closest/Integrating genotypes and phenotypes improves long-term forecasts of seasonal influenza A/H3N2 evolution.pdf`
- `kermack1927contribution`: SIR, from the old draft. Not cited. PDF: `3rd Closest/A contribution to the mathematical theory of epidemics.pdf`
- **Probably drop** (not cited):
  - `gradon2021misinformation`. PDF: `2nd Closest/Countering misinformation_A multidisciplinary approach.pdf`
  - `abdelouahed2025ai`. PDF: `2nd Closest/Integrating artificial intelligence into public health education and healthcare_insights from the COVID-19 and monkeypox crises for future pandemic readiness.pdf`
  - `delreypuech2026gap`. PDF: `2nd Closest/Mind the (widening) gap_why public health must engage with AI now.pdf`

---

## Coverage check against PAPER_PLAN

| Claim / limitation | Supporting citations |
|---|---|
| 1. The graph helps in Boston | yang2016nyc (contrast), gog2014pandemic, viboud2006synchrony, pei2018spatial, kipf2017gcn; tests: diebold1995comparing, harvey1997testing, newey1987hac, holm1979simple, kunsch1989bootstrap |
| 2. No wide margin over tuned baselines | mathis2024flusight, cramer2022covid, kandula2019autoregressive, gogovi2026spatial |
| 3. Graph built from boundary files | morris2019bym |
| 4. Transfer between cities | panagopoulos2021transfer, lutz2019applying |
| 5. Held-out 4th city (Chicago) and what doesn't replicate | luo2025novel |
| Post-COVID start for Columbus | olsen2020decreased |
| No reporting delay or revisions | brooks2018nonmechanistic; bracherfunk2026leakage (in text) |
| Cola-GNN is a reimplementation | deng2020colagnn |
| One unseen season for Columbus | tashman2000outofsample |
