/-
Guarantee 3, anyOf, about the decision: a request all of whose labels are of anyOf attributes is entitled exactly when, for every
label, the subject holds some label of the request of the same attribute.
Hand-written (plan node T9.7a, fix round). The theorem is named exactly `Rule.tdflite_decision_core.g3_any_of_decision` and its type is exactly `Rule.tdflite_decision_core.g3_any_of_decision.obligation`
(Local/Obligations.lean, generated from the pieces). ONE-WAY: the sentence follows from the theorems of T9.3 named below; it is in no
link, and nothing shows that it says as much as any statement of T9.3.
THROUGH T9.3: `T93.core_g3_entitled`, `T93.core_g3_anyOf` (in `TdfProofs.g3_labelled`, `TdfProofs.satisfied_iff`), `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g3_any_of_decision : Rule.tdflite_decision_core.g3_any_of_decision.obligation := by
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
    obtain ⟨j, hj, hja, hh⟩ := (TdfProofs.ruleSatisfied_anyOf hr).mp hs
    exact ⟨a', ha, j, hj, hja, hh⟩
  · intro H x hx
    obtain ⟨a, ha, j, hj, hja, hh⟩ := H x hx
    obtain ⟨a', ha', hr⟩ := hk x hx
    have e : a' = a := Option.some.inj (ha'.symm.trans ha)
    subst e
    exact ⟨a', ha, (TdfProofs.ruleSatisfied_anyOf hr).mpr ⟨j, hj, hja, hh⟩⟩

/-- The scope is met: the cleared request at the two-level policy with its attribute given the anyOf rule. -/
theorem Rule.tdflite_decision_core.g3_any_of_decision.sat : Rule.tdflite_decision_core.g3_any_of_decision.in_scope :=
  ⟨TdfProofs.policyOfKind .AnyOf, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _,
    fun i hi => by
      rw [Tdf.clearedDeclaring, TdfProofs.labels_fixture] at hi
      rw [List.mem_singleton.mp hi]
      exact TdfProofs.ofKind_fixture _⟩
