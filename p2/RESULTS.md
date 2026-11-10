# P2 results: two agents write loop proofs for a new crate, scored independently

Plan node P2 (`docs/PLAN.md`, Track P): *an agent can write loop proofs unaided, at bounded cost.*
Scored on 2026-11-10 by a separate agent (Opus 5.5 in a scoring role) that wrote neither the task nor any proof.
Every number below was re-derived from the arms' files and logs, in scratch copies under `p2/score/work/`. The arms'
own reports were read only to compare against. Scripts: `p2/score/` (driver `score.sh`). Raw results:
`p2/score/results/`. Tables marked *(summarize.py)* are printed by `p2/score/summarize.py` from those results.

- **What was attempted:** `p2/base/TASK.md`. There are 7 Rust functions with loops (128 Rust code lines) and 16
  universally quantified scenarios. The arms got no lemma library.
- **Freeze:** by content hash only. `p2/base/FROZEN.sha256` lists 39 files and its digest is
  `1ba3568cc64f960873c1ab4cd0443e4d96c735fb733a37256a99a3377e8005d9`. Nothing under `p2/` is committed, so this
  report names a digest, not a commit. PLAN rule 1 asks for a commit, so that part of the rule is not met.
- **Budget given to both arms** (their `DECISIONS.md` entries): about 150 min wall-clock, at most about 25 min per
  scenario. Tokens were neither budgeted nor measured.
- **Arms:** `p2/arm-fable` (Fable) and `p2/arm-opus` (Opus 5.5). Each ran once.

## Signals against the plan's targets

| | arm-fable | arm-opus | PLAN P2 target (a signal, not a gate) |
|---|---|---|---|
| functions fully proved (every scenario of the function) | **7 of 7** | **7 of 7** | pass: at least 5 of 6; fail: at most 2 (this crate has 7) |
| scenarios proved (exact type, standard axioms only, kernel replay) | 16 of 16 | 16 of 16 | |
| within budget | yes: 14.1 min from first to last attempt | yes: 10.3 min | about 150 min |
| hand-written Lean per Rust code line (my count) | **6.1** (6.7 with the glossary) | **6.0** (6.6) | record it; P1 ledger: 6.0 |
| failed builds / attempts (proof work) | 14 / 27: 6 real, 4 real plus probe, 4 pure probes | 8 / 16, all real | record it; P1 ledger: about 21 |
| cargo-mutants mutants (107): shown false by a scenario / only lose a proof / every proof kept | 92 / 5 / 0 (10 stop the pipeline) | 92 / 5 / 0 (10 stop the pipeline) | rule 5: a lost proof is not a detection |
| proofs of *other* functions lost to those mutants (module coupling) | 111 | 159 | (not a plan target) |

**How to read this.** Both arms land in the pass band on this item set. With 7 functions all proved, the 95%
interval (Wilson) for an arm's per-function success rate is about 0.65 to 1.00. That is clearly above the fail
band, but it cannot tell a 70% agent from a 100% one.

This is also one small fixture with textbook loops. Both arms say they recognised the two-pass majority vote that
was meant to be the hard case. What the result shows:
- the pipeline and the scoring work end to end;
- the budget did not bind (each arm used under 10% of it);
- the Lean-per-Rust ratio did not move from P1.

It does **not** show that agents write loop proofs unaided on unfamiliar code (see "Limits").

## 1. What was checked, and how

1. **Frozen files.** `shasum -a 256 -c FROZEN.sha256` gives 39 of 39 OK in each arm, and both arms' `FROZEN.sha256`
   have the base's digest. A recursive diff of each arm against `p2/base` (build outputs excluded) shows only three
   kinds of difference: new files in `lean/Lemmas/`, the 16 proof files, and `effort/attempts.tsv`. Neither arm
   changed or added anything anywhere else.
2. **Cold rebuild.** `p2/score/mkcopy.sh` makes a scratch copy from p2/base's frozen files plus the arm's
   `lean/Lemmas/` and `lean/Spec/Proofs/` only, with no Lean build outputs. The Mathlib and Aeneas packages are the
   shared prebuilt cache. The full `./run.sh` then exited 0 with 16 PROVED-FOR-ALL in each copy (83 s each).
   Logs: `results/run-{fable,opus}.log`.
