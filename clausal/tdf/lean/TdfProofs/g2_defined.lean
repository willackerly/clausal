/-
Guarantee 2: entitled only if every label is defined by the policy.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g2_defined` and its type is exactly
`Rule.tdflite_decision_core.g2_defined.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g2`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g2_defined : Rule.tdflite_decision_core.g2_defined.obligation := by
  intro st inp
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  intro he
  intro x hx
  cases hb : inp.bound with
  | Unresolved => simp [Abac.labels, hb] at hx
  | Labels ids =>
    simp only [Abac.labels, hb] at hx
    exact T93.core_g2 st inp d ids hd he hb x hx
