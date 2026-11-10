#!/usr/bin/env python3
"""Independent audit of one scored P2 copy (p2/score/work/<arm>), written for scoring, not taken from the pipeline.

    python3 p2/score/audit.py <copy-dir> <out.json>

1. Writes <copy>/lean/ScoreAudit.lean, which imports Spec.Statements and the 16 proof modules and prints, per
   scenario: does `Spec.inventory.<id>` exist, is it a theorem, is its type *syntactically* the constant
   `Spec.inventory.<id>.stmt`, which module declares it, which axioms it depends on (`Lean.collectAxioms`), and
   which hand-written constants (modules Lemmas.* and Spec.Proofs.*) it reaches, entering proofs. Per hand-written
   Lemmas declaration: module, line range, kind, model functions in its type, Aeneas library constants it uses.
   This code shares nothing with lean/Bdd/Audit.lean.
2. Replays every Lemmas module and every proof module through the kernel with the toolchain's `leanchecker`
   (lean4checker): catches anything added without kernel checking (e.g. `set_option debug.skipKernelTC`).
3. Writes one JSON file with all of it.

Run once per arm after a full ./run.sh in the copy (the modules must be built). Not an iterative loop.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCEN = ["stock_is_sum", "stock_too_big", "find_first_bin", "find_no_bin", "restock_adds", "restock_counts",
        "take_amount", "take_stock_down", "take_earliest_first", "fill_count", "fill_state", "fill_at_most",
        "count_products", "count_at_most_bins", "dominant_found", "dominant_none"]
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ENV = dict(os.environ, PATH=f"{Path.home()}/.elan/bin:{Path.home()}/.cargo/bin:" + os.environ.get("PATH", ""))

LEAN_TEMPLATE = r'''
import Lean
import Spec.Statements
{imports}
open Lean

namespace ScoreAudit

def modOf (env : Environment) (n : Name) : Option Name :=
  (env.getModuleIdxFor? n).bind fun i => env.header.moduleNames[i.toNat]?

def isHand (env : Environment) (n : Name) : Bool :=
  match modOf env n with
  | some m => (`Lemmas).isPrefixOf m || (`Spec.Proofs).isPrefixOf m
  | none => false

def used (ci : ConstantInfo) : Array Name :=
  let a := ci.type.getUsedConstants
  match ci.value? (allowOpaque := true) with
  | some v => a ++ v.getUsedConstants
  | none => a

/-- Hand-written constants reachable from `root`, entering hand-written values (proofs included) only. -/
def handClosure (env : Environment) (root : Name) : Array Name := Id.run do
  let mut seen : NameSet := {{}}
  let mut out : Array Name := #[]
  let mut todo : Array Name := #[root]
  let mut fuel := 1000000
  while !todo.isEmpty && fuel > 0 do
    fuel := fuel - 1
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    if !isHand env n then continue
    out := out.push n
    if let some ci := env.find? n then
      for m in used ci do
        if !seen.contains m then todo := todo.push m
  return out

def js (a : Array Name) : Json := Json.arr (a.map fun n => Json.str n.toString)

def kindOf : ConstantInfo → String
  | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .opaqueInfo _ => "opaque" | .axiomInfo _ => "axiom"
  | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor" | .recInfo _ => "rec" | .quotInfo _ => "quot"

def run (scen : List String) : CoreM Unit := do
  let env ← getEnv
  for s in scen do
    let t := Name.mkStr (Name.mkStr (Name.mkStr .anonymous "Spec") "inventory") s
    let st := Name.mkStr t "stmt"
    match env.find? t with
    | none => IO.println s!"SCORE\t{{(Json.mkObj [("kind", "scenario"), ("id", s), ("exists", false)]).compress}}"
    | some ci =>
      let ax ← collectAxioms t
      let isThm := match ci with | .thmInfo _ => true | _ => false
      let stmtMod := (modOf env st).map toString
      IO.println s!"SCORE\t{{(Json.mkObj [("kind", "scenario"), ("id", s), ("exists", true), ("is_theorem", isThm),
        ("type_exact", ci.type == mkConst st), ("level_params", ci.levelParams.length),
        ("module", toJson ((modOf env t).map toString)), ("stmt_module", toJson stmtMod),
        ("axioms", js ax), ("hand", js (handClosure env t))]).compress}}"
  -- every constant declared in a Lemmas module
  let names := env.header.moduleNames
  for h : i in [0:names.size] do
    let m := names[i]
    if !(`Lemmas).isPrefixOf m then continue
    for c in env.header.moduleData[i]!.constNames do
      let some ci := env.find? c | continue
      let rng ← findDeclarationRanges? c
      let modelFns := ci.type.getUsedConstants.filter fun x => (`inventory).isPrefixOf x
      let lib := (used ci).filter fun x => !isHand env x
      let aen := lib.filter fun x => (`Aeneas).isPrefixOf x
      let ax ← collectAxioms c
      IO.println s!"SCORE\t{{(Json.mkObj [("kind", "decl"), ("name", c.toString), ("module", m.toString),
        ("decl_kind", kindOf ci),
        ("start", toJson (rng.map (·.range.pos.line))), ("end", toJson (rng.map (·.range.endPos.line))),
        ("model_fns_in_type", js modelFns), ("aeneas_used", js aen), ("axioms", js ax)]).compress}}"

end ScoreAudit

#eval ScoreAudit.run [{scen}]
'''


def main():
    copy = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]).resolve()
    lean = copy / "lean"
    imports = "\n".join(f"import Spec.Proofs.inventory.{s}" for s in SCEN)
    (lean / "ScoreAudit.lean").write_text(LEAN_TEMPLATE.format(imports=imports, scen=", ".join(f'"{s}"' for s in SCEN)))
    r = subprocess.run(["lake", "env", "lean", "ScoreAudit.lean"], cwd=lean, env=ENV, capture_output=True, text=True,
                       timeout=1800)
    lines = [json.loads(l.split("\t", 1)[1]) for l in r.stdout.splitlines() if l.startswith("SCORE\t")]
    result = {"copy": str(copy), "lean_exit": r.returncode, "lean_stderr": r.stderr[-4000:],
              "lean_errors": [l for l in r.stdout.splitlines() if ": error" in l][:20],
              "scenarios": {}, "decls": []}
    for d in lines:
        if d["kind"] == "scenario":
            d["proved"] = bool(d.get("exists") and d.get("is_theorem") and d.get("type_exact")
                               and d.get("module") == f"Spec.Proofs.inventory.{d['id']}"
                               and d.get("stmt_module") == "Spec.Statements"
                               and set(d.get("axioms", [])) <= STANDARD_AXIOMS)
            result["scenarios"][d["id"]] = d
        else:
            result["decls"].append(d)
    # kernel replay of every hand-written module
    mods = sorted("Lemmas." + p.stem for p in (lean / "Lemmas").glob("*.lean")) + \
        [f"Spec.Proofs.inventory.{s}" for s in SCEN]
    replay = {}
    for m in mods:
        rr = subprocess.run(["lake", "env", "leanchecker", m], cwd=lean, env=ENV, capture_output=True, text=True,
                            timeout=1800)
        replay[m] = {"exit": rr.returncode, "tail": (rr.stdout + rr.stderr).strip()[-600:]}
    result["kernel_replay"] = replay
    (lean / "ScoreAudit.lean").unlink()
    out.write_text(json.dumps(result, indent=1))
    ok = sum(1 for d in result["scenarios"].values() if d["proved"])
    rep_ok = sum(1 for v in replay.values() if v["exit"] == 0)
    print(f"{copy.name}: {ok}/{len(SCEN)} scenarios proved by this audit; kernel replay ok for {rep_ok}/{len(replay)} "
          f"modules; {len(result['decls'])} Lemmas constants listed")


if __name__ == "__main__":
    main()
