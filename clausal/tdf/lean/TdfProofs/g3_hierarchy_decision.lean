/-
Guarantee 3, hierarchy, about the decision: a request all of whose labels are of hierarchy attributes is entitled exactly when
every label is at or below the subject's level for its attribute.
Hand-written (plan node T9.7a, fix round). The theorem is named exactly `Rule.tdflite_decision_core.g3_hierarchy_decision` and its type is exactly `Rule.tdflite_decision_core.g3_hierarchy_decision.obligation`
(Local/Obligations.lean, generated from the pieces). ONE-WAY: the sentence follows from the theorems of T9.3 named below; it is in no
link, and nothing shows that it says as much as any statement of T9.3.
THROUGH T9.3: `T93.core_g3_entitled`, `T93.core_g3_hierarchy` (in `TdfProofs.g3_labelled`, `TdfProofs.satisfied_iff`), `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g3_hierarchy_decision : Rule.tdflite_decision_core.g3_hierarchy_decision.obligation := by
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
    obtain ⟨mine, hm, hall⟩ := (TdfProofs.ruleSatisfied_hierarchy hr).mp hs
    obtain ⟨k, hk', hle⟩ := hall x hx ha
    exact ⟨a', mine, k, ha, hm, hk', hle⟩
  · intro H x hx
    obtain ⟨a, mine, k, ha, hm, hk', hle⟩ := H x hx
    obtain ⟨a', ha', hr⟩ := hk x hx
    have e : a' = a := Option.some.inj (ha'.symm.trans ha)
    subst e
    refine ⟨a', ha, (TdfProofs.ruleSatisfied_hierarchy hr).mpr ⟨mine, hm, ?_⟩⟩
    intro j hj hja
    obtain ⟨a2, mine2, k2, ha2, hm2, hk2, hle2⟩ := H j hj
    have e2 : a2 = a' := Option.some.inj (ha2.symm.trans hja)
    subst e2
    have e3 : subject.Level.At mine2 = subject.Level.At mine := Option.some.inj (hm2.symm.trans hm)
    cases e3
    exact ⟨k2, hk2, hle2⟩

/-- The scope is met: the cleared request at the two-level policy (its one attribute is a hierarchy). -/
theorem Rule.tdflite_decision_core.g3_hierarchy_decision.sat : Rule.tdflite_decision_core.g3_hierarchy_decision.in_scope :=
  ⟨TdfProofs.policyOfKind .Hierarchy, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _,
    fun i hi => by
      rw [Tdf.clearedDeclaring, TdfProofs.labels_fixture] at hi
      rw [List.mem_singleton.mp hi]
      exact TdfProofs.ofKind_fixture _⟩
