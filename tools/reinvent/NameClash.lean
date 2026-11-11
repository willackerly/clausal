/-
M7 side check: project declarations whose full name also exists in the project's pinned Mathlib
(in a module the project may or may not import).  usage: lean --run NameClash.lean names.txt
Loads Mathlib only (never the project), so the hit is a library constant of the same name.
-/
import Lean
open Lean

unsafe def main (args : List String) : IO UInt32 := do
  initSearchPath (← findSysroot)
  let env ← importModules #[{ module := `Mathlib }] {} (trustLevel := 1024)
  let mut byStr : Std.HashMap String Name := {}
  for (n, _) in env.constants.map₁.toList do
    byStr := byStr.insert (n.toString (escape := false)) n
  for l in (← IO.FS.lines args.head!) do
    if let some n := byStr[l]? then
      let kind := match env.find? n with
        | some (.thmInfo _) => "theorem"
        | some (.defnInfo _) => "def"
        | some (.inductInfo _) => "inductive"
        | _ => "other"
      let m := match env.getModuleIdxFor? n with
        | some i => env.header.moduleNames[i.toNat]!.toString
        | none => ""
      IO.println s!"{l}\t{kind}\t{m}"
  return 0
