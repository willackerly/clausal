/-
Proof of the flat proof obligation `Rule.ledger_rules.f_no_valid_none_applied.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the vocabulary pieces of this NEW sentence:

    Rule.ledger_rules.f_no_valid_none_applied.obligation : Prop :=
      (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), (Frames.noneOf ((L.transfers inp)) (fun x => (L.valid st x))) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((L.applied ans) = 0))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-11). The theorem must be named exactly `Rule.ledger_rules.f_no_valid_none_applied` and its type must be exactly
`Rule.ledger_rules.f_no_valid_none_applied.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.ledger_rules.f_no_valid_none_applied.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/ledger_rules.feature:149  Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero -/
theorem Rule.ledger_rules.f_no_valid_none_applied : Rule.ledger_rules.f_no_valid_none_applied.obligation := by
  intro st inp hnone
  obtain ⟨⟨n, l'⟩, e, -, hle, hfirst, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec st inp)
  refine ⟨n, l', e, ?_⟩
  by_cases hb : inp.val = []
  · have : inp.val.length = 0 := by rw [hb]; rfl
    have hle' : n.val ≤ inp.val.length := hle
    show n.val = 0
    omega
  · exact (hfirst ⟨hb, fun t ht => hnone t (List.mem_of_mem_head? ht)⟩).1
