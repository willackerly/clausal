/-
Guarantee 1, an unlabelled object: entitled only if the policy admits unlabelled objects.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g1_unlabelled` and its type is exactly
`Rule.tdflite_decision_core.g1_unlabelled.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g1`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g1_unlabelled : Rule.tdflite_decision_core.g1_unlabelled.obligation := by
  intro st inp hu
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  intro he
  obtain ⟨ids0, hb0, h0⟩ := hu
  obtain ⟨ids, hb, h⟩ := T93.core_g1 st inp d hd he
  rw [hb0] at hb
  cases hb
  rcases h with ⟨_, hdeny⟩ | ⟨hne, _⟩
  · exact hdeny
  · exact absurd h0 hne

/-- The scope is met: a request for an object that carries no label. -/
theorem Rule.tdflite_decision_core.g1_unlabelled.sat : Rule.tdflite_decision_core.g1_unlabelled.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.unlabelledRequest, trivial, ⟨_, rfl, by simp [Tdf.vec3]⟩⟩
