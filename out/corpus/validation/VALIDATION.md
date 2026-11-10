# H3 validation: does graph structure predict what humans put in the blueprint? (2026-11-10)

**H3:** "declarations that humans put in the blueprint can be predicted from the dependency graph alone."

**Verdict: negative for the dominator idea, weak for the graph as a whole.**

- **Graph features carry a real but modest signal.** A graph-only model reaches ROC-AUC 0.85 (PFR) and 0.87 (Carleson), but at k = number of blueprint nodes only 62% and 46% of its picks are blueprint theorems.
- **The dominator tree adds nothing.** Adding every dominator feature to the naive graph baselines changes AUC by +0.001 in both projects, with intervals that straddle zero in all eight ablations.
- **The signal is size, not structure.** Dominated proof mass is statistically indistinguishable from the declaration's own proof size and from its out-degree. "Big proof that uses many things" is what is being detected.
- **Normalising by statement size hurts.** Blueprint theorems have *larger* statements than the rest (median 383 vs 191 nodes in PFR, 1,477 vs 239 in Carleson), so "short statement, large hidden mass" points the wrong way.
- **Surface cues beat the graph.** "Has a docstring" alone matches or beats the best single graph score, and a four-feature surface model beats the full graph model in both projects.
- **Structure agrees better than membership.** Lean reachability between blueprint nodes recovers 87–94% of the human `\uses` edges. The dominator tree's parent relation is precise (0.71) but recalls only 19% (PFR) and 58% (Carleson) of them.
- **One positive observation for the outline use-case.** The top "false positives" are mostly not noise: 20 of the top 25 in PFR and 17 of 25 in Carleson are a dominator-tree neighbour or a primed/`_aux` variant of a blueprint declaration.

Everything below is produced by `bench/validate_outline.py` and `bench/validate_outline_extra.py` from the exported Lean data. The full tables for every evaluation set are in `tables.md`; numbers are in `results.json`.

## Setup

| | PFR | Carleson |
|---|---|---|
| declarations / edges (type ∪ value, deduplicated) | 1,118 / 4,877 | 3,199 / 25,554 |
| headline roots (from `axioms.json`) | 12 | 4 |
| reachable from the roots | 830 | 2,349 |
| nontrivial dominators | 242 | 628 |
| blueprint nodes (= k) | 219 | 180 |
| blueprint-tagged project declarations | 247 | 236 |
| theorems, tagged / all | 225 / 978 (23.0%) | 229 / 2,675 (8.6%) |
| mainline theorems, tagged / all | 145 / 310 (46.8%) | 224 / 1,486 (15.1%) |

