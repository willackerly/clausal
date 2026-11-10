/-
`#follows` : kernel-checked evidence that existing theorems are instances of a general lemma.

    #follows "<tag>" ["Full.Name.of.member", ...] := <proof term>
    #follows_file "<tag>" "<file with one full name per line>" := <proof term>

For every member `m` (full kernel name as printed by `Name.toString`, so private names work) the
proof term is elaborated against EXACTLY `m`'s type and the result is added to the environment as
a new theorem `ReuseCheck.<tag>.«<member>»` through `Environment.addDeclCore`, i.e. it is
type-checked by the kernel synchronously, and a kernel error makes the member FAIL. The
term must not mention `m` itself (checked), must not contain `sorry`, and the new theorem's axioms
are collected. One JSON line per member is appended to the file named by `REUSE_CHECK_OUT`.
-/
import Lean
open Lean Elab Command Term Meta

namespace ReuseCheck

def findConst (env : Environment) (s : String) : Option ConstantInfo :=
  env.constants.fold (init := none) fun acc n ci =>
    if acc.isSome then acc else if n.toString == s then some ci else none

def oneLine (s : String) : String := " ".intercalate (s.splitOn "\n")

def checkMembersWith (tag : String) (members : Array String) (termText : String)
    (mk : ConstantInfo → TermElabM Expr) (start : Nat := 0) : CommandElabM Unit := do
  let out? ← IO.getEnv "REUSE_CHECK_OUT"
  let mut nOk : Nat := 0
  let mut i : Nat := start
  let env0 ← getEnv
  -- resolve all names in one pass
  let want : Std.HashSet String := Std.HashSet.ofList members.toList
  let tbl : Std.HashMap String ConstantInfo := env0.constants.fold (init := {}) fun acc n ci =>
    let s := n.toString
    if want.contains s then acc.insert s ci else acc
  for m in members do
    i := i + 1
    let res : Except String (Array Name) ← (do
      let some ci := tbl[m]? | return .error "member not found in the environment"
      let newName := ((`ReuseCheck).str tag).str m
      try
        let axs ← liftTermElabM <| withLevelNames ci.levelParams do
          let v ← mk ci
          let v ← instantiateMVars v
          if v.hasExprMVar || v.hasLevelMVar then throwError "proof term has unassigned metavariables"
          if v.hasSorry then throwError "proof term contains sorry"
          if (v.getUsedConstantsAsSet).contains ci.name then
            throwError "proof term mentions the member itself"
          -- synchronous kernel check (`Lean.addDecl` checks asynchronously and only LOGS a
          -- kernel error, which would let a wrong proof pass as "ok")
          let decl : Declaration :=
            .thmDecl { name := newName, levelParams := ci.levelParams, type := ci.type, value := v }
          let opts ← getOptions
          match (← getEnv).addDeclCore (Core.getMaxHeartbeats opts).toUSize
              (maxRecDepth.get opts).toUSize decl none true with
          | .ok env => setEnv env
          | .error e => throwError "kernel: {e.toMessageData opts}"
          let axs ← collectAxioms newName
          if axs.contains ``sorryAx then throwError "depends on sorryAx"
          if axs.any fun a => a != ``propext && a != ``Classical.choice && a != ``Quot.sound then
            throwError "unexpected axioms: {axs}"
          pure axs
        return .ok axs
      catch ex =>
        return .error (oneLine (← ex.toMessageData.toString)))
    let (ok, note) : Bool × String := match res with
      | .ok axs => (true, ", ".intercalate (axs.toList.map Name.toString))
      | .error e => (false, e)
    if ok then nOk := nOk + 1 else logWarning m!"{tag}: {m}: FAILED: {note}"
    if let some out := out? then
      let h ← IO.FS.Handle.mk out .append
      h.putStrLn (Json.mkObj [("tag", tag), ("member", m), ("ok", ok),
        ("note", (note.take 600).toString), ("term", termText)]).compress
  logInfo m!"{tag}: {nOk} of {members.size} members follow (kernel-checked)"

def checkMembers (tag : String) (members : Array String) (t : Syntax) : CommandElabM Unit :=
  checkMembersWith tag members (oneLine (toString t.reprint.get!)) fun ci => do
    let v ← elabTermEnsuringType t ci.type
    synthesizeSyntheticMVarsNoPostponing
    return v

/-- Exact-statement duplicates: every member's type must be the representative's type, so the
representative constant itself (same universe parameters, by position) is the proof. -/
def checkDups (file : String) (tag : String := "dup") : CommandElabM Unit := do
  let env ← getEnv
  let mut start := 0
  let mut names : Std.HashSet String := {}
  let mut groups : Array (String × Array String) := #[]
  for l in (← IO.FS.lines file) do
    let .ok j := Json.parse l | continue
    let .ok rep := j.getObjValAs? String "rep" | continue
    let .ok ms := j.getObjValAs? (Array String) "members" | continue
    groups := groups.push (rep, ms)
    names := names.insert rep
  let reps : Std.HashMap String ConstantInfo := env.constants.fold (init := {}) fun acc n ci =>
    let s := n.toString
    if names.contains s then acc.insert s ci else acc
  for (rep, ms) in groups do
    let some rci := reps[rep]? | logWarning m!"dup: representative {rep} not found"
    checkMembersWith tag ms s!"@{rep}" (start := start) fun ci => do
      unless ci.levelParams.length == rci.levelParams.length do
        throwError "different number of universe parameters"
      return .const rci.name (ci.levelParams.map mkLevelParam)
    start := start + ms.size

elab "#follows_dups " f:str : command => checkDups f.getString

/-- Same check for arbitrary (representative, members) pairs, e.g. a theorem and its copy in a
cloned module: succeeds iff the copy's statement is definitionally the original's. -/
elab "#follows_pairs " tag:str f:str : command => checkDups f.getString tag.getString

elab "#follows " tag:str " [" ms:str,* "]" " := " t:term : command =>
  checkMembers tag.getString (ms.getElems.map (·.getString)) t

elab "#follows_file " tag:str f:str " := " t:term : command => do
  let ls := ((← IO.FS.lines f.getString).filter (· ≠ ""))
  checkMembers tag.getString ls t

end ReuseCheck
