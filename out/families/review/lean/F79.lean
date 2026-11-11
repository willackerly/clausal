/-
M9 families, F00079 (positive control: constant-hiding predicates):
`MemClass`, `UniformClass`, `LocalClass`, `LocalJets`.

THE PRIMITIVE ALREADY EXISTS IN THE CORPUS: `LocalClass` has both optional features (an extra index and a
localising family of sets).  `MemClass` is `LocalClass` at a one-point index with no localisation,
`UniformClass` is `LocalClass` with no localisation (index order swapped), and `LocalJets` is `LocalClass`
with an index-free weight MINUS the field `weight_nonneg`, so it is an instance only under that hypothesis.
Form: a Prop-valued structure with explicit parameters; no type class.
-/
import Tool
import NavierStokes.LocalizedWaveBounds
import NavierStokes.LabelSumBounds

open Set NavierStokes NavierStokes.WeightedClasses NavierStokes.LabelSumBounds NavierStokes.LocalizedWaveBounds
  NavierStokes.PeriodizedWaveBounds
open scoped ContDiff

namespace Fam.F79

section
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- `MemClass` is `LocalClass` at a one-point index with every set the whole space. -/
theorem memClass_iff {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ} {f : ℕ → D → E} :
    MemClass s w α f ↔
      LocalClass s (fun _ (_ : Unit) => univ) (fun n _ => w n) α (fun n _ => f n) := by
  constructor
  · exact fun hf => LocalClass.of_global hf
  · intro hf
    refine ⟨fun n x hx => hf.weight_nonneg n () x hx, fun n => ?_, fun m => ?_⟩
    · exact fun x hx => (hf.smooth n () x hx (mem_univ x)).contDiffWithinAt
    · obtain ⟨C, hC, p, hb⟩ := hf.bounds m
      exact ⟨C, hC, p, fun n x hx j hj => hb n () x hx (mem_univ x) j hj⟩

/-- `LocalJets` is `LocalClass` with an index-free weight, GIVEN that the weight is nonnegative
(a hypothesis `LocalJets` does not carry). -/
theorem localJets_iff {I : Type*} {s : StripData D} {w : ℕ → D → ℝ} {α : ℝ} {K : ℕ → I → Set D}
    {f : ℕ → I → D → E} (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K f ↔ LocalClass s K (fun n _ => w n) α f :=
  ⟨fun hf => LocalClass.of_localJets hw hf, fun hf => hf.to_localJets⟩

/-- The hypothesis cannot be dropped: with weight `-1` the zero family is in `LocalJets` and not in `LocalClass`. -/
theorem localJets_not_localClass {I : Type*} (s : StripData D) (α : ℝ) (K : ℕ → I → Set D) (i : I) {x : D}
    (hx : x ∈ s.domain) :
    LocalJets s (fun _ _ => (-1 : ℝ)) α K (fun _ _ _ => (0 : E)) ∧
      ¬ LocalClass s K (fun _ _ _ => (-1 : ℝ)) α (fun _ _ _ => (0 : E)) := by
  refine ⟨⟨fun n i x _ _ => contDiffAt_const, fun m => ⟨0, le_rfl, 0, fun n i x _ _ j _ => ?_⟩⟩, fun h => ?_⟩
  · have h0 : iteratedFDeriv ℝ j (fun _ : D => (0 : E)) x = 0 := by
      simpa using iteratedFDeriv_zero_fun (𝕜 := ℝ) (E := D) (F := E) (n := j) ▸ rfl
    rw [h0]; unfold majorant; simp
  · have := h.weight_nonneg 0 i x hx
    norm_num at this

end

section
variable {ι E : Type*} {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- `UniformClass` is `LocalClass` with every set the whole space (index order swapped). -/
theorem uniformClass_iff {s : StripData D} {w : ι → ℕ → D → ℝ} {α : ℝ} {f : ι → ℕ → D → E} :
    UniformClass s w α f ↔
      LocalClass s (fun _ (_ : ι) => univ) (fun n l => w l n) α (fun n l => f l n) := by
  constructor
  · intro hf
    refine ⟨fun n l x hx => hf.weight_nonneg l n x hx,
      fun n l x hx _ => (hf.smooth l n).contDiffAt (s.isOpen_domain.mem_nhds hx), fun m => ?_⟩
    obtain ⟨C, hC, p, hb⟩ := hf.bounds m
    exact ⟨C, hC, p, fun n l x hx _ j hj => hb l n x hx j hj⟩
  · intro hf
    refine ⟨fun l n x hx => hf.weight_nonneg n l x hx, fun l n => ?_, fun m => ?_⟩
    · exact fun x hx => (hf.smooth n l x hx (mem_univ x)).contDiffWithinAt
    · obtain ⟨C, hC, p, hb⟩ := hf.bounds m
      exact ⟨C, hC, p, fun l n x hx j hj => hb n l x hx (mem_univ x) j hj⟩

end

end Fam.F79

run_cmd do
  Fam.report "F00079" [("prim", `NavierStokes.LocalizedWaveBounds.LocalClass), ("member", `NavierStokes.WeightedClasses.MemClass),
    ("member", `NavierStokes.LabelSumBounds.UniformClass), ("member", `NavierStokes.PeriodizedWaveBounds.LocalJets),
    ("inst", `Fam.F79.memClass_iff), ("inst", `Fam.F79.uniformClass_iff), ("inst", `Fam.F79.localJets_iff),
    ("counter", `Fam.F79.localJets_not_localClass),
    ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.map), ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.add),
    ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.neg), ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.sub),
    ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.fderiv), ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.bilinear),
    ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.smul), ("lib", `NavierStokes.LocalizedWaveBounds.LocalClass.mul)]
