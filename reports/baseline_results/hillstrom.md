# Hillstrom baseline results

The [executed Hillstrom notebook](../../notebooks/baseline_hillstrom.ipynb) ran CausalPFN and four classical comparators on both email arms. All **50 method-folds** completed in **249.6 seconds**. The notebook includes the captured fold outputs and both Table 2 mappings.

[Aggregate scores (CSV)](hillstrom.csv)

## Women's email vs. no email

The five held-out folds cover all **42,693** rows.

| Method | Qini | Normalized Qini | Table 2 notebook mapping | Table 2 prose mapping |
| --- | ---: | ---: | ---: | ---: |
| X-learner | 0.669640 | 1.000000 | 0.975 | 0.980 |
| DA-learner | 0.666195 | 0.994856 | 0.985 | 0.964 |
| T-learner | 0.655225 | 0.978474 | 0.991 | 0.972 |
| S-learner | 0.654741 | 0.977751 | 1.000 | 1.000 |
| CausalPFN | 0.639788 | 0.955421 | 0.992 | 0.968 |

## Men's email vs. no email

The five held-out folds cover all **42,613** rows.

| Method | Qini | Normalized Qini | Table 2 notebook mapping | Table 2 prose mapping |
| --- | ---: | ---: | ---: | ---: |
| CausalPFN | 0.518377 | 1.000000 | 0.968 | 0.992 |
| S-learner | 0.517034 | 0.997410 | 1.000 | 1.000 |
| DA-learner | 0.514872 | 0.993239 | 0.964 | 0.985 |
| T-learner | 0.513419 | 0.990435 | 0.972 | 0.991 |
| X-learner | 0.495451 | 0.955773 | 0.980 | 0.975 |

The authors' notebook uses Hill(1) for women's email and Hill(2) for men's email. The paper's prose reverses the labels. The CausalPFN gaps from Table 2 are -0.0366 for women and +0.0320 for men under the notebook mapping, and -0.0126 and +0.0080 under the prose mapping. [Paper](https://arxiv.org/html/2506.07918v2) · [Authors' notebook](https://github.com/vdblm/CausalPFN/blob/7da4afa35affea0f1fb58893e9f41e87dafdc7eb/notebooks/qini.ipynb)

## Run details

- The notebook verified the original scikit-uplift archive (MD5 a68a81291f53a14f4e29002629803ba3) and the published CausalPFN checkpoint. It used upstream revision 7da4afa and an RTX 4080 SUPER. [Hillstrom data loader](https://www.uplift-modeling.com/en/latest/_modules/sklift/datasets/datasets.html#fetch_hillstrom)
- The two arm comparisons use website visit as the outcome and five shuffled folds stratified by treatment and outcome with root seed 82718. The notebook verified row IDs, treatment, and visit labels across all methods.
- This run trained the four classical comparators in team runner order (X, S, DA, T) within each arm. The authors' full benchmark uses a different execution order, which affects the random-number sequence.
- Qini comes from pooled held-out predictions. Normalized Qini divides each score by the best Qini among the five methods for the same arm. [Scoring code](../../eval/qini.py)
