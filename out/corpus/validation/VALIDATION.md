# H3 validation: does graph structure predict what humans put in the blueprint? (2026-11-10, revised after review)

**H3:** "declarations that humans put in the blueprint can be predicted from the dependency graph alone."

**Verdict: negative for the dominator idea. The graph as a whole ranks blueprint theorems well above chance, but most of that is proof length and telling the main argument from the staging folders, not graph structure.**

- **Graph features carry a real but modest signal.** A graph-only model reaches ROC-AUC 0.85 (PFR) and 0.87 (Carleson), but at k = number of blueprint nodes only 62% and 43% of its picks are blueprint theorems.
- **The dominator tree adds nothing.** Adding every dominator feature to the naive graph baselines changes AUC by +0.001 (PFR) and +0.003 (Carleson); the interval contains zero in 12 of 12 ablations and no point estimate exceeds ±0.004 AUC.
- **The signal is mostly size.** In AUC, dominated proof mass is statistically indistinguishable from the declaration's own proof size, its out-degree and its length in source lines. On mainline theorems the whole graph model is not distinguishable from a three-feature size model (PFR +0.001 [−0.072, +0.047], Carleson +0.024 [−0.001, +0.049] AUC).
- **Normalising by statement size hurts.** Blueprint theorems have *larger* statements than the rest (median 383 vs 191 nodes in PFR, 1,477 vs 239 in Carleson), so "short statement, large hidden mass" points the wrong way.
- **The docstring flag alone matches the graph; the other surface cues do not.** "Has a docstring" scores AUC 0.78 / 0.85, but it is contaminated by the blueprint (see Leakage). Without it the surface model falls to 0.80 / 0.63, below the graph model (0.85 / 0.87).
- **Structure agrees better than membership.** Lean reachability between blueprint nodes recovers 87–94% of the human `\uses` edges. The dominator tree's parent relation is precise (0.71 / 0.73) but recalls only 18% (PFR) and 58% (Carleson) of them.
- **One positive observation for the outline use-case.** The top "false positives" are mostly not noise: 20 of the top 25 in PFR and 17 of 25 in Carleson are a dominator-tree neighbour or a primed/`_aux` variant of a blueprint declaration.

Everything below is produced by `bench/validate_outline.py`, `bench/validate_outline_extra.py` and `bench/validate_outline_report.py` from the exported Lean data. The full tables for every evaluation set are in `tables.md`; numbers are in `results.json`.

## What changed after the review

- **Exporter bug fixed and both corpora re-exported.** `corpora/tools/ExportDecls.lean` attributed a use of another declaration's cached auxiliary (`_proof_N`, `_simp_N`, `irreducible_def` wrappers) to that declaration. It now inlines the auxiliary's own dependencies, as the Navier-Stokes exporter does. Carleson lost 294 false edges and gained 112 true ones (25,554 → 25,372 edges; reachable 2,349 → 2,344); PFR lost 6 and gained 1 (4,877 → 4,872). No conclusion changed; Carleson figures moved by at most about 0.01 AUC and the example tables were redone.
- **Intervals are now a module-cluster bootstrap** (whole files resampled), because blueprint theorems cluster by file. They are about two to three times wider than the per-declaration intervals reported before, and they still cover test-set sampling only (fitted models are held fixed).
- **Three models were added:** surface cues without the docstring flag, a size-only model (source lines, own proof size, statement size), and surface cues plus length (source lines, statement characters). Source line count is also a single score.
- **Root sensitivity** is now reported (it was listed as unchecked).
- **Two claims were withdrawn:** "surface cues beat the graph" (true only of the contaminated docstring flag) and "the graph adds +0.03 to +0.08 AUC to surface cues" (it shrinks to +0.01 to +0.02 once length is among the surface cues).

## Setup

| | PFR | Carleson |
|---|---|---|
| declarations / edges (type ∪ value, deduplicated) | 1,118 / 4,872 | 3,199 / 25,372 |
| headline roots (from `axioms.json`) | 12 | 4 |
| reachable from the roots | 830 | 2,344 |
| nontrivial dominators | 242 | 628 |
| blueprint nodes (= k) | 219 | 180 |
| blueprint-tagged project declarations | 247 | 236 |
| theorems, tagged / all | 225 / 978 (23.0%) | 229 / 2,675 (8.6%) |
| mainline theorems, tagged / all | 145 / 310 (46.8%) | 224 / 1,486 (15.1%) |

