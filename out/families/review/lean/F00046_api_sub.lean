import Tool
import F46
import NavierStokes.ActualStageEstimates
import NavierStokes.BaseContextAssembly
import NavierStokes.BaseStressClasses
import NavierStokes.CorrectionInitialization
import NavierStokes.CorrectionStep
import NavierStokes.CurlClassBounds
import NavierStokes.GaugeAliasDecay
import NavierStokes.GaugeDebtIncrement
import NavierStokes.HarmonicWaveInteraction
import NavierStokes.LocalSignedRequest
import NavierStokes.MeanIncrementBounds
import NavierStokes.MeanMomentBounds
import NavierStokes.MovingMomentBounds
import NavierStokes.PhysicalMeanDomain
import NavierStokes.SignedStressPrimitive
import NavierStokes.VariableGaugeMean
import NavierStokes.WaveInteractionBounds
import NavierStokes.WeightedClasses
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualStageEstimates.RunData.rank_class 25 44
run_cmd IO.println "BLOCK NavierStokes.ActualStageEstimates.RunData.rank_class"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualStageEstimates
open Set Function Filter ProblemStatement CorrectionState CorrectionStep
open CorrectionInitialization CorrectionInitialization.ActualPrimary
open ActualPhysicalStageBounds
open scoped ContDiff Topology BigOperators
#count_heartbeats in
theorem RunData.rank_class_R {B N0 : ℕ} (R : RunData B N0) (j : ℕ) :
    WeightedClasses.UnweightedClass ActualInitialization.slowStrip
      (1 + ActualIterationLedger.sigma j - 2 * ChartScales.kappa)
      (CorrectionState.debt (commonContext B)
        (ActualIntermediateDebtBounds.postTemporal (ActualCyclePreservation.state B N0 j))) :=
  ActualIntermediateDebtBounds.afterTemporal_debt_from_stepData
    (ActualCyclePreservation.staticData B) (R.invariant j) (ActualIterationLedger.sigma_admissible j)
    (R.particular j) (R.step j)
end NavierStokes.ActualStageEstimates
end
end

-- REPLAY NavierStokes.BaseContextAssembly.envelope_pullback 48 80
run_cmd IO.println "BLOCK NavierStokes.BaseContextAssembly.envelope_pullback"
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
#count_heartbeats in
theorem envelope_pullback_R {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : StripData Point) {D : PhaseJetBounds.Domain ℕ Slow} {f : ℕ → Slow → E}
    {w : ℕ → ℝ} (hf : PrimaryPulseBounds.EnvelopeJets (BaseChartJets.unitScale D) (fun n _ => w n) f)
    (hmap : ∀ n, MapsTo slowCoordinates s.domain (D.carrier n)) {alpha : ℝ}
    (hw : ∀ n, w n = s.epsilon n ^ alpha) :
    UnweightedClass s alpha (fun n x => f n (slowCoordinates x)) := by
  refine ⟨fun _ _ _ => zero_le_one, fun n => (hf.smooth n).comp slowCoordinates.contDiff.contDiffOn (hmap n), ?_⟩
  intro m
  obtain ⟨C, hC, hb⟩ := BaseChartJets.envelope_unit_bound hf m
  refine ⟨C, zero_le_one.trans hC, 0, fun n x hx j hj => ?_⟩
  have hjet := PhaseJetBounds.norm_jet_comp_linear (D.isOpen n) (hf.smooth n)
    slowCoordinates (hmap n hx) j
  calc
    _ ≤ ‖iteratedFDeriv ℝ j (f n) (slowCoordinates x)‖ * ‖slowCoordinates‖ ^ j := hjet
    _ ≤ (C * w n) * 1 := mul_le_mul (hb n _ (hmap n hx) j hj)
      (pow_le_one₀ (norm_nonneg _) slowCoordinates_norm_le) (by positivity)
      (mul_nonneg (zero_le_one.trans hC) (hf.nonneg n _ (hmap n hx)))
    _ = _ := by simp only [majorant, pow_zero, mul_one, hw]
end NavierStokes.BaseContextAssembly
end
end

-- REPLAY NavierStokes.BaseContextAssembly.unweighted_polynomial_pullback 84 114
run_cmd IO.println "BLOCK NavierStokes.BaseContextAssembly.unweighted_polynomial_pullback"
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
#count_heartbeats in
theorem unweighted_polynomial_pullback_R {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : StripData Point) {D : PhaseJetBounds.Domain ℕ Slow} {f : ℕ → Slow → E}
    (hf : PhaseJetBounds.PolynomialJets (BaseChartJets.unitScale D) f)
    (hmap : ∀ n, MapsTo slowCoordinates s.domain (D.carrier n)) :
    UnweightedClass s 0 (fun n x => f n (slowCoordinates x)) := by
  refine ⟨fun _ _ _ => zero_le_one, fun n => (hf.smooth n).comp slowCoordinates.contDiff.contDiffOn (hmap n), ?_⟩
  intro m
  obtain ⟨C, hC, hb⟩ := BaseChartJets.polynomial_unit_bound hf m
  refine ⟨C, zero_le_one.trans hC, 0, fun n x hx j hj => ?_⟩
  have hjet := PhaseJetBounds.norm_jet_comp_linear (D.isOpen n) (hf.smooth n)
    slowCoordinates (hmap n hx) j
  calc
    _ ≤ ‖iteratedFDeriv ℝ j (f n) (slowCoordinates x)‖ * ‖slowCoordinates‖ ^ j := hjet
    _ ≤ C * 1 := mul_le_mul (hb n j hj _ (hmap n hx))
      (pow_le_one₀ (norm_nonneg _) slowCoordinates_norm_le) (by positivity) (zero_le_one.trans hC)
    _ = _ := by simp only [majorant, Real.rpow_zero, pow_zero, mul_one]
end NavierStokes.BaseContextAssembly
end
end

-- REPLAY NavierStokes.BaseStressClasses.correction_composed_meanClass 118 205
run_cmd IO.println "BLOCK NavierStokes.BaseStressClasses.correction_composed_meanClass"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseStressClasses
open Set Filter Function WeightedClasses
open scoped ContDiff Topology BigOperators
section Composition
variable {D E V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end Composition
section Rescaling
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Rescaling
section NativeGeometry
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
end NativeGeometry
section ActualStress
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
#count_heartbeats in
theorem correction_composed_meanClass_R (upper : ℝ) (B : ℕ)
    (U : LocalSignedRequest.SlowRegion (2*F.data.h)) :
    MeanClass (BaseContextAssembly.nativeStrip W U) 1
      (fun n x => correction H v upper B
        (SlowBorelBase.scaleMap (ChartScales.Q n) (coordinates (F := F) x))) := by
  let s := BaseContextAssembly.nativeStrip W U
  have hs n : ContDiffOn ℝ ∞
      (correction H v upper B ∘ SlowBorelBase.scaleMap (ChartScales.Q n)) BaseChartJets.sumRegion :=
    (correction_smooth H v upper B).comp (SlowBorelBase.scaleMap (ChartScales.Q n)).contDiff.contDiffOn
      (fun y hy => ⟨mul_pos (ChartScales.Q_pos n) hy.1, hy.2⟩)
  have hmap (n : ℕ) : MapsTo (fun x => coordinates (F := F) x) s.domain BaseChartJets.sumRegion := by
    intro x hx
    have hq := coordinates_range W U hx
    have hw := BaseContextAssembly.nativeStrip_active W U hx
    exact ⟨(div_pos U.qlo_pos (by norm_num)).trans hq.1,
      (NominalConeAssembly.activeLeft_pos W).trans hw.1.1, mem_univ _⟩
  apply class_comp_of_outer_jets (s := s) BaseChartJets.sumRegion_open hs
    (coordinates_unweighted W U) hmap (fun _ x hx => s.zeta_nonneg x hx)
  intro j
  obtain ⟨D, hD, N, hb⟩ := correction_weighted_jets H v upper B j
  let K : ℝ := max 1 (1/(U.qlo/2))
  let R : ℝ := BaseContextAssembly.geometryUpper U
  have hR : 0 < R := BaseContextAssembly.geometryUpper_pos U
  have hK : 1 ≤ K := le_max_left _ _
  refine ⟨D * R^F.data.h * K^j, by positivity, N, fun n x hx => ?_⟩
  have hqp : 0 < (coordinates (F := F) x).1 := (hmap n hx).1
  have hxpos : 0 < (coordinates (F := F) x).2.1 := (hmap n hx).2.1
  have hqr := coordinates_range W U hx
  have hinv : 1 / (coordinates (F := F) x).1 ≤ K :=
    (one_div_le_one_div_of_le (div_pos U.qlo_pos (by norm_num)) hqr.1.le).trans (le_max_right _ _)
  have hscaled := scaled_jet_from_blown (correction_smooth H v upper B)
    (ChartScales.Q_pos n) hqp hxpos hK hinv j
  have hbound := hb (ChartScales.Q n * (coordinates (F := F) x).1)
    (mul_pos (ChartScales.Q_pos n) hqp) _ (BaseContextAssembly.nativeStrip_active W U hx)
  have hzeta : FinalSlowBase.weight W (coordinates (F := F) x).2 = s.zeta x :=
    (BaseContextAssembly.nativeStrip_weight W U hx).symm
  have hpos : 0 < FinalSlowBase.edgeDistance W (coordinates (F := F) x).2 :=
    (s.delta_pos x hx).trans_le (native_edgeDistance_le W U hx)
  have hd := pow_le_pow_left₀ (inv_nonneg.mpr hpos.le)
    (inverse_edgeDistance_le_growth W U n hx) N
  have hrpow : (ChartScales.Q n * (coordinates (F := F) x).1)^F.data.h ≤
      s.epsilon n * R^F.data.h := by
    rw [Real.mul_rpow (ChartScales.Q_pos n).le hqp.le]
    exact mul_le_mul_of_nonneg_left (Real.rpow_le_rpow hqp.le hqr.2.le F.data.h_pos.le)
      (Real.rpow_nonneg (ChartScales.Q_pos n).le _)
  calc
    _ ≤ ‖SlowBorelBase.blownJet j (correction H v upper B)
        (ChartScales.Q n * (coordinates (F := F) x).1, (coordinates (F := F) x).2)‖ * K^j := hscaled
    _ ≤ (D * (ChartScales.Q n * (coordinates (F := F) x).1)^F.data.h *
        FinalSlowBase.weight W (coordinates (F := F) x).2 *
        (FinalSlowBase.edgeDistance W (coordinates (F := F) x).2)⁻¹^N) * K^j :=
      mul_le_mul_of_nonneg_right hbound (pow_nonneg (zero_le_one.trans hK) j)
    _ = (D * (ChartScales.Q n * (coordinates (F := F) x).1)^F.data.h * s.zeta x *
        (FinalSlowBase.edgeDistance W (coordinates (F := F) x).2)⁻¹^N) * K^j := by rw [hzeta]
    _ ≤ (D * (s.epsilon n * R^F.data.h) * s.zeta x * s.growth n x^N) * K^j := by
      apply mul_le_mul_of_nonneg_right _ (pow_nonneg (zero_le_one.trans hK) j)
      exact mul_le_mul
        (mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hrpow hD.le) (s.zeta_nonneg x hx))
        hd (pow_nonneg (inv_nonneg.mpr hpos.le) N)
        (mul_nonneg (mul_nonneg hD.le (mul_nonneg (s.epsilon_pos n).le
          (Real.rpow_nonneg hR.le _))) (s.zeta_nonneg x hx))
    _ = _ := by simp only [majorant, Real.rpow_one]; ring
