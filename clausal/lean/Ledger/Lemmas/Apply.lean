import Ledger.Lemmas.Basic
open Aeneas Aeneas.Std Result

/- `Ledger::apply` (no loop; Vec reads and writes). -/
namespace ledger

@[step]
theorem Ledger.apply.spec (l : Ledger) (t : Transfer) :
    Ledger.apply l t ⦃ r =>
      (r.1 = true ∧ LVocab.valid l t ∧ LVocab.moved l r.2 t ∧ LVocab.total r.2 = LVocab.total l ∧
        stepN (nums l) t = some (nums r.2)) ∨
      (r.1 = false ∧ ¬ LVocab.valid l t ∧ r.2 = l ∧ stepN (nums l) t = none) ⦄ := by
  unfold Ledger.apply
  step*
  · have hinv : ¬ LVocab.valid l t := by simp [LVocab.valid]; scalar_tac
    simp [stepN_nums, hinv]
  · have hinv : ¬ LVocab.valid l t := by simp [LVocab.valid]; scalar_tac
    simp [stepN_nums, hinv]
  · have hinv : ¬ LVocab.valid l t := by simp [LVocab.valid]; scalar_tac
    simp [stepN_nums, hinv]
  · have hf : t.from.val < l.balances.val.length := by scalar_tac
    have hinv : ¬ LVocab.valid l t := by simp [LVocab.valid, LVocab.bal, hf]; scalar_tac
    simp [stepN_nums, hinv]
  · have hf : t.to.val < l.balances.val.length := by scalar_tac
    have hinv : ¬ LVocab.valid l t := by simp_all [LVocab.valid, LVocab.bal]
    simp [stepN_nums, hinv]
  · simp_all; scalar_tac
  · left
    have hf : t.from.val < l.balances.val.length := by scalar_tac
    have ht : t.to.val < l.balances.val.length := by scalar_tac
    have hne : t.from.val ≠ t.to.val := by scalar_tac
    have hm := sum_move (l.balances.val.map (·.val)) t.from.val t.to.val t.amount.val
      (by simpa using hf) (by simpa using ht) hne (by simp_all)
    have hs : stepN (nums l) t = some (nums { balances := index_mut_back1 b }) := by
      have hv : LVocab.valid l t := by simp_all [LVocab.valid, LVocab.bal]
      rw [stepN_nums]; simp only [hv, ite_true]
      clear hv
      simp_all [nums, LVocab.bal, List.map_set]
    simp_all [LVocab.valid, LVocab.bal, LVocab.total, List.map_set]

end ledger
