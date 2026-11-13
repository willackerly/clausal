/-
Guarantee 3: for a labelled object, entitled exactly when every label is satisfied under its attribute's rule.
Hand-written (plan node T9.7a). FIX ROUND: the sentence is one of the sentences of the link `g3` (tdf/links.yaml); its proof is
the one the run derives from `Link.g3` (TdfLinks/g3.lean) and the theorems of T9.3. What is left here is that its scope is met.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

/-- The scope is met: a request for a labelled object. -/
theorem Rule.tdflite_decision_core.g3_entitled.sat : Rule.tdflite_decision_core.g3_entitled.in_scope :=
  ⟨Tdf.twoLevelPolicy, Tdf.clearedDeclaring, trivial, TdfProofs.labelled_fixture _ _ _⟩
