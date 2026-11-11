import Tool
import Euler.MeanSolenoidalTranslation
import Euler.MeanTimeTranslation
import Mathlib.Util.CountHeartbeats
set_option Elab.async false  -- so that #count_heartbeats includes the proof

-- REPLAY EulerMeanSolenoidal.translation_ae 8 20
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_ae"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_ae_S (a : Space) (u : L2) :
    translation a u =ᵐ[volume] fun x => u (x + a) :=
  Lp.coeFn_compMeasurePreserving u (measurePreserving_add_right volume a)
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanSolenoidal.translation_add 24 40
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_add"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_add_S (a b : Space) (u : L2) :
    translation a (translation b u) = translation (a + b) u := by
  apply Lp.ext
  filter_upwards [translation_ae a (translation b u),
    (measurePreserving_add_right (volume : Measure Space) a).quasiMeasurePreserving.ae
      (translation_ae b u), translation_ae (a + b) u] with x hx hy hz
  rw [hx, hy, hz, add_assoc]
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanSolenoidal.translation_zero 44 57
run_cmd IO.println "BLOCK EulerMeanSolenoidal.translation_zero"
section
set_option linter.all false
noncomputable section
namespace EulerMeanSolenoidal
open MeasureTheory InnerProductSpace EulerSmoothLimit
open scoped ContDiff
#count_heartbeats in
theorem translation_zero_S (u : L2) : translation 0 u = u := by
  apply Lp.ext
  filter_upwards [translation_ae 0 u] with x hx
  simpa only [add_zero] using hx
end EulerMeanSolenoidal
end
end

-- REPLAY EulerMeanTimeTranslation.translation_continuous 61 76
run_cmd IO.println "BLOCK EulerMeanTimeTranslation.translation_continuous"
section
set_option linter.all false
noncomputable section
namespace EulerMeanTimeTranslation
open Set MeasureTheory InnerProductSpace ContinuousLinearMap EulerSmoothLimit
  EulerMeanSolenoidal EulerTimeLp EulerTerminalTimePrimitive EulerTimeLpBoundedMap
#count_heartbeats in
theorem translation_continuous_S (u : L2) : Continuous (fun a : Space => translation a u) := by
  let g : Space → C(Space, Space) := fun a => ⟨fun x => x+a, continuous_id.add continuous_const⟩
  have hg : Continuous g := ContinuousMap.continuous_of_continuous_uncurry g
    (continuous_snd.add continuous_fst)
  exact continuous_const.compMeasurePreservingLp hg
    (fun a => measurePreserving_add_right (volume : Measure Space) a) (by norm_num)
end EulerMeanTimeTranslation
end
end

