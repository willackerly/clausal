import Tool
import NavierStokes.ActualCurrentParticularAssembly
import NavierStokes.ActualPrimaryCovariance
import NavierStokes.ActualSignedMeanBinding
import NavierStokes.AlignedProfileSpectralCone
import NavierStokes.BaseChartJets
import NavierStokes.BaseRadialJets
import NavierStokes.BaseResidual
import NavierStokes.CorrectionInitialization
import NavierStokes.HeatTailEdit
import NavierStokes.HeatedOutgoing
import NavierStokes.OutgoingEntranceCone
import NavierStokes.OutgoingHistories
import NavierStokes.ParametricHeatTail
import NavierStokes.PulseCone
import NavierStokes.RenormalizedHeatMoment
import NavierStokes.SlowBorelBase
import NavierStokes.SlowExpansionResidual
import NavierStokes.SlowResidualMatching
import NavierStokes.TerminalHistoryBridge
import NavierStokes.TerminalPressure
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualCurrentParticularAssembly.velocityMap_apply 26 46
run_cmd IO.println "BLOCK NavierStokes.ActualCurrentParticularAssembly.velocityMap_apply"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualCurrentParticularAssembly
open Set Function Filter ProblemStatement CorrectionState CorrectionStep CorrectionInitialization
open ActualCurrentParticularPhysical
open scoped ContDiff Topology BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem velocityMap_apply_S (n : ℕ) (v : PhysicalResidualBridge.Cylinder → Fin 3 → ℝ)
    (z : SpaceTime) (k : Fin 3) :
    CyclePhysicalPrefixes.velocityMap (ActualCycleResidualBounds.actualBandGraph n) v z k =
      (ChartScales.Q n) ^ (-CoordinateAlgebra.A CorrectionInitialization.ActualPrimary.h) *
        v (PhysicalResidualTZ.graphMapTZ (ActualCycleResidualBounds.actualBandGraph n) z) k := by
  change (ActualCycleResidualBounds.actualBandGraph n).velocity
    (fun x => v (PhysicalResidualTZ.swapCylinder x)) z k = _
  rw [PhysicalResidualBridge.ScaledGraph.velocity_apply]
  rfl
end NavierStokes.ActualCurrentParticularAssembly
end
end

-- REPLAY NavierStokes.ActualPrimaryCovariance.viewTangent_pair_covariance 50 93
run_cmd IO.println "BLOCK NavierStokes.ActualPrimaryCovariance.viewTangent_pair_covariance"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualPrimaryCovariance
open Set Function Filter
open scoped ContDiff Topology BigOperators
open CorrectionInitialization.ActualPrimary PartitionedCovariance PrimaryFieldAssembly
variable {B N0 : ℕ}
#count_heartbeats in
theorem viewTangent_pair_covariance_S (n : ℕ) {x : Point}
    (hx : x ∈ (BaseContextAssembly.nativeStrip nominal standardRegion).domain)
    (L : Label B N0) (hL : L ∈ unsignedLabels B N0 n) (i : Fin 2) :
    (∑ j : Fin 2, doubleAverage (fun Y theta =>
      viewTangent n x (L, j) Y theta 0 * viewTangent n x (L, j) Y theta i.succ)) =
      (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h)) ^ 2 *
        ChartScales.epsilon h (BaseChartJets.cellBand L) * spatialMask L (nativePoint n x L) ^ 2 *
          PrimaryTargetBounds.actualTarget modulation (nativePoint n x L) i := by
  by_cases hm : spatialMask L (nativePoint n x L) = 0
  · simp only [viewTangent, physicalTangentMode_zero_of_mask _ L _ hm, Pi.zero_apply,
      zero_mul, doubleAverage, SmoothLoop.angularMean, TorusAverages.squareAverage,
      intervalIntegral.integral_zero, zero_div, Finset.sum_const_zero, hm, zero_pow (by decide : (2 : ℕ) ≠ 0), mul_zero]
  have hT := BaseContextAssembly.nativeStrip_time nominal standardRegion hx
  have hp := spatialMask_carrier L (nativePoint_time n hT L) hm
  have hK := nativePoint_reference n hx L hm
  have hw := nativePoint_weight_pos n hx L
  have hi := active_cover_le n hL
  have he (j : Fin 2) : doubleAverage (fun Y theta =>
      viewTangent n x (L, j) Y theta 0 * viewTangent n x (L, j) Y theta i.succ) =
      doubleAverage (fun Y theta => physicalTangentMode j L (nativePoint n x L) Y theta 0 *
        physicalTangentMode j L (nativePoint n x L) Y theta i.succ) := by
    simp only [viewTangent, physicalTangentMode_eq_slot j L _ hp]
    rw [pair_diagonal_common (sourcePair L (nativePoint n x L) hp).pairData vectors_det hi]
    symm
    simpa only [slotVelocity_zero, slotVelocity_succ] using
      (sourcePair L (nativePoint n x L) hp).pairData.diagonal_covariance vectors_det
        (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h))
        (ChartScales.epsilon h (BaseChartJets.cellBand L))
        (fun k => PrimaryTargetBounds.actualTarget modulation (nativePoint n x L) k)
        (similarityScale L (nativePoint n x L)) (position L (nativePoint n x L)) j i
  simp_rw [he]
  exact physicalTangentMode_diagonal_covariance L (nativePoint n x L) hp hK hw i
end NavierStokes.ActualPrimaryCovariance
end
end

-- REPLAY NavierStokes.ActualSignedMeanBinding.primary_mode_view 97 124
run_cmd IO.println "BLOCK NavierStokes.ActualSignedMeanBinding.primary_mode_view"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualSignedMeanBinding
open Set Function Filter
open scoped ContDiff Topology BigOperators
open CorrectionInitialization.ActualPrimary ActualPrimaryCovariance
variable {B N0 : ℕ}
#count_heartbeats in
theorem primary_mode_view_S (n : ℕ) {x : Point}
    (hx : x ∈ ActualInitialization.geometry.strip.domain)
    (l : Label B N0 × Fin 2) (Y : TorusInverse.Plane) (theta : ℝ) (i : Fin 3) :
    (ActualInitialization.tangentBlock l).oscillation n ((x.1, (x.2.1, Y)), theta) i =
      ChartScales.Q n ^ CoordinateAlgebra.A h * viewTangent n x l Y theta i := by
  rw [ActualInitialization.tangentBlock_represents]
  have hr := ((BaseContextAssembly.nativeStrip_mem nominal standardRegion x).mp hx).2
  have hT := BaseContextAssembly.nativeStrip_time nominal standardRegion hx
  have hR := BaseContextAssembly.nativeStrip_radius nominal standardRegion hx
  have hrad : PrimaryTargetBounds.profileRadius h (nativePoint n x l.1) ∈
      Ioo (PrimaryTargetBounds.leftRadius nominal) (PrimaryTargetBounds.rightRadius nominal) := by
    rwa [nativePoint_profileRadius n hT hR]
  unfold ActualInitialization.primaryPiece
  rw [piece_tangent_representation,
    absoluteTangent_eq l.2 l.1 (toAbsolute n (x.1, (x.2.1, Y)), theta) hrad]
  rfl
end NavierStokes.ActualSignedMeanBinding
end
end

-- REPLAY NavierStokes.ActualSignedMeanBinding.velocityScale_eq 128 144
run_cmd IO.println "BLOCK NavierStokes.ActualSignedMeanBinding.velocityScale_eq"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualSignedMeanBinding
open Set Function Filter
open scoped ContDiff Topology BigOperators
open CorrectionInitialization.ActualPrimary ActualPrimaryCovariance
variable {B N0 : ℕ}
#count_heartbeats in
theorem velocityScale_eq_S (L : Label B N0) (n : ℕ) :
    velocityScale L n = ChartScales.Q n ^ CoordinateAlgebra.A h *
      ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h) := by
  simp only [velocityScale, PhysicalParticularWave.velocityWeight, PhysicalParticularWave.ratioPower,
    Real.rpow_neg (ChartScales.Q_pos _).le, div_eq_mul_inv]
end NavierStokes.ActualSignedMeanBinding
end
end

-- REPLAY NavierStokes.AlignedProfileSpectralCone.modulated_frequency_eq 148 174
run_cmd IO.println "BLOCK NavierStokes.AlignedProfileSpectralCone.modulated_frequency_eq"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AlignedProfileSpectralCone
open Set Function Filter ProfileHistories ProfileSpectralCone
open scoped ContDiff Topology InnerProductSpace
section Modulated
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
    (H : NominalConeAssembly.Certificate W) {d : ModulatedProfileAssembly.LoopData W}
    (v : ModulatedProfileAssembly.Witness d)
