/-
The allOf line with its scope said as "every label of the request is of an allOf attribute": FALSE.
Hand-written (plan node T9.7a, fix round). `Rule.tdflite_decision_core.g3_all_of_unscoped.refuted : ¬ Rule.tdflite_decision_core.g3_all_of_unscoped.obligation`, at the named input
(`Tdf.twoLevelPolicy`, `Tdf.unresolvedRequest`): an unresolved request has no label, so it is in the scope and "every label is held" is
true of it, and it is never entitled.
THROUGH T9.3: `T93.decide_total` (the decision at that input), `T93.core_g1` (an entitled request records a list of labels).
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g3_all_of_unscoped.refuted : ¬ Rule.tdflite_decision_core.g3_all_of_unscoped.obligation := by
  intro h
  have hnil : Abac.labels Tdf.unresolvedRequest = [] := rfl
  obtain ⟨d, hd⟩ := T93.decide_total Tdf.twoLevelPolicy Tdf.unresolvedRequest
  obtain ⟨ans, _, ⟨ha, _⟩, hiff⟩ := h Tdf.twoLevelPolicy Tdf.unresolvedRequest (by intro x hx; rw [hnil] at hx; cases hx)
  have e := TdfProofs.ok_eq ha hd
  subst e
  have he : ans.entitled = true := hiff.mpr (by intro x hx; rw [hnil] at hx; cases hx)
  obtain ⟨ids, hb, _⟩ := T93.core_g1 Tdf.twoLevelPolicy Tdf.unresolvedRequest ans hd he
  have hb' : request.Bound.Unresolved = request.Bound.Labels ids := hb
  cases hb'
