# Mutation run

Generated 2026-11-10T06:10:30+00:00 by `python3 mutation/run_mutants.py`. Logs: `mutation/logs/`.

Columns. *Examples rows on Rust*: an Examples row or a literal scenario gives a different result on the compiled Rust. *Proofs lost*: scenarios that were PROVED and no longer are, because their proof or a lemma module it depends on no longer compiles; this does not by itself mean their statement is false of the mutant. *New counterexamples*: scenarios for which the grid search on the Lean model now finds a failing input, so their statement is false of the mutant.

## `wallet/src/lib.rs`: 18 mutants

- noticed by the scenarios (pipeline run without the crate's unit tests, exit status non-zero): **18 of 18**
- noticed by an example row on the compiled Rust: 17
- at least one proof lost: 18
- a new counterexample found by the search on the Lean model: 17
- a proof lost but NO example row differs: 1 (d6)
- an example row differs but NO proof is lost: 0 (-)
- neither a row nor the search shows a failing input (only a lost proof says something is wrong): 1 (d6)
- missed by the crate's own unit tests: 3 (d4, d6, w5)

| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | Noticed by the scenarios |
|---|---|---|---|---|---|---|---|---|
| d1 | `wallet::{wallet::Wallet}::deposit` | no overflow check: the balance wraps around | caught | caught (2 rows) | 2 | 1 | deposit_overflow: REFUTED; deposit_with_room: TESTED-ONLY | yes |
| d2 | `wallet::{wallet::Wallet}::deposit` | a successful deposit sets the balance to the amount instead of adding it | caught | caught (2 rows) | 1 | 1 | deposit_with_room: REFUTED | yes |
| d3 | `wallet::{wallet::Wallet}::deposit` | overflow is reported as insufficient funds | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes |
| d4 | `wallet::{wallet::Wallet}::deposit` | a deposit that reaches exactly the maximum is rejected | MISSED | caught (2 rows) | 2 | 2 | deposit_with_room: REFUTED; bystander_unchanged: REFUTED | yes |
| d5 | `wallet::{wallet::Wallet}::deposit` | a rejected deposit empties the wallet | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes |
| d6 | `wallet::{wallet::Wallet}::deposit` | a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 1 | none | deposit_with_room: TESTED-ONLY | yes |
| w1 | `wallet::{wallet::Wallet}::withdraw` | withdrawing the whole balance is rejected (> became >=) | caught | caught (2 rows) | 1 | 1 | withdraw_covered: REFUTED | yes |
| w2 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal does not take the money | caught | caught (2 rows) | 1 | 1 | withdraw_covered: REFUTED | yes |
| w3 | `wallet::{wallet::Wallet}::withdraw` | insufficient funds is reported as overflow | caught | caught (2 rows) | 1 | 1 | withdraw_too_much: REFUTED | yes |
| w4 | `wallet::{wallet::Wallet}::withdraw` | a rejected withdrawal empties the wallet | caught | caught (1 rows) | 1 | 1 | withdraw_too_much: REFUTED | yes |
| w5 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal takes one unit too many when it can | MISSED | caught (1 rows) | 1 | 1 | withdraw_covered: REFUTED | yes |
| t1 | `wallet::transfer` | transferring the whole balance is rejected (< became <=) | caught | caught (3 rows) | 2 | 2 | transfer_conserves: REFUTED; transfer_no_room: REFUTED | yes |
| t2 | `wallet::transfer` | the sender is debited before the receiver's overflow check, so a rejected transfer loses money | caught | caught (2 rows) | 1 | 1 | transfer_no_room: REFUTED | yes |
| t3 | `wallet::transfer` | the receiver is never credited (money vanishes) | caught | caught (4 rows) | 1 | 1 | transfer_conserves: REFUTED | yes |
| t4 | `wallet::transfer` | the sender is never debited (money is created) | caught | caught (4 rows) | 1 | 1 | transfer_conserves: REFUTED | yes |
| t5 | `wallet::transfer` | receiver overflow is reported as insufficient funds | caught | caught (2 rows) | 1 | 1 | transfer_no_room: REFUTED | yes |
| t6 | `wallet::transfer` | insufficient funds is reported as overflow | caught | caught (3 rows) | 2 | 2 | transfer_short: REFUTED; transfer_short_example: REFUTED | yes |
| t7 | `wallet::transfer` | no funds check at all (the subtraction panics instead) | caught | caught (3 rows) | 2 | 2 | transfer_short: COUNTEREXAMPLE; transfer_short_example: COUNTEREXAMPLE | yes |

## `ledger/src/lib.rs`: 27 mutants

- noticed by the scenarios (pipeline run without the crate's unit tests, exit status non-zero): **27 of 27**
- noticed by an example row on the compiled Rust: 22
- at least one proof lost: 27
- a new counterexample found by the search on the Lean model: 22
- a proof lost but NO example row differs: 5 (la6, r1, r2, r3, r5)
- an example row differs but NO proof is lost: 0 (-)
- neither a row nor the search shows a failing input (only a lost proof says something is wrong): 5 (la6, r1, r2, r3, r5)
- missed by the crate's own unit tests: 4 (la6, r1, r2, r3)

| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | Noticed by the scenarios |
|---|---|---|---|---|---|---|---|---|
| lt1 | `ledger::{ledger::Ledger}::total` | LOOP off-by-one bound: the last balance is not added | caught | caught (4 rows) | 3 | 3 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE | yes |
| lt2 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: the sum is overwritten by each balance instead of accumulated | caught | caught (5 rows) | 3 | 2 | total_is_sum: COUNTEREXAMPLE; total_overflow: TESTED-ONLY; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE | yes |
| lt3 | `ledger::{ledger::Ledger}::total` | LOOP skipped element: summing starts at account 1 | caught | caught (6 rows) | 3 | 3 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE | yes |
| lt4 | `ledger::{ledger::Ledger}::total` | an overflowing total is reported as u64::MAX instead of absent | caught | caught (2 rows) | 3 | 1 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY | yes |
| lt5 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: wrapping addition, so an overflowing total wraps around | caught | caught (2 rows) | 3 | 1 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY | yes |
| la1 | `ledger::{ledger::Ledger}::apply` | no check that sender and receiver differ: a self-transfer creates money | caught | caught (2 rows) | 13 | 7 | batch_conserves: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: REFUTED; whole_conserves: COUNTEREXAMPLE; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE | yes |
| la2 | `ledger::{ledger::Ledger}::apply` | transferring the sender's whole balance is rejected (< became <=) | caught | caught (5 rows) | 13 | 3 | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: COUNTEREXAMPLE; transfer_invalid_rejected: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| la3 | `ledger::{ledger::Ledger}::apply` | the receiver is never credited (money vanishes) | caught | caught (9 rows) | 13 | 8 | batch_conserves: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE | yes |
| la4 | `ledger::{ledger::Ledger}::apply` | the sender is never debited (money is created) | caught | caught (10 rows) | 13 | 8 | batch_conserves: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE | yes |
| la5 | `ledger::{ledger::Ledger}::apply` | receiver bounds check off by one (>= became >): indexing one past the end panics | caught | caught (2 rows) | 13 | 8 | batch_conserves: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: COUNTEREXAMPLE; whole_conserves: COUNTEREXAMPLE; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE | yes |
| la6 | `ledger::{ledger::Ledger}::apply` | a transfer of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 13 | none | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lb1 | `ledger::{ledger::Ledger}::apply_batch` | LOOP missing early exit: the batch carries on after a rejected transfer and counts it | caught | caught (6 rows) | 11 | 4 | batch_conserves: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lb2 | `ledger::{ledger::Ledger}::apply_batch` | LOOP off-by-one bound: the last transfer of the batch is never applied | caught | caught (4 rows) | 11 | 2 | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lb3 | `ledger::{ledger::Ledger}::apply_batch` | LOOP skipped element: every second transfer is skipped (i += 2) | caught | caught (5 rows) | 11 | 6 | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE | yes |
| lb4 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong result: the batch length is returned instead of the number applied | caught | caught (6 rows) | 11 | 4 | batch_conserves: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lb5 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong counter: a rejected transfer is counted as applied | caught | caught (5 rows) | 11 | 4 | batch_conserves: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lb6 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong early exit: the batch stops after the first APPLIED transfer | caught | caught (3 rows) | 11 | 2 | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: REFUTED; batch_example_stop: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| lw1 | `ledger::{ledger::Ledger}::apply_all` | no rollback: a rejected batch keeps the transfers applied before the failure | caught | caught (1 rows) | 4 | 1 | whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE | yes |
| lw2 | `ledger::{ledger::Ledger}::apply_all` | a rolled-back batch is reported as applied | caught | caught (2 rows) | 4 | 2 | whole_conserves: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE | yes |
| lw3 | `ledger::{ledger::Ledger}::apply_all` | every batch is rolled back and rejected (< became <=) | caught | caught (1 rows) | 4 | 1 | whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY | yes |
| lg1 | `ledger::{ledger::Ledger}::balance` | lookup bounds check off by one (< became <=): looking up account `len` panics | caught | caught (2 rows) | 2 | 1 | balance_of_account: TESTED-ONLY; balance_no_account: COUNTEREXAMPLE | yes |
| lg2 | `ledger::{ledger::Ledger}::balance` | lookup returns the balance of account 0 whatever the account | caught | caught (1 rows) | 2 | 1 | balance_of_account: REFUTED; balance_no_account: TESTED-ONLY | yes |
| r1 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP cap: the batch silently stops after three transfers | MISSED | MISSED | 11 | none | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| r2 | `ledger::{ledger::Ledger}::total` | REVIEW LOOP cap: only the first three accounts are summed | MISSED | MISSED | 3 | none | total_is_sum: TESTED-ONLY; total_overflow: TESTED-ONLY; total_always_available: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY | yes |
| r3 | `ledger::{ledger::Ledger}::apply_all` | REVIEW atomicity: no rollback once two or more transfers have been applied | MISSED | MISSED | 4 | none | whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY | yes |
| r4 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied | caught | caught (1 rows) | 11 | 1 | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |
| r5 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP state corruption on the third iteration: one unit is minted to account 0 (conservation is false, but only for batches whose first two transfers apply and that have a third) | caught | MISSED | 11 | none | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; two_batches_conserve: TESTED-ONLY | yes |


## Negative controls (checks of the checks)

| Control | What is wrong | Expected exit | Got | As expected |
|---|---|---|---|---|
| c1 | a 'proof' whose type is True instead of the scenario's statement | 1 | 1 | yes |
| c2 | a proof replaced by sorry | 1 | 1 | yes |
| c3 | one proof that does not compile: only its own scenario should lose its proof | 1 | 1 | yes |
| c4 | glossary: 'decreased by <amount>' weakened so it no longer mentions the amount (proofs still compile) | 1 | 1 | yes |
| c5 | glossary: 'does not exceed the maximum' silently narrowed to amounts up to a million (proofs still compile) | 1 | 1 | yes |
| c6 | glossary: 'is not more than' reversed in the Lean definition | 1 | 1 | yes |
| c7 | the Rust reading of 'is not more than' made strict (the Lean definition is untouched) | 1 | 1 | yes |
| c8 | the four scenarios added after the review are removed: inputs are no longer covered, and the run says so | 0 | 0 | yes |
| c9 | --strict on the unchanged tree: proved scenarios rest on a glossary nobody has signed off | 1 | 1 | yes |
| c10 | not a fault: every glossary entry signed off by a test reviewer, then --strict; the run should pass | 0 | 0 | yes |
| c11 | signed off, then the text of one definition is edited (same meaning): that sign-off is void | 1 | 1 | yes |
| c12 | the shared hand-written lemma module does not compile: every ledger proof that depends on it is lost; the wallet's proofs and the lookup proofs are not | 1 | 1 | yes |
| c13 | ledger glossary: `valid` in Lean no longer requires sender and receiver to differ (the Rust reading still does) | 1 | 1 | yes |
| c14 | multi-step scenario whose Then is about the wrong When's kind of result: rejected, not mis-translated | 1 | 1 | yes |
| c15 | the batch loop's invariant weakened in its lemma module: the lemma no longer proves, the batch scenarios lose their proofs, the total's do not | 1 | 1 | yes |
