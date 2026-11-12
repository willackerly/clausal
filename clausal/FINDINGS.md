# Vertical slice: findings (2026-11-09, ledger added 2026-11-10)

The chain works end to end on a small example: English scenarios → Lean statements → proofs about Lean code that Aeneas generated from real Rust. Assembled from the final agent's report, which was blocked from writing this file.

## Run it
`cd clausal && ./run.sh` (about 15 s warm). Exits 0 when every scenario gets its expected verdict. `./run.sh --strict` currently exits 1 on purpose, because nobody has signed the glossary. Output: `clausal/out/report.md` and `clausal/out/graph.json`.

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
3. Read and sign the 14 glossary entries (`python3 -m clausal review all --reviewer NAME`), then make `--strict` the default.

Detail: `clausal/DESIGN.md`, `clausal/TOOLCHAIN.md`, `clausal/mutation/results.md`, reviewers' evidence in `clausal/review/`.

---

# Addendum: the ledger (loops and a collection), 2026-11-10

The sections above describe the wallet only. A second crate, `clausal/ledger` (85 lines, a `Vec` of balances, two `while` loops, batches of transfers), was added to see what happens beyond straight-line code. `./run.sh` now covers both: 35 scenarios, all with their expected verdict.

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

Plan nodes F1, the first check of V2, and X1a for the slice. Detail: `clausal/DESIGN.md` section 13. The fixtures
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
`python3 -m clausal.selftest` (22 checks of the parser and the note's bookkeeping, no Lean) and five controls
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

---

# Addendum: the composable vocabulary, compiled Rule lines, echo-back, 2026-11-10

Plan nodes V2 (frame library) and V3 (recompile regression). Detail: `clausal/DESIGN.md` section 14. The wallet
and the ledger are toy fixtures; the numbers below show the machinery working and are not conclusions about
real systems. Negative results are in "What did not work or is not done".

## What changed
- **Sentences are assembled from typed pieces, not bound whole.** `clausebook.yaml` has three kinds of piece:
  31 domain words (8 operations bound to the Aeneas model; measures, conditions, collections, answer words),
  27 modifiers, 19 frames with a surface form; plus 10 idioms (a surface form with the composition it means).
  A sentence that does not compose is refused with file:line: UNBOUND, ILL-TYPED (the two types are named) or
  AMBIGUOUS. Never a guess. ILL-TYPED is reported only when the sentence fits a form once value types and type parameters
  are ignored; other type errors (an actor where a number is needed, a ledger as a result) come back as UNBOUND, and an
  UNBOUND Rule line names the grammar but no nearest forms.
- **A shared frame library** (`lean/Frames/`, core Lean only): an abstract operation (state, input; an answer
  with the state afterwards, or no answer), typed holes, the fail-closed defaults written once, and 23
  definitions covering the 14 frames of the first catalogue. Each frame has a Lean definition, a fixed English
  paraphrase and an executable second reading (same author, different style); the definition and the executable
  reading are compared on generated inputs every run, and since the review also on a toy operation that gives no
  answer at one input and rejects another (see the addendum on the review below).
- **The `Rule:` line is compiled** to one Lean statement that covers every input, and is proved from the
  scenarios beneath it by a generated, kernel-checked glue theorem (or by a hand-written proof where the
  script fails), or refuted in the kernel at the input a search found.
- **Echo-back.** Every rule and scenario is printed first as its compiled reading in slot-structured English
  (applies to / assuming / then / defaults applied); the Lean is underneath.

## Results
| | |
|---|---|
| Frames | 23 Lean definitions for the 14 catalogue frames; 19 reachable from a sentence; 4 not (counting with a number, monotone, agrees with a reference, independent of) |
| Pieces by kind | 31 domain, 27 modifiers, 19 frames = 77; plus 10 idioms |
| The old 44 whole-phrase entries | read with 73 entries of the new vocabulary (31 domain, 21 modifiers, 11 frames, 10 idioms). 26 of the 36 old Given/Then phrases compose from regular forms; 10 needed an idiom; the 8 Whens are the 8 operations |
| Scenarios recompiled | 34 of 34 that had a statement (the 35th is the deliberately unbound one) |
| NEW ↔ OLD | 34 of 34 readings proved EQUIVALENT to the old statement by the kernel (`<id>.reading_iff`), standard axioms only; 33 non-vacuity theorems (the 34th scenario is the deliberately vacuous one) |
| Strengthened by the defaults | 0 scenario statements (the old ones were already fail-closed) |
| Scenario verdicts | all 35 as before: 24 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 3 REFUTED, 1 UNBOUND, 1 VACUOUS |
| Rule lines compiled | 13 of 14 (the 14th is "earns interest", meant to be unbound). 13 of the 14 rule lines had to be REWORDED into the vocabulary; no scenario text changed. Five of the 13 said less than the lines they replaced. Two were restored after the review (withdrawal and deposit again say that the call always answers; both are still proved from their scenarios). Three still say less: total_fits ("the sum of its balances, or absent") and batch_then_total ("does not change the total computed afterwards") no longer say what the total is, only whether one is returned; whole_batch no longer says that an accepted batch is applied completely. These three cannot be said with the current pieces (UNBOUND / ILL-TYPED: apply_all answers a Bool, and no piece turns a sum into an optional value). The scenarios beneath them still say these things |
| Rule statements | 10 PROVED-FOR-ALL (8 by generated glue from their scenarios, 2 by a hand-written proof from the loop lemmas), 3 REFUTED in the kernel, 1 UNBOUND |
| Definition against executable reading | agree on 23,772 of 23,772 (point, frame) evaluations over the 47 fixture readings (23,700 before two rule lines gained a clause), but with little power: the definition is false at only 125 of them (always 76, decreases by 35, the result is 14; all in the six deliberately false readings) and no call in scope gives no answer. A checker that is wrong only where a claim fails, or only on a silent call, passes that comparison: in the review, 4 of 7 deliberately broken checkers (D1 dropped; never-changes always true; exactly-when read as if-then; decreases-by without its guard) passed `./run.sh` with exit 0. Held-out sentences: 2,801 of 2,801, 306 of them false (result at least 225, at most 81). Since the review every frame is also compared on a toy operation with a silent and a rejected input: 3,141 of 3,141 hand-written evaluations, 632 false, 192 with a silent call; all 7 broken checkers now disagree there (see the addendum below) |
| Five new ledger rules, existing pieces only | 5 of 5 compile; they were written by the vocabulary's builder, `clausebook.yaml`, `Ledger/Pieces.lean` and `vocab.py` were last edited after them, and three of the five use a form that no other sentence uses, so "no change to the vocabulary" cannot be confirmed; 4 no counterexample on the grid, 1 (meant false) counterexample found; none proved |
| Feature files under cucumber-rs | unchanged: 81 scenarios, 365 steps |

## What a new sentence needs
- **Nothing, to get a statement and an echo**, if it can be said with existing forms. The five new rules are the
  only evidence for that here, and the tree cannot show that no entry was added or changed for them (see Results).
- **A proof**, to get a verdict. A rule that follows from scenario theorems by cases gets one from the glue
  script; anything else needs a person or an agent.
- **A Rust step**, to run on the compiled code. The Rust side is still one step per old whole phrase.
- **The right words.** The five rules were written by the builder of the vocabulary, who knows its forms.
  Whether an author who does not know them hits the forms is plan node V4 and is not measured here.

## What did not work or is not done
- **The glossary did not shrink.** 44 entries became 87 (77 pieces and 10 idioms). The hoped-for gain is that 46 of the
  77 are shared (by kind: modifiers and frames; in use, 12 of them occur in sentences of both fixtures, 24 in one fixture
  only and 10 in none; 11 / 25 / 10 before the withdrawal and deposit rules regained "always answers"), and that new
  sentences stop adding entries; on two toy crates that gain is asserted by five
  builder-written sentences, not measured.
- **Every fixture scenario needs an idiom** (the naming Givens "has a balance of", "holds the balances"),
  because the scenario texts were kept so that the same files run under cucumber-rs.
- **The Rust side is not compositional**: no second reading in Rust per piece, no step for a new composition.
- **Two rule statements could not be derived from their scenarios** by the script (the scenarios name a sum
  with a `u64` outline parameter). They are proved by hand from the loop lemmas instead, so those two rules
  rest on unsigned lemmas, the open problem already recorded for the ledger.
- **Frames 12 to 14 and counting with a number are definitions with a test, not vocabulary**: no surface
  form, no domain word for the relation or the reference they take.
- **The echo has not been shown to a reader.** Its English is the builder's.
- **Rule lines became long.** "For a batch, the number of transfers applied is at most the length of the
  batch, and for a batch for which the first transfer of the batch is not valid on the ledger, no transfer is
  applied and the ledger is unchanged" is what a compound rule costs in this grammar.
- **Run time**: the final `./run.sh` from scratch took 1 min 51 s warm, at a load average of 58 to 120 from
  other agents; 3 min 56 s on the first run, when the new Lean modules had to be built. The three new Lean
  scripts cost about 50 s of CPU. Not measured on an idle machine.

## Controls and the mutation run
Rerun after the change (`python3 mutation/run_mutants.py --jobs 12`, 73 minutes on a machine at load 80 to 180
from other agents; 45 Rust mutants, 27 controls):

- **Mutants: every recorded field of all 45 is what it was**, except that the changed example rows are listed
  at their new line numbers (the feature files gained tag lines; same rows, same counts). A scenario is shown
  false of 17 of 18 wallet and 26 of 27 ledger mutants; `d6` and `la6` still fail the run only through a lost
  proof.
- **The rule statements add no detection.** Each mutant now also records which rule statements are found
  false. A rule that holds of the unmutated code is found false for 30 of the 45 (10 wallet, 20 ledger), never
  for a mutant of which no scenario is shown false, and for 13 mutants a scenario is shown false and no rule
  statement is. That is what "the scenarios entail the rule" predicts: the rule lines say less than their suites.
  Only 2 of those 30 falsities were confirmed in the kernel; the rest are counterexamples found by the search.
- **Controls: 27 of 27 as expected.** Seven are new (c21 to c27; `DESIGN.md` 14.8): a frame's definition
  weakened, a domain word redefined, a frame's executable reading wrong, an ill-typed rule line, a rule line
  that is false while its scenarios stay proved, a signed piece edited, a form removed. Two older ones changed
  their expected exit status from 0 to 1 on purpose (c8, c17: removing a progress scenario now also costs the
  rule statement its proof). One finding from writing c21: weakening "is decreased by" does NOT break the
  equivalence of the covered-transfer scenario, because its other Thens ("increased by", "total unchanged")
  imply the exact decrease; it does break the covered-withdrawal scenario, which has no such redundancy.

---

# Addendum: review of the frame library and fixes, 2026-11-10 (evening)

The frame library was checked by a second agent on a different model (evidence: `review/frames/rv_tools/`;
its judgement calls: `DECISIONS.md`, "V2/V3 frame library: review"). This addendum says what was changed in
response and what the rerun shows. The wallet and the ledger are toy fixtures. No reader, person or model, has
looked at an echo. The frame mutants and the four test sentences are the reviewer's; the toy tests were
written by the fixer knowing those mutants, so "all are now caught" is a regression result, not a blind one.

## What the review found
- **Reproduced:** every number of the builder's report (verdicts, 34 of 34 equivalences, 23,700 of 23,700,
  the mutation fields it sampled, 27 of 27 controls).
