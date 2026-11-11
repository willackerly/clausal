# M9 families: triage, and seven families taken through Lean

2026-11-11. Corpus: `corpora/ns` (Lean 4.34.0-rc2), read-only; nothing in it was modified or rebuilt. Work: `corpora/families/`, results: `out/families/`. The clustering this starts from is `out/families/ns/CLUSTERS.md`.

**What is evidence here.** Every primitive, every "member is an instance" statement, every re-derived lemma and every counterexample is kernel-checked against the built corpus, with no `sorry` and axioms `Classical.choice`, `Quot.sound`, `propext` only. Sizes, instance counts and heartbeats are measured on the elaborated terms. The triage (section 1) and every sentence marked *reading* are a model's reading and are not evidence. Each re-derived proof's transitive dependencies were checked for the corpus lemma it replaces: 67 of 68 are non-circular; `MemClass.band_smul` is circular and is excluded from every total. The node is **exploratory**: the triage and the family list were frozen before any Lean, but the measuring tools were written while looking at results. One independent agent has reviewed it (section 10); this version applies its corrections and reruns what they affect.

## Result

1. **Each of the seven chosen families has a kernel-checked common form, and in four of them it was already in the project or in Mathlib.** For three families the primitive is a definition the corpus already has (`LocalClass`, `MemClass`, the vector-valued `translation`); for the 15-predicate family it is Mathlib's `AddSubgroup`; three got a new definition (`dirDeriv`, `JetRateOn`, one shared exponent), and for `dirDeriv` the review showed that no new definition does as well (Mathlib's `fderiv` written directly). No generalisation was false, but that tests little: only two genuinely new parameterised statements were attempted. Two members are instances only under a hypothesis they do not carry (`LocalJets` and `NativeJets`: a nonnegative weight), each with a kernel-checked counterexample.
2. **Concept count, on the seven families: 52 distinct definitions → 25, and 110 lemma statements → 72 in the library.** `MemClass` is counted once; `LocalJets` stays, because it is an instance only under a hypothesis it lacks and two of its laws do not transfer. The number of statements a downstream user cites goes 110 → 32, but 40 of that difference is the 15-predicate family, whose 40 `zero`/`add`/`neg` proofs remain as the fields of its 15 subgroup declarations. 67 member lemmas were re-derived from the primitive's API with their corpus statements unchanged (68 attempted, 68 compile, 1 is circular and not counted). A merged primitive also carries more parameters than a member: `LocalClass` has five explicit parameters and an index type against `MemClass`'s four, and `dirDeriv` adds a direction and four instance arguments.
3. **Proof size: one family pays for all the others.** Over 67 re-derived lemmas, proofs go from 71,753 to 14,932 elaborated nodes (-79%) and from 471 to 232 source lines, against 16,257 nodes and 241 lines of new library: net 40,564 nodes saved and 2 source lines added. A 68th, `MemClass.band_smul`, compiles but is circular (the corpus proves `LocalClass.band_smul` from `MemClass.band_smul`), so it is not counted. `MemClass`/`UniformClass`/`LocalClass`/`LocalJets` alone gives 52,179 → 9,290 over 27 lemmas for 2,844 nodes of bridging lemmas (net 40,045, 99% of the net saving), because the corpus proved the same laws up to four times. The other six families together net +519 nodes: break-even, which is what the earlier constant-threading experiment found.
4. **Elaboration cost: cheaper proofs, dearer in total once the new library is charged.** Re-derived proofs fill 83% fewer instance-argument slots (25,298 → 4,238), or 64% fewer with the new library's 4,962 slots charged. Heartbeats (Lean's deterministic work counter) in the proofs themselves fall 18% (42,154 → 34,752) over the 63 lemmas whose corpus proof replays in a scratch file and whose re-derivation is not circular. Charging the new library's own elaboration, as its nodes are charged, the total **rises**: +12% (47,271) counting only the declarations the re-derived proofs depend on, +31% (55,314) counting every new declaration that is charged in nodes. F00079 is 19,905 → 9,802 (-51%) with its bridges charged; the other six families together go 22,249 → 45,512 (+105%; +69% on the narrower count). Two specific costs: in the family that goes through a bundled interface (`AddSubgroup`), 11 of the fifteen `sub` lemmas are cheaper, 3 are 6 to 16 heartbeats dearer, and **one costs 16× more** (912 → 15,040, a relation on a pair of coefficient families, where Lean has to see through a product of two group structures). And a polymorphic primitive makes statements larger: restating 50 theorems about the directional derivative against `dirDeriv` grows their statements by +27% in elaborated nodes, all of it type and instance arguments the local names had hidden.
5. **Downstream, about half of the proofs never look inside the definition they use.** Of 1,317 sampled theorems that use a member, 661 (50%) are kernel-checked to be generic in it: they would go through unchanged for any primitive with the same lemmas. The share is 75% for `MemClass` and its named weights and 28% for the exponent, whose users unfold it and do arithmetic. In the five families where a restatement tool was run, every sampled downstream statement that mentions a replaceable member was restated against the primitive and kernel-checked (46 of 46: 40 with the original proof accepted as it stands, 6 across a proved equation). The 40 are in the four families whose members equal the primitive by `rfl`, so they follow from the instance lemma by unfolding and check the tool, not the generalisation; the informative cases are the 6. And the interface the generic proofs are generic over is large: 52 to 258 distinct lemmas per family.
6. **The cheapest concept reduction needs no abstraction at all.** 408 type abbreviations in 19 families are the first member of their family by `rfl` (389 of 389 checked): 389 names can go with no proof touched.

The trade is stated at the end.

## 1. Triage of the 60 top clusters

**This table is a model's reading, not evidence.** It was written to `out/families/TRIAGE_2026-11-11.md` before any generalisation was attempted, from each cluster's member bodies, types and side-by-side lemma blocks, and has not been edited since. Classes: **(a)** one idea, several instances; **(a0)** one *type* under several local names (one idea, but no hole and no lemma API: deduplication only, added by me, see `DECISIONS.md`); **(b)** parallel by construction, different mathematics; **(c)** accidental resemblance; **(d)** a library notion under a local name.

Counts: (a) 8, (a0) 20, (b) 19, (c) 9, (d) 4.

