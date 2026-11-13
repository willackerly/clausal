/-
Witness (T9.3 `witness_withheld`) as a refutation: an entitled subject is not always given the key.
Hand-written (plan node T9.7a). `Rule.tdflite_decision_core.w_entitled_not_released.refuted : ¬ Rule.tdflite_decision_core.w_entitled_not_released.obligation`: the sentence is FALSE, at the named input
(`Tdf.twoLevelPolicy`, `Tdf.clearedSilent`). The overlay run derives `¬ reading` through the kernel-checked equivalence and checks its type and axioms.
THROUGH T9.3: `T93.decide_total`, `T93.decide_refines` (what the model answers at that input). The input is the one
T9.3's witness theorem is proved at; it was named by hand, not found by a search.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.w_entitled_not_released.refuted : ¬ Rule.tdflite_decision_core.w_entitled_not_released.obligation := by
  intro h
  obtain ⟨d, hd⟩ := T93.decide_total Tdf.twoLevelPolicy Tdf.clearedSilent
  have a := TdfProofs.at_clearedSilent d hd
  have r : d.release = true := h Tdf.twoLevelPolicy Tdf.clearedSilent d Tdf.twoLevelPolicy ⟨hd, rfl⟩ a.1
  rw [a.2] at r
  cases r
