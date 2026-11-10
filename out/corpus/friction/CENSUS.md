# Friction census: claims A–D and the "unfolding" claim, measured

Source of this section: `bench/friction_census_verdict.md`, hand-written; every number in braces there is filled from `census.json` (or, for the robustness figures, `robust.json`) when `bench/friction_census.py` runs, so the figures cannot drift from the tables below and from `ROBUSTNESS.md`. Cells are `value [95% bootstrap interval over theorems]`.

**Revised 2026-11-10 after an adversarial review.** The first version of this verdict gave single headline figures for claim D and for the regularity excess, called the unfolding claim "not supported", and said the machine corpus has no function-with-facts packets. Those statements did not survive; the changes are marked "revised" below and the evidence is in `ROBUSTNESS.md`.

Three corpora in Lean 4 with Mathlib: **ns**, OpenAI's machine-generated Navier–Stokes/Euler formalization (38,601 theorems); **Carleson**, human-written harmonic analysis (2,675); **PFR**, human-written combinatorics and entropy (978). The primary comparison is ns against Carleson.

## Result

Of the four places the earlier chat said proofs bloat: B (casts) and C (domain surgery) are close to absent from the machine corpus under every cut tried; they describe Carleson, the human corpus. A (constants) is present and larger than first reported once the project's own predicates are opened: the machine corpus hides `∃ C` witnesses inside home-made predicates. D (side conditions) is present, but its size depends on two counting choices and ranges from about 5.65% to 15.4% of proof mass; the part the chat named (measurability, integrability) is small overall because few ns theorems are about integrals, and where they are it costs what it costs in Carleson. Whether machine proofs unfold what humans keep bundled cannot be told from this data.

| claim | verdict for the machine corpus | ns | Carleson |
|---|---|---|---|
| A. explicit constants | **supported as a pattern; moderate in size** (revised) | 2.45 [2.30, 2.61]% of theorems conclude `∃ C, 0 < C ∧ …` directly, holding 5.09 [4.65, 5.53]% of proof mass; a further 1,509 theorems (3.89% of mass) conclude a project predicate that hides one | 0.037 [0.000, 0.112]% of theorems, none hidden; constants are named definitions instead (28.7 [27.0, 30.5]% of statements) |
| B. ℝ / ℝ≥0 / ℝ≥0∞ casts | **not supported** | 0.074 [0.061, 0.087]% of proof mass on finiteness goals; a cast or finiteness fact in 0.84 [0.75, 0.93]% of statements; in integral / Lp theorems only, finiteness 0.66 [0.50, 0.85]% | 1.76 [1.40, 2.22]% of mass; 26.7 [25.0, 28.4]% of statements; in integral / Lp theorems 1.90 [1.46, 2.40]% |
| C. domain surgery | **not supported** | 1.46 [1.38, 1.54]% of hypotheses; 0.088 [0.083, 0.092]% of library constant uses | 3.02 [2.55, 3.55]% of hypotheses; 0.62 [0.55, 0.70]% of constant uses |
| D. side-condition leakage | **partly supported; size not robust** (revised) | between 5.65% and 15.4% of proof mass depending on the rule (table below); measurability + integrability 2.17 [2.01, 2.32]% overall, 10.5 [9.4, 11.6]% in integral / Lp theorems | between 3.47% and 9.15%; measurability + integrability 6.93 [5.93, 8.00]% overall, 8.29 [7.14, 9.67]% in integral / Lp theorems |
| machine proofs unfold what humans keep bundled | **cannot tell** (revised) | statements are more bundled (bundled morphism type in 26.0 [25.5, 26.4]% of statements; project bundle structure in 40.6 [40.1, 41.1]%); proofs leave no usable trace | 3.07 [2.47, 3.74]%; 13.3 [12.0, 14.6]% |

Claim D under the four combinations of the two counting choices (`ROBUSTNESS.md` section 1). "Outer" charges everything below a side goal to it, including the rewriting and instance terms used to prove it; "inner" charges a node to its nearest enclosing goal. "Derivative-value facts" are `HasDerivAt f f' x`-style statements, which say what a derivative is rather than that a function is smooth.

