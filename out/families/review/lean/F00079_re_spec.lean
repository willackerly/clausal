import Tool
import NavierStokes.CurlClassBounds
import NavierStokes.LabelSumBounds
import NavierStokes.PeriodizedWaveBounds
import NavierStokes.UniformHarmonicInteraction
import NavierStokes.UniformPrimaryWeights
import NavierStokes.WeightedClasses
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.WeightedClasses.MemClass.map 12 44
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
theorem map_S (hf : MemClass s w α f) (L : E →L[ℝ] F) :
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

-- REPLAY NavierStokes.WeightedClasses.MemClass.fderiv 48 76
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
theorem fderiv_S (hf : MemClass s w α f) :
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

-- REPLAY NavierStokes.WeightedClasses.MemClass.bilinear 80 120
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.bilinear"
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
theorem bilinear_S {u : ℕ → D → F} (hf : MemClass s w α f)
    (hu : MemClass s v β u) (L : E →L[ℝ] F →L[ℝ] G) :
    MemClass s (fun n x => w n x * v n x) (α + β)
      (fun n x => L (f n x) (u n x)) := by
  refine ⟨fun n x hx => mul_nonneg (hf.weight_nonneg n x hx) (hu.weight_nonneg n x hx),
    fun n => (L.contDiff.comp_contDiffOn (hf.smooth n)).clm_apply (hu.smooth n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hu.bounds m
  refine ⟨‖L‖ * (2 : ℝ) ^ m * A * B, by positivity, p + q, ?_⟩
  intro n x hx j hj
  calc
    _ ≤ ‖L‖ * (2 : ℝ) ^ m * majorant s w α A p n x * majorant s v β B q n x :=
      bilinear_bound_at L hx (hf.smooth n) (hu.smooth n)
        (majorant_nonneg s w α hA p n x (hf.weight_nonneg n x hx))
        (majorant_nonneg s v β hB q n x (hu.weight_nonneg n x hx))
        (fun i hi => ha n x hx i hi) (fun i hi => hb n x hx i hi) hj
    _ = (‖L‖ * (2 : ℝ) ^ m) *
        (majorant s w α A p n x * majorant s v β B q n x) := by ring
    _ = _ := by
      rw [majorant_mul]
      unfold majorant
      ring
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mul 124 146
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
theorem mul_S {a b : ℕ → D → ℝ} (ha : MemClass s w α a)
    (hb : MemClass s v β b) :
    MemClass s (fun n x => w n x * v n x) (α + β)
      (fun n x => a n x * b n x) := by
  simpa only [smul_eq_mul] using ha.smul hb
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.CurlClassBounds.class_neg 150 167
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
theorem class_neg_S {f : ℕ → D → E} (hf : MemClass s w α f) :
    MemClass s w α (fun n x => -f n x) := by
  simpa using hf.map (-ContinuousLinearMap.id ℝ E)
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.CurlClassBounds.class_sub 171 188
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
theorem class_sub_S {f g : ℕ → D → E} (hf : MemClass s w α f) (hg : MemClass s w α g) :
    MemClass s w α (fun n x => f n x - g n x) := by
  simpa only [sub_eq_add_neg] using hf.add (class_neg hg)
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.map 192 225
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
theorem map_S (hf : UniformClass s w α f) (L : E →L[ℝ] F) :
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

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.neg 229 252
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
theorem neg_S (hf : UniformClass s w α f) :
    UniformClass s w α (fun l n x => -f l n x) := by
  simpa only [_root_.neg_apply, ContinuousLinearMap.id_apply] using
    hf.map (-(ContinuousLinearMap.id ℝ E))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.bilinear 256 299
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
theorem bilinear_S (hf : UniformClass s w α f) (hg : UniformClass s v β g)
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

-- REPLAY NavierStokes.UniformPrimaryWeights.fderiv_class 303 333
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
theorem fderiv_class_S {f : ι → ℕ → D → E} (hf : UniformClass s w α f) :
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

-- REPLAY NavierStokes.UniformHarmonicInteraction.cmul 337 356
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
theorem cmul_S {f g : ι → ℕ → D → ℂ} (hf : UniformClass s w α f)
    (hg : UniformClass s v β g) :
    UniformClass s (fun l n x => w l n x * v l n x) (α+β)
      (fun l n x => f l n x * g l n x) :=
  hf.bilinear hg (ContinuousLinearMap.mul ℝ ℂ)
end UniformAlgebra
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear 360 412
run_cmd IO.println "BLOCK NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PeriodizedWaveBounds
open Set Function Filter WeightedClasses
open scoped Topology ContDiff BigOperators
section LocalGluing
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] {I : Type*}
end LocalGluing
section UniformLabels
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {L I : Type*}
end UniformLabels
section NativeCells
open CommonCoverSolve TorusInverse TorusAverages
variable {P E : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end NativeCells
section NativeJetOperations
variable {D E F G : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G] {I : Type*}
namespace LocalJets
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {K : ℕ → I → Set D} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem bilinear_S {u : ℕ → I → D → F} (hf : LocalJets s w α K f)
    (hu : LocalJets s v β K u) (L : E →L[ℝ] F →L[ℝ] G)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x)
    (hv : ∀ n x, x ∈ s.domain → 0 ≤ v n x) :
    LocalJets s (fun n x => w n x * v n x) (α + β) K
      (fun n i x => L (f n i x) (u n i x)) := by
  refine ⟨fun n i x hx hi => (L.contDiff.contDiffAt.comp x (hf.smooth n i x hx hi)).clm_apply
    (hu.smooth n i x hx hi), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hu.bounds m
  refine ⟨‖L‖ * (2 : ℝ) ^ m * A * B, by positivity, p + q, ?_⟩
  intro n i x hx hi j hj
  calc
    _ ≤ ‖L‖ * (2 : ℝ) ^ m * majorant s w α A p n x * majorant s v β B q n x :=
      bilinear_jet_at L (hf.smooth n i x hx hi) (hu.smooth n i x hx hi)
        (majorant_nonneg s w α hA p n x (hw n x hx))
        (majorant_nonneg s v β hB q n x (hv n x hx)) hj
        (fun k hk => ha n i x hx hi k hk) (fun k hk => hb n i x hx hi k hk)
    _ = (‖L‖ * (2 : ℝ) ^ m) * (majorant s w α A p n x * majorant s v β B q n x) := by ring
    _ = _ := by rw [majorant_mul]; unfold majorant; ring
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.add 416 452
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.add"
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
theorem add_S (hf : MemClass s w α f) (hg : MemClass s w α g) :
    MemClass s w α (fun n x => f n x + g n x) := by
  refine ⟨hf.weight_nonneg, fun n => (hf.smooth n).add (hg.smooth n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hg.bounds m
  refine ⟨A + B, add_nonneg hA hB, p + q, ?_⟩
  intro n x hx j hj
  rw [fun_iteratedFDeriv_add_apply (hf.contDiffAt n hx j) (hg.contDiffAt n hx j)]
  calc
    _ ≤ ‖iteratedFDeriv ℝ j (f n) x‖ + ‖iteratedFDeriv ℝ j (g n) x‖ := norm_add_le _ _
    _ ≤ majorant s w α A p n x + majorant s w α B q n x :=
      add_le_add (ha n x hx j hj) (hb n x hx j hj)
    _ ≤ majorant s w α A (p + q) n x + majorant s w α B (p + q) n x :=
      add_le_add (majorant_mono_degree s w α hA (Nat.le_add_right p q) n x
        (hf.weight_nonneg n x hx))
        (majorant_mono_degree s w α hB (Nat.le_add_left q p) n x
          (hf.weight_nonneg n x hx))
    _ = _ := by unfold majorant; ring
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.zero 456 480
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.zero"
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
theorem zero_S (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    MemClass s w α (fun _ _ => (0 : E)) := by
  refine ⟨hw, fun _ => contDiffOn_const, ?_⟩
  intro m
  refine ⟨0, le_rfl, 0, ?_⟩
  intro n x hx j hj
  simp [majorant]
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mono_exponent 484 513
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.mono_exponent"
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
theorem mono_exponent_S (hf : MemClass s w α f) (hβα : β ≤ α) :
    MemClass s w β f := by
  refine ⟨hf.weight_nonneg, hf.smooth, ?_⟩
  intro m
  obtain ⟨C, hC, p, h⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro n x hx j hj
  apply (h n x hx j hj).trans
  apply mul_le_mul_of_nonneg_right _ (hf.weight_nonneg n x hx)
  apply mul_le_mul_of_nonneg_right _ (pow_nonneg (s.growth_nonneg n x) p)
  exact mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge (s.epsilon_pos n) (s.epsilon_le_one n) hβα) hC
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mono_weight 517 546
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.mono_weight"
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
theorem mono_weight_S (hf : MemClass s w α f)
    (hv : ∀ n x, x ∈ s.domain → 0 ≤ v n x)
    (hwv : ∀ n x, x ∈ s.domain → w n x ≤ v n x) : MemClass s v α f := by
  refine ⟨hv, hf.smooth, ?_⟩
  intro m
  obtain ⟨C, hC, p, h⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro n x hx j hj
  apply (h n x hx j hj).trans
  apply mul_le_mul_of_nonneg_left (hwv n x hx)
  exact mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (s.epsilon_pos n) α).le)
    (pow_nonneg (s.growth_nonneg n x) p)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.smul 550 572
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.smul"
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
theorem smul_S {a : ℕ → D → ℝ} (ha : MemClass s v β a)
    (hf : MemClass s w α f) :
    MemClass s (fun n x => v n x * w n x) (β + α)
      (fun n x => a n x • f n x) :=
  ha.bilinear hf (ContinuousLinearMap.lsmul ℝ ℝ)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.band_smul 576 616
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
theorem band_smul_S {a : ℕ → ℝ} (hf : MemClass s w α f) (ha : BandBound s β a) :
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

