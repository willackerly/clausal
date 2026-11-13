/-
Proof of the flat proof obligation `Rule.kvparse_rules.vi_4.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.kvparse_rules.vi_4.obligation : Prop :=
      (∀ (st : kvparse.Parser) (inp : Slice U8), ∃ (ans : Option kvparse.Record) (st' : kvparse.Parser), (kvparse.Parser.parse st inp = ok ans ∧ st' = st) ∧ ((KV.found ans) → (((KV.length inp) ≤ (KV.limit st)))))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The theorem must be named exactly `Rule.kvparse_rules.vi_4` and its type must be exactly
`Rule.kvparse_rules.vi_4.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.kvparse_rules.vi_4.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
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

/-- features/kvparse_rules.feature:22  Rule: A parse is accepted only if the length of the input is at most the parser's size limit -/
theorem Rule.kvparse_rules.vi_4 : Rule.kvparse_rules.vi_4.obligation := by
  intro st inp
  -- the parse answers, and an input longer than the limit gets no record (lean/Kvparse/Lemmas.lean)
  obtain ⟨ans, e, h⟩ := Bdd.ok_of_spec (kvparse.Parser.parse.spec st inp)
  refine ⟨ans, st, ⟨e, rfl⟩, fun hf => ?_⟩
  by_contra hc
  exact hf (h (by simp only [KV.length, KV.limit] at hc; omega))
