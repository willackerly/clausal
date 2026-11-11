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

