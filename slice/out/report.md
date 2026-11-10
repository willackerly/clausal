# Slice: scenario report (wallet and ledger)

Generated 2026-11-10T12:35:53+00:00 by `slice/run.sh`. Lean `leanprover/lean4:v4.35.0`, Aeneas `nightly-2026.11.09-5a392f4`, Charon `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, slicegen 9b7dcdf4ec25 (slicegen-rule/3).

Each scenario below is an English claim about one of the Rust crates `slice/wallet` (three straight-line functions) and `slice/ledger` (loops over a `Vec` and a slice). The claim is turned into a Lean statement about the Aeneas-generated Lean model of that crate, and the statement is then proved, refuted or left open. Every link in that chain is labelled with the kind of evidence behind it:

| Evidence kind | Meaning here |
|---|---|
| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |
| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, and the two readings of each phrase compared on a grid. |
| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, slicegen (scenario to statement), and the audit that reads facts out of the Lean environment. |
| human-asserted | A person's say-so: that each glossary phrase means its Lean definition. Nothing checks this. It exists only where someone has signed off. |

Scenarios sit under Gherkin `Rule:` lines. A rule line is a plain-English claim and is carried here as written; it is **not** compiled to Lean. What is proved is each scenario beneath it, and those scenarios together are the rule's suite.

## Rules

Generated from `out/graph.json` (`python3 -m slicegen rules` prints the same from the stored graph). The full block of each rule, with what it rests on, is under [Rules and their scenarios](#rules-and-their-scenarios).

| Rule | Verdict | Examples on Rust / on model | Suite adequacy (informational) |
|---|---|---|---|
| Rule: A transfer never changes the total of all balances (`features/wallet.feature:10`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 1 PROVED-INSTANCE | 7 / 7 of 7 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A withdrawal takes exactly the amount, or is rejected and takes nothing (`features/wallet.feature:72`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A deposit adds exactly the amount, or is rejected and adds nothing (`features/wallet.feature:101`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A transfer the sender can afford always succeeds (`features/wallet.feature:131`) | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: A deposit earns interest (`features/wallet.feature:151`) | **NO SCENARIO PROVED**<br>1 UNBOUND | - / 0 of 0 | not assessed: no scenario of this group is meant to be proved |
| Rule: Applying a batch of transfers never changes the total of all balances (`features/ledger.feature:11`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL | 12 / 12 of 12 | suite rules out: reject-all, identity, constant; still allows: no-op: reports every transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the search grid] |
| Rule: A batch reports how many transfers it applied, and applies none when the first is invalid (`features/ledger.feature:63`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL, 2 PROVED-INSTANCE | 8 / 8 of 8 | suite rules out: no-op, constant; still allows: reject-all: always answers `0` and leaves the state as it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid] |
| Rule: A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:108`) | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: A single transfer moves exactly its amount, or is rejected and changes nothing (`features/ledger.feature:126`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 8 / 8 of 8 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: The total of a ledger is the sum of its balances, or absent when the sum does not fit (`features/ledger.feature:159`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 8 / 8 of 8 | suite rules out: reject-all, no-op; still allows: (none found) |
| Rule: The total of a ledger can always be computed (`features/ledger.feature:189`) | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: Looking up an account gives its balance, or nothing when there is no such account (`features/ledger.feature:204`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 4 / 4 of 4 | suite rules out: reject-all, no-op; still allows: (none found) |
| Rule: A batch applied as a whole is applied completely or not at all (`features/ledger.feature:230`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 3 PROVED-INSTANCE | 10 / 10 of 10 | suite rules out: no-op, constant; still allows: reject-all: always answers `false` and leaves the state as it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid] |
| Rule: Applying a batch does not change the total that is computed afterwards (`features/ledger.feature:295`) | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | [ledger.Ledger.apply_batch] suite rules out: (nothing); still allows: reject-all: always answers `0` and leaves the state as it was [no scenario counted is false of it on the search grid]; no-op: reports every transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the search grid]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid]; constant (4 of 9 variants): always answers `1` and leaves the state as it was; always answers `2` and leaves the state as it was; and 2 more [no scenario counted is false of it on the search grid]<br>[ledger.Ledger.total] suite rules out: reject-all, no-op; still allows: (none found) |
| (scenarios of `Feature: Negative controls` that are not under a Rule) (`features/negative.feature`) | **SOME SCENARIOS PROVED**<br>1 VACUOUS, 1 PROVED-FOR-ALL | 1 / 1 of 2 | not assessed: its scenarios are tagged @control |

## Summary

| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |
|---|---|---|---|---|
| A covered transfer moves the money and conserves the total (`features/wallet.feature:16`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (8 of 8) |
| Transferring more than the sender has is rejected and changes nothing (`features/wallet.feature:33`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A transfer the receiver has no room for is rejected and changes nothing (`features/wallet.feature:48`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6) |
| Transferring more than you have is rejected and changes nothing (`features/wallet.feature:64`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A covered withdrawal succeeds and takes exactly the amount (`features/wallet.feature:75`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| Withdrawing more than the balance is rejected and changes nothing (`features/wallet.feature:89`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A deposit with room succeeds and adds exactly the amount (`features/wallet.feature:104`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| A deposit that would overflow is rejected and changes nothing (`features/wallet.feature:118`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A transfer the sender can afford always succeeds (`features/wallet.feature:137`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6) |
| A deposit earns interest (`features/wallet.feature:156`) | **UNBOUND** | UNBOUND | - | - |
| Applying any batch of transfers conserves the total of all balances (`features/ledger.feature:18`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 6 / 6 of 6 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch stops only at a transfer that cannot be carried out (`features/ledger.feature:37`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (3 of 3) |
| Two batches applied one after the other conserve the total (`features/ledger.feature:52`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch whose first transfer is invalid changes nothing (`features/ledger.feature:66`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| The number of transfers applied is at most the length of the batch (`features/ledger.feature:80`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch of two valid transfers is applied in full (`features/ledger.feature:93`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch stops at its first invalid transfer and keeps what it has applied (`features/ledger.feature:101`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:115`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| A valid transfer is accepted and moves exactly its amount (`features/ledger.feature:129`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (6 of 6) |
| An invalid transfer is rejected and changes nothing (`features/ledger.feature:144`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (5 of 5) |
| The total is the sum of the balances when that fits (`features/ledger.feature:162`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of balances that do not fit is reported as absent (`features/ledger.feature:177`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of a ledger can always be computed (`features/ledger.feature:194`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| Looking up an existing account gives its balance (`features/ledger.feature:207`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| Looking up an account that does not exist gives nothing (`features/ledger.feature:219`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole that is rejected leaves the ledger unchanged (`features/ledger.feature:235`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 4 / 4 of 4 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch applied as a whole whose first transfer is invalid is rejected and changes nothing (`features/ledger.feature:248`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5) |
| Applying a batch as a whole conserves the total of all balances (`features/ledger.feature:260`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch of valid transfers applied as a whole is accepted and applied (`features/ledger.feature:272`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole is rolled back when its third transfer is invalid (`features/ledger.feature:281`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole is rolled back when a later transfer is invalid (`features/ledger.feature:289`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| The total computed after any batch is the total before it, when that total fits (`features/ledger.feature:302`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| The total computed after any batch is still absent when it did not fit before (`features/ledger.feature:317`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| A withdrawal that is both covered and not covered (`features/negative.feature:11`) | **VACUOUS** | VACUOUS | 0 / 0 of 1 | ROW OUTSIDE GIVENS; UNREVIEWED GLOSSARY (5 of 5) |
| A deposit does not touch a bystander (`features/negative.feature:25`) | **PROVED-FOR-ALL (1 of 2 Thens substantive)** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); TRIVIAL-THEN; FRAME-TRIVIAL |

Every scenario got the verdict it was expected to get.
A scenario tagged `@expect-refuted`, `@expect-unbound` or `@expect-vacuous` is a deliberate negative control.

**30 proved scenarios rest on glossary entries with no valid sign-off.** A proof shows the Lean statement holds; that the statement says what the English says is exactly what the sign-off is for. `./run.sh --strict` makes this a failure.

## Which inputs the scenarios apply to, and what they say about the outputs

A green scenario says nothing about inputs outside its Givens, and nothing about an output its Thens do not mention. Three views of what is left unsaid:

1. **Inputs for which some scenario applies.** For each operation, a generated theorem states that the Givens of its proved universal scenarios, taken together, hold of every input. If the kernel accepts it, no input falls outside every scenario. **This says nothing about what those scenarios promise.** A scenario with no Given beyond naming its values applies to every input whatever its Then says, so for such an operation the answer is trivially yes.
2. **What is said about each output.** The Thens of the proved universal scenarios, listed per output (the value the call returns; the state it hands back), each with the condition under which it is promised. This is a list for a person to read: nothing checks that the Thens determine the output, and for the loops here they do not (the ledger an `apply_batch` leaves is constrained only by its total and by where the batch stopped).
3. **Mutants.** A mutation run (`python3 mutation/run_mutants.py`, not part of `run.sh`) changes the Rust in small wrong ways and reports for which changes some scenario is shown false.

| Operation (Lean model) | Does some proved universal scenario apply to every input? | Said about the returned value | Said about the state afterwards | Scenarios |
|---|---|---|---|---|
| `wallet.Wallet.deposit` | **yes**: kernel-checked `Coverage.g2` over 2 proved scenarios | "the operation succeeds" (only when: Alice's balance plus <amount> does not exceed the maximum); "the operation is rejected with {error:e}" (only when: Alice's balance plus <amount> exceeds the maximum) | "{wallet:w}'s balance is increased by {amount:n}" (only when: Alice's balance plus <amount> does not exceed the maximum); "{wallet:w}'s balance is unchanged" (only when: Alice's balance plus <amount> exceeds the maximum) | deposit_with_room: PROVED-FOR-ALL; deposit_overflow: PROVED-FOR-ALL; bystander_unchanged: PROVED-FOR-ALL (1 of 2 Thens substantive) |
| `wallet.Wallet.withdraw` | **yes**: kernel-checked `Coverage.g1` over 2 proved scenarios | "the operation succeeds" (only when: <amount> is not more than Alice's balance); "the operation is rejected with {error:e}" (only when: <amount> is more than Alice's balance) | "{wallet:w}'s balance is decreased by {amount:n}" (only when: <amount> is not more than Alice's balance); "{wallet:w}'s balance is unchanged" (only when: <amount> is more than Alice's balance) | withdraw_covered: PROVED-FOR-ALL; withdraw_too_much: PROVED-FOR-ALL; contradictory_givens: VACUOUS |
| `wallet.transfer` | **yes**: kernel-checked `Coverage.g0` over 3 proved scenarios | "the operation succeeds" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "the operation is rejected with {error:e}" (only when: <amount> is more than Alice's balance); "the operation is rejected with {error:e}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> exceeds the maximum) | "{wallet:w}'s balance is decreased by {amount:n}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "{wallet:w}'s balance is increased by {amount:n}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "the total of all balances is unchanged" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "{wallet:w}'s balance is unchanged" (only when: <amount> is more than Alice's balance); "{wallet:w}'s balance is unchanged" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> exceeds the maximum) | transfer_conserves: PROVED-FOR-ALL; transfer_short: PROVED-FOR-ALL; transfer_no_room: PROVED-FOR-ALL; transfer_short_example: PROVED-INSTANCE; transfer_always_succeeds: REFUTED |
| `ledger.Ledger.balance` | **yes**: kernel-checked `Coverage.g7` over 2 proved scenarios | "the result is the balance of account {index:i} of ledger {ledger:l}" (only when: <i> is an account of ledger Main); "there is no result" (only when: <i> is not an account of ledger Main) | **nothing** | balance_of_account: PROVED-FOR-ALL; balance_no_account: PROVED-FOR-ALL |
| `ledger.Ledger.total_loop.body` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.total_loop` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.total` | **NOT SHOWN**: `Coverage.g5` (1 scenarios): their Givens do not cover every input; `Coverage.g6` (1 scenarios): their Givens do not cover every input | "the result is {amount:s}" (only when: the balances of ledger Main add up to <sum>); "there is no result" (only when: the balances of ledger Main add up to more than the maximum); "the result is {amount:s}" (only when: the balances of ledger Main add up to <sum>; after: the batch <batch> is applied to ledger Main); "there is no result" (only when: the balances of ledger Main add up to more than the maximum; after: the batch <batch> is applied to ledger Main) | **nothing** | total_is_sum: PROVED-FOR-ALL; total_overflow: PROVED-FOR-ALL; total_always_available: REFUTED; batch_then_total: PROVED-FOR-ALL; batch_then_total_overflow: PROVED-FOR-ALL |
| `ledger.Ledger.apply` | **yes**: kernel-checked `Coverage.g4` over 2 proved scenarios | "it is accepted" (only when: the transfer <t> is valid on ledger Main); "it is rejected" (only when: the transfer <t> is not valid on ledger Main) | "the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed" (only when: the transfer <t> is valid on ledger Main); "the total of ledger {ledger:l}'s balances is unchanged" (only when: the transfer <t> is valid on ledger Main); "ledger {ledger:l} is unchanged" (only when: the transfer <t> is not valid on ledger Main) | transfer_valid_moves: PROVED-FOR-ALL; transfer_invalid_rejected: PROVED-FOR-ALL |
| `ledger.Ledger.apply_batch_loop.body` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch_loop` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch` | **yes**: kernel-checked `Coverage.g3` over 4 proved scenarios | "the batch {batch:b} has stopped only at a transfer that is not valid on ledger {ledger:l} as it now stands" (always); "the number of transfers applied is at most the length of {batch:b}" (only when: after: the batch <first> is applied to ledger Main); "no transfer is applied" (only when: the first transfer of <batch> is not valid on ledger Main); "the number of transfers applied is at most the length of {batch:b}" (always) | "the total of ledger {ledger:l}'s balances is unchanged" (always); "the batch {batch:b} has stopped only at a transfer that is not valid on ledger {ledger:l} as it now stands" (always); "the total of ledger {ledger:l}'s balances is unchanged" (only when: after: the batch <first> is applied to ledger Main); "ledger {ledger:l} is unchanged" (only when: the first transfer of <batch> is not valid on ledger Main) | batch_conserves: PROVED-FOR-ALL; batch_stops_at_invalid: PROVED-FOR-ALL; two_batches_conserve: PROVED-FOR-ALL; batch_first_invalid: PROVED-FOR-ALL; batch_count_bounded: PROVED-FOR-ALL; batch_example_all: PROVED-INSTANCE; batch_example_stop: PROVED-INSTANCE; batch_all_valid_all_applied: REFUTED; batch_then_total: PROVED-FOR-ALL; batch_then_total_overflow: PROVED-FOR-ALL |
| `ledger.Ledger.apply_all` | **yes**: kernel-checked `Coverage.g8` over 3 proved scenarios | "if it is rejected, ledger {ledger:l} is unchanged" (always); "it is rejected" (only when: the first transfer of <batch> is not valid on ledger Main) | "if it is rejected, ledger {ledger:l} is unchanged" (always); "ledger {ledger:l} is unchanged" (only when: the first transfer of <batch> is not valid on ledger Main); "the total of ledger {ledger:l}'s balances is unchanged" (always) | whole_rejected_unchanged: PROVED-FOR-ALL; whole_first_invalid: PROVED-FOR-ALL; whole_conserves: PROVED-FOR-ALL; whole_example_accept: PROVED-INSTANCE; whole_example_rollback_late: PROVED-INSTANCE; whole_example_rollback: PROVED-INSTANCE |

Mutation run of 2026-11-10T08:24:26+00:00: 45 mutants of `wallet/src/lib.rs` and `ledger/src/lib.rs`. **A scenario is shown false of 43 of them** (an example row differs on the compiled Rust, or the search finds a counterexample). For 2 more (d6, la6) the run fails only because a hand-written proof or lemma stopped compiling, which is not detection by the scenarios. 0 make no difference to the run at all. These results are for the current Rust, features, glossary and proofs.

A lost proof means the proof (or a lemma it depends on) no longer compiles; it does not by itself mean the scenario's statement is false of the mutant. A new counterexample does.

| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | A scenario shown false | Run fails |
|---|---|---|---|---|---|---|---|---|---|
| d1 | `wallet::{wallet::Wallet}::deposit` | no overflow check: the balance wraps around | caught | caught (2 rows) | 2 | 1 | deposit_with_room: TESTED-ONLY; deposit_overflow: REFUTED | yes | yes |
| d2 | `wallet::{wallet::Wallet}::deposit` | a successful deposit sets the balance to the amount instead of adding it | caught | caught (2 rows) | 1 | 1 | deposit_with_room: REFUTED | yes | yes |
| d3 | `wallet::{wallet::Wallet}::deposit` | overflow is reported as insufficient funds | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes | yes |
| d4 | `wallet::{wallet::Wallet}::deposit` | a deposit that reaches exactly the maximum is rejected | MISSED | caught (2 rows) | 2 | 2 | deposit_with_room: REFUTED; bystander_unchanged: REFUTED | yes | yes |
| d5 | `wallet::{wallet::Wallet}::deposit` | a rejected deposit empties the wallet | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes | yes |
| d6 | `wallet::{wallet::Wallet}::deposit` | a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 1 | none | deposit_with_room: TESTED-ONLY | **NO** (lost proof only) | yes |
| w1 | `wallet::{wallet::Wallet}::withdraw` | withdrawing the whole balance is rejected (> became >=) | caught | caught (2 rows) | 1 | 1 | withdraw_covered: REFUTED | yes | yes |
| w2 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal does not take the money | caught | caught (2 rows) | 1 | 1 | withdraw_covered: REFUTED | yes | yes |
| w3 | `wallet::{wallet::Wallet}::withdraw` | insufficient funds is reported as overflow | caught | caught (2 rows) | 1 | 1 | withdraw_too_much: REFUTED | yes | yes |
| w4 | `wallet::{wallet::Wallet}::withdraw` | a rejected withdrawal empties the wallet | caught | caught (1 rows) | 1 | 1 | withdraw_too_much: REFUTED | yes | yes |
| w5 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal takes one unit too many when it can | MISSED | caught (1 rows) | 1 | 1 | withdraw_covered: REFUTED | yes | yes |
| t1 | `wallet::transfer` | transferring the whole balance is rejected (< became <=) | caught | caught (3 rows) | 2 | 2 | transfer_conserves: REFUTED; transfer_no_room: REFUTED | yes | yes |
| t2 | `wallet::transfer` | the sender is debited before the receiver's overflow check, so a rejected transfer loses money | caught | caught (2 rows) | 1 | 1 | transfer_no_room: REFUTED | yes | yes |
| t3 | `wallet::transfer` | the receiver is never credited (money vanishes) | caught | caught (4 rows) | 1 | 1 | transfer_conserves: REFUTED | yes | yes |
| t4 | `wallet::transfer` | the sender is never debited (money is created) | caught | caught (4 rows) | 1 | 1 | transfer_conserves: REFUTED | yes | yes |
| t5 | `wallet::transfer` | receiver overflow is reported as insufficient funds | caught | caught (2 rows) | 1 | 1 | transfer_no_room: REFUTED | yes | yes |
| t6 | `wallet::transfer` | insufficient funds is reported as overflow | caught | caught (3 rows) | 2 | 2 | transfer_short: REFUTED; transfer_short_example: REFUTED | yes | yes |
| t7 | `wallet::transfer` | no funds check at all (the subtraction panics instead) | caught | caught (3 rows) | 2 | 2 | transfer_short: COUNTEREXAMPLE; transfer_short_example: COUNTEREXAMPLE | yes | yes |
| lt1 | `ledger::{ledger::Ledger}::total` | LOOP off-by-one bound: the last balance is not added | caught | caught (9 rows) | 4 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| lt2 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: the sum is overwritten by each balance instead of accumulated | caught | caught (10 rows) | 4 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| lt3 | `ledger::{ledger::Ledger}::total` | LOOP skipped element: summing starts at account 1 | caught | caught (12 rows) | 4 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| lt4 | `ledger::{ledger::Ledger}::total` | an overflowing total is reported as u64::MAX instead of absent | caught | caught (5 rows) | 4 | 2 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| lt5 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: wrapping addition, so an overflowing total wraps around | caught | caught (5 rows) | 4 | 2 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| la1 | `ledger::{ledger::Ledger}::apply` | no check that sender and receiver differ: a self-transfer creates money | caught | caught (2 rows) | 17 | 7 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: REFUTED; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| la2 | `ledger::{ledger::Ledger}::apply` | transferring the sender's whole balance is rejected (< became <=) | caught | caught (6 rows) | 17 | 4 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: COUNTEREXAMPLE; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| la3 | `ledger::{ledger::Ledger}::apply` | the receiver is never credited (money vanishes) | caught | caught (14 rows) | 17 | 9 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| la4 | `ledger::{ledger::Ledger}::apply` | the sender is never debited (money is created) | caught | caught (13 rows) | 17 | 8 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| la5 | `ledger::{ledger::Ledger}::apply` | receiver bounds check off by one (>= became >): indexing one past the end panics | caught | caught (2 rows) | 17 | 11 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: COUNTEREXAMPLE; whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| la6 | `ledger::{ledger::Ledger}::apply` | a transfer of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 17 | none | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | **NO** (lost proof only) | yes |
| lb1 | `ledger::{ledger::Ledger}::apply_batch` | LOOP missing early exit: the batch carries on after a rejected transfer and counts it | caught | caught (7 rows) | 15 | 5 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lb2 | `ledger::{ledger::Ledger}::apply_batch` | LOOP off-by-one bound: the last transfer of the batch is never applied | caught | caught (6 rows) | 15 | 3 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lb3 | `ledger::{ledger::Ledger}::apply_batch` | LOOP skipped element: every second transfer is skipped (i += 2) | caught | caught (5 rows) | 15 | 6 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lb4 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong result: the batch length is returned instead of the number applied | caught | caught (7 rows) | 15 | 5 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lb5 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong counter: a rejected transfer is counted as applied | caught | caught (8 rows) | 15 | 6 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lb6 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong early exit: the batch stops after the first APPLIED transfer | caught | caught (6 rows) | 15 | 3 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: REFUTED; batch_example_stop: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| lw1 | `ledger::{ledger::Ledger}::apply_all` | no rollback: a rejected batch keeps the transfers applied before the failure | caught | caught (5 rows) | 6 | 3 | whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE | yes | yes |
| lw2 | `ledger::{ledger::Ledger}::apply_all` | a rolled-back batch is reported as applied | caught | caught (3 rows) | 6 | 3 | whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE | yes | yes |
| lw3 | `ledger::{ledger::Ledger}::apply_all` | every batch is rolled back and rejected (< became <=) | caught | caught (1 rows) | 6 | 1 | whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY | yes | yes |
| lg1 | `ledger::{ledger::Ledger}::balance` | lookup bounds check off by one (< became <=): looking up account `len` panics | caught | caught (2 rows) | 2 | 1 | balance_of_account: TESTED-ONLY; balance_no_account: COUNTEREXAMPLE | yes | yes |
| lg2 | `ledger::{ledger::Ledger}::balance` | lookup returns the balance of account 0 whatever the account | caught | caught (1 rows) | 2 | 1 | balance_of_account: REFUTED; balance_no_account: TESTED-ONLY | yes | yes |
| r1 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP cap: the batch silently stops after three transfers | MISSED | caught (1 rows) | 15 | 1 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| r2 | `ledger::{ledger::Ledger}::total` | REVIEW LOOP cap: only the first three accounts are summed | MISSED | caught (4 rows) | 4 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE | yes | yes |
| r3 | `ledger::{ledger::Ledger}::apply_all` | REVIEW atomicity: no rollback once two or more transfers have been applied | MISSED | caught (3 rows) | 6 | 2 | whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY | yes | yes |
| r4 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied | caught | caught (2 rows) | 15 | 2 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY | yes | yes |
| r5 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP state corruption: one unit is minted to account 0 at the start of the third iteration (conservation is false, but only for batches whose first two transfers apply and that have a third) | caught | caught (3 rows) | 15 | 4 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY | yes | yes |

## Suite adequacy note

**Informational. It changes no verdict and never fails a run.** A single proved scenario is not expected to pin behaviour: "a transfer never changes the total" is also true of code that rejects every transfer. The question here is about the suite. For each operation, trivial implementations are generated as Lean models of exactly the type of the Aeneas-generated model (`type_of%`), and each proved universal scenario is stated again with the trivial model in place of the call:

| Trivial implementation | What it does |
|---|---|
| reject-all | always answers with a rejecting value and leaves the state as it was |
| no-op | always answers with a success value and leaves the state as it was (does nothing but report success) |
| identity | answers as the code does, but never changes the state |
| constant | always answers the same value; the state is left as it was, or reset to a fixed one |

A scenario **rules out** a trivial implementation when the search finds an input on which the scenario is false of it (the same boundary grid as the counterexample search; a kernel-checked refutation at that input is attempted). A suite rules it out when one of its scenarios does, and **still allows** it otherwise. "Still allows" is proved for all inputs only where it says so; otherwise it means no scenario was shown false of it on the grid. Scenarios tagged `@control` and scenarios that are not proved are not counted. Which result values count as a rejection or a success is stated in `glossary.yaml` (`trivial`).

234 (scenario, trivial implementation) pairs were checked: the scenario is false of the trivial implementation for 169 (an input is given for each), proved to hold of it for all inputs for 32, and neither for 33 (no input found on the grid, no proof). 165 of the 234 results are kernel-checked; the rest rest on evaluation by the Lean interpreter (tested).

| Operation (Lean model) | Proved universal scenarios counted | The suite as a whole | Trivial implementations still allowed |
|---|---|---|---|
| `wallet.Wallet.deposit` | 2 | rules out: reject-all, no-op, identity, constant; still allows: (none found) | none found |
| `wallet.Wallet.withdraw` | 2 | rules out: reject-all, no-op, identity, constant; still allows: (none found) | none found |
| `wallet.transfer` | 3 (and 1 literal example, counted separately) | rules out: reject-all, no-op, identity, constant; still allows: (none found) | none found |
| `ledger.Ledger.balance` | 2 | rules out: reject-all, no-op; still allows: (none found) | none found |
| `ledger.Ledger.total` | 4 | rules out: reject-all, no-op; still allows: (none found) | none found |
| `ledger.Ledger.apply` | 2 | rules out: reject-all, no-op, identity, constant; still allows: (none found) | none found |
| `ledger.Ledger.apply_batch` | 7 (and 2 literal examples, counted separately) | rules out: reject-all, no-op, identity, constant; still allows: (none found) | none found |
| `ledger.Ledger.apply_all` | 3 (and 3 literal examples, counted separately) | rules out: no-op, constant; still allows: reject-all: always answers `false` and leaves the state as it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid]<br>of those still allowed, 2 are ruled out only by a literal example, for its one input: "A batch of valid transfers applied as a whole is accepted and applied" | reject-all: always answers `false` and leaves the state as it was (proved to satisfy every scenario counted) (ruled out by a literal example only)<br>identity: answers as the code does, but never changes the state (ruled out by a literal example only) |

The per-rule line ("suite rules out ...; still allows ...") is in each rule's block below. Where a rule or a single scenario would on its own also be true of a trivial implementation that the wider suite rules out, the block says so; that is the normal case and not a defect of the rule.

## Rules and their scenarios

One block per `Rule:` (and one per feature for scenarios that sit under no rule), generated from `out/graph.json`: the rule text as written, the verdict of its scenarios, the example rows, the suite note, and what the result rests on. A compiled reading of the rule line is not printed (the rule line is not compiled); the generated Lean statement of each scenario is printed beneath its block.

### Rule: A transfer never changes the total of all balances

```text
Rule: A transfer never changes the total of all balances   [features/wallet.feature:10]
  Every transfer falls under one of three cases. Covered, and the receiver has room: it must
  succeed and move exactly the amount (the progress scenario). The sender is short, or the
  receiver has no room: it is rejected and neither balance moves.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 1 of 1 literal examples proved for their own values
            PROVED-FOR-ALL  A covered transfer moves the money and conserves the total
            PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing
            PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing
            PROVED-INSTANCE Transferring more than you have is rejected and changes nothing
  Examples  7 of 7 pass on the compiled Rust; 7 of 7 pass on the Lean model
  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "Transferring more than the sender has is rejected and changes nothing" would also hold of:
              reject-all, identity; ruled out here by "A covered transfer moves the money and conserves the total"; "A
              transfer the receiver has no room for is rejected and changes nothing"
            alone, "A transfer the receiver has no room for is rejected and changes nothing" would also hold of:
              reject-all, identity; ruled out here by "A covered transfer moves the money and conserves the total";
              "Transferring more than the sender has is rejected and changes nothing"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      12 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (G-balance, G-covers, G-room, W-transfer, T-ok, T-dec, T-inc, T-total, G-exceeds, T-err, T-same,
                 G-noroom)
    proof        checked by Lean's kernel: 3 theorems for all inputs, 1 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.wallet.transfer_conserves, Spec.wallet.transfer_short, Spec.wallet.transfer_no_room,
                 Spec.wallet.transfer_short_example)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 7 example rows: 7 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A covered transfer moves the money and conserves the total

`features/wallet.feature:16`  id `Spec.wallet.transfer_conserves`  tags `@id:transfer_conserves`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

#### PROVED-FOR-ALL: Transferring more than the sender has is rejected and changes nothing

`features/wallet.feature:33`  id `Spec.wallet.transfer_short`  tags `@id:transfer_short`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

#### PROVED-FOR-ALL: A transfer the receiver has no room for is rejected and changes nothing

`features/wallet.feature:48`  id `Spec.wallet.transfer_no_room`  tags `@id:transfer_no_room`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

#### PROVED-INSTANCE: Transferring more than you have is rejected and changes nothing

`features/wallet.feature:64`  id `Spec.wallet.transfer_short_example`  tags `@id:transfer_short_example`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### Rule: A withdrawal takes exactly the amount, or is rejected and takes nothing

```text
Rule: A withdrawal takes exactly the amount, or is rejected and takes nothing   [features/wallet.feature:72]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount
            PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "Withdrawing more than the balance is rejected and changes nothing" would also hold of: reject-all,
              identity; ruled out here by "A covered withdrawal succeeds and takes exactly the amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      8 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (G-balance, G-covers, W-withdraw, T-ok, T-dec, G-exceeds, T-err, T-same)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.wallet.withdraw_covered, Spec.wallet.withdraw_too_much)
    translation  Lean model wallet.Wallet.withdraw generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 5 example rows: 5 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A covered withdrawal succeeds and takes exactly the amount

`features/wallet.feature:75`  id `Spec.wallet.withdraw_covered`  tags `@id:withdraw_covered`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

#### PROVED-FOR-ALL: Withdrawing more than the balance is rejected and changes nothing

`features/wallet.feature:89`  id `Spec.wallet.withdraw_too_much`  tags `@id:withdraw_too_much`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### Rule: A deposit adds exactly the amount, or is rejected and adds nothing

```text
Rule: A deposit adds exactly the amount, or is rejected and adds nothing   [features/wallet.feature:101]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount
            PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "A deposit that would overflow is rejected and changes nothing" would also hold of: reject-all,
              identity; ruled out here by "A deposit with room succeeds and adds exactly the amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      8 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (G-balance, G-room, W-deposit, T-ok, T-inc, G-noroom, T-err, T-same)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.wallet.deposit_with_room, Spec.wallet.deposit_overflow)
    translation  Lean model wallet.Wallet.deposit generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 5 example rows: 5 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A deposit with room succeeds and adds exactly the amount

`features/wallet.feature:104`  id `Spec.wallet.deposit_with_room`  tags `@id:deposit_with_room`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

#### PROVED-FOR-ALL: A deposit that would overflow is rejected and changes nothing

`features/wallet.feature:118`  id `Spec.wallet.deposit_overflow`  tags `@id:deposit_overflow`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### Rule: A transfer the sender can afford always succeeds

```text
Rule: A transfer the sender can afford always succeeds   [features/wallet.feature:131]   tags @expect-refuted
  Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A transfer the sender can afford always succeeds   (expected REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      6 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (G-balance, G-covers, W-transfer, T-ok, T-dec, T-total)
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.wallet.transfer_always_succeeds.refuted)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows: 2 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### REFUTED: A transfer the sender can afford always succeeds

`features/wallet.feature:137`  id `Spec.wallet.transfer_always_succeeds`  tags `@expect-refuted @id:transfer_always_succeeds`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-transfer, T-ok, T-dec, T-total
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1587 of 1587 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 216 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### Rule: A deposit earns interest

```text
Rule: A deposit earns interest   [features/wallet.feature:151]
  Not a claim about this wallet: its scenario uses a phrase the glossary does not define.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   NO SCENARIO PROVED: 0 of 1 literal examples proved for their own values
            UNBOUND         A deposit earns interest   (expected UNBOUND)
  Examples  none could be evaluated
  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      no vocabulary entry is bound (no statement was generated)
    proof        no kernel-checked theorem for: deposit_earns_interest
    translation  no model function is involved (no statement was generated)
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### UNBOUND: A deposit earns interest

`features/wallet.feature:156`  id `Spec.wallet.deposit_earns_interest`  tags `@id:deposit_earns_interest @expect-unbound`

```gherkin
Scenario: A deposit earns interest
  Given Alice has a balance of 100
  When Alice deposits 5
  Then Alice earns interest on her balance
```

```text
UNBOUND  A deposit earns interest
  features/wallet.feature:159: no glossary `then` phrase matches: "Alice earns interest on her balance"
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

### Rule: Applying a batch of transfers never changes the total of all balances

```text
Rule: Applying a batch of transfers never changes the total of all balances   [features/ledger.feature:11]
  The first scenario is the safety half: it holds whatever the ledger and whatever the batch,
  and it would also hold of a batch function that does nothing. The second is the progress
  half: the batch goes on for as long as it can.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances
            PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out
            PROVED-FOR-ALL  Two batches applied one after the other conserve the total
  Examples  12 of 12 pass on the compiled Rust; 12 of 12 pass on the Lean model
  Suite     suite rules out: reject-all, identity, constant; still allows: no-op: reports every transfer of the batch as
              applied and leaves the state as it was [no scenario counted is false of it on the search grid]
            taken alone, this group would also hold of: no-op (1 variant); the whole suite for
              `ledger.Ledger.apply_batch` rules it out through Rule "A batch reports how many transfers it applied, and
              applies none when the first is invalid"
            alone, "Applying any batch of transfers conserves the total of all balances" would also hold of: reject-all,
              identity, constant; ruled out here by "A batch stops only at a transfer that cannot be carried out"; "Two
              batches applied one after the other conserve the total"
            alone, "A batch stops only at a transfer that cannot be carried out" would also hold of: constant; ruled out
              here by "Two batches applied one after the other conserve the total"; "Applying any batch of transfers
              conserves the total of all balances"
            alone, "Two batches applied one after the other conserve the total" would also hold of: reject-all,
              identity; ruled out here by "A batch stops only at a transfer that cannot be carried out"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      5 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LW-batch, LT-total-same, LT-stops-at-invalid, LT-at-most)
    proof        checked by Lean's kernel: 3 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_conserves, Spec.ledger.batch_stops_at_invalid, Spec.ledger.two_batches_conserve)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 12 example rows: 12 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: Applying any batch of transfers conserves the total of all balances

`features/ledger.feature:18`  id `Spec.ledger.batch_conserves`  tags `@id:batch_conserves`

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
    | [100, 20, 0]    | [0->1:30, 1->2:50, 2->0:5]  |
    | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:1] |
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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           6 of 6 rows pass on compiled Rust (cucumber-rs); 6 of 6 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_conserves.lean`):

```lean
theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h1⟩
```

#### PROVED-FOR-ALL: A batch stops only at a transfer that cannot be carried out

`features/ledger.feature:37`  id `Spec.ledger.batch_stops_at_invalid`  tags `@id:batch_stops_at_invalid`

```gherkin
Scenario Outline: A batch stops only at a transfer that cannot be carried out
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main
  Then the batch <batch> has stopped only at a transfer that is not valid on ledger Main as it now stands

  Examples:
    | balances        | batch                              |
    | [100, 20, 0]    | [0->1:30, 1->2:50]                 |
    | [100, 20, 0]    | [0->1:30, 2->1:5, 0->1:1]          |
    | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:1]   |
    | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:5]   |
    | [5, 5]          | [0->1:6, 1->0:1]                   |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_stops_at_invalid.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.stopsAtInvalid outcome batch main'
```

```text
PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid : Spec.ledger.batch_stops_at_invalid.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_stops_at_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_stops_at_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-stops-at-invalid
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1606 of 1606 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_stops_at_invalid.lean`):

```lean
theorem Spec.ledger.batch_stops_at_invalid : Spec.ledger.batch_stops_at_invalid.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, ledger.Ledger.apply_batch.stops hx⟩
```

#### PROVED-FOR-ALL: Two batches applied one after the other conserve the total

`features/ledger.feature:52`  id `Spec.ledger.two_batches_conserve`  tags `@id:two_batches_conserve`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 377 of 377 grid points
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

### Rule: A batch reports how many transfers it applied, and applies none when the first is invalid

```text
Rule: A batch reports how many transfers it applied, and applies none when the first is invalid   [features/ledger.feature:63]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs; 2 of 2 literal examples proved for their own values
            PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing
            PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch
            PROVED-INSTANCE A batch of two valid transfers is applied in full
            PROVED-INSTANCE A batch stops at its first invalid transfer and keeps what it has applied
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Suite     suite rules out: no-op, constant; still allows: reject-all: always answers `0` and leaves the state as it
              was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the
              state [no scenario counted is false of it on the search grid]
            taken alone, this group would also hold of: reject-all, identity (2 variants); the whole suite for
              `ledger.Ledger.apply_batch` rules them out through Rule "Applying a batch of transfers never changes the
              total of all balances"
            alone, "The number of transfers applied is at most the length of the batch" would also hold of: no-op,
              constant; ruled out here by "A batch whose first transfer is invalid changes nothing"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      8 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same, LT-at-most, LT-exactly,
                 LT-now-holds)
    proof        checked by Lean's kernel: 2 theorems for all inputs, 2 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_first_invalid, Spec.ledger.batch_count_bounded, Spec.ledger.batch_example_all,
                 Spec.ledger.batch_example_stop)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows: 8 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A batch whose first transfer is invalid changes nothing

`features/ledger.feature:66`  id `Spec.ledger.batch_first_invalid`  tags `@id:batch_first_invalid`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 544 of 544 grid points
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

#### PROVED-FOR-ALL: The number of transfers applied is at most the length of the batch

`features/ledger.feature:80`  id `Spec.ledger.batch_count_bounded`  tags `@id:batch_count_bounded`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 256 of 256 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_count_bounded.lean`):

```lean
theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, -, h2, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h2⟩
```

#### PROVED-INSTANCE: A batch of two valid transfers is applied in full

`features/ledger.feature:93`  id `Spec.ledger.batch_example_all`  tags `@id:batch_example_all`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
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

#### PROVED-INSTANCE: A batch stops at its first invalid transfer and keeps what it has applied

`features/ledger.feature:101`  id `Spec.ledger.batch_example_stop`  tags `@id:batch_example_stop`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
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

### Rule: A batch of transfers that are each valid on the starting ledger is applied in full

```text
Rule: A batch of transfers that are each valid on the starting ledger is applied in full   [features/ledger.feature:108]   tags @expect-refuted
  Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A batch of transfers that are each valid on the starting ledger is applied in full   (expected REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      4 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-all-valid, LW-batch, LT-all-applied)
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_all_valid_all_applied.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows: 2 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### REFUTED: A batch of transfers that are each valid on the starting ledger is applied in full

`features/ledger.feature:115`  id `Spec.ledger.batch_all_valid_all_applied`  tags `@expect-refuted @id:batch_all_valid_all_applied`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-all-valid, LW-batch, LT-all-applied
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 553 of 553 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### Rule: A single transfer moves exactly its amount, or is rejected and changes nothing

```text
Rule: A single transfer moves exactly its amount, or is rejected and changes nothing   [features/ledger.feature:126]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount
            PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "An invalid transfer is rejected and changes nothing" would also hold of: reject-all, identity; ruled
              out here by "A valid transfer is accepted and moves exactly its amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      9 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same, LG-invalid, LT-rejected,
                 LT-same)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.transfer_valid_moves, Spec.ledger.transfer_invalid_rejected)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows: 8 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A valid transfer is accepted and moves exactly its amount

`features/ledger.feature:129`  id `Spec.ledger.transfer_valid_moves`  tags `@id:transfer_valid_moves`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1036 of 1036 grid points
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

#### PROVED-FOR-ALL: An invalid transfer is rejected and changes nothing

`features/ledger.feature:144`  id `Spec.ledger.transfer_invalid_rejected`  tags `@id:transfer_invalid_rejected`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-invalid, LW-transfer, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 310 of 310 grid points
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

### Rule: The total of a ledger is the sum of its balances, or absent when the sum does not fit

```text
Rule: The total of a ledger is the sum of its balances, or absent when the sum does not fit   [features/ledger.feature:159]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total is the sum of the balances when that fits
            PROVED-FOR-ALL  The total of balances that do not fit is reported as absent
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Suite     suite rules out: reject-all, no-op; still allows: (none found)
            alone, "The total of balances that do not fit is reported as absent" would also hold of: reject-all; ruled
              out here by "The total is the sum of the balances when that fits"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      6 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-sums-to, LW-total, LT-result, LG-sum-too-big, LT-no-result)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.total_is_sum, Spec.ledger.total_overflow)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows: 8 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: The total is the sum of the balances when that fits

`features/ledger.feature:162`  id `Spec.ledger.total_is_sum`  tags `@id:total_is_sum`

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
    | [1, 2, 3, 4]                | 10                   |
    | [1, 2, 3, 4, 5]             | 15                   |
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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 217 of 217 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
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

#### PROVED-FOR-ALL: The total of balances that do not fit is reported as absent

`features/ledger.feature:177`  id `Spec.ledger.total_overflow`  tags `@id:total_overflow`

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
    | [18446744073709551615, 0, 0, 1]                |
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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 137 of 137 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/total_overflow.lean`):

```lean
theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt := by
  intro balances main _ hbig
  obtain ⟨o, e, -, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  exact ⟨o, e, h2 hbig⟩
```

### Rule: The total of a ledger can always be computed

```text
Rule: The total of a ledger can always be computed   [features/ledger.feature:189]
  Deliberately false; here the tag is on the scenario.
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         The total of a ledger can always be computed   (expected REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      3 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LW-total, LT-some-result)
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.total_always_available.refuted)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows: 2 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### REFUTED: The total of a ledger can always be computed

`features/ledger.feature:194`  id `Spec.ledger.total_always_available`  tags `@id:total_always_available @expect-refuted`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-total, LT-some-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 126 of 126 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 11 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### Rule: Looking up an account gives its balance, or nothing when there is no such account

```text
Rule: Looking up an account gives its balance, or nothing when there is no such account   [features/ledger.feature:204]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Looking up an existing account gives its balance
            PROVED-FOR-ALL  Looking up an account that does not exist gives nothing
  Examples  4 of 4 pass on the compiled Rust; 4 of 4 pass on the Lean model
  Suite     suite rules out: reject-all, no-op; still allows: (none found)
            alone, "Looking up an account that does not exist gives nothing" would also hold of: reject-all; ruled out
              here by "Looking up an existing account gives its balance"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      6 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-account, LW-balance, LT-balance, LG-no-account, LT-no-result)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.balance_of_account, Spec.ledger.balance_no_account)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4 example rows: 4 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: Looking up an existing account gives its balance

`features/ledger.feature:207`  id `Spec.ledger.balance_of_account`  tags `@id:balance_of_account`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-account, LW-balance, LT-balance
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 451 of 451 grid points
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

#### PROVED-FOR-ALL: Looking up an account that does not exist gives nothing

`features/ledger.feature:219`  id `Spec.ledger.balance_no_account`  tags `@id:balance_no_account`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-no-account, LW-balance, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 181 of 181 grid points
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

### Rule: A batch applied as a whole is applied completely or not at all

```text
Rule: A batch applied as a whole is applied completely or not at all   [features/ledger.feature:230]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 3 of 3 literal examples proved for their own values
            PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged
            PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
            PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances
            PROVED-INSTANCE A batch of valid transfers applied as a whole is accepted and applied
            PROVED-INSTANCE A batch applied as a whole is rolled back when its third transfer is invalid
            PROVED-INSTANCE A batch applied as a whole is rolled back when a later transfer is invalid
  Examples  10 of 10 pass on the compiled Rust; 10 of 10 pass on the Lean model
  Suite     suite rules out: no-op, constant; still allows: reject-all: always answers `false` and leaves the state as
              it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes
              the state [no scenario counted is false of it on the search grid]
            alone, "A batch applied as a whole that is rejected leaves the ledger unchanged" would also hold of: no-op,
              constant; ruled out here by "A batch applied as a whole whose first transfer is invalid is rejected and
              changes nothing"; "Applying a batch as a whole conserves the total of all balances"
            alone, "Applying a batch as a whole conserves the total of all balances" would also hold of: no-op; ruled
              out here by "A batch applied as a whole whose first transfer is invalid is rejected and changes nothing"
            no proved universal scenario of any rule rules out the 2 still allowed; the literal example "A batch of
              valid transfers applied as a whole is accepted and applied" rules out all of them, for one input each
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      9 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LW-whole, LT-same-if-rejected, LG-first-invalid, LT-rejected, LT-same, LT-total-same,
                 LT-accepted, LT-now-holds)
    proof        checked by Lean's kernel: 3 theorems for all inputs, 3 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.whole_rejected_unchanged, Spec.ledger.whole_first_invalid, Spec.ledger.whole_conserves,
                 Spec.ledger.whole_example_accept, Spec.ledger.whole_example_rollback_late,
                 Spec.ledger.whole_example_rollback)
    translation  Lean model ledger.Ledger.apply_all generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 10 example rows: 10 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: A batch applied as a whole that is rejected leaves the ledger unchanged

`features/ledger.feature:235`  id `Spec.ledger.whole_rejected_unchanged`  tags `@id:whole_rejected_unchanged`

```gherkin
Scenario Outline: A batch applied as a whole that is rejected leaves the ledger unchanged
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main as a whole
  Then if it is rejected, ledger Main is unchanged

  Examples:
    | balances        | batch                              |
    | [100, 20, 0]    | [0->1:30, 2->1:5]                  |
    | [100, 20, 0]    | [0->1:30, 1->2:50, 2->0:60]        |
    | [9, 0, 0, 0]    | [0->1:4, 1->2:3, 2->3:2, 3->0:5]   |
    | [100, 20, 0]    | [0->1:30, 1->2:50]                 |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_rejected_unchanged.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main batch = ok (outcome, main') ∧
      LVocab.unchangedIfRejected outcome main main'
```

```text
PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_rejected_unchanged.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_rejected_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-same-if-rejected
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 363 of 363 grid points
  tested           4 of 4 rows pass on compiled Rust (cucumber-rs); 4 of 4 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_rejected_unchanged.lean`):

```lean
theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, -, hback, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, fun hb => congrArg (·.balances.val) (hback hb)⟩
```

#### PROVED-FOR-ALL: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing

`features/ledger.feature:248`  id `Spec.ledger.whole_first_invalid`  tags `@id:whole_first_invalid`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-whole, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 541 of 541 grid points
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

#### PROVED-FOR-ALL: Applying a batch as a whole conserves the total of all balances

`features/ledger.feature:260`  id `Spec.ledger.whole_conserves`  tags `@id:whole_conserves`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_conserves.lean`):

```lean
theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, h1⟩
```

#### PROVED-INSTANCE: A batch of valid transfers applied as a whole is accepted and applied

`features/ledger.feature:272`  id `Spec.ledger.whole_example_accept`  tags `@id:whole_example_accept`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-accepted, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
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

#### PROVED-INSTANCE: A batch applied as a whole is rolled back when its third transfer is invalid

`features/ledger.feature:281`  id `Spec.ledger.whole_example_rollback_late`  tags `@id:whole_example_rollback_late`

```gherkin
Scenario: A batch applied as a whole is rolled back when its third transfer is invalid
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50, 2->0:60] is applied to ledger Main as a whole
  Then it is rejected
  And ledger Main now holds the balances [100, 20, 0]
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_rollback_late.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64, ledger.Transfer.mk 2#usize 0#usize 60#u64]) = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.nowHolds main' ([100#u64, 20#u64, 0#u64])
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when its third transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late : Spec.ledger.whole_example_rollback_late.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback_late.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback_late.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/whole_example_rollback_late.lean`):

```lean
theorem Spec.ledger.whole_example_rollback_late : Spec.ledger.whole_example_rollback_late.stmt := by
  intro main h
  -- literal values: the pure model `runN` applies 2 of the 3 transfers, so the batch is rejected
  obtain ⟨⟨b, l'⟩, e, -, hback, -, hx, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main _)
  refine ⟨b, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx
  obtain rfl := hback hx
  exact ⟨hx, h⟩
```

#### PROVED-INSTANCE: A batch applied as a whole is rolled back when a later transfer is invalid

`features/ledger.feature:289`  id `Spec.ledger.whole_example_rollback`  tags `@id:whole_example_rollback`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
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

### Rule: Applying a batch does not change the total that is computed afterwards

```text
Rule: Applying a batch does not change the total that is computed afterwards   [features/ledger.feature:295]
  (the rule line and the text under it are carried as written; they are not compiled. What is proved is each scenario below.)
  Verdict   SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits
            PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Suite     [ledger.Ledger.apply_batch] suite rules out: (nothing); still allows: reject-all: always answers `0` and
              leaves the state as it was [no scenario counted is false of it on the search grid]; no-op: reports every
              transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the
              search grid]; identity: answers as the code does, but never changes the state [no scenario counted is
              false of it on the search grid]; constant (4 of 9 variants): always answers `1` and leaves the state as it
              was; always answers `2` and leaves the state as it was; and 2 more [no scenario counted is false of it on
              the search grid]
            [ledger.Ledger.apply_batch] taken alone, this group would also hold of: reject-all, no-op, identity,
              constant (7 variants); the whole suite for `ledger.Ledger.apply_batch` rules them out through Rule
              "Applying a batch of transfers never changes the total of all balances"; Rule "A batch reports how many
              transfers it applied, and applies none when the first is invalid"
            [ledger.Ledger.total] suite rules out: reject-all, no-op; still allows: (none found)
            [ledger.Ledger.total] alone, "The total computed after any batch is still absent when it did not fit before"
              would also hold of: reject-all; ruled out here by "The total computed after any batch is the total before
              it, when that total fits"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      7 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (LG-holds, LG-sums-to, LW-batch, LW-total, LT-result, LG-sum-too-big, LT-no-result)
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_then_total, Spec.ledger.batch_then_total_overflow)
    translation  Lean models ledger.Ledger.apply_batch, ledger.Ledger.total generated from ledger/src/lib.rs by
                 charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 cross-checked on 5 example rows: 5 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### PROVED-FOR-ALL: The total computed after any batch is the total before it, when that total fits

