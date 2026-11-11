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
import Mathlib.Util.CountHeartbeats
set_option Elab.async false
set_option Elab.async false

open scoped ContDiff

namespace Fam.F42

variable {E F G : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [NormedAddCommGroup F] [NormedSpace ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G]

#count_heartbeats in
/-- THE PRIMITIVE: the derivative of `f` at `x` along `v`. -/
noncomputable def dirDeriv (v : E) (f : E → F) (x : E) : F := fderiv ℝ f x v

/-! ### Each member is an instance (all by `rfl`) -/
section members
open NavierStokes

#count_heartbeats in
theorem m01 (f : EulerSmoothLimit.Space → EulerSmoothLimit.Space) (i : Fin 3) (x : EulerSmoothLimit.Space) :
    EulerMeanVectorIdentities.vectorPartial f i x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
#count_heartbeats in
theorem m02 (q : EulerLiftedGradientSpace.LiftTangent → ℝ) (z : EulerLiftedGradientSpace.LiftTangent) :
    EulerPacketGraphHessian.angularDerivative q z = dirDeriv (0, 1) q z := rfl
#count_heartbeats in
theorem m03 {F : Type*} [NormedAddCommGroup F] [InnerProductSpace ℂ F] (i : Fin 3) (f : EulerSobolev.Domain 3 → F)
    (x : EulerSobolev.Domain 3) :
    EulerSmoothSobolev.coordinateDerivative i f x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
#count_heartbeats in
theorem m04 (f : EulerSmoothLimit.Space → ℝ) (i : Fin 3) (x : EulerSmoothLimit.Space) :
    EulerVectorCalculus.partialDerivative f i x = dirDeriv (EuclideanSpace.single i 1) f x := rfl
#count_heartbeats in
theorem m05 {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P] (v : P) (F : ℝ × P → ℝ) (x : ℝ × P) :
    IntegratedMeanBalances.parameterPartial v F x = dirDeriv (0, v) F x := rfl
#count_heartbeats in
theorem m06 (f : ParametricTorusInverse.Source) (z : ParametricTorusInverse.Point) :
    ParametricTorusInverse.parameterPartial f z = dirDeriv (1, 0) f z := rfl
#count_heartbeats in
theorem m07 {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] (k : ℝ → ℝ) (v : E) (f : ℝ × E → ℝ) (p : ℝ × E) :
    PressureStream.graphDr k v f p = dirDeriv (PressureStream.radialVector k v p) f p := rfl
#count_heartbeats in
theorem m08 {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] (w : E) (f : ℝ × E → ℝ) (p : ℝ × E) :
    PressureStream.graphDz w f p = dirDeriv (0, w) f p := rfl
#count_heartbeats in
theorem m09 (F : ProfileHistories.Field) (p : ProfileHistories.Point) :
    ProfileHistories.parameterPartial F p = dirDeriv (0, 1) F p := rfl
#count_heartbeats in
theorem m10 (F : ProfileHistories.Field) (p : ProfileHistories.Point) :
    ProfileHistories.radialPartial F p = dirDeriv (1, 0) F p := rfl
#count_heartbeats in
theorem m11 (v : E) (f : ℝ × E → F) (z : ℝ × E) : RadialAlias.directionalDeriv v f z = dirDeriv (0, v) f z := rfl
#count_heartbeats in
theorem m12 (f : ℝ × E → F) (z : ℝ × E) : RadialAlias.slowDeriv f z = dirDeriv (1, 0) f z := rfl
#count_heartbeats in
theorem m13 (f : SimilarityProfile.InnerProfile) (w : SimilarityProfile.InnerPoint) :
    SimilarityProfile.partialEta f w = dirDeriv (0, 1) f w := rfl
#count_heartbeats in
theorem m14 (f : SimilarityProfile.InnerProfile) (w : SimilarityProfile.InnerPoint) :
    SimilarityProfile.partialX f w = dirDeriv (1, 0) f w := rfl
#count_heartbeats in
theorem m15 {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P] (d : TorusInverse.Direction)
    (f : SmoothFamilyTorusInverse.Source P) (z : SmoothFamilyTorusInverse.Point P) :
    SmoothFamilyTorusInverse.directionalPartial d f z = dirDeriv (0, TorusInverse.vector d) f z := rfl
#count_heartbeats in
theorem m16 (f : TorusInverse.Plane → ℂ) (z : TorusInverse.Plane) : SmoothFourierData.partialX f z = dirDeriv (1, 0) f z := rfl
#count_heartbeats in
theorem m17 {S : Type} [NormedAddCommGroup S] [NormedSpace ℝ S] (F : ℝ × S → ℝ) (x : ℝ × S) :
    StateMomentBalances.radialPartial F x = dirDeriv (1, 0) F x := rfl
#count_heartbeats in
theorem m18 (f : TorusInverse.Plane → ℂ) (z : TorusInverse.Plane) : TemporalMeanUpdate.partialY f z = dirDeriv (0, 1) f z := rfl

end members

/-! ### The API, once -/

#count_heartbeats in
theorem dirDeriv_contDiffAt {v : E} {f : E → F} {x : E} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f x) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (dirDeriv v f) x :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const

#count_heartbeats in
theorem dirDeriv_contDiffOn {v : E} {f : E → F} {U : Set E} {m n : WithTop ℕ∞} (hU : IsOpen U)
    (hf : ContDiffOn ℝ n f U) (hmn : m + 1 ≤ n) : ContDiffOn ℝ m (dirDeriv v f) U :=
  (hf.fderiv_of_isOpen hU hmn).clm_apply contDiffOn_const

#count_heartbeats in
theorem dirDeriv_contDiff {v : E} {f : E → F} {m n : WithTop ℕ∞}
    (hf : ContDiff ℝ n f) (hmn : m + 1 ≤ n) : ContDiff ℝ m (dirDeriv v f) :=
  (hf.fderiv_right hmn).clm_apply contDiff_const

#count_heartbeats in
theorem dirDeriv_const_mul {v : E} (C : ℝ) {f : E → ℝ} {x : E} (hf : DifferentiableAt ℝ f x) :
    dirDeriv v (fun p => C * f p) x = C * dirDeriv v f x := by
  simp only [dirDeriv, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]

#count_heartbeats in
theorem dirDeriv_mul {v : E} {f g : E → ℝ} {x : E} (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) :
    dirDeriv v (f * g) x = g x * dirDeriv v f x + f x * dirDeriv v g x := by
  simp only [dirDeriv, fderiv_mul hf hg, _root_.add_apply, _root_.smul_apply, smul_eq_mul]
  ring

#count_heartbeats in
/-- the slice in the first coordinate has the directional derivative along `(1, 0)` -/
theorem hasDerivAt_fst_slice {f : ℝ × G → F} {x : ℝ} {y : G} (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (dirDeriv (1, 0) f (x, y)) x :=
  hf.hasFDerivAt.comp_hasDerivAt x ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))

#count_heartbeats in
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
