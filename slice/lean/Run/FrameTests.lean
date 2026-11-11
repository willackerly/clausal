/-
HAND-WRITTEN (not generated). The frames of lean/Frames that no sentence of the fixtures reaches
(vocabulary.yaml, `frames_without_surface`): counting with a number, monotone, agrees with a reference,
independent of. Each is instantiated on concrete operations of the wallet and the ledger, once with a claim
that is true and once with one that is false at some inputs, and at every point of a grid the DEFINITION
(`decide (F.at ...)`) is compared with the independent executable reading (`Frames.Check.F ...`).

Run once per pipeline run with `lake env lean Run/FrameTests.lean`. One line per test:
  FTEST <frame id> <what> <evaluations> <on which the two readings agree> <on which the claim is false>
A disagreement is an error of the run. The "false" count shows the test can tell true from false.
-/
import Wallet.Pieces
import Ledger.Pieces
import Wallet.Vocab
import Ledger.Vocab
open Aeneas Aeneas.Std Result

def amounts : List U64 := [0#u64, 1#u64, 2#u64, 5#u64, 18446744073709551615#u64, 18446744073709551614#u64]
def wallets : List wallet.Wallet := amounts.map Vocab.mkWallet
def ledgers : List ledger.Ledger :=
  [[], [0#u64], [1#u64, 0#u64], [0#u64, 1#u64], [5#u64, 3#u64, 1#u64], [18446744073709551615#u64, 1#u64],
   [1#u64, 0#u64, 0#u64, 1#u64]].map LVocab.mkLedger
def batches : List (Slice ledger.Transfer) :=
  [[], [ledger.Transfer.mk 0#usize 1#usize 1#u64], [ledger.Transfer.mk 1#usize 0#usize 1#u64],
   [ledger.Transfer.mk 0#usize 1#usize 1#u64, ledger.Transfer.mk 1#usize 0#usize 1#u64],
   [ledger.Transfer.mk 0#usize 1#usize 2#u64, ledger.Transfer.mk 0#usize 0#usize 1#u64],
   [ledger.Transfer.mk 0#usize 2#usize 1#u64]].map L.mkBatch
def indexes : List Usize := [0#usize, 1#usize, 2#usize, 3#usize]

def line (frame what : String) (rs : List (Bool × Bool)) : String :=
  s!"FTEST\t{frame}\t{what}\t{rs.length}\t{(rs.filter fun p => p.1 == p.2).length}\t{(rs.filter fun p => !p.1).length}"

-- 11. counting with a number
@[reducible] def coll : Frames.Coll ledger.Ledger (Slice ledger.Transfer) Usize ledger.Transfer := fun _ inp _ => L.transfers inp
@[reducible] def P : Frames.ItemCond ledger.Ledger (Slice ledger.Transfer) ledger.Transfer := fun st _ t => L.valid st t
def countTest (cmp : Frames.Cmp) (n : Nat) : List (Bool × Bool) := Id.run do
  let mut out := []
  for l in ledgers do
    for b in batches do
      out := (decide (Frames.CountOf.at L.applyBatch coll P cmp (fun _ _ => n) l b),
              Frames.Check.countOf L.applyBatch coll P cmp (fun _ _ => n) l b) :: out
  return out

-- 12. monotone: a wallet holding more never loses <class of answer>
@[reducible] def moreMoney : Frames.Variation wallet.Wallet U64 := fun s a s₂ a₂ => a₂ = a ∧ W.balance s ≤ W.balance s₂
def monoTest (op : Frames.Op wallet.Wallet U64 W.Answer) [∀ s a, Decidable (op.scope s a)] [DecidablePred op.accepted] :
    List (Bool × Bool) := Id.run do
  let mut out := []
  for w in wallets do
    for w₂ in wallets do
      for n in amounts do
        out := (decide (Frames.Monotone.at op moreMoney W.accepted w n w₂ n),
                Frames.Check.monotone op moreMoney W.accepted w n w₂ n) :: out
  return out

-- 13. agrees with a reference
@[reducible] def lookupRef : Frames.Term ledger.Ledger Usize (Option U64 × ledger.Ledger) := fun st i => (L.balanceAt st i, st)
@[reducible] def oneRef : Frames.Term ledger.Ledger Unit (Option U64 × ledger.Ledger) := fun st _ => (some 1#u64, st)
def agreeTest : List (Bool × Bool) := Id.run do
  let mut out := []
  for l in ledgers do
    for i in indexes do
      out := (decide (Frames.AgreesWith.at L.lookup lookupRef l i), Frames.Check.agreesWith L.lookup lookupRef l i) :: out
  return out
def agreeTestFalse : List (Bool × Bool) := Id.run do
  let mut out := []
  for l in ledgers do
    out := (decide (Frames.AgreesWith.at L.total oneRef l ()), Frames.Check.agreesWith L.total oneRef l ()) :: out
  return out

-- 14. independent of (two runs)
@[reducible] def sameAccount : Frames.Variation ledger.Ledger Usize := fun s a s₂ a₂ => a₂ = a ∧ L.balanceAt s a = L.balanceAt s₂ a
def indepTest : List (Bool × Bool) := Id.run do
  let mut out := []
  for l in ledgers do
    for l₂ in ledgers do
      for i in indexes do
        out := (decide (Frames.IndependentOf.at L.lookup sameAccount (fun r _ => r) l i l₂ i),
                Frames.Check.independentOf L.lookup sameAccount (fun r _ => r) l i l₂ i) :: out
  return out
/-- "the answer of a transfer is independent of the receiver's balance": false (the receiver can overflow). -/
@[reducible] def sameSender : Frames.Variation (wallet.Wallet × wallet.Wallet) U64 := fun s a s₂ a₂ => a₂ = a ∧ s.1 = s₂.1
def indepTestFalse : List (Bool × Bool) := Id.run do
  let mut out := []
  for a in wallets do
    for b in wallets do
      for b₂ in wallets do
        for n in amounts do
          out := (decide (Frames.IndependentOf.at W.transfer sameSender (fun r _ => r) (a, b) n (a, b₂) n),
                  Frames.Check.independentOf W.transfer sameSender (fun r _ => r) (a, b) n (a, b₂) n) :: out
  return out

#eval show IO Unit from do
  IO.println (line "count_of" "no transfer of the batch is valid on the ledger afterwards (exactly 0)" (countTest .exactly 0))
  IO.println (line "count_of" "at least 1 transfer of the batch is valid on the ledger afterwards" (countTest .atLeast 1))
  IO.println (line "count_of" "at most 1 transfer of the batch is valid on the ledger afterwards" (countTest .atMost 1))
  IO.println (line "monotone" "a wallet holding more never loses acceptance of a withdrawal (true)" (monoTest W.withdraw))
  IO.println (line "monotone" "a wallet holding more never loses acceptance of a deposit (false: it can overflow)" (monoTest W.deposit))
  IO.println (line "monotone" "the same, of successful deposits only (not fail-closed)" (monoTest W.deposit.successful))
  IO.println (line "agrees_with" "a lookup agrees with reading the balance off the ledger (true)" agreeTest)
  IO.println (line "agrees_with" "the total agrees with the constant 1 (false)" agreeTestFalse)
  IO.println (line "same_answer" "a lookup is independent of every other account (true)" indepTest)
  IO.println (line "same_answer" "a transfer's answer is independent of the receiver's balance (false)" indepTestFalse)
