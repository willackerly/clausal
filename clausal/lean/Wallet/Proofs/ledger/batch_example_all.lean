/-
Proof of the scenario statement `Spec.ledger.batch_example_all.stmt` (lean/Wallet/Statements.lean).

Hand-written (by a person or an agent). clausal created this file as a `sorry`
stub and never edits it again. The theorem must be named exactly `Spec.ledger.batch_example_all`
and its type must be exactly `Spec.ledger.batch_example_all.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

Usual recipe: `intro` the variables and Givens, `apply Bdd.okN_of_spec` (N = number
of things the call returns), `unfold` the model function, `step*`, then arithmetic.
A call with a loop cannot be unfolded and stepped: use its hand-proved `@[step]` lemma
(lean/Ledger/Lemmas/), which carries the loop invariant.
-/
import Wallet.Statements
import Ledger.Lemmas.Batch
open Aeneas Aeneas.Std Result

/-- features/ledger.feature:49  A batch of two valid transfers is applied in full -/
theorem Spec.ledger.batch_example_all : Spec.ledger.batch_example_all.stmt := by
  intro main h
  -- literal values: take the exact result of the loop (the pure model `runN`) and compute it
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main _)
  refine ⟨n, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  refine ⟨?_, ledger.holds_of_nums (by simpa [ledger.nums] using hx.2)⟩
  simp only [LVocab.appliedExactly]; scalar_tac
