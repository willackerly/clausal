/-
Proof of the flat proof obligation `Rule.ledger_rules.stopped_is_of_batch.obligation` (lean/Wallet/Obligations.lean), which slicegen
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.stopped_is_of_batch.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (∀ x ∈ (L.stoppedAt inp ans), x ∈ (L.transfers inp)))

Hand-written (by a person or an agent). slicegen created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Rule.ledger_rules.stopped_is_of_batch` and its type must be exactly
`Rule.ledger_rules.stopped_is_of_batch.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.stopped_is_of_batch.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

Usual recipe: `intro` the variables and hypotheses, get what the call returns from the hand-proved step lemma
of the model function (`Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)`; lean/Ledger/Lemmas/), then
`refine ⟨_, _, e, ?_⟩` and arithmetic. For a straight-line function: `unfold` it and `step*`.
-/
import Wallet.Obligations
import Ledger.Lemmas.Apply
import Ledger.Lemmas.Batch
import Ledger.Lemmas.Total
import Ledger.Lemmas.Balance
import Ledger.Lemmas.All
open Aeneas Aeneas.Std Result

/-- features/ledger_rules.feature:103  Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch -/
theorem Rule.ledger_rules.stopped_is_of_batch : Rule.ledger_rules.stopped_is_of_batch.obligation := by
  intro st inp
  obtain ⟨⟨n, l'⟩, e, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec st inp)
  refine ⟨n, l', e, ?_⟩
  intro x hm
  exact List.mem_of_getElem? (by simpa using hm)