| # | id | class | members | users | first member | reason (reading) |
|---:|---|---|---:|---:|---|---|
| 1 | F00001 | (a0) | 75 | 3,169 | `ActualBaseResidual.Point` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 2 | F00002 | (a0) | 60 | 8,117 | `ActualCarrierTransportBase.Plane` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 3 | F00003 | (a0) | 52 | 3,004 | `ActualCarrierGeometry.Slow` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 4 | F00005 | (a0) | 41 | 1,409 | `ActualBaseResidual.Full` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 5 | F00006 | (a0) | 28 | 12,066 | `EulerLiftedGradientSpace.Vector3` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 6 | F00007 | (a0) | 18 | 993 | `ActualCarrierTransportBase.Index` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 7 | F00010 | (c) | 22 | 369 | `EulerAllOrderDriftCorrection.Budget.solution` | Each member is `Classical.choose` of a different existence proof; only the head matches. |
| 8 | F00011 | (a0) | 35 | 1,674 | `ActivationContinuation.FieldJet` | `Fin n → ℝ` for six values of n under 35 names; the 'parameter' is the library's own (`Fin n`), so this is renaming, not a new primitive. |
| 9 | F00014 | (b) | 36 | 132 | `EulerMeanPacketProvider.Forcing.pressureGradientCylinderField` | 36 fields each built by transporting a different field along an equality with `Field.congr`; shared constructor, different objects. |
| 10 | F00015 | (a) | 15 | 906 | `ActualCyclePeriodicity.CoefficientsTranslation` | 15 predicates on (sequences of) fields with different bodies and the same closure laws (`add`, `sub`, `neg`, `smul`, some `mul`): one idea, 'a linear subspace of fields', needing an interface rather than a parameter. Whether all 15 really satisfy the same laws is unchecked. |
| 11 | F00016 | (c) | 20 | 938 | `EulerBaseDatum.FirstScaleGuards.packet` | `Classical.choice` of different nonemptiness proofs; only the head matches. |
| 12 | F00019 | (a) | 7 | 828 | `CoordinateAlgebra.A` | The exponent `1/2 + h` defined seven times in seven modules, verbatim; a project quantity with its own lemmas, so one definition is natural. |
| 13 | F00023 | (a0) | 6 | 1,031 | `CorrectionState.ScalarField` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 14 | F00026 | (b) | 3 | 198 | `EulerPacketCylinderField.joinedSourceProfiles` | Profiles of the forward and of the joined packet problem, both built with the existing recursion `profiles`; the two problems have different solve operators and different proofs. |
| 15 | F00027 | (a0) | 13 | 713 | `ActualCopySliceRegularity.Label` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 16 | F00028 | (b) | 18 | 272 | `EulerCylinderPotential.potentialField` | 18 fields each the point evaluation (`pointField`) of a different path; shared evaluator, different objects. |
| 17 | F00029 | (a0) | 15 | 1,686 | `ActualPeriodizedSignedRealization.Frequency` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 18 | F00030 | (b) | 2 | 257 | `EulerPacketCylinderField.joinedSourceOperators` | Two operator records (forward, joined) that differ in the high-frequency solve operator; a parameter would fit the record, but every lemma about it needs facts of the particular solver. |
| 19 | F00031 | (a0) | 15 | 349 | `ActualCandidateConstruction.Index` | One index type family `ℕ → ℕ → Type` re-exported as `abbrev` in 15 modules; verbatim, no hole. |
| 20 | F00035 | (c) | 3 | 4,680 | `OutgoingProfile.Profile` | Three unrelated parameter records joined because their lemmas have similar shapes; nested data, not instances of one thing. |
| 21 | F00036 | (a0) | 5 | 127 | `ActualMeanPhysicalData.Scalar` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 22 | F00037 | (a0) | 13 | 629 | `ActualParticularRealization.Associated` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 23 | F00038 | (a0) | 13 | 170 | `ActualPeriodizedSignedRealization.Mat2` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 24 | F00039 | (a0) | 13 | 447 | `BasePhaseGeometry.Plane` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 25 | F00040 | (b) | 7 | 141 | `EulerElapsedTimePathGluing.join` | Seven paths each glued from a different past and future piece with the existing `join`. |
| 26 | F00041 | (b) | 8 | 94 | `FiveRowRank.deltaV` | Seven uses of the existing `repair` with different moments and debts. |
| 27 | F00042 | (a) | 18 | 652 | `EulerMeanVectorIdentities.vectorPartial` | The derivative of a function along a fixed vector, under 18 names in 14 modules; one hole (the direction) and one (the domain). One definition with the direction as a parameter. Close to (d): the body is the library's `fderiv` applied to a vector. |
| 28 | F00043 | (c) | 35 | 99 | `EulerContinuousBoundedTensor.tensorPathLinear` | 35 functions each bundled as a `LinearMap`; the shared skeleton is the structure constructor. |
| 29 | F00044 | (c) | 9 | 336 | `EulerOrdinarySobolev.FiniteLifespan.evolution` | `Exists.choose` of different proofs; only the head matches. |
| 30 | F00045 | (b) | 9 | 224 | `EulerPacketInitial.high` | Eight finite sums `fieldSum (N+1) κ u` of different coefficient families. |
| 31 | F00046 | (a) | 5 | 453 | `CurrentSignedCurl.AmplitudeBound` | `MemClass` at four weights (`MeanClass`, `UnweightedClass`, `WaveClass`, `AmplitudeBound`): the parameterised primitive already exists in the corpus and the instances are named; the question is whether the lemmas are restated per instance. |
| 32 | F00049 | (a0) | 9 | 1,408 | `GlobalSlowProfiles.Field` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 33 | F00050 | (c) | 30 | 448 | `EulerBoundedFieldCalculus.pathCompositionMap` | 30 compositions of two continuous linear maps; the shared skeleton is `comp`. |
| 34 | F00052 | (b) | 4 | 98 | `EulerPacketCoordinates.coordinateData` | Three correction-data records built by one constructor from different fields. |
| 35 | F00053 | (d) | 9 | 152 | `EulerPacketCylinderField.Field.changeTime` | Nine casts along `T = T'` (`h ▸ x`) for nine dependent types: the library's transport, named per type. |
| 36 | F00054 | (a0) | 9 | 1,924 | `ActualBaseResidual.SpaceTime` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 37 | F00055 | (a0) | 10 | 330 | `ActualCurrentCarrierJets.Native` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 38 | F00058 | (b) | 11 | 95 | `EulerPacketFiveCost.costConstant` | Ten constants, each `coefficientCost` of a different polynomial. |
| 39 | F00060 | (d) | 13 | 132 | `EulerBoundedFieldCalculus.pathAdjointMap` | 13 operators lifted to paths, each `ContinuousLinearMap.compLeftContinuous ℝ K L` for a different L: the library notion with a local name. |
| 40 | F00061 | (a) | 3 | 133 | `ActualInitialCoherence.pieces` | One definition (`primaryPiece`) repeated verbatim in three modules, with five parallel lemmas. |
| 41 | F00062 | (b) | 16 | 53 | `ActualIntermediateDebtBounds.postSigned` | 16 abbreviations `x ↦ params.method x.coefficients ctx x.state` for 13 different methods; local shorthand. |
| 42 | F00064 | (a) | 5 | 67 | `DefectIncrementBounds.axialQuadratic` | The quadratic increment `2•(b·m) + m·m` written once per component (axial, radial, angular); one hole, the component. |
| 43 | F00066 | (c) | 14 | 69 | `EulerContinuousBoundedTensor.tensorPathMap` | 14 linear maps each bundled as a continuous linear map; the shared skeleton is the constructor. |
| 44 | F00067 | (b) | 13 | 278 | `ActualMeanPotentialRealization.componentPotential` | 13 vectors built from three components with `pack`; chart map, real part, velocity are different objects. |
| 45 | F00068 | (c) | 13 | 560 | `EulerBaseDatum.firstFrequencyPower` | 13 constants that happen to be a product of two things. |
| 46 | F00071 | (d) | 6 | 396 | `EulerCylinderPathProduct.basisVector` | `EuclideanSpace.single i 1` under six names: the library's standard basis vector. |
| 47 | F00072 | (b) | 10 | 134 | `EulerLpTranslation.SmoothL2Field.directionalField` | Nine fields, each `mapField L A` for a different operator L. |
| 48 | F00073 | (a) | 2 | 157 | `EulerLpTranslation.translation` | Translation on L² written twice, once for vector-valued and once for ℝ³-valued fields; the second looks like the first at one type. |
| 49 | F00074 | (b) | 12 | 156 | `ActualCyclePreservation.primaryField` | Eleven sums over labels of different oscillation blocks with the existing `fieldSum`. |
| 50 | F00075 | (b) | 8 | 243 | `ActualInitialMean.primary` | Seven states rebuilt with `reconstructState` from different increments. |
| 51 | F00077 | (a0) | 8 | 367 | `ActualSignedNativeProfiles.LiftPoint` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 52 | F00078 | (a0) | 5 | 1,201 | `CorrectionState.Lift` | One type written out again under local names (transparent `abbrev`); no hole and no lemma API of its own, so there is nothing to parameterise: deduplicate. |
| 53 | F00079 | (a) | 4 | 453 | `LabelSumBounds.UniformClass` | Four jet-bound predicates with a hidden constant that differ by an extra index and by a localising set (`MemClass`, `UniformClass`, `LocalClass`, `LocalJets`): one idea with two optional features. |
| 54 | F00080 | (b) | 6 | 151 | `OutgoingHistories.I` | Five moment histories (mass, energy, pressure, transport, angular), each `history initial weight`; the general form exists and the five are different quantities. |
| 55 | F00084 | (b) | 14 | 242 | `EulerMeanPacketProvider.Forcing.toCylinderField` | The field algebra (`add`, `smul`, `zero`, `map`, …) each built with `ofLifted`; the members ARE the API of one structure, not copies of one definition. |
| 56 | F00085 | (b) | 7 | 82 | `EulerPacketInitialAmplitude.degree` | Seven degrees, each `natDegree` of a different polynomial. |
| 57 | F00089 | (c) | 22 | 1,768 | `ActualCycleCoherence.geometry` | 22 unrelated one-line aliases (each renames a different definition); each alias is removable, but there is no common idea. |
| 58 | F00091 | (b) | 4 | 67 | `EulerCylinderDirichlet.Coefficients.frame` | Four fields of one record pushed through one map; four different coefficients. |
| 59 | F00092 | (d) | 4 | 84 | `EulerMeanHarmonic.innerCutoff` | Four cutoffs, each the coercion of a different `ContDiffBump`; the library object under a name. |
| 60 | F00095 | (b) | 11 | 118 | `EulerPacketCylinderField.Field.changeTime` | Ten fields each cast in time with `changeTime`; different fields. |

**Chosen by rule** (top 6 of class (a) by number of users, plus the positive controls): F00015, F00019, F00042, F00046, F00079, F00073, F02076. F00046 and F00079 are also the constant-hiding control; F02076 is the big-O control and was added by the rule (it is rank 2,076 of the clustering, not in the top 60). Class (a) and not chosen: F00061, F00064.

