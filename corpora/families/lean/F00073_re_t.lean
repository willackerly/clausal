import Tool
import F73
import Euler.MeanSolenoidalTranslation
import Euler.MeanTimeTranslation
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY EulerMeanSolenoidal.translation_ae 9 21
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_ae"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_ae_R (a : Space) (u : L2) :
    translation a u =ᵐ[volume] fun x => u (x + a) :=
  EulerLpTranslation.translation_ae a u
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanSolenoidal.translation_add 25 37
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_add"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_add_R (a b : Space) (u : L2) :
    translation a (translation b u) = translation (a + b) u :=
  EulerLpTranslation.translation_add a b u
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanSolenoidal.translation_zero 41 52
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_zero"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_zero_R (u : L2) : translation 0 u = u :=
  EulerLpTranslation.translation_zero u
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanTimeTranslation.translation_continuous 56 67
run_cmd IO.println "BLOCK EulerMeanTimeTranslation.translation_continuous"
section
set_option linter.all false
noncomputable section
namespace EulerMeanTimeTranslation
open Set MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerTimeLp EulerTerminalTimePrimitive EulerTimeLpBoundedMap
#count_heartbeats in
theorem translation_continuous_R (u : L2) : Continuous (fun a : Space => translation a u) :=
  EulerLpTranslation.translation_continuous u
end EulerMeanTimeTranslation
end
end