end ActualStress
end NavierStokes.BaseStressClasses
end
end

-- REPLAY NavierStokes.BaseStressClasses.higherStress_meanClass 209 247
run_cmd IO.println "BLOCK NavierStokes.BaseStressClasses.higherStress_meanClass"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseStressClasses
open Set Filter Function WeightedClasses
open scoped ContDiff Topology BigOperators
section Composition
variable {D E V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end Composition
section Rescaling
variable {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end Rescaling
section NativeGeometry
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
end NativeGeometry
section ActualStress
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld)
#count_heartbeats in
theorem higherStress_meanClass_R (upper : ℝ) (B : ℕ)
    (U : LocalSignedRequest.SlowRegion (2*F.data.h)) :
    MeanClass (BaseContextAssembly.nativeStrip W U) 2
      (fun n x => BaseContextAssembly.virtualStress H v upper B n x -
        BaseContextAssembly.leadingVirtualStress H v n x) := by
  apply CurlClassBounds.class_congr (raw_higher_meanClass H v upper B U)
  intro n x hx
  dsimp only
  rw [BaseContextAssembly.virtualStress_normalized H v upper B n
      (BaseContextAssembly.nativeStrip_time W U hx) (BaseContextAssembly.nativeStrip_radius W U hx),
    BaseContextAssembly.leadingVirtualStress_eq H v n
      (BaseContextAssembly.nativeStrip_time W U hx) (BaseContextAssembly.nativeStrip_radius W U hx)]
  exact smul_sub _ _ _
end ActualStress
end NavierStokes.BaseStressClasses
end
end

-- REPLAY NavierStokes.CorrectionInitialization.MovingInitialization.PrimaryMeanData.temporal_debt_bounds 251 486
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.MovingInitialization.PrimaryMeanData.temporal_debt_bounds"
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
#count_heartbeats in
theorem temporal_debt_bounds_R :
    UnweightedClass slowSt (1 - ChartScales.kappa)
      (debt c (temporalStageState g h index axial c (reconstructState g c u))) := by
  let p := reconstructState g c u
  let v := temporalStageState g h index axial c p
  have hmean : v.mean = temporalIncrementState g h index axial c p := by
    change updated u.mean _ = _
    rw [d.mean_zero]
    simp only [updated, zero_add]
  have hcov : v.covariance = u.covariance := CorrectionStep.gaugeTemporalStage_covariance g h index axial c p
  obtain ⟨hgr, _, _, _, hcum⟩ := zeroMean_reconstructed_bounds U g ha d.exponent_pos
    hcL hcR ε L hε hεone hL d.gauge_length c u d.operators d.localOperators d.mean_zero
    d.covariance d.covariance_smooth d.covariance_support d.theta d.axial
  have hgv := temporal_gr_mem g h index axial c p d.operators d.base hcum.velocity t.increment
    (by norm_num [ChartScales.kappa]) (by norm_num [ChartScales.kappa])
    (fun i j => (d.covariance i j).smooth) hgr
  apply RankStateBounds.debtClass_of_components
  exact state_debt_mem U ha g.radial.inner_lt_outer hcL hcR ε L hε hεone hL c v
    (by norm_num [ChartScales.kappa]) d.operators d.base
    (by simpa only [hmean] using t.increment) hgv d.localOperators d.base_smooth
    (by simpa only [hmean] using t.increment_smooth)
    (by simpa only [hmean] using t.increment_support)
    (fun i j => by rw [hcov]; exact (d.covariance i j).mono_exponent (by norm_num [ChartScales.kappa]))
    (by simpa only [hcov] using d.covariance_smooth)
    (by simpa only [hcov] using d.covariance_support)
end PrimaryMeanData
end RankComposition
end MovingInitialization
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.CorrectionInitialization.zeroMean_theta_mem 490 580
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.zeroMean_theta_mem"
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
#count_heartbeats in
theorem zeroMean_theta_mem_R {s : StripData D} {κ : ℝ} (c : Context D) (u : State D)
    (ho : OperatorBounds s c.operators κ) (hm : u.mean = ⟨0, 0, 0⟩)
    (hW : ∀ i j, MeanClass s 1 (u.covariance i j))
    (hT : MeanClass s 1 c.virtualTheta) : MeanClass s (1 - κ) (u.thetaResidual c) := by
  rw [zeroMean_theta c u hm]
  exact Class.sub ((ho.radialDiv (hW 0 1) 2).add
    ((ho.dz (hW 2 1)).mono_exponent (by linarith [ho.kappa_nonneg])))
    (ho.radialDiv hT 2)
end ZeroMean
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.CorrectionStep.gaugeWaveStage_pressure_from_covariance 584 1040
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.gaugeWaveStage_pressure_from_covariance"
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
end ParticularParameters
end ParticularLinear
section SupportedWaveGain
open Set Filter WeightedClasses MeanIncrementBounds CorrectionState
open scoped ContDiff Topology
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end SupportedWaveGain
section ActualRecurrence
open Set CorrectionState WeightedClasses
open scoped BigOperators
namespace CycleParameters
variable {ι : Type} (p : CycleParameters ι) (v : CycleCoefficients ι)
    (c : Context CyclePoint) (u : State CyclePoint)
end CycleParameters
namespace CycleState
variable {ι : Type}
end CycleState
end ActualRecurrence
section PeriodizedCurl
open Set Filter WeightedClasses HarmonicCalculus CorrectionState
open scoped ContDiff Topology InnerProductSpace
variable {D I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace PeriodizedSignedParameters
variable {p : PeriodizedSignedParameters D I} {s : StripData D}
  {P : ℕ → D → ℝ} {κ β : ℝ} (h : p.NativeControl s P κ)
  (request : ℕ → D × ℝ → SignedWaveUpdate.Vec2)
variable {h request}
end PeriodizedSignedParameters
open CommonCoverSolve TorusInverse ParticularWaveAssembly ParticularWaveBounds LinearWaveBounds
namespace ParticularParameters
variable {Q : Type} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
  {p : ParticularParameters Q} {s : StripData (Q × Plane)}
  {c : Context (Q × Plane)} {u : State (Q × Plane)} {b : HarmonicBlock (Q × Plane)}
  {G A : HarmonicResidual.BlockCoefficients (Q × Plane)} {j : ℤ}
  {W : ℕ → (Q × ℝ) × Plane → ℝ} {α κ : ℝ}
  (h : p.NativeControl s c u b G A j W α κ)
variable {h}
variable (p : ParticularParameters Q) (s : StripData (Q × Plane))
  (c : Context (Q × Plane)) (u : State (Q × Plane)) (b : HarmonicBlock (Q × Plane))
  (G A : HarmonicResidual.BlockCoefficients (Q × Plane)) (N : ℕ)
  (C : ∀ j ∈ modes N, p.NativeControl s c u b G A j W α κ)
  (dyn : ∀ j hj, NativeDynamics (C j hj))
end ParticularParameters
end PeriodizedCurl
section UniformCycleGains
open Set Filter WeightedClasses MeanIncrementBounds CorrectionState
open LabelSumBounds UniformHarmonicInteraction
open scoped ContDiff Topology
variable {D ι : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end UniformCycleGains
section ConstructedWaveGains
open Set Filter WeightedClasses MeanIncrementBounds CorrectionState
open HarmonicCalculus ParticularWaveAssembly ParticularWaveBounds
open scoped ContDiff Topology InnerProductSpace
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
namespace ParticularParameters
open TorusInverse
variable {Q : Type} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
end ParticularParameters
namespace PeriodizedSignedParameters
variable {I : Type} {p : PeriodizedSignedParameters D I} {s : StripData D}
  {P : ℕ → D → ℝ} {B κ : ℝ} {h : p.NativeControl s P κ}
  {request : ℕ → D × ℝ → SignedWaveUpdate.Vec2}
end PeriodizedSignedParameters
end ConstructedWaveGains
section ConstructedWaveMeans
open Set Filter WeightedClasses MeanIncrementBounds CorrectionState VariableGaugeMean LocalSignedRequest
open scoped ContDiff BigOperators Topology
section CovarianceAssembly
variable {D ι : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end CovarianceAssembly
section WavePressureDebt
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
local notation "st" => movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL
local notation "ss" => PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL
variable (c : Context Point) (u : State Point) (w : Oscillation Point)
    (q : OscillatoryScalar Point) (gaussian : Oscillation Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hbase : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : GaugeDebtIncrement.RegularTriple U g.radial.inner g.radial.outer u.mean)
    (hW : ∀ i j, GaugeDebtIncrement.Regular U g.radial.inner g.radial.outer (u.covariance i j))
    (hX : ∀ i j, GaugeDebtIncrement.Regular U g.radial.inner g.radial.outer
      (SignedMeanGain.covarianceIncrement u.oscillation w i j))
    {κ α : ℝ} (ho : OperatorBounds (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL) c.operators κ)
    (hcX : SignedMeanGain.TensorClass (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL) α (SignedMeanGain.covarianceIncrement u.oscillation w))
#count_heartbeats in
theorem gaugeWaveStage_pressure_from_covariance_R
    (hfixed : (reconstructState g c u).pressure = u.pressure) :
    MeanClass st (α-κ) (SignedMeanGain.pressureChange g c u w q gaussian) := by
  let v := SignedMeanGain.waveStage g c u w q gaussian
  have hmu := GaugeDebtIncrement.waveStage_mean_regular U g c u w q gaussian hm
  have hvW := GaugeDebtIncrement.waveStage_covariance_regular U g c u w q gaussian hW hX
  have hgu := hm.gr ha g.radial.inner_lt_outer hbase hop u.covariance hW
  have hgv := hmu.gr ha g.radial.inner_lt_outer hbase hop v.covariance hvW
  have hgr : MeanClass st (α-κ) (v.gr c - u.gr c) := by
    apply class_congr (SignedMeanGain.radialCovarianceChange_mem ho hcX)
    intro n x hx
    exact GaugeDebtIncrement.waveStage_gr_agree U ha g.radial.inner_lt_outer g c u w q gaussian
      hop hbase hm hW hX n hx.1
  have hp := reconstructState_pressure_change_class U g ha hd hcL hcR ε L hε hεone hL hell
    c v u hgv.smooth hgu.smooth hgv.supported hgu.supported hgr
  simp only [hfixed] at hp
  exact hp
end WavePressureDebt
end ConstructedWaveMeans
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CorrectionStep.reconstructedMeanStage_pressure_change_mem 1044 1271
run_cmd IO.println "BLOCK NavierStokes.CorrectionStep.reconstructedMeanStage_pressure_change_mem"
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
#count_heartbeats in
theorem reconstructedMeanStage_pressure_change_mem_R
    (c : Context Point) (u v : State Point) (inc : Triple Point)
    (hme : v.mean = updated u.mean inc) (hce : v.covariance = u.covariance)
    (hfixed : (reconstructState g c u).pressure = u.pressure)
    {H κ : ℝ} (hH : 9 / 10 ≤ H) (hκ : 2 * κ ≤ 9 / 10)
    (ho : OperatorBounds stageStrip c.operators κ)
    (hb : BaseBounds stageStrip c.base)
    (hu : CorrectionState.CumulativeBounds stageStrip u)
    (hi : IncrementBounds stageStrip H inc)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hbase : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : SmoothTriple (PhysicalMeanDomain.slowDomain U.carrier) u.mean)
    (him : SmoothTriple (PhysicalMeanDomain.slowDomain U.carrier) inc)
    (hms : GaugeSupportedTriple g.radial.inner g.radial.outer (qLength coord) U.carrier u.mean)
    (his : GaugeSupportedTriple g.radial.inner g.radial.outer (qLength coord) U.carrier inc)
    (hW : ∀ i j, SmoothOn (PhysicalMeanDomain.slowDomain U.carrier) (u.covariance i j))
    (hWs : ∀ i j, GaugeSupported g.radial.inner g.radial.outer (qLength coord) U.carrier (u.covariance i j)) :
    MeanClass stageStrip H ((reconstructState g c v).pressure - u.pressure) := by
  have huReg := state_gr_moving_regular U ha g.radial.inner_lt_outer c u hop hbase hm hms hW hWs
  have hvReg := state_gr_moving_regular U ha g.radial.inner_lt_outer c v hop hbase
    (by rw [hme]; exact smooth_updated hm him)
    (by rw [hme]; exact hms.updated his)
    (by simpa only [hce] using hW) (by simpa only [hce] using hWs)
  have hcov : ∀ i j, SmoothOn (stageStrip).domain (u.covariance i j) :=
    fun i j n => (hW i j n).mono (fun _ hx => hx.1)
  have hgr : MeanClass stageStrip H (v.gr c - u.gr c) := by
    simpa only [State.gr, hme, hce] using gr_change_mem ho hb hu.velocity hi hH u.covariance hcov hκ
  have hp := reconstructState_pressure_change_class U g ha hd hcL hcR ε L hε hεone hL hell
    c v u hvReg.1 huReg.1 hvReg.2 huReg.2 hgr
  simp only [hfixed] at hp
  exact hp
end MovingMeanPressure
end NavierStokes.CorrectionStep
end
end

-- REPLAY NavierStokes.CurlClassBounds.class_neg 1275 1292
run_cmd IO.println "BLOCK NavierStokes.CurlClassBounds.class_neg"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CurlClassBounds
open Set Filter Function WeightedClasses
open scoped Topology ContDiff BigOperators InnerProductSpace
section Classes
variable {D E F : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  {s : StripData D} {w : ℕ → D → ℝ} {α β : ℝ}
#count_heartbeats in
theorem class_neg_R {f : ℕ → D → E} (hf : MemClass s w α f) :
    MemClass s w α (fun n x => -f n x) := by
  simpa using hf.map (-ContinuousLinearMap.id ℝ E)
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.CurlClassBounds.class_sub 1296 1313
run_cmd IO.println "BLOCK NavierStokes.CurlClassBounds.class_sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.CurlClassBounds
open Set Filter Function WeightedClasses
open scoped Topology ContDiff BigOperators InnerProductSpace
section Classes
variable {D E F : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  {s : StripData D} {w : ℕ → D → ℝ} {α β : ℝ}
#count_heartbeats in
theorem class_sub_R {f g : ℕ → D → E} (hf : MemClass s w α f) (hg : MemClass s w α g) :
    MemClass s w α (fun n x => f n x - g n x) := by
  simpa only [sub_eq_add_neg] using hf.add (class_neg hg)
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.GaugeAliasDecay.temporalAxialDifference_mem 1317 1376
run_cmd IO.println "BLOCK NavierStokes.GaugeAliasDecay.temporalAxialDifference_mem"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.GaugeAliasDecay
open Set Filter Function MeasureTheory
open scoped ContDiff Topology Interval BigOperators
open TorusInverse JetBounds UniformFourierAlias
section FiberInverse
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end FiberInverse
section PhysicalIntegral
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end PhysicalIntegral
section MovingAlias
open VariableGaugeMean LocalSignedRequest WeightedClasses
end MovingAlias
section ActualFrequency
end ActualFrequency
section ClassConclusions
open VariableGaugeMean LocalSignedRequest WeightedClasses
end ClassConclusions
section ActualTemporalAlias
open VariableGaugeMean LocalSignedRequest WeightedClasses
#count_heartbeats in
theorem temporalAxialDifference_mem_R {a b h Mbase α : ℝ} (U : SlowRegion (2 * h))
    (ha : 0 < a) (hab : a < b) {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (hh : 0 < h) (hM : Mbase ≠ 0) (index : ℕ → ℕ) (D : ℕ)
    (hgap : ∀ n, ChartScales.nativeIndex h n ≤ index n + D)
    (L : ℕ → ℝ) (hL : ∀ n, 1 ≤ L n) (hS : ∀ n, ChartScales.S n ≤ L n)
    (c : CorrectionState.Context (Point Plane)) (u : CorrectionState.State (Point Plane))
    (hf : ∀ n, ContDiffOn ℝ ∞ (u.axialResidual c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hs : ∀ n, SupportedGauge a b (qLength (2 * h)) U.carrier (u.axialResidual c n))
    (hp : ∀ n, PhysicalMeanDomain.PeriodicOn U.carrier (u.axialResidual c n))
    (hclass : MeanClass (movingStripData U a b cL cR ha hcL hcR (ChartScales.epsilon h) L
      (ChartScales.epsilon_pos h) (ChartScales.epsilon_le_one h hh.le) hL) α (u.axialResidual c)) (β : ℝ) :
    MeanClass (movingStripData U a b cL cR ha hcL hcR (ChartScales.epsilon h) L
      (ChartScales.epsilon_pos h) (ChartScales.epsilon_le_one h hh.le) hL) β
      (temporalAxialDifference (similarityGauge h (ChartScales.radialExponent h) a b Mbase hab index)
        h index c u) := by
  have hfield := temporalSource_movingField U h index hf hs hp
  have hsrc := temporalSource_mem U ha hcL hcR hh index D hgap L hL hS hf hp hclass
  have hgain := meanClass_dividedAlias_superflat U ha hab hcL hcR hh hM index D hgap L hL hS
    hfield.smooth hfield.supported hfield.periodic
    (fun n s hs => temporalSource_zero_mass U h index hf hp n hs) hsrc β
  apply MeanRankUpdate.meanClass_congr_on hgain
  intro n z hz
  have hzm := (movingStrip_domain U a b cL cR ha hcL hcR (ChartScales.epsilon h) L
    (ChartScales.epsilon_pos h) (ChartScales.epsilon_le_one h hh.le) hL z).mp hz
  have hell := qLength_pos U.coord_pos U.coord_lt_one (U.time_pos z.2.1 hzm.1)
  have hR : z.1 ≠ 0 := ne_of_gt (by
    have hpR : 0 < z.1 / qLength (2 * h) z.2.1 := ha.trans hzm.2.1
    simpa only [zero_mul] using (lt_div_iff₀ hell).mp hpR)
  exact temporalAxialDifference_eq_dividedAlias U
    (similarityGauge h (ChartScales.radialExponent h) a b Mbase hab index)
    ha (ChartScales.radialExponent_pos h hh.le) (fun _ => rfl) c u h index n
    (hf n) (hp n) (hs n) hzm.1 hR
end ActualTemporalAlias
end NavierStokes.GaugeAliasDecay
end
end

-- REPLAY NavierStokes.GaugeDebtIncrement.temporalStage_debt_change_mem 1380 1508
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.temporalStage_debt_change_mem"
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
end WaveBounds
section TemporalAlgebra
variable (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
end TemporalAlgebra
section TemporalRegularity
variable {coord a b : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b)
    (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hi : RegularTriple U a b (VariableGaugeMean.temporalIncrementState g h index axial c u))
    (hW : ∀ i j, Regular U a b (u.covariance i j))
end TemporalRegularity
section TemporalBounds
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hi : RegularTriple U a b (VariableGaugeMean.temporalIncrementState g h index axial c u))
    (hW : ∀ i j, Regular U a b (u.covariance i j))
include hab hop hb hm hi hW
#count_heartbeats in
theorem temporalStage_debt_change_mem_R {κ H : ℝ}
    (ho : OperatorBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) c.operators κ)
    (hbC : BaseBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) c.base)
    (hmC : MeanIncrementBounds.CumulativeBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) u.mean)
    (hiC : IncrementBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) H
      (VariableGaugeMean.temporalIncrementState g h index axial c u))
    (hH : 9 / 10 ≤ H) (hκ : 2 * κ ≤ 9 / 10) (i : Fin 3) :
    UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL) H
      (fun n x => debt c (VariableGaugeMean.temporalStageState g h index axial c u) n x i - debt c u n x i) := by
  let st := movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL
  have hsub : st.domain ⊆ PhysicalMeanDomain.slowDomain U.carrier := fun z hz =>
    ((movingStrip_domain U a b cL cR ha hcL hcR ε L hε hεone hL z).mp hz).1
  have hmu := temporalStage_mean_regular U g h index axial c u hm hi
  have hWv := temporalStage_covariance_regular U g h index axial c u hW
  have hcg : MeanClass st H ((VariableGaugeMean.temporalStageState g h index axial c u).gr c - u.gr c) := by
    simpa only [State.gr, temporalStage_mean, temporalStage_covariance] using
      gr_change_mem ho hbC hmC hiC hH u.covariance
        (fun i j n => ((hW i j).smooth n).mono hsub) hκ
  have hct : MeanClass st H
      ((thetaAxial c.base (VariableGaugeMean.temporalStageState g h index axial c u).mean +
        (VariableGaugeMean.temporalStageState g h index axial c u).covariance 2 1) -
          (thetaAxial c.base u.mean + u.covariance 2 1)) := by
    rw [temporal_thetaFlux_change]
    exact deltaThetaAxial_mem ho hbC hmC hiC hH
  have hcz : MeanClass st H
      ((axialAxial c.base (VariableGaugeMean.temporalStageState g h index axial c u).mean +
        (VariableGaugeMean.temporalStageState g h index axial c u).covariance 2 2) -
          (axialAxial c.base u.mean + u.covariance 2 2)) := by
    rw [temporal_axialFlux_change]
    exact deltaAxialAxial_mem ho hbC hmC hiC hH
  exact debt_change_mem U ha hab hcL hcR ε L hε hεone hL c u
    (VariableGaugeMean.temporalStageState g h index axial c u)
    (hm.gr ha hab hb hop u.covariance hW)
    (hmu.gr ha hab hb hop (VariableGaugeMean.temporalStageState g h index axial c u).covariance hWv)
    ((hm.thetaAxial ha hab hb).add (hW 2 1)) ((hmu.thetaAxial ha hab hb).add (hWv 2 1))
    ((hm.axialAxial ha hab hb).add (hW 2 2)) ((hmu.axialAxial ha hab hb).add (hWv 2 2)) hcg hct hcz i
end TemporalBounds
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.GaugeDebtIncrement.waveStage_debt_change_mem 1512 1594
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

-- REPLAY NavierStokes.GaugeDebtIncrement.waveStage_debt_mem 1598 1717
run_cmd IO.println "BLOCK NavierStokes.GaugeDebtIncrement.waveStage_debt_mem"
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
end WaveBounds
section TemporalAlgebra
variable (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
end TemporalAlgebra
section TemporalRegularity
variable {coord a b : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b)
    (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hi : RegularTriple U a b (VariableGaugeMean.temporalIncrementState g h index axial c u))
    (hW : ∀ i j, Regular U a b (u.covariance i j))
end TemporalRegularity
section TemporalBounds
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (g : VariableGaugeMean.GaugeData Plane) (h : ℝ) (index : ℕ → ℕ)
    (axial : Plane × Plane) (c : Context Point) (u : State Point)
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hb : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hm : RegularTriple U a b u.mean)
    (hi : RegularTriple U a b (VariableGaugeMean.temporalIncrementState g h index axial c u))
    (hW : ∀ i j, Regular U a b (u.covariance i j))
include hab hop hb hm hi hW
end TemporalBounds
section DebtPropagation
end DebtPropagation
section WaveNextDebt
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
    {κ α : ℝ}
    (ho : OperatorBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) c.operators κ)
    (hcX : SignedMeanGain.TensorClass (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) α
      (SignedMeanGain.covarianceIncrement u.oscillation w))
include hab hop hb hm hW hX ho hcX
#count_heartbeats in
theorem waveStage_debt_mem_R {β : ℝ} (hβ : α - κ ≤ β)
    (hold : ∀ i : Fin 3, UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen
      ε L hε hεone hL) β (fun n x => debt c u n x i)) :
    ∀ i : Fin 3, UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen
      ε L hε hεone hL) (α - κ)
      (fun n x => debt c (SignedMeanGain.waveStage g c u w q gaussian) n x i) :=
  debt_mem_after_change _ c u _ hβ le_rfl hold
    (waveStage_debt_change_mem U ha hab hcL hcR ε L hε hεone hL g c u w q gaussian hop hb hm hW hX ho hcX)
