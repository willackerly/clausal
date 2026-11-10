/-
Constant-threading experiment: the library.

The relation is Mathlib's own: `f =O[𝓟 S] g` (`Asymptotics.IsBigO` along the principal filter of a set `S`)
unfolds to `∃ c, ∀ x ∈ S, ‖f x‖ ≤ c * ‖g x‖` (`Asymptotics.isBigO_principal`).  The constant is uniform in
the variable that ranges over `S` (a tuple when several parameters matter) and may depend on everything
bound outside the relation.  Mathlib already supplies reflexivity, transitivity, `add`, `mul`, `pow`, `sum`,
`mono`, `comp_tendsto`, `congr'`.  This file adds what Mathlib does not have:

* part A (generic): moving between `=O[𝓟 S]` and the corpus's `∃ C, 0 ≤ C ∧ ∀ x ∈ S, … ≤ C * g x`;
  set-flavoured names for `mono`, `congr'`, `comp_tendsto`; a finite family of estimates has one constant;
  lowering the exponent of a quantity in `(0, 1]`.
* part B (the project's operations): jets of a sum, jets of a composition (the chain rule estimate),
  and the reading of the project predicate `UniformClass` as a big-O.
-/
import NavierStokes.ActualPhysicalStageBounds

noncomputable section

open Asymptotics Filter Set
open scoped Topology ContDiff

namespace Lesssim

/-! ## Part A: generic -/

section Generic

variable {X Y : Type*} {E F : Type*} [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  {S T : Set X} {f f' : X → E} {g g' : X → F}

/-- Import: a bound with an explicit constant is a big-O on the set.  No sign condition is needed. -/
theorem isBigO_of_bound_on {g : X → ℝ} (C : ℝ) (h : ∀ x ∈ S, ‖f x‖ ≤ C * g x) : f =O[𝓟 S] g :=
  IsBigO.of_bound |C| (eventually_principal.2 fun x hx =>
    (h x hx).trans ((le_abs_self _).trans (abs_mul C (g x)).le))

/-- Export (the escape hatch): where the comparison function is nonnegative, a big-O on the set gives
the corpus's explicit form with a nonnegative constant. -/
theorem exists_bound_on {g : X → ℝ} (h : f =O[𝓟 S] g) (hg : ∀ x ∈ S, 0 ≤ g x) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, ‖f x‖ ≤ C * g x := by
  obtain ⟨C, hC, hb⟩ := h.exists_nonneg
  refine ⟨C, hC, fun x hx => ?_⟩
  have := isBigOWith_principal.1 hb x hx
  rwa [Real.norm_of_nonneg (hg x hx)] at this

theorem isBigO_on_iff {g : X → ℝ} (hg : ∀ x ∈ S, 0 ≤ g x) :
    f =O[𝓟 S] g ↔ ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, ‖f x‖ ≤ C * g x :=
  ⟨fun h => exists_bound_on h hg, fun ⟨C, _, h⟩ => isBigO_of_bound_on C h⟩

theorem mono_set (h : f =O[𝓟 S] g) (hT : T ⊆ S) : f =O[𝓟 T] g :=
  h.mono (principal_mono.2 hT)

theorem congr_on (h : f =O[𝓟 S] g) (hf : EqOn f f' S) (hg : EqOn g g' S) : f' =O[𝓟 S] g' :=
  h.congr' (eventuallyEq_principal.2 hf) (eventuallyEq_principal.2 hg)

theorem congr_left_on (h : f =O[𝓟 S] g) (hf : EqOn f f' S) : f' =O[𝓟 S] g :=
  congr_on h hf fun _ _ => rfl

theorem congr_right_on (h : f =O[𝓟 S] g) (hg : EqOn g g' S) : f =O[𝓟 S] g' :=
  congr_on h (fun _ _ => rfl) hg

/-- Substitution: an estimate on `S` pulls back along any map into `S`. -/
theorem comp_mapsTo (h : f =O[𝓟 S] g) {k : Y → X} {R : Set Y} (hk : MapsTo k R S) :
    (fun y => f (k y)) =O[𝓟 R] fun y => g (k y) :=
  h.comp_tendsto (tendsto_principal_principal.2 hk)

/-- A pointwise inequality of norms on the set. -/
theorem isBigO_of_le_on (h : ∀ x ∈ S, ‖f x‖ ≤ ‖g x‖) : f =O[𝓟 S] g :=
  IsBigO.of_bound' (eventually_principal.2 h)

/-- Finitely many estimates against the same comparison function share one constant. -/
theorem exists_bound_on_finset {ι : Type*} (I : Finset ι) {A : ι → X → ℝ} {g : X → ℝ}
    (h : ∀ i ∈ I, A i =O[𝓟 S] g) (hg : ∀ x ∈ S, 0 ≤ g x) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, ∀ i ∈ I, ‖A i x‖ ≤ C * g x := by
  have hs : (fun x => ∑ i ∈ I, ‖A i x‖) =O[𝓟 S] g := IsBigO.fun_sum fun i hi => (h i hi).norm_left
  obtain ⟨C, hC, hb⟩ := exists_bound_on hs hg
  exact ⟨C, hC, fun x hx i hi => ((Finset.single_le_sum (fun j _ => norm_nonneg (A j x)) hi).trans
    (le_abs_self _)).trans (hb x hx)⟩

/-- The same for a family indexed by `j ≤ m` whose values may live in a space depending on `j`
(jets of order `j`). -/
theorem exists_bound_on_le {m : ℕ} {G : ℕ → Type*} [∀ j, SeminormedAddCommGroup (G j)]
    {A : ∀ j, X → G j} {g : X → ℝ} (h : ∀ j ≤ m, A j =O[𝓟 S] g) (hg : ∀ x ∈ S, 0 ≤ g x) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ x ∈ S, ∀ j ≤ m, ‖A j x‖ ≤ C * g x := by
  obtain ⟨C, hC, hb⟩ := exists_bound_on_finset (Finset.range (m + 1)) (A := fun j x => ‖A j x‖)
    (fun j hj => (h j (Nat.lt_succ_iff.1 (Finset.mem_range.1 hj))).norm_left) hg
  exact ⟨C, hC, fun x hx j hj =>
    (le_abs_self _).trans (hb x hx j (Finset.mem_range.2 (Nat.lt_succ_of_le hj)))⟩

/-- For a quantity in `(0, 1]`, a larger exponent is dominated by a smaller one. -/
theorem isBigO_rpow_of_le {q : X → ℝ} {r s : ℝ} (hq : ∀ x ∈ S, 0 < q x ∧ q x ≤ 1) (hsr : s ≤ r) :
    (fun x => q x ^ r) =O[𝓟 S] fun x => q x ^ s :=
  isBigO_of_bound_on 1 fun x hx => by
    rw [Real.norm_of_nonneg (Real.rpow_nonneg (hq x hx).1.le _), one_mul]
    exact Real.rpow_le_rpow_of_exponent_ge (hq x hx).1 (hq x hx).2 hsr

end Generic

/-! ## Part B: the project's operations -/

section Jets

open NavierStokes

variable {D V : Type*} [NormedAddCommGroup D] [NormedSpace ℝ D] [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- Jets of a sum: both summands smooth on an open set containing the set of uniformity. -/
theorem jet_add {U S : Set D} {f g : D → V} {k : D → ℝ} (hU : IsOpen U)
    (hf : ContDiffOn ℝ ∞ f U) (hg : ContDiffOn ℝ ∞ g U) (hS : S ⊆ U) {m : ℕ}
    (hfb : (fun x => iteratedFDeriv ℝ m f x) =O[𝓟 S] k)
    (hgb : (fun x => iteratedFDeriv ℝ m g x) =O[𝓟 S] k) :
    (fun x => iteratedFDeriv ℝ m (fun y => f y + g y) x) =O[𝓟 S] k :=
  (isBigO_of_le_on fun _ hx => (ResidualStability.norm_jet_add_le hU hf hg (hS hx) m).trans
    (le_abs_self _)).trans (hfb.norm_left.add hgb.norm_left)

/-- The chain-rule estimate as a law of the relation.  `q` is the parameter the constant is uniform in;
the outer map, the inner map, their patches and the evaluation point may all depend on it. -/
theorem jet_comp {P : Type*} {D E : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
    [NormedAddCommGroup E] [NormedSpace ℝ E] {Y : Type*} [NormedAddCommGroup Y] [NormedSpace ℝ Y]
    {T : Set P} {g : P → D → E} {φ : P → Y → D} {U : P → Set Y} {W : P → Set D} {pt : P → Y}
    (hU : ∀ q ∈ T, IsOpen (U q)) (hW : ∀ q ∈ T, IsOpen (W q))
    (hg : ∀ q ∈ T, ContDiffOn ℝ ∞ (g q) (W q)) (hφ : ∀ q ∈ T, ContDiffOn ℝ ∞ (φ q) (U q))
    (hmap : ∀ q ∈ T, MapsTo (φ q) (U q) (W q)) (hpt : ∀ q ∈ T, pt q ∈ U q)
    (m : ℕ) {A B : P → ℝ} (hA : ∀ q ∈ T, 0 ≤ A q) (hB : ∀ q ∈ T, 1 ≤ B q)
    (hgb : ∀ i ≤ m, (fun q => iteratedFDeriv ℝ i (g q) (φ q (pt q))) =O[𝓟 T] A)
    (hφb : ∀ i, 1 ≤ i → i ≤ m → (fun q => iteratedFDeriv ℝ i (φ q) (pt q)) =O[𝓟 T] B) :
    ∀ j ≤ m, (fun q => iteratedFDeriv ℝ j (g q ∘ φ q) (pt q)) =O[𝓟 T] fun q => A q * B q ^ m := by
  obtain ⟨CA, hCA, hA'⟩ := exists_bound_on_le hgb hA
  obtain ⟨CB, hCB, hB'⟩ := exists_bound_on_finset (Finset.Icc 1 m)
    (fun i hi => (hφb i (Finset.mem_Icc.1 hi).1 (Finset.mem_Icc.1 hi).2).norm_left)
    (fun q hq => zero_le_one.trans (hB q hq))
  intro j hj
  refine isBigO_of_bound_on ((m.factorial : ℝ) * CA * (max CB 1) ^ m) fun q hq => ?_
  have hB0 : 0 ≤ B q := zero_le_one.trans (hB q hq)
  refine (LocalPhysicalCopyBounds.composition_jet_bound_on (hU q hq) (hW q hq) (hg q hq) (hφ q hq)
    (hmap q hq) (hpt q hq) m (A := CA * A q) (B := max CB 1 * B q)
    (mul_nonneg hCA (hA q hq)) (one_le_mul_of_one_le_of_one_le (le_max_right _ _) (hB q hq))
    (fun i hi => hA' q hq i hi)
    (fun i h1 hi => ((le_abs_self _).trans (hB' q hq i (Finset.mem_Icc.2 ⟨h1, hi⟩))).trans
      (mul_le_mul_of_nonneg_right (le_max_left _ _) hB0)) j hj).trans_eq ?_
  rw [mul_pow]; ring

end Jets

section ProjectPredicates

open NavierStokes NavierStokes.WeightedClasses NavierStokes.LabelSumBounds

variable {D : Type} [NormedAddCommGroup D] [NormedSpace ℝ D]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] {ι : Type*}

/-- The project's `UniformClass` read as a big-O, uniform in the label, the band and the point. -/
theorem uniformClass_isBigO {s : StripData D} {w : ι → ℕ → D → ℝ} {α : ℝ} {f : ι → ℕ → D → E}
    (hf : UniformClass s w α f) (m : ℕ) :
    ∃ p : ℕ, ∀ j ≤ m, (fun ((l, n, x) : ι × ℕ × D) => iteratedFDeriv ℝ j (f l n) x)
      =O[𝓟 {q | q.2.2 ∈ s.domain}] fun (l, n, x) => s.epsilon n ^ α * s.growth n x ^ p * w l n x := by
  obtain ⟨C, -, p, hb⟩ := hf.bounds m
  refine ⟨p, fun j hj => isBigO_of_bound_on C ?_⟩
  rintro ⟨l, n, x⟩ hx
  exact (hb l n x hx j hj).trans_eq (by simp only [majorant, mul_assoc])

end ProjectPredicates

end Lesssim
