# L2: three pieces the Clausebook lacked

Plan node L2 (`docs/PLAN.md`, track L). The proxy trial of 48 sentences (`trials/sentences/RESULTS.md`) found three
kinds of claim that five rules each needed and the book could not say. This node adds one piece for each, in core.
The freeze written before any run is `FREEZE.md`; this file is the design note and the results. Run every command
from `clausal/`.

## Result

- **Three pieces, four entries, five forms, all in `core.yaml`.** `equals` (and its negation), `each_at_most`
  (frame 17), `tied` with the tie `same_input`. `clausal book check` reports the same 21 violations as before; the
  new forms add none.
- **Ten fixture rules, each with the verdict frozen for it**: 5 true, all PROVED-FOR-ALL by a hand-written proof of
  the generated obligation; 5 false, all REFUTED in the kernel at an input that also fails on the compiled Rust.
- **Every verdict code of the baseline is unchanged** (97 of 97); the run now has 107.
- **`tied` covers one of the three ties the trial named.** "The same input again" is built. "The reverse" needs a
  domain word of the new category `tie` (none is built). "The two in the other order" is a comparison of two
  sequences, one of the eleven smaller pieces (judged in `FREEZE.md`, not built).
- **No trial sentence compiles as written, before or after** (0 of 48). The literal words of the five forms occur in
  none of the 48.

## The pieces