end WaveNextDebt
end
end NavierStokes.GaugeDebtIncrement
end

-- REPLAY NavierStokes.HarmonicWaveInteraction.class_slice 1721 1743
run_cmd IO.println "BLOCK NavierStokes.HarmonicWaveInteraction.class_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.HarmonicWaveInteraction
open Set Filter Function HarmonicCalculus HarmonicFields WeightedClasses WaveInteractionBounds
open HarmonicMeanInteraction
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
#count_heartbeats in
theorem class_slice_R {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ} {f : ℕ → D × ℝ → F}
    (hf : MemClass (productStrip s) (fun n p => w n p.1) α f) :
    MemClass s w α (fun n x => f n (x, 0)) := by
  have hh := class_pullback hf inclusion inclusion_norm
  have he : pullbackStrip (productStrip s) (inclusion (D := D)) = s := by
    cases s
    rfl
  rw [he] at hh
  exact hh
end NavierStokes.HarmonicWaveInteraction
end
end

-- REPLAY NavierStokes.LocalSignedRequest.meanClass_compact 1747 1810
run_cmd IO.println "BLOCK NavierStokes.LocalSignedRequest.meanClass_compact"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalSignedRequest
open Set Function Filter MeasureTheory
open WeightedClasses WeightedRadialPrimitive
open scoped ContDiff Topology Interval BigOperators
section Composition
variable {D E F : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end Composition
section ClassMaps
variable {coord : ℝ} (U : SlowRegion coord)
  (a b cL cR : ℝ) (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
  (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end ClassMaps
section LocalPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
#count_heartbeats in
theorem meanClass_compact_R {a b c d cL cR : ℝ}
    (ha : 0 < a) (hac : a < c) (hcd : c < d) (hdb : d < b)
    (hcL : 0 < cL) (hcR : 0 < cR) (χ : ℝ → ℝ) (hχ : ContDiff ℝ ∞ χ)
    (hleft : ∀ X, X ≤ c → χ X = 0) (hright : ∀ X, d ≤ X → χ X = 1)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (U : Set S) (hU : IsOpen U) (α : ℝ) (M : ℕ → ℝ) (v : ℕ → Plane)
    (f : ℕ → PressureStream.Lift S → ℝ)
    (hf : ∀ n, ContDiffOn ℝ ∞ (f n) (PhysicalMeanDomain.slowDomain U))
    (hs : ∀ n, PhysicalMeanDomain.SupportedOn a b U (f n))
    (hclass : MeanClass (PhysicalMeanDomain.localStripData a b cL cR ha hcL hcR
      ε L hε hεone hL U hU) α f) :
    MeanClass (PhysicalMeanDomain.localStripData a b cL cR ha hcL hcR
      ε L hε hεone hL U hU) α
      (fun n => TransportPrimitive.compactIntegral χ (M n) ((0 : S), v n) (f n)) := by
  refine ⟨hclass.weight_nonneg,
    fun n => (compact_contDiffOn hχ (v n) hU (hf n) (hs n)).mono (fun _ hp => hp.2), ?_⟩
  intro m
  obtain ⟨C, hC, k, hb⟩ := hclass.bounds m
  obtain ⟨K, hK, hbound⟩ := PhysicalMeanDomain.transport_compact_finiteJets_fiber
    (S := S) (V := ℝ) ha hac hcd hdb hcL hcR k m χ hχ hleft hright
  refine ⟨K * C, mul_nonneg hK hC, k, ?_⟩
  intro n p hp j hj
  obtain ⟨c₀, _, hcs, hcf, he⟩ := PhysicalMeanDomain.exists_fiber_localization hU hp.2 (hf n)
  have hA : 0 ≤ C * ε n ^ α * L n ^ k :=
    mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (hε n) α).le)
      (pow_nonneg (zero_le_one.trans (hL n)) _)
  have hin : ∀ i ≤ m, ∀ R ∈ Ioo a b, ∀ Y : Plane,
      ‖iteratedFDeriv ℝ i (PhysicalMeanDomain.localize c₀ (f n)) (R, (p.2.1, Y))‖ ≤
        (C * ε n ^ α * L n ^ k) * logWeight cL cR a b k R := by
    intro i hi R hR Y
    rw [he.jet_eq i R Y]
    have h := hb n (R, (p.2.1, Y)) ⟨hR, hp.2⟩ i hi
    rwa [PhysicalMeanDomain.localStrip_majorant_eq ha hcL hcR
      ε L hε hεone hL U hU α C k n _ hR] at h
  have hout := hbound (M n) (v n) _ hcf (PhysicalMeanDomain.localize_supported hcs (hs n))
    (C * ε n ^ α * L n ^ k) hA p.2.1 hin p hp.1 rfl j hj
  rw [((compact_fiberLocal χ (M n) (v n)).germ he).jet_eq j p.1 p.2.2] at hout
  rw [PhysicalMeanDomain.localStrip_majorant_eq ha hcL hcR
    ε L hε hεone hL U hU α (K * C) k n p hp.1]
  exact hout.trans_eq (by ring)
end LocalPrimitive
end NavierStokes.LocalSignedRequest
end
end

-- REPLAY NavierStokes.LocalSignedRequest.normalizedRequest_class 1814 1862
run_cmd IO.println "BLOCK NavierStokes.LocalSignedRequest.normalizedRequest_class"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalSignedRequest
open Set Function Filter MeasureTheory
open WeightedClasses WeightedRadialPrimitive
open scoped ContDiff Topology Interval BigOperators
section Composition
variable {D E F : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end Composition
section ClassMaps
variable {coord : ℝ} (U : SlowRegion coord)
  (a b cL cR : ℝ) (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
  (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end ClassMaps
section LocalPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalPrimitive
section PhysicalRequest
#count_heartbeats in
theorem normalizedRequest_class_R {coord : ℝ} (U : SlowRegion coord)
    (P : SignedStressPrimitive.Patch) {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (c : CorrectionState.Context Point) (u : CorrectionState.State Point) (α : ℝ)
    (hθ : ∀ n, ContDiffOn ℝ ∞ (u.thetaResidual c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hz : ∀ n, ContDiffOn ℝ ∞ (u.axialResidual c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hsθ : ∀ n, MovingSupport P.a P.b coord U.carrier (u.thetaResidual c n))
    (hsz : ∀ n, MovingSupport P.a P.b coord U.carrier (u.axialResidual c n))
    (hcθ : MeanClass (movingStripData U P.a P.b cL cR P.a_pos hcL hcR ε L hε hεone hL) α
      (u.thetaResidual c))
    (hcz : MeanClass (movingStripData U P.a P.b cL cR P.a_pos hcL hcR ε L hε hεone hL) α
      (u.axialResidual c)) :
    ∀ i, MeanClass (movingStripData U P.a P.b cL cR P.a_pos hcL hcR ε L hε hεone hL) (α - 1)
      (fun n x => normalizedRequest
        (movingStripData U P.a P.b cL cR P.a_pos hcL hcR ε L hε hεone hL) P coord c u n x i) := by
  have h1 := meanClass_physicalBarSigma U P 2 hcL hcR ε L hε hεone hL hθ hsθ hcθ
  have h2 := meanClass_physicalBarSigma U P 1 hcL hcR ε L hε hεone hL hz hsz hcz
  have hscale := bandBound_rpow
    (movingStripData U P.a P.b cL cR P.a_pos hcL hcR ε L hε hεone hL) (-1)
  intro i
  fin_cases i
  · simpa [normalizedRequest, requestedStress, Real.rpow_neg_one, sub_eq_add_neg] using h1.band_smul hscale
  · simpa [normalizedRequest, requestedStress, Real.rpow_neg_one, sub_eq_add_neg] using h2.band_smul hscale
end PhysicalRequest
end NavierStokes.LocalSignedRequest
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.Class.neg 1866 1890
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.Class.neg"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
#count_heartbeats in
theorem neg_R {s : StripData D} {α : ℝ} {f : Field D} (hf : MeanClass s α f) :
    MeanClass s α (-f) := by
  have h := hf.map (-ContinuousLinearMap.id ℝ ℝ)
  simp only [_root_.neg_apply, ContinuousLinearMap.id_apply] at h
  exact h
end Class
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.Class.product 1894 1917
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.Class.product"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
#count_heartbeats in
theorem product_R {s : StripData D} {α β : ℝ} {f g : Field D}
    (hf : MeanClass s α f) (hg : MeanClass s β g)
    (hζ : ∀ x ∈ s.domain, s.zeta x ≤ 1) : MeanClass s (α + β) (f * g) := by
  exact hf.bilinear hg hζ (ContinuousLinearMap.lsmul ℝ ℝ)
end Class
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.Class.sub 1921 1945
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.Class.sub"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
#count_heartbeats in
theorem sub_R {s : StripData D} {α : ℝ} {f g : Field D}
    (hf : MeanClass s α f) (hg : MeanClass s α g) : MeanClass s α (f - g) := by
  have h := hf.add (neg hg)
  simp only [sub_eq_add_neg] at h ⊢
  exact h
end Class
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.OperatorBounds.inv_mul 1949 1974
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.OperatorBounds.inv_mul"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
#count_heartbeats in
theorem inv_mul_R (ho : OperatorBounds s o κ) {f : Field D} (hf : MeanClass s α f) :
    MeanClass s α (o.invRadius * f) := by
  simpa only [zero_add] using Class.coefficient_mul ho.invRadius hf
end OperatorBounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.OperatorBounds.radialDiv 1978 2004
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.OperatorBounds.radialDiv"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
#count_heartbeats in
theorem radialDiv_R (ho : OperatorBounds s o κ) {f : Field D} (hf : MeanClass s α f) (c : ℝ) :
    MeanClass s (α - κ) (o.radialDiv c f) :=
  (ho.dr hf).add ((Class.smul (ho.inv_mul hf) c).mono_exponent
    (sub_le_self α ho.kappa_nonneg))
end OperatorBounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.gr_change_sub_leading_mem 2008 2059
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.gr_change_sub_leading_mem"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
end Bounds
namespace SmoothTriple
variable {U : Set D} {b m h : Triple D}
end SmoothTriple
section ExactChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U) {b m h : Triple D}
  (hb : SmoothTriple U b) (hm : SmoothTriple U m) (hh : SmoothTriple U h)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn U (W i j))
end ExactChanges
section ActualBounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn s.domain (W i j))
#count_heartbeats in
theorem gr_change_sub_leading_mem_R :
    MeanClass s (H + 9 / 10 - 2 * κ)
      (gr o b (updated m h) W - gr o b m W - leadingRadial o b h) := by
  apply class_congr (radialRemainder_mem ho hb hm hh hH)
  intro n x hx
  have he := gr_change s.isOpen_domain o (ho.radialProfile.smooth 0)
    hb.smooth hm.smooth hh.smooth W hW n hx
  simp only [Pi.sub_apply, Pi.add_apply] at he ⊢
  linarith
end ActualBounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.interior_cutoff_meanClass 2063 2145
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.interior_cutoff_meanClass"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
end Bounds
namespace SmoothTriple
variable {U : Set D} {b m h : Triple D}
end SmoothTriple
section ExactChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U) {b m h : Triple D}
  (hb : SmoothTriple U b) (hm : SmoothTriple U m) (hh : SmoothTriple U h)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn U (W i j))
end ExactChanges
section ActualBounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn s.domain (W i j))
end ActualBounds
section PressureReconstruction
open MeasureTheory Function WeightedRadialPrimitive
open scoped Interval
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
#count_heartbeats in
theorem interior_cutoff_meanClass_R
    {a b cL cR l r : ℝ} (ha : 0 < a) (hal : a < l) (hrb : r < b)
    (hcL : 0 < cL) (hcR : 0 < cR)
    (ε S : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1)
    (hS : ∀ n, 1 ≤ S n) (χ : ℝ → ℝ) (hχ : ContDiff ℝ ∞ χ)
    (hs : support χ ⊆ Icc l r) :
    MeanClass (logStripData a b cL cR ha hcL hcR ε S hε hεone hS) 0
      (fun _ (x : ℝ × P) => χ x.1) := by
  have hlog : ContinuousOn (fun x : ℝ => logPosition a x) (Icc l r) :=
    (continuousOn_id.div_const a).log (fun x hx =>
      (div_pos (ha.trans (hal.trans_le hx.1)) ha).ne')
  obtain ⟨d, hd, hmargin⟩ := UniformCone.positive_uniform_margin isCompact_Icc
    ((zeta_continuous hcL hcR (logLength a b)).comp_continuousOn hlog)
    (fun x (hx : x ∈ Icc l r) => zeta_pos cL cR
      (logPosition_mem ha ⟨hal.trans_le hx.1, hx.2.trans_lt hrb⟩))
  have hsupport : RadialAlias.RadiallySupported l r (fun x : ℝ × P => χ x.1) :=
    fun _ hx => hs hx
  refine ⟨fun _ x hx => (zeta_pos cL cR (logPosition_mem ha hx)).le,
    fun _ => (hχ.comp contDiff_fst).contDiffOn, ?_⟩
  intro m
  obtain ⟨B, hB, hbound⟩ := cutoff_finiteJet_bound (E := P) a b χ hχ m
  refine ⟨B / d, div_nonneg hB hd.le, 0, ?_⟩
  intro n x hx j hj
  rw [logStrip_majorant_eq ha hcL hcR ε S hε hεone hS 0 (B / d) 0 n x hx]
  simp only [Real.rpow_zero, pow_zero, mul_one, logWeight, weight, div_one]
  by_cases hm : x.1 ∈ Icc l r
  · calc
      _ ≤ B := hbound j hj x ⟨hx.1.le, hx.2.le⟩
      _ = (B / d) * d := by field_simp
      _ ≤ _ := mul_le_mul_of_nonneg_left (hmargin x.1 hm) (div_nonneg hB hd.le)
  · have hz : iteratedFDeriv ℝ j (fun x : ℝ × P => χ x.1) x = 0 := by
      by_contra hn
      exact hm ((TransportPrimitive.iteratedFDeriv_supported hsupport j) hn)
    rw [hz, norm_zero]
    exact mul_nonneg (div_nonneg hB hd.le) (zeta_pos cL cR (logPosition_mem ha hx)).le
end PressureReconstruction
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.radialRemainder_mem 2149 2189
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.radialRemainder_mem"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
#count_heartbeats in
theorem radialRemainder_mem_R :
    MeanClass s (H + 9 / 10 - 2 * κ) (radialRemainder o b m h) := by
  have h1 := (ho.time hh.radial).mono_exponent
    (show H + 9 / 10 - 2 * κ ≤ H + 1 by linarith [ho.kappa_nonneg])
  have h2 := (ho.radialDiv (deltaRadialRadial_mem ho hb hm hh hH) 1).mono_exponent
    (show H + 9 / 10 - 2 * κ ≤ (H + 2) - κ by linarith [ho.kappa_nonneg])
  have h3 := (ho.dz (deltaAxialRadial_mem ho hb hm hh hH)).mono_exponent
    (show H + 9 / 10 - 2 * κ ≤ (H + 1) + 1 by linarith [ho.kappa_nonneg])
  have h4 := (ho.inv_mul (radialAngularRemainder_mem ho hm hh hH)).mono_exponent
    (show H + 9 / 10 - 2 * κ ≤ H + 9 / 10 by linarith [ho.kappa_nonneg])
  have h5 := (ho.viscosity hh.radial 1).mono_exponent
    (show H + 9 / 10 - 2 * κ ≤ (H + 1) + 1 - 2 * κ by linarith)
  exact ((Class.sub (Class.sub (Class.neg h1) h2) h3).add h4).add h5
end Bounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.rho_meanClass 2193 2254
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.rho_meanClass"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
end Bounds
namespace SmoothTriple
variable {U : Set D} {b m h : Triple D}
end SmoothTriple
section ExactChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U) {b m h : Triple D}
  (hb : SmoothTriple U b) (hm : SmoothTriple U m) (hh : SmoothTriple U h)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn U (W i j))
