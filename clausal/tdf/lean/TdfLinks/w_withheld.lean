/-
LINK w_withheld (negated): the sentence "For an accepted entitlement decision, the key is released" is FALSE exactly when
`T93.witness_withheld.stmt` holds (some entitled subject is refused the key).
Hand-written (plan node T9.7a, fix round). `Link.w_withheld.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: nothing.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.w_withheld : Link.w_withheld.claim := by
  unfold Link.w_withheld.claim
  constructor
  · intro hn
    apply Classical.byContradiction
    intro hw
    apply hn
    intro st inp d st' hd he
    show d.release = true
    cases hr : d.release with
    | true => rfl
    | false => exact absurd ⟨st, inp, d, hd.1, he, hr⟩ hw
  · rintro ⟨s, req, d, hd, he, hr⟩ O
    have h1 : d.release = true := O s req d s ⟨hd, rfl⟩ he
    rw [hr] at h1
    cases h1
