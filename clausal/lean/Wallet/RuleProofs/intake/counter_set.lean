/-
Proof of the flat proof obligation `Rule.intake.counter_set.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.intake.counter_set.obligation : Prop :=
      (∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message), ∀ (ans : Bool) (st' : sigintake.Key × sigintake.Counter), (sigintake.intake st.1 st.2 inp = ok (ans, st')) → (In.said ans → (In.last st'.2) = (In.counterOf inp)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node W6). The theorem must be named exactly `Rule.intake.counter_set` and its type must be exactly
`Rule.intake.counter_set.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.intake.counter_set.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were replaced
here by the intake's own (lean/Intake/Lemmas.lean: what one call of `sigintake.intake` returns, proved once by
stepping through the model).
-/
import Wallet.Obligations
import Intake.Lemmas
open Aeneas Aeneas.Std Result

/-- features/intake.feature:36  Rule: For an accepted intake, the last counter is now the counter of the message -/
theorem Rule.intake.counter_set : Rule.intake.counter_set.obligation := by
  intro st inp ans st' e ha
  have key := Bdd.post_of_spec e (In.intake_spec st.1 st.2 inp)
  -- on a yes the last counter handed back is the message's counter
  have h : st'.2 = { last := inp.counter } := key.2.2.1 ha
  simp [In.last, In.counterOf, h]
