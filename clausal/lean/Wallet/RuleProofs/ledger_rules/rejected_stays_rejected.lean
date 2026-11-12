/-
Proof of the flat proof obligation `Rule.ledger_rules.rejected_stays_rejected.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.ledger_rules.rejected_stays_rejected.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.largerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((¬ ((L.said ans))) → ans = ans2))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Rule.ledger_rules.rejected_stays_rejected` and its type must be exactly
`Rule.ledger_rules.rejected_stays_rejected.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.rejected_stays_rejected.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:96  Rule: A transfer gives the same answer when the amount is larger, if it is rejected -/
theorem Rule.ledger_rules.rejected_stays_rejected : Rule.ledger_rules.rejected_stays_rejected.obligation := by
  rintro st inp st2 inp2 ⟨rfl, hf, ht, ha⟩
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st2 inp)
  obtain ⟨⟨a2, l2'⟩, e2, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st2 inp2)
  refine ⟨a, l', a2, l2', e, e2, ?_⟩
  intro hns
  rcases h with ⟨rfl, -⟩ | ⟨rfl, hnv, -⟩
  · exact absurd rfl hns
  · rcases h2 with ⟨-, hv2, -⟩ | ⟨rfl, -⟩
    · exfalso
      apply hnv
      obtain ⟨h1, h2, h3, h4, h5⟩ := hv2
      simp only [hf, ht] at h1 h2 h3 h4 h5
      unfold LVocab.valid
      exact ⟨h1, h2, h3, by omega, by omega⟩
    · rfl