| claim D, % of proof mass | ns | Carleson | ns − Carleson |
|---|---|---|---|
| outer, derivative-value facts counted (the first version's headline) | 15.4 [14.8, 16.0] | 9.15 [7.70, 10.61] | +6.22 [+4.63, +7.87] |
| outer, derivative-value facts not counted | 10.1 [9.6, 10.6] | 9.07 [7.65, 10.50] | +0.98 [-0.57, +2.58] |
| inner, derivative-value facts counted | 6.90 [6.73, 7.07] | 3.49 [3.16, 3.82] | +3.41 [+3.05, +3.78] |
| inner, derivative-value facts not counted | 5.65 [5.50, 5.80] | 3.47 [3.15, 3.79] | +2.17 [+1.82, +2.55] |

Two things push the other way and are not in these rows: project-defined predicates that contain smoothness facts are classed `other` (charging every theorem that concludes one wholly to D would give 20.3%, an upper bound), and proof obligations of definitions and instances are outside the theorem export (including them gives 15.2% on the first row).

**Largest measured source of bulk in the machine corpus.** In absolute terms it is proving equations: 53.5 [53.1, 53.9]% of proof-term nodes sit under a goal that is an equation (with inequalities, 62.2 [61.9, 62.6]%). The chat did not list this, and it is not specific to the machine: the share is higher in Carleson (58.7 [57.9, 59.6]%) and PFR (68.5 [66.9, 70.1]%). Of the things the machine corpus has *more* of than Carleson, the one that survives every control is type-class instance arguments, which the chat did not predict (revised):

- type-class instance arguments: 27.1 [26.8, 27.4]% of proof-term nodes against 16.6 [16.1, 17.1]%, a raw difference of +10.5 [+9.9, +11.1] points, rising to 40.0 [39.4, 40.7]% in the Euler half. Part of the raw gap is proof size: instance share falls with proof size in both corpora and ns mass sits in smaller proofs. Standardised for size the excess is +6.30 to +8.93 points; in theorems about integrals or Lp norms it is +23.7 [+22.1, +25.2] points (39.3 [38.1, 40.5]% against 15.6 [14.7, 16.6]%). The Lean and Mathlib versions differ between the corpora and were not controlled;
- regularity side conditions (`ContDiff`, `Continuous`, `HasDerivAt`, …): 13.2 [12.6, 13.8]% of proof mass against 2.21 [1.30, 3.23]% on the first version's rule, a difference of +11.0 [+9.8, +12.0] points. This is not robust: 5.32 [5.00, 5.70] points of it are derivative-value facts; without them the excess is +5.74 [+4.62, +6.79]; on the inner label it is +5.64 [+5.48, +5.84]; and among theorems about integrals or Lp norms whose statements mention no derivative it is -0.01 [-3.15, +2.71]. It is a subject effect: ns proves that explicit functions are smooth and computes their derivatives.

These two come from different partitions of the same nodes and must not be added. Their measured overlap is at least 3.61 [3.47, 3.76]% of all ns nodes (instance arguments inside stand-alone regularity lemmas, which are 36.8% instance arguments).

## What "proof mass" and "hypothesis" mean here

- **Hypothesis**: a Prop-valued binder of the theorem statement (explicit hypotheses and Prop-valued instance arguments). Each gets one class from its outermost shape or head constant; the classes are listed in `bench/friction_families.json`.
- **Proof mass**: distinct nodes of the kernel proof term after opening binders. A node is charged to a side-condition class if it lies inside a subterm whose goal is of that class ("outer" label), and separately to the class of the nearest enclosing goal ("inner" label). Full definition in `README.md`.
- **Side-condition classes**: finiteness, positivity, measurability, integrability, regularity, support. Claim B maps to finiteness and to anything mentioning a cast function; C to support and to anything mentioning indicator / restrict / support / cutoff; D to measurability, integrability and regularity; A to positivity and to the constant patterns of section 3.
- Proof terms are what the kernel checks, not what the author typed. One `simp` call can produce thousands of nodes. Shares of proof mass are shares of elaborated work, not of source lines.

## Claim A: implied-constant tracking — supported as a pattern, moderate in size (revised)

What the chat said: explicit constants and `∃ C, 0 < C ∧ …` witnesses are threaded through estimates.

- **The `∃ C` pattern exists in the machine corpus and is almost absent from the human ones.** 2.45 [2.30, 2.61]% of ns theorems (946) conclude with a real-valued ∃ that carries a `0 < C` or `0 ≤ C` conjunct; Carleson has 1 such theorem and PFR none. Requiring in addition that `C` appears as an upper bound gives 2.01 [1.87, 2.15]%. It is concentrated in the Navier–Stokes half (3.33 [3.12, 3.54]%) and rare in Euler (0.41 [0.28, 0.53]%).
- **The constants are threaded.** 744 of the 946 are used by another project theorem and 585 by another `∃ C` theorem. A theorem whose proof uses an `∃ C` lemma concludes with `∃ C` itself in 69.8 [67.1, 72.7]% of cases, against 0.60 [0.52, 0.68]% otherwise. The longest chain of `∃ C` lemmas feeding `∃ C` lemmas is 13 lemmas long.
- **Direct `∃ C` theorems hold 5.09 [4.65, 5.53]% of proof mass.**
- **More are hidden inside the project's own predicates (revised).** The first version treated project-defined predicates as opaque. Opened at Expr level (`ROBUSTNESS.md` section 5), 114 of the 669 ns predicates contain a real `∃ C` with a sign conjunct; `DiagonalResidual.JetRate` is `∃ C, 0 ≤ C ∧ ∀ᶠ x, ‖iteratedFDeriv … f x‖ ≤ C * q x ^ r`, a home-made big-O, and `WeightedClasses.MemClass` pairs a `ContDiffOn` field with a `∀ m, ∃ C, 0 ≤ C ∧ …` field. A further 1,509 theorems conclude a predicate that hides such a constant within two levels of unfolding (3.89% of proof mass; 1,675 and 4.34% at any depth), and 3.20% of all ns hypotheses are such a predicate. Direct and hidden together are roughly 5.09% + 3.89% of proof mass. Carleson has no predicate of this kind. So the machine did what the chat describes and then wrapped it: it built its own substitutes for an implied-constant notation.
- **Positive parameters are common; the proof-mass comparison says little about constants (revised).** 27.8 [27.4, 28.3]% of ns theorems take a real parameter together with `0 < x`, against 13.9 [12.6, 15.3]% in Carleson; positivity is 26.7 [26.4, 27.0]% of ns hypotheses against 15.0 [13.8, 16.1]%. Most of these parameters are not constants in the chat's sense (the commonest binder names are `a`, `h`, `c`, `τ`, `T`, `δ`, `ε`); with a name-based filter for constants (`C*`, `K*`, `M*`, `c*`) the figure is 3.74 [3.54, 3.92]% against 1.53 [1.08, 2.02]%. Proof mass on positivity goals is 9.23 [9.00, 9.44]% in ns and 9.26 [8.54, 10.04]% in Carleson (difference -0.033 [-0.853, +0.703]); with the instance arguments of numerals (`NeZero`, `Nat.AtLeastTwo`) taken out it is 8.63 [8.43, 8.86]% and 8.78 [8.03, 9.52]% (difference -0.15 [-0.92, +0.62]). The review's sample also found output of `norm_num` / `linarith` and inequalities written as `0 ≤ b - a` inside this class, so the equality of the two figures is not evidence about implied constants either way.
- **Numeric literals do not separate the corpora** once the literal 2 is set aside: a real literal ≥ 3 occurs in 9.17 [8.89, 9.45]% of ns statements and 11.1 [9.9, 12.2]% of Carleson's. Any real literal ≥ 2: 47.1 [46.6, 47.7]% against 24.9 [23.4, 26.6]%.
- **Carleson handles constants a third way that the chat did not mention**: as named definitions (`C2_1_2 a`, `defaultD a`). 28.7 [27.0, 30.5]% of Carleson statements, and 51.6 [49.1, 54.2]% outside its `ToMathlib` folder, mention a project-defined real constant; ns 10.5 [10.1, 10.7]%.

Not tested: the chat's causal clause, that this happens because Mathlib lacks a multi-parameter "≲". The data show which of three styles each project used (∃-witness, parameter with positivity hypothesis, named definition), not what a "≲" would save.

## Claim B: the ℝ / ℝ≥0 / ℝ≥0∞ cast tax — not supported for the machine corpus

- The machine corpus barely uses ℝ≥0∞. Finiteness is 0.037 [0.025, 0.051]% of hypotheses; a cast function occurs in 0.19 [0.15, 0.22]% of hypotheses; 0.84 [0.75, 0.93]% of statements have a cast or a finiteness fact; finiteness goals take 0.074 [0.061, 0.087]% of proof mass; cast, ℝ≥0∞ and finiteness lemmas are 0.042 [0.038, 0.046]% of library constant uses.
- A generous upper bound, counting the whole proof of anything whose goal mentions a cast, is 1.61 [1.44, 1.80]%.
- In Carleson the tax is visible: 26.7 [25.0, 28.4]% of statements, 8.05 [7.21, 8.87]% of hypotheses, 1.76 [1.40, 2.22]% of proof mass on finiteness goals, 2.02 [1.88, 2.16]% of library constant uses. The upper bound is 43.0 [39.9, 46.2]%. The true cost in Carleson lies between about 2% and 43% and this export cannot narrow it: the region label is inherited from the statement, so a theorem stated with one `ENNReal.ofReal` puts its whole proof in the region.
- Restricting both corpora to theorems that mention measure theory does not close the gap: upper bound 6.86 [6.01, 7.69]% against 58.6 [54.4, 62.8]%.

So B describes a human analysis library built on ℝ≥0∞-valued integrals; it is not where the machine corpus is large.

## Claim C: local domain surgery — not supported

- Direct measures are small in both corpora. Support-class goals take 0.16 [0.13, 0.19]% of ns proof mass; indicator / restrict / support / cutoff lemmas and functions are 0.088 [0.083, 0.092]% of library constant uses in ns and 0.62 [0.55, 0.70]% in Carleson; 1.46 [1.38, 1.54]% of ns hypotheses and 3.02 [2.55, 3.55]% of Carleson's are about support or mention one of these operations.
- Statement-level prevalence: 8.48 [8.20, 8.76]% of ns theorems, 15.6 [14.2, 17.0]% of Carleson's.
- Upper bounds (whole proof of any goal mentioning one of these): 11.3 [10.9, 11.8]% in ns, 33.3 [30.1, 36.3]% in Carleson. As with B this is not a cost estimate.

## Claim D: side-condition leakage — partly supported, size not robust (revised)

- **D is present in the machine corpus; its size depends on the rule (revised).** On the first version's rule it is 15.4 [14.8, 15.9]% of proof mass and 14.0 [13.7, 14.2]% of hypotheses (22.4 [22.0, 22.8]% of theorems have at least one such hypothesis), against 9.15 [7.79, 10.69]% and 16.7 [15.4, 17.9]% in Carleson. The table under "Result" gives the four rule combinations: 5.65% to 15.4% in ns, 3.47% to 9.15% in Carleson. On three of the four the ns excess is between 0.98 and 3.41 points.
- **Its content in ns is smoothness and derivative computation.** Regularity is 13.2 [12.6, 13.8]% of mass on the outer label, of which 5.32 [5.00, 5.70] points are derivative-value facts (`HasDerivAt`), and 12.4 [12.2, 12.7]% of hypotheses. Measurability and integrability together are 2.17 [2.01, 2.32]% of mass and 1.53 [1.43, 1.64]% of hypotheses. In Carleson the proportions are reversed (measurability + integrability 6.93 [5.93, 8.00]% of mass, 16.0 [14.9, 17.2]% of hypotheses; regularity 2.21 [1.30, 3.23]%), and in PFR measurability alone is 39.7 [38.5, 40.8]% of hypotheses.
- **Most of the ns regularity mass is in lemmas whose own conclusion is a regularity fact**, not in side goals inside other proofs. Side conditions discharged inline take 12.1 [11.9, 12.4]% of ns mass and 13.0 [12.1, 13.8]% of Carleson's (difference -0.84 [-1.71, +0.03]); inline regularity is 3.38 [3.22, 3.54]%, inline measurability 0.39 [0.37, 0.41]%, inline integrability 0.49 [0.45, 0.53]%. Inside those stand-alone lemmas only 41.2% of nodes sit directly under a regularity goal; 32.9% are under equation goals and 36.8% are instance arguments, which is why the inner label gives about half the outer figure.
- **The small measurability / integrability share is a composition effect (revised).** The first version said a packet of measurability, integrability and finiteness "would address at most" 2.17 [2.01, 2.32]% + 0.074 [0.061, 0.087]% of ns proof mass. That is the corpus-wide share, and it is small because only 1,759 ns theorems (5.12% of proof nodes) state something about an integral or an Lp norm without a derivative. Inside that stratum ns spends 10.5 [9.4, 11.6]% of proof mass on measurability and integrability against 8.29 [7.14, 9.67]% in Carleson (difference +2.19 [+0.48, +3.82]); with finiteness added, 11.1 [10.0, 12.3]% against 10.2 [8.9, 11.8]% (+0.95 [-0.87, +2.64]); with instance synthesis taken out, 9.51 [8.51, 10.60]% against 10.0 [8.7, 11.4]%. So where the machine corpus does integration it pays about what the human corpus pays, roughly a tenth of proof mass. This is the claim-D cost the chat described, and it is not machine-specific.
- **The machine corpus built its own function-with-facts predicates (revised).** 34.9 [34.4, 35.4]% of ns statements mention a project-defined structure that carries data fields together with proof fields, and 40.6 [40.1, 41.1]% mention that or a project Prop-valued structure; Carleson 7.48 [6.43, 8.45]% and 13.3 [12.0, 14.6]%. The first version called these "specific to the construction, not reusable function-with-facts packets". That was wrong for a large part of them: 258 of the 669 project predicates contain a regularity, measurability or integrability fact, and 6.41% of all ns hypotheses are a project predicate containing a smoothness fact (2.84% one that pairs smoothness with a hidden constant: `MemClass`, `MeanClass`, `UniformClass`, `PolynomialJets`). They bundle smoothness with bounds, not measurability with integrability (0.37% of hypotheses). Theorems that conclude such a smoothness-carrying predicate hold 5.23% of proof mass, all counted as main-line proof above. The ns support library uses almost no project bundles (2.79 [2.09, 3.48]%).

## The unfolding claim — cannot tell (revised)

What the chat said: machine-written proofs unfold abstractions that human proofs keep. The first version's verdict was "not supported". The evidence supports less than that. Four of the five proxies below describe *statements*, and the claim is about *proofs*. On statements the machine corpus is as bundled as Carleson or more so. The one proof-level trace (P5, equation-lemma rewrites) cannot see the usual ways of unfolding. So the claim is neither supported nor refuted here.

| proxy | why it measures the claim | ns | Carleson | reading |
|---|---|---|---|---|
| P1 limits: statements using filters or asymptotics, against statements with an explicit `∀ ε > 0, … ∃ …, … < ε` | an unfolded limit is an ε-statement | 6.01 [5.79, 6.24]% bundled, 0.080 [0.052, 0.111]% explicit | 3.59 [2.88, 4.26]%, 0.34 [0.11, 0.56]% | no sign of unfolding |
| P2 maps: bundled morphism types against `IsLinearMap`-style predicates; share of term binders that are bare functions | an unfolded linear map is a function plus hypotheses | 26.0 [25.5, 26.4]% bundled, 0.00% predicate; 14.7 [14.5, 14.9]% bare functions | 3.07 [2.47, 3.74]%, 0.00%; 26.8 [26.3, 27.4]% | machine more bundled |
| P3 Lp: `eLpNorm` / `MemLp` / `Lp` against an integral of a power of a norm | an unfolded Lp norm is that integral | 4.38 [4.17, 4.59]% bundled, 0.036 [0.021, 0.057]% raw | 12.0 [10.8, 13.1]%, 0.67 [0.37, 1.01]% | both bundled; Carleson uses Lp more and raw integrals more |
| P4 certificates: output of `ring`, `norm_num`, `linarith`, `omega` in the proof | arithmetic done from scratch instead of by a named lemma | 14.1 [13.8, 14.4]% of library constant uses; linarith in 10.5 [10.2, 10.8]% of theorems | 9.95 [9.10, 10.83]%; 10.3 [9.2, 11.6]% | machine somewhat higher, driven by `ring` |
| P5 project vocabulary: rewriting with a definition's equation lemma; statements mentioning project bundles | the only proof-level trace of unfolding, and a partial one; and its opposite | equation lemma in 3.01 [2.85, 3.17]% of proofs; bundle in 40.6 [40.1, 41.1]% of statements | 9.31 [8.26, 10.47]%; 13.3 [12.0, 14.6]% | fewer equation-lemma rewrites, more bundles in statements; says nothing about `change` / `dsimp` / `simp [foo]` |

- P4 is the only proxy pointing the chat's way, and it is not stable under the subject controls: among theorems mentioning measure theory the certificate share is 5.81 [5.44, 6.19]% in ns against 7.47 [6.56, 8.46]% in Carleson. The large gap is between the support libraries (23.8 [22.4, 25.3]% against 3.53 [2.74, 4.35]%).
- P5's equation-lemma count sees `rw [foo]` and recursive unfolding. It does not see `simp [foo]` or `unfold foo` on a non-recursive definition, `dsimp`, `show` or `change`, which unfold by definitional equality and leave no trace in the term. Neither "the machine unfolds less" nor "the machine does not unfold more" is established.
- **A source-level cross-check points the chat's way.** This is a count of tactic names in the source files, which this census otherwise does not use, reproduced after the review; it is a pointer, not a measurement. Per `rw [` call, ns uses `change` 0.31 times against 0.02 in Carleson and `dsimp` 0.11 against 0.01. Per theorem, ns calls the side-condition automation `fun_prop` / `measurability` / `continuity` 0.010 times against 0.20, and `gcongr` 0.009 against 0.46. So the machine scripts restate goals by definitional unfolding far more per rewrite and discharge side conditions and monotonicity by hand far more often.
- Settling the claim needs the tactic-level record of each proof (Lean's InfoTrees): which definitions each step unfolds and which side goals each step closes by automation.

## Subject-matter control, and what cannot be concluded

The three corpora are about different mathematics, so a raw difference between ns and Carleson mixes author with subject. Four checks were made (section 5 below, and `ROBUSTNESS.md` section 3 for the last):

- **Loose content stratum.** Restricted to theorems whose statement mentions any `Mathlib.MeasureTheory` constant (6,309 in ns, 1,268 in Carleson), the regularity excess remains (13.2 [12.3, 14.1]% against 2.32 [0.94, 4.00]%), the cast gap remains, and the instance-argument excess grows (43.8 [43.1, 44.5]% against 15.9 [15.4, 16.5]%).
- **Tighter matched stratum (revised).** Statement mentions `eLpNorm` / `MemLp` / `Lp` or an integral, and no derivative or `ContDiff` constant (1,759 ns theorems, 440 in Carleson). The regularity excess vanishes (3.37 [2.61, 4.27]% against 3.37 [0.79, 6.48]%, difference -0.01 [-3.15, +2.71]), so the first version's statement that it "survives all three subject controls" was wrong: the loose stratum was not a control for it. Measurability + integrability is at parity or slightly higher in ns (+2.19 [+0.48, +3.82]). The cast gap survives (finiteness 0.66 [0.50, 0.85]% against 1.90 [1.46, 2.40]%; cast region 8.58 [6.95, 10.33]% against 68.3 [61.8, 74.2]%), and so does the instance excess (+23.7 [+22.1, +25.2]).
- **Support library against support library** (ns modules that import no project module, 2,010 theorems, against `Carleson.ToMathlib`, 1,189): regularity 12.1 [10.1, 14.2]% against 1.56 [0.51, 3.00]%; finiteness 0.16 [0.09, 0.24]% against 4.13 [2.82, 5.71]%.
- **Second human corpus.** PFR differs from Carleson by as much as ns does on many rows (measurability 39.7 [38.5, 40.8]% of hypotheses against 10.5 [9.4, 11.5]%; positivity 1.16 [0.81, 1.51]% against 15.0 [13.8, 16.1]%). Human-to-human variation across subjects is as large as the machine-to-human differences reported here.

What follows:

- The profile of the machine corpus is established: where its hypotheses and proof mass are, by class, with intervals.
- No difference between ns and Carleson can be attributed to machine authorship. There is one machine project and one human analysis project; they differ in subject (PDE blow-up construction with explicit smooth profiles against harmonic analysis on doubling metric measure spaces), in Lean and Mathlib version, and in conventions (Carleson states its estimates with ℝ≥0∞-valued integrals; ns stays in ℝ). The regularity excess is a subject effect by the matched comparison above. The instance-argument excess survives the subject and size controls but not a version control, which was not possible.
- The intervals cover sampling of theorems within a corpus only. They say nothing about how another machine-written or human-written project would look. Section 6 repeats the key rows resampling whole modules; the intervals widen, most for Carleson, and no verdict changes.
- The claims are about *bloat*, which implies a counterfactual: how long the proof would be with better abstractions. A census measures where mass is, not how much of it is avoidable.

## Limits of the measurements

- **Only theorems are covered by the tables below (revised).** Proof obligations of definitions, instances and structures (`foo._proof_N`) are outside `kind == theorem`. Exported separately (`ROBUSTNESS.md` section 6) they are 7.60% of all ns proof nodes (2.00% in Carleson, 0.88% in PFR). Their class mix is close to that of the theorems (claim D 13.2% against 15.4%; combined 15.2%), except that they are 53.4% instance arguments. No verdict changes when they are included.
- **Side-condition classes include instance synthesis.** `NeZero` and `Nat.AtLeastTwo` arguments of numerals count as positivity, `BorelSpace` instances as measurability, `IsFiniteMeasure` instances as finiteness. With Prop-valued instance arguments taken out (`ROBUSTNESS.md` section 2), ns measurability falls from 0.51% to 0.28% of proof mass and PFR finiteness from 1.22% to 0.53%; other rows move by under half a point.

- Classes are syntactic. `0 ≤ b - a` counts as positivity; a regularity fact hidden inside a project-defined predicate is `other` (14.6 [14.3, 14.9]% of ns hypotheses, 14.3 [14.0, 14.7]% have a project-defined head), so D is undercounted in ns by an unknown amount.
- The `∃ C` detector accepts any real-valued ∃ with a sign conjunct; a hash-ordered sample (section 8) contains a time budget `∃ T, 0 < T ∧ T ≤ Tmax ∧ …` that is not an implied constant. The stricter "used as an upper bound" row is the conservative figure.
- "Positive real parameter" includes viscosities, times, radii and ε. The name filter is a heuristic on binder names.
- "Named real constant" means a project definition with result type ℝ, ℝ≥0 or ℝ≥0∞ whose arguments are all ℕ or ℤ; it misses constants that take a real argument and the wider row includes ordinary real functions.
- The support-library split for ns is by import graph (modules importing no project module); the repository has no folder that marks a support library, and Navier–Stokes and Euler do not import each other.
- Proof-side attribution was verified by the export step only through its invariants and six small proofs. The new detectors added for this census (ε-shape, integral of a power, `∃ C` used as a bound, literals) were checked by reading hash-ordered samples of their hits against the stored statements, not exhaustively; one false-positive pattern in the ε-shape detector was found that way and fixed.

---

# Tables

Generated by `bench/friction_census.py` (B = 1000 bootstrap resamples of theorems, seed 20261110). Cells are `value [2.5%, 97.5%]`. Every share is a ratio of sums over theorems, so large theorems weigh more in mass shares. The `ns − Carleson` column is the difference with its own interval (independent resamples); an interval that excludes 0 is a difference not explained by theorem sampling.

## Groups

| group | theorems | modules | rule |
|---|---|---|---|
| ns | 38,601 | 2,614 | all exported theorems |
| ns/NavierStokes | 26,378 | 761 | module root `NavierStokes`, not support |
| ns/Euler | 10,213 | 1,781 | module root `Euler`, not support |
| ns/support | 2,010 | 72 | modules that import no project module (import graph read from the environment header) |
| ns, MT | 6,309 | 1,253 | statement mentions a constant declared under `Mathlib.MeasureTheory.` |
| ns, D-hyp | 8,650 | 1,369 | theorem has at least one measurability / integrability / regularity hypothesis |
| carleson | 2,675 | 121 | all |
| carleson/main | 1,486 | 58 | not under `Carleson.ToMathlib` |
| carleson/ToMathlib | 1,189 | 63 | under `Carleson.ToMathlib` |
| carleson, MT | 1,268 | 106 | same |
| carleson, D-hyp | 605 | 86 | same |
| pfr | 978 | 68 | all |

## 1. Statement hypotheses

Denominator for the class shares: Prop-valued binders of the statement telescope (explicit hypotheses plus Prop-valued instance arguments).

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| Prop-valued binders per theorem (mean) | 2.73 [2.69, 2.76] | 1.79 [1.72, 1.88] | 0.93 [0.84, 1.03] | 5.13 [4.88, 5.37] |
| explicit hypotheses per theorem (mean) | 2.51 [2.48, 2.55] | 1.60 [1.52, 1.68] | 0.92 [0.83, 1.01] | 2.01 [1.89, 2.13] |
| all binders per theorem (mean) | 9.03 [8.96, 9.10] | 10.0 [9.8, 10.3] | -1.00 [-1.25, -0.76] | 13.9 [13.5, 14.4] |
| side-condition hypotheses per theorem (mean) | 1.12 [1.10, 1.14] | 0.67 [0.63, 0.71] | 0.45 [0.41, 0.50] | 2.87 [2.72, 3.03] |
| % of Prop binders: finiteness (side) | 0.037 [0.025, 0.051] | 5.52 [4.81, 6.25] | -5.49 [-6.22, -4.77] | 15.2 [14.3, 16.0] |
| % of Prop binders: positivity (side) | 26.7 [26.4, 27.0] | 15.0 [13.8, 16.1] | 11.7 [10.5, 12.9] | 1.16 [0.81, 1.51] |
| % of Prop binders: measurability (side) | 0.61 [0.55, 0.67] | 10.5 [9.4, 11.5] | -9.88 [-10.93, -8.80] | 39.7 [38.5, 40.8] |
| % of Prop binders: integrability (side) | 0.93 [0.85, 1.01] | 5.56 [4.86, 6.34] | -4.64 [-5.41, -3.92] | 0.00 [0.00, 0.00] |
| % of Prop binders: regularity (side) | 12.4 [12.2, 12.7] | 0.60 [0.40, 0.85] | 11.8 [11.5, 12.2] | 0.060 [0.000, 0.161] |
| % of Prop binders: support (side) | 0.36 [0.33, 0.41] | 0.021 [0.000, 0.065] | 0.34 [0.29, 0.39] | 0.00 [0.00, 0.00] |
| % of Prop binders: order | 20.7 [20.4, 21.1] | 17.5 [16.3, 18.9] | 3.21 [1.88, 4.50] | 1.14 [0.85, 1.47] |
| % of Prop binders: eq | 7.50 [7.30, 7.71] | 8.40 [7.42, 9.39] | -0.90 [-1.94, 0.07] | 1.99 [1.57, 2.48] |
| % of Prop binders: logic | 0.64 [0.58, 0.69] | 1.19 [0.87, 1.53] | -0.55 [-0.89, -0.22] | 1.20 [0.85, 1.59] |
| % of Prop binders: mem | 7.28 [7.11, 7.47] | 18.1 [16.8, 19.6] | -10.8 [-12.3, -9.5] | 19.6 [18.6, 20.6] |
| % of Prop binders: limit | 1.30 [1.21, 1.39] | 1.52 [1.12, 1.99] | -0.22 [-0.72, 0.20] | 0.44 [0.26, 0.62] |
| % of Prop binders: topo | 2.69 [2.59, 2.80] | 1.04 [0.75, 1.36] | 1.65 [1.32, 1.97] | 0.00 [0.00, 0.00] |
| % of Prop binders: prob | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 6.08 [5.30, 6.95] |
| % of Prop binders: cert | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| % of Prop binders: tc | 4.19 [4.07, 4.33] | 5.98 [5.15, 6.84] | -1.79 [-2.63, -0.95] | 9.35 [8.47, 10.23] |
| % of Prop binders: other | 14.6 [14.3, 14.9] | 9.05 [8.05, 10.04] | 5.56 [4.55, 6.60] | 4.11 [3.60, 4.72] |
| % of Prop binders: any side-condition class | 41.1 [40.7, 41.4] | 37.2 [35.6, 38.6] | 3.87 [2.39, 5.50] | 56.1 [54.9, 57.1] |
| claim A: % positivity | 26.7 [26.4, 27.0] | 15.0 [13.8, 16.1] | 11.7 [10.5, 12.9] | 1.16 [0.81, 1.51] |
| claim B: % finiteness class or mentioning a cast | 0.22 [0.19, 0.26] | 8.05 [7.21, 8.87] | -7.82 [-8.64, -6.98] | 15.2 [14.4, 16.0] |
| ... % mentioning a cast function | 0.19 [0.15, 0.22] | 2.52 [1.97, 3.09] | -2.33 [-2.91, -1.78] | 0.020 [0.000, 0.061] |
| ... % of shape `x ≠ ⊤` / `x < ⊤` | 0.015 [0.008, 0.023] | 3.61 [3.05, 4.19] | -3.59 [-4.18, -3.04] | 0.00 [0.00, 0.00] |
| claim C: % support class or mentioning indicator/restrict/support/cutoff | 1.46 [1.38, 1.54] | 3.02 [2.55, 3.55] | -1.56 [-2.12, -1.09] | 0.00 [0.00, 0.00] |
| claim D: % measurability + integrability + regularity | 14.0 [13.7, 14.2] | 16.7 [15.4, 17.9] | -2.69 [-3.97, -1.49] | 39.7 [38.6, 40.9] |
| ... % measurability + integrability | 1.53 [1.43, 1.64] | 16.0 [14.9, 17.2] | -14.5 [-15.7, -13.3] | 39.7 [38.5, 40.8] |
| % of Prop binders whose head is a project-defined predicate | 14.3 [14.0, 14.7] | 11.4 [10.4, 12.5] | 2.90 [1.78, 4.05] | 12.4 [11.5, 13.3] |
| % of theorems with at least one claim-D hypothesis | 22.4 [22.0, 22.8] | 22.6 [21.1, 24.1] | -0.21 [-1.74, 1.36] | 71.7 [68.9, 74.4] |
| % of theorems with at least one side-condition hypothesis | 53.6 [53.1, 54.1] | 38.4 [36.6, 40.0] | 15.3 [13.5, 17.1] | 77.7 [75.2, 80.5] |
| % of theorems whose statement has a cast or a finiteness-class fact | 0.84 [0.75, 0.93] | 26.7 [25.0, 28.4] | -25.8 [-27.5, -24.2] | 51.4 [48.4, 54.6] |
| % of theorems whose statement has domain surgery | 8.48 [8.20, 8.76] | 15.6 [14.2, 17.0] | -7.14 [-8.61, -5.65] | 0.31 [0.00, 0.72] |
| % of theorems whose conclusion is a side-condition class | 18.3 [17.9, 18.6] | 16.5 [15.1, 17.8] | 1.79 [0.37, 3.19] | 4.91 [3.68, 6.34] |

| | ns (machine) | Carleson (human) | PFR (human) |
|---|---|---|---|
| Prop-valued binders per theorem (median) | 2 [2, 2] | 1 [1, 1] | 4 [4, 5] |
| statement size, tree nodes (median) | 477 [469, 487] | 271 [255, 291] | 220 [203, 239] |
| proof size, distinct subterms (median) | 652 [640, 661] | 595 [551, 627] | 664 [597, 750] |

By area:

| | ns: Navier–Stokes | ns: Euler | ns: support | Carleson: main | Carleson: ToMathlib |
|---|---|---|---|---|---|
| Prop-valued binders per theorem (mean) | 2.44 [2.40, 2.47] | 3.52 [3.43, 3.60] | 2.55 [2.41, 2.69] | 1.49 [1.40, 1.59] | 2.17 [2.02, 2.32] |
| explicit hypotheses per theorem (mean) | 2.40 [2.36, 2.43] | 2.86 [2.78, 2.93] | 2.33 [2.20, 2.47] | 1.41 [1.32, 1.49] | 1.84 [1.70, 1.98] |
| all binders per theorem (mean) | 8.50 [8.42, 8.58] | 10.7 [10.5, 10.9] | 7.43 [7.18, 7.69] | 11.0 [10.7, 11.3] | 8.81 [8.49, 9.15] |
| side-condition hypotheses per theorem (mean) | 0.92 [0.90, 0.93] | 1.60 [1.56, 1.63] | 1.35 [1.27, 1.43] | 0.41 [0.37, 0.45] | 0.99 [0.91, 1.06] |
| % of Prop binders: finiteness (side) | 0.011 [0.003, 0.019] | 0.033 [0.014, 0.056] | 0.39 [0.21, 0.62] | 0.90 [0.50, 1.37] | 9.50 [8.31, 10.76] |
| % of Prop binders: positivity (side) | 23.2 [22.8, 23.6] | 32.9 [32.4, 33.4] | 26.9 [25.4, 28.1] | 10.5 [9.0, 11.9] | 18.9 [17.2, 20.5] |
| % of Prop binders: measurability (side) | 0.23 [0.19, 0.28] | 1.14 [1.01, 1.29] | 1.52 [1.19, 1.98] | 7.44 [6.10, 8.76] | 13.1 [11.5, 14.7] |
| % of Prop binders: integrability (side) | 0.76 [0.67, 0.85] | 0.92 [0.79, 1.04] | 3.01 [2.46, 3.60] | 7.62 [6.45, 8.84] | 3.80 [3.04, 4.66] |
| % of Prop binders: regularity (side) | 13.1 [12.7, 13.4] | 10.2 [9.8, 10.6] | 20.3 [18.9, 21.8] | 0.95 [0.57, 1.34] | 0.31 [0.12, 0.59] |
| % of Prop binders: support (side) | 0.39 [0.34, 0.44] | 0.26 [0.21, 0.32] | 0.80 [0.55, 1.07] | 0.00 [0.00, 0.00] | 0.039 [0.000, 0.124] |
| % of Prop binders: order | 17.6 [17.2, 18.0] | 25.7 [25.0, 26.3] | 25.6 [23.9, 27.3] | 22.9 [21.1, 24.6] | 12.9 [11.3, 14.6] |
| % of Prop binders: eq | 6.12 [5.88, 6.35] | 10.0 [9.6, 10.4] | 6.89 [6.10, 7.77] | 4.51 [3.70, 5.42] | 11.7 [10.2, 13.4] |
| % of Prop binders: logic | 0.70 [0.63, 0.78] | 0.48 [0.40, 0.56] | 0.92 [0.64, 1.22] | 1.31 [0.85, 1.85] | 1.09 [0.66, 1.57] |
| % of Prop binders: mem | 10.1 [9.9, 10.4] | 2.60 [2.43, 2.76] | 4.36 [3.75, 4.94] | 28.4 [26.1, 30.8] | 9.26 [8.07, 10.55] |
| % of Prop binders: limit | 1.37 [1.25, 1.48] | 1.10 [0.96, 1.24] | 1.84 [1.39, 2.32] | 0.81 [0.36, 1.37] | 2.13 [1.46, 2.91] |
| % of Prop binders: topo | 3.75 [3.60, 3.90] | 0.91 [0.81, 1.02] | 1.91 [1.51, 2.36] | 0.90 [0.50, 1.36] | 1.16 [0.76, 1.66] |
| % of Prop binders: prob | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| % of Prop binders: cert | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| % of Prop binders: tc | 1.49 [1.39, 1.58] | 9.23 [8.92, 9.57] | 2.87 [2.40, 3.36] | 4.15 [3.31, 5.05] | 7.56 [6.11, 8.96] |
| % of Prop binders: other | 21.2 [20.7, 21.6] | 4.55 [4.27, 4.83] | 2.73 [2.24, 3.31] | 9.69 [8.33, 10.97] | 8.49 [7.01, 9.89] |
| % of Prop binders: any side-condition class | 37.7 [37.2, 38.1] | 45.4 [44.8, 46.1] | 52.9 [51.3, 54.5] | 27.4 [25.5, 29.4] | 45.6 [43.5, 47.7] |
| claim A: % positivity | 23.2 [22.8, 23.6] | 32.9 [32.4, 33.4] | 26.9 [25.4, 28.1] | 10.5 [9.0, 11.9] | 18.9 [17.2, 20.5] |
| claim B: % finiteness class or mentioning a cast | 0.036 [0.015, 0.062] | 0.30 [0.23, 0.37] | 2.07 [1.58, 2.65] | 3.70 [2.83, 4.51] | 11.8 [10.4, 13.1] |
| ... % mentioning a cast function | 0.025 [0.005, 0.050] | 0.26 [0.20, 0.33] | 1.68 [1.23, 2.22] | 2.80 [2.04, 3.59] | 2.29 [1.49, 3.13] |
| ... % of shape `x ≠ ⊤` / `x < ⊤` | 0.005 [0.000, 0.011] | 0.011 [0.003, 0.022] | 0.18 [0.08, 0.30] | 0.45 [0.18, 0.73] | 6.32 [5.33, 7.29] |
| claim C: % support class or mentioning indicator/restrict/support/cutoff | 1.28 [1.19, 1.39] | 1.70 [1.55, 1.85] | 2.03 [1.63, 2.47] | 5.00 [4.11, 5.89] | 1.32 [0.90, 1.77] |
| claim D: % measurability + integrability + regularity | 14.1 [13.7, 14.4] | 12.3 [11.8, 12.7] | 24.8 [23.4, 26.4] | 16.0 [14.5, 17.5] | 17.2 [15.5, 19.0] |
| ... % measurability + integrability | 0.99 [0.88, 1.11] | 2.07 [1.89, 2.25] | 4.53 [3.85, 5.28] | 15.1 [13.4, 16.6] | 16.9 [15.1, 18.7] |
| % of Prop binders whose head is a project-defined predicate | 20.9 [20.4, 21.4] | 4.34 [4.06, 4.62] | 2.13 [1.67, 2.64] | 14.7 [13.0, 16.5] | 8.64 [7.54, 9.87] |
| % of theorems with at least one claim-D hypothesis | 21.2 [20.7, 21.7] | 23.5 [22.7, 24.3] | 33.1 [31.1, 35.4] | 18.1 [16.2, 20.1] | 28.3 [25.6, 30.9] |
| % of theorems with at least one side-condition hypothesis | 46.7 [46.1, 47.3] | 69.8 [69.0, 70.7] | 62.3 [60.1, 64.2] | 28.9 [26.6, 31.2] | 50.2 [47.2, 52.9] |
| % of theorems whose statement has a cast or a finiteness-class fact | 0.12 [0.08, 0.16] | 2.00 [1.73, 2.28] | 4.43 [3.63, 5.32] | 18.1 [16.1, 20.0] | 37.3 [34.7, 40.2] |
| % of theorems whose statement has domain surgery | 7.39 [7.07, 7.70] | 10.1 [9.5, 10.7] | 14.6 [13.0, 16.2] | 16.0 [14.1, 17.9] | 15.1 [13.1, 17.3] |
| % of theorems whose conclusion is a side-condition class | 17.7 [17.2, 18.1] | 18.8 [18.1, 19.6] | 23.3 [21.3, 25.1] | 14.3 [12.4, 16.0] | 19.3 [16.9, 21.4] |

## 2. Proof mass

Share (%) of distinct proof-term nodes (`mass.nodes`, definition in `README.md`). "Inside a side-condition proof" uses the outermost-attribution label; "nearest goal" uses the inner label; they are two marginals of the same nodes and are not additive with each other.

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| inside a side-condition proof (any class) | 24.8 [24.3, 25.4] | 20.2 [18.7, 21.8] | 4.63 [3.07, 6.18] | 13.1 [12.0, 14.4] |
| ... finiteness | 0.074 [0.061, 0.087] | 1.76 [1.40, 2.22] | -1.69 [-2.15, -1.33] | 1.22 [0.99, 1.48] |
| ... positivity | 9.23 [9.00, 9.44] | 9.26 [8.54, 10.04] | -0.033 [-0.853, 0.703] | 6.27 [5.42, 7.18] |
| ... measurability | 0.51 [0.47, 0.55] | 3.92 [3.10, 4.80] | -3.41 [-4.31, -2.60] | 4.87 [4.10, 5.74] |
| ... integrability | 1.66 [1.51, 1.81] | 3.01 [2.42, 3.71] | -1.35 [-2.05, -0.74] | 0.19 [0.12, 0.28] |
| ... regularity | 13.2 [12.6, 13.8] | 2.21 [1.30, 3.23] | 11.0 [9.8, 12.0] | 0.53 [0.23, 0.91] |
| ... support | 0.16 [0.13, 0.19] | 0.021 [0.004, 0.041] | 0.14 [0.11, 0.18] | 0.00 [0.00, 0.00] |
| claim B: finiteness side-conditions | 0.074 [0.061, 0.087] | 1.76 [1.40, 2.22] | -1.69 [-2.15, -1.33] | 1.22 [0.99, 1.48] |
| claim B upper bound: inside a proof whose type mentions a cast | 1.61 [1.44, 1.80] | 43.0 [39.9, 46.2] | -41.4 [-44.6, -38.3] | 2.01 [1.18, 2.96] |
| claim C: support side-conditions | 0.16 [0.13, 0.19] | 0.021 [0.004, 0.041] | 0.14 [0.11, 0.18] | 0.00 [0.00, 0.00] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 11.3 [10.9, 11.8] | 33.3 [30.1, 36.3] | -22.0 [-24.9, -18.7] | 2.52 [1.54, 3.78] |
| claim D: measurability + integrability + regularity | 15.4 [14.8, 15.9] | 9.15 [7.79, 10.69] | 6.21 [4.65, 7.77] | 5.59 [4.77, 6.62] |
| ... measurability + integrability only | 2.17 [2.01, 2.32] | 6.93 [5.93, 8.00] | -4.76 [-5.80, -3.76] | 5.06 [4.30, 5.93] |
| in theorems whose own conclusion is a side condition | 12.7 [12.1, 13.3] | 7.23 [5.83, 8.82] | 5.47 [3.82, 7.00] | 1.50 [0.96, 2.20] |
| side conditions discharged inline (other theorems) | 12.1 [11.9, 12.4] | 13.0 [12.1, 13.8] | -0.84 [-1.71, 0.03] | 11.6 [10.6, 12.7] |
| ... inline finiteness | 0.066 [0.054, 0.078] | 1.35 [1.03, 1.74] | -1.28 [-1.67, -0.97] | 1.22 [0.99, 1.47] |
| ... inline positivity | 7.77 [7.58, 7.97] | 8.36 [7.71, 9.04] | -0.59 [-1.32, 0.11] | 5.38 [4.61, 6.15] |
| ... inline measurability | 0.39 [0.37, 0.41] | 1.84 [1.57, 2.16] | -1.45 [-1.77, -1.19] | 4.76 [4.00, 5.61] |
| ... inline integrability | 0.49 [0.45, 0.53] | 1.16 [0.87, 1.46] | -0.67 [-0.97, -0.37] | 0.18 [0.12, 0.27] |
| ... inline regularity | 3.38 [3.22, 3.54] | 0.25 [0.10, 0.47] | 3.13 [2.87, 3.35] | 0.046 [0.013, 0.092] |
| ... inline support | 0.027 [0.022, 0.033] | 0.003 [0.000, 0.008] | 0.024 [0.016, 0.032] | 0.00 [0.00, 0.00] |
| proof mass of theorems concluding `∃ C, 0 < C ∧ …` (claim A) | 5.09 [4.65, 5.53] | 0.013 [0.000, 0.040] | 5.07 [4.62, 5.50] | 0.00 [0.00, 0.00] |
| proof mass of theorems taking a positive real parameter (claim A, upper bound) | 35.5 [34.7, 36.3] | 14.5 [12.3, 16.8] | 21.0 [18.6, 23.3] | 5.87 [2.16, 10.24] |
| nearest goal is an equation | 53.5 [53.1, 53.9] | 58.7 [57.9, 59.6] | -5.21 [-6.21, -4.28] | 68.5 [66.9, 70.1] |
| nearest goal is an inequality (not 0-positivity) | 8.69 [8.52, 8.85] | 13.5 [13.0, 13.9] | -4.79 [-5.29, -4.28] | 7.75 [7.09, 8.42] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 62.2 [61.9, 62.6] | 72.2 [71.5, 72.9] | -10.0 [-10.8, -9.2] | 76.3 [74.5, 78.0] |
| nearest goal is positivity | 4.17 [4.10, 4.24] | 3.49 [3.31, 3.68] | 0.67 [0.48, 0.87] | 2.01 [1.77, 2.26] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 5.91 [5.79, 6.04] | 4.57 [4.22, 4.94] | 1.34 [0.95, 1.71] | 4.29 [3.61, 4.87] |
| nearest goal is a Prop-valued type-class fact | 7.62 [7.47, 7.76] | 2.80 [2.68, 2.93] | 4.82 [4.62, 5.00] | 1.34 [1.18, 1.49] |
| nearest goal is unclassified (mostly project predicates) | 3.91 [3.78, 4.03] | 1.12 [0.97, 1.28] | 2.79 [2.59, 2.98] | 0.78 [0.59, 1.02] |
| nearest goal is logic | 5.10 [4.93, 5.29] | 5.91 [5.54, 6.29] | -0.81 [-1.23, -0.41] | 5.31 [4.60, 6.05] |
| nearest goal is membership / inclusion | 2.47 [2.39, 2.54] | 4.79 [4.43, 5.16] | -2.32 [-2.70, -1.95] | 2.95 [2.49, 3.58] |
| nodes inside an instance argument | 27.1 [26.8, 27.4] | 16.6 [16.1, 17.1] | 10.5 [9.9, 11.1] | 9.25 [8.78, 9.70] |
| nodes inside a non-proof (term) argument | 31.3 [31.1, 31.5] | 36.7 [35.9, 37.4] | -5.42 [-6.23, -4.63] | 42.6 [40.3, 45.3] |
| nodes on the proof spine | 41.6 [41.3, 42.0] | 46.7 [45.7, 47.8] | -5.11 [-6.19, -4.01] | 48.2 [45.3, 50.5] |
| statement DAG nodes as % of statement + proof DAG nodes | 19.8 [19.5, 20.0] | 14.1 [13.5, 14.7] | 5.67 [4.99, 6.28] | 7.22 [6.38, 8.10] |
| statement DAG nodes per theorem (mean) | 310.1 [305.9, 314.2] | 253.0 [242.1, 263.8] | 57.1 [44.7, 68.8] | 166.4 [159.4, 173.8] |
| proof DAG nodes per theorem (mean, `proofSize`) | 1259.7 [1242.0, 1281.1] | 1542.6 [1449.0, 1633.5] | -283.0 [-377.6, -192.4] | 2137.9 [1844.7, 2480.2] |
| distinct proof nodes per theorem (mean) | 1020.5 [1007.7, 1035.6] | 1281.2 [1207.9, 1357.0] | -260.7 [-336.0, -185.9] | 1677.0 [1453.2, 1932.7] |

By area:

| | ns: Navier–Stokes | ns: Euler | ns: support | Carleson: main | Carleson: ToMathlib |
|---|---|---|---|---|---|
| inside a side-condition proof (any class) | 24.0 [23.2, 24.8] | 25.5 [24.8, 26.3] | 28.7 [26.6, 30.9] | 19.7 [18.0, 21.6] | 21.9 [19.7, 24.4] |
| ... finiteness | 0.057 [0.042, 0.073] | 0.086 [0.063, 0.110] | 0.16 [0.09, 0.24] | 1.09 [0.86, 1.34] | 4.13 [2.82, 5.71] |
| ... positivity | 8.80 [8.54, 9.13] | 9.44 [9.09, 9.81] | 11.7 [10.8, 12.7] | 9.80 [8.86, 10.73] | 7.36 [6.33, 8.50] |
| ... measurability | 0.28 [0.24, 0.31] | 0.97 [0.88, 1.06] | 0.58 [0.40, 0.83] | 3.32 [2.41, 4.54] | 6.05 [5.13, 7.09] |
| ... integrability | 1.57 [1.41, 1.75] | 1.25 [1.04, 1.48] | 3.88 [2.89, 5.07] | 3.08 [2.33, 3.99] | 2.77 [1.95, 3.80] |
| ... regularity | 13.1 [12.4, 14.0] | 13.6 [12.8, 14.3] | 12.1 [10.1, 14.2] | 2.40 [1.35, 3.62] | 1.56 [0.51, 3.00] |
| ... support | 0.11 [0.09, 0.14] | 0.22 [0.15, 0.29] | 0.30 [0.16, 0.46] | 0.009 [0.000, 0.024] | 0.062 [0.000, 0.160] |
| claim B: finiteness side-conditions | 0.057 [0.042, 0.073] | 0.086 [0.063, 0.110] | 0.16 [0.09, 0.24] | 1.09 [0.86, 1.34] | 4.13 [2.82, 5.71] |
| claim B upper bound: inside a proof whose type mentions a cast | 0.30 [0.23, 0.38] | 3.63 [3.08, 4.22] | 4.18 [3.28, 5.18] | 40.6 [36.5, 44.5] | 51.2 [46.2, 56.1] |
| claim C: support side-conditions | 0.11 [0.09, 0.14] | 0.22 [0.15, 0.29] | 0.30 [0.16, 0.46] | 0.009 [0.000, 0.024] | 0.062 [0.000, 0.160] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 10.3 [9.7, 10.9] | 14.4 [13.4, 15.6] | 7.79 [6.51, 9.24] | 34.4 [30.6, 38.3] | 29.8 [25.2, 34.8] |
| claim D: measurability + integrability + regularity | 15.0 [14.2, 15.9] | 15.8 [15.0, 16.6] | 16.5 [14.4, 18.8] | 8.80 [7.25, 10.57] | 10.4 [8.7, 12.4] |
| ... measurability + integrability only | 1.85 [1.69, 2.03] | 2.22 [2.00, 2.47] | 4.46 [3.45, 5.67] | 6.40 [5.21, 7.99] | 8.82 [7.53, 10.29] |
| in theorems whose own conclusion is a side condition | 12.4 [11.5, 13.3] | 13.0 [12.3, 13.8] | 14.0 [11.9, 16.0] | 6.82 [5.23, 8.74] | 8.68 [6.85, 10.63] |
| side conditions discharged inline (other theorems) | 11.6 [11.3, 11.9] | 12.5 [12.1, 12.9] | 14.8 [13.6, 16.0] | 12.9 [11.9, 13.9] | 13.3 [11.6, 15.1] |
| ... inline finiteness | 0.052 [0.038, 0.067] | 0.073 [0.054, 0.095] | 0.15 [0.08, 0.23] | 0.89 [0.71, 1.08] | 2.98 [1.81, 4.58] |
| ... inline positivity | 7.34 [7.10, 7.59] | 8.09 [7.75, 8.42] | 9.88 [9.10, 10.69] | 8.99 [8.20, 9.80] | 6.13 [5.19, 7.13] |
| ... inline measurability | 0.21 [0.19, 0.24] | 0.79 [0.74, 0.85] | 0.27 [0.20, 0.36] | 1.42 [1.12, 1.77] | 3.35 [2.76, 3.95] |
| ... inline integrability | 0.49 [0.44, 0.55] | 0.46 [0.39, 0.53] | 0.58 [0.44, 0.76] | 1.35 [0.99, 1.76] | 0.49 [0.26, 0.80] |
| ... inline regularity | 3.48 [3.31, 3.65] | 3.05 [2.81, 3.31] | 3.83 [2.84, 5.04] | 0.24 [0.08, 0.49] | 0.30 [0.06, 0.61] |
| ... inline support | 0.021 [0.016, 0.027] | 0.037 [0.025, 0.051] | 0.033 [0.014, 0.055] | 0.003 [0.000, 0.011] | 0.00 [0.00, 0.00] |
| proof mass of theorems concluding `∃ C, 0 < C ∧ …` (claim A) | 7.26 [6.61, 7.92] | 1.54 [0.90, 2.18] | 1.60 [0.90, 2.51] | 0.016 [0.000, 0.050] | 0.00 [0.00, 0.00] |
| proof mass of theorems taking a positive real parameter (claim A, upper bound) | 26.9 [25.9, 27.8] | 53.7 [52.4, 55.1] | 34.0 [30.5, 37.5] | 10.9 [8.4, 13.5] | 27.2 [22.4, 32.5] |
| nearest goal is an equation | 56.2 [55.7, 56.7] | 45.9 [45.2, 46.5] | 61.3 [60.1, 62.4] | 57.8 [56.8, 58.8] | 62.0 [60.3, 63.6] |
| nearest goal is an inequality (not 0-positivity) | 6.81 [6.64, 6.98] | 12.3 [12.0, 12.7] | 9.51 [8.95, 10.09] | 14.6 [14.1, 15.2] | 9.51 [8.61, 10.48] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 63.0 [62.6, 63.5] | 58.2 [57.5, 58.8] | 70.8 [69.8, 71.8] | 72.4 [71.5, 73.2] | 71.5 [70.0, 72.9] |
| nearest goal is positivity | 3.99 [3.91, 4.08] | 4.44 [4.31, 4.59] | 4.54 [4.28, 4.77] | 3.63 [3.43, 3.83] | 3.00 [2.66, 3.40] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 6.65 [6.49, 6.81] | 3.61 [3.43, 3.78] | 8.80 [8.30, 9.30] | 5.49 [5.03, 5.93] | 1.29 [0.99, 1.58] |
| nearest goal is a Prop-valued type-class fact | 4.27 [4.16, 4.39] | 15.1 [14.8, 15.5] | 5.49 [5.13, 5.90] | 2.75 [2.62, 2.90] | 2.97 [2.66, 3.27] |
| nearest goal is unclassified (mostly project predicates) | 5.23 [5.05, 5.42] | 2.10 [1.94, 2.29] | 0.47 [0.36, 0.59] | 0.70 [0.58, 0.84] | 2.59 [2.10, 3.09] |
| nearest goal is logic | 5.84 [5.64, 6.06] | 4.25 [3.84, 4.66] | 2.61 [2.35, 2.88] | 5.74 [5.31, 6.25] | 6.49 [5.81, 7.17] |
| nearest goal is membership / inclusion | 2.57 [2.50, 2.64] | 2.61 [2.45, 2.77] | 1.19 [1.03, 1.36] | 5.01 [4.56, 5.49] | 4.03 [3.47, 4.68] |
| nodes inside an instance argument | 22.0 [21.7, 22.3] | 40.0 [39.4, 40.7] | 18.5 [17.5, 19.4] | 17.3 [16.8, 17.8] | 14.0 [13.4, 14.7] |
| nodes inside a non-proof (term) argument | 32.7 [32.4, 33.0] | 30.0 [29.6, 30.3] | 25.3 [24.7, 25.9] | 35.5 [34.6, 36.5] | 40.8 [39.9, 41.7] |
| nodes on the proof spine | 45.3 [44.9, 45.7] | 30.0 [29.3, 30.8] | 56.2 [54.8, 57.6] | 47.2 [45.9, 48.5] | 45.2 [44.0, 46.2] |
| statement DAG nodes as % of statement + proof DAG nodes | 15.3 [15.0, 15.5] | 27.7 [27.2, 28.2] | 11.9 [11.2, 12.6] | 13.9 [13.3, 14.6] | 14.7 [13.7, 15.8] |
| statement DAG nodes per theorem (mean) | 193.7 [191.5, 195.8] | 623.7 [611.3, 635.9] | 245.2 [234.9, 256.9] | 358.9 [342.4, 376.7] | 120.6 [113.8, 128.3] |
| proof DAG nodes per theorem (mean, `proofSize`) | 1073.8 [1052.6, 1093.5] | 1628.9 [1579.1, 1673.5] | 1823.0 [1708.5, 1952.2] | 2216.5 [2088.5, 2344.9] | 700.4 [639.2, 768.2] |
| distinct proof nodes per theorem (mean) | 924.7 [907.9, 940.4] | 1158.2 [1130.8, 1181.3] | 1578.7 [1488.1, 1685.3] | 1797.9 [1685.8, 1913.0] | 635.5 [581.7, 692.4] |

### Constants used in proofs

Share (%) of non-project constant uses (distinct applications). The per-tool rows use the declaring module of each constant.

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 14.1 [13.8, 14.4] | 9.95 [9.10, 10.83] | 4.13 [3.22, 5.10] | 10.5 [9.0, 12.0] |
| ... ring | 8.36 [8.15, 8.62] | 5.35 [4.83, 5.90] | 3.01 [2.44, 3.60] | 6.62 [5.42, 7.81] |
| ... normnum | 3.20 [3.11, 3.28] | 2.80 [2.56, 3.06] | 0.39 [0.13, 0.66] | 1.94 [1.59, 2.27] |
| ... linarith | 0.46 [0.44, 0.48] | 0.36 [0.31, 0.42] | 0.097 [0.038, 0.150] | 0.29 [0.24, 0.35] |
| ... fieldsimp | 1.19 [1.08, 1.29] | 0.39 [0.24, 0.57] | 0.79 [0.59, 0.98] | 1.01 [0.70, 1.35] |
| ... omega | 0.69 [0.64, 0.74] | 0.70 [0.50, 0.93] | -0.007 [-0.243, 0.204] | 0.40 [0.11, 0.70] |
| rewrite glue (Eq.mpr, congrArg, simp lemmas of core) | 7.55 [7.45, 7.65] | 12.9 [12.7, 13.2] | -5.39 [-5.68, -5.09] | 11.8 [10.9, 12.9] |
| order/arithmetic library lemmas | 0.59 [0.58, 0.61] | 0.74 [0.70, 0.78] | -0.15 [-0.19, -0.11] | 0.32 [0.23, 0.45] |
| positivity lemmas | 0.82 [0.81, 0.84] | 0.70 [0.66, 0.74] | 0.13 [0.08, 0.17] | 0.30 [0.27, 0.34] |
| arithmetic total: certificates + rewrite + order + positivity | 23.0 [22.7, 23.4] | 24.3 [23.4, 25.2] | -1.29 [-2.23, -0.23] | 22.9 [21.3, 24.4] |
| claim B: cast functions, cast lemmas, ENNReal/NNReal lemmas, finiteness lemmas, ℝ≥0∞ norms | 0.042 [0.038, 0.046] | 2.02 [1.88, 2.16] | -1.97 [-2.12, -1.84] | 0.58 [0.49, 0.71] |
| claim C: indicator/restrict/support/cutoff lemmas and functions | 0.088 [0.083, 0.092] | 0.62 [0.55, 0.70] | -0.54 [-0.61, -0.46] | 0.046 [0.032, 0.064] |
| claim D: measurability + integrability + regularity lemmas | 0.43 [0.42, 0.44] | 0.45 [0.41, 0.50] | -0.018 [-0.065, 0.025] | 0.90 [0.78, 1.02] |
| ... regularity lemmas | 0.31 [0.30, 0.32] | 0.034 [0.025, 0.045] | 0.28 [0.26, 0.29] | 0.013 [0.005, 0.022] |
| instances (data_instance) | 33.2 [32.7, 33.6] | 22.1 [21.5, 22.7] | 11.1 [10.3, 11.8] | 16.0 [15.0, 17.0] |
| functions and types (data) | 38.9 [38.6, 39.3] | 45.7 [45.1, 46.3] | -6.83 [-7.53, -6.14] | 54.6 [53.4, 56.0] |
| % of theorems whose proof contains ring output | 20.1 [19.7, 20.5] | 16.3 [15.0, 17.8] | 3.80 [2.27, 5.19] | 17.7 [15.3, 20.1] |
| % of theorems whose proof contains normnum output | 25.4 [25.0, 25.8] | 23.4 [21.8, 25.0] | 1.98 [0.32, 3.61] | 17.1 [14.8, 19.5] |
| % of theorems whose proof contains linarith output | 10.5 [10.2, 10.8] | 10.3 [9.2, 11.6] | 0.18 [-1.11, 1.39] | 11.9 [9.9, 13.9] |
| % of theorems whose proof contains fieldsimp output | 7.13 [6.87, 7.39] | 3.66 [2.95, 4.37] | 3.47 [2.73, 4.21] | 9.10 [7.36, 10.84] |
| % of theorems whose proof contains omega output | 2.87 [2.70, 3.04] | 5.16 [4.34, 6.06] | -2.29 [-3.19, -1.46] | 1.53 [0.82, 2.35] |
| % of theorems whose proof contains any of these | 28.1 [27.7, 28.5] | 25.7 [24.1, 27.4] | 2.35 [0.68, 4.03] | 18.6 [16.3, 21.2] |

By area:

| | ns: Navier–Stokes | ns: Euler | ns: support | Carleson: main | Carleson: ToMathlib |
|---|---|---|---|---|---|
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 15.6 [15.1, 16.0] | 8.96 [8.45, 9.40] | 23.8 [22.4, 25.3] | 11.9 [10.9, 13.0] | 3.53 [2.74, 4.35] |
| ... ring | 9.36 [9.09, 9.63] | 5.08 [4.68, 5.43] | 14.3 [13.1, 15.5] | 6.32 [5.71, 6.97] | 2.17 [1.55, 2.81] |
| ... normnum | 3.79 [3.67, 3.92] | 1.75 [1.64, 1.85] | 4.74 [4.39, 5.10] | 3.48 [3.17, 3.80] | 0.57 [0.43, 0.70] |
| ... linarith | 0.51 [0.49, 0.53] | 0.30 [0.27, 0.32] | 0.78 [0.68, 0.86] | 0.45 [0.38, 0.52] | 0.085 [0.051, 0.122] |
| ... fieldsimp | 1.48 [1.33, 1.64] | 0.34 [0.25, 0.43] | 2.46 [2.03, 2.91] | 0.43 [0.25, 0.65] | 0.26 [0.10, 0.47] |
| ... omega | 0.28 [0.24, 0.33] | 1.26 [1.13, 1.39] | 1.29 [1.01, 1.55] | 0.82 [0.58, 1.11] | 0.30 [0.12, 0.57] |
| rewrite glue (Eq.mpr, congrArg, simp lemmas of core) | 8.93 [8.79, 9.07] | 4.74 [4.58, 4.89] | 9.06 [8.68, 9.44] | 12.5 [12.2, 12.8] | 14.4 [13.8, 14.9] |
| order/arithmetic library lemmas | 0.51 [0.49, 0.52] | 0.76 [0.73, 0.78] | 0.55 [0.51, 0.58] | 0.80 [0.76, 0.85] | 0.54 [0.48, 0.60] |
| positivity lemmas | 0.82 [0.80, 0.84] | 0.81 [0.78, 0.84] | 0.92 [0.87, 0.97] | 0.83 [0.78, 0.88] | 0.27 [0.23, 0.30] |
| arithmetic total: certificates + rewrite + order + positivity | 25.8 [25.4, 26.3] | 15.3 [14.7, 15.8] | 34.4 [32.8, 35.8] | 26.0 [25.0, 27.1] | 18.7 [17.7, 19.7] |
| claim B: cast functions, cast lemmas, ENNReal/NNReal lemmas, finiteness lemmas, ℝ≥0∞ norms | 0.026 [0.022, 0.030] | 0.058 [0.050, 0.066] | 0.090 [0.071, 0.112] | 1.59 [1.43, 1.75] | 3.42 [3.15, 3.72] |
| claim C: indicator/restrict/support/cutoff lemmas and functions | 0.082 [0.076, 0.087] | 0.099 [0.091, 0.108] | 0.086 [0.067, 0.107] | 0.57 [0.48, 0.65] | 0.81 [0.65, 0.99] |
| claim D: measurability + integrability + regularity lemmas | 0.51 [0.49, 0.53] | 0.32 [0.30, 0.33] | 0.37 [0.32, 0.42] | 0.37 [0.32, 0.43] | 0.71 [0.61, 0.81] |
| ... regularity lemmas | 0.42 [0.40, 0.44] | 0.14 [0.13, 0.15] | 0.21 [0.18, 0.25] | 0.038 [0.027, 0.052] | 0.018 [0.010, 0.029] |
| instances (data_instance) | 28.7 [28.2, 29.2] | 43.2 [42.5, 44.0] | 24.5 [23.0, 26.1] | 21.9 [21.2, 22.6] | 22.7 [21.4, 24.1] |
| functions and types (data) | 40.9 [40.4, 41.4] | 35.9 [35.4, 36.5] | 37.1 [36.4, 37.8] | 45.0 [44.3, 45.6] | 48.2 [47.1, 49.2] |
| % of theorems whose proof contains ring output | 20.9 [20.3, 21.3] | 15.2 [14.4, 15.9] | 34.4 [32.4, 36.5] | 24.8 [22.8, 27.0] | 5.55 [4.29, 6.90] |
| % of theorems whose proof contains normnum output | 25.7 [25.1, 26.2] | 21.5 [20.7, 22.3] | 41.2 [39.1, 43.4] | 36.1 [33.6, 38.5] | 7.57 [6.06, 9.08] |
| % of theorems whose proof contains linarith output | 10.8 [10.4, 11.2] | 8.09 [7.53, 8.65] | 18.9 [17.3, 20.5] | 16.8 [14.9, 18.6] | 2.19 [1.35, 3.03] |
| % of theorems whose proof contains fieldsimp output | 7.92 [7.58, 8.25] | 3.54 [3.20, 3.89] | 15.1 [13.5, 16.5] | 5.72 [4.58, 7.00] | 1.09 [0.50, 1.68] |
| % of theorems whose proof contains omega output | 1.19 [1.05, 1.32] | 6.39 [5.86, 6.86] | 7.06 [5.97, 8.21] | 7.60 [6.26, 8.95] | 2.10 [1.43, 2.94] |
| % of theorems whose proof contains any of these | 27.4 [26.9, 28.0] | 26.4 [25.5, 27.2] | 45.1 [42.9, 47.3] | 38.3 [35.7, 40.6] | 10.0 [8.3, 11.9] |

## 3. Explicit constants (claim A)

Percent of theorems unless the row says otherwise.

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 2.45 [2.30, 2.61] | 0.037 [0.000, 0.112] | 2.41 [2.25, 2.58] | 0.00 [0.00, 0.00] |
| ... and that C is used as an upper bound (`… ≤ … C …`) | 2.01 [1.87, 2.15] | 0.037 [0.000, 0.112] | 1.97 [1.81, 2.13] | 0.00 [0.00, 0.00] |
| conclusion has a real ∃ used as an upper bound, with or without a sign conjunct | 2.49 [2.34, 2.63] | 0.19 [0.04, 0.37] | 2.30 [2.08, 2.52] | 0.00 [0.00, 0.00] |
| conclusion has any real-typed ∃ | 2.95 [2.78, 3.11] | 0.19 [0.04, 0.37] | 2.76 [2.52, 3.00] | 0.20 [0.00, 0.51] |
| a hypothesis has the `∃ C, 0 < C ∧ …` shape | 0.18 [0.14, 0.23] | 0.075 [0.000, 0.187] | 0.11 [-0.02, 0.20] | 0.00 [0.00, 0.00] |
| takes a real parameter x together with `0 < x` | 27.8 [27.4, 28.3] | 13.9 [12.6, 15.3] | 13.9 [12.4, 15.3] | 1.64 [0.82, 2.45] |
| ... two or more such parameters | 8.02 [7.75, 8.28] | 5.23 [4.41, 6.06] | 2.79 [1.89, 3.69] | 0.31 [0.00, 0.72] |
| ... mean number of such parameters per theorem | 0.39 [0.38, 0.39] | 0.22 [0.19, 0.24] | 0.17 [0.14, 0.19] | 0.021 [0.010, 0.036] |
| ... and the conclusion is an inequality mentioning it | 4.30 [4.10, 4.51] | 4.22 [3.44, 5.01] | 0.079 [-0.736, 0.887] | 0.61 [0.20, 1.12] |
| ... and the binder is named like a constant (C*, K*, M*, c*) | 3.74 [3.54, 3.92] | 1.53 [1.08, 2.02] | 2.20 [1.69, 2.71] | 0.61 [0.20, 1.12] |
| statement mentions a project-defined real constant (closed or ℕ/ℤ-indexed) | 10.5 [10.1, 10.7] | 28.7 [27.0, 30.5] | -18.3 [-20.1, -16.5] | 0.00 [0.00, 0.00] |
| ... allowing real parameters too (includes ordinary real functions) | 23.0 [22.6, 23.4] | 35.0 [33.2, 36.8] | -12.0 [-13.8, -10.1] | 0.00 [0.00, 0.00] |
| statement has a real literal ≥ 2 | 47.1 [46.6, 47.7] | 24.9 [23.4, 26.6] | 22.2 [20.5, 23.9] | 14.0 [11.9, 16.3] |
| statement has a real literal ≥ 3 | 9.17 [8.89, 9.45] | 11.1 [9.9, 12.2] | -1.89 [-3.05, -0.72] | 6.95 [5.42, 8.59] |
| statement has a real literal ≥ 100 | 1.61 [1.49, 1.74] | 0.79 [0.49, 1.12] | 0.83 [0.47, 1.18] | 0.00 [0.00, 0.00] |
| distinct real literals ≥ 2 per theorem (mean) | 0.58 [0.57, 0.59] | 0.33 [0.31, 0.36] | 0.25 [0.22, 0.28] | 0.20 [0.17, 0.24] |
| statement has any numeric literal ≥ 3 | 46.1 [45.6, 46.6] | 17.2 [15.9, 18.5] | 28.9 [27.4, 30.4] | 9.41 [7.67, 11.15] |
| P(conclusion is ∃C>0 | proof uses a lemma concluding ∃C>0) | 69.8 [67.1, 72.7] | 0.00 [0.00, 0.00] | 69.8 [67.1, 72.7] | – |
| P(conclusion is ∃C>0 | proof uses no such lemma) | 0.60 [0.52, 0.68] | 0.037 [0.000, 0.112] | 0.56 [0.45, 0.66] | 0.00 [0.00, 0.00] |
| % of theorems whose proof uses a lemma concluding ∃C>0 | 2.67 [2.52, 2.82] | 0.19 [0.04, 0.37] | 2.48 [2.24, 2.71] | 0.00 [0.00, 0.00] |
| % of ∃C>0 lemmas used by another project theorem | 78.6 [75.8, 81.2] | 100.0 [100.0, 100.0] | -21.4 [-24.3, -18.9] | – |
| % of ∃C>0 lemmas used by another ∃C>0 lemma | 61.8 [58.7, 64.9] | 0.00 [0.00, 0.00] | 61.8 [58.6, 64.6] | – |

By area:

| | ns: Navier–Stokes | ns: Euler | ns: support | Carleson: main | Carleson: ToMathlib |
|---|---|---|---|---|---|
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 3.33 [3.12, 3.54] | 0.41 [0.28, 0.53] | 1.24 [0.80, 1.79] | 0.067 [0.000, 0.202] | 0.00 [0.00, 0.00] |
| ... and that C is used as an upper bound (`… ≤ … C …`) | 2.76 [2.57, 2.96] | 0.26 [0.17, 0.36] | 1.00 [0.60, 1.49] | 0.067 [0.000, 0.202] | 0.00 [0.00, 0.00] |
| conclusion has a real ∃ used as an upper bound, with or without a sign conjunct | 3.28 [3.06, 3.49] | 0.68 [0.52, 0.83] | 1.34 [0.85, 1.89] | 0.34 [0.07, 0.67] | 0.00 [0.00, 0.00] |
| conclusion has any real-typed ∃ | 3.84 [3.62, 4.06] | 0.87 [0.69, 1.03] | 1.84 [1.24, 2.49] | 0.34 [0.07, 0.67] | 0.00 [0.00, 0.00] |
| a hypothesis has the `∃ C, 0 < C ∧ …` shape | 0.25 [0.19, 0.31] | 0.00 [0.00, 0.00] | 0.20 [0.05, 0.40] | 0.00 [0.00, 0.00] | 0.17 [0.00, 0.42] |
| takes a real parameter x together with `0 < x` | 20.6 [20.1, 21.1] | 46.2 [45.2, 47.2] | 29.8 [27.6, 31.7] | 11.0 [9.4, 12.7] | 17.5 [15.4, 19.6] |
| ... two or more such parameters | 6.11 [5.84, 6.41] | 13.7 [13.0, 14.4] | 4.18 [3.33, 5.03] | 2.22 [1.48, 3.03] | 9.00 [7.49, 10.60] |
| ... mean number of such parameters per theorem | 0.30 [0.29, 0.30] | 0.62 [0.61, 0.64] | 0.36 [0.33, 0.38] | 0.13 [0.11, 0.15] | 0.32 [0.28, 0.37] |
| ... and the conclusion is an inequality mentioning it | 1.75 [1.61, 1.90] | 10.1 [9.5, 10.7] | 8.56 [7.36, 9.75] | 4.91 [3.84, 5.99] | 3.36 [2.44, 4.37] |
| ... and the binder is named like a constant (C*, K*, M*, c*) | 3.02 [2.82, 3.22] | 5.61 [5.19, 6.08] | 3.58 [2.79, 4.38] | 0.47 [0.20, 0.81] | 2.86 [1.93, 3.87] |
| statement mentions a project-defined real constant (closed or ℕ/ℤ-indexed) | 12.0 [11.7, 12.4] | 7.75 [7.22, 8.25] | 3.33 [2.59, 4.13] | 51.6 [49.1, 54.2] | 0.084 [0.000, 0.252] |
| ... allowing real parameters too (includes ordinary real functions) | 24.4 [23.8, 24.9] | 19.6 [18.8, 20.4] | 22.4 [20.5, 24.2] | 59.6 [57.1, 62.0] | 4.37 [3.28, 5.55] |
| statement has a real literal ≥ 2 | 35.5 [34.9, 36.0] | 76.7 [75.9, 77.5] | 50.3 [48.3, 52.5] | 42.7 [40.1, 45.2] | 2.69 [1.85, 3.62] |
| statement has a real literal ≥ 3 | 8.26 [7.96, 8.58] | 10.2 [9.6, 10.7] | 16.0 [14.4, 17.6] | 19.4 [17.4, 21.3] | 0.67 [0.25, 1.18] |
| statement has a real literal ≥ 100 | 1.28 [1.14, 1.40] | 2.03 [1.76, 2.31] | 3.83 [2.98, 4.68] | 1.41 [0.81, 2.02] | 0.00 [0.00, 0.00] |
| distinct real literals ≥ 2 per theorem (mean) | 0.45 [0.44, 0.46] | 0.90 [0.89, 0.91] | 0.76 [0.71, 0.81] | 0.57 [0.53, 0.62] | 0.031 [0.021, 0.042] |
| statement has any numeric literal ≥ 3 | 36.4 [35.8, 36.9] | 72.2 [71.4, 73.0] | 40.8 [38.8, 43.0] | 30.5 [28.1, 32.7] | 0.67 [0.25, 1.18] |
| P(conclusion is ∃C>0 | proof uses a lemma concluding ∃C>0) | 70.4 [67.6, 73.4] | 54.8 [39.1, 69.2] | 72.2 [50.0, 92.3] | 0.00 [0.00, 0.00] | – |
| P(conclusion is ∃C>0 | proof uses no such lemma) | 0.77 [0.67, 0.87] | 0.19 [0.11, 0.28] | 0.60 [0.30, 0.96] | 0.068 [0.000, 0.203] | 0.00 [0.00, 0.00] |
| % of theorems whose proof uses a lemma concluding ∃C>0 | 3.68 [3.46, 3.89] | 0.41 [0.29, 0.53] | 0.90 [0.50, 1.34] | 0.34 [0.07, 0.67] | 0.00 [0.00, 0.00] |
| % of ∃C>0 lemmas used by another project theorem | 78.8 [76.1, 81.4] | 69.0 [55.1, 81.8] | 88.0 [75.0, 100.0] | 100.0 [100.0, 100.0] | – |
| % of ∃C>0 lemmas used by another ∃C>0 lemma | 62.2 [59.1, 65.4] | 45.2 [30.3, 60.0] | 76.0 [57.9, 91.7] | 0.00 [0.00, 0.00] | – |

Propagation of `∃ C > 0` through the dependency graph (project theorems, `valueDeps` of the earlier export):

| | ns | Carleson | PFR |
|---|---|---|---|
| theorems concluding `∃ C, 0 < C ∧ …` | 946 | 1 | 0 |
| ... used by another project theorem | 744 | 1 | 0 |
| ... used by another theorem that also concludes `∃ C > 0` | 585 | 0 | 0 |
| theorems whose proof uses such a lemma | 1031 | 5 | 0 |
| ... and conclude `∃ C > 0` themselves | 720 | 0 | 0 |
| longest chain of `∃ C` lemmas feeding `∃ C` lemmas | 13 | 1 | 0 |

Chain depth of ns `∃ C` lemmas (1 = uses no other `∃ C` lemma): 1: 226, 2: 170, 3: 132, 4: 100, 5: 80, 6: 68, 7: 58, 8: 37, 9: 23, 10: 17, 11: 22, 12: 10, 13: 3.

## 4. Unfolding proxies

Percent of theorems unless the row says otherwise. P1–P5 are defined and justified in the verdict section.

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| P1 statement uses a filter/asymptotic notion (Tendsto, ∀ᶠ, IsBigO, HasSum, …) | 6.01 [5.79, 6.24] | 3.59 [2.88, 4.26] | 2.42 [1.69, 3.16] | 4.70 [3.37, 5.93] |
| P1 ... Filter.Tendsto | 1.43 [1.32, 1.55] | 0.60 [0.34, 0.93] | 0.83 [0.50, 1.13] | 0.72 [0.31, 1.23] |
| P1 statement has an explicit ε-shape `∀ ε>0, … ∃ …, … < ε` | 0.080 [0.052, 0.111] | 0.34 [0.11, 0.56] | -0.26 [-0.50, -0.03] | 0.00 [0.00, 0.00] |
| P1 statement has `∀ x>0, … ∃ …` (looser) | 0.85 [0.77, 0.95] | 0.56 [0.30, 0.86] | 0.29 [-0.04, 0.58] | 0.51 [0.10, 1.02] |
| P1 bundled share = bundled / (bundled + strict ε-shape) | 98.7 [98.2, 99.1] | 91.4 [85.7, 96.8] | 7.25 [1.90, 12.96] | 100.0 [100.0, 100.0] |
| P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …) | 26.0 [25.5, 26.4] | 3.07 [2.47, 3.74] | 22.9 [22.1, 23.7] | 3.58 [2.45, 4.81] |
| P2 statement uses IsLinearMap / IsBoundedLinearMap-style predicates | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| P2 statement uses a bundled function space (C(X,Y), Lp, 𝓢, a.e.-classes) | 16.1 [15.7, 16.4] | 4.56 [3.78, 5.35] | 11.5 [10.6, 12.3] | 0.10 [0.00, 0.31] |
| P2 % of term binders that are bare functions | 14.7 [14.5, 14.9] | 26.8 [26.3, 27.4] | -12.1 [-12.7, -11.5] | 48.0 [45.8, 50.0] |
| P2 % of term binders whose type is a structure | 55.2 [54.9, 55.5] | 31.5 [30.8, 32.1] | 23.6 [22.9, 24.4] | 42.7 [40.9, 44.7] |
| P2 ... a project-defined structure | 17.2 [17.0, 17.5] | 1.35 [1.18, 1.52] | 15.9 [15.6, 16.2] | 2.07 [1.64, 2.53] |
| P3 statement uses eLpNorm / MemLp / Lp | 4.38 [4.17, 4.59] | 12.0 [10.8, 13.1] | -7.58 [-8.80, -6.38] | 0.00 [0.00, 0.00] |
| P3 statement has an integral of a power of a norm | 0.036 [0.021, 0.057] | 0.67 [0.37, 1.01] | -0.64 [-0.96, -0.34] | 0.00 [0.00, 0.00] |
| P3 statement has any integral | 3.32 [3.14, 3.49] | 9.23 [8.11, 10.32] | -5.91 [-7.01, -4.80] | 1.94 [1.12, 2.86] |
| P3 bundled share = bundled / (bundled + raw) | 99.2 [98.7, 99.5] | 94.7 [92.2, 96.9] | 4.50 [2.17, 7.08] | – |
| P4 proof mass whose nearest goal is a certificate predicate | 5.91 [5.79, 6.04] | 4.57 [4.22, 4.94] | 1.34 [0.95, 1.71] | 4.29 [3.61, 4.87] |
| P4 certificate constants as share of non-project constant uses | 14.1 [13.8, 14.4] | 9.95 [9.10, 10.83] | 4.13 [3.22, 5.10] | 10.5 [9.0, 12.0] |
| P4 % of theorems with linarith/nlinarith output in the proof | 10.5 [10.2, 10.8] | 10.3 [9.2, 11.6] | 0.18 [-1.11, 1.39] | 11.9 [9.9, 13.9] |
| P5 % of theorems whose proof rewrites with an equation lemma of a project definition | 3.01 [2.85, 3.17] | 9.31 [8.26, 10.47] | -6.30 [-7.47, -5.22] | 3.58 [2.45, 4.70] |
| P5 % of theorems whose statement mentions a project-defined constant | 96.2 [96.0, 96.4] | 81.5 [79.9, 82.9] | 14.8 [13.3, 16.3] | 73.1 [70.0, 75.8] |
| P5 project-defined share of the distinct constants in a statement | 15.1 [14.9, 15.2] | 17.5 [16.9, 18.1] | -2.44 [-3.08, -1.81] | 7.97 [7.52, 8.41] |
| P5 statement mentions a project structure bundling data with proofs ("packet") | 34.9 [34.4, 35.4] | 7.48 [6.43, 8.45] | 27.4 [26.4, 28.5] | 7.16 [5.62, 8.79] |
| P5 statement mentions a project Prop-valued structure | 14.7 [14.4, 15.1] | 7.81 [6.77, 8.90] | 6.92 [5.82, 7.99] | 4.91 [3.58, 6.44] |
| P5 either | 40.6 [40.1, 41.1] | 13.3 [12.0, 14.6] | 27.3 [26.0, 28.7] | 11.9 [9.9, 14.0] |
| P5 % of term binders whose type is a project packet | 11.9 [11.7, 12.1] | 1.35 [1.18, 1.52] | 10.6 [10.3, 10.8] | 2.07 [1.64, 2.53] |
| P5 % of Prop binders whose head is a project structure | 7.14 [6.94, 7.36] | 7.07 [6.25, 7.95] | 0.078 [-0.831, 0.945] | 9.15 [8.31, 9.98] |

By area:

| | ns: Navier–Stokes | ns: Euler | ns: support | Carleson: main | Carleson: ToMathlib |
|---|---|---|---|---|---|
| P1 statement uses a filter/asymptotic notion (Tendsto, ∀ᶠ, IsBigO, HasSum, …) | 5.61 [5.33, 5.88] | 6.55 [6.09, 7.05] | 8.51 [7.36, 9.75] | 2.02 [1.34, 2.76] | 5.55 [4.29, 6.90] |
| P1 ... Filter.Tendsto | 1.27 [1.13, 1.41] | 1.61 [1.37, 1.86] | 2.64 [1.99, 3.33] | 0.94 [0.47, 1.48] | 0.17 [0.00, 0.42] |
| P1 statement has an explicit ε-shape `∀ ε>0, … ∃ …, … < ε` | 0.087 [0.057, 0.125] | 0.039 [0.010, 0.078] | 0.20 [0.05, 0.40] | 0.47 [0.13, 0.81] | 0.17 [0.00, 0.42] |
| P1 statement has `∀ x>0, … ∃ …` (looser) | 0.83 [0.72, 0.94] | 0.98 [0.77, 1.17] | 0.55 [0.25, 0.90] | 0.54 [0.20, 0.94] | 0.59 [0.17, 1.01] |
| P1 bundled share = bundled / (bundled + strict ε-shape) | 98.5 [97.8, 99.0] | 99.4 [98.8, 99.9] | 97.7 [95.3, 99.4] | 81.1 [68.9, 92.6] | 97.1 [92.4, 100.0] |
| P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …) | 16.4 [15.9, 16.8] | 52.0 [51.1, 53.0] | 19.9 [18.3, 21.7] | 3.03 [2.22, 3.97] | 3.11 [2.19, 4.12] |
| P2 statement uses IsLinearMap / IsBoundedLinearMap-style predicates | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] |
| P2 statement uses a bundled function space (C(X,Y), Lp, 𝓢, a.e.-classes) | 1.24 [1.11, 1.38] | 54.6 [53.6, 55.5] | 14.6 [13.1, 16.2] | 6.86 [5.65, 8.14] | 1.68 [1.01, 2.44] |
| P2 % of term binders that are bare functions | 16.3 [16.0, 16.6] | 9.49 [9.12, 9.86] | 24.0 [22.8, 25.1] | 30.7 [30.2, 31.2] | 18.3 [17.3, 19.4] |
| P2 % of term binders whose type is a structure | 51.5 [51.1, 51.8] | 65.0 [64.5, 65.5] | 50.0 [48.5, 51.5] | 32.6 [31.9, 33.2] | 29.1 [27.6, 30.6] |
| P2 ... a project-defined structure | 17.5 [17.2, 17.8] | 19.0 [18.6, 19.5] | 0.42 [0.27, 0.57] | 1.73 [1.51, 1.96] | 0.52 [0.33, 0.72] |
| P3 statement uses eLpNorm / MemLp / Lp | 1.17 [1.04, 1.30] | 11.6 [11.0, 12.2] | 9.90 [8.66, 11.24] | 7.00 [5.79, 8.28] | 18.2 [16.1, 20.4] |
| P3 statement has an integral of a power of a norm | 0.008 [0.000, 0.019] | 0.059 [0.020, 0.108] | 0.30 [0.10, 0.55] | 0.00 [0.00, 0.00] | 1.51 [0.84, 2.27] |
| P3 statement has any integral | 3.20 [2.99, 3.42] | 3.08 [2.76, 3.41] | 6.17 [5.17, 7.26] | 9.35 [7.81, 11.04] | 9.08 [7.57, 10.77] |
| P3 bundled share = bundled / (bundled + raw) | 99.4 [98.3, 100.0] | 99.5 [99.1, 99.8] | 97.1 [94.5, 99.1] | 100.0 [100.0, 100.0] | 92.3 [88.8, 95.7] |
| P4 proof mass whose nearest goal is a certificate predicate | 6.65 [6.49, 6.81] | 3.61 [3.43, 3.78] | 8.80 [8.30, 9.30] | 5.49 [5.03, 5.93] | 1.29 [0.99, 1.58] |
| P4 certificate constants as share of non-project constant uses | 15.6 [15.1, 16.0] | 8.96 [8.45, 9.40] | 23.8 [22.4, 25.3] | 11.9 [10.9, 13.0] | 3.53 [2.74, 4.35] |
| P4 % of theorems with linarith/nlinarith output in the proof | 10.8 [10.4, 11.2] | 8.09 [7.53, 8.65] | 18.9 [17.3, 20.5] | 16.8 [14.9, 18.6] | 2.19 [1.35, 3.03] |
| P5 % of theorems whose proof rewrites with an equation lemma of a project definition | 3.28 [3.08, 3.49] | 2.17 [1.90, 2.45] | 3.73 [2.94, 4.53] | 14.5 [12.9, 16.1] | 2.78 [1.93, 3.70] |
| P5 % of theorems whose statement mentions a project-defined constant | 96.8 [96.6, 97.0] | 97.8 [97.5, 98.1] | 80.6 [79.0, 82.3] | 94.1 [92.9, 95.3] | 65.6 [63.1, 68.2] |
| P5 project-defined share of the distinct constants in a statement | 19.8 [19.6, 20.1] | 10.3 [10.2, 10.4] | 5.78 [5.54, 6.01] | 22.7 [22.0, 23.4] | 4.40 [4.13, 4.72] |
| P5 statement mentions a project structure bundling data with proofs ("packet") | 32.3 [31.8, 32.9] | 48.1 [47.2, 49.1] | 1.49 [1.00, 2.04] | 11.8 [10.2, 13.3] | 2.02 [1.26, 2.78] |
| P5 statement mentions a project Prop-valued structure | 19.0 [18.5, 19.5] | 6.31 [5.87, 6.77] | 1.29 [0.80, 1.79] | 10.2 [8.6, 11.8] | 4.88 [3.70, 6.22] |
| P5 either | 40.1 [39.5, 40.7] | 49.3 [48.3, 50.2] | 2.79 [2.09, 3.48] | 18.4 [16.4, 20.3] | 6.90 [5.55, 8.41] |
| P5 % of term binders whose type is a project packet | 9.94 [9.75, 10.14] | 18.5 [18.0, 19.0] | 0.42 [0.27, 0.57] | 1.73 [1.51, 1.96] | 0.52 [0.33, 0.72] |
| P5 % of Prop binders whose head is a project structure | 10.4 [10.1, 10.7] | 2.24 [2.03, 2.44] | 0.51 [0.32, 0.72] | 10.5 [9.2, 11.9] | 4.11 [3.31, 4.93] |

