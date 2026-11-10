# out/corpus/friction: hypothesis-level and proof-term-level export

One exporter, three corpora. Everything is read from the built Lean environments at `Expr` level; no source text or pretty-printed text is parsed.

- Exporter: `corpora/friction/Friction.lean` (imports only `Lean`), compiled to a native binary against each corpus's own toolchain by `corpora/friction/run.sh <ns|carleson|pfr> [shards]`.
- Classification config: `bench/friction_families.json` (read at run time; its `_doc` field states every rule and which ones are built in).
- Merge and coverage: `bench/friction_merge.py`; verification: `bench/friction_verify.py`; cross-corpus table: `bench/friction_summary.py` -> `SUMMARY.md`.
- Inclusion rule: exactly the declarations with `kind == theorem` in `out/corpus/<corpus>/decls.jsonl` (38,601 / 2,675 / 978). Prop-valued instances (`kind == instance`) are not included.

| file (per corpus) | content |
|---|---|
| `hyps.jsonl` | one line per theorem, sorted by name |
| `consts.jsonl` | every constant occurring in an exported proof: family, flags, summed uses |
| `heads.jsonl` | every (class, head constant) of a proof-subterm type: mass (first-reach audit figure) and number of proof subterms |
| `coverage.json`, `COVERAGE.md` | class/family tables and what falls in "other" |
| `export_meta.json` | counts, failures, timings |
| `verify_checks.json` | whole-corpus consistency checks |
| `verify_sample.md`, `verify_check_output.json`, `verify_verdicts.json` | the 15 hand-checked theorems: source, live `#check`, exporter rows; verdicts |

## `hyps.jsonl`

- `name`, `module`, `statementSize` (tree node count, equals the earlier export for every theorem), `statementDagSize`, `proofSize` (distinct subterms of the value, strict structural equality).
- `binders`: the statement's telescope, i.e. every leading `∀` including those written after the colon. Per binder:
  - `i`, `name` (`✝` marks an anonymous/hygienic name), `bi` (explicit / implicit / strict / inst),
  - `kind`: `inst` (instance-implicit binder), else `hyp` (type is a Prop), else `type` (type is a Sort), else `term`. An implicit `{m : MeasurableSpace α}` is `term`.
  - `isProp`, `mentions` (indices of earlier binders occurring in the type, implicit arguments included), `size` (tree).
  - non-Prop binders: `head` (head constant of the type after peeling `∀`; `<fvar>` if it is a type variable), `isFun`, `coarse`, `flags`.
  - Prop binders (hypotheses and Prop-valued instances) additionally carry the proposition fields below.
- `concl`: proposition fields for the conclusion, plus `mentions`, `size`.
- Proposition fields:
  - `peel`: what was stripped to reach the atom, one letter each: `A` ∀/→, `N` ¬, `E` ∃, `F` `Fact`. `neg`: parity of negations.
  - `head`: head constant of the atom (`<fvar>`, `<bvar>`, ... if not a constant). `cls`: its class (config).
  - `pos`: `lt` / `le` / `ne` if the atom is `0 < x`, `0 ≤ x`, `x ≠ 0` (also `>`/`≥` forms and `¬ x = 0`); `fin`: `lt_top` / `ne_top`. `subjVar`: binder index if `x` is exactly a telescope variable. A top-level fact has `peel == ""`.
  - `dag`, `shape` (canonical text: telescope variables become `?0, ?1, …` in order of first occurrence, instance arguments and universe levels dropped; cut at 400 characters), `shapeHash` (hash of the full text), `shapeBig` (statement over 4,000 nodes: no text, hash identifies all variables).
  - `coarse`: peel prefix, head, and a one-level summary of each explicit argument (`?` variable, `λ`, a constant name, a numeral).
  - `flags`: `ennreal` (constant `ENNReal`/`NNReal` occurs, anywhere, including inside implicit arguments such as the exponent of `PiLp`), `cast` (toReal/ofReal/toNNReal/coercions, list in config), `enorm` (ℝ≥0/ℝ≥0∞-valued norms and distances), `top` (any `⊤`), `ennrealTop` (`⊤ : ℝ≥0∞`), `indicator`, `restrict`, `support`, `cutoff`.
  - `exN`, `exReal`, `exRealPos`: number of ∃-bound variables reachable through ∃ / ∧ / ∀; how many have type ℝ, ℝ≥0 or ℝ≥0∞; how many of those have a positivity conjunct about exactly that variable (`∃ C, 0 < C ∧ …`, `∃ C > 0, …`).
