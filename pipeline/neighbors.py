"""Precompute fold-aware nearest-neighbor lists for Model 1b.

Owner: Person 1. Linear: CUE M2 "pipeline/neighbors.py".

Requirements (docs/DATA_CONTRACTS.md section 4):
- For each task and fold k, index only fold k's TRAINING rows, separately for treated and control.
- For every row (train and test), store the K nearest treated and K nearest control training rows.
- A training row must never be its own neighbor.
- Features are standardized with statistics from the training fold only.
- Output: neighbors_fold<k>.npz with arrays `treated` and `control`, int64 [N, K].
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("CUE M2: neighbor lists")


if __name__ == "__main__":
    main()
