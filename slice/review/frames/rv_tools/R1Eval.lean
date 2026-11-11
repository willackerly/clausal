/- Reviewer: r1's natural reading ("not every transfer is valid -> none applied") is false of the model:
   ledger [1, 0], batch [0->1:1, 0->0:1]: the second transfer is invalid (same account), the first is valid. -/
import Ledger.Pieces
import Ledger.Vocab
open Aeneas Aeneas.Std Result
#eval (L.applyBatch.run (LVocab.mkLedger [1#u64, 0#u64]) (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 1#u64, ledger.Transfer.mk 0#usize 0#usize 1#u64])).map (fun p => p.1.val)
