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
import Lemmas.Fill
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:159  No more orders are filled than were given -/
theorem Spec.inventory.fill_at_most : Spec.inventory.fill_at_most.stmt := by
  intro bins orders main _
  obtain ⟨⟨c, w'⟩, ho, hq1, hq2⟩ := Bdd.ok_of_spec (Lemmas.fill_orders_spec main orders)
  refine ⟨c, w', ho, ?_⟩
  have h := Lemmas.fillFrom_le (orders.val.map Lemmas.ow) (main.bins.val.map Lemmas.vw)
  simp only [List.length_map] at h
  show c.val ≤ orders.val.length
  rw [show c.val = _ from hq1]
  exact h
