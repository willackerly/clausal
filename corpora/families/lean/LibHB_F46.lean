/-
M9 families, F00046 (positive control: constant-hiding predicates): `MemClass` at four named weights.
THE PRIMITIVE ALREADY EXISTS: `MemClass` takes the weight as an explicit parameter and the four members are
reducible abbreviations of it at one weight each.  Nothing new is defined; the question measured here is how
much of what is proved about the named instances is the primitive's API restated.
-/
import Tool
import NavierStokes.CurrentSignedCurl
import NavierStokes.CurlClassBounds
import NavierStokes.MeanIncrementBounds
import Mathlib.Util.CountHeartbeats
set_option Elab.async false

open NavierStokes NavierStokes.WeightedClasses

namespace Fam.F46

section
variable {D E : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup E] [NormedSpace ℝ E]

run_cmd IO.println "LIBDECL m1"
#count_heartbeats in
theorem m1 (s : StripData D) (α : ℝ) (f : ℕ → D → E) :
    MeanClass s α f = MemClass s (fun _ x => s.zeta x) α f := rfl
run_cmd IO.println "LIBDECL m2"
#count_heartbeats in
theorem m2 (s : StripData D) (α : ℝ) (f : ℕ → D → E) :
    UnweightedClass s α f = MemClass s (fun _ _ => 1) α f := rfl
run_cmd IO.println "LIBDECL m3"
#count_heartbeats in
theorem m3 (s : StripData D) (P : ℕ → D → ℝ) (α : ℝ) (f : ℕ → D → E) :
    WaveClass s P α f = MemClass s (fun n x => Real.sqrt (s.zeta x) * P n x) α f := rfl
end

run_cmd IO.println "LIBDECL m4"
#count_heartbeats in
open NavierStokes.CurrentSignedCurl in
theorem m4 {B N0 : ℕ} (l : ActualSignedCoherence.SignedLabel B N0)
    (u : CorrectionState.State CurrentSignedCurl.Point) (α : ℝ) :
    CurrentSignedCurl.AmplitudeBound l u α =
      MemClass ActualSignedStageControls.fullStrip
        (fun n x => Real.sqrt (ActualSignedStageControls.fullStrip.zeta x) *
          ActualSignedStageControls.envelope l n x) α (ActualSignedCoherence.copies l u).common.amplitude := rfl

end Fam.F46

