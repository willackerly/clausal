import F00079_re
open Lean Meta Elab Command
partial def findPath (env : Environment) (start target : Name) : Option (List Name) := Id.run do
  let mut seen : Std.HashSet Name := {}
  let mut q : Array (Name × List Name) := #[(start, [start])]
  let mut i := 0
  while i < q.size do
    let (c, p) := q[i]!
    i := i + 1
    if c == target then return some p.reverse
    if seen.contains c then continue
    seen := seen.insert c
    let some ci := env.find? c | continue
    let ok := match env.getModuleIdxFor? c with
      | some j => let m := env.header.moduleNames[j.toNat]!; (`NavierStokes).isPrefixOf m || m.toString.startsWith "F"
      | none => true
    if !ok then continue
    let mut used := ci.type.getUsedConstants
    if let some v := ci.value? (allowOpaque := true) then used := used ++ v.getUsedConstants
    for u in used do
      if !seen.contains u then q := q.push (u, u :: p)
  return none
run_cmd do
  let env ← getEnv
  IO.println s!"{findPath env `NavierStokes.WeightedClasses.MemClass.band_smul_R `NavierStokes.WeightedClasses.MemClass.band_smul}"
