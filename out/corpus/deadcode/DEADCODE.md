# What you need not read: dead code in the machine-generated Navier–Stokes / Euler corpus

Plan node M4, 2026-11-10. Corpus: `openai/NavierStokesAndEuler@f9e8bc5b` built at `corpora/ns` (Lean 4.34.0-rc2), 2,657 project files, 52,505 declarations. Script: `bench/deadcode.py`. All deletions were made in a copy (`corpora/ns_trim/work`); `corpora/ns` is untouched.

## Result

**13,625 declarations and 233 whole files (158,394 lines, 24.7% of the corpus) were deleted, and all four headline theorems still compile with the same three axioms.** The target for this node (sample confirmed, control fails as it should) is met, with one control and eight sampled deletions that did not behave as the term graph predicts; both are explained below.

| | before | after deleting everything classified dead | change |
|---|---:|---:|---:|
| project files | 2,657 | 2,424 | −233 (−8.8%) |
| source lines | 640,860 | 482,466 | −158,394 (−24.7%) |
| declarations | 52,505 | 38,880 | −13,625 (−25.9%) |
| theorems | 38,601 | 26,961 | −11,640 (−30.2%) |
| headline theorems check, axioms `propext`, `Classical.choice`, `Quot.sound` | 4 of 4 | 4 of 4 | none |
| declarations reachable from a headline theorem (re-exported from the trimmed build) | 37,070 | 37,070 | none |
| build time | 1,068 s wall, 16,936 module-seconds (recorded build of 9 November) | **not measured cleanly**; estimated 13,400 to 14,100 module-seconds | about −17% to −21% (estimate) |

- **29.4% of declarations (15,435) and 32.4% of theorems (12,516) are not used by any of the four headline theorems.** That is 157,444 declaration lines, 24.6% of all source lines.
- **The term graph alone is not a safe deletion list.** In a seeded sample of 300 unreachable theorems, 8 deletions broke the build (2.7%). All 8 are one-line lemmas proved by `rfl`: `simp` uses them by unfolding and leaves no trace in the proof term. Lean's own reference index (`.ilean`) predicted 7 of the 8; the eighth carries `@[simp]` and is used without being named.
- **After excluding what those two signals flag, nothing broke.** 270 of the 300 sampled theorems were classified dead and none of them broke the build; the full deletion of all 13,625 then went through on the first build.
- **1,810 unreachable declarations were not deleted**: 176 are needed by the elaborator (known by name), 1,634 are held back because they carry an attribute, are instances or abbreviations, or are named in a command of a file that stays. In the sample, 1 of 496 such deletions broke the build.
- **The outline does not change on the predicted graph.** `bench/outline.py` on the original graph minus the deleted declarations gives byte-identical output to the original graph (same hash seed). On the graph Lean re-exports from the trimmed build, 63 numeric fields of `shape.json` move by at most 0.03 points (total mass +2,588 Navier-Stokes, +9,843 Euler), because of the auxiliary definitions noted under Stage 3; chapters and reachable counts do not change.

## What "reachable" means here

- **Graph.** Node = exported declaration; edge A → B when A's statement or proof term mentions B (`typeDeps ∪ valueDeps` of `out/corpus/ns/decls.jsonl`, exported from the built environment). Auxiliaries, constructors and projections are folded into their parent by the exporter.
- **Roots.** The four headline theorems of `main_theorems.json`: `NavierStokes.Comparator.navier_stokes_breakdown_R3`, `…breakdown_periodic`, `Euler.euler_breakdown_R3`, `Euler.exists_compact_smooth_euler_singularity`.
- **Reachable** = in the dependency closure of a root: 37,070 declarations. This is exactly what the kernel needs to check the four theorems (`out/corpus/ns/README.md` verifies the closure against the raw constant closure).
- **Second graph, also from Lean.** The `.ilean` files of the build record every source position where the elaborator resolved a constant, with the enclosing declaration. An edge A ⇢ B means "the source of A names B". This sees uses that vanish from the term (`simp only [foo]` where `foo` is true by unfolding) and uses in commands outside any declaration (`variable (D : Data)`, `export`, `open`).
- **What neither graph sees**: a `@[simp]` lemma that `simp` applies by unfolding without being named, a `local instance` that only shortens type-class search, and anything decided by notation or by the order of imports. These are the reason for the held class.

## What is unreachable

### By kind

| kind | all | not reachable from a headline theorem | share |
|---|---:|---:|---:|
| theorem | 38,601 | 12,516 | 32.4% |
| def | 11,721 | 2,298 | 19.6% |
| instance | 1,517 | 465 | 30.7% |
| structure | 652 | 152 | 23.3% |
| inductive | 14 | 4 | 28.6% |
| **all** | 52,505 | 15,435 | 29.4% |

### By library

