/-
M9 families: is a theorem's proof GENERIC in a family member?

For a theorem `T` and a set of member constants `Ms`, replace every member by a variable `M'` of the same
type, and every theorem that `T`'s proof cites and whose statement mentions a member by a hypothesis with
that statement (member replaced).  If the result type-checks, the proof never looks inside the member: it
uses it only through the cited lemmas, i.e. as an interface.  The abstracted theorem is then added to the
environment (kernel-checked) as `Fam.Abs.<T>`:   ∀ M' (cited lemmas for M'), statement[M'].

Outcomes:  generic      kernel-checked abstraction
           opens        the proof uses a constructor / projection / recursor of a member structure
           unfolds      abstraction does not type-check (the proof needs the member's body by unfolding)
           error        something else (reported)
Reducible definitions (`abbrev`) built on a member are unfolded first, so going through
`WaveClass := MemClass …` is not counted as looking inside `MemClass`.  Other definitions built on a member
are left as they are: a proof that unfolds one of them to reach the member counts as `unfolds`.
-/
import Tool

open Lean Meta Elab Command

namespace Fam.Abs

structure Ctx where
  ms : NameSet
  memo : IO.Ref (Std.HashMap Name Bool)

/-- does the constant's value (transitively through definitions, depth-limited) or type mention a member? -/
partial def builtOn (c : Ctx) (n : Name) (depth : Nat := 4) : CoreM Bool := do
  if c.ms.contains n then return false
  if let some r := (← c.memo.get)[n]? then return r
  let env ← getEnv
  let r ← match env.find? n with
    | some (.defnInfo d) =>
      if ((`NavierStokes).isPrefixOf n || n.toString.startsWith "Euler" || (`Fam).isPrefixOf n)
          && (getReducibilityStatusCore env n == .reducible) then
        let used := d.value.getUsedConstants ++ d.type.getUsedConstants
        if used.contains n then pure false
        else if used.any c.ms.contains then pure true
        else if depth == 0 then pure false
        else used.anyM (fun u => builtOn c u (depth - 1))
      else pure false
    | _ => pure false
  c.memo.modify (·.insert n r)
  return r

def expand (c : Ctx) (e : Expr) : CoreM Expr := do
  let e ← Core.transform e (pre := fun e => do
    match e with
    | .const n us =>
      if (← builtOn c n) then
        let ci ← getConstInfo n
        return .visit (ci.instantiateValueLevelParams! us)
      else return .continue
    | _ => return .continue)
  Core.betaReduce e

def isOpener (env : Environment) (ms : NameSet) (n : Name) : Bool :=
  match env.find? n with
  | some (.ctorInfo v) => ms.contains v.induct
  | some (.recInfo v) => v.all.any ms.contains
  | _ => (ms.contains n.getPrefix) &&
      (env.isProjectionFn n || isAuxRecursor env n || isNoConfusion env n || (isMatcherCore env n))

partial def hasProjOf (ms : NameSet) (e : Expr) : Bool :=
  (e.find? fun x => match x with | .proj s _ _ => ms.contains s | _ => false).isSome

def mentions (ms : NameSet) (e : Expr) : Bool := (e.find? fun x => match x with | .const n _ => ms.contains n | _ => false).isSome

/-- distinct constant occurrences (name with universe levels) -/
def collectConsts (e : Expr) (acc : Array Expr) : Array Expr := Id.run do
  let mut acc := acc
  let mut stack := #[e]
  let mut vis : Std.HashSet ExprStructEq := {}
  let mut have_ : Std.HashSet Expr := acc.foldl (·.insert ·) {}
  while !stack.isEmpty do
    let x := stack.back!
    stack := stack.pop
    if vis.contains ⟨x⟩ then continue
    vis := vis.insert ⟨x⟩
    match x with
    | .const .. => if !have_.contains x then acc := acc.push x; have_ := have_.insert x
    | .app f a => stack := (stack.push f).push a
    | .lam _ d b _ => stack := (stack.push d).push b
    | .forallE _ d b _ => stack := (stack.push d).push b
    | .letE _ t v b _ => stack := ((stack.push t).push v).push b
    | .proj _ _ b => stack := stack.push b
    | .mdata _ b => stack := stack.push b
    | _ => pure ()
  return acc

def run (fam : String) (c : Ctx) (t : Name) (add : Bool) : MetaM Json := do
  let env ← getEnv
  let some ci := env.find? t | return Json.mkObj [("name", toJson t.toString), ("result", Json.str "missing")]
  let some v0 := ci.value? (allowOpaque := true) | return Json.mkObj [("name", toJson t.toString), ("result", Json.str "novalue")]
  let base : List (String × Json) := [("family", toJson fam), ("name", toJson t.toString), ("inStatement", toJson (mentions c.ms ci.type)),
    ("membersUsed", toJson ((v0.getUsedConstants ++ ci.type.getUsedConstants).filter c.ms.contains |>.toList.eraseDups.map (·.toString)))]
  try
    let v ← expand c v0
    let ty ← expand c ci.type
    let used := v.getUsedConstants
    let openers := used.filter (isOpener env c.ms)
    if !openers.isEmpty || hasProjOf c.ms v then
      return Json.mkObj (base ++ [("result", Json.str "opens"), ("openers", toJson (openers.map (·.toString)))])
    -- cited constants: non-members whose (expanded) type mentions a member
    let mut citedTypes : Array (Expr × Expr) := #[]   -- (const expr, its type)
    let mut seen : Std.HashSet Expr := {}
    let occ : Array Expr := collectConsts ty (collectConsts v #[])
    for e in occ do
      let .const n us := e | continue
      if c.ms.contains n || seen.contains e then continue
      seen := seen.insert e
      let some ni := env.find? n | continue
      if !((`NavierStokes).isPrefixOf n || n.toString.startsWith "Euler" || n.toString.startsWith "_private") then continue
      let nty ← expand c (ni.type.instantiateLevelParams ni.levelParams us)
      if mentions c.ms nty then citedTypes := citedTypes.push (e, nty)
    -- member occurrences (name with levels)
    let mut mocc : Array Expr := #[]
    for e in occ do
      if let .const n _ := e then if c.ms.contains n then mocc := mocc.push e
    -- collect member occurrences inside cited types too
    for (_, nty) in citedTypes do
      for e in collectConsts nty #[] do
        if let .const n _ := e then if c.ms.contains n && !mocc.contains e then mocc := mocc.push e
    let mtys ← mocc.mapM fun e => do
      let .const n us := e | unreachable!
      let mi ← getConstInfo n
      pure (mi.type.instantiateLevelParams mi.levelParams us)
    if mtys.any (mentions c.ms) then
      return Json.mkObj (base ++ [("result", Json.str "error"), ("why", Json.str "member type mentions a member")])
    let res ← withLocalDeclsDND ((mocc.mapIdx fun i _ => (Name.mkSimple s!"M{i}")).zip mtys) fun mf => do
      let rep1 (e : Expr) : Expr := e.replace fun x => (mocc.idxOf? x).map (fun i => mf[i]!)
      withLocalDeclsDND ((citedTypes.mapIdx fun i _ => (Name.mkSimple s!"L{i}")).zip (citedTypes.map fun p => rep1 p.2)) fun lf => do
        let cs := citedTypes.map (·.1)
        let rep2 (e : Expr) : Expr := e.replace fun x =>
          match mocc.idxOf? x with
          | some i => some mf[i]!
          | none => (cs.idxOf? x).map (fun i => lf[i]!)
        let v' := rep2 v
        let ty' := rep2 ty
        let ok ← try
            Meta.check v'
            let t' ← inferType v'
            isDefEq t' ty'
          catch _ => pure false
        if !ok then return (false, Expr.sort .zero, Expr.sort .zero)
        let val ← mkLambdaFVars (mf ++ lf) v'
        let typ ← mkForallFVars (mf ++ lf) ty'
        return (true, ← instantiateMVars val, ← instantiateMVars typ)
    let citedJ := toJson (citedTypes.map fun p => p.1.constName!.toString)
    if !res.1 then
      return Json.mkObj (base ++ [("result", Json.str "unfolds"), ("cited", citedJ)])
    if add then
      let nm := `Fam.Abs ++ t
      try
        addDecl (.thmDecl { name := nm, levelParams := ci.levelParams, type := res.2.2, value := res.2.1 })
      catch ex =>
        return Json.mkObj (base ++ [("result", Json.str "error"), ("why", toJson s!"kernel: {← ex.toMessageData.toString}"), ("cited", citedJ)])
      let ax ← collectAxioms nm
      return Json.mkObj (base ++ [("result", Json.str "generic"), ("kernel", true), ("cited", citedJ), ("absName", toJson nm.toString),
        ("axioms", toJson (ax.map (·.toString))), ("absStatementDag", toJson (Fam.sizes res.2.2).2)])
    return Json.mkObj (base ++ [("result", Json.str "generic"), ("kernel", false), ("cited", citedJ)])
  catch ex =>
    return Json.mkObj (base ++ [("result", Json.str "error"), ("why", toJson (← ex.toMessageData.toString))])

def go (fam : String) (ms : List Name) (ts : List Name) (add : Bool := true) : CommandElabM Unit := do
  let memo ← IO.mkRef {}
  let c : Ctx := { ms := ms.foldl (·.insert ·) {}, memo }
  for t in ts do
    let j ← liftTermElabM <| tryCatchRuntimeEx (withTheReader Core.Context (fun c => { c with maxRecDepth := 8192, maxHeartbeats := 60000 * 1000 }) (withCurrHeartbeats (run fam c t add)))
      (fun ex => do return Json.mkObj [("family", toJson fam), ("name", toJson t.toString), ("result", Json.str "error"), ("why", toJson (← ex.toMessageData.toString))])
    let h ← IO.FS.Handle.mk (System.FilePath.mk ((← IO.getEnv "FAM_OUT").getD "/dev/null")) .append
    h.putStrLn ("ABS " ++ j.compress); h.flush

/-- Restate `t` with every member replaced by its replacement constant (same type, same universe parameters).
`defeq`: the original proof is accepted by the kernel for the new statement as it stands.
`eq`: transported along the equation `member = replacement` (third component), kernel-checked. -/
def transportOne (fam : String) (pairs : List (Name × Name × Option Name)) (t : Name) : MetaM Json := do
  let env ← getEnv
  let some ci := env.find? t | return Json.mkObj [("name", toJson t.toString), ("result", Json.str "missing")]
  let ms : NameSet := pairs.foldl (fun s p => s.insert p.1) {}
  let base : List (String × Json) := [("family", toJson fam), ("name", toJson t.toString), ("statementDag", toJson (Fam.sizes ci.type).2)]
  if !mentions ms ci.type then return Json.mkObj (base ++ [("result", Json.str "nomention")])
  let repl (e : Expr) : Expr := e.replace fun x => match x with
    | .const n us => (pairs.find? (·.1 == n)).map fun p => .const p.2.1 us
    | _ => none
  let ty' := repl ci.type
  let nm := `Fam.Tr ++ t
  let lv := ci.levelParams.map Level.param
  let r1 ← try
      addDecl (.thmDecl { name := nm, levelParams := ci.levelParams, type := ty', value := .const t lv }); pure true
    catch _ => pure false
  if r1 then return Json.mkObj (base ++ [("result", Json.str "defeq"), ("newStatementDag", toJson (Fam.sizes ty').2)])
  try
    let mut cur := ci.type
    let mut prf : Expr := .const t lv
    for occ in collectConsts ci.type #[] do
      let .const n us := occ | continue
      let some p := pairs.find? (·.1 == n) | continue
      let some eqn := p.2.2 | throwError "no equation for {n}"
      let mty ← inferType occ
      let motive ← withLocalDeclD `X mty fun x => do
        mkLambdaFVars #[x] (cur.replace fun y => if y == occ then some x else none)
      let h ← mkCongrArg motive (.const eqn us)
      prf ← mkEqMP h prf
      cur := cur.replace fun y => if y == occ then some (.const p.2.1 us) else none
    addDecl (.thmDecl { name := `Fam.TrEq ++ t, levelParams := ci.levelParams, type := ty', value := ← instantiateMVars prf })
    return Json.mkObj (base ++ [("result", Json.str "eq"), ("newStatementDag", toJson (Fam.sizes ty').2)])
  catch ex =>
    return Json.mkObj (base ++ [("result", Json.str "fail"), ("why", toJson (← ex.toMessageData.toString))])

/-- Restate `t` by rewriting every full application of a member with its pointwise equation
(`∀ args, member args = primitive …`, proved by `rfl` in the family file).  The original proof must then be
accepted by the kernel for the new statement as it stands. -/
def transportEqnOne (fam : String) (eqns : List (Name × Name)) (t : Name) : MetaM Json := do
  let env ← getEnv
  let some ci := env.find? t | return Json.mkObj [("name", toJson t.toString), ("result", Json.str "missing")]
  let ms : NameSet := eqns.foldl (fun s p => s.insert p.1) {}
  let (st, sd) := Fam.sizes ci.type
  let base : List (String × Json) := [("family", toJson fam), ("name", toJson t.toString), ("statementDag", toJson sd), ("statementTree", toJson st)]
  if !mentions ms ci.type then return Json.mkObj (base ++ [("result", Json.str "nomention")])
  try
    let ty' ← Meta.transform ci.type (pre := fun e => do
      let .const n _ := e | return .continue
      let some p := eqns.find? (·.1 == n) | return .continue
      let thm ← mkConstWithFreshMVarLevels p.2
      let lam ← forallTelescope (← inferType thm) fun xs body => do
        let some (_, _, rhs) := body.eq? | throwError "equation expected: {p.2}"
        mkLambdaFVars xs rhs
      unless (← isDefEq (← inferType lam) (← inferType e)) do throwError "equation {p.2} does not match the type of {n}"
      return .done (← instantiateMVars lam))
    let ty' ← Core.betaReduce ty'
    let ty' := ty'.eta
    let ty' ← instantiateMVars ty'
    if mentions ms ty' then
      return Json.mkObj (base ++ [("result", Json.str "fail"), ("why", Json.str "member not fully applied in the statement")])
    let nm := `Fam.Tr ++ t
    addDecl (.thmDecl { name := nm, levelParams := ci.levelParams, type := ty', value := .const t (ci.levelParams.map Level.param) })
    let (st', sd') := Fam.sizes ty'
    return Json.mkObj (base ++ [("result", Json.str "defeq"), ("newStatementDag", toJson sd'), ("newStatementTree", toJson st')])
  catch ex =>
    return Json.mkObj (base ++ [("result", Json.str "fail"), ("why", toJson (← ex.toMessageData.toString))])

def transportEqns (fam : String) (eqns : List (Name × Name)) (ts : List Name) : CommandElabM Unit := do
  for t in ts do
    let j ← liftTermElabM <| tryCatchRuntimeEx (transportEqnOne fam eqns t)
      (fun ex => do return Json.mkObj [("family", toJson fam), ("name", toJson t.toString), ("result", Json.str "fail"), ("why", toJson (← ex.toMessageData.toString))])
    let h ← IO.FS.Handle.mk (System.FilePath.mk ((← IO.getEnv "FAM_OUT").getD "/dev/null")) .append
    h.putStrLn ("TR " ++ j.compress); h.flush

def transport (fam : String) (pairs : List (Name × Name × Option Name)) (ts : List Name) : CommandElabM Unit := do
  for t in ts do
    let j ← liftTermElabM <| tryCatchRuntimeEx (transportOne fam pairs t)
      (fun ex => do return Json.mkObj [("family", toJson fam), ("name", toJson t.toString), ("result", Json.str "fail"), ("why", toJson (← ex.toMessageData.toString))])
    let h ← IO.FS.Handle.mk (System.FilePath.mk ((← IO.getEnv "FAM_OUT").getD "/dev/null")) .append
    h.putStrLn ("TR " ++ j.compress); h.flush

end Fam.Abs