end ExactChanges
section ActualBounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn s.domain (W i j))
end ActualBounds
section PressureReconstruction
open MeasureTheory Function WeightedRadialPrimitive
open scoped Interval
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
#count_heartbeats in
theorem rho_meanClass_R
    {a b cL cR : ℝ} (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε S : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1)
    (hS : ∀ n, 1 ≤ S n) :
    MeanClass (logStripData a b cL cR ha hcL hcR ε S hε hεone hS) 0
      (fun _ (x : ℝ × P) => PressureStream.rho a b hab x.1) := by
  apply interior_cutoff_meanClass ha (show a < (3 * a + b) / 4 by linarith)
    (show (a + 3 * b) / 4 < b by linarith) hcL hcR ε S hε hεone hS
    _ (PressureStream.rho_contDiff a b hab)
  intro x hx
  rw [PressureStream.rho, ContDiffBump.support_normed_eq] at hx
  change dist x ((a + b) / 2) < (b - a) / 4 at hx
  rw [Real.dist_eq, abs_lt] at hx
  constructor <;> linarith [hx.1, hx.2]
end PressureReconstruction
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.thetaRemainder_mem 2258 2293
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.thetaRemainder_mem"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
#count_heartbeats in
theorem thetaRemainder_mem_R : MeanClass s (H + 1 - 2 * κ) (thetaRemainder o b m h) := by
  have h1 := (ho.slowTime hh.angular).mono_exponent
    (show H + 1 - 2 * κ ≤ H + 1 by linarith [ho.kappa_nonneg])
  have h2 := (ho.radialDiv (deltaThetaRadial_mem ho hb hm hh hH) 2).mono_exponent
    (show H + 1 - 2 * κ ≤ (H + 1) - κ by linarith [ho.kappa_nonneg])
  have h3 := (ho.dz (deltaThetaAxial_mem ho hb hm hh hH)).mono_exponent
    (show H + 1 - 2 * κ ≤ H + 1 by linarith [ho.kappa_nonneg])
  exact Class.sub ((h1.add h2).add h3) (ho.viscosity hh.angular 1)
end Bounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.thetaResidual_change_slow_mem 2297 2346
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.thetaResidual_change_slow_mem"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
end Bounds
namespace SmoothTriple
variable {U : Set D} {b m h : Triple D}
end SmoothTriple
section ExactChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U) {b m h : Triple D}
  (hb : SmoothTriple U b) (hm : SmoothTriple U m) (hh : SmoothTriple U h)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn U (W i j))
end ExactChanges
section ActualBounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn s.domain (W i j))
#count_heartbeats in
theorem thetaResidual_change_slow_mem_R (T : Field D)
    (hslow : ∀ n x, x ∈ s.domain → fderiv ℝ (h.angular n) x o.vT = 0) :
    MeanClass s (H + 1 - 2 * κ)
      (thetaResidual o b (updated m h) W T - thetaResidual o b m W T) := by
  apply class_congr (thetaResidual_change_sub_fast_mem ho hb hm hh hH W hW T)
  intro n x hx
  simp only [Pi.sub_apply, Operators.fastTime, hslow n x hx, mul_zero, sub_zero]
end ActualBounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanIncrementBounds.thetaResidual_change_sub_fast_mem 2350 2402
run_cmd IO.println "BLOCK NavierStokes.MeanIncrementBounds.thetaResidual_change_sub_fast_mem"
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
end SmoothOn
namespace Operators
end Operators
namespace Class
end Class
namespace OperatorBounds
variable {s : StripData D} {o : Operators D} {κ α : ℝ}
end OperatorBounds
section Bounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
end Bounds
namespace SmoothTriple
variable {U : Set D} {b m h : Triple D}
end SmoothTriple
section ExactChanges
variable {U : Set D} (hU : IsOpen U) (o : Operators D)
  (ha : ContDiffOn ℝ ∞ o.radialProfile U) {b m h : Triple D}
  (hb : SmoothTriple U b) (hm : SmoothTriple U m) (hh : SmoothTriple U h)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn U (W i j))
