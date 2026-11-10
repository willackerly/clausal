/-
Statement keys for declaration-level recurrence in a built Lean project (written for
`corpora/ns`, Lean 4.34.0-rc2; imports only `Lean`, compiled stand-alone like
`corpora/ns_export/Export.lean`).

For every theorem that lives in a project module it prints one JSON line with these keys of the
theorem's TYPE (all are 64-bit structural hashes that ignore binder names, binder kinds, `mdata`
and universe levels):

* `kE`   exact.
* `kN`   numeric literals abstracted: every `@OfNat.ofNat T n inst` with `n` a raw literal becomes
         `NUM(T)` (the type is kept, the value and the instance are dropped); every other raw
         literal becomes `LIT`.
* `kL`   `kN`, and in addition every constant that stands, without arguments of its own, in an
         ARGUMENT position of an application is replaced by a numbered hole; holes are numbered in
         order of first occurrence, so the renaming is consistent (`f a a` and `f b b` agree,
         `f a b` differs).  This is "one level of leaf abstraction": types (`ℝ`), instances
         (`Real.instLE`) and named constants (`Real.pi`, a project-defined exponent) are leaves;
         heads of applications are kept.
* `kP`   `kN`, and in addition every constant DECLARED IN THE PROJECT is replaced by a numbered
         hole wherever it occurs, head positions included (consistent renaming again).  Two
         theorems agree on `kP` iff one is obtained from the other by renaming project
         definitions and changing numerals: the "same lemma for another object" pattern.  A head
         is a second-order parameter, so a common generalisation need not be provable.
* `kLP`  both abstractions.
* `pE`, `pN`, `pLP`  the same as `kE`, `kN`, `kLP` but invariant under reordering of binders:
         the telescope `∀ x₁ … xₙ, C` is opened; a binder is *floating* if its variable occurs in
         no other binder type and not in `C` (ordinary hypotheses, unused variables), otherwise
         it is a *data* binder.  Data variables are numbered by first occurrence in `C`, then in
         the types of already numbered variables, then in the floating binders (sorted by a
         provisional hash).  The key hashes `C`, the data binder types in that order and the
         SORTED multiset of floating binder types.  Equal keys imply equal statements up to
         binder order (the key is the hash of a rearranged statement); the numbering is a
         heuristic, so some permuted pairs can be missed.

* `svE`, `svN`, `svP`  JOINT keys of statement and proof term: exact; numerals abstracted; and
         project constants renamed consistently across statement AND proof, where every hole
         also carries the kind of the constant (theorem / definition / …) and the shape of ITS
         type (numerals abstracted, project constants anonymous).  Equal `svP` means: the two
         theorems are the same derivation from parallel ingredients, so the proof is a candidate
         for one lemma taking the renamed definitions as arguments and the renamed lemmas as
         hypotheses.  It is a candidate only: the kernel may have unfolded a renamed definition
         silently, and the hole annotation looks one level deep.

`holesL` / `holesP` / `holesSV` list the constants that were abstracted for `kL` / `kP` (first 24).

Usage: LEAN_PATH=... stmtkeys <modules.txt> <out.jsonl>
-/
import Lean
open Lean

namespace StmtKeys

