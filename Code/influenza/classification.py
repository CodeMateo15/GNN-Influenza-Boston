"""Severity bands scored as a classification problem.

`severity.py` asks whether a forecast crossed a threshold. This asks the
classifier's version of the same question -- which of the four bands did it
put the week in, and how often was that right -- with the metrics a
classification paper reports: accuracy, precision, recall, F1, ROC-AUC, PR-AUC
and the confusion matrix. Both compare_classification.py (binned rate forecasts)
and run_severity_classifier.py (a model that outputs the band directly) score
through here, so the two are measured by exactly the same code.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from .severity import SEVERITY_BANDS

BAND_CODES = tuple(range(len(SEVERITY_BANDS)))

# The two alert questions worth asking of a four-band scale. 'very high or
# worse' is left out: at 10 test weeks it cannot carry a ranking metric.
ALERT_LEVELS = {1: "moderate_plus", 2: "high_plus"}
ALERT_LABELS = {1: "moderate or worse", 2: "high or worse"}

# Below this many observed events an alert row is reported but flagged, the same
# rule compare_severity.py applies.
MIN_EVENTS = 5


def band_scores(true_band, pred_band, scores: dict[int, np.ndarray] | None = None) -> dict:
    """Accuracy and macro P/R/F1 over the four bands, plus the binary alert view.

    `scores[k]` ranks weeks by how likely they are to sit at band k or above --
    the forecast rate itself for a binned regression model, P(band >= k) for a
    classifier. ROC-AUC and PR-AUC need only the ranking, so a rate is a valid
    score without being a probability.

    Macro-averaged, so 'very high' counts as much as 'low'. Weighted averaging
    would let the 92% of weeks that are low carry the number, which is the
    same trap as reading accuracy on a rare-event problem.
    """
    true_band = np.asarray(true_band, dtype=int)
    pred_band = np.asarray(pred_band, dtype=int)
    labels = list(BAND_CODES)
    row = {
        "n_obs": int(true_band.size),
        "accuracy": accuracy_score(true_band, pred_band),
        "precision_macro": precision_score(true_band, pred_band, labels=labels,
                                           average="macro", zero_division=0),
        "recall_macro": recall_score(true_band, pred_band, labels=labels,
                                     average="macro", zero_division=0),
        "f1_macro": f1_score(true_band, pred_band, labels=labels,
                             average="macro", zero_division=0),
    }
    for level, tag in ALERT_LEVELS.items():
        observed = true_band >= level
        called = pred_band >= level
        events = int(observed.sum())
        row[f"{tag}_n_events"] = events
        row[f"{tag}_base_rate"] = events / max(true_band.size, 1)
        row[f"{tag}_precision"] = precision_score(observed, called, zero_division=0)
        row[f"{tag}_recall"] = recall_score(observed, called, zero_division=0)
        row[f"{tag}_f1"] = f1_score(observed, called, zero_division=0)
        score = None if scores is None else scores.get(level)
        # An AUC needs both classes present; with none it is undefined, not 0.
        ranked = score is not None and 0 < events < true_band.size
        row[f"{tag}_roc_auc"] = roc_auc_score(observed, score) if ranked else np.nan
        row[f"{tag}_pr_auc"] = average_precision_score(observed, score) if ranked else np.nan
        row[f"{tag}_underpowered"] = events < MIN_EVENTS
    return row


def band_confusion(true_band, pred_band) -> np.ndarray:
    """4x4 counts, rows = what happened, columns = what was forecast."""
    return confusion_matrix(np.asarray(true_band, dtype=int),
                            np.asarray(pred_band, dtype=int), labels=list(BAND_CODES))
