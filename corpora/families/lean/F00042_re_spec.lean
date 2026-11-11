import Tool
import Euler.MeanScalarProductDerivatives
import NavierStokes.AxisSourceRegularity
import NavierStokes.NaturalCoefficientBridge
import NavierStokes.ParametricTorusInverse
import NavierStokes.PositiveAxisSystem
import NavierStokes.ProfileHistories
import NavierStokes.SimilarityProfile
import NavierStokes.SmoothFourierData
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY NavierStokes.SimilarityProfile.partialX_smoothAt 14 26
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialX_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialX_smoothAt_S {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialX f) w :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.SimilarityProfile.partialEta_smoothAt 30 42
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialEta_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialEta_smoothAt_S {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialEta f) w :=
  (hf.fderiv_right hmn).clm_apply contDiffAt_const
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialX_smooth 46 58
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialX_smooth_S {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialX v) w :=
  partialX_smoothAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialEta_smooth 62 74
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialEta_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialEta_smooth_S {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialEta v) w :=
  partialEta_smoothAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialX_const_mul 78 93
run_cmd IO.println "BLOCK NavierStokes.NaturalCoefficientBridge.partialX_const_mul"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped Topology ContDiff
namespace NavierStokes.NaturalCoefficientBridge
open SimilarityProfile (InnerPoint InnerProfile partialX partialEta T Z)
open SlowExpansionResidual
#count_heartbeats in
theorem partialX_const_mul_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialX (fun p => C * f p) w = C * partialX f w := by
  simp only [partialX, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialEta_const_mul 97 112
run_cmd IO.println "BLOCK NavierStokes.NaturalCoefficientBridge.partialEta_const_mul"
section
set_option linter.all false
noncomputable section
open Set Filter
open scoped Topology ContDiff
namespace NavierStokes.NaturalCoefficientBridge
open SimilarityProfile (InnerPoint InnerProfile partialX partialEta T Z)
open SlowExpansionResidual
#count_heartbeats in
theorem partialEta_const_mul_S (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialEta (fun p => C * f p) w = C * partialEta f w := by
  simp only [partialEta, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile 116 137
run_cmd IO.println "BLOCK NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile"
section
set_option linter.all false
noncomputable section
open Set
open scoped BigOperators ContDiff
namespace NavierStokes.PositiveAxisSystem
section Algebra
variable {K : Type*} [Field K] [CharZero K]
end Algebra
section ActualProfiles
open SimilarityProfile
#count_heartbeats in
theorem hasDerivAt_parameterProfile_S {f : InnerProfile} {X eta : ℝ}
    (hf : DifferentiableAt ℝ f (X, eta)) :
    HasDerivAt (fun z => f (X, z)) (partialEta f (X, eta)) eta := by
  have hc := hf.hasFDerivAt.comp_hasDerivAt eta
    ((hasDerivAt_const eta X).prodMk (hasDerivAt_id eta))
  simpa [fderiv_inner_apply, Function.comp_def] using hc
end ActualProfiles
end NavierStokes.PositiveAxisSystem
end
end

-- REPLAY NavierStokes.ProfileHistories.radialPartial_smooth 141 153
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.radialPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem radialPartial_smooth_S (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (radialPartial F) D.carrier := by
  exact (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ProfileHistories.parameterPartial_smooth 157 169
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.parameterPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem parameterPartial_smooth_S (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (parameterPartial F) D.carrier := by
  exact (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.SmoothFourierData.partialX_smooth 173 187
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem partialX_smooth_S {f : Plane → ℂ} (hf : ContDiff ℝ ∞ f) :
    ContDiff ℝ ∞ (partialX f) :=
  (ContinuousLinearMap.apply ℝ ℂ (1, 0)).contDiff.comp
    (hf.fderiv_right (by simp))
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.SmoothFourierData.hasDerivAt_slice 191 206
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.hasDerivAt_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem hasDerivAt_slice_S {f : Plane → ℂ} {x y : ℝ}
    (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (partialX f (x, y)) x := by
  exact hf.hasFDerivAt.comp_hasDerivAt x
    ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt 210 225
run_cmd IO.println "BLOCK NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParametricTorusInverse
open Set Filter MeasureTheory
open TorusInverse
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem parameter_slice_hasDerivAt_S {f : Source} (hf : ContDiff ℝ ∞ f)
    (p : ℝ) (Y : Plane) :
    HasDerivAt (fun q => f (q, Y)) (parameterPartial f (p, Y)) p := by
  exact ((hf.differentiable (by simp)) (p, Y)).hasFDerivAt.comp_hasDerivAt p
    ((hasDerivAt_id p).prodMk (hasDerivAt_const p Y))
end NavierStokes.ParametricTorusInverse
end
end

-- REPLAY EulerMeanHarmonic.partialDerivative_mul 229 243
run_cmd IO.println "BLOCK EulerMeanHarmonic.partialDerivative_mul"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open InnerProductSpace EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff
#count_heartbeats in
theorem partialDerivative_mul_S {f g : Space → ℝ} {x : Space}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 3) :
    partialDerivative (f * g) i x = g x * partialDerivative f i x + f x * partialDerivative g i x := by
  rw [← gradient_coordinate, gradient_mul hf hg]
  simp only [PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, gradient_coordinate]
end EulerMeanHarmonic
end
end