- **"If-then" said less than its echo.** "X is accepted whenever C" required an answer only where C holds; the
  echo printed "the call gives an answer [default D1]" for every input.
- **The definition-versus-checker comparison had almost no power on the fixtures** (see Results above): 4 of 7
  deliberately broken checkers passed the run.
- **Rewording the Rule lines lost content in 5 of 13.**
- **The echo hid three reading rules** (conditions are judged before the call; negation binds to its one
  condition; collection scope was printed for scenarios only) **and what "accepted" means per operation.**
  In 0 of the reviewer's 4 test sentences did the echo show how the compiled reading differs from the natural one.
- **The equivalence audit checked the type only**, and its guard against a general relation was a blocklist of
  three names.
- **Three statements were overstated:** "no vocabulary change" for the five new rules, "46 of 77 shared", and the
  description of the refusals.

## What changed
| | |
|---|---|
| If-then | The DEFINITION was changed, not the echo: `IfThen.at` is now `op.HoldsAt (fun s a r _ => C s a → cls r)`, so the call must answer whether or not C holds, like every other frame. The narrower claim keeps its own sentence ("<operation> for which C is always accepted") and its own echo ("assuming C"). Four kernel-checked lemmas state the relation (`Frames/Lemmas.lean`: `IfThen.alwaysAnswers`, `IfThen.given`, `IfThen_of_given`, `ExactlyWhen_iff`). Nothing proved depended on the old definition; the one held-out sentence that uses it still has no counterexample on the grid |
| Comparison power | `lean/Run/FrameToyTests.lean` (core Lean only): every one of the 23 frames on a toy operation that gives no answer at 0, rejects 1 and accepts from 2, 35 lines, each claim false at some points. The reading search now counts, per frame, the evaluations at which the definition is false and at which the call is silent, and the report prints `comparison untested for <frame>` when no comparison of the run saw both |
| Rule lines | The withdrawal and deposit rules again say "always answers"; both are still PROVED-FOR-ALL from their scenarios by the generated glue |
| Echo | D8 (conditions are judged before the call) and D9 ("every X is not P" means no X is P) are printed with every reading they apply to; D5 is printed for Rule lines too; an `accepted` line says which answers of the operation count as accepted; every outline parameter and input is printed with its type ("sum (a u64: 0 to 2^64 - 1)"); the "changes only" frame no longer has ledger words in its shared English |
| Clauses that cover no call | A clause about accepted or rejected calls only that is about no call on the search grid is flagged COVERS NO CALL ON THE GRID (terminal, report, graph). No fixture reading has one |
| Link audit | An equivalence is not counted if its proof reaches a proof of either side (walked through every constant of the project; by type and by name). The blocklist is replaced by an allowlist: of the project's constants, a reading may mention only what its pieces name |
| Controls and checks | Four new controls (c28 to c31, `DESIGN.md` 14.8); the selftest now exercises ILL-TYPED, UNBOUND and AMBIGUOUS on rule lines |
| Overstated text | Corrected in this file, `DESIGN.md` 14, `heldout/new_rules.feature`, the report's "New sentences" section and the builder's report |
| Scratch | 3.6 GB of stale first-pass review files deleted from `review/frames/` (one still held a mutated checker) |

