/-
Witness (T9.3 `witness_withheld`): an entitled subject is refused the key, at the named input.
Hand-written (plan node T9.7a). The theorem is named exactly `Spec.tdflite_decision_core.w_withheld` and its type is exactly
`Spec.tdflite_decision_core.w_withheld.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.decide_total`, `T93.decide_refines`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Spec.tdflite_decision_core.w_withheld : Spec.tdflite_decision_core.w_withheld.obligation := by
  intro st inp hs hi
  subst hs hi
  obtain ⟨d, hd⟩ := T93.decide_total Tdf.twoLevelPolicy Tdf.clearedSilent
  have h := TdfProofs.at_clearedSilent d hd
  exact ⟨d, _, ⟨hd, rfl⟩, by simp [Abac.released, h.2], h.1⟩

/-- The scope is met: at the named policy and the named request. -/
theorem Spec.tdflite_decision_core.w_withheld.sat : Spec.tdflite_decision_core.w_withheld.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.clearedSilent, trivial, rfl, rfl⟩
