import Tool
import F79
import NavierStokes.CurlClassBounds
import NavierStokes.LabelSumBounds
import NavierStokes.PeriodizedWaveBounds
import NavierStokes.UniformHarmonicInteraction
import NavierStokes.UniformPrimaryWeights
import NavierStokes.WeightedClasses
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.WeightedClasses.MemClass.map 13 33
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
    MemClass s w α (fun n x => L (f n x)) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).map L)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.fderiv 37 57
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
    MemClass s w α (fun n => _root_.fderiv ℝ (f n)) :=
  Fam.F79.memClass_iff.2 (Fam.F79.memClass_iff.1 hf).fderiv
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.bilinear 61 83
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
theorem bilinear_R {u : ℕ → D → F} (hf : MemClass s w α f)
    (hu : MemClass s v β u) (L : E →L[ℝ] F →L[ℝ] G) :
    MemClass s (fun n x => w n x * v n x) (α + β)
      (fun n x => L (f n x) (u n x)) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).bilinear (Fam.F79.memClass_iff.1 hu) L)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mul 87 109
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
      (fun n x => a n x * b n x) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 ha).mul (Fam.F79.memClass_iff.1 hb))
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.CurlClassBounds.class_neg 113 130
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
    MemClass s w α (fun n x => -f n x) :=
  Fam.F79.memClass_iff.2 (Fam.F79.memClass_iff.1 hf).neg
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.CurlClassBounds.class_sub 134 151
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
    MemClass s w α (fun n x => f n x - g n x) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).sub (Fam.F79.memClass_iff.1 hg))
end Classes
end NavierStokes.CurlClassBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.map 155 177
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
    UniformClass s w α (fun l n x => L (f l n x)) :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).map L)
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.neg 181 203
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
    UniformClass s w α (fun l n x => -f l n x) :=
  Fam.F79.uniformClass_iff.2 (Fam.F79.uniformClass_iff.1 hf).neg
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.bilinear 207 235
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
      (fun l n x => L (f l n x) (g l n x)) :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).bilinear (Fam.F79.uniformClass_iff.1 hg) L)
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.UniformPrimaryWeights.fderiv_class 239 263
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
    UniformClass s w α (fun l n => fderiv ℝ (f l n)) :=
  Fam.F79.uniformClass_iff.2 (Fam.F79.uniformClass_iff.1 hf).fderiv
end Calculus
end NavierStokes.UniformPrimaryWeights
end
end

-- REPLAY NavierStokes.UniformHarmonicInteraction.cmul 267 286
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
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).bilinear (Fam.F79.uniformClass_iff.1 hg) (ContinuousLinearMap.mul ℝ ℂ))
end UniformAlgebra
end NavierStokes.UniformHarmonicInteraction
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear 290 328
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
theorem bilinear_R {u : ℕ → I → D → F} (hf : LocalJets s w α K f)
    (hu : LocalJets s v β K u) (L : E →L[ℝ] F →L[ℝ] G)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x)
    (hv : ∀ n x, x ∈ s.domain → 0 ≤ v n x) :
    LocalJets s (fun n x => w n x * v n x) (α + β) K
      (fun n i x => L (f n i x) (u n i x)) :=
  ((NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hw hf).bilinear (NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hv hu) L).to_localJets
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.add 332 352
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
theorem add_R (hf : MemClass s w α f) (hg : MemClass s w α g) :
    MemClass s w α (fun n x => f n x + g n x) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).add (Fam.F79.memClass_iff.1 hg))
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.zero 356 376
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
theorem zero_R (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    MemClass s w α (fun _ _ => (0 : E)) :=
  Fam.F79.memClass_iff.2 (NavierStokes.LocalizedWaveBounds.LocalClass.zero (fun n _ x hx => hw n x hx))
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mono_exponent 380 400
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
theorem mono_exponent_R (hf : MemClass s w α f) (hβα : β ≤ α) :
    MemClass s w β f :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).mono_exponent hβα)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.mono_weight 404 425
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
theorem mono_weight_R (hf : MemClass s w α f)
    (hv : ∀ n x, x ∈ s.domain → 0 ≤ v n x)
    (hwv : ∀ n x, x ∈ s.domain → w n x ≤ v n x) : MemClass s v α f :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).mono_weight (fun n _ x hx => hv n x hx) (fun n _ x hx _ => hwv n x hx))
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.smul 429 451
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
theorem smul_R {a : ℕ → D → ℝ} (ha : MemClass s v β a)
    (hf : MemClass s w α f) :
    MemClass s (fun n x => v n x * w n x) (β + α)
      (fun n x => a n x • f n x) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 ha).smul (Fam.F79.memClass_iff.1 hf))
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.band_smul 455 475
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
    MemClass s w (α + β) (fun n x => a n • f n x) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).band_smul ha)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.WeightedClasses.MemClass.directional 479 499
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
theorem directional_R (hf : MemClass s w α f) (v : D) :
    MemClass s w α (fun n x => _root_.fderiv ℝ (f n) x v) :=
  Fam.F79.memClass_iff.2 ((Fam.F79.memClass_iff.1 hf).directional v)
