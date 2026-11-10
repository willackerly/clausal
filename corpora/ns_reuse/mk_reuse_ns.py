#!/usr/bin/env python3
"""Assemble ReuseNS.lean (Lean 4.34, corpus corpora/ns) from the root project's
Rosette/Candidates.lean and Rosette/Reuse.lean WITHOUT editing the originals.

    python3 mk_reuse_ns.py <imports.txt> > ReuseNS.lean

Changes relative to the originals (everything else is copied verbatim):
  * one file; imports = Mathlib + the project modules listed in imports.txt;
  * the theorems to enumerate are read from a file (ROSETTE_REUSE_DECLS, lines "<slice>\\t<name>")
    instead of being selected by Mathlib module prefix; no to_additive filter;
  * the library lookup table is split: `inLib` / `inLibL1` = theorems outside the project
    (Mathlib, Batteries, core), `inProj` / `inProjL1` = named (not auto-generated) theorems of the
    project; `exact?` still runs on statements with a project hash match (it searches the whole
    environment, project lemmas included);
  * `exactLemmaProj` says whether the lemma `exact?` found is a project declaration;
  * the traversal is DAG-aware: a subterm met again inside one theorem (same term, same local
    variables) is not walked again; if it is a candidate, an alias row records the extra position;
  * ROSETTE_REUSE_NOLGG skips the anti-unifier pass; ROSETTE_REUSE_EXACTMODE turns the probe
    driver into an `exact?` driver for the keys it is given (writes exact.jsonl).
"""
import sys, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
cand = (root / "Rosette/Candidates.lean").read_text()
reuse = (root / "Rosette/Reuse.lean").read_text()
imports = [l.strip() for l in open(sys.argv[1]) if l.strip()]

# --- Candidates: body between the import line and the JSON section
a = cand.index("open Lean Meta Elab Command")
b = cand.index("/-! ### JSON -/")
cand_body = cand[a:b] + "\nend Rosette\n"

# --- Reuse: from `open Lean Meta` on
a = reuse.index("open Lean Meta\n\nnamespace Rosette.Reuse")
body = reuse[a:]

def rep(old, new, count=1):
    global body
    assert body.count(old) >= 1, old[:60]
    body = body.replace(old, new) if count == 0 else body.replace(old, new, count)

s0 = body.index("  let modNames := env.header.moduleNames\n  let addImages")
s1 = body.index("  -- 3. enumerate")
new_sel = r'''  let modNames := env.header.moduleNames
  let projIdx : Array Bool := modNames.map fun m => m.getRoot == `NavierStokes || m.getRoot == `Euler
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  let wantedFile := (← IO.getEnv "ROSETTE_REUSE_DECLS").getD (outDir / "sample.txt").toString
  let mut wanted : Std.HashMap String String := {}
  for l in (← IO.FS.lines wantedFile) do
    match l.splitOn "\t" with
    | [s, n] => wanted := wanted.insert n s
    | _ => pure ()
  let mut sel : Array (String × Name × Name × Nat) := #[]
  let mut libE : Std.HashMap UInt64 (Array Name) := {}
  let mut libL1 : Std.HashMap UInt64 (Array Name) := {}
  let mut projE : Std.HashMap UInt64 (Array Name) := {}
  let mut projL1 : Std.HashMap UInt64 (Array Name) := {}
  let mut instCache : Std.HashMap Name (Array Bool) := {}
  let mut nLib := 0
  let mut nProjLib := 0
  for (n, ci) in env.constants.map₁.toList do
    let .thmInfo t := ci | continue
    let auto := isAutoName n
    let he := statementHash t.type
    let (h1, s) := (gHash env none t.type 0).run { inst := instCache }
    instCache := s.inst
    let put (m : Std.HashMap UInt64 (Array Name)) (h : UInt64) :=
      let cur := m.getD h #[]
      if cur.size ≥ 3 then m else m.insert h (if auto then cur.push n else #[n] ++ cur)
    if isProj n then
      unless auto do
        nProjLib := nProjLib + 1
        projE := put projE he
        projL1 := put projL1 h1
    else
      nLib := nLib + 1
      libE := put libE he
      libL1 := put libL1 h1
    if let some sl := wanted[n.toString]? then
      let some idx := env.getModuleIdxFor? n | continue
      sel := sel.push (sl, n, modNames[idx.toNat]!, dagSize t.value)
  IO.println s!"library theorems hashed: {nLib} outside the project, {nProjLib} named project theorems"
  let decls := sel.qsort fun a b => a.2.1.toString < b.2.1.toString
  let mut selCounts : Array Json := #[]
  for lab in (decls.foldl (fun (acc : Array String) d => if acc.contains d.1 then acc else acc.push d.1) #[]) do
    let k := (decls.filter (·.1 == lab)).size
    selCounts := selCounts.push <| Json.mkObj [("slice", lab), ("eligible", k), ("used", k)]
  IO.println s!"theorems requested: {wanted.size}, found: {decls.size}"
'''
body = body[:s0] + new_sel + body[s1:]
rep('''      ("inLib", names libE sh), ("inLibL1", names libL1 h1),
      ("exact", ex), ("exactLemma", optName exLemma), ("exactNote", exMsg)]).compress''',
    '''      ("inLib", names libE sh), ("inLibL1", names libL1 h1),
      ("inProj", names projE sh), ("inProjL1", names projL1 h1),
      ("exact", ex), ("exactLemma", optName exLemma),
      ("exactLemmaProj", match exLemma with | some l => isProj l | none => false),
      ("exactNote", exMsg)]).compress''')