## Results after the fixes
| | |
|---|---|
| `./run.sh` from scratch | exit 0 in 5 min 18 s at load 80 to 110 from other agents (not a timing). 35 scenarios: 24 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 3 REFUTED, 1 UNBOUND, 1 VACUOUS. 14 rule statements: 10 PROVED-FOR-ALL, 3 REFUTED, 1 UNBOUND. All as before |
| NEW ↔ OLD | 34 of 34, standard axioms only; none of the 34 proofs reaches a proof of either side |
| Allowlist | 47 of 47 compiled readings mention only project constants their pieces name |
| Definition against checker, fixtures | 23,772 of 23,772; false at 125, silent at 0 (unchanged in kind: the fixtures still have no power) |
| Definition against checker, held-out sentences | 2,801 of 2,801; false at 306 |
| Definition against checker, hand-written instances | 3,141 of 3,141 (45 lines: 10 on the wallet and the ledger, 35 on the toy operation); false at 632, silent call at 192. Every frame is compared at a false claim and at a silent call |
| The reviewer's 12 frame mutants, against the toy lines alone | 7 of 7 broken checkers disagree on at least one toy line (4 of 7 passed the run before). Of the 5 broken definitions, 4 disagree on a toy line and 1 breaks the build as before; 2 of the 4 also stop a new lemma compiling. Not blind: two toy lines were added because a first version missed the decreases-by guard and the weakened exactly-when |
| The reviewer's 4 test sentences | r2 (if-then): the Lean now says what the echo says. r1 (scope) and r3 (timing): the compiled reading is unchanged, and the echo now prints D9 and D8. r4 (a rejected batch): the echo prints "every answer is an acceptance ... a clause about rejected calls covers no call", and the search flags it. Whether a reader notices is not measured (`review/frames/fix_tools/natural_echo_after_fixes.txt`) |
| Controls | 31 of 31 as expected, rerun one pipeline at a time (57 minutes): the 27 earlier ones, and four new ones: c28 a clause about rejected calls of an operation that never rejects is flagged and the run passes; c29 a checker wrong only on a silent call fails the run through the toy operation while the fixture comparison still reports 23,772 of 23,772; c30 an equivalence proved from the proof of the old statement is not counted and the scenario is UNLINKED; c31 a model field written into a domain word fails the allowlist in 19 readings (`review/frames/fix_tools/controls_after_fixes.txt`) |
| cucumber-rs | unchanged: 14 rules, 81 scenarios, 365 steps |

## Where the fixes differ from the reviewer's proposals
- **"Every X is not P" is not refused.** The reviewer preferred refusing it as AMBIGUOUS with a hint to write "no X
  is P". It has exactly one reading under the grammar, so AMBIGUOUS would be the wrong label, and refusing it
  changes which sentences the vocabulary accepts (held-out rule n5 would stop compiling). That is a change to the
  vocabulary for the owner to make; D9 is printed meanwhile.
- **`accepted` lines say what the Lean says, not what the code does.** The proposed "(the sum fits in 2^64 - 1)"
  and "(the account exists)" describe the model's behaviour; the definition is only "the answer carries a value".
- **The allowlist is about the project's constants only.** Core notation cannot be listed robustly, and a lambda
  written with core notation alone is not stopped by any list of names: `EveryOf` with the answer as its
  collection can still state any predicate of (input, answer, state after), if a piece produced such a
  collection. No piece does; pieces are what a person signs; 0 of 87 are signed.
- **The toy tests are a file of their own** (`Run/FrameToyTests.lean`, importing the frame library only), not an
  appendix to `Run/FrameTests.lean`, so they can travel with the library; they also cover the four frames with
  no surface form.
- **"Untested" is printed, not fatal.** A frame with no false or no silent comparison is reported; the run does
  not fail on it.

## Not done
- **Three rule lines still say less than the lines they replaced** (total_fits, batch_then_total, whole_batch):
  the pieces to say them do not exist.
- **The 45-mutant run was not repeated** after the fixes (an estimated one and a half to two hours, one run at a time);
  `mutation/results.json` is from before them and the report marks it OUT OF DATE. The controls were rerun.
- **The checker and the definition still have one author**, and the comparison on the fixtures still has no power;
  the toy operation is where a wrong checker would be seen.
- **An UNBOUND Rule line still names the grammar but no nearest forms**; other type errors still come back as
  UNBOUND, not ILL-TYPED.