- Proof term (the theorem's own body auxiliaries are inlined where they are used; `auxInlined` counts them):
  - `proofDagWithAux`, `proofTree` (fully unshared size; can be astronomically large).
  - `constsExt`, `constsProj`: per constant family `[dag, tree]` for non-project and project constants. `dag` = number of distinct applications headed by the constant; `tree` = occurrences in the unshared term.
  - `lemmaFlagUses`: `[dag, tree]` of lemma uses whose statement carries each flag.
  - `rootClass`: class of the theorem's own conclusion.
  - `mass`: see next section. `sideSubterms`: number of outermost side-condition proof subterms per class. `sideTop`: the five largest, with the coarse key of the type proved and the head of the proof term.

## Proof mass: definition

The proof term is walked once from the root; every binder is opened once with a fresh free variable, so two occurrences of the same subterm at different binder depths are one node. `mass.nodes` is the number of distinct subterms after opening binders (structural equality). It is smaller than `proofSize`, which counts de Bruijn-shifted copies separately.

A *proof subterm* is the root, an argument of an application, or a `let`/`have` value, whose expected type is a Prop. The expected type is the binder domain of the function's type instantiated with the earlier arguments (for a β-redex `(fun h : T => b) p` it is `T`), head-β-reduced; it is the goal the subterm had to prove.

Each node gets five labels from the path that reaches it:

- `outer`: class of the outermost enclosing proof subterm whose class is a side-condition class; `main` if none. This is "how much of the proof is spent proving side conditions of each kind". Once inside a side-condition proof everything below belongs to it, so nested side conditions are not counted again.
- `inner`: class of the nearest enclosing proof subterm (the root counts, with the class of the theorem's statement).
- `castRegion`, `surgRegion`: some enclosing proof subterm's type (root included) carries the `cast` flag, or an indicator/restrict/support/cutoff flag.
- `kind`: `[proof spine, inside a non-proof argument, inside an instance argument]`.

Sharing: a subterm reached under k different values of a label contributes 1/k to each. Each label's shares therefore sum exactly to `nodes` (checked for every theorem), independent of traversal order. The alternative, weighting by occurrences in the unshared tree, is dominated by a few heavily shared terms.

If the theorem's own conclusion is a side-condition class the whole proof is in that `outer` class; `rootClass` lets a reader separate stand-alone side-condition lemmas from side conditions discharged inline.

## Known limits

- Classes are syntactic. `0 ≤ b - a` is `positivity` although it may be an inequality in disguise; `p ≠ ⊤` for an exponent and `⨆ … < ⊤` for a norm are both `finiteness`; the shape rules fire for any carrier type.
- In the Mathlib of the two human corpora `s ⊆ t` on sets is `LE.le`; it is classed `mem` by a carrier-type rule (config `set_like_types`).
- Predicates defined by a project are `other` unless they are type classes (`tc`). In ns they are 14.3 of the 14.6 points of `other` among hypotheses.
- `castRegion` and `surgRegion` are sticky from the root: a theorem whose statement mentions a cast puts its whole proof in the region.
- `exReal` counts any real-typed ∃ (it also catches `∃ d : ℝ, HasDerivAt …`); `exRealPos` is the tighter signature. Constants passed as binders (`(C : ℝ) (hC : 0 < C)`) are not flagged in the exporter; they are recoverable from `pos`, `subjVar` and the binder's `head`.
- `heads.jsonl` mass is attributed to the first proof subterm that reaches a node, so within a class it depends on traversal order; it is for auditing what `other` contains, not for measurement.
- `proofSize` matches the earlier export exactly for ns; for Carleson and PFR it is 0.4% and 0.7% larger in total because the earlier exporter identified terms up to binder names.
- Hand verification covered the statement side (45 theorems) and six small proofs on the proof side; the mass partition on large proofs is checked only through its invariants.

## Census (`CENSUS.md`, `census.json`, `<corpus>/census/`)

- `corpora/friction/Census.lean` + `corpora/friction/census_run.sh <corpus> [shards]`: a second native exporter (imports only `Lean`, same inclusion rule and same inlining of body auxiliaries as `Friction.lean`). It writes `<corpus>/census/c.thm.<shard>.jsonl` (per theorem: constants of the statement, constants of the proof with counts, numeric literals, ε-shape counts, real ∃ of the conclusion, integrals of powers), `c.tab.<shard>.jsonl` (per constant: module, kind, result head, argument heads, structure facts, equation-lemma parent) and `c.meta.<shard>.json` (shard 0 also holds the project import graph read from the environment header). Field definitions are in the header comment of `Census.lean`. Constant ids are local to a shard.
- `bench/friction_census.py [--B 1000]` reads `hyps.jsonl`, the census shards and `out/corpus/<corpus>/decls.jsonl` (dependency edges; statement text for display only) and writes `census.json` and `CENSUS.md`. It needs numpy, so run it without `-I`.
- `bench/friction_census_verdict.md` is the hand-written verdict; `{{stat-id @ group}}` placeholders are filled from the computed numbers.
- Cross-check: the per-theorem non-project and project constant-use totals computed by `Census.lean` equal `constsExt` / `constsProj` of `Friction.lean` for every theorem.

## Robustness variants (`ROBUSTNESS.md`, `robust.json`, `<corpus>/robust/`)

Added after the adversarial review of the census. `corpora/friction/robust_run.sh <corpus> <variant> [shards]` reruns the same exporter binary with a variant config or target list and writes only under `<corpus>/robust/`; the baseline files above are not touched (the patched binary reproduces every stored Carleson and PFR row exactly under the baseline config).

| variant | what changes | output |
|---|---|---|
| `split` | `HasDerivAt`-style derivative-value facts are a side class of their own (`derivval`) instead of `regularity` | `split.jsonl` (slim per-theorem rows: nodes, outer, inner, kind, cast, rootClass, conclusion head), `split.heads.jsonl` |
| `splitinst` | `split`, and a Prop-valued instance-implicit argument is an instance argument, not a side-condition proof (config key `inst_props_are_instances`) | `splitinst.jsonl` |
| `aux` | `split` rules on proofs outside `kind == theorem`: auxiliary theorem constants of definitions / instances / structures (`a.auxlist.tsv`, exporter mode `auxlist`) and Prop-typed non-theorem declarations | `aux_targets.txt`, `aux_parent.tsv`, `aux.jsonl`. The report counts `_proof_N` constants and Prop-typed declarations only; compiler-generated lemmas are exported but left out |
| `preds` | exporter mode `preds <depth>`: every project-defined, non-class, Prop-valued definition or structure is opened (δ-unfolding, structure fields, ∧ / ∀ / ∃) and the classes of the atoms reached are listed, with the number of real `∃ C` with a sign conjunct | `p.preds8.jsonl` (to depth 8), `p.preds2.jsonl` (two levels) |

- Variant configs are written to `out/corpus/friction/robust/cfg_*.json` by `bench/friction_robust.py mkconfig`.
- `bench/friction_robust.py report [--B 1000]` (needs numpy, so no `-I`) writes `robust.json` and `ROBUSTNESS.md`; its hand-written head is `bench/friction_robust_head.md`. `bench/friction_census.py` fills the `{{r:…}}` placeholders of the census verdict from `robust.json`, so run the report first.
- The exporter's label layout now allows 24 classes (was 16).
