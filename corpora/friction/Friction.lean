/-
Friction census exporter: hypothesis-level and proof-term-level data for every project theorem.

Stand-alone program (imports only `Lean`); loads the BUILT environment of a corpus with
`importModules` and reads everything from `Environment` / `Expr`.  No source text, no
pretty-printer output is parsed.  The same file is compiled against each corpus's toolchain.

  friction <families.json> <modules.txt> <roots,csv> <primary.txt> <theorems.txt> <outPrefix> <shard> <nshards>
  friction ... <outPrefix> auxlist 1     writes <outPrefix>.auxlist.tsv: non-primary project theorem constants and their primary parent
  friction ... <outPrefix> preds <d>     writes <outPrefix>.preds<d>.jsonl: content of project-defined predicates, opened to depth d (see `predScan`)

  modules.txt   modules to import (one per line)
  roots         module-name roots that count as "project"
  primary.txt   names of all primary declarations of the existing export (decls.jsonl `name`)
  theorems.txt  the subset with kind == theorem: these are exported
  writes <outPrefix>.hyps.<shard>.jsonl, .consts.<shard>.jsonl, .heads.<shard>.jsonl, .meta.<shard>.json

Definitions (see also out/corpus/friction/README.md):

* A proposition's CLASS: peel metadata / optParam / leading ∀ (incl. implications) / ¬ / ∃, then
  shape rules (finiteness: `x < ⊤`, `x ≠ ⊤`; positivity: `0 < x`, `0 ≤ x`, `x ≠ 0`), then the head
  constant looked up in the config's `type_heads`, else `other`.
