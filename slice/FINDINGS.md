# Vertical slice: findings (2026-11-09, ledger added 2026-11-10)

The chain works end to end on a small example: English scenarios → Lean statements → proofs about Lean code that Aeneas generated from real Rust. Assembled from the final agent's report, which was blocked from writing this file.

## Run it
`cd slice && ./run.sh` (about 15 s warm). Exits 0 when every scenario gets its expected verdict. `./run.sh --strict` currently exits 1 on purpose, because nobody has signed the glossary. Output: `slice/out/report.md` and `slice/out/graph.json`.

## Scenario verdicts (45-line Rust wallet: deposit, withdraw, transfer)

| Scenario | Verdict |
|---|---|
| A covered transfer moves the money and conserves the total | PROVED-FOR-ALL |
| Withdrawing more than the balance is rejected and changes nothing | PROVED-FOR-ALL |
| A deposit that would overflow is rejected and changes nothing | PROVED-FOR-ALL |
| A covered withdrawal succeeds and takes exactly the amount | PROVED-FOR-ALL |
| A deposit with room succeeds and adds exactly the amount | PROVED-FOR-ALL |
| Transferring more than the sender has is rejected and changes nothing | PROVED-FOR-ALL |
| A transfer the receiver has no room for is rejected and changes nothing | PROVED-FOR-ALL |
| Transferring more than you have is rejected (literal values) | PROVED-INSTANCE |
| A transfer the sender can afford always succeeds (deliberately false) | REFUTED |
| A deposit earns interest (phrase not in the glossary) | UNBOUND |
| A withdrawal both covered and not covered (contradictory Givens) | VACUOUS |
| A deposit does not touch a bystander (control for an empty Then) | PROVED-FOR-ALL, 1 of 2 Thens substantive |

The false scenario passes both of its example rows as ordinary tests. The search found `a = 1, b = u64::MAX, amount = 1`; the kernel checked that the statement is false there, and the same input fails on the compiled Rust.

## What PROVED does and does not guarantee
PROVED means Lean's kernel accepted a proof whose type is exactly the generated statement, using only Lean's three standard axioms, and a second checked theorem shows the Givens can be satisfied.

It does not mean the Rust does what the English says. Four things are trusted, not proved:

| Trusted | Risk limited by | Not covered |
|---|---|---|
| Glossary: each phrase means its Lean definition | 14 one-line entries printed in the report; each compared on a grid with a second reading in Rust; sign-off voided when an entry changes | nobody has signed; both readings wrong the same way |
| Aeneas translation, including its hand-written models of `checked_add` and `-` | example rows and counterexamples run on both model and Rust | agreement checked on 21 rows only |
| Lean kernel plus ~120 lines of audit code | both are small | a bug in either |
| rustc | standard | miscompilation; proofs see a nightly's view, tests run on stable |

The statement generator and the proof text are not trusted: Lean type-checks the first and only kernel acceptance counts for the second.

## What the review found and what changed
- **A proof of the wrong statement counted as a proof.** Replacing a proof with `theorem … : True` still gave PROVED. Fixed: the audit now requires the exact statement type.
- **Three real Rust bugs survived every proof.** The first eight scenarios left most success paths unspecified. Fixed with four more scenarios and a checked coverage theorem per operation.
- **A misleading glossary entry passed silently.** Fixed in part: each phrase now has a second reading in Rust, compared on a grid.

## Mutation test (18 hand-picked bugs injected into the Rust)

| Scenario set | Noticed |
|---|---|
| First 8 scenarios | 11 of 18 |
| Current 12 scenarios | 18 of 18 |

- The example rows alone catch 17 of the 18. The proofs caught one bug the tests miss: a deposit of exactly 1,000,003 that credits one unit too few.
- The crate's own unit tests miss three.
- A proof can fail when nothing is wrong, so a failed proof means "not shown", never "false".

## Schema
`docs/SCHEMA.md` holds version 2 of the refinement graph: nodes with a statement and one or more implementations, edges carrying evidence of four kinds (kernel-checked, tested, tool-trusted, human-asserted), and staleness computed from content digests. It validates the slice's real graph (109 nodes, 275 edges) and a small maths example (11 nodes from the Pell demo), the latter assembled by hand.

## Limitations
- The code is three straight-line functions: no loops, collections, traits or I/O. Whether proofs stay short on real code is the largest unknown.
- The glossary is unreviewed, so every PROVED rests on one agent's reading of the English.
- The counterexample search is a small boundary grid; a bug away from boundaries shows only as a failed proof.
- The 18 mutants were chosen by the agent that wrote the scenarios.
- The maths side does not yet emit the schema itself.
- Toolchain: Charon needs one exact Rust nightly and Aeneas pins Lean 4.35.0, so the slice carries its own Mathlib (about 12 GB in all).

