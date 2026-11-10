/-
ADVERSARIAL REVIEW of the ledger (loops) slice. Written by the reviewer, not the builder.
Run once, in a scratch copy of slice/ (never in the real tree):

    cp review/loops/ReviewLoops.lean <copy>/lean/ && cd <copy>/lean && lake env lean ReviewLoops.lean

Sections
  A  every ledger scenario theorem has exactly the type of its statement; axioms printed
  B  what the statements are ABOUT: the non-library constants each statement reaches, with the
     module that declares them (expected: Generated.Ledger, Ledger.Vocab, Wallet.Statements only;
     in particular NOT the hand-written pure model runN/stepN/nums of Ledger.Lemmas.Basic)
  C  satisfiability / non-vacuity witnesses with batches of length 3, 4 and 5 that really iterate
  D  properties the lemma library proves but NO scenario states (what the suite leaves unpinned)
  E  marginal cost probe: one new universal property (a batch never changes the number of accounts)
-/
import Wallet.Statements
import Wallet.Proofs.ledger.balance_no_account
import Wallet.Proofs.ledger.balance_of_account
import Wallet.Proofs.ledger.batch_conserves
import Wallet.Proofs.ledger.batch_count_bounded
import Wallet.Proofs.ledger.batch_example_all
import Wallet.Proofs.ledger.batch_example_stop
import Wallet.Proofs.ledger.batch_first_invalid
import Wallet.Proofs.ledger.batch_then_total
import Wallet.Proofs.ledger.total_is_sum
import Wallet.Proofs.ledger.total_overflow
import Wallet.Proofs.ledger.transfer_invalid_rejected
import Wallet.Proofs.ledger.transfer_valid_moves
import Wallet.Proofs.ledger.two_batches_conserve
import Wallet.Proofs.ledger.whole_conserves
import Wallet.Proofs.ledger.whole_example_accept
import Wallet.Proofs.ledger.whole_example_rollback
import Wallet.Proofs.ledger.whole_first_invalid
import Ledger.Lemmas.All
import Ledger.Lemmas.Total
import Ledger.Lemmas.Balance
open Aeneas Aeneas.Std Result Lean Elab Command Meta

/-! ## A. types and axioms -/
example : Spec.ledger.balance_no_account.stmt := Spec.ledger.balance_no_account
example : Spec.ledger.balance_of_account.stmt := Spec.ledger.balance_of_account
example : Spec.ledger.batch_conserves.stmt := Spec.ledger.batch_conserves
example : Spec.ledger.batch_count_bounded.stmt := Spec.ledger.batch_count_bounded
example : Spec.ledger.batch_example_all.stmt := Spec.ledger.batch_example_all
example : Spec.ledger.batch_example_stop.stmt := Spec.ledger.batch_example_stop
example : Spec.ledger.batch_first_invalid.stmt := Spec.ledger.batch_first_invalid
example : Spec.ledger.batch_then_total.stmt := Spec.ledger.batch_then_total
example : Spec.ledger.total_is_sum.stmt := Spec.ledger.total_is_sum
example : Spec.ledger.total_overflow.stmt := Spec.ledger.total_overflow
example : Spec.ledger.transfer_invalid_rejected.stmt := Spec.ledger.transfer_invalid_rejected
example : Spec.ledger.transfer_valid_moves.stmt := Spec.ledger.transfer_valid_moves
example : Spec.ledger.two_batches_conserve.stmt := Spec.ledger.two_batches_conserve
example : Spec.ledger.whole_conserves.stmt := Spec.ledger.whole_conserves
example : Spec.ledger.whole_example_accept.stmt := Spec.ledger.whole_example_accept
example : Spec.ledger.whole_example_rollback.stmt := Spec.ledger.whole_example_rollback
example : Spec.ledger.whole_first_invalid.stmt := Spec.ledger.whole_first_invalid

