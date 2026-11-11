/-
M7 re-invented abstractions: stage 2 (confirmation by proof) and stage 3 (derivation of project lemmas
from library lemmas through a confirmed equivalence).

Compiled once per project against the project's own Mathlib, then imported by generated batch files
(one `lean` process per batch, never one per candidate).  Nothing here writes to a corpus.

  reinvent_equiv "id" D n "iff|imp" (fun p0 .. p(n-1) => RHS) sides [fun p0 .. => S, ..] using "names" "names"
      states  ∀ xs, S xs → .. → (D xs ↔ RHS xs)      (`=` when D is not Prop-valued, `→` in mode imp)
      where xs are the first n binders of D's own type (taken from the environment), tries the fixed
      portfolio below in order, and on the first success adds the theorem `Reinvent.eqv.<id>` to the
      environment through the kernel and reports the axioms it depends on.
  reinvent_derive "id" projectLemma libraryLemma eqvTheorem
      re-proves the statement of `projectLemma` (its type, from the environment) by rewriting with the
      equivalence and applying `libraryLemma`; reports whether the kernel-checked proof term uses the
      library lemma and that it does not use the project lemma.
Every result is one line `RV {json}` on stdout.
-/
import Mathlib.Tactic
import Mathlib.Data.Real.Basic

open Lean Meta Elab Command Term

namespace Reinvent

/-- A sign condition on a hidden constant is redundant when the bounded statement is monotone in it. -/
theorem exists_nonneg_and_iff {P : ℝ → Prop} (h : ∀ c, P c → P (max c 0)) :
    (∃ C, 0 ≤ C ∧ P C) ↔ ∃ C, P C :=
  ⟨fun ⟨C, _, hC⟩ => ⟨C, hC⟩, fun ⟨C, hC⟩ => ⟨max C 0, le_max_right _ _, h C hC⟩⟩

theorem exists_pos_and_iff {P : ℝ → Prop} (h : ∀ c, P c → P (max c 1)) :
    (∃ C, 0 < C ∧ P C) ↔ ∃ C, P C :=
  ⟨fun ⟨C, _, hC⟩ => ⟨C, hC⟩,
   fun ⟨C, hC⟩ => ⟨max C 1, lt_of_lt_of_le one_pos (le_max_right _ _), h C hC⟩⟩

/-- The fixed portfolio for equivalences.  `«S»` is replaced by the simp set of the candidate: the project
definition, the project-local definitions unfolded to find the match, and the library characterisation
theorem the pattern came from.  Heartbeat limit per entry in thousands. -/
def portfolioIff : Array (String × String × Nat) := #[
  ("rfl", "(intros; first | exact Iff.rfl | rfl)", 20000),
  ("unfold", "(intros; simp only [«S»])", 40000),
  ("unfold+rfl", "(intros; (try simp only [«S»]); first | exact Iff.rfl | rfl | (constructor <;> intro h <;> exact h))", 40000),
  ("simp", "(intros; simp [«S»])", 60000),
  ("ext", "(intros; (try simp only [«S»]); (first | ext | funext); simp [«S»])", 60000),
  ("constructor", "(intros; (try simp only [«S»]); constructor <;> intro h <;> simp_all)", 60000),
  ("cases", "(intros; (try simp only [«S»]); refine ⟨fun h => ?_, fun h => ?_⟩ <;> (rcases h with ⟨⟩) <;> (first | assumption | (constructor <;> assumption) | (refine ⟨?_, ?_⟩ <;> assumption) | (refine ⟨?_, ?_, ?_⟩ <;> assumption) | (refine ⟨?_, ?_, ?_, ?_⟩ <;> assumption) | simp_all))", 60000),
  ("exact?", "(intros; (try simp only [«S»]); exact?)", 30000),
  ("aesop", "(intros; (try simp only [«S»]); aesop)", 40000),
  ("constant-sign", "(intros; (try simp only [«S»]); (try simp only [Real.norm_eq_abs, norm_norm, abs_abs, abs_of_nonneg, *]); (first | refine Reinvent.exists_nonneg_and_iff ?_ | refine Reinvent.exists_pos_and_iff ?_ | refine (Reinvent.exists_nonneg_and_iff ?_).symm | refine (Reinvent.exists_pos_and_iff ?_).symm); intro c hc; first | (filter_upwards [hc] with x hx; exact hx.trans (mul_le_mul_of_nonneg_right (le_max_left _ _) (by first | assumption | positivity | apply_assumption))) | (intros; exact (by solve_by_elim : _ ≤ _).trans (mul_le_mul_of_nonneg_right (le_max_left _ _) (by first | assumption | positivity | apply_assumption))))", 80000)
]

