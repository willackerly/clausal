/-
M9 families, F00042: the derivative along a fixed vector, under 18 names in 14 modules.
Primitive: ONE DEFINITION with the direction as an explicit parameter; the domain and value spaces are type
parameters with their normed-space instances (that is the price: four instance arguments on every use).
-/
import Tool
import NavierStokes.AxisSourceRegularity
import NavierStokes.NaturalCoefficientBridge
import NavierStokes.ProfileHistories
import NavierStokes.SimilarityProfile
import NavierStokes.SmoothFourierData
import NavierStokes.TemporalMeanUpdate
import NavierStokes.ParametricTorusInverse
import NavierStokes.PositiveAxisSystem
import NavierStokes.ReferenceBounds
import NavierStokes.IntegratedMeanBalances
import NavierStokes.PressureStream
import NavierStokes.RadialAlias
import NavierStokes.SmoothFamilyTorusInverse
import NavierStokes.StateMomentBalances
import Euler.MeanScalarProductDerivatives
import Euler.MeanVectorIdentities
import Euler.PacketGraphHessian
import Euler.EulerProof
import Mathlib.Util.CountHeartbeats
set_option Elab.async false

open scoped ContDiff

namespace Fam.F42

variable {E F G : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]

/-- THE PRIMITIVE: the derivative of `f` at `x` along `v`. -/
noncomputable def dirDeriv (v : E) (f : E → F) (x : E) : F := fderiv ℝ f x v

/-! ### Each member is an instance (all by `rfl`) -/
section members
open NavierStokes

theorem m01 (f : EulerSmoothLimit.Space → EulerSmoothLimit.Space) (i : Fin 3) (x : EulerSmoothLimit.Space) :
    EulerMeanVectorIdentities.vectorPartial f i x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
theorem m02 (q : EulerLiftedGradientSpace.LiftTangent → ℝ) (z : EulerLiftedGradientSpace.LiftTangent) :
    EulerPacketGraphHessian.angularDerivative q z = dirDeriv (0, 1) q z := rfl
theorem m03 {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] (i : Fin 3) (f : EulerSobolev.Domain 3 → F)
    (x : EulerSobolev.Domain 3) :
    EulerSmoothSobolev.coordinateDerivative i f x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
theorem m04 (f : EulerSmoothLimit.Space → ℝ) (i : Fin 3) (x : EulerSmoothLimit.Space) :
    EulerVectorCalculus.partialDerivative f i x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
theorem m05 {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P] (v : P) (F : ℝ × P → ℝ) (x : ℝ × P) :
    IntegratedMeanBalances.parameterPartial v F x = dirDeriv (0, v) F x := rfl
theorem m06 (f : ParametricTorusInverse.Source) (z : ParametricTorusInverse.Point) :
    ParametricTorusInverse.parameterPartial f z = dirDeriv (1, 0) f z := rfl
theorem m07 {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] (k : ℝ → ℝ) (v : E) (f : ℝ × E → ℝ) (p : ℝ × E) :
    PressureStream.graphDr k v f p = dirDeriv (PressureStream.radialVector k v p) f p := rfl
theorem m08 {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] (w : E) (f : ℝ × E → ℝ) (p : ℝ × E) :
    PressureStream.graphDz w f p = dirDeriv (0, w) f p := rfl
theorem m09 (F : ProfileHistories.Field) (p : ProfileHistories.Point) :
    ProfileHistories.parameterPartial F p = dirDeriv (0, 1) F p := rfl
theorem m10 (F : ProfileHistories.Field) (p : ProfileHistories.Point) :
    ProfileHistories.radialPartial F p = dirDeriv (1, 0) F p := rfl
theorem m11 (v : E) (f : ℝ × E → F) (z : ℝ × E) : RadialAlias.directionalDeriv v f z = dirDeriv (0, v) f z := rfl
theorem m12 (f : ℝ × E → F) (z : ℝ × E) : RadialAlias.slowDeriv f z = dirDeriv (1, 0) f z := rfl
theorem m13 (f : SimilarityProfile.InnerProfile) (w : SimilarityProfile.InnerPoint) :
    SimilarityProfile.partialEta f w = dirDeriv (0, 1) f w := rfl
theorem m14 (f : SimilarityProfile.InnerProfile) (w : SimilarityProfile.InnerPoint) :
    SimilarityProfile.partialX f w = dirDeriv (1, 0) f w := rfl