#count_heartbeats in
theorem modulated_frequency_eq_S {p : Slow} (hT : 0 < p.2.2) (hR : 0 < p.1) :
    BaseChartJets.leadingFrequency F.data.h W.axis.normalization
        (EntranceAlignedBase.modulatedCoefficients H v) p =
      (BaseChartJets.normalizedCoordinates F.data.h p).1 ^ (-CoordinateAlgebra.A F.data.h - 1 / 2) *
        v.profiles.f (BaseChartJets.normalizedCoordinates F.data.h p).2 := by
  have hh := ConstructedSlowBase.height_pos W
  have hh1 := ConstructedSlowBase.height_lt_half W
  have hX := normalized_X_pos hh hh1 hT hR
  have heta := BaseChartJets.normalizedCoordinates_eta hh hh1 hT
  rw [BaseChartJets.leadingFrequency_eq hh hh1 hT hR,
    (EntranceAlignedBase.modulated_zero_fields H v hX.le heta.le).1]
  field_simp [W.axis.normalization_pos.ne']
end Modulated
end NavierStokes.AlignedProfileSpectralCone
end
end

-- REPLAY NavierStokes.BaseChartJets.axial_eq_normalized_velocity 178 199
run_cmd IO.println "BLOCK NavierStokes.BaseChartJets.axial_eq_normalized_velocity"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseChartJets
open Set Filter Function PhaseJetBounds PrimaryPulseBounds
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem axial_eq_normalized_velocity_S {a : ℕ → ℕ} (ha : StrictMono a) {h C Q : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hQ : 0 < Q)
    {d : SlowBorelBase.Coefficients} (hd : SlowBorelBase.SmoothCoefficients d)
    {p : Slow} (hT : 0 < p.2.2) :
    axial a h d Q p = Q ^ CoordinateAlgebra.A h *
      SlowBorelBase.baseVelocity a h C d (bandPoint h Q p) 2 := by
  rw [SlowBorelBase.baseVelocity_axial ha hh hh1 hd C (bandPoint_time (h := h) hQ hT)]
  unfold SlowBorelBase.physicalProfile
  rw [bandPoint_profile hQ.le, physicalChart_band hh hh1 hQ hT]
  simp only [SlowBorelBase.scaleMap_apply, smul_eq_mul]
  rw [← mul_assoc, normalized_power hQ (normalizedCoordinates_q_pos hh hh1 hT)]
  rfl
end NavierStokes.BaseChartJets
end
end

-- REPLAY NavierStokes.BaseRadialJets.normalizedStream_deriv_Z 203 241
run_cmd IO.println "BLOCK NavierStokes.BaseRadialJets.normalizedStream_deriv_Z"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseRadialJets
open Set Filter Function BaseChartJets PhaseJetBounds PrimaryPulseBounds
open scoped ContDiff Topology BigOperators
#count_heartbeats in
theorem normalizedStream_deriv_Z_S {a : ℕ → ℕ} (ha : StrictMono a) {h C Q : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hQ : 0 < Q)
    {d : SlowBorelBase.Coefficients} (hd : SlowBorelBase.SmoothCoefficients d)
    {p : Slow} (hT : 0 < p.2.2) :
    PhaseCalculus.slowZ (normalizedStream a h d Q) p =
      Q ^ CoordinateAlgebra.A h * Q ^ CoordinateAlgebra.D h *
        AxisymmetricFields.partialZ (SlowBorelBase.streamFactor a h C d) (bandInput h Q p) := by
  have ht : (bandInput h Q p).1 < 1 := by
    change 1 - Q * p.2.2 < 1
    linarith [mul_pos hQ hT]
  have hs := (SlowBorelBase.physicalProfile_smoothAt ha hh hh1
    (SlowBorelBase.bundleComponent_smooth hd C 0) (-CoordinateAlgebra.A h) ht).differentiableAt (by simp)
  change DifferentiableAt ℝ (SlowBorelBase.streamFactor a h C d) (bandInput h Q p) at hs
  have he : normalizedStream a h d Q =ᶠ[𝓝 p]
      (fun q => Q ^ CoordinateAlgebra.A h * SlowBorelBase.streamFactor a h C d (bandInput h Q q)) := by
    filter_upwards [(isOpen_lt continuous_const continuous_snd.snd).mem_nhds hT] with q hq
    exact normalizedStream_eq hh hh1 hQ d hq
  have hb := ((bandInput_smooth h Q).differentiable (by simp)).differentiableAt (x := p) |>.hasFDerivAt
  have hder := (hs.hasFDerivAt.comp p hb).const_mul (Q ^ CoordinateAlgebra.A h)
  simp only [Function.comp_apply] at hder
  unfold PhaseCalculus.slowZ
  rw [he.fderiv_eq, hder.fderiv]
  simp only [_root_.smul_apply, ContinuousLinearMap.comp_apply,
    smul_eq_mul, bandInput_deriv_Z]
  have hez : ((0, (0, Q ^ CoordinateAlgebra.D h)) : Chart) =
      Q ^ CoordinateAlgebra.D h • (0, (0, 1)) := by simp
  rw [hez, map_smul]
  simp only [smul_eq_mul, AxisymmetricFields.partialZ]
  ring
end NavierStokes.BaseRadialJets
end
end

-- REPLAY NavierStokes.BaseResidual.baseVelocity_norm_at_origin 245 269
run_cmd IO.println "BLOCK NavierStokes.BaseResidual.baseVelocity_norm_at_origin"
section
set_option linter.all false
noncomputable section
open Set Filter Function
open scoped Topology ContDiff BigOperators
namespace NavierStokes.BaseResidual
open SlowBorelBase
section Axis
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
#count_heartbeats in
theorem baseVelocity_norm_at_origin_S {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) {d : Coefficients}
    (hd : SmoothCoefficients d) (C : ℝ)
    (hz : ∀ j, 0 < j → d.axial j (0, 0) = 0) (h0 : 0 < d.axial 0 (0, 0))
    {t : ℝ} (ht : t < 1) :
    ‖baseVelocity a h C d (t, 0)‖ =
      (1 - t) ^ (-CoordinateAlgebra.A h) * d.axial 0 (0, 0) := by
  rw [baseVelocity_at_origin ha hh hh1 hd C hz ht, norm_smul]
  simp only [ProblemStatement.coordinateVector, PiLp.norm_single, norm_one,
    mul_one, Real.norm_eq_abs]
  exact abs_of_pos (mul_pos (Real.rpow_pos_of_pos (sub_pos.mpr ht) _) h0)
end Axis
end NavierStokes.BaseResidual
end
end

-- REPLAY NavierStokes.CorrectionInitialization.ActualPrimary.physicalTangentMode_diagonal_covariance 273 540
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.ActualPrimary.physicalTangentMode_diagonal_covariance"
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
end ChosenNativeBounds
section ActualTangentCovariance
open PartitionedCovariance PrimaryFieldAssembly
variable {B N0 : ℕ}
#count_heartbeats in
theorem physicalTangentMode_diagonal_covariance_S (L : Label B N0) (p : PhaseCalculus.Slow)
    (hp : p ∈ (PrimaryGeometryAssembly.domain nominal (choice B N0).prepared.N).carrier L)
    (hK : p ∈ PositiveRepresentatives.positivePart (PrimaryGeometryAssembly.referenceSet nominal))
    (hw : 0 < PrimaryTargetBounds.movingWeight nominal p) (i : Fin 2) :
    (∑ j : Fin 2, doubleAverage (fun Y theta =>
      physicalTangentMode j L p Y theta 0 * physicalTangentMode j L p Y theta i.succ)) =
      (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h)) ^ 2 *
        ChartScales.epsilon h (BaseChartJets.cellBand L) * spatialMask L p ^ 2 *
          PrimaryTargetBounds.actualTarget modulation p i := by
  simp only [physicalTangentMode, Pi.smul_apply, smul_eq_mul]
  simp_rw [show ∀ j Y theta, (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h) *
      tangentMode j L p Y theta 0) * (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h) *
      tangentMode j L p Y theta i.succ) =
      (ChartScales.Q (BaseChartJets.cellBand L) ^ (-CoordinateAlgebra.A h)) ^ 2 *
        (tangentMode j L p Y theta 0 * tangentMode j L p Y theta i.succ) from by intros; ring]
  simp_rw [doubleAverage_const_mul]
  rw [← Finset.mul_sum, tangentMode_diagonal_covariance L p hp hK hw i]
  ring
end ActualTangentCovariance
end ActualPrimary
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.HeatTailEdit.outgoingEdit_full 544 564
run_cmd IO.println "BLOCK NavierStokes.HeatTailEdit.outgoingEdit_full"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.HeatTailEdit
open OutgoingTail
#count_heartbeats in
theorem outgoingEdit_full_S (d : TailData) (ν eta : ℝ) {K X : ℝ}
    (hK : 0 < K) (hX : 0 < X) (hfull : 1 / 2 ≤ Real.log (X / K) + 1 / 5) :
    outgoingEdit d ν K eta X =
      outgoingAmplitude d * (X / K) ^ (-exponent d.h) *
        tailShape d (Real.log (X / K) + 1 / 5) *
          RadialHeatProfile.profile (1 + d.h) (2 * ν / X) := by
  unfold outgoingEdit
  rw [edit_after _ _ _ (by linarith),
    outgoingProfile_eq_powerTail_of_log d hK hX (by linarith) eta]
  rfl
end NavierStokes.HeatTailEdit
end
end

