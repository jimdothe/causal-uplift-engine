# Baseline Reproduction: CausalPFN

Reproduces paper Tables 2 and 7 (normalized Qini) separately for **Hillstrom** and **Criteo**, using the authors' own data loaders, folds, comparison methods, and Qini code from the pinned submodule `third_party/CausalPFN`.

## What runs

| Dataset | Task | Paper column | Rows | CausalPFN target |
|---|---|---|---|---|
| Hillstrom | `hill_womens_vs_none` | Table 2, Hill(1) | ~42.7k (two arms) | 0.992 |
| Hillstrom | `hill_mens_vs_none` | Table 2, Hill(2) | ~42.6k (two arms) | 0.968 |
| Criteo | `criteo_sub50k` | Table 2, Criteo | 50,000 | 0.859 |
| Criteo | `criteo_full` (`--include-full`) | Table 7, Criteo | full 10% sample | 0.939 |

Methods per task: CausalPFN, X-, S-, DA-, T-Learner (EconML, `hpo=False`), each on the same 5 folds (seed 82718). Normalization divides by the best method in each task, so **all five methods must run** for the normalized numbers to be comparable with the paper.

## How to run (GPU server)

```bash
git clone --recurse-submodules https://github.com/yashashree5/causal-uplift-engine.git
cd causal-uplift-engine
python3.10 -m venv .venv-baseline && source .venv-baseline/bin/activate
pip install -r baseline/requirements.txt
pip install -e . --no-deps

bash scripts/run_baseline_hillstrom.sh             # Hillstrom, both arms
bash scripts/run_baseline_criteo.sh                # Criteo 50k subsample
bash scripts/run_baseline_criteo.sh --include-full # + full Criteo (Table 7), slow
```

Outputs:
- Predictions: `outputs/predictions/<method>/<task>/seed82718_fold<k>.parquet`
- Run metadata: `outputs/predictions/<task>_run.json`
- Results: `reports/baseline_hillstrom.md|csv`, `reports/baseline_criteo.md|csv` (commit these)

Re-running skips finished folds. To run one piece: `python -m baseline.run --task criteo_full --methods causalpfn`.

## Decisions and known issues

- **Pinned source `7da4afa` (Feb 2026), not the latest `b7ed2f1`.** The September 2026 release (0.1.5) replaced FAISS and changed how context rows are chosen on large tables ("prevent duplicate context rows"). That can change full-Criteo results, so we use the version closest to the paper. Running at `b7ed2f1` as a second check is useful.
- **Arm labels:** the code's Hill(1) is women's e-mail vs. none; the paper text says men's. We name tasks by arm.
- **Comparison methods use random forests without a fixed seed** (authors' code), so their scores vary slightly between runs. This moves CausalPFN's normalized score too. Report raw Qini alongside.
- **Data download:** the first run downloads Hillstrom and Criteo through scikit-uplift, and the CausalPFN weights from Hugging Face (`vdblm/causalpfn`). Make sure the cache directories have space.
- **GPU memory:** CausalPFN uses a context of 50,000 rows. If it runs out of memory, record the GPU and stop; don't lower the context without agreeing with the team, because results would no longer match the paper's setup.
- **Full Criteo** is slow: CausalPFN uses retrieval, and the random-forest learners train on ~1M+ rows per fold on CPU.
- `row_id` in prediction files is the index into the task's arrays (after arm filtering or subsampling), not the raw-table `row_id`.
