# Slice: scenario report (wallet and ledger)

Generated 2026-11-10T05:37:45+00:00 by `slice/run.sh`. Lean `leanprover/lean4:v4.35.0`, Aeneas `nightly-2026.11.09-5a392f4`, Charon `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, slicegen e66d2bb71733 (slicegen-rule/2).

Each scenario below is an English claim about one of the Rust crates `slice/wallet` (three straight-line functions) and `slice/ledger` (loops over a `Vec` and a slice). The claim is turned into a Lean statement about the Aeneas-generated Lean model of that crate, and the statement is then proved, refuted or left open. Every link in that chain is labelled with the kind of evidence behind it:

| Evidence kind | Meaning here |
|---|---|
| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |
| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, and the two readings of each phrase compared on a grid. |
| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, slicegen (scenario to statement), and the audit that reads facts out of the Lean environment. |
| human-asserted | A person's say-so: that each glossary phrase means its Lean definition. Nothing checks this. It exists only where someone has signed off. |

## Summary

| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |
|---|---|---|---|---|
| A covered transfer moves the money and conserves the total (`features/wallet.feature:7`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (8 of 8) |
| Withdrawing more than the balance is rejected and changes nothing (`features/wallet.feature:24`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A deposit that would overflow is rejected and changes nothing (`features/wallet.feature:37`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A covered withdrawal succeeds and takes exactly the amount (`features/wallet.feature:50`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| A deposit with room succeeds and adds exactly the amount (`features/wallet.feature:64`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| Transferring more than the sender has is rejected and changes nothing (`features/wallet.feature:78`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A transfer the receiver has no room for is rejected and changes nothing (`features/wallet.feature:93`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6) |
| Transferring more than you have is rejected and changes nothing (`features/wallet.feature:109`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A transfer the sender can afford always succeeds (`features/wallet.feature:120`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6) |
| A deposit earns interest (`features/wallet.feature:136`) | **UNBOUND** | UNBOUND | - | - |
| Applying any batch of transfers conserves the total of all balances (`features/ledger.feature:9`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 4 / 4 of 4 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch whose first transfer is invalid changes nothing (`features/ledger.feature:22`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| The number of transfers applied is at most the length of the batch (`features/ledger.feature:36`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch of two valid transfers is applied in full (`features/ledger.feature:49`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch stops at its first invalid transfer and keeps what it has applied (`features/ledger.feature:57`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:67`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| A valid transfer is accepted and moves exactly its amount (`features/ledger.feature:79`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (6 of 6) |
| An invalid transfer is rejected and changes nothing (`features/ledger.feature:94`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (5 of 5) |
| The total is the sum of the balances when that fits (`features/ledger.feature:110`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of balances that do not fit is reported as absent (`features/ledger.feature:123`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of a ledger can always be computed (`features/ledger.feature:136`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| Looking up an existing account gives its balance (`features/ledger.feature:147`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| Looking up an account that does not exist gives nothing (`features/ledger.feature:159`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| Applying a batch as a whole conserves the total of all balances (`features/ledger.feature:171`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch applied as a whole whose first transfer is invalid is rejected and changes nothing (`features/ledger.feature:182`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5) |
| A batch of valid transfers applied as a whole is accepted and applied (`features/ledger.feature:195`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole is rolled back when a later transfer is invalid (`features/ledger.feature:203`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| The total computed after any batch is the total before it (`features/ledger.feature:212`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| Two batches applied one after the other conserve the total (`features/ledger.feature:226`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A withdrawal that is both covered and not covered (`features/negative.feature:8`) | **VACUOUS** | VACUOUS | 0 / 0 of 1 | ROW OUTSIDE GIVENS; UNREVIEWED GLOSSARY (5 of 5) |
| A deposit does not touch a bystander (`features/negative.feature:22`) | **PROVED-FOR-ALL (1 of 2 Thens substantive)** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); TRIVIAL-THEN; FRAME-TRIVIAL |

Every scenario got the verdict it was expected to get.
A scenario tagged `@expect-refuted`, `@expect-unbound` or `@expect-vacuous` is a deliberate negative control.

**26 proved scenarios rest on glossary entries with no valid sign-off.** A proof shows the Lean statement holds; that the statement says what the English says is exactly what the sign-off is for. `./run.sh --strict` makes this a failure.

## How much of each operation the scenarios pin down

A green scenario says nothing about inputs outside its Givens. Two measurements of what is left unsaid:

1. **Inputs.** For each operation, a generated theorem states that the Givens of its proved universal scenarios, taken together, hold of every input. If the kernel accepts it, no input falls outside every scenario.
2. **Outputs.** A mutation run (`python3 mutation/run_mutants.py`, not part of `run.sh`) changes the Rust in small wrong ways and reports which changes no scenario notices.

| Operation (Lean model) | Every input covered by a proved scenario? | Scenarios |
|---|---|---|
| `wallet.Wallet.deposit` | **yes**: kernel-checked `Coverage.g2` over 2 proved scenarios | deposit_overflow: PROVED-FOR-ALL; deposit_with_room: PROVED-FOR-ALL; bystander_unchanged: PROVED-FOR-ALL (1 of 2 Thens substantive) |
| `wallet.Wallet.withdraw` | **yes**: kernel-checked `Coverage.g1` over 2 proved scenarios | withdraw_too_much: PROVED-FOR-ALL; withdraw_covered: PROVED-FOR-ALL; contradictory_givens: VACUOUS |
| `wallet.transfer` | **yes**: kernel-checked `Coverage.g0` over 3 proved scenarios | transfer_conserves: PROVED-FOR-ALL; transfer_short: PROVED-FOR-ALL; transfer_no_room: PROVED-FOR-ALL; transfer_short_example: PROVED-INSTANCE; transfer_always_succeeds: REFUTED |
| `ledger.Ledger.balance` | **yes**: kernel-checked `Coverage.g7` over 2 proved scenarios | balance_of_account: PROVED-FOR-ALL; balance_no_account: PROVED-FOR-ALL |
| `ledger.Ledger.total_loop.body` | **NOT SHOWN**: no universal scenario exercises it |  |
| `ledger.Ledger.total_loop` | **NOT SHOWN**: no universal scenario exercises it |  |
| `ledger.Ledger.total` | **NOT SHOWN**: `Coverage.g5` (1 scenarios): their Givens do not cover every input; `Coverage.g6` (1 scenarios): their Givens do not cover every input | total_is_sum: PROVED-FOR-ALL; total_overflow: PROVED-FOR-ALL; total_always_available: REFUTED; batch_then_total: PROVED-FOR-ALL |
| `ledger.Ledger.apply` | **yes**: kernel-checked `Coverage.g4` over 2 proved scenarios | transfer_valid_moves: PROVED-FOR-ALL; transfer_invalid_rejected: PROVED-FOR-ALL |
| `ledger.Ledger.apply_batch_loop.body` | **NOT SHOWN**: no universal scenario exercises it |  |
| `ledger.Ledger.apply_batch_loop` | **NOT SHOWN**: no universal scenario exercises it |  |
| `ledger.Ledger.apply_batch` | **yes**: kernel-checked `Coverage.g3` over 3 proved scenarios | batch_conserves: PROVED-FOR-ALL; batch_first_invalid: PROVED-FOR-ALL; batch_count_bounded: PROVED-FOR-ALL; batch_example_all: PROVED-INSTANCE; batch_example_stop: PROVED-INSTANCE; batch_all_valid_all_applied: REFUTED; batch_then_total: PROVED-FOR-ALL; two_batches_conserve: PROVED-FOR-ALL |
| `ledger.Ledger.apply_all` | **yes**: kernel-checked `Coverage.g8` over 2 proved scenarios | whole_conserves: PROVED-FOR-ALL; whole_first_invalid: PROVED-FOR-ALL; whole_example_accept: PROVED-INSTANCE; whole_example_rollback: PROVED-INSTANCE |

Mutation run of 2026-11-10T05:34:44+00:00: 40 mutants of `wallet/src/lib.rs` and `ledger/src/lib.rs`; **40 noticed by the scenarios, 0 not**. These results are for the current Rust, features, glossary and proofs.

A lost proof means the proof (or a lemma it depends on) no longer compiles; it does not by itself mean the scenario's statement is false of the mutant. A new counterexample does.

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

## Scenarios

### PROVED-FOR-ALL: A covered transfer moves the money and conserves the total

`features/wallet.feature:7`  id `Spec.wallet.transfer_conserves`  tags `@id:transfer_conserves`

```gherkin
Scenario Outline: A covered transfer moves the money and conserves the total
  Given Alice has a balance of <a>
  And Bob has a balance of <b>
  And <amount> is not more than Alice's balance
  And Bob's balance plus <amount> does not exceed the maximum
  When Alice transfers <amount> to Bob
  Then the operation succeeds
  And Alice's balance is decreased by <amount>
  And Bob's balance is increased by <amount>
  And the total of all balances is unchanged

  Examples:
    | a   | b  | amount |
    | 100 | 20 | 30     |
    | 5   | 0  | 5      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.transfer_conserves.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.covers alice amount →
    Vocab.roomFor bob amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.succeeds outcome ∧
      Vocab.decreasedBy alice alice' amount ∧
      Vocab.increasedBy bob bob' amount ∧
      Vocab.totalUnchanged [alice, bob] [alice', bob']
```

```text
PROVED-FOR-ALL  A covered transfer moves the money and conserves the total
  kernel-checked   theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/wallet/transfer_conserves.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 8 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-room, W-transfer, T-ok, T-dec, T-inc, T-total
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1839 of 1839 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/transfer_conserves.lean`):

```lean
theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt := by
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
  simp [Vocab.hasBalance, Vocab.decreasedBy, Vocab.increasedBy, Vocab.totalUnchanged] at *
  scalar_tac
```

### PROVED-FOR-ALL: Withdrawing more than the balance is rejected and changes nothing

`features/wallet.feature:24`  id `Spec.wallet.withdraw_too_much`  tags `@id:withdraw_too_much`

```gherkin
Scenario Outline: Withdrawing more than the balance is rejected and changes nothing
  Given Alice has a balance of <a>
  And <amount> is more than Alice's balance
  When Alice withdraws <amount>
  Then the operation is rejected with insufficient funds
  And Alice's balance is unchanged

  Examples:
    | a  | amount |
    | 10 | 11     |
    | 0  | 1      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.withdraw_too_much.stmt : Prop :=
  ∀ (a amount : U64) (alice : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.exceeds amount alice →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.withdraw alice amount = ok (outcome, alice') ∧
      Vocab.rejectedWith outcome wallet.WalletError.InsufficientFunds ∧
      Vocab.unchanged alice alice'
```

```text
PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_too_much.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_too_much.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-withdraw, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/withdraw_too_much.lean`):

```lean
theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.withdraw
  step*
```

### PROVED-FOR-ALL: A deposit that would overflow is rejected and changes nothing

`features/wallet.feature:37`  id `Spec.wallet.deposit_overflow`  tags `@id:deposit_overflow`

```gherkin
Scenario Outline: A deposit that would overflow is rejected and changes nothing
  Given Alice has a balance of <a>
  And Alice's balance plus <amount> exceeds the maximum
  When Alice deposits <amount>
  Then the operation is rejected with overflow
  And Alice's balance is unchanged

  Examples:
    | a                    | amount |
    | 18446744073709551615 | 1      |
    | 18446744073709551000 | 616    |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.deposit_overflow.stmt : Prop :=
  ∀ (a amount : U64) (alice : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.noRoomFor alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.deposit alice amount = ok (outcome, alice') ∧
      Vocab.rejectedWith outcome wallet.WalletError.Overflow ∧
      Vocab.unchanged alice alice'
```

```text
PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.deposit_overflow : Spec.wallet.deposit_overflow.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_overflow.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-noroom, W-deposit, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/deposit_overflow.lean`):

```lean
theorem Spec.wallet.deposit_overflow : Spec.wallet.deposit_overflow.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

### PROVED-FOR-ALL: A covered withdrawal succeeds and takes exactly the amount

`features/wallet.feature:50`  id `Spec.wallet.withdraw_covered`  tags `@id:withdraw_covered`

```gherkin
Scenario Outline: A covered withdrawal succeeds and takes exactly the amount
  Given Alice has a balance of <a>
  And <amount> is not more than Alice's balance
  When Alice withdraws <amount>
  Then the operation succeeds
  And Alice's balance is decreased by <amount>

  Examples:
    | a  | amount |
    | 10 | 4      |
    | 7  | 7      |
    | 0  | 0      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.withdraw_covered.stmt : Prop :=
  ∀ (a amount : U64) (alice : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.covers alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.withdraw alice amount = ok (outcome, alice') ∧
      Vocab.succeeds outcome ∧
      Vocab.decreasedBy alice alice' amount
```

```text
PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount
  kernel-checked   theorem Spec.wallet.withdraw_covered : Spec.wallet.withdraw_covered.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_covered.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_covered.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-withdraw, T-ok, T-dec
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 291 of 291 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/withdraw_covered.lean`):

```lean
theorem Spec.wallet.withdraw_covered : Spec.wallet.withdraw_covered.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.withdraw
  step*
```

### PROVED-FOR-ALL: A deposit with room succeeds and adds exactly the amount

`features/wallet.feature:64`  id `Spec.wallet.deposit_with_room`  tags `@id:deposit_with_room`

```gherkin
Scenario Outline: A deposit with room succeeds and adds exactly the amount
  Given Alice has a balance of <a>
  And Alice's balance plus <amount> does not exceed the maximum
  When Alice deposits <amount>
  Then the operation succeeds
  And Alice's balance is increased by <amount>

  Examples:
    | a                    | amount               |
    | 1                    | 2                    |
    | 18446744073709551615 | 0                    |
    | 0                    | 18446744073709551615 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.deposit_with_room.stmt : Prop :=
  ∀ (a amount : U64) (alice : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.roomFor alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.deposit alice amount = ok (outcome, alice') ∧
      Vocab.succeeds outcome ∧
      Vocab.increasedBy alice alice' amount
```

```text
PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount
  kernel-checked   theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_with_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_with_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-inc
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 291 of 291 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/deposit_with_room.lean`):

```lean
theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

### PROVED-FOR-ALL: Transferring more than the sender has is rejected and changes nothing

`features/wallet.feature:78`  id `Spec.wallet.transfer_short`  tags `@id:transfer_short`

```gherkin
Scenario Outline: Transferring more than the sender has is rejected and changes nothing
  Given Alice has a balance of <a>
  And Bob has a balance of <b>
  And <amount> is more than Alice's balance
  When Alice transfers <amount> to Bob
  Then the operation is rejected with insufficient funds
  And Alice's balance is unchanged
  And Bob's balance is unchanged

  Examples:
    | a  | b | amount |
    | 10 | 7 | 11     |
    | 0  | 0 | 1      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.transfer_short.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.exceeds amount alice →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.rejectedWith outcome wallet.WalletError.InsufficientFunds ∧
      Vocab.unchanged alice alice' ∧
      Vocab.unchanged bob bob'
```

```text
PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short : Spec.wallet.transfer_short.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/transfer_short.lean`):

```lean
theorem Spec.wallet.transfer_short : Spec.wallet.transfer_short.stmt := by
  intro a b amount alice bob h1 h2 h3
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

### PROVED-FOR-ALL: A transfer the receiver has no room for is rejected and changes nothing

`features/wallet.feature:93`  id `Spec.wallet.transfer_no_room`  tags `@id:transfer_no_room`

```gherkin
Scenario Outline: A transfer the receiver has no room for is rejected and changes nothing
  Given Alice has a balance of <a>
  And Bob has a balance of <b>
  And <amount> is not more than Alice's balance
  And Bob's balance plus <amount> exceeds the maximum
  When Alice transfers <amount> to Bob
  Then the operation is rejected with overflow
  And Alice's balance is unchanged
  And Bob's balance is unchanged

  Examples:
    | a | b                    | amount |
    | 1 | 18446744073709551615 | 1      |
    | 9 | 18446744073709551610 | 6      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.transfer_no_room.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.covers alice amount →
    Vocab.noRoomFor bob amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.rejectedWith outcome wallet.WalletError.Overflow ∧
      Vocab.unchanged alice alice' ∧
      Vocab.unchanged bob bob'
```

```text
PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_no_room : Spec.wallet.transfer_no_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_no_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_no_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-noroom, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 150 of 150 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/transfer_no_room.lean`):

```lean
theorem Spec.wallet.transfer_no_room : Spec.wallet.transfer_no_room.stmt := by
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

### PROVED-INSTANCE: Transferring more than you have is rejected and changes nothing

`features/wallet.feature:109`  id `Spec.wallet.transfer_short_example`  tags `@id:transfer_short_example`

```gherkin
Scenario: Transferring more than you have is rejected and changes nothing
  Given Alice has a balance of 10
  And Bob has a balance of 7
  When Alice transfers 11 to Bob
  Then the operation is rejected with insufficient funds
  And Alice's balance is unchanged
  And Bob's balance is unchanged
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.transfer_short_example.stmt : Prop :=
  ∀ (alice bob : wallet.Wallet),
    Vocab.hasBalance alice (10#u64) →
    Vocab.hasBalance bob (7#u64) →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob (11#u64) = ok (outcome, alice', bob') ∧
      Vocab.rejectedWith outcome wallet.WalletError.InsufficientFunds ∧
      Vocab.unchanged alice alice' ∧
      Vocab.unchanged bob bob'
```

```text
PROVED-INSTANCE  Transferring more than you have is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short_example.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short_example.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: G-balance, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 78 of 78 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/wallet/transfer_short_example.lean`):

```lean
theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt := by
  intro alice bob h1 h2
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

### REFUTED: A transfer the sender can afford always succeeds

`features/wallet.feature:120`  id `Spec.wallet.transfer_always_succeeds`  tags `@id:transfer_always_succeeds @expect-refuted`

```gherkin
Scenario Outline: A transfer the sender can afford always succeeds
  Given Alice has a balance of <a>
  And Bob has a balance of <b>
  And <amount> is not more than Alice's balance
  When Alice transfers <amount> to Bob
  Then the operation succeeds
  And Alice's balance is decreased by <amount>
  And the total of all balances is unchanged

  Examples:
    | a   | b  | amount |
    | 100 | 20 | 30     |
    | 5   | 0  | 5      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.wallet.transfer_always_succeeds.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.covers alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' bob' : wallet.Wallet),
      wallet.transfer alice bob amount = ok (outcome, alice', bob') ∧
      Vocab.succeeds outcome ∧
      Vocab.decreasedBy alice alice' amount ∧
      Vocab.totalUnchanged [alice, bob] [alice', bob']
```

```text
REFUTED  A transfer the sender can afford always succeeds
  kernel-checked   theorem Spec.wallet.transfer_always_succeeds.refuted : ¬ Spec.wallet.transfer_always_succeeds.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | a | b                    | amount |
                   | 1 | 18446744073709551615 | 1      |
                   When Alice transfers 1 to Bob  =>  returned Err(Overflow); Alice: balance 1; Bob: balance 18446744073709551615
                   failed Then: "the operation succeeds"; "Alice's balance is decreased by 1"
                   held   Then: "the total of all balances is unchanged"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-transfer, T-ok, T-dec, T-total
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1587 of 1587 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 216 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### UNBOUND: A deposit earns interest

`features/wallet.feature:136`  id `Spec.wallet.deposit_earns_interest`  tags `@id:deposit_earns_interest @expect-unbound`

```gherkin
Scenario: A deposit earns interest
  Given Alice has a balance of 100
  When Alice deposits 5
  Then Alice earns interest on her balance
```

```text
UNBOUND  A deposit earns interest
  features/wallet.feature:139: no glossary `then` phrase matches: "Alice earns interest on her balance"
    nearest glossary phrases:
      - the result is the balance of account {index:i} of ledger {ledger:l}
      - the operation succeeds
      - no transfer is applied
    paste-ready glossary stub (then define the Lean definition in the Vocab file of that crate):
      - id: T-TODO
        kind: then
        phrase: "Alice earns interest on her balance"
        lean: Vocab.TODO
        args: []
  no Lean statement was generated, so nothing was proved or refuted
  tested           cucumber-rs on compiled Rust: skipped (the undefined step and everything after it are skipped)
```

### PROVED-FOR-ALL: Applying any batch of transfers conserves the total of all balances

`features/ledger.feature:9`  id `Spec.ledger.batch_conserves`  tags `@id:batch_conserves`

```gherkin
Scenario Outline: Applying any batch of transfers conserves the total of all balances
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main
  Then the total of ledger Main's balances is unchanged

  Examples:
    | balances        | batch                       |
    | [100, 20, 0]    | [0->1:30, 1->2:50]          |
    | [5, 5]          | [0->1:6]                    |
    | [1, 0]          | [0->1:1, 0->1:1, 1->0:2]    |
    | []              | []                          |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_conserves.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.totalUnchanged main main'
```

```text
PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances
  kernel-checked   theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 162 of 162 grid points
  tested           4 of 4 rows pass on compiled Rust (cucumber-rs); 4 of 4 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_conserves.lean`):

```lean
theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h1⟩
```

### PROVED-FOR-ALL: A batch whose first transfer is invalid changes nothing

`features/ledger.feature:22`  id `Spec.ledger.batch_first_invalid`  tags `@id:batch_first_invalid`

```gherkin
Scenario Outline: A batch whose first transfer is invalid changes nothing
  Given ledger Main holds the balances <balances>
  And the first transfer of <batch> is not valid on ledger Main
  When the batch <batch> is applied to ledger Main
  Then no transfer is applied
  And ledger Main is unchanged

  Examples:
    | balances      | batch                  |
    | [5, 5]        | [0->1:6, 1->0:1]       |
    | [5, 5]        | [0->0:1]               |
    | [5, 5]        | [0->2:1, 0->1:1]       |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_first_invalid.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.firstInvalid main batch →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.appliedNone outcome ∧
      LVocab.unchanged main main'
```

```text
PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing
  kernel-checked   theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/batch_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 373 of 373 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_first_invalid.lean`):

```lean
theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt := by
  intro balances batch main _ hfirst
  obtain ⟨⟨n, l'⟩, e, -, -, h3, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  obtain ⟨h0, rfl⟩ := h3 hfirst
  exact ⟨n, _, e, h0, rfl⟩
```

### PROVED-FOR-ALL: The number of transfers applied is at most the length of the batch

`features/ledger.feature:36`  id `Spec.ledger.batch_count_bounded`  tags `@id:batch_count_bounded`

```gherkin
Scenario Outline: The number of transfers applied is at most the length of the batch
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main
  Then the number of transfers applied is at most the length of <batch>

  Examples:
    | balances      | batch                       |
    | [100, 20, 0]  | [0->1:30, 1->2:50]          |
    | [5, 5]        | [0->1:6]                    |
    | [7]           | []                          |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_count_bounded.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.appliedAtMost outcome batch
```

```text
PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch
  kernel-checked   theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_count_bounded.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_count_bounded.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 173 of 173 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_count_bounded.lean`):

```lean
theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, -, h2, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h2⟩
```

### PROVED-INSTANCE: A batch of two valid transfers is applied in full

`features/ledger.feature:49`  id `Spec.ledger.batch_example_all`  tags `@id:batch_example_all`

```gherkin
Scenario: A batch of two valid transfers is applied in full
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50] is applied to ledger Main
  Then exactly 2 transfers are applied
  And ledger Main now holds the balances [70, 0, 50]
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_example_all.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]) = ok (outcome, main') ∧
      LVocab.appliedExactly outcome (2#usize) ∧
      LVocab.nowHolds main' ([70#u64, 0#u64, 50#u64])
```

```text
PROVED-INSTANCE  A batch of two valid transfers is applied in full
  kernel-checked   theorem Spec.ledger.batch_example_all : Spec.ledger.batch_example_all.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_all.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_all.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 182 of 182 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_example_all.lean`):

```lean
theorem Spec.ledger.batch_example_all : Spec.ledger.batch_example_all.stmt := by
  intro main h
  -- literal values: take the exact result of the loop (the pure model `runN`) and compute it
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main _)
  refine ⟨n, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  refine ⟨?_, ledger.holds_of_nums (by simpa [ledger.nums] using hx.2)⟩
  simp only [LVocab.appliedExactly]; scalar_tac
```

### PROVED-INSTANCE: A batch stops at its first invalid transfer and keeps what it has applied

`features/ledger.feature:57`  id `Spec.ledger.batch_example_stop`  tags `@id:batch_example_stop`

```gherkin
Scenario: A batch stops at its first invalid transfer and keeps what it has applied
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 2->1:5, 0->1:1] is applied to ledger Main
  Then exactly 1 transfers are applied
  And ledger Main now holds the balances [70, 50, 0]
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_example_stop.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64, ledger.Transfer.mk 0#usize 1#usize 1#u64]) = ok (outcome, main') ∧
      LVocab.appliedExactly outcome (1#usize) ∧
      LVocab.nowHolds main' ([70#u64, 50#u64, 0#u64])
```

```text
PROVED-INSTANCE  A batch stops at its first invalid transfer and keeps what it has applied
  kernel-checked   theorem Spec.ledger.batch_example_stop : Spec.ledger.batch_example_stop.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_stop.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_stop.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 182 of 182 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_example_stop.lean`):

```lean
theorem Spec.ledger.batch_example_stop : Spec.ledger.batch_example_stop.stmt := by
  intro main h
  -- literal values: take the exact result of the loop (the pure model `runN`) and compute it
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main _)
  refine ⟨n, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  refine ⟨?_, ledger.holds_of_nums (by simpa [ledger.nums] using hx.2)⟩
  simp only [LVocab.appliedExactly]; scalar_tac
```

### REFUTED: A batch of transfers that are each valid on the starting ledger is applied in full

`features/ledger.feature:67`  id `Spec.ledger.batch_all_valid_all_applied`  tags `@id:batch_all_valid_all_applied @expect-refuted`

```gherkin
Scenario Outline: A batch of transfers that are each valid on the starting ledger is applied in full
  Given ledger Main holds the balances <balances>
  And every transfer of <batch> is valid on ledger Main
  When the batch <batch> is applied to ledger Main
  Then every transfer of <batch> is applied

  Examples:
    | balances      | batch                  |
    | [100, 20, 0]  | [0->1:30, 1->2:20]     |
    | [5, 5]        | [0->1:5]               |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_all_valid_all_applied.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.allValid main batch →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.appliedAll outcome batch
```

```text
REFUTED  A batch of transfers that are each valid on the starting ledger is applied in full
  kernel-checked   theorem Spec.ledger.batch_all_valid_all_applied.refuted : ¬ Spec.ledger.batch_all_valid_all_applied.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances | batch            |
                   | [1, 0]   | [0->1:1, 0->1:1] |
                   When the batch [0->1:1, 0->1:1] is applied to ledger Main  =>  returned 1 applied; Main: balances [0, 1]
                   failed Then: "every transfer of [0->1:1, 0->1:1] is applied"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-all-valid, LW-batch, LT-all-applied
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 380 of 380 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 207 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### PROVED-FOR-ALL: A valid transfer is accepted and moves exactly its amount

`features/ledger.feature:79`  id `Spec.ledger.transfer_valid_moves`  tags `@id:transfer_valid_moves`

```gherkin
Scenario Outline: A valid transfer is accepted and moves exactly its amount
  Given ledger Main holds the balances <balances>
  And the transfer <t> is valid on ledger Main
  When the transfer <t> is applied to ledger Main
  Then it is accepted
  And the amount of <t> has moved between its accounts in ledger Main and no other balance changed
  And the total of ledger Main's balances is unchanged

  Examples:
    | balances        | t         |
    | [100, 20, 0]    | 0->2:100  |
    | [1, 2, 3]       | 2->0:1    |
    | [0, 0]          | 1->0:0    |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.transfer_valid_moves.stmt : Prop :=
  ∀ (balances : List U64) (t : ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.validOn main t →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply main t = ok (outcome, main') ∧
      LVocab.accepted outcome ∧
      LVocab.moved main main' t ∧
      LVocab.totalUnchanged main main'
```

```text
PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount
  kernel-checked   theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_valid_moves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_valid_moves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 704 of 704 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/transfer_valid_moves.lean`):

```lean
theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt := by
  intro balances t main _ hvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨hb, -, hm, ht, -⟩ | ⟨-, hinv, -⟩ := h
  · exact ⟨b, l', e, hb, hm, ht⟩
  · exact absurd hvalid hinv
```

### PROVED-FOR-ALL: An invalid transfer is rejected and changes nothing

`features/ledger.feature:94`  id `Spec.ledger.transfer_invalid_rejected`  tags `@id:transfer_invalid_rejected`

```gherkin
Scenario Outline: An invalid transfer is rejected and changes nothing
  Given ledger Main holds the balances <balances>
  And the transfer <t> is not valid on ledger Main
  When the transfer <t> is applied to ledger Main
  Then it is rejected
  And ledger Main is unchanged

  Examples:
    | balances                        | t         |
    | [100, 20, 0]                    | 0->2:101  |
    | [100, 20, 0]                    | 0->3:1    |
    | [100, 20, 0]                    | 3->0:1    |
    | [100, 20, 0]                    | 1->1:5    |
    | [1, 18446744073709551615]       | 0->1:1    |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.transfer_invalid_rejected.stmt : Prop :=
  ∀ (balances : List U64) (t : ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.invalidOn main t →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply main t = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.unchanged main main'
```

```text
PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_invalid_rejected.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_invalid_rejected.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-invalid, LW-transfer, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 218 of 218 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/transfer_invalid_rejected.lean`):

```lean
theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt := by
  intro balances t main _ hinvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨-, hv, -⟩ | ⟨hb, -, rfl, -⟩ := h
  · exact absurd hv hinvalid
  · exact ⟨b, _, e, hb, rfl⟩
```

### PROVED-FOR-ALL: The total is the sum of the balances when that fits

`features/ledger.feature:110`  id `Spec.ledger.total_is_sum`  tags `@id:total_is_sum`

```gherkin
Scenario Outline: The total is the sum of the balances when that fits
  Given ledger Main holds the balances <balances>
  And the balances of ledger Main add up to <sum>
  When the total of ledger Main is computed
  Then the result is <sum>

  Examples:
    | balances                    | sum                  |
    | [100, 20, 0]                | 120                  |
    | []                          | 0                    |
    | [18446744073709551615, 0]   | 18446744073709551615 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_is_sum.stmt : Prop :=
  ∀ (balances : List U64) (sum : U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumsTo main sum →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.resultIs outcome sum
```

```text
PROVED-FOR-ALL  The total is the sum of the balances when that fits
  kernel-checked   theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/total_is_sum.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_is_sum.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 165 of 165 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/total_is_sum.lean`):

```lean
theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt := by
  intro balances sum main _ hsum
  obtain ⟨o, e, h1, -⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  obtain ⟨s, rfl, hs⟩ := h1 (by rw [hsum]; scalar_tac)
  refine ⟨_, e, ?_⟩
  simp only [LVocab.resultIs, Option.some.injEq]
  scalar_tac
```

### PROVED-FOR-ALL: The total of balances that do not fit is reported as absent

`features/ledger.feature:123`  id `Spec.ledger.total_overflow`  tags `@id:total_overflow`

```gherkin
Scenario Outline: The total of balances that do not fit is reported as absent
  Given ledger Main holds the balances <balances>
  And the balances of ledger Main add up to more than the maximum
  When the total of ledger Main is computed
  Then there is no result

  Examples:
    | balances                                       |
    | [18446744073709551615, 1]                      |
    | [9223372036854775808, 5, 9223372036854775808]  |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_overflow.stmt : Prop :=
  ∀ (balances : List U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumTooBig main →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.noResult outcome
```

```text
PROVED-FOR-ALL  The total of balances that do not fit is reported as absent
  kernel-checked   theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/total_overflow.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 95 of 95 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/total_overflow.lean`):

```lean
theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt := by
  intro balances main _ hbig
  obtain ⟨o, e, -, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  exact ⟨o, e, h2 hbig⟩
```

### REFUTED: The total of a ledger can always be computed

`features/ledger.feature:136`  id `Spec.ledger.total_always_available`  tags `@id:total_always_available @expect-refuted`

```gherkin
Scenario Outline: The total of a ledger can always be computed
  Given ledger Main holds the balances <balances>
  When the total of ledger Main is computed
  Then there is a result

  Examples:
    | balances        |
    | [100, 20, 0]    |
    | []              |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_always_available.stmt : Prop :=
  ∀ (balances : List U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.someResult outcome
```

```text
REFUTED  The total of a ledger can always be computed
  kernel-checked   theorem Spec.ledger.total_always_available.refuted : ¬ Spec.ledger.total_always_available.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances                  |
                   | [18446744073709551615, 1] |
                   When the total of ledger Main is computed  =>  returned None
                   failed Then: "there is a result"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-total, LT-some-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 86 of 86 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 9 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### PROVED-FOR-ALL: Looking up an existing account gives its balance

`features/ledger.feature:147`  id `Spec.ledger.balance_of_account`  tags `@id:balance_of_account`

```gherkin
Scenario Outline: Looking up an existing account gives its balance
  Given ledger Main holds the balances <balances>
  And <i> is an account of ledger Main
  When the balance of account <i> of ledger Main is looked up
  Then the result is the balance of account <i> of ledger Main

  Examples:
    | balances      | i |
    | [100, 20, 0]  | 0 |
    | [100, 20, 0]  | 2 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.balance_of_account.stmt : Prop :=
  ∀ (balances : List U64) (i : Usize) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.isAccount main i →
    ∃ (outcome : Option U64),
      ledger.Ledger.balance main i = ok (outcome) ∧
      LVocab.resultIsBalance outcome main i
```

```text
PROVED-FOR-ALL  Looking up an existing account gives its balance
  kernel-checked   theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_of_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_of_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-account, LW-balance, LT-balance
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 351 of 351 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/balance_of_account.lean`):

```lean
theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt := by
  intro balances i main _ hacc
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec main i)
  refine ⟨o, e, h, ?_⟩
  simp_all [LVocab.isAccount]
```

### PROVED-FOR-ALL: Looking up an account that does not exist gives nothing

`features/ledger.feature:159`  id `Spec.ledger.balance_no_account`  tags `@id:balance_no_account`

```gherkin
Scenario Outline: Looking up an account that does not exist gives nothing
  Given ledger Main holds the balances <balances>
  And <i> is not an account of ledger Main
  When the balance of account <i> of ledger Main is looked up
  Then there is no result

  Examples:
    | balances      | i |
    | [100, 20, 0]  | 3 |
    | []            | 0 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.balance_no_account.stmt : Prop :=
  ∀ (balances : List U64) (i : Usize) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.notAccount main i →
    ∃ (outcome : Option U64),
      ledger.Ledger.balance main i = ok (outcome) ∧
      LVocab.noResult outcome
```

```text
PROVED-FOR-ALL  Looking up an account that does not exist gives nothing
  kernel-checked   theorem Spec.ledger.balance_no_account : Spec.ledger.balance_no_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_no_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_no_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-no-account, LW-balance, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 131 of 131 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/balance_no_account.lean`):

```lean
theorem Spec.ledger.balance_no_account : Spec.ledger.balance_no_account.stmt := by
  intro balances i main _ hnone
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec main i)
  refine ⟨o, e, ?_⟩
  simp_all [LVocab.notAccount]
```

### PROVED-FOR-ALL: Applying a batch as a whole conserves the total of all balances

`features/ledger.feature:171`  id `Spec.ledger.whole_conserves`  tags `@id:whole_conserves`

```gherkin
Scenario Outline: Applying a batch as a whole conserves the total of all balances
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main as a whole
  Then the total of ledger Main's balances is unchanged

  Examples:
    | balances        | batch                  |
    | [100, 20, 0]    | [0->1:30, 1->2:50]     |
    | [100, 20, 0]    | [0->1:30, 1->2:51]     |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_conserves.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main batch = ok (outcome, main') ∧
      LVocab.totalUnchanged main main'
```

```text
PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances
  kernel-checked   theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 162 of 162 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_conserves.lean`):

```lean
theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, h1⟩
```

### PROVED-FOR-ALL: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing

`features/ledger.feature:182`  id `Spec.ledger.whole_first_invalid`  tags `@id:whole_first_invalid`

```gherkin
Scenario Outline: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
  Given ledger Main holds the balances <balances>
  And the first transfer of <batch> is not valid on ledger Main
  When the batch <batch> is applied to ledger Main as a whole
  Then it is rejected
  And ledger Main is unchanged

  Examples:
    | balances      | batch                  |
    | [5, 5]        | [0->1:6, 1->0:1]       |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_first_invalid.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.firstInvalid main batch →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main batch = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.unchanged main main'
```

```text
PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.whole_first_invalid : Spec.ledger.whole_first_invalid.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/whole_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-whole, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 371 of 371 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_first_invalid.lean`):

```lean
theorem Spec.ledger.whole_first_invalid : Spec.ledger.whole_first_invalid.stmt := by
  intro balances batch main _ hfirst
  obtain ⟨⟨b, l'⟩, e, -, h2, h3, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  have hb := h3 hfirst
  obtain rfl := h2 hb
  exact ⟨b, _, e, hb, rfl⟩
```

### PROVED-INSTANCE: A batch of valid transfers applied as a whole is accepted and applied

`features/ledger.feature:195`  id `Spec.ledger.whole_example_accept`  tags `@id:whole_example_accept`

```gherkin
Scenario: A batch of valid transfers applied as a whole is accepted and applied
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50] is applied to ledger Main as a whole
  Then it is accepted
  And ledger Main now holds the balances [70, 0, 50]
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_accept.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]) = ok (outcome, main') ∧
      LVocab.accepted outcome ∧
      LVocab.nowHolds main' ([70#u64, 0#u64, 50#u64])
```

```text
PROVED-INSTANCE  A batch of valid transfers applied as a whole is accepted and applied
  kernel-checked   theorem Spec.ledger.whole_example_accept : Spec.ledger.whole_example_accept.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/whole_example_accept.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_accept.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-accepted, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 164 of 164 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_example_accept.lean`):

```lean
theorem Spec.ledger.whole_example_accept : Spec.ledger.whole_example_accept.stmt := by
  intro main h
  -- literal values: the pure model `runN` applies both transfers, so the batch is accepted
  obtain ⟨⟨b, l'⟩, e, -, -, -, hx, hy⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main _)
  refine ⟨b, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx hy
  exact ⟨hx, ledger.holds_of_nums (by simpa [ledger.nums] using hy hx)⟩
```

### PROVED-INSTANCE: A batch applied as a whole is rolled back when a later transfer is invalid

`features/ledger.feature:203`  id `Spec.ledger.whole_example_rollback`  tags `@id:whole_example_rollback`

```gherkin
Scenario: A batch applied as a whole is rolled back when a later transfer is invalid
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 2->1:5] is applied to ledger Main as a whole
  Then it is rejected
  And ledger Main now holds the balances [100, 20, 0]
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_rollback.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64]) = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.nowHolds main' ([100#u64, 20#u64, 0#u64])
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when a later transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback : Spec.ledger.whole_example_rollback.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 164 of 164 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_example_rollback.lean`):

```lean
theorem Spec.ledger.whole_example_rollback : Spec.ledger.whole_example_rollback.stmt := by
  intro main h
  -- literal values: the pure model `runN` applies 1 of the 2 transfers, so the batch is rejected
  obtain ⟨⟨b, l'⟩, e, -, hback, -, hx, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main _)
  refine ⟨b, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  obtain rfl := hback hx
  exact ⟨hx, h⟩
```

### PROVED-FOR-ALL: The total computed after any batch is the total before it

`features/ledger.feature:212`  id `Spec.ledger.batch_then_total`  tags `@id:batch_then_total`

```gherkin
Scenario Outline: The total computed after any batch is the total before it
  Given ledger Main holds the balances <balances>
  And the balances of ledger Main add up to <sum>
  When the batch <batch> is applied to ledger Main
  And the total of ledger Main is computed
  Then the result is <sum>

  Examples:
    | balances        | sum | batch                    |
    | [100, 20, 0]    | 120 | [0->1:30, 1->2:50]       |
    | [5, 5]          | 10  | [0->1:6]                 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_then_total.stmt : Prop :=
  ∀ (balances : List U64) (sum : U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumsTo main sum →
    ∃ (outcome_1 : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome_1, main') ∧
    ∃ (outcome : Option U64),
      ledger.Ledger.total main' = ok (outcome) ∧
      LVocab.resultIs outcome sum
```

```text
PROVED-FOR-ALL  The total computed after any batch is the total before it
  kernel-checked   theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt (type checked by the audit; 10-line proof, lean/Wallet/Proofs/ledger/batch_then_total.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-batch, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 165 of 165 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_then_total.lean`):

```lean
theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt := by
  intro balances sum batch main _ hsum
  -- first When: the batch loop conserves the total
  obtain ⟨⟨n, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  refine ⟨n, l1, e1, ?_⟩
  -- second When: the summing loop, on the ledger the batch left
  obtain ⟨o, e2, h2, -⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec l1)
  obtain ⟨s, rfl, hs⟩ := h2 (by rw [h1, hsum]; scalar_tac)
  refine ⟨_, e2, ?_⟩
  simp only [LVocab.resultIs, Option.some.injEq]
  scalar_tac
```

### PROVED-FOR-ALL: Two batches applied one after the other conserve the total

`features/ledger.feature:226`  id `Spec.ledger.two_batches_conserve`  tags `@id:two_batches_conserve`

```gherkin
Scenario Outline: Two batches applied one after the other conserve the total
  Given ledger Main holds the balances <balances>
  When the batch <first> is applied to ledger Main
  And the batch <second> is applied to ledger Main
  Then the total of ledger Main's balances is unchanged
  And the number of transfers applied is at most the length of <second>

  Examples:
    | balances        | first                | second              |
    | [100, 20, 0]    | [0->1:30, 1->2:50]   | [2->0:50, 0->1:1]   |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.two_batches_conserve.stmt : Prop :=
  ∀ (balances : List U64) (first second : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome_1 : Usize) (main_1 : ledger.Ledger),
      ledger.Ledger.apply_batch main first = ok (outcome_1, main_1) ∧
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main_1 second = ok (outcome, main') ∧
      LVocab.totalUnchanged main main' ∧
      LVocab.appliedAtMost outcome second
```

```text
PROVED-FOR-ALL  Two batches applied one after the other conserve the total
  kernel-checked   theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/two_batches_conserve.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.two_batches_conserve.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.apply_batch, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 254 of 254 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/two_batches_conserve.lean`):

```lean
theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt := by
  intro balances first second main _
  obtain ⟨⟨n1, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main first)
  refine ⟨n1, l1, e1, ?_⟩
  obtain ⟨⟨n2, l2⟩, e2, h2, hle, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec l1 second)
  exact ⟨n2, l2, e2, h2.trans h1, hle⟩
```

### VACUOUS: A withdrawal that is both covered and not covered

`features/negative.feature:8`  id `Spec.negative_controls.contradictory_givens`  tags `@id:contradictory_givens @expect-vacuous`

```gherkin
Scenario Outline: A withdrawal that is both covered and not covered
  Given Alice has a balance of <a>
  And <amount> is more than Alice's balance
  And <amount> is not more than Alice's balance
  When Alice withdraws <amount>
  Then the operation succeeds

  Examples:
    | a | amount |
    | 5 | 6      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.negative_controls.contradictory_givens.stmt : Prop :=
  ∀ (a amount : U64) (alice : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.exceeds amount alice →
    Vocab.covers alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.withdraw alice amount = ok (outcome, alice') ∧
      Vocab.succeeds outcome
```

```text
VACUOUS  A withdrawal that is both covered and not covered
  kernel-checked   theorem Spec.negative_controls.contradictory_givens.unsat: no input satisfies all the Givens; axioms propext, Quot.sound
  meaning          the scenario is true of nothing; any proof of it would be worthless
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, G-covers, W-withdraw, T-ok
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 111 of 111 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
```

### PROVED-FOR-ALL (1 of 2 Thens substantive): A deposit does not touch a bystander

`features/negative.feature:22`  id `Spec.negative_controls.bystander_unchanged`  tags `@id:bystander_unchanged`

```gherkin
Scenario Outline: A deposit does not touch a bystander
  Given Alice has a balance of <a>
  And Bob has a balance of <b>
  And Alice's balance plus <amount> does not exceed the maximum
  When Alice deposits <amount>
  Then the operation succeeds
  And Bob's balance is unchanged

  Examples:
    | a | b | amount |
    | 1 | 2 | 3      |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.negative_controls.bystander_unchanged.stmt : Prop :=
  ∀ (a b amount : U64) (alice bob : wallet.Wallet),
    Vocab.hasBalance alice a →
    Vocab.hasBalance bob b →
    Vocab.roomFor alice amount →
    ∃ (outcome : Vocab.Outcome) (alice' : wallet.Wallet),
      wallet.Wallet.deposit alice amount = ok (outcome, alice') ∧
      Vocab.succeeds outcome ∧
      Vocab.unchanged bob bob
```

```text
PROVED-FOR-ALL (1 of 2 Thens substantive)  A deposit does not touch a bystander
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/negative_controls/bystander_unchanged.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.negative_controls.bystander_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen e66d2bb71733 (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 111 of 111 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  flag             TRIVIAL-THEN: follows from the Givens alone, whatever the code does: "Bob's balance is unchanged"
  flag             FRAME-TRIVIAL: the call does not return this actor, so the Then compares it with itself: "Bob's balance is unchanged"
```

Proof (`lean/Wallet/Proofs/negative_controls/bystander_unchanged.lean`):

```lean
theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt := by
  intro a b amount alice bob h1 h2 h3
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

## Glossary (the link from English to Lean)

Each English phrase and the one Lean definition (or model function) it is bound to. This table, `lean/Wallet/Vocab.lean` and `lean/Ledger/Vocab.lean` are what a reviewer has to read to trust the step from English to Lean. The last column compares that Lean definition with a second, independently written reading of the same phrase (the Rust predicate in `wallet-bdd/src/lib.rs` that the cucumber step asserts) on a grid of arguments. Agreement does not show that either reading matches the English; disagreement shows that one of them is wrong.

| Id | Kind | English phrase | Lean | Definition | Sign-off | Rust step regex identical | Lean vs Rust reading |
|---|---|---|---|---|---|---|---|
| G-balance | given | {wallet:w} has a balance of {amount:n} | `Vocab.hasBalance` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance = n` | UNREVIEWED | yes | agree on 36 of 36 |
| G-covers | given | {amount:n} is not more than {wallet:w}'s balance | `Vocab.covers` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val` | UNREVIEWED | yes | agree on 36 of 36 |
| G-exceeds | given | {amount:n} is more than {wallet:w}'s balance | `Vocab.exceeds` applied to `n, pre(w)` | `(n : U64) (w : Wallet) : Prop := w.balance.val < n.val` | UNREVIEWED | yes | agree on 36 of 36 |
| G-room | given | {wallet:w}'s balance plus {amount:n} does not exceed the maximum | `Vocab.roomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max` | UNREVIEWED | yes | agree on 36 of 36 |
| G-noroom | given | {wallet:w}'s balance plus {amount:n} exceeds the maximum | `Vocab.noRoomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := U64.max < w.balance.val + n.val` | UNREVIEWED | yes | agree on 36 of 36 |
| W-transfer | when | {wallet:src} transfers {amount:n} to {wallet:dst} | `wallet.transfer` applied to `pre(src), pre(dst), n` | Aeneas-generated model of Rust `wallet::transfer`; returns `outcome, post(src), post(dst)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| W-deposit | when | {wallet:w} deposits {amount:n} | `wallet.Wallet.deposit` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::deposit`; returns `outcome, post(w)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| W-withdraw | when | {wallet:w} withdraws {amount:n} | `wallet.Wallet.withdraw` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::withdraw`; returns `outcome, post(w)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| T-ok | then | the operation succeeds | `Vocab.succeeds` applied to `outcome` | `(o : Outcome) : Prop := o = .Ok ()` | UNREVIEWED | yes | agree on 3 of 3 |
| T-err | then | the operation is rejected with {error:e} | `Vocab.rejectedWith` applied to `outcome, e` | `(o : Outcome) (e : WalletError) : Prop := o = .Err e` | UNREVIEWED | yes | agree on 6 of 6 |
| T-dec | then | {wallet:w}'s balance is decreased by {amount:n} | `Vocab.decreasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val` | UNREVIEWED | yes | agree on 216 of 216 |
| T-inc | then | {wallet:w}'s balance is increased by {amount:n} | `Vocab.increasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val` | UNREVIEWED | yes | agree on 216 of 216 |
| T-same | then | {wallet:w}'s balance is unchanged | `Vocab.unchanged` applied to `pre(w), post(w)` | `(pre post : Wallet) : Prop := post = pre` | UNREVIEWED | yes | agree on 36 of 36 |
| T-total | then | the total of all balances is unchanged | `Vocab.totalUnchanged` applied to `all_pre(wallet), all_post(wallet)` | `(pre post : List Wallet) : Prop := (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum` | UNREVIEWED | yes | agree on 1296 of 1296 |
| LG-holds | given | ledger {ledger:l} holds the balances {balances:bs} | `LVocab.holds` applied to `pre(l), bs` | `(l : Ledger) (bs : List U64) : Prop := l.balances.val = bs` | UNREVIEWED | yes | agree on 81 of 81 |
| LG-sums-to | given | the balances of ledger {ledger:l} add up to {amount:s} | `LVocab.sumsTo` applied to `pre(l), s` | `(l : Ledger) (s : U64) : Prop := total l = s.val` | UNREVIEWED | yes | agree on 54 of 54 |
| LG-sum-too-big | given | the balances of ledger {ledger:l} add up to more than the maximum | `LVocab.sumTooBig` applied to `pre(l)` | `(l : Ledger) : Prop := U64.max < total l` | UNREVIEWED | yes | agree on 9 of 9 |
| LG-account | given | {index:i} is an account of ledger {ledger:l} | `LVocab.isAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | UNREVIEWED | yes | agree on 45 of 45 |
| LG-no-account | given | {index:i} is not an account of ledger {ledger:l} | `LVocab.notAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := l.balances.val.length ≤ i.val` | UNREVIEWED | yes | agree on 45 of 45 |
| LG-valid | given | the transfer {transfer:t} is valid on ledger {ledger:l} | `LVocab.validOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := valid l t` | UNREVIEWED | yes | agree on 54 of 54 |
| LG-invalid | given | the transfer {transfer:t} is not valid on ledger {ledger:l} | `LVocab.invalidOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := ¬ valid l t` | UNREVIEWED | yes | agree on 54 of 54 |
| LG-first-invalid | given | the first transfer of {batch:b} is not valid on ledger {ledger:l} | `LVocab.firstInvalid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := b.val ≠ [] ∧ ∀ t ∈ b.val.head?, ¬ valid l t` | UNREVIEWED | yes | agree on 207 of 207 |
| LG-all-valid | given | every transfer of {batch:b} is valid on ledger {ledger:l} | `LVocab.allValid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := ∀ t ∈ b.val, valid l t` | UNREVIEWED | yes | agree on 207 of 207 |
| LW-batch | when | the batch {batch:b} is applied to ledger {ledger:l} | `ledger.Ledger.apply_batch` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_batch`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-whole | when | the batch {batch:b} is applied to ledger {ledger:l} as a whole | `ledger.Ledger.apply_all` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_all`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-transfer | when | the transfer {transfer:t} is applied to ledger {ledger:l} | `ledger.Ledger.apply` applied to `pre(l), t` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-total | when | the total of ledger {ledger:l} is computed | `ledger.Ledger.total` applied to `pre(l)` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::total`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-balance | when | the balance of account {index:i} of ledger {ledger:l} is looked up | `ledger.Ledger.balance` applied to `pre(l), i` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::balance`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LT-total-same | then | the total of ledger {ledger:l}'s balances is unchanged | `LVocab.totalUnchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := total post = total pre` | UNREVIEWED | yes | agree on 81 of 81 |
| LT-same | then | ledger {ledger:l} is unchanged | `LVocab.unchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := post.balances.val = pre.balances.val` | UNREVIEWED | yes | agree on 81 of 81 |
| LT-now-holds | then | ledger {ledger:l} now holds the balances {balances:bs} | `LVocab.nowHolds` applied to `post(l), bs` | `(post : Ledger) (bs : List U64) : Prop := post.balances.val = bs` | UNREVIEWED | yes | agree on 81 of 81 |
| LT-at-most | then | the number of transfers applied is at most the length of {batch:b} | `LVocab.appliedAtMost` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val ≤ b.val.length` | UNREVIEWED | yes | agree on 92 of 92 |
| LT-none-applied | then | no transfer is applied | `LVocab.appliedNone` applied to `outcome` | `(n : Usize) : Prop := n.val = 0` | UNREVIEWED | yes | agree on 4 of 4 |
| LT-all-applied | then | every transfer of {batch:b} is applied | `LVocab.appliedAll` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val = b.val.length` | UNREVIEWED | yes | agree on 92 of 92 |
| LT-exactly | then | exactly {index:k} transfers are applied | `LVocab.appliedExactly` applied to `outcome, k` | `(n : Usize) (k : Usize) : Prop := n = k` | UNREVIEWED | yes | agree on 20 of 20 |
| LT-result | then | the result is {amount:s} | `LVocab.resultIs` applied to `outcome, s` | `(o : Option U64) (s : U64) : Prop := o = some s` | UNREVIEWED | yes | agree on 30 of 30 |
| LT-no-result | then | there is no result | `LVocab.noResult` applied to `outcome` | `(o : Option U64) : Prop := o = none` | UNREVIEWED | yes | agree on 5 of 5 |
| LT-some-result | then | there is a result | `LVocab.someResult` applied to `outcome` | `(o : Option U64) : Prop := o ≠ none` | UNREVIEWED | yes | agree on 5 of 5 |
| LT-balance | then | the result is the balance of account {index:i} of ledger {ledger:l} | `LVocab.resultIsBalance` applied to `outcome, pre(l), i` | `(o : Option U64) (l : Ledger) (i : Usize) : Prop := o = l.balances.val[i.val]? ∧ o ≠ none` | UNREVIEWED | yes | agree on 225 of 225 |
| LT-accepted | then | it is accepted | `LVocab.accepted` applied to `outcome` | `(ok : Bool) : Prop := ok = true` | UNREVIEWED | yes | agree on 2 of 2 |
| LT-rejected | then | it is rejected | `LVocab.rejected` applied to `outcome` | `(ok : Bool) : Prop := ok = false` | UNREVIEWED | yes | agree on 2 of 2 |
| LT-moved | then | the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed | `LVocab.moved` applied to `pre(l), post(l), t` | `(pre post : Ledger) (t : Transfer) : Prop := post.balances.val.length = pre.balances.val.length ∧ bal post t.from.val + t.amount.val = bal pre t.from.val ∧ bal post t.to.val = bal pre t.to.val + t.amount.val ∧ ∀ k < pre.balances.val.length, k ≠ t.from.val → k ≠ t.to.val → bal post k = bal pre k` | UNREVIEWED | yes | agree on 486 of 486 |

42 of 42 entries are unreviewed. Record a review with `python3 -m slicegen review <id> --reviewer <name>`; any later change to the phrase, its argument order or its definition voids it.

## Trusted base

- **Rust to Lean**: `lean/Generated/Wallet.lean` and `lean/Generated/Ledger.lean` are produced by Charon + Aeneas from `wallet/src/lib.rs` and `ledger/src/lib.rs`. Hashes of inputs and outputs are in `lean/provenance.json`. The theorems are about the Lean models. A Rust `while` loop becomes a call of Aeneas's `loop` combinator on a separately generated loop-body function.
- **Hand-written loop lemmas** (`lean/Ledger/Lemmas/`, one module per Rust function): not trusted. They are kernel-checked like any proof, and they appear in no statement; a scenario proof that uses one is still checked against exactly its statement.
- **Aeneas library models** (hand-written Lean standing in for std operations): `Aeneas.Std.U64.checked_add` for `u64::checked_add`; `Aeneas.Std.instHSubUScalarResult` for `u64 - u64 (panics on underflow)`; `Aeneas.Std.instHAddUScalarResult` for `usize + usize (panics on overflow)`; `Aeneas.Std.alloc.vec.Vec.len` for `Vec::len`; `Aeneas.Std.alloc.vec.Vec.index` for `Vec indexing v[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.Vec.index_mut` for `Vec indexing v[i] = x (panics out of bounds)`; `Aeneas.Std.Slice.len` for `slice::len`; `Aeneas.Std.Slice.index_usize` for `slice indexing s[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.CloneVec.clone` for `Vec::clone`; `Aeneas.Std.loop` for `while loop (Aeneas's fixed-point combinator; a loop that never ends is `div`)`.
- **slicegen**: untrusted generator. Defences: Lean type-checks its output; the audit compares the constants in each elaborated statement with the glossary entries of the scenario's steps; the statement is printed above.
- **The audit** (`lean/Bdd/Audit.lean`, about 120 lines): reads from the Lean environment which axioms each theorem uses, that each proof's type is exactly its scenario's statement, and which constants statements and definitions mention.
- **Glossary**: `glossary.yaml` + `lean/Wallet/Vocab.lean` + `lean/Ledger/Vocab.lean`. The audit checks that no Given/Then definition depends on a model function: passed for all 34 definitions.
- **Second reading of each phrase**: the Rust predicates in `wallet-bdd/src/lib.rs`, asserted by the cucumber steps in `wallet-bdd/tests/bdd.rs`. The step regexes are checked against the glossary; the predicates are compared with the Lean definitions on a grid of arguments (table above) and by Examples rows giving the same result on both sides.
- **Lean kernel** and the axioms `propext`, `Classical.choice`, `Quot.sound`; **rustc** for everything said about the compiled Rust.

## What this run did not check

- That any glossary definition means what its English phrase says. Only a person can.
- A scenario with several Whens says that each call returns and constrains the state after the LAST one (and the last call's result). Results of earlier Whens are not constrained, no kernel refutation is generated for such a scenario, and it does not count towards input coverage.
- A counterexample to a scenario about a loop is confirmed in the kernel only if a hand-proved lemma about that loop says enough at that input (here: the exact-result lemmas in `lean/Ledger/Lemmas/`). Without one the verdict is COUNTEREXAMPLE, not REFUTED.
- The boundary grid is small (the product of each parameter's sample values plus literals and their neighbours); there is no random sampling and no shrinking. A false scenario whose counterexamples all lie away from the boundaries would be TESTED-ONLY, not REFUTED. The same holds for the grid on which the two readings of a phrase are compared.
- The trivial-Then check is a `simp`/`scalar_tac` attempt. A Then that follows from the Givens by harder reasoning is not flagged, and a Then that is true but weaker than the English is invisible to it.
- Input coverage says every input falls under some scenario's Givens. It does not say the Thens of that scenario pin the result down; that is what the mutation run measures, for the mutants it happens to contain.
- The derived theorems (`.sat`, `.unsat`, `.refuted`, coverage, trivial-Then attempts) are checked by one `lean` run over `lean/Run/Audit.lean`, not stored as library modules. Trivial-Then attempts are expected to fail; their errors are in `out/audit.log`.
- Staleness is computed from the digests in `out/graph.json`, but every run regenerates everything, so nothing is ever stale here. `python3 -m slicegen.graphlint out/graph.json --what-if <node-id>` shows what would be.

## Refinement graph

`out/graph.json`: 322 nodes, 782 edges, 43 verdicts. Evidence entries by kind: kernel-checked 66, tested 299, tool-trusted 480. Edges claimed with no evidence at all: 76 (the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.