`features/ledger.feature:302`  id `Spec.ledger.batch_then_total`  tags `@id:batch_then_total`

```gherkin
Scenario Outline: The total computed after any batch is the total before it, when that total fits
  Given ledger Main holds the balances <balances>
  And the balances of ledger Main add up to <sum>
  When the batch <batch> is applied to ledger Main
  And the total of ledger Main is computed
  Then the result is <sum>

  Examples:
    | balances        | sum | batch                    |
    | [100, 20, 0]    | 120 | [0->1:30, 1->2:50]       |
    | [5, 5]          | 10  | [0->1:6]                 |
    | [1, 2, 3, 4]    | 10  | [3->0:4, 2->0:3, 1->0:2] |
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
PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits
  kernel-checked   theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt (type checked by the audit; 10-line proof, lean/Wallet/Proofs/ledger/batch_then_total.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-batch, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 217 of 217 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
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

#### PROVED-FOR-ALL: The total computed after any batch is still absent when it did not fit before

`features/ledger.feature:317`  id `Spec.ledger.batch_then_total_overflow`  tags `@id:batch_then_total_overflow`

```gherkin
Scenario Outline: The total computed after any batch is still absent when it did not fit before
  Given ledger Main holds the balances <balances>
  And the balances of ledger Main add up to more than the maximum
  When the batch <batch> is applied to ledger Main
  And the total of ledger Main is computed
  Then there is no result

  Examples:
    | balances                          | batch                |
    | [18446744073709551615, 1]         | [0->1:5]             |
    | [18446744073709551615, 0, 0, 1]   | [0->1:5, 0->2:7]     |
