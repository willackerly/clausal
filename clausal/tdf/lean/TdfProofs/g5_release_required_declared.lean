/-
Guarantee 5, the "only if" half said of what is required: a key is released only if every required obligation was declared.
Hand-written (plan node T9.7a, fix round). The theorem is named exactly `Rule.tdflite_decision_core.g5_release_required_declared` and its type is exactly `Rule.tdflite_decision_core.g5_release_required_declared.obligation`
(Local/Obligations.lean, generated from the pieces). ONE-WAY: the sentence follows from the theorems of T9.3 named below; it is in no
link, and nothing shows that it says as much as any statement of T9.3.
THROUGH T9.3: `T93.core_g5`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g5_release_required_declared : Rule.tdflite_decision_core.g5_release_required_declared.obligation := by
  intro st inp
  obtain ⟨d, hd⟩ := T93.decide_total st inp
  refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
  intro hr x hx
  have h5 := T93.core_g5 st inp d hd
  obtain ⟨he, hall⟩ := h5.1.mp hr
  have hl : T93.nats d.listed.val = Tdf.requiredList st inp := h5.2.2 he
  rw [← hl] at hx
  obtain ⟨o, ho, rfl⟩ := List.mem_map.mp hx
  exact List.mem_map.mpr ⟨o, hall o ho, rfl⟩
