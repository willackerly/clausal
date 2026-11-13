/-
Proof of the flat proof obligation `Rule.intake.accept_only_if_verified.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.intake.accept_only_if_verified.obligation : Prop :=
      (∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message), ∃ (ans : Bool) (st' : sigintake.Key × sigintake.Counter), (sigintake.intake st.1 st.2 inp = ok (ans, st')) ∧ ((In.said ans) → ((In.verifies st.1 inp))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node W6). The theorem must be named exactly `Rule.intake.accept_only_if_verified` and its type must be exactly
`Rule.intake.accept_only_if_verified.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.intake.accept_only_if_verified.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were replaced
here by the intake's own (lean/Intake/Lemmas.lean: what one call of `sigintake.intake` returns, proved once by
stepping through the model).
-/
import Wallet.Obligations
import Intake.Lemmas
open Aeneas Aeneas.Std Result

/-- features/intake.feature:15  Rule: An intake is accepted only if the signature of the message verifies under the expected key -/
theorem Rule.intake.accept_only_if_verified : Rule.intake.accept_only_if_verified.obligation := by
  intro st inp
  obtain ⟨⟨a, s'⟩, e, h, -⟩ := Bdd.ok_of_spec (In.intake_spec st.1 st.2 inp)
  -- a yes comes only with a tag that verifies under the key the call was given, which is the expected key `st.1`
  exact ⟨a, s', e, fun ha => (h.mp ha).1⟩