```

Generated Lean statement (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_then_total_overflow.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumTooBig main →
    ∃ (outcome_1 : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome_1, main') ∧
    ∃ (outcome : Option U64),
      ledger.Ledger.total main' = ok (outcome) ∧
      LVocab.noResult outcome
```

```text
PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow : Spec.ledger.batch_then_total_overflow.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_then_total_overflow.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-batch, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 137 of 137 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
```

Proof (`lean/Wallet/Proofs/ledger/batch_then_total_overflow.lean`):

```lean
theorem Spec.ledger.batch_then_total_overflow : Spec.ledger.batch_then_total_overflow.stmt := by
  intro balances batch main _ hbig
  -- first When: the batch loop conserves the total, so it is still too big
  obtain ⟨⟨n, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  refine ⟨n, l1, e1, ?_⟩
  -- second When: the summing loop reports a total that does not fit as absent
  obtain ⟨o, e2, -, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec l1)
  exact ⟨o, e2, h2 (by rw [h1]; exact hbig)⟩
```

### (scenarios of `Feature: Negative controls` that are not under a Rule)

```text
(scenarios of `Feature: Negative controls` that are not under a Rule)   [features/negative.feature]   tags @control
  Verdict   SOME SCENARIOS PROVED: 1 of 2 universal scenarios proved for all inputs
            VACUOUS         A withdrawal that is both covered and not covered   (expected VACUOUS)
            PROVED-FOR-ALL  A deposit does not touch a bystander
  Examples  1 of 2 pass on the compiled Rust; 1 of 2 pass on the Lean model
  Suite     not assessed: its scenarios are tagged @control

  Rests on
    meaning      8 vocabulary entries, 0 signed   [NOT ASSERTED by anyone]
                 (G-balance, G-exceeds, G-covers, W-withdraw, T-ok, G-room, W-deposit, T-same)
    proof        checked by Lean's kernel: 1 theorem for all inputs, 1 proof that the Givens contradict each other
                 (the scenario is true of nothing); axioms: propext, Classical.choice, Quot.sound (the standard three
                 only)   [kernel-checked]
                 (Spec.negative_controls.bystander_unchanged, Spec.negative_controls.contradictory_givens.unsat)
    translation  Lean models wallet.Wallet.withdraw, wallet.Wallet.deposit generated from wallet/src/lib.rs by charon
                 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 cross-checked on 2 example rows: 2 give the same result on the compiled Rust and on the model
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]
```

