/-
`fill_orders`: a loop over the orders whose body calls `stock_of` (through `can_fill`) and `take`,
both of which loop. Loop lemma, generalised over the state: from (warehouse s, filled, i) the loop
returns filled + (orders from i on that fillFrom fills) and the bins fillFrom leaves.
-/
import Lemmas.Basic
import Lemmas.StockOf
import Lemmas.Take
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

theorem slice_index_ok {α} (v : Slice α) (i : Usize) (h : i.val < v.val.length) :
    Slice.index_usize v i = ok (v.val[i.val]) := by
  simp [Slice.index_usize, h]

theorem can_fill_spec (w : Warehouse) (p : U32) (q : U64) :
    Warehouse.can_fill w p q = ok (decide (q.val ≤ IVocab.stock w p)) := by
  obtain ⟨r, hr, h1, h2⟩ := stock_of_spec w p
  unfold Warehouse.can_fill
  rw [hr]
  cases r with
  | none =>
    have := h2 rfl
    have hq : q.val ≤ U64.max := by scalar_tac
    simp only [bind_ok]
    congr 1; simp; omega
  | some s =>
    simp only [bind_ok]
    congr 1; simp [h1 s rfl]

theorem fillFrom_fst_le : ∀ (bs os : List (Nat × Nat)), (IVocab.fillFrom bs os).1 ≤ os.length
  | bs, [] => by simp [IVocab.fillFrom]
  | bs, (p, u) :: os => by
    have h1 := fillFrom_fst_le (IVocab.takeFrom p u bs) os
    have h2 := fillFrom_fst_le bs os
    unfold IVocab.fillFrom
    split <;> simp <;> omega

theorem orderView_drop_cons (os : Slice Order) (i : Nat) (h : i < os.val.length) :
    (IVocab.orderView os).drop i
      = (os.val[i].product.val, os.val[i].qty.val) :: (IVocab.orderView os).drop (i+1) := by
  rw [drop_cons _ i (by simp [IVocab.orderView, h])]; simp [IVocab.orderView]

theorem fill_orders_loop_spec (os : Slice Order) :
    ∀ (k : Nat) (s : Warehouse) (filled i : Usize), os.val.length - i.val = k →
    i.val ≤ os.val.length → filled.val ≤ i.val →
    ∃ c w', Warehouse.fill_orders_loop s os filled i = ok (c, w') ∧
      c.val = filled.val + (IVocab.fillFrom (IVocab.view s) ((IVocab.orderView os).drop i.val)).1 ∧
      IVocab.view w' = (IVocab.fillFrom (IVocab.view s) ((IVocab.orderView os).drop i.val)).2 := by
  intro k
  induction k with
  | zero =>
    intro s filled i hk hi hf
    have hi' : os.val.length ≤ i.val := by omega
    have hd : (IVocab.orderView os).drop i.val = [] := by simp [IVocab.orderView, hi']
    refine ⟨filled, s, ?_, ?_, ?_⟩
    · unfold Warehouse.fill_orders_loop
      apply loop_done
      simp [Warehouse.fill_orders_loop.body, hi']
    · simp [hd, IVocab.fillFrom]
    · simp [hd, IVocab.fillFrom]
  | succ k ih =>
    intro s filled i hk hi hf
    have hlt : i.val < os.val.length := by omega
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    rw [orderView_drop_cons os i.val hlt]
    by_cases hc : os.val[i.val].qty.val ≤ IVocab.stock s os.val[i.val].product
    · obtain ⟨t, s2, ht, hv2, -⟩ := take_spec s os.val[i.val].product os.val[i.val].qty
      obtain ⟨f1, hf1, hfv1⟩ := usize_succ_ok filled (by scalar_tac)
      have hb : Warehouse.fill_orders_loop.body os s filled i = ok (.cont (s2, f1, i1)) := by
        simp [Warehouse.fill_orders_loop.body, hlt, slice_index_ok _ _ hlt, can_fill_spec, hc, ht,
          hf1, hi1]
      rw [show Warehouse.fill_orders_loop s os filled i = Warehouse.fill_orders_loop s2 os f1 i1
        from loop_cont hb]
      obtain ⟨c, w', hr, hcv, hwv⟩ := ih s2 f1 i1 (by omega) (by omega) (by omega)
      refine ⟨c, w', hr, ?_, ?_⟩
      · rw [hcv, hfv1, hv2, hv1]
        simp only [IVocab.stock] at hc
        simp [IVocab.fillFrom, hc]; omega
      · rw [hwv, hv2, hv1]
        simp only [IVocab.stock] at hc
        simp [IVocab.fillFrom, hc]
    · have hb : Warehouse.fill_orders_loop.body os s filled i = ok (.cont (s, filled, i1)) := by
        simp [Warehouse.fill_orders_loop.body, hlt, slice_index_ok _ _ hlt, can_fill_spec, hc, hi1]
      rw [show Warehouse.fill_orders_loop s os filled i = Warehouse.fill_orders_loop s os filled i1
        from loop_cont hb]
      obtain ⟨c, w', hr, hcv, hwv⟩ := ih s filled i1 (by omega) (by omega) (by omega)
      refine ⟨c, w', hr, ?_, ?_⟩
      · rw [hcv, hv1]
        simp only [IVocab.stock] at hc
        simp [IVocab.fillFrom, hc]
      · rw [hwv, hv1]
        simp only [IVocab.stock] at hc
        simp [IVocab.fillFrom, hc]

theorem fill_orders_spec (w : Warehouse) (os : Slice Order) :
    ∃ c w', Warehouse.fill_orders w os = ok (c, w') ∧
      c.val = (IVocab.fillFrom (IVocab.view w) (IVocab.orderView os)).1 ∧
      IVocab.view w' = (IVocab.fillFrom (IVocab.view w) (IVocab.orderView os)).2 := by
  obtain ⟨c, w', hr, hcv, hwv⟩ := fill_orders_loop_spec os _ w 0#usize 0#usize rfl (by simp) (by simp)
  exact ⟨c, w', hr, by simpa using hcv, by simpa using hwv⟩

end PL
