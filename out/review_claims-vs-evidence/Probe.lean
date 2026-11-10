import Mathlib
open Lean Meta Elab Command Term

def withBudgetR (k : Nat) (x : MetaM α) : MetaM α :=
  withCurrHeartbeats <| withTheReader Core.Context (fun c => { c with maxHeartbeats := k * 1000 }) x

def tryExactR (stmt : Expr) (k : Nat) : MetaM (String × Option Name) := do
  let act : MetaM (String × Option Name) := withoutModifyingState <| withBudgetR k do
    let g ← mkFreshExprMVar stmt
    let (_, g') ← g.mvarId!.intros
    match ← LibrarySearch.librarySearch g' with
    | none =>
      let pf ← instantiateMVars (mkMVar g')
      return ("closed", pf.getAppFn.constName?)
    | some _ => return ("open", none)
  try tryCatchRuntimeEx act fun _ => pure ("timeout", none)
  catch _ => pure ("error", none)

elab "#exactq " k:num t:term : command => liftTermElabM do
  let stmt ← instantiateMVars (← elabType t)
  let t0 ← IO.monoMsNow
  let r ← tryExactR stmt k.getNat
  logInfo m!"EXACTQ budget={k.getNat}k {r.1} {r.2} ({(← IO.monoMsNow) - t0} ms) :: {stmt}"

-- same budget as Rosette/Reuse.lean (20000), then Lean's default (200000)
#exactq 20000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 20000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 200000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 20000 (∀ {s : ℝ}, -s < -1 ↔ 1 < s)
#exactq 200000 (∀ {s : ℝ}, -s < -1 ↔ 1 < s)
#exactq 20000 (∀ {s : ℝ}, 1 < s → -s < -1)
#exactq 200000 (∀ {s : ℝ}, 1 < s → -s < -1)
#exactq 200000 (∀ {E : Type} [NormedAddCommGroup E] [NormedSpace ℂ E] (P : WeakFEPair E), Continuous P.Λ₀)
#exactq 200000 (∀ {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E], MeasurableEmbedding ⇑(homeomorphUnitSphereProd E))
#exactq 200000 (∀ {V : Type} [Fintype V] {G : SimpleGraph V} [DecidableRel G.Adj] {v : V} ⦃u : V⦄, (u ∈ G.neighborFinset v) = G.Adj v u)

macro "probe" : tactic => `(tactic| first
  | (intros; rfl; trace "CLOSED rfl")
  | (intros; exact?)
  | (intros; simp; done; trace "CLOSED simp")
  | (intros; norm_num; done; trace "CLOSED norm_num")
  | (intros; push_cast; ring; trace "CLOSED push_cast; ring")
  | (intros; ring_nf; done; trace "CLOSED ring_nf")
  | (intros; congr 1; ring; trace "CLOSED congr 1; ring")
  | (intros; gcongr; exact?)
  | (intros; linarith; trace "CLOSED linarith")
  | (intros; fun_prop; trace "CLOSED fun_prop")
  | (intros; measurability; trace "CLOSED measurability")
  | (intros; grind; trace "CLOSED grind")
  | (trace "OPEN (no one-line closer found)"; sorry))

section sample
universe u
-- [0]
example {V : Type u} [Fintype V] {G : SimpleGraph V} [DecidableRel G.Adj] {v : V} ⦃u : V⦄ :
    (u ∈ G.neighborFinset v) = G.Adj v u := by probe
-- [1]
example {α 𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜] [DecidableEq α] {A : Finset α}
    {P : Finpartition A} : (A.card : 𝕜) + P.parts.card ≤ A.card + A.card := by probe
-- [2]
example {s : ℂ} : ((|(0:ℤ)| : ℤ) : ℂ) ^ s = ((0:ℕ) : ℂ) ^ s := by probe
-- [3]
example {s : ℂ} (n : ℕ) : ((|(-(n:ℤ))| : ℤ) : ℂ) ^ s = ((|(n:ℤ)| : ℤ) : ℂ) ^ s := by probe
-- [4]
example {V : Type*} (G : SimpleGraph V) {s t : V} [DecidableEq V] [Fintype V] [DecidableRel G.Adj] :
    G.edgeFinset.card + (Finset.image (fun x => s(x, t)) (G.neighborFinset s)).card - G.degree t
      = G.edgeFinset.card + G.degree s - G.degree t := by probe
-- [5]
example {T : ℝ} : MeasurableSet (Set.Ioi T) := by probe
-- [6]
example (a t : ℝ) (n : ℤ) :
    Real.exp (-Real.pi * (↑n + a) ^ 2 * t) = Real.exp (-(Real.pi * (↑n + a) ^ 2 * t)) := by probe
-- [7]
example (a : ℝ) {s : ℂ} (n : ℕ) :
    Complex.exp (2 * ↑Real.pi * Complex.I * ↑a * ↑n) / ↑n ^ s / 2
      + Complex.exp (-(2 * ↑Real.pi * Complex.I * ↑a * ↑n)) / ↑n ^ s / 2
    = (Complex.exp (2 * ↑Real.pi * Complex.I * ↑a * ↑n)
      + Complex.exp (-(2 * ↑Real.pi * Complex.I * ↑a * ↑n))) / ↑n ^ s / 2 := by probe
-- [8]
example (a : ℝ) (n : ℕ) :
    (Complex.exp (-((2 * Real.pi * a * n : ℝ) : ℂ) * Complex.I)
      - Complex.exp (((2 * Real.pi * a * n : ℝ) : ℂ) * Complex.I)) * Complex.I / 2
    = (Complex.exp (-(2 * ↑Real.pi * ↑a * ↑n) * Complex.I)
      - Complex.exp (2 * ↑Real.pi * ↑a * ↑n * Complex.I)) * Complex.I / 2 := by probe
-- [9]
example (a x : ℝ) :
    Complex.exp (-↑Real.pi * ↑a ^ 2 * ↑x) * jacobiTheta₂ (↑a * Complex.I * ↑x) (Complex.I * ↑x)
    = Complex.exp (-(↑Real.pi * ↑a ^ 2 * ↑x)) * jacobiTheta₂ (↑a * Complex.I * ↑x) (Complex.I * ↑x) := by probe
end sample

section named  -- statements the REUSE.md verdict names as the substantive residue
example : Complex.re ⁻¹' Set.Ioi 1 ∈ nhds (2:ℂ) := by probe
example : IsPreconnected ({1}ᶜ : Set ℂ) := by probe
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E] (P : WeakFEPair E) : Continuous P.Λ₀ := by probe
example {s : ℝ} : -s < -1 ↔ 1 < s := by probe
example {s : ℝ} : 1 < s → -s < -1 := by probe
example ⦃s : ℂ⦄ : 1 < s.re → s = 1 → False := by probe
example (t : ℝ) : (1:ℂ) / 2 + ↑t * Complex.I = 2⁻¹ + ↑t * Complex.I := by probe
example (k : ℕ) : 4 ^ k * 4 ^ k = (4 * 4) ^ k := by probe
example {N : ℕ} [NeZero N] (s : ℂ) : DifferentiableAt ℂ (fun x => (N:ℂ) ^ (-x)) s := by probe
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E] :
    MeasurableEmbedding ⇑(homeomorphUnitSphereProd E) := by probe
example {s : ℂ} : (∀ (n : ℕ), s ≠ 1 - ↑n) → ∀ (n : ℕ), s ≠ -↑n := by probe
end named
