/-
Decidable equality for the wallet model's types. Derived once here because both the vocabulary's domain
words (Wallet/Pieces.lean) and the old whole-phrase glossary (Wallet/Vocab.lean) need it, and deriving
it twice clashes. Not a definition of any word.
-/
import Generated.Wallet
open Aeneas Aeneas.Std

deriving instance DecidableEq for wallet.WalletError
deriving instance DecidableEq for wallet.Wallet
deriving instance DecidableEq for core.result.Result
