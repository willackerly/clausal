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
  try tryCatchRuntimeEx act fun ex => do
        let msg ← ex.toMessageData.toString
        pure ("EXCEPTION[" ++ (msg.take 300).toString ++ "]", none)
  catch _ => pure ("error", none)

elab "#exactq " k:num t:term : command => liftTermElabM do
  let stmt ← instantiateMVars (← elabType t)
  let t0 ← IO.monoMsNow
  let r ← tryExactR stmt k.getNat
  logInfo m!"EXACTQ budget={k.getNat}k {r.1} {r.2} ({(← IO.monoMsNow) - t0} ms) :: {stmt}"

#exactq 20000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 200000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 2000000 (∀ {T : ℝ}, MeasurableSet (Set.Ioi T))
#exactq 20000 (∀ {s : ℝ}, -s < -1 ↔ 1 < s)
#exactq 2000000 (∀ {s : ℝ}, -s < -1 ↔ 1 < s)
#exactq 2000000 (∀ {s : ℝ}, 1 < s → -s < -1)
#exactq 2000000 (∀ {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E], MeasurableEmbedding ⇑(homeomorphUnitSphereProd E))
#exactq 20000 (∀ (k : ℕ), 4 ^ k * 4 ^ k = (4 * 4) ^ k)
#exactq 20000 ((3:ℕ) = 3)
#exactq 20000 (∀ (a b : ℕ), a + b = b + a)