- **Dominator tree:** computed from a virtual root that uses every headline theorem. Dominated mass and transitive mass were checked against brute force (delete the node, recount) on 150 random declarations per project with no mismatch, before and again after the edge fix.
- **Proof mass:** `proofSize + auxProofSize` (distinct subterms), summed over the relevant set, including the declaration itself unless marked "excl. own".
- **Unreachable declarations:** dominator scores are 0 and depth is set to worst.
- **Evaluation sets:** `T-all` is all theorems (primary). `T-main` drops the staging folders (`PFR/Mathlib`, `PFR/ForMathlib`, `Carleson/ToMathlib`, …) that the blueprints do not try to cover. `T-main-reach` and `SPEC` (tagged declarations of any kind plus untagged theorems, the task's literal wording) are in `tables.md` and tell the same story.
- **Intervals:** 95% percentile bootstrap, 1,000 resamples of whole modules, the same resamples for every score so differences are paired. Training variance of the fitted models is not included.
- **k:** the number of blueprint nodes. In PFR `T-main` k = 219 exceeds the 145 positives, so precision@k cannot exceed 0.66 there.
- **Carleson has two genuine 2-cycles** (`mutual` theorems `I1_prop_1`/`I3_prop_1` and `I2_prop_2`/`I3_prop_2`); the script handles cycles.

## Single scores, all theorems (`T-all`)

PFR: n = 978, 225 positives, k = 219. Carleson: n = 2,675, 229 positives, k = 180.

| score | PFR AUC | PFR AP | PFR P@k | PFR R@k | Carleson AUC | Carleson AP | Carleson P@k | Carleson R@k |
|---|---|---|---|---|---|---|---|---|
| (a) dominated proof mass (incl. own) | 0.78 [0.72, 0.84] | 0.56 [0.45, 0.67] | 0.54 [0.37, 0.68] | 0.53 [0.39, 0.74] | 0.83 [0.78, 0.88] | 0.35 [0.29, 0.42] | 0.44 [0.35, 0.51] | 0.35 [0.25, 0.50] |
| (a') dominated proof mass (excl. own) | 0.65 [0.61, 0.71] | 0.43 [0.32, 0.52] | 0.45 [0.27, 0.59] | 0.44 [0.34, 0.56] | 0.73 [0.69, 0.77] | 0.29 [0.24, 0.35] | 0.45 [0.34, 0.51] | 0.35 [0.24, 0.47] |
| (b) is nontrivial dominator | 0.64 [0.60, 0.69] | 0.32 [0.23, 0.40] | 0.43 [0.27, 0.53] | 0.42 [0.30, 0.55] | 0.70 [0.67, 0.74] | 0.17 [0.12, 0.21] | 0.24 [0.18, 0.32] | 0.19 [0.14, 0.28] |
| (b) dominator depth (shallower = higher) | 0.63 [0.56, 0.69] | 0.29 [0.20, 0.38] | 0.31 [0.16, 0.42] | 0.30 [0.20, 0.43] | 0.56 [0.50, 0.62] | 0.09 [0.06, 0.13] | 0.06 [0.02, 0.11] | 0.04 [0.01, 0.10] |
| (c) transitive proof mass beneath | 0.83 [0.78, 0.88] | 0.59 [0.45, 0.74] | 0.63 [0.40, 0.74] | 0.61 [0.43, 0.77] | 0.87 [0.83, 0.90] | 0.30 [0.24, 0.36] | 0.37 [0.28, 0.43] | 0.29 [0.21, 0.41] |
| (d) own proof size | 0.77 [0.69, 0.85] | 0.56 [0.44, 0.68] | 0.52 [0.35, 0.68] | 0.51 [0.37, 0.71] | 0.81 [0.76, 0.87] | 0.31 [0.24, 0.37] | 0.36 [0.27, 0.42] | 0.28 [0.20, 0.39] |
| (s) source lines of the declaration | 0.75 [0.69, 0.83] | 0.52 [0.40, 0.65] | 0.51 [0.35, 0.64] | 0.49 [0.35, 0.71] | 0.80 [0.75, 0.84] | 0.25 [0.19, 0.32] | 0.31 [0.22, 0.39] | 0.24 [0.18, 0.34] |
| (e) in-degree (users) | 0.55 [0.48, 0.60] | 0.27 [0.17, 0.37] | 0.24 [0.12, 0.37] | 0.23 [0.15, 0.35] | 0.52 [0.47, 0.59] | 0.09 [0.06, 0.12] | 0.09 [0.04, 0.14] | 0.07 [0.04, 0.11] |
| (e) PageRank, rank flows to used declarations | 0.50 [0.43, 0.57] | 0.23 [0.14, 0.32] | 0.19 [0.09, 0.30] | 0.19 [0.11, 0.29] | 0.38 [0.34, 0.43] | 0.06 [0.04, 0.09] | 0.01 [0.00, 0.04] | 0.01 [0.00, 0.03] |
| (e) PageRank, rank flows to users | 0.79 [0.74, 0.85] | 0.54 [0.41, 0.67] | 0.56 [0.38, 0.69] | 0.55 [0.40, 0.74] | 0.81 [0.77, 0.84] | 0.30 [0.24, 0.35] | 0.36 [0.28, 0.43] | 0.28 [0.20, 0.41] |
| (f) statement size, negated | 0.26 [0.16, 0.34] | 0.15 [0.09, 0.21] | 0.05 [0.01, 0.12] | 0.05 [0.01, 0.12] | 0.22 [0.16, 0.27] | 0.05 [0.03, 0.07] | 0.01 [0.00, 0.02] | 0.00 [0.00, 0.02] |
| (g) dominated mass / statement size | 0.72 [0.67, 0.77] | 0.46 [0.35, 0.55] | 0.43 [0.29, 0.55] | 0.42 [0.32, 0.60] | 0.71 [0.66, 0.77] | 0.23 [0.18, 0.30] | 0.31 [0.22, 0.41] | 0.24 [0.18, 0.35] |
| (g') dominated mass / statement DAG size | 0.75 [0.69, 0.81] | 0.51 [0.39, 0.62] | 0.49 [0.32, 0.61] | 0.48 [0.34, 0.68] | 0.79 [0.74, 0.84] | 0.31 [0.25, 0.38] | 0.40 [0.31, 0.49] | 0.31 [0.25, 0.43] |
| (h) has docstring | 0.78 [0.72, 0.84] | 0.43 [0.32, 0.54] | 0.43 [0.31, 0.56] | 0.42 [0.25, 0.71] | 0.85 [0.77, 0.90] | 0.37 [0.25, 0.47] | 0.46 [0.32, 0.57] | 0.36 [0.28, 0.49] |
| (h) non-private | 0.51 [0.50, 0.53] | 0.23 [0.16, 0.31] | 0.18 [0.12, 0.26] | 0.18 [0.12, 0.28] | 0.54 [0.52, 0.56] | 0.09 [0.06, 0.13] | 0.13 [0.07, 0.19] | 0.10 [0.07, 0.14] |
| (h) short name | 0.77 [0.69, 0.86] | 0.44 [0.36, 0.54] | 0.51 [0.37, 0.58] | 0.49 [0.33, 0.74] | 0.60 [0.51, 0.68] | 0.11 [0.07, 0.15] | 0.07 [0.03, 0.14] | 0.06 [0.02, 0.12] |
| (x) reachable from the headline theorems | 0.61 [0.56, 0.66] | 0.28 [0.20, 0.35] | 0.24 [0.16, 0.32] | 0.24 [0.16, 0.37] | 0.62 [0.58, 0.67] | 0.11 [0.08, 0.14] | 0.14 [0.08, 0.20] | 0.11 [0.07, 0.16] |
| (x) out-degree | 0.80 [0.74, 0.85] | 0.55 [0.43, 0.66] | 0.53 [0.37, 0.66] | 0.52 [0.39, 0.73] | 0.84 [0.79, 0.88] | 0.34 [0.27, 0.43] | 0.38 [0.31, 0.47] | 0.30 [0.21, 0.45] |
| (i) random | 0.51 [0.48, 0.54] | 0.24 [0.16, 0.32] | 0.24 [0.16, 0.34] | 0.24 [0.18, 0.36] | 0.47 [0.44, 0.51] | 0.08 [0.05, 0.11] | 0.08 [0.03, 0.13] | 0.06 [0.02, 0.10] |

Rows (x) and (s) are baselines added to the brief's list. Reverse-direction rows (deeper depth, larger statement, longer name) are in `tables.md`.

**Dominated mass (a) against the baselines, paired, `T-all`:**

| (a) minus | PFR dAUC | PFR dAP | Carleson dAUC | Carleson dAP |
|---|---|---|---|---|
| (c) transitive mass | −0.055 [−0.095, −0.003] | −0.028 [−0.139, +0.086] | −0.036 [−0.081, +0.006] | +0.053 [+0.003, +0.115] |
| (d) own proof size | +0.010 [−0.032, +0.055] | −0.000 [−0.061, +0.058] | +0.016 [−0.009, +0.040] | +0.048 [−0.006, +0.110] |
| (s) source lines | +0.025 [−0.015, +0.065] | +0.037 [−0.032, +0.107] | +0.035 [−0.002, +0.072] | +0.105 [+0.048, +0.165] |
| out-degree | −0.024 [−0.073, +0.042] | +0.010 [−0.075, +0.103] | −0.007 [−0.052, +0.037] | +0.010 [−0.066, +0.100] |
| PageRank to users | −0.014 [−0.054, +0.039] | +0.017 [−0.053, +0.100] | +0.019 [−0.026, +0.064] | +0.058 [+0.015, +0.111] |
| has docstring | −0.008 [−0.070, +0.067] | +0.134 [+0.035, +0.253] | −0.015 [−0.082, +0.073] | −0.019 [−0.107, +0.105] |
| random | +0.268 [+0.197, +0.353] | +0.320 [+0.222, +0.420] | +0.359 [+0.298, +0.422] | +0.277 [+0.224, +0.342] |

- **Dominated mass is well above random** but never clearly above the naive baselines in AUC; in PFR it is significantly *below* plain transitive mass (−0.055 [−0.095, −0.003]).
- **Most of its signal is the declaration's own proof.** Excluding the node's own proof (a') drops AUC from 0.78 to 0.65 (PFR) and 0.83 to 0.73 (Carleson).
- **Carleson, average precision:** (a) does beat transitive mass (dAP +0.053 [+0.003, +0.115]) and source line count (dAP +0.105 [+0.048, +0.165]). This is the only place a dominator score clearly beats a naive one, and it does not survive into the fitted models.
- **Library-style centrality is useless here.** In-degree and PageRank-to-used are at or below chance: blueprints list the spine of the argument, not the shared layer.

## Single scores, mainline theorems only (`T-main`)

This removes the easiest part of the task (telling the argument from the staging library). PFR: n = 310, 145 positives. Carleson: n = 1,486, 224 positives.

| score | PFR AUC | PFR AP | Carleson AUC | Carleson AP | Carleson P@k |
|---|---|---|---|---|---|
| (a) dominated proof mass | 0.73 [0.67, 0.80] | 0.72 [0.63, 0.82] | 0.77 [0.72, 0.82] | 0.39 [0.34, 0.46] | 0.47 [0.40, 0.54] |
| (b) is nontrivial dominator | 0.61 [0.55, 0.66] | 0.54 [0.46, 0.64] | 0.68 [0.65, 0.71] | 0.25 [0.20, 0.29] | 0.33 [0.25, 0.40] |
| (c) transitive proof mass | 0.76 [0.61, 0.84] | 0.67 [0.49, 0.85] | 0.78 [0.74, 0.83] | 0.32 [0.27, 0.38] | 0.37 [0.31, 0.44] |
| (d) own proof size | 0.77 [0.71, 0.84] | 0.73 [0.64, 0.85] | 0.75 [0.69, 0.80] | 0.35 [0.29, 0.42] | 0.38 [0.31, 0.44] |
| (s) source lines | 0.74 [0.67, 0.83] | 0.70 [0.59, 0.83] | 0.78 [0.73, 0.83] | 0.36 [0.31, 0.43] | 0.40 [0.33, 0.49] |
| (e) in-degree | 0.49 [0.40, 0.58] | 0.46 [0.40, 0.57] | 0.48 [0.42, 0.53] | 0.14 [0.11, 0.18] | 0.12 [0.07, 0.19] |
| (e) PageRank to users | 0.74 [0.62, 0.82] | 0.68 [0.52, 0.82] | 0.78 [0.74, 0.81] | 0.36 [0.32, 0.42] | 0.39 [0.34, 0.49] |
| (f) statement size, negated | 0.31 [0.25, 0.37] | 0.36 [0.32, 0.45] | 0.34 [0.28, 0.40] | 0.11 [0.08, 0.14] | 0.03 [0.00, 0.06] |
| (g) dominated mass / statement size | 0.64 [0.58, 0.74] | 0.64 [0.55, 0.75] | 0.66 [0.61, 0.71] | 0.29 [0.23, 0.37] | 0.34 [0.27, 0.43] |
| (h) has docstring | 0.81 [0.74, 0.87] | 0.71 [0.65, 0.79] | 0.84 [0.78, 0.90] | 0.50 [0.40, 0.58] | 0.64 [0.52, 0.72] |
| (h) short name | 0.60 [0.49, 0.71] | 0.51 [0.45, 0.64] | 0.47 [0.41, 0.54] | 0.14 [0.10, 0.18] | 0.08 [0.03, 0.14] |
| (i) random | 0.47 [0.42, 0.51] | 0.48 [0.41, 0.60] | 0.48 [0.45, 0.52] | 0.14 [0.11, 0.17] | 0.13 [0.08, 0.18] |

- **The graph scores drop** by 0.04–0.10 AUC (dominated mass, transitive mass, out-degree) once the staging folders are gone; own proof size and source lines barely move in PFR, and the docstring cue does not drop.
- **"Short name" was a folder detector.** Its PFR AUC falls from 0.77 to 0.60: staging-library lemmas have long namespaced names.
- **Source line count alone** scores 0.74 (PFR) and 0.78 (Carleson) here, level with dominated mass (0.73 and 0.77).

## Fitted models (regularised logistic regression, graph features log-scaled)

Out-of-fold scores, 5 folds grouped by module so a file never straddles train and test, averaged over 3 fold seeds; L2 strength chosen by inner cross-validation. A shallow gradient-boosted model is included to check that the null is not an artefact of linearity.

**`T-all`**

| model | PFR AUC | PFR AP | PFR P@k | Carleson AUC | Carleson AP | Carleson P@k |
|---|---|---|---|---|---|---|
| LR: graph baselines (c, d, e, f, out-degree, reachable) | 0.85 [0.80, 0.90] | 0.65 [0.54, 0.75] | 0.62 [0.39, 0.74] | 0.87 [0.83, 0.91] | 0.36 [0.30, 0.44] | 0.43 [0.34, 0.50] |
| LR: dominator features only (a, b, g) | 0.73 [0.68, 0.81] | 0.50 [0.38, 0.61] | 0.47 [0.33, 0.62] | 0.80 [0.75, 0.86] | 0.31 [0.26, 0.38] | 0.40 [0.33, 0.49] |
| LR: graph baselines + dominator | 0.85 [0.80, 0.90] | 0.66 [0.55, 0.76] | 0.62 [0.41, 0.76] | 0.87 [0.83, 0.91] | 0.37 [0.31, 0.44] | 0.46 [0.37, 0.53] |
| LR: size only (source lines, own proof size, statement size) | 0.76 [0.67, 0.88] | 0.55 [0.41, 0.69] | 0.54 [0.35, 0.66] | 0.83 [0.78, 0.88] | 0.29 [0.24, 0.34] | 0.29 [0.23, 0.37] |
| LR: surface cues without docstring (private, name length, name parts) | 0.80 [0.70, 0.90] | 0.48 [0.39, 0.58] | 0.54 [0.38, 0.62] | 0.63 [0.51, 0.74] | 0.12 [0.08, 0.18] | 0.09 [0.03, 0.19] |
| LR: surface cues (docstring, private, name length, name parts) | 0.90 [0.83, 0.96] | 0.74 [0.60, 0.84] | 0.68 [0.42, 0.81] | 0.90 [0.85, 0.93] | 0.50 [0.35, 0.62] | 0.53 [0.34, 0.72] |
| LR: surface + length (source lines, statement chars) | 0.91 [0.86, 0.96] | 0.75 [0.65, 0.85] | 0.68 [0.47, 0.82] | 0.92 [0.89, 0.95] | 0.50 [0.38, 0.60] | 0.52 [0.39, 0.66] |
| LR: surface + graph baselines | 0.93 [0.90, 0.96] | 0.79 [0.72, 0.86] | 0.74 [0.48, 0.83] | 0.94 [0.92, 0.96] | 0.59 [0.49, 0.68] | 0.63 [0.50, 0.74] |
| LR: surface + length + graph baselines | 0.93 [0.90, 0.96] | 0.79 [0.72, 0.86] | 0.74 [0.48, 0.83] | 0.94 [0.91, 0.96] | 0.57 [0.48, 0.67] | 0.66 [0.49, 0.74] |
| LR: surface + graph baselines + dominator | 0.93 [0.90, 0.97] | 0.79 [0.73, 0.86] | 0.74 [0.48, 0.83] | 0.94 [0.91, 0.96] | 0.59 [0.48, 0.69] | 0.62 [0.48, 0.73] |
| GBT: graph baselines | 0.82 [0.76, 0.88] | 0.58 [0.45, 0.71] | 0.58 [0.38, 0.72] | 0.88 [0.84, 0.91] | 0.40 [0.33, 0.48] | 0.47 [0.36, 0.57] |
| GBT: graph baselines + dominator | 0.82 [0.76, 0.88] | 0.56 [0.42, 0.72] | 0.59 [0.39, 0.74] | 0.88 [0.84, 0.92] | 0.41 [0.35, 0.49] | 0.49 [0.38, 0.56] |

**`T-main`**

| model | PFR AUC | PFR AP | PFR P@k | Carleson AUC | Carleson AP | Carleson P@k |
|---|---|---|---|---|---|---|
| LR: graph baselines (c, d, e, f, out-degree, reachable) | 0.77 [0.71, 0.83] | 0.72 [0.65, 0.82] | 0.59 [0.40, 0.69] | 0.80 [0.76, 0.85] | 0.40 [0.34, 0.48] | 0.45 [0.38, 0.54] |
| LR: dominator features only (a, b, g) | 0.67 [0.58, 0.76] | 0.66 [0.58, 0.78] | 0.54 [0.39, 0.64] | 0.73 [0.68, 0.79] | 0.35 [0.30, 0.42] | 0.47 [0.37, 0.54] |
| LR: graph baselines + dominator | 0.77 [0.70, 0.84] | 0.72 [0.63, 0.84] | 0.58 [0.40, 0.69] | 0.80 [0.75, 0.85] | 0.40 [0.34, 0.48] | 0.47 [0.39, 0.55] |
| LR: size only (source lines, own proof size, statement size) | 0.77 [0.71, 0.84] | 0.74 [0.64, 0.84] | 0.58 [0.40, 0.67] | 0.78 [0.73, 0.83] | 0.35 [0.30, 0.41] | 0.35 [0.29, 0.43] |
| LR: surface cues without docstring (private, name length, name parts) | 0.61 [0.50, 0.73] | 0.53 [0.46, 0.69] | 0.52 [0.40, 0.60] | 0.52 [0.44, 0.59] | 0.15 [0.11, 0.19] | 0.14 [0.07, 0.20] |
| LR: surface cues (docstring, private, name length, name parts) | 0.87 [0.81, 0.92] | 0.86 [0.79, 0.92] | 0.62 [0.40, 0.80] | 0.84 [0.76, 0.91] | 0.51 [0.40, 0.62] | 0.56 [0.47, 0.71] |
| LR: surface + length (source lines, statement chars) | 0.87 [0.80, 0.92] | 0.84 [0.78, 0.90] | 0.63 [0.40, 0.80] | 0.90 [0.86, 0.94] | 0.55 [0.46, 0.65] | 0.57 [0.48, 0.67] |
| LR: surface + graph baselines | 0.89 [0.84, 0.92] | 0.85 [0.79, 0.91] | 0.64 [0.40, 0.80] | 0.92 [0.88, 0.95] | 0.63 [0.54, 0.71] | 0.68 [0.54, 0.77] |
| LR: surface + length + graph baselines | 0.89 [0.83, 0.92] | 0.85 [0.79, 0.90] | 0.64 [0.40, 0.79] | 0.92 [0.88, 0.94] | 0.61 [0.52, 0.69] | 0.65 [0.53, 0.74] |
| LR: surface + graph baselines + dominator | 0.89 [0.84, 0.92] | 0.85 [0.81, 0.91] | 0.64 [0.40, 0.80] | 0.92 [0.88, 0.95] | 0.62 [0.54, 0.72] | 0.67 [0.53, 0.76] |
| GBT: graph baselines | 0.69 [0.58, 0.79] | 0.61 [0.47, 0.82] | 0.56 [0.40, 0.65] | 0.80 [0.76, 0.84] | 0.41 [0.35, 0.49] | 0.43 [0.36, 0.53] |
| GBT: graph baselines + dominator | 0.69 [0.58, 0.78] | 0.62 [0.48, 0.81] | 0.54 [0.40, 0.65] | 0.80 [0.76, 0.84] | 0.40 [0.34, 0.48] | 0.44 [0.36, 0.52] |

**Ablation: what the dominator features add (paired, module-cluster bootstrap).**

| comparison | set | PFR dAUC | PFR dAP | Carleson dAUC | Carleson dAP |
|---|---|---|---|---|---|
| graph + dominator minus graph | `T-all` | +0.001 [−0.004, +0.009] | +0.007 [−0.006, +0.025] | +0.003 [−0.004, +0.010] | +0.006 [−0.022, +0.038] |
| graph + dominator minus graph | `T-main` | +0.001 [−0.026, +0.019] | +0.007 [−0.040, +0.040] | −0.004 [−0.015, +0.006] | −0.001 [−0.037, +0.029] |
| surface + graph + dominator minus surface + graph | `T-all` | +0.001 [−0.002, +0.004] | +0.004 [−0.004, +0.012] | +0.000 [−0.003, +0.003] | −0.003 [−0.025, +0.024] |
| surface + graph + dominator minus surface + graph | `T-main` | +0.001 [−0.005, +0.005] | +0.007 [−0.004, +0.026] | +0.002 [−0.002, +0.007] | −0.008 [−0.032, +0.015] |
| GBT graph + dominator minus GBT graph | `T-all` | +0.003 [−0.011, +0.017] | −0.020 [−0.066, +0.052] | +0.003 [−0.004, +0.011] | +0.006 [−0.033, +0.044] |
| GBT graph + dominator minus GBT graph | `T-main` | −0.000 [−0.035, +0.030] | +0.010 [−0.046, +0.055] | −0.003 [−0.018, +0.009] | −0.009 [−0.047, +0.022] |

**What the graph is worth against simpler feature sets (paired, module-cluster bootstrap).**

| comparison | set | PFR dAUC | PFR dAP | Carleson dAUC | Carleson dAP |
|---|---|---|---|---|---|
| graph minus size only | `T-all` | +0.082 [−0.004, +0.164] | +0.099 [+0.015, +0.189] | +0.040 [+0.018, +0.059] | +0.073 [+0.025, +0.128] |
| graph minus size only | `T-main` | +0.001 [−0.072, +0.047] | −0.023 [−0.075, +0.021] | +0.024 [−0.001, +0.049] | +0.050 [−0.003, +0.106] |
| graph minus surface without docstring | `T-all` | +0.049 [−0.033, +0.129] | +0.174 [+0.047, +0.287] | +0.239 [+0.128, +0.370] | +0.236 [+0.169, +0.317] |
| graph minus surface without docstring | `T-main` | +0.160 [−0.007, +0.309] | +0.190 [+0.020, +0.317] | +0.282 [+0.188, +0.383] | +0.252 [+0.197, +0.325] |
| graph minus surface with docstring | `T-all` | −0.049 [−0.110, +0.014] | −0.084 [−0.200, +0.032] | −0.026 [−0.084, +0.031] | −0.139 [−0.272, +0.011] |
| graph minus surface with docstring | `T-main` | −0.097 [−0.193, −0.009] | −0.141 [−0.226, −0.056] | −0.039 [−0.131, +0.067] | −0.112 [−0.232, −0.002] |
| surface + graph minus surface | `T-all` | +0.034 [+0.002, +0.079] | +0.052 [−0.010, +0.143] | +0.046 [+0.020, +0.083] | +0.090 [+0.029, +0.188] |
| surface + graph minus surface | `T-main` | +0.022 [−0.026, +0.057] | −0.010 [−0.061, +0.035] | +0.076 [+0.026, +0.144] | +0.118 [+0.065, +0.188] |
| surface + length + graph minus surface + length | `T-all` | +0.024 [−0.001, +0.048] | +0.035 [−0.014, +0.082] | +0.016 [+0.003, +0.032] | +0.078 [+0.024, +0.143] |
| surface + length + graph minus surface + length | `T-main` | +0.016 [−0.013, +0.038] | +0.008 [−0.029, +0.037] | +0.011 [−0.004, +0.025] | +0.060 [−0.001, +0.108] |

- **Dominator features add nothing**, with or without surface cues, in either project, linear or boosted: 12 of 12 AUC intervals contain zero and every point estimate is within ±0.004 AUC.
- **Against size alone the graph adds little.** On all theorems the graph model beats the size-only model by +0.082 AUC in PFR (interval includes zero) and +0.040 in Carleson (clear of zero). On mainline theorems the gain is +0.001 and +0.024, with both intervals including zero. What the graph adds over size is mostly reachability from the headline theorems, i.e. telling the main argument from the staging folders.
- **Against surface cues that include length the graph adds +0.011 to +0.024 AUC**; the AUC interval is clear of zero only for Carleson `T-all` (+0.016 [+0.003, +0.032]), and the average-precision gain is clear of zero only there (+0.078 [+0.024, +0.143]). The earlier figure of +0.03 to +0.08 compared against a surface set with no length feature.
- **The docstring flag carries the surface model.** With it the surface model scores 0.90 / 0.90 on all theorems; without it 0.80 / 0.63, and on mainline theorems 0.61 / 0.52 against 0.77 / 0.80 for the graph.
- **Cross-project transfer holds up**, so the models are not memorising one project. Graph baselines fitted on PFR score 0.86 AUC on Carleson (0.83 the other way); adding dominator features changes these to 0.85 and 0.82. See `tables.md`.

## Root sensitivity

Dominated proof mass recomputed from one headline theorem at a time (AUC over all theorems, and over theorems reachable from that root).

| project | root | reachable declarations | AUC, all theorems | AUC, reachable theorems | blueprint theorems reachable |
|---|---|---|---|---|---|
| pfr | `(virtual root over all)` | 830 | 0.78 | 0.75 | 210 of 225 |
| pfr | `weak_PFR_int` | 503 | 0.56 | 0.70 | 110 of 225 |
| pfr | `torsion_PFR` | 443 | 0.59 | 0.74 | 108 of 225 |
| pfr | `homomorphism_pfr` | 456 | 0.53 | 0.71 | 90 of 225 |
| pfr | `approx_hom_pfr` | 455 | 0.53 | 0.71 | 90 of 225 |
| pfr | `PFR_conjecture_improv` | 415 | 0.57 | 0.71 | 97 of 225 |
| pfr | `PFR_conjecture` | 400 | 0.56 | 0.69 | 93 of 225 |
| pfr | `Marton.weak_pfr_int` | 505 | 0.57 | 0.71 | 111 of 225 |
| pfr | `Marton.torsion_pfr_conjecture` | 444 | 0.59 | 0.73 | 108 of 225 |
| pfr | `Marton.pfr_conjecture_nine` | 456 | 0.52 | 0.70 | 89 of 225 |
| pfr | `Marton.pfr_conjecture` | 402 | 0.56 | 0.69 | 93 of 225 |
| pfr | `Marton.homomorphism_pfr` | 458 | 0.53 | 0.70 | 90 of 225 |
| pfr | `Marton.approx_hom_pfr` | 462 | 0.54 | 0.70 | 94 of 225 |
| carleson | `(virtual root over all)` | 2,344 | 0.83 | 0.83 | 212 of 229 |
| carleson | `metric_carleson` | 1,892 | 0.68 | 0.83 | 154 of 229 |
| carleson | `linearized_metric_carleson` | 1,856 | 0.68 | 0.83 | 152 of 229 |
| carleson | `classical_carleson_check` | 2,344 | 0.83 | 0.83 | 212 of 229 |
| carleson | `classical_carleson` | 2,342 | 0.83 | 0.83 | 212 of 229 |

- **PFR depends on the root set.** A single root reaches 400–505 declarations instead of 830, and AUC over all theorems falls to 0.52–0.59. Within the reachable set it is 0.69–0.74, close to the virtual root's 0.75. The virtual root over twelve theorems is what makes reachability a useful feature (AUC 0.61 on its own).
- **Carleson:** the two `classical_carleson` roots reproduce the virtual-root numbers; the two metric roots reach less and score lower over all theorems.
- **The sensitivity does not rescue the dominator idea:** no root choice lifts dominated mass above the size baselines.

## Leakage: which features could be contaminated

- **Blueprint tooling leaves no mark in Lean.** Both projects use the classic `leanblueprint` + `checkdecls` setup, where `\lean{...}` lives in the LaTeX. No Lean file contains a `@[blueprint]` attribute, so no attribute or generated docstring is added to tagged declarations.
- **Docstrings are contaminated by convention, not tooling.** In PFR 95 of 204 tagged-theorem docstrings contain LaTeX `$…$` (the blueprint statement pasted in) against 28 of 254 untagged ones. In Carleson 40 of 178 tagged docstrings cite blueprint numbering ("Lemma 7.2.3", "in the blueprint") against 28 of 213 untagged. The docstring flag is therefore partly the label itself; treat it as an upper bound on honest surface cues, not as a fair competitor. This is why the surface model is reported with and without it.
- **Name length is a folder proxy** in PFR (see above). Not contaminated by the blueprint, but not a property of importance either.
- **Folder effect on graph features.** 36% of tagged PFR theorems sit in staging folders that the blueprint covers only selectively, and reachability alone gets AUC 0.61. `T-main` and `T-main-reach` remove this.
- **Root effect.** Dominator features are defined relative to the headline theorems, which are themselves blueprint nodes in 6 of 12 (PFR) and 3 of 4 (Carleson) cases. That is at most 6 positives and does not move any number.
- **"Top-level theorem of its file"** was a worry in the brief. No positional feature (line number, last-in-file) is used; the reviewer measured "last theorem in its module" at AUC 0.51 (PFR) and 0.54 (Carleson). In-degree 0 is not a giveaway: only 6% of tagged PFR theorems have no user, against 17% of untagged.
- **Size is the confound that matters.** Tagged theorems have a median proof of 2,617 subterms against 523 (PFR) and 3,410 against 545 (Carleson). Any score correlated with proof size inherits AUC ≈ 0.75–0.81 for free; dominated mass includes own proof size.

## Structure: Lean graph restricted to blueprint nodes against the blueprint `\uses` graph

Nodes are blueprint nodes with at least one exported declaration (PFR 206, Carleson 170). An ordered pair (A, B) is a human edge if A `\uses` B in the statement or proof. Chance precision is the edge density: 0.011 (PFR, 466 edges) and 0.007 (Carleson, 212 edges).

| Lean relation A → B | PFR edges | PFR precision | PFR recall | Carleson edges | Carleson precision | Carleson recall |
|---|---|---|---|---|---|---|
| direct dependency | 794 | 0.40 | 0.69 | 154 | 0.68 | 0.49 |
| reachable with no blueprint declaration in between | 1,166 | 0.35 | 0.87 | 353 | 0.56 | 0.94 |
| reachable (transitive) | 4,958 | 0.09 | 0.91 | 2,502 | 0.08 | 0.94 |
| dominator tree: A is B's nearest blueprint ancestor | 121 | 0.71 | 0.18 | 171 | 0.73 | 0.58 |
| dominator tree: A is any blueprint ancestor of B | 432 | 0.20 | 0.18 | 1,127 | 0.11 | 0.58 |

Against the transitive closure of `\uses` (4,460 pairs in PFR, 2,474 in Carleson): Lean reachability has precision 0.84 / recall 0.93 (PFR) and 0.95 / 0.96 (Carleson); dominator ancestry has precision 0.97 / 1.00 but recall 0.09 / 0.45.

- **The two graphs agree on order.** No human edge runs the opposite way in Lean. 42 of 466 (PFR) and 12 of 212 (Carleson) human edges join declarations with no Lean dependency in either direction; these are `\uses` that the formal proof does not need.
- **Reachability reproduces the human graph's shape.** Contracted reachability recovers 87% and 94% of human edges. Of its extra edges, 71% (PFR) and 64% (Carleson) are in the `\uses` closure, i.e. indirect human dependencies that Lean uses directly; the rest are Lean dependencies the blueprint does not record at all.
- **The dominator tree is a precise but thin skeleton.** When it says "B sits under A" (nearest blueprint ancestor), the human graph agrees 71–73% of the time directly and 97–99% transitively. But a tree has at most one parent per node, and blueprint nodes have 2.3 (PFR) and 1.2 (Carleson) uses each on average.
- **PFR is the hard case for dominators.** Only 119 of 197 reachable blueprint nodes have any blueprint dominator ancestor: the entropy toolkit is shared by many chapters, so its lemmas are dominated only by the root. Carleson is more tree-like (159 of 164), which is why recall is 0.58 there.
- **This comparison is partly circular.** Blueprint `\uses` is meant to mirror the Lean dependencies, and the dependency-graph tool is used to keep them in step, so high reachability agreement is expected rather than a discovery.

## Ten high-scoring declarations that are not in the blueprint

Ranked by dominated proof mass and by the out-of-fold graph-only model; both lists overlap heavily (`examples_pfr.json`, `examples_carleson.json`). "Dominates n" counts declarations used only through it. Counts and masses are read from `scores_*.csv`; descriptions and verdicts are one reader's.

| declaration | where | dominates | what it is | verdict |
|---|---|---|---|---|
| `phiMinimizer_exists_rdist_eq_zero` | PFR.RhoFunctional:1852 | 57, mass 201,306 | Short statement (335 nodes): a φ-minimiser with distance zero exists. Sole user is blueprint `pfr-rho`; it packages blueprint nodes `phi_min_exists` and `dist_of_min_eq_zero`. | Plausible omission: a real chapter boundary the blueprint leaves implicit. |
| `weak_PFR_asymm_prelim` | PFR.WeakPFR:625 | 61, mass 152,815 | Preliminary form of blueprint theorem `weak_PFR_asymm`, its only user. | Variant of a blueprint node, not noise. |
| `dist_of_min_eq_zero'` | PFR.RhoFunctional:1773 | 35, mass 152,046 | Primed version carrying the actual proof; blueprint tags the unprimed wrapper. | Variant. |
| `tau_strictly_decreases_aux'` | PFR.ImprovedPFR:677 | 27, mass 146,650 | Body of blueprint theorem `tau_strictly_decreases'` (`de-prop-improv`). | Variant. |
| `averaged_final` | PFR.ImprovedPFR:667 | 26, mass 139,482 | Undocumented intermediate step collecting four blueprint lemmas (`averaged_construct_good`, `dist_diff_bound_1/2`, `gen_ineq_01`). | Plausible omission, but its statement is long (1,635 nodes). |
| `condRuzsaDist_nonneg` | PFR.ForMathlib.Entropy.RuzsaDist:573 | 37, mass 35,593 | Used once, by blueprint `fibring-ineq`; pulls in the whole kernel Ruzsa-distance development. | Noise for an outline: a trivial fact that happens to be the only door into a library. |
| `R_truncation'` | Carleson.MetricCarleson.Truncation:603 | 1,381, mass 2,957,674 | Primed version of blueprint lemma `R-truncation`; nearly the whole metric-space proof sits under it. | Variant. |
| `finitary_carleson_step` | Carleson.MetricCarleson.Truncation:81 | 1,284, mass 2,832,398 | Induction step wrapped around blueprint node `finitary_carleson`. | Plausible omission (formalisation-specific step). |
| `forest_union_optimized` / `forest_union_aux` | Carleson.Discrete.ForestUnion:970, 833 | 555 / 552 | Sharper-constant and auxiliary versions of blueprint lemma `forest-union`. | Variant. |
| `control_approximation_effect'` | Carleson.Classical.ControlApproximationEffectContinuous:177 | 413, mass 687,047 | Primed version; dominates four blueprint lemmas on Dirichlet kernels. | Variant. |

- **Mostly variants, little noise.** Among the top 25 untagged theorems by dominated mass, 20 (PFR) and 17 (Carleson) are a dominator-tree parent or child of a blueprint declaration or share its name stem; among the top 100, 57 and 65. The base rate for being a dominator-tree neighbour of a blueprint declaration is 36% (PFR) and 37% (Carleson) of untagged reachable theorems.
- **Why they count as errors.** Dominator chains (`foo` → `foo'` → `foo_aux`) carry almost the same mass at every link; the blueprint names one link, the score rewards all of them. Membership metrics punish this; a reader would not.
- **The edge fix moved one chain.** Blueprint lemmas `S_truncation` and `linearized_truncation` now dominate 1,304 and 1,303 declarations (13 and 12 before the fix, when a false edge gave their subtree a second entrance), so they sit on the same chain as `R_truncation'` and `finitary_carleson_step`.
- **Also in the PFR top list:** the six `Marton.*` restatements in `PFRPalomar.Solution`, which are our roots. They are wrappers, i.e. noise caused by the root choice.

## Ten blueprint declarations the graph scores badly

Rank is by the graph-only model among all theorems (978 in PFR, 2,675 in Carleson).

| declaration | blueprint node | rank | why the graph misses it |
|---|---|---|---|
| `hahn_banach` (PFR.HomPFR:31) | `hb-thm` | 881 | Not used by any project declaration (in-degree 0, out-degree 0): the final proof goes another way. Unreachable, so every dominator score is 0. |
| `ProbabilityTheory.entropy_le_log_card` (PFR.ForMathlib.Entropy.Basic:81) | `jensen-bound` | 884 | Proof of 44 subterms, 1 user, not on any path from the headline theorems. A textbook fact the blueprint states for the reader. |
| `sum_uvw_eq_zero` (PFR.Endgame:311) | `key-ident` | 817 | The "key identity" U + V + W = 0: a one-line algebraic fact with no project dependencies. Mathematically central, structurally a leaf. |
| `condKLDiv_nonneg`, `KLDiv_eq_zero_iff_identDistrib` (PFR.Kullback) | `Conditional-Gibbs`, Gibbs | 776, 751 | Side results of the Kullback–Leibler chapter that the headline theorems do not use. |
| `card_of_dual` (PFR.ApproxHomPFR:194) | `gdual` | 720 | Small counting lemma (164 subterms), 2 users, dominates nothing. |
| `ProbabilityTheory.IdentDistrib.entropy_congr` (PFR.ForMathlib.Entropy.Basic:76) | `copy-ent` | 656 | Tiny proof, 40 users. A shared-library fact; dominated only by the root. This is exactly the layer dominators cannot see. |
| `support_holderApprox_subset` (Carleson.HolderVanDerCorput:165) | `Lipschitz-Holder-approximation` | 2,385 | One of several declarations a single blueprint lemma is split into; each piece is small. |
| `laverage_le_globalMaximalFunction` (Carleson.ToMathlib.HardyLittlewood:34) | `Hardy-Littlewood` | 1,852 | A blueprint *proposition* whose Lean counterpart is spread over a staging file; the tagged piece has a 466-subterm proof and 7 users. |
| `periodic_dirichletApprox` (Carleson.Classical.HilbertStrongType:419) | `Dirichlet-approximation` | 1,828 | Unused part of a multi-part blueprint lemma (in-degree 0, unreachable). |
| `tsum_eLpNorm_czRemainder_le`, `eLpNorm_czRemainder_le`, `integral_czRemainder` (Carleson.TwoSidedCarleson.WeakCalderonZygmund) | `Calderon-Zygmund-decomposition` | 1,170, 1,074, 1,102 | Clauses of one blueprint lemma proved as separate theorems; these clauses are not needed by the headline theorems. |

The misses fall into four kinds:
- **Not on the main line.** 7% of tagged theorems in each project are unreachable from the headline theorems (15 of 225 in PFR, 17 of 229 in Carleson). No root-relative score can find them.
- **Small but conceptually central facts** (`key-ident`). Importance to a reader is not proof mass.
- **Shared toolkit lemmas** with many users. Dominators miss them by construction, and in-degree does not rescue them (AUC 0.55 and 0.52) because most heavily used declarations are not blueprint material.
- **One blueprint node, several Lean declarations.** The unit of the blueprint is coarser than the Lean declaration; each fragment looks unimportant.

## Plain verdict on H3

- **As stated, H3 is weakly supported and not in the form we wanted.** The dependency graph alone ranks blueprint theorems clearly above chance (AUC 0.85–0.87, average precision 0.65 in PFR and 0.36 in Carleson against base rates 0.23 and 0.09). But at k it recovers about 60% of the PFR blueprint theorems and 34% of Carleson's, which is not a usable reconstruction of the human interface.
- **What the graph detects is proof length plus the main-argument/staging split.** A size-only model reaches 0.76 / 0.83, and on mainline theorems the graph model is not distinguishable from it. The graph's gain over size is clear of zero only in Carleson on all theorems.
- **The dominator-tree claim is negative.** Dominator features add nothing measurable to transitive mass, own proof size and out-degree, under four evaluation sets, two model families, cross-project transfer and every root choice tried. A dominator-only model is worse than the naive baselines (AUC 0.73 vs 0.85 in PFR, 0.80 vs 0.87 in Carleson).
- **The "short statement hiding a large subtree" criterion is contradicted.** Human blueprint statements are longer than average, and dividing by statement size lowers every metric.
- **The docstring flag alone matches the graph, but it is partly the label.** The remaining surface cues (privacy, name shape) do worse than the graph; adding length to them closes most of the gap.
- **Structure is the better news.** Reachability restricted to blueprint nodes reproduces the human `\uses` graph (recall 0.87–0.94 direct, precision 0.84–0.95 against its closure). Dominator-tree parents are 71% precise but cover a minority of human edges in PFR. Part of this agreement is by construction.
- **What this does and does not say about the machine corpus.** These two projects were factored by people who also wrote the blueprint, and in both the dominator tree's large-mass nodes are mostly variants of blueprint nodes rather than junk. That is consistent with "the dominator tree gives a navigable skeleton" but it is not evidence that it *selects* what a human would select; on that question the result is negative. Two projects are a small sample, and both come from the same community and tooling.

## Files

- `bench/validate_outline.py`: features, metrics, module-cluster bootstrap, models, structure comparison, root sensitivity. About 5 minutes with `--boot 1000`.
- `bench/validate_outline_extra.py`: chain/variant analysis, tagged-vs-untagged shares, docstring LaTeX count.
- `bench/validate_outline_report.py`: writes this file from the outputs of the two scripts above.
- `out/corpus/validation/tables.md`: every table for every evaluation set (generated).
- `out/corpus/validation/results.json`, `extra.json`: all numbers.
- `out/corpus/validation/scores_pfr.csv`, `scores_carleson.csv`: per-declaration features and out-of-fold model scores.
- `out/corpus/validation/examples_pfr.json`, `examples_carleson.json`: top untagged and bottom tagged declarations with statements.
- `out/corpus/_before_fix/`: the exports and reports as they stood before the review fixes, for comparison.
