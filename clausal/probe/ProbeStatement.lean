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

deriving instance DecidableEq for wallet.Error
deriving instance DecidableEq for wallet.Wallet
deriving instance DecidableEq for core.result.Result

namespace Bdd
theorem ok_of_spec {α} {m : Result α} {Q : α → Prop} (h : Std.WP.spec m Q) : ∃ r, m = ok r ∧ Q r := by
  cases m using Result.cases with
  | ret r => exact ⟨r, rfl, by simpa using h⟩
  | vis i k => simp at h
  | div => simp at h
theorem ok3_of_spec {α β γ} {m : Result (α × β × γ)} {Q : α → β → γ → Prop}
    (h : Std.WP.spec m (fun r => Q r.1 r.2.1 r.2.2)) : ∃ a b c, m = ok (a, b, c) ∧ Q a b c := by
  obtain ⟨⟨a, b, c⟩, e, q⟩ := ok_of_spec h; exact ⟨a, b, c, e, q⟩
inductive Check | pass | givenFalse | thenFalse | panicked | diverged deriving Repr, DecidableEq
def run {α} (r : Result α) (T : α → Bool) : Check :=
  match Result.match r with
  | .ok o => if T o then .pass else .thenFalse
  | .div => .diverged
  | .vis _ _ => .panicked
end Bdd

namespace Vocab
open wallet
abbrev Outcome := core.result.Result Unit wallet.Error
@[reducible] def hasBalance (w : Wallet) (n : U64) : Prop := w.balance = n
@[reducible] def covers (w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val
@[reducible] def roomFor (w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max
@[reducible] def succeeds (o : Outcome) : Prop := o = .Ok ()
@[reducible] def rejectedWith (o : Outcome) (e : wallet.Error) : Prop := o = .Err e
@[reducible] def decreasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val
@[reducible] def increasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val
@[reducible] def unchanged (pre post : Wallet) : Prop := post = pre
@[reducible] def totalUnchanged (pre post : List Wallet) : Prop :=
  (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum
def mkWallet (n : U64) : Wallet := { balance := n }
end Vocab

def A.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.covers alice amount →
    Vocab.roomFor bob amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.succeeds outcome ∧
      Vocab.decreasedBy alice alice' amount ∧
      Vocab.increasedBy bob bob' amount ∧
      Vocab.totalUnchanged [alice, bob] [alice', bob']

theorem A : A.stmt := by
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
  simp [Vocab.hasBalance, Vocab.succeeds, Vocab.decreasedBy, Vocab.increasedBy, Vocab.totalUnchanged] at *
  scalar_tac
#print axioms A

def A.check (a b amount : U64) (alice bob : wallet.Wallet) : Bdd.Check :=
  if ¬ (Vocab.hasBalance alice a ∧ Vocab.hasBalance bob b ∧ Vocab.covers alice amount ∧ Vocab.roomFor bob amount)
  then .givenFalse
  else Bdd.run (wallet.transfer alice bob amount) (fun (outcome, alice', bob') =>
    decide (Vocab.succeeds outcome ∧ Vocab.decreasedBy alice alice' amount ∧
      Vocab.increasedBy bob bob' amount ∧ Vocab.totalUnchanged [alice, bob] [alice', bob']))
#eval A.check 100#u64 20#u64 30#u64 (Vocab.mkWallet 100#u64) (Vocab.mkWallet 20#u64)
#eval A.check 5#u64 0#u64 5#u64 (Vocab.mkWallet 5#u64) (Vocab.mkWallet 0#u64)
#eval A.check 5#u64 0#u64 6#u64 (Vocab.mkWallet 5#u64) (Vocab.mkWallet 0#u64)

theorem A.sat : ∃ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a ∧ Vocab.hasBalance bob b ∧ Vocab.covers alice amount ∧ Vocab.roomFor bob amount :=
  ⟨100#u64, 20#u64, 30#u64, Vocab.mkWallet 100#u64, Vocab.mkWallet 20#u64, by simp [Vocab.mkWallet, Vocab.hasBalance, Vocab.covers, Vocab.roomFor]; scalar_tac⟩
#print axioms A.sat

-- the false variant: roomFor dropped
def F.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a → Vocab.hasBalance bob b → Vocab.covers alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧ Vocab.succeeds outcome
theorem F.refuted : ¬ F.stmt := by
  intro h
  obtain ⟨o, a', b', e, t⟩ := h 1#u64 18446744073709551615#u64 1#u64 (Vocab.mkWallet 1#u64) (Vocab.mkWallet 18446744073709551615#u64) (by decide) (by decide) (by decide)
  have w : ∃ o a' b', wallet.transfer (Vocab.mkWallet 1#u64) (Vocab.mkWallet 18446744073709551615#u64) 1#u64 = ok (o, a', b') ∧ ¬ Vocab.succeeds o := by
    apply Bdd.ok3_of_spec
    unfold wallet.transfer
    step*
    simp [Vocab.mkWallet] at *
    scalar_tac
  obtain ⟨o2, a2, b2, e2, t2⟩ := w
  rw [e] at e2; simp at e2
  exact t2 (e2.1 ▸ t)
#print axioms F.refuted
