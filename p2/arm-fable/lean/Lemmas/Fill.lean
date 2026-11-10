/- Pure facts about the reference `fillFrom`, a specification of `can_fill`, and the loop
   invariant of `fill_orders`. -/
import Vocab.Inventory
import Lemmas.Stock
import Lemmas.Take
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

/-- One order as a pair (product, units). -/
def ow (o : Order) : Nat × Nat := (o.product.val, o.qty.val)

theorem orderView_eq (os : Slice Order) : orderView os = os.val.map ow := rfl

theorem fillFrom_nil (V : List (Nat × Nat)) : fillFrom V [] = (0, V) := by
  cases V <;> rfl

theorem fillFrom_cons (V : List (Nat × Nat)) (q u : Nat) (os : List (Nat × Nat)) :
    fillFrom V ((q, u) :: os) =
      if u ≤ stockIn q V then ((fillFrom (takeFrom q u V) os).1 + 1, (fillFrom (takeFrom q u V) os).2)
      else fillFrom V os := by
  cases V <;> rfl

theorem fillFrom_le (os : List (Nat × Nat)) : ∀ V, (fillFrom V os).1 ≤ os.length := by
  induction os with
  | nil => intro V; simp [fillFrom_nil]
  | cons e t ih =>
    obtain ⟨q, u⟩ := e
    intro V
    rw [fillFrom_cons]
    split
    · have := ih (takeFrom q u V); simp; omega
    · have := ih V; simp; omega

theorem can_fill_spec (w : Warehouse) (p : U32) (q : U64) :
    Warehouse.can_fill w p q ⦃ b => (b = true ↔ q.val ≤ stockIn p.val (w.bins.val.map vw)) ⦄ := by
  unfold Warehouse.can_fill
  apply WP.spec_bind (stock_of_spec w p)
  intro o ho
  have e : stockIn p.val (w.bins.val.map vw) = stk p w.bins.val := stockIn_view p _
  rw [e]
  cases o with
  | none => simp only at ho ⊢; simp; scalar_tac
  | some s => simp only at ho ⊢; simp; scalar_tac

theorem fill_loop_spec (V0 : List (Nat × Nat)) (orders : Slice Order) (w : Warehouse)
    (filled i : Usize) (hi : i.val ≤ orders.val.length) (hf : filled.val ≤ i.val)
    (h1 : (fillFrom (w.bins.val.map vw) ((orders.val.map ow).drop i.val)).1 + filled.val
            = (fillFrom V0 (orders.val.map ow)).1)
    (h2 : (fillFrom (w.bins.val.map vw) ((orders.val.map ow).drop i.val)).2
            = (fillFrom V0 (orders.val.map ow)).2) :
    Warehouse.fill_orders_loop w orders filled i ⦃ r =>
      r.1.val = (fillFrom V0 (orders.val.map ow)).1 ∧
        r.2.bins.val.map vw = (fillFrom V0 (orders.val.map ow)).2 ⦄ := by
  unfold Warehouse.fill_orders_loop
  apply loop.spec_decr_nat (fun (x : Warehouse × Usize × Usize) => orders.val.length - x.2.2.val)
    (fun (x : Warehouse × Usize × Usize) => x.2.2.val ≤ orders.val.length ∧ x.2.1.val ≤ x.2.2.val ∧
      (fillFrom (x.1.bins.val.map vw) ((orders.val.map ow).drop x.2.2.val)).1 + x.2.1.val
          = (fillFrom V0 (orders.val.map ow)).1 ∧
      (fillFrom (x.1.bins.val.map vw) ((orders.val.map ow).drop x.2.2.val)).2
          = (fillFrom V0 (orders.val.map ow)).2)
  · rintro ⟨s, c, j⟩ ⟨hj, hc, hA, hB⟩
    simp only at hj hc hA hB
    unfold Warehouse.fill_orders_loop.body
    step*
    · have hlt : j.val < (orders.val.map ow).length := by
        have : j.val < orders.val.length := by scalar_tac
        simpa using this
      have hO : (orders.val.map ow)[j.val] = (o.product.val, o.qty.val) := by simp [ow, o_post]
      have hd := List.drop_eq_getElem_cons hlt
      rw [hO] at hd
      rw [hd, fillFrom_cons] at hA hB
      step with can_fill_spec as ⟨b, hb⟩
      by_cases hbt : b = true
      · subst hbt
        simp only [↓reduceIte]
        have hle := hb.1 rfl
        rw [if_pos hle] at hA hB
        simp only at hA hB
        step with take_spec as ⟨r, hr1, hr2⟩
        rcases r with ⟨t, s2⟩
        simp only at hr1 ⊢
        step as ⟨c2, hc2⟩
        step as ⟨j2, hj2⟩
        rw [hr1, hj2]
        exact ⟨by scalar_tac, by scalar_tac, by rw [hc2, ← hA]; omega, hB, by scalar_tac⟩
      · have hbf : b = false := by simpa using hbt
        subst hbf
        simp only [Bool.false_eq_true, ↓reduceIte]
        have hle : ¬ o.qty.val ≤ stockIn o.product.val (s.bins.val.map vw) := fun h => hbt (hb.2 h)
        rw [if_neg hle] at hA hB
        step as ⟨j2, hj2⟩
        rw [hj2]
        exact ⟨by scalar_tac, by scalar_tac, hA, hB, by scalar_tac⟩
    · have hjl : j.val = orders.val.length := by scalar_tac
      have hd : List.drop j.val (List.map ow orders.val) = [] := by simp [hjl]
      rw [hd, fillFrom_nil] at hA hB
      simp only at hA hB
      exact ⟨by omega, hB⟩
  · exact ⟨hi, hf, h1, h2⟩

theorem fill_orders_spec (w : Warehouse) (orders : Slice Order) :
    Warehouse.fill_orders w orders ⦃ r =>
      r.1.val = (fillFrom (w.bins.val.map vw) (orders.val.map ow)).1 ∧
        r.2.bins.val.map vw = (fillFrom (w.bins.val.map vw) (orders.val.map ow)).2 ⦄ :=
  fill_loop_spec (w.bins.val.map vw) orders w 0#usize 0#usize (by simp) (by simp) (by simp) (by simp)

end Lemmas
