/-
Guarantee 5: a released key is released to an entitled subject.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g5_released_entitled` and its type is exactly
`Rule.tdflite_decision_core.g5_released_entitled.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g5`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g5_released_entitled : Rule.tdflite_decision_core.g5_released_entitled.obligation := by
  intro st inp d st' hd hr
  exact ((T93.core_g5 st inp d hd.1).1.mp hr).1