| library | declarations | unreachable | share | theorems | unreachable theorems | share |
|---|---:|---:|---:|---:|---:|---:|
| NavierStokes | 36,203 | 12,347 | 34.1% | 27,301 | 10,151 | 37.2% |
| Euler | 16,302 | 3,088 | 18.9% | 11,300 | 2,365 | 20.9% |

### By source lines

| measure | lines |
|---|---:|
| all lines of the 2,657 project files | 640,860 |
| lines inside a declaration (Lean declaration ranges, plus `omit/include ... in` prefixes) | 510,729 |
| ... of unreachable declarations | 157,444 (30.8% of declaration lines, 24.6% of all lines) |
| proof size (distinct subterms) of unreachable theorems | 13,183,334 of 48,624,258 (27.1%) |

### By module

| | modules | declarations | lines |
|---|---:|---:|---:|
| project modules (two root files and three import hubs have no declarations) | 2,657 | 52,505 | 640,860 |
| in the import closure of the two headline modules | 2,438 | | |
| every declaration reachable | 1,039 | | |
| some unreachable, some reachable | 1,312 | | |
| ... of which at least half unreachable | 264 | | |
| **wholly unreachable** | **301** | 4,147 | 57,201 |
| ... imported on the way to a headline theorem, nothing in them used | 87 | 531 | 9,226 |
| ... imported only from the root files (paper-form results and their support) | 141 | 1,366 | 21,970 |
| ... imported by nothing (orphans, built only by the Lake glob) | 73 | 2,250 | 26,005 |

Largest wholly unreachable modules: `NavierStokes.CorrectionInitializationNoOptions` (393 decls, 5573 lines), `NavierStokes.WaveStageContinuation` (162 decls, 1995 lines), `NavierStokes.ActualParticularPhysicalData` (151 decls, 1783 lines), `NavierStokes.InitialHarmonicContinuation` (159 decls, 1459 lines), `NavierStokes.MeanResidual` (150 decls, 1166 lines), `NavierStokes.ActualCorrectionModels` (117 decls, 985 lines), `NavierStokes.SignedRequestContinuation` (100 decls, 751 lines), `NavierStokes.MeanStageContinuation` (73 decls, 732 lines), `NavierStokes.CycleContinuationInvariant` (57 decls, 665 lines), `NavierStokes.InitialDyadicSource` (74 decls, 658 lines), `NavierStokes.BoundaryCoordinates` (52 decls, 488 lines), `NavierStokes.ReferenceUniformStocks` (41 decls, 461 lines).

Partly unreachable modules with the most unreachable lines:

| module | declarations | unreachable | unreachable lines | file lines |
|---|---:|---:|---:|---:|
| `NavierStokes.CorrectionStep` | 559 | 287 | 4,925 | 9,849 |
| `Euler.EulerProof` | 1239 | 308 | 4,518 | 20,755 |
| `NavierStokes.CorrectionInitialization` | 393 | 131 | 1,938 | 5,562 |
| `NavierStokes.ParticularWaveBounds` | 124 | 64 | 1,473 | 2,602 |
| `NavierStokes.SignedWaveUpdate` | 97 | 61 | 1,036 | 1,472 |
| `NavierStokes.ParticularWaveAssembly` | 174 | 102 | 976 | 2,015 |
| `NavierStokes.WaveInteractionBounds` | 96 | 79 | 961 | 1,187 |
| `NavierStokes.PhysicalSignedWave` | 143 | 94 | 948 | 1,575 |
| `NavierStokes.PhysicalParticularWave` | 141 | 99 | 943 | 1,464 |
| `NavierStokes.CommonCoverClass` | 126 | 94 | 849 | 1,321 |
| `NavierStokes.TemporalMeanUpdate` | 116 | 57 | 843 | 1,539 |
| `NavierStokes.MeanRankUpdate` | 181 | 80 | 836 | 2,037 |
| `NavierStokes.OffplaneCorrectionExtensions` | 112 | 107 | 813 | 1,083 |
| `NavierStokes.UniformFourierAlias` | 102 | 50 | 806 | 1,334 |
| `NavierStokes.SignedCovariance` | 70 | 57 | 800 | 976 |

### Cloned modules

The 13 modules that `out/corpus/reuse/REUSE.md` identified as namespace-renamed copies. All 488 of their declarations are unreachable, and nothing imports any of them. In 9 of the 13 base modules some declarations are unreachable too (154 in all).

