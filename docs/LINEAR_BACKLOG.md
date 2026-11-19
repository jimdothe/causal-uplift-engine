# Linear Backlog: Semester 1

Create these in Linear under team **CUE**, project **Causal Uplift Engine: Semester 1**. Each heading is a Linear **milestone**; each row is an **issue**. Estimates are in points (1 = half a day, 2 = a day, 3 = two to three days, 5 = about a week).

Labels to create: `data`, `warehouse`, `pipeline`, `baseline`, `model`, `eval`, `infra`, `docs`.

Owner numbers refer to roles in [WORK_DIVISION.md](WORK_DIVISION.md).

## M0: Setup

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| Connect Linear to GitHub (GitHub integration, branch-name format, auto-close on merge) | 1 | infra | 1 | A test PR with `Fixes CUE-x` moves the issue to Done on merge |
| Protect `main` (PR required, 1 review, CI must pass) | 1 | infra | 1 | Direct push to `main` is rejected |
| Create Snowflake account, database, warehouse, roles (`warehouse/snowflake_setup.sql`) | 1 | warehouse | 2 | Every member can log in and query `CAUSAL_UPLIFT.RAW` |
| Create Snowflake service user with key-pair auth for GitHub Actions | 1 | warehouse, infra | 1 | Key stored as GitHub secret; CI connects |
| Local environment: `pip install -e ".[dev]"` works on every laptop | 5 | infra | 1 | Each member posts `pytest` output |
| College GPU access: run CausalPFN README example with a large context | 3 | infra, baseline | 2 | GPU model, memory, and max working context recorded in Linear |
| Weights & Biases team project | 5 | infra | 1 | Test run visible to all |

## M1: Data pipeline

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| `pipeline/extract.py`: download Hillstrom + Criteo, add `row_id`, write Parquet + MD5 manifest | 1 | data, pipeline | 3 | Hillstrom has 64,000 rows; Criteo row count recorded |
| `pipeline/load_snowflake.py`: PUT + COPY Parquet into `RAW` | 1 | warehouse, pipeline | 3 | Re-running replaces tables without duplicates |
| dbt project setup (`dbt-snowflake` + `dbt-duckdb` targets) | 2 | warehouse | 2 | `dbt debug` passes on both targets |
| dbt staging models `stg_hillstrom`, `stg_criteo` | 2 | warehouse | 2 | Types and names per `DATA_CONTRACTS.md` |
| dbt tests: not null, accepted values, row counts, outcome-rate ranges | 2 | warehouse | 2 | `dbt test` passes |
| Randomization check model (standardized mean difference by feature) | 2 | warehouse, eval | 2 | All SMD < 0.05, results table in `ANALYTICS` |
| `pipeline/export.py`: validated tables to Parquet sorted by `row_id` | 2 | pipeline | 2 | Exported row order equals extract order |
| GitHub Actions `pipeline.yml`: extract → load → dbt build → export | 1 | pipeline, infra | 3 | One manual run completes green |

## M2: Model-ready data

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| Add CausalPFN repo at pinned commit under `third_party/` | 3 | baseline | 1 | `benchmarks` importable |
| `pipeline/prepare.py`: authors' preprocessing + folds (seed 82718) | 3 | data, baseline | 3 | Snapshot written per `DATA_CONTRACTS.md` |
| Equality test: our arrays == authors' arrays | 3 | baseline | 2 | `tests/test_equality.py` passes |
| `pipeline/neighbors.py`: fold-aware neighbor lists (train fold only) | 1 | data, model | 3 | Lists saved for Hillstrom + Criteo |
| Leakage test for neighbor lists | 5 | eval, model | 2 | Test fails on a deliberately leaky list, passes on real ones |

## M3: Baseline reproduced

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| `eval/qini.py` port of authors' Qini (done in scaffold) + bootstrap CIs | 5 | eval | 2 | Matches authors' function on random inputs |
| `eval/normalize.py`: per-column normalization as in paper | 5 | eval | 1 | Reproduces paper's normalization on toy table |
| Run CausalPFN on Hillstrom (both arms) | 3 | baseline | 3 | Predictions saved in prediction format |
| Run X/S/T/DA learners on Hillstrom | 5 | baseline | 2 | Predictions saved |
| Run CausalPFN on Criteo 50k subsample | 3 | baseline | 3 | Predictions saved |
| Run X/S/T/DA learners on Criteo 50k subsample | 5 | baseline | 2 | Predictions saved |
| Run CausalPFN on full Criteo | 3 | baseline | 5 | Predictions saved (or 500k fallback documented) |
| Run X/S/T/DA learners on full Criteo | 5 | baseline | 3 | Predictions saved |
| Reproduction report: our numbers vs. paper Tables 2 and 7 | 5 | eval, docs | 2 | Table in `reports/`, within tolerance or gap explained |

## M4: Model 1a

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| Feature tokenizer + transformer encoder (`models/m1/encoder.py`) | 4 | model | 3 | Unit test on shapes passes |
| Two-head outcome model + arm-weighted BCE loss | 4 | model | 2 | Overfits a 1k-row sample (sanity check) |
| Training loop: checkpoints every epoch, resume, W&B logging | 4 | model, infra | 3 | Resumes after a killed job |
| Early stopping on validation Qini | 4, 5 | model, eval | 2 | Best epoch chosen by Qini |
| M1a on Hillstrom (5 folds) and Criteo (5 folds) | 4 | model | 3 | Predictions saved, evaluated |

## M5: Model 1b

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| Neighbor attention module (treated and control separately) | 4 | model | 5 | Unit test + overfit sanity check |
| Data loader that joins precomputed neighbors | 1, 4 | model, data | 3 | Throughput measured on GPU |
| Learned retrieval refresh (rebuild neighbors from encoder vectors) | 4 | model | 3 | Refresh runs between epochs |
| Optuna tuning on 500k Criteo subset (~20 trials) | 4 | model | 3 | Best config committed in `configs/m1.yaml` |
| Final runs: 5 folds × 3 seeds, Criteo + Hillstrom | 4 | model | 5 | All predictions saved |
| Comparison table: M1a, M1b, CausalPFN, learners | 5 | eval | 2 | Table + bootstrap CIs in `reports/` |

## M6: Report

| Issue | Owner | Labels | Est. | Done when |
|---|---|---|---|---|
| Results write-up and figures (Qini curves) | 5 | docs | 3 | Draft reviewed by team |
| Pipeline and architecture write-up | 1, 2 | docs | 2 | Section merged |
| Semester 2 proposal: M2, M3, M4 | All | docs | 3 | Submitted |
