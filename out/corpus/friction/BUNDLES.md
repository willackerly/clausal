# Packets: mined bundles and one kernel-checked experiment

**Verdict: marginal as tested.** Bundling hypotheses into structures, applied mechanically to existing statements and proofs, does not compress this corpus materially. Whether proofs written against a packet-level API would be shorter was not tested.

**Revised 2026-11-10 after an adversarial review**: the ceiling, the "proofs do not shrink" line and the "chat's packet is rare" line were overstated, and the headline savings were gross of the glue. Changed lines are marked "revised".

- **Whole corpus (ns):** turning the 10 best bundles into structures removes 1.5–2.5% of hypotheses and 0.6–1.0% of statement nodes. Turning the best 100 into structures removes 7–8.5% of hypotheses and under 2% of nodes.
- **Ceiling for side-condition-only bundles (revised):** merging every side-condition hypothesis of every theorem into one would remove 21% of hypotheses and 8% of statement nodes. This is not a ceiling for packets in general: it leaves out order and equation hypotheses (the top bundle below contains a coercivity inequality), data binders, hypotheses over 3,000 nodes, and the 3,300 theorems over 100,000 statement nodes that hold nearly all statement mass.
- **Where the saving comes from:** 98–99% of the node saving is from giving a large hypothesis a name. Merging hypotheses into one token contributes 1–2%.
- **Inside one lemma family the effect is real but smaller net of glue (revised):** in the nine-theorem cluster tested, statements shrink 16.5% gross and 10.4% once the structure declaration is counted (5.7% if the 17 wrapper definitions are also counted), hypotheses go from 83 to 56 and explicit arguments from 161 to 98. The cluster is the module with the most carriers of the top bundle, so this is a best case.
- **A mechanical port grows proofs by 7.6% (revised):** the nine proofs were re-proved by a scripted rename in which every lemma outside the cluster still takes the four facts separately, so the packet is opened at each use (6,174 projection occurrences). Growth is a consequence of that design. Proofs redesigned around a packet-level API were not written, so "packets do not shorten proofs" is not established.
- **The chat's literal packet is rare among loose hypotheses, but the machine corpus built packets of its own (revised).** A function with its measurability, integrability and finiteness is almost absent in ns, because little of ns is integration. What recurs among loose hypotheses is the standing assumptions of a lemma family: a few constants, their signs, one coercivity bound and one derivative fact. Separately, and missed by the mining because each is a single hypothesis: 6.41% of all ns hypotheses are a project-defined predicate that contains a smoothness fact, and 2.84% one that pairs smoothness with a hidden `∃ C` bound (`MemClass`, `MeanClass`, `UniformClass`, `PolynomialJets`; `ROBUSTNESS.md` section 5). Those are function-with-facts packets, written by the machine, carrying smoothness and bounds instead of measurability and integrability.

Worth pursuing: a Prop-valued "context" structure for a lemma family's shared hypotheses, with the data left as parameters, and plain definitions that name large recurring hypotheses. Not worth pursuing as a compression device: function-plus-regularity packets, and packet-level wrappers for every operation.

Everything below is read from the built environments at `Expr` level. ns is the machine-written corpus; Carleson is the human one.

## 1. Mining

### Method

- **Atom:** a Prop-valued binder, split through top-level `∧`. Conclusions are split through `∧` and `∃`.
- **Per-variable bundle:** two or more atoms about the same variable, with that variable written `$` and other variables anonymised. These are mined exhaustively (closed frequent itemsets).
- **Variable-group bundle:** two or more atoms that recur with the same binder names across theorems. This is a greedy search from every frequent atom, not exhaustive. Binder names are read from the environment.
- **Saving:** the atoms' binders are replaced by one binder of type `P x₁ … xₙ`, where the `xᵢ` are all variables the atoms mention. Measured in tree nodes, the same measure as `statementSize`.
- **Minimum support:** 20 instances in ns, 5 in Carleson.
- **Bundles kept:** those with at least one side-condition atom ("mixed"), reported next to those whose atoms are all side conditions ("strict").
- **Top-10 selection:** greedy, each atom consumed by one bundle only.

