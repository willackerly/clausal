/- Independent check: raw constant closure (no auxiliary folding) below given roots,
   restricted to project modules. Prints one name per line. -/
import Lean
open Lean
unsafe def main (args : List String) : IO Unit := do
  let modsFile :: outFile :: roots := args | throw <| IO.userError "usage"
  initSearchPath (← findSysroot)
  let mods := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (mods.map fun m => { module := m }) {}
  let proj : Array Bool := env.header.moduleNames.map fun m =>
    [`NavierStokes, `Euler].contains m.getRoot
  let isProj (n : Name) := match env.getModuleIdxFor? n with
    | some i => proj[i.toNat]! | none => false
  let mut seen : Std.HashSet Name := {}
  let mut todo : Array Name := roots.toArray.map (·.toName)
  while !todo.isEmpty do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n || !isProj n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      todo := todo ++ ci.type.getUsedConstants
      match ci with
      | .thmInfo v => todo := todo ++ v.value.getUsedConstants
      | .defnInfo v => todo := todo ++ v.value.getUsedConstants
      | .opaqueInfo v => todo := todo ++ v.value.getUsedConstants
      | .inductInfo v => todo := todo ++ v.ctors.toArray
      | _ => pure ()
  IO.FS.writeFile outFile ("\n".intercalate (seen.toList.map (·.toString (escape := false))))