#### VACUOUS: A withdrawal that is both covered and not covered

`features/negative.feature:11`  id `Spec.negative_controls.contradictory_givens`  tags `@control @id:contradictory_givens @expect-vacuous`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, G-covers, W-withdraw, T-ok
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 111 of 111 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
```

#### PROVED-FOR-ALL (1 of 2 Thens substantive): A deposit does not touch a bystander

`features/negative.feature:25`  id `Spec.negative_controls.bystander_unchanged`  tags `@control @id:bystander_unchanged`

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
  tool-trusted     statement generated by slicegen 9b7dcdf4ec25 (slicegen-rule/3); printed for comparison with the scenario; constants it uses match the glossary: yes
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
| LG-holds | given | ledger {ledger:l} holds the balances {balances:bs} | `LVocab.holds` applied to `pre(l), bs` | `(l : Ledger) (bs : List U64) : Prop := l.balances.val = bs` | UNREVIEWED | yes | agree on 121 of 121 |
| LG-sums-to | given | the balances of ledger {ledger:l} add up to {amount:s} | `LVocab.sumsTo` applied to `pre(l), s` | `(l : Ledger) (s : U64) : Prop := total l = s.val` | UNREVIEWED | yes | agree on 66 of 66 |
| LG-sum-too-big | given | the balances of ledger {ledger:l} add up to more than the maximum | `LVocab.sumTooBig` applied to `pre(l)` | `(l : Ledger) : Prop := U64.max < total l` | UNREVIEWED | yes | agree on 11 of 11 |
| LG-account | given | {index:i} is an account of ledger {ledger:l} | `LVocab.isAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | UNREVIEWED | yes | agree on 55 of 55 |
| LG-no-account | given | {index:i} is not an account of ledger {ledger:l} | `LVocab.notAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := l.balances.val.length ≤ i.val` | UNREVIEWED | yes | agree on 55 of 55 |
| LG-valid | given | the transfer {transfer:t} is valid on ledger {ledger:l} | `LVocab.validOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := valid l t` | UNREVIEWED | yes | agree on 66 of 66 |
| LG-invalid | given | the transfer {transfer:t} is not valid on ledger {ledger:l} | `LVocab.invalidOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := ¬ valid l t` | UNREVIEWED | yes | agree on 66 of 66 |
| LG-first-invalid | given | the first transfer of {batch:b} is not valid on ledger {ledger:l} | `LVocab.firstInvalid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := b.val ≠ [] ∧ ∀ t ∈ b.val.head?, ¬ valid l t` | UNREVIEWED | yes | agree on 297 of 297 |
| LG-all-valid | given | every transfer of {batch:b} is valid on ledger {ledger:l} | `LVocab.allValid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := ∀ t ∈ b.val, valid l t` | UNREVIEWED | yes | agree on 297 of 297 |
| LW-batch | when | the batch {batch:b} is applied to ledger {ledger:l} | `ledger.Ledger.apply_batch` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_batch`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-whole | when | the batch {batch:b} is applied to ledger {ledger:l} as a whole | `ledger.Ledger.apply_all` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_all`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-transfer | when | the transfer {transfer:t} is applied to ledger {ledger:l} | `ledger.Ledger.apply` applied to `pre(l), t` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-total | when | the total of ledger {ledger:l} is computed | `ledger.Ledger.total` applied to `pre(l)` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::total`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-balance | when | the balance of account {index:i} of ledger {ledger:l} is looked up | `ledger.Ledger.balance` applied to `pre(l), i` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::balance`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LT-total-same | then | the total of ledger {ledger:l}'s balances is unchanged | `LVocab.totalUnchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := total post = total pre` | UNREVIEWED | yes | agree on 121 of 121 |
| LT-same | then | ledger {ledger:l} is unchanged | `LVocab.unchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := post.balances.val = pre.balances.val` | UNREVIEWED | yes | agree on 121 of 121 |
| LT-now-holds | then | ledger {ledger:l} now holds the balances {balances:bs} | `LVocab.nowHolds` applied to `post(l), bs` | `(post : Ledger) (bs : List U64) : Prop := post.balances.val = bs` | UNREVIEWED | yes | agree on 121 of 121 |
| LT-at-most | then | the number of transfers applied is at most the length of {batch:b} | `LVocab.appliedAtMost` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val ≤ b.val.length` | UNREVIEWED | yes | agree on 135 of 135 |
| LT-none-applied | then | no transfer is applied | `LVocab.appliedNone` applied to `outcome` | `(n : Usize) : Prop := n.val = 0` | UNREVIEWED | yes | agree on 5 of 5 |
| LT-all-applied | then | every transfer of {batch:b} is applied | `LVocab.appliedAll` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val = b.val.length` | UNREVIEWED | yes | agree on 135 of 135 |
| LT-exactly | then | exactly {index:k} transfers are applied | `LVocab.appliedExactly` applied to `outcome, k` | `(n : Usize) (k : Usize) : Prop := n = k` | UNREVIEWED | yes | agree on 25 of 25 |
| LT-stops-at-invalid | then | the batch {batch:b} has stopped only at a transfer that is not valid on ledger {ledger:l} as it now stands | `LVocab.stopsAtInvalid` applied to `outcome, b, post(l)` | `(n : Usize) (b : Slice Transfer) (post : Ledger) : Prop := ∀ t ∈ b.val[n.val]?, ¬ valid post t` | UNREVIEWED | yes | agree on 1485 of 1485 |
| LT-same-if-rejected | then | if it is rejected, ledger {ledger:l} is unchanged | `LVocab.unchangedIfRejected` applied to `outcome, pre(l), post(l)` | `(ok : Bool) (pre post : Ledger) : Prop := ok = false → post.balances.val = pre.balances.val` | UNREVIEWED | yes | agree on 242 of 242 |
| LT-result | then | the result is {amount:s} | `LVocab.resultIs` applied to `outcome, s` | `(o : Option U64) (s : U64) : Prop := o = some s` | UNREVIEWED | yes | agree on 30 of 30 |
| LT-no-result | then | there is no result | `LVocab.noResult` applied to `outcome` | `(o : Option U64) : Prop := o = none` | UNREVIEWED | yes | agree on 5 of 5 |
| LT-some-result | then | there is a result | `LVocab.someResult` applied to `outcome` | `(o : Option U64) : Prop := o ≠ none` | UNREVIEWED | yes | agree on 5 of 5 |
| LT-balance | then | the result is the balance of account {index:i} of ledger {ledger:l} | `LVocab.resultIsBalance` applied to `outcome, pre(l), i` | `(o : Option U64) (l : Ledger) (i : Usize) : Prop := o = l.balances.val[i.val]? ∧ o ≠ none` | UNREVIEWED | yes | agree on 275 of 275 |
| LT-accepted | then | it is accepted | `LVocab.accepted` applied to `outcome` | `(ok : Bool) : Prop := ok = true` | UNREVIEWED | yes | agree on 2 of 2 |
| LT-rejected | then | it is rejected | `LVocab.rejected` applied to `outcome` | `(ok : Bool) : Prop := ok = false` | UNREVIEWED | yes | agree on 2 of 2 |
| LT-moved | then | the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed | `LVocab.moved` applied to `pre(l), post(l), t` | `(pre post : Ledger) (t : Transfer) : Prop := post.balances.val.length = pre.balances.val.length ∧ bal post t.from.val + t.amount.val = bal pre t.from.val ∧ bal post t.to.val = bal pre t.to.val + t.amount.val ∧ ∀ k < pre.balances.val.length, k ≠ t.from.val → k ≠ t.to.val → bal post k = bal pre k` | UNREVIEWED | yes | agree on 726 of 726 |