end ExactChanges
section ActualBounds
variable {s : StripData D} {o : Operators D} {κ H : ℝ} {b m h : Triple D}
  (ho : OperatorBounds s o κ) (hb : BaseBounds s b) (hm : CumulativeBounds s m)
  (hh : IncrementBounds s H h) (hH : 9 / 10 ≤ H)
  (W : Fin 3 → Fin 3 → Field D) (hW : ∀ i j, SmoothOn s.domain (W i j))
#count_heartbeats in
theorem thetaResidual_change_sub_fast_mem_R (T : Field D) :
    MeanClass s (H + 1 - 2 * κ)
      (thetaResidual o b (updated m h) W T - thetaResidual o b m W T -
        o.fastTime h.angular) := by
  apply class_congr (thetaRemainder_mem ho hb hm hh hH)
  intro n x hx
  have he := thetaResidual_change s.isOpen_domain o (ho.radialProfile.smooth 0)
    hb.smooth hm.smooth hh.smooth W hW T n hx
  simp only [Pi.sub_apply, Pi.add_apply] at he ⊢
  linarith
end ActualBounds
end NavierStokes.MeanIncrementBounds
end
end

-- REPLAY NavierStokes.MeanMomentBounds.radialCoefficient_unweighted 2406 2444
run_cmd IO.println "BLOCK NavierStokes.MeanMomentBounds.radialCoefficient_unweighted"
section
set_option linter.all false
namespace NavierStokes.MeanMomentBounds
noncomputable section
open Set Function MeasureTheory Filter
open scoped ContDiff Topology Interval BigOperators
open WeightedClasses WeightedRadialPrimitive
variable {D E F : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
section AffineAverage
variable [CompleteSpace F]
end AffineAverage
section Torus
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end Torus
section RadialIntegral
variable [CompleteSpace E]
end RadialIntegral
section PressureMass
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
end PressureMass
section WeightedMoments
variable {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
#count_heartbeats in
theorem radialCoefficient_unweighted_R
    {a b cL cR : ℝ} (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε S : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1)
    (hS : ∀ n, 1 ≤ S n) {g : ℝ → ℝ} (hg : ContDiff ℝ ∞ g) :
    UnweightedClass (logStripData (E := P) a b cL cR ha hcL hcR ε S hε hεone hS) 0
      (fun _ x => g x.1) := by
  apply unweighted_of_finiteJetBounds _ _ (hg.comp contDiff_fst).contDiffOn
  intro m
  obtain ⟨C, _, hb⟩ := cutoff_finiteJet_bound (E := P) a b g hg m
  exact ⟨C, fun j hj x hx => hb j hj x ⟨hx.1.le, hx.2.le⟩⟩
end WeightedMoments
end
end NavierStokes.MeanMomentBounds
end

-- REPLAY NavierStokes.MovingMomentBounds.rankStage_defect_class 2448 2548
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.rankStage_defect_class"
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
end Support
end Support
section Remainders
open DefectIncrementBounds
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end Remainders
section RankDefect
variable {coord cL cR : ℝ} (U : SlowRegion coord)
    (g : GaugeData PressureStream.Plane) (r : RankData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
    (axial : PressureStream.Plane × PressureStream.Plane)
    (c : Context Point) (u : State Point)
    (hg : LocalRankDefect.RankGeometry g r U.carrier c u)
#count_heartbeats in
theorem rankStage_defect_class_R {κ H : ℝ}
    (hop : LocalRankDefect.LocalOperators U.carrier c.operators)
    (hbc : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) c.base)
    (hmc : SmoothTriple (PhysicalMeanDomain.slowDomain U.carrier) u.mean)
    (hms : SupportedTriple g.radial.inner g.radial.outer (qLength coord) U.carrier u.mean)
    (hWc : ∀ i j, SmoothOn (PhysicalMeanDomain.slowDomain U.carrier) (u.covariance i j))
    (hWs : ∀ i j, Support g.radial.inner g.radial.outer (qLength coord) U.carrier (u.covariance i j))
    (hV : LocalRankDefect.IsSlowOn U.carrier c.base.angular)
    (hG : LocalRankDefect.IsSlowOn U.carrier c.base.axial)
    (ho : OperatorBounds (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL)
      c.operators κ)
    (hb : BaseBounds (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL) c.base)
    (hm : MeanIncrementBounds.CumulativeBounds
      (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL) u.mean)
    (hi : IncrementBounds (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL)
      H (rankIncrementState g r axial c u)) (hH : 9 / 10 ≤ H) (i : Fin 3) :
    UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL)
      (H + 9 / 10 - 2 * κ) (fun n x => debt c (rankStageState g r axial c u) n x i) := by
  obtain ⟨a₀, b₀, R₀, ha₀, hab₀, _, _, hleft, hright, _⟩ :=
    qLength_reference_bounds U ha g.radial.inner_lt_outer
  have hl (n : ℕ) (x : PressureStream.Plane) (hx : x ∈ U.carrier) : a₀ ≤ r.length n x * r.inner := by
    have hh := hg.gauge_left n x hx
    rw [hell n] at hh
    exact (hleft x hx).trans hh
  have hr (n : ℕ) (x : PressureStream.Plane) (hx : x ∈ U.carrier) : r.length n x * r.outer ≤ b₀ := by
    have hh := hg.gauge_right n x hx
    rw [hell n] at hh
    exact hh.trans (hright x hx)
  have hfixed {f : ScalarField Point}
      (hs : Support g.radial.inner g.radial.outer (qLength coord) U.carrier f) :
      ∀ n, PhysicalMeanDomain.SupportedOn a₀ b₀ U.carrier (f n) := by
    intro n x hx hn
    exact ⟨(hleft _ hx).trans (hs n x hx hn).1, (hs n x hx hn).2.trans (hright _ hx)⟩
  have hml : LocalRankDefect.LocalTriple a₀ b₀ U.carrier u.mean :=
    ⟨⟨hmc.radial, hfixed hms.radial⟩, ⟨hmc.angular, hfixed hms.angular⟩,
      ⟨hmc.axial, hfixed hms.axial⟩⟩
  have hwl (i j : Fin 3) : LocalRankDefect.LocalShell a₀ b₀ U.carrier (u.covariance i j) :=
    ⟨hWc i j, hfixed (hWs i j)⟩
  have hir := hg.increment_localTriple ha₀ hab₀ U.isOpen hl hr axial
  have his : SupportedTriple g.radial.inner g.radial.outer (qLength coord) U.carrier
      (rankIncrementState g r axial c u) := by
    have hcontain (n : ℕ) {f : Point → ℝ}
        (hs : SupportedGauge r.inner r.outer (r.length n) U.carrier f) :
        SupportedGauge g.radial.inner g.radial.outer (qLength coord) U.carrier f := by
      intro z hz hn
      obtain ⟨hzl, hzr⟩ := hs z hz hn
      have hgl := hg.gauge_left n z.2.1 hz
      have hgr := hg.gauge_right n z.2.1 hz
      rw [hell n] at hgl hgr
      exact ⟨hgl.trans hzl, hzr.trans hgr⟩
    exact ⟨fun n => hcontain n (hg.increment_supportedGauge ha₀ hab₀ U.isOpen hl hr axial n).1,
      fun n => hcontain n (hg.increment_supportedGauge ha₀ hab₀ U.isOpen hl hr axial n).2.1,
      fun n => hcontain n (hg.increment_supportedGauge ha₀ hab₀ U.isOpen hl hr axial n).2.2⟩
  have hrem := remainders_mem U ha g.radial.inner_lt_outer hcL hcR ε L hε hεone hL hop hbc hmc
    hir.smooth hms his u.covariance hWc hWs ho hb hm hi hH i
  apply LinearWaveBounds.class_congr hrem
  intro n x hx
  exact congrArg (fun v : Fin 3 → ℝ => v i)
    (hg.debt_eq_remainders ha₀ hab₀ U.isOpen hl hr axial hop hbc hml hwl hV hG n hx).symm
end RankDefect
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.MovingMomentBounds.remainders_mem 2552 2635
run_cmd IO.println "BLOCK NavierStokes.MovingMomentBounds.remainders_mem"
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
end Support
end Support
section Remainders
open DefectIncrementBounds
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
#count_heartbeats in
theorem remainders_mem_R {o : Operators Point} {base m h : Triple Point} {κ H : ℝ}
    (hop : LocalRankDefect.LocalOperators U.carrier o)
    (hbs : SmoothTriple (LocalRankDefect.positiveDomain U.carrier) base)
    (hmc : SmoothTriple (PhysicalMeanDomain.slowDomain U.carrier) m)
    (hhc : SmoothTriple (PhysicalMeanDomain.slowDomain U.carrier) h)
    (hms : SupportedTriple a b (qLength coord) U.carrier m)
    (hhs : SupportedTriple a b (qLength coord) U.carrier h)
    (W : Fin 3 → Fin 3 → CorrectionState.ScalarField Point) (hWc : ∀ i j, SmoothOn (PhysicalMeanDomain.slowDomain U.carrier) (W i j))
    (hWs : ∀ i j, Support a b (qLength coord) U.carrier (W i j))
    (ho : OperatorBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) o κ)
    (hb : BaseBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) base)
    (hm : MeanIncrementBounds.CumulativeBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) m)
    (hh : IncrementBounds (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) H h)
    (hH : 9 / 10 ≤ H) (i : Fin 3) :
    UnweightedClass (PhysicalMeanDomain.localSlowStripData U.carrier U.isOpen ε L hε hεone hL)
      (H + 9 / 10 - 2 * κ) (fun n x => DefectIncrementBounds.remainders o base m h W n x i) := by
  obtain ⟨a₀, b₀, R₀, ha₀, _, _, _, hleft, hright, _⟩ := qLength_reference_bounds U ha hab
  have hfixed {f : CorrectionState.ScalarField Point} (hs : Support a b (qLength coord) U.carrier f) :
      ∀ n, PhysicalMeanDomain.SupportedOn a₀ b₀ U.carrier (f n) := by
    intro n x hx hn
    exact ⟨(hleft _ hx).trans (hs n x hx hn).1, (hs n x hx hn).2.trans (hright _ hx)⟩
  have hml : LocalRankDefect.LocalTriple a₀ b₀ U.carrier m :=
    ⟨⟨hmc.radial, hfixed hms.radial⟩, ⟨hmc.angular, hfixed hms.angular⟩, ⟨hmc.axial, hfixed hms.axial⟩⟩
  have hhl : LocalRankDefect.LocalTriple a₀ b₀ U.carrier h :=
    ⟨⟨hhc.radial, hfixed hhs.radial⟩, ⟨hhc.angular, hfixed hhs.angular⟩, ⟨hhc.axial, hfixed hhs.axial⟩⟩
  have hwl (i j : Fin 3) : LocalRankDefect.LocalShell a₀ b₀ U.carrier (W i j) :=
    ⟨hWc i j, hfixed (hWs i j)⟩
  have hrc := actualRadialError_mem ho hb hm hh hH W
    (fun i j n => (hWc i j n).mono (fun x hx =>
      ((movingStrip_domain U a b cL cR ha hcL hcR ε L hε hεone hL x).mp hx).1))
  have hrl := LocalRankDefect.actualRadialError_localShell ha₀ U.isOpen hbs hml hhl hop W hwl
  have hl : ContinuousOn (qLength coord) U.carrier :=
    ((qLength_contDiffOn U.coord_pos U.coord_lt_one).mono (fun x hx => U.time_pos x hx)).continuousOn
  have hrs : Support a b (qLength coord) U.carrier (actualRadialError o base m h W) :=
    ((gr_support U.isOpen hl o base (updated m h) W (hms.updated hhs) hWs).sub
      (gr_support U.isOpen hl o base m W hms hWs)).sub
      (((hhs.angular.mul_left base.angular).smul 2).mul_left o.invRadius)
  have hts : Support a b (qLength coord) U.carrier (thetaQuadratic m h) :=
    ((hms.axial.mul_right h.angular).add (hhs.axial.mul_right m.angular)).add
      (hhs.axial.mul_right h.angular)
  have hzs : Support a b (qLength coord) U.carrier (axialQuadratic m h) :=
    ((hms.axial.mul_right h.axial).smul 2).add (hhs.axial.mul_right h.axial)
  have hP := radialMoment_mem U ha hab hcL hcR ε L hε hεone hL hrl.smooth hrs hrc 0
  have hP2 := radialMoment_mem U ha hab hcL hcR ε L hε hεone hL hrl.smooth hrs hrc 2
  have hT := radialMoment_mem U ha hab hcL hcR ε L hε hεone hL
    (LocalRankDefect.thetaQuadratic_localShell hml hhl).smooth hts (thetaQuadratic_mem ho hm hh hH) 2
  have hZ := radialMoment_mem U ha hab hcL hcR ε L hε hεone hL
    (LocalRankDefect.axialQuadratic_localShell hml hhl).smooth hzs (axialQuadratic_mem ho hm hh hH) 1
  fin_cases i
  · exact hP
  · exact hT
  · exact Class.sub hZ (Class.smul hP2 (1 / 2))
