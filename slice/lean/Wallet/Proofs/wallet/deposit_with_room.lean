/-
Proof of the scenario statement `Spec.wallet.deposit_with_room.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.wallet.deposit_with_room`
and its type must be exactly `Spec.wallet.deposit_with_room.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
-/
import Wallet.Statements
open Aeneas Aeneas.Std Result

/-- features/wallet.feature:64  A deposit with room succeeds and adds exactly the amount -/
theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
