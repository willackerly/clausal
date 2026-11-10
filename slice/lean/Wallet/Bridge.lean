/-
Facts used only by GENERATED GLUE PROOFS about the wallet (see lean/Bdd/Bridge.lean). Not definitions.
-/
import Generated.Wallet
import Bdd.Bridge
open Aeneas Aeneas.Std

namespace Bdd.Bridge

/-- A wallet is its balance: two wallets are equal exactly when their balances are the same number. -/
theorem wallet_eq {a b : wallet.Wallet} : a.balance.val = b.balance.val ↔ a = b := by
  constructor
  · intro h; cases a; cases b; simp_all [u64_val_eq]
  · intro h; rw [h]

theorem wallet_eq' {a b : wallet.Wallet} : a.balance = b.balance ↔ a = b := by
  constructor
  · intro h; cases a; cases b; simp_all
  · intro h; rw [h]

end Bdd.Bridge
