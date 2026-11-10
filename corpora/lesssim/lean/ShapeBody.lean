
/-
Constant-threading experiment: which of the corpus's `∃ C` theorems have the shape the relation covers.
Generated header above imports every module holding a census producer.  For each producer the conclusion
is opened (`∃`, `∧`, `∀`/`→`) and every atom that mentions a real `∃`-bound variable is classified.
-/
open Lean Meta Elab Command

namespace Lesssim.Shape

def occ (x : FVarId) (e : Expr) : Nat :=
  match e with
  | .fvar y => if x == y then 1 else 0
  | .app f a => occ x f + occ x a
  | .lam _ d b _ => occ x d + occ x b
  | .forallE _ d b _ => occ x d + occ x b
  | .letE _ t v b _ => occ x t + occ x v + occ x b
  | .proj _ _ b => occ x b
  | .mdata _ b => occ x b
  | _ => 0

partial def factors (e : Expr) : Array Expr :=
  let e := e.consumeMData
  if e.isAppOfArity ``HMul.hMul 6 then factors (e.getArg! 4) ++ factors (e.getArg! 5) else #[e]

structure Acc where
  realEx : Nat := 0
  natEx : Nat := 0
  otherEx : Nat := 0
  signed : Nat := 0
  atoms : Array String := #[]
  hypMentions : Nat := 0

def isReal (t : Expr) : Bool := t.consumeMData.isConstOf ``Real

/-- class of an atom that mentions the real ∃-variables `cs` -/
def classify (cs : Array FVarId) (a : Expr) : MetaM String := do
  let a := a.consumeMData
  let present := cs.filter fun c => occ c a > 0
  if present.size > 1 then return "multi"
  let c := present[0]!
  -- normalise ≥ / > to ≤ / <
  let rel? : Option (Expr × Expr × Expr) :=
    if a.isAppOfArity ``LE.le 4 || a.isAppOfArity ``LT.lt 4 then some (a.getArg! 0, a.getArg! 2, a.getArg! 3)
    else if a.isAppOfArity ``GE.ge 4 || a.isAppOfArity ``GT.gt 4 then some (a.getArg! 0, a.getArg! 3, a.getArg! 2)
    else none
  let some (ty, lhs, rhs) := rel? | return "other"
  if !isReal ty then return "nonreal"
  let rhs := rhs.consumeMData
  let lhs := lhs.consumeMData
  -- sign atom: literal on the left, the variable alone on the right
  if rhs.isFVarOf c && !lhs.hasFVar then return "sign"
  if occ c lhs > 0 then
    return (if occ c rhs > 0 then "both-sides" else "lower")
  if rhs.isFVarOf c then return "O1"
  let fs := factors rhs
  let withC := fs.filter fun f => occ c f > 0
  if withC.size == 1 && withC[0]!.isFVarOf c then
    return (if fs[0]!.isFVarOf c then "O" else "Oprod")
  return "upper-other"

partial def walk (cs : Array FVarId) (e : Expr) (acc : Acc) : MetaM Acc := do
  let e := e.consumeMData
  if e.isAppOfArity ``Exists 2 then
    let ty := e.getArg! 0
    let body := e.getArg! 1
    let .lam n _ b _ := body.consumeMData | return { acc with atoms := acc.atoms.push "other" }
    withLocalDeclD n ty fun x => do
      let acc := if isReal ty then { acc with realEx := acc.realEx + 1 }
        else if ty.consumeMData.isConstOf ``Nat then { acc with natEx := acc.natEx + 1 }
        else { acc with otherEx := acc.otherEx + 1 }
      walk (if isReal ty then cs.push x.fvarId! else cs) (b.instantiate1 x) acc
  else if e.isAppOfArity ``And 2 then
    walk cs (e.getArg! 1) (← walk cs (e.getArg! 0) acc)
  else if let .forallE n d b bi := e then
    let acc := if cs.any (fun c => occ c d > 0) then { acc with hypMentions := acc.hypMentions + 1 } else acc
    withLocalDecl n bi d fun x => walk cs (b.instantiate1 x) acc
  else if cs.any (fun c => occ c e > 0) then
    let k ← classify cs e
    return (if k == "sign" then { acc with signed := acc.signed + 1 } else { acc with atoms := acc.atoms.push k })
  else return acc

run_cmd do
  let names := (← IO.FS.lines "../../../out/corpus/lesssim/producers.txt").filter (· ≠ "")
  let env ← getEnv
  let mut out : Array String := #[]
  let mut missing := 0
  for s in names do
    -- names are printed with `toString`; private names need the stored Name, so search by string
    let n := s.toName
    let some ci := env.find? n | do missing := missing + 1; out := out.push (Json.mkObj [("name", s), ("missing", true)]).compress; continue
    let acc ← liftTermElabM <| forallTelescope ci.type fun _ body => walk #[] body {}
    out := out.push (Json.mkObj [("name", s), ("realEx", acc.realEx), ("natEx", acc.natEx), ("otherEx", acc.otherEx),
      ("signed", acc.signed), ("hypMentions", acc.hypMentions), ("atoms", toJson acc.atoms)]).compress
  IO.FS.writeFile "../../../out/corpus/lesssim/shape.jsonl" ("\n".intercalate out.toList ++ "\n")
  IO.println s!"SHAPE {names.size} missing {missing}"

end Lesssim.Shape
