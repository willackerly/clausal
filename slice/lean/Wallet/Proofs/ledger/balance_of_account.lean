/-
Proof of the scenario statement `Spec.ledger.balance_of_account.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.balance_of_account`
and its type must be exactly `Spec.ledger.balance_of_account.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Balance
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:147  Looking up an existing account gives its balance -/
theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt := by
  intro balances i main _ hacc
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec main i)
  refine ⟨o, e, h, ?_⟩
  simp_all [LVocab.isAccount]