## 5. Subject-matter control

The same shares restricted to theorems of comparable content in both corpora. `MT`: the statement mentions a constant from `Mathlib.MeasureTheory`. `D-hyp`: the theorem has a measurability, integrability or regularity hypothesis.

| | ns, MT | Carleson, MT | difference |
|---|---|---|---|
| Prop-valued binders per theorem (mean) | 3.55 [3.45, 3.65] | 2.32 [2.18, 2.46] | 1.23 [1.07, 1.40] |
| % of Prop binders: finiteness (side) | 0.17 [0.11, 0.24] | 6.12 [5.15, 7.06] | -5.95 [-6.88, -4.98] |
| % of Prop binders: positivity (side) | 31.5 [30.9, 32.1] | 12.6 [11.3, 13.9] | 18.9 [17.4, 20.4] |
| % of Prop binders: measurability (side) | 2.85 [2.58, 3.10] | 17.1 [15.5, 18.8] | -14.3 [-15.9, -12.7] |
| % of Prop binders: integrability (side) | 4.22 [3.90, 4.58] | 9.05 [7.94, 10.22] | -4.82 [-5.99, -3.71] |
| % of Prop binders: regularity (side) | 14.4 [13.8, 15.0] | 0.48 [0.24, 0.73] | 13.9 [13.3, 14.5] |
| ... % mentioning a cast function | 0.83 [0.67, 1.00] | 3.61 [2.78, 4.45] | -2.78 [-3.62, -1.93] |
| claim C: % support class or mentioning indicator/restrict/support/cutoff | 2.18 [1.99, 2.40] | 4.12 [3.38, 4.90] | -1.93 [-2.75, -1.17] |
| inside a side-condition proof (any class) | 28.7 [27.8, 29.7] | 23.9 [21.7, 26.2] | 4.82 [2.31, 7.29] |
| ... finiteness | 0.33 [0.27, 0.39] | 2.57 [1.99, 3.24] | -2.24 [-2.92, -1.65] |
| ... positivity | 6.14 [5.80, 6.46] | 7.06 [6.39, 7.77] | -0.93 [-1.73, -0.20] |
| ... measurability | 2.39 [2.21, 2.57] | 6.78 [5.54, 8.37] | -4.39 [-5.97, -3.14] |
| ... integrability | 6.45 [5.93, 7.07] | 5.15 [4.05, 6.32] | 1.30 [-0.03, 2.67] |
| ... regularity | 13.2 [12.3, 14.1] | 2.32 [0.94, 4.00] | 10.9 [9.1, 12.6] |
| claim B upper bound: inside a proof whose type mentions a cast | 6.86 [6.01, 7.69] | 58.6 [54.4, 62.8] | -51.7 [-56.0, -47.3] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 21.8 [20.4, 23.3] | 51.3 [46.8, 55.8] | -29.5 [-34.3, -24.7] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 53.4 [52.6, 54.2] | 73.5 [72.4, 74.5] | -20.1 [-21.4, -18.7] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 2.86 [2.67, 3.04] | 3.27 [2.90, 3.63] | -0.41 [-0.81, -0.02] |
| nodes inside an instance argument | 43.8 [43.1, 44.5] | 15.9 [15.4, 16.5] | 27.9 [27.0, 28.8] |
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 5.81 [5.44, 6.19] | 7.47 [6.56, 8.46] | -1.66 [-2.74, -0.66] |
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 0.82 [0.62, 1.08] | 0.00 [0.00, 0.00] | 0.82 [0.62, 1.08] |
| takes a real parameter x together with `0 < x` | 53.5 [52.3, 54.7] | 16.6 [14.5, 18.5] | 36.9 [34.6, 39.3] |
| statement has a real literal ≥ 3 | 9.86 [9.15, 10.62] | 8.44 [6.94, 9.94] | 1.42 [-0.27, 3.06] |
| P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …) | 55.3 [54.1, 56.4] | 4.97 [3.79, 6.07] | 50.3 [48.8, 52.0] |
| P3 statement uses eLpNorm / MemLp / Lp | 26.8 [25.8, 27.9] | 25.2 [22.9, 27.7] | 1.55 [-1.07, 4.22] |
| P3 statement has an integral of a power of a norm | 0.22 [0.11, 0.35] | 1.42 [0.79, 2.13] | -1.20 [-1.91, -0.57] |
| P5 either | 36.3 [35.2, 37.6] | 20.2 [18.0, 22.6] | 16.2 [13.6, 18.7] |