-- REPLAY NavierStokes.WeightedClasses.MemClass.directional 620 640
run_cmd IO.println "BLOCK NavierStokes.WeightedClasses.MemClass.directional"
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
theorem directional_S (hf : MemClass s w α f) (v : D) :
    MemClass s w α (fun n x => _root_.fderiv ℝ (f n) x v) :=
  hf.fderiv.map (ContinuousLinearMap.apply ℝ E v)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.add 644 681
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.add"
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
theorem add_S (hf : UniformClass s w α f) (hg : UniformClass s w α g) :
    UniformClass s w α (fun l n x => f l n x + g l n x) := by
  refine ⟨hf.weight_nonneg, fun l n => (hf.smooth l n).add (hg.smooth l n), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hg.bounds m
  refine ⟨A + B, add_nonneg hA hB, p + q, ?_⟩
  intro l n x hx j hj
  rw [fun_iteratedFDeriv_add_apply ((hf.each l).contDiffAt n hx j) ((hg.each l).contDiffAt n hx j)]
  calc
    _ ≤ ‖iteratedFDeriv ℝ j (f l n) x‖ + ‖iteratedFDeriv ℝ j (g l n) x‖ := norm_add_le _ _
    _ ≤ majorant s (w l) α A p n x + majorant s (w l) α B q n x :=
      add_le_add (ha l n x hx j hj) (hb l n x hx j hj)
    _ ≤ majorant s (w l) α A (p + q) n x + majorant s (w l) α B (p + q) n x :=
      add_le_add (majorant_mono_degree s (w l) α hA (Nat.le_add_right p q) n x
        (hf.weight_nonneg l n x hx))
        (majorant_mono_degree s (w l) α hB (Nat.le_add_left q p) n x (hf.weight_nonneg l n x hx))
    _ = _ := by unfold majorant; ring
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.sub 685 707
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.sub"
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
theorem sub_S (hf : UniformClass s w α f) (hg : UniformClass s w α g) :
    UniformClass s w α (fun l n x => f l n x - g l n x) := by
  simpa only [sub_eq_add_neg] using hf.add hg.neg
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.zero 711 737
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.zero"
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
theorem zero_S (hw : ∀ l n x, x ∈ s.domain → 0 ≤ w l n x) :
    UniformClass s w α (fun _ _ _ => (0 : E)) := by
  refine ⟨hw, fun _ _ => contDiffOn_const, ?_⟩
  intro m
  refine ⟨0, le_rfl, 0, ?_⟩
  intro l n x hx j hj
  simp [majorant]
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.mono_exponent 741 772
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.mono_exponent"
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
theorem mono_exponent_S (hf : UniformClass s w α f) (hβα : β ≤ α) :
    UniformClass s w β f := by
  refine ⟨hf.weight_nonneg, hf.smooth, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro l n x hx j hj
  apply (hb l n x hx j hj).trans
  apply mul_le_mul_of_nonneg_right _ (hf.weight_nonneg l n x hx)
  apply mul_le_mul_of_nonneg_right _ (pow_nonneg (s.growth_nonneg n x) p)
  exact mul_le_mul_of_nonneg_left
    (Real.rpow_le_rpow_of_exponent_ge (s.epsilon_pos n) (s.epsilon_le_one n) hβα) hC
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.mono_weight 776 807
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.mono_weight"
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
theorem mono_weight_S (hf : UniformClass s w α f)
    (hv : ∀ l n x, x ∈ s.domain → 0 ≤ v l n x)
    (hwv : ∀ l n x, x ∈ s.domain → w l n x ≤ v l n x) : UniformClass s v α f := by
  refine ⟨hv, hf.smooth, ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro l n x hx j hj
  apply (hb l n x hx j hj).trans
  exact mul_le_mul_of_nonneg_left (hwv l n x hx)
    (mul_nonneg (mul_nonneg hC (Real.rpow_pos_of_pos (s.epsilon_pos n) α).le)
      (pow_nonneg (s.growth_nonneg n x) p))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.congr 811 842
