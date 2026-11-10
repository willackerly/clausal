/-
`dominant_product`: two passes. The first pass keeps a candidate and a vote counter (a vote for the
candidate adds one, any other product takes one away, and a candidate with no votes is replaced);
the second pass counts the candidate.

Invariant of the first pass, after bins 0..i-1, with `cnt x i` the number of those bins holding x:
    for every product x:  2 * cnt x i ≤ (i - votes) + (if x = candidate then 2 * votes else 0)
i.e. outside the `votes` unmatched copies of the candidate, the bins seen so far pair off into
pairs of different products, so no product fills more than half of them. At the end (i = n),
a product held by more than half of all bins must therefore be the candidate.
-/
import Lemmas.Basic
import Lemmas.Restock
import Lemmas.Take
import Vocab.Inventory
open Aeneas Aeneas.Std Result inventory

namespace PL

/-- How many of the first `i` bins hold product `x`. -/
def cnt (bs : List Bin) (x : U32) (i : Nat) : Nat := ((bs.take i).filter fun b => b.product = x).length

theorem cnt_le (bs : List Bin) (x : U32) (i : Nat) : cnt bs x i ≤ i :=
  (List.length_filter_le _ _).trans (by simp)

theorem cnt_succ (bs : List Bin) (x : U32) (i : Nat) (h : i < bs.length) :
    cnt bs x (i + 1) = cnt bs x i + (if bs[i].product = x then 1 else 0) :=
  count_take_succ bs x i h

