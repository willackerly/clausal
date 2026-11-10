- constants in environment: 803267
- theorems in `Mathlib.*` modules: 453756
- of which human-written by name (not auto-generated, not a `to_additive` image, not an instance): 228825
- of those, used by no other declaration: 86683; used by 1..2 declarations: 90768; used by more: 51374
- (theorem, helper) pairs: same module, theorem's proof term references helper directly, helper used by ≤ 2 declarations: 66874
- helper proof DAG size over those pairs: p10=61, p25=139, median=316, p75=760, p90=1706
- pairs with a strong signal (private or aux): 2354  (private: 1983, aux: 699, both: 328)
- pairs with no strong signal (excluded): 64520, of which prefix-only: 3178
- helper proof DAG size over strong-signal pairs: p10=202, p25=421, median=970, p75=2242, p90=4263
- eligible pairs (strong signal, helper proof ≥ 150, theorem proof ≥ 50): 2177, in 698 modules
- after module cap (1 per module): 698 (dropped 1479)
- after area cap (20 per area): 323 (dropped 375)
- **corpus size: 323 items, 323 modules, 27 areas, 323 distinct helpers, 323 distinct theorems**
- corpus helper proof DAG size: min=150, p25=612, median=1196, p75=2363, max=28876
- corpus helper statement DAG size: min=15, p25=98, median=159, p75=283, max=1925
- corpus theorem proof DAG size: min=51, p25=419, median=886, p75=2374, max=23976
- corpus helperUseCount: 1 → 236, 2 → 87

SIGNALS

| signal | eligible | corpus |
|---|---:|---:|
| `aux` | 107 | 7 |
| `aux+prefix` | 35 | 16 |
| `aux+prefix+sole_use` | 131 | 43 |
| `aux+sole_use` | 80 | 11 |
| `private` | 614 | 44 |
| `private+aux` | 89 | 6 |
| `private+aux+prefix` | 10 | 4 |
| `private+aux+prefix+sole_use` | 98 | 32 |
| `private+aux+sole_use` | 109 | 29 |
| `private+prefix` | 32 | 10 |
| `private+prefix+sole_use` | 131 | 44 |
| `private+sole_use` | 741 | 77 |

AREAS

| area | eligible pairs | dropped by module cap | dropped by area cap | corpus items |
|---|---:|---:|---:|---:|
| Algebra | 140 | 85 | 35 | 20 |
| AlgebraicGeometry | 90 | 64 | 6 | 20 |
| AlgebraicTopology | 27 | 19 | 0 | 8 |
| Analysis | 342 | 227 | 95 | 20 |
| Basic | 10 | 7 | 0 | 3 |
| CategoryTheory | 86 | 49 | 17 | 20 |
| Combinatorics | 157 | 119 | 18 | 20 |
| Computability | 11 | 6 | 0 | 5 |
| Condensed | 9 | 8 | 0 | 1 |
| Data | 66 | 41 | 5 | 20 |
| Dynamics | 3 | 1 | 0 | 2 |
| FieldTheory | 70 | 56 | 0 | 14 |
| Geometry | 64 | 42 | 2 | 20 |
| GroupTheory | 37 | 25 | 0 | 12 |
| InformationTheory | 8 | 6 | 0 | 2 |
| LinearAlgebra | 120 | 68 | 32 | 20 |
| Logic | 2 | 1 | 0 | 1 |
| MeasureTheory | 123 | 78 | 25 | 20 |
| ModelTheory | 28 | 25 | 0 | 3 |
| NumberTheory | 380 | 298 | 62 | 20 |
| Order | 14 | 9 | 0 | 5 |
| Probability | 40 | 23 | 0 | 17 |
| RepresentationTheory | 1 | 0 | 0 | 1 |
| RingTheory | 228 | 143 | 65 | 20 |
| SetTheory | 14 | 8 | 0 | 6 |
| Tactic | 19 | 16 | 0 | 3 |
| Topology | 88 | 55 | 13 | 20 |

SAMPLE

### 1. `Polynomial.add_divByMonic_modByMonic` used in `Polynomial.add_divByMonic`

- module `Mathlib.Algebra.Polynomial.Div`; signal `private+prefix`; helper proof size 909 (tree 32645); helper statement size 98; theorem proof size 105; helper use count 2

Helper statement:

```lean
∀ {R : Type u} [inst : CommRing R] {q : Polynomial R} (p₁ p₂ : Polynomial R),
  (p₁ + p₂) /ₘ q = p₁ /ₘ q + p₂ /ₘ q ∧ (p₁ + p₂) %ₘ q = p₁ %ₘ q + p₂ %ₘ q
```

Theorem statement:

```lean
∀ {R : Type u} [inst : CommRing R] {q : Polynomial R} (p₁ p₂ : Polynomial R),
  (p₁ + p₂) /ₘ q = p₁ /ₘ q + p₂ /ₘ q
```

### 2. `AnalyticOnNhd.eqOn_zero_of_preconnected_of_eventuallyEq_zero_aux` used in `AnalyticOnNhd.eqOn_zero_of_preconnected_of_eventuallyEq_zero`

- module `Mathlib.Analysis.Analytic.Uniqueness`; signal `aux+prefix+sole_use`; helper proof size 3368 (tree 17264); helper statement size 189; theorem proof size 1983; helper use count 1

Helper statement:

```lean
∀ {𝕜 : Type u_1} [inst : NontriviallyNormedField 𝕜] {E : Type u_2} [inst_1 : NormedAddCommGroup E]
  [inst_2 : NormedSpace 𝕜 E] {F : Type u_3} [inst_3 : NormedAddCommGroup F]
  [inst_4 : NormedSpace 𝕜 F] [CompleteSpace F] {f : E → F} {U : Set E},
  AnalyticOnNhd 𝕜 f U → IsPreconnected U → ∀ {z₀ : E}, z₀ ∈ U → f =ᶠ[nhds z₀] 0 → Set.EqOn f 0 U
```

Theorem statement:

```lean
∀ {𝕜 : Type u_1} [inst : NontriviallyNormedField 𝕜] {E : Type u_2} [inst_1 : NormedAddCommGroup E]
  [inst_2 : NormedSpace 𝕜 E] {F : Type u_3} [inst_3 : NormedAddCommGroup F]
  [inst_4 : NormedSpace 𝕜 F] {f : E → F} {U : Set E},
  AnalyticOnNhd 𝕜 f U → IsPreconnected U → ∀ {z₀ : E}, z₀ ∈ U → f =ᶠ[nhds z₀] 0 → Set.EqOn f 0 U
```

### 3. `CategoryTheory.Limits.SequentialProduct.functorMap_commSq_aux` used in `CategoryTheory.Limits.SequentialProduct.functorMap_commSq`

- module `Mathlib.CategoryTheory.Limits.Shapes.SequentialProduct`; signal `aux+prefix+sole_use`; helper proof size 2592 (tree 162817); helper statement size 283; theorem proof size 2531; helper use count 1

Helper statement:

```lean
∀ {C : Type u_1} {M N : ℕ → C} [inst : CategoryTheory.Category.{v_1, u_1} C]
  (f : (n : ℕ) → M n ⟶ N n) [inst_1 : CategoryTheory.Limits.HasCountableProducts C] {n m k : ℕ}
  (h : n ≤ m) (hh : ¬k < m),
  CategoryTheory.CategoryStruct.comp
      ((CategoryTheory.Functor.ofOpSequence
            (CategoryTheory.Limits.SequentialProduct.functorMap f)).map
        (CategoryTheory.homOfLE h).op)
      (CategoryTheory.CategoryStruct.comp
        (CategoryTheory.Limits.Pi.π
          (fun m => if x : m < Opposite.unop (Opposite.op n) then M m else N m) k)
        (CategoryTheory.eqToHom ⋯)) =
    CategoryTheory.CategoryStruct.comp
      (CategoryTheory.Limits.Pi.π (fun i => if x : i < m then M i else N i) k)
      (CategoryTheory.eqToHom ⋯)
```

Theorem statement:

```lean
∀ {C : Type u_1} {M N : ℕ → C} [inst : CategoryTheory.Category.{v_1, u_1} C]
  (f : (n : ℕ) → M n ⟶ N n) [inst_1 : CategoryTheory.Limits.HasCountableProducts C] {n m : ℕ}
  (h : ¬m < n),
  CategoryTheory.CategoryStruct.comp
      ((CategoryTheory.Functor.ofOpSequence
            (CategoryTheory.Limits.SequentialProduct.functorMap f)).map
        (CategoryTheory.homOfLE ⋯).op)
      (CategoryTheory.CategoryStruct.comp
        (CategoryTheory.Limits.Pi.π
          (fun m => if x : m < Opposite.unop (Opposite.op n) then M m else N m) m)
        (CategoryTheory.eqToHom ⋯)) =
    CategoryTheory.CategoryStruct.comp
      (CategoryTheory.Limits.Pi.π (fun i => if x : i < m + 1 then M i else N i) m)
      (CategoryTheory.CategoryStruct.comp (CategoryTheory.eqToHom ⋯) (f m))
```

### 4. `Partrec.fix_aux` used in `Partrec.fix`

