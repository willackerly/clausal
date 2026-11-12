/-
Guarantee 5: for an entitled subject, what is listed is what the specification requires, in order.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g5_listed_required` and its type is exactly
`Rule.tdflite_decision_core.g5_listed_required.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g5`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g5_listed_required : Rule.tdflite_decision_core.g5_listed_required.obligation := by
  intro st inp d st' hd he
  exact (T93.core_g5 st inp d hd.1).2.2 he
