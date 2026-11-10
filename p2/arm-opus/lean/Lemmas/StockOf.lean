/-
`stock_of`: the loop adds up the units of one product over the bins from position `i` on.
Invariant (as a generalised loop lemma): from state (sum, i) the loop returns `some s` with
s = sum + (units of p in bins i..), or `none` exactly when that number is past u64::MAX.
-/
import Lemmas.Basic
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

theorem stockIn_cons (p : Nat) (x : Nat × Nat) (l : List (Nat × Nat)) :
    IVocab.stockIn p (x :: l) = (if x.1 = p then x.2 else 0) + IVocab.stockIn p l := by
  unfold IVocab.stockIn; by_cases h : x.1 = p <;> simp [h]

theorem stockIn_nil (p : Nat) : IVocab.stockIn p [] = 0 := rfl

theorem view_length (w : Warehouse) : (IVocab.view w).length = w.bins.val.length := by
  simp [IVocab.view]

theorem view_drop_cons (w : Warehouse) (i : Nat) (h : i < w.bins.val.length) :
    (IVocab.view w).drop i
      = (w.bins.val[i].product.val, w.bins.val[i].qty.val) :: (IVocab.view w).drop (i+1) := by
  rw [drop_cons _ i (by simp [view_length, h])]; simp [IVocab.view]

theorem view_drop_len (w : Warehouse) (i : Nat) (h : w.bins.val.length ≤ i) :
    (IVocab.view w).drop i = [] := by
  simp [IVocab.view, h]

theorem stock_of_loop_spec (w : Warehouse) (p : U32) :
    ∀ (n : Nat) (sum : U64) (i : Usize), w.bins.val.length - i.val = n → i.val ≤ w.bins.val.length →
    ∃ r, Warehouse.stock_of_loop w p sum i = ok r ∧
      (∀ s, r = some s → s.val = sum.val + IVocab.stockIn p.val ((IVocab.view w).drop i.val)) ∧
      (r = none → U64.max < sum.val + IVocab.stockIn p.val ((IVocab.view w).drop i.val)) := by
  intro n
  induction n with
  | zero =>
    intro sum i hn hi
    have hi' : w.bins.val.length ≤ i.val := by omega
    refine ⟨some sum, ?_, ?_, ?_⟩
    · unfold Warehouse.stock_of_loop
      apply loop_done
      simp [Warehouse.stock_of_loop.body, hi']
    · intro s hs; cases hs; simp [view_drop_len w _ hi', stockIn_nil]
    · simp
  | succ n ih =>
    intro sum i hn hi
    have hlt : i.val < w.bins.val.length := by omega
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    rw [view_drop_cons w i.val hlt, stockIn_cons]
    by_cases hp : w.bins.val[i.val].product = p
    · rcases u64_checked_add_cases sum w.bins.val[i.val].qty with ⟨s, hs, hsv⟩ | ⟨hs, hsv⟩
      · have hb : Warehouse.stock_of_loop.body w p sum i = ok (.cont (s, i1)) := by
          simp [Warehouse.stock_of_loop.body, hlt, vec_index_ok _ _ hlt, hp, hi1, lift, hs]
        rw [show Warehouse.stock_of_loop w p sum i = Warehouse.stock_of_loop w p s i1 from loop_cont hb]
        obtain ⟨r, hr, h1, h2⟩ := ih s i1 (by omega) (by omega)
        refine ⟨r, hr, ?_, ?_⟩
        · intro s' hs'; rw [h1 s' hs', hsv, hv1]; simp [hp]; omega
        · intro hn'; have := h2 hn'; rw [hsv, hv1] at this; simp [hp]; omega
      · have hb : Warehouse.stock_of_loop.body w p sum i = ok (.done none) := by
          simp [Warehouse.stock_of_loop.body, hlt, vec_index_ok _ _ hlt, hp, lift, hs]
        refine ⟨none, by unfold Warehouse.stock_of_loop; exact loop_done hb, by simp, ?_⟩
        intro _; simp [hp]; omega
    · have hb : Warehouse.stock_of_loop.body w p sum i = ok (.cont (sum, i1)) := by
        simp [Warehouse.stock_of_loop.body, hlt, vec_index_ok _ _ hlt, hp, hi1]
      rw [show Warehouse.stock_of_loop w p sum i = Warehouse.stock_of_loop w p sum i1 from loop_cont hb]
      obtain ⟨r, hr, h1, h2⟩ := ih sum i1 (by omega) (by omega)
      have hpv : ¬ (w.bins.val[i.val].product.val = p.val) := fun h => hp (UScalar.eq_of_val_eq h)
      refine ⟨r, hr, ?_, ?_⟩
      · intro s' hs'; rw [h1 s' hs', hv1]; simp [hpv]
      · intro hn'; have := h2 hn'; rw [hv1] at this; simpa [hpv] using this

/-- The whole function: `some` of the stock when it fits, `none` when it does not. -/
theorem stock_of_spec (w : Warehouse) (p : U32) :
    ∃ r, Warehouse.stock_of w p = ok r ∧
      (∀ s, r = some s → s.val = IVocab.stock w p) ∧ (r = none → U64.max < IVocab.stock w p) := by
  obtain ⟨r, hr, h1, h2⟩ := stock_of_loop_spec w p _ 0#u64 0#usize rfl (by simp)
  refine ⟨r, hr, ?_, ?_⟩
  · intro s hs; simpa [IVocab.stock] using h1 s hs
  · intro hn; simpa [IVocab.stock] using h2 hn

end PL
