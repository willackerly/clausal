import Tool
import F79
import NavierStokes.ActualPrimaryBounds
import NavierStokes.CorrectionInitialization
import NavierStokes.CurlClassBounds
import NavierStokes.HarmonicWaveInteraction
import NavierStokes.InitialPhysicalData
import NavierStokes.LabelSumBounds
import NavierStokes.LocalizedMeanInteraction
import NavierStokes.LocalizedWaveBounds
import NavierStokes.MeanBoundsReindex
import NavierStokes.SignedCopyBounds
import NavierStokes.UniformBlockBounds
import NavierStokes.UniformHarmonicInteraction
import NavierStokes.UniformPrimaryWeights
import NavierStokes.WeightedClasses
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.ActualPrimaryBounds.uniform_lift 21 64
run_cmd IO.println "BLOCK NavierStokes.ActualPrimaryBounds.uniform_lift"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualPrimaryBounds
open Set Function Filter WeightedClasses PhaseJetBounds PrimaryCopyBounds
open CorrectionInitialization
open scoped ContDiff Topology BigOperators
section NativeBounds
variable (B N0 : ℕ)
end NativeBounds
section CopyGeometry
variable {B N0 : ℕ}
end CopyGeometry
section NativeCopyEstimates
variable {B N0 : ℕ}
end NativeCopyEstimates
section ActualCopySums
variable {B N0 : ℕ}
end ActualCopySums
section InactiveBands
variable {B N0 : ℕ}
end InactiveBands
section LiteralCoefficients
variable {B N0 : ℕ}
#count_heartbeats in
theorem uniform_lift_R {D E ι : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup E] [NormedSpace ℝ E] {s : StripData D}
    {w : ι → ℕ → D → ℝ} {α : ℝ} {f : ι → ℕ → D → E}
    (hf : LabelSumBounds.UniformClass s w α f) :
    LabelSumBounds.UniformClass (HarmonicWaveInteraction.productStrip s)
      (fun l n x => w l n x.1) α (fun l n x => f l n x.1) := by
  refine ⟨fun l n x hx => hf.weight_nonneg l n x.1 hx,
    fun l n => (hf.each l |> HarmonicWaveInteraction.class_lift).smooth n, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, fun l n x hx j hj => ?_⟩
  have hd := HarmonicWaveInteraction.norm_jet_comp_linear s.isOpen_domain (hf.smooth l n)
    HarmonicWaveInteraction.projection hx j
  exact (hd.trans (mul_le_of_le_one_right (norm_nonneg _)
    (pow_le_one₀ (norm_nonneg _) HarmonicWaveInteraction.projection_norm))).trans (hb l n x.1 hx j hj)
end LiteralCoefficients
end NavierStokes.ActualPrimaryBounds
end
end

-- REPLAY NavierStokes.CorrectionInitialization.AssembledPrimary.conjugatePair_uniform 68 206
run_cmd IO.println "BLOCK NavierStokes.CorrectionInitialization.AssembledPrimary.conjugatePair_uniform"
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
#count_heartbeats in
theorem conjugatePair_uniform_R {s : StripData D} {w : ι → ℕ → D → ℝ} {α : ℝ}
    {f : ι → ℕ → D → ℂ} (hf : UniformClass s w α f) (j : ℤ) :
    UniformClass s w α (fun l n x => ErrorHarmonics.conjugatePair 1 (f l n) j x) := by
  exact UniformPrimaryWeights.uniform_of_pull (UniformPrimaryWeights.enumeration_surjective ι)
    (SignedWaveUpdate.conjugatePair_class
      (UniformPrimaryWeights.pull_class hf (UniformPrimaryWeights.enumeration ι)) j)
end AssembledPrimary
end NavierStokes.CorrectionInitialization
end
end

-- REPLAY NavierStokes.CurlClassBounds.class_neg 210 227
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

-- REPLAY NavierStokes.CurlClassBounds.class_sub 231 248
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

-- REPLAY NavierStokes.HarmonicWaveInteraction.class_pullback 252 277
run_cmd IO.println "BLOCK NavierStokes.HarmonicWaveInteraction.class_pullback"
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
theorem class_pullback_R {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ} {f : ℕ → D → F}
    (hf : MemClass s w α f) (L : E →L[ℝ] D) (hL : ‖L‖ ≤ 1) :
    MemClass (pullbackStrip s L) (fun n x => w n (L x)) α (fun n x => f n (L x)) := by
  refine ⟨fun n x hx => hf.weight_nonneg n (L x) hx,
    fun n => (hf.smooth n).comp L.contDiff.contDiffOn (fun _ hx => hx), ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro n x hx j hj
  have hc := norm_jet_comp_linear s.isOpen_domain (hf.smooth n) L hx j
  have hpow : ‖L‖ ^ j ≤ 1 := pow_le_one₀ (norm_nonneg L) hL
  exact (hc.trans (mul_le_of_le_one_right (norm_nonneg _) hpow)).trans (hb n (L x) hx j hj)
