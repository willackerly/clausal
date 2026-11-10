/- Pure facts about per-product sums over bins, and the loop invariant of `stock_of`. -/
import Vocab.Inventory
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

/-- Units of product `p` in a list of bins. -/
def stk (p : U32) (l : List Bin) : Nat := ((l.filter fun b => b.product = p).map (·.qty.val)).sum

theorem u32_val_eq (a b : U32) : a.val = b.val ↔ a = b := by
  constructor
  · intro h; scalar_tac
  · intro h; rw [h]

theorem stockIn_view (p : U32) (l : List Bin) :
    stockIn p.val (l.map fun b => (b.product.val, b.qty.val)) = stk p l := by
  unfold stockIn stk
  induction l with
  | nil => simp
  | cons b t ih =>
    by_cases h : b.product = p
    · simp_all
    · have : ¬ b.product.val = p.val := fun e => h ((u32_val_eq _ _).1 e)
      simp_all

theorem stock_eq (w : Warehouse) (p : U32) : stock w p = stk p w.bins.val := by
  unfold stock view; exact stockIn_view p _

theorem stk_append (p : U32) (a b : List Bin) : stk p (a ++ b) = stk p a + stk p b := by
  simp [stk]

theorem stk_take_succ (p : U32) (l : List Bin) (i : Nat) (h : i < l.length) :
    stk p (l.take (i+1)) = stk p (l.take i) + (if l[i].product = p then l[i].qty.val else 0) := by
  rw [List.take_succ_eq_append_getElem h, stk_append]
  by_cases e : l[i].product = p <;> simp [stk, e]

theorem stk_take_le (p : U32) (l : List Bin) (i : Nat) : stk p (l.take i) ≤ stk p l := by
  conv => rhs; rw [← List.take_append_drop i l, stk_append]
  omega

theorem stock_of_loop_spec (w : Warehouse) (p : U32) (sum : U64) (i : Usize)
    (hi : i.val ≤ w.bins.val.length) (hs : sum.val = stk p (w.bins.val.take i.val)) :
    Warehouse.stock_of_loop w p sum i ⦃ o =>
      match o with
      | some s => s.val = stk p w.bins.val
      | none => U64.max < stk p w.bins.val ⦄ := by
  unfold Warehouse.stock_of_loop
  apply loop.spec_decr_nat (fun (x : U64 × Usize) => w.bins.val.length - x.2.val)
    (fun (x : U64 × Usize) => x.2.val ≤ w.bins.val.length ∧ x.1.val = stk p (w.bins.val.take x.2.val))
  · rintro ⟨s, j⟩ ⟨hj, hsj⟩
    simp only at hj hsj
    unfold Warehouse.stock_of_loop.body
    step*
    · have hlt : j.val < w.bins.val.length := by scalar_tac
      have h1 := stk_take_succ p _ j.val hlt
      have h2 := stk_take_le p w.bins.val (j.val+1)
      simp_all; omega
    · have hlt : j.val < w.bins.val.length := by scalar_tac
      have h1 := stk_take_succ p _ j.val hlt
      simp_all; omega
    · have hlt : j.val < w.bins.val.length := by scalar_tac
      have h1 := stk_take_succ p _ j.val hlt
      simp_all; omega
    · have hlt : j.val = w.bins.val.length := by scalar_tac
      simp_all
  · exact ⟨hi, hs⟩

theorem stock_of_spec (w : Warehouse) (p : U32) :
    Warehouse.stock_of w p ⦃ o =>
      match o with
      | some s => s.val = stk p w.bins.val
      | none => U64.max < stk p w.bins.val ⦄ :=
  stock_of_loop_spec w p 0#u64 0#usize (by simp) (by simp [stk])

end Lemmas
