# Contributing

## Workflow: Linear + GitHub

1. **Pick an issue in Linear** and assign it to yourself. Move it to *In Progress*.
2. **Create the branch from Linear's name.** In the issue, press `Cmd/Ctrl + Shift + .` ("Copy git branch name"):
   ```bash
   git checkout main && git pull
   git checkout -b yashashree/cue-12-extract-hillstrom
   ```
   The `cue-12` part links the branch to the issue automatically.
3. **Commit small and often.** Start messages with the issue ID:
   ```
   CUE-12: add row_id and MD5 manifest to extract
   ```
4. **Open a pull request** using the template. Title: `CUE-12: Extract Hillstrom and Criteo`. Put `Fixes CUE-12` in the description. Linear moves the issue to *In Review* when the PR opens and to *Done* when it merges.
5. **One reviewer approves**, CI passes, then **squash-merge**. Delete the branch.

Use `Part of CUE-12` instead of `Fixes CUE-12` if the PR doesn't finish the issue.

## Rules

- No direct pushes to `main`.
- Never commit data, credentials, private keys, or `.env`. Data goes to Snowflake and college storage.
- Don't change preprocessing in `pipeline/prepare.py` until the reproduction passes (see the project plan, Section 5).
- Every model writes predictions in the format in [docs/DATA_CONTRACTS.md](docs/DATA_CONTRACTS.md).
- Every reported number must come from a script in the repo, not a notebook cell.
- Fix seeds and log the data snapshot version and git commit with every run.

## Code style

- Python 3.11+, formatted and linted with `ruff` (`ruff check . && ruff format .`).
- Tests in `tests/`, run with `pytest`.
- SQL models in `warehouse/models/`, lowercase keywords optional but consistent within a file.

## Linear setup (done once by the lead)

- Team key: `CUE`.
- Settings → Integrations → GitHub: connect the `causal-uplift-engine` repo.
- Enable: link branches by issue ID, move to *In Progress* on branch push, *In Review* on PR open, *Done* on merge.
- Create labels and milestones from [docs/LINEAR_BACKLOG.md](docs/LINEAR_BACKLOG.md).
