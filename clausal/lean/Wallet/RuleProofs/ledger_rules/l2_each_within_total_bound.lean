/-
Proof of the flat proof obligation `Rule.ledger_rules.l2_each_within_total_bound.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.l2_each_within_total_bound.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ((Frames.aggregate (((L.balances st).map L.amount))) ≤ (L.amountOf inp)) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (∀ num_ ∈ ((L.balances st').map L.amount), num_ ≤ (L.amountOf inp)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node L2). The theorem must be named exactly `Rule.ledger_rules.l2_each_within_total_bound` and its type must be exactly
`Rule.ledger_rules.l2_each_within_total_bound.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.l2_each_within_total_bound.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:209  Rule: For a transfer for which the total of the ledger's balances is at most the amount of the transfer, each of the ledger's balances is afterwards at most the amount of the transfer -/
theorem Rule.ledger_rules.l2_each_within_total_bound : Rule.ledger_rules.l2_each_within_total_bound.obligation := by
  intro st inp hle
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  -- the total after the call is the total before it: conserved if accepted, the same ledger if rejected
  have ht : (((L.balances l').map L.amount)).sum = (((L.balances st).map L.amount)).sum := by
    rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
    · exact ht
    · rfl
  intro n hn
  exact (List.single_le_sum (fun _ _ => Nat.zero_le _) n hn).trans (ht ▸ hle)
