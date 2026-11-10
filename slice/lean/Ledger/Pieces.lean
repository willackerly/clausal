/-
THE VOCABULARY, Lean side, for the ledger crate: DOMAIN WORDS. Hand-written and HUMAN-ASSERTED: each
definition is the intended meaning of one domain word of ../../vocabulary.yaml (kind `domain`).
Modifiers and frames are not here: they are shared, in lean/Frames.

Rule (as for the old glossary): apart from the operations at the end, nothing here may mention a function
of the generated model. `valid` is therefore written out in terms of plain lists and numbers; it is the
specification, not the code.
-/
import Generated.Ledger
import Bdd.Ops
open Aeneas Aeneas.Std

deriving instance DecidableEq for ledger.Transfer
deriving instance DecidableEq for ledger.Ledger

namespace L
open ledger

-- measures and the collections they are taken over
/-- "the balances": the balances of a ledger, account 0 first. -/
@[reducible] def balances (l : Ledger) : List U64 := l.balances.val
/-- the number an amount of money stands for -/
@[reducible] def amount (x : U64) : Nat := x.val
/-- "the balance of account k": 0 if there is no such account. -/
@[reducible] def bal (l : Ledger) (k : Nat) : Nat := (l.balances.val.getD k 0#u64).val
/-- "the accounts": the account numbers of a ledger. -/
@[reducible] def accounts (l : Ledger) : List Nat := List.range l.balances.val.length
/-- "the balance of account i", as a lookup would report it: absent if there is no such account. -/
@[reducible] def balanceAt (l : Ledger) (i : Usize) : Option U64 := l.balances.val[i.val]?

-- conditions
/-- "is an account of": the account number exists. -/
@[reducible] def isAccount (l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length
/-- "valid on": a transfer the ledger can carry out exactly: both accounts exist and differ, the sender
    covers the amount, and the receiver's balance stays within u64. -/
def valid (l : Ledger) (t : Transfer) : Prop :=
  t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧
  t.amount.val ≤ bal l t.from.val ∧ bal l t.to.val + t.amount.val ≤ U64.max
instance (l : Ledger) (t : Transfer) : Decidable (valid l t) := by unfold valid; infer_instance
/-- "the maximum": the largest total a `total` can report. -/
@[reducible] def maximum : Nat := U64.max

-- parts of the inputs
/-- "the transfers of a batch", in order. -/
@[reducible] def transfers (b : Slice Transfer) : List Transfer := b.val
/-- "the length of a batch". -/
@[reducible] def length (b : Slice Transfer) : Nat := b.val.length
/-- "the sender / the receiver / the amount of a transfer". -/
@[reducible] def sender (t : Transfer) : Nat := t.from.val
@[reducible] def receiver (t : Transfer) : Nat := t.to.val
@[reducible] def amountOf (t : Transfer) : Nat := t.amount.val
/-- "the parties of a transfer": the account numbers it names. -/
@[reducible] def parties (t : Transfer) : List Usize := [t.from, t.to]

/-- How a batch written out in a sentence (`[0->1:30, 1->2:50]`) becomes a value. A list too long for the
    machine (never the case for a literal) gives the empty batch. -/
def mkBatch (ts : List Transfer) : Slice Transfer :=
  if h : ts.length ≤ Usize.max then .from ts h else .from [] (by simp)

/-- NOT a definition: what `mkBatch` builds, for generated proof scripts. A literal list is always short enough. -/
theorem mkBatch_val (ts : List Transfer) (h : ts.length ≤ 4294967295) : (mkBatch ts).val = ts := by
  have : ts.length ≤ Usize.max := by scalar_tac
  simp [mkBatch, this]

-- answers
/-- "the number of transfers applied": what `apply_batch` returns. -/
@[reducible] def applied (n : Usize) : Nat := n.val
/-- "the transfer a batch stopped at": the transfer at the position the count points to, if there is one. -/
@[reducible] def stoppedAt (b : Slice Transfer) (n : Usize) : List Transfer := (b.val[n.val]?).toList
/-- "accepted" for an operation that answers yes or no. -/
@[reducible] def said (ok : Bool) : Prop := ok = true
/-- "there is a result" for a lookup: it reports a value. -/
@[reducible] def found (o : Option U64) : Prop := o ≠ none
/-- an operation that reports a count never rejects: every answer counts as accepted -/
@[reducible] def counted (_ : Usize) : Prop := True

-- operations (the only definitions that mention the generated model)
/-- "a batch is applied": state = the ledger, input = the batch, answer = how many were applied. -/
@[reducible] def applyBatch : Frames.Op Ledger (Slice Transfer) Usize := Bdd.opMut ledger.Ledger.apply_batch counted
/-- "a batch is applied as a whole": answer = whether it was accepted. -/
@[reducible] def applyAll : Frames.Op Ledger (Slice Transfer) Bool := Bdd.opMut ledger.Ledger.apply_all said
/-- "a transfer is applied": answer = whether it was accepted. -/
@[reducible] def apply : Frames.Op Ledger Transfer Bool := Bdd.opMut ledger.Ledger.apply said
/-- "the total is computed": reads the ledger; no input. -/
@[reducible] def total : Frames.Op Ledger Unit (Option U64) := Bdd.opRead0 ledger.Ledger.total found
/-- "a balance is looked up": reads the ledger; input = the account number. -/
@[reducible] def lookup : Frames.Op Ledger Usize (Option U64) := Bdd.opRead ledger.Ledger.balance found

end L
