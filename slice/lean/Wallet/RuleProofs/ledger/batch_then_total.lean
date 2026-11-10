/-
Hand-written proof of the RULE statement `Rule.ledger.batch_then_total.reading` (lean/Wallet/Readings.lean):

    Rule: A batch followed by a computation of the total is accepted exactly when the total of the
          balances of the ledger is at most the maximum

No glue is generated for this rule: the scenarios beneath it are about a sequence of two operations and
name the sum with an outline parameter. This proof uses the two loop lemmas (the batch conserves the total;
the summing loop reports the total exactly when it fits). The theorem must be named exactly
`Rule.ledger.batch_then_total` and its type must be exactly `Rule.ledger.batch_then_total.reading`.
-/
import Wallet.Readings
import Ledger.Lemmas.Batch
import Ledger.Lemmas.Total
open Aeneas Aeneas.Std Result

theorem Rule.ledger.batch_then_total : Rule.ledger.batch_then_total.reading := by
  intro st inp _
  obtain ⟨⟨n, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec st inp.1)
  obtain ⟨o, e2, h2, h3⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec l1)
  have h1 : LVocab.total l1 = LVocab.total st := h1
  rw [h1] at h2 h3
  refine ⟨o, l1, Frames.Op.andThen_some.mpr ⟨n, l1, Bdd.opMut_some.mpr e1, Bdd.opRead0_some.mpr ⟨e2, rfl⟩⟩, ?_⟩
  constructor
  · intro ha
    by_contra hb
    exact ha (h3 (Nat.lt_of_not_le hb))
  · intro hb
    obtain ⟨s, rfl, -⟩ := h2 hb
    exact Option.some_ne_none s
