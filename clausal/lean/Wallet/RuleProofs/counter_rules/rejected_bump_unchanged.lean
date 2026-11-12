/-
Proof of the flat proof obligation `Rule.counter_rules.rejected_bump_unchanged.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.counter_rules.rejected_bump_unchanged.obligation : Prop :=
      (∀ (st : counter.Counter) (inp : U64), ∀ (ans : Bool) (st' : counter.Counter), (counter.Counter.bump st inp = ok (ans, st')) → (¬ Ctr.said ans → (Ctr.count st') = (Ctr.count st)))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node X7). The theorem must be named exactly `Rule.counter_rules.rejected_bump_unchanged` and its type must be exactly
`Rule.counter_rules.rejected_bump_unchanged.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.counter_rules.rejected_bump_unchanged.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were removed
here: this proof is about the counter and uses none of them. A straight-line function: `unfold` it and `step*`.
-/
import Wallet.Obligations
import Bdd.Basic
open Aeneas Aeneas.Std Result

/-- features/counter_rules.feature:8  Rule: A rejected bump never changes the counter's count -/
theorem Rule.counter_rules.rejected_bump_unchanged : Rule.counter_rules.rejected_bump_unchanged.obligation := by
  intro st inp ans st' e h
  -- whatever a bump returns: if the answer is no, the counter it hands back has the count it was given
  -- (both rejecting branches return `self`; the accepting branch answers yes)
  have key : Std.WP.spec (counter.Counter.bump st inp) (fun r => ¬ Ctr.said r.1 → Ctr.count r.2 = Ctr.count st) := by
    unfold counter.Counter.bump
    step*
  exact Bdd.post_of_spec e key h