-- REPLAY NavierStokes.HeatTailEdit.outgoingEdit_heat_factorization 568 592
run_cmd IO.println "BLOCK NavierStokes.HeatTailEdit.outgoingEdit_heat_factorization"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.HeatTailEdit
open OutgoingTail
#count_heartbeats in
theorem outgoingEdit_heat_factorization_S (d : TailData) (ν eta : ℝ) {K X : ℝ}
    (hK : 0 < K) (hX : 0 < X) (hfull : 1 / 2 ≤ Real.log (X / K) + 1 / 5) :
    outgoingEdit d ν K eta X =
      (outgoingAmplitude d * K ^ exponent d.h) *
        RadialHeatProfile.spatialProfile (1 + d.h) ν X *
          tailShape d (Real.log (X / K) + 1 / 5) := by
  rw [outgoingEdit_full d ν eta hK hX hfull]
  have hexp : RadialHeatProfile.spatialExponent (1 + d.h) = -exponent d.h := by
    unfold RadialHeatProfile.spatialExponent exponent
    ring
  rw [RadialHeatProfile.spatialProfile, hexp, Real.div_rpow hX.le hK.le,
    Real.rpow_neg hK.le]
  simp only [div_inv_eq_mul]
  ring
end NavierStokes.HeatTailEdit
end
end

-- REPLAY NavierStokes.HeatTailEdit.powerTail_bound 596 618
run_cmd IO.println "BLOCK NavierStokes.HeatTailEdit.powerTail_bound"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.HeatTailEdit
#count_heartbeats in
theorem powerTail_bound_S {K e M X : ℝ} (hK : 0 < K) (he : 0 ≤ e) (hX : K ≤ X)
    (h : ℝ) {f : ℝ → ℝ} (hf : ∀ t, 0 ≤ t → |f t| ≤ M) :
    |powerTail h e K f X| ≤ e * M * (X / K) ^ (-exponent h) := by
  have hp := div_pos (hK.trans_le hX) hK
  have hlog : 0 ≤ Real.log (X / K) :=
    Real.log_nonneg ((one_le_div hK).mpr hX)
  unfold powerTail
  rw [abs_mul, abs_mul, abs_of_nonneg he, abs_of_pos (Real.rpow_pos_of_pos hp _)]
  calc
    _ ≤ (e * (X / K) ^ (-exponent h)) * M :=
      mul_le_mul_of_nonneg_left (hf _ hlog)
        (mul_nonneg he (Real.rpow_pos_of_pos hp _).le)
    _ = _ := by ring
end NavierStokes.HeatTailEdit
end
end

-- REPLAY NavierStokes.HeatedOutgoing.E_eventual_heat 622 649
run_cmd IO.println "BLOCK NavierStokes.HeatedOutgoing.E_eventual_heat"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped ContDiff Topology BigOperators
open NavierStokes.OutgoingProfile (Profile)
open NavierStokes.OutgoingDilation (switchRadius patchRadius patchRatio compensationPatch shapedPatchAmplitude)
namespace NavierStokes.HeatedOutgoing
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
#count_heartbeats in
theorem E_eventual_heat_S (F : Profile) (XR : ℝ) (c : ℝ → Coeff) (eta X : ℝ)
    (hXR : 0 < XR) (hX : 0 < X)
    (hlate : 3 ≤ Real.log (X / switchRadius F XR) + 1 / 5) :
    E F XR c (X, eta) =
      (OutgoingDilation.carrierAmplitude F * (switchRadius F XR) ^ HeatTailEdit.exponent F.data.h) *
        RadialHeatProfile.spatialProfile (1 + F.data.h) (ParametricHeatTail.diffusion eta) X := by
  rw [E_full_switch F XR c eta X hXR hX (by linarith), OutgoingTail.tailShape_late F.data hlate, mul_one]
end NavierStokes.HeatedOutgoing
end
end

-- REPLAY NavierStokes.HeatedOutgoing.E_full_switch 653 684
run_cmd IO.println "BLOCK NavierStokes.HeatedOutgoing.E_full_switch"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped ContDiff Topology BigOperators
open NavierStokes.OutgoingProfile (Profile)
open NavierStokes.OutgoingDilation (switchRadius patchRadius patchRatio compensationPatch shapedPatchAmplitude)
namespace NavierStokes.HeatedOutgoing
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
namespace CompensationWitness
variable {F : Profile} {XR C : ℝ} (w : CompensationWitness F XR C)
end CompensationWitness
#count_heartbeats in
theorem E_full_switch_S (F : Profile) (XR : ℝ) (c : ℝ → Coeff) (eta X : ℝ)
    (hXR : 0 < XR) (hX : 0 < X)
    (hfull : 1 / 2 ≤ Real.log (X / switchRadius F XR) + 1 / 5) :
    E F XR c (X, eta) =
      (OutgoingDilation.carrierAmplitude F * (switchRadius F XR) ^ HeatTailEdit.exponent F.data.h) *
        RadialHeatProfile.spatialProfile (1 + F.data.h) (ParametricHeatTail.diffusion eta) X *
          OutgoingTail.tailShape F.data (Real.log (X / switchRadius F XR) + 1 / 5) := by
  rw [E_after_switch F XR c eta X hXR
    (full_switch_above_radius (OutgoingDilation.switchRadius_pos F XR hXR) hX hfull)]
  exact HeatTailEdit.outgoingEdit_heat_factorization F.data _ _
    (OutgoingDilation.switchRadius_pos F XR hXR) hX hfull
end NavierStokes.HeatedOutgoing
end
end

-- REPLAY NavierStokes.OutgoingEntranceCone.axialLag_integrated_history 688 708
run_cmd IO.println "BLOCK NavierStokes.OutgoingEntranceCone.axialLag_integrated_history"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.OutgoingEntranceCone
open Set Filter MeasureTheory
open scoped Topology ContDiff
open OutgoingSchedule OutgoingTail NaturalAxisData
#count_heartbeats in
theorem axialLag_integrated_history_S (v : TailData) (y η : ℝ) :
    axialLag v y η = -transportW v.core v.h y η * (dropCoefficient v.core.m y * η) +
      4 * v.h * η * normalizedEnergyHistory v.core y η -
        d η * deriv (normalizedEnergyHistory v.core y) η +
          4 * A v.h * η * entrancePressure v y η -
            d η * deriv (entrancePressure v y) η := by
  rw [(normalizedEnergyHistory_hasDerivAt_eta v.core y η).deriv,
    (entrancePressure_hasDerivAt_eta v y η).deriv]
  unfold axialLag geometricAxialLag pressureAxialLag normalizedEnergyHistory
  ring
end NavierStokes.OutgoingEntranceCone
end
end

-- REPLAY NavierStokes.OutgoingHistories.Ns_after_endpoint 712 734
run_cmd IO.println "BLOCK NavierStokes.OutgoingHistories.Ns_after_endpoint"
section
set_option linter.all false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open NavierStokes.OutgoingSchedule NavierStokes.OutgoingTail
open NavierStokes.AngularMomentReset NavierStokes.UniformAngularReset
open NavierStokes.StressAlgebra
namespace NavierStokes.OutgoingHistories
variable {d : TailData} {K : ℝ}
#count_heartbeats in
theorem Ns_after_endpoint_S (w : ResetWitness d K) {Amp : ℝ → ℝ}
    (ha : ContDiff ℝ ∞ Amp) (eta : ℝ) {y : ℝ} (hy : d.core.endpoint ≤ y) :
    Ns w Amp (y, eta) =
      (4 * d.h * eta * S w Amp (y, eta) - coordinateFactor eta * dEta (S w Amp) (y, eta)) /
        Real.exp y + 4 * velocityExponent d.h * eta * Pi w (y, eta) -
          coordinateFactor eta * dEta (Pi w) (y, eta) := by
  rw [Ns_integrated, U_after_endpoint d Amp eta hy, M_after_endpoint d Amp eta hy,
    dEta_M_after_endpoint d ha eta hy]
  simp only [X, mul_zero, sub_zero, zero_div, zero_add]
end NavierStokes.OutgoingHistories
end
end

-- REPLAY NavierStokes.ParametricHeatTail.physicalEdit_eventual_heat_carrier 738 778
run_cmd IO.println "BLOCK NavierStokes.ParametricHeatTail.physicalEdit_eventual_heat_carrier"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.ParametricHeatTail
section IntegralChain
variable {α : Type*} [MeasurableSpace α] {μ : Measure α}
  {J : ℕ → ℝ → α → ℝ}
variable
  (hJ : ∀ᵐ t ∂μ, ∀ n ν, 0 ≤ ν →
    HasDerivWithinAt (fun u => J n u t) (J (n + 1) ν t) (Ici 0) ν)
  (hm : ∀ n ν, 0 ≤ ν → AEStronglyMeasurable (J n ν) μ)
  (hb : ChainDominated J μ)
include hJ hm hb
end IntegralChain
open HeatTailEdit
section Weighted
variable {W : ℝ → ℝ} {h K p q B : ℝ}
  (hh : 0 < h) (hK : 1 ≤ K)
  (hW : ContinuousOn W (Ioi K))
  (hB : 0 ≤ B)
  (hweight : ∀ X ∈ Ioi K, |W X| ≤ B * (X / K) ^ p)
  (hpq : p + q < 0)
