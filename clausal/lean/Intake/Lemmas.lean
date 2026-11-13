/-
What one call of `sigintake.intake` returns, proved once (hand-written; used by the proofs of the intake's Rule
obligations in lean/Wallet/RuleProofs/intake/). Not vocabulary: no sentence is read through this file, and a
statement never mentions it. It affects only whether a proof goes through.

`verify_spec`: the toy verifier returns, and answers yes exactly when the tag is the toy tag (`In.verifies`); it is the
step lemma of lean/Intake/Lemmas/Verify.lean under another name.
`intake_spec`: the intake returns; it answers yes exactly when the tag verifies under the key it was GIVEN and the
message's counter is above the last counter; it hands the key back as it was; on yes the last counter is the
message's, on no it is as it was.
-/
import Intake.Lemmas.Verify
open Aeneas Aeneas.Std Result

namespace In

theorem verify_spec (k : sigintake.Key) (p c t : U64) :
    Std.WP.spec (sigintake.verify k p c t)
      (fun b => b = true ↔ t.val = (k.id.val % 16) * 256 + (p.val % 16) * 16 + c.val % 16) :=
  sigintake.verify.spec k p c t

theorem intake_spec (k : sigintake.Key) (c : sigintake.Counter) (m : sigintake.Message) :
    Std.WP.spec (sigintake.intake k c m)
      (fun r => (r.1 = true ↔ (In.verifies k m ∧ c.last.val < m.counter.val)) ∧ r.2.1 = k ∧
                (r.1 = true → r.2.2 = { last := m.counter }) ∧ (r.1 = false → r.2.2 = c)) := by
  unfold sigintake.intake
  have hv := verify_spec k m.payload m.counter m.tag
  obtain ⟨b, eb, hb⟩ := Bdd.ok_of_spec hv
  rw [eb]
  by_cases h : b = true
  · subst h
    have hver : In.verifies k m := hb.mp rfl
    by_cases hle : m.counter <= c.last
    · simp [hle]
      intro _; scalar_tac
    · simp [hle]
      exact ⟨hver, by scalar_tac⟩
  · have hb' : b = false := by simpa using h
    subst hb'
    have hnv : ¬ In.verifies k m := fun hx => by simpa using hb.mpr hx
    simp [hnv]

end In
