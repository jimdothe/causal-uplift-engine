import numpy as np
import pytest

from eval.qini import get_qini_curve, normalize_scores


def _rct(n=5000, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    t = rng.integers(0, 2, size=n).astype(float)
    true_cate = 0.1 * (x > 0)
    y = (rng.random(n) < 0.2 + true_cate * t).astype(float)
    return x, t, y, true_cate


def test_good_ranking_beats_random():
    x, t, y, true_cate = _rct()
    _, oracle = get_qini_curve(t, y, true_cate)
    _, random = get_qini_curve(t, y, np.random.default_rng(1).random(len(x)))
    assert oracle > random


def test_normalized_curve_ends_at_one():
    _, t, y, true_cate = _rct()
    curve, _ = get_qini_curve(t, y, true_cate)
    assert curve[-1] == pytest.approx(1.0, abs=1e-6)


def test_normalize_scores_best_is_one():
    out = normalize_scores({"a": 0.5, "b": 0.25})
    assert out == {"a": 1.0, "b": 0.5}


def test_matches_reference_implementation():
    ref = pytest.importorskip("causalpfn.evaluation")
    _, t, y, _ = _rct(seed=3)
    pred = np.random.default_rng(4).normal(size=len(t))
    ours_curve, ours_score = get_qini_curve(t, y, pred)
    ref_curve, ref_score = ref.get_qini_curve(t.copy(), y.copy(), pred.copy())
    np.testing.assert_allclose(ours_curve, ref_curve)
    assert ours_score == pytest.approx(ref_score)