include hh hK
include hW
include hB hweight
include hpq
end Weighted
open OutgoingTail
#count_heartbeats in
theorem physicalEdit_eventual_heat_carrier_S (d : TailData) {K q s τ eta : ℝ}
    (hK : 0 < K) (hq : 0 < q) (hs : 0 < s) (hν : diffusion eta = τ / q)
    (hlate : 3 ≤ Real.log ((s / q) / K) + 1 / 5) :
    q ^ (-exponent d.h) * physicalEdit d K eta (s / q) =
      (outgoingAmplitude d * K ^ exponent d.h) *
        RadialHeatProfile.spatialProfile (1 + d.h) τ s := by
  rw [physicalEdit_heat_carrier d hK hq hs hν (by linarith), tailShape_late d hlate, mul_one]
end NavierStokes.ParametricHeatTail
end
end

-- REPLAY NavierStokes.ParametricHeatTail.physicalEdit_heat_carrier 782 838
run_cmd IO.println "BLOCK NavierStokes.ParametricHeatTail.physicalEdit_heat_carrier"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.ParametricHeatTail
section IntegralChain
variable {α : Type*} [MeasurableSpace α] {μ : Measure α}
  {J : ℕ → ℝ → α → ℝ}
variable
  (hJ : ∀ᵐ t ∂μ, ∀ n ν, 0 ≤ ν →
    HasDerivWithinAt (fun u => J n u t) (J (n + 1) ν t) (Ici 0) ν)
  (hm : ∀ n ν, 0 ≤ ν → AEStronglyMeasurable (J n ν) μ)
  (hb : ChainDominated J μ)
include hJ hm hb
end IntegralChain
open HeatTailEdit
section Weighted
variable {W : ℝ → ℝ} {h K p q B : ℝ}
  (hh : 0 < h) (hK : 1 ≤ K)
  (hW : ContinuousOn W (Ioi K))
  (hB : 0 ≤ B)
  (hweight : ∀ X ∈ Ioi K, |W X| ≤ B * (X / K) ^ p)
  (hpq : p + q < 0)