run_cmd IO.println "BLOCK NavierStokes.LabelSumBounds.UniformClass.congr"
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
theorem congr_S (hf : UniformClass s w α f) (hfg : ∀ l n, EqOn (f l n) (g l n) s.domain) :
    UniformClass s w α g := by
  refine ⟨hf.weight_nonneg, fun l n => (hf.smooth l n).congr
    (fun x hx => (hfg l n hx).symm), ?_⟩
  intro m
  obtain ⟨C, hC, p, hb⟩ := hf.bounds m
  refine ⟨C, hC, p, ?_⟩
  intro l n x hx j hj
  have he : f l n =ᶠ[𝓝 x] g l n :=
    eventually_of_mem (s.isOpen_domain.mem_nhds hx) (hfg l n)
  rw [← PhysicalWaveSum.iteratedFDeriv_eq_of_eventuallyEq he j]
  exact hb l n x hx j hj
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.add 846 896
run_cmd IO.println "BLOCK NavierStokes.PeriodizedWaveBounds.LocalJets.add"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PeriodizedWaveBounds
open Set Function Filter WeightedClasses
open scoped Topology ContDiff BigOperators
section LocalGluing
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] {I : Type*}
end LocalGluing
section UniformLabels
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {L I : Type*}
end UniformLabels
section NativeCells
open CommonCoverSolve TorusInverse TorusAverages
variable {P E : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end NativeCells
section NativeJetOperations
variable {D E F G : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G] {I : Type*}
namespace LocalJets
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {K : ℕ → I → Set D} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem add_S (hf : LocalJets s w α K f) (hg : LocalJets s w α K g)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => f n i x + g n i x) := by
  refine ⟨fun n i x hx hi => (hf.smooth n i x hx hi).add (hg.smooth n i x hx hi), ?_⟩
  intro m
  obtain ⟨A, hA, p, ha⟩ := hf.bounds m
  obtain ⟨B, hB, q, hb⟩ := hg.bounds m
  refine ⟨A + B, add_nonneg hA hB, p + q, ?_⟩
  intro n i x hx hi j hj
  rw [fun_iteratedFDeriv_add_apply ((hf.smooth n i x hx hi).of_le (finite_le_infty j))
    ((hg.smooth n i x hx hi).of_le (finite_le_infty j))]
  calc
    _ ≤ ‖iteratedFDeriv ℝ j (f n i) x‖ + ‖iteratedFDeriv ℝ j (g n i) x‖ := norm_add_le _ _
    _ ≤ majorant s w α A p n x + majorant s w α B q n x :=
      add_le_add (ha n i x hx hi j hj) (hb n i x hx hi j hj)
    _ ≤ majorant s w α A (p + q) n x + majorant s w α B (p + q) n x :=
      add_le_add (majorant_mono_degree s w α hA (Nat.le_add_right _ _) n x (hw n x hx))
        (majorant_mono_degree s w α hB (Nat.le_add_left _ _) n x (hw n x hx))
    _ = _ := by unfold majorant; ring
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul 900 938
run_cmd IO.println "BLOCK NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PeriodizedWaveBounds
open Set Function Filter WeightedClasses
open scoped Topology ContDiff BigOperators
section LocalGluing
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] {I : Type*}
end LocalGluing
section UniformLabels
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {L I : Type*}
end UniformLabels
section NativeCells
open CommonCoverSolve TorusInverse TorusAverages
variable {P E : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end NativeCells
section NativeJetOperations
variable {D E F G : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G] {I : Type*}
namespace LocalJets
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {K : ℕ → I → Set D} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem band_smul_S {r : ℕ → ℝ} (hf : LocalJets s w α K f)
    (hr : BandBound s 0 r) (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => r n • f n i x) := by
  have hc : UnweightedClass s 0 (fun n (_ : D) => r n) := by
    have h := (unweighted_const s (1 : ℝ)).band_smul hr
    simpa using h
  exact (LocalJets.of_memClass hc).smul hf hw
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.smul 942 979
run_cmd IO.println "BLOCK NavierStokes.PeriodizedWaveBounds.LocalJets.smul"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.PeriodizedWaveBounds
open Set Function Filter WeightedClasses
open scoped Topology ContDiff BigOperators
section LocalGluing
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] {I : Type*}
end LocalGluing
section UniformLabels
variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {L I : Type*}
end UniformLabels
section NativeCells
open CommonCoverSolve TorusInverse TorusAverages
variable {P E : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]
  [NormedAddCommGroup E] [NormedSpace ℝ E]
end NativeCells
section NativeJetOperations
variable {D E F G : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D]
  [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G] {I : Type*}
namespace LocalJets
variable {s : StripData D} {w v : ℕ → D → ℝ} {α β : ℝ}
  {K : ℕ → I → Set D} {f g : ℕ → I → D → E}
#count_heartbeats in
theorem smul_S {r : ℕ → I → D → ℝ} (hr : LocalJets s (fun _ _ => 1) 0 K r)
    (hf : LocalJets s w α K f) (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => r n i x • f n i x) := by
  have h := hr.bilinear hf (ContinuousLinearMap.lsmul ℝ ℝ) (fun _ _ _ => zero_le_one) hw
  simp only [one_mul, zero_add] at h
  exact h
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