44 of 44 entries are unreviewed. Record a review with `python3 -m slicegen review <id> --reviewer <name>`; any later change to the phrase, its argument order or its definition voids it.

## Trusted base

- **Rust to Lean**: `lean/Generated/Wallet.lean` and `lean/Generated/Ledger.lean` are produced by Charon + Aeneas from `wallet/src/lib.rs` and `ledger/src/lib.rs`. Hashes of inputs and outputs are in `lean/provenance.json`. The theorems are about the Lean models. A Rust `while` loop becomes a call of Aeneas's `loop` combinator on a separately generated loop-body function.
- **Hand-written loop lemmas** (`lean/Ledger/Lemmas/`, one module per Rust function): not trusted. They are kernel-checked like any proof, and they appear in no statement; a scenario proof that uses one is still checked against exactly its statement.
- **Aeneas library models** (hand-written Lean standing in for std operations): `Aeneas.Std.U64.checked_add` for `u64::checked_add`; `Aeneas.Std.instHSubUScalarResult` for `u64 - u64 (panics on underflow)`; `Aeneas.Std.instHAddUScalarResult` for `usize + usize (panics on overflow)`; `Aeneas.Std.alloc.vec.Vec.len` for `Vec::len`; `Aeneas.Std.alloc.vec.Vec.index` for `Vec indexing v[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.Vec.index_mut` for `Vec indexing v[i] = x (panics out of bounds)`; `Aeneas.Std.Slice.len` for `slice::len`; `Aeneas.Std.Slice.index_usize` for `slice indexing s[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.CloneVec.clone` for `Vec::clone`; `Aeneas.Std.loop` for `while loop (Aeneas's fixed-point combinator; a loop that never ends is `div`)`.
- **slicegen**: untrusted generator. Defences: Lean type-checks its output; the audit compares the constants in each elaborated statement with the glossary entries of the scenario's steps; the statement is printed above.
- **The audit** (`lean/Bdd/Audit.lean`, about 120 lines): reads from the Lean environment which axioms each theorem uses, that each proof's type is exactly its scenario's statement, and which constants statements and definitions mention.
- **Glossary**: `glossary.yaml` + `lean/Wallet/Vocab.lean` + `lean/Ledger/Vocab.lean`. The audit checks that no Given/Then definition depends on a model function: passed for all 36 definitions.
- **Second reading of each phrase**: the Rust predicates in `wallet-bdd/src/lib.rs`, asserted by the cucumber steps in `wallet-bdd/tests/bdd.rs`. The step regexes are checked against the glossary; the predicates are compared with the Lean definitions on a grid of arguments (table above) and by Examples rows giving the same result on both sides.
- **Lean kernel** and the axioms `propext`, `Classical.choice`, `Quot.sound`; **rustc** for everything said about the compiled Rust.

