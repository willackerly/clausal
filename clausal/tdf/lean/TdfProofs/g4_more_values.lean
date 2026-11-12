/-
Guarantee 4 (restricted form): the same levels and more values never lose the entitlement.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g4_more_values` and its type is exactly
`Rule.tdflite_decision_core.g4_more_values.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g4`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g4_more_values : Rule.tdflite_decision_core.g4_more_values.obligation := by
  intro st inp st2 inp2 rel
  obtain ⟨rfl, hb, hc, hdcl, hlv, hheld⟩ := rel
  obtain ⟨d, hd⟩ := T93.decide_total st2 inp
  obtain ⟨d2, hd2⟩ := T93.decide_total st2 inp2
  exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩, (T93.core_g4 st2 inp inp2 d d2 hb hc hdcl hlv hheld hd hd2).1⟩