- **Dominator tree:** computed from a virtual root that uses every headline theorem. Dominated mass and transitive mass were checked against brute force (delete the node, recount) on 150 random declarations per project with no mismatch.
- **Proof mass:** `proofSize + auxProofSize` (distinct subterms), summed over the relevant set, including the declaration itself unless marked "excl. own".
- **Unreachable declarations:** dominator scores are 0 and depth is set to worst.
- **Evaluation sets:** `T-all` is all theorems (primary). `T-main` drops the staging folders (`PFR/Mathlib`, `PFR/ForMathlib`, `Carleson/ToMathlib`, …) that the blueprints do not try to cover. `T-main-reach` and `SPEC` (tagged declarations of any kind plus untagged theorems, the task's literal wording) are in `tables.md` and tell the same story.
- **Intervals:** 95% percentile bootstrap, 1,000 resamples of declarations, the same resamples for every score so differences are paired.
- **k:** the number of blueprint nodes. In PFR `T-main` k = 219 exceeds the 145 positives, so precision@k cannot exceed 0.66 there.
- **Carleson has two genuine 2-cycles** (`mutual` theorems `I1_prop_1`/`I3_prop_1` and `I2_prop_2`/`I3_prop_2`); the script handles cycles.

## Single scores, all theorems (`T-all`)

PFR: n = 978, 225 positives, k = 219. Carleson: n = 2,675, 229 positives, k = 180.

| score | PFR AUC | PFR AP | PFR P@k | PFR R@k | Carleson AUC | Carleson AP | Carleson P@k | Carleson R@k |
|---|---|---|---|---|---|---|---|---|
| (a) dominated proof mass (incl. own) | 0.78 [0.74, 0.81] | 0.56 [0.49, 0.63] | 0.54 [0.47, 0.62] | 0.53 [0.48, 0.58] | 0.84 [0.80, 0.87] | 0.35 [0.30, 0.41] | 0.44 [0.37, 0.51] | 0.34 [0.29, 0.40] |
| (a') dominated proof mass (excl. own) | 0.65 [0.62, 0.69] | 0.43 [0.36, 0.49] | 0.45 [0.38, 0.52] | 0.44 [0.38, 0.50] | 0.73 [0.69, 0.77] | 0.28 [0.23, 0.34] | 0.45 [0.37, 0.51] | 0.35 [0.29, 0.40] |
| (b) is nontrivial dominator | 0.64 [0.60, 0.67] | 0.32 [0.28, 0.37] | 0.43 [0.36, 0.49] | 0.42 [0.36, 0.47] | 0.70 [0.67, 0.74] | 0.17 [0.14, 0.20] | 0.25 [0.19, 0.31] | 0.20 [0.15, 0.24] |
| (b) dominator depth (shallower = higher) | 0.63 [0.59, 0.67] | 0.29 [0.25, 0.33] | 0.31 [0.25, 0.37] | 0.30 [0.25, 0.35] | 0.57 [0.54, 0.60] | 0.09 [0.08, 0.11] | 0.06 [0.02, 0.09] | 0.04 [0.02, 0.07] |
| (c) transitive proof mass beneath | 0.83 [0.80, 0.86] | 0.59 [0.52, 0.67] | 0.63 [0.53, 0.70] | 0.61 [0.55, 0.66] | 0.86 [0.84, 0.88] | 0.29 [0.25, 0.34] | 0.35 [0.27, 0.42] | 0.28 [0.23, 0.33] |
| (d) own proof size | 0.77 [0.73, 0.80] | 0.56 [0.49, 0.63] | 0.52 [0.45, 0.59] | 0.51 [0.45, 0.56] | 0.81 [0.79, 0.84] | 0.31 [0.25, 0.37] | 0.36 [0.28, 0.42] | 0.28 [0.23, 0.33] |
| (e) in-degree (users) | 0.55 [0.51, 0.58] | 0.27 [0.23, 0.32] | 0.24 [0.18, 0.29] | 0.23 [0.18, 0.28] | 0.53 [0.50, 0.56] | 0.09 [0.08, 0.11] | 0.09 [0.05, 0.14] | 0.07 [0.04, 0.11] |
| (e) PageRank, rank flows to used declarations | 0.50 [0.46, 0.54] | 0.23 [0.20, 0.27] | 0.19 [0.15, 0.24] | 0.19 [0.14, 0.23] | 0.39 [0.36, 0.42] | 0.06 [0.06, 0.07] | 0.02 [0.00, 0.03] | 0.01 [0.00, 0.03] |
| (e) PageRank, rank flows to users | 0.79 [0.75, 0.82] | 0.54 [0.47, 0.61] | 0.56 [0.50, 0.63] | 0.55 [0.50, 0.61] | 0.81 [0.78, 0.84] | 0.30 [0.25, 0.36] | 0.36 [0.29, 0.42] | 0.28 [0.23, 0.33] |
| (f) statement size, negated | 0.26 [0.22, 0.30] | 0.15 [0.13, 0.17] | 0.05 [0.02, 0.09] | 0.05 [0.02, 0.08] | 0.22 [0.19, 0.25] | 0.05 [0.04, 0.06] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.01] |
| (g) dominated mass / statement size | 0.72 [0.68, 0.75] | 0.46 [0.39, 0.52] | 0.43 [0.37, 0.50] | 0.42 [0.37, 0.47] | 0.72 [0.68, 0.76] | 0.23 [0.19, 0.28] | 0.31 [0.24, 0.39] | 0.24 [0.20, 0.30] |
| (g') dominated mass / statement DAG size | 0.75 [0.71, 0.78] | 0.51 [0.44, 0.57] | 0.49 [0.42, 0.55] | 0.48 [0.42, 0.53] | 0.79 [0.76, 0.82] | 0.30 [0.26, 0.36] | 0.41 [0.33, 0.47] | 0.32 [0.27, 0.37] |
| (h) has docstring | 0.78 [0.76, 0.81] | 0.43 [0.38, 0.47] | 0.43 [0.37, 0.50] | 0.42 [0.36, 0.49] | 0.85 [0.82, 0.87] | 0.37 [0.32, 0.43] | 0.46 [0.39, 0.54] | 0.36 [0.31, 0.42] |
| (h) non-private | 0.51 [0.51, 0.52] | 0.23 [0.21, 0.26] | 0.18 [0.14, 0.25] | 0.18 [0.13, 0.23] | 0.54 [0.53, 0.55] | 0.09 [0.08, 0.10] | 0.13 [0.08, 0.18] | 0.10 [0.07, 0.14] |
| (h) short name | 0.77 [0.74, 0.81] | 0.44 [0.39, 0.50] | 0.51 [0.44, 0.57] | 0.49 [0.44, 0.55] | 0.60 [0.56, 0.63] | 0.11 [0.09, 0.13] | 0.07 [0.04, 0.12] | 0.06 [0.03, 0.09] |
| (x) reachable from the headline theorems | 0.61 [0.58, 0.63] | 0.28 [0.25, 0.31] | 0.24 [0.19, 0.30] | 0.24 [0.19, 0.29] | 0.62 [0.60, 0.64] | 0.11 [0.10, 0.13] | 0.14 [0.09, 0.20] | 0.11 [0.08, 0.15] |
| (x) out-degree | 0.80 [0.77, 0.83] | 0.55 [0.48, 0.62] | 0.53 [0.46, 0.60] | 0.52 [0.47, 0.57] | 0.84 [0.81, 0.86] | 0.34 [0.28, 0.41] | 0.38 [0.31, 0.46] | 0.30 [0.25, 0.35] |
| (i) random | 0.51 [0.46, 0.55] | 0.24 [0.21, 0.28] | 0.24 [0.19, 0.31] | 0.24 [0.19, 0.29] | 0.47 [0.44, 0.51] | 0.08 [0.07, 0.09] | 0.08 [0.04, 0.12] | 0.06 [0.03, 0.09] |

Rows (x) are two extra baselines I added. Reverse-direction rows (deeper depth, larger statement, longer name) are in `tables.md`.

**Dominated mass (a) against the baselines, paired, `T-all`:**

| (a) minus | PFR dAUC | Carleson dAUC |
|---|---|---|
| (c) transitive mass | −0.055 [−0.088, −0.025] | −0.022 [−0.053, +0.006] |
| (d) own proof size | +0.010 [−0.022, +0.037] | +0.023 [−0.004, +0.050] |
| out-degree | −0.024 [−0.061, +0.012] | +0.002 [−0.031, +0.033] |
| PageRank to users | −0.014 [−0.048, +0.017] | +0.026 [−0.007, +0.055] |
| has docstring | −0.008 [−0.056, +0.036] | −0.008 [−0.047, +0.027] |
| random | +0.268 [+0.211, +0.325] | +0.366 [+0.318, +0.409] |

- **Dominated mass is well above random** but never clearly above the naive baselines; in PFR it is significantly *below* plain transitive mass.
- **Most of its signal is the declaration's own proof.** Excluding the node's own proof (a') drops AUC from 0.78 to 0.65 (PFR) and 0.84 to 0.73 (Carleson).
- **Carleson, average precision:** (a) does beat transitive mass (dAP +0.061 [+0.015, +0.103]). This is the only place a dominator score clearly beats the naive version, and it does not survive into the fitted models.
- **Library-style centrality is useless here.** In-degree and PageRank-to-used are at or below chance: blueprints list the spine of the argument, not the shared layer.

## Single scores, mainline theorems only (`T-main`)

This removes the easiest part of the task (telling the argument from the staging library). PFR: n = 310, 145 positives. Carleson: n = 1,486, 224 positives.

| score | PFR AUC | PFR AP | Carleson AUC | Carleson AP | Carleson P@k |
|---|---|---|---|---|---|
| (a) dominated proof mass | 0.73 [0.67, 0.79] | 0.72 [0.64, 0.79] | 0.78 [0.74, 0.81] | 0.38 [0.33, 0.45] | 0.47 [0.39, 0.54] |
| (b) is nontrivial dominator | 0.61 [0.56, 0.66] | 0.54 [0.47, 0.60] | 0.68 [0.65, 0.72] | 0.25 [0.21, 0.28] | 0.35 [0.28, 0.42] |
| (c) transitive proof mass | 0.76 [0.70, 0.81] | 0.67 [0.59, 0.77] | 0.77 [0.74, 0.80] | 0.30 [0.26, 0.36] | 0.35 [0.28, 0.42] |
| (d) own proof size | 0.77 [0.71, 0.81] | 0.73 [0.65, 0.81] | 0.75 [0.71, 0.78] | 0.35 [0.29, 0.41] | 0.38 [0.31, 0.46] |
| (e) in-degree | 0.49 [0.43, 0.54] | 0.46 [0.40, 0.53] | 0.48 [0.45, 0.52] | 0.15 [0.13, 0.17] | 0.13 [0.08, 0.18] |
| (e) PageRank to users | 0.74 [0.67, 0.80] | 0.68 [0.60, 0.77] | 0.77 [0.74, 0.81] | 0.36 [0.31, 0.42] | 0.39 [0.33, 0.48] |
| (f) statement size, negated | 0.31 [0.26, 0.37] | 0.36 [0.31, 0.42] | 0.34 [0.30, 0.37] | 0.11 [0.09, 0.12] | 0.03 [0.01, 0.06] |
| (g) dominated mass / statement size | 0.64 [0.58, 0.70] | 0.64 [0.56, 0.72] | 0.66 [0.62, 0.70] | 0.29 [0.24, 0.34] | 0.34 [0.28, 0.42] |
| (h) has docstring | 0.81 [0.77, 0.85] | 0.71 [0.65, 0.77] | 0.84 [0.81, 0.87] | 0.50 [0.44, 0.55] | 0.57 [0.50, 0.64] |
| (h) short name | 0.60 [0.54, 0.66] | 0.51 [0.44, 0.59] | 0.47 [0.43, 0.51] | 0.14 [0.12, 0.16] | 0.08 [0.04, 0.13] |
| (i) random | 0.47 [0.41, 0.53] | 0.48 [0.40, 0.56] | 0.48 [0.44, 0.52] | 0.14 [0.12, 0.17] | 0.13 [0.08, 0.18] |

- **Every graph score drops** by 0.03–0.08 AUC once the staging folders are gone; the docstring cue does not.
- **"Short name" was a folder detector.** Its PFR AUC falls from 0.77 to 0.60: staging-library lemmas have long namespaced names.

## Fitted models (regularised logistic regression, graph features log-scaled)

Out-of-fold scores, 5 folds grouped by module so a file never straddles train and test, averaged over 3 fold seeds; L2 strength chosen by inner cross-validation. A shallow gradient-boosted model is included to check that the null is not an artefact of linearity.

| model | PFR `T-all` AUC | PFR AP | PFR P@k | Carleson `T-all` AUC | Carleson AP | Carleson P@k |
|---|---|---|---|---|---|---|
| LR: graph baselines (c, d, e, f, out-degree, reachable) | 0.85 [0.82, 0.87] | 0.65 [0.59, 0.72] | 0.62 [0.55, 0.69] | 0.87 [0.85, 0.89] | 0.37 [0.31, 0.43] | 0.46 [0.38, 0.52] |
| LR: dominator features only (a, b, g) | 0.73 [0.69, 0.77] | 0.50 [0.43, 0.56] | 0.47 [0.40, 0.53] | 0.81 [0.78, 0.84] | 0.31 [0.25, 0.37] | 0.40 [0.33, 0.47] |
| LR: graph baselines + dominator | 0.85 [0.82, 0.88] | 0.66 [0.59, 0.72] | 0.62 [0.55, 0.69] | 0.87 [0.85, 0.89] | 0.35 [0.30, 0.42] | 0.46 [0.38, 0.53] |
| LR: surface cues only (docstring, private, name length, name parts) | 0.90 [0.87, 0.92] | 0.74 [0.68, 0.79] | 0.68 [0.58, 0.76] | 0.90 [0.87, 0.92] | 0.50 [0.44, 0.57] | 0.53 [0.45, 0.61] |
| LR: surface + graph baselines | 0.93 [0.91, 0.95] | 0.79 [0.73, 0.84] | 0.75 [0.68, 0.80] | 0.94 [0.93, 0.95] | 0.58 [0.51, 0.65] | 0.63 [0.55, 0.69] |
| LR: surface + graph baselines + dominator | 0.93 [0.91, 0.95] | 0.79 [0.74, 0.84] | 0.73 [0.68, 0.80] | 0.94 [0.93, 0.95] | 0.58 [0.51, 0.65] | 0.61 [0.53, 0.68] |
| GBT: graph baselines | 0.82 [0.79, 0.85] | 0.58 [0.51, 0.64] | 0.59 [0.52, 0.65] | 0.87 [0.85, 0.89] | 0.38 [0.33, 0.45] | 0.46 [0.38, 0.52] |
| GBT: graph baselines + dominator | 0.82 [0.79, 0.85] | 0.56 [0.50, 0.63] | 0.58 [0.51, 0.65] | 0.87 [0.85, 0.89] | 0.41 [0.35, 0.48] | 0.47 [0.40, 0.55] |

**Ablation: what the dominator features add (paired bootstrap).**

| comparison | set | PFR dAUC | PFR dAP | Carleson dAUC | Carleson dAP |
|---|---|---|---|---|---|
| graph + dominator minus graph | `T-all` | +0.001 [−0.003, +0.005] | +0.007 [−0.003, +0.016] | +0.001 [−0.005, +0.006] | −0.012 [−0.038, +0.014] |
| graph + dominator minus graph | `T-main` | +0.001 [−0.016, +0.019] | +0.007 [−0.026, +0.042] | −0.004 [−0.013, +0.006] | +0.001 [−0.029, +0.029] |
| surface + graph + dominator minus surface + graph | `T-all` | +0.001 [−0.001, +0.003] | +0.003 [−0.005, +0.013] | +0.002 [−0.001, +0.004] | +0.001 [−0.017, +0.021] |
| surface + graph + dominator minus surface + graph | `T-main` | +0.001 [−0.004, +0.005] | +0.007 [−0.003, +0.017] | +0.004 [−0.001, +0.010] | −0.010 [−0.033, +0.014] |
| GBT graph + dominator minus GBT graph | `T-all` | +0.004 [−0.004, +0.012] | −0.015 [−0.045, +0.015] | +0.005 [−0.003, +0.012] | +0.023 [−0.010, +0.061] |
| surface + graph minus surface | `T-all` | +0.034 [+0.017, +0.051] | +0.052 [−0.000, +0.104] | +0.045 [+0.031, +0.060] | +0.077 [+0.023, +0.130] |
| surface + graph minus surface | `T-main` | +0.022 [−0.013, +0.057] | −0.010 [−0.060, +0.047] | +0.075 [+0.051, +0.102] | +0.115 [+0.062, +0.166] |

- **Dominator features add nothing**, with or without surface cues, in either project, linear or boosted. Every interval contains zero and every point estimate is within ±0.005 AUC.
- **Graph features do add to surface cues**: +0.03 to +0.08 AUC, significant everywhere except PFR mainline. So the graph is not redundant with docstrings; it is the dominator part that is redundant with the rest of the graph.
- **Cross-project transfer holds up**, so the models are not memorising one project. Graph baselines fitted on PFR score 0.86 AUC on Carleson (0.83 the other way); adding dominator features lowers both slightly (0.85 and 0.82). See `tables.md`.

## Leakage: which features could be contaminated

- **Blueprint tooling leaves no mark in Lean.** Both projects use the classic `leanblueprint` + `checkdecls` setup, where `\lean{...}` lives in the LaTeX. No Lean file contains a `@[blueprint]` attribute, so no attribute or generated docstring is added to tagged declarations.
- **Docstrings are contaminated by convention, not tooling.** In PFR 95 of 204 tagged-theorem docstrings contain LaTeX `$…$` (the blueprint statement pasted in) against 28 of 254 untagged ones. In Carleson 40 of 178 tagged docstrings cite blueprint numbering ("Lemma 7.2.3", "in the blueprint") against 28 of 213 untagged. The docstring baseline is therefore partly the label itself; treat it as an upper bound on honest surface cues, not as a fair competitor.
- **Name length is a folder proxy** in PFR (see above). Not contaminated by the blueprint, but not a property of importance either.
- **Folder effect on graph features.** 36% of tagged PFR theorems sit in staging folders that the blueprint covers only selectively, and reachability alone gets AUC 0.61. `T-main` and `T-main-reach` remove this; conclusions do not change.
- **Root effect.** Dominator features are defined relative to the headline theorems, which are themselves blueprint nodes in 6 of 12 (PFR) and 3 of 4 (Carleson) cases. That is at most 6 positives and does not move any number.
- **"Top-level theorem of its file"** was a worry in the brief. No positional feature (line number, last-in-file) is used. In-degree 0 is not a giveaway: only 6% of tagged PFR theorems have no user, against 17% of untagged.
- **Size is the confound that matters.** Tagged theorems have a median proof of 2,617 subterms against 523 (PFR) and 3,410 against 545 (Carleson). Any score correlated with proof size inherits AUC ≈ 0.77–0.81 for free; dominated mass includes own proof size.

## Structure: Lean graph restricted to blueprint nodes against the blueprint `\uses` graph

Nodes are blueprint nodes with at least one exported declaration (PFR 206, Carleson 170). An ordered pair (A, B) is a human edge if A `\uses` B in the statement or proof. Chance precision is the edge density: 0.011 (PFR, 466 edges) and 0.007 (Carleson, 212 edges).

| Lean relation A → B | PFR edges | PFR precision | PFR recall | Carleson edges | Carleson precision | Carleson recall |
|---|---|---|---|---|---|---|
| direct dependency | 794 | 0.40 | 0.69 | 155 | 0.67 | 0.49 |
| reachable with no blueprint declaration in between | 1,181 | 0.34 | 0.87 | 358 | 0.56 | 0.94 |
| reachable (transitive) | 4,963 | 0.09 | 0.91 | 2,509 | 0.08 | 0.94 |
| dominator tree: A is B's nearest blueprint ancestor | 121 | 0.71 | 0.19 | 172 | 0.72 | 0.58 |
| dominator tree: A is any blueprint ancestor of B | 432 | 0.20 | 0.19 | 904 | 0.14 | 0.58 |

Against the transitive closure of `\uses` (4,460 pairs in PFR, 2,474 in Carleson): Lean reachability has precision 0.84 / recall 0.93 (PFR) and 0.95 / 0.96 (Carleson); dominator ancestry has precision 0.97 / 1.00 but recall 0.09 / 0.36.

- **The two graphs agree on order.** No human edge runs the opposite way in Lean. 42 of 466 (PFR) and 12 of 212 (Carleson) human edges join declarations with no Lean dependency in either direction; these are `\uses` that the formal proof does not need.
- **Reachability reproduces the human graph's shape.** Contracted reachability recovers 87% and 94% of human edges. Of its extra edges, 71% (PFR) and 64% (Carleson) are in the `\uses` closure, i.e. indirect human dependencies that Lean uses directly; the rest are Lean dependencies the blueprint does not record at all.
- **The dominator tree is a precise but thin skeleton.** When it says "B sits under A", the human graph agrees 71% of the time directly and 97–99% transitively. But a tree has at most one parent per node, and blueprint nodes have 2.3 (PFR) and 1.2 (Carleson) uses each on average.
- **PFR is the hard case for dominators.** Only 119 of 197 reachable blueprint nodes have any blueprint dominator ancestor: the entropy toolkit is shared by many chapters, so its lemmas are dominated only by the root. Carleson is more tree-like (159 of 164), which is why recall is 0.58 there.
- **This comparison is partly circular.** Blueprint `\uses` is meant to mirror the Lean dependencies, and the dependency-graph tool is used to keep them in step, so high reachability agreement is expected rather than a discovery.

## Ten high-scoring declarations that are not in the blueprint

Ranked by dominated proof mass and by the out-of-fold graph-only model; both lists overlap heavily (`examples_pfr.json`, `examples_carleson.json`). "Dominates n" counts declarations used only through it.

| declaration | where | dominates | what it is | verdict |
|---|---|---|---|---|
| `phiMinimizer_exists_rdist_eq_zero` | PFR.RhoFunctional:1852 | 57, mass 201,306 | Short statement (335 nodes): a φ-minimiser with distance zero exists. Sole user is blueprint `pfr-rho`; it packages blueprint nodes `phi_min_exists` and `dist_of_min_eq_zero`. | Plausible omission: a real chapter boundary the blueprint leaves implicit. |
| `weak_PFR_asymm_prelim` | PFR.WeakPFR:625 | 61, mass 152,815 | Preliminary form of blueprint theorem `weak_PFR_asymm`, its only user. | Variant of a blueprint node, not noise. |
| `dist_of_min_eq_zero'` | PFR.RhoFunctional:1773 | 35, mass 152,046 | Primed version carrying the actual proof; blueprint tags the unprimed wrapper. | Variant. |
| `tau_strictly_decreases_aux'` | PFR.ImprovedPFR:677 | 27, mass 146,650 | Body of blueprint theorem `tau_strictly_decreases'` (`de-prop-improv`). | Variant. |
| `averaged_final` | PFR.ImprovedPFR:667 | 26, mass 139,482 | Undocumented intermediate step collecting four blueprint lemmas (`averaged_construct_good`, `dist_diff_bound_1/2`, `gen_ineq_01`). | Plausible omission, but its statement is long (1,635 nodes). |
| `condRuzsaDist_nonneg` | PFR.ForMathlib.Entropy.RuzsaDist:573 | 37, mass 35,593 | Used once, by blueprint `fibring-ineq`; pulls in the whole kernel Ruzsa-distance development. | Noise for an outline: a trivial fact that happens to be the only door into a library. |
| `R_truncation'` | Carleson.MetricCarleson.Truncation:603 | 1,385, mass 2,990,480 | Primed version of blueprint lemma `R-truncation`; nearly the whole metric-space proof sits under it. | Variant. |
| `finitary_carleson_step` | Carleson.MetricCarleson.Truncation:81 | 1,288, mass 2,865,204 | Induction step wrapped around blueprint node `finitary_carleson`. | Plausible omission (formalisation-specific step). |
| `forest_union_optimized` / `forest_union_aux` | Carleson.Discrete.ForestUnion:970, 833 | 553 / 550 | Sharper-constant and auxiliary versions of blueprint lemma `forest-union`. | Variant. |
| `control_approximation_effect'` | Carleson.Classical.ControlApproximationEffectContinuous:177 | 413, mass 687,047 | Primed version; dominates four blueprint lemmas on Dirichlet kernels. | Variant. |

- **Mostly variants, little noise.** Among the top 25 untagged theorems by dominated mass, 20 (PFR) and 17 (Carleson) are a dominator-tree parent or child of a blueprint declaration or share its name stem; among the top 100, 57 and 65. The base rate for being a dominator-tree neighbour of a blueprint declaration is 36% (PFR) and 37% (Carleson) of untagged reachable theorems.
- **Why they count as errors.** Dominator chains (`foo` → `foo'` → `foo_aux`) carry almost the same mass at every link; the blueprint names one link, the score rewards all of them. Membership metrics punish this; a reader would not.
- **Also in the PFR top list:** the six `Marton.*` restatements in `PFRPalomar.Solution`, which are our roots. They are wrappers, i.e. noise caused by the root choice.

## Ten blueprint declarations the graph scores badly

Rank is by the graph-only model among all theorems (978 in PFR, 2,675 in Carleson).

| declaration | blueprint node | rank | why the graph misses it |
|---|---|---|---|
| `hahn_banach` (PFR.HomPFR:31) | `hb-thm` | 881 | Not used by any project declaration (in-degree 0, out-degree 0): the final proof goes another way. Unreachable, so every dominator score is 0. |
| `ProbabilityTheory.entropy_le_log_card` (PFR.ForMathlib.Entropy.Basic:81) | `jensen-bound` | 884 | Proof of 44 subterms, one user, not on any path from the headline theorems. A textbook fact the blueprint states for the reader. |
| `sum_uvw_eq_zero` (PFR.Endgame:311) | `key-ident` | 817 | The "key identity" U + V + W = 0: a one-line algebraic fact with no project dependencies. Mathematically central, structurally a leaf. |
| `condKLDiv_nonneg`, `KLDiv_eq_zero_iff_identDistrib` (PFR.Kullback) | `Conditional-Gibbs`, Gibbs | 775, 751 | Side results of the Kullback–Leibler chapter that the headline theorems do not use. |
| `card_of_dual` (PFR.ApproxHomPFR:194) | `gdual` | 720 | Small counting lemma (164 subterms), two users, dominates nothing. |
| `ProbabilityTheory.IdentDistrib.entropy_congr` (PFR.ForMathlib.Entropy.Basic:76) | `copy-ent` | 656 | Tiny proof, 40 users. A shared-library fact; dominated only by the root. This is exactly the layer dominators cannot see. |
| `support_holderApprox_subset` (Carleson.HolderVanDerCorput:165) | `Lipschitz-Holder-approximation` | 2,315 | One of several declarations a single blueprint lemma is split into; each piece is small. |
| `laverage_le_globalMaximalFunction` (Carleson.ToMathlib.HardyLittlewood:34) | `Hardy-Littlewood` | 2,085 | A blueprint *proposition* whose Lean counterpart is spread over a staging file; the tagged piece has a 466-subterm proof and 7 users. |
| `periodic_dirichletApprox` (Carleson.Classical.HilbertStrongType:419) | `Dirichlet-approximation` | 1,862 | Unused part of a multi-part blueprint lemma (in-degree 0, unreachable). |
| `tsum_eLpNorm_czRemainder_le`, `eLpNorm_czRemainder_le`, `integral_czRemainder` (Carleson.TwoSidedCarleson.WeakCalderonZygmund) | `Calderon-Zygmund-decomposition` | 1,433, 1,421, 1,400 | Clauses of one blueprint lemma proved as separate theorems; these clauses are not needed by the headline theorems. |

The misses fall into four kinds:
- **Not on the main line.** 7% of tagged theorems in each project are unreachable from the headline theorems (15 of 225 in PFR, 15 of 229 in Carleson). No root-relative score can find them.
- **Small but conceptually central facts** (`key-ident`). Importance to a reader is not proof mass.
- **Shared toolkit lemmas** with many users. Dominators miss them by construction, and in-degree does not rescue them (AUC 0.55 and 0.53) because most heavily used declarations are not blueprint material.
- **One blueprint node, several Lean declarations.** The unit of the blueprint is coarser than the Lean declaration; each fragment looks unimportant.

## Plain verdict on H3

- **As stated, H3 is weakly supported and not in the form we wanted.** The dependency graph alone ranks blueprint theorems clearly above chance (AUC 0.85–0.87, average precision 0.65 in PFR and 0.37 in Carleson against base rates 0.23 and 0.09). But at k it recovers about 60% of the PFR blueprint and 36% of Carleson's, which is not a usable reconstruction of the human interface.
- **The dominator-tree claim is negative.** Dominator features add nothing measurable to transitive mass, own proof size and out-degree, under four evaluation sets, two model families and cross-project transfer. A dominator-only model is worse than the naive baselines (AUC 0.73 vs 0.85 in PFR, 0.81 vs 0.87 in Carleson).
- **The "short statement hiding a large subtree" criterion is contradicted.** Human blueprint statements are longer than average, and dividing by statement size lowers every metric.
- **Cheap surface cues do better than any graph score**, although the docstring cue is partly contaminated by the blueprint itself.
- **Structure is the better news.** Reachability restricted to blueprint nodes reproduces the human `\uses` graph (recall 0.87–0.94 direct, precision 0.84–0.95 against its closure). Dominator-tree parents are 71% precise but cover a minority of human edges in PFR.
- **What this does and does not say about the machine corpus.** These two projects were factored by people who also wrote the blueprint, and in both the dominator tree's large-mass nodes are mostly variants of blueprint nodes rather than junk. That is consistent with "the dominator tree gives a navigable skeleton" but it is not evidence that it *selects* what a human would select; on that question the result is negative. Two projects are a small sample, and both come from the same community and tooling.

## Files

- `bench/validate_outline.py`: features, metrics, bootstrap, models, structure comparison. About 3.5 minutes with `--boot 1000`.
- `bench/validate_outline_extra.py`: chain/variant analysis, tagged-vs-untagged shares, docstring LaTeX count.
- `out/corpus/validation/tables.md`: every table for every evaluation set (generated).
- `out/corpus/validation/results.json`, `extra.json`: all numbers.
- `out/corpus/validation/scores_pfr.csv`, `scores_carleson.csv`: per-declaration features and out-of-fold model scores.
- `out/corpus/validation/examples_pfr.json`, `examples_carleson.json`: top untagged and bottom tagged declarations with statements.
