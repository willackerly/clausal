/-
Guarantee 3, allOf, about the decision: a request all of whose labels are of allOf attributes is entitled exactly when the subject
holds every label.
Hand-written (plan node T9.7a, fix round). The theorem is named exactly `Rule.tdflite_decision_core.g3_all_of_decision` and its type is exactly `Rule.tdflite_decision_core.g3_all_of_decision.obligation`
(Local/Obligations.lean, generated from the pieces). ONE-WAY: the sentence follows from the theorems of T9.3 named below; it is in no
link, and nothing shows that it says as much as any statement of T9.3.
THROUGH T9.3: `T93.core_g3_entitled`, `T93.core_g3_allOf` (in `TdfProofs.g3_labelled`, `TdfProofs.satisfied_iff`), `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g3_all_of_decision : Rule.tdflite_decision_core.g3_all_of_decision.obligation := by
  intro st inp hu
  obtain ⟨hlab, hk⟩ := hu
  obtain ⟨d, hd, hiff⟩ := TdfProofs.g3_labelled st inp hlab
  refine ⟨d, st, ⟨hd, rfl⟩, hiff.trans ?_⟩
  constructor
  · intro H x hx
    obtain ⟨a, ha, hs⟩ := H x hx
    obtain ⟨a', ha', hr⟩ := hk x hx
    have e : a' = a := Option.some.inj (ha'.symm.trans ha)
    subst e
    exact (TdfProofs.ruleSatisfied_allOf hr).mp hs x hx ha
  · intro H x hx
    obtain ⟨a, ha, hr⟩ := hk x hx
    exact ⟨a, ha, (TdfProofs.ruleSatisfied_allOf hr).mpr (fun j hj _ => H j hj)⟩

/-- The scope is met: the cleared request at the two-level policy with its attribute given the allOf rule. -/
theorem Rule.tdflite_decision_core.g3_all_of_decision.sat : Rule.tdflite_decision_core.g3_all_of_decision.in_scope :=
  ⟨TdfProofs.policyOfKind .AllOf, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _,
    fun i hi => by
      rw [Tdf.clearedDeclaring, TdfProofs.labels_fixture] at hi
      rw [List.mem_singleton.mp hi]
      exact TdfProofs.ofKind_fixture _⟩