* PROOF MASS.  The proof term (plus the values of the theorem's own body auxiliaries, inlined at
  their use sites) is walked once from the root.  Binders are opened with fresh free variables.
  A *proof subterm* is an argument of an application, a `let`/`have` value, or the root, whose
  expected type (the instantiated binder domain of the function's type) is a `Prop`.
  Every node carries five independent labels inherited from the path that reaches it:
    outer : the class of the OUTERMOST enclosing proof subterm whose class is a side-condition
            class ("main" if there is none);
    inner : the class of the NEAREST enclosing proof subterm (the root counts);
    cast  : some enclosing proof subterm's type mentions a cast-flag constant;
    surg  : some enclosing proof subterm's type mentions an indicator/restrict/support/cutoff constant;
    kind  : proof spine / inside a non-proof (data or type) argument / inside an instance argument.
  For each label the count is the number of DISTINCT subterms (structural equality, after opening
  binders) reached with that label value.  A subterm reached with two values of a label (shared
  between two regions) is counted once under each, so the `outer` counts sum to slightly more than
  the number of distinct subterms (`nodes`); within one label value nothing is counted twice, and
  nested proof subterms are never double counted because a node has exactly one outermost /
  nearest enclosing proof subterm on any given path.
-/
import Lean
open Lean Meta

namespace Friction

def nameStr (n : Name) : String := n.toString (escape := false)
def hasSub (s pat : String) : Bool := (s.splitOn pat).length > 1
def takeStr (s : String) (n : Nat) : String := String.ofList (s.toList.take n)

/-! ### configuration -/

structure Matcher where
  exact : Std.HashSet String := {}
  pre : Array String := #[]
  modPre : Array String := #[]
  sub : Array String := #[]
  deriving Inhabited

def strs (j : Json) (k : String) : Array String :=
  match (j.getObjValD k).getArr? with
  | .ok a => a.filterMap fun x => x.getStr?.toOption
  | _ => #[]

def objs (j : Json) (k : String) : Array Json :=
  match (j.getObjValD k).getArr? with
  | .ok a => a
  | _ => #[]

def Matcher.ofJson (j : Json) : Matcher :=
  { exact := (strs j "exact").foldl (·.insert ·) {}, pre := strs j "prefix",
    modPre := strs j "module_prefix", sub := strs j "contains" }

def Matcher.test (m : Matcher) (name mod : String) : Bool :=
  m.exact.contains name || m.pre.any (name.startsWith ·) || m.modPre.any (mod.startsWith ·)
    || (!m.sub.isEmpty && (let l := name.toLower; m.sub.any (hasSub l ·)))

def flagNames : Array String := #["ennreal", "cast", "indicator", "restrict", "support", "cutoff", "top", "enorm", "ennrealTop"]
def fCast : UInt16 := 2
def fSurg : UInt16 := 4 ||| 8 ||| 16 ||| 32
def fTop : UInt16 := 64
def fEnnTop : UInt16 := 256

structure Config where
  classes : Array String
  sideId : Array UInt8                     -- class id -> outer id (0 = not a side condition)
  outerNames : Array String                -- outer id -> name ("main" at 0)
  typeHeads : Std.HashMap String UInt8
  flagM : Array Matcher                    -- indexed like flagNames (top unused)
  realTypes : Std.HashSet String
  constRules : Array (String × Matcher)
  orderMods : Array String
  families : Array String                  -- constant families
  cFin : UInt8
  cPos : UInt8
  cOrder : UInt8
  cOther : UInt8
  cTc : UInt8                              -- 255 if the config has no "tc" class
  cMem : UInt8                             -- 255 if the config has no "mem" class
  setTypes : Std.HashSet String            -- carriers whose ≤ / < is set inclusion
  instProp : Bool                          -- variant: a Prop-valued instance-implicit argument is an instance argument, not a proof subterm
  deriving Inhabited

def Config.clsId (classes : Array String) (s : String) : UInt8 :=
  match classes.findIdx? (· == s) with
  | some i => i.toUInt8
  | none => 255

def Config.load (path : String) : IO Config := do
  let j ← IO.ofExcept (Json.parse (← IO.FS.readFile path))
  let classes := strs j "classes"
  if classes.size > 24 then throw <| IO.userError "at most 24 classes"
  let side := strs j "side_condition_classes"
  if side.size > 7 then throw <| IO.userError "at most 7 side-condition classes"
  let mut sideId : Array UInt8 := classes.map fun _ => 0
  for i in [0:side.size] do
    let c := Config.clsId classes side[i]!
    if c == 255 then throw <| IO.userError s!"unknown side class {side[i]!}"
    sideId := sideId.set! c.toNat (i + 1).toUInt8
  let mut th : Std.HashMap String UInt8 := {}
  for o in objs j "type_heads" do
    let c := Config.clsId classes ((o.getObjValD "class").getStr?.toOption.getD "")
    if c == 255 then throw <| IO.userError s!"unknown class in type_heads: {o.getObjValD "class"}"
    for h in strs o "heads" do th := th.insert h c
  let mut flagM : Array Matcher := flagNames.map fun _ => {}
  for o in objs j "flags" do
    let f := (o.getObjValD "flag").getStr?.toOption.getD ""
    match flagNames.findIdx? (· == f) with
    | some i => flagM := flagM.set! i (Matcher.ofJson o)
    | none => throw <| IO.userError s!"unknown flag {f}"
  let rules := (objs j "const_rules").map fun o =>
    ((o.getObjValD "family").getStr?.toOption.getD "?", Matcher.ofJson o)
  let mut fams : Array String := #[]
  let add (fams : Array String) (s : String) := if fams.contains s then fams else fams.push s
  for (f, _) in rules do fams := add fams f
  for i in [0:classes.size] do
    fams := add fams (if sideId[i]! != 0 then classes[i]! else classes[i]! ++ "_lemma")
  for f in #["cast", "ennreal_ns", "indicator", "order_plumbing", "data_instance", "data"] do fams := add fams f
  let need (s : String) : IO UInt8 := do
    let c := Config.clsId classes s
    if c == 255 then throw <| IO.userError s!"class {s} missing from config"
    return c
  return { classes, sideId, outerNames := #["main"] ++ side, typeHeads := th, flagM,
           realTypes := (strs j "real_types").foldl (·.insert ·) {}, constRules := rules,
           orderMods := strs j "order_plumbing_module_prefixes", families := fams,
           cFin := ← need "finiteness", cPos := ← need "positivity", cOrder := ← need "order",
           cOther := ← need "other", cTc := Config.clsId classes "tc",
           cMem := Config.clsId classes "mem", setTypes := (strs j "set_like_types").foldl (·.insert ·) {},
           instProp := ((j.getObjValD "inst_props_are_instances").getBool?.toOption.getD false) }

def Config.famId (cfg : Config) (s : String) : UInt8 :=
  match cfg.families.findIdx? (· == s) with
  | some i => i.toUInt8
  | none => 255

/-! ### proposition classification (pure, syntactic) -/

def isZeroLit (e : Expr) : Bool :=
  let e := e.consumeMData
  match e with
  | .lit (.natVal 0) => true
  | _ =>
    if e.isAppOfArity ``OfNat.ofNat 3 then
      match (e.getArg! 1).consumeMData with
      | .lit (.natVal 0) => true
      | x => x.isAppOfArity ``OfNat.ofNat 3 && (x.getArg! 1).consumeMData == .lit (.natVal 0)
    else e.isAppOfArity ``Zero.zero 2

def isTopLit (e : Expr) : Bool := e.consumeMData.isAppOfArity `Top.top 2

/-- Peel metadata, optParam/autoParam, let, β-redexes, ∀ (A), ¬ (N), ∃ (E), `Fact` (F).
Returns core, peel string, negation parity. -/
partial def peelProp (e : Expr) (acc : String := "") (neg : Bool := false) : Expr × String × Bool :=
  match e with
  | .mdata _ b => peelProp b acc neg
  | .forallE _ _ b _ => peelProp b (acc.push 'A') neg
  | .letE _ _ v b _ => peelProp (b.instantiate1 v) acc neg
  | _ =>
    if e.getAppFn.isLambda then peelProp e.headBeta acc neg
    else if e.isAppOfArity ``Not 1 then peelProp e.appArg! (acc.push 'N') (!neg)
    else if e.isAppOfArity ``optParam 2 || e.isAppOfArity ``autoParam 2 || e.isAppOfArity ``outParam 1 then
      peelProp (e.getArg! 0) acc neg
    else if e.isAppOfArity `Fact 1 then peelProp e.appArg! (acc.push 'F') neg
    else if e.isAppOfArity ``Exists 2 then
      match e.appArg!.consumeMData with
      | .lam _ _ b _ => peelProp b (acc.push 'E') neg
      | _ => (e, acc, neg)
    else (e, acc, neg)

structure Shape where
  pos : String := ""       -- "", "lt", "le", "ne"
  fin : String := ""       -- "", "lt_top", "ne_top"
  subj : Option Expr := none
  deriving Inhabited

/-- Positivity / finiteness shape of an (already peeled) atom. -/
def shapeOfRaw (core : Expr) (neg : Bool) : Shape :=
  let args := core.getAppArgs
  match core.getAppFn.constName?, args.size with
  | some ``LT.lt, 4 =>
    if neg then {} else
    if isZeroLit args[2]! then { pos := "lt", subj := args[3]! }
    else if isTopLit args[3]! then { fin := "lt_top", subj := args[2]! } else {}
  | some ``GT.gt, 4 =>
    if neg then {} else
    if isZeroLit args[3]! then { pos := "lt", subj := args[2]! }
    else if isTopLit args[2]! then { fin := "lt_top", subj := args[3]! } else {}
  | some ``LE.le, 4 => if !neg && isZeroLit args[2]! then { pos := "le", subj := args[3]! } else {}
  | some ``GE.ge, 4 => if !neg && isZeroLit args[3]! then { pos := "le", subj := args[2]! } else {}
  | some ``Ne, 3 =>
    if neg then {} else
    if isZeroLit args[2]! then { pos := "ne", subj := args[1]! }
    else if isZeroLit args[1]! then { pos := "ne", subj := args[2]! }
    else if isTopLit args[2]! then { fin := "ne_top", subj := args[1]! }
    else if isTopLit args[1]! then { fin := "ne_top", subj := args[2]! } else {}
  | some ``Eq, 3 =>
    if !neg then {} else
    if isZeroLit args[2]! then { pos := "ne", subj := args[1]! }
    else if isZeroLit args[1]! then { pos := "ne", subj := args[2]! }
    else if isTopLit args[2]! then { fin := "ne_top", subj := args[1]! }
    else if isTopLit args[1]! then { fin := "ne_top", subj := args[2]! } else {}
  | _, _ => {}

/-- `0 < 0`, `0 ≤ 0`, `0 ≠ 0`, `⊤ ≠ ⊤` are not side conditions (`0 < 0` is linarith's final
contradiction atom): the subject must not itself be the literal. -/
def shapeOf (core : Expr) (neg : Bool) : Shape :=
  let sh := shapeOfRaw core neg
  match sh.subj with
  | some x => if (sh.pos != "" && isZeroLit x) || (sh.fin != "" && isTopLit x) then {} else sh
  | none => sh

def headName (e : Expr) : Name :=
  match e.getAppFn.consumeMData with
  | .const n _ => n
  | .fvar _ => `«<fvar>»
  | .bvar _ => `«<bvar>»
  | .sort _ => `«<sort>»
  | .lam .. => `«<lam>»
  | .forallE .. => `«<forall>»
  | .proj .. => `«<proj>»
  | .letE .. => `«<let>»
  | .lit _ => `«<lit>»
  | _ => `«<other>»

structure PropCls where
  cls : UInt8
  head : Name
  peel : String
  neg : Bool
  shape : Shape
  core : Expr
  deriving Inhabited

/-- `s ≤ t` / `s < t` on a set-like carrier is set inclusion (current Mathlib elaborates `⊆` on
`Set` to `LE.le`), so it is classed with membership facts, not with numeric inequalities. -/
def isSetOrder (cfg : Config) (core : Expr) : Bool :=
  match core.getAppFn.constName? with
  | some n =>
    (n == ``LE.le || n == ``LT.lt || n == ``GE.ge || n == ``GT.gt) && core.getAppNumArgs == 4 &&
      (match (core.getArg! 0).getAppFn.consumeMData with
       | .const t _ => cfg.setTypes.contains (nameStr t)
       | _ => false)
  | none => false

def classifyProp (env : Environment) (cfg : Config) (e : Expr) : PropCls :=
  let (core, peel, neg) := peelProp e
  let sh := shapeOf core neg
  let head := headName core
  let cls :=
    if sh.fin != "" then cfg.cFin
    else if sh.pos != "" then cfg.cPos
    else if cfg.cMem != 255 && isSetOrder cfg core then cfg.cMem
    else match cfg.typeHeads[nameStr head]? with
      | some c => c
      | none => if cfg.cTc != 255 && isClass env head then cfg.cTc else cfg.cOther
  { cls, head, peel, neg, shape := sh, core }

/-! ### sizes and structural hash (same measure as the existing corpus exports) -/

structure Info where
  tree : Nat
  h : UInt64
  deriving Inhabited

partial def analyze (e : Expr) : StateM (Std.HashMap ExprStructEq Info) Info := do
  match e with
  | .mdata _ b => analyze b
  | _ =>
    if let some r := (← get)[(⟨e⟩ : ExprStructEq)]? then return r
    let r ← match e with
      | .app f a => do
        let x ← analyze f; let y ← analyze a
        pure (⟨x.tree + y.tree + 1, mixHash 7 (mixHash x.h y.h)⟩ : Info)
      | .lam _ d b _ => do
        let x ← analyze d; let y ← analyze b
        pure ⟨x.tree + y.tree + 1, mixHash 59 (mixHash x.h y.h)⟩
      | .forallE _ d b _ => do
        let x ← analyze d; let y ← analyze b
        pure ⟨x.tree + y.tree + 1, mixHash 61 (mixHash x.h y.h)⟩
      | .letE _ t v b _ => do
        let x ← analyze t; let y ← analyze v; let z ← analyze b
        pure ⟨x.tree + y.tree + z.tree + 1, mixHash 67 (mixHash x.h (mixHash y.h z.h))⟩
      | .proj s i b => do
        let x ← analyze b
        pure ⟨x.tree + 1, mixHash 71 (mixHash (hash s) (mixHash (hash i) x.h))⟩
      | .bvar i => pure ⟨1, mixHash 3 (hash i)⟩
      | .sort _ => pure ⟨1, 37⟩
      | .lit (.natVal n) => pure ⟨1, mixHash 41 (hash n)⟩
      | .lit (.strVal s) => pure ⟨1, mixHash 43 (hash s)⟩
      | .const n _ => pure ⟨1, mixHash 5 (hash n)⟩
      | _ => pure ⟨1, 47⟩     -- free variables: one anonymous placeholder
    modify (·.insert ⟨e⟩ r)
    return r

/-- (tree size, DAG size, hash with all free variables identified). -/
def sizes (e : Expr) : Nat × Nat × UInt64 :=
  let (r, m) := (analyze e).run {}
  (r.tree, m.size, r.h)

def hexOf (h : UInt64) : String :=
  let s := String.ofList (Nat.toDigits 16 h.toNat)
  "".pushn '0' (16 - s.length) ++ s

/-! ### shape keys -/

def binderInfosOf (env : Environment) (n : Name) : Array BinderInfo :=
  match env.find? n with
  | none => #[]
  | some ci => Id.run do
    let mut t := ci.type
    let mut out := #[]
    let mut go := true
    while go do
      match t with
      | .forallE _ _ b bi => out := out.push bi; t := b
      | .mdata _ b => t := b
      | _ => go := false
    return out

structure SerSt where
  ph : Std.HashMap FVarId Nat := {}
  bc : Std.HashMap Name (Array BinderInfo) := {}

/-- Canonical text of an expression: telescope variables become `?0, ?1, …` in order of first
occurrence, instance-implicit arguments are dropped, universe levels are dropped. -/
partial def ser (env : Environment) (e : Expr) : StateM SerSt String := do
  match e with
  | .mdata _ b => ser env b
  | .fvar id =>
    let s ← get
    match s.ph[id]? with
    | some k => return s!"?{k}"
    | none =>
      let k := s.ph.size
      set { s with ph := s.ph.insert id k }
      return s!"?{k}"
  | .bvar i => return s!"#{i}"
  | .const n _ => return nameStr n
  | .sort l => return (if l.isZero then "Prop" else "Sort")
  | .lit (.natVal n) => return toString n
  | .lit (.strVal s) => return s.quote
  | .lam _ d b _ => return s!"(λ {← ser env d}. {← ser env b})"
  | .forallE _ d b _ => return s!"(∀ {← ser env d}. {← ser env b})"
  | .letE _ t v b _ => return s!"(let {← ser env t} := {← ser env v}. {← ser env b})"
  | .proj s i b => return s!"({nameStr s}.{i} {← ser env b})"
  | .mvar _ => return "?m"
  | .app .. =>
    let fn := e.getAppFn
    let args := e.getAppArgs
    let bis ← match fn.consumeMData with
      | .const n _ => do
        match (← get).bc[n]? with
        | some b => pure b
        | none =>
          let b := binderInfosOf env n
          modify fun s => { s with bc := s.bc.insert n b }
          pure b
      | _ => pure #[]
    let mut out := "(" ++ (← ser env fn)
    for i in [0:args.size] do
      if i < bis.size && bis[i]!.isInstImplicit then continue
      out := out ++ " " ++ (← ser env args[i]!)
    return out ++ ")"

def coarseArg (e : Expr) : String :=
  let e := e.consumeMData
  if e.isAppOfArity ``OfNat.ofNat 3 then
    match (e.getArg! 1).consumeMData with
    | .lit (.natVal n) => toString n
    | _ => "OfNat"
  else match e.getAppFn.consumeMData with
    | .fvar _ => "?"
    | .bvar _ => "#"
    | .const n _ => nameStr n
    | .lam .. => "λ"
    | .forallE .. => "∀"
    | .sort _ => "Sort"
    | .lit (.natVal n) => toString n
    | .lit _ => "lit"
    | .proj .. => "π"
    | _ => "…"

/-- Head of the peeled proposition with one-level summaries of its explicit arguments. -/
def coarseKey (env : Environment) (peel : String) (core : Expr) : String := Id.run do
  let fn := core.getAppFn.consumeMData
  let args := core.getAppArgs
  let bis := match fn with | .const n _ => binderInfosOf env n | _ => #[]
  let mut parts : Array String := #[]
  for i in [0:args.size] do
    if i < bis.size && !bis[i]!.isExplicit then continue
    parts := parts.push (coarseArg args[i]!)
  let h := match fn with
    | .const n _ => nameStr n
    | _ => coarseArg fn
  return (if peel == "" then "" else peel ++ ":") ++ h ++ "(" ++ ",".intercalate parts.toList ++ ")"

/-! ### existential-constant detection -/

structure ExSt where
  isReal : Array Bool := #[]
  posHit : Array Bool := #[]

/-- Walk through `∃`, `∧` and `∀` (including implications, conclusion side only); record for every
∃-bound variable whether its type is a real type and whether a conjunct directly under its binder
chain is a positivity fact about exactly that variable (`∃ C, 0 < C ∧ …`, `∃ C > 0, …`). -/
partial def exScan (cfg : Config) (e : Expr) (stack : List (Option Nat)) : StateM ExSt Unit := do
  match e.consumeMData with
  | .forallE _ _ b _ => exScan cfg b (none :: stack)
  | e =>
  if e.isAppOfArity ``Exists 2 then
    match e.appArg!.consumeMData with
    | .lam _ t b _ =>
      let id := (← get).isReal.size
      let real := match t.getAppFn.consumeMData with
        | .const n _ => cfg.realTypes.contains (nameStr n)
        | _ => false
      modify fun s => { isReal := s.isReal.push real, posHit := s.posHit.push false }
      exScan cfg b (some id :: stack)
    | _ => pure ()
  else if e.isAppOfArity ``And 2 then
    exScan cfg (e.getArg! 0) stack
    exScan cfg (e.getArg! 1) stack
  else
    let sh := shapeOf e false
    if sh.pos != "" then
      match (sh.subj.map (·.consumeMData) : Option Expr) with
      | some (Expr.bvar k) =>
        match stack[k]? with
        | some (some id) => modify fun s => { s with posHit := s.posHit.set! id true }
        | _ => pure ()
      | _ => pure ()

partial def stripLams : Expr → Expr
  | .lam _ _ b _ => stripLams b
  | .mdata _ b => stripLams b
  | e => e

partial def stripForalls : Expr → Expr
  | .forallE _ _ b _ => stripForalls b
  | .mdata _ b => stripForalls b
  | e => e

/-! ### content of project-defined predicates (mode `preds`) -/

structure PredSt where
  cls : Array Nat
  unresolved : Array String := #[]
  exReal : Nat := 0
  exRealPos : Nat := 0
  atoms : Nat := 0
  maxDepth : Nat := 0
  structs : Nat := 0

def PredSt.addEx (cfg : Config) (e : Expr) (s : PredSt) : PredSt :=
  let ((), ex) := (exScan cfg e []).run {}
  let nReal := (ex.isReal.filter id).size
  let nPos := ((List.range ex.isReal.size).filter fun i => ex.isReal[i]! && ex.posHit[i]!).length
  { s with exReal := s.exReal + nReal, exRealPos := s.exRealPos + nPos }

/-- Classes of the atoms a proposition is built from, looking THROUGH project definitions
(δ-unfolded with their arguments) and project structures (their field types), through `∧` and
through whatever `peelProp` peels (∀, ¬, ∃, `Fact`).  `exReal`/`exRealPos` are counted on every
body that is opened.  Purely syntactic; depth and atom budgets guard against blow-up. -/
partial def predScan (env : Environment) (cfg : Config) (isProj : Name → Bool) (maxD : Nat) (e : Expr) (depth : Nat) :
    StateM PredSt Unit := do
  if (← get).atoms > 3000 then return
  let pc := classifyProp env cfg e
  let core := pc.core
  if core.isAppOfArity ``And 2 || core.isAppOfArity ``Iff 2 || core.isAppOfArity ``Or 2 then
    predScan env cfg isProj maxD (core.getArg! 0) depth
    predScan env cfg isProj maxD (core.getArg! 1) depth
    return
  let atom (c : UInt8) : StateM PredSt Unit :=
    modify fun s => { s with cls := s.cls.modify c.toNat (· + 1), atoms := s.atoms + 1,
                             maxDepth := max s.maxDepth depth }
  if pc.cls != cfg.cOther then atom pc.cls; return
  let fn := core.getAppFn.consumeMData
  let args := core.getAppArgs
  let unres : StateM PredSt Unit := do
    atom cfg.cOther
    modify fun s => if s.unresolved.size < 8 && !s.unresolved.contains (nameStr pc.head)
      then { s with unresolved := s.unresolved.push (nameStr pc.head) } else s
  match fn with
  | .const n ls =>
    if !isProj n || depth ≥ maxD then unres else
    match env.find? n with
    | some (.defnInfo v) =>
      if v.levelParams.length != ls.length then unres else
      let body := (v.value.instantiateLevelParams v.levelParams ls).beta args
      modify (PredSt.addEx cfg (stripLams body))
      predScan env cfg isProj maxD (stripLams body) (depth + 1)
    | some (.inductInfo iv) =>
      match iv.ctors with
      | [ctor] =>
        match env.find? ctor with
        | some ci =>
          if iv.numIndices != 0 || ci.levelParams.length != ls.length || args.size < iv.numParams then unres else
          modify fun s => { s with structs := s.structs + 1 }
          let mut t := ci.type.instantiateLevelParams ci.levelParams ls
          -- instantiate the parameters
          for i in [0:iv.numParams] do
            match t with
            | .forallE _ _ b _ => t := b.instantiate1 args[i]!
            | _ => pure ()
          let mut go := true
          while go do
            match t with
            | .forallE _ d b _ =>
              modify (PredSt.addEx cfg d)
              predScan env cfg isProj maxD d (depth + 1)
              t := b
            | .mdata _ b => t := b
            | _ => go := false
        | none => unres
      | _ => unres
    | _ => unres
  | _ => atom cfg.cOther

/-! ### global caches -/

structure CInfo where
  fam : UInt8
  own : UInt16
  flags : UInt16
  isProj : Bool
  isProp : Bool
  deriving Inhabited

structure Global where
  own : Std.HashMap Name UInt16 := {}
  cinfo : Std.HashMap Name CInfo := {}
  argKinds : Std.HashMap Name (Array UInt8) := {}
  cDag : Std.HashMap Name Nat := {}
  cTree : Std.HashMap Name Nat := {}
  cThm : Std.HashMap Name Nat := {}
  headMass : Std.HashMap (UInt8 × Name) Nat := {}
  headN : Std.HashMap (UInt8 × Name) Nat := {}

structure Env where
  cfg : Config
  env : Environment
  isProj : Name → Bool
  modOf : Name → String
  g : IO.Ref Global

def ownFlag (x : Env) (n : Name) : IO UInt16 := do
  if let some f := (← x.g.get).own[n]? then return f
  let s := nameStr n
  let m := x.modOf n
  let mut f : UInt16 := 0
  for i in [0:x.cfg.flagM.size] do
    if x.cfg.flagM[i]!.test s m then f := f ||| ((1 : UInt16) <<< i.toUInt16)
  if n == `Top.top then f := f ||| fTop
  x.g.modify fun g => { g with own := g.own.insert n f }
  return f

/-- `(⊤ : ℝ≥0∞)` occurs (as opposed to the ⊤ of `ℕ∞`, `WithTop _`, a lattice of sets, …). -/
def hasEnnTop (e : Expr) : Bool :=
  (e.find? fun s => s.isAppOfArity `Top.top 2 &&
    (match (s.getArg! 0).consumeMData with | .const n _ => n == `ENNReal | _ => false)).isSome

