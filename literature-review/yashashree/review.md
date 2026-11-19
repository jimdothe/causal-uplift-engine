# Literature Review: Yashashree Shinde

**Role:** 1. Data engineer (lead) · **Linear issue:** TEA-1

**Status:** first pass. Notes come from each paper's abstract plus the sections listed. A deeper second pass follows as the pipeline work needs it.

## Papers I took

| ID | Paper | Type |
|---|---|---|
| A1 | CausalPFN (Balazadeh et al., NeurIPS 2025) | Core |
| A5 | LoCalPFN: Retrieval & Fine-Tuning for In-Context Tabular Models (Thomas et al., NeurIPS 2024) | Core |
| B1 | Meta-learners for heterogeneous treatment effects (Künzel et al., PNAS 2019) | Core |
| B4 | TARNet / CFR (Shalit et al., ICML 2017) | Core |
| C1 | FT-Transformer: Revisiting Deep Learning Models for Tabular Data (Gorishniy et al., NeurIPS 2021) | Core |
| D1 | Causal Inference and Uplift Modelling: A Review (Gutierrez & Gérardy, 2017) | Core |
| D2 | Criteo benchmark for ITE prediction and uplift modeling (Diemert et al., 2021) | Role |
| D3 | UpliftBench: meta-learners and causal forests on Criteo (Singh, 2026) | Role |
| D4 | Hillstrom MineThatData e-mail challenge (2008) | Role |
| A4 | A Closer Look at TabPFN v2 (Ye et al., 2025) | Role |

## 1. Paper notes

### A1 CausalPFN (Balazadeh et al., 2025)

- **Link:** https://arxiv.org/abs/2506.07918 · code https://github.com/vdblm/CausalPFN
- **Problem:** estimate treatment effects without choosing and tuning a new estimator for every dataset.
- **Method:** a transformer pretrained on many simulated experiments. At prediction time it reads rows of a real experiment as context and outputs each new unit's outcome with and without treatment. On tables too large for the context, it trains a quick gradient-boosting model, sorts rows by that model's rough effect estimate, and reads the closest rows (Appendix D.2).
- **Data:** IHDP, ACIC, Lalonde, and five marketing experiments: Hillstrom, Criteo, X5, Lenta, Megafon.
- **Results:** normalized Qini in Table 2 (Hillstrom full 64k: 0.992 and 0.968; Criteo 50k sample: 0.859, X-Learner best). On full tables (Table 7) CausalPFN is 0.939 on Criteo, and S-Learner is best on every column except Megafon.
- **Limitations:** the authors list a performance drop on large tables, binary treatment only, and no instrumental-variable setting (Section 7). They suspect their row-selection step causes the drop.
- **Relevance to us:** our baseline. Model 1 targets the large-table drop. For the pipeline: folds depend on row order, so `row_id` must be kept from extract to snapshot. Hillstrom arm labels differ between the paper text and the code.
- **Open questions:** do we get the same Criteo row count from `percent10=True` that the paper reports (2.5M)?

### A5 LoCalPFN (Thomas et al., 2024)

- **Link:** https://arxiv.org/abs/2406.05207
- **Problem:** in-context tabular models (TabPFN) do well on small datasets but struggle on large, complex ones.
- **Method:** for each query, retrieve its nearest neighbors and use them as the context, then fine-tune TabPFN on these retrieved local contexts.
- **Data:** 95 OpenML datasets from TabZilla.
- **Results:** new state of the art on that benchmark, including against tuned tree models, and a large gain over plain TabPFN.
- **Limitations:** prediction only, not treatment effects.
- **Relevance to us:** the closest existing idea to Model 1. M1 differs by retrieving treated and control neighbors separately and estimating uplift. Retrieval at this scale needs a fast neighbor index, which affects my `neighbors.py` work. One LoCalPFN author is also a CausalPFN author, so a causal version may appear; we need to search again before each deliverable.
- **Open questions:** do they retrieve in raw feature space or a learned space?

### B1 Meta-learners (Künzel et al., 2019)

- **Link:** https://arxiv.org/abs/1706.03461
- **Problem:** estimate individual treatment effects using any standard machine learning model.
- **Method:** S-Learner (one model with treatment as a feature), T-Learner (separate models for treated and control), and the proposed X-Learner, which imputes individual effects and weights them by propensity.
- **Data:** simulations and two field experiments.
- **Results:** X-Learner works best when one group is much larger than the other.
- **Limitations:** quality depends on the underlying models.
- **Relevance to us:** S/T/X-Learners are the comparison methods in the paper's tables. Criteo is 85% treated, which is the unbalanced setting where X-Learner should help.

### B4 TARNet / CFR (Shalit et al., 2017)

- **Link:** https://arxiv.org/abs/1606.03976
- **Problem:** learn individual treatment effects from data with neural networks, with a guarantee on error.
- **Method:** a shared representation network with two outcome heads, one per group. CFR adds a penalty that makes the treated and control representations look alike. The paper bounds the error of the estimated effect.
- **Data:** IHDP (semi-synthetic) and Jobs.
- **Relevance to us:** M1a follows this design (shared encoder plus two heads). Our data is randomized, so the balancing penalty matters less than in observational data.

### C1 FT-Transformer (Gorishniy et al., 2021)

- **Link:** https://arxiv.org/abs/2106.11959
- **Problem:** which deep learning models actually work on tabular data?
- **Method:** compares strong baselines and proposes FT-Transformer: each feature becomes a token (value × learned vector + bias), then a standard transformer encoder.
- **Results:** FT-Transformer is strong across many datasets, but there's no universal winner over gradient-boosted trees.
- **Relevance to us:** M1's encoder. The "no universal winner" finding is why we keep S-Learner and gradient-boosting comparisons.

