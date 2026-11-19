# Data Contracts

Shared formats so team members can work in parallel. Change these only through a PR that everyone reviews.

## 1. Raw Parquet (output of `pipeline/extract.py`)

Location: `data/raw/<dataset>/<dataset>.parquet` plus `data/raw/<dataset>/manifest.json`.

Every raw table gets `row_id` (int64, 0-based original row position from scikit-uplift). **Never reorder rows without sorting by `row_id` afterwards.** The authors' folds depend on row order.

### Hillstrom

| Column | Type | Notes |
|---|---|---|
| row_id | int64 | Original row position |
| recency | int64 | Months since last purchase |
| history_segment | string | e.g. `3) $200 - $350` |
| history | float64 | Dollars spent last year |
| mens | int64 | 0/1 |
| womens | int64 | 0/1 |
| zip_code | string | Urban / Suburban / Rural |
| newbie | int64 | 0/1 |
| channel | string | Phone / Web / Multichannel |
| segment | string | `Mens E-Mail`, `Womens E-Mail`, `No E-Mail` |
| visit | int64 | 0/1 outcome |
| conversion | int64 | 0/1 |
| spend | float64 | Dollars |

### Criteo

| Column | Type | Notes |
|---|---|---|
| row_id | int64 | Original row position |
| f0 … f11 | float64 | Anonymized features |
| treatment | int64 | 0/1, randomized |
| exposure | int64 | 0/1, actually shown an ad (not randomized; never use as treatment) |
| visit | int64 | 0/1 outcome |
| conversion | int64 | 0/1 |

### manifest.json

```json
{"dataset": "hillstrom", "rows": 64000, "md5": "...", "source": "sklift.fetch_hillstrom", "sklift_version": "...", "created_utc": "..."}
```

## 2. Snowflake layout

Database `CAUSAL_UPLIFT`:

| Schema | Contents | Written by |
|---|---|---|
| `RAW` | Exact copies of raw Parquet | `load_snowflake.py` |
| `STAGING` | Typed, renamed, one model per source | dbt |
| `VALIDATED` | Staging + passed tests; source for export | dbt |
| `ANALYTICS` | Randomization checks, summaries, model results | dbt + `eval/` |

## 3. Model-ready snapshot (output of `pipeline/prepare.py`)

Location: `data/snapshots/<snapshot_id>/<task>/` where `task` is one of `hill_womens_vs_none`, `hill_mens_vs_none`, `criteo_sub50k`, `criteo_full`.

| File | Contents |
|---|---|
| `X.npy` | float32 [N, D], authors' preprocessing |
| `t.npy` | float32 [N] |
| `y.npy` | float32 [N] |
| `row_id.npy` | int64 [N], maps each row back to raw `row_id` |
| `folds.npz` | `train_0..4`, `test_0..4` index arrays (into X) |
| `manifest.json` | snapshot_id, git commit, seed, arrays' MD5, equality-check result |

`snapshot_id` format: `YYYYMMDD-<short git sha>`.

## 4. Neighbor lists (output of `pipeline/neighbors.py`)

`data/snapshots/<snapshot_id>/<task>/neighbors_fold<k>.npz` with `treated` and `control`: int64 [N, K] indices into X. Neighbors for any row are drawn only from fold k's **training** rows and never include the row itself.

## 5. Prediction file (every model)

`outputs/predictions/<model>/<task>/seed<s>_fold<k>.parquet`

| Column | Type |
|---|---|
| row_id | int64 |
| task | string |
| fold | int32 |
| seed | int32 |
| model | string (e.g. `causalpfn`, `s_learner`, `m1a`, `m1b`) |
| uplift_pred | float64 |
| t | int8 |
| y | float32 |

Only test-fold rows are written. `eval/` reads these files and nothing else.