end NavierStokes.HarmonicWaveInteraction
end
end

-- REPLAY NavierStokes.HarmonicWaveInteraction.class_slice 281 303
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

-- REPLAY NavierStokes.InitialPhysicalData.sourceFamily_uniform 307 359
run_cmd IO.println "BLOCK NavierStokes.InitialPhysicalData.sourceFamily_uniform"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.InitialPhysicalData
open Set Function Filter WeightedClasses HarmonicCalculus
open CorrectionInitialization ActualPrimaryBounds
open scoped Topology ContDiff BigOperators
attribute [local instance] Classical.propDecidable
section NativePotential
variable {B N0 : ℕ}
end NativePotential
section GermBounds
variable {D E I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  {s : StripData D} {w : I → ℕ → D → ℝ} {α : ℝ}
  {f0 g0 : I → ℕ → D → E}
end GermBounds
section NativeCopies
variable {B N0 : ℕ}
end NativeCopies
section Labels
variable {B N0 : ℕ}
#count_heartbeats in
theorem sourceFamily_uniform_R {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {f : (SignedLabel B N0 × Frequency) → ℕ → LocalSignedRequest.Point → E}
    (hf : LabelSumBounds.UniformClass strip (fun _ _ x => Real.sqrt (strip.zeta x)) 1 f) :
    LabelSumBounds.UniformClass strip (fun (_ : SourceIndex) _ x => Real.sqrt (strip.zeta x)) 1
      (sourceFamily f) := by
  refine ⟨fun _ _ _ _ => Real.sqrt_nonneg _, ?_, ?_⟩
  · intro I n
    by_cases hn : n = I.1.1.val.1
    · cases hc : sourceChoice (B := B) (N0 := N0) I with
      | none => rw [sourceFamily_eq_zero _ _ _ (Or.inr hc)]; exact contDiffOn_const
      | some l => rw [sourceFamily_eq_some _ _ _ hn l hc]; exact hf.smooth l n
    · rw [sourceFamily_eq_zero _ _ _ (Or.inl hn)]; exact contDiffOn_const
  · intro m
    obtain ⟨C, hC, p, hb⟩ := hf.bounds m
    refine ⟨C, hC, p, ?_⟩
    intro I n x hx j hj
    have hz : (0 : ℝ) ≤ majorant strip (fun _ x => Real.sqrt (strip.zeta x)) 1 C p n x :=
      majorant_nonneg strip _ 1 hC p n x (Real.sqrt_nonneg _)
    by_cases hn : n = I.1.1.val.1
    · cases hc : sourceChoice (B := B) (N0 := N0) I with
      | none =>
          rw [sourceFamily_eq_zero _ _ _ (Or.inr hc)]
          simpa only [iteratedFDeriv_fun_zero, Pi.zero_apply, norm_zero] using hz
      | some l => rw [sourceFamily_eq_some _ _ _ hn l hc]; exact hb l n x hx j hj
    · rw [sourceFamily_eq_zero _ _ _ (Or.inl hn)]
      simpa only [iteratedFDeriv_fun_zero, Pi.zero_apply, norm_zero] using hz
end Labels
end NavierStokes.InitialPhysicalData
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.bilinear 363 406
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.bilinear"
section
set_option linter.all false
noncomputable section
open Set Function Filter
open scoped ContDiff Topology BigOperators
namespace NavierStokes.LabelSumBounds
open WeightedClasses
variable {ι κ E F G : Type*} {D : Type}
variable [NormedAddCommGroup D] [NormedSpace ℝ D]
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F]
variable [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace UniformClass
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β : ℝ}
variable {f g : ι → ℕ → D → E}
end UniformClass
namespace UniformClass
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β : ℝ}
variable {f : ι → ℕ → D → E} {g : ι → ℕ → D → F}
#count_heartbeats in
theorem bilinear_R (hf : UniformClass s w α f) (hg : UniformClass s v β g)
    (L : E →L[ℝ] F →L[ℝ] G) :
    UniformClass s (fun l n x => w l n x * v l n x) (α + β)
      (fun l n x => L (f l n x) (g l n x)) := by
  refine ⟨fun l n x hx => mul_nonneg (hf.weight_nonneg l n x hx) (hg.weight_nonneg l n x hx),
    fun l n => (L.contDiff.comp_contDiffOn (hf.smooth l n)).clm_apply (hg.smooth l n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hg.bounds m
  refine ⟨‖L‖ * 2 ^ m * A * B, by positivity, p + q, ?_⟩
  intro l n x hx j hj
  calc
    _ ≤ ‖L‖ * 2 ^ m * majorant s (w l) α A p n x * majorant s (v l) β B q n x :=
      bilinear_jet_bound L s.isOpen_domain (hf.smooth l n) (hg.smooth l n) hx hj
        (majorant_nonneg s (w l) α hA p n x (hf.weight_nonneg l n x hx))
        (majorant_nonneg s (v l) β hB q n x (hg.weight_nonneg l n x hx))
        (ha l n x hx) (hb l n x hx)
    _ = (‖L‖ * 2 ^ m) *
        (majorant s (w l) α A p n x * majorant s (v l) β B q n x) := by ring
    _ = _ := by rw [majorant_mul]; unfold majorant; ring
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.map 410 443
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.map"
section
set_option linter.all false
noncomputable section
open Set Function Filter
open scoped ContDiff Topology BigOperators
namespace NavierStokes.LabelSumBounds
open WeightedClasses
variable {ι κ E F G : Type*} {D : Type}
variable [NormedAddCommGroup D] [NormedSpace ℝ D]
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F]
variable [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace UniformClass
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β : ℝ}
variable {f g : ι → ℕ → D → E}
#count_heartbeats in
theorem map_R (hf : UniformClass s w α f) (L : E →L[ℝ] F) :
    UniformClass s w α (fun l n x => L (f l n x)) := by
  refine ⟨hf.weight_nonneg, fun l n => (hf.smooth l n).continuousLinearMap_comp L, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨‖L‖ * C, mul_nonneg (norm_nonneg _) hC, p, ?_⟩
  intro l n x hx j hj
  change ‖iteratedFDeriv ℝ j (L ∘ f l n) x‖ ≤ _
  rw [L.iteratedFDeriv_comp_left ((hf.each l).contDiffAt n hx j) le_rfl]
  calc
    _ ≤ ‖L‖ * ‖iteratedFDeriv ℝ j (f l n) x‖ := L.norm_compContinuousMultilinearMap_le _
    _ ≤ ‖L‖ * majorant s (w l) α C p n x := mul_le_mul_of_nonneg_left
      (hb l n x hx j hj) (norm_nonneg _)
    _ = _ := by unfold majorant; ring
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.neg 447 470
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.neg"
section
set_option linter.all false
noncomputable section
open Set Function Filter
open scoped ContDiff Topology BigOperators
namespace NavierStokes.LabelSumBounds
open WeightedClasses
variable {ι κ E F G : Type*} {D : Type}
variable [NormedAddCommGroup D] [NormedSpace ℝ D]
variable [NormedAddCommGroup E] [NormedSpace ℝ E]
variable [NormedAddCommGroup F] [NormedSpace ℝ F]
variable [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace UniformClass
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β : ℝ}
variable {f g : ι → ℕ → D → E}
#count_heartbeats in
theorem neg_R (hf : UniformClass s w α f) :
    UniformClass s w α (fun l n x => -f l n x) := by
  simpa only [_root_.neg_apply, ContinuousLinearMap.id_apply] using
    hf.map (-(ContinuousLinearMap.id ℝ E))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LocalizedMeanInteraction.local_cmul 474 493
