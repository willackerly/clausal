/-
LINK g4b: "never loses acceptance when the subject holds more values or higher levels", said of the entitlement and of the
release, together say exactly what `T93.core_g4b.stmt` and `T93.decide_total.stmt` say.
Hand-written (plan node T9.7a, fix round). `Link.g4b.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: lemmas about reading a list of identifiers as numbers (`T93.mem_of_mem_nats`, `T93.mem_nats`, ...), in
`TdfProofs.atOrAbove_abs` and `TdfProofs.atOrAbove_of_abs`: T9.3 states "at or above" on the specification's reading of the two
subjects, the pack on the subjects. Nothing about the model.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g4b : Link.g4b.claim := by
  unfold Link.g4b.claim
  constructor
  · rintro ⟨O1, O2⟩
    refine ⟨?_, ?_⟩
    · intro s req req' d d' hb hc hdcl hao hd hd'
      obtain ⟨a, _, a2, _, ⟨ha, _⟩, ⟨ha2, _⟩, h1⟩ := O1 s req s req' ⟨rfl, hb, hc, hdcl, (TdfProofs.atOrAbove_of_abs _ _ hao).1, (TdfProofs.atOrAbove_of_abs _ _ hao).2⟩
      obtain ⟨b, _, b2, _, ⟨hb1, _⟩, ⟨hb2, _⟩, h2⟩ := O2 s req s req' ⟨rfl, hb, hc, hdcl, (TdfProofs.atOrAbove_of_abs _ _ hao).1, (TdfProofs.atOrAbove_of_abs _ _ hao).2⟩
      have e1 := TdfProofs.ok_eq ha hd
      have e2 := TdfProofs.ok_eq ha2 hd'
      have e3 := TdfProofs.ok_eq hb1 hd
      have e4 := TdfProofs.ok_eq hb2 hd'
      subst e1 e2
      subst e3 e4
      exact ⟨h1, h2⟩
    · intro s req
      obtain ⟨a, _, _, _, ⟨ha, _⟩, _⟩ := O1 s req s req ⟨rfl, rfl, rfl, rfl, fun _ h => h, fun a n h => ⟨n, h, Nat.le_refl _⟩⟩
      exact ⟨a, ha⟩
  · rintro ⟨S1, S2⟩
    refine ⟨?_, ?_⟩
    · intro st inp st2 inp2 rel
      obtain ⟨rfl, hb, hc, hdcl, hheld, hlv⟩ := rel
      obtain ⟨d, hd⟩ := S2 st2 inp
      obtain ⟨d2, hd2⟩ := S2 st2 inp2
      exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩, (S1 st2 inp inp2 d d2 hb hc hdcl (TdfProofs.atOrAbove_abs _ _ hheld hlv) hd hd2).1⟩
    · intro st inp st2 inp2 rel
      obtain ⟨rfl, hb, hc, hdcl, hheld, hlv⟩ := rel
      obtain ⟨d, hd⟩ := S2 st2 inp
      obtain ⟨d2, hd2⟩ := S2 st2 inp2
      exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩, (S1 st2 inp inp2 d d2 hb hc hdcl (TdfProofs.atOrAbove_abs _ _ hheld hlv) hd hd2).2⟩
