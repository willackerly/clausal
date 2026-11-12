/-
Proof of the flat proof obligation `Rule.ledger_rules.l2_each_within_maximum.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.l2_each_within_maximum.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (∀ num_ ∈ ((L.balances st').map L.amount), num_ ≤ L.maximum))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node L2). The theorem must be named exactly `Rule.ledger_rules.l2_each_within_maximum` and its type must be exactly
`Rule.ledger_rules.l2_each_within_maximum.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.l2_each_within_maximum.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:204  Rule: For a transfer, each of the ledger's balances is afterwards at most the maximum -/
theorem Rule.ledger_rules.l2_each_within_maximum : Rule.ledger_rules.l2_each_within_maximum.obligation := by
  intro st inp
  obtain ⟨⟨a, l'⟩, e, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  intro n hn
  obtain ⟨x, -, rfl⟩ := List.mem_map.mp hn
  show x.val ≤ U64.max
  scalar_tac
