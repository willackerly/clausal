/-
Why a narrowing word on a TIED sequence is refused (L2 fix round). Run from `clausal/lean`:

    lake env lean ../clausebook/l2/NarrowedTie.lean

"An accepted deposit followed by a withdrawal with the same input never changes the wallet's balance" would
compile to `Frames.NeverChanges ((((W.deposit).andThen W.withdraw).tied Frames.sameInput).successful) ...`.
`Op.andThen` has `accepted := second.accepted`, so `.successful` narrows on the WITHDRAWAL's answer. At wallet
2^64 - 1, amount 1 the deposit is rejected and the withdrawal accepted: a reader who takes "accepted" as said of
the deposit says the clause does not apply; the Lean statement applies there and is false. Each line below prints
what is said after it.

The ledger case is the other way round: "A rejected transfer followed by a transfer with the same input never
changes the ledger" would narrow on the SECOND transfer being rejected. At ledger [1, 0], transfer 0->1:1 the
first transfer is accepted and the second rejected: a reader who takes "rejected" as said of the first transfer
says the clause does not apply; the Lean statement applies there and is false (the ledger is now [0, 1]).
-/
import Wallet.Readings
import Ledger.Vocab
open Aeneas Aeneas.Std Result

def showAns (r : W.Answer) : String := match r with | .Ok _ => "Ok" | .Err _ => "Err"
def showO (x : Option (W.Answer × wallet.Wallet)) : String :=
  match x with | some (r, w) => s!"some ({showAns r}, balance {w.balance.val})" | none => "none"

def full : wallet.Wallet := ⟨18446744073709551615#u64⟩
@[reducible] def seqOp := ((W.deposit).andThen W.withdraw).tied Frames.sameInput

#eval s!"NTIE deposit alone: {showO ((W.deposit).run full 1#u64)}"                 -- Err, balance 2^64 - 1
#eval s!"NTIE tied sequence: {showO (seqOp.run full 1#u64)}"                        -- Ok, balance 2^64 - 2
#eval s!"NTIE the sequence's answer counts as accepted: {decide (seqOp.successful.accepted (.Ok ()))}"   -- true
#eval s!"NTIE balance unchanged by the sequence: {decide (((seqOp.run full 1#u64).map (fun x => x.2.balance.val)) = some full.balance.val)}"   -- false

def led : ledger.Ledger := LVocab.mkLedger [1#u64, 0#u64]
def tr : ledger.Transfer := ⟨0#usize, 1#usize, 1#u64⟩
@[reducible] def seqL := ((L.apply).andThen L.apply).tied Frames.sameInput
def showL (x : Option (Bool × ledger.Ledger)) : String :=
  match x with | some (r, l) => s!"some ({r}, balances {(L.balances l).map (·.val)})" | none => "none"

#eval s!"NTIE transfer alone: {showL ((L.apply).run led tr)}"                       -- true (accepted), balances [0, 1]
#eval s!"NTIE tied sequence: {showL (seqL.run led tr)}"                             -- false (rejected), balances [0, 1]
#eval s!"NTIE ledger unchanged by the sequence: {decide (((seqL.run led tr).map (fun x => (L.balances x.2).map (·.val))) = some ((L.balances led).map (·.val)))}"   -- false
