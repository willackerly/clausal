import Tool
import F15
import NavierStokes.ActualInitialMean
import NavierStokes.ActualMeanPhysicalData
import NavierStokes.ActualWaveRegularityData
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionStep
import NavierStokes.DefectIncrementBounds
import NavierStokes.GaugeDebtIncrement
import NavierStokes.HarmonicFields
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

-- REPLAY NavierStokes.ActualInitialMean.seed_covariance_regular 23 44
run_cmd IO.println "BLOCK NavierStokes.ActualInitialMean.seed_covariance_regular"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualInitialMean
open Set Filter CorrectionState CorrectionInitialization WeightedClasses
open scoped ContDiff Topology BigOperators
section AngularBookkeeping
variable {B N0 : ℕ}
end AngularBookkeeping
section CovarianceInputs
variable {B N0 : ℕ}
#count_heartbeats in
theorem seed_covariance_regular_R (B N0 : ℕ) (i j : Fin 3) :
    GaugeDebtIncrement.Regular ActualPrimary.standardRegion
      ActualPrimary.commonGauge.radial.inner ActualPrimary.commonGauge.radial.outer
      ((seed B N0).covariance i j) :=
  WaveStateRegularity.bilinearCovariance_regular ActualPrimary.standardRegion
    (seed_angularSmooth B N0) (seed_angularSmooth B N0) (seed_waveSupport B N0) i j
end CovarianceInputs
end NavierStokes.ActualInitialMean
end
end

-- REPLAY NavierStokes.ActualMeanPhysicalData.CycleData.pressure_moving 48 72
run_cmd IO.println "BLOCK NavierStokes.ActualMeanPhysicalData.CycleData.pressure_moving"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualMeanPhysicalData
open Set Function Filter ProblemStatement
open PhysicalResidualNaturality GaugeStateCoherence
open scoped Topology ContDiff BigOperators
open CorrectionInitialization.ActualPrimary
open CorrectionStep CorrectionState
namespace CycleData
variable {ι : Type} {G : CycleStateCoherence.Geometry} {N Δ : ℕ}
    {p : ℕ → CycleParameters ι} {c : Context Point} {seed : CycleState ι}
    {U : LocalSignedRequest.SlowRegion (2 * G.h)} (D : CycleData G N Δ p c seed U)
include D
#count_heartbeats in
theorem pressure_moving_R
    (hseed : (VariableGaugeMean.reconstructState G.gauge c seed.state).pressure = seed.state.pressure)
    (j : ℕ) :
    GaugeMomentBalances.MovingField U G.inner G.outer (CycleState.iterate p c seed j).state.pressure :=
  (D.primitives j).pressure G.inner_pos (ChartScales.radialExponent_pos G.h G.h_pos.le)
    (fun _ => rfl) (D.reconstructed hseed j)
end CycleData
end NavierStokes.ActualMeanPhysicalData
end
end

-- REPLAY NavierStokes.ActualWaveRegularityData.signed_gaussian_coefficients_smooth 76 98
run_cmd IO.println "BLOCK NavierStokes.ActualWaveRegularityData.signed_gaussian_coefficients_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualWaveRegularityData
open Set Function Filter WeightedClasses HarmonicCalculus
open CorrectionInitialization CommonCoverSolve TorusInverse
open scoped Topology ContDiff BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem signed_gaussian_coefficients_smooth_R (l : Index B N0)
    (request : ℕ → FullPoint → SignedWaveUpdate.Vec2) {α : ℝ}
    (hg : MemClass ActualSignedStageControls.fullStrip
      (fun _ x => Real.sqrt (ActualSignedStageControls.fullStrip.zeta x)) α
      ((signedCopies l request).globalGaussian (ActualSignedStageControls.parameters l).directions))
    (n : ℕ) (i : Fin 3) :
    HarmonicResidual.SmoothCoefficients (PhysicalMeanDomain.slowDomain ActualPrimary.standardRegion.carrier)
      (((ActualSignedStageControls.parameters l).gaussianBlock ActualPrimaryBounds.strip request).velocity n i) := by
  apply smooth_conjugatePair
  exact ((contDiffOn_pi.mp (signed_gaussian_full_regular l request hg n).1) i).comp
    (HarmonicWaveInteraction.inclusion (D := Point)).contDiff.contDiffOn (fun _ hx => ⟨hx, mem_univ _⟩)