theorem dom_loop0_spec (v : alloc.vec.Vec Bin) (n : Usize) (hn : n.val = v.val.length) :
    ∀ (k : Nat) (cand : U32) (votes i : Usize), n.val - i.val = k → i.val ≤ n.val →
    votes.val ≤ i.val →
    (∀ x : U32, 2 * cnt v.val x i.val ≤ (i.val - votes.val) + (if x = cand then 2 * votes.val else 0)) →
    ∃ c, Warehouse.dominant_product_loop0 v n cand votes i = ok c ∧
      ∀ x : U32, n.val < 2 * cnt v.val x n.val → x = c := by
  intro k
  induction k with
  | zero =>
    intro cand votes i hk hi hvi hinv
    have hi' : n.val ≤ i.val := by omega
    have hin : i.val = n.val := by omega
    refine ⟨cand, ?_, ?_⟩
    · unfold Warehouse.dominant_product_loop0
      apply loop_done
      simp [Warehouse.dominant_product_loop0.body, hi']
    · intro x hx
      by_contra hxc
      have h := hinv x
      simp only [hxc, if_false, hin] at h
      omega
  | succ k ih =>
    intro cand votes i hk hi hvi hinv
    have hlt : i.val < n.val := by omega
    have hlt' : i.val < v.val.length := by omega
    obtain ⟨i1, hi1, hv1⟩ := usize_succ_ok i (by scalar_tac)
    by_cases hvz : votes.val = 0
    · -- no votes: bin i's product becomes the candidate
      have hv0 : votes = 0#usize := UScalar.eq_of_val_eq (by simp [hvz])
      have hb : Warehouse.dominant_product_loop0.body v n cand votes i
          = ok (.cont (v.val[i.val].product, 1#usize, i1)) := by
        simp [Warehouse.dominant_product_loop0.body, hlt, vec_index_ok _ _ hlt', hv0, hi1]
      rw [show Warehouse.dominant_product_loop0 v n cand votes i
        = Warehouse.dominant_product_loop0 v n v.val[i.val].product 1#usize i1 from loop_cont hb]
      refine ih _ _ _ (by omega) (by omega) (by simp; omega) ?_
      intro x
      have h := hinv x
      simp only [hvz, Nat.sub_zero, Nat.mul_zero, ite_self, Nat.add_zero] at h
      rw [hv1, cnt_succ _ _ _ hlt']
      have h1 : (1#usize : Usize).val = 1 := by simp
      rw [h1]
      by_cases hxy : x = v.val[i.val].product
      · subst hxy; simp; omega
      · have : ¬ v.val[i.val].product = x := fun e => hxy e.symm
        simp [hxy, this]; omega
    · have hv0 : ¬ votes = 0#usize := fun e => hvz (by rw [e]; simp)
      by_cases hyc : v.val[i.val].product = cand
      · -- a vote for the candidate
        obtain ⟨w1, hw1, hwv1⟩ := usize_succ_ok votes (by scalar_tac)
        have hb : Warehouse.dominant_product_loop0.body v n cand votes i
            = ok (.cont (cand, w1, i1)) := by
          simp [Warehouse.dominant_product_loop0.body, hlt, vec_index_ok _ _ hlt', hv0, hyc, hw1, hi1]
        rw [show Warehouse.dominant_product_loop0 v n cand votes i
          = Warehouse.dominant_product_loop0 v n cand w1 i1 from loop_cont hb]
        refine ih _ _ _ (by omega) (by omega) (by omega) ?_
        intro x
        have h := hinv x
        rw [hv1, cnt_succ _ _ _ hlt', hwv1]
        by_cases hxc : x = cand
        · subst hxc; simp [hyc] at h ⊢; omega
        · have : ¬ v.val[i.val].product = x := fun e => hxc (e ▸ hyc)
          simp [hxc, this] at h ⊢; omega
      · -- a vote against the candidate
        have hycv : ¬ v.val[i.val].product.val = cand.val := fun e => hyc (UScalar.eq_of_val_eq e)
        obtain ⟨w1, hw1, hwv1⟩ := usub_ok votes 1#usize (by simp; omega)
        have h1 : (1#usize : Usize).val = 1 := by simp
        rw [h1] at hwv1
        have hb : Warehouse.dominant_product_loop0.body v n cand votes i
            = ok (.cont (cand, w1, i1)) := by
          simp [Warehouse.dominant_product_loop0.body, hlt, vec_index_ok _ _ hlt', hv0, hycv, hw1, hi1]
        rw [show Warehouse.dominant_product_loop0 v n cand votes i
          = Warehouse.dominant_product_loop0 v n cand w1 i1 from loop_cont hb]
        refine ih _ _ _ (by omega) (by omega) (by omega) ?_
        intro x
        have h := hinv x
        rw [hv1, cnt_succ _ _ _ hlt', hwv1]
        by_cases hxc : x = cand
        · subst hxc
          simp [hyc] at h ⊢; omega
        · by_cases hxy : v.val[i.val].product = x
          · have hcy : ¬ x = cand := hxc
            simp [hxc, hxy] at h ⊢; omega
          · simp [hxc, hxy] at h ⊢; omega

theorem dom_loop1_spec (v : alloc.vec.Vec Bin) (n : Usize) (hn : n.val = v.val.length) (cand : U32) :
    ∀ (k : Nat) (count j : Usize), n.val - j.val = k → j.val ≤ n.val →
    count.val = cnt v.val cand j.val →
    ∃ r, Warehouse.dominant_product_loop1 v n cand count j = ok r ∧ r.val = cnt v.val cand n.val := by
  intro k
  induction k with
  | zero =>
    intro count j hk hj hc
    have hj' : n.val ≤ j.val := by omega
    refine ⟨count, ?_, by rw [hc, show j.val = n.val by omega]⟩
    unfold Warehouse.dominant_product_loop1
    apply loop_done
    simp [Warehouse.dominant_product_loop1.body, hj']
  | succ k ih =>
    intro count j hk hj hc
    have hlt : j.val < n.val := by omega
    have hlt' : j.val < v.val.length := by omega
    have hcj : count.val ≤ j.val := hc ▸ cnt_le _ _ _
    obtain ⟨j1, hj1, hv1⟩ := usize_succ_ok j (by scalar_tac)
    by_cases hp : v.val[j.val].product = cand
    · obtain ⟨c1, hc1, hcv1⟩ := usize_succ_ok count (by scalar_tac)
      have hb : Warehouse.dominant_product_loop1.body v n cand count j = ok (.cont (c1, j1)) := by
        simp [Warehouse.dominant_product_loop1.body, hlt, vec_index_ok _ _ hlt', hp, hc1, hj1]
      rw [show Warehouse.dominant_product_loop1 v n cand count j
        = Warehouse.dominant_product_loop1 v n cand c1 j1 from loop_cont hb]
      refine ih c1 j1 (by omega) (by omega) ?_
      rw [hcv1, hv1, cnt_succ _ _ _ hlt', hc]; simp [hp]
    · have hpv : ¬ v.val[j.val].product.val = cand.val := fun e => hp (UScalar.eq_of_val_eq e)
      have hb : Warehouse.dominant_product_loop1.body v n cand count j = ok (.cont (count, j1)) := by
        simp [Warehouse.dominant_product_loop1.body, hlt, vec_index_ok _ _ hlt', hpv, hj1]
      rw [show Warehouse.dominant_product_loop1 v n cand count j
        = Warehouse.dominant_product_loop1 v n cand count j1 from loop_cont hb]
      refine ih count j1 (by omega) (by omega) ?_
      rw [hv1, cnt_succ _ _ _ hlt', hc]; simp [hp]

theorem binsOf_eq_cnt (w : Warehouse) (x : U32) :
    IVocab.binsOf w x = cnt w.bins.val x w.bins.val.length := by
  simp [IVocab.binsOf, cnt]

theorem dominant_spec (w : Warehouse) :
    ∃ r, Warehouse.dominant_product w = ok r ∧
      (∀ x : U32, w.bins.val.length < 2 * IVocab.binsOf w x → r = some x) ∧
      (∀ c, r = some c → w.bins.val.length < 2 * IVocab.binsOf w c) := by
  have hn : (alloc.vec.Vec.len w.bins).val = w.bins.val.length := by simp
  obtain ⟨c, hc, hmaj⟩ := dom_loop0_spec w.bins (alloc.vec.Vec.len w.bins) hn _ 0#u32 0#usize 0#usize
    rfl (by simp) (by simp) (by intro x; simp [cnt])
  obtain ⟨m, hm, hmv⟩ := dom_loop1_spec w.bins (alloc.vec.Vec.len w.bins) hn c _ 0#usize 0#usize
    rfl (by simp) (by simp [cnt])
  have hmn : m.val ≤ (alloc.vec.Vec.len w.bins).val := by rw [hmv]; exact cnt_le _ _ _
  obtain ⟨d, hd, hdv⟩ := usub_ok (alloc.vec.Vec.len w.bins) m hmn
  refine ⟨if d.val < m.val then some c else none, ?_, ?_, ?_⟩
  · unfold Warehouse.dominant_product
    dsimp only
    simp only [hc, hm, hd, bind_ok, bind_tc_ok]
    simp [ite_ok]
  · intro x hx
    rw [binsOf_eq_cnt, ← hn] at hx
    have hxc := hmaj x hx
    subst hxc
    have : d.val < m.val := by rw [hdv, hmv]; rw [hn] at hx ⊢; omega
    simp [this]
  · intro c' hc'
    split at hc'
    · rename_i hlt
      cases hc'
      rw [binsOf_eq_cnt]
      rw [hdv, hmv, hn] at hlt
      omega
    · cases hc'

end PL