def exprFlags (x : Env) (e : Expr) : IO UInt16 := do
  let mut f : UInt16 := 0
  for c in e.getUsedConstants do f := f ||| (← ownFlag x c)
  if f &&& fTop != 0 && hasEnnTop e then f := f ||| fEnnTop
  return f

def isPropSafe (e : Expr) : MetaM Bool := do
  try isProp e catch _ => return false

def constInfoOf (x : Env) (n : Name) : MetaM CInfo := do
  if let some c := (← x.g.get).cinfo[n]? then return c
  let cfg := x.cfg
  let some ci := x.env.find? n | return { fam := cfg.famId "data", own := 0, flags := 0, isProj := false, isProp := false }
  let s := nameStr n
  let m := x.modOf n
  let proj := x.isProj n
  let own ← ownFlag x n
  let tfl ← exprFlags x ci.type
  let isP ← isPropSafe ci.type
  let mut fam : Option String := none
  if !proj then
    for (f, mt) in cfg.constRules do
      if fam.isNone && mt.test s m then fam := some f
  if fam.isNone then
    if isP then
      let pc := classifyProp x.env cfg ci.type
      if cfg.sideId[pc.cls.toNat]! != 0 then fam := some cfg.classes[pc.cls.toNat]!
      else if tfl &&& fCast != 0 then fam := some "cast"
      else if !proj && (s.startsWith "ENNReal." || s.startsWith "NNReal.") then fam := some "ennreal_ns"
      else if tfl &&& fSurg != 0 then fam := some "indicator"
      else if pc.cls == cfg.cOrder && !proj && cfg.orderMods.any (m.startsWith ·) then fam := some "order_plumbing"
      else fam := some (cfg.classes[pc.cls.toNat]! ++ "_lemma")
    else
      if own &&& fCast != 0 then fam := some "cast"
      else if own &&& fSurg != 0 then fam := some "indicator"
      else
        let isInst := match ci.type.getForallBody.getAppFn with
          | .const c _ => isClass x.env c
          | _ => false
        fam := some (if isInst then "data_instance" else "data")
  let r : CInfo := { fam := cfg.famId (fam.getD "data"), own, flags := own ||| tfl, isProj := proj, isProp := isP }
  x.g.modify fun g => { g with cinfo := g.cinfo.insert n r }
  return r