*How the reading held up (measured afterwards).* All seven chosen families did have one idea behind them. Two readings were off: F00015 was read as possibly "one interface", and it is one, but the interface is the library's (`AddSubgroup`), so it could equally have been classed (d); and for F00079, F00046 and F00073 the "parameterised primitive" was already a corpus definition, which the reading anticipated only for F00046.

*A second model reading.* The reviewing agent re-classified 20 of the 60 (seed 4242). It was **not blind**: the reviewer had read the table above first, so agreement is probably inflated. It agreed on 17 of 20 (κ ≈ 0.80); 12 of 15 when the type clusters, which nobody would dispute, are left out. The three disagreements: F00015 is (d) or (b), since the shared notion is the library's `AddSubgroup` and the members are different subspaces; F00042 is (d), Mathlib's `fderiv` applied to a vector; F00030 is (a), one operator record with the solve operator as a parameter, 257 users. On the second reading two of the seven measured families would not have been chosen, and one family that was not measured would have been. The measurements side with the second reading on both: F00015 saved nothing, and F00042 does as well with no new definition (section 2).

## 2. The seven families, before and after

| family | members | primitive, and its form | members are instances | re-derived lemmas | proof nodes | new library nodes | net nodes |
|---|---:|---|---|---:|---|---:|---:|
| F00015 15 predicates with the same closure laws | 15 | Mathlib `AddSubgroup` (bundled structure); one instance per member | 15 of 15 are subgroups; 1 only under a hypothesis on its weight | 15 | 3,207 → 1,402 | 1,717 | +88 |
| F00019 the exponent `1/2 + h` | 7 | one definition, no parameter | 7 of 7 by `rfl` | 0 | 0 → 0 | 121 | -121 |
| F00042 derivative along a fixed vector | 18 | new definition `dirDeriv v f x`, direction explicit, spaces as type parameters | 18 of 18 by `rfl` | 13 | 4,405 → 1,811 | 3,675 | -1,081 |
| F00046 `MemClass` at named weights | 5 | existing corpus definition `MemClass` (weight is already a parameter) | 4 of 4 by `rfl` | 2 | 580 → 174 | 222 | +184 |
| F00079 `MemClass` / `UniformClass` / `LocalClass` / `LocalJets` | 4 | existing corpus structure `LocalClass` (index and localising sets as parameters) | 2 of 3 by `↔`; `LocalJets` only with weight ≥ 0 | 27 | 52,179 → 9,290 | 2,844 | +40,045 |
| F00073 translation on L² | 2 | existing corpus definition `EulerLpTranslation.translation` (value space as type parameter) | 1 of 1 by `rfl` | 4 | 2,879 → 1,173 | 366 | +1,340 |
| F02076 `JetRate` / `FiniteJetRate` (big-O) | 2 | new definition `JetRateOn S …`, the set of orders explicit | 1 by `↔`, 1 by `rfl` | 6 | 8,503 → 1,082 | 7,312 | +109 |
| **total** | | | | **67** | **71,753 → 14,932** | **16,257** | **+40,564** |

"Net" is nodes saved in the re-derived proofs minus the new library; positive is a saving. Lemmas of a primitive that the corpus already has are not charged. `MemClass` is a member of two families. F00079 has 28 re-derivations that compile; one is circular and is not counted (section 3).

**Why each form.**

- **F00019, one definition.** The seven members are the same function; any parameter would be decoration.
- **F00042, a definition with an explicit parameter.** The members differ in a direction vector and in the spaces. The direction is an explicit argument; the spaces are implicit type arguments with their normed-space instances. A structure or class has nothing to bundle. **A simpler choice exists, found in review and rerun here: no new definition, with Mathlib's `fderiv ℝ f x v` written directly.** Re-deriving the same 13 lemmas from Mathlib alone (`corpora/families/lean/F00042_mathlib.lean`; 13 of 13 statements are the corpus's, 9 syntactically and 4 up to unfolding instances) gives 4,405 → 4,419 proof nodes and 6,814 → 6,677 heartbeats (12 measurable) with no library at all, against 1,811 nodes plus 3,675 of library with `dirDeriv`, and 18 → 0 definitions instead of 18 → 1. The corpus's member lemmas were already Mathlib one-liners, so the `dirDeriv` saving is those proofs moved into seven generic lemmas. On this evidence F00042 is class (d), a library notion under local names, not a family that needed a primitive.
- **F02076, a definition with an explicit parameter.** "One order" and "all orders up to M" are both "the orders in a set S": `JetRateOn {m}` and `JetRateOn (Set.Iic M)`. The second is definitional; the first is an `↔`.
- **F00046, F00073, F00079: nothing new.** The corpus already wrote the parameterised form (a weight; a value space; an index and localising sets). What was missing is the statement that the other members are instances of it.
- **F00015, a bundled structure from the library.** The bodies have nothing in common, so no parameter can merge them; what they share is closure under `0`, `+`, `-`. That is `AddSubgroup`. It is not `Submodule` because six members have no constant-multiple lemma in the corpus. It is not a type class because each member is a family indexed by sets, intervals or gauges, so there is no canonical instance for search to find; instance search would add cost and find nothing.

## 3. One family in full: F00079

Four predicates say "all jets of `f` are bounded by a constant times a majorant", with the constant hidden behind `∃`. The corpus source, abridged (fields in the same order):

```lean
structure MemClass     (s) (w : ℕ → D → ℝ)     (α) (f : ℕ → D → E)                             -- one family
structure UniformClass (s) (w : ι → ℕ → D → ℝ) (α) (f : ι → ℕ → D → E)                         -- uniform in a label
structure LocalJets    (s) (w : ℕ → D → ℝ)     (α) (K : ℕ → I → Set D) (f : ℕ → I → D → E)     -- only on cells K
structure LocalClass   (s) (K : ℕ → I → Set D) (w : ℕ → I → D → ℝ) (α) (f : ℕ → I → D → E) : Prop where
  weight_nonneg : ∀ n i x, x ∈ s.domain → 0 ≤ w n i x
  smooth : ∀ n i x, x ∈ s.domain → x ∈ K n i → ContDiffAt ℝ ∞ (f n i) x
  bounds : ∀ m : ℕ, ∃ C : ℝ, 0 ≤ C ∧ ∃ p : ℕ,
    ∀ n i x, x ∈ s.domain → x ∈ K n i → ∀ j ≤ m,
      ‖iteratedFDeriv ℝ j (f n i) x‖ ≤ majorant s (fun n x => w n i x) α C p n x
```

`LocalClass` has both optional features, so it is the primitive. What this node adds (`corpora/families/lean/F79.lean`, kernel-checked):

```lean
theorem memClass_iff :
    MemClass s w α f ↔ LocalClass s (fun _ (_ : Unit) => univ) (fun n _ => w n) α (fun n _ => f n)
theorem uniformClass_iff :
    UniformClass s w α f ↔ LocalClass s (fun _ (_ : ι) => univ) (fun n l => w l n) α (fun n l => f l n)
theorem localJets_iff (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K f ↔ LocalClass s K (fun n _ => w n) α f
-- the hypothesis cannot be dropped: weight −1, the zero family
theorem localJets_not_localClass (s) (α) (K) (i : I) {x : D} (hx : x ∈ s.domain) :
    LocalJets s (fun _ _ => -1) α K (fun _ _ _ => (0 : E)) ∧
      ¬ LocalClass s K (fun _ _ _ => -1) α (fun _ _ _ => (0 : E))
```

The API is `LocalClass`'s own, already in the corpus. A member lemma before and after (statement identical; the proof is the only change):

```lean
-- corpus: 23 lines, 6,787 proof nodes (heartbeats not measured: the corpus proof uses a private helper and did not replay in the scratch file)
theorem MemClass.bilinear {u : ℕ → D → F} (hf : MemClass s w α f) (hu : MemClass s v β u) (L : E →L[ℝ] F →L[ℝ] G) :
    MemClass s (fun n x => w n x * v n x) (α + β) (fun n x => L (f n x) (u n x)) := by
  refine ⟨fun n x hx => mul_nonneg (hf.weight_nonneg n x hx) (hu.weight_nonneg n x hx),
    fun n => (L.contDiff.comp_contDiffOn (hf.smooth n)).clm_apply (hu.smooth n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hu.bounds m
  refine ⟨‖L‖ * (2 : ℝ) ^ m * A * B, by positivity, p + q, ?_⟩
  …                                                   -- 12 more lines; the same proof is in the corpus four times
-- re-derived: 5 lines, 1,015 proof nodes, 1,113 heartbeats
    … := memClass_iff.2 ((memClass_iff.1 hf).bilinear (memClass_iff.1 hu) L)
```

