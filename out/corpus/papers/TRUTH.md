# Ground truth for the machine corpus from its own papers (2026-11-10)

Status: built and scored; **not reviewed by a person**. The builder and the only reader of the verification sample are the same model, so every figure here is a model proxy's. Files: `truth.json` (items, mappings, confidence, renumbering, verification), `BASELINES.md` / `baselines.json` (scores), `src/` (hand-written item files and the builder), `bench/paper_truth.py` (scorer).

## What it is

- **117 paper items** (86 Navier-Stokes, 31 Euler), each with section, number, a one-sentence paraphrase and the paper's own proof steps in order, mapped to **333 mappings onto 321 distinct Lean declarations** of `out/corpus/ns/decls.jsonl`.
- Each mapping has a relation (`states` 120, `part` 153, `defines` 60), an evidence sentence and a confidence.
- A scorer that takes any ranked list or outline and reports how many items it reaches at each depth.

## Sources

| paper | URL | version |
|---|---|---|
| Finite time blowup for Navier-Stokes (OpenAI), 166 pages | https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf | PDF created 2026-09-08 15:06 EDT; Last-Modified 2026-09-08 19:09 GMT; sha256 `0e779481…ae228f` |
| Finite time blowup for the Euler equation (OpenAI), 57 pages | https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf | PDF created 2026-09-08 15:07 EDT; Last-Modified 2026-09-08 19:13 GMT; sha256 `a0c23451…54bfdd` |

Both URLs are the ones in `corpora/ns/README.md` and `formalization.yaml`. Fetched 2026-11-10 with `curl`, text extracted with `pdftotext -layout`. The PDFs and extracted text were kept outside the repository; the repository holds paraphrases only.

## Method

1. **Items.** Navier-Stokes: every numbered Theorem, Proposition, Lemma, Corollary, Definition and Remark found by a line-start pattern in the extracted text (80), plus 6 equation-numbered definitions picked by the builder from the paper's symbol table. Euler has only 5 numbered results, so its item set also takes the 7 numbered claims inside Propositions 3.1 and 4.1, 12 equation-numbered definitions from the paper's notation index, and 7 numbered subsections of Sections 5 and 6 that the paper's proof outline names as steps.
2. **Proof steps** are the paper's: the "Step n" headings or opening sentences of each proof, and for the main theorems the proof outline (Navier-Stokes Section 3, Euler Section 2.3).
3. **Mapping.** In this order: (a) docstrings that cite an item, by published number or by TeX label (`seed:cone-test`, `heat:flat-primitive`, ...); (b) the paper-facing modules imported by `NavierStokes/PaperResults.lean`; (c) docstrings citing the earlier manuscript, after renumbering; (d) the closing theorems of the module whose name and docstring match the item's topic; (e) statement comparison for the sample below.
4. **Confidence.** `certain`: cited in the published numbering or TeX label, named in the README, or the statement was read against the paper and agrees. `probable`: cited in the old numbering with content matched, or docstring/statement describes the item. `guess`: name only.
5. **Verification.** 20 of the 333 mappings drawn with `random.Random(20261110)`, Lean statement (as exported, cut at 2,000 characters) read against the paper statement.

## Coverage

Items by their best mapping:

| | items | certain | probable | guess | no Lean counterpart |
|---|---|---|---|---|---|
| Navier-Stokes | 86 | 20 | 59 | 6 | 1 |
| Euler | 31 | 4 | 27 | 0 | 0 |

By kind (certain / probable / guess / none):

| Navier-Stokes | n | c / p / g / none | | Euler | n | c / p / g / none |
|---|---|---|---|---|---|---|
| theorems | 3 | 2 / 1 / 0 / 0 | | theorem | 1 | 1 / 0 / 0 / 0 |
| propositions | 26 | 5 / 21 / 0 / 0 | | propositions | 2 | 0 / 2 / 0 / 0 |
| lemmas | 38 | 9 / 28 / 1 / 0 | | lemmas | 2 | 0 / 2 / 0 / 0 |
| corollaries | 7 | 1 / 2 / 4 / 0 | | claims of Props 3.1, 4.1 | 7 | 0 / 7 / 0 / 0 |
| numbered definitions | 5 | 0 / 3 / 1 / 1 | | equation-numbered definitions | 12 | 2 / 10 / 0 / 0 |
| remark | 1 | 0 / 1 / 0 / 0 | | section-level steps | 7 | 1 / 6 / 0 / 0 |
| equation-numbered definitions | 6 | 3 / 3 / 0 / 0 | | | | |

Mappings: Navier-Stokes 243 (37 certain, 193 probable, 13 guess); Euler 90 (7 certain, 79 probable, 4 guess).

**No counterpart found (1):** Navier-Stokes Definition 3.3 (the "alpha << beta" order-of-choices convention). Lean discharges it as nested explicit quantifiers; there is nothing to point at.