include hh hK
include hW
include hB hweight
include hpq
end Weighted
open OutgoingTail
#count_heartbeats in
theorem physicalEdit_heat_carrier_S (d : TailData) {K q s τ eta : ℝ}
    (hK : 0 < K) (hq : 0 < q) (hs : 0 < s) (hν : diffusion eta = τ / q)
    (hfull : 1 / 2 ≤ Real.log ((s / q) / K) + 1 / 5) :
    q ^ (-exponent d.h) * physicalEdit d K eta (s / q) =
      (outgoingAmplitude d * K ^ exponent d.h) *
        RadialHeatProfile.spatialProfile (1 + d.h) τ s *
          tailShape d (Real.log ((s / q) / K) + 1 / 5) := by
  unfold physicalEdit
  rw [outgoingEdit_heat_factorization d (diffusion eta) eta hK (div_pos hs hq) hfull, hν]
  have hexp : RadialHeatProfile.spatialExponent (1 + d.h) = -exponent d.h := by
    unfold RadialHeatProfile.spatialExponent exponent
    ring
  have hp : (s / q) ^ (-exponent d.h) = s ^ (-exponent d.h) * q ^ exponent d.h := by
    rw [Real.div_rpow hs.le hq.le, Real.rpow_neg hq.le, div_inv_eq_mul]
  have hcancel : q ^ (-exponent d.h) * q ^ exponent d.h = 1 := by
    rw [Real.rpow_neg hq.le, inv_mul_cancel₀ (Real.rpow_pos_of_pos hq _).ne']
  simp only [RadialHeatProfile.spatialProfile, hexp, heat_ratio_physical hq hs, hp]
  calc
    _ = (q ^ (-exponent d.h) * q ^ exponent d.h) *
        ((outgoingAmplitude d * K ^ exponent d.h) *
          (s ^ (-exponent d.h) * RadialHeatProfile.profile (1 + d.h) (2 * τ / s)) *
            tailShape d (Real.log ((s / q) / K) + 1 / 5)) := by ring
    _ = _ := by rw [hcancel, one_mul]
end NavierStokes.ParametricHeatTail
end
end

-- REPLAY NavierStokes.PulseCone.Ns_integrated_Ubar 842 866
run_cmd IO.println "BLOCK NavierStokes.PulseCone.Ns_integrated_Ubar"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PulseCone
open Set Filter MeasureTheory
open scoped Topology ContDiff
open OutgoingSchedule OutgoingPulseBounds PulseLag
open OutgoingHistories
open OutgoingTail (TailData)
open UniformAngularReset (ResetWitness)
variable {d : TailData} {K : ℝ}
#count_heartbeats in
theorem Ns_integrated_Ubar_S (w : ResetWitness d K) {amp : ℝ → ℝ}
    (ha : ContDiff ℝ ∞ amp) (p : Point) :
    Ns w amp p = -W d amp p * U d amp p +
      StressAlgebra.axialExponent d.h * (Ubar d amp p - p.2 * dEta (Ubar d amp) p) +
      (4 * d.h * p.2 * S w amp p - StressAlgebra.coordinateFactor p.2 * dEta (S w amp) p) / X p +
      4 * StressAlgebra.velocityExponent d.h * p.2 * Pi w p -
        StressAlgebra.coordinateFactor p.2 * dEta (Pi w) p := by
  rw [Ns_integrated, Ubar_parameter d ha]
  unfold Ubar
  ring
end NavierStokes.PulseCone
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.heatCarrier_scaling 870 894
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.heatCarrier_scaling"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem heatCarrier_scaling_S (h C : ℝ) {q τ ν r : ℝ} (hq : 0 < q) (hr : 0 < r)
    (hν : ν = τ / q) :
    q ^ (-A h) * heatCarrier h C ν (r / Real.sqrt q) = heatCarrier h C τ r := by
  have hp : (r / Real.sqrt q) ^ 2 / 2 = (r ^ 2 / 2) / q := by
    rw [div_pow, Real.sq_sqrt hq.le]
    ring
  have hexp : RadialHeatProfile.spatialExponent (1 + h) = -A h := by
    unfold RadialHeatProfile.spatialExponent A
    ring
  have hs : 0 < r ^ 2 / 2 := by positivity
  simp only [heatCarrier, RadialHeatProfile.radialProfile,
    RadialHeatProfile.spatialProfile, hexp, hp, hν,
    ParametricHeatTail.heat_ratio_physical hq hs]
  rw [Real.div_rpow hs.le hq.le]
  field_simp [(Real.rpow_pos_of_pos hq (-A h)).ne']
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.heated_exterior 898 927
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.heated_exterior"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem heated_exterior_S (P : OutgoingProfile.Profile) {XR : ℝ} (hXR : 0 < XR)
    (c : ℝ → HeatedOutgoing.Coeff) (eta : ℝ) {X : ℝ} (hX : heatThreshold P XR ≤ X) :
    HeatedOutgoing.E P XR c (X, eta) =
      outgoingPowerAmplitude P XR * X ^ (-A P.data.h) *
        RadialHeatProfile.profile (1 + P.data.h) (2 * (1 - eta ^ 2) / X) := by
  have hK := OutgoingDilation.switchRadius_pos P XR hXR
  have hXp := (heatThreshold_pos P hXR).trans_le hX
  have hdiv : Real.exp 3 ≤ X / OutgoingDilation.switchRadius P XR := by
    apply (le_div_iff₀ hK).mpr
    simpa only [heatThreshold, mul_comm] using hX
  have hlog : 3 ≤ Real.log (X / OutgoingDilation.switchRadius P XR) := by
    simpa only [Real.log_exp] using Real.log_le_log (Real.exp_pos 3) hdiv
  have he := HeatedOutgoing.E_eventual_heat P XR c eta X hXR hXp (by linarith)
  rw [← outgoing_amplitude_eq_heat P hXR] at he
  have hexp : RadialHeatProfile.spatialExponent (1 + P.data.h) = -A P.data.h := by
    unfold RadialHeatProfile.spatialExponent A
    ring
  rw [he]
  simp only [RadialHeatProfile.spatialProfile, hexp, ParametricHeatTail.diffusion]
  ring
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.outgoing_amplitude_eq_heat 931 955
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.outgoing_amplitude_eq_heat"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem outgoing_amplitude_eq_heat_S (P : OutgoingProfile.Profile) {XR : ℝ} (hXR : 0 < XR) :
    outgoingPowerAmplitude P XR =
      OutgoingDilation.carrierAmplitude P *
        OutgoingDilation.switchRadius P XR ^ HeatTailEdit.exponent P.data.h := by
  change OutgoingTail.powerConstant P.data * XR ^ A P.data.h =
    (OutgoingTail.powerConstant P.data * Real.exp (-A P.data.h * HeatTailEdit.switchStart P.data)) *
      (XR * Real.exp (HeatTailEdit.switchStart P.data)) ^ A P.data.h
  rw [Real.mul_rpow hXR.le (Real.exp_pos _).le, ← Real.exp_mul]
  have he : Real.exp (-A P.data.h * HeatTailEdit.switchStart P.data) *
      Real.exp (HeatTailEdit.switchStart P.data * A P.data.h) = 1 := by
    rw [← Real.exp_add, show -A P.data.h * HeatTailEdit.switchStart P.data +
      HeatTailEdit.switchStart P.data * A P.data.h = 0 by ring, Real.exp_zero]
  calc
    _ = (OutgoingTail.powerConstant P.data * XR ^ A P.data.h) * 1 := by ring
    _ = _ := by rw [← he]; ring
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.outgoing_powerH 959 974
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.outgoing_powerH"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem outgoing_powerH_S (P : OutgoingProfile.Profile) {XR X : ℝ}
    (hXR : 0 < XR) (hX : 0 < X) :
    OutgoingDilation.powerH P XR X =
      Real.sqrt (2 * X) * (outgoingPowerAmplitude P XR * X ^ (-A P.data.h)) := by
  rw [OutgoingDilation.powerH, OutgoingDilation.powerE_coefficient P XR X hXR hX]
  rfl
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.referencePower_scaling 978 995
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.referencePower_scaling"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem referencePower_scaling_S (h C : ℝ) {q : ℝ} (hq : 0 < q) (r : ℝ) :
    q ^ (-A h) * referencePower h C (r / Real.sqrt q) = referencePower h C r := by
  have hp : (r / Real.sqrt q) ^ 2 / 2 = (r ^ 2 / 2) / q := by
    rw [div_pow, Real.sq_sqrt hq.le]
    ring
  rw [referencePower, referencePower, hp,
    Real.div_rpow (by positivity) hq.le]
  field_simp [(Real.rpow_pos_of_pos hq (-A h)).ne']
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.uTheta_eq_similarity_pullback 999 1015
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.uTheta_eq_similarity_pullback"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem uTheta_eq_similarity_pullback_S (h : ℝ) (E : ℝ × ℝ → ℝ) (t r z : ℝ) :
    uTheta h E t r z = SimilarityProfile.pullback h (-A h) E (t, (r ^ 2 / 2, z)) := by
  unfold uTheta profileVelocity SimilarityProfile.pullback SimilarityProfile.inner
    SimilarityProfile.X SimilarityProfile.q SimilarityProfile.eta Q eta
  have he : r ^ 2 / (2 * SimilarityCoordinates.coordinateQ (2 * h) (1 - t, z)) =
      (r ^ 2 / 2) / SimilarityCoordinates.coordinateQ (2 * h) (1 - t, z) := by ring
  rw [he]
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.weighted_referencePower 1019 1043
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.weighted_referencePower"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem weighted_referencePower_S (h C : ℝ) {r : ℝ} (hr : 0 < r) :
    r ^ 2 * referencePower h C r = C * (2 : ℝ) ^ A h * r ^ (1 - 2 * h) := by
  unfold referencePower
  rw [Real.div_rpow (sq_nonneg r) (by norm_num), Real.rpow_neg (by norm_num : (0 : ℝ) ≤ 2),
    div_inv_eq_mul, ← Real.rpow_natCast_mul hr.le]
  calc
    _ = C * (2 : ℝ) ^ A h * (r ^ (2 : ℝ) * r ^ ((2 : ℕ) * -A h)) := by
      rw [Real.rpow_two]
      ring
    _ = _ := by
      rw [← Real.rpow_add hr]
      congr 2
      unfold A
      norm_num
      ring
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.RenormalizedHeatMoment.weighted_referencePower_nonneg_radius 1047 1062
run_cmd IO.println "BLOCK NavierStokes.RenormalizedHeatMoment.weighted_referencePower_nonneg_radius"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.RenormalizedHeatMoment
#count_heartbeats in
theorem weighted_referencePower_nonneg_radius_S {h : ℝ} (hh1 : h < 1 / 2)
    (C : ℝ) {r : ℝ} (hr : 0 ≤ r) :
    r ^ 2 * referencePower h C r = C * (2 : ℝ) ^ A h * r ^ (1 - 2 * h) := by
  rcases eq_or_lt_of_le hr with rfl | hr
  · simp [referencePower, Real.zero_rpow (by linarith : 1 - 2 * h ≠ 0)]
  · exact weighted_referencePower h C hr
end NavierStokes.RenormalizedHeatMoment
end
end

-- REPLAY NavierStokes.SlowBorelBase.angularMoment_eq_normalizedSwirl 1066 1123
run_cmd IO.println "BLOCK NavierStokes.SlowBorelBase.angularMoment_eq_normalizedSwirl"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowBorelBase
open Set Filter Function
open scoped Topology ContDiff BigOperators
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
section PhysicalCoordinates
end PhysicalCoordinates
section PhysicalProfiles
end PhysicalProfiles
section PoweredTails
end PoweredTails
section LinearMaps
variable {W : Type} [NormedAddCommGroup W] [NormedSpace ℝ W]
end LinearMaps
section BaseFields
end BaseFields
section CoefficientIdentification
end CoefficientIdentification
section CartesianTails
end CartesianTails
section NormalizedTangential
end NormalizedTangential
section PhysicalIdentification
#count_heartbeats in
theorem angularMoment_eq_normalizedSwirl_S {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) {d : Coefficients} (hd : SmoothCoefficients d)
    (C : ℝ) {t : ℝ} (ht : t < 1) (x : ProblemStatement.Space) :
    -x 1 * baseVelocity a h C d (t, x) 0 + x 0 * baseVelocity a h C d (t, x) 1 =
      Real.sqrt (2 * AxisymmetricFields.radialEnergy x) *
        (cartesianChart h (t, x)).1 ^ (-CoordinateAlgebra.A h) *
          normalizedSwirl a h C d (cartesianChart h (t, x)) := by
  rw [baseVelocity_angularMoment ha hh hh1 hd C ht]
  let p := AxisymmetricFields.profilePoint t x
  let q := (physicalChart h p).1
  let s := AxisymmetricFields.radialEnergy x
  let v := slowSum a h d.phi (physicalChart h p)
  have hq : 0 < q := physicalChart_positive hh hh1 ht
  have hs : 0 ≤ 2 * s := mul_nonneg (by norm_num) (AxisymmetricFields.radialEnergy_nonneg x)
  have hsqrt : Real.sqrt (2 * s) ^ 2 = 2 * s := Real.sq_sqrt hs
  change (2 * s) * C⁻¹ * (q ^ (-CoordinateAlgebra.A h - 1 / 2) * v) =
    Real.sqrt (2 * s) * q ^ (-CoordinateAlgebra.A h) *
      (Real.sqrt (2 * (s / q)) / C * v)
  symm
  calc
    _ = Real.sqrt (2 * s) ^ 2 * C⁻¹ *
        (q ^ (-CoordinateAlgebra.A h) / q ^ (1 / 2 : ℝ)) * v := by
      rw [show 2 * (s / q) = (2 * s) / q by ring, Real.sqrt_div hs q,
        Real.sqrt_eq_rpow q]
      ring
    _ = _ := by
      rw [hsqrt, Real.rpow_sub hq]
      ring
end PhysicalIdentification
end NavierStokes.SlowBorelBase
end
end

-- REPLAY NavierStokes.SlowBorelBase.baseVelocity_axial 1127 1163
run_cmd IO.println "BLOCK NavierStokes.SlowBorelBase.baseVelocity_axial"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowBorelBase
open Set Filter Function
open scoped Topology ContDiff BigOperators
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
section PhysicalCoordinates
end PhysicalCoordinates
section PhysicalProfiles
end PhysicalProfiles
section PoweredTails
end PoweredTails
section LinearMaps
variable {W : Type} [NormedAddCommGroup W] [NormedSpace ℝ W]
end LinearMaps
section BaseFields
end BaseFields
section CoefficientIdentification
#count_heartbeats in
theorem baseVelocity_axial_S {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) {d : Coefficients} (hd : SmoothCoefficients d)
    (C : ℝ) {t : ℝ} (ht : t < 1) (x : ProblemStatement.Space) :
    baseVelocity a h C d (t, x) 2 =
      physicalProfile a h (-CoordinateAlgebra.A h) d.axial (AxisymmetricFields.profilePoint t x) := by
  have hH := (physicalProfile_smoothAt ha hh hh1 (bundleComponent_smooth hd C 0)
    (-CoordinateAlgebra.A h) (p := AxisymmetricFields.profilePoint t x) ht).differentiableAt (by simp)
  have hK := (physicalProfile_smoothAt ha hh hh1 (bundleComponent_smooth hd C 1)
    (1 / 2 - CoordinateAlgebra.A h) (p := AxisymmetricFields.profilePoint t x) ht).differentiableAt (by simp)
  change DifferentiableAt ℝ (streamFactor a h C d) (AxisymmetricFields.profilePoint t x) at hH
  change DifferentiableAt ℝ (swirlPotential a h C d) (AxisymmetricFields.profilePoint t x) at hK
  rw [baseVelocity, AxisymmetricFields.velocity_two _ _ _ _ hH hK]
  exact (partialS_radial_mul hH).symm.trans (partialS_integratedStream ha hh hh1 hd C ht)
end CoefficientIdentification
end NavierStokes.SlowBorelBase
end
end

-- REPLAY NavierStokes.SlowBorelBase.partialS_integratedStream 1167 1208
run_cmd IO.println "BLOCK NavierStokes.SlowBorelBase.partialS_integratedStream"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowBorelBase
open Set Filter Function
open scoped Topology ContDiff BigOperators
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
section PhysicalCoordinates
end PhysicalCoordinates
section PhysicalProfiles
end PhysicalProfiles
section PoweredTails
end PoweredTails
section LinearMaps
variable {W : Type} [NormedAddCommGroup W] [NormedSpace ℝ W]
end LinearMaps
section BaseFields
end BaseFields
section CoefficientIdentification
#count_heartbeats in
theorem partialS_integratedStream_S {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) {d : Coefficients} (hd : SmoothCoefficients d)
    (C : ℝ) {p : Chart} (hp : p.1 < 1) :
    AxisymmetricFields.partialS (integratedStream a h C d) p =
      physicalProfile a h (-CoordinateAlgebra.A h) d.axial p := by
  have he : integratedStream a h C d =ᶠ[𝓝 p]
      physicalProfile a h (1 - CoordinateAlgebra.A h)
        (fun j => ProfileHistories.primitive (d.axial j)) := by
    filter_upwards [continuousAt_fst.eventually (Iio_mem_nhds hp)] with y hy
    exact integratedStream_eq_primitive ha hh hh1 C d hy
  change fderiv ℝ (integratedStream a h C d) p (0, (1, 0)) = _
  rw [he.fderiv_eq]
  change AxisymmetricFields.partialS
    (physicalProfile a h (1 - CoordinateAlgebra.A h)
      (fun j => ProfileHistories.primitive (d.axial j))) p = _
  rw [partialS_physicalProfile ha hh hh1 (fun j => primitive_smooth (hd.axial j)) _ hp]
  simp_rw [partialX_primitive (hd.axial _)]
  rw [show 1 - CoordinateAlgebra.A h - 1 = -CoordinateAlgebra.A h by ring]
end CoefficientIdentification
end NavierStokes.SlowBorelBase
end
end

-- REPLAY NavierStokes.SlowExpansionResidual.transport_finiteProfile 1212 1254
run_cmd IO.println "BLOCK NavierStokes.SlowExpansionResidual.transport_finiteProfile"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SlowExpansionResidual
open AxisymmetricFields
open SimilarityProfile (InnerProfile InnerPoint pullback partialX T Z)
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem transport_finiteProfile_S {h e : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    (N : ℕ) (α m : ℝ) (v u f source : ℕ → InnerProfile) {p : ProfilePoint}
    (hp : p.1 < 1) (hs : 0 < p.2.1)
    (hf : ∀ n ≤ N, ContDiffAt ℝ 2 (f n) (SimilarityProfile.inner h p)) :
    transportResidual α m (finiteProfile N h 0 v)
      (finiteProfile N h (-CoordinateAlgebra.A h) u) (finiteProfile N h e f)
      (finiteProfile N h (e - 1) source) p =
    finiteSeries N (SimilarityProfile.q h p) h (e - 1)
      (fun n => transportCoefficient h e α m v u f source n (SimilarityProfile.inner h p)) +
    transportTail N (SimilarityProfile.q h p) h e α v u f (SimilarityProfile.inner h p) := by
  have hq := SimilarityProfile.q_pos hh hh1 hp
  have hX : (SimilarityProfile.inner h p).1 ≠ 0 := by
    change p.2.1 / SimilarityProfile.q h p ≠ 0
    exact div_ne_zero hs.ne' hq.ne'
  have hd : ∀ n ≤ N, DifferentiableAt ℝ (f n) (SimilarityProfile.inner h p) :=
    fun n hn => (hf n hn).differentiableAt (by norm_num)
  unfold transportResidual
  rw [partialT_finiteProfile hh hh1 N f hp hd, partialS_finiteProfile hh hh1 N f hp hd,
    partialZ_finiteProfile hh hh1 N f hp hd, partialSS_finiteProfile hh hh1 N f hp hf,
    partialZZ_finiteProfile hh hh1 N f hp hf]
  simp_rw [finiteProfile_value]
  rw [← q_mul_X hh hh1 hp]
  have hcalc := transport_series_identity hq hX N h e α m
    (fun n => v n (SimilarityProfile.inner h p)) (fun n => u n (SimilarityProfile.inner h p))
    (fun n => f n (SimilarityProfile.inner h p))
    (fun n => T h (e + slowOrder h n) (f n) (SimilarityProfile.inner h p))
    (fun n => partialX (f n) (SimilarityProfile.inner h p))
    (fun n => partialX (partialX (f n)) (SimilarityProfile.inner h p))
    (fun n => Z h (e + slowOrder h n) (f n) (SimilarityProfile.inner h p))
    (fun n => Z2 h (e + slowOrder h n) (f n) (SimilarityProfile.inner h p))
    (fun n => source n (SimilarityProfile.inner h p))
  simpa only [transportCoefficient, transportTail, add_sub_assoc] using hcalc
end NavierStokes.SlowExpansionResidual
end
end

-- REPLAY NavierStokes.SlowResidualMatching.normalized_axial_viscosity 1258 1297
run_cmd IO.println "BLOCK NavierStokes.SlowResidualMatching.normalized_axial_viscosity"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped BigOperators Topology ContDiff
namespace NavierStokes.SlowResidualMatching
open SimilarityProfile (InnerPoint InnerProfile PhysicalPoint PhysicalProfile
  partialX partialEta T Z pullback)
open SlowExpansionResidual
open AxisymmetricFields (radialEnergy profilePoint)
#count_heartbeats in
theorem normalized_axial_viscosity_S {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)
    {F E : InnerProfile} (hF : SlowStressSupport.Smooth (Ioo (-1) 1) F)
    (hFE : ∀ R : ℝ, 0 < R → ∀ eta ∈ Ioo (-1 : ℝ) 1, F (R, eta) = E (R ^ 2 / 2, eta))
    {eta R : ℝ} (heta : eta ∈ Ioo (-1 : ℝ) 1) (hR : 0 < R) :
    deriv (deriv (RenormalizedHeatMoment.uTheta h E (eta ^ 2) R)) eta =
      SlowStressSupport.axialOp2 h (-CoordinateAlgebra.A h) F (R, eta) := by
  obtain ⟨ht, hq, he⟩ := RenormalizedHeatMoment.normalized_coordinates hh hh1 heta
  let p : PhysicalPoint := (eta ^ 2, (R ^ 2 / 2, eta))
  have hqp : SimilarityProfile.q h p = 1 := hq
  have hep : SimilarityProfile.eta h p = eta := he
  have hip : SimilarityProfile.inner h p = radiusPoint (R, eta) := by
    ext <;> simp [SimilarityProfile.inner, SimilarityProfile.X, hqp, hep, radiusPoint, p]
  have hL : CoordinateAlgebra.L h eta ≠ 0 := by
    have hl := (SimilarityProfile.L_pos hh hh1 (p := p) ht).ne'
    rwa [hep] at hl
  have hE := inner_smoothAt_of_radial isOpen_Ioo hF hFE
    (w := radiusPoint (R, eta)) (by dsimp [radiusPoint]; positivity) heta
  have hE2 : ContDiffAt ℝ 2 E (SimilarityProfile.inner h p) := by
    rw [hip]
    exact hE.of_le (ENat.natCast_le_of_coe_top_le_withTop le_rfl 2)
  rw [axialOp2_radial_eq_Z2 isOpen_Ioo h (-CoordinateAlgebra.A h) hF hFE hR heta hL]
  have hfun : RenormalizedHeatMoment.uTheta h E (eta ^ 2) R =
      fun z => pullback h (-CoordinateAlgebra.A h) E (p.1, (p.2.1, z)) :=
    funext (RenormalizedHeatMoment.uTheta_eq_similarity_pullback h E (eta ^ 2) R)
  rw [hfun, deriv_deriv_pullback_z hh hh1 (p := p) ht hE2]
  simp only [pullback, hqp, hip, Real.one_rpow, one_mul]
end NavierStokes.SlowResidualMatching
end
end

-- REPLAY NavierStokes.TerminalHistoryBridge.Ns_after_endpoint 1301 1327
run_cmd IO.println "BLOCK NavierStokes.TerminalHistoryBridge.Ns_after_endpoint"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TerminalHistoryBridge
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open OutgoingProfile (Profile)
open HeatedOutgoing (CompensationWitness Coeff)
#count_heartbeats in
theorem Ns_after_endpoint_S (F : Profile) (XR : ℝ) (c : ℝ → Coeff)
    {p : ℝ × ℝ} (hp : F.data.core.endpoint ≤ p.1) :
    HeatSwitchCone.Ns F XR c p =
      (4*F.data.h*p.2*HeatSwitchCone.logS F XR c p -
        StressAlgebra.coordinateFactor p.2 *
        derivWithin (fun η => HeatSwitchCone.logS F XR c (p.1,η))
          HeatedOutgoing.parameterDomain p.2) / Real.exp p.1 +
      4*StressAlgebra.velocityExponent F.data.h*p.2*HeatSwitchCone.logPi F XR c p -
        StressAlgebra.coordinateFactor p.2 *
        derivWithin (fun η => HeatSwitchCone.logPi F XR c (p.1,η))
          HeatedOutgoing.parameterDomain p.2 := by
  simp only [HeatSwitchCone.Ns, OutgoingHistories.M_after_endpoint F.data F.amp p.2 hp,
    OutgoingHistories.dEta_M_after_endpoint F.data F.amp_contDiff p.2 hp,
    show F.logU p = 0 from F.logU_after p.2 hp,
    mul_zero, sub_zero, zero_div, add_zero, zero_add]
end NavierStokes.TerminalHistoryBridge
end
end

-- REPLAY NavierStokes.TerminalHistoryBridge.physicalLog_angularResidual 1331 1364
run_cmd IO.println "BLOCK NavierStokes.TerminalHistoryBridge.physicalLog_angularResidual"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TerminalHistoryBridge
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open OutgoingProfile (Profile)
open HeatedOutgoing (CompensationWitness Coeff)
open HeatSwitchCone (logE logI logS logPi)
open ProfileHistories (radialPartial parameterPartial)
#count_heartbeats in
theorem physicalLog_angularResidual_S (F : Profile) {XR C : ℝ} (w : CompensationWitness F XR C)
    {p : SimilarityProfile.PhysicalPoint} (ht : p.1 < 1) (hs : 0 < p.2.1) :
    amplitudeOperator (physicalLog F.data.h (-TerminalPressure.amplitudeExponent F.data.h)
      XR (logE F XR w.coefficients)) p =
      SimilarityProfile.q F.data.h p^(-TerminalPressure.amplitudeExponent F.data.h-1) *
        angularResidual F XR w.coefficients (logPoint XR (SimilarityProfile.inner F.data.h p)) := by
  rw [physicalLog_amplitudeOperator F.data.h_pos F.data.h_lt_half w.radius_pos
    (HeatSwitchHistoryDerivatives.logE_contDiffOn F w) ht hs]
  have hx : 0 < SimilarityProfile.X F.data.h p :=
    div_pos hs (SimilarityProfile.q_pos F.data.h_pos F.data.h_lt_half ht)
  have heta : SimilarityProfile.eta F.data.h p ∈ Ioo (-1) 1 := by
    have he := SimilarityProfile.eta_sq_lt_one F.data.h_pos F.data.h_lt_half ht
    constructor <;> nlinarith [sq_nonneg (SimilarityProfile.eta F.data.h p+1),sq_nonneg (SimilarityProfile.eta F.data.h p-1)]
  have hp : logPoint XR (SimilarityProfile.inner F.data.h p) ∈ HeatSwitchHistoryDerivatives.interiorDomain.carrier :=
    ⟨mem_univ _,heta⟩
  unfold angularResidual etaDerivative
  rw [HeatSwitchHistoryDerivatives.within_parameter_eq (HeatSwitchHistoryDerivatives.logE_contDiffOn F w) hp]
  simp only [logPoint,SimilarityProfile.inner,Real.exp_log (div_pos hx w.radius_pos),
    mul_div_cancel₀ _ w.radius_pos.ne',TerminalPressure.amplitudeExponent,StressAlgebra.velocityExponent,
    StressAlgebra.axialExponent,CoordinateAlgebra.D,neg_neg]
end NavierStokes.TerminalHistoryBridge
end
end

-- REPLAY NavierStokes.TerminalHistoryBridge.physical_forwardAxial_eq_terminal 1368 1410
run_cmd IO.println "BLOCK NavierStokes.TerminalHistoryBridge.physical_forwardAxial_eq_terminal"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TerminalHistoryBridge
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open OutgoingProfile (Profile)
open HeatedOutgoing (CompensationWitness Coeff)
open HeatSwitchCone (logE logI logS logPi)
open ProfileHistories (radialPartial parameterPartial)
#count_heartbeats in
theorem physical_forwardAxial_eq_terminal_S (F : Profile) {XR C B t r z : ℝ}
    (hF : OutgoingProfile.Specification F B) (w : CompensationWitness F XR C) (ht : t < 1) (hr : 0 < r)
    (hfull : 1/2 < Real.log (SimilarityProfile.X F.data.h (TerminalStress.radiusPoint t r z) /
      OutgoingDilation.switchRadius F XR)+1/5) :
    SimilarityProfile.q F.data.h (TerminalStress.radiusPoint t r z)^(-TerminalPressure.amplitudeExponent F.data.h-1/2) *
      forwardAxial F XR w.coefficients (logPoint XR (SimilarityProfile.inner F.data.h (TerminalStress.radiusPoint t r z))) =
        TerminalPressure.axialBackwardStress (normalization F XR) F.data.h
          (TerminalPressure.outgoingTaper F.data (shift F XR)) t z r := by
  let q := SimilarityProfile.q F.data.h (t,(0,z))
  let η := SimilarityProfile.eta F.data.h (t,(0,z))
  have hq : 0 < q := SimilarityProfile.q_pos F.data.h_pos F.data.h_lt_half ht
  have hx : 0 < r^2/2/q := div_pos (by positivity) hq
  have hy : F.data.core.endpoint ≤ radiusClock q XR r :=
    (terminalStart_after_endpoint F).le.trans (full_switch_late F w.radius_pos hx hfull.le)
  have hw := axialWeight_eq_forward F w (p := (radiusClock q XR r,η)) hy
  have he := physicalAxialWeight_eq_tail F hF w ht (by positivity : 0 < r^2/2) hfull
  change q^(-TerminalPressure.amplitudeExponent F.data.h)*axialWeight F XR w.coefficients (radiusClock q XR r,η) = _ at he
  unfold TerminalPressure.axialBackwardStress
  change _ = (∫ u in Ioi (r^2/2), SimilarityProfile.partialZ
    (TerminalPressure.outgoingPressure (normalization F XR) F.data (shift F XR)) (t,(u,z)))/r
  rw [← he,hw]
  change q^(-TerminalPressure.amplitudeExponent F.data.h-1/2)*
    forwardAxial F XR w.coefficients (radiusClock q XR r,η) =
    q^(-TerminalPressure.amplitudeExponent F.data.h)*
      (Real.sqrt (2*XR*Real.exp (radiusClock q XR r))*forwardAxial F XR w.coefficients (radiusClock q XR r,η))/r
  rw [show 2*XR*Real.exp (radiusClock q XR r)=2*(XR*Real.exp (radiusClock q XR r)) by ring,
    radiusClock,exp_regularClock hq w.radius_pos (by positivity : 0 < r^2/2),sqrt_radius_quotient hq hr,
    Real.rpow_sub hq,← Real.sqrt_eq_rpow]
  field_simp [hr.ne',(Real.sqrt_pos.mpr hq).ne']
end NavierStokes.TerminalHistoryBridge
end
end

-- REPLAY NavierStokes.TerminalHistoryBridge.physical_forwardTheta_eq_terminal 1414 1454
run_cmd IO.println "BLOCK NavierStokes.TerminalHistoryBridge.physical_forwardTheta_eq_terminal"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TerminalHistoryBridge
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open OutgoingProfile (Profile)
open HeatedOutgoing (CompensationWitness Coeff)
open HeatSwitchCone (logE logI logS logPi)
open ProfileHistories (radialPartial parameterPartial)
#count_heartbeats in
theorem physical_forwardTheta_eq_terminal_S (F : Profile) {XR C t r z : ℝ}
    (w : CompensationWitness F XR C) (ht : t < 1) (hr : 0 < r)
    (hfull : 1/2 < Real.log (SimilarityProfile.X F.data.h (TerminalStress.radiusPoint t r z) /
      OutgoingDilation.switchRadius F XR)+1/5) :
    SimilarityProfile.q F.data.h (TerminalStress.radiusPoint t r z)^(-TerminalPressure.amplitudeExponent F.data.h-1/2) *
      forwardTheta F XR w.coefficients (logPoint XR (SimilarityProfile.inner F.data.h (TerminalStress.radiusPoint t r z))) =
        TerminalStress.terminalStress (normalization F XR) F.data.h
          (TerminalPressure.outgoingTaper F.data (shift F XR)) t z r := by
  let q := SimilarityProfile.q F.data.h (t,(0,z))
  let η := SimilarityProfile.eta F.data.h (t,(0,z))
  have hq : 0 < q := SimilarityProfile.q_pos F.data.h_pos F.data.h_lt_half ht
  have heta : η ∈ Ioo (-1) 1 := eta_mem_interior F.data.h_pos F.data.h_lt_half ht
  have hx : 0 < r^2/2/q := div_pos (by positivity) hq
  have hy : F.data.core.endpoint ≤ radiusClock q XR r :=
    (terminalStart_after_endpoint F).le.trans (full_switch_late F w.radius_pos hx hfull.le)
  have hw := thetaWeight_eq_forward F w (p := (radiusClock q XR r,η)) heta hy
  have he := physicalThetaWeight_eq_tail F w ht hr hfull
  change q^(-F.data.h)*thetaWeight F XR w.coefficients (radiusClock q XR r,η) = _ at he
  unfold TerminalStress.terminalStress TerminalStress.backwardStress
  rw [← he,hw]
  change q^(-TerminalPressure.amplitudeExponent F.data.h-1/2)*
    forwardTheta F XR w.coefficients (radiusClock q XR r,η) =
    q^(-F.data.h)*(2*(XR*Real.exp (radiusClock q XR r))*forwardTheta F XR w.coefficients (radiusClock q XR r,η))/r^2
  rw [show -TerminalPressure.amplitudeExponent F.data.h-1/2=-F.data.h-1 by
    unfold TerminalPressure.amplitudeExponent
    ring,Real.rpow_sub_one hq.ne',radiusClock,exp_regularClock hq w.radius_pos (by positivity : 0 < r^2/2)]
  field_simp [hq.ne',hr.ne']
end NavierStokes.TerminalHistoryBridge
end
end

-- REPLAY NavierStokes.TerminalHistoryBridge.terminal_axialResidual 1458 1482
run_cmd IO.println "BLOCK NavierStokes.TerminalHistoryBridge.terminal_axialResidual"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.TerminalHistoryBridge
open Set Filter Function MeasureTheory
open scoped Topology ContDiff
open OutgoingProfile (Profile)
open HeatedOutgoing (CompensationWitness Coeff)
open HeatSwitchCone (logE logI logS logPi)
open ProfileHistories (radialPartial parameterPartial)
#count_heartbeats in
theorem terminal_axialResidual_S (F : Profile) {XR C : ℝ} (w : CompensationWitness F XR C)
    {p : SimilarityProfile.PhysicalPoint} (ht : p.1 < 1) (hs : 0 < p.2.1)
    (hfull : 1/2 < Real.log (SimilarityProfile.X F.data.h p /
      OutgoingDilation.switchRadius F XR) + 1/5) :
    SimilarityProfile.partialZ (TerminalPressure.outgoingPressure (normalization F XR) F.data (shift F XR)) p =
      SimilarityProfile.q F.data.h p^(-TerminalPressure.amplitudeExponent F.data.h-1) *
        axialResidual F XR w.coefficients (logPoint XR (SimilarityProfile.inner F.data.h p)) := by
  have he := (terminal_germs F w ht hs hfull).2
  unfold SimilarityProfile.partialZ
  rw [← he.fderiv_eq]
  exact physicalLog_axialResidual F w ht hs
end NavierStokes.TerminalHistoryBridge
end
end

-- REPLAY NavierStokes.TerminalPressure.heatAmplitude_annulus_lower 1486 1519
run_cmd IO.println "BLOCK NavierStokes.TerminalPressure.heatAmplitude_annulus_lower"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.TerminalPressure
#count_heartbeats in
theorem heatAmplitude_annulus_lower_S {C h t r R Λ : ℝ}
    (hC : 0 < C) (hh : 0 < h) (ht : t < 1) (hr : 0 < r) (hrR : r ≤ R)
    (hΛ : 1 ≤ Λ) (hRΛ : R ^ 2 ≤ Λ * r ^ 2) :
    Λ ^ (-amplitudeExponent h) * TerminalStress.heatAmplitude C (1 + h) t r ≤
      TerminalStress.heatAmplitude C (1 + h) t R := by
  have hR : 0 < R := hr.trans_le hrR
  have hτ : 0 < 1 - t := sub_pos.mpr ht
  have ha : 0 < r ^ 2 / 2 := by positivity
  have hb : 0 < R ^ 2 / 2 := by positivity
  have hab : r ^ 2 / 2 ≤ R ^ 2 / 2 := by nlinarith
  have hΛp : 0 < Λ := zero_lt_one.trans_le hΛ
  have hpow : Λ ^ (-amplitudeExponent h) * (r ^ 2 / 2) ^ (-amplitudeExponent h) ≤
      (R ^ 2 / 2) ^ (-amplitudeExponent h) := by
    rw [← Real.mul_rpow hΛp.le ha.le]
    exact Real.rpow_le_rpow_of_nonpos hb (by nlinarith) (by dsimp [amplitudeExponent]; linarith)
  have harg : 2 * (1 - t) / (R ^ 2 / 2) ≤ 2 * (1 - t) / (r ^ 2 / 2) :=
    div_le_div_of_nonneg_left (by positivity) ha hab
  have hH := heatProfile_antitoneOn hh (div_pos (by positivity) hb) (div_pos (by positivity) ha) harg
  have hHa := (RadialHeatProfile.profile_pos (a := 1 + h) (by linarith)
    (show 0 ≤ 2 * (1 - t) / (r ^ 2 / 2) by positivity)).le
  have he := mul_le_mul hpow hH hHa (Real.rpow_nonneg hb.le _)
  have heC := mul_le_mul_of_nonneg_left he hC.le
  simpa only [TerminalStress.heatAmplitude, RadialHeatProfile.radialProfile_source_formula,
    amplitudeExponent, mul_assoc, mul_left_comm, mul_comm] using heC
end NavierStokes.TerminalPressure
end
end

-- REPLAY NavierStokes.TerminalPressure.physicalEdit_eq_released_carrier 1523 1558
run_cmd IO.println "BLOCK NavierStokes.TerminalPressure.physicalEdit_eq_released_carrier"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.TerminalPressure
#count_heartbeats in
theorem physicalEdit_eq_released_carrier_S (d : OutgoingTail.TailData) {K : ℝ} (hK : 0 < K)
    {p : SimilarityProfile.PhysicalPoint} (ht : p.1 < 1) (hs : 0 < p.2.1)
    (hfull : 1 / 2 ≤ Real.log (SimilarityProfile.X d.h p / K) + 1 / 5) :
    SimilarityProfile.q d.h p ^ (-amplitudeExponent d.h) *
      ParametricHeatTail.physicalEdit d K (SimilarityProfile.eta d.h p) (SimilarityProfile.X d.h p) =
        TerminalStress.physicalHeat (releasedNormalization d K) (1 + d.h) p *
          outgoingTaper d (Real.log K - 1 / 5) (Real.log (SimilarityProfile.X d.h p)) := by
  have hq := SimilarityProfile.q_pos d.h_pos d.h_lt_half ht
  have hτ : 1 - p.1 = SimilarityProfile.q d.h p * (1 - SimilarityProfile.eta d.h p ^ 2) :=
    SimilarityCoordinates.tau_coordinate_identity (by linarith [d.h_pos])
      (by linarith [d.h_lt_half]) (p := (1 - p.1, p.2.2)) (sub_pos.mpr ht)
  have hν : ParametricHeatTail.diffusion (SimilarityProfile.eta d.h p) =
      (1 - p.1) / SimilarityProfile.q d.h p := by
    rw [hτ]
    unfold ParametricHeatTail.diffusion
    field_simp [hq.ne']
  have he := ParametricHeatTail.physicalEdit_heat_carrier d hK hq hs hν hfull
  have hlog : Real.log (SimilarityProfile.X d.h p / K) + 1 / 5 =
      Real.log (SimilarityProfile.X d.h p) - (Real.log K - 1 / 5) := by
    unfold SimilarityProfile.X
    rw [Real.log_div (div_pos hs hq).ne' hK.ne']
    ring
  simp only [SimilarityProfile.X] at hlog
  rw [hlog] at he
  simpa only [SimilarityProfile.X, TerminalStress.physicalHeat, releasedNormalization,
    outgoingTaper, HeatTailEdit.exponent, amplitudeExponent] using he
end NavierStokes.TerminalPressure
end
end

-- REPLAY NavierStokes.TerminalPressure.swirlCoefficient_sq 1562 1592
run_cmd IO.println "BLOCK NavierStokes.TerminalPressure.swirlCoefficient_sq"
section
set_option linter.all false
noncomputable section
open Set Filter MeasureTheory
open scoped Topology ContDiff
namespace NavierStokes.TerminalPressure
#count_heartbeats in
theorem swirlCoefficient_sq_S (C h : ℝ) (f : ℝ → ℝ) {p : SimilarityProfile.PhysicalPoint}
    (hs : 0 < p.2.1) :
    TerminalStress.swirlCoefficient C h f p ^ 2 =
      (C ^ 2 / 2) * p.2.1 ^ (-2 * amplitudeExponent h - 1) *
        RadialHeatProfile.profile (1 + h) (2 * (1 - p.1) / p.2.1) ^ 2 *
        f (Real.log (SimilarityProfile.X h p)) ^ 2 := by
  have hexp : RadialHeatProfile.spatialExponent (1 + h) = -amplitudeExponent h := by
    unfold RadialHeatProfile.spatialExponent amplitudeExponent
    ring
  have hp : (p.2.1 ^ (-amplitudeExponent h)) ^ (2 : ℕ) = p.2.1 ^ (-2 * amplitudeExponent h) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hs.le]
    congr 1
    ring
  have hpow : p.2.1 ^ (-2 * amplitudeExponent h - 1) =
      p.2.1 ^ (-2 * amplitudeExponent h) / p.2.1 := by
    rw [Real.rpow_sub hs, Real.rpow_one]
  unfold TerminalStress.swirlCoefficient TerminalStress.physicalHeat RadialHeatProfile.spatialProfile
    TerminalStress.flattening
  rw [hexp, div_pow, mul_pow, mul_pow, mul_pow, hp,
    Real.sq_sqrt (by positivity : 0 ≤ 2 * p.2.1), hpow]
  field_simp [hs.ne']
end NavierStokes.TerminalPressure
end
end

