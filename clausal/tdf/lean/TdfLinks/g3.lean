/-
LINK g3: "for a labelled request, entitled exactly when every label is satisfied under the policy" says exactly what
`T93.core_g3_entitled.stmt` says.
Hand-written (plan node T9.7a, fix round). `Link.g3.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: `T93.decide_total` (the sentence is about labelled requests only, so it does not give totality back), and, in
`TdfProofs.satisfied_iff`, that the model's attribute check computes the pack's rule: `T93.core_g3_hierarchy`, `T93.core_g3_allOf`,
`T93.core_g3_anyOf`, `T93.satisfied_refines`, `T93.idspec_g3_norule`, `T93.deref_val`.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g3 : Link.g3.claim := by
  unfold Link.g3.claim
  constructor
  · intro O s req d ids hd hb hne
    obtain ⟨ans, _, ⟨ha, _⟩, hiff⟩ := O s req ⟨ids, hb, hne⟩
    have e := TdfProofs.ok_eq ha hd
    subst e
    have hl : Abac.labels req = ids.val := TdfProofs.labels_of hb
    constructor
    · intro he i hi
      obtain ⟨a, ha', hs⟩ := hiff.mp he i (by rw [hl]; exact hi)
      rw [hl] at hs
      exact ⟨a, ha', (TdfProofs.satisfied_iff s req.subject a ids).mpr hs⟩
    · intro H
      refine hiff.mpr ?_
      intro i hi
      rw [hl] at hi
      obtain ⟨a, ha', hs⟩ := H i hi
      exact ⟨a, ha', by rw [hl]; exact (TdfProofs.satisfied_iff s req.subject a ids).mp hs⟩
  · intro S st inp hu
    obtain ⟨d, hd⟩ := T93.decide_total st inp
    refine ⟨d, st, ⟨hd, rfl⟩, ?_⟩
    obtain ⟨ids, hb, hne⟩ := hu
    have key := S st inp d ids hd hb hne
    have hl : Abac.labels inp = ids.val := TdfProofs.labels_of hb
    constructor
    · intro he x hx
      rw [hl] at hx
      obtain ⟨a, ha, hs⟩ := key.mp he x hx
      exact ⟨a, ha, by rw [hl]; exact (TdfProofs.satisfied_iff st inp.subject a ids).mp hs⟩
    · intro H
      refine key.mpr ?_
      intro i hi
      obtain ⟨a, ha, hs⟩ := H i (by rw [hl]; exact hi)
      rw [hl] at hs
      exact ⟨a, ha, (TdfProofs.satisfied_iff st inp.subject a ids).mpr hs⟩
