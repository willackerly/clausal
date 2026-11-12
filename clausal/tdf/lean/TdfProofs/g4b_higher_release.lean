/-
Guarantee 4b, said of the release.
Hand-written (plan node T9.7a). The theorem is named exactly `Rule.tdflite_decision_core.g4b_higher_release` and its type is exactly
`Rule.tdflite_decision_core.g4b_higher_release.obligation` (Local/Obligations.lean, generated from the pieces); the overlay run checks both, and
kernel-checks that the obligation is equivalent to the compiled reading.
THROUGH T9.3: `T93.core_g4b`, `T93.decide_total`. Nothing about the model is proved here from scratch.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Rule.tdflite_decision_core.g4b_higher_release : Rule.tdflite_decision_core.g4b_higher_release.obligation := by
  intro st inp st2 inp2 rel
  obtain ⟨rfl, hb, hc, hdcl, hheld, hlv⟩ := rel
  obtain ⟨d, hd⟩ := T93.decide_total st2 inp
  obtain ⟨d2, hd2⟩ := T93.decide_total st2 inp2
  exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩,
    (T93.core_g4b st2 inp inp2 d d2 hb hc hdcl (TdfProofs.atOrAbove_abs _ _ hheld hlv) hd hd2).2⟩