| clone | lines | declarations | unreachable | base module | base declarations | base unreachable | imported by anything |
|---|---:|---:|---:|---|---:|---:|---|
| `Euler.BaseFirstPacketChoiceNoOptions` | 145 | 6 | 6 | `BaseFirstPacketChoice` | 6 | 0 | no |
| `Euler.BaseFirstPacketEvolutionNoOptions` | 159 | 3 | 3 | `BaseFirstPacketEvolution` | 3 | 0 | no |
| `Euler.BaseInductionStageNoOptions` | 130 | 4 | 4 | `BaseInductionStage` | 4 | 3 | no |
| `Euler.GevreyGeneratingDerivativesNoOptions` | 152 | 9 | 9 | `GevreyGeneratingDerivatives` | 9 | 1 | no |
| `Euler.LpCylinderCoefficientTimeInvestigation` | 148 | 14 | 14 | `LpCylinderCoefficientTime` | 14 | 0 | no |
| `Euler.MeanPacketEnvelopeBoundsNoOptions` | 117 | 1 | 1 | `MeanPacketEnvelopeBounds` | 1 | 0 | no |
| `Euler.PacketShiftArithmeticNoOptions` | 73 | 14 | 14 | `PacketShiftArithmetic` | 14 | 4 | no |
| `Euler.ParentGeometryForwardChoiceNoOptions` | 161 | 14 | 14 | `ParentGeometryForwardChoice` | 14 | 1 | no |
| `Euler.ParentGeometryJoinedChoiceInvestigation` | 128 | 6 | 6 | `ParentGeometryJoinedChoice` | 6 | 2 | no |
| `Euler.TransversePacketCorrectorNoOptions` | 39 | 7 | 7 | `TransversePacketCorrector` | 34 | 2 | no |
| `NavierStokes.ActualParticularDynamicsNoOptions` | 143 | 2 | 2 | `ActualParticularDynamics` | 93 | 4 | no |
| `NavierStokes.CorrectionInitializationNoOptions` | 5,573 | 393 | 393 | `CorrectionInitialization` | 393 | 131 | no |
| `NavierStokes.DiagonalJetBoundsNoOptions` | 340 | 15 | 15 | `DiagonalJetBounds` | 15 | 6 | no |
| **total** | 7,308 | 488 | 488 | | | 154 | |

### By status

| status | declarations | declaration lines | by kind |
|---|---:|---:|---|
| named in the source of a reachable declaration, absent from its term (elaboration-only dependency) | 176 | 382 | 176 theorem |
| held back: carries an attribute, is an instance or an abbreviation, is named in a command of a kept file, or is needed by one of those | 1,634 | 5,279 | 700 theorem, 465 instance, 396 def, 72 structure, 1 inductive |
| **classified dead** | **13,625** | **151,783** | 11,640 theorem, 1,902 def, 80 structure, 3 inductive |

## How the unreachable set divides

### By what it is for: (a) superseded, (b) no term use, (c) other setting

Stated rule, first match wins:

1. **a1** the declaration is in one of the 13 cloned modules;
2. **a2** a reachable declaration has the identical statement (exact statement key; for non-theorems the statement hash and at least 8 nodes);
3. **a3** a reachable theorem is the same derivation up to numerals (none found);
4. **c1** a reachable theorem has the same statement and proof up to one renaming of project constants (keys of `out/corpus/reuse/stmt_keys.jsonl`);
5. **c2** a reachable theorem has the same statement up to numerals;
6. **c3** the declaration is in, or is used by a declaration of, a *root result module*: one of the 34 modules that `NavierStokes.lean` / `Euler.lean` import (through declaration-free hubs) besides the headline modules. They hold the results in the papers' own form: the local theorem, the periodic corollary as printed, appendix lemmas, `Euler.EulerSingularity`;
7. **a4** the declaration is in a module nothing imports (74 such modules, built only because the Lake glob builds every file), or every chain of users above it ends in such a module;
8. **b** everything else. A non-theorem with no match takes the majority class of the unreachable theorems that use it.

| class | rule | theorems | other declarations |
|---|---|---:|---:|
| a | a1 cloned module | 318 | 170 |
| a | a2 identical statement | 80 | 286 |
| a | a4 orphaned development | 1,287 | 490 |
| a | inherited from users | 0 | 10 |
| b | b no twin found | 9,611 | 1,634 |
| c | c1 same derivation up to renaming | 201 | 0 |
| c | c2 same statement up to numerals | 6 | 0 |
| c | c3 serves a root result (paper-form statement) | 1,013 | 319 |
| c | inherited from users | 0 | 10 |

| class | declarations | theorems | declaration lines | share of unreachable declarations |
|---|---:|---:|---:|---:|
| (a) alternative or superseded version | 2,641 | 1,685 | 22,073 | 17.1% |
| (b) support with no term use (includes 174 elaboration-only lemmas that `simp` needs and 1,048 held declarations) | 11,245 | 9,611 | 116,466 | 72.9% |
| (c) variant for another setting or form | 1,549 | 1,220 | 18,905 | 10.0% |

Hand-read sample of 40 (seed 20261110), rule against reader:

| rule \ reader | a | b | c |
|---|---:|---:|---:|
| a | 11 | 0 | 0 |
| b | 1 | 24 | 0 |
| c | 0 | 0 | 4 |