## What this run did not check

- That any glossary definition means what its English phrase says. Only a person can.
- That a `Rule:` line says what the scenarios beneath it say. The rule line is English and is not compiled; nothing connects it to the statements except that a person wrote them under it.
- The suite adequacy note covers four kinds of trivial implementation, generated from the result values listed in the glossary. An implementation that is wrong in some other way is not looked for (the mutation run samples that). "Still allows" without "proved" means only that the search grid holds no input on which a scenario fails; pairs with several Whens, and the `identity` variant (which calls the real model), get no kernel attempt.
- A scenario with several Whens says that each call returns and constrains the state after the LAST one (and the last call's result). Results of earlier Whens are not constrained, no kernel refutation is generated for such a scenario, and it does not count towards input coverage.
- A counterexample to a scenario about a loop is confirmed in the kernel only if a hand-proved lemma about that loop says enough at that input (here: the exact-result lemmas in `lean/Ledger/Lemmas/`). Without one the verdict is COUNTEREXAMPLE, not REFUTED.
- The search grid for the ledger has ledgers of up to four accounts and batches of up to four transfers (two of each length three and four). A fault that needs a fifth loop iteration, or particular amounts, is outside it.
- The boundary grid is small (the product of each parameter's sample values plus literals and their neighbours); there is no random sampling and no shrinking. A false scenario whose counterexamples all lie away from the boundaries would be TESTED-ONLY, not REFUTED. The same holds for the grid on which the two readings of a phrase are compared.
- The trivial-Then check is a `simp`/`scalar_tac` attempt. A Then that follows from the Givens by harder reasoning is not flagged, and a Then that is true but weaker than the English is invisible to it.
- "Some scenario applies to every input" is about Givens only. Whether the Thens pin the result down is not checked by anything: the report lists the Thens per output for a person to judge, and the mutation run samples it with the mutants it happens to contain.
- For the ledger's loops the universal scenarios do NOT determine the result. They state: the total is conserved, the count is at most the batch length, a batch stops only at a transfer that is invalid on the ledger it left, a rejected whole batch changes nothing, and what happens when the first transfer is invalid. They do not state which ledger a partly or fully applied batch leaves, nor that every counted transfer was really applied. That would need the batch computation written again as a specification in the glossary, which this design does not allow. The hand-written lemma library does prove the exact result (against its own pure model `runN`), but a lemma is not a scenario.
- A mutant for which the run fails only because a proof or lemma stopped compiling is not counted as detected: the proof could be rewritten to fit the changed code.
- The derived theorems (`.sat`, `.unsat`, `.refuted`, coverage, trivial-Then attempts) are checked by one `lean` run over `lean/Run/Audit.lean`, not stored as library modules. Trivial-Then attempts are expected to fail; their errors are in `out/audit.log`.
- Staleness is computed from the digests in `out/graph.json`, but every run regenerates everything, so nothing is ever stale here. `python3 -m slicegen.graphlint out/graph.json --what-if <node-id>` shows what would be.

## Refinement graph

`out/graph.json`: 828 nodes, 1303 edges, 55 verdicts. Evidence entries by kind: kernel-checked 239, tested 542, tool-trusted 772. Edges claimed with no evidence at all: 80 (the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.
