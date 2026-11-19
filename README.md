# Causal Uplift Engine

Estimating who a marketing campaign actually persuades. We reproduce **CausalPFN** (NeurIPS 2025) on the **Hillstrom** and **Criteo** randomized experiments, then build a retrieval-based uplift transformer that targets CausalPFN's known drop on large campaigns.

**Start here:** [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)

| Document | What it covers |
|---|---|
| [Project plan](docs/PROJECT_PLAN.md) | Problem, baseline targets, models, architecture, roles, timeline, risks |
| [Linear backlog](docs/LINEAR_BACKLOG.md) | Milestones and issues to create in Linear |
| [Data contracts](docs/DATA_CONTRACTS.md) | Shared file formats and Snowflake layout |
| [Setup](docs/SETUP.md) | Local env, Snowflake, dbt, GPU server |
| [Contributing](CONTRIBUTING.md) | Linear + GitHub workflow, rules |

## Repository layout

```
.github/            CI, data pipeline workflow, PR template
configs/            dataset and model configs
pipeline/           extract → load → export → prepare → neighbors
warehouse/          dbt project + Snowflake setup SQL
baseline/           CausalPFN and X/S/T/DA learner reproduction
models/m1/          retrieval uplift transformer (Semester 1)
eval/               Qini, normalization, bootstrap
tests/              unit, equality, and leakage tests
reports/            results tables and figures
third_party/        pinned CausalPFN source (Linear milestone M2)
data/, outputs/     local only, git-ignored
```

## Pipeline

```
GitHub Actions: extract (sklift → Parquet) → load (Snowflake RAW) → dbt build (STAGING, VALIDATED, ANALYTICS + tests) → export
College GPU:    prepare (authors' preprocessing + folds) → neighbors → baseline / M1 training → eval
```

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,pipeline]"
pytest
python -m pipeline.extract --dataset hillstrom
```