end Remainders
end NavierStokes.MovingMomentBounds
end
end

-- REPLAY NavierStokes.PhysicalMeanDomain.meanClass_physicalCompact 2639 2691
run_cmd IO.println "BLOCK NavierStokes.PhysicalMeanDomain.meanClass_physicalCompact"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PhysicalMeanDomain
open Set Function MeasureTheory Filter
open scoped ContDiff Topology Interval BigOperators
open WeightedClasses WeightedRadialPrimitive
variable {S V : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
variable [CompleteSpace V]
open RadialPullback
variable {W : Type} [NormedAddCommGroup W] [NormedSpace ℝ W]
section LocalSmoothness
variable [FiniteDimensional ℝ S]
#count_heartbeats in
theorem meanClass_physicalCompact_R {a b d cL cR : ℝ}
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (U : Set S) (hU : IsOpen U) (α : ℝ) (M : ℕ → ℝ) (v : ℕ → PressureStream.Plane)
    (f : ℕ → PressureStream.Lift S → V)
    (hf : ∀ n, ContDiffOn ℝ ∞ (f n) (slowDomain U))
    (hs : ∀ n, SupportedOn a b U (f n))
    (hclass : MeanClass (localStripData a b cL cR ha hcL hcR ε L hε hεone hL U hU) α f) :
    MeanClass (localStripData a b cL cR ha hcL hcR ε L hε hεone hL U hU) α
      (fun n => physicalCompact d a b (M n) ((0 : S), v n) (f n)) := by
  refine ⟨hclass.weight_nonneg, ?_, ?_⟩
  · intro n
    exact (physicalCompact_contDiffOn ha hab hd (v n) hU (hf n) (hs n)).mono (fun _ hp => hp.2)
  · intro m
    obtain ⟨C, hC, k, hb⟩ := hclass.bounds m
    obtain ⟨K, hK, hbound⟩ := physicalCompact_finiteJets_fiber (S := S) (V := V) ha hab hd hcL hcR k m
    refine ⟨K * C, mul_nonneg hK hC, k, ?_⟩
    intro n p hp j hj
    obtain ⟨c, _, hcs, hcf, he⟩ := exists_fiber_localization hU hp.2 (hf n)
    have hA : 0 ≤ C * ε n ^ α * L n ^ k :=
      mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (hε n) α).le)
        (pow_nonneg (zero_le_one.trans (hL n)) _)
    have hin : ∀ i ≤ m, ∀ R ∈ Ioo a b, ∀ Y : PressureStream.Plane,
        ‖iteratedFDeriv ℝ i (localize c (f n)) (R, (p.2.1, Y))‖ ≤
          (C * ε n ^ α * L n ^ k) * logWeight cL cR a b k R := by
      intro i hi R hR Y
      rw [he.jet_eq i R Y]
      have h := hb n (R, (p.2.1, Y)) ⟨hR, hp.2⟩ i hi
      rwa [localStrip_majorant_eq ha hcL hcR ε L hε hεone hL U hU α C k n _ hR] at h
    have hout := hbound (M n) (v n) _ hcf (localize_supported hcs (hs n))
      (C * ε n ^ α * L n ^ k) hA p.2.1 hin p hp.1 rfl j hj
    rw [(physicalCompact_fiberLocal d a b (M n) (v n)).germ he |>.jet_eq j p.1 p.2.2] at hout
    rw [localStrip_majorant_eq ha hcL hcR ε L hε hεone hL U hU α (K * C) k n p hp.1]
    exact hout.trans_eq (by ring)
end LocalSmoothness
end NavierStokes.PhysicalMeanDomain
end
end