Statement sizes in ns are extremely skewed (median 477 nodes, largest 2.4 × 10¹⁰), so node shares are given for theorems of at most 100,000 nodes (35,301 of 38,601 theorems, 110.6 M nodes).

### Upper bounds

| | ns | Carleson |
|---|---|---|
| hypotheses (Prop binders) | 105,257 | 4,798 |
| side-condition atoms among them | 43,226 | 1,789 |
| top 10 variable-group bundles: hypotheses removed | 2,618 (2.5%) | 380 (7.9%) |
| … statement nodes removed | 0.61% | 1.55% |
| … theorems touched | 1,222 (3.2%) | 145 (5.4%) |
| top 10 per-variable bundles: hypotheses removed | 1,554 (1.5%) | 294 (6.1%) |
| … statement nodes removed | 0.96% | 0.55% |
| top 10, strict side-condition bundles only: hypotheses removed | 519–585 (0.5–0.6%) | 79–90 (1.6–1.9%) |
| top 100 bundles: hypotheses removed | 7,392–8,915 (7.0–8.5%) | 457–676 (9.5–14.1%) |
| … statement nodes removed | 1.0–1.7% | 0.7–1.9% |
| ceiling, all side conditions of a theorem as one hypothesis: hypotheses removed | 22,516 (21.4%) | 760 (15.8%) |
| … statement nodes removed | 7.8% | 1.0% |
| share of the top-10 node saving that is naming, not merging | 98–99% | 95–96% |

Carleson has only 40 bundles above its support threshold, so its "top 100" row is all of them. Node shares for Carleson are over all 2,675 theorems.

### Top 10 bundles in ns (variable groups, by total saving)

| # | bundle | theorems | nodes saved | hypotheses removed | already a structure? | in a conclusion as a whole? |
|---|---|---|---|---|---|---|
| 1 | frame: `0 ≤ T`, `0 < c`, coercivity `c‖v‖² ≤ ‖Q t v‖²`, `Q₁` is the derivative of `Q` on `[0,T]` (plus two `CompleteSpace` instances) | 109 | 463,032 | 545 | no | 0 |
| 2 | `Fact (0 < period)`, `0 < c`, coercivity on the lifted domain | 67 | 112,828 | 134 | no | 0 |
| 3 | `0 < h`, `h < 1/2` | 853 | 78,476 | 853 | yes, `NavierStokes.CycleStateCoherence.Geometry` | 0 |
| 4 | `0 ≤ T`, `0 < c`, `0 < cm`, `MeasurableSet S`, lower bound by `cm` on `[0,T]` | 21 | 57,456 | 105 | no | 0 |
| 5 | 19 hypotheses of the transverse-packet "join" budget | 25 | 49,100 | 450 | no (its parts are project structures) | 0 |
| 6 | `Fact (0 < period)`, operator-norm bound on four coefficients | 60 | 44,040 | 60 | no | 0 |
| 7 | 16 hypotheses of the transverse-packet "forward" budget | 21 | 39,102 | 315 | no (its parts are project structures) | 0 |
| 8 | `0 ≤ T`, uniform bound on a sequence of paths | 21 | 35,280 | 21 | no | 0 |
| 9 | `0 < c`, parametrised coercivity `∀ P, …` | 23 | 31,648 | 69 | no | 0 |
| 10 | `0 < ε`, `ε ≤ …`, two `HasDerivAt` facts on `t ≥ 0` | 22 | 28,336 | 66 | no | 0 |

**The top of both lists is one lemma family (revised).** In the per-variable list, bundles 1, 2, 3, 4, 5 and 7 all contain the same `HasDerivWithinAt … (Icc 0 T)` frame atom, and bundle 8 its coercivity companion; the carriers are 110 theorems in 26 Euler modules (0.3% of theorems). In the table above nine of the ten bundles have between 21 and 109 theorems against a support threshold of 20; only `0 < h, h < 1/2` is widespread. The top 10 is therefore two or three mathematical units, not ten.

