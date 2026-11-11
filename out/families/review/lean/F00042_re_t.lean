import Tool
import F42
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

-- REPLAY NavierStokes.SimilarityProfile.partialX_smoothAt 15 27
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialX_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialX_smoothAt_R {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialX f) w :=
  Fam.F42.dirDeriv_contDiffAt hf hmn
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.SimilarityProfile.partialEta_smoothAt 31 43
run_cmd IO.println "BLOCK NavierStokes.SimilarityProfile.partialEta_smoothAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SimilarityProfile
open Set Filter
open scoped Topology ContDiff
#count_heartbeats in
theorem partialEta_smoothAt_R {f : InnerProfile} {w : InnerPoint} {m n : WithTop ℕ∞}
    (hf : ContDiffAt ℝ n f w) (hmn : m + 1 ≤ n) : ContDiffAt ℝ m (partialEta f) w :=
  Fam.F42.dirDeriv_contDiffAt hf hmn
end NavierStokes.SimilarityProfile
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialX_smooth 47 59
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialX_smooth_R {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialX v) w :=
  Fam.F42.dirDeriv_contDiffAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.AxisSourceRegularity.partialEta_smooth 63 75
run_cmd IO.println "BLOCK NavierStokes.AxisSourceRegularity.partialEta_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.AxisSourceRegularity
open SimilarityProfile Set Filter
open scoped BigOperators Topology ContDiff
#count_heartbeats in
theorem partialEta_smooth_R {v : InnerProfile} {w : InnerPoint}
    (hv : ContDiffAt ℝ ∞ v w) : ContDiffAt ℝ ∞ (partialEta v) w :=
  Fam.F42.dirDeriv_contDiffAt hv (by simp)
end NavierStokes.AxisSourceRegularity
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialX_const_mul 79 94
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
theorem partialX_const_mul_R (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialX (fun p => C * f p) w = C * partialX f w :=
  Fam.F42.dirDeriv_const_mul C hf
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.NaturalCoefficientBridge.partialEta_const_mul 98 113
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
theorem partialEta_const_mul_R (C : ℝ) {f : InnerProfile} {w : InnerPoint}
    (hf : DifferentiableAt ℝ f w) :
    partialEta (fun p => C * f p) w = C * partialEta f w :=
  Fam.F42.dirDeriv_const_mul C hf
end NavierStokes.NaturalCoefficientBridge
end
end

-- REPLAY NavierStokes.PositiveAxisSystem.hasDerivAt_parameterProfile 117 136
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
theorem hasDerivAt_parameterProfile_R {f : InnerProfile} {X eta : ℝ}
    (hf : DifferentiableAt ℝ f (X, eta)) :
    HasDerivAt (fun z => f (X, z)) (partialEta f (X, eta)) eta :=
  Fam.F42.hasDerivAt_snd_slice hf
end ActualProfiles
end NavierStokes.PositiveAxisSystem
end
end

-- REPLAY NavierStokes.ProfileHistories.radialPartial_smooth 140 152
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.radialPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem radialPartial_smooth_R (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (radialPartial F) D.carrier :=
  Fam.F42.dirDeriv_contDiffOn D.isOpen hF (by simp)
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.ProfileHistories.parameterPartial_smooth 156 168
run_cmd IO.println "BLOCK NavierStokes.ProfileHistories.parameterPartial_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ProfileHistories
open Set MeasureTheory Filter Metric
open scoped Topology ContDiff
#count_heartbeats in
theorem parameterPartial_smooth_R (D : RadialDomain) {F : Field}
    (hF : ContDiffOn ℝ ∞ F D.carrier) : ContDiffOn ℝ ∞ (parameterPartial F) D.carrier :=
  Fam.F42.dirDeriv_contDiffOn D.isOpen hF (by simp)
end NavierStokes.ProfileHistories
end
end

-- REPLAY NavierStokes.SmoothFourierData.partialX_smooth 172 185
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.partialX_smooth"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem partialX_smooth_R {f : Plane → ℂ} (hf : ContDiff ℝ ∞ f) :
    ContDiff ℝ ∞ (partialX f) :=
  Fam.F42.dirDeriv_contDiff hf (by simp)
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.SmoothFourierData.hasDerivAt_slice 189 203
run_cmd IO.println "BLOCK NavierStokes.SmoothFourierData.hasDerivAt_slice"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.SmoothFourierData
open Set Function MeasureTheory TorusInverse
open scoped BigOperators ContDiff Interval Topology
local instance : Fact ((0 : ℝ) < 1) := ⟨by norm_num⟩
#count_heartbeats in
theorem hasDerivAt_slice_R {f : Plane → ℂ} {x y : ℝ}
    (hf : DifferentiableAt ℝ f (x, y)) :
    HasDerivAt (fun t => f (t, y)) (partialX f (x, y)) x :=
  Fam.F42.hasDerivAt_fst_slice hf
end NavierStokes.SmoothFourierData
end
end

-- REPLAY NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt 207 221
run_cmd IO.println "BLOCK NavierStokes.ParametricTorusInverse.parameter_slice_hasDerivAt"
section
set_option linter.all false
noncomputable section
namespace NavierStokes.ParametricTorusInverse
open Set Filter MeasureTheory
open TorusInverse
open scoped Topology ContDiff BigOperators
#count_heartbeats in
theorem parameter_slice_hasDerivAt_R {f : Source} (hf : ContDiff ℝ ∞ f)
    (p : ℝ) (Y : Plane) :
    HasDerivAt (fun q => f (q, Y)) (parameterPartial f (p, Y)) p :=
  Fam.F42.hasDerivAt_fst_slice ((hf.differentiable (by simp)) (p, Y))
end NavierStokes.ParametricTorusInverse
end
end

-- REPLAY EulerMeanHarmonic.partialDerivative_mul 225 238
run_cmd IO.println "BLOCK EulerMeanHarmonic.partialDerivative_mul"
section
set_option linter.all false
noncomputable section
namespace EulerMeanHarmonic
open InnerProductSpace EulerSmoothLimit EulerVectorCalculus
open scoped ContDiff
#count_heartbeats in
theorem partialDerivative_mul_R {f g : Space → ℝ} {x : Space}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) (i : Fin 3) :
    partialDerivative (f * g) i x = g x * partialDerivative f i x + f x * partialDerivative g i x :=
  Fam.F42.dirDeriv_mul hf hg
end EulerMeanHarmonic
end
end

