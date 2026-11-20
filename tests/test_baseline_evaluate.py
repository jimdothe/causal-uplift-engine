import numpy as np
import pandas as pd
import pytest

from baseline.evaluate import score_task, to_markdown
from baseline.tasks import PAPER, SEED, TASKS


def _write_fake_predictions(root, task, methods, n=2000, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    t = rng.integers(0, 2, size=n)
    y = (rng.random(n) < 0.1 + 0.1 * (x > 0) * t).astype(np.float32)
    folds = np.arange(n) % 5
    for i, method in enumerate(methods):
        noise = rng.normal(scale=0.5 + i, size=n)
        for k in range(5):
            m = folds == k
            out = root / "predictions" / method / task / f"seed{SEED}_fold{k}.parquet"
            out.parent.mkdir(parents=True, exist_ok=True)
            pd.DataFrame(
                {
                    "row_id": np.flatnonzero(m),
                    "task": task,
                    "fold": k,
                    "seed": SEED,
                    "model": method,
                    "uplift_pred": x[m] + noise[m],
                    "t": t[m].astype(np.int8),
                    "y": y[m],
                }
            ).to_parquet(out, index=False)


def test_best_method_normalized_to_one(tmp_path):
    methods = ["causalpfn", "s_learner", "t_learner"]
    _write_fake_predictions(tmp_path, "criteo_sub50k", methods)
    table = score_task(tmp_path, "criteo_sub50k")
    assert set(table["method"]) == set(methods)
    assert table["qini_normalized"].max() == pytest.approx(1.0)
    assert (table["n_test_rows"] == 2000).all()
    md = to_markdown(table)
    assert "Table 2" in md and "0.859" in md


def test_incomplete_folds_are_skipped(tmp_path):
    _write_fake_predictions(tmp_path, "criteo_full", ["causalpfn"])
    (tmp_path / "predictions" / "causalpfn" / "criteo_full" / f"seed{SEED}_fold4.parquet").unlink()
    assert score_task(tmp_path, "criteo_full").empty


def test_paper_targets_cover_every_task():
    assert set(PAPER) == set(TASKS) == {"criteo_sub50k", "criteo_full"}
    for scores in PAPER.values():
        assert max(scores.values()) == 1.0  # paper normalizes the best method to 1.000
        assert set(scores) == {"causalpfn", "x_learner", "s_learner", "da_learner", "t_learner"}