| | ns, D-hyp | Carleson, D-hyp | difference |
|---|---|---|---|
| Prop-valued binders per theorem (mean) | 5.13 [5.03, 5.22] | 3.30 [3.08, 3.52] | 1.83 [1.59, 2.07] |
| % of Prop binders: finiteness (side) | 0.063 [0.039, 0.091] | 4.91 [3.81, 6.05] | -4.85 [-5.98, -3.75] |
| % of Prop binders: positivity (side) | 20.0 [19.7, 20.4] | 9.57 [8.17, 11.02] | 10.5 [9.0, 12.0] |
| % of Prop binders: measurability (side) | 1.44 [1.30, 1.57] | 25.2 [22.9, 27.5] | -23.8 [-26.2, -21.5] |
| % of Prop binders: integrability (side) | 2.20 [2.01, 2.38] | 13.4 [11.8, 15.2] | -11.2 [-13.0, -9.5] |
| % of Prop binders: regularity (side) | 29.5 [29.0, 30.1] | 1.45 [0.92, 2.07] | 28.1 [27.2, 28.8] |
| ... % mentioning a cast function | 0.37 [0.29, 0.45] | 4.06 [2.95, 5.20] | -3.69 [-4.82, -2.57] |
| claim C: % support class or mentioning indicator/restrict/support/cutoff | 1.62 [1.49, 1.75] | 5.66 [4.64, 6.69] | -4.04 [-5.05, -3.01] |
| inside a side-condition proof (any class) | 33.9 [32.6, 35.3] | 27.4 [24.3, 31.2] | 6.51 [2.51, 10.11] |
| ... finiteness | 0.15 [0.12, 0.19] | 2.01 [1.49, 2.56] | -1.86 [-2.41, -1.34] |
| ... positivity | 5.64 [5.34, 5.97] | 5.93 [5.18, 6.76] | -0.29 [-1.17, 0.53] |
| ... measurability | 0.73 [0.65, 0.82] | 8.17 [6.14, 10.98] | -7.45 [-10.24, -5.44] |
| ... integrability | 2.55 [2.28, 2.80] | 8.09 [6.13, 9.99] | -5.55 [-7.39, -3.64] |
| ... regularity | 24.7 [23.2, 26.1] | 3.17 [1.09, 5.74] | 21.5 [18.6, 24.2] |
| claim B upper bound: inside a proof whose type mentions a cast | 3.31 [2.81, 3.82] | 60.6 [54.7, 66.3] | -57.3 [-63.0, -51.2] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 14.3 [13.4, 15.5] | 67.2 [62.0, 71.8] | -52.8 [-57.7, -47.5] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 56.8 [55.9, 57.6] | 74.4 [73.0, 75.7] | -17.6 [-19.2, -15.9] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 4.11 [3.89, 4.32] | 2.99 [2.47, 3.48] | 1.12 [0.60, 1.69] |
| nodes inside an instance argument | 30.6 [29.8, 31.4] | 15.6 [14.9, 16.4] | 15.0 [13.9, 16.0] |
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 10.7 [10.1, 11.3] | 7.42 [5.96, 8.89] | 3.26 [1.68, 4.77] |
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 3.95 [3.56, 4.35] | 0.00 [0.00, 0.00] | 3.95 [3.56, 4.35] |
| takes a real parameter x together with `0 < x` | 31.7 [30.7, 32.7] | 18.0 [14.9, 21.2] | 13.7 [10.5, 17.1] |
| statement has a real literal ≥ 3 | 9.06 [8.45, 9.70] | 9.09 [6.78, 11.40] | -0.027 [-2.454, 2.325] |
| P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …) | 38.3 [37.3, 39.4] | 8.10 [6.12, 10.25] | 30.2 [27.7, 32.6] |
| P3 statement uses eLpNorm / MemLp / Lp | 11.7 [11.0, 12.4] | 33.7 [30.1, 37.5] | -22.0 [-25.9, -18.3] |
| P3 statement has an integral of a power of a norm | 0.12 [0.05, 0.18] | 1.98 [0.99, 3.14] | -1.87 [-3.02, -0.84] |
| P5 either | 24.7 [23.7, 25.6] | 26.3 [23.0, 30.1] | -1.60 [-5.40, 1.96] |

