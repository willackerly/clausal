/-
Proof of the flat proof obligation `Rule.ledger_rules.n3_lookup_missing_account.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.n3_lookup_missing_account.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Usize), (¬ ((L.isAccount st inp))) → ∃ (ans : Option U64) (st' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ (¬ ((L.found ans))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Rule.ledger_rules.n3_lookup_missing_account` and its type must be exactly
`Rule.ledger_rules.n3_lookup_missing_account.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.n3_lookup_missing_account.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

Usual recipe: `intro` the variables and hypotheses, get what the call returns from the hand-proved step lemma
of the model function (`Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)`; lean/Ledger/Lemmas/), then
`refine ⟨_, _, e, ?_⟩` and arithmetic. For a straight-line function: `unfold` it and `step*`.
-/
import Wallet.Obligations
import Ledger.Lemmas.Apply
import Ledger.Lemmas.Batch
import Ledger.Lemmas.Total
import Ledger.Lemmas.Balance
import Ledger.Lemmas.All
open Aeneas Aeneas.Std Result

/-- features/ledger_rules.feature:49  Rule: For a lookup for which the account is not an account of the ledger, there is no result -/
theorem Rule.ledger_rules.n3_lookup_missing_account : Rule.ledger_rules.n3_lookup_missing_account.obligation := by
  intro st inp hna
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec st inp)
  refine ⟨o, st, ⟨e, rfl⟩, ?_⟩
  subst h
  simp_all