/-- Per binder of a constant's type: 0 = never a proof, 1 = always a proof, 2 = depends on the instance. -/
def getArgKinds (x : Env) (n : Name) : MetaM (Array UInt8) := do
  if let some k := (← x.g.get).argKinds[n]? then return k
  let k ← try
      match x.env.find? n with
      | none => pure #[]
      | some ci =>
        forallTelescope ci.type fun xs _ => xs.mapM fun v => do
          let t ← inferType v
          let s ← whnfD (← inferType t)
          match s with
          | .sort l => pure (if l.isZero then (1 : UInt8) else if l.isNeverZero then 0 else 2)
          | _ => pure 2
    catch _ => pure #[]
  x.g.modify fun g => { g with argKinds := g.argKinds.insert n k }
  return k

/-! ### pass P: constant occurrence counts on the raw proof DAG -/

structure PSt where
  idx : Std.HashMap ExprStructEq Nat := {}
  nodes : Array Expr := #[]
  nonFn : Array Bool := #[]

partial def pdfs (auxVal : Name → Option Expr) (e : Expr) (isFn : Bool) : StateM PSt Unit := do
  match e with
  | .mdata _ b => pdfs auxVal b isFn
  | _ =>
    if let some i := (← get).idx[(⟨e⟩ : ExprStructEq)]? then
      if !isFn then modify fun s => { s with nonFn := s.nonFn.set! i true }
      return
    match e with
    | .app f a => pdfs auxVal f true; pdfs auxVal a false
    | .lam _ d b _ => pdfs auxVal d false; pdfs auxVal b false
    | .forallE _ d b _ => pdfs auxVal d false; pdfs auxVal b false
    | .letE _ t v b _ => pdfs auxVal t false; pdfs auxVal v false; pdfs auxVal b false
    | .proj _ _ b => pdfs auxVal b false
    | .const n _ => if let some v := auxVal n then pdfs auxVal v false
    | _ => pure ()
    modify fun s => { idx := s.idx.insert ⟨e⟩ s.nodes.size, nodes := s.nodes.push e, nonFn := s.nonFn.push (!isFn) }

partial def stripM : Expr → Expr
  | .mdata _ b => stripM b
  | e => e

