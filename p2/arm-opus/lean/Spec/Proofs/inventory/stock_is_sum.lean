/-
Proof of the scenario statement `Spec.inventory.stock_is_sum.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.stock_is_sum`
and its type must be exactly `Spec.inventory.stock_is_sum.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.StockOf
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:15  The count of a product's units is the sum over its bins -/
theorem Spec.inventory.stock_is_sum : Spec.inventory.stock_is_sum.stmt := by
  intro bins p main _ hfit
  obtain ⟨r, hr, h1, h2⟩ := PL.stock_of_spec main p
  refine ⟨r, hr, ?_⟩
  cases r with
  | none => exact absurd hfit (Nat.not_le.mpr (h2 rfl))
  | some s => simp [h1 s rfl]