def projectRoots : List Name := [`NavierStokes, `Euler, `ComparatorChallenges]

structure Opts where
  nums : Bool := false
  leaves : Bool := false
  proj : Bool := false

structure HS where
  memo : Std.HashMap Expr UInt64 := {}
  ren : Std.HashMap Name Nat := {}
  order : Array Name := #[]
  /-- numbering of opened binder variables -/
  fv : Std.HashMap FVarId Nat := {}

abbrev M := StateM HS

def tokNum : UInt64 := 1009
def tokLit : UInt64 := 1013
def tokHoleProv : UInt64 := 1019
def tokVarProv : UInt64 := 1021

structure Cx where
  o : Opts
  isProj : Name → Bool
  /-- final pass: holes and variables get numbers; provisional pass: one token each. -/
  final : Bool := true
  /-- extra data hashed into every numbered hole (used by the joint statement+proof key). -/
  annot : Name → UInt64 := fun _ => 0

def renameConst (cx : Cx) (n : Name) : M UInt64 := do
  if !cx.final then return tokHoleProv
  let s ← get
  match s.ren[n]? with
  | some i => return mixHash (mixHash 97 (hash i)) (cx.annot n)
  | none =>
    let i := s.order.size
    set { s with ren := s.ren.insert n i, order := s.order.push n }
    return mixHash (mixHash 97 (hash i)) (cx.annot n)

def isRawNat : Expr → Bool
  | .lit (.natVal _) => true
  | .mdata _ e => isRawNat e
  | _ => false

partial def hx (cx : Cx) (e : Expr) : M UInt64 := do
  match e with
  | .mdata _ b => hx cx b
  | .bvar i => return mixHash 31 (hash i)
  | .fvar id =>
    match (← get).fv[id]? with
    | some i => return mixHash 37 (hash i)
    | none => return tokVarProv
  | .mvar _ => return 41
  | .sort _ => return 43
  | .const n _ =>
    if cx.o.proj && cx.isProj n then renameConst cx n else return mixHash 47 (hash n)
  | .lit (.natVal n) => return if cx.o.nums then tokLit else mixHash 53 (hash n)
  | .lit (.strVal s) => return mixHash 59 (hash s)
  | _ =>
    if let some h := (← get).memo[e]? then return h
    let h ← match e with
      | .app .. => do
        let f := e.getAppFn
        let args := e.getAppArgs
        if cx.o.nums && f.isConstOf ``OfNat.ofNat && args.size == 3 && isRawNat args[1]! then
          pure (mixHash tokNum (← hx cx args[0]!))
        else
          let mut h := mixHash 61 (mixHash (← hx cx f) (hash args.size))
          for a in args do
            let ha ← match a.consumeMData with
              | .const n _ =>
                if cx.o.leaves || (cx.o.proj && cx.isProj n) then renameConst cx n
                else pure (mixHash 47 (hash n))
              | a' => hx cx a'
            h := mixHash h ha
          pure h
      | .lam _ t b _ => do pure (mixHash 67 (mixHash (← hx cx t) (← hx cx b)))
      | .forallE _ t b _ => do pure (mixHash 71 (mixHash (← hx cx t) (← hx cx b)))
      | .letE _ t v b _ => do
        pure (mixHash 73 (mixHash (← hx cx t) (mixHash (← hx cx v) (← hx cx b))))
      | .proj s i b => do pure (mixHash 79 (mixHash (hash s) (mixHash (hash i) (← hx cx b))))
      | _ => pure 0
    modify fun s => { s with memo := s.memo.insert e h }
    return h

/-- plain key of a closed statement and the abstracted constants. -/
def plainKey (o : Opts) (isProj : Name → Bool) (e : Expr) : UInt64 × Array Name :=
  let (h, s) := (hx { o, isProj } e).run {}
  (h, s.order)

/-- joint key of statement and proof term (one renaming for both), and the abstracted constants. -/
def jointKey (o : Opts) (isProj : Name → Bool) (annot : Name → UInt64) (ty val : Expr) :
    UInt64 × Array Name :=
  let cx : Cx := { o, isProj, annot }
  let (h, s) := (do let a ← hx cx ty; let b ← hx cx val; pure (mixHash a b) : M UInt64).run {}
  (h, s.order)

/-- free variables of `e` in order of first occurrence (pre-order, function before arguments). -/
partial def fvarOrder (e : Expr) : StateM (Std.HashSet Expr × Array FVarId) Unit := do
  if !e.hasFVar then return
  match e with
  | .fvar id =>
    let (seen, out) ← get
    unless out.contains id do set (seen, out.push id)
  | _ =>
    if (← get).1.contains e then return
    modify fun (seen, out) => (seen.insert e, out)
    match e with
    | .app f a => fvarOrder f; fvarOrder a
    | .lam _ t b _ | .forallE _ t b _ => fvarOrder t; fvarOrder b
    | .letE _ t v b _ => fvarOrder t; fvarOrder v; fvarOrder b
    | .mdata _ b | .proj _ _ b => fvarOrder b
    | _ => pure ()

def fvarsOf (e : Expr) : Array FVarId := ((fvarOrder e).run ({}, #[])).2.2

/-- binder-order-invariant key; also returns (#binders, #floating). -/
def permKey (o : Opts) (isProj : Name → Bool) (ty : Expr) : UInt64 × Nat × Nat := Id.run do
  -- open the telescope
  let mut tys : Array Expr := #[]
  let mut fvs : Array Expr := #[]
  let mut e := ty
  let mut i := 0
  repeat
    match e with
    | .mdata _ b => e := b
    | .forallE _ t b _ =>
      tys := tys.push (t.instantiateRev fvs)
      fvs := fvs.push (.fvar ⟨Name.mkNum `v i⟩)
      i := i + 1
      e := b
    | _ => break
  let concl := e.instantiateRev fvs
  let n := tys.size
  let idx (id : FVarId) : Nat := match id.name with | .num _ k => k | _ => 0
  -- occurrence sets
  let occT := tys.map fvarsOf
  let occC := fvarsOf concl
  let mut used : Array Bool := Array.replicate n false
  for id in occC do used := used.set! (idx id) true
  for j in [0:n] do
    for id in occT[j]! do used := used.set! (idx id) true
  let floating := (List.range n).filter fun j => !used[j]!
  -- number data variables
  let mut order : Array Nat := #[]
  let mut numbered : Array Bool := Array.replicate n false
  let mut q := 0
  for id in occC do
    let j := idx id
    unless numbered[j]! do
      numbered := numbered.set! j true; order := order.push j
  while q < order.size do
    for id in occT[order[q]!]! do
      let j := idx id
      unless numbered[j]! do
        numbered := numbered.set! j true; order := order.push j
    q := q + 1
  -- provisional hashes of floating binders (numbered variables so far, others one token)
  let mkFv (ord : Array Nat) : Std.HashMap FVarId Nat := Id.run do
    let mut m : Std.HashMap FVarId Nat := {}
    for k in [0:ord.size] do m := m.insert ⟨Name.mkNum `v ord[k]!⟩ k
    return m
  let cxP : Cx := { o, isProj, final := false }
  let mut prov : Array (UInt64 × Nat) := #[]
  let mut st : HS := { fv := mkFv order }
  for j in floating do
    let (h, s) := (hx cxP tys[j]!).run st
    st := s
    prov := prov.push (h, j)
  prov := prov.qsort fun a b => a.1 < b.1 || (a.1 == b.1 && a.2 < b.2)
  for (_, j) in prov do
    for id in occT[j]! do
      let k := idx id
      unless numbered[k]! do
        numbered := numbered.set! k true; order := order.push k
  while q < order.size do
    for id in occT[order[q]!]! do
      let j := idx id
      unless numbered[j]! do
        numbered := numbered.set! j true; order := order.push j
    q := q + 1
  for j in [0:n] do
    if used[j]! && !numbered[j]! then
      numbered := numbered.set! j true; order := order.push j
  -- final pass
  let cx : Cx := { o, isProj }
  let mut s : HS := { fv := mkFv order }
  let (hc, s1) := (hx cx concl).run s
  s := s1
  let mut key := mixHash 101 hc
  for j in order do
    let (h, s1) := (hx cx tys[j]!).run s
    s := s1
    key := mixHash key h
  let mut fl : Array UInt64 := #[]
  for (_, j) in prov do
    let (h, s1) := (hx cx tys[j]!).run s
    s := s1
    fl := fl.push h
  for h in fl.qsort (· < ·) do key := mixHash key (mixHash 103 h)
  return (key, n, floating.length)

def hex64 (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

unsafe def main (args : List String) : IO UInt32 := do
  let [modsFile, outFile] := args
    | throw <| IO.userError "usage: stmtkeys modules.txt out.jsonl"
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024)
    (loadExts := false)
  let projIdx : Array Bool := env.header.moduleNames.map fun m => projectRoots.contains m.getRoot
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  -- annotation of a project constant: its kind and the shape of its type (numerals abstracted,
  -- project constants one anonymous token)
  let mut annotMap : Std.HashMap Name UInt64 := {}
  for (n, ci) in env.constants.map₁.toList do
    if isProj n then
      let kind : UInt64 := match ci with
        | .thmInfo _ => 1 | .defnInfo _ => 2 | .ctorInfo _ => 3 | .inductInfo _ => 4
        | .recInfo _ => 5 | .opaqueInfo _ => 6 | _ => 7
      let (ht, _) := (hx { o := { nums := true, proj := true }, isProj, final := false } ci.type).run {}
      annotMap := annotMap.insert n (mixHash kind ht)
  let annot (n : Name) : UInt64 := annotMap.getD n 0
  let isThm (n : Name) : Bool := match env.find? n with | some (.thmInfo _) => true | _ => false
  let h ← IO.FS.Handle.mk outFile .write
  let mut cnt := 0
  for (n, ci) in env.constants.map₁.toList do
    let .thmInfo t := ci | continue
    unless isProj n do continue
    let ty := t.type
    let (kE, _) := plainKey {} isProj ty
    let (kN, _) := plainKey { nums := true } isProj ty
    let (kL, hl) := plainKey { nums := true, leaves := true } isProj ty
    let (kP, hp) := plainKey { nums := true, proj := true } isProj ty
    let (kLP, _) := plainKey { nums := true, leaves := true, proj := true } isProj ty
    let (pE, nb, nf) := permKey {} isProj ty
    let (pN, _, _) := permKey { nums := true } isProj ty
    let (pLP, _, _) := permKey { nums := true, leaves := true, proj := true } isProj ty
    let (svE, _) := jointKey {} isProj (fun _ => 0) ty t.value
    let (svN, _) := jointKey { nums := true } isProj (fun _ => 0) ty t.value
    let (svP, hsv) := jointKey { nums := true, proj := true } isProj annot ty t.value
    h.putStrLn (Json.mkObj [("svE", hex64 svE), ("svN", hex64 svN), ("svP", hex64 svP),
      ("holesSV", toJson ((hsv.extract 0 40).map (·.toString))), ("numHolesSV", hsv.size),
      ("numHolesSVThm", (hsv.filter isThm).size),
      ("name", n.toString), ("kE", hex64 kE), ("kN", hex64 kN),
      ("kL", hex64 kL), ("kP", hex64 kP), ("kLP", hex64 kLP), ("pE", hex64 pE),
      ("pN", hex64 pN), ("pLP", hex64 pLP), ("binders", nb), ("floating", nf),
      ("holesL", toJson ((hl.extract 0 24).map (·.toString))),
      ("holesP", toJson ((hp.extract 0 24).map (·.toString))),
      ("numHolesL", hl.size), ("numHolesP", hp.size)]).compress
    cnt := cnt + 1
  h.flush
  IO.eprintln s!"wrote {cnt} theorems"
  return 0

end StmtKeys

unsafe def main (args : List String) : IO UInt32 := StmtKeys.main args
