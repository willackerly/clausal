/- The two loop invariants of `dominant_product`. -/
import Vocab.Inventory
import Lemmas.Restock
open Aeneas Aeneas.Std Result ControlFlow

namespace Lemmas
open inventory IVocab

/-- Candidate loop. Invariant: for every product `q`, twice its count in the bins seen so far, plus
    the votes, is at most the number of bins seen, plus twice the votes if `q` is the candidate. -/
theorem dom0_spec (v : alloc.vec.Vec Bin) (n : Usize) (cand : U32) (votes i : Usize)
    (hn : n.val = v.val.length) (hi : i.val ≤ n.val) (hv : votes.val ≤ i.val)
    (hinv : ∀ q : U32, 2 * cnt q (v.val.take i.val) + votes.val
              ≤ i.val + 2 * votes.val * (if cand = q then 1 else 0)) :
    Warehouse.dominant_product_loop0 v n cand votes i ⦃ c =>
      ∀ q : U32, c ≠ q → 2 * cnt q v.val ≤ v.val.length ⦄ := by
  unfold Warehouse.dominant_product_loop0
  apply loop.spec_decr_nat (fun (x : U32 × Usize × Usize) => n.val - x.2.2.val)
    (fun (x : U32 × Usize × Usize) => x.2.2.val ≤ n.val ∧ x.2.1.val ≤ x.2.2.val ∧
      ∀ q : U32, 2 * cnt q (v.val.take x.2.2.val) + x.2.1.val
        ≤ x.2.2.val + 2 * x.2.1.val * (if x.1 = q then 1 else 0))
  · rintro ⟨c, vt, k⟩ ⟨hk, hvk, hI⟩
    simp only at hk hvk hI
    unfold Warehouse.dominant_product_loop0.body
    step*
    · have hlt : k.val < v.val.length := by scalar_tac
      by_cases h0 : vt = 0#usize
      · simp only [h0, ↓reduceIte]
        step*
        refine ⟨by scalar_tac, by scalar_tac, ?_, by scalar_tac⟩
        intro q
        have h := hI q
        have hs := cnt_take_succ q v.val k.val hlt
        have hv0 : vt.val = 0 := by scalar_tac
        rw [hv0] at h
        simp only [Nat.zero_mul, Nat.mul_zero, Nat.add_zero] at h
        have h1 : (1#usize).val = 1 := by scalar_tac
        rw [i1_post, hs, b_post, h1]
        by_cases e1 : v.val[k.val].product = q
        · simp only [if_pos e1]; omega
        · simp only [if_neg e1]; omega
      · simp only [h0, ↓reduceIte]
        by_cases hb : b.product = c
        · simp only [if_pos hb]
          step as ⟨v2, hv2⟩
          step as ⟨k2, hk2⟩
          refine ⟨by scalar_tac, by scalar_tac, ?_, by scalar_tac⟩
          intro q
          have h := hI q
          have hs := cnt_take_succ q v.val k.val hlt
          rw [← b_post, hb] at hs
          rw [hk2, hs, hv2]
          by_cases e : c = q
          · simp only [if_pos e] at h ⊢; omega
          · simp only [if_neg e] at h ⊢; omega
        · simp only [if_neg hb]
          step as ⟨v2, hv2⟩
          step as ⟨k2, hk2⟩
          have hvpos : 0 < vt.val := by scalar_tac
          refine ⟨by scalar_tac, by scalar_tac, ?_, by scalar_tac⟩
          intro q
          have h := hI q
          have hs := cnt_take_succ q v.val k.val hlt
          rw [← b_post] at hs
          rw [hk2, hs, hv2]
          by_cases e : c = q
          · have e1 : ¬ b.product = q := fun h' => hb (h'.trans e.symm)
            simp only [if_pos e, if_neg e1] at h ⊢; omega
          · by_cases e1 : b.product = q
            · simp only [if_neg e, if_pos e1] at h ⊢; omega
            · simp only [if_neg e, if_neg e1] at h ⊢; omega
    · have hkn : k.val = v.val.length := by scalar_tac
      intro q hq
      have h := hI q
      rw [hkn, List.take_length, if_neg hq] at h
      omega
  · exact ⟨hi, hv, hinv⟩

/-- Counting loop: the count so far is the number of bins of the candidate among those seen. -/
theorem dom1_spec (v : alloc.vec.Vec Bin) (n : Usize) (cand : U32) (count j : Usize)
    (hn : n.val = v.val.length) (hj : j.val ≤ n.val)
    (hc : count.val = cnt cand (v.val.take j.val)) :
    Warehouse.dominant_product_loop1 v n cand count j ⦃ r => r.val = cnt cand v.val ⦄ := by
  unfold Warehouse.dominant_product_loop1
  apply loop.spec_decr_nat (fun (x : Usize × Usize) => n.val - x.2.val)
    (fun (x : Usize × Usize) => x.2.val ≤ n.val ∧ x.1.val = cnt cand (v.val.take x.2.val))
  · rintro ⟨c, k⟩ ⟨hk, hck⟩
    simp only at hk hck
    unfold Warehouse.dominant_product_loop1.body
    step*
    · have hlt : k.val < v.val.length := by scalar_tac
      have hs := cnt_take_succ cand v.val k.val hlt
      have hcl := cnt_take_le cand v.val k.val
      rw [← b_post] at hs
      by_cases hb : b.product = cand
      · simp only [if_pos hb] at hs ⊢
        step as ⟨c2, hc2⟩
        step as ⟨k2, hk2⟩
        exact ⟨by scalar_tac, by rw [hk2, hs]; scalar_tac, by scalar_tac⟩
      · simp only [if_neg hb] at hs ⊢
        step as ⟨k2, hk2⟩
        exact ⟨by scalar_tac, by rw [hk2, hs]; scalar_tac, by scalar_tac⟩
    · have hkn : k.val = v.val.length := by scalar_tac
      rw [hkn, List.take_length] at hck
      exact hck
  · exact ⟨hj, hc⟩

theorem dominant_spec (w : Warehouse) :
    Warehouse.dominant_product w ⦃ o =>
      ∃ c : U32, (∀ q : U32, c ≠ q → 2 * cnt q w.bins.val ≤ w.bins.val.length) ∧
        o = if w.bins.val.length - cnt c w.bins.val < cnt c w.bins.val then some c else none ⦄ := by
  unfold Warehouse.dominant_product
  simp only
  have h0 := dom0_spec w.bins (alloc.vec.Vec.len w.bins) 0#u32 0#usize 0#usize (by simp) (by simp)
    (by simp) (by intro q; simp [cnt])
  apply WP.spec_bind h0
  intro c hc
  have h1 := dom1_spec w.bins (alloc.vec.Vec.len w.bins) c 0#usize 0#usize (by simp) (by simp)
    (by simp [cnt])
  apply WP.spec_bind h1
  intro count hcount
  have hle : cnt c w.bins.val ≤ w.bins.val.length := List.length_filter_le _ _
  step as ⟨d, hd⟩
  by_cases hgt : count > d
  · simp only [hgt, ↓reduceIte, WP.spec_ok]
    refine ⟨c, hc, ?_⟩
    rw [if_pos (by scalar_tac)]
  · simp only [hgt, ↓reduceIte, WP.spec_ok]
    refine ⟨c, hc, ?_⟩
    rw [if_neg (by scalar_tac)]

end Lemmas
