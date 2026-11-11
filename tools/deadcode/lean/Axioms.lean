/-
deadcode/Axioms: axioms of a list of declarations, from a built project.

  lean --run Axioms.lean <modulesFile> <namesFile> <out.json>

LEAN_PATH must point at the build to inspect (the Python driver sets it).  Writes
{name: [axioms, sorted]} with null for a name that is not in the environment.
Imports only `Lean`; runs on the project's own toolchain (tested 4.34.0-rc2, 4.36.0-rc1/rc2).
-/
import Lean
open Lean

/-- Parse a printed name; a component made of digits is a numeric component (private names). -/
def parseName (s : String) : Name := Id.run do
  let mut n : Name := .anonymous
  let mut cur : Array Char := #[]
  let mut quoted := false
  let push (n : Name) (cur : Array Char) : Name :=
    let str := String.ofList cur.toList
    if !cur.isEmpty && cur.all Char.isDigit then Name.num n str.toNat! else Name.str n str
  for c in s.toList do
    if c == '«' then quoted := true
    else if c == '»' then quoted := false
    else if c == '.' && !quoted then
      n := push n cur
      cur := #[]
    else cur := cur.push c
  return push n cur

/-- Constants a constant's kernel check depends on directly: the same edges as Lean's `collectAxioms`. -/
def directDeps (ci : ConstantInfo) : Array Name :=
  let t := ci.type.getUsedConstants
  match ci with
  | .defnInfo v => t ++ v.value.getUsedConstants
  | .thmInfo v => t ++ v.value.getUsedConstants
  | .opaqueInfo v => t ++ v.value.getUsedConstants
  | .inductInfo v => t ++ v.ctors.toArray
  | _ => t

unsafe def main (args : List String) : IO UInt32 := do
  let modsFile :: namesFile :: out :: _ := args
    | IO.eprintln "usage: <modulesFile> <namesFile> <out.json>"; return 1
  let mods := ((← IO.FS.lines modsFile).filter (· ≠ "")).map String.toName
  let names := (← IO.FS.lines namesFile).filter (· ≠ "")
  initSearchPath (← findSysroot)
  let env ← importModules (mods.map fun m => {module := m}) {} (trustLevel := 1024)
  -- one forward walk from all names, recording reverse edges; then, for every axiom met, a backward
  -- walk.  `collectAxioms` once per name gives the same sets but walks the library once per name.
  let roots := names.map parseName
  let mut seen : NameSet := {}
  let mut rev : Std.HashMap Name (Array Name) := {}
  let mut axs : Array Name := #[]
  let mut stack : Array Name := roots
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | none => continue
    | some ci =>
      if ci matches .axiomInfo _ then axs := axs.push n
      for c in directDeps ci do
        rev := rev.alter c fun o => some ((o.getD #[]).push n)
        if !seen.contains c then stack := stack.push c
  let mut reach : Std.HashMap Name NameSet := {}
  for a in axs do
    let mut r : NameSet := {}
    let mut st : Array Name := #[a]
    while !st.isEmpty do
      let n := st.back!
      st := st.pop
      if r.contains n then continue
      r := r.insert n
      for u in rev.getD n #[] do
        if !r.contains u then st := st.push u
    reach := reach.insert a r
  let mut rows : Array (String × Json) := #[]
  for s in names do
    let n := parseName s
    if env.contains n then
      let a := axs.filter fun x => (reach.getD x {}).contains n
      rows := rows.push (s, toJson (a.map (·.toString) |>.qsort (· < ·)))
    else
      rows := rows.push (s, Json.null)
  IO.FS.writeFile out (Json.compress (Json.mkObj rows.toList))
  return 0
