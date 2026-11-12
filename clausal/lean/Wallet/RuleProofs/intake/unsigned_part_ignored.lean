/-
Proof of the flat proof obligation `Rule.intake.unsigned_part_ignored.obligation` (lean/Wallet/Obligations.lean), which clausal
generated from the Clausebook pieces of this NEW sentence:

    Rule.intake.unsigned_part_ignored.obligation : Prop :=
      (∀ (st : sigintake.Key × sigintake.Counter) (inp : sigintake.Message) (st2 : sigintake.Key × sigintake.Counter) (inp2 : sigintake.Message), In.unsignedDiffers st inp st2 inp2 → ∃ (ans : Bool) (st' : sigintake.Key × sigintake.Counter) (ans2 : Bool) (st2' : sigintake.Key × sigintake.Counter), (sigintake.intake st.1 st.2 inp = ok (ans, st')) ∧ (sigintake.intake st2.1 st2.2 inp2 = ok (ans2, st2')) ∧ (ans = ans2))

Hand-written (by a person or an agent). clausal created this file as a `sorry` stub and never edits it
again. The proof below was supplied by an agent (2026-11-12, plan node W6). The theorem must be named exactly `Rule.intake.unsigned_part_ignored` and its type must be exactly
`Rule.intake.unsigned_part_ignored.obligation`: the audit checks both. The obligation is tied to the compiled reading by a generated,
kernel-checked equivalence (`Rule.intake.unsigned_part_ignored.reading_iff_obligation`, lean/Run/Links.lean), so a proof here
makes the sentence PROVED-FOR-ALL; while it is `sorry` the sentence is TESTED-ONLY.

The stub imported the ledger's lemma modules (glossary.yaml, `audit_imports`, given to every stub); they were replaced
here by the intake's own (lean/Intake/Lemmas.lean: what one call of `sigintake.intake` returns, proved once by
stepping through the model).
-/
import Wallet.Obligations
import Intake.Lemmas
open Aeneas Aeneas.Std Result

/-- features/intake.feature:23  Rule: An intake gives the same answer when only the unsigned part of the message differs -/
theorem Rule.intake.unsigned_part_ignored : Rule.intake.unsigned_part_ignored.obligation := by
  intro st inp st2 inp2 hrel
  obtain ⟨hs, hp, hc, ht⟩ := hrel
  obtain ⟨⟨a, s'⟩, e, h, -⟩ := Bdd.ok_of_spec (In.intake_spec st.1 st.2 inp)
  obtain ⟨⟨a2, s2'⟩, e2, h2, -⟩ := Bdd.ok_of_spec (In.intake_spec st2.1 st2.2 inp2)
  refine ⟨a, s', a2, s2', e, e2, ?_⟩
  subst hs
  -- both answers are decided by the key, the last counter, and the payload, counter and tag of the message: the hint is not read
  have hiff : a = true ↔ a2 = true := by
    have h' : a = true ↔ (In.verifies st2.1 inp ∧ st2.2.last.val < inp.counter.val) := h
    have h2' : a2 = true ↔ (In.verifies st2.1 inp2 ∧ st2.2.last.val < inp2.counter.val) := h2
    rw [h', h2']
    simp only [In.verifies, hp, hc, ht]
  cases a <;> cases a2 <;> simp_all
