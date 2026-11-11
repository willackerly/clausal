import Tool
import F15
import NavierStokes.CorrectionInitializationNoOptions
import NavierStokes.CorrectionStep
import NavierStokes.GaugeDebtIncrement
import NavierStokes.HarmonicFields
import NavierStokes.HarmonicResidual
import NavierStokes.MeanStateRegularity
import NavierStokes.PhysicalResidualNaturality
import NavierStokes.PrimaryResidualClass
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.GaugeDebtIncrement.waveStage_debt_change_mem 15 97
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.waveStage_debt_change_mem"
section
set_option linter.all false
namespace NavierStokes.GaugeDebtIncrement
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval BigOperators
open WeightedClasses MeanIncrementBounds CorrectionState LocalSignedRequest
namespace Regular
variable {coord a b : ℝ} {U : SlowRegion coord} {f g : Scalar}
end Regular
namespace RegularTriple
variable {coord a b : ℝ} {U : SlowRegion coord} {m h base : Triple Point}
end RegularTriple
section Moments
variable {coord a b cL cR : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b)
include ha hab
end Moments
section DebtIdentity
variable {coord a b : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b)
    (c : Context Point) (u v : State Point)
    (hgu : Regular U a b (u.gr c)) (hgv : Regular U a b (v.gr c))
    (htu : Regular U a b (thetaAxial c.base u.mean + u.covariance 2 1))
    (htv : Regular U a b (thetaAxial c.base v.mean + v.covariance 2 1))
    (hzu : Regular U a b (axialAxial c.base u.mean + u.covariance 2 2))
    (hzv : Regular U a b (axialAxial c.base v.mean + v.covariance 2 2))
end DebtIdentity
section MomentClasses
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
include hab
end MomentClasses
section DomainTools
end DomainTools
section WaveAlgebra
variable (g : VariableGaugeMean.GaugeData Plane) (c : Context Point) (u : State Point)
    (w : Oscillation Point) (q : OscillatoryScalar Point) (gaussian : Oscillation Point)
end WaveAlgebra
section WaveRegularity
variable {coord a b : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b)
    (g : VariableGaugeMean.GaugeData Plane) (c : Context Point) (u : State Point)
    (w : Oscillation Point) (q : OscillatoryScalar Point) (gaussian : Oscillation Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hW : ∀ i j, Regular U a b (u.covariance i j))
    (hX : ∀ i j, Regular U a b (SignedMeanGain.covarianceIncrement u.oscillation w i j))
include ha hab hop hb hm hW hX
end WaveRegularity
section WaveBounds
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (g : VariableGaugeMean.GaugeData Plane) (c : Context Point) (u : State Point)
    (w : Oscillation Point) (q : OscillatoryScalar Point) (gaussian : Oscillation Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hW : ∀ i j, Regular U a b (u.covariance i j))
    (hX : ∀ i j, Regular U a b (SignedMeanGain.covarianceIncrement u.oscillation w i j))
include hab hop hb hm hW hX
#count_heartbeats in
theorem waveStage_debt_change_mem_R {κ α : ℝ}
    (ho : OperatorBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) c.operators κ)
    (hcX : SignedMeanGain.TensorClass (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) α
      (SignedMeanGain.covarianceIncrement u.oscillation w)) (i : Fin 3) :
    UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL) (α - κ)
      (fun n x => debt c (SignedMeanGain.waveStage g c u w q gaussian) n x i - debt c u n x i) := by
  have hR : Regular U a b (SignedMeanGain.radialCovarianceChange c.operators
      (SignedMeanGain.covarianceIncrement u.oscillation w)) :=
    (((hX 0 0).radialDiv ha hab hop 1).neg.sub ((hX 2 0).dz c.operators)).add
      ((hX 1 1).inv_mul ha hab hop)
  have hclass := momentChange_mem U ha hab hcL hcR ε L hε hεone hL hR (hX 2 1) (hX 2 2)
    (SignedMeanGain.radialCovarianceChange_mem ho hcX)
    ((hcX 2 1).mono_exponent (by linarith [ho.kappa_nonneg]))
    ((hcX 2 2).mono_exponent (by linarith [ho.kappa_nonneg])) i
  apply class_congr hclass
  intro n x hx
  exact congrFun (waveStage_debt_change_formula U ha hab g c u w q gaussian hop hb hm hW hX n hx) i
