# M9 families: wide-aperture clustering of definitions (ns, with Carleson and PFR beside it)

2026-11-11. Tool: `tools/families/` (one Lean program run read-only against each project's built `.olean` files, plus Python). One command: `tools/families/run.sh`. No corpus file was modified or rebuilt. This is the clustering step of M9 only: nothing here has been generalised in Lean, so **no family below is known to have a correct common generalisation**. Skeletons are syntactic. A line marked *reading* is a model's reading and is not evidence.

**Exploratory.** Thresholds, the lemma-role channel and the score were fixed while looking at the ns output (see "What was changed after looking" at the end of this section). The directory is not under version control, so rule 1 of the plan (frozen before data) is not met.

## Result

Universe: 13,043 definitions and structures in ns; 9,903 are reachable from the four headline theorems (dead-code tool) and are what is clustered. Carleson 401, PFR 52.

1. **A quarter to a half of the definitions fall in some family once the match is loose, but most of that is not subtle.**
   - Exact body up to bound names (L0): 1,025 definitions in 275 families; replacing each family by one definition removes 750 (7.6%). 452 of those are type abbreviations (`Point := ℝ × (ℝ × ℝ) × (ℝ × ℝ)` under 75 names, `ℝ × ℝ` under 60), 291 are values or functions, 7 are propositions.
   - Numerals and leaf constants abstracted (L1, L2): 806 and 874 removable. The owner's leading example, definitions that differ in an exponent or an index, adds 806 − 750 = 56 definitions at L1.
   - Project constants in head position abstracted (L3): 2,090 in 698 families, 1,392 removable (14.1%).
   - Anti-unification, at most 30% of a member inside compound holes (AU@0.7): 4,307 in 1,392 families, 2,915 removable (29.4%). Requiring a shared skeleton of at least four nodes: 2,739 in 1,055, 1,684 removable (17.0%). The difference is families like "a product of two types" and "one function applied to one argument".
   - At AU@0.5, 5,925 definitions (42% removable on paper) are in a family and the largest has 129 members; by then the skeletons are a few nodes.
2. **Families with one simple parameter are the rule, independent parameters the exception.** Of the 1,392 AU@0.7 families, 136 have no hole, 983 have one effective parameter and 273 have two or more. 851 have two or more holes, and in 69 of them the holes vary independently; in the rest every hole changes together (one index, such as radial / angular / axial, picks all of them). 101 families have a hole that depends on a bound variable (the parameter would be a function), 658 have a compound hole. Kinds of hole: mixed 1,553, head 1,487, parameter 631, term 235, numeral 182, type 58, function 47, constant 29, set 11, prop 9, boundvar 1 ("head" is a function symbol in head position, "mixed" is a hole filled by different kinds in different members, most often a parameter in one and a constant in another).
3. **Parallel lemma families are small.** 3,812 of 24,778 reachable theorems that mention a definition (15.4%) have a statement also proved, hole for hole, about a different definition. Families whose members have at least two identical lemma shapes (API@2): 879 definitions in 380 families, largest 9. Same body (AU@0.7) *and* at least two identical lemma shapes: 288 definitions in 137 families, largest 6; a parameterised version of each would remove 151 definitions and 499 lemma statements by this count, 134 of the 137 with at most one effective parameter. That is the set where "same body, same lemmas, one parameter" holds on the evidence here: 1.5% of definitions.
4. **The class-like families exist, and only the lemma-role channel sees them.** 283 of the 340 ROLE@0.25 families (732 definitions) have no common body: their members are written differently and proved to have the same closure laws (`add`, `sub`, `neg`, `mul`, `smul`, `map`, `fderiv`). 18 role families of three or more consist only of predicates. The largest is 15 predicates (family 10 below); `MemClass`, `UniformClass`, `LocalClass` and `LocalJets` are another (family 53). A parameter cannot merge these; a structure or type class stating the closure laws could. Whether it would pay is the LESSSIM question and is not answered here.
5. **The corpus already wrote many of the general forms and then named the instances.** 475 definitions have two or more named specialisations (1,487 specialisations in all, 15.0% of definitions): a definition whose body is another project definition applied to arguments. `WaveClass`, `MeanClass` and `UnweightedClass` are `MemClass` at three weights. For these the generalisation exists and the concept count is in the names.
6. **Human projects, same tool.** Removable at L0: Carleson 5 (1.2%), PFR 0. At L3: Carleson 39 (9.7%), PFR 2 (3.8%); with a body of at least four nodes Carleson 34 (8.5%). Carleson's largest L1 family is the owner's example exactly: seven named constants `2 ^ ((𝕔 + n + 𝕔 / k) * a ^ 3)` that differ in two numerals; the authors kept them as separate named constants. AU@0.7 with skeleton ≥ 4: Carleson 53 (13.2%), PFR 2. Theorems with a statement shape also proved about another definition: Carleson 10.9%, PFR 0.9% (ns 15.4%). Named specialisations: Carleson 13 (3.2%), PFR 2. So verbatim duplication of definitions and naming of instances are specific to the machine corpus; loose structural similarity is not (Carleson reaches 23% at AU@0.7 against 29%).
7. **Controls.** Planted families: 4 of 4 as expected. Known cases, no names supplied: the `MemClass` family surfaces as a specialisation family (rank 46 of 4,178) and, with `UniformClass`, as a role family (rank 79); `JetRate` pairs with `FiniteJetRate` by three identical lemma shapes (rank 2,076) and with `UnweightedClass` by roles (rank 783); every definition of the near-identical cloned modules is matched to its original at L3, but only in the run that includes dead code. Details and the misses in section 3.

*Reading (model, not evidence).* The idea is worth one more step, aimed differently from how it was posed. The fuzzy matcher finds families easily; what it mostly finds is (a) the same type or value under many local names, and (b) instances of a general definition the corpus already has. Both reduce concept count by deleting names, with no new abstraction and no effect on proofs. The case the idea is about, a slightly more flexible primitive replacing subtly different definitions together with their lemmas, is supported for about 137 small families by body and for a few dozen predicate families by role, and the second group is the one where "behaving like a class" is the right description. The next step should take a handful of those through Lean and measure concept count, proof size and elaboration cost, because nothing above says the generalisations are true or cheap.

### What was changed after looking at ns output

- The lemma-role channel was added after the first run: identical lemma shapes gave `MemClass` and `UniformClass` no shape in common (every `UniformClass` lemma carries an extra index), although both were known controls. So the role channel was designed knowing this case, and its finding them is not an independent test. The planted family B is; it was written afterwards with its expectation.
- Statements that mention two members of a pair are not counted as parallel lemmas. Without this the role channel's largest families were definitions that always appear together in one statement.
- Types are excluded from the role channel (a type is "mentioned" by every theorem that quantifies over it).
- The role-based lemma count was made conservative (one lemma per further member and role) after the first version produced estimates in the thousands.
- AU levels 1.0 to 0.5, the top-60 neighbour search and the penalties in the score were chosen by hand and not tuned against a target.


## 1. What was clustered

| | ns (machine) | Carleson | PFR |
|---|---:|---:|---:|
| definitions and structures exported | 13,043 | 481 | 138 |
| dropped: syntax / metaprogramming | 0 | 26 | 75 |
| dropped: body over 4000 nodes | 0 | 0 | 0 |
| definitions and structures kept (all) | 13,043 | 455 | 63 |
| … not in the dead-code export (auxiliary definitions Lean generated) | 712 | 34 | 6 |
| … reachable from the headline theorems | 9,903 | 401 | 52 |
| theorems with a statement tree | 44,009 | 2,664 | 1,050 |
| … reachable | 25,715 | 1,968 | 773 |
| theorem statements over the node limit (not profiled) | 7 | 16 | 0 |
| definitions with ≥ 1 reachable theorem stated about them | 8,941 | 384 | 49 |

Reachable definitions by result: ns: 848 type, 497 proposition, 8,558 value or function; Carleson: 30 proposition, 351 value or function, 20 type; PFR: 37 value or function, 12 proposition, 3 type.
"Not in the dead-code export" are `ctorIdx`, `noConfusionType` and similar definitions Lean generates for each structure; they are not declarations a reader meets and are counted as unreachable. Instances (25 in ns) and definitions whose result is a type class (143) are not exported.

## 2. The aperture: how many definitions fall in families as the matching loosens

Each cell is the number of reachable definitions in a family of at least that size (share of all reachable definitions in brackets for "≥ 2"). "removable" = members − 1 summed over families: the definitions that would disappear if each family became one definition. A row marked *skeleton ≥ 4* counts only families whose shared body has at least four nodes; the rest of a row is families like "a product of two types" or "one function applied to one argument".

### ns: 9,903 reachable definitions

| level | families | defs in ≥ 2 | ≥ 3 | ≥ 5 | ≥ 10 | largest | removable |
|---|---:|---:|---:|---:|---:|---:|---:|
| L0 body, exact up to bound names | 275 | 1,025 (10.4%) | 627 | 470 | 392 | 75 | 750 (7.6%) |
| … *body ≥ 4 nodes* | 236 | 856 (8.6%) | 510 | 381 | 317 | 75 | 620 (6.3%) |
| … and equal signature | 235 | 930 (9.4%) | 592 | 462 | 392 | 75 | 695 (7.0%) |
| L1 + numerals abstracted | 305 | 1,111 (11.2%) | 655 | 493 | 413 | 75 | 806 (8.1%) |
| L2 + leaf constants → typed holes | 327 | 1,201 (12.1%) | 711 | 540 | 447 | 77 | 874 (8.8%) |
| L3 + project heads → holes | 698 | 2,090 (21.1%) | 1,024 | 608 | 467 | 77 | 1,392 (14.1%) |
| … *body ≥ 4 nodes* | 631 | 1,804 (18.2%) | 818 | 459 | 360 | 75 | 1,173 (11.8%) |
| … and equal signature at L3 | 599 | 1,819 (18.4%) | 887 | 550 | 447 | 77 | 1,220 (12.3%) |
| AU@1.0 anti-unification, leaf and head holes only | 934 | 3,124 (31.5%) | 1,892 | 1,187 | 742 | 77 | 2,190 (22.1%) |
| … *skeleton ≥ 4* | 698 | 1,913 (19.3%) | 869 | 420 | 239 | 75 | 1,215 (12.3%) |
| AU@0.9 | 971 | 3,208 (32.4%) | 1,918 | 1,187 | 742 | 77 | 2,237 (22.6%) |
| AU@0.8 | 1,141 | 3,606 (36.4%) | 2,048 | 1,223 | 744 | 77 | 2,465 (24.9%) |
| AU@0.7 (≤ 30% of a member inside compound holes) | 1,392 | 4,307 (43.5%) | 2,403 | 1,409 | 777 | 77 | 2,915 (29.4%) |
| … *skeleton ≥ 4* | 1,055 | 2,739 (27.7%) | 1,137 | 475 | 234 | 75 | 1,684 (17.0%) |
| AU@0.6 | 1,616 | 5,134 (51.8%) | 3,074 | 1,728 | 916 | 129 | 3,518 (35.5%) |
| AU@0.5 | 1,717 | 5,925 (59.8%) | 3,871 | 2,365 | 1,362 | 129 | 4,208 (42.5%) |
| … *skeleton ≥ 4* | 1,195 | 3,232 (32.6%) | 1,572 | 627 | 275 | 42 | 2,037 (20.6%) |
| API@8 ≥ 8 identical lemma shapes | 11 | 22 (0.2%) | 0 | 0 | 0 | 2 | 11 (0.1%) |
| API@5 | 41 | 86 (0.9%) | 8 | 5 | 0 | 5 | 45 (0.5%) |
| API@3 | 174 | 373 (3.8%) | 59 | 6 | 0 | 6 | 199 (2.0%) |
| API@2 | 380 | 879 (8.9%) | 251 | 66 | 0 | 9 | 499 (5.0%) |
| APIL@2 the same with leaf constants abstracted | 382 | 883 (8.9%) | 251 | 66 | 0 | 9 | 501 (5.1%) |
| ROLE@0.5 lemma roles, weighted overlap ≥ 0.5 | 177 | 419 (4.2%) | 139 | 38 | 0 | 8 | 242 (2.4%) |
| ROLE@0.35 | 262 | 633 (6.4%) | 231 | 65 | 12 | 12 | 371 (3.7%) |
| ROLE@0.25 | 340 | 852 (8.6%) | 362 | 95 | 14 | 14 | 512 (5.2%) |
| ROLE@0.15 | 432 | 1,109 (11.2%) | 501 | 165 | 15 | 15 | 677 (6.8%) |
| AU@0.7 and ≥ 2 identical lemma shapes | 137 | 288 (2.9%) | 32 | 6 | 0 | 6 | 151 (1.5%) |
| WRAP a definition and ≥ 2 named specialisations | 475 | 1,962 (19.8%) | 1,962 | 771 | 156 | 36 | 1,487 (15.0%) |

Of the 750 exact duplicates (L0 removable), 452 are types, 291 are values or functions, 7 are propositions.

Lemma side. 126,928 distinct (statement, definition-holed) shapes; 1,786 are held by two or more definitions, by 2,693 definitions in all. 3,812 of 24,778 reachable theorems that mention a definition (15.4%) have a statement that is also proved, hole for hole, about a different definition. Abstracting leaf constants as well adds 6 shapes: nothing. Roles are much coarser: 11,548 distinct, 4,241 held by two or more definitions, the commonest by 2,183.

### ns, every definition (dead code included): 13,043 definitions

| level | families | defs in ≥ 2 | ≥ 3 | ≥ 5 | ≥ 10 | largest | removable |
|---|---:|---:|---:|---:|---:|---:|---:|
| L0 body, exact up to bound names | 381 | 1,672 (12.8%) | 1,116 | 889 | 795 | 331 | 1,291 (9.9%) |
| L3 + project heads → holes | 1,014 | 3,279 (25.1%) | 1,741 | 1,118 | 911 | 331 | 2,265 (17.4%) |
| AU@0.7 (≤ 30% of a member inside compound holes) | 1,852 | 6,094 (46.7%) | 3,600 | 2,210 | 1,335 | 337 | 4,242 (32.5%) |
| API@2 | 750 | 1,744 (13.4%) | 502 | 147 | 22 | 11 | 994 (7.6%) |
| ROLE@0.25 | 528 | 1,296 (9.9%) | 490 | 130 | 39 | 20 | 768 (5.9%) |

### Carleson: 401 reachable definitions

| level | families | defs in ≥ 2 | ≥ 3 | ≥ 5 | ≥ 10 | largest | removable |
|---|---:|---:|---:|---:|---:|---:|---:|
| L0 body, exact up to bound names | 4 | 9 (2.2%) | 3 | 0 | 0 | 3 | 5 (1.2%) |
| L1 + numerals abstracted | 13 | 43 (10.7%) | 35 | 13 | 0 | 7 | 30 (7.5%) |
| L2 + leaf constants → typed holes | 13 | 43 (10.7%) | 35 | 13 | 0 | 7 | 30 (7.5%) |
| L3 + project heads → holes | 22 | 61 (15.2%) | 35 | 13 | 0 | 7 | 39 (9.7%) |
| … *body ≥ 4 nodes* | 19 | 53 (13.2%) | 29 | 13 | 0 | 7 | 34 (8.5%) |
| AU@1.0 anti-unification, leaf and head holes only | 31 | 101 (25.2%) | 65 | 43 | 0 | 9 | 70 (17.5%) |
| AU@0.7 (≤ 30% of a member inside compound holes) | 40 | 134 (33.4%) | 86 | 60 | 14 | 14 | 94 (23.4%) |
| … *skeleton ≥ 4* | 31 | 84 (20.9%) | 40 | 23 | 0 | 8 | 53 (13.2%) |
| AU@0.5 | 45 | 162 (40.4%) | 110 | 72 | 34 | 14 | 117 (29.2%) |
| API@3 | 9 | 19 (4.7%) | 3 | 0 | 0 | 3 | 10 (2.5%) |
| API@2 | 12 | 31 (7.7%) | 13 | 5 | 0 | 5 | 19 (4.7%) |
| ROLE@0.5 lemma roles, weighted overlap ≥ 0.5 | 17 | 37 (9.2%) | 7 | 0 | 0 | 4 | 20 (5.0%) |
| ROLE@0.25 | 28 | 71 (17.7%) | 35 | 5 | 0 | 5 | 43 (10.7%) |
| ROLE@0.15 | 37 | 96 (23.9%) | 50 | 10 | 0 | 5 | 59 (14.7%) |
| AU@0.7 and ≥ 2 identical lemma shapes | 6 | 15 (3.7%) | 7 | 0 | 0 | 4 | 9 (2.2%) |
| WRAP a definition and ≥ 2 named specialisations | 5 | 18 (4.5%) | 18 | 5 | 0 | 5 | 13 (3.2%) |

173 of 1,580 theorems (10.9%) have a statement shape also proved about another definition.

### PFR: 52 reachable definitions

| level | families | defs in ≥ 2 | ≥ 3 | ≥ 5 | ≥ 10 | largest | removable |
|---|---:|---:|---:|---:|---:|---:|---:|
| L0 body, exact up to bound names | 0 | 0 (0.0%) | 0 | 0 | 0 | 1 | 0 (0.0%) |
| L1 + numerals abstracted | 0 | 0 (0.0%) | 0 | 0 | 0 | 1 | 0 (0.0%) |
| L2 + leaf constants → typed holes | 0 | 0 (0.0%) | 0 | 0 | 0 | 1 | 0 (0.0%) |
| L3 + project heads → holes | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |
| … *body ≥ 4 nodes* | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |
| AU@1.0 anti-unification, leaf and head holes only | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |
| AU@0.7 (≤ 30% of a member inside compound holes) | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |
| … *skeleton ≥ 4* | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |
| AU@0.5 | 3 | 8 (15.4%) | 4 | 0 | 0 | 4 | 5 (9.6%) |
| API@3 | 0 | 0 (0.0%) | 0 | 0 | 0 | 0 | 0 (0.0%) |
| API@2 | 1 | 2 (3.8%) | 0 | 0 | 0 | 2 | 1 (1.9%) |
| ROLE@0.5 lemma roles, weighted overlap ≥ 0.5 | 2 | 4 (7.7%) | 0 | 0 | 0 | 2 | 2 (3.8%) |
| ROLE@0.25 | 4 | 8 (15.4%) | 0 | 0 | 0 | 2 | 4 (7.7%) |
| ROLE@0.15 | 6 | 13 (25.0%) | 3 | 0 | 0 | 3 | 7 (13.5%) |
| AU@0.7 and ≥ 2 identical lemma shapes | 0 | 0 (0.0%) | 0 | 0 | 0 | 0 | 0 (0.0%) |
| WRAP a definition and ≥ 2 named specialisations | 1 | 3 (5.8%) | 3 | 0 | 0 | 3 | 2 (3.8%) |

5 of 584 theorems (0.9%) have a statement shape also proved about another definition.

The largest families in the human projects, for scale:

- Carleson: 9 members, anti-unification (AU@1.0, AU@0.7, AU@0.5); skeleton `Exists.choose`; members `Antichain.L'`, `Antichain.p''`, `Yk`, `cancelPt`, `enumΘ'`, `maximalSubfamily` …; 0 identical lemma shapes, 5 shared roles.
- Carleson: 4 members, lemma shapes (API@2); body and lemma shapes; skeleton `Set.ofPred (fun x0 : p0 ↦ ((Dist.dist p3 x0) ∈ (⟨h1⟩ p1 p2)))`; members `Annulus.cc`, `Annulus.co`, `Annulus.oc`, `Annulus.oo`; 5 identical lemma shapes, 1 shared roles.
- Carleson: 4 members, specialisation (WRAP); skeleton `Set.minLayer ⟨h1⟩ ⟨h2⟩`; members `Set.maxLayer`, `Set.minLayer`, `𝔏₀'`, `𝔏₁`; 3 identical lemma shapes, 5 shared roles.
- Carleson: 2 members, body (L3); anti-unification (AU@1.0); skeleton `Finset.sum (Finset.filter (Membership.mem p0) Finset.univ) (fun x0 : (𝔓 p1 (Nat.cast (2 ^ p2)) (defaultD p2) (defaultκ p2) (defaultS p1 p2 p3 p4 p5 p6`; members `adjointCarlesonSum`, `carlesonSum`; 0 identical lemma shapes, 3 shared roles.
- PFR: 3 members, specialisation (WRAP); skeleton `Kernel.rdist ⟨h1⟩ (ProbabilityTheory.condDistrib ⟨h2⟩ ⟨h3⟩ ⟨h4⟩) ⟨h5⟩ (Measure.map ⟨h3⟩ ⟨h4⟩)`; members `Kernel.rdist`, `condRuzsaDist`, `condRuzsaDist'`; 0 identical lemma shapes, 2 shared roles.
- PFR: 2 members, lemma roles (ROLE@0.15); skeleton `no common body`; members `condRho`, `condRuzsaDist'`; 0 identical lemma shapes, 7 shared roles.
- PFR: 4 members, anti-unification (AU@0.5); skeleton `tsum (fun x0 : p0 ↦ ((Measure.real p1 (Set.preimage p2 (Singleton.singleton x0))) * ⟨h1⟩)) (SummationFilter.unconditional p0)`; members `condKLDiv`, `condRho`, `condRhoMinus`, `condRhoPlus`; 0 identical lemma shapes, 2 shared roles.
- PFR: 3 members, lemma roles (ROLE@0.15); skeleton `no common body`; members `KLDiv`, `rhoMinus`, `rhoPlus`; 2 identical lemma shapes, 4 shared roles.

## 3. Controls

### 3.1 Known cases in ns (no names were given to the tool)

- **Constant-hiding predicates with no algebra of their own (`MemClass`, `UniformClass`, `WaveClass`).**
  - `WaveClass`, `MeanClass`, `UnweightedClass` and `AmplitudeBound` are found as specialisations of `MemClass` (WRAP: each body is `MemClass` applied to a weight). Likewise `UniformMeanClass` and `UniformWaveClass` for `UniformClass`. Surfaced: yes.
  - `MemClass` and `UniformClass` are **not** joined by body at any level (similarity 0.29: `UniformClass` has one more index, so every quantifier block differs by a binder, which first-order anti-unification cannot express) and have **no** identical lemma shape. They are joined by lemma roles: 17 roles in common (`add`, `sub`, `neg`, `mul`/`cmul`, `bilinear`, `map`, `sum`, `fderiv`, `lift`, `slice`, …), weighted overlap 0.24, together with `LocalClass` at ROLE@0.25 and `LocalJets` at ROLE@0.15. Surfaced: by roles only, and the role channel was built after seeing this miss.
- **Home-made big-O (`JetRate`) and its duplicated laws.** `JetRate` and `FiniteJetRate` (the same bound for all orders up to `M`) share three identical lemma shapes (API@3) and are not joined by body at any level (similarity 0.37; the extra quantifier again). By roles `JetRate` pairs with `UnweightedClass` at ROLE@0.15. The other two copies of the big-O laws reported in LESSSIM (`weaken_bound` / `add_bounds`, `finite_polynomial_majorant`) are theorems about an inline `∃ C, 0 ≤ C ∧ …`, with no definition to cluster, so a tool that clusters definitions cannot see them. Surfaced: partly, and low in the list.
- **Near-identical cloned modules.** See 3.2. Surfaced: yes at L3, in the run over all definitions; the clones are dead code and absent from the main run by construction.


Where each known definition sits (every family record that contains it; rank is by triage score among 4,178 family records):

| definition | rank | channel | members | identical lemma shapes | shared roles | others in the family |
|---|---:|---|---:|---:|---:|---|
| `WeightedClasses.MemClass` | 46 | WRAP | 5 | 0 | 12 | `AmplitudeBound`, `MeanClass`, `UnweightedClass`, `WaveClass` |
| `WeightedClasses.MemClass` | 79 | ROLE@0.15 | 4 | 0 | 18 | `UniformClass`, `LocalClass`, `LocalJets` |
| `WeightedClasses.MemClass` | 118 | ROLE@0.25 | 3 | 0 | 17 | `UniformClass`, `LocalClass` |
| `WeightedClasses.MemClass` | 824 | AU@0.7, AU@0.5 | 3 | 2 | 5 | `NativeJets`, `EnvelopeJets` |
| `LabelSumBounds.UniformClass` | 79 | ROLE@0.15 | 4 | 0 | 18 | `LocalClass`, `LocalJets`, `MemClass` |
| `LabelSumBounds.UniformClass` | 118 | ROLE@0.25 | 3 | 0 | 17 | `LocalClass`, `MemClass` |
| `LabelSumBounds.UniformClass` | 164 | WRAP | 3 | 0 | 5 | `UniformMeanClass`, `UniformWaveClass` |
| `WeightedClasses.WaveClass` | 46 | WRAP | 5 | 0 | 12 | `AmplitudeBound`, `MeanClass`, `MemClass`, `UnweightedClass` |
| `DiagonalResidual.JetRate` | 783 | ROLE@0.15 | 2 | 0 | 5 | `UnweightedClass` |
| `DiagonalResidual.JetRate` | 2,076 | API@3, API@2, APIL@3, APIL@2 | 2 | 3 | 2 | `FiniteJetRate` |

### 3.2 Cloned modules

The dead-code tool lists 15 near-identical module clones. They hold 169 definitions, of which 1 is reachable from the headline theorems, so the clones are invisible to the main run and were checked in the run over every definition. A clone definition counts as found when it is in one family with a definition of the module it was copied from.

- by exact body (L0): 53 of 169. The rest mention other cloned definitions, so their bodies differ in names.
- with project heads abstracted (L3): 169 of 169.
- by identical lemma shapes (API@2): 109 of 169; by roles (ROLE@0.25): 16.

6 of the 15 clone modules contain theorems only and are not in the table.

| clone module | definitions | L0 | L3 | AU@0.7 | API@2 | ROLE@0.25 | reachable |
|---|---:|---:|---:|---:|---:|---:|---:|
| `NavierStokes.CorrectionInitializationNoOptions` | 134 | 39 | 134 | 134 | 93 | 14 | 0 |
| `NavierStokes.DiagonalJetBoundsNoOptions` | 2 | 2 | 2 | 2 | 2 | 0 | 0 |
| `Euler.PacketShiftArithmeticNoOptions` | 4 | 2 | 4 | 4 | 4 | 1 | 0 |
| `Euler.ParentGeometryForwardChoiceNoOptions` | 15 | 3 | 15 | 15 | 6 | 0 | 0 |
| `Euler.GevreyGeneratingDerivativesNoOptions` | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| `Euler.BaseFirstPacketChoiceNoOptions` | 6 | 2 | 6 | 6 | 1 | 0 | 0 |
| `Euler.ParentGeometryJoinedChoiceInvestigation` | 5 | 2 | 5 | 5 | 1 | 0 | 0 |
| `Euler.BaseInductionStageNoOptions` | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| `Euler.PacketInitializedHessianError` | 1 | 1 | 1 | 1 | 0 | 0 | 1 |

### 3.3 Planted families

`tools/families/planted/FamiliesPlanted.lean` (compiled against the corpus's Mathlib, never part of it) is mixed into the ns export and the whole pipeline rerun; expectations were written in `planted/expected.json` before the planted run. The families were written by the builder of the matcher, after the ns runs, so they test that the pipeline does what it is described to do and not how it fares on families someone else would write (plan rule 2 is not met).

| control | expectation | result | where it landed |
|---|---|---|---|
| A: `Decay2`, `Decay3`, `Decay5` | one family from level 1 on; one numeral hole; four parallel lemma shapes; in the body-and-API channel | **as expected** | rank 118: API@3, API@2, APIL@3, 6 members (with EvenFn, PeriodicOne, VanishAtZero); rank 134: L1, L2, L3, 3 members, holes: numeral |
| B: `EvenFn`, `PeriodicOne`, `VanishAtZero` | not together at body levels 0-3; together in a ROLE (or API) family | **as expected** | rank 118: API@3, API@2, APIL@3, 6 members (with Decay2, Decay3, Decay5); rank 504: API@5, APIL@5, 3 members; rank 612: AU@0.5, 3 members (with Periodic), holes: type, head, mixed, head |
| N1: `Lonely` | in no family | **as expected** | no family |
| N2: `scaleUp`, `stepAbove` | together at level 1 (coincidence the matcher cannot rule out); no parallel lemmas | **as expected** | rank 234: AU@0.5, 21 members (with frameConstant, highShift, meanShift…), holes: head, head, mixed, mixed, mixed; rank 317: AU@1.0, AU@0.7, 14 members (with frameConstant, highShift, meanShift…), holes: head, head, mixed, mixed, mixed; rank 2,831: L1, L2, L3, 2 members, holes: numeral, numeral |

The two planted families also merge with each other in the lemma-shape channel: `zero`, `neg`, `add` and `const_mul` have the identical statement for all six predicates. That is correct behaviour (all six are sets of functions closed under the same operations) and it shows what the lemma channel finds: a shared algebra, whatever the bodies are.

## 4. Triage score

The score orders the reading list. It is not a measure of whether a family is one idea, and it is not used to decide anything.

    score = conceptReductionHigh / penalty

- `conceptReductionLow` = (members − 1) + lemma statements with an identical shape held by two or more members, minus the largest member's share (the statements one parameterised version would replace, counted strictly).
- `conceptReductionHigh` = (members − 1) + the larger of that and the role count: for each lemma role shared by two or more members and held by at most max(40, 3·members + 20) definitions in the corpus, one lemma per further member. For a family of types the role count is set to 0.
- Statements that mention two or more members are left out of both counts.
- `penalty` = 1 + effective parameters + 0.5 × (holes that depend on a bound variable) + 0.5 × (compound holes) when the members share a body; 2 for a specialisation family (the general form exists); 5 when there is no common body (similarity below 0.5), because the replacement would be an interface and not a parameter.
- Printed beside it and not in the score: users, statements mentioning a member, co-occurrence, skeleton size, instance and type arguments per member.

Known distortions. A family of verbatim copies scores highest (no holes, penalty 1) although merging it changes no proof. A two-member family of large structures with many shared roles scores high on the role count alone. The role count is an optimistic bound: two lemmas with the same role need not be instances of one statement, and earlier work here found 18 of the 20 largest statement-shape clusters had a false common generalisation.


## 5. The 60 highest-scoring families

A family that overlaps a higher-scoring one (60% of the smaller) is folded into it and its id is listed under "also". Columns: m members; tight = tightest level at which the members are already together; sk = nodes of the shared skeleton (– = no common body); holes = distinct holes / effective parameters (holes that always change together count once); users = declarations that use a member; stmt = theorems whose statement mentions a member; shapes = identical lemma shapes held by ≥ 2 members; roles = shared lemma roles; low–high = estimated concept-count reduction (definitions + lemma statements).

| # | id | m | tight | channels | sk | holes | users | stmt | shapes | roles | low–high | pen | score | skeleton / first members |
|---:|---|---:|---|---|---:|---|---:|---:|---:|---:|---|---:|---:|---|
| 1 | F00001 | 75 | L0 | body+AU | 9 | 0/0 | 3,169 | 1,232 | 10 | 27 | 86–86 | 1 | 86 | `Prod Real (Prod (Prod Real Real) (Prod Real Real))` · Point, Point, Point |
| 2 | F00002 | 60 | L0 | body | 3 | 0/0 | 8,117 | 2,231 | 10 | 42 | 69–69 | 1 | 69 | `Prod Real Real` · Plane, Plane, Plane |
| 3 | F00003 | 52 | L0 | body | 5 | 0/0 | 3,004 | 783 | 5 | 23 | 56–56 | 1 | 56 | `Prod Real (Prod Real Real)` · Slow, Parameter, Parameter |
| 4 | F00005 | 41 | L0 | body+AU | 11 | 0/0 | 1,409 | 648 | 1 | 16 | 41–41 | 1 | 41 | `Prod (Prod Real (Prod (Prod Real Real) (Prod Real Real))) Real` · Full, Full, FullPoint |
| 5 | F00006 | 28 | L0 | body | 4 | 0/0 | 12,066 | 4,550 | 8 | 94 | 37–37 | 1 | 37 | `EuclideanSpace Real (Fin 3)` · Vector3, Space, Space |
| 6 | F00007 | 18 | L0 | body+AU | 23 | 0/0 | 993 | 656 | 12 | 7 | 31–31 | 1 | 31 | `Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (ProfileData.o` · Index, Index, Index |
| 7 | F00010 | 22 | AU@1.0 | AU | 1 | 0/0 | 369 | 147 | 1 | 5 | 23–28 | 1 | 28 | `Classical.choose` · solution, representative, representative |
| 8 | F00011 | 35 | L1 | body | 3 | 1/1 | 1,674 | 545 | 14 | 5 | 52–52 | 2 | 26 | `∀ x0 : (Fin ⟨h1⟩), Real` · FieldJet, StockJet, Vec2 |
| 9 | F00014 | 36 | WRAP | wrap | 1 | 5/3 | 132 | 55 | 0 | 5 | 35–48 | 2 | 24 | `Field.congr ⟨h1⟩ ⟨h2⟩ ⟨h3⟩ ⟨h4⟩ ⟨h5⟩` · pressureGradientCylinderField, meanSolveCylinderField, pressureField |
| 10 | F00015 | 15 | ROLE@0.15 | roles | – | –/– | 906 | 690 | 17 | 14 | 35–110 | 5 | 22 | `no common body` · CoefficientsTranslation, GaugeSupported, Shell |
| 11 | F00016 | 20 | L3 | body+AU | 1 | 0/0 | 938 | 340 | 0 | 1 | 19–21 | 1 | 21 | `Classical.choice` · packet, toJet, fundamentalPath |
| 12 | F00019 | 7 | L0 | body | 5 | 0/0 | 828 | 270 | 0 | 10 | 6–20 | 1 | 20 | `(1 / 2) + p0` · A, waveExponent, exponent |
| 13 | F00023 | 6 | L0 | body | 5 | 0/0 | 1,031 | 212 | 10 | 1 | 18–18 | 1 | 18 | `∀ x0 : Nat, (∀ x1 : p0, Real)` · ScalarField, ScalarField, ScalarField |
| 14 | F00026 | 3 | WRAP | wrap | 1 | 2/1 | 198 | 104 | 0 | 19 | 2–33 | 2 | 16.5 | `EulerPacketProfileRecursion.profiles ⟨h1⟩ ⟨h2⟩` · joinedSourceProfiles, sourceProfiles, profiles |
| 15 | F00027 | 13 | L0 | body+AU | 23 | 0/0 | 713 | 428 | 4 | 5 | 16–16 | 1 | 16 | `Prod (Fin 2) (BaseChartJets.CellIndex (TailData.h (Profile.data (Profi` · Label, Label, Label |
| 16 | F00028 | 18 | WRAP | wrap | – | –/– | 272 | 159 | 7 | 8 | 24–31 | 2 | 15.5 | `no common body` · potentialField, field, pointField |
| 17 | F00029 | 15 | L0 | body | 3 | 0/0 | 1,686 | 820 | 1 | 10 | 15–15 | 1 | 15 | `Prod Int Int` · Frequency, Frequency, Copy |
| 18 | F00030 | 2 | AU@0.7 | AU+roles | 36 | 1/1 | 257 | 125 | 0 | 17 | 1–36 | 2.5 | 14.4 | `Operators.mk (Set.Icc 0 (Data.T p0)) p1 (fun x0 : (Prod Real (Prod (Eu` · joinedSourceOperators, sourceOperators |
| 19 | F00031 | 15 | L0 | body+AU | 27 | 0/0 | 349 | 233 | 0 | 0 | 14–14 | 1 | 14 | `fun x0 : Nat ↦ (fun x1 : Nat ↦ (Prod (BaseChartJets.CellIndex (TailDat` · Index, Index, Index |
| 20 | F00035 | 3 | API@5 | shapes | 5 | 2/1 | 4,680 | 3,568 | 13 | 23 | 62–62 | 5 | 12.4 | `∃ x0 : ⟨h1⟩, (∃ x1 : Real, ⟨h2⟩)` · Profile, Parameters, TailData |
| 21 | F00036 | 5 | L0 | body+AU | 13 | 0/0 | 127 | 67 | 7 | 0 | 12–12 | 1 | 12 | `∀ x0 : Nat, (∀ x1 : (Prod Real (Prod (Prod Real Real) (Prod Real Real)` · Scalar, Scalar, Scalar |
| 22 | F00037 | 13 | L0 | body+AU | 9 | 0/0 | 629 | 136 | 0 | 3 | 12–12 | 1 | 12 | `Prod (Prod Real (Prod Real Real)) (Prod Real Real)` · Associated, Native, Native |
| 23 | F00038 | 13 | L0 | body | 6 | 0/0 | 170 | 67 | 0 | 0 | 12–12 | 1 | 12 | `Matrix (Fin 2) (Fin 2) Real` · Mat2, Mat2, Mat2 |
| 24 | F00039 | 13 | L0 | body | 4 | 0/0 | 447 | 130 | 0 | 2 | 12–12 | 1 | 12 | `EuclideanSpace Real (Fin 2)` · Plane, State, Plane |
| 25 | F00040 | 7 | WRAP | wrap | 2 | 3/2 | 141 | 91 | 14 | 1 | 23–23 | 2 | 11.5 | `EulerElapsedTimePathGluing.join ⟨h1⟩ p1 ⟨h2⟩ ⟨h3⟩` · join, profile, derivativePath |
| 26 | F00041 | 8 | WRAP | wrap | – | –/– | 94 | 71 | 9 | 3 | 23–23 | 2 | 11.5 | `no common body` · deltaV, gamma, repair |
| 27 | F00042 | 18 | AU@0.5 | AU | 5 | 1/1 | 652 | 343 | 9 | 8 | 27–28 | 2.5 | 11.2 | `DFunLike.coe (fderiv Real p0 p1) ⟨h1⟩` · vectorPartial, angularDerivative, coordinateDerivative |
| 28 | F00043 | 35 | AU@0.5 | AU | 3 | 2/2 | 99 | 35 | 0 | 1 | 34–39 | 3.5 | 11.14 | `LinearMap.mk (RingHom.id ⟨h1⟩) (AddHom.mk ⟨h2⟩)` · tensorPathLinear, coefficientLinear, derivativeBundlingLinear |
| 29 | F00044 | 9 | AU@1.0 | AU | 1 | 0/0 | 336 | 267 | 0 | 3 | 8–11 | 1 | 11 | `Exists.choose` · evolution, lifespan, sourceGrowthProfile |
| 30 | F00045 | 9 | WRAP | wrap | 5 | 1/1 | 224 | 144 | 0 | 14 | 8–22 | 2 | 11 | `EulerPacketPointJets.fieldSum (p0 + 1) p1 ⟨h1⟩` · high, mean, fieldSum |
| 31 | F00046 | 5 | WRAP | wrap | 3 | 4/3 | 453 | 382 | 0 | 12 | 4–21 | 2 | 10.5 | `WeightedClasses.MemClass ⟨h1⟩ (fun x0 : Nat ↦ ⟨h2⟩) ⟨h3⟩ ⟨h4⟩` · AmplitudeBound, MeanClass, MemClass |
| 32 | F00049 | 9 | L0 | body | 5 | 0/0 | 1,408 | 512 | 2 | 3 | 10–10 | 1 | 10 | `∀ x0 : (Prod Real Real), Real` · Field, Field, Field |
| 33 | F00050 | 30 | AU@0.5 | AU | 4 | 3/3 | 448 | 171 | 1 | 12 | 30–47 | 5 | 9.4 | `ContinuousLinearMap.comp (RingHom.id ⟨h1⟩) (RingHom.id ⟨h1⟩) (RingHom.` · pathCompositionMap, pressureSolver, freezePath |
| 34 | F00052 | 4 | WRAP | wrap | 3 | 8/2 | 98 | 53 | 0 | 11 | 3–18 | 2 | 9 | `EulerPacketCorrectionCoefficients.correctionDataOfFields p0 ⟨h1⟩ (Inv.` · coordinateData, correctionDataOfFields, forwardInitializedCorrectionData |
| 35 | F00053 | 9 | AU@1.0 | AU | 4 | 0/0 | 152 | 93 | 0 | 1 | 8–9 | 1 | 9 | `Eq.rec p0 p1 p2` · changeTime, changeTime, congr |
| 36 | F00054 | 9 | L0 | body+AU | 6 | 0/0 | 1,924 | 1,037 | 1 | 9 | 9–9 | 1 | 9 | `Prod Real (EuclideanSpace Real (Fin 3))` · SpaceTime, SpaceTime, SpaceTime |
| 37 | F00055 | 10 | L0 | body+AU | 11 | 0/0 | 330 | 154 | 0 | 3 | 9–9 | 1 | 9 | `Prod (Prod (Prod Real (Prod Real Real)) Real) (Prod Real Real)` · Native, Native, Native |
| 38 | F00058 | 11 | WRAP | wrap | 1 | 1/1 | 95 | 69 | 3 | 0 | 17–17 | 2 | 8.5 | `EulerPolynomialCost.coefficientCost ⟨h1⟩` · costConstant, constant, sourceConstant |
| 39 | F00060 | 13 | AU@0.5 | AU | 3 | 1/1 | 132 | 46 | 1 | 4 | 13–20 | 2.5 | 8 | `ContinuousLinearMap.compLeftContinuous Real p0 ⟨h1⟩` · pathAdjointMap, adjointMap, pathAverage |
| 40 | F00061 | 3 | L0 | body+AU | 8 | 0/0 | 133 | 53 | 5 | 2 | 8–8 | 1 | 8 | `ActualPrimary.piece p0 p1 ActualPrimary.standardRegion (Prod.snd p2) (` · pieces, primaryPiece, primaryPiece |
| 41 | F00062 | 16 | AU@1.0 | AU | 9 | 1/1 | 53 | 31 | 1 | 1 | 16–16 | 2 | 8 | `⟨h1⟩ (ActualCycleParameters.fixedParameters p0 p1) (CycleState.coeffic` · postSigned, postTemporal, signedGaussian |
| 42 | F00064 | 5 | L3 | body+AU | 9 | 1/1 | 67 | 32 | 7 | 0 | 16–16 | 2 | 8 | `(2 • ((⟨h1⟩ p0) * (⟨h1⟩ p1))) + ((⟨h1⟩ p1) * (⟨h1⟩ p1))` · axialQuadratic, axialAxial, radialAngular |
| 43 | F00066 | 14 | AU@0.5 | AU | 3 | 1/1 | 69 | 26 | 0 | 3 | 13–19 | 2.5 | 7.6 | `ContinuousLinearMap.mk (RingHom.id Real) ⟨h1⟩` · tensorPathMap, coefficientMap, derivativeBundling |
| 44 | F00067 | 13 | WRAP | wrap | 1 | 3/2 | 278 | 197 | 0 | 2 | 12–15 | 2 | 7.5 | `AxisymmetricResidual.pack ⟨h1⟩ ⟨h2⟩ ⟨h3⟩` · componentPotential, pack, velocity |
| 45 | F00068 | 13 | AU@1.0 | AU | 1 | 2/2 | 560 | 276 | 3 | 3 | 22–22 | 3 | 7.33 | `⟨h1⟩ * ⟨h2⟩` · firstFrequencyPower, uniformL2Amplitude, boundaryLocalizationC2 |
| 46 | F00071 | 6 | L0 | body | 3 | 0/0 | 396 | 77 | 1 | 2 | 6–7 | 1 | 7 | `EuclideanSpace.single p0 1` · basisVector, direction, axis |
| 47 | F00072 | 10 | WRAP | wrap | 1 | 2/2 | 134 | 67 | 2 | 1 | 11–14 | 2 | 7 | `SmoothL2Field.mapField ⟨h1⟩ ⟨h2⟩` · directionalField, mapField, componentField |
| 48 | F00073 | 2 | L0 | body+AU | 13 | 0/0 | 157 | 76 | 0 | 5 | 1–7 | 1 | 7 | `Lp.compMeasurePreservingₗᵢ 2 MeasureSpace.volume MeasureSpace.volume R` · translation, translation |
| 49 | F00074 | 12 | WRAP | wrap | 3 | 3/3 | 156 | 107 | 2 | 2 | 13–14 | 2 | 7 | `LabelSumBounds.fieldSum ⟨h1⟩ (fun x0 : ⟨h2⟩ ↦ (HarmonicBlock.oscillati` · primaryField, actualPrimaryField, actualSignedField |
| 50 | F00075 | 8 | WRAP | wrap | 1 | 3/2 | 243 | 167 | 0 | 5 | 7–14 | 2 | 7 | `VariableGaugeMean.reconstructState ⟨h1⟩ ⟨h2⟩ ⟨h3⟩` · primary, primaryState, primaryBands |
| 51 | F00077 | 8 | L0 | body+AU | 11 | 0/0 | 367 | 99 | 0 | 1 | 7–7 | 1 | 7 | `Prod (Prod Real (Prod Real (Prod Real Real))) (Prod Real Real)` · LiftPoint, LiftPoint, LiftPoint |
| 52 | F00078 | 5 | L0 | body | 7 | 0/0 | 1,201 | 520 | 3 | 3 | 7–7 | 1 | 7 | `Prod Real (Prod p0 (Prod Real Real))` · Lift, Point, Point |
| 53 | F00079 | 4 | ROLE@0.15 | roles | – | –/– | 453 | 243 | 0 | 18 | 3–35 | 5 | 7 | `no common body` · UniformClass, LocalClass, LocalJets |
| 54 | F00080 | 6 | WRAP | wrap | 1 | 2/1 | 151 | 91 | 4 | 2 | 9–14 | 2 | 7 | `OutgoingHistories.history ⟨h1⟩ ⟨h2⟩` · I, J, M |
| 55 | F00084 | 14 | WRAP | wrap | 6 | 4/2 | 242 | 99 | 0 | 0 | 13–13 | 2 | 6.5 | `Field.ofLifted p0 ⟨h1⟩ ⟨h2⟩ ⟨h3⟩ (fun x0 : (Set.Elem (Set.Icc 0 ⟨h1⟩))` · toCylinderField, add, angleMean |
| 56 | F00085 | 7 | L2 | body+AU | 1 | 1/1 | 82 | 54 | 1 | 2 | 7–13 | 2 | 6.5 | `Polynomial.natDegree ⟨h1⟩` · degree, uniformPower, uniformPower |
| 57 | F00089 | 22 | AU@1.0 | AU | – | –/– | 1,768 | 828 | 5 | 8 | 27–31 | 5 | 6.2 | `no common body` · geometry, overlap, active |
| 58 | F00091 | 4 | L3 | body+AU | 4 | 1/1 | 67 | 50 | 7 | 4 | 12–12 | 2 | 6 | `DFunLike.coe (EulerLpCylinderRectangular.fullPathMap p0) (⟨h1⟩ p1)` · frame, frameDerivative, frameSecond |
| 59 | F00092 | 4 | AU@1.0 | AU | 2 | 1/1 | 84 | 46 | 4 | 2 | 12–12 | 2 | 6 | `ContDiffBump.toFun 0 ⟨h1⟩` · innerCutoff, middleCutoff, outerCutoff |
| 60 | F00095 | 11 | WRAP | wrap | 7 | 3/2 | 118 | 55 | 0 | 2 | 10–12 | 2 | 6 | `Field.changeTime (2 * Real.pi) (Data.T p0) ⟨h1⟩ (Data.T ⟨h2⟩) ⟨h3⟩` · changeTime, forwardInitializedCovectorRemainderField, forwardInitializedNormalizedField |

By what the members are: 20 families of types, 3 of propositions (predicates and Prop-valued structures), 37 of values or functions.

### Reading of the list (a model's reading, not evidence)

Read from skeletons, member names and bodies only; no member's lemmas were opened beyond the side-by-side blocks, and no generalisation was tried in Lean. Each family has its reading under its heading. Counts over the 60:

- **A, the same type under many local names: 20 families.** Product types, `EuclideanSpace ℝ (Fin 3)`, `Fin n → ℝ`, re-declared as `abbrev` in module after module. The largest concept-count item the tool finds, and the least interesting: one shared definition per type removes several hundred names and changes no proof.
- **B, not a family: 4.** `Classical.choose` and `Eq.rec` bodies whose only difference is an erased proof.
- **C, named instances of an existing general definition: 16.** The corpus wrote the parameterised form and then named its instances. `MemClass` and its weights are here.
- **D, same algebra, different bodies: 2.** Predicate families joined only by their lemma roles. These are the candidates for a structure or type class.
- **E, repeated data structures or records: 3.**
- **F, one operation or value written several times, zero or one simple hole: 8.** The directional derivative under 18 names is the clearest. These are where a single definition with one parameter would do, and where the library often already has it.
- **G, aperture noise: 7.** Skeletons of a few generic nodes.

So by this reading 26 of the 60 (C, D, F) are the kind of family the idea is about, and within them the general form usually exists already, in the corpus (C) or in Mathlib (F). D is the part that needs a new abstraction.

### Details


#### 1. F00001: 75 members, score 86

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7); also F00004, F00202, F00220 (3 overlapping records folded in)
- kinds: 75 abbrev; 74 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 3,169 declarations use a member; 1,232 theorem statements mention one; 73 member pairs occur together in a statement
- lemma family: 10 identical shapes (25 theorems; 0 shapes held by every member), 27 shared roles (210 theorems; 0 roles held by every member), out of 1,232 statements about the members
- concept-count estimate: 74 definitions + 12 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 86
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 9 nodes over 1 distinct bodies:

  ```
  Prod Real (Prod (Prod Real Real) (Prod Real Real))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualBaseResidual.Point` | 16 | 59 | `NavierStokes.CommonBaseContext.Point` |
| `NavierStokes.ActualCandidateConstruction.Point` | 0 | 1 | `NavierStokes.CorrectionStep.CyclePoint` |
| `NavierStokes.ActualCarrierGeometry.Point` | 9 | 9 | `NavierStokes.LocalSignedRequest.Point` |
| `NavierStokes.ActualCarrierTransportBase.Point` | 3 | 26 | `NavierStokes.LocalSignedRequest.Point` |
| `NavierStokes.ActualCoreSupport.Point` | 7 | 53 | `NavierStokes.LocalSignedRequest.Point` |
| `NavierStokes.ActualCurrentWaveSupport.Point` | 2 | 2 | `NavierStokes.LocalSignedRequest.Point` |
| `NavierStokes.ActualCycleAssembly.Point` | 37 | 42 | `NavierStokes.ActualInitialization.Point` |
| `NavierStokes.ActualCycleCoherence.Point` | 32 | 35 | `NavierStokes.ActualInitialization.Point` |
| `NavierStokes.ActualCycleExcluded.Point` | 5 | 9 | `NavierStokes.MeanStateRegularity.Point` |
| `NavierStokes.ActualCyclePeriodicity.Point` | 11 | 13 | `NavierStokes.ActualInitialization.Point` |
| `NavierStokes.ActualCyclePreservation.Point` | 12 | 19 | `NavierStokes.ActualInitialization.Point` |
| `NavierStokes.ActualCycleResidualBounds.Point` | 20 | 54 | `NavierStokes.LocalSignedRequest.Point` |
| `NavierStokes.ActualInitialCoherence.Point` | 20 | 70 | `NavierStokes.PressureStream.Lift NavierStokes.ActualInitialCoherence.Plane` |
| `NavierStokes.ActualInitialMean.Point` | 11 | 64 | `NavierStokes.LocalSignedRequest.Point` |

… and 61 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `3|uses>P|` (held by 208 definitions in the corpus)
  - `Point`: `ActualCycleAssembly.associated_update_inputSupport` : `NavierStokes.ActualCycleAssembly.associated_update_inputSupport {B N0 : ℕ}   (l : NavierStokes.ActualCycleAssembly.Index B N0)   (K : ℕ → Set NavierStokes.ActualCycleAssembly.Point)   (slowCarrier : ℕ → Set Nav`
  - `Point`: `ActualCycleExcluded.afterRank_covariance_mem` : `NavierStokes.ActualCycleExcluded.afterRank_covariance_mem {ι : Type}   (p : NavierStokes.CorrectionStep.CycleParameters ι)   (v : NavierStokes.CorrectionStep.CycleCoefficients ι)   (c : NavierStokes.CorrectionS`
  - `Point`: `ActualCyclePreservation.localUnweighted_restrict` : `NavierStokes.ActualCyclePreservation.localUnweighted_restrict {E I : Type} [NormedAddCommGroup E]   [NormedSpace ℝ E]   {s : NavierStokes.WeightedClasses.StripData NavierStokes.ActualCyclePreservation.Point}   `
  - `Point`: `ActualInitialMeanEquation.meanHypotheses_of_primitive` : `NavierStokes.ActualInitialMeanEquation.meanHypotheses_of_primitive {coord : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {g : NavierStokes.VariableGaugeMean.GaugeData NavierStokes.PressureStrea`
  - `Point`: `ActualInitialization.initial_residual_uniform_of_primary` : `NavierStokes.ActualInitialization.initial_residual_uniform_of_primary (B N0 : ℕ)   (hprimary :     NavierStokes.UniformHarmonicInteraction.UniformVelocity NavierStokes.ActualInitialization.strip       NavierSto`
- role `3|uses>K|` (held by 134 definitions in the corpus)
  - `Point`: `ActualCurrentWaveSupport.particular_radial_zero_germs` : `NavierStokes.ActualCurrentWaveSupport.particular_radial_zero_germs {B N0 : ℕ}   (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0)   (l : NavierStokes.ActualCurrentWaveSupport.Index B N0)   (c : `
  - `Point`: `ActualCycleAssembly.refined_particular_zero_germs` : `NavierStokes.ActualCycleAssembly.refined_particular_zero_germs {B N0 : ℕ}   (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0)   (l : NavierStokes.ActualCycleAssembly.Index B N0)   (c : NavierSto`
  - `Point`: `ActualCycleCoherence.wave_fields_zero_of_support` : `NavierStokes.ActualCycleCoherence.wave_fields_zero_of_support   {U : Set NavierStokes.ActualCycleCoherence.Point}   {K : ℕ → Set NavierStokes.ActualCycleCoherence.Point}   (b g : NavierStokes.CorrectionState.Ha`
  - `Point`: `WaveData.covariance_moving` : `NavierStokes.CorrectionAnalyticStep.WaveData.covariance_moving {ι : Type}   {G : NavierStokes.SignedMeanGain.Geometry} {p : NavierStokes.CorrectionStep.CycleParameters ι}   {v : NavierStokes.CorrectionStep.Cycl`
  - `CyclePoint`: `CycleAnalyticInvariant.raw_mean_bounds` : `NavierStokes.CorrectionStep.CycleAnalyticInvariant.raw_mean_bounds {ι : Type}   {G : NavierStokes.SignedMeanGain.Geometry}   {c : NavierStokes.CorrectionState.Context NavierStokes.CorrectionStep.CyclePoint}   {`
- role `2|uses>ContDiffOn|` (held by 64 definitions in the corpus)
  - `Point`: `ActualCycleResidualBounds.realization_native_smooth` : `NavierStokes.ActualCycleResidualBounds.realization_native_smooth {h : ℝ} {N : ℕ} {gap : ℕ → ℕ}   {U : Set NavierStokes.ActualCycleResidualBounds.Cylinder}   {c : NavierStokes.CorrectionState.Context NavierStoke`
  - `Point`: `ActualWaveRegularityData.signed_pressure_smooth` : `NavierStokes.ActualWaveRegularityData.signed_pressure_smooth {B N0 : ℕ}   (l : NavierStokes.ActualWaveRegularityData.Index B N0)   (P : NavierStokes.SignedStressPrimitive.Patch) (coord : ℝ)   (c : NavierStokes.`
  - `Point`: `StepData.next_pressure_smooth` : `NavierStokes.CycleMeanEquation.StepData.next_pressure_smooth {ι : Type} {coord : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {p : NavierStokes.CorrectionStep.CycleParameters ι}   {v : NavierSt`
  - `Point`: `GaugeMomentBalances.axialDebtPotential_smooth` : `NavierStokes.GaugeMomentBalances.axialDebtPotential_smooth {coord : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion coord)   (g : NavierStokes.VariableGaugeMean.GaugeData NavierStokes.GaugeMomentBalances.P`
  - `Point`: `MovingInitialization.zeroMean_gr_smooth` : `NavierStokes.CorrectionInitialization.MovingInitialization.zeroMean_gr_smooth {coord a b : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion coord) (ha : 0 < a) (hab : a < b)   (c : NavierStokes.CorrectionSt`
- role `0|P>L>L>◊|` (held by 49 definitions in the corpus)
  - `Point`: `BaseStressClasses.leading_composed_meanClass` : `NavierStokes.BaseStressClasses.leading_composed_meanClass {F : NavierStokes.OutgoingProfile.Profile}   {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W)   {ld : Na`
  - `Point`: = `Regular.band_mul` : `NavierStokes.GaugeDebtIncrement.Regular.band_mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.R`
  - `Point`: = `MovingField.band_mul` : `NavierStokes.MeanStateRegularity.MovingField.band_mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBal`
  - `Point`: `GaugeAliasDecay.pressureAliasState_radial_mem` : `NavierStokes.GaugeAliasDecay.pressureAliasState_radial_mem {a b h Mbase α : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion (2 * h)) (ha : 0 < a) (hab : a < b) {cL cR : ℝ}   (hcL : 0 < cL) (hcR : 0 < cR) (`
  - `Point`: `Periodic.band_mul` : `NavierStokes.MeanStateRegularity.Periodic.band_mul {U : Set NavierStokes.MeanStateRegularity.Plane}   {f : NavierStokes.MeanStateRegularity.Scalar} (hf : NavierStokes.MeanStateRegularity.Periodic U f)   (c : ℕ `
- role `0|P>L>L>L>◊|` (held by 41 definitions in the corpus)
  - `Point`: `ActualInitialMean.curl_amplitude_uniform` : `NavierStokes.ActualInitialMean.curl_amplitude_uniform {B N0 : ℕ} :   NavierStokes.LabelSumBounds.UniformWaveClass NavierStokes.ActualInitialMean.strip     NavierStokes.ActualInitialMean.envelope (1 - NavierStok`
  - `Point`: `ActualInitialization.angularFrequency_local` : `NavierStokes.ActualInitialization.angularFrequency_local (B N0 : ℕ) :   NavierStokes.LocalizedWaveBounds.LocalUnweighted NavierStokes.ActualInitialization.strip     NavierStokes.ActualInitialization.meanControl`
  - `Point`: `InitialPhysicalData.nativePotentialSource_bounds` : `NavierStokes.InitialPhysicalData.nativePotentialSource_bounds {B N0 : ℕ} :   NavierStokes.LocalPhysicalCopyBounds.LocalSourceBounds NavierStokes.ActualPrimaryBounds.strip     NavierStokes.CorrectionInitializati`
  - `Point`: `ActualParticularStageControls.associated_wave_return` : `NavierStokes.ActualParticularStageControls.associated_wave_return {B N0 : ℕ} {E : Type}   [NormedAddCommGroup E] [NormedSpace ℝ E] {α : ℝ}   {f :     NavierStokes.ActualParticularStageControls.Label B N0 →     `
  - `Point`: `Invariant.source_localBounds` : `NavierStokes.ActualCycleResidualBounds.Invariant.source_localBounds {B N0 : ℕ} {σ : ℝ}   {x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualCycleResidualBounds.Index B N0)}   (H : NavierStokes.Actu`
- role `1|P>L>L>◊|` (held by 14 definitions in the corpus)
  - `Point`: `BaseContextAssembly.envelope_pullback` : `NavierStokes.BaseContextAssembly.envelope_pullback.{u_1} {E : Type u_1} [NormedAddCommGroup E]   [NormedSpace ℝ E]   (s : NavierStokes.WeightedClasses.StripData NavierStokes.BaseContextAssembly.Point)   {D : Na`
  - `Point`: `Regular.directional` : `NavierStokes.GaugeDebtIncrement.Regular.directional {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncremen`
  - `Point`: `LocalSignedRequest.meanClass_profileMap` : `NavierStokes.LocalSignedRequest.meanClass_profileMap {coord : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion coord) (a b cL cR : ℝ) (ha : 0 < a) (hcL : 0 < cL)   (hcR : 0 < cR) (ε L : ℕ → ℝ) (hε : ∀ (n : `
  - `Point`: `Periodic.directional` : `NavierStokes.MeanStateRegularity.Periodic.directional   {U : Set NavierStokes.MeanStateRegularity.Plane} {f : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.MeanStateRegularity.Periodic U f) (hU `

#### 2. F00002: 60 members, score 69

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1); also F00008, F00221, F00380 (3 overlapping records folded in)
- kinds: 60 abbrev; 60 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 8,117 declarations use a member; 2,231 theorem statements mention one; 68 member pairs occur together in a statement
- lemma family: 10 identical shapes (23 theorems; 0 shapes held by every member), 42 shared roles (341 theorems; 0 roles held by every member), out of 2,231 statements about the members
- concept-count estimate: 59 definitions + 10 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 69
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 3 nodes over 1 distinct bodies:

  ```
  Prod Real Real
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCarrierTransportBase.Plane` | 11 | 26 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualCopySliceRegularity.Plane` | 6 | 6 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualInitialCoherence.Plane` | 11 | 99 | `NavierStokes.PressureStream.Plane` |
| `NavierStokes.ActualMeanPhysicalData.Plane` | 21 | 58 | `NavierStokes.PressureStream.Plane` |
| `NavierStokes.ActualParticularControl.Plane` | 6 | 15 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualParticularRealization.Plane` | 0 | 5 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualParticularStageControls.Plane` | 7 | 182 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualPeriodizedSignedRealization.Plane` | 4 | 13 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualPhaseDefect.Plane` | 0 | 13 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualPrimaryCovariance.Plane` | 18 | 33 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualSignedGeometry.Plane` | 11 | 430 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualSignedPhysicalBinding.Plane` | 0 | 1 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualSignedPhysicalData.Plane` | 17 | 36 | `NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualSignedStageControls.Plane` | 1 | 5 | `NavierStokes.TorusInverse.Plane` |

