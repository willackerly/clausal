/-
THE GLOSSARY, Lean side. Hand-written and HUMAN-ASSERTED: each definition is the
intended meaning of one English phrase in ../../glossary.yaml. Nothing checks that
the English and the Lean agree; the definitions are kept to one line each so a
reader can.

Rule (checked by the audit): no definition here may mention a function of the
generated model (wallet.transfer, wallet.Wallet.deposit, ...). Types, constructors
and field projections are fine. Otherwise a Then could restate the code.
-/
import Generated.Wallet
import Bdd.Basic
open Aeneas Aeneas.Std

deriving instance DecidableEq for wallet.WalletError
deriving instance DecidableEq for wallet.Wallet
deriving instance DecidableEq for core.result.Result

namespace Vocab
open wallet

/-- What a wallet operation hands back at the Rust level: `Ok(())` or `Err(e)`. -/
abbrev Outcome := core.result.Result Unit wallet.WalletError

@[reducible] def hasBalance (w : Wallet) (n : U64) : Prop := w.balance = n
@[reducible] def covers (w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val
@[reducible] def exceeds (n : U64) (w : Wallet) : Prop := w.balance.val < n.val
@[reducible] def roomFor (w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max
@[reducible] def noRoomFor (w : Wallet) (n : U64) : Prop := U64.max < w.balance.val + n.val
@[reducible] def succeeds (o : Outcome) : Prop := o = .Ok ()
@[reducible] def rejectedWith (o : Outcome) (e : WalletError) : Prop := o = .Err e
@[reducible] def decreasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val
@[reducible] def increasedBy (pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val
@[reducible] def unchanged (pre post : Wallet) : Prop := post = pre
@[reducible] def totalUnchanged (pre post : List Wallet) : Prop :=
  (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum

/-- Constructor used only to build concrete wallets for row evaluation, search and witnesses. -/
def mkWallet (n : U64) : Wallet := { balance := n }

/-- Printing, for counterexample reports only. -/
def showError : WalletError → String
  | .InsufficientFunds => "Err(InsufficientFunds)"
  | .Overflow => "Err(Overflow)"
def showOutcome : Outcome → String
  | .Ok _ => "Ok(())"
  | .Err e => showError e
def showWallet (w : Wallet) : String := s!"balance {w.balance.val}"

end Vocab