All re-derived lemmas of this family:

| lemma | proof nodes | instance slots | heartbeats | lines |
|---|---|---|---|---|
| `WeightedClasses.MemClass.map` | 2,948 → 387 | 1,020 → 131 | 1,655 → 423 | 15 → 3 |
| `WeightedClasses.MemClass.fderiv` | 1,957 → 403 | 846 → 134 | 1,149 → 811 | 11 → 3 |
| `WeightedClasses.MemClass.bilinear` | 6,787 → 1,015 | 2,756 → 436 | n/a (replay failed) → 1,113 | 23 → 5 |
| `WeightedClasses.MemClass.mul` | 101 → 235 | 20 → 61 | 245 → 263 | 5 → 5 |
| `CurlClassBounds.class_neg` | 320 → 185 | 119 → 54 | 419 → 170 | 3 → 3 |
| `CurlClassBounds.class_sub` | 243 → 217 | 57 → 68 | 278 → 235 | 3 → 3 |
| `LabelSumBounds.UniformClass.map` | 3,005 → 348 | 1,024 → 101 | 1,617 → 429 | 14 → 3 |
| `LabelSumBounds.UniformClass.neg` | 342 → 184 | 119 → 48 | 447 → 198 | 4 → 3 |
| `LabelSumBounds.UniformClass.bilinear` | 6,790 → 863 | 2,683 → 319 | 3,582 → 1,123 | 20 → 5 |
| `UniformPrimaryWeights.fderiv_class` | 1,939 → 373 | 846 → 122 | 1,159 → 814 | 9 → 3 |
| `UniformHarmonicInteraction.cmul` | 186 → 347 | 49 → 93 | 439 → 484 | 5 → 5 |
| `PeriodizedWaveBounds.LocalJets.bilinear` | 6,972 → 799 | 2,776 → 301 | n/a (replay failed) → 1,148 | 21 → 7 |
| `WeightedClasses.MemClass.add` | 3,347 → 222 | 1,038 → 70 | 1,118 → 286 | 19 → 3 |
| `WeightedClasses.MemClass.zero` | 876 → 215 | 281 → 49 | 436 → 213 | 7 → 3 |
| `WeightedClasses.MemClass.mono_exponent` | 1,177 → 154 | 384 → 41 | 351 → 159 | 12 → 3 |
| `WeightedClasses.MemClass.mono_weight` | 1,165 → 251 | 369 → 54 | 374 → 196 | 12 → 4 |
| `WeightedClasses.MemClass.smul` | 194 → 387 | 51 → 100 | 975 → 507 | 5 → 5 |
| `WeightedClasses.MemClass.band_smul` *(circular, not counted)* | 2,459 → 291 | 852 → 80 | 2,387 → 418 | 23 → 3 |
| `WeightedClasses.MemClass.directional` | 717 → 335 | 343 → 124 | 1,005 → 356 | 3 → 3 |
| `LabelSumBounds.UniformClass.add` | 3,432 → 225 | 1,046 → 64 | 1,165 → 295 | 18 → 3 |
| `LabelSumBounds.UniformClass.sub` | 270 → 222 | 57 → 63 | 300 → 262 | 3 → 3 |
| `LabelSumBounds.UniformClass.zero` | 889 → 206 | 281 → 41 | 452 → 223 | 7 → 3 |
| `LabelSumBounds.UniformClass.mono_exponent` | 1,209 → 163 | 384 → 41 | 368 → 167 | 12 → 3 |
| `LabelSumBounds.UniformClass.mono_weight` | 1,202 → 267 | 370 → 54 | 400 → 209 | 12 → 4 |
| `LabelSumBounds.UniformClass.congr` | 1,195 → 254 | 375 → 56 | 362 → 207 | 12 → 3 |
| `PeriodizedWaveBounds.LocalJets.add` | 3,555 → 221 | 1,060 → 45 | n/a (replay failed) → 306 | 19 → 4 |
| `PeriodizedWaveBounds.LocalJets.band_smul` | 423 → 328 | 101 → 82 | 536 → 448 | 7 → 4 |
| `PeriodizedWaveBounds.LocalJets.smul` | 938 → 484 | 381 → 120 | 1,073 → 557 | 6 → 4 |
| **27 lemmas counted** | **52,179 → 9,290** | **18,836 → 2,872** | **19,905 → 9,035 (24 measurable)** | **287 → 100** |

*Circular:* the corpus's `LocalClass.band_smul`, which the re-derived `MemClass.band_smul` cites, is itself proved from `MemClass.band_smul` (`corpora/families/lean/Circ.lean` prints, for every re-derived lemma, which replaced originals it depends on; this is the only one that depends on itself, and no two re-derivations depend on each other's originals). The original cannot be deleted, and the row is in no total. The re-derived `LocalJets.band_smul` also depends on `MemClass.band_smul` staying. *Replay failed:* three corpus proofs use a private helper that is out of scope in a scratch file, so they have no valid "before" heartbeat figure; the first version of this report printed the heartbeats of the failed elaboration.

The list is every theorem of `MemClass.*`, `UniformClass.*`, `LocalJets.*` with the same short name as a `LocalClass` lemma (17 / 12 / 7 theorems in those namespaces; 11 / 9 / 6 matched), plus four with other names (`class_neg`, `class_sub`, `fderiv_class`, `cmul`). Three small lemmas grow (`MemClass.mul`, `MemClass.smul`, `cmul`, each a one-line corollary already). **Two did not transfer: `LocalJets.map` and `LocalJets.fderiv`** are stated without a nonnegative weight, and `LocalClass` cannot supply them without one. The corpus itself carries that hypothesis by hand on `LocalJets.add`, `.bilinear`, `.smul` and `.band_smul`. `UniformClass.congr` needed `LocalClass.congr_germ`, because it is stated with equality on the domain only and `LocalClass.congr` asks for equality everywhere.

The corpus knows these predicates are related: it has `LocalClass.of_global`, `of_localJets`, `to_localJets` and `UniformClass.each`, and a private helper `bilinear_jet_at` that is defined identically in two files. It converts between the predicates and still proves the algebra for each.

## 4. Measurements

### 4.1 Concept count

