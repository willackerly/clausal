
# Generated tables

Everything below is written by `bench/outline.py` from `out/corpus/ns/decls.jsonl`. Mass = proofSize + auxProofSize (distinct subterms). A head is a dominator-tree child of the hub or a side branch of the spine; a chapter is a head that dominates at least 20 declarations.

## Shape of the dominator tree

| | ns_r3 | ns_periodic | euler_r3 | euler_compact |
|---|---|---|---|---|
| declarations below the root | 23,747 | 23,840 | 13,108 | 13,213 |
| spine length below the root | 4 | 4 | 0 | 0 |
| children of the hub | 8,599 | 8,586 | 5,846 | 5,938 |
| ... that dominate nothing else | 7,448 | 7,437 | 4,829 | 4,894 |
| heads (children of the hub plus side branches of the spine) | 8,685 | 8,731 | 5,846 | 5,938 |
| accounting: mass under chapters | 65.0% | 64.9% | 42.1% | 41.3% |
| accounting: mass under heads dominating 2 to 19 | 19.6% (1,104 heads) | 19.7% (1,112 heads) | 32.4% (963 heads) | 33.0% (988 heads) |
| accounting: heads that dominate nothing (shared layer), mass | 15.4% (7,520 declarations, 31.7% of all) | 15.4% (7,556 declarations, 31.7% of all) | 25.5% (4,829 declarations, 36.8% of all) | 25.6% (4,894 declarations, 37.0% of all) |
| accounting: own proofs of the spine | 0.01% | 0.02% | 0.00% | 0.00% |
| chapters (20+ declarations) | 61 | 63 | 54 | 56 |
| mass under heads dominating 100+ declarations | 51.6% (13 heads) | 51.2% (13 heads) | 25.0% (7 heads) | 24.3% (9 heads) |
| skipped by trusting the 10 heaviest heads | 54.7% | 54.3% | 28.5% | 26.4% |
| ... the 40 heaviest | 63.4% | 63.0% | 40.4% | 39.1% |
| ... the 100 heaviest | 69.5% | 69.2% | 50.6% | 49.7% |
| ... every head that dominates anything | 84.6% (1,165 statements) | 84.6% (1,175 statements) | 74.5% (1,017 statements) | 74.4% (1,044 statements) |
| skipped by the outline printed below (level 1 only) | 56.5% (13 statements) | 56.1% (13 statements) | 33.2% (19 statements) | 32.5% (21 statements) |
| ... of which under: intermediate milestone, readable as printed | 3.7% | 3.7% | 0.0% | 0.0% |
| ... of which under: technical waypoint, readable as printed | 6.5% | 6.5% | 0.0% | 0.0% |
| ... of which under: waypoint whose content is in a structure defined elsewhere | 42.6% | 42.3% | 11.6% | 11.6% |
| ... of which under: restatement of the headline theorem | 0.0% | 0.0% | 3.9% | 1.6% |
| ... of which under: unreadable or arbitrary | 1.1% | 1.1% | 10.4% | 10.4% |
| ... of which under: not rated | 2.5% | 2.5% | 7.3% | 8.9% |
| definitions needed to unfold the level-1 statements alone (share of all non-theorems below the root) | 2,880 (43%) | 2,880 (43%) | 2,003 (47%) | 2,024 (47%) |
| chapter heads that are theorems / not | 52 / 9 | 54 / 9 | 33 / 21 | 35 / 21 |
| chapter heads with a docstring (all declarations) | 54% (19%) | 56% (19%) | 30% (30%) | 30% (29%) |
| median statement length of chapter heads, chars (all theorems) | 756 (375) | 811 (375) | 643 (406) | 634 (403) |
| outline statements over 1,000 chars | 19 of 40 | 19 of 40 | 20 of 40 | 20 of 40 |
| project declarations mentioned directly by outline statements | 369 | 369 | 250 | 252 |
| definitions needed to unfold them fully | 3,240 | 3,245 | 2,126 | 2,127 |

## Relaxations (two primary roots)

### ns_r3

(a) Library layer cut out, dominators recomputed. "Lost" = declarations reached only through the library, which no longer belong to any region.

| library = | library decls | lost decls | hub children | chapters | chapter mass, % of original | 40 heaviest heads, % of original |
|---|---|---|---|---|---|---|
| (none, baseline) | 0 | 0 | 8,599 | 61 | 65.0 | 63.4 |
| users>=200 | 143 | 3,408 | 7,524 | 67 | 44.0 | 41.2 |
| users>=100 | 339 | 3,501 | 7,262 | 66 | 43.8 | 41.2 |
| users>=50 | 788 | 3,556 | 6,729 | 66 | 44.2 | 41.6 |
| users>=20 | 2,044 | 3,939 | 5,578 | 62 | 43.2 | 41.3 |
| users>=10 | 3,907 | 4,073 | 4,580 | 66 | 34.6 | 32.1 |
| users>=5 | 6,898 | 5,170 | 1,621 | 38 | 37.0 | 37.7 |
| users>=3 | 10,213 | 9,558 | 14 | 3 | 17.8 | 17.9 |
| all non-theorems | 6,688 | 6,028 | 2,987 | 37 | 26.6 | 27.6 |

(b) Cuts made of 2 or 3 chapter statements. 35.0% of the mass (11,730 declarations) lies outside the chapters; of it:

| where it sits | declarations | % of all mass |
|---|---|---|
| cut needs 4 or more chapters | 1,225 | 4.2 |
| cut of 2 chapters | 1,545 | 5.8 |
| cut of 3 chapters | 903 | 3.9 |
| reached from the hub or spine without passing a chapter | 8,057 | 21.1 |

81 distinct pairs and 68 distinct triples occur. The best 5 pairs add 2.9% of the mass, the best 20 add 5.1%; the best 5 triples 2.4%. Best pairs:

- `NavierStokes.ActualCandidateAssembly.selected_witness` + `NavierStokes.ActualCyclePreservation.state_runInvariant`: +1.04% (251 declarations)
- `NavierStokes.ActualCandidateAssembly.selected_witness` + `NavierStokes.ActualCyclePreservation.particularData`: +0.67% (203 declarations)
- `NavierStokes.ActualCyclePreservation.particularData` + `NavierStokes.ActualCyclePreservation.waveData_of_particular`: +0.43% (75 declarations)
- `NavierStokes.ActualCandidateAssembly.selected_witness` + `NavierStokes.ActualCyclePreservation.waveData_of_particular`: +0.43% (122 declarations)
- `NavierStokes.ActualCandidateAssembly.selected_witness` + `NavierStokes.ActualCycleCoherence.waves`: +0.29% (91 declarations)

