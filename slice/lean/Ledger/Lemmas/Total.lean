import Ledger.Lemmas.Basic
open Aeneas Aeneas.Std Result

/- `Ledger::total`: the summing loop. -/
namespace ledger

/-- THE LOOP INVARIANT of `total`: in state (sum, i), `sum` is the sum of the first `i` balances. -/
def totalInv (l : Ledger) (p : U64 × Usize) : Prop :=
  p.2.val ≤ l.balances.val.length ∧ p.1.val = ((l.balances.val.map (·.val)).take p.2.val).sum

@[step]
theorem Ledger.total.spec (l : Ledger) :
    Ledger.total l ⦃ o =>
      (LVocab.total l ≤ U64.max → ∃ s, o = some s ∧ s.val = LVocab.total l) ∧
      (U64.max < LVocab.total l → o = none) ⦄ := by
  unfold Ledger.total Ledger.total_loop
  apply loop.spec_decr_nat (fun p => l.balances.val.length - p.2.val) (totalInv l)
  · rintro ⟨sum, i⟩ ⟨h1, h2⟩
    simp only [totalInv] at h1 h2 ⊢
    unfold Ledger.total_loop.body
    have hL : (l.balances.val.map (·.val)).length = l.balances.val.length := by simp
    step*
    · -- the checked addition overflowed: the prefix sum, hence the total, exceeds u64
      have hi : i.val < (l.balances.val.map (·.val)).length := by scalar_tac
      have h3 := sum_take_succ _ _ hi
      have h4 := sum_take_le (l.balances.val.map (·.val)) (i.val + 1)
      simp_all [LVocab.total]
      scalar_tac
    · -- one more balance added: the invariant holds at i + 1, and the variant decreased
      have hi : i.val < (l.balances.val.map (·.val)).length := by scalar_tac
      have h3 := sum_take_succ _ _ hi
      simp_all
      scalar_tac
    · -- all balances added
      have h3 : (l.balances.val.map (·.val)).take i.val = l.balances.val.map (·.val) :=
        List.take_of_length_le (by scalar_tac)
      simp_all [LVocab.total]
      scalar_tac
  · simp [totalInv]

end ledger