run_cmd IO.println "BLOCK NavierStokes.LocalizedMeanInteraction.local_cmul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedMeanInteraction
open Set Function Filter WeightedClasses HarmonicCalculus HarmonicFields
open LocalizedWaveBounds WaveInteractionBounds HarmonicMeanInteraction
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} {I E : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
#count_heartbeats in
theorem local_cmul_R {s : StripData D} {C : ℕ → I → Set D}
    {w v : ℕ → I → D → ℝ} {α β : ℝ} {f g : ℕ → I → D → ℂ}
    (hf : LocalClass s C w α f) (hg : LocalClass s C v β g) :
    LocalClass s C (fun n l x => w n l x * v n l x) (α + β)
      (fun n l x => f n l x * g n l x) :=
  hf.bilinear hg (ContinuousLinearMap.mul ℝ ℂ)
end NavierStokes.LocalizedMeanInteraction
end
end

-- REPLAY NavierStokes.LocalizedMeanInteraction.local_div_radius 497 517
run_cmd IO.println "BLOCK NavierStokes.LocalizedMeanInteraction.local_div_radius"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedMeanInteraction
open Set Function Filter WeightedClasses HarmonicCalculus HarmonicFields
open LocalizedWaveBounds WaveInteractionBounds HarmonicMeanInteraction
open scoped Topology ContDiff BigOperators ComplexConjugate
variable {D : Type} {I E : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
#count_heartbeats in
theorem local_div_radius_R {s : StripData D} {C : ℕ → I → Set D}
    {w : ℕ → I → D → ℝ} {α κ : ℝ} (G : Geometry s κ)
    {f : ℕ → I → D → ℂ} (hf : LocalClass s C w α f) :
    LocalClass s C w α (fun n l x => f n l x / (G.radius n x : ℂ)) := by
  have hi : LocalUnweighted s C 0 (fun n _ x => ((G.radius n x : ℂ))⁻¹) :=
    LocalClass.of_global (inverse_radius_complex G)
  simpa only [zero_add, one_mul, mul_one, div_eq_mul_inv, mul_comm] using local_cmul hi hf
end NavierStokes.LocalizedMeanInteraction
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.Dr_mem 521 558
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.Dr_mem"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
end LocalClass
section ElementaryOperations
variable {s : StripData D} {K : ℕ → I → Set D} {w : ℕ → I → D → ℝ} {α β : ℝ}
end ElementaryOperations
section Derivatives
variable {s : StripData D} {K : ℕ → I → Set D} {w : ℕ → I → D → ℝ}
  {α κ : ℝ}
#count_heartbeats in
theorem Dr_mem_R (d : GraphDirections D) {f : ℕ → I → D → E} (hf : LocalClass s K w α f)
    (hρ : LocalUnweighted s K 0 (fun _ _ => d.radialProfile))
    (hM : BandBound s (-κ) d.radialScale) (hκ : 0 ≤ κ) :
    LocalClass s K w (α - κ) (Dr d f) := by
  have he := (hf.directional d.radial).mono_exponent (sub_le_self α hκ)
  have hv := (unweighted_smul hρ (hf.directional d.auxiliary)).band_smul hM
  have hv' : LocalClass s K w (α - κ) (fun n i x =>
      d.radialScale n • (d.radialProfile x • fderiv ℝ (f n i) x d.auxiliary)) := by
    simpa only [zero_add, sub_eq_add_neg] using hv
  apply (he.add hv').congr
  intro n i x
  simp [Dr, GraphDirections.radialField, along]
end Derivatives
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.band_smul 562 586
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.band_smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem band_smul_R {r : ℕ → ℝ} (hf : LocalClass s K w α f)
    (hr : BandBound s β r) :
    LocalClass s K w (α + β) (fun n i x => r n • f n i x) := by
  have hc : UnweightedClass s β (fun n (_ : D) => r n) := by
    simpa only [smul_eq_mul, mul_one, zero_add] using (unweighted_const s (1 : ℝ)).band_smul hr
  simpa only [one_mul, add_comm β α] using (LocalClass.of_global hc (K := K)).smul hf
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.fderiv 590 616
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.fderiv"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem fderiv_R (hf : LocalClass s K w α f) :
    LocalClass s K w α (fun n i => _root_.fderiv ℝ (f n i)) := by
  refine ⟨hf.weight_nonneg, fun n i x hx hi => (hf.smooth n i x hx hi).fderiv_right (by simp),
    fun m => ?_⟩
  obtain ⟨C, hC, p, hb⟩ := hf.bounds (m + 1)
  refine ⟨C, hC, p, fun n i x hx hi j hj => ?_⟩
  rw [norm_iteratedFDeriv_fderiv]
  exact hb n i x hx hi (j + 1) (Nat.add_le_add_right hj 1)
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.mul 620 643
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.mul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem mul_R {a b : ℕ → I → D → ℝ} (ha : LocalClass s K w α a)
    (hb : LocalClass s K v β b) :
    LocalClass s K (fun n i x => w n i x * v n i x) (α + β)
      (fun n i x => a n i x * b n i x) := by
  simpa only [smul_eq_mul] using ha.smul hb
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.neg 647 668
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.neg"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem neg_R (hf : LocalClass s K w α f) : LocalClass s K w α (fun n i x => -f n i x) := by
  simpa only [_root_.neg_apply, ContinuousLinearMap.id_apply] using
    hf.map (-ContinuousLinearMap.id ℝ E)
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.smul 672 695
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem smul_R {r : ℕ → I → D → ℝ} (hr : LocalClass s K v β r)
    (hf : LocalClass s K w α f) :
    LocalClass s K (fun n i x => v n i x * w n i x) (β + α)
      (fun n i x => r n i x • f n i x) :=
  hr.bilinear hf (ContinuousLinearMap.lsmul ℝ ℝ)
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.sub 699 720
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.sub"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LocalizedWaveBounds
open Set Function Filter WeightedClasses HarmonicCalculus LinearWaveBounds
open scoped Topology ContDiff BigOperators InnerProductSpace
variable {D E F G I : Type*}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
namespace LocalClass
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → I → D → ℝ}
  {α β : ℝ} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem sub_R (hf : LocalClass s K w α f) (hg : LocalClass s K w α g) :
    LocalClass s K w α (fun n i x => f n i x - g n i x) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.MeanBoundsReindex.uniformClass_return 724 743
run_cmd IO.println "BLOCK NavierStokes.MeanBoundsReindex.uniformClass_return"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.MeanBoundsReindex
open Set Function Filter WeightedClasses LabelSumBounds
open scoped ContDiff Topology
variable {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
#count_heartbeats in
theorem uniformClass_return_R {F ι : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F]
    (e : D ≃ₗᵢ[ℝ] E) {s : StripData D} {w : ι → ℕ → D → ℝ} {α : ℝ}
    {f : ι → ℕ → E → F}
    (hf : UniformClass (ParticularWaveBounds.reindexStrip e.symm s)
      (fun l n y => w l n (e.symm y)) α f) :
    UniformClass s w α (fun l n x => f l n (e x)) := by
  have hh := UniformBlockBounds.uniform_reindex e hf
  simpa only [strip_roundtrip, e.symm_apply_apply] using hh
end NavierStokes.MeanBoundsReindex
end
end

-- REPLAY NavierStokes.SignedCopyBounds.NativeCovariance.increment_jets 747 788
run_cmd IO.println "BLOCK NavierStokes.SignedCopyBounds.NativeCovariance.increment_jets"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SignedCopyBounds
open Set Function Filter WeightedClasses PeriodizedWaveBounds
open scoped ContDiff Topology BigOperators
variable {D E F G I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
section LocalOperations
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → D → ℝ} {α β : ℝ}
end LocalOperations
section QuotientAt
open WeightedQuotients
end QuotientAt
section LocalQuotient
variable {s : StripData D} {K : ℕ → I → Set D} {w : ℕ → D → ℝ}
  {g r : ℕ → I → D → ℝ}
end LocalQuotient
namespace NativeCovariance
variable {s : StripData D} {K : ℕ → I → Set D}
  {H : I → ℕ → D → Mat2} {T : I → ℕ → D → Vec2} (h : NativeCovariance s K H T)
include h
#count_heartbeats in
theorem increment_jets_R {R : I → ℕ → D → Vec2} {β : ℝ}
    (hR : ∀ a, LocalJets s (fun _ x => s.zeta x) β K (fun n i x => R i n x a)) (j : Fin 2) :
    LocalJets s (fun _ x => Real.sqrt (s.zeta x)) β K
      (fun n i x => SignedCovariance.increment (H i n x) (T i n x) (R i n x) j) := by
  have hg := h.weights_jets (fun _ x hx => s.zeta_nonneg x hx) h.target_jets j
  have hr := h.weights_jets (fun _ x hx => s.zeta_nonneg x hx) hR j
  have hq := local_signed_quotient (fun _ x hx => h.zeta_pos x hx) hg hr h.lower_pos
    (fun n i x hx hi => h.lower n i x hx hi j)
  apply local_congr hq
  intro n i x hx hi
  filter_upwards [h.det_eventually n i hx hi] with y hy
  simp only [SignedCovariance.increment, SmoothCovariance.amplitudes,
    SmoothCovariance.inverse_formula _ _ hy]
end NativeCovariance
end NavierStokes.SignedCopyBounds
end
end

-- REPLAY NavierStokes.SignedCopyBounds.local_band_smul 792 818
run_cmd IO.println "BLOCK NavierStokes.SignedCopyBounds.local_band_smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SignedCopyBounds
open Set Function Filter WeightedClasses PeriodizedWaveBounds
open scoped ContDiff Topology BigOperators
variable {D E F G I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
section LocalOperations
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → D → ℝ} {α β : ℝ}
#count_heartbeats in
theorem local_band_smul_R {r : ℕ → ℝ} {f : ℕ → I → D → E}
    (hf : LocalJets s w α K f) (hr : BandBound s β r)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w (α + β) K (fun n i x => r n • f n i x) := by
  have hc : LocalJets s (fun _ _ => 1) β K (fun n _ (_ : D) => r n) := by
    apply LocalJets.of_memClass
    simpa using (unweighted_const s (1 : ℝ)).band_smul hr
  have hh := hc.bilinear hf (ContinuousLinearMap.lsmul ℝ ℝ) (fun _ _ _ => zero_le_one) hw
  simp only [one_mul, add_comm] at hh
  exact hh
end LocalOperations
end NavierStokes.SignedCopyBounds
end
end

-- REPLAY NavierStokes.SignedCopyBounds.local_indexed_band_smul 822 858
run_cmd IO.println "BLOCK NavierStokes.SignedCopyBounds.local_indexed_band_smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SignedCopyBounds
open Set Function Filter WeightedClasses PeriodizedWaveBounds
open scoped ContDiff Topology BigOperators
variable {D E F G I : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
section LocalOperations
variable {s : StripData D} {K : ℕ → I → Set D} {w v : ℕ → D → ℝ} {α β : ℝ}
#count_heartbeats in
theorem local_indexed_band_smul_R {r : I → ℕ → ℝ} {f : ℕ → I → D → E}
    (hf : LocalJets s w α K f) (hr : UniformPrimaryWeights.UniformBandBound s β r)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w (α + β) K (fun n i x => r i n • f n i x) := by
  obtain ⟨C, hC, p, hb⟩ := hr
  have hc : LocalJets s (fun _ _ => 1) β K (fun n i (_ : D) => r i n) := by
    refine ⟨fun _ _ _ _ _ => contDiffAt_const, fun _ => ⟨C, hC, p, ?_⟩⟩
    intro n i x hx hi j hj
    by_cases hj0 : j = 0
    · subst j
      rw [norm_iteratedFDeriv_zero]
      simp only [majorant, mul_one]
      exact (hb i n).trans (mul_le_mul_of_nonneg_left
        (pow_le_pow_left₀ (zero_le_one.trans (s.one_le_slow n)) (s.slow_le_growth n x) p)
        (mul_nonneg hC (Real.rpow_pos_of_pos (s.epsilon_pos n) β).le))
    · rw [iteratedFDeriv_const_of_ne hj0]
      simpa only [Pi.zero_apply, norm_zero] using majorant_nonneg s (fun _ _ => 1) β hC p n x zero_le_one
  have hh := hc.bilinear hf (ContinuousLinearMap.lsmul ℝ ℝ) (fun _ _ _ => zero_le_one) hw
  simp only [one_mul, add_comm] at hh
  exact hh
end LocalOperations
end NavierStokes.SignedCopyBounds
end
end

-- REPLAY NavierStokes.UniformBlockBounds.block_velocity_reindex 862 909
run_cmd IO.println "BLOCK NavierStokes.UniformBlockBounds.block_velocity_reindex"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformBlockBounds
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open scoped Topology ContDiff BigOperators
section Restriction
variable {D E : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
end Restriction
section ZeroSection
variable {D : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end ZeroSection
section Pairing
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {s : StripData D} {w : ι → ℕ → D → ℝ} {α γ : ℝ}
end Pairing
section SignedBlocks
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {s : StripData (D × ℝ)} {w : ι → ℕ → D × ℝ → ℝ} {α γ : ℝ}
end SignedBlocks
section ProductSignedBlocks
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {s : StripData D} {P : ι → ℕ → D → ℝ} {α γ : ℝ}
end ProductSignedBlocks
section FiniteAssembly
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {s : StripData D} {w : ι → ℕ → D → ℝ} {α γ : ℝ}
end FiniteAssembly
section NativeAssembly
variable {Q : Type} {ι F : Type*} [NormedAddCommGroup Q] [NormedSpace ℝ Q]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
end NativeAssembly
section StateReindex
variable {D E : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
#count_heartbeats in
theorem block_velocity_reindex_R (e : D ≃ₗᵢ[ℝ] E) {s : StripData E}
    {w : ι → ℕ → E → ℝ} {α : ℝ} {a : ι → CorrectionState.HarmonicBlock E}
    (i : Fin 3) (j : ℤ) (ha : UniformClass s w α (fun l n x => (a l).velocity n i j x)) :
    UniformClass (StateReindex.strip e s) (fun l n x => w l n (e x)) α
      (fun l n x => (StateReindex.block e (a l)).velocity n i j x) :=
  uniform_reindex e ha
end StateReindex
end NavierStokes.UniformBlockBounds
end
end

-- REPLAY NavierStokes.UniformBlockBounds.uniform_slice 913 938
run_cmd IO.println "BLOCK NavierStokes.UniformBlockBounds.uniform_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformBlockBounds
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open scoped Topology ContDiff BigOperators
section Restriction
variable {D E : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
end Restriction
section ZeroSection
variable {D : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
#count_heartbeats in
theorem uniform_slice_R {s : StripData D} {w : ι → ℕ → D → ℝ} {α : ℝ}
    {f : ι → ℕ → D × ℝ → F}
    (hf : UniformClass (HarmonicWaveInteraction.productStrip s)
      (fun l n x => w l n x.1) α f) :
    UniformClass s w α (fun l n x => f l n (x,0)) := by
  have hh := uniform_zeroSection hf
  rw [sectionStrip_productStrip] at hh
  exact hh
end ZeroSection
end NavierStokes.UniformBlockBounds
end
end

-- REPLAY NavierStokes.UniformBlockBounds.uniform_zeroSection 942 973
run_cmd IO.println "BLOCK NavierStokes.UniformBlockBounds.uniform_zeroSection"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformBlockBounds
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open scoped Topology ContDiff BigOperators
section Restriction
variable {D E : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
end Restriction
section ZeroSection
variable {D : Type} {F ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
#count_heartbeats in
theorem uniform_zeroSection_R {s : StripData (D × ℝ)} {w : ι → ℕ → D × ℝ → ℝ}
    {α : ℝ} {f : ι → ℕ → D × ℝ → F} (hf : UniformClass s w α f) :
    UniformClass (SignedWaveUpdate.sectionStrip s) (fun l n x => w l n (x,0)) α
      (fun l n x => f l n (x,0)) := by
  refine ⟨fun l n x hx => hf.weight_nonneg l n _ hx,
    fun l n => (hf.smooth l n).comp (SignedWaveUpdate.zeroSection (D := D)).contDiff.contDiffOn
      (fun _ hx => hx), fun m => ?_⟩
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, fun l n x hx j hj => ?_⟩
  have hc := PhaseJetBounds.norm_jet_comp_linear s.isOpen_domain (hf.smooth l n)
    (SignedWaveUpdate.zeroSection (D := D)) hx j
  have hp : ‖SignedWaveUpdate.zeroSection (D := D)‖^j ≤ 1 :=
    pow_le_one₀ (norm_nonneg _) SignedWaveUpdate.zeroSection_norm_le
  exact (hc.trans (mul_le_of_le_one_right (norm_nonneg _) hp)).trans (hb l n (x,0) hx j hj)
end ZeroSection
end NavierStokes.UniformBlockBounds
end
end

-- REPLAY NavierStokes.UniformHarmonicInteraction.cmul 977 996
run_cmd IO.println "BLOCK NavierStokes.UniformHarmonicInteraction.cmul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformHarmonicInteraction
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open WaveInteractionBounds HarmonicMeanInteraction HarmonicWaveInteraction
open scoped Topology ContDiff BigOperators
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
section UniformAlgebra
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β κ : ℝ}
#count_heartbeats in
theorem cmul_R {f g : ι → ℕ → D → ℂ} (hf : UniformClass s w α f)
    (hg : UniformClass s v β g) :
    UniformClass s (fun l n x => w l n x * v l n x) (α+β)
      (fun l n x => f l n x * g l n x) :=
  hf.bilinear hg (ContinuousLinearMap.mul ℝ ℂ)
end UniformAlgebra
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.UniformHarmonicInteraction.div_radius 1000 1018
run_cmd IO.println "BLOCK NavierStokes.UniformHarmonicInteraction.div_radius"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformHarmonicInteraction
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open WaveInteractionBounds HarmonicMeanInteraction HarmonicWaveInteraction
open scoped Topology ContDiff BigOperators
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
section UniformAlgebra
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β κ : ℝ}
#count_heartbeats in
theorem div_radius_R (G : Geometry s κ) {f : ι → ℕ → D → ℂ} (hf : UniformClass s w α f) :
    UniformClass s w α (fun l n x => f l n x / (G.radius n x : ℂ)) := by
  simpa only [mul_one, add_zero, div_eq_mul_inv] using
    cmul hf (UniformPrimaryWeights.class_of_single (inverse_radius_complex G))
end UniformAlgebra
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.UniformHarmonicInteraction.strippedDivergence_uniform 1022 1051
run_cmd IO.println "BLOCK NavierStokes.UniformHarmonicInteraction.strippedDivergence_uniform"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformHarmonicInteraction
open Set Filter Function WeightedClasses LabelSumBounds HarmonicCalculus HarmonicFields
open WaveInteractionBounds HarmonicMeanInteraction HarmonicWaveInteraction
open scoped Topology ContDiff BigOperators
variable {D : Type} {ι : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
section UniformAlgebra
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β κ : ℝ}
#count_heartbeats in
theorem strippedDivergence_uniform_R (G : Geometry s κ) (hκ : 0 ≤ κ)
    {a : ι → Family D} (ha : ∀ i, UniformClass s w α (fun l n x => a l n x i)) :
    UniformClass s w (α-κ)
      (fun l n => strippedDivergence (G.radius n) (G.radial n) (G.axial n) (a l n)) := by
  have hr : UniformClass s w (α-κ) (fun l n => along (G.radial n) (fun x => a l n x 0)) := by
    simpa only [sub_eq_add_neg] using UniformPrimaryWeights.along_class
      (UniformPrimaryWeights.class_of_single G.radial_class) (ha 0)
  have hc := (div_radius G (ha 0)).mono_exponent (show α-κ ≤ α by linarith)
  have hz := (UniformPrimaryWeights.along_class
    (UniformPrimaryWeights.class_of_single G.axial_class) (ha 2)).mono_exponent
      (show α-κ ≤ α+1 by linarith)
  apply ((hr.add hc).add hz).congr
  intro l n x hx
  simp only [strippedDivergence, Complex.real_smul, Complex.ofReal_inv, div_eq_mul_inv]
  ring
end UniformAlgebra
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.UniformPrimaryWeights.fderiv_class 1055 1085
run_cmd IO.println "BLOCK NavierStokes.UniformPrimaryWeights.fderiv_class"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.UniformPrimaryWeights
open Set Function Filter WeightedClasses LabelSumBounds
open scoped ContDiff Topology BigOperators
variable {ι E F G : Type*} {D : Type}
  [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
section WeightedOperations
variable [Countable ι] [Nonempty ι]
  {s : StripData D} {w g r : ι → ℕ → D → ℝ} {β : ℝ}
end WeightedOperations
section Calculus
variable {s : StripData D} {w v : ι → ℕ → D → ℝ} {α β : ℝ}
#count_heartbeats in
theorem fderiv_class_R {f : ι → ℕ → D → E} (hf : UniformClass s w α f) :
    UniformClass s w α (fun l n => fderiv ℝ (f l n)) := by
  refine ⟨hf.weight_nonneg, fun l n =>
    (contDiffOn_infty_iff_fderiv_of_isOpen s.isOpen_domain).mp (hf.smooth l n) |>.2, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds (m + 1)
  refine ⟨C, hC, p, fun l n x hx j hj => ?_⟩
  rw [norm_iteratedFDeriv_fderiv]
  exact hb l n x hx (j + 1) (Nat.add_le_add_right hj 1)
end Calculus
end NavierStokes.UniformPrimaryWeights
end
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.band_smul 1089 1129
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

-- REPLAY NavierStokes.WeightedClasses.MemClass.fderiv 1133 1161
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.fderiv"
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
theorem fderiv_R (hf : MemClass s w α f) :
    MemClass s w α (fun n => _root_.fderiv ℝ (f n)) := by
  refine ⟨hf.weight_nonneg, ?_, ?_⟩
  · intro n
    exact (contDiffOn_infty_iff_fderiv_of_isOpen s.isOpen_domain).mp (hf.smooth n) |>.2
  · intro m
    obtain ⟨C, hC, p, h⟩ := hf.bounds (m + 1)
    refine ⟨C, hC, p, ?_⟩
    intro n x hx j hj
    rw [norm_iteratedFDeriv_fderiv]
    exact h n x hx (j + 1) (Nat.add_le_add_right hj 1)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.graphDerivative 1165 1195
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.graphDerivative"
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
end MemClass
#count_heartbeats in
theorem MemClass.graphDerivative_R {s : StripData D} {w : ℕ → D → ℝ}
    {α κ : ℝ} {f : ℕ → D → E} {M : ℕ → ℝ} {a : D → ℝ}
    (hf : MemClass s w α f) (ha : UnweightedClass s 0 (fun _ => a))
    (hM : BandBound s (-κ) M) (hκ : 0 ≤ κ) (e v : D) :
    MemClass s w (α - κ) (graphDerivative M a e v f) := by
  have he : MemClass s w (α - κ) (fun n x => _root_.fderiv ℝ (f n) x e) :=
    (hf.directional e).mono_exponent (sub_le_self α hκ)
  have hv : MemClass s w α (fun n x => a x • _root_.fderiv ℝ (f n) x v) := by
    simpa only [zero_add, one_mul] using MemClass.smul ha (hf.directional v)
  have hmv : MemClass s w (α - κ)
      (fun n x => M n • (a x • _root_.fderiv ℝ (f n) x v)) := by
    simpa only [sub_eq_add_neg] using hv.band_smul hM
  exact he.add hmv
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.map 1199 1231
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.map"
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
theorem map_R (hf : MemClass s w α f) (L : E →L[ℝ] F) :
    MemClass s w α (fun n x => L (f n x)) := by
  refine ⟨hf.weight_nonneg, fun n => (hf.smooth n).continuousLinearMap_comp L, ?_⟩
  intro m
  obtain ⟨C, hC, p, h⟩ := hf.bounds m
  refine ⟨‖L‖ * C, mul_nonneg (norm_nonneg _) hC, p, ?_⟩
  intro n x hx j hj
  change ‖iteratedFDeriv ℝ j (L ∘ f n) x‖ ≤ _
  rw [L.iteratedFDeriv_comp_left (hf.contDiffAt n hx j) le_rfl]
  calc
    _ ≤ ‖L‖ * ‖iteratedFDeriv ℝ j (f n) x‖ :=
      L.norm_compContinuousMultilinearMap_le _
    _ ≤ ‖L‖ * majorant s w α C p n x :=
      mul_le_mul_of_nonneg_left (h n x hx j hj) (norm_nonneg _)
    _ = _ := by unfold majorant; ring
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mul 1235 1257
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

