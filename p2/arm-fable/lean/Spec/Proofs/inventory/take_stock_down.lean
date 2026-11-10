/-
Proof of the scenario statement `Spec.inventory.take_stock_down.stmt` (lean/Spec/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.inventory.take_stock_down`
and its type must be exactly `Spec.inventory.take_stock_down.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Straight-line code: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped that way. Helper lemmas may go in
modules of their own under lean/Lemmas/ (library `Lemmas`), imported from here.
-/
import Spec.Statements
import Lemmas.Take
open Aeneas Aeneas.Std Result

/-- features/inventory.feature:111  The product's units go down by exactly the amount taken -/
theorem Spec.inventory.take_stock_down : Spec.inventory.take_stock_down.stmt := by
  intro bins p n main _
  obtain ⟨⟨t, w'⟩, ho, hq1, hq2⟩ := Bdd.ok_of_spec (Lemmas.take_spec main p n)
  refine ⟨t, w', ho, ?_⟩
  have h := Lemmas.stockIn_takeFrom p.val (IVocab.view main) n.val
  show IVocab.stockIn p.val (IVocab.view w') + t.val = IVocab.stockIn p.val (IVocab.view main)
  rw [show IVocab.view w' = _ from hq1, show t.val = _ from hq2]
  exact h
