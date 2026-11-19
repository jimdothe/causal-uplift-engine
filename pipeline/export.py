"""Export VALIDATED tables from Snowflake to Parquet, sorted by row_id.

Owner: Person 2. Linear: CUE M1 "pipeline/export.py".

Requirements:
- Read CAUSAL_UPLIFT.VALIDATED.<dataset>.
- ORDER BY row_id (the authors' folds depend on row order).
- Write data/validated/<dataset>/<dataset>.parquet and a manifest with row count and MD5.
- Check that row_id is exactly 0..N-1 with no gaps.
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("CUE M1: export validated tables")


if __name__ == "__main__":
    main()