| | `equals` | `each_at_most` | `tied` (+ `same_input`) |
|---|---|---|---|
| Kind of claim | a comparison of two values known before the call | a bound on every number of a collection of the state, after the call | a sequence of two calls whose second input is got from the first |
| Kind of piece | modifier, a condition | frame 17 | modifier on the operation; `same_input` is a word of the new category `tie` |
| Book | core | core | core |
| Why core | names no sort or type: `term<T>` on any one sort. The values are the packs' | uses `nums`, the category "the total of" already sums. The collections are the packs' | stated of any two operations with one input type. A tie about one project's inputs would go to a pack |
| The one form | `{a:term<T>} equals {b:term<T>}`; negated: `{a:term<T>} differs from {b:term<T>}` | `each of {ns:nums} is afterwards at most {t:term<num>}` | `{op} with {t:tie}`, after a sequence; `same_input`: `the same input` |
| Position | any Given, "for which", "whenever", "only if", "exactly when" | a Then; in a Rule line through "for <subject>, <claim>" (it has no verb phrase) | the subject of a Rule line |
| Lean | `{a} = {b}` (Lean's equality, as `is` uses) | `Frames.EachAtMost`, `Frames.EachAtMost.at` (`lean/Frames/Frames.lean`) | `Frames.Op.tied`, `Frames.sameInput` (`lean/Frames/Core.lean`); `Frames.Op.tied_andThen_some` for generated glue |
| Second reading in Lean | none of its own: a condition is decided by its `Decidable` instance. Toy comparison against `==` (`FrameToyTests.lean`) | `Frames.Check.eachAtMost` (`lean/Frames/Check.lean`), compared with the definition at every grid point of every reading that uses it, and on the toy operation | none in the library. Toy comparison against a program that runs the two calls (`FrameToyTests.lean`) |
| Rust readings | `pieces.rs` `eval`; generated typed reading in `evgen.py` | `pieces.rs` `frame_content`; `evgen.py` `frame` | `pieces.rs` `tie`, `call_inputs`; `typed.rs` `tie_same_input`; `evgen.py` `run_code` |
| Compared on generated inputs | the scope bit of every grid point (Lean against compiled Rust); every property-test case (typed reading against tree evaluator) | the claim bit, same two comparisons; definition against checker in Lean | the claim bit of every tied reading, same two comparisons |

### `equals`

- The existing comparisons set a quantity of the state against a value (`is`, `more_than`, ...). None sets two
  values against each other, so "the sender is the receiver" and "the amount is zero" had no form.
- It is equality only. An order between two values known before the call is not built; nothing asked for it.
- It does not share the skeleton of `is` ("{} is {}"), which already has a recorded violation with `result_is`.
- **Ambiguity it can meet.** A written amount is read both as a number and as a value that may be absent
  (`amount_value`, `amount_result`). "the amount equals the amount" therefore has two readings and is refused. A
  sentence with one side of a single sort ("... equals zero", "the sender of ... equals the receiver of ...") has one.
- **It cannot compare a quantity of the state.** A measure is not a `term`. Row 6 of the eleven (a coercion from a
  measure to a value known before the call) would allow it.

### `each_at_most`

- Reads the collection after the call and the bound before it, like frame 10 (`at_most`) and frame 11 (`every_of`).
- An empty collection satisfies it; with the default the call must still give an answer (the toy test has that case).
- **Only "at most".** "at least" would be a second frame; nothing in the trial classification needs it on these
  fixtures (a balance is never below zero).
- **Why not a new domain word "every balance".** The ledger pack already has `{l:ledger}'s balances` as a `nums`.
  The frame takes that, so the wallet's "all balances" works too and no pack entry was added.
- In a Rule line it is written "For <subject>, each of ... is afterwards at most ...". It has no verb phrase, so it
  adds no second voice (check 3b).

### `tied`

- **What was refused before, and still is without a tie.** A sequence of two operations takes a pair of unrelated
  inputs. If both operations call their input by the same role name ("the amount"), the subject is refused: which of
  the two is meant? "A deposit followed by a withdrawal ..." is UNBOUND today, as before.
- **What the tie does.** `Op.tied op tie` runs the sequence `op` on `(a, tie a)`. The sequence has ONE input, the
  first call's, and the first operation's role names it. Every such sequence is in the claim; nothing is narrowed.
- **Why a function and not a condition on the pair.** `(A followed by B) for which the second input equals the
  first` says the same thing, but generated inputs then almost never meet the condition, and the role names still
  clash. A function leaves nothing to generate.
- **Composition.** `tied` is said of a sequence: "A followed by B with <tie>" is `tied(and_then(A, B), tie)`, and the
  reading lists `and_then`, `tied` and the tie among its pieces. `and_then` keeps its one form.
- **Refused, with the reason (ILL-TYPED):** a tie on three operations; on an operation with no input; on two
  operations whose input types differ; a tie that names another input type (`input:` of a tie entry).
- **Refused, with the reason (UNSUPPORTED, code NARROWED-TIE): a narrowing word on a tied sequence** ("An accepted
  deposit followed by a withdrawal with the same input ...", "A rejected transfer followed by a transfer with the
  same input ..."). The word stands before the first operation and reads as said of the FIRST call. The answer of a
  sequence is its LAST call's (`Frames.Op.andThen`: `accepted := second.accepted`), so the Lean would narrow on the
  last call. The two differ: at wallet `2^64 - 1`, amount `1` the deposit is rejected and the withdrawal accepted;
  at ledger `[1, 0]`, transfer `0->1:1` the first transfer is accepted and the second rejected
  (`NarrowedTie.lean` beside this file evaluates both on the model). The word is not dropped and not moved to the
  other call. The book has no form that says which call of a sequence is accepted or rejected, so a claim about
  "the sequences whose first call is accepted" or "in which both calls are accepted" cannot be written; see Limits.
  This was found by review after the first L2 commit, which compiled these sentences to the last-call reading.
- **Echo.** The "applies to" line names the sequence with its tie and lists one input. Two notes follow the claim:
  the sequence note of `coverage:`, and the tie's own line.
- **Not built:** a form that narrows a sequence by the answer of one named call, or of both; a tie in a scenario (two Whens with the same `<parameter>` are still refused); a tie on a two-call
  comparison of sequences; any tie but `same_input`.

## What changed in the compiler and the pipeline

| File | Change |
|---|---|
| `clausebook/core.yaml` | the four entries; the category `tie`; `nums` described as "to be totalled, or bounded one by one" |
| `clausal/vocab.py` | `nums` may fill a frame hole; `tied`'s subject form is read (`_surface`, `subjects`); the tie is echoed (`echo_rule`) and written back (`subject_text`); the UNBOUND message of a Rule clause lists `[with <tie>]` |
| `clausal/oblig.py` | the flat obligation of a tied sequence (the second call written on the tied input; glue through `Frames.Op.tied_andThen_some`). Two changes to the generated REFUTATION script, both kernel-checked glue: the equation is stated about the unscoped operation before the run lemma is applied; a sequence of two `&mut self` functions with no hand-proved step lemma is stepped through at the concrete input |
| `clausal/rsearch.py`, `clausal/trees.py` | a tied sequence has one grid variable for its input; the tree of the unit carries the tie's id |
| `clausal/evgen.py`, `evidence/src/typed.rs` | typed readings of `equals`, `each_at_most`, `tie_same_input` |
| `wallet-bdd/src/pieces.rs` | `equals`, `each_at_most`, `tie`, `call_inputs` |
| `lean/Frames/*.lean`, `lean/Run/FrameToyTests.lean` | the definitions, the checker, the lemma, 9 toy lines |
| `features/ledger_rules.feature`, `features/wallet_rules.feature` (new) | 8 and 2 Rule lines |
| `lean/Wallet/RuleProofs/{ledger_rules,wallet_rules}/l2_*.lean` | 5 hand-written proofs |
| `clausal/selftest.py` | 5 removal controls for the new forms, 2 checks of the tie and of the ambiguity of `equals`; the count of core's pieces; fix round: 4 lines with a narrowing word on a tied sequence are refused as NARROWED-TIE |
| `clausal/vocab.py`, `clausal/vreport.py` (fix round) | `Compiler.subjects` refuses a narrowing word on a tied sequence (`narrowed_tie`); the report says why no statement was generated |
| `clausebook/l2/NarrowedTie.lean` (fix round) | the two inputs at which the first-call and the last-call reading of such a sentence differ, evaluated on the model |

The refusal message of one existing sentence changed (`Rule.wallet.interest`, expected UNBOUND, still UNBOUND): its
grammar line now mentions the tie. No other compiled reading, echo or refusal differs from the commit before L2.

## Results

All measured 2026-11-12. The fix round (a narrowing word on a tied sequence is refused) reran the book check, the selftest, the removal sweep, the comparison of readings, the `--quick` run and the one full run on its tree; the rows below give those results where they are printed by these, and no number other than the two bounded-check rows changed. The 48 sentences were rerun as written (0 of 48, all UNBOUND, as before). The toy comparison and the mutation sample were not rerun in the fix round (no Lean library file, fixture or control changed). The baseline is the run of commit `5e6cfa7` kept by the
orchestrator (`graph.json`, `report.md`); "before L2" is commit `5a8f799`.

| What | Result | Command |
|---|---|---|
| `clausal book check` | 136 surface forms (131 before L2); 21 violations, exactly the recorded ones (0 new); core stands alone; `lean/Frames` builds alone | `python3 -m clausal book check --lean` |
| Forms that are an instance of another piece's skeleton (informational, not a violation) | 104 (98 before). The 6 new: "agrees with {r}" and the two forms of `w.rejected_with` are instances of "{op} with {t:tie}"; the form of `each_at_most` is an instance of the forms of `is`, `result_is` and `at_most` | `python3 -m clausal book check --json` |
| Term lock | 121 sentences (111 before); the 111 unchanged; 10 added | `git diff 5a8f799 -- clausebook/terms.lock.json` (insertions only) |
| Compiled readings against the commit before L2 | 95 compilations (85 before): 93 compiled, 2 refused. 11 differ: the 10 new rules, and the refusal message of `Rule.wallet.interest` (same status). Echo of every other reading identical | `python3 compare/against/readings.py 5a8f799` |
| Toy comparison, definition against second reading | `each_at_most`: 60 of 60 evaluations agree (18 false, 12 silent). `equals`: 40 of 40 (8 false, 8 silent). `tied`: 80 of 80 (40 false, 20 silent) | `( cd lean && lake env lean Run/FrameToyTests.lean )` |
| Selftest | all checks pass, among them the 5 new removal controls, the 2 new L2 checks and (fix round) the refusal of 4 lines that narrow a tied sequence | `python3 -m clausal.selftest` |
| Fix round: where the two readings of a narrowed tied sequence differ | wallet `2^64 - 1`, amount `1`: deposit alone Err; tied sequence Ok, balance `2^64 - 2`; that answer counts as accepted; balance unchanged: false. Ledger `[1, 0]`, `0->1:1`: transfer alone accepted, `[0, 1]`; tied sequence rejected, `[0, 1]`; ledger unchanged: false | `( cd lean && lake env lean ../clausebook/l2/NarrowedTie.lean )` |
| Removal sweep | 255 removals (246 before); 0 leave a sentence that uses the entry unchanged; 11 change no recorded term, none of them an L2 entry or form | `python3 mutation/removal_sweep.py` |
| Controls the book check stops | c39 to c42, as meant | `python3 mutation/check_controls.py` |
| Verdict codes, `--quick` run | 97 of 97 identical to the baseline; 10 new, each as frozen | `python3 compare/against/verdicts.py <baseline graph.json>` |
| Verdict codes, the one full run | 97 of 97 identical to the baseline; 10 new, each as frozen. 39 scenarios as before; 56 Rule statements: 33 PROVED-FOR-ALL, 20 REFUTED, 1 UNBOUND, 2 TESTED-ONLY (46 before: 28, 15, 1, 2). Exit 0 | `../tools/sem.sh 3 -- ./run.sh`; same comparison |
| Definition against executable reading, all fixture readings | 30713 of 30713 evaluations agree | printed by the run |
| Lean pieces against the Rust readings, on the grid | 93 of 93 compiled readings (83 before); 668081 of 668081 evaluations agree | printed by the run |
| Generated property tests | 93 readings, 10000 cases in scope each, seed 20261111: 68 found nothing, 24 shown false, 1 had no input in scope (not an L2 rule), 0 READING MISMATCH (typed reading against tree evaluator) | printed by the run |
| Bounded checks (Kani), full run | 295 harnesses: 192 verified, 74 failed, 29 no answer in 30 s, 0 error (the full run of the fix round; the run of the first L2 commit had 190, 74, 31) | printed by the run |
| Bounded-check rungs that answered differently from the baseline, among the 83 readings it had | 2 in the full run of the fix round. `Rule.ledger.batch_total`: "up to 4 accounts and up to 1 transfer" verified then, no answer in 30 s now. `Spec.ledger.batch_conserves`: the same rung, no answer then, verified now. (The run of the first L2 commit differed in 4 rungs: `Rule.ledger.batch_total`, `Rule.ledger_rules.some_valid_conserves`, `Spec.ledger.whole_conserves` at that rung, verified then and no answer in that run; `Spec.ledger.batch_then_total` at "up to 2 accounts and up to 3 transfers", the other way.) | `python3 compare/against/bounded.py <baseline graph.json>` |
| Falsifying inputs fed back from the generated harnesses | 48; 45 fail on the Lean model too; 3 are not evaluated on the model (2 of them belong to rules that were there before L2; the third is the bounded-check input of `l2_distinct_accounts_accepted`, whose rule is refuted at two other inputs); 0 MODEL MISMATCH | printed by the run |
| Generated glue scripts that fail | 9 error lines in `out/links.log`. 7 were there before L2 (4 scripts). 2 are the first-choice refutation scripts of `l2_distinct_accounts_accepted` and `l2_each_within_amount`; the general script proves both rules false | `grep -c ': error:' out/links.log` |
| The 48 frozen sentences, as written | 0 of 48 compile before L2; 0 of 48 now | `bash clausebook/q4/sentences.sh 5a8f799` |
| Literal words of the new forms in the 48 | 0 sentences for each of: "equals", "differs from", "each of", "is afterwards at most", "followed by ... with", "the same input" | `python3 clausebook/l2/coincide.py` |
| Mutation harness, a sample only | the harness's own baseline run passes (39 scenarios as expected); controls c18 and c32 as expected; mutants d1, la1 and la4 are each still shown false by a scenario. 5 of 73 items: the full harness was NOT rerun, and `mutation/results.json` is the run of before L2 | `../tools/sem.sh 3 -- python3 mutation/run_mutants.py --only d1,la1,la4,c18,c32 --jobs 3` |

### The ten rules

Every rule below has no scenario beneath it. "Grid" is the reading search on the Lean model, repeated on the
compiled Rust; "bounded" is the full run's Kani ladder.

| id | Sentence | Verdict (as frozen) | How |
|---|---|---|---|
| `l2_same_account_rejected` | A transfer for which the sender of the transfer equals the receiver of the transfer is rejected and changes nothing | PROVED-FOR-ALL | hand proof from `ledger.Ledger.apply.spec`; 11 of 66 grid inputs in scope; property test 10000 in scope of 53569 generated; bounded: holds at 2, 4 and 6 accounts |
| `l2_zero_amount_rejected` | A transfer for which the amount of the transfer equals zero is always rejected | REFUTED | false at ledger `[0, 0]`, transfer `0->1:0`: found by the property test on the compiled Rust (generated input 182, shrunk), fails on the Lean model, refuted in the kernel. The grid has no input in scope. Bounded: false at `[18446744073709551615, 0]`, `1->0:0` |
| `l2_distinct_accounts_accepted` | A transfer for which the sender of the transfer differs from the receiver of the transfer is always accepted | REFUTED | false at ledger `[]`, transfer `0->1:1` (grid; reproduced on the compiled Rust; kernel, `.refuted2`). Property test: `[0, 0, 0]`, `1->2:1` |
| `l2_each_within_maximum` | For a transfer, each of the ledger's balances is afterwards at most the maximum | PROVED-FOR-ALL | hand proof (a u64 is at most the maximum; the call answers); bounded: holds at 2, 4 and 6 accounts |
| `l2_each_within_total_bound` | For a transfer for which the total of the ledger's balances is at most the amount of the transfer, each of the ledger's balances is afterwards at most the amount of the transfer | PROVED-FOR-ALL | hand proof from conservation of the total in `apply.spec` and `List.single_le_sum`; 29 of 66 grid inputs in scope; property test 10000 in scope of 24634 generated; bounded: holds at 2, 4 and 6 accounts |
| `l2_each_within_amount` | For a transfer, each of the ledger's balances is afterwards at most the amount of the transfer | REFUTED | false at ledger `[2, 1]`, transfer `0->1:1` (grid; reproduced on the compiled Rust; kernel, `.refuted2`). Bounded: `[5, 9223372036854775824]`, `0->1:5` |
| `l2_twice_conserves` | A transfer followed by a transfer with the same input never changes the total of the ledger's balances | PROVED-FOR-ALL | hand proof, `apply.spec` twice; bounded: holds at 2 accounts, no answer in 30 s at 4 and 6 |
| `l2_twice_changes_nothing` | A transfer followed by a transfer with the same input never changes the ledger | REFUTED | false at ledger `[1, 0]`, transfer `0->1:1` (grid; reproduced on the compiled Rust; kernel, `.refuted2` through the step lemma of each call) |
| `l2_deposit_then_withdraw_answers` | A deposit followed by a withdrawal with the same input always answers | PROVED-FOR-ALL | hand proof, stepping through both model functions; bounded: holds (no size bound) |
| `l2_deposit_then_withdraw_restores` | A deposit followed by a withdrawal with the same input never changes the wallet's balance | REFUTED | false at wallet `18446744073709551615`, amount `1` (grid; reproduced on the compiled Rust; kernel, `.refuted2` by stepping through both functions). Property test and bounded check: wallet `9223372036854775808`, amount `9223372036854775808` |

The five REFUTED rules are the "toy case where the sentence is false" of each piece: `equals` two (one through its
negated form), `each_at_most` one, `tied` two (one per fixture).

### Limits and things to distrust

- **A tied sequence cannot be narrowed by what its calls answer.** A narrowing word on it is refused (see `tied`
  above). A rule of the kind "A, then B with the same input, restores the state when both are accepted" therefore
  has no reading: it can only be stated of every such sequence (where it is usually false, as
  `l2_deposit_then_withdraw_restores` is) or scoped by a condition on the state and input before the first call.
  L4 will meet trial rules of this kind; the piece they need is a narrowing that names the call, and it is not built.
- **The same word on a sequence WITHOUT a tie is still read as before L2, as said of the last call.** "A rejected
  transfer followed by a lookup never changes the ledger" compiles to `((L.apply).andThen L.lookup).rejected`:
  sequences whose LOOKUP is rejected. That reading was fixed in the review of Q1/Q2 (the `sequence` line of
  `coverage:` prints it, and the selftest holds it); it is not changed here, because it is not L2's and three
  selftest controls and the coverage check rest on it. A reader can misread it in the same way. Whether to refuse
  it too is left to the orchestrator.

- **Both readings of each piece have one author.** Agreement on generated inputs shows consistency, not independent
  confirmation, as for every other piece.
- **`equals` and `tied` have no second reading in the frame library.** Their Lean-side comparison is the toy file
  only (40 and 80 evaluations). On the fixtures they are compared Lean against Rust.
- **`l2_each_within_maximum` cannot be false of any code that answers**: a balance is a u64 and the bound is its
  maximum. It is proved, and it is weak. `l2_each_within_total_bound` is the rule that needs the code to be right.
- **The grid had no input in the scope of `l2_zero_amount_rejected`** (no sampled transfer has amount 0). It was
  refuted through the generated property test's input, replayed on the Lean model. Without the Rust evidence step
  (`--no-rust`) it would not be refuted.
- **The first-choice refutation script fails for two of the five false rules** (`l2_distinct_accounts_accepted`,
  `l2_each_within_amount`); the general script (`.refuted2`) proves both. These are two of the glue failures the run
  prints.
- **The new refutation path for sequences was written for the wallet rule and is exercised by that one rule.**
- **The mutation harness was not rerun.** No control text depends on the count of Rule statements (they match
  "39 scenarios: ...", unchanged), and `mutation/check_controls.py` passes; whether a mutant's verdict table changes
  with ten more rules was not measured.
- **Whether the three pieces serve the trial rules that needed them is not measured here** (that is L4). `tied` with
  `same_input` cannot serve the rules that need the reverse or the other order.
- **Seen by accident.** After the forms were written, a search of the repository for a message text printed the
  first words of about ten trial sentences from `trials/sentences/results.json`. No form or fixture sentence was
  changed afterwards; the wallet fixture ("a deposit followed by a withdrawal") was taken from the scout's brief.

## Reproduce

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
python3 -m clausal book check --lean                 # core alone; the lint (21 violations, as recorded); the term lock (121)
python3 -m clausal.selftest                          # among others: the 5 removal controls of the new forms, the tie checks
( cd lean && lake env lean Run/FrameToyTests.lean )  # FTEST lines of each_at_most, equals, tied
python3 mutation/removal_sweep.py                    # every entry and form taken out in turn
( cd lean && lake env lean ../clausebook/l2/NarrowedTie.lean )   # fix round: where "accepted" on a tied sequence would be read two ways
python3 clausebook/l2/coincide.py                    # literal words of the new forms in the 48 frozen sentences (keys only)
bash clausebook/q4/sentences.sh 5a8f799              # the 48 as written, before and after L2 (its last step fails: see below)
python3 compare/against/readings.py 5a8f799          # compiled readings against the commit before L2
../tools/sem.sh 3 -- ./run.sh                        # the full run
python3 compare/against/verdicts.py <baseline graph.json>
python3 compare/against/bounded.py <baseline graph.json>
```

`sentences.sh` ends with a step that rewrites the Q4 rewordings; it assumes its "before" revision is older than Q4
and stops with a Python error when given `5a8f799`. The two "as written" blocks it prints first are the measure.
