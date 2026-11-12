/-
Guarantee 1, an unresolved object: never entitled.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g1_unresolved` and its type is exactly
`Rule.tdflite_decision_core.g1_unresolved.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g1`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g1_unresolved : Rule.tdflite_decision_core.g1_unresolved.obligation := by
  intro st inp hu
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  intro he
  obtain ⟨ids, hb, _⟩ := T93.core_g1 st inp d hd he
  have hu' : inp.bound = .Unresolved := hu
  rw [hu'] at hb
  cases hb

/-- The scope is met: a request whose labels did not resolve. -/
theorem Rule.tdflite_decision_core.g1_unresolved.sat : Rule.tdflite_decision_core.g1_unresolved.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.unresolvedRequest, trivial, rfl⟩
