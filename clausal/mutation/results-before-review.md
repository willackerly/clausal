# Mutation run against the scenario set BEFORE the review (8 scenarios)

Generated 2026-11-10T04:19:11+00:00 by `python3 mutation/run_mutants.py`. Logs: `mutation/logs/`.

18 mutants of `wallet/src/lib.rs`: 11 noticed by the scenarios (pipeline run without the crate's unit tests), 7 not.

| Mutant | Operation | What was changed | Crate unit tests | Examples rows on Rust | Proofs and search (verdicts that changed) | Noticed by the scenarios |
|---|---|---|---|---|---|---|
| d1 | `wallet::{wallet::Wallet}::deposit` | no overflow check: the balance wraps around | caught | caught (2 rows) | deposit_overflow: REFUTED | yes |
| d2 | `wallet::{wallet::Wallet}::deposit` | a successful deposit sets the balance to the amount instead of adding it | caught | MISSED | MISSED | **NO** |
| d3 | `wallet::{wallet::Wallet}::deposit` | overflow is reported as insufficient funds | caught | caught (2 rows) | deposit_overflow: REFUTED | yes |
| d4 | `wallet::{wallet::Wallet}::deposit` | a deposit that reaches exactly the maximum is rejected | MISSED | MISSED | bystander_unchanged: REFUTED | yes |
| d5 | `wallet::{wallet::Wallet}::deposit` | a rejected deposit empties the wallet | caught | caught (2 rows) | deposit_overflow: REFUTED | yes |
| d6 | `wallet::{wallet::Wallet}::deposit` | a deposit of exactly 1000003 credits one unit too few (wrong only at an input no example or grid point uses) | MISSED | MISSED | MISSED | **NO** |
| w1 | `wallet::{wallet::Wallet}::withdraw` | withdrawing the whole balance is rejected (> became >=) | caught | MISSED | MISSED | **NO** |
| w2 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal does not take the money | caught | MISSED | MISSED | **NO** |
| w3 | `wallet::{wallet::Wallet}::withdraw` | insufficient funds is reported as overflow | caught | caught (2 rows) | withdraw_too_much: REFUTED | yes |
| w4 | `wallet::{wallet::Wallet}::withdraw` | a rejected withdrawal empties the wallet | caught | caught (1 rows) | withdraw_too_much: REFUTED | yes |
| w5 | `wallet::{wallet::Wallet}::withdraw` | a successful withdrawal takes one unit too many when it can | MISSED | MISSED | MISSED | **NO** |
| t1 | `wallet::transfer` | transferring the whole balance is rejected (< became <=) | caught | caught (2 rows) | transfer_conserves: REFUTED | yes |
| t2 | `wallet::transfer` | the sender is debited before the receiver's overflow check, so a rejected transfer loses money | caught | MISSED | MISSED | **NO** |
| t3 | `wallet::transfer` | the receiver is never credited (money vanishes) | caught | caught (4 rows) | transfer_conserves: REFUTED | yes |
| t4 | `wallet::transfer` | the sender is never debited (money is created) | caught | caught (4 rows) | transfer_conserves: REFUTED | yes |
| t5 | `wallet::transfer` | receiver overflow is reported as insufficient funds | caught | MISSED | MISSED | **NO** |
| t6 | `wallet::transfer` | insufficient funds is reported as overflow | caught | caught (1 rows) | transfer_short_example: REFUTED | yes |
| t7 | `wallet::transfer` | no funds check at all (the subtraction panics instead) | caught | caught (1 rows) | transfer_short_example: COUNTEREXAMPLE | yes |

## Negative controls (checks of the checks)

| Control | What is wrong | Expected exit | Got | As expected |
|---|---|---|---|---|
