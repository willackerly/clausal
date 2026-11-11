# E1: the generated harness set beside the K2 trade map

2026-11-11. Plan node E1 (`docs/PLAN.md`). `../TRADES.md` (K2) compared four kinds of evidence for 23 rules, with a
property test and a Kani harness WRITTEN BY HAND for each rule. Here the property test and the Kani harness of each rule
are GENERATED from the composition tree that also gives the rule its Lean statement (`../../slicegen/evgen.py`,
`../../evidence/`; `../../DESIGN.md` section 16), and run on the same mutants. The question: does the generated set find
every falsified rule that the hand-written arms found?

- **Same mutants, same rules, same unit.** The 52 mutants of cargo-mutants 27.1.0 and the 45 hand-written ones of
  `../mutants/`; the 23 universal rules of `../rules.json`, read from the current feature files (their wording changed
  since K2's snapshot when seven idioms were retired; every one is kernel-proved equivalent to its old flat statement). A
  (mutant, rule) pair counts when the rule is shown false of the mutant. K2's side of every table is `../results/results.json`,
  unchanged.
- **Generated side.** Property test: 10,000 cases in the rule's scope, seed 20261111, collections up to 6 items, 30 s per
  rule; "shown false" is a failing case or a test that does not finish (K2 counted a hang the same way). Kani: the fixed
  ladder (accounts, transfers) = (2, 1), (2, 2), (4, 1), (2, 3), (6, 4), 30 s per harness, the first rung for every rule
  and then the others for the rules the first did not show false; "shown false" is a failed harness whose input fails when
  replayed on the compiled Rust, or a failed unwinding assertion (a loop that does not terminate within the bound).
- **Not frozen in the sense of PLAN rule 1.** The generator was written on 2026-11-11 by an agent that had read
  `../TRADES.md`, including which sizes K2's Kani arm missed; the ladder was chosen from that text and its first rung was
  added after seeing the unmutated code time out. So this is a regression against K2 on mutants the builder knew, not a
  blind result. The generators were not tuned on any mutant: the one change made to them (account numbers mostly existing
  positions) was made on the unmutated code, to find the deliberately false fixture rules the grid search finds.
- **What was run.** Two scratch copies of the crates and the generated harnesses (`w0` made at 03:50, `w1` at 04:21 local
  time), from the same `build/trees.json`. Between the two the generator changed only the wording of the rung labels.
  The digests of `w1` are in `results/frozen.w1.json`; those of `w0` were deleted with the scratch copy by mistake, so that
  the two copies held the same generated predicates is my account, not a recorded fact.
- **Run:** `python3 compare/e1/run.py`, then `python3 compare/e1/analyse.py`. Raw data `results/raw/`, per pair
  `results/pairs.json`, numbers `results/summary.json`, the tables below `results/tables.md`.

## In short

1. **Yes, on both sets.** Every (mutant, rule) pair that any K2 arm shows false is shown false by the generated set: 212 of
   212 on the tool set, 97 of 97 on the hand-written set. No test code was written for any rule.
   10 of the 212 tool-set pairs (8 under `cm-l34` and 2 under `cm-l14`, loops that never end) count as shown false only
   because the property test did not finish in 30 s or Kani failed an unwinding assertion; neither gives a concrete failing
   input (the property test names the input it was evaluating when the time ran out, which is not a demonstrated failure). K2
   counted them the same way. Counting only a concrete input that fails, the generated set shows 202 of 212.
2. **Generated property test = hand-written edge-weighted property test, pair for pair in total:** 212 of 212 (tool) and
   90 of 97 (hand-written; the 7 it misses are the magic-value mutants `d6` and `la6`, which K2's property tests missed too).
3. **Generated Kani ladder: 210 of 212 (tool) and 97 of 97 (hand-written); K2's Kani at its registered bounds had 209 and
   89.** The ladder finds all 8 hand-written pairs and 1 of the 3 tool pairs that K2's Kani missed for size, at the rung
   TRADES.md predicted: a fourth account for `cm-l23`, `lt2`, `r2`; a third transfer for `r5`; 6 accounts and 4 transfers for
   `r1`. It gives no answer for 2 tool pairs: `batch_then_total_overflow` under `cm-l22` (verified at the two smallest rungs,
   no answer in 30 s at the others) and `two_batches_conserve` under `cm-l34` (a loop that does not terminate: no answer at
   any rung). The generated property test finds both. (Retried alone with 120 s afterwards: the first is found at 4
   accounts and 1 transfer in 47 s, the second still gets no answer; see Limits.)
4. **Nothing new is caught through the 23 rules, and nothing is lost.** The generated set shows no pair false that no K2 arm
   did. The same 4 mutants are caught through none of the 23 rules: `cm-l36`, `cm-l39`, `lw3`, `r4`.
5. **With the two candidate rules of TRADES.md section 5 added as sentences, all four are shown false**, by the generated
   property test and by Kani at the first or second rung: `cm-l36`, `cm-l39` and `lw3` by candidate 1 (at the empty batch),
   `r4` by candidate 2. Mutants shown false through no rule: 0 of 97.
6. **Cost.** No lines per rule (K2: 9 to 27 lines of property and 10 to 23 of harness per rule). Once: 395 lines of typed
   piece readings, 594 of runner, 1,272 of generator and glue in Python (`evgen.py` 756, `evidence.py` 516). To run, per ledger mutant (median):
   16 s for the property tests of all 68 ledger readings, 126 s for the Kani ladder of 18 rules, 30 s to get and replay
   Kani's inputs. K2's hand-written arms: 2.3 s (edge property tests, 16 rules) and 233 s (Kani, one size per rule).
7. **One run was wrong and was caught by the replay.** The first run of `cm-l35` came after `cm-l34` (a loop that does not
   terminate) in the same scratch copy and used a stale Kani build: Kani reported a rule about `apply_batch` false although
   the mutant does not touch it. Its input did not fail when replayed on the compiled Rust ("NOT reproduced"), which is how
   it was noticed. Rerun alone it is as expected. The runner now stops anything left behind and touches the sources before
   each mutant; the analysis does not count a Kani failure that does not reproduce. Kept:
   `results/raw_first_pass_under_overload/cm-l35.stale-kani-build.json`.

## The tables

Generated from 97 of 97 mutant runs.

### Detection, mutant by mutant (through at least one of the 23 rules)

| Mutant set | Mutants | K2 a. rows | K2 b. plain | K2 b. edge | K2 c. Kani | K2 d. Lean (incl. confirmed) | GENERATED property test | GENERATED Kani ladder | GENERATED either | K2: no arm at all | GENERATED: neither | GENERATED: neither, with the two candidate rules added |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cargo-mutants, wallet | 13 | 13 | 11 | 13 | 13 | 13 | 13 | 13 | 13 | 0 | 0 | 0 |
| cargo-mutants, ledger | 39 | 37 | 34 | 37 | 37 | 36 | 37 | 37 | 37 | 2 | 2 | 0 |
| cargo-mutants, both | 52 | 50 | 45 | 50 | 50 | 49 | 50 | 50 | 50 | 2 | 2 | 0 |
| hand-written, wallet | 18 | 17 | 14 | 17 | 18 | 18 | 17 | 18 | 18 | 0 | 0 | 0 |
| hand-written, ledger (builder) | 22 | 19 | 18 | 20 | 21 | 21 | 20 | 21 | 21 | 1 | 1 | 0 |
| hand-written, ledger (reviewer) | 5 | 4 | 4 | 4 | 2 | 4 | 4 | 4 | 4 | 1 | 1 | 0 |
| hand-written, all | 45 | 40 | 36 | 41 | 41 | 43 | 41 | 43 | 43 | 2 | 2 | 0 |

### Detection by kind of rule: Tool set (cargo-mutants)

Unit: a (mutant, rule) pair in which some K2 arm shows the rule false of the mutant.

| Kind of rule | Pairs where some K2 arm shows the rule false | K2 b. edge (hand-written) | K2 c. Kani (hand-written) | GENERATED property test | GENERATED Kani ladder | GENERATED either | GENERATED shows false, no K2 arm did | Kani: not failed, and no answer at some rung |
|---|---|---|---|---|---|---|---|---|
| safety / never-changes | 91 | 91 | 88 | 91 | 89 | 91 | 0 | 90 |
| exact-result | 36 | 36 | 36 | 36 | 36 | 36 | 0 | 29 |
| rejection-and-unchanged | 53 | 53 | 53 | 53 | 53 | 53 | 0 | 0 |
| progress (1 rule) | 19 | 19 | 19 | 19 | 19 | 19 | 0 | 0 |
| bound (1 rule) | 13 | 13 | 13 | 13 | 13 | 13 | 0 | 0 |
| all 23 rules | 212 | 212 | 209 | 212 | 210 | 212 | 0 | 119 |

### Detection by kind of rule: Hand-written set

Unit: a (mutant, rule) pair in which some K2 arm shows the rule false of the mutant.

| Kind of rule | Pairs where some K2 arm shows the rule false | K2 b. edge (hand-written) | K2 c. Kani (hand-written) | GENERATED property test | GENERATED Kani ladder | GENERATED either | GENERATED shows false, no K2 arm did | Kani: not failed, and no answer at some rung |
|---|---|---|---|---|---|---|---|---|
| safety / never-changes | 41 | 36 | 34 | 36 | 41 | 41 | 0 | 95 |
| exact-result | 18 | 16 | 18 | 16 | 18 | 18 | 0 | 23 |
| rejection-and-unchanged | 30 | 30 | 30 | 30 | 30 | 30 | 0 | 0 |
| progress (1 rule) | 6 | 6 | 5 | 6 | 6 | 6 | 0 | 0 |
| bound (1 rule) | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 0 |
| all 23 rules | 97 | 90 | 89 | 90 | 97 | 97 | 0 | 118 |

### Pairs a hand-written property test or Kani harness of K2 found and the generated set did not

None.

### Pairs only K2's example rows or Lean arm found and the generated set did not

None.

### Pairs the generated set shows false and no K2 arm did

None.

### Property test against Kani ladder, within the generated set

| Set | Pairs shown false by either | by both | by the property test only | by Kani only | property test did not finish (counted as shown false) |
|---|---|---|---|---|---|
| tool | 212 | 210 | 2 | 0 | 12 |
| hand-written | 97 | 90 | 0 | 7 | 0 |

Rung of the ladder at which Kani first fails a pair: up to 2 accounts and up to 1 transfer: 190; up to 2 accounts: 57; no size bound: 43; up to 2 accounts and up to 3 transfers: 5; up to 4 accounts and up to 1 transfer: 4; up to 2 accounts and up to 2 transfers: 4; up to 4 accounts: 3; up to 6 accounts and up to 4 transfers: 1.

Generated input at which the property test first fails: median 6, largest 9637 (hand-r5, whole_conserves); 2 of 290 pairs after the 1,000th.

### The mutants no K2 arm caught, and the two candidate rules

| Mutant | Change | Shown false through one of the 23 rules by a generated harness | candidate 1: whole batch agrees with the batch applied transfer by transfer | candidate 2: batch agrees with its transfers applied one at a time |
|---|---|---|---|---|
| cm-l36 | src/lib.rs:77:9: replace Ledger::apply_all -> bool with false | no | FALSE: property test + Kani (up to 2 accounts and up to 1 transfer) at `{"the_batch": "[]", "the_ledger": "[]"}` | not shown false |
| cm-l39 | src/lib.rs:79:20: replace < with <= in Ledger::apply_all | no | FALSE: property test + Kani (up to 2 accounts and up to 1 transfer) at `{"the_batch": "[]", "the_ledger": "[]"}` | not shown false |
| hand-lw3 | every batch is rolled back and rejected (< became <=) | no | FALSE: property test + Kani (up to 2 accounts and up to 1 transfer) at `{"the_batch": "[]", "the_ledger": "[]"}` | not shown false |
| hand-r4 | REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied | no | not shown false | FALSE: property test + Kani (up to 2 accounts and up to 2 transfers) at `{"the_batch": "[1->0:0, 0->2:0]", "the_ledger": "[0, 0]"}` |

- candidate 1: whole batch agrees with the batch applied transfer by transfer: shown false of 24 of 66 ledger mutants (tool 18 of 39, hand-written 6 of 27).
- candidate 2: batch agrees with its transfers applied one at a time: shown false of 26 of 66 ledger mutants (tool 16 of 39, hand-written 10 of 27).

### The unmutated code

| Rule | Kind | Generated property test | Kani: verified with | Kani: no answer in 30 s with | Kani: failed | Solver seconds (answered rungs) |
|---|---|---|---|---|---|---|
| transfer_conserves | exact | pass (312 ms) | no size bound | - | - | 0.4 |
| withdraw_too_much | rejection | pass (103 ms) | no size bound | - | - | 0.1 |
| deposit_overflow | rejection | pass (215 ms) | no size bound | - | - | 0.1 |
| withdraw_covered | exact | pass (144 ms) | no size bound | - | - | 0.1 |
| deposit_with_room | exact | pass (86 ms) | no size bound | - | - | 0.1 |
| transfer_short | rejection | pass (142 ms) | no size bound | - | - | 0.1 |
| transfer_no_room | rejection | pass (812 ms) | no size bound | - | - | 0.1 |
| batch_conserves | safety | pass (204 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers | up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | 12.7 |
| batch_first_invalid | rejection | pass (263 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | - | 30.5 |
| batch_count_bounded | bound | pass (202 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | - | 18.3 |
| batch_stops_at_invalid | progress | pass (203 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | - | 33.7 |
| transfer_valid_moves | exact | pass (1543 ms) | up to 2 accounts | up to 4 accounts; up to 6 accounts | - | 3.3 |
| transfer_invalid_rejected | rejection | pass (147 ms) | up to 2 accounts; up to 4 accounts; up to 6 accounts | - | - | 5.1 |
| total_is_sum | exact | pass (1275 ms) | up to 2 accounts; up to 4 accounts; up to 6 accounts | - | - | 5.3 |
| total_overflow | rejection | pass (259 ms) | up to 2 accounts; up to 4 accounts; up to 6 accounts | - | - | 4.4 |
| balance_of_account | exact | pass (178 ms) | up to 2 accounts; up to 4 accounts; up to 6 accounts | - | - | 3.0 |
| balance_no_account | rejection | pass (245 ms) | up to 2 accounts; up to 4 accounts; up to 6 accounts | - | - | 2.2 |
| whole_conserves | safety | pass (204 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 2 accounts and up to 3 transfers | up to 4 accounts and up to 1 transfer; up to 6 accounts and up to 4 transfers | - | 42.0 |
| whole_first_invalid | rejection | pass (266 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | - | 29.5 |
| whole_rejected_unchanged | safety | pass (203 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | - | 29.7 |
| batch_then_total | safety | pass (2549 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers | up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | 15.8 |
| batch_then_total_overflow | safety | pass (558 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 2 accounts and up to 3 transfers | up to 4 accounts and up to 1 transfer; up to 6 accounts and up to 4 transfers | - | 37.5 |
| two_batches_conserve | safety | pass (316 ms) | up to 2 accounts and up to 1 transfer | up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers; up to 6 accounts and up to 4 transfers | - | 17.6 |
| k2_whole_agrees_with_batch | candidate | pass (213 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers | up to 6 accounts and up to 4 transfers | - | 38.9 |
| k2_batch_agrees_with_transfers | candidate | pass (219 ms) | up to 2 accounts and up to 1 transfer; up to 2 accounts and up to 2 transfers; up to 4 accounts and up to 1 transfer; up to 2 accounts and up to 3 transfers | up to 6 accounts and up to 4 transfers | - | 29.9 |

Baseline cost: {"property_build_secs": 5.93, "property_secs": 27.51, "bounded_secs": 134.2, "bounded_witness_secs": 0.0}

### Cost of the generated harnesses on the mutants (seconds, wall-clock)

| Crate (mutants) | What | Median per mutant | Largest | All mutants |
|---|---|---|---|---|
| wallet (31) | property tests, every reading of the crate | 7.8 | 9.9 | 239 |
| wallet (31) | Kani ladder, the K2 rules of the crate (and the 2 candidates) | 1.1 | 1.3 | 34 |
| wallet (31) | Kani: concrete input of each failing rule, and its replay | 0.8 | 2.4 | 33 |
| wallet (31) | whole run (build included) | 10.2 | 13.5 | 323 |
| ledger (66) | property tests, every reading of the crate | 16.3 | 730.5 | 2026 |
| ledger (66) | Kani ladder, the K2 rules of the crate (and the 2 candidates) | 125.5 | 269.4 | 7965 |
| ledger (66) | Kani: concrete input of each failing rule, and its replay | 29.9 | 195.6 | 3158 |
| ledger (66) | whole run (build included) | 181.8 | 961.1 | 13217 |

READING MISMATCH (generated predicate against the tree evaluator) in any mutant run: 0 readings in 0 runs.

Kani failures whose concrete input did not fail when replayed on the compiled Rust (not counted as shown false): 0.

Kani failures with no concrete input to replay (the failed check is an unwinding assertion: the loop does not terminate within the bound): 9 pairs, counted as shown false as K2 did.


## Reading the tables

- **Where the two generated harnesses differ.** On the tool set they find the same pairs except the 2 above. On the
  hand-written set Kani alone finds the 7 magic-value pairs (`d6`: 1, `la6`: 6): no sample draws 1,000,003, and Kani's
  integers are symbolic. That is K2's finding again, now without a hand-written harness.
- **How early.** Kani first fails 290 of its 307 pairs at the first rung of the ladder or with no size bound; 17 need a
  later rung (4 accounts: 7; 3 transfers: 5; 2 transfers: 4; 6 and 4: 1). The property test's first failing input is the
  6th generated in the median; 2 of 290 come after the 1,000th (`r5` at 9,637: 10,000 cases was just enough, as in K2).
- **What a rung without an answer costs.** In 237 pairs Kani shows nothing false and gives no answer at one rung at least
  (all of them rules with a total, or `transfer_valid_moves`). There the bounded result is "holds up to the rungs that
  answered", and the report says which. On the unmutated code every one of the 25 rules is verified at one rung at least;
  10 of the 18 ledger rules at every rung.
- **The candidate rules also catch much of what the 23 catch**: candidate 1 is false of 24 of the 66 ledger mutants and
  candidate 2 of 26. Candidate 1 is not false of `r4` and candidate 2 not of the three `apply_all` mutants, as TRADES.md
  argued. Candidate 2 is false of `cm-l34` whenever the call returns, without relying on non-termination, as predicted.
- **Property tests are slower than K2's by about ten times per rule** (0.09 to 2.5 s against 0.03 to 0.13 s). The causes are
  measured only as a whole: every case is also evaluated by the tree evaluator (JSON, dynamically typed) for the READING
  MISMATCH check; Givens other than "is exactly this value" are kept by rejection (2.4 million cases generated for 0.63
  million counted on the unmutated code); and all 83 readings run, not 23.

## The feed-back on a sample of mutants (`feedback.py`, the whole pipeline in a scratch copy)

The measurement above is on the compiled Rust only. For five mutants the whole pipeline was run, so that what the generated
harnesses find reaches the Lean side (`results/feedback/`; the logs beside the JSON files are cut to their head and tail):

| Mutant | Mode | What happened |
|---|---|---|
| `hand-d6` (control c36 of the mutation harness) | with Kani | K2: found by Kani only, the Lean arm's only signal a lost proof. Now: the generated Kani harness finds amount 1,000,003; it fails on the compiled Rust and on the model; `Spec.wallet.deposit_with_room` is REFUTED in the kernel, source "generated bounded check" |
| `hand-la6` | with Kani | the same on the ledger: 16 readings fed back from the bounded check; 7 readings REFUTED in the kernel (3 scenarios, among them `transfer_valid_moves`, and 4 rule statements), 6 more COUNTEREXAMPLE. (Run before two-When scenarios were given the fed-back row; the mutation harness's run of `la6` has them) |
| `cm-l22` | quick | `batch_then_total_overflow`, the three-account case K2's Lean grid missed: found by the generated property test, fails on the model, verdict COUNTEREXAMPLE with its source |
| `cm-l36` | quick | candidate 1 goes from PROVED-FOR-ALL to COUNTEREXAMPLE (the grid finds the empty batch too; no kernel refutation: the script cannot unfold a reference that is another operation) |
| `hand-r4` | quick | candidate 2 goes from TESTED-ONLY to COUNTEREXAMPLE |
| `cm-l34` | quick | NOTHING: the pipeline stops at step 5 (the search on the model overflows the stack on the non-terminating loop), before the generated harnesses run. On the compiled Rust alone (the table above) they do show 8 rules false of it |

No MODEL MISMATCH in any of these runs: every input that failed on the compiled Rust and could be evaluated on the model
failed there too. Inputs that could not be evaluated: account numbers above 4294967295 from Kani (the model leaves the
width of `usize` open and has no literal for them); 3 of 54 inputs under `la6`.

## Limits

- Two toy crates; fixtures for building the infrastructure. Nothing here says how generic generators fare on real code.
- The mutants were known to the builder (see the top). The reviewer's five and the tool's 52 were not written by the
  builder, but the ladder was chosen knowing which sizes they need.
- The machine was shared: load 7 to 27 during the measured run. Eight runs made while a third job pushed the load above 50
  were repeated (`results/raw_first_pass_under_overload/`); none changed in what it detects. Timings are not clean timings.
- Kani's "no answer" depends on the 30 s allowed and on the load. The two tool pairs it gave no answer for were put to it
  again after the run, alone, with 120 s per harness (exploratory; `results/kani_retry_120s.json`):
  `batch_then_total_overflow` under `cm-l22` FAILS at 4 accounts and 1 transfer in 47 s (the call panics; the input fails
  on the compiled Rust), so with that time the ladder has 211 of 212; `two_batches_conserve` under `cm-l34` gives no
  answer at any rung in 120 s either.
- **A false rule can pass every layer.** A reviewer's probe, "For a batch, the number of transfers applied is at most 4",
  is false at ledger `[0, 0]` with five 0-amount transfers, and the compiled Rust fails there (replayed by the reviewer).
  The grid search (at most 4 transfers per batch) and the generated property test (10,000 cases, collections up to 6) did
  not find it. The Kani ladder cannot, because no rung has more than 4 transfers (the reviewer's probe run was `--quick`,
  so Kani was not put to it). Its verdict is TESTED-ONLY with STRONGEST HELD "PROPERTY TEST only ... NOT PROVED". The
  wording is right, but the rule is not flagged. The probe is in `../../review/step3/`; it is not in `features/`.
- The two candidate rules compare one operation of the code with another (`apply_all` against `apply_batch`;
  `apply_batch` against `apply`, once per transfer). They catch disagreement between the operations, not a mistake the
  operations share.
- The 23 rules are scenario-level readings. The 45 Rule lines have generated harnesses too and were run on every mutant
  (property tests only); they are in `results/raw/` and are not analysed here.
