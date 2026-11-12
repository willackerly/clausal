/-
Guarantee 1, a labelled object: entitled only if the subject holds something.
Hand-written (plan node T9.7a). FIX ROUND: the sentence is one of the sentences of the link `g1` (tdf/links.yaml); its proof is
the one the run derives from `Link.g1` (TdfLinks/g1.lean) and the theorems of T9.3. What is left here is that its scope is met.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

/-- The scope is met: a request for a labelled object. -/
theorem Rule.tdflite_decision_core.g1_labelled.sat : Rule.tdflite_decision_core.g1_labelled.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _⟩