-- REPLAY NavierStokes.SignedStressPrimitive.momentDensity_meanClass 2695 2746
run_cmd IO.println "BLOCK NavierStokes.SignedStressPrimitive.momentDensity_meanClass"
section
set_option linter.all false
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology BigOperators
namespace NavierStokes.SignedStressPrimitive
section Primitive
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
#count_heartbeats in
theorem momentDensity_meanClass_R (P : Patch) (e : ℕ) {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (ε slow : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hε1 : ∀ n, ε n ≤ 1) (hslow : ∀ n, 1 ≤ slow n) :
    WeightedClasses.MeanClass
      (WeightedRadialPrimitive.logStripData P.a P.b cL cR P.a_pos hcL hcR ε slow hε hε1 hslow)
      0 (fun _ (z : ℝ × E) => momentDensity P e z.1) := by
  let s := WeightedRadialPrimitive.logStripData (E := E) P.a P.b cL cR P.a_pos hcL hcR ε slow hε hε1 hslow
  have hmem : ∀ r ∈ Icc P.left P.right, (r, (0 : E)) ∈ s.domain := by
    intro r hr
    exact ⟨P.a_lt_left.trans_le hr.1, hr.2.trans_lt P.right_lt_b⟩
  have hc : ContinuousOn (fun r => s.zeta (r, (0 : E))) (Icc P.left P.right) :=
    s.zeta_smooth.continuousOn.comp (continuous_id.prodMk continuous_const).continuousOn hmem
  have hp : ∀ r ∈ Icc P.left P.right, 0 < s.zeta (r, (0 : E)) := by
    intro r hr
    exact WeightedRadialPrimitive.zeta_pos cL cR
      (WeightedRadialPrimitive.logPosition_mem P.a_pos (hmem r hr))
  obtain ⟨D, hD, hDb⟩ := UniformCone.positive_uniform_margin isCompact_Icc hc hp
  have hs : RadialAlias.RadiallySupported P.left P.right (fun z : ℝ × E => momentDensity P e z.1) :=
    fun z hz => momentDensity_support P e hz
  refine ⟨fun _ z hz => s.zeta_nonneg z hz,
    fun _ => ((momentDensity_contDiff P e).comp contDiff_fst).contDiffOn, ?_⟩
  intro m
  obtain ⟨C, hC, hCb⟩ := WeightedRadialPrimitive.cutoff_finiteJet_bound (E := E)
    P.a P.b (momentDensity P e) (momentDensity_contDiff P e) m
  refine ⟨C / D, div_nonneg hC hD.le, 0, ?_⟩
  intro n z hz j hj
  change ‖iteratedFDeriv ℝ j (fun z : ℝ × E => momentDensity P e z.1) z‖ ≤
    WeightedClasses.majorant s (fun _ y => s.zeta y) 0 (C / D) 0 n z
  simp only [WeightedClasses.majorant, Real.rpow_zero, pow_zero, mul_one]
  by_cases hi : z.1 ∈ Icc P.left P.right
  · have hd : D ≤ s.zeta z := hDb z.1 hi
    calc
      _ ≤ C := hCb j hj z ⟨hz.1.le, hz.2.le⟩
      _ = (C / D) * D := by field_simp
      _ ≤ _ := mul_le_mul_of_nonneg_left hd (div_nonneg hC hD.le)
  · have hzj : iteratedFDeriv ℝ j (fun z : ℝ × E => momentDensity P e z.1) z = 0 := by
      by_contra hn
      exact hi (TransportPrimitive.iteratedFDeriv_supported hs j hn)
    rw [hzj, norm_zero]
    exact mul_nonneg (div_nonneg hC hD.le) (s.zeta_nonneg z hz)
end Primitive
end NavierStokes.SignedStressPrimitive
end
end

-- REPLAY NavierStokes.VariableGaugeMean.meanClass_scaledTemporalStreamBeta 2750 2905
run_cmd IO.println "BLOCK NavierStokes.VariableGaugeMean.meanClass_scaledTemporalStreamBeta"
section
set_option linter.all false
namespace NavierStokes.VariableGaugeMean
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval BigOperators
section Scale
end Scale
section Gauge
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Gauge
section ActualQ
open TorusInverse
end ActualQ
section AnchorReference
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end AnchorReference
section LocalGauge
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end LocalGauge
section IntegralJets
open WeightedRadialPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end IntegralJets
section StateConstructors
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end StateConstructors
section GaugeNaturality
open MeanChartCompatibility
variable {S T : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  [NormedAddCommGroup T] [NormedSpace ℝ T]
end GaugeNaturality
section ProductJets
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end ProductJets
section LocalQuantitative
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalQuantitative
section ActualChart
open TorusInverse MeanChartCompatibility
end ActualChart
open WeightedRadialPrimitive RadialPullback
section MovingSupport
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end MovingSupport
section ScaledIntegrals
variable {E V : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end ScaledIntegrals
section ScaledNormalization
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end ScaledNormalization
section VariableTransport
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end VariableTransport
section LocalComposition
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalComposition
section PhysicalTransportIdentity
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end PhysicalTransportIdentity
section QWeighted
open LocalSignedRequest
end QWeighted
section LocalWeighted
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end LocalWeighted
section MovingClasses
open LocalSignedRequest WeightedClasses
variable {coord a b d cL cR : ℝ} (U : SlowRegion coord)
variable (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingClasses
section Periodicity
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Periodicity
section MovingSupportClass
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingSupportClass
section FiberDerivatives
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end FiberDerivatives
section ActualIdentities
open LocalSignedRequest
variable {coord a b d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d)
include ha hab hd
end ActualIdentities
section AliasRepresentation
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end AliasRepresentation
section PressureChanges
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end PressureChanges
section MovingPressureChanges
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingPressureChanges
section MovingTemporal
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingTemporal
section TemporalLocal
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalLocal
section AliasClass
open LocalSignedRequest WeightedClasses
variable {coord a b d : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b) (hd : 0 < d)
include ha hab hd
variable {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end AliasClass
section MovingStageClasses
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
include hab hd
#count_heartbeats in
theorem meanClass_scaledTemporalStreamBeta_R {h α : ℝ} (hh : 0 ≤ h)
    (hscale : ∀ n, ChartScales.S n ≤ L n) (index : ℕ → ℕ) (D : ℕ)
    (hgap : ∀ n, ChartScales.nativeIndex h n ≤ index n + D) {f : ℕ → Point → ℝ}
    (hf : ∀ n, ContDiffOn ℝ ∞ (f n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hp : ∀ n, PhysicalMeanDomain.PeriodicOn U.carrier (f n))
    (hs : ∀ n, SupportedGauge a b (qLength coord) U.carrier (f n))
    (hclass : MeanClass (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) α f)
    (M : ℕ → ℝ) (v : ℕ → PressureStream.Plane) (w : PressureStream.Plane × PressureStream.Plane) :
    MeanClass (movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL) (α + 1)
      (fun n => PressureStream.streamBeta (ε n • w)
        (streamPotential d a b (M n) (qLength coord) (v n)
          (MeanChartCompatibility.temporalAtIndex h n (index n) (f n)))) := by
  let st := movingStripData U a b cL cR ha hcL hcR ε L hε hεone hL
  have hc := meanClass_temporalAtIndex_moving U ha hcL hcR ε L hε hεone hL hh hscale index D hgap hf hp hclass
  have hi := meanClass_streamBeta U ha hcL hcR ε L hε hεone hL hab hd
    (fun n => temporalAtIndex_contDiffOn h n (index n) U.isOpen (hf n) (hp n))
    (fun n => temporalAtIndex_supportedGauge h n (index n) (hs n)) hc M v w
  have hb : BandBound st 1 ε := by
    have he := bandBound_rpow st 1
    simp only [Real.rpow_one] at he
    exact he
  simpa only [streamBeta_smul_direction] using hi.band_smul hb
end MovingStageClasses
end
end NavierStokes.VariableGaugeMean
end

-- REPLAY NavierStokes.VariableGaugeMean.reconstructState_pressure_change_class 2909 3064
run_cmd IO.println "BLOCK NavierStokes.VariableGaugeMean.reconstructState_pressure_change_class"
section
set_option linter.all false
namespace NavierStokes.VariableGaugeMean
noncomputable section
open Set Function Filter MeasureTheory
open scoped ContDiff Topology Interval BigOperators
section Scale
end Scale
section Gauge
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Gauge
section ActualQ
open TorusInverse
end ActualQ
section AnchorReference
variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
end AnchorReference
section LocalGauge
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end LocalGauge
section IntegralJets
open WeightedRadialPrimitive
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end IntegralJets
section StateConstructors
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end StateConstructors
section GaugeNaturality
open MeanChartCompatibility
variable {S T : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  [NormedAddCommGroup T] [NormedSpace ℝ T]
end GaugeNaturality
section ProductJets
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
end ProductJets
section LocalQuantitative
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalQuantitative
section ActualChart
open TorusInverse MeanChartCompatibility
end ActualChart
open WeightedRadialPrimitive RadialPullback
section MovingSupport
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
  {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]
end MovingSupport
section ScaledIntegrals
variable {E V : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup V] [NormedSpace ℝ V]
end ScaledIntegrals
section ScaledNormalization
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end ScaledNormalization
section VariableTransport
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end VariableTransport
section LocalComposition
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end LocalComposition
section PhysicalTransportIdentity
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end PhysicalTransportIdentity
section QWeighted
open LocalSignedRequest
end QWeighted
section LocalWeighted
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end LocalWeighted
section MovingClasses
open LocalSignedRequest WeightedClasses
variable {coord a b d cL cR : ℝ} (U : SlowRegion coord)
variable (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingClasses
section Periodicity
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end Periodicity
section MovingSupportClass
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingSupportClass
section FiberDerivatives
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
variable [FiniteDimensional ℝ S]
end FiberDerivatives
section ActualIdentities
open LocalSignedRequest
variable {coord a b d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d)
include ha hab hd
end ActualIdentities
section AliasRepresentation
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end AliasRepresentation
section PressureChanges
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S]
end PressureChanges
section MovingPressureChanges
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingPressureChanges
section MovingTemporal
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end MovingTemporal
section TemporalLocal
variable {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] [FiniteDimensional ℝ S]
end TemporalLocal
section AliasClass
open LocalSignedRequest WeightedClasses
variable {coord a b d : ℝ} (U : SlowRegion coord) (ha : 0 < a) (hab : a < b) (hd : 0 < d)
include ha hab hd
variable {cL cR : ℝ} (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
end AliasClass
section MovingStageClasses
open LocalSignedRequest WeightedClasses
variable {coord a b cL cR d : ℝ} (U : SlowRegion coord)
    (ha : 0 < a) (hab : a < b) (hd : 0 < d) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
include hab hd
end MovingStageClasses
section ActualStateClasses
open LocalSignedRequest WeightedClasses
variable {coord cL cR : ℝ} (U : SlowRegion coord) (g : GaugeData PressureStream.Plane)
    (ha : 0 < g.radial.inner) (hd : 0 < g.radial.exponent) (hcL : 0 < cL) (hcR : 0 < cR)
    (ε L : ℕ → ℝ) (hε : ∀ n, 0 < ε n) (hεone : ∀ n, ε n ≤ 1) (hL : ∀ n, 1 ≤ L n)
    (hell : ∀ n, g.length n = qLength coord)
include hd hell
#count_heartbeats in
theorem reconstructState_pressure_change_class_R
    (c : CorrectionState.Context Point) (u v : CorrectionState.State Point) {α : ℝ}
    (hf : ∀ n, ContDiffOn ℝ ∞ (u.gr c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hg : ∀ n, ContDiffOn ℝ ∞ (v.gr c n) (PhysicalMeanDomain.slowDomain U.carrier))
    (hsf : ∀ n, SupportedGauge g.radial.inner g.radial.outer (qLength coord) U.carrier (u.gr c n))
    (hsg : ∀ n, SupportedGauge g.radial.inner g.radial.outer (qLength coord) U.carrier (v.gr c n))
    (hclass : MeanClass (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL)
      α (u.gr c - v.gr c)) :
    MeanClass (movingStripData U g.radial.inner g.radial.outer cL cR ha hcL hcR ε L hε hεone hL)
      α ((reconstructState g c u).pressure - (reconstructState g c v).pressure) := by
  have he := meanClass_meanPressure_change U ha g.radial.inner_lt_outer hd hcL hcR ε L hε hεone hL hf hg hsf hsg hclass
      g.radial.frequency (fun _ => g.radial.radialDirection)
  simp only [reconstructState, hell] at he ⊢
  exact he
end ActualStateClasses
end
end NavierStokes.VariableGaugeMean
end

-- REPLAY NavierStokes.WaveInteractionBounds.class_const_cmul 3068 3084
run_cmd IO.println "BLOCK NavierStokes.WaveInteractionBounds.class_const_cmul"
section
set_option linter.all false
namespace NavierStokes.WaveInteractionBounds
noncomputable section
open Set Filter WeightedClasses HarmonicCalculus
open scoped ContDiff Topology BigOperators
variable {D E F : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
#count_heartbeats in
theorem class_const_cmul_R {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ}
    {f : ℕ → D → ℂ} (hf : MemClass s w α f) (c : ℂ) :
    MemClass s w α (fun n x => c * f n x) :=
  hf.map (ContinuousLinearMap.mul ℝ ℂ c)
end
end NavierStokes.WaveInteractionBounds
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.band_smul 3088 3128
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.band_smul"
section
set_option linter.all false
namespace NavierStokes.WeightedClasses
noncomputable section
open scoped BigOperators ContDiff
variable {D E F G : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace MemClass
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {f g : ℕ → D → E}
#count_heartbeats in
theorem band_smul_R {a : ℕ → ℝ} (hf : MemClass s w α f) (ha : BandBound s β a) :
    MemClass s w (α + β) (fun n x => a n • f n x) := by
  obtain ⟨A, hA, p, ha⟩ := ha
  refine ⟨hf.weight_nonneg, fun n => (hf.smooth n).const_smul (a n), ?_⟩
  intro m
  obtain ⟨B, hB, q, hb⟩ := hf.bounds m
  refine ⟨A * B, mul_nonneg hA hB, p + q, ?_⟩
  intro n x hx j hj
  have han : ‖a n‖ ≤ majorant s (fun _ _ => 1) β A p n x := by
    apply (ha n).trans
    simp only [majorant, mul_one]
    apply mul_le_mul_of_nonneg_left
      (pow_le_pow_left₀ (zero_le_one.trans (s.one_le_slow n)) (s.slow_le_growth n x) p)
    exact mul_nonneg hA (Real.rpow_pos_of_pos (s.epsilon_pos n) β).le
  rw [iteratedFDeriv_const_smul_apply' (hf.contDiffAt n hx j)]
  rw [norm_smul (a n) (iteratedFDeriv ℝ j (f n) x)]
  calc
    _ ≤ majorant s (fun _ _ => 1) β A p n x * majorant s w α B q n x :=
      mul_le_mul han (hb n x hx j hj) (norm_nonneg _)
        (majorant_nonneg s (fun _ _ => 1) β hA p n x (by norm_num))
    _ = majorant s (fun n x => 1 * w n x) (β + α) (A * B) (p + q) n x :=
      majorant_mul s (fun _ _ => 1) w β α A B p q n x
    _ = _ := by simp only [majorant, one_mul, add_comm β α]
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mul 3132 3154
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.mul"
section
set_option linter.all false
namespace NavierStokes.WeightedClasses
noncomputable section
open scoped BigOperators ContDiff
variable {D E F G : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace MemClass
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {f g : ℕ → D → E}
#count_heartbeats in
theorem mul_R {a b : ℕ → D → ℝ} (ha : MemClass s w α a)
    (hb : MemClass s v β b) :
    MemClass s (fun n x => w n x * v n x) (α + β)
      (fun n x => a n x * b n x) := by
  simpa only [smul_eq_mul] using ha.smul hb
end MemClass
end
end NavierStokes.WeightedClasses
end

