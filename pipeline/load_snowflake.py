"""Load raw Parquet into Snowflake CAUSAL_UPLIFT.RAW (PUT to a stage, then COPY INTO).

Usage:
    python -m pipeline.load_snowflake --dataset hillstrom

Re-running replaces the table, so loads are idempotent.
Auth: key-pair only (SNOWFLAKE_PRIVATE_KEY or SNOWFLAKE_PRIVATE_KEY_PATH). See docs/SETUP.md.
Linear: CUE M1 "pipeline/load_snowflake.py".
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def _private_key_der() -> bytes:
    from cryptography.hazmat.primitives import serialization

    pem = os.environ.get("SNOWFLAKE_PRIVATE_KEY")
    if pem is None:
        key_path = os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"]
        pem = Path(key_path).read_text()
    key = serialization.load_pem_private_key(pem.encode(), password=None)
    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def connect():
    import snowflake.connector

    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        private_key=_private_key_der(),
        role=os.environ.get("SNOWFLAKE_ROLE", "UPLIFT_PIPELINE"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "UPLIFT_WH"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "CAUSAL_UPLIFT"),
        schema="RAW",
    )


def load(dataset: str, data_dir: Path) -> int:
    parquet = (data_dir / "raw" / dataset / f"{dataset}.parquet").resolve()
    if not parquet.exists():
        raise FileNotFoundError(f"{parquet} not found; run pipeline.extract first")

    table = dataset.upper()
    stage = f"RAW_STAGE_{table}"
    statements = [
        f"CREATE STAGE IF NOT EXISTS {stage} FILE_FORMAT = (TYPE = PARQUET)",
        f"REMOVE @{stage}",
        f"PUT 'file://{parquet.as_posix()}' @{stage} AUTO_COMPRESS = FALSE OVERWRITE = TRUE",
        # Create the table from the Parquet schema, then load by column name.
        # IGNORE_CASE uppercases column names so SQL doesn't need quoted lowercase identifiers.
        f"""CREATE OR REPLACE TABLE {table} USING TEMPLATE (
              SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
              FROM TABLE(INFER_SCHEMA(LOCATION => '@{stage}', FILE_FORMAT => '{stage}_FMT',
                                      IGNORE_CASE => TRUE)))""",
        f"""COPY INTO {table} FROM @{stage}
              FILE_FORMAT = (FORMAT_NAME = '{stage}_FMT')
              MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE""",
    ]
    with connect() as conn, conn.cursor() as cur:
        cur.execute(f"CREATE FILE FORMAT IF NOT EXISTS {stage}_FMT TYPE = PARQUET")
        for sql in statements:
            cur.execute(sql)
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        (rows,) = cur.fetchone()
    return int(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["hillstrom", "criteo"], required=True)
    parser.add_argument("--data-dir", default=os.environ.get("DATA_DIR", "./data"))
    args = parser.parse_args()
    rows = load(args.dataset, Path(args.data_dir))
    print(f"loaded {rows:,} rows into RAW.{args.dataset.upper()}")


if __name__ == "__main__":
    main()
