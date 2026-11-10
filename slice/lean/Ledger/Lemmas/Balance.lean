import Ledger.Vocab
open Aeneas Aeneas.Std Result

/- `Ledger::balance`: bounds-checked lookup. -/
namespace ledger

@[step]
theorem Ledger.balance.spec (l : Ledger) (i : Usize) :
    Ledger.balance l i ⦃ o => o = l.balances.val[i.val]? ⦄ := by
  unfold Ledger.balance
  step*
  · have hi : i.val < l.balances.val.length := by scalar_tac
    simp_all
  · have hi : l.balances.val.length ≤ i.val := by scalar_tac
    simp_all

end ledger
