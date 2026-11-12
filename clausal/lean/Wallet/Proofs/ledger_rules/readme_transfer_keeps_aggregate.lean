/-
Proof of the scenario statement `Spec.ledger_rules.readme_transfer_keeps_aggregate.stmt` (lean/Wallet/Statements.lean).

Hand-written (by an agent). The theorem must be named exactly `Spec.ledger_rules.readme_transfer_keeps_aggregate`
and its type must be exactly `Spec.ledger_rules.readme_transfer_keeps_aggregate.stmt`: the audit checks both, so a
theorem of some other type is not counted as a proof.

HISTORY (plan node Q4, 2026-11-12). Until the first batch of rewordings this scenario's Then was written "the aggregate
account value of ledger Main is unchanged", a sentence the old whole-phrase glossary did not have, so the scenario had no
flat statement and this file proved its generated obligation (`….obligation`, lean/Wallet/Obligations.lean; proof supplied
by an agent, 2026-11-10). With one live form per piece the Then reads "the total of ledger Main's balances is unchanged",
which IS a glossary phrase (LT-total-same), so the scenario now has a flat statement like every other old sentence and
the proof is of that statement. The argument is the same: the step lemma of `apply`, then its two cases.
-/
import Wallet.Statements
import Ledger.Lemmas.Apply
open Aeneas Aeneas.Std Result

/-- features/ledger_rules.feature:17  a transfer between two accounts of the ledger -/
theorem Spec.ledger_rules.readme_transfer_keeps_aggregate : Spec.ledger_rules.readme_transfer_keeps_aggregate.stmt := by
  intro balances t main _
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  refine ⟨b, l', e, ?_⟩
  rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
  · exact ht
  · rfl
