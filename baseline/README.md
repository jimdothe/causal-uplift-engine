# Baseline Reproduction: CausalPFN on Criteo

Reproduces the paper's Criteo results (normalized Qini, Tables 2 and 7) using the authors' own data loader, folds, comparison methods, and Qini code from the pinned submodule `third_party/CausalPFN`.

## What runs

| Step | Task | Paper | Rows | CausalPFN target |
|---|---|---|---|---|
| 1 (default) | `criteo_sub50k` | Table 2 | 50,000 stratified subsample | 0.859 |
| 2 (`--include-full`) | `criteo_full` | Table 7 | full sklift 10% sample (paper: ~2.5M) | 0.939 |

Step 1 is quick and gives a complete baseline on its own. Step 2 is the full-table run and needs the college GPU and several hours.

Methods per task: CausalPFN, X-, S-, DA-, T-Learner (EconML, `hpo=False`), each on the same 5 folds (seed 82718). Normalization divides by the best method in each task, so **all five methods must run** for the normalized numbers to be comparable with the paper.

## How to run (GPU server)

```bash
git clone --recurse-submodules https://github.com/yashashree5/causal-uplift-engine.git
cd causal-uplift-engine
python3.10 -m venv .venv-baseline && source .venv-baseline/bin/activate
pip install -r baseline/requirements.txt
pip install -e . --no-deps

bash scripts/run_baseline_criteo.sh                 # Step 1: Table 2 (50k)
bash scripts/run_baseline_criteo.sh --include-full  # Step 2: + Table 7 (full table)
```

Outputs:
- Predictions: `outputs/predictions/<method>/<task>/seed82718_fold<k>.parquet`
- Run metadata (rows, device, commits): `outputs/predictions/<task>_run.json`
- Results: `reports/baseline_criteo.md` and `.csv` (commit these)
- Logs: `outputs/logs/`

Re-running skips finished folds. To run one piece: `python -m baseline.run --task criteo_full --methods causalpfn`.

## Decisions and known issues

- **Row count:** the full run prints the number of rows and warns if it differs from the paper's ~2.5M by more than 5%. Record the number in TEA-6; a different sample size can explain a gap with Table 7.
- **Pinned source `7da4afa` (Feb 2026), not the latest `b7ed2f1`.** The September 2026 release (0.1.5) replaced FAISS and changed how context rows are chosen on large tables. That can change full-Criteo results, so we use the version closest to the paper. Running at `b7ed2f1` afterwards is a useful second check.
- **Treatment column:** always `treatment` (randomized). Never `exposure`, which isn't randomized.
- **Comparison methods use random forests without a fixed seed** (authors' code), so their scores vary slightly between runs. This moves CausalPFN's normalized score too, so the report also shows raw Qini.
- **Downloads:** the first run downloads Criteo through scikit-uplift and the CausalPFN weights from Hugging Face (`vdblm/causalpfn`). Make sure the cache directories have space.
- **GPU memory:** CausalPFN uses a 50,000-row context. If it runs out of memory, record the GPU and stop; lowering the context means the setup no longer matches the paper.
- **Full table runtime:** CausalPFN switches to retrieval, and the random-forest learners train on 1M+ rows per fold on CPU.
- `row_id` in prediction files is the index into the task's arrays (after subsampling), not the raw-table `row_id`.