| family | definitions | lemma statements in the library | cited by a user | what is counted |
|---|---|---|---|---|
| F00015 | 15 → 14 (`Support` and `GaugeSupported` are one predicate (`rfl`); the predicates stay) | 55 → 55 | 55 → 15 | the corpus's `zero` (11), `add` (15), `neg` (14), `sub` (15) statements. In the library: 15 `sub` removed, 15 subgroup declarations added, the 40 `zero`/`add`/`neg` proofs kept as their fields. A user cites the 15 subgroup declarations |
| F00019 | 7 → 1 | 0 → 0 | 0 → 0 | the definition has no lemmas of its own |
| F00042 | 18 → 1 (18 → 0 with Mathlib's `fderiv ℝ f x v` written directly, section 2) | 13 → 7 | 13 → 7 | the 13 closure laws in the sampled list against 7 generic lemmas |
| F00046 | 5 → 5 (the four names stay as abbreviations (5 → 1 if they are inlined)) | 2 → 0 | 2 → 0 | `Class.neg` and `Class.sub` duplicate `CurlClassBounds.class_neg`/`class_sub` and were re-derived by citing those (which are themselves re-derived in F00079), not through `MemClass`'s API |
| F00079 | 4 → 2 (`UniformClass` goes; `LocalJets` stays (an instance only with a nonnegative weight); `MemClass` goes here but stays through F00046) | 30 → 6 | 30 → 6 | 30 laws with a `LocalClass` counterpart; after: 3 bridges, the 2 `LocalJets` laws that do not transfer, and `MemClass.band_smul`, which `LocalClass.band_smul` is proved from |
| F00073 | 2 → 1 | 4 → 0 | 4 → 0 | four lemmas stated for both |
| F02076 | 2 → 1 | 6 → 4 | 6 → 4 | `weaken`, `add`, `congr_on` twice against the same three plus `mono` |
| **total** | **52 distinct → 25** | **110 → 72 (-35%)** | **110 → 32** | |

`MemClass` is in two families: it is counted once before, and after it survives once, as the form the four named weights are instances of (and because `LocalClass.band_smul` is proved from `MemClass.band_smul`). If `MemClass` were also folded into `LocalClass` the count would be 52 → 24, at the price of stating the four weights against a five-parameter structure at a one-point index. The first version of this report said 53 → 24 and 110 → 31: it counted `MemClass` twice, counted `LocalJets` as deleted while keeping two of its laws, and counted only what a user cites. The corpus has 9,903 reachable definitions and 25,715 reachable theorems, so these seven families are 27 definitions (0.27%) and 38 statements (0.15%). For F00042 only the sampled list was worked (13 closure laws in 40 sampled of 43 listed); the corpus has more copies of the same seven laws that were not counted.

*More parameters per concept.* Fewer concepts is not the same as lighter concepts: `LocalClass` has five explicit parameters and an index type where `MemClass` has four; `dirDeriv` has a direction and four instance arguments where `partialX` had none; `JetRateOn` takes a set of orders where `JetRate` took one order.

### 4.2 Proof size, with the library charged

| family | lemmas | proof nodes | source lines | library: declarations / nodes / lines | net nodes | net lines |
|---|---:|---|---|---|---:|---:|
| F00015 | 15 | 3,207 → 1,402 (-56%) | 47 → 43 | 18 / 1,717 / 76 | +88 | -72 |
| F00019 | 0 | – | – | 2 / 121 / 6 | -121 | -6 |
| F00042 | 13 | 4,405 → 1,811 (-59%) | 51 → 45 | 26 / 3,675 / 58 | -1,081 | -52 |
| F00046 | 2 | 580 → 174 (-70%) | 10 → 6 | 4 / 222 / 12 | +184 | -8 |
| F00079 | 27 | 52,179 → 9,290 (-82%) | 287 → 100 | 3 / 2,844 / 39 | +40,045 | +148 |
| F00073 | 4 | 2,879 → 1,173 (-59%) | 20 → 10 | 1 / 366 / 2 | +1,340 | +8 |
| F02076 | 6 | 8,503 → 1,082 (-87%) | 56 → 28 | 7 / 7,312 / 48 | +109 | -20 |
| **total** | **67** | **71,753 → 14,932 (-79%)** | **471 → 232** | **61 / 16,257 / 241** | **+40,564** | **-2** |

Proof nodes are distinct subterms of the elaborated proof (the corpus export's `proofSize`). Source lines are whole declarations, statement included. The library column counts only declarations written for this node: the primitive where it is new, its API where it is new, and the "member is an instance" lemmas.

- **F00042**: the generic API is 7 lemmas, 2,990 nodes; the 18 `rfl` instance lemmas are 522 nodes. At 13 re-derived lemmas the library is not yet paid for.
- **F02076**: the three generic laws plus `mono` are 5,830 nodes, about the size of one copy of the three laws they replace (4,672); the `↔` for `JetRate` is 1,247.
- **F00015**: the 15 subgroup declarations and the two bridge lemmas are 1,717 nodes for 1,805 saved: the `sub` lemmas were already one-liners (`hf.add hg.neg`).
- **F00019**: nothing to save. The members have no lemmas of their own.
- **Without F00079** the six other families net +519 nodes and -150 source lines.

### 4.3 Statements

Re-derived lemmas keep the corpus statement, so their size and hypothesis counts do not change. Two things do change.

*Generic lemma against the member lemma it replaces* (statement nodes; proposition hypotheses; instance arguments):

| generic | statement | member lemma | statement |
|---|---|---|---|
| `F2076.JetRateOn.add` | 196 nodes, 6 hyps, 4 inst | `DiagonalResidual.JetRate.add` | 194 nodes, 6 hyps, 4 inst |
| `F2076.JetRateOn.weaken` | 123 nodes, 3 hyps, 4 inst | `DiagonalResidual.JetRate.weaken` | 121 nodes, 3 hyps, 4 inst |
| `F42.dirDeriv_contDiffAt` | 126 nodes, 2 hyps, 4 inst | `SimilarityProfile.partialX_smoothAt` | 101 nodes, 2 hyps, 0 inst |
| `F42.dirDeriv_const_mul` | 138 nodes, 1 hyps, 2 inst | `NaturalCoefficientBridge.partialX_const_mul` | 99 nodes, 1 hyps, 0 inst |
| `F42.hasDerivAt_fst_slice` | 347 nodes, 1 hyps, 4 inst | `SmoothFourierData.hasDerivAt_slice` | 206 nodes, 1 hyps, 0 inst |
| `F42.dirDeriv_mul` | 195 nodes, 2 hyps, 2 inst | `EulerMeanHarmonic.partialDerivative_mul` | 180 nodes, 2 hyps, 0 inst |
| `LocalizedWaveBounds.LocalClass.bilinear` | 692 nodes, 2 hyps, 8 inst | `WeightedClasses.MemClass.bilinear` | 666 nodes, 2 hyps, 8 inst |
| `LocalizedWaveBounds.LocalClass.map` | 248 nodes, 1 hyps, 6 inst | `WeightedClasses.MemClass.map` | 229 nodes, 1 hyps, 6 inst |
| `LocalizedWaveBounds.LocalClass.fderiv` | 288 nodes, 1 hyps, 4 inst | `WeightedClasses.MemClass.fderiv` | 270 nodes, 1 hyps, 4 inst |

Over these nine pairs the generic statement is +14% in nodes (2,066 → 2,353). Hypothesis counts are equal; the polymorphic ones carry more instance arguments (`dirDeriv_*`: 4 against 0, because the member was stated at `ℝ × ℝ`).

*A downstream statement restated against the primitive* (statement nodes summed over the theorems that were restated):

| family | sampled API list | 10 downstream |
|---|---|---|
| F00019 | 7,234 → 7,234 (+0%) | 4,098 → 4,098 (+0%) |
| F00042 | 5,695 → 7,428 (+30%) | 2,106 → 2,486 (+18%) |
| F00046 | 10,098 → 10,874 (+8%) | 4,468 → 4,814 (+8%) |
| F00073 | 2,771 → 2,755 (-1%) | 3,495 → 3,536 (+1%) |
| F02076 | 1,971 → 1,971 (+0%) | 3,885 → 3,885 (+0%) |

F00019 is a rename. F02076 replaces the member by a reducible name for the instance, so sizes are equal by construction. F00042 is the measured cost of polymorphism in statements: each `partialX f w` becomes `dirDeriv (1, 0) f w` with the two spaces and four instances written out in the term. A reader does not see them; the elaborator and every tool that walks the term does. F00046 grows because the named weight is written out.

### 4.4 Elaboration cost

| family | instance slots in the proofs | + new library | heartbeats in the proofs (lemmas measurable) | new library: charged / used | total with library, charged (used) |
|---|---|---|---|---|---|
| F00015 | 689 → 233 (-66%) | 538 | 3,312 → 17,035 (+414%; 15 of 15) | 5,297 / 5,025 | 3,312 → 22,332 (+574%); 22,060 (+566%) |
| F00019 | – | 10 | – | 114 / 0 | 0 → 114 |
| F00042 | 1,507 → 497 (-67%) | 1,581 | 6,814 → 4,849 (-29%; 12 of 13) | 11,839 / 5,294 | 6,814 → 16,688 (+145%); 10,143 (+49%) |
| F00046 | 173 → 40 (-77%) | 76 | 538 → 261 (-51%; 2 of 2) | 439 / 0 | 538 → 700 (+30%); 261 (-51%) |
| F00079 | 18,836 → 2,872 (-85%) | 3,690 | 19,905 → 9,035 (-55%; 24 of 27) | 767 / 647 | 19,905 → 9,802 (-51%); 9,682 (-51%) |
| F00073 | 933 → 348 (-63%) | 465 | 9,206 → 2,212 (-76%; 4 of 4) | 353 / 0 | 9,206 → 2,565 (-72%); 2,212 (-76%) |
| F02076 | 3,160 → 248 (-92%) | 2,840 | 2,379 → 1,360 (-43%; 6 of 6) | 1,753 / 1,553 | 2,379 → 3,113 (+31%); 2,913 (+22%) |
| **total** | **25,298 → 4,238 (-83%)** | **9,200 (-64%)** | **42,154 → 34,752 (-18%; 63 of 67)** | **20,562 / 12,519** | **42,154 → 55,314 (+31%); 47,271 (+12%)** |

- *Instance slots*: instance-implicit arguments filled at constant applications in the proof term, counted on distinct subterms. They fall with proof size; the share of applications that carry one does not change much.
- *Heartbeats*: Lean's deterministic work counter (`#count_heartbeats`, statement and proof, asynchronous elaboration off), for the same statement with the corpus proof and with the re-derived proof, each re-elaborated in a scratch file. Independent of machine load; repeat runs differ by a few heartbeats.
- *Which lemmas are in the heartbeat totals.* 63 of the 67 counted lemmas. Four corpus proofs did not elaborate in the scratch file, so their "before" figure is not a measurement and they are left out on both sides: `PositiveAxisSystem.hasDerivAt_parameterProfile`, `WeightedClasses.MemClass.bilinear`, `PeriodizedWaveBounds.LocalJets.bilinear`, `PeriodizedWaveBounds.LocalJets.add` (three use a private helper that is out of scope there, one hits an ambiguous name). The first version of this report used the heartbeats of those failed elaborations and reported 53,179 → 38,096 (-28%).
- *New library.* The first version charged the new library in nodes and lines and not in elaboration. "Charged" is the elaboration of every new declaration that is charged in nodes (the primitive, its API, the "member is an instance" lemmas; 20,562 heartbeats); "used" is the subset that some re-derived proof depends on, by transitive closure (12,519; the reviewer's slightly wider reading of "used" gave 13,096 and +14%). The library is elaborated once, so at higher adoption its share falls; at the adoption measured here it outweighs the saving in every family except the two whose primitive the corpus already had and proved laws for (F00079 and F00073). F00046 is cheaper only if its four `rfl` instance lemmas, which its two re-derived proofs do not cite, are left uncharged.
- **F00015 shows the risk of the bundled form.** 11 of the fifteen `sub` lemmas are cheaper through `AddSubgroup`, 3 are 6 to 16 heartbeats dearer; the fourteen other than `CoefficientsOn.sub` total 2,400 → 1,995. `CoefficientsOn.sub` goes from 912 to 15,040: its subgroup lives in a product of two `AddMonoidAlgebra`s, and matching `(c₁, d₁) - (c₂, d₂) ∈ S` against `CoefficientsOn … (c₁ - c₂) (d₁ - d₂)` makes the elaborator unfold both group structures. The proof term is a third of the size. The 15 subgroup declarations themselves cost 5,297 heartbeats, so the family goes 3,312 → 22,332 with its library charged. The cost is not a steady tax; it is an occasional large bill that the proof-size figure does not show.
- **Statement elaboration dominates small lemmas.** With asynchronous elaboration on, `#count_heartbeats` sees only the statement; those figures were within a few percent of the full ones for the short lemmas. A two-line corollary costs about what its statement costs, whichever proof it has.
- *Wall-clock file times are not reported.* The first version had a column of them, taken at load average 12 to 18 from other agents' builds: two rows were negative and F00073's re-derived file came out slower although its heartbeats fall 76%. That is noise, not a measurement, and the plan requires timings in a quiet window. No quiet window was available for this revision (load average 9 to 13), so the column is removed; `timing.sh` is kept.

### 4.5 Downstream theorems

Two kernel-level checks (`corpora/families/lean/Abs.lean`), on a seeded sample of 10 downstream theorems per family (statement mentions a member, not in the API list) and, for the second, on up to 200 seeded users per family.

- **Transport**: rewrite the statement to mention the primitive and give the kernel the original proof for the new statement (`defeq`), or carry it across a proved equation `member = instance` (`eq`).
- **Opacity**: replace the member by a variable and every cited lemma about it by a hypothesis; if the kernel accepts the result, the proof is *generic*: it uses the member only through lemmas. Otherwise it *opens* a structure member (constructor, projection) or *unfolds* a definition.

| family | theorems using a member | analysed | generic | opens / unfolds | 10 downstream: transport | 10 downstream: opacity |
|---|---:|---:|---|---|---|---|
| F00015 | 1,058 | 200 | 103 (52%; 95% 45–58%) | 33 / 61 (+3 not decided) | not run (`↔`, no tool) | 3 unfolds, 7 generic |
| F00019 | 1,070 | 200 | 57 (28%; 95% 23–35%) | 0 / 142 (+1 not decided) | 10 defeq | 7 unfolds, 3 generic |
| F00042 | 758 | 200 | 75 (38%; 95% 31–44%) | 0 / 125 | 10 defeq | 5 generic, 5 unfolds |
| F00046 | 993 | 200 | 150 (75%; 95% 69–80%) | 39 / 11 | 9 defeq, 1 nomention | 9 generic, 1 opens |
| F00079 | 796 | 200 | 114 (57%; 95% 50–64%) | 81 / 5 | not run (`↔`, no tool) | 6 opens, 4 generic |
| F00073 | 169 | 169 | 75 (44%; 95% 37–52%) | 0 / 92 (+2 not decided) | 7 defeq, 3 nomention | 8 generic, 2 unfolds |
| F02076 | 148 | 148 | 87 (59%; 95% 51–66%) | 0 / 61 | 6 eq, 4 defeq | 5 unfolds, 5 generic |

- `nomention` = the sampled theorem mentions only the member that is itself the primitive. Where transport was run, every statement that mentions a replaceable member was restated and kernel-checked: **F00019 10/10, F00042 10/10, F00046 9/9, F00073 7/7, F02076 10/10** (6 of those across the equation, since `JetRate` is an instance up to `↔` only). For the four families whose members equal the primitive by `rfl`, the 40 `defeq` results follow from the instance lemma by unfolding definitions, so they check the tool and not the generalisation; the informative cases are F02076's 6.
- For F00079 and F00015 no transport was run: the members are instances up to `↔` and I did not build the equation-based restatement for structures. The opacity column is the evidence there: 4 and 7 of 10 are generic.
- On the sampled API lists transport gave: F00019 40/40, F00042 40/40, F00046 34/34, F00073 5/5, F02076 9 of 13 (4 universe-polymorphic statements defeated the tool, three of them the closure laws that were re-derived by hand).
- *What "generic" buys.* A generic proof is the theorem already written against an interface: `Fam.Abs.<name>` is the kernel-checked statement "for any `M` with these lemmas, …". That is the class-like reading of the owner's idea, and it holds for about half of the users without anyone having written a class. The interface is large, though: the generic proofs cite 216 (F00015), 52 (F00019), 112 (F00042), 258 (F00046), 241 (F00079), 62 (F00073), 106 (F02076) distinct lemmas about the members, so "generic" here does not mean "written against a small, class-like API".
- Replaying a theorem's source with the member's name swapped (the first method tried) under-measures: on F02076 it passed 5 of 13 and 3 of 10, failing wherever the proof cites a corpus lemma still stated with the old name. It is kept only for that family (`out/families/gen/F02076_replay_piecemeal.txt`).

## 5. What did not generalise, and why

1. **`LocalJets` is not an instance of `LocalClass` without a hypothesis it lacks.** `LocalClass` bundles `weight_nonneg`; `LocalJets` does not. Counterexample (kernel-checked, `localJets_not_localClass`): weight −1 and the zero family. Consequence: `LocalJets.map` and `LocalJets.fderiv` cannot be obtained from the primitive. A primitive without the field would fix that and break the other three members, whose `bilinear` uses it. *Reading:* the nonnegativity is a fact about the weight, not about `f`, and would sit better as a separate hypothesis for all four; that is a redesign, not a merge.
2. **`NativeJets` is a subgroup only for a nonnegative weight** (`nativeJets_empty`: with weight −1 it has no members, so not even zero). Same cause: a predicate about `f` that also carries a fact about a parameter.
3. **The 15 predicates have no common body, so there is no parameterised primitive, only an interface, and the interface deletes no definition.** It also splits: 9 members have a constant-multiple lemma and could be `Submodule`s, 6 have none in the corpus, and `ScalarOn` has no `neg` (it was derived from `smul (-1)`). Two of the 15 (`Support`, `GaugeSupported`) are the same predicate by `rfl`; that is deduplication and the only definition removed.
4. **F00042 is better left as two primitives.** `dirDeriv` covers all 18 members. The corpus also has `NaturalAxisBridge.partialEta F p := deriv (fun η => F (p.1, η)) p.2`, the derivative of a slice, which agrees with `dirDeriv (0, 1)` only where `F` is differentiable. The corpus proves that agreement several times with that hypothesis (`parameterPartial_natural`, `parameterPartial_eq_partialEta`, …). Merging the two would put a differentiability side condition on every use.
5. **For F02076 the instance is an `↔`, not a definitional equality**, so the 61 of 148 users that unpack the constant by hand (`obtain ⟨C, hC, hb⟩ := hf`) would have to be rewritten or go through the equivalence. The other 87 need no change.
6. **F00019 has nothing to generalise.** It is one definition written seven times. 71% of its sampled users unfold it, so an opaque interface would be the wrong tool; one shared name is the whole gain.
7. **Proof size does not repay the library in two families and barely does in two more.** Net of the new library: F00042 and F00019 are negative, F00015 and F02076 are within about a hundred nodes of zero, F00046 and F00073 save a few hundred to a thousand, and F00079 saves 40 thousand (section 4.2). In elaboration, with the library charged, only F00079, F00073 and F00046 come out cheaper (section 4.4).
8. **Nothing false was found**, against 18 of 20 in the earlier statement-shape clusters. This tests little: in three of seven families the primitive was a definition the corpus already had and in one it was Mathlib's, so only `JetRateOn` and `dirDeriv` were new parameterised statements, and no over-general statement was attempted. *Reading:* those were clusters of theorems with similar statements; these are clusters of definitions chosen after a reading of their bodies. The two are not comparable, and seven families is a small number.
9. **One re-derivation was circular.** `MemClass.band_smul` re-derived from `LocalClass.band_smul` compiles, but the corpus proves the latter from the former. A merge has to follow the direction in which the corpus proved things, or re-prove the general lemma; compiling is not enough. Every re-derivation is now checked for this (`Circ.lean`).

## 6. Extrapolation, with the range the sample supports

The clustering has 4,178 family records. Sorted by the kind of hole, with how the 60 that were read fell:

| kind | records | definitions removable on paper | read in the top 60 | of those, class (a) | 95% interval |
|---|---:|---:|---:|---:|---|
| value or predicate, body identical (like F00019) | 222 | 298 | 5 | 3 | 23–88% |
| one simple hole, shared body ≥ 4 nodes (like F00042) | 680 | 934 | 6 | 1 | 3–56% |
| named instances of an existing definition (like F00046, F00073) | 469 | 1,473 | 16 | 1 | 1–28% |
| predicates joined by lemma roles only (like F00015, F00079) | 44 | 62 | 2 | 2 | 34–100% |
| non-predicates joined by lemma roles or shapes | 762 | 912 | 0 | 0 | none read |
| loose anti-unification | 1,830 | 3,269 | 11 | 1 | 2–38% |
| types | 171 | 569 | 20 | – | class (a0), section 7 |

"Removable on paper" is members minus one per connected group of records, the clustering's own count; it is an upper bound, not a measurement. The top 60 are the highest-scoring records, not a random sample, so the intervals describe "if the rest were like the ones read", which favours the rest.

- **Definitions.** The two kinds where a merge deletes definitions are the verbatim copies and the one-hole families. Applying the class (a) shares read above: 179 + 156 ≈ **334 definitions, range 97 to 789** (3.4% of 9,903; 1.0% to 8.0%). The range is wide because 5 and 6 families of those kinds were read. **The central estimate is fragile to a single reading:** the one-hole kind's only class (a) family is F00042, which the second reading and the Mathlib-only rerun both make class (d); with 0 of 6 the estimate falls to about 179 definitions (range 69 to 628).
- **Named instances** (469 records). One in 16 was read as class (a). Where it is, the primitive exists and the definitions stay as names; the gain is lemma statements, and section 4.5 says how many: for `MemClass` and its weights 75% of users are already generic.
- **Role families of predicates** (44 records, 89 definitions). Both that were read were class (a) and both generalised, in opposite ways: F00079 into an existing structure with a large proof saving, F00015 into a library interface with none. Two families do not support a rate.
- **Lemma statements and proofs.** The measured saving per re-derived lemma is 848 nodes on average before the library is charged and 348 without F00079. The clustering counts 589 identical-shape lemma statements in the verbatim and one-hole kinds; at the shares above that is roughly 134 statements. *Reading:* a full pass would be worth a few hundred definitions (about 2% to 3% of them, anywhere from 1% to 8%) and one to a few hundred lemma statements (under 1%), with proof-size savings concentrated in a handful of families like F00079 that a body-based matcher does not find; the role channel found it and ranked it 79th.
- **What the sample cannot say.** Whether the unread 4,118 records contain more families like F00079. It was found by lemma roles; its members differ by a binder, so the body channel did not join them. A search aimed at that pattern (several structures whose fields are the same up to an extra index or an extra guard) is the obvious next instrument.

## 7. Class (a0): one type under many names

Twenty of the 60 clusters are type abbreviations. For the 19 with no hole, every member was compared with the first of its family: **389 of 389 are equal by `rfl`** (`corpora/families/lean/A0.lean`), so 389 names (3.9% of reachable definitions) could be removed with no statement or proof changing its meaning. The largest:

| family | type | names | modules | users |
|---|---|---:|---:|---:|
| F00001 | `Prod Real (Prod (Prod Real Real) (Prod Real Real))` | 75 | 74 | 3,169 |
| F00002 | `Prod Real Real` | 60 | 60 | 8,117 |
| F00003 | `Prod Real (Prod Real Real)` | 52 | 49 | 3,004 |
| F00005 | `Prod (Prod Real (Prod (Prod Real Real) (Prod Real Real))) Re` | 41 | 41 | 1,409 |
| F00006 | `EuclideanSpace Real (Fin 3)` | 28 | 27 | 12,066 |
| F00007 | `Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (Pro` | 18 | 18 | 993 |

F00011 (`Fin n → ℝ`, 35 names for six values of n) was not checked member by member. *Reading:* this is the largest concept-count item in the top 60 and it is not what the owner's idea is about; it is a linter rule ("this abbreviation already exists in module X"), and the human projects show almost none of it (Carleson 5, PFR 0 verbatim copies).

## 8. The software side: could this propose frames?

Read from `slice/lean/Frames/` (read-only; nothing was built or run there). *This section is a reading.*

**Yes for modifiers, with changes; not yet for new frames.** The frame library is a set of definitions `Frame op holes := ∀ s a, Frame.at op holes s a` over one `Op` structure, which is the shape the body channel handles. Reading the 23 signatures, the existing frames already fall into families with one hole in head position: `IncreasesBy` / `DecreasesBy` / `Becomes` / `AtMost` / `AtLeast` (how the new measure relates to the old one), `ResultIs` / `ResultAtMost` / `ResultAtLeast` (the comparison), `Always` / `Never` and `EveryOf` / `NoneOf` (polarity), `Within` / `Covers` (direction of inclusion), `IndependentOf` / `IndependentGiven` (an extra guard, the `MemClass` / `LocalClass` pattern). Anti-unification would report those holes, and a hole that recurs across families is a candidate *modifier*: a comparison, a polarity, a guard.

What would have to change:

1. **Cluster rule statements, not library definitions.** The input is the body of compiled rules (each an instance of a frame) plus the rules that did not fit any frame and were written by hand. The second set is where a new frame would come from; today it is small.
2. **Typed holes in the frame vocabulary.** A hole should be reported as "a `Measure`", "a `Cond`", "an `AnswerClass`", not as an expression. The exporter here already types holes; it needs the frame library's role abbreviations as the type lattice.
3. **Anti-unify both readings together.** Every frame has a logical reading and an executable one (`Check.*`). A proposed frame must come with both, so the unit to generalise is the pair, and a proposal whose checker does not generalise the same way is rejected. The lemma-role channel plays that part for mathematics; here the second reading plays it.
4. **The kernel decides, as here.** Acceptance is "every old rule statement is equivalent to an instance of the proposed frame", which is the transport check of section 4.5 and what V2/V3 already did by hand for the 23 frames.
5. **A person decides whether it reads.** A parameterised frame is only better if its rule line is still a sentence. That is K1's meaning trial, not something this tool can score; F00015 above is the warning (a correct abstraction that made nothing simpler to state).
6. **Expect the same economics.** In the mathematics the merge paid where the same proof had been written four times and not otherwise. For frames the analogue is the per-frame lemmas and harness generators: a modifier pays if it removes duplicated proofs about frames, not because it removes a name.

## 9. Verdict, as a trade

**Worth exploring: yes, as a finder of a few large families and as a deduplication report; no, as a general way to shrink proofs.**

- **What it buys in concepts.** On seven families, 52 distinct definitions → 25, and 110 lemma statements → 72 in the library (32 cited by users, by a convention that hides 40 proofs inside 15 declarations). Extrapolated with wide error, 180 to 330 definitions over the corpus (2% to 3%, range 1% to 8%) and one to a few hundred lemma statements, plus 389 type abbreviations that need no abstraction. Half of the downstream proofs use a member only through lemmas, but through 52 to 258 of them per family.
- **What it costs or saves in proof size.** 71,753 → 14,932 nodes over 67 lemmas, for 16,257 nodes of library. F00079 is 75% of the gross saving and 99% of the net saving once the library is charged; the other six families net +519 nodes together, which is break-even, as before. In source lines the whole exercise is 2 lines longer.
- **What it costs in elaboration.** Proofs alone: -18% heartbeats. With the new library's elaboration charged: +12% to +31%. Only two families are cheaper, both reusing a primitive the corpus already had with its laws proved (F00079 -51%, F00073 9,206 → 2,565). F00046 goes 538 → 700, F00042 6,814 → 16,688, F02076 2,379 → 3,113, F00015 3,312 → 22,332. Statement terms grow +30% when the parameter is a type with instances. A bundled interface: 16× on one lemma in fifteen.
- **Where it applies.** Where the corpus wrote one structure several times with an extra index or guard and proved its laws each time (F00079), and where it wrote the general form and then restated its lemmas for named instances (F00046). Both are found by lemma roles and named-instance detection, not by body similarity.
- **Where it does not.** Predicates with different bodies and the same algebra: the interface exists (it is the library's), deletes no definition, saves no proof, and once in fifteen cost a great deal of elaboration. Definitions that bundle a fact about a parameter: the generalisation needs a hypothesis. Quantities whose users unfold them: one shared name is all there is. Named instances built with one constructor from different objects (19 of the 60 read): leave alone. A library notion applied to an argument (F00042): use the library notion; a new primitive only moves the proofs.
- **On "like a class".** Nothing here needed a type class, and the one bundled interface was the weakest trade. What worked was the lightest form each time: an existing definition with one more thing said about it ("this other one is an instance").

## 10. Review, corrections applied, and where this version disagrees

An independent agent rebuilt everything from copies under `out/families/review/`. The kernel-checked core reproduced exactly: every family file, re-derivation, transport and opacity result, all 68 statements equal to the corpus's, every "member is an instance" lemma about the original corpus constant. It found three defects in the measurements, all fixed here and rerun in `corpora/families/` (not copied from the review):

1. **A circular re-derivation** (`MemClass.band_smul`). Now detected by `Circ.lean` for all 81 re-derivations (68 plus the 13 Mathlib-only ones) and excluded: 67 lemmas, 71,753 → 14,932 nodes, net 40,564 (was 42,732), and 2 source lines added (was 18 saved).
2. **Four invalid "before" heartbeat figures**, from corpus proofs that failed to replay. `measure.py` now uses a heartbeat figure only when that elaboration succeeded: 63 valid pairs, 42,154 → 34,752 (-18%; was reported as -28%).
3. **The new library was not charged in elaboration.** Now measured (`LibHB_*.lean`): 20,562 heartbeats for every charged declaration, 12,519 for those the re-derived proofs depend on, and 4,962 instance slots. The total is +12% to +31%, not -28%.

Also applied: the concept-count recount (section 4.1); the Mathlib-only alternative for F00042, rerun here (section 2); the second triage reading (section 1); the softened claims about "46 of 46", "generic", "nothing false" and the F00015 lemma split; the corrected F00046 description; the fragility of the extrapolation; the wall-clock column removed.

**Where this version differs from the review.**

- *Definitions after the merge: 25, not 24.* The review's 52 → 24 keeps `LocalJets` and counts `MemClass` once, but then `MemClass` is deleted in F00079 and kept in F00046. It has to stay once (the four weights are instances of it, and `LocalClass.band_smul` is proved from it), which gives 25; 24 needs the further step of folding `MemClass` away.
- *Lemma statements in the library: 72, not 71,* because the circular `MemClass.band_smul` has to stay.
- *Library elaboration: a range, not one figure.* The review charged 13,096 heartbeats ("declarations the re-derivations use") and got +14%. By transitive closure the proofs depend on 12,519 heartbeats of new declarations (+12%); charging the same set that is charged in nodes gives 20,562 (+31%). Both are given; the sign is the same.
- *Instance slots* are given with the circular lemma excluded, so the "before" figure is 25,298 where the review's text has 26,150.
- *F00042.* The review's reading that it is class (d) is accepted on the measurement, with one qualification that is a reading: writing `fderiv ℝ f x (1, 0)` in 652 downstream statements is longer for a person to read than `partialX f x`, and that cost was not measured. The Mathlib-only rerun keeps the member names in the 13 statements (they are the corpus's, verbatim); 18 → 0 definitions means restating their users, which was not done.

**What the review found about the clustering** (the reviewer's readings, not rerun here):

- No control name appears in the clustering logic; only the report looks names up.
- *15 random clusters outside the top 60* (seed 9090, spread over the looseness levels): 4 real families (a verbatim copy, one operation written four times, a pair differing in one projection, a tuple reordering that is a library equivalence), 6 parallel by construction, 5 accidental. The real ones were at the exact level, the project-heads level and the loosest level; none were in the mid-looseness, named-instance or lemma-role samples.
- *Families the method cannot see.* Of 30 random reachable definitions read with their 5 nearest neighbours by name and signature (seed 31337), 7 (95% interval 12% to 41%) have a neighbour the reviewer would call the same notion that no channel joins to them: `GradeGuards` as the same structure in 4 parallel modules; the `PressureStream` module redone in `VariableGaugeMean` with one extra argument; `MeanVector` / `LocalMeanVector` / `WaveVector`, a componentwise version of the class predicates; a `Cutoff` algebra; one map bundled twice; one formula over different triples; `basePressure` in three representations. The first three have the shape of F00079: parallel structures or modules that differ by one inserted argument or record. That is the pattern that paid, and the wide aperture as built misses it.

## Caveats

- **Exploratory.** The triage, the rule, the frozen list and the definition of each family's API list were written before any Lean (`TRIAGE_2026-11-11.md`). The sub-class (a0), the tools, the choice to re-derive closure laws outside the sampled lists (F00079, F00015) and the concept-count conventions were decided while working. `DECISIONS.md` lists them. One agent has reviewed the tools and the report; its second triage reading was not blind. Nothing is under version control, so "frozen before Lean" rests on file times.
- **Seven families.** Chosen by number of users among eight read as class (a); the two controls were known in advance to be good cases. The totals are dominated by one of the controls: F00079 is 99% of the net proof saving.
- **The triage is one model's reading**, made from bodies and lemma blocks. Classing named-instance families as (b) shrank class (a); a different reader gets a different top six.
- **Opacity is a property of the proof term**, with reducible abbreviations unfolded first. A proof that unfolds some other definition built on the member is counted as "unfolds". Theorems that hit the per-theorem limit are "not decided". Private theorems (1 to 7 per family) are skipped.
- **Transport for `↔` families** is done by a reducible name for the instance (F02076) or not at all (F00079, F00015).
- **Statements re-elaborated in a scratch file** are compared with the corpus statement term by term; four F00042 statements are equal only up to unfolding instances (a different but equal instance term was chosen) and are counted as the same.
- **No wall-clock timing is reported**; heartbeats are the elaboration measurement. Library heartbeats were measured in a copy of each family file with a counter on every declaration.
- **Four of 67 lemmas have no heartbeat comparison** (their corpus proof does not replay in a scratch file); they are large ones in F00079, so that family's heartbeat saving is measured on its smaller lemmas.
- **Concept counts are conventions**, given in the table. In particular F00015 counts 15 subgroup declarations in place of 55 closure statements although the member-specific `zero`, `add`, `neg` proofs are still needed as their fields; the library column counts them.

## Files and how to rerun

- `corpora/families/lean/F15.lean`, `F19.lean`, `F42.lean`, `F46.lean`, `F73.lean`, `F79.lean`, `F2076.lean`: primitives, instance lemmas, generic APIs, counterexamples. `A0.lean`: the type abbreviations.
- `corpora/families/subst/*.re.json`: the proof term of each re-derived lemma; `replay.py` copies the corpus statement and context around it.
- `corpora/families/lean/Tool.lean` (sizes, instance slots, statement comparison), `Abs.lean` (opacity, transport).
- `corpora/families/checkgen.py` writes `lean/Circ.lean` (dependency check of every re-derivation) and `lean/LibHB_*.lean` (library heartbeats) and collects them into `out/families/gen/circular.json` and `libhb.json`; `subst/F00042_mathlib.re.json` and `lean/F00042_mathlib.lean` are the Mathlib-only re-derivation.
- `out/families/review/`: the reviewer's copies, logs and readings (`retriage.json`, `recount.json`, `nn30.txt`).
- `corpora/families/all.sh` runs every Lean step, one process at a time (roughly 40 minutes on this machine under load; not timed as one command); `measure.py` and `report.py` rebuild `out/families/gen/summary.json` and this file.
- Inputs produced once by inline scripts and not regenerated by `all.sh`: `out/families/gen/api.json` (the frozen API lists), `kinds.json`, `F00079_names.json`.
- `out/families/TRIAGE_2026-11-11.md` / `.json`: the triage as frozen. `out/families/gen/`: API lists, samples, per-theorem results.