theorem m15 {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P] (d : TorusInverse.Direction)
    (f : SmoothFamilyTorusInverse.Source P) (z : SmoothFamilyTorusInverse.Point P) :
    SmoothFamilyTorusInverse.directionalPartial d f z = dirDeriv (0, TorusInverse.vector d) f z := rfl
theorem m16 (f : TorusInverse.Plane → ℂ) (z : TorusInverse.Plane) : SmoothFourierData.partialX f z = dirDeriv (1, 0) f z := rfl
theorem m17 {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] (F : ℝ × S → ℝ) (x : ℝ × S) :
    StateMomentBalances.radialPartial F x = dirDeriv (1, 0) F x := rfl
theorem m18 (f : TorusInverse.Plane → ℂ) (z : TorusInverse.Plane) : TemporalMeanUpdate.partialY f z = dirDeriv (0, 1) f z := rfl

end members

/-! ### The API, once -/

theorem dirDeriv_contDiffAt {v : E} {f : E → F} {x : E} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f x) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (dirDeriv v f) x :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const

theorem dirDeriv_contDiffOn {v : E} {f : E → F} {U : Set E} {m n : WithTop ℕ∞} (hU : IsOpen U)
    (hf : ContDiffOn ℝ n f U) (hmn : m + 1 ≤ n) : ContDiffOn ℝ m (dirDeriv v f) U :=
  (hf.fderiv_of_isOpen hU hmn).clm_apply contDiffOn_const

theorem dirDeriv_contDiff {v : E} {f : E → F} {m n : WithTop ℕ∞}
    (hf : ContDiff ℝ n f) (hmn : m + 1 ≤ n) : ContDiff ℝ m (dirDeriv v f) :=
  (hf.fderiv_right hmn).clm_apply contDiff_const

theorem dirDeriv_const_mul {v : E} (C : ℝ) {f : E → ℝ} {x : E} (hf : DifferentiableAt ℝ f x) :
    dirDeriv v (fun p => C * f p) x = C * dirDeriv v f x := by
  simp only [dirDeriv, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]

theorem dirDeriv_mul {v : E} {f g : E → ℝ} {x : E} (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) :
    dirDeriv v (f * g) x = g x * dirDeriv v f x + f x * dirDeriv v g x := by
  simp only [dirDeriv, fderiv_mul hf hg, _root_.add_apply, _root_.smul_apply, smul_eq_mul]
  ring

/-- the slice in the first coordinate has the directional derivative along `(1, 0)` -/
theorem hasDerivAt_fst_slice {f : ℝ × G → F} {x : ℝ} {y : G} (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (dirDeriv (1, 0) f (x, y)) x :=
  hf.hasFDerivAt.comp_hasDerivAt x ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))

/-- the slice in the second coordinate has the directional derivative along `(0, 1)` -/
theorem hasDerivAt_snd_slice {f : G × ℝ → F} {x : G} {y : ℝ} (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (x, t)) (dirDeriv (0, 1) f (x, y)) y :=
  hf.hasFDerivAt.comp_hasDerivAt y ((hasDerivAt_const y x).prodMk (hasDerivAt_id y))

/-! ### Member lemmas re-derived (statements identical to the corpus) -/
namespace Re
open NavierStokes

section
open SimilarityProfile
#count_heartbeats in
theorem partialX_smoothAt {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialX f) w :=
  dirDeriv_contDiffAt hf hmn
#count_heartbeats in
theorem partialEta_smoothAt {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialEta f) w :=
  dirDeriv_contDiffAt hf hmn
#count_heartbeats in
theorem partialX_smooth {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialX v) w :=
  dirDeriv_contDiffAt hv (by simp)
#count_heartbeats in
theorem partialEta_smooth {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialEta v) w :=
  dirDeriv_contDiffAt hv (by simp)
