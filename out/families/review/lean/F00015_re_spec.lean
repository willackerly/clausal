import Tool
import NavierStokes.ActualCyclePeriodicity
import NavierStokes.CorrectionStep
import NavierStokes.DefectIncrementBounds
import NavierStokes.GaugeDebtIncrement
import NavierStokes.HarmonicResidual
import NavierStokes.HarmonicSourceSupport
import NavierStokes.LocalRankDefect
import NavierStokes.MeanIncrementBounds
import NavierStokes.MeanStateRegularity
import NavierStokes.MovingMomentBounds
import NavierStokes.PhysicalResidualNaturality
import NavierStokes.PrimaryCopyBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.sub 18 39
run_cmd IO.println "BLOCK NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualCyclePeriodicity
open Set Function Filter CorrectionState CorrectionStep CorrectionInitialization
open HarmonicFields HarmonicResidual
open ActualWaveRegularity
open scoped Topology ContDiff BigOperators ComplexConjugate
section TranslationCalculus
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace CoefficientsTranslation
variable {U : Set D} {v : D} {a b : HarmonicFields.Coefficients D}
omit [NormedSpace ℝ D] in
#count_heartbeats in
theorem sub_S (ha : CoefficientsTranslation U v a) (hb : CoefficientsTranslation U v b) :
    CoefficientsTranslation U v (a - b) :=
  fun j => (ha j).map₂ (hb j) (· - ·)
end CoefficientsTranslation
end TranslationCalculus
end NavierStokes.ActualCyclePeriodicity
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.sub 43 234
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CorrectionStep
open Set WeightedClasses MeanIncrementBounds
open scoped ContDiff BigOperators
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
section CovarianceChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  {b m : Triple D} (hb : SmoothTriple U b) (hm : SmoothTriple U m)
  (W X : Tensor D) (hW : ∀ i j, SmoothOn U (W i j))
  (hX : ∀ i j, SmoothOn U (X i j))
end CovarianceChanges
section JointChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U)
  {b m h : Triple D} (hb : SmoothTriple U b) (hm : SmoothTriple U m)
  (hh : SmoothTriple U h) (W X : Tensor D)
  (hW : ∀ i j, SmoothOn U (W i j)) (hX : ∀ i j, SmoothOn U (X i j))
end JointChanges
section CovarianceBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
  (ho : OperatorBounds s o κ) {X : Tensor D} (hX : TensorClass s α X)
end CovarianceBounds
section FullCalculus
open HarmonicCalculus LinearWaveResidual
end FullCalculus
section FullFields
open CorrectionState HarmonicCalculus
end FullFields
section ActualCovariance
open CorrectionState MeasureTheory
end ActualCovariance
section ActualFullUpdate
open CorrectionState HarmonicCalculus
end ActualFullUpdate
section TemporalComposition
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalComposition
section TemporalAngularGain
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalAngularGain
section TemporalPressureAndAxial
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalPressureAndAxial
section PhysicalRepresentation
open CorrectionState
variable {P : Type}
end PhysicalRepresentation
section RankMeanComposition
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end RankMeanComposition
section ExcludedMeanErrors
open CorrectionState MeasureTheory
end ExcludedMeanErrors
section ConcreteRankConstruction
open CorrectionState
end ConcreteRankConstruction
section RankPressureConstruction
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end RankPressureConstruction
section PressureAliasBookkeeping
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end PressureAliasBookkeeping
section ActualHarmonicForcing
open CorrectionState
end ActualHarmonicForcing
section TemporalMasses
open CorrectionState MeasureTheory
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalMasses
section ActualMeanAndDivergence
open CorrectionState
end ActualMeanAndDivergence
section MeanDivergencePreservation
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end MeanDivergencePreservation
section CommonTemporalConstruction
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end CommonTemporalConstruction
section CommonTemporalScale
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end CommonTemporalScale
section HarmonicStateUpdates
open CorrectionState
end HarmonicStateUpdates
section MeanWaveComposition
open CorrectionState
end MeanWaveComposition
section RankRetainedAlias
open CorrectionState
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end RankRetainedAlias
section SignedTensorRemainder
open CorrectionState MeasureTheory
end SignedTensorRemainder
section LocalMeanConstruction
open CorrectionState PhysicalMeanDomain
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalMeanConstruction
section ConstructedSignedBlocks
open CorrectionState SignedWaveUpdate
end ConstructedSignedBlocks
section CumulativeWaveUpdates
open CorrectionState
end CumulativeWaveUpdates
section LocalCommonClock
open CorrectionState PhysicalMeanDomain
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalCommonClock
section GaugeMeanBookkeeping
open CorrectionState VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end GaugeMeanBookkeeping
section GaugeTemporalResidual
open CorrectionState VariableGaugeMean PhysicalMeanDomain
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end GaugeTemporalResidual
section GaugeTemporalGain
open CorrectionState VariableGaugeMean PhysicalMeanDomain
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end GaugeTemporalGain
section GaugeAliasBookkeeping
open CorrectionState VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end GaugeAliasBookkeeping
section PhysicalResidualDecomposition
open CorrectionState PhysicalResidualBridge ProblemStatement Filter
open scoped Topology
end PhysicalResidualDecomposition
section SourceCoefficientCompatibility
open CorrectionState HarmonicFields MeasureTheory
end SourceCoefficientCompatibility
section AssembledSignedTensor
open CorrectionState
variable {ι : Type}
end AssembledSignedTensor
section WaveStageGain
open CorrectionState
end WaveStageGain
section WaveMeanResidual
open CorrectionState VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end WaveMeanResidual
section SignedParameters
open CorrectionState
end SignedParameters
section ActualSignedStage
open CorrectionState
end ActualSignedStage
section LinearCoefficientBridge
open CorrectionState
end LinearCoefficientBridge
section ConstructedSignedLinear
open CorrectionState
end ConstructedSignedLinear
section ConstructedSignedInvariants
open CorrectionState
open scoped InnerProductSpace
end ConstructedSignedInvariants
section GaugeRankMean
open CorrectionState VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end GaugeRankMean
section MovingSupport
open CorrectionState VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
namespace GaugeSupported
variable {a b : ℝ} {ell : S → ℝ} {U : Set S}
  {f g : ScalarField (PressureStream.Lift S)}
