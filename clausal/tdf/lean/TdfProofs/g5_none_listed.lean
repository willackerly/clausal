/-
Guarantee 5: nothing is listed for a subject that is not entitled.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g5_none_listed` and its type is exactly
`Rule.tdflite_decision_core.g5_none_listed.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g5`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g5_none_listed : Rule.tdflite_decision_core.g5_none_listed.obligation := by
  intro st inp d st' hd hn
  have he : d.entitled = false := by
    cases h : d.entitled with
    | false => rfl
    | true => exact absurd h hn
  have hl := (T93.core_g5 st inp d hd.1).2.1 he
  simp [Abac.listedCount, hl]