end NavierStokes.ActualWaveRegularityData
end
end

-- REPLAY NavierStokes.ActualWaveRegularityData.signed_pressure_coefficients_smooth 102 124
run_cmd IO.println "BLOCK NavierStokes.ActualWaveRegularityData.signed_pressure_coefficients_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualWaveRegularityData
open Set Function Filter WeightedClasses HarmonicCalculus
open CorrectionInitialization CommonCoverSolve TorusInverse
open scoped Topology ContDiff BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem signed_pressure_coefficients_smooth_R (l : Index B N0)
    (request : ℕ → FullPoint → SignedWaveUpdate.Vec2) {α : ℝ}
    (hp : MemClass ActualSignedStageControls.fullStrip
      (fun n x => Real.sqrt (ActualSignedStageControls.fullStrip.zeta x) *
        ActualSignedStageControls.envelope l n x) α (signedCopies l request).common.pressure)
    (n : ℕ) :
    HarmonicResidual.SmoothCoefficients (PhysicalMeanDomain.slowDomain ActualPrimary.standardRegion.carrier)
      (((ActualSignedStageControls.parameters l).exactBlock ActualPrimaryBounds.strip request).pressure n) := by
  apply smooth_conjugatePair
  exact (signed_pressure_full_regular l request hp n).1.comp
    (HarmonicWaveInteraction.inclusion (D := Point)).contDiff.contDiffOn (fun _ hx => ⟨hx, mem_univ _⟩)
end NavierStokes.ActualWaveRegularityData
end
end

-- REPLAY NavierStokes.CorrectionInitialization.ActualPrimary.rawPressure_jets 128 387
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.ActualPrimary.rawPressure_jets"
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
end PrimaryPiece
end PrimaryBlocks
section ZeroMean
open MeanIncrementBounds WeightedClasses
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end ZeroMean
section InitialMeanBounds
open MeanIncrementBounds WeightedClasses WeightedRadialPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end InitialMeanBounds
namespace AuxiliaryAverage
open StateMomentBalances.AuxiliaryAverage
open MeanIncrementBounds WeightedClasses WeightedRadialPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end AuxiliaryAverage
namespace MovingInitialization
open WeightedClasses MeanIncrementBounds VariableGaugeMean LocalSignedRequest
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
section MovingMoments
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
include hab
end MovingMoments
namespace LocalAverage
open PhysicalMeanDomain StateMomentBalances
open StateMomentBalances.AuxiliaryAverage
variable {V : Set S}
variable [FiniteDimensional ℝ S]
end LocalAverage
section MovingBarBounds
open StateMomentBalances
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingBarBounds
end MovingInitialization
namespace NativeResidual
open WeightedClasses LinearWaveBounds PrimaryConstruction
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
    {U : PhaseJetBounds.Domain ℕ PhaseCalculus.Slow}
namespace Control
variable {F : Fin 2 → PrimaryPulseBounds.PhaseConstruction U} {pref : Fin 2 → ℕ → ℝ}
    {s : StripData D} {c : Context D} {χ : ℕ → D × ℝ → PhaseCalculus.Slot}
    {b : ℕ → PhaseCalculus.Slow → ℝ} {frequency : ℕ → ℝ}
    {T : ℕ → D × ℝ → SmoothCovariance.Vec2} {mask cutoff : ℕ → D × ℝ → ℝ}
    {j : Fin 2} {kp : ℕ → ℤ}
    (C : Control F pref s c χ b frequency T mask cutoff j kp)
