# M7: re-invented library abstractions (detector, three projects)

2026-11-10, revised the same evening after an independent review. Tool: `tools/reinvent/` (two Lean programs run read-only against each project's built `.olean` files, plus Python drivers). Per-project reports with every confirmed pair: `ns/REPORT.md`, `carleson/REPORT.md`, `pfr/REPORT.md`; synthetic controls: `planted/REPORT.md`. Library: each project's own pinned Mathlib. No corpus file was modified or rebuilt.

Evidence is the kernel: each "confirmed" pair is a theorem `Reinvent.eqv.<id>` added to the project's environment through the Lean kernel, with no `sorry` and only `propext`, `Classical.choice`, `Quot.sound` (0 exceptions in 127 confirmed statements: 103 in ns, 12 in Carleson, 12 on the synthetic controls). Where this report says a pair "is a re-invention", "is an instance" or "is a coincidence", that is a reading by a model (the agent that built the tool, revised after the review) and is labelled so; it is not evidence. A reviewer restated the 103 ns and 12 Carleson statements, the 3 builder-control statements and 18 derivations as plain Lean theorems outside the tool, and all check with the same axioms (`tools/reinvent/review/kcheck/`). Six ns statements, as printed, do not re-elaborate (c00018, c00040, c00162, c00229, c00275, c00289): the printer drops an implicit argument or a coercion's source type. With that argument written out, each holds.

**These results are exploratory.** The rules were changed after the first full ns run: the rule that drops a library operation was narrowed to norm and absolute value, four heads were added to the list of constants never reported as a notion, and the hidden-constant proof script was written knowing that class exists in this corpus. After the review, three more things changed (which library theorems are exported, how the shown notion is picked, a guard in the statement builder); none changed a verdict. No commit names a frozen rule set (the directory is not under version control), so the plan's rule 1 (frozen before data) is not met.

## Result

- **The known case is found without its name.** `NavierStokes.DiagonalResidual.JetRate` surfaces at stage 1 by the shape rule (its body matches Mathlib's `isBigO_iff` with one extra conjunct `0 ≤ C` and one norm missing) and is confirmed at stage 2: `(∀ x, 0 ≤ q x ^ r) → (JetRate l q f m r ↔ (fun x => iteratedFDeriv ℝ m f x) =O[l] fun x => q x ^ r)`, kernel-checked. 106 theorems are stated about it (2,323 source lines) and 108 theorems use it. The API-copy signal does not find it: 0 of those 106 statements are instances of a library theorem after substitution. The side condition is stronger than needed. A reviewer proved `JetRate → IsBigO` with no condition, and the equivalence under `∀ᶠ x in l, 0 ≤ q x ^ r` (`tools/reinvent/review/misses/JetRate.lean`). Whether the global form holds for the weights the project uses was not checked; a real power of a negative weight can be negative.
- **Controls: the builder's 3 positives are all confirmed; a reviewer's 5 positives give 3, and none of the reviewer's 3 negatives is confirmed.** The builder's three (a copy of `Set.MapsTo` with shuffled arguments, a thin wrapper of `dist`, a hidden-constant bound equal to `IsBigO` under nonnegativity) were written by the builder and are all positive. The reviewer's (another author, written after reading the matcher, so not blind) are now part of the control file: `Monotone`, `Function.Injective` and `IsLittleO` written out are found; ε–N convergence (`Tendsto … atTop (𝓝 a)`) and a Lipschitz bound written with `|·|` get no candidate. Of the negatives, an extra conjunct gives "implication only", a near-miss gives no candidate, and a hidden constant against a bound that is never nonnegative is "not proved". That last one was rejected only because no portfolio entry closed it: the side-condition statement the tool tried is provable in one line (the side condition is false), and nothing checks that a side condition can hold. Two formulas with no shared meaning (`80 * n + 1`, a swapped pair) are confirmed, as the next bullet predicts. Of 5 planted lemma copies, 3 map to their library lemma and all 3 are re-derived from it in Lean; 2 are missed (one whose statement differs by a commuted sum, one copy of `Set.MapsTo.mono_left`).
- **A kernel-checked equivalence is not yet a re-invention.** In the machine project 90 definitions are confirmed equal to a library term. Two facts are mechanical. First, 4 are aliases defined directly from the library notion (`projection`, `coordinate` and `component` := `EuclideanSpace.proj i`; `ValidBandGluing.domain` := `⋃ i, U i`); this is use of the library, not re-invention. Second, 3 are defined from another confirmed project definition and are found only by unfolding it (`SignedMeanGain.Geometry.domain`, `ActualCarrierTransportBase.domain`, `LocalPaperDomain.residualBand`), so 87 distinct notions are confirmed. Of the 103 statements, 92 close by `rfl` and 10 by `simp` with the definitions and at most one library characterisation lemma; only `JetRate` needs an argument. Read by a model (not evidence), the other 86 definitions are: 16 that rebuild a library notion by writing out its definition (`inl`/`inr` 7, `NormedSpace.normalize` 2, `discrim` 2, `deriv`, `Real.logb`, `Prod.swap`, `LinearIsometryEquiv.prodComm`, and `JetRate` through a proof); 40 that are a specific object built with a general combinator (`Set.preimage` 12, `dotProduct` 11, `cond` 6, `Function.support`, `List.Forall`, and `x ^ (1/2 : ℝ)` against `√x`, read the same way for `bandScale` and `radialLength`); and 30 coincidences where the library definition unfolds to a small formula or a pair that the project term equals by `rfl` (`TrivSqZeroExt.inr`, `GenContFract.nextDen`, `Order.succ` on ℕ, and `GradientTensor`, which is defined from `PiLp`). So proof removes the false resemblances (183 of 290 candidates do not even type-check) but does not separate meaning from definitional accident.
- **Measured duplication is small in ns.** Across the 90 confirmed definitions (87 distinct notions), 1,857 project theorems mention one of them in the statement; 20 of those statements (60 source lines) match a library theorem after substitution, and 15 of the 20 were re-derived in Lean from that library theorem through the equivalence. The 5 that were not are matches to `isOpen_induced` (4) and `isClosed_induced` (1), a wrong library lemma chosen because the comparison erases types. So 15 theorems are shown to be copies; the other 1,842 are not shown to duplicate anything by this method. The first version of the tool left library lemmas about `Set.preimage` out of the comparison; with them in, the 4 `isOpen_induced` matches are the only change in ns and Carleson still has none. Theorems about notions the detector missed are not counted (see `extendPath` below).
- **A large re-invention was missed.** In a seeded sample of 5 rejected ns definitions a reviewer found `EulerVolterraConvolution.extendPath`, which equals Mathlib's `Set.IccExtend` by `rfl` and is used by 798 theorems, more than any confirmed definition. The detector missed it because the library body is written without its last argument (`f ∘ projIcc a b h`).
- **Human projects: Carleson 12 confirmed, all one family; PFR none.** Carleson's 12 are the annulus sets (`Set.Annulus.oo` and 11 siblings), each `rfl`-equal to a preimage of an interval under `dist` (6) or `edist` (6); read by a model as instances of a combinator, not re-inventions. PFR has no confirmed pair, but 4 PFR declarations (2 definitions, 2 theorems) carry the full name of a declaration in a Mathlib module PFR does not import.
- **The second API signal, with no candidate pair to start from, did not discriminate.** Matching Prop-level statement signatures with one predicate replaced by a hole proposes 6,850 pairs in ns and 56 in Carleson; none coincides with a shape or wrapper candidate and none is confirmed.

## What was built

| stage | rule | implemented as |
|---|---|---|
| export | skeletons | `Export.lean` writes each definition body, structure (fields as nested `∃`/`∧`) and theorem statement as an s-expression with instances, proofs and implicit types erased, `>`/`≥`/`≠` normalised, project-local reducible definitions unfolded (and one further level of project definitions as a second attempt). Library theorems `L xs ↔ R` or `L xs = R` whose value arguments are distinct variables give extra bodies for `L`. |
| 1 S | shape | Second-order pattern matching of each library body (its parameters are the pattern variables) against each project body: Miller patterns (a parameter applied to distinct bound variables binds to a lambda; other applied parameters are checked afterwards), up to bound names, argument order and currying of `L`, erased arguments and order of conjuncts. Two approximate rules, both recorded per candidate: extra conjuncts in the project body; a norm or absolute value in the library body with no counterpart (gives the side condition `0 ≤ t`). No anti-unification. Kept when the pattern has ≥ 3 rigid symbols, ≥ 40% of the project body's, and extra conjuncts ≤ 34% of it; best 3 library notions per definition. |
| 1 W | thin wrapper | `def`/`abbrev` with ≤ 15 nodes over library constants only. `alias` when the body is one library constant applied to the parameters (sent to stage 2; by construction this is use of the library); otherwise `composite` (counted only). |
| 1c | API copy | (a) For a candidate pair, each project theorem mentioning D is rewritten with the library term and counted when some library theorem mentioning L matches its conclusion as a pattern and each library hypothesis matches a project hypothesis. (b) With no pair: holed statement signatures (above). |
| 2 | proof | `Confirm.lean`: the statement is built from D's own type in the environment and the candidate's library term (rejected if that term mentions D), then a fixed portfolio is tried in order: `rfl`/`Iff.rfl`; `simp only` with the definitions; the same then `rfl`; `simp`; `ext`; `constructor` + `simp_all`; `cases`; `exact?`; `aesop`; and one script for hidden constants (a sign condition on `∃ C` is redundant when the bound is monotone in `C`). With side conditions if the match has any; `D → L` if it had extra conjuncts. Heartbeat limit per entry. Refutation is attempted only as `simp` on the negation. |
| 3 | cost | Theorems about D, the mapped ones, their source lines and proof sizes (from the earlier corpus export, itself from Lean), theorems using D, and a seeded sample (≤ 5 per definition, seed 20261110) of mapped theorems re-proved by rewriting with the equivalence and applying the library theorem; a derivation counts only if the kernel-checked proof term uses the library theorem and not the project theorem. When several library notions are confirmed for one definition, the one shown has the most mapped theorems, then is proved outright, then is a shape match rather than an alias, then has the fewest approximations, the heaviest pattern and the smallest library term. |

One command per project: `tools/reinvent/run.sh <ns|carleson|pfr>`; the controls: `tools/reinvent/planted.sh`. Both were run end to end for this revision and the figures below are from those runs.

## Funnel

| | ns (machine) | Carleson (human) | PFR (human) |
|---|---|---|---|
| project theorems (corpus export) | 38,601 | 2,675 | 978 |
| definitions and structures in the environment | 12,891 | 476 | 135 |
| after removing syntax and metaprogramming definitions | 12,891 | 451 | 81 |
| Prop-valued | 646 | 34 | 14 |
| skipped (index keys not enumerated in 2 s; large structures) | 29 | 0 | 0 |
| 1 S: definitions with a shape candidate | 208 | 14 | 2 |
| 1 S: pairs (same shape / instance / approximate) | 284 (26 / 251 / 7) | 14 (0 / 14 / 0) | 3 (0 / 3 / 0) |
| 1 W: thin wrappers (alias / composite) | 6 / 339 | 0 / 65 | 0 / 2 |
| pairs sent to stage 2 (definitions) | 290 (214) | 14 (14) | 3 (2) |
| 2: statement does not type-check | 183 | 2 | 3 |
| 2: proved | 102 | 12 | 0 |
| 2: proved under a side condition | 1 | 0 | 0 |
| 2: not proved (type-checks) / refuted | 4 / 0 | 0 / 0 | 0 / 0 |
| 2: definitions with a kernel-checked equivalence | 90 (0.70% of definitions; 87 not counting 3 defined from another confirmed definition) | 12 (2.7%) | 0 |
| 2: of those, aliases (the library constant applied to the definition's parameters) | 4 | 0 | 0 |
| 1c (a): pairs with ≥ 1 mapped theorem (all confirmed) | 15 | 0 | 0 |
| 1c (b): pairs from holed signatures (also a stage-1 candidate) | 6,850 (0) | 56 (0) | 0 (0) |
| 3: theorems whose statement mentions a confirmed definition | 1,857 (27,857 lines) | 220 (1,157 lines) | — |
| 3: of those, matching a library theorem after substitution | 20 (60 lines, proof size 5,144) | 0 | — |
| 3: sampled and re-derived from the library theorem | 15 of 20 | — | — |
| 3: uses of confirmed definitions by theorems (summed per definition) | 2,826 | 264 | — |
| declarations sharing a full name with un-imported Mathlib | 0 | 0 | 4 |

Portfolio entry that closed the 103 ns statements: `rfl` 92, `simp only` 9, `simp` 1, constant-sign 1. Carleson: `rfl` 12. The "skipped" row is a wall-clock limit, so it varies with machine load: 42 in the first run, 29 in this one; the candidate list was identical in both.

## Reading of the confirmed pairs (by a model; not evidence)

All confirmed definitions were read, by library notion (`tools/reinvent/reading.json`), and the seeded sample of 15 confirmed pairs per project is in `<project>/reading_sample.json`. "Use of the library" is not a reading: it is every pair found by the alias rule.

| ns, 90 definitions | definitions | theorems about them | lines | matched to library | uses |
|---|---|---|---|---|---|
| read as re-invention (rebuilds a library notion) | 16 | 265 | 4,277 | 11 | 424 |
| use of the library (alias rule; mechanical) | 4 | 27 | 198 | 2 | 151 |
| read as instance of a combinator | 40 | 1,159 | 17,682 | 6 | 1,539 |
| read as coincidence | 30 | 406 | 5,700 | 1 | 712 |

- Seeded sample of 15 confirmed ns pairs: 4 re-invention, 5 instance, 6 coincidence. Precision for "re-invention" by this reading: 16 of 90 over all (18%), 4 of 15 on the sample.
- By rule class: the 4 "alias" definitions are, by construction of the rule, the library constant applied to their own parameters (`def D xs := L xs`), so they are uses of the library, not re-inventions; of the 13 "same shape" definitions 12 are read as re-inventions and 1 (`radialLength`) as an instance; the 72 "instance" definitions split 3 re-invention, 39 instance, 30 coincidence; the 1 "approximate" is `JetRate`. Reporting only same-shape pairs would keep 12 of the 16 and lose `JetRate`, `temporalDerivative` and `discriminant` (two copies).
- Carleson's 12 are all read (by a model) as instances. 10 are defined in `Carleson.ToMathlib.Annulus`, the folder of material written for upstreaming, and 2 in `Carleson.Defs`.
- Seeded sample of 15 rejected ns candidates (builder's, seed 20261110): none read as a missed re-invention; 14 do not type-check (9 on a type or instance mismatch that the erased skeleton cannot see, 5 leave a hole the elaborator cannot fill, of which 4 are library constructors that take a proof argument: `IsLinearMap.mk'`, `Units.mk`), 1 type-checks and was not proved.
- Seeded sample of 5 rejected ns definitions (reviewer's, seed 777): 1 real miss (`centerStrain`, through `extendPath` = `Set.IccExtend`); 2 equal the constructor `IsLinearMap.mk'` (the constructor itself, not a re-invention); 1 whose underlying function equals `ContinuousMap.compRightContinuousMap`, with no linear-map version in this Mathlib; 1 with no library equivalent. Proofs: `tools/reinvent/review/misses/Misses.lean`.
- Read as re-inventions in ns, by library notion: `ContinuousLinearMap.inl`/`inr` (7 separate project definitions), `NormedSpace.normalize` (2), `discrim` (2), `deriv`, `Real.logb`, `Prod.swap`, `LinearIsometryEquiv.prodComm`, `Asymptotics.IsBigO` (aliases of `EuclideanSpace.proj` (3) and `Set.iUnion` (1) are uses, not re-inventions).

## The ten most consequential cases (ns)

Ranked by theorems using the definition. Statements, signatures and derivations are in `ns/REPORT.md`.

| # | project definition | kernel-checked statement | reading (model) | uses | theorems about it (lines) | re-derived from library |
|---|---|---|---|---|---|---|
| 1 | `PhysicalMeanDomain.slowDomain` | `slowDomain U = (fun x => x.2.1) ⁻¹' U` | instance: set-builder notation for a preimage | 646 | 492 (8,765) | 0 (1 wrong match) |
| 2 | `SignedMeanGain.Geometry.domain` | `G.domain = (fun x => x.2.1) ⁻¹' G.region.carrier` | instance; defined as `slowDomain G.region.carrier` (row 1), not a separate finding | 186 | 181 (2,047) | 0 |
| 3 | `GaugeStateCoherence.bandScale` | `bandScale n m = √(dyadicQ n / dyadicQ m)` | instance (`x ^ (1/2 : ℝ)` against `√x`: two library spellings of the same thing) | 128 | 106 (1,729) | 0 |
| 4 | `DiagonalResidual.JetRate` | `(∀ x, 0 ≤ q x ^ r) → (JetRate l q f m r ↔ (fun x => iteratedFDeriv ℝ m f x) =O[l] fun x => q x ^ r)` | re-invention; the only one that is not a definitional equality | 108 | 106 (2,323) | 0 |
| 5 | `EulerParentNeighborThreshold.requiredExponent` | `requiredExponent = Order.succ (80 * degree)` | coincidence | 106 | 107 (695) | 0 |
| 6 | `EulerPacketNormalizedPrimary.unit` | `unit x = NormedSpace.normalize x` | re-invention (the library definition written out; `rfl`) | 97 | 71 (724) | 1 |
| 7 | `EulerMeanGradientTest.GradientTensor` | `GradientTensor = EuclideanSpace (↥L2) (Fin 3)` | coincidence: defined as `PiLp 2 (fun _ => L2)`; `EuclideanSpace` is the scalar-field abbreviation of `PiLp`, here applied to a Hilbert space | 95 | 0 | 0 |
| 8 | `AxisymmetricFields.projection` | `projection i = EuclideanSpace.proj i` | use of the library: defined as `EuclideanSpace.proj i` (alias rule) | 86 | 2 (11) | 0 |
| 9 | `PhysicalResidualBridge.ScaledGraph.angular` | `angular _x = TrivSqZeroExt.inr 1` | coincidence | 84 | 57 (1,213) | 0 |
| 10 | `ProblemStatement.temporalDerivative` | `temporalDerivative u t x = deriv (fun s => u (s, x)) t` | re-invention (the library definition written out; `rfl`) | 80 | 34 (494) | 1 |

So among the ten most used, one (`JetRate`) is a non-definitional equivalence with a library notion the project rebuilt, and two (`unit`, `temporalDerivative`) are small re-implementations closed by `rfl`. The ten most used among those read as re-inventions add `PrimaryRepresentatives.normalDirection` (= `NormedSpace.normalize`, 49 uses, 3 of 29 theorems re-derived from `norm_normalize`, `normalize_smul_of_pos`, `norm_smul_normalize`), `HarmonicWaveInteraction.inclusion` and `SignedWaveUpdate.zeroSection` (= `ContinuousLinearMap.inl`), `supportLabel` (= `Prod.swap`), `ChartScales.rho` (= `Real.logb Tg Lambda`) and two copies of `discriminant` (= `discrim`).

## Machine and human projects, side by side

- Confirmed definitions per 100 definitions examined: ns 0.70, Carleson 2.7, PFR 0. Carleson's figure is one family of 12 sets.
- Definitions read (model) as rebuilding a library notion: ns 16, Carleson 0, PFR 0, plus 4 ns aliases defined directly from the library notion. ns repeats the same notion in separate modules (seven `inl`/`inr`, two `normalize`, two `discrim`, three aliases of `EuclideanSpace.proj`, and two copies of the missed `Set.IccExtend`); neither human project shows that pattern among its confirmed pairs.
- Thin composites over library constants (not confirmed, counted): ns 339 of 12,891 (2.6%), Carleson 65 of 451 (14%), PFR 2 of 81.
- Hidden-constant predicates: of ns's 646 Prop-valued definitions, 79 contain `∃ C : ℝ` in the exported body (the census, by its own rule, counted 114 of 669); 1 is confirmed equal to a library notion. The human projects have no candidate of this kind.
- Name clashes with un-imported Mathlib: PFR 4 (`MeasureTheory.Measure.support`, `ProbabilityTheory.CondIndepFun`, `condIndepFun_iff`, `IdentDistrib.prodMk`), Carleson 0, ns 0. Only the names were compared; equivalence was not checked.
- The projects differ in size by a factor of 14 to 40 and in subject, so these are counts, not rates of a behaviour. Nothing here generalises beyond these three projects.

## What the detector cannot see

- **Library definitions written point-free.** A library body `f ∘ g` is not matched against a project body applied to one more argument. Missed this way: `EulerVolterraConvolution.extendPath T hT f t := f (projIcc 0 T hT t)`, which is `Set.IccExtend hT f t` by `rfl` and is used by 798 theorems, more than any confirmed definition. A second copy, `NavierStokes.NilpotentVolterra.extendPath`, is used by 17. 45 library definitions in the ns environment have a point-free body. Found by a reviewer in a seeded sample of 5 rejected definitions (seed 777); the builder's sample of 15 found none.
- **Notions the library states differently.** Only bodies with the same shape as a library definition or a library `↔`/`=` characterisation with variable arguments are matched. A bound `∃ C, ∀ x ∈ S, ‖f x‖ ≤ C * g x` equals `f =O[𝓟 S] g` only through `isBigO_principal`, whose left side has a non-variable argument, so it is not a pattern. The other two big-O re-inventions named in `LESSSIM.md` are of this kind or are lemmas, not definitions; neither is found. The reviewer's controls add two more of this kind: ε–N convergence and a Lipschitz bound with a real constant.
- **Generalisations, specialisations and compounds.** Most hidden-constant predicates in ns hide a constant and an exponent (`∃ C N, … ≤ C * (1 + r) ^ N`), which is `∃ N, IsBigO …`, not one library notion. Extra conjuncts are allowed only up to a third of the body; `D → L` was proved for no pair in the three projects.
- **Types.** Skeletons erase types and instances, so 63% of ns candidates fail to type-check at stage 2, and the best-3 cut is taken before that check; a correct pair ranked fourth is lost. The same erasure produces the 5 wrong lemma matches at stage 1c.
- **Proof arguments.** A library term that needs a proof argument cannot be written back; such candidates end as "does not type-check".
- **Satisfiability of side conditions.** It is not checked. A statement whose side condition can never hold would be reported "proved under side condition" if a portfolio entry closed it. The side conditions the tool states are also global where an eventual one would do (`JetRate`).
- **Which library notion is shown.** When several library notions are confirmed for one definition, one is shown. In a reviewer's control, `Function.Injective` written out was first reported as `Function.FactorsThrough`; the selection rule now prefers the smaller library term and shows `Function.Injective`, but a coincidental notion with a heavier pattern can still be shown in place of the right one.
- **Definitions built from other project definitions.** They are found again by one-level unfolding (3 of 90 in ns); the report now marks them.
- **Library modules the project does not import**, beyond the name-clash check, and **notions absent from the library**.
- **Large structures**: 29 to 42 ns structures with many fields were skipped, depending on load; structures are otherwise compared only as a conjunction of fields.
- **Duplicated lemmas whose hypotheses differ.** A project theorem counts as a copy only if every library hypothesis appears among its own; a copy that needs a side fact proved (as `JetRate.add` needs `iteratedFDeriv_add`) is not counted, so 15 is a lower bound.
- **Refutation.** No counterexample search exists; "not proved" means the portfolio failed.
- **Meaning.** `rfl`-equality with a library definition that is itself a small formula is reported as confirmed, and so is a project definition written as the library constant applied to its parameters (alias rule), which is use of the library.