- module `Mathlib.Computability.Partrec`; signal `aux+prefix+sole_use`; helper proof size 2579 (tree 32921); helper statement size 160; theorem proof size 1700; helper use count 1

Helper statement:

```lean
∀ {α : Type u_5} {σ : Type u_6} (f : α →. σ ⊕ α) (a : α) (b : σ),
  have F := fun a n =>
    Nat.rec (Part.some (Sum.inr a))
      (fun x IH => IH.bind fun s => Sum.casesOn s (fun x => Part.some s) f) n;
  (∃ n,
      ((∃ b', Sum.inl b' ∈ F a n) ∧ ∀ {m : ℕ}, m < n → ∃ b, Sum.inr b ∈ F a m) ∧
        Sum.inl b ∈ F a n) ↔
    b ∈ f.fix a
```

Theorem statement:

```lean
∀ {α : Type u_1} {σ : Type u_4} [inst : Primcodable α] [inst_1 : Primcodable σ] {f : α →. σ ⊕ α},
  Partrec f → Partrec f.fix
```

### 5. `X_pow_sub_C_eq_prod'` used in `X_pow_sub_C_eq_prod`

- module `Mathlib.FieldTheory.KummerExtension`; signal `private+prefix+sole_use`; helper proof size 689 (tree 23945); helper statement size 261; theorem proof size 1915; helper use count 1

Helper statement:

```lean
∀ {K : Type u} [inst : Field K] {n : ℕ} {ζ : K},
  IsPrimitiveRoot ζ n →
    ∀ {α a : K},
      0 < n →
        α ^ n = a →
          Polynomial.X ^ n - Polynomial.C a =
            ∏ i ∈ Finset.range n, (Polynomial.X - Polynomial.C (ζ ^ i * α))
```

Theorem statement:

```lean
∀ {R : Type u_1} [inst : CommRing R] [IsDomain R] {n : ℕ} {ζ : R},
  IsPrimitiveRoot ζ n →
    ∀ {α a : R},
      0 < n →
        α ^ n = a →
          Polynomial.X ^ n - Polynomial.C a =
            ∏ i ∈ Finset.range n, (Polynomial.X - Polynomial.C (ζ ^ i * α))
```

### 6. `FreeGroup.Red.Step.diamond_aux` used in `FreeGroup.Red.Step.diamond`

- module `Mathlib.GroupTheory.FreeGroup.Basic`; signal `aux+prefix+sole_use`; helper proof size 204 (tree 711); helper statement size 127; theorem proof size 186; helper use count 1

Helper statement:

```lean
∀ {α : Type u} {L₁ L₂ L₃ L₄ : List (α × Bool)} {x1 : α} {b1 : Bool} {x2 : α} {b2 : Bool},
  L₁ ++ (x1, b1) :: (x1, !b1) :: L₂ = L₃ ++ (x2, b2) :: (x2, !b2) :: L₄ →
    L₁ ++ L₂ = L₃ ++ L₄ ∨ ∃ L₅, FreeGroup.Red.Step (L₁ ++ L₂) L₅ ∧ FreeGroup.Red.Step (L₃ ++ L₄) L₅
```

Theorem statement:

```lean
∀ {α : Type u} {L₁ L₂ L₃ L₄ : List (α × Bool)},
  FreeGroup.Red.Step L₁ L₃ →
    FreeGroup.Red.Step L₂ L₄ →
      L₁ = L₂ → L₃ = L₄ ∨ ∃ L₅, FreeGroup.Red.Step L₃ L₅ ∧ FreeGroup.Red.Step L₄ L₅
```

### 7. `MeasureTheory.Measure.toSphere_apply_aux` used in `MeasureTheory.Measure.measurePreserving_homeomorphUnitSphereProd`

- module `Mathlib.MeasureTheory.Constructions.HaarToSphere`; signal `aux`; helper proof size 1134 (tree 159815); helper statement size 391; theorem proof size 2928; helper use count 2

Helper statement:

```lean
∀ {E : Type u_1} [inst : NormedAddCommGroup E] [inst_1 : NormedSpace ℝ E]
  [inst_2 : MeasurableSpace E] (μ : MeasureTheory.Measure E) (s : Set ↑(Metric.sphere 0 1))
  (r : ↑(Set.Ioi 0)),
  μ (Subtype.val '' ⇑(homeomorphUnitSphereProd E) ⁻¹' s ×ˢ Set.Iio r) =
    μ (Set.Ioo 0 ↑r • Subtype.val '' s)
```

Theorem statement:

```lean
∀ {E : Type u_1} [inst : NormedAddCommGroup E] [inst_1 : NormedSpace ℝ E]
  [inst_2 : MeasurableSpace E] (μ : MeasureTheory.Measure E) [BorelSpace E] [FiniteDimensional ℝ E]
  [μ.IsAddHaarMeasure],
  MeasureTheory.MeasurePreserving (⇑(homeomorphUnitSphereProd E))
    (MeasureTheory.Measure.comap Subtype.val μ)
    (μ.toSphere.prod (MeasureTheory.Measure.volumeIoiPow (Module.finrank ℝ E - 1)))
```

### 8. `UpperHalfPlane.hasSum_cuspFunction_of_hasSum_punctured` used in `UpperHalfPlane.tendsto_atImInfty_of_hasSum_qExpansion`

- module `Mathlib.NumberTheory.ModularForms.QExpansion`; signal `private`; helper proof size 245 (tree 803); helper statement size 148; theorem proof size 481; helper use count 2

Helper statement:

```lean
∀ {h : ℝ} {f : UpperHalfPlane → ℂ},
  0 < h →
    ∀ {c : ℕ → ℂ},
      (∀ (τ : UpperHalfPlane), HasSum (fun m => c m • Function.Periodic.qParam h ↑τ ^ m) (f τ)) →
        ∀ {q : ℂ},
          ‖q‖ < 1 → q ≠ 0 → HasSum (fun m => c m • q ^ m) (UpperHalfPlane.cuspFunction h f q)
```

Theorem statement:

```lean
∀ {h : ℝ} {f : UpperHalfPlane → ℂ} {c : ℕ → ℂ},
  0 < h →
    (∀ (τ : UpperHalfPlane), HasSum (fun m => c m • Function.Periodic.qParam h ↑τ ^ m) (f τ)) →
      Filter.Tendsto f UpperHalfPlane.atImInfty (nhds (c 0))
```

### 9. `AdicCompletion.ofValEqZeroAux_exists` used in `AdicCompletion.ofValEqZeroAux_prop`

- module `Mathlib.RingTheory.AdicCompletion.Completeness`; signal `private`; helper proof size 1899 (tree 817910); helper statement size 1355; theorem proof size 1369; helper use count 2

Helper statement:

```lean
∀ {R : Type u_1} [inst : CommRing R] (I : Ideal R) {M : Type u_2} [inst_1 : AddCommGroup M]
  [inst_2 : _root_.Module R M] {a b c : ℕ} {x : AdicCompletion I M} (h : c = b + a),
  ↑x a = 0 → ∃ t, (Submodule.powSMulQuotInclusion I M h ⊤) t = ↑x c
```

Theorem statement:

```lean
∀ {R : Type u_1} [inst : CommRing R] (I : Ideal R) {M : Type u_2} [inst_1 : AddCommGroup M]
  [inst_2 : _root_.Module R M] {a b c : ℕ} {x : AdicCompletion I M} (h : c = b + a) (ha : ↑x a = 0),
  (Submodule.powSMulQuotInclusion I M h ⊤) (AdicCompletion.ofValEqZeroAux I h ha) = ↑x c
```

### 10. `Valuation.embedding_valueGroup₀ExtensionHomFun` used in `Valuation.embedding_valueGroup₀ExtensionHom`

- module `Mathlib.Topology.Algebra.ValuativeRel.Completion`; signal `private+prefix`; helper proof size 1184 (tree 175749); helper statement size 460; theorem proof size 143; helper use count 2

Helper statement:

```lean
∀ {K : Type u_2} {Γ₀ : Type u_3} [inst : Field K] [inst_1 : ValuativeRel K]
  [inst_2 : UniformSpace K] [inst_3 : IsValuativeTopology K]
  [inst_4 : LinearOrderedCommGroupWithZero Γ₀] (v : Valuation K Γ₀) [inst_5 : v.Compatible]
  [inst_6 : IsUniformAddGroup K] (a : (↑v).ValueGroup₀),
  MonoidWithZeroHom.ValueGroup₀.embedding (Valuation.valueGroup₀ExtensionHomFun✝ v a) =
    MonoidWithZeroHom.ValueGroup₀.embedding a
```

Theorem statement:

```lean
∀ {K : Type u_2} {Γ₀ : Type u_3} [inst : Field K] [inst_1 : ValuativeRel K]
  [inst_2 : UniformSpace K] [inst_3 : IsValuativeTopology K]
  [inst_4 : LinearOrderedCommGroupWithZero Γ₀] (v : Valuation K Γ₀) [inst_5 : v.Compatible]
  [inst_6 : IsUniformAddGroup K] (a : (↑v).ValueGroup₀),
  MonoidWithZeroHom.ValueGroup₀.embedding (v.valueGroup₀ExtensionHom a) =
    MonoidWithZeroHom.ValueGroup₀.embedding a
```