The per-variable list is led by the same family: the derivative and coercivity atoms of bundle 1 about the same `Q` occur together in 120 statements (500,640 nodes). Full lists: `ns/bundles/MINING.md`, `carleson/bundles/MINING.md`.

### What the mining shows

- **Bundles are consumed, not produced.** No top-10 bundle appears as a conjunction in any theorem's conclusion. Its atoms are concluded one at a time (for example, 436 theorems conclude some `0 ≤ x`). A packet would have to be assembled by hand at each producer.
- **The most frequent bundle is trivial.** `0 < h ∧ h < 1/2` is in 853 theorems and saves 92 nodes each. The project already has a structure containing it and does not use it in those statements.
- **ns already bundles heavily.** It defines 652 structures, 576 with two or more Prop fields. 18.1% of its data binders (35,158 of 194,052) have a project structure as their type; in Carleson it is 1.4% (201 of 14,692). On this measure the machine corpus does not unfold abstractions that the human corpus keeps.
- **The chat's literal packet is rare in ns; home-made smoothness packets are not (revised).** Measurability is 0.6% of ns hypotheses and integrability 0.9%, and the only top-10 per-variable bundle with a measurability atom has 20 instances. But the mining treats a project predicate as one opaque atom. Opened at Expr level, 258 of the 669 ns project predicates contain a regularity, measurability or integrability fact and 114 hide a real `∃ C` with a sign; 6.41% of ns hypotheses are a predicate with a smoothness fact inside. The machine corpus already bundles a function with its regularity and bound facts where it needs to; what it leaves loose is the lemma-family context.
- **It does occur in Carleson, at small scale.** `Measurable f` with `‖f x‖ ≤ 𝟙_F x` occurs 45 times; `0 < p` with `p ≠ ⊤` 46 times; exponent-interpolation hypotheses 73 times. Carleson already made the obvious packet itself (`BoundedCompactSupport`, `BoundedFiniteSupport`), and those appear here as single atoms.

## 2. Experiment

### Choice of bundle and cluster

- **Bundle:** number 1 above, the best one that no structure in the environment packages. As one hypothesis:

```lean
structure Frame (T : ℝ) (Q Q₁ : C(Icc (0 : ℝ) T, U →L[ℝ] E)) (c : ℝ) : Prop where
  hT : 0 ≤ T
  hc : 0 < c
  hQ : ∀ t v, c * ‖v‖ ^ 2 ≤ ‖Q t v‖ ^ 2
  hd : ∀ t : Icc (0 : ℝ) T, HasDerivWithinAt (extendPath T hT Q) (Q₁ t) (Icc (0 : ℝ) T) t
```

- **Carriers:** 110 theorems in 26 modules carry all four hypotheses about one `(T, Q, Q₁, c)`.
- **Cluster rule, fixed before reading any proof:** rank modules by number of carriers; in the first module whose carriers contain a connected component of at least 8 under "one's proof uses the other", take that component. This gives all 9 carriers of `Euler.FixedEndpointStrong`.
- **The three for direct re-proof:** the ones with most dependencies inside the cluster, ties by source order: `continuousCoordinateVelocity_eq_forward`, `coordinateSlope_ae`, `coordinate_equation`. In the end all nine were re-proved directly.

### What was proved

All in `corpora/friction/packet/`, compiled against the built ns environment, no `sorry`; axioms are `propext`, `Classical.choice`, `Quot.sound` only.

- **`PacketWrap.lean`, restated from original:** all 9 theorems restated with `(F : Frame T Q Q₁ c)` and proved from the originals.
- **`PacketWrap.lean`, original from restated:** all 9 original statements proved from the restated ones. The types are structurally identical to the originals (checked in Lean).
- **`PacketDirect.lean`:** all 9 re-proved against the structure without using any original cluster theorem. This is a mechanical port of the source proofs: 15 calls to cluster lemmas pass `F`; every other lemma still takes the facts one by one.
- **`PacketApi.lean`:** a third restatement in which each operation occurring in the statements gets a packet-level wrapper.

### Measurements

