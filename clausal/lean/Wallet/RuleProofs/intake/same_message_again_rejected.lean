/-
Proof of the flat proof obligation `Rule.intake.same_message_again_rejected.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.intake.same_message_again_rejected.obligation : Prop :=
      (∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message), ∃ (ans : Bool) (st' : sigintake.Key × sigintake.Counter), (∃ r_1 s_1, (sigintake.intake st.1 st.2 inp = ok (r_1, s_1)) ∧ (sigintake.intake s_1.1 s_1.2 inp = ok (ans, st'))) ∧ (¬ ((In.said ans))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node W6). The theorem must be named exactly `Rule.intake.same_message_again_rejected` and its type must be exactly
`Rule.intake.same_message_again_rejected.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.intake.same_message_again_rejected.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were replaced
here by the intake's own (lean/Intake/Lemmas.lean: what one call of `sigintake.intake` returns, proved once by
stepping through the model).
-/
import Wallet.Obligations
import Intake.Lemmas
open Aeneas Aeneas.Std Result

/-- features/intake.feature:40  Rule: An intake followed by an intake with the same input is always rejected -/
theorem Rule.intake.same_message_again_rejected : Rule.intake.same_message_again_rejected.obligation := by
  intro st inp
  obtain ⟨⟨a1, s1⟩, e1, h1, hk1, hy1, hn1⟩ := Bdd.ok_of_spec (In.intake_spec st.1 st.2 inp)
  obtain ⟨⟨a2, s2⟩, e2, h2, -⟩ := Bdd.ok_of_spec (In.intake_spec s1.1 s1.2 inp)
  refine ⟨a2, s2, ⟨a1, s1, e1, e2⟩, ?_⟩
  intro ha2
  obtain ⟨hv, hlt⟩ := h2.mp ha2
  have hk : s1.1 = st.1 := hk1
  cases a1 with
  | true =>
    -- the first call was accepted: the last counter is now this message's counter, which is not above itself
    have hs : s1.2 = { last := inp.counter } := hy1 rfl
    rw [hs] at hlt
    exact absurd hlt (lt_irrefl _)
  | false =>
    -- the first call was rejected and changed nothing: the second call sees what the first saw, and answers the same
    have hs : s1.2 = st.2 := hn1 rfl
    rw [hs] at hlt
    rw [hk] at hv
    have : (false : Bool) = true := h1.mpr ⟨hv, hlt⟩
    exact absurd this (by simp)
