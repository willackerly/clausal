/-
THE VOCABULARY, Lean side, of the local book that binds the access-control pack to the extracted TDFLite
decision core (../../../clausebook/local/tdf.yaml, plan node T9.7a). Hand-written and HUMAN-ASSERTED.

  operation   a `Frames.Op` bound to ONE function of the Aeneas-generated model through a fixed constructor of
              lean/Bdd/Ops.lean. Nothing else in this file may mention a model function.
              `release` and `entitlement` are the SAME function, `tdf_core.decide.decide`, read with two notions
              of an accepted answer: the release bit, the entitlement bit.
  reference   `requiredList`: the obligations a request must be able to fulfil, AS THE ID-LEVEL SPECIFICATION
              COMPUTES THEM (`Tdf.IdSpec.required`, read through the plain structural reading of T93/Abs.lean).
              This word is not defined on the values alone: it is the specification's.
  fixtures    one concrete policy and three concrete requests, for scenarios and refutations. They are the
              values the witness theorems of T9.3 are proved at (`T93.wSnapshot`, `T93.wRequest`), restated
              here so that this file does not import the proofs; `Tdf/Fixtures.lean` proves them equal.
-/
import Abac.Pieces
import Bdd.Ops
import IdSpec
import T93.Abs
open Aeneas Aeneas.Std

namespace Tdf
open tdf_core

/-- "key release": state = the policy, input = the request; accepted = the key is released. -/
@[reducible] def release : Frames.Op snapshot.Snapshot request.Request decide.Decision :=
  Bdd.opRead decide.decide Abac.released

/-- "entitlement decision": the same call; accepted = the subject is entitled. -/
@[reducible] def entitlement : Frames.Op snapshot.Snapshot request.Request decide.Decision :=
  Bdd.opRead decide.decide Abac.entitled

/-- "the obligation list": what the decision lists, as identifiers, in order. -/
@[reducible] def obligationList (d : decide.Decision) : List Nat := Abac.listed d

/-- "the required obligation list of the request under the policy": the specification's, in trigger order, with
    repeats. -/
@[reducible] def requiredList (p : snapshot.Snapshot) (r : request.Request) : List Nat :=
  Tdf.IdSpec.required (T93.absSnapshot p) (T93.absRequest r)

/-! ## Fixtures (not vocabulary: concrete values for scenarios, and for printing) -/

/-- A `Vec` of at most three elements. -/
def vec3 {α} (l : List α) (h : l.length ≤ 3) : alloc.vec.Vec α :=
  alloc.vec.Vec.from l (by scalar_tac)

/-- "the two-level policy": one hierarchy attribute (0) with two values (0 above 1); a trigger on value 1 asking
    obligation 7 of everyone; unlabelled objects admitted. -/
def twoLevelPolicy : snapshot.Snapshot :=
  { value_attr := vec3 [0#u32, 0#u32] (by simp)
    rank := vec3 [0#u32, 1#u32] (by simp)
    attr_rule := vec3 [some .Hierarchy] (by simp)
    triggers := vec3 [{ obligation := 7#u32, value := 1#u32, scope := .Everyone }] (by simp)
    deny_unlabelled := false }

/-- A request for an object labelled with value 1, from a subject that holds value 0 and has the given level,
    whose client is not established and declares the given obligations. -/
def requestWith (level : subject.Level) (declared : List Std.U32) (h : declared.length ≤ 3) : request.Request :=
  { bound := .Labels (vec3 [1#u32] (by simp))
    subject := { held := vec3 [0#u32] (by simp), level := vec3 [level] (by simp) }
    client := .NotEstablished
    declared := vec3 declared h }

/-- "the cleared request declaring obligation 7": the subject is at the top level and the client declares 7. -/
def clearedDeclaring : request.Request := requestWith (.At 0#u32) [7#u32] (by simp)

/-- "the cleared request declaring nothing": the subject is at the top level and the client declares nothing. -/
def clearedSilent : request.Request := requestWith (.At 0#u32) [] (by simp)

/-- "the request without a level": the subject holds value 0 and has no level for the attribute. -/
def noLevel : request.Request := requestWith .None [] (by simp)

/-- A request whose bound strings did not resolve (not a scenario value: the input at which the scope of
    "for which the request is unresolved" is shown to be met). -/
def unresolvedRequest : request.Request := { clearedSilent with bound := .Unresolved }

/-- A request for an object that carries no label (the same use). -/
def unlabelledRequest : request.Request := { clearedSilent with bound := .Labels (vec3 [] (by simp)) }

end Tdf
