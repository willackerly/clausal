/-
Fixed support for lean/Run/Narrowing.lean (plan nodes Q1 and Q2): two commands that READ FACTS FROM LEAN and
print them, one tab-separated line each, for `clausal narrowing` to compare with what the compiler did.

  #calls "<id>" : <term>
      `<term>` is `(op).calls` for the operation of one claim of a compiled reading, as the compiler wrote it
      (under `fun (x : T) ... =>` for the outline parameters it mentions). Prints the constructor of
      `Frames.Calls` it reduces to:      CALLS <id> <every | accepted | rejected>
      This is the value `Frames.Op.HoldsAt` matches on: which calls the claim is about, according to Lean.

  #narrowing_report <theorem names>
      For each name: `proved` (declared, and its proof uses no `sorryAx`), `notproved` (declared, but its script
      failed: Lean keeps the statement with `sorryAx`), or `missing` (the STATEMENT did not elaborate; a generator
      fault, never an answer).            NARROWING <name> <state> <axioms>
-/
import Lean
import Frames.Narrowing
open Lean Elab Command Term Meta

elab "#calls " id:str " : " t:term : command => liftTermElabM do
  let e ← elabTerm t none
  synthesizeSyntheticMVarsNoPostponing
  let e ← instantiateMVars e
  let c ← lambdaTelescope e fun _ body => do
    let ty ← whnf (← inferType body)
    unless ty.isConstOf ``Frames.Calls do
      throwError "#calls: the term is not a `Frames.Calls`"
    whnf body
  let name := match c.getAppFn with
    | .const n _ => if n.getPrefix == ``Frames.Calls then n.getString! else "?"
    | _ => "?"
  IO.println s!"CALLS\t{id.getString}\t{name}"

elab "#narrowing_report " ids:ident* : command => do
  let env ← getEnv
  for i in ids do
    let n := i.getId
    if env.contains n then
      let ax ← liftCoreM (collectAxioms n)
      let state := if ax.contains ``sorryAx then "notproved" else "proved"
      IO.println s!"NARROWING\t{n}\t{state}\t{", ".intercalate (ax.toList.map toString)}"
    else
      IO.println s!"NARROWING\t{n}\tmissing\t"
