# GNN-Influenza-Boston

This is the research code behind a 1–4 week flu forecast for Boston's 14
neighborhoods. The forecast is for flu-like illness emergency-department
visits per 100,000 residents, using the weekly data the Boston Public Health
Commission (BPHC) publishes.

The main question: **if a model knows which neighborhoods border each other,
does it forecast better than one that looks at each neighborhood on its own?**
To answer it, the project uses a graph neural network (GNN), a model that is
given the map of which areas touch.

If you want to forecast for your own city, use this package instead:
[areaFluForecast](https://github.com/CodeMateo15/areaFluForecast)
(`pip install areaFluForecast`). This repository is where the research was done.

---

## What we found

Each model was tested on past seasons it never saw while being built. It was
compared with the simplest guess: "next week looks like this week".

- **Boston:** the graph model's error was 18–28% lower than that simple guess.
  - It beat the same model run without the map at 1 week ahead in all three
    seasons tested, and at 2 and 4 weeks ahead in two of three.
  - It tied a well-tuned standard neural network (an LSTM) at 1 week ahead.
  - It led that network at 2 and 4 weeks ahead, but clearly in only one season
    of three.
- **Chicago** (58 ZIP codes, held out the whole time): error was 17–19% lower
  than the simple guess. The map helped at 1 week ahead in all four seasons
  tested.
- **Columbus, Ohio:** error was 12–23% lower on average, but the gap wasn't
  clear enough to call. The graph model led the other models only at 1 week
  ahead.
- **Buenos Aires:** no better than the simple guess.

**Limits:**
- Every model runs about a week behind the curve for each week ahead it
  forecasts.
  - The models are better at predicting how big the flu wave gets than when
    it turns.
- Boston's neighborhoods rise and fall almost together, which limits how much
  any model can gain from the map. Neighborhoods, counties, or nodes with more of a difference can gain more from the model.

The full methods and results are in [Methods](Code/docs/METHODS.md).

---

## What's in this repository

| Folder | What it holds |
| --- | --- |
| [`BPHC/`](BPHC/) | **For BPHC:** the latest 2-week forecast, how accurate past forecasts were, and the code to make them each week |
| `Code/` | The models, the tests on past seasons, and the plots |
| `Data/` | The weekly data for each city, plus weather and neighborhood data |
| `Paper/` | The paper draft |

---

## Data

| City | Areas | Source |
| --- | --- | --- |
| Boston | 14 neighborhoods, weekly since Dec 2017 | BPHC public dashboard |
| Chicago | 58 ZIP codes, weekly activity level (1–10) | Chicago Department of Public Health |
| Columbus, Ohio | 17 areas, weekly since Jan 2022 | Columbus Public Health |
| Buenos Aires | 19 districts | Argentina's Ministry of Health (SNVS) |

Weather comes from [Open-Meteo](https://open-meteo.com/) (CC BY 4.0).

- **Columbus:** Columbus Public Health provided visit-level records. Only the
  weekly area counts are in this repository; the visit-level records are not
  shared.
- **Before using any city's data:** each one has quirks, so read its notes:
  - [Boston](Code/docs/DATA_NOTES.md)
  - [Chicago](Code/docs/CHICAGO_DATA_NOTES.md)
  - [Columbus](Code/docs/COLUMBUS_DATA_NOTES.md)
  - [Buenos Aires](Code/docs/AMBA_DATA_NOTES.md)

---

## Run it

```bash
pip install -r requirements.txt
python Code/run_arima.py --variant post_covid    # a quick statistical model
python Code/run_gnn.py   --experiment gnn_st     # the graph model
```

This is a research repository, so script options can change. For a stable
tool, use [areaFluForecast](https://github.com/CodeMateo15/areaFluForecast).

---

## More detail

- [Methods and results](Code/docs/METHODS.md)
- [What each score means, in plain language](Code/docs/METRICS_PLAIN.md)
- [How the neighborhood map was built](Code/docs/EDGES_AND_NODES_NOTES.txt)

## Credits

Supported by the Boston Public Health Commission, Columbus Public Health, the
PEAK Trailblazer fellowship, Prof. Ariel Hamlin, Prof. Deahan Yu, and Prof. Rajagopal Venkatesaramani (Northeastern University).

## Contact

Mateo Biggs (biggs.m@northeastern.edu) or Atharva Nilapwar (nilapwar.a@northeastern.edu).
