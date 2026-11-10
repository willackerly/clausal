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

#exactq (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq (∀ {s : ℝ}, -s < -1 ↔ 1 < s)
#exactq (∀ {s : ℝ}, 1 < s → -s < -1)
#exactq (∀ {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E], MeasurableEmbedding ⇑(homeomorphUnitSphereProd E))
#exactq (∀ {α 𝕜 : Type} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜] [DecidableEq α] {A : Finset α} {P : Finpartition A}, (A.card : 𝕜) + P.parts.card ≤ A.card + A.card)
#exactq (∀ {E : Type} [NormedAddCommGroup E] [NormedSpace ℂ E] (P : WeakFEPair E), Continuous P.Λ₀)
#exactq (∀ {N : ℕ} [NeZero N] (s : ℂ), DifferentiableAt ℂ (fun x => (N:ℂ) ^ (-x)) s)
#exactq (∀ (a b : ℕ), a + b = b + a)
#exactq (∀ (t : ℝ) (n : ℤ), -Real.pi * ↑n ^ 2 * t = -(Real.pi * ↑n ^ 2) * t)
#exactq (∀ {V : Type} [Fintype V] {G : SimpleGraph V} [DecidableRel G.Adj] {v : V} ⦃u : V⦄, (u ∈ G.neighborFinset v) = G.Adj v u)