### D1 Uplift modelling review (Gutierrez & Gérardy, 2017)

- **Link:** https://proceedings.mlr.press/v67/gutierrez17a/gutierrez17a.pdf
- **Problem:** connect uplift modeling (marketing) with causal inference (statistics).
- **Method:** reviews approaches (two-model, class transformation, direct tree methods) and evaluation with uplift and Qini curves.
- **Relevance to us:** the CausalPFN code cites this paper for its Qini curve. Our `eval/qini.py` matches that code exactly.

### D2 Criteo benchmark (Diemert et al., 2021)

- **Link:** https://arxiv.org/abs/2111.10106
- **Problem:** treatment-effect research lacks large public randomized datasets.
- **Method:** releases 13.9 million samples from several randomized ad tests (210× larger than earlier datasets), with sanity checks that the data is valid for causal work, a formal uplift task, and metrics.
- **Relevance to us:** the source of our main dataset. Key pipeline facts: `treatment` is randomized; `exposure` (actually shown an ad) isn't, so it must never be used as the treatment. The features are anonymized.
- **Open questions:** which version does scikit-uplift's `percent10` sample come from, and how many rows does it have?

### D3 UpliftBench (Singh, 2026)

- **Link:** https://arxiv.org/abs/2604.06123
- **Problem:** few benchmarks of uplift methods at industrial scale.
- **Method:** S-, T-, X-Learner (LightGBM) and causal forest on full Criteo v2.1 (13.98M rows).
- **Results:** treatment assignment looks random (propensity AUC 0.509). S-Learner has the highest Qini (0.376). The top 20% by predicted effect capture 77.7% of incremental conversions.
- **Relevance to us:** independent numbers on full Criteo. Their propensity-AUC check is a cheap randomization test we can add to the dbt checks. Note the outcome is conversion, not visit, so the numbers aren't directly comparable to CausalPFN's.

### D4 Hillstrom MineThatData challenge (2008)

- **Problem:** which e-mail campaign (men's, women's, none) drives visits and purchases?
- **Data:** 64,000 customers who purchased within the last twelve months, randomly split into thirds. Visits, conversions, and spend were tracked for two weeks.
- **Relevance to us:** the Hillstrom row count (64,000) and the three arms are the first dbt tests in the pipeline.

### A4 A Closer Look at TabPFN v2 (Ye et al., 2025)

- **Link:** https://arxiv.org/abs/2502.17361
- **Problem:** why does TabPFN v2 work, and how can its limits on high-dimensional, many-category, and large-scale tasks be reduced?
- **Method / results:** it infers feature relationships even with randomized feature tokens; it can be used as a feature extractor; a test-time divide-and-conquer strategy scales it without retraining.
- **Relevance to us:** another way to handle large tables (split, then combine) that we should mention next to retrieval.

## 2. New papers found

| Paper | Link | Year | Why it matters |
|---|---|---|---|
| Shi et al., **TERRA: A Transformer-Enabled Recursive R-learner for Longitudinal HTE Estimation** | https://arxiv.org/abs/2510.22407 | 2025 | A transformer for treatment effects over time; related transformer design, different setting |
| Sapru, **Guardrailed Uplift Targeting: A Causal Optimization Playbook for Marketing Strategy** | https://arxiv.org/abs/2512.19805 | 2025 | Turns uplift estimates into targeting decisions under budget limits; useful for our business-value results |
| Panagopoulos et al., **Uplift Modeling Under Limited Supervision** | https://arxiv.org/abs/2403.19289 | 2024 | Reduces how much experiment data uplift models need; related to our small-data comparison |

## 3. Synthesis

**What is already solved?** Pretrained in-context models (CausalPFN) estimate effects well on tables that fit their context. Retrieval fixes much of the large-table problem for ordinary prediction (LoCalPFN, TabR).

**What is still open?** CausalPFN still drops on full large marketing tables (its Table 7), and its authors list scaling as future work.

**Does anything already do what our Model 1 does?** Not found in this first pass. LoCalPFN and TabR retrieve neighbors for prediction, not uplift. CausalPFN retrieves for uplift, but by a single rough effect score and without training on the real data. Searches run: `CausalPFN`, `retrieval augmented uplift modeling`, `uplift modeling transformer`. Needs a full "cited by" check on CausalPFN.

**Risks this review uncovered:**
- The Criteo row count may differ from the paper's 2.5M; record it at extract.
- Results on Criteo conversion (UpliftBench) and visit (CausalPFN) shouldn't be compared directly.
- A causal version of LoCalPFN could appear from the same group.

## 4. Related-work paragraph for the report

Uplift models estimate how much a treatment changes each person's outcome. Classic approaches combine standard learners (S-, T-, X-Learner [B1]) or use causal forests [B2], and neural models share an encoder with separate outcome heads [B4]. CausalPFN [A1] instead pretrains a transformer on simulated experiments and estimates effects in-context, matching or beating these methods on marketing experiments, but its accuracy drops on full large tables such as Criteo [D2]. For ordinary tabular prediction, retrieving each query's nearest neighbors as context, with fine-tuning, addresses the same scaling problem [A5, C2], and test-time divide-and-conquer is another option [A4]. Our Model 1 brings retrieval to uplift estimation by attending separately to similar treated and untreated customers, trained on the full campaign.