- **No reader trial.** K1/V5 on these echoes with proxy readers (the reviewer's r1 to r4 are ready-made items)
  and V4 with authors who do not know the vocabulary are the next measurements.

# Addendum: end to end for new sentences (2026-11-10/11)

The largest gap in the builder's report was that a NEW sentence got a statement and an echo and nothing else. This addendum is what was built to close it, what it measures on the fixtures, and what is still missing from the README's target. Everything is on two toy crates; the sentences, the proofs, the Rust readings and the controls have one author lineage (agents), and no reader, person or proxy, has seen the new echoes.

## What a new sentence gets now

A scenario or `Rule:` line with no entry in the old whole-phrase glossary, built from existing pieces:

| Stage | Before | Now |
|---|---|---|
| Reading and echo | yes | yes |
| Runs on the compiled Rust | no (a step had to be written) | yes: one generic cucumber step evaluates the step's composition tree with one Rust reading per piece; a Rule line with no scenario is evaluated on generated inputs |
| Proof obligation | none | a flat obligation generated from a `flat:` template per frame, tied to the reading by a generated kernel-checked equivalence; a `sorry` stub |
| Verdict | none (informational search only) | PROVED-FOR-ALL when a proof of the obligation is supplied, TESTED-ONLY while it is not, REFUTED when the search finds a counterexample and the kernel confirms it |
| Old glossary, hand-written step, hand-written Rust predicate | all three needed | none |

## Counts (final `./run.sh`, from scratch)

| | |
|---|---|
| Scenario verdicts | 39: 27 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 4 REFUTED, 1 UNBOUND, 1 VACUOUS. The 35 earlier scenarios are unchanged (24 / 6 / 3 / 1 / 1); 4 are new sentences (3 proved, 1 refuted) |
| Rule statements | 43: 27 PROVED-FOR-ALL, 14 REFUTED, 1 UNBOUND, 1 TESTED-ONLY. The 14 earlier rules are unchanged (10 / 3 / 1); 29 are new |
| New sentences | 4 scenarios and 29 Rule lines: 20 PROVED-FOR-ALL, 12 REFUTED, 1 TESTED-ONLY (its stub left as `sorry` on purpose) |
| Obligation ↔ reading | 46 of 46 kernel-checked (the 4 new scenarios and all 42 compiled Rule lines), standard axioms only, no proof of either side used |
| NEW ↔ OLD (older scenarios) | 34 of 34, as before, after the fixture texts of 7 retired idioms were reworded |
| Cucumber on compiled Rust | 49 step forms as composition trees (15 Given, 8 When, 26 Then), 0 hand-written steps; 18 rules, 90 scenarios (88 passed, 1 skipped, 1 failed, the same two as before), 400 steps |
| Lean pieces on the model vs Rust pieces on the compiled crate | 80 compiled readings, 665,264 of 665,264 evaluations agree |
| Pieces with a compared Rust reading | 91 of 91 (each through the readings that use it) |
| Frame definition vs checker | 29,622 of 29,622 on the fixtures (917 false, 0 silent); 3,281 of 3,281 on the hand-written and toy instances (677 false, 236 silent); every frame compared at both |
| Kernel refutation of false Rule statements | 14 of 14. 7 need the new general script: 3 that compare two calls, 1 about successful calls, 1 about rejected calls, 1 about a sequence, 1 whose scope is a "some X of XS" condition |
| Vocabulary | 94 entries a person would sign: 91 pieces (8 operations, 30 other domain words, 28 modifiers, 25 frames) and 3 idioms. Was 87: 77 pieces and 10 idioms. 0 signed |
| `./run.sh` | exit 0; 66 s for the final run from scratch at load 4, warm build outputs (earlier runs of this pass were at load 75 to 150 and are not timings) |

## The five held-out rules

All five are now in `features/ledger_rules.feature`. The four true ones are PROVED-FOR-ALL through a supplied proof of their generated obligation (n1, n2, n3, n5; each proof is four to seven lines from a hand-proved step lemma). The false one (n4) is REFUTED in the kernel at ledger `[18446744073709551615, 1]` with the empty batch, and the compiled Rust gives the same result there. n2 also has a scenario beneath it; the generated glue from that scenario does not prove the rule (it covers only the rejected half), so the rule rests on its own proof.

## The two-run and reference frames

Each has a sentence form, a true rule proved and a false rule refuted, on the ledger:

| Frame | True, PROVED-FOR-ALL | False, REFUTED |
|---|---|---|
| monotone | "A transfer never loses acceptance when the amount is smaller" | "... when the amount is larger" |
| agrees with a reference | "A lookup agrees with the reference lookup" | "A lookup agrees with the zero-default lookup" |
| independent of (same answer) | "A lookup gives the same answer when the ledger agrees at the account" | "A transfer gives the same answer when only the amount differs" |
| independent of, given the first answer (new) | "A transfer gives the same answer when the amount is larger, if it is rejected" | "..., if it is accepted" |
| containment, input and answer collections (new) | "For a batch, every transfer at which the batch stopped is a transfer of the batch" | "For a batch, every transfer of the batch is a transfer at which the batch stopped" |
| "some X of XS" as a condition (new modifier) | "A batch for which some transfer of the batch is valid on the ledger never changes the total ..." | "A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected" |

A second monotone rule ("A lookup never loses that there is a result when the ledger is extended") is true and left unproved on purpose: TESTED-ONLY.

## Private coverage recount

Counts and generic frame names only; judged by reading the pilot's descriptions, with no domain word of that system built and no sentence compiled. Of the 85 readings, **84 can now be said as a sentence** with the forms that exist, given domain words of kinds that exist (33 before: the 50 that needed monotone, agrees-with or independent-of had no sentence form, and 2 had no frame). By form: agrees with a reference 28; monotone 14; only if 11; every / no over a collection of the answer 11; always / never under a condition 9; same answer under a change of input 7; the result is 1; always answers 1; containment between an input and an answer collection 1; same answer given the first answer 1. **Not sayable: 1**, a monotone reading whose answer is a set (the second call's set must contain the first's); it needs containment between the answers of two runs, or a rule-level "for every item". About five of the 84 fold a nested quantifier into one domain word, which the grammar cannot spell out.

## Controls and the mutation run (full harness, one pipeline at a time, 2 h 32 min at load 6 to 150)

- **Controls: 35 of 35 as expected.** The 31 earlier ones, with their expected text following the new scenario count, the retired idiom in c14 and the word TESTED-ONLY for a Rule (c8, c17), and four new builder's controls:
  - c32 one Rust piece reading made wrong (`is not more than` made strict): PIECE READINGS DISAGREE on the readings that use it, and the boundary rows differ between Rust and model;
  - c33 the `flat:` template of `never changes` replaced by True: the three new scenarios that use it are NOT LINKED and TESTED-ONLY, never PROVED;
  - c34 a new sentence's proof replaced by `sorry`: the scenario and the Rule proved from it are TESTED-ONLY;
  - c35 a new Rule line about successful calls that is false: REFUTED by the general script, reproduced on the compiled Rust.
- **Mutants: 45 of 45 identical to the previous run on the 35 older scenarios** (verdict changes, changed rows, unit-test result, exit). A scenario is shown false of 43; `d6` and `la6` still fail only through a lost proof.
- **What the new sentences add under mutation:**
  - a new scenario is found false of 15 mutants and a row of `ledger_rules.feature` changes for 3, always where an older scenario already was shown false;
  - a Rule statement is newly found false of 33 mutants (30 before); never where no scenario is; for 10 mutants a scenario is shown false and no rule is (13 before);
  - of those 33, a newly false rule is refuted in the kernel for 14 (2 of 30 before the general script), and 26 of the 96 newly false (rule, mutant) pairs. The rest stay COUNTEREXAMPLE: the script could not close the goals at the mutant's counterexample;
  - the Lean-versus-Rust comparison of the readings stayed in agreement for every mutant, as it should: a mutant changes the Rust and the model together.
- **A cost the run showed:** the proof stub of a new sentence imports every lemma module of the ledger, so a mutant that breaks one lemma module (say the lookup's) costs every new sentence its proof, not only the sentences about that function. The older proof files import one module each.

## What did not work or is not done

- **The suite adequacy note and the input-coverage table do not see new sentences.** Both are generated from the flat statements of the old glossary.
- **A rule with no scenario has no Examples rows**, and a rule that compares two calls cannot have a scenario at all. On the compiled Rust such a rule is evaluated on generated inputs only.
- **The Rust readings are compared through compositions**, never one piece alone, and they share an author with the Lean pieces. Control c32 (one Rust reading made wrong) is the only test of the comparison's power in this pass.
- **The generated glue from scenarios is unchanged** and still fails where it failed (a parameter that names a computed number; a suite that covers one half of an "only if").
- **Kernel refutation still has gaps**: a sequence of more than two calls or without step lemmas, a two-run claim narrowed to accepted or rejected calls, a scenario with a bystander. None occurs in the fixtures.
- **Counting with a number has no sentence form.**
- **The README's own scenario is not reproduced word for word**: the rule is singular and names the ledger, and a transfer is one value where the README has three columns.
- **The old glossary is still in the tree** for the 34 older scenarios (their flat statements, their proofs, the adequacy note). Moving them onto generated obligations was not attempted.
- **0 of 94 entries are signed**, and nobody has read an echo.


# Addendum: layered evidence from one compiled rule (plan node E1, 2026-11-11)

Everything below is on the two toy crates. The generator, the typed piece readings, the generators' design, the two candidate
rules, their proof and the new controls were written by an agent; nothing is signed; no reader has seen the new block.

## What one rule yields now

From the composition tree that gives a sentence its Lean statement and its echo, `clausal gen` now also writes a property
test and a Kani harness (`evidence/`, generated; DESIGN.md section 16). No test code is written per rule. What they find
false is replayed on the Lean model and becomes a kernel-checked refutation, or a MODEL MISMATCH. The per-Rule block has an
evidence ladder. For the README's rule, from the final run:

```
Rule: An internal fund transfer never changes the aggregate account value of the ledger
  Reading   for a transfer: every ledger, every transfer (...); every such call, accepted or rejected [default D2]; assuming
            every account the transfer names is an account of the ledger (internal); then the call gives an answer [default
            D1]; the sum of the balances of every account of the ledger after the call equals the sum ... before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (24436 generated), none falsifies it (seed 20261111); of the 1
                     scenario beneath it, 1 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; NO ANSWER in 30 s with up to
                     6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.readme_internal_transfers.holds,
                     Rule.ledger_rules.readme_internal_transfers.from_scenarios: the rule statement for all inputs
                     and all sizes, from its scenarios; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model
  ...
  Rests on   (meaning / proof / translation / compilation, as before)
```

Two other shapes the ladder takes, both in the final report:

- **Property-test and bounded evidence only.** "A batch agrees with its transfers applied one at a time until one is
  rejected" (candidate 2 below; no proof supplied): 10,000 cases, none falsifies it; Kani verifies it at four rungs and gives
  no answer at 6 accounts and 4 transfers; proof: none. Verdict TESTED-ONLY; STRONGEST HELD "BOUNDED CHECK only: it holds
  at the sizes where Kani answered (listed above); it is NOT PROVED at any size where Kani gave no answer, nor beyond"
  (reworded after the step 3 review: the earlier text could be read as covering rungs that gave no answer).
- **A counterexample that came from a generated harness.** "A transfer never leaves the balance of account 4 of the ledger
  above zero" is false only of a ledger with five accounts; the reading search's grid has none (66 inputs, none falsifies
  it). The property test fails at its first case, shrunk to ledger `[0, 0, 0, 0, 1]` with `0->0:0`; Kani verifies the rule
  with up to 2 and up to 4 accounts and fails it with up to 6. The property test's input fails on the Lean model too and
  `Rule.ledger_rules.e1_fifth_account_empty.refuted` is kernel-checked. STRONGEST HELD "a kernel-checked REFUTATION: the
  rule is false (the input was found by the generated property test)".

## Counts (final `./run.sh` from scratch, exit 0, 10 min 39 s on a shared machine; `--quick` 2 min 23 s)

| | |
|---|---|
| Scenario verdicts | 39: 27 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 4 REFUTED, 1 UNBOUND, 1 VACUOUS. Unchanged |
| Rule statements | 46: 28 PROVED-FOR-ALL, 15 REFUTED, 1 UNBOUND, 2 TESTED-ONLY. The 43 earlier ones are unchanged (27 / 14 / 1 / 1); three were added |
| Readings with a generated property test and Kani harnesses | 83 of 83 (every compiled scenario and Rule line); 269 Kani harnesses |
| Property tests | 10,000 cases in scope each, seed 20261111: 63 not falsified, 19 shown false (the 4 refuted scenarios and the 15 false rules: every one the grid search finds, and the one it does not), 1 with no input in scope (the contradictory-Givens control), 0 did not finish; 25 s |
| Generated predicate against the tree evaluator | 2,405,688 generated cases, 0 differences |
| Kani, 30 s per harness, 6 at a time | 172 verified, 61 failed, 36 no answer; per reading: 47 hold at every rung, 17 hold at some rungs and give no answer at others, 19 shown false; 444 s wall-clock. Which rungs answer varies with the load: the full run before this one (10 min 44 s) had 171 and 37, and there the README rule's 4-account rung gave no answer |
| Falsifying inputs found | 38 (19 by the property test, 19 by Kani): 36 fail on the Lean model too, 0 MODEL MISMATCH, 2 not evaluated on the model (an account number above 4294967295 has no literal there) |
| Fed back as a counterexample the grid did not have | 1 (the control above) |
| Everything else | as in the previous addendum: 34 of 34 old ↔ new equivalences, 49 of 49 obligation ↔ reading, 666,584 of 666,584 Lean-versus-Rust evaluations over 83 readings |
| Vocabulary to sign | 96 entries (was 94): two reference words added. 0 signed |

## Against the K2 trade map (`compare/e1/E1_TRADES.md`)

The same 97 mutants and 23 rules as K2, the generated harnesses in place of the hand-written ones, on the compiled Rust.

| | Tool set (52 mutants) | Hand-written set (45) |
|---|---|---|
| (mutant, rule) pairs some K2 arm shows false | 212 | 97 |
| K2 hand-written property test (edge) / Kani | 212 / 209 | 90 / 89 |
| GENERATED property test / Kani ladder | 212 / 210 | 90 / 97 |
| GENERATED, either | 212 | 97 |
| Pairs a K2 arm found and the generated set did not | 0 | 0 |
| Pairs the generated set shows false and no K2 arm did | 0 | 0 |
| Mutants caught through none of the 23 rules, K2 / generated | 2 / 2 | 2 / 2 |
| ... with the two candidate rules added | 0 | 0 |

10 of the 212 tool-set pairs (8 under `cm-l34` and 2 under `cm-l14`, loops that never end) count as shown false only
because the property test did not finish in 30 s or Kani failed an unwinding assertion; neither gives a concrete failing
input (the property test names the input it was evaluating when the time ran out, which is not a demonstrated failure). K2
counted them the same way. Counting only a concrete input that fails, the generated set shows 202 of 212.

- The generated set finds every falsified rule the hand-written arms found.
- The ladder is what closes K2's Kani gap on the hand-written set (8 pairs missed for size, all found, at the rung
  TRADES.md predicted). It gives no answer for 2 tool pairs, which the generated property test finds; retried alone with
  120 s, one of the two is found.
