/-
Proof of the scenario statement `Spec.inventory.fill_at_most.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.fill_at_most`
and its type must be exactly `Spec.inventory.fill_at_most.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.FillOrders
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:159  No more orders are filled than were given -/
theorem Spec.inventory.fill_at_most : Spec.inventory.fill_at_most.stmt := by
  intro bins orders main _
  obtain ⟨c, w', hr, hc, -⟩ := PL.fill_orders_spec main orders
  refine ⟨c, w', hr, ?_⟩
  have := PL.fillFrom_fst_le (IVocab.view main) (IVocab.orderView orders)
  simp only [IVocab.filledAtMost, hc]
  simpa [IVocab.orderView] using this