Support libraries against each other (ns modules importing no project module vs `Carleson.ToMathlib`):

| | ns: support | Carleson: ToMathlib | difference |
|---|---|---|---|
| Prop-valued binders per theorem (mean) | 2.55 [2.41, 2.69] | 2.17 [2.02, 2.32] | 0.38 [0.18, 0.58] |
| % of Prop binders: finiteness (side) | 0.39 [0.21, 0.62] | 9.50 [8.31, 10.76] | -9.11 [-10.32, -7.90] |
| % of Prop binders: positivity (side) | 26.9 [25.4, 28.1] | 18.9 [17.2, 20.5] | 8.00 [5.79, 9.97] |
| % of Prop binders: measurability (side) | 1.52 [1.19, 1.98] | 13.1 [11.5, 14.7] | -11.6 [-13.2, -10.0] |
| % of Prop binders: integrability (side) | 3.01 [2.46, 3.60] | 3.80 [3.04, 4.66] | -0.79 [-1.83, 0.14] |
| % of Prop binders: regularity (side) | 20.3 [18.9, 21.8] | 0.31 [0.12, 0.59] | 20.0 [18.6, 21.4] |
| ... % mentioning a cast function | 1.68 [1.23, 2.22] | 2.29 [1.49, 3.13] | -0.61 [-1.66, 0.41] |
| claim C: % support class or mentioning indicator/restrict/support/cutoff | 2.03 [1.63, 2.47] | 1.32 [0.90, 1.77] | 0.71 [0.08, 1.30] |
| inside a side-condition proof (any class) | 28.7 [26.6, 30.9] | 21.9 [19.7, 24.4] | 6.80 [3.48, 9.80] |
| ... finiteness | 0.16 [0.09, 0.24] | 4.13 [2.82, 5.71] | -3.97 [-5.57, -2.66] |
| ... positivity | 11.7 [10.8, 12.7] | 7.36 [6.33, 8.50] | 4.36 [2.91, 5.88] |
| ... measurability | 0.58 [0.40, 0.83] | 6.05 [5.13, 7.09] | -5.47 [-6.52, -4.49] |
| ... integrability | 3.88 [2.89, 5.07] | 2.77 [1.95, 3.80] | 1.11 [-0.47, 2.56] |
| ... regularity | 12.1 [10.1, 14.2] | 1.56 [0.51, 3.00] | 10.5 [8.1, 12.9] |
| claim B upper bound: inside a proof whose type mentions a cast | 4.18 [3.28, 5.18] | 51.2 [46.2, 56.1] | -47.1 [-52.1, -41.9] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 7.79 [6.51, 9.24] | 29.8 [25.2, 34.8] | -22.0 [-27.2, -17.0] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 70.8 [69.8, 71.8] | 71.5 [70.0, 72.9] | -0.68 [-2.34, 1.11] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 8.80 [8.30, 9.30] | 1.29 [0.99, 1.58] | 7.51 [6.93, 8.10] |
| nodes inside an instance argument | 18.5 [17.5, 19.4] | 14.0 [13.4, 14.7] | 4.43 [3.27, 5.60] |
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 23.8 [22.4, 25.3] | 3.53 [2.74, 4.35] | 20.3 [18.7, 22.0] |
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 1.24 [0.80, 1.79] | 0.00 [0.00, 0.00] | 1.24 [0.80, 1.79] |
| takes a real parameter x together with `0 < x` | 29.8 [27.6, 31.7] | 17.5 [15.4, 19.6] | 12.3 [9.4, 15.0] |
| statement has a real literal ≥ 3 | 16.0 [14.4, 17.6] | 0.67 [0.25, 1.18] | 15.3 [13.7, 17.0] |
| P2 statement uses a bundled morphism type (ContinuousLinearMap, LinearMap, …) | 19.9 [18.3, 21.7] | 3.11 [2.19, 4.12] | 16.8 [14.8, 18.8] |
| P3 statement uses eLpNorm / MemLp / Lp | 9.90 [8.66, 11.24] | 18.2 [16.1, 20.4] | -8.27 [-10.64, -5.75] |
| P3 statement has an integral of a power of a norm | 0.30 [0.10, 0.55] | 1.51 [0.84, 2.27] | -1.22 [-2.00, -0.46] |
| P5 either | 2.79 [2.09, 3.48] | 6.90 [5.55, 8.41] | -4.11 [-5.85, -2.58] |

