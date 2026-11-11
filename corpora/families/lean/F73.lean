/-
M9 families, F00073: translation on L², written twice.  The primitive ALREADY EXISTS in the corpus:
`EulerLpTranslation.translation` is polymorphic in the value space `V` (a definition with a type parameter and
its instance arguments); `EulerMeanSolenoidal.translation` is that definition at `V := Space`.
-/
import Tool
import Euler.MeanTimeTranslation
import Euler.LpTranslation
import Mathlib.Util.CountHeartbeats
set_option Elab.async false

open MeasureTheory EulerSmoothLimit

namespace Fam.F73

/-- the member is the primitive at one type, definitionally -/
theorem member_eq : @EulerMeanSolenoidal.translation = @EulerLpTranslation.translation Space _ _ := rfl

theorem m1 (a : Space) : EulerMeanSolenoidal.translation a = EulerLpTranslation.translation (V := Space) a := rfl

namespace Re
open EulerMeanSolenoidal

#count_heartbeats in
theorem translation_ae (a : Space) (u : L2) :
    translation a u =ᵐ[volume] fun x => u (x + a) :=
  EulerLpTranslation.translation_ae a u

#count_heartbeats in
theorem translation_add (a b : Space) (u : L2) :
    translation a (translation b u) = translation (a + b) u :=
  EulerLpTranslation.translation_add a b u

#count_heartbeats in
theorem translation_zero (u : L2) : translation 0 u = u :=
  EulerLpTranslation.translation_zero u

#count_heartbeats in
theorem translation_continuous (u : L2) : Continuous (fun a : Space => translation a u) :=
  EulerLpTranslation.translation_continuous u

end Re
end Fam.F73

run_cmd do
  Fam.report "F00073" [("prim", `EulerLpTranslation.translation), ("member", `EulerMeanSolenoidal.translation), ("inst", `Fam.F73.member_eq),
    ("lib", `EulerLpTranslation.translation_ae), ("lib", `EulerLpTranslation.translation_add),
    ("lib", `EulerLpTranslation.translation_zero), ("lib", `EulerLpTranslation.translation_continuous)]
  Fam.reportPairs "F00073" "re" [
    (`EulerMeanSolenoidal.translation_ae, `Fam.F73.Re.translation_ae),
    (`EulerMeanSolenoidal.translation_add, `Fam.F73.Re.translation_add),
    (`EulerMeanSolenoidal.translation_zero, `Fam.F73.Re.translation_zero),
    (`EulerMeanTimeTranslation.translation_continuous, `Fam.F73.Re.translation_continuous)]