| theorem | statement nodes: original / packet / packet + API | hypotheses | explicit arguments | proof value: original / direct | proof body: original / direct |
|---|---|---|---|---|---|
| `fixedEndpointDerivative_weak` | 44976 / 40938 / 35238 | 8 → 5 | 17 → 10 | 6371 / 6201 | 5150 / 5371 |
| `coordinateSlope_range` | 13807 / 9703 / 4069 | 7 → 4 | 15 → 8 | 2422 / 2117 | 1542 / 1631 |
| `coordinateSlope_ae` | 18589 / 14639 / 8841 | 8 → 5 | 15 → 8 | 1910 / 1577 | 948 / 1031 |
| `coordinate_equation` | 21812 / 18038 / 12080 | 10 → 7 | 19 → 12 | 3191 / 3049 | 1789 / 1949 |
| `coordinateSlope_h1` | 31634 / 27794 / 21902 | 10 → 7 | 18 → 11 | 9034 / 9442 | 7677 / 8387 |
| `continuousCoordinateVelocity_eq` | 21581 / 17653 / 11855 | 10 → 7 | 19 → 12 | 2755 / 2583 | 1319 / 1449 |
| `historyVelocity_eq` | 22779 / 18851 / 13053 | 10 → 7 | 19 → 12 | 2535 / 2319 | 1137 / 1223 |
| `continuousCoordinateVelocity_hasDerivWithinAt_generator` | 19601 / 15651 / 15409 | 10 → 7 | 19 → 12 | 3331 / 3197 | 1920 / 2088 |
| `continuousCoordinateVelocity_eq_forward` | 19007 / 15145 / 14663 | 10 → 7 | 20 → 13 | 2673 / 2484 | 1226 / 1306 |
| **total** | 213786 / 178412 / 137110 | 83 → 56 | 161 → 98 | 34222 / 32969 | 22708 / 24435 |

Proof value is the number of distinct subterms of the whole proof term, the corpus's `proofSize`. Proof body is the same after stripping the leading binders, so it excludes the restated hypotheses.

- **Net of glue (revised):** originals 213,786 statement nodes; packet 178,412 plus 13,160 for the structure, its constructor and projections = 191,572 (−10.4%); packet with API 137,110 plus 13,160 plus 51,295 for the 17 wrappers = 201,565 (−5.7%). The structure cost would amortise to about 120 nodes per theorem over all 110 carriers.
- **Statements, gross:** −16.5% in tree nodes (−14.5% as distinct subterms). The mining formula predicted about 4,210 nodes per theorem; 3,930 were realised (93%). The rest is the cost of `F.hT`, `F.hc`, `F.hQ`, `F.hd` appearing inside the statement, 5 to 20 times per theorem, because every definition in the statement takes those proofs as arguments.
- **Hypotheses:** 3 fewer per theorem, as expected for four-into-one.
- **Explicit arguments:** 7 fewer per theorem. Three are from bundling. Four are `T Q Q₁ c` becoming implicit, which the original could also have done.
- **Proof terms, mechanical port:** the whole value is 3.7% smaller, but only because the binder types are part of it. The body, the actual argument, is 7.6% larger: 24,435 against 22,708. For the three designated theorems the bodies grow 6.5%, 8.8% and 8.9%. This measures the same proofs with the packet opened at each use, not proofs written for the packet.
- **Source text:** 9,249 → 9,379 characters; 1,747 → 1,642 whitespace-separated tokens. Roughly unchanged.
- **Wrappers are pure overhead if the originals stay:** the nine wrappers add 10,383 proof nodes, the nine converses 13,183.
- **Across the corpus:** the predicted saving for all 110 carriers is 463,320 nodes, 9.6% of those theorems' statements and 0.4% of the corpus's statements of at most 100,000 nodes.

### Glue

- **Structure:** one declaration; Lean generates the constructor and four projections (13,160 statement nodes in total).
- **Projection or constructor lemmas written by hand:** none. The converse direction uses the anonymous constructor.
- **Preservation lemmas:** none needed. No operation in this cluster changes `T`, `Q`, `Q₁` or `c`, so the cluster does not test that cost.
- **Packet-level API:** 17 wrapper definitions (51,295 statement nodes) to remove a further 41,302 nodes from nine statements. At nine theorems the wrappers cost more than they save; they could only pay off across the whole 110-theorem family.