- **(b), support with no term use, is the bulk: 72.9%** (of which 174 are needed by elaboration and 1,048 are held, not shown dead)**.** These sit in live files next to used declarations: 5,630 unreachable declarations have no user at all, and the rest feed only those. By reading, they are corollaries packaged and never called, wrappers (the `S = univ` case of a used `_on` lemma), `rfl` restatements, and helpers of abandoned branches of a live file.
- **(a) is 17.1%, and most of it is orphaned developments (a4), not twins.** Only 854 declarations have a reachable copy (clone or identical statement). The 74 orphan modules include a flat `NavierStokes.R3*` family of about 40 files (whole-space pressure recovery through Riesz kernels, which the final ℝ³ argument under `NavierStokes/R3/` does not use) and a `…Continuation` family. Calling these "superseded" is a reading of file headers and names, not a proof.
- **(c) is 10.0%.** 1,332 declarations serve the paper-form results; 207 theorems are parallel copies for another parameter (the `q ≥ 5` / `q ≥ 6` and narrow / wide range families of `REUSE.md`).
- **Copy-and-modify families are over-represented among the dead.** Of the 2,486 theorems in a same-derivation cluster (1,124 clusters), 1,116 (44.9%) are unreachable, against 32.4% of all theorems; 308 clusters are unreachable in every member, 405 are mixed. Of 591 theorems with an identical-statement twin, 216 (36.5%) are unreachable.
- **Hand-read sample.** 40 unreachable declarations drawn with seed 20261110 (`sample40.md`, labels in `hand_sample.json`). Rule and reader agree on 39. **Limits of that figure:** the reader is the analysing agent (a model proxy, not a mathematician), was not blind to the rule's label, and the definitions of c3 and a4 were tightened after the sample had been read. It shows the rule is not wild; it does not validate it. The one disagreement is a definition re-declared under the same name as a reachable one in another module, which the rule files under (b).

## Uses that are not term dependencies

Lean can use a declaration without it appearing in any proof term. Each class below was identified from Lean or from the source inside Lean's declaration ranges, and is kept apart from "dead".

| class | how identified | unreachable declarations | treated as | what compilation showed |
|---|---|---:|---|---|
| lemma named in a reachable proof, absent from its term | `.ilean` reference with a reachable enclosing declaration | 176 (all theorems, all proved by `rfl`) | kept: elaboration-only dependency | 7 fell in the sample; all 7 broke the build when deleted |
| `@[simp]` | source attribute; equals the environment's simp set (1,264 = 1,264) | 743 (594 proved by `rfl`) | held | 102 deleted in the sample, 1 broke |
| instance (`instance`, `local instance`, or a definition whose type is a class) | declaration kind from the exporter | 474 | held | 75 deleted in the sample, 0 broke; a *used* one deleted in the control also did not break |
| `abbrev` / reducible | source keyword; environment has 901 reducible against 900 | 139 | held | 101 deleted in the sample, 0 broke |
| named in a `variable` command of a kept file | `.ilean` reference outside every declaration | 84 (57 structures, 27 definitions) | held | not deleted |
| named in an `export` or `open … (name)` command | same | 10 | held | not deleted |
| `@[ext]`, `@[fun_prop]`, `@[reducible]` | source attribute | 3 | held | not tested alone |
| notation, macros, tactics | exporter drops them (412 objects); the corpus has 151 `notation` and 4 `prefix` commands, no `macro`, `syntax` or `elab` | not declarations | untouched | no failure traced to notation |
| namespace kept alive only by dead declarations | `open X` in a kept file, `X` declared nowhere else | 18 namespaces | `open` command trimmed | 5 files failed before the trim, none after |

- **The 176 are named in `simp only [...]` (128 of them), `simpa only` (42), `simp [...]` (31), and `simp_rw`, `simpa` or `dsimp` (7); a lemma can be named in more than one way.** List with users: `elaboration_only.jsonl`. They are definitional unfoldings such as `@[simp] theorem cylinder_apply … : cylinder e x = (e x.1, x.2) := rfl`.
- **Held is small.** 1,303 tagged declarations plus 331 they depend on: 1,634 declarations, 5,279 lines (0.8% of the corpus).
- **`aesop`, `norm_cast`, `gcongr`, `positivity` extensions and `to_additive` do not occur** on any declaration in the corpus.

## Negative control

