/-
What one call of the TOY verifier `sigintake.verify` returns, as a step lemma (hand-written). It is in a module of its
own, listed under `audit_imports` in glossary.yaml, so that the generated refutation scripts can step through a
call of `verify` inside `intake`: without it a false rule about `intake` has a counterexample and no kernel-checked
refutation. Not vocabulary: no statement mentions it. A mutant of `intake` does not break this module; a mutant of
`verify` does, and it is then left out of the scripts (clausal/pipeline.py, `failed_libs`).
-/
import Intake.Pieces
import Bdd.Basic
open Aeneas Aeneas.Std Result

namespace sigintake

@[step]
theorem verify.spec (k : Key) (p c t : U64) :
    verify k p c t ⦃ b => b = true ↔ t.val = (k.id.val % 16) * 256 + (p.val % 16) * 16 + c.val % 16 ⦄ := by
  unfold verify
  step*

end sigintake