omit [NormedAddCommGroup S] [NormedSpace ℝ S] in
#count_heartbeats in
theorem sub_S (hf : GaugeSupported a b ell U f) (hg : GaugeSupported a b ell U g) :
    GaugeSupported a b ell U (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.DefectIncrementBounds.Shell.sub 238 254
run_cmd IO.println "BLOCK NavierStokes.DefectIncrementBounds.Shell.sub"
section
set_option linter.all false
namespace NavierStokes.DefectIncrementBounds
noncomputable section
open Set Function MeasureTheory Filter
open scoped ContDiff Topology Interval
open WeightedClasses MeanIncrementBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
namespace Shell
variable {a b : ℝ} {f g : ScalarField (Point P)}
#count_heartbeats in
theorem sub_S (hf : Shell a b f) (hg : Shell a b g) : Shell a b (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end Shell
end
end NavierStokes.DefectIncrementBounds
end

-- REPLAY NavierStokes.GaugeDebtIncrement.Regular.sub 258 273
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.Regular.sub"
section
set_option linter.all false
namespace NavierStokes.GaugeDebtIncrement
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval BigOperators
open WeightedClasses MeanIncrementBounds CorrectionState LocalSignedRequest
namespace Regular
variable {coord a b : ℝ} {U : SlowRegion coord} {f g : Scalar}
#count_heartbeats in
theorem sub_S (hf : Regular U a b f) (hg : Regular U a b g) : Regular U a b (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end Regular
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.MeanStateRegularity.MovingField.sub 277 300
run_cmd IO.println "BLOCK NavierStokes.MeanStateRegularity.MovingField.sub"
section
set_option linter.all false
namespace NavierStokes.MeanStateRegularity
noncomputable section
open Set Function Filter
open scoped ContDiff Topology
open MeanIncrementBounds CorrectionState LocalSignedRequest
namespace Periodic
variable {U : Set Plane} {f g : Scalar}
end Periodic
namespace OperatorData
variable {U : Set Plane} {o : Operators Point}
end OperatorData
namespace MovingField
variable {coord a b : ℝ} {U : SlowRegion coord} {f g : Scalar}
#count_heartbeats in
theorem sub_S (hf : GaugeMomentBalances.MovingField U a b f)
    (hg : GaugeMomentBalances.MovingField U a b g) :
    GaugeMomentBalances.MovingField U a b (f - g) :=
  of_regular ((regular hf).sub (regular hg)) (Periodic.sub hf.periodic hg.periodic)
end MovingField
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.HarmonicResidual.band_sub 304 319
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.band_sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
omit [NormedAddCommGroup D] [NormedSpace ℝ D] in
#count_heartbeats in
theorem band_sub_S {c d : Coefficients D} {N : ℕ} (hc : BandLimited c N)
    (hd : BandLimited d N) : BandLimited (c - d) N := by
  simpa only [sub_eq_add_neg] using hc.add (band_neg hd)
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicResidual.SmoothCoefficients.sub 323 337
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.SmoothCoefficients.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
#count_heartbeats in
theorem SmoothCoefficients.sub_S {U : Set D} {c d : Coefficients D}
    (hc : SmoothCoefficients U c) (hd : SmoothCoefficients U d) : SmoothCoefficients U (c - d) :=
  fun j => (hc j).sub (hd j)
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicSourceSupport.NonzeroSupported.sub 341 358
run_cmd IO.println "BLOCK NavierStokes.HarmonicSourceSupport.NonzeroSupported.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicSourceSupport
open Set Function Filter HarmonicFields HarmonicResidual HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace NonzeroSupported
variable {K : Set D} {c d : HarmonicFields.Coefficients D}
omit [NormedAddCommGroup D] [NormedSpace ℝ D] in
#count_heartbeats in
theorem sub_S (hc : NonzeroSupported K c) (hd : NonzeroSupported K d) :
    NonzeroSupported K (c - d) := by
  simpa only [sub_eq_add_neg] using hc.add hd.neg
end NonzeroSupported
end NavierStokes.HarmonicSourceSupport
end
end

-- REPLAY NavierStokes.LocalRankDefect.LocalShell.sub 362 379
run_cmd IO.println "BLOCK NavierStokes.LocalRankDefect.LocalShell.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalRankDefect
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval
open WeightedClasses MeanIncrementBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
namespace LocalShell
variable {a b : ℝ} {U : Set P} {f g : ScalarField (Point P)}
#count_heartbeats in
theorem sub_S (hf : LocalShell a b U f) (hg : LocalShell a b U g) :
    LocalShell a b U (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end LocalShell
end NavierStokes.LocalRankDefect
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.SmoothOn.sub 383 400
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.SmoothOn.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MeanIncrementBounds
open Set Filter WeightedClasses
open scoped ContDiff Topology
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace Operators
end Operators
namespace SmoothOn
variable {U : Set D} {f g : Field D}
#count_heartbeats in
theorem sub_S (hf : SmoothOn U f) (hg : SmoothOn U g) : SmoothOn U (f - g) :=
  hf.add hg.neg
end SmoothOn
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanStateRegularity.Periodic.sub 404 419
run_cmd IO.println "BLOCK NavierStokes.MeanStateRegularity.Periodic.sub"
section
set_option linter.all false
namespace NavierStokes.MeanStateRegularity
noncomputable section
open Set Function Filter
open scoped ContDiff Topology
open MeanIncrementBounds CorrectionState LocalSignedRequest
namespace Periodic
variable {U : Set Plane} {f g : Scalar}
#count_heartbeats in
theorem sub_S (hf : Periodic U f) (hg : Periodic U g) : Periodic U (f - g) :=
  fun n R s hs Y k => congrArg₂ (· - ·) (hf n R s hs Y k) (hg n R s hs Y k)
end Periodic
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.sub 423 451
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MovingMomentBounds
open Set Filter MeasureTheory CorrectionState WeightedClasses MeanIncrementBounds
open VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology BigOperators
section Moments
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
include hab
end Moments
open Set Filter MeasureTheory CorrectionState WeightedClasses MeanIncrementBounds
open VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology BigOperators
section Support
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
namespace Support
variable {a b : ℝ} {ell : S → ℝ} {U : Set S} {f g : ScalarField (PressureStream.Lift S)}
omit [NormedAddCommGroup S] [NormedSpace ℝ S] in
#count_heartbeats in
theorem sub_S (hf : Support a b ell U f) (hg : Support a b ell U g) : Support a b ell U (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.CoefficientsOn.sub 455 477
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.CoefficientsOn.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PhysicalResidualNaturality
open Set Filter
open scoped Topology ComplexConjugate
open HarmonicCalculus HarmonicFields
variable {D E F : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
namespace CoefficientsOn
#count_heartbeats in
theorem sub_S {U : Set D} {e : D ≃L[ℝ] E} {a : ℝ}
    {c₁ c₂ : Coefficients D} {d₁ d₂ : Coefficients E}
    (h₁ : CoefficientsOn U e a c₁ d₁) (h₂ : CoefficientsOn U e a c₂ d₂) :
    CoefficientsOn U e a (c₁ - c₂) (d₁ - d₂) := by
  intro j x hx
  change c₁ j x - c₂ j x = a • (d₁ j (e x) - d₂ j (e x))
  rw [h₁ j x hx, h₂ j x hx, smul_sub]
end CoefficientsOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.ScalarOn.sub 481 508
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.ScalarOn.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PhysicalResidualNaturality
open Set Filter
open scoped Topology ComplexConjugate
open HarmonicCalculus HarmonicFields
variable {D E F : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
namespace CoefficientsOn
end CoefficientsOn
namespace FrameOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c l : ℝ}
  {g : HarmonicResidual.Frame D} {r : HarmonicResidual.Frame E}
end FrameOn
open PhysicalParticularWave CommonCoverSolve
namespace ScalarOn
#count_heartbeats in
theorem sub_S {U : Set D} {e : D ≃L[ℝ] E} {a : ℝ} {f v : D → ℝ} {g w : E → ℝ}
    (hf : ScalarOn U e a f g) (hv : ScalarOn U e a v w) : ScalarOn U e a (f-v) (g-w) := by
  intro x hx
  change f x - v x = a * (g (e x) - w (e x))
  rw [hf x hx, hv x hx, mul_sub]
end ScalarOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.PrimaryCopyBounds.NativeJets.sub 512 532
run_cmd IO.println "BLOCK NavierStokes.PrimaryCopyBounds.NativeJets.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PrimaryCopyBounds
open Set Function Filter PhaseJetBounds PrimaryPulseBounds WeightedClasses
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {ι : Type*} {D : Type} {E F G : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace NativeJets
variable {V : JetDomain ι D} {w v : ι → D → ℝ} {f g : ι → D → E}
#count_heartbeats in
theorem sub_S (hf : NativeJets V w f) (hg : NativeJets V w g) :
    NativeJets V w (fun i x => f i x - g i x) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end NativeJets
end NavierStokes.PrimaryCopyBounds
end
end

