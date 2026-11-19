# Literature Review

Every team member writes a literature review in their own folder, using the same template. The reviews feed the related-work section of the report and check that Model 1 is new.

## Structure

```
literature-review/
├── README.md          this file
├── READING_LIST.md    shared list of papers (verified links)
├── TEMPLATE.md        copy this into your folder as review.md
└── <your-name>/
    ├── review.md      your review (from TEMPLATE.md)
    └── notes/         optional: extra notes and figures
```

## The task (same for everyone)

1. Read the **core** papers in `READING_LIST.md` (marked **Core**).
2. Read the papers for your role (table below).
3. Search for papers since 2024 that we're missing, using the queries at the bottom of the reading list. Find at least 3.
4. Fill in `review.md`: paper notes, new papers, synthesis, and a related-work paragraph.
5. Open a PR titled `CUE-<n>: Literature review (<your name>)`, with `Fixes CUE-<n>` in the description.

**Done when:** all core papers and your role's papers have notes, at least 3 new papers are added to the reading list, and the synthesis answers "does anything already do what Model 1 does?"

## Who reads what

| Role | Focus | Papers (besides core) |
|---|---|---|
| 1. Data engineer | Datasets and how they were collected | D2, D3, D4, A4 |
| 2. Analytics engineer | Data quality, randomization, evaluation data | D2, D3, D4, B2 |
| 3. Baseline engineer | The baseline and PFN models | A2, A3, A4, B3 |
| 4. Model engineer | Neural uplift models and retrieval | B5, C2, A3, B3 |
| 5. Evaluation lead | Comparison methods, metrics, LLM work for Semester 2 | B2, D3, E1, E2 |

Core papers for everyone: A1 (CausalPFN), A5 (LoCalPFN), B1 (meta-learners), B4 (TARNet), C1 (FT-Transformer), D1 (Qini review).

## Rules

- Write in your own words. Quote at most one sentence per paper, in quotation marks.
- Record exact numbers with their table or figure number.
- Don't commit copyrighted PDFs. Link to arXiv or the publisher instead.
