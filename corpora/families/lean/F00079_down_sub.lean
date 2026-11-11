import Tool
import F79
import NavierStokes.ActualCurrentParticularPhysical
import NavierStokes.ActualInitialExcluded
import NavierStokes.BaseRadialJets
import NavierStokes.LabelSumBounds
import NavierStokes.LinearWaveBounds
import NavierStokes.LocalizedWaveBounds
import NavierStokes.SignedCopyBounds
import NavierStokes.UniformBlockBounds
import NavierStokes.UniformHarmonicInteraction
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.UniformBlockBounds.pair_uniform 16 50
run_cmd IO.println "BLOCK NavierStokes.UniformBlockBounds.pair_uniform"
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
#count_heartbeats in
theorem pair_uniform_R {a : ι → ℕ → D → ℂ} (ha : UniformClass s w α a) (j m : ℤ) :
    UniformClass s w α (fun l n x => ErrorHarmonics.conjugatePair j (a l n) m x) := by
  have hp : UniformClass s w α (fun l n x => a l n x / 2) := by
    simpa only [ContinuousLinearMap.mul_apply', div_eq_mul_inv, mul_comm] using
      ha.map (ContinuousLinearMap.mul ℝ ℂ (2 : ℂ)⁻¹)
  have hn : UniformClass s w α (fun l n x => (starRingEnd ℂ) (a l n x / 2)) :=
    hp.map (Complex.conjCLE : ℂ →L[ℝ] ℂ)
  have hz := UniformClass.zero (s := s) (α := α) (E := ℂ) ha.weight_nonneg
  by_cases hm : m = j <;> by_cases hm' : -m = j
  · simpa only [ParticularWaveAssembly.pair_apply, ite_eq_left hm, ite_eq_left hm'] using hp.add hn
  · simpa only [ParticularWaveAssembly.pair_apply, ite_eq_left hm, ite_eq_right hm', map_zero, add_zero] using hp
  · simpa only [ParticularWaveAssembly.pair_apply, ite_eq_right hm, ite_eq_left hm', zero_add] using hn
  · simpa only [ParticularWaveAssembly.pair_apply, ite_eq_right hm, ite_eq_right hm', map_zero, add_zero] using hz
end Pairing
end NavierStokes.UniformBlockBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.reindex 54 79
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.reindex"
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
theorem reindex_R (hf : UniformClass s w α f) (a : κ → ι) :
    UniformClass s (fun l => w (a l)) α (fun l => f (a l)) := by
  refine ⟨fun l => hf.weight_nonneg (a l), fun l => hf.smooth (a l), ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  exact ⟨C, hC, p, fun l => hb (a l)⟩
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.ActualCurrentParticularPhysical.nativePressure_re_contDiffOn 83 113
run_cmd IO.println "BLOCK NavierStokes.ActualCurrentParticularPhysical.nativePressure_re_contDiffOn"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualCurrentParticularPhysical
open Set Function Filter ProblemStatement HarmonicCalculus
open CorrectionState CorrectionStep CorrectionInitialization
open scoped Topology ContDiff BigOperators
variable {B N0 : ℕ}
#count_heartbeats in
theorem nativePressure_re_contDiffOn_R (x : CycleState (Label B N0)) (l : Label B N0)
    (j : ℤ) (hphase : (copyData x l j).background.phase =
      (ActualParticularStageControls.background l).phase) {β : ℝ}
    (hp : WeightedClasses.MemClass ActualWaveRegularityData.particularFullStrip
      (fun _ z => Real.sqrt (ActualWaveRegularityData.particularFullStrip.zeta z)) β
      (copyData x l j).common.pressure)
    (hz : RawBoundaryZero x l j) (n : ℕ) :
    ContDiffOn ℝ ∞ (fun z => (nativePressure x l j n z).re) nativeDomain := by
  have hs := ActualWaveRegularityData.particular_mode_pressure_smooth l
    (ActualParticularStageControls.assembly x l).context
    (ActualParticularStageControls.assembly x l).state
    (ActualParticularStageControls.assembly x l).carrierBlock
    (ActualParticularStageControls.assembly x l).gaussianInput
    (ActualParticularStageControls.assembly x l).aliasInput j hphase hp
    (fun m z hm hr => (hz m z hm hr).2) n
  have he := hs.comp ActualWaveRegularity.particularChart.symm.contDiff.contDiffOn
    (fun _ hx => hx)
  simp only [Function.comp_def, LinearIsometryEquiv.apply_symm_apply] at he
  exact he
end NavierStokes.ActualCurrentParticularPhysical
end
end

-- REPLAY NavierStokes.SignedCopyBounds.local_congr 117 144
run_cmd IO.println "BLOCK NavierStokes.SignedCopyBounds.local_congr"
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
theorem local_congr_R {f g : ℕ → I → D → E} (hf : LocalJets s w α K f)
    (he : ∀ n i x, x ∈ s.domain → x ∈ K n i → f n i =ᶠ[𝓝 x] g n i) :
    LocalJets s w α K g := by
  refine ⟨fun n i x hx hi => (hf.smooth n i x hx hi).congr_of_eventuallyEq
    (he n i x hx hi).symm, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro n i x hx hi j hj
  rw [← jets_eq_of_germ (he n i x hx hi) j]
  exact hb n i x hx hi j hj
end LocalOperations
end NavierStokes.SignedCopyBounds
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.mono_weight 148 176
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.mono_weight"
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
theorem mono_weight_R (hf : LocalClass s K w α f)
    (hv : ∀ n i x, x ∈ s.domain → 0 ≤ v n i x)
    (hwv : ∀ n i x, x ∈ s.domain → x ∈ K n i → w n i x ≤ v n i x) :
    LocalClass s K v α f := by
  refine ⟨hv, hf.smooth, fun m => ?_⟩
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, fun n i x hx hi j hj => (hb n i x hx hi j hj).trans ?_⟩
  apply mul_le_mul_of_nonneg_left (hwv n i x hx hi)
  exact mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (s.epsilon_pos n) α).le)
    (pow_nonneg (s.growth_nonneg n x) p)
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.LinearWaveBounds.component_classes 180 208
run_cmd IO.println "BLOCK NavierStokes.LinearWaveBounds.component_classes"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.LinearWaveBounds
open WeightedClasses HarmonicCalculus Set Filter
open scoped ContDiff Topology BigOperators
variable {D E F : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]
namespace GraphDirections
end GraphDirections
namespace WaveCoefficients
end WaveCoefficients
namespace WaveCoefficients
end WaveCoefficients
#count_heartbeats in
theorem component_classes_R {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ}
    {f : ℕ → D → ComplexVector} (hf : ∀ i, MemClass s w α (fun n x => f n x i)) :
    MemClass s w α f := by
  have hh := MemClass.sum (s := s) Finset.univ
    (fun i n x => insertComponent i (f n x i)) (hf 0).weight_nonneg
    (fun i _ => (hf i).map (insertComponent i))
  apply class_congr hh
  intro n x _
  ext i
  fin_cases i <;> simp [insertComponent, Fin.sum_univ_three]
end NavierStokes.LinearWaveBounds
end
end

-- REPLAY NavierStokes.UniformHarmonicInteraction.square_weight_wave 212 246
run_cmd IO.println "BLOCK NavierStokes.UniformHarmonicInteraction.square_weight_wave"
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
end UniformAlgebra
section Cancellation
variable {s : StripData D} {κ α β : ℝ} {P : ℕ → D → ℝ}
end Cancellation
section Nonlinear
variable {s : StripData D} {κ α β : ℝ} {P : ι → ℕ → D → ℝ}
#count_heartbeats in
theorem square_weight_wave_R {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {γ : ℝ} {f : ι → ℕ → D → E}
    (hf : UniformClass s (fun l n x => (Real.sqrt (s.zeta x)*P l n x) *
      (Real.sqrt (s.zeta x)*P l n x)) γ f)
    (hζ : ∀ x ∈ s.domain, s.zeta x ≤ 1)
    (hP0 : ∀ l n x, x ∈ s.domain → 0 ≤ P l n x)
    (hP1 : ∀ l n x, x ∈ s.domain → P l n x ≤ 1) : UniformWaveClass s P γ f := by
  apply hf.mono_weight (fun l n x hx => mul_nonneg (Real.sqrt_nonneg _) (hP0 l n x hx))
  intro l n x hx
  have hs1 : Real.sqrt (s.zeta x) ≤ 1 := by
    nlinarith [Real.sq_sqrt (s.zeta_nonneg x hx), hζ x hx, Real.sqrt_nonneg (s.zeta x)]
  have hw1 : Real.sqrt (s.zeta x)*P l n x ≤ 1 :=
    (mul_le_mul hs1 (hP1 l n x hx) (hP0 l n x hx) zero_le_one).trans_eq (one_mul 1)
  exact mul_le_of_le_one_right (mul_nonneg (Real.sqrt_nonneg _) (hP0 l n x hx)) hw1
end Nonlinear
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.ActualInitialExcluded.initialGaussian_class_of_fields 250 325
run_cmd IO.println "BLOCK NavierStokes.ActualInitialExcluded.initialGaussian_class_of_fields"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ActualInitialExcluded
open Set Filter Function WeightedClasses ProblemStatement
open scoped Topology ContDiff BigOperators
section BaseContinuation
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
end BaseContinuation
section CompactNativeGeometry
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
  (U : LocalSignedRequest.SlowRegion (2 * F.data.h))
end CompactNativeGeometry
section PhysicalBaseJets
variable {F : OutgoingProfile.Profile} (W : NominalProfile.Witness F)
  (U : LocalSignedRequest.SlowRegion (2 * F.data.h))
variable (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
end PhysicalBaseJets
section NormalizedBase
variable {F : OutgoingProfile.Profile} {W : NominalProfile.Witness F}
  (H : NominalConeAssembly.Certificate W) {ld : ModulatedProfileAssembly.LoopData W}
  (v : ModulatedProfileAssembly.Witness ld) (upper : ℝ) (B : ℕ)
  (U : LocalSignedRequest.SlowRegion (2 * F.data.h))
end NormalizedBase
section NativeGaussianBounds
open CorrectionInitialization PrimaryCopyBounds PhaseJetBounds LocalizedWaveBounds
open ActualPrimaryBounds
variable {B N0 : ℕ}
end NativeGaussianBounds
section InitialLabelSupport
open CorrectionInitialization ActualPrimaryBounds
variable {B N0 : ℕ}
end InitialLabelSupport
section ActualGaussianIdentification
open CorrectionInitialization ActualPrimaryBounds
variable {B N0 : ℕ}
end ActualGaussianIdentification
section FlatProducts
variable {D : Type} {I : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {s : StripData D} {w : I → ℕ → D → ℝ} {K : I → ℕ → Set D}
  {f g : I → ℕ → D → ℂ}
end FlatProducts
section FullGaussian
open CorrectionInitialization ActualPrimaryBounds
variable {B N0 : ℕ}
#count_heartbeats in
theorem initialGaussian_class_of_fields_R (β : ℝ) (i : Fin 3)
    (hf : LabelSumBounds.UniformClass gaussianStrip
      (fun _ _ x => Real.sqrt (strip.zeta x.1)) β
      (fun l : SignedLabel B N0 => fun n x => gaussianField l n x i)) :
    MemClass gaussianStrip (fun _ x => Real.sqrt (strip.zeta x.1)) β
      (fun n x => initialGaussian B N0 n x i) := by
  have h := hf.reindex (fun l : ActualPrimary.Label B N0 × Fin 2 => (l.2,l.1))
  have hχ (n : ℕ) : ContinuousOn
      (fun x : ActualPrimary.FullPoint => ActualPrimaryCovariance.physicalWindow n x.1)
      gaussianStrip.domain :=
    (ActualPrimaryCovariance.physicalWindow_continuousOn n).comp
      continuous_fst.continuousOn (fun _ hx => hx)
  exact LabelSumBounds.window_sum_memClass (s := gaussianStrip)
    (w := fun _ x => Real.sqrt (strip.zeta x.1))
    (ActualPrimary.activeLabels ActualPrimary.standardRegion B N0)
    (fun _ => ActualPrimaryCovariance.signedLabelOf)
    (fun _ => ActualPrimaryCovariance.signedLabelOf_injective.injOn)
    (fun _ l _ => l.1.val.property.1)
    (CoordinateAlgebra.D ActualPrimary.h)
    (fun n x => ActualPrimaryCovariance.physicalWindow n x.1)
    hχ h
    (fun _ _ _ => Real.sqrt_nonneg _)
    (fun n l _ x hx hn => gaussianField_window (l.2,l.1) n hx i hn)
end FullGaussian
end NavierStokes.ActualInitialExcluded
end
end

-- REPLAY NavierStokes.LocalizedWaveBounds.LocalClass.enlarge 329 363
run_cmd IO.println "BLOCK NavierStokes.LocalizedWaveBounds.LocalClass.enlarge"
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
theorem enlarge_R {C : ℕ → I → Set D} (hf : LocalClass s C w α f)
    (hcover : ∀ n i x, x ∈ s.domain → x ∈ K n i →
      x ∈ C n i ∨ f n i =ᶠ[𝓝 x] fun _ => 0) : LocalClass s K w α f := by
  refine ⟨hf.weight_nonneg, ?_, ?_⟩
  · intro n i x hx hi
    rcases hcover n i x hx hi with hC | hz
    · exact hf.smooth n i x hx hC
    · exact contDiffAt_const.congr_of_eventuallyEq hz
  · intro m
    obtain ⟨A, hA, p, hb⟩ := hf.bounds m
    refine ⟨A, hA, p, fun n i x hx hi j hj => ?_⟩
    rcases hcover n i x hx hi with hC | hz
    · exact hb n i x hx hC j hj
    · rw [PeriodizedWaveBounds.jets_eq_of_germ hz j]
      simpa only [iteratedFDeriv_fun_zero, Pi.zero_apply, norm_zero] using
        majorant_nonneg s (fun n x => w n i x) α hA p n x (hf.weight_nonneg n i x hx)
end LocalClass
end NavierStokes.LocalizedWaveBounds
end
end

-- REPLAY NavierStokes.BaseRadialJets.radial_uniform_pullback 367 402
run_cmd IO.println "BLOCK NavierStokes.BaseRadialJets.radial_uniform_pullback"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.BaseRadialJets
open Set Filter Function BaseChartJets PhaseJetBounds PrimaryPulseBounds
open scoped ContDiff Topology BigOperators
#count_heartbeats in
theorem radial_uniform_pullback_R {ι : Type*} {E : Type}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (s : WeightedClasses.StripData E) (L : E →L[ℝ] Slow)
    {D : Domain (ℕ × ι) Slow} {a : ℕ → ℕ} {h C r M qlo qhi lo hi : ℝ}
    (hh : 0 < h) (hh1 : h < 1 / 2) (hr : 0 < r) (hM : 1 ≤ M)
    (hqlo : 0 < qlo) (hqhi : 0 < qhi) (hlo : 0 < lo)
    (H : GeometryBounds D h r M qlo qhi lo hi)
    {d : SlowBorelBase.Coefficients} (hd : SlowBorelBase.SmoothCoefficients d)
    (ha : SlowBorelBase.AdmissibleScales h (SlowBorelBase.coefficientBundle C d)
      (SlowBorelBase.innerBox lo hi) a)
    (Q : (ℕ × ι) → ℝ) (hQ : ∀ i, 0 < Q i) (hQ1 : ∀ i, Q i ≤ 1)
    (hsmall : ∀ i, Q i * qhi ≤ 1)
    (heps : ∀ n l, Q (n, l) ^ h = s.epsilon n)
    (hmap : ∀ n l, MapsTo L s.domain (D.carrier (n, l))) :
    LabelSumBounds.UniformClass s (fun _ _ _ => 1) 1
      (fun l n x => radial a h C d (Q (n, l)) (L x)) := by
  let V : Domain (ℕ × ι) E := oneDomain (ℕ × ι) (fun _ => s.domain) (fun _ => s.isOpen_domain)
  have he := radial_envelope hh hh1 hr hM hqlo hqhi hlo H hd ha Q hQ hQ1 hsmall
  have hp := he.precomp_linear (D := V) (fun _ => L) (fun _ => rfl)
    (fun i => hmap i.1 i.2) (C := max 1 ‖L‖) (k := 0) (le_max_left _ _)
    (fun _ => by simpa only [pow_zero, mul_one] using le_max_right 1 ‖L‖)
  apply LabelSumBounds.uniformClass_of_envelopeJets hp (K := 1) (q := 0) le_rfl
    (fun n l => by simp [V, oneDomain]) (fun _ _ => subset_rfl)
    (fun _ _ _ _ => zero_le_one)
  intro l n x hx
  simp only [heps, Real.rpow_one, mul_one, le_refl]
end NavierStokes.BaseRadialJets
end
end

