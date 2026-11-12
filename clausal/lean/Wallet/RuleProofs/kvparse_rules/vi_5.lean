/-
Proof of the flat proof obligation `Rule.kvparse_rules.vi_5.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.kvparse_rules.vi_5.obligation : Prop :=
      (∀ (st : kvparse.Parser) (inp : Slice U8), ∃ (ans : Option kvparse.Record) (st' : kvparse.Parser), (kvparse.Parser.parse st inp = ok ans ∧ st' = st) ∧ ((KV.count ans) ≤ KV.fieldLimit))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The theorem must be named exactly `Rule.kvparse_rules.vi_5` and its type must be exactly
`Rule.kvparse_rules.vi_5.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.kvparse_rules.vi_5.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The proof below was supplied by an agent (2026-11-12, plan node K1). The stub imported the ledger's lemma modules
(glossary.yaml, `audit_imports`, given to every stub); they were replaced by the parser's own (lean/Kvparse/Lemmas.lean).
The obligation asks that the call ANSWERS (default D1) as well as for the bound, so the proof needs the loop to end:
that is the lemma `kvparse.Parser.parse.spec`.
-/
import Wallet.Obligations
import Kvparse.Lemmas
import Bdd.Basic
open Aeneas Aeneas.Std Result

/-- features/kvparse_rules.feature:26  Rule: For a parse, the number of fields of the result is at most the field limit -/
theorem Rule.kvparse_rules.vi_5 : Rule.kvparse_rules.vi_5.obligation := by
  intro st inp
  -- the parse answers (lean/Kvparse/Lemmas.lean); the bound itself holds of any answer of this type: a record has two keys
  obtain ⟨ans, e, -⟩ := Bdd.ok_of_spec (kvparse.Parser.parse.spec st inp)
  refine ⟨ans, st, ⟨e, rfl⟩, ?_⟩
  cases ans with
  | none => simp [KV.count]
  | some r => simp only [KV.count, KV.fieldLimit]; split_ifs <;> omega
