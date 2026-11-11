import F15
import F19
import F42
import F46
import F73
import F79
import F2076
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let insts : List Name := [`Fam.F79.memClass_iff, `Fam.F79.uniformClass_iff, `Fam.F79.localJets_iff,
    `Fam.F19.members_eq, `Fam.F46.m1, `Fam.F46.m2, `Fam.F46.m3, `Fam.F46.m4, `Fam.F73.member_eq,
    `Fam.F2076.jetRate_iff, `Fam.F2076.finiteJetRate_iff, `Fam.F15.coefficientsTranslation, `Fam.F15.coefficientsOn,
    `Fam.F15.nativeJets, `Fam.F15.scalarOn, `Fam.F15.support] ++ (List.range 18).map (fun i => (`Fam.F42).str (if i < 9 then s!"m0{i+1}" else s!"m{i+1}"))
  for n in insts do
    let some ci := env.find? n | IO.println s!"missing {n}"
    let mut e := ci.type
    if let some v := ci.value? then e := mkApp e v
    let cs := e.getUsedConstants.filter fun c =>
      match env.getModuleIdxFor? c with
      | some i => let m := env.header.moduleNames[i.toNat]!; (`NavierStokes).isPrefixOf m || (`Euler).isPrefixOf m || m.toString.startsWith "F"
      | none => false
    let fam := cs.filter fun c => (`Fam).isPrefixOf c
    let corpusDefs := cs.filter fun c => !(`Fam).isPrefixOf c && (match env.find? c with | some (.defnInfo _) => true | some (.inductInfo _) => true | _ => false)
    IO.println s!"{n}: Fam consts {fam.toList.take 4} | corpus defs {corpusDefs.size}: {(corpusDefs.toList.take 4)}"