rep('("minTheoremProof", minThm), ("maxDeclsPerSlice", maxDecls), ', '')
rep('("libraryTheoremsHashed", nLib),', '("libraryTheoremsHashed", nLib), ("projectTheoremsHashed", nProjLib),')
rep('  let minThm ← envNat "ROSETTE_REUSE_MINPROOF" 800\n  let maxDecls ← envNat "ROSETTE_REUSE_MAXDECLS" 0\n', '')
rep("def interfaceDedup (e ty : Expr) : MetaM Interface := Rosette.interfaceOf e ty",
    "def interfaceDedup (e ty : Expr) : MetaM Rosette.Interface := Rosette.interfaceOf e ty")
# --- DAG-aware traversal (the tree walk of the original explodes on machine-generated terms:
# a third of the sampled theorems hit maxVisited = 300000 with proof DAG sizes of 1-3 thousand)
rep("""  sizes : Std.HashMap Expr Nat := {}
  /-- distinct exact statements seen so far (global across declarations). -/""",
    """  sizes : Std.HashMap Expr Nat := {}
  /-- subterms already walked in the current declaration ↦ the candidate recorded for them. -/
  seen : Std.HashMap Expr (Option Nat) := {}
  /-- distinct exact statements seen so far (global across declarations). -/""")
rep("""  let mut parent := parent
  unless e.isMData do
    parent ← record e parent role ts
""", """  let mut parent := parent
  unless e.isMData do
    if let some c? := s.seen[e]? then
      -- same subterm (same local variables) at another tree position: it would give the same
      -- candidate and the same nested candidates. Record the position of the candidate itself
      -- (an alias row with the new parent) and do not descend again.
      if let some id := c? then
        modify fun s =>
          match s.cands[id]? with
          | some c => { s with cands := s.cands.push { c with id := s.cands.size, parent := parent, role := role } }
          | none => s
      return
    let before := (← get).cands.size
    parent ← record e parent role ts
    let after := (← get).cands.size
    modify fun s => { s with seen := s.seen.insert e (if after > before then some before else none) }
""")
rep("""truncated := false,
                                 note := "", sizes := {} }""", """truncated := false,
                                 note := "", sizes := {}, seen := {} }""", 0)
# --- optional: skip the anti-unifier pass (meaningless inside one shard)
rep("""  for (level, agg) in [("L1", aggL1), ("L2", aggL2)] do""",
    """  for (level, agg) in (if (← IO.getEnv "ROSETTE_REUSE_NOLGG").isSome then [] else [("L1", aggL1), ("L2", aggL2)]) do""")
# --- second-pass driver: `exact?` on given keys (ROSETTE_REUSE_EXACTKEYS) or the one-tactic probe
rep("""  let tacs ← probeTactics
  let h ← IO.FS.Handle.mk (outDir / "probe.jsonl") .write""",
    """  if (← IO.getEnv "ROSETTE_REUSE_EXACTMODE").isSome then
    let env ← getEnv
    let modNames := env.header.moduleNames
    let isProj (n : Name) : Bool :=
      match env.getModuleIdxFor? n with
      | some i => let r := modNames[i.toNat]!.getRoot; r == `NavierStokes || r == `Euler
      | none => false
    let h ← IO.FS.Handle.mk (outDir / "exact.jsonl") .write
    let t0 ← IO.monoMsNow
    for sh in wantedH.toArray.qsort (· < ·) do
      let some (stmt, _) := st.stmts[sh]? | continue
      let (ex, exLemma, exMsg) ← tryExact stmt probeBudgetK
      h.putStrLn (Json.mkObj [("stmtHash", hex64 sh), ("exact", ex), ("exactLemma", optName exLemma),
        ("exactLemmaProj", match exLemma with | some l => isProj l | none => false),
        ("exactNote", exMsg)]).compress
      h.flush
    IO.println s!"exact?: {wantedH.size} statements, {((← IO.monoMsNow) - t0) / 1000}s"
    return
  let tacs ← probeTactics
  let h ← IO.FS.Handle.mk (outDir / "probe.jsonl") .write""")
# the slices table is unused here
s0 = body.index("/-! ## Slices -/"); s1 = body.index("/-! ## Name filter")
body = body[:s0] + body[s1:]

print("-- GENERATED by mk_reuse_ns.py from Rosette/Candidates.lean and Rosette/Reuse.lean; do not edit.")
print("import Mathlib")
for m in imports:
    print("import " + m)
print()
print(cand_body)
print(body)
