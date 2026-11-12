/-
Witness (T9.3 `witness_denied`): a labelled object is denied to a subject that holds something, at the named input.
Hand-written (plan node T9.7a). The theorem is named exactly `Spec.tdflite_decision_core.w_denied` and its type is exactly
`Spec.tdflite_decision_core.w_denied.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.decide_total`, `T93.decide_refines`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Spec.tdflite_decision_core.w_denied : Spec.tdflite_decision_core.w_denied.obligation := by
  intro st inp hs _ hi
  subst hs hi
  obtain ⟨d, hd⟩ := T93.decide_total Tdf.twoLevelPolicy Tdf.noLevel
  have h := TdfProofs.at_noLevel d hd
  exact ⟨d, _, ⟨hd, rfl⟩, by simp [Abac.entitled, h]⟩

/-- The scope is met: at the named policy and the named request. -/
theorem Spec.tdflite_decision_core.w_denied.sat : Spec.tdflite_decision_core.w_denied.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.noLevel, trivial, rfl, Or.inl (by simp [Tdf.noLevel, Tdf.requestWith, Tdf.vec3]), rfl⟩
