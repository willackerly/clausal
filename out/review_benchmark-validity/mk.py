src=open('Rosette/Bench.lean').read()
src=src.replace('namespace Rosette.Bench','namespace Rosette.BenchR').replace('end Rosette.Bench','end Rosette.BenchR').replace('Rosette.Bench.run','Rosette.BenchR.run')
dedup='''
/-- REVIEW: interface with duplicate fvars removed (toggle with ROSETTE_NODEDUP). -/
def dedupArr (xs : Array Expr) : Array Expr := Id.run do
  let mut seen : Std.HashSet FVarId := {}
  let mut out := #[]
  for x in xs do
    if !seen.contains x.fvarId! then
      seen := seen.insert x.fvarId!
      out := out.push x
  return out

def interfaceOf (e ty : Expr) : MetaM Interface := do
  let ifc ← Rosette.interfaceOf e ty
  if (← IO.getEnv "ROSETTE_NODEDUP").isSome then return ifc
  return { deps := dedupArr ifc.deps, args := dedupArr ifc.args }
'''
src=src.replace('def tagKey : Name','%s\ndef tagKey : Name'%dedup,1)
insp=open('out/review_benchmark-validity/inspect_part.lean').read()
head,tail=src.split('end Rosette.BenchR')
tail=tail.replace('''  else
    IO.println "Rosette.Bench: set ROSETTE_BENCH=1 to run (see bench/run_bench.sh)"''','''  else if (← IO.getEnv "ROSETTE_INSPECT").isSome then
    Rosette.BenchR.inspectAll
  else
    IO.println "nothing"''')
open('out/review_benchmark-validity/BenchR.lean','w').write(head+insp+'\nend Rosette.BenchR'+tail)