## 6. Sensitivity: resampling modules instead of theorems

Theorems in one file are not independent. The same point estimates with intervals from resampling whole modules:

| | ns | ns: Navier–Stokes | ns: Euler | Carleson |
|---|---|---|---|---|
| % of Prop binders: positivity (side) | 26.7 [25.5, 27.7] | 23.2 [21.7, 24.9] | 32.9 [31.8, 33.9] | 15.0 [9.5, 20.9] |
| % of Prop binders: measurability (side) | 0.61 [0.46, 0.78] | 0.23 [0.11, 0.40] | 1.14 [0.83, 1.55] | 10.5 [7.0, 14.4] |
| % of Prop binders: regularity (side) | 12.4 [11.5, 13.5] | 13.1 [11.8, 14.5] | 10.2 [9.3, 11.1] | 0.60 [0.19, 1.24] |
| inside a side-condition proof (any class) | 24.8 [23.7, 25.9] | 24.0 [22.5, 25.7] | 25.5 [24.5, 26.5] | 20.2 [17.9, 23.0] |
| ... positivity | 9.23 [8.68, 9.74] | 8.80 [8.15, 9.53] | 9.44 [8.84, 10.04] | 9.26 [8.20, 10.41] |
| ... regularity | 13.2 [12.2, 14.4] | 13.1 [11.7, 14.9] | 13.6 [12.4, 14.7] | 2.21 [0.93, 3.89] |
| claim B: finiteness side-conditions | 0.074 [0.050, 0.100] | 0.057 [0.034, 0.089] | 0.086 [0.056, 0.119] | 1.76 [1.30, 2.36] |
| claim B upper bound: inside a proof whose type mentions a cast | 1.61 [1.17, 2.20] | 0.30 [0.18, 0.47] | 3.63 [2.92, 4.33] | 43.0 [36.6, 49.4] |
| claim C upper bound: inside a proof whose type mentions indicator/restrict/support/cutoff | 11.3 [10.4, 12.3] | 10.3 [9.1, 11.7] | 14.4 [12.7, 16.2] | 33.3 [26.6, 39.5] |
| ... measurability + integrability only | 2.17 [1.73, 2.71] | 1.85 [1.53, 2.23] | 2.22 [1.89, 2.58] | 6.93 [5.35, 8.82] |
| arithmetic/order plumbing: nearest goal is an equation or inequality | 62.2 [60.9, 63.6] | 63.0 [61.8, 64.3] | 58.2 [57.2, 59.2] | 72.2 [70.7, 73.5] |
| nearest goal is a certificate predicate (ring/norm_num/linarith internals) | 5.91 [5.47, 6.36] | 6.65 [6.07, 7.25] | 3.61 [3.30, 3.93] | 4.57 [3.90, 5.17] |
| nodes inside an instance argument | 27.1 [25.8, 28.4] | 22.0 [21.1, 22.9] | 40.0 [38.8, 41.1] | 16.6 [15.7, 17.4] |
| automation certificates (ring, norm_num, linarith, omega, decide, ...) | 14.1 [12.8, 15.6] | 15.6 [14.3, 16.8] | 8.96 [8.21, 9.71] | 9.95 [8.67, 11.28] |
| conclusion is `∃ C, 0 < C ∧ …` (real-typed ∃ with a `0 < C` or `0 ≤ C` conjunct) | 2.45 [2.07, 2.85] | 3.33 [2.81, 3.91] | 0.41 [0.27, 0.57] | 0.037 [0.000, 0.126] |
| takes a real parameter x together with `0 < x` | 27.8 [26.0, 29.7] | 20.6 [18.5, 22.8] | 46.2 [43.3, 48.7] | 13.9 [8.6, 20.7] |
| P5 % of theorems whose proof rewrites with an equation lemma of a project definition | 3.01 [2.74, 3.28] | 3.28 [2.95, 3.65] | 2.17 [1.82, 2.50] | 9.31 [6.82, 12.07] |
| P5 either | 40.6 [37.6, 43.3] | 40.1 [36.9, 43.3] | 49.3 [46.4, 51.8] | 13.3 [7.7, 19.5] |