| # | declaration | kind | direct users | build target | result | first error |
|---|---|---|---:|---|---|---|
| 1 | `NavierStokes.DefectIncrementBounds.Shell.barIntegrable` | theorem | 3 | `NavierStokes.DefectIncrementBounds` | FAILED (as it should) | line 243: Invalid field `barIntegrable`: The environment does not contain `Navie |
| 2 | `EulerTransversePacketJoin.vectorField_time` | theorem | 6 | `Euler.TransversePacketJoinedField` | FAILED (as it should) | line 53: Unknown identifier `vectorField_time` |
| 3 | `NavierStokes.SignedCopyBounds.local_neg` | theorem | 1 | `NavierStokes.SignedCopyBounds` | FAILED (as it should) | line 74: Unknown identifier `local_neg` |
| 4 | `NavierStokes.NaturalAxisBridge.UniformMixedError` | def | 19 | `NavierStokes.NaturalAxisBridge` | FAILED (as it should) | line 690: Function expected at |
| 5 | `NavierStokes.GenericEndpointExtension.Gluing.future` | def | 9 | `NavierStokes.GenericEndpointExtension` | FAILED (as it should) | line 183: Invalid argument name `X` for function |
| 6 | `EulerTransversePacketProvider.HistoryData.residualPath_ae` | theorem | 2 | `Euler.TransversePacketHistoryPressure` | FAILED (as it should) | line 87: Invalid field `residualPath_ae`: The environment does not contain `Eul |
| 7 | `EulerSourcePotentialCoefficient.instNormedAddCommGroupContinuousLinearMapRealIdSpace` | instance | 9 | `Euler.SourcePotentialTimeCoefficient` | **built** |  |
| 8 | `NavierStokes.HarmonicResidual.BlockRepresentation.pressureField` | theorem | 1 | `NavierStokes.HarmonicResidual` | FAILED (as it should) | line 1424: Invalid field `pressureField`: The environment does not contain `Navie |
| 9 | `NavierStokes.ActualPrimaryCoherence.absoluteCutoff_smooth` | theorem | 6 | `NavierStokes.ActualPrimaryCoherence` | FAILED (as it should) | line 480: Unknown identifier `absoluteCutoff_smooth` |
| 10 | `NavierStokes.HarmonicResidual.band_sub` | theorem | 7 | `NavierStokes.HarmonicResidual` | FAILED (as it should) | line 422: Unknown identifier `band_sub` |
| 11 | `NavierStokes.WeightedQuotients.orderBound` | def | 12 | `NavierStokes.WeightedQuotients` | FAILED (as it should) | line 232: Function expected at |
| 12 | `SmoothTimeField.superposition_taylor_bound` | theorem | 1 | `Euler.SmoothTimeSuperposition` | FAILED (as it should) | line 83: Invalid field `superposition_taylor_bound`: The environment does not c |
| 13 | `NavierStokes.ParametricRephase.familyRate` | def | 10 | `NavierStokes.ParametricRephase` | FAILED (as it should) | line 61: Function expected at |
| 14 | `NavierStokesR3.CompactComparisonBounds.hasCompactSupport_slice` | theorem | 2 | `NavierStokes.R3.CompactComparisonBounds` | FAILED (as it should) | line 48: Unknown identifier `hasCompactSupport_slice` |
| 15 | `EulerParentPacketFrames.Parent.forward_primary_center_term` | theorem | 1 | `Euler.ParentPacketPrimaryCenter` | FAILED (as it should) | line 74: Invalid field `forward_primary_center_term`: The environment does not  |
| 16 | `NavierStokes.LocalSignedRequest.sigma_fiberLocal` | theorem | 1 | `NavierStokes.LocalSignedRequest` | FAILED (as it should) | line 408: Unknown identifier `sigma_fiberLocal` |
| 17 | `NavierStokes.PulseAmplitude.prefixEnergy` | def | 8 | `NavierStokes.PulseAmplitude` | FAILED (as it should) | line 516: Function expected at |
| 18 | `NavierStokes.ParametricKernelBounds.norm_iteratedFDeriv_scalar_snd_le` | theorem | 2 | `NavierStokes.ParametricKernelBounds` | FAILED (as it should) | line 176: Unknown identifier `norm_iteratedFDeriv_scalar_snd_le` |
| 19 | `NavierStokes.ActualParticularStageControls.selected_near` | theorem | 7 | `NavierStokes.ActualParticularStageControls` | FAILED (as it should) | line 468: Unknown identifier `selected_near` |
| 20 | `EulerTransversePacketPrimary.Budget.derivative_bound` | theorem | 1 | `Euler.TransversePacketPrimaryFullBounds` | FAILED (as it should) | line 196: Invalid field `derivative_bound`: The environment does not contain `Eu |

- **Result: 19 of 20 failed, each with an error at a use of the deleted name.** The sample is uniform (seed 20261110) over the 37,070 reachable declarations with at least one user, the headline theorems excluded; each deletion was built alone at the nearest dependent module (157 s in total).
- **The one that built is a private `local instance`** (`NormedAddCommGroup (Space →L[ℝ] ℝ) := inferInstance`, 9 users in its file). Its file comments say such instances "cache" a nested instance; without it type-class search finds the same instance the long way. So "appears in the term" does not imply "needed" for instance shortcuts, and "does not appear" does not imply "unneeded" for `rfl` lemmas: the term graph errs in both directions, by a little.

## Confirmation by compilation

### Stage 2: a seeded sample plus every wholly unreachable module

