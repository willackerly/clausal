/-
Robustness sweep for `Rosette.Lift` (a script, not part of the `Rosette` library):
lift up to 5 lemmas out of every public Mathlib theorem whose name hash is 0 mod N and whose proof
has at least 400 DAG nodes; every lift is kernel-checked by `liftConst` (which also checks that no
axiom was added). Prints one summary line and one `FAIL` line per failure.

    lake build Rosette.Lift && ROSETTE_SWEEP_MOD=60 lake env lean bench/sweep.lean   (about 1 min)

`ROSETTE_SWEEP_MOD` defaults to 240 (about 15 s).
-/
import Mathlib
import Rosette.Lift
open Lean Meta Elab Command Rosette
set_option maxHeartbeats 0
run_meta do
  let env ← getEnv
  let modulus := ((← IO.getEnv "ROSETTE_SWEEP_MOD").bind String.toNat?).getD 240
  let mut names : Array Name := #[]
  for (n, ci) in env.constants.map₁.toList do
    if let .thmInfo _ := ci then
      if n.isInternalDetail then continue
      if (hash n).toNat % modulus != 0 then continue
      names := names.push n
  let mut tried := 0; let mut ok := 0; let mut lifted := 0; let mut nolift := 0
  let mut trunc := 0; let mut errs := 0; let mut subErrs := 0; let mut reused := 0; let mut multi := 0
  let mut fails : Array String := #[]
  let t0 ← IO.monoMsNow
  for n in names do
    let p ← proofOfConst n
    if dagSize p < 400 then continue
    tried := tried + 1
    let saved ← getEnv
    try
      let r ← liftConst n { k := 5 }
      ok := ok + 1
      lifted := lifted + r.lemmas.size
      if r.lemmas.isEmpty then nolift := nolift + 1
      if r.enumeration.truncated then trunc := trunc + 1
      subErrs := subErrs + r.enumeration.errors
      for l in r.lemmas do
        if l.uses > 1 then reused := reused + 1
        if l.cand.occurrences > 1 then multi := multi + 1
    catch ex =>
      errs := errs + 1
      let m ← ex.toMessageData.toString
      fails := fails.push s!"{n}: {(m.take 300).toString}"
    setEnv saved
  let t1 ← IO.monoMsNow
  IO.println s!"sampled theorems={names.size} tried(dag>=400)={tried} ok={ok} failed={errs} lemmasLifted={lifted} nothingLifted={nolift} truncatedEnum={trunc} perSubtermErrors={subErrs} lemmasSharedByStatement={reused} lemmasWithSeveralPositions={multi} modulus={modulus} ms={t1-t0}"
  for f in fails do IO.println s!"FAIL {f}"