## 7. Where the proof mass is: three partitions

Each block is an exclusive partition of the same proof nodes (shares sum to 100 within a block), sorted by the ns share. outer = outermost enclosing side-condition proof; inner = class of the nearest enclosing goal; kind = syntactic position.

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| outer: main argument (not inside any side-condition proof) | 75.2 [74.6, 75.7] | 79.8 [78.2, 81.3] | -4.63 [-6.18, -3.07] | 86.9 [85.6, 88.0] |
| outer: regularity | 13.2 [12.6, 13.8] | 2.21 [1.30, 3.23] | 11.0 [9.8, 12.0] | 0.53 [0.23, 0.91] |
| outer: positivity | 9.23 [9.00, 9.44] | 9.26 [8.54, 10.04] | -0.033 [-0.853, 0.703] | 6.27 [5.42, 7.18] |
| outer: integrability | 1.66 [1.51, 1.81] | 3.01 [2.42, 3.71] | -1.35 [-2.05, -0.74] | 0.19 [0.12, 0.28] |
| outer: measurability | 0.51 [0.47, 0.55] | 3.92 [3.10, 4.80] | -3.41 [-4.31, -2.60] | 4.87 [4.10, 5.74] |
| outer: support | 0.16 [0.13, 0.19] | 0.021 [0.004, 0.041] | 0.14 [0.11, 0.18] | 0.00 [0.00, 0.00] |
| outer: finiteness | 0.074 [0.061, 0.087] | 1.76 [1.40, 2.22] | -1.69 [-2.15, -1.33] | 1.22 [0.99, 1.48] |

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| inner: eq | 53.5 [53.1, 53.9] | 58.7 [57.9, 59.6] | -5.21 [-6.21, -4.28] | 68.5 [66.9, 70.1] |
| inner: order | 8.69 [8.52, 8.85] | 13.5 [13.0, 13.9] | -4.79 [-5.29, -4.28] | 7.75 [7.09, 8.42] |
| inner: tc | 7.62 [7.47, 7.76] | 2.80 [2.68, 2.93] | 4.82 [4.62, 5.00] | 1.34 [1.18, 1.49] |
| inner: regularity | 5.93 [5.77, 6.08] | 0.32 [0.24, 0.40] | 5.61 [5.43, 5.78] | 0.18 [0.09, 0.31] |
| inner: cert | 5.91 [5.79, 6.04] | 4.57 [4.22, 4.94] | 1.34 [0.95, 1.71] | 4.29 [3.61, 4.87] |
| inner: logic | 5.10 [4.93, 5.29] | 5.91 [5.54, 6.29] | -0.81 [-1.23, -0.41] | 5.31 [4.60, 6.05] |
| inner: positivity | 4.17 [4.10, 4.24] | 3.49 [3.31, 3.68] | 0.67 [0.48, 0.87] | 2.01 [1.77, 2.26] |
| inner: other | 3.91 [3.78, 4.03] | 1.12 [0.97, 1.28] | 2.79 [2.59, 2.98] | 0.78 [0.59, 1.02] |
| inner: mem | 2.47 [2.39, 2.54] | 4.79 [4.43, 5.16] | -2.32 [-2.70, -1.95] | 2.95 [2.49, 3.58] |
| inner: limit | 1.41 [1.36, 1.48] | 0.65 [0.54, 0.76] | 0.76 [0.64, 0.89] | 0.73 [0.54, 0.96] |
| inner: measurability | 0.48 [0.45, 0.50] | 2.29 [2.06, 2.53] | -1.82 [-2.06, -1.57] | 3.43 [2.96, 4.01] |
| inner: integrability | 0.46 [0.43, 0.49] | 0.88 [0.77, 1.01] | -0.42 [-0.55, -0.30] | 0.11 [0.07, 0.16] |
| inner: topo | 0.22 [0.21, 0.23] | 0.24 [0.19, 0.31] | -0.024 [-0.095, 0.036] | 0.016 [0.007, 0.030] |
| inner: support | 0.081 [0.070, 0.094] | 0.037 [0.023, 0.053] | 0.044 [0.025, 0.063] | 0.00 [0.00, 0.00] |
| inner: finiteness | 0.050 [0.044, 0.056] | 0.70 [0.62, 0.79] | -0.65 [-0.74, -0.57] | 0.94 [0.77, 1.11] |
| inner: prob | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 0.00 [0.00, 0.00] | 1.65 [1.40, 1.92] |

| | ns (machine) | Carleson (human) | ns − Carleson | PFR (human) |
|---|---|---|---|---|
| kind: proof spine | 41.6 [41.3, 42.0] | 46.7 [45.7, 47.8] | -5.11 [-6.19, -4.01] | 48.2 [45.3, 50.5] |
| kind: inside a term argument | 31.3 [31.1, 31.5] | 36.7 [35.9, 37.4] | -5.42 [-6.23, -4.63] | 42.6 [40.3, 45.3] |
| kind: inside an instance argument | 27.1 [26.8, 27.4] | 16.6 [16.1, 17.1] | 10.5 [9.9, 11.1] | 9.25 [8.78, 9.70] |

## 8. Examples

Selection rule (no hand-picking): among theorems matching the stated predicate whose stored statement is complete and at most 420 characters, sort by the SHA-1 of the theorem name and take the first five. Statements are the pretty-printed text stored by the earlier export, shown for reading only; the predicates were evaluated on the `Expr`. The length cap biases the examples towards short statements; the share that passes it is given.

### A: conclusion `∃ C, 0 < C ∧ …`

**ns**: 946 theorems match, 186 within the length cap.

- `NavierStokes.PositiveRepresentatives`
  ```lean
  NavierStokes.PositiveRepresentatives.compact_jet_bound.{u_1} {E : Type u_1} [NormedAddCommGroup E]
    [NormedSpace ℝ E] {K : Set NavierStokes.PositiveRepresentatives.Slow} (hK : IsCompact K)
    {f : NavierStokes.PositiveRepresentatives.Slow → E} (hf : ∀ p ∈ K, ContDiffAt ℝ (↑⊤) f p)
    (n : ℕ) : ∃ C, 0 < C ∧ ∀ p ∈ K, ‖iteratedFDeriv ℝ n f p‖ ≤ C
  ```
- `NavierStokes.OutgoingPulseBounds`
  ```lean
  NavierStokes.OutgoingPulseBounds.exists_mainPulse_bound :
    ∃ C, 0 < C ∧ ∀ (z : ℝ), |NavierStokes.OutgoingSchedule.mainPulse z| ≤ C
  ```
- `NavierStokes.StressActivation`
  ```lean
  NavierStokes.StressActivation.compact_parameter_jet_bound {J K : Set ℝ} (hJ : IsOpen J)
    (hK : IsCompact K) (hKJ : K ⊆ J) {H : NavierStokes.StressActivation.FamilyPoint → ℝ}
    (hH : ContDiffOn ℝ (↑⊤) H (Set.univ ×ˢ J)) (T : ℝ) (n : ℕ) :
    ∃ M,
      0 ≤ M ∧
        ∀ κ ∈ Set.Icc 0 1,
          ∀ y ∈ Set.Icc 0 T, ∀ η ∈ K, |iteratedDeriv n (fun ξ => H ((κ, y), ξ)) η| ≤ M
  ```
- `Euler.VolterraUniqueness`
  ```lean
  EulerSobolevHeat.exists_positive_time_budget (ν M L margin Tmax : ℝ) (hmargin : 0 < margin)
    (hTmax : 0 < Tmax) :
    ∃ T,
      0 < T ∧
        T ≤ Tmax ∧
          (T + 2 * EulerSobolevHeat.parabolicConstant ν * √T) * M < margin ∧
            (T + 2 * EulerSobolevHeat.parabolicConstant ν * √T) * L < 1
  ```
- `Euler.MeanBoundaryDerivative`
  ```lean
  EulerMeanBoundary.Cutoff.exists_taylor_controls (χ : EulerMeanBoundary.Cutoff) :
    ∃ R M₂ M₃,
      0 ≤ M₂ ∧
        0 ≤ M₃ ∧
          tsupport χ.field ⊆ Metric.closedBall 0 R ∧
            (∀ (x : EulerSmoothLimit.Space), ‖fderiv ℝ (fderiv ℝ χ.field) x‖ ≤ M₂) ∧
              ∀ (x : EulerSmoothLimit.Space), ‖fderiv ℝ (fderiv ℝ (fderiv ℝ χ.field)) x‖ ≤ M₃
  ```

**carleson**: 1 theorems match, 1 within the length cap.

- `Carleson.Psi`
  ```lean
  Bornology.IsBounded.exists_bound_of_norm_Ks.{u_1} {X : Type u_1} {a : ℕ} {K : X → X → ℂ}
    [PseudoMetricSpace X] [KernelProofData a K] {A : Set X} (hA : Bornology.IsBounded A) (s : ℤ) :
    ∃ C, 0 ≤ C ∧ ∀ (x y : X), x ∈ A → ‖Ks s x y‖ ≤ C
  ```

### A: positive real parameter in an inequality

**ns**: 1,661 theorems match, 620 within the length cap.

- `Euler.PacketCylinderTermBudget`
  ```lean
  EulerPacketCylinderField.CoefficientBudget.twice_multiplierCost_le {P T : ℝ} [Fact (0 < P)]
    {O : EulerPacketProfileRecursion.Operators} {C : EulerPacketCylinderField.CoefficientData P T O}
    (B : EulerPacketCylinderField.CoefficientBudget C) : 2 * B.multiplierCost ≤ B.termCost
  ```
- `NavierStokes.ReservedPatches`
  ```lean
  NavierStokes.ReservedPatches.right_before_switch (F : NavierStokes.OutgoingProfile.Profile) (XR : ℝ)
    (hXR : 0 < XR) (s : NavierStokes.ReservedPatches.Slot) :
    NavierStokes.ReservedPatches.right F XR s < NavierStokes.OutgoingDilation.switchRadius F XR
  ```
- `NavierStokes.R3.ComparisonGronwall`
  ```lean
  NavierStokesR3.ComparisonGronwall.le_div_radius_of_deriv_le {T K C R : ℝ} {E E' : ℝ → ℝ}
    (hT : 0 ≤ T) (hK : 0 ≤ K) (hC : 0 ≤ C) (hR : 0 < R) (hcont : ContinuousOn E (Set.Icc 0 T))
    (hinitial : E 0 = 0) (hderiv : ∀ t ∈ Set.Ioo 0 T, HasDerivAt E (E' t) t)
    (hbound : ∀ t ∈ Set.Ioo 0 T, E' t ≤ K * E t + C / R) (t : ℝ) :
    t ∈ Set.Icc 0 T → E t ≤ C * T * Real.exp (K * T) / R
  ```
- `NavierStokes.ReservedPatches`
  ```lean
  NavierStokes.ReservedPatches.left_lt_right (F : NavierStokes.OutgoingProfile.Profile) (XR : ℝ)
    (hXR : 0 < XR) (s : NavierStokes.ReservedPatches.Slot) :
    NavierStokes.ReservedPatches.left F XR s < NavierStokes.ReservedPatches.right F XR s
  ```
- `NavierStokes.SimilarityHomogeneity`
  ```lean
  NavierStokes.SimilarityHomogeneity.physicalScale_time_lt_one {h Q : ℝ} (hQ : 0 < Q)
    {p : NavierStokes.SimilarityProfile.PhysicalPoint} (hp : p.1 < 1) :
    (NavierStokes.SimilarityHomogeneity.physicalScale h Q p).1 < 1
  ```

**carleson**: 113 theorems match, 74 within the length cap.

- `Carleson.Classical.SpectralProjectionBound`
  ```lean
  spectral_projection_bound_lp {N : ℕ} {T : ℝ} [hT : Fact (0 < T)]
    (f : ↥(MeasureTheory.Lp ℂ 2 AddCircle.haarAddCircle)) : ‖partialFourierSumLp 2 N ↑↑f‖ ≤ ‖f‖
  ```
- `Carleson.ToMathlib.WNorm`
  ```lean
  MeasureTheory.iSup_mul_distribution_rpow_le_eLpNorm'.{u_1, u_3} {α : Type u_1} {ε : Type u_3}
    {m : MeasurableSpace α} {μ : MeasureTheory.Measure α} [TopologicalSpace ε] [ContinuousENorm ε]
    {f : α → ε} (hf : MeasureTheory.AEStronglyMeasurable f μ) {p : ℝ} (p0 : 0 < p) :
    ⨆ t, ↑t * MeasureTheory.distribution f (↑t) μ ^ p⁻¹ ≤ MeasureTheory.eLpNorm' f p μ
  ```
- `Carleson.ToMathlib.RealInterpolation.InterpolatedExponents`
  ```lean
  ENNReal.rpow_le_rpow_of_exponent_le_base_ge {a b t γ : ℝ} (hγ : 0 < γ) (htγ : γ ≤ t) (hab : a ≤ b) :
    ENNReal.ofReal (t ^ a) ≤ ENNReal.ofReal (t ^ b) * ENNReal.ofReal (γ ^ (a - b))
  ```
- `Carleson.Classical.ClassicalCarleson`
  ```lean
  exceptional_set_carleson' {f : ℝ → ℂ} (cont_f : Continuous f)
    (periodic_f : Function.Periodic f (2 * Real.pi)) {δ ε : NNReal} (δpos : 0 < δ) (εpos : 0 < ε) :
    ∃ N₀,
      MeasureTheory.distribution (fun x ↦ ⨆ N, ⨆ (_ : N > N₀), ‖f x - partialFourierSum N f x‖ₑ) (↑δ)
          (MeasureTheory.volume.restrict (Set.Ioc 0 (2 * Real.pi))) ≤
        ↑ε
  ```
- `Carleson.HolderVanDerCorput`
  ```lean
  iLipENorm_holderApprox_le.{u_1} {X : Type u_1} {a : ℕ} {q : ℝ} {K : X → X → ℂ} {σ₁ σ₂ : X → ℤ}
    {F G : Set X} [MetricSpace X] [ProofData a q K σ₁ σ₂ F G] {z : X} {R t : ℝ} (ht : 0 < t)
    (h't : t ≤ 1) {φ : X → ℂ} (hφ : Function.support φ ⊆ Metric.ball z R) :
    iLipENorm (holderApprox R t φ) z (2 * R) ≤
      2 ^ (4 * a) * ENNReal.ofReal t ^ (-1 - ↑a) * iHolENorm φ z (2 * R) (defaultτ a)
  ```

### B: statement with a cast or a finiteness fact

**ns**: 324 theorems match, 99 within the length cap.

- `Euler.EulerProof`
  ```lean
  EulerPressureSpatialRegularity.uniform_derivative_remainder.{u_3} {W : Type u_3}
    [NormedAddCommGroup W] [NormedSpace ℝ W] (f f' : ℝ → W) (hf : ∀ (s : ℝ), HasDerivAt f (f' s) s)
    (L : NNReal) (hL : ∀ (s : ℝ), ‖f' s - f' 0‖ ≤ ↑L * |s|) (t : ℝ) :
    ‖f t - f 0 - t • f' 0‖ ≤ ↑L * |t| ^ 2
  ```
- `Euler.ComparatorSingularityNorms`
  ```lean
  Euler.ComparatorBridge.velocityC1Norm_eq
    (A : EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space) :
    Euler.velocityC1Norm A.field =
      ENNReal.ofReal
        (‖EulerMeanSobolevBoundedField.finiteField A‖ +
          ‖EulerMeanSobolevBoundedField.finiteField A.derivative‖)
  ```
- `Euler.MeanScaledBoundaryGevrey`
  ```lean
  EulerMeanBoundary.closedBall_volume_oneThird (R : ℝ) (hR : 0 ≤ R) :
    (MeasureTheory.volume (Metric.closedBall 0 R)).toReal ^ (1 / 3) =
      R * EulerMeanBoundary.cutoffUnitBallFactor
  ```
- `Euler.BoundedLipschitzFlow`
  ```lean
  EulerBoundedLipschitzFlow.Data.flow_distance_initial.{u_1} {E : Type u_1} [NormedAddCommGroup E]
    [NormedSpace ℝ E] [CompleteSpace E] (V : EulerBoundedLipschitzFlow.Data E) (s t : ℝ) (x y : E) :
    dist (V.flow s t x) (V.flow s t y) ≤ dist x y * Real.exp (↑V.lipschitzConstant * |t - s|)
  ```
- `Euler.EulerC1Limsup`
  ```lean
  EulerOrdinarySobolev.FiniteLifespan.maximalC1Norm_limsup_atTop
    {A : EulerLpTranslation.SmoothL2Field EulerSmoothLimit.Space}
    (L : EulerOrdinarySobolev.FiniteLifespan A) :
    Filter.limsup (fun t => ENNReal.ofReal (L.maximalC1Norm t)) Filter.atTop = ⊤
  ```

**carleson**: 713 theorems match, 446 within the length cap.

- `Carleson.ToMathlib.Analysis.RCLike.Components`
  ```lean
  RCLike.nnnorm_ofReal.{u_1} {𝕂 : Type u_1} [RCLike 𝕂] {a : NNReal} : a = ‖↑↑a‖₊
  ```