- The magic-value mutants `d6` and `la6` are still found by Kani only: 7 pairs.
- Cost: no lines per rule; 395 + 594 lines of Rust and 1,272 of Python once. Per ledger mutant (median): 16 s of property
  tests for 68 readings, 126 s of Kani for 18 rules, 30 s to get and replay Kani's inputs.

## The two candidate rules, and the survivors

Both are sentences in `features/ledger_rules.feature`, through "agrees with a reference", where the reference is another
operation of the same code (two new domain words; DESIGN.md 16.6).

| | Unmutated code | `cm-l36`, `cm-l39`, `lw3` | `r4` |
|---|---|---|---|
| 1. A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied | PROVED-FOR-ALL (proof supplied by an agent, five builds) | shown false at the empty batch, by the property test and by Kani at the first rung | not shown false |
| 2. A batch agrees with its transfers applied one at a time until one is rejected | TESTED-ONLY on purpose; bounded check holds at four rungs | not shown false | shown false at a two-transfer batch, by the property test and by Kani at the second rung |

So the four mutants K2 found no rule for are all shown false now. They are shown false by two rules that compare one
operation of the code with another (`apply_all` against `apply_batch`; `apply_batch` against `apply`, once per transfer).
These rules catch disagreement between the operations, not a mistake the operations share. Candidate 1 is false of 24 of
the 66 ledger mutants and candidate 2 of 26.

