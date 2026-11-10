/-
THE GLOSSARY, Lean side, for the ledger crate. Hand-written and HUMAN-ASSERTED: each
definition is the intended meaning of one English phrase in ../../glossary.yaml.

Rule (checked by the audit): no definition here may mention a function of the generated
model (ledger.Ledger.apply, ledger.Ledger.apply_batch, ...). Types, constructors and
field projections are fine. `valid`, `bal` and `total` are therefore written out again here, in
terms of plain lists and numbers; they are the specification, not the code.
-/
import Generated.Ledger
import Bdd.Basic
open Aeneas Aeneas.Std

namespace LVocab
open ledger

/-- The sum of all balances, as an unbounded natural number. -/
def total (l : Ledger) : Nat := (l.balances.val.map (·.val)).sum

/-- The balance of account `i` as a number (0 if there is no such account). -/
def bal (l : Ledger) (i : Nat) : Nat := (l.balances.val.getD i 0#u64).val

/-- A transfer the ledger can carry out exactly: both accounts exist and differ, the sender
    covers the amount, and the receiver's balance stays within u64. -/
def valid (l : Ledger) (t : Transfer) : Prop :=
  t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧
  t.amount.val ≤ bal l t.from.val ∧ bal l t.to.val + t.amount.val ≤ U64.max
instance (l : Ledger) (t : Transfer) : Decidable (valid l t) := by unfold valid; infer_instance

-- Givens
@[reducible] def holds (l : Ledger) (bs : List U64) : Prop := l.balances.val = bs
@[reducible] def sumsTo (l : Ledger) (s : U64) : Prop := total l = s.val
@[reducible] def sumTooBig (l : Ledger) : Prop := U64.max < total l
@[reducible] def isAccount (l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length
@[reducible] def notAccount (l : Ledger) (i : Usize) : Prop := l.balances.val.length ≤ i.val
@[reducible] def validOn (l : Ledger) (t : Transfer) : Prop := valid l t
@[reducible] def invalidOn (l : Ledger) (t : Transfer) : Prop := ¬ valid l t
@[reducible] def firstInvalid (l : Ledger) (b : Slice Transfer) : Prop :=
  b.val ≠ [] ∧ ∀ t ∈ b.val.head?, ¬ valid l t
@[reducible] def allValid (l : Ledger) (b : Slice Transfer) : Prop := ∀ t ∈ b.val, valid l t

-- Thens
@[reducible] def totalUnchanged (pre post : Ledger) : Prop := total post = total pre
@[reducible] def unchanged (pre post : Ledger) : Prop := post.balances.val = pre.balances.val
@[reducible] def nowHolds (post : Ledger) (bs : List U64) : Prop := post.balances.val = bs
@[reducible] def appliedAtMost (n : Usize) (b : Slice Transfer) : Prop := n.val ≤ b.val.length
@[reducible] def appliedNone (n : Usize) : Prop := n.val = 0
@[reducible] def appliedAll (n : Usize) (b : Slice Transfer) : Prop := n.val = b.val.length
@[reducible] def appliedExactly (n : Usize) (k : Usize) : Prop := n = k
@[reducible] def resultIs (o : Option U64) (s : U64) : Prop := o = some s
@[reducible] def noResult (o : Option U64) : Prop := o = none
@[reducible] def someResult (o : Option U64) : Prop := o ≠ none
@[reducible] def resultIsBalance (o : Option U64) (l : Ledger) (i : Usize) : Prop :=
  o = l.balances.val[i.val]? ∧ o ≠ none
@[reducible] def accepted (ok : Bool) : Prop := ok = true
@[reducible] def rejected (ok : Bool) : Prop := ok = false
/-- The amount left the sender, arrived at the receiver, and nothing else changed. -/
@[reducible] def moved (pre post : Ledger) (t : Transfer) : Prop :=
  post.balances.val.length = pre.balances.val.length ∧
  bal post t.from.val + t.amount.val = bal pre t.from.val ∧
  bal post t.to.val = bal pre t.to.val + t.amount.val ∧
  ∀ k < pre.balances.val.length, k ≠ t.from.val → k ≠ t.to.val → bal post k = bal pre k

/-- Constructors used only to build concrete values for row evaluation, search and witnesses.
    A list too long for the machine (never the case for a literal) gives the empty value. -/
def mkLedger (bs : List U64) : Ledger :=
  if h : bs.length ≤ Usize.max then { balances := .from bs h } else { balances := .from [] (by simp) }
def mkBatch (ts : List Transfer) : Slice Transfer :=
  if h : ts.length ≤ Usize.max then .from ts h else .from [] (by simp)

/-- NOT definitions: facts about the two constructors above, for the generated proof scripts
    (glossary `proof_hints.simp`). A literal list is always short enough. -/
theorem mkLedger_val (bs : List U64) (h : bs.length ≤ 4294967295) : (mkLedger bs).balances.val = bs := by
  have : bs.length ≤ Usize.max := by scalar_tac
  simp [mkLedger, this]
theorem mkBatch_val (ts : List Transfer) (h : ts.length ≤ 4294967295) : (mkBatch ts).val = ts := by
  have : ts.length ≤ Usize.max := by scalar_tac
  simp [mkBatch, this]

/-- Printing, for counterexample reports only. -/
def showLedger (l : Ledger) : String := s!"balances {l.balances.val.map (·.val)}"
def showCount (n : Usize) : String := s!"{n.val} applied"
def showOpt : Option U64 → String
  | some s => s!"Some({s.val})"
  | none => "None"
def showBool (b : Bool) : String := if b then "true" else "false"

end LVocab
