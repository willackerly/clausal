/-
deadcode/Closure: the constants the kernel needs for a list of declarations, with no folding at all.

  lean --run Closure.lean <modulesFile> <namesFile> <rootPrefixes,comma> <out.json>

Walks type and value of every constant reachable from the given names (through the whole library) and
writes the ones that live in a project module.  Used to check the folded graph of Export.lean: every
constant listed here must be, or belong to, a declaration the folded graph calls reachable.
Imports only `Lean`.
-/
import Lean
open Lean

def parseName' (s : String) : Name := Id.run do
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

unsafe def main (args : List String) : IO UInt32 := do
  let modsFile :: namesFile :: rootsS :: out :: _ := args
    | IO.eprintln "usage: <modulesFile> <namesFile> <rootPrefixes> <out.json>"; return 1
  let mods := ((← IO.FS.lines modsFile).filter (· ≠ "")).map String.toName
  let names := (← IO.FS.lines namesFile).filter (· ≠ "")
  let roots := (rootsS.splitOn ",").map String.toName
  initSearchPath (← findSysroot)
  let env ← importModules (mods.map fun m => {module := m}) {} (trustLevel := 1024)
  let modNames := env.header.moduleNames
  let inProject (n : Name) : Bool := match env.getModuleIdxFor? n with
    | some i => roots.any (·.isPrefixOf modNames[i.toNat]!)
    | none => false
  let mut seen : NameSet := {}
  let mut stack : Array Name := names.map parseName'
  let mut proj : Array String := #[]
  while !stack.isEmpty do
    let n := stack.back!
    stack := stack.pop
    if seen.contains n then continue
    seen := seen.insert n
    match env.find? n with
    | none => continue
    | some ci =>
      if inProject n then proj := proj.push n.toString
      for c in ci.type.getUsedConstants do
        if !seen.contains c then stack := stack.push c
      if let some v := ci.value? (allowOpaque := true) then
        for c in v.getUsedConstants do
          if !seen.contains c then stack := stack.push c
      match ci with
      | .inductInfo iv => for c in iv.ctors do if !seen.contains c then stack := stack.push c
      | .ctorInfo cv => if !seen.contains cv.induct then stack := stack.push cv.induct
      | .recInfo rv => for c in rv.all do if !seen.contains c then stack := stack.push c
      | _ => pure ()
  IO.FS.writeFile out (Json.compress (Json.mkObj [("closure", toJson seen.size), ("project", toJson (proj.qsort (· < ·)))]))
  return 0