## Feed-back on mutants (whole pipeline, a sample)

- `d6` (control c36) and `la6`: K2's only signal on the Lean side was a lost proof. Now the generated Kani harness finds the
  amount 1,000,003, it fails on the compiled Rust and on the model, and the scenario is REFUTED in the kernel with its
  source printed.
- `cm-l22`: the three-account case the Lean grid missed is found by the generated property test and is a COUNTEREXAMPLE on
  the model.
- `cm-l34` (a loop that does not terminate): nothing changes. The pipeline stops at step 5 before the generated harnesses run.
- No MODEL MISMATCH in any run on a real mutant. Control c38 makes one on purpose.

## Controls and the mutation run

Full harness, `python3 mutation/run_mutants.py --jobs 3`, 1 h 36 min on a shared machine (load 10 to 30). Every pipeline in
it runs with `--quick` (property tests, no Kani), except control c36 and a mutant run that shows no scenario false, which
is repeated with the bounded check.

- **Controls: 38 of 38 as expected**, the 35 earlier ones and three new builder's controls:

| Control | What is wrong | What must happen, and does |
|---|---|---|
| c36 | the magic-value mutant `d6` | the generated Kani harness finds amount 1,000,003; fed back; `deposit_with_room` is REFUTED with "source ... the generated bounded check (Kani)"; exit 1 |
| c37 | one typed piece reading is wrong (`the balance of account k` gives 1 for a missing account) | READING MISMATCH on the readings that use it; exit 1 |
| c38 | the Rust-side crates are built against a changed copy of the wallet; the translation still reads the original | MODEL MISMATCH: "the compiled Rust fails, the Lean model holds", beside the older PIECE READINGS DISAGREE; exit 1 |

  The older control c32 (one Rust piece reading wrong in `pieces.rs`) now also reports READING MISMATCH, since the typed
  reading and the tree evaluator then differ.

- **Mutants: 45 of 45 valid; a scenario is shown false of 45 of 45** (was 43). `d6` and `la6`, which until now failed only
  through a lost proof, are shown false at the input the generated Kani harness finds: `deposit_with_room` REFUTED;
  under `la6` eight scenarios, three of them REFUTED in the kernel and five COUNTEREXAMPLE (three of those are two-When
  scenarios, for which no kernel refutation is generated).
- **A counterexample that came from a generated harness and not from the grid search**: in 9 of 45 mutant runs, 32
  readings (14 from the property test, 18 from the bounded check). The bounded check ran for `d6` and `la6` only.
- **Rule statements newly found false**: 38 of 45 mutants and 123 (rule, mutant) pairs, 31 of them refuted in the kernel
  (was 33 mutants, 96 pairs, 26). Not broken down between the three added rule lines and the fed-back inputs.
