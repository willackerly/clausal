# Clausal: rule and scenario report (wallet and ledger)

Generated 2026-11-12T08:18:16+00:00 by `clausal/run.sh`. Lean `leanprover/lean4:v4.35.0`, Aeneas `nightly-2026.11.09-5a392f4`, Charon `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, clausal 7bd9f57bc2ba (clausal-rule/4).

Each `Rule:` line and each scenario below is an English claim about one of the Rust crates `clausal/wallet` (three straight-line functions) and `clausal/ledger` (loops over a `Vec` and a slice). The sentence is not bound as a whole: it is **assembled from typed pieces** of a Clausebook (40 domain words, 28 modifiers, 25 frames). The composition is compiled to one Lean statement about the Aeneas-generated Lean model of the crate, and **echoed back in fixed, slot-structured English** (applies to / assuming / then / defaults applied) so the author can check that the tool read the sentence as it was meant. The echo is the first thing printed for every rule and scenario; the Lean is underneath. The statement is then proved, refuted or left open, and every link in that chain is labelled with the kind of evidence behind it:

| Evidence kind | Meaning here |
|---|---|
| kernel-checked | Lean's kernel accepted a proof of exactly the stated theorem. Holds for every input the statement quantifies over. |
| tested | Evaluated on particular inputs: Examples rows on the compiled Rust (cucumber-rs, one generic step) and on the Lean model, a boundary grid on the model, counterexamples replayed on the Rust, every compiled reading on generated inputs three ways (the definition of each frame, its executable reading, and the Rust reading of every piece on the compiled crate), and the two readings of each old glossary phrase compared on a grid. |
| tool-trusted | Produced by a program whose output is not proved correct: Charon + Aeneas (Rust to Lean), Aeneas's hand-written models of std operations, clausal (sentence to composition to statement), and the audits that read facts out of the Lean environment. |
| human-asserted | A person's say-so: that each Clausebook piece means its Lean definition. Nothing checks this. It exists only where someone has signed off. |

**How a Rule relates to its scenarios.** The rule line compiles to ONE Lean statement that covers every input (fail-closed: rejected calls included, and the call must answer). The scenarios beneath it are its tested instances (their Examples rows run on the compiled Rust) and, where they are outlines, its **parts**: a generated, kernel-checked theorem `<rule>.from_scenarios` derives the rule statement from the scenario statements, by cases on their Givens. Where that script does not go through, a hand-written proof of exactly the rule statement may stand in (`lean/Wallet/RuleProofs/`). A rule statement found false by the reading search is refuted in the kernel at that input. A scenario may say more than its rule (a progress scenario under a safety rule); the block says which scenarios are parts.

**Two statements per scenario.** The reading compiled from the Clausebook is what is shown and what the verdict is about. For the OLDER scenarios the hand-written proofs, the counterexample search and the refutations are about the *flat statement* of the old whole-phrase glossary, unchanged; a generated kernel-checked equivalence carries the verdict across ([Regression](#regression-every-old-statement-against-its-new-reading-plan-node-v3)). A **NEW sentence** (marked so) has no entry in the old glossary: its flat proof obligation is generated from the pieces, a supplied proof of it is carried to the reading by a kernel-checked equivalence, and it runs on the compiled Rust through the generic step ([New sentences, end to end](#new-sentences-end-to-end)).

## Rules

Generated from `out/graph.json` (`python3 -m clausal rules` prints the same from the stored graph). The full block of each rule, with its reading and what it rests on, is under [Rules and their scenarios](#rules-and-their-scenarios).

| Rule | The rule statement | Its scenarios | Examples on Rust / on model | Suite adequacy (informational) |
|---|---|---|---|---|
| Rule: A transfer never changes the total of all balances (`features/wallet.feature:12`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 1 PROVED-INSTANCE | 7 / 7 of 7 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A withdrawal always answers, and a successful withdrawal decreases the wallet's balance by exactly the amount, and a rejected withdrawal never changes the wallet's balance (`features/wallet.feature:75`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A deposit always answers, and a successful deposit increases the wallet's balance by exactly the amount, and a rejected deposit never changes the wallet's balance (`features/wallet.feature:105`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A transfer for which the amount is not more than the sender's balance is always accepted (`features/wallet.feature:135`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: A deposit earns interest (`features/wallet.feature:156`) | **UNBOUND (no statement)** | **NO SCENARIO PROVED**<br>1 UNBOUND | - / 0 of 0 | not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios of this group are NEW sentences that have none |
| Rule: A batch never changes the total of all balances of the ledger (`features/ledger.feature:13`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL | 12 / 12 of 12 | suite rules out: reject-all, identity, constant; still allows: no-op: reports every transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the search grid] |
| Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, the number of transfers applied is zero and the ledger is unchanged (`features/ledger.feature:66`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL, 2 PROVED-INSTANCE | 8 / 8 of 8 | suite rules out: no-op, constant; still allows: reject-all: always answers `0` and leaves the state as it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid] |
| Rule: For a batch for which every transfer of the batch is valid on the ledger, the number of transfers applied is the length of the batch (`features/ledger.feature:111`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: A transfer is accepted exactly when the transfer is valid on the ledger, and a rejected transfer never changes the ledger, and for a successful transfer, the amount of the transfer has moved between its accounts in the ledger and no other balance changed (`features/ledger.feature:130`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 8 / 8 of 8 | suite rules out: reject-all, no-op, identity, constant; still allows: (none found) |
| Rule: A computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum (`features/ledger.feature:164`) | **PROVED FOR ALL INPUTS (by a hand-written proof)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 8 / 8 of 8 | suite rules out: reject-all, no-op; still allows: (none found) |
| Rule: A computation of the total is always accepted (`features/ledger.feature:195`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: no scenario of this group is meant to be proved |
| Rule: For a lookup, the result is the balance of the account in the ledger (`features/ledger.feature:211`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 4 / 4 of 4 | suite rules out: reject-all, no-op; still allows: (none found) |
| Rule: A rejected batch applied as a whole never changes the ledger, and a batch applied as a whole never changes the total of all balances of the ledger (`features/ledger.feature:238`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>3 PROVED-FOR-ALL, 3 PROVED-INSTANCE | 10 / 10 of 10 | suite rules out: no-op, constant; still allows: reject-all: always answers `false` and leaves the state as it was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid] |
| Rule: A batch followed by a computation of the total is accepted exactly when the total of the balances of the ledger is at most the maximum (`features/ledger.feature:304`) | **PROVED FOR ALL INPUTS (by a hand-written proof)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>2 PROVED-FOR-ALL | 5 / 5 of 5 | [ledger.Ledger.apply_batch] suite rules out: (nothing); still allows: reject-all: always answers `0` and leaves the state as it was [no scenario counted is false of it on the search grid]; no-op: reports every transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the search grid]; identity: answers as the code does, but never changes the state [no scenario counted is false of it on the search grid]; constant (4 of 9 variants): always answers `1` and leaves the state as it was; always answers `2` and leaves the state as it was; and 2 more [no scenario counted is false of it on the search grid]<br>[ledger.Ledger.total] suite rules out: reject-all, no-op; still allows: (none found) |
| Rule: An internal fund transfer never changes the aggregate account value of the ledger (`features/ledger_rules.feature:14`) | **PROVED FOR ALL INPUTS (from its scenarios)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>1 PROVED-FOR-ALL | 2 / 2 of 2 | not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios of this group are NEW sentences that have none |
| Rule: An internal transfer never changes the total of all balances of the ledger (`features/ledger_rules.feature:29`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger (`features/ledger_rules.feature:32`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>1 PROVED-FOR-ALL | 3 / 3 of 3 | not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios of this group are NEW sentences that have none |
| Rule: For a lookup for which the account is not an account of the ledger, there is no result (`features/ledger_rules.feature:49`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch never leaves the total of all balances of the ledger above the maximum (`features/ledger_rules.feature:52`) | **REFUTED (false at a concrete input, kernel-checked)** | **A SCENARIO IS SHOWN FALSE**<br>1 REFUTED | 2 / 2 of 2 | not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios of this group are NEW sentences that have none |
| Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards (`features/ledger_rules.feature:67`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer never loses acceptance when the amount is smaller (`features/ledger_rules.feature:72`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer never loses acceptance when the amount is larger (`features/ledger_rules.feature:75`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A lookup never loses that there is a result when the ledger is extended (`features/ledger_rules.feature:78`) | **TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A lookup agrees with the reference lookup (`features/ledger_rules.feature:84`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A lookup agrees with the zero-default lookup (`features/ledger_rules.feature:87`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A lookup gives the same answer when the ledger agrees at the account (`features/ledger_rules.feature:91`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer gives the same answer when only the amount differs (`features/ledger_rules.feature:94`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer gives the same answer when the amount is larger, if it is rejected (`features/ledger_rules.feature:98`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer gives the same answer when the amount is larger, if it is accepted (`features/ledger_rules.feature:101`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch (`features/ledger_rules.feature:105`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a batch, every transfer of the batch is a transfer at which the batch stopped (`features/ledger_rules.feature:108`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger (`features/ledger_rules.feature:112`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected (`features/ledger_rules.feature:115`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied (`features/ledger_rules.feature:123`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch agrees with its transfers applied one at a time until one is rejected (`features/ledger_rules.feature:126`) | **TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer never leaves the balance of account 4 of the ledger above zero (`features/ledger_rules.feature:137`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A successful transfer never changes the ledger (`features/ledger_rules.feature:141`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a rejected transfer, the total of all balances of the ledger is now zero (`features/ledger_rules.feature:144`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch followed by a computation of the total is always accepted (`features/ledger_rules.feature:147`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer is accepted whenever the transfer is valid on the ledger (`features/ledger_rules.feature:154`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing (`features/ledger_rules.feature:157`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a batch, the number of transfers applied is at least the length of the batch (`features/ledger_rules.feature:160`) | **REFUTED (false at a concrete input, kernel-checked)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A batch never leaves the total of all balances of the ledger below zero (`features/ledger_rules.feature:163`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards (`features/ledger_rules.feature:166`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero (`features/ledger_rules.feature:169`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)**<br> | - / 0 of 0 | not assessed: there is no scenario beneath this rule |
| Rule: A successful transfer never changes the total of all balances of the ledger (`features/ledger_rules.feature:172`) | **PROVED FOR ALL INPUTS (by a supplied proof of its obligation)** | **SCENARIOS PROVED FOR ALL INPUTS**<br>1 PROVED-FOR-ALL | 2 / 2 of 2 | not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios of this group are NEW sentences that have none |
| (scenarios of `Feature: Negative controls` that are not under a Rule) (`features/negative.feature`) | - | **SOME SCENARIOS PROVED**<br>1 VACUOUS, 1 PROVED-FOR-ALL | 1 / 1 of 2 | not assessed: its scenarios are tagged @control |

46 rule statements: 28 PROVED-FOR-ALL, 15 REFUTED, 1 UNBOUND, 2 TESTED-ONLY. Every rule statement got the verdict it was expected to get.


## Summary

| Scenario | Verdict | Expected | Rows on Rust / on model | Flags |
|---|---|---|---|---|
| A covered transfer moves the money and conserves the total (`features/wallet.feature:18`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (8 of 8); UNREVIEWED CLAUSEBOOK (21 of 21) |
| Transferring more than the sender has is rejected and changes nothing (`features/wallet.feature:35`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (15 of 15) |
| A transfer the receiver has no room for is rejected and changes nothing (`features/wallet.feature:50`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED CLAUSEBOOK (17 of 17) |
| Transferring more than you have is rejected and changes nothing (`features/wallet.feature:66`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (14 of 14) |
| A covered withdrawal succeeds and takes exactly the amount (`features/wallet.feature:78`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (15 of 15) |
| Withdrawing more than the balance is rejected and changes nothing (`features/wallet.feature:92`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (15 of 15) |
| A deposit with room succeeds and adds exactly the amount (`features/wallet.feature:108`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A deposit that would overflow is rejected and changes nothing (`features/wallet.feature:122`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A transfer the sender can afford always succeeds (`features/wallet.feature:141`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED CLAUSEBOOK (18 of 18) |
| A deposit earns interest (`features/wallet.feature:161`) | **UNBOUND** | UNBOUND | - | - |
| Applying any batch of transfers conserves the total of all balances (`features/ledger.feature:20`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 6 / 6 of 6 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (15 of 15) |
| A batch stops only at a transfer that cannot be carried out (`features/ledger.feature:39`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (18 of 18) |
| Two batches applied one after the other conserve the total (`features/ledger.feature:54`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (19 of 19) |
| A batch whose first transfer is invalid changes nothing (`features/ledger.feature:69`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (22 of 22) |
| The number of transfers applied is at most the length of the batch (`features/ledger.feature:83`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (14 of 14) |
| A batch of two valid transfers is applied in full (`features/ledger.feature:96`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A batch stops at its first invalid transfer and keeps what it has applied (`features/ledger.feature:104`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:118`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (18 of 18) |
| A valid transfer is accepted and moves exactly its amount (`features/ledger.feature:133`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (6 of 6); UNREVIEWED CLAUSEBOOK (29 of 29) |
| An invalid transfer is rejected and changes nothing (`features/ledger.feature:148`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (20 of 20) |
| The total is the sum of the balances when that fits (`features/ledger.feature:167`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (17 of 17) |
| The total of balances that do not fit is reported as absent (`features/ledger.feature:182`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (19 of 19) |
| The total of a ledger can always be computed (`features/ledger.feature:200`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (13 of 13) |
| Looking up an existing account gives its balance (`features/ledger.feature:214`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (15 of 15) |
| Looking up an account that does not exist gives nothing (`features/ledger.feature:226`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A batch applied as a whole that is rejected leaves the ledger unchanged (`features/ledger.feature:243`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 4 / 4 of 4 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A batch applied as a whole whose first transfer is invalid is rejected and changes nothing (`features/ledger.feature:256`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (22 of 22) |
| Applying a batch as a whole conserves the total of all balances (`features/ledger.feature:268`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3); UNREVIEWED CLAUSEBOOK (15 of 15) |
| A batch of valid transfers applied as a whole is accepted and applied (`features/ledger.feature:280`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (14 of 14) |
| A batch applied as a whole is rolled back when its third transfer is invalid (`features/ledger.feature:289`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (16 of 16) |
| A batch applied as a whole is rolled back when a later transfer is invalid (`features/ledger.feature:297`) | **PROVED-INSTANCE** | PROVED-INSTANCE | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4); UNREVIEWED CLAUSEBOOK (16 of 16) |
| The total computed after any batch is the total before it, when that total fits (`features/ledger.feature:311`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (19 of 19) |
| The total computed after any batch is still absent when it did not fit before (`features/ledger.feature:326`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (21 of 21) |
| a transfer between two accounts of the ledger (`features/ledger_rules.feature:17`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED CLAUSEBOOK (15 of 15) |
| a transfer of more than the sender holds is rejected and changes nothing (`features/ledger_rules.feature:35`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED CLAUSEBOOK (21 of 21) |
| after a batch the total of all balances is within the maximum (`features/ledger_rules.feature:56`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED CLAUSEBOOK (15 of 15) |
| A rejected transfer leaves every single balance as it was (`features/ledger_rules.feature:176`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED CLAUSEBOOK (22 of 22) |
| A withdrawal that is both covered and not covered (`features/negative.feature:11`) | **VACUOUS** | VACUOUS | 0 / 0 of 1 | ROW OUTSIDE GIVENS; UNREVIEWED GLOSSARY (5 of 5); UNREVIEWED CLAUSEBOOK (14 of 14) |
| A deposit does not touch a bystander (`features/negative.feature:25`) | **PROVED-FOR-ALL (1 of 2 Thens substantive)** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); TRIVIAL-THEN; FRAME-TRIVIAL; UNREVIEWED CLAUSEBOOK (17 of 17) |

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
| `ledger.Ledger.total` | **NOT SHOWN**: `Coverage.g5` (1 scenarios): their Givens do not cover every input; `Coverage.g6` (1 scenarios): their Givens do not cover every input | "the result is {amount:s}" (only when: the total of the balances of ledger Main is <sum>); "there is no result" (only when: the total of the balances of ledger Main is more than the maximum); "the result is {amount:s}" (only when: the total of the balances of ledger Main is <sum>; after: the batch <batch> is applied to ledger Main); "there is no result" (only when: the total of the balances of ledger Main is more than the maximum; after: the batch <batch> is applied to ledger Main) | **nothing** | total_is_sum: PROVED-FOR-ALL; total_overflow: PROVED-FOR-ALL; total_always_available: REFUTED; batch_then_total: PROVED-FOR-ALL; batch_then_total_overflow: PROVED-FOR-ALL |
| `ledger.Ledger.apply` | **yes**: kernel-checked `Coverage.g4` over 2 proved scenarios | "it is accepted" (only when: the transfer <t> is valid on ledger Main); "it is rejected" (only when: the transfer <t> is not valid on ledger Main) | "the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed" (only when: the transfer <t> is valid on ledger Main); "the total of ledger {ledger:l}'s balances is unchanged" (only when: the transfer <t> is valid on ledger Main); "ledger {ledger:l} is unchanged" (only when: the transfer <t> is not valid on ledger Main) | transfer_valid_moves: PROVED-FOR-ALL; transfer_invalid_rejected: PROVED-FOR-ALL |
| `ledger.Ledger.apply_batch_loop.body` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch_loop` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch` | **yes**: kernel-checked `Coverage.g3` over 4 proved scenarios | "every transfer at which {batch:b} stopped is not valid on ledger {ledger:l} afterwards" (always); "the number of transfers applied is at most the length of {batch:b}" (only when: after: the batch <first> is applied to ledger Main); "the number of transfers applied is zero" (only when: the first transfer of <batch> is not valid on ledger Main); "the number of transfers applied is at most the length of {batch:b}" (always) | "the total of ledger {ledger:l}'s balances is unchanged" (always); "every transfer at which {batch:b} stopped is not valid on ledger {ledger:l} afterwards" (always); "the total of ledger {ledger:l}'s balances is unchanged" (only when: after: the batch <first> is applied to ledger Main); "ledger {ledger:l} is unchanged" (only when: the first transfer of <batch> is not valid on ledger Main) | batch_conserves: PROVED-FOR-ALL; batch_stops_at_invalid: PROVED-FOR-ALL; two_batches_conserve: PROVED-FOR-ALL; batch_first_invalid: PROVED-FOR-ALL; batch_count_bounded: PROVED-FOR-ALL; batch_example_all: PROVED-INSTANCE; batch_example_stop: PROVED-INSTANCE; batch_all_valid_all_applied: REFUTED; batch_then_total: PROVED-FOR-ALL; batch_then_total_overflow: PROVED-FOR-ALL |
| `ledger.Ledger.apply_all` | **yes**: kernel-checked `Coverage.g8` over 3 proved scenarios | "if it is rejected, ledger {ledger:l} is unchanged" (always); "it is rejected" (only when: the first transfer of <batch> is not valid on ledger Main) | "if it is rejected, ledger {ledger:l} is unchanged" (always); "ledger {ledger:l} is unchanged" (only when: the first transfer of <batch> is not valid on ledger Main); "the total of ledger {ledger:l}'s balances is unchanged" (always) | whole_rejected_unchanged: PROVED-FOR-ALL; whole_first_invalid: PROVED-FOR-ALL; whole_conserves: PROVED-FOR-ALL; whole_example_accept: PROVED-INSTANCE; whole_example_rollback_late: PROVED-INSTANCE; whole_example_rollback: PROVED-INSTANCE |

Mutation run of 2026-11-12T05:58:14+00:00: 45 mutants of `wallet/src/lib.rs` and `ledger/src/lib.rs`. **A scenario is shown false of 45 of them** (an example row differs on the compiled Rust, or the search finds a counterexample). For 0 more (-) the run fails only because a hand-written proof or lemma stopped compiling, which is not detection by the scenarios. 0 make no difference to the run at all. **These results are for an OLDER version of the Rust, features, glossary or proofs; rerun.**

A lost proof means the proof (or a lemma it depends on) no longer compiles; it does not by itself mean the scenario's statement is false of the mutant. A new counterexample does.

| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs lost | New counterexamples | Verdicts that changed | A scenario shown false | Run fails |
|---|---|---|---|---|---|---|---|---|---|
| d1 | `wallet::{wallet::Wallet}::deposit` | no overflow check: the balance wraps around | caught | caught (2 rows) | 2 | 1 | deposit_with_room: TESTED-ONLY; deposit_overflow: REFUTED | yes | yes |
| d2 | `wallet::{wallet::Wallet}::deposit` | a successful deposit sets the balance to the amount instead of adding it | caught | caught (2 rows) | 1 | 1 | deposit_with_room: REFUTED | yes | yes |
| d3 | `wallet::{wallet::Wallet}::deposit` | overflow is reported as insufficient funds | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes | yes |
| d4 | `wallet::{wallet::Wallet}::deposit` | a deposit that reaches exactly the maximum is rejected | MISSED | caught (2 rows) | 2 | 2 | deposit_with_room: REFUTED; bystander_unchanged: REFUTED | yes | yes |
| d5 | `wallet::{wallet::Wallet}::deposit` | a rejected deposit empties the wallet | caught | caught (2 rows) | 1 | 1 | deposit_overflow: REFUTED | yes | yes |
| d6 | `wallet::{wallet::Wallet}::deposit` | a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 1 | 1 | deposit_with_room: REFUTED | yes | yes |
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
| lt1 | `ledger::{ledger::Ledger}::total` | LOOP off-by-one bound: the last balance is not added | caught | caught (9 rows) | 7 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lt2 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: the sum is overwritten by each balance instead of accumulated | caught | caught (10 rows) | 7 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lt3 | `ledger::{ledger::Ledger}::total` | LOOP skipped element: summing starts at account 1 | caught | caught (12 rows) | 7 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lt4 | `ledger::{ledger::Ledger}::total` | an overflowing total is reported as u64::MAX instead of absent | caught | caught (5 rows) | 7 | 2 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lt5 | `ledger::{ledger::Ledger}::total` | LOOP wrong accumulator: wrapping addition, so an overflowing total wraps around | caught | caught (5 rows) | 7 | 2 | total_is_sum: TESTED-ONLY; total_overflow: COUNTEREXAMPLE; total_always_available: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| la1 | `ledger::{ledger::Ledger}::apply` | no check that sender and receiver differ: a self-transfer creates money | caught | caught (2 rows) | 20 | 9 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: REFUTED; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: REFUTED; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: REFUTED | yes | yes |
| la2 | `ledger::{ledger::Ledger}::apply` | transferring the sender's whole balance is rejected (< became <=) | caught | caught (6 rows) | 20 | 4 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: COUNTEREXAMPLE; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| la3 | `ledger::{ledger::Ledger}::apply` | the receiver is never credited (money vanishes) | caught | caught (17 rows) | 20 | 11 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: REFUTED; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: REFUTED | yes | yes |
| la4 | `ledger::{ledger::Ledger}::apply` | the sender is never debited (money is created) | caught | caught (16 rows) | 20 | 10 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: REFUTED; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: REFUTED | yes | yes |
| la5 | `ledger::{ledger::Ledger}::apply` | receiver bounds check off by one (>= became >): indexing one past the end panics | caught | caught (3 rows) | 20 | 13 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: TESTED-ONLY; transfer_invalid_rejected: COUNTEREXAMPLE; whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: COUNTEREXAMPLE; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: COUNTEREXAMPLE | yes | yes |
| la6 | `ledger::{ledger::Ledger}::apply` | a transfer of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | 20 | 8 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: REFUTED; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: REFUTED | yes | yes |
| lb1 | `ledger::{ledger::Ledger}::apply_batch` | LOOP missing early exit: the batch carries on after a rejected transfer and counts it | caught | caught (7 rows) | 18 | 5 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lb2 | `ledger::{ledger::Ledger}::apply_batch` | LOOP off-by-one bound: the last transfer of the batch is never applied | caught | caught (6 rows) | 18 | 3 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: COUNTEREXAMPLE; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lb3 | `ledger::{ledger::Ledger}::apply_batch` | LOOP skipped element: every second transfer is skipped (i += 2) | caught | caught (5 rows) | 18 | 6 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: COUNTEREXAMPLE; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lb4 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong result: the batch length is returned instead of the number applied | caught | caught (7 rows) | 18 | 5 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lb5 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong counter: a rejected transfer is counted as applied | caught | caught (8 rows) | 18 | 6 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: COUNTEREXAMPLE; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lb6 | `ledger::{ledger::Ledger}::apply_batch` | LOOP wrong early exit: the batch stops after the first APPLIED transfer | caught | caught (6 rows) | 18 | 3 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: REFUTED; batch_example_stop: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lw1 | `ledger::{ledger::Ledger}::apply_all` | no rollback: a rejected batch keeps the transfers applied before the failure | caught | caught (5 rows) | 9 | 3 | whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lw2 | `ledger::{ledger::Ledger}::apply_all` | a rolled-back batch is reported as applied | caught | caught (3 rows) | 9 | 3 | whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: COUNTEREXAMPLE; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lw3 | `ledger::{ledger::Ledger}::apply_all` | every batch is rolled back and rejected (< became <=) | caught | caught (1 rows) | 9 | 1 | whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lg1 | `ledger::{ledger::Ledger}::balance` | lookup bounds check off by one (< became <=): looking up account `len` panics | caught | caught (2 rows) | 5 | 1 | balance_of_account: TESTED-ONLY; balance_no_account: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| lg2 | `ledger::{ledger::Ledger}::balance` | lookup returns the balance of account 0 whatever the account | caught | caught (1 rows) | 5 | 1 | balance_of_account: REFUTED; balance_no_account: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| r1 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP cap: the batch silently stops after three transfers | MISSED | caught (1 rows) | 18 | 1 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| r2 | `ledger::{ledger::Ledger}::total` | REVIEW LOOP cap: only the first three accounts are summed | MISSED | caught (4 rows) | 7 | 4 | total_is_sum: COUNTEREXAMPLE; total_overflow: COUNTEREXAMPLE; total_always_available: COUNTEREXAMPLE; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: COUNTEREXAMPLE; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| r3 | `ledger::{ledger::Ledger}::apply_all` | REVIEW atomicity: no rollback once two or more transfers have been applied | MISSED | caught (3 rows) | 9 | 2 | whole_rejected_unchanged: COUNTEREXAMPLE; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; f_other_account_untouched: TESTED-ONLY | yes | yes |
| r4 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP wrong counter: a rejected LAST transfer (not the first) is counted as applied | caught | caught (2 rows) | 18 | 2 | batch_conserves: TESTED-ONLY; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: TESTED-ONLY; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: COUNTEREXAMPLE; whole_example_rollback: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |
| r5 | `ledger::{ledger::Ledger}::apply_batch` | REVIEW LOOP state corruption: one unit is minted to account 0 at the start of the third iteration (conservation is false, but only for batches whose first two transfers apply and that have a third) | caught | caught (3 rows) | 18 | 4 | batch_conserves: COUNTEREXAMPLE; batch_stops_at_invalid: TESTED-ONLY; two_batches_conserve: COUNTEREXAMPLE; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_example_all: TESTED-ONLY; batch_example_stop: TESTED-ONLY; batch_all_valid_all_applied: COUNTEREXAMPLE; whole_rejected_unchanged: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_conserves: COUNTEREXAMPLE; whole_example_accept: TESTED-ONLY; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY; batch_then_total: COUNTEREXAMPLE; batch_then_total_overflow: TESTED-ONLY; readme_transfer_keeps_aggregate: TESTED-ONLY; n2_short_sender_rejected: TESTED-ONLY; n4_total_within_maximum_after_batch: COUNTEREXAMPLE; f_other_account_untouched: TESTED-ONLY | yes | yes |

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

## Layered evidence from one compiled rule

From the composition tree that gives a sentence its Lean statement and its echo, `clausal gen` also writes a property test and a bounded-model-checking harness (`evidence/`, generated; `clausal/evgen.py`). No test code is written per rule: both assert one generated predicate, straight-line Rust over one typed reading per Clausebook piece (`evidence/src/typed.rs`). The property test's generators are derived from the types of the rule's variables and from its Givens. The bounded check runs each rule at every rung of one fixed ladder of sizes. Every input either of them finds false is evaluated on the Lean model through the reading: if it fails there too it becomes the reading's counterexample and gets a kernel-checked refutation; if the model does not fail where the compiled Rust did, the verdict is flagged MODEL MISMATCH. Each rule's block below has the ladder: example rows, property test, bounded check, proof, what each rests on, and which is the strongest evidence held. Nothing is called proved without a kernel-checked theorem.

| | |
|---|---|
| Readings with a generated property test and Kani harness | 83 (every compiled scenario and Rule line) |
| Property test | proptest 1.12.0, seed 20261111, 10000 cases IN SCOPE per reading, collections up to 6 items, shrinking: 63 not falsified, 19 shown false, 0 did not finish, 1 had no input in scope, 0 READING MISMATCH |
| Generated predicate against the tree evaluator | compared at every generated case (2405688 cases): 0 readings differ |
| Cost of the property tests | 17.23 s for all readings (build 0.27 s) |
| Bounded check | Kani Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0; size ladder (accounts, transfers) = (2, 1), (2, 2), (4, 1), (2, 3), (6, 4), the same for every rule; 30 s per harness, 6 at a time: 269 harnesses, 180 verified, 61 failed, 28 no answer in time, 0 error |
| Bounded check, per reading | 47 hold at every rung; 17 hold at some rungs and give no answer at others; 19 shown false; 0 no answer at any rung |
| Cost of the bounded checks | 384.7 s wall-clock; 748 s of solver time in the harnesses that answered; 70.8 s more to get and replay the failing inputs |
| Falsifying inputs found (property test + bounded check) | 38: 36 fail on the Lean model too, 0 MODEL MISMATCH, 2 not evaluated on the model |

| Reading | Source | Falsifying input | Compiled Rust | Lean model |
|---|---|---|---|---|
| `Spec.wallet.transfer_always_succeeds` | property test | `{"a": "18446744073709551615", "alice_state": "18446744073709551615", "amount": "18446744073709551615", "b": "4", "bob_state": "4"}` | fails | fails |
| `Spec.wallet.transfer_always_succeeds` | bounded check | `{"a": "13835058055282163711", "alice_state": "13835058055282163711", "amount": "4611686018427387903", "b": "18446744073709551615", "bob_state": "18446744073709551615"}` | fails | fails |
| `Spec.ledger.batch_all_valid_all_applied` | property test | `{"balances": "[0, 2, 0, 0, 0, 0]", "batch": "[1->2:1, 1->2:2]", "main_state": "[0, 2, 0, 0, 0, 0]"}` | fails | fails |
| `Spec.ledger.batch_all_valid_all_applied` | bounded check | `{"balances": "[2305843009213693954, 16140901064495857660]", "batch": "[1->0:9223372036854775807, 1->0:6917529027641081854]", "main_state": "[2305843009213693954, 16140901064495857660]"}` | fails | fails |
| `Spec.ledger.total_always_available` | property test | `{"balances": "[4, 18446744073709551615]", "main_state": "[4, 18446744073709551615]"}` | fails | fails |
| `Spec.ledger.total_always_available` | bounded check | `{"balances": "[18446744073709551615, 18446744073709551615]", "main_state": "[18446744073709551615, 18446744073709551615]"}` | fails | fails |
| `Spec.ledger_rules.n4_total_within_maximum_after_batch` | property test | `{"balances": "[18446744073709551615, 1]", "batch": "[]", "main_state": "[18446744073709551615, 1]"}` | fails | fails |
| `Spec.ledger_rules.n4_total_within_maximum_after_batch` | bounded check | `{"balances": "[4, 18446744073709551615]", "batch": "[]", "main_state": "[4, 18446744073709551615]"}` | fails | fails |
| `Rule.wallet.transfer_affordable` | property test | `{"the_amount": "1", "the_receiver": "18446744073709551615", "the_sender": "2"}` | fails | fails |
| `Rule.wallet.transfer_affordable` | bounded check | `{"the_amount": "1", "the_receiver": "18446744073709551615", "the_sender": "1"}` | fails | fails |
| `Rule.ledger.batch_all_valid` | property test | `{"the_batch": "[0->1:14779828575414881320, 0->5:1]", "the_ledger": "[14779828575414881320, 0, 3666915498294670295, 0, 0, 0]"}` | fails | fails |
| `Rule.ledger.batch_all_valid` | bounded check | `{"the_batch": "[0->1:9223372036854775809, 0->1:7242086547668779013]", "the_ledger": "[11925865344506247229, 1049636799838765050]"}` | fails | fails |
| `Rule.ledger.total_always` | property test | `{"the_ledger": "[5003681978720493492, 13443062094989058124]"}` | fails | fails |
| `Rule.ledger.total_always` | bounded check | `{"the_ledger": "[1, 18446744073709551615]"}` | fails | fails |
| `Rule.ledger_rules.n4_total_stays_within_maximum` | property test | `{"the_batch": "[]", "the_ledger": "[18446744073709551615, 1]"}` | fails | fails |
| `Rule.ledger_rules.n4_total_stays_within_maximum` | bounded check | `{"the_batch": "[1->0:4611686018427387909]", "the_ledger": "[18446744073709551610, 13835058055282163717]"}` | fails | fails |
| `Rule.ledger_rules.mono_larger_amount` | property test | `{"the_ledger": "[0, 0, 1, 0]", "the_ledger_2": "[0, 0, 1, 0]", "the_transfer": "2->3:0", "the_transfer_2": "2->3:2"}` | fails | fails |
| `Rule.ledger_rules.mono_larger_amount` | bounded check | `{"the_ledger": "[9223372036854775808, 9223372036854775808]", "the_ledger_2": "[9223372036854775808, 9223372036854775808]", "the_transfer": "0->1:1", "the_transfer_2": "0->1:9223372036854775808"}` | fails | fails |
| `Rule.ledger_rules.agrees_zero_default` | property test | `{"the_account": "0", "the_ledger": "[]"}` | fails | fails |
| `Rule.ledger_rules.agrees_zero_default` | bounded check | `{"the_account": "9223372036854775808", "the_ledger": "[0]"}` | fails | not evaluated |
| `Rule.ledger_rules.same_answer_any_amount` | property test | `{"the_ledger": "[1, 18446744073709551615, 0, 0]", "the_ledger_2": "[1, 18446744073709551615, 0, 0]", "the_transfer": "0->1:0", "the_transfer_2": "0->1:1"}` | fails | fails |
| `Rule.ledger_rules.same_answer_any_amount` | bounded check | `{"the_ledger": "[18446744073709551615, 1]", "the_ledger_2": "[18446744073709551615, 1]", "the_transfer": "0->1:18446744073709551615", "the_transfer_2": "0->1:18446744073709551614"}` | fails | fails |
| `Rule.ledger_rules.accepted_stays_accepted` | property test | `{"the_ledger": "[0, 13808191158069793772, 0, 2319276457819878922]", "the_ledger_2": "[0, 13808191158069793772, 0, 2319276457819878922]", "the_transfer": "3->0:0", "the_transfer_2": "3->0:2319276457819878923"}` | fails | fails |
| `Rule.ledger_rules.accepted_stays_accepted` | bounded check | `{"the_ledger": "[9223372036854775808, 9223372036854775808]", "the_ledger_2": "[9223372036854775808, 9223372036854775808]", "the_transfer": "0->1:1", "the_transfer_2": "0->1:9223372036854775808"}` | fails | fails |
| `Rule.ledger_rules.batch_is_stopped` | property test | `{"the_batch": "[0->0:0, 0->0:1]", "the_ledger": "[]"}` | fails | fails |
| `Rule.ledger_rules.batch_is_stopped` | bounded check | `{"the_batch": "[0->1:9223372036854775807]", "the_ledger": "[18446744073709551614, 9223372036854775808]"}` | fails | fails |
| `Rule.ledger_rules.some_invalid_rejected` | property test | `{"the_batch": "[0->1:1, 1->0:1]", "the_ledger": "[1, 0]"}` | fails | fails |
| `Rule.ledger_rules.some_invalid_rejected` | bounded check | `{"the_batch": "[0->1:24206847997116417, 1->0:6485746413366935563]", "the_ledger": "[444730463202836485, 6462665465276661766]"}` | fails | fails |
| `Rule.ledger_rules.e1_fifth_account_empty` | property test | `{"the_ledger": "[0, 0, 0, 0, 1]", "the_transfer": "0->0:0"}` | fails | fails |
| `Rule.ledger_rules.e1_fifth_account_empty` | bounded check | `{"the_ledger": "[18446744073709551615, 18446744073709551615, 18446744073709551615, 18446744073709551615, 4, 18446744073709551615]", "the_transfer": "0->4:0"}` | fails | fails |
| `Rule.ledger_rules.successful_changes_nothing` | property test | `{"the_ledger": "[0, 0, 0, 18446744073709551614]", "the_transfer": "3->0:1"}` | fails | fails |
| `Rule.ledger_rules.successful_changes_nothing` | bounded check | `{"the_ledger": "[18446744073709551615, 18446744073709551614]", "the_transfer": "0->1:1"}` | fails | fails |
| `Rule.ledger_rules.rejected_empties_ledger` | property test | `{"the_ledger": "[1]", "the_transfer": "0->0:0"}` | fails | fails |
| `Rule.ledger_rules.rejected_empties_ledger` | bounded check | `{"the_ledger": "[4, 0]", "the_transfer": "0->0:18446744073709551615"}` | fails | fails |
| `Rule.ledger_rules.batch_then_total_always` | property test | `{"the_batch": "[]", "the_ledger": "[428257041932146292, 18018487031777405324]"}` | fails | fails |
| `Rule.ledger_rules.batch_then_total_always` | bounded check | `{"the_batch": "[0->1:33]", "the_ledger": "[48, 18446744073709551583]"}` | fails | fails |
| `Rule.ledger_rules.f_result_at_least` | property test | `{"the_batch": "[0->0:0]", "the_ledger": "[]"}` | fails | fails |
| `Rule.ledger_rules.f_result_at_least` | bounded check | `{"the_batch": "[18446744073709551615->18446744073709551615:18446744073709551615]", "the_ledger": "[]"}` | fails | not evaluated |

## Rules and their scenarios

One block per `Rule:` (and one per feature for scenarios that sit under no rule), generated from `out/graph.json`: the rule line, **its compiled reading echoed in English**, the verdict of the rule statement, the scenarios beneath it and whether each is a part the rule is proved from, the example rows, the suite note, and what the result rests on. Beneath each block: the rule's Lean statement, then every scenario with its own reading, verdict and (folded) Lean.

### Rule: A transfer never changes the total of all balances

```text
Rule: A transfer never changes the total of all balances   [features/wallet.feature:12]   tags @id:transfer_total
  Every transfer falls under one of three cases. Covered, and the receiver has room: it must
  succeed and move exactly the amount (the progress scenario). The sender is short, or the
  receiver has no room: it is rejected and neither balance moves.
  Reading   for a transfer: every sender, every receiver, every amount (a u64: 0 to 2^64 - 1); every such call,
            accepted or rejected [default D2]; then the call gives an answer [default D1]; the sum of the balances
            of every wallet named (the sender, the receiver) after the call equals the sum of the balances of every
            wallet named (the sender, the receiver) before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  7 of 7 pass on the compiled Rust; 7 of 7 pass on the Lean model
  Generated the rule statement at 216 generated inputs on the compiled Rust: the same result as on the Lean model at
            432 of 432 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   7 of 7 pass on the compiled Rust; 7 of 7 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 4
                     scenarios beneath it, 4 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input (no size bound: the rule speaks of no collection)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.wallet.transfer_total.holds, Rule.wallet.transfer_total.from_scenarios: the rule
                     statement for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

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
    meaning      27 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.transfer: domain, unsigned, never_changes: frame, unsigned, aggregate: modifier, unsigned,
                 all_of: modifier, unsigned, w.balance: domain, unsigned, calls.every: coverage, unsigned, g.subject:
                 grammar, unsigned, g.rule_vp: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned,
                 D2: default, unsigned, D3: default, unsigned, D4: default, unsigned, given: modifier, unsigned, is:
                 modifier, unsigned, amount_value: modifier, unsigned, not_more_than: modifier, unsigned, sum_within:
                 modifier, unsigned, w.maximum: domain, unsigned, always: frame, unsigned, decreases_by: frame,
                 unsigned, increases_by: frame, unsigned, w.succeeds: domain, unsigned, D8: default, unsigned,
                 more_than: modifier, unsigned, w.rejected_with: domain, unsigned, sum_exceeds: modifier, unsigned)
                 4 of 4 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 12 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 3 scenario theorems
                 for all inputs, 1 for literal values only; axioms: propext, Classical.choice, Quot.sound (the
                 standard three only)   [kernel-checked]
                 (Rule.wallet.transfer_total.holds, Rule.wallet.transfer_total.from_scenarios,
                 Spec.wallet.transfer_conserves, Spec.wallet.transfer_short, Spec.wallet.transfer_no_room,
                 Spec.wallet.transfer_short_example)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 7 example rows (7 give the same result on the compiled Rust and on the model) and
                 on 216 generated inputs of the rule statement (432 of 432 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every sender, every receiver, every amount (a u64: 0 to 2^64 - 1)
            covers      every such call, accepted or rejected [default D2]
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
            tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             432 of 432 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 1 of 1 literal examples proved for their own values
            PROVED-FOR-ALL  A covered transfer moves the money and conserves the total   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-INSTANCE Transferring more than you have is rejected and changes nothing   [an instance: literal values]
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
  Given Alice's balance is <a>
  And Bob's balance is <b>
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
            <amount> (a u64: 0 to 2^64 - 1); for every value of a (a u64: 0 to 2^64 - 1), b (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A covered transfer moves the money and conserves the total
  kernel-checked   theorem Spec.wallet.transfer_conserves.reading_holds : Spec.wallet.transfer_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_conserves.reading_iff : Spec.wallet.transfer_conserves.reading ↔ Spec.wallet.transfer_conserves.stmt  (NEW ↔ OLD: the reading compiled from 21 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_conserves.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_conserves : Spec.wallet.transfer_conserves.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/wallet/transfer_conserves.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 8 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-room, W-transfer, T-ok, T-dec, T-inc, T-total
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1839 of 1839 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 21 Clausebook pieces signed off by anyone - UNREVIEWED: w.transfer, given, is, w.balance, amount_value, not_more_than, sum_within, w.maximum, always, decreases_by, increases_by, never_changes, w.succeeds, aggregate, all_of, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 7776 generated inputs (91 in scope): the definition of each frame and its executable reading agree on 364 of 364 evaluations
  tested           the reading on the COMPILED RUST at the same 7776 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 38880 of 38880 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, is, w.balance, amount_value, not_more_than, sum_within, w.maximum, always, decreases_by, increases_by, never_changes, w.succeeds, aggregate, all_of, calls.every, D1, D2, D3, D4, D8`:

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
  Given Alice's balance is <a>
  And Bob's balance is <b>
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
            <amount> (a u64: 0 to 2^64 - 1); for every value of a (a u64: 0 to 2^64 - 1), b (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Transferring more than the sender has is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short.reading_holds : Spec.wallet.transfer_short.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_short.reading_iff : Spec.wallet.transfer_short.reading ↔ Spec.wallet.transfer_short.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_short.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_short : Spec.wallet.transfer_short.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: w.transfer, given, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 7776 generated inputs (90 in scope): the definition of each frame and its executable reading agree on 270 of 270 evaluations
  tested           the reading on the COMPILED RUST at the same 7776 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 31104 of 31104 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8`:

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
  Given Alice's balance is <a>
  And Bob's balance is <b>
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
            <amount> (a u64: 0 to 2^64 - 1); for every value of a (a u64: 0 to 2^64 - 1), b (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A transfer the receiver has no room for is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_no_room.reading_holds : Spec.wallet.transfer_no_room.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_no_room.reading_iff : Spec.wallet.transfer_no_room.reading ↔ Spec.wallet.transfer_no_room.stmt  (NEW ↔ OLD: the reading compiled from 17 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_no_room.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_no_room : Spec.wallet.transfer_no_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_no_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_no_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, G-noroom, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 150 of 150 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 17 Clausebook pieces signed off by anyone - UNREVIEWED: w.transfer, given, is, w.balance, amount_value, not_more_than, sum_exceeds, w.maximum, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 7776 generated inputs (35 in scope): the definition of each frame and its executable reading agree on 105 of 105 evaluations
  tested           the reading on the COMPILED RUST at the same 7776 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 31104 of 31104 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, is, w.balance, amount_value, not_more_than, sum_exceeds, w.maximum, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8`:

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
  Given Alice's balance is 10
  And Bob's balance is 7
  When Alice transfers 11 to Bob
  Then the operation is rejected with insufficient funds
  And Alice's balance is unchanged
  And Bob's balance is unchanged
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  a transfer of 11 from Alice to Bob: every sender (Alice), every receiver (Bob), with the one amount 11 (a
            plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  Transferring more than you have is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.transfer_short_example.reading_holds : Spec.wallet.transfer_short_example.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.transfer_short_example.reading_iff : Spec.wallet.transfer_short_example.reading ↔ Spec.wallet.transfer_short_example.stmt  (NEW ↔ OLD: the reading compiled from 14 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_short_example.reading_sat)
  kernel-checked   theorem Spec.wallet.transfer_short_example : Spec.wallet.transfer_short_example.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/transfer_short_example.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.transfer_short_example.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model wallet.transfer, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.transfer: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: G-balance, W-transfer, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 78 of 78 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 14 Clausebook pieces signed off by anyone - UNREVIEWED: w.transfer, given, is, w.balance, amount_value, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 169 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 3 of 3 evaluations
  tested           the reading on the COMPILED RUST at the same 169 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 676 of 676 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, is, w.balance, amount_value, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8`:

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
  Reading   for clause 1: a withdrawal: every wallet, every amount (a u64: 0 to 2^64 - 1); every such call, accepted
            or rejected [default D2]; then the call gives an answer [default D1; also asked for by 'always
            answers']; clause 2: a withdrawal: every wallet, every amount (a u64: 0 to 2^64 - 1); ONLY accepted
            calls [asked for]; then the balance of the wallet after the call, plus the amount, equals the balance of
            the wallet before it, exactly; ONLY rejected calls [asked for]; then the balance of the wallet after the
            call equals the balance of the wallet before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Generated the rule statement at 36 generated inputs on the compiled Rust: the same result as on the Lean model at
            216 of 216 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   5 of 5 pass on the compiled Rust; 5 of 5 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input (no size bound: the rule speaks of no collection)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.wallet.withdrawal.holds, Rule.wallet.withdrawal.from_scenarios: the rule statement
                     for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "Withdrawing more than the balance is rejected and changes nothing" would also hold of: reject-all,
              identity; ruled out here by "A covered withdrawal succeeds and takes exactly the amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      28 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.withdraw: domain, unsigned, always_answers: frame, unsigned, successful: modifier, unsigned,
                 decreases_by: frame, unsigned, w.balance: domain, unsigned, amount_value: modifier, unsigned,
                 rejected: modifier, unsigned, never_changes: frame, unsigned, calls.every: coverage, unsigned,
                 calls.accepted: coverage, unsigned, calls.rejected: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.clauses: grammar, unsigned,
                 g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4:
                 default, unsigned, given: modifier, unsigned, is: modifier, unsigned, not_more_than: modifier,
                 unsigned, always: frame, unsigned, w.succeeds: domain, unsigned, D8: default, unsigned, more_than:
                 modifier, unsigned, w.rejected_with: domain, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 2 scenario theorems
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.wallet.withdrawal.holds, Rule.wallet.withdrawal.from_scenarios, Spec.wallet.withdraw_covered,
                 Spec.wallet.withdraw_too_much)
    translation  Lean model wallet.Wallet.withdraw generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 5 example rows (5 give the same result on the compiled Rust and on the model) and
                 on 36 generated inputs of the rule statement (216 of 216 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  clause 1: a withdrawal: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1; also asked for by 'always answers']
                        clause 2: a withdrawal: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      ONLY accepted calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call, plus the amount, equals the balance of the wallet before
                        it, exactly
            accepted    an acceptance is the answer Ok; an Err answer is a rejection
                        clause 3: a withdrawal: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      ONLY rejected calls [asked for]
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
            tested           the reading on the COMPILED RUST at the same 36 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             216 of 216 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 20 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 20 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing   [a part: the rule statement is proved from it]
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
  Given Alice's balance is <a>
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
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A covered withdrawal succeeds and takes exactly the amount
  kernel-checked   theorem Spec.wallet.withdraw_covered.reading_holds : Spec.wallet.withdraw_covered.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.withdraw_covered.reading_iff : Spec.wallet.withdraw_covered.reading ↔ Spec.wallet.withdraw_covered.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.withdraw_covered.reading_sat)
  kernel-checked   theorem Spec.wallet.withdraw_covered : Spec.wallet.withdraw_covered.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_covered.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_covered.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-withdraw, T-ok, T-dec
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 291 of 291 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: w.withdraw, given, is, w.balance, amount_value, not_more_than, always, decreases_by, w.succeeds, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 216 generated inputs (21 in scope): the definition of each frame and its executable reading agree on 42 of 42 evaluations
  tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 648 of 648 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, is, w.balance, amount_value, not_more_than, always, decreases_by, w.succeeds, calls.every, D1, D2, D3, D4, D8`:

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
  Given Alice's balance is <a>
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
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Withdrawing more than the balance is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.withdraw_too_much.reading_holds : Spec.wallet.withdraw_too_much.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.withdraw_too_much.reading_iff : Spec.wallet.withdraw_too_much.reading ↔ Spec.wallet.withdraw_too_much.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.withdraw_too_much.reading_sat)
  kernel-checked   theorem Spec.wallet.withdraw_too_much : Spec.wallet.withdraw_too_much.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/withdraw_too_much.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.withdraw_too_much.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.withdraw: Aeneas.Std.instHSubUScalarResult
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, W-withdraw, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: w.withdraw, given, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 216 generated inputs (15 in scope): the definition of each frame and its executable reading agree on 30 of 30 evaluations
  tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 648 of 648 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, is, w.balance, amount_value, more_than, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8`:

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
  Reading   for clause 1: a deposit: every wallet, every amount (a u64: 0 to 2^64 - 1); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1; also asked for by 'always answers'];
            clause 2: a deposit: every wallet, every amount (a u64: 0 to 2^64 - 1); ONLY accepted calls [asked for];
            then the balance of the wallet after the call equals the balance of the wallet before it plus the
            amount, exactly; ONLY rejected calls [asked for]; then the balance of the wallet after the call equals
            the balance of the wallet before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Generated the rule statement at 36 generated inputs on the compiled Rust: the same result as on the Lean model at
            216 of 216 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   5 of 5 pass on the compiled Rust; 5 of 5 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input (no size bound: the rule speaks of no collection)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.wallet.deposit.holds, Rule.wallet.deposit.from_scenarios: the rule statement for
                     all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "A deposit that would overflow is rejected and changes nothing" would also hold of: reject-all,
              identity; ruled out here by "A deposit with room succeeds and adds exactly the amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      29 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.deposit: domain, unsigned, always_answers: frame, unsigned, successful: modifier, unsigned,
                 increases_by: frame, unsigned, w.balance: domain, unsigned, amount_value: modifier, unsigned,
                 rejected: modifier, unsigned, never_changes: frame, unsigned, calls.every: coverage, unsigned,
                 calls.accepted: coverage, unsigned, calls.rejected: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.clauses: grammar, unsigned,
                 g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4:
                 default, unsigned, given: modifier, unsigned, is: modifier, unsigned, sum_within: modifier,
                 unsigned, w.maximum: domain, unsigned, always: frame, unsigned, w.succeeds: domain, unsigned, D8:
                 default, unsigned, sum_exceeds: modifier, unsigned, w.rejected_with: domain, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 2 scenario theorems
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.wallet.deposit.holds, Rule.wallet.deposit.from_scenarios, Spec.wallet.deposit_with_room,
                 Spec.wallet.deposit_overflow)
    translation  Lean model wallet.Wallet.deposit generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 5 example rows (5 give the same result on the compiled Rust and on the model) and
                 on 36 generated inputs of the rule statement (216 of 216 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  clause 1: a deposit: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1; also asked for by 'always answers']
                        clause 2: a deposit: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      ONLY accepted calls [asked for]
            assuming    nothing: every state and every input
            then        the balance of the wallet after the call equals the balance of the wallet before it plus the
                        amount, exactly
            accepted    an acceptance is the answer Ok; an Err answer is a rejection
                        clause 3: a deposit: every wallet, every amount (a u64: 0 to 2^64 - 1)
            covers      ONLY rejected calls [asked for]
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
            tested           the reading on the COMPILED RUST at the same 36 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             216 of 216 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 20 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 20 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing   [a part: the rule statement is proved from it]
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
  Given Alice's balance is <a>
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
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A deposit with room succeeds and adds exactly the amount
  kernel-checked   theorem Spec.wallet.deposit_with_room.reading_holds : Spec.wallet.deposit_with_room.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.deposit_with_room.reading_iff : Spec.wallet.deposit_with_room.reading ↔ Spec.wallet.deposit_with_room.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.deposit_with_room.reading_sat)
  kernel-checked   theorem Spec.wallet.deposit_with_room : Spec.wallet.deposit_with_room.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_with_room.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_with_room.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-inc
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 291 of 291 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: w.deposit, given, is, w.balance, amount_value, sum_within, w.maximum, always, increases_by, w.succeeds, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 216 generated inputs (21 in scope): the definition of each frame and its executable reading agree on 42 of 42 evaluations
  tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 648 of 648 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, given, is, w.balance, amount_value, sum_within, w.maximum, always, increases_by, w.succeeds, calls.every, D1, D2, D3, D4, D8`:

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
  Given Alice's balance is <a>
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
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A deposit that would overflow is rejected and changes nothing
  kernel-checked   theorem Spec.wallet.deposit_overflow.reading_holds : Spec.wallet.deposit_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.wallet.deposit_overflow.reading_iff : Spec.wallet.deposit_overflow.reading ↔ Spec.wallet.deposit_overflow.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.deposit_overflow.reading_sat)
  kernel-checked   theorem Spec.wallet.deposit_overflow : Spec.wallet.deposit_overflow.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/wallet/deposit_overflow.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.wallet.deposit_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-noroom, W-deposit, T-err, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 114 of 114 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: w.deposit, given, is, w.balance, amount_value, sum_exceeds, w.maximum, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 216 generated inputs (15 in scope): the definition of each frame and its executable reading agree on 30 of 30 evaluations
  tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 648 of 648 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, given, is, w.balance, amount_value, sum_exceeds, w.maximum, always, never_changes, w.rejected_with, calls.every, D1, D2, D3, D4, D8`:

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
  Reading   for a transfer: every sender, every receiver, every amount (a u64: 0 to 2^64 - 1); every such call,
            accepted or rejected [default D2]; assuming the amount is at most the balance of the sender; then the
            call gives an answer [default D1]; the answer is an acceptance (see `accepted`)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 216 generated inputs on the compiled Rust: the same result as on the Lean model at
            432 of 432 evaluations; it is FALSE at {"the_sender": "1", "the_receiver": "18446744073709551615",
            "the_amount": "1"}, on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  FALSE at an input found at generated input 3 and shrunk: {"the_amount": "1", "the_receiver":
                     "18446744073709551615", "the_sender": "2"} (seed 20261111); of the 1 scenario beneath it, 0 not
                     falsified, 1 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with no size bound (the rule's assertion; input {"the_amount": "1", "the_receiver":
                     "18446744073709551615", "the_sender": "1"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.wallet.transfer_affordable.refuted (the negation of the rule
                     statement) at {"the_sender": "1", "the_receiver": "18446744073709551615", "the_amount": "1"};
                     axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_amount": "1", "the_receiver": "18446744073709551615", "the_sender": "2"}   source:
                     generated property test (case 3 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it
                     fails; on the Lean model the reading fails
    found false at   {"the_amount": "1", "the_receiver": "18446744073709551615", "the_sender": "1"}   source:
                     generated bounded check (Kani at no size bound; replayed on the compiled Rust through the
                     generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the
                     reading fails
    found false at   [A transfer the sender can afford always succeeds] {"a": "18446744073709551615", "alice_state":
                     "18446744073709551615", "amount": "18446744073709551615", "b": "4", "bob_state": "4"}   source:
                     generated property test (case 11 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it
                     fails; on the Lean model the reading fails
    found false at   [A transfer the sender can afford always succeeds] {"a": "13835058055282163711", "alice_state":
                     "13835058055282163711", "amount": "4611686018427387903", "b": "18446744073709551615",
                     "bob_state": "18446744073709551615"}   source: generated bounded check (Kani at no size bound;
                     replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the compiled
                     Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      23 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.transfer: domain, unsigned, given: modifier, unsigned, always: frame, unsigned, not_more_than:
                 modifier, unsigned, amount_value: modifier, unsigned, w.balance: domain, unsigned, accepted:
                 modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp:
                 grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2:
                 default, unsigned, D4: default, unsigned, D8: default, unsigned, is: modifier, unsigned,
                 decreases_by: frame, unsigned, never_changes: frame, unsigned, w.succeeds: domain, unsigned,
                 aggregate: modifier, unsigned, all_of: modifier, unsigned, D3: default, unsigned)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input, 1 refutation (the
                 scenario is false); axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.wallet.transfer_affordable.refuted, Spec.wallet.transfer_always_succeeds.refuted)
    translation  Lean model wallet.transfer generated from wallet/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 216 generated inputs of the rule statement (432 of 432 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every sender, every receiver, every amount (a u64: 0 to 2^64 - 1)
            covers      every such call, accepted or rejected [default D2]
            assuming    the amount is at most the balance of the sender
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`)
            accepted    an acceptance is the answer Ok; an Err answer is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.wallet.transfer_affordable.refuted : ¬
                             Rule.wallet.transfer_affordable.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   sender = 1, receiver = 18446744073709551615, amount = 1
                             at this input the rule does not hold: NOT "the answer is an acceptance (see `accepted`)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 216 generated inputs (126 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 126 of 126 evaluations
            tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             432 of 432 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 16 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A transfer the sender can afford always succeeds   (expected REFUTED)   [beneath the rule; not used to prove it]
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
  Given Alice's balance is <a>
  And Bob's balance is <b>
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
            <amount> (a u64: 0 to 2^64 - 1); for every value of a (a u64: 0 to 2^64 - 1), b (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
REFUTED  A transfer the sender can afford always succeeds
  kernel-checked   theorem Spec.wallet.transfer_always_succeeds.reading_iff : Spec.wallet.transfer_always_succeeds.reading ↔ Spec.wallet.transfer_always_succeeds.stmt  (NEW ↔ OLD: the reading compiled from 18 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.wallet.transfer_always_succeeds.reading_sat)
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
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-covers, W-transfer, T-ok, T-dec, T-total
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1587 of 1587 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 216 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone - UNREVIEWED: w.transfer, given, is, w.balance, amount_value, not_more_than, always, decreases_by, never_changes, w.succeeds, aggregate, all_of, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 7776 generated inputs (126 in scope): the definition of each frame and its executable reading agree on 378 of 378 evaluations; the reading is false at one of them
  tested           the reading on the COMPILED RUST at the same 7776 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 31104 of 31104 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.transfer, given, is, w.balance, amount_value, not_more_than, always, decreases_by, never_changes, w.succeeds, aggregate, all_of, calls.every, D1, D2, D3, D4, D8`:

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
  Verdict   no statement: the rule line is not a composition of Clausebook pieces
  Examples  none could be evaluated

  Evidence  for the scenarios, weakest first; each rung with what it rests on
    1 example rows   none
                     rests on: nothing
    2 property test  none: no reading was compiled for this rule, so no test was generated
                     rests on: nothing
    3 bounded check  none: no reading was compiled for this rule
                     rests on: nothing
    4 proof          none: nothing about this rule is kernel-checked
                     rests on: nothing
    STRONGEST HELD   none

  Suite     not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios
              of this group are NEW sentences that have none

  Rests on
    meaning      no Clausebook piece is used (no reading was compiled)
    proof        no kernel-checked theorem for: deposit_earns_interest
    translation  no model function is involved (no statement was generated)
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
            features/wallet.feature:156: no composition of Clausebook pieces reads "a deposit earns interest" as a rule
                             clause (<a / an> [successful | rejected | internal] <operation> [followed by <operation>]
                             [for which <condition>] <what it does>, or: for <such an operation>, <what a Then would
                             say>)
              operations of the Clausebook: batch, batch applied as a whole, computation of the total, fund transfer,
                             lookup, transfer
            the rule line is not a composition of Clausebook pieces, so no statement was generated for it
  Scenarios NO SCENARIO PROVED: 0 of 1 literal examples proved for their own values
            UNBOUND         A deposit earns interest   (expected UNBOUND)
```

#### UNBOUND: A deposit earns interest

`features/wallet.feature:161`  id `Spec.wallet.deposit_earns_interest`  tags `@expect-unbound @id:deposit_earns_interest`

```gherkin
Scenario: A deposit earns interest
  Given Alice's balance is 100
  When Alice deposits 5
  Then Alice earns interest on her balance
```

```text
UNBOUND  A deposit earns interest
  Clausebook       UNBOUND: features/wallet.feature:164: no composition of Clausebook pieces reads "Alice earns interest on her balance" as a claim
                   nearest forms of the Clausebook for a claim:
                     - {m:measure<transfer>} is now {t:term<transfer>}
                     - {a:ameasure<transfer>} is {t:term<transfer>}
                     - {m:measure<optnum>} is unchanged
                   a new sentence needs no new entry if it can be said with existing forms; otherwise add a piece (or an idiom) to the project's local book (clausebook/local/)
  features/wallet.feature:164: no glossary `then` phrase matches: "Alice earns interest on her balance"
    nearest glossary phrases:
      - the result is the balance of account {index:i} of ledger {ledger:l}
      - the operation succeeds
      - the result is {amount:s}
    paste-ready glossary stub (then define the Lean definition in the Vocab file of that crate):
      - id: T-TODO
        kind: then
        phrase: "Alice earns interest on her balance"
        lean: Vocab.TODO
        args: []
  no Lean statement was generated, so nothing was proved or refuted
  tested           cucumber-rs on compiled Rust: skipped (the undefined step and everything after it are skipped)
```

### Rule: A batch never changes the total of all balances of the ledger

```text
Rule: A batch never changes the total of all balances of the ledger   [features/ledger.feature:13]   tags @id:batch_total
  The first scenario is the safety half: it holds whatever the ledger and whatever the batch,
  and it would also hold of a batch function that does nothing. The second is the progress
  half: the batch goes on for as long as it can.
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the sum of the balances of every
            account of the ledger after the call equals the sum of the balances of every account of the ledger
            before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  12 of 12 pass on the compiled Rust; 12 of 12 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   12 of 12 pass on the compiled Rust; 12 of 12 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 3
                     scenarios beneath it, 3 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; NO ANSWER in 30 s with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.batch_total.holds, Rule.ledger.batch_total.from_scenarios: the rule
                     statement for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, identity, constant; still allows: no-op: reports every transfer of the batch as
              applied and leaves the state as it was [no scenario counted is false of it on the search grid]
            taken alone, this group would also hold of: no-op (1 variant); the whole suite for
              `ledger.Ledger.apply_batch` rules it out through Rule "For a batch, the number of transfers applied is at
              most the length of the batch, and for a batch for which the first transfer of the batch is not valid on
              the ledger, the number of transfers applied is zero and the ledger is unchanged"
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
    meaning      30 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, never_changes: frame, unsigned, aggregate: modifier, unsigned,
                 l.balances_of: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D3: default, unsigned, D4: default, unsigned, given: modifier,
                 unsigned, i.holds: idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned,
                 balances_value: modifier, unsigned, D8: default, unsigned, every_of: frame, unsigned, l.stopped_at:
                 domain, unsigned, not: modifier, unsigned, l.valid: domain, unsigned, D5: default, unsigned, D7:
                 default, unsigned, D9: default, unsigned, and_then: modifier, unsigned, result_at_most: frame,
                 unsigned, l.applied: domain, unsigned, l.length: domain, unsigned)
                 3 of 3 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 5 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 3 scenario theorems
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.batch_total.holds, Rule.ledger.batch_total.from_scenarios, Spec.ledger.batch_conserves,
                 Spec.ledger.batch_stops_at_invalid, Spec.ledger.two_batches_conserve)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 12 example rows (12 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (594 of 594 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
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
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Two batches applied one after the other conserve the total   [beneath the rule; not used to prove it]
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
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Applying any batch of transfers conserves the total of all balances
  kernel-checked   theorem Spec.ledger.batch_conserves.reading_holds : Spec.ledger.batch_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_conserves.reading_iff : Spec.ledger.batch_conserves.reading ↔ Spec.ledger.batch_conserves.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_conserves.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_conserves : Spec.ledger.batch_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           6 of 6 rows pass on compiled Rust (cucumber-rs); 6 of 6 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8`:

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
  Then every transfer at which <batch> stopped is not valid on ledger Main afterwards

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
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
            D9 negation binds to the one condition it is written on: 'every X is not P' means that no X is P, never 'not
            every X is P'
```

```text
PROVED-FOR-ALL  A batch stops only at a transfer that cannot be carried out
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid.reading_holds : Spec.ledger.batch_stops_at_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid.reading_iff : Spec.ledger.batch_stops_at_invalid.reading ↔ Spec.ledger.batch_stops_at_invalid.stmt  (NEW ↔ OLD: the reading compiled from 18 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_stops_at_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_stops_at_invalid : Spec.ledger.batch_stops_at_invalid.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_stops_at_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_stops_at_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-stops-at-invalid
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1606 of 1606 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
  NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, every_of, l.stopped_at, not, l.valid, calls.every, D1, D2, D4, D5, D7, D8, D9
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, every_of, l.stopped_at, not, l.valid, calls.every, D1, D2, D4, D5, D7, D8, D9`:

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
            ledger Main, transfer by transfer: every ledger Main, and every batch <first> (a list of transfers, in
            order) and every batch <second> (a list of transfers, in order); for every value of balances (a list of u64
            balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Two batches applied one after the other conserve the total
  kernel-checked   theorem Spec.ledger.two_batches_conserve.reading_holds : Spec.ledger.two_batches_conserve.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.two_batches_conserve.reading_iff : Spec.ledger.two_batches_conserve.reading ↔ Spec.ledger.two_batches_conserve.stmt  (NEW ↔ OLD: the reading compiled from 19 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.two_batches_conserve.reading_sat)
  kernel-checked   theorem Spec.ledger.two_batches_conserve : Spec.ledger.two_batches_conserve.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/two_batches_conserve.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.two_batches_conserve.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.apply_batch, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 377 of 377 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 19 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, and_then, given, i.holds, is, l.ledger, balances_value, never_changes, result_at_most, aggregate, l.balances_of, l.applied, l.length, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 88209 generated inputs (8019 in scope): the definition of each frame and its executable reading agree on 16038 of 16038 evaluations
  tested           the reading on the COMPILED RUST at the same 88209 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 264627 of 264627 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, and_then, given, i.holds, is, l.ledger, balances_value, never_changes, result_at_most, aggregate, l.balances_of, l.applied, l.length, calls.every, D1, D2, D3, D4, D8`:

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

### Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, the number of transfers applied is zero and the ledger is unchanged

```text
Rule: For a batch, the number of transfers applied is at most the length of the batch, and for a batch for which the first transfer of the batch is not valid on the ledger, the number of transfers applied is zero and the ledger is unchanged   [features/ledger.feature:66]   tags @id:batch_count
  Reading   for clause 1: a batch: every ledger, every batch (a list of transfers, in order); every such call,
            accepted or rejected [default D2]; then the call gives an answer [default D1]; the number of transfers
            the call reports as applied is at most the number of transfers in the batch; clause 2: a batch: every
            ledger, every batch (a list of transfers, in order); every such call, accepted or rejected [default D2];
            assuming there is a first transfer of the batch, and it can NOT be carried out exactly on the ledger (an
            account does not exist, or both are the same, or the sender does not cover the amount, or the receiver's
            balance would pass 2^64 - 1); then the call gives an answer [default D1]; the number of transfers the
            call reports as applied is 0; the balances of the ledger, account by account after the call equals the
            balances of the ledger, account by account before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            1485 of 1485 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   8 of 8 pass on the compiled Rust; 8 of 8 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 4
                     scenarios beneath it, 4 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.batch_count.holds, Rule.ledger.batch_count.from_scenarios: the rule
                     statement for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: no-op, constant; still allows: reject-all: always answers `0` and leaves the state as it
              was [proved to satisfy every scenario counted]; identity: answers as the code does, but never changes the
              state [no scenario counted is false of it on the search grid]
            taken alone, this group would also hold of: reject-all, identity (2 variants); the whole suite for
              `ledger.Ledger.apply_batch` rules them out through Rule "A batch never changes the total of all balances
              of the ledger"
            alone, "The number of transfers applied is at most the length of the batch" would also hold of: no-op,
              constant; ruled out here by "A batch whose first transfer is invalid changes nothing"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      33 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, result_at_most: frame, unsigned, l.applied: domain, unsigned,
                 l.length: domain, unsigned, given: modifier, unsigned, result_is: frame, unsigned, never_changes:
                 frame, unsigned, the_first: modifier, unsigned, l.transfers: domain, unsigned, not: modifier,
                 unsigned, l.valid: domain, unsigned, zero: modifier, unsigned, l.ledger: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_for: grammar, unsigned,
                 g.role: grammar, unsigned, g.claims: grammar, unsigned, g.clauses: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4: default,
                 unsigned, D5: default, unsigned, D8: default, unsigned, i.holds: idiom, unsigned, is: modifier,
                 unsigned, balances_value: modifier, unsigned, D6: default, unsigned, becomes: frame, unsigned,
                 i.exactly_applied: idiom, unsigned, index_count: modifier, unsigned)
                 4 of 4 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 2 scenario theorems
                 for all inputs, 2 for literal values only; axioms: propext, Classical.choice, Quot.sound (the
                 standard three only)   [kernel-checked]
                 (Rule.ledger.batch_count.holds, Rule.ledger.batch_count.from_scenarios,
                 Spec.ledger.batch_first_invalid, Spec.ledger.batch_count_bounded, Spec.ledger.batch_example_all,
                 Spec.ledger.batch_example_stop)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows (8 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (1485 of 1485 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  clause 1: a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is at most the number of transfers in the
                        batch
                        clause 2: a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
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
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
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
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             1485 of 1485 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 26 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 26 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs; 2 of 2 literal examples proved for their own values
            PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch   [a part: the rule statement is proved from it]
            PROVED-INSTANCE A batch of two valid transfers is applied in full   [an instance: literal values]
            PROVED-INSTANCE A batch stops at its first invalid transfer and keeps what it has applied   [an instance: literal values]
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
  Then the number of transfers applied is zero
  And ledger Main is unchanged

  Examples:
    | balances      | batch                  |
    | [5, 5]        | [0->1:6, 1->0:1]       |
    | [5, 5]        | [0->0:1]               |
    | [5, 5]        | [0->2:1, 0->1:1]       |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A batch whose first transfer is invalid changes nothing
  kernel-checked   theorem Spec.ledger.batch_first_invalid.reading_holds : Spec.ledger.batch_first_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_first_invalid.reading_iff : Spec.ledger.batch_first_invalid.reading ↔ Spec.ledger.batch_first_invalid.stmt  (NEW ↔ OLD: the reading compiled from 22 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_first_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_first_invalid : Spec.ledger.batch_first_invalid.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/batch_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 544 of 544 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 22 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, result_is, never_changes, l.applied, zero, calls.every, D1, D2, D3, D4, D5, D6, D8
  tested           the reading on 3267 generated inputs (188 in scope): the definition of each frame and its executable reading agree on 376 of 376 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 9801 of 9801 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, result_is, never_changes, l.applied, zero, calls.every, D1, D2, D3, D4, D5, D6, D8`:

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
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the number of transfers the call reports as applied is at most the number of transfers in the batch <batch>
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  The number of transfers applied is at most the length of the batch
  kernel-checked   theorem Spec.ledger.batch_count_bounded.reading_holds : Spec.ledger.batch_count_bounded.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_count_bounded.reading_iff : Spec.ledger.batch_count_bounded.reading ↔ Spec.ledger.batch_count_bounded.stmt  (NEW ↔ OLD: the reading compiled from 14 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_count_bounded.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_count_bounded : Spec.ledger.batch_count_bounded.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/batch_count_bounded.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_count_bounded.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 256 of 256 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 14 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_at_most, l.applied, l.length, calls.every, D1, D2, D4, D8
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_at_most, l.applied, l.length, calls.every, D1, D2, D4, D8`:

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
  And ledger Main is now [70, 0, 50]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50] to ledger Main, transfer by transfer: every ledger Main, with the one
            batch [0->1:30, 1->2:50] (a plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  A batch of two valid transfers is applied in full
  kernel-checked   theorem Spec.ledger.batch_example_all.reading_holds : Spec.ledger.batch_example_all.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_example_all.reading_iff : Spec.ledger.batch_example_all.reading ↔ Spec.ledger.batch_example_all.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_example_all.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_example_all : Spec.ledger.batch_example_all.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_all.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_all.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, calls.every, D1, D2, D4, D8
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
  tested           the reading on the COMPILED RUST at the same 13 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 39 of 39 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, calls.every, D1, D2, D4, D8`:

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
  And ledger Main is now [70, 50, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 2->1:5, 0->1:1] to ledger Main, transfer by transfer: every ledger Main, with
            the one batch [0->1:30, 2->1:5, 0->1:1] (a plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  A batch stops at its first invalid transfer and keeps what it has applied
  kernel-checked   theorem Spec.ledger.batch_example_stop.reading_holds : Spec.ledger.batch_example_stop.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_example_stop.reading_iff : Spec.ledger.batch_example_stop.reading ↔ Spec.ledger.batch_example_stop.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_example_stop.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_example_stop : Spec.ledger.batch_example_stop.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_example_stop.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_example_stop.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, calls.every, D1, D2, D4, D8
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
  tested           the reading on the COMPILED RUST at the same 13 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 39 of 39 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, result_is, becomes, i.exactly_applied, l.applied, index_count, calls.every, D1, D2, D4, D8`:

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

### Rule: For a batch for which every transfer of the batch is valid on the ledger, the number of transfers applied is the length of the batch

```text
Rule: For a batch for which every transfer of the batch is valid on the ledger, the number of transfers applied is the length of the batch   [features/ledger.feature:111]   tags @expect-refuted @id:batch_all_valid
  Deliberately false, and tagged on the rule: the tag applies to every scenario beneath it.
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; assuming every transfer of the batch can be carried out exactly on the ledger
            (both accounts exist and differ, the sender covers the amount, the receiver's balance stays within 2^64
            - 1); then the call gives an answer [default D1]; the number of transfers the call reports as applied is
            the number of transfers in the batch
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_batch": "[0->1:1, 0->1:1]"}, on the
            compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  FALSE at an input found at generated input 2085 and shrunk: {"the_batch":
                     "[0->1:14779828575414881320, 0->5:1]", "the_ledger": "[14779828575414881320, 0,
                     3666915498294670295, 0, 0, 0]"} (seed 20261111); of the 1 scenario beneath it, 0 not falsified,
                     1 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 2 transfers (the rule's assertion; input {"the_batch":
                     "[0->1:9223372036854775809, 0->1:7242086547668779013]", "the_ledger": "[11925865344506247229,
                     1049636799838765050]"}; on the compiled Rust it fails); holds for every input with up to 2
                     accounts and up to 1 transfer; with up to 4 accounts and up to 1 transfer
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger.batch_all_valid.refuted (the negation of the rule
                     statement) at {"the_ledger": "[1, 0]", "the_batch": "[0->1:1, 0->1:1]"}; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[0->1:14779828575414881320, 0->5:1]", "the_ledger": "[14779828575414881320, 0,
                     3666915498294670295, 0, 0, 0]"}   source: generated property test (case 2085 of the run,
                     shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_batch": "[0->1:9223372036854775809, 0->1:7242086547668779013]", "the_ledger":
                     "[11925865344506247229, 1049636799838765050]"}   source: generated bounded check (Kani at up to
                     2 accounts and up to 2 transfers; replayed on the compiled Rust through the generated
                     predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   [A batch of transfers that are each valid on the starting ledger is applied in full]
                     {"balances": "[0, 2, 0, 0, 0, 0]", "batch": "[1->2:1, 1->2:2]", "main_state": "[0, 2, 0, 0, 0,
                     0]"}   source: generated property test (case 1841 of the run, shrunk). COUNTEREXAMPLE: on the
                     compiled Rust it fails; on the Lean model the reading fails
    found false at   [A batch of transfers that are each valid on the starting ledger is applied in full]
                     {"balances": "[2305843009213693954, 16140901064495857660]", "batch": "[1->0:9223372036854775807,
                     1->0:6917529027641081854]", "main_state": "[2305843009213693954, 16140901064495857660]"}
                     source: generated bounded check (Kani at up to 2 accounts and up to 2 transfers; replayed on the
                     compiled Rust through the generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails;
                     on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      22 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, given: modifier, unsigned, result_is: frame, unsigned, every:
                 modifier, unsigned, l.transfers: domain, unsigned, l.valid: domain, unsigned, l.applied: domain,
                 unsigned, l.length: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned, D8: default,
                 unsigned, i.holds: idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned,
                 balances_value: modifier, unsigned)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 4 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input, 1 refutation (the
                 scenario is false); axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.batch_all_valid.refuted, Spec.ledger.batch_all_valid_all_applied.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (594 of 594 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
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
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger.batch_all_valid.refuted : ¬ Rule.ledger.batch_all_valid.reading; axioms
                             propext, Classical.choice, Quot.sound
            counterexample   ledger = [1, 0], batch = [0->1:1, 0->1:1]
                             at this input the rule does not hold: NOT "the number of transfers the call reports as
                             applied is the number of transfers in the batch"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (63 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 63 of 63 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 18 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         A batch of transfers that are each valid on the starting ledger is applied in full   (expected REFUTED)   [beneath the rule; not used to prove it]
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
  Then the number of transfers applied is the length of <batch>

  Examples:
    | balances      | batch                  |
    | [100, 20, 0]  | [0->1:30, 1->2:20]     |
    | [5, 5]        | [0->1:5]               |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
REFUTED  A batch of transfers that are each valid on the starting ledger is applied in full
  kernel-checked   theorem Spec.ledger.batch_all_valid_all_applied.reading_iff : Spec.ledger.batch_all_valid_all_applied.reading ↔ Spec.ledger.batch_all_valid_all_applied.stmt  (NEW ↔ OLD: the reading compiled from 18 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_all_valid_all_applied.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_all_valid_all_applied.refuted : ¬ Spec.ledger.batch_all_valid_all_applied.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances | batch            |
                   | [1, 0]   | [0->1:1, 0->1:1] |
                   When the batch [0->1:1, 0->1:1] is applied to ledger Main  =>  returned 1 applied; Main: balances [0, 1]
                   failed Then: "the number of transfers applied is the length of [0->1:1, 0->1:1]"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-all-valid, LW-batch, LT-all-applied
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 553 of 553 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, every, l.transfers, l.valid, result_is, l.applied, l.length, calls.every, D1, D2, D4, D5, D8
  tested           the reading on 3267 generated inputs (63 in scope): the definition of each frame and its executable reading agree on 63 of 63 evaluations; the reading is false at one of them
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, every, l.transfers, l.valid, result_is, l.applied, l.length, calls.every, D1, D2, D4, D5, D8`:

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
  Reading   for clause 1: a transfer: every ledger, every transfer (sender->receiver:amount, two usize account
            numbers and a u64 amount); every such call, accepted or rejected [default D2]; then the call gives an
            answer [default D1]; the answer is an acceptance (see `accepted`) if and only if the transfer can be
            carried out exactly on the ledger (both accounts exist and differ, the sender covers the amount, the
            receiver's balance stays within 2^64 - 1); ONLY rejected calls [asked for]; then the balances of the
            ledger, account by account after the call equals the balances of the ledger, account by account before
            it; clause 3: a transfer: every ledger, every transfer (sender->receiver:amount, two usize account
            numbers and a u64 amount); ONLY accepted calls [asked for]; then the balance, in the ledger, of account
            the sending account of the transfer (0 if there is no such account) after the call, plus the amount of
            the transfer, equals the balance, in the ledger, of account the sending account of the transfer (0 if
            there is no such account) before it, exactly; the balance, in the ledger, of account the receiving
            account of the transfer (0 if there is no such account) after the call equals the balance, in the
            ledger, of account the receiving account of the transfer (0 if there is no such account) before it plus
            the amount of the transfer, exactly; the accounts of the ledger are the same after the call, and every
            one of them other than the sending account of the transfer and the receiving account of the transfer has
            the balance it had before
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            528 of 528 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   8 of 8 pass on the compiled Rust; 8 of 8 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.single_transfer.holds, Rule.ledger.single_transfer.from_scenarios: the rule
                     statement for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, no-op, identity, constant; still allows: (none found)
            alone, "An invalid transfer is rejected and changes nothing" would also hold of: reject-all, identity; ruled
              out here by "A valid transfer is accepted and moves exactly its amount"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      43 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, exactly_when: frame, unsigned, holds_of: modifier, unsigned,
                 l.the_transfer: domain, unsigned, l.valid: domain, unsigned, accepted: modifier, unsigned, rejected:
                 modifier, unsigned, never_changes: frame, unsigned, l.ledger: domain, unsigned, successful:
                 modifier, unsigned, decreases_by: frame, unsigned, increases_by: frame, unsigned, changes_only:
                 frame, unsigned, i.moved: idiom, unsigned, l.bal_of: domain, unsigned, l.sender: domain, unsigned,
                 l.amount_of: domain, unsigned, l.receiver: domain, unsigned, l.accounts: domain, unsigned,
                 calls.every: coverage, unsigned, calls.rejected: coverage, unsigned, calls.accepted: coverage,
                 unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.clauses: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D3: default, unsigned, D4: default, unsigned, D8: default,
                 unsigned, given: modifier, unsigned, i.holds: idiom, unsigned, is: modifier, unsigned,
                 balances_value: modifier, unsigned, always: frame, unsigned, l.accepted: domain, unsigned,
                 aggregate: modifier, unsigned, l.balances_of: domain, unsigned, not: modifier, unsigned, never:
                 frame, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 9 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 2 scenario theorems
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.single_transfer.holds, Rule.ledger.single_transfer.from_scenarios,
                 Spec.ledger.transfer_valid_moves, Spec.ledger.transfer_invalid_rejected)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows (8 give the same result on the compiled Rust and on the model) and
                 on 66 generated inputs of the rule statement (528 of 528 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  clause 1: a transfer: every ledger, every transfer (sender->receiver:amount, two usize account
                        numbers and a u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`) if and only if the transfer can be carried out
                        exactly on the ledger (both accounts exist and differ, the sender covers the amount, the
                        receiver's balance stays within 2^64 - 1)
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
                        clause 2: a transfer: every ledger, every transfer (sender->receiver:amount, two usize account
                        numbers and a u64 amount)
            covers      ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
                        clause 3: a transfer: every ledger, every transfer (sender->receiver:amount, two usize account
                        numbers and a u64 amount)
            covers      ONLY accepted calls [asked for]
            assuming    nothing: every state and every input
            then        the balance, in the ledger, of account the sending account of the transfer (0 if there is no such
                        account) after the call, plus the amount of the transfer, equals the balance, in the ledger, of
                        account the sending account of the transfer (0 if there is no such account) before it, exactly
                        the balance, in the ledger, of account the receiving account of the transfer (0 if there is no
                        such account) after the call equals the balance, in the ledger, of account the receiving account
                        of the transfer (0 if there is no such account) before it plus the amount of the transfer, exactly
                        the accounts of the ledger are the same after the call, and every one of them other than the
                        sending account of the transfer and the receiving account of the transfer has the balance it had
                        before
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
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
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             528 of 528 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 33 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 33 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing   [a part: the rule statement is proved from it]
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
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>
            (sender->receiver:amount, two usize account numbers and a u64 amount); for every value of balances (a list
            of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            the accounts of ledger Main are the same after the call, and every one of them other than the sending
            account of the transfer <t> and the receiving account of the transfer <t> has the balance it had before
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A valid transfer is accepted and moves exactly its amount
  kernel-checked   theorem Spec.ledger.transfer_valid_moves.reading_holds : Spec.ledger.transfer_valid_moves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.transfer_valid_moves.reading_iff : Spec.ledger.transfer_valid_moves.reading ↔ Spec.ledger.transfer_valid_moves.stmt  (NEW ↔ OLD: the reading compiled from 29 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.transfer_valid_moves.reading_sat)
  kernel-checked   theorem Spec.ledger.transfer_valid_moves : Spec.ledger.transfer_valid_moves.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_valid_moves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_valid_moves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1036 of 1036 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 29 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, l.valid, always, decreases_by, increases_by, changes_only, never_changes, l.accepted, i.moved, l.bal_of, l.sender, l.amount_of, l.receiver, l.accounts, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 726 generated inputs (18 in scope): the definition of each frame and its executable reading agree on 90 of 90 evaluations
  tested           the reading on the COMPILED RUST at the same 726 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 4356 of 4356 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, l.valid, always, decreases_by, increases_by, changes_only, never_changes, l.accepted, i.moved, l.bal_of, l.sender, l.amount_of, l.receiver, l.accounts, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8`:

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
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>
            (sender->receiver:amount, two usize account numbers and a u64 amount); for every value of balances (a list
            of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  An invalid transfer is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected.reading_holds : Spec.ledger.transfer_invalid_rejected.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected.reading_iff : Spec.ledger.transfer_invalid_rejected.reading ↔ Spec.ledger.transfer_invalid_rejected.stmt  (NEW ↔ OLD: the reading compiled from 20 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.transfer_invalid_rejected.reading_sat)
  kernel-checked   theorem Spec.ledger.transfer_invalid_rejected : Spec.ledger.transfer_invalid_rejected.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/transfer_invalid_rejected.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.transfer_invalid_rejected.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-invalid, LW-transfer, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 310 of 310 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
  NOT ASSERTED     0 of 20 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, not, l.valid, never, never_changes, always, l.accepted, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 726 generated inputs (48 in scope): the definition of each frame and its executable reading agree on 96 of 96 evaluations
  tested           the reading on the COMPILED RUST at the same 726 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 2178 of 2178 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, holds_of, l.the_transfer, not, l.valid, never, never_changes, always, l.accepted, calls.every, D1, D2, D3, D4, D8`:

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
  Reading   for a computation of the total: every ledger; every such call, accepted or rejected [default D2]; then
            the call gives an answer [default D1]; the answer is an acceptance (see `accepted`) if and only if the
            sum of the balances of every account of the ledger is at most the largest total that can be reported
            (2^64 - 1)
  Verdict   PROVED FOR ALL INPUTS (by a hand-written proof)
  Examples  8 of 8 pass on the compiled Rust; 8 of 8 pass on the Lean model
  Generated the rule statement at 11 generated inputs on the compiled Rust: the same result as on the Lean model at
            22 of 22 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   8 of 8 pass on the compiled Rust; 8 of 8 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.total_fits: the rule statement for all inputs and all sizes, a hand-written
                     proof; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, no-op; still allows: (none found)
            alone, "The total of balances that do not fit is reported as absent" would also hold of: reject-all; ruled
              out here by "The total is the sum of the balances when that fits"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      30 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.total: domain, unsigned, exactly_when: frame, unsigned, at_most_value: modifier, unsigned,
                 aggregate: modifier, unsigned, l.balances_of: domain, unsigned, l.maximum: domain, unsigned,
                 accepted: modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned, D8: default, unsigned, given: modifier,
                 unsigned, i.holds: idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned,
                 balances_value: modifier, unsigned, amount_value: modifier, unsigned, result_is: frame, unsigned,
                 l.result: domain, unsigned, amount_result: modifier, unsigned, exceeds: modifier, unsigned, never:
                 frame, unsigned, always: frame, unsigned, not: modifier, unsigned, l.found: domain, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, a hand-written proof, 2 scenario
                 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.total_fits, Spec.ledger.total_is_sum, Spec.ledger.total_overflow)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 8 example rows (8 give the same result on the compiled Rust and on the model) and
                 on 11 generated inputs of the rule statement (22 of 22 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a computation of the total: every ledger
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`) if and only if the sum of the balances of every
                        account of the ledger is at most the largest total that can be reported (2^64 - 1)
            accepted    an acceptance is an answer that carries a value; an answer with no value is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger.total_fits : Rule.ledger.total_fits.reading  (hand-written,
                             lean/Wallet/RuleProofs/ledger/total_fits.lean; type checked by the audit); axioms propext,
                             Classical.choice, Quot.sound
            glue             the generated glue from the scenarios did not go through (the generated proof script failed
                             (see out/links.log))
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 11 generated inputs (11 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 11 of 11 evaluations
            tested           the reading on the COMPILED RUST at the same 11 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             22 of 22 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 16 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total is the sum of the balances when that fits   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  The total of balances that do not fit is reported as absent   [a part: the rule statement is proved from it]
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
  And the total of the balances of ledger Main is <sum>
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
applies to  computing the total of ledger Main: every ledger Main; for every value of balances (a list of u64 balances,
            account 0 first), sum (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  The total is the sum of the balances when that fits
  kernel-checked   theorem Spec.ledger.total_is_sum.reading_holds : Spec.ledger.total_is_sum.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.total_is_sum.reading_iff : Spec.ledger.total_is_sum.reading ↔ Spec.ledger.total_is_sum.stmt  (NEW ↔ OLD: the reading compiled from 17 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_is_sum.reading_sat)
  kernel-checked   theorem Spec.ledger.total_is_sum : Spec.ledger.total_is_sum.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/total_is_sum.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_is_sum.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 217 of 217 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
  NOT ASSERTED     0 of 17 Clausebook pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result, calls.every, D1, D2, D4, D8
  tested           the reading on 726 generated inputs (6 in scope): the definition of each frame and its executable reading agree on 6 of 6 evaluations
  tested           the reading on the COMPILED RUST at the same 726 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 1452 of 1452 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result, calls.every, D1, D2, D4, D8`:

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
  And the total of the balances of ledger Main is more than the maximum
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
applies to  computing the total of ledger Main: every ledger Main; for every value of balances (a list of u64 balances,
            account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  The total of balances that do not fit is reported as absent
  kernel-checked   theorem Spec.ledger.total_overflow.reading_holds : Spec.ledger.total_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.total_overflow.reading_iff : Spec.ledger.total_overflow.reading ↔ Spec.ledger.total_overflow.stmt  (NEW ↔ OLD: the reading compiled from 19 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_overflow.reading_sat)
  kernel-checked   theorem Spec.ledger.total_overflow : Spec.ledger.total_overflow.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/total_overflow.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 137 of 137 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 19 Clausebook pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found, calls.every, D1, D2, D4, D8
  tested           the reading on 121 generated inputs (3 in scope): the definition of each frame and its executable reading agree on 3 of 3 evaluations
  tested           the reading on the COMPILED RUST at the same 121 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 242 of 242 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found, calls.every, D1, D2, D4, D8`:

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
  Reading   for a computation of the total: every ledger; every such call, accepted or rejected [default D2]; then
            the call gives an answer [default D1]; the answer is an acceptance (see `accepted`)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 11 generated inputs on the compiled Rust: the same result as on the Lean model at
            22 of 22 evaluations; it is FALSE at {"the_ledger": "[18446744073709551615, 1]"}, on the compiled Rust
            too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  FALSE at an input found at generated input 2 and shrunk: {"the_ledger": "[5003681978720493492,
                     13443062094989058124]"} (seed 20261111); of the 1 scenario beneath it, 0 not falsified, 1 shown
                     false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[1,
                     18446744073709551615]"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger.total_always.refuted (the negation of the rule
                     statement) at {"the_ledger": "[18446744073709551615, 1]"}; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[5003681978720493492, 13443062094989058124]"}   source: generated property test
                     (case 2 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model
                     the reading fails
    found false at   {"the_ledger": "[1, 18446744073709551615]"}   source: generated bounded check (Kani at up to 2
                     accounts; replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the
                     compiled Rust it fails; on the Lean model the reading fails
    found false at   [The total of a ledger can always be computed] {"balances": "[4, 18446744073709551615]",
                     "main_state": "[4, 18446744073709551615]"}   source: generated property test (case 2 of the run,
                     shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   [The total of a ledger can always be computed] {"balances": "[18446744073709551615,
                     18446744073709551615]", "main_state": "[18446744073709551615, 18446744073709551615]"}   source:
                     generated bounded check (Kani at up to 2 accounts; replayed on the compiled Rust through the
                     generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the
                     reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: no scenario of this group is meant to be proved

  Rests on
    meaning      17 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.total: domain, unsigned, always: frame, unsigned, accepted: modifier, unsigned, calls.every:
                 coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.line: grammar,
                 unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, given: modifier,
                 unsigned, i.holds: idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned,
                 balances_value: modifier, unsigned, l.found: domain, unsigned, D8: default, unsigned)
                 1 of 1 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 3 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input, 1 refutation (the
                 scenario is false); axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.total_always.refuted, Spec.ledger.total_always_available.refuted)
    translation  Lean model ledger.Ledger.total generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 11 generated inputs of the rule statement (22 of 22 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a computation of the total: every ledger
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`)
            accepted    an acceptance is an answer that carries a value; an answer with no value is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger.total_always.refuted : ¬ Rule.ledger.total_always.reading; axioms
                             propext, Classical.choice, Quot.sound
            counterexample   ledger = [18446744073709551615, 1]
                             at this input the rule does not hold: NOT "the answer is an acceptance (see `accepted`)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 11 generated inputs (11 in scope): counterexample found; the definition of each
                             frame and its executable reading agree on 11 of 11 evaluations
            tested           the reading on the COMPILED RUST at the same 11 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             22 of 22 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 10 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 10 Clausebook pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         The total of a ledger can always be computed   (expected REFUTED)   [beneath the rule; not used to prove it]
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
applies to  computing the total of ledger Main: every ledger Main; for every value of balances (a list of u64 balances,
            account 0 first)
covers      every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the call returns a value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
REFUTED  The total of a ledger can always be computed
  kernel-checked   theorem Spec.ledger.total_always_available.reading_iff : Spec.ledger.total_always_available.reading ↔ Spec.ledger.total_always_available.stmt  (NEW ↔ OLD: the reading compiled from 13 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.total_always_available.reading_sat)
  kernel-checked   theorem Spec.ledger.total_always_available.refuted : ¬ Spec.ledger.total_always_available.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances                  |
                   | [18446744073709551615, 1] |
                   When the total of ledger Main is computed  =>  returned None
                   failed Then: "there is a result"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.total, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-total, LT-some-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 126 of 126 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 11 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
  NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone - UNREVIEWED: l.total, given, i.holds, is, l.ledger, balances_value, always, l.found, calls.every, D1, D2, D4, D8
  tested           the reading on 121 generated inputs (11 in scope): the definition of each frame and its executable reading agree on 11 of 11 evaluations; the reading is false at one of them
  tested           the reading on the COMPILED RUST at the same 121 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 242 of 242 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.total, given, i.holds, is, l.ledger, balances_value, always, l.found, calls.every, D1, D2, D4, D8`:

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
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the value the call returns is the
            balance of account the account of the ledger before the call (absent if there is no such account)
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  4 of 4 pass on the compiled Rust; 4 of 4 pass on the Lean model
  Generated the rule statement at 55 generated inputs on the compiled Rust: the same result as on the Lean model at
            110 of 110 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   4 of 4 pass on the compiled Rust; 4 of 4 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.lookup.holds, Rule.ledger.lookup.from_scenarios: the rule statement for all
                     inputs and all sizes, from its scenarios; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     suite rules out: reject-all, no-op; still allows: (none found)
            alone, "Looking up an account that does not exist gives nothing" would also hold of: reject-all; ruled out
              here by "Looking up an existing account gives its balance"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      23 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, result_is: frame, unsigned, l.result: domain, unsigned, l.balance_at:
                 domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_for:
                 grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2:
                 default, unsigned, D4: default, unsigned, given: modifier, unsigned, i.holds: idiom, unsigned, is:
                 modifier, unsigned, l.ledger: domain, unsigned, balances_value: modifier, unsigned, l.is_account:
                 domain, unsigned, D8: default, unsigned, not: modifier, unsigned, never: frame, unsigned, always:
                 frame, unsigned, l.found: domain, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 6 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 2 scenario theorems
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.lookup.holds, Rule.ledger.lookup.from_scenarios, Spec.ledger.balance_of_account,
                 Spec.ledger.balance_no_account)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4 example rows (4 give the same result on the compiled Rust and on the model) and
                 on 55 generated inputs of the rule statement (110 of 110 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
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
            tested           the reading on the COMPILED RUST at the same 55 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             110 of 110 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  Looking up an existing account gives its balance   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Looking up an account that does not exist gives nothing   [a part: the rule statement is proved from it]
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
applies to  looking up the balance of account <i> of ledger Main: every ledger Main, and every account <i> (an account
            number, a usize); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Looking up an existing account gives its balance
  kernel-checked   theorem Spec.ledger.balance_of_account.reading_holds : Spec.ledger.balance_of_account.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.balance_of_account.reading_iff : Spec.ledger.balance_of_account.reading ↔ Spec.ledger.balance_of_account.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.balance_of_account.reading_sat)
  kernel-checked   theorem Spec.ledger.balance_of_account : Spec.ledger.balance_of_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_of_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_of_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-account, LW-balance, LT-balance
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 451 of 451 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: l.lookup, given, i.holds, is, l.ledger, balances_value, l.is_account, result_is, l.result, l.balance_at, calls.every, D1, D2, D4, D8
  tested           the reading on 605 generated inputs (24 in scope): the definition of each frame and its executable reading agree on 24 of 24 evaluations
  tested           the reading on the COMPILED RUST at the same 605 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 1210 of 1210 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.lookup, given, i.holds, is, l.ledger, balances_value, l.is_account, result_is, l.result, l.balance_at, calls.every, D1, D2, D4, D8`:

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
applies to  looking up the balance of account <i> of ledger Main: every ledger Main, and every account <i> (an account
            number, a usize); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; <i> is NOT an account number of ledger Main
then        the call gives an answer [default D1]
            the call returns no value
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Looking up an account that does not exist gives nothing
  kernel-checked   theorem Spec.ledger.balance_no_account.reading_holds : Spec.ledger.balance_no_account.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.balance_no_account.reading_iff : Spec.ledger.balance_no_account.reading ↔ Spec.ledger.balance_no_account.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.balance_no_account.reading_sat)
  kernel-checked   theorem Spec.ledger.balance_no_account : Spec.ledger.balance_no_account.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/ledger/balance_no_account.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.balance_no_account.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.balance, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.balance: Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-no-account, LW-balance, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 181 of 181 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.lookup, given, i.holds, is, l.ledger, balances_value, not, l.is_account, never, always, l.found, calls.every, D1, D2, D4, D8
  tested           the reading on 605 generated inputs (31 in scope): the definition of each frame and its executable reading agree on 31 of 31 evaluations
  tested           the reading on the COMPILED RUST at the same 605 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 1210 of 1210 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.lookup, given, i.holds, is, l.ledger, balances_value, not, l.is_account, never, always, l.found, calls.every, D1, D2, D4, D8`:

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
  Reading   for clause 1: a batch applied as a whole: every ledger, every batch (a list of transfers, in order);
            ONLY rejected calls [asked for]; then the balances of the ledger, account by account after the call
            equals the balances of the ledger, account by account before it; every such call, accepted or rejected
            [default D2]; then the call gives an answer [default D1]; the sum of the balances of every account of
            the ledger after the call equals the sum of the balances of every account of the ledger before it
  Verdict   PROVED FOR ALL INPUTS (from its scenarios)
  Examples  10 of 10 pass on the compiled Rust; 10 of 10 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            1188 of 1188 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   10 of 10 pass on the compiled Rust; 10 of 10 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 6
                     scenarios beneath it, 6 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 2 accounts and up to 3 transfers; NO ANSWER in 30 s with up to 4
                     accounts and up to 1 transfer; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.whole_batch.holds, Rule.ledger.whole_batch.from_scenarios: the rule
                     statement for all inputs and all sizes, from its scenarios; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

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
    meaning      33 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_all: domain, unsigned, rejected: modifier, unsigned, never_changes: frame, unsigned,
                 l.ledger: domain, unsigned, aggregate: modifier, unsigned, l.balances_of: domain, unsigned,
                 calls.rejected: coverage, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.clauses: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4: default,
                 unsigned, given: modifier, unsigned, i.holds: idiom, unsigned, is: modifier, unsigned,
                 balances_value: modifier, unsigned, always_answers: frame, unsigned, D8: default, unsigned,
                 the_first: modifier, unsigned, l.transfers: domain, unsigned, not: modifier, unsigned, l.valid:
                 domain, unsigned, never: frame, unsigned, always: frame, unsigned, l.accepted: domain, unsigned, D5:
                 default, unsigned, D6: default, unsigned, becomes: frame, unsigned)
                 6 of 6 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 9 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 3 scenario theorems
                 for all inputs, 3 for literal values only; axioms: propext, Classical.choice, Quot.sound (the
                 standard three only)   [kernel-checked]
                 (Rule.ledger.whole_batch.holds, Rule.ledger.whole_batch.from_scenarios,
                 Spec.ledger.whole_rejected_unchanged, Spec.ledger.whole_first_invalid, Spec.ledger.whole_conserves,
                 Spec.ledger.whole_example_accept, Spec.ledger.whole_example_rollback_late,
                 Spec.ledger.whole_example_rollback)
    translation  Lean model ledger.Ledger.apply_all generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 10 example rows (10 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (1188 of 1188 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  clause 1: a batch applied as a whole: every ledger, every batch (a list of transfers, in order)
            covers      ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
                        clause 2: a batch applied as a whole: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
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
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             1188 of 1188 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 17 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 17 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 3 of 3 universal scenarios proved for all inputs; 3 of 3 literal examples proved for their own values
            PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing   [a part: the rule statement is proved from it]
            PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances   [a part: the rule statement is proved from it]
            PROVED-INSTANCE A batch of valid transfers applied as a whole is accepted and applied   [an instance: literal values]
            PROVED-INSTANCE A batch applied as a whole is rolled back when its third transfer is invalid   [an instance: literal values]
            PROVED-INSTANCE A batch applied as a whole is rolled back when a later transfer is invalid   [an instance: literal values]
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
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch> (a list of
            transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]; ONLY rejected calls [asked for]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            if the call is rejected: the balances of ledger Main, account by account after the call equals the balances
            of ledger Main, account by account before it
accepted    an acceptance is the answer yes (true); the answer no is a rejection
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or
            that give no answer, are outside this clause
```

```text
PROVED-FOR-ALL  A batch applied as a whole that is rejected leaves the ledger unchanged
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged.reading_holds : Spec.ledger.whole_rejected_unchanged.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged.reading_iff : Spec.ledger.whole_rejected_unchanged.reading ↔ Spec.ledger.whole_rejected_unchanged.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_rejected_unchanged.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_rejected_unchanged : Spec.ledger.whole_rejected_unchanged.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_rejected_unchanged.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_rejected_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-same-if-rejected
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 363 of 363 grid points
  tested           4 of 4 rows pass on compiled Rust (cucumber-rs); 4 of 4 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, rejected, always_answers, never_changes, calls.every, calls.rejected, D1, D2, D3, D4, D8
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 594 of 594 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 9801 of 9801 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, rejected, always_answers, never_changes, calls.every, calls.rejected, D1, D2, D3, D4, D8`:

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
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch> (a list of
            transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
  kernel-checked   theorem Spec.ledger.whole_first_invalid.reading_holds : Spec.ledger.whole_first_invalid.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_first_invalid.reading_iff : Spec.ledger.whole_first_invalid.reading ↔ Spec.ledger.whole_first_invalid.stmt  (NEW ↔ OLD: the reading compiled from 22 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_first_invalid.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_first_invalid : Spec.ledger.whole_first_invalid.stmt (type checked by the audit; 5-line proof, lean/Wallet/Proofs/ledger/whole_first_invalid.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_first_invalid.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-whole, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 541 of 541 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 22 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, never, never_changes, always, l.accepted, calls.every, D1, D2, D3, D4, D5, D6, D8
  tested           the reading on 3267 generated inputs (188 in scope): the definition of each frame and its executable reading agree on 376 of 376 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 9801 of 9801 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, the_first, l.transfers, not, l.valid, never, never_changes, always, l.accepted, calls.every, D1, D2, D3, D4, D5, D6, D8`:

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
applies to  applying the batch <batch> to ledger Main as a whole: every ledger Main, and every batch <batch> (a list of
            transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  Applying a batch as a whole conserves the total of all balances
  kernel-checked   theorem Spec.ledger.whole_conserves.reading_holds : Spec.ledger.whole_conserves.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_conserves.reading_iff : Spec.ledger.whole_conserves.reading ↔ Spec.ledger.whole_conserves.stmt  (NEW ↔ OLD: the reading compiled from 15 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_conserves.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_conserves : Spec.ledger.whole_conserves.stmt (type checked by the audit; 3-line proof, lean/Wallet/Proofs/ledger/whole_conserves.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_conserves.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 3267 generated inputs (297 in scope): the definition of each frame and its executable reading agree on 297 of 297 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8`:

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
  And ledger Main is now [70, 0, 50]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50] to ledger Main as a whole: every ledger Main, with the one batch
            [0->1:30, 1->2:50] (a plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  A batch of valid transfers applied as a whole is accepted and applied
  kernel-checked   theorem Spec.ledger.whole_example_accept.reading_holds : Spec.ledger.whole_example_accept.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_accept.reading_iff : Spec.ledger.whole_example_accept.reading ↔ Spec.ledger.whole_example_accept.stmt  (NEW ↔ OLD: the reading compiled from 14 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_accept.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_accept : Spec.ledger.whole_example_accept.stmt (type checked by the audit; 6-line proof, lean/Wallet/Proofs/ledger/whole_example_accept.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_accept.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-accepted, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 14 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, always, becomes, l.accepted, calls.every, D1, D2, D4, D8
  tested           the reading on 13 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
  tested           the reading on the COMPILED RUST at the same 13 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 39 of 39 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, always, becomes, l.accepted, calls.every, D1, D2, D4, D8`:

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
  And ledger Main is now [100, 20, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 1->2:50, 2->0:60] to ledger Main as a whole: every ledger Main, with the one
            batch [0->1:30, 1->2:50, 2->0:60] (a plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when its third transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late.reading_holds : Spec.ledger.whole_example_rollback_late.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late.reading_iff : Spec.ledger.whole_example_rollback_late.reading ↔ Spec.ledger.whole_example_rollback_late.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_rollback_late.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_rollback_late : Spec.ledger.whole_example_rollback_late.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback_late.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback_late.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, calls.every, D1, D2, D4, D8
  tested           the reading on 12 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
  tested           the reading on the COMPILED RUST at the same 12 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 36 of 36 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, calls.every, D1, D2, D4, D8`:

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
  And ledger Main is now [100, 20, 0]
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch [0->1:30, 2->1:5] to ledger Main as a whole: every ledger Main, with the one batch
            [0->1:30, 2->1:5] (a plain Scenario: the values are the literals written in it)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-INSTANCE  A batch applied as a whole is rolled back when a later transfer is invalid
  kernel-checked   theorem Spec.ledger.whole_example_rollback.reading_holds : Spec.ledger.whole_example_rollback.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.whole_example_rollback.reading_iff : Spec.ledger.whole_example_rollback.reading ↔ Spec.ledger.whole_example_rollback.stmt  (NEW ↔ OLD: the reading compiled from 16 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.whole_example_rollback.reading_sat)
  kernel-checked   theorem Spec.ledger.whole_example_rollback : Spec.ledger.whole_example_rollback.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/whole_example_rollback.lean:19); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.whole_example_rollback.sat)
  scope            THIS input only (plain Scenario: the values are literals)
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, calls.every, D1, D2, D4, D8
  tested           the reading on 12 generated inputs (1 in scope): the definition of each frame and its executable reading agree on 2 of 2 evaluations
  tested           the reading on the COMPILED RUST at the same 12 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 36 of 36 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_all, given, i.holds, is, l.ledger, balances_value, never, becomes, always, not, l.accepted, calls.every, D1, D2, D4, D8`:

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
  Reading   for a batch followed by a computation of the total: every ledger, every batch (a list of transfers, in
            order); every such call, accepted or rejected [default D2]; then the call gives an answer [default D1];
            the answer is an acceptance (see `accepted`) if and only if the sum of the balances of every account of
            the ledger is at most the largest total that can be reported (2^64 - 1); (of a sequence: every call in
            it must answer; the answer spoken of is the LAST call's)
  Verdict   PROVED FOR ALL INPUTS (by a hand-written proof)
  Examples  5 of 5 pass on the compiled Rust; 5 of 5 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   5 of 5 pass on the compiled Rust; 5 of 5 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 2
                     scenarios beneath it, 2 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; NO ANSWER in 30 s with up to 4 accounts and up to 1 transfer; with up to 2
                     accounts and up to 3 transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger.batch_then_total: the rule statement for all inputs and all sizes, a
                     hand-written proof; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     [ledger.Ledger.apply_batch] suite rules out: (nothing); still allows: reject-all: always answers `0` and
              leaves the state as it was [no scenario counted is false of it on the search grid]; no-op: reports every
              transfer of the batch as applied and leaves the state as it was [no scenario counted is false of it on the
              search grid]; identity: answers as the code does, but never changes the state [no scenario counted is
              false of it on the search grid]; constant (4 of 9 variants): always answers `1` and leaves the state as it
              was; always answers `2` and leaves the state as it was; and 2 more [no scenario counted is false of it on
              the search grid]
            [ledger.Ledger.apply_batch] taken alone, this group would also hold of: reject-all, no-op, identity,
              constant (7 variants); the whole suite for `ledger.Ledger.apply_batch` rules them out through Rule "A
              batch never changes the total of all balances of the ledger"; Rule "For a batch, the number of transfers
              applied is at most the length of the batch, and for a batch for which the first transfer of the batch is
              not valid on the ledger, the number of transfers applied is zero and the ledger is unchanged"
            [ledger.Ledger.total] suite rules out: reject-all, no-op; still allows: (none found)
            [ledger.Ledger.total] alone, "The total computed after any batch is still absent when it did not fit before"
              would also hold of: reject-all; ruled out here by "The total computed after any batch is the total before
              it, when that total fits"
            (A single scenario or rule that also holds of a trivial implementation is expected; adequacy is judged for
              the suite.)

  Rests on
    meaning      32 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, l.total: domain, unsigned, and_then: modifier, unsigned,
                 exactly_when: frame, unsigned, at_most_value: modifier, unsigned, aggregate: modifier, unsigned,
                 l.balances_of: domain, unsigned, l.maximum: domain, unsigned, accepted: modifier, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role:
                 grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4:
                 default, unsigned, D8: default, unsigned, given: modifier, unsigned, i.holds: idiom, unsigned, is:
                 modifier, unsigned, l.ledger: domain, unsigned, balances_value: modifier, unsigned, amount_value:
                 modifier, unsigned, result_is: frame, unsigned, l.result: domain, unsigned, amount_result: modifier,
                 unsigned, exceeds: modifier, unsigned, never: frame, unsigned, always: frame, unsigned, not:
                 modifier, unsigned, l.found: domain, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 7 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: the rule statement for all inputs, a hand-written proof, 2 scenario
                 theorems for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger.batch_then_total, Spec.ledger.batch_then_total, Spec.ledger.batch_then_total_overflow)
    translation  Lean models ledger.Ledger.apply_batch, ledger.Ledger.total generated from ledger/src/lib.rs by
                 charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 cross-checked on 5 example rows (5 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (594 of 594 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch followed by a computation of the total: every ledger, every batch (a list of transfers, in
                        order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`) if and only if the sum of the balances of every
                        account of the ledger is at most the largest total that can be reported (2^64 - 1)
                        (of a sequence: every call in it must answer; the answer spoken of is the LAST call's)
            accepted    an acceptance is an answer that carries a value; an answer with no value is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger.batch_then_total : Rule.ledger.batch_then_total.reading  (hand-written,
                             lean/Wallet/RuleProofs/ledger/batch_then_total.lean; type checked by the audit); axioms
                             propext, Classical.choice, Quot.sound
            glue             no glue from the scenarios was generated: no universal scenario beneath the rule is about
                             one operation with nothing pinned
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 18 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 2 of 2 universal scenarios proved for all inputs
            PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits   [beneath the rule; not used to prove it]
            PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before   [beneath the rule; not used to prove it]
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
  And the total of the balances of ledger Main is <sum>
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
            Main: every ledger Main, and every batch <batch> (a list of transfers, in order); for every value of
            balances (a list of u64 balances, account 0 first), sum (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  The total computed after any batch is the total before it, when that total fits
  kernel-checked   theorem Spec.ledger.batch_then_total.reading_holds : Spec.ledger.batch_then_total.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_then_total.reading_iff : Spec.ledger.batch_then_total.reading ↔ Spec.ledger.batch_then_total.stmt  (NEW ↔ OLD: the reading compiled from 19 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_then_total.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_then_total : Spec.ledger.batch_then_total.stmt (type checked by the audit; 10-line proof, lean/Wallet/Proofs/ledger/batch_then_total.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-batch, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 217 of 217 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  NOT ASSERTED     0 of 19 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result, calls.every, D1, D2, D4, D8
  tested           the reading on 19602 generated inputs (162 in scope): the definition of each frame and its executable reading agree on 162 of 162 evaluations
  tested           the reading on the COMPILED RUST at the same 19602 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 39204 of 39204 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, aggregate, l.balances_of, amount_value, result_is, l.result, amount_result, calls.every, D1, D2, D4, D8`:

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
  And the total of the balances of ledger Main is more than the maximum
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
            Main: every ledger Main, and every batch <batch> (a list of transfers, in order); for every value of
            balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  The total computed after any batch is still absent when it did not fit before
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow.reading_holds : Spec.ledger.batch_then_total_overflow.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow.reading_iff : Spec.ledger.batch_then_total_overflow.reading ↔ Spec.ledger.batch_then_total_overflow.stmt  (NEW ↔ OLD: the reading compiled from 21 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger.batch_then_total_overflow.reading_sat)
  kernel-checked   theorem Spec.ledger.batch_then_total_overflow : Spec.ledger.batch_then_total_overflow.stmt (type checked by the audit; 7-line proof, lean/Wallet/Proofs/ledger/batch_then_total_overflow.lean:20); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.ledger.batch_then_total_overflow.sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.U64.checked_add, Aeneas.Std.instHSubUScalarResult, Aeneas.Std.instHAddUScalarResult, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index, Aeneas.Std.alloc.vec.Vec.index_mut, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-batch, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 137 of 137 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  NOT ASSERTED     0 of 21 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found, calls.every, D1, D2, D4, D8
  tested           the reading on 3267 generated inputs (81 in scope): the definition of each frame and its executable reading agree on 81 of 81 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, l.total, and_then, given, i.holds, is, l.ledger, balances_value, exceeds, aggregate, l.balances_of, l.maximum, never, always, not, l.found, calls.every, D1, D2, D4, D8`:

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

### Rule: An internal fund transfer never changes the aggregate account value of the ledger

```text
Rule: An internal fund transfer never changes the aggregate account value of the ledger   [features/ledger_rules.feature:14]   tags @id:readme_internal_transfers
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; assuming every account the transfer
            names is an account of the ledger (internal); then the call gives an answer [default D1]; the sum of the
            balances of every account of the ledger after the call equals the sum of the balances of every account
            of the ledger before it
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

  Suite     not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios
              of this group are NEW sentences that have none

  Rests on
    meaning      20 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, internal: modifier, unsigned, never_changes: frame, unsigned, aggregate:
                 modifier, unsigned, l.balances_of: domain, unsigned, calls.every: coverage, unsigned, g.subject:
                 grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar,
                 unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4: default,
                 unsigned, D8: default, unsigned, given: modifier, unsigned, i.holds: idiom, unsigned, is: modifier,
                 unsigned, l.ledger: domain, unsigned, balances_value: modifier, unsigned)
                 1 scenario beneath the rule is a NEW sentence: read by the Clausebook alone, no entry of the old
                 glossary
    proof        checked by Lean's kernel: the rule statement for all inputs, from its scenarios, 1 scenario theorem
                 for all inputs; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.readme_internal_transfers.holds,
                 Rule.ledger_rules.readme_internal_transfers.from_scenarios,
                 Spec.ledger_rules.readme_transfer_keeps_aggregate.reading_holds)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 66 generated inputs of the rule statement (132 of 132 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    every account the transfer names is an account of the ledger (internal)
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
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.readme_internal_transfers.holds :
                             Rule.ledger_rules.readme_internal_transfers.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem; type checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.readme_internal_transfers.from_scenarios :
                             readme_transfer_keeps_aggregate.reading →
                             Rule.ledger_rules.readme_internal_transfers.reading  (generated glue, type checked by the
                             audit); axioms propext, Classical.choice, Quot.sound
                             and each of those 1 scenario readings is PROVED-FOR-ALL (its own proof, carried through its
                             equivalence)
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (49 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 49 of 49 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 15 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 1 of 1 universal scenarios proved for all inputs
            PROVED-FOR-ALL  a transfer between two accounts of the ledger   [a part: the rule statement is proved from it]   [NEW sentence]
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.readme_internal_transfers.reading : Prop :=
  Frames.NeverChanges ((L.apply).internal L.isAccount L.parties) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### PROVED-FOR-ALL: a transfer between two accounts of the ledger

`features/ledger_rules.feature:17`  id `Spec.ledger_rules.readme_transfer_keeps_aggregate`  tags `@id:readme_transfer_keeps_aggregate`

```gherkin
Scenario Outline: a transfer between two accounts of the ledger
  Given ledger Main holds the balances <balances>
  When the transfer <t> is applied to ledger Main
  Then the aggregate account value of ledger Main is unchanged

  Examples:
    | balances      | t        |
    | [100, 20, 0]  | 0->1:30  |
    | [100, 600]    | 1->0:500 |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>
            (sender->receiver:amount, two usize account numbers and a u64 amount); for every value of balances (a list
            of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  a transfer between two accounts of the ledger
  kernel-checked   theorem Spec.ledger_rules.readme_transfer_keeps_aggregate.reading_holds : Spec.ledger_rules.readme_transfer_keeps_aggregate.reading  (THE READING ITSELF, as one theorem: the supplied proof of its flat obligation carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger_rules.readme_transfer_keeps_aggregate : Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation  (hand-written, lean/Wallet/Proofs/ledger_rules/readme_transfer_keeps_aggregate.lean; type checked by the audit)
  kernel-checked   theorem Spec.ledger_rules.readme_transfer_keeps_aggregate.reading_iff_obligation : Spec.ledger_rules.readme_transfer_keeps_aggregate.reading ↔ Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation  (generated script; the audit checked its type and that its proof uses no proof of either side); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger_rules.readme_transfer_keeps_aggregate.reading_sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     reading compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 15 Clausebook pieces; echoed above for comparison with the scenario
  new sentence     no entry of the old whole-phrase glossary is involved: no flat statement of that kind, no hand-written step, no hand-written Rust predicate
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs, generic step: the composition tree evaluated by the per-piece Rust readings); 2 of 2 pass on the Lean model; they agree
  tested           the reading on 726 generated inputs (66 in scope) on the Lean model: no counterexample; the definition of each frame and its executable reading agree on 66 of 66 evaluations
  tested           the reading on the COMPILED RUST at the same 726 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 1452 of 1452 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, never_changes, aggregate, l.balances_of, calls.every, D1, D2, D3, D4, D8`:

```lean
def Spec.ledger_rules.readme_transfer_keeps_aggregate.reading : Prop :=
  ∀ (balances : List U64),
    Frames.NeverChanges ((L.apply).given (fun st inp => (L.balances st) = balances)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

Flat proof obligation, generated from the pieces (`lean/Wallet/Obligations.lean`); a NEW sentence has no flat statement in the old glossary:

```lean
def Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

Supplied proof of the obligation (`lean/Wallet/Proofs/ledger_rules/readme_transfer_keeps_aggregate.lean`):

```lean
theorem Spec.ledger_rules.readme_transfer_keeps_aggregate : Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation := by
  intro balances st inp _
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
  · exact ht
  · rfl
```

</details>

### Rule: An internal transfer never changes the total of all balances of the ledger

```text
Rule: An internal transfer never changes the total of all balances of the ledger   [features/ledger_rules.feature:29]   tags @id:n1_internal_transfer
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; assuming every account the transfer
            names is an account of the ledger (internal); then the call gives an answer [default D1]; the sum of the
            balances of every account of the ledger after the call equals the sum of the balances of every account
            of the ledger before it
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (24626 generated), none falsifies it (seed 20261111)
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
    4 proof          theorem Rule.ledger_rules.n1_internal_transfer.proved, Rule.ledger_rules.n1_internal_transfer,
                     Rule.ledger_rules.n1_internal_transfer.reading_iff_obligation: the rule statement for all inputs
                     and all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      15 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, internal: modifier, unsigned, never_changes: frame, unsigned, aggregate:
                 modifier, unsigned, l.balances_of: domain, unsigned, calls.every: coverage, unsigned, g.subject:
                 grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar,
                 unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4: default,
                 unsigned, D8: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.n1_internal_transfer.proved, Rule.ledger_rules.n1_internal_transfer,
                 Rule.ledger_rules.n1_internal_transfer.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    every account the transfer names is an account of the ledger (internal)
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
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.n1_internal_transfer.proved :
                             Rule.ledger_rules.n1_internal_transfer.reading  (THE RULE STATEMENT ITSELF, as one theorem:
                             the supplied proof of its flat obligation carried through the equivalence; type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.n1_internal_transfer :
                             Rule.ledger_rules.n1_internal_transfer.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/n1_internal_transfer.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.n1_internal_transfer.reading_iff_obligation :
                             Rule.ledger_rules.n1_internal_transfer.reading ↔
                             Rule.ledger_rules.n1_internal_transfer.obligation  (generated script; the audit checked its
                             type and that its proof uses no proof of either side); axioms propext, Classical.choice,
                             Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (49 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 49 of 49 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 15 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.n1_internal_transfer.reading : Prop :=
  Frames.NeverChanges ((L.apply).internal L.isAccount L.parties) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

### Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger

```text
Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger   [features/ledger_rules.feature:32]   tags @id:n2_accepted_only_if_covered
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; the answer is an acceptance (see `accepted`) only if the amount of the transfer is at most the
            balance, in the ledger, of account the sending account of the transfer (0 if there is no such account)
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  3 of 3 pass on the compiled Rust; 3 of 3 pass on the Lean model
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   3 of 3 pass on the compiled Rust; 3 of 3 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 1
                     scenario beneath it, 1 not falsified, 0 shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.n2_accepted_only_if_covered.proved,
                     Rule.ledger_rules.n2_accepted_only_if_covered,
                     Rule.ledger_rules.n2_accepted_only_if_covered.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios
              of this group are NEW sentences that have none

  Rests on
    meaning      28 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, only_if: frame, unsigned, not_more_than: modifier, unsigned,
                 l.amount_of: domain, unsigned, l.bal_of: domain, unsigned, l.sender: domain, unsigned, accepted:
                 modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp:
                 grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2:
                 default, unsigned, D4: default, unsigned, D8: default, unsigned, given: modifier, unsigned, i.holds:
                 idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned, balances_value: modifier,
                 unsigned, more_than: modifier, unsigned, never: frame, unsigned, never_changes: frame, unsigned,
                 always: frame, unsigned, not: modifier, unsigned, l.accepted: domain, unsigned, D3: default,
                 unsigned)
                 1 scenario beneath the rule is a NEW sentence: read by the Clausebook alone, no entry of the old
                 glossary
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation, 1 scenario theorem for all inputs; axioms: propext, Classical.choice, Quot.sound (the
                 standard three only)   [kernel-checked]
                 (Rule.ledger_rules.n2_accepted_only_if_covered.proved,
                 Rule.ledger_rules.n2_accepted_only_if_covered,
                 Rule.ledger_rules.n2_accepted_only_if_covered.reading_iff_obligation,
                 Spec.ledger_rules.n2_short_sender_rejected.reading_holds)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 3 example rows (3 give the same result on the compiled Rust and on the model) and
                 on 66 generated inputs of the rule statement (132 of 132 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`) only if the amount of the transfer is at most the
                        balance, in the ledger, of account the sending account of the transfer (0 if there is no such
                        account)
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.n2_accepted_only_if_covered.proved :
                             Rule.ledger_rules.n2_accepted_only_if_covered.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.n2_accepted_only_if_covered :
                             Rule.ledger_rules.n2_accepted_only_if_covered.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/n2_accepted_only_if_covered.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.n2_accepted_only_if_covered.reading_iff_obligation :
                             Rule.ledger_rules.n2_accepted_only_if_covered.reading ↔
                             Rule.ledger_rules.n2_accepted_only_if_covered.obligation  (generated script; the audit
                             checked its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (66 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 16 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 1 of 1 universal scenarios proved for all inputs
            PROVED-FOR-ALL  a transfer of more than the sender holds is rejected and changes nothing   [a part: the rule statement is proved from it]   [NEW sentence]
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.n2_accepted_only_if_covered.reading : Prop :=
  Frames.OnlyIf L.apply (fun ans => (L.apply).accepted ans) (fun st inp => (L.amountOf inp) ≤ (L.bal st (L.sender inp)))
```

</details>

#### PROVED-FOR-ALL: a transfer of more than the sender holds is rejected and changes nothing

`features/ledger_rules.feature:35`  id `Spec.ledger_rules.n2_short_sender_rejected`  tags `@id:n2_short_sender_rejected`

```gherkin
Scenario Outline: a transfer of more than the sender holds is rejected and changes nothing
  Given ledger Main holds the balances <balances>
  And the amount of <t> is more than the balance of account the sender of <t> of ledger Main
  When the transfer <t> is applied to ledger Main
  Then it is rejected
  And ledger Main is unchanged

  Examples:
    | balances      | t         |
    | [100, 20, 0]  | 0->1:101  |
    | [5, 5]        | 1->0:6    |
    | [5, 5]        | 3->0:1    |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>
            (sender->receiver:amount, two usize account numbers and a u64 amount); for every value of balances (a list
            of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>; the amount of the transfer <t> is strictly
            more than the balance, in ledger Main, of account the sending account of the transfer <t> (0 if there is no
            such account)
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL  a transfer of more than the sender holds is rejected and changes nothing
  kernel-checked   theorem Spec.ledger_rules.n2_short_sender_rejected.reading_holds : Spec.ledger_rules.n2_short_sender_rejected.reading  (THE READING ITSELF, as one theorem: the supplied proof of its flat obligation carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger_rules.n2_short_sender_rejected : Spec.ledger_rules.n2_short_sender_rejected.obligation  (hand-written, lean/Wallet/Proofs/ledger_rules/n2_short_sender_rejected.lean; type checked by the audit)
  kernel-checked   theorem Spec.ledger_rules.n2_short_sender_rejected.reading_iff_obligation : Spec.ledger_rules.n2_short_sender_rejected.reading ↔ Spec.ledger_rules.n2_short_sender_rejected.obligation  (generated script; the audit checked its type and that its proof uses no proof of either side); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger_rules.n2_short_sender_rejected.reading_sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     reading compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 21 Clausebook pieces; echoed above for comparison with the scenario
  new sentence     no entry of the old whole-phrase glossary is involved: no flat statement of that kind, no hand-written step, no hand-written Rust predicate
  NOT ASSERTED     0 of 21 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, more_than, l.amount_of, l.bal_of, l.sender, never, never_changes, always, not, l.accepted, calls.every, D1, D2, D3, D4, D8
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs, generic step: the composition tree evaluated by the per-piece Rust readings); 3 of 3 pass on the Lean model; they agree
  tested           the reading on 726 generated inputs (32 in scope) on the Lean model: no counterexample; the definition of each frame and its executable reading agree on 64 of 64 evaluations
  tested           the reading on the COMPILED RUST at the same 726 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 2178 of 2178 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, more_than, l.amount_of, l.bal_of, l.sender, never, never_changes, always, not, l.accepted, calls.every, D1, D2, D3, D4, D8`:

```lean
def Spec.ledger_rules.n2_short_sender_rejected.reading : Prop :=
  ∀ (balances : List U64),
    Frames.Never ((L.apply).given (fun st inp => (L.balances st) = balances ∧ (L.bal st (L.sender inp)) < (L.amountOf inp))) (fun ans => L.said ans) ∧
    Frames.NeverChanges ((L.apply).given (fun st inp => (L.balances st) = balances ∧ (L.bal st (L.sender inp)) < (L.amountOf inp))) (fun st inp => L.balances st)
```

Flat proof obligation, generated from the pieces (`lean/Wallet/Obligations.lean`); a NEW sentence has no flat statement in the old glossary:

```lean
def Spec.ledger_rules.n2_short_sender_rejected.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ((L.bal st (L.sender inp)) < (L.amountOf inp)) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (¬ ((L.said ans))) ∧ ((L.balances st') = (L.balances st)))
```

Supplied proof of the obligation (`lean/Wallet/Proofs/ledger_rules/n2_short_sender_rejected.lean`):

```lean
theorem Spec.ledger_rules.n2_short_sender_rejected : Spec.ledger_rules.n2_short_sender_rejected.obligation := by
  intro balances st inp _ hlt
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, ?_⟩
  rcases h with ⟨-, hv, -⟩ | ⟨rfl, -, rfl, -⟩
  · exfalso
    have hc : inp.amount.val ≤ LVocab.bal st inp.from.val := hv.2.2.2.1
    have hlt' : LVocab.bal st inp.from.val < inp.amount.val := hlt
    omega
  · exact ⟨by simp, rfl⟩
```

</details>

### Rule: For a lookup for which the account is not an account of the ledger, there is no result

```text
Rule: For a lookup for which the account is not an account of the ledger, there is no result   [features/ledger_rules.feature:49]   tags @id:n3_lookup_missing_account
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; assuming the account is NOT an account number of the ledger; then the call gives
            an answer [default D1]; the call returns no value
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 55 generated inputs on the compiled Rust: the same result as on the Lean model at
            110 of 110 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (24130 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.n3_lookup_missing_account.proved,
                     Rule.ledger_rules.n3_lookup_missing_account,
                     Rule.ledger_rules.n3_lookup_missing_account.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      16 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, given: modifier, unsigned, never: frame, unsigned, not: modifier,
                 unsigned, l.is_account: domain, unsigned, always: frame, unsigned, l.found: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_for: grammar, unsigned,
                 g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned,
                 D4: default, unsigned, D8: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.n3_lookup_missing_account.proved, Rule.ledger_rules.n3_lookup_missing_account,
                 Rule.ledger_rules.n3_lookup_missing_account.reading_iff_obligation)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 55 generated inputs of the rule statement (110 of 110 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
            assuming    the account is NOT an account number of the ledger
            then        the call gives an answer [default D1]
                        the call returns no value
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.n3_lookup_missing_account.proved :
                             Rule.ledger_rules.n3_lookup_missing_account.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.n3_lookup_missing_account :
                             Rule.ledger_rules.n3_lookup_missing_account.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/n3_lookup_missing_account.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.n3_lookup_missing_account.reading_iff_obligation :
                             Rule.ledger_rules.n3_lookup_missing_account.reading ↔
                             Rule.ledger_rules.n3_lookup_missing_account.obligation  (generated script; the audit
                             checked its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 55 generated inputs (31 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 31 of 31 evaluations
            tested           the reading on the COMPILED RUST at the same 55 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             110 of 110 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 16 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.n3_lookup_missing_account.reading : Prop :=
  Frames.Never ((L.lookup).given (fun st inp => ¬ ((L.isAccount st inp)))) (fun ans => L.found ans)
```

</details>

### Rule: A batch never leaves the total of all balances of the ledger above the maximum

```text
Rule: A batch never leaves the total of all balances of the ledger above the maximum   [features/ledger_rules.feature:52]   tags @id:n4_total_stays_within_maximum @expect-refuted
  Deliberately false: a batch conserves the total, and the total of a ledger can exceed the maximum to begin with.
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the sum of the balances of every
            account of the ledger after the call is at most the largest total that can be reported (2^64 - 1)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[18446744073709551615, 1]", "the_batch": "[]"},
            on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  FALSE at an input found at generated input 2 and shrunk: {"the_batch": "[]", "the_ledger":
                     "[18446744073709551615, 1]"} (seed 20261111); of the 1 scenario beneath it, 0 not falsified, 1
                     shown false
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 1 transfer (the rule's assertion; input {"the_batch":
                     "[1->0:4611686018427387909]", "the_ledger": "[18446744073709551610, 13835058055282163717]"}; on
                     the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.n4_total_stays_within_maximum.refuted (the
                     negation of the rule statement) at {"the_ledger": "[18446744073709551615, 1]", "the_batch":
                     "[]"}; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[]", "the_ledger": "[18446744073709551615, 1]"}   source: generated property test
                     (case 2 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model
                     the reading fails
    found false at   {"the_batch": "[1->0:4611686018427387909]", "the_ledger": "[18446744073709551610,
                     13835058055282163717]"}   source: generated bounded check (Kani at up to 2 accounts and up to 1
                     transfer; replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the
                     compiled Rust it fails; on the Lean model the reading fails
    found false at   [after a batch the total of all balances is within the maximum] {"balances":
                     "[18446744073709551615, 1]", "batch": "[]", "main_state": "[18446744073709551615, 1]"}   source:
                     generated property test (case 4 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it
                     fails; on the Lean model the reading fails
    found false at   [after a batch the total of all balances is within the maximum] {"balances": "[4,
                     18446744073709551615]", "batch": "[]", "main_state": "[4, 18446744073709551615]"}   source:
                     generated bounded check (Kani at up to 2 accounts and up to 1 transfer; replayed on the compiled
                     Rust through the generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the
                     Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios
              of this group are NEW sentences that have none

  Rests on
    meaning      19 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, at_most: frame, unsigned, aggregate: modifier, unsigned,
                 l.balances_of: domain, unsigned, l.maximum: domain, unsigned, calls.every: coverage, unsigned,
                 g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, given:
                 modifier, unsigned, i.holds: idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned,
                 balances_value: modifier, unsigned, D8: default, unsigned)
                 1 scenario beneath the rule is a NEW sentence: read by the Clausebook alone, no entry of the old
                 glossary
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input, 1 refutation (the
                 scenario is false); axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.n4_total_stays_within_maximum.refuted,
                 Spec.ledger_rules.n4_total_within_maximum_after_batch.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 297 generated inputs of the rule statement (594 of 594 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the sum of the balances of every account of the ledger after the call is at most the largest total
                        that can be reported (2^64 - 1)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.n4_total_stays_within_maximum.refuted : ¬
                             Rule.ledger_rules.n4_total_stays_within_maximum.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [18446744073709551615, 1], batch = []
                             at this input the rule does not hold: NOT "the sum of the balances of every account of the
                             ledger after the call is at most the largest total that can be reported (2^64 - 1)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (297 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios A SCENARIO IS SHOWN FALSE: 0 of 1 universal scenarios proved for all inputs
            REFUTED         after a batch the total of all balances is within the maximum   (expected REFUTED)   [beneath the rule; not used to prove it]   [NEW sentence]
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.n4_total_stays_within_maximum.reading : Prop :=
  Frames.AtMost L.applyBatch (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => L.maximum)
```

</details>

#### REFUTED: after a batch the total of all balances is within the maximum

`features/ledger_rules.feature:56`  id `Spec.ledger_rules.n4_total_within_maximum_after_batch`  tags `@expect-refuted @id:n4_total_within_maximum_after_batch`

```gherkin
Scenario Outline: after a batch the total of all balances is within the maximum
  Given ledger Main holds the balances <balances>
  When the batch <batch> is applied to ledger Main
  Then the total of ledger Main's balances is afterwards at most the maximum

  Examples:
    | balances      | batch      |
    | [100, 20, 0]  | [0->1:30]  |
    | [5, 5]        | []         |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the batch <batch> to ledger Main, transfer by transfer: every ledger Main, and every batch <batch>
            (a list of transfers, in order); for every value of balances (a list of u64 balances, account 0 first)
covers      every such call, accepted or rejected [default D2]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            the sum of the balances of every account of ledger Main after the call is at most the largest total that can
            be reported (2^64 - 1)
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
REFUTED  after a batch the total of all balances is within the maximum
  kernel-checked   theorem Spec.ledger_rules.n4_total_within_maximum_after_batch.refuted : ¬ Spec.ledger_rules.n4_total_within_maximum_after_batch.reading; axioms propext, Classical.choice, Quot.sound
  counterexample   balances = [18446744073709551615, 1], main = [18446744073709551615, 1], batch = []
                   at this input the reading does not hold: NOT "the sum of the balances of every account of ledger Main after the call is at most the largest total that can be reported (2^64 - 1)"
  tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     reading compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 15 Clausebook pieces; echoed above for comparison with the scenario
  new sentence     no entry of the old whole-phrase glossary is involved: no flat statement of that kind, no hand-written step, no hand-written Rust predicate
  NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply_batch, given, i.holds, is, l.ledger, balances_value, at_most, aggregate, l.balances_of, l.maximum, calls.every, D1, D2, D4, D8
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs, generic step: the composition tree evaluated by the per-piece Rust readings); 2 of 2 pass on the Lean model; they agree
  tested           the reading on 3267 generated inputs (297 in scope) on the Lean model: counterexample found; the definition of each frame and its executable reading agree on 297 of 297 evaluations
  tested           the reading on the COMPILED RUST at the same 3267 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 6534 of 6534 evaluations
  note             every Examples row passes; the examples alone would not have caught this
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply_batch, given, i.holds, is, l.ledger, balances_value, at_most, aggregate, l.balances_of, l.maximum, calls.every, D1, D2, D4, D8`:

```lean
def Spec.ledger_rules.n4_total_within_maximum_after_batch.reading : Prop :=
  ∀ (balances : List U64),
    Frames.AtMost ((L.applyBatch).given (fun st inp => (L.balances st) = balances)) (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => L.maximum)
```

Flat proof obligation, generated from the pieces (`lean/Wallet/Obligations.lean`); a NEW sentence has no flat statement in the old glossary:

```lean
def Spec.ledger_rules.n4_total_within_maximum_after_batch.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : Slice ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) ≤ L.maximum))
```

</details>

### Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards

```text
Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards   [features/ledger_rules.feature:67]   tags @id:n5_stopped_at_invalid
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; every transfer of the batch at the
            position the reported count points to (none if every transfer was applied) can NOT be carried out
            exactly on the ledger (an account does not exist, or both are the same, or the sender does not cover the
            amount, or the receiver's balance would pass 2^64 - 1), judged on the state after the call
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.n5_stopped_at_invalid.proved, Rule.ledger_rules.n5_stopped_at_invalid,
                     Rule.ledger_rules.n5_stopped_at_invalid.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      16 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, every_of: frame, unsigned, l.stopped_at: domain, unsigned, not:
                 modifier, unsigned, l.valid: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1:
                 default, unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned, D7: default,
                 unsigned, D9: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.n5_stopped_at_invalid.proved, Rule.ledger_rules.n5_stopped_at_invalid,
                 Rule.ledger_rules.n5_stopped_at_invalid.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        every transfer of the batch at the position the reported count points to (none if every transfer
                        was applied) can NOT be carried out exactly on the ledger (an account does not exist, or both are
                        the same, or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1),
                        judged on the state after the call
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D7 items are judged afterwards: in a Then about a collection read off the answer, each item is
                        judged on the state after the call
                        D9 negation binds to the one condition it is written on: 'every X is not P' means that no X is P,
                        never 'not every X is P'
            kernel-checked   theorem Rule.ledger_rules.n5_stopped_at_invalid.proved :
                             Rule.ledger_rules.n5_stopped_at_invalid.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.n5_stopped_at_invalid :
                             Rule.ledger_rules.n5_stopped_at_invalid.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/n5_stopped_at_invalid.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.n5_stopped_at_invalid.reading_iff_obligation :
                             Rule.ledger_rules.n5_stopped_at_invalid.reading ↔
                             Rule.ledger_rules.n5_stopped_at_invalid.obligation  (generated script; the audit checked
                             its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 16 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 16 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.n5_stopped_at_invalid.reading : Prop :=
  Frames.EveryOf L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp x => ¬ ((L.valid st x)))
```

</details>

### Rule: A transfer never loses acceptance when the amount is smaller

```text
Rule: A transfer never loses acceptance when the amount is smaller   [features/ledger_rules.feature:72]   tags @id:mono_smaller_amount
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; whenever the second call is on the same ledger, with the same sender and receiver, and its amount
            is at most the first call's, and for the first call the answer is an acceptance (see `accepted`), then
            for the second call too the answer is an acceptance (see `accepted`); (TWO calls are compared: every
            pair of calls of the operation related as stated; both must be in scope and both must give an answer
            [default D10])
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 4356 generated inputs on the compiled Rust: the same result as on the Lean model
            at 13068 of 13068 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (40103 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.mono_smaller_amount.proved, Rule.ledger_rules.mono_smaller_amount,
                     Rule.ledger_rules.mono_smaller_amount.reading_iff_obligation: the rule statement for all inputs
                     and all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, monotone: frame, unsigned, l.smaller_amount: domain, unsigned, accepted:
                 modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp:
                 grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4:
                 default, unsigned, D10: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.mono_smaller_amount.proved, Rule.ledger_rules.mono_smaller_amount,
                 Rule.ledger_rules.mono_smaller_amount.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4356 generated inputs of the rule statement (13068 of 13068 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call is on the same ledger, with the same sender and receiver, and its amount
                        is at most the first call's, and for the first call the answer is an acceptance (see `accepted`),
                        then for the second call too the answer is an acceptance (see `accepted`)
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.mono_smaller_amount.proved :
                             Rule.ledger_rules.mono_smaller_amount.reading  (THE RULE STATEMENT ITSELF, as one theorem:
                             the supplied proof of its flat obligation carried through the equivalence; type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.mono_smaller_amount :
                             Rule.ledger_rules.mono_smaller_amount.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/mono_smaller_amount.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.mono_smaller_amount.reading_iff_obligation :
                             Rule.ledger_rules.mono_smaller_amount.reading ↔
                             Rule.ledger_rules.mono_smaller_amount.obligation  (generated script; the audit checked its
                             type and that its proof uses no proof of either side); axioms propext, Classical.choice,
                             Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 4356 generated inputs (88 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 88 of 88 evaluations
            tested           the reading on the COMPILED RUST at the same 4356 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 13068 of 13068 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.mono_smaller_amount.reading : Prop :=
  Frames.Monotone L.apply L.smallerAmount (fun ans => (L.apply).accepted ans)
```

</details>

### Rule: A transfer never loses acceptance when the amount is larger

```text
Rule: A transfer never loses acceptance when the amount is larger   [features/ledger_rules.feature:75]   tags @id:mono_larger_amount @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; whenever the second call is on the same ledger, with the same sender and receiver, and its amount
            is at least the first call's, and for the first call the answer is an acceptance (see `accepted`), then
            for the second call too the answer is an acceptance (see `accepted`); (TWO calls are compared: every
            pair of calls of the operation related as stated; both must be in scope and both must give an answer
            [default D10])
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 4356 generated inputs on the compiled Rust: the same result as on the Lean model
            at 13068 of 13068 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1",
            "the_ledger_2": "[1, 0]", "the_transfer_2": "0->1:2"}, on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 8 and shrunk: {"the_ledger": "[0, 0, 1, 0]",
                     "the_ledger_2": "[0, 0, 1, 0]", "the_transfer": "2->3:0", "the_transfer_2": "2->3:2"} (seed
                     20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[9223372036854775808,
                     9223372036854775808]", "the_ledger_2": "[9223372036854775808, 9223372036854775808]",
                     "the_transfer": "0->1:1", "the_transfer_2": "0->1:9223372036854775808"}; on the compiled Rust it
                     fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.mono_larger_amount.refuted2 (the negation of
                     the rule statement) at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1", "the_ledger_2": "[1,
                     0]", "the_transfer_2": "0->1:2"}; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[0, 0, 1, 0]", "the_ledger_2": "[0, 0, 1, 0]", "the_transfer": "2->3:0",
                     "the_transfer_2": "2->3:2"}   source: generated property test (case 8 of the run, shrunk).
                     COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_ledger": "[9223372036854775808, 9223372036854775808]", "the_ledger_2":
                     "[9223372036854775808, 9223372036854775808]", "the_transfer": "0->1:1", "the_transfer_2":
                     "0->1:9223372036854775808"}   source: generated bounded check (Kani at up to 2 accounts;
                     replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the compiled
                     Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, monotone: frame, unsigned, l.larger_amount: domain, unsigned, accepted:
                 modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp:
                 grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4:
                 default, unsigned, D10: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.mono_larger_amount.refuted2)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4356 generated inputs of the rule statement (13068 of 13068 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call is on the same ledger, with the same sender and receiver, and its amount
                        is at least the first call's, and for the first call the answer is an acceptance (see `accepted`),
                        then for the second call too the answer is an acceptance (see `accepted`)
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.mono_larger_amount.refuted2 : ¬
                             Rule.ledger_rules.mono_larger_amount.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   ledger = [1, 0], transfer = 0->1:1, ledger_2 = [1, 0], transfer_2 = 0->1:2   (the names
                             ending in _2 are the SECOND call's)
                             at this input the rule does not hold: NOT "whenever the second call is on the same ledger,
                             with the same sender and receiver, and its amount is at least the first call's, and for the
                             first call the answer is an acceptance (see `accepted`), then for the second call too the
                             answer is an acceptance (see `accepted`)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 4356 generated inputs (88 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 88 of 88 evaluations
            tested           the reading on the COMPILED RUST at the same 4356 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 13068 of 13068 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.mono_larger_amount.reading : Prop :=
  Frames.Monotone L.apply L.largerAmount (fun ans => (L.apply).accepted ans)
```

</details>

### Rule: A lookup never loses that there is a result when the ledger is extended

```text
Rule: A lookup never loses that there is a result when the ledger is extended   [features/ledger_rules.feature:78]   tags @id:mono_extended_ledger @expect-unproved
  True, and deliberately left WITHOUT a proof: its generated proof stub is still `sorry`
  (lean/Wallet/RuleProofs/ledger_rules/mono_extended_ledger.lean), so its verdict is TESTED-ONLY.
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; whenever the second call looks up the
            same account number, on the first ledger with accounts added at its end, and for the first call the call
            returns a value, then for the second call too the call returns a value; (TWO calls are compared: every
            pair of calls of the operation related as stated; both must be in scope and both must give an answer
            [default D10])
  Verdict   TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)   (expected:
            TESTED-ONLY)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 3025 generated inputs on the compiled Rust: the same result as on the Lean model
            at 9075 of 9075 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (33089 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          none: nothing about this rule is kernel-checked
                     rests on: nothing
    STRONGEST HELD   BOUNDED CHECK only: it holds at the sizes where Kani answered (listed above); it is NOT PROVED
                     at any size where Kani gave no answer, nor beyond

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, monotone: frame, unsigned, l.found: domain, unsigned, l.extended:
                 domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar,
                 unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default,
                 unsigned, D10: default, unsigned)
    proof        none: nothing about this rule is kernel-checked; it is TESTED ONLY
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 3025 generated inputs of the rule statement (9075 of 9075 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call looks up the same account number, on the first ledger with accounts added
                        at its end, and for the first call the call returns a value, then for the second call too the call
                        returns a value
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            not proved       proof incomplete (sorry): lean/Wallet/RuleProofs/ledger_rules/mono_extended_ledger.lean is
                             still the generated stub, or part of it is
            obligation       Rule.ledger_rules.mono_extended_ledger.obligation (lean/Wallet/Obligations.lean), generated
                             from the pieces
            not proved       no glue from the scenarios: no universal scenario beneath the rule is about one operation
                             with nothing pinned; no hand-written proof
                             (lean/Wallet/RuleProofs/ledger_rules/mono_extended_ledger.lean)
            tested           searched on 3025 generated inputs (120 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 120 of 120 evaluations
            tested           the reading on the COMPILED RUST at the same 3025 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 9075 of 9075 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.mono_extended_ledger.reading : Prop :=
  Frames.Monotone L.lookup L.extended (fun ans => L.found ans)
```

</details>

### Rule: A lookup agrees with the reference lookup

```text
Rule: A lookup agrees with the reference lookup   [features/ledger_rules.feature:84]   tags @id:agrees_reference_lookup
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the answer and the state after the
            call are exactly what the reference lookup (the balance at that account number if there is one,
            otherwise no value; the ledger left as it was) gives for the state before and the input
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 55 generated inputs on the compiled Rust: the same result as on the Lean model at
            110 of 110 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.agrees_reference_lookup.proved,
                     Rule.ledger_rules.agrees_reference_lookup,
                     Rule.ledger_rules.agrees_reference_lookup.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      10 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, agrees_with: frame, unsigned, l.ref_lookup: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.agrees_reference_lookup.proved, Rule.ledger_rules.agrees_reference_lookup,
                 Rule.ledger_rules.agrees_reference_lookup.reading_iff_obligation)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 55 generated inputs of the rule statement (110 of 110 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer and the state after the call are exactly what the reference lookup (the balance at that
                        account number if there is one, otherwise no value; the ledger left as it was) gives for the state
                        before and the input
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.agrees_reference_lookup.proved :
                             Rule.ledger_rules.agrees_reference_lookup.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.agrees_reference_lookup :
                             Rule.ledger_rules.agrees_reference_lookup.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/agrees_reference_lookup.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.agrees_reference_lookup.reading_iff_obligation :
                             Rule.ledger_rules.agrees_reference_lookup.reading ↔
                             Rule.ledger_rules.agrees_reference_lookup.obligation  (generated script; the audit checked
                             its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 55 generated inputs (55 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 55 of 55 evaluations
            tested           the reading on the COMPILED RUST at the same 55 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             110 of 110 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 10 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 10 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.agrees_reference_lookup.reading : Prop :=
  Frames.AgreesWith L.lookup L.refLookup
```

</details>

### Rule: A lookup agrees with the zero-default lookup

```text
Rule: A lookup agrees with the zero-default lookup   [features/ledger_rules.feature:87]   tags @id:agrees_zero_default @expect-refuted
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the answer and the state after the
            call are exactly what the zero-default lookup (the balance at that account number, and the value 0 if
            there is no such account; the ledger left as it was) gives for the state before and the input
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 55 generated inputs on the compiled Rust: the same result as on the Lean model at
            110 of 110 evaluations; it is FALSE at {"the_ledger": "[]", "the_account": "0"}, on the compiled Rust
            too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_account": "0", "the_ledger":
                     "[]"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_account": "9223372036854775808",
                     "the_ledger": "[0]"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.agrees_zero_default.refuted (the negation of
                     the rule statement) at {"the_ledger": "[]", "the_account": "0"}; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_account": "0", "the_ledger": "[]"}   source: generated property test (case 1 of the run,
                     shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_account": "9223372036854775808", "the_ledger": "[0]"}   source: generated bounded check
                     (Kani at up to 2 accounts; replayed on the compiled Rust through the generated predicate).
                     falsifying input: on the compiled Rust it fails; NOT EVALUATED on the Lean model (an account
                     number above 4294967295 has no literal in the Lean model, which leaves the width of usize open:
                     the_account)
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      10 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, agrees_with: frame, unsigned, l.ref_lookup_zero: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.agrees_zero_default.refuted)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 55 generated inputs of the rule statement (110 of 110 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer and the state after the call are exactly what the zero-default lookup (the balance at
                        that account number, and the value 0 if there is no such account; the ledger left as it was) gives
                        for the state before and the input
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.agrees_zero_default.refuted : ¬
                             Rule.ledger_rules.agrees_zero_default.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   ledger = [], account = 0
                             at this input the rule does not hold: NOT "the answer and the state after the call are
                             exactly what the zero-default lookup (the balance at that account number, and the value 0
                             if there is no such account; the ledger left as it was) gives for the state before and the
                             input"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 55 generated inputs (55 in scope): counterexample found; the definition of each
                             frame and its executable reading agree on 55 of 55 evaluations
            tested           the reading on the COMPILED RUST at the same 55 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             110 of 110 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 10 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 10 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.agrees_zero_default.reading : Prop :=
  Frames.AgreesWith L.lookup L.refLookupZero
```

</details>

### Rule: A lookup gives the same answer when the ledger agrees at the account

```text
Rule: A lookup gives the same answer when the ledger agrees at the account   [features/ledger_rules.feature:91]   tags @id:same_answer_at_account
  Reading   for a lookup: every ledger, every account (an account number, a usize); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; whenever the second call looks up the
            same account number, on a ledger that holds the same there (the same balance, or no such account in
            either), the two calls give the same answer; (TWO calls are compared: every pair of calls of the
            operation related as stated; both must be in scope and both must give an answer [default D10])
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 3025 generated inputs on the compiled Rust: the same result as on the Lean model
            at 9075 of 9075 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (28299 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.same_answer_at_account.proved,
                     Rule.ledger_rules.same_answer_at_account,
                     Rule.ledger_rules.same_answer_at_account.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      11 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.lookup: domain, unsigned, same_answer: frame, unsigned, l.agrees_at_account: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, D10:
                 default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.same_answer_at_account.proved, Rule.ledger_rules.same_answer_at_account,
                 Rule.ledger_rules.same_answer_at_account.reading_iff_obligation)
    translation  Lean model ledger.Ledger.balance generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 3025 generated inputs of the rule statement (9075 of 9075 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a lookup: every ledger, every account (an account number, a usize)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call looks up the same account number, on a ledger that holds the same there
                        (the same balance, or no such account in either), the two calls give the same answer
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.same_answer_at_account.proved :
                             Rule.ledger_rules.same_answer_at_account.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.same_answer_at_account :
                             Rule.ledger_rules.same_answer_at_account.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/same_answer_at_account.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.same_answer_at_account.reading_iff_obligation :
                             Rule.ledger_rules.same_answer_at_account.reading ↔
                             Rule.ledger_rules.same_answer_at_account.obligation  (generated script; the audit checked
                             its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 3025 generated inputs (327 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 327 of 327 evaluations
            tested           the reading on the COMPILED RUST at the same 3025 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 9075 of 9075 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 11 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 11 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.same_answer_at_account.reading : Prop :=
  Frames.IndependentOf L.lookup L.agreesAtAccount (fun ans _ => ans)
```

</details>

### Rule: A transfer gives the same answer when only the amount differs

```text
Rule: A transfer gives the same answer when only the amount differs   [features/ledger_rules.feature:94]   tags @id:same_answer_any_amount @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; whenever the second call is on the same ledger, with the same sender and receiver (the two amounts
            may be anything), the two calls give the same answer; (TWO calls are compared: every pair of calls of
            the operation related as stated; both must be in scope and both must give an answer [default D10])
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 4356 generated inputs on the compiled Rust: the same result as on the Lean model
            at 13068 of 13068 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1",
            "the_ledger_2": "[1, 0]", "the_transfer_2": "0->1:2"}, on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 29 and shrunk: {"the_ledger": "[1,
                     18446744073709551615, 0, 0]", "the_ledger_2": "[1, 18446744073709551615, 0, 0]", "the_transfer":
                     "0->1:0", "the_transfer_2": "0->1:1"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[18446744073709551615,
                     1]", "the_ledger_2": "[18446744073709551615, 1]", "the_transfer": "0->1:18446744073709551615",
                     "the_transfer_2": "0->1:18446744073709551614"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.same_answer_any_amount.refuted2 (the negation
                     of the rule statement) at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1", "the_ledger_2":
                     "[1, 0]", "the_transfer_2": "0->1:2"}; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[1, 18446744073709551615, 0, 0]", "the_ledger_2": "[1, 18446744073709551615, 0,
                     0]", "the_transfer": "0->1:0", "the_transfer_2": "0->1:1"}   source: generated property test
                     (case 29 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model
                     the reading fails
    found false at   {"the_ledger": "[18446744073709551615, 1]", "the_ledger_2": "[18446744073709551615, 1]",
                     "the_transfer": "0->1:18446744073709551615", "the_transfer_2": "0->1:18446744073709551614"}
                     source: generated bounded check (Kani at up to 2 accounts; replayed on the compiled Rust through
                     the generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the
                     reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      11 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, same_answer: frame, unsigned, l.only_amount_differs: domain, unsigned,
                 calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, D10:
                 default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.same_answer_any_amount.refuted2)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4356 generated inputs of the rule statement (13068 of 13068 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call is on the same ledger, with the same sender and receiver (the two amounts
                        may be anything), the two calls give the same answer
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.same_answer_any_amount.refuted2 : ¬
                             Rule.ledger_rules.same_answer_any_amount.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [1, 0], transfer = 0->1:1, ledger_2 = [1, 0], transfer_2 = 0->1:2   (the names
                             ending in _2 are the SECOND call's)
                             at this input the rule does not hold: NOT "whenever the second call is on the same ledger,
                             with the same sender and receiver (the two amounts may be anything), the two calls give the
                             same answer"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 4356 generated inputs (110 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 110 of 110 evaluations
            tested           the reading on the COMPILED RUST at the same 4356 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 13068 of 13068 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 11 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 11 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.same_answer_any_amount.reading : Prop :=
  Frames.IndependentOf L.apply L.onlyAmountDiffers (fun ans _ => ans)
```

</details>

### Rule: A transfer gives the same answer when the amount is larger, if it is rejected

```text
Rule: A transfer gives the same answer when the amount is larger, if it is rejected   [features/ledger_rules.feature:98]   tags @id:rejected_stays_rejected
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; whenever the second call is on the same ledger, with the same sender and receiver, and its amount
            is at least the first call's, and for the first call the answer is no (rejected), the two calls give the
            same answer; (TWO calls are compared: every pair of calls of the operation related as stated; both must
            be in scope and both must give an answer [default D10])
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 4356 generated inputs on the compiled Rust: the same result as on the Lean model
            at 13068 of 13068 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (39070 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.rejected_stays_rejected.proved,
                     Rule.ledger_rules.rejected_stays_rejected,
                     Rule.ledger_rules.rejected_stays_rejected.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      13 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, same_answer_if: frame, unsigned, l.larger_amount: domain, unsigned, not:
                 modifier, unsigned, l.accepted: domain, unsigned, calls.every: coverage, unsigned, g.subject:
                 grammar, unsigned, g.rule_vp: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned,
                 D2: default, unsigned, D4: default, unsigned, D10: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.rejected_stays_rejected.proved, Rule.ledger_rules.rejected_stays_rejected,
                 Rule.ledger_rules.rejected_stays_rejected.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4356 generated inputs of the rule statement (13068 of 13068 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call is on the same ledger, with the same sender and receiver, and its amount
                        is at least the first call's, and for the first call the answer is no (rejected), the two calls
                        give the same answer
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.rejected_stays_rejected.proved :
                             Rule.ledger_rules.rejected_stays_rejected.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.rejected_stays_rejected :
                             Rule.ledger_rules.rejected_stays_rejected.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/rejected_stays_rejected.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.rejected_stays_rejected.reading_iff_obligation :
                             Rule.ledger_rules.rejected_stays_rejected.reading ↔
                             Rule.ledger_rules.rejected_stays_rejected.obligation  (generated script; the audit checked
                             its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 4356 generated inputs (88 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 88 of 88 evaluations
            tested           the reading on the COMPILED RUST at the same 4356 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 13068 of 13068 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.rejected_stays_rejected.reading : Prop :=
  Frames.IndependentGiven L.apply L.largerAmount (fun ans => ¬ ((L.said ans))) (fun ans _ => ans)
```

</details>

### Rule: A transfer gives the same answer when the amount is larger, if it is accepted

```text
Rule: A transfer gives the same answer when the amount is larger, if it is accepted   [features/ledger_rules.feature:101]   tags @id:accepted_stays_accepted @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; whenever the second call is on the same ledger, with the same sender and receiver, and its amount
            is at least the first call's, and for the first call the answer is yes (accepted), the two calls give
            the same answer; (TWO calls are compared: every pair of calls of the operation related as stated; both
            must be in scope and both must give an answer [default D10])
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 4356 generated inputs on the compiled Rust: the same result as on the Lean model
            at 13068 of 13068 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1",
            "the_ledger_2": "[1, 0]", "the_transfer_2": "0->1:2"}, on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 397 and shrunk: {"the_ledger": "[0,
                     13808191158069793772, 0, 2319276457819878922]", "the_ledger_2": "[0, 13808191158069793772, 0,
                     2319276457819878922]", "the_transfer": "3->0:0", "the_transfer_2": "3->0:2319276457819878923"}
                     (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[9223372036854775808,
                     9223372036854775808]", "the_ledger_2": "[9223372036854775808, 9223372036854775808]",
                     "the_transfer": "0->1:1", "the_transfer_2": "0->1:9223372036854775808"}; on the compiled Rust it
                     fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.accepted_stays_accepted.refuted2 (the negation
                     of the rule statement) at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1", "the_ledger_2":
                     "[1, 0]", "the_transfer_2": "0->1:2"}; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[0, 13808191158069793772, 0, 2319276457819878922]", "the_ledger_2": "[0,
                     13808191158069793772, 0, 2319276457819878922]", "the_transfer": "3->0:0", "the_transfer_2":
                     "3->0:2319276457819878923"}   source: generated property test (case 397 of the run, shrunk).
                     COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_ledger": "[9223372036854775808, 9223372036854775808]", "the_ledger_2":
                     "[9223372036854775808, 9223372036854775808]", "the_transfer": "0->1:1", "the_transfer_2":
                     "0->1:9223372036854775808"}   source: generated bounded check (Kani at up to 2 accounts;
                     replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the compiled
                     Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, same_answer_if: frame, unsigned, l.larger_amount: domain, unsigned,
                 l.accepted: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_vp: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default,
                 unsigned, D4: default, unsigned, D10: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.accepted_stays_accepted.refuted2)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 4356 generated inputs of the rule statement (13068 of 13068 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        whenever the second call is on the same ledger, with the same sender and receiver, and its amount
                        is at least the first call's, and for the first call the answer is yes (accepted), the two calls
                        give the same answer
                        (TWO calls are compared: every pair of calls of the operation related as stated; both must be in
                        scope and both must give an answer [default D10])
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D10 two calls are compared: the claim is about every pair of calls of the operation related as
                        stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and
                        both must give an answer
            kernel-checked   theorem Rule.ledger_rules.accepted_stays_accepted.refuted2 : ¬
                             Rule.ledger_rules.accepted_stays_accepted.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [1, 0], transfer = 0->1:1, ledger_2 = [1, 0], transfer_2 = 0->1:2   (the names
                             ending in _2 are the SECOND call's)
                             at this input the rule does not hold: NOT "whenever the second call is on the same ledger,
                             with the same sender and receiver, and its amount is at least the first call's, and for the
                             first call the answer is yes (accepted), the two calls give the same answer"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 4356 generated inputs (88 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 88 of 88 evaluations
            tested           the reading on the COMPILED RUST at the same 4356 generated inputs, through the Rust
                             reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean
                             model on 13068 of 13068 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.accepted_stays_accepted.reading : Prop :=
  Frames.IndependentGiven L.apply L.largerAmount (fun ans => L.said ans) (fun ans _ => ans)
```

</details>

### Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch

```text
Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch   [features/ledger_rules.feature:105]   tags @id:stopped_is_of_batch
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; every transfer of the batch at the
            position the reported count points to (none if every transfer was applied) is a transfer of the batch
            (the first is read off the answer, the second off the input before the call)
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.stopped_is_of_batch.proved, Rule.ledger_rules.stopped_is_of_batch,
                     Rule.ledger_rules.stopped_is_of_batch.reading_iff_obligation: the rule statement for all inputs
                     and all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      13 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, within: frame, unsigned, l.stopped_at: domain, unsigned,
                 l.transfers: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.stopped_is_of_batch.proved, Rule.ledger_rules.stopped_is_of_batch,
                 Rule.ledger_rules.stopped_is_of_batch.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        every transfer of the batch at the position the reported count points to (none if every transfer
                        was applied) is a transfer of the batch (the first is read off the answer, the second off the
                        input before the call)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
            kernel-checked   theorem Rule.ledger_rules.stopped_is_of_batch.proved :
                             Rule.ledger_rules.stopped_is_of_batch.reading  (THE RULE STATEMENT ITSELF, as one theorem:
                             the supplied proof of its flat obligation carried through the equivalence; type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.stopped_is_of_batch :
                             Rule.ledger_rules.stopped_is_of_batch.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/stopped_is_of_batch.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.stopped_is_of_batch.reading_iff_obligation :
                             Rule.ledger_rules.stopped_is_of_batch.reading ↔
                             Rule.ledger_rules.stopped_is_of_batch.obligation  (generated script; the audit checked its
                             type and that its proof uses no proof of either side); axioms propext, Classical.choice,
                             Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.stopped_is_of_batch.reading : Prop :=
  Frames.Within L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp => L.transfers inp)
```

</details>

### Rule: For a batch, every transfer of the batch is a transfer at which the batch stopped

```text
Rule: For a batch, every transfer of the batch is a transfer at which the batch stopped   [features/ledger_rules.feature:108]   tags @id:batch_is_stopped @expect-refuted
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; every transfer of the batch is a
            transfer of the batch at the position the reported count points to (none if every transfer was applied)
            (the first is read off the input before the call, the second off the answer)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[]", "the_batch": "[0->1:1, 1->0:1]"}, on the
            compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_batch": "[0->0:0, 0->0:1]",
                     "the_ledger": "[]"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 1 transfer (the rule's assertion; input {"the_batch":
                     "[0->1:9223372036854775807]", "the_ledger": "[18446744073709551614, 9223372036854775808]"}; on
                     the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.batch_is_stopped.refuted (the negation of the
                     rule statement) at {"the_ledger": "[]", "the_batch": "[0->1:1, 1->0:1]"}; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[0->0:0, 0->0:1]", "the_ledger": "[]"}   source: generated property test (case 1
                     of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the
                     reading fails
    found false at   {"the_batch": "[0->1:9223372036854775807]", "the_ledger": "[18446744073709551614,
                     9223372036854775808]"}   source: generated bounded check (Kani at up to 2 accounts and up to 1
                     transfer; replayed on the compiled Rust through the generated predicate). COUNTEREXAMPLE: on the
                     compiled Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      13 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, covers: frame, unsigned, l.transfers: domain, unsigned,
                 l.stopped_at: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.batch_is_stopped.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        every transfer of the batch is a transfer of the batch at the position the reported count points
                        to (none if every transfer was applied) (the first is read off the input before the call, the
                        second off the answer)
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
            kernel-checked   theorem Rule.ledger_rules.batch_is_stopped.refuted : ¬
                             Rule.ledger_rules.batch_is_stopped.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   ledger = [], batch = [0->1:1, 1->0:1]
                             at this input the rule does not hold: NOT "every transfer of the batch is a transfer of the
                             batch at the position the reported count points to (none if every transfer was applied)
                             (the first is read off the input before the call, the second off the answer)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (297 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.batch_is_stopped.reading : Prop :=
  Frames.Covers L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp => L.transfers inp)
```

</details>

### Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger

```text
Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger   [features/ledger_rules.feature:112]   tags @id:some_valid_conserves
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; assuming at least one transfer of the batch can be carried out exactly on the
            ledger (both accounts exist and differ, the sender covers the amount, the receiver's balance stays
            within 2^64 - 1); then the call gives an answer [default D1]; the sum of the balances of every account
            of the ledger after the call equals the sum of the balances of every account of the ledger before it
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (50722 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 2 accounts and up to 3 transfers; NO ANSWER in 30 s with up to 4
                     accounts and up to 1 transfer; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.some_valid_conserves.proved, Rule.ledger_rules.some_valid_conserves,
                     Rule.ledger_rules.some_valid_conserves.reading_iff_obligation: the rule statement for all inputs
                     and all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      19 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, given: modifier, unsigned, never_changes: frame, unsigned,
                 some_of: modifier, unsigned, l.transfers: domain, unsigned, l.valid: domain, unsigned, aggregate:
                 modifier, unsigned, l.balances_of: domain, unsigned, calls.every: coverage, unsigned, g.subject:
                 grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar,
                 unsigned, D1: default, unsigned, D2: default, unsigned, D3: default, unsigned, D4: default,
                 unsigned, D5: default, unsigned, D8: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.some_valid_conserves.proved, Rule.ledger_rules.some_valid_conserves,
                 Rule.ledger_rules.some_valid_conserves.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    at least one transfer of the batch can be carried out exactly on the ledger (both accounts exist
                        and differ, the sender covers the amount, the receiver's balance stays within 2^64 - 1)
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
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.some_valid_conserves.proved :
                             Rule.ledger_rules.some_valid_conserves.reading  (THE RULE STATEMENT ITSELF, as one theorem:
                             the supplied proof of its flat obligation carried through the equivalence; type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.some_valid_conserves :
                             Rule.ledger_rules.some_valid_conserves.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/some_valid_conserves.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.some_valid_conserves.reading_iff_obligation :
                             Rule.ledger_rules.some_valid_conserves.reading ↔
                             Rule.ledger_rules.some_valid_conserves.obligation  (generated script; the audit checked its
                             type and that its proof uses no proof of either side); axioms propext, Classical.choice,
                             Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (130 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 130 of 130 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 19 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 19 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.some_valid_conserves.reading : Prop :=
  Frames.NeverChanges ((L.applyBatch).given (fun st inp => Frames.someOf ((L.transfers inp)) (fun x => (L.valid st x)))) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

### Rule: A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected

```text
Rule: A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected   [features/ledger_rules.feature:115]   tags @id:some_invalid_rejected @expect-refuted
  Deliberately false, and it sounds right: a transfer that cannot be carried out on the ledger as it starts
  can become possible after an earlier transfer of the same batch.
  Reading   for a batch applied as a whole: every ledger, every batch (a list of transfers, in order); every such
            call, accepted or rejected [default D2]; assuming at least one transfer of the batch can NOT be carried
            out exactly on the ledger (an account does not exist, or both are the same, or the sender does not cover
            the amount, or the receiver's balance would pass 2^64 - 1); then the call gives an answer [default D1];
            it is NOT the case that the answer is an acceptance (see `accepted`)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_batch": "[0->1:1, 1->0:1]"}, on the
            compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1857 and shrunk: {"the_batch": "[0->1:1, 1->0:1]",
                     "the_ledger": "[1, 0]"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 2 transfers (the rule's assertion; input {"the_batch":
                     "[0->1:24206847997116417, 1->0:6485746413366935563]", "the_ledger": "[444730463202836485,
                     6462665465276661766]"}; on the compiled Rust it fails); holds for every input with up to 2
                     accounts and up to 1 transfer; with up to 4 accounts and up to 1 transfer
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.some_invalid_rejected.refuted2 (the negation of
                     the rule statement) at {"the_ledger": "[1, 0]", "the_batch": "[0->1:1, 1->0:1]"}; axioms:
                     propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[0->1:1, 1->0:1]", "the_ledger": "[1, 0]"}   source: generated property test
                     (case 1857 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model
                     the reading fails
    found false at   {"the_batch": "[0->1:24206847997116417, 1->0:6485746413366935563]", "the_ledger":
                     "[444730463202836485, 6462665465276661766]"}   source: generated bounded check (Kani at up to 2
                     accounts and up to 2 transfers; replayed on the compiled Rust through the generated predicate).
                     COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      18 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_all: domain, unsigned, given: modifier, unsigned, never: frame, unsigned, some_of:
                 modifier, unsigned, l.transfers: domain, unsigned, not: modifier, unsigned, l.valid: domain,
                 unsigned, accepted: modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1:
                 default, unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned, D8: default,
                 unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.some_invalid_rejected.refuted2)
    translation  Lean model ledger.Ledger.apply_all generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch applied as a whole: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    at least one transfer of the batch can NOT be carried out exactly on the ledger (an account does
                        not exist, or both are the same, or the sender does not cover the amount, or the receiver's
                        balance would pass 2^64 - 1)
            then        the call gives an answer [default D1]
                        it is NOT the case that the answer is an acceptance (see `accepted`)
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.some_invalid_rejected.refuted2 : ¬
                             Rule.ledger_rules.some_invalid_rejected.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [1, 0], batch = [0->1:1, 1->0:1]
                             at this input the rule does not hold: NOT "it is NOT the case that the answer is an
                             acceptance (see `accepted`)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (234 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 234 of 234 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 18 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.some_invalid_rejected.reading : Prop :=
  Frames.Never ((L.applyAll).given (fun st inp => Frames.someOf ((L.transfers inp)) (fun x => (¬ ((L.valid st x)))))) (fun ans => (L.applyAll).accepted ans)
```

</details>

### Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied

```text
Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied   [features/ledger_rules.feature:123]   tags @id:k2_whole_agrees_with_batch
  Reading   for a batch applied as a whole: every ledger, every batch (a list of transfers, in order); every such
            call, accepted or rejected [default D2]; then the call gives an answer [default D1]; the answer and the
            state after the call are exactly what the same batch applied transfer by transfer (the operation
            `apply_batch` of the same code) and kept only if every transfer is applied (accepted, with the ledger
            that leaves, if it applies every transfer of the batch; otherwise rejected, with the ledger left as it
            was) gives for the state before and the input
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; NO ANSWER in 30 s with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.k2_whole_agrees_with_batch.proved,
                     Rule.ledger_rules.k2_whole_agrees_with_batch,
                     Rule.ledger_rules.k2_whole_agrees_with_batch.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      10 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_all: domain, unsigned, agrees_with: frame, unsigned, l.ref_whole_by_batch: domain,
                 unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar,
                 unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default,
                 unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.k2_whole_agrees_with_batch.proved, Rule.ledger_rules.k2_whole_agrees_with_batch,
                 Rule.ledger_rules.k2_whole_agrees_with_batch.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_all generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch applied as a whole: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer and the state after the call are exactly what the same batch applied transfer by
                        transfer (the operation `apply_batch` of the same code) and kept only if every transfer is applied
                        (accepted, with the ledger that leaves, if it applies every transfer of the batch; otherwise
                        rejected, with the ledger left as it was) gives for the state before and the input
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.k2_whole_agrees_with_batch.proved :
                             Rule.ledger_rules.k2_whole_agrees_with_batch.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.k2_whole_agrees_with_batch :
                             Rule.ledger_rules.k2_whole_agrees_with_batch.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/k2_whole_agrees_with_batch.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.k2_whole_agrees_with_batch.reading_iff_obligation :
                             Rule.ledger_rules.k2_whole_agrees_with_batch.reading ↔
                             Rule.ledger_rules.k2_whole_agrees_with_batch.obligation  (generated script; the audit
                             checked its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 10 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 10 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.k2_whole_agrees_with_batch.reading : Prop :=
  Frames.AgreesWith L.applyAll L.refWholeByBatch
```

</details>

### Rule: A batch agrees with its transfers applied one at a time until one is rejected

```text
Rule: A batch agrees with its transfers applied one at a time until one is rejected   [features/ledger_rules.feature:126]   tags @id:k2_batch_agrees_with_transfers @expect-unproved
  True as far as the property test and the bounded check can tell, and left WITHOUT a proof on purpose: it is the
  rule shown with property-test and bounded evidence only (no proof of its obligation has been supplied).
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the answer and the state after the
            call are exactly what its transfers applied one at a time, in order, until one is rejected (the
            operation `apply` of the same code, once per transfer; the answer is how many were accepted before the
            first rejection, and the ledger is the one those calls leave) gives for the state before and the input
  Verdict   TESTED ONLY (compiled, evaluated on generated inputs, no counterexample; NOT PROVED)   (expected:
            TESTED-ONLY)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; NO ANSWER in 30 s with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          none: nothing about this rule is kernel-checked
                     rests on: nothing
    STRONGEST HELD   BOUNDED CHECK only: it holds at the sizes where Kani answered (listed above); it is NOT PROVED
                     at any size where Kani gave no answer, nor beyond

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      10 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, agrees_with: frame, unsigned, l.ref_batch_by_transfers: domain,
                 unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar,
                 unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default,
                 unsigned)
    proof        none: nothing about this rule is kernel-checked; it is TESTED ONLY
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer and the state after the call are exactly what its transfers applied one at a time, in
                        order, until one is rejected (the operation `apply` of the same code, once per transfer; the
                        answer is how many were accepted before the first rejection, and the ledger is the one those calls
                        leave) gives for the state before and the input
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not proved       no glue from the scenarios: no universal scenario beneath the rule is about one operation
                             with nothing pinned; no hand-written proof
                             (lean/Wallet/RuleProofs/ledger_rules/k2_batch_agrees_with_transfers.lean)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 10 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 10 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.k2_batch_agrees_with_transfers.reading : Prop :=
  Frames.AgreesWith L.applyBatch L.refBatchByTransfers
```

</details>

### Rule: A transfer never leaves the balance of account 4 of the ledger above zero

```text
Rule: A transfer never leaves the balance of account 4 of the ledger above zero   [features/ledger_rules.feature:137]   tags @id:e1_fifth_account_empty @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; the balance, in the ledger, of account 4 (0 if there is no such account) after the call is at most
            0
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; none of them falsifies it (it is FALSE at {"the_ledger": "[0, 0, 0, 0, 1]",
            "the_transfer": "0->0:0"}, an input the generated property test found on the compiled Rust; see
            Evidence)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_ledger": "[0, 0, 0, 0, 1]",
                     "the_transfer": "0->0:0"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 6 accounts (the rule's assertion; input {"the_ledger": "[18446744073709551615,
                     18446744073709551615, 18446744073709551615, 18446744073709551615, 4, 18446744073709551615]",
                     "the_transfer": "0->4:0"}; on the compiled Rust it fails); holds for every input with up to 2
                     accounts; with up to 4 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.e1_fifth_account_empty.refuted (the negation of
                     the rule statement) at {"the_ledger": "[0, 0, 0, 0, 1]", "the_transfer": "0->0:0"}; axioms:
                     propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[0, 0, 0, 0, 1]", "the_transfer": "0->0:0"}   source: generated property test
                     (case 1 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model
                     the reading fails
    found false at   {"the_ledger": "[18446744073709551615, 18446744073709551615, 18446744073709551615,
                     18446744073709551615, 4, 18446744073709551615]", "the_transfer": "0->4:0"}   source: generated
                     bounded check (Kani at up to 6 accounts; replayed on the compiled Rust through the generated
                     predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the generated property
                     test)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      13 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, at_most: frame, unsigned, l.bal_of: domain, unsigned, index_number:
                 modifier, unsigned, zero: modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1:
                 default, unsigned, D2: default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.e1_fifth_account_empty.refuted)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the balance, in the ledger, of account 4 (0 if there is no such account) after the call is at most
                        0
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.e1_fifth_account_empty.refuted : ¬
                             Rule.ledger_rules.e1_fifth_account_empty.reading; axioms propext, Classical.choice,
                             Quot.sound
            source           the input was found on the compiled Rust by the generated property test, then evaluated on
                             the Lean model, where the rule fails too
            counterexample   ledger = [0, 0, 0, 0, 1], transfer = 0->0:0
                             at this input the rule does not hold: NOT "the balance, in the ledger, of account 4 (0 if
                             there is no such account) after the call is at most 0"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 66 generated inputs (66 in scope): no counterexample on the grid (the
                             counterexample came from the generated property test); the definition of each frame and its
                             executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.e1_fifth_account_empty.reading : Prop :=
  Frames.AtMost L.apply (fun st inp => L.bal st (4#usize).val) (fun st inp => 0)
```

</details>

### Rule: A successful transfer never changes the ledger

```text
Rule: A successful transfer never changes the ledger   [features/ledger_rules.feature:141]   tags @id:successful_changes_nothing @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); ONLY accepted calls [asked for]; then the balances of the ledger, account by account after
            the call equals the balances of the ledger, account by account before it
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1"}, on the
            compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 17 and shrunk: {"the_ledger": "[0, 0, 0,
                     18446744073709551614]", "the_transfer": "3->0:1"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[18446744073709551615,
                     18446744073709551614]", "the_transfer": "0->1:1"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.successful_changes_nothing.refuted2 (the
                     negation of the rule statement) at {"the_ledger": "[1, 0]", "the_transfer": "0->1:1"}; axioms:
                     propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[0, 0, 0, 18446744073709551614]", "the_transfer": "3->0:1"}   source: generated
                     property test (case 17 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on
                     the Lean model the reading fails
    found false at   {"the_ledger": "[18446744073709551615, 18446744073709551614]", "the_transfer": "0->1:1"}
                     source: generated bounded check (Kani at up to 2 accounts; replayed on the compiled Rust through
                     the generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the
                     reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      11 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, successful: modifier, unsigned, never_changes: frame, unsigned,
                 l.ledger: domain, unsigned, calls.accepted: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D3: default,
                 unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.successful_changes_nothing.refuted2)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      ONLY accepted calls [asked for]
            assuming    nothing: every state and every input
            then        the balances of the ledger, account by account after the call equals the balances of the ledger,
                        account by account before it
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
            kernel-checked   theorem Rule.ledger_rules.successful_changes_nothing.refuted2 : ¬
                             Rule.ledger_rules.successful_changes_nothing.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [1, 0], transfer = 0->1:1
                             at this input the rule does not hold: NOT "the balances of the ledger, account by account
                             after the call equals the balances of the ledger, account by account before it"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 66 generated inputs (66 in scope): counterexample found; the definition of each
                             frame and its executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 11 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 11 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.successful_changes_nothing.reading : Prop :=
  Frames.NeverChanges (L.apply).successful (fun st inp => L.balances st)
```

</details>

### Rule: For a rejected transfer, the total of all balances of the ledger is now zero

```text
Rule: For a rejected transfer, the total of all balances of the ledger is now zero   [features/ledger_rules.feature:144]   tags @id:rejected_empties_ledger @expect-refuted
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); ONLY rejected calls [asked for]; then the sum of the balances of every account of the
            ledger after the call is 0
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; it is FALSE at {"the_ledger": "[1, 0]", "the_transfer": "1->0:1"}, on the
            compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_ledger": "[1]", "the_transfer":
                     "0->0:0"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts (the rule's assertion; input {"the_ledger": "[4, 0]",
                     "the_transfer": "0->0:18446744073709551615"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.rejected_empties_ledger.refuted2 (the negation
                     of the rule statement) at {"the_ledger": "[1, 0]", "the_transfer": "1->0:1"}; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_ledger": "[1]", "the_transfer": "0->0:0"}   source: generated property test (case 1 of the
                     run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_ledger": "[4, 0]", "the_transfer": "0->0:18446744073709551615"}   source: generated
                     bounded check (Kani at up to 2 accounts; replayed on the compiled Rust through the generated
                     predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, rejected: modifier, unsigned, becomes: frame, unsigned, aggregate:
                 modifier, unsigned, l.balances_of: domain, unsigned, zero: modifier, unsigned, calls.rejected:
                 coverage, unsigned, g.subject: grammar, unsigned, g.rule_for: grammar, unsigned, g.role: grammar,
                 unsigned, g.line: grammar, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.rejected_empties_ledger.refuted2)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      ONLY rejected calls [asked for]
            assuming    nothing: every state and every input
            then        the sum of the balances of every account of the ledger after the call is 0
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are
                        accepted, or that give no answer, are outside this clause
            kernel-checked   theorem Rule.ledger_rules.rejected_empties_ledger.refuted2 : ¬
                             Rule.ledger_rules.rejected_empties_ledger.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [1, 0], transfer = 1->0:1
                             at this input the rule does not hold: NOT "the sum of the balances of every account of the
                             ledger after the call is 0"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 66 generated inputs (66 in scope): counterexample found; the definition of each
                             frame and its executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.rejected_empties_ledger.reading : Prop :=
  Frames.Becomes (L.apply).rejected (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => 0)
```

</details>

### Rule: A batch followed by a computation of the total is always accepted

```text
Rule: A batch followed by a computation of the total is always accepted   [features/ledger_rules.feature:147]   tags @id:batch_then_total_always @expect-refuted
  Reading   for a batch followed by a computation of the total: every ledger, every batch (a list of transfers, in
            order); every such call, accepted or rejected [default D2]; then the call gives an answer [default D1];
            the answer is an acceptance (see `accepted`); (of a sequence: every call in it must answer; the answer
            spoken of is the LAST call's)
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[18446744073709551615, 1]", "the_batch": "[]"},
            on the compiled Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_batch": "[]", "the_ledger":
                     "[428257041932146292, 18018487031777405324]"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 1 transfer (the rule's assertion; input {"the_batch":
                     "[0->1:33]", "the_ledger": "[48, 18446744073709551583]"}; on the compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.batch_then_total_always.refuted2 (the negation
                     of the rule statement) at {"the_ledger": "[18446744073709551615, 1]", "the_batch": "[]"};
                     axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[]", "the_ledger": "[428257041932146292, 18018487031777405324]"}   source:
                     generated property test (case 1 of the run, shrunk). COUNTEREXAMPLE: on the compiled Rust it
                     fails; on the Lean model the reading fails
    found false at   {"the_batch": "[0->1:33]", "the_ledger": "[48, 18446744073709551583]"}   source: generated
                     bounded check (Kani at up to 2 accounts and up to 1 transfer; replayed on the compiled Rust
                     through the generated predicate). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean
                     model the reading fails
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, l.total: domain, unsigned, and_then: modifier, unsigned, always:
                 frame, unsigned, accepted: modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar,
                 unsigned, g.rule_vp: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2:
                 default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.batch_then_total_always.refuted2)
    translation  Lean models ledger.Ledger.apply_batch, ledger.Ledger.total generated from ledger/src/lib.rs by
                 charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch followed by a computation of the total: every ledger, every batch (a list of transfers, in
                        order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the answer is an acceptance (see `accepted`)
                        (of a sequence: every call in it must answer; the answer spoken of is the LAST call's)
            accepted    an acceptance is an answer that carries a value; an answer with no value is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.batch_then_total_always.refuted2 : ¬
                             Rule.ledger_rules.batch_then_total_always.reading; axioms propext, Classical.choice,
                             Quot.sound
            counterexample   ledger = [18446744073709551615, 1], batch = []
                             at this input the rule does not hold: NOT "the answer is an acceptance (see `accepted`)"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (297 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.batch_then_total_always.reading : Prop :=
  Frames.Always ((L.applyBatch).andThen L.total) (fun ans => ((L.applyBatch).andThen L.total).accepted ans)
```

</details>

### Rule: A transfer is accepted whenever the transfer is valid on the ledger

```text
Rule: A transfer is accepted whenever the transfer is valid on the ledger   [features/ledger_rules.feature:154]   tags @id:f_if_then
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; then the call gives an answer [default
            D1]; if the transfer can be carried out exactly on the ledger (both accounts exist and differ, the
            sender covers the amount, the receiver's balance stays within 2^64 - 1), then the answer is an
            acceptance (see `accepted`) (and the call gives an answer whether or not the transfer can be carried out
            exactly on the ledger (both accounts exist and differ, the sender covers the amount, the receiver's
            balance stays within 2^64 - 1))
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.f_if_then.proved, Rule.ledger_rules.f_if_then,
                     Rule.ledger_rules.f_if_then.reading_iff_obligation: the rule statement for all inputs and all
                     sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      15 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, if_then: frame, unsigned, holds_of: modifier, unsigned, l.the_transfer:
                 domain, unsigned, l.valid: domain, unsigned, accepted: modifier, unsigned, calls.every: coverage,
                 unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned,
                 g.line: grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, D8:
                 default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.f_if_then.proved, Rule.ledger_rules.f_if_then,
                 Rule.ledger_rules.f_if_then.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        if the transfer can be carried out exactly on the ledger (both accounts exist and differ, the
                        sender covers the amount, the receiver's balance stays within 2^64 - 1), then the answer is an
                        acceptance (see `accepted`) (and the call gives an answer whether or not the transfer can be
                        carried out exactly on the ledger (both accounts exist and differ, the sender covers the amount,
                        the receiver's balance stays within 2^64 - 1))
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.f_if_then.proved : Rule.ledger_rules.f_if_then.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem: the supplied proof of its flat obligation carried through
                             the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_if_then : Rule.ledger_rules.f_if_then.obligation
                             (hand-written, lean/Wallet/RuleProofs/ledger_rules/f_if_then.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.f_if_then.reading_iff_obligation :
                             Rule.ledger_rules.f_if_then.reading ↔ Rule.ledger_rules.f_if_then.obligation  (generated
                             script; the audit checked its type and that its proof uses no proof of either side); axioms
                             propext, Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (66 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 15 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 15 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_if_then.reading : Prop :=
  Frames.IfThen L.apply (fun st inp => L.valid st inp) (fun ans => (L.apply).accepted ans)
```

</details>

### Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing

```text
Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing   [features/ledger_rules.feature:157]   tags @id:f_rejected_unchanged
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); every such call, accepted or rejected [default D2]; assuming the transfer can NOT be
            carried out exactly on the ledger (an account does not exist, or both are the same, or the sender does
            not cover the amount, or the receiver's balance would pass 2^64 - 1); then the call gives an answer
            [default D1]; the answer is a rejection, and the whole state after the call is the state before it
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10936 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts; with up to 4 accounts; with up to 6 accounts
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.f_rejected_unchanged.proved, Rule.ledger_rules.f_rejected_unchanged,
                     Rule.ledger_rules.f_rejected_unchanged.reading_iff_obligation: the rule statement for all inputs
                     and all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      17 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, given: modifier, unsigned, rejected_unchanged: frame, unsigned,
                 holds_of: modifier, unsigned, l.the_transfer: domain, unsigned, not: modifier, unsigned, l.valid:
                 domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_vp: grammar,
                 unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2: default,
                 unsigned, D3: default, unsigned, D4: default, unsigned, D8: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.f_rejected_unchanged.proved, Rule.ledger_rules.f_rejected_unchanged,
                 Rule.ledger_rules.f_rejected_unchanged.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 66 generated inputs of the rule statement (132 of 132 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      every such call, accepted or rejected [default D2]
            assuming    the transfer can NOT be carried out exactly on the ledger (an account does not exist, or both are
                        the same, or the sender does not cover the amount, or the receiver's balance would pass 2^64 - 1)
            then        the call gives an answer [default D1]
                        the answer is a rejection, and the whole state after the call is the state before it
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.f_rejected_unchanged.proved :
                             Rule.ledger_rules.f_rejected_unchanged.reading  (THE RULE STATEMENT ITSELF, as one theorem:
                             the supplied proof of its flat obligation carried through the equivalence; type checked by
                             the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_rejected_unchanged :
                             Rule.ledger_rules.f_rejected_unchanged.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/f_rejected_unchanged.lean; type checked by the audit)
            kernel-checked   theorem Rule.ledger_rules.f_rejected_unchanged.reading_iff_obligation :
                             Rule.ledger_rules.f_rejected_unchanged.reading ↔
                             Rule.ledger_rules.f_rejected_unchanged.obligation  (generated script; the audit checked its
                             type and that its proof uses no proof of either side); axioms propext, Classical.choice,
                             Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (48 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 48 of 48 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 17 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 17 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_rejected_unchanged.reading : Prop :=
  Frames.RejectedUnchanged ((L.apply).given (fun st inp => ¬ ((L.valid st inp))))
```

</details>

### Rule: For a batch, the number of transfers applied is at least the length of the batch

```text
Rule: For a batch, the number of transfers applied is at least the length of the batch   [features/ledger_rules.feature:160]   tags @id:f_result_at_least @expect-refuted
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the number of transfers the call
            reports as applied is at least the number of transfers in the batch
  Verdict   REFUTED (false at a concrete input, kernel-checked)   (expected: REFUTED)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; it is FALSE at {"the_ledger": "[]", "the_batch": "[0->1:1]"}, on the compiled
            Rust too (reproduced)

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  FALSE at an input found at generated input 1 and shrunk: {"the_batch": "[0->0:0]", "the_ledger":
                     "[]"} (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  FALSE with up to 2 accounts and up to 1 transfer (the rule's assertion; input {"the_batch":
                     "[18446744073709551615->18446744073709551615:18446744073709551615]", "the_ledger": "[]"}; on the
                     compiled Rust it fails)
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          REFUTED in the kernel: theorem Rule.ledger_rules.f_result_at_least.refuted (the negation of the
                     rule statement) at {"the_ledger": "[]", "the_batch": "[0->1:1]"}; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted; the input also
                     fails on the compiled Rust)   [kernel-checked]
    found false at   {"the_batch": "[0->0:0]", "the_ledger": "[]"}   source: generated property test (case 1 of the
                     run, shrunk). COUNTEREXAMPLE: on the compiled Rust it fails; on the Lean model the reading fails
    found false at   {"the_batch": "[18446744073709551615->18446744073709551615:18446744073709551615]", "the_ledger":
                     "[]"}   source: generated bounded check (Kani at up to 2 accounts and up to 1 transfer; replayed
                     on the compiled Rust through the generated predicate). falsifying input: on the compiled Rust it
                     fails; NOT EVALUATED on the Lean model (an account number above 4294967295 has no literal in the
                     Lean model, which leaves the width of usize open: the_batch)
    STRONGEST HELD   a kernel-checked REFUTATION: the rule is false (the input was found by the grid search of the
                     reading)

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      12 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, result_at_least: frame, unsigned, l.applied: domain, unsigned,
                 l.length: domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement is refuted at a concrete input; axioms: propext,
                 Classical.choice, Quot.sound (the standard three only)   [kernel-checked]
                 (Rule.ledger_rules.f_result_at_least.refuted)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is at least the number of transfers in the
                        batch
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.f_result_at_least.refuted : ¬
                             Rule.ledger_rules.f_result_at_least.reading; axioms propext, Classical.choice, Quot.sound
            counterexample   ledger = [], batch = [0->1:1]
                             at this input the rule does not hold: NOT "the number of transfers the call reports as
                             applied is at least the number of transfers in the batch"
            tested           the same input on the compiled Rust (per-piece Rust readings): reproduced
            tested           searched on 297 generated inputs (297 in scope): counterexample found; the definition of
                             each frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_result_at_least.reading : Prop :=
  Frames.ResultAtLeast L.applyBatch (fun ans => L.applied ans) (fun st inp => L.length inp)
```

</details>

### Rule: A batch never leaves the total of all balances of the ledger below zero

```text
Rule: A batch never leaves the total of all balances of the ledger below zero   [features/ledger_rules.feature:163]   tags @id:f_at_least
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; the sum of the balances of every
            account of the ledger after the call is at least 0
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.f_at_least.proved, Rule.ledger_rules.f_at_least,
                     Rule.ledger_rules.f_at_least.reading_iff_obligation: the rule statement for all inputs and all
                     sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      13 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, at_least: frame, unsigned, aggregate: modifier, unsigned,
                 l.balances_of: domain, unsigned, zero: modifier, unsigned, calls.every: coverage, unsigned,
                 g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line:
                 grammar, unsigned, D1: default, unsigned, D2: default, unsigned, D4: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.f_at_least.proved, Rule.ledger_rules.f_at_least,
                 Rule.ledger_rules.f_at_least.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        the sum of the balances of every account of the ledger after the call is at least 0
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            kernel-checked   theorem Rule.ledger_rules.f_at_least.proved : Rule.ledger_rules.f_at_least.reading  (THE
                             RULE STATEMENT ITSELF, as one theorem: the supplied proof of its flat obligation carried
                             through the equivalence; type checked by the audit); axioms propext, Classical.choice,
                             Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_at_least : Rule.ledger_rules.f_at_least.obligation
                             (hand-written, lean/Wallet/RuleProofs/ledger_rules/f_at_least.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.f_at_least.reading_iff_obligation :
                             Rule.ledger_rules.f_at_least.reading ↔ Rule.ledger_rules.f_at_least.obligation  (generated
                             script; the audit checked its type and that its proof uses no proof of either side); axioms
                             propext, Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 13 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 13 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_at_least.reading : Prop :=
  Frames.AtLeast L.applyBatch (fun st inp => Frames.aggregate (((L.balances st).map L.amount))) (fun st inp => 0)
```

</details>

### Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards

```text
Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards   [features/ledger_rules.feature:166]   tags @id:f_none_of
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; then the call gives an answer [default D1]; no transfer of the batch at the
            position the reported count points to (none if every transfer was applied) can be carried out exactly on
            the ledger (both accounts exist and differ, the sender covers the amount, the receiver's balance stays
            within 2^64 - 1), judged on the state after the call
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.f_none_of.proved, Rule.ledger_rules.f_none_of,
                     Rule.ledger_rules.f_none_of.reading_iff_obligation: the rule statement for all inputs and all
                     sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      14 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, none_of: frame, unsigned, l.stopped_at: domain, unsigned, l.valid:
                 domain, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned, g.rule_for:
                 grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default, unsigned, D2:
                 default, unsigned, D4: default, unsigned, D5: default, unsigned, D7: default, unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.f_none_of.proved, Rule.ledger_rules.f_none_of,
                 Rule.ledger_rules.f_none_of.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    nothing: every state and every input
            then        the call gives an answer [default D1]
                        no transfer of the batch at the position the reported count points to (none if every transfer was
                        applied) can be carried out exactly on the ledger (both accounts exist and differ, the sender
                        covers the amount, the receiver's balance stays within 2^64 - 1), judged on the state after the
                        call
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D7 items are judged afterwards: in a Then about a collection read off the answer, each item is
                        judged on the state after the call
            kernel-checked   theorem Rule.ledger_rules.f_none_of.proved : Rule.ledger_rules.f_none_of.reading  (THE RULE
                             STATEMENT ITSELF, as one theorem: the supplied proof of its flat obligation carried through
                             the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_none_of : Rule.ledger_rules.f_none_of.obligation
                             (hand-written, lean/Wallet/RuleProofs/ledger_rules/f_none_of.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.f_none_of.reading_iff_obligation :
                             Rule.ledger_rules.f_none_of.reading ↔ Rule.ledger_rules.f_none_of.obligation  (generated
                             script; the audit checked its type and that its proof uses no proof of either side); axioms
                             propext, Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (297 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 297 of 297 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 14 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 14 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_none_of.reading : Prop :=
  Frames.NoneOf L.applyBatch (fun st inp ans => L.stoppedAt inp ans) (fun st inp x => L.valid st x)
```

</details>

### Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero

```text
Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero   [features/ledger_rules.feature:169]   tags @id:f_no_valid_none_applied
  Reading   for a batch: every ledger, every batch (a list of transfers, in order); every such call, accepted or
            rejected [default D2]; assuming no transfer of the batch can be carried out exactly on the ledger (both
            accounts exist and differ, the sender covers the amount, the receiver's balance stays within 2^64 - 1);
            then the call gives an answer [default D1]; the number of transfers the call reports as applied is 0
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  none: no scenario with Examples rows sits under this rule
  Generated the rule statement at 297 generated inputs on the compiled Rust: the same result as on the Lean model at
            594 of 594 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   none: no scenario sits under this rule
                     rests on: nothing
    2 property test  10000 generated inputs in scope (12528 generated), none falsifies it (seed 20261111)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  holds for every input with up to 2 accounts and up to 1 transfer; with up to 2 accounts and up
                     to 2 transfers; with up to 4 accounts and up to 1 transfer; with up to 2 accounts and up to 3
                     transfers; with up to 6 accounts and up to 4 transfers
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          theorem Rule.ledger_rules.f_no_valid_none_applied.proved,
                     Rule.ledger_rules.f_no_valid_none_applied,
                     Rule.ledger_rules.f_no_valid_none_applied.reading_iff_obligation: the rule statement for all
                     inputs and all sizes, a supplied proof of its flat obligation; axioms: propext,
                     Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: there is no scenario beneath this rule

  Rests on
    meaning      18 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply_batch: domain, unsigned, given: modifier, unsigned, result_is: frame, unsigned, no_such:
                 modifier, unsigned, l.transfers: domain, unsigned, l.valid: domain, unsigned, l.applied: domain,
                 unsigned, zero: modifier, unsigned, calls.every: coverage, unsigned, g.subject: grammar, unsigned,
                 g.rule_for: grammar, unsigned, g.role: grammar, unsigned, g.line: grammar, unsigned, D1: default,
                 unsigned, D2: default, unsigned, D4: default, unsigned, D5: default, unsigned, D8: default,
                 unsigned)
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation; axioms: propext, Classical.choice, Quot.sound (the standard three only)
                 [kernel-checked]
                 (Rule.ledger_rules.f_no_valid_none_applied.proved, Rule.ledger_rules.f_no_valid_none_applied,
                 Rule.ledger_rules.f_no_valid_none_applied.reading_iff_obligation)
    translation  Lean model ledger.Ledger.apply_batch generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 297 generated inputs of the rule statement (594 of 594 evaluations the same)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a batch: every ledger, every batch (a list of transfers, in order)
            covers      every such call, accepted or rejected [default D2]
            assuming    no transfer of the batch can be carried out exactly on the ledger (both accounts exist and differ,
                        the sender covers the amount, the receiver's balance stays within 2^64 - 1)
            then        the call gives an answer [default D1]
                        the number of transfers the call reports as applied is 0
            defaults    D1 always answers: the call must return an answer for every input the reading applies to (no
                        panic, no abort, no endless loop)
                        D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or
                        rejects it
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
                        D5 collection words bind inside their own clause: 'every', 'the first', 'no' range over the named
                        collection within the one Given, Then or Rule clause they occur in
                        D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and
                        'exactly when' say about the state is judged on the state before the call (of a sequence: before
                        its first call), not on any state the call passes through or leaves
            kernel-checked   theorem Rule.ledger_rules.f_no_valid_none_applied.proved :
                             Rule.ledger_rules.f_no_valid_none_applied.reading  (THE RULE STATEMENT ITSELF, as one
                             theorem: the supplied proof of its flat obligation carried through the equivalence; type
                             checked by the audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_no_valid_none_applied :
                             Rule.ledger_rules.f_no_valid_none_applied.obligation  (hand-written,
                             lean/Wallet/RuleProofs/ledger_rules/f_no_valid_none_applied.lean; type checked by the
                             audit)
            kernel-checked   theorem Rule.ledger_rules.f_no_valid_none_applied.reading_iff_obligation :
                             Rule.ledger_rules.f_no_valid_none_applied.reading ↔
                             Rule.ledger_rules.f_no_valid_none_applied.obligation  (generated script; the audit checked
                             its type and that its proof uses no proof of either side); axioms propext,
                             Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 297 generated inputs (167 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 167 of 167 evaluations
            tested           the reading on the COMPILED RUST at the same 297 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             594 of 594 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 18 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 18 Clausebook pieces signed off by anyone
  Scenarios no scenario sits under this rule; the rule line itself is compiled, evaluated and given a verdict (above)
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_no_valid_none_applied.reading : Prop :=
  Frames.ResultIs ((L.applyBatch).given (fun st inp => Frames.noneOf ((L.transfers inp)) (fun x => (L.valid st x)))) (fun ans => L.applied ans) (fun st inp => 0)
```

</details>

### Rule: A successful transfer never changes the total of all balances of the ledger

```text
Rule: A successful transfer never changes the total of all balances of the ledger   [features/ledger_rules.feature:172]   tags @id:f_scenario_level
  Reading   for a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
            u64 amount); ONLY accepted calls [asked for]; then the sum of the balances of every account of the
            ledger after the call equals the sum of the balances of every account of the ledger before it
  Verdict   PROVED FOR ALL INPUTS (by a supplied proof of its obligation)
  Examples  2 of 2 pass on the compiled Rust; 2 of 2 pass on the Lean model
  Generated the rule statement at 66 generated inputs on the compiled Rust: the same result as on the Lean model at
            132 of 132 evaluations; no input found at which it is false

  Evidence  for the rule statement, weakest first; each rung with what it rests on
    1 example rows   2 of 2 pass on the compiled Rust; 2 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  10000 generated inputs in scope (10000 generated), none falsifies it (seed 20261111); of the 1
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
    4 proof          theorem Rule.ledger_rules.f_scenario_level.proved, Rule.ledger_rules.f_scenario_level,
                     Rule.ledger_rules.f_scenario_level.reading_iff_obligation: the rule statement for all inputs and
                     all sizes, a supplied proof of its flat obligation; axioms: propext, Classical.choice,
                     Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas, which is trusted and
                     cross-checked only by the rungs above   [kernel-checked]
    STRONGEST HELD   PROOF: kernel-checked for all inputs and sizes, on the Lean model

  Suite     not assessed: the adequacy note is generated from the flat statements of the old glossary, and the scenarios
              of this group are NEW sentences that have none

  Rests on
    meaning      26 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (l.apply: domain, unsigned, successful: modifier, unsigned, never_changes: frame, unsigned,
                 aggregate: modifier, unsigned, l.balances_of: domain, unsigned, calls.accepted: coverage, unsigned,
                 g.subject: grammar, unsigned, g.rule_vp: grammar, unsigned, g.role: grammar, unsigned, g.line:
                 grammar, unsigned, D3: default, unsigned, D4: default, unsigned, given: modifier, unsigned, i.holds:
                 idiom, unsigned, is: modifier, unsigned, l.ledger: domain, unsigned, balances_value: modifier,
                 unsigned, rejected: modifier, unsigned, always_answers: frame, unsigned, l.bal_of: domain, unsigned,
                 index_number: modifier, unsigned, calls.every: coverage, unsigned, calls.rejected: coverage,
                 unsigned, D1: default, unsigned, D2: default, unsigned, D8: default, unsigned)
                 1 scenario beneath the rule is a NEW sentence: read by the Clausebook alone, no entry of the old
                 glossary
    proof        checked by Lean's kernel: the rule statement for all inputs, a supplied proof of its flat
                 obligation, 1 scenario theorem for all inputs; axioms: propext, Classical.choice, Quot.sound (the
                 standard three only)   [kernel-checked]
                 (Rule.ledger_rules.f_scenario_level.proved, Rule.ledger_rules.f_scenario_level,
                 Rule.ledger_rules.f_scenario_level.reading_iff_obligation,
                 Spec.ledger_rules.f_other_account_untouched.reading_holds)
    translation  Lean model ledger.Ledger.apply generated from ledger/src/lib.rs by charon 0.1.315
                 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4   [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model) and
                 on 66 generated inputs of the rule statement (132 of 132 evaluations the same)   [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Reading   applies to  a transfer: every ledger, every transfer (sender->receiver:amount, two usize account numbers and a
                        u64 amount)
            covers      ONLY accepted calls [asked for]
            assuming    nothing: every state and every input
            then        the sum of the balances of every account of the ledger after the call equals the sum of the
                        balances of every account of the ledger before it
            accepted    an acceptance is the answer yes (true); the answer no is a rejection
            defaults    D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one
                        call with the state after it, not states in between
                        D4 for all values: every outline <parameter>, every state and every input is universally
                        quantified at the front; the Examples rows are instances
            not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are
                        rejected, or that give no answer, are outside this clause
            kernel-checked   theorem Rule.ledger_rules.f_scenario_level.proved :
                             Rule.ledger_rules.f_scenario_level.reading  (THE RULE STATEMENT ITSELF, as one theorem: the
                             supplied proof of its flat obligation carried through the equivalence; type checked by the
                             audit); axioms propext, Classical.choice, Quot.sound
            kernel-checked   theorem Rule.ledger_rules.f_scenario_level : Rule.ledger_rules.f_scenario_level.obligation
                             (hand-written, lean/Wallet/RuleProofs/ledger_rules/f_scenario_level.lean; type checked by
                             the audit)
            kernel-checked   theorem Rule.ledger_rules.f_scenario_level.reading_iff_obligation :
                             Rule.ledger_rules.f_scenario_level.reading ↔ Rule.ledger_rules.f_scenario_level.obligation
                             (generated script; the audit checked its type and that its proof uses no proof of either
                             side); axioms propext, Classical.choice, Quot.sound
            scope            every state and every input the rule line names (see `applies to`)
            tested           searched on 66 generated inputs (66 in scope): no counterexample; the definition of each
                             frame and its executable reading agree on 66 of 66 evaluations
            tested           the reading on the COMPILED RUST at the same 66 generated inputs, through the Rust reading
                             of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on
                             132 of 132 evaluations
            tool-trusted     rule line compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 12 Clausebook pieces;
                             echoed above for comparison
            NOT ASSERTED     0 of 12 Clausebook pieces signed off by anyone
  Scenarios SCENARIOS PROVED FOR ALL INPUTS: 1 of 1 universal scenarios proved for all inputs
            PROVED-FOR-ALL  A rejected transfer leaves every single balance as it was   [a part: the rule statement is proved from it]   [NEW sentence]
```

<details><summary>Lean statement of the rule (<code>lean/Wallet/Readings.lean</code>)</summary>

```lean
def Rule.ledger_rules.f_scenario_level.reading : Prop :=
  Frames.NeverChanges (L.apply).successful (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

</details>

#### PROVED-FOR-ALL: A rejected transfer leaves every single balance as it was

`features/ledger_rules.feature:176`  id `Spec.ledger_rules.f_other_account_untouched`  tags `@id:f_other_account_untouched`

```gherkin
Scenario Outline: A rejected transfer leaves every single balance as it was
  Given ledger Main holds the balances <balances>
  When the transfer <t> is applied to ledger Main
  Then if it is rejected, the balance of account <k> of ledger Main is unchanged
  And if it is accepted, the total of ledger Main's balances is unchanged

  Examples:
    | balances      | t        | k |
    | [100, 20, 0]  | 0->3:1   | 1 |
    | [100, 20, 0]  | 0->1:5   | 2 |
```

Reading (how the sentence was compiled, in fixed English; compare it with the scenario above):

```text
applies to  applying the transfer <t> to ledger Main: every ledger Main, and every transfer <t>
            (sender->receiver:amount, two usize account numbers and a u64 amount); for every value of balances (a list
            of u64 balances, account 0 first), k (an account number, a usize)
covers      every such call, accepted or rejected [default D2]; ONLY rejected calls [asked for]; ONLY accepted calls
            [asked for]
assuming    the balances of ledger Main, account by account is <balances>
then        the call gives an answer [default D1]
            if the call is rejected: the balance, in ledger Main, of account <k> (0 if there is no such account) after
            the call equals the balance, in ledger Main, of account <k> (0 if there is no such account) before it
            if the call is accepted: the sum of the balances of every account of ledger Main after the call equals the
            sum of the balances of every account of ledger Main before it
accepted    an acceptance is the answer yes (true); the answer no is a rejection
defaults    D1 always answers: the call must return an answer for every input the reading applies to (no panic, no
            abort, no endless loop)
            D2 rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects
            it
            D3 before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with
            the state after it, not states in between
            D4 for all values: every outline <parameter>, every state and every input is universally quantified at the
            front; the Examples rows are instances
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
not default ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are rejected,
            or that give no answer, are outside this clause
not default ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or
            that give no answer, are outside this clause
```

```text
PROVED-FOR-ALL  A rejected transfer leaves every single balance as it was
  kernel-checked   theorem Spec.ledger_rules.f_other_account_untouched.reading_holds : Spec.ledger_rules.f_other_account_untouched.reading  (THE READING ITSELF, as one theorem: the supplied proof of its flat obligation carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.ledger_rules.f_other_account_untouched : Spec.ledger_rules.f_other_account_untouched.obligation  (hand-written, lean/Wallet/Proofs/ledger_rules/f_other_account_untouched.lean; type checked by the audit)
  kernel-checked   theorem Spec.ledger_rules.f_other_account_untouched.reading_iff_obligation : Spec.ledger_rules.f_other_account_untouched.reading ↔ Spec.ledger_rules.f_other_account_untouched.obligation  (generated script; the audit checked its type and that its proof uses no proof of either side); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.ledger_rules.f_other_account_untouched.reading_sat)
  scope            every input satisfying the Givens
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     reading compiled by clausal 7bd9f57bc2ba (clausal-rule/4) from 22 Clausebook pieces; echoed above for comparison with the scenario
  new sentence     no entry of the old whole-phrase glossary is involved: no flat statement of that kind, no hand-written step, no hand-written Rust predicate
  NOT ASSERTED     0 of 22 Clausebook pieces signed off by anyone - UNREVIEWED: l.apply, given, i.holds, is, l.ledger, balances_value, rejected, successful, always_answers, never_changes, l.bal_of, index_number, aggregate, l.balances_of, calls.every, calls.rejected, calls.accepted, D1, D2, D3, D4, D8
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs, generic step: the composition tree evaluated by the per-piece Rust readings); 2 of 2 pass on the Lean model; they agree
  tested           the reading on 3630 generated inputs (330 in scope) on the Lean model: no counterexample; the definition of each frame and its executable reading agree on 990 of 990 evaluations
  tested           the reading on the COMPILED RUST at the same 3630 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 14520 of 14520 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `l.apply, given, i.holds, is, l.ledger, balances_value, rejected, successful, always_answers, never_changes, l.bal_of, index_number, aggregate, l.balances_of, calls.every, calls.rejected, calls.accepted, D1, D2, D3, D4, D8`:

```lean
def Spec.ledger_rules.f_other_account_untouched.reading : Prop :=
  ∀ (balances : List U64) (k : Usize),
    Frames.AlwaysAnswers ((L.apply).given (fun st inp => (L.balances st) = balances)) ∧
    Frames.NeverChanges (((L.apply).given (fun st inp => (L.balances st) = balances)).rejected) (fun st inp => L.bal st k.val) ∧
    Frames.NeverChanges (((L.apply).given (fun st inp => (L.balances st) = balances)).successful) (fun st inp => Frames.aggregate (((L.balances st).map L.amount)))
```

Flat proof obligation, generated from the pieces (`lean/Wallet/Obligations.lean`); a NEW sentence has no flat statement in the old glossary:

```lean
def Spec.ledger_rules.f_other_account_untouched.obligation : Prop :=
  (∀ (balances : List U64) (k : Usize) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ True ∧ (¬ L.said ans → (L.bal st' k.val) = (L.bal st k.val)) ∧ (L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

Supplied proof of the obligation (`lean/Wallet/Proofs/ledger_rules/f_other_account_untouched.lean`):

```lean
theorem Spec.ledger_rules.f_other_account_untouched : Spec.ledger_rules.f_other_account_untouched.obligation := by
  intro balances k st inp _
  obtain ⟨⟨a, l'⟩, e, h⟩ := Bdd.ok_of_spec (ledger.Ledger.apply.spec st inp)
  refine ⟨a, l', e, trivial, ?_, ?_⟩
  · intro hn
    rcases h with ⟨rfl, -⟩ | ⟨-, -, rfl, -⟩
    · exact absurd rfl hn
    · rfl
  · intro _
    rcases h with ⟨-, -, -, ht, -⟩ | ⟨-, -, rfl, -⟩
    · exact ht
    · rfl
```

</details>

### (scenarios of `Feature: Negative controls` that are not under a Rule)

```text
(scenarios of `Feature: Negative controls` that are not under a Rule)   [features/negative.feature]   tags @control
  Verdict   SOME SCENARIOS PROVED: 1 of 2 universal scenarios proved for all inputs
  Examples  1 of 2 pass on the compiled Rust; 1 of 2 pass on the Lean model

  Evidence  for the scenarios, weakest first; each rung with what it rests on
    1 example rows   1 of 2 pass on the compiled Rust; 1 of 2 on the Lean model
                     rests on: the rows the author wrote, and nothing beyond them; cucumber-rs through the per-piece
                     Rust readings; rustc   [tested]
    2 property test  1 of 2 scenarios: none falsified in 10000 generated inputs in scope (seed 20261111); A
                     withdrawal that is both covered and not covered: no result: 0 inputs in scope among 1000001
                     generated (the scope is hardly ever or never met)
                     rests on: a test GENERATED from the same composition tree as the Lean statement (no test code
                     written for this rule); proptest 1.12.0 with shrinking; generators derived from the types and
                     the Givens, edge-weighted, collections up to 6 items; the typed piece readings, compared with
                     the tree evaluator at every case; the compiled Rust (rustc). A sample: it says nothing about
                     inputs it did not draw   [tested, sampled]
    3 bounded check  2 of 2 scenarios hold at every rung of the ladder, 0 at some rungs only, 0 shown false
                     rests on: a harness GENERATED from the same tree, asserting the same generated predicate; Kani
                     Rust Verifier 0.68.0 (cargo plugin) / CBMC 6.11.0 on the Rust's MIR; every integer symbolic;
                     collections bounded by a fixed ladder of sizes, the same for every rule (given in the result; 30
                     s per rung); it says nothing beyond those sizes, and trusts Kani and CBMC   [tool-checked,
                     bounded]
    4 proof          1 scenario theorem for all inputs (Spec.negative_controls.bystander_unchanged); 1 shown true of
                     nothing; axioms: propext, Classical.choice, Quot.sound
                     rests on: Lean's kernel; the Lean model generated by charon + aeneas (trusted)
                     [kernel-checked]
    STRONGEST HELD   PROOF for 1 of 2 scenarios (kernel-checked, on the Lean model); the others hold what the rungs
                     above say and are NOT PROVED

  Suite     not assessed: its scenarios are tagged @control

  Rests on
    meaning      20 Clausebook pieces, 0 signed   [NOT ASSERTED by anyone]
                 (w.withdraw: domain, unsigned, given: modifier, unsigned, is: modifier, unsigned, w.balance: domain,
                 unsigned, amount_value: modifier, unsigned, more_than: modifier, unsigned, not_more_than: modifier,
                 unsigned, always: frame, unsigned, w.succeeds: domain, unsigned, calls.every: coverage, unsigned,
                 D1: default, unsigned, D2: default, unsigned, D4: default, unsigned, D8: default, unsigned,
                 w.deposit: domain, unsigned, beside: modifier, unsigned, sum_within: modifier, unsigned, w.maximum:
                 domain, unsigned, never_changes: frame, unsigned, D3: default, unsigned)
                 2 of 2 scenario readings proved equivalent to the flat statement their proof is about
                 [kernel-checked]
                 the flat statements of the older scenarios still use 8 whole-phrase entries of the old glossary, 0
                 signed
    proof        checked by Lean's kernel: 1 scenario theorem for all inputs, 1 proof that the Givens contradict each
                 other (the scenario is true of nothing); axioms: propext, Classical.choice, Quot.sound (the standard
                 three only)   [kernel-checked]
                 (Spec.negative_controls.bystander_unchanged, Spec.negative_controls.contradictory_givens.unsat)
    translation  Lean models wallet.Wallet.withdraw, wallet.Wallet.deposit generated from wallet/src/lib.rs by charon
                 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2) + aeneas nightly-2026.11.09-5a392f4
                 [tool-trusted]
                 cross-checked on 2 example rows (2 give the same result on the compiled Rust and on the model)
                 [tested]
    compilation  rustc 1.94.0 (4a4ef493e 2026-03-02), as used for the cucumber-rs test build   [trusted, not checked]

  Detail
  Scenarios SOME SCENARIOS PROVED: 1 of 2 universal scenarios proved for all inputs
            VACUOUS         A withdrawal that is both covered and not covered   (expected VACUOUS)
            PROVED-FOR-ALL  A deposit does not touch a bystander
```

#### VACUOUS: A withdrawal that is both covered and not covered

`features/negative.feature:11`  id `Spec.negative_controls.contradictory_givens`  tags `@control @id:contradictory_givens @expect-vacuous`

```gherkin
Scenario Outline: A withdrawal that is both covered and not covered
  Given Alice's balance is <a>
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
applies to  a withdrawal of <amount> from Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
VACUOUS  A withdrawal that is both covered and not covered
  kernel-checked   theorem Spec.negative_controls.contradictory_givens.reading_iff : Spec.negative_controls.contradictory_givens.reading ↔ Spec.negative_controls.contradictory_givens.stmt  (NEW ↔ OLD: the reading compiled from 14 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.negative_controls.contradictory_givens.unsat: no input satisfies all the Givens; axioms propext, Quot.sound
  meaning          the scenario is true of nothing; any proof of it would be worthless
  about            the Lean model wallet.Wallet.withdraw, not the Rust source
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-exceeds, G-covers, W-withdraw, T-ok
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 111 of 111 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
  NOT ASSERTED     0 of 14 Clausebook pieces signed off by anyone - UNREVIEWED: w.withdraw, given, is, w.balance, amount_value, more_than, not_more_than, always, w.succeeds, calls.every, D1, D2, D4, D8
  tested           the reading on 216 generated inputs (0 in scope): the definition of each frame and its executable reading agree on 0 of 0 evaluations
  tested           the reading on the COMPILED RUST at the same 216 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 432 of 432 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.withdraw, given, is, w.balance, amount_value, more_than, not_more_than, always, w.succeeds, calls.every, D1, D2, D4, D8`:

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
  Given Alice's balance is <a>
  And Bob's balance is <b>
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
applies to  a deposit of <amount> into Alice: every wallet (Alice), and every amount <amount> (a u64: 0 to 2^64 - 1);
            for every value of a (a u64: 0 to 2^64 - 1), b (a u64: 0 to 2^64 - 1)
            beside it: Bob (named, but not passed to the operation, so unchanged by construction)
covers      every such call, accepted or rejected [default D2]
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
            D8 conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly
            when' say about the state is judged on the state before the call (of a sequence: before its first call), not
            on any state the call passes through or leaves
```

```text
PROVED-FOR-ALL (1 of 2 Thens substantive)  A deposit does not touch a bystander
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged.reading_holds : Spec.negative_controls.bystander_unchanged.reading  (THE READING ITSELF, as one theorem: the proof of the flat statement carried through the equivalence; type checked by the audit); axioms propext, Classical.choice, Quot.sound
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged.reading_iff : Spec.negative_controls.bystander_unchanged.reading ↔ Spec.negative_controls.bystander_unchanged.stmt  (NEW ↔ OLD: the reading compiled from 17 Clausebook pieces is equivalent to the flat statement below; generated script, type checked by the audit); axioms propext, Classical.choice, Quot.sound; reading non-vacuous (Spec.negative_controls.bystander_unchanged.reading_sat)
  kernel-checked   theorem Spec.negative_controls.bystander_unchanged : Spec.negative_controls.bystander_unchanged.stmt (type checked by the audit; 4-line proof, lean/Wallet/Proofs/negative_controls/bystander_unchanged.lean:16); axioms propext, Classical.choice, Quot.sound; Givens satisfiable (Spec.negative_controls.bystander_unchanged.sat)
  scope            every input satisfying the Givens
  about            the Lean model wallet.Wallet.deposit, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by wallet.Wallet.deposit: Aeneas.Std.U64.checked_add
  tool-trusted     statement generated by clausal 7bd9f57bc2ba (clausal-rule/4); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: G-balance, G-room, W-deposit, T-ok, T-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 111 of 111 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  flag             TRIVIAL-THEN: follows from the Givens alone, whatever the code does: "Bob's balance is unchanged"
  flag             FRAME-TRIVIAL: the call does not return this actor, so the Then compares it with itself: "Bob's balance is unchanged"
  NOT ASSERTED     0 of 17 Clausebook pieces signed off by anyone - UNREVIEWED: w.deposit, beside, given, is, w.balance, amount_value, sum_within, w.maximum, always, never_changes, w.succeeds, calls.every, D1, D2, D3, D4, D8
  tested           the reading on 7776 generated inputs (126 in scope): the definition of each frame and its executable reading agree on 252 of 252 evaluations
  tested           the reading on the COMPILED RUST at the same 7776 generated inputs, through the Rust reading of each piece (wallet-bdd/src/pieces.rs): agrees with the Lean pieces on the Lean model on 23328 of 23328 evaluations
```

<details><summary>Lean: the compiled reading, the flat statement the proof is about, the proof</summary>

Compiled reading (`lean/Wallet/Readings.lean`), from pieces `w.deposit, beside, given, is, w.balance, amount_value, sum_within, w.maximum, always, never_changes, w.succeeds, calls.every, D1, D2, D3, D4, D8`:

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
- **(b) a fixed English paraphrase** with slots, used for the echo (`clausebook/`, `echo:`);
- **(c) an independent executable reading** (`lean/Frames/Check.lean`): run the call, then case on what came back. The definition and the executable reading are evaluated side by side on generated inputs for the concrete operations (`lean/Run/ReadingSearch.lean`; NASA FRET's practice of two semantics per template). A disagreement fails the run. The comparison can only catch a wrong reading where the claim is FALSE or the call gives NO ANSWER, and the fixtures hardly ever supply either, so every frame is also compared on a toy operation that gives no answer at one input and rejects another (`lean/Run/FrameToyTests.lean`). The last column counts, per source, the evaluations at which the definition is false and those at which the call is silent; a frame for which no comparison of this run saw both is marked **comparison untested**.

| # | Frame | Lean definition | English paraphrase (slots in braces) | Executable reading | Definition vs executable reading |
|---|---|---|---|---|---|
| 1 | `always_answers` | `@[reducible] def AlwaysAnswers.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ _ _ => True) s a` | the call gives an answer | `Frames.Check.alwaysAnswers` | agree on 699 evaluations in 4 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (4 false, 4 silent) |
| 2 | `never_changes` | `@[reducible] def NeverChanges.at (op : Op σ α ρ) (m : Measure σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a) s a` | {m} after the call equals {m} before it | `Frames.Check.neverChanges` | agree on 12637 evaluations in 31 readings of the fixtures (18 false, 0 silent); agree on 60 of 60 evaluations in 3 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (28 false, 12 silent) |
| 3 | `changes_only` | `@[reducible] def ChangesOnly.at (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => parts s' = parts s ∧ ∀ k ∈ parts s, k ∉ X s a → m s' k = m s k) s a` | {c} are the same after the call, and every one of them other than {xs} has the {part} it had before | `Frames.Check.changesOnly` | agree on 84 evaluations in 2 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 4 silent) |
| 4 | `always` | `@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => cls r) s a` | {c} | `Frames.Check.always` | agree on 1005 evaluations in 16 readings of the fixtures (157 false, 0 silent); agree on 60 of 60 evaluations in 3 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (16 false, 12 silent) |
| 4 | `never` | `@[reducible] def Never.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => ¬ cls r) s a` | it is NOT the case that {c} | `Frames.Check.never` | agree on 650 evaluations in 10 readings of the fixtures (16 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (16 false, 4 silent) |
| 5 | `if_then` | `@[reducible] def IfThen.at (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => C s a → cls r) s a` | if {k}, then {c} (and the call gives an answer whether or not {k}) | `Frames.Check.ifThen` | agree on 66 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 40 of 40 evaluations in 2 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 8 silent) |
| 6 | `only_if` | `@[reducible] def OnlyIf.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r → C s a) s a` | {c} only if {k} | `Frames.Check.onlyIf` | agree on 66 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 7 | `exactly_when` | `@[reducible] def ExactlyWhen.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a` | {c} if and only if {k} | `Frames.Check.exactlyWhen` | agree on 374 evaluations in 3 readings of the fixtures (0 false, 0 silent); agree on 40 of 40 evaluations in 2 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (16 false, 8 silent) |
| 8 | `rejected_unchanged` | `@[reducible] def RejectedUnchanged.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s _ r s' => ¬ op.accepted r ∧ s' = s) s a` | the answer is a rejection, and the whole state after the call is the state before it | `Frames.Check.rejectedUnchanged` | agree on 48 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (16 false, 4 silent) |
| 9 | `increases_by` | `@[reducible] def IncreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a + f s a) s a` | {m} after the call equals {m} before it plus {t}, exactly | `Frames.Check.increasesBy` | agree on 232 evaluations in 5 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 9 | `decreases_by` | `@[reducible] def DecreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a` | {m} after the call, plus {t}, equals {m} before it, exactly | `Frames.Check.decreasesBy` | agree on 358 evaluations in 6 readings of the fixtures (35 false, 0 silent); agree on 40 of 40 evaluations in 2 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (36 false, 8 silent) |
| 9 | `becomes` | `@[reducible] def Becomes.at (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = f s a) s a` | {m} after the call is {t} | `Frames.Check.becomes` | agree on 71 evaluations in 6 readings of the fixtures (36 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 9 | `result_is` | `@[reducible] def ResultIs.at (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r = f s a) s a` | {a} is {t} | `Frames.Check.resultIs` | agree on 1027 evaluations in 11 readings of the fixtures (14 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 10 | `result_at_most` | `@[reducible] def ResultAtMost.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r ≤ f s a) s a` | {a} is at most {t} | `Frames.Check.resultAtMost` | agree on 8613 evaluations in 3 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 10 | `result_at_least` | `@[reducible] def ResultAtLeast.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => f s a ≤ out r) s a` | {a} is at least {t} | `Frames.Check.resultAtLeast` | agree on 297 evaluations in 1 readings of the fixtures (225 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 10 | `at_most` | `@[reducible] def AtMost.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a` | {m} after the call is at most {t} | `Frames.Check.atMost` | agree on 660 evaluations in 3 readings of the fixtures (162 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 4 silent) |
| 10 | `at_least` | `@[reducible] def AtLeast.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => f s a ≤ m s' a) s a` | {m} after the call is at least {t} | `Frames.Check.atLeast` | agree on 297 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (8 false, 4 silent) |
| 11 | `every_of` | `@[reducible] def EveryOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, P s' a x) s a` | every {c} {p}, judged on the state after the call | `Frames.Check.everyOf` | agree on 594 evaluations in 2 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 4 silent) |
| 11 | `none_of` | `@[reducible] def NoneOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, ¬ P s' a x) s a` | no {c} {p}, judged on the state after the call | `Frames.Check.noneOf` | agree on 297 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 4 silent) |
| 12 | `monotone` | `@[reducible] def Monotone.at (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 more (fun r _ r₂ _ => cls r → cls r₂) s a s₂ a₂` | whenever {v}, and for the first call {c}, then for the second call too {c} | `Frames.Check.monotone` | agree on 296 evaluations in 3 readings of the fixtures (5 false, 0 silent); agree on 798 of 798 evaluations in 6 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (50 false, 54 silent) |
| 13 | `agrees_with` | `@[reducible] def AgreesWith.at (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => (r, s') = ref s a) s a` | the answer and the state after the call are exactly what {r} gives for the state before and the input | `Frames.Check.agreesWith` | agree on 704 evaluations in 4 readings of the fixtures (31 false, 0 silent); agree on 55 of 55 evaluations in 3 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (13 false, 4 silent) |
| 14 | `same_answer` | `@[reducible] def IndependentOf.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => view r s' = view r₂ s₂') s a s₂ a₂` | whenever {v}, the two calls give the same answer | `Frames.Check.independentOf` | agree on 437 evaluations in 2 readings of the fixtures (10 false, 0 silent); agree on 1582 of 1582 evaluations in 4 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (246 false, 18 silent) |
| 15 | `within` | `@[reducible] def Within.at (op : Op σ α ρ) (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => ∀ x ∈ sub s' a r, x ∈ sup s a) s a` | every {c} is a {d} (the first is read off the answer, the second off the input before the call) | `Frames.Check.within` | agree on 297 evaluations in 1 readings of the fixtures (0 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (7 false, 4 silent) |
| 15 | `covers` | `@[reducible] def Covers.at (op : Op σ α ρ) (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => ∀ x ∈ sub s a, x ∈ sup s' a r) s a` | every {d} is a {c} (the first is read off the input before the call, the second off the answer) | `Frames.Check.covers` | agree on 297 evaluations in 1 readings of the fixtures (203 false, 0 silent); agree on 20 of 20 evaluations in 1 hand-written instance (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (12 false, 4 silent) |
| 16 | `same_answer_if` | `@[reducible] def IndependentGiven.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (cls : AnswerClass ρ) (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => cls r → view r s' = view r₂ s₂') s a s₂ a₂` | whenever {v}, and for the first call {c}, the two calls give the same answer | `Frames.Check.independentGiven` | agree on 176 evaluations in 2 readings of the fixtures (5 false, 0 silent); agree on 100 of 100 evaluations in 2 hand-written instances (`lean/Run/FrameTests.lean`, `FrameToyTests.lean`) (26 false, 36 silent) |
| 11 | `count_of` (no surface form yet) | `@[reducible] def CountOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) [∀ s a x, Decidable (P s a x)] (cmp : Cmp) (n : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => cmp.holds ((coll s' a r).countP (fun x => decide (P s' a x))) (n s a)) s a` | at most / at least / exactly n {c} {p}, judged on the state after the call | `Frames.Check.countOf` | no transfer of the batch is valid on the ledger afterwards (exactly 0): agree on 42 of 42 evaluations (11 of them false); at least 1 transfer of the batch is valid on the ledger afterwards: agree on 42 of 42 evaluations (31 of them false); at most 1 transfer of the batch is valid on the ledger afterwards: agree on 42 of 42 evaluations (1 of them false); toy operation (no answer at 0, rejected at 1, accepted from 2); exactly 2: agree on 20 of 20 evaluations (8 of them false, 4 with a silent call); toy operation (no answer at 0, rejected at 1, accepted from 2); at most 1: agree on 20 of 20 evaluations (16 of them false, 4 with a silent call); toy operation (no answer at 0, rejected at 1, accepted from 2); at least 2: agree on 20 of 20 evaluations (8 of them false, 4 with a silent call) |

Over all compiled readings of the fixtures: the definition and the executable reading of the frames agree on **30282 of 30282** (point, frame) evaluations; the definition is false at 917 of them and the call is silent at 0. On the hand-written instances (the wallet and the ledger for the frames with no surface form, and the toy operation for every frame): **3281 of 3281** (677 false, 236 with a silent call). Every frame was compared at a false claim and at a silent call at least once. Agreement on generated inputs is a test, not a proof that the two readings are the same; both readings were written by one author.

**The defaults** (fail-closed; each reading lists the ones applied to it):

- **D1** always answers: the call must return an answer for every input the reading applies to (no panic, no abort, no endless loop)
- **D2** rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects it
- **D3** before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with the state after it, not states in between
- **D4** for all values: every outline <parameter>, every state and every input is universally quantified at the front; the Examples rows are instances
- **D5** collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection within the one Given, Then or Rule clause they occur in
- **D6** 'the first X of XS is P' requires that there is a first X
- **D7** items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the state after the call
- **D8** conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly when' say about the state is judged on the state before the call (of a sequence: before its first call), not on any state the call passes through or leaves
- **D9** negation binds to the one condition it is written on: 'every X is not P' means that no X is P, never 'not every X is P'
- **D10** two calls are compared: the claim is about every pair of calls of the operation related as stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and both must give an answer

**Weakenings** (never applied silently; a modifier has to ask):

- **accepted** (`calls.accepted`): ONLY accepted calls are covered (asked for by 'successful' / 'if it is accepted'); calls that are rejected, or that give no answer, are outside this clause
- **rejected** (`calls.rejected`): ONLY rejected calls are covered (asked for by 'rejected' / 'if it is rejected'); calls that are accepted, or that give no answer, are outside this clause

**Quantifier scope, the one rule.** Every outline `<parameter>`, then the state, then the input are universally quantified at the front, in that order, and Givens restrict them. Collection words (`every`, `the first`, `no`) bind inside the one clause they are written in. Negation applies to the one atomic condition it is written on. Nothing is ever existentially quantified over inputs. The tool never chooses a scope.

## Clausebook (the link from English to Lean)

`clausebook/` (4 books, in the order loaded: `clausebook/core.yaml` (68 entries), `clausebook/ledger.yaml` (16 entries), `clausebook/local/ledger.yaml` (25 entries), `clausebook/local/wallet.yaml` (7 entries)): **40 domain words** (8 operations, 32 measures, conditions, collections and answer words), **28 modifiers**, **25 frames**, and 3 idioms (a surface form that is not the regular form of one piece, with the composition it means; an idiom adds English, no Lean). A sentence is the composition of pieces its words spell out; this table and the Lean files it names are what a reviewer has to read to trust the step from English to Lean. Sign-off is per piece and is void as soon as the piece's entry or a Lean definition it names changes.

The column **Rust reading** says whether the piece's one Rust reading (`wallet-bdd/src/pieces.rs`) was set against the Lean definition in this run: every compiled reading that uses the piece is evaluated at every point of its grid of generated inputs on the Lean model (Lean pieces) and on the compiled Rust (Rust pieces), and the results are compared.

| Piece | Kind | Type | Surface forms | Lean | Definition | English paraphrase | Used by | Rust reading | Sign-off |
|---|---|---|---|---|---|---|---|---|---|
| l.apply_batch | domain | operation (ledger: ledger / batch: batch; answers `Usize`) | the batch {batch} is applied to {ledger}; in a Rule: batch | `L.applyBatch` around the Aeneas model `ledger.Ledger.apply_batch` | `@[reducible] def applyBatch : Frames.Op Ledger (Slice Transfer) Usize := Bdd.opMut ledger.Ledger.apply_batch counted` | applying the batch {batch} to {ledger}, transfer by transfer | 26 | agrees in 26 readings, 135161 generated inputs | UNREVIEWED |
| l.apply_all | domain | operation (ledger: ledger / batch: batch; answers `Bool`) | the batch {batch} is applied to {ledger} as a whole; in a Rule: batch applied as a whole | `L.applyAll` around the Aeneas model `ledger.Ledger.apply_all` | `@[reducible] def applyAll : Frames.Op Ledger (Slice Transfer) Bool := Bdd.opMut ledger.Ledger.apply_all said` | applying the batch {batch} to {ledger} as a whole | 9 | agrees in 9 readings, 10729 generated inputs | UNREVIEWED |
| l.apply | domain | operation (ledger: ledger / transfer: transfer; answers `Bool`) | the transfer {transfer} is applied to {ledger}; in a Rule: transfer, fund transfer | `L.apply` around the Aeneas model `ledger.Ledger.apply` | `@[reducible] def apply : Frames.Op Ledger Transfer Bool := Bdd.opMut ledger.Ledger.apply said` | applying the transfer {transfer} to {ledger} | 20 | agrees in 20 readings, 28974 generated inputs | UNREVIEWED |
| l.total | domain | operation (ledger: ledger; answers `Option U64`) | the total of {ledger} is computed; in a Rule: computation of the total | `L.total` around the Aeneas model `ledger.Ledger.total` | `@[reducible] def total : Frames.Op Ledger Unit (Option U64) := Bdd.opRead0 ledger.Ledger.total found` | computing the total of {ledger} | 9 | agrees in 9 readings, 24453 generated inputs | UNREVIEWED |
| l.lookup | domain | operation (ledger: ledger / account: index; answers `Option U64`) | the balance of account {account} of {ledger} is looked up; in a Rule: lookup | `L.lookup` around the Aeneas model `ledger.Ledger.balance` | `@[reducible] def lookup : Frames.Op Ledger Usize (Option U64) := Bdd.opRead ledger.Ledger.balance found` | looking up the balance of account {account} of {ledger} | 8 | agrees in 8 readings, 7480 generated inputs | UNREVIEWED |
| w.transfer | domain | operation (sender: wallet, receiver: wallet / amount: amount; answers `W.Answer`) | {sender} transfers {amount} to {receiver}; in a Rule: transfer | `W.transfer` around the Aeneas model `wallet.transfer` | `@[reducible] def transfer : Frames.Op (Wallet × Wallet) U64 Answer := Bdd.opMut2 wallet.transfer accepted` | a transfer of {amount} from {sender} to {receiver} | 7 | agrees in 7 readings, 31705 generated inputs | UNREVIEWED |
| w.deposit | domain | operation (wallet: wallet / amount: amount; answers `W.Answer`) | {wallet} deposits {amount}; in a Rule: deposit | `W.deposit` around the Aeneas model `wallet.Wallet.deposit` | `@[reducible] def deposit : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.deposit accepted` | a deposit of {amount} into {wallet} | 4 | agrees in 4 readings, 8244 generated inputs | UNREVIEWED |
| w.withdraw | domain | operation (wallet: wallet / amount: amount; answers `W.Answer`) | {wallet} withdraws {amount}; in a Rule: withdrawal | `W.withdraw` around the Aeneas model `wallet.Wallet.withdraw` | `@[reducible] def withdraw : Frames.Op Wallet U64 Answer := Bdd.opMut wallet.Wallet.withdraw accepted` | a withdrawal of {amount} from {wallet} | 4 | agrees in 4 readings, 684 generated inputs | UNREVIEWED |
| zero | modifier | term<num> | zero | `0` | - | 0 | 6 | agrees in 6 readings, 4290 generated inputs | UNREVIEWED |
| is | modifier | cond | {m:measure<T>} is {t:term<T>} | `{m} = {t}` | - | {m} is {t} | 38 | agrees in 38 readings, 189385 generated inputs | UNREVIEWED |
| not_more_than | modifier | cond | {t:term<num>} is not more than {m:measure<num>} | `{t} ≤ {m}` | - | {t} is at most {m} | 7 | agrees in 7 readings, 24042 generated inputs | UNREVIEWED |
| more_than | modifier | cond | {t:term<num>} is more than {m:measure<num>} | `{m} < {t}` | - | {t} is strictly more than {m} | 4 | agrees in 4 readings, 8934 generated inputs | UNREVIEWED |
| exceeds | modifier | cond | {m:measure<num>} is more than {t:term<num>} | `{t} < {m}` | - | {m} is strictly more than {t} | 2 | agrees in 2 readings, 3388 generated inputs | UNREVIEWED |
| at_most_value | modifier | cond | {m:measure<num>} is at most {t:term<num>} | `{m} ≤ {t}` | - | {m} is at most {t} | 2 | agrees in 2 readings, 308 generated inputs | UNREVIEWED |
| sum_within | modifier | cond | {m:measure<num>} plus {t:term<num>} does not exceed {z:term<num>} | `{m} + {t} ≤ {z}` | - | {m} plus {t} is at most {z} | 3 | agrees in 3 readings, 15768 generated inputs | UNREVIEWED |
| sum_exceeds | modifier | cond | {m:measure<num>} plus {t:term<num>} exceeds {z:term<num>} | `{z} < {m} + {t}` | - | {m} plus {t} is strictly more than {z} | 2 | agrees in 2 readings, 7992 generated inputs | UNREVIEWED |
| not | modifier | * | (no surface of its own) | `¬ ({p})` | - | it is NOT the case that {p} | 16 | agrees in 16 readings, 20638 generated inputs | UNREVIEWED |
| aggregate | modifier | measure<num> | the total of {ns:nums}; the aggregate {ns:nums} | `Frames.aggregate ({ns})` | `@[reducible] def aggregate (xs : List Nat) : Nat := xs.sum` | the sum of {ns} | 25 | agrees in 25 readings, 144633 generated inputs | UNREVIEWED |
| all_of | modifier | nums | all {pm:per_actor} | `[{pm}]` | - | {pm} | 3 | agrees in 3 readings, 15768 generated inputs | UNREVIEWED |
| holds_of | modifier | cond | {i:item<T>} {p:itempred<T>} | `{p}` | - | {i} {p} | 5 | agrees in 5 readings, 1650 generated inputs | UNREVIEWED |
| every | modifier | cond | every {c:coll<T>} {p:itempred<T>} | `Frames.every ({c}) (fun x => {p})` | `@[reducible] def every (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, P x` | every {c} {p} | 2 | agrees in 2 readings, 3564 generated inputs | UNREVIEWED |
| the_first | modifier | cond | the first {c:coll<T>} {p:itempred<T>} | `Frames.theFirst ({c}) (fun x => {p})` | `@[reducible] def theFirst (items : List ι) (P : ι → Prop) : Prop := items ≠ [] ∧ ∀ x ∈ items.head?, P x` | there is a first {c}, and it {p} | 3 | agrees in 3 readings, 6831 generated inputs | UNREVIEWED |
| no_such | modifier | cond | no {c:coll<T>} {p:itempred<T>} | `Frames.noneOf ({c}) (fun x => {p})` | `@[reducible] def noneOf (items : List ι) (P : ι → Prop) : Prop := ∀ x ∈ items, ¬ P x` | no {c} {p} | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| some_of | modifier | cond | some {c:coll<T>} {p:itempred<T>} | `Frames.someOf ({c}) (fun x => {p})` | `@[reducible] def someOf (items : List ι) (P : ι → Prop) : Prop := ∃ x ∈ items, P x` | at least one {c} {p} | 2 | agrees in 2 readings, 594 generated inputs | UNREVIEWED |
| given | modifier | opmod | (no surface of its own) | `({op}).given (fun st inp => {c})` | `@[reducible] def Op.given (op : Op σ α ρ) (C : Cond σ α) : Op σ α ρ := { op with scope := fun s a => op.scope s a ∧ C s a }` | assuming {c} | 46 | agrees in 46 readings, 191207 generated inputs | UNREVIEWED |
| rejected | modifier | opmod | (no surface of its own) | `({op}).rejected` | `@[reducible] def Op.rejected (op : Op σ α ρ) : Op σ α ρ := { op with calls := .rejected }`<br>`inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr` | rejected calls only | 7 | agrees in 7 readings, 7398 generated inputs | UNREVIEWED |
| successful | modifier | opmod | (no surface of its own) | `({op}).successful` | `@[reducible] def Op.successful (op : Op σ α ρ) : Op σ α ρ := { op with calls := .accepted }`<br>`inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr` | accepted calls only | 6 | agrees in 6 readings, 3900 generated inputs | UNREVIEWED |
| internal | modifier | opmod | (no surface of its own) | `({op}).internal {member} {parties}` | `@[reducible] def Op.internal (op : Op σ α ρ) (member : σ → ι → Prop) (parties : α → List ι) : Op σ α ρ := op.given (fun s a => ∀ p ∈ parties a, member s p)` | every party the input names is a member of the state | 2 | agrees in 2 readings, 132 generated inputs | UNREVIEWED |
| and_then | modifier | opmod | (no surface of its own) | `({op}).andThen ({op2})` | `@[reducible] def Op.andThen {α₂ ρ₂ : Type} (first : Op σ α ρ) (second : Op σ α₂ ρ₂) : Op σ (α × α₂) ρ₂ where run s a := match first.run s a.1 with \| none => none \| some (_, s₁) => second.run s₁ a.2 accepted := second.accepted` | then, on the state that leaves, | 5 | agrees in 5 readings, 111672 generated inputs | UNREVIEWED |
| beside | modifier | opmod | (no surface of its own) | `({op}).beside {type}` | `@[reducible] def Op.beside (op : Op σ α ρ) (β : Type) : Op (σ × β) α ρ where run s a := match op.run s.1 a with \| none => none \| some (r, s') => some (r, (s', s.2)) accepted := op.accepted scope s a := op.scope s.1 a calls := op.calls` | a bystander, not passed to the operation | 1 | agrees in 1 readings, 7776 generated inputs | UNREVIEWED |
| accepted | modifier | class | (no surface of its own) | `({opbase}).accepted ans` | - | the answer is an acceptance (see `accepted`) | 11 | agrees in 11 readings, 10039 generated inputs | UNREVIEWED |
| always_answers | frame | claim | it answers; (Rule) always answers | `Frames.AlwaysAnswers {op}` | `def AlwaysAnswers (op : Op σ α ρ) : Prop := ∀ s a, AlwaysAnswers.at op s a`<br>`@[reducible] def AlwaysAnswers.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ _ _ => True) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | the call gives an answer | 4 | agrees in 4 readings, 6969 generated inputs | UNREVIEWED |
| never_changes | frame | claim | {m:measure<T>} is unchanged; (Rule) never changes {m:measure<T>} | `Frames.NeverChanges {op} {m}` | `def NeverChanges (op : Op σ α ρ) (m : Measure σ α μ) : Prop := ∀ s a, NeverChanges.at op m s a`<br>`@[reducible] def NeverChanges.at (op : Op σ α ρ) (m : Measure σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call equals {m} before it | 31 | agrees in 31 readings, 152365 generated inputs | UNREVIEWED |
| changes_only | frame | claim | of {c:parts<T>}, only {x:term<T>} and {y:term<T>} change | `Frames.ChangesOnly {op} {c} {xs}` | `def ChangesOnly (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) : Prop := ∀ s a, ChangesOnly.at op parts m X s a`<br>`@[reducible] def ChangesOnly.at (op : Op σ α ρ) (parts : σ → List κ) (m : σ → κ → μ) (X : Term σ α (List κ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => parts s' = parts s ∧ ∀ k ∈ parts s, k ∉ X s a → m s' k = m s k) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} are the same after the call, and every one of them other than {xs} has the {part} it had before | 2 | agrees in 2 readings, 792 generated inputs | UNREVIEWED |
| always | frame | claim | {c:class}; (Rule) is always accepted; (Rule) always succeeds | `Frames.Always {op} {c}` | `def Always (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Always.at op cls s a`<br>`@[reducible] def Always.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => cls r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} | 26 | agrees in 26 readings, 50304 generated inputs | UNREVIEWED |
| never | frame | claim | (Rule) is never accepted; (Rule) is always rejected | `Frames.Never {op} {c}` | `def Never (op : Op σ α ρ) (cls : AnswerClass ρ) : Prop := ∀ s a, Never.at op cls s a`<br>`@[reducible] def Never.at (op : Op σ α ρ) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ _ r _ => ¬ cls r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | it is NOT the case that {c} | 10 | agrees in 10 readings, 9088 generated inputs | UNREVIEWED |
| if_then | frame | claim | (Rule) is accepted whenever {k:cond} | `Frames.IfThen {op} {k} {c}` | `def IfThen (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) : Prop := ∀ s a, IfThen.at op C cls s a`<br>`@[reducible] def IfThen.at (op : Op σ α ρ) (C : Cond σ α) (cls : AnswerClass ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => C s a → cls r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | if {k}, then {c} (and the call gives an answer whether or not {k}) | 1 | agrees in 1 readings, 66 generated inputs | UNREVIEWED |
| only_if | frame | claim | (Rule) is accepted only if {k:cond} | `Frames.OnlyIf {op} {c} {k}` | `def OnlyIf (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, OnlyIf.at op cls C s a`<br>`@[reducible] def OnlyIf.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r → C s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} only if {k} | 1 | agrees in 1 readings, 66 generated inputs | UNREVIEWED |
| exactly_when | frame | claim | (Rule) is accepted exactly when {k:cond} | `Frames.ExactlyWhen {op} {c} {k}` | `def ExactlyWhen (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) : Prop := ∀ s a, ExactlyWhen.at op cls C s a`<br>`@[reducible] def ExactlyWhen.at (op : Op σ α ρ) (cls : AnswerClass ρ) (C : Cond σ α) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => cls r ↔ C s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {c} if and only if {k} | 3 | agrees in 3 readings, 374 generated inputs | UNREVIEWED |
| rejected_unchanged | frame | claim | it is rejected and nothing is changed; (Rule) is rejected and changes nothing | `Frames.RejectedUnchanged {op}` | `def RejectedUnchanged (op : Op σ α ρ) : Prop := ∀ s a, RejectedUnchanged.at op s a`<br>`@[reducible] def RejectedUnchanged.at (op : Op σ α ρ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s _ r s' => ¬ op.accepted r ∧ s' = s) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | the answer is a rejection, and the whole state after the call is the state before it | 1 | agrees in 1 readings, 66 generated inputs | UNREVIEWED |
| increases_by | frame | claim | {m:measure<num>} is increased by {t:term<num>}; (Rule) increases {m:measure<num>} by exactly {t:term<num>} | `Frames.IncreasesBy {op} {m} {t}` | `def IncreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, IncreasesBy.at op m f s a`<br>`@[reducible] def IncreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = m s a + f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call equals {m} before it plus {t}, exactly | 5 | agrees in 5 readings, 8820 generated inputs | UNREVIEWED |
| decreases_by | frame | claim | {m:measure<num>} is decreased by {t:term<num>}; (Rule) decreases {m:measure<num>} by exactly {t:term<num>} | `Frames.DecreasesBy {op} {m} {t}` | `def DecreasesBy (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, DecreasesBy.at op m f s a`<br>`@[reducible] def DecreasesBy.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a + f s a = m s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call, plus {t}, equals {m} before it, exactly | 6 | agrees in 6 readings, 16596 generated inputs | UNREVIEWED |
| becomes | frame | claim | {m:measure<T>} is now {t:term<T>} | `Frames.Becomes {op} {m} {t}` | `def Becomes (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) : Prop := ∀ s a, Becomes.at op m f s a`<br>`@[reducible] def Becomes.at (op : Op σ α ρ) (m : Measure σ α μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a = f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is {t} | 6 | agrees in 6 readings, 129 generated inputs | UNREVIEWED |
| result_is | frame | claim | {a:ameasure<T>} is {t:term<T>} | `Frames.ResultIs {op} {a} {t}` | `def ResultIs (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) : Prop := ∀ s a, ResultIs.at op out f s a`<br>`@[reducible] def ResultIs.at (op : Op σ α ρ) (out : Answer ρ μ) (f : Term σ α μ) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r = f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is {t} | 11 | agrees in 11 readings, 28439 generated inputs | UNREVIEWED |
| result_at_most | frame | claim | {a:ameasure<num>} is at most {t:term<num>} | `Frames.ResultAtMost {op} {a} {t}` | `def ResultAtMost (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtMost.at op out f s a`<br>`@[reducible] def ResultAtMost.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => out r ≤ f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is at most {t} | 3 | agrees in 3 readings, 91773 generated inputs | UNREVIEWED |
| result_at_least | frame | claim | {a:ameasure<num>} is at least {t:term<num>} | `Frames.ResultAtLeast {op} {a} {t}` | `def ResultAtLeast (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) : Prop := ∀ s a, ResultAtLeast.at op out f s a`<br>`@[reducible] def ResultAtLeast.at (op : Op σ α ρ) (out : Answer ρ Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r _ => f s a ≤ out r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {a} is at least {t} | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| at_most | frame | claim | {m:measure<num>} is afterwards at most {t:term<num>}; (Rule) never leaves {m:measure<num>} above {t:term<num>} | `Frames.AtMost {op} {m} {t}` | `def AtMost (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtMost.at op m f s a`<br>`@[reducible] def AtMost.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => m s' a ≤ f s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is at most {t} | 3 | agrees in 3 readings, 3630 generated inputs | UNREVIEWED |
| at_least | frame | claim | {m:measure<num>} is afterwards at least {t:term<num>}; (Rule) never leaves {m:measure<num>} below {t:term<num>} | `Frames.AtLeast {op} {m} {t}` | `def AtLeast (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) : Prop := ∀ s a, AtLeast.at op m f s a`<br>`@[reducible] def AtLeast.at (op : Op σ α ρ) (m : Measure σ α Nat) (f : Term σ α Nat) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a _ s' => f s a ≤ m s' a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | {m} after the call is at least {t} | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| every_of | frame | claim | every {c:acoll<T>} {p:itempred<T>} afterwards | `Frames.EveryOf {op} {c} {p}` | `def EveryOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, EveryOf.at op coll P s a`<br>`@[reducible] def EveryOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, P s' a x) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | every {c} {p}, judged on the state after the call | 2 | agrees in 2 readings, 3564 generated inputs | UNREVIEWED |
| none_of | frame | claim | no {c:acoll<T>} {p:itempred<T>} afterwards | `Frames.NoneOf {op} {c} {p}` | `def NoneOf (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) : Prop := ∀ s a, NoneOf.at op coll P s a`<br>`@[reducible] def NoneOf.at (op : Op σ α ρ) (coll : Coll σ α ρ ι) (P : ItemCond σ α ι) (s : σ) (a : α) : Prop := op.HoldsAt (fun _ a r s' => ∀ x ∈ coll s' a r, ¬ P s' a x) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | no {c} {p}, judged on the state after the call | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| monotone | frame | claim | (Rule) never loses acceptance when {v:variation}; (Rule) never loses that {c:class} when {v:variation} | `Frames.Monotone {op} {v} {c}` | `def Monotone (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ) : Prop := ∀ s a s₂ a₂, Monotone.at op more cls s a s₂ a₂`<br>`@[reducible] def Monotone.at (op : Op σ α ρ) (more : Variation σ α) (cls : AnswerClass ρ) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 more (fun r _ r₂ _ => cls r → cls r₂) s a s₂ a₂`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | whenever {v}, and for the first call {c}, then for the second call too {c} | 3 | agrees in 3 readings, 11737 generated inputs | UNREVIEWED |
| agrees_with | frame | claim | (Rule) agrees with {r:reference} | `Frames.AgreesWith {op} {r}` | `def AgreesWith (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) : Prop := ∀ s a, AgreesWith.at op ref s a`<br>`@[reducible] def AgreesWith.at (op : Op σ α ρ) (ref : Term σ α (ρ × σ)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => (r, s') = ref s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | the answer and the state after the call are exactly what {r} gives for the state before and the input | 4 | agrees in 4 readings, 704 generated inputs | UNREVIEWED |
| same_answer | frame | claim | (Rule) gives the same answer when {v:variation} | `Frames.IndependentOf {op} {v} (fun ans _ => ans)` | `def IndependentOf (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν) : Prop := ∀ s a s₂ a₂, IndependentOf.at op differOnlyIn view s a s₂ a₂`<br>`@[reducible] def IndependentOf.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => view r s' = view r₂ s₂') s a s₂ a₂`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | whenever {v}, the two calls give the same answer | 2 | agrees in 2 readings, 7381 generated inputs | UNREVIEWED |
| within | frame | claim | every {c:acoll<T>} is a {d:coll<T>} | `Frames.Within {op} {c} {d}` | `def Within (op : Op σ α ρ) (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) : Prop := ∀ s a, Within.at op sub sup s a`<br>`@[reducible] def Within.at (op : Op σ α ρ) (sub : Coll σ α ρ ι) (sup : Term σ α (List ι)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => ∀ x ∈ sub s' a r, x ∈ sup s a) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | every {c} is a {d} (the first is read off the answer, the second off the input before the call) | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| covers | frame | claim | every {d:coll<T>} is a {c:acoll<T>} | `Frames.Covers {op} {c} {d}` | `def Covers (op : Op σ α ρ) (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) : Prop := ∀ s a, Covers.at op sup sub s a`<br>`@[reducible] def Covers.at (op : Op σ α ρ) (sup : Coll σ α ρ ι) (sub : Term σ α (List ι)) (s : σ) (a : α) : Prop := op.HoldsAt (fun s a r s' => ∀ x ∈ sub s a, x ∈ sup s' a r) s a`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'` | every {d} is a {c} (the first is read off the input before the call, the second off the answer) | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| same_answer_if | frame | claim | (Rule) gives the same answer when {v:variation}, if {c:class} | `Frames.IndependentGiven {op} {v} {c} (fun ans _ => ans)` | `def IndependentGiven (op : Op σ α ρ) (differOnlyIn : Variation σ α) (cls : AnswerClass ρ) (view : ρ → σ → ν) : Prop := ∀ s a s₂ a₂, IndependentGiven.at op differOnlyIn cls view s a s₂ a₂`<br>`@[reducible] def IndependentGiven.at (op : Op σ α ρ) (differOnlyIn : Variation σ α) (cls : AnswerClass ρ) (view : ρ → σ → ν) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.HoldsAt2 differOnlyIn (fun r s' r₂ s₂' => cls r → view r s' = view r₂ s₂') s a s₂ a₂`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | whenever {v}, and for the first call {c}, the two calls give the same answer | 2 | agrees in 2 readings, 8712 generated inputs | UNREVIEWED |
| l.ledger | domain | measure<balances> | {l:ledger} | `L.balances {l}` | `@[reducible] def balances (l : Ledger) : List U64 := l.balances.val` | the balances of {l}, account by account | 31 | agrees in 31 readings, 149982 generated inputs | UNREVIEWED |
| l.balances_of | domain | nums | {l:ledger}'s balances; the balances of {l:ledger}; all balances of {l:ledger}; account value of {l:ledger} | `(L.balances {l}).map L.amount` | `@[reducible] def balances (l : Ledger) : List U64 := l.balances.val`<br>`@[reducible] def amount (x : U64) : Nat := x.val` | the balances of every account of {l} | 22 | agrees in 22 readings, 128865 generated inputs | UNREVIEWED |
| l.bal_of | domain | measure<num> | the balance of account {k:term<acct>} of {l:ledger} | `L.bal {l} {k}` | `@[reducible] def bal (l : Ledger) (k : Nat) : Nat := (l.balances.val.getD k 0#u64).val` | the balance, in {l}, of account {k} (0 if there is no such account) | 6 | agrees in 6 readings, 5280 generated inputs | UNREVIEWED |
| l.balance_at | domain | term<optnum> | the balance of account {i:index} of {l:ledger}; the balance of {i:index} in {l:ledger} | `L.balanceAt {l} {i}` | `@[reducible] def balanceAt (l : Ledger) (i : Usize) : Option U64 := l.balances.val[i.val]?` | the balance of account {i} of {l} before the call (absent if there is no such account) | 2 | agrees in 2 readings, 660 generated inputs | UNREVIEWED |
| l.accounts | domain | parts<acct> | the accounts of {l:ledger} | `L.accounts {l}` | `@[reducible] def accounts (l : Ledger) : List Nat := List.range l.balances.val.length`<br>`@[reducible] def bal (l : Ledger) (k : Nat) : Nat := (l.balances.val.getD k 0#u64).val` | the accounts of {l} | 2 | agrees in 2 readings, 792 generated inputs | UNREVIEWED |
| l.is_account | domain | cond | {i:index} is an account of {l:ledger}; (negated) {i:index} is not an account of {l:ledger} | `L.isAccount {l} {i}` | `@[reducible] def isAccount (l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | {i} is an account number of {l} | 3 | agrees in 3 readings, 1265 generated inputs | UNREVIEWED |
| l.the_transfer | domain | item<transfer> | the transfer {t:transfer}; {t:transfer} | `{t}` | - | {t} | 5 | agrees in 5 readings, 1650 generated inputs | UNREVIEWED |
| l.sender | domain | term<acct> | the sender of {t:transfer} | `L.sender {t}` | `@[reducible] def sender (t : Transfer) : Nat := t.from.val` | the sending account of {t} | 4 | agrees in 4 readings, 1584 generated inputs | UNREVIEWED |
| l.receiver | domain | term<acct> | the receiver of {t:transfer} | `L.receiver {t}` | `@[reducible] def receiver (t : Transfer) : Nat := t.to.val` | the receiving account of {t} | 2 | agrees in 2 readings, 792 generated inputs | UNREVIEWED |
| l.amount_of | domain | term<num> | the amount of {t:transfer} | `L.amountOf {t}` | `@[reducible] def amountOf (t : Transfer) : Nat := t.amount.val` | the amount of {t} | 4 | agrees in 4 readings, 1584 generated inputs | UNREVIEWED |
| amount_value | modifier | term<num> | {x:amount} | `{x}.val` | - | {x} | 16 | agrees in 16 readings, 60745 generated inputs | UNREVIEWED |
| index_number | modifier | term<acct> | {x:index} | `{x}.val` | - | {x} | 2 | agrees in 2 readings, 3696 generated inputs | UNREVIEWED |
| balances_value | modifier | term<balances> | {x:balances} | `{x}` | - | {x} | 27 | agrees in 27 readings, 149256 generated inputs | UNREVIEWED |
| amount_result | modifier | term<optnum> | {x:amount} | `some {x}` | - | the value {x} | 2 | agrees in 2 readings, 20328 generated inputs | UNREVIEWED |
| l.valid | domain | itempred<transfer> | is valid on {l:ledger}; (negated) is not valid on {l:ledger} | `L.valid {l} {item}` | `def valid (l : Ledger) (t : Transfer) : Prop := t.from.val < l.balances.val.length ∧ t.to.val < l.balances.val.length ∧ t.from.val ≠ t.to.val ∧ t.amount.val ≤ bal l t.from.val ∧ bal l t.to.val + t.amount.val ≤ U64.max` | can be carried out exactly on {l} (both accounts exist and differ, the sender covers the amount, the receiver's balance stays within 2^64 - 1) | 16 | agrees in 16 readings, 16797 generated inputs | UNREVIEWED |
| l.maximum | domain | term<num> | the maximum | `L.maximum` | `@[reducible] def maximum : Nat := U64.max` | the largest total that can be reported (2^64 - 1) | 6 | agrees in 6 readings, 7260 generated inputs | UNREVIEWED |
| l.transfers | domain | coll<transfer> | transfer of {b:batch} | `L.transfers {b}` | `@[reducible] def transfers (b : Slice Transfer) : List Transfer := b.val` | transfer of {b} | 10 | agrees in 10 readings, 11880 generated inputs | UNREVIEWED |
| l.length | domain | term<num> | the length of {b:batch} | `L.length {b}` | `@[reducible] def length (b : Slice Transfer) : Nat := b.val.length` | the number of transfers in {b} | 6 | agrees in 6 readings, 95634 generated inputs | UNREVIEWED |
| l.applied | domain | ameasure<num> | the number of transfers applied | `L.applied ans` | `@[reducible] def applied (n : Usize) : Nat := n.val` | the number of transfers the call reports as applied | 10 | agrees in 10 readings, 99224 generated inputs | UNREVIEWED |
| l.stopped_at | domain | acoll<transfer> | transfer at which {b:batch} stopped | `L.stoppedAt {b} ans` | `@[reducible] def stoppedAt (b : Slice Transfer) (n : Usize) : List Transfer := (b.val[n.val]?).toList` | transfer of {b} at the position the reported count points to (none if every transfer was applied) | 5 | agrees in 5 readings, 4455 generated inputs | UNREVIEWED |
| l.result | domain | ameasure<optnum> | the result | `ans` | - | the value the call returns | 4 | agrees in 4 readings, 20988 generated inputs | UNREVIEWED |
| l.accepted | domain | class | it is accepted; (negated) it is rejected | `L.said ans` | `@[reducible] def said (ok : Bool) : Prop := ok = true` | the answer is yes (accepted) | 9 | agrees in 9 readings, 14194 generated inputs | UNREVIEWED |
| l.found | domain | class | there is a result; (negated) there is no result | `L.found ans` | `@[reducible] def found (o : Option U64) : Prop := o ≠ none` | the call returns a value | 6 | agrees in 6 readings, 7194 generated inputs | UNREVIEWED |
| l.smaller_amount | domain | variation | the amount is smaller | `L.smallerAmount` | `@[reducible] def smallerAmount : Frames.Variation Ledger Transfer := fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to ∧ a₂.amount.val ≤ a.amount.val` | the second call is on the same ledger, with the same sender and receiver, and its amount is at most the first call's | 1 | agrees in 1 readings, 4356 generated inputs | UNREVIEWED |
| l.larger_amount | domain | variation | the amount is larger | `L.largerAmount` | `@[reducible] def largerAmount : Frames.Variation Ledger Transfer := fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to ∧ a.amount.val ≤ a₂.amount.val` | the second call is on the same ledger, with the same sender and receiver, and its amount is at least the first call's | 3 | agrees in 3 readings, 13068 generated inputs | UNREVIEWED |
| l.only_amount_differs | domain | variation | only the amount differs | `L.onlyAmountDiffers` | `@[reducible] def onlyAmountDiffers : Frames.Variation Ledger Transfer := fun s a s₂ a₂ => s₂ = s ∧ a₂.from = a.from ∧ a₂.to = a.to` | the second call is on the same ledger, with the same sender and receiver (the two amounts may be anything) | 1 | agrees in 1 readings, 4356 generated inputs | UNREVIEWED |
| l.agrees_at_account | domain | variation | the ledger agrees at the account | `L.agreesAtAccount` | `@[reducible] def agreesAtAccount : Frames.Variation Ledger Usize := fun s a s₂ a₂ => a₂ = a ∧ s₂.balances.val[a.val]? = s.balances.val[a.val]?` | the second call looks up the same account number, on a ledger that holds the same there (the same balance, or no such account in either) | 1 | agrees in 1 readings, 3025 generated inputs | UNREVIEWED |
| l.extended | domain | variation | the ledger is extended | `L.extended` | `@[reducible] def extended : Frames.Variation Ledger Usize := fun s a s₂ a₂ => a₂ = a ∧ s.balances.val <+: s₂.balances.val` | the second call looks up the same account number, on the first ledger with accounts added at its end | 1 | agrees in 1 readings, 3025 generated inputs | UNREVIEWED |
| l.ref_lookup | domain | reference | the reference lookup | `L.refLookup` | `@[reducible] def refLookup : Frames.Term Ledger Usize (Option U64 × Ledger) := fun l i => (l.balances.val[i.val]?, l)` | the reference lookup (the balance at that account number if there is one, otherwise no value; the ledger left as it was) | 1 | agrees in 1 readings, 55 generated inputs | UNREVIEWED |
| l.ref_lookup_zero | domain | reference | the zero-default lookup | `L.refLookupZero` | `@[reducible] def refLookupZero : Frames.Term Ledger Usize (Option U64 × Ledger) := fun l i => (some (l.balances.val.getD i.val 0#u64), l)` | the zero-default lookup (the balance at that account number, and the value 0 if there is no such account; the ledger left as it was) | 1 | agrees in 1 readings, 55 generated inputs | UNREVIEWED |
| l.ref_whole_by_batch | domain | reference | the same batch applied transfer by transfer and kept only if every transfer is applied | `L.refWholeByBatch` | `@[reducible] def refWholeByBatch : Frames.Term Ledger (Slice Transfer) (Bool × Ledger) := fun l b => match applyBatch.run l b with \| some (n, l') => if n.val = b.val.length then (true, l') else (false, l) \| none => (false, l)` | the same batch applied transfer by transfer (the operation `apply_batch` of the same code) and kept only if every transfer is applied (accepted, with the ledger that leaves, if it applies every transfer of the batch; otherwise rejected, with the ledger left as it was) | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| l.ref_batch_by_transfers | domain | reference | its transfers applied one at a time until one is rejected | `L.refBatchByTransfers` | `@[reducible] def refBatchByTransfers : Frames.Term Ledger (Slice Transfer) (Usize × Ledger) := fun l b => let r := foldApply l b.val (if h : r.1 ≤ Usize.max then Usize.ofNatCore r.1 (by scalar_tac) else 0#usize, r.2)`<br>`def foldApply : Ledger → List Transfer → Nat × Ledger \| l, [] => (0, l) \| l, t :: ts => match apply.run l t with \| some (true, l') => ((foldApply l' ts).1 + 1, (foldApply l' ts).2) \| some (false, l') => (0, l') \| none => (0, l)` | its transfers applied one at a time, in order, until one is rejected (the operation `apply` of the same code, once per transfer; the answer is how many were accepted before the first rejection, and the ledger is the one those calls leave) | 1 | agrees in 1 readings, 297 generated inputs | UNREVIEWED |
| index_count | modifier | term<num> | (no surface of its own) | `{x}.val` | - | {x} | 2 | agrees in 2 readings, 26 generated inputs | UNREVIEWED |
| w.balance | domain | measure<num> | {w:wallet}'s balance; (plural) balances | `W.balance {w}` | `@[reducible] def balance (w : Wallet) : Nat := w.balance.val` | the balance of {w} | 15 | agrees in 15 readings, 40633 generated inputs | UNREVIEWED |
| w.maximum | domain | term<num> | the maximum | `W.maximum` | `@[reducible] def maximum : Nat := U64.max` | the largest balance a wallet can hold (2^64 - 1) | 5 | agrees in 5 readings, 23760 generated inputs | UNREVIEWED |
| w.succeeds | domain | class | the operation succeeds | `W.accepted ans` | `@[reducible] def accepted (r : Answer) : Prop := r = .Ok ()` | the answer is Ok | 6 | agrees in 6 readings, 23976 generated inputs | UNREVIEWED |
| w.rejected_with | domain | class | the operation is rejected with {e:error} | `W.rejectedWith {e} ans` | `@[reducible] def rejectedWith (e : WalletError) (r : Answer) : Prop := r = .Err e` | the answer is the error '{e}' | 5 | agrees in 5 readings, 16153 generated inputs | UNREVIEWED |
| i.holds | idiom | cond | {l:ledger} holds the balances {t:term<balances>} | means `is(l.ledger(l), t)` | - | (the reading of that composition) | 27 | n/a (an idiom adds no Lean and no Rust: it is its composition) | UNREVIEWED |
| i.moved | idiom | claim | the amount of {t:transfer} has moved between its accounts in {l:ledger} and no other balance changed | means `decreases_by(l.bal_of(l.sender(t), l), l.amount_of(t)); increases_by(l.bal_of(l.receiver(t), l), l.amount_of(t)); changes_only(l.accounts(l), [l.sender(t), l.receiver(t)])` | - | (the reading of that composition) | 2 | n/a (an idiom adds no Lean and no Rust: it is its composition) | UNREVIEWED |
| i.exactly_applied | idiom | claim | exactly {k:index} transfers are applied | means `result_is(l.applied(), index_count(k))` | - | (the reading of that composition) | 2 | n/a (an idiom adds no Lean and no Rust: it is its composition) | UNREVIEWED |
| g.subject | grammar | Rule line | a {op}; an {op}; every {op}; any {op} | - | - | every call of the operation (with every state and every input) | 45 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.role | grammar | Rule line | the {role} | - | - | the part of the state, or the input, that the operation gives that role | 31 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.rule_vp | grammar | Rule line | {subject} {vp} | - | - | what the Rule says of its subject | 34 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.rule_for | grammar | Rule line | for {subject}, {claim} | - | - | what a Then would say, said of the subject | 12 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.claims | grammar | Rule line | {claim} and {claim} | - | - | each claim is made of the same subject | 1 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.clauses | grammar | Rule line | {clause}, and {clause} | - | - | each clause is a rule of its own, with its own subject | 5 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| g.line | grammar | Rule line | {line} | - | - | the Rule line as written, up to the case of its first letter and a final full stop | 45 | n/a (words of the Rule line; no Lean and no Rust of their own) | UNREVIEWED |
| D1 | default | reading rule | (printed with the reading) | - | - | always answers: the call must return an answer for every input the reading applies to (no panic, no abort, no endless loop) | 80 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D2 | default | reading rule | (printed with the reading) | - | - | rejected calls are covered: the reading applies to every call, whether the operation accepts or rejects it | 80 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D3 | default | reading rule | (printed with the reading) | - | - | before / after one call: 'unchanged', 'increased by' and the like compare the state before one call with the state after it, not states in between | 34 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D4 | default | reading rule | (printed with the reading) | - | - | for all values: every outline <parameter>, every state and every input is universally quantified at the front; the Examples rows are instances | 83 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D5 | default | reading rule | (printed with the reading) | - | - | collection words bind inside their own clause: 'every', 'the first', 'no' range over the named collection within the one Given, Then or Rule clause they occur in | 13 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D6 | default | reading rule | (printed with the reading) | - | - | 'the first X of XS is P' requires that there is a first X | 2 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D7 | default | reading rule | (printed with the reading) | - | - | items are judged afterwards: in a Then about a collection read off the answer, each item is judged on the state after the call | 3 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D8 | default | reading rule | (printed with the reading) | - | - | conditions are read before the call: what 'assuming', 'for which', 'whenever', 'only if' and 'exactly when' say about the state is judged on the state before the call (of a sequence: before its first call), not on any state the call passes through or leaves | 53 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D9 | default | reading rule | (printed with the reading) | - | - | negation binds to the one condition it is written on: 'every X is not P' means that no X is P, never 'not every X is P' | 2 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| D10 | default | reading rule | (printed with the reading) | - | - | two calls are compared: the claim is about every pair of calls of the operation related as stated; both calls are in scope, the first is the one the words 'for the first call' speak of, and both must give an answer | 7 | n/a (a reading rule; what it says of the calls covered is compared with Lean through the coverage entries) | UNREVIEWED |
| calls.every | coverage | calls | (printed: every such call, accepted or rejected [default D2]) | `Frames.Calls.every` | `inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | every call in scope, accepted or rejected, and each must give an answer | 80 | n/a (printed text; compared with the Calls value Lean reports, `out/narrowing.json`) | UNREVIEWED |
| calls.accepted | coverage | calls | (printed: ONLY accepted calls [asked for]) | `Frames.Calls.accepted` | `inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | accepted calls only; a call that is rejected or gives no answer is not covered | 6 | n/a (printed text; compared with the Calls value Lean reports, `out/narrowing.json`) | UNREVIEWED |
| calls.rejected | coverage | calls | (printed: ONLY rejected calls [asked for]) | `Frames.Calls.rejected` | `inductive Calls where /-- every call in scope, accepted or rejected; and every such call must give an answer -/ \| every /-- only calls that give an answer that is accepted (asked for with "successful") -/ \| accepted /-- only calls that give an answer that is a rejection (asked for with "rejected") -/ \| rejected deriving DecidableEq, Repr`<br>`def Op.HoldsAt (op : Op σ α ρ) (Q : σ → α → ρ → σ → Prop) (s : σ) (a : α) : Prop := op.scope s a → match op.calls with \| .every    => ∃ r s', op.run s a = some (r, s') ∧ Q s a r s' \| .accepted => ∀ r s', op.run s a = some (r, s') → op.accepted r → Q s a r s' \| .rejected => ∀ r s', op.run s a = some (r, s') → ¬ op.accepted r → Q s a r s'`<br>`def Op.HoldsAt2 (op : Op σ α ρ) (rel : Variation σ α) (Q : ρ → σ → ρ → σ → Prop) (s : σ) (a : α) (s₂ : σ) (a₂ : α) : Prop := op.scope s a → op.scope s₂ a₂ → rel s a s₂ a₂ → match op.calls with \| .every    => ∃ r s' r₂ s₂', op.run s a = some (r, s') ∧ op.run s₂ a₂ = some (r₂, s₂') ∧ Q r s' r₂ s₂' \| .accepted => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → op.accepted r → op.accepted r₂ → Q r s' r₂ s₂' \| .rejected => ∀ r s' r₂ s₂', op.run s a = some (r, s') → op.run s₂ a₂ = some (r₂, s₂') → ¬ op.accepted r → ¬ op.accepted r₂ → Q r s' r₂ s₂'` | rejected calls only; a call that is accepted or gives no answer is not covered | 7 | n/a (printed text; compared with the Calls value Lean reports, `out/narrowing.json`) | UNREVIEWED |

116 of 116 entries are unreviewed. Record a review with `python3 -m clausal review <id|all> --reviewer <name>` (piece ids and the ids of the old glossary are both accepted).

**What a person has to sign:** 116 entries (93 pieces: 8 operations, 32 other domain words, 28 modifiers, 25 frames; 3 idioms; 3 coverage entries, the lines printed about which calls a claim covers; 7 grammar entries, the words that put a Rule line together; and 10 defaults, the reading rules). A new sentence built from them adds none. **Rust readings compared in this run:** 93 of 93 pieces, through the compiled readings that use them; not compared: none.

## Narrowed claims: vacuity and printed coverage (plan nodes Q1, Q2)

A claim narrowed to accepted calls (`successful`, `if it is accepted`) or to rejected calls covers only the calls that give an answer of that kind. **A narrowed Rule clause whose claim follows from the narrowing alone is refused** (`SAYS-NOTHING`): it would hold of every possible operation, so no code could break it. The compiler decides from what narrowing settles about each operation's answers (`narrowing:` in the operation's entry, `clausebook/local/`) and names a theorem of `lean/Frames/Narrowing.lean`; what follows is what Lean said about that in this run (`lean/Run/Narrowing.lean`).

- **Declared facts:** 24 lines of `narrowing:` kernel-checked; the 35 lines that could have been written and were not were each attempted with the same fixed tactic and are not provable by it.
- **Refused controls** (`controls/narrowing.feature`): 12 sentences refused; compiled without the refusal, their 12 narrowed claims are kernel-checked to hold for every `run`, each through the theorem its refusal names.
- **Not refused:** 20 narrowed claims (12 in the fixture Rules, the rest in the 8 controls that must compile). The fixed tactic `vacuous_by_narrowing` fails on each: none is shown to hold of every operation. This is proof search, not a proof that each says something.
- **Printed coverage:** Lean reported the `Frames.Calls` value of 147 of 147 claims in 103 compiled readings (38 scenarios and 45 Rule lines of the fixtures, 20 control lines). The coverage lines printed for a reading differ from the lines the book gives for those values in **0** readings. The lines compared are the `covers` slot, the answer requirement, the note of a sequence (8 claims are about a sequence according to Lean: their operation mentions `Frames.Op.andThen`), the note of two compared calls, and the stated weakenings.
- **Narrowed twice:** 6 control sentences narrow or scope one clause with more than one word (two of successful / rejected / internal on the subject, a narrowed subject and `if it is ...` on its claim, or two `if it is ...`). Each is refused (`UNSUPPORTED`, code `NARROWED-TWICE`): a word is never dropped and never overrides another.
- **Must-fail attempts count only if their statement was read.** A theorem whose script fails is reported `notproved`; one whose statement does not elaborate is reported `badstatement` and fails the run. One statement broken on purpose checks the report itself on every run. Statements that did not elaborate, other than that one: **0**.

Coverage lines, by `Frames.Calls` value (entries `coverage:` of the Clausebook, signed like any other entry):

- **every** (`calls.every`): every such call, accepted or rejected [default D2]. Of a sequence: (of a sequence: every call in it must answer; the answer spoken of is the LAST call's)
- **accepted** (`calls.accepted`): ONLY accepted calls [asked for]. Of a sequence: (of a sequence: ONLY sequences in which every call gives an answer and the LAST call is accepted are covered; a sequence in which any call gives no answer, or whose last call is rejected, is outside this clause; the answer spoken of is the LAST call's, and whether an earlier call was accepted or rejected is not looked at)
- **rejected** (`calls.rejected`): ONLY rejected calls [asked for]. Of a sequence: (of a sequence: ONLY sequences in which every call gives an answer and the LAST call is rejected are covered; a sequence in which any call gives no answer, or whose last call is accepted, is outside this clause; the answer spoken of is the LAST call's, and whether an earlier call was accepted or rejected is not looked at)

## Regression: every old statement against its new reading (plan node V3)

Each scenario has two Lean statements: the **reading** compiled from the composable Clausebook (`lean/Wallet/Readings.lean`) and the **flat statement** of the old whole-phrase glossary (`lean/Wallet/Statements.lean`, unchanged; every hand-written proof is about it). A generated theorem `<id>.reading_iff : <id>.reading ↔ <id>.stmt` is checked by Lean's kernel, and the audit checks that its type is exactly that (`lean/Run/Links.lean`, `lean/Bdd/AuditLinks.lean`). So a verdict is carried from the old statement to the new one by an equivalence, not by getting the same answer twice; a reading whose equivalence is missing gets the verdict UNLINKED.

| Scenario | Old glossary entries | New pieces | Idioms needed | NEW ↔ OLD | Axioms | Reading non-vacuous |
|---|---|---|---|---|---|---|
| `wallet.transfer_conserves` | 8 | 21 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_short` | 5 | 15 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_no_room` | 6 | 17 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_short_example` | 4 | 14 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.withdraw_covered` | 5 | 15 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.withdraw_too_much` | 5 | 15 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.deposit_with_room` | 5 | 16 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.deposit_overflow` | 5 | 16 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `wallet.transfer_always_succeeds` | 6 | 18 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_conserves` | 3 | 14 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_stops_at_invalid` | 3 | 17 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.two_batches_conserve` | 4 | 18 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_first_invalid` | 5 | 21 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_count_bounded` | 3 | 13 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_example_all` | 4 | 14 | i.holds, i.exactly_applied | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_example_stop` | 4 | 14 | i.holds, i.exactly_applied | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_all_valid_all_applied` | 4 | 17 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.transfer_valid_moves` | 6 | 27 | i.holds, i.moved | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.transfer_invalid_rejected` | 5 | 19 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_is_sum` | 4 | 16 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_overflow` | 4 | 18 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.total_always_available` | 3 | 12 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.balance_of_account` | 4 | 14 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.balance_no_account` | 4 | 15 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_rejected_unchanged` | 3 | 15 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_first_invalid` | 5 | 21 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_conserves` | 3 | 14 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_accept` | 4 | 13 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_rollback_late` | 4 | 15 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.whole_example_rollback` | 4 | 15 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_then_total` | 5 | 18 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `ledger.batch_then_total_overflow` | 5 | 20 | i.holds | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |
| `negative_controls.contradictory_givens` | 5 | 14 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | n/a (the Givens contradict each other) |
| `negative_controls.bystander_unchanged` | 5 | 17 | - | **equivalent** (kernel-checked) | propext, Classical.choice, Quot.sound | kernel-checked |

**34 of 34** readings are proved equivalent to their old statement. **None is a deliberate strengthening**: the old statements were already fail-closed (each said the call returns, for every input satisfying the Givens), so the defaults change nothing at scenario level. The defaults do bite at the level of the `Rule:` lines, which had no statement before: each rule statement covers every input, and is proved FROM its scenarios (see each rule's block).

## New sentences, end to end

A NEW sentence is a scenario or a `Rule:` line that the composable Clausebook reads and that has NO entry in the old whole-phrase glossary, no hand-written cucumber step and no hand-written Rust predicate. What each one gets, from the pieces alone:

- **a reading** (the composition, type-checked by Lean) and its **echo**;
- **a run on the compiled Rust**: Examples rows through the one generic cucumber step, and the reading itself at every point of its grid of generated inputs, both evaluated by the per-piece Rust readings;
- **a flat proof obligation** generated from the `flat:` template of each frame (`lean/Wallet/Obligations.lean`), tied to the reading by a generated, kernel-checked equivalence, and a proof stub;
- **a verdict**: PROVED-FOR-ALL when a proof of the obligation has been supplied (here: by an agent), TESTED-ONLY while the stub is `sorry`, REFUTED when the search finds an input at which the reading is false and the kernel confirms it there.

| Sentence | Kind | Pieces | Verdict | How | Examples on Rust | Generated inputs: Rust = model | Obligation ↔ reading |
|---|---|---|---|---|---|---|---|
| a transfer between two accounts of the ledger (`features/ledger_rules.feature:17`) | scenario | 15 | **PROVED-FOR-ALL** | supplied proof of the obligation | 2 of 2 | 1452 of 1452 at 726 inputs | kernel-checked |
| a transfer of more than the sender holds is rejected and changes nothing (`features/ledger_rules.feature:35`) | scenario | 21 | **PROVED-FOR-ALL** | supplied proof of the obligation | 3 of 3 | 2178 of 2178 at 726 inputs | kernel-checked |
| after a batch the total of all balances is within the maximum (`features/ledger_rules.feature:56`) | scenario | 15 | **REFUTED** | kernel refutation at the counterexample | 2 of 2 | 6534 of 6534 at 3267 inputs | kernel-checked |
| A rejected transfer leaves every single balance as it was (`features/ledger_rules.feature:176`) | scenario | 22 | **PROVED-FOR-ALL** | supplied proof of the obligation | 2 of 2 | 14520 of 14520 at 3630 inputs | kernel-checked |
| An internal fund transfer never changes the aggregate account value of the ledger (`features/ledger_rules.feature:14`) | Rule | 15 | **PROVED-FOR-ALL** | from its scenarios | - | 132 of 132 at 66 inputs | kernel-checked |
| An internal transfer never changes the total of all balances of the ledger (`features/ledger_rules.feature:29`) | Rule | 15 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 132 of 132 at 66 inputs | kernel-checked |
| A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger (`features/ledger_rules.feature:32`) | Rule | 16 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 132 of 132 at 66 inputs | kernel-checked |
| For a lookup for which the account is not an account of the ledger, there is no result (`features/ledger_rules.feature:49`) | Rule | 16 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 110 of 110 at 55 inputs | kernel-checked |
| A batch never leaves the total of all balances of the ledger above the maximum (`features/ledger_rules.feature:52`) | Rule | 13 | **REFUTED** | kernel refutation at the counterexample (refuted) | - | 594 of 594 at 297 inputs | kernel-checked |
| For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards (`features/ledger_rules.feature:67`) | Rule | 16 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| A transfer never loses acceptance when the amount is smaller (`features/ledger_rules.feature:72`) | Rule | 12 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 13068 of 13068 at 4356 inputs | kernel-checked |
| A transfer never loses acceptance when the amount is larger (`features/ledger_rules.feature:75`) | Rule | 12 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 13068 of 13068 at 4356 inputs | kernel-checked |
| A lookup never loses that there is a result when the ledger is extended (`features/ledger_rules.feature:78`) | Rule | 12 | **TESTED-ONLY** | no proof supplied (stub is `sorry`) | - | 9075 of 9075 at 3025 inputs | kernel-checked |
| A lookup agrees with the reference lookup (`features/ledger_rules.feature:84`) | Rule | 10 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 110 of 110 at 55 inputs | kernel-checked |
| A lookup agrees with the zero-default lookup (`features/ledger_rules.feature:87`) | Rule | 10 | **REFUTED** | kernel refutation at the counterexample (refuted) | - | 110 of 110 at 55 inputs | kernel-checked |
| A lookup gives the same answer when the ledger agrees at the account (`features/ledger_rules.feature:91`) | Rule | 11 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 9075 of 9075 at 3025 inputs | kernel-checked |
| A transfer gives the same answer when only the amount differs (`features/ledger_rules.feature:94`) | Rule | 11 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 13068 of 13068 at 4356 inputs | kernel-checked |
| A transfer gives the same answer when the amount is larger, if it is rejected (`features/ledger_rules.feature:98`) | Rule | 13 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 13068 of 13068 at 4356 inputs | kernel-checked |
| A transfer gives the same answer when the amount is larger, if it is accepted (`features/ledger_rules.feature:101`) | Rule | 12 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 13068 of 13068 at 4356 inputs | kernel-checked |
| For a batch, every transfer at which the batch stopped is a transfer of the batch (`features/ledger_rules.feature:105`) | Rule | 13 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| For a batch, every transfer of the batch is a transfer at which the batch stopped (`features/ledger_rules.feature:108`) | Rule | 13 | **REFUTED** | kernel refutation at the counterexample (refuted) | - | 594 of 594 at 297 inputs | kernel-checked |
| A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger (`features/ledger_rules.feature:112`) | Rule | 19 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected (`features/ledger_rules.feature:115`) | Rule | 18 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 594 of 594 at 297 inputs | kernel-checked |
| A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied (`features/ledger_rules.feature:123`) | Rule | 10 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| A batch agrees with its transfers applied one at a time until one is rejected (`features/ledger_rules.feature:126`) | Rule | 10 | **TESTED-ONLY** | no proof supplied (stub is `sorry`) | - | 594 of 594 at 297 inputs | kernel-checked |
| A transfer never leaves the balance of account 4 of the ledger above zero (`features/ledger_rules.feature:137`) | Rule | 13 | **REFUTED** | kernel refutation at the counterexample (refuted) | - | 132 of 132 at 66 inputs | kernel-checked |
| A successful transfer never changes the ledger (`features/ledger_rules.feature:141`) | Rule | 11 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 132 of 132 at 66 inputs | kernel-checked |
| For a rejected transfer, the total of all balances of the ledger is now zero (`features/ledger_rules.feature:144`) | Rule | 12 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 132 of 132 at 66 inputs | kernel-checked |
| A batch followed by a computation of the total is always accepted (`features/ledger_rules.feature:147`) | Rule | 12 | **REFUTED** | kernel refutation at the counterexample (refuted2) | - | 594 of 594 at 297 inputs | kernel-checked |
| A transfer is accepted whenever the transfer is valid on the ledger (`features/ledger_rules.feature:154`) | Rule | 15 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 132 of 132 at 66 inputs | kernel-checked |
| A transfer for which the transfer is not valid on the ledger is rejected and changes nothing (`features/ledger_rules.feature:157`) | Rule | 17 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 132 of 132 at 66 inputs | kernel-checked |
| For a batch, the number of transfers applied is at least the length of the batch (`features/ledger_rules.feature:160`) | Rule | 12 | **REFUTED** | kernel refutation at the counterexample (refuted) | - | 594 of 594 at 297 inputs | kernel-checked |
| A batch never leaves the total of all balances of the ledger below zero (`features/ledger_rules.feature:163`) | Rule | 13 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| For a batch, no transfer at which the batch stopped is valid on the ledger afterwards (`features/ledger_rules.feature:166`) | Rule | 14 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero (`features/ledger_rules.feature:169`) | Rule | 18 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 594 of 594 at 297 inputs | kernel-checked |
| A successful transfer never changes the total of all balances of the ledger (`features/ledger_rules.feature:172`) | Rule | 12 | **PROVED-FOR-ALL** | by a supplied proof of its obligation | - | 132 of 132 at 66 inputs | kernel-checked |

4 new scenarios and 32 new Rule lines: 21 PROVED-FOR-ALL, 13 REFUTED, 2 TESTED-ONLY. A flat obligation is generated for every Rule line as well as for the new scenarios: 49 of 49 are proved equivalent to their reading (kernel-checked; the audit checks the type of each and that its proof uses no proof of either side). The proofs of the obligations were written by an agent, from the hand-proved step lemmas of `lean/Ledger/Lemmas/`; one true rule is deliberately left with its generated stub to show the TESTED-ONLY state.

<details><summary>The flat proof obligation of each new sentence (<code>lean/Wallet/Obligations.lean</code>)</summary>

**a transfer between two accounts of the ledger**

```lean
def Spec.ledger_rules.readme_transfer_keeps_aggregate.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

**a transfer of more than the sender holds is rejected and changes nothing**

```lean
def Spec.ledger_rules.n2_short_sender_rejected.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ((L.bal st (L.sender inp)) < (L.amountOf inp)) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (¬ ((L.said ans))) ∧ ((L.balances st') = (L.balances st)))
```

**after a batch the total of all balances is within the maximum**

```lean
def Spec.ledger_rules.n4_total_within_maximum_after_batch.obligation : Prop :=
  (∀ (balances : List U64) (st : ledger.Ledger) (inp : Slice ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) ≤ L.maximum))
```

**A rejected transfer leaves every single balance as it was**

```lean
def Spec.ledger_rules.f_other_account_untouched.obligation : Prop :=
  (∀ (balances : List U64) (k : Usize) (st : ledger.Ledger) (inp : ledger.Transfer), ((L.balances st) = balances) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ True ∧ (¬ L.said ans → (L.bal st' k.val) = (L.bal st k.val)) ∧ (L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

**Rule: An internal fund transfer never changes the aggregate account value of the ledger**

```lean
def Rule.ledger_rules.readme_internal_transfers.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), (∀ p ∈ L.parties inp, L.isAccount st p) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

**Rule: An internal transfer never changes the total of all balances of the ledger**

```lean
def Rule.ledger_rules.n1_internal_transfer.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), (∀ p ∈ L.parties inp, L.isAccount st p) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

**Rule: A transfer is accepted only if the amount of the transfer is not more than the balance of account the sender of the transfer of the ledger**

```lean
def Rule.ledger_rules.n2_accepted_only_if_covered.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((L.said ans) → (((L.amountOf inp) ≤ (L.bal st (L.sender inp))))))
```

**Rule: For a lookup for which the account is not an account of the ledger, there is no result**

```lean
def Rule.ledger_rules.n3_lookup_missing_account.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Usize), (¬ ((L.isAccount st inp))) → ∃ (ans : Option U64) (st' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ (¬ ((L.found ans))))
```

**Rule: A batch never leaves the total of all balances of the ledger above the maximum**

```lean
def Rule.ledger_rules.n4_total_stays_within_maximum.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) ≤ L.maximum))
```

**Rule: For a batch, every transfer at which the batch stopped is not valid on the ledger afterwards**

```lean
def Rule.ledger_rules.n5_stopped_at_invalid.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (∀ x ∈ (L.stoppedAt inp ans), (¬ ((L.valid st' x)))))
```

**Rule: A transfer never loses acceptance when the amount is smaller**

```lean
def Rule.ledger_rules.mono_smaller_amount.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.smallerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((L.said ans) → (L.said ans2)))
```

**Rule: A transfer never loses acceptance when the amount is larger**

```lean
def Rule.ledger_rules.mono_larger_amount.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.largerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((L.said ans) → (L.said ans2)))
```

**Rule: A lookup never loses that there is a result when the ledger is extended**

```lean
def Rule.ledger_rules.mono_extended_ledger.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Usize) (st2 : ledger.Ledger) (inp2 : Usize), L.extended st inp st2 inp2 → ∃ (ans : Option U64) (st' : ledger.Ledger) (ans2 : Option U64) (st2' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ (ledger.Ledger.balance st2 inp2 = ok ans2 ∧ st2' = st2) ∧ ((L.found ans) → (L.found ans2)))
```

**Rule: A lookup agrees with the reference lookup**

```lean
def Rule.ledger_rules.agrees_reference_lookup.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Usize), ∃ (ans : Option U64) (st' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ ((ans, st') = L.refLookup st inp))
```

**Rule: A lookup agrees with the zero-default lookup**

```lean
def Rule.ledger_rules.agrees_zero_default.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Usize), ∃ (ans : Option U64) (st' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ ((ans, st') = L.refLookupZero st inp))
```

**Rule: A lookup gives the same answer when the ledger agrees at the account**

```lean
def Rule.ledger_rules.same_answer_at_account.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Usize) (st2 : ledger.Ledger) (inp2 : Usize), L.agreesAtAccount st inp st2 inp2 → ∃ (ans : Option U64) (st' : ledger.Ledger) (ans2 : Option U64) (st2' : ledger.Ledger), (ledger.Ledger.balance st inp = ok ans ∧ st' = st) ∧ (ledger.Ledger.balance st2 inp2 = ok ans2 ∧ st2' = st2) ∧ (ans = ans2))
```

**Rule: A transfer gives the same answer when only the amount differs**

```lean
def Rule.ledger_rules.same_answer_any_amount.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.onlyAmountDiffers st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ (ans = ans2))
```

**Rule: A transfer gives the same answer when the amount is larger, if it is rejected**

```lean
def Rule.ledger_rules.rejected_stays_rejected.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.largerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((¬ ((L.said ans))) → ans = ans2))
```

**Rule: A transfer gives the same answer when the amount is larger, if it is accepted**

```lean
def Rule.ledger_rules.accepted_stays_accepted.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer) (st2 : ledger.Ledger) (inp2 : ledger.Transfer), L.largerAmount st inp st2 inp2 → ∃ (ans : Bool) (st' : ledger.Ledger) (ans2 : Bool) (st2' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (ledger.Ledger.apply st2 inp2 = ok (ans2, st2')) ∧ ((L.said ans) → ans = ans2))
```

**Rule: For a batch, every transfer at which the batch stopped is a transfer of the batch**

```lean
def Rule.ledger_rules.stopped_is_of_batch.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (∀ x ∈ (L.stoppedAt inp ans), x ∈ (L.transfers inp)))
```

**Rule: For a batch, every transfer of the batch is a transfer at which the batch stopped**

```lean
def Rule.ledger_rules.batch_is_stopped.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (∀ x ∈ (L.transfers inp), x ∈ (L.stoppedAt inp ans)))
```

**Rule: A batch for which some transfer of the batch is valid on the ledger never changes the total of all balances of the ledger**

```lean
def Rule.ledger_rules.some_valid_conserves.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), (Frames.someOf ((L.transfers inp)) (fun x => (L.valid st x))) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))
```

**Rule: A batch applied as a whole for which some transfer of the batch is not valid on the ledger is always rejected**

```lean
def Rule.ledger_rules.some_invalid_rejected.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), (Frames.someOf ((L.transfers inp)) (fun x => (¬ ((L.valid st x))))) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply_all st inp = ok (ans, st')) ∧ (¬ ((L.said ans))))
```

**Rule: A batch applied as a whole agrees with the same batch applied transfer by transfer and kept only if every transfer is applied**

```lean
def Rule.ledger_rules.k2_whole_agrees_with_batch.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply_all st inp = ok (ans, st')) ∧ ((ans, st') = L.refWholeByBatch st inp))
```

**Rule: A batch agrees with its transfers applied one at a time until one is rejected**

```lean
def Rule.ledger_rules.k2_batch_agrees_with_transfers.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((ans, st') = L.refBatchByTransfers st inp))
```

**Rule: A transfer never leaves the balance of account 4 of the ledger above zero**

```lean
def Rule.ledger_rules.e1_fifth_account_empty.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ ((L.bal st' (4#usize).val) ≤ 0))
```

**Rule: A successful transfer never changes the ledger**

```lean
def Rule.ledger_rules.successful_changes_nothing.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∀ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) → (L.said ans → (L.balances st') = (L.balances st)))
```

**Rule: For a rejected transfer, the total of all balances of the ledger is now zero**

```lean
def Rule.ledger_rules.rejected_empties_ledger.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∀ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) → (¬ L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = 0))
```

**Rule: A batch followed by a computation of the total is always accepted**

```lean
def Rule.ledger_rules.batch_then_total_always.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : (Slice ledger.Transfer) × Unit), ∃ (ans : Option U64) (st' : ledger.Ledger), (∃ r_1 s_1, (ledger.Ledger.apply_batch st inp.1 = ok (r_1, s_1)) ∧ (ledger.Ledger.total s_1 = ok ans ∧ st' = s_1)) ∧ ((L.found ans)))
```

**Rule: A transfer is accepted whenever the transfer is valid on the ledger**

```lean
def Rule.ledger_rules.f_if_then.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (((L.valid st inp)) → (L.said ans)))
```

**Rule: A transfer for which the transfer is not valid on the ledger is rejected and changes nothing**

```lean
def Rule.ledger_rules.f_rejected_unchanged.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), (¬ ((L.valid st inp))) → ∃ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) ∧ (¬ (L.said ans) ∧ st' = st))
```

**Rule: For a batch, the number of transfers applied is at least the length of the batch**

```lean
def Rule.ledger_rules.f_result_at_least.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((L.length inp) ≤ (L.applied ans)))
```

**Rule: A batch never leaves the total of all balances of the ledger below zero**

```lean
def Rule.ledger_rules.f_at_least.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (0 ≤ (Frames.aggregate (((L.balances st').map L.amount)))))
```

**Rule: For a batch, no transfer at which the batch stopped is valid on the ledger afterwards**

```lean
def Rule.ledger_rules.f_none_of.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ (∀ x ∈ (L.stoppedAt inp ans), ¬ ((L.valid st' x))))
```

**Rule: For a batch for which no transfer of the batch is valid on the ledger, the number of transfers applied is zero**

```lean
def Rule.ledger_rules.f_no_valid_none_applied.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : Slice ledger.Transfer), (Frames.noneOf ((L.transfers inp)) (fun x => (L.valid st x))) → ∃ (ans : Usize) (st' : ledger.Ledger), (ledger.Ledger.apply_batch st inp = ok (ans, st')) ∧ ((L.applied ans) = 0))
```

**Rule: A successful transfer never changes the total of all balances of the ledger**

```lean
def Rule.ledger_rules.f_scenario_level.obligation : Prop :=
  (∀ (st : ledger.Ledger) (inp : ledger.Transfer), ∀ (ans : Bool) (st' : ledger.Ledger), (ledger.Ledger.apply st inp = ok (ans, st')) → (L.said ans → (Frames.aggregate (((L.balances st').map L.amount))) = (Frames.aggregate (((L.balances st).map L.amount)))))

```

</details>

## The old whole-phrase glossary (the flat statements and the Rust steps)

NO LONGER the link from English to Lean: that is the Clausebook above. These entries are what the flat statements of the OLDER scenarios are written with (each proved equivalent to its reading). The cucumber steps are no longer keyed by them (a step is the composition tree of its pieces), and a NEW sentence needs no entry here. Each English phrase and the one Lean definition (or model function) it is bound to: `glossary.yaml`, `lean/Wallet/Vocab.lean` and `lean/Ledger/Vocab.lean`. The last column compares that Lean definition with a second, independently written reading of the same phrase (the whole-phrase Rust predicate in `wallet-bdd/src/lib.rs`) on a grid of arguments. Agreement does not show that either reading matches the English; disagreement shows that one of them is wrong.

| Id | Kind | English phrase | Lean | Definition | Sign-off | Lean vs Rust reading |
|---|---|---|---|---|---|---|
| G-balance | given | {wallet:w}'s balance is {amount:n} | `Vocab.hasBalance` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance = n` | UNREVIEWED | agree on 36 of 36 |
| G-covers | given | {amount:n} is not more than {wallet:w}'s balance | `Vocab.covers` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := n.val ≤ w.balance.val` | UNREVIEWED | agree on 36 of 36 |
| G-exceeds | given | {amount:n} is more than {wallet:w}'s balance | `Vocab.exceeds` applied to `n, pre(w)` | `(n : U64) (w : Wallet) : Prop := w.balance.val < n.val` | UNREVIEWED | agree on 36 of 36 |
| G-room | given | {wallet:w}'s balance plus {amount:n} does not exceed the maximum | `Vocab.roomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := w.balance.val + n.val ≤ U64.max` | UNREVIEWED | agree on 36 of 36 |
| G-noroom | given | {wallet:w}'s balance plus {amount:n} exceeds the maximum | `Vocab.noRoomFor` applied to `pre(w), n` | `(w : Wallet) (n : U64) : Prop := U64.max < w.balance.val + n.val` | UNREVIEWED | agree on 36 of 36 |
| W-transfer | when | {wallet:src} transfers {amount:n} to {wallet:dst} | `wallet.transfer` applied to `pre(src), pre(dst), n` | Aeneas-generated model of Rust `wallet::transfer`; returns `outcome, post(src), post(dst)` | UNREVIEWED | n/a (the step calls the real function) |
| W-deposit | when | {wallet:w} deposits {amount:n} | `wallet.Wallet.deposit` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::deposit`; returns `outcome, post(w)` | UNREVIEWED | n/a (the step calls the real function) |
| W-withdraw | when | {wallet:w} withdraws {amount:n} | `wallet.Wallet.withdraw` applied to `pre(w), n` | Aeneas-generated model of Rust `wallet::{wallet::Wallet}::withdraw`; returns `outcome, post(w)` | UNREVIEWED | n/a (the step calls the real function) |
| T-ok | then | the operation succeeds | `Vocab.succeeds` applied to `outcome` | `(o : Outcome) : Prop := o = .Ok ()` | UNREVIEWED | agree on 3 of 3 |
| T-err | then | the operation is rejected with {error:e} | `Vocab.rejectedWith` applied to `outcome, e` | `(o : Outcome) (e : WalletError) : Prop := o = .Err e` | UNREVIEWED | agree on 6 of 6 |
| T-dec | then | {wallet:w}'s balance is decreased by {amount:n} | `Vocab.decreasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val + n.val = pre.balance.val` | UNREVIEWED | agree on 216 of 216 |
| T-inc | then | {wallet:w}'s balance is increased by {amount:n} | `Vocab.increasedBy` applied to `pre(w), post(w), n` | `(pre post : Wallet) (n : U64) : Prop := post.balance.val = pre.balance.val + n.val` | UNREVIEWED | agree on 216 of 216 |
| T-same | then | {wallet:w}'s balance is unchanged | `Vocab.unchanged` applied to `pre(w), post(w)` | `(pre post : Wallet) : Prop := post = pre` | UNREVIEWED | agree on 36 of 36 |
| T-total | then | the total of all balances is unchanged | `Vocab.totalUnchanged` applied to `all_pre(wallet), all_post(wallet)` | `(pre post : List Wallet) : Prop := (post.map (·.balance.val)).sum = (pre.map (·.balance.val)).sum` | UNREVIEWED | agree on 1296 of 1296 |
| LG-holds | given | ledger {ledger:l} holds the balances {balances:bs} | `LVocab.holds` applied to `pre(l), bs` | `(l : Ledger) (bs : List U64) : Prop := l.balances.val = bs` | UNREVIEWED | agree on 121 of 121 |
| LG-sums-to | given | the total of the balances of ledger {ledger:l} is {amount:s} | `LVocab.sumsTo` applied to `pre(l), s` | `(l : Ledger) (s : U64) : Prop := total l = s.val` | UNREVIEWED | agree on 66 of 66 |
| LG-sum-too-big | given | the total of the balances of ledger {ledger:l} is more than the maximum | `LVocab.sumTooBig` applied to `pre(l)` | `(l : Ledger) : Prop := U64.max < total l` | UNREVIEWED | agree on 11 of 11 |
| LG-account | given | {index:i} is an account of ledger {ledger:l} | `LVocab.isAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := i.val < l.balances.val.length` | UNREVIEWED | agree on 55 of 55 |
| LG-no-account | given | {index:i} is not an account of ledger {ledger:l} | `LVocab.notAccount` applied to `pre(l), i` | `(l : Ledger) (i : Usize) : Prop := l.balances.val.length ≤ i.val` | UNREVIEWED | agree on 55 of 55 |
| LG-valid | given | the transfer {transfer:t} is valid on ledger {ledger:l} | `LVocab.validOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := valid l t` | UNREVIEWED | agree on 66 of 66 |
| LG-invalid | given | the transfer {transfer:t} is not valid on ledger {ledger:l} | `LVocab.invalidOn` applied to `pre(l), t` | `(l : Ledger) (t : Transfer) : Prop := ¬ valid l t` | UNREVIEWED | agree on 66 of 66 |
| LG-first-invalid | given | the first transfer of {batch:b} is not valid on ledger {ledger:l} | `LVocab.firstInvalid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := b.val ≠ [] ∧ ∀ t ∈ b.val.head?, ¬ valid l t` | UNREVIEWED | agree on 297 of 297 |
| LG-all-valid | given | every transfer of {batch:b} is valid on ledger {ledger:l} | `LVocab.allValid` applied to `pre(l), b` | `(l : Ledger) (b : Slice Transfer) : Prop := ∀ t ∈ b.val, valid l t` | UNREVIEWED | agree on 297 of 297 |
| LW-batch | when | the batch {batch:b} is applied to ledger {ledger:l} | `ledger.Ledger.apply_batch` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_batch`; returns `outcome, post(l)` | UNREVIEWED | n/a (the step calls the real function) |
| LW-whole | when | the batch {batch:b} is applied to ledger {ledger:l} as a whole | `ledger.Ledger.apply_all` applied to `pre(l), b` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply_all`; returns `outcome, post(l)` | UNREVIEWED | n/a (the step calls the real function) |
| LW-transfer | when | the transfer {transfer:t} is applied to ledger {ledger:l} | `ledger.Ledger.apply` applied to `pre(l), t` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::apply`; returns `outcome, post(l)` | UNREVIEWED | n/a (the step calls the real function) |
| LW-total | when | the total of ledger {ledger:l} is computed | `ledger.Ledger.total` applied to `pre(l)` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::total`; returns `outcome` | UNREVIEWED | n/a (the step calls the real function) |
| LW-balance | when | the balance of account {index:i} of ledger {ledger:l} is looked up | `ledger.Ledger.balance` applied to `pre(l), i` | Aeneas-generated model of Rust `ledger::{ledger::Ledger}::balance`; returns `outcome` | UNREVIEWED | n/a (the step calls the real function) |
| LT-total-same | then | the total of ledger {ledger:l}'s balances is unchanged | `LVocab.totalUnchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := total post = total pre` | UNREVIEWED | agree on 121 of 121 |
| LT-same | then | ledger {ledger:l} is unchanged | `LVocab.unchanged` applied to `pre(l), post(l)` | `(pre post : Ledger) : Prop := post.balances.val = pre.balances.val` | UNREVIEWED | agree on 121 of 121 |
| LT-now-holds | then | ledger {ledger:l} is now {balances:bs} | `LVocab.nowHolds` applied to `post(l), bs` | `(post : Ledger) (bs : List U64) : Prop := post.balances.val = bs` | UNREVIEWED | agree on 121 of 121 |
| LT-at-most | then | the number of transfers applied is at most the length of {batch:b} | `LVocab.appliedAtMost` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val ≤ b.val.length` | UNREVIEWED | agree on 135 of 135 |
| LT-none-applied | then | the number of transfers applied is zero | `LVocab.appliedNone` applied to `outcome` | `(n : Usize) : Prop := n.val = 0` | UNREVIEWED | agree on 5 of 5 |
| LT-all-applied | then | the number of transfers applied is the length of {batch:b} | `LVocab.appliedAll` applied to `outcome, b` | `(n : Usize) (b : Slice Transfer) : Prop := n.val = b.val.length` | UNREVIEWED | agree on 135 of 135 |
| LT-exactly | then | exactly {index:k} transfers are applied | `LVocab.appliedExactly` applied to `outcome, k` | `(n : Usize) (k : Usize) : Prop := n = k` | UNREVIEWED | agree on 25 of 25 |
| LT-stops-at-invalid | then | every transfer at which {batch:b} stopped is not valid on ledger {ledger:l} afterwards | `LVocab.stopsAtInvalid` applied to `outcome, b, post(l)` | `(n : Usize) (b : Slice Transfer) (post : Ledger) : Prop := ∀ t ∈ b.val[n.val]?, ¬ valid post t` | UNREVIEWED | agree on 1485 of 1485 |
| LT-same-if-rejected | then | if it is rejected, ledger {ledger:l} is unchanged | `LVocab.unchangedIfRejected` applied to `outcome, pre(l), post(l)` | `(ok : Bool) (pre post : Ledger) : Prop := ok = false → post.balances.val = pre.balances.val` | UNREVIEWED | agree on 242 of 242 |
| LT-result | then | the result is {amount:s} | `LVocab.resultIs` applied to `outcome, s` | `(o : Option U64) (s : U64) : Prop := o = some s` | UNREVIEWED | agree on 30 of 30 |
| LT-no-result | then | there is no result | `LVocab.noResult` applied to `outcome` | `(o : Option U64) : Prop := o = none` | UNREVIEWED | agree on 5 of 5 |
| LT-some-result | then | there is a result | `LVocab.someResult` applied to `outcome` | `(o : Option U64) : Prop := o ≠ none` | UNREVIEWED | agree on 5 of 5 |
| LT-balance | then | the result is the balance of account {index:i} of ledger {ledger:l} | `LVocab.resultIsBalance` applied to `outcome, pre(l), i` | `(o : Option U64) (l : Ledger) (i : Usize) : Prop := o = l.balances.val[i.val]? ∧ o ≠ none` | UNREVIEWED | agree on 275 of 275 |
| LT-accepted | then | it is accepted | `LVocab.accepted` applied to `outcome` | `(ok : Bool) : Prop := ok = true` | UNREVIEWED | agree on 2 of 2 |
| LT-rejected | then | it is rejected | `LVocab.rejected` applied to `outcome` | `(ok : Bool) : Prop := ok = false` | UNREVIEWED | agree on 2 of 2 |
| LT-moved | then | the amount of {transfer:t} has moved between its accounts in ledger {ledger:l} and no other balance changed | `LVocab.moved` applied to `pre(l), post(l), t` | `(pre post : Ledger) (t : Transfer) : Prop := post.balances.val.length = pre.balances.val.length ∧ bal post t.from.val + t.amount.val = bal pre t.from.val ∧ bal post t.to.val = bal pre t.to.val + t.amount.val ∧ ∀ k < pre.balances.val.length, k ≠ t.from.val → k ≠ t.to.val → bal post k = bal pre k` | UNREVIEWED | agree on 726 of 726 |

44 of 44 entries are unreviewed. Record a review with `python3 -m clausal review <id> --reviewer <name>`; any later change to the phrase, its argument order or its definition voids it.

## Trusted base

- **Rust to Lean**: `lean/Generated/Wallet.lean` and `lean/Generated/Ledger.lean` are produced by Charon + Aeneas from `wallet/src/lib.rs` and `ledger/src/lib.rs`. Hashes of inputs and outputs are in `lean/provenance.json`. The theorems are about the Lean models. A Rust `while` loop becomes a call of Aeneas's `loop` combinator on a separately generated loop-body function.
- **Hand-written loop lemmas** (`lean/Ledger/Lemmas/`, one module per Rust function): not trusted. They are kernel-checked like any proof, and they appear in no statement; a scenario proof that uses one is still checked against exactly its statement.
- **Aeneas library models** (hand-written Lean standing in for std operations): `Aeneas.Std.U64.checked_add` for `u64::checked_add`; `Aeneas.Std.instHSubUScalarResult` for `u64 - u64 (panics on underflow)`; `Aeneas.Std.instHAddUScalarResult` for `usize + usize (panics on overflow)`; `Aeneas.Std.alloc.vec.Vec.len` for `Vec::len`; `Aeneas.Std.alloc.vec.Vec.index` for `Vec indexing v[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.Vec.index_mut` for `Vec indexing v[i] = x (panics out of bounds)`; `Aeneas.Std.Slice.len` for `slice::len`; `Aeneas.Std.Slice.index_usize` for `slice indexing s[i] (panics out of bounds)`; `Aeneas.Std.alloc.vec.CloneVec.clone` for `Vec::clone`; `Aeneas.Std.loop` for `while loop (Aeneas's fixed-point combinator; a loop that never ends is `div`)`.
- **clausal**: untrusted generator. Defences: Lean type-checks its output; the audit compares the constants in each elaborated statement with the glossary entries of the scenario's steps; the statement is printed above.
- **The audit** (`lean/Bdd/Audit.lean`, about 120 lines): reads from the Lean environment which axioms each theorem uses, that each proof's type is exactly its scenario's statement, and which constants statements and definitions mention.
- **Glossary**: `glossary.yaml` + `lean/Wallet/Vocab.lean` + `lean/Ledger/Vocab.lean`. The audit checks that no Given/Then definition depends on a model function: passed for all 36 definitions.
- **The Rust side** (`wallet-bdd/`): one Rust reading per Clausebook piece and an evaluator of composition trees (`src/pieces.rs`), ONE generic cucumber step (`tests/bdd.rs`) and the grid evaluation (`tests/grid.rs`). No step and no predicate is written per sentence. The trees come from clausal (`build/trees.json`, untrusted); a wrong tree or a wrong Rust reading shows up as a disagreement with the Lean side on generated inputs, or as an Examples row that differs between the compiled Rust and the model.
- **Second reading of each OLD phrase**: the whole-phrase Rust predicates in `wallet-bdd/src/lib.rs` are no longer asserted by any cucumber step; they are still compared with the old glossary's Lean definitions on a grid of arguments (table above).
- **The generated harnesses** (`evidence/`): `clausal/evgen.py` (untrusted generator), one typed Rust reading per Clausebook piece (`evidence/src/typed.rs`, hand-written once; a third reading by the same author) and a generic runner (`evidence/src/main.rs`). Defence: at every generated case the generated predicate is compared with the tree evaluator of `wallet-bdd/src/pieces.rs`, which is itself compared with the Lean pieces on the grid. Under Kani only the typed reading runs; a failing Kani input is replayed on the compiled Rust through the property-test runner, tree evaluator included. **proptest** for sampling and shrinking; **Kani and CBMC** for every bounded result.
- **Lean kernel** and the axioms `propext`, `Classical.choice`, `Quot.sound`; **rustc** for everything said about the compiled Rust.

## What this run did not check

- A property test that finds nothing has sampled; a bounded check that verifies has covered every input up to the sizes it names and nothing larger, and where it gives no answer in the time allowed it has shown nothing. Neither is a proof, and the block of each rule says which of them it holds.
- The generators of the property tests are generic (types and Givens). A falsifying input that needs a structure they are unlikely to draw, or a value that appears only in the code, is not found by them; the bounded check finds such a value when it lies within its sizes.
- That any glossary definition means what its English phrase says. Only a person can.
- That the echo of a reading says what the author meant. It is printed so that a person can check; nobody has (no trial with readers has been run on these generated echoes).
- That any Clausebook piece means what its English says. Only a person can; no piece is signed.
- A `Rule:` statement is tied to its scenarios in one direction only: the scenarios entail the rule. That the rule says everything its scenarios say is not claimed, and usually false (a rule is one sentence; its suite says more).
- A rule statement with a hand-written proof rests on the loop lemmas, not on the scenarios beneath it.
- That the Rust reading of a Clausebook piece (`wallet-bdd/src/pieces.rs`) and its Lean definition say the same is TESTED, not proved: every compiled reading is evaluated on its grid of generated inputs on both sides and the results are compared. A piece is compared only through the readings that use it, so a piece no sentence uses is not compared at all (the Clausebook table says which), and the two sides were written by one author.
- A `Rule:` line with no scenario beneath it has no Examples rows: on the compiled Rust it is evaluated on generated inputs only. A rule that compares two calls cannot have a Gherkin scenario at all (a scenario is one run).
- A flat proof obligation is generated text. What ties it to the reading is one kernel-checked equivalence per sentence; if that script fails the sentence cannot be PROVED, whatever is proved of the obligation.
- The suite adequacy note and the input-coverage table are generated from the flat statements of the old glossary, so the NEW sentences are in neither.
- The definition of each frame and its executable reading are compared on generated inputs, not proved equal. The frame with no surface form (counting with a number) is compared on a few hand-written instances only.
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
- Staleness is computed from the digests in `out/graph.json`, but every run regenerates everything, so nothing is ever stale here. `python3 -m clausal.graphlint out/graph.json --what-if <node-id>` shows what would be.

## Refinement graph

`out/graph.json`: 913 nodes, 1443 edges, 105 verdicts. Evidence entries by kind: kernel-checked 277, tested 578, tool-trusted 851. Edges claimed with no evidence at all: 80 (the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.
