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
theorem partialX_smoothAt_M {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
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
theorem partialEta_smoothAt_M {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
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
theorem partialX_smooth_M {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialX v) w :=
  (hv.fderiv_right (by simp)).clm_apply contDiffAt_const
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
theorem partialEta_smooth_M {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialEta v) w :=
  (hv.fderiv_right (by simp)).clm_apply contDiffAt_const
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
theorem partialX_const_mul_M (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialX (fun p => C * f p) w = C * partialX f w :=
  by simp only [partialX, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
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
theorem partialEta_const_mul_M (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialEta (fun p => C * f p) w = C * partialEta f w :=
  by simp only [partialEta, fderiv_const_mul hf, _root_.smul_apply, smul_eq_mul]
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile 116 135
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
theorem hasDerivAt_parameterProfile_M {f : InnerProfile} {X eta : ℝ}
    (hf : DifferentiableAt ℝ f (X, eta)) :
    HasDerivAt (fun z => f (X, z)) (partialEta f (X, eta)) eta :=
  hf.hasFDerivAt.comp_hasDerivAt eta ((hasDerivAt_const eta X).prodMk (hasDerivAt_id eta))
end ActualProfiles
end NavierStokes.PositiveAxisSystem
end
end

-- REPLAY NavierStokes.ProfileHistories.radialPartial_smooth 139 151
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.radialPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem radialPartial_smooth_M (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (radialPartial F) D.carrier :=
  (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ProfileHistories.parameterPartial_smooth 155 167
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.parameterPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem parameterPartial_smooth_M (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (parameterPartial F) D.carrier :=
  (hF.fderiv_of_isOpen D.isOpen (by simp)).clm_apply contDiffOn_const
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.SmoothFourierData.partialX_smooth 171 184
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem partialX_smooth_M {f : Plane → ℂ} (hf : ContDiff ℝ ∞ f) :
    ContDiff ℝ ∞ (partialX f) :=
  (hf.fderiv_right (by simp)).clm_apply contDiff_const
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.SmoothFourierData.hasDerivAt_slice 188 202
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.hasDerivAt_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem hasDerivAt_slice_M {f : Plane → ℂ} {x y : ℝ}
    (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (partialX f (x, y)) x :=
  hf.hasFDerivAt.comp_hasDerivAt x ((hasDerivAt_id x).prodMk (hasDerivAt_const x y))
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt 206 220
run_cmd IO.println "BLOCK NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParametricTorusInverse
open Set Filter MeasureTheory
open TorusInverse
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem parameter_slice_hasDerivAt_M {f : Source} (hf : ContDiff ℝ ∞ f)
    (p : ℝ) (Y : Plane) :
    HasDerivAt (fun q => f (q, Y)) (parameterPartial f (p, Y)) p :=
  ((hf.differentiable (by simp)) (p, Y)).hasFDerivAt.comp_hasDerivAt p ((hasDerivAt_id p).prodMk (hasDerivAt_const p Y))
end NavierStokes.ParametricTorusInverse
end
end

-- REPLAY EulerMeanHarmonic.partialDerivative_mul 224 237
run_cmd IO.println "BLOCK EulerMeanHarmonic.partialDerivative_mul"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open InnerProductSpace EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff
#count_heartbeats in
theorem partialDerivative_mul_M {f g : Space → ℝ} {x : Space}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 3) :
    partialDerivative (f * g) i x = g x * partialDerivative f i x + f x * partialDerivative g i x :=
  by simp only [partialDerivative, fderiv_mul hf hg, _root_.add_apply, _root_.smul_apply, smul_eq_mul]; ring
end EulerMeanHarmonic
end
end

run_cmd Fam.reportPairs "F00042" "re" [(`NavierStokes.SimilarityProfile.partialX_smoothAt, `NavierStokes.SimilarityProfile.partialX_smoothAt_M), (`NavierStokes.SimilarityProfile.partialEta_smoothAt, `NavierStokes.SimilarityProfile.partialEta_smoothAt_M), (`NavierStokes.AxisSourceRegularity.partialX_smooth, `NavierStokes.AxisSourceRegularity.partialX_smooth_M), (`NavierStokes.AxisSourceRegularity.partialEta_smooth, `NavierStokes.AxisSourceRegularity.partialEta_smooth_M), (`NavierStokes.NaturalCoefficientBridge.partialX_const_mul, `NavierStokes.NaturalCoefficientBridge.partialX_const_mul_M), (`NavierStokes.NaturalCoefficientBridge.partialEta_const_mul, `NavierStokes.NaturalCoefficientBridge.partialEta_const_mul_M), (`NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile, `NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile_M), (`NavierStokes.ProfileHistories.radialPartial_smooth, `NavierStokes.ProfileHistories.radialPartial_smooth_M), (`NavierStokes.ProfileHistories.parameterPartial_smooth, `NavierStokes.ProfileHistories.parameterPartial_smooth_M), (`NavierStokes.SmoothFourierData.partialX_smooth, `NavierStokes.SmoothFourierData.partialX_smooth_M), (`NavierStokes.SmoothFourierData.hasDerivAt_slice, `NavierStokes.SmoothFourierData.hasDerivAt_slice_M), (`NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt, `NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt_M), (`EulerMeanHarmonic.partialDerivative_mul, `EulerMeanHarmonic.partialDerivative_mul_M)]