3. **Independent audit** (`p2/score/audit.py`; it shares no code with `lean/Bdd/Audit.lean`). For each scenario it
   requires all of the following:
   - a theorem `Spec.inventory.<id>`, declared in module `Spec.Proofs.inventory.<id>`;
   - a type that is *syntactically* the constant `Spec.inventory.<id>.stmt`, which is declared in the frozen
     `Spec.Statements`;
   - axioms, collected with `Lean.collectAxioms`, of exactly `propext`, `Classical.choice` and `Quot.sound`.

   **Result: 16 of 16 in both arms.**
4. **Kernel replay.** The toolchain's `leanchecker` (lean4checker, Lean v4.35.0) replays every constant of every
   `Lemmas` module and every proof module through the kernel. All modules pass: 23 of 23 for fable (7 lemma modules
   and 16 proofs) and 24 of 24 for opus (8 and 16). This rules out declarations added without a kernel check
   (`debug.skipKernelTC` and similar). I ran no negative control for leanchecker; the claim rests on reading its
   source (`LeanChecker.lean`: `Kernel.Environment.replay` of each module's constants).
5. **Source scan.** Neither arm's files contain `sorry`, `admit`, `native_decide`, `axiom`, `set_option`,
   `unsafe`, `implemented_by`, `extern`, `macro`/`elab`, `instance` or `attribute`. Generated header comments are
   the only exception. Deprecated lemma names produce warnings in both arms; they are harmless.
6. **The Givens can be satisfied.** In both cold runs the pipeline's 16 `.sat` theorems kernel-check, and none of
   the "Then follows from the Givens alone" attempts succeeds.

## 2. Verdicts per scenario and per function

All 16 scenarios are PROVED-FOR-ALL in both arms, by the pipeline's own report in the cold copies and by the
independent audit above.

| function | scenarios | arm-fable | arm-opus |
|---|---|---|---|
| `stock_of` | `stock_is_sum`, `stock_too_big` | 2/2, done | 2/2, done |
| `find_bin` | `find_first_bin`, `find_no_bin` | 2/2, done | 2/2, done |
| `restock` | `restock_adds`, `restock_counts` | 2/2, done | 2/2, done |
| `take` | `take_amount`, `take_stock_down`, `take_earliest_first` | 3/3, done | 3/3, done |
| `fill_orders` | `fill_count`, `fill_state`, `fill_at_most` | 3/3, done | 3/3, done |
| `product_count` | `count_products`, `count_at_most_bins` | 2/2, done | 2/2, done |
| `dominant_product` | `dominant_found`, `dominant_none` | 2/2, done | 2/2, done |

## 3. Cost

### Lines (my recount, `p2/score/count_lines.py`)

**How lines are counted.**
- A *code line* is non-blank and is not a comment. `--` lines, `/- -/` blocks and docstrings are comments.
- `import`, `open`, `namespace` and `end` lines are boilerplate and are counted separately.
- Each `Lemmas` declaration is located by Lean's own declaration ranges and split into its statement (up to
  `:=`) and its proof.
- Each declaration is classified by what its type mentions: a generated loop function makes it a *loop lemma*,
  another generated function a *function spec*. Otherwise it is a *helper*: an *Aeneas/scalar* helper if its
  statement uses the Aeneas monad, scalars or containers, a *pure* helper if not. A `def` is a *definition*.
- Scenario proofs are counted from the line after the fixed `theorem` line.

