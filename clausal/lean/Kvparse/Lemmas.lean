import Kvparse.Pieces
open Aeneas Aeneas.Std Result

/-
`kvparse`: what is PROVED of the parser's code (hand-written, by an agent, plan node K1). Two facts and no more:
the parse gives an answer for every parser and every input (no index out of range, no subtraction below zero, the loop
ends), and an input longer than the limit gets the answer `none`. Nothing here relates the loop to the format: that
the accepted inputs are the well-formed ones is NOT proved.
-/
namespace kvparse

/-- One field check at a position within the input gives an answer, and says yes only if three bytes were there. -/
@[step]
theorem field.spec (inp : Slice U8) (i : Usize) (r : Record) (h : i.val ≤ inp.val.length) :
    field inp i r ⦃ out => out.1 = true → i.val + 3 ≤ inp.val.length ⦄ := by
  unfold field
  step*

/-- THE LOOP: from any position within the input it ends with an answer.
    Invariant: the position is within the input. Variant: the bytes left, plus one while another field is expected. -/
theorem record_loop.spec (inp : Slice U8) (n : Usize) (hn : n.val = inp.val.length) (r : Record) (i : Usize)
    (more : Bool) (h : i.val ≤ n.val) :
    record_loop inp n r i more ⦃ _ => True ⦄ := by
  unfold record_loop
  apply loop.spec_decr_nat (fun p : Record × Usize × Bool => (n.val - p.2.1.val) + (if p.2.2 then 1 else 0))
    (fun p => p.2.1.val ≤ n.val)
  · rintro ⟨r, i, more⟩ h
    simp only at h ⊢
    unfold record_loop.body
    step*
    all_goals
      first
      | scalar_tac
      | (simp_all; done)
      | (-- another field follows: the position moved on by four and is still within the input
         simp_all
         have h3 := b_post (by assumption)
         have hne : i1.val ≠ n.val := fun e => ‹¬ i1 = n› (by scalar_tac)
         scalar_tac)
  · simpa using h

/-- A parse gives an answer, and an input longer than the parser's limit gets no record. -/
@[step]
theorem Parser.parse.spec (p : Parser) (inp : Slice U8) :
    Parser.parse p inp ⦃ o => p.limit.val < inp.val.length → o = none ⦄ := by
  unfold Parser.parse record
  by_cases hl : Slice.len inp > p.limit
  · simp [hl]
  · simp only [hl, ↓reduceIte]
    have h := record_loop.spec inp (Slice.len inp) (by simp) { has_a := false, a := 0#u8, has_b := false, b := 0#u8 }
      0#usize true (by simp)
    apply Std.WP.spec_mono h
    intro o _ hlt
    exfalso
    apply hl
    scalar_tac

end kvparse

namespace KV
open kvparse

/-- THE SPECIFICATION'S ENCODER GIVES EACH RECORD ITS OWN BYTES: two records with the same encoding are the same
    record. So where "the encoding of the result is the bytes of the message" holds of an accepted parse, the bytes
    leave one record the answer can be. About the word `KV.encode` only: nothing here mentions the parser's code. -/
theorem encode_inj (r r' : Record) (l : List Nat) (h : encode r = some l) (h' : encode r' = some l) : r = r' := by
  have w : writable r := by
    unfold encode at h
    split at h <;> simp_all
  have w' : writable r' := by
    unfold encode at h'
    split at h' <;> simp_all
  have e : encode r = encode r' := h.trans h'.symm
  unfold encode at e
  simp only [w, w', ite_true, Option.some.injEq] at e
  clear h h'
  obtain ⟨ha, a, hb, b⟩ := r
  obtain ⟨ha', a', hb', b'⟩ := r'
  unfold writable at w w'
  cases ha <;> cases hb <;> cases ha' <;> cases hb' <;> simp at w w' e ⊢ <;> constructor <;> scalar_tac

end KV
