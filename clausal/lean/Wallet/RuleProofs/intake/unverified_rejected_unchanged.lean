/-
Proof of the flat proof obligation `Rule.intake.unverified_rejected_unchanged.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.intake.unverified_rejected_unchanged.obligation : Prop :=
      (∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message), (¬ ((In.verifies st.1 inp))) → ∃ (ans : Bool) (st' : sigintake.Key × sigintake.Counter), (sigintake.intake st.1 st.2 inp = ok (ans, st')) ∧ (¬ (In.said ans) ∧ st' = st))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node W6). The theorem must be named exactly `Rule.intake.unverified_rejected_unchanged` and its type must be exactly
`Rule.intake.unverified_rejected_unchanged.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.intake.unverified_rejected_unchanged.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were replaced
here by the intake's own (lean/Intake/Lemmas.lean: what one call of `sigintake.intake` returns, proved once by
stepping through the model).
-/
import Wallet.Obligations
import Intake.Lemmas
open Aeneas Aeneas.Std Result

/-- features/intake.feature:19  Rule: An intake for which the signature of the message does not verify under the expected key is rejected and changes nothing -/
theorem Rule.intake.unverified_rejected_unchanged : Rule.intake.unverified_rejected_unchanged.obligation := by
  intro st inp hnv
  obtain ⟨⟨a, s'⟩, e, h, hk, -, hno⟩ := Bdd.ok_of_spec (In.intake_spec st.1 st.2 inp)
  have ha : a = false := by
    cases a with
    | false => rfl
    | true => exact absurd (h.mp rfl).1 hnv
  subst ha
  -- on a no the key and the last counter are handed back as they were
  have h2 : s'.2 = st.2 := hno rfl
  have h1 : s'.1 = st.1 := hk
  exact ⟨false, s', e, by simp, Prod.ext h1 h2⟩
