/-
Proof of the flat proof obligation `Rule.ledger_rules.f_scenario_level.obligation` (lean/Wallet/Obligations.lean), which slicegen
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.f_scenario_level.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∀ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) → (L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

Hand-written (by a person or an agent). slicegen created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-11). The theorem must be named exactly `Rule.ledger_rules.f_scenario_level` and its type must be exactly
`Rule.ledger_rules.f_scenario_level.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.f_scenario_level.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:152  Rule: A successful transfer never changes the total of all balances of the ledger -/
theorem Rule.ledger_rules.f_scenario_level : Rule.ledger_rules.f_scenario_level.obligation := by
  intro st inp ans st' e hs
  have h := Bdd.post_of_spec e (ledger.Ledger.apply.spec st inp)
  rcases h with ⟨-, -, -, ht, -⟩ | ⟨hf, -⟩
  · exact ht
  · have hf' : ans = false := hf
    subst hf'
    simp at hs
