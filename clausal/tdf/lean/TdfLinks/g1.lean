/-
LINK g1: the three sentences of guarantee 1 (an unresolved, an unlabelled, a labelled request), together, say exactly
what `T93.core_g1.stmt` and `T93.decide_total.stmt` say.
Hand-written (plan node T9.7a, fix round). `Link.g1.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: nothing. Both directions are by the meaning of the words: a request is unresolved, or carries no label, or carries one.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g1 : Link.g1.claim := by
  unfold Link.g1.claim
  constructor
  · rintro ⟨O1, O2, O3⟩
    constructor
    · intro s req d hd he
      cases hb : req.bound with
      | Unresolved =>
        obtain ⟨ans, _, ⟨ha, _⟩, hn⟩ := O1 s req hb
        have e := TdfProofs.ok_eq ha hd
        subst e
        exact absurd he hn
      | Labels ids =>
        refine ⟨ids, rfl, ?_⟩
        by_cases h0 : ids.val = []
        · left
          obtain ⟨ans, _, ⟨ha, _⟩, hi⟩ := O2 s req ⟨ids, hb, h0⟩
          have e := TdfProofs.ok_eq ha hd
          subst e
          exact ⟨h0, hi he⟩
        · right
          obtain ⟨ans, _, ⟨ha, _⟩, hi⟩ := O3 s req ⟨ids, hb, h0⟩
          have e := TdfProofs.ok_eq ha hd
          subst e
          exact ⟨h0, hi he⟩
    · intro s req
      cases hb : req.bound with
      | Unresolved =>
        obtain ⟨ans, _, ⟨ha, _⟩, _⟩ := O1 s req hb
        exact ⟨ans, ha⟩
      | Labels ids =>
        by_cases h0 : ids.val = []
        · obtain ⟨ans, _, ⟨ha, _⟩, _⟩ := O2 s req ⟨ids, hb, h0⟩
          exact ⟨ans, ha⟩
        · obtain ⟨ans, _, ⟨ha, _⟩, _⟩ := O3 s req ⟨ids, hb, h0⟩
          exact ⟨ans, ha⟩
  · rintro ⟨S1, S2⟩
    refine ⟨?_, ?_, ?_⟩
    · intro st inp hu
      obtain ⟨d, hd⟩ := S2 st inp
      refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
      intro he
      obtain ⟨ids, hb, _⟩ := S1 st inp d hd he
      have hu' : inp.bound = .Unresolved := hu
      rw [hu'] at hb
      cases hb
    · intro st inp hu
      obtain ⟨d, hd⟩ := S2 st inp
      refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
      intro he
      obtain ⟨ids0, hb0, h0⟩ := hu
      obtain ⟨ids, hb, h⟩ := S1 st inp d hd he
      rw [hb0] at hb
      cases hb
      rcases h with ⟨_, hdeny⟩ | ⟨hne, _⟩
      · exact hdeny
      · exact absurd h0 hne
    · intro st inp hu
      obtain ⟨d, hd⟩ := S2 st inp
      refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
      intro he
      obtain ⟨ids0, hb0, h0⟩ := hu
      obtain ⟨ids, hb, h⟩ := S1 st inp d hd he
      rw [hb0] at hb
      cases hb
      rcases h with ⟨he0, _⟩ | ⟨_, hh⟩
      · exact absurd he0 h0
      · exact hh