macro "probe" : tactic => `(tactic| first
  | (intros; rfl; trace "CLOSED rfl")
  | (intros; exact?)
  | (intros; simp; done; trace "CLOSED simp")
  | (intros; norm_num; done; trace "CLOSED norm_num")
  | (intros; push_cast; ring1; trace "CLOSED push_cast; ring1")
  | (intros; congr 1; ring1; trace "CLOSED congr 1; ring1")
  | (intros; gcongr; exact?)
  | (intros; linarith; trace "CLOSED linarith")
  | (intros; fun_prop; trace "CLOSED fun_prop")
  | (intros; measurability; trace "CLOSED measurability")
  | (intros; grind; trace "CLOSED grind")
  | (trace "OPEN (no one-line closer found)"; sorry))

section sample
universe u
example {V : Type u} [Fintype V] {G : SimpleGraph V} [DecidableRel G.Adj] {v : V} ⦃u : V⦄ :
    (u ∈ G.neighborFinset v) = G.Adj v u := by trace "[0]"; probe
example {α 𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜] [DecidableEq α] {A : Finset α}
    {P : Finpartition A} : (A.card : 𝕜) + P.parts.card ≤ A.card + A.card := by trace "[1]"; probe
example {s : ℂ} : ((|(0:ℤ)| : ℤ) : ℂ) ^ s = ((0:ℕ) : ℂ) ^ s := by trace "[2]"; probe
example {s : ℂ} (n : ℕ) : ((|(-(n:ℤ))| : ℤ) : ℂ) ^ s = ((|(n:ℤ)| : ℤ) : ℂ) ^ s := by trace "[3]"; probe
example {V : Type*} (G : SimpleGraph V) {s t : V} [DecidableEq V] [Fintype V] [DecidableRel G.Adj] :
    G.edgeFinset.card + (Finset.image (fun x => s(x, t)) (G.neighborFinset s)).card - G.degree t
      = G.edgeFinset.card + G.degree s - G.degree t := by trace "[4]"; probe
-- [4] second attempt: one library lemma + injectivity
example {V : Type*} (G : SimpleGraph V) {s t : V} [DecidableEq V] [Fintype V] [DecidableRel G.Adj] :
    G.edgeFinset.card + (Finset.image (fun x => s(x, t)) (G.neighborFinset s)).card - G.degree t
      = G.edgeFinset.card + G.degree s - G.degree t := by
  trace "[4b]"
  rw [Finset.card_image_of_injective _ (fun a b h => by simpa using h), SimpleGraph.card_neighborFinset_eq_degree]
example {T : ℝ} : MeasurableSet (Set.Ioi T) := by trace "[5]"; probe
example (a t : ℝ) (n : ℤ) :
    Real.exp (-Real.pi * (↑n + a) ^ 2 * t) = Real.exp (-(Real.pi * (↑n + a) ^ 2 * t)) := by trace "[6]"; probe
example (a : ℝ) {s : ℂ} (n : ℕ) :
    Complex.exp (2 * ↑Real.pi * Complex.I * ↑a * ↑n) / ↑n ^ s / 2
      + Complex.exp (-(2 * ↑Real.pi * Complex.I * ↑a * ↑n)) / ↑n ^ s / 2
    = (Complex.exp (2 * ↑Real.pi * Complex.I * ↑a * ↑n)
      + Complex.exp (-(2 * ↑Real.pi * Complex.I * ↑a * ↑n))) / ↑n ^ s / 2 := by trace "[7]"; probe
example (a : ℝ) (n : ℕ) :
    (Complex.exp (-((2 * Real.pi * a * n : ℝ) : ℂ) * Complex.I)
      - Complex.exp (((2 * Real.pi * a * n : ℝ) : ℂ) * Complex.I)) * Complex.I / 2
    = (Complex.exp (-(2 * ↑Real.pi * ↑a * ↑n) * Complex.I)
      - Complex.exp (2 * ↑Real.pi * ↑a * ↑n * Complex.I)) * Complex.I / 2 := by trace "[8]"; probe
example (a x : ℝ) :
    Complex.exp (-↑Real.pi * ↑a ^ 2 * ↑x) * jacobiTheta₂ (↑a * Complex.I * ↑x) (Complex.I * ↑x)
    = Complex.exp (-(↑Real.pi * ↑a ^ 2 * ↑x)) * jacobiTheta₂ (↑a * Complex.I * ↑x) (Complex.I * ↑x) := by trace "[9]"; probe
end sample

section named
example : Complex.re ⁻¹' Set.Ioi 1 ∈ nhds (2:ℂ) := by trace "[n1]"; probe
example : Complex.re ⁻¹' Set.Ioi 1 ∈ nhds (2:ℂ) := by
  trace "[n1b]"; exact Complex.continuous_re.continuousAt.preimage_mem_nhds (Ioi_mem_nhds (by norm_num))
example : IsPreconnected ({1}ᶜ : Set ℂ) := by trace "[n2]"; probe
example : IsPreconnected ({1}ᶜ : Set ℂ) := by
  trace "[n2b]"; exact (isConnected_compl_singleton_of_one_lt_rank (by simp) _).isPreconnected
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E] (P : WeakFEPair E) : Continuous P.Λ₀ := by trace "[n3]"; probe
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E] (P : WeakFEPair E) : Continuous P.Λ₀ := by
  trace "[n3b]"; exact P.differentiable_Λ₀.continuous
example {s : ℝ} : -s < -1 ↔ 1 < s := by trace "[n4]"; probe
example {s : ℝ} : 1 < s → -s < -1 := by trace "[n5]"; probe
example ⦃s : ℂ⦄ : 1 < s.re → s = 1 → False := by trace "[n6]"; probe
example (t : ℝ) : (1:ℂ) / 2 + ↑t * Complex.I = 2⁻¹ + ↑t * Complex.I := by trace "[n7]"; probe
example (k : ℕ) : 4 ^ k * 4 ^ k = (4 * 4) ^ k := by trace "[n8]"; probe
example {N : ℕ} [NeZero N] (s : ℂ) : DifferentiableAt ℂ (fun x => (N:ℂ) ^ (-x)) s := by trace "[n9]"; probe
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E] [BorelSpace E] :
    MeasurableEmbedding ⇑(homeomorphUnitSphereProd E) := by trace "[n10]"; probe
example {s : ℂ} : (∀ (n : ℕ), s ≠ 1 - ↑n) → ∀ (n : ℕ), s ≠ -↑n := by trace "[n11]"; probe
example {s : ℂ} : (∀ (n : ℕ), s ≠ 1 - ↑n) → ∀ (n : ℕ), s ≠ -↑n := by
  trace "[n11b]"; intro h n; simpa using h (n + 1)
end named