- **What was deleted.** 300 theorems drawn uniformly from the 12,516 unreachable theorems (270 classified dead, 23 held, 7 elaboration-only), every unreachable declaration that depends on one of them, and all 301 wholly unreachable modules: 4,992 declarations, 302 files (one import hub went with its imports).
- **What was built.** `lake build NavierStokes.ComparatorSolution Euler.Solution`, the import closure of the headline theorems, restoring the declarations named by the errors and rebuilding until green: five builds (1,069, 735, 436, 120 and 34 modules; 33 minutes in all under heavy load).
- **Outcome.** 4,984 of the 4,992 deletions stand; the four headline theorems compile and `#print axioms` gives `propext`, `Classical.choice`, `Quot.sound` for each, as before.

Every deletion that broke the build:

| declaration | what it is | why the build broke | predicted |
|---|---|---|---|
| `NavierStokes.PhysicalGraphBounds.liftXY_apply` | `@[simp] … := rfl` | named in `simp […]` of `liftXY_physicalLift` | yes (`.ilean`) |
| `NavierStokes.FiveRowRank.deltaVLinearMap_apply` | `@[simp] … := rfl` | named in `simpa only […]` in `MeanRankUpdate` | yes |
| `EulerPacketProfileRecursion.zero_highPressure` | `@[simp] … := rfl` | named in `simpa only […]`; a second `simp` in the same file used it unnamed | yes |
| `NavierStokes.StateReindex.cylinder_apply` | `@[simp] … := rfl` | named in `simp only […]` in four reachable proofs | yes |
| `EulerPacketCylinderField.Field.normalized_path` | `@[simp] … := rfl` | named in `simpa only […]` in five reachable proofs (three files failed) | yes |
| `NavierStokes.PhysicalResidualTZ.graphAngularTZ_eq` | `theorem … := rfl`, no attribute | named in `simp […]` in `ActualBaseResidual` | yes |
| `NavierStokes.ActualSignedCoherence.chart_apply` | `@[simp] … := rfl` | named in `simp only […]` | yes |
| `NavierStokes.SlowExpansionResidual.previous_zero` | `@[simp] … := rfl` | a bare `simp` in the reachable `shifted_sum` closes its base case with it; named nowhere | no; held by the `@[simp]` class |
| five `open` commands (`EulerContinuousGramGevrey` twice, `EulerWeightedSobolevEnergy`, `EulerSobolevTimeRegularization`, `EulerSmoothPathJoint`) | namespaces of deleted modules | "unknown namespace"; the whole `open` line is lost, so `Icc` etc. stop resolving | not by the first version of the script; now trimmed automatically |

- **Rates.** Sampled theorems that broke the build: 8 of 300 (2.7%; 95% interval about 1.2% to 5.2%). Among the 270 classified dead: 0 (upper 95% bound about 1.1%). The `.ilean` prediction: 7 predicted, 7 broke, 1 break not predicted.
- **Scaled to the corpus**, 2.7% of 12,516 is about 330 unreachable theorems that elaboration needs. 176 are known by name; the others are among the 594 unreachable `@[simp]` lemmas proved by `rfl`, and are not identified individually.
- **No failure came from an instance, an abbreviation, notation, or a module deletion as such.** Deleting a module replaces `import M` in its importers by M's own imports; 76 files had import lines rewritten and none failed for a missing transitive import.

### Stage 3: everything classified dead