def reviewIds : List Name := [
  `Spec.ledger.balance_no_account, `Spec.ledger.balance_of_account, `Spec.ledger.batch_conserves,
  `Spec.ledger.batch_count_bounded, `Spec.ledger.batch_example_all, `Spec.ledger.batch_example_stop,
  `Spec.ledger.batch_first_invalid, `Spec.ledger.batch_then_total, `Spec.ledger.total_is_sum,
  `Spec.ledger.total_overflow, `Spec.ledger.transfer_invalid_rejected, `Spec.ledger.transfer_valid_moves,
  `Spec.ledger.two_batches_conserve, `Spec.ledger.whole_conserves, `Spec.ledger.whole_example_accept,
  `Spec.ledger.whole_example_rollback, `Spec.ledger.whole_first_invalid]

/-- Transitive closure of constants reachable from `root`, entering definitions but not proofs. -/
partial def reviewClosure (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo : Array Name := #[root]
  while !todo.isEmpty do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | some ci =>
      let isThm := match ci with | .thmInfo _ => true | _ => false
      let mut used := ci.type.getUsedConstants
      if !isThm then
        match ci.value? (allowOpaque := true) with
        | some v => used := used ++ v.getUsedConstants
        | none => pure ()
      for m in used do
        if !seen.contains m then todo := todo.push m
    | none => pure ()
  return seen

def reviewModuleOf (env : Environment) (n : Name) : String :=
  match (env.getModuleIdxFor? n).bind (fun i => env.header.moduleNames[i.toNat]?) with
  | some m => m.toString
  | none => "<this file>"

def isLocalModule (m : String) : Bool :=
  m.startsWith "Generated" || m.startsWith "Ledger" || m.startsWith "Wallet" || m.startsWith "Bdd" || m == "<this file>"

run_cmd do
  let env ← getEnv
  for id in reviewIds do
    let ax ← liftCoreM (collectAxioms id)
    logInfo m!"AXIOMS {id}: {ax.toList}"
  -- B: what each STATEMENT reaches (definitions entered, proofs not)
  let mut allMods : Std.HashSet String := {}
  for id in reviewIds do
    let cl := reviewClosure env (id ++ `stmt)
    let mut locals : Array String := #[]
    for n in cl.toArray do
      let m := reviewModuleOf env n
      if isLocalModule m then
        allMods := allMods.insert m
        if m.startsWith "Generated" || m.startsWith "Ledger.Lemmas" then
          locals := locals.push s!"{n} [{m}]"
    logInfo m!"STMT {id}.stmt reaches model/lemma constants: {locals.qsort (· < ·)}"
  logInfo m!"MODULES reached by all ledger statements: {allMods.toList}"
  -- is any axiom declared in our own modules?
  let mut ownAx : Array Name := #[]
  for (n, ci) in env.constants.toList do
    if let .axiomInfo _ := ci then
      if isLocalModule (reviewModuleOf env n) then ownAx := ownAx.push n
  logInfo m!"AXIOMS DECLARED in Generated/Ledger/Wallet/Bdd modules: {ownAx}"

/-! ## C. witnesses with batches of length >= 3 -/
namespace ReviewLoops
open ledger

def T (f t : Usize) (a : U64) : Transfer := ⟨f, t, a⟩

