/-
LINK g5: the five sentences of guarantee 5 (released implies entitled; released implies every listed obligation declared;
nothing listed when not entitled; when entitled the list is the required one; entitled with every required obligation
declared implies released), together, say exactly what `T93.core_g5.stmt` says.
Hand-written (plan node T9.7a, fix round). `Link.g5.claim` is generated from tdf/links.yaml (Local/Links.lean). The run counts
this theorem only if its type is exactly the claim, its axioms are the standard three, and its proof uses no theorem of a
statement of the link, no proof of a sentence of the link, and no theorem of T9.3 outside the link's `given`.
GIVEN: `T93.mem_nats` (an identifier is in a list exactly when its number is in the list of numbers). Nothing about the model.
-/
import Local.Links
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

theorem Link.g5 : Link.g5.claim := by
  unfold Link.g5.claim
  constructor
  · rintro ⟨O1, O2, O3, O4, O5⟩
    intro s req d hd
    have hd' : decide.decide s req = ok d ∧ s = s := ⟨hd, rfl⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
    · intro hr
      refine ⟨O1 s req d s hd' hr, ?_⟩
      intro o ho
      have h1 : o.val ∈ T93.nats req.declared.val := O2 s req d s hd' hr o.val (List.mem_map.mpr ⟨o, ho, rfl⟩)
      exact (T93.mem_nats req.declared.val o).mp h1
    · rintro ⟨he, hall⟩
      refine O5 s req ?_ d s hd' he
      intro x hx
      have hl : T93.nats d.listed.val = Tdf.requiredList s req := O4 s req d s hd' he
      rw [← hl] at hx
      obtain ⟨o, ho, rfl⟩ := List.mem_map.mp hx
      exact List.mem_map.mpr ⟨o, hall o ho, rfl⟩
    · intro he
      have hc : d.listed.val.length = 0 := O3 s req d s hd' (by simp [he])
      exact List.eq_nil_of_length_eq_zero hc
    · intro he
      exact O4 s req d s hd' he
  · intro S
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · intro st inp d st' hd hr
      exact ((S st inp d hd.1).1.mp hr).1
    · intro st inp d st' hd hr x hx
      obtain ⟨o, ho, rfl⟩ := List.mem_map.mp hx
      exact List.mem_map.mpr ⟨o, ((S st inp d hd.1).1.mp hr).2 o ho, rfl⟩
    · intro st inp d st' hd hn
      have he : d.entitled = false := by
        cases h : d.entitled with
        | false => rfl
        | true => exact absurd h hn
      have hl := (S st inp d hd.1).2.1 he
      simp [Abac.listedCount, hl]
    · intro st inp d st' hd he
      exact (S st inp d hd.1).2.2 he
    · intro st inp hall d st' hd he
      refine (S st inp d hd.1).1.mpr ⟨he, ?_⟩
      intro o ho
      have hl : T93.nats d.listed.val = Tdf.requiredList st inp := (S st inp d hd.1).2.2 he
      have h1 : o.val ∈ Tdf.requiredList st inp := by
        rw [← hl]
        exact (T93.mem_nats d.listed.val o).mpr ho
      exact (T93.mem_nats inp.declared.val o).mp (hall o.val h1)