- No MODEL MISMATCH and no READING MISMATCH in any mutant run.
- Not compared field by field with the previous run: this run overwrote `mutation/results.json`.

## What did not work or is not done

- **The bounded check is slow and often silent.** 36 or 37 of 269 harnesses give no answer in 30 s on the unmutated code; the
  rules about a conserved total stop answering at 4 accounts or at 3 transfers. The 37 of the earlier run, put to Kani again with 120 s each (exploratory,
  on a shared machine; `compare/e1/results/baseline_no_answer_retry_120s.json`), 18 of the 37 verify, in 38 to 97 s each, and
  19 still give no answer (the 6-account, 4-transfer rung of the total rules, and two batches in a row beyond one transfer
  each). `./run.sh` takes about 11 minutes with the bounded check and about 2.5 without (`--quick`).
- **Generic generators have a known blind spot** (a value that occurs only in the code) **and an unknown one** (structures
  they seldom draw). On these fixtures the only misses are the magic-value mutants. One false fixture rule (two transfers
  where the second is valid only after the first) was first found at case 1,857 of 10,000, and `r5` at 9,637.
- **A false rule can pass every layer.** A reviewer's probe, "For a batch, the number of transfers applied is at most 4",
  is false at ledger `[0, 0]` with five 0-amount transfers, and the compiled Rust fails there (replayed by the reviewer).
  The grid search (at most 4 transfers per batch) and the generated property test (10,000 cases, collections up to 6) did
  not find it. The Kani ladder cannot, because no rung has more than 4 transfers (the reviewer's probe run was `--quick`,
  so Kani was not put to it). Its verdict is TESTED-ONLY with STRONGEST HELD "PROPERTY TEST only ... NOT PROVED". The
  wording is right, but the rule is not flagged. The probe is in `review/step3/`; it is not in `features/`.
- **The typed piece readings are a third hand-written reading by the same author.** They are compared with the tree
  evaluator at every generated case, which is a test. Under Kani only the typed reading runs.
- **One stale Kani build** (after a mutant whose loop does not terminate) gave a wrong "failed"; the replay on the compiled
  Rust did not reproduce it, which is how it was caught. A stale build that wrongly VERIFIES would not be caught that way.
- **Inputs with an account number above 2^32 - 1 are not fed back**: the model has no literal for them. Kani picks such
  numbers freely. 2 of 38 in the final run.
- **No kernel refutation for a reference that is another operation** (the candidate rules under a mutant stay
  COUNTEREXAMPLE), nor for a two-When scenario (as before).
- **The feed-back cannot run where the model cannot be evaluated** (`cm-l34`, `cm-l14`, `cm-l26`): the pipeline stops first.
- **Not frozen before data, and the mutants were known**: see the top of `compare/e1/E1_TRADES.md`.
- **The suite adequacy note still does not see new sentences**, so the two candidate rules do not appear in it, although
  candidate 1 is exactly the progress rule it reports missing for `apply_all`.
- **Sign-off**: 0 of 96 vocabulary entries. Two more are unsigned and questionable by design (references that mention the
  model).
- The root README and `docs/` were not edited (outside `clausal/`).


# Addendum: review of step 3 (new sentences, layered evidence, trials) and fixes, 2026-11-11

An independent reviewer reran all three steps in scratch copies. Nothing was fabricated and no verdict changed. Seven
write-up statements were wrong or overstated, one limit of the layered evidence was not reported, and two printed
messages misled. All were applied; none was disputed. Everything is still on the two toy crates.

## What changed

| # | What was wrong | Fix |
|---|---|---|
| 1 | A false rule can pass every generated layer, and this was not reported | Reported in the E1 addendum above ("What did not work"), in `compare/e1/E1_TRADES.md` (Limits) and in `README.md`. The probe ("For a batch, the number of transfers applied is at most 4": false with five 0-amount transfers) is in `review/step3/`, not in `features/` |
| 2 | "Shown false" for 212 of 212 tool-set pairs includes 10 with no concrete failing input (loops that never end) | Stated under the table above and in `E1_TRADES.md`: 202 of 212 by a concrete input that fails. Recounted from `compare/e1/results/pairs.json` |
| 3 | "The four survivors are all shown false now" did not say how | The two candidate rules compare one operation of the code with another; they catch disagreement between the operations, not a shared mistake. Said where the claim is made |
| 4 | The Rust piece readings were described as a second reading | `DESIGN.md` 15.1 and the header of `wallet-bdd/src/pieces.rs`: a second implementation by the same author, changed together with the Lean pieces when a meaning changed; agreement shows consistency, not independent confirmation |
| 5 | `gen` printed "nothing is stated or proved for it" for 30 rules that do get a statement and a verdict, and printed the old glossary's UNBOUND for sentences the vocabulary reads | `clausal/pipeline.py`: the note now says the rule line is compiled, searched, run and given a verdict; the old-glossary lines are prefixed "(old glossary only; this sentence is read by the vocabulary)" |
| 6 | STRONGEST HELD "holds within the sizes given" could be read as covering rungs where Kani gave no answer | `clausal/rules.py`: "it holds at the sizes where Kani answered (listed above); it is NOT PROVED at any size where Kani gave no answer, nor beyond" |
| 7 | `README.md` said 38 domain words and 94 entries | 40 and 96 (8 operations, 32 other domain words, 28 modifiers, 25 frames, 3 idioms) |

The corrections to the trials write-up (K1's weakest kind, what two of the three false alarms are, the comparison with
K1, the word counts) are in `../trials/sentences/RESULTS.md` and the bank's `analyst_notes.md`.

## Rerun

- `./run.sh` from scratch: exit 0, 11 min 16 s. 39 scenarios (27 / 6 / 4 / 1 / 1) and 46 rule statements (28 PROVED-FOR-ALL,
  15 REFUTED, 1 UNBOUND, 2 TESTED-ONLY), as before. All 913 graph nodes have the status they had before the fixes; against
  the committed graph, 0 of 862 shared nodes changed.
- Kani in this run: 170 verified, 61 failed, 38 no answer (172 / 61 / 36 in the run reported above). The README rule's
  4-account rung gave no answer this time, so its bounded rung reads "holds with up to 2 accounts". Which rungs answer
  depends on the load; what is shown false does not.
