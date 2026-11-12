/-
Proof of the flat proof obligation `Rule.ledger_rules.mono_smaller_amount.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.mono_smaller_amount.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.smallerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((L.said ans) → (L.said ans2)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-10). The theorem must be named exactly `Rule.ledger_rules.mono_smaller_amount` and its type must be exactly
`Rule.ledger_rules.mono_smaller_amount.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.mono_smaller_amount.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:72  Rule: A transfer never loses acceptance when the amount is smaller -/
theorem Rule.ledger_rules.mono_smaller_amount : Rule.ledger_rules.mono_smaller_amount.obligation := by
  rintro st inp st2 inp2 ⟨rfl, hf, ht, ha⟩
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st2 inp)
  obtain ⟨⟨a2, l2'⟩, e2, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st2 inp2)
  refine ⟨a, l', a2, l2', e, e2, ?_⟩
  intro hs
  rcases h with ⟨-, hv, -⟩ | ⟨rfl, -⟩
  · rcases h2 with ⟨r, -⟩ | ⟨-, hnv, -⟩
    · exact r
    · exfalso
      apply hnv
      obtain ⟨h1, h2, h3, h4, h5⟩ := hv
      unfold LVocab.valid
      rw [hf, ht]
      exact ⟨h1, h2, h3, by omega, by omega⟩
  · simp at hs