- `Carleson.LipschitzNorm`
  ```lean
  continuous_of_iLipENorm_ne_top.{u_1, u_2} {𝕜 : Type u_1} {X : Type u_2} [MetricSpace X]
    [NormedField 𝕜] {z : X} {R : ℝ} {φ : X → 𝕜} (hφ : tsupport φ ⊆ Metric.ball z R)
    (h'φ : iLipENorm φ z R ≠ ⊤) : Continuous φ
  ```
- `Carleson.ToMathlib.Analysis.RCLike.Components`
  ```lean
  RCLike.component_one_add_neg_one✝.{u_1} {𝕂 : Type u_1} [RCLike 𝕂] (a : 𝕂) :
    (algebraMap ℝ 𝕂) ↑(RCLike.component 1 a) + -1 * (algebraMap ℝ 𝕂) ↑(RCLike.component (-1) a) =
      (algebraMap ℝ 𝕂) (RCLike.re a)
  ```
- `Carleson.Classical.ControlApproximationEffectContinuous`
  ```lean
  C_distribution_carlesonOperatorReal_le'_property {δ ε : NNReal} (δpos : 0 < δ) :
    ↑ε =
      ↑(C_distribution_carlesonOperatorReal_le' δ ε) ^ 2 * ↑(C10_0_1 4 2) ^ 2 *
          ENNReal.ofReal (2 * Real.pi + 2) /
        ↑δ ^ 2
  ```
- `Carleson.ToMathlib.Misc`
  ```lean
  MeasureTheory.toReal_ofReal_preimage {s : Set ENNReal} :
    s =
      if ⊤ ∈ s ↔ 0 ∈ s then ENNReal.toReal ⁻¹' ENNReal.ofReal ⁻¹' s
      else
        if 0 ∈ s then ENNReal.toReal ⁻¹' ENNReal.ofReal ⁻¹' s \ {⊤}
        else ENNReal.toReal ⁻¹' ENNReal.ofReal ⁻¹' s ∪ {⊤}
  ```

### C: statement with indicator / restrict / support / cutoff

**ns**: 3,275 theorems match, 1,562 within the length cap.

- `NavierStokes.ActualCoreSupport`
  ```lean
  NavierStokes.ActualCoreSupport.cut_pressure_mem_refined {B N0 : ℕ}
    (l : NavierStokes.ActualCoreSupport.Index B N0) (n : ℕ)
    {x : NavierStokes.CorrectionInitialization.ActualPrimary.FullPoint} (hT : 0 < x.1.2.1.1)
    (hx :
      x ∈
        Function.support
          ((NavierStokes.ActualInitialization.primaryPiece l).exactCoefficients.pressure n)) :
    x.1 ∈ NavierStokes.ActualCoreSupport.refinedCarrier l n
  ```
- `Euler.PacketTerminalDatum`
  ```lean
  EulerPacketTerminalDatum.scalarField_coe (δ : ℝ) (y : EulerSmoothLimit.Space) (θ : ℝ) :
    EulerPacketTerminalDatum.scalarField δ (y, ↑θ) =
      EulerSpatialCutoffs.innerCutoff y * EulerPeriodicProfile.profile δ θ
  ```
- `NavierStokes.SmoothCutoffs`
  ```lean
  NavierStokes.SmoothCutoffs.cutoff_iteratedDeriv_zero_inside (n : ℕ) {x : ℝ} (hx : |x| < 1 / 2) :
    iteratedDeriv (n + 1) NavierStokes.SmoothCutoffs.cutoff x = 0
  ```
- `NavierStokes.SquaredPartition`
  ```lean
  NavierStokes.SquaredPartition.labelMask_locallyFinite :
    LocallyFinite fun p =>
      Function.support fun z => NavierStokes.SquaredPartition.labelMask p.1 p.2 (↑z.1, z.2)
  ```
- `NavierStokes.PressureDatum`
  ```lean
  NavierStokes.PressureDatum.pressure_le_prefix {g a : ℝ → ℝ} {A b : ℝ}
    (h : NavierStokes.PressureDatum.Admissible g a A) {s : Set ℝ} (hs : MeasurableSet s)
    (ha : ∀ y ∈ s, a y = b) (η : ℝ) :
    NavierStokes.PressureDatum.pressure g a η ≤
      -(1 / 2) * NavierStokes.PressureDatum.kernel b η * ∫ (y : ℝ) in s, g y
  ```

**carleson**: 418 theorems match, 229 within the length cap.

- `Carleson.LipschitzNorm`
  ```lean
  continuous_of_iLipENorm_ne_top.{u_1, u_2} {𝕜 : Type u_1} {X : Type u_2} [MetricSpace X]
    [NormedField 𝕜] {z : X} {R : ℝ} {φ : X → 𝕜} (hφ : tsupport φ ⊆ Metric.ball z R)
    (h'φ : iLipENorm φ z R ≠ ⊤) : Continuous φ
  ```
- `Carleson.ToMathlib.BoundedFiniteSupport`
  ```lean
  BoundedFiniteSupport.aemeasurable_restrict.{u_1, u_2} {X : Type u_1} {E : Type u_2}
    [MeasurableSpace X] {f : X → E} {μ : MeasureTheory.Measure X} [TopologicalSpace E] [ENorm E]
    [Zero E] (bfs : BoundedFiniteSupport f μ) [MeasurableSpace E]
    [TopologicalSpace.PseudoMetrizableSpace E] [BorelSpace E] {s : Set X} :
    AEMeasurable f (μ.restrict s)
  ```
- `Carleson.ToMathlib.Distribution`
  ```lean
  MeasureTheory.distribution_indicator_eq.{u_1, u_13} {α : Type u_1} {m : MeasurableSpace α}
    {μ : MeasureTheory.Measure α} {x : ENNReal} {ε : Type u_13} [TopologicalSpace ε]
    [ESeminormedAddMonoid ε] {f : α → ε} {X : Set α} :
    MeasureTheory.distribution (X.indicator f) x μ = μ (X ∩ MeasureTheory.superlevelSet f x)
  ```
- `Carleson.ToMathlib.Misc`
  ```lean
  Function.support_ofNNReal : Function.support ENNReal.ofNNReal = Set.Ioi 0
  ```
- `Carleson.ToMathlib.Rearrangement`
  ```lean
  MeasureTheory.setLIntegral_enorm_le_lintegral_rearrangement.{u_1, u_4} {α : Type u_1}
    {m : MeasurableSpace α} {μ : MeasureTheory.Measure α} {ε : Type u_4} [TopologicalSpace ε]
    [ENormedAddMonoid ε] {f : α → ε} (hf : MeasureTheory.AEStronglyMeasurable f μ) {X : Set α}
    (hX : MeasurableSet X) :
    ∫⁻ (x : α) in X, ‖f x‖ₑ ∂μ ≤ ∫⁻ (t : ENNReal) in Set.Iio (μ X), MeasureTheory.rearrangement f t μ
  ```

### D: measurability or integrability hypothesis

**ns**: 1,062 theorems match, 249 within the length cap.

- `NavierStokes.PressureDatum`
  ```lean
  NavierStokes.PressureDatum.pressure_le_prefix {g a : ℝ → ℝ} {A b : ℝ}
    (h : NavierStokes.PressureDatum.Admissible g a A) {s : Set ℝ} (hs : MeasurableSet s)
    (ha : ∀ y ∈ s, a y = b) (η : ℝ) :
    NavierStokes.PressureDatum.pressure g a η ≤
      -(1 / 2) * NavierStokes.PressureDatum.kernel b η * ∫ (y : ℝ) in s, g y
  ```
- `NavierStokes.R3ConvolutionYoung`
  ```lean
  NavierStokes.R3ConvolutionYoung.majorant_young_two_one
    {f g : NavierStokes.ProblemStatement.Space → ENNReal} (hf : Measurable f) (hg : Measurable g) :
    ∫⁻ (x : NavierStokes.ProblemStatement.Space), NavierStokes.R3ConvolutionYoung.majorant f g x ^ 2 ≤
      (∫⁻ (y : NavierStokes.ProblemStatement.Space), f y ^ 2) *
        (∫⁻ (z : NavierStokes.ProblemStatement.Space), g z) ^ 2
  ```
- `Euler.OrdinarySobolevL4`
  ```lean
  EulerOrdinarySobolev.square_memLp.{u_2} {E : Type u_2} [NormedAddCommGroup E]
    {f : EulerSmoothLimit.Space → E} (h2 : MeasureTheory.MemLp f 2 MeasureTheory.volume)
    (h6 : MeasureTheory.MemLp f 6 MeasureTheory.volume) :
    MeasureTheory.MemLp (fun x => ‖f x‖ ^ 2) 2 MeasureTheory.volume
  ```
- `NavierStokes.ExtendedHeatDebts`
  ```lean
  NavierStokes.ExtendedHeatDebts.chain_integrable.{u_1} {α : Type u_1} [MeasurableSpace α]
    {μ : MeasureTheory.Measure α} {J : ℕ → ℝ → α → ℝ}
    (hm : ∀ (n : ℕ) (ν : ℝ), MeasureTheory.AEStronglyMeasurable (J n ν) μ)
    (hb : NavierStokes.ExtendedHeatDebts.ChainDominated J μ) (n : ℕ) (ν : ℝ) :
    MeasureTheory.Integrable (J n ν) μ
  ```
- `NavierStokes.R3.H3WeakEmbedding`
  ```lean
  NavierStokesR3.H3Embedding.squareEnergy_eq_norm_toLp
    {f : NavierStokes.ProblemStatement.Space → NavierStokes.ProblemStatement.Space}
    (hf : MeasureTheory.MemLp f 2 MeasureTheory.volume) :
    NavierStokesR3.H3Embedding.squareEnergy f = ‖MeasureTheory.MemLp.toLp f hf‖ ^ 2
  ```

**carleson**: 581 theorems match, 332 within the length cap.

- `Carleson.ToMathlib.BoundedCompactSupport`
  ```lean
  MeasureTheory.BoundedCompactSupport.norm.{u_1, u_2} {X : Type u_1} {E : Type u_2}
    [TopologicalSpace X] [MeasurableSpace X] {μ : MeasureTheory.Measure X} {f : X → E}
    [NormedAddCommGroup E] (hf : MeasureTheory.BoundedCompactSupport f μ) :
    MeasureTheory.BoundedCompactSupport (fun x ↦ ‖f x‖) μ
  ```
- `Carleson.ToMathlib.BoundedFiniteSupport`
  ```lean
  BoundedFiniteSupport.aemeasurable_restrict.{u_1, u_2} {X : Type u_1} {E : Type u_2}
    [MeasurableSpace X] {f : X → E} {μ : MeasureTheory.Measure X} [TopologicalSpace E] [ENorm E]
    [Zero E] (bfs : BoundedFiniteSupport f μ) [MeasurableSpace E]
    [TopologicalSpace.PseudoMetrizableSpace E] [BorelSpace E] {s : Set X} :
    AEMeasurable f (μ.restrict s)
  ```
- `Carleson.ToMathlib.Rearrangement`
  ```lean
  MeasureTheory.setLIntegral_enorm_le_lintegral_rearrangement.{u_1, u_4} {α : Type u_1}
    {m : MeasurableSpace α} {μ : MeasureTheory.Measure α} {ε : Type u_4} [TopologicalSpace ε]
    [ENormedAddMonoid ε] {f : α → ε} (hf : MeasureTheory.AEStronglyMeasurable f μ) {X : Set α}
    (hX : MeasurableSet X) :
    ∫⁻ (x : α) in X, ‖f x‖ₑ ∂μ ≤ ∫⁻ (t : ENNReal) in Set.Iio (μ X), MeasureTheory.rearrangement f t μ
  ```
- `Carleson.ToMathlib.BoundedCompactSupport`
  ```lean
  MeasureTheory.BoundedCompactSupport.sub.{u_1, u_2} {X : Type u_1} {E : Type u_2}
    [TopologicalSpace X] [MeasurableSpace X] {μ : MeasureTheory.Measure X} {f : X → E}
    [NormedAddCommGroup E] {g : X → E} (hf : MeasureTheory.BoundedCompactSupport f μ)
    (hg : MeasureTheory.BoundedCompactSupport g μ) : MeasureTheory.BoundedCompactSupport (f - g) μ
  ```
- `Carleson.ToMathlib.IntegralBallContinuity`
  ```lean
  MeasureTheory.LocallyIntegrable.integrableOn_of_isBounded.{u_1, u_2} {X : Type u_1} {E : Type u_2}
    [MeasurableSpace X] [PseudoMetricSpace X] [NormedAddCommGroup E] {μ : MeasureTheory.Measure X}
    [ProperSpace X] {f : X → E} (hf : MeasureTheory.LocallyIntegrable f μ) {s : Set X}
    (hs : Bornology.IsBounded s) : MeasureTheory.IntegrableOn f s μ
  ```

### D: regularity hypothesis (ContDiff, Continuous, HasDerivAt, …)

**ns**: 7,993 theorems match, 2,544 within the length cap.

- `NavierStokes.PositiveRepresentatives`
  ```lean
  NavierStokes.PositiveRepresentatives.compact_jet_bound.{u_1} {E : Type u_1} [NormedAddCommGroup E]
    [NormedSpace ℝ E] {K : Set NavierStokes.PositiveRepresentatives.Slow} (hK : IsCompact K)
    {f : NavierStokes.PositiveRepresentatives.Slow → E} (hf : ∀ p ∈ K, ContDiffAt ℝ (↑⊤) f p)
    (n : ℕ) : ∃ C, 0 < C ∧ ∀ p ∈ K, ‖iteratedFDeriv ℝ n f p‖ ≤ C
  ```
- `NavierStokes.InitialDyadicSource`
  ```lean
  NavierStokes.InitialDyadicSource.flat_mul_left.{u_1} {D : Type u_1} [NormedAddCommGroup D]
    [NormedSpace ℝ D] {f g : D → ℂ} {x : D} (hf : NavierStokes.NativeDyadicRegularity.FlatAt f x)
    (hg : ContDiffAt ℝ (↑⊤) g x) : NavierStokes.NativeDyadicRegularity.FlatAt (fun y => f y * g y) x
  ```
- `Euler.PacketJetAssembly`
  ```lean
  EulerPacketPointJets.differentiableAt_truncate.{u_1} {E : Type u_1} [NormedAddCommGroup E]
    [NormedSpace ℝ E] (N n : ℕ) (u : ℕ → EulerPacketPointJets.Domain → E)
    (z : EulerPacketPointJets.Domain) (hu : ∀ i ≤ N, DifferentiableAt ℝ (u i) z) :
    DifferentiableAt ℝ (EulerFiniteGrades.truncate N u n) z
  ```
- `NavierStokes.WaveInteractionBounds`
  ```lean
  NavierStokes.WaveInteractionBounds.mul_along_zero.{u_1} {D : Type u_1} [NormedAddCommGroup D]
    [NormedSpace ℝ D] {U : Set D} (hU : IsOpen U) {f g : D → ℂ} {x : D} (hx : x ∈ U)
    (hf : ContinuousAt f x) (hfg : ∀ y ∈ U, f y * g y = 0) (V : D → D) :
    f x * NavierStokes.HarmonicCalculus.along V g x = 0
  ```
- `NavierStokes.SmoothFamilyTorusInverse`
  ```lean
  NavierStokes.SmoothFamilyTorusInverse.nonbarPart_zeroMean {P : Type} [NormedAddCommGroup P]
    [NormedSpace ℝ P] {f : NavierStokes.SmoothFamilyTorusInverse.Source P} (hf : ContDiff ℝ (↑⊤) f)
    (hp : NavierStokes.SmoothFamilyTorusInverse.Periodic f) :
    NavierStokes.SmoothFamilyTorusInverse.ZeroMean
      (NavierStokes.SmoothFamilyTorusInverse.nonbarPart f)
  ```

**carleson**: 27 theorems match, 20 within the length cap.

- `Carleson.Classical.CarlesonOperatorReal`
  ```lean
  sup_eq_sup_dense_of_continuous {f : ℝ → ENNReal} {S : Set ℝ} (D : Set ℝ) (hS : IsOpen S)
    (hD : Dense D) (hf : ContinuousOn f S) : ⨆ r ∈ S, f r = ⨆ r ∈ S ∩ D, f r
  ```
- `Carleson.Classical.Approximation`
  ```lean
  fourierCoeffOn_ContDiff_two_bound {f : ℝ → ℂ} (periodicf : Function.Periodic f (2 * Real.pi))
    (fdiff : ContDiff ℝ 2 f) :
    ∃ C, ∀ (n : ℤ), n ≠ 0 → ‖fourierCoeffOn Real.two_pi_pos f n‖ ≤ C / ↑n ^ 2
  ```
- `Carleson.Classical.ClassicalCarleson`
  ```lean
  exceptional_set_carleson' {f : ℝ → ℂ} (cont_f : Continuous f)
    (periodic_f : Function.Periodic f (2 * Real.pi)) {δ ε : NNReal} (δpos : 0 < δ) (εpos : 0 < ε) :
    ∃ N₀,
      MeasureTheory.distribution (fun x ↦ ⨆ N, ⨆ (_ : N > N₀), ‖f x - partialFourierSum N f x‖ₑ) (↑δ)
          (MeasureTheory.volume.restrict (Set.Ioc 0 (2 * Real.pi))) ≤
        ↑ε
  ```
- `Carleson.Classical.Approximation`
  ```lean
  close_smooth_approx_periodic {T : ℝ} {f : ℝ → ℂ} (unicontf : UniformContinuous f)
    (periodicf : Function.Periodic f T) {ε : ℝ} (εpos : ε > 0) :
    ∃ f₀, ContDiff ℝ (↑⊤) f₀ ∧ Function.Periodic f₀ T ∧ ∀ (x : ℝ), ‖f x - f₀ x‖ ≤ ε
  ```
- `Carleson.ToMathlib.Topology.ContinuousOn`
  ```lean
  eLpNormEssSup_eq_iSup' {f : ENNReal → ENNReal}
    (hf : ∀ (a x : ENNReal), a < f x → ContinuousWithinAt f (Set.Ioi x) x) (f_top : f ⊤ = ⊥) :
    MeasureTheory.eLpNormEssSup f MeasureTheory.volume = ⨆ x, f x
  ```