- **Deleted:** 13,625 declarations (11,640 theorems, 1,902 definitions, 80 structures, 3 inductive types) and 233 files; 17 `open` commands trimmed; import lines rewritten in 76 files.
- **Built on the first attempt**: 2,331 modules for the two headline targets (2,682 s wall at load averages of 70 to 190), then the 58 remaining modules of `lake build NavierStokes Euler` (176 s). No errors.
- **Headline theorems:** all four compile; axioms unchanged.
- **Checked from Lean.** The unchanged exporter of `corpora/ns_export` was run on the trimmed build (`trimmed_export/`). It returns 38,880 declarations with the same names as predicted; kind, module, dependencies, statement hash and proof size are identical for every one of them; besides line numbers, 42 declarations (40 reachable) differ in `numAux`/`auxProofSize` (18,689 to 31,196 nodes in all) and one in `extValueByRoot`, because auxiliary definitions they shared with deleted declarations are now generated under them, 37,070 are reachable from the headline theorems as before, and `collectAxioms` gives a file identical to the original `axioms.json`. The remaining proofs elaborate to the same terms up to which declaration owns a shared auxiliary definition. (`trimmed_export/compare.json` is now written by `python3 bench/deadcode.py compare out/corpus/deadcode/trimmed/decls.jsonl out/corpus/deadcode/trimmed_export` and compares every field; the earlier file compared only some and was written by code not in the repository.)
- **What the trimmed corpus no longer contains:** 27 of the 34 root result modules. It proves the four headline theorems and not the paper-form statements (`LocalPaper.local_theorem` and its heat formulas, the appendix results, `H3MaximalLifespan`, most of `Euler.EulerSingularity`). To keep those, keep class c3: 1,365 declarations, 17,716 lines. The unreachable set relative to headline theorems *and* root results is then 14,070 declarations (26.8%). That variant was not compiled.
- **Build time.** There is no clean number. The machine was heavily loaded by other jobs, and the original 1,068 s was recorded the night before under different load. Two estimates in module-seconds (sum of Lake's per-module times; original 16,936):
  - 14,078 (−16.9%): stage-3 times divided by the slowdown measured on the 1,106 rebuilt modules whose text did not change (2.34 by ratio of sums; 1.83 by median, so this normalisation is itself rough);
  - 13,368 (−21.1%): original per-module times scaled by the share of lines kept.
  The deleted files alone account for 1,522 module-seconds (9.0%).

## What a reader of this corpus can safely ignore

1. **To follow any of the four headline theorems, ignore all 15,435 unreachable declarations** (`unreachable.jsonl`, one line each with module, lines, status and class). None is in the dependency closure the kernel checks. The 176 elaboration-only lemmas and the needed `@[simp]` lemmas are restatements of definitions by `rfl`; they carry no mathematical step.
2. **Whole files to skip: 301** (`modules.json`, entries with `unreachable == decls`). 73 of them are imported by nothing; 141 only by the root files; 87 are imported on the way to a headline theorem and contribute nothing to it, the largest being `NavierStokes.MeanResidual` (150 declarations).
3. **All 13 cloned modules** (`…NoOptions`, `…Investigation`; 7,308 lines). No declaration of any clone is used, and nothing imports them.
4. **In live files, expect a quarter to a half of the text to be skippable.** 1,312 files mix used and unused declarations; in 264 of them at least half the declarations are unused. `NavierStokes.CorrectionStep` has 287 unused of 559 (4,925 lines); `Euler.EulerProof` 308 of 1,239.
5. **If the paper-form results matter to you, do not skip class c3** (1,365 declarations). They are unused by the Comparator-checked headline theorems and are the only place the local theorem, the appendix lemmas and the Euler singularity statement in the paper's form are proved.
6. **To delete rather than skip:** the 13,625 classified dead are confirmed by compilation as one set. The 1,634 held ones are probably removable too (1 break in 496 sampled) but each `@[simp] … := rfl` lemma needs the build to say so. The 176 must stay unless the `simp` calls that name them are edited.

## Outline rerun

`bench/outline.py` was run unchanged on the predicted trimmed graph (`trimmed/decls.jsonl`: the original graph minus the deleted declarations, 38,880 declarations) into `outline_trimmed/`, and on the original graph into `outline_control/`, both with `PYTHONHASHSEED=0`.

- **No change on the predicted trimmed graph.** `shape.json`, `relaxations.json`, `outline.json`, `OUTLINE.md` and the four `dominators_*.jsonl` files are byte-identical between the two runs (`outline_fixedseed_compare.txt`). On the graph Lean re-exports from the trimmed build (independent check, `out/corpus/review_maths2/outline_reexport/`), 63 numeric fields of `shape.json` move by at most 0.03 points (total mass +2,588 Navier-Stokes, +9,843 Euler); chapters and reachable counts do not change. Reachable counts, hubs, chapters and mass shares are those of `out/corpus/outline/shape.json`: 23,747 reachable and 61 chapters with 65.0% of mass for Navier–Stokes on ℝ³; 13,108, 54 and 42.1% for Euler.
- **Why:** every statistic of the outline is computed below a headline theorem, and the deletion removes only declarations outside those closures. Dead code makes the corpus a quarter longer; it is not what makes the outline hard to read.
- **A side finding about the outline script:** without a fixed hash seed, two runs on the *same* graph differ in the Louvain clustering section and in about a thousand fields of `outline.json` (set iteration order). `shape.json` and the dominator files are stable. Comparisons of those outputs between runs need `PYTHONHASHSEED` fixed.

## Limits

- **One sample, one corpus.** 300 theorems, seed 20261110. The 2.7% break rate has a wide interval, and the corpus's `simp`-heavy style drives it.
- **Held classes were not deleted in full.** Their status is "not shown dead". The sample estimate (1 of 496) is the only evidence.
- **Definitions, structures and instances were not sampled separately** in stage 2; they were deleted as dependents and in stage 3 (1,985 non-theorems), without failure.
- **The (a)/(b)/(c) split rests on keys and import structure.** It finds copies and orphaned files; it cannot tell whether an unused lemma in a live file was superseded by a differently stated one. The hand reading is by a model proxy and was not blind.
- **"Root result module" is read off the import structure**, not from the papers. A mapping of the papers' numbered results to declarations (the ground-truth task of this track) would make class c3 exact.
- **The trimmed corpus was built, not re-audited.** Comparator was not run on it; the check is that the four theorems elaborate, pass the kernel as part of the build, and print the same axioms.
- **Build time after trimming is estimated**, as stated above.

## Next actions

1. **Time a clean build of the trimmed corpus on a quiet machine**: `cd corpora/ns_trim/work && rm -rf .lake/build && lake build` against the same for a fresh clone of the original. About 20 minutes each.
2. **Settle the held classes**: `python3 bench/deadcode.py plan all`, then apply, build, restore from the errors and repeat. Expect a handful of `@[simp] … := rfl` lemmas to come back; each round rebuilds most of the corpus.
3. **Give the 176 a mechanical fix**: replacing `simp only [foo_apply]` by `simp only [foo]` or `show` would let them be deleted; small, and it removes the gap between the kernel's graph and the elaborator's.
4. **Use the trimmed graph as the default input** for the outline and friction work: same headline closures, a quarter less to load.
5. **Run this report on a software proof development** (plan node M6). The script needs only `decls.jsonl`, the `.ilean` files and the sources.

## Rerun

```sh
export PATH="$HOME/.elan/bin:$PATH"
# working copy (once): sources copied, packages symlinked, build output cloned so Lake replays it
mkdir -p corpora/ns_trim/work/.lake && cd corpora/ns_trim/work
for f in ComparatorChallenges Euler NavierStokes Euler.lean NavierStokes.lean formalization.yaml \
         lake-manifest.json lakefile.toml lean-toolchain LICENSE README.md; do cp -Rp ../../ns/$f .; done
ln -s ../../../ns/.lake/packages .lake/packages
cp -cRp ../../ns/.lake/build .lake/build && cp -Rp ../../ns/.lake/config .lake/config
lake build --no-build NavierStokes.ComparatorSolution Euler.Solution   # must say "All targets up-to-date"
cd ../../..

python3 bench/deadcode.py analyze          # 5 s: analysis.json, modules.json, unreachable.jsonl, sample40.md
python3 bench/deadcode.py tables           # tables.md (the tables of this report)
python3 bench/deadcode.py plan control && python3 bench/deadcode.py control      # 20 builds, about 3 min
python3 bench/deadcode.py plan sample && python3 bench/deadcode.py apply out/corpus/deadcode/plans/sample.json \
    --restore out/corpus/deadcode/restore/stage2.txt && python3 bench/deadcode.py build stage2
python3 bench/deadcode.py plan full && python3 bench/deadcode.py apply out/corpus/deadcode/plans/full.json
python3 bench/deadcode.py build stage3 && python3 bench/deadcode.py build stage3_libs NavierStokes Euler
python3 bench/deadcode.py sizes out/corpus/deadcode/plans/full.json
python3 bench/deadcode.py trimgraph out/corpus/deadcode/plans/full.json out/corpus/deadcode/trimmed/decls.jsonl
PYTHONHASHSEED=0 python3 bench/deadcode.py outline out/corpus/deadcode/trimmed/decls.jsonl out/corpus/deadcode/outline_trimmed
python3 bench/deadcode.py reset            # working copy back to the original sources
```

- `apply` always regenerates the working copy from the pristine `corpora/ns` sources, so plans do not stack. Without `--restore`, stage 2 reproduces the eight declaration failures of the table above over successive builds. The five `open` failures of the first build no longer occur, because trimming dead namespaces from `open` commands is now part of `apply`.
- The first `analyze` reads 2,657 `.ilean` files and caches the reference graph in `ilean_refs.json` (20 MB, git-ignored).
- Attribute cross-check: `corpora/ns_trim/attrs/Attrs.lean` (`LEAN_PATH=$(cat corpora/ns_export/lean_path.txt) lean --run Attrs.lean out/corpus/ns/modules_arg.txt out/corpus/deadcode/attrs.jsonl`, run from that directory).
- Graph of the trimmed build from Lean: `out/corpus/deadcode/trimmed_export/run.sh` (the exporter of `corpora/ns_export`, pointed at the trimmed build).
- Seeds: 20261110 for the control, the sample of 300 and the 40 hand-read items.

## Files

| file | content |
|---|---|
| `analysis.json`, `tables.md` | every number above; the tables |
| `unreachable.jsonl` | the 15,435 unreachable declarations: module, lines, status (dead / held / elaboration-only), tags, class and rule, twin |
| `modules.json` | per module: declarations, unreachable, lines, import status, clone base |
| `elaboration_only.jsonl` | the 176 lemmas named in reachable proofs but absent from their terms, with users and tactic |
| `plans/{control,sample,full,all}.json` | deletion plans; `restore/stage2.txt` the eight restored declarations |
| `control_results.json`, `stage2_summary.json`, `stage3_edits.json`, `build_time.json` | results of the builds; `logs/` raw Lake logs and parsed errors |
| `sample40.md`, `sample40.json`, `hand_sample.json` | the hand-read sample and its labels (model proxy) |
| `attrs.jsonl` | simp / instance / reducibility as the environment has them |
| `trimmed/decls.jsonl`, `outline_trimmed/`, `outline_control/` | trimmed graph (predicted) and the outline reruns |
| `trimmed_export/` | graph and axioms re-exported from the built trimmed corpus, `compare.json` against the prediction |
