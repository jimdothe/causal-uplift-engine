"""Build model-ready snapshots using the CausalPFN authors' exact preprocessing and folds.

Owner: Person 3. Linear: CUE M2 "pipeline/prepare.py" and "Equality test".

Requirements:
- Use the authors' benchmark classes (third_party/CausalPFN/benchmarks: HillstromDataset,
  CriteoDataset) with seed 82718 and n_folds 5, for every task in configs/datasets.yaml.
- Save X, t, y, row_id, folds, manifest per docs/DATA_CONTRACTS.md section 3.
- Rebuild the same arrays from data/validated/*.parquet with our own code and assert they are
  identical to the authors' arrays. Record the result in the manifest. Stop if they differ.
- Do not change preprocessing until the reproduction passes (project plan, section 5).
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("CUE M2: prepare snapshots")


if __name__ == "__main__":
    main()