**Guess only (6, all Navier-Stokes):** Definition 3.2 (regularity at the axis: no named predicate, stated as Cartesian `ContDiff` each time); Lemma 4.4 (stress depends on the profile through five integrals: no single statement found); Corollary 7.3 (one domain for all solution operators: built into the fixed threshold `N0`); Corollary 7.8 (covariance change: the identity sits inside the mean-gain theorems); Corollary 8.5 (covariance targets: found by module name only); Corollary B.6 (its statement is in the extracted text, split over two lines; each of the two mappings covers one clause).

**Two facts about where the targets sit.**
- Only 53 of the 85 mapped Navier-Stokes items have any target below the whole-space headline theorem (101 of 233 target declarations); for Euler 29 of 31 (70 of 88). Much of the paper-facing restatement layer (`SeedConePaper`, `AppendixHeatResults`, `LocalPaperTheorem`, ...) is not used by the headline proof. An outline grown from the headline root cannot reach those items exactly.
- 202 of 233 Navier-Stokes targets have a docstring; only 35 of 88 Euler targets do. The Euler development cites the paper almost only by old equation numbers.

## Renumbering

The Lean docstrings cite two generations of the papers. `NavierStokes/R3/*`, `LocalPaper*`, `PeriodicPaper*` and the modules imported by `PaperResults.lean` use the published numbering. Earlier modules cite a "candidate manuscript" with eleven sections, one appendix and equations numbered (1) to (39) straight through. That manuscript is not in the repository, so the table in `truth.json` (`renumbering`, 33 Navier-Stokes rows and 11 Euler rows) was established from content. In outline:

| old | published | basis |
|---|---|---|
| Section 3 (Prop 3.2, Lemmas 3.3, 3.5, 3.6, 3.7; eqs (3)-(11)) | Section 4 (Prop 4.2, Lemmas 4.3, 4.5, 4.7 = A.1 + A.2) | statement for 3.5 and 3.6, content for the rest |
| Sections 4, 5, 6 (Prop 5.1, Lemma 5.2, Lemma 6.1, Prop 6.2) | Appendices A, B, C (Prop B.2, Lemma B.4, Lemma C.1, Prop C.2) | content |
| Section 8 (Def 8.1, Lemmas 8.3, 8.4, 8.5, 8.7, 8.8; eqs (25)-(29)) | Sections 6 and 7 (phase map (6.3), Lemma 6.1, Prop 7.2, Lemma 7.4, Prop 7.5, Lemma 7.7; (7.3), (7.5), (7.21)) | statement for (26) = (7.3), content for the rest |
| Prop 9.3 | Prop 9.1 | content |
| eqs (32)-(35); Section 10.2; Prop 10.3 | (8.3), (8.12), (8.16), (8.25); Prop 7.6; Prop 9.6 | content; Section 10.2 by topic |
| Lemma 11.3, Props 11.4, 11.7 | Lemma 5.4, Prop 10.1 / Lemma 10.3, Section 10.4 | content |
| Euler eq (30) | (4.21) | statement |
| Euler eqs (9), (16)-(17), (35)-(37), (39) | (3.19)-(3.21), Section 3.6, (4.11), (4.12), (5.3), Section 5.5 | content |

Nine rows are `guess` (topic only). "Lemma 9.2" in `CurlClassBounds.lean` is published Lemma 7.7 by content (independent check, 2026-11-10).

## Verification of 20 sampled mappings

| verdict | n | meaning |
|---|---|---|
| match | 12 | the Lean statement says what the paper item (or the mapped clause) says |
| partial | 7 | one clause matches, or the statement is longer than the 2,000-character export and was not read to the end |
| weak | 1 | a related record only (`EulerParentPacketFrames.SmoothState` for the shear decomposition (4.3)) |

- 12 of 20 is 60% (95% interval about 39% to 78%); 19 of 20 are match or partial.
- **Independent check (2026-11-10; a second model reader, not the builder, still a proxy).** 15 further mappings, 5 per confidence level, seed 20261112, all Navier-Stokes. certain: 4 correct, 1 `states` that should be `part`; probable: 4 correct, 1 `states` that should be `part`; guess: 2 partial, 2 weak, 1 wrong (`physical_normalCoefficient_class` belongs to Lemma 7.7, not 9.2). Wrong at certain or probable: 0 of 10 (95% interval 0% to 31%). Euler mappings were not drawn. Data: `out/corpus/review_maths2/truth_check/verdicts.json`.
- Corrections applied from the sample: 8 mappings raised to `certain`, 1 lowered to `guess`, 2 relations changed. The per-mapping notes are in `truth.json` (`verification.sample`).
- The reader was the builder. This is a consistency check, not an independent one.

## Baseline scores

`python3 bench/paper_truth.py --baselines` (about 35 s). Cell = exact / near hits; full tables at three confidence cut-offs in `BASELINES.md`. All mapped items, any confidence:

| Navier-Stokes, 85 items | listed | k=20 | k=50 | k=100 | k=1000 | all |
|---|---|---|---|---|---|---|
| dominator outline `ns_r3` | 69 | 6 / 20 | 8 / 49 | | | 8 / 56 |
| ... levels 1 to 3 only, without the toolkit | 45 | | | | | 8 / 22 |
| largest proof beneath it | 36,203 | 5 / 8 | 7 / 15 | 8 / 16 | 10 / 20 | |
| own proof size | 36,203 | 0 / 0 | 4 / 11 | 10 / 24 | 30 / 55 | |
| has a docstring, ordered by proof mass beneath | 7,671 | 7 / 11 | 8 / 16 | 9 / 19 | 32 / 50 | 83 / 85 |
| has a docstring, random order (mean of 200) | 7,671 | 0.5 / 8.4 | 1.4 / 16.5 | 2.7 / 25.8 | 24.4 / 74.3 | |
| any declaration, random order (mean of 200) | 36,203 | 0.1 / 6.1 | 0.3 / 11.6 | 0.6 / 17.4 | 6.2 / 59.8 | |

| Euler, 31 items | listed | k=20 | k=50 | k=100 | k=1000 | all |
|---|---|---|---|---|---|---|
| dominator outline `euler_compact` | 65 | 1 / 14 | 4 / 27 | | | 4 / 27 |
| largest proof beneath it | 16,302 | 2 / 4 | 4 / 11 | 6 / 14 | 10 / 20 | |
| own proof size | 16,302 | 1 / 8 | 2 / 13 | 4 / 18 | 13 / 27 | |
| has a docstring, ordered by proof mass beneath | 4,839 | 1 / 10 | 2 / 13 | 3 / 15 | 11 / 23 | 22 / 31 |
| has a docstring, random order (mean of 200) | 4,839 | 0.1 / 4.1 | 0.4 / 8.1 | 0.8 / 12.0 | 6.7 / 27.7 | |
| any declaration, random order (mean of 200) | 16,302 | 0.1 / 5.8 | 0.3 / 10.2 | 0.6 / 14.3 | 5.1 / 28.2 | |

What the numbers say:

- **The dominator outline reaches 8 of 85 Navier-Stokes items and 4 of 31 Euler items exactly**, against 0.4 and 0.4 for the same number of random declarations. It is far above chance and covers about a tenth of the paper.
- **"Largest proof beneath it" saturates.** It finds the headline theorems and their wrappers first (5 items in 20) and then stalls: 10 of 85 at k=1000. Ranking by the declaration's own proof size overtakes it from k=100 (30 at k=1000).
- **A docstring is the strongest cheap signal for Navier-Stokes and a weak one for Euler.** Random docstringed declarations hit 4 times as many items as random declarations at k=1000 (24 against 6), and the docstringed set contains a target for 83 of 85 items. In Euler it contains a target for 22 of 31.
- **Near hits must be read against the random rows.** One dependency step from 50 random Navier-Stokes declarations already touches 12 of 85 items, and from 1,000 touches 60. The outline's jump from 22 to 56 near hits comes from its 24 toolkit entries, which are hubs. Exact hits are the informative column.

## Limitations

- Built by a model in one pass; no mathematician has read the paraphrases, the proof steps or the mappings. The proof-step lists for the 80 smaller results come from the first lines of each proof.
- The Lean development is far more granular than the paper (52,505 declarations for 117 items). Each item is mapped to 1 to 5 declarations chosen as its statement, closing theorem or definition; many other declarations belong to the same item and are not listed. A list can therefore miss an item "exactly" while showing one of its unlisted lemmas.
- 193 + 79 mappings are `probable`; most of those rest on a docstring that describes the content, or on being the closing theorem of the matching module. The sample puts the share that fully match near 60%.
- Statements were read from the export, which cuts at 2,000 characters; 3 of the 7 partial verdicts are due to that.
- `pdftotext` scrambles displayed formulas. Paraphrases of formula-heavy statements (Theorem 4.6, Propositions 4.10, 9.3) are coarse. Corollary B.6's heading is split over two lines by the extraction, which is why it was first missed.
- The Euler item set had to be widened beyond numbered results by the builder's choice, which Rule 2 of the plan warns against; the equation-numbered definitions in both papers are also the builder's selection. `kind` in `truth.json` lets a scorer drop them.
- "Near" counts either direction of dependency and is inflated by hubs.

## Reproduce

```sh
python3 out/corpus/papers/src/build_truth.py     # truth.json from src/items_*.py; fails on an unresolved name
python3 bench/paper_truth.py --test              # scorer self-test
python3 bench/paper_truth.py --baselines         # BASELINES.md, baselines.json
python3 bench/paper_truth.py --outline out/corpus/outline/outline.json --key ns_r3
python3 bench/paper_truth.py --ranking my_list.json --paper ns --min-confidence probable
```

## Next actions

1. Have a second, independent reader (a person if one is available) redo the 20-mapping sample and a fresh sample of 20 from the `probable` mappings only.
2. Score the definition-centred outline of M2 with this scorer, at `--min-confidence probable`, next to the rows above.
3. Add a hub-discounted near hit (ignore neighbours with more than a fixed number of users) so the near column carries information.
4. Extend each item from a few declarations to the set of modules that implement it, so coverage can be reported by proof mass as well as by item.
5. Re-export the long statements without the 2,000-character cut to settle the partial verdicts.
