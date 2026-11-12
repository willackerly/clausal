/-
Guarantee 5: every obligation a releasing decision lists was declared by the client.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g5_released_declared` and its type is exactly
`Rule.tdflite_decision_core.g5_released_declared.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g5`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g5_released_declared : Rule.tdflite_decision_core.g5_released_declared.obligation := by
  intro st inp d st' hd hr x hx
  obtain ⟨o, ho, rfl⟩ := List.mem_map.mp hx
  exact List.mem_map.mpr ⟨o, ((T93.core_g5 st inp d hd.1).1.mp hr).2 o ho, rfl⟩
