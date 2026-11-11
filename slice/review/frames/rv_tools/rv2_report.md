# Slice: rule and scenario report (wallet and ledger)

Generated 2026-11-11T00:19:26+00:00 by `slice/run.sh`. Lean `leanprover/lean4:v4.35.0`, Aeneas `nightly-2026.11.09-5a392f4`, Charon `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, slicegen 0dbb98484692 (slicegen-rule/4).

Each `Rule:` line and each scenario below is an English claim about one of the Rust crates `slice/wallet` (three straight-line functions) and `slice/ledger` (loops over a `Vec` and a slice). The sentence is not bound as a whole: it is **assembled from typed pieces** of a vocabulary (31 domain words, 27 modifiers, 19 frames). The composition is compiled to one Lean statement about the Aeneas-generated Lean model of the crate, and **echoed back in fixed, slot-structured English** (applies to / assuming / then / defaults applied) so the author can check that the tool read the sentence as it was meant. The echo is the first thing printed for every rule and scenario; the Lean is underneath. The statement is then proved, refuted or left open, and every link in that chain is labelled with the kind of evidence behind it:

| Evidence kind | Meaning here |
|---|---|
| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |
| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, every compiled reading on generated inputs (the definition of each frame against its executable reading), and the two readings of each old glossary phrase compared on a grid. |
| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, slicegen (sentence to composition to statement), and the audits that read facts out of the Lean environment. |
| human-asserted | A person's say-so: that each vocabulary piece means its Lean definition. Nothing checks this. It exists only where someone has signed off. |

**How a Rule relates to its scenarios.** The rule line compiles to ONE Lean statement that covers every input (fail-closed: rejected calls included, and the call must answer). The scenarios beneath it are its tested instances (their Examples rows run on the compiled Rust) and, where they are outlines, its **parts**: a generated, kernel-checked theorem `<rule>.from_scenarios` derives the rule statement from the scenario statements, by cases on their Givens. Where that script does not go through, a hand-written proof of exactly the rule statement may stand in (`lean/Wallet/RuleProofs/`). A rule statement found false by the reading search is refuted in the kernel at that input. A scenario may say more than its rule (a progress scenario under a safety rule); the block says which scenarios are parts.

**Two statements per scenario.** The reading compiled from the vocabulary is what is shown and what the verdict is about. The hand-written proofs, the counterexample search and the refutations are about the *flat statement* of the old whole-phrase glossary, unchanged; a generated kernel-checked equivalence carries the verdict across ([Regression](#regression-every-old-statement-against-its-new-reading-plan-node-v3)).

## Rules

Generated from `out/graph.json` (`python3 -m slicegen rules` prints the same from the stored graph). The full block of each rule, with its reading and what it rests on, is under [Rules and their scenarios](#rules-and-their-scenarios).

| Rule | The rule statement | Its scenarios | Examples on Rust / on model | Suite adequacy (informational) |
|---|---|---|---|---|
| Rule: A transfer never changes the total of all balances (`features/wallet.feature:12`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 1 PROVED-INSTANCE | - / 7 of 7 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance (`features/wallet.feature:75`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 5 of 5 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance (`features/wallet.feature:105`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 5 of 5 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A transfer for which the amount is not more than the sender's balance is always accepted (`features/wallet.feature:135`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | - / 2 of 2 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A deposit earns interest (`features/wallet.feature:156`) | **UNBOUND (no statement)** | **NO SCENARIO PROVED**<br>1 UNBOUND | - / 0 of 0 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A batch never changes the total of all balances of the ledger (`features/ledger.feature:13`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL | - / 12 of 12 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, no transfer is applied and the ledger is unchanged (`features/ledger.feature:66`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL, 2 PROVED-INSTANCE | - / 8 of 8 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: For a batch for which every transfer of the batch is valid on the ledger, every transfer of the batch is applied (`features/ledger.feature:111`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | - / 2 of 2 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A transfer is accepted exactly when the transfer is valid on the ledger, and a rejected transfer never changes the ledger, and for a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed (`features/ledger.feature:130`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 8 of 8 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum (`features/ledger.feature:164`) | **PROVED FOR ALL INPUTS (by a hand-written proof)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 8 of 8 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A computation of the total is always accepted (`features/ledger.feature:195`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | - / 2 of 2 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: For a lookup, the result is the balance of the account in the ledger (`features/ledger.feature:211`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 4 of 4 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A rejected batch applied as a whole never changes the ledger, and a batch applied as a whole never changes the total of all balances of the ledger (`features/ledger.feature:238`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 3 PROVED-INSTANCE | - / 10 of 10 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| Rule: A batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum (`features/ledger.feature:304`) | **PROVED FOR ALL INPUTS (by a hand-written proof)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | - / 5 of 5 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |
| (scenarios of `Feature: Negative controls` that are not under a Rule) (`features/negative.feature`) | - | **SOME SCENARIOS PROVED**<br>1 VACUOUS, 1 PROVED-FOR-ALL | - / 1 of 2 | not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed) |

14 rule statements: 10 PROVED-FOR-ALL, 3 REFUTED, 1 UNBOUND. Every rule statement got the verdict it was expected to get.


## Summary

| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |
|---|---|---|---|---|
| A covered transfer moves the money and conserves the total (`features/wallet.feature:18`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (8 of 8); UNREVIEWED VOCABULARY (16 of 16) |
| Transferring more than the sender has is rejected and changes nothing (`features/wallet.feature:35`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (10 of 10) |
| A transfer the receiver has no room for is rejected and changes nothing (`features/wallet.feature:50`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED VOCABULARY (12 of 12) |
| Transferring more than you have is rejected and changes nothing (`features/wallet.feature:66`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (9 of 9) |
| A covered withdrawal succeeds and takes exactly the amount (`features/wallet.feature:78`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (10 of 10) |
| Withdrawing more than the balance is rejected and changes nothing (`features/wallet.feature:92`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (10 of 10) |
| A deposit with room succeeds and adds exactly the amount (`features/wallet.feature:108`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (11 of 11) |
| A deposit that would overflow is rejected and changes nothing (`features/wallet.feature:122`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (11 of 11) |
| A transfer the sender can afford always succeeds (`features/wallet.feature:141`) | **REFUTED** | REFUTED | - / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED VOCABULARY (13 of 13) |
| A deposit earns interest (`features/wallet.feature:161`) | **UNBOUND** | UNBOUND | - | - |
| Applying any batch of transfers conserves the total of all balances (`features/ledger.feature:20`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 6 of 6 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (9 of 9) |
| A batch stops only at a transfer that cannot be carried out (`features/ledger.feature:39`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 5 of 5 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (11 of 11) |
| Two batches applied one after the other conserve the total (`features/ledger.feature:54`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (13 of 13) |
| A batch whose first transfer is invalid changes nothing (`features/ledger.feature:69`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (15 of 15) |
| The number of transfers applied is at most the length of the batch (`features/ledger.feature:83`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (9 of 9) |
| A batch of two valid transfers is applied in full (`features/ledger.feature:96`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (12 of 12) |
| A batch stops at its first invalid transfer and keeps what it has applied (`features/ledger.feature:104`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (12 of 12) |
| A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:118`) | **REFUTED** | REFUTED | - / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (13 of 13) |
| A valid transfer is accepted and moves exactly its amount (`features/ledger.feature:133`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED VOCABULARY (23 of 23) |
| An invalid transfer is rejected and changes nothing (`features/ledger.feature:148`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 5 of 5 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (14 of 14) |
| The total is the sum of the balances when that fits (`features/ledger.feature:167`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 5 of 5 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (13 of 13) |
| The total of balances that do not fit is reported as absent (`features/ledger.feature:182`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (15 of 15) |
| The total of a ledger can always be computed (`features/ledger.feature:200`) | **REFUTED** | REFUTED | - / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (8 of 8) |
| Looking up an existing account gives its balance (`features/ledger.feature:214`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (10 of 10) |
| Looking up an account that does not exist gives nothing (`features/ledger.feature:226`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (11 of 11) |
| A batch applied as a whole that is rejected leaves the ledger unchanged (`features/ledger.feature:243`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 4 of 4 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (9 of 9) |
| A batch applied as a whole whose first transfer is invalid is rejected and changes nothing (`features/ledger.feature:256`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (14 of 14) |
| Applying a batch as a whole conserves the total of all balances (`features/ledger.feature:268`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED VOCABULARY (9 of 9) |
| A batch of valid transfers applied as a whole is accepted and applied (`features/ledger.feature:280`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (10 of 10) |
| A batch applied as a whole is rolled back when its third transfer is invalid (`features/ledger.feature:289`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (12 of 12) |
| A batch applied as a whole is rolled back when a later transfer is invalid (`features/ledger.feature:297`) | **PROVED-INSTANCE** | PROVED-INSTANCE | - / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED VOCABULARY (12 of 12) |
| The total computed after any batch is the total before it, when that total fits (`features/ledger.feature:311`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (15 of 15) |
| The total computed after any batch is still absent when it did not fit before (`features/ledger.feature:326`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | - / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (17 of 17) |
| A withdrawal that is both covered and not covered (`features/negative.feature:11`) | **VACUOUS** | VACUOUS | - / 0 of 1 | ROW OUTSIDE GIVENS; UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED VOCABULARY (10 of 10) |
| A deposit does not touch a bystander (`features/negative.feature:25`) | **PROVED-FOR-ALL (1 of 2 Thens substantive)** | PROVED-FOR-ALL | - / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); TRIVIAL-THEN; FRAME-TRIVIAL; UNREVIEWED VOCABULARY (12 of 12) |

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

No mutation results found (`mutation/results.json`). Run `python3 mutation/run_mutants.py`.

## Suite adequacy note

**Informational. It changes no verdict and never fails a run.** A single proved scenario is not expected to pin behaviour: "a transfer never changes the total" is also true of code that rejects every transfer. The question here is about the suite. For each operation, trivial implementations are generated as Lean models of exactly the type of the Aeneas-generated model (`type_of%`), and each proved universal scenario is stated again with the trivial model in place of the call:

| Trivial implementation | What it does |
|---|---|
| reject-all | always answers with a rejecting value and leaves the state as it was |
| no-op | always answers with a success value and leaves the state as it was (does nothing but report success) |
| identity | answers as the code does, but never changes the state |
| constant | always answers the same value; the state is left as it was, or reset to a fixed one |

A scenario **rules out** a trivial implementation when the search finds an input on which the scenario is false of it (the same boundary grid as the counterexample search; a kernel-checked refutation at that input is attempted). A suite rules it out when one of its scenarios does, and **still allows** it otherwise. "Still allows" is proved for all inputs only where it says so; otherwise it means no scenario was shown false of it on the grid. Scenarios tagged `@control` and scenarios that are not proved are not counted. Which result values count as a rejection or a success is stated in `glossary.yaml` (`trivial`).

**Not computed in this run:** the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed).

## Rules and their scenarios

One block per `Rule:` (and one per feature for scenarios that sit under no rule), generated from `out/graph.json`: the rule line, **its compiled reading echoed in English**, the verdict of the rule statement, the scenarios beneath it and whether each is a part the rule is proved from, the example rows, the suite note, and what the result rests on. Beneath each block: the rule's Lean statement, then every scenario with its own reading, verdict and (folded) Lean.

### Rule: A transfer never changes the total of all balances

```text
Rule: A transfer never changes the total of all balances   [features/wallet.feature:12]   tags @id:transfer_total
  Every transfer falls under one of three cases. Covered, and the receiver has room: it must
  succeed and move exactly the amount (the progress scenario). The sender is short, or the
  receiver has no room: it is rejected and neither balance moves.
  Reading   applies to  a transfer: every sender, every receiver, every amount
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the sum of the balances of every wallet named (the sender, the receiver) after the call equals the
                        sum of the balances of every wallet named (the sender, the receiver) before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.wallet.transfer_total.holds : Rule.wallet.transfer_total.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            kernel-checked   theorem Rule.wallet.transfer_total.from_scenarios : transfer_conserves.reading →
                             transfer_short.reading → transfer_no_room.reading → Rule.wallet.transfer_total.reading
                             (generated glue, type checked by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 3 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 216 generated inputs (216 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 216 of 216 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 5 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 5 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 1 of 1 literal examples proved for their own values
            PROVED-FOR-ALL  A covered transfer moves the money and conserves the total   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-INSTANCE Transferring more than you have is rejected and changes nothing   [an instance: literal values]
  Examples  7 of 7 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      19 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.transfer, never_changes, aggregate, all_of, w.balance, given, i.has_balance, is, amount_value,
                 not_more_than, sum_within, w.maximum, always, decreases_by, increases_by, w.succeeds, more_than,
                 w.rejected_with, sum_exceeds)
                 4 of 4 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 12 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 3 theorems for all inputs, 1 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.wallet.transfer_conserves, Spec.wallet.transfer_short, Spec.wallet.transfer_no_room,
                 Spec.wallet.transfer_short_example)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.wallet.transfer_total.reading : Prop :=
  Frames.NeverChanges W.transfer (fun st inp => Frames.aggregate ([W.balance st.1, W.balance st.2]))
```

</details>

#### PROVED-FOR-ALL: A covered transfer moves the money and conserves the total

`features/wallet.feature:18`  id `Spec.wallet.transfer_conserves`  tags `@id:transfer_conserves`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of <amount> from Alice to Bob: every sender (Alice), every receiver (Bob), and every amount
            <amount>; for every value of a, b
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Bob is <b>; <amount> is at most the balance of Alice; the
            balance of Bob plus <amount> is at most the largest balance a wallet can hold (2^64 - 1)
then        the call gives an answer [default D1]
            the answer is Ok
            the balance of Alice after the call, plus <amount>, equals the balance of Alice before it, exactly
            the balance of Bob after the call equals the balance of Bob before it plus <amount>, exactly
            the sum of the balances of every wallet named (Alice, Bob) after the call equals the sum of the balances of
            every wallet named (Alice, Bob) before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A covered transfer moves the money and conserves the total
  kernel-checked   theorem Spec.wallet.transfer_conserves.reading_holds : Spec.wallet.transfer_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_conserves.reading_iff : Spec.wallet.transfer_conserves.reading ↔ Spec.wallet.transfer_conserves.stmt  (NEW ↔ OLD: the reading compiled from 16 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_conserves.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/wallet/transfer_conserves.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 8 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-room, W-transfer, T-ok, T-dec, T-inc, T-total
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 16 vocabulary pieces signed off by anyone - UNREVIEWED: w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, sum_within, w.maximum, always, decreases_by, increases_by, never_changes, w.succeeds, aggregate, all_of
  tested           the reading on 7776 generated inputs (91 in scope): the definition of each frame and its executable reading agree on 364 of 364 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, sum_within, w.maximum, always, decreases_by, increases_by, never_changes, w.succeeds, aggregate, all_of`:

```lean
def Spec.wallet.transfer_conserves.reading : Prop :=
  ∀ (a b : U64),
    Frames.Always ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ (W.balance st.2) + inp.val ≤ W.maximum)) (fun ans => W.accepted ans) ∧
    Frames.DecreasesBy ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ (W.balance st.2) + inp.val ≤ W.maximum)) (fun st inp => W.balance st.1) (fun st inp => inp.val) ∧
    Frames.IncreasesBy ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ (W.balance st.2) + inp.val ≤ W.maximum)) (fun st inp => W.balance st.2) (fun st inp => inp.val) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ (W.balance st.2) + inp.val ≤ W.maximum)) (fun st inp => Frames.aggregate ([W.balance st.1, W.balance st.2]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/transfer_conserves.lean`):

```lean
theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt := by
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
  simp [Vocab.hasBalance, Vocab.decreasedBy, Vocab.increasedBy, Vocab.totalUnchanged] at *
  scalar_tac
```

</details>

#### PROVED-FOR-ALL: Transferring more than the sender has is rejected and changes nothing

`features/wallet.feature:35`  id `Spec.wallet.transfer_short`  tags `@id:transfer_short`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of <amount> from Alice to Bob: every sender (Alice), every receiver (Bob), and every amount
            <amount>; for every value of a, b
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Bob is <b>; <amount> is strictly more than the balance of Alice
then        the call gives an answer [default D1]
            the answer is the error 'insufficient funds'
            the balance of Alice after the call equals the balance of Alice before it
            the balance of Bob after the call equals the balance of Bob before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short.reading_holds : Spec.wallet.transfer_short.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_short.reading_iff : Spec.wallet.transfer_short.reading ↔ Spec.wallet.transfer_short.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_short.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_short : Spec.wallet.transfer_short.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-transfer, T-err, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: w.transfer, given, i.has_balance, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with
  tested           the reading on 7776 generated inputs (90 in scope): the definition of each frame and its executable reading agree on 270 of 270 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, i.has_balance, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with`:

```lean
def Spec.wallet.transfer_short.reading : Prop :=
  ∀ (a b : U64),
    Frames.Always ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ (W.balance st.1) < inp.val)) (fun ans => W.rejectedWith wallet.WalletError.InsufficientFunds ans) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ (W.balance st.1) < inp.val)) (fun st inp => W.balance st.1) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ (W.balance st.1) < inp.val)) (fun st inp => W.balance st.2)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/transfer_short.lean`):

```lean
theorem Spec.wallet.transfer_short : Spec.wallet.transfer_short.stmt := by
  intro a b amount alice bob h1 h2 h3
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

</details>

#### PROVED-FOR-ALL: A transfer the receiver has no room for is rejected and changes nothing

`features/wallet.feature:50`  id `Spec.wallet.transfer_no_room`  tags `@id:transfer_no_room`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of <amount> from Alice to Bob: every sender (Alice), every receiver (Bob), and every amount
            <amount>; for every value of a, b
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Bob is <b>; <amount> is at most the balance of Alice; the
            balance of Bob plus <amount> is strictly more than the largest balance a wallet can hold (2^64 - 1)
then        the call gives an answer [default D1]
            the answer is the error 'overflow'
            the balance of Alice after the call equals the balance of Alice before it
            the balance of Bob after the call equals the balance of Bob before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_no_room.reading_holds : Spec.wallet.transfer_no_room.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_no_room.reading_iff : Spec.wallet.transfer_no_room.reading ↔ Spec.wallet.transfer_no_room.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_no_room.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_no_room : Spec.wallet.transfer_no_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_no_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_no_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-noroom, W-transfer, T-err, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, sum_exceeds, w.maximum, always, never_changes, w.rejected_with
  tested           the reading on 7776 generated inputs (35 in scope): the definition of each frame and its executable reading agree on 105 of 105 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, sum_exceeds, w.maximum, always, never_changes, w.rejected_with`:

```lean
def Spec.wallet.transfer_no_room.reading : Prop :=
  ∀ (a b : U64),
    Frames.Always ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ W.maximum < (W.balance st.2) + inp.val)) (fun ans => W.rejectedWith wallet.WalletError.Overflow ans) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ W.maximum < (W.balance st.2) + inp.val)) (fun st inp => W.balance st.1) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1) ∧ W.maximum < (W.balance st.2) + inp.val)) (fun st inp => W.balance st.2)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/transfer_no_room.lean`):

```lean
theorem Spec.wallet.transfer_no_room : Spec.wallet.transfer_no_room.stmt := by
  intro a b amount alice bob h1 h2 h3 h4
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

</details>

#### PROVED-INSTANCE: Transferring more than you have is rejected and changes nothing

`features/wallet.feature:66`  id `Spec.wallet.transfer_short_example`  tags `@id:transfer_short_example`

```gherkin
Scenario: Transferring more than you have is rejected and changes nothing
  Given Alice has a balance of 10
  And Bob has a balance of 7
  When Alice transfers 11 to Bob
  Then the operation is rejected with insufficient funds
  And Alice's balance is unchanged
  And Bob's balance is unchanged
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of 11 from Alice to Bob: every sender (Alice), every receiver (Bob), with the one amount 11 (a
            plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is 10; the balance of Bob is 7; the input is 11
then        the call gives an answer [default D1]
            the answer is the error 'insufficient funds'
            the balance of Alice after the call equals the balance of Alice before it
            the balance of Bob after the call equals the balance of Bob before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  Transferring more than you have is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short_example.reading_holds : Spec.wallet.transfer_short_example.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_short_example.reading_iff : Spec.wallet.transfer_short_example.reading ↔ Spec.wallet.transfer_short_example.stmt  (NEW ↔ OLD: the reading compiled from 9 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_short_example.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short_example.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short_example.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: G-balance, W-transfer, T-err, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone - UNREVIEWED: w.transfer, given, i.has_balance, is, w.balance, amount_value, always, never_changes, w.rejected_with
  tested           the reading on 169 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 3 of 3 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, i.has_balance, is, w.balance, amount_value, always, never_changes, w.rejected_with`:

```lean
def Spec.wallet.transfer_short_example.reading : Prop :=
  Frames.Always ((W.transfer).given (fun st inp => (W.balance st.1) = (10#u64).val ∧ (W.balance st.2) = (7#u64).val ∧ inp = (11#u64))) (fun ans => W.rejectedWith wallet.WalletError.InsufficientFunds ans) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = (10#u64).val ∧ (W.balance st.2) = (7#u64).val ∧ inp = (11#u64))) (fun st inp => W.balance st.1) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = (10#u64).val ∧ (W.balance st.2) = (7#u64).val ∧ inp = (11#u64))) (fun st inp => W.balance st.2)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/transfer_short_example.lean`):

```lean
theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt := by
  intro alice bob h1 h2
  apply Bdd.ok3_of_spec
  unfold wallet.transfer
  step*
```

</details>

### Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance

```text
Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance   [features/wallet.feature:75]   tags @id:withdrawal
  Reading   applies to  clause 1: a withdrawal: every wallet, every amount
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the call gives an answer
                        clause 2: a withdrawal: every wallet, every amount
                        ONLY successful calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call, plus the amount, equals the balance of the wallet before
                        it, exactly
                        clause 3: a withdrawal: every wallet, every amount
                        ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call equals the balance of the wallet before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.wallet.withdrawal.holds : Rule.wallet.withdrawal.reading  (THE RULE STATEMENT
                             ITSELF, as one theorem; type checked by the audit); axioms propext, Classical.choice,
                             Quot.sound
            kernel-checked   theorem Rule.wallet.withdrawal.from_scenarios : withdraw_covered.reading →
                             withdraw_too_much.reading → Rule.wallet.withdrawal.reading  (generated glue, type checked
                             by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 36 generated inputs (36 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 108 of 108 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 8 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 8 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing   [a part: the rule statement is proved from it]
  Examples  5 of 5 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      16 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.withdraw, always_answers, successful, decreases_by, w.balance, amount_value, rejected,
                 never_changes, given, i.has_balance, is, not_more_than, always, w.succeeds, more_than,
                 w.rejected_with)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.wallet.withdraw_covered, Spec.wallet.withdraw_too_much)
    translation  Lean model wallet.Wallet.withdraw generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.wallet.withdrawal.reading : Prop :=
  Frames.AlwaysAnswers W.withdraw ∧
    Frames.DecreasesBy (W.withdraw).successful (fun st inp => W.balance st) (fun st inp => inp.val) ∧
    Frames.NeverChanges (W.withdraw).rejected (fun st inp => W.balance st)
```

</details>

#### PROVED-FOR-ALL: A covered withdrawal succeeds and takes exactly the amount

`features/wallet.feature:78`  id `Spec.wallet.withdraw_covered`  tags `@id:withdraw_covered`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount>; for every value of a
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; <amount> is at most the balance of Alice
then        the call gives an answer [default D1]
            the answer is Ok
            the balance of Alice after the call, plus <amount>, equals the balance of Alice before it, exactly
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount
  kernel-checked   theorem Spec.wallet.withdraw_covered.reading_holds : Spec.wallet.withdraw_covered.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.withdraw_covered.reading_iff : Spec.wallet.withdraw_covered.reading ↔ Spec.wallet.withdraw_covered.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.withdraw_covered.reading_sat)
  kernel-checked   theorem Spec.wallet.withdraw_covered : Spec.wallet.withdraw_covered.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_covered.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_covered.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-withdraw, T-ok, T-dec
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: w.withdraw, given, i.has_balance, is, w.balance, amount_value, not_more_than, always, decreases_by, w.succeeds
  tested           the reading on 216 generated inputs (21 in scope): the definition of each frame and its executable reading agree on 42 of 42 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, i.has_balance, is, w.balance, amount_value, not_more_than, always, decreases_by, w.succeeds`:

```lean
def Spec.wallet.withdraw_covered.reading : Prop :=
  ∀ (a : U64),
    Frames.Always ((W.withdraw).given (fun st inp => (W.balance st) = a.val ∧ inp.val ≤ (W.balance st))) (fun ans => W.accepted ans) ∧
    Frames.DecreasesBy ((W.withdraw).given (fun st inp => (W.balance st) = a.val ∧ inp.val ≤ (W.balance st))) (fun st inp => W.balance st) (fun st inp => inp.val)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/withdraw_covered.lean`):

```lean
theorem Spec.wallet.withdraw_covered : Spec.wallet.withdraw_covered.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.withdraw
  step*
```

</details>

#### PROVED-FOR-ALL: Withdrawing more than the balance is rejected and changes nothing

`features/wallet.feature:92`  id `Spec.wallet.withdraw_too_much`  tags `@id:withdraw_too_much`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount>; for every value of a
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; <amount> is strictly more than the balance of Alice
then        the call gives an answer [default D1]
            the answer is the error 'insufficient funds'
            the balance of Alice after the call equals the balance of Alice before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.withdraw_too_much.reading_holds : Spec.wallet.withdraw_too_much.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.withdraw_too_much.reading_iff : Spec.wallet.withdraw_too_much.reading ↔ Spec.wallet.withdraw_too_much.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.withdraw_too_much.reading_sat)
  kernel-checked   theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_too_much.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_too_much.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-withdraw, T-err, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: w.withdraw, given, i.has_balance, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with
  tested           the reading on 216 generated inputs (15 in scope): the definition of each frame and its executable reading agree on 30 of 30 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, i.has_balance, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with`:

```lean
def Spec.wallet.withdraw_too_much.reading : Prop :=
  ∀ (a : U64),
    Frames.Always ((W.withdraw).given (fun st inp => (W.balance st) = a.val ∧ (W.balance st) < inp.val)) (fun ans => W.rejectedWith wallet.WalletError.InsufficientFunds ans) ∧
    Frames.NeverChanges ((W.withdraw).given (fun st inp => (W.balance st) = a.val ∧ (W.balance st) < inp.val)) (fun st inp => W.balance st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/withdraw_too_much.lean`):

```lean
theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.withdraw
  step*
```

</details>

### Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance

```text
Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance   [features/wallet.feature:105]   tags @id:deposit
  Reading   applies to  clause 1: a deposit: every wallet, every amount
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the call gives an answer
                        clause 2: a deposit: every wallet, every amount
                        ONLY successful calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call equals the balance of the wallet before it plus the
                        amount, exactly
                        clause 3: a deposit: every wallet, every amount
                        ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call equals the balance of the wallet before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.wallet.deposit.holds : Rule.wallet.deposit.reading  (THE RULE STATEMENT
                             ITSELF, as one theorem; type checked by the audit); axioms propext, Classical.choice,
                             Quot.sound
            kernel-checked   theorem Rule.wallet.deposit.from_scenarios : deposit_with_room.reading →
                             deposit_overflow.reading → Rule.wallet.deposit.reading  (generated glue, type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 36 generated inputs (36 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 108 of 108 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 8 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 8 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing   [a part: the rule statement is proved from it]
  Examples  5 of 5 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      17 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.deposit, always_answers, successful, increases_by, w.balance, amount_value, rejected,
                 never_changes, given, i.has_balance, is, sum_within, w.maximum, always, w.succeeds, sum_exceeds,
                 w.rejected_with)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.wallet.deposit_with_room, Spec.wallet.deposit_overflow)
    translation  Lean model wallet.Wallet.deposit generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.wallet.deposit.reading : Prop :=
  Frames.AlwaysAnswers W.deposit ∧
    Frames.IncreasesBy (W.deposit).successful (fun st inp => W.balance st) (fun st inp => inp.val) ∧
    Frames.NeverChanges (W.deposit).rejected (fun st inp => W.balance st)
```

</details>

#### PROVED-FOR-ALL: A deposit with room succeeds and adds exactly the amount

`features/wallet.feature:108`  id `Spec.wallet.deposit_with_room`  tags `@id:deposit_with_room`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount>; for every value of a
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Alice plus <amount> is at most the largest balance a wallet can
            hold (2^64 - 1)
then        the call gives an answer [default D1]
            the answer is Ok
            the balance of Alice after the call equals the balance of Alice before it plus <amount>, exactly
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount
  kernel-checked   theorem Spec.wallet.deposit_with_room.reading_holds : Spec.wallet.deposit_with_room.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.deposit_with_room.reading_iff : Spec.wallet.deposit_with_room.reading ↔ Spec.wallet.deposit_with_room.stmt  (NEW ↔ OLD: the reading compiled from 11 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.deposit_with_room.reading_sat)
  kernel-checked   theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_with_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_with_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-inc
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 11 vocabulary pieces signed off by anyone - UNREVIEWED: w.deposit, given, i.has_balance, is, w.balance, amount_value, sum_within, w.maximum, always, increases_by, w.succeeds
  tested           the reading on 216 generated inputs (21 in scope): the definition of each frame and its executable reading agree on 42 of 42 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, given, i.has_balance, is, w.balance, amount_value, sum_within, w.maximum, always, increases_by, w.succeeds`:

```lean
def Spec.wallet.deposit_with_room.reading : Prop :=
  ∀ (a : U64),
    Frames.Always ((W.deposit).given (fun st inp => (W.balance st) = a.val ∧ (W.balance st) + inp.val ≤ W.maximum)) (fun ans => W.accepted ans) ∧
    Frames.IncreasesBy ((W.deposit).given (fun st inp => (W.balance st) = a.val ∧ (W.balance st) + inp.val ≤ W.maximum)) (fun st inp => W.balance st) (fun st inp => inp.val)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/deposit_with_room.lean`):

```lean
theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

</details>

#### PROVED-FOR-ALL: A deposit that would overflow is rejected and changes nothing

`features/wallet.feature:122`  id `Spec.wallet.deposit_overflow`  tags `@id:deposit_overflow`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount>; for every value of a
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Alice plus <amount> is strictly more than the largest balance a
            wallet can hold (2^64 - 1)
then        the call gives an answer [default D1]
            the answer is the error 'overflow'
            the balance of Alice after the call equals the balance of Alice before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.deposit_overflow.reading_holds : Spec.wallet.deposit_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.deposit_overflow.reading_iff : Spec.wallet.deposit_overflow.reading ↔ Spec.wallet.deposit_overflow.stmt  (NEW ↔ OLD: the reading compiled from 11 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.deposit_overflow.reading_sat)
  kernel-checked   theorem Spec.wallet.deposit_overflow : Spec.wallet.deposit_overflow.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_overflow.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-noroom, W-deposit, T-err, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 11 vocabulary pieces signed off by anyone - UNREVIEWED: w.deposit, given, i.has_balance, is, w.balance, amount_value, sum_exceeds, w.maximum, always, never_changes, w.rejected_with
  tested           the reading on 216 generated inputs (15 in scope): the definition of each frame and its executable reading agree on 30 of 30 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, given, i.has_balance, is, w.balance, amount_value, sum_exceeds, w.maximum, always, never_changes, w.rejected_with`:

```lean
def Spec.wallet.deposit_overflow.reading : Prop :=
  ∀ (a : U64),
    Frames.Always ((W.deposit).given (fun st inp => (W.balance st) = a.val ∧ W.maximum < (W.balance st) + inp.val)) (fun ans => W.rejectedWith wallet.WalletError.Overflow ans) ∧
    Frames.NeverChanges ((W.deposit).given (fun st inp => (W.balance st) = a.val ∧ W.maximum < (W.balance st) + inp.val)) (fun st inp => W.balance st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/wallet/deposit_overflow.lean`):

```lean
theorem Spec.wallet.deposit_overflow : Spec.wallet.deposit_overflow.stmt := by
  intro a amount alice h1 h2
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

</details>

### Rule: A transfer for which the amount is not more than the sender's balance is always accepted

```text
Rule: A transfer for which the amount is not more than the sender's balance is always accepted   [features/wallet.feature:135]   tags @expect-refuted @id:transfer_affordable
  Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.
  Reading   applies to  a transfer: every sender, every receiver, every amount
                        every such call, accepted or rejected [default D2]
            assuming    the amount is at most the balance of the sender
            then        the call gives an answer [default D1]
                        the answer is an acceptance
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
            kernel-checked   theorem Rule.wallet.transfer_affordable.refuted : ¬
                             Rule.wallet.transfer_affordable.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   sender = 1, receiver = 18446744073709551615, amount = 1
                             at this input the rule does not hold: NOT "the answer is an acceptance"
            tested           searched on 216 generated inputs (126 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 126 of 126 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 7 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 7 vocabulary pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A transfer the sender can afford always succeeds   (expected REFUTED)   [beneath the rule; not used to prove it]
  Examples  2 of 2 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      14 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.transfer, given, always, not_more_than, amount_value, w.balance, accepted, i.has_balance, is,
                 decreases_by, never_changes, w.succeeds, aggregate, all_of)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.wallet.transfer_always_succeeds.refuted)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.wallet.transfer_affordable.reading : Prop :=
  Frames.Always ((W.transfer).given (fun st inp => inp.val ≤ (W.balance st.1))) (fun ans => (W.transfer).accepted ans)
```

</details>

#### REFUTED: A transfer the sender can afford always succeeds

`features/wallet.feature:141`  id `Spec.wallet.transfer_always_succeeds`  tags `@expect-refuted @id:transfer_always_succeeds`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of <amount> from Alice to Bob: every sender (Alice), every receiver (Bob), and every amount
            <amount>; for every value of a, b
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Bob is <b>; <amount> is at most the balance of Alice
then        the call gives an answer [default D1]
            the answer is Ok
            the balance of Alice after the call, plus <amount>, equals the balance of Alice before it, exactly
            the sum of the balances of every wallet named (Alice, Bob) after the call equals the sum of the balances of
            every wallet named (Alice, Bob) before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
REFUTED  A transfer the sender can afford always succeeds
  kernel-checked   theorem Spec.wallet.transfer_always_succeeds.reading_iff : Spec.wallet.transfer_always_succeeds.reading ↔ Spec.wallet.transfer_always_succeeds.stmt  (NEW ↔ OLD: the reading compiled from 13 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_always_succeeds.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_always_succeeds.refuted : ¬ Spec.wallet.transfer_always_succeeds.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | a | b                    | amount |
                   | 1 | 18446744073709551615 | 1      |
                   When Alice transfers 1 to Bob  =>  returned Err(Overflow); Alice: balance 1; Bob: balance 18446744073709551615
                   failed Then: "the operation succeeds"; "Alice's balance is decreased by 1"
                   held   Then: "the total of all balances is unchanged"
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-transfer, T-ok, T-dec, T-total
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  tested           boundary grid on the Lean model: 216 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 13 vocabulary pieces signed off by anyone - UNREVIEWED: w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, always, decreases_by, never_changes, w.succeeds, aggregate, all_of
  tested           the reading on 7776 generated inputs (126 in scope): the definition of each frame and its executable reading agree on 378 of 378 evaluations; the reading is false at one of them
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, i.has_balance, is, w.balance, amount_value, not_more_than, always, decreases_by, never_changes, w.succeeds, aggregate, all_of`:

```lean
def Spec.wallet.transfer_always_succeeds.reading : Prop :=
  ∀ (a b : U64),
    Frames.Always ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1))) (fun ans => W.accepted ans) ∧
    Frames.DecreasesBy ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1))) (fun st inp => W.balance st.1) (fun st inp => inp.val) ∧
    Frames.NeverChanges ((W.transfer).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ inp.val ≤ (W.balance st.1))) (fun st inp => Frames.aggregate ([W.balance st.1, W.balance st.2]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

</details>

### Rule: A deposit earns interest

```text
Rule: A deposit earns interest   [features/wallet.feature:156]   tags @expect-unbound @id:interest
  Not a claim about this wallet: the rule line and its scenario use words the vocabulary does not define.
  Reading   NONE: UNBOUND   (expected: UNBOUND)
            features/wallet.feature:156: no composition of vocabulary pieces reads "a deposit earns interest" as a rule
              clause (<a / an> [successful | rejected | internal] <operation> [followed by <operation>] [for which
              <condition>] <what it does>, or: for <such an operation>, <what a Then would say>)
              operations of the vocabulary: batch, batch applied as a whole, computation of the total, lookup, transfer
            the rule line is not a composition of vocabulary pieces, so no statement was generated for it
  Scenarios NO SCENARIO PROVED: 0 of 1 literal examples proved for their own values
            UNBOUND         A deposit earns interest   (expected UNBOUND)
  Examples  none could be evaluated
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      no vocabulary piece is used (no reading was compiled)
    proof        no kernel-checked theorem for: deposit_earns_interest
    translation  no model function is involved (no statement was generated)
    compilation  the compiled Rust was not exercised in this run
```

#### UNBOUND: A deposit earns interest

`features/wallet.feature:161`  id `Spec.wallet.deposit_earns_interest`  tags `@expect-unbound @id:deposit_earns_interest`

```gherkin
Scenario: A deposit earns interest
  Given Alice has a balance of 100
  When Alice deposits 5
  Then Alice earns interest on her balance
```

```text
UNBOUND  A deposit earns interest
  vocabulary       UNBOUND: features/wallet.feature:164: no composition of vocabulary pieces reads "Alice earns interest on her balance" as a claim
                   nearest forms of the vocabulary for a claim:
                     - {m:measure<transfer>} is now {t:term<transfer>}
                     - {a:ameasure<transfer>} is {t:term<transfer>}
                     - {m:measure<optnum>} is unchanged
                   a new sentence needs no new entry if it can be said with existing forms; otherwise add a piece (or an idiom) to vocabulary.yaml
  features/wallet.feature:164: no glossary `then` phrase matches: "Alice earns interest on her balance"
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
```

### Rule: A batch never changes the total of all balances of the ledger

```text
Rule: A batch never changes the total of all balances of the ledger   [features/ledger.feature:13]   tags @id:batch_total
  The first scenario is the safety half: it holds whatever the ledger and whatever the batch,
  and it would also hold of a batch function that does nothing. The second is the progress
  half: the batch goes on for as long as it can.
  Reading   applies to  a batch: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the sum of the balances of every account of the ledger after the call equals the sum of the
                        balances of every account of the ledger before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.ledger.batch_total.holds : Rule.ledger.batch_total.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger.batch_total.from_scenarios : batch_conserves.reading →
                             batch_stops_at_invalid.reading → Rule.ledger.batch_total.reading  (generated glue, type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 4 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 4 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Two batches applied one after the other conserve the total   [beneath the rule; not used to prove it]
  Examples  12 of 12 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      18 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch, never_changes, aggregate, l.balances_of, given, i.holds, is, l.ledger,
                 balances_value, every_of, i.stopped_only_at, l.stopped_at, not, l.valid, and_then, result_at_most,
                 l.applied, l.length)
                 3 of 3 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 5 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 3 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_conserves, Spec.ledger.batch_stops_at_invalid, Spec.ledger.two_batches_conserve)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.batch_total.reading : Prop :=
  Frames.NeverChanges L.applyBatch (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### PROVED-FOR-ALL: Applying any batch of transfers conserves the total of all balances

`features/ledger.feature:20`  id `Spec.ledger.batch_conserves`  tags `@id:batch_conserves`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>;
            for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the sum of the balances of every account of ledger Main after the call equals the sum of the balances of
            every account of ledger Main before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances
  kernel-checked   theorem Spec.ledger.batch_conserves.reading_holds : Spec.ledger.batch_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_conserves.reading_iff : Spec.ledger.batch_conserves.reading ↔ Spec.ledger.batch_conserves.stmt  (NEW ↔ OLD: the reading compiled from 9 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_conserves.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           6 of 6 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of`:

```lean
def Spec.ledger.batch_conserves.reading : Prop :=
  ∀ (balances : List U64),
    Frames.NeverChanges ((L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_conserves.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.totalUnchanged main main'
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_conserves.lean`):

```lean
theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h1⟩
```

</details>

#### PROVED-FOR-ALL: A batch stops only at a transfer that cannot be carried out

`features/ledger.feature:39`  id `Spec.ledger.batch_stops_at_invalid`  tags `@id:batch_stops_at_invalid`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>;
            for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            every transfer of the batch <batch> at the position the reported count points to (none if every transfer was
            applied) can NOT be carried out exactly on ledger Main (an account does not exist, or both are the same, or
            the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1), judged on the state
            after the call
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection
            within the one Given, Then or Rule clause they occur in
            D7 items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the
            state after the call
```

```text
PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid.reading_holds : Spec.ledger.batch_stops_at_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid.reading_iff : Spec.ledger.batch_stops_at_invalid.reading ↔ Spec.ledger.batch_stops_at_invalid.stmt  (NEW ↔ OLD: the reading compiled from 11 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_stops_at_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid : Spec.ledger.batch_stops_at_invalid.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_stops_at_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_stops_at_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-stops-at-invalid
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           5 of 5 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 11 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, every_of, i.stopped_only_at, l.stopped_at, not, l.valid
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, every_of, i.stopped_only_at, l.stopped_at, not, l.valid`:

```lean
def Spec.ledger.batch_stops_at_invalid.reading : Prop :=
  ∀ (balances : List U64),
    Frames.EveryOf ((L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun st inp ans => L.stoppedAt inp ans) (fun st inp x => ¬ ((L.valid st x)))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_stops_at_invalid.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.stopsAtInvalid outcome batch main'
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_stops_at_invalid.lean`):

```lean
theorem Spec.ledger.batch_stops_at_invalid : Spec.ledger.batch_stops_at_invalid.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, -, -, -, hx⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, ledger.Ledger.apply_batch.stops hx⟩
```

</details>

#### PROVED-FOR-ALL: Two batches applied one after the other conserve the total

`features/ledger.feature:54`  id `Spec.ledger.two_batches_conserve`  tags `@id:two_batches_conserve`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <first> to ledger Main, transfer by transfer followed by applying the batch <second> to
            ledger Main, transfer by transfer: every ledger Main, and every batch <first> and every batch <second>; for
            every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the sum of the balances of every account of ledger Main after the call equals the sum of the balances of
            every account of ledger Main before it
            the number of transfers the call reports as applied is at most the number of transfers in the batch <second>
            (of a sequence: every call in it must answer; the answer spoken of is the LAST call's; earlier answers are
            otherwise unconstrained)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Two batches applied one after the other conserve the total
  kernel-checked   theorem Spec.ledger.two_batches_conserve.reading_holds : Spec.ledger.two_batches_conserve.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.two_batches_conserve.reading_iff : Spec.ledger.two_batches_conserve.reading ↔ Spec.ledger.two_batches_conserve.stmt  (NEW ↔ OLD: the reading compiled from 13 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.two_batches_conserve.reading_sat)
  kernel-checked   theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/two_batches_conserve.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.two_batches_conserve.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.apply_batch, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same, LT-at-most
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 13 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, and_then, given, i.holds, is, l.ledger, balances_value, never_changes, result_at_most, aggregate, l.balances_of, l.applied, l.length
  tested           the reading on 88209 generated inputs (8019 in scope): the definition of each frame and its executable reading agree on 16038 of 16038 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, and_then, given, i.holds, is, l.ledger, balances_value, never_changes, result_at_most, aggregate, l.balances_of, l.applied, l.length`:

```lean
def Spec.ledger.two_batches_conserve.reading : Prop :=
  ∀ (balances : List U64),
    Frames.NeverChanges (((L.applyBatch).andThen L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) ∧
    Frames.ResultAtMost (((L.applyBatch).andThen L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun ans => L.applied ans) (fun st inp => L.length inp.2)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/two_batches_conserve.lean`):

```lean
theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt := by
  intro balances first second main _
  obtain ⟨⟨n1, l1⟩, e1, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main first)
  refine ⟨n1, l1, e1, ?_⟩
  obtain ⟨⟨n2, l2⟩, e2, h2, hle, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec l1 second)
  exact ⟨n2, l2, e2, h2.trans h1, hle⟩
```

</details>

### Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, no transfer is applied and the ledger is unchanged

```text
Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, no transfer is applied and the ledger is unchanged   [features/ledger.feature:66]   tags @id:batch_count
  Reading   applies to  clause 1: a batch: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is at most the number of transfers in the
                        batch
                        clause 2: a batch: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    there is a first transfer of the batch, and it can NOT be carried out exactly on the ledger (an
                        account does not exist, or both are the same, or the sender does not cover the amount, or the
                        receiver's balance would pass 2^64 - 1)
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is 0
                        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.ledger.batch_count.holds : Rule.ledger.batch_count.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger.batch_count.from_scenarios : batch_first_invalid.reading →
                             batch_count_bounded.reading → Rule.ledger.batch_count.reading  (generated glue, type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 891 of 891 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 14 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 14 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs; 2 of 2 literal examples proved for their own values
            PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch   [a part: the rule statement is proved from it]
            PROVED-INSTANCE A batch of two valid transfers is applied in full   [an instance: literal values]
            PROVED-INSTANCE A batch stops at its first invalid transfer and keeps what it has applied   [an instance: literal values]
  Examples  8 of 8 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      21 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch, result_at_most, l.applied, l.length, given, result_is, never_changes, the_first,
                 l.transfers, not, l.valid, i.none_applied, zero, l.ledger, i.holds, is, balances_value, becomes,
                 i.exactly_applied, index_count, i.now_holds)
                 4 of 4 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs, 2 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_first_invalid, Spec.ledger.batch_count_bounded, Spec.ledger.batch_example_all,
                 Spec.ledger.batch_example_stop)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.batch_count.reading : Prop :=
  Frames.ResultAtMost L.applyBatch (fun ans => L.applied ans) (fun st inp => L.length inp) ∧
    Frames.ResultIs ((L.applyBatch).given (fun st inp => Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun ans => L.applied ans) (fun st inp => 0) ∧
    Frames.NeverChanges ((L.applyBatch).given (fun st inp => Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun st inp => L.balances st)
```

</details>

#### PROVED-FOR-ALL: A batch whose first transfer is invalid changes nothing

`features/ledger.feature:69`  id `Spec.ledger.batch_first_invalid`  tags `@id:batch_first_invalid`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>;
            for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; there is a first transfer of the batch
            <batch>, and it can NOT be carried out exactly on ledger Main (an account does not exist, or both are the
            same, or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1)
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is 0
            the balances of ledger Main, account by account after the call equals the balances of ledger Main, account
            by account before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection
            within the one Given, Then or Rule clause they occur in
            D6 'the first X of XS is P' requires that there is a first X
```

```text
PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing
  kernel-checked   theorem Spec.ledger.batch_first_invalid.reading_holds : Spec.ledger.batch_first_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_first_invalid.reading_iff : Spec.ledger.batch_first_invalid.reading ↔ Spec.ledger.batch_first_invalid.stmt  (NEW ↔ OLD: the reading compiled from 15 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_first_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/batch_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 15 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, result_is, never_changes, i.none_applied, l.applied, zero
  tested           the reading on 3267 generated inputs (188 in scope): the definition of each frame and its executable reading agree on 376 of 376 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, result_is, never_changes, i.none_applied, l.applied, zero`:

```lean
def Spec.ledger.batch_first_invalid.reading : Prop :=
  ∀ (balances : List U64),
    Frames.ResultIs ((L.applyBatch).given (fun st inp => (L.balances st) = balances ∧ Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun ans => L.applied ans) (fun st inp => 0) ∧
    Frames.NeverChanges ((L.applyBatch).given (fun st inp => (L.balances st) = balances ∧ Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun st inp => L.balances st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_first_invalid.lean`):

```lean
theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt := by
  intro balances batch main _ hfirst
  obtain ⟨⟨n, l'⟩, e, -, -, h3, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  obtain ⟨h0, rfl⟩ := h3 hfirst
  exact ⟨n, _, e, h0, rfl⟩
```

</details>

#### PROVED-FOR-ALL: The number of transfers applied is at most the length of the batch

`features/ledger.feature:83`  id `Spec.ledger.batch_count_bounded`  tags `@id:batch_count_bounded`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>;
            for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is at most the number of transfers in the batch <batch>
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch
  kernel-checked   theorem Spec.ledger.batch_count_bounded.reading_holds : Spec.ledger.batch_count_bounded.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_count_bounded.reading_iff : Spec.ledger.batch_count_bounded.reading ↔ Spec.ledger.batch_count_bounded.stmt  (NEW ↔ OLD: the reading compiled from 9 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_count_bounded.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_count_bounded.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_count_bounded.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-at-most
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_at_most, l.applied, l.length
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_at_most, l.applied, l.length`:

```lean
def Spec.ledger.batch_count_bounded.reading : Prop :=
  ∀ (balances : List U64),
    Frames.ResultAtMost ((L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun ans => L.applied ans) (fun st inp => L.length inp)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_count_bounded.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.appliedAtMost outcome batch
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_count_bounded.lean`):

```lean
theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt := by
  intro balances batch main _
  obtain ⟨⟨n, l'⟩, e, -, h2, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_batch.spec main batch)
  exact ⟨n, l', e, h2⟩
```

</details>

#### PROVED-INSTANCE: A batch of two valid transfers is applied in full

`features/ledger.feature:96`  id `Spec.ledger.batch_example_all`  tags `@id:batch_example_all`

```gherkin
Scenario: A batch of two valid transfers is applied in full
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50] is applied to ledger Main
  Then exactly 2 transfers are applied
  And ledger Main now holds the balances [70, 0, 50]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50] to ledger Main, transfer by transfer: every ledger Main, with the one
            batch [0->1:30, 1->2:50] (a plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is [100, 20, 0]; the input is [0->1:30, 1->2:50]
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is 2
            the balances of ledger Main, account by account after the call is [70, 0, 50]
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  A batch of two valid transfers is applied in full
  kernel-checked   theorem Spec.ledger.batch_example_all.reading_holds : Spec.ledger.batch_example_all.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_example_all.reading_iff : Spec.ledger.batch_example_all.reading ↔ Spec.ledger.batch_example_all.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_example_all.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_example_all : Spec.ledger.batch_example_all.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_all.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_all.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, i.now_holds
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, i.now_holds`:

```lean
def Spec.ledger.batch_example_all.reading : Prop :=
  Frames.ResultIs ((L.applyBatch).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]))) (fun ans => L.applied ans) (fun st inp => (2#usize).val) ∧
    Frames.Becomes ((L.applyBatch).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]))) (fun st inp => L.balances st) (fun st inp => ([70#u64, 0#u64, 50#u64]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_example_all.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]) = ok (outcome, main') ∧
      LVocab.appliedExactly outcome (2#usize) ∧
      LVocab.nowHolds main' ([70#u64, 0#u64, 50#u64])
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_example_all.lean`):

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

</details>

#### PROVED-INSTANCE: A batch stops at its first invalid transfer and keeps what it has applied

`features/ledger.feature:104`  id `Spec.ledger.batch_example_stop`  tags `@id:batch_example_stop`

```gherkin
Scenario: A batch stops at its first invalid transfer and keeps what it has applied
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 2->1:5, 0->1:1] is applied to ledger Main
  Then exactly 1 transfers are applied
  And ledger Main now holds the balances [70, 50, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 2->1:5, 0->1:1] to ledger Main, transfer by transfer: every ledger Main, with
            the one batch [0->1:30, 2->1:5, 0->1:1] (a plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is [100, 20, 0]; the input is [0->1:30, 2->1:5, 0->1:1]
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is 1
            the balances of ledger Main, account by account after the call is [70, 50, 0]
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  A batch stops at its first invalid transfer and keeps what it has applied
  kernel-checked   theorem Spec.ledger.batch_example_stop.reading_holds : Spec.ledger.batch_example_stop.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_example_stop.reading_iff : Spec.ledger.batch_example_stop.reading ↔ Spec.ledger.batch_example_stop.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_example_stop.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_example_stop : Spec.ledger.batch_example_stop.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_stop.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_stop.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, i.now_holds
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, i.now_holds`:

```lean
def Spec.ledger.batch_example_stop.reading : Prop :=
  Frames.ResultIs ((L.applyBatch).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64, ledger.Transfer.mk 0#usize 1#usize 1#u64]))) (fun ans => L.applied ans) (fun st inp => (1#usize).val) ∧
    Frames.Becomes ((L.applyBatch).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64, ledger.Transfer.mk 0#usize 1#usize 1#u64]))) (fun st inp => L.balances st) (fun st inp => ([70#u64, 50#u64, 0#u64]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_example_stop.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64, ledger.Transfer.mk 0#usize 1#usize 1#u64]) = ok (outcome, main') ∧
      LVocab.appliedExactly outcome (1#usize) ∧
      LVocab.nowHolds main' ([70#u64, 50#u64, 0#u64])
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_example_stop.lean`):

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

</details>

### Rule: For a batch for which every transfer of the batch is valid on the ledger, every transfer of the batch is applied

```text
Rule: For a batch for which every transfer of the batch is valid on the ledger, every transfer of the batch is applied   [features/ledger.feature:111]   tags @expect-refuted @id:batch_all_valid
  Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.
  Reading   applies to  a batch: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    every transfer of the batch can be carried out exactly on the ledger (both accounts exist and
                        differ, the sender covers the amount, the receiver's balance stays within 2^64 - 1)
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is the number of transfers in the batch
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
            kernel-checked   theorem Rule.ledger.batch_all_valid.refuted : ¬ Rule.ledger.batch_all_valid.reading; axioms
                             propext, Classical.choice, Quot.sound
            counterexample   ledger = [1, 0], batch = [0->1:1, 0->1:1]
                             at this input the rule does not hold: NOT "the number of transfers the call reports as
                             applied is the number of transfers in the batch"
            tested           searched on 297 generated inputs (63 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 63 of 63 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 9 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A batch of transfers that are each valid on the starting ledger is applied in full   (expected REFUTED)   [beneath the rule; not used to prove it]
  Examples  2 of 2 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      13 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch, given, result_is, every, l.transfers, l.valid, i.all_applied, l.applied, l.length,
                 i.holds, is, l.ledger, balances_value)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 4 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_all_valid_all_applied.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.batch_all_valid.reading : Prop :=
  Frames.ResultIs ((L.applyBatch).given (fun st inp => Frames.every ((L.transfers inp)) (fun x => (L.valid st x)))) (fun ans => L.applied ans) (fun st inp => L.length inp)
```

</details>

#### REFUTED: A batch of transfers that are each valid on the starting ledger is applied in full

`features/ledger.feature:118`  id `Spec.ledger.batch_all_valid_all_applied`  tags `@expect-refuted @id:batch_all_valid_all_applied`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>;
            for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; every transfer of the batch <batch> can be
            carried out exactly on ledger Main (both accounts exist and differ, the sender covers the amount, the
            receiver's balance stays within 2^64 - 1)
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is the number of transfers in the batch <batch>
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection
            within the one Given, Then or Rule clause they occur in
```

```text
REFUTED  A batch of transfers that are each valid on the starting ledger is applied in full
  kernel-checked   theorem Spec.ledger.batch_all_valid_all_applied.reading_iff : Spec.ledger.batch_all_valid_all_applied.reading ↔ Spec.ledger.batch_all_valid_all_applied.stmt  (NEW ↔ OLD: the reading compiled from 13 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_all_valid_all_applied.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_all_valid_all_applied.refuted : ¬ Spec.ledger.batch_all_valid_all_applied.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances | batch            |
                   | [1, 0]   | [0->1:1, 0->1:1] |
                   When the batch [0->1:1, 0->1:1] is applied to ledger Main  =>  returned 1 applied; Main: balances [0, 1]
                   failed Then: "every transfer of [0->1:1, 0->1:1] is applied"
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-all-valid, LW-batch, LT-all-applied
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  tested           boundary grid on the Lean model: 297 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 13 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, every, l.transfers, l.valid, result_is, i.all_applied, l.applied, l.length
  tested           the reading on 3267 generated inputs (63 in scope): the definition of each frame and its executable reading agree on 63 of 63 evaluations; the reading is false at one of them
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, every, l.transfers, l.valid, result_is, i.all_applied, l.applied, l.length`:

```lean
def Spec.ledger.batch_all_valid_all_applied.reading : Prop :=
  ∀ (balances : List U64),
    Frames.ResultIs ((L.applyBatch).given (fun st inp => (L.balances st) = balances ∧ Frames.every ((L.transfers inp)) (fun x => (L.valid st x)))) (fun ans => L.applied ans) (fun st inp => L.length inp)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.batch_all_valid_all_applied.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.allValid main batch →
    ∃ (outcome : Usize) (main' : ledger.Ledger),
      ledger.Ledger.apply_batch main batch = ok (outcome, main') ∧
      LVocab.appliedAll outcome batch
```

</details>

### Rule: A transfer is accepted exactly when the transfer is valid on the ledger, and a rejected transfer never changes the ledger, and for a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed

```text
Rule: A transfer is accepted exactly when the transfer is valid on the ledger, and a rejected transfer never changes the ledger, and for a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed   [features/ledger.feature:130]   tags @id:single_transfer
  Reading   applies to  clause 1: a transfer: every ledger, every transfer
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance if and only if the transfer can be carried out exactly on the ledger
                        (both accounts exist and differ, the sender covers the amount, the receiver's balance stays within
                        2^64 - 1)
                        clause 2: a transfer: every ledger, every transfer
                        ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
                        clause 3: a transfer: every ledger, every transfer
                        ONLY successful calls [asked for]
            assuming    nothing: every state and every input
            then        the balance, in the ledger, of account the sending account of the transfer (0 if there is no such
                        account) after the call, plus the amount of the transfer, equals the balance, in the ledger, of
                        account the sending account of the transfer (0 if there is no such account) before it, exactly
                        the balance, in the ledger, of account the receiving account of the transfer (0 if there is no
                        such account) after the call equals the balance, in the ledger, of account the receiving account
                        of the transfer (0 if there is no such account) before it plus the amount of the transfer, exactly
                        the accounts of the ledger are the same accounts after the call, and every one of them other than
                        the sending account of the transfer and the receiving account of the transfer has the balance it
                        had before
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.ledger.single_transfer.holds : Rule.ledger.single_transfer.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger.single_transfer.from_scenarios : transfer_valid_moves.reading →
                             transfer_invalid_rejected.reading → Rule.ledger.single_transfer.reading  (generated glue,
                             type checked by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (66 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 330 of 330 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 19 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 19 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing   [a part: the rule statement is proved from it]
  Examples  8 of 8 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      29 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply, exactly_when, holds_of, l.the_transfer, l.valid, accepted, rejected, never_changes,
                 l.ledger, successful, decreases_by, increases_by, changes_only, i.moved, l.bal_of, l.sender,
                 l.amount_of, l.receiver, l.accounts, given, i.holds, is, balances_value, always, l.accepted,
                 aggregate, l.balances_of, not, never)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 9 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.transfer_valid_moves, Spec.ledger.transfer_invalid_rejected)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.single_transfer.reading : Prop :=
  Frames.ExactlyWhen L.apply (fun ans => (L.apply).accepted ans) (fun st inp => L.valid st inp) ∧
    Frames.NeverChanges (L.apply).rejected (fun st inp => L.balances st) ∧
    Frames.DecreasesBy (L.apply).successful (fun st inp => L.bal st (L.sender inp)) (fun st inp => L.amountOf inp) ∧
    Frames.IncreasesBy (L.apply).successful (fun st inp => L.bal st (L.receiver inp)) (fun st inp => L.amountOf inp) ∧
    Frames.ChangesOnly (L.apply).successful (fun st => L.accounts st) (fun st k => L.bal st k) (fun st inp => [L.sender inp, L.receiver inp])
```

</details>

#### PROVED-FOR-ALL: A valid transfer is accepted and moves exactly its amount

`features/ledger.feature:133`  id `Spec.ledger.transfer_valid_moves`  tags `@id:transfer_valid_moves`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>; for every value of
            balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the transfer <t> can be carried out exactly
            on ledger Main (both accounts exist and differ, the sender covers the amount, the receiver's balance stays
            within 2^64 - 1)
then        the call gives an answer [default D1]
            the answer is yes (accepted)
            the balance, in ledger Main, of account the sending account of the transfer <t> (0 if there is no such
            account) after the call, plus the amount of the transfer <t>, equals the balance, in ledger Main, of account
            the sending account of the transfer <t> (0 if there is no such account) before it, exactly
            the balance, in ledger Main, of account the receiving account of the transfer <t> (0 if there is no such
            account) after the call equals the balance, in ledger Main, of account the receiving account of the transfer
            <t> (0 if there is no such account) before it plus the amount of the transfer <t>, exactly
            the accounts of ledger Main are the same accounts after the call, and every one of them other than the
            sending account of the transfer <t> and the receiving account of the transfer <t> has the balance it had
            before
            the sum of the balances of every account of ledger Main after the call equals the sum of the balances of
            every account of ledger Main before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount
  kernel-checked   theorem Spec.ledger.transfer_valid_moves.reading_holds : Spec.ledger.transfer_valid_moves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.transfer_valid_moves.reading_iff : Spec.ledger.transfer_valid_moves.reading ↔ Spec.ledger.transfer_valid_moves.stmt  (NEW ↔ OLD: the reading compiled from 23 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.transfer_valid_moves.reading_sat)
  kernel-checked   theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_valid_moves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_valid_moves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 23 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, l.valid, always, decreases_by, increases_by, changes_only, never_changes, l.accepted, i.moved, l.bal_of, l.sender, l.amount_of, l.receiver, l.accounts, aggregate, l.balances_of
  tested           the reading on 726 generated inputs (18 in scope): the definition of each frame and its executable reading agree on 90 of 90 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, l.valid, always, decreases_by, increases_by, changes_only, never_changes, l.accepted, i.moved, l.bal_of, l.sender, l.amount_of, l.receiver, l.accounts, aggregate, l.balances_of`:

```lean
def Spec.ledger.transfer_valid_moves.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Always ((L.apply).given (fun st inp => (L.balances st) = balances ∧ L.valid st inp)) (fun ans => L.said ans) ∧
    Frames.DecreasesBy ((L.apply).given (fun st inp => (L.balances st) = balances ∧ L.valid st inp)) (fun st inp => L.bal st (L.sender inp)) (fun st inp => L.amountOf inp) ∧
    Frames.IncreasesBy ((L.apply).given (fun st inp => (L.balances st) = balances ∧ L.valid st inp)) (fun st inp => L.bal st (L.receiver inp)) (fun st inp => L.amountOf inp) ∧
    Frames.ChangesOnly ((L.apply).given (fun st inp => (L.balances st) = balances ∧ L.valid st inp)) (fun st => L.accounts st) (fun st k => L.bal st k) (fun st inp => [L.sender inp, L.receiver inp]) ∧
    Frames.NeverChanges ((L.apply).given (fun st inp => (L.balances st) = balances ∧ L.valid st inp)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/transfer_valid_moves.lean`):

```lean
theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt := by
  intro balances t main _ hvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨hb, -, hm, ht, -⟩ | ⟨-, hinv, -⟩ := h
  · exact ⟨b, l', e, hb, hm, ht⟩
  · exact absurd hvalid hinv
```

</details>

#### PROVED-FOR-ALL: An invalid transfer is rejected and changes nothing

`features/ledger.feature:148`  id `Spec.ledger.transfer_invalid_rejected`  tags `@id:transfer_invalid_rejected`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>; for every value of
            balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the transfer <t> can NOT be carried out
            exactly on ledger Main (an account does not exist, or both are the same, or the sender does not cover the
            amount, or the receiver's balance would pass 2^64 - 1)
then        the call gives an answer [default D1]
            the answer is no (rejected)
            the balances of ledger Main, account by account after the call equals the balances of ledger Main, account
            by account before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected.reading_holds : Spec.ledger.transfer_invalid_rejected.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected.reading_iff : Spec.ledger.transfer_invalid_rejected.reading ↔ Spec.ledger.transfer_invalid_rejected.stmt  (NEW ↔ OLD: the reading compiled from 14 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.transfer_invalid_rejected.reading_sat)
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_invalid_rejected.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_invalid_rejected.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-invalid, LW-transfer, LT-rejected, LT-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           5 of 5 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 14 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, not, l.valid, never, never_changes, always, l.accepted
  tested           the reading on 726 generated inputs (48 in scope): the definition of each frame and its executable reading agree on 96 of 96 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, not, l.valid, never, never_changes, always, l.accepted`:

```lean
def Spec.ledger.transfer_invalid_rejected.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never ((L.apply).given (fun st inp => (L.balances st) = balances ∧ ¬ ((L.valid st inp)))) (fun ans => L.said ans) ∧
    Frames.NeverChanges ((L.apply).given (fun st inp => (L.balances st) = balances ∧ ¬ ((L.valid st inp)))) (fun st inp => L.balances st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/transfer_invalid_rejected.lean`):

```lean
theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt := by
  intro balances t main _ hinvalid
  obtain ⟨⟨b, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec main t)
  obtain ⟨-, hv, -⟩ | ⟨hb, -, rfl, -⟩ := h
  · exact absurd hv hinvalid
  · exact ⟨b, _, e, hb, rfl⟩
```

</details>

### Rule: A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum

```text
Rule: A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum   [features/ledger.feature:164]   tags @id:total_fits
  Reading   applies to  a computation of the total: every ledger
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance if and only if the sum of the balances of every account of the ledger
                        is at most the largest total that can be reported (2^64 - 1)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (by a hand-written proof)
            kernel-checked   theorem Rule.ledger.total_fits : Rule.ledger.total_fits.reading  (hand-written,
                             lean/Wallet/RuleProofs/ledger/total_fits.lean; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            glue             the generated glue from the scenarios did not go through (the generated proof script failed
                             (see out/links.log))
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 11 generated inputs (11 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 11 of 11 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 7 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 7 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total is the sum of the balances when that fits   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  The total of balances that do not fit is reported as absent   [a part: the rule statement is proved from it]
  Examples  8 of 8 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      23 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.total, exactly_when, at_most_value, aggregate, l.balances_of, l.maximum, accepted, given,
                 i.holds, is, l.ledger, balances_value, i.add_up_to, amount_value, result_is, l.result,
                 amount_result, i.add_up_to_more, exceeds, never, always, not, l.found)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.total_is_sum, Spec.ledger.total_overflow)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.total_fits.reading : Prop :=
  Frames.ExactlyWhen L.total (fun ans => (L.total).accepted ans) (fun st inp => (Frames.aggregate (((L.balances st).map L.amount))) ≤ L.maximum)
```

</details>

#### PROVED-FOR-ALL: The total is the sum of the balances when that fits

`features/ledger.feature:167`  id `Spec.ledger.total_is_sum`  tags `@id:total_is_sum`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  computing the total of ledger Main: every ledger Main; for every value of balances, sum
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the sum of the balances of every account of
            ledger Main is <sum>
then        the call gives an answer [default D1]
            the value the call returns is the value <sum>
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  The total is the sum of the balances when that fits
  kernel-checked   theorem Spec.ledger.total_is_sum.reading_holds : Spec.ledger.total_is_sum.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.total_is_sum.reading_iff : Spec.ledger.total_is_sum.reading ↔ Spec.ledger.total_is_sum.stmt  (NEW ↔ OLD: the reading compiled from 13 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_is_sum.reading_sat)
  kernel-checked   theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/total_is_sum.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_is_sum.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-total, LT-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           5 of 5 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 13 vocabulary pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, i.add_up_to, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result
  tested           the reading on 726 generated inputs (6 in scope): the definition of each frame and its executable reading agree on 6 of 6 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, i.add_up_to, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result`:

```lean
def Spec.ledger.total_is_sum.reading : Prop :=
  ∀ (balances : List U64) (sum : U64),
    Frames.ResultIs ((L.total).given (fun st inp => (L.balances st) = balances ∧ (Frames.aggregate (((L.balances st).map L.amount))) = sum.val)) (fun ans => ans) (fun st inp => some sum)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_is_sum.stmt : Prop :=
  ∀ (balances : List U64) (sum : U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumsTo main sum →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.resultIs outcome sum
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/total_is_sum.lean`):

```lean
theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt := by
  intro balances sum main _ hsum
  obtain ⟨o, e, h1, -⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  obtain ⟨s, rfl, hs⟩ := h1 (by rw [hsum]; scalar_tac)
  refine ⟨_, e, ?_⟩
  simp only [LVocab.resultIs, Option.some.injEq]
  scalar_tac
```

</details>

#### PROVED-FOR-ALL: The total of balances that do not fit is reported as absent

`features/ledger.feature:182`  id `Spec.ledger.total_overflow`  tags `@id:total_overflow`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  computing the total of ledger Main: every ledger Main; for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the sum of the balances of every account of
            ledger Main is strictly more than the largest total that can be reported (2^64 - 1)
then        the call gives an answer [default D1]
            the call returns no value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  The total of balances that do not fit is reported as absent
  kernel-checked   theorem Spec.ledger.total_overflow.reading_holds : Spec.ledger.total_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.total_overflow.reading_iff : Spec.ledger.total_overflow.reading ↔ Spec.ledger.total_overflow.stmt  (NEW ↔ OLD: the reading compiled from 15 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_overflow.reading_sat)
  kernel-checked   theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/total_overflow.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-total, LT-no-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 15 vocabulary pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, i.add_up_to_more, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found
  tested           the reading on 121 generated inputs (3 in scope): the definition of each frame and its executable reading agree on 3 of 3 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, i.add_up_to_more, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found`:

```lean
def Spec.ledger.total_overflow.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never ((L.total).given (fun st inp => (L.balances st) = balances ∧ L.maximum < (Frames.aggregate (((L.balances st).map L.amount))))) (fun ans => L.found ans)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_overflow.stmt : Prop :=
  ∀ (balances : List U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.sumTooBig main →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.noResult outcome
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/total_overflow.lean`):

```lean
theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt := by
  intro balances main _ hbig
  obtain ⟨o, e, -, h2⟩ := Bdd.ok_of_spec (ledger.Ledger.total.spec main)
  exact ⟨o, e, h2 hbig⟩
```

</details>

### Rule: A computation of the total is always accepted

```text
Rule: A computation of the total is always accepted   [features/ledger.feature:195]   tags @expect-refuted @id:total_always
  Deliberately false; the tag is on the rule and on the scenario.
  Reading   applies to  a computation of the total: every ledger
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
            kernel-checked   theorem Rule.ledger.total_always.refuted : ¬ Rule.ledger.total_always.reading; axioms
                             propext, Classical.choice, Quot.sound
            counterexample   ledger = [18446744073709551615, 1]
                             at this input the rule does not hold: NOT "the answer is an acceptance"
            tested           searched on 11 generated inputs (11 in scope): counterexample found; the definition of each
                             frame and its executable reading agree on 11 of 11 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 3 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 3 vocabulary pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         The total of a ledger can always be computed   (expected REFUTED)   [beneath the rule; not used to prove it]
  Examples  2 of 2 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      9 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.total, always, accepted, given, i.holds, is, l.ledger, balances_value, l.found)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 3 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 1 refutation (the scenario is false); axioms: propext, Classical.choice,
                 Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.total_always_available.refuted)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.total_always.reading : Prop :=
  Frames.Always L.total (fun ans => (L.total).accepted ans)
```

</details>

#### REFUTED: The total of a ledger can always be computed

`features/ledger.feature:200`  id `Spec.ledger.total_always_available`  tags `@expect-refuted @id:total_always_available`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  computing the total of ledger Main: every ledger Main; for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the call returns a value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
REFUTED  The total of a ledger can always be computed
  kernel-checked   theorem Spec.ledger.total_always_available.reading_iff : Spec.ledger.total_always_available.reading ↔ Spec.ledger.total_always_available.stmt  (NEW ↔ OLD: the reading compiled from 8 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_always_available.reading_sat)
  kernel-checked   theorem Spec.ledger.total_always_available.refuted : ¬ Spec.ledger.total_always_available.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances                  |
                   | [18446744073709551615, 1] |
                   When the total of ledger Main is computed  =>  returned None
                   failed Then: "there is a result"
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-total, LT-some-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  tested           boundary grid on the Lean model: 11 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 8 vocabulary pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, always, l.found
  tested           the reading on 121 generated inputs (11 in scope): the definition of each frame and its executable reading agree on 11 of 11 evaluations; the reading is false at one of them
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, always, l.found`:

```lean
def Spec.ledger.total_always_available.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Always ((L.total).given (fun st inp => (L.balances st) = balances)) (fun ans => L.found ans)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.total_always_available.stmt : Prop :=
  ∀ (balances : List U64) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Option U64),
      ledger.Ledger.total main = ok (outcome) ∧
      LVocab.someResult outcome
```

</details>

### Rule: For a lookup, the result is the balance of the account in the ledger

```text
Rule: For a lookup, the result is the balance of the account in the ledger   [features/ledger.feature:211]   tags @id:lookup
  Reading   applies to  a lookup: every ledger, every account
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the value the call returns is the balance of account the account of the ledger before the call
                        (absent if there is no such account)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.ledger.lookup.holds : Rule.ledger.lookup.reading  (THE RULE STATEMENT ITSELF,
                             as one theorem; type checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger.lookup.from_scenarios : balance_of_account.reading →
                             balance_no_account.reading → Rule.ledger.lookup.reading  (generated glue, type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 2 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 55 generated inputs (55 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 55 of 55 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 4 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 4 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Looking up an existing account gives its balance   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Looking up an account that does not exist gives nothing   [a part: the rule statement is proved from it]
  Examples  4 of 4 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      14 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup, result_is, l.result, l.balance_at, given, i.holds, is, l.ledger, balances_value,
                 l.is_account, not, never, always, l.found)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.balance_of_account, Spec.ledger.balance_no_account)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.lookup.reading : Prop :=
  Frames.ResultIs L.lookup (fun ans => ans) (fun st inp => L.balanceAt st inp)
```

</details>

#### PROVED-FOR-ALL: Looking up an existing account gives its balance

`features/ledger.feature:214`  id `Spec.ledger.balance_of_account`  tags `@id:balance_of_account`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  looking up the balance of account <i> of ledger Main: every ledger Main, and every account <i>; for every
            value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; <i> is an account number of ledger Main
then        the call gives an answer [default D1]
            the value the call returns is the balance of account <i> of ledger Main before the call (absent if there is
            no such account)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Looking up an existing account gives its balance
  kernel-checked   theorem Spec.ledger.balance_of_account.reading_holds : Spec.ledger.balance_of_account.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.balance_of_account.reading_iff : Spec.ledger.balance_of_account.reading ↔ Spec.ledger.balance_of_account.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.balance_of_account.reading_sat)
  kernel-checked   theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_of_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_of_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-account, LW-balance, LT-balance
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: l.lookup, given, i.holds, is, l.ledger, balances_value, l.is_account, result_is, l.result, l.balance_at
  tested           the reading on 605 generated inputs (24 in scope): the definition of each frame and its executable reading agree on 24 of 24 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.lookup, given, i.holds, is, l.ledger, balances_value, l.is_account, result_is, l.result, l.balance_at`:

```lean
def Spec.ledger.balance_of_account.reading : Prop :=
  ∀ (balances : List U64),
    Frames.ResultIs ((L.lookup).given (fun st inp => (L.balances st) = balances ∧ L.isAccount st inp)) (fun ans => ans) (fun st inp => L.balanceAt st inp)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.balance_of_account.stmt : Prop :=
  ∀ (balances : List U64) (i : Usize) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.isAccount main i →
    ∃ (outcome : Option U64),
      ledger.Ledger.balance main i = ok (outcome) ∧
      LVocab.resultIsBalance outcome main i
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/balance_of_account.lean`):

```lean
theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt := by
  intro balances i main _ hacc
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec main i)
  refine ⟨o, e, h, ?_⟩
  simp_all [LVocab.isAccount]
```

</details>

#### PROVED-FOR-ALL: Looking up an account that does not exist gives nothing

`features/ledger.feature:226`  id `Spec.ledger.balance_no_account`  tags `@id:balance_no_account`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  looking up the balance of account <i> of ledger Main: every ledger Main, and every account <i>; for every
            value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; <i> is NOT an account number of ledger Main
then        the call gives an answer [default D1]
            the call returns no value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Looking up an account that does not exist gives nothing
  kernel-checked   theorem Spec.ledger.balance_no_account.reading_holds : Spec.ledger.balance_no_account.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.balance_no_account.reading_iff : Spec.ledger.balance_no_account.reading ↔ Spec.ledger.balance_no_account.stmt  (NEW ↔ OLD: the reading compiled from 11 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.balance_no_account.reading_sat)
  kernel-checked   theorem Spec.ledger.balance_no_account : Spec.ledger.balance_no_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_no_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_no_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-no-account, LW-balance, LT-no-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 11 vocabulary pieces signed off by anyone - UNREVIEWED: l.lookup, given, i.holds, is, l.ledger, balances_value, not, l.is_account, never, always, l.found
  tested           the reading on 605 generated inputs (31 in scope): the definition of each frame and its executable reading agree on 31 of 31 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.lookup, given, i.holds, is, l.ledger, balances_value, not, l.is_account, never, always, l.found`:

```lean
def Spec.ledger.balance_no_account.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never ((L.lookup).given (fun st inp => (L.balances st) = balances ∧ ¬ ((L.isAccount st inp)))) (fun ans => L.found ans)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.balance_no_account.stmt : Prop :=
  ∀ (balances : List U64) (i : Usize) (main : ledger.Ledger),
    LVocab.holds main balances →
    LVocab.notAccount main i →
    ∃ (outcome : Option U64),
      ledger.Ledger.balance main i = ok (outcome) ∧
      LVocab.noResult outcome
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/balance_no_account.lean`):

```lean
theorem Spec.ledger.balance_no_account : Spec.ledger.balance_no_account.stmt := by
  intro balances i main _ hnone
  obtain ⟨o, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.balance.spec main i)
  refine ⟨o, e, ?_⟩
  simp_all [LVocab.notAccount]
```

</details>

### Rule: A rejected batch applied as a whole never changes the ledger, and a batch applied as a whole never changes the total of all balances of the ledger

```text
Rule: A rejected batch applied as a whole never changes the ledger, and a batch applied as a whole never changes the total of all balances of the ledger   [features/ledger.feature:238]   tags @id:whole_batch
  Reading   applies to  clause 1: a batch applied as a whole: every ledger, every batch
                        ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
                        clause 2: a batch applied as a whole: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the sum of the balances of every account of the ledger after the call equals the sum of the
                        balances of every account of the ledger before it
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
            kernel-checked   theorem Rule.ledger.whole_batch.holds : Rule.ledger.whole_batch.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger.whole_batch.from_scenarios : whole_rejected_unchanged.reading →
                             whole_first_invalid.reading → whole_conserves.reading → Rule.ledger.whole_batch.reading
                             (generated glue, type checked by the audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 3 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 594 of 594 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 6 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 6 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 3 of 3 literal examples proved for their own values
            PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances   [a part: the rule statement is proved from it]
            PROVED-INSTANCE A batch of valid transfers applied as a whole is accepted and applied   [an instance: literal values]
            PROVED-INSTANCE A batch applied as a whole is rolled back when its third transfer is invalid   [an instance: literal values]
            PROVED-INSTANCE A batch applied as a whole is rolled back when a later transfer is invalid   [an instance: literal values]
  Examples  10 of 10 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      20 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_all, rejected, never_changes, l.ledger, aggregate, l.balances_of, given, i.holds, is,
                 balances_value, always_answers, the_first, l.transfers, not, l.valid, never, always, l.accepted,
                 becomes, i.now_holds)
                 6 of 6 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 9 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 3 theorems for all inputs, 3 for literal values only; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Spec.ledger.whole_rejected_unchanged, Spec.ledger.whole_first_invalid, Spec.ledger.whole_conserves,
                 Spec.ledger.whole_example_accept, Spec.ledger.whole_example_rollback_late,
                 Spec.ledger.whole_example_rollback)
    translation  Lean model ledger.Ledger.apply_all generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.whole_batch.reading : Prop :=
  Frames.NeverChanges (L.applyAll).rejected (fun st inp => L.balances st) ∧
    Frames.NeverChanges L.applyAll (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### PROVED-FOR-ALL: A batch applied as a whole that is rejected leaves the ledger unchanged

`features/ledger.feature:243`  id `Spec.ledger.whole_rejected_unchanged`  tags `@id:whole_rejected_unchanged`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch>; for every
            value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            if the call is rejected: the balances of ledger Main, account by account after the call equals the balances
            of ledger Main, account by account before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or
            that give no answer, are outside this clause
```

```text
PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged.reading_holds : Spec.ledger.whole_rejected_unchanged.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged.reading_iff : Spec.ledger.whole_rejected_unchanged.reading ↔ Spec.ledger.whole_rejected_unchanged.stmt  (NEW ↔ OLD: the reading compiled from 9 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_rejected_unchanged.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_rejected_unchanged.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_rejected_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-same-if-rejected
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           4 of 4 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, rejected, always_answers, never_changes
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 594 of 594 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, rejected, always_answers, never_changes`:

```lean
def Spec.ledger.whole_rejected_unchanged.reading : Prop :=
  ∀ (balances : List U64),
    Frames.AlwaysAnswers ((L.applyAll).given (fun st inp => (L.balances st) = balances)) ∧
    Frames.NeverChanges (((L.applyAll).given (fun st inp => (L.balances st) = balances)).rejected) (fun st inp => L.balances st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_rejected_unchanged.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main batch = ok (outcome, main') ∧
      LVocab.unchangedIfRejected outcome main main'
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_rejected_unchanged.lean`):

```lean
theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, -, hback, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, fun hb => congrArg (·.balances.val) (hback hb)⟩
```

</details>

#### PROVED-FOR-ALL: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing

`features/ledger.feature:256`  id `Spec.ledger.whole_first_invalid`  tags `@id:whole_first_invalid`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch>; for every
            value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; there is a first transfer of the batch
            <batch>, and it can NOT be carried out exactly on ledger Main (an account does not exist, or both are the
            same, or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1)
then        the call gives an answer [default D1]
            the answer is no (rejected)
            the balances of ledger Main, account by account after the call equals the balances of ledger Main, account
            by account before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection
            within the one Given, Then or Rule clause they occur in
            D6 'the first X of XS is P' requires that there is a first X
```

```text
PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.whole_first_invalid.reading_holds : Spec.ledger.whole_first_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_first_invalid.reading_iff : Spec.ledger.whole_first_invalid.reading ↔ Spec.ledger.whole_first_invalid.stmt  (NEW ↔ OLD: the reading compiled from 14 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_first_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_first_invalid : Spec.ledger.whole_first_invalid.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/whole_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-whole, LT-rejected, LT-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 14 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, never, never_changes, always, l.accepted
  tested           the reading on 3267 generated inputs (188 in scope): the definition of each frame and its executable reading agree on 376 of 376 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, never, never_changes, always, l.accepted`:

```lean
def Spec.ledger.whole_first_invalid.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never ((L.applyAll).given (fun st inp => (L.balances st) = balances ∧ Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun ans => L.said ans) ∧
    Frames.NeverChanges ((L.applyAll).given (fun st inp => (L.balances st) = balances ∧ Frames.theFirst ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun st inp => L.balances st)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_first_invalid.lean`):

```lean
theorem Spec.ledger.whole_first_invalid : Spec.ledger.whole_first_invalid.stmt := by
  intro balances batch main _ hfirst
  obtain ⟨⟨b, l'⟩, e, -, h2, h3, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  have hb := h3 hfirst
  obtain rfl := h2 hb
  exact ⟨b, _, e, hb, rfl⟩
```

</details>

#### PROVED-FOR-ALL: Applying a batch as a whole conserves the total of all balances

`features/ledger.feature:268`  id `Spec.ledger.whole_conserves`  tags `@id:whole_conserves`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch>; for every
            value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the sum of the balances of every account of ledger Main after the call equals the sum of the balances of
            every account of ledger Main before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances
  kernel-checked   theorem Spec.ledger.whole_conserves.reading_holds : Spec.ledger.whole_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_conserves.reading_iff : Spec.ledger.whole_conserves.reading ↔ Spec.ledger.whole_conserves.stmt  (NEW ↔ OLD: the reading compiled from 9 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_conserves.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-total-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of`:

```lean
def Spec.ledger.whole_conserves.reading : Prop :=
  ∀ (balances : List U64),
    Frames.NeverChanges ((L.applyAll).given (fun st inp => (L.balances st) = balances)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_conserves.stmt : Prop :=
  ∀ (balances : List U64) (batch : Slice ledger.Transfer) (main : ledger.Ledger),
    LVocab.holds main balances →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main batch = ok (outcome, main') ∧
      LVocab.totalUnchanged main main'
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_conserves.lean`):

```lean
theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt := by
  intro balances batch main _
  obtain ⟨⟨b, l'⟩, e, h1, -, -⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main batch)
  exact ⟨b, l', e, h1⟩
```

</details>

#### PROVED-INSTANCE: A batch of valid transfers applied as a whole is accepted and applied

`features/ledger.feature:280`  id `Spec.ledger.whole_example_accept`  tags `@id:whole_example_accept`

```gherkin
Scenario: A batch of valid transfers applied as a whole is accepted and applied
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50] is applied to ledger Main as a whole
  Then it is accepted
  And ledger Main now holds the balances [70, 0, 50]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50] to ledger Main as a whole: every ledger Main, with the one batch
            [0->1:30, 1->2:50] (a plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is [100, 20, 0]; the input is [0->1:30, 1->2:50]
then        the call gives an answer [default D1]
            the answer is yes (accepted)
            the balances of ledger Main, account by account after the call is [70, 0, 50]
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  A batch of valid transfers applied as a whole is accepted and applied
  kernel-checked   theorem Spec.ledger.whole_example_accept.reading_holds : Spec.ledger.whole_example_accept.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_accept.reading_iff : Spec.ledger.whole_example_accept.reading ↔ Spec.ledger.whole_example_accept.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_accept.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_accept : Spec.ledger.whole_example_accept.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/whole_example_accept.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_accept.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-accepted, LT-now-holds
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, always, becomes, l.accepted, i.now_holds
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, always, becomes, l.accepted, i.now_holds`:

```lean
def Spec.ledger.whole_example_accept.reading : Prop :=
  Frames.Always ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]))) (fun ans => L.said ans) ∧
    Frames.Becomes ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]))) (fun st inp => L.balances st) (fun st inp => ([70#u64, 0#u64, 50#u64]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_accept.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64]) = ok (outcome, main') ∧
      LVocab.accepted outcome ∧
      LVocab.nowHolds main' ([70#u64, 0#u64, 50#u64])
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_example_accept.lean`):

```lean
theorem Spec.ledger.whole_example_accept : Spec.ledger.whole_example_accept.stmt := by
  intro main h
  -- literal values: the pure model `runN` applies both transfers, so the batch is accepted
  obtain ⟨⟨b, l'⟩, e, -, -, -, hx, hy⟩ := Bdd.ok_of_spec (ledger.Ledger.apply_all.spec main _)
  refine ⟨b, l', e, ?_⟩
  simp [ledger.nums, h, LVocab.mkBatch_val, ledger.runN, ledger.stepN, U64.max, U64.numBits] at hx hy
  exact ⟨hx, ledger.holds_of_nums (by simpa [ledger.nums] using hy hx)⟩
```

</details>

#### PROVED-INSTANCE: A batch applied as a whole is rolled back when its third transfer is invalid

`features/ledger.feature:289`  id `Spec.ledger.whole_example_rollback_late`  tags `@id:whole_example_rollback_late`

```gherkin
Scenario: A batch applied as a whole is rolled back when its third transfer is invalid
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 1->2:50, 2->0:60] is applied to ledger Main as a whole
  Then it is rejected
  And ledger Main now holds the balances [100, 20, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50, 2->0:60] to ledger Main as a whole: every ledger Main, with the one
            batch [0->1:30, 1->2:50, 2->0:60] (a plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is [100, 20, 0]; the input is [0->1:30, 1->2:50, 2->0:60]
then        the call gives an answer [default D1]
            the answer is no (rejected)
            the balances of ledger Main, account by account after the call is [100, 20, 0]
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when its third transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late.reading_holds : Spec.ledger.whole_example_rollback_late.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late.reading_iff : Spec.ledger.whole_example_rollback_late.reading ↔ Spec.ledger.whole_example_rollback_late.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_rollback_late.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late : Spec.ledger.whole_example_rollback_late.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback_late.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback_late.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, i.now_holds
  tested           the reading on 12 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, i.now_holds`:

```lean
def Spec.ledger.whole_example_rollback_late.reading : Prop :=
  Frames.Never ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64, ledger.Transfer.mk 2#usize 0#usize 60#u64]))) (fun ans => L.said ans) ∧
    Frames.Becomes ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64, ledger.Transfer.mk 2#usize 0#usize 60#u64]))) (fun st inp => L.balances st) (fun st inp => ([100#u64, 20#u64, 0#u64]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_rollback_late.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 1#usize 2#usize 50#u64, ledger.Transfer.mk 2#usize 0#usize 60#u64]) = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.nowHolds main' ([100#u64, 20#u64, 0#u64])
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_example_rollback_late.lean`):

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

</details>

#### PROVED-INSTANCE: A batch applied as a whole is rolled back when a later transfer is invalid

`features/ledger.feature:297`  id `Spec.ledger.whole_example_rollback`  tags `@id:whole_example_rollback`

```gherkin
Scenario: A batch applied as a whole is rolled back when a later transfer is invalid
  Given ledger Main holds the balances [100, 20, 0]
  When the batch [0->1:30, 2->1:5] is applied to ledger Main as a whole
  Then it is rejected
  And ledger Main now holds the balances [100, 20, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 2->1:5] to ledger Main as a whole: every ledger Main, with the one batch
            [0->1:30, 2->1:5] (a plain Scenario: the values are the literals written in it)
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is [100, 20, 0]; the input is [0->1:30, 2->1:5]
then        the call gives an answer [default D1]
            the answer is no (rejected)
            the balances of ledger Main, account by account after the call is [100, 20, 0]
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when a later transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback.reading_holds : Spec.ledger.whole_example_rollback.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_rollback.reading_iff : Spec.ledger.whole_example_rollback.reading ↔ Spec.ledger.whole_example_rollback.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_rollback.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_rollback : Spec.ledger.whole_example_rollback.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, i.now_holds
  tested           the reading on 12 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, i.now_holds`:

```lean
def Spec.ledger.whole_example_rollback.reading : Prop :=
  Frames.Never ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64]))) (fun ans => L.said ans) ∧
    Frames.Becomes ((L.applyAll).given (fun st inp => (L.balances st) = ([100#u64, 20#u64, 0#u64]) ∧ inp = (L.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64]))) (fun st inp => L.balances st) (fun st inp => ([100#u64, 20#u64, 0#u64]))
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

```lean
def Spec.ledger.whole_example_rollback.stmt : Prop :=
  ∀ (main : ledger.Ledger),
    LVocab.holds main ([100#u64, 20#u64, 0#u64]) →
    ∃ (outcome : Bool) (main' : ledger.Ledger),
      ledger.Ledger.apply_all main (LVocab.mkBatch [ledger.Transfer.mk 0#usize 1#usize 30#u64, ledger.Transfer.mk 2#usize 1#usize 5#u64]) = ok (outcome, main') ∧
      LVocab.rejected outcome ∧
      LVocab.nowHolds main' ([100#u64, 20#u64, 0#u64])
```

Proof of the flat statement (`lean/Wallet/Proofs/ledger/whole_example_rollback.lean`):

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

</details>

### Rule: A batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum

```text
Rule: A batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum   [features/ledger.feature:304]   tags @id:batch_then_total
  Reading   applies to  a batch followed by a computation of the total: every ledger, every batch
                        every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance if and only if the sum of the balances of every account of the ledger
                        is at most the largest total that can be reported (2^64 - 1)
                        (of a sequence: every call in it must answer; the answer spoken of is the LAST call's)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
  Verdict   PROVED FOR ALL INPUTS (by a hand-written proof)
            kernel-checked   theorem Rule.ledger.batch_then_total : Rule.ledger.batch_then_total.reading  (hand-written,
                             lean/Wallet/RuleProofs/ledger/batch_then_total.lean; type checked by the audit); axioms
                             propext, Classical.choice, Quot.sound
            glue             no glue from the scenarios was generated: no universal scenario beneath the rule is about
                             one operation with nothing pinned
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tool-trusted     rule line compiled by slicegen 0dbb98484692 (slicegen-rule/4) from 9 vocabulary pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 9 vocabulary pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits   [beneath the rule; not used to prove it]
            PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before   [beneath the rule; not used to prove it]
  Examples  5 of 5 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      25 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch, l.total, and_then, exactly_when, at_most_value, aggregate, l.balances_of, l.maximum,
                 accepted, given, i.holds, is, l.ledger, balances_value, i.add_up_to, amount_value, result_is,
                 l.result, amount_result, i.add_up_to_more, exceeds, never, always, not, l.found)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 7 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 2 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound
                 (the standard three only)   [kernel-checked]
                 (Spec.ledger.batch_then_total, Spec.ledger.batch_then_total_overflow)
    translation  Lean models ledger.Ledger.apply_batch, ledger.Ledger.total generated from ledger/src/lib.rs by
                 charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger.batch_then_total.reading : Prop :=
  Frames.ExactlyWhen ((L.applyBatch).andThen L.total) (fun ans => ((L.applyBatch).andThen L.total).accepted ans) (fun st inp => (Frames.aggregate (((L.balances st).map L.amount))) ≤ L.maximum)
```

</details>

#### PROVED-FOR-ALL: The total computed after any batch is the total before it, when that total fits

`features/ledger.feature:311`  id `Spec.ledger.batch_then_total`  tags `@id:batch_then_total`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer followed by computing the total of ledger
            Main: every ledger Main, and every batch <batch>; for every value of balances, sum
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the sum of the balances of every account of
            ledger Main is <sum>
then        the call gives an answer [default D1]
            the value the call returns is the value <sum>
            (of a sequence: every call in it must answer; the answer spoken of is the LAST call's; earlier answers are
            otherwise unconstrained)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits
  kernel-checked   theorem Spec.ledger.batch_then_total.reading_holds : Spec.ledger.batch_then_total.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_then_total.reading_iff : Spec.ledger.batch_then_total.reading ↔ Spec.ledger.batch_then_total.stmt  (NEW ↔ OLD: the reading compiled from 15 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_then_total.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt (type checked by the audit; 10-line proof, lean/Wallet/Proofs/ledger/batch_then_total.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-batch, LW-total, LT-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           3 of 3 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 15 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, i.add_up_to, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result
  tested           the reading on 19602 generated inputs (162 in scope): the definition of each frame and its executable reading agree on 162 of 162 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, i.add_up_to, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result`:

```lean
def Spec.ledger.batch_then_total.reading : Prop :=
  ∀ (balances : List U64) (sum : U64),
    Frames.ResultIs (((L.applyBatch).andThen L.total).given (fun st inp => (L.balances st) = balances ∧ (Frames.aggregate (((L.balances st).map L.amount))) = sum.val)) (fun ans => ans) (fun st inp => some sum)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_then_total.lean`):

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

</details>

#### PROVED-FOR-ALL: The total computed after any batch is still absent when it did not fit before

`features/ledger.feature:326`  id `Spec.ledger.batch_then_total_overflow`  tags `@id:batch_then_total_overflow`

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer followed by computing the total of ledger
            Main: every ledger Main, and every batch <batch>; for every value of balances
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the sum of the balances of every account of
            ledger Main is strictly more than the largest total that can be reported (2^64 - 1)
then        the call gives an answer [default D1]
            the call returns no value
            (of a sequence: every call in it must answer; the answer spoken of is the LAST call's; earlier answers are
            otherwise unconstrained)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow.reading_holds : Spec.ledger.batch_then_total_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow.reading_iff : Spec.ledger.batch_then_total_overflow.reading ↔ Spec.ledger.batch_then_total_overflow.stmt  (NEW ↔ OLD: the reading compiled from 17 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_then_total_overflow.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow : Spec.ledger.batch_then_total_overflow.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_then_total_overflow.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-batch, LW-total, LT-no-result
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           2 of 2 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 17 vocabulary pieces signed off by anyone - UNREVIEWED: l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, i.add_up_to_more, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found
  tested           the reading on 3267 generated inputs (81 in scope): the definition of each frame and its executable reading agree on 81 of 81 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, i.add_up_to_more, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found`:

```lean
def Spec.ledger.batch_then_total_overflow.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never (((L.applyBatch).andThen L.total).given (fun st inp => (L.balances st) = balances ∧ L.maximum < (Frames.aggregate (((L.balances st).map L.amount))))) (fun ans => L.found ans)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/ledger/batch_then_total_overflow.lean`):

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

</details>

### (scenarios of `Feature: Negative controls` that are not under a Rule)

```text
(scenarios of `Feature: Negative controls` that are not under a Rule)   [features/negative.feature]   tags @control
  Scenarios SOME SCENARIOS PROVED: 1 of 2 universal scenarios proved for all inputs
            VACUOUS         A withdrawal that is both covered and not covered   (expected VACUOUS)
            PROVED-FOR-ALL  A deposit does not touch a bystander
  Examples  1 of 2 pass on the Lean model; not run on the compiled Rust in this run
  Suite     not computed: the adequacy search did not run (./run.sh --no-adequacy, or an earlier step failed)

  Rests on
    meaning      15 vocabulary pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.withdraw, given, i.has_balance, is, w.balance, amount_value, more_than, not_more_than, always,
                 w.succeeds, w.deposit, beside, sum_within, w.maximum, never_changes)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements and the Rust steps still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 1 theorem for all inputs, 1 proof that the Givens contradict each other
                 (the scenario is true of nothing); axioms: propext, Classical.choice, Quot.sound (the standard three
                 only)   [kernel-checked]
                 (Spec.negative_controls.bystander_unchanged, Spec.negative_controls.contradictory_givens.unsat)
    translation  Lean models wallet.Wallet.withdraw, wallet.Wallet.deposit generated from wallet/src/lib.rs by charon
                 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 not cross-checked in this run: no example row was run on both the compiled Rust and the model
    compilation  the compiled Rust was not exercised in this run
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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount>; for every value of a
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; <amount> is strictly more than the balance of Alice; <amount> is at most the
            balance of Alice
then        the call gives an answer [default D1]
            the answer is Ok
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
VACUOUS  A withdrawal that is both covered and not covered
  kernel-checked   theorem Spec.negative_controls.contradictory_givens.reading_iff : Spec.negative_controls.contradictory_givens.reading ↔ Spec.negative_controls.contradictory_givens.stmt  (NEW ↔ OLD: the reading compiled from 10 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.negative_controls.contradictory_givens.unsat: no input satisfies all the Givens; axioms propext, Quot.sound
  meaning          the scenario is true of nothing; any proof of it would be worthless
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, G-covers, W-withdraw, T-ok
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           0 of 1 rows pass on the Lean model; cucumber-rs did not run
  NOT ASSERTED     0 of 10 vocabulary pieces signed off by anyone - UNREVIEWED: w.withdraw, given, i.has_balance, is, w.balance, amount_value, more_than, not_more_than, always, w.succeeds
  tested           the reading on 216 generated inputs (0 in scope): the definition of each frame and its executable reading agree on 0 of 0 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, i.has_balance, is, w.balance, amount_value, more_than, not_more_than, always, w.succeeds`:

```lean
def Spec.negative_controls.contradictory_givens.reading : Prop :=
  ∀ (a : U64),
    Frames.Always ((W.withdraw).given (fun st inp => (W.balance st) = a.val ∧ (W.balance st) < inp.val ∧ inp.val ≤ (W.balance st))) (fun ans => W.accepted ans)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

</details>

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

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount>; for every value of a, b
            beside it: Bob (named, but not passed to the operation, so unchanged by construction)
            every such call, accepted or rejected [default D2]
assuming    the balance of Alice is <a>; the balance of Bob is <b>; the balance of Alice plus <amount> is at most the
            largest balance a wallet can hold (2^64 - 1)
then        the call gives an answer [default D1]
            the answer is Ok
            the balance of Bob after the call equals the balance of Bob before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

```text
PROVED-FOR-ALL (1 of 2 Thens substantive)  A deposit does not touch a bystander
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged.reading_holds : Spec.negative_controls.bystander_unchanged.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged.reading_iff : Spec.negative_controls.bystander_unchanged.reading ↔ Spec.negative_controls.bystander_unchanged.stmt  (NEW ↔ OLD: the reading compiled from 12 vocabulary pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.negative_controls.bystander_unchanged.reading_sat)
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/negative_controls/bystander_unchanged.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.negative_controls.bystander_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by slicegen 0dbb98484692 (slicegen-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-same
  not compared     the two readings of each phrase (Lean definition, Rust predicate): cucumber-rs did not run
  tested           1 of 1 rows pass on the Lean model; cucumber-rs did not run
  flag             TRIVIAL-THEN: follows from the Givens alone, whatever the code does: "Bob's balance is unchanged"
  flag             FRAME-TRIVIAL: the call does not return this actor, so the Then compares it with itself: "Bob's balance is unchanged"
  NOT ASSERTED     0 of 12 vocabulary pieces signed off by anyone - UNREVIEWED: w.deposit, beside, given, i.has_balance, is, w.balance, amount_value, sum_within, w.maximum, always, never_changes, w.succeeds
  tested           the reading on 7776 generated inputs (126 in scope): the definition of each frame and its executable reading agree on 252 of 252 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, beside, given, i.has_balance, is, w.balance, amount_value, sum_within, w.maximum, always, never_changes, w.succeeds`:

```lean
def Spec.negative_controls.bystander_unchanged.reading : Prop :=
  ∀ (a b : U64),
    Frames.Always (((W.deposit).beside wallet.Wallet).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ (W.balance st.1) + inp.val ≤ W.maximum)) (fun ans => W.accepted ans) ∧
    Frames.NeverChanges (((W.deposit).beside wallet.Wallet).given (fun st inp => (W.balance st.1) = a.val ∧ (W.balance st.2) = b.val ∧ (W.balance st.1) + inp.val ≤ W.maximum)) (fun st inp => W.balance st.2)
```

Flat statement of the old whole-phrase glossary (`lean/Wallet/Statements.lean`):

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

Proof of the flat statement (`lean/Wallet/Proofs/negative_controls/bystander_unchanged.lean`):

```lean
theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt := by
  intro a b amount alice bob h1 h2 h3
  apply Bdd.ok2_of_spec
  unfold wallet.Wallet.deposit
  step*
```

</details>

## The frame library

Shared and project-independent: `lean/Frames/` imports nothing but Lean's core. A frame is a statement shape about ONE call of an abstract operation (a state, an input, and either an answer with the state afterwards, or no answer). Its holes are typed (a measure, a value known before the call, a condition, a class of answers, a named collection, a condition on an item, a relation between two inputs), so no frame takes an arbitrary relation between before and after. Each frame has three things:

- **(a) a Lean definition** (`lean/Frames/Frames.lean`), with the fail-closed defaults written once, in `Frames.Op.HoldsAt`;
- **(b) a fixed English paraphrase** with slots, used for the echo (`vocabulary.yaml`, `echo:`);
- **(c) an independent executable reading** (`lean/Frames/Check.lean`): run the call, then case on what came back. The definition and the executable reading are evaluated side by side on generated inputs for the concrete operations (`lean/Run/ReadingSearch.lean`; NASA FRET's practice of two semantics per template). A disagreement fails the run.

| # | Frame | Lean definition | English paraphrase (slots in braces) | Executable reading | Definition vs executable reading |
|---|---|---|---|---|---|
| 1 | `always_answers` | `@[reducible] def AlwaysAnswers.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ _ _ => True) s a` | the call gives an answer | `Frames.Check.alwaysAnswers` | agree on 369 evaluations in 3 readings of the fixtures; agree on 330 evaluations in 1 new sentences (`heldout/`) |
| 2 | `never_changes` | `@[reducible] def NeverChanges.at (op : Op σ α ρ) (m : Measure σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a) s a` | {m} after the call equals {m} before it | `Frames.Check.neverChanges` | agree on 11519 evaluations in 23 readings of the fixtures; agree on 1072 evaluations in 5 new sentences (`heldout/`) |
| 3 | `changes_only` | `@[reducible] def ChangesOnly.at (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => parts s' = parts s ∧ ∀ k ∈ parts s, k ∉ X s a → m s' k = m s k) s a` | {c} are the same accounts after the call, and every one of them other than {xs} has the balance it had before | `Frames.Check.changesOnly` | agree on 84 evaluations in 2 readings of the fixtures |
| 4 | `always` | `@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => cls r) s a` | {c} | `Frames.Check.always` | agree on 708 evaluations in 15 readings of the fixtures |
| 4 | `never` | `@[reducible] def Never.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => ¬ cls r) s a` | it is NOT the case that {c} | `Frames.Check.never` | agree on 353 evaluations in 7 readings of the fixtures; agree on 31 evaluations in 1 new sentences (`heldout/`) |
| 5 | `if_then` | `@[reducible] def IfThen.at (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := Always.at (op.given C) cls s a` | if {k}, then {c} | `Frames.Check.ifThen` | agree on 102 evaluations in 2 new sentences (`heldout/`) |
| 6 | `only_if` | `@[reducible] def OnlyIf.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r → C s a) s a` | {c} only if {k} | `Frames.Check.onlyIf` | agree on 66 evaluations in 1 new sentences (`heldout/`) |
| 7 | `exactly_when` | `@[reducible] def ExactlyWhen.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a` | {c} if and only if {k} | `Frames.Check.exactlyWhen` | agree on 374 evaluations in 3 readings of the fixtures; agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 8 | `rejected_unchanged` | `@[reducible] def RejectedUnchanged.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s _ r s' => ¬ op.accepted r ∧ s' = s) s a` | the answer is a rejection, and the whole state after the call is the state before it | `Frames.Check.rejectedUnchanged` | agree on 48 evaluations in 1 new sentences (`heldout/`) |
| 9 | `increases_by` | `@[reducible] def IncreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a + f s a) s a` | {m} after the call equals {m} before it plus {t}, exactly | `Frames.Check.increasesBy` | agree on 232 evaluations in 5 readings of the fixtures |
| 9 | `decreases_by` | `@[reducible] def DecreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a` | {m} after the call, plus {t}, equals {m} before it, exactly | `Frames.Check.decreasesBy` | agree on 358 evaluations in 6 readings of the fixtures |
| 9 | `becomes` | `@[reducible] def Becomes.at (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = f s a) s a` | {m} after the call is {t} | `Frames.Check.becomes` | agree on 5 evaluations in 5 readings of the fixtures |
| 9 | `result_is` | `@[reducible] def ResultIs.at (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r = f s a) s a` | {a} is {t} | `Frames.Check.resultIs` | agree on 860 evaluations in 10 readings of the fixtures; agree on 167 evaluations in 1 new sentences (`heldout/`) |
| 10 | `result_at_most` | `@[reducible] def ResultAtMost.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r ≤ f s a) s a` | {a} is at most {t} | `Frames.Check.resultAtMost` | agree on 8613 evaluations in 3 readings of the fixtures |
| 10 | `result_at_least` | `@[reducible] def ResultAtLeast.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => f s a ≤ out r) s a` | {a} is at least {t} | `Frames.Check.resultAtLeast` | agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 10 | `at_most` | `@[reducible] def AtMost.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a` | {m} after the call is at most {t} | `Frames.Check.atMost` | agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 10 | `at_least` | `@[reducible] def AtLeast.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => f s a ≤ m s' a) s a` | {m} after the call is at least {t} | `Frames.Check.atLeast` | agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 11 | `every_of` | `@[reducible] def EveryOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, P s' a x) s a` | every {c} {p}, judged on the state after the call | `Frames.Check.everyOf` | agree on 297 evaluations in 1 readings of the fixtures; agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 11 | `none_of` | `@[reducible] def NoneOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, ¬ P s' a x) s a` | no {c} {p}, judged on the state after the call | `Frames.Check.noneOf` | agree on 297 evaluations in 1 new sentences (`heldout/`) |
| 11 | `count_of` (no surface form yet) | `@[reducible] def CountOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) [∀ s a x, Decidable (P s a x)] (cmp : Cmp) (n : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => cmp.holds ((coll s' a r).countP (fun x => decide (P s' a x))) (n s a)) s a` | at most / at least / exactly n {c} {p}, judged on the state after the call | `Frames.Check.countOf` | no transfer of the batch is valid on the ledger afterwards (exactly 0): agree on 42 of 42 evaluations (11 of them false); at least 1 transfer of the batch is valid on the ledger afterwards: agree on 42 of 42 evaluations (31 of them false); at most 1 transfer of the batch is valid on the ledger afterwards: agree on 42 of 42 evaluations (1 of them false) |
| 12 | `monotone` (no surface form yet) | `@[reducible] def Monotone.at (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 more (fun r _ r₂ _ => cls r → cls r₂) s a s₂ a₂` | whenever a second state and input are {more} than the first and, for the first, {c}, then {c} for the second too (both calls must answer) | `Frames.Check.monotone` | a wallet holding more never loses acceptance of a withdrawal (true): agree on 216 of 216 evaluations (0 of them false); a wallet holding more never loses acceptance of a deposit (false: it can overflow): agree on 216 of 216 evaluations (34 of them false); the same, of successful deposits only (not fail-closed): agree on 216 of 216 evaluations (0 of them false) |
| 13 | `agrees_with` (no surface form yet) | `@[reducible] def AgreesWith.at (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => (r, s') = ref s a) s a` | the answer and the state after the call are exactly what {ref} gives | `Frames.Check.agreesWith` | a lookup agrees with reading the balance off the ledger (true): agree on 28 of 28 evaluations (0 of them false); the total agrees with the constant 1 (false): agree on 7 of 7 evaluations (5 of them false) |
| 14 | `independent_of` (no surface form yet) | `@[reducible] def IndependentOf.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => view r s' = view r₂ s₂') s a s₂ a₂` | two calls whose states and inputs differ only in {h} show the same {view} (both calls must answer) | `Frames.Check.independentOf` | a lookup is independent of every other account (true): agree on 196 of 196 evaluations (0 of them false); a transfer's answer is independent of the receiver's balance (false): agree on 1296 of 1296 evaluations (204 of them false) |

Over all compiled readings of the fixtures: the definition and the executable reading of the frames agree on **23772 of 23772** (point, frame) evaluations; over the new sentences of `heldout/`: **3598 of 3598**. The frames with no surface form are compared by `lean/Run/FrameTests.lean` on hand-written instances over the ledger and the wallet. Agreement on generated inputs is a test, not a proof that the two readings are the same.

**The defaults** (fail-closed; each reading lists the ones applied to it):

- **D1** always answers: the call must return an answer for every input the reading applies to (no panic, no abort, no endless loop)
- **D2** rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects it
- **D3** before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with the state after it, not states in between
- **D4** for all values: every outline <parameter>, every state and every input is universally quantified at the front; the Examples rows are instances
- **D5** collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection within the one Given, Then or Rule clause they occur in
- **D6** 'the first X of XS is P' requires that there is a first X
- **D7** items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the state after the call

**Weakenings** (never applied silently; a modifier has to ask):

- **rejected**: ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or that give no answer, are outside this clause
- **successful**: ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are rejected, or that give no answer, are outside this clause

**Quantifier scope, the one rule.** Every outline `<parameter>`, then the state, then the input are universally quantified at the front, in that order, and Givens restrict them. Collection words (`every`, `the first`, `no`) bind inside the one clause they are written in. Negation applies to the one atomic condition it is written on. Nothing is ever existentially quantified over inputs. The tool never chooses a scope.

## Vocabulary (the link from English to Lean)

`vocabulary.yaml`: **31 domain words** (8 operations, 23 measures, conditions, collections and answer words), **27 modifiers**, **19 frames**, and 10 idioms (a surface form that is not the regular form of one piece, with the composition it means; an idiom adds English, no Lean). A sentence is the composition of pieces its words spell out; this table and the Lean files it names are what a reviewer has to read to trust the step from English to Lean. Sign-off is per piece and is void as soon as the piece's entry or a Lean definition it names changes.

| Piece | Kind | Type | Surface forms | Lean | Definition | English paraphrase | Used by | Sign-off |
|---|---|---|---|---|---|---|---|---|
| w.transfer | domain | operation (sender: wallet, receiver: wallet / amount: amount; answers `W.Answer`) | {sender} transfers {amount} to {receiver}; in a Rule: transfer | `W.transfer` around the Aeneas model `wallet.transfer` | `@[reducible] def transfer : Frames.Op (Wallet × Wallet) U64 Answer := Bdd.opMut2 wallet.transfer accepted` | a transfer of {amount} from {sender} to {receiver} | 7 | UNREVIEWED |
| w.deposit | domain | operation (wallet: wallet / amount: amount; answers `W.Answer`) | {wallet} deposits {amount}; in a Rule: deposit | `W.deposit` around the Aeneas model `wallet.Wallet.deposit` | `@[reducible] def deposit : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.deposit accepted` | a deposit of {amount} into {wallet} | 4 | UNREVIEWED |
| w.withdraw | domain | operation (wallet: wallet / amount: amount; answers `W.Answer`) | {wallet} withdraws {amount}; in a Rule: withdrawal | `W.withdraw` around the Aeneas model `wallet.Wallet.withdraw` | `@[reducible] def withdraw : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.withdraw accepted` | a withdrawal of {amount} from {wallet} | 4 | UNREVIEWED |
| l.apply_batch | domain | operation (ledger: ledger / batch: batch; answers `Usize`) | the batch {batch} is applied to {ledger}; in a Rule: batch | `L.applyBatch` around the Aeneas model `ledger.Ledger.apply_batch` | `@[reducible] def applyBatch : Frames.Op Ledger (Slice Transfer) Usize := Bdd.opMut ledger.Ledger.apply_batch counted` | applying the batch {batch} to {ledger}, transfer by transfer | 14 | UNREVIEWED |
| l.apply_all | domain | operation (ledger: ledger / batch: batch; answers `Bool`) | the batch {batch} is applied to {ledger} as a whole; in a Rule: batch applied as a whole | `L.applyAll` around the Aeneas model `ledger.Ledger.apply_all` | `@[reducible] def applyAll : Frames.Op Ledger (Slice Transfer) Bool := Bdd.opMut ledger.Ledger.apply_all said` | applying the batch {batch} to {ledger} as a whole | 7 | UNREVIEWED |
| l.apply | domain | operation (ledger: ledger / transfer: transfer; answers `Bool`) | the transfer {transfer} is applied to {ledger}; in a Rule: transfer | `L.apply` around the Aeneas model `ledger.Ledger.apply` | `@[reducible] def apply : Frames.Op Ledger Transfer Bool := Bdd.opMut ledger.Ledger.apply said` | applying the transfer {transfer} to {ledger} | 3 | UNREVIEWED |
| l.total | domain | operation (ledger: ledger; answers `Option U64`) | the total of {ledger} is computed; in a Rule: computation of the total | `L.total` around the Aeneas model `ledger.Ledger.total` | `@[reducible] def total : Frames.Op Ledger Unit (Option U64) := Bdd.opRead0 ledger.Ledger.total found` | computing the total of {ledger} | 8 | UNREVIEWED |
| l.lookup | domain | operation (ledger: ledger / account: index; answers `Option U64`) | the balance of account {account} of {ledger} is looked up; in a Rule: lookup | `L.lookup` around the Aeneas model `ledger.Ledger.balance` | `@[reducible] def lookup : Frames.Op Ledger Usize (Option U64) := Bdd.opRead ledger.Ledger.balance found` | looking up the balance of account {account} of {ledger} | 3 | UNREVIEWED |
| w.balance | domain | measure<num> | {w:wallet}'s balance; (plural) balances | `W.balance {w}` | `@[reducible] def balance (w : Wallet) : Nat := w.balance.val` | the balance of {w} | 15 | UNREVIEWED |
| w.maximum | domain | term<num> | the maximum | `W.maximum` | `@[reducible] def maximum : Nat := U64.max` | the largest balance a wallet can hold (2^64 - 1) | 5 | UNREVIEWED |
| w.succeeds | domain | class | the operation succeeds | `W.accepted ans` | `@[reducible] def accepted (r : Answer) : Prop := r = .Ok ()` | the answer is Ok | 6 | UNREVIEWED |
| w.rejected_with | domain | class | the operation is rejected with {e:error} | `W.rejectedWith {e} ans` | `@[reducible] def rejectedWith (e : WalletError) (r : Answer) : Prop := r = .Err e` | the answer is the error '{e}' | 5 | UNREVIEWED |
| l.ledger | domain | measure<balances> | {l:ledger} | `L.balances {l}` | `@[reducible] def balances (l : Ledger) : List U64 := l.balances.val` | the balances of {l}, account by account | 26 | UNREVIEWED |
| l.balances_of | domain | nums | {l:ledger}'s balances; the balances of {l:ledger}; all balances of {l:ledger} | `(L.balances {l}).map L.amount` | `@[reducible] def balances (l : Ledger) : List U64 := l.balances.val`<br>`@[reducible] def amount (x : U64) : Nat := x.val` | the balances of every account of {l} | 12 | UNREVIEWED |
| l.bal_of | domain | measure<num> | the balance of account {k:term<acct>} of {l:ledger} | `L.bal {l} {k}` | `@[reducible] def bal (l : Ledger) (k : Nat) : Nat := (l.balances.val.getD k 0#u64).val` | the balance, in {l}, of account {k} (0 if there is no such account) | 2 | UNREVIEWED |
| l.balance_at | domain | term<optnum> | the balance of account {i:index} of {l:ledger}; the balance of {i:index} in {l:ledger} | `L.balanceAt {l} {i}` | `@[reducible] def balanceAt (l : Ledger) (i : Usize) : Option U64 := l.balances.val[i.val]?` | the balance of account {i} of {l} before the call (absent if there is no such account) | 2 | UNREVIEWED |
| l.accounts | domain | parts<acct> | the accounts of {l:ledger} | `L.accounts {l}` | `@[reducible] def accounts (l : Ledger) : List Nat := List.range l.balances.val.length`<br>`@[reducible] def bal (l : Ledger) (k : Nat) : Nat := (l.balances.val.getD k 0#u64).val` | the accounts of {l} | 2 | UNREVIEWED |
| l.is_account | domain | cond | {i:index} is an account of {l:ledger}; (negated) {i:index} is not an account of {l:ledger} | `L.isAccount {l} {i}` | `@[reducible] def isAccount (l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | {i} is an account number of {l} | 2 | UNREVIEWED |
| l.valid | domain | itempred<transfer> | is valid on {l:ledger}; (negated) is not valid on {l:ledger} | `L.valid {l} {item}` | `def valid (l : Ledger) (t : Transfer) : Prop := t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧ t.amount.val ≤ bal l t.from.val ∧ bal l t.to.val + t.amount.val ≤ U64.max` | can be carried out exactly on {l} (both accounts exist and differ, the sender covers the amount, the receiver's balance stays within 2^64 - 1) | 9 | UNREVIEWED |
| l.maximum | domain | term<num> | the maximum | `L.maximum` | `@[reducible] def maximum : Nat := U64.max` | the largest total that can be reported (2^64 - 1) | 4 | UNREVIEWED |
| l.the_transfer | domain | item<transfer> | the transfer {t:transfer}; {t:transfer} | `{t}` | - | {t} | 3 | UNREVIEWED |
| l.transfers | domain | coll<transfer> | transfer of {b:batch} | `L.transfers {b}` | `@[reducible] def transfers (b : Slice Transfer) : List Transfer := b.val` | transfer of {b} | 5 | UNREVIEWED |
| l.length | domain | term<num> | the length of {b:batch} | `L.length {b}` | `@[reducible] def length (b : Slice Transfer) : Nat := b.val.length` | the number of transfers in {b} | 5 | UNREVIEWED |
| l.sender | domain | term<acct> | the sender of {t:transfer} | `L.sender {t}` | `@[reducible] def sender (t : Transfer) : Nat := t.from.val` | the sending account of {t} | 2 | UNREVIEWED |
| l.receiver | domain | term<acct> | the receiver of {t:transfer} | `L.receiver {t}` | `@[reducible] def receiver (t : Transfer) : Nat := t.to.val` | the receiving account of {t} | 2 | UNREVIEWED |
| l.amount_of | domain | term<num> | the amount of {t:transfer} | `L.amountOf {t}` | `@[reducible] def amountOf (t : Transfer) : Nat := t.amount.val` | the amount of {t} | 2 | UNREVIEWED |
| l.applied | domain | ameasure<num> | the number of transfers applied | `L.applied ans` | `@[reducible] def applied (n : Usize) : Nat := n.val` | the number of transfers the call reports as applied | 8 | UNREVIEWED |
| l.stopped_at | domain | acoll<transfer> | transfer at which {b:batch} stopped | `L.stoppedAt {b} ans` | `@[reducible] def stoppedAt (b : Slice Transfer) (n : Usize) : List Transfer := (b.val[n.val]?).toList` | transfer of {b} at the position the reported count points to (none if every transfer was applied) | 1 | UNREVIEWED |
| l.result | domain | ameasure<optnum> | the result | `ans` | - | the value the call returns | 4 | UNREVIEWED |
| l.accepted | domain | class | it is accepted; (negated) it is rejected | `L.said ans` | `@[reducible] def said (ok : Bool) : Prop := ok = true` | the answer is yes (accepted) | 6 | UNREVIEWED |
| l.found | domain | class | there is a result; (negated) there is no result | `L.found ans` | `@[reducible] def found (o : Option U64) : Prop := o ≠ none` | the call returns a value | 4 | UNREVIEWED |
| amount_value | modifier | term<num> | {x:amount} | `{x}.val` | - | {x} | 16 | UNREVIEWED |
| index_number | modifier | term<acct> | {x:index} | `{x}.val` | - | {x} | 0 | UNREVIEWED |
| index_count | modifier | term<num> | (no surface of its own) | `{x}.val` | - | {x} | 2 | UNREVIEWED |
| balances_value | modifier | term<balances> | {x:balances} | `{x}` | - | {x} | 23 | UNREVIEWED |
| amount_result | modifier | term<optnum> | {x:amount} | `some {x}` | - | the value {x} | 2 | UNREVIEWED |
| zero | modifier | term<num> | zero | `0` | - | 0 | 2 | UNREVIEWED |
| is | modifier | cond | {m:measure<T>} is {t:term<T>} | `{m} = {t}` | - | {m} is {t} | 34 | UNREVIEWED |
| not_more_than | modifier | cond | {t:term<num>} is not more than {m:measure<num>} | `{t} ≤ {m}` | - | {t} is at most {m} | 6 | UNREVIEWED |
| more_than | modifier | cond | {t:term<num>} is more than {m:measure<num>} | `{m} < {t}` | - | {t} is strictly more than {m} | 3 | UNREVIEWED |
| exceeds | modifier | cond | {m:measure<num>} is more than {t:term<num>} | `{t} < {m}` | - | {m} is strictly more than {t} | 2 | UNREVIEWED |
| at_most_value | modifier | cond | {m:measure<num>} is at most {t:term<num>} | `{m} ≤ {t}` | - | {m} is at most {t} | 2 | UNREVIEWED |
| sum_within | modifier | cond | {m:measure<num>} plus {t:term<num>} does not exceed {z:term<num>} | `{m} + {t} ≤ {z}` | - | {m} plus {t} is at most {z} | 3 | UNREVIEWED |
| sum_exceeds | modifier | cond | {m:measure<num>} plus {t:term<num>} exceeds {z:term<num>} | `{z} < {m} + {t}` | - | {m} plus {t} is strictly more than {z} | 2 | UNREVIEWED |
| not | modifier | * | (no surface of its own) | `¬ ({p})` | - | it is NOT the case that {p} | 10 | UNREVIEWED |
| aggregate | modifier | measure<num> | the total of {ns:nums} | `Frames.aggregate ({ns})` | `@[reducible] def aggregate (xs : List Nat) : Nat := xs.sum` | the sum of {ns} | 15 | UNREVIEWED |
| all_of | modifier | nums | all {pm:per_actor} | `[{pm}]` | - | {pm} | 3 | UNREVIEWED |
| holds_of | modifier | cond | {i:item<T>} {p:itempred<T>} | `{p}` | - | {i} {p} | 3 | UNREVIEWED |
| every | modifier | cond | every {c:coll<T>} {p:itempred<T>} | `Frames.every ({c}) (fun x => {p})` | `@[reducible] def every (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, P x` | every {c} {p} | 2 | UNREVIEWED |
| the_first | modifier | cond | the first {c:coll<T>} {p:itempred<T>} | `Frames.theFirst ({c}) (fun x => {p})` | `@[reducible] def theFirst (items : List ι) (P : ι → Prop) : Prop := items ≠ [] ∧ ∀ x ∈ items.head?, P x` | there is a first {c}, and it {p} | 3 | UNREVIEWED |
| no_such | modifier | cond | no {c:coll<T>} {p:itempred<T>} | `Frames.noneOf ({c}) (fun x => {p})` | `@[reducible] def noneOf (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, ¬ P x` | no {c} {p} | 0 | UNREVIEWED |
| given | modifier | opmod | (no surface of its own) | `({op}).given (fun st inp => {c})` | `@[reducible] def Op.given (op : Op σ α ρ) (C : Cond σ α) : Op σ α ρ := { op with scope := fun s a => op.scope s a ∧ C s a }` | assuming {c} | 37 | UNREVIEWED |
| rejected | modifier | opmod | (no surface of its own) | `({op}).rejected` | `@[reducible] def Op.rejected (op : Op σ α ρ) : Op σ α ρ := { op with calls := .rejected }`<br>`inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr` | rejected calls only | 5 | UNREVIEWED |
| successful | modifier | opmod | (no surface of its own) | `({op}).successful` | `@[reducible] def Op.successful (op : Op σ α ρ) : Op σ α ρ := { op with calls := .accepted }`<br>`inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr` | accepted calls only | 3 | UNREVIEWED |
| internal | modifier | opmod | (no surface of its own) | `({op}).internal {member} {parties}` | `@[reducible] def Op.internal (op : Op σ α ρ) (member : σ → ι → Prop) (parties : α → List ι) : Op σ α ρ := op.given (fun s a => ∀ p ∈ parties a, member s p)` | every party the input names is a member of the state | 0 | UNREVIEWED |
| and_then | modifier | opmod | (no surface of its own) | `({op}).andThen ({op2})` | `@[reducible] def Op.andThen {α₂ ρ₂ : Type} (first : Op σ α ρ) (second : Op σ α₂ ρ₂) : Op σ (α × α₂) ρ₂ where run s a := match first.run s a.1 with \| none => none \| some (_, s₁) => second.run s₁ a.2 accepted := second.accepted` | then, on the state that leaves, | 4 | UNREVIEWED |
| beside | modifier | opmod | (no surface of its own) | `({op}).beside {type}` | `@[reducible] def Op.beside (op : Op σ α ρ) (β : Type) : Op (σ × β) α ρ where run s a := match op.run s.1 a with \| none => none \| some (r, s') => some (r, (s', s.2)) accepted := op.accepted scope s a := op.scope s.1 a calls := op.calls` | a bystander, not passed to the operation | 1 | UNREVIEWED |
| accepted | modifier | class | (no surface of its own) | `({opbase}).accepted ans` | - | the answer is an acceptance | 5 | UNREVIEWED |
| always_answers | frame | claim | it answers; (Rule) always answers | `Frames.AlwaysAnswers {op}` | `def AlwaysAnswers (op : Op σ α ρ) : Prop := ∀ s a, AlwaysAnswers.at op s a`<br>`@[reducible] def AlwaysAnswers.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ _ _ => True) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | the call gives an answer | 3 | UNREVIEWED |
| never_changes | frame | claim | {m:measure<T>} is unchanged; (Rule) never changes {m:measure<T>} | `Frames.NeverChanges {op} {m}` | `def NeverChanges (op : Op σ α ρ) (m : Measure σ α μ) : Prop := ∀ s a, NeverChanges.at op m s a`<br>`@[reducible] def NeverChanges.at (op : Op σ α ρ) (m : Measure σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call equals {m} before it | 23 | UNREVIEWED |
| changes_only | frame | claim | of {c:parts<acct>}, only {x:term<acct>} and {y:term<acct>} change | `Frames.ChangesOnly {op} {c} {xs}` | `def ChangesOnly (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) : Prop := ∀ s a, ChangesOnly.at op parts m X s a`<br>`@[reducible] def ChangesOnly.at (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => parts s' = parts s ∧ ∀ k ∈ parts s, k ∉ X s a → m s' k = m s k) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} are the same accounts after the call, and every one of them other than {xs} has the balance it had before | 2 | UNREVIEWED |
| always | frame | claim | {c:class} | `Frames.Always {op} {c}` | `def Always (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Always.at op cls s a`<br>`@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => cls r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} | 23 | UNREVIEWED |
| never | frame | claim | (no surface of its own) | `Frames.Never {op} {c}` | `def Never (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Never.at op cls s a`<br>`@[reducible] def Never.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => ¬ cls r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | it is NOT the case that {c} | 7 | UNREVIEWED |
| if_then | frame | claim | (Rule) is accepted whenever {k:cond} | `Frames.IfThen {op} {k} {c}` | `def IfThen (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) : Prop := ∀ s a, IfThen.at op C cls s a`<br>`@[reducible] def IfThen.at (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := Always.at (op.given C) cls s a`<br>`@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => cls r) s a`<br>`@[reducible] def Op.given (op : Op σ α ρ) (C : Cond σ α) : Op σ α ρ := { op with scope := fun s a => op.scope s a ∧ C s a }`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | if {k}, then {c} | 0 | UNREVIEWED |
| only_if | frame | claim | (Rule) is accepted only if {k:cond} | `Frames.OnlyIf {op} {c} {k}` | `def OnlyIf (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, OnlyIf.at op cls C s a`<br>`@[reducible] def OnlyIf.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r → C s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} only if {k} | 0 | UNREVIEWED |
| exactly_when | frame | claim | (Rule) is accepted exactly when {k:cond} | `Frames.ExactlyWhen {op} {c} {k}` | `def ExactlyWhen (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, ExactlyWhen.at op cls C s a`<br>`@[reducible] def ExactlyWhen.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} if and only if {k} | 3 | UNREVIEWED |
| rejected_unchanged | frame | claim | it is rejected and nothing is changed; (Rule) is rejected and changes nothing | `Frames.RejectedUnchanged {op}` | `def RejectedUnchanged (op : Op σ α ρ) : Prop := ∀ s a, RejectedUnchanged.at op s a`<br>`@[reducible] def RejectedUnchanged.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s _ r s' => ¬ op.accepted r ∧ s' = s) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | the answer is a rejection, and the whole state after the call is the state before it | 0 | UNREVIEWED |
| increases_by | frame | claim | {m:measure<num>} is increased by {t:term<num>}; (Rule) increases {m:measure<num>} by exactly {t:term<num>} | `Frames.IncreasesBy {op} {m} {t}` | `def IncreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, IncreasesBy.at op m f s a`<br>`@[reducible] def IncreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a + f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call equals {m} before it plus {t}, exactly | 5 | UNREVIEWED |
| decreases_by | frame | claim | {m:measure<num>} is decreased by {t:term<num>}; (Rule) decreases {m:measure<num>} by exactly {t:term<num>} | `Frames.DecreasesBy {op} {m} {t}` | `def DecreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, DecreasesBy.at op m f s a`<br>`@[reducible] def DecreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call, plus {t}, equals {m} before it, exactly | 6 | UNREVIEWED |
| becomes | frame | claim | {m:measure<T>} is now {t:term<T>} | `Frames.Becomes {op} {m} {t}` | `def Becomes (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) : Prop := ∀ s a, Becomes.at op m f s a`<br>`@[reducible] def Becomes.at (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is {t} | 5 | UNREVIEWED |
| result_is | frame | claim | {a:ameasure<T>} is {t:term<T>} | `Frames.ResultIs {op} {a} {t}` | `def ResultIs (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) : Prop := ∀ s a, ResultIs.at op out f s a`<br>`@[reducible] def ResultIs.at (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r = f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is {t} | 10 | UNREVIEWED |
| result_at_most | frame | claim | {a:ameasure<num>} is at most {t:term<num>} | `Frames.ResultAtMost {op} {a} {t}` | `def ResultAtMost (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtMost.at op out f s a`<br>`@[reducible] def ResultAtMost.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r ≤ f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is at most {t} | 3 | UNREVIEWED |
| result_at_least | frame | claim | {a:ameasure<num>} is at least {t:term<num>} | `Frames.ResultAtLeast {op} {a} {t}` | `def ResultAtLeast (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtLeast.at op out f s a`<br>`@[reducible] def ResultAtLeast.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => f s a ≤ out r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is at least {t} | 0 | UNREVIEWED |
| at_most | frame | claim | {m:measure<num>} is afterwards at most {t:term<num>}; (Rule) never leaves {m:measure<num>} above {t:term<num>} | `Frames.AtMost {op} {m} {t}` | `def AtMost (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtMost.at op m f s a`<br>`@[reducible] def AtMost.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is at most {t} | 0 | UNREVIEWED |
| at_least | frame | claim | {m:measure<num>} is afterwards at least {t:term<num>}; (Rule) never leaves {m:measure<num>} below {t:term<num>} | `Frames.AtLeast {op} {m} {t}` | `def AtLeast (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtLeast.at op m f s a`<br>`@[reducible] def AtLeast.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => f s a ≤ m s' a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is at least {t} | 0 | UNREVIEWED |
| every_of | frame | claim | every {c:acoll<T>} {p:itempred<T>} afterwards | `Frames.EveryOf {op} {c} {p}` | `def EveryOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, EveryOf.at op coll P s a`<br>`@[reducible] def EveryOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, P s' a x) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | every {c} {p}, judged on the state after the call | 1 | UNREVIEWED |
| none_of | frame | claim | no {c:acoll<T>} {p:itempred<T>} afterwards | `Frames.NoneOf {op} {c} {p}` | `def NoneOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, NoneOf.at op coll P s a`<br>`@[reducible] def NoneOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, ¬ P s' a x) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | no {c} {p}, judged on the state after the call | 0 | UNREVIEWED |
| i.has_balance | idiom | cond | {w:wallet} has a balance of {t:term<num>} | means `is(w.balance(w), t)` | - | (the reading of that composition) | 11 | UNREVIEWED |
| i.holds | idiom | cond | {l:ledger} holds the balances {t:term<balances>} | means `is(l.ledger(l), t)` | - | (the reading of that composition) | 23 | UNREVIEWED |
| i.add_up_to | idiom | cond | {ns:nums} add up to {t:term<num>} | means `is(aggregate(ns), t)` | - | (the reading of that composition) | 2 | UNREVIEWED |
| i.add_up_to_more | idiom | cond | {ns:nums} add up to more than {t:term<num>} | means `exceeds(aggregate(ns), t)` | - | (the reading of that composition) | 2 | UNREVIEWED |
| i.now_holds | idiom | claim | {l:ledger} now holds the balances {t:term<balances>} | means `becomes(l.ledger(l), t)` | - | (the reading of that composition) | 5 | UNREVIEWED |
| i.none_applied | idiom | claim | no transfer is applied | means `result_is(l.applied(), zero())` | - | (the reading of that composition) | 2 | UNREVIEWED |
| i.all_applied | idiom | claim | every transfer of {b:batch} is applied | means `result_is(l.applied(), l.length(b))` | - | (the reading of that composition) | 2 | UNREVIEWED |
| i.exactly_applied | idiom | claim | exactly {k:index} transfers are applied | means `result_is(l.applied(), index_count(k))` | - | (the reading of that composition) | 2 | UNREVIEWED |
| i.stopped_only_at | idiom | claim | the batch {b:batch} has stopped only at a transfer that {p:itempred<transfer>} as it now stands | means `every_of(l.stopped_at(b), p)` | - | (the reading of that composition) | 1 | UNREVIEWED |
| i.moved | idiom | claim | the amount of {t:transfer} has moved between its accounts in {l:ledger} and no other balance changed | means `decreases_by(l.bal_of(l.sender(t), l), l.amount_of(t)); increases_by(l.bal_of(l.receiver(t), l), l.amount_of(t)); changes_only(l.accounts(l), [l.sender(t), l.receiver(t)])` | - | (the reading of that composition) | 2 | UNREVIEWED |

87 of 87 entries are unreviewed. Record a review with `python3 -m slicegen review <id|all> --reviewer <name>` (piece ids and the ids of the old glossary are both accepted).

## Regression: every old statement against its new reading (plan node V3)

Each scenario has two Lean statements: the **reading** compiled from the composable vocabulary (`lean/Wallet/Readings.lean`) and the **flat statement** of the old whole-phrase glossary (`lean/Wallet/Statements.lean`, unchanged; every hand-written proof is about it). A generated theorem `<id>.reading_iff : <id>.reading ↔ <id>.stmt` is checked by Lean's kernel, and the audit checks that its type is exactly that (`lean/Run/Links.lean`, `lean/Bdd/AuditLinks.lean`). So a verdict is carried from the old statement to the new one by an equivalence, not by getting the same answer twice; a reading whose equivalence is missing gets the verdict UNLINKED.

| Scenario | Old glossary entries | New pieces | Idioms needed | NEW ↔ OLD | Axioms | Reading non-vacuous |
|---|---|---|---|---|---|---|
| `wallet.transfer_conserves` | 8 | 15 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_short` | 5 | 9 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_no_room` | 6 | 11 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_short_example` | 4 | 8 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.withdraw_covered` | 5 | 9 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.withdraw_too_much` | 5 | 9 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.deposit_with_room` | 5 | 10 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.deposit_overflow` | 5 | 10 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_always_succeeds` | 6 | 12 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_conserves` | 3 | 8 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_stops_at_invalid` | 3 | 9 | i.holds, i.stopped_only_at | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.two_batches_conserve` | 4 | 12 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_first_invalid` | 5 | 13 | i.holds, i.none_applied | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_count_bounded` | 3 | 8 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_example_all` | 4 | 9 | i.holds, i.exactly_applied, i.now_holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_example_stop` | 4 | 9 | i.holds, i.exactly_applied, i.now_holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_all_valid_all_applied` | 4 | 11 | i.holds, i.all_applied | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.transfer_valid_moves` | 6 | 21 | i.holds, i.moved | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.transfer_invalid_rejected` | 5 | 13 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_is_sum` | 4 | 11 | i.holds, i.add_up_to | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_overflow` | 4 | 13 | i.holds, i.add_up_to_more | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_always_available` | 3 | 7 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.balance_of_account` | 4 | 9 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.balance_no_account` | 4 | 10 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_rejected_unchanged` | 3 | 8 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_first_invalid` | 5 | 13 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_conserves` | 3 | 8 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_accept` | 4 | 8 | i.holds, i.now_holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_rollback_late` | 4 | 10 | i.holds, i.now_holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_rollback` | 4 | 10 | i.holds, i.now_holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_then_total` | 5 | 13 | i.holds, i.add_up_to | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_then_total_overflow` | 5 | 15 | i.holds, i.add_up_to_more | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `negative_controls.contradictory_givens` | 5 | 9 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | n/a (the Givens contradict each other) |
| `negative_controls.bystander_unchanged` | 5 | 11 | i.has_balance | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |

**34 of 34** readings are proved equivalent to their old statement. **None is a deliberate strengthening**: the old statements were already fail-closed (each said the call returns, for every input satisfying the Givens), so the defaults change nothing at scenario level. The defaults do bite at the level of the `Rule:` lines, which had no statement before: each rule statement covers every input, and is proved FROM its scenarios (see each rule's block).

## New sentences (not in the fixtures)

Informational; it changes no verdict and no exit status. The feature files of `heldout/` hold rules that are in no fixture, written with the existing vocabulary: **no piece was added or changed for them**. Each is compiled from the vocabulary alone (`python3 -m slicegen compile heldout/*.feature`). A new sentence has no old whole-phrase binding, so it has no flat statement, no hand-written proof and no cucumber step: what it gets here is its compiled reading (type-checked by Lean), its echo, and a search on generated inputs through the frames' two readings. NO-COUNTEREXAMPLE is not a proof.

| Sentence | Compiled from existing pieces | Pieces | Idioms | Searched on generated inputs | Result |
|---|---|---|---|---|---|
| Rule: A transfer is accepted whenever the transfer is valid on the ledger (`heldout/frames.feature:8`) | yes | 6 | none | 66 inputs, 66 in scope; definition and executable reading agree on 66 of 66 | **NO-COUNTEREXAMPLE** |
| Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing (`heldout/frames.feature:11`) | yes | 7 | none | 66 inputs, 48 in scope; definition and executable reading agree on 48 of 48 | **NO-COUNTEREXAMPLE** |
| Rule: For a batch, the number of transfers applied is at least the length of the batch (`heldout/frames.feature:14`) | yes | 4 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **COUNTEREXAMPLE: {"the_ledger": "[]", "the_batch": "[0->1:1]"}** (expected REFUTED) |
| Rule: A batch never leaves the total of all balances of the ledger below zero (`heldout/frames.feature:17`) | yes | 5 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **NO-COUNTEREXAMPLE** |
| Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards (`heldout/frames.feature:20`) | yes | 4 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **NO-COUNTEREXAMPLE** |
| Rule: A successful transfer never changes the total of all balances of the ledger (`heldout/frames.feature:23`) | yes | 5 | none | 66 inputs, 66 in scope; definition and executable reading agree on 66 of 66 | **NO-COUNTEREXAMPLE** |
| Scenario Outline: A rejected transfer leaves every single balance as it was (`heldout/frames.feature:27`) | yes | 14 | yes | 3630 inputs, 330 in scope; definition and executable reading agree on 990 of 990 | **NO-COUNTEREXAMPLE** |
| Rule: An internal transfer never changes the total of all balances of the ledger (`heldout/new_rules.feature:12`) | yes | 5 | none | 66 inputs, 49 in scope; definition and executable reading agree on 49 of 49 | **NO-COUNTEREXAMPLE** |
| Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger (`heldout/new_rules.feature:15`) | yes | 7 | none | 66 inputs, 66 in scope; definition and executable reading agree on 66 of 66 | **NO-COUNTEREXAMPLE** |
| Rule: For a lookup for which the account is not an account of the ledger, there is no result (`heldout/new_rules.feature:18`) | yes | 7 | none | 55 inputs, 31 in scope; definition and executable reading agree on 31 of 31 | **NO-COUNTEREXAMPLE** |
| Rule: A batch never leaves the total of all balances of the ledger above the maximum (`heldout/new_rules.feature:21`) | yes | 5 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **COUNTEREXAMPLE: {"the_ledger": "[18446744073709551615, 1]", "the_batch": "[]"}** (expected REFUTED) |
| Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards (`heldout/new_rules.feature:24`) | yes | 5 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **NO-COUNTEREXAMPLE** |
| Rule: For a batch for which every transfer of the batch is not valid on the ledger, no transfer is applied (`heldout/zz_reviewer_natural.feature:6`) | yes | 10 | yes | 297 inputs, 167 in scope; definition and executable reading agree on 167 of 167 | **NO-COUNTEREXAMPLE** |
| Rule: A withdrawal is accepted whenever the amount is not more than the wallet's balance (`heldout/zz_reviewer_natural.feature:9`) | yes | 6 | none | 36 inputs, 36 in scope; definition and executable reading agree on 36 of 36 | **NO-COUNTEREXAMPLE** |
| Rule: A batch applied as a whole is accepted exactly when every transfer of the batch is valid on the ledger (`heldout/zz_reviewer_natural.feature:12`) | yes | 6 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **COUNTEREXAMPLE: {"the_ledger": "[1, 0]", "the_batch": "[0->1:1, 0->1:1]"}** |
| Rule: A rejected batch never changes the total of all balances of the ledger (`heldout/zz_reviewer_natural.feature:15`) | yes | 5 | none | 297 inputs, 297 in scope; definition and executable reading agree on 297 of 297 | **NO-COUNTEREXAMPLE** |

16 of 16 sentences compiled with no new piece.

#### Rule: A transfer is accepted whenever the transfer is valid on the ledger

`heldout/frames.feature:8`  pieces `l.apply, if_then, holds_of, l.the_transfer, l.valid, accepted`

```text
applies to  a transfer: every ledger, every transfer
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            if the transfer can be carried out exactly on the ledger (both accounts exist and differ, the sender covers
            the amount, the receiver's balance stays within 2^64 - 1), then the answer is an acceptance
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_if_then.reading : Prop :=
  Frames.IfThen L.apply (fun st inp => L.valid st inp) (fun ans => (L.apply).accepted ans)
```

</details>

#### Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing

`heldout/frames.feature:11`  pieces `l.apply, given, rejected_unchanged, holds_of, l.the_transfer, not, l.valid`

```text
applies to  a transfer: every ledger, every transfer
            every such call, accepted or rejected [default D2]
assuming    the transfer can NOT be carried out exactly on the ledger (an account does not exist, or both are the same,
            or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1)
then        the call gives an answer [default D1]
            the answer is a rejection, and the whole state after the call is the state before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_rejected_unchanged.reading : Prop :=
  Frames.RejectedUnchanged ((L.apply).given (fun st inp => ¬ ((L.valid st inp))))
```

</details>

#### Rule: For a batch, the number of transfers applied is at least the length of the batch

`heldout/frames.feature:14`  pieces `l.apply_batch, result_at_least, l.applied, l.length`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is at least the number of transfers in the batch
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_result_at_least.reading : Prop :=
  Frames.ResultAtLeast L.applyBatch (fun ans => L.applied ans) (fun st inp => L.length inp)
```

</details>

#### Rule: A batch never leaves the total of all balances of the ledger below zero

`heldout/frames.feature:17`  pieces `l.apply_batch, at_least, aggregate, l.balances_of, zero`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            the sum of the balances of every account of the ledger after the call is at least 0
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_at_least.reading : Prop :=
  Frames.AtLeast L.applyBatch (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => 0)
```

</details>

#### Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards

`heldout/frames.feature:20`  pieces `l.apply_batch, none_of, l.stopped_at, l.valid`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            no transfer of the batch at the position the reported count points to (none if every transfer was applied)
            can be carried out exactly on the ledger (both accounts exist and differ, the sender covers the amount, the
            receiver's balance stays within 2^64 - 1), judged on the state after the call
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D7 items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the
            state after the call
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_none_of.reading : Prop :=
  Frames.NoneOf L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp x => L.valid st x)
```

</details>

#### Rule: A successful transfer never changes the total of all balances of the ledger

`heldout/frames.feature:23`  pieces `l.apply, successful, never_changes, aggregate, l.balances_of`

```text
applies to  a transfer: every ledger, every transfer
            ONLY successful calls [asked for]
assuming    nothing: every state and every input
then        the sum of the balances of every account of the ledger after the call equals the sum of the balances of
            every account of the ledger before it
defaults    D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are rejected,
            or that give no answer, are outside this clause
```

<details><summary>Lean statement</summary>

```lean
def Rule.sentences_that_exercise_the_remaining_frames.f_scenario_level.reading : Prop :=
  Frames.NeverChanges (L.apply).successful (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### Scenario Outline: A rejected transfer leaves every single balance as it was

`heldout/frames.feature:27`  pieces `l.apply, given, i.holds, is, l.ledger, balances_value, rejected, successful, always_answers, never_changes, l.bal_of, index_number, aggregate, l.balances_of`

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>; for every value of
            balances, k
            every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            if the call is rejected: the balance, in ledger Main, of account <k> (0 if there is no such account) after
            the call equals the balance, in ledger Main, of account <k> (0 if there is no such account) before it
            if the call is accepted: the sum of the balances of every account of ledger Main after the call equals the
            sum of the balances of every account of ledger Main before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or
            that give no answer, are outside this clause
not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are rejected,
            or that give no answer, are outside this clause
```

<details><summary>Lean statement</summary>

```lean
def Spec.sentences_that_exercise_the_remaining_frames.f_other_account_untouched.reading : Prop :=
  ∀ (balances : List U64) (k : Usize),
    Frames.AlwaysAnswers ((L.apply).given (fun st inp => (L.balances st) = balances)) ∧
    Frames.NeverChanges (((L.apply).given (fun st inp => (L.balances st) = balances)).rejected) (fun st inp => L.bal st k.val) ∧
    Frames.NeverChanges (((L.apply).given (fun st inp => (L.balances st) = balances)).successful) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### Rule: An internal transfer never changes the total of all balances of the ledger

`heldout/new_rules.feature:12`  pieces `l.apply, internal, never_changes, aggregate, l.balances_of`

```text
applies to  a transfer: every ledger, every transfer
            every such call, accepted or rejected [default D2]
assuming    every account the transfer names is an account of the ledger (internal)
then        the call gives an answer [default D1]
            the sum of the balances of every account of the ledger after the call equals the sum of the balances of
            every account of the ledger before it
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.new_rules_about_the_ledger.n1_internal_transfer.reading : Prop :=
  Frames.NeverChanges ((L.apply).internal L.isAccount L.parties) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger

`heldout/new_rules.feature:15`  pieces `l.apply, only_if, not_more_than, l.amount_of, l.bal_of, l.sender, accepted`

```text
applies to  a transfer: every ledger, every transfer
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            the answer is an acceptance only if the amount of the transfer is at most the balance, in the ledger, of
            account the sending account of the transfer (0 if there is no such account)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.new_rules_about_the_ledger.n2_accepted_only_if_covered.reading : Prop :=
  Frames.OnlyIf L.apply (fun ans => (L.apply).accepted ans) (fun st inp => (L.amountOf inp) ≤ (L.bal st (L.sender inp)))
```

</details>

#### Rule: For a lookup for which the account is not an account of the ledger, there is no result

`heldout/new_rules.feature:18`  pieces `l.lookup, given, never, not, l.is_account, always, l.found`

```text
applies to  a lookup: every ledger, every account
            every such call, accepted or rejected [default D2]
assuming    the account is NOT an account number of the ledger
then        the call gives an answer [default D1]
            the call returns no value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.new_rules_about_the_ledger.n3_lookup_missing_account.reading : Prop :=
  Frames.Never ((L.lookup).given (fun st inp => ¬ ((L.isAccount st inp)))) (fun ans => L.found ans)
```

</details>

#### Rule: A batch never leaves the total of all balances of the ledger above the maximum

`heldout/new_rules.feature:21`  pieces `l.apply_batch, at_most, aggregate, l.balances_of, l.maximum`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            the sum of the balances of every account of the ledger after the call is at most the largest total that can
            be reported (2^64 - 1)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.new_rules_about_the_ledger.n4_total_stays_within_maximum.reading : Prop :=
  Frames.AtMost L.applyBatch (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => L.maximum)
```

</details>

#### Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards

`heldout/new_rules.feature:24`  pieces `l.apply_batch, every_of, l.stopped_at, not, l.valid`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            every transfer of the batch at the position the reported count points to (none if every transfer was
            applied) can NOT be carried out exactly on the ledger (an account does not exist, or both are the same, or
            the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1), judged on the state
            after the call
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D7 items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the
            state after the call
```

<details><summary>Lean statement</summary>

```lean
def Rule.new_rules_about_the_ledger.n5_stopped_at_invalid.reading : Prop :=
  Frames.EveryOf L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp x => ¬ ((L.valid st x)))
```

</details>

#### Rule: For a batch for which every transfer of the batch is not valid on the ledger, no transfer is applied

`heldout/zz_reviewer_natural.feature:6`  pieces `l.apply_batch, given, result_is, every, l.transfers, not, l.valid, i.none_applied, l.applied, zero`

```text
applies to  a batch: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    every transfer of the batch can NOT be carried out exactly on the ledger (an account does not exist, or both
            are the same, or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1)
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is 0
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.natural_readings_that_differ.r1_scope.reading : Prop :=
  Frames.ResultIs ((L.applyBatch).given (fun st inp => Frames.every ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun ans => L.applied ans) (fun st inp => 0)
```

</details>

#### Rule: A withdrawal is accepted whenever the amount is not more than the wallet's balance

`heldout/zz_reviewer_natural.feature:9`  pieces `w.withdraw, if_then, not_more_than, amount_value, w.balance, accepted`

```text
applies to  a withdrawal: every wallet, every amount
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            if the amount is at most the balance of the wallet, then the answer is an acceptance
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.natural_readings_that_differ.r2_whenever.reading : Prop :=
  Frames.IfThen W.withdraw (fun st inp => inp.val ≤ (W.balance st)) (fun ans => (W.withdraw).accepted ans)
```

</details>

#### Rule: A batch applied as a whole is accepted exactly when every transfer of the batch is valid on the ledger

`heldout/zz_reviewer_natural.feature:12`  pieces `l.apply_all, exactly_when, every, l.transfers, l.valid, accepted`

```text
applies to  a batch applied as a whole: every ledger, every batch
            every such call, accepted or rejected [default D2]
assuming    nothing: every state and every input
then        the call gives an answer [default D1]
            the answer is an acceptance if and only if every transfer of the batch can be carried out exactly on the
            ledger (both accounts exist and differ, the sender covers the amount, the receiver's balance stays within
            2^64 - 1)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
```

<details><summary>Lean statement</summary>

```lean
def Rule.natural_readings_that_differ.r3_timing.reading : Prop :=
  Frames.ExactlyWhen L.applyAll (fun ans => (L.applyAll).accepted ans) (fun st inp => Frames.every ((L.transfers inp)) (fun x => (L.valid st x)))
```

</details>

#### Rule: A rejected batch never changes the total of all balances of the ledger

`heldout/zz_reviewer_natural.feature:15`  pieces `l.apply_batch, rejected, never_changes, aggregate, l.balances_of`

```text
applies to  a batch: every ledger, every batch
            ONLY rejected calls [asked for]
assuming    nothing: every state and every input
then        the sum of the balances of every account of the ledger after the call equals the sum of the balances of
            every account of the ledger before it
defaults    D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or
            that give no answer, are outside this clause
```

<details><summary>Lean statement</summary>

```lean
def Rule.natural_readings_that_differ.r4_rejected_batch.reading : Prop :=
  Frames.NeverChanges (L.applyBatch).rejected (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

## The old whole-phrase glossary (the flat statements and the Rust steps)

NO LONGER the link from English to Lean: that is the vocabulary above. These entries are what the flat statements are written with (each proved equivalent to its reading), and what the cucumber steps and the Rust second readings are still keyed by. Each English phrase and the one Lean definition (or model function) it is bound to: `glossary.yaml`, `lean/Wallet/Vocab.lean` and `lean/Ledger/Vocab.lean`. The last column compares that Lean definition with a second, independently written reading of the same phrase (the Rust predicate in `wallet-bdd/src/lib.rs` that the cucumber step asserts) on a grid of arguments. Agreement does not show that either reading matches the English; disagreement shows that one of them is wrong.

| Id | Kind | English phrase | Lean | Definition | Sign-off | Rust step regex identical | Lean vs Rust reading |
|---|---|---|---|---|---|---|---|
| G-balance | given | {wallet:w} has a balance of {amount:n} | `Vocab.hasBalance` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance = n` | UNREVIEWED | yes | not compared |
| G-covers | given | {amount:n} is not more than {wallet:w}'s balance | `Vocab.covers` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val` | UNREVIEWED | yes | not compared |
| G-exceeds | given | {amount:n} is more than {wallet:w}'s balance | `Vocab.exceeds` applied to `n, pre(w)` | `(n : U64) (w : Wallet) : Prop := w.balance.val < n.val` | UNREVIEWED | yes | not compared |
| G-room | given | {wallet:w}'s balance plus {amount:n} does not exceed the maximum | `Vocab.roomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max` | UNREVIEWED | yes | not compared |
| G-noroom | given | {wallet:w}'s balance plus {amount:n} exceeds the maximum | `Vocab.noRoomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := U64.max < w.balance.val + n.val` | UNREVIEWED | yes | not compared |
| W-transfer | when | {wallet:src} transfers {amount:n} to {wallet:dst} | `wallet.transfer` applied to `pre(src), pre(dst), n` | Aeneas-generated model of Rust `wallet::transfer`; returns `outcome, post(src), post(dst)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| W-deposit | when | {wallet:w} deposits {amount:n} | `wallet.Wallet.deposit` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::deposit`; returns `outcome, post(w)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| W-withdraw | when | {wallet:w} withdraws {amount:n} | `wallet.Wallet.withdraw` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::withdraw`; returns `outcome, post(w)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| T-ok | then | the operation succeeds | `Vocab.succeeds` applied to `outcome` | `(o : Outcome) : Prop := o = .Ok ()` | UNREVIEWED | yes | not compared |
| T-err | then | the operation is rejected with {error:e} | `Vocab.rejectedWith` applied to `outcome, e` | `(o : Outcome) (e : WalletError) : Prop := o = .Err e` | UNREVIEWED | yes | not compared |
| T-dec | then | {wallet:w}'s balance is decreased by {amount:n} | `Vocab.decreasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val` | UNREVIEWED | yes | not compared |
| T-inc | then | {wallet:w}'s balance is increased by {amount:n} | `Vocab.increasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val` | UNREVIEWED | yes | not compared |
| T-same | then | {wallet:w}'s balance is unchanged | `Vocab.unchanged` applied to `pre(w), post(w)` | `(pre post : Wallet) : Prop := post = pre` | UNREVIEWED | yes | not compared |
| T-total | then | the total of all balances is unchanged | `Vocab.totalUnchanged` applied to `all_pre(wallet), all_post(wallet)` | `(pre post : List Wallet) : Prop := (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum` | UNREVIEWED | yes | not compared |
| LG-holds | given | ledger {ledger:l} holds the balances {balances:bs} | `LVocab.holds` applied to `pre(l), bs` | `(l : Ledger) (bs : List U64) : Prop := l.balances.val = bs` | UNREVIEWED | yes | not compared |
| LG-sums-to | given | the balances of ledger {ledger:l} add up to {amount:s} | `LVocab.sumsTo` applied to `pre(l), s` | `(l : Ledger) (s : U64) : Prop := total l = s.val` | UNREVIEWED | yes | not compared |
| LG-sum-too-big | given | the balances of ledger {ledger:l} add up to more than the maximum | `LVocab.sumTooBig` applied to `pre(l)` | `(l : Ledger) : Prop := U64.max < total l` | UNREVIEWED | yes | not compared |
| LG-account | given | {index:i} is an account of ledger {ledger:l} | `LVocab.isAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | UNREVIEWED | yes | not compared |
| LG-no-account | given | {index:i} is not an account of ledger {ledger:l} | `LVocab.notAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := l.balances.val.length ≤ i.val` | UNREVIEWED | yes | not compared |
| LG-valid | given | the transfer {transfer:t} is valid on ledger {ledger:l} | `LVocab.validOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := valid l t` | UNREVIEWED | yes | not compared |
| LG-invalid | given | the transfer {transfer:t} is not valid on ledger {ledger:l} | `LVocab.invalidOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := ¬ valid l t` | UNREVIEWED | yes | not compared |
| LG-first-invalid | given | the first transfer of {batch:b} is not valid on ledger {ledger:l} | `LVocab.firstInvalid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := b.val ≠ [] ∧ ∀ t ∈ b.val.head?, ¬ valid l t` | UNREVIEWED | yes | not compared |
| LG-all-valid | given | every transfer of {batch:b} is valid on ledger {ledger:l} | `LVocab.allValid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := ∀ t ∈ b.val, valid l t` | UNREVIEWED | yes | not compared |
| LW-batch | when | the batch {batch:b} is applied to ledger {ledger:l} | `ledger.Ledger.apply_batch` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_batch`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-whole | when | the batch {batch:b} is applied to ledger {ledger:l} as a whole | `ledger.Ledger.apply_all` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_all`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-transfer | when | the transfer {transfer:t} is applied to ledger {ledger:l} | `ledger.Ledger.apply` applied to `pre(l), t` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply`; returns `outcome, post(l)` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-total | when | the total of ledger {ledger:l} is computed | `ledger.Ledger.total` applied to `pre(l)` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::total`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LW-balance | when | the balance of account {index:i} of ledger {ledger:l} is looked up | `ledger.Ledger.balance` applied to `pre(l), i` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::balance`; returns `outcome` | UNREVIEWED | yes | n/a (the step calls the real function) |
| LT-total-same | then | the total of ledger {ledger:l}'s balances is unchanged | `LVocab.totalUnchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := total post = total pre` | UNREVIEWED | yes | not compared |
| LT-same | then | ledger {ledger:l} is unchanged | `LVocab.unchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := post.balances.val = pre.balances.val` | UNREVIEWED | yes | not compared |
| LT-now-holds | then | ledger {ledger:l} now holds the balances {balances:bs} | `LVocab.nowHolds` applied to `post(l), bs` | `(post : Ledger) (bs : List U64) : Prop := post.balances.val = bs` | UNREVIEWED | yes | not compared |
| LT-at-most | then | the number of transfers applied is at most the length of {batch:b} | `LVocab.appliedAtMost` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val ≤ b.val.length` | UNREVIEWED | yes | not compared |
| LT-none-applied | then | no transfer is applied | `LVocab.appliedNone` applied to `outcome` | `(n : Usize) : Prop := n.val = 0` | UNREVIEWED | yes | not compared |
| LT-all-applied | then | every transfer of {batch:b} is applied | `LVocab.appliedAll` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val = b.val.length` | UNREVIEWED | yes | not compared |
| LT-exactly | then | exactly {index:k} transfers are applied | `LVocab.appliedExactly` applied to `outcome, k` | `(n : Usize) (k : Usize) : Prop := n = k` | UNREVIEWED | yes | not compared |
| LT-stops-at-invalid | then | the batch {batch:b} has stopped only at a transfer that is not valid on ledger {ledger:l} as it now stands | `LVocab.stopsAtInvalid` applied to `outcome, b, post(l)` | `(n : Usize) (b : Slice Transfer) (post : Ledger) : Prop := ∀ t ∈ b.val[n.val]?, ¬ valid post t` | UNREVIEWED | yes | not compared |
| LT-same-if-rejected | then | if it is rejected, ledger {ledger:l} is unchanged | `LVocab.unchangedIfRejected` applied to `outcome, pre(l), post(l)` | `(ok : Bool) (pre post : Ledger) : Prop := ok = false → post.balances.val = pre.balances.val` | UNREVIEWED | yes | not compared |
| LT-result | then | the result is {amount:s} | `LVocab.resultIs` applied to `outcome, s` | `(o : Option U64) (s : U64) : Prop := o = some s` | UNREVIEWED | yes | not compared |
| LT-no-result | then | there is no result | `LVocab.noResult` applied to `outcome` | `(o : Option U64) : Prop := o = none` | UNREVIEWED | yes | not compared |
| LT-some-result | then | there is a result | `LVocab.someResult` applied to `outcome` | `(o : Option U64) : Prop := o ≠ none` | UNREVIEWED | yes | not compared |
| LT-balance | then | the result is the balance of account {index:i} of ledger {ledger:l} | `LVocab.resultIsBalance` applied to `outcome, pre(l), i` | `(o : Option U64) (l : Ledger) (i : Usize) : Prop := o = l.balances.val[i.val]? ∧ o ≠ none` | UNREVIEWED | yes | not compared |
| LT-accepted | then | it is accepted | `LVocab.accepted` applied to `outcome` | `(ok : Bool) : Prop := ok = true` | UNREVIEWED | yes | not compared |
| LT-rejected | then | it is rejected | `LVocab.rejected` applied to `outcome` | `(ok : Bool) : Prop := ok = false` | UNREVIEWED | yes | not compared |
| LT-moved | then | the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed | `LVocab.moved` applied to `pre(l), post(l), t` | `(pre post : Ledger) (t : Transfer) : Prop := post.balances.val.length = pre.balances.val.length ∧ bal post t.from.val + t.amount.val = bal pre t.from.val ∧ bal post t.to.val = bal pre t.to.val + t.amount.val ∧ ∀ k < pre.balances.val.length, k ≠ t.from.val → k ≠ t.to.val → bal post k = bal pre k` | UNREVIEWED | yes | not compared |

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
- That the echo of a reading says what the author meant. It is printed so that a person can check; nobody has (no trial with readers has been run on these generated echoes).
- That any vocabulary piece means what its English says. Only a person can; no piece is signed.
- A `Rule:` statement is tied to its scenarios in one direction only: the scenarios entail the rule. That the rule says everything its scenarios say is not claimed, and usually false (a rule is one sentence; its suite says more).
- A rule statement with a hand-written proof rests on the loop lemmas, not on the scenarios beneath it.
- The compiled Rust is exercised only through the old whole-phrase steps (`wallet-bdd/tests/bdd.rs`). A NEW sentence composed from existing pieces compiles to Lean and is searched on the model, but has no cucumber step until one is written: the Rust side has no compositional reading of the vocabulary.
- The definition of each frame and its executable reading are compared on generated inputs, not proved equal. The frames with no surface form (count, monotone, agrees with a reference, independent of) are compared on a few hand-written instances only.
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

`out/graph.json`: 406 nodes, 849 edges, 61 verdicts. Evidence entries by kind: kernel-checked 108, tested 163, tool-trusted 572. Edges claimed with no evidence at all: 80 (the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.
