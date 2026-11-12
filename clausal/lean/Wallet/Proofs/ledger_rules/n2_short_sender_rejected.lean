/-
Proof of the flat proof obligation `Spec.ledger_rules.n2_short_sender_rejected.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Spec.ledger_rules.n2_short_sender_rejected.obligation : Prop :=
      (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ((L.bal st (L.sender inp)) < (L.amountOf inp)) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (¬ ((L.said ans))) ∧ ((L.balances st') = (L.balances st)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Spec.ledger_rules.n2_short_sender_rejected` and its type must be exactly
`Spec.ledger_rules.n2_short_sender_rejected.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Spec.ledger_rules.n2_short_sender_rejected.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:35  a transfer of more than the sender holds is rejected and changes nothing -/
theorem Spec.ledger_rules.n2_short_sender_rejected : Spec.ledger_rules.n2_short_sender_rejected.obligation := by
  intro balances st inp _ hlt
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  rcases h with ⟨-, hv, -⟩ | ⟨rfl, -, rfl, -⟩
  · exfalso
    have hc : inp.amount.val ≤ LVocab.bal st inp.from.val := hv.2.2.2.1
    have hlt' : LVocab.bal st inp.from.val < inp.amount.val := hlt
    omega
  · exact ⟨by simp, rfl⟩