include C
end Control
end NativeResidual
namespace AssembledPrimary
open WeightedClasses LabelSumBounds
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
    {ι : Type} [Countable ι] [Nonempty ι]
end AssembledPrimary
namespace MovingInitialization
open Set Filter CorrectionState WeightedClasses MeanIncrementBounds VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology
namespace InitialRegularity
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end InitialRegularity
section RawRegularity
variable {coord : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent)
    (hell : ∀ n, g.length n = qLength coord)
    (c : Context Point) (u : State Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hprofile : ∀ R s, s ∈ U.carrier → ∀ Y,
      c.operators.radialProfile (R, (s, Y)) = c.operators.radialProfile (R, (s, 0)))
    (hm : u.mean = ⟨0, 0, 0⟩)
    (hWc : ∀ i j n, ContDiffOn ℝ ∞ (u.covariance i j n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hWp : ∀ i j n, PhysicalMeanDomain.PeriodicOn U.carrier (u.covariance i j n))
    (hWs : ∀ i j n, SupportedGauge g.radial.inner g.radial.outer (qLength coord)
      U.carrier (u.covariance i j n))
end RawRegularity
section TemporalBounds
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
end TemporalBounds
end MovingInitialization
namespace MovingInitialization
open Set Filter CorrectionState WeightedClasses MeanIncrementBounds VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology
section DebtAfterMean
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end DebtAfterMean
section TemporalSource
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end TemporalSource
section InitialRank
variable {coord A B cL cR : ℝ} (U : SlowRegion coord)
    (g : GaugeData PressureStream.Plane) (r : RankData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end InitialRank
end MovingInitialization
namespace MovingInitialization
open Set Filter CorrectionState WeightedClasses MeanIncrementBounds VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology
section PrimaryMeanData
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
local notation "st" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
namespace PrimaryMeanData
variable {U g ha hcL hcR ε L hε hεone hL} {c : Context Point} {u : State Point}
    (d : PrimaryMeanData U g ha hcL hcR ε L hε hεone hL c u)
include d
end PrimaryMeanData
end PrimaryMeanData
end MovingInitialization
namespace MovingInitialization
open Set Filter CorrectionState WeightedClasses MeanIncrementBounds VariableGaugeMean LocalSignedRequest
open scoped ContDiff Topology
section RankComposition
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
local notation "st" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
local notation "slowSt" => PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL
namespace PrimaryMeanData
variable {U g ha hcL hcR ε L hε hεone hL} {c : Context Point} {u : State Point}
    (d : PrimaryMeanData U g ha hcL hcR ε L hε hεone hL c u)
    {h : ℝ} {index : ℕ → ℕ} {axial : PressureStream.Plane × PressureStream.Plane}
    (t : TemporalStateBounds U g ha hcL hcR ε L hε hεone hL h index axial c u)
include d t
end PrimaryMeanData
end RankComposition
section InitialMeanConclusion
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (r : RankData PressureStream.Plane) (ha : 0 < g.radial.inner) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    {ι : Type} (labels : ℕ → Finset ι) (pieces : ι → PrimaryPiece (Point × ℝ))
    (baseError : Oscillation Point) (c : Context Point)
    (d : PrimaryMeanData U g ha hcL hcR ε L hε hεone hL c (bandSeed labels pieces baseError))
local notation "st" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
local notation "slowSt" => PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL
end InitialMeanConclusion
end MovingInitialization
namespace CommonWindow
open Set Function
end CommonWindow
namespace ActualPrimary
open Set Function
open scoped ContDiff Topology
section NativeFields
variable {B N0 : ℕ}
end NativeFields
section NativePair
variable {B N0 : ℕ}
end NativePair
section Coordinates
variable {B N0 : ℕ}
end Coordinates
section AmplitudeIdentity
variable {B N0 : ℕ}
end AmplitudeIdentity
section ActualMask
variable {B N0 : ℕ}
end ActualMask
section ChosenNativeBounds
open PhaseJetBounds PrimaryPulseBounds PrimaryCopyBounds
#count_heartbeats in
theorem rawPressure_jets_R (B N0 : ℕ) (j : Fin 2) :
    PrimaryCopyBounds.NativeJets (nativeChart B N0).native
      (fun L x => ChartScales.epsilon h (BaseChartJets.cellBand L) * nativeEnvelope B N0 j L x)
      (fun L => rawPressure j L) := by
  let c := nativeChart B N0
  have hp := PrimaryCopyBounds.phasePressure_carrier_jets (phases B N0 j) c.coordinate
    c.scale c.coordinate_jets c.maps (rawVelocity_jets B N0 j) h outgoing.data.h_pos.le BaseChartJets.cellBand
  have he : (fun L x => Real.sqrt (ChartScales.epsilon h (BaseChartJets.cellBand L)) *
      (Real.sqrt (ChartScales.epsilon h (BaseChartJets.cellBand L)) * nativeEnvelope B N0 j L x)) =
      (fun L x => ChartScales.epsilon h (BaseChartJets.cellBand L) * nativeEnvelope B N0 j L x) := by
    funext L x
    rw [← mul_assoc, Real.mul_self_sqrt (ChartScales.epsilon_pos h _).le]
  rw [he] at hp
  exact hp.congr (fun L x _ => phasePressure_eq_raw B N0 j L x)
end ChosenNativeBounds
end ActualPrimary
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.directional 391 582
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.directional"
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
theorem directional_R (hf : GaugeSupported a b ell U f) (hU : IsOpen U)
    (hell : ContinuousOn ell U) (v : PressureStream.Lift S) :
    GaugeSupported a b ell U (fun n x => fderiv ℝ (f n) x v) :=
  fun n => fderiv_apply_supportedGauge hU hell (hf n) (fun _ => v)
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.radialDiv 586 777
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.radialDiv"
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
theorem radialDiv_R (hf : GaugeSupported a b ell U f) (hU : IsOpen U)
    (hell : ContinuousOn ell U) (o : Operators (PressureStream.Lift S)) (t : ℝ) :
    GaugeSupported a b ell U (o.radialDiv t f) :=
  (hf.dr hU hell o).add ((hf.mul_left o.invRadius).smul t)
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.smul 781 973
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.smul"
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
theorem smul_R (hf : GaugeSupported a b ell U f) (t : ℝ) :
    GaugeSupported a b ell U (t • f) := by
  intro n x hx hn
  exact hf n x hx (right_ne_zero_of_mul hn)
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.sub 977 1168
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
theorem sub_R (hf : GaugeSupported a b ell U f) (hg : GaugeSupported a b ell U g) :
    GaugeSupported a b ell U (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionStep.GaugeSupported.viscosity 1172 1365
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.GaugeSupported.viscosity"
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
theorem viscosity_R (hf : GaugeSupported a b ell U f) (hU : IsOpen U)
    (hell : ContinuousOn ell U) (o : Operators (PressureStream.Lift S)) (t : ℝ) :
    GaugeSupported a b ell U (o.viscosity t f) :=
  (((((hf.dr hU hell o).dr hU hell o).add ((hf.dr hU hell o).mul_left o.invRadius)).add
    ((hf.dz hU hell o).dz hU hell o)).sub
      (((hf.mul_left o.invRadius).mul_left o.invRadius).smul t)).mul_left (fun n _ => o.epsilon n)
end GaugeSupported
end MovingSupport
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.DefectIncrementBounds.Shell.directional 1369 1387
run_cmd IO.println "BLOCK NavierStokes.DefectIncrementBounds.Shell.directional"
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
theorem directional_R (hf : Shell a b f) (v : Point P) :
    Shell a b (fun n x => fderiv ℝ (f n) x v) :=
  ⟨fun n => ((hf.smooth n).fderiv_right (by simp)).clm_apply contDiff_const,
    fun n => RadialAlias.radialSupport_fderiv_apply (hf.supported n) v⟩
end Shell
end
end NavierStokes.DefectIncrementBounds
end

-- REPLAY NavierStokes.DefectIncrementBounds.Shell.neg 1391 1409
run_cmd IO.println "BLOCK NavierStokes.DefectIncrementBounds.Shell.neg"
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
theorem neg_R (hf : Shell a b f) : Shell a b (-f) := by
  refine ⟨fun n => (hf.smooth n).neg, ?_⟩
  intro n x hx
  exact hf.supported n (neg_ne_zero.mp hx)
end Shell
end
end NavierStokes.DefectIncrementBounds
end

-- REPLAY NavierStokes.DefectIncrementBounds.Shell.smul 1413 1429
run_cmd IO.println "BLOCK NavierStokes.DefectIncrementBounds.Shell.smul"
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
theorem smul_R (hf : Shell a b f) (c : ℝ) : Shell a b (c • f) :=
  hf.band_mul (fun _ => c)
end Shell
end
end NavierStokes.DefectIncrementBounds
end

-- REPLAY NavierStokes.GaugeDebtIncrement.Regular.inv_mul 1433 1449
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.Regular.inv_mul"
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
theorem inv_mul_R (hf : Regular U a b f) (ha : 0 < a) (hab : a < b) {o : Operators Point}
    (ho : LocalRankDefect.LocalOperators U.carrier o) : Regular U a b (o.invRadius * f) :=
  hf.coefficient_mul ha hab ho.invRadius_smooth
end Regular
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.GaugeDebtIncrement.Regular.sub 1453 1468
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
theorem sub_R (hf : Regular U a b f) (hg : Regular U a b g) : Regular U a b (f - g) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end Regular
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.HarmonicFields.BandLimited.add 1472 1487
run_cmd IO.println "BLOCK NavierStokes.HarmonicFields.BandLimited.add"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped BigOperators Topology ContDiff ComplexConjugate Pointwise
namespace NavierStokes.HarmonicFields
#count_heartbeats in
theorem BandLimited.add_R {α : Type*} {c d : Coefficients α} {N : ℕ}
    (hc : BandLimited c N) (hd : BandLimited d N) : BandLimited (c + d) N := by
  intro j hj
  rcases Finset.mem_union.mp (Finsupp.support_add hj) with hj | hj
  · exact hc j hj
  · exact hd j hj
end NavierStokes.HarmonicFields
end
end

-- REPLAY NavierStokes.HarmonicResidual.SmoothCoefficients.mul 1491 1510
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.SmoothCoefficients.mul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
#count_heartbeats in
theorem SmoothCoefficients.mul_R {U : Set D} {c d : Coefficients D}
    (hc : SmoothCoefficients U c) (hd : SmoothCoefficients U d) : SmoothCoefficients U (c * d) := by
  intro j
  have he : (c * d) j = fun x => ∑ i ∈ c.support, c i x * d (j - i) x := by
    funext x
    exact HarmonicFields.convolution_apply c d j x
  rw [he]
  exact ContDiffOn.sum (fun i _ => (hc i).mul (hd (j - i)))
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicResidual.band_constant_mul 1514 1529
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.band_constant_mul"
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
theorem band_constant_mul_R (f : D → ℂ) {c : Coefficients D} {N : ℕ}
    (hc : BandLimited c N) : BandLimited (constantCoefficient f * c) N := by
  simpa only [zero_add] using (band_constantCoefficient f).mul hc
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicResidual.band_mul_constant 1533 1548
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.band_mul_constant"
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
theorem band_mul_constant_R {c : Coefficients D} {N : ℕ}
    (hc : BandLimited c N) (f : D → ℂ) : BandLimited (c * constantCoefficient f) N := by
  simpa only [add_zero] using hc.mul (band_constantCoefficient f)
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicResidual.smooth_nonlinearResidual 1552 1574
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.smooth_nonlinearResidual"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace Actual
end Actual
#count_heartbeats in
theorem smooth_nonlinearResidual_R {U : Set D} (hU : IsOpen U) {g : Frame D} (hg : g.Regular U)
    {Φ : D → ℝ} (hΦ : ContDiffOn ℝ ∞ Φ U) (k : ℝ) (kp : ℤ)
    {B a : VectorCoefficients D} (hB : ∀ i, SmoothCoefficients U (B i))
    (ha : ∀ i, SmoothCoefficients U (a i)) {c : Coefficients D} (hc : SmoothCoefficients U c) :
    ∀ i, SmoothCoefficients U (nonlinearResidual g k Φ kp B a c i) := fun i =>
  (((((ha i).differentiate hU hg.time hΦ k).add (smooth_transport hU hg hΦ k kp hB ha i)).add
    (smooth_transport hU hg hΦ k kp ha hB i)).add (smooth_gradient hU hg hΦ k kp hc i) |>.sub
      ((smoothCoefficients_constant contDiffOn_const).mul (smooth_vectorLaplacian hU hg hΦ k kp ha i))).add
    (smooth_transport hU hg hΦ k kp ha ha i)
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicResidual.smooth_transport 1578 1602
run_cmd IO.println "BLOCK NavierStokes.HarmonicResidual.smooth_transport"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicResidual
open Set Function Filter MeasureTheory
open HarmonicFields HarmonicCalculus
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace Actual
end Actual
#count_heartbeats in
theorem smooth_transport_R {U : Set D} (hU : IsOpen U) {g : Frame D} (hg : g.Regular U)
    {Φ : D → ℝ} (hΦ : ContDiffOn ℝ ∞ Φ U) (k : ℝ) (kp : ℤ)
    {a b : VectorCoefficients D} (ha : ∀ i, SmoothCoefficients U (a i))
    (hb : ∀ i, SmoothCoefficients U (b i)) :
    ∀ i, SmoothCoefficients U (transport g k Φ kp a b i) := by
  have hri : SmoothCoefficients U (constantCoefficient (fun x => (g.radius x : ℂ)⁻¹)) := by
    simpa only [Complex.ofReal_inv] using hg.invRadius
  intro i
  exact (((ha 0).mul ((hb i).differentiate hU hg.radial hΦ k)).add
    (((ha 1).mul hri).mul (((hb i).angular kp).add (smooth_rotate hb i)))).add
      ((ha 2).mul ((hb i).differentiate hU hg.axial hΦ k))
end NavierStokes.HarmonicResidual
end
end

-- REPLAY NavierStokes.HarmonicSourceSupport.NonzeroSupported.sub 1606 1623
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
theorem sub_R (hc : NonzeroSupported K c) (hd : NonzeroSupported K d) :
    NonzeroSupported K (c - d) := by
  simpa only [sub_eq_add_neg] using hc.add hd.neg
end NonzeroSupported
end NavierStokes.HarmonicSourceSupport
end
end

-- REPLAY NavierStokes.LocalRankDefect.LocalShell.directional 1627 1651
run_cmd IO.println "BLOCK NavierStokes.LocalRankDefect.LocalShell.directional"
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
theorem directional_R (hf : LocalShell a b U f) (hU : IsOpen U) (v : Point P) :
    LocalShell a b U (fun n x => fderiv ℝ (f n) x v) := by
  refine ⟨hf.smooth.directional (PhysicalMeanDomain.slowDomain_open hU) v, ?_⟩
  intro n x hx hn
  by_contra hr
  have he : f n =ᶠ[𝓝 x] fun _ => 0 := by
    filter_upwards [(PhysicalMeanDomain.slowDomain_open hU).mem_nhds hx,
      (isClosed_Icc.preimage continuous_fst).isOpen_compl.mem_nhds hr] with y hy hyr
    exact hf.zero_of_not_mem n y hy hyr
  exact hn (by change fderiv ℝ (f n) x v = 0; rw [he.fderiv_eq]; simp)
end LocalShell
end NavierStokes.LocalRankDefect
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.SmoothOn.directional 1655 1674
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.SmoothOn.directional"
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
theorem directional_R (hf : SmoothOn U f) (hU : IsOpen U) (v : D) :
    SmoothOn U (fun n x => fderiv ℝ (f n) x v) := by
  intro n
  exact ((contDiffOn_infty_iff_fderiv_of_isOpen hU).mp (hf n)).2.clm_apply contDiffOn_const
end SmoothOn
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.SmoothOn.smul 1678 1695
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.SmoothOn.smul"
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
theorem smul_R (hf : SmoothOn U f) (c : ℝ) : SmoothOn U (c • f) :=
  fun n => (hf n).const_smul c
end SmoothOn
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.SmoothOn.sub 1699 1716
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
theorem sub_R (hf : SmoothOn U f) (hg : SmoothOn U g) : SmoothOn U (f - g) :=
  hf.add hg.neg
end SmoothOn
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanStateRegularity.MovingField.directional 1720 1742
run_cmd IO.println "BLOCK NavierStokes.MeanStateRegularity.MovingField.directional"
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
theorem directional_R (hf : GaugeMomentBalances.MovingField U a b f) (v : Point) :
    GaugeMomentBalances.MovingField U a b (fun n x => fderiv ℝ (f n) x v) :=
  of_regular ((regular hf).directional v) (Periodic.directional hf.periodic U.isOpen v)
end MovingField
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.MeanStateRegularity.Periodic.mul 1746 1761
run_cmd IO.println "BLOCK NavierStokes.MeanStateRegularity.Periodic.mul"
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
theorem mul_R (hf : Periodic U f) (hg : Periodic U g) : Periodic U (f * g) :=
  fun n R s hs Y k => congrArg₂ (· * ·) (hf n R s hs Y k) (hg n R s hs Y k)
end Periodic
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.MeanStateRegularity.Periodic.sub 1765 1780
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
theorem sub_R (hf : Periodic U f) (hg : Periodic U g) : Periodic U (f - g) :=
  fun n R s hs Y k => congrArg₂ (· - ·) (hf n R s hs Y k) (hg n R s hs Y k)
end Periodic
end
end NavierStokes.MeanStateRegularity
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.directional 1784 1812
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.directional"
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
#count_heartbeats in
theorem directional_R (hf : Support a b ell U f) (hU : IsOpen U) (hl : ContinuousOn ell U)
    (v : PressureStream.Lift S) : Support a b ell U (fun n x => fderiv ℝ (f n) x v) :=
  fun n => fderiv_apply_supportedGauge hU hl (hf n) (fun _ => v)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.dz 1816 1844
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.dz"
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
#count_heartbeats in
theorem dz_R (hf : Support a b ell U f) (hU : IsOpen U) (hl : ContinuousOn ell U)
    (o : Operators (PressureStream.Lift S)) : Support a b ell U (o.dz f) :=
  (hf.directional hU hl o.eZ).mul_left (fun n _ => o.epsilon n)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.neg 1848 1876
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.neg"
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
theorem neg_R (hf : Support a b ell U f) : Support a b ell U (-f) :=
  fun n x hx hn => hf n x hx (neg_ne_zero.mp hn)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.radialDiv 1880 1908
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.radialDiv"
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
#count_heartbeats in
theorem radialDiv_R (hf : Support a b ell U f) (hU : IsOpen U) (hl : ContinuousOn ell U)
    (o : Operators (PressureStream.Lift S)) (r : ℝ) : Support a b ell U (o.radialDiv r f) :=
  (hf.dr hU hl o).add ((hf.mul_left o.invRadius).smul r)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.smul 1912 1940
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.smul"
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
theorem smul_R (hf : Support a b ell U f) (r : ℝ) : Support a b ell U (r • f) :=
  fun n x hx hn => hf n x hx (right_ne_zero_of_mul hn)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.Support.viscosity 1944 1974
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.Support.viscosity"
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
#count_heartbeats in
theorem viscosity_R (hf : Support a b ell U f) (hU : IsOpen U) (hl : ContinuousOn ell U)
    (o : Operators (PressureStream.Lift S)) (r : ℝ) : Support a b ell U (o.viscosity r f) :=
  (((((hf.dr hU hl o).dr hU hl o).add ((hf.dr hU hl o).mul_left o.invRadius)).add
    ((hf.dz hU hl o).dz hU hl o)).sub
      (((hf.mul_left o.invRadius).mul_left o.invRadius).smul r)).mul_left (fun n _ => o.epsilon n)
end Support
end Support
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.CoefficientsOn.neg 1978 1999
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.CoefficientsOn.neg"
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
theorem neg_R {U : Set D} {e : D ≃L[ℝ] E} {a : ℝ}
    {c : Coefficients D} {d : Coefficients E} (hc : CoefficientsOn U e a c d) :
    CoefficientsOn U e a (-c) (-d) := by
  intro j x hx
  change -c j x = a • (-d j (e x))
  rw [hc j x hx, smul_neg]
end CoefficientsOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.FrameOn.scalarLaplacian 2003 2038
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.FrameOn.scalarLaplacian"
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
#count_heartbeats in
theorem scalarLaplacian_R (H : FrameOn U e c l g r) (hU : IsOpen U) (hl : l ≠ 0)
    {a k kr : ℝ} {Phi : D → ℝ} {Psi : E → ℝ} (kp : ℤ)
    {f : Coefficients D} {q : Coefficients E} (hf : CoefficientsOn U e a f q)
    (hp : EqOn (fun x => k*Phi x) (fun x => kr*Psi (e x)) U) :
    CoefficientsOn U e (a*(l*l))
      (HarmonicResidual.scalarLaplacian g k Phi kp f)
      (HarmonicResidual.scalarLaplacian r kr Psi kp q) := by
  have hrr := (hf.differentiate hU H.radial hp).differentiate hU H.radial hp
  have hr := (H.inverseRadius hl).mul (hf.differentiate hU H.radial hp)
  have ht := (H.inverseRadiusSq hl).mul ((hf.angular kp).angular kp)
  have hzz := (hf.differentiate hU H.axial hp).differentiate hU H.axial hp
  have hrr' := hrr.reweight (b := a*(l*l)) (by ring)
  have hr' := hr.reweight (b := a*(l*l)) (by ring)
  have ht' := ht.reweight (b := a*(l*l)) (by ring)
  have hzz' := hzz.reweight (b := a*(l*l)) (by ring)
  exact ((hrr'.add hr').add ht').add hzz'
end FrameOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.PhysicalResidualNaturality.TripleOn.axialRadial 2042 2077
run_cmd IO.println "BLOCK NavierStokes.PhysicalResidualNaturality.TripleOn.axialRadial"
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
theorem axialRadial_R (hb : TripleOn U e c b br n nr) (hm : TripleOn U e c m mr n nr) :
    ScalarOn U e (c*c) (MeanIncrementBounds.axialRadial b m n) (MeanIncrementBounds.axialRadial br mr nr) :=
  ((hb.radial.mul hm.axial).add (hm.radial.mul hb.axial)).add (hm.radial.mul hm.axial)
end TripleOn
end NavierStokes.PhysicalResidualNaturality
end
end

-- REPLAY NavierStokes.PrimaryCopyBounds.NativeJets.neg 2081 2100
run_cmd IO.println "BLOCK NavierStokes.PrimaryCopyBounds.NativeJets.neg"
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
theorem neg_R (hf : NativeJets V w f) : NativeJets V w (fun i x => -f i x) :=
  hf.map (-ContinuousLinearMap.id ℝ E)
end NativeJets
end NavierStokes.PrimaryCopyBounds
end
end

