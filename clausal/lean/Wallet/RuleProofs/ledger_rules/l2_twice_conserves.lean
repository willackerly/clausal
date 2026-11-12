/-
Proof of the flat proof obligation `Rule.ledger_rules.l2_twice_conserves.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.l2_twice_conserves.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (∃ r_1 s_1, (ledger.Ledger.apply st inp = ok (r_1, s_1)) ∧ (ledger.Ledger.apply s_1 inp = ok (ans, st'))) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node L2). The theorem must be named exactly `Rule.ledger_rules.l2_twice_conserves` and its type must be exactly
`Rule.ledger_rules.l2_twice_conserves.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.l2_twice_conserves.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:218  Rule: A transfer followed by a transfer with the same input never changes the total of the ledger's balances -/
theorem Rule.ledger_rules.l2_twice_conserves : Rule.ledger_rules.l2_twice_conserves.obligation := by
  intro st inp
  obtain ⟨⟨a₁, l₁⟩, e₁, h₁⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  obtain ⟨⟨a₂, l₂⟩, e₂, h₂⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec l₁ inp)
  refine ⟨a₂, l₂, ⟨a₁, l₁, e₁, e₂⟩, ?_⟩
  have t₁ : LVocab.total l₁ = LVocab.total st := by
    rcases h₁ with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
    · exact ht
    · rfl
  have t₂ : LVocab.total l₂ = LVocab.total l₁ := by
    rcases h₂ with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
    · exact ht
    · rfl
  exact t₂.trans t₁