structure PRes where
  dag : Nat
  tree : Nat
  cDag : Std.HashMap Name Nat
  cTree : Std.HashMap Name Nat
  auxUsed : Nat

def passP (auxVal : Name → Option Expr) (root : Expr) : PRes := Id.run do
  let ((), st) := (pdfs auxVal root false).run {}
  let n := st.nodes.size
  let mut mult : Array Nat := Array.replicate n 0
  if n > 0 then mult := mult.set! (n - 1) 1
  let mut cDag : Std.HashMap Name Nat := {}
  let mut cTree : Std.HashMap Name Nat := {}
  let mut tree := 0
  let mut auxUsed := 0
  let bump (mult : Array Nat) (c : Expr) (m : Nat) : Array Nat :=
    match st.idx[(⟨stripM c⟩ : ExprStructEq)]? with
    | some i => mult.modify i (· + m)
    | none => mult
  for k in [0:n] do
    let i := n - 1 - k
    let e := st.nodes[i]!
    let m := mult[i]!
    tree := tree + m
    match e with
    | .app f a => mult := bump mult f m; mult := bump mult a m
    | .lam _ d b _ => mult := bump mult d m; mult := bump mult b m
    | .forallE _ d b _ => mult := bump mult d m; mult := bump mult b m
    | .letE _ t v b _ => mult := bump mult t m; mult := bump mult v m; mult := bump mult b m
    | .proj _ _ b => mult := bump mult b m
    | .const c _ =>
      match auxVal c with
      | some v => mult := bump mult v m; auxUsed := auxUsed + 1
      | none => cTree := cTree.insert c (cTree.getD c 0 + m)
    | _ => pure ()
    if st.nonFn[i]! then
      match e.getAppFn with
      | .const c _ => if (auxVal c).isNone then cDag := cDag.insert c (cDag.getD c 0 + 1)
      | _ => pure ()
  return { dag := n, tree, cDag, cTree, auxUsed }

/-! ### pass M: proof-mass partitions -/

structure WCtx where
  outer : UInt8 := 0
  inner : UInt8 := 0
  kind : UInt8 := 0
  cast : Bool := false
  surg : Bool := false
  head : Name := .anonymous

def WCtx.pos (c : WCtx) : Array Nat :=
  #[c.outer.toNat, 8 + c.inner.toNat, if c.cast then 33 else 32, if c.surg then 35 else 34,
    36 + c.kind.toNat, 63]

def WCtx.data (c : WCtx) : WCtx := if c.kind == 0 then { c with kind := 1 } else c
def WCtx.inst (c : WCtx) : WCtx := { c with kind := 2 }

structure MSt where
  seen : Std.HashMap ExprStructEq UInt64 := {}
  wt : Std.HashMap ExprStructEq Nat := {}          -- extra weight (collapsed binder chains)
  -- a binder chain is opened ONCE: revisits under other labels reuse the same free variables,
  -- otherwise the body would be duplicated with fresh variables and counted again
  bcache : Std.HashMap ExprStructEq (Array (FVarId × Name × Expr × BinderInfo) × Expr) := {}
  lcache : Std.HashMap ExprStructEq (FVarId × Expr) := {}
  sideN : Array Nat := Array.replicate 8 0
  sideTop : Array (Nat × UInt8 × String × String) := #[]
  headMass : Std.HashMap (UInt8 × Name) Nat := {}
  headN : Std.HashMap (UInt8 × Name) Nat := {}
  clsCache : Std.HashMap ExprStructEq (UInt8 × Name × UInt16) := {}
  visits : Nat := 0
  proofSubterms : Nat := 0

structure WEnv where
  x : Env
  auxVal : Name → Option Expr
  budget : Nat

abbrev W := ReaderT WEnv (StateRefT MSt MetaM)

/-- Record that `e` is reached with labels `c`; returns the positions that are new. -/
def mark (e : Expr) (c : WCtx) (w : Nat := 1) : W (Array Nat) := do
  let ps := c.pos
  let r ← modifyGet fun (s : MSt) =>
    let old := s.seen.getD ⟨e⟩ 0
    let newPs := ps.filter fun p => (old >>> p.toUInt64) &&& 1 == 0
    if newPs.isEmpty then (newPs, { s with visits := s.visits + 1 })
    else
      let bits := newPs.foldl (fun b p => b ||| ((1 : UInt64) <<< p.toUInt64)) old
      let innerNew := newPs.any fun p => p ≥ 8 && p < 32
      let hm := if innerNew then s.headMass.insert (c.inner, c.head) (s.headMass.getD (c.inner, c.head) 0 + w) else s.headMass
      (newPs, { s with seen := s.seen.insert ⟨e⟩ bits, headMass := hm, visits := s.visits + 1 })
  if (← get).visits > (← read).budget then throwError "node budget exceeded"
  return r

def addExtra (e : Expr) (ps : Array Nat) (c : WCtx) (w : Nat) : W Unit := do
  if w == 0 then return
  modify fun s =>
    let innerNew := ps.any fun p => p ≥ 8 && p < 32
    let hm := if innerNew then s.headMass.insert (c.inner, c.head) (s.headMass.getD (c.inner, c.head) 0 + w) else s.headMass
    { s with wt := s.wt.insert ⟨e⟩ (w + 1), headMass := hm }

