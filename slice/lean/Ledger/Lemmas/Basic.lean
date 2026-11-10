import Ledger.Vocab
open Aeneas Aeneas.Std Result

/-
Hand-written, kernel-checked, UNTRUSTED support for the ledger proofs: list arithmetic, and a
pure model of the batch computation for exact results. Nothing here appears in a statement.
The lemmas are split by function (Apply, Batch, Total, Balance, All) so that a change to one
Rust function costs only the scenarios about that function their proofs.
-/
namespace ledger

/-- Replacing one entry of a list of numbers changes the sum by the difference. -/
theorem sum_set (L : List Nat) (i x : Nat) (h : i < L.length) :
    (L.set i x).sum + L[i] = L.sum + x := by
  induction L generalizing i with
  | nil => simp at h
  | cons a L ih =>
    cases i with
    | zero => simp; omega
    | succ i => have := ih i (by simpa using h); simp; omega

/-- Moving `a` from entry `f` to a different entry `t` keeps the sum. -/
theorem sum_move (L : List Nat) (f t a : Nat) (hf : f < L.length) (ht : t < L.length) (hne : f ≠ t)
    (ha : a ≤ L[f]) : ((L.set f (L[f] - a)).set t (L[t] + a)).sum = L.sum := by
  have h1 := sum_set L f (L[f] - a) hf
  have h2 := sum_set (L.set f (L[f] - a)) t (L[t] + a) (by simpa using ht)
  simp [List.getElem_set_ne hne] at h2
  omega

/-! ## A pure model, for EXACT results

The invariants below (total conserved, count bounded, ...) do not say what a batch returns on a
given input. Scenarios with literal values, and refutations at a concrete counterexample, need
exactly that, and the model's `loop` cannot be run by `decide`, `rfl` or `simp`. So the same
computation is written once more as plain structural recursion over lists of numbers, and the
loop is proved to compute it. `runN` and `stepN` are not part of any statement. -/

/-- The balances as numbers. -/
def nums (l : Ledger) : List Nat := l.balances.val.map (·.val)

/-- One transfer on the balances as numbers; `none` if it is not valid. -/
def stepN (bs : List Nat) (t : Transfer) : Option (List Nat) :=
  if t.from.val < bs.length ∧ t.to.val < bs.length ∧ t.from.val ≠ t.to.val ∧
      t.amount.val ≤ bs.getD t.from.val 0 ∧ bs.getD t.to.val 0 + t.amount.val ≤ U64.max
  then some ((bs.set t.from.val (bs.getD t.from.val 0 - t.amount.val)).set t.to.val
              (bs.getD t.to.val 0 + t.amount.val))
  else none

/-- A batch on the balances as numbers: (how many were applied, the balances afterwards). -/
def runN : List Nat → List Transfer → Nat × List Nat
  | bs, [] => (0, bs)
  | bs, t :: ts =>
    match stepN bs t with
    | none => (0, bs)
    | some bs' => ((runN bs' ts).1 + 1, (runN bs' ts).2)

/-- Two ledgers with the same numbers hold the same balances. -/
theorem holds_of_nums {l : Ledger} {bs : List U64} (h : nums l = bs.map (·.val)) :
    l.balances.val = bs := by
  have inj : Function.Injective (fun x : U64 => x.val) := by intro a b hab; scalar_tac
  exact List.map_injective_iff.mpr inj h

theorem nums_getD (l : Ledger) (i : Nat) : (nums l).getD i 0 = LVocab.bal l i := by
  simp only [nums, LVocab.bal, List.getD_eq_getElem?_getD, List.getElem?_map]
  cases l.balances.val[i]? <;> simp

/-- The pure step agrees with the glossary's `valid`. -/
theorem stepN_nums (l : Ledger) (t : Transfer) :
    stepN (nums l) t =
      if LVocab.valid l t then
        some (((nums l).set t.from.val (LVocab.bal l t.from.val - t.amount.val)).set t.to.val
                (LVocab.bal l t.to.val + t.amount.val))
      else none := by
  simp only [stepN, LVocab.valid, nums_getD]
  simp [nums]

theorem runN_cons_some {bs bs' : List Nat} {t : Transfer} (ts : List Transfer) (h : stepN bs t = some bs') :
    runN bs (t :: ts) = ((runN bs' ts).1 + 1, (runN bs' ts).2) := by simp [runN, h]

theorem runN_cons_none {bs : List Nat} {t : Transfer} (ts : List Transfer) (h : stepN bs t = none) :
    runN bs (t :: ts) = (0, bs) := by simp [runN, h]

/-- The pure model stops only where it has to: the transfer at the position it stopped at (if there is
    one) cannot be carried out on the balances it ended with. -/
theorem runN_stops (bs : List Nat) (ts : List Transfer) :
    ∀ t ∈ ts[(runN bs ts).1]?, stepN (runN bs ts).2 t = none := by
  induction ts generalizing bs with
  | nil => simp [runN]
  | cons t ts ih =>
    cases h : stepN bs t with
    | none => simp [runN_cons_none _ h, h]
    | some bs' => rw [runN_cons_some _ h]; simpa using ih bs'

theorem sum_take_succ (L : List Nat) (i : Nat) (h : i < L.length) :
    (L.take (i + 1)).sum = (L.take i).sum + L[i] := by
  rw [List.take_succ_eq_append_getElem h, List.sum_append]; simp

theorem sum_take_le (L : List Nat) (i : Nat) : (L.take i).sum ≤ L.sum := by
  have := List.sum_take_add_sum_drop L i; omega

end ledger
