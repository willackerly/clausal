/-
Proof of the flat proof obligation `Rule.ledger_rules.mono_extended_ledger.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.mono_extended_ledger.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Usize) (st2 : ledger.Ledger) (inp2 : Usize), L.extended st inp st2 inp2 → ∃ (ans : Option U64) (st' : ledger.Ledger) (ans2 : Option U64) (st2' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ (ledger.Ledger.balance st2 inp2 = ok ans2 ∧ st2' = st2) ∧ ((L.found ans) → (L.found ans2)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The theorem must be named exactly `Rule.ledger_rules.mono_extended_ledger` and its type must be exactly
`Rule.ledger_rules.mono_extended_ledger.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.mono_extended_ledger.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:78  Rule: A lookup never loses that there is a result when the ledger is extended -/
theorem Rule.ledger_rules.mono_extended_ledger : Rule.ledger_rules.mono_extended_ledger.obligation := by
  sorry
