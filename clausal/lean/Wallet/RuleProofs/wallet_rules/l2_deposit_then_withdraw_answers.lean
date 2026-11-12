/-
Proof of the flat proof obligation `Rule.wallet_rules.l2_deposit_then_withdraw_answers.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.wallet_rules.l2_deposit_then_withdraw_answers.obligation : Prop :=
      (∀ (st : wallet.Wallet) (inp : U64), ∃ (ans : W.Answer) (st' : wallet.Wallet), (∃ r_1 s_1, (wallet.Wallet.deposit st inp = ok (r_1, s_1)) ∧ (wallet.Wallet.withdraw s_1 inp = ok (ans, st'))) ∧ True)

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node L2). The theorem must be named exactly `Rule.wallet_rules.l2_deposit_then_withdraw_answers` and its type must be exactly
`Rule.wallet_rules.l2_deposit_then_withdraw_answers.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.wallet_rules.l2_deposit_then_withdraw_answers.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/wallet_rules.feature:10  Rule: A deposit followed by a withdrawal with the same input always answers -/
theorem Rule.wallet_rules.l2_deposit_then_withdraw_answers : Rule.wallet_rules.l2_deposit_then_withdraw_answers.obligation := by
  intro st inp
  -- each of the two calls returns, whatever it is given: step through the model function
  have dep : ∃ r s, wallet.Wallet.deposit st inp = ok (r, s) ∧ True := by
    apply Bdd.ok2_of_spec
    unfold wallet.Wallet.deposit
    step*
  obtain ⟨r₁, s₁, e₁, -⟩ := dep
  have wd : ∃ r s, wallet.Wallet.withdraw s₁ inp = ok (r, s) ∧ True := by
    apply Bdd.ok2_of_spec
    unfold wallet.Wallet.withdraw
    step*
  obtain ⟨r₂, s₂, e₂, -⟩ := wd
  exact ⟨r₂, s₂, ⟨r₁, s₁, e₁, e₂⟩, trivial⟩