def portfolioImp : Array (String × String × Nat) := #[
  ("simp_all", "(intros; simp_all [«S»])", 60000),
  ("aesop", "(intros; (try simp only [«S»] at *); aesop)", 80000)
]

/-- `«E»` the equivalence, `«L»` the library lemma. -/
def portfolioDerive : Array (String × String × Nat) := #[
  ("rewrite+exact", "(intros; simp only [«E»] at *; first | exact «L» | exact «L» _ | exact «L» _ _ | exact «L» _ _ _ | (apply «L» <;> assumption) | solve_by_elim [«L»])", 60000),
  ("rewrite+simpa", "(intros; simp only [«E»] at *; first | simpa using «L» | simpa using «L» _ | simpa using «L» _ _ | simpa using «L» _ _ _)", 60000),
  ("rewrite+aesop", "(intros; simp only [«E»] at *; aesop (add safe apply «L»))", 80000)
]

def stdAxioms : List Name := [``propext, ``Classical.choice, ``Quot.sound]

def out (fields : List (String × Json)) : CoreM Unit := do
  IO.println ("RV " ++ (Json.mkObj fields).compress)

def parseTac (s : String) : CoreM Syntax := do
  match Parser.runParserCategory (← getEnv) `tactic s with
  | .ok stx => pure stx
  | .error e => throwError "tactic parse error: {e}"

/-- Try one tactic on `stmt`; on success return a closed proof term. -/
def tryTac (stmt : Expr) (tacS : String) (hb : Nat) : TermElabM (Option Expr) := do
  let s ← saveState
  let r ← withCurrHeartbeats <|
    withTheReader Core.Context (fun c => { c with maxHeartbeats := hb * 1000 }) do
      tryCatchRuntimeEx (do
        let tac ← parseTac tacS
        let mv ← mkFreshExprSyntheticOpaqueMVar stmt
        let rest ← Tactic.run mv.mvarId! (Tactic.evalTactic tac)
        unless rest.isEmpty do throwError "goals remain"
        synthesizeSyntheticMVarsNoPostponing
        let pf ← instantiateMVars mv
        if pf.hasExprMVar || pf.hasSorry then throwError "incomplete"
        pure (some pf)) (fun _ => pure none)
  if r.isNone then s.restore
  return r

def closeLevels (e : Expr) : Expr :=
  e.replaceLevel fun l => if l.isMVar then some Level.zero else none

/-- Add `name : stmt := pf` through the kernel; return whether its axioms are the standard three. -/
def addChecked (name : Name) (stmt pf : Expr) : TermElabM (Option (Array Name)) := do
  let stmt := closeLevels stmt
  let pf := closeLevels pf
  let ps := (collectLevelParams (collectLevelParams {} stmt) pf).params
  try
    addDecl (.thmDecl { name, levelParams := ps.toList, type := stmt, value := pf })
    let ax ← collectAxioms name
    return some ax
  catch _ => return none

def runPortfolio (name : Name) (stmt : Expr) (pf : Array (String × String × Nat)) (subst : String → String)
    (accept : Expr → Bool := fun _ => true) :
    TermElabM (Option (String × Array Name × Expr)) := do
  for (lbl, t, hb) in pf do
    if let some p ← tryTac stmt (subst t) hb then
      unless accept p do continue
      if let some ax ← addChecked name stmt p then
        return some (lbl, ax, p)
  return none

def resolve (id : Syntax) : TermElabM Name := do
  let n := id.getId
  if (← getEnv).contains n then return n
  realizeGlobalConstNoOverload id

def buildStmt (D : Name) (n : Nat) (mode : String) (rhsStx : Syntax) (sideStx : Array Syntax) :
    TermElabM Expr := do
  let ci ← getConstInfo D
  let lhsC := Lean.mkConst D (ci.levelParams.map mkLevelParam)
  let stmt ← forallBoundedTelescope ci.type (some n) fun xs _ =>
      withNewBinderInfos (xs.map fun x => (x.fvarId!, BinderInfo.default)) do
    unless xs.size == n do throwError "arity"
    let lhs := mkAppN lhsC xs
    let ty ← inferType lhs
    let rhsF ← elabTermEnsuringType rhsStx (← mkForallFVars xs ty)
    synthesizeSyntheticMVarsNoPostponing
    let rhs := (mkAppN (← instantiateMVars rhsF) xs).headBeta
    -- the right-hand side must not mention D itself (the statement would be trivially true)
    if rhs.getUsedConstants.contains D then throwError "rhs mentions D"
    let propTy ← mkForallFVars xs (mkSort 0)
    let mut sides := #[]
    for s in sideStx do
      let sF ← elabTermEnsuringType s propTy
      synthesizeSyntheticMVarsNoPostponing
      sides := sides.push (mkAppN (← instantiateMVars sF) xs).headBeta
    let core ←
      if (← Meta.isProp lhs) then
        if mode == "imp" then mkArrow lhs rhs else pure (mkIff lhs rhs)
      else mkEq lhs rhs
    let body ← sides.foldrM (fun s acc => mkArrow s acc) core
    mkForallFVars xs body
  let stmt ← instantiateMVars stmt
  if stmt.hasExprMVar then throwError "statement has unresolved holes"
  return stmt

syntax (name := rvEquiv) "reinvent_equiv " str ident num str term " sides " "[" term,* "]" " using " str : command

@[command_elab rvEquiv] def elabEquiv : CommandElab := fun stx => do
  let id := stx[1].isStrLit?.getD ""
  let n := stx[3].isNatLit?.getD 0
  let mode := stx[4].isStrLit?.getD "iff"
  let rhsStx := stx[5]
  let sideStx := stx[8].getSepArgs
  let simpset0 := stx[11].isStrLit?.getD ""
  -- keep only names simp can use: definitions and theorems (structures are opened by `cases`)
  let env ← getEnv
  let simpset := ", ".intercalate <| (simpset0.splitOn ", ").filter fun s =>
    match env.find? s.toName with
    | some (.defnInfo _) => true
    | some (.thmInfo _) => true
    | _ => false
  let base : List (String × Json) := [("kind", "equiv"), ("id", id), ("mode", mode)]
  let r ← liftTermElabM <| withoutErrToSorry do
    try
      let D ← resolve stx[2]
      let stmt ← buildStmt D n mode rhsStx sideStx
      let pp := (← ppExpr stmt).pretty 100
      let name := (`Reinvent.eqv).str (id ++ (if mode == "imp" then "_imp" else ""))
      let subst (t : String) := t.replace "«S»" simpset
      match ← runPortfolio name stmt (if mode == "imp" then portfolioImp else portfolioIff) subst with
      | some (lbl, ax, _) =>
        pure ([("status", "proved"), ("tactic", Json.str lbl), ("thm", Json.str name.toString),
          ("axioms", toJson (ax.map (·.toString))), ("stdAxioms", ax.all (stdAxioms.contains ·)),
          ("stmt", Json.str pp)] : List (String × Json))
      | none =>
        -- refutation attempt: the negation, by simp only
        let neg := mkNot stmt
        let rf ← runPortfolio (name.str "neg") neg
          #[("simp-false", "(intro h; simp [«S»] at h)", 40000)] subst
        pure ([("status", if rf.isSome then "refuted" else "notproved"), ("stmt", Json.str pp)] : List (String × Json))
    catch e =>
      pure ([("status", "illformed"), ("msg", Json.str ((← e.toMessageData.toString).take 300).toString)] : List (String × Json))
  liftCoreM <| out (base ++ r)

