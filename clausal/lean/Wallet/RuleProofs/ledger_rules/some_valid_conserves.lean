/-
Proof of the flat proof obligation `Rule.ledger_rules.some_valid_conserves.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.some_valid_conserves.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), (Frames.someOf ((L.transfers inp)) (fun x => (L.valid st x))) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Rule.ledger_rules.some_valid_conserves` and its type must be exactly
`Rule.ledger_rules.some_valid_conserves.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.some_valid_conserves.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:110  Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger -/
theorem Rule.ledger_rules.some_valid_conserves : Rule.ledger_rules.some_valid_conserves.obligation := by
  intro st inp _
  obtain ⟨⟨n, l'⟩, e, ht, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec st inp)
  exact ⟨n, l', e, ht⟩