end MemClass
end
end NavierStokes.WeightedClasses
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.add 503 525
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
theorem add_R (hf : UniformClass s w α f) (hg : UniformClass s w α g) :
    UniformClass s w α (fun l n x => f l n x + g l n x) :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).add (Fam.F79.uniformClass_iff.1 hg))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.sub 529 551
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
theorem sub_R (hf : UniformClass s w α f) (hg : UniformClass s w α g) :
    UniformClass s w α (fun l n x => f l n x - g l n x) :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).sub (Fam.F79.uniformClass_iff.1 hg))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.zero 555 577
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
theorem zero_R (hw : ∀ l n x, x ∈ s.domain → 0 ≤ w l n x) :
    UniformClass s w α (fun _ _ _ => (0 : E)) :=
  Fam.F79.uniformClass_iff.2 (NavierStokes.LocalizedWaveBounds.LocalClass.zero (fun n l x hx => hw l n x hx))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.mono_exponent 581 603
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
theorem mono_exponent_R (hf : UniformClass s w α f) (hβα : β ≤ α) :
    UniformClass s w β f :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).mono_exponent hβα)
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.mono_weight 607 630
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
theorem mono_weight_R (hf : UniformClass s w α f)
    (hv : ∀ l n x, x ∈ s.domain → 0 ≤ v l n x)
    (hwv : ∀ l n x, x ∈ s.domain → w l n x ≤ v l n x) : UniformClass s v α f :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).mono_weight (fun n l x hx => hv l n x hx) (fun n l x hx _ => hwv l n x hx))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.LabelSumBounds.UniformClass.congr 634 656
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
theorem congr_R (hf : UniformClass s w α f) (hfg : ∀ l n, EqOn (f l n) (g l n) s.domain) :
    UniformClass s w α g :=
  Fam.F79.uniformClass_iff.2 ((Fam.F79.uniformClass_iff.1 hf).congr_germ (fun n l x hx _ => Filter.eventuallyEq_of_mem (s.isOpen_domain.mem_nhds hx) (hfg l n)))
end UniformClass
end NavierStokes.LabelSumBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.add 660 695
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
theorem add_R (hf : LocalJets s w α K f) (hg : LocalJets s w α K g)
    (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => f n i x + g n i x) :=
  ((NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hw hf).add (NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hw hg)).to_localJets
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul 699 734
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
theorem band_smul_R {r : ℕ → ℝ} (hf : LocalJets s w α K f)
    (hr : BandBound s 0 r) (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => r n • f n i x) :=
  by simpa only [add_zero] using ((NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hw hf).band_smul hr).to_localJets
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

-- REPLAY NavierStokes.PeriodizedWaveBounds.LocalJets.smul 738 773
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
theorem smul_R {r : ℕ → I → D → ℝ} (hr : LocalJets s (fun _ _ => 1) 0 K r)
    (hf : LocalJets s w α K f) (hw : ∀ n x, x ∈ s.domain → 0 ≤ w n x) :
    LocalJets s w α K (fun n i x => r n i x • f n i x) :=
  by simpa only [one_mul, zero_add] using ((NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets (fun _ _ _ => zero_le_one) hr).smul (NavierStokes.LocalizedWaveBounds.LocalClass.of_localJets hw hf)).to_localJets
