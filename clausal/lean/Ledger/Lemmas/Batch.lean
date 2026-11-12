import Ledger.Lemmas.Apply
open Aeneas Aeneas.Std Result

/- `Ledger::apply_batch`: THE loop invariant, and the exact result of the loop. -/
namespace ledger

/-- THE LOOP INVARIANT of `apply_batch`, for a run started on ledger `l0` at index 0. In state
(l, i): the total is that of `l0`; `i` is within the batch; nothing has changed while `i = 0`;
once `i > 0` the first transfer was valid on `l0`; and (for exact results) running the pure model
on the rest of the batch from `l` finishes what the pure model does on the whole batch from `l0`.
Variant: `batch.length - i`. -/
def batchInv (l0 : Ledger) (batch : Slice Transfer) (p : Ledger × Usize) : Prop :=
  LVocab.total p.1 = LVocab.total l0 ∧ p.2.val ≤ batch.val.length ∧
  (p.2.val = 0 → p.1 = l0) ∧ (0 < p.2.val → ¬ LVocab.firstInvalid l0 batch) ∧
  runN (nums l0) batch.val =
    ((runN (nums p.1) (batch.val.drop p.2.val)).1 + p.2.val, (runN (nums p.1) (batch.val.drop p.2.val)).2)

theorem Ledger.apply_batch_loop.spec (l0 : Ledger) (batch : Slice Transfer) :
    Ledger.apply_batch_loop l0 batch 0#usize ⦃ r =>
      LVocab.total r.2 = LVocab.total l0 ∧ r.1.val ≤ batch.val.length ∧
      (LVocab.firstInvalid l0 batch → r.1.val = 0 ∧ r.2 = l0) ∧
      (r.1.val, nums r.2) = runN (nums l0) batch.val ⦄ := by
  unfold Ledger.apply_batch_loop
  apply loop.spec_decr_nat (fun p => batch.val.length - p.2.val) (batchInv l0 batch)
  · rintro ⟨l, i⟩ ⟨h1, h2, h3, h4, h5⟩
    simp only [batchInv] at h1 h2 h3 h4 h5 ⊢
    unfold Ledger.apply_batch_loop.body
    step*
    · -- the transfer was applied: the invariant holds at i + 1, and the variant decreased
      have hi : i.val < batch.val.length := by scalar_tac
      obtain ⟨-, hv, -, -, -, -, ht, hs⟩ | ⟨hb, -⟩ := b_post
      · refine ⟨by omega, by scalar_tac, by omega, fun _ => ?_, ?_, by scalar_tac⟩
        · by_cases hi0 : i.val = 0
          · have := h3 hi0; subst this
            simp_all [LVocab.firstInvalid, List.head?_eq_getElem?]
          · exact h4 (by omega)
        · rw [h5, List.drop_eq_getElem_cons hi, ← t_post, runN_cons_some _ hs, i2_post]
          simp only [Prod.mk.injEq, and_true]; omega
      · simp_all
    · -- the transfer was rejected: stop with the ledger as it was before this transfer
      have hi : i.val < batch.val.length := by scalar_tac
      obtain ⟨hb, -⟩ | ⟨-, -, rfl, hs⟩ := b_post
      · simp_all
      · refine ⟨h1, h2, fun hne hall => ?_, ?_⟩
        · by_cases hi0 : i.val = 0
          · exact ⟨hi0, h3 hi0⟩
          · exact absurd ⟨hne, hall⟩ (h4 (by omega))
        · rw [h5, List.drop_eq_getElem_cons hi, ← t_post, runN_cons_none _ hs]; simp
    · -- the batch is exhausted
      refine ⟨h1, h2, fun hfi => ?_, ?_⟩
      · by_cases hi0 : i.val = 0
        · exact ⟨hi0, h3 hi0⟩
        · exact absurd hfi (h4 (by omega))
      · have hd : batch.val.drop i.val = [] := List.drop_eq_nil_of_le (by scalar_tac)
        rw [h5, hd]; simp [runN]
  · simp [batchInv]

/-- What every scenario about `apply_batch` uses: total conserved; count within the batch;
    a batch whose first transfer is invalid changes nothing; and the exact result, as the pure
    model `runN` on the balances as numbers. -/
@[step]
theorem Ledger.apply_batch.spec (l0 : Ledger) (batch : Slice Transfer) :
    Ledger.apply_batch l0 batch ⦃ r =>
      LVocab.total r.2 = LVocab.total l0 ∧ r.1.val ≤ batch.val.length ∧
      (LVocab.firstInvalid l0 batch → r.1.val = 0 ∧ r.2 = l0) ∧
      (r.1.val, nums r.2) = runN (nums l0) batch.val ⦄ := by
  unfold Ledger.apply_batch
  exact Ledger.apply_batch_loop.spec l0 batch

/-- Progress, derived from the exact result: a batch that stopped early stopped at a transfer that is not
    valid on the ledger it left. (Kept out of `apply_batch.spec` so the scenario proofs that destructure
    that lemma did not have to change.) -/
theorem Ledger.apply_batch.stops {l0 l' : Ledger} {batch : Slice Transfer} {n : Usize}
    (h : (n.val, nums l') = runN (nums l0) batch.val) : LVocab.stopsAtInvalid n batch l' := by
  intro t ht
  have h1 : (runN (nums l0) batch.val).1 = n.val := by rw [← h]
  have h2 : (runN (nums l0) batch.val).2 = nums l' := by rw [← h]
  have hs := runN_stops (nums l0) batch.val t (by rw [h1]; exact ht)
  rw [h2, stepN_nums] at hs
  intro hv
  simp [hv] at hs

end ledger
