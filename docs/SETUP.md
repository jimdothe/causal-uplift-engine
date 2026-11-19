# Setup

## 1. Local environment

```bash
git clone https://github.com/yashashree5/causal-uplift-engine.git
cd causal-uplift-engine
python3.11 -m venv .venv && source .venv/bin/activate   # 3.10+ works; 3.11 recommended
pip install -e ".[dev,pipeline]"
cp .env.example .env    # fill in your values; never commit .env
pytest
```

Extras in `pyproject.toml`:

| Extra | For |
|---|---|
| `dev` | tests and linting |
| `pipeline` | extract, Snowflake load, dbt |
| `models` | CausalPFN, EconML, PyTorch, training (install on the GPU server) |

## 2. Snowflake (done once by the lead)

1. Sign up for a trial (30 days, $400 credits) or a student account if available. Choose **Standard edition**, AWS, a region near you.
2. As `ACCOUNTADMIN`, run [`warehouse/snowflake_setup.sql`](../warehouse/snowflake_setup.sql). It creates:
   - database `CAUSAL_UPLIFT` with schemas `RAW`, `STAGING`, `VALIDATED`, `ANALYTICS`
   - warehouse `UPLIFT_WH` (X-Small, auto-suspend 60 s) to keep credit use low
   - role `UPLIFT_DEV` for team members and role `UPLIFT_PIPELINE` for automation
   - service user `UPLIFT_CI` (key-pair auth only)
3. Create a user for each teammate and grant `UPLIFT_DEV`.
4. Set a resource monitor so the trial credits can't be used up by accident (included in the setup script).

### Key pair for the CI service user

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Paste the public key body into `ALTER USER UPLIFT_CI SET RSA_PUBLIC_KEY='...'`. Store the private key as the GitHub secret `SNOWFLAKE_PRIVATE_KEY`. Delete the local private key file afterwards or keep it in a password manager. Never commit it.

### GitHub secrets (Settings → Secrets and variables → Actions)

| Secret | Value |
|---|---|
| `SNOWFLAKE_ACCOUNT` | Account identifier, e.g. `orgname-accountname` |
| `SNOWFLAKE_USER` | `UPLIFT_CI` |
| `SNOWFLAKE_PRIVATE_KEY` | Contents of `rsa_key.p8` |
| `SNOWFLAKE_ROLE` | `UPLIFT_PIPELINE` |
| `SNOWFLAKE_WAREHOUSE` | `UPLIFT_WH` |
| `SNOWFLAKE_DATABASE` | `CAUSAL_UPLIFT` |

### If the trial ends

Switch dbt to the DuckDB target (`dbt build --target duckdb`) and keep working from the Parquet files on college storage. The SQL models are written to run on both.

## 3. dbt

```bash
cp warehouse/profiles.example.yml ~/.dbt/profiles.yml   # edit account and user
cd warehouse
dbt debug
dbt build            # runs models and tests
```

## 4. College GPU server

```bash
git clone --recurse-submodules https://github.com/yashashree5/causal-uplift-engine.git
pip install -e ".[models]"
python -c "import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_properties(0).total_memory / 1e9, 'GB')"
```

Record the GPU model, memory, and how jobs are submitted (SLURM or direct) in the Linear setup issue. Keep raw Parquet and snapshots under the shared project directory on college storage, not in your home directory.

## 5. Linear

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the GitHub integration and branch naming, and [LINEAR_BACKLOG.md](LINEAR_BACKLOG.md) for the issues to create.
