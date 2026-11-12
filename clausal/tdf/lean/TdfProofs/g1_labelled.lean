/-
Guarantee 1, a labelled object: entitled only if the subject holds something.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g1_labelled` and its type is exactly
`Rule.tdflite_decision_core.g1_labelled.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g1`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g1_labelled : Rule.tdflite_decision_core.g1_labelled.obligation := by
  intro st inp hu
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  intro he
  obtain ⟨ids0, hb0, h0⟩ := hu
  obtain ⟨ids, hb, h⟩ := T93.core_g1 st inp d hd he
  rw [hb0] at hb
  cases hb
  rcases h with ⟨he0, _⟩ | ⟨_, hh⟩
  · exact absurd he0 h0
  · exact hh

/-- The scope is met: a request for a labelled object. -/
theorem Rule.tdflite_decision_core.g1_labelled.sat : Rule.tdflite_decision_core.g1_labelled.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _⟩
