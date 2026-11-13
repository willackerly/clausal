/-
LINK g2: "accepted only if every label of the request is defined by the policy" says exactly what `T93.core_g2.stmt` and
`T93.decide_total.stmt` say.
Hand-written (plan node T9.7a, fix round). `Link.g2.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: nothing.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g2 : Link.g2.claim := by
  unfold Link.g2.claim
  constructor
  · intro O
    refine ⟨?_, ?_⟩
    · intro s req d ids hd he hb i hi
      obtain ⟨ans, _, ⟨ha, _⟩, h⟩ := O s req
      have e := TdfProofs.ok_eq ha hd
      subst e
      exact h he i (by rw [TdfProofs.labels_of hb]; exact hi)
    · intro s req
      obtain ⟨ans, _, ⟨ha, _⟩, _⟩ := O s req
      exact ⟨ans, ha⟩
  · rintro ⟨S1, S2⟩
    intro st inp
    obtain ⟨d, hd⟩ := S2 st inp
    refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
    intro he
    intro x hx
    cases hb : inp.bound with
    | Unresolved => simp [Abac.labels, hb] at hx
    | Labels ids =>
      simp only [Abac.labels, hb] at hx
      exact S1 st inp d ids hd he hb x hx
