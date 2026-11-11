import Tool
import NavierStokes.ActualWaveRegularityData
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionStep
import NavierStokes.CurrentSignedCurl
import NavierStokes.DefectIncrementBounds
import NavierStokes.HarmonicCovariance
import NavierStokes.ParticularWaveAssembly
import NavierStokes.PrimaryMaterialDefect
import NavierStokes.SignedStressPrimitive
import NavierStokes.TemporalMeanUpdate
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.PrimaryMaterialDefect.affine_slot_class 16 56
run_cmd IO.println "BLOCK NavierStokes.PrimaryMaterialDefect.affine_slot_class"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PrimaryMaterialDefect
open Set WeightedClasses LinearWaveBounds
open scoped Topology ContDiff
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
namespace NativeCoordinates
variable {s : StripData E} {d : GraphDirections E} {χ : ℕ → E → Slot}
variable (hχ : NativeCoordinates s d χ)
include hχ
end NativeCoordinates
section CommonPullback
variable {E' : Type*} [NormedAddCommGroup E'] [NormedSpace ℝ E']
end CommonPullback
#count_heartbeats in
theorem affine_slot_class_S (s : StripData E) (L : ℕ → E →L[ℝ] ℝ) (c : ℕ → ℝ)
    {C : ℝ} {m : ℕ} (hC : 1 ≤ C)
    (hL : ∀ n, ‖L n‖ ≤ C * s.slow n ^ m)
    (hv : ∀ n x, x ∈ s.domain → |L n x + c n| ≤ C * s.slow n ^ m) :
    UnweightedClass s 0 (fun n x => L n x + c n) := by
  apply PrimaryPulseBounds.polynomial_memClass s
  refine ⟨fun n => (L n).contDiff.contDiffOn.add contDiffOn_const, fun _ => ⟨C, hC, m, ?_⟩⟩
  intro n j _ x hx
  have hd : fderiv ℝ (fun y => L n y + c n) = fun _ => L n := by
    funext y
    exact ((L n).hasFDerivAt.add_const (c n)).fderiv
  cases j with
  | zero => simpa only [norm_iteratedFDeriv_zero, Real.norm_eq_abs, PrimaryPulseBounds.phaseDomain] using hv n x hx
  | succ j =>
      rw [← norm_iteratedFDeriv_fderiv, hd]
      cases j with
      | zero => simpa only [norm_iteratedFDeriv_zero, PrimaryPulseBounds.phaseDomain] using hL n
      | succ j =>
          rw [iteratedFDeriv_succ_const]
          simp only [Pi.zero_apply, norm_zero]
          exact mul_nonneg (zero_le_one.trans hC)
            (pow_nonneg (zero_le_one.trans (s.one_le_slow n)) _)
end NavierStokes.PrimaryMaterialDefect
end
end

-- REPLAY NavierStokes.CurrentSignedCurl.currentPotential_curl 60 84
run_cmd IO.println "BLOCK NavierStokes.CurrentSignedCurl.currentPotential_curl"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CurrentSignedCurl
open Set Function Filter ProblemStatement HarmonicCalculus WeightedClasses
open CorrectionInitialization CorrectionInitialization.ActualPrimary
open ActualSignedCoherence ActualSignedPotentialCoherence
open scoped Topology ContDiff BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem currentPotential_curl_S (l : SignedLabel B N0)
    (u : CorrectionState.State Point) {α : ℝ} (hamp : AmplitudeBound l u α)
    (n : ℕ) {a : ℝ} (ha : 0 < a) (i : PolarCharts.Index) {qbig : ℝ} {z : SpaceTime}
    (hz : z ∈ ActualPhysicalPrefixFields.cartesianChartDomain qbig n a i) :
    SpatialCurl.spatialCurl (currentPotential l u n a i) z =
      CyclePhysicalPrefixes.polarVelocityMap a i
        (CyclePhysicalPrefixes.velocityMap (ActualCycleResidualBounds.actualBandGraph n)
          (((ActualSignedStageControls.parameters l).exactBlock ActualInitialization.geometry.strip
            (request B u)).oscillation n)) z := by
  have ht := currentPotential_curl_forward l u hamp n ha i
    (ActualMeanPotentialRealization.polarCoordinates_valid ha i hz.2.1) hz.2.2
  simpa only [ActualMeanPotentialRealization.polarCoordinates_back ha i hz.2.1] using ht
end NavierStokes.CurrentSignedCurl
end
end

-- REPLAY NavierStokes.CorrectionStep.ParticularParameters.linearGood_bounds 88 475
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.ParticularParameters.linearGood_bounds"
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
end GaugeSupported
end MovingSupport
section MovingMeanPressure
open CorrectionState VariableGaugeMean LocalSignedRequest
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
include hd hell
local notation "stageStrip" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
end MovingMeanPressure
section TemporalRegularity
open CorrectionState VariableGaugeMean LocalSignedRequest
variable {coord : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent)
    (hell : ∀ n, g.length n = qLength coord)
    (h : ℝ) (index : ℕ → ℕ) (axial : PressureStream.Plane × PressureStream.Plane)
    (c : Context Point) (u : State Point)
    (hθ : ∀ n, ContDiffOn ℝ ∞ (u.thetaResidual c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hz : ∀ n, ContDiffOn ℝ ∞ (u.axialResidual c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hpθ : ∀ n, PhysicalMeanDomain.PeriodicOn U.carrier (u.thetaResidual c n))
    (hpz : ∀ n, PhysicalMeanDomain.PeriodicOn U.carrier (u.axialResidual c n))
    (hsz : GaugeSupported g.radial.inner g.radial.outer (qLength coord) U.carrier (u.axialResidual c))
end TemporalRegularity
section PeriodizedSignedConstruction
open CorrectionState VariableGaugeMean LocalSignedRequest
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I : Type}
namespace PeriodizedSignedParameters
variable (p : PeriodizedSignedParameters D I)
end PeriodizedSignedParameters
end PeriodizedSignedConstruction
section ParticularConstruction
open CorrectionState VariableGaugeMean
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
namespace ParticularParameters
variable (p : ParticularParameters P)
end ParticularParameters
end ParticularConstruction
section ActualCycle
open CorrectionState VariableGaugeMean
namespace CycleParameters
variable {ι : Type} (p : CycleParameters ι) (v : CycleCoefficients ι)
    (c : Context CyclePoint) (u : State CyclePoint)
end CycleParameters
end ActualCycle
section ConstructedTemporalStage
open CorrectionState VariableGaugeMean LocalSignedRequest
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
include hd hell
local notation "stageStrip" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
end ConstructedTemporalStage
section ConstructedRankStage
open CorrectionState VariableGaugeMean LocalSignedRequest
variable {coord cL cR A B : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (r : RankData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
include hd hell
local notation "stageStrip" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
end ConstructedRankStage
section CycleMassPreservation
open Set WeightedClasses MeanIncrementBounds CorrectionState VariableGaugeMean LocalSignedRequest
open scoped ContDiff BigOperators
namespace CycleParameters
variable {ι : Type} (p : CycleParameters ι) (v : CycleCoefficients ι)
    (c : Context CyclePoint) (u : State CyclePoint)
end CycleParameters
end CycleMassPreservation
section CycleMeanCompletion
open Set WeightedClasses MeanIncrementBounds CorrectionState VariableGaugeMean LocalSignedRequest
open scoped ContDiff BigOperators
namespace CycleParameters
variable {ι : Type} (p : CycleParameters ι) (v : CycleCoefficients ι)
    (c : Context CyclePoint) (u : State CyclePoint)
    {coord cL cR A B : ℝ} (U : SlowRegion coord)
    (ha : 0 < p.gauge.radial.inner) (hd : 0 < p.gauge.radial.exponent)
    (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, p.gauge.length n = qLength coord)
include hd hell
local notation "stageStrip" => movingStripData U p.gauge.radial.inner p.gauge.radial.outer cL cR ha hcL hcR ε L hε hεone hL
local notation "slowStrip" => PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL
local notation "signedState" => p.afterSigned v c u
local notation "temporalState" => p.afterTemporal v c u
end CycleParameters
end CycleMeanCompletion
section PeriodizedNativeBounds
open Set Filter WeightedClasses CorrectionState
open scoped ContDiff Topology
variable {D I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace PeriodizedSignedParameters
variable (p : PeriodizedSignedParameters D I) (s : StripData D)
variable {p s} {P : ℕ → D → ℝ} {κ β : ℝ}
end PeriodizedSignedParameters
namespace ParticularParameters
open CommonCoverSolve TorusInverse
variable {Q : Type} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
    (p : ParticularParameters Q) (s : StripData (Q × Plane))
    (c : Context (Q × Plane)) (u : State (Q × Plane)) (b : HarmonicBlock (Q × Plane))
    (G A : HarmonicResidual.BlockCoefficients (Q × Plane)) (j : ℤ)
variable {p s c u b G A j} {W : ℕ → (Q × ℝ) × Plane → ℝ} {α κ : ℝ}
end ParticularParameters
end PeriodizedNativeBounds
section NativeEquations
open Set Filter WeightedClasses HarmonicCalculus CorrectionState
open scoped ContDiff Topology
variable {D I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace PeriodizedSignedParameters
variable {p : PeriodizedSignedParameters D I} {s : StripData D}
    {P : ℕ → D → ℝ} {κ β : ℝ} (h : p.NativeControl s P κ)
    (request : ℕ → D × ℝ → SignedWaveUpdate.Vec2)
variable {h request}
end PeriodizedSignedParameters
namespace ParticularParameters
open CommonCoverSolve TorusInverse ParticularWaveAssembly CopyAngularInvariance
variable {Q : Type} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
    {p : ParticularParameters Q} {s : StripData (Q × Plane)}
    {c : Context (Q × Plane)} {u : State (Q × Plane)} {b : HarmonicBlock (Q × Plane)}
    {G A : HarmonicResidual.BlockCoefficients (Q × Plane)} {j : ℤ}
    {W : ℕ → (Q × ℝ) × Plane → ℝ} {α κ : ℝ}
    (h : p.NativeControl s c u b G A j W α κ)
variable {h}
end ParticularParameters
end NativeEquations
section PeriodizedSignedLinear
open Set Filter WeightedClasses HarmonicCalculus CorrectionState
open scoped ContDiff Topology
variable {D I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace NativeAngularGeometry
variable {a : PeriodizedWaveBounds.CopyData D I} {s : StripData D}
  {d : LinearWaveBounds.GraphDirections D} {C : ℕ → I → Set D}
  (g : NativeAngularGeometry a s d C)
include g
end NativeAngularGeometry
namespace PeriodizedSignedParameters
variable {p : PeriodizedSignedParameters D I} {s : StripData D}
  {P : ℕ → D → ℝ} {κ β : ℝ} {h : p.NativeControl s P κ}
  {request : ℕ → D × ℝ → SignedWaveUpdate.Vec2}
  (d : NativeDynamics h request) (i₀ : I)
end PeriodizedSignedParameters
end PeriodizedSignedLinear
section ParticularLinear
open Set WeightedClasses HarmonicCalculus
open ParticularWaveBounds LinearWaveBounds
variable {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
open CorrectionState TorusInverse CommonCoverSolve ParticularWaveAssembly CopyAngularInvariance
open scoped ContDiff BigOperators
namespace ParticularParameters
variable {Q : Type} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
  {p : ParticularParameters Q} {s : StripData (Q × Plane)}
  {c : Context (Q × Plane)} {u : State (Q × Plane)} {b : HarmonicBlock (Q × Plane)}
  {G A : HarmonicResidual.BlockCoefficients (Q × Plane)} {j : ℤ}
  {W : ℕ → (Q × ℝ) × Plane → ℝ} {α κ : ℝ}
  {h : p.NativeControl s c u b G A j W α κ}
variable (p : ParticularParameters Q) (s : StripData (Q × Plane))
  (c : Context (Q × Plane)) (u : State (Q × Plane)) (b : HarmonicBlock (Q × Plane))
  (G A : HarmonicResidual.BlockCoefficients (Q × Plane)) (N : ℕ)
  (C : ∀ j ∈ modes N, p.NativeControl s c u b G A j W α κ)
  (dyn : ∀ j hj, NativeDynamics (C j hj))
#count_heartbeats in
theorem linearGood_bounds_S (hκ : κ ≤ 1 / 2)
    (hN : (HarmonicResidual.residualBlock c u b G A).BandLimited N)
    (hB : MeanIncrementBounds.SmoothTriple s.domain c.base)
    (hrad : ∀ n, ContDiffOn ℝ ∞ (HarmonicResidual.contextFrame c n).radial s.domain)
    (hm : WaveFrameMatch c (HarmonicWaveInteraction.productStrip s)
      (reindexDirections angleShuffle p.directions) (reindexCoefficients angleShuffle p.background))
    (hphase : ∀ n, ContDiffOn ℝ ∞ (b.phase n) s.domain)
    (hkp : ∀ n, b.angularFrequency n ≠ 0)
    (hW : ∀ n x, x ∈ (nativeStrip s).domain → 0 ≤ W n x) :
    ∀ i j, j ≠ 0 → WaveClass s (fun n x => W n (angleShuffle (x,0)))
      (α + 1 / 2 - 3 * κ) (fun n x =>
        (HarmonicResidual.residualBlock c u b G A).velocity n i j x +
        (HarmonicWaveInteraction.linearGoodBlock c b (p.updateBlock s c u b G A N)
          (p.gaussianBlock c u b G A N).velocity).velocity n i j x) := by
  have hb := p.assembled_bounds s c u b G A N C hW hκ
  have hz : HarmonicWaveInteraction.ZeroMode (p.updateBlock s c u b G A N) :=
    (assembledBlock_zero _ _ _ _ _ _).1
  have hpz : ∀ n, (p.updateBlock s c u b G A N).pressure n 0 = 0 :=
    (assembledBlock_zero _ _ _ _ _ _).2
  have hbs := HarmonicWaveInteraction.waveBounds_smooth hb.1 hz
  have hps (n : ℕ) : HarmonicResidual.SmoothCoefficients s.domain
      ((p.updateBlock s c u b G A N).pressure n) := by
    intro j
    by_cases hj : j = 0
    · subst j
      rw [hpz]
      exact contDiffOn_const
    exact (hb.2.1 j hj).smooth n
  apply linearGoodBlock_cancel_mem c b (p.updateBlock s c u b G A N)
    (HarmonicResidual.residualBlock c u b G A) (p.goodBlock s c u b G A N)
    (p.gaussianBlock c u b G A N).velocity hrad (fun _ => contDiffOn_const)
    hB hbs hps hphase hkp (HarmonicResidual.residualBlock_conjugate _ _ _ _ _)
    (assembledBlock_real _ _ _ _ _ _).1 hb.2.2
  intro n x hx θ i
  have he := congrFun (p.context_linear_cancellation s c u b G A N C dyn hκ hN hB hrad hm n (x,θ) hx) i
  exact he
end ParticularParameters
end ParticularLinear
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.ActualWaveRegularityData.particular_full_regular_of_class 479 522
run_cmd IO.println "BLOCK NavierStokes.ActualWaveRegularityData.particular_full_regular_of_class"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualWaveRegularityData
open Set Function Filter WeightedClasses HarmonicCalculus
open CorrectionInitialization CommonCoverSolve TorusInverse
open scoped Topology ContDiff BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem particular_full_regular_of_class_S {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : ℕ → ActualWaveRegularity.ParticularSpace → E} {α : ℝ}
    (hf : MemClass particularFullStrip (fun _ x => Real.sqrt (particularFullStrip.zeta x)) α f)
    (hz : ∀ n z, z ∈ ActualWaveRegularity.nativeDomain ActualWaveRegularity.particularChart
        ActualPrimary.standardRegion →
      radius (ActualWaveRegularity.particularChart.symm z) ∉
        Ioo (PrimaryTargetBounds.leftRadius ActualPrimary.nominal)
          (PrimaryTargetBounds.rightRadius ActualPrimary.nominal) → f n z = 0)
    (n : ℕ) :
    ContDiffOn ℝ ∞ (f n)
      (ActualWaveRegularity.nativeDomain ActualWaveRegularity.particularChart ActualPrimary.standardRegion) ∧
      ∀ m z, z ∈ ActualWaveRegularity.nativeDomain ActualWaveRegularity.particularChart
          ActualPrimary.standardRegion →
        (radius (ActualWaveRegularity.particularChart.symm z) = PrimaryTargetBounds.leftRadius ActualPrimary.nominal ∨
         radius (ActualWaveRegularity.particularChart.symm z) = PrimaryTargetBounds.rightRadius ActualPrimary.nominal) →
        iteratedFDeriv ℝ m (f n) z = 0 := by
  have hs := full_regular_of_class (particular_pull_class hf)
    (fun m x hx ho => hz m (ActualWaveRegularity.particularChart x)
      (by simpa only [ActualWaveRegularity.nativeDomain, mem_preimage,
        LinearIsometryEquiv.symm_apply_apply] using hx)
      (by simpa only [LinearIsometryEquiv.symm_apply_apply] using ho)) n
  constructor
  · have hh := hs.1.comp ActualWaveRegularity.particularChart.symm.contDiff.contDiffOn
      (fun _ hz => hz)
    simp only [Function.comp_def, LinearIsometryEquiv.apply_symm_apply] at hh ⊢
    exact hh
  · intro m z hz he
    have hj := hs.2 m (ActualWaveRegularity.particularChart.symm z) hz he
    have hn := StateReindex.norm_iteratedFDeriv_pull ActualWaveRegularity.particularChart
      (f n) m (ActualWaveRegularity.particularChart.symm z)
    rw [LinearIsometryEquiv.apply_symm_apply, hj, norm_zero] at hn
    exact norm_eq_zero.mp hn.symm
end NavierStokes.ActualWaveRegularityData
end
end

-- REPLAY NavierStokes.CorrectionInitialization.PrimaryPiece.harmonic_cumulative_bounds 526 624
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.PrimaryPiece.harmonic_cumulative_bounds"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CorrectionInitialization
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
#count_heartbeats in
theorem harmonic_cumulative_bounds_S (p : PrimaryPiece (D × ℝ))
    (Φ : ℕ → D → ℝ) (kp : ℕ → ℤ) {P : ℕ → D × ℝ → ℝ}
    (hp : InputBounds p.strip P (1 / 2) ChartScales.kappa p.directions p.coefficients)
    (hcut : UnweightedClass p.strip 0 p.cutoff) {R : D × ℝ → ℝ}
    (hR : p.coefficients.radius = fun _ => R)
    (hN : PhaseJetBounds.PolynomialJets (CurlClassBounds.phaseDomain p.strip)
      (p.coefficients.normal p.strip p.directions)) {b M : ℝ} (hb : 0 < b)
    (hlo : ∀ n x, x ∈ p.strip.domain → b ≤ ‖p.coefficients.normal p.strip p.directions n x‖)
    (hhi : ∀ n x, x ∈ p.strip.domain → ‖p.coefficients.normal p.strip p.directions n x‖ ≤ M)
    (hK : BandBound p.strip (1 / 2) (fun n => 1 / p.coefficients.frequency n)) :
    let s := AngularRestriction.strip p.strip
    let P0 := fun n x => P n (x, 0)
    (∀ i j, WaveClass s P0 (1 / 2) (fun n x => (p.harmonicBlock Φ kp).velocity n i j x)) ∧
    (∀ i j, WaveClass s P0 (17 / 25) (fun n x => (p.differenceBlock Φ kp).velocity n i j x)) ∧
    (∀ j, WaveClass s P0 1 (fun n x => (p.harmonicBlock Φ kp).pressure n j x)) := by
  obtain ⟨hamp, hdiff, hpressure⟩ := p.cumulative_bounds hp hcut hR hN hb hlo hhi hK
  exact ⟨fun i j => PrimaryHarmonics.block_coefficient_class p.exactCoefficients Φ kp hamp i j,
    fun i j => PrimaryHarmonics.block_coefficient_class p.differenceCoefficients Φ kp
      (fun i => CurlClassBounds.class_component hdiff i) i j,
    fun j => PrimaryHarmonics.block_pressure_class p.exactCoefficients Φ kp hpressure j⟩
end PrimaryPiece
end PrimaryBlocks
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.HarmonicCovariance.realAngularProduct_mem 628 671
run_cmd IO.println "BLOCK NavierStokes.HarmonicCovariance.realAngularProduct_mem"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicCovariance
open Set Filter MeasureTheory CorrectionState
open scoped BigOperators ContDiff Topology
section CoefficientCovariance
open HarmonicFields WeightedClasses
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end CoefficientCovariance
section RealCoefficientCovariance
open HarmonicFields WeightedClasses
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
#count_heartbeats in
theorem realAngularProduct_mem_S {s : StripData D} {P : ℕ → D → ℝ} {α β : ℝ}
    (a b : ℕ → Coefficients D) (N : ℕ)
    (hband : ∀ n, BandLimited (a n) N)
    (ha : ∀ j, WaveClass s P α (fun n x => a n j x))
    (hb : ∀ j, WaveClass s P β (fun n x => b n j x))
    (hP0 : ∀ n x, x ∈ s.domain → 0 ≤ P n x)
    (hP1 : ∀ n x, x ∈ s.domain → P n x ≤ 1)
    (k : ℕ → ℝ) (Φ : ℕ → D → ℝ) (kp : ℕ → ℤ) (hkp : ∀ n, kp n ≠ 0) :
    MeanClass s (α + β) (angularAverage (fun n p =>
      (field (a n) (k n) (Φ n) (kp n) p).re *
        (field (b n) (k n) (Φ n) (kp n) p).re)) := by
  have hF : ∀ n, (HarmonicResidual.realCoefficients (a n)).support ⊆
      Finset.Icc (-(N : ℤ)) (N : ℤ) := by
    intro n j hj
    have h := HarmonicResidual.band_realCoefficients (hband n) j hj
    simp only [Finset.mem_Icc]
    omega
  have hc := angularProduct_mem
    (fun n => HarmonicResidual.realCoefficients (a n))
    (fun n => HarmonicResidual.realCoefficients (b n))
    (Finset.Icc (-(N : ℤ)) (N : ℤ)) hF
    (fun j _ => realCoefficients_mem a ha j)
    (fun j _ => realCoefficients_mem b hb (-j)) hP0 hP1 k Φ kp hkp
  apply WaveInteractionBounds.class_congr (hc.map Complex.reCLM)
  intro n x _
  exact (realAngularProduct_eq (a n) (b n) (k n) (Φ n) (hkp n) x).symm
end RealCoefficientCovariance
end NavierStokes.HarmonicCovariance
end
end

-- REPLAY NavierStokes.SignedStressPrimitive.axial_bump_improvedClass 675 715
run_cmd IO.println "BLOCK NavierStokes.SignedStressPrimitive.axial_bump_improvedClass"
section
set_option linter.all false
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology BigOperators
namespace NavierStokes.SignedStressPrimitive
section Primitive
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end Primitive
section Physical
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end Physical
section IntegratedBalances
open IntegratedMeanBalances
#count_heartbeats in
theorem axial_bump_improvedClass_S (P : Patch) {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (ε slow : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hε1 : ∀ n, ε n ≤ 1) (hslow : ∀ n, 1 ≤ slow n)
    (α : ℝ) (γ radialFlux axialFlux pressure virtualFlux gr ρ : ℕ → MeanField)
    (hγ : ∀ n, SmoothShell P.a P.b (γ n)) (hr : ∀ n, SmoothShell P.a P.b (radialFlux n))
    (hz : ∀ n, SmoothShell P.a P.b (axialFlux n)) (hp : ∀ n, SmoothShell P.a P.b (pressure n))
    (hT : ∀ n, SmoothShell P.a P.b (virtualFlux n)) (hg : ∀ n, SmoothShell P.a P.b (gr n))
    (hρ : ∀ n, SmoothShell P.a P.b (ρ n)) (hmass : ∀ n, radialMoment 1 (γ n) = 0)
    (hderiv : ∀ n r p, deriv (fun s => pressure n (s, p)) r =
      gr n (r, p) - ρ n (r, p) * pressureTotal (gr n) p)
    (hclass : WeightedClasses.UnweightedClass
      (WeightedRadialPrimitive.logStripData P.a P.b cL cR P.a_pos hcL hcR ε slow hε hε1 hslow)
      α (fun n (z : MeanPoint) => axialMomentPotential (axialFlux n) (gr n) (ρ n) z.2)) :
    WeightedClasses.MeanClass
      (WeightedRadialPrimitive.logStripData P.a P.b cL cR P.a_pos hcL hcR ε slow hε hε1 hslow)
      (α + 1) (fun n => bumpCorrection P 1
        (axialBalance (ε n) (γ n) (radialFlux n) (axialFlux n) (pressure n) (virtualFlux n))) := by
  apply bump_improvedClass_of_moment_identity P 1 hcL hcR ε slow hε hε1 hslow α
    (fun n => axialBalance (ε n) (γ n) (radialFlux n) (axialFlux n) (pressure n) (virtualFlux n))
    (fun n => axialMomentPotential (axialFlux n) (gr n) (ρ n)) (0, 1)
    (fun n => axialMomentPotential_contDiff P (hz n) (hg n) (hρ n)) hclass
  exact fun n p => integrated_axial_reconstructed (ε n) (hγ n) (hr n) (hz n) (hp n)
    (hT n) (hg n) (hρ n) (hmass n) (hderiv n) p
end IntegratedBalances
end NavierStokes.SignedStressPrimitive
end
end

-- REPLAY NavierStokes.TemporalMeanUpdate.dividedAlias_global_bounds 719 816
run_cmd IO.println "BLOCK NavierStokes.TemporalMeanUpdate.dividedAlias_global_bounds"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TemporalMeanUpdate
open Set Filter MeasureTheory Function
open TorusInverse
open scoped Topology ContDiff BigOperators Interval
section CenteredSource
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end CenteredSource
section FamilyInverse
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end FamilyInverse
section ExactUpdate
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end ExactUpdate
section NativePullback
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end NativePullback
section AxialReconstruction
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end AxialReconstruction
section WeightedStream
variable {E V : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end WeightedStream
section AliasPullback
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end AliasPullback
section WeightedTemporal
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end WeightedTemporal
section PhysicalAliasSuperflat
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end PhysicalAliasSuperflat
section InteriorAliasClass
variable {E V : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end InteriorAliasClass
section CompleteWeightedUpdate
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
#count_heartbeats in
theorem dividedAlias_global_bounds_S {a b d cL cR α : ℝ}
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε R : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hR : ∀ n, 1 ≤ R n)
    (M : ℕ → ℝ) (hM : ∀ n, M n ≠ 0) {g : ℕ → PressureStream.Lift S → ℝ}
    (hg : WeightedClasses.MeanClass
      (WeightedRadialPrimitive.logStripData a b cL cR ha hcL hcR ε R hε hεone hR) α g)
    (hgc : ∀ n, ContDiff ℝ ∞ (g n)) (hgp : ∀ n, PressureStream.TorusPeriodicLift (g n))
    (hgm : ∀ n p, PressureStream.torusAverage (g n) p = 0)
    (hgs : ∀ n, RadialAlias.RadiallySupported a b (g n)) (m : ℕ) :
    ∃ C : ℝ, 0 ≤ C ∧ ∃ p : ℕ, ∀ n j, j ≤ m → ∀ z : PressureStream.Lift S,
      ‖iteratedFDeriv ℝ j (PressureStream.divideRadius
        (RadialPullback.physicalAlias d a b (M n) ((0 : S), vector .radial) (g n))) z‖ ≤
          C * ε n ^ α * R n ^ p := by
  have haU : 0 < a ^ d := Real.rpow_pos_of_pos ha d
  have habU : a ^ d < b ^ d := Real.rpow_lt_rpow ha.le hab hd
  have hcLU : 0 < d ^ 2 * cL := mul_pos (sq_pos_of_pos hd) hcL
  have hcRU : 0 < d ^ 2 * cR := mul_pos (sq_pos_of_pos hd) hcR
  let G := fun n => RadialPullback.normalizeSource d a (g n)
  have hG := UniformFourierAlias.meanClass_normalizeSource ha hab hd hcL hcR ε R hε hεone hR hg hgc
  have hGc : ∀ n, ContDiff ℝ ∞ (G n) := fun n => RadialPullback.normalizeSource_contDiff ha hd (hgc n)
  have hGp : ∀ n, UniformFourierAlias.SourcePeriodic (G n) := fun n => normalizeSource_periodic d a (hgp n)
  have hGm : ∀ n p, UniformFourierAlias.sourceMean (G n) p = 0 := by
    intro n p
    change PressureStream.torusAverage (RadialPullback.normalizeSource d a (g n)) p = 0
    rw [normalizeSource_torusAverage, hgm, mul_zero]
  have hGs := fun n => RadialPullback.normalizeSource_supported ha hab hd (hgs n)
  obtain ⟨C, hC, p, hsource⟩ := UniformFourierAlias.meanClass_global_finiteJets
    haU hcLU hcRU ε R hε hεone hR hG hGs hGc m
  let χ := TransportPrimitive.interiorCutoff (a ^ d) (b ^ d)
  have hχ : ContDiff ℝ ∞ χ := TransportPrimitive.interiorCutoff_contDiff _ _
  have hleft : ∀ U ≤ a ^ d, χ U = 0 := fun U hU =>
    TransportPrimitive.interiorCutoff_zero habU (by linarith)
  have hright : ∀ U, b ^ d ≤ U → χ U = 1 := fun U hU =>
    TransportPrimitive.interiorCutoff_one habU (by linarith)
  obtain ⟨KA, hKA, hbA⟩ := UniformFourierAlias.real_exactAlias_finiteJets (S := S) .radial
    habU.le hχ hleft hright m 0
  obtain ⟨KT, hKT, hbT⟩ := dividedAlias_finiteJets_transfer (E := S × Plane) ha hab hd m
  refine ⟨KT * KA * C, mul_nonneg (mul_nonneg hKT hKA) hC, p, ?_⟩
  intro n j hj z
  let B := C * ε n ^ α * R n ^ p
  have hB : 0 ≤ B := mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (hε n) α).le)
    (pow_nonneg (zero_le_one.trans (hR n)) _)
  have hAb : ∀ i ≤ m, ∀ y : PressureStream.Lift S,
      ‖iteratedFDeriv ℝ i (UniformFourierAlias.exactAlias χ (M n) ((0 : S), vector .radial) (G n)) y‖ ≤ KA * B := by
    intro i hi y
    have he := hbA (G n) (hGc n) (hGp n) (hGm n) (hGs n) B hB
      (fun k hk x _ => hsource n k (by simpa using hk) x (Set.mem_univ x)) (M n) (hM n) i hi y
    simpa only [pow_zero, mul_one] using he
  have he := hbT (M n) ((0 : S), vector .radial) (g n) (hgc n) (hgs n)
    (KA * B) (mul_nonneg hKA hB) hAb j hj z
  exact he.trans_eq (by dsimp [B]; ring)
end CompleteWeightedUpdate
end NavierStokes.TemporalMeanUpdate
end
end

-- REPLAY NavierStokes.ParticularWaveAssembly.LocalControl.common_classes 820 902
run_cmd IO.println "BLOCK NavierStokes.ParticularWaveAssembly.LocalControl.common_classes"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParticularWaveAssembly
open Set Function HarmonicFields ErrorHarmonics CorrectionState
open HarmonicCalculus WeightedClasses
open scoped BigOperators Topology ContDiff ComplexConjugate
section ReferenceTransport
open CommonCoverSolve TorusInverse
variable {P Q H : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup Q] [NormedSpace ℝ Q]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
end ReferenceTransport
section ComplexTransport
open CommonCoverSolve TorusInverse ParticularWaveBounds
variable {P Q : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup Q] [NormedSpace ℝ Q]
end ComplexTransport
section FixedReference
open CommonCoverSolve TorusInverse ParticularWaveBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end FixedReference
section AngularConstruction
open CommonCoverSolve TorusInverse ParticularWaveBounds CopyAngularInvariance
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end AngularConstruction
section OperatorInvariance
open CopyAngularInvariance LinearWaveResidual LinearWaveBounds
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
variable {θ : E} {R b F G Φ : E → ℝ} {Vr Vθ Vz Vf Vs : E → E}
variable {a : E → ComplexVector} {p : E → ℂ} {m : ℝ}
end OperatorInvariance
section NativeLocalization
open CommonCoverSolve TorusInverse TorusAverages ParticularWaveBounds
variable {P H : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup H] [NormedSpace ℝ H] [CompleteSpace H]
end NativeLocalization
section ActualCoefficients
open CommonCoverSolve TorusInverse ParticularWaveBounds CopyAngularInvariance LinearWaveBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end ActualCoefficients
section DifferentialGerms
open Filter LinearWaveResidual
open CurlClassBounds hiding ComplexVector
variable {E F : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end DifferentialGerms
section CommonLocalCurl
open CommonCoverSolve TorusInverse TorusAverages ParticularWaveBounds LinearWaveBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end CommonLocalCurl
section NativeBlocks
open CommonCoverSolve TorusInverse ParticularWaveBounds CopyAngularInvariance LinearWaveBounds
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end NativeBlocks
section ConstructedControls
open Filter
open CommonCoverSolve TorusInverse HarmonicCalculus WeightedClasses LinearWaveBounds
open ParticularWaveBounds CopyAngularInvariance CorrectionState
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
namespace LocalControl
variable {r : Reference P} {charts : BandCharts P}
  {c : Context (P × Plane)} {u : State (P × Plane)} {b : HarmonicBlock (P × Plane)}
  {G A : HarmonicResidual.BlockCoefficients (P × Plane)} {j : ℤ}
  {base : WaveCoefficients ((P × ℝ) × Plane)} {copy : ℕ → Frequency}
  {s : StripData ((P × ℝ) × Plane)} {dirs : GraphDirections ((P × ℝ) × Plane)} {α κ : ℝ}
  (C : LocalControl r charts c u b G A j base copy s dirs α κ)
include C
#count_heartbeats in
theorem common_classes_S :
    WaveClass s C.weight α (actualCorrectedCommon r charts c u b G A j base s dirs).amplitude ∧
    WaveClass s C.weight (α + 1 / 2) (actualCorrectedCommon r charts c u b G A j base s dirs).pressure := by
  refine ⟨LinearWaveBounds.class_congr C.local_result.2.1 ?_,
    LinearWaveBounds.class_congr C.local_result.2.2.1 ?_⟩
  · intro n x hx
    exact (C.common_germ n hx).1.self_of_nhds.symm
  · intro n x hx
    exact (C.common_germ n hx).2.self_of_nhds.symm
end LocalControl
end ConstructedControls
end NavierStokes.ParticularWaveAssembly
end
end

-- REPLAY NavierStokes.DefectIncrementBounds.axialQuadratic_mem 906 940
run_cmd IO.println "BLOCK NavierStokes.DefectIncrementBounds.axialQuadratic_mem"
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
end Shell
namespace Shell
variable {a b : ℝ} {f : ScalarField (Point P)} {o : Operators (Point P)}
end Shell
section FluxSupport
variable {a b : ℝ} (ha : 0 < a) {base m h : Triple (Point P)}
  (hb : SmoothTriple (positiveDomain (P := P)) base)
  (hm : ShellTriple a b m) (hh : ShellTriple a b h)
end FluxSupport
section RemainderClasses
variable {s : StripData (Point P)} {o : Operators (Point P)} {κ H : ℝ}
  {base m h : Triple (Point P)} (ho : OperatorBounds s o κ)
  (hb : BaseBounds s base) (hm : CumulativeBounds s m) (hh : IncrementBounds s H h)
  (hH : 9 / 10 ≤ H)
#count_heartbeats in
theorem axialQuadratic_mem_S : MeanClass s (H + 9 / 10 - 2 * κ) (axialQuadratic m h) := by
  have h1 : MeanClass s (H + 9 / 10) ((2 : ℝ) • (m.axial * h.axial)) := by
    simpa only [add_comm] using Class.smul (Class.product hm.axial hh.axial ho.weight_le_one) 2
  have h2 := (Class.product hh.axial hh.axial ho.weight_le_one).mono_exponent
    (show H + 9 / 10 ≤ H + H from by linarith)
  exact (h1.add h2).mono_exponent (by linarith [ho.kappa_nonneg])
end RemainderClasses
end
end NavierStokes.DefectIncrementBounds
end

