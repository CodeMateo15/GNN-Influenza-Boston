# Where every number on the 12/3 poster comes from

Source of truth: the AJE submission, `~/Downloads/AJE/AJE_main.pdf`. `build_poster.py` gets the table
numbers by running `Paper/scripts/make_tables.py`, which writes the paper's tables. It asserts that they
equal the values printed in the PDF and stops if any differ. The rest come from the paper's text and
were copied in by hand. All are from unseen test seasons; the 2025–26 development season is never
quoted.

| Poster claim | Value | Paper source |
|---|---|---|
| Boston results table, mean WIS (relative) | GNN 5.13/6.47/8.22 (0.82/0.81/0.72); LSTM 5.18/6.82/9.16; Cola-GNN 5.35/7.61/8.77; seasonal ARIMA 6.52/7.66/9.15; seasonal blend 5.95/7.29/9.57; persistence 6.24/7.94/11.44 | Table 2 (asserted) |
| Stat strip: 18–28%, 14 of 14, 93–94%, ~1 min | | Table 2; Figure 6 (asserted in `make_poster_figures.py`); Results l. 230–231; Discussion l. 309–311 |
| Less error than persistence | 18–28% Boston, 17–19% Chicago | Table 2; Chicago rel. WIS 0.81/0.83/0.83 (asserted); Discussion l. 282 |
| LSTM ties at 1 week in Boston | 5.18 vs 5.13 | Results l. 216–218 |
| 95% ranges contain 93–94% | | Results l. 230–231, Figure 4A |
| Components table, % more error (seasons clearly worse) | map: Boston +10.8 (3/3), +3.8 (2/3), +5.6 (2/3); Chicago +7.4 (4/4), +6.0 (3/4), +3.6 (0/4). Weather and demographics are in the same table | Table 3 (asserted) |
| † Chicago without weather clearly better | 2 seasons at 1 wk, 1 at 2 wk | Table 3 footnote b |
| Map lowered error in all 14 neighborhoods | 6.1–15.3% at 1 wk, 2.0–7.9% at 2 wk, 1.8–7.9% at 4 wk | Results l. 243–244, Figure 6 (printed by `make_poster_figures.py`) |
| Automatic maps: no clear difference in 36 comparisons | | Table 4, Results l. 267–270 |
| Boston → Columbus transfer | WIS 3.90 vs 4.11 at 1 wk | Table 5 (asserted) |
| Package reproduces the Boston evaluation within 0.4%; about a minute a week on a laptop | | Discussion l. 309–311 |
| Persistence example: Dorchester week of Feb 2, 2025 = 294 (peak); actual 217 one week and 84 four weeks later; graph model median 252 and 135 | | Boston 2024–25 `predictions.csv`, gnn_st_tuned and persistence, h=1 and h=4 (same files as Figure 4) |
| Dorchester 7× Fenway, 67 vs 9 per 100,000 | | Introduction l. 25–27 |
| Cities: 14 neighborhoods, 58 ZIP codes, 17 planning areas; 16 weeks, 6 weather, 8 demographic inputs; 10 training runs | | Table 1, Methods l. 86–92, 120 |

## Figures (`figures/`, from `make_poster_figures.py`)
- `p_relative_wis.png`: paper Figure 2, redrawn with `make_figures.relative_wis()` with larger text.
- `p_forecast_paths.png`: Dorchester 2024–25. Forecasts made on four single weeks (6 and 2 weeks before the peak, at the peak, and 3 weeks after), each drawn 1, 2 and 4 weeks ahead from the `predictions.csv` files behind paper Figure 4. Persistence is the flat line from the same week.
- `p_map_benefit.png`: paper Figure 6, redrawn with `make_figures.map_benefit()`, with one title per horizon.
- `p_model_simple.png`: a three-step picture of the model for a general audience. Its curve is Dorchester's real 16 weeks up to the 2024–25 peak, and its range is the real forecast made at that peak.
- `p_fig1a_map.png` (used) and `p_fig1c_model.png` (no longer used): cropped from the vector PDF of paper Figure 1 at 600 dpi, with the panel letters blanked.
- `nu_seal.png`: the Northeastern seal image, taken from the CMSAC deck.
- `qr_app.png` encodes `https://codemateo15-boston-flu-outlook.share.connect.posit.cloud/`.
  `qr_package.png` encodes `https://github.com/CodeMateo15/areaFluForecast`.
  Both were decoded back from the rendered poster.

The live app shows 2026–27 forecasts, so the poster labels it "Not part of the paper's evidence".
