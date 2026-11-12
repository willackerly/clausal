/-
THE VOCABULARY, Lean side, for the ledger crate: DOMAIN WORDS. Hand-written and HUMAN-ASSERTED: each
definition is the intended meaning of one domain word of ../../clausebook.yaml (kind `domain`).
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

-- relations between two calls: the "more X" / "differs only in X" of the two-run frames (monotone, independent of)
/-- "the amount is smaller": the same ledger, the same sender and receiver; the second call's amount is at most the first's. -/
@[reducible] def smallerAmount : Frames.Variation Ledger Transfer :=
  fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to ∧ a₂.amount.val ≤ a.amount.val
/-- "the amount is larger": the same ledger, the same sender and receiver; the second call's amount is at least the first's. -/
@[reducible] def largerAmount : Frames.Variation Ledger Transfer :=
  fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to ∧ a.amount.val ≤ a₂.amount.val
/-- "only the amount differs": the same ledger, the same sender and receiver; any two amounts. -/
@[reducible] def onlyAmountDiffers : Frames.Variation Ledger Transfer :=
  fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to
/-- "the ledger agrees at the account": the same account number is looked up, and the two ledgers hold the same there
    (both hold the same balance, or neither has such an account). -/
@[reducible] def agreesAtAccount : Frames.Variation Ledger Usize :=
  fun s a s₂ a₂ => a₂ = a ∧ s₂.balances.val[a.val]? = s.balances.val[a.val]?
/-- "the ledger is extended": the same account number is looked up; the second ledger is the first with accounts added at the end. -/
@[reducible] def extended : Frames.Variation Ledger Usize :=
  fun s a s₂ a₂ => a₂ = a ∧ s.balances.val <+: s₂.balances.val

-- reference functions: what a call should answer and leave, written without the code (for "agrees with")
/-- "the reference lookup": the balance at that account number if there is one, otherwise no value; the ledger untouched. -/
@[reducible] def refLookup : Frames.Term Ledger Usize (Option U64 × Ledger) := fun l i => (l.balances.val[i.val]?, l)
/-- "the zero-default lookup": the balance at that account number, and 0 if there is no such account; the ledger untouched. -/
@[reducible] def refLookupZero : Frames.Term Ledger Usize (Option U64 × Ledger) :=
  fun l i => (some (l.balances.val.getD i.val 0#u64), l)

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

-- reference functions that are ANOTHER OPERATION OF THE SAME MODEL (plan node E1; compare/TRADES.md section 5).
-- Unlike `refLookup` these mention the generated model: the rules they make relate two operations of the code.
/-- "the same batch applied transfer by transfer and kept only if every transfer is applied": what `apply_batch` of the
    model does with the batch; accepted with the ledger that leaves if it applies every transfer, otherwise rejected with
    the ledger as it was (also if `apply_batch` gives no answer). -/
@[reducible] def refWholeByBatch : Frames.Term Ledger (Slice Transfer) (Bool × Ledger) := fun l b =>
  match applyBatch.run l b with
  | some (n, l') => if n.val = b.val.length then (true, l') else (false, l)
  | none => (false, l)
/-- `apply` of the model, once per transfer, in order, until one is rejected (or gives no answer):
    (how many were accepted, the ledger those calls left: the one the rejecting call left, if one rejected). -/
def foldApply : Ledger → List Transfer → Nat × Ledger
  | l, [] => (0, l)
  | l, t :: ts =>
    match apply.run l t with
    | some (true, l') => ((foldApply l' ts).1 + 1, (foldApply l' ts).2)
    | some (false, l') => (0, l')
    | none => (0, l)
/-- "its transfers applied one at a time until one is rejected". A count too large for the machine (never the case:
    it is at most the length of the batch) gives 0. -/
@[reducible] def refBatchByTransfers : Frames.Term Ledger (Slice Transfer) (Usize × Ledger) := fun l b =>
  let r := foldApply l b.val
  (if h : r.1 ≤ Usize.max then Usize.ofNatCore r.1 (by scalar_tac) else 0#usize, r.2)


end L
