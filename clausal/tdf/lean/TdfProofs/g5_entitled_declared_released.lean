/-
Guarantee 5, the "if" half: entitled, and every required obligation declared, gives the release.
Hand-written (plan node T9.7a). FIX ROUND: the sentence is one of the sentences of the link `g5` (tdf/links.yaml); its proof is
the one the run derives from `Link.g5` (TdfLinks/g5.lean) and the theorems of T9.3. What is left here is that its scope is met.
-/
import TdfProofs.Support
open Aeneas Aeneas.Std Result
open tdf_core

/-- The scope is met: at the two-level policy the cleared request's one required obligation is 7, and its client declares 7. -/
theorem Rule.tdflite_decision_core.g5_entitled_declared_released.sat : Rule.tdflite_decision_core.g5_entitled_declared_released.in_scope := by
  refine ⟨Tdf.twoLevelPolicy, Tdf.clearedDeclaring, trivial, ?_⟩
  have key : ∀ x ∈ Tdf.IdSpec.required (T93.absSnapshot Tdf.twoLevelPolicy) (T93.absRequest Tdf.clearedDeclaring), x = 7 := by
    simp only [Tdf.clearedDeclaring, TdfProofs.policy_eq, TdfProofs.request_eq]
    rw [T93.wSnapshot_abs, T93.wRequest_abs]
    simp only [T93.absLevel, T93.nats, List.map]
    decide
  intro x hx
  have hreq : x = 7 := key x hx
  subst hreq
  simp [Abac.declaredBy, Abac.declared, Tdf.clearedDeclaring, Tdf.requestWith, Tdf.vec3]