end LocalJets
end NativeJetOperations
end NavierStokes.PeriodizedWaveBounds
end
end

run_cmd Fam.reportPairs "F00079" "re" [(`NavierStokes.WeightedClasses.MemClass.map, `NavierStokes.WeightedClasses.MemClass.map_R), (`NavierStokes.WeightedClasses.MemClass.fderiv, `NavierStokes.WeightedClasses.MemClass.fderiv_R), (`NavierStokes.WeightedClasses.MemClass.bilinear, `NavierStokes.WeightedClasses.MemClass.bilinear_R), (`NavierStokes.WeightedClasses.MemClass.mul, `NavierStokes.WeightedClasses.MemClass.mul_R), (`NavierStokes.CurlClassBounds.class_neg, `NavierStokes.CurlClassBounds.class_neg_R), (`NavierStokes.CurlClassBounds.class_sub, `NavierStokes.CurlClassBounds.class_sub_R), (`NavierStokes.LabelSumBounds.UniformClass.map, `NavierStokes.LabelSumBounds.UniformClass.map_R), (`NavierStokes.LabelSumBounds.UniformClass.neg, `NavierStokes.LabelSumBounds.UniformClass.neg_R), (`NavierStokes.LabelSumBounds.UniformClass.bilinear, `NavierStokes.LabelSumBounds.UniformClass.bilinear_R), (`NavierStokes.UniformPrimaryWeights.fderiv_class, `NavierStokes.UniformPrimaryWeights.fderiv_class_R), (`NavierStokes.UniformHarmonicInteraction.cmul, `NavierStokes.UniformHarmonicInteraction.cmul_R), (`NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear, `NavierStokes.PeriodizedWaveBounds.LocalJets.bilinear_R), (`NavierStokes.WeightedClasses.MemClass.add, `NavierStokes.WeightedClasses.MemClass.add_R), (`NavierStokes.WeightedClasses.MemClass.zero, `NavierStokes.WeightedClasses.MemClass.zero_R), (`NavierStokes.WeightedClasses.MemClass.mono_exponent, `NavierStokes.WeightedClasses.MemClass.mono_exponent_R), (`NavierStokes.WeightedClasses.MemClass.mono_weight, `NavierStokes.WeightedClasses.MemClass.mono_weight_R), (`NavierStokes.WeightedClasses.MemClass.smul, `NavierStokes.WeightedClasses.MemClass.smul_R), (`NavierStokes.WeightedClasses.MemClass.band_smul, `NavierStokes.WeightedClasses.MemClass.band_smul_R), (`NavierStokes.WeightedClasses.MemClass.directional, `NavierStokes.WeightedClasses.MemClass.directional_R), (`NavierStokes.LabelSumBounds.UniformClass.add, `NavierStokes.LabelSumBounds.UniformClass.add_R), (`NavierStokes.LabelSumBounds.UniformClass.sub, `NavierStokes.LabelSumBounds.UniformClass.sub_R), (`NavierStokes.LabelSumBounds.UniformClass.zero, `NavierStokes.LabelSumBounds.UniformClass.zero_R), (`NavierStokes.LabelSumBounds.UniformClass.mono_exponent, `NavierStokes.LabelSumBounds.UniformClass.mono_exponent_R), (`NavierStokes.LabelSumBounds.UniformClass.mono_weight, `NavierStokes.LabelSumBounds.UniformClass.mono_weight_R), (`NavierStokes.LabelSumBounds.UniformClass.congr, `NavierStokes.LabelSumBounds.UniformClass.congr_R), (`NavierStokes.PeriodizedWaveBounds.LocalJets.add, `NavierStokes.PeriodizedWaveBounds.LocalJets.add_R), (`NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul, `NavierStokes.PeriodizedWaveBounds.LocalJets.band_smul_R), (`NavierStokes.PeriodizedWaveBounds.LocalJets.smul, `NavierStokes.PeriodizedWaveBounds.LocalJets.smul_R)]
