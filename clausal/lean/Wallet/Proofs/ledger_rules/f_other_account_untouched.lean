/-
Proof of the flat proof obligation `Spec.ledger_rules.f_other_account_untouched.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the vocabulary pieces of this NEW sentence:

    Spec.ledger_rules.f_other_account_untouched.obligation : Prop :=
      (∀ (balances : List U64) (k : Usize) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ True ∧ (¬ L.said ans → (L.bal st' k.val) = (L.bal st k.val)) ∧ (L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-11). The theorem must be named exactly `Spec.ledger_rules.f_other_account_untouched` and its type must be exactly
`Spec.ledger_rules.f_other_account_untouched.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Spec.ledger_rules.f_other_account_untouched.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:156  A rejected transfer leaves every single balance as it was -/
theorem Spec.ledger_rules.f_other_account_untouched : Spec.ledger_rules.f_other_account_untouched.obligation := by
  intro balances k st inp _
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, trivial, ?_, ?_⟩
  · intro hn
    rcases h with ⟨rfl, -⟩ | ⟨-, -, rfl, -⟩
    · exact absurd rfl hn
    · rfl
  · intro _
    rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
    · exact ht
    · rfl