- **Full mutation harness rerun** (the comment change in `pieces.rs` changes the digest the report uses to tell whether
  the mutation results belong to the tree): `--jobs 2`, 2 h 2 min, load 8 to 20. 38 of 38 controls as expected; a scenario
  shown false of 45 of 45 mutants. Compared field by field with the previous `results.json`: identical for every mutant
  and every control (only the timestamp and the digest differ). The previous file is `build/step3_final/results.before.json`.
- A second `./run.sh` from scratch after the harness: exit 0, the same counts, every node status the same; the report no
  longer marks the mutation run out of date.

## Still open from the review

- **The probe is not a standing control.** A false rule that no layer flags would be a useful fixture with an expected
  verdict of TESTED-ONLY, so that a wider generator or a taller ladder shows up as a change. Not added: it changes the rule
  counts every control text depends on.
- **No size limit is printed as a warning.** The ladder and the generator sizes are printed on each rung, but a rule whose
  subject can be larger than every size tried gets no extra flag.
- **The bounded-check line lists rungs awkwardly** when two rungs in a row give no answer ("NO ANSWER in 30 s with up to
  4 accounts; with up to 6 accounts").


# Addendum: sizes tried and the standing probe (plan node E2), 2026-11-12

Review finding 1 above ("a false rule can pass every generated layer, and the rule is not flagged") is now acted on.
Design: `DESIGN.md` section 17. Code: `clausal/sizes.py`.

## What changed

- A statement about a collection of open length that is neither proved for all inputs nor shown false now carries the
  flag `LARGER INPUTS NOT EXAMINED`, with the largest size each layer tried in that run. Its verdict line reads
  `TESTED ONLY (...; NOT PROVED; LARGER INPUTS NOT EXAMINED: see sizes)`. No verdict code changes.
- A standing probe is in `features/ledger_rules.feature` (`e2_probe_at_most_six`), expected TESTED-ONLY with the flag,
  and tagged `@must-flag-larger-inputs`: the run fails if the flag is not on its verdict.
- Control `c39` removes the flag; the checks named E2 in `python3 -m clausal.selftest` cover the rule that decides it (see the fix round below for `c40` to `c42`).

## What did not work

- **The reviewer's probe could not be the standing fixture.** "For a batch, the number of transfers applied is at most
  4" was added first, expected TESTED-ONLY with the flag, committed before any run (ae738db). The first
  `./run.sh --quick` REFUTED it: the generated property test found a batch of five applied transfers at generated input
  4218 (seed 20261111, rule id `Rule.ledger_rules.e2_probe_at_most_four`), and the kernel confirmed the refutation. The
  reviewer's run of the same sentence under another id found nothing in 10,000 cases. Whether the property test finds
  this probe depends on the rule id, because each rule's random stream is seeded from the run seed and the id.
- The expectation was not edited and the id was not changed. The probe in `features/` is now "... is at most 6", false
  only at seven or more transfers, which no layer tries (grid 4, ladder 4, property test 6). Its expectation was
  committed before its first run (1096c78).

## Run (one full `./run.sh`, load average 14 to 17, other agents building)

- Exit 0, 655 s. 39 scenarios: 27 PROVED-FOR-ALL, 6 PROVED-INSTANCE, 4 REFUTED, 1 UNBOUND, 1 VACUOUS (as before).
- 47 rule statements (46 before): 28 PROVED-FOR-ALL, 15 REFUTED, 1 UNBOUND, 3 TESTED-ONLY (2 before). The 46 earlier
  rule statements, the 39 scenarios and the 12 function verdicts have the code they had in the baseline of 5e6cfa7.
- Flagged: 3 of 47 rule statements (`mono_extended_ledger`, `k2_batch_agrees_with_transfers`, `e2_probe_at_most_six`),
  0 of 39 scenarios.
- The probe: grid search 297 inputs, no counterexample; property test 10,000 cases, none falsifies it; bounded check
  verified at all five rungs (1.1 to 2.7 s each). Every layer passes a false rule, and the report says how far each went.
- Property tests: 84 readings (83 before); 64 found nothing, 19 shown false, 1 had no input in scope.
- Bounded check: 274 harnesses (269 before); 181 verified, 61 failed, 32 no answer in time.
- Graph: 914 nodes, 1,444 edges (913 and 1,443 before).
- Controls rerun: `c39`, `c12`, `c18`, `c20`, `c34`, each as expected (336 s). Under `c12` (the shared lemma module does not compile) 27 rule
  statements and 17 scenarios are flagged.

## Not done

- The full mutation harness was not rerun. The fixture changes the digest, so the report marks the stored mutation run
  out of date. 34 of the 39 controls and all 45 mutants have not been run against this tree.
- The flag is about collection length only, not about integer ranges.

## Fix round on the E2 addendum (review by another model), 2026-11-12

Two defects in the step above, both confirmed and fixed (DESIGN.md 17.5).

- **The guard could be removed together with the flag.** With the loop that calls `sizes.apply` emptied, or `apply`
  returning at once, the probe read as a clean TESTED ONLY and the run exited 0. A separate check (`clausal/mustflag.py`,
  on `out/graph.json` and the rendered rule blocks, sharing no code with `sizes.py`) now fails the run. The reviewer's
  two patches, applied to scratch copies: exit 1 each, four `EXPECTED FLAG MISSING` errors naming the probe. Controls
  `c40` and `c41` are those patches; `c39` to `c42` rerun, each as expected (265 s).
- **The property-test size was understated for two-call rules.** It was reported as 6 items; the second call of a
  two-call rule is drawn with up to 8 accounts or 7 transfers. The runner now records, per reading, the longest
  collection its generators can produce and the longest it drew in scope. In the full run 7 rule statements have a
  limit of 8 accounts; 2 of them drew 8 among the cases in scope (`mono_extended_ledger`, `same_answer_at_account`),
  the other 5 drew at most 6. Of the 3 flagged statements one changed: `mono_extended_ledger` now reads "at most 8
  accounts"; the probe and `k2_batch_agrees_with_transfers` read 6 accounts and 6 transfers, as before. The run fails
  if a drawn collection exceeds the stated limit (control `c42`).
- One full `./run.sh`: exit 0; 39 scenarios and 47 rule statements with the same verdict codes as before the fix; 3
  flagged. Four bounded-check rungs answered differently from the previous full run (one timeout became verified, three
  verified became timeout, at 30 s per rung under load); no verdict depends on them.
- Not covered by any control: taking the tag off the fixture, or removing the call to `mustflag.check`.
- The stored mutation run is still out of date (not rerun in full).
