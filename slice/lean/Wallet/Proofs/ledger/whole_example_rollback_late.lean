/-
Proof of the scenario statement `Spec.ledger.whole_example_rollback_late.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). slicegen created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.whole_example_rollback_late`
and its type must be exactly `Spec.ledger.whole_example_rollback_late.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.All
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:242  A batch applied as a whole is rolled back when its third transfer is invalid -/
theorem Spec.ledger.whole_example_rollback_late : Spec.ledger.whole_example_rollback_late.stmt := by
  intro main h
  -- literal values: the pure model `runN` applies 2 of the 3 transfers, so the batch is rejected
  obtain ⟨⟨b, l'⟩, e, -, hback, -, hx, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main _)
  refine ⟨b, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  obtain rfl := hback hx
  exact ⟨hx, h⟩