#count_heartbeats in
theorem partialX_const_mul (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialX (fun p => C * f p) w = C * partialX f w :=
  dirDeriv_const_mul C hf
#count_heartbeats in
theorem partialEta_const_mul (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialEta (fun p => C * f p) w = C * partialEta f w :=
  dirDeriv_const_mul C hf
#count_heartbeats in
theorem hasDerivAt_parameterProfile {f : InnerProfile} {X eta : ℝ}
    (hf : DifferentiableAt ℝ f (X, eta)) :
    HasDerivAt (fun z => f (X, z)) (partialEta f (X, eta)) eta :=
  hasDerivAt_snd_slice hf
end

section
open ProfileHistories
#count_heartbeats in
theorem radialPartial_smooth (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (radialPartial F) D.carrier :=
  dirDeriv_contDiffOn D.isOpen hF (by simp)
#count_heartbeats in
theorem parameterPartial_smooth (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (parameterPartial F) D.carrier :=
  dirDeriv_contDiffOn D.isOpen hF (by simp)
end

section
open TorusInverse
#count_heartbeats in
theorem partialX_smooth' {f : Plane → ℂ} (hf : ContDiff ℝ ∞ f) :
    ContDiff ℝ ∞ (SmoothFourierData.partialX f) :=
  dirDeriv_contDiff hf (by simp)
#count_heartbeats in
theorem hasDerivAt_slice {f : Plane → ℂ} {x y : ℝ}
    (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (SmoothFourierData.partialX f (x, y)) x :=
  hasDerivAt_fst_slice hf
end

section
open ParametricTorusInverse
#count_heartbeats in
theorem parameter_slice_hasDerivAt {f : Source} (hf : ContDiff ℝ ∞ f)
    (p : ℝ) (Y : TorusInverse.Plane) :
    HasDerivAt (fun q => f (q, Y)) (parameterPartial f (p, Y)) p :=
  hasDerivAt_fst_slice ((hf.differentiable (by simp)) (p, Y))
end

section
open EulerVectorCalculus EulerSmoothLimit
#count_heartbeats in
theorem partialDerivative_mul {f g : Space → ℝ} {x : Space}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 3) :
    partialDerivative (f * g) i x = g x * partialDerivative f i x + f x * partialDerivative g i x :=
  dirDeriv_mul hf hg
end

end Re

end Fam.F42

run_cmd do
  Fam.report "F00042" ([("prim", `Fam.F42.dirDeriv),
    ("lib", `Fam.F42.dirDeriv_contDiffAt), ("lib", `Fam.F42.dirDeriv_contDiffOn), ("lib", `Fam.F42.dirDeriv_contDiff),
    ("lib", `Fam.F42.dirDeriv_const_mul), ("lib", `Fam.F42.dirDeriv_mul), ("lib", `Fam.F42.hasDerivAt_fst_slice),
    ("lib", `Fam.F42.hasDerivAt_snd_slice)] ++
    (List.range 18).map (fun i => ("inst", (`Fam.F42).str (if i < 9 then s!"m0{i+1}" else s!"m{i+1}"))))
  Fam.reportPairs "F00042" "re" [
    (`NavierStokes.SimilarityProfile.partialX_smoothAt, `Fam.F42.Re.partialX_smoothAt),
    (`NavierStokes.SimilarityProfile.partialEta_smoothAt, `Fam.F42.Re.partialEta_smoothAt),
    (`NavierStokes.AxisSourceRegularity.partialX_smooth, `Fam.F42.Re.partialX_smooth),
    (`NavierStokes.AxisSourceRegularity.partialEta_smooth, `Fam.F42.Re.partialEta_smooth),
    (`NavierStokes.NaturalCoefficientBridge.partialX_const_mul, `Fam.F42.Re.partialX_const_mul),
    (`NavierStokes.NaturalCoefficientBridge.partialEta_const_mul, `Fam.F42.Re.partialEta_const_mul),
    (`NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile, `Fam.F42.Re.hasDerivAt_parameterProfile),
    (`NavierStokes.ProfileHistories.radialPartial_smooth, `Fam.F42.Re.radialPartial_smooth),
    (`NavierStokes.ProfileHistories.parameterPartial_smooth, `Fam.F42.Re.parameterPartial_smooth),
    (`NavierStokes.SmoothFourierData.partialX_smooth, `Fam.F42.Re.partialX_smooth'),
    (`NavierStokes.SmoothFourierData.hasDerivAt_slice, `Fam.F42.Re.hasDerivAt_slice),
    (`NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt, `Fam.F42.Re.parameter_slice_hasDerivAt),
    (`EulerMeanHarmonic.partialDerivative_mul, `Fam.F42.Re.partialDerivative_mul)]
