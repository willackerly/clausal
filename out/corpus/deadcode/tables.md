### T1. Unreachable declarations by kind

| kind | all | not reachable from a headline theorem | share |
|---|---:|---:|---:|
| theorem | 38,601 | 12,516 | 32.4% |
| def | 11,721 | 2,298 | 19.6% |
| instance | 1,517 | 465 | 30.7% |
| structure | 652 | 152 | 23.3% |
| inductive | 14 | 4 | 28.6% |
| **all** | 52,505 | 15,435 | 29.4% |

### T2. By library

| library | declarations | unreachable | share | theorems | unreachable theorems | share |
|---|---:|---:|---:|---:|---:|---:|
| NavierStokes | 36,203 | 12,347 | 34.1% | 27,301 | 10,151 | 37.2% |
| Euler | 16,302 | 3,088 | 18.9% | 11,300 | 2,365 | 20.9% |

### T3. By source lines

| measure | lines |
|---|---:|
| all lines of the 2,657 project files | 640,860 |
| lines inside a declaration (Lean declaration ranges, plus `omit/include ... in` prefixes) | 510,729 |
| ... of unreachable declarations | 157,444 (30.8% of declaration lines, 24.6% of all lines) |
| proof size (distinct subterms) of unreachable theorems | 13,183,334 of 48,624,258 (27.1%) |

### T4. Modules

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

### T5. Cloned modules (the 13 of REUSE.md section 1.7)

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

### T6. Status of the unreachable declarations

| status | declarations | declaration lines | by kind |
|---|---:|---:|---|
| named in the source of a reachable declaration, absent from its term (elaboration-only dependency) | 176 | 382 | 176 theorem |
| held back: carries an attribute, is an instance or an abbreviation, is named in a command of a kept file, or is needed by one of those | 1,634 | 5,279 | 700 theorem, 465 instance, 396 def, 72 structure, 1 inductive |
| **classified dead** | **13,625** | **151,783** | 11,640 theorem, 1,902 def, 80 structure, 3 inductive |

Why declarations are held back (a declaration can carry several tags; 1,303 tagged declarations pull in the rest as dependencies):

| tag | unreachable declarations |
|---|---:|
| simp | 743 |
| instance | 474 |
| abbrev | 139 |
| cmd:variable | 84 |
| cmd:export | 8 |
| other-attribute | 3 |
| cmd:open | 2 |
| no-source-range | 1 |

### T7. (a) / (b) / (c) by the stated rule

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

### T8. Negative control: 20 used declarations deleted one at a time

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

19 of 20 builds failed.

