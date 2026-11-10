import Mathlib

/-!
# Rosette.Corpus — ground-truth corpus for the lemma-boundary-recovery benchmark

A ground-truth item is a pair `(T, L)` where `T` is a Mathlib theorem and `L` is a helper
lemma that a human chose to factor out of `T`'s proof.  Everything here is computed from the
elaborated Mathlib environment (no source regexes, no hand-written data).

Criteria (all must hold; the constants are in `Params` below):

* `L` and `T` are both `theorem`s (`ConstantInfo.thmInfo`, so their statements are `Prop`s),
  declared in the same `Mathlib.*` module, `L ≠ T`;
* neither is auto-generated (see `isAutoName`, `isInstanceCore`, `to_additive` images);
* `T`'s own proof term references `L` directly;
* `L` is used by at most `maxUsers` (= 2) *declarations* in the whole environment, where
  a declaration is a constant name with its compiler-generated suffixes stripped (`rootOf`),
  and uses by `L` itself do not count;
* `L`'s proof is non-trivial: DAG size of its proof term `≥ minHelperProof`;
* `T`'s proof term has DAG size `≥ minTheoremProof` (so `T` is not a bare alias of `L`).

Signals of helper-hood recorded per item: `private` (the helper is a `private theorem`),
`aux` (an `_`-separated token of the helper's last name component starts with "aux", or the
last component is `aux…`: `foo_aux`, `foo_aux₁`, `aux_foo`, `Foo.aux`), `prefix` (the helper's
name strictly extends the theorem's name: `T_aux`, `T'`, `T_of_foo`) and `sole_use` (the
theorem is the helper's only user).  An item needs a *strong* signal (`private` or `aux`) to
enter the corpus; `prefix` and `sole_use` are recorded but do not qualify on their own
(prefix-only pairs are mostly named variants such as `foo'` / `foo_iff`, not proof-specific
helpers).

Run (from the project root, about 7 minutes):

    ROSETTE_CORPUS=1 lake env lean Rosette/Corpus.lean

which writes `bench/corpus.json` and prints the statistics block that `bench/CORPUS.md`
quotes (also written to `$ROSETTE_CORPUS_STATS` if set).  The full uncapped list of
(theorem, helper) pairs goes to `$ROSETTE_CORPUS_RAW` (JSON lines) if set.
-/

open Lean Meta

namespace Rosette.Corpus

structure Params where
  /-- Helper is used by at most this many declarations. -/
  maxUsers : Nat := 2
  /-- Minimum DAG size of the helper's proof term. -/
  minHelperProof : Nat := 150
  /-- Minimum DAG size of the theorem's proof term. -/
  minTheoremProof : Nat := 50
  /-- Maximum number of corpus items per module. -/
  moduleCap : Nat := 1
  /-- Maximum number of corpus items per top-level area (`Mathlib.<Area>`). -/
  areaCap : Nat := 20
  /-- Number of sampled items printed with statements. -/
  nSample : Nat := 10

/-! ## Name classification -/

/-- Last-component names produced by Lean / Mathlib machinery rather than by a human. -/
def generatedSuffixes : List String :=
  ["eq_def", "eq_unfold", "congr_simp", "sizeOf_spec", "injEq", "inj", "noConfusion",
   "noConfusionType", "rec", "recOn", "casesOn", "brecOn", "binductionOn", "below", "ibelow",
   "ctorIdx", "induct", "induct_unfolding", "fun_cases", "fun_cases_unfolding", "elim",
   "ext_iff", "mk_inj", "mk_injEq", "ofNat_ctorIdx", "toCtorIdx", "ind", "omega_nat"]

def isGeneratedComp (s : String) : Bool :=
  s.startsWith "_" || s.startsWith "match_" || s.startsWith "proof_" ||
  s.startsWith "hcongr_" || s.startsWith "inst" ||
  (s.startsWith "eq_" && (s.drop 3).all Char.isDigit && s.length > 3) ||
  generatedSuffixes.contains s

/-- `true` if the (user-facing part of the) name looks auto-generated. -/
def isAutoName (n : Name) : Bool :=
  let u := privateToUserName n
  u.isAnonymous || go u