syntax (name := rvDerive) "reinvent_derive " str ident ident ident : command

@[command_elab rvDerive] def elabDerive : CommandElab := fun stx => do
  let id := stx[1].isStrLit?.getD ""
  let base : List (String × Json) := [("kind", "derive"), ("id", id)]
  let r ← liftTermElabM <| withoutErrToSorry do
    try
      let T ← resolve stx[2]
      let L ← resolve stx[3]
      let E ← resolve stx[4]
      let ci ← getConstInfo T
      let name := (`Reinvent.drv).str id
      let subst (t : String) :=
        (t.replace "«E»" E.toString).replace "«L»" ("@" ++ L.toString) |>.replace "@@" "@"
      let subst2 (t : String) := (t.replace "«E»" E.toString).replace "«L»" L.toString
      let accept (p : Expr) : Bool :=
        let cs := p.getUsedConstants
        cs.contains L && !cs.contains T
      let mut res ← runPortfolio name ci.type portfolioDerive subst2 accept
      if res.isNone then res ← runPortfolio name ci.type portfolioDerive subst accept
      match res with
      | some (lbl, ax, _) =>
        pure ([("status", "derived"), ("tactic", Json.str lbl), ("stdAxioms", ax.all (stdAxioms.contains ·)),
          ("lemma", Json.str T.toString), ("lib", Json.str L.toString)] : List (String × Json))
      | none => pure ([("status", "notderived"), ("lemma", Json.str T.toString), ("lib", Json.str L.toString)] : List (String × Json))
    catch e =>
      pure ([("status", "illformed"), ("msg", Json.str ((← e.toMessageData.toString).take 300).toString)] : List (String × Json))
  liftCoreM <| out (base ++ r)

end Reinvent
