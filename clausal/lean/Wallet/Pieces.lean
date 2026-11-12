/-
THE VOCABULARY, Lean side, for the wallet crate: DOMAIN WORDS. Hand-written and HUMAN-ASSERTED: each
definition is the intended meaning of one domain word of the wallet's local book
(../../clausebook/local/wallet.yaml, kind `domain`).
Modifiers and frames are not here: they are shared, in lean/Frames.

Three sorts of domain word:
  measures      a quantity of a wallet                       (`balance`)
  answer words  which returned values count as accepted      (`accepted`), named values (`maximum`)
  operations    a `Frames.Op` bound to ONE function of the Aeneas-generated model through a fixed
                constructor of lean/Bdd/Ops.lean. Nothing else in this file may mention a model function.
-/
import Generated.Wallet
import Wallet.Instances
import Bdd.Ops
open Aeneas Aeneas.Std

namespace W
open wallet

/-- What a wallet operation hands back at the Rust level: `Ok(())` or `Err(e)`. -/
abbrev Answer := core.result.Result Unit wallet.WalletError

/-- "balance": the balance of one wallet, as a number. -/
@[reducible] def balance (w : Wallet) : Nat := w.balance.val

/-- "the maximum": the largest balance a wallet can hold. -/
@[reducible] def maximum : Nat := U64.max

/-- "succeeds" / "is accepted": the operation answered `Ok(())`. Every other answer is a rejection. -/
@[reducible] def accepted (r : Answer) : Prop := r = .Ok ()

/-- "is rejected with e": the operation answered `Err(e)`. -/
@[reducible] def rejectedWith (e : WalletError) (r : Answer) : Prop := r = .Err e

/-- "transfer": state = (sender, receiver), input = the amount. -/
@[reducible] def transfer : Frames.Op (Wallet × Wallet) U64 Answer := Bdd.opMut2 wallet.transfer accepted

/-- "deposit": state = the wallet, input = the amount. -/
@[reducible] def deposit : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.deposit accepted

/-- "withdrawal": state = the wallet, input = the amount. -/
@[reducible] def withdraw : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.withdraw accepted

end W
