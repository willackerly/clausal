import Aeneas
open Aeneas Aeneas.Std Result ControlFlow Error
namespace wallet
inductive Error where
| InsufficientFunds : Error
| Overflow : Error
structure Wallet where
  balance : Std.U64
def transfer
  (src : Wallet) (dst : Wallet) (amt : Std.U64) :
  Result ((core.result.Result Unit Error) × Wallet × Wallet)
  := do
  if src.balance < amt
  then ok (core.result.Result.Err Error.InsufficientFunds, src, dst)
  else
    let o ← lift (U64.checked_add dst.balance amt)
    match o with
    | none => ok (core.result.Result.Err Error.Overflow, src, dst)
    | some b =>
      let i ← src.balance - amt
      ok (core.result.Result.Ok (), { balance := i }, { balance := b })
end wallet

open wallet
deriving instance DecidableEq, Repr for wallet.Error
deriving instance DecidableEq, Repr for wallet.Wallet
deriving instance DecidableEq for core.result.Result
def w (n : U64) : Wallet := ⟨n⟩
abbrev Ret := core.result.Result Unit wallet.Error
-- E1: executable checker through Result.match
inductive Check | pass | thenFalse | panicked | diverged deriving Repr, DecidableEq
def check (r : Result (Ret × Wallet × Wallet)) (T : Ret × Wallet × Wallet → Bool) : Check :=
  match Result.match r with
  | .ok o => if T o then .pass else .thenFalse
  | .div => .diverged
  | .vis _ _ => .panicked
#eval check (transfer (w 100#u64) (w 5#u64) 30#u64) (fun (o, s, d) => decide (o = .Ok () ∧ s.balance.val = 70 ∧ d.balance.val = 35))
#eval check (transfer (w 100#u64) (w 18446744073709551600#u64) 30#u64) (fun (o, s, d) => decide (o = .Ok ()))
#eval check (transfer (w 1#u64) (w 5#u64) 30#u64) (fun (o, s, d) => decide (o = .Err .InsufficientFunds ∧ s = w 1#u64))
-- E2: Holds as exists-form, bridge to spec
def Holds {α} (m : Result α) (Q : α → Prop) : Prop := ∃ r, m = ok r ∧ Q r
theorem holds_of_spec {α} {m : Result α} {Q : α → Prop} (h : Std.WP.spec m Q) : Holds m Q := by
  unfold Holds
  cases m using Result.cases with
  | ret r => exact ⟨r, rfl, by simpa using h⟩
  | vis i k => simp at h
  | div => simp at h
theorem spec_of_holds {α} {m : Result α} {Q : α → Prop} (h : Holds m Q) : Std.WP.spec m Q := by
  obtain ⟨r, rfl, hq⟩ := h; simpa using hq
-- E3: universal theorem, triple form with step*
theorem transfer_ok (src dst : Wallet) (amt : U64)
    (h1 : amt.val ≤ src.balance.val) (h2 : dst.balance.val + amt.val ≤ U64.max) :
    Holds (transfer src dst amt) (fun (o, s', d') => o = core.result.Result.Ok () ∧
      s'.balance.val + amt.val = src.balance.val ∧ d'.balance.val = dst.balance.val + amt.val ∧
      s'.balance.val + d'.balance.val = src.balance.val + dst.balance.val) := by
  apply holds_of_spec
  unfold transfer
  step*
  scalar_tac
#print axioms transfer_ok
theorem transfer_rej (src dst : Wallet) (amt : U64) (h1 : src.balance.val < amt.val) :
    Holds (transfer src dst amt) (fun (o, s', d') => o = core.result.Result.Err .InsufficientFunds ∧ s' = src ∧ d' = dst) := by
  apply holds_of_spec
  unfold transfer
  step*
#print axioms transfer_rej
-- E4: kernel refutation: witness + Holds of the negated postcondition
theorem holds_excl {α} {m : Result α} {Q Q' : α → Prop} (h : Holds m Q) (h' : Holds m Q') : ∃ r, Q r ∧ Q' r := by
  obtain ⟨r, e, q⟩ := h; obtain ⟨r', e', q'⟩ := h'
  rw [e] at e'; simp at e'; subst e'; exact ⟨r, q, q'⟩
theorem witness : Holds (transfer (w 100#u64) (w 18446744073709551600#u64) 30#u64)
    (fun (o, _, _) => ¬ o = core.result.Result.Ok ()) := by
  apply holds_of_spec
  unfold transfer
  step*
  simp [w] at *
  scalar_tac
theorem refute : ¬ (∀ (src dst : Wallet), src.balance.val = 100 →
    Holds (transfer src dst 30#u64) (fun (o, _, _) => o = core.result.Result.Ok ())) := by
  intro h
  obtain ⟨r, a, b⟩ := holds_excl (h (w 100#u64) (w 18446744073709551600#u64) (by decide)) witness
  exact b a
#print axioms refute