### Callers

All 217 applications of the 110 carriers anywhere in the corpus were classified by how the four facts are supplied.

- **175 pass the caller's own four hypotheses straight through.** With a packet these become one argument. Nothing is moved; the saving per call is three arguments.
- **42 build at least one fact.** 26 of those turn `0 < T` into `0 ≤ T`. The rest come from about five places, mainly lemmas about the project structure `EulerCylinderDirichlet.Coefficients`. A packet needs one constructor lemma per such producer.
- **So the bulk does not move into building the structure.** Producers are few and consumers many. But the saving at each call is small, and the corpus already holds this data in a structure at the top and unbundles it for the lemma layer.

### Counter-arguments: which costs were hit

- **Partial reuse: hit, three ways.**
  - 195 statements carry the derivative fact or the coercivity fact; 85 of them (44%) carry only one. Those either keep loose hypotheses, giving two vocabularies, or must assume more than they need.
  - Inside the cluster, `hd₁` is the same derivative fact one level up, for `(Q₁, Q₂)`. There is no coercivity for `Q₁`, so it cannot be a `Frame` and stays a loose hypothesis.
  - Of the 17 operations in the statements, 5 use all four facts, 4 use three, 1 uses two and 7 use only `hT`. A packet-level `F.generator` demands a derivative fact that `generator` does not need.
- **An API lemma per operation: hit.** Without the 17 wrappers the packet is taken apart 207 times in the nine direct proofs, against 15 calls that pass it whole.
- **Blocks rewriting: not hit.** All nine proofs ported by renaming alone; every `rw`, `simp only`, `change` and `filter_upwards` step passes unchanged. No step in this cluster rewrites `T` or `Q`, so this is weak evidence.
- **Deliberate unbundling: the corpus follows the same convention as Mathlib.** Its definitions take the individual proofs as arguments, which is why a packet has to be opened at almost every use.

## Limits

- **Atoms over 3,000 nodes are excluded from mining:** 5,077 of 105,283 hypothesis atoms in ns. Bundles made of very large hypotheses are not seen.
- **Variable-group bundles depend on binder names and on a greedy search.** They are a lower bound on what an exhaustive search would find at the same support.
- **Support thresholds differ between corpora** (20 and 5), so the Carleson and ns rows are not like for like.
- **"Already a structure" is a syntactic match** of a bundle's atoms against the fields of every structure and the conjuncts of every Prop-valued definition in the environment. A structure that states the same facts in a different form is not found; `Coefficients` is such a case for bundle 1.
- **One bundle, one cluster of nine theorems, one module, chosen as the module with most carriers: a best case.** Preservation under operations and rewriting were not exercised by this cluster.
- **Proofs were ported, not redesigned.** No proof was written against packet-level lemmas, so the experiment bounds the cost of a mechanical migration and says nothing about the benefit of a packet-native lemma library.
- **The mining sees a project predicate as one atom.** Bundles the corpus already made (its own predicates and structures) are invisible to it by construction.
- **Sizes are of kernel terms.** They include implicit and instance arguments and say little about how the source reads.

## Files

- **Lean, exporters:** `corpora/friction/Bundles.lean` (telescopes, atoms, structures), `corpora/friction/Callsites.lean` (call-site census), `corpora/friction/bundles_run.sh`.
- **Lean, experiment:** `corpora/friction/packet/Packet{Frame,Wrap,Direct,Api,Measure}.lean`, `corpora/friction/packet_run.sh`.
- **Analysis:** `bench/friction_bundles.py` (`check`, `mine`, `tables`, `cluster`, `partial`, `callsites`, `packet`).
- **Data:** `out/corpus/friction/{ns,carleson}/bundles/` — `b.thm.jsonl`, `b.pkg.jsonl`, `mine.json`, `MINING.md`; for ns also `cluster.json`, `frame_targets.txt`, `frame_callsites.jsonl`, `frame_callsites_summary.json`, `frame_partial.json`, `packet_measure.jsonl`, `packet_summary.json`, `packet_table.md`.
