/-
Witness (T9.3 `witness_denied`) as a refutation: holding something does not entitle to a labelled object.
Hand-written (plan node T9.7a). `Rule.tdflite_decision_core.w_holding_not_enough.refuted : ¬ Rule.tdflite_decision_core.w_holding_not_enough.obligation`: the sentence is FALSE, at the named input
(`Tdf.twoLevelPolicy`, `Tdf.noLevel`). The overlay run derives `¬ reading` through the kernel-checked equivalence and checks its type and axioms.
THROUGH T9.3: `T93.decide_total`, `T93.decide_refines` (what the model answers at that input). The input is the one
T9.3's witness theorem is proved at; it was named by hand, not found by a search.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.w_holding_not_enough.refuted : ¬ Rule.tdflite_decision_core.w_holding_not_enough.obligation := by
  intro h
  obtain ⟨d, _, ⟨hd, _⟩, himp⟩ := h Tdf.twoLevelPolicy Tdf.noLevel (TdfProofs.labelled_fixture _ _ _)
  have e : d.entitled = true := himp (Or.inl (by simp [Tdf.noLevel, Tdf.requestWith, Tdf.vec3]))
  rw [TdfProofs.at_noLevel d hd] at e
  cases e