… and 46 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|uses>HasDerivAt|` (held by 163 definitions in the corpus)
  - `Point`: `HeatSwitchHistoryDerivatives.logI_hasDerivAt` : `NavierStokes.HeatSwitchHistoryDerivatives.logI_hasDerivAt (F : NavierStokes.OutgoingProfile.Profile)   {XR C : ℝ} (w : NavierStokes.HeatedOutgoing.CompensationWitness F XR C)   (p : NavierStokes.HeatSwitchCone.`
  - `Point`: `OutgoingHistories.Qs_hasDerivAt` : `NavierStokes.OutgoingHistories.Qs_hasDerivAt {d : NavierStokes.OutgoingTail.TailData} {K : ℝ}   (w : NavierStokes.UniformAngularReset.ResetWitness d K) {Amp : ℝ → ℝ} (ha : ContDiff ℝ (↑⊤) Amp)   (p : NavierStok`
  - `RadialParameter`: `ParametricModulation.theta_derivative_asRadialPrimitive` : `NavierStokes.ParametricModulation.theta_derivative_asRadialPrimitive   (Q : NavierStokes.ParametricModulation.RadialParameter × ℝ → ℝ) (hQ : ContDiff ℝ (↑⊤) Q)   (X η θ : ℝ) :   HasDerivAt (fun s => Q ((X, η), `
  - `Plane`: `PressureStream.meanPressure_bar_hasDerivAt` : `NavierStokes.PressureStream.meanPressure_bar_hasDerivAt {S : Type} [NormedAddCommGroup S]   [NormedSpace ℝ S] {d a b M : ℝ} (ha : 0 < a) (hab : a < b) (hd : 0 < d)   (v : NavierStokes.PressureStream.Plane) {f :`
  - `Point`: `Profiles.XW_hasDerivAt` : `NavierStokes.ProfileHistories.Profiles.XW_hasDerivAt   {D : NavierStokes.ProfileHistories.RadialDomain} (P : NavierStokes.ProfileHistories.Profiles D)   (h : ℝ) {p : NavierStokes.ProfileHistories.Point} (hp : p`
- role `1|uses>ContDiffAt|` (held by 193 definitions in the corpus)
  - `Slow`: `AngularData.field_smoothAt` : `NavierStokes.DirectAngularDiagonal.AngularData.field_smoothAt   {U : Set NavierStokes.DirectAngularDiagonal.Slow}   (D : NavierStokes.DirectAngularDiagonal.AngularData U) (hU : IsOpen U)   {w : NavierStokes.Pro`
  - `Point`: `Controls.extendedE_smoothAt` : `NavierStokes.NominalProfile.Controls.extendedE_smoothAt {F : NavierStokes.OutgoingProfile.Profile}   {A : NavierStokes.NominalProfile.AxisStage F} (c : NavierStokes.NominalProfile.Controls A) {B : ℝ}   (w : Nav`
  - `Plane`: `LocalMeanPhysicalBounds.angularField_smoothAt` : `NavierStokes.LocalMeanPhysicalBounds.angularField_smoothAt {h degree a b : ℝ} {N Δ : ℕ}   {U : Set NavierStokes.PhysicalGraphBounds.Plane}   (D : NavierStokes.PhysicalMeanJetBounds.CoherentFamily h degree N Δ U`
  - `Point`: `LeadingStress.axial_smoothAt` : `NavierStokes.LeadingStress.axial_smoothAt {Ω : NavierStokes.ProfileHistories.RadialDomain}   (P : NavierStokes.ProfileHistories.Profiles Ω) (h : ℝ) {w : NavierStokes.ProfileHistories.Point}   (hw : w ∈ Ω.carrie`
  - `Point`: = `RepairConeBounds.physicalE_smoothAt` : `NavierStokes.RepairConeBounds.physicalE_smoothAt {D : NavierStokes.ProfileHistories.RadialDomain}   (P : NavierStokes.ProfileHistories.Profiles D) {p : NavierStokes.RepairConeBounds.Point}   (hp : p ∈ D.carrier`
- role `1|uses>IsOpen|` (held by 31 definitions in the corpus)
  - `Plane`: `ActualMeanPhysicalData.overlap_open` : `NavierStokes.ActualMeanPhysicalData.overlap_open (h : ℝ)   {U : Set NavierStokes.ActualMeanPhysicalData.Plane} (hU : IsOpen U) (n m : ℕ) :   IsOpen (NavierStokes.ActualMeanPhysicalData.overlap h U n m)`
  - `Slow`: = `DirectAngularDiagonal.physicalDomain_open` : `NavierStokes.DirectAngularDiagonal.physicalDomain_open   {U : Set NavierStokes.DirectAngularDiagonal.Slow} (hU : IsOpen U) :   IsOpen (NavierStokes.DirectAngularDiagonal.physicalDomain U)`
  - `Plane`: `PrimaryCopyBridge.copyInterior_isOpen` : `NavierStokes.PrimaryCopyBridge.copyInterior_isOpen {P : Type} [NormedAddCommGroup P]   (g : NavierStokes.CommonCoverSolve.Geometry) (k : NavierStokes.PrimaryCopyBridge.Frequency)   [NormedSpace ℝ P] {Ω : Set (P`
  - `InnerPoint`: = `SimilarityProfile.isOpen_physicalDomain` : `NavierStokes.SimilarityProfile.isOpen_physicalDomain {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   {U : Set NavierStokes.SimilarityProfile.InnerPoint} (hU : IsOpen U) :   IsOpen (NavierStokes.SimilarityProfile.physi`
  - `Inner`: = `BaseResidual.chartedDomain_isOpen` : `NavierStokes.BaseResidual.chartedDomain_isOpen {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   {U : Set NavierStokes.SlowBorelBase.Inner} (hU : IsOpen U) :   IsOpen (NavierStokes.BaseResidual.chartedDomain h U)`
- role `0|Eq>P>L>◊|` (held by 67 definitions in the corpus)
  - `Point`: `NominalProfile.ideal_rows_moments` : `NavierStokes.NominalProfile.ideal_rows_moments (F : NavierStokes.OutgoingProfile.Profile) {r : ℝ}   (hr : 0 ≤ r) (eta : ℝ) :   NavierStokes.NominalProfile.moments (fun p => NavierStokes.NominalProfile.idealU p.`
  - `Plane`: `SignedMeanGain.meanBar_symmetricCovariance` : `NavierStokes.SignedMeanGain.meanBar_symmetricCovariance   (p t : NavierStokes.CorrectionState.Oscillation NavierStokes.SignedMeanGain.Point)   (hp : NavierStokes.LabelSumBounds.AngularContinuous p)   (ht : Navi`
  - `Point`: `SlowStressSupport.dr_sub` : `NavierStokes.SlowStressSupport.dr_sub {S : Set ℝ} (hS : IsOpen S)   {f g : NavierStokes.SlowStressSupport.Field} (hf : NavierStokes.SlowStressSupport.Smooth S f)   (hg : NavierStokes.SlowStressSupport.Smooth S `
  - `Inner`: `BaseResidual.radialPower_eq_monomial` : `NavierStokes.BaseResidual.radialPower_eq_monomial {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2) (c : ℝ)   {z : NavierStokes.ProblemStatement.SpaceTime} (ht : z.1 < 1) :   NavierStokes.BaseResidual.radialPower c z =   `
  - `Plane`: `FourierAlias.torusMean_intervalIntegral` : `NavierStokes.FourierAlias.torusMean_intervalIntegral {F : Type} [NormedAddCommGroup F]   [NormedSpace ℝ F] {g : NavierStokes.FourierAlias.State → F} (hg : Continuous g) {a b : ℝ}   (hab : a ≤ b) :   (NavierStok`
- role `0|Exists>L>K>Q>Q>◊|` (held by 123 definitions in the corpus)
  - `Plane`: `PhysicalGraphBounds.liftedPhase_power_bound` : `NavierStokes.PhysicalGraphBounds.liftedPhase_power_bound {h K Z r0 P B d : ℝ} (hh : 0 ≤ h)   (hh1 : h ≤ 1) (hK : 1 ≤ K) (hZ : 0 ≤ Z) (hr0 : 0 ≤ r0) (hP : 1 ≤ P) (hB : 1 ≤ B) (hd : 0 ≤ d)   (m : ℕ) :   ∃ C,     `
  - `Plane`: `PolarCharts.chart_finiteJets_uniform` : `NavierStokes.PolarCharts.chart_finiteJets_uniform {a : ℝ} (ha : 0 < a) (b : ℝ) (m : ℕ) :   ∃ C,     1 ≤ C ∧       ∀ (j : NavierStokes.PolarCharts.Index),         ∀ k ≤ m,           ∀ p ∈ Metric.closedBall 0 b, `
  - `Plane`: `PhysicalMeanDomain.transport_mass_fiber` : `NavierStokes.PhysicalMeanDomain.transport_mass_fiber {S V : Type} [NormedAddCommGroup S]   [NormedSpace ℝ S] [NormedAddCommGroup V] [NormedSpace ℝ V] {a b cL cR : ℝ} (ha : 0 < a)   (hab : a < b) (hcL : 0 < cL) `
  - `Point`: `ActivationContinuation.angular_endpoint_transfer` : `NavierStokes.ActivationContinuation.angular_endpoint_transfer (N : NavierStokes.ReferencePath.Input)   {ε : ℝ} (hε : 0 < ε) :   ∃ τ > 0,     ∀ {D : NavierStokes.ProfileHistories.RadialDomain}       (P : NavierS`
  - `Plane`: `UniformFourierAlias.realCentered_finiteJets` : `NavierStokes.UniformFourierAlias.realCentered_finiteJets {P : Type} [NormedAddCommGroup P]   [NormedSpace ℝ P] [FiniteDimensional ℝ P] (m : ℕ) :   ∃ K,     0 ≤ K ∧       ∀ (f : P × NavierStokes.TorusInverse.Pla`
- role `3|uses>K|` (held by 134 definitions in the corpus)
  - `Plane`: `GaugeMassPreservation.temporalStage_torusMean_on` : `NavierStokes.GaugeMassPreservation.temporalStage_torusMean_on {coord : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion coord)   (g : NavierStokes.VariableGaugeMean.GaugeData NavierStokes.GaugeMassPreservat`
  - `RadialParameter`: `ParametricModulation.realized_primitive_theta` : `NavierStokes.ParametricModulation.realized_primitive_theta   {a m p₁ p₂ : NavierStokes.ParametricModulation.RadialParameter → ℝ}   {K B : Set NavierStokes.ParametricModulation.RadialParameter}   (r : NavierStok`
  - `Plane`: `CorrectionStep.gaugeRankStage_constructed` : `NavierStokes.CorrectionStep.gaugeRankStage_constructed {coord cL cR A B : ℝ}   (U : NavierStokes.LocalSignedRequest.SlowRegion coord)   (g : NavierStokes.VariableGaugeMean.GaugeData NavierStokes.PressureStream.`
  - `Point`: `ActivationContinuation.nearby_source_jets` : `NavierStokes.ActivationContinuation.nearby_source_jets   {D E : NavierStokes.ProfileHistories.RadialDomain} (P : NavierStokes.ProfileHistories.Profiles D)   (Q : NavierStokes.ProfileHistories.Profiles E) {h j σ`
  - `Plane`: `ActualWaveRegularityData.particular_coefficient_translations` : `NavierStokes.ActualWaveRegularityData.particular_coefficient_translations {B N0 : ℕ}   (l : NavierStokes.ActualParticularStageControls.Label B N0)   (c :     NavierStokes.CorrectionState.Context       (NavierSt`

#### 3. F00003: 52 members, score 56

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1); also F00009, F00021, F00229 (3 overlapping records folded in)
- kinds: 52 abbrev; 49 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 3,004 declarations use a member; 783 theorem statements mention one; 10 member pairs occur together in a statement
- lemma family: 5 identical shapes (10 theorems; 0 shapes held by every member), 23 shared roles (113 theorems; 0 roles held by every member), out of 783 statements about the members
- concept-count estimate: 51 definitions + 5 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 56
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 5 nodes over 1 distinct bodies:

  ```
  Prod Real (Prod Real Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCarrierGeometry.Slow` | 3 | 5 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualCarrierTransportBase.Parameter` | 10 | 37 | `NavierStokes.CorrectionStep.CycleSlow` |
| `NavierStokes.ActualCopySliceRegularity.Parameter` | 7 | 7 | `NavierStokes.PhysicalParticularWave.Parameter` |
| `NavierStokes.ActualInitialExcluded.Slow` | 5 | 19 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualParticularBackground.Parameter` | 0 | 27 | `NavierStokes.CorrectionStep.CycleSlow` |
| `NavierStokes.ActualParticularRealization.Parameter` | 0 | 5 | `NavierStokes.PhysicalParticularWave.Parameter` |
| `NavierStokes.ActualParticularStageControls.Parameter` | 28 | 326 | `NavierStokes.PhysicalParticularWave.Parameter` |
| `NavierStokes.ActualParticularStageControls.Slow` | 0 | 21 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualPhaseDefect.Slow` | 10 | 38 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualPrimaryCovariance.Slow` | 5 | 14 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualSignedGeometry.Slow` | 13 | 471 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualSignedNativeProfiles.Slow` | 4 | 15 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.ActualSignedPhysicalBinding.Slow` | 0 | 9 | `NavierStokes.PhaseCalculus.Slow` |
| `NavierStokes.AllBandBaseJets.Slow` | 7 | 8 | `NavierStokes.PhaseCalculus.Slow` |

… and 38 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|Exists>L>K>Q>◊|` (held by 29 definitions in the corpus)
  - `Chart`: `BaseChartJets.physicalChart_jet_bound` : `NavierStokes.BaseChartJets.physicalChart_jet_bound {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   (lo hi qhi : ℝ) (j : ℕ) :   ∃ C,     0 < C ∧       ∀ (p : NavierStokes.BaseChartJets.Chart),         p.1 < 1 →        `
  - `Slow`: `ActualInitialExcluded.physical_error_fixed` : `NavierStokes.ActualInitialExcluded.physical_error_fixed {F : NavierStokes.OutgoingProfile.Profile}   (W : NavierStokes.NominalProfile.Witness F)   (U : NavierStokes.LocalSignedRequest.SlowRegion (2 * F.data.h))`
  - `Point`: `PhysicalCoordinateBounds.eta_derivative_bound` : `NavierStokes.PhysicalCoordinateBounds.eta_derivative_bound {a : ℝ} (ha : 0 < a) (ha1 : a < 1)   (lo hi qbig : ℝ) (n : ℕ) :   ∃ C,     0 < C ∧       ∀ p ∈ NavierStokes.PhysicalCoordinateBounds.positiveTime,     `
  - `Slow`: `PrimaryTargetBounds.targetAmplitude_lower` : `NavierStokes.PrimaryTargetBounds.targetAmplitude_lower {F : NavierStokes.OutgoingProfile.Profile}   {W : NavierStokes.NominalProfile.Witness F}   {ld : NavierStokes.ModulatedProfileAssembly.LoopData W}   (v : N`
  - `Chart`: `BaseResidual.physical_monomial_bound` : `NavierStokes.BaseResidual.physical_monomial_bound {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   {f : NavierStokes.SlowBorelBase.Inner → ℝ} (hf : ContDiff ℝ (↑⊤) f) (b lo hi qbig : ℝ) (m : ℕ) :   ∃ C,     0 < C ∧    `
- role `3|uses>Filter.EventuallyEq|` (held by 55 definitions in the corpus)
  - `Slow`: `ActualPhaseDefect.periodic_material_germ` : `NavierStokes.ActualPhaseDefect.periodic_material_germ {dimension h : ℝ}   (sys :     NavierStokes.PartitionedCovariance.SlotSystem dimension h       NavierStokes.ActualSignedGeometry.radialVector       NavierSt`
  - `Slow`: `ActualSignedGeometry.periodicPhase_normal_germ` : `NavierStokes.ActualSignedGeometry.periodicPhase_normal_germ {D h : ℝ}   (sys :     NavierStokes.PartitionedCovariance.SlotSystem D h NavierStokes.ActualSignedGeometry.radialVector       NavierStokes.ActualSigne`
  - `CycleSlow`: `ActualWaveRegularityData.particular_corrected_zero_germ` : `NavierStokes.ActualWaveRegularityData.particular_corrected_zero_germ {B N0 : ℕ}   (l : NavierStokes.ActualParticularStageControls.Label B N0)   (c :     NavierStokes.CorrectionState.Context       (NavierStokes.`
  - `Slow`: `NativeCutoffJets.literalCutoff_gaussian_germ` : `NavierStokes.NativeCutoffJets.literalCutoff_gaussian_germ {Label P : Type} [NormedAddCommGroup P]   [NormedSpace ℝ P]   {D : NavierStokes.PhaseJetBounds.Domain (Label × ℕ) NavierStokes.PhaseCalculus.Slow}   (F `
  - `Chart`: `BaseResidual.stressForce_core_germ` : `NavierStokes.BaseResidual.stressForce_core_germ {h r : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   {theta axial : NavierStokes.SlowBorelBase.Chart → ℝ}   (htheta :     ∀ (p : NavierStokes.SlowBorelBase.Chart),       p.`
- role `3|uses>LE.le|` (held by 111 definitions in the corpus)
  - `Slow`: `BasePhaseGeometry.derivative_norm_of_error` : `NavierStokes.BasePhaseGeometry.derivative_norm_of_error   {F F0 : NavierStokes.BasePhaseGeometry.Slow → ℝ} {q : NavierStokes.BasePhaseGeometry.Slow}   {M ε : ℝ} (hM : 0 ≤ M) (hε : ε ^ 2 ≤ 1) (href : ‖fderiv ℝ F`
  - `CycleSlow`: `ActualCycleAssembly.canonical_cutoff_support` : `NavierStokes.ActualCycleAssembly.canonical_cutoff_support {B N0 : ℕ}   (l : NavierStokes.ActualCycleAssembly.Index B N0)   (c :     NavierStokes.CorrectionState.Context       (NavierStokes.CorrectionStep.CycleS`
  - `Slow`: `ActualParticularControl.scaled_selected_copy_energy` : `NavierStokes.ActualParticularControl.scaled_selected_copy_energy {Label P : Type}   [NormedAddCommGroup P] [NormedSpace ℝ P]   {D : NavierStokes.PhaseJetBounds.Domain (Label × ℕ) NavierStokes.PhaseCalculus.Slow`
  - `Slow`: `PhaseEstimates.localBase_shear_error` : `NavierStokes.PhaseEstimates.localBase_shear_error {F G F0 G0 : NavierStokes.PhaseEstimates.Slow → ℝ}   {U : Set NavierStokes.PhaseEstimates.Slow} {M ε diameter : ℝ}   {q q0 : NavierStokes.PhaseEstimates.Slow}  `
  - `Chart`: `SlowBorelBase.physical_composition_bound` : `NavierStokes.SlowBorelBase.physical_composition_bound {V : Type} [NormedAddCommGroup V]   [NormedSpace ℝ V] {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   {F : NavierStokes.SlowBorelBase.Chart → V} (hF : ContDiffOn ℝ`
- role `3|uses>K|` (held by 134 definitions in the corpus)
  - `Slow`: `BasePhaseGeometry.phase_errors_on_mesh` : `NavierStokes.BasePhaseGeometry.phase_errors_on_mesh   {F G F0 G0 : NavierStokes.BasePhaseGeometry.Slow → ℝ}   {U : Set NavierStokes.BasePhaseGeometry.Slow} {q q0 : NavierStokes.BasePhaseGeometry.Slow}   {ε targ`
  - `CycleSlow`: `ActualWaveRegularityData.particular_coefficient_translations` : `NavierStokes.ActualWaveRegularityData.particular_coefficient_translations {B N0 : ℕ}   (l : NavierStokes.ActualParticularStageControls.Label B N0)   (c :     NavierStokes.CorrectionState.Context       (NavierSt`
  - `Slow`: `PhaseEstimates.actual_phase_estimates` : `NavierStokes.PhaseEstimates.actual_phase_estimates   {F G F0 G0 : NavierStokes.PhaseEstimates.Slow → ℝ} {U : Set NavierStokes.PhaseEstimates.Slow}   {q q0 : NavierStokes.PhaseEstimates.Slow} {ε target pz v θ B `
  - `Slow`: `ScaledParticularFrameJets.native_geometry_jets` : `NavierStokes.ScaledParticularFrameJets.native_geometry_jets {Label P : Type} [NormedAddCommGroup P]   [NormedSpace ℝ P]   {D : NavierStokes.PhaseJetBounds.Domain (Label × ℕ) NavierStokes.ScaledParticularFrameJe`
- role `1|uses>HasDerivAt|` (held by 163 definitions in the corpus)
  - `PhysicalPoint`: `SimilarityProfile.hasDerivAt_pullback_s` : `NavierStokes.SimilarityProfile.hasDerivAt_pullback_s {h b : ℝ}   {f : NavierStokes.SimilarityProfile.InnerProfile} (hh : 0 < h) (hh1 : h < 1 / 2)   {p : NavierStokes.SimilarityProfile.PhysicalPoint} (hp : p.1 <`
  - `Chart`: `SlowBorelBase.hasDerivAt_physicalProfile_s` : `NavierStokes.SlowBorelBase.hasDerivAt_physicalProfile_s {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}   (hh : 0 < h) (hh1 : h < 1 / 2) {f : ℕ → NavierStokes.SlowBorelBase.Inner → ℝ}   (hf : ∀ (j : ℕ), ContDiff ℝ (↑⊤)`
  - `PhysicalPoint`: `SlowFirstOrderEdge.physicalChi_hasDerivAt_z` : `NavierStokes.SlowFirstOrderEdge.physicalChi_hasDerivAt_z (d : NavierStokes.OutgoingTail.TailData)   {p : NavierStokes.SlowFirstOrderEdge.PhysicalPoint} (ht : p.1 < 1) :   HasDerivAt (fun z => NavierStokes.SlowF`
  - `PhysicalPoint`: `TerminalStress.timeSlice_hasDerivAt` : `NavierStokes.TerminalStress.timeSlice_hasDerivAt {G : NavierStokes.TerminalStress.PhysicalProfile}   {p : NavierStokes.TerminalStress.PhysicalPoint} (hG : DifferentiableAt ℝ G p) :   HasDerivAt (fun t => G (t, `
- role `1|Eq>P>L>◊|` (held by 25 definitions in the corpus)
  - `ProfilePoint`: `SlowExpansionResidual.omega_finite_expansion` : `NavierStokes.SlowExpansionResidual.omega_finite_expansion {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   (N : ℕ) (f : NavierStokes.SlowExpansionResidual.SlowProfiles)   {p : NavierStokes.AxisymmetricFields.ProfilePoi`
  - `PhysicalPoint`: `SlowResidualMatching.radialDivergence_sum` : `NavierStokes.SlowResidualMatching.radialDivergence_sum.{u_1} {ι : Type u_1} (s : Finset ι) (k : ℝ)   (F : ι → NavierStokes.SimilarityProfile.PhysicalProfile)   (p : NavierStokes.SimilarityProfile.PhysicalPoint)`
  - `Chart`: `SlowBorelBase.blownJet_sum` : `NavierStokes.SlowBorelBase.blownJet_sum.{u_1} {V : Type} [NormedAddCommGroup V] [NormedSpace ℝ V]   {ι : Type u_1} (s : Finset ι) (F : ι → NavierStokes.SlowBorelBase.Chart → V) {q : ℝ}   {w : NavierStokes.SlowB`

#### 4. F00005: 41 members, score 41

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0); also F00025 (1 overlapping records folded in)
- kinds: 41 abbrev; 41 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,409 declarations use a member; 648 theorem statements mention one; 70 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 16 shared roles (108 theorems; 0 roles held by every member), out of 648 statements about the members
- concept-count estimate: 40 definitions + 1 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 41
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 11 nodes over 1 distinct bodies:

  ```
  Prod (Prod Real (Prod (Prod Real Real) (Prod Real Real))) Real
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualBaseResidual.Full` | 13 | 38 | `NavierStokes.ActualBaseResidual.Point × ℝ` |
| `NavierStokes.ActualCandidateConstruction.Full` | 0 | 2 | `NavierStokes.ActualCandidateConstruction.Point × ℝ` |
| `NavierStokes.ActualCurrentCarrierJets.FullPoint` | 1 | 1 | `NavierStokes.CorrectionInitialization.ActualPrimary.FullPoint` |
| `NavierStokes.ActualCycleResidualBounds.Cylinder` | 13 | 23 | `NavierStokes.ActualCycleResidualBounds.Point × ℝ` |
| `NavierStokes.ActualInitialMeanEquation.Full` | 6 | 6 | `NavierStokes.ActualInitialMeanEquation.Point × ℝ` |
| `NavierStokes.ActualMeanPotentialRealization.Cylinder` | 0 | 7 | `NavierStokes.PhysicalResidualTZ.Cylinder` |
| `NavierStokes.ActualParticularStageControls.AP` | 0 | 37 | `NavierStokes.CorrectionInitialization.ActualPrimary.FullPoint` |
| `NavierStokes.ActualPeriodizedSignedRealization.Cylinder` | 3 | 13 | `NavierStokes.PhysicalResidualBridge.Cylinder` |
| `NavierStokes.ActualPhaseDefect.Cylinder` | 5 | 12 | `NavierStokes.PhysicalResidualBridge.Cylinder` |
| `NavierStokes.ActualPhysicalPrefixFields.Cylinder` | 4 | 4 | `NavierStokes.PhysicalResidualBridge.Cylinder` |
| `NavierStokes.ActualPolarCoverage.Cylinder` | 1 | 5 | `NavierStokes.PhysicalResidualJetBounds.Cylinder` |
| `NavierStokes.ActualPrimaryCoherence.ChartPoint` | 46 | 124 | `NavierStokes.LocalSignedRequest.Point × ℝ` |
| `NavierStokes.ActualSignedCoherence.FullPoint` | 24 | 64 | `NavierStokes.ActualSignedCoherence.Point × ℝ` |
| `NavierStokes.ActualSignedCurrentSupport.FullPoint` | 4 | 4 | `NavierStokes.ActualSignedCoherence.FullPoint` |

… and 27 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|Filter.EventuallyEq>L>◊|` (held by 27 definitions in the corpus)
  - `ChartPoint`: `ActualPrimaryCoherence.piece_velocity_zero_germ_nonpositive` : `NavierStokes.ActualPrimaryCoherence.piece_velocity_zero_germ_nonpositive {B N0 : ℕ}   (U :     NavierStokes.LocalSignedRequest.SlowRegion       (2 * NavierStokes.CorrectionInitialization.ActualPrimary.h))   (j `
  - `FullPoint`: `ActualSignedCoherence.common_amplitude_germ` : `NavierStokes.ActualSignedCoherence.common_amplitude_germ {B N0 : ℕ}   (l : NavierStokes.ActualSignedCoherence.SignedLabel B N0)   (u : NavierStokes.CorrectionState.State NavierStokes.ActualSignedCoherence.Point`
  - `Cylinder`: `ActualSignedGeometry.preparedView_normal_germ` : `NavierStokes.ActualSignedGeometry.preparedView_normal_germ   {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F}   (H : NavierStokes.NominalConeAssembly.Certificate W)   {ld :`
  - `FullPoint`: `ActualSignedStageControls.cutoff_zero_germ_outside_time` : `NavierStokes.ActualSignedStageControls.cutoff_zero_germ_outside_time {B N0 : ℕ}   (l : NavierStokes.ActualSignedStageControls.SignedLabel B N0) (n : ℕ)   (k : NavierStokes.ActualSignedStageControls.Frequency)  `
  - `FullPoint`: `ActualWaveRegularityData.mask_zero_germ_outside_carrier` : `NavierStokes.ActualWaveRegularityData.mask_zero_germ_outside_carrier {B N0 : ℕ}   (l : NavierStokes.ActualWaveRegularityData.Index B N0) (n : ℕ)   (k : NavierStokes.TorusInverse.Frequency) {x : NavierStokes.Act`
- role `0|Eq>L>◊|` (held by 21 definitions in the corpus)
  - `ChartPoint`: `ActualPrimaryCoherence.chart_radial_curve` : `NavierStokes.ActualPrimaryCoherence.chart_radial_curve (B n : ℕ) :   (NavierStokes.PrimaryResidualClass.directions           (NavierStokes.CorrectionInitialization.ActualPrimary.commonContext B)).radialField   `
  - `FullPoint`: `ActualSignedCoherence.phase_transport` : `NavierStokes.ActualSignedCoherence.phase_transport {B N0 : ℕ}   (l : NavierStokes.ActualSignedCoherence.SignedLabel B N0) (n m k : ℕ)   (hi :     NavierStokes.CorrectionInitialization.CommonWindow.index        `
  - `Cylinder`: `ActualSignedGeometry.slotCoordinates_affine` : `NavierStokes.ActualSignedGeometry.slotCoordinates_affine   (g : NavierStokes.CommonCoverSolve.Geometry) (k : NavierStokes.TorusInverse.Frequency) :   NavierStokes.ActualSignedGeometry.slotCoordinates g k = fun `
  - `FullPoint`: `ActualCycleResidualBounds.fullPhase_eq_weighted` : `NavierStokes.ActualCycleResidualBounds.fullPhase_eq_weighted {B N0 : ℕ}   (b :     NavierStokes.ActualCycleResidualBounds.Index B N0 →       NavierStokes.CorrectionState.HarmonicBlock NavierStokes.ActualCycleRe`
  - `Cylinder`: `PhysicalResidualTZ.complexBase_swap` : `NavierStokes.PhysicalResidualTZ.complexBase_swap   (c : NavierStokes.CorrectionState.Context NavierStokes.PhysicalResidualTZ.Lift) (n : ℕ) :   NavierStokes.LiftedMeanResidual.complexBase (NavierStokes.PhysicalR`
- role `1|Eq>P>L>◊|` (held by 25 definitions in the corpus)
  - `Full`: `ActualInitialMeanEquation.piece_divergence` : `NavierStokes.ActualInitialMeanEquation.piece_divergence {B N0 : ℕ}   (l : NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0 × Fin 2) (n : ℕ)   {x : NavierStokes.ActualInitialMeanEquation.Full}   (h`
  - `ChartPoint`: `ActualPrimaryCoherence.piece_complex_divergence` : `NavierStokes.ActualPrimaryCoherence.piece_complex_divergence {B N0 : ℕ}   (U :     NavierStokes.LocalSignedRequest.SlowRegion       (2 * NavierStokes.CorrectionInitialization.ActualPrimary.h))   (j : Fin 2) (L `
  - `FullPoint`: `ActualPrimaryDynamics.copy_principal_zero` : `NavierStokes.ActualPrimaryDynamics.copy_principal_zero {B N0 : ℕ} (j : Fin 2)   (L : NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0) (n : ℕ)   (U :     NavierStokes.LocalSignedRequest.SlowRegion`
  - `Cylinder`: `ActualCurrentParticularPhysical.nativeCurl_reindex` : `NavierStokes.ActualCurrentParticularPhysical.nativeCurl_reindex {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState       (NavierStokes.ActualCurrentParticularPhysical.Label B N0))   (l : NavierStokes.`
- role `0|ContDiffOn>L>◊|` (held by 45 definitions in the corpus)
  - `Full`: `ActualBaseResidual.errorAtScale_smooth` : `NavierStokes.ActualBaseResidual.errorAtScale_smooth {F : NavierStokes.OutgoingProfile.Profile}   {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W)   {ld : NavierSt`
  - `Cylinder`: `ActualWaveRegularityData.particular_mode_pressure_smooth` : `NavierStokes.ActualWaveRegularityData.particular_mode_pressure_smooth {B N0 : ℕ}   (l : NavierStokes.ActualParticularStageControls.Label B N0)   (c :     NavierStokes.CorrectionState.Context       (NavierStokes`
  - `Point`: `InitialNativeRegularity.copied_smooth` : `NavierStokes.InitialNativeRegularity.copied_smooth.{u_1} {B N0 : ℕ} {E : Type u_1}   [NormedAddCommGroup E] [NormedSpace ℝ E] (a : ℝ)   (f :     NavierStokes.ActualPrimaryBounds.SignedLabel B N0 → NavierStokes.`
  - `Cylinder`: `ActualBaseResidual.baseComponents_smooth` : `NavierStokes.ActualBaseResidual.baseComponents_smooth {F : NavierStokes.OutgoingProfile.Profile}   {W : NavierStokes.NominalProfile.Witness F} (H : NavierStokes.NominalConeAssembly.Certificate W)   {ld : Navier`
- role `2|Filter.EventuallyEq>L>◊|` (held by 9 definitions in the corpus)
  - `FullPoint`: `ActualSignedGaussian.localGaussian_zero_outside_phaseCell` : `NavierStokes.ActualSignedGaussian.localGaussian_zero_outside_phaseCell {B N0 : ℕ}   (request :     ℕ → NavierStokes.ActualSignedStageControls.FullPoint → NavierStokes.SignedWaveUpdate.Vec2)   (l : NavierStokes.`
  - `FullPoint`: `ActualWaveRegularityData.signed_common_raw_zero_germ_of_not_ordered` : `NavierStokes.ActualWaveRegularityData.signed_common_raw_zero_germ_of_not_ordered {B N0 : ℕ}   (l : NavierStokes.ActualWaveRegularityData.Index B N0)   (request :     ℕ → NavierStokes.ActualWaveRegularityData.Fu`
  - `Point`: `InitialPhysicalData.potentialCoefficient_zero_germ` : `NavierStokes.InitialPhysicalData.potentialCoefficient_zero_germ {B N0 : ℕ}   (l : NavierStokes.InitialPhysicalData.SignedLabel B N0) (n : ℕ)   {x : NavierStokes.InitialPhysicalData.Point}   (ha : (NavierStokes.`
- role `1|uses>IsOpen|` (held by 31 definitions in the corpus)
  - `Cylinder`: `ActualPhysicalPrefixFields.graphSource_open` : `NavierStokes.ActualPhysicalPrefixFields.graphSource_open   (G : NavierStokes.ActualPhysicalPrefixFields.ScaledGraph) (hl : 0 < G.radialScale)   {U : Set NavierStokes.ActualPhysicalPrefixFields.Cylinder} (hU : I`
  - `Cylinder`: `ActualWaveRegularity.nativeDomain_open` : `NavierStokes.ActualWaveRegularity.nativeDomain_open {D : Type} [NormedAddCommGroup D]   [NormedSpace ℝ D] {coord : ℝ} (e : NavierStokes.ActualWaveRegularity.Cylinder ≃ₗᵢ[ℝ] D)   (U : NavierStokes.LocalSignedReq`
  - `Cylinder`: `ScaledGraph.source_open` : `NavierStokes.PhysicalResidualBridge.ScaledGraph.source_open   (G : NavierStokes.PhysicalResidualBridge.ScaledGraph) (hl : 0 < G.radialScale)   {U : Set NavierStokes.PhysicalResidualBridge.Cylinder} (hU : IsOpen`

#### 5. F00006: 28 members, score 37

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0); also F00012, F00013, F00131 (3 overlapping records folded in)
- kinds: 28 abbrev; 27 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 12,066 declarations use a member; 4,550 theorem statements mention one; 71 member pairs occur together in a statement
- lemma family: 8 identical shapes (20 theorems; 0 shapes held by every member), 94 shared roles (798 theorems; 0 roles held by every member), out of 4,550 statements about the members
- concept-count estimate: 27 definitions + 10 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 37
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 4 nodes over 1 distinct bodies:

  ```
  EuclideanSpace Real (Fin 3)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerLiftedGradientSpace.Vector3` | 500 | 3933 | `EuclideanSpace ℝ (Fin 3)` |
| `EulerSmoothLimit.Space` | 2873 | 6196 | `EuclideanSpace ℝ (Fin 3)` |
| `NavierStokes.ActualBaseResidual.Space` | 4 | 5 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualCopySliceRegularity.Space` | 4 | 5 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualPeriodizedSignedRealization.Space` | 3 | 20 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualPrimaryDynamics.Space` | 2 | 12 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualSignedControl.Space` | 0 | 4 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualSignedDynamics.Space` | 0 | 10 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.ActualSignedStageControls.Space` | 0 | 28 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.AnnularEndpoint.Space` | 4 | 7 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.BasePhaseGeometry.Space` | 2 | 3 | `NavierStokes.MovingFrameODE.Space` |
| `NavierStokes.CurlClassBounds.RealVector` | 10 | 120 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.JointResidualLimits.Space` | 5 | 28 | `NavierStokes.ProblemStatement.Space` |
| `NavierStokes.MovingFrameODE.Space` | 21 | 103 | `EuclideanSpace ℝ (Fin 3)` |

… and 14 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|uses>Filter.Tendsto|` (held by 58 definitions in the corpus)
  - `Vector3`: `EulerSobolevL2Product.productApprox_value_tendsto` : `EulerSobolevL2Product.productApprox_value_tendsto (period : ℝ) [Fact (0 < period)] {q : ℕ}   (hq : 6 ≤ q) (L : EulerLiftedGradientSpace.Vector3 →L[ℝ] ℝ)   (u v : ↥(EulerCylinderSobolevSpace.SobolevSpace period `
  - `Space`: `SmoothLimitData.jetPath_convergence` : `EulerOrdinarySobolev.SmoothLimitData.jetPath_convergence {T : ℝ}   {A : ℕ → ↑(Set.Icc 0 T) → EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space}   {hA : ∀ (k n : ℕ), Continuous fun t => (A k t).jetLp n}   `
  - `Space`: `AnnularEndpoint.outerRadius_tendsto_zero` : `NavierStokes.AnnularEndpoint.outerRadius_tendsto_zero {h : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2) (C : ℝ)   {x : NavierStokes.AnnularEndpoint.Space} (hz : x.ofLp 2 = 0) :   Filter.Tendsto (NavierStokes.AnnularEndpoi`
  - `Space`: `OneSidedExtension.jet_tendsto` : `NavierStokes.JointResidualLimits.OneSidedExtension.jet_tendsto.{u_1} {V : Type u_1}   [NormedAddCommGroup V] [NormedSpace ℝ V] {f : NavierStokes.JointResidualLimits.SpaceTime → V}   {x : NavierStokes.JointResid`
  - `Space`: `MixedPeriodicAssembly.boundaryLimits_joint` : `NavierStokes.MixedPeriodicAssembly.boundaryLimits_joint   {A v : NavierStokes.ProblemStatement.VelocityField}   {p : NavierStokes.ProblemStatement.PressureField}   (hz :     NavierStokes.JointResidualLimits.Van`
- role `2|uses>HasDerivAt|` (held by 40 definitions in the corpus)
  - `Vector3`: `SmoothCoefficient.pressure_hasDerivAt` : `EulerSpatialSobolevInverse.SmoothCoefficient.pressure_hasDerivAt {period : ℝ} [Fact (0 < period)]   (A B : EulerSpatialSobolevInverse.SmoothCoefficient period)   (a : EulerLiftedGradientSpace.LiftTangent)   (hB`
  - `Space`: `EulerPacketAngularPotential.potential_hasDerivAt` : `EulerPacketAngularPotential.potential_hasDerivAt (P : ℝ) (m : EulerSmoothLimit.Space)   (A : ℝ → EulerSmoothLimit.Space) (hA : Continuous A) (θ : ℝ) :   HasDerivAt (EulerPacketAngularPotential.potential P m A) `
  - `Space`: `PhaseEstimates.hasDerivAt_normalDirection` : `NavierStokes.PhaseEstimates.hasDerivAt_normalDirection {n : ℝ → NavierStokes.PhaseEstimates.Space}   {n' : NavierStokes.PhaseEstimates.Space} {v : ℝ} (hn : HasDerivAt n n' v)   (hne : NavierStokes.MovingFrameOD`
  - `Space`: `CompactEnergy.energy_hasDerivAt` : `NavierStokesR3.CompactEnergy.energy_hasDerivAt {a b t : ℝ}   {u : NavierStokes.ProblemStatement.VelocityField} {K : Set NavierStokes.ProblemStatement.Space}   (hK : IsCompact K) (hu : ContDiffOn ℝ (↑⊤) u (Navie`
  - `Space`: `CompactTimeIntegral.hasDerivAt_time_of_contDiffOn` : `NavierStokesR3.CompactTimeIntegral.hasDerivAt_time_of_contDiffOn.{u_1} {E : Type u_1}   [NormedAddCommGroup E] [NormedSpace ℝ E] {F : ℝ × NavierStokesR3.ProblemStatement.Space → E}   {a b t : ℝ} (hF : ContDiffO`
- role `1|uses>HasCompactSupport|` (held by 27 definitions in the corpus)
  - `Vector3`: `EulerLiftedCurl.curlTest_compact` : `EulerLiftedCurl.curlTest_compact (period κ : ℝ) (m : EulerLiftedGradientSpace.Vector3) (i j : Fin 3)   (ψ : EulerLiftedGradientSpace.LiftDomain period → ℝ) (hψ : HasCompactSupport ψ) :   HasCompactSupport (Eule`
  - `Space`: `ComparatorBridge.scaledCutoff_compact` : `Euler.ComparatorBridge.scaledCutoff_compact (χ : EulerSmoothLimit.Space → ℝ)   (hχ : HasCompactSupport χ) (R : ℝ) (hR : R ≠ 0) :   HasCompactSupport (Euler.ComparatorBridge.scaledCutoff χ R)`
  - `Space`: `ConservativeDifference.compact_scalarLaplacian` : `NavierStokesR3.ConservativeDifference.compact_scalarLaplacian   {f : NavierStokes.ProblemStatement.Space → ℝ} (hf : HasCompactSupport f) :   HasCompactSupport (NavierStokesR3.ConservativeDifference.scalarLaplac`
  - `Space`: `PressureFluxTest.cutoffTest_hasCompactSupport` : `NavierStokesR3.PressureFluxTest.cutoffTest_hasCompactSupport {R : ℝ} (hR : 0 < R)   (w : NavierStokesR3.ProblemStatement.Space → NavierStokesR3.ProblemStatement.Space) :   HasCompactSupport (NavierStokesR3.Pres`
- role `2|uses>Continuous|` (held by 29 definitions in the corpus)
  - `Vector3`: `EulerVolumeSobolevPath.partitionCoefficient_continuous` : `EulerVolumeSobolevPath.partitionCoefficient_continuous.{u_1} {K : Type u_1} [TopologicalSpace K]   (Y : C(K, C(EulerLiftedGradientSpace.Vector3, EulerLiftedGradientSpace.Vector3))) {n : ℕ}   (hJ : ∀ (i : ℕ), 1 `
  - `Space`: `LabelData.packetForceField_continuous` : `EulerParentPacketFrames.LabelData.packetForceField_continuous.{u_1}   {A : EulerParentPacketFrames.Parent} (L : EulerParentPacketFrames.LabelData A)   (I : EulerParentPacketFrames.ParticleInverse A) {U : Type u`
  - `Space`: `LocalizedTensorBounds.continuous_tensorDiff` : `NavierStokesR3.LocalizedTensorBounds.continuous_tensorDiff   {u v : NavierStokesR3.ProblemStatement.VelocityField} {t : ℝ} (hu : Continuous fun x => u (t, x))   (hv : Continuous fun x => v (t, x)) (i j : Fin 3)`
  - `Space`: `WeightedSobolev.continuous_cutoffGradientAmplitude` : `NavierStokesR3.WeightedSobolev.continuous_cutoffGradientAmplitude   {φ : NavierStokesR3.ProblemStatement.Space → ℝ}   {w : NavierStokesR3.ProblemStatement.Space → NavierStokesR3.ProblemStatement.Space}   (hφ : `
- role `2|uses>ContDiff|` (held by 54 definitions in the corpus)
  - `Vector3`: `EulerMetricTransport.metricEnergy_smooth` : `EulerMetricTransport.metricEnergy_smooth (period : ℝ)   (K :     EulerLiftedGradientSpace.LiftDomain period →       EulerLiftedGradientSpace.Vector3 →L[ℝ] EulerLiftedGradientSpace.Vector3)   (e : EulerLiftedGra`
  - `Space`: `ComparatorBridge.potentialTruncation_smooth` : `Euler.ComparatorBridge.potentialTruncation_smooth   (u : EulerSmoothLimit.Space → EulerSmoothLimit.Space) (hu : ContDiff ℝ (↑⊤) u)   (χ : EulerSmoothLimit.Space → ℝ) (hχ : ContDiff ℝ (↑⊤) χ) :   ContDiff ℝ (↑⊤)`
  - `Space`: `ConservativeDifference.tensorDiff_contDiff` : `NavierStokesR3.ConservativeDifference.tensorDiff_contDiff   {u v : NavierStokes.ProblemStatement.VelocityField} {t : ℝ} (hu : ContDiff ℝ ↑⊤ fun x => u (t, x))   (hv : ContDiff ℝ ↑⊤ fun x => v (t, x)) (i j : Fin`
  - `Space`: `PressureFluxTest.r_smooth` : `NavierStokesR3.PressureFluxTest.r_smooth {φ : NavierStokesR3.ProblemStatement.Space → ℝ}   {w : NavierStokesR3.ProblemStatement.Space → NavierStokesR3.ProblemStatement.Space}   (hφ : ContDiff ℝ (↑⊤) φ) (hw : Co`
- role `1|uses>HasFDerivAt|` (held by 55 definitions in the corpus)
  - `Space`: `BoundedSmoothField.translation_hasFDerivAt` : `EulerMeanCoefficients.BoundedSmoothField.translation_hasFDerivAt.{u} {V : Type u}   [NormedAddCommGroup V] [NormedSpace ℝ V] (A : EulerMeanCoefficients.BoundedSmoothField V)   (a : EulerSmoothLimit.Space) :   H`
  - `Space`: `AxisymmetricFields.hasFDerivAt_radialEnergy` : `NavierStokes.AxisymmetricFields.hasFDerivAt_radialEnergy (x : NavierStokes.ProblemStatement.Space) :   HasFDerivAt NavierStokes.AxisymmetricFields.radialEnergy     (NavierStokes.AxisymmetricFields.radialLinear `
  - `Space`: `SpacetimeEndpoint.hasFDerivAt_extendTrace` : `NavierStokes.SpacetimeEndpoint.hasFDerivAt_extendTrace.{u_1} {V : Type u_1} [NormedAddCommGroup V]   [NormedSpace ℝ V] {T : ℝ} {f : NavierStokes.SpacetimeEndpoint.SpaceTime → V}   {L : NavierStokes.SpacetimeEnd`
  - `Space`: `Comparison.hasFDerivAt_heatKernel` : `NavierStokesR3.Comparison.hasFDerivAt_heatKernel {s : ℝ} (hs : 0 < s)   (z : NavierStokesR3.ProblemStatement.Space) :   HasFDerivAt (NavierStokesR3.Comparison.heatKernel s)     (-(NavierStokesR3.Comparison.heat`

#### 6. F00007: 18 members, score 31

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7, AU@0.5); also F00047, F00407 (2 overlapping records folded in)
- kinds: 18 abbrev; 18 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 993 declarations use a member; 656 theorem statements mention one; 19 member pairs occur together in a statement
- lemma family: 12 identical shapes (29 theorems; 0 shapes held by every member), 7 shared roles (37 theorems; 0 roles held by every member), out of 656 statements about the members
- concept-count estimate: 17 definitions + 14 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 31
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 23 nodes over 1 distinct bodies:

  ```
  Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (ProfileData.outgoing FinalSlowBase.actualProfile))) (NominalConeAssembly.activeLeft (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (NominalConeAssembly.activeRight (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (Prepared.N (Choice.prepared (ActualPrimary.choice p0 p1)))) (Fin 2)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCarrierTransportBase.Index` | 14 | 29 | `NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0 × Fin 2` |
| `NavierStokes.ActualCoreSupport.Index` | 18 | 21 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualCurrentWaveSupport.Index` | 2 | 2 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualCycleAssembly.Index` | 40 | 49 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualCycleParameters.Index` | 18 | 123 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualInitialMean.Index` | 15 | 20 | `NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0 × Fin 2` |
| `NavierStokes.ActualInitialization.Index` | 155 | 332 | `NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0 × Fin 2` |
| `NavierStokes.ActualIntermediateDebtBounds.Index` | 3 | 9 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualParticularCycleData.Index` | 47 | 57 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualParticularMeanGain.Index` | 3 | 33 | `NavierStokes.ActualInitialization.Index B N0` |
| `NavierStokes.ActualSignedCoherence.SignedLabel` | 56 | 68 | `NavierStokes.ActualSignedStageControls.SignedLabel B N0` |
| `NavierStokes.ActualSignedNativeRegularity.Label` | 10 | 11 | `NavierStokes.ActualSignedPhysicalBinding.Label B N0` |
| `NavierStokes.ActualSignedPhysicalBinding.Label` | 54 | 94 | `NavierStokes.ActualSignedStageControls.SignedLabel B N0` |
| `NavierStokes.ActualSignedPhysicalCoherence.Label` | 21 | 31 | `NavierStokes.ActualSignedPhysicalBinding.Label B N0` |

… and 4 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|uses>Or|` (held by 50 definitions in the corpus)
  - `Index`: `ActualCycleAssembly.native_zero_alternative_of_factorization` : `NavierStokes.ActualCycleAssembly.native_zero_alternative_of_factorization {B N0 : ℕ}   (l : NavierStokes.ActualCycleAssembly.Index B N0)   (K : ℕ → Set NavierStokes.ActualCycleAssembly.Point)   (slowCarrier : ℕ`
  - `SignedLabel`: `ActualSignedOutputBounds.phaseCell_or_localized_zero` : `NavierStokes.ActualSignedOutputBounds.phaseCell_or_localized_zero {B N0 : ℕ}   (request :     ℕ → NavierStokes.ActualSignedStageControls.FullPoint → NavierStokes.SignedWaveUpdate.Vec2)   (l : NavierStokes.Actua`
  - `Label`: `ActualSignedUnmaskedBounds.own_phaseCell_or_zero` : `NavierStokes.ActualSignedUnmaskedBounds.own_phaseCell_or_zero {B N0 : ℕ}   (request : ℕ → NavierStokes.ActualSignedUnmaskedBounds.Full → NavierStokes.SignedWaveUpdate.Vec2)   (l : NavierStokes.ActualSignedUnmas`
  - `Index`: `ActualWaveRegularityData.signed_phaseCell_or_zero` : `NavierStokes.ActualWaveRegularityData.signed_phaseCell_or_zero {B N0 : ℕ}   (l : NavierStokes.ActualWaveRegularityData.Index B N0) (n : ℕ)   (k : NavierStokes.TorusInverse.Frequency) {x : NavierStokes.ActualWav`
- role `1|uses>Iff|` (held by 60 definitions in the corpus)
  - `Index`: `ActualCarrierTransportBase.labelCarrier_iff_canonicalSourceRegion` : `NavierStokes.ActualCarrierTransportBase.labelCarrier_iff_canonicalSourceRegion {B N0 : ℕ}   (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0)   (l : NavierStokes.ActualCarrierTransportBase.Index`
  - `Index`: `ActualCoreSupport.mem_refinedCarrier_iff` : `NavierStokes.ActualCoreSupport.mem_refinedCarrier_iff {B N0 : ℕ}   (l : NavierStokes.ActualCoreSupport.Index B N0) (n : ℕ) {x : NavierStokes.ActualCoreSupport.Point}   (hT : 0 < x.2.1.1) :   x ∈ NavierStokes.Ac`
  - `Index`: `ActualCycleAssembly.refined_carrier_factorization` : `NavierStokes.ActualCycleAssembly.refined_carrier_factorization {B N0 : ℕ}   (hN : NavierStokes.ActualCarrierGeometry.geometricThreshold ≤ N0)   (l : NavierStokes.ActualCycleAssembly.Index B N0) (n : ℕ)   (p : N`
  - `SignedLabel`: `ActualSignedStageControls.cells_mem` : `NavierStokes.ActualSignedStageControls.cells_mem {B N0 : ℕ}   (l : NavierStokes.ActualSignedStageControls.SignedLabel B N0) (n : ℕ)   (k : NavierStokes.ActualSignedStageControls.Frequency)   (x : NavierStokes.A`
- role `3|P>L>◊|` (held by 14 definitions in the corpus)
  - `Index`: `ActualCycleAssembly.old_supported` : `NavierStokes.ActualCycleAssembly.old_supported {B N0 : ℕ} {σ : ℝ}   {P : NavierStokes.ActualCycleAssembly.Index B N0 → ℕ → NavierStokes.ActualCycleAssembly.Point → ℝ}   {carrier :     NavierStokes.ActualCycleAs`
  - `Index`: `ActualInitialization.linearGood_uniform_of_identity` : `NavierStokes.ActualInitialization.linearGood_uniform_of_identity (B N0 : ℕ) {γ : ℝ}   (hprimary :     NavierStokes.UniformHarmonicInteraction.UniformVelocity NavierStokes.ActualInitialization.strip       Navier`
  - `SignedLabel`: `ActualSignedStageControls.uniform_select_two` : `NavierStokes.ActualSignedStageControls.uniform_select_two {B N0 : ℕ} {E : Type}   [NormedAddCommGroup E] [NormedSpace ℝ E]   {w :     NavierStokes.ActualSignedStageControls.SignedLabel B N0 →       ℕ → NavierSt`
- role `1|Eq>Finset.sum>L>◊|` (held by 5 definitions in the corpus)
  - `Index`: `ActualCurrentParticularAssembly.particularPressure_eq_sum` : `NavierStokes.ActualCurrentParticularAssembly.particularPressure_eq_sum {B N0 : ℕ}   {x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualInitialization.Index B N0)}   {σ : ℝ} (H : NavierStokes.Actual`
  - `Label`: `ActualSignedPhysicalCoherence.measuredPotential_eq_sum` : `NavierStokes.ActualSignedPhysicalCoherence.measuredPotential_eq_sum {B N0 : ℕ}   (u : NavierStokes.CorrectionState.State NavierStokes.ActualSignedPhysicalCoherence.Point)   (H :     NavierStokes.MeanStateRegula`
- role `1|uses>IsClosed|` (held by 24 definitions in the corpus)
  - `Index`: = `ActualCoreSupport.refinedCarrier_closed` : `NavierStokes.ActualCoreSupport.refinedCarrier_closed {B N0 : ℕ}   (l : NavierStokes.ActualCoreSupport.Index B N0) (n : ℕ) :   IsClosed (NavierStokes.ActualCoreSupport.refinedCarrier l n)`
  - `Index`: = `ActualInitialization.labelCarrier_closed` : `NavierStokes.ActualInitialization.labelCarrier_closed {B N0 : ℕ}   (l : NavierStokes.ActualInitialization.Index B N0) (n : ℕ) :   IsClosed (NavierStokes.ActualInitialization.labelCarrier l n)`
- role `0|K>Q>Q>P>L>◊|` (held by 33 definitions in the corpus)
  - `Index`: `ActualCyclePreservation.signed_block_bounds` : `NavierStokes.ActualCyclePreservation.signed_block_bounds {B N0 : ℕ} {σ : ℝ}   {x : NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualCyclePreservation.Index B N0)}   (first : NavierStokes.ActualParticu`
  - `SignedLabel`: `ActualSignedOutputBounds.actual_block_bounds` : `NavierStokes.ActualSignedOutputBounds.actual_block_bounds {B N0 : ℕ}   (G : NavierStokes.SignedMeanGain.Geometry) (hs : G.strip = NavierStokes.ActualPrimaryBounds.strip)   (c : NavierStokes.CorrectionState.Cont`

#### 7. F00010: 22 members, score 28

*Reading (model, not evidence):* B. Not one idea. Each member is `Classical.choose` / `choice` / `Exists.choose` applied to a different existence proof; the proof is an erased argument, so only the head is compared.

- found by: anti-unification (AU@1.0, AU@0.7, AU@0.5); also F00056, F00552, F00671, F01351, F01400, F01465, F01583 (7 overlapping records folded in)
- kinds: 22 def; 20 modules; instance arguments per member 0–5, type arguments 0–2
- usage: 369 declarations use a member; 147 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 1 identical shapes (3 theorems; 0 shapes held by every member), 5 shared roles (15 theorems; 0 roles held by every member), out of 147 statements about the members
- concept-count estimate: 21 definitions + 2 lemma statements by identical shape (low), or + 7 by role (high); penalty 1; score 28
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 1 nodes over 11 distinct bodies:

  ```
  Classical.choose
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerAllOrderDriftCorrection.Budget.solution` | 5 | 12 | `Classical.choose ⋯` |
| `EulerCylinderSmoothOrbit.representative` | 9 | 23 | `Classical.choose ⋯` |
| `EulerMeanSmoothRepresentative.representative` | 22 | 38 | `Classical.choose ⋯` |
| `EulerOrdinarySobolev.regularizedSolution` | 3 | 6 | `Classical.choose ⋯` |
| `EulerSobolevL2Product.productHq` | 16 | 33 | `Classical.choose ⋯` |
| `EulerSobolevPointEvaluation.representative` | 9 | 26 | `Classical.choose ⋯` |
| `EulerSobolevSmoothing.smoothingDerivative` | 4 | 6 | `Classical.choose ⋯` |
| `NavierStokes.ActualSignedExterior.actualLabel` | 19 | 48 | `Classical.choose ⋯` |
| `NavierStokes.ActualSlowAxis.tubeWidth` | 15 | 55 | `Classical.choose ⋯` |
| `NavierStokes.BorelExtension.localScale` | 1 | 4 | `Classical.choose ⋯` |
| `NavierStokes.BorelExtension.templateBound` | 4 | 9 | `Classical.choose ⋯` |
| `NavierStokes.EntranceAlignedBase.scales` | 3 | 7 | `Classical.choose ⋯` |
| `NavierStokes.GlobalSlowProfiles.step` | 2 | 4 | `Classical.choose ⋯` |
| `NavierStokes.OutgoingPulseBounds.mainBound` | 7 | 24 | `Classical.choose NavierStokes.OutgoingPulseBounds.exists_mainPulse_bound` |

… and 8 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|Eq>◊|HSMul.hSMul` (held by 86 definitions in the corpus)
  - `productHq`: `EulerSobolevL2Product.productHq_smul_right` : `EulerSobolevL2Product.productHq_smul_right (period : ℝ) [Fact (0 < period)] {q : ℕ} (hq : 6 ≤ q)   (L : EulerLiftedGradientSpace.Vector3 →L[ℝ] ℝ) (hL : ‖L‖ ≤ 1)   (u : ↥(EulerCylinderSobolevSpace.SobolevSpace p`
  - `representative`: `EulerSobolevPointEvaluation.representative_smul` : `EulerSobolevPointEvaluation.representative_smul (period : ℝ) [Fact (0 < period)] (c : ℝ)   (u : ↥(EulerCylinderSobolevSpace.SobolevSpace period 3)) :   EulerSobolevPointEvaluation.representative period (c • u) `
  - `smoothingDerivative`: `EulerSobolevSmoothing.smoothingDerivative_smul` : `EulerSobolevSmoothing.smoothingDerivative_smul (period : ℝ) [Fact (0 < period)]   (A : ↥(EulerLiftedGradientSpace.LiftL2 period) →L[ℝ] ↥(EulerLiftedGradientSpace.LiftL2 period))   (C : ℝ)   (hD :     ∀ (i : Fin`
- role `0|LT.lt>Nat.cast>◊|` (held by 4 definitions in the corpus)
  - `localScale`: `BorelExtension.localScale_bound` : `NavierStokes.BorelExtension.localScale_bound.{u_1} {E : Type u_1} [NormedAddCommGroup E]   [NormedSpace ℝ E] (a : ℕ → E) (j : ℕ) :   2 ^ j * NavierStokes.BorelExtension.boundSum j (a j) <     ↑(NavierStokes.Bor`
  - `localScale`: `SpatialBorelExtension.localScale_bound` : `NavierStokes.SpatialBorelExtension.localScale_bound.{u_1, u_2} {X : Type u_1} {V : Type u_2}   [NormedAddCommGroup X] [NormedSpace ℝ X] [FiniteDimensional ℝ X] [NormedAddCommGroup V]   [NormedSpace ℝ V] (a : ℕ `
- role `0|LE.le>HDiv.hDiv>◊|` (held by 47 definitions in the corpus)
  - `derivativeConstant`: `ComparisonCutoffs.cutoff_iteratedFDeriv_le` : `NavierStokesR3.ComparisonCutoffs.cutoff_iteratedFDeriv_le {R : ℝ} (hR : 0 < R) (n : ℕ)   (x : NavierStokesR3.ProblemStatement.Space) :   ‖iteratedFDeriv ℝ n (NavierStokesR3.ComparisonCutoffs.cutoff R) x‖ ≤     `
  - `weightSecondDerivativeConstant`: `LocalizedFluxEstimates.weight_iteratedFDeriv_two_le` : `NavierStokesR3.LocalizedFluxEstimates.weight_iteratedFDeriv_two_le {R : ℝ} (hR : 0 < R)   (x : NavierStokesR3.ProblemStatement.Space) :   ‖iteratedFDeriv ℝ 2 (NavierStokesR3.ComparisonCutoffs.weight R) x‖ ≤    `
- role `0|Eq>◊|Neg.neg` (held by 52 definitions in the corpus)
  - `representative`: `EulerMeanPacketProvider.representative_odd_of_reflection` : `EulerMeanPacketProvider.representative_odd_of_reflection (u : ↥EulerMeanSolenoidal.L2)   (hs : EulerMeanSmoothRepresentative.SmoothOrbit u) (hu : EulerMeanSolenoidal.reflection u = -u)   (x : EulerSmoothLimit.S`
  - `productHq`: `EulerSobolevParityOperators.product_neg_right` : `EulerSobolevParityOperators.product_neg_right (period : ℝ) [Fact (0 < period)] {q : ℕ} (hq : 6 ≤ q)   (L : EulerLiftedGradientSpace.Vector3 →L[ℝ] ℝ) (hL : ‖L‖ ≤ 1)   (u v : ↥(EulerCylinderSobolevSpace.SobolevSp`
- role `0|Filter.EventuallyEq>P>◊|` (held by 78 definitions in the corpus)
  - `representative`: `EulerCylinderSmoothOrbit.strongWord_ae` : `EulerCylinderSmoothOrbit.strongWord_ae (period : ℝ) [Fact (0 < period)]   (u : ↥(EulerLiftedGradientSpace.LiftL2 period))   (hu : EulerCylinderSmoothOrbit.SmoothOrbit period u) {n : ℕ} (w : Fin n → Fin 4) :   ↑`
  - `representative`: `EulerMeanClassicalWordBounds.ordinaryWord_ae` : `EulerMeanClassicalWordBounds.ordinaryWord_ae.{u_1} {ι : Type u_1}   (directions : ι → EulerSmoothLimit.Space) (u : ↥EulerMeanSolenoidal.L2)   (hu : EulerMeanSmoothRepresentative.SmoothOrbit u) {n : ℕ} (w : Fin `

#### 8. F00011: 35 members, score 26

*Reading (model, not evidence):* A. `Fin n → ℝ` under 35 local names for a handful of dimensions n (one numeral hole). Same habit as the product types.

- found by: body (L1); also F00017, F00020, F00022, F00032, F00048, F00135, F00219, F01486 (8 overlapping records folded in)
- kinds: 35 abbrev; 34 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,674 declarations use a member; 545 theorem statements mention one; 12 member pairs occur together in a statement
- lemma family: 14 identical shapes (37 theorems; 0 shapes held by every member), 5 shared roles (21 theorems; 0 roles held by every member), out of 545 statements about the members
- concept-count estimate: 34 definitions + 18 lemma statements by identical shape (low), or + 0 by role (high); penalty 2; score 26
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 3 nodes over 6 distinct bodies:

  ```
  ∀ x0 : (Fin ⟨h1⟩), Real
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ numeral; 6 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `NavierStokes.ActivationContinuation.FieldJet` | 3 | 14 | `4` |
| `NavierStokes.ActivationContinuation.StockJet` | 3 | 12 | `12` |
| `NavierStokes.ActualPeriodizedSignedRealization.Vec2` | 5 | 7 | `2` |
| `NavierStokes.ActualSignedControl.Vec2` | 1 | 7 | (same body as another member) |
| `NavierStokes.ActualSignedMeanBinding.Vec2` | 5 | 11 | (same body as another member) |
| `NavierStokes.ActualSignedPhysicalData.Vec2` | 1 | 3 | (same body as another member) |
| `NavierStokes.AngularMomentReset.Coeff` | 73 | 250 | (same body as another member) |
| `NavierStokes.ExtendedHeatedOutgoing.Coeff` | 17 | 76 | `3` |
| `NavierStokes.FiveProfileMoments.Debt` | 6 | 34 | `5` |
| `NavierStokes.FiveRowRank.Debt` | 18 | 30 | (same body as another member) |
| `NavierStokes.HeatSwitchCone.Coeff` | 13 | 104 | (same body as another member) |
| `NavierStokes.HeatedOutgoing.Coeff` | 56 | 224 | (same body as another member) |
| `NavierStokes.MatchingDebtBounds.Debt` | 2 | 15 | (same body as another member) |
| `NavierStokes.MeanRankUpdate.Debt` | 25 | 39 | (same body as another member) |

… and 21 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|uses>MeasureTheory.IntegrableOn|` (held by 32 definitions in the corpus)
  - `Coeff`: `CorrectedPulseAmplitude.radialEnergy_integrable` : `NavierStokes.CorrectedPulseAmplitude.radialEnergy_integrable   (d : NavierStokes.OutgoingTail.TailData) (c : ℝ → NavierStokes.AngularMomentReset.Coeff)   (amp : ℝ → ℝ) (eta XR : ℝ) (hXR : 0 < XR) :   MeasureThe`
  - `Coeff`: `HeatedOutgoing.patchRow_integrable` : `NavierStokes.HeatedOutgoing.patchRow_integrable (F : NavierStokes.OutgoingProfile.Profile) (XR : ℝ)   (c : ℝ → NavierStokes.HeatedOutgoing.Coeff) (eta : ℝ) (i : Fin 3) (hXR : 0 < XR) :   MeasureTheory.Integrabl`
  - `Debt`: `NominalProfile.corrected_density_integrable` : `NavierStokes.NominalProfile.corrected_density_integrable (F : NavierStokes.OutgoingProfile.Profile)   (U E : NavierStokes.NominalProfile.Field) (debt : ℝ → NavierStokes.NominalProfile.Debt)   (eta r : ℝ)   (hU `
- role `1|uses>MeasureTheory.Integrable|` (held by 37 definitions in the corpus)
  - `Coeff`: `AngularMomentReset.weighted_relative_integrable` : `NavierStokes.AngularMomentReset.weighted_relative_integrable (s : ℝ)   (c : NavierStokes.AngularMomentReset.Coeff) :   MeasureTheory.Integrable     (fun y => Real.exp (s * y) * NavierStokes.AngularMomentReset.r`
  - `Debt`: `PositiveOrderMoments.repairE_power_integrable` : `NavierStokes.PositiveOrderMoments.repairE_power_integrable (lam A a b p : ℝ)   (d : NavierStokes.PositiveOrderMoments.Debt) (ha : 0 < a) (hab : a < b) :   MeasureTheory.Integrable     (fun R => R ^ p * NavierSt`
  - `Coeff`: `TerminalCompensation.weighted_correction_sq_integrable` : `NavierStokes.TerminalCompensation.weighted_correction_sq_integrable   (P : NavierStokes.TerminalCompensation.Patch) (s : ℝ)   (c : NavierStokes.TerminalCompensation.Coeff) :   MeasureTheory.Integrable (fun x =>`
- role `0|Continuous>L>Prod>◊|` (held by 10 definitions in the corpus)
  - `FieldJet`: `ActivationContinuation.densityJet_continuous` : `NavierStokes.ActivationContinuation.densityJet_continuous :   Continuous fun p => NavierStokes.ActivationContinuation.densityJet p.1 p.2`
  - `StockJet`: `ActivationContinuation.clippedStockMap_continuous` : `NavierStokes.ActivationContinuation.clippedStockMap_continuous {h j μ B : ℝ}   (hsmall : NavierStokes.NaturalAxisData.SmallParameters h j) (hμ : 0 < μ)   {S : Set NavierStokes.ProfileHistories.Point} (hX : ∀ p `
- role `0|Exists>L>K>Q>◊|` (held by 29 definitions in the corpus)
  - `Coeff`: `AngularMomentReset.relative_first_jet_bound` : `NavierStokes.AngularMomentReset.relative_first_jet_bound :   ∃ D,     0 < D ∧       ∀ (c : NavierStokes.AngularMomentReset.Coeff) (y : ℝ),         \|NavierStokes.AngularMomentReset.relative c y\| ≤ D * ‖c‖ ∧     `
  - `Coeff`: `TerminalCompensation.correction_derivative_bound` : `NavierStokes.TerminalCompensation.correction_derivative_bound   (P : NavierStokes.TerminalCompensation.Patch) (k : ℕ) :   ∃ C,     0 ≤ C ∧       ∀ (c : NavierStokes.TerminalCompensation.Coeff) (x : ℝ),         `
- role `1|uses>ContinuousOn|` (held by 46 definitions in the corpus)
  - `Vec2`: `PulseBounds.ratio_continuousOn` : `NavierStokes.PulseCovariance.PulseBounds.ratio_continuousOn {r a A b B : ℝ} {ψ x : ℝ → ℝ}   (h : NavierStokes.PulseCovariance.PulseBounds r a A b B ψ x)   {t : ℝ → NavierStokes.PulseCovariance.Vec2}   (ht : ∀ (`
  - `Vec2`: `SmoothCovariance.continuousOn_numerator` : `NavierStokes.SmoothCovariance.continuousOn_numerator.{u_1} {X : Type u_1} [TopologicalSpace X]   {K : Set X} {H : X → NavierStokes.SmoothCovariance.Mat2}   {T : X → NavierStokes.SmoothCovariance.Vec2}   (hH : ∀`

#### 9. F00014: 36 members, score 24

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F02237, F02586, F02587, F03133, F03281, F03285, F04014, F04061 (8 overlapping records folded in)
- kinds: 36 def; 27 modules; instance arguments per member 1–4, type arguments 0–1
- usage: 132 declarations use a member; 55 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 5 shared roles (19 theorems; 0 roles held by every member), out of 55 statements about the members
- concept-count estimate: 35 definitions + 0 lemma statements by identical shape (low), or + 13 by role (high); penalty 2; score 24
- the general form already exists: `EulerPacketCylinderField.Field.congr`; the skeleton below is over its named specialisations
- similarity 0.002 (smallest share of a member outside compound holes), skeleton of 1 nodes over 35 distinct bodies:

  ```
  Field.congr ⟨h1⟩ ⟨h2⟩ ⟨h3⟩ ⟨h4⟩ ⟨h5⟩
  ```
- holes: 5, effective parameters 3; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ parameter ×29, term ×6; 2 distinct values; compound
  - ⟨h2⟩ parameter ×21, term ×14; 4 distinct values; compound
  - ⟨h3⟩ function ×34, parameter ×1; 35 distinct values; compound
  - ⟨h4⟩ function; 35 distinct values; compound
  - ⟨h5⟩ term ×34, parameter ×1; 35 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ | ⟨h4⟩ | ⟨h5⟩ |
|---|---:|---:|---|---|---|---|---|
| `EulerMeanPacketProvider.Forcing.pressureGradientCylinderField` | 5 | 10 | `P` | `Data.T D` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `EulerPacketCylinderField.pressureGradient (Forcing.scalar D ` | `MatrixCoefficient.multiply P (Data.T D) (fun x0 : (Prod Real` |
| `EulerMeanPacketProvider.meanSolveCylinderField` | 0 | 1 | `P` | `Data.T D` | `Forcing.vector D raw Classical.choice` | `Prod.fst (EulerMeanPacketProvider.meanSolve D raw)` | `Forcing.vectorCylinderField P D raw Classical.choice` |
| `EulerPacketCoordinates.pressureField` | 1 | 3 | `P` | `Data.T D` | `(k ^ 2) • (EulerPacketPressure.rawGradient (Inv.inv k) (Data` | `EulerPacketCoordinates.coordinatePressure D k p` | `Field.smul P (Data.T D) (EulerPacketPressure.rawGradient (In` |
| `EulerPacketCylinderField.Field.angularTransport` | 0 | 1 | `P` | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `Field.scalarProduct P T (fun x0 : (Prod Real (Prod (Euclidea` |
| `EulerPacketCylinderField.Field.congr` | 0 | 65 | (the general form) |  |  |  |  |
| `EulerPacketCylinderField.Field.convolution` | 1 | 4 | `P` | `T` | `Finset.sum (Finset.range (M + 1)) (fun x0 : Nat ↦ (Finset.su` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `Field.finsetSum P T (Finset.range (M + 1)) (fun x0 : Nat ↦ (` |
| `EulerPacketCylinderField.Field.evaluateFamily` | 4 | 9 | `P` | `T` | `Finset.sum (Finset.range (M + 1)) (fun x0 : Nat ↦ ((κ ^ x0) ` | `EulerPacketPointJets.fieldSum M κ f` | `Field.finsetSum P T (Finset.range (M + 1)) (fun x0 : Nat ↦ (` |
| `EulerPacketCylinderField.Field.evaluateRemainder` | 1 | 5 | `P` | `T` | `Finset.sum (Finset.erase (Finset.range (M + 1)) 1) (fun x0 :` | `(EulerPacketPointJets.fieldSum M κ f) - (κ • (f 1))` | `Field.finsetSum P T (Finset.erase (Finset.range (M + 1)) 1) ` |
| `EulerPacketCylinderField.Field.linearPart` | 2 | 7 | `P` | `T` | `raw_t + (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `Field.add P T raw_t (fun x0 : (Prod Real (Prod (EuclideanSpa` |
| `EulerPacketCylinderField.Field.slowPressure` | 2 | 7 | `P` | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `MatrixCoefficient.multiply P T (fun x0 : (Prod Real (Prod (E` |
| `EulerPacketCylinderField.Field.sub` | 3 | 7 | `P` | `T` | `raw + -raw'` | `raw - raw'` | `Field.add P T raw -raw' G (Field.neg P T raw' H)` |
| `EulerPacketCylinderField.Field.timeDerivativeField` | 0 | 3 | `P` | `T` | `raw_t` | `EulerPacketCylinderField.rawTimeDerivative T raw` | `H` |
| `EulerPacketCylinderField.PrefixFields.highForce` | 1 | 6 | `P` | `T` | `((EulerPacketProfileRecursion.knownForce O p a) - (EulerPack` | `EulerPacketProfileRecursion.highForce O p a` | `Field.sub P T ((EulerPacketProfileRecursion.knownForce O p a` |
| `EulerPacketCylinderField.PrefixFields.knownForce` | 0 | 5 | `P` | `T` | `-(((fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) ` | `EulerPacketProfileRecursion.knownForce O p a` | `Field.neg P T (((fun x0 : (Prod Real (Prod (EuclideanSpace R` |

… and 22 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|P>P>P>◊|Inv.inv` (held by 13 definitions in the corpus)
  - `primaryRemainderField`: `ProfileRegularity.normalizedRemainder_bound` : `EulerPacketCylinderField.ProfileRegularity.normalizedRemainder_bound {P T : ℝ} [Fact (0 < P)]   {N : ℕ} {a : ℕ → EulerPacketProfileRecursion.Profile} {support : Set EulerSmoothLimit.Space}   (hT : 0 < T)   (G :`
  - `joinedPacketPullbackField`: `EulerPacketCylinderField.joinedPacket_normal_bound` : `EulerPacketCylinderField.joinedPacket_normal_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerT`
  - `joinedResidualField`: `EulerPacketCylinderField.joinedResidual_normalized_bound` : `EulerPacketCylinderField.joinedResidual_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : `
  - `sourcePacketPullbackField`: `EulerPacketCylinderField.forwardPacket_normal_bound` : `EulerPacketCylinderField.forwardPacket_normal_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Euler`
  - `sourceResidualField`: `EulerPacketCylinderField.forwardResidual_normalized_bound` : `EulerPacketCylinderField.forwardResidual_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D :`
- role `0|P>◊|HAdd.hAdd` (held by 14 definitions in the corpus)
  - `evaluateFamily`: `Field.wordBound_evaluate_low_high_scaled` : `EulerPacketCylinderField.Field.wordBound_evaluate_low_high_scaled {P T : ℝ} [Fact (0 < P)] (N : ℕ)   (hN : 1 ≤ N) (κ B C₁ C₂ γ : ℝ) (hκ : 0 ≤ κ) (hB : 0 ≤ B) (hγ : 0 < γ) (hsmall : κ * B ≤ 1 / 2)   (f : ℕ → Eul`
  - `evaluateRemainder`: `Field.wordBound_evaluateRemainder` : `EulerPacketCylinderField.Field.wordBound_evaluateRemainder {P T : ℝ} [Fact (0 < P)] (N : ℕ)   (hN : 1 ≤ N) (κ B C₂ : ℝ) (hκ : 0 ≤ κ) (hB : 0 ≤ B) (hsmall : κ * B ≤ 1 / 2)   (f : ℕ → EulerPacketProfileRecursion.`
  - `fastAdvection`: `PrefixBound.tail_fast_product_bound` : `EulerPacketCylinderField.PrefixBound.tail_fast_product_bound {P T : ℝ} [Fact (0 < P)] {N : ℕ}   {a : ℕ → EulerPacketProfileRecursion.Profile}   {F : EulerPacketCylinderField.PrefixFields P T (N + 1) a} {hT : 0 `
  - `slowAdvection`: `PrefixBound.tail_slow_product_bound` : `EulerPacketCylinderField.PrefixBound.tail_slow_product_bound {P T : ℝ} [Fact (0 < P)] {N : ℕ}   {a : ℕ → EulerPacketProfileRecursion.Profile}   {F : EulerPacketCylinderField.PrefixFields P T (N + 1) a} {hT : 0 `
- role `0|P>◊|Inv.inv` (held by 17 definitions in the corpus)
  - `primaryRemainderField`: `ProfileRegularity.primaryRemainder_bound` : `EulerPacketCylinderField.ProfileRegularity.primaryRemainder_bound {P T : ℝ} [Fact (0 < P)] {N : ℕ}   {a : ℕ → EulerPacketProfileRecursion.Profile} {support : Set EulerSmoothLimit.Space} (hT : 0 < T)   (G : (i :`
  - `covectorRemainderField`: `EulerPacketPressure.covectorRemainder_bound` : `EulerPacketPressure.covectorRemainder_bound {P T : ℝ} [Fact (0 < P)] {N : ℕ}   {a : ℕ → EulerPacketProfileRecursion.Profile} {support : Set EulerSmoothLimit.Space} (hT : 0 < T)   (m : EulerSmoothLimit.Space)   `
  - `forwardInitializedPrimaryRemainderField`: `EulerPacketTerminalDatum.forwardInitializedPrimaryRemainder_bound` : `EulerPacketTerminalDatum.forwardInitializedPrimaryRemainder_bound.{u_1}   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerTransvers`
  - `initializedPrimaryRemainderField`: `EulerPacketTerminalDatum.initializedPrimaryRemainder_bound` : `EulerPacketTerminalDatum.initializedPrimaryRemainder_bound.{u_1} (M : EulerMeanPacketProvider.Data)   {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]   (D : EulerTransversePacket`
- role `0|Membership.mem>DFunLike.coe>P>◊|` (held by 24 definitions in the corpus)
  - `pressureField`: `EulerPacketCoordinates.pressureField_mem` : `EulerPacketCoordinates.pressureField_mem.{u_1} {P : ℝ} [Fact (0 < P)] {U : Type u_1}   [NormedAddCommGroup U] [InnerProductSpace ℝ U] (D : EulerTransversePacketProvider.Data U) (k : ℝ)   (hk : k ≠ 0) {p : Euler`
  - `joinedPacketPullbackField`: `EulerPacketCylinderField.joinedPacketPullbackField_mem` : `EulerPacketCylinderField.joinedPacketPullbackField_mem.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Eu`
  - `sourcePacketPullbackField`: `EulerPacketCylinderField.sourcePacketPullbackField_mem` : `EulerPacketCylinderField.sourcePacketPullbackField_mem.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Eu`
- role `0|P>P>◊|Inv.inv` (held by 8 definitions in the corpus)
  - `joinedPacketPullbackField`: `EulerPacketCylinderField.joinedPacket_normalized_bound` : `EulerPacketCylinderField.joinedPacket_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Eu`
  - `sourcePacketPullbackField`: `EulerPacketCylinderField.forwardPacket_normalized_bound` : `EulerPacketCylinderField.forwardPacket_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : E`

#### 10. F00015: 15 members, score 22

*Reading (model, not evidence):* D. The class-like case. Fifteen predicates on sequences or coefficient families with different bodies and the same closure lemmas (`add`, `sub`, `neg`, `mul`, `smul`, directional derivative). No parameter merges them; a structure or class stating the closure laws would. Whether each lemma pair is an instance of one statement is unchecked.

- found by: lemma roles (ROLE@0.15); also F00018, F00024, F00034, F00059, F00142, F00427, F00710, F01211 (8 overlapping records folded in)
- kinds: 10 def, 5 structure; 14 modules; instance arguments per member 0–4, type arguments 0–3
- usage: 906 declarations use a member; 690 theorem statements mention one; 26 member pairs occur together in a statement
- lemma family: 17 identical shapes (42 theorems; 0 shapes held by every member), 14 shared roles (159 theorems; 2 roles held by every member), out of 690 statements about the members
- concept-count estimate: 14 definitions + 21 lemma statements by identical shape (low), or + 96 by role (high); penalty 5; score 22
- no common body (the generalisation is a single hole): a shared interface would have to be a structure or class, not a parameter

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation` | 19 | 22 | `∀ (j : ℤ), NavierStokes.ActualWaveRegularity.TranslationOn U v (a.coeff j)` |
| `NavierStokes.CorrectionStep.GaugeSupported` | 24 | 37 | `∀ (n : ℕ), NavierStokes.VariableGaugeMean.SupportedGauge a b ell U (f n)` |
| `NavierStokes.DefectIncrementBounds.Shell` | 24 | 28 | `(∀ x0 : Nat, (ContDiff Real (WithTop.some Top.top) (f x0))) ∧ (∀ x0 : Nat, (RadialAlias.RadiallySupported a b ` |
| `NavierStokes.GaugeDebtIncrement.Regular` | 48 | 56 | `(MeanIncrementBounds.SmoothOn (PhysicalMeanDomain.slowDomain (SlowRegion.carrier U)) f) ∧ (∀ x0 : Nat, (Variab` |
| `NavierStokes.GaugeMomentBalances.MovingField` | 162 | 286 | `(∀ x0 : Nat, (ContDiffOn Real (WithTop.some Top.top) (f x0) (PhysicalMeanDomain.slowDomain (SlowRegion.carrier` |
| `NavierStokes.HarmonicFields.BandLimited` | 43 | 69 | `∀ j ∈ c.support, j.natAbs ≤ N` |
| `NavierStokes.HarmonicResidual.SmoothCoefficients` | 66 | 88 | `∀ (j : ℤ), ContDiffOn ℝ (↑⊤) (c.coeff j) U` |
| `NavierStokes.HarmonicSourceSupport.NonzeroSupported` | 21 | 21 | `∀ (j : ℤ), j ≠ 0 → ∀ x ∉ K, c.coeff j x = 0` |
| `NavierStokes.LocalRankDefect.LocalShell` | 41 | 61 | `(MeanIncrementBounds.SmoothOn (PhysicalMeanDomain.slowDomain U) f) ∧ (∀ x0 : Nat, (PhysicalMeanDomain.Supporte` |
| `NavierStokes.MeanIncrementBounds.SmoothOn` | 93 | 182 | `∀ (n : ℕ), ContDiffOn ℝ (↑⊤) (f n) U` |
| `NavierStokes.MeanStateRegularity.Periodic` | 13 | 13 | `∀ (n : ℕ), NavierStokes.PhysicalMeanDomain.PeriodicOn U (f n)` |
| `NavierStokes.MovingMomentBounds.Support` | 16 | 20 | `∀ (n : ℕ), NavierStokes.VariableGaugeMean.SupportedGauge a b ell U (f n)` |
| `NavierStokes.PhysicalResidualNaturality.CoefficientsOn` | 24 | 26 | `∀ (j : ℤ), ∀ x ∈ U, c.coeff j x = a • d.coeff j (e x)` |
| `NavierStokes.PhysicalResidualNaturality.ScalarOn` | 37 | 62 | `∀ x ∈ U, f x = a * g (e x)` |

… and 1 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `2|◊|HSub.hSub` (held by 30 definitions in the corpus)
  - `CoefficientsTranslation`: `CoefficientsTranslation.sub` : `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.sub {D : Type} [NormedAddCommGroup D]   {U : Set D} {v : D} {a b : NavierStokes.HarmonicFields.Coefficients D}   (ha : NavierStokes.ActualCyclePeriodi`
  - `GaugeSupported`: = `GaugeSupported.sub` : `NavierStokes.CorrectionStep.GaugeSupported.sub {S : Type} {a b : ℝ} {ell : S → ℝ} {U : Set S}   {f g : NavierStokes.CorrectionStep.ScalarField (NavierStokes.PressureStream.Lift S)}   (hf : NavierStokes.Correcti`
  - `Shell`: `Shell.sub` : `NavierStokes.DefectIncrementBounds.Shell.sub {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ}   {f g :     NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds.Point`
  - `Regular`: `Regular.sub` : `NavierStokes.GaugeDebtIncrement.Regular.sub {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.Regu`
  - `MovingField`: `MovingField.sub` : `NavierStokes.MeanStateRegularity.MovingField.sub {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBalanc`
- role `2|◊|HAdd.hAdd` (held by 54 definitions in the corpus)
  - `CoefficientsTranslation`: `CoefficientsTranslation.add` : `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.add {D : Type} [NormedAddCommGroup D]   {U : Set D} {v : D} {a b : NavierStokes.HarmonicFields.Coefficients D}   (ha : NavierStokes.ActualCyclePeriodi`
  - `GaugeSupported`: = `GaugeSupported.add` : `NavierStokes.CorrectionStep.GaugeSupported.add {S : Type} {a b : ℝ} {ell : S → ℝ} {U : Set S}   {f g : NavierStokes.CorrectionStep.ScalarField (NavierStokes.PressureStream.Lift S)}   (hf : NavierStokes.Correcti`
  - `Shell`: `Shell.add` : `NavierStokes.DefectIncrementBounds.Shell.add {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ}   {f g :     NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds.Point`
  - `Regular`: = `Regular.add` : `NavierStokes.GaugeDebtIncrement.Regular.add {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.Regu`
  - `MovingField`: = `MovingField.add` : `NavierStokes.MeanStateRegularity.MovingField.add {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBalanc`
- role `1|◊|Neg.neg` (held by 23 definitions in the corpus)
  - `CoefficientsTranslation`: `CoefficientsTranslation.neg` : `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.neg {D : Type} [NormedAddCommGroup D]   {U : Set D} {v : D} {a : NavierStokes.HarmonicFields.Coefficients D}   (ha : NavierStokes.ActualCyclePeriodici`
  - `GaugeSupported`: = `GaugeSupported.neg` : `NavierStokes.CorrectionStep.GaugeSupported.neg {S : Type} {a b : ℝ} {ell : S → ℝ} {U : Set S}   {f : NavierStokes.CorrectionStep.ScalarField (NavierStokes.PressureStream.Lift S)}   (hf : NavierStokes.Correction`
  - `Shell`: `Shell.neg` : `NavierStokes.DefectIncrementBounds.Shell.neg {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ}   {f : NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds.Point P)}  `
  - `Regular`: = `Regular.neg` : `NavierStokes.GaugeDebtIncrement.Regular.neg {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.Regula`
  - `MovingField`: = `MovingField.neg` : `NavierStokes.MeanStateRegularity.MovingField.neg {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBalances`
- role `1|◊|HMul.hMul` (held by 25 definitions in the corpus)
  - `GaugeSupported`: `GaugeSupported.mul_left` : `NavierStokes.CorrectionStep.GaugeSupported.mul_left {S : Type} {a b : ℝ} {ell : S → ℝ} {U : Set S}   {f : NavierStokes.CorrectionStep.ScalarField (NavierStokes.PressureStream.Lift S)}   (hf : NavierStokes.Corre`
  - `Shell`: `Shell.inv_mul` : `NavierStokes.DefectIncrementBounds.Shell.inv_mul {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ}   {f : NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds.Point P`
  - `Regular`: `Regular.band_mul` : `NavierStokes.GaugeDebtIncrement.Regular.band_mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.R`
  - `MovingField`: `MovingField.inv_mul` : `NavierStokes.MeanStateRegularity.MovingField.inv_mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBala`
  - `BandLimited`: `HarmonicResidual.band_mul_constant` : `NavierStokes.HarmonicResidual.band_mul_constant {D : Type}   {c : NavierStokes.HarmonicResidual.Coefficients D} {N : ℕ}   (hc : NavierStokes.HarmonicFields.BandLimited c N) (f : D → ℂ) :   NavierStokes.Harmonic`
- role `1|◊|HSMul.hSMul` (held by 17 definitions in the corpus)
  - `GaugeSupported`: = `GaugeSupported.smul` : `NavierStokes.CorrectionStep.GaugeSupported.smul {S : Type} {a b : ℝ} {ell : S → ℝ} {U : Set S}   {f : NavierStokes.CorrectionStep.ScalarField (NavierStokes.PressureStream.Lift S)}   (hf : NavierStokes.Correctio`
  - `Shell`: `Shell.smul` : `NavierStokes.DefectIncrementBounds.Shell.smul {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ}   {f : NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds.Point P)} `
  - `Regular`: = `Regular.smul` : `NavierStokes.GaugeDebtIncrement.Regular.smul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.Regul`
  - `MovingField`: = `MovingField.smul` : `NavierStokes.MeanStateRegularity.MovingField.smul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBalance`
  - `LocalShell`: `LocalShell.smul` : `NavierStokes.LocalRankDefect.LocalShell.smul {P : Type} [NormedAddCommGroup P] [NormedSpace ℝ P]   {a b : ℝ} {U : Set P}   {f : NavierStokes.LocalRankDefect.ScalarField (NavierStokes.LocalRankDefect.Point P)}  `
- role `2|◊|HMul.hMul` (held by 21 definitions in the corpus)
  - `CoefficientsTranslation`: `CoefficientsTranslation.mul` : `NavierStokes.ActualCyclePeriodicity.CoefficientsTranslation.mul {D : Type} [NormedAddCommGroup D]   {U : Set D} {v : D} {a b : NavierStokes.HarmonicFields.Coefficients D}   (ha : NavierStokes.ActualCyclePeriodi`
  - `Regular`: = `Regular.mul` : `NavierStokes.GaugeDebtIncrement.Regular.mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.GaugeDebtIncrement.Scalar}   (hf : NavierStokes.GaugeDebtIncrement.Regu`
  - `MovingField`: = `MovingField.mul` : `NavierStokes.MeanStateRegularity.MovingField.mul {coord a b : ℝ}   {U : NavierStokes.LocalSignedRequest.SlowRegion coord}   {f g : NavierStokes.MeanStateRegularity.Scalar}   (hf : NavierStokes.GaugeMomentBalanc`
  - `SmoothCoefficients`: `SmoothCoefficients.mul` : `NavierStokes.HarmonicResidual.SmoothCoefficients.mul {D : Type} [NormedAddCommGroup D]   [NormedSpace ℝ D] {U : Set D} {c d : NavierStokes.HarmonicResidual.Coefficients D}   (hc : NavierStokes.HarmonicResidual.`
  - `NonzeroSupported`: `NonzeroSupported.mul` : `NavierStokes.HarmonicSourceSupport.NonzeroSupported.mul {D : Type} {K : Set D}   {c d : NavierStokes.HarmonicFields.Coefficients D}   (hc : NavierStokes.HarmonicSourceSupport.NonzeroSupported K c)   (hd : Navie`

#### 11. F00016: 20 members, score 21

*Reading (model, not evidence):* B. Not one idea. Each member is `Classical.choose` / `choice` / `Exists.choose` applied to a different existence proof; the proof is an erased argument, so only the head is compared.

- found by: body (L3); anti-unification (AU@1.0, AU@0.7, AU@0.5); also F01412, F01446 (2 overlapping records folded in)
- kinds: 20 def; 20 modules; instance arguments per member 0–4, type arguments 0–1
- usage: 938 declarations use a member; 340 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 1 shared roles (7 theorems; 0 roles held by every member), out of 340 statements about the members
- concept-count estimate: 19 definitions + 0 lemma statements by identical shape (low), or + 2 by role (high); penalty 1; score 21
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 1 nodes over 18 distinct bodies:

  ```
  Classical.choice
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerBaseDatum.FirstScaleGuards.packet` | 0 | 6 | `Classical.choice ⋯` |
| `EulerCylinderSobolevSpace.toJet` | 41 | 131 | `Classical.choice ⋯` |
| `EulerLinearFundamentalExistence.fundamentalPath` | 11 | 29 | `Classical.choice ⋯` |
| `EulerMeanPacketProvider.Data.evolution` | 0 | 1 | `Classical.choice ⋯` |
| `EulerOrdinarySobolev.smoothLimitData` | 0 | 3 | `Classical.choice ⋯` |
| `EulerPacketCylinderField.joinedProfileWitness` | 0 | 4 | `Classical.choice ⋯` |
| `EulerPacketCylinderField.profileWitness` | 0 | 4 | `Classical.choice ⋯` |
| `EulerPacketInduction.Stage.chooseForward` | 0 | 8 | `have hsec := ⋯; Classical.choice ⋯` |
| `EulerPacketInduction.Stage.chooseJoined` | 0 | 9 | `have hsec := ⋯; Classical.choice ⋯` |
| `EulerPacketInduction.constructionScales` | 12 | 21 | `Classical.choice EulerPacketInduction.constructionScales._proof_1` |
| `EulerPacketTerminalDatum.forwardInitializedPressureBudget` | 0 | 4 | `Classical.choice ⋯` |
| `EulerPacketTerminalDatum.initializedPressureBudget` | 0 | 4 | `Classical.choice ⋯` |
| `NavierStokes.ActualSlowAxis.constructedTube` | 2 | 6 | `Classical.choice ⋯` |
| `CorrectionInitialization.ActualPrimary.choice` | 269 | 683 | `Classical.choice ⋯` |

… and 6 more members (all in `clusters.jsonl`).

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|LE.le>P>P>◊|` (held by 50 definitions in the corpus)
  - `constructionScales`: `EulerPacketInduction.lifespan_le_packet_horizon` : `EulerPacketInduction.lifespan_le_packet_horizon (n : ℕ) :   EulerPacketInduction.lifespan.duration ≤ (EulerPacketInduction.packets n).parent.T`
  - `choice`: `ActualInitialExcluded.nativeGaussian_source_support` : `NavierStokes.ActualInitialExcluded.nativeGaussian_source_support {B N0 : ℕ}   (l : NavierStokes.ActualPrimaryBounds.SignedLabel B N0) :   Function.support (NavierStokes.ActualInitialExcluded.nativeGaussian l) ⊆`

#### 12. F00019: 7 members, score 20

*Reading (model, not evidence):* F. The exponent `1/2 + h` under seven names in seven modules, verbatim.

- found by: body (L0, L1, L2, L3); also F00070, F00117, F00223 (3 overlapping records folded in)
- kinds: 7 def; 7 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 828 declarations use a member; 270 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 10 shared roles (61 theorems; 0 roles held by every member), out of 270 statements about the members
- concept-count estimate: 6 definitions + 0 lemma statements by identical shape (low), or + 14 by role (high); penalty 1; score 20
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 5 nodes over 1 distinct bodies:

  ```
  (1 / 2) + p0
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.CoordinateAlgebra.A` | 212 | 643 | `1 / 2 + h` |
| `NavierStokes.ExponentLedger.waveExponent` | 0 | 5 | `1 / 2 + σ` |
| `NavierStokes.HeatTailEdit.exponent` | 15 | 29 | `1 / 2 + h` |
| `NavierStokes.NaturalAxisData.A` | 4 | 41 | `1 / 2 + h` |
| `NavierStokes.RenormalizedHeatMoment.A` | 12 | 33 | `1 / 2 + h` |
| `NavierStokes.StressAlgebra.velocityExponent` | 9 | 42 | `1 / 2 + h` |
| `NavierStokes.TerminalPressure.amplitudeExponent` | 18 | 45 | `1 / 2 + h` |

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|Eq>HMul.hMul>HPow.hPow>Neg.neg>◊|` (held by 6 definitions in the corpus)
  - `A`: `ActualCurrentParticularAssembly.velocityMap_apply` : `NavierStokes.ActualCurrentParticularAssembly.velocityMap_apply (n : ℕ)   (v : NavierStokes.PhysicalResidualBridge.Cylinder → Fin 3 → ℝ)   (z : NavierStokes.ProblemStatement.SpaceTime) (k : Fin 3) :   ((NavierSt`
  - `exponent`: `ParametricHeatTail.physicalEdit_heat_carrier` : `NavierStokes.ParametricHeatTail.physicalEdit_heat_carrier (d : NavierStokes.OutgoingTail.TailData)   {K q s τ eta : ℝ} (hK : 0 < K) (hq : 0 < q) (hs : 0 < s)   (hν : NavierStokes.ParametricHeatTail.diffusion et`
  - `A`: `RenormalizedHeatMoment.heatCarrier_scaling` : `NavierStokes.RenormalizedHeatMoment.heatCarrier_scaling (h C : ℝ) {q τ ν r : ℝ} (hq : 0 < q)   (hr : 0 < r) (hν : ν = τ / q) :   q ^ (-NavierStokes.RenormalizedHeatMoment.A h) *       NavierStokes.RenormalizedH`
  - `amplitudeExponent`: `TerminalPressure.physicalEdit_eq_released_carrier` : `NavierStokes.TerminalPressure.physicalEdit_eq_released_carrier   (d : NavierStokes.OutgoingTail.TailData) {K : ℝ} (hK : 0 < K)   {p : NavierStokes.SimilarityProfile.PhysicalPoint} (ht : p.1 < 1) (hs : 0 < p.2.1`
- role `0|Eq>HMul.hMul>HMul.hMul>HPow.hPow>◊|` (held by 15 definitions in the corpus)
  - `A`: `BaseRadialJets.normalizedStream_deriv_Z` : `NavierStokes.BaseRadialJets.normalizedStream_deriv_Z {a : ℕ → ℕ} (ha : StrictMono a) {h C Q : ℝ}   (hh : 0 < h) (hh1 : h < 1 / 2) (hQ : 0 < Q) {d : NavierStokes.SlowBorelBase.Coefficients}   (hd : NavierStokes.`
  - `exponent`: `HeatedOutgoing.E_eventual_heat` : `NavierStokes.HeatedOutgoing.E_eventual_heat (F : NavierStokes.OutgoingProfile.Profile) (XR : ℝ)   (c : ℝ → NavierStokes.HeatedOutgoing.Coeff) (eta X : ℝ) (hXR : 0 < XR) (hX : 0 < X)   (hlate : 3 ≤ Real.log (X /`
  - `A`: `RenormalizedHeatMoment.weighted_referencePower_nonneg_radius` : `NavierStokes.RenormalizedHeatMoment.weighted_referencePower_nonneg_radius {h : ℝ} (hh1 : h < 1 / 2)   (C : ℝ) {r : ℝ} (hr : 0 ≤ r) :   r ^ 2 * NavierStokes.RenormalizedHeatMoment.referencePower h C r =     C * `
- role `0|Eq>HMul.hMul>HMul.hMul>HMul.hMul>HPow.hPow>◊|` (held by 24 definitions in the corpus)
  - `A`: `ActualPrimaryCovariance.viewTangent_pair_covariance` : `NavierStokes.ActualPrimaryCovariance.viewTangent_pair_covariance {B N0 : ℕ} (n : ℕ)   {x : NavierStokes.ActualPrimaryCovariance.Point}   (hx :     x ∈       (NavierStokes.BaseContextAssembly.nativeStrip        `
  - `exponent`: `HeatTailEdit.outgoingEdit_heat_factorization` : `NavierStokes.HeatTailEdit.outgoingEdit_heat_factorization (d : NavierStokes.OutgoingTail.TailData)   (ν eta : ℝ) {K X : ℝ} (hK : 0 < K) (hX : 0 < X) (hfull : 1 / 2 ≤ Real.log (X / K) + 1 / 5) :   NavierStokes.H`
  - `amplitudeExponent`: `TerminalPressure.swirlCoefficient_sq` : `NavierStokes.TerminalPressure.swirlCoefficient_sq (C h : ℝ) (f : ℝ → ℝ)   {p : NavierStokes.SimilarityProfile.PhysicalPoint} (hs : 0 < p.2.1) :   NavierStokes.TerminalStress.swirlCoefficient C h f p ^ 2 =     C`
- role `0|Eq>HMul.hMul>HPow.hPow>HSub.hSub>Neg.neg>◊|` (held by 2 definitions in the corpus)
  - `A`: `AlignedProfileSpectralCone.modulated_frequency_eq` : `NavierStokes.AlignedProfileSpectralCone.modulated_frequency_eq   {F : NavierStokes.OutgoingProfile.Profile} {W : NavierStokes.NominalProfile.Witness F}   (H : NavierStokes.NominalConeAssembly.Certificate W)   {`
  - `amplitudeExponent`: `TerminalHistoryBridge.physical_forwardAxial_eq_terminal` : `NavierStokes.TerminalHistoryBridge.physical_forwardAxial_eq_terminal   (F : NavierStokes.OutgoingProfile.Profile) {XR C B t r z : ℝ}   (hF : NavierStokes.OutgoingProfile.Specification F B)   (w : NavierStokes.H`
- role `0|Eq>P>Neg.neg>◊|` (held by 2 definitions in the corpus)
  - `A`: `SlowBorelBase.partialS_integratedStream` : `NavierStokes.SlowBorelBase.partialS_integratedStream {a : ℕ → ℕ} (ha : StrictMono a) {h : ℝ}   (hh : 0 < h) (hh1 : h < 1 / 2) {d : NavierStokes.SlowBorelBase.Coefficients}   (hd : NavierStokes.SlowBorelBase.Smo`
  - `A`: `RenormalizedHeatMoment.uTheta_eq_similarity_pullback` : `NavierStokes.RenormalizedHeatMoment.uTheta_eq_similarity_pullback (h : ℝ) (E : ℝ × ℝ → ℝ)   (t r z : ℝ) :   NavierStokes.RenormalizedHeatMoment.uTheta h E t r z =     NavierStokes.SimilarityProfile.pullback h (`
- role `0|Eq>P>P>Neg.neg>◊|` (held by 2 definitions in the corpus)
  - `A`: `SlowExpansionResidual.transport_finiteProfile` : `NavierStokes.SlowExpansionResidual.transport_finiteProfile {h e : ℝ} (hh : 0 < h) (hh1 : h < 1 / 2)   (N : ℕ) (α m : ℝ) (v u f source : ℕ → NavierStokes.SimilarityProfile.InnerProfile)   {p : NavierStokes.Axisy`
  - `amplitudeExponent`: `TerminalHistoryBridge.physicalLog_angularResidual` : `NavierStokes.TerminalHistoryBridge.physicalLog_angularResidual   (F : NavierStokes.OutgoingProfile.Profile) {XR C : ℝ}   (w : NavierStokes.HeatedOutgoing.CompensationWitness F XR C)   {p : NavierStokes.Similari`

#### 13. F00023: 6 members, score 18

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); also F00033, F00082 (2 overlapping records folded in)
- kinds: 6 abbrev; 6 modules; instance arguments per member 0–0, type arguments 1–1
- usage: 1,031 declarations use a member; 212 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 10 identical shapes (26 theorems; 0 shapes held by every member), 1 shared roles (3 theorems; 0 roles held by every member), out of 212 statements about the members
- concept-count estimate: 5 definitions + 13 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 18
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 5 nodes over 1 distinct bodies:

  ```
  ∀ x0 : Nat, (∀ x1 : p0, Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.CorrectionState.ScalarField` | 63 | 572 | `NavierStokes.MeanIncrementBounds.Field D` |
| `NavierStokes.CorrectionStep.ScalarField` | 18 | 40 | `NavierStokes.MeanIncrementBounds.Field D` |
| `NavierStokes.DefectIncrementBounds.ScalarField` | 23 | 48 | `NavierStokes.MeanIncrementBounds.Field D` |
| `NavierStokes.LocalRankDefect.ScalarField` | 32 | 62 | `NavierStokes.MeanIncrementBounds.Field D` |
| `NavierStokes.MeanIncrementBounds.Field` | 65 | 519 | `ℕ → D → ℝ` |
| `NavierStokes.SignedMeanGain.ScalarField` | 11 | 51 | `NavierStokes.MeanIncrementBounds.Field D` |

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `1|uses>MeasureTheory.Integrable|` (held by 37 definitions in the corpus)
  - `ScalarField`: `Shell.sliceIntegrable` : `NavierStokes.DefectIncrementBounds.Shell.sliceIntegrable {P : Type} [NormedAddCommGroup P]   [NormedSpace ℝ P] {a b : ℝ}   {f : NavierStokes.DefectIncrementBounds.ScalarField (NavierStokes.DefectIncrementBounds`
  - `ScalarField`: `LocalShell.sliceIntegrable` : `NavierStokes.LocalRankDefect.LocalShell.sliceIntegrable {P : Type} [NormedAddCommGroup P]   [NormedSpace ℝ P] {a b : ℝ} {U : Set P}   {f : NavierStokes.LocalRankDefect.ScalarField (NavierStokes.LocalRankDefect.`

#### 14. F00026: 3 members, score 16.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00087, F00235 (2 overlapping records folded in)
- kinds: 3 def; 3 modules; instance arguments per member 0–4, type arguments 0–1
- usage: 198 declarations use a member; 104 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 19 shared roles (72 theorems; 0 roles held by every member), out of 104 statements about the members
- concept-count estimate: 2 definitions + 0 lemma statements by identical shape (low), or + 31 by role (high); penalty 2; score 16.5
- the general form already exists: `EulerPacketProfileRecursion.profiles`; the skeleton below is over its named specialisations
- similarity 0.067 (smallest share of a member outside compound holes), skeleton of 1 nodes over 2 distinct bodies:

  ```
  EulerPacketProfileRecursion.profiles ⟨h1⟩ ⟨h2⟩
  ```
- holes: 2, effective parameters 1; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ term; 2 distinct values; compound
  - ⟨h2⟩ parameter ×1, term ×1; 2 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `EulerPacketCylinderField.joinedSourceProfiles` | 41 | 77 | `EulerPacketCylinderField.joinedSourceOperators P M D τ B` | `primary` |
| `EulerPacketCylinderField.sourceProfiles` | 48 | 97 | `EulerPacketCylinderField.sourceOperators P M D I` | `EulerPacketCylinderField.homogeneousPrimary P D Iprimary (Eu` |
| `EulerPacketProfileRecursion.profiles` | 15 | 52 | (the general form) |  |

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `0|Eq>DFunLike.coe>Prod.snd>P>P>◊|` (held by 2 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketCylinderField.joinedSource_meanPressure_angle_all` : `EulerPacketCylinderField.joinedSource_meanPressure_angle_all.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (`
  - `sourceProfiles`: `EulerPacketCylinderField.source_meanPressure_angle` : `EulerPacketCylinderField.source_meanPressure_angle.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerT`
- role `0|P>HSMul.hSMul>L>DFunLike.coe>Finset.sum>◊|` (held by 4 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketCylinderField.joinedTailSum_normalized_bound` : `EulerPacketCylinderField.joinedTailSum_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : E`
  - `sourceProfiles`: `EulerPacketCylinderField.forwardTailSum_normalized_bound` : `EulerPacketCylinderField.forwardTailSum_normalized_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : `
- role `0|P>L>DFunLike.coe>HSMul.hSMul>L>◊|` (held by 4 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketCylinderField.joinedPacket_normal_bound` : `EulerPacketCylinderField.joinedPacket_normal_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerT`
  - `sourceProfiles`: `EulerPacketCylinderField.forwardPacket_normal_bound` : `EulerPacketCylinderField.forwardPacket_normal_bound.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Euler`
- role `0|P>L>DFunLike.coe>P>P>◊|HSMul.hSMul` (held by 4 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketTerminalDatum.initializedPacketField_odd` : `EulerPacketTerminalDatum.initializedPacketField_odd.{u_1} (M : EulerMeanPacketProvider.Data)   {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]   (D : EulerTransversePacketProvide`
  - `sourceProfiles`: `EulerPacketTerminalDatum.forwardInitializedPacketField_odd` : `EulerPacketTerminalDatum.forwardInitializedPacketField_odd.{u_1} (M : EulerMeanPacketProvider.Data)   {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U] [CompleteSpace U]   (D : EulerTransversePacket`
- role `0|Eq>P>HSMul.hSMul>L>DFunLike.coe>◊|HSMul.hSMul` (held by 5 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketTerminalDatum.initializedNormalizedField_tower_eq` : `EulerPacketTerminalDatum.initializedNormalizedField_tower_eq.{u_1}   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerTransversePack`
  - `sourceProfiles`: `EulerPacketTerminalDatum.forwardInitializedNormalizedField_tower_eq` : `EulerPacketTerminalDatum.forwardInitializedNormalizedField_tower_eq.{u_1}   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : EulerTransve`
- role `0|Eq>P>L>DFunLike.coe>P>◊|` (held by 5 definitions in the corpus)
  - `joinedSourceProfiles`: `EulerPacketCylinderField.joinedMeanPullback_divergence` : `EulerPacketCylinderField.joinedMeanPullback_divergence.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Eu`
  - `sourceProfiles`: `EulerPacketCylinderField.sourceMeanPullback_divergence` : `EulerPacketCylinderField.sourceMeanPullback_divergence.{u_1} (P : ℝ) [Fact (0 < P)]   (M : EulerMeanPacketProvider.Data) {U : Type u_1} [NormedAddCommGroup U] [InnerProductSpace ℝ U]   [CompleteSpace U] (D : Eu`

#### 15. F00027: 13 members, score 16

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7, AU@0.5)
- kinds: 13 abbrev; 13 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 713 declarations use a member; 428 theorem statements mention one; 10 member pairs occur together in a statement
- lemma family: 4 identical shapes (10 theorems; 0 shapes held by every member), 5 shared roles (22 theorems; 0 roles held by every member), out of 428 statements about the members
- concept-count estimate: 12 definitions + 4 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 16
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 23 nodes over 1 distinct bodies:

  ```
  Prod (Fin 2) (BaseChartJets.CellIndex (TailData.h (Profile.data (ProfileData.outgoing FinalSlowBase.actualProfile))) (NominalConeAssembly.activeLeft (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (NominalConeAssembly.activeRight (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (Prepared.N (Choice.prepared (ActualPrimary.choice p0 p1))))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCopySliceRegularity.Label` | 8 | 8 | `NavierStokes.ActualParticularStageControls.Label B N0` |
| `NavierStokes.ActualCurrentCarrierJets.Label` | 6 | 12 | `NavierStokes.ActualPrimaryBounds.SignedLabel B N0` |
| `NavierStokes.ActualCurrentParticularBounds.Label` | 15 | 16 | `NavierStokes.ActualParticularStageControls.Label B N0` |
| `NavierStokes.ActualCurrentParticularPhysical.Label` | 41 | 60 | `NavierStokes.ActualParticularStageControls.Label B N0` |
| `NavierStokes.ActualCycleParameters.ParticularIndex` | 2 | 32 | `NavierStokes.ActualParticularStageControls.Label B N0` |
| `NavierStokes.ActualParticularBackground.Label` | 5 | 12 | `NavierStokes.ActualPrimaryBounds.SignedLabel B N0` |
| `NavierStokes.ActualParticularStageControls.Label` | 140 | 246 | `Fin 2 × NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0` |
| `NavierStokes.ActualPhaseJetBounds.SignedLabel` | 7 | 31 | `NavierStokes.ActualPrimaryBounds.SignedLabel B N0` |
| `NavierStokes.ActualPrimaryBounds.SignedLabel` | 108 | 226 | `Fin 2 × NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0` |
| `NavierStokes.ActualSignedStageControls.PulseLabel` | 7 | 26 | `Fin 2 × NavierStokes.CorrectionInitialization.ActualPrimary.Label B N0` |
| `NavierStokes.CurrentParticularLabelBounds.Label` | 7 | 11 | `NavierStokes.ActualCurrentParticularPhysical.Label B N0` |
| `NavierStokes.CurrentPhysicalModeGerms.Label` | 4 | 4 | `NavierStokes.ActualCurrentParticularPhysical.Label B N0` |
| `NavierStokes.InitialPhysicalData.SignedLabel` | 78 | 112 | `NavierStokes.ActualPrimaryBounds.SignedLabel B N0` |

Parallel lemmas, side by side (one block per shared role; `=` marks a statement that is identical, hole for hole, to one about another member):

- role `2|uses>Or|` (held by 16 definitions in the corpus)
  - `Label`: `ActualCurrentParticularBounds.common_control_or_zero` : `NavierStokes.ActualCurrentParticularBounds.common_control_or_zero {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualCurrentParticularBounds.Label B N0))   (hs : NavierStokes.Actua`
  - `Label`: `ActualParticularStageControls.data_control_alternative` : `NavierStokes.ActualParticularStageControls.data_control_alternative {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0))   (hs : NavierStokes.Act`
- role `2|uses>Not|` (held by 18 definitions in the corpus)
  - `Label`: `ActualCurrentParticularPhysical.native_normal_ne` : `NavierStokes.ActualCurrentParticularPhysical.native_normal_ne {B N0 : ℕ}   {x :     NavierStokes.CorrectionStep.CycleState       (NavierStokes.ActualCurrentParticularPhysical.Label B N0)}   (hx : NavierStokes.A`
  - `Label`: `ActualParticularDynamics.native_normal_ne` : `NavierStokes.ActualParticularDynamics.native_normal_ne {B N0 : ℕ}   {x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0)}   (H : NavierStokes.ActualParticularD`
- role `1|P>L>◊|` (held by 19 definitions in the corpus)
  - `Label`: `ActualParticularGaussian.source_complement` : `NavierStokes.ActualParticularGaussian.source_complement {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0))   (hs : NavierStokes.ActualParticula`
  - `SignedLabel`: `ActualPrimaryBounds.copied_uniformLocalJets` : `NavierStokes.ActualPrimaryBounds.copied_uniformLocalJets.{u_1} {B N0 : ℕ} {E : Type u_1}   [NormedAddCommGroup E] [NormedSpace ℝ E] {a α : ℝ}   {f :     NavierStokes.ActualPrimaryBounds.SignedLabel B N0 → Navie`
- role `1|Eq>P>L>◊|` (held by 25 definitions in the corpus)
  - `Label`: `ActualParticularStageControls.native_background_eq` : `NavierStokes.ActualParticularStageControls.native_background_eq {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0))   (j : ℤ) :   (NavierStokes.`
  - `SignedLabel`: `ActualPrimaryBounds.periodized_pressure_eq` : `NavierStokes.ActualPrimaryBounds.periodized_pressure_eq {B N0 : ℕ}   (l : NavierStokes.ActualPrimaryBounds.SignedLabel B N0) (n : ℕ)   {x : NavierStokes.ActualPrimaryBounds.Native}   (hx : x ∈ NavierStokes.Actu`
- role `2|uses>ContDiffAt|` (held by 40 definitions in the corpus)
  - `Label`: `ActualCurrentParticularPhysical.localPotentialMode_contDiffAt_of_native` : `NavierStokes.ActualCurrentParticularPhysical.localPotentialMode_contDiffAt_of_native {B N0 : ℕ}   (x :     NavierStokes.CorrectionStep.CycleState       (NavierStokes.ActualCurrentParticularPhysical.Label B N0))`
  - `Label`: `ActualParticularDynamics.data_phase_smoothAt` : `NavierStokes.ActualParticularDynamics.data_phase_smoothAt {B N0 : ℕ}   {x :     NavierStokes.CorrectionStep.CycleState (NavierStokes.ActualParticularStageControls.Label B N0)}   (H : NavierStokes.ActualParticul`

#### 16. F00028: 18 members, score 15.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00088, F00244, F00323, F00510, F00512, F00603, F00607, F00816 … (15 overlapping records folded in)
- kinds: 17 def, 1 abbrev; 11 modules; instance arguments per member 3–4, type arguments 1–1
- usage: 272 declarations use a member; 159 theorem statements mention one; 36 member pairs occur together in a statement
- lemma family: 7 identical shapes (14 theorems; 0 shapes held by every member), 8 shared roles (26 theorems; 0 roles held by every member), out of 159 statements about the members
- concept-count estimate: 17 definitions + 7 lemma statements by identical shape (low), or + 14 by role (high); penalty 2; score 15.5
- the general form already exists: `EulerCylinderSmoothOrbit.pointField`; the skeleton below is over its named specialisations
- no common body (the generalisation is a single hole): a shared interface would have to be a structure or class, not a parameter

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerCylinderPotential.potentialField` | 2 | 5 | `EulerCylinderSmoothOrbit.pointField P (EulerCylinderPotential.potentialPath P B p) ⋯ t` |
| `EulerCylinderSlowCurl.field` | 1 | 4 | `EulerCylinderSmoothOrbit.pointField P (EulerCylinderSlowCurl.path P G p) ⋯ t` |
| `EulerCylinderSmoothOrbit.pointField` | 49 | 182 | `(EulerSobolevPointEvaluation.pointEvaluation period x)   ((EulerCylinderSmoothOrbit.sobolevPath period 3 p hp)` |
| `EulerSourceCylinderClassical.derivativeField` | 5 | 8 | `EulerCylinderSmoothOrbit.pointField period   ((EulerLpCylinderPaths.includePath period S hS)     (EulerSourceC` |
| `EulerSourceCylinderClassical.field` | 7 | 20 | `EulerCylinderSmoothOrbit.pointField period   ((EulerLpCylinderPaths.includePath period S hS)     (EulerSourceC` |
| `EulerTransversePacketJoin.corrector` | 3 | 5 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketJoin.correctorPath τ hτ hτT B G) ⋯ (D.clamp z.1)  ` |
| `EulerTransversePacketJoin.correctorDerivative` | 2 | 5 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketJoin.correctorTimePath τ hτ hτT B G) ⋯   (D.clamp ` |
| `EulerTransversePacketJoin.vector` | 18 | 31 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketJoin.velocityPath τ hτ hτT B G) ⋯ (D.clamp z.1)   ` |
| `EulerTransversePacketJoin.vectorDerivative` | 5 | 9 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketJoin.derivativePath τ hτ hτT B G) ⋯ (D.clamp z.1) ` |
| `EulerTransversePacketPrimary.corrector` | 3 | 5 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketPrimary.correctorPath τ hτ hτT B Y) ⋯   (D.clamp z` |
| `EulerTransversePacketPrimary.correctorDerivative` | 2 | 5 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketPrimary.correctorTimePath τ hτ hτT B Y) ⋯   (D.cla` |
| `EulerTransversePacketPrimary.vector` | 36 | 69 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketPrimary.velocityPath τ hτ hτT B Y) ⋯ (D.clamp z.1)` |
| `EulerTransversePacketPrimary.vectorDerivative` | 4 | 9 | `EulerCylinderSmoothOrbit.pointField P (EulerTransversePacketPrimary.derivativePath τ hτ hτT B Y) ⋯   (D.clamp ` |
| `EulerTransversePacketProvider.Forcing.corrector` | 5 | 11 | `EulerCylinderSmoothOrbit.pointField P (G.correctorPath I) ⋯ (D.clamp z.1) (z.2.1, ↑z.2.2)` |

… and 4 more members (all in `clusters.jsonl`).

#### 17. F00029: 15 members, score 15

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1)
- kinds: 15 abbrev; 15 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,686 declarations use a member; 820 theorem statements mention one; 6 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 10 shared roles (66 theorems; 0 roles held by every member), out of 820 statements about the members
- concept-count estimate: 14 definitions + 1 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 15
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 3 nodes over 1 distinct bodies:

  ```
  Prod Int Int
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualPeriodizedSignedRealization.Frequency` | 6 | 18 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedMeanBinding.Frequency` | 1 | 2 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedNativeBounds.Copy` | 22 | 28 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedNativeProfiles.Frequency` | 5 | 6 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedPhysicalCoherence.Frequency` | 5 | 10 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedPhysicalData.Frequency` | 35 | 118 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedPhysicalZeros.Frequency` | 10 | 12 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedStageControls.Frequency` | 101 | 276 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedUnmaskedBinding.Copy` | 11 | 11 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualSignedUnmaskedBounds.Copy` | 16 | 32 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.ActualWaveCoefficientPeriodicity.Frequency` | 6 | 7 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.InitialNativeRegularity.Frequency` | 9 | 12 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.InitialPhysicalData.Frequency` | 60 | 130 | `NavierStokes.TorusInverse.Frequency` |
| `NavierStokes.PrimaryCopyBridge.Frequency` | 16 | 33 | `NavierStokes.TorusInverse.Frequency` |

… and 1 more members (all in `clusters.jsonl`).

#### 18. F00030: 2 members, score 14.4

*Reading (model, not evidence):* E. Two builds of one operator record (`sourceOperators`, `joinedSourceOperators`) that differ in one field, with 17 shared lemma roles.

- found by: anti-unification (AU@0.7, AU@0.5); lemma roles (ROLE@0.5, ROLE@0.35, ROLE@0.25, ROLE@0.15)
- kinds: 2 def; 2 modules; instance arguments per member 4–4, type arguments 1–1
- usage: 257 declarations use a member; 125 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 17 shared roles (73 theorems; 17 roles held by every member), out of 125 statements about the members
- concept-count estimate: 1 definitions + 0 lemma statements by identical shape (low), or + 35 by role (high); penalty 2.5; score 14.4
- similarity 0.878 (smallest share of a member outside compound holes), skeleton of 36 nodes over 2 distinct bodies:

  ```
  Operators.mk (Set.Icc 0 (Data.T p0)) p1 (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real)) ↦ (DFunLike.coe (DFunLike.coe (SmoothCoefficientPath.field (Data.FInv p2)) (Data.clamp p2 (Prod.fst x0))) (Prod.fst (Prod.snd x0)))) (Data.strain p2) (Data.normalField p2) (EulerMeanPacketProvider.meanSolve p0) ⟨h1⟩ (Data.curlCorrector p2 p1)
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ function; 2 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerPacketCylinderField.joinedSourceOperators` | 61 | 126 | `EulerTransversePacketJoin.highSolve P D τ B` |
| `EulerPacketCylinderField.sourceOperators` | 64 | 133 | `EulerTransversePacketProvider.highSolve P D I` |

#### 19. F00031: 15 members, score 14

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7, AU@0.5)
- kinds: 15 abbrev; 15 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 349 declarations use a member; 233 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 233 statements about the members
- concept-count estimate: 14 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 14
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 27 nodes over 1 distinct bodies:

  ```
  fun x0 : Nat ↦ (fun x1 : Nat ↦ (Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (ProfileData.outgoing FinalSlowBase.actualProfile))) (NominalConeAssembly.activeLeft (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (NominalConeAssembly.activeRight (ProfileData.outgoing FinalSlowBase.actualProfile) (ProfileData.nominal FinalSlowBase.actualProfile)) (Prepared.N (Choice.prepared (ActualPrimary.choice x0 x1)))) (Fin 2)))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCandidateConstruction.Index` | 2 | 37 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualCycleCoherence.Index` | 32 | 43 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualCyclePeriodicity.Index` | 10 | 13 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualCyclePreservation.Index` | 38 | 55 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualCycleResidualBounds.Index` | 44 | 49 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualSignedCurrentSupport.Index` | 6 | 6 | `NavierStokes.ActualInitialization.Index` |
| `NavierStokes.ActualSignedExterior.Label` | 17 | 43 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedFamilySupport.Label` | 6 | 8 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedNativeBounds.Label` | 28 | 36 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedNativeProfiles.Label` | 7 | 8 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedPhysicalZeros.Label` | 19 | 19 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedReferenceGeometry.Label` | 0 | 5 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedUnmaskedBinding.Label` | 3 | 4 | `NavierStokes.ActualSignedPhysicalBinding.Label` |
| `NavierStokes.ActualSignedWaveData.Label` | 15 | 32 | `NavierStokes.ActualSignedPhysicalBinding.Label` |

… and 1 more members (all in `clusters.jsonl`).

#### 20. F00035: 3 members, score 12.4

*Reading (model, not evidence):* E. Three nested data structures that share 13 identical lemma shapes. They occur together in 919 statements, so much of the overlap may be the same lemmas seen through each structure; not read further.

- found by: lemma shapes (API@5, API@3, API@2); also F00090 (1 overlapping records folded in)
- kinds: 3 structure; 3 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 4,680 declarations use a member; 3,568 theorem statements mention one; 919 member pairs occur together in a statement
- lemma family: 13 identical shapes (151 theorems; 5 shapes held by every member), 23 shared roles (156 theorems; 3 roles held by every member), out of 3,568 statements about the members
- concept-count estimate: 2 definitions + 60 lemma statements by identical shape (low), or + 0 by role (high); penalty 5; score 12.4
- similarity 0.2 (smallest share of a member outside compound holes), skeleton of 5 nodes over 3 distinct bodies:

  ```
  ∃ x0 : ⟨h1⟩, (∃ x1 : Real, ⟨h2⟩)
  ```
- holes: 2, effective parameters 1; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ type; 3 distinct values
  - ⟨h2⟩ prop; 3 distinct values; depends on a bound variable, so the parameter must be a function; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `NavierStokes.OutgoingProfile.Profile` | 1461 | 3065 | `OutgoingTail.TailData` | `∃ x0 : (UniformAngularReset.ResetWitness ⟨bound↑2⟩ ⟨bound↑1⟩` |
| `NavierStokes.OutgoingSchedule.Parameters` | 521 | 1057 | `Real` | `∃ x0 : Real, (∃ x1 : Real, ((0 < ⟨bound↑2⟩) ∧ (0 < ⟨bound↑1⟩` |
| `NavierStokes.OutgoingTail.TailData` | 1586 | 3018 | `OutgoingSchedule.Parameters` | `(0 < ⟨bound↑1⟩) ∧ ((2 * ⟨bound↑1⟩) < (Parameters.lam ⟨bound↑` |

#### 21. F00036: 5 members, score 12

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0); also F00057, F00122 (2 overlapping records folded in)
- kinds: 5 abbrev; 5 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 127 declarations use a member; 67 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 7 identical shapes (16 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 67 statements about the members
- concept-count estimate: 4 definitions + 8 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 12
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 13 nodes over 1 distinct bodies:

  ```
  ∀ x0 : Nat, (∀ x1 : (Prod Real (Prod (Prod Real Real) (Prod Real Real))), Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualMeanPhysicalData.Scalar` | 13 | 38 | `ℕ → NavierStokes.ActualMeanPhysicalData.Point → ℝ` |
| `NavierStokes.GaugeDebtIncrement.Scalar` | 21 | 49 | `NavierStokes.MeanIncrementBounds.Field NavierStokes.GaugeDebtIncrement.Point` |
| `NavierStokes.GaugeRadialResidualBounds.Scalar` | 1 | 2 | `NavierStokes.MeanIncrementBounds.Field NavierStokes.GaugeRadialResidualBounds.Point` |
| `NavierStokes.MeanStageRegularity.Scalar` | 5 | 5 | `NavierStokes.MeanIncrementBounds.Field NavierStokes.MeanStageRegularity.Point` |
| `NavierStokes.MeanStateRegularity.Scalar` | 27 | 39 | `NavierStokes.MeanIncrementBounds.Field NavierStokes.MeanStateRegularity.Point` |

#### 22. F00037: 13 members, score 12

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0); also F00051, F00063 (2 overlapping records folded in)
- kinds: 13 abbrev; 13 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 629 declarations use a member; 136 theorem statements mention one; 1 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 3 shared roles (13 theorems; 0 roles held by every member), out of 136 statements about the members
- concept-count estimate: 12 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 12
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 9 nodes over 1 distinct bodies:

  ```
  Prod (Prod Real (Prod Real Real)) (Prod Real Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualParticularRealization.Associated` | 0 | 4 | `NavierStokes.ActualParticularRealization.Parameter × NavierStokes.ActualParticularRealization.Plane` |
| `NavierStokes.ActualPrimaryBounds.Native` | 26 | 110 | `NavierStokes.ActualSignedGeometry.Native` |
| `NavierStokes.ActualPrimaryDynamics.Native` | 9 | 43 | `NavierStokes.ActualSignedGeometry.Native` |
| `NavierStokes.ActualSignedDynamics.Native` | 3 | 5 | `NavierStokes.ActualSignedGeometry.Native` |
| `NavierStokes.ActualSignedGeometry.Native` | 38 | 167 | `NavierStokes.ActualSignedGeometry.Slow × NavierStokes.ActualSignedGeometry.Plane` |
| `NavierStokes.ActualSignedStageControls.Native` | 3 | 62 | `NavierStokes.ActualSignedGeometry.Native` |
| `CorrectionInitialization.ActualPrimary.AbsolutePoint` | 3 | 174 | `NavierStokes.PhaseCalculus.Slow × NavierStokes.TorusInverse.Plane` |
| `NavierStokes.NativeBandExtension.Native` | 29 | 77 | `NavierStokes.WaveEdgeExtension.NativePoint` |
| `NavierStokes.PhaseCalculus.Slot` | 14 | 64 | `NavierStokes.PhaseCalculus.Slow × ℝ × ℝ` |
| `NavierStokes.PhysicalGraphBounds.Slot` | 2 | 26 | `NavierStokes.PhaseCalculus.Slot` |
| `NavierStokes.PhysicalResidualNaturality.Associated` | 3 | 14 | `NavierStokes.PhysicalParticularWave.Parameter × NavierStokes.TorusInverse.Plane` |
| `NavierStokes.PrimaryMaterialDefect.Slot` | 1 | 1 | `NavierStokes.PhaseCalculus.Slot` |
| `NavierStokes.WaveEdgeExtension.NativePoint` | 5 | 33 | `NavierStokes.PhaseCalculus.Slow × NavierStokes.TorusInverse.Plane` |

#### 23. F00038: 13 members, score 12

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0); also F00086 (1 overlapping records folded in)
- kinds: 13 abbrev; 13 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 170 declarations use a member; 67 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 67 statements about the members
- concept-count estimate: 12 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 12
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 6 nodes over 1 distinct bodies:

  ```
  Matrix (Fin 2) (Fin 2) Real
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualPeriodizedSignedRealization.Mat2` | 3 | 3 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.ActualSignedControl.Mat2` | 1 | 1 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.ActualSignedMeanBinding.Mat2` | 0 | 1 | `NavierStokes.SignedWaveUpdate.Mat2` |
| `NavierStokes.ActualSignedPhysicalData.Mat2` | 1 | 1 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.PartitionedCovariance.Mat2` | 2 | 15 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.PhysicalSignedWave.Mat2` | 7 | 14 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.PrimaryCovarianceBounds.Mat2` | 8 | 17 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.PrimaryTargetBounds.Mat2` | 2 | 11 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.PulseCovariance.Mat2` | 0 | 4 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.SignedCopyBounds.Mat2` | 7 | 12 | `NavierStokes.SignedWaveUpdate.Mat2` |
| `NavierStokes.SignedCovariance.Mat2` | 3 | 9 | `Matrix (Fin 2) (Fin 2) ℝ` |
| `NavierStokes.SignedWaveUpdate.Mat2` | 6 | 41 | `NavierStokes.SmoothCovariance.Mat2` |
| `NavierStokes.SmoothCovariance.Mat2` | 27 | 83 | `Matrix (Fin 2) (Fin 2) ℝ` |

#### 24. F00039: 13 members, score 12

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0)
- kinds: 13 abbrev; 13 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 447 declarations use a member; 130 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 2 shared roles (9 theorems; 0 roles held by every member), out of 130 statements about the members
- concept-count estimate: 12 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 12
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 4 nodes over 1 distinct bodies:

  ```
  EuclideanSpace Real (Fin 2)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.BasePhaseGeometry.Plane` | 7 | 23 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.GrowingMode.State` | 4 | 15 | `EuclideanSpace ℝ (Fin 2)` |
| `NavierStokes.MovingFrameODE.Plane` | 26 | 199 | `EuclideanSpace ℝ (Fin 2)` |
| `NavierStokes.PhaseEstimates.Plane` | 18 | 45 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PhaseJetBounds.Plane` | 4 | 29 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PrimaryCopyBridge.State` | 0 | 7 | `NavierStokes.PrimaryODE.State` |
| `NavierStokes.PrimaryGeometryAssembly.Plane` | 0 | 10 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PrimaryODE.State` | 17 | 117 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PrimaryPulseBounds.State` | 2 | 17 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PrimaryRepresentatives.Plane` | 30 | 61 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.PrimaryTargetBounds.Plane` | 9 | 50 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.ProfileSpectralCone.Plane` | 9 | 39 | `NavierStokes.MovingFrameODE.Plane` |
| `NavierStokes.ViscousPropagator.Plane` | 4 | 17 | `EuclideanSpace ℝ (Fin 2)` |

#### 25. F00040: 7 members, score 11.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00098, F00195, F00196, F02025 (4 overlapping records folded in)
- kinds: 7 def; 4 modules; instance arguments per member 0–4, type arguments 0–1
- usage: 141 declarations use a member; 91 theorem statements mention one; 13 member pairs occur together in a statement
- lemma family: 14 identical shapes (31 theorems; 0 shapes held by every member), 1 shared roles (2 theorems; 0 roles held by every member), out of 91 statements about the members
- concept-count estimate: 6 definitions + 17 lemma statements by identical shape (low), or + 1 by role (high); penalty 2; score 11.5
- the general form already exists: `EulerElapsedTimePathGluing.join`; the skeleton below is over its named specialisations
- similarity 0.111 (smallest share of a member outside compound holes), skeleton of 2 nodes over 6 distinct bodies:

  ```
  EulerElapsedTimePathGluing.join ⟨h1⟩ p1 ⟨h2⟩ ⟨h3⟩
  ```
- holes: 3, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ term ×5, parameter ×1; 2 distinct values; compound
  - ⟨h2⟩ term; 6 distinct values; compound
  - ⟨h3⟩ term ×5, parameter ×1; 6 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `EulerElapsedTimePathGluing.join` | 14 | 24 | (the general form) |  |  |
| `EulerElapsedTimePathGluing.profile` | 8 | 13 | `S` | `ContinuousMap.const (Set.Elem (Set.Icc 0 τ)) 1` | `g` |
| `EulerTransversePacketJoin.derivativePath` | 10 | 17 | `Data.T D` | `EulerTransversePacketJoin.pastDerivative P D τ B raw G` | `EulerTransversePacketJoin.futureDerivative P D τ B raw G` |
| `EulerTransversePacketJoin.pressurePath` | 9 | 20 | `Data.T D` | `EulerTransversePacketJoin.pastPressure P D τ B raw G` | `EulerTransversePacketJoin.futurePressure P D τ B raw G` |
| `EulerTransversePacketJoin.velocityPath` | 19 | 35 | `Data.T D` | `EulerTransversePacketJoin.pastVelocity P D τ B raw G` | `EulerTransversePacketJoin.futureVelocity P D τ B raw G` |
| `EulerTransversePacketPrimary.derivativePath` | 12 | 20 | `Data.T D` | `EulerTransversePacketPrimary.pastDerivative P D τ B Y` | `EulerTransversePacketPrimary.futureDerivative P D τ B Y` |
| `EulerTransversePacketPrimary.velocityPath` | 19 | 49 | `Data.T D` | `EulerTransversePacketPrimary.pastVelocity P D τ B Y` | `EulerTransversePacketPrimary.futureVelocity P D τ B Y` |

#### 26. F00041: 8 members, score 11.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00119, F00280, F00389, F00752, F01232 (5 overlapping records folded in)
- kinds: 8 def; 5 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 94 declarations use a member; 71 theorem statements mention one; 12 member pairs occur together in a statement
- lemma family: 9 identical shapes (25 theorems; 0 shapes held by every member), 3 shared roles (18 theorems; 0 roles held by every member), out of 71 statements about the members
- concept-count estimate: 7 definitions + 16 lemma statements by identical shape (low), or + 10 by role (high); penalty 2; score 11.5
- the general form already exists: `NavierStokes.LocalizedMomentRepair.repair`; the skeleton below is over its named specialisations
- no common body (the generalisation is a single hole): a shared interface would have to be a structure or class, not a parameter

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.FiveRowRank.deltaV` | 9 | 16 | `NavierStokes.LocalizedMomentRepair.repair (NavierStokes.FiveRowRank.angularPowers lam)   (NavierStokes.FiveRow` |
| `NavierStokes.FiveRowRank.gamma` | 9 | 17 | `NavierStokes.LocalizedMomentRepair.repair (NavierStokes.FiveRowRank.axialPowers lam)   (NavierStokes.FiveRowRa` |
| `NavierStokes.LocalizedMomentRepair.repair` | 9 | 34 | `∑ j,   NavierStokes.LocalizedMomentRepair.coefficients a l u d j *     NavierStokes.LocalizedMomentRepair.bump` |
| `NavierStokes.OutgoingSchedule.correction` | 12 | 25 | `NavierStokes.LocalizedMomentRepair.repair c.exponents c.lower c.upper   (NavierStokes.OutgoingSchedule.debt c ` |
| `NavierStokes.PositiveOrderMoments.repairE` | 9 | 10 | `NavierStokes.LocalizedMomentRepair.repair (NavierStokes.FiveRowRank.angularPowers lam)   (NavierStokes.FiveRow` |
| `NavierStokes.PositiveOrderMoments.repairU` | 9 | 10 | `NavierStokes.LocalizedMomentRepair.repair (NavierStokes.FiveRowRank.axialPowers lam)   (NavierStokes.FiveRowRa` |
| `NavierStokes.PulseAmplitude.amplitudeRepair` | 7 | 13 | `NavierStokes.LocalizedMomentRepair.repair c.exponents c.lower c.upper   (fun i ↦ -NavierStokes.OutgoingSchedul` |
| `NavierStokes.PulseAmplitude.prefixRepair` | 7 | 12 | `NavierStokes.LocalizedMomentRepair.repair c.exponents c.lower c.upper   (fun i ↦ -NavierStokes.OutgoingSchedul` |

#### 27. F00042: 18 members, score 11.2

*Reading (model, not evidence):* F. One idea by this reading: the derivative of `f` at `x` in a direction, under 18 names; the hole is the direction (a basis vector, `(0, 1)`, `(1, 0)`, …). Mathlib's `fderiv ℝ f x v` or `lineDeriv` is the primitive.

- found by: anti-unification (AU@0.5); also F00069, F00083, F00102, F00390, F00491, F00492, F00918, F01750 … (10 overlapping records folded in)
- kinds: 18 def; 13 modules; instance arguments per member 0–4, type arguments 0–2
- usage: 652 declarations use a member; 343 theorem statements mention one; 17 member pairs occur together in a statement
- lemma family: 9 identical shapes (20 theorems; 0 shapes held by every member), 8 shared roles (26 theorems; 0 roles held by every member), out of 343 statements about the members
- concept-count estimate: 17 definitions + 10 lemma statements by identical shape (low), or + 11 by role (high); penalty 2.5; score 11.2
- similarity 0.556 (smallest share of a member outside compound holes), skeleton of 5 nodes over 15 distinct bodies:

  ```
  DFunLike.coe (fderiv Real p0 p1) ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ term; 9 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerMeanVectorIdentities.vectorPartial` | 4 | 9 | `EuclideanSpace.single i 1` |
| `EulerPacketGraphHessian.angularDerivative` | 7 | 10 | `Prod.mk 0 1` |
| `EulerSmoothSobolev.coordinateDerivative` | 4 | 5 | `EuclideanSpace.single i 1` |
| `EulerVectorCalculus.partialDerivative` | 42 | 80 | `EuclideanSpace.single i 1` |
| `NavierStokes.IntegratedMeanBalances.parameterPartial` | 10 | 18 | `Prod.mk 0 v` |
| `NavierStokes.ParametricTorusInverse.parameterPartial` | 3 | 4 | `Prod.mk 1 0` |
| `NavierStokes.PressureStream.graphDr` | 18 | 36 | `PressureStream.radialVector k v p` |
| `NavierStokes.PressureStream.graphDz` | 6 | 16 | (same body as another member) |
| `NavierStokes.ProfileHistories.parameterPartial` | 83 | 168 | `Prod.mk 0 1` |
| `NavierStokes.ProfileHistories.radialPartial` | 48 | 137 | `Prod.mk 1 0` |
| `NavierStokes.RadialAlias.directionalDeriv` | 7 | 7 | `Prod.mk 0 v` |
| `NavierStokes.RadialAlias.slowDeriv` | 8 | 12 | `Prod.mk 1 0` |
| `NavierStokes.SimilarityProfile.partialEta` | 15 | 61 | (same body as another member) |
| `NavierStokes.SimilarityProfile.partialX` | 71 | 168 | (same body as another member) |

… and 4 more members (all in `clusters.jsonl`).

#### 28. F00043: 35 members, score 11.14

*Reading (model, not evidence):* G. Aperture noise by this reading: the skeleton is only the constructor of a (continuous) linear map; any two linear maps built by a structure literal match.

- found by: anti-unification (AU@0.5); also F00109, F00367, F00912, F01149, F01330, F02217, F02684, F02687 … (15 overlapping records folded in)
- kinds: 35 def; 29 modules; instance arguments per member 0–8, type arguments 0–4
- usage: 99 declarations use a member; 35 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 1 shared roles (10 theorems; 0 roles held by every member), out of 35 statements about the members
- concept-count estimate: 34 definitions + 0 lemma statements by identical shape (low), or + 5 by role (high); penalty 3.5; score 11.14
- similarity 0.5 (smallest share of a member outside compound holes), skeleton of 3 nodes over 35 distinct bodies:

  ```
  LinearMap.mk (RingHom.id ⟨h1⟩) (AddHom.mk ⟨h2⟩)
  ```
- holes: 2, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ type; 2 distinct values
  - ⟨h2⟩ function; 35 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `EulerContinuousBoundedTensor.tensorPathLinear` | 0 | 1 | `Real` | `EulerContinuousBoundedTensor.tensorPath n` |
| `EulerContinuousPathCalculus.coefficientLinear` | 0 | 1 | `Real` | `EulerContinuousTimeIntegral.multiplier` |
| `EulerContinuousSpatialFamily.derivativeBundlingLinear` | 0 | 1 | `Real` | `EulerContinuousSpatialFamily.derivativeMap` |
| `EulerContinuousSpatialFamily.derivativeLinear` | 0 | 1 | `Real` | `EulerContinuousSpatialFamily.direction D` |
| `EulerCylinderAnglePrimitive.primitiveLinear` | 0 | 1 | `Real` | `EulerCylinderAnglePrimitive.kernelIntegral P` |
| `EulerCylinderBoundedCover.coverLinear` | 0 | 1 | `Real` | `EulerCylinderBoundedCover.cover P` |
| `EulerCylinderMollifier.mollifierLinearMap` | 0 | 1 | `Real` | `EulerCylinderMollifier.mollify period n` |
| `EulerFinitePathTensor.tensorPathLinear` | 0 | 1 | `Real` | `EulerFinitePathTensor.tensorPath n` |
| `EulerLiftedPressure.coefficientLinearMap` | 0 | 1 | `Real` | `EulerLiftedPressure.coefficientApply μ A C` |
| `EulerLpCylinderCoefficients.liftedOperatorPathLinear` | 0 | 1 | `Real` | `EulerLpCylinderCoefficients.liftedOperatorPath period S T` |
| `EulerLpDerivative.bundlingLinear` | 0 | 1 | `Real` | `EulerLpDerivative.derivativeMap μ` |
| `EulerLpDerivative.derivativeLinear` | 0 | 1 | `Real` | `EulerLpDerivative.applyDerivative μ D` |
| `EulerLpOperatorField.fullLinear` | 0 | 1 | `Real` | `EulerLpOperatorField.applyField μ A` |
| `EulerLpOperatorField.supportedLinear` | 0 | 1 | `Real` | `EulerLpOperatorField.supported μ S` |

… and 21 more members (all in `clusters.jsonl`).

#### 29. F00044: 9 members, score 11

*Reading (model, not evidence):* B. Not one idea. Each member is `Classical.choose` / `choice` / `Exists.choose` applied to a different existence proof; the proof is an erased argument, so only the head is compared.

- found by: anti-unification (AU@1.0, AU@0.7, AU@0.5); also F00194, F00840, F01396, F01441 (4 overlapping records folded in)
- kinds: 9 def; 8 modules; instance arguments per member 0–3, type arguments 0–1
- usage: 336 declarations use a member; 267 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 3 shared roles (7 theorems; 0 roles held by every member), out of 267 statements about the members
- concept-count estimate: 8 definitions + 0 lemma statements by identical shape (low), or + 3 by role (high); penalty 1; score 11
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 1 nodes over 7 distinct bodies:

  ```
  Exists.choose
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerOrdinarySobolev.FiniteLifespan.evolution` | 19 | 31 | `⋯.choose` |
| `EulerPacketInduction.lifespan` | 7 | 10 | `EulerPacketInduction.initialDatum_finite_lifespan.choose` |
| `EulerPacketSourceGeometry.ForwardGuards.sourceGrowthProfile` | 6 | 7 | `⋯.choose` |
| `EulerPacketSourceGeometry.Guards.slope` | 2 | 6 | `⋯.choose` |
| `EulerPacketSourceGeometry.Guards.sourceGrowthProfile` | 7 | 10 | `⋯.choose` |
| `EulerPacketSourceGeometry.Guards.terminal` | 14 | 26 | `⋯.choose` |
| `NavierStokes.ActualCarrierGeometry.geometricThreshold` | 208 | 229 | `NavierStokes.ActualCarrierGeometry.geometricThreshold._proof_3.choose` |
| `NavierStokes.EntranceAlignedBase.trueWidth` | 1 | 5 | `⋯.choose` |
| `NavierStokes.InitialPhysicalData.selected` | 3 | 19 | `Exists.choose hL` |

#### 30. F00045: 9 members, score 11

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00424, F00580, F00590, F01098, F02790, F02792 (6 overlapping records folded in)
- kinds: 9 def; 6 modules; instance arguments per member 0–3, type arguments 0–1
- usage: 224 declarations use a member; 144 theorem statements mention one; 33 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 14 shared roles (28 theorems; 0 roles held by every member), out of 144 statements about the members
- concept-count estimate: 8 definitions + 0 lemma statements by identical shape (low), or + 14 by role (high); penalty 2; score 11
- the general form already exists: `EulerPacketPointJets.fieldSum`; the skeleton below is over its named specialisations
- similarity 0.294 (smallest share of a member outside compound holes), skeleton of 5 nodes over 8 distinct bodies:

  ```
  EulerPacketPointJets.fieldSum (p0 + 1) p1 ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ function; 8 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerPacketInitial.high` | 7 | 17 | `EulerPacketInitial.highGrade N t a` |
| `EulerPacketInitial.mean` | 8 | 16 | `EulerPacketInitial.meanGrade N t a` |
| `EulerPacketPointJets.fieldSum` | 81 | 178 | (the general form) |
| `EulerPacketTerminalDatum.forwardInitializedPressure` | 6 | 11 | `EulerPacketProfileRecursion.assembledPressure N (EulerPacket` |
| `EulerPacketTerminalDatum.forwardInitializedVelocity` | 13 | 21 | `EulerPacketProfileRecursion.assembledVelocity N (EulerPacket` |
| `EulerPacketTerminalDatum.forwardInitializedVelocityDerivative` | 5 | 9 | `ProfileRegularity.velocityTimeCoefficients (Data.T M) N (Eul` |
| `EulerPacketTerminalDatum.initializedPressure` | 6 | 11 | `EulerPacketProfileRecursion.assembledPressure N (EulerPacket` |
| `EulerPacketTerminalDatum.initializedVelocity` | 13 | 21 | `EulerPacketProfileRecursion.assembledVelocity N (EulerPacket` |
| `EulerPacketTerminalDatum.initializedVelocityDerivative` | 5 | 9 | `ProfileRegularity.velocityTimeCoefficients (Data.T M) N (Eul` |

#### 31. F00046: 5 members, score 10.5

*Reading (model, not evidence):* C, and a positive control. `MeanClass`, `UnweightedClass`, `WaveClass`, `AmplitudeBound` are `MemClass` at four weights. The weight hole is a function of the bound point, the other holes are parameters passed through.

- found by: specialisation (WRAP); also F00177 (1 overlapping records folded in)
- kinds: 4 abbrev, 1 structure; 2 modules; instance arguments per member 0–4, type arguments 0–2
- usage: 453 declarations use a member; 382 theorem statements mention one; 25 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 12 shared roles (61 theorems; 0 roles held by every member), out of 382 statements about the members
- concept-count estimate: 4 definitions + 0 lemma statements by identical shape (low), or + 17 by role (high); penalty 2; score 10.5
- the general form already exists: `NavierStokes.WeightedClasses.MemClass`; the skeleton below is over its named specialisations
- similarity 0.139 (smallest share of a member outside compound holes), skeleton of 3 nodes over 4 distinct bodies:

  ```
  WeightedClasses.MemClass ⟨h1⟩ (fun x0 : Nat ↦ ⟨h2⟩) ⟨h3⟩ ⟨h4⟩
  ```
- holes: 4, effective parameters 3; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ parameter ×3, constant ×1; 2 distinct values
  - ⟨h2⟩ function; 4 distinct values; depends on a bound variable, so the parameter must be a function; compound
  - ⟨h3⟩ parameter; 3 distinct values
  - ⟨h4⟩ parameter ×3, function ×1; 4 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ | ⟨h4⟩ |
|---|---:|---:|---|---|---|---|
| `NavierStokes.CurrentSignedCurl.AmplitudeBound` | 13 | 13 | `ActualSignedStageControls.fullStrip` | `fun x0 : (Prod (Prod Real (Prod (Prod Real Real) (Prod Real ` | `α` | `WaveCoefficients.amplitude (CopyData.common (ActualSignedCoh` |
| `NavierStokes.WeightedClasses.MeanClass` | 223 | 281 | `s` | `StripData.zeta s` | `α` | `f` |
| `NavierStokes.WeightedClasses.MemClass` | 74 | 195 | (the general form) |  |  |  |
| `NavierStokes.WeightedClasses.UnweightedClass` | 70 | 120 | `s` | `fun x0 : D ↦ 1` | `α` | `f` |
| `NavierStokes.WeightedClasses.WaveClass` | 2 | 5 | `s` | `fun x0 : D ↦ ((Real.sqrt ((StripData.zeta s) x0)) * (P ⟨boun` | `α` | `f` |

#### 32. F00049: 9 members, score 10

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1); also F00099, F00138, F00374 (3 overlapping records folded in)
- kinds: 9 abbrev; 9 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,408 declarations use a member; 512 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 2 identical shapes (7 theorems; 0 shapes held by every member), 3 shared roles (19 theorems; 0 roles held by every member), out of 512 statements about the members
- concept-count estimate: 8 definitions + 2 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 10
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 5 nodes over 1 distinct bodies:

  ```
  ∀ x0 : (Prod Real Real), Real
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.GlobalSlowProfiles.Field` | 18 | 189 | `ℝ × ℝ → ℝ` |
| `NavierStokes.MatchingDebtBounds.Field` | 5 | 9 | `NavierStokes.MatchingDebtBounds.Point → ℝ` |
| `NavierStokes.ModulatedHistories.Field` | 37 | 54 | `NavierStokes.ModulatedHistories.Point → ℝ` |
| `NavierStokes.NominalProfile.Field` | 26 | 59 | `NavierStokes.NominalProfile.Point → ℝ` |
| `NavierStokes.OutgoingHistories.Field` | 13 | 26 | `NavierStokes.OutgoingHistories.Point → ℝ` |
| `NavierStokes.PositiveOrderMoments.JointProfile` | 12 | 26 | `ℝ × ℝ → ℝ` |
| `NavierStokes.ProfileHistories.Field` | 171 | 731 | `NavierStokes.ProfileHistories.Point → ℝ` |
| `NavierStokes.SimilarityProfile.InnerProfile` | 173 | 319 | `NavierStokes.SimilarityProfile.InnerPoint → ℝ` |
| `NavierStokes.SlowStressSupport.Field` | 57 | 75 | `ℝ × ℝ → ℝ` |

#### 33. F00050: 30 members, score 9.4

*Reading (model, not evidence):* G. Aperture noise by this reading: the skeleton is only the constructor of a (continuous) linear map; any two linear maps built by a structure literal match.

- found by: anti-unification (AU@0.5); also F01178, F01374, F01391, F01926, F01929, F02572, F02681, F02731 … (14 overlapping records folded in)
- kinds: 30 def; 24 modules; instance arguments per member 0–9, type arguments 0–5
- usage: 448 declarations use a member; 171 theorem statements mention one; 13 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 12 shared roles (35 theorems; 0 roles held by every member), out of 171 statements about the members
- concept-count estimate: 29 definitions + 1 lemma statements by identical shape (low), or + 18 by role (high); penalty 5; score 9.4
- similarity 0.5 (smallest share of a member outside compound holes), skeleton of 4 nodes over 30 distinct bodies:

  ```
  ContinuousLinearMap.comp (RingHom.id ⟨h1⟩) (RingHom.id ⟨h1⟩) (RingHom.id ⟨h1⟩) ⟨h2⟩ ⟨h3⟩
  ```
- holes: 3, effective parameters 3; the holes vary independently (more joint combinations than any one hole has values)
  - ⟨h1⟩ type; 2 distinct values
  - ⟨h2⟩ term ×28, constant ×2; 22 distinct values; compound
  - ⟨h3⟩ term ×24, constant ×5, parameter ×1; 27 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `EulerBoundedFieldCalculus.pathCompositionMap` | 4 | 21 | `Real` | `EulerContinuousPathCalculus.coefficientMap` | `ContinuousLinearMap.compLeftContinuous Real K EulerBoundedFi` |
| `EulerCoerciveProjection.pressureSolver` | 2 | 7 | `Real` | `EulerCoerciveProjection.projectedInverse S G c` | `Submodule.orthogonalProjectionOnto S` |
| `EulerContinuousTimeFreeze.freezePath` | 2 | 4 | `Real` | `ContinuousLinearMap.const Real K` | `ContinuousMap.evalCLM Real t` |
| `EulerCylinderDirichlet.Coefficients.endpointDisplacement` | 5 | 10 | `Real` | `EulerInitialTimePrimitive.initialPrimitive T` | `Coefficients.endpointSlope P T D` |
| `EulerCylinderPathProduct.pathBilinear` | 5 | 8 | `Real` | `EulerContinuousPathCalculus.coefficientMap` | `ContinuousLinearMap.compLeftContinuous Real K B` |
| `EulerCylinderSobolevSpace.valueOperator` | 14 | 85 | `Real` | `ContinuousLinearMap.proj (EulerCylinderSobolevSpace.emptyWor` | `EulerCylinderSobolevSpace.arrayOperator period q` |
| `EulerCylinderSobolevSpace.wordOperator` | 3 | 21 | `Real` | `ContinuousLinearMap.proj w` | `EulerCylinderSobolevSpace.arrayOperator period q` |
| `EulerDirichletEndpointReduction.endpointExtension` | 1 | 6 | `Real` | `EulerDirichletEndpointReduction.stationaryPart S A c` | `L` |
| `EulerLiftedVelocitySplit.normalVelocityMap` | 2 | 3 | `Real` | `ContinuousLinearMap.toSpanSingleton Real (EuclideanSpace.sin` | `EulerCylinderScalarPrimitive.scalarProject` |
| `EulerLinearDuhamel.Evolution.weightedInitial` | 2 | 6 | `Real` | `EulerContinuousTimeWeight.normalize g` | `Evolution.initialOperator T B U` |
| `EulerLpCylinderRectangular.fullMultiplierMap` | 7 | 32 | `Real` | `EulerContinuousPathCalculus.coefficientMap` | `EulerLpCylinderRectangular.fullPathMap period` |
| `EulerLpCylinderRectangular.fullOperatorMap` | 11 | 48 | `Real` | `EulerLpOperatorField.fullMap (EulerLiftedGradientSpace.liftM` | `EulerLpCylinderTranslation.fieldLift period` |
| `EulerLpCylinderRectangular.supportedMultiplierMap` | 4 | 26 | `Real` | `EulerContinuousPathCalculus.coefficientMap` | `EulerLpCylinderRectangular.supportedPathMap period S` |
| `EulerMeanBoundary.boundaryOperator` | 36 | 70 | `Real` | `EulerMeanBoundary.cutoffCurl χ` | `EulerMeanBoundary.weakPotential χ` |

… and 16 more members (all in `clusters.jsonl`).

#### 34. F00052: 4 members, score 9

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00248 (1 overlapping records folded in)
- kinds: 4 def; 4 modules; instance arguments per member 3–3, type arguments 1–1
- usage: 98 declarations use a member; 53 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 11 shared roles (30 theorems; 0 roles held by every member), out of 53 statements about the members
- concept-count estimate: 3 definitions + 0 lemma statements by identical shape (low), or + 15 by role (high); penalty 2; score 9
- the general form already exists: `EulerPacketCorrectionCoefficients.correctionDataOfFields`; the skeleton below is over its named specialisations
- similarity 0.024 (smallest share of a member outside compound holes), skeleton of 3 nodes over 3 distinct bodies:

  ```
  EulerPacketCorrectionCoefficients.correctionDataOfFields p0 ⟨h1⟩ (Inv.inv ⟨h2⟩) (⟨h3⟩ ⟨h4⟩ ⟨h2⟩ ⟨h5⟩) ⟨h6⟩ ⟨h7⟩ ⟨h8⟩
  ```
- holes: 8, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ term ×2, parameter ×1; 2 distinct values; compound
  - ⟨h2⟩ parameter; 2 distinct values
  - ⟨h3⟩ head; 2 distinct values
  - ⟨h4⟩ erased ×2, parameter ×1; 2 distinct values
  - ⟨h5⟩ function ×2, parameter ×1; 3 distinct values; compound
  - ⟨h6⟩ function; 3 distinct values; compound
  - ⟨h7⟩ term; 3 distinct values; compound
  - ⟨h8⟩ term ×2, parameter ×1; 3 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ | ⟨h4⟩ | ⟨h5⟩ | ⟨h6⟩ |
|---|---:|---:|---|---|---|---|---|---|
| `EulerPacketCoordinates.coordinateData` | 5 | 7 | `P` | `k` | `EulerPacketCoordinates.coordinate` | `D` | `W` | `EulerPacketCoordinates.normalizedResidual D k W p` |
| `EulerPacketCorrectionCoefficients.correctionDataOfFields` | 0 | 8 | (the general form) |  |  |  |  |  |
| `EulerPacketTerminalDatum.forwardInitializedCorrectionData` | 26 | 54 | `2 * Real.pi` | `k` | `HSMul.hSMul` | `_` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` |
| `EulerPacketTerminalDatum.initializedCorrectionData` | 22 | 39 | `2 * Real.pi` | `k` | `HSMul.hSMul` | `_` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` |

#### 35. F00053: 9 members, score 9

*Reading (model, not evidence):* B. Transport along an equality (`Eq.rec`), with the equality proof erased. Nine casts, not one notion.

- found by: anti-unification (AU@1.0, AU@0.7); also F00094, F00399 (2 overlapping records folded in)
- kinds: 9 def; 6 modules; instance arguments per member 0–2, type arguments 0–1
- usage: 152 declarations use a member; 93 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 1 shared roles (2 theorems; 0 roles held by every member), out of 93 statements about the members
- concept-count estimate: 8 definitions + 0 lemma statements by identical shape (low), or + 1 by role (high); penalty 1; score 9
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 4 nodes over 9 distinct bodies:

  ```
  Eq.rec p0 p1 p2
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerPacketCylinderField.Field.changeTime` | 5 | 41 | `h ▸ G` |
| `EulerPacketCylinderField.MatrixCoefficient.changeTime` | 1 | 3 | `h ▸ G` |
| `EulerPacketCylinderField.ProfileRegularity.congr` | 0 | 2 | `h ▸ G` |
| `EulerPacketCylinderField.VectorCoefficient.changeTime` | 1 | 3 | `h ▸ G` |
| `EulerPacketCylinderField.timeProfileChange` | 75 | 93 | `h ▸ g` |
| `EulerPacketPressure.GradientWitness.changeTime` | 0 | 12 | `h ▸ G` |
| `EulerPacketPressure.GradientWitness.congr` | 0 | 3 | `h ▸ G` |
| `EulerPacketSourceGeometry.ParentFrame.changeActivation` | 8 | 18 | `h ▸ P` |
| `EulerPacketTimeProfile.Scales.changeTime` | 3 | 5 | `h ▸ S` |

#### 36. F00054: 9 members, score 9

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7, AU@0.5)
- kinds: 9 abbrev; 9 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,924 declarations use a member; 1,037 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 9 shared roles (97 theorems; 0 roles held by every member), out of 1,037 statements about the members
- concept-count estimate: 8 definitions + 1 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 9
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 6 nodes over 1 distinct bodies:

  ```
  Prod Real (EuclideanSpace Real (Fin 3))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualBaseResidual.SpaceTime` | 0 | 27 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.ActualSignedPhysicalCoherence.SpaceTime` | 13 | 16 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.AnnularEndpoint.SpaceTime` | 7 | 19 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.JointResidualLimits.SpaceTime` | 7 | 29 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.OffplaneCorrectionExtensions.SpaceTime` | 2 | 3 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.ProblemStatement.SpaceTime` | 947 | 1807 | `ℝ × NavierStokes.ProblemStatement.Space` |
| `NavierStokes.SpacetimeEndpoint.SpaceTime` | 17 | 33 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokes.SpacetimeGluing.SpaceTime` | 22 | 40 | `NavierStokes.ProblemStatement.SpaceTime` |
| `NavierStokesR3.ProblemStatement.SpaceTime` | 22 | 39 | `NavierStokes.ProblemStatement.SpaceTime` |

#### 37. F00055: 10 members, score 9

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7); also F00281 (1 overlapping records folded in)
- kinds: 10 abbrev; 10 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 330 declarations use a member; 154 theorem statements mention one; 4 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 3 shared roles (12 theorems; 0 roles held by every member), out of 154 statements about the members
- concept-count estimate: 9 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 9
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 11 nodes over 1 distinct bodies:

  ```
  Prod (Prod (Prod Real (Prod Real Real)) Real) (Prod Real Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCurrentCarrierJets.Native` | 7 | 16 | `NavierStokes.ActualParticularBackground.Native` |
| `NavierStokes.ActualCurrentParticularBounds.Native` | 13 | 20 | `NavierStokes.ActualParticularStageControls.Native` |
| `NavierStokes.ActualCurrentParticularPhysical.Native` | 14 | 57 | `NavierStokes.PhysicalParticularWave.WaveSpace` |
| `NavierStokes.ActualParticularBackground.Native` | 6 | 26 | `(NavierStokes.ActualParticularBackground.Parameter × ℝ) × NavierStokes.TorusInverse.Plane` |
| `NavierStokes.ActualParticularRealization.WaveSpace` | 0 | 1 | `NavierStokes.PhysicalParticularWave.WaveSpace` |
| `NavierStokes.ActualParticularStageControls.Native` | 55 | 151 | `(NavierStokes.ActualParticularStageControls.Parameter × ℝ) × NavierStokes.ActualParticularStageControls.Plane` |
| `NavierStokes.ActualWaveRegularity.ParticularSpace` | 25 | 75 | `(NavierStokes.CorrectionStep.CycleSlow × ℝ) × NavierStokes.TorusInverse.Plane` |
| `NavierStokes.CurrentPhysicalChartJets.Native` | 5 | 17 | `NavierStokes.PhysicalParticularWave.WaveSpace` |
| `NavierStokes.GaussianErrorNaturality.WaveSpace` | 1 | 1 | `NavierStokes.PhysicalParticularWave.WaveSpace` |
| `NavierStokes.PhysicalParticularWave.WaveSpace` | 28 | 97 | `(NavierStokes.PhysicalParticularWave.Parameter × ℝ) × NavierStokes.TorusInverse.Plane` |

#### 38. F00058: 11 members, score 8.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00065, F00096, F01414, F04100 (4 overlapping records folded in)
- kinds: 11 def; 11 modules; instance arguments per member 0–1, type arguments 0–0
- usage: 95 declarations use a member; 69 theorem statements mention one; 11 member pairs occur together in a statement
- lemma family: 3 identical shapes (10 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 69 statements about the members
- concept-count estimate: 10 definitions + 7 lemma statements by identical shape (low), or + 0 by role (high); penalty 2; score 8.5
- the general form already exists: `EulerPolynomialCost.coefficientCost`; the skeleton below is over its named specialisations
- similarity 0.333 (smallest share of a member outside compound holes), skeleton of 1 nodes over 10 distinct bodies:

  ```
  EulerPolynomialCost.coefficientCost ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ constant ×7, term ×3; 10 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerPacketFiveCost.costConstant` | 4 | 7 | `EulerPacketFiveCost.fivePolynomial P` |
| `EulerPacketInitialAmplitude.constant` | 6 | 8 | `EulerPacketInitialAmplitude.polynomial` |
| `EulerPacketInitialCost.sourceConstant` | 5 | 7 | `EulerPacketInitialCost.sourcePolynomial s` |
| `EulerPacketInitializedCost.uniformConstant` | 9 | 16 | `EulerPacketInitializedCost.polynomial` |
| `EulerPacketInitializedOutputCost.uniformConstant` | 15 | 23 | `EulerPacketInitializedOutputCost.polynomial` |
| `EulerPacketUniformSource.frequencyConstant` | 10 | 19 | `EulerPacketUniformSource.frequencyPolynomial` |
| `EulerParentBadRatio.constant` | 4 | 8 | `EulerParentBadRatio.polynomial` |
| `EulerParentCorrectionCost.parentConstant` | 2 | 6 | `EulerParentCorrectionCost.parentPolynomial P` |
| `EulerParentHistoryCost.labelHistoryConstant` | 5 | 14 | `EulerParentHistoryCost.labelHistoryPolynomial` |
| `EulerParentNeighborCost.constant` | 7 | 10 | `EulerParentNeighborCost.polynomial` |
| `EulerPolynomialCost.coefficientCost` | 2 | 12 | (the general form) |

#### 39. F00060: 13 members, score 8

*Reading (model, not evidence):* G. Aperture noise by this reading: the skeleton is only the constructor of a (continuous) linear map; any two linear maps built by a structure literal match.

- found by: anti-unification (AU@0.5); also F00899, F02334, F02676 (3 overlapping records folded in)
- kinds: 13 def; 12 modules; instance arguments per member 2–8, type arguments 1–4
- usage: 132 declarations use a member; 46 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 4 shared roles (14 theorems; 0 roles held by every member), out of 46 statements about the members
- concept-count estimate: 12 definitions + 1 lemma statements by identical shape (low), or + 8 by role (high); penalty 2.5; score 8
- similarity 0.5 (smallest share of a member outside compound holes), skeleton of 3 nodes over 13 distinct bodies:

  ```
  ContinuousLinearMap.compLeftContinuous Real p0 ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ term; 13 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerBoundedFieldCalculus.pathAdjointMap` | 1 | 11 | `EulerBoundedFieldCalculus.adjointMap` |
| `EulerContinuousPathComposition.adjointMap` | 3 | 8 | `EulerTransverseGramInverse.realAdjoint` |
| `EulerCylinderAngleAverage.pathAverage` | 4 | 9 | `EulerCylinderAngleAverage.average P` |
| `EulerCylinderAngleAverage.supportedPathAverage` | 1 | 2 | `EulerCylinderAngleAverage.supportedAverage P S` |
| `EulerCylinderAnglePrimitive.pathPrimitive` | 9 | 15 | `EulerCylinderAnglePrimitive.primitive P` |
| `EulerCylinderBoundedCover.coverPathMap` | 0 | 5 | `EulerCylinderBoundedCover.coverMap P` |
| `EulerCylinderConstantMap.pathMap` | 4 | 20 | `EulerCylinderConstantMap.map period L` |
| `EulerCylinderFieldReflection.supportedPathReflection` | 1 | 2 | `EulerCylinderFieldReflection.supportedReflection P S` |
| `EulerCylinderScalarPrimitive.pathPrimitive` | 4 | 8 | `EulerCylinderScalarPrimitive.primitive period` |
| `EulerCylinderSpatialMean.pathMean` | 9 | 11 | `EulerCylinderSpatialMean.mean P` |
| `EulerLpCylinderRectangular.fullPathMap` | 4 | 18 | `EulerLpCylinderRectangular.fullOperatorMap period` |
| `EulerLpCylinderRectangular.supportedPathMap` | 2 | 5 | `EulerLpCylinderRectangular.supportedOperatorMap period S` |
| `EulerTransverseSourceCoefficientPath.pathEvaluation` | 4 | 18 | `BoundedContinuousFunction.evalCLM Real x` |

#### 40. F00061: 3 members, score 8

*Reading (model, not evidence):* F. Three definitions of the same `piece` at the standard region; two are verbatim copies.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7); also F00076, F00161, F00332 (3 overlapping records folded in)
- kinds: 3 def; 3 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 133 declarations use a member; 53 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 5 identical shapes (12 theorems; 0 shapes held by every member), 2 shared roles (5 theorems; 1 roles held by every member), out of 53 statements about the members
- concept-count estimate: 2 definitions + 6 lemma statements by identical shape (low), or + 3 by role (high); penalty 1; score 8
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 8 nodes over 1 distinct bodies:

  ```
  ActualPrimary.piece p0 p1 ActualPrimary.standardRegion (Prod.snd p2) (Prod.fst p2)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualInitialCoherence.pieces` | 13 | 34 | `NavierStokes.CorrectionInitialization.ActualPrimary.piece   NavierStokes.CorrectionInitialization.ActualPrimar` |
| `NavierStokes.ActualInitialMean.primaryPiece` | 11 | 19 | `NavierStokes.CorrectionInitialization.ActualPrimary.piece   NavierStokes.CorrectionInitialization.ActualPrimar` |
| `NavierStokes.ActualInitialization.primaryPiece` | 29 | 80 | `NavierStokes.CorrectionInitialization.ActualPrimary.piece   NavierStokes.CorrectionInitialization.ActualPrimar` |

#### 41. F00062: 16 members, score 8

*Reading (model, not evidence):* G. Sixteen different project functions applied to one standard argument tuple (a head hole). The shared part is the arguments, not an idea.

- found by: anti-unification (AU@1.0); also F00144, F00247, F00460, F00461, F00640, F00642, F00976, F01548 … (10 overlapping records folded in)
- kinds: 14 abbrev, 2 def; 5 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 53 declarations use a member; 31 theorem statements mention one; 13 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 1 shared roles (3 theorems; 0 roles held by every member), out of 31 statements about the members
- concept-count estimate: 15 definitions + 1 lemma statements by identical shape (low), or + 1 by role (high); penalty 2; score 8
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 9 nodes over 13 distinct bodies:

  ```
  ⟨h1⟩ (ActualCycleParameters.fixedParameters p0 p1) (CycleState.coefficients p2) (ActualPrimary.commonContext p0) (CycleState.state p2)
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ head; 13 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `NavierStokes.ActualIntermediateDebtBounds.postSigned` | 2 | 3 | `CycleParameters.afterSigned` |
| `NavierStokes.ActualIntermediateDebtBounds.postTemporal` | 4 | 4 | `CycleParameters.afterTemporal` |
| `NavierStokes.ActualIntermediateDebtBounds.signedGaussian` | 0 | 1 | `CycleParameters.signedGaussian` |
| `NavierStokes.ActualIntermediateDebtBounds.signedPressure` | 0 | 1 | `CycleParameters.signedPressure` |
| `NavierStokes.ActualIntermediateDebtBounds.signedVelocity` | 1 | 2 | `CycleParameters.signedVelocity` |
| `NavierStokes.ActualIntermediateDebtBounds.temporalIncrement` | 1 | 1 | `CycleParameters.temporalIncrement` |
| `NavierStokes.ActualParticularCycleData.block` | 10 | 18 | `CycleParameters.particularBlock` |
| `NavierStokes.ActualParticularCycleData.gaussianBlock` | 5 | 8 | `CycleParameters.particularGaussianBlock` |
| `NavierStokes.ActualParticularMeanGain.particularBlocks` | 0 | 4 | (same body as another member) |
| `NavierStokes.ActualParticularMeanGain.particularGaussian` | 0 | 1 | `CycleParameters.particularGaussian` |
| `NavierStokes.ActualParticularMeanGain.particularPressure` | 0 | 1 | `CycleParameters.particularPressure` |
| `NavierStokes.ActualParticularMeanGain.particularVelocity` | 2 | 7 | `CycleParameters.particularVelocity` |
| `NavierStokes.ActualParticularMeanGain.postParticular` | 3 | 23 | `CycleParameters.afterParticular` |
| `NavierStokes.ActualParticularMeanGain.signedRequest` | 0 | 2 | `CycleParameters.signedRequest` |

… and 2 more members (all in `clusters.jsonl`).

#### 42. F00064: 5 members, score 8

*Reading (model, not evidence):* F. The same quadratic increment `2 • (a * b) + b * b` for the axial, angular and radial component: one head hole (the projection).

- found by: body (L3); anti-unification (AU@1.0); also F00123, F00145, F00232, F01686, F01764 (5 overlapping records folded in)
- kinds: 5 def; 2 modules; instance arguments per member 0–0, type arguments 1–1
- usage: 67 declarations use a member; 32 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 7 identical shapes (19 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 32 statements about the members
- concept-count estimate: 4 definitions + 12 lemma statements by identical shape (low), or + 0 by role (high); penalty 2; score 8
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 9 nodes over 3 distinct bodies:

  ```
  (2 • ((⟨h1⟩ p0) * (⟨h1⟩ p1))) + ((⟨h1⟩ p1) * (⟨h1⟩ p1))
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ head; 3 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `NavierStokes.DefectIncrementBounds.axialQuadratic` | 4 | 7 | `Triple.axial` |
| `NavierStokes.MeanIncrementBounds.axialAxial` | 13 | 35 | (same body as another member) |
| `NavierStokes.MeanIncrementBounds.radialAngular` | 6 | 18 | `Triple.angular` |
| `NavierStokes.MeanIncrementBounds.radialAngularRemainder` | 2 | 5 | (same body as another member) |
| `NavierStokes.MeanIncrementBounds.radialRadial` | 7 | 19 | `Triple.radial` |

#### 43. F00066: 14 members, score 7.6

*Reading (model, not evidence):* G. Aperture noise by this reading: the skeleton is only the constructor of a (continuous) linear map; any two linear maps built by a structure literal match.

- found by: anti-unification (AU@0.5); also F00812, F01329, F01331, F02685, F03245 (5 overlapping records folded in)
- kinds: 14 def; 12 modules; instance arguments per member 0–9, type arguments 0–4
- usage: 69 declarations use a member; 26 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 3 shared roles (10 theorems; 0 roles held by every member), out of 26 statements about the members
- concept-count estimate: 13 definitions + 0 lemma statements by identical shape (low), or + 6 by role (high); penalty 2.5; score 7.6
- similarity 0.5 (smallest share of a member outside compound holes), skeleton of 3 nodes over 14 distinct bodies:

  ```
  ContinuousLinearMap.mk (RingHom.id Real) ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ term ×13, constant ×1; 14 distinct values; compound

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerContinuousBoundedTensor.tensorPathMap` | 1 | 3 | `EulerContinuousBoundedTensor.tensorPathLinear n` |
| `EulerContinuousPathCalculus.coefficientMap` | 1 | 10 | `EulerContinuousPathCalculus.coefficientLinear` |
| `EulerContinuousSpatialFamily.derivativeBundling` | 1 | 2 | `EulerContinuousSpatialFamily.derivativeBundlingLinear` |
| `EulerContinuousSpatialFamily.derivativeMap` | 3 | 7 | `EulerContinuousSpatialFamily.derivativeLinear D` |
| `EulerCylinderBoundedCover.coverMap` | 0 | 1 | `EulerCylinderBoundedCover.coverLinear P` |
| `EulerFinitePathTensor.tensorPathMap` | 4 | 11 | `EulerFinitePathTensor.tensorPathLinear n` |
| `EulerLpDerivative.derivativeBundling` | 4 | 11 | `EulerLpDerivative.bundlingLinear μ` |
| `EulerLpOperatorField.supportedMap` | 0 | 1 | `EulerLpOperatorField.supportedLinear μ S` |
| `EulerMeanCoefficients.derivativeBundling` | 1 | 3 | `EulerMeanCoefficients.derivativeBundlingLinear` |
| `EulerMeanCoefficients.fieldDerivativeMap` | 4 | 9 | `EulerMeanCoefficients.fieldDerivativeLinear DA` |
| `EulerMeanCoefficients.multiplierMap` | 1 | 6 | `EulerMeanCoefficients.multiplierLinear` |
| `EulerMeanCoefficients.pathDerivativeBundling` | 1 | 2 | `EulerMeanCoefficients.pathDerivativeBundlingLinear` |
| `EulerMeanCoefficients.pathDerivativeMap` | 4 | 8 | `EulerMeanCoefficients.pathDerivativeLinear DA` |
| `EulerTimeLpCoefficientMap.coefficientMap` | 1 | 5 | `EulerTimeLpCoefficientMap.coefficientLinear T` |

#### 44. F00067: 13 members, score 7.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP)
- kinds: 13 def; 8 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 278 declarations use a member; 197 theorem statements mention one; 36 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 2 shared roles (7 theorems; 0 roles held by every member), out of 197 statements about the members
- concept-count estimate: 12 definitions + 0 lemma statements by identical shape (low), or + 3 by role (high); penalty 2; score 7.5
- the general form already exists: `NavierStokes.AxisymmetricResidual.pack`; the skeleton below is over its named specialisations
- similarity 0.007 (smallest share of a member outside compound holes), skeleton of 1 nodes over 12 distinct bodies:

  ```
  AxisymmetricResidual.pack ⟨h1⟩ ⟨h2⟩ ⟨h3⟩
  ```
- holes: 3, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ term ×11, numeral ×1; 12 distinct values; compound
  - ⟨h2⟩ term; 12 distinct values; compound
  - ⟨h3⟩ term ×9, numeral ×3; 10 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `NavierStokes.ActualMeanPotentialRealization.componentPotential` | 4 | 8 | `0` | `((ScaledGraph.velocityScale G) / (ScaledGraph.radialScale G)` | `0` |
| `NavierStokes.AxisymmetricResidual.pack` | 42 | 147 | (the general form) |  |  |
| `NavierStokes.AxisymmetricResidual.velocity` | 10 | 17 | `AxisymmetricResidual.componentX B F (Prod.fst w) (Prod.snd w` | `AxisymmetricResidual.componentY B F (Prod.fst w) (Prod.snd w` | `AxisymmetricResidual.lift U (Prod.fst w) (Prod.snd w)` |
| `NavierStokes.CylindricalResidual.chart` | 98 | 140 | `(WithLp.ofLp 2 q 0) * (Real.cos (WithLp.ofLp 2 q 1))` | `(WithLp.ofLp 2 q 0) * (Real.sin (WithLp.ofLp 2 q 1))` | `WithLp.ofLp 2 q 2` |
| `NavierStokes.CylindricalResidual.chartVector` | 2 | 3 | `WithLp.ofLp 2 (DFunLike.coe (CylindricalResidual.frame -(Wit` | `(WithLp.ofLp 2 (DFunLike.coe (CylindricalResidual.frame -(Wi` | `WithLp.ofLp 2 (DFunLike.coe (CylindricalResidual.frame -(Wit` |
| `NavierStokes.CylindricalResidual.scalarGradient` | 1 | 4 | `CylindricalResidual.dCoord 0 f q` | `(CylindricalResidual.dCoord 1 f q) / (WithLp.ofLp 2 q 0)` | `CylindricalResidual.dCoord 2 f q` |
| `NavierStokes.DirectAngularDiagonal.rotationField` | 3 | 5 | `-(WithLp.ofLp 2 (Prod.snd w) 1) * (F (AxisymmetricFields.pro` | `(WithLp.ofLp 2 (Prod.snd w) 0) * (F (AxisymmetricFields.prof` | `0` |
| `NavierStokes.PhysicalCurlCovariance.cylindricalSpatialCurl` | 3 | 4 | `((WithLp.ofLp 2 (CylindricalResidual.dCoord 1 a q) 2) / (Wit` | `(WithLp.ofLp 2 (CylindricalResidual.dCoord 2 a q) 0) - (With` | `((WithLp.ofLp 2 (CylindricalResidual.dCoord 0 a q) 1) + ((Wi` |
| `NavierStokes.PhysicalCurlCovariance.realVector` | 20 | 40 | `Complex.re (a 0)` | `Complex.re (a 1)` | `Complex.re (a 2)` |
| `PhysicalResidualBridge.ScaledGraph.velocity` | 6 | 9 | `(ScaledGraph.velocityScale G) * (a (ScaledGraph.map G p) 0)` | `(ScaledGraph.velocityScale G) * (a (ScaledGraph.map G p) 1)` | `(ScaledGraph.velocityScale G) * (a (ScaledGraph.map G p) 2)` |
| `NavierStokes.SlowExpansionResidual.truncationResidual` | 3 | 6 | `((WithLp.ofLp 2 x 0) * ((SlowExpansionResidual.pressureTail ` | `((WithLp.ofLp 2 x 1) * ((SlowExpansionResidual.pressureTail ` | `SlowExpansionResidual.transportTail N (SimilarityProfile.q h` |
| `NavierStokes.SlowResidualMatching.retainedRadialForce` | 1 | 2 | `(WithLp.ofLp 2 x 0) * (((2 * (Prod.fst (SimilarityProfile.in` | `(WithLp.ofLp 2 x 1) * (((2 * (Prod.fst (SimilarityProfile.in` | `0` |
| `NavierStokes.SlowResidualMatching.tangentialStressForce` | 4 | 7 | `((WithLp.ofLp 2 x 1) / (Real.sqrt (2 * (AxisymmetricFields.r` | `(-(WithLp.ofLp 2 x 0) / (Real.sqrt (2 * (AxisymmetricFields.` | `-(LeadingStress.radialDivergence 1 axial (AxisymmetricFields` |

#### 45. F00068: 13 members, score 7.33

*Reading (model, not evidence):* G. Aperture noise: the skeleton is `⟨h1⟩ * ⟨h2⟩`.

- found by: anti-unification (AU@1.0, AU@0.7); also F00081, F00103, F00318, F01315 (4 overlapping records folded in)
- kinds: 12 def, 1 abbrev; 12 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 560 declarations use a member; 276 theorem statements mention one; 1 member pairs occur together in a statement
- lemma family: 3 identical shapes (13 theorems; 0 shapes held by every member), 3 shared roles (8 theorems; 0 roles held by every member), out of 276 statements about the members
- concept-count estimate: 12 definitions + 10 lemma statements by identical shape (low), or + 4 by role (high); penalty 3; score 7.33
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 1 nodes over 11 distinct bodies:

  ```
  ⟨h1⟩ * ⟨h2⟩
  ```
- holes: 2, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ numeral ×9, constant ×2; 8 distinct values
  - ⟨h2⟩ constant; 11 distinct values

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `EulerBaseDatum.firstFrequencyPower` | 4 | 5 | `1010` | `EulerPacketUniformSource.frequencyPower` |
| `EulerBaseDatum.uniformL2Amplitude` | 2 | 11 | `EulerBaseDatum.uniformAmplitude` | `EulerBaseDatum.volumeFactor` |
| `EulerMeanHarmonic.boundaryLocalizationC2` | 20 | 52 | `4` | `EulerMeanHarmonic.weakHarmonicSmallBallConstant` |
| `EulerOrdinarySobolev.logarithmicGradientConstant` | 4 | 5 | `36` | `EulerWholeSpaceGaussian.splitCost` |
| `EulerPacketFirstLowBounds.firstRatio` | 9 | 25 | `4` | `EulerPacketGeometryLowBounds.cutoffBound` |
| `EulerPacketTerminalDatum.period` | 213 | 407 | `2` | `Real.pi` |
| `NavierStokes.HarmonicFields.period` | 6 | 17 | (same body as another member) |  |
| `NavierStokes.LiftedMeanResidual.period` | 1 | 22 | (same body as another member) |  |
| `NavierStokes.OutgoingEntranceCone.pressureBound` | 5 | 16 | `10` | `FuturePressureBounds.envelopeConstant` |
| `NavierStokes.PulseCone.mainRatioBound` | 2 | 5 | `2` | `OutgoingPulseBounds.mainBound` |
| `NavierStokesR3.LocalizedFluxEstimates.weightLaplacianConstant` | 3 | 4 | `3` | `LocalizedFluxEstimates.weightSecondDerivativeConstant` |
| `NavierStokesR3.PressureFlux.localPairConstant` | 6 | 7 | `PressureFlux.rieszSobolevConstant` | `PressureFluxTest.cutoffDerivativeConstant` |
| `NavierStokesR3.PressureFlux.rieszSobolevConstant` | 1 | 4 | `3` | `WeightedSobolev.sobolevConstant` |

#### 46. F00071: 6 members, score 7

*Reading (model, not evidence):* F. The i-th basis vector `EuclideanSpace.single i 1` under six names, verbatim.

- found by: body (L0, L1, L2, L3); also F00107 (1 overlapping records folded in)
- kinds: 6 def; 6 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 396 declarations use a member; 77 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 2 shared roles (5 theorems; 0 roles held by every member), out of 77 statements about the members
- concept-count estimate: 5 definitions + 1 lemma statements by identical shape (low), or + 2 by role (high); penalty 1; score 7
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 3 nodes over 1 distinct bodies:

  ```
  EuclideanSpace.single p0 1
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerCylinderPathProduct.basisVector` | 2 | 6 | `EuclideanSpace.single i 1` |
| `EulerLpFiniteTensor.direction` | 6 | 12 | `EuclideanSpace.single i 1` |
| `EulerOrdinarySobolev.axis` | 16 | 48 | `EuclideanSpace.single i 1` |
| `EulerPacketCofactor.basis` | 1 | 6 | `EuclideanSpace.single i 1` |
| `EulerPacketParentLabelBounds.direction` | 20 | 26 | `EuclideanSpace.single i 1` |
| `NavierStokes.ProblemStatement.coordinateVector` | 32 | 299 | `EuclideanSpace.single i 1` |

#### 47. F00072: 10 members, score 7

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F02391, F03346 (2 overlapping records folded in)
- kinds: 10 def; 9 modules; instance arguments per member 0–4, type arguments 0–2
- usage: 134 declarations use a member; 67 theorem statements mention one; 2 member pairs occur together in a statement
- lemma family: 2 identical shapes (4 theorems; 0 shapes held by every member), 1 shared roles (6 theorems; 0 roles held by every member), out of 67 statements about the members
- concept-count estimate: 9 definitions + 2 lemma statements by identical shape (low), or + 5 by role (high); penalty 2; score 7
- the general form already exists: `EulerLpTranslation.SmoothL2Field.mapField`; the skeleton below is over its named specialisations
- similarity 0.006 (smallest share of a member outside compound holes), skeleton of 1 nodes over 9 distinct bodies:

  ```
  SmoothL2Field.mapField ⟨h1⟩ ⟨h2⟩
  ```
- holes: 2, effective parameters 2; the holes vary independently (more joint combinations than any one hole has values)
  - ⟨h1⟩ term ×8, constant ×1; 8 distinct values; compound
  - ⟨h2⟩ term ×6, parameter ×3; 8 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `EulerLpTranslation.SmoothL2Field.directionalField` | 18 | 38 | `DFunLike.coe (ContinuousLinearMap.apply Real V) v` | `SmoothL2Field.derivative A` |
| `EulerLpTranslation.SmoothL2Field.mapField` | 16 | 52 | (the general form) |  |
| `EulerOrdinarySobolev.componentField` | 5 | 6 | `EuclideanSpace.proj j` | `A` |
| `EulerOrdinarySobolev.fieldNeg` | 4 | 22 | `-(ContinuousLinearMap.id Real V)` | `A` |
| `EulerOrdinarySobolev.scaleField` | 12 | 15 | `c • (ContinuousLinearMap.id Real V)` | `A` |
| `EulerOrdinarySobolev.vorticityField` | 3 | 9 | `EulerPacketPiola.curlOperator` | `SmoothL2Field.derivative A` |
| `EulerSmoothEulerEvolution.rhs` | 2 | 3 | `-(ContinuousLinearMap.id Real (EuclideanSpace Real (Fin 3)))` | `SmoothL2Field.addField (EulerSmoothEulerEvolution.advection ` |
| `EulerStaticEuler.localDerivativeField` | 2 | 3 | `((Inv.inv (EulerStaticEuler.amplitude P C R)) ^ 2) • (Contin` | `FieldTower.zeroGraphField P 1 (Budget.timeDerivativeTower P ` |
| `EulerStaticEuler.localField` | 3 | 5 | `(Inv.inv (EulerStaticEuler.amplitude P C R)) • (ContinuousLi` | `EulerConstantEuler.field P 1 (Field.toFieldTower P 1 ((Euler` |
| `EulerStaticEuler.localForceField` | 2 | 3 | `((Inv.inv (EulerStaticEuler.amplitude P C R)) ^ 2) • (Contin` | `FieldTower.zeroGraphField P 1 (ExactLiftedPacket.pressure (E` |

#### 48. F00073: 2 members, score 7

*Reading (model, not evidence):* E. Two verbatim copies of an L² translation operator in two modules.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0, AU@0.7); also F00146, F00169, F00192 (3 overlapping records folded in)
- kinds: 2 def; 2 modules; instance arguments per member 0–2, type arguments 0–1
- usage: 157 declarations use a member; 76 theorem statements mention one; 0 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 5 shared roles (12 theorems; 5 roles held by every member), out of 76 statements about the members
- concept-count estimate: 1 definitions + 0 lemma statements by identical shape (low), or + 6 by role (high); penalty 1; score 7
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 13 nodes over 1 distinct bodies:

  ```
  Lp.compMeasurePreservingₗᵢ 2 MeasureSpace.volume MeasureSpace.volume Real (fun x0 : (EuclideanSpace Real (Fin 3)) ↦ (x0 + p0))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `EulerLpTranslation.translation` | 24 | 53 | `MeasureTheory.Lp.compMeasurePreservingₗᵢ ℝ (fun x ↦ x + a) ⋯` |
| `EulerMeanSolenoidal.translation` | 52 | 112 | `MeasureTheory.Lp.compMeasurePreservingₗᵢ ℝ (fun x ↦ x + a) ⋯` |

#### 49. F00074: 12 members, score 7

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00475, F01011, F01060, F01527, F02263 (5 overlapping records folded in)
- kinds: 12 def; 5 modules; instance arguments per member 0–2, type arguments 0–2
- usage: 156 declarations use a member; 107 theorem statements mention one; 32 member pairs occur together in a statement
- lemma family: 2 identical shapes (4 theorems; 0 shapes held by every member), 2 shared roles (6 theorems; 0 roles held by every member), out of 107 statements about the members
- concept-count estimate: 11 definitions + 2 lemma statements by identical shape (low), or + 3 by role (high); penalty 2; score 7
- the general form already exists: `NavierStokes.LabelSumBounds.fieldSum`; the skeleton below is over its named specialisations
- similarity 0.083 (smallest share of a member outside compound holes), skeleton of 3 nodes over 10 distinct bodies:

  ```
  LabelSumBounds.fieldSum ⟨h1⟩ (fun x0 : ⟨h2⟩ ↦ (HarmonicBlock.oscillation ⟨h3⟩))
  ```
- holes: 3, effective parameters 3; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ function; 3 distinct values; compound
  - ⟨h2⟩ parameter ×8, type ×2; 2 distinct values; compound
  - ⟨h3⟩ term; 10 distinct values; depends on a bound variable, so the parameter must be a function; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `NavierStokes.ActualCyclePreservation.primaryField` | 4 | 6 | `ActualPrimary.activeLabels ActualPrimary.standardRegion B N0` | `Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (Pro` | `ActualInitialization.tangentBlock B N0 ⟨bound↑1⟩` |
| `NavierStokes.ActualSignedMeanBinding.actualPrimaryField` | 1 | 3 | (same body as another member) |  |  |
| `NavierStokes.ActualSignedMeanBinding.actualSignedField` | 1 | 3 | `ActualPrimary.activeLabels ActualPrimary.standardRegion B N0` | `Prod (BaseChartJets.CellIndex (TailData.h (Profile.data (Pro` | `ActualSignedMeanBinding.actualSignedBlock B N0 c u ⟨bound↑1⟩` |
| `CorrectionStep.CycleParameters.particularGaussian` | 4 | 27 | `CycleCoefficients.labels v` | `ι` | `CycleParameters.particularGaussianBlock p v c u ⟨bound↑1⟩` |
| `CorrectionStep.CycleParameters.particularVelocity` | 27 | 69 | `CycleCoefficients.labels v` | `ι` | `CycleParameters.particularBlock p v c u ⟨bound↑1⟩` |
| `CorrectionStep.CycleParameters.signedGaussian` | 4 | 25 | `CycleCoefficients.labels v` | `ι` | `CycleParameters.signedGaussianBlock p v c u ⟨bound↑1⟩` |
| `CorrectionStep.CycleParameters.signedVelocity` | 24 | 62 | `CycleCoefficients.labels v` | `ι` | `CycleParameters.signedBlock p v c u ⟨bound↑1⟩` |
| `NavierStokes.LabelSumBounds.fieldSum` | 30 | 71 | (the general form) |  |  |
| `NavierStokes.SignedMeanGain.curlField` | 3 | 9 | `Assembly.labels a` | `ι` | `(SignedFamily.curl f) ⟨bound↑1⟩` |
| `NavierStokes.SignedMeanGain.oldField` | 3 | 9 | `Assembly.labels a` | `ι` | `(SignedFamily.old f) ⟨bound↑1⟩` |
| `NavierStokes.SignedMeanGain.primaryField` | 3 | 11 | `Assembly.labels a` | `ι` | `(SignedFamily.primary f) ⟨bound↑1⟩` |
| `NavierStokes.SignedMeanGain.tangentField` | 3 | 12 | `Assembly.labels a` | `ι` | `(SignedFamily.tangent f) ⟨bound↑1⟩` |

#### 50. F00075: 8 members, score 7

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00873, F01667, F02264, F02551, F03483 (5 overlapping records folded in)
- kinds: 8 def; 6 modules; instance arguments per member 0–2, type arguments 0–2
- usage: 243 declarations use a member; 167 theorem statements mention one; 22 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 5 shared roles (17 theorems; 0 roles held by every member), out of 167 statements about the members
- concept-count estimate: 7 definitions + 0 lemma statements by identical shape (low), or + 7 by role (high); penalty 2; score 7
- the general form already exists: `NavierStokes.VariableGaugeMean.reconstructState`; the skeleton below is over its named specialisations
- similarity 0.083 (smallest share of a member outside compound holes), skeleton of 1 nodes over 7 distinct bodies:

  ```
  VariableGaugeMean.reconstructState ⟨h1⟩ ⟨h2⟩ ⟨h3⟩
  ```
- holes: 3, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ parameter ×5, constant ×2; 2 distinct values
  - ⟨h2⟩ parameter ×5, term ×2; 2 distinct values; compound
  - ⟨h3⟩ term; 7 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `NavierStokes.ActualInitialMean.primary` | 4 | 9 | `ActualPrimary.commonGauge` | `ActualPrimary.commonContext B` | `ActualInitialMean.seed B N0` |
| `NavierStokes.ActualInitialization.primaryState` | 0 | 5 | `ActualPrimary.commonGauge` | `ActualPrimary.commonContext B` | `ActualInitialization.sourceState B N0` |
| `CorrectionInitialization.GaugeInitialization.primaryBands` | 2 | 10 | `g` | `c` | `CorrectionInitialization.bandSeed labels pieces baseError` |
| `NavierStokes.CorrectionStep.gaugeWaveStage` | 4 | 9 | `g` | `c` | `State.addIncrement u CorrectionStep.zeroTriple 0 w q e` |
| `NavierStokes.SignedMeanGain.waveStage` | 24 | 37 | `g` | `c` | `State.addIncrement u SignedMeanGain.zeroTriple 0 w q (Exclud` |
| `NavierStokes.VariableGaugeMean.rankStageState` | 16 | 32 | `g` | `c` | `State.addIncrement u (VariableGaugeMean.rankIncrementState g` |
| `NavierStokes.VariableGaugeMean.reconstructState` | 90 | 162 | (the general form) |  |  |
| `NavierStokes.VariableGaugeMean.temporalStageState` | 27 | 50 | `g` | `c` | `State.addIncrement u (VariableGaugeMean.temporalIncrementSta` |

#### 51. F00077: 8 members, score 7

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); anti-unification (AU@1.0)
- kinds: 8 abbrev; 8 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 367 declarations use a member; 99 theorem statements mention one; 1 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 1 shared roles (7 theorems; 0 roles held by every member), out of 99 statements about the members
- concept-count estimate: 7 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 7
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 11 nodes over 1 distinct bodies:

  ```
  Prod (Prod Real (Prod Real (Prod Real Real))) (Prod Real Real)
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualSignedNativeProfiles.LiftPoint` | 0 | 3 | `NavierStokes.PhysicalGraphBounds.LiftPoint` |
| `NavierStokes.ActualSignedPhysicalData.LiftPoint` | 16 | 36 | `NavierStokes.PhysicalGraphBounds.LiftPoint` |
| `NavierStokes.CartesianCopySource.LiftPoint` | 6 | 17 | `NavierStokes.PhysicalWaveSum.LiftPoint` |
| `NavierStokes.CurrentPhysicalChartJets.LiftPoint` | 4 | 18 | `NavierStokes.PhysicalWaveSum.LiftPoint` |
| `NavierStokes.InitialPhysicalData.LiftPoint` | 20 | 62 | `NavierStokes.PhysicalGraphBounds.LiftPoint` |
| `NavierStokes.PhysicalGraphBounds.LiftPoint` | 20 | 177 | `NavierStokes.PhysicalGraphBounds.ChartPoint × NavierStokes.PhysicalGraphBounds.Plane` |
| `NavierStokes.PhysicalWaveSum.LiftPoint` | 31 | 229 | `NavierStokes.PhysicalGraphBounds.LiftPoint` |
| `NavierStokes.PositiveTimeCopyFamily.LiftPoint` | 2 | 17 | `NavierStokes.PhysicalGraphBounds.LiftPoint` |

#### 52. F00078: 5 members, score 7

*Reading (model, not evidence):* A. The same type written out again under a local name (`abbrev`), module after module. No holes. Merging removes names only: the abbreviations are transparent, so no statement or proof changes.

- found by: body (L0, L1, L2, L3); also F00163, F00224 (2 overlapping records folded in)
- kinds: 5 abbrev; 5 modules; instance arguments per member 0–0, type arguments 1–1
- usage: 1,201 declarations use a member; 520 theorem statements mention one; 10 member pairs occur together in a statement
- lemma family: 3 identical shapes (6 theorems; 0 shapes held by every member), 3 shared roles (12 theorems; 0 roles held by every member), out of 520 statements about the members
- concept-count estimate: 4 definitions + 3 lemma statements by identical shape (low), or + 0 by role (high); penalty 1; score 7
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 7 nodes over 1 distinct bodies:

  ```
  Prod Real (Prod p0 (Prod Real Real))
  ```
- no holes: the bodies are identical up to bound names

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.CorrectionState.Lift` | 30 | 99 | `NavierStokes.PressureStream.Lift S` |
| `NavierStokes.DefectIncrementBounds.Point` | 28 | 70 | `NavierStokes.PressureStream.Lift P` |
| `NavierStokes.GaugeAliasDecay.Point` | 24 | 26 | `NavierStokes.PressureStream.Lift S` |
| `NavierStokes.LocalRankDefect.Point` | 80 | 182 | `NavierStokes.PressureStream.Lift P` |
| `NavierStokes.PressureStream.Lift` | 358 | 989 | `ℝ × S × NavierStokes.PressureStream.Plane` |

#### 53. F00079: 4 members, score 7

*Reading (model, not evidence):* D, and a positive control. `MemClass`, `UniformClass`, `LocalClass`, `LocalJets`: weighted smoothness classes that differ in an extra index or a localising set, each with `add` / `sub` / `neg` / `mul` / `bilinear` / `map`. The bodies differ by inserted binders, which the body channel cannot express.

- found by: lemma roles (ROLE@0.15); also F00118 (1 overlapping records folded in)
- kinds: 4 structure; 4 modules; instance arguments per member 4–4, type arguments 2–3
- usage: 453 declarations use a member; 243 theorem statements mention one; 12 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 18 shared roles (66 theorems; 5 roles held by every member), out of 243 statements about the members
- concept-count estimate: 3 definitions + 0 lemma statements by identical shape (low), or + 32 by role (high); penalty 5; score 7
- no common body (the generalisation is a single hole): a shared interface would have to be a structure or class, not a parameter

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.LabelSumBounds.UniformClass` | 88 | 147 | `(∀ x0 : ι, (∀ x1 : Nat, (∀ x2 : D, ((x2 ∈ (StripData.domain s)) → (0 ≤ (w x0 x1 x2)))))) ∧ (∀ x0 : ι, (∀ x1 : ` |
| `NavierStokes.LocalizedWaveBounds.LocalClass` | 45 | 90 | `(∀ x0 : Nat, (∀ x1 : I, (∀ x2 : D, ((x2 ∈ (StripData.domain s)) → (0 ≤ (w x0 x1 x2)))))) ∧ (∀ x0 : Nat, (∀ x1 ` |
| `NavierStokes.PeriodizedWaveBounds.LocalJets` | 36 | 42 | `(∀ x0 : Nat, (∀ x1 : I, (∀ x2 : D, ((x2 ∈ (StripData.domain s)) → ((x2 ∈ (K x0 x1)) → (ContDiffAt Real (WithTo` |
| `NavierStokes.WeightedClasses.MemClass` | 74 | 195 | `(∀ x0 : Nat, (∀ x1 : D, ((x1 ∈ (StripData.domain s)) → (0 ≤ (w x0 x1))))) ∧ (∀ x0 : Nat, (ContDiffOn Real (Wit` |

#### 54. F00080: 6 members, score 7

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F00731, F00814, F01043, F01243, F02495, F02497 (6 overlapping records folded in)
- kinds: 6 def; 1 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 151 declarations use a member; 91 theorem statements mention one; 11 member pairs occur together in a statement
- lemma family: 4 identical shapes (8 theorems; 0 shapes held by every member), 2 shared roles (12 theorems; 1 roles held by every member), out of 91 statements about the members
- concept-count estimate: 5 definitions + 4 lemma statements by identical shape (low), or + 9 by role (high); penalty 2; score 7
- the general form already exists: `NavierStokes.OutgoingHistories.history`; the skeleton below is over its named specialisations
- similarity 0.125 (smallest share of a member outside compound holes), skeleton of 1 nodes over 5 distinct bodies:

  ```
  OutgoingHistories.history ⟨h1⟩ ⟨h2⟩
  ```
- holes: 2, effective parameters 1; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ function; 5 distinct values; compound
  - ⟨h2⟩ function; 5 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ |
|---|---:|---:|---|---|
| `NavierStokes.OutgoingHistories.I` | 13 | 32 | `OutgoingHistories.initialI d` | `OutgoingHistories.angularWeight d K w` |
| `NavierStokes.OutgoingHistories.J` | 15 | 35 | `OutgoingHistories.initialJ d` | `OutgoingHistories.transportWeight d K w Amp` |
| `NavierStokes.OutgoingHistories.M` | 16 | 45 | `OutgoingHistories.initialM` | `OutgoingHistories.massWeight d Amp` |
| `NavierStokes.OutgoingHistories.Pi` | 18 | 39 | `OutgoingHistories.initialPi d` | `OutgoingHistories.pressureWeight d K w` |
| `NavierStokes.OutgoingHistories.S` | 23 | 44 | `OutgoingHistories.initialS d` | `OutgoingHistories.energyWeight d K w Amp` |
| `NavierStokes.OutgoingHistories.history` | 6 | 21 | (the general form) |  |

#### 55. F00084: 14 members, score 6.5

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F01906, F02753, F03679, F03928, F04006 (5 overlapping records folded in)
- kinds: 14 def; 8 modules; instance arguments per member 1–1, type arguments 0–1
- usage: 242 declarations use a member; 99 theorem statements mention one; 12 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 0 shared roles (0 theorems; 0 roles held by every member), out of 99 statements about the members
- concept-count estimate: 13 definitions + 0 lemma statements by identical shape (low), or + 0 by role (high); penalty 2; score 6.5
- the general form already exists: `EulerPacketCylinderField.Field.ofLifted`; the skeleton below is over its named specialisations
- similarity 0.14 (smallest share of a member outside compound holes), skeleton of 6 nodes over 13 distinct bodies:

  ```
  Field.ofLifted p0 ⟨h1⟩ ⟨h2⟩ ⟨h3⟩ (fun x0 : (Set.Elem (Set.Icc 0 ⟨h1⟩)) ↦ ⟨h4⟩)
  ```
- holes: 4, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ parameter ×12, term ×1; 2 distinct values; compound
  - ⟨h2⟩ function ×11, parameter ×1, numeral ×1; 13 distinct values; compound
  - ⟨h3⟩ term ×12, numeral ×1; 13 distinct values; compound
  - ⟨h4⟩ function; 13 distinct values; depends on a bound variable, so the parameter must be a function; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ | ⟨h4⟩ |
|---|---:|---:|---|---|---|---|
| `EulerMeanPacketProvider.Forcing.toCylinderField` | 5 | 10 | `Data.T D` | `raw` | `DFunLike.coe (EulerMeanPacketProvider.spatialEmbeddingPath P` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.add` | 4 | 37 | `T` | `raw + raw'` | `(Field.path G) + (Field.path H)` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.angleMean` | 3 | 9 | `T` | `EulerPacketProfileRecursion.angleMean P raw` | `DFunLike.coe (EulerCylinderAngleAverage.pathAverage P) (Fiel` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.finsetSum` | 5 | 19 | `T` | `Finset.sum s f` | `Finset.sum s (fun x0 : ι ↦ (Field.path (G x0)))` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.freeze` | 6 | 10 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `DFunLike.coe (EulerContinuousTimeFreeze.freezePath t) (Field` | `EulerCylinderSmoothOrbit.pointField P (Field.path G) t` |
| `EulerPacketCylinderField.Field.map` | 16 | 25 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `DFunLike.coe (EulerCylinderConstantMap.pathMap P L) (Field.p` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.multiply` | 0 | 2 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `DFunLike.coe (DFunLike.coe (EulerLpCylinderRectangular.fullM` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.neg` | 3 | 7 | `T` | `-raw` | `-(Field.path G)` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.ofLifted` | 0 | 13 | (the general form) |  |  |  |
| `EulerPacketCylinderField.Field.smul` | 37 | 113 | `T` | `c • raw` | `c • (Field.path G)` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.weighted` | 5 | 9 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `DFunLike.coe (EulerContinuousTimeWeight.weight g) (Field.pat` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.Field.zero` | 6 | 34 | `T` | `0` | `0` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerPacketCylinderField.scalarEmbeddingField` | 2 | 7 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `DFunLike.coe (EulerCylinderConstantMap.pathMap P EulerCylind` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |
| `EulerStaticCylinder.field` | 7 | 32 | `T` | `fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3)) Real` | `ContinuousMap.const (Set.Elem (Set.Icc 0 T)) (DFunLike.coe (` | `fun x0 : (Prod (EuclideanSpace Real (Fin 3)) (AddCircle P)) ` |

#### 56. F00085: 7 members, score 6.5

*Reading (model, not evidence):* F. `Polynomial.natDegree` of seven different polynomials: a naming habit more than a family.

- found by: body (L2, L3); anti-unification (AU@1.0, AU@0.7, AU@0.5)
- kinds: 7 def; 7 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 82 declarations use a member; 54 theorem statements mention one; 6 member pairs occur together in a statement
- lemma family: 1 identical shapes (2 theorems; 0 shapes held by every member), 2 shared roles (16 theorems; 1 roles held by every member), out of 54 statements about the members
- concept-count estimate: 6 definitions + 1 lemma statements by identical shape (low), or + 7 by role (high); penalty 2; score 6.5
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 1 nodes over 7 distinct bodies:

  ```
  Polynomial.natDegree ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ constant; 7 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerPacketInitialAmplitude.degree` | 5 | 7 | `EulerPacketInitialAmplitude.polynomial` |
| `EulerPacketInitializedCost.uniformPower` | 8 | 15 | `EulerPacketInitializedCost.polynomial` |
| `EulerPacketInitializedOutputCost.uniformPower` | 15 | 23 | `EulerPacketInitializedOutputCost.polynomial` |
| `EulerPacketUniformSource.frequencyPower` | 9 | 19 | `EulerPacketUniformSource.frequencyPolynomial` |
| `EulerParentBadRatio.degree` | 6 | 10 | `EulerParentBadRatio.polynomial` |
| `EulerParentHistoryCost.labelHistoryPower` | 4 | 13 | `EulerParentHistoryCost.labelHistoryPolynomial` |
| `EulerParentNeighborCost.degree` | 7 | 12 | `EulerParentNeighborCost.polynomial` |

#### 57. F00089: 22 members, score 6.2

*Reading (model, not evidence):* G. Twenty-two definitions whose body is a single other constant: aliases.

- found by: anti-unification (AU@1.0, AU@0.7, AU@0.5); also F00376, F00409, F00706, F01792, F01851, F02039, F02149, F03425 … (10 overlapping records folded in)
- kinds: 16 abbrev, 6 def; 13 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 1,768 declarations use a member; 828 theorem statements mention one; 22 member pairs occur together in a statement
- lemma family: 5 identical shapes (11 theorems; 0 shapes held by every member), 8 shared roles (52 theorems; 0 roles held by every member), out of 828 statements about the members
- concept-count estimate: 21 definitions + 6 lemma statements by identical shape (low), or + 10 by role (high); penalty 5; score 6.2
- each body is a single constant or parameter (the generalisation is one leaf hole): a family of aliases

| member | stmt | users | body |
|---|---:|---:|---|
| `NavierStokes.ActualCycleCoherence.geometry` | 10 | 14 | `NavierStokes.ActualMeanPhysicalData.initialGeometry` |
| `NavierStokes.ActualCycleCoherence.overlap` | 14 | 19 | `NavierStokes.ActualInitialCoherence.overlap` |
| `NavierStokes.ActualSignedExterior.active` | 17 | 18 | `NavierStokes.ActualPolarCoverage.active` |
| `NavierStokes.ActualSignedStageControls.fullStrip` | 119 | 159 | `NavierStokes.ActualPrimaryBounds.fullStrip` |
| `NavierStokes.ActualValidBandWaves.gluedPotential` | 0 | 1 | `@NavierStokes.ActualValidBandWaves.potential` |
| `NavierStokes.ActualValidBandWaves.gluedPressure` | 0 | 1 | `@NavierStokes.ActualValidBandWaves.pressure` |
| `NavierStokes.ChartScales.Tg` | 70 | 145 | `NavierStokes.SlotColoring.coverGrowth` |
| `CorrectionInitialization.ActualPrimary.profile` | 444 | 1097 | `NavierStokes.FinalSlowBase.actualProfile` |
| `NavierStokes.DependentSignedPhysicalFamily.NativeLabel` | 12 | 109 | `NavierStokes.ActualSignedPhysicalData.NativeLabel` |
| `NavierStokes.GlobalSlowProfiles.Exterior` | 22 | 30 | `NavierStokes.SlowStressSupport.exterior` |
| `NavierStokes.GlobalSlowProfiles.de` | 2 | 6 | `NavierStokes.ProfileHistories.parameterPartial` |
| `NavierStokes.GlobalSlowProfiles.dr` | 1 | 5 | `NavierStokes.ProfileHistories.radialPartial` |
| `NavierStokes.OutgoingHistories.dEta` | 58 | 98 | `NavierStokes.ProfileHistories.parameterPartial` |
| `NavierStokes.OutgoingHistories.dY` | 14 | 45 | `NavierStokes.ProfileHistories.radialPartial` |

… and 8 more members (all in `clusters.jsonl`).

#### 58. F00091: 4 members, score 6

*Reading (model, not evidence):* F. One map applied to a frame and its first and second derivative.

- found by: body (L3); anti-unification (AU@1.0, AU@0.7); also F00108, F00190, F00282 (3 overlapping records folded in)
- kinds: 4 def; 1 modules; instance arguments per member 5–5, type arguments 2–2
- usage: 67 declarations use a member; 50 theorem statements mention one; 25 member pairs occur together in a statement
- lemma family: 7 identical shapes (16 theorems; 0 shapes held by every member), 4 shared roles (11 theorems; 0 roles held by every member), out of 50 statements about the members
- concept-count estimate: 3 definitions + 9 lemma statements by identical shape (low), or + 7 by role (high); penalty 2; score 6
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 4 nodes over 4 distinct bodies:

  ```
  DFunLike.coe (EulerLpCylinderRectangular.fullPathMap p0) (⟨h1⟩ p1)
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ head; 4 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerCylinderDirichlet.Coefficients.frame` | 18 | 50 | `Coefficients.Q` |
| `EulerCylinderDirichlet.Coefficients.frameDerivative` | 18 | 50 | `Coefficients.Q₁` |
| `EulerCylinderDirichlet.Coefficients.frameSecond` | 2 | 8 | `Coefficients.Q₂` |
| `EulerCylinderDirichlet.Coefficients.hessian` | 12 | 36 | `Coefficients.H` |

#### 59. F00092: 4 members, score 6

*Reading (model, not evidence):* F. Inner, middle and outer cutoff: one bump-function construction at different radii.

- found by: anti-unification (AU@1.0, AU@0.7); body and lemma shapes; also F00093, F00120, F00154, F00307 (4 overlapping records folded in)
- kinds: 4 def; 2 modules; instance arguments per member 0–0, type arguments 0–0
- usage: 84 declarations use a member; 46 theorem statements mention one; 6 member pairs occur together in a statement
- lemma family: 4 identical shapes (13 theorems; 2 shapes held by every member), 2 shared roles (7 theorems; 1 roles held by every member), out of 46 statements about the members
- concept-count estimate: 3 definitions + 9 lemma statements by identical shape (low), or + 4 by role (high); penalty 2; score 6
- similarity 1.0 (smallest share of a member outside compound holes), skeleton of 2 nodes over 4 distinct bodies:

  ```
  ContDiffBump.toFun 0 ⟨h1⟩
  ```
- holes: 1, effective parameters 1
  - ⟨h1⟩ constant; 4 distinct values

| member | stmt | users | ⟨h1⟩ |
|---|---:|---:|---|
| `EulerMeanHarmonic.innerCutoff` | 12 | 15 | `EulerMeanHarmonic.innerBump` |
| `EulerMeanHarmonic.middleCutoff` | 8 | 10 | `EulerMeanHarmonic.middleBump` |
| `EulerMeanHarmonic.outerCutoff` | 9 | 12 | `EulerMeanHarmonic.outerBump` |
| `NavierStokes.SmoothCutoffs.cutoff` | 17 | 55 | `SmoothCutoffs.cutoffBump` |

#### 60. F00095: 11 members, score 6

*Reading (model, not evidence):* C. Named instances of a general definition the corpus already has (the head of the skeleton). The parameterised primitive exists; what could shrink is the number of names and the lemmas restated per instance.

- found by: specialisation (WRAP); also F01447, F02592, F02789, F03320, F03322, F03323 (6 overlapping records folded in)
- kinds: 11 def; 7 modules; instance arguments per member 1–3, type arguments 0–1
- usage: 118 declarations use a member; 55 theorem statements mention one; 14 member pairs occur together in a statement
- lemma family: 0 identical shapes (0 theorems; 0 shapes held by every member), 2 shared roles (4 theorems; 0 roles held by every member), out of 55 statements about the members
- concept-count estimate: 10 definitions + 0 lemma statements by identical shape (low), or + 2 by role (high); penalty 2; score 6
- the general form already exists: `EulerPacketCylinderField.Field.changeTime`; the skeleton below is over its named specialisations
- similarity 0.015 (smallest share of a member outside compound holes), skeleton of 7 nodes over 10 distinct bodies:

  ```
  Field.changeTime (2 * Real.pi) (Data.T p0) ⟨h1⟩ (Data.T ⟨h2⟩) ⟨h3⟩
  ```
- holes: 3, effective parameters 2; the holes do not vary independently (no more joint combinations than the most varied hole has values)
  - ⟨h1⟩ function; 10 distinct values; compound
  - ⟨h2⟩ parameter; 2 distinct values
  - ⟨h3⟩ term; 10 distinct values; compound

| member | stmt | users | ⟨h1⟩ | ⟨h2⟩ | ⟨h3⟩ |
|---|---:|---:|---|---|---|
| `EulerPacketCylinderField.Field.changeTime` | 5 | 41 | (the general form) |  |  |
| `EulerPacketTerminalDatum.forwardInitializedCovectorRemainderField` | 1 | 2 | `EulerPacketPressure.covectorRemainder N (EulerPacketTerminal` | `D` | `EulerPacketPressure.covectorRemainderField (2 * Real.pi) (Da` |
| `EulerPacketTerminalDatum.forwardInitializedNormalizedField` | 15 | 41 | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` | `D` | `Field.smul (2 * Real.pi) (Data.T M) (fun x0 : (Prod Real (Pr` |
| `EulerPacketTerminalDatum.forwardInitializedNormalizedResidualField` | 8 | 30 | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` | `D` | `Field.smul (2 * Real.pi) (Data.T M) (fun x0 : (Prod Real (Pr` |
| `EulerPacketTerminalDatum.forwardInitializedVelocityDerivativeField` | 1 | 5 | `EulerPacketPointJets.fieldSum (N + 1) κ (ProfileRegularity.v` | `D` | `ProfileRegularity.velocityDerivativeField (2 * Real.pi) (Dat` |
| `EulerPacketTerminalDatum.forwardInitializedVelocityField` | 4 | 10 | `EulerPacketPointJets.fieldSum (N + 1) κ (EulerPacketProfileR` | `D` | `ProfileRegularity.velocityField (2 * Real.pi) (Data.T M) N (` |
| `EulerPacketTerminalDatum.initializedCovectorRemainderField` | 1 | 2 | `EulerPacketPressure.covectorRemainder N (EulerPacketTerminal` | `D` | `EulerPacketPressure.covectorRemainderField (2 * Real.pi) (Da` |
| `EulerPacketTerminalDatum.initializedNormalizedField` | 11 | 26 | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` | `D` | `Field.smul (2 * Real.pi) (Data.T M) (fun x0 : (Prod Real (Pr` |
| `EulerPacketTerminalDatum.initializedNormalizedResidualField` | 4 | 17 | `k • (fun x0 : (Prod Real (Prod (EuclideanSpace Real (Fin 3))` | `D` | `Field.smul (2 * Real.pi) (Data.T M) (fun x0 : (Prod Real (Pr` |
| `EulerPacketTerminalDatum.initializedVelocityDerivativeField` | 1 | 5 | `EulerPacketPointJets.fieldSum (N + 1) κ (ProfileRegularity.v` | `D` | `ProfileRegularity.velocityDerivativeField (2 * Real.pi) (Dat` |
| `EulerPacketTerminalDatum.initializedVelocityField` | 4 | 10 | `EulerPacketPointJets.fieldSum (N + 1) κ (EulerPacketProfileR` | `D` | `ProfileRegularity.velocityField (2 * Real.pi) (Data.T M) N (` |

## 6. Files

- `out/families/ns/clusters.jsonl`: every family record (one per distinct member set over all channels), highest score first, with members, levels, skeleton, holes and their fillers per member, usage, lemma shapes and roles with theorem names, and every score component. `clusters_all.jsonl`: the same over all definitions, dead code included. `clusters_planted.jsonl`: ns with the planted controls mixed in.
- `out/families/ns/summary.json`, `summary_all.json`, `funnel.json`, `planted_result.json`; `out/families/{carleson,pfr}/clusters.jsonl`, `summary.json`, `funnel.json`.
- `out/families/<project>/raw/export.jsonl`: the typed trees from Lean (definition bodies, signatures, theorem statements). `features.pkl`: keys, profiles, usage.
- `tools/families/`: `Export.lean` (tree grammar in its header), `tree.py` (keys, anti-unification, roles, printer), `features.py`, `cluster.py`, `report.py`, `planted/`, `run.sh`.

Limits of the method, stated once:

- Anti-unification is first-order with a hole allowed in head position. A family whose members differ by an extra binder, an extra argument or an inserted structure field is not seen by body (this is why `MemClass` / `UniformClass` and `JetRate` / `FiniteJetRate` are missed by body).
- Structures are encoded as nested `∃ field, …`; inserting a field turns the rest of the structure into one compound hole.
- AU candidates are each definition's 60 nearest neighbours by a label-and-edge cosine, and the agglomeration is greedy, so a pair outside the neighbour lists is missed and cluster boundaries depend on order. A cluster is not grown beyond 250 distinct bodies.
- Erased arguments (instances, proofs, implicit types) are not compared. Two definitions that differ only there have equal keys. This is why 22 definitions "are" `Classical.choose`.
- Tags (coarse types) are part of the keys at L0 to L3 and ignored by AU.
- Non-structure inductive types (15 in ns) and instances are not clustered. 7 theorem statements over 2,500 nodes are not profiled.
- Usage counts come from the dead-code tool's term-dependency export, restricted to reachable declarations.
- Member bodies in the tables are the source bodies; skeletons are computed after unfolding project abbreviations, so a member may show `ProblemStatement.Space` where the skeleton shows `EuclideanSpace ℝ (Fin 3)`.


## 7. After review (2026-11-11)

An independent agent checked this step together with the Lean step (`out/families/FAMILIES.md`, section 10). Its findings about the clustering are readings, not kernel-checked, and were not rerun:

- No control name appears in `cluster.py`, `features.py`, `tree.py` or `Export.lean`; only this report looks names up, to print ranks.
- **15 random family records outside the top 60** (seed 9090, spread over the looseness levels): 4 real families, 6 parallel by construction with different mathematics, 5 accidental. The real ones were at the exact level, the project-heads level and the loosest anti-unification level; none were in the samples from the middle levels, the named-specialisation channel or the lemma channels.
- **Families no channel sees.** Of 30 random reachable definitions (types left out; seed 31337) read with their 5 nearest neighbours by name and signature, 7 (95% interval 12% to 41%) have a neighbour the reviewer would call the same notion that nothing here joins to them. Three have the shape of the one family that paid in Lean: the same structure or module repeated with one inserted argument or a different record (`GradeGuards` in 4 parallel modules; the `PressureStream` module redone in `VariableGaugeMean` with an extra gauge argument; `MeanVector` / `LocalMeanVector` / `WaveVector`). The list is in `out/families/review/nn30.txt`.
- **Consequence for the numbers above.** The "in families" percentages are upper bounds on paper at every level (most loose families are not one idea), and at the same time the method misses the kind of family worth most. Of the top 60 read in the Lean step, 8 were read as one idea with several instances and 20 as one type under many names; measured, the type names are removable as they stand (389 of 389 by `rfl`), and one of the 7 families taken through Lean supplies 99% of the net proof saving, the other six together being break-even.

