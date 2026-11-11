/-
Proof of the flat proof obligation `Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation` (lean/Wallet/Obligations.lean), which slicegen
generated from the vocabulary pieces of this NEW sentence:

    Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation : Prop :=
      (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

Hand-written (by a person or an agent). slicegen created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Spec.ledger_rules.readme_transfer_keeps_aggregate` and its type must be exactly
`Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Spec.ledger_rules.readme_transfer_keeps_aggregate.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:17  a transfer between two accounts of the ledger -/
theorem Spec.ledger_rules.readme_transfer_keeps_aggregate : Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation := by
  intro balances st inp _
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
  · exact ht
  · rfl
