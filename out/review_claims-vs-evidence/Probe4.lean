import Mathlib
open Lean Meta Elab Command Term

def withBudgetR (k : Nat) (x : MetaM α) : MetaM α :=
  withCurrHeartbeats <| withTheReader Core.Context (fun c => { c with maxHeartbeats := k * 1000 }) x

/-- as in Rosette/Reuse.lean (`fixed = false`) or with the search run in the goal's context. -/
def tryExactR (stmt : Expr) (k : Nat) (fixed : Bool) : MetaM (String × Option Name) := do
  let act : MetaM (String × Option Name) := withoutModifyingState <| withBudgetR k do
    let g ← mkFreshExprMVar stmt
    let (_, g') ← g.mvarId!.intros
    let r ← if fixed then g'.withContext (LibrarySearch.librarySearch g') else LibrarySearch.librarySearch g'
    match r with
    | none =>
      let pf ← instantiateMVars (mkMVar g')
      return ("closed", pf.getAppFn.constName?)
    | some _ => return ("open", none)
  try tryCatchRuntimeEx act fun ex => do
        let msg ← ex.toMessageData.toString
        pure ("EXCEPTION[" ++ (msg.take 120).toString ++ "]", none)
  catch _ => pure ("error", none)

elab "#exactq " t:term : command => liftTermElabM do
  let stmt ← instantiateMVars (← elabType t)
  let a ← tryExactR stmt 20000 false
  let t0 ← IO.monoMsNow
  let b ← tryExactR stmt 20000 true
  logInfo m!"EXACTQ as-shipped: {a.1} | in goal context, same 20000k budget: {b.1} {b.2} ({(← IO.monoMsNow) - t0} ms) :: {stmt}"


-- labelled "open" in out/reuse/statements.jsonl (binder statements)
#exactq (∀ (n : ℤ), ((Real.pi * (n:ℝ) ^ 2 : ℝ) : ℂ) = (Real.pi : ℂ) * (n:ℂ) ^ 2)
#exactq (∀ {V : Type} (x y x_1 : V), (x_1 = y ∧ x = x) = (x_1 = y))
#exactq (∀ {α : Type} (x : Finset α), (0 < (x.card : ℝ)) = (0 < x.card))
#exactq (∀ {q : ℕ}, ((q.totient : ℂ) = ((0:ℕ):ℂ)) = (q.totient = 0))
#exactq (∀ ⦃s : ℂ⦄, 1 < s.re → s = 1 → False)
#exactq (∀ (t : ℝ), (1:ℂ) / 2 + ↑t * Complex.I = 2⁻¹ + ↑t * Complex.I)
-- labelled "closed"
#exactq (∀ {α : Type} [Fintype α] [DecidableEq α] {P : Finpartition (Finset.univ : Finset α)}, (4 * 4) ^ P.parts.card = 4 ^ P.parts.card * 4 ^ P.parts.card)
#exactq (∀ (y : ℂ), 0 + (y ^ 1 * 1 + 0) = y ^ 1 * 1 + 0)
