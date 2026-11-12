/-
Fixed support for lean/Run/Narrowing.lean (plan nodes Q1 and Q2): two commands that READ FACTS FROM LEAN and
print them, one tab-separated line each, for `clausal narrowing` to compare with what the compiler did.

  #calls "<id>" : <term>
      `<term>` is `(op).calls` for the operation of one claim of a compiled reading, as the compiler wrote it
      (under `fun (x : T) ... =>` for the outline parameters it mentions). Prints the constructor of
      `Frames.Calls` it reduces to, and whether the operation is a sequence (the elaborated term mentions
      `Frames.Op.andThen`):              CALLS <id> <every | accepted | rejected> <single | sequence>
      This is the value `Frames.Op.HoldsAt` matches on: which calls the claim is about, according to Lean.

  #narrowing_report <theorem names>
      For each name, one of
        proved        declared, and its proof uses no `sorryAx`
        notproved     declared, its STATEMENT elaborated (its type has no `sorry`), but its script failed: Lean keeps
                      the statement with `sorryAx` as the proof. This is the only state that is an answer "not shown".
        badstatement  declared, but the STATEMENT did not elaborate: Lean recovers from the error by putting `sorry`
                      in the type. A generator fault, never an answer (a failed script and a broken statement both
                      leave `sorryAx` among the axioms; the type tells them apart).
        missing       not declared at all. A generator fault, never an answer.
                                          NARROWING <name> <state> <axioms>
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
  let seq := if (e.find? (·.isConstOf ``Frames.Op.andThen)).isSome then "sequence" else "single"
  IO.println s!"CALLS\t{id.getString}\t{name}\t{seq}"

elab "#narrowing_report " ids:ident* : command => do
  let env ← getEnv
  for i in ids do
    let n := i.getId
    if env.contains n then
      let ax ← liftCoreM (collectAxioms n)
      let ty := (← liftCoreM (getConstInfo n)).type
      let state := if ty.hasSorry then "badstatement" else if ax.contains ``sorryAx then "notproved" else "proved"
      IO.println s!"NARROWING\t{n}\t{state}\t{", ".intercalate (ax.toList.map toString)}"
    else
      IO.println s!"NARROWING\t{n}\tmissing\t"