(b') Object-plus-statements cuts: a non-theorem declaration together with the 1 to 10 declarations whose statements mention it. 4,346 candidates; 1149 cut off something that no single member dominates, 516 of them something outside every chapter. Outside the chapters, all such regions together (they overlap) hold 6.3% of the mass (1,835 declarations). Choosing interfaces greedily: the best 5 add 1.6% (42 statements to trust); the best 10 add 2.4% (83 statements to trust); the best 20 add 3.4% (167 statements to trust); the best 40 add 4.4% (320 statements to trust). Best by new mass outside the chapters:

| object | statements in the interface | new mass outside chapters, % |
|---|---|---|
| `NavierStokes.ActualParticularCycleData.Data` | 10 | 0.53 |
| `NavierStokes.TerminalCone.profilePoint` | 10 | 0.38 |
| `NavierStokes.ActualParticularStageControls.selectedPatch` | 7 | 0.26 |
| `NavierStokes.LinearWaveBounds.WaveCoefficients.goodCoefficient` | 4 | 0.24 |
| `NavierStokes.LeadingStressWeights.logStress` | 11 | 0.18 |
| `NavierStokes.CorrectionAnalyticStep.StepData` | 7 | 0.18 |
| `NavierStokes.FirstOrderBaseEdge.terminalShift` | 9 | 0.17 |
| `NavierStokes.ActualPrimaryCovariance.partitionFactor` | 7 | 0.16 |

(c) Definitions as dominators: 27 non-theorem declarations dominate 20+ declarations; the 11 maximal ones cover 39.5% of the mass. Module quotient graph: 581 modules, hub module `NavierStokes.R3.ActualCandidate` has 362 children of which 337 dominate no other module (73.2% of mass); heads dominating 5+ modules: 2, covering 10.5%.

| definition | mass % | declarations dominated | statement chars |
|---|---|---|---|
| `NavierStokes.CorrectionInitialization.ActualPrimary.profile` (def) | 23.17 | 3,010 | 100 |
| `NavierStokes.ActualCandidateAssembly.estimates` (def) | 9.15 | 2,536 | 492 |
| `NavierStokes.ActualSlowAxis.hierarchy` (def) | 3.39 | 503 | 567 |
| `NavierStokes.CorrectionInitialization.ActualPrimary.choice` (def) | 2.27 | 359 | 137 |
| `NavierStokes.ActualParticularStageControls.selectedActualControl` (def) | 0.59 | 46 | 1817 |
| `NavierStokes.ActualCyclePreservation.stepData_of_particular` (def) | 0.27 | 106 | 1369 |
| `NavierStokes.NominalProfile.Witness.profiles` (def) | 0.20 | 60 | 183 |
| `NavierStokes.CorrectionInitialization.ActualPrimary.slots` (def) | 0.15 | 34 | 398 |

(d) Different method, not dominators: Louvain (networkx, seed 1) on the undirected graph after removing nodes with >= 50 users. 28 communities, modularity 0.83. The median community has 169 entry points (members used from outside it), so there is no single statement to trust. Louvain is randomised; counts move by a community or two between runs.

| declarations | mass % | entry points | modules | most common module | share inside one dominator chapter |
|---|---|---|---|---|---|
| 1,694 | 9.4 | 272 | 50 | `NavierStokes.OutgoingEntranceCone` | 58% in `profile` |
| 886 | 8.0 | 145 | 30 | `NavierStokes.NominalProfile` | 43% in `profile` |
| 1,719 | 7.2 | 611 | 114 | `NavierStokes.ActualPrimaryCoherence` | 13% in `selected_witness` |
| 1,343 | 6.6 | 254 | 49 | `NavierStokes.TransitionRamp` | 44% in `profile` |
| 1,372 | 5.6 | 322 | 86 | `NavierStokes.BaseResidual` | 41% in `selected_witness` |
| 744 | 4.9 | 200 | 48 | `NavierStokes.MovingFrameODE` | 20% in `choice` |
| 503 | 4.9 | 77 | 17 | `NavierStokes.ExtendedHeatDebts` | 20% in `profile` |
| 473 | 4.4 | 100 | 18 | `NavierStokes.PulseCone` | 72% in `profile` |

### euler_r3

(a) Library layer cut out, dominators recomputed. "Lost" = declarations reached only through the library, which no longer belong to any region.

| library = | library decls | lost decls | hub children | chapters | chapter mass, % of original | 40 heaviest heads, % of original |
|---|---|---|---|---|---|---|
| (none, baseline) | 0 | 0 | 5,846 | 54 | 42.1 | 40.4 |
| users>=200 | 62 | 0 | 5,783 | 54 | 42.1 | 40.4 |
| users>=100 | 139 | 10 | 5,688 | 54 | 42.2 | 40.5 |
| users>=50 | 303 | 34 | 5,506 | 57 | 43.0 | 40.6 |
| users>=20 | 844 | 222 | 4,835 | 56 | 43.2 | 41.0 |
| users>=10 | 1,779 | 1,137 | 3,451 | 51 | 37.5 | 36.7 |
| users>=5 | 3,529 | 5,447 | 329 | 10 | 27.0 | 29.6 |
| users>=3 | 5,499 | 6,802 | 40 | 3 | 4.0 | 4.7 |
| all non-theorems | 4,256 | 4,321 | 832 | 12 | 29.5 | 32.1 |

(b) Cuts made of 2 or 3 chapter statements. 57.9% of the mass (8,679 declarations) lies outside the chapters; of it:

| where it sits | declarations | % of all mass |
|---|---|---|
| cut needs 4 or more chapters | 999 | 5.9 |
| cut of 2 chapters | 657 | 4.8 |
| cut of 3 chapters | 660 | 4.5 |
| reached from the hub or spine without passing a chapter | 6,363 | 42.7 |

54 distinct pairs and 41 distinct triples occur. The best 5 pairs add 3.3% of the mass, the best 20 add 4.5%; the best 5 triples 2.8%. Best pairs:

- `EulerPacketInduction.Stage.chooseJoined` + `EulerParentPacketFrames.LabelData.forward_uniform_child`: +1.63% (223 declarations)
- `EulerPacketInduction.Stage.forwardNext` + `EulerPacketInduction.Stage.joinedNext`: +0.52% (66 declarations)
- `EulerPacketCylinderField.joinedSource_profile_budgets` + `EulerPacketInduction.Stage.chooseJoined`: +0.46% (42 declarations)
- `EulerPacketInduction.Stage.chooseJoined` + `EulerPacketInitial.actual_increment_summable`: +0.41% (54 declarations)
- `EulerPacketInduction.Stage.chooseJoined` + `EulerPacketTerminalDatum.joinedTerminalPrimary_budget`: +0.28% (21 declarations)

(b') Object-plus-statements cuts: a non-theorem declaration together with the 1 to 10 declarations whose statements mention it. 2,828 candidates; 779 cut off something that no single member dominates, 556 of them something outside every chapter. Outside the chapters, all such regions together (they overlap) hold 14.7% of the mass (2,233 declarations). Choosing interfaces greedily: the best 5 add 5.0% (42 statements to trust); the best 10 add 7.0% (77 statements to trust); the best 20 add 9.1% (154 statements to trust); the best 40 add 11.3% (319 statements to trust). Best by new mass outside the chapters:

| object | statements in the interface | new mass outside chapters, % |
|---|---|---|
| `EulerPacketCylinderField.joinedCoefficientBudget` | 11 | 1.77 |
| `EulerChildParticleFieldBounds.Data.childAcceleration` | 10 | 1.59 |
| `EulerPacketInduction.stages` | 8 | 0.60 |
| `EulerMeanSourceInverse.sourceMeanSolver` | 8 | 0.59 |
| `EulerPacketInduction.Stage.forwardNext` | 5 | 0.49 |
| `EulerTransverseFixedEvolution.velocityPath` | 11 | 0.42 |
| `EulerBaseDatum.solutionParent` | 7 | 0.40 |
| `EulerParentPacketFrames.LabelData.geometryInputs` | 3 | 0.39 |

(c) Definitions as dominators: 38 non-theorem declarations dominate 20+ declarations; the 25 maximal ones cover 11.1% of the mass. Module quotient graph: 1,743 modules, hub module `Euler.Solution` has 1,153 children of which 938 dominate no other module (61.1% of mass); heads dominating 5+ modules: 30, covering 16.3%.

| definition | mass % | declarations dominated | statement chars |
|---|---|---|---|
| `EulerPacketInduction.Stage.chooseJoined` (def) | 1.57 | 94 | 406 |
| `EulerPacketInduction.constructionScales` (def) | 1.13 | 93 | 81 |
| `EulerPacketInduction.Stage.joinedNext` (def) | 0.79 | 83 | 417 |
| `EulerParentPacketFrames.Evolution.child` (def) | 0.73 | 100 | 1422 |
| `EulerPacketSourceGeometry.Guards.geometryData` (def) | 0.69 | 53 | 524 |
| `EulerPacketInductionScales.Scales.firstStage` (def) | 0.64 | 58 | 133 |
| `EulerParentPacketFrames.SmoothState.packetChild` (def) | 0.62 | 84 | 1702 |
| `EulerPacketInduction.Stage.forwardNext` (def) | 0.49 | 45 | 391 |

(d) Different method, not dominators: Louvain (networkx, seed 1) on the undirected graph after removing nodes with >= 50 users. 29 communities, modularity 0.81. The median community has 93 entry points (members used from outside it), so there is no single statement to trust. Louvain is randomised; counts move by a community or two between runs.

| declarations | mass % | entry points | modules | most common module | share inside one dominator chapter |
|---|---|---|---|---|---|
| 930 | 9.7 | 152 | 218 | `Euler.SobolevSmoothing` | 55% in `finite_exists` |
| 595 | 8.3 | 95 | 87 | `Euler.EulerProof` | 51% in `exists_geometry` |
| 739 | 8.0 | 169 | 122 | `Euler.TerminalTimePrimitive` | 20% in `selection` |
| 742 | 8.0 | 190 | 115 | `Euler.LpCylinderRectangular` | 10% in `source_forward_block_bound` |
| 1,221 | 7.7 | 199 | 289 | `Euler.MeanPacketForcing` | 6% in `forward_uniform_child` |
| 751 | 6.9 | 187 | 108 | `Euler.EulerProof` | 32% in `finite_exists` |
| 793 | 5.3 | 241 | 149 | `Euler.CylinderScalarPrimitive` | 4% in `forward_uniform_child` |
| 697 | 5.3 | 251 | 132 | `Euler.EulerProof` | 4% in `ofPath` |

## Navier-Stokes: where the paper's steps sit relative to the chapters

Modules are assigned to a step of the paper by filename keyword (the second reader's mapping, rough by construction). "Outside" = share of the step's proof mass that lies under no chapter.

| paper step (keywords) | modules | % of all mass | outside every chapter | chapters holding most of the rest |
|---|---|---|---|---|
| Moment matching (App. A.1 / B.8) (MomentRepair, FiveProfileMoments, PowerMomentMatrix) | 5 | 5.7 | 11% | `exists_normalized_repair` 86%, `profile` 3% |
| Axis profile and series (App. B) (AxisProfile, AxisSeries, PositiveAxis) | 4 | 2.4 | 2% | `hierarchy` 85%, `profile` 13% |
| Admissible stress cone (Sec. 4.3, App. C) (Cone) | 16 | 7.8 | 7% | `profile` 85%, `choice` 7%, `log_stocks` 1% |
| Loop data (App. C.1) (Loop) | 4 | 0.7 | 65% | `profile` 35% |
| Coefficient induction (Sec. 5) (SlowRecursion, SlowAxis, SlowBase) | 6 | 1.0 | 52% | `hierarchy` 27%, `selected_witness` 17%, `choice` 1% |
| Torus charts (Sec. 6) (Torus, Chart, Slot) | 12 | 1.8 | 68% | `selected_witness` 14%, `slots` 7%, `choice` 5% |
| Phases and pulses (Sec. 7.1-7.2) (Phase, Pulse) | 16 | 6.5 | 33% | `profile` 54%, `choice` 5%, `selected_witness` 3% |
| Covariance, oscillatory stress (Sec. 7.3, Prop. 7.5) (Covariance) | 10 | 1.4 | 25% | `choice` 40%, `selected_witness` 20%, `matched_fluxes` 10% |
| Mean corrections (Sec. 8) (Mean, AnglePrimitive, Primitive) | 34 | 5.7 | 55% | `selected_witness` 17%, `step` 12%, `meanClass_compactPrimitive` 5% |
| Correction cycle (Sec. 9) (Correction, Cycle) | 17 | 3.1 | 55% | `step` 16%, `selected_witness` 11%, `particularData` 4% |
| Localisation (Sec. 10.1) (Localization) | 4 | 0.2 | 37% | `selected_witness` 55%, `of_localized_fields` 8% |
| Force limits (Sec. 10.2) (ResidualLimits, ForceDecay, BoundaryLimit) | 4 | 0.1 | 33% | `selected_witness` 43%, `comparator_of_breakdown` 25% |
| Comparison and energy (Sec. 10.3) (.R3.) | 72 | 3.0 | 6% | `no_global_solution_one` 89%, `of_localized_fields` 5%, `comparator_of_breakdown` 1% |

## Ratings of the heaviest chapter statements

First reader (the agent that built the outline), after reading the source around each declaration; a second reader agreed on all 15 originally rated, though not blind. milestone = a recognisable intermediate mathematical milestone; restatement = the headline theorem again, minus a side condition; waypoint = a sensible technical waypoint (readable as printed, or opaque: its content is in a structure defined elsewhere); unreadable = arbitrary or unreadable as a statement.

| root | statement | mass % | hidden | chars | rating | why |
|---|---|---|---|---|---|---|
| ns_r3 | `NavierStokes.CorrectionInitialization.ActualPrimary.profile` | 23.17 | 3,009 | 100 | **waypoint-opaque** | An abbreviation for `FinalSlowBase.actualProfile := Classical.choice profileData_nonempty`: the one self-similar profile fixed for the whole construction. Sensible place to cut, but the statement shown is only `: ProfileData`; what is being trusted is a six-field structure (outgoing profile, nominal witness, cone certificate, loop data, modulation witness, full cone) that must be unfolded to mean anything. |
| ns_r3 | `NavierStokes.ActualCandidateAssembly.selected_witness` | 13.81 | 4,072 | 297 | **waypoint-opaque** | Says the selected budget and threshold give a `Witness`: a schedule whose three stage sums (potential, direct, pressure) define a velocity, pressure and smooth forcing with `CandidateProperties` and the strong `Consequences`. This is the candidate-construction step of the paper, but the printed statement names only three constants; the content sits in a 25-line `def Witness : Prop`. |
| ns_r3 | `NavierStokes.FiveProfileMoments.exists_normalized_repair` | 4.96 | 21 | 550 | **waypoint-readable** | The most readable chapter: a quantitative inverse-function statement (a smooth local right inverse `g` of the normalised moment map near 0, with `‖g d‖ ≤ C‖d‖`, bounded derivative and a positivity side condition). A lemma, not a milestone; its 5% mass comes from a few very large proofs (it hides only 21 declarations). |
| ns_r3 | `NavierStokes.ActualSlowAxis.hierarchy` | 3.39 | 502 | 567 | **waypoint-opaque** | Builds the `LocalHierarchy` of slow-order coefficient functions from one base profile (structure docstring: 'the output, not a hypothesis'). The source gives no return type; the printed one is elaborator output with seven nested project terms as indices. |
| ns_r3 | `NavierStokesR3.ProblemStatement.CandidateProperties.no_global_solution_one` | 2.70 | 655 | 435 | **milestone** | Added after review (it hangs off a spine node, not the hub, and was missed by the first chapter definition). `CandidateProperties 1 u p f K → ¬ Nonempty (GlobalFiniteEnergySolution 1 f)`: any candidate with the listed properties at viscosity 1 excludes a global finite-energy solution for its force. This is the paper's comparison step (Section 10.3): weak-strong uniqueness makes a global solution agree with the candidate before time one, and the candidate's speed is unbounded on a compact set. Short, has a docstring, and uses only the vocabulary of the headline theorem. |
| ns_r3 | `NavierStokes.CorrectionInitialization.ActualPrimary.choice` | 2.27 | 358 | 137 | **waypoint-opaque** | `Classical.choice` of `Choice B N0`: prepared primary geometry plus three positive constants and a covariance bound. Reasonable boundary, uninformative statement (`: Choice B N0`). |
| ns_r3 | `NavierStokes.CorrectionAnalyticStep.step` | 1.57 | 400 | 1366 | **waypoint-readable** | The analytic induction step: from the cycle invariant at exponent σ and the step data, the invariant at σ+1/10 plus increment bounds (`StepResult`). Recognisable as the step of an iteration, with a docstring, but printed with 20 implicit parameters before the two-line content. |
| ns_r3 | `NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile` | 1.08 | 198 | 1326 | **unreadable** | Three identities equating `forwardTheta`, `forwardAxial`, `radialA` with profile stresses on a closed log-domain. A matching identity inside the terminal-cone analysis; nothing in the statement tells a reader why it matters. |
| ns_r3 | `NavierStokes.ActualCyclePreservation.state_runInvariant` | 1.03 | 307 | 297 | **milestone** | Every stage `j` of the fixed construction satisfies `RunInvariant (sigma j)`: the main induction of the iteration, proved by a five-line `induction j`. Short statement, docstring, and the natural thing to trust. |
| euler_r3 | `EulerAllOrderDriftCorrection.finite_exists` | 8.90 | 797 | 1512 | **waypoint-opaque** | Existence of a finite-order inviscid correction: a continuous path in a Sobolev space, zero at t=0, divergence-free, with two Gevrey-energy bounds, solving the linearised evolution equation. A genuine existence theorem with a docstring, but 1,500 characters and readable only with the `Data`/`Budget` structures in hand. |
| euler_r3 | `EulerPacketMovingFrame.PhysicalGeometryData.exists_geometry` | 6.43 | 313 | 213 | **unreadable** | `∃ F F₁ Z Z₁, PhysicalGeometryConclusion D F F₁ Z Z₁`. Short, but hypothesis and conclusion are two structures of dozens of fields with constants such as `8232*exp 9*Θ^5` and `30000000*neighborStabilityConstant`; the statement is a pointer to a page of estimates. |
| euler_r3 | `Euler.initialDatum_no_global_solution (private)` | 3.89 | 703 | 130 | **restatement** | The constructed initial datum admits no global smooth solution: `¬∃ v p, EulerExistenceAndSmoothnessR3 initialDatum.field v p`. This is the headline theorem minus the regularity and decay of the datum; the root's proof is a one-line tuple ending in this lemma, so trusting it is trusting the theorem. Counted as a restatement, not an intermediate milestone (second reader's finding). It dominates only 3.9% of the mass. |
| euler_r3 | `EulerParentPacketFrames.LabelData.forward_uniform_child` | 2.18 | 165 | 4007 | **unreadable** | 4,007 characters; some twenty section variables as hypotheses and a conclusion of nested existentials over budgets and graph-flow data. Not a statement anyone can take on trust by reading it. |
| euler_r3 | `EulerPacketSourceGeometry.Guards.selection` | 1.82 | 151 | 1261 | **unreadable** | Existence of a terminal vector ξ and slope λ normalising a scaled ray to `![0,0,1]` and two scaled-velocity components to `-λ` and `1`. A parameter-selection lemma whose meaning depends entirely on surrounding definitions. |
| euler_r3 | `EulerPacketInduction.Stage.chooseJoined` | 1.57 | 93 | 406 | **waypoint-opaque** | `Classical.choice` of a `GeometryJoinedChoice` for stage `n`: the choice made in the successor step of the packet induction. Right place for a boundary; the statement is only the name of a structure. |
| euler_r3 | `EulerPacketInduction.constructionScales` | 1.13 | 92 | 81 | **waypoint-opaque** | `Classical.choice (exists_scales ...)`: the scale sequence used by the whole infinite construction. Short and sensible; again the content is the `Scales` structure, not the statement. |

Tally by count (16 rated): 7 waypoint-opaque, 4 unreadable, 2 waypoint-readable, 2 milestone, 1 restatement.

Mass-weighted (share of all proof mass below the root that sits under rated statements of each class):

| class | ns_r3 | euler_r3 |
|---|---|---|
| intermediate milestone, readable as printed | 3.7% | 0.0% |
| technical waypoint, readable as printed | 6.5% | 0.0% |
| waypoint whose content is in a structure defined elsewhere | 42.6% | 11.6% |
| restatement of the headline theorem | 0.0% | 3.9% |
| unreadable or arbitrary | 1.1% | 10.4% |

# Outlines

The two primary roots are printed with statements (trimmed to 420 characters). The other two share almost all of their graph with them and are printed as names only.


## NavierStokes.Comparator.navier_stokes_breakdown_R3

Navier-Stokes Theorem 1.1, Clay alternative (C): breakdown on R^3. Reaches 23,747 declarations, proof mass 24,565,760.

```lean
NavierStokes.Comparator.navier_stokes_breakdown_R3 (nu : ℝ) (hnu : nu > 0) :
  ∃ u₀ f,
    NavierStokes.Comparator.InitialVelocityConditionDecay u₀ ∧
      NavierStokes.Comparator.ForceConditionDecay f ∧
        ¬∃ v p, NavierStokes.Comparator.NavierStokesExistenceAndSmoothnessRn nu u₀ f v p
```

**Spine** (each statement is the only way into the one before it and carries at least 90% of its mass):

1. `NavierStokes.ComparatorBridge.navier_stokes_breakdown_R3` (theorem, `NavierStokes.ComparatorR3Theorem:37`), 100.0% of mass, 23,739 declarations beneath, 32 tree children
   ```lean
   NavierStokes.ComparatorBridge.navier_stokes_breakdown_R3 (ν : ℝ) (hν : ν > 0) : ∃ u₀ f, NavierStokes.Comparator.InitialVelocityConditionDecay u₀ ∧ NavierStokes.Comparator.ForceConditionDecay f ∧ ¬∃ v p, NavierStokes.Comparator.NavierStokesExistenceAndSmoothnessRn ν u₀ f v p
   ```
2. `NavierStokesR3.theorem_1_1` (theorem, `NavierStokes.R3.Theorem:44`), 99.9% of mass, 23,687 declarations beneath, 2 tree children
   ```lean
   NavierStokesR3.theorem_1_1 : NavierStokesR3.ProblemStatement.breakdownStatement
   ```
3. `NavierStokesR3.theorem_1_1_with_initial_rest` (theorem, `NavierStokes.R3.Theorem:24`), 99.9% of mass, 23,685 declarations beneath, 48 tree children
   ```lean
   NavierStokesR3.theorem_1_1_with_initial_rest (ν : ℝ) (hν : 0 < ν) : ∃ u p f K, NavierStokesR3.ProblemStatement.CandidateProperties ν u p f K ∧ ¬Nonempty (NavierStokesR3.ProblemStatement.GlobalFiniteEnergySolution ν f) ∧ ∀ (t : ℝ), |t| ≤ 3 / 8 → ∀ (x : NavierStokesR3.ProblemStatement.Space), u (t, x) = 0 ∧ p (t, x) = 0
   ```
4. `NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest` (theorem, `NavierStokes.R3.ActualCandidate:141`), 96.9% of mass, 22,958 declarations beneath, 8599 tree children
   ```lean
   NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest : ∃ u p f K, NavierStokesR3.ProblemStatement.CandidateProperties 1 u p f K ∧ ∀ (t : ℝ), |t| ≤ 3 / 8 → ∀ (x : NavierStokes.ProblemStatement.Space), u (t, x) = 0 ∧ p (t, x) = 0
   ```

**Hub** `NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest` has 8,599 dominator-tree children; 7,448 of them dominate nothing but themselves.

The spine nodes above the hub have 86 further children of their own (side branches such as the comparison argument); they are chapter candidates too.

**Outline** (40 statements; mass = share of all proof mass below the root that sits under the statement, itself included; hidden = declarations a reader skips by trusting it):

- `NavierStokes.CorrectionInitialization.ActualPrimary.profile` (def) | mass 23.17% | hidden 3,009 decls | statement 100 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.FinalSlowBase.actualProfile` → `NavierStokes.FinalSlowBase.profileData_nonempty` → `NavierStokes.NominalConeAssembly.exists_nominal_cone`
  ```lean
  NavierStokes.CorrectionInitialization.ActualPrimary.profile : NavierStokes.FinalSlowBase.ProfileData
  ```
  _An abbreviation for `FinalSlowBase.actualProfile := Classical.choice profileData_nonempty`: the one self-similar profile fixed for the whole construction. Sensible place to cut, but the statement shown is only `: ProfileData`; what is being trusted is a six-field structure (outgoing profile, nominal witness, cone certificate, loop data, modulation witness, full cone) that must be unfolded to mean anything._
  - `NavierStokes.NominalConeAssembly.exists_certificate` (theorem, doc) | mass 11.38% | hidden 1,424 decls | statement 161 chars
    ```lean
    NavierStokes.NominalConeAssembly.exists_certificate (d : NavierStokes.PreparedOutgoing.PreparedProfile) : ∃ W, NavierStokes.NominalConeAssembly.Certificate W
    ```
    - `NavierStokes.NominalConeAssembly.assembly_exists` (theorem) | mass 9.49% | hidden 1,073 decls | statement 161 chars
      ```lean
      NavierStokes.NominalConeAssembly.assembly_exists (d : NavierStokes.PreparedOutgoing.PreparedProfile) : Nonempty (NavierStokes.NominalConeAssembly.Assembly d)
      ```
    - `NavierStokes.NominalConeAssembly.Assembly.certificate` (theorem, doc) | mass 0.88% | hidden 132 decls | statement 218 chars
      ```lean
      NavierStokes.NominalConeAssembly.Assembly.certificate {d : NavierStokes.PreparedOutgoing.PreparedProfile} (A : NavierStokes.NominalConeAssembly.Assembly d) : NavierStokes.NominalConeAssembly.Certificate A.witness
      ```
  - `NavierStokes.PreparedOutgoing.exists_prepared` (theorem, doc) | mass 9.53% | hidden 1,039 decls | statement 104 chars
    ```lean
    NavierStokes.PreparedOutgoing.exists_prepared : Nonempty NavierStokes.PreparedOutgoing.PreparedProfile
    ```
    - `NavierStokes.OutgoingCone.exists_ordered_profile_cone` (theorem, doc) | mass 5.64% | hidden 715 decls | statement 1158 chars
      - _passes through:_ `NavierStokes.OutgoingCone.exists_ordered_clean_cone`
      ```lean
      NavierStokes.OutgoingCone.exists_ordered_profile_cone : ∃ M, 0 < M ∧ ∀ (m : ℝ), M ≤ m → ∀ (P : ℝ), NavierStokes.OutgoingEntranceCone.amplitudeThreshold m ≤ P → ∀ (K : ℝ), 0 < K → ∃ lam0, 0 < lam0 ∧ ∀ (F : NavierStokes.OutgoingProfile.Profile), F.data.core.P = P → F.data.core.m = m → F.coefficientBound = K → F.data.core.wait = 60 * Real.log (1 / F.data.core.lam) → F.data.core.lam < lam0 → F.data.h ≤ NavierStokes.Outgo ...
      ```
    - `NavierStokes.ScheduledProfileChoice.exists_scheduled_family_below` (theorem, doc) | mass 1.95% | hidden 89 decls | statement 1257 chars
      - _passes through:_ `NavierStokes.ScheduledProfileChoice.exists_scheduled_core_below` → `NavierStokes.UniformAngularReset.exists_scheduled_reset`
      ```lean
      NavierStokes.ScheduledProfileChoice.exists_scheduled_family_below (P m : ℝ) (hP : 0 < P) (hm : 0 < m) (cap : ℝ → ℝ) (hcap : ∀ (K : ℝ), 0 < K → 0 < cap K) (extraHeight : NavierStokes.OutgoingSchedule.Parameters → ℝ) (hextra : ∀ (core : NavierStokes.OutgoingSchedule.Parameters), 0 < extraHeight core) : ∃ K B H core, 0 < K ∧ 0 < B ∧ 0 < H ∧ core.P = P ∧ core.m = m ∧ core.wait = 60 * Real.log (1 / core.lam) ∧ core.lam < ...
      ```
- `NavierStokes.ActualCandidateAssembly.selected_witness` (theorem) | mass 13.81% | hidden 4,072 decls | statement 297 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.ActualCandidateAssembly.witness`
  ```lean
  NavierStokes.ActualCandidateAssembly.selected_witness : NavierStokes.ActualCandidateAssembly.Witness NavierStokes.ActualCandidateConstruction.selectedBudget NavierStokes.ActualCandidateConstruction.selectedThreshold NavierStokes.ActualCandidateConstruction.selectedThreshold_geometry
  ```
  _Says the selected budget and threshold give a `Witness`: a schedule whose three stage sums (potential, direct, pressure) define a velocity, pressure and smooth forcing with `CandidateProperties` and the strong `Consequences`. This is the candidate-construction step of the paper, but the printed statement names only three constants; the content sits in a 25-line `def Witness : Prop`._
  - `NavierStokes.ActualCandidateAssembly.estimates` (def) | mass 9.15% | hidden 2,535 decls | statement 492 chars
    ```lean
    NavierStokes.ActualCandidateAssembly.estimates (B N0 : ℕ) (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0) : NavierStokes.MixedCandidateAssembly.StageEstimates NavierStokes.CorrectionInitialization.ActualPrimary.h (NavierStokes.ActualCandidateConstruction.qbig B N0) (NavierStokes.ActualCandidateAssembly.potentialStages B N0 hN) (NavierStokes.ActualCandidateAssembly.directStages B N0 hN) (NavierStokes ...
    ```
    - `NavierStokes.GluedStageEstimates.actualStageEstimates` (def, doc) | mass 5.72% | hidden 1,230 decls | statement 1341 chars
      ```lean
      NavierStokes.GluedStageEstimates.actualStageEstimates.{u_1, u_2} {B N0 N : ℕ} (R : NavierStokes.ActualStageEstimates.RunData B N0) {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I : Type u_1} {K : Type u_2} (M : NavierStokes.ActualMeanPhysicalData.InitialCycleInput B N0 N fun x => NavierStokes.ActualCycleParameters.fixedParameters B N0) (hN : 4 ≤ N) (W : NavierStokes.GluedStageEstimates.SignedInputs D I K) (C : ...
      ```
    - `NavierStokes.ActualCandidateAssembly.physicalData` (theorem) | mass 1.92% | hidden 674 decls | statement 642 chars
      ```lean
      NavierStokes.ActualCandidateAssembly.physicalData (B N0 : ℕ) (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0) (J : ℕ) : NavierStokes.ActualCycleResidualBounds.PhysicalData B (NavierStokes.ActualCandidateConstruction.residualBand B N0) (NavierStokes.ActualCandidateConstruction.cycle B N0 J).state (NavierStokes.MixedDiagonalResidual.uncutVelocity (NavierStokes.ActualCandidateAssembly.potentialStages B ...
      ```
  - `NavierStokes.GermCandidateAssembly.exists_candidate_witness_of_finite_stages` (theorem, doc) | mass 1.35% | hidden 467 decls | statement 6382 chars
    ```lean
    NavierStokes.GermCandidateAssembly.exists_candidate_witness_of_finite_stages {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W) {ld : NavierStokes.ModulatedProfileAssembly.LoopData W} (v : NavierStokes.ModulatedProfileAssembly.Witness ld) (upper : ℝ) (bandFloor : ℕ) {qbig C : ℝ} (hqbig : 0 < qbig) (initial : NavierStokes.ProblemS ...
    ```
    - `NavierStokes.CandidateConsequences.mixed_exists_force_with_consequences` (theorem, doc) | mass 0.73% | hidden 280 decls | statement 2893 chars
      ```lean
      NavierStokes.CandidateConsequences.mixed_exists_force_with_consequences {A v : NavierStokes.ProblemStatement.VelocityField} {p : NavierStokes.ProblemStatement.PressureField} (hA : ContDiffOn ℝ (↑⊤) A (NavierStokes.SpacetimeEndpoint.openPast 1)) (hv : ContDiffOn ℝ (↑⊤) v (NavierStokes.SpacetimeEndpoint.openPast 1)) (hp : ContDiffOn ℝ (↑⊤) p (NavierStokes.SpacetimeEndpoint.openPast 1)) (hd : ∀ t < 1, ∀ (x : NavierStoke ...
      ```
- `NavierStokes.FiveProfileMoments.exists_normalized_repair` (theorem, doc) | mass 4.96% | hidden 21 decls | statement 550 chars **[waypoint-readable]**
  ```lean
  NavierStokes.FiveProfileMoments.exists_normalized_repair (P : NavierStokes.FiveProfileMoments.Patch) (b : ℝ) (hb : NavierStokes.FiveProfileMoments.GoodExponent b) : ∃ g ε C, 0 < ε ∧ 0 < C ∧ ContDiffOn ℝ (↑⊤) g (Metric.ball 0 ε) ∧ g 0 = 0 ∧ ∀ d ∈ Metric.ball 0 ε, NavierStokes.FiveProfileMoments.normalizedMap P b (g d) = d ∧ ‖g d‖ ≤ C * ‖d‖ ∧ ‖fderiv ℝ g d‖ ≤ C ∧ ∀ (x : ℝ), 0 < x → 0 < x ^ b + NavierStokes.FiveProfileM ...
  ```
  _The most readable chapter: a quantitative inverse-function statement (a smooth local right inverse `g` of the normalised moment map near 0, with `‖g d‖ ≤ C‖d‖`, bounded derivative and a positivity side condition). A lemma, not a milestone; its 5% mass comes from a few very large proofs (it hides only 21 declarations)._
- `NavierStokes.ActualSlowAxis.hierarchy` (def) | mass 3.39% | hidden 502 decls | statement 567 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.SlowRecursion.buildLocalHierarchy`
  ```lean
  NavierStokes.ActualSlowAxis.hierarchy {N : NavierStokes.ReferencePath.Input} {h R : ℝ} {P0 : ℝ → ℝ} {Ω : Set ℂ} (E : NavierStokes.ActivationHolomorphic.InitialTube N h P0 R Ω) {T δ : ℝ} (hT : 0 < T) (hδ : 0 < δ) (hδT : 2 * δ < NavierStokes.ReferencePath.rampLimit) (κ : ℝ) (hP0 : ContDiff ℝ (↑⊤) P0) (C : ℝ) : NavierStokes.SlowRecursion.LocalHierarchy (NavierStokes.ActualSlowAxis.axisRadius N δ) (NavierStokes.ActualSlo ...
  ```
  _Builds the `LocalHierarchy` of slow-order coefficient functions from one base profile (structure docstring: 'the output, not a hypothesis'). The source gives no return type; the printed one is elaborator output with seven nested project terms as indices._
  - `NavierStokes.SlowRecursion.sequence_positive_order` (theorem, doc) | mass 1.04% | hidden 121 decls | statement 1662 chars
    - _passes through:_ `NavierStokes.SlowRecursion.sequence_expanded` → `NavierStokes.SlowRecursion.step_expanded`
    ```lean
    NavierStokes.SlowRecursion.sequence_positive_order {core buffer : ℝ} {U : Set ℂ} {h : ℝ} (c : NavierStokes.SlowRecursion.Domain (NavierStokes.SlowRecursion.radius core buffer 0) U h) (hcore : 0 < core) (hbuffer : 0 < buffer) (C : ℝ) (base : NavierStokes.SlowRecursion.Coefficient (NavierStokes.SlowRecursion.radius core buffer 0) U) {n : ℕ} (hn : 0 < n) {X eta : ℝ} (hX : X ∈ Set.Ioo 0 (core ^ 2)) (heta : ↑eta ∈ U) : ha ...
    ```
    - `NavierStokes.PositiveAxisExistence.positiveSolution_profiles_system` (theorem) | mass 0.45% | hidden 38 decls | statement 1039 chars
      ```lean
      NavierStokes.PositiveAxisExistence.positiveSolution_profiles_system {R T : ℝ} (hR : 0 < R) (hRT : R < T) {U : Set ℂ} (hU : IsOpen U) (h lam C : ℝ) {F : NavierStokes.PositiveAxisSystem.CoefficientData} (hF : NavierStokes.PositiveAxisExistence.LowerInputRegularity T U (↑h) F) {G : NavierStokes.PositiveAxisExistence.RealCoefficientData} (hreal : NavierStokes.PositiveAxisExistence.RealCompatible R U F G) {r eta : ℝ} (hr ...
      ```
  - `NavierStokes.PositiveAxisExistence.LowerInputRegularity.system` (theorem) | mass 0.52% | hidden 9 decls | statement 486 chars
    ```lean
    NavierStokes.PositiveAxisExistence.LowerInputRegularity.system {T : ℝ} {U : Set ℂ} (hU : IsOpen U) {h : ℂ} (lam C : ℂ) {F : NavierStokes.PositiveAxisSystem.CoefficientData} (hF : NavierStokes.PositiveAxisExistence.LowerInputRegularity T U h F) : NavierStokes.PositiveAxisExistence.SmoothHolomorphicSystem T U (NavierStokes.PositiveAxisSystem.coefficient0 h lam C F) (NavierStokes.PositiveAxisSystem.coefficient1 h F) (Na ...
    ```
  - `NavierStokes.PositiveAxisExistence.positiveSolution_parity` (theorem) | mass 0.50% | hidden 26 decls | statement 528 chars
    ```lean
    NavierStokes.PositiveAxisExistence.positiveSolution_parity {R T : ℝ} (hR : 0 ≤ R) (hRT : R < T) {U : Set ℂ} (hU : IsOpen U) {h : ℂ} (lam C : ℂ) {F : NavierStokes.PositiveAxisSystem.CoefficientData} (hF : NavierStokes.PositiveAxisExistence.LowerInputRegularity T U h F) {r : ℝ} (hr : r ∈ Set.Icc (-R) R) {z : ℂ} (hz : z ∈ U) : NavierStokes.PositiveAxisExistence.positiveSolution hR h lam C F (-r) z = NavierStokes.Volterr ...
    ```
- `NavierStokesR3.ProblemStatement.CandidateProperties.no_global_solution_one` (theorem, doc) | mass 2.70% | hidden 655 decls | statement 435 chars **[milestone]**
  - _passes through:_ `NavierStokesR3.WholeSpaceUniqueness.candidate_global_agrees_before_one` → `NavierStokesR3.WholeSpaceUniqueness.candidate_unique_on_Icc` → `NavierStokesR3.WholeSpaceUniqueness.classical_uniqueness_on_Icc`
  ```lean
  NavierStokesR3.ProblemStatement.CandidateProperties.no_global_solution_one {u : NavierStokesR3.ProblemStatement.VelocityField} {p : NavierStokesR3.ProblemStatement.PressureField} {f : NavierStokesR3.ProblemStatement.VelocityField} {K : Set NavierStokesR3.ProblemStatement.Space} (h : NavierStokesR3.ProblemStatement.CandidateProperties 1 u p f K) : ¬Nonempty (NavierStokesR3.ProblemStatement.GlobalFiniteEnergySolution 1 ...
  ```
  _Added after review (it hangs off a spine node, not the hub, and was missed by the first chapter definition). `CandidateProperties 1 u p f K → ¬ Nonempty (GlobalFiniteEnergySolution 1 f)`: any candidate with the listed properties at viscosity 1 excludes a global finite-energy solution for its force. This is the paper's comparison step (Section 10.3): weak-strong uniqueness makes a global solution agree with the candidate before time one, and the candidate's speed is unbounded on a compact set. Short, has a docstring, and uses only the vocabulary of the headline theorem._
  - `NavierStokesR3.PressureFlux.exists_uniform_actual_pressure_flux_bound` (theorem, doc) | mass 2.01% | hidden 475 decls | statement 1892 chars
    ```lean
    NavierStokesR3.PressureFlux.exists_uniform_actual_pressure_flux_bound {T : ℝ} {u v : NavierStokesR3.ProblemStatement.VelocityField} {p q : NavierStokesR3.ProblemStatement.PressureField} (H : NavierStokesR3.PressureRecovery.Hypotheses T u v p q) (M₀ U₀ G₀ : ℝ) (hM₀ : 0 ≤ M₀) (hU₀ : 0 ≤ U₀) (hG₀ : 0 ≤ G₀) (hM : ∀ t ∈ Set.Icc 0 T, MeasureTheory.MemLp (fun x => (u - v) (t, x)) 2 MeasureTheory.volume ∧ (NavierStokesR3.Com ...
    ```
    - `NavierStokesR3.PressureFlux.exists_uniform_canonicalCutoffFlux_bound` (theorem, doc) | mass 1.09% | hidden 227 decls | statement 1853 chars
      - _passes through:_ `NavierStokesR3.PressureFlux.canonicalCutoffFlux_bound` → `NavierStokesR3.PressureFlux.cutoff_pressurePair_bound`
      ```lean
      NavierStokesR3.PressureFlux.exists_uniform_canonicalCutoffFlux_bound (M₀ U₀ G₀ : ℝ) (hM₀ : 0 ≤ M₀) (hU₀ : 0 ≤ U₀) (hG₀ : 0 ≤ G₀) : ∃ CP, 0 ≤ CP ∧ ∀ (R : ℝ) (hR : 1 ≤ R) (u v : NavierStokesR3.ProblemStatement.VelocityField) (t : ℝ) (hu : ContDiff ℝ ↑⊤ fun x => u (t, x)) (hv : ContDiff ℝ ↑⊤ fun x => v (t, x)), MeasureTheory.MemLp (fun x => (u - v) (t, x)) 2 MeasureTheory.volume → MeasureTheory.MemLp (fun x => u (t, x)) ...
      ```
    - `NavierStokesR3.PressureFlux.actual_flux_integrable_and_le_canonicalNorm` (theorem) | mass 0.83% | hidden 216 decls | statement 785 chars
      - _passes through:_ `NavierStokesR3.PressureFlux.actual_flux_eq_canonicalCutoffFlux` → `NavierStokesR3.ActualPressureFlux.pressure_flux_eq_canonical` → `NavierStokesR3.PressureRecovery.gradient_recovery` → `NavierStokesR3.PressureRecovery.gradient_recovery_complex`
      ```lean
      NavierStokesR3.PressureFlux.actual_flux_integrable_and_le_canonicalNorm {T t R : ℝ} {u v : NavierStokesR3.ProblemStatement.VelocityField} {p q : NavierStokesR3.ProblemStatement.PressureField} (H : NavierStokesR3.PressureRecovery.Hypotheses T u v p q) (ht : t ∈ Set.Ioo 0 T) (hR : 0 < R) (hu : ContDiff ℝ ↑⊤ fun x => u (t, x)) (hv : ContDiff ℝ ↑⊤ fun x => v (t, x)) : MeasureTheory.Integrable (fun x => (p - q) (t, x) * ( ...
      ```
  - `NavierStokesR3.WholeSpaceComparisonClosure.eq_of_pressure_flux_bound` (theorem, doc) | mass 0.46% | hidden 76 decls | statement 2341 chars
    ```lean
    NavierStokesR3.WholeSpaceComparisonClosure.eq_of_pressure_flux_bound {T M G CP R₀ : ℝ} {u v : NavierStokesR3.ProblemStatement.VelocityField} {p q : NavierStokesR3.ProblemStatement.PressureField} (hT : 0 ≤ T) (hM0 : 0 ≤ M) (hG0 : 0 ≤ G) (hCP0 : 0 ≤ CP) (hu : ContDiffOn ℝ (↑⊤) u (NavierStokesR3.Comparison.slab 0 T)) (hv : ContDiffOn ℝ (↑⊤) v (NavierStokesR3.Comparison.slab 0 T)) (hp : ContDiffOn ℝ (↑⊤) p (NavierStokesR ...
    ```
- `NavierStokes.CorrectionInitialization.ActualPrimary.choice` (def) | mass 2.27% | hidden 358 decls | statement 137 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.CorrectionInitialization.ActualPrimary.choice_nonempty` → `NavierStokes.PrimaryTargetBounds.exists_constructed_bounds`
  ```lean
  NavierStokes.CorrectionInitialization.ActualPrimary.choice (B N0 : ℕ) : NavierStokes.CorrectionInitialization.ActualPrimary.Choice B N0
  ```
  _`Classical.choice` of `Choice B N0`: prepared primary geometry plus three positive constants and a covariance bound. Reasonable boundary, uninformative statement (`: Choice B N0`)._
  - `NavierStokes.PrimaryTargetBounds.exists_restricted_actual_bounds` (theorem, doc) | mass 1.21% | hidden 194 decls | statement 1577 chars
    - _passes through:_ `NavierStokes.PrimaryTargetBounds.exists_actual_bounds` → `NavierStokes.PrimaryTargetBounds.exists_prepared_bounds` → `NavierStokes.PrimaryTargetBounds.exists_family_bounds`
    ```lean
    NavierStokes.PrimaryTargetBounds.exists_restricted_actual_bounds {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W) {ld : NavierStokes.ModulatedProfileAssembly.LoopData W} (v : NavierStokes.ModulatedProfileAssembly.Witness ld) {upper : ℝ} {B : ℕ} {r0 : ℝ} {N0 : ℕ} (a : NavierStokes.PrimaryGeometryAssembly.Prepared H v upper B r0 ...
    ```
  - `NavierStokes.PrimaryGeometryAssembly.prepared` (def, doc) | mass 1.01% | hidden 147 decls | statement 588 chars
    - _passes through:_ `NavierStokes.PrimaryGeometryAssembly.exists_prepared`
    ```lean
    NavierStokes.PrimaryGeometryAssembly.prepared {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W) {ld : NavierStokes.ModulatedProfileAssembly.LoopData W} (v : NavierStokes.ModulatedProfileAssembly.Witness ld) (hcone : NavierStokes.LeadingStressWeights.FullTrueCone v) (upper : ℝ) (B : ℕ) (r0 : ℝ) (hbox : 2 * NavierStokes.NominalCon ...
    ```
    - `NavierStokes.AlignedProfileSpectralCone.modulated_representative_bounds` (theorem, doc) | mass 0.64% | hidden 80 decls | statement 3790 chars
      ```lean
      NavierStokes.AlignedProfileSpectralCone.modulated_representative_bounds {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F} {d : NavierStokes.ModulatedProfileAssembly.LoopData W} (v : NavierStokes.ModulatedProfileAssembly.Witness d) (H : NavierStokes.NominalConeAssembly.Certificate W) (hcone : NavierStokes.LeadingStressWeights.FullTrueCone v) : have K := NavierStokes.AlignedProfileS ...
      ```
- `NavierStokes.CorrectionAnalyticStep.step` (theorem, doc) | mass 1.57% | hidden 400 decls | statement 1366 chars **[waypoint-readable]**
  ```lean
  NavierStokes.CorrectionAnalyticStep.step {ι : Type} (G : NavierStokes.SignedMeanGain.Geometry) (h : ℝ) (index : ℕ → ℕ) (axial : NavierStokes.PressureStream.Plane × NavierStokes.PressureStream.Plane) (particular : ι → NavierStokes.CorrectionStep.ParticularParameters NavierStokes.CorrectionStep.CycleSlow) (signed : ι → NavierStokes.CorrectionStep.PeriodizedSignedParameters NavierStokes.CorrectionAnalyticStep.Point Navi ...
  ```
  _The analytic induction step: from the cycle invariant at exponent σ and the step data, the invariant at σ+1/10 plus increment bounds (`StepResult`). Recognisable as the step of an iteration, with a docstring, but printed with 20 implicit parameters before the two-line content._
  - `NavierStokes.CrossBasedMeanComposition.CycleParameters.mean_gain_from_waves_of_cross_defects` (theorem, doc) | mass 0.98% | hidden 235 decls | statement 11579 chars
    - _passes through:_ `NavierStokes.CrossBasedMeanComposition.fourStage_mean_gain_of_cross_defects`
    ```lean
    NavierStokes.CrossBasedMeanComposition.CycleParameters.mean_gain_from_waves_of_cross_defects {ι : Type} (G : NavierStokes.SignedMeanGain.Geometry) (h : ℝ) (index : ℕ → ℕ) (axial : NavierStokes.PressureStream.Plane × NavierStokes.PressureStream.Plane) (particular : ι → NavierStokes.CorrectionStep.ParticularParameters NavierStokes.CorrectionStep.CycleSlow) (signed : ι → NavierStokes.CorrectionStep.PeriodizedSignedParam ...
    ```
    - `NavierStokes.CrossBasedMeanComposition.bandSignedStage_mean_debt_of_cross_defects` (theorem, doc) | mass 0.83% | hidden 226 decls | statement 3430 chars
      - _passes through:_ `NavierStokes.CrossBasedMeanComposition.signed_mean_gain_of_cross_defects`
      ```lean
      NavierStokes.CrossBasedMeanComposition.bandSignedStage_mean_debt_of_cross_defects {ι : Type} (G : NavierStokes.SignedMeanGain.Geometry) (c : NavierStokes.CorrectionState.Context NavierStokes.CrossBasedMeanComposition.Point) (u : NavierStokes.CorrectionState.State NavierStokes.CrossBasedMeanComposition.Point) {P : ι → ℕ → NavierStokes.CrossBasedMeanComposition.Point → ℝ} {σ κ : ℝ} (hσ : 1 / 5 ≤ σ) (hκ : 0 ≤ κ) (hκsmal ...
      ```
- `NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile` (theorem, doc) | mass 1.08% | hidden 198 decls | statement 1326 chars **[unreadable]**
  ```lean
  NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile (F : NavierStokes.OutgoingProfile.Profile) {XR C B y η : ℝ} (hF : NavierStokes.OutgoingProfile.Specification F B) (w : NavierStokes.HeatedOutgoing.CompensationWitness F XR C) (hy : NavierStokes.TerminalCone.terminalStart F.data ≤ y) (hη : η ∈ NavierStokes.HeatedOutgoing.parameterDomain) : NavierStokes.TerminalHistoryBridge.forwardTheta F XR w.coefficients ...
  ```
  _Three identities equating `forwardTheta`, `forwardAxial`, `radialA` with profile stresses on a closed log-domain. A matching identity inside the terminal-cone analysis; nothing in the statement tells a reader why it matters._
  - `NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile_interior` (theorem, doc) | mass 0.96% | hidden 184 decls | statement 982 chars
    ```lean
    NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile_interior (F : NavierStokes.OutgoingProfile.Profile) {XR C B y η : ℝ} (hF : NavierStokes.OutgoingProfile.Specification F B) (w : NavierStokes.HeatedOutgoing.CompensationWitness F XR C) (hy : NavierStokes.TerminalCone.terminalStart F.data < y) (hη : η ∈ Set.Ioo (-1) 1) : NavierStokes.TerminalHistoryBridge.forwardTheta F XR w.coefficients (y, η) = NavierStok ...
    ```
    - `NavierStokes.TerminalHistoryBridge.physical_forwardTheta_eq_terminal` (theorem, doc) | mass 0.47% | hidden 68 decls | statement 1122 chars
      ```lean
      NavierStokes.TerminalHistoryBridge.physical_forwardTheta_eq_terminal (F : NavierStokes.OutgoingProfile.Profile) {XR C t r z : ℝ} (w : NavierStokes.HeatedOutgoing.CompensationWitness F XR C) (ht : t < 1) (hr : 0 < r) (hfull : 1 / 2 < Real.log (NavierStokes.SimilarityProfile.X F.data.h (NavierStokes.TerminalStress.radiusPoint t r z) / NavierStokes.OutgoingDilation.switchRadius F XR) + 1 / 5) : NavierStokes.SimilarityPr ...
      ```
- `NavierStokes.ActualCyclePreservation.state_runInvariant` (theorem, doc) | mass 1.03% | hidden 307 decls | statement 297 chars **[milestone]**
  - _passes through:_ `NavierStokes.ActualCyclePreservation.initial_runInvariant` → `NavierStokes.ActualCyclePreservation.initial_invariant` → `NavierStokes.ActualCoreSupport.initial_invariant`
  ```lean
  NavierStokes.ActualCyclePreservation.state_runInvariant (B N0 : ℕ) (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0) (j : ℕ) : NavierStokes.ActualCyclePreservation.RunInvariant (NavierStokes.ActualIterationLedger.sigma j) (NavierStokes.ActualCyclePreservation.state B N0 j)
  ```
  _Every stage `j` of the fixed construction satisfies `RunInvariant (sigma j)`: the main induction of the iteration, proved by a five-line `induction j`. Short statement, docstring, and the natural thing to trust._
  - `NavierStokes.ActualInitialization.initial_invariant` (theorem, doc) | mass 0.81% | hidden 209 decls | statement 450 chars
    ```lean
    NavierStokes.ActualInitialization.initial_invariant (B N0 : ℕ) : NavierStokes.CorrectionStep.CycleAnalyticInvariant NavierStokes.ActualInitialization.geometry (NavierStokes.CorrectionInitialization.ActualPrimary.commonContext B) NavierStokes.ActualInitialization.tangentBlock NavierStokes.ActualInitialization.envelope NavierStokes.ActualInitialization.labelCarrier (1 / 5) (NavierStokes.ActualInitialization.initialCycl ...
    ```
- `NavierStokes.ActualCyclePreservation.particularData` (theorem) | mass 0.72% | hidden 214 decls | statement 366 chars
  - _passes through:_ `NavierStokes.ActualParticularCycleData.actual_data`
  ```lean
  NavierStokes.ActualCyclePreservation.particularData {B N0 : ℕ} {σ : ℝ} {x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualCyclePreservation.Index B N0)} (R : NavierStokes.ActualCyclePreservation.RunInvariant σ x) (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0) (hσ : 1 / 5 ≤ σ) : NavierStokes.ActualParticularCycleData.Data x σ
  ```
- `NavierStokes.ActualParticularCoherence.raw_outputs` (theorem, doc) | mass 0.66% | hidden 176 decls | statement 2796 chars
  ```lean
  NavierStokes.ActualParticularCoherence.raw_outputs {B N0 : ℕ} (x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularCoherence.Label B N0)) (l : NavierStokes.ActualParticularCoherence.Label B N0) (I : NavierStokes.ActualParticularCoherence.SourceInputs x l) (hfrequency : ∀ (n : ℕ), (x.coefficients.blocks l).frequency n = ↑(NavierStokes.ChartScales.carrier NavierStokes.CorrectionInitialization.Actua ...
  ```
- `NavierStokes.ActualParticularStageControls.selectedActualControl` (def, doc) | mass 0.59% | hidden 45 decls | statement 1817 chars
  - _passes through:_ `NavierStokes.ActualParticularStageControls.selectedControl` → `NavierStokes.ScaledActualParticularControl.scaledControl`
  ```lean
  NavierStokes.ActualParticularStageControls.selectedActualControl {B N0 : ℕ} (e : ℕ → NavierStokes.ActualParticularStageControls.ActivePair B N0) (x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0)) (hfrequency : ∀ (l : NavierStokes.ActualParticularStageControls.Label B N0) (n : ℕ), (x.coefficients.blocks l).frequency n = ↑(NavierStokes.ChartScales.carrier NavierStokes.C ...
  ```
- `NavierStokes.FirstOrderBaseEdge.modified_first_pair_eq` (theorem) | mass 0.51% | hidden 116 decls | statement 903 chars
  ```lean
  NavierStokes.FirstOrderBaseEdge.modified_first_pair_eq {F : NavierStokes.OutgoingProfile.Profile} (W : NavierStokes.NominalProfile.Witness F) {D : NavierStokes.ProfileHistories.RadialDomain} (Q : NavierStokes.ProfileHistories.Profiles D) {S : Set ℝ} {lo hi : ℝ} (M : NavierStokes.AssembledSlowBase.FiniteModification W Q S lo hi) (hI : ∀ eta ∈ S, Q.I (NavierStokes.AssembledSlowBase.nominalOuterX W, eta) = W.profiles.I ...
  ```

Trusting the 13 top-level statements skips **56.5%** of the proof mass (10,086 of 23,747 declarations). The other 43.5% (13,661 declarations) is the hub's own proof plus the shared layer and small regions not listed. The 40 outline statements and the spine mention 369 distinct project declarations directly; unfolding those definitions down to Mathlib takes 3240 project definitions, 343 of which sit inside the regions being skipped.

**Shared toolkit** (most-used declarations below this root; users counted below this root only):

| users | kind | name | statement |
|---|---|---|---|
| 2892 | structure | `NavierStokes.OutgoingTail.TailData` | `NavierStokes.OutgoingTail.TailData : Type \| NavierStokes.OutgoingTail.TailData.mk : (core : NavierStokes.OutgoingSchedule.Parameters) → (h : ℝ) → 0 < h → 2 * h ...` |
| 2828 | def | `NavierStokes.PressureStream.Plane` | `NavierStokes.PressureStream.Plane : Type` |
| 2547 | structure | `NavierStokes.OutgoingProfile.Profile` | `NavierStokes.OutgoingProfile.Profile : Type \| NavierStokes.OutgoingProfile.Profile.mk : (data : NavierStokes.OutgoingTail.TailData) → (coefficientBound : ℝ) → N ...` |
| 2520 | def | `NavierStokes.ProblemStatement.Space` | `NavierStokes.ProblemStatement.Space : Type` |
| 2225 | def | `NavierStokes.TorusInverse.Plane` | `NavierStokes.TorusInverse.Plane : Type` |
| 2040 | def | `NavierStokes.CorrectionInitialization.ActualPrimary.h` | `NavierStokes.CorrectionInitialization.ActualPrimary.h : ℝ` |
| 1828 | def | `NavierStokes.LocalSignedRequest.Plane` | `NavierStokes.LocalSignedRequest.Plane : Type` |
| 1737 | def | `NavierStokes.ProblemStatement.SpaceTime` | `NavierStokes.ProblemStatement.SpaceTime : Type` |
| 1451 | structure | `NavierStokes.WeightedClasses.StripData` | `NavierStokes.WeightedClasses.StripData.{u_5} (D : Type u_5) [NormedAddCommGroup D] [NormedSpace ℝ D] : Type u_5 \| NavierStokes.WeightedClasses.StripData.mk : {D ...` |
| 1275 | def | `NavierStokes.CorrectionInitialization.ActualPrimary.Label` | `NavierStokes.CorrectionInitialization.ActualPrimary.Label (B N0 : ℕ) : Type` |
| 1242 | def | `NavierStokes.TorusInverse.Frequency` | `NavierStokes.TorusInverse.Frequency : Type` |
| 1161 | def | `NavierStokes.HarmonicCalculus.ComplexVector` | `NavierStokes.HarmonicCalculus.ComplexVector : Type` |
| 360 | theorem | `NavierStokes.ChartScales.Q_pos` | `NavierStokes.ChartScales.Q_pos (n : ℕ) : 0 < NavierStokes.ChartScales.Q n` |
| 282 | theorem | `NavierStokes.OutgoingTail.TailData.h_lt_half` | `NavierStokes.OutgoingTail.TailData.h_lt_half (d : NavierStokes.OutgoingTail.TailData) : d.h < 1 / 2` |
| 103 | theorem | `NavierStokes.NominalProfile.Controls.radius_pos` | `NavierStokes.NominalProfile.Controls.radius_pos {F : NavierStokes.OutgoingProfile.Profile} {A : NavierStokes.NominalProfile.AxisStage F} (c : NavierStokes.Nomin ...` |
| 97 | theorem | `NavierStokes.PrimaryTargetBounds.leftRadius_pos` | `NavierStokes.PrimaryTargetBounds.leftRadius_pos {F : NavierStokes.OutgoingProfile.Profile} (W : NavierStokes.NominalProfile.Witness F) : 0 < NavierStokes.Primar ...` |
| 96 | theorem | `NavierStokes.NominalProfile.AxisStage.scale_pos` | `NavierStokes.NominalProfile.AxisStage.scale_pos {F : NavierStokes.OutgoingProfile.Profile} (A : NavierStokes.NominalProfile.AxisStage F) : 0 < A.scale` |
| 92 | theorem | `NavierStokes.ChartScales.epsilon_pos` | `NavierStokes.ChartScales.epsilon_pos (h : ℝ) (n : ℕ) : 0 < NavierStokes.ChartScales.epsilon h n` |
| 91 | theorem | `NavierStokes.ReferencePath.parameterInterval_open` | `NavierStokes.ReferencePath.parameterInterval_open : IsOpen NavierStokes.ReferencePath.parameterInterval` |
| 83 | theorem | `NavierStokes.OutgoingProfile.Profile.axisDatum_contDiff` | `NavierStokes.OutgoingProfile.Profile.axisDatum_contDiff (F : NavierStokes.OutgoingProfile.Profile) : ContDiff ℝ (↑⊤) F.axisDatum` |
| 72 | theorem | `NavierStokes.SimilarityProfile.q_pos` | `NavierStokes.SimilarityProfile.q_pos {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2) {p : NavierStokes.SimilarityProfile.PhysicalPoint} (hp : p.1 < 1) : 0 < NavierStokes ...` |
| 69 | theorem | `NavierStokes.CorrectionInitialization.ActualPrimary.vectors_det` | `NavierStokes.CorrectionInitialization.ActualPrimary.vectors_det : NavierStokes.CorrectionInitialization.ActualPrimary.radialVector.1 * NavierStokes.CorrectionIn ...` |
| 65 | theorem | `NavierStokes.AxisymmetricResidual.pack_zero` | `NavierStokes.AxisymmetricResidual.pack_zero (a b c : ℝ) : (NavierStokes.AxisymmetricResidual.pack a b c).ofLp 0 = a` |
| 64 | theorem | `NavierStokes.NominalConeAssembly.activeLeft_pos` | `NavierStokes.NominalConeAssembly.activeLeft_pos {F : NavierStokes.OutgoingProfile.Profile} (W : NavierStokes.NominalProfile.Witness F) : 0 < NavierStokes.Nomina ...` |


## NavierStokes.Comparator.navier_stokes_breakdown_periodic

Navier-Stokes Corollary 10.6, Clay alternative (D): breakdown on R^3/Z^3. Reaches 23,840 declarations, proof mass 24,637,853.

```lean
NavierStokes.Comparator.navier_stokes_breakdown_periodic (nu : ℝ) (hnu : nu > 0) :
  ∃ u₀ f,
    NavierStokes.Comparator.InitialVelocityConditionPeriodic u₀ ∧
      NavierStokes.Comparator.ForceConditionPeriodic f ∧
        ¬∃ v p, NavierStokes.Comparator.NavierStokesExistenceAndSmoothnessPeriodic nu u₀ f v p
```

**Spine** (each statement is the only way into the one before it and carries at least 90% of its mass):

1. `NavierStokes.ComparatorBridge.navier_stokes_breakdown_periodic` (theorem, `NavierStokes.ComparatorTheorem:45`), 100.0% of mass, 23,831 declarations beneath, 36 tree children
2. `NavierStokes.PeriodicPaper.periodic_corollary` (theorem, `NavierStokes.PeriodicPaperTheorem:153`), 99.9% of mass, 23,772 declarations beneath, 84 tree children
3. `NavierStokesR3.theorem_1_1_with_initial_rest` (theorem, `NavierStokes.R3.Theorem:24`), 99.2% of mass, 23,541 declarations beneath, 20 tree children
4. `NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest` (theorem, `NavierStokes.R3.ActualCandidate:141`), 96.4% of mass, 22,853 declarations beneath, 8586 tree children

**Hub** `NavierStokesR3.ActualCandidate.selected_candidate_one_with_initial_rest` has 8,586 dominator-tree children; 7,437 of them dominate nothing but themselves.

The spine nodes above the hub have 145 further children of their own (side branches such as the comparison argument); they are chapter candidates too.

**Outline** (40 statements; mass = share of all proof mass below the root that sits under the statement, itself included; hidden = declarations a reader skips by trusting it):

- `NavierStokes.CorrectionInitialization.ActualPrimary.profile` (def) | mass 23.10% | hidden 3,009 decls | statement 100 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.FinalSlowBase.actualProfile` → `NavierStokes.FinalSlowBase.profileData_nonempty` → `NavierStokes.NominalConeAssembly.exists_nominal_cone`
  - `NavierStokes.NominalConeAssembly.exists_certificate` (theorem, doc) | mass 11.35% | hidden 1,424 decls | statement 161 chars
    - `NavierStokes.NominalConeAssembly.assembly_exists` (theorem) | mass 9.46% | hidden 1,073 decls | statement 161 chars
    - `NavierStokes.NominalConeAssembly.Assembly.certificate` (theorem, doc) | mass 0.88% | hidden 132 decls | statement 218 chars
  - `NavierStokes.PreparedOutgoing.exists_prepared` (theorem, doc) | mass 9.50% | hidden 1,039 decls | statement 104 chars
    - `NavierStokes.OutgoingCone.exists_ordered_profile_cone` (theorem, doc) | mass 5.63% | hidden 715 decls | statement 1158 chars
      - _passes through:_ `NavierStokes.OutgoingCone.exists_ordered_clean_cone`
    - `NavierStokes.ScheduledProfileChoice.exists_scheduled_family_below` (theorem, doc) | mass 1.95% | hidden 89 decls | statement 1257 chars
      - _passes through:_ `NavierStokes.ScheduledProfileChoice.exists_scheduled_core_below` → `NavierStokes.UniformAngularReset.exists_scheduled_reset`
- `NavierStokes.ActualCandidateAssembly.selected_witness` (theorem) | mass 13.56% | hidden 3,988 decls | statement 297 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.ActualCandidateAssembly.witness`
  - `NavierStokes.ActualCandidateAssembly.estimates` (def) | mass 9.12% | hidden 2,535 decls | statement 492 chars
    - `NavierStokes.GluedStageEstimates.actualStageEstimates` (def, doc) | mass 5.71% | hidden 1,230 decls | statement 1341 chars
    - `NavierStokes.ActualCandidateAssembly.physicalData` (theorem) | mass 1.92% | hidden 674 decls | statement 642 chars
  - `NavierStokes.GermCandidateAssembly.exists_candidate_witness_of_finite_stages` (theorem, doc) | mass 1.13% | hidden 383 decls | statement 6382 chars
    - `NavierStokes.CandidateConsequences.mixed_exists_force_with_consequences` (theorem, doc) | mass 0.52% | hidden 196 decls | statement 2893 chars
- `NavierStokes.FiveProfileMoments.exists_normalized_repair` (theorem, doc) | mass 4.94% | hidden 21 decls | statement 550 chars **[waypoint-readable]**
- `NavierStokes.ActualSlowAxis.hierarchy` (def) | mass 3.38% | hidden 502 decls | statement 567 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.SlowRecursion.buildLocalHierarchy`
  - `NavierStokes.SlowRecursion.sequence_positive_order` (theorem, doc) | mass 1.04% | hidden 121 decls | statement 1662 chars
    - _passes through:_ `NavierStokes.SlowRecursion.sequence_expanded` → `NavierStokes.SlowRecursion.step_expanded`
    - `NavierStokes.PositiveAxisExistence.positiveSolution_profiles_system` (theorem) | mass 0.45% | hidden 38 decls | statement 1039 chars
  - `NavierStokes.PositiveAxisExistence.LowerInputRegularity.system` (theorem) | mass 0.52% | hidden 9 decls | statement 486 chars
  - `NavierStokes.PositiveAxisExistence.positiveSolution_parity` (theorem) | mass 0.50% | hidden 26 decls | statement 528 chars
- `NavierStokesR3.ProblemStatement.CandidateProperties.no_global_solution_one` (theorem, doc) | mass 2.70% | hidden 655 decls | statement 435 chars **[milestone]**
  - _passes through:_ `NavierStokesR3.WholeSpaceUniqueness.candidate_global_agrees_before_one` → `NavierStokesR3.WholeSpaceUniqueness.candidate_unique_on_Icc` → `NavierStokesR3.WholeSpaceUniqueness.classical_uniqueness_on_Icc`
  - `NavierStokesR3.PressureFlux.exists_uniform_actual_pressure_flux_bound` (theorem, doc) | mass 2.00% | hidden 475 decls | statement 1892 chars
    - `NavierStokesR3.PressureFlux.exists_uniform_canonicalCutoffFlux_bound` (theorem, doc) | mass 1.09% | hidden 227 decls | statement 1853 chars
      - _passes through:_ `NavierStokesR3.PressureFlux.canonicalCutoffFlux_bound` → `NavierStokesR3.PressureFlux.cutoff_pressurePair_bound`
    - `NavierStokesR3.PressureFlux.actual_flux_integrable_and_le_canonicalNorm` (theorem) | mass 0.83% | hidden 216 decls | statement 785 chars
      - _passes through:_ `NavierStokesR3.PressureFlux.actual_flux_eq_canonicalCutoffFlux` → `NavierStokesR3.ActualPressureFlux.pressure_flux_eq_canonical` → `NavierStokesR3.PressureRecovery.gradient_recovery` → `NavierStokesR3.PressureRecovery.gradient_recovery_complex`
  - `NavierStokesR3.WholeSpaceComparisonClosure.eq_of_pressure_flux_bound` (theorem, doc) | mass 0.46% | hidden 76 decls | statement 2341 chars
- `NavierStokes.CorrectionInitialization.ActualPrimary.choice` (def) | mass 2.27% | hidden 358 decls | statement 137 chars **[waypoint-opaque]**
  - _passes through:_ `NavierStokes.CorrectionInitialization.ActualPrimary.choice_nonempty` → `NavierStokes.PrimaryTargetBounds.exists_constructed_bounds`
  - `NavierStokes.PrimaryTargetBounds.exists_restricted_actual_bounds` (theorem, doc) | mass 1.21% | hidden 194 decls | statement 1577 chars
    - _passes through:_ `NavierStokes.PrimaryTargetBounds.exists_actual_bounds` → `NavierStokes.PrimaryTargetBounds.exists_prepared_bounds` → `NavierStokes.PrimaryTargetBounds.exists_family_bounds`
  - `NavierStokes.PrimaryGeometryAssembly.prepared` (def, doc) | mass 1.00% | hidden 147 decls | statement 588 chars
    - _passes through:_ `NavierStokes.PrimaryGeometryAssembly.exists_prepared`
    - `NavierStokes.AlignedProfileSpectralCone.modulated_representative_bounds` (theorem, doc) | mass 0.64% | hidden 80 decls | statement 3790 chars
- `NavierStokes.CorrectionAnalyticStep.step` (theorem, doc) | mass 1.56% | hidden 400 decls | statement 1366 chars **[waypoint-readable]**
  - `NavierStokes.CrossBasedMeanComposition.CycleParameters.mean_gain_from_waves_of_cross_defects` (theorem, doc) | mass 0.97% | hidden 235 decls | statement 11579 chars
    - _passes through:_ `NavierStokes.CrossBasedMeanComposition.fourStage_mean_gain_of_cross_defects`
    - `NavierStokes.CrossBasedMeanComposition.bandSignedStage_mean_debt_of_cross_defects` (theorem, doc) | mass 0.82% | hidden 226 decls | statement 3430 chars
      - _passes through:_ `NavierStokes.CrossBasedMeanComposition.signed_mean_gain_of_cross_defects`
- `NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile` (theorem, doc) | mass 1.08% | hidden 198 decls | statement 1326 chars **[unreadable]**
  - `NavierStokes.TerminalHistoryBridge.forward_stresses_eq_profile_interior` (theorem, doc) | mass 0.95% | hidden 184 decls | statement 982 chars
    - `NavierStokes.TerminalHistoryBridge.physical_forwardTheta_eq_terminal` (theorem, doc) | mass 0.47% | hidden 68 decls | statement 1122 chars
- `NavierStokes.ActualCyclePreservation.state_runInvariant` (theorem, doc) | mass 1.03% | hidden 307 decls | statement 297 chars **[milestone]**
  - _passes through:_ `NavierStokes.ActualCyclePreservation.initial_runInvariant` → `NavierStokes.ActualCyclePreservation.initial_invariant` → `NavierStokes.ActualCoreSupport.initial_invariant`
  - `NavierStokes.ActualInitialization.initial_invariant` (theorem, doc) | mass 0.81% | hidden 209 decls | statement 450 chars
- `NavierStokes.ActualCyclePreservation.particularData` (theorem) | mass 0.72% | hidden 214 decls | statement 366 chars
  - _passes through:_ `NavierStokes.ActualParticularCycleData.actual_data`
- `NavierStokes.ActualParticularCoherence.raw_outputs` (theorem, doc) | mass 0.66% | hidden 176 decls | statement 2796 chars
- `NavierStokes.ActualParticularStageControls.selectedActualControl` (def, doc) | mass 0.59% | hidden 45 decls | statement 1817 chars
  - _passes through:_ `NavierStokes.ActualParticularStageControls.selectedControl` → `NavierStokes.ScaledActualParticularControl.scaledControl`
- `NavierStokes.FirstOrderBaseEdge.modified_first_pair_eq` (theorem) | mass 0.51% | hidden 116 decls | statement 903 chars

Trusting the 13 top-level statements skips **56.1%** of the proof mass (10,002 of 23,840 declarations). The other 43.9% (13,838 declarations) is the hub's own proof plus the shared layer and small regions not listed. The 40 outline statements and the spine mention 369 distinct project declarations directly; unfolding those definitions down to Mathlib takes 3245 project definitions, 343 of which sit inside the regions being skipped.

**Shared toolkit** (most-used declarations below this root; users counted below this root only):

| users | kind | name | statement |
|---|---|---|---|
| 2892 | structure | `NavierStokes.OutgoingTail.TailData` | `NavierStokes.OutgoingTail.TailData : Type \| NavierStokes.OutgoingTail.TailData.mk : (core : NavierStokes.OutgoingSchedule.Parameters) → (h : ℝ) → 0 < h → 2 * h ...` |
| 2828 | def | `NavierStokes.PressureStream.Plane` | `NavierStokes.PressureStream.Plane : Type` |
| 2606 | def | `NavierStokes.ProblemStatement.Space` | `NavierStokes.ProblemStatement.Space : Type` |
| 2547 | structure | `NavierStokes.OutgoingProfile.Profile` | `NavierStokes.OutgoingProfile.Profile : Type \| NavierStokes.OutgoingProfile.Profile.mk : (data : NavierStokes.OutgoingTail.TailData) → (coefficientBound : ℝ) → N ...` |
| 2225 | def | `NavierStokes.TorusInverse.Plane` | `NavierStokes.TorusInverse.Plane : Type` |
| 2040 | def | `NavierStokes.CorrectionInitialization.ActualPrimary.h` | `NavierStokes.CorrectionInitialization.ActualPrimary.h : ℝ` |
| 1828 | def | `NavierStokes.LocalSignedRequest.Plane` | `NavierStokes.LocalSignedRequest.Plane : Type` |
| 1787 | def | `NavierStokes.ProblemStatement.SpaceTime` | `NavierStokes.ProblemStatement.SpaceTime : Type` |
| 1451 | structure | `NavierStokes.WeightedClasses.StripData` | `NavierStokes.WeightedClasses.StripData.{u_5} (D : Type u_5) [NormedAddCommGroup D] [NormedSpace ℝ D] : Type u_5 \| NavierStokes.WeightedClasses.StripData.mk : {D ...` |
| 1275 | def | `NavierStokes.CorrectionInitialization.ActualPrimary.Label` | `NavierStokes.CorrectionInitialization.ActualPrimary.Label (B N0 : ℕ) : Type` |
| 1242 | def | `NavierStokes.TorusInverse.Frequency` | `NavierStokes.TorusInverse.Frequency : Type` |
| 1161 | def | `NavierStokes.HarmonicCalculus.ComplexVector` | `NavierStokes.HarmonicCalculus.ComplexVector : Type` |
| 360 | theorem | `NavierStokes.ChartScales.Q_pos` | `NavierStokes.ChartScales.Q_pos (n : ℕ) : 0 < NavierStokes.ChartScales.Q n` |
| 282 | theorem | `NavierStokes.OutgoingTail.TailData.h_lt_half` | `NavierStokes.OutgoingTail.TailData.h_lt_half (d : NavierStokes.OutgoingTail.TailData) : d.h < 1 / 2` |
| 103 | theorem | `NavierStokes.NominalProfile.Controls.radius_pos` | `NavierStokes.NominalProfile.Controls.radius_pos {F : NavierStokes.OutgoingProfile.Profile} {A : NavierStokes.NominalProfile.AxisStage F} (c : NavierStokes.Nomin ...` |
| 97 | theorem | `NavierStokes.PrimaryTargetBounds.leftRadius_pos` | `NavierStokes.PrimaryTargetBounds.leftRadius_pos {F : NavierStokes.OutgoingProfile.Profile} (W : NavierStokes.NominalProfile.Witness F) : 0 < NavierStokes.Primar ...` |
| 96 | theorem | `NavierStokes.NominalProfile.AxisStage.scale_pos` | `NavierStokes.NominalProfile.AxisStage.scale_pos {F : NavierStokes.OutgoingProfile.Profile} (A : NavierStokes.NominalProfile.AxisStage F) : 0 < A.scale` |
| 92 | theorem | `NavierStokes.ChartScales.epsilon_pos` | `NavierStokes.ChartScales.epsilon_pos (h : ℝ) (n : ℕ) : 0 < NavierStokes.ChartScales.epsilon h n` |
| 91 | theorem | `NavierStokes.ReferencePath.parameterInterval_open` | `NavierStokes.ReferencePath.parameterInterval_open : IsOpen NavierStokes.ReferencePath.parameterInterval` |
| 83 | theorem | `NavierStokes.OutgoingProfile.Profile.axisDatum_contDiff` | `NavierStokes.OutgoingProfile.Profile.axisDatum_contDiff (F : NavierStokes.OutgoingProfile.Profile) : ContDiff ℝ (↑⊤) F.axisDatum` |
| 72 | theorem | `NavierStokes.SimilarityProfile.q_pos` | `NavierStokes.SimilarityProfile.q_pos {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2) {p : NavierStokes.SimilarityProfile.PhysicalPoint} (hp : p.1 < 1) : 0 < NavierStokes ...` |
| 69 | theorem | `NavierStokes.CorrectionInitialization.ActualPrimary.vectors_det` | `NavierStokes.CorrectionInitialization.ActualPrimary.vectors_det : NavierStokes.CorrectionInitialization.ActualPrimary.radialVector.1 * NavierStokes.CorrectionIn ...` |
| 65 | theorem | `NavierStokes.AxisymmetricResidual.pack_zero` | `NavierStokes.AxisymmetricResidual.pack_zero (a b c : ℝ) : (NavierStokes.AxisymmetricResidual.pack a b c).ofLp 0 = a` |
| 64 | theorem | `NavierStokes.NominalConeAssembly.activeLeft_pos` | `NavierStokes.NominalConeAssembly.activeLeft_pos {F : NavierStokes.OutgoingProfile.Profile} (W : NavierStokes.NominalProfile.Witness F) : 0 < NavierStokes.Nomina ...` |


## Euler.euler_breakdown_R3

Euler Theorem 1.1: no global smooth unforced Euler solution with bounded energy. Reaches 13,108 declarations, proof mass 22,359,509.

```lean
Euler.euler_breakdown_R3 :
  ∃ u₀, Euler.InitialVelocityConditionDecay u₀ ∧ ¬∃ v p, Euler.EulerExistenceAndSmoothnessR3 u₀ v p
```

**Spine** (each statement is the only way into the one before it and carries at least 90% of its mass):

(none: the root itself is the hub; no single statement stands between it and the rest)

**Hub** `Euler.euler_breakdown_R3` has 5,846 dominator-tree children; 4,829 of them dominate nothing but themselves.

**Outline** (40 statements; mass = share of all proof mass below the root that sits under the statement, itself included; hidden = declarations a reader skips by trusting it):

- `EulerAllOrderDriftCorrection.finite_exists` (theorem, doc) | mass 8.90% | hidden 797 decls | statement 1512 chars **[waypoint-opaque]**
  - _passes through:_ `EulerDriftGlobalInviscidGevrey.exists_global_inviscid_gevrey_PDE`
  ```lean
  EulerAllOrderDriftCorrection.finite_exists (period : ℝ) [Fact (0 < period)] {T : ℝ} (hT : 0 < T) (A : EulerAllOrderCorrectionData.Data period T) (B : EulerAllOrderDriftCorrection.Budget period hT A) (q : ℕ) (hq : 6 ≤ q) : ∃ e, e ⟨0, ⋯⟩ = 0 ∧ (∀ (t : ↑(Set.Icc 0 T)), EulerCylinderSobolevSpace.value period (e t) ∈ EulerLiftedGradientSpace.divergenceFreeSpace period A.κ A.direction) ∧ (∀ P ≤ q - 4, ∀ (hP : P + 6 ≤ q + 1 ...
  ```
  _Existence of a finite-order inviscid correction: a continuous path in a Sobolev space, zero at t=0, divergence-free, with two Gevrey-energy bounds, solving the linearised evolution equation. A genuine existence theorem with a docstring, but 1,500 characters and readable only with the `Data`/`Budget` structures in hand._
  - `EulerDriftGevreyInviscidEnergyCompactness.exists_gevrey_inviscid_energy_limit` (theorem, doc) | mass 7.78% | hidden 668 decls | statement 3834 chars
    - _passes through:_ `EulerDriftViscousCorrectionFamily.exists_viscous_correction_family` → `EulerDriftGlobalGevreyCorrection.exists_global_gevrey_correction`
    ```lean
    EulerDriftGevreyInviscidEnergyCompactness.exists_gevrey_inviscid_energy_limit (period : ℝ) [Fact (0 < period)] {q : ℕ} (hq : 6 ≤ q) (S : ℝ) (hS : 0 < S) (D : EulerCorrectionOperators.CorrectionData period (q + 1) ↑(Set.Icc 0 S)) (KG : (t : ↑(Set.Icc 0 S)) → EulerSpatialSobolevInverse.CoefficientJet period EulerCylinderSobolev.standardDirection q (D.metric.coefficient t)) (KL : (t : ↑(Set.Icc 0 S)) → EulerSpatialSobol ...
    ```
    - `EulerDriftPartialCorrectionBootstrap.partial_correction_bootstrap` (theorem, doc) | mass 6.35% | hidden 525 decls | statement 2891 chars
      - _passes through:_ `EulerDriftCorrectionBootstrap.correction_mild_bootstrap` → `EulerDriftCorrectionMildEnergy.correction_mild_integral`
      ```lean
      EulerDriftPartialCorrectionBootstrap.partial_correction_bootstrap (period : ℝ) [Fact (0 < period)] {q : ℕ} (hq : 6 ≤ q) (S : ℝ) (hS : 0 ≤ S) (D : EulerCorrectionOperators.CorrectionData period (q + 1) ↑(Set.Icc 0 S)) (KG : (t : ↑(Set.Icc 0 S)) → EulerSpatialSobolevInverse.CoefficientJet period EulerCylinderSobolev.standardDirection q (D.metric.coefficient t)) (KL : (t : ↑(Set.Icc 0 S)) → EulerSpatialSobolevInverse.Co ...
      ```
    - `EulerCorrectionContinuation.exists_global_correction_of_bound` (theorem, doc) | mass 0.58% | hidden 60 decls | statement 1047 chars
      - _passes through:_ `EulerBoundedMildContinuation.exists_global_mild_of_bound`
      ```lean
      EulerCorrectionContinuation.exists_global_correction_of_bound (period : ℝ) [Fact (0 < period)] {q : ℕ} (hq : 6 ≤ q) (ν : ℝ) (hν : 0 < ν) (S : ℝ) (hS : 0 < S) (R : ℝ) (hR : 0 ≤ R) (D : EulerCorrectionOperators.CorrectionData period q ↑(Set.Icc 0 S)) (hbound : ∀ (T : ℝ) (hT : 0 ≤ T) (hTS : T ≤ S) (e : C(↑(Set.Icc 0 T), ↥(EulerCylinderSobolevSpace.SobolevSpace period (q + 1)))), (∀ (t : ↑(Set.Icc 0 T)), e t = EulerQuadr ...
      ```
- `EulerPacketMovingFrame.PhysicalGeometryData.exists_geometry` (theorem) | mass 6.43% | hidden 313 decls | statement 213 chars **[unreadable]**
  ```lean
  EulerPacketMovingFrame.PhysicalGeometryData.exists_geometry.{u_1} {α : Type u_1} (D : EulerPacketMovingFrame.PhysicalGeometryData α) : ∃ F F₁ Z Z₁, EulerPacketMovingFrame.PhysicalGeometryConclusion D F F₁ Z Z₁
  ```
  _`∃ F F₁ Z Z₁, PhysicalGeometryConclusion D F F₁ Z Z₁`. Short, but hypothesis and conclusion are two structures of dozens of fields with constants such as `8232*exp 9*Θ^5` and `30000000*neighborStabilityConstant`; the statement is a pointer to a page of estimates._
  - `EulerPacketMovingFrame.physical_frame_renewal_order40` (theorem) | mass 1.35% | hidden 51 decls | statement 2538 chars
    ```lean
    EulerPacketMovingFrame.physical_frame_renewal_order40 (M : EulerSmoothLimit.Space →L[ℝ] EulerSmoothLimit.Space) (m v r w : ℝ → EulerSmoothLimit.Space) {s₀ t₀ a ε σ y Θ K e : ℝ} {Z Z₁ : ℝ → ℝ} (ha : a ≠ 0) (hs₀ : 0 < s₀) (hε : 0 < ε) (hm : m (EulerPacketMovingFrame.physicalTime t₀ a ε (y⁻¹ / σ)) ≠ 0) (hv : v (EulerPacketMovingFrame.physicalTime t₀ a ε (y⁻¹ / σ)) ≠ 0) (hmv : inner ℝ (m (EulerPacketMovingFrame.physicalT ...
    ```
    - `EulerPacketFrameQuantitative.frame_renewal_order40` (theorem, doc) | mass 1.18% | hidden 31 decls | statement 1456 chars
      ```lean
      EulerPacketFrameQuantitative.frame_renewal_order40 {σ y Θ K e ε P Q N r : ℝ} {A : Fin 3 → Fin 3 → ℝ} {Z Z₁ : ℝ → ℝ} (hσ : 0 < σ) (hσsmall : σ ≤ 1 / 4) (hy : 0 < y) (hysmall : y ≤ 1 / 2) (hΘ : 1 ≤ Θ) (hK : 1 ≤ K) (he : 0 ≤ e) (hε : 0 ≤ ε) (hεe : ε ≤ e) (htΘ : y⁻¹ / σ ≤ Θ) (hsmall : 1000000 * K * e * Θ ^ 40 ≤ 1) (hZ : ∀ (t : ℝ), 0 ≤ t → HasDerivAt Z (Z₁ t) t) (hfluxZ : ∀ (t : ℝ), 0 ≤ t → HasDerivAt (fun s => (1 + (σ ^ ...
      ```
  - `EulerPacketMovingFrame.physical_matrix_errors` (theorem, doc) | mass 0.56% | hidden 11 decls | statement 2826 chars
    ```lean
    EulerPacketMovingFrame.physical_matrix_errors {B B₁ M E : ℝ → EulerSmoothLimit.Space →L[ℝ] EulerSmoothLimit.Space} {m v : ℝ → EulerSmoothLimit.Space} {c t₀ a ε Θ G d β : ℝ} {S : Set ℝ} (ha : 1 / 2 ≤ a) (hε : 0 < ε) (hΘ : 1 ≤ Θ) (hG : 1 ≤ G) (hd : 0 ≤ d) (hsmall : 16 * (ε * Θ * (4 * G) ^ 2 + d) ≤ 1) (hmap : Set.MapsTo (EulerPacketMovingFrame.physicalTime t₀ a ε) (Set.Icc 0 Θ) S) (hBd : ∀ t ∈ S, HasDerivWithinAt B (B₁ ...
    ```
    - `EulerPacketCoefficientControl.raw_frame_matrix_errors` (theorem, doc) | mass 0.52% | hidden 10 decls | statement 1269 chars
      ```lean
      EulerPacketCoefficientControl.raw_frame_matrix_errors {a ε e β h : ℝ} {B E : Fin 3 → Fin 3 → ℝ} (ha : a ≠ 0) (hε : 0 < ε) (hεe : ε ≤ e) (he : 0 ≤ e) (heSmall : e ≤ 1) (hB : ∀ (i j : Fin 3), |ε * B i j / a| ≤ e) (hE : ∀ (i j : Fin 3), |E i j / a| ≤ e) (hH : |ε ^ 2 * h / a - 1| ≤ e) (hα : |B 0 1 / a - 1| ≤ e) (hκ : |B 2 1 / a - β| ≤ e) : (∀ (i j : Fin 3), |EulerPacketRay.scaledRayEntry a ε (EulerPacketRay.parentEntry B ...
      ```
  - `EulerPacketMovingFrame.physical_family_amplification_and_size` (theorem) | mass 0.43% | hidden 9 decls | statement 5841 chars
    ```lean
    EulerPacketMovingFrame.physical_family_amplification_and_size.{u_1} {α : Type u_1} (center : α) {B B₁ : ℝ → EulerSmoothLimit.Space →L[ℝ] EulerSmoothLimit.Space} {M E : α → ℝ → EulerSmoothLimit.Space →L[ℝ] EulerSmoothLimit.Space} {m v : ℝ → EulerSmoothLimit.Space} {r w : α → ℝ → EulerSmoothLimit.Space} {c s₀ t₀ a ε σ Θ T G d lam : ℝ} {S : Set ℝ} (hσ : 0 < σ) (hσsmall : σ ≤ 1 / 4) (hT0 : 1 ≤ T) (hT : T ≤ Θ) (ha : 1 / 2 ...
    ```
- `Euler.initialDatum_no_global_solution (private)` (theorem) | mass 3.89% | hidden 703 decls | statement 130 chars **[restatement]**
  ```lean
  Euler.initialDatum_no_global_solution✝ : ¬∃ v p, Euler.EulerExistenceAndSmoothnessR3 EulerPacketInduction.initialDatum.field v p
  ```
  _The constructed initial datum admits no global smooth solution: `¬∃ v p, EulerExistenceAndSmoothnessR3 initialDatum.field v p`. This is the headline theorem minus the regularity and decay of the datum; the root's proof is a one-line tuple ending in this lemma, so trusting it is trusting the theorem. Counted as a restatement, not an intermediate milestone (second reader's finding). It dominates only 3.9% of the mass._
  - `Euler.ComparatorBridge.finiteLifespan_contradiction_of_compact_vorticity` (theorem) | mass 1.97% | hidden 337 decls | statement 563 chars
    - _passes through:_ `EulerOrdinarySobolev.FiniteLifespan.vorticityIntegral_unbounded`
    ```lean
    Euler.ComparatorBridge.finiteLifespan_contradiction_of_compact_vorticity {A : EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space} (L : EulerOrdinarySobolev.FiniteLifespan A) {v : EulerSmoothLimit.Space → ℝ → EulerSmoothLimit.Space} {p : EulerSmoothLimit.Space → ℝ → ℝ} (h : Euler.EulerExistenceAndSmoothnessR3 A.field v p) (K : Set EulerSmoothLimit.Space) (hK : IsCompact K) (hmatch : ∀ (t : L.Time), L.maximalVeloc ...
    ```
    - `EulerOrdinarySobolev.FiniteLifespan.vorticity_unbounded_of_logarithmic` (theorem) | mass 1.32% | hidden 214 decls | statement 717 chars
      ```lean
      EulerOrdinarySobolev.FiniteLifespan.vorticity_unbounded_of_logarithmic (C : ℝ) (hC : 0 ≤ C) (hlog : ∀ (A : EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space) (W : ℝ), A.toLp ∈ EulerMeanSolenoidal.solenoidalSpace → (∀ (x : EulerSmoothLimit.Space), ‖EulerMeanCutoffCurl.vectorCurl A.field x‖ ≤ W) → ∀ (x : EulerSmoothLimit.Space), ‖fderiv ℝ A.field x‖ ≤ C * (1 + ‖A.toLp‖ + W * Real.log (Real.exp 1 + EulerOrdinarySo ...
      ```
    - `EulerOrdinarySobolev.logarithmic_gradient_bound_solenoidal` (theorem, doc) | mass 0.61% | hidden 96 decls | statement 472 chars
      - _passes through:_ `EulerOrdinarySobolev.logarithmic_gradient_bound` → `EulerWholeSpaceGaussian.elliptic_derivative_logarithmic` → `EulerWholeSpaceGaussian.elliptic_derivative_split`
      ```lean
      EulerOrdinarySobolev.logarithmic_gradient_bound_solenoidal (A : EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space) (W : ℝ) (hA : A.toLp ∈ EulerMeanSolenoidal.solenoidalSpace) (hW : ∀ (y : EulerSmoothLimit.Space), ‖EulerMeanCutoffCurl.vectorCurl A.field y‖ ≤ W) (x : EulerSmoothLimit.Space) : ‖fderiv ℝ A.field x‖ ≤ EulerOrdinarySobolev.logarithmicGradientConstant * (1 + ‖A.toLp‖ + W * Real.log (Real.exp 1 + Euler ...
      ```
  - `Euler.ComparatorBridge.compactCurlLocalUpgrade` (theorem, doc) | mass 1.44% | hidden 254 decls | statement 95 chars
    ```lean
    Euler.ComparatorBridge.compactCurlLocalUpgrade : Euler.ComparatorBridge.CompactCurlLocalUpgrade
    ```
    - `Euler.ComparatorBridge.exists_evolution_of_commonCompactCurl` (theorem, doc) | mass 0.58% | hidden 104 decls | statement 507 chars
      ```lean
      Euler.ComparatorBridge.exists_evolution_of_commonCompactCurl {u₀ : EulerSmoothLimit.Space → EulerSmoothLimit.Space} {v : EulerSmoothLimit.Space → ℝ → EulerSmoothLimit.Space} {p : EulerSmoothLimit.Space → ℝ → ℝ} (h : Euler.EulerExistenceAndSmoothnessR3 u₀ v p) (T : ℝ) (hT : 0 < T) (K : Set EulerSmoothLimit.Space) (hK : IsCompact K) (hsupport : ∀ t ∈ Set.Icc 0 T, tsupport (EulerMeanCutoffCurl.vectorCurl fun x => v x t) ...
      ```
    - `Euler.EulerExistenceAndSmoothnessR3.local_compact_vorticity_of_truncationFamily` (theorem, doc) | mass 0.44% | hidden 68 decls | statement 546 chars
      ```lean
      Euler.EulerExistenceAndSmoothnessR3.local_compact_vorticity_of_truncationFamily {u₀ : EulerSmoothLimit.Space → EulerSmoothLimit.Space} {v : EulerSmoothLimit.Space → ℝ → EulerSmoothLimit.Space} {p : EulerSmoothLimit.Space → ℝ → ℝ} (h : Euler.EulerExistenceAndSmoothnessR3 u₀ v p) (F : Euler.ComparatorBridge.FiniteEnergyTruncationFamily v) (hc : HasCompactSupport (EulerMeanCutoffCurl.vectorCurl u₀)) : ∃ δ B, 0 < δ ∧ ∀ t ...
      ```
- `EulerParentPacketFrames.LabelData.forward_uniform_child` (theorem) | mass 2.18% | hidden 165 decls | statement 4007 chars **[unreadable]**
  - _passes through:_ `EulerPacketTerminalDatum.forward_uniform_child_label_bounds` → `EulerPacketTerminalDatum.forward_uniform_flow_and_shear`
  ```lean
  EulerParentPacketFrames.LabelData.forward_uniform_child {A : EulerParentPacketFrames.Parent} (L : EulerParentPacketFrames.LabelData A) (I : EulerParentPacketFrames.ParticleInverse A) (H : EulerParentPacketFrames.LowBounds A) {U : Type} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] (m : EulerSmoothLimit.Space) (hm : ‖m‖ = 1) (R : U ≃ₗᵢ[ℝ] ↥(EulerTransverseFrameCoordinates.referencePlane m)) (S : Set ...
  ```
  _4,007 characters; some twenty section variables as hypotheses and a conclusion of nested existentials over budgets and graph-flow data. Not a statement anyone can take on trust by reading it._
  - `EulerPacketTerminalDatum.forwardUniformBudget` (def) | mass 0.44% | hidden 22 decls | statement 1697 chars
    ```lean
    EulerPacketTerminalDatum.forwardUniformBudget.{u_1} (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] (D : EulerTransversePacketProvider.Data U) (hTime : M.T = D.T) (δ : ℝ) (hδ : 0 < δ) (hδ1 : δ ≤ 1) (ξ : U) (hs : tsupport EulerSpatialCutoffs.innerCutoff ⊆ D.support) (α : ℝ) (hα : 0 < α) (L : EulerTransversePacketForward.Budget D (Fin 4) 6) (NB : EulerT ...
    ```
- `EulerPacketSourceGeometry.Guards.selection` (theorem) | mass 1.82% | hidden 151 decls | statement 1261 chars **[unreadable]**
  - _passes through:_ `EulerPacketActivationHistory.exists_activated_primary` → `EulerPacketActivationHistory.select_physical_history_coordinate` → `EulerPacketActivationHistory.select_history_coordinate`
  ```lean
  EulerPacketSourceGeometry.Guards.selection.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] {D : EulerTransversePacketProvider.Data U} {τ : ℝ} [CompleteSpace U] (hτ : 0 < τ) (hτT : τ < D.T) (P : EulerPacketSourceGeometry.ParentFrame D τ) (H : EulerTransversePacketProvider.HistoryData (D.initial τ hτ ⋯)) (A : EulerPacketSourceGeometry.Guards hτ hτT P H) : 0 < P.rayScale hτ hτT ∧ EulerPacketMovingFra ...
  ```
  _Existence of a terminal vector ξ and slope λ normalising a scaled ray to `![0,0,1]` and two scaled-velocity components to `-λ` and `1`. A parameter-selection lemma whose meaning depends entirely on surrounding definitions._
  - `EulerTransverseActivationSelection.select_actual_activation` (theorem, doc) | mass 0.80% | hidden 51 decls | statement 2863 chars
    ```lean
    EulerTransverseActivationSelection.select_actual_activation.{u_1, u_2, u_3} {U : Type u_1} {E : Type u_2} {V : Type u_3} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E] [NormedAddCommGroup V] [InnerProductSpace ℝ V] [CompleteSpace V] (T : ℝ) (hT : 0 < T) (Q Q₁ : C(↑(Set.Icc 0 T), U →L[ℝ] E)) (c : ℝ) (hc : 0 < c) (hQ : ∀ (t : ↑(Set.Icc 0 ...
    ```
- `EulerPacketInduction.Stage.chooseJoined` (def) | mass 1.57% | hidden 93 decls | statement 406 chars **[waypoint-opaque]**
  - _passes through:_ `EulerParentPacketFrames.exists_geometryJoinedChoice` → `EulerParentPacketFrames.LabelData.joined_uniform_child` → `EulerPacketTerminalDatum.initialized_uniform_child_label_bounds` → `EulerPacketTerminalDatum.initialized_uniform_flow_and_shear`
  ```lean
  EulerPacketInduction.Stage.chooseJoined {q : ℕ} {B : ℝ} {S : EulerPacketInductionScales.Scales (↑q) B} {n : ℕ} (P : EulerPacketInduction.Stage S n) (hn : n ≠ 0) (hq : EulerParentNeighborThreshold.requiredExponent ≤ q) (hB : EulerParentNeighborThreshold.commonThreshold EulerPacketLowConstants.gradientConstant EulerPacketLowConstants.hessianConstant ≤ B) : P.JoinedChoice hn hq hB
  ```
  _`Classical.choice` of a `GeometryJoinedChoice` for stage `n`: the choice made in the successor step of the packet induction. Right place for a boundary; the statement is only the name of a structure._
  - `EulerPacketTerminalDatum.initializedUniformBudget` (def) | mass 0.49% | hidden 22 decls | statement 1842 chars
    ```lean
    EulerPacketTerminalDatum.initializedUniformBudget.{u_1} (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] (D : EulerTransversePacketProvider.Data U) (hTime : M.T = D.T) (τ : ℝ) (hτ : 0 < τ) (hτT : τ < D.T) (B : EulerTransversePacketProvider.HistoryData (D.initial τ hτ ⋯)) (δ : ℝ) (hδ : 0 < δ) (hδ1 : δ ≤ 1) (ξ : U) (hs : tsupport EulerSpatialCutoffs.inne ...
    ```
- `EulerPacketInduction.constructionScales` (def) | mass 1.13% | hidden 92 decls | statement 81 chars **[waypoint-opaque]**
  - _passes through:_ `EulerPacketInductionScales.exists_scales`
  ```lean
  EulerPacketInduction.constructionScales : EulerPacketInduction.ConstructionScales
  ```
  _`Classical.choice (exists_scales ...)`: the scale sequence used by the whole infinite construction. Short and sensible; again the content is the `Scales` structure, not the statement._
  - `EulerPacketCommonScaleChoice.exists_common_guards` (theorem) | mass 0.87% | hidden 51 decls | statement 2452 chars
    ```lean
    EulerPacketCommonScaleChoice.exists_common_guards.{u_1} {ι : Type u_1} [Fintype ι] (s : ι → EulerPacketSourceScaleChoice.CostSpec) (D : ℕ) (hD : 1000 ≤ D) (C c K CM CMn CHn cP : ℝ) (hC : 4 ≤ C) (hc : 0 ≤ c) (hK : 1 ≤ K) (hCM : 0 ≤ CM) (hCMn : 0 ≤ CMn) (hCHn : 0 ≤ CHn) : ∃ J, 3 ≤ J ∧ ∀ (η : ℝ), 0 < η → ∃ X₀ δ, 8 ≤ X₀ ∧ 0 < δ ∧ δ ≤ η ∧ δ ≤ 1 / 2 ∧ ∀ (X : ℝ), X₀ ≤ X → EulerPacketSourceScaleActual.ActualBounds J D C c X ...
    ```
- `EulerMeanPacketProvider.Budget.grade_bounds` (theorem, doc) | mass 1.04% | hidden 147 decls | statement 971 chars
  - _passes through:_ `EulerMeanPacketProvider.Budget.grade_profile_bounds` → `EulerMeanPacketProvider.Budget.three_shift_bounds` → `EulerMeanPacketProvider.Budget.word_bounds_of_field` → `EulerMeanPacketProvider.Budget.word_bounds` → `EulerMeanPacketProvider.Budget.physical_word_bounds`
  ```lean
  EulerMeanPacketProvider.Budget.grade_bounds {P : ℝ} [Fact (0 < P)] {D : EulerMeanPacketProvider.Data} {R : ℝ} (L : EulerMeanPacketProvider.Budget D 6 R) (W : L.GradeGuards) (S : EulerPacketTimeProfile.Scales ↑(Set.Icc 0 D.T)) {raw : EulerPacketProfileRecursion.VectorField} (G : EulerMeanPacketProvider.Forcing D raw) (F : EulerPacketCylinderField.Field P D.T raw) (p : ℕ) (hp : 2 ≤ p) (hforce : (F.normalized ⋯ (S.mean ...
  ```
  - `EulerMeanPacketProvider.SobolevData.path_envelope_bounds` (theorem, doc) | mass 0.87% | hidden 116 decls | statement 1533 chars
    - _passes through:_ `EulerMeanPacketProvider.SobolevData.envelope_bounds`
    ```lean
    EulerMeanPacketProvider.SobolevData.path_envelope_bounds.{u_1} {D : EulerMeanPacketProvider.Data} {ι : Type u_1} [Fintype ι] {q : ℕ} {R : ℝ} (E : EulerMeanPacketProvider.SobolevData D ι q R) (hCf1 : 1 ≤ E.Cf) (hCfT : √D.T ≤ E.Cf) (directions : ι → EulerSmoothLimit.Space) (hd : ∀ (i : ι), ‖directions i‖ ≤ 1) {raw : EulerPacketProfileRecursion.VectorField} (G : EulerMeanPacketProvider.Forcing D raw) (d : ℕ) (A : ℝ) (hA ...
    ```
    - `EulerMeanPacketProvider.SobolevData.normalized_bounds` (theorem, doc) | mass 0.74% | hidden 97 decls | statement 1684 chars
      ```lean
      EulerMeanPacketProvider.SobolevData.normalized_bounds.{u_1} {D : EulerMeanPacketProvider.Data} {ι : Type u_1} [Fintype ι] {q : ℕ} {R : ℝ} (E : EulerMeanPacketProvider.SobolevData D ι q R) (directions : ι → EulerSmoothLimit.Space) (hd : ∀ (i : ι), ‖directions i‖ ≤ 1) {raw : EulerPacketProfileRecursion.VectorField} (G : EulerMeanPacketProvider.Forcing D raw) (d : ℕ) (hfb : ∀ (n : ℕ) (a : EulerSmoothLimit.Space), EulerP ...
      ```
- `EulerPacketInduction.Stage.joinedNext` (def) | mass 0.79% | hidden 82 decls | statement 417 chars
  ```lean
  EulerPacketInduction.Stage.joinedNext {q : ℕ} {B : ℝ} {S : EulerPacketInductionScales.Scales (↑q) B} {n : ℕ} (P : EulerPacketInduction.Stage S n) (hn : n ≠ 0) (hq : EulerParentNeighborThreshold.requiredExponent ≤ q) (hB : EulerParentNeighborThreshold.commonThreshold EulerPacketLowConstants.gradientConstant EulerPacketLowConstants.hessianConstant ≤ B) : EulerPacketInduction.Stage S (n + 1)
  ```
- `EulerParentPacketFrames.Evolution.child` (def) | mass 0.73% | hidden 99 decls | statement 1422 chars
  ```lean
  EulerParentPacketFrames.Evolution.child.{u_1} {A : EulerParentPacketFrames.Parent} (E : EulerParentPacketFrames.Evolution A) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (m : EulerSmoothLimit.Space) (hm : ‖m‖ = 1) (J : U ≃ₗᵢ[ℝ] ↥(EulerTransverseFrameCoordinates.referencePlane m)) (support : Set EulerSmoothLimit.Space) (hSupport : IsCompact support) {P : ℝ} [Fact (0 < P)] {κ : ℝ} {hκ : |κ| ≤ 1} {Z R : ...
  ```
- `EulerPacketSourceGeometry.Guards.geometryData` (def, doc) | mass 0.69% | hidden 52 decls | statement 524 chars
  ```lean
  EulerPacketSourceGeometry.Guards.geometryData.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] {D : EulerTransversePacketProvider.Data U} {τ : ℝ} {hτ : 0 < τ} {hτT : τ < D.T} {P : EulerPacketSourceGeometry.ParentFrame D τ} {H : EulerTransversePacketProvider.HistoryData (D.initial τ hτ ⋯)} (A : EulerPacketSourceGeometry.Guards hτ hτT P H) (Ω : Set EulerSmoothLimit.Space) (h0 : 0 ∈ ...
  ```
  - `EulerPacketSourceGeometry.Guards.source_velocity_initial_error` (theorem) | mass 0.53% | hidden 35 decls | statement 761 chars
    - _passes through:_ `EulerPacketActivationHistory.actual_scaled_velocity_initial_error` → `EulerPacketActivationHistory.uncutVelocity_activation_difference` → `EulerPacketActivationHistory.labelVelocity_point_difference` → `EulerPacketActivationHistory.labelVelocity_difference` → `EulerTransverseHistoryBounds.historyVelocity_sub_norm_le_of_coefficient_bounds` → `EulerTransverseHistoryBounds.historyVelocity_sub_norm_le`
    ```lean
    EulerPacketSourceGeometry.Guards.source_velocity_initial_error.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] {D : EulerTransversePacketProvider.Data U} {τ : ℝ} {hτ : 0 < τ} {hτT : τ < D.T} {P : EulerPacketSourceGeometry.ParentFrame D τ} {H : EulerTransversePacketProvider.HistoryData (D.initial τ hτ ⋯)} (A : EulerPacketSourceGeometry.Guards hτ hτT P H) (x : EulerSmoothLimit.Spac ...
    ```
- `EulerPacketInductionScales.Scales.firstStage` (def) | mass 0.64% | hidden 57 decls | statement 133 chars
  ```lean
  EulerPacketInductionScales.Scales.firstStage {c B : ℝ} (S : EulerPacketInductionScales.Scales c B) : EulerPacketInduction.Stage S 0
  ```
- `EulerParentPacketFrames.SmoothState.packetChild` (def) | mass 0.62% | hidden 83 decls | statement 1702 chars
  - _passes through:_ `EulerParentPacketFrames.SobolevData.child`
  ```lean
  EulerParentPacketFrames.SmoothState.packetChild.{u_1} {A : EulerParentPacketFrames.Parent} (S : EulerParentPacketFrames.SmoothState A) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (m : EulerSmoothLimit.Space) (hm : ‖m‖ = 1) (J : U ≃ₗᵢ[ℝ] ↥(EulerTransverseFrameCoordinates.referencePlane m)) (support : Set EulerSmoothLimit.Space) (hSupport : IsCompact support) {P : ℝ} [Fact (0 < P)] {κ : ℝ} {hκ : |κ| ≤ ...
  ```
- `EulerTransversePacketPrimary.vector_compact_wave_history` (theorem) | mass 0.53% | hidden 43 decls | statement 687 chars
  - _passes through:_ `EulerTransversePacketPrimary.vector_eq_history` → `EulerTransversePacketEndpoint.velocityPath_eq_history` → `EulerCylinderDirichlet.Coefficients.endpointVelocity_pointwise`
  ```lean
  EulerTransversePacketPrimary.vector_compact_wave_history.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U] {D : EulerTransversePacketProvider.Data U} (τ : ℝ) (hτ : 0 < τ) (hτT : τ < D.T) (B : EulerTransversePacketProvider.HistoryData (D.initial τ hτ ⋯)) (δ : ℝ) (hδ : 0 < δ) (ξ : U) (hs : tsupport EulerSpatialCutoffs.innerCutoff ⊆ D.support) (t : ↑(Set.Icc 0 τ)) (x : EulerSmoothLimi ...
  ```
- `EulerPacketInitial.actual_increment_summable` (theorem) | mass 0.51% | hidden 82 decls | statement 932 chars
  ```lean
  EulerPacketInitial.actual_increment_summable {U : ℕ → Type} [(n : ℕ) → NormedAddCommGroup (U n)] [(n : ℕ) → InnerProductSpace ℝ (U n)] [∀ (n : ℕ), CompleteSpace (U n)] (A : (n : ℕ) → EulerPacketInitial.Input (U n)) (J : ℕ) (hJ : 2 ≤ J) (C c : ℝ) (hC : 0 < C) (hc : 0 ≤ c) (p q : ℕ) (X : ℝ) (hX : 1 ≤ X) (hparameter : ∀ (n : ℕ), (A n).parameterSize ≤ EulerPacketUniformFrequencyScales.parameterEnvelope J C c p q X n) (hs ...
  ```
- `EulerPacketInduction.Stage.forwardNext` (def) | mass 0.49% | hidden 44 decls | statement 391 chars
  ```lean
  EulerPacketInduction.Stage.forwardNext {q : ℕ} {B : ℝ} {S : EulerPacketInductionScales.Scales (↑q) B} (P : EulerPacketInduction.Stage S 0) (hq : EulerParentNeighborThreshold.requiredExponent ≤ q) (hB : EulerParentNeighborThreshold.commonThreshold EulerPacketLowConstants.gradientConstant EulerPacketLowConstants.hessianConstant ≤ B) : EulerPacketInduction.Stage S 1
  ```
- `EulerMeanHarmonic.weakHarmonic_pointwise_scaled` (theorem) | mass 0.45% | hidden 78 decls | statement 323 chars
  - _passes through:_ `EulerMeanHarmonic.weakScalarHarmonic_pointwise_scaled` → `EulerMeanHarmonic.weakScalarHarmonic_pointwise`
  ```lean
  EulerMeanHarmonic.weakHarmonic_pointwise_scaled (u : ↥EulerMeanSolenoidal.L2) (R : ℝ) (hR : 0 < R) (hu : EulerMeanHarmonic.WeakHarmonicOn (Metric.ball 0 R) u) : ∀ᵐ (x : EulerSmoothLimit.Space), x ∈ Metric.closedBall 0 (R / 4) → ‖↑↑u x‖ ^ 2 ≤ EulerMeanHarmonic.harmonicQuarterBallConstant * (R ^ 3)⁻¹ * ‖u‖ ^ 2
  ```
- `EulerAllOrderDriftCorrection.Budget.physicalFlowData` (def) | mass 0.43% | hidden 59 decls | statement 1438 chars
  ```lean
  EulerAllOrderDriftCorrection.Budget.physicalFlowData (P : ℝ) [Fact (0 < P)] {T : ℝ} {hT : 0 < T} {A : EulerAllOrderCorrectionData.Data P T} (B : EulerAllOrderDriftCorrection.Budget P hT A) {raw raw_t : EulerPacketProfileRecursion.VectorField} (G : EulerPacketCylinderField.Field P T raw) (H : EulerPacketCylinderField.Field P T raw_t) (hGfield : A.approximation = G.toFieldTower) (htime : EulerPacketCylinderField.TimeDe ...
  ```
- `EulerAllOrderDriftCorrection.Budget.commonPath_odd` (theorem, doc) | mass 0.42% | hidden 51 decls | statement 468 chars
  - _passes through:_ `EulerCorrectionAssembly.FiniteFamily.commonPath_odd`
  ```lean
  EulerAllOrderDriftCorrection.Budget.commonPath_odd (period : ℝ) [Fact (0 < period)] {T : ℝ} {hT : 0 < T} {A : EulerAllOrderCorrectionData.Data period T} (B : EulerAllOrderDriftCorrection.Budget period hT A) (P : EulerCorrectionAssembly.ParityData period A) (t : ↑(Set.Icc 0 T)) : -(EulerCylinderReflection.reflection period) ((EulerAllOrderDriftCorrection.Budget.commonPath period B) t) = (EulerAllOrderDriftCorrection.B ...
  ```

Trusting the 19 top-level statements skips **33.2%** of the proof mass (3,210 of 13,108 declarations). The other 66.8% (9,898 declarations) is the hub's own proof plus the shared layer and small regions not listed. The 40 outline statements and the spine mention 250 distinct project declarations directly; unfolding those definitions down to Mathlib takes 2126 project definitions, 128 of which sit inside the regions being skipped.

**Shared toolkit** (most-used declarations below this root; users counted below this root only):

| users | kind | name | statement |
|---|---|---|---|
| 6002 | def | `EulerSmoothLimit.Space` | `EulerSmoothLimit.Space : Type` |
| 3912 | def | `EulerLiftedGradientSpace.Vector3` | `EulerLiftedGradientSpace.Vector3 : Type` |
| 3436 | def | `EulerLiftedGradientSpace.LiftDomain` | `EulerLiftedGradientSpace.LiftDomain (period : ℝ) : Type` |
| 3025 | def | `EulerLiftedGradientSpace.liftMeasure` | `EulerLiftedGradientSpace.liftMeasure (period : ℝ) [Fact (0 < period)] : MeasureTheory.Measure (EulerLiftedGradientSpace.LiftDomain period)` |
| 2022 | def | `EulerLiftedGradientSpace.LiftL2` | `EulerLiftedGradientSpace.LiftL2 (period : ℝ) [Fact (0 < period)] : AddSubgroup (EulerLiftedGradientSpace.LiftDomain period →ₘ[EulerLiftedGradientSpace.liftMeasu ...` |
| 1643 | def | `EulerLiftedGradientSpace.LiftTangent` | `EulerLiftedGradientSpace.LiftTangent : Type` |
| 1639 | structure | `EulerTransversePacketProvider.Data` | `EulerTransversePacketProvider.Data.{u_1} (U : Type u_1) [NormedAddCommGroup U] [InnerProductSpace ℝ U] : Type u_1 \| EulerTransversePacketProvider.Data.mk : {U : ...` |
| 1169 | def | `EulerCylinderSobolevSpace.SobolevWord` | `EulerCylinderSobolevSpace.SobolevWord (q : ℕ) : Type` |
| 1153 | def | `EulerCylinderSobolevSpace.SobolevSpace` | `EulerCylinderSobolevSpace.SobolevSpace (period : ℝ) [Fact (0 < period)] (q : ℕ) : ClosedSubmodule ℝ (EulerCylinderSobolevSpace.SobolevWord q → ↥(EulerLiftedGrad ...` |
| 1148 | def | `EulerPacketProfileRecursion.VectorField` | `EulerPacketProfileRecursion.VectorField : Type` |
| 996 | def | `EulerLpCylinderTranslation.CylinderL2` | `EulerLpCylinderTranslation.CylinderL2.{u_1} (period : ℝ) [Fact (0 < period)] (V : Type u_1) [NormedAddCommGroup V] : AddSubgroup (EulerLiftedGradientSpace.LiftD ...` |
| 980 | def | `EulerMeanSolenoidal.L2` | `EulerMeanSolenoidal.L2 : AddSubgroup (EulerSmoothLimit.Space →ₘ[MeasureTheory.volume] EulerSmoothLimit.Space)` |
| 363 | theorem | `EulerPacketTerminalDatum.period_pos` | `EulerPacketTerminalDatum.period_pos : Fact (0 < EulerPacketTerminalDatum.period)` |
| 207 | theorem | `EulerTransversePacketProvider.Data.support_measurable` | `EulerTransversePacketProvider.Data.support_measurable.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Dat ...` |
| 86 | theorem | `EulerTransversePacketProvider.Data.clamp_coe` | `EulerTransversePacketProvider.Data.clamp_coe.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Data U) (t : ...` |
| 83 | theorem | `EulerMetricTransport.smoothField_continuous` | `EulerMetricTransport.smoothField_continuous.{u_1} (period : ℝ) {W : Type u_1} [NormedAddCommGroup W] [NormedSpace ℝ W] (f : EulerLiftedGradientSpace.LiftDomain ...` |
| 80 | theorem | `EulerCylinderSobolevSpace.value_injective` | `EulerCylinderSobolevSpace.value_injective (period : ℝ) [Fact (0 < period)] {q : ℕ} : Function.Injective (EulerCylinderSobolevSpace.value period)` |
| 79 | theorem | `EulerMeanSolenoidal.instCompleteSpaceSubtypeAEEqFunSpaceVolumeMemAddSubgroupL2SubmoduleRealSolenoidalSpace` | `EulerMeanSolenoidal.instCompleteSpaceSubtypeAEEqFunSpaceVolumeMemAddSubgroupL2SubmoduleRealSolenoidalSpace : CompleteSpace ↥EulerMeanSolenoidal.solenoidalSpace` |
| 69 | theorem | `EulerGevrey.majorant_nonneg` | `EulerGevrey.majorant_nonneg (R : ℝ) (hR : 0 ≤ R) (d n : ℕ) : 0 ≤ EulerGevrey.majorant R d n` |
| 69 | theorem | `EulerTransversePacketProvider.Data.frameLower_pos` | `EulerTransversePacketProvider.Data.frameLower_pos.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Data U) ...` |
| 63 | theorem | `EulerParameterWordGevrey.sobolevCoefficientAmplitude_nonneg` | `EulerParameterWordGevrey.sobolevCoefficientAmplitude_nonneg.{u_3} {ι : Type u_3} [Fintype ι] (q : ℕ) (Rc C : ℝ) (hRc : 0 ≤ Rc) (hC : 0 ≤ C) : 0 ≤ EulerParameter ...` |
| 58 | theorem | `EulerPacketSupport.compact` | `EulerPacketSupport.compact : IsCompact EulerPacketSupport.support` |
| 57 | theorem | `EulerPacketWeights.weight_pos` | `EulerPacketWeights.weight_pos {ρ : ℝ} (hρ : 0 < ρ) (n : ℕ) : 0 < EulerPacketWeights.weight ρ n` |
| 57 | theorem | `EulerLpCylinderTranslation.spatialSet_measurable` | `EulerLpCylinderTranslation.spatialSet_measurable (period : ℝ) (S : Set EulerSmoothLimit.Space) (hS : MeasurableSet S) : MeasurableSet (EulerLpCylinderTranslatio ...` |


## Euler.exists_compact_smooth_euler_singularity

Euler Theorem 1.1, alternate version (compact support, C^1 norm and vorticity integral blow up). Reaches 13,213 declarations, proof mass 22,418,831.

```lean
Euler.exists_compact_smooth_euler_singularity :
  ∃ u₀ Tstar v p,
    Euler.InitialVelocityConditionDecay u₀ ∧
      HasCompactSupport u₀ ∧
        u₀ ≠ 0 ∧
          0 < Tstar ∧
            Tstar ≤ 1 ∧
              Euler.EulerSobolevExistenceAndSmoothnessR3On (Set.Ico 0 Tstar) u₀ v p ∧
                (∃ E, ∀ t ∈ Set.Ico 0 Tstar, ∫ (x : EuclideanSpace ℝ (Fin 3)), ‖v x t‖ ^ 2 < E) ∧
                  (∀ (T : ℝ),
                      0 < T →
                        ((∃ w q,
                            Euler.EulerSobolevExistenceAndSmoothnessR3On (Set.Icc 0 T) u₀ w q) ↔
                          T < Tstar)) ∧
                    (∀ T ∈ Set.Ioo 0 Tstar,
                        (⨆ t ∈ Set.Icc 0 T, Euler.velocityC1Norm fun x => v x t) < ⊤ ∧
                          (∫⁻ (t : ℝ) in Set.Ico 0 T, Euler.vorticityNorm fun x => v x t) < ⊤) ∧
                      Filter.limsup (fun t => Euler.velocityC1Norm fun x => v x t)
                            (nhdsWithin Tstar (Set.Iio Tstar)) =
                          ⊤ ∧
                        (∫⁻ (t : ℝ) in Set.Ico 0 Tstar, Euler.vorticityNorm fun x => v x t) = ⊤ ∧
                          ¬∃ w q, Euler.EulerExistenceAndSmoothnessR3 u₀ w q
```

**Spine** (each statement is the only way into the one before it and carries at least 90% of its mass):

(none: the root itself is the hub; no single statement stands between it and the rest)

**Hub** `Euler.exists_compact_smooth_euler_singularity` has 5,938 dominator-tree children; 4,894 of them dominate nothing but themselves.

**Outline** (40 statements; mass = share of all proof mass below the root that sits under the statement, itself included; hidden = declarations a reader skips by trusting it):

- `EulerAllOrderDriftCorrection.finite_exists` (theorem, doc) | mass 8.88% | hidden 797 decls | statement 1512 chars **[waypoint-opaque]**
  - _passes through:_ `EulerDriftGlobalInviscidGevrey.exists_global_inviscid_gevrey_PDE`
  - `EulerDriftGevreyInviscidEnergyCompactness.exists_gevrey_inviscid_energy_limit` (theorem, doc) | mass 7.76% | hidden 668 decls | statement 3834 chars
    - _passes through:_ `EulerDriftViscousCorrectionFamily.exists_viscous_correction_family` → `EulerDriftGlobalGevreyCorrection.exists_global_gevrey_correction`
    - `EulerDriftPartialCorrectionBootstrap.partial_correction_bootstrap` (theorem, doc) | mass 6.33% | hidden 525 decls | statement 2891 chars
      - _passes through:_ `EulerDriftCorrectionBootstrap.correction_mild_bootstrap` → `EulerDriftCorrectionMildEnergy.correction_mild_integral`
    - `EulerCorrectionContinuation.exists_global_correction_of_bound` (theorem, doc) | mass 0.58% | hidden 60 decls | statement 1047 chars
      - _passes through:_ `EulerBoundedMildContinuation.exists_global_mild_of_bound`
- `EulerPacketMovingFrame.PhysicalGeometryData.exists_geometry` (theorem) | mass 6.41% | hidden 313 decls | statement 213 chars **[unreadable]**
  - `EulerPacketMovingFrame.physical_frame_renewal_order40` (theorem) | mass 1.35% | hidden 51 decls | statement 2538 chars
    - `EulerPacketFrameQuantitative.frame_renewal_order40` (theorem, doc) | mass 1.18% | hidden 31 decls | statement 1456 chars
  - `EulerPacketMovingFrame.physical_matrix_errors` (theorem, doc) | mass 0.56% | hidden 11 decls | statement 2826 chars
    - `EulerPacketCoefficientControl.raw_frame_matrix_errors` (theorem, doc) | mass 0.52% | hidden 10 decls | statement 1269 chars
  - `EulerPacketMovingFrame.physical_family_amplification_and_size` (theorem) | mass 0.43% | hidden 9 decls | statement 5841 chars
- `EulerParentPacketFrames.LabelData.forward_uniform_child` (theorem) | mass 2.17% | hidden 165 decls | statement 4007 chars **[unreadable]**
  - _passes through:_ `EulerPacketTerminalDatum.forward_uniform_child_label_bounds` → `EulerPacketTerminalDatum.forward_uniform_flow_and_shear`
  - `EulerPacketTerminalDatum.forwardUniformBudget` (def) | mass 0.44% | hidden 22 decls | statement 1697 chars
- `EulerPacketSourceGeometry.Guards.selection` (theorem) | mass 1.81% | hidden 151 decls | statement 1261 chars **[unreadable]**
  - _passes through:_ `EulerPacketActivationHistory.exists_activated_primary` → `EulerPacketActivationHistory.select_physical_history_coordinate` → `EulerPacketActivationHistory.select_history_coordinate`
  - `EulerTransverseActivationSelection.select_actual_activation` (theorem, doc) | mass 0.80% | hidden 51 decls | statement 2863 chars
- `Euler.initialDatum_no_global_solution (private)` (theorem) | mass 1.64% | hidden 306 decls | statement 130 chars **[restatement]**
  - `Euler.ComparatorBridge.compactCurlLocalUpgrade` (theorem, doc) | mass 1.36% | hidden 242 decls | statement 95 chars
    - `Euler.ComparatorBridge.exists_evolution_of_commonCompactCurl` (theorem, doc) | mass 0.51% | hidden 92 decls | statement 507 chars
    - `Euler.EulerExistenceAndSmoothnessR3.local_compact_vorticity_of_truncationFamily` (theorem, doc) | mass 0.44% | hidden 68 decls | statement 546 chars
- `EulerPacketInduction.Stage.chooseJoined` (def) | mass 1.57% | hidden 93 decls | statement 406 chars **[waypoint-opaque]**
  - _passes through:_ `EulerParentPacketFrames.exists_geometryJoinedChoice` → `EulerParentPacketFrames.LabelData.joined_uniform_child` → `EulerPacketTerminalDatum.initialized_uniform_child_label_bounds` → `EulerPacketTerminalDatum.initialized_uniform_flow_and_shear`
  - `EulerPacketTerminalDatum.initializedUniformBudget` (def) | mass 0.49% | hidden 22 decls | statement 1842 chars
- `EulerPacketInduction.constructionScales` (def) | mass 1.13% | hidden 92 decls | statement 81 chars **[waypoint-opaque]**
  - _passes through:_ `EulerPacketInductionScales.exists_scales`
  - `EulerPacketCommonScaleChoice.exists_common_guards` (theorem) | mass 0.87% | hidden 51 decls | statement 2452 chars
- `EulerMeanPacketProvider.Budget.grade_bounds` (theorem, doc) | mass 1.04% | hidden 147 decls | statement 971 chars
  - _passes through:_ `EulerMeanPacketProvider.Budget.grade_profile_bounds` → `EulerMeanPacketProvider.Budget.three_shift_bounds` → `EulerMeanPacketProvider.Budget.word_bounds_of_field` → `EulerMeanPacketProvider.Budget.word_bounds` → `EulerMeanPacketProvider.Budget.physical_word_bounds`
  - `EulerMeanPacketProvider.SobolevData.path_envelope_bounds` (theorem, doc) | mass 0.87% | hidden 116 decls | statement 1533 chars
    - _passes through:_ `EulerMeanPacketProvider.SobolevData.envelope_bounds`
    - `EulerMeanPacketProvider.SobolevData.normalized_bounds` (theorem, doc) | mass 0.74% | hidden 97 decls | statement 1684 chars
- `EulerOrdinarySobolev.FiniteLifespan.no_endpoint` (theorem) | mass 0.93% | hidden 152 decls | statement 212 chars
  - _passes through:_ `EulerOrdinarySobolev.HasEulerEvolution.extend` → `EulerOrdinarySobolev.Evolution.exists_extension`
- `EulerPacketInduction.Stage.joinedNext` (def) | mass 0.79% | hidden 82 decls | statement 417 chars
- `EulerParentPacketFrames.Evolution.child` (def) | mass 0.73% | hidden 99 decls | statement 1422 chars
- `EulerPacketSourceGeometry.Guards.geometryData` (def, doc) | mass 0.69% | hidden 52 decls | statement 524 chars
  - `EulerPacketSourceGeometry.Guards.source_velocity_initial_error` (theorem) | mass 0.52% | hidden 35 decls | statement 761 chars
    - _passes through:_ `EulerPacketActivationHistory.actual_scaled_velocity_initial_error` → `EulerPacketActivationHistory.uncutVelocity_activation_difference` → `EulerPacketActivationHistory.labelVelocity_point_difference` → `EulerPacketActivationHistory.labelVelocity_difference` → `EulerTransverseHistoryBounds.historyVelocity_sub_norm_le_of_coefficient_bounds` → `EulerTransverseHistoryBounds.historyVelocity_sub_norm_le`
- `EulerOrdinarySobolev.FiniteLifespan.vorticityIntegral_unbounded` (theorem, doc) | mass 0.69% | hidden 121 decls | statement 281 chars
  - `EulerOrdinarySobolev.logarithmic_gradient_bound_solenoidal` (theorem, doc) | mass 0.60% | hidden 96 decls | statement 472 chars
    - _passes through:_ `EulerOrdinarySobolev.logarithmic_gradient_bound` → `EulerWholeSpaceGaussian.elliptic_derivative_logarithmic` → `EulerWholeSpaceGaussian.elliptic_derivative_split`
- `EulerPacketInductionScales.Scales.firstStage` (def) | mass 0.64% | hidden 57 decls | statement 133 chars
- `EulerParentPacketFrames.SmoothState.packetChild` (def) | mass 0.62% | hidden 83 decls | statement 1702 chars
  - _passes through:_ `EulerParentPacketFrames.SobolevData.child`
- `EulerTransversePacketPrimary.vector_compact_wave_history` (theorem) | mass 0.53% | hidden 43 decls | statement 687 chars
  - _passes through:_ `EulerTransversePacketPrimary.vector_eq_history` → `EulerTransversePacketEndpoint.velocityPath_eq_history` → `EulerCylinderDirichlet.Coefficients.endpointVelocity_pointwise`
- `EulerPacketInitial.actual_increment_summable` (theorem) | mass 0.50% | hidden 82 decls | statement 932 chars
- `EulerPacketInduction.Stage.forwardNext` (def) | mass 0.49% | hidden 44 decls | statement 391 chars
- `EulerMeanHarmonic.weakHarmonic_pointwise_scaled` (theorem) | mass 0.44% | hidden 78 decls | statement 323 chars
  - _passes through:_ `EulerMeanHarmonic.weakScalarHarmonic_pointwise_scaled` → `EulerMeanHarmonic.weakScalarHarmonic_pointwise`
- `EulerAllOrderDriftCorrection.Budget.physicalFlowData` (def) | mass 0.43% | hidden 59 decls | statement 1438 chars
- `EulerAllOrderDriftCorrection.Budget.commonPath_odd` (theorem, doc) | mass 0.42% | hidden 51 decls | statement 468 chars
  - _passes through:_ `EulerCorrectionAssembly.FiniteFamily.commonPath_odd`

Trusting the 21 top-level statements skips **32.5%** of the proof mass (3,088 of 13,213 declarations). The other 67.5% (10,125 declarations) is the hub's own proof plus the shared layer and small regions not listed. The 40 outline statements and the spine mention 252 distinct project declarations directly; unfolding those definitions down to Mathlib takes 2127 project definitions, 117 of which sit inside the regions being skipped.

**Shared toolkit** (most-used declarations below this root; users counted below this root only):

| users | kind | name | statement |
|---|---|---|---|
| 6095 | def | `EulerSmoothLimit.Space` | `EulerSmoothLimit.Space : Type` |
| 3912 | def | `EulerLiftedGradientSpace.Vector3` | `EulerLiftedGradientSpace.Vector3 : Type` |
| 3436 | def | `EulerLiftedGradientSpace.LiftDomain` | `EulerLiftedGradientSpace.LiftDomain (period : ℝ) : Type` |
| 3025 | def | `EulerLiftedGradientSpace.liftMeasure` | `EulerLiftedGradientSpace.liftMeasure (period : ℝ) [Fact (0 < period)] : MeasureTheory.Measure (EulerLiftedGradientSpace.LiftDomain period)` |
| 2022 | def | `EulerLiftedGradientSpace.LiftL2` | `EulerLiftedGradientSpace.LiftL2 (period : ℝ) [Fact (0 < period)] : AddSubgroup (EulerLiftedGradientSpace.LiftDomain period →ₘ[EulerLiftedGradientSpace.liftMeasu ...` |
| 1643 | def | `EulerLiftedGradientSpace.LiftTangent` | `EulerLiftedGradientSpace.LiftTangent : Type` |
| 1639 | structure | `EulerTransversePacketProvider.Data` | `EulerTransversePacketProvider.Data.{u_1} (U : Type u_1) [NormedAddCommGroup U] [InnerProductSpace ℝ U] : Type u_1 \| EulerTransversePacketProvider.Data.mk : {U : ...` |
| 1169 | def | `EulerCylinderSobolevSpace.SobolevWord` | `EulerCylinderSobolevSpace.SobolevWord (q : ℕ) : Type` |
| 1153 | def | `EulerCylinderSobolevSpace.SobolevSpace` | `EulerCylinderSobolevSpace.SobolevSpace (period : ℝ) [Fact (0 < period)] (q : ℕ) : ClosedSubmodule ℝ (EulerCylinderSobolevSpace.SobolevWord q → ↥(EulerLiftedGrad ...` |
| 1148 | def | `EulerPacketProfileRecursion.VectorField` | `EulerPacketProfileRecursion.VectorField : Type` |
| 996 | def | `EulerLpCylinderTranslation.CylinderL2` | `EulerLpCylinderTranslation.CylinderL2.{u_1} (period : ℝ) [Fact (0 < period)] (V : Type u_1) [NormedAddCommGroup V] : AddSubgroup (EulerLiftedGradientSpace.LiftD ...` |
| 984 | def | `EulerMeanSolenoidal.L2` | `EulerMeanSolenoidal.L2 : AddSubgroup (EulerSmoothLimit.Space →ₘ[MeasureTheory.volume] EulerSmoothLimit.Space)` |
| 363 | theorem | `EulerPacketTerminalDatum.period_pos` | `EulerPacketTerminalDatum.period_pos : Fact (0 < EulerPacketTerminalDatum.period)` |
| 207 | theorem | `EulerTransversePacketProvider.Data.support_measurable` | `EulerTransversePacketProvider.Data.support_measurable.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Dat ...` |
| 86 | theorem | `EulerTransversePacketProvider.Data.clamp_coe` | `EulerTransversePacketProvider.Data.clamp_coe.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Data U) (t : ...` |
| 83 | theorem | `EulerMetricTransport.smoothField_continuous` | `EulerMetricTransport.smoothField_continuous.{u_1} (period : ℝ) {W : Type u_1} [NormedAddCommGroup W] [NormedSpace ℝ W] (f : EulerLiftedGradientSpace.LiftDomain ...` |
| 80 | theorem | `EulerCylinderSobolevSpace.value_injective` | `EulerCylinderSobolevSpace.value_injective (period : ℝ) [Fact (0 < period)] {q : ℕ} : Function.Injective (EulerCylinderSobolevSpace.value period)` |
| 79 | theorem | `EulerMeanSolenoidal.instCompleteSpaceSubtypeAEEqFunSpaceVolumeMemAddSubgroupL2SubmoduleRealSolenoidalSpace` | `EulerMeanSolenoidal.instCompleteSpaceSubtypeAEEqFunSpaceVolumeMemAddSubgroupL2SubmoduleRealSolenoidalSpace : CompleteSpace ↥EulerMeanSolenoidal.solenoidalSpace` |
| 69 | theorem | `EulerGevrey.majorant_nonneg` | `EulerGevrey.majorant_nonneg (R : ℝ) (hR : 0 ≤ R) (d n : ℕ) : 0 ≤ EulerGevrey.majorant R d n` |
| 69 | theorem | `EulerTransversePacketProvider.Data.frameLower_pos` | `EulerTransversePacketProvider.Data.frameLower_pos.{u_1} {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Data U) ...` |
| 63 | theorem | `EulerParameterWordGevrey.sobolevCoefficientAmplitude_nonneg` | `EulerParameterWordGevrey.sobolevCoefficientAmplitude_nonneg.{u_3} {ι : Type u_3} [Fintype ι] (q : ℕ) (Rc C : ℝ) (hRc : 0 ≤ Rc) (hC : 0 ≤ C) : 0 ≤ EulerParameter ...` |
| 58 | theorem | `EulerLpTranslation.SmoothL2Field.toLp_ae` | `EulerLpTranslation.SmoothL2Field.toLp_ae.{u} {V : Type u} [NormedAddCommGroup V] [NormedSpace ℝ V] (A : EulerLpTranslation.SmoothL2Field V) : ↑↑A.toLp =ᵐ[Measur ...` |
| 58 | theorem | `EulerPacketSupport.compact` | `EulerPacketSupport.compact : IsCompact EulerPacketSupport.support` |
| 57 | theorem | `EulerPacketWeights.weight_pos` | `EulerPacketWeights.weight_pos {ρ : ℝ} (hρ : 0 < ρ) (n : ℕ) : 0 < EulerPacketWeights.weight ρ n` |

