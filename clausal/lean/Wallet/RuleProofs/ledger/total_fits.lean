/-
Hand-written proof of the RULE statement `Rule.ledger.total_fits.reading` (lean/Wallet/Readings.lean):

    Rule: A computation of the total is accepted exactly when the total of the balances of the ledger
          is at most the maximum

The generated glue (`Rule.ledger.total_fits.from_scenarios`, lean/Run/Links.lean) does not go through:
the scenarios beneath the rule name the sum with an outline parameter of type u64, and the fixed script
cannot produce that u64 from a number. This proof goes to the loop lemma instead. The theorem must be
named exactly `Rule.ledger.total_fits` and its type must be exactly `Rule.ledger.total_fits.reading`
(the audit checks both).
-/
import Wallet.Readings
import Ledger.Lemmas.Total
open Aeneas Aeneas.Std Result

theorem Rule.ledger.total_fits : Rule.ledger.total_fits.reading := by
  intro st inp _
  obtain ⟨o, e, h1, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec st)
  refine ⟨o, st, Bdd.opRead0_some.mpr ⟨e, rfl⟩, ?_⟩
  constructor
  · intro ha
    by_contra hb
    exact ha (h2 (Nat.lt_of_not_le hb))
  · intro hb
    obtain ⟨s, rfl, -⟩ := h1 hb
    exact Option.some_ne_none s
