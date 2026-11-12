/-
Guarantee 3: for a labelled object, entitled exactly when every label is satisfied under its attribute's rule.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g3_entitled` and its type is exactly
`Rule.tdflite_decision_core.g3_entitled.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g3_entitled`; `T93.core_g3_hierarchy`, `T93.core_g3_allOf`, `T93.core_g3_anyOf`, `T93.satisfied_refines`, `T93.idspec_g3_norule` (in `TdfProofs.satisfied_iff`); `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g3_entitled : Rule.tdflite_decision_core.g3_entitled.obligation := by
  intro st inp hu
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  obtain ⟨ids, hb, hne⟩ := hu
  have key := T93.core_g3_entitled st inp d ids hd hb hne
  have hl : Abac.labels inp = ids.val := by simp [Abac.labels, hb]
  constructor
  · intro he x hx
    rw [hl] at hx
    obtain ⟨a, ha, hs⟩ := key.mp he x hx
    exact ⟨a, ha, by rw [hl]; exact (TdfProofs.satisfied_iff st inp.subject a ids).mp hs⟩
  · intro H
    refine key.mpr ?_
    intro i hi
    obtain ⟨a, ha, hs⟩ := H i (by rw [hl]; exact hi)
    rw [hl] at hs
    exact ⟨a, ha, (TdfProofs.satisfied_iff st inp.subject a ids).mpr hs⟩

/-- The scope is met: a request for a labelled object. -/
theorem Rule.tdflite_decision_core.g3_entitled.sat : Rule.tdflite_decision_core.g3_entitled.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _⟩