where
  go : Name → Bool
    | .anonymous => false
    | .num _ _ => true
    | .str p s => isGeneratedComp s || go p

/-- Strip compiler-generated suffixes: `Foo.bar._proof_3 ↦ Foo.bar`, `Foo.bar.match_1 ↦ Foo.bar`,
`Foo.bar._auxLemma.2 ↦ Foo.bar`.  The numeric component of a private prefix is kept. -/
partial def rootOf : Name → Name
  | n@(.str p s) =>
    if s.startsWith "_" && !p.isAnonymous && !(n == `_private) && !isPrivatePrefixHead n then rootOf p
    else if s.startsWith "match_" || s.startsWith "proof_" then rootOf p
    else if s.startsWith "eq_" && s.length > 3 && (s.drop 3).all Char.isDigit then rootOf p
    else n
  | n@(.num p _) =>
    match p with
    | .str _ s => if s.startsWith "_" then rootOf p else n
    | _ => n
  | .anonymous => .anonymous
where
  isPrivatePrefixHead : Name → Bool
    | .str .anonymous "_private" => true
    | _ => false

/-! ## Term sizes -/

/-- Returns `(dagSize, treeSize)` of an expression: the number of distinct subterms (shared
subterms counted once, up to structural equality) and the number of nodes of the unfolded tree. -/
partial def sizes (e : Expr) : Nat × Nat :=
  let (t, m) := (go e).run {}
  (m.size, t)
where
  go (e : Expr) : StateM (Std.HashMap Expr Nat) Nat := do
    if let some n := (← get)[e]? then return n
    let n ← match e with
      | .app f a => do pure (1 + (← go f) + (← go a))
      | .lam _ t b _ => do pure (1 + (← go t) + (← go b))
      | .forallE _ t b _ => do pure (1 + (← go t) + (← go b))
      | .letE _ t v b _ => do pure (1 + (← go t) + (← go v) + (← go b))
      | .mdata _ b => do pure (1 + (← go b))
      | .proj _ _ b => do pure (1 + (← go b))
      | _ => pure 1
    modify (·.insert e n)
    return n

/-! ## The scan -/

structure Item where
  thm : Name
  helper : Name
  module : Name
  helperProofSize : Nat
  helperProofTreeSize : Nat
  helperStatementSize : Nat
  theoremProofSize : Nat
  helperUseCount : Nat
  isPrivate : Bool
  isAux : Bool
  isPrefix : Bool
  soleUse : Bool
  deriving Inhabited

/-- Canonical order: module, helper, theorem. -/
def Item.key (i : Item) : String :=
  s!"{i.module}|{i.helper}|{i.thm}"


/-- Qualifying signal: private helper or aux-named helper. -/
def Item.strong (i : Item) : Bool := i.isPrivate || i.isAux

/-- Number of name-based signals, used only to rank items inside one module. -/
def Item.strength (i : Item) : Nat :=
  (if i.isPrivate then 1 else 0) + (if i.isAux then 1 else 0) + (if i.isPrefix then 1 else 0)

def Item.signal (i : Item) : String :=
  let l := (if i.isPrivate then ["private"] else []) ++ (if i.isAux then ["aux"] else []) ++
    (if i.isPrefix then ["prefix"] else []) ++ (if i.soleUse then ["sole_use"] else [])
  if l.isEmpty then "none" else "+".intercalate l

def Item.area (i : Item) : String :=
  match i.module.components with
  | _ :: a :: _ => a.toString
  | _ => "?"

def showName (n : Name) : String := (privateToUserName n).toString

def Item.toJson (i : Item) : Json :=
  Json.mkObj [
    ("theorem", showName i.thm),
    ("helper", showName i.helper),
    ("module", i.module.toString),
    ("area", i.area),
    ("helperProofSize", i.helperProofSize),
    ("theoremProofSize", i.theoremProofSize),
    ("helperUseCount", i.helperUseCount),
    ("signal", i.signal),
    ("helperProofTreeSize", i.helperProofTreeSize),
    ("helperStatementSize", i.helperStatementSize),
    ("helperIsPrivate", i.isPrivate),
    ("theoremFullName", i.thm.toString),
    ("helperFullName", i.helper.toString)]

/-- `foo_aux`, `foo_aux₁`, `aux_foo`, `Foo.aux`, `foo_auxiliary`; but not `fooAux_bar`, which is
a lemma *about* an auxiliary definition `fooAux`. -/
def containsAux (n : Name) : Bool :=
  match privateToUserName n with
  | .str _ s => (s.toLower.splitOn "_").any (·.startsWith "aux")
  | _ => false

def isPrefixSignal (thm helper : Name) : Bool :=
  let t := (privateToUserName thm).toString
  let h := (privateToUserName helper).toString
  t.length < h.length && h.startsWith t

def pct (xs : Array Nat) (p : Nat) : Nat :=
  if xs.isEmpty then 0 else
    let s := xs.qsort (· < ·)
    s[(s.size - 1) * p / 100]!

def run (P : Params := {}) : MetaM Unit := do
  let env ← getEnv
  let modNames := env.header.moduleNames
  let out : IO.Ref (Array String) ← IO.mkRef #[]
  let say (s : String) : MetaM Unit := do out.modify (·.push s); IO.println s
  -- to_additive images are machine-generated copies
  let addImages : NameSet :=
    (Mathlib.Tactic.ToAdditive.translations.getState env).get.foldl
      (fun s src info => if info.translation == src then s else s.insert info.translation) {}
  let mathlibMod (n : Name) : Option Name := do
    let idx ← env.getModuleIdxFor? n
    let m := modNames[idx.toNat]!
    if m.getRoot == `Mathlib then some m else none
  let okDecl (n : Name) : Bool :=
    !isAutoName n && !addImages.contains n && !Meta.isInstanceCore env n
  -- Pass 0: candidate helpers = human-written theorems in Mathlib modules
  let mut cand : Std.HashMap Name (Array Name) := {}
  let mut nConst := 0
  let mut nThm := 0
  for (n, ci) in env.constants.map₁ do
    nConst := nConst + 1
    if let .thmInfo _ := ci then
      if (mathlibMod n).isSome then
        nThm := nThm + 1
        if okDecl n then cand := cand.insert n #[]
  say s!"- constants in environment: {nConst}"
  say s!"- theorems in `Mathlib.*` modules: {nThm}"
  say s!"- of which human-written by name (not auto-generated, not a `to_additive` image, not an instance): {cand.size}"
  -- Pass 1: reverse usage (distinct user declarations, capped at maxUsers+1)
  for (n, ci) in env.constants.map₁ do
    let r := rootOf n
    let mut used := ci.type.getUsedConstantsAsSet
    if let some v := ci.value? (allowOpaque := true) then
      used := v.getUsedConstantsAsSet.foldl (·.insert ·) used
    for u in used do
      if u != r then
        if let some us := cand[u]? then
          if us.size ≤ P.maxUsers && !us.contains r && rootOf u != r then
            cand := cand.insert u (us.push r)
  let mut nUnused := 0
  let mut nFew := 0
  for (_, us) in cand do
    if us.size == 0 then nUnused := nUnused + 1
    else if us.size ≤ P.maxUsers then nFew := nFew + 1
  say s!"- of those, used by no other declaration: {nUnused}; used by 1..{P.maxUsers} declarations: {nFew}; used by more: {cand.size - nUnused - nFew}"
  -- Pass 2: pair each rarely-used helper with its same-module theorem users
  let mut raw : Array Item := #[]
  let mut nPairs := 0
  for (h, us) in cand do
    if us.size == 0 || us.size > P.maxUsers then continue
    let some hm := mathlibMod h | continue
    let some hci := env.find? h | continue
    let some hv := hci.value? (allowOpaque := true) | continue
    let mut hsz : Option (Nat × Nat × Nat) := none
    for t in us do
      let some (.thmInfo tci) := env.find? t | continue
      unless mathlibMod t == some hm do continue
      unless okDecl t do continue
      unless tci.value.getUsedConstantsAsSet.contains h do continue
      nPairs := nPairs + 1
      let (hd, ht, hs) ← match hsz with
        | some x => pure x
        | none =>
          let (d, tr) := sizes hv
          let x := (d, tr, (sizes hci.type).1)
          hsz := some x
          pure x
      raw := raw.push {
        thm := t, helper := h, module := hm
        helperProofSize := hd, helperProofTreeSize := ht, helperStatementSize := hs
        theoremProofSize := (sizes tci.value).1
        helperUseCount := us.size
        isPrivate := isPrivateName h
        isAux := containsAux h
        isPrefix := isPrefixSignal t h
        soleUse := us.size == 1 }
  raw := raw.qsort (fun a b => a.key < b.key)
  say s!"- (theorem, helper) pairs: same module, theorem's proof term references helper directly, helper used by ≤ {P.maxUsers} declarations: {nPairs}"
  let hs := raw.map (·.helperProofSize)
  say s!"- helper proof DAG size over those pairs: p10={pct hs 10}, p25={pct hs 25}, median={pct hs 50}, p75={pct hs 75}, p90={pct hs 90}"
  let strong := raw.filter (·.strong)
  let hs2 := strong.map (·.helperProofSize)
  say s!"- pairs with a strong signal (private or aux): {strong.size}  (private: {(raw.filter (·.isPrivate)).size}, aux: {(raw.filter (·.isAux)).size}, both: {(raw.filter fun i => i.isPrivate && i.isAux).size})"
  say s!"- pairs with no strong signal (excluded): {raw.size - strong.size}, of which prefix-only: {(raw.filter fun i => !i.strong && i.isPrefix).size}"
  say s!"- helper proof DAG size over strong-signal pairs: p10={pct hs2 10}, p25={pct hs2 25}, median={pct hs2 50}, p75={pct hs2 75}, p90={pct hs2 90}"
  if let some path ← IO.getEnv "ROSETTE_CORPUS_RAW" then
    IO.FS.writeFile path ("\n".intercalate (raw.map (·.toJson.compress)).toList ++ "\n")
  -- Thresholds
  let elig := strong.filter fun i =>
    i.helperProofSize ≥ P.minHelperProof && i.theoremProofSize ≥ P.minTheoremProof
  say s!"- eligible pairs (strong signal, helper proof ≥ {P.minHelperProof}, theorem proof ≥ {P.minTheoremProof}): {elig.size}, in {(elig.foldl (fun (s : NameSet) i => s.insert i.module) {}).size} modules"
  -- Caps: within a module keep the items with most name signals (ties: hash of helper name,
  -- so neither size nor alphabet decides); then per area, keep modules in a deterministic
  -- pseudo-random order (hash of module name).
  let pad (n : UInt64) : String := String.ofList (Nat.toDigits 10 (n.toNat + 10 ^ 20))
  let rk (i : Item) : String :=
    s!"{i.module}|{9 - i.strength}|{pad (hash (showName i.helper))}|{i.helper}|{i.thm}"
  let ranked := elig.qsort fun a b => rk a < rk b
  let mut perMod : Std.HashMap Name Nat := {}
  let mut afterMod : Array Item := #[]
  let mut dropMod : Std.HashMap String Nat := {}
  for i in ranked do
    let c := perMod.getD i.module 0
    if c < P.moduleCap then
      perMod := perMod.insert i.module (c + 1)
      afterMod := afterMod.push i
    else
      dropMod := dropMod.insert i.area (dropMod.getD i.area 0 + 1)
  let shuffled := afterMod.qsort fun a b =>
    let ha := hash a.module.toString
    let hb := hash b.module.toString
    ha < hb || (ha == hb && a.key < b.key)
  let mut perArea : Std.HashMap String Nat := {}
  let mut sel : Array Item := #[]
  let mut dropArea : Std.HashMap String Nat := {}
  for i in shuffled do
    let c := perArea.getD i.area 0
    if c < P.areaCap then
      perArea := perArea.insert i.area (c + 1)
      sel := sel.push i
    else
      dropArea := dropArea.insert i.area (dropArea.getD i.area 0 + 1)
  sel := sel.qsort fun a b => a.key < b.key
  say s!"- after module cap ({P.moduleCap} per module): {afterMod.size} (dropped {elig.size - afterMod.size})"
  say s!"- after area cap ({P.areaCap} per area): {sel.size} (dropped {afterMod.size - sel.size})"
  say s!"- **corpus size: {sel.size} items, {(sel.foldl (fun (s : NameSet) i => s.insert i.module) {}).size} modules, {perArea.size} areas, {(sel.foldl (fun (s : NameSet) i => s.insert i.helper) {}).size} distinct helpers, {(sel.foldl (fun (s : NameSet) i => s.insert i.thm) {}).size} distinct theorems**"
  let shs := sel.map (·.helperProofSize)
  let sts := sel.map (·.theoremProofSize)
  let sss := sel.map (·.helperStatementSize)
  say s!"- corpus helper proof DAG size: min={pct shs 0}, p25={pct shs 25}, median={pct shs 50}, p75={pct shs 75}, max={pct shs 100}"
  say s!"- corpus helper statement DAG size: min={pct sss 0}, p25={pct sss 25}, median={pct sss 50}, p75={pct sss 75}, max={pct sss 100}"
  say s!"- corpus theorem proof DAG size: min={pct sts 0}, p25={pct sts 25}, median={pct sts 50}, p75={pct sts 75}, max={pct sts 100}"
  say s!"- corpus helperUseCount: 1 → {(sel.filter (·.helperUseCount == 1)).size}, 2 → {(sel.filter (·.helperUseCount == 2)).size}"
  say ""
  say "SIGNALS"
  say ""
  say "| signal | eligible | corpus |"
  say "|---|---:|---:|"
  let sigs := (elig.foldl (fun (m : Std.HashMap String Nat) i => m.insert i.signal (m.getD i.signal 0 + 1)) {})
  for (s, c) in sigs.toArray.qsort (fun a b => a.1 < b.1) do
    say s!"| `{s}` | {c} | {(sel.filter (·.signal == s)).size} |"
  say ""
  say "AREAS"
  say ""
  say "| area | eligible pairs | dropped by module cap | dropped by area cap | corpus items |"
  say "|---|---:|---:|---:|---:|"
  let areas := (elig.foldl (fun (m : Std.HashMap String Nat) i => m.insert i.area (m.getD i.area 0 + 1)) {})
  for (a, c) in areas.toArray.qsort (fun a b => a.1 < b.1) do
    say s!"| {a} | {c} | {dropMod.getD a 0} | {dropArea.getD a 0} | {perArea.getD a 0} |"
  say ""
  say "SAMPLE"
  say ""
  for k in [0:P.nSample] do
    if sel.isEmpty then break
    let i := sel[(2 * k + 1) * sel.size / (2 * P.nSample)]!
    let some hci := env.find? i.helper | continue
    let some tci := env.find? i.thm | continue
    let fmtH ← ppExpr hci.type
    let fmtT ← ppExpr tci.type
    say s!"### {k + 1}. `{showName i.helper}` used in `{showName i.thm}`"
    say ""
    say s!"- module `{i.module}`; signal `{i.signal}`; helper proof size {i.helperProofSize} (tree {i.helperProofTreeSize}); helper statement size {i.helperStatementSize}; theorem proof size {i.theoremProofSize}; helper use count {i.helperUseCount}"
    say ""
    say s!"Helper statement:\n\n```lean\n{fmtH.pretty 100}\n```\n"
    say s!"Theorem statement:\n\n```lean\n{fmtT.pretty 100}\n```\n"
  IO.FS.createDirAll "bench"
  IO.FS.writeFile "bench/corpus.json" ((Json.arr (sel.map (·.toJson))).pretty 120 ++ "\n")
  if let some path ← IO.getEnv "ROSETTE_CORPUS_STATS" then
    IO.FS.writeFile path ("\n".intercalate (← out.get).toList ++ "\n")

end Rosette.Corpus

-- The scan only runs on request, so that building/importing this module stays cheap.
#eval show MetaM Unit from do
  if (← IO.getEnv "ROSETTE_CORPUS").isSome then
    Rosette.Corpus.run
  else
    IO.println "Rosette.Corpus: set ROSETTE_CORPUS=1 to run the scan and write bench/corpus.json"
