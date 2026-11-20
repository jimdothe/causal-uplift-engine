"""Criteo reproduction tasks, built exactly as in the authors' notebooks/qini.ipynb."""

from __future__ import annotations

SEED = 82718
N_FOLDS = 5
PAPER_FULL_ROWS = 2_500_000  # paper Appendix D.6: "2.5M stratified subset from sklift"

# Task name → (constructor kwargs for the authors' CriteoDataset, paper column)
TASKS = {
    "criteo_sub50k": (
        {"outcome_col": "visit", "treatment_col": "treatment", "subsample_max_rows": 50_000},
        "Table 2, Criteo (50k stratified subsample)",
    ),
    "criteo_full": (
        {"outcome_col": "visit", "treatment_col": "treatment"},
        "Table 7, Criteo (full table)",
    ),
}

# Normalized Qini from the paper. Best method in each column = 1.000.
PAPER = {
    "criteo_sub50k": {
        "causalpfn": 0.859,
        "x_learner": 1.000,
        "s_learner": 0.881,
        "da_learner": 0.626,
        "t_learner": 0.701,
    },
    "criteo_full": {
        "causalpfn": 0.939,
        "x_learner": 0.994,
        "s_learner": 1.000,
        "da_learner": 0.955,
        "t_learner": 0.902,
    },
}
TOLERANCE = 0.03


def paper_scores(task: str) -> dict[str, float]:
    return PAPER.get(task, {})


def build(task: str):
    """Return the authors' CriteoDataset object (iterable over 5 folds) for a task."""
    from baseline.authors import criteo_dataset

    kwargs, _ = TASKS[task]
    return criteo_dataset()(seed=SEED, n_folds=N_FOLDS, **kwargs)