end WaveBounds
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.HarmonicFields.band_single_zero 101 115
run_cmd IO.println "BLOCK NavierStokes.HarmonicFields.band_single_zero"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped BigOperators Topology ContDiff ComplexConjugate Pointwise
namespace NavierStokes.HarmonicFields
#count_heartbeats in
theorem band_single_zero_R {α : Type*} (a : α → ℂ) :
    BandLimited (AddMonoidAlgebra.single (0 : ℤ) a : Coefficients α) 0 := by
  intro j hj
  have hj0 : j = 0 := Finset.mem_singleton.mp (Finsupp.support_single_subset hj)
  simp [hj0]
end NavierStokes.HarmonicFields
end
end

-- REPLAY NavierStokes.GaugeDebtIncrement.RegularTriple.radialRadial 119 139
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.RegularTriple.radialRadial"
section
set_option linter.all false
namespace NavierStokes.GaugeDebtIncrement
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval BigOperators
open WeightedClasses MeanIncrementBounds CorrectionState LocalSignedRequest
namespace Regular
variable {coord a b : ℝ} {U : SlowRegion coord} {f g : Scalar}
end Regular
namespace RegularTriple
variable {coord a b : ℝ} {U : SlowRegion coord} {m h base : Triple Point}
#count_heartbeats in
theorem radialRadial_R (hm : RegularTriple U a b m) (ha : 0 < a) (hab : a < b)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) base) :
    Regular U a b (MeanIncrementBounds.radialRadial base m) :=
  ((hm.radial.coefficient_mul ha hab hb.radial).smul 2).add (hm.radial.mul hm.radial)
end RegularTriple
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.TripleOn.axialAxial 143 178
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.TripleOn.axialAxial"
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
end ScalarOn
namespace FrameOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c l : ℝ}
  {C : CorrectionState.Context D} {Cr : CorrectionState.Context E} {n nr : ℕ}
  (H : FrameOn U e c l (HarmonicResidual.contextFrame C n) (HarmonicResidual.contextFrame Cr nr))
include H
end FrameOn
namespace TripleOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c : ℝ} {n nr : ℕ}
  {b m : MeanIncrementBounds.Triple D} {br mr : MeanIncrementBounds.Triple E}
#count_heartbeats in
theorem axialAxial_R (hb : TripleOn U e c b br n nr) (hm : TripleOn U e c m mr n nr) :
    ScalarOn U e (c*c) (MeanIncrementBounds.axialAxial b m n) (MeanIncrementBounds.axialAxial br mr nr) :=
  ((hb.axial.mul hm.axial).smul 2).add (hm.axial.mul hm.axial)
end TripleOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.time 182 374
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.time"
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
#count_heartbeats in
theorem time_R (hf : GaugeSupported a b ell U f) (hU : IsOpen U)
    (hell : ContinuousOn ell U) (o : Operators (PressureStream.Lift S)) :
    GaugeSupported a b ell U (o.time f) :=
  ((hf.directional hU hell o.eT).mul_left (fun n _ => o.epsilon n)).neg.add
    ((hf.directional hU hell o.vT).mul_left (fun n _ => o.fastCoefficient n))
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionInitializationNoOptions.zeroMean_debt_mem 378 496
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitializationNoOptions.zeroMean_debt_mem"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CorrectionInitializationNoOptions
open Set Filter MeasureTheory CorrectionState MovingMomentBounds
open scoped BigOperators ContDiff Topology InnerProductSpace
section Partition
open PartitionedCovariance
variable {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
  {D h : ℝ} {vr vt : Plane}
end Partition
section Primary
open WeightedClasses LinearWaveBounds HarmonicCalculus
variable {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
namespace PrimaryPiece
end PrimaryPiece
end Primary
section PrimarySupport
open LinearWaveBounds HarmonicCalculus
variable {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
namespace PrimaryPiece
end PrimaryPiece
end PrimarySupport
namespace PrimaryConstruction
open WeightedClasses LinearWaveBounds
variable {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
section NativePair
open PartitionedCovariance
variable {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow}
  {d h : ℝ} {vr vt : Plane}
end NativePair
end PrimaryConstruction
section PrimaryExcluded
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace PrimaryPiece
end PrimaryPiece
end PrimaryExcluded
section Construction
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {ι : Type}
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end Construction
namespace GaugeInitialization
open VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] {ι : Type}
end GaugeInitialization
namespace GaugeInitialization
open VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] {ι : Type}
end GaugeInitialization
section InitializedExcludedMean
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {ι : Type}
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end InitializedExcludedMean
section BandExcludedMean
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {ι : Type}
namespace GaugeInitialization
open VariableGaugeMean
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end GaugeInitialization
end BandExcludedMean
namespace AngularRestriction
open WeightedClasses
variable {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end AngularRestriction
namespace PrimaryHarmonics
open WeightedClasses HarmonicFields
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end PrimaryHarmonics
section PrimaryBlocks
open WeightedClasses LinearWaveBounds HarmonicCalculus
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace PrimaryPiece
end PrimaryPiece
end PrimaryBlocks
section ZeroMean
open MeanIncrementBounds WeightedClasses
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end ZeroMean
section InitialMeanBounds
open MeanIncrementBounds WeightedClasses WeightedRadialPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
#count_heartbeats in
theorem zeroMean_debt_mem_R
    {a b cL cR : ℝ} (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (c : Context (Lift S)) (u : State (Lift S))
    (ho : OperatorBounds (logStripData a b cL cR ha hcL hcR ε L hε hεone hL)
      c.operators ChartScales.kappa)
    (hop : DefectIncrementBounds.PositiveOperators c.operators)
    (hm : u.mean = ⟨0, 0, 0⟩)
    (hW : ∀ i j, MeanClass (logStripData a b cL cR ha hcL hcR ε L hε hεone hL)
      1 (u.covariance i j))
    (hWs : ∀ i j, DefectIncrementBounds.Shell a b (u.covariance i j)) (i : Fin 3) :
    UnweightedClass (MeanMomentBounds.slowStripData (D := S) ε L hε hεone hL)
      (1 - ChartScales.kappa) (fun n x => debt c u n x i) := by
  have hg := zeroMean_gr_mem c u ho hm hW
  have hgs := zeroMean_gr_shell ha c u hop hm hWs
  have hP := DefectIncrementBounds.barMoment_mem ha hab hcL hcR ε L hε hεone hL hgs hg 0
  have hP2 := DefectIncrementBounds.barMoment_mem ha hab hcL hcR ε L hε hεone hL hgs hg 2
  have hθ := (DefectIncrementBounds.barMoment_mem ha hab hcL hcR ε L hε hεone hL
    (hWs 2 1) (hW 2 1) 2).mono_exponent
      (show 1 - ChartScales.kappa ≤ 1 by norm_num [ChartScales.kappa])
  have hz := (DefectIncrementBounds.barMoment_mem ha hab hcL hcR ε L hε hεone hL
    (hWs 2 2) (hW 2 2) 1).mono_exponent
      (show 1 - ChartScales.kappa ≤ 1 by norm_num [ChartScales.kappa])
  fin_cases i
  · exact hP
  · simpa only [debt, Matrix.cons_val_one, Matrix.cons_val_zero, Matrix.cons_val_zero', Matrix.cons_val_succ',
      zeroMean_thetaDefect c u hm, DefectIncrementBounds.barMoment] using hθ
  · have h := Class.sub hz (Class.smul hP2 (1 / 2))
    simp only [debt,
      Matrix.cons_val_zero', Matrix.cons_val_succ', zeroMean_axialDefect c u hm,
      DefectIncrementBounds.barMoment] at h ⊢
    exact h
end InitialMeanBounds
end NavierStokes.CorrectionInitializationNoOptions
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.StateOn.reducedMeanResidual 500 546
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.StateOn.reducedMeanResidual"
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
end ScalarOn
namespace FrameOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c l : ℝ}
  {C : CorrectionState.Context D} {Cr : CorrectionState.Context E} {n nr : ℕ}
  (H : FrameOn U e c l (HarmonicResidual.contextFrame C n) (HarmonicResidual.contextFrame Cr nr))
include H
end FrameOn
namespace TripleOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c : ℝ} {n nr : ℕ}
  {b m : MeanIncrementBounds.Triple D} {br mr : MeanIncrementBounds.Triple E}
end TripleOn
namespace StateOn
variable {U : Set D} {e : D ≃L[ℝ] E} {c l : ℝ}
  {C : CorrectionState.Context D} {Cr : CorrectionState.Context E}
  {s : CorrectionState.State D} {r : CorrectionState.State E} {n nr : ℕ}
  (H : StateOn U e c l s r n nr) (G : ContextOn U e c l C Cr n nr)
include H G
#count_heartbeats in
theorem reducedMeanResidual_R (hU : IsOpen U) (hl : l ≠ 0) (i : Fin 3) :
    ScalarOn U e (c*c*l) (fun x => s.reducedMeanResidual C n x i)
      (fun x => r.reducedMeanResidual Cr nr x i) := by
  fin_cases i
  · exact H.radialResidual G hU hl
  · exact H.thetaResidual G hU hl
  · exact H.axialResidual G hU hl
end StateOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.MeanStateRegularity.Periodic.band_mul 550 566
run_cmd IO.println "BLOCK NavierStokes.MeanStateRegularity.Periodic.band_mul"
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
theorem band_mul_R (hf : Periodic U f) (c : ℕ → ℝ) :
    Periodic U (fun n x => c n * f n x) :=
  fun n R s hs Y k => congrArg (fun t : ℝ => c n * t) (hf n R s hs Y k)
end Periodic
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.PrimaryResidualClass.Inputs.initial_residual_class_of_zero_mode 570 613
run_cmd IO.println "BLOCK NavierStokes.PrimaryResidualClass.Inputs.initial_residual_class_of_zero_mode"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PrimaryResidualClass
open Set Function Filter HarmonicCalculus HarmonicFields WeightedClasses
open CopyAngularInvariance
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
section InvariantOperators
variable {X : Type} [NormedAddCommGroup X] [NormedSpace ℝ X]
  {θ : X} {R b F G : X → ℝ} {Vr Vθ Vz Vf Vs : X → X}
  {Φ : X → ℝ} {m : ℝ} {a : X → ComplexVector} {p : X → ℂ}
end InvariantOperators
namespace Inputs
variable {s : StripData D} {P : ℕ → D → ℝ} {κ : ℝ} {c : CorrectionState.Context D}
  {a : LinearWaveBounds.WaveCoefficients (D × ℝ)} {ψ : ℕ → D × ℝ → ℝ} {kp : ℕ → ℤ}
  (h : Inputs s P κ c a ψ kp)
include h
end Inputs
namespace Inputs
variable {s : StripData D} {P : ℕ → D → ℝ} {κ : ℝ} {c : CorrectionState.Context D}
  {a : LinearWaveBounds.WaveCoefficients (D × ℝ)} {ψ : ℕ → D × ℝ → ℝ} {kp : ℕ → ℤ}
  (h : Inputs s P κ c a ψ kp)
include h
end Inputs
namespace Inputs
variable {s : StripData D} {P : ℕ → D → ℝ} {κ : ℝ} {c : CorrectionState.Context D}
  {a : LinearWaveBounds.WaveCoefficients (D × ℝ)} {ψ : ℕ → D × ℝ → ℝ} {kp : ℕ → ℤ}
  (h : Inputs s P κ c a ψ kp)
include h
#count_heartbeats in
theorem initial_residual_class_of_zero_mode_R (u : CorrectionState.State D)
    (hmean : u.mean = ⟨0, 0, 0⟩) (A : HarmonicResidual.BlockCoefficients D)
    (hA : ∀ n i, HarmonicFields.BandLimited (A n i) 0) :
    (HarmonicResidual.residualBlock c u (primaryBlock s c a ψ kp)
      (gaussianCoefficients c a ψ) A).WaveBounds s P (7 / 10) := by
  apply h.initial_residual_class u hmean A
  intro n i j hj
  rw [HarmonicResidual.band_zero_eq_constant (hA n i)]
  simp [constantCoefficient, hj]
end Inputs
end NavierStokes.PrimaryResidualClass
end
end

-- REPLAY NavierStokes.HarmonicResidual.SmoothCoefficients.differentiate 617 633
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.SmoothCoefficients.differentiate"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
#count_heartbeats in
theorem SmoothCoefficients.differentiate_R {U : Set D} (hU : IsOpen U)
    {V : D → D} {Φ : D → ℝ} (hV : ContDiffOn ℝ ∞ V U) (hΦ : ContDiffOn ℝ ∞ Φ U)
    (k : ℝ) {c : Coefficients D} (hc : SmoothCoefficients U c) :
    SmoothCoefficients U (differentiate V k Φ c) :=
  fun j => derivativeCoefficient_contDiffOn hU hV hΦ (hc j) k j
end NavierStokes.HarmonicResidual
end
end