/-- a batch of FOUR transfers, all of which apply in sequence on [100, 20, 0] -/
def b4 : Slice Transfer := LVocab.mkBatch [T 0#usize 1#usize 30#u64, T 1#usize 2#usize 50#u64, T 2#usize 0#usize 10#u64, T 0#usize 2#usize 5#u64]
/-- a batch of FIVE transfers that stops at its FOURTH (index 3): 1->0:1 finds account 1 empty -/
def b5 : Slice Transfer := LVocab.mkBatch [T 0#usize 1#usize 30#u64, T 1#usize 2#usize 50#u64, T 2#usize 0#usize 10#u64, T 1#usize 0#usize 1#u64, T 0#usize 2#usize 5#u64]
/-- a batch of THREE whose first transfer is invalid on [5, 5] -/
def b3bad : Slice Transfer := LVocab.mkBatch [T 0#usize 1#usize 6#u64, T 1#usize 0#usize 1#u64, T 0#usize 1#usize 2#u64]
/-- a batch of THREE, each valid on the STARTING ledger [100, 20, 0] -/
def b3ok : Slice Transfer := LVocab.mkBatch [T 0#usize 1#usize 60#u64, T 1#usize 2#usize 20#u64, T 0#usize 2#usize 60#u64]
def L3 : Ledger := LVocab.mkLedger [100#u64, 20#u64, 0#u64]
def L2 : Ledger := LVocab.mkLedger [5#u64, 5#u64]

theorem b4_len : b4.val.length = 4 := by simp [b4, LVocab.mkBatch_val]
theorem b5_len : b5.val.length = 5 := by simp [b5, LVocab.mkBatch_val]

/-- C1. Givens of batch_first_invalid / whole_first_invalid hold at a batch of length 3. -/
theorem sat_first_invalid_len3 :
    LVocab.holds L2 [5#u64, 5#u64] ∧ LVocab.firstInvalid L2 b3bad ∧ b3bad.val.length = 3 := by
  simp [L2, b3bad, T, LVocab.holds, LVocab.firstInvalid, LVocab.mkLedger_val, LVocab.mkBatch_val,
    LVocab.valid, LVocab.bal]

/-- C2. Givens of batch_all_valid_all_applied hold at a batch of length 3. -/
theorem sat_all_valid_len3 :
    LVocab.holds L3 [100#u64, 20#u64, 0#u64] ∧ LVocab.allValid L3 b3ok ∧ b3ok.val.length = 3 := by
  simp [L3, b3ok, T, LVocab.holds, LVocab.allValid, LVocab.mkLedger_val, LVocab.mkBatch_val,
    LVocab.valid, LVocab.bal, U64.max, U64.numBits]

/-- C3. The universal theorem, instantiated (no extra hypothesis) at the 4-transfer batch: the
    generated loop function returns, and the total is still 120. -/
theorem conserves_at_b4 :
    ∃ (n : Usize) (l' : Ledger), Ledger.apply_batch L3 b4 = ok (n, l') ∧ LVocab.total l' = 120 := by
  obtain ⟨n, l', e, h⟩ := Spec.ledger.batch_conserves [100#u64, 20#u64, 0#u64] b4 L3
    (by simp [L3, LVocab.holds, LVocab.mkLedger_val])
  refine ⟨n, l', e, ?_⟩
  simp [LVocab.totalUnchanged, L3, LVocab.total, LVocab.mkLedger_val] at h
  exact h

/-- C4. All four iterations really run: the generated loop returns exactly 4 and [75, 0, 45]. -/
theorem exact_at_b4 :
    ∃ (n : Usize) (l' : Ledger), Ledger.apply_batch L3 b4 = ok (n, l') ∧ n.val = 4 ∧
      l'.balances.val = [75#u64, 0#u64, 45#u64] := by
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (Ledger.apply_batch.spec L3 b4)
  refine ⟨n, l', e, ?_⟩
  simp [L3, b4, T, nums, LVocab.mkLedger_val, LVocab.mkBatch_val, runN, stepN, U64.max, U64.numBits] at hx
  exact ⟨hx.1, holds_of_nums (by simpa [nums] using hx.2)⟩

/-- C5. A five-transfer batch that stops at its fourth: exactly 3 applied, [80, 0, 40]. -/
theorem exact_at_b5 :
    ∃ (n : Usize) (l' : Ledger), Ledger.apply_batch L3 b5 = ok (n, l') ∧ n.val = 3 ∧
      l'.balances.val = [80#u64, 0#u64, 40#u64] := by
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (Ledger.apply_batch.spec L3 b5)
  refine ⟨n, l', e, ?_⟩
  simp [L3, b5, T, nums, LVocab.mkLedger_val, LVocab.mkBatch_val, runN, stepN, U64.max, U64.numBits] at hx
  exact ⟨hx.1, holds_of_nums (by simpa [nums] using hx.2)⟩

/-- C6. The deliberately false claim is ALSO false at a batch of length 3 (not only the length-2
    counterexample the grid found): b3ok is valid transfer by transfer on [100, 20, 0], yet only 2 apply
    (the third finds 40 left where it needs 60). -/
theorem all_valid_fails_len3 :
    ∃ (n : Usize) (l' : Ledger), Ledger.apply_batch L3 b3ok = ok (n, l') ∧ ¬ LVocab.appliedAll n b3ok := by
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (Ledger.apply_batch.spec L3 b3ok)
  refine ⟨n, l', e, ?_⟩
  simp [L3, b3ok, T, nums, LVocab.mkLedger_val, LVocab.mkBatch_val, runN, stepN, U64.max, U64.numBits] at hx
  simp [LVocab.appliedAll, b3ok, LVocab.mkBatch_val, hx.1]

/-- The same inputs on the executable model (interpreter, not kernel), for comparison with Rust. -/
def showBatch (l : Ledger) (b : Slice Transfer) : String :=
  Bdd.showResult (Ledger.apply_batch l b) (fun r => s!"{r.1.val} applied, balances {r.2.balances.val.map (·.val)}")
#eval showBatch L3 b4
#eval showBatch L3 b5
#eval showBatch L3 b3ok
#eval showBatch L2 b3bad

/-! ## D. proved by the lemma library, stated by NO scenario -/

/-- D1. ATOMICITY of apply_all (the function's whole purpose): a rejected batch changes nothing.
    One line from the hand-written lemma; no universal scenario says it (whole_first_invalid only
    covers a batch whose FIRST transfer is invalid). -/
theorem apply_all_atomic (l : Ledger) (batch : Slice Transfer) :
    ∃ (b : Bool) (l' : Ledger), Ledger.apply_all l batch = ok (b, l') ∧ (b = false → l' = l) := by
  obtain ⟨⟨b, l'⟩, e, -, h, -⟩ := Bdd.ok_of_spec (Ledger.apply_all.spec l batch)
  exact ⟨b, l', e, h⟩

/-! ## E. marginal cost of ONE new universal property -/

theorem stepN_length {bs bs' : List Nat} {t : Transfer} (h : stepN bs t = some bs') :
    bs'.length = bs.length := by
  unfold stepN at h
  split at h
  · cases h; simp
  · cases h

theorem runN_length (ts : List Transfer) : ∀ bs : List Nat, (runN bs ts).2.length = bs.length := by
  induction ts with
  | nil => intro bs; simp [runN]
  | cons t ts ih =>
    intro bs
    cases hs : stepN bs t with
    | none => simp [runN, hs]
    | some bs' => simp [runN, hs, ih bs', stepN_length hs]

/-- E1. "A batch never changes the number of accounts", for all ledgers and batches. -/
theorem batch_keeps_accounts (l : Ledger) (batch : Slice Transfer) :
    ∃ (n : Usize) (l' : Ledger), Ledger.apply_batch l batch = ok (n, l') ∧
      l'.balances.val.length = l.balances.val.length := by
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (Ledger.apply_batch.spec l batch)
  refine ⟨n, l', e, ?_⟩
  have h2 := congrArg Prod.snd hx
  have h3 := runN_length batch.val (nums l)
  simp only at h2
  rw [← h2] at h3
  simpa [nums] using h3

#print axioms conserves_at_b4
#print axioms exact_at_b4
#print axioms exact_at_b5
#print axioms all_valid_fails_len3
#print axioms sat_first_invalid_len3
#print axioms sat_all_valid_len3
#print axioms apply_all_atomic
#print axioms batch_keeps_accounts
end ReviewLoops
