"""Model 1: retrieval uplift transformer. Design in docs/PROJECT_PLAN.md section 6.1.

Owner: Person 4. Linear: CUE milestones M4 (M1a) and M5 (M1b).

Planned modules:
- encoder.py              feature tokenizer + transformer encoder → customer vector
- retrieval_attention.py  attention over treated / control neighbors (M1b)
- model.py                M1a (two heads) and M1b (retrieval heads)
- losses.py               arm-weighted BCE on the observed arm
- train.py                training loop, checkpoints, resume, W&B, early stopping on val Qini
"""
