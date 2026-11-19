"""Download Hillstrom and Criteo with scikit-uplift and write raw Parquet + manifest.

Usage:
    python -m pipeline.extract --dataset hillstrom
    python -m pipeline.extract --dataset criteo

Linear: CUE M1 "pipeline/extract.py". Contract: docs/DATA_CONTRACTS.md section 1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _md5(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def fetch(dataset: str) -> pd.DataFrame:
    """Return the full raw table with outcomes and treatment, plus row_id in original order."""
    from sklift import datasets as sk  # imported lazily so tests don't need sklift

    if dataset == "hillstrom":
        bunch = sk.fetch_hillstrom(target_col="all")
        df = pd.concat([bunch.data, bunch.target, bunch.treatment.rename("segment")], axis=1)
    elif dataset == "criteo":
        bunch = sk.fetch_criteo(target_col="all", treatment_col="all", percent10=True)
        df = pd.concat([bunch.data, bunch.target, bunch.treatment], axis=1)
    else:
        raise ValueError(f"unknown dataset {dataset!r}")

    df = df.reset_index(drop=True)
    df.insert(0, "row_id", range(len(df)))
    return df


def write(df: pd.DataFrame, dataset: str, data_dir: Path) -> Path:
    out_dir = data_dir / "raw" / dataset
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{dataset}.parquet"
    df.to_parquet(path, index=False)

    import sklift

    manifest = {
        "dataset": dataset,
        "rows": int(len(df)),
        "columns": list(df.columns),
        "md5": _md5(path),
        "source": f"sklift.fetch_{dataset}",
        "sklift_version": sklift.__version__,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["hillstrom", "criteo"], required=True)
    parser.add_argument("--data-dir", default=os.environ.get("DATA_DIR", "./data"))
    args = parser.parse_args()

    df = fetch(args.dataset)
    if args.dataset == "hillstrom" and len(df) != 64_000:
        raise SystemExit(f"Hillstrom should have 64,000 rows, got {len(df)}")
    path = write(df, args.dataset, Path(args.data_dir))
    print(f"wrote {len(df):,} rows to {path}")


if __name__ == "__main__":
    main()
