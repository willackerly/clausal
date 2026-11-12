/-
LINK g4: "never loses acceptance when the subject holds more values", said of the entitlement and of the release, together say
exactly what `T93.core_g4.stmt` and `T93.decide_total.stmt` say.
Hand-written (plan node T9.7a, fix round). `Link.g4.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: nothing.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g4 : Link.g4.claim := by
  unfold Link.g4.claim
  constructor
  · rintro ⟨O1, O2⟩
    refine ⟨?_, ?_⟩
    · intro s req req' d d' hb hc hdcl hlv hheld hd hd'
      obtain ⟨a, _, a2, _, ⟨ha, _⟩, ⟨ha2, _⟩, h1⟩ := O1 s req s req' ⟨rfl, hb, hc, hdcl, hlv, hheld⟩
      obtain ⟨b, _, b2, _, ⟨hb1, _⟩, ⟨hb2, _⟩, h2⟩ := O2 s req s req' ⟨rfl, hb, hc, hdcl, hlv, hheld⟩
      have e1 := TdfProofs.ok_eq ha hd
      have e2 := TdfProofs.ok_eq ha2 hd'
      have e3 := TdfProofs.ok_eq hb1 hd
      have e4 := TdfProofs.ok_eq hb2 hd'
      subst e1 e2
      subst e3 e4
      exact ⟨h1, h2⟩
    · intro s req
      obtain ⟨a, _, _, _, ⟨ha, _⟩, _⟩ := O1 s req s req ⟨rfl, rfl, rfl, rfl, rfl, fun _ h => h⟩
      exact ⟨a, ha⟩
  · rintro ⟨S1, S2⟩
    refine ⟨?_, ?_⟩
    · intro st inp st2 inp2 rel
      obtain ⟨rfl, hb, hc, hdcl, hlv, hheld⟩ := rel
      obtain ⟨d, hd⟩ := S2 st2 inp
      obtain ⟨d2, hd2⟩ := S2 st2 inp2
      exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩, (S1 st2 inp inp2 d d2 hb hc hdcl hlv hheld hd hd2).1⟩
    · intro st inp st2 inp2 rel
      obtain ⟨rfl, hb, hc, hdcl, hlv, hheld⟩ := rel
      obtain ⟨d, hd⟩ := S2 st2 inp
      obtain ⟨d2, hd2⟩ := S2 st2 inp2
      exact ⟨d, st2, d2, st2, ⟨hd, rfl⟩, ⟨hd2, rfl⟩, (S1 st2 inp inp2 d d2 hb hc hdcl hlv hheld hd hd2).2⟩
