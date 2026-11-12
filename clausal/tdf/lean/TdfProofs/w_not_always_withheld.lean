/-
Witness (T9.3 `witness_release`) as a refutation: not every labelled object is withheld.
Hand-written (plan node T9.7a). `Rule.tdflite_decision_core.w_not_always_withheld.refuted : ¬ Rule.tdflite_decision_core.w_not_always_withheld.obligation`: the sentence is FALSE, at the named input
(`Tdf.twoLevelPolicy`, `Tdf.clearedDeclaring`). The overlay run derives `¬ reading` through the kernel-checked equivalence and checks its type and axioms.
THROUGH T9.3: `T93.decide_total`, `T93.decide_refines` (what the model answers at that input). The input is the one
T9.3's witness theorem is proved at; it was named by hand, not found by a search.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.w_not_always_withheld.refuted : ¬ Rule.tdflite_decision_core.w_not_always_withheld.obligation := by
  intro h
  obtain ⟨d, _, ⟨hd, _⟩, hn⟩ := h Tdf.twoLevelPolicy Tdf.clearedDeclaring (TdfProofs.labelled_fixture _ _ _)
  exact hn (TdfProofs.at_clearedDeclaring d hd).2
