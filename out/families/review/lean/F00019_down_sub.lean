import Tool
import F19
import NavierStokes.ActualMeanPhysicalData
import NavierStokes.ActualPhysicalStageBounds
import NavierStokes.ActualSignedPhysicalData
import NavierStokes.BaseContextAssembly
import NavierStokes.CorrectionStep
import NavierStokes.InitializedPhysicalBackground
import NavierStokes.NaturalCore
import NavierStokes.PhysicalSignedWave
import NavierStokes.PhysicalStageBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualPhysicalStageBounds.initialPotential_smooth 16 75
run_cmd IO.println "BLOCK NavierStokes.ActualPhysicalStageBounds.initialPotential_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualPhysicalStageBounds
open Set Function Filter ProblemStatement DiagonalResidual
open scoped Topology ContDiff BigOperators
section JetAlgebra
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
  {h qbig : ℝ} {f g : SpaceTime → V} {m : ℕ} {r s : ℝ}
end JetAlgebra
section Increments
variable {h : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
end Increments
namespace CycleInputs
variable {h : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
namespace CycleInputs
variable {h κ qbig : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
section RawTransfer
variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
  {h qbig : ℝ} {f g : SpaceTime → V} {m : ℕ} {r : ℝ}
end RawTransfer
namespace CycleInputs
variable {h κ qbig : ℝ}
  {DP DS : Type} [NormedAddCommGroup DP] [NormedSpace ℝ DP]
  [NormedAddCommGroup DS] [NormedSpace ℝ DS] {IP KP IS KS : Type*}
  (D : CycleInputs h DP IP KP DS IS KS)
end CycleInputs
open InitializedPhysicalBackground (seedPotentialLoss seedDirectLoss initialLoss)
section InitialIncrement
variable {h : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
end InitialIncrement
section ActualInitialBase
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
  {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
#count_heartbeats in
theorem initialPotential_smooth_R (upper : ℝ) (B : ℕ)
    (WA : PhysicalStageBounds.WaveData F.data.h D I K (Fin 3))
    (MT MR : MeanInput F.data.h (Fam.F19.halfPlus F.data.h - 1 / 2))
    {qbig : ℝ} (hqT : qbig ≤ ChartScales.Q MT.firstBand) (hqR : qbig ≤ ChartScales.Q MR.firstBand) :
    ContDiffOn ℝ ∞ (initialPotential H v upper B WA MT MR)
      (CutStageEstimates.physicalSublevel F.data.h qbig) :=
  ((TailGaugePotential.finalPotential_smooth H v upper B).mono
    (fun _ hw => ⟨hw.1, mem_univ _⟩)).add
      (initialIncrement_smooth WA MT MR F.data.h_pos F.data.h_lt_half hqT hqR)
end ActualInitialBase
end NavierStokes.ActualPhysicalStageBounds
end
end

-- REPLAY NavierStokes.PhysicalStageBounds.directStages_smooth 79 111
run_cmd IO.println "BLOCK NavierStokes.PhysicalStageBounds.directStages_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PhysicalStageBounds
open Set Function Filter ProblemStatement
open scoped Topology ContDiff BigOperators
section Waves
variable (h : ℝ) (D : Type) [NormedAddCommGroup D] [NormedSpace ℝ D]
  (I K J : Type*)
variable {h D I K J}
end Waves
section GainComparison
variable {h g delta : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {I K : Type*}
end GainComparison
section Assembly
variable {h : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
end Assembly
section InitializedStages
variable {X V : Type*} [Add V]
end InitializedStages
section Sequences
variable {h qbig : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
omit [NormedAddCommGroup D] [NormedSpace ℝ D] in
#count_heartbeats in
theorem directStages_smooth_R (M : ℕ → MeanData h (Fam.F19.halfPlus h))
    (hh : 0 < h) (hh1 : h < 1 / 2) (hq : ∀ j, qbig ≤ ChartScales.Q (M j).firstBand) :
    ∀ j, ContDiffOn ℝ ∞ (directStages M j) (CutStageEstimates.physicalSublevel h qbig) :=
  fun j => (M j).angular_smooth hh hh1 (hq j)
end Sequences
end NavierStokes.PhysicalStageBounds
end
end

-- REPLAY NavierStokes.ActualMeanPhysicalData.Atlas.temporal_overlap 115 152
run_cmd IO.println "BLOCK NavierStokes.ActualMeanPhysicalData.Atlas.temporal_overlap"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualMeanPhysicalData
open Set Function Filter ProblemStatement
open PhysicalResidualNaturality GaugeStateCoherence
open scoped Topology ContDiff BigOperators
open CorrectionInitialization.ActualPrimary
#count_heartbeats in
theorem Atlas.temporal_overlap_R {h : ℝ} {N Δ : ℕ} (Fam.F19.halfPlus : Atlas h N Δ)
    (U : LocalSignedRequest.SlowRegion (2 * h))
    (g : VariableGaugeMean.GaugeData Plane) (c : CorrectionState.Context Point)
    (u : CorrectionState.State Point)
    (HC : Fam.F19.halfPlus.ContextOverlap U.carrier c) (HS : Fam.F19.halfPlus.StateOverlap U.carrier u)
    (HG : Fam.F19.halfPlus.GaugeOverlap U.carrier g)
    (HP : MeanStateRegularity.PrimitiveData U g.radial.inner g.radial.outer c u)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent)
    (hell : ∀ n, g.length n = VariableGaugeMean.qLength (2 * h))
    (hfixed : (VariableGaugeMean.reconstructState g c u).pressure = u.pressure) :
    Fam.F19.halfPlus.OverlapLaw U.carrier (Fam.F19.halfPlus h - 1 / 2)
      (VariableGaugeMean.temporalPotential g h Fam.F19.halfPlus.index c u) := by
  intro n hn m hm k hk x hx
  have Hz := HP.axial_reconstructed ha hd hell hfixed
  have Hs : VariableGaugeMean.SupportedGauge g.radial.inner g.radial.outer (g.length m)
      U.carrier (u.axialResidual c m) := by
    rw [hell]
    exact Hz.supported m
  have Ht := TemporalStateCoherence.temporalPotential_on (bandScale_pos n m) (bandSlowEquiv h n m) k
    (overlap_open h U.isOpen n m) U.isOpen (fun _ hx => hx.2) g g c c u u h Fam.F19.halfPlus.index Fam.F19.halfPlus.index
    n m ha hd (HG n hn m hm k hk) (HS n hn m hm k hk) (HC n hn m hm k hk)
    (TemporalStateCoherence.clock_band_transport h n m _ _ k hk)
    (Hz.smooth m) (Hz.periodic m) Hs
  have he := Ht x hx
  simp only [streamScale] at he ⊢
  exact he
end NavierStokes.ActualMeanPhysicalData
end
end

-- REPLAY NavierStokes.NaturalCore.coreVelocity_at_origin 156 182
run_cmd IO.println "BLOCK NavierStokes.NaturalCore.coreVelocity_at_origin"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff Interval BigOperators
namespace NavierStokes.NaturalCore
open ProblemStatement AxisymmetricFields
#count_heartbeats in
theorem coreVelocity_at_origin_R {h j Λ : ℝ} {P0 a0 : ℝ → ℝ}
    {f U V Pr : ℝ × ℝ → ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    (hs : NaturalProfile.IsNaturalSolution h j Λ P0 a0 f U V Pr)
    {t : ℝ} (ht : t < 1) :
    coreVelocity h f V (t, 0) = ((1 - t) ^ (-Fam.F19.halfPlus h) * j) • coordinateVector 2 := by
  have hp : profilePoint t (0 : Space) ∈ profileDomain h Λ := core_axis_mem h Λ ht
  have hH := (meridionalPotential_contDiffAt hh hh1 hs.average_smooth hp).differentiableAt (by simp)
  have hK := (swirlPotential_contDiffAt hh hh1 hs.f_smooth hp).differentiableAt (by simp)
  change velocity (meridionalPotential h V) (swirlPotential h f) (t, 0) = _
  rw [velocity_on_axis _ _ t 0 hH hK (by simp) (by simp)]
  have haxis : V (0, 0) = j := by
    simpa only [NaturalAxisData.U, mul_zero, zero_add] using
      hs.average_axis 0 (by norm_num [NaturalAxisCoefficients.window])
  change (physicalQ h (t, (0, 0)) ^ (-Fam.F19.halfPlus h) *
    V (0 / physicalQ h (t, (0, 0)), physicalEta h (t, (0, 0)))) • coordinateVector 2 = _
  rw [physicalQ_at_zero_z hh hh1 ht, physicalEta_at_zero_z, zero_div, haxis]
end NavierStokes.NaturalCore
end
end

-- REPLAY NavierStokes.PhysicalSignedWave.PrimaryData.Views.StateData.actual_wave_physical 186 244
run_cmd IO.println "BLOCK NavierStokes.PhysicalSignedWave.PrimaryData.Views.StateData.actual_wave_physical"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PhysicalSignedWave
open Set Function Filter Matrix HarmonicCalculus WeightedClasses
open ProblemStatement CommonCoverSolve TorusInverse
open scoped ContDiff Topology InnerProductSpace BigOperators
section QuotientAlgebra
end QuotientAlgebra
namespace ReferencePhase
variable (C : ReferencePhase)
end ReferencePhase
section ActualRequest
end ActualRequest
section CoefficientTransport
variable {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end CoefficientTransport
namespace PrimaryData
variable {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (B : PrimaryData U)
namespace Regular
variable {B} {request : ℕ → Cylinder → Vec2} {reference : ℕ} {column : Fin 2}
  (H : B.Regular request reference column)
include H
end Regular
end PrimaryData
namespace PrimaryData
variable {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (B : PrimaryData U) (reference : ℕ)
namespace Views
variable {B reference} (V : B.Views reference)
namespace StateData
variable {V} (D : V.StateData)
#count_heartbeats in
theorem actual_wave_physical_R (j : Fin 2) (n : ℕ)
    (R : B.Regular D.referenceRequest reference j) (Fam.F19.halfPlus : B.Angular D.referenceRequest reference)
    (hK : B.base.frequency reference ≠ 0)
    (G : ChartGeometry B.base B.strip B.directions reference V.exponent V.referenceScale V.referenceCover)
    (H : ChartGeometry (B.viewBase V.background V.frequency (fun n => V.map n) reference)
      V.strip V.directions n V.exponent (V.scale n) (V.cover n))
    (hmap : MapsTo (V.map n) V.strip.domain B.strip.domain)
    (hradius : ∀ x ∈ V.strip.domain, 0 < x.1.1)
    {z : SpaceTime}
    (hz : z ∈ (PhysicalResidualBridge.commonGraph (V.scale n) V.exponent (V.cover n)).source V.strip.domain)
    {delta : ℝ} (hdelta : 0 < delta) (chart : PolarCharts.Index)
    (hchart : z ∈ PhysicalCurlCovariance.validCylindrical delta chart) (component : Fin 3) :
    (vectorMode ((V.exactCoefficients D.request j).frequency n) ((V.exactCoefficients D.request j).phase n)
      ((V.exactCoefficients D.request j).amplitude n)
      ((PhysicalResidualBridge.commonGraph (V.scale n) V.exponent (V.cover n)).map z) component).re =
        V.scale n ^ Fam.F19.halfPlus V.exponent * CylindricalResidual.frame (-(z.2 1))
          (V.physicalVelocity D.referenceRequest j delta (z.1, CylindricalResidual.chart z.2)) component := by
  have he := V.wave_physical D.request D.referenceRequest j n R Fam.F19.halfPlus hK G H hmap hradius
    (D.request_transport n) hz hdelta chart hchart component
  rwa [V.wave_eq_exact D.request j n H] at he
end StateData
end Views
end PrimaryData
end NavierStokes.PhysicalSignedWave
end
end

-- REPLAY NavierStokes.ActualSignedPhysicalData.pressure_physical_bound 248 332
run_cmd IO.println "BLOCK NavierStokes.ActualSignedPhysicalData.pressure_physical_bound"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualSignedPhysicalData
open Set Function Filter ProblemStatement HarmonicCalculus LinearWaveBounds WeightedClasses
open scoped Topology ContDiff BigOperators InnerProductSpace
attribute [local instance] Classical.propDecidable
section Repartition
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  (a : WaveCoefficients D) (s : StripData D) (d : GraphDirections D)
  (H : ℕ → D → Mat2) (T R : ℕ → D → Vec2)
  (mask factor cutoff : ℕ → D → ℝ) (unit Ndot : ℕ → D → Space)
  (A : ℕ → D → Space →L[ℝ] Space) (j : Fin 2)
end Repartition
section Copies
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {K : Type}
end Copies
section Geometry
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
end Geometry
section ActualCopies
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
  (hh : 0 ≤ h) (label : SlotColoring.Label) (hl : 4 ≤ label.1) (gap : ℕ)
  {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (B : PhysicalSignedWave.PrimaryData U)
  {reference : ℕ} (V : B.Views reference)
end ActualCopies
section PhysicalFamilies
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
  (hh : 0 ≤ h) {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (f : SignedFamily U)
variable (G : ReferenceGeometry sys f)
include G hh
end PhysicalFamilies
section NativeSources
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
  (hh : 0 ≤ h) {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (f : SignedFamily U)
variable {a b : ℝ} {s : StripData Native}
  (hloc : PrimitiveLocalization (h := h) f a b s)
include hloc
end NativeSources
section NativeBounds
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
  (hh : 0 ≤ h) {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (f : SignedFamily U)
variable {a b : ℝ} (ha : 0 < a) (hp : NativeProfiles (h := h) f)
variable (hn : NativeRegular sys hh f)
include hn ha
variable {s : StripData Native} (hloc : PrimitiveLocalization (h := h) f a b s)
  (G : ReferenceGeometry sys f) (hh0 : 0 < h) (hh1 : h < 1 / 2) (hb : 0 < b)
include hp hloc G hh0 hh1 hb
end NativeBounds
section WaveData
variable {D h : ℝ}
  (sys : PartitionedCovariance.SlotSystem D h ActualSignedGeometry.radialVector ActualSignedGeometry.temporalVector)
  (hh : 0 ≤ h) {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow} (f : SignedFamily U)
  {a b : ℝ} {s : StripData Native} (hloc : PrimitiveLocalization (h := h) f a b s)
  (G : ReferenceGeometry sys f) (hh0 : 0 < h) (hh1 : h < 1 / 2)
  (ha : 0 < a) (hb : 0 < b)
include hloc hh0 hh1 ha hb
variable (hp : NativeProfiles (h := h) f) (hn : NativeRegular sys hh f)
  {P : ℝ} (hP : 1 ≤ P)
  (hf : ∀ L : NativeLabel f.active,
      |((f.primary L).pulse (f.column L)).phase.p L.val.1| ≤ P ∧
      |((f.primary L).pulse (f.column L)).phase.pz L.val.1| ≤ P ∧
      |((f.primary L).pulse (f.column L)).phase.x0 L.val.1| ≤ P)
  {α : ℝ} {w : SourceIndex → ℕ → Native → ℝ}
variable
  (hpotential : LocalPhysicalCopyBounds.LocalSourceBounds s h α w (nativePotentialSource sys hh f))
  (hpressure : LocalPhysicalCopyBounds.LocalSourceBounds s h α w (nativePressureSource sys hh f))
#count_heartbeats in
theorem pressure_physical_bound_R (m : ℕ) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ PhysicalWaveSum.preterminal,
      PhysicalWaveSum.physicalQ h x ≤ 1 →
      ‖iteratedFDeriv ℝ m
        (fun y => ((pressureFamily sys hh f).sum (a / 4) h sys.radius y).re) x‖ ≤
        C * PhysicalWaveSum.physicalQ h x ^
          (h * α - PhysicalClassBounds.physicalLoss h (-(2 * Fam.F19.halfPlus h)) m) :=
  (pressureWaveData sys hh f hloc G hh0 hh1 ha hb hp hn hP hf hpressure).pressure_bound hh0 hh1 m
end WaveData
end NavierStokes.ActualSignedPhysicalData
end
end

-- REPLAY NavierStokes.BaseContextAssembly.virtualStress_normalized 336 364
run_cmd IO.println "BLOCK NavierStokes.BaseContextAssembly.virtualStress_normalized"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseContextAssembly
open Set Function Filter WeightedClasses
open scoped ContDiff Topology BigOperators EuclideanSpace
section OperatorBounds
end OperatorBounds
section NativeGeometry
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
end NativeGeometry
section ActualFields
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
#count_heartbeats in
theorem virtualStress_normalized_R (n : ℕ) {x : Point} (hT : 0 < x.2.1.1) (hR : 0 < x.1) :
    virtualStress H v upper B n x =
      (ChartScales.epsilon F.data.h n *
        (BaseChartJets.normalizedCoordinates F.data.h (slowCoordinates x)).1 ^
          (-Fam.F19.halfPlus F.data.h - 1 / 2)) •
      FinalSlowBase.normalizedStress H v upper B
        (SlowBorelBase.scaleMap (ChartScales.Q n)
          (BaseChartJets.normalizedCoordinates F.data.h (slowCoordinates x))) := by
  rw [virtualStress_eq_raw H v upper B n hR, rawStress_normalized H v upper B n hT]
end ActualFields
end NavierStokes.BaseContextAssembly
end
end

-- REPLAY NavierStokes.CorrectionStep.signedTensorRemainder_divergence_mem 368 509
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.signedTensorRemainder_divergence_mem"
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
#count_heartbeats in
theorem signedTensorRemainder_divergence_mem_R {s : StripData D} {P : ℕ → D → ℝ}
    {σ κ : ℝ} (c : Context D) (hops : OperatorBounds s c.operators κ)
    (hσ : 1 / 5 ≤ σ) (hκ : κ ≤ 1 / 100000)
    (primary old tangent curl : HarmonicBlock D) (N : ℕ)
    (hop : SameCarrier old primary) (hot : SameCarrier old tangent)
    (hoc : SameCarrier old curl)
    (hpN : primary.BandLimited N) (hoN : old.BandLimited N)
    (htN : tangent.BandLimited N) (hcN : curl.BandLimited N)
    (ho : old.WaveBounds s P (1 / 2))
    (hd : (subBlock old primary).WaveBounds s P (17 / 25))
    (ht : tangent.WaveBounds s P (Fam.F19.halfPlus σ - κ))
    (hc : curl.WaveBounds s P (Fam.F19.halfPlus σ + 1 / 2 - 2 * κ))
    (hp0 : ∀ n i, primary.velocity n i 0 = 0) (ho0 : ∀ n i, old.velocity n i 0 = 0)
    (ht0 : ∀ n i, tangent.velocity n i 0 = 0) (hc0 : ∀ n i, curl.velocity n i 0 = 0)
    (hkp : ∀ n, old.angularFrequency n ≠ 0)
    (hP0 : ∀ n x, x ∈ s.domain → 0 ≤ P n x)
    (hP1 : ∀ n x, x ∈ s.domain → P n x ≤ 1) :
    let E := signedTensorRemainder primary.oscillation old.oscillation tangent.oscillation curl.oscillation
    MeanClass s (ExponentLedger.meanExponent σ + 17 / 100) (thetaCovarianceChange c.operators E) ∧
      MeanClass s (ExponentLedger.meanExponent σ + 17 / 100) (axialCovarianceChange c.operators E) ∧
      MeanClass s (ExponentLedger.meanExponent σ + 17 / 100) (radialCovarianceChange c.operators E) := by
  have he := signedTensorRemainder_mem (γ := ExponentLedger.meanExponent σ + 17 / 100 + κ)
    primary old tangent curl N hop hot hoc hpN hoN htN hcN ho hd ht hc hp0 ho0 ht0 hc0
    (by linarith) (by unfold Fam.F19.halfPlus ExponentLedger.meanExponent; linarith)
    (by unfold Fam.F19.halfPlus ExponentLedger.meanExponent; linarith)
    (by unfold Fam.F19.halfPlus ExponentLedger.meanExponent; linarith)
    hkp hP0 hP1
  simpa only [add_sub_cancel_right] using
    And.intro (thetaCovarianceChange_mem hops he)
      (And.intro (axialCovarianceChange_mem hops he) (radialCovarianceChange_mem hops he))
end SignedTensorRemainder
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.InitializedPhysicalBackground.initializedVelocity_finite_rate 513 544
run_cmd IO.println "BLOCK NavierStokes.InitializedPhysicalBackground.initializedVelocity_finite_rate"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.InitializedPhysicalBackground
open Set Filter ProblemStatement DiagonalResidual PhysicalStageBounds
open scoped Topology ContDiff BigOperators
section NativeInitialization
variable {h : ℝ} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {I K : Type*}
end NativeInitialization
section ActualBase
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
  {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] {I K : Type*}
#count_heartbeats in
theorem initializedVelocity_finite_rate_R (upper : ℝ) (B : ℕ)
    (WA : WaveData F.data.h D I K (Fin 3))
    (MA : MeanData F.data.h (Fam.F19.halfPlus F.data.h - 1 / 2))
    (MB : MeanData F.data.h (Fam.F19.halfPlus F.data.h)) (m : ℕ) :
    FiniteJetRate ActualBaseVelocityBounds.endpoint (PhysicalWaveSum.physicalQ F.data.h)
      (initializedVelocity H v upper B WA MA MB) m
      (-maxJetLoss (initialLoss F.data.h WA.alpha WA.shift MA.alpha MB.alpha) m) := by
  have hq := ActualBaseVelocityBounds.endpoint_q_small F.data.h_pos F.data.h_lt_half
  apply finiteJetRate_of_jetRate (hq.mono (fun _ hw => hw.1))
  intro i hi
  exact (initializedVelocity_rate H v upper B WA MA MB i).weaken hq
    (neg_le_neg (le_maxJetLoss _ hi))
end ActualBase
end NavierStokes.InitializedPhysicalBackground
end
end

-- REPLAY NavierStokes.BaseContextAssembly.rawStress_normalized 548 596
run_cmd IO.println "BLOCK NavierStokes.BaseContextAssembly.rawStress_normalized"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseContextAssembly
open Set Function Filter WeightedClasses
open scoped ContDiff Topology BigOperators EuclideanSpace
section OperatorBounds
end OperatorBounds
section NativeGeometry
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
end NativeGeometry
section ActualFields
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
#count_heartbeats in
theorem rawStress_normalized_R (n : ℕ) {x : Point} (hT : 0 < x.2.1.1) :
    rawStress H v upper B n x =
      (ChartScales.epsilon F.data.h n *
        (BaseChartJets.normalizedCoordinates F.data.h (slowCoordinates x)).1 ^
          (-Fam.F19.halfPlus F.data.h - 1 / 2)) •
      FinalSlowBase.normalizedStress H v upper B
        (SlowBorelBase.scaleMap (ChartScales.Q n)
          (BaseChartJets.normalizedCoordinates F.data.h (slowCoordinates x))) := by
  have hq := BaseChartJets.normalizedCoordinates_q_pos F.data.h_pos F.data.h_lt_half
    (p := slowCoordinates x) hT
  have he := FinalSlowBase.physical_stress_eq_normalized H v upper B
    (p := AxisymmetricFields.profilePoint (physicalPoint F.data.h n x).1 (physicalPoint F.data.h n x).2)
    (physicalPoint_time F.data.h n hT)
  have hc := BaseChartJets.bandPoint_chart F.data.h_pos F.data.h_lt_half (ChartScales.Q_pos n)
    (p := slowCoordinates x) hT
  change SlowBorelBase.physicalChart F.data.h
    (AxisymmetricFields.profilePoint (physicalPoint F.data.h n x).1 (physicalPoint F.data.h n x).2) = _ at hc
  rw [hc] at he
  change ChartScales.Q n ^ (2 * Fam.F19.halfPlus F.data.h) • _ = _
  rw [he, smul_smul]
  congr 1
  simp only [SlowBorelBase.scaleMap_apply]
  rw [Real.mul_rpow (ChartScales.Q_pos n).le hq.le, ← mul_assoc,
    ← Real.rpow_add (ChartScales.Q_pos n)]
  have hex : 2 * Fam.F19.halfPlus F.data.h + (-Fam.F19.halfPlus F.data.h - 1 / 2) = F.data.h := by
    unfold Fam.F19.halfPlus
    ring
  rw [hex]
  rfl
end ActualFields
end NavierStokes.BaseContextAssembly
end
end