## Next steps
1. Try code with a loop over a collection, where proofs need invariants.
2. Have the maths side write the graph directly.
3. Read and sign the 14 glossary entries (`python3 -m slicegen review all --reviewer NAME`), then make `--strict` the default.

Detail: `slice/DESIGN.md`, `slice/TOOLCHAIN.md`, `slice/mutation/results.md`, reviewers' evidence in `slice/review/`.

---

# Addendum: the ledger (loops and a collection), 2026-11-10

The sections above describe the wallet only. A second crate, `slice/ledger` (85 lines, a `Vec` of balances, two `while` loops, batches of transfers), was added to see what happens beyond straight-line code. `./run.sh` now covers both: 35 scenarios, all with their expected verdict.

## Result
- **16 ledger scenarios proved for all inputs**, among them: applying any batch conserves the total; a batch stops only at a transfer that cannot be carried out; a rejected whole batch leaves the ledger unchanged.
- **5 proved for literal values, 2 false claims refuted** with counterexamples that reproduce on the compiled Rust.
- **Scenarios with two operations in sequence work** (apply a batch, then compute the total).

## Cost

| | Wallet (straight-line) | Ledger (2 loops, a Vec) |
|---|---|---|
| Rust code lines | 37 | 65 |
| Hand-written Lean in all | 58 lines | 389 lines |
| Lean per Rust line | 1.6 | 6.0 |
| Loop invariants written by hand | 0 | 2 |
| Helper lemma library | none | 227 lines |
| Failed builds on first attempt | 2 | about 21 (builder's tally) |

- **Effort follows loops, not line count.** Each loop needed an invariant, a second pure version of the computation, and a proof linking them: roughly 50–90 lines and an agent-hour.
- **After that, new properties are cheap.** Four scenarios added in the fix round took three builds.
- **The short scenario proofs are short only because the lemmas carry the difficulty.**

## What the review found
- **A bug could be proved around.** No scenario said a rejected batch is rolled back. The reviewer removed the rollback, re-proved one lemma and two scenarios, and got a fully green run. Fixed by adding the atomicity scenario; the same patch now fails with a counterexample.
- **A lost proof is not a detection.** Four of the reviewer's five injected bugs were noticed only because a proof stopped compiling. The report now separates "a scenario is shown false" from "a proof was lost".
- **Witnesses were degenerate.** The check that each rule's conditions can be met used the empty ledger, exercising no loop iteration.

After the fixes, 26 of 27 ledger mutants are shown false by a scenario. The new scenarios were written knowing the reviewer's mutants, so this confirms the fix and is not an unbiased rate.

## Verdict
Viable with an agent writing the proofs, for safety properties, stop and atomicity conditions, and literal examples. Not push-button once there is a loop.

## Open problems
- **Scenarios do not determine what a loop computes.** The exact behaviour is proved only in the helper lemmas, which nobody signs. Fixing this needs either a small signed reference model in the vocabulary or a rule form that compares two runs.
- **Idiomatic Rust does not translate.** `for` over ranges, iterator chains and closures failed; they must be rewritten as index-based `while` loops.
- **Small sample.** Two loops, one flat collection; no nesting, traits or generics.
- **The glossary (now 44 entries) is still unsigned.**

---

# Addendum: Rules, the suite adequacy note, the per-Rule block, 2026-11-10

Plan nodes F1, the first check of V2, and X1a for the slice. Detail: `slice/DESIGN.md` section 13. The fixtures
are toys; the numbers below show the machinery working and say nothing about suites in general.

## What changed
- **Gherkin `Rule:` works with the pinned runner.** cucumber-rs 0.23.0 runs a Scenario Outline with Examples
  under a `Rule:` (confirmed by running it; `review/rule-probe/`). The wallet and ledger features now put their
  scenarios under 14 Rules; the same files still run as cucumber tests (81 scenarios, 365 steps, as before).
- **The rule line is carried, not compiled.** It is plain English printed in the report and stored in the
  graph. What is proved is each scenario under it. Nothing checks that a rule line says what its scenarios say.
- **Every verdict is unchanged**: 35 scenario verdicts and 12 input-coverage verdicts, compared field by field.
- **Each report now carries a suite adequacy note**, per operation and per Rule, and a per-Rule block
  (verdict, examples, suite, rests on) generated from `out/graph.json`.

## What the adequacy note found
For each operation, trivial implementations (rejects everything; does nothing but report success; answers as
the code does but never changes the state; returns a constant) are generated as Lean models of the same type,
and every proved universal scenario is checked against them: 53 models, 234 scenario-model pairs.

| | |
|---|---|
| Operations whose proved universal scenarios rule out every trivial variant | 7 of 8 |
| Operation that still allows one | `apply_all`: "always rejects, changes nothing" satisfies all three of its universal scenarios (kernel-checked), and so does "answers correctly but never changes the ledger" (not refuted on the grid) |
| What rules those out | only a literal example, for one input |
| Rules that rule out every variant on their own | 6 of the 10 with a proved universal scenario |
| Pairs where the scenario is false of the trivial model | 169 (133 kernel-checked at the found input) |
| Pairs where the scenario is proved to hold of the trivial model | 32 |
| Pairs with neither | 33 (32 get no kernel attempt; 1 attempt fails) |

- The `apply_all` gap is real and was already known from the hand review (no universal scenario promises that
  a whole batch is ever accepted; mutant `lw3` falsifies no universal scenario). The note finds it mechanically.
  It was not closed: the missing rule needs the intermediate ledgers, the open problem recorded above.
- A single scenario or Rule often holds of a trivial implementation (the conservation scenario holds of a batch
  function that does nothing). The report states this per Rule in neutral terms and names what rules it out.

## Controls
`python3 -m slicegen.selftest` (22 checks of the parser and the note's bookkeeping, no Lean) and five controls
in the mutation harness: removing the progress scenario of the batch suite makes the report say the suite still
allows reject-all (c16); the same for withdrawals, with a kernel proof (c17); the unchanged tree reports
"(none found)" where it should and the `apply_all` gap (c18); an ill-typed trivial model costs the note and
nothing else (c19); taking a tag off a Rule changes what its scenario is expected to be (c20).

## Limits
- Four kinds of trivial implementation only. "None found" is not "the suite pins the behaviour".
- "Still allows" is proved only where the report says so; otherwise it rests on the search grid. One pair shows
  why that matters: a grid whose batches have at most four transfers cannot refute "always answers 4".
- Which result values count as a rejection or a success is a hand-made, unsigned list in the glossary.
- Rule texts are the builder's wording and unreviewed, like the rest of the glossary.
- No echo of a compiled reading: that needs the frame library.
- Cost: two more Lean processes per run, 21 s and 12 s measured alone, beside a run that took 33 s before. The
  whole run was not re-measured on an idle machine (87 to 95 s under a load average of 60 to 100).
  `--no-adequacy` skips the note.

## Regression
- **Mutation harness rerun after the change** (45 Rust mutants, 20 controls, 26 minutes with 6 jobs on a heavily
  loaded machine): every recorded field of all 45 mutants is identical to the previous run (shown false: wallet
  17 of 18, ledger 26 of 27; lost-proof-only: `d6`, `la6`), and the 15 earlier controls behave as before.
- **Harness changes, for the record**: scenarios are now removed by id, one control's pattern no longer depends
  on the order of the verdict tally, one patch text was re-indented, and mutant runs skip the adequacy note.
- **Not changed**: no scenario, glossary phrase, Lean definition, proof, lemma or line of Rust.

---

# Addendum: Rules, the suite note and the trade map (2026-11-10)

## `Rule:` and the suite adequacy note
- Scenarios now sit under Gherkin `Rule:` lines (14 Rules for the 33 fixture scenarios). The pinned cucumber-rs runs outlines under a Rule; every earlier verdict is unchanged.
- For each operation, the proved rules are checked together against trivial implementations (reject everything, do nothing, identity, constant). This is information for the author, never a failure.
- 7 of 8 operations' suites rule out every trivial implementation. The whole-batch operation's suite still allows "always rejects".
- `out/report.md` has one block per Rule: text, verdict, examples, suite line, and what the verdict rests on (meaning, proof, translation, compilation), generated from `out/graph.json`.
- The rule line is not yet compiled or echoed back; that is the frame-library step.

## Trade map (`compare/TRADES.md`)
The same 23 rules discharged by example rows, property-based tests, bounded model checking and Lean proofs, against 52 tool-generated mutants.

| Arm | Mutants caught (of 52) |
|---|---|
| Example rows | 50 |
| Property tests, plain generators | 45 |
| Property tests, edge-weighted | 50 |
| Bounded model checking (Kani) | 50 |
| Lean, own counterexample search | 47 |

- Proofs give the result for all inputs and sizes on the real code; no injected bug was caught by proof alone on these fixtures.
- Kani alone found the two single-magic-value bugs, and can only show a ledger rule holds up to small sizes.
- Four mutants are caught by nothing: no rule yet says a whole batch is ever accepted.
- Practical consequence: the pipeline should accept falsifying inputs from property tests and Kani, since its own search found 188 of the 212 falsifiable pairs.