`effort/count.py` (the pipeline's counter) counts comments in proof files and recognises loop invariants only by
`loop.spec_decr_nat`. Its totals nonetheless agree with mine: lemma code 668 / 673, proof lines 115 / 93.

| measure *(summarize.py)* | arm-fable | arm-opus |
|---|---|---|
| hand-written Lean (lemma code + scenario proofs) | 783 | 766 |
| ... per Rust code line (128) | **6.12** | **5.98** |
| ... with the glossary's 77 code lines (written by the task author, not the arms) | 6.72 | 6.59 |
| lemma code lines (boilerplate apart) | 668 (41) | 673 (51) |
| scenario proof lines (shortest to longest) | 115 (3 to 18) | 93 (3 to 14) |
| declarations: theorems / definitions | 54 / 7 | 46 / 2 |
| **loop lemmas**: declarations / statement lines / proof lines | 10 / 55 / 349 | 9 / 51 / 420 |
| function specs (top level, built on the loop lemmas) | 8 / 25 / 48 | 8 / 28 / 53 |
| pure helpers (lists, naturals, the reference definitions) | 33 / 68 / 97 | 16 / 30 / 35 |
| Aeneas/scalar helpers | 3 / 6 / 12 | 13 / 27 / 26 |
| definitions | 7 / 7 / 1 | 2 / 2 / 1 |
| declarations no scenario proof uses | 2 (`view_eq`, `orderView_eq`) | 2 (`val_eq_iff`, `stockIn_nil`) |
| tactic uses: `step*` / `step` / `loop.spec_decr_nat` | 15 / 25 / 9 | 0 / 0 / 0 |
| tactic uses: `scalar_tac` / `omega` / `simp*` / `rw` / `induction` | 81 / 39 / 150 / 85 / 4 | 18 / 109 / 185 / 89 / 9 |

**The 9 loops' lemmas are most of the cost.** Statements and proofs together are 52% of fable's hand-written
Lean and 61% of opus's; the proof bodies alone are 45% and 55%.
Opus has more Aeneas/scalar helpers because of its proof style (see section 4). Fable's loop invariants are written
inside the proof (the second argument of `loop.spec_decr_nat`), so its "statement lines" understate the
invariants. Opus's invariants are the hypotheses of its loop lemmas.

### Builds (`effort/attempts.tsv`, plus the full build log of every attempt)

`lakebuild.sh` writes each attempt's full `lake build` output to a `mktemp` file and never deletes it. I copied
those 46 files from `$TMPDIR` into `p2/score/results/buildlogs/` and matched each one to its attempt by time and
module name: 27 of 27 for fable, 19 of 19 for opus. That made it possible to sort the FAILED lines:
- **probe:** the NOTE says the build was meant to show goals, and every error is "unsolved goals";
- **real plus probe:** the NOTE says probe, but the log also contains another error;
- **real:** any other failure.

| *(summarize.py)* | arm-fable | arm-opus |
|---|---|---|
| attempts while proving / FAILED | 27 / 14 | 16 / 8 |
| FAILED, real error only | 6 | 8 |
| FAILED, real error in a build labelled a probe | 4 | 0 |
| FAILED, pure probe (only unsolved goals) | 4 | 0 |
| ok builds that still contained `sorry` (probes that compiled) | 4 | 0 |
| attempts after the last proof (labelled post-hoc probes) | 0 | 3 (2 FAILED) |
| seconds spent inside `lake build`, proof work | 201 | 120 |

Fable reported "7 of the 14 FAILED were probes". The logs support 4 pure probes. The other 3 builds labelled
probes also contained real mistakes (for example "Invalid `⟨...⟩` notation", "no goals", `scalar_tac` failures).
Opus's 8 failures are all real. Their error kinds are `omega` failures, `simp` making no progress, a type
mismatch, an unknown identifier, and unsolved goals.

### Time (from `effort/attempts.tsv` and file times)

| | arm-fable | arm-opus |
|---|---|---|
| working copy created (UTC) | 13:07:55 | 13:07:52 |
| first logged build | 13:09:16 | 13:11:35 |
| last proof build | 13:23:19 | 13:21:51 |
| final `./run.sh` report written | 13:24:15 | 13:25:14 |
| **first to last proof build** | **14.1 min** | **10.3 min** |
| copy to last proof build | 15.4 min | 14.0 min |

Both self-reports agree with the logs. Scenarios of one function were always built together, so time can be split
per function but not per scenario. The two time columns in section 4 mean:
- **active:** from the first build that touches the function to its last ok build;
- **increment:** from the previous function's last ok build to this one's, which includes writing time.

## 4. Per function and kind of loop *(summarize.py)*

Column meanings:
- *loop lemmas*: the declarations whose type mentions the function's generated loops, as count, statement lines
  plus proof lines.
- *helpers (own)*: helpers that only this function's proofs reach.
- *helpers (shared)*: helpers that this function's proofs reach and some other function's proofs also reach.
- *own total*: loop lemmas, spec, own helpers and scenario proofs.

| function | kind of loop | arm | Rust lines | loop lemmas | spec | helpers (own) | helpers (shared) | scenario proofs | own total | own Lean/Rust | builds / FAILED (real, real+probe, probe) | active min | increment min |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `stock_of` | accumulation, early return on overflow | fable | 14 | 1: 4 + 22 | 6 | 2 | 24 | 14 | 48 | 3.4 | 5 / 1 (0, 0, 1) | 1.3 | 2.7 |
| | | opus | 14 | 1: 5 + 37 | 7 | 0 | 38 | 15 | 64 | 4.6 | 4 / 2 (2, 0, 0) | 0.9 | 4.6 |
| `find_bin` | search, early exit | fable | 10 | 1: 4 + 26 | 7 | 0 | 0 | 23 | 60 | 6.0 | 2 / 1 (1, 0, 0) | 0.3 | 0.8 |
| | | opus | 10 | 1: 7 + 35 | 6 | 3 | 16 | 14 | 65 | 6.5 | 2 / 1 (1, 0, 0) | 0.3 | 0.8 |
| `restock` | in-place update of every match | fable | 12 | 1: 6 + 41 | 8 | 42 | 15 | 11 | 108 | 9.0 | **8 / 7 (4, 3, 0)** | 2.9 | 3.7 |
| | | opus | 12 | 1: 7 + 52 | 6 | 12 | 26 | 13 | 90 | 7.5 | 2 / 1 (1, 0, 0) | 0.3 | 1.4 |
| `take` | in-place update, two-part condition, early stop | fable | 14 | 1: 10 + 78 | 11 | 14 | 63 | 13 | 126 | 9.0 | 5 / 2 (1, 0, 1) | 2.0 | 3.1 |
| | | opus | 14 | 1: 5 + 74 | 8 | 11 | 38 | 12 | 110 | 7.9 | 3 / 2 (2, 0, 0) | 1.1 | 2.4 |
| `fill_orders` | loop calling two looping functions | fable | 19 | 1: 9 + 46 | 15 | 18 | 83 | 14 | 102 | 5.4 | 2 / 1 (0, 0, 1) | 0.6 | 1.1 |
| | | opus | 19 | 1: 6 + 45 | 20 | 14 | 57 | 12 | 97 | 5.1 | 1 / 0 | 0.0 | 0.9 |
| `product_count` | nested loop | fable | 15 | 3: 12 + 52 | 3 | 19 | 4 | 11 | 97 | 6.5 | 2 / 1 (0, 1, 0) | 0.7 | 1.1 |
| | | opus | 15 | 2: 11 + 70 | 4 | 6 | 19 | 10 | 101 | 6.7 | 3 / 2 (2, 0, 0) | 0.6 | 2.2 |
| `dominant_product` | non-obvious invariant (two passes) | fable | 31 | 2: 10 + 84 | 23 | 0 | 11 | 29 | 146 | 4.7 | 3 / 1 (0, 0, 1) | 1.7 | 2.9 |
| | | opus | 31 | 2: 10 + 107 | 30 | 9 | 29 | 17 | 173 | 5.6 | 1 / 0 | 0.0 | 1.6 |

The Rust lines column counts each function's own code lines. `can_fill` is counted with `fill_orders`, and the
13 lines of struct definitions are counted with no function.

What the table says, kind by kind:

- **Read-only loops** (`stock_of`, `find_bin`) were the cheapest in both arms: 3.4 to 6.5 Lean lines per Rust
  line, 2 to 5 builds, at most 2 real failures. In fable, Aeneas's `step*` took each loop body all the way through,
  including the early-exit branch and the overflow check. Fable's own probe and opus's post-hoc probe both show
  this.
- **In-place update** (`restock`, `take`) was the most expensive kind in both arms, at 7.5 to 9.0 lines per Rust
  line.
  - `restock` was fable's worst function: 8 builds, 7 FAILED. The build logs show `step*` stopping at the value
    `if` (`let x ← if … then … else …`), then at the pair returned by `index_mut`. They also show the usual
    mechanics: "no goals", anonymous-constructor errors, and an unknown name (`Vec.set_val_eq`).
  - For opus, `restock` took 2 builds. Its equational style handles the `if` with `simp` and its own
    `vec_index_mut_ok`.
  - `take` has fable's largest loop lemma (10 + 78 lines) and opus's second largest (5 + 74, after the
    majority-vote pass). Fable's invariant has three parts, the third of which pins the returned amount. Opus
    generalises over a prefix and the rest of the bins.
- **A loop that calls looping functions** (`fill_orders`) was cheap once the callees had specs. Both arms reused
  their `stock_of` and `take` specs and needed one or two builds. In "lines needed" (everything its proofs reach)
  it is the most expensive function, 15 to 17 lines per Rust line, because it inherits the `take` proof.
- **Nested loop** (`product_count`): one lemma per loop, plus a `toFinset` cardinality fact that both arms proved
  independently. It took 2 to 3 builds, and the failures were mechanical (`!=` normalised to an inequality of the
  underlying values, and the value of `0#usize`).
- **Non-obvious invariant** (`dominant_product`) had the most lines in both arms (146 and 173). It needed the
  fewest builds: 1 for opus, and for fable 3, one of them a probe. Both arms recognised the Boyer–Moore majority
  vote and wrote the same invariant in two arithmetic forms. For every product q:
  - fable: `2·count_q + votes ≤ i + 2·votes·[q = candidate]`;
  - opus: `2·count_q ≤ (i − votes) + [q = candidate]·2·votes`.

  `dominant_none` needs only the counting pass (both arms noticed this), so only `dominant_found` exercises the
  invariant.

**Two proof styles, the same line count.**
- **Fable** used Aeneas's own loop rule `loop.spec_decr_nat` with `step*`/`step` in weakest-precondition (WP)
  style.
- **Opus** used none of Aeneas's step automation. It proved "this loop, from this state, returns `ok` of this
  value" by induction on the remaining length. It added two 2-line lemmas that unfold the `loop` combinator once,
  and a dozen "this operation returns `ok` of that value" helpers.

Total hand-written lines differ by 2%. On this crate, Aeneas's step automation shortened neither the proofs nor the
time to finish them. It helped on read-only bodies and got in the way on in-place updates (fable's `restock`).

## 5. Weaknesses in the statements, and whether either arm used one

I read all 16 statements, the vocabulary they use, and every proof, looking for a proof that goes through because
the statement is weak rather than because the code is right. **Neither arm exploited a weakness.** Each scenario
proof comes from a spec of the whole function, which is in turn proved from loop lemmas. Each proof uses its
Givens only to rule out the branch that another scenario of the same function covers. Examples:
- `stock_is_sum` uses "fits" to rule out `none`;
- `find_first_bin` uses "some bin holds" to rule out `none`;
- `dominant_found` and `dominant_none` use their Givens to settle the final comparison.

What the statements leave open, and what it means:

- **No Given is vacuous.** The pipeline's `.sat` theorems hold for all 16, so no proof can obtain `False` from the
  Givens.
- **The reference definitions restate the intended algorithm, not the code.**
  - `takeFrom` and `fillFrom` are structural recursions over (product, units) pairs. The code is an index loop
    with an early exit (`left > 0`), a `min` written as `if`, and, in `fill_orders`, a `can_fill` that treats an
    overflowing stock as "enough".
  - Both arms needed real invariants to connect the two. Fable's `take` invariant has three parts; opus's
    generalises over prefix and rest.
  - So the references are not the code in disguise. They are, however, as "greedy, earliest first" as the code.
    The English Rule ("empties its earliest bins first") is all that justifies that choice, and the glossary is
    unsigned. If the owner meant a different allocation policy, the code and the reference would be wrong
    together.
- **Every output of every function is pinned by some scenario.** The exact scenarios fix:
  - `stock_of`'s result both ways;
  - `find_bin`'s result both ways;
  - every bin after `restock`, `take` and `fill_orders`;
  - every count;
  - `dominant_product` in both cases.

  `fill_at_most` and `count_at_most_bins` are corollaries of exact scenarios, and both arms proved them that way.
  So for a mutant, "every proof of its function still compiles" should mean the mutant is equivalent with respect
  to the statements. Section 6 tests this on 107 tool-generated mutants. No mutant kept its function's proofs in
  either arm, not even the 3 equivalent ones.
- **Two scenarios do not exercise the hard part.** `dominant_none` is true of the counting pass alone; it holds for
  any candidate-picking pass. `fill_at_most` holds for any implementation that returns at most `orders.len()`.
  These are not weaknesses in the suite, which contains the exact scenarios, but the count "16 scenarios proved"
  overstates the number of independent facts.
- **The pipeline reports one coverage check as NOT SHOWN.** `dominant_product`'s two scenarios have different
  variable lists, so the pipeline's "some scenario applies to every input" check is NOT SHOWN for it. That limit
  was already in the base and is unrelated to the proofs.

## 6. Mutants (cargo-mutants, every mutant the tool lists)

**Method.**
- **Item set:** 107 mutants of `inventory/src/lib.rs`. This is cargo-mutants 27.1.0's complete list (function
  bodies replaced by constants, operators swapped), so nobody chose them (PLAN rule 2). The list is in
  `results/mutants-diff.json`.
- **Per mutant** (`p2/score/mutants.py`; one JSON record per mutant in `results/mutants/`, summary in
  `results/mutants.tsv`):
  - a copy with **no proofs** runs `./run.sh --no-unit --no-adequacy`, which shows what the scenarios catch on
    their own, independently of the arms;
  - then **each arm's** lemmas and proofs are rebuilt against the mutated model.
- **"Shown false"** means a concrete input:
  - a REFUTED or COUNTEREXAMPLE verdict (an input found on the Lean model, replayed on the compiled Rust), or
  - an Examples row failing on the compiled Rust.

  A proof that stops compiling is **not** a detection (PLAN rule 5).
- **For reference**, cargo-mutants' own run with the crate's 9 unit tests: 93 caught, 5 missed, 9 timeouts,
  0 unviable.

**What the scenarios do on their own** (independent of the arms) *(summarize.py)*:

| outcome | mutants | detail |
|---|---|---|
| **shown false by at least one scenario** | **92** | 17 with a kernel-checked refutation theorem; 75 with a counterexample on the model, reproduced on the compiled Rust |
| pipeline stopped before giving verdicts | 10 | **9** turn a loop counter's `+= 1` into `*= 1`, so the loop never ends. The Lean search recurses through `Aeneas.Std.loop` until it crashes (7, each with a backtrace about 930,000 frames deep) or reaches my 420 s limit (2). The pipeline has no per-evaluation time limit. **1** (#44, `q - t` becomes `q / t` in `take`, on u64) yields a model that **does not compile**: Aeneas nightly-2026.11.09 emits `U64.div`, which its own Lean library does not define (it has `UScalar.div` and an `HDiv` instance). The usize division of mutant #106 compiles. |
| not shown false | 5 | **3 equivalent** to the original: #38 `left > 0` becomes `left >= 0` (taking 0 units changes nothing); #42 `q < left` becomes `q <= left` (both branches agree when `q = left`); #71 `j < i` becomes `j <= i` (the inner loop stops at `j = i` anyway). **2 real bugs that nothing shows false:** #88 and #89 change the vote update in `dominant_product`'s first pass. `dominant_found` is false for them at bins `[7,7,3]` with p = 7 (#88) and `[7,7,7,3,3]` with p = 7 (#89), which I confirmed on compiled Rust in a scratch check. The Examples rows and the 45-point boundary grid miss them. |

The crate's unit tests miss **exactly the same 5**. Every mutant the unit tests catch is either shown false by a
scenario (92) or stops the pipeline (#44, whose model does not compile). Every one of the 92 counterexamples
reproduced on the compiled Rust; there was no model/Rust mismatch. On this crate the scenario suite, used as a
test, found nothing that the unit tests miss, and the unit tests found nothing that it misses.

**Per arm:**

| *(summarize.py)* | arm-fable | arm-opus |
|---|---|---|
| shown false by a scenario | 92 | 92 |
| **not shown false, and only lose a proof** | **5** (#38, #42, #71, #88, #89) | **5** (the same) |
| not shown false, every proof still compiles | 0 | 0 |
| pipeline stopped (the mutated function's proofs are lost as well) | 10 | 10 |
| a scenario shown false whose proof still compiled (would be a soundness alarm) | **0** | **0** |
| proofs lost for the mutated function and its callers, summed over 107 mutants | 337 | 337 |
| ... of which for a scenario of the mutated function that was not shown false | 46 | 46 |
| **proofs lost elsewhere** (collateral, through `import`s between lemma modules) | **111** | **159** |

What this says:

1. **On detection the two arms cannot be told apart**, because detection belongs to the scenarios and the search,
   not to the proofs. The arms differ only in what else breaks.
2. **A lost proof does not separate a bug from a harmless change.**
   - Both arms lost their proofs on all 3 equivalent mutants and on both real bugs that went unseen. The two cases
     look the same from the build: on #38 the code is still correct, on #88 it is wrong.
   - Why the proofs broke on the equivalent mutants (`results/mutant-errors/`): both arms' `take` proofs have a
     case for "the loop stopped because nothing is left to take". Under #38 the loop no longer stops there.
     Fable's `scalar_tac` then cannot show `left = 0`; opus is left with an unsolved goal in its `left = 0` case.
     Both `product_count` proofs fail where they rely on the inner loop's exact exit test.
   - So the proofs follow the code's control flow, not only its results. This is the "brittleness with no change
     in behaviour" that S2 will meet when it replays real commit histories.
3. **One exact spec per function means one break loses every scenario of that function.**
   - In both arms, every mutant cost all of its function's scenario proofs, including scenarios that stayed true.
     Examples: `stock_too_big` when `stock_of` always returns `None`; `take_stock_down` when `take` takes nothing
     and returns 0.
   - The 46 in the table are those losses plus any false-but-unfound ones.
   - This is the price of the line savings from deriving each scenario from one shared spec.
4. **Collateral loss depends on where helpers live.**
   - Fable put its generic sum and count helpers in `Lemmas.Stock`. Four other lemma modules import it directly
     and `Dominant` imports it through `Restock`. Each `stock_of` mutant therefore costs 9 proofs of unrelated
     functions (`restock`, `take`, `product_count`, `dominant_product`), besides the 5 of `stock_of` and its caller
     `fill_orders`.
   - Opus's `Lemmas.Restock` imports `FindBin`, and its `Dominant` imports `Restock` and `Take`. Each `find_bin`
     mutant costs 4 unrelated proofs, and each `take` mutant 2.
   - The minimum is 0: generic helpers in model-free modules, and each function's lemmas importing only those
     helpers and its callees' specs.
5. **The search has a gap, not the statements.**
   - #88 and #89 make `dominant_found` false.
   - The grid is small (45 points for that scenario), and no Examples row has a majority product that loses its
     votes early.
   - One more row such as `[7:1, 7:1, 3:1]` with p = 7 would catch #88. A property-based search, which the plan
     already prefers to a hand-built grid, would most likely catch both.


## 7. What each arm found hard

- **arm-fable.**
  - The in-place update in `restock` (7 of 8 builds FAILED). `step*` cannot go past a value-producing `if`, and
    after a manual `by_cases`, the `index_mut` result is a pair that `step*` does not destructure (fixed with
    `rcases` plus `simp only`).
  - Seeing goals at all. `lakebuild.sh` prints goal states only when a build fails, so 12 of fable's 27 attempts
    were partly or wholly probes: 4 FAILED pure probes, 4 FAILED builds that mixed a probe with real mistakes, and
    4 ok builds that still contained `sorry`.
  - Predicting what `step*` leaves. Five of fable's failed builds contain "No goals to be solved": `step*` had
    already closed a goal the agent meant to close by hand.
  - No invariant had to be revised in a way the logs show.
- **arm-opus.**
  - Lean mechanics with no pattern by kind of loop. In its own account: a hypothesis left unnamed that a later
    `omega` needed, `simp` normal forms (`!=` becoming an inequality of values, `0#usize`), a `_` for the next
    state that Lean could not fill, and an inequality written the wrong way round. The error kinds in the logs are
    consistent with that account.
  - Its first build of `fill_orders` and of `dominant_product` succeeded.
  - It reports that every invariant worked as first written. The logs are consistent with that, but cannot prove
    it: no snapshot of the first drafts exists.
- **Both arms.**
  - **Missing library fact:** neither Aeneas nor the task supplies the value of `saturating_add`. Both proved
    the same lemma (6 and 10 code lines).
  - **Invariant discovery** was not where the time went. Both name prior knowledge as the source of every
    invariant, including the majority vote.

## 8. What this suggests

**Agent effort.**
- On loops of this kind, one agent session with no lemma library proved all 7 functions in 10 to 14 minutes of
  build activity, against a 150-minute budget.
- The cost is dominated by per-loop scaffolding, not by finding invariants: loop lemmas are 52% (fable) and
  61% (opus) of all hand-written Lean, and their proof bodies alone 45% and 55%.
- A budget of about 25 minutes per function would have been ample here. This item set cannot say what budget an
  unfamiliar invariant needs.
- The next P2 item set should come from a different author, with loops whose invariants are not textbook ones
  (both arms said the same), so that skill can be separated from recall.

**Lemma libraries worth sharing.** Both arms independently wrote the same facts. Each group below is a candidate
for a shared library; making one would change what P2 measures, so record it as a separate condition.

| fact | arm-fable | arm-opus | belongs in |
|---|---|---|---|
| value of `saturating_add` is `min (x + y) U64.max` | `sat_val` | `sat_add_val` | Aeneas (upstream patch) or a project Aeneas-facts library |
| scalar equality from value equality | `u32_val_eq` (re-proved) | used Aeneas's `UScalar.eq_of_val_eq`; its own `val_eq_iff` is unused | already in Aeneas; a matter of finding it |
| one step of the `loop` combinator; `ok`-equations for `Vec.index`, `index_mut`, `+ 1`, `-` | (used `step` instead) | `loop_cont`, `loop_done`, `vec_index_ok`, `vec_index_mut_ok`, `uadd_ok`, `usub_ok`, `usize_succ_ok` | Aeneas-facts library |
| count / sum over `take (i+1)` = over `take i` + this element | `cnt_take_succ`, `stk_take_succ` | `count_take_succ` | a small "prefix loop" library |
| `toFinset.card` after appending one element | `card_snoc` | `card_toFinset_append_single` | same (or Mathlib) |
| `stockIn` on cons/nil; `takeFrom p 0 = id`; stock after `takeFrom` + amount taken = stock; `fillFrom` count ≤ orders | `stockIn_cons`, `takeFrom_zero`, `stockIn_takeFrom`, `fillFrom_le` | `stockIn_cons`, `takeFrom_zero`, `stockIn_takeFrom`, `fillFrom_fst_le` | **next to the reference definitions in the vocabulary**, signed with them: they are what a reader checks a reference against |
| a list with its first `j` elements mapped (in-place update invariant) | `part` and 6 lemmas | (element-wise statement instead) | a small "in-place update" library |

**Where the Rust profile or the tools should change.**
- **Aeneas `step*`** should handle a value-producing `if` in a loop body and destructure the `index_mut` pair.
  That was the single most expensive obstacle in the WP style (fable's `restock`). The alternative is a profile
  rule: write `let new = …; v[i].f = new;` rather than `v[i].f = v[i].f.op(…)` under an `if`. That rule is
  untested; the evidence is one arm on one function.
- **Aeneas library:** add a spec for `saturating_add`, and probably the other `saturating_*` and `checked_*`
  values. Both arms had to prove the first one.
- **`lakebuild.sh`** should be able to print goal states from a successful build, for example with a `PROBE=1`
  mode that adds `trace_state` or logs the build as a probe. In this run, 8 of fable's 14 FAILED lines were
  labelled probes, and 4 of those also contained real errors. As it stands, "failed builds" mixes mistakes with
  looking.
- **`effort/count.py`** recognises loop invariants only by `loop.spec_decr_nat`, so it reports 0 for opus's 9
  loop lemmas. It should classify declarations by the loop functions their types mention, as
  `p2/score/count_lines.py` does.
- **How proofs are laid out** matters for maintenance more than for cost. Over the 107 mutants, fable lost 111
  proofs and opus 159 for functions that were neither mutated nor callers of the mutated one; the minimum is 0.
  - Generic helpers should sit in modules that import no model, so that a change to one function can break only
    that function's proofs and its callers' proofs.
  - Deriving every scenario of a function from one exact spec saves lines but loses all of them together. One
    option is a small per-scenario lemma for the cheap properties, such as `fill_at_most` or `stock_too_big`.
- **The counterexample search** missed two real bugs in `dominant_product` (section 6). The boundary grid should
  be complemented by random or property-based inputs with recorded seeds, as the plan's "Use existing tools"
  table already says. The pipeline also needs a per-evaluation time limit: a loop that never ends currently
  crashes the search or hangs it, with no verdict.
- **Aeneas extraction:** `u64 / u64` (mutant #44) produced `U64.div`, which the pinned library does not define.
  This belongs on the K3 list of tool fixes; the fix is a one-line alias or an extraction change.

## 9. Limits of this scoring

- **One run per arm on one toy crate.** The loops are textbook patterns, and the "non-obvious" one was recognised
  by both arms. No variance estimate is possible.
- **Time and tokens.** Time is wall-clock including the agents' own reasoning. Tokens were not measured by
  anyone.
- **Line counts.** These follow the rule stated in section 3. A different rule (comments counted, statements
  attributed differently) moves the per-function numbers by a few lines, not the totals.
- **Kernel replay.** It was not negative-controlled. The axioms check and the exact-type check do not depend on
  it.
- **Freeze.** The task was frozen by digest, not by commit (PLAN rule 1, partly unmet).
- **Mutation run.** It ran while the machine's load average was between 100 and 175 (other agents' jobs and mine),
  so the per-mutant times in `results/mutants/*.json` say nothing about the pipeline's speed.

## 10. Reproduce

    export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
    /Users/will/dev/lean-rosette/p2/score/score.sh              # everything (hours under load; mutants dominate)
    /Users/will/dev/lean-rosette/p2/score/score.sh --no-mutants # frozen check, cold rebuild, audit, lines, cost
    python3 /Users/will/dev/lean-rosette/p2/score/summarize.py  # the tables above, from results/

Scratch copies go to `p2/score/work/` (git-ignored; several GB apparent size, mostly APFS clones). Delete them with
`rm -rf p2/score/work`.