/-- Record an outermost side-condition proof subterm (for the per-theorem "largest" list). -/
def noteSide (c c' : WCtx) (t pf : Expr) : W Unit := do
  if c.outer != 0 || c'.outer == 0 then return
  let x := (← read).x
  let (_, dag, _) := sizes pf
  let pc := classifyProp x.env x.cfg t
  let entry := (dag, c'.inner, coarseKey x.env pc.peel pc.core, nameStr (headName (stripLams pf)))
  modify fun s =>
    let top := (s.sideTop.push entry).qsort (fun a b => a.1 > b.1)
    { s with sideN := s.sideN.modify c'.outer.toNat (· + 1), sideTop := top.extract 0 5 }

def enterProof (c : WCtx) (t : Expr) : W WCtx := do
  let x := (← read).x
  let (cls, head, fl) ← do
    match (← get).clsCache[(⟨t⟩ : ExprStructEq)]? with
    | some r => pure r
    | none =>
      let pc := classifyProp x.env x.cfg t
      let fl ← exprFlags x t
      let r := (pc.cls, pc.head, fl)
      modify fun s => { s with clsCache := s.clsCache.insert ⟨t⟩ r }
      pure r
  modify fun s => { s with proofSubterms := s.proofSubterms + 1,
                           headN := s.headN.insert (cls, head) (s.headN.getD (cls, head) 0 + 1) }
  return { outer := if c.outer != 0 then c.outer else x.cfg.sideId[cls.toNat]!,
           inner := cls, kind := c.kind,
           cast := c.cast || fl &&& fCast != 0, surg := c.surg || fl &&& fSurg != 0, head }

/-- For arguments `lo ≤ i < n` of `fn args`: `(some T, _)` if the argument is a proof of `T`,
else `(none, isInstanceArgument)`. -/
def argInfos (fn : Expr) (args : Array Expr) (lo : Nat) : W (Array (Option Expr × Bool)) := do
  let x := (← read).x
  let fn' := fn.consumeMData
  let n := args.size
  let beta := fn'.isLambda
  let kinds ← match fn' with
    | .const c _ => (getArgKinds x c : MetaM _)
    | _ => pure #[]
  let mut out : Array (Option Expr × Bool) := #[]
  let mut dead := false
  let mut fty : Expr := fn'
  if !beta then
    match ← (try some <$> inferType fn' catch _ => pure none : MetaM (Option Expr)) with
    | some t => fty := t
    | none => dead := true
  let mut j := 0
  for i in [0:n] do
    let mut dom : Option (Expr × BinderInfo) := none
    if !dead then
      if beta then
        match fty with
        | .lam _ d b bi => dom := some (d, bi); fty := b
        | _ => dead := true
      else
        if !fty.isForall then
          let t ← (try whnf (fty.instantiateRevRange j i args) catch _ => pure (.sort .zero) : MetaM Expr)
          fty := t; j := i
        match fty with
        | .forallE _ d b bi => dom := some (d, bi); fty := b
        | _ => dead := true
    if i < lo then continue
    match dom with
    | none =>
      let r ← (try
          let t ← inferType args[i]!
          if ← isProp t then pure (some t) else pure none
        catch _ => pure none : MetaM (Option Expr))
      out := out.push (r, false)
    | some (d, bi) =>
      let kind : UInt8 := if !beta && i < kinds.size then kinds[i]! else 2
      if kind == 0 then out := out.push (none, bi.isInstImplicit)
      else
        let d' := (d.instantiateRevRange j i args).headBeta
        let isPf ← if kind == 1 then pure true else (isPropSafe d' : MetaM Bool)
        if isPf && !(x.cfg.instProp && bi.isInstImplicit) then out := out.push (some d', false)
        else out := out.push (none, bi.isInstImplicit)
  return out

mutual

partial def visit (e : Expr) (c : WCtx) : W Unit := do
  match e with
  | .mdata _ b => visit b c
  | .app .. => visitApp e c
  | _ =>
    let nb ← mark e c
    if nb.isEmpty then return
    match e with
    | .lam .. => visitBinders e c nb
    | .forallE .. => visitBinders e c nb
    | .letE n t v b _ =>
      visit t c.data
      let cv ← if ← (isPropSafe t : MetaM Bool) then enterProof c t else pure c.data
      noteSide c cv t v
      visit v cv
      let (id, body) ← match (← get).lcache[(⟨e⟩ : ExprStructEq)]? with
        | some r => pure r
        | none => do
          let id ← mkFreshFVarId
          let r := (id, b.instantiate1 (mkFVar id))
          modify fun s => { s with lcache := s.lcache.insert ⟨e⟩ r }
          pure r
      let lctx := (← getLCtx).mkLetDecl id n t v
      withLCtx lctx (← getLocalInstances) (visit body c)
    | .proj _ _ s => visit s c
    | .const n _ =>
      if let some v := (← read).auxVal n then visit v c
    | _ => pure ()

partial def visitBinders (e : Expr) (c : WCtx) (nb : Array Nat) : W Unit := do
  let (decls, body) ← match (← get).bcache[(⟨e⟩ : ExprStructEq)]? with
    | some r => pure r
    | none => do
      let isLam := e.isLambda
      let mut fvars : Array Expr := #[]
      let mut decls : Array (FVarId × Name × Expr × BinderInfo) := #[]
      let mut cur := e
      let mut go := true
      while go do
        match cur with
        | .lam n d b bi =>
          if isLam then
            let id ← mkFreshFVarId
            decls := decls.push (id, n, d.instantiateRev fvars, bi)
            fvars := fvars.push (mkFVar id); cur := b
          else go := false
        | .forallE n d b bi =>
          if !isLam then
            let id ← mkFreshFVarId
            decls := decls.push (id, n, d.instantiateRev fvars, bi)
            fvars := fvars.push (mkFVar id); cur := b
          else go := false
        | _ => go := false
      let r := (decls, cur.instantiateRev fvars)
      modify fun s => { s with bcache := s.bcache.insert ⟨e⟩ r }
      pure r
  addExtra e nb c (decls.size - 1)
  let mut lctx ← getLCtx
  for (id, n, d, bi) in decls do lctx := lctx.mkLocalDecl id n d bi
  withLCtx lctx (← getLocalInstances) do
    for (_, _, d, _) in decls do visit d c.data
    visit body c

partial def visitApp (e : Expr) (c : WCtx) : W Unit := do
  let fn := e.getAppFn
  let args := e.getAppArgs
  let n := args.size
  let mut lo := n
  let mut p := e
  let mut go := true
  while go && lo > 0 do
    let nb ← mark p c
    if nb.isEmpty then go := false
    else
      lo := lo - 1
      p := p.appFn!
  if lo == n then return
  if lo == 0 then visit fn c
  let infos ← argInfos fn args lo
  for i in [lo:n] do
    let (ty?, inst) := infos[i - lo]!
    let ci ← match ty? with
      | some t => do
        let c' ← enterProof c t
        noteSide c c' t args[i]!
        pure c'
      | none => pure (if inst then c.inst else c.data)
    visit args[i]! ci

end

/-! ### statement telescope -/

def flagList (f : UInt16) : Json :=
  toJson ((List.range flagNames.size).filterMap fun i =>
    if f &&& ((1 : UInt16) <<< i.toUInt16) != 0 then some flagNames[i]! else none)

def biStr : BinderInfo → String
  | .default => "explicit"
  | .implicit => "implicit"
  | .strictImplicit => "strict"
  | .instImplicit => "inst"

def propFields (x : Env) (idx : Std.HashMap FVarId Nat) (t : Expr) : MetaM (List (String × Json)) := do
  let cfg := x.cfg
  let pc := classifyProp x.env cfg t
  let (tree, dag, h) := sizes t
  let fl ← exprFlags x t
  let big := tree > 4000
  let (shape, shapeHash) :=
    if big then ("", hexOf h)
    else
      let (s, _) := (ser x.env t).run {}
      (takeStr s 400, hexOf (hash s))
  let subjVar : Json := match (pc.shape.subj.map (·.consumeMData) : Option Expr) with
    | some (Expr.fvar id) => match idx[id]? with | some i => toJson i | none => Json.null
    | _ => Json.null
  let ((), ex) := (exScan cfg t []).run {}
  let exReal := (ex.isReal.filter id).size
  let exRealPos := ((List.range ex.isReal.size).filter fun i => ex.isReal[i]! && ex.posHit[i]!).length
  return [
    ("head", nameStr pc.head), ("cls", cfg.classes[pc.cls.toNat]!), ("peel", pc.peel), ("neg", pc.neg),
    ("pos", pc.shape.pos), ("fin", pc.shape.fin), ("subjVar", subjVar),
    ("dag", toJson dag), ("shape", toJson shape), ("shapeHash", shapeHash), ("shapeBig", toJson (decide big)),
    ("coarse", coarseKey x.env pc.peel pc.core), ("flags", flagList fl),
    ("exN", ex.isReal.size), ("exReal", exReal), ("exRealPos", exRealPos)]

def stmtInfo (x : Env) (ty : Expr) : MetaM (Json × Json × UInt8) :=
  forallTelescope ty fun xs concl => do
    let mut idx : Std.HashMap FVarId Nat := {}
    for i in [0:xs.size] do idx := idx.insert xs[i]!.fvarId! i
    let mentions (e : Expr) : Json :=
      let ids := (collectFVars {} e).fvarIds.filterMap fun f => idx[f]?
      toJson (ids.qsort (· < ·))
    let mut bs : Array Json := #[]
    for i in [0:xs.size] do
      let decl ← xs[i]!.fvarId!.getDecl
      let t := decl.type
      let isP ← isPropSafe t
      let kind := if decl.binderInfo.isInstImplicit then "inst"
        else if isP then "hyp"
        else if (stripM t).isSort then "type" else "term"
      let (core, peel, _) := peelProp t
      let mut fields : List (String × Json) := [
        ("i", i), ("name", decl.userName.eraseMacroScopes.toString ++ (if decl.userName.hasMacroScopes then "✝" else "")), ("bi", biStr decl.binderInfo), ("kind", kind),
        ("isProp", isP), ("mentions", mentions t), ("size", (sizes t).1)]
      if isP then fields := fields ++ (← propFields x idx t)
      else
        let fl ← exprFlags x t
        fields := fields ++ ([("head", toJson (nameStr (headName core))), ("isFun", toJson (stripM t).isForall),
                                ("coarse", toJson (coarseKey x.env peel core)), ("flags", flagList fl)] : List (String × Json))
      bs := bs.push (Json.mkObj fields)
    let cf ← propFields x idx concl
    let cj := Json.mkObj ([("mentions", mentions concl), ("size", (sizes concl).1)] ++ cf)
    return (toJson bs, cj, (classifyProp x.env x.cfg concl).cls)

/-! ### driver -/

def famVec (cfg : Config) (v : Array (Nat × Nat)) : Json :=
  Json.mkObj ((List.range cfg.families.size).filterMap fun i =>
    let (a, b) := v[i]!
    if a == 0 && b == 0 then none else some (cfg.families[i]!, toJson #[a, b]))

partial def chainParent (isPrim : Name → Bool) : Name → Option Name
  | .str p _ | .num p _ =>
    if isPrim p then some p
    else if isPrivateName p && isPrim (privateToUserName p) then some (privateToUserName p)
    else chainParent isPrim p
  | .anonymous => none

unsafe def main (args : List String) : IO UInt32 := do
  let [cfgFile, modsFile, rootsS, primFile, thmFile, outPrefix, shardS, nshardS] := args
    | throw <| IO.userError "usage: friction families.json modules.txt roots primary.txt theorems.txt outPrefix shard nshards"
  let mode := shardS
  let shard := if mode == "preds" || mode == "auxlist" then 0 else shardS.toNat!
  let nshards := nshardS.toNat!
  let t0 ← IO.monoMsNow
  let cfg ← Config.load cfgFile
  initSearchPath (← findSysroot)
  enableInitializersExecution
  let modNames := ((← IO.FS.lines modsFile).filter (· ≠ "")).map (·.toName)
  let env ← importModules (modNames.map fun m => { module := m }) {} (trustLevel := 1024) (loadExts := true)
  let t1 ← IO.monoMsNow
  let roots := (rootsS.splitOn ",").map (·.toName)
  let projIdx : Array Bool := env.header.moduleNames.map fun m => roots.contains m.getRoot
  let modStr : Array String := env.header.moduleNames.map (·.toString)
  let isProj (n : Name) : Bool :=
    match env.getModuleIdxFor? n with
    | some i => projIdx[i.toNat]!
    | none => false
  let modOf (n : Name) : String :=
    match env.getModuleIdxFor? n with
    | some i => modStr[i.toNat]!
    | none => ""
  -- name table of project constants (both renderings used by the existing exports)
  let mut byStr : Std.HashMap String Name := {}
  let mut nProjConsts := 0
  for (n, _) in env.constants.map₁.toList do
    if isProj n then
      nProjConsts := nProjConsts + 1
      byStr := byStr.insert (n.toString (escape := false)) n
      byStr := byStr.insert n.toString n
  let mut primary : Std.HashSet Name := {}
  let mut missing := 0
  for l in (← IO.FS.lines primFile) do
    if l == "" then continue
    match byStr[l]? with
    | some n => primary := primary.insert n
    | none => missing := missing + 1
  let mut thms : Array Name := #[]
  let mut thmMissing : Array String := #[]
  for l in (← IO.FS.lines thmFile) do
    if l == "" then continue
    match byStr[l]? with
    | some n => thms := thms.push n
    | none => thmMissing := thmMissing.push l
  IO.eprintln s!"[shard {shard}] import {t1 - t0} ms; project constants {nProjConsts}; primary {primary.size} (unresolved {missing}); theorems {thms.size} (unresolved {thmMissing.size})"
  let g ← IO.mkRef ({} : Global)
  let x : Env := { cfg, env, isProj, modOf, g }
  let isPrim (n : Name) : Bool := primary.contains n
  if mode == "auxlist" then
    -- every non-primary project THEOREM constant with the primary declaration it was generated for
    let h ← IO.FS.Handle.mk s!"{outPrefix}.auxlist.tsv" .write
    for (n, ci) in env.constants.map₁.toList do
      if !isProj n || isPrim n then continue
      match ci with
      | .thmInfo _ =>
        match chainParent isPrim n with
        | some p => h.putStrLn s!"{n.toString (escape := false)}\t{p.toString (escape := false)}"
        | none => pure ()
      | _ => pure ()
    h.flush
    return 0
  if mode == "preds" then
    -- content of every project-defined Prop-valued definition / structure that is not a class
    let h ← IO.FS.Handle.mk s!"{outPrefix}.preds{nshards}.jsonl" .write
    for (n, ci) in env.constants.map₁.toList do
      if !isProj n || isClass env n then continue
      let kind := match ci with
        | .defnInfo _ => "def"
        | .inductInfo iv => if iv.ctors.length == 1 && iv.numIndices == 0 then "structure" else "inductive"
        | _ => ""
      if kind == "" then continue
      unless (stripForalls ci.type).isProp do continue
      -- apply the constant to placeholders for its arguments
      let mut t := ci.type
      let mut args : Array Expr := #[]
      let mut go := true
      while go do
        match t with
        | .forallE _ _ b _ => args := args.push (mkFVar ⟨Name.mkNum `_pred args.size⟩); t := b
        | .mdata _ b => t := b
        | _ => go := false
      let e := mkAppN (mkConst n (ci.levelParams.map mkLevelParam)) args
      let ((), st) := (predScan env cfg isProj nshards e 0).run { cls := Array.replicate cfg.classes.size 0 }
      h.putStrLn (Json.mkObj [
        ("name", nameStr n), ("module", modOf n), ("kind", kind), ("arity", args.size),
        ("classes", Json.mkObj ((List.range cfg.classes.size).filterMap fun i =>
          if st.cls[i]! == 0 then none else some (cfg.classes[i]!, toJson st.cls[i]!))),
        ("unresolved", toJson st.unresolved), ("exReal", st.exReal), ("exRealPos", st.exRealPos),
        ("atoms", st.atoms), ("maxDepth", st.maxDepth), ("structs", st.structs)]).compress
    h.flush
    return 0
  let coreCtx : Core.Context := { fileName := "<friction>", fileMap := default, maxHeartbeats := 0,
                                  maxRecDepth := 1000000 }
  let runMeta {α} (act : MetaM α) : IO (Except String α) := do
    try
      let (a, _) ← act.run'.toIO coreCtx { env := env }
      return .ok a
    catch e => return .error (toString e)
  let h ← IO.FS.Handle.mk s!"{outPrefix}.hyps.{shard}.jsonl" .write
  let mut written := 0
  let mut stmtFail := 0
  let mut massFail := 0
  let mut noValue := 0
  let mut failNames : Array String := #[]
  let mut slowest : Array (Nat × String) := #[]
  let nF := cfg.families.size
  for k in [0:thms.size] do
    unless k % nshards == shard do continue
    let n := thms[k]!
    let some ci := env.find? n | continue
    let ts ← IO.monoMsNow
    let auxVal (c : Name) : Option Expr :=
      if c == n || !isProj c || isPrim c || env.isProjectionFn c then none
      else match env.find? c with
        | some (.thmInfo v) => (match chainParent isPrim c with | some p => if p == n then some v.value else none | none => some v.value)
        | some (.defnInfo v) => (match chainParent isPrim c with | some p => if p == n then some v.value else none | none => some v.value)
        | _ => none
    let mut fields : List (String × Json) := [
      ("name", n.toString (escape := false)), ("module", modOf n)]
    let (stTree, stDag, _) := sizes ci.type
    fields := fields ++ [("statementSize", toJson stTree), ("statementDagSize", toJson stDag)]
    -- statement
    let mut rootCls : UInt8 := cfg.cOther
    match ← runMeta (stmtInfo x ci.type) with
    | .ok (bs, cj, rc) =>
      rootCls := rc
      fields := fields ++ [("binders", bs), ("concl", cj)]
    | .error err =>
      stmtFail := stmtFail + 1
      failNames := failNames.push s!"stmt {n}: {takeStr err 200}"
      fields := fields ++ [("stmtError", Json.str (takeStr err 300))]
    -- proof
    let val? : Option Expr := match ci with
      | .thmInfo v => some v.value
      | .defnInfo v => some v.value
      | .opaqueInfo v => some v.value
      | _ => none
    match val? with
    | none =>
      noValue := noValue + 1
      fields := fields ++ [("proofSize", toJson (0 : Nat)), ("hasProof", toJson false)]
    | some v =>
      let (_, pDag, _) := sizes v
      let pr := passP auxVal v
      -- constant families
      let famRes ← runMeta (do
        let mut ext : Array (Nat × Nat) := Array.replicate nF (0, 0)
        let mut prj : Array (Nat × Nat) := Array.replicate nF (0, 0)
        let mut flagCnt : Array (Nat × Nat) := Array.replicate flagNames.size (0, 0)
        let mut nExt := 0
        let mut nPrj := 0
        for (c, tr) in pr.cTree.toList do
          let info ← constInfoOf x c
          let dg := pr.cDag.getD c 0
          let i := info.fam.toNat
          if i < nF then
            if info.isProj then prj := prj.modify i fun (a, b) => (a + dg, b + tr)
            else ext := ext.modify i fun (a, b) => (a + dg, b + tr)
          if info.isProj then nPrj := nPrj + 1 else nExt := nExt + 1
          if info.isProp then
            for f in [0:flagNames.size] do
              if info.flags &&& ((1 : UInt16) <<< f.toUInt16) != 0 then
                flagCnt := flagCnt.modify f fun (a, b) => (a + dg, b + tr)
        return (ext, prj, flagCnt, nExt, nPrj))
      g.modify fun gl => Id.run do
        let mut gl := gl
        for (c, tr) in pr.cTree.toList do
          gl := { gl with cTree := gl.cTree.insert c (gl.cTree.getD c 0 + tr),
                          cDag := gl.cDag.insert c (gl.cDag.getD c 0 + pr.cDag.getD c 0),
                          cThm := gl.cThm.insert c (gl.cThm.getD c 0 + 1) }
        return gl
      fields := fields ++ [("proofSize", toJson pDag), ("hasProof", toJson true),
        ("proofDagWithAux", toJson pr.dag), ("proofTree", toJson pr.tree), ("auxInlined", toJson pr.auxUsed)]
      match famRes with
      | .ok (ext, prj, flagCnt, nExt, nPrj) =>
        fields := fields ++ [("constsExt", famVec cfg ext), ("constsProj", famVec cfg prj),
          ("lemmaFlagUses", Json.mkObj ((List.range flagNames.size).filterMap fun i =>
            let (a, b) := flagCnt[i]!
            if a == 0 && b == 0 then none else some (flagNames[i]!, toJson #[a, b]))),
          ("nDistinctExt", toJson nExt), ("nDistinctProj", toJson nPrj)]
      | .error err =>
        failNames := failNames.push s!"consts {n}: {takeStr err 200}"
        fields := fields ++ [("constError", Json.str (takeStr err 300))]
      -- mass
      let tm ← IO.monoMsNow
      let wenv : WEnv := { x, auxVal, budget := 40000000 }
      let massRes ← runMeta (do
        let act : W Unit := do
          let c0 ← enterProof {} ci.type
          visit v c0
        let ((), st) ← (act.run wenv).run {}
        return st)
      let tm2 ← IO.monoMsNow
      match massRes with
      | .ok st =>
        -- fractional shares: a node reached with k values of a label gives 1/k to each
        let U : Nat := 720720
        let mut acc : Array Nat := Array.replicate 64 0
        let mut nodes := 0
        let groups : Array (Nat × Nat) := #[(0, 8), (8, 32), (32, 34), (34, 36), (36, 39)]
        for (e, bits) in st.seen.toList do
          let w := st.wt.getD e 1
          nodes := nodes + w
          for (a, b) in groups do
            let mut k := 0
            for p in [a:b] do
              if (bits >>> p.toUInt64) &&& 1 != 0 then k := k + 1
            if k == 0 then continue
            for p in [a:b] do
              if (bits >>> p.toUInt64) &&& 1 != 0 then acc := acc.modify p (· + w * (U / k))
        let fl (p : Nat) : Json := toJson (Float.round (acc[p]!.toFloat / U.toFloat * 1000) / 1000)
        let outer := Json.mkObj ((List.range cfg.outerNames.size).filterMap fun i =>
          if acc[i]! == 0 then none else some (cfg.outerNames[i]!, fl i))
        let inner := Json.mkObj ((List.range cfg.classes.size).filterMap fun i =>
          if acc[8 + i]! == 0 then none else some (cfg.classes[i]!, fl (8 + i)))
        let sideN := Json.mkObj ((List.range cfg.outerNames.size).filterMap fun i =>
          if i == 0 || st.sideN[i]! == 0 then none else some (cfg.outerNames[i]!, toJson st.sideN[i]!))
        let sideTop := toJson (st.sideTop.map fun (dag, cls, ty, by') => Json.mkObj [
          ("cls", Json.str cfg.classes[cls.toNat]!), ("type", Json.str ty), ("by", Json.str by'), ("dag", toJson dag)])
        fields := fields ++ [("mass", Json.mkObj [
          ("nodes", toJson nodes), ("outer", outer), ("inner", inner),
          ("castRegion", fl 33), ("surgRegion", fl 35),
          ("kind", toJson #[fl 36, fl 37, fl 38]),
          ("sideSubterms", sideN), ("sideTop", sideTop),
          ("proofSubterms", toJson st.proofSubterms), ("ms", toJson (tm2 - tm))]),
          ("rootClass", Json.str cfg.classes[rootCls.toNat]!)]
        g.modify fun gl => Id.run do
          let mut gl := gl
          for (key, m) in st.headMass.toList do
            gl := { gl with headMass := gl.headMass.insert key (gl.headMass.getD key 0 + m) }
          for (key, m) in st.headN.toList do
            gl := { gl with headN := gl.headN.insert key (gl.headN.getD key 0 + m) }
          return gl
      | .error err =>
        massFail := massFail + 1
        failNames := failNames.push s!"mass {n}: {takeStr err 200}"
        fields := fields ++ [("massError", Json.str (takeStr err 300))]
    let te ← IO.monoMsNow
    fields := fields ++ [("ms", toJson (te - ts))]
    if te - ts > 2000 then slowest := slowest.push (te - ts, n.toString (escape := false))
    h.putStrLn (Json.mkObj fields).compress
    written := written + 1
    if written % 500 == 0 then
      h.flush
      IO.eprintln s!"[shard {shard}] {written} written, {(← IO.monoMsNow) - t0} ms"
  h.flush
  -- aggregates
  let gl ← g.get
  let hc ← IO.FS.Handle.mk s!"{outPrefix}.consts.{shard}.jsonl" .write
  for (c, tr) in gl.cTree.toList do
    let info := gl.cinfo.getD c default
    hc.putStrLn (Json.mkObj [
      ("name", nameStr c), ("module", modOf c), ("family", cfg.families[info.fam.toNat]?.getD "?"),
      ("isProject", info.isProj), ("isProp", info.isProp), ("flags", flagList info.flags),
      ("dag", gl.cDag.getD c 0), ("tree", tr), ("theorems", gl.cThm.getD c 0)]).compress
  hc.flush
  let hh ← IO.FS.Handle.mk s!"{outPrefix}.heads.{shard}.jsonl" .write
  for ((cls, head), m) in gl.headMass.toList do
    hh.putStrLn (Json.mkObj [
      ("cls", cfg.classes[cls.toNat]?.getD "?"), ("head", nameStr head), ("isProject", isProj head),
      ("mass", m), ("proofSubterms", gl.headN.getD (cls, head) 0)]).compress
  hh.flush
  let t2 ← IO.monoMsNow
  IO.FS.writeFile s!"{outPrefix}.meta.{shard}.json" (Json.mkObj [
    ("shard", shard), ("nshards", nshards), ("leanVersion", Lean.versionString),
    ("modulesImported", modNames.size), ("projectConstants", nProjConsts),
    ("primaryResolved", primary.size), ("primaryUnresolved", missing),
    ("theoremsListed", thms.size), ("theoremsUnresolved", toJson thmMissing),
    ("written", written), ("noValue", noValue), ("stmtFail", stmtFail), ("massFail", massFail),
    ("failures", toJson failNames),
    ("slow", toJson (slowest.map fun (ms, nm) => Json.mkObj [("ms", ms), ("name", nm)])),
    ("importMs", t1 - t0), ("totalMs", t2 - t0)]).pretty
  IO.eprintln s!"[shard {shard}] wrote {written}; stmtFail {stmtFail} massFail {massFail}; total {t2 - t0} ms"
  return 0

end Friction

unsafe def main (args : List String) : IO UInt32 := Friction.main args
