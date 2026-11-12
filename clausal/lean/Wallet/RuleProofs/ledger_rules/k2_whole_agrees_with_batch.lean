/-
Proof of the flat proof obligation `Rule.ledger_rules.k2_whole_agrees_with_batch.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.k2_whole_agrees_with_batch.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply_all st inp = ok (ans, st')) ∧ ((ans, st') = L.refWholeByBatch st inp))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-11, plan node E1). The theorem must be named exactly `Rule.ledger_rules.k2_whole_agrees_with_batch` and its type must be exactly
`Rule.ledger_rules.k2_whole_agrees_with_batch.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.k2_whole_agrees_with_batch.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:123  Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied -/
theorem Rule.ledger_rules.k2_whole_agrees_with_batch : Rule.ledger_rules.k2_whole_agrees_with_batch.obligation := by
  intro st inp
  obtain ⟨⟨a, st'⟩, e, -, hrej, -, hdec, hacc⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec st inp)
  obtain ⟨⟨n, l'⟩, eb, -, -, -, hrun⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec st inp)
  refine ⟨a, st', e, ?_⟩
  have h1 : (ledger.runN (ledger.nums st) inp.val).1 = n.val := by rw [← hrun]
  have h2 : (ledger.runN (ledger.nums st) inp.val).2 = ledger.nums l' := by rw [← hrun]
  simp only at hrej hdec hacc
  simp only [L.refWholeByBatch, eb, Bdd.toOption_ok]
  by_cases hn : n.val = inp.val.length
  · have ha : a = true := by rw [hdec, h1]; simp [hn]
    subst ha
    have hv : st'.balances.val = l'.balances.val := ledger.holds_of_nums (by rw [hacc rfl, h2]; rfl)
    have hl : st' = l' := by
      cases st' with | mk b1 => cases l' with | mk b2 =>
        simp only [ledger.Ledger.mk.injEq]
        exact (alloc.vec.Vec.eq_iff b1 b2).mpr hv
    simp [hn, hl]
  · have ha : a = false := by rw [hdec, h1]; simp [hn]
    subst ha
    simp [hn, hrej rfl]
