# Slice: scenario report (wallet and ledger)

Generated 2026-11-10T11:34:56+00:00 by `slice/run.sh`. Lean `leanprover/lean4:v4.35.0`, Aeneas `nightly-2026.11.09-5a392f4`, Charon `0.1.315 (454586e9b770231e66d2062993e632dfc06463e2)`, `rustc 1.100.0-nightly (923c95cdf 2026-09-16)`, slicegen 4174fa563dab (slicegen-rule/2).

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
| Applying any batch of transfers conserves the total of all balances (`features/ledger.feature:9`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 6 / 6 of 6 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch whose first transfer is invalid changes nothing (`features/ledger.feature:24`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| The number of transfers applied is at most the length of the batch (`features/ledger.feature:38`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 3 / 3 of 3 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch stops only at a transfer that cannot be carried out (`features/ledger.feature:54`) | **COUNTEREXAMPLE** | PROVED-FOR-ALL - MISMATCH | 1 / 1 of 5 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch of two valid transfers is applied in full (`features/ledger.feature:69`) | **COUNTEREXAMPLE** | PROVED-INSTANCE - MISMATCH | 0 / 0 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch stops at its first invalid transfer and keeps what it has applied (`features/ledger.feature:77`) | **COUNTEREXAMPLE** | PROVED-INSTANCE - MISMATCH | 0 / 0 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch of transfers that are each valid on the starting ledger is applied in full (`features/ledger.feature:87`) | **COUNTEREXAMPLE** | REFUTED - MISMATCH | 0 / 0 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| A valid transfer is accepted and moves exactly its amount (`features/ledger.feature:99`) | **REFUTED** | PROVED-FOR-ALL - MISMATCH | 0 / 0 of 3 | UNREVIEWED GLOSSARY (6 of 6) |
| An invalid transfer is rejected and changes nothing (`features/ledger.feature:114`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 5 / 5 of 5 | UNREVIEWED GLOSSARY (5 of 5) |
| The total is the sum of the balances when that fits (`features/ledger.feature:130`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 5 / 5 of 5 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of balances that do not fit is reported as absent (`features/ledger.feature:145`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 3 / 3 of 3 | UNREVIEWED GLOSSARY (4 of 4) |
| The total of a ledger can always be computed (`features/ledger.feature:159`) | **REFUTED** | REFUTED | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| Looking up an existing account gives its balance (`features/ledger.feature:170`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| Looking up an account that does not exist gives nothing (`features/ledger.feature:182`) | **PROVED-FOR-ALL** | PROVED-FOR-ALL | 2 / 2 of 2 | UNREVIEWED GLOSSARY (4 of 4) |
| Applying a batch as a whole conserves the total of all balances (`features/ledger.feature:194`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 2 / 2 of 2 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch applied as a whole whose first transfer is invalid is rejected and changes nothing (`features/ledger.feature:205`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5) |
| A batch applied as a whole that is rejected leaves the ledger unchanged (`features/ledger.feature:219`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 4 / 4 of 4 | UNREVIEWED GLOSSARY (3 of 3) |
| A batch of valid transfers applied as a whole is accepted and applied (`features/ledger.feature:233`) | **COUNTEREXAMPLE** | PROVED-INSTANCE - MISMATCH | 0 / 0 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole is rolled back when its third transfer is invalid (`features/ledger.feature:242`) | **TESTED-ONLY** | PROVED-INSTANCE - MISMATCH | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A batch applied as a whole is rolled back when a later transfer is invalid (`features/ledger.feature:250`) | **TESTED-ONLY** | PROVED-INSTANCE - MISMATCH | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| The total computed after any batch is the total before it, when that total fits (`features/ledger.feature:261`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 3 / 3 of 3 | UNREVIEWED GLOSSARY (5 of 5) |
| The total computed after any batch is still absent when it did not fit before (`features/ledger.feature:276`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 2 / 2 of 2 | UNREVIEWED GLOSSARY (5 of 5) |
| Two batches applied one after the other conserve the total (`features/ledger.feature:290`) | **TESTED-ONLY** | PROVED-FOR-ALL - MISMATCH | 1 / 1 of 1 | UNREVIEWED GLOSSARY (4 of 4) |
| A withdrawal that is both covered and not covered (`features/negative.feature:8`) | **VACUOUS** | VACUOUS | 0 / 0 of 1 | ROW OUTSIDE GIVENS; UNREVIEWED GLOSSARY (5 of 5) |
| A deposit does not touch a bystander (`features/negative.feature:22`) | **PROVED-FOR-ALL (1 of 2 Thens substantive)** | PROVED-FOR-ALL | 1 / 1 of 1 | UNREVIEWED GLOSSARY (5 of 5); TRIVIAL-THEN; FRAME-TRIVIAL |

**At least one scenario did not get its expected verdict.**
A scenario tagged `@expect-refuted`, `@expect-unbound` or `@expect-vacuous` is a deliberate negative control.

**13 proved scenarios rest on glossary entries with no valid sign-off.** A proof shows the Lean statement holds; that the statement says what the English says is exactly what the sign-off is for. `./run.sh --strict` makes this a failure.

## Which inputs the scenarios apply to, and what they say about the outputs

A green scenario says nothing about inputs outside its Givens, and nothing about an output its Thens do not mention. Three views of what is left unsaid:

1. **Inputs for which some scenario applies.** For each operation, a generated theorem states that the Givens of its proved universal scenarios, taken together, hold of every input. If the kernel accepts it, no input falls outside every scenario. **This says nothing about what those scenarios promise.** A scenario with no Given beyond naming its values applies to every input whatever its Then says, so for such an operation the answer is trivially yes.
2. **What is said about each output.** The Thens of the proved universal scenarios, listed per output (the value the call returns; the state it hands back), each with the condition under which it is promised. This is a list for a person to read: nothing checks that the Thens determine the output, and for the loops here they do not (the ledger an `apply_batch` leaves is constrained only by its total and by where the batch stopped).
3. **Mutants.** A mutation run (`python3 mutation/run_mutants.py`, not part of `run.sh`) changes the Rust in small wrong ways and reports for which changes some scenario is shown false.

| Operation (Lean model) | Does some proved universal scenario apply to every input? | Said about the returned value | Said about the state afterwards | Scenarios |
|---|---|---|---|---|
| `wallet.Wallet.deposit` | **yes**: kernel-checked `Coverage.g2` over 2 proved scenarios | "the operation is rejected with {error:e}" (only when: Alice's balance plus <amount> exceeds the maximum); "the operation succeeds" (only when: Alice's balance plus <amount> does not exceed the maximum) | "{wallet:w}'s balance is unchanged" (only when: Alice's balance plus <amount> exceeds the maximum); "{wallet:w}'s balance is increased by {amount:n}" (only when: Alice's balance plus <amount> does not exceed the maximum) | deposit_overflow: PROVED-FOR-ALL; deposit_with_room: PROVED-FOR-ALL; bystander_unchanged: PROVED-FOR-ALL (1 of 2 Thens substantive) |
| `wallet.Wallet.withdraw` | **yes**: kernel-checked `Coverage.g1` over 2 proved scenarios | "the operation is rejected with {error:e}" (only when: <amount> is more than Alice's balance); "the operation succeeds" (only when: <amount> is not more than Alice's balance) | "{wallet:w}'s balance is unchanged" (only when: <amount> is more than Alice's balance); "{wallet:w}'s balance is decreased by {amount:n}" (only when: <amount> is not more than Alice's balance) | withdraw_too_much: PROVED-FOR-ALL; withdraw_covered: PROVED-FOR-ALL; contradictory_givens: VACUOUS |
| `wallet.transfer` | **yes**: kernel-checked `Coverage.g0` over 3 proved scenarios | "the operation succeeds" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "the operation is rejected with {error:e}" (only when: <amount> is more than Alice's balance); "the operation is rejected with {error:e}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> exceeds the maximum) | "{wallet:w}'s balance is decreased by {amount:n}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "{wallet:w}'s balance is increased by {amount:n}" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "the total of all balances is unchanged" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> does not exceed the maximum); "{wallet:w}'s balance is unchanged" (only when: <amount> is more than Alice's balance); "{wallet:w}'s balance is unchanged" (only when: <amount> is not more than Alice's balance; Bob's balance plus <amount> exceeds the maximum) | transfer_conserves: PROVED-FOR-ALL; transfer_short: PROVED-FOR-ALL; transfer_no_room: PROVED-FOR-ALL; transfer_short_example: PROVED-INSTANCE; transfer_always_succeeds: REFUTED |
| `ledger.Ledger.balance` | **yes**: kernel-checked `Coverage.g7` over 2 proved scenarios | "the result is the balance of account {index:i} of ledger {ledger:l}" (only when: <i> is an account of ledger Main); "there is no result" (only when: <i> is not an account of ledger Main) | **nothing** | balance_of_account: PROVED-FOR-ALL; balance_no_account: PROVED-FOR-ALL |
| `ledger.Ledger.total_loop.body` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.total_loop` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.total` | **NOT SHOWN**: `Coverage.g5` (1 scenarios): their Givens do not cover every input; `Coverage.g6` (1 scenarios): their Givens do not cover every input | "the result is {amount:s}" (only when: the balances of ledger Main add up to <sum>); "there is no result" (only when: the balances of ledger Main add up to more than the maximum) | **nothing** | total_is_sum: PROVED-FOR-ALL; total_overflow: PROVED-FOR-ALL; total_always_available: REFUTED; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY |
| `ledger.Ledger.apply` | **NOT SHOWN**: `Coverage.g4` (2 scenarios): not all proved (transfer_valid_moves, transfer_invalid_rejected) | **nothing** | **nothing** | transfer_valid_moves: REFUTED; transfer_invalid_rejected: TESTED-ONLY |
| `ledger.Ledger.apply_batch_loop.body` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch_loop` | **NOT SHOWN**: no universal scenario exercises it | **nothing** | **nothing** |  |
| `ledger.Ledger.apply_batch` | **NOT SHOWN**: `Coverage.g3` (4 scenarios): not all proved (batch_conserves, batch_first_invalid, batch_count_bounded, batch_stops_at_invalid) | **nothing** | **nothing** | batch_conserves: TESTED-ONLY; batch_first_invalid: TESTED-ONLY; batch_count_bounded: TESTED-ONLY; batch_stops_at_invalid: COUNTEREXAMPLE; batch_example_all: COUNTEREXAMPLE; batch_example_stop: COUNTEREXAMPLE; batch_all_valid_all_applied: COUNTEREXAMPLE; batch_then_total: TESTED-ONLY; batch_then_total_overflow: TESTED-ONLY; two_batches_conserve: TESTED-ONLY |
| `ledger.Ledger.apply_all` | **NOT SHOWN**: `Coverage.g8` (3 scenarios): not all proved (whole_conserves, whole_first_invalid, whole_rejected_unchanged) | **nothing** | **nothing** | whole_conserves: TESTED-ONLY; whole_first_invalid: TESTED-ONLY; whole_rejected_unchanged: TESTED-ONLY; whole_example_accept: COUNTEREXAMPLE; whole_example_rollback_late: TESTED-ONLY; whole_example_rollback: TESTED-ONLY |

No mutation results found (`mutation/results.json`). Run `python3 mutation/run_mutants.py`.

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### TESTED-ONLY: Applying any batch of transfers conserves the total of all balances

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
TESTED-ONLY  Applying any batch of transfers conserves the total of all balances
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           6 of 6 rows pass on compiled Rust (cucumber-rs); 6 of 6 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### TESTED-ONLY: A batch whose first transfer is invalid changes nothing

`features/ledger.feature:24`  id `Spec.ledger.batch_first_invalid`  tags `@id:batch_first_invalid`

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
TESTED-ONLY  A batch whose first transfer is invalid changes nothing
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-batch, LT-none-applied, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 544 of 544 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### TESTED-ONLY: The number of transfers applied is at most the length of the batch

`features/ledger.feature:38`  id `Spec.ledger.batch_count_bounded`  tags `@id:batch_count_bounded`

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
TESTED-ONLY  The number of transfers applied is at most the length of the batch
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 256 of 256 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### COUNTEREXAMPLE: A batch stops only at a transfer that cannot be carried out

`features/ledger.feature:54`  id `Spec.ledger.batch_stops_at_invalid`  tags `@id:batch_stops_at_invalid`

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
COUNTEREXAMPLE  A batch stops only at a transfer that cannot be carried out
  tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED (the call contains a loop: the generated script can only use a hand-proved loop lemma, and none says enough at this input)
  counterexample   | balances | batch    |
                   | [1, 0]   | [0->1:1] |
                   When the batch [0->1:1] is applied to ledger Main  =>  returned 0 applied; Main: balances [1, 0]
                   failed Then: "the batch [0->1:1] has stopped only at a transfer that is not valid on ledger Main as it now stands"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-stops-at-invalid
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1606 of 1606 grid points
  tested           1 of 5 rows pass on compiled Rust (cucumber-rs); 1 of 5 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, counterexample found
```

### COUNTEREXAMPLE: A batch of two valid transfers is applied in full

`features/ledger.feature:69`  id `Spec.ledger.batch_example_all`  tags `@id:batch_example_all`

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
COUNTEREXAMPLE  A batch of two valid transfers is applied in full
  tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED (the call contains a loop: the generated script can only use a hand-proved loop lemma, and none says enough at this input)
  counterexample   |  |
                   |  |
                   When the batch [0->1:30, 1->2:50] is applied to ledger Main  =>  returned 0 applied; Main: balances [100, 20, 0]
                   failed Then: "exactly 2 transfers are applied"; "ledger Main now holds the balances [70, 0, 50]"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1 inputs, counterexample found
```

### COUNTEREXAMPLE: A batch stops at its first invalid transfer and keeps what it has applied

`features/ledger.feature:77`  id `Spec.ledger.batch_example_stop`  tags `@id:batch_example_stop`

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
COUNTEREXAMPLE  A batch stops at its first invalid transfer and keeps what it has applied
  tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED (the call contains a loop: the generated script can only use a hand-proved loop lemma, and none says enough at this input)
  counterexample   |  |
                   |  |
                   When the batch [0->1:30, 2->1:5, 0->1:1] is applied to ledger Main  =>  returned 0 applied; Main: balances [100, 20, 0]
                   failed Then: "exactly 1 transfers are applied"; "ledger Main now holds the balances [70, 50, 0]"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-exactly, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 267 of 267 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1 inputs, counterexample found
```

### COUNTEREXAMPLE: A batch of transfers that are each valid on the starting ledger is applied in full

`features/ledger.feature:87`  id `Spec.ledger.batch_all_valid_all_applied`  tags `@id:batch_all_valid_all_applied @expect-refuted`

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
COUNTEREXAMPLE  A batch of transfers that are each valid on the starting ledger is applied in full
  tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED (the call contains a loop: the generated script can only use a hand-proved loop lemma, and none says enough at this input)
  counterexample   | balances | batch    |
                   | [1, 0]   | [0->1:1] |
                   When the batch [0->1:1] is applied to ledger Main  =>  returned 0 applied; Main: balances [1, 0]
                   failed Then: "every transfer of [0->1:1] is applied"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_batch, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-all-valid, LW-batch, LT-all-applied
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 553 of 553 grid points
  tested           0 of 2 rows pass on compiled Rust (cucumber-rs); 0 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, counterexample found
```

### REFUTED: A valid transfer is accepted and moves exactly its amount

`features/ledger.feature:99`  id `Spec.ledger.transfer_valid_moves`  tags `@id:transfer_valid_moves`

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
REFUTED  A valid transfer is accepted and moves exactly its amount
  kernel-checked   theorem Spec.ledger.transfer_valid_moves.refuted : ¬ Spec.ledger.transfer_valid_moves.stmt; axioms propext, Classical.choice, Quot.sound
  counterexample   | balances | t      |
                   | [1, 0]   | 0->1:1 |
                   When the transfer 0->1:1 is applied to ledger Main  =>  returned false; Main: balances [1, 0]
                   failed Then: "it is accepted"; "the amount of 0->1:1 has moved between its accounts in ledger Main and no other balance changed"
                   held   Then: "the total of ledger Main's balances is unchanged"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: none
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 6 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-valid, LW-transfer, LT-accepted, LT-moved, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 1036 of 1036 grid points
  tested           0 of 3 rows pass on compiled Rust (cucumber-rs); 0 of 3 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 66 inputs, counterexample found
```

### TESTED-ONLY: An invalid transfer is rejected and changes nothing

`features/ledger.feature:114`  id `Spec.ledger.transfer_invalid_rejected`  tags `@id:transfer_invalid_rejected`

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
TESTED-ONLY  An invalid transfer is rejected and changes nothing
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply: none
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-invalid, LW-transfer, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 310 of 310 grid points
  tested           5 of 5 rows pass on compiled Rust (cucumber-rs); 5 of 5 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 66 inputs, no counterexample
```

### PROVED-FOR-ALL: The total is the sum of the balances when that fits

`features/ledger.feature:130`  id `Spec.ledger.total_is_sum`  tags `@id:total_is_sum`

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### PROVED-FOR-ALL: The total of balances that do not fit is reported as absent

`features/ledger.feature:145`  id `Spec.ledger.total_overflow`  tags `@id:total_overflow`

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### REFUTED: The total of a ledger can always be computed

`features/ledger.feature:159`  id `Spec.ledger.total_always_available`  tags `@id:total_always_available @expect-refuted`

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-total, LT-some-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 126 of 126 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 11 inputs, counterexample found
  note             every Examples row passes; the examples alone would not have caught this
```

### PROVED-FOR-ALL: Looking up an existing account gives its balance

`features/ledger.feature:170`  id `Spec.ledger.balance_of_account`  tags `@id:balance_of_account`

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### PROVED-FOR-ALL: Looking up an account that does not exist gives nothing

`features/ledger.feature:182`  id `Spec.ledger.balance_no_account`  tags `@id:balance_no_account`

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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

### TESTED-ONLY: Applying a batch as a whole conserves the total of all balances

`features/ledger.feature:194`  id `Spec.ledger.whole_conserves`  tags `@id:whole_conserves`

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
TESTED-ONLY  Applying a batch as a whole conserves the total of all balances
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-total-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 242 of 242 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### TESTED-ONLY: A batch applied as a whole whose first transfer is invalid is rejected and changes nothing

`features/ledger.feature:205`  id `Spec.ledger.whole_first_invalid`  tags `@id:whole_first_invalid`

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
TESTED-ONLY  A batch applied as a whole whose first transfer is invalid is rejected and changes nothing
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-first-invalid, LW-whole, LT-rejected, LT-same
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 541 of 541 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### TESTED-ONLY: A batch applied as a whole that is rejected leaves the ledger unchanged

`features/ledger.feature:219`  id `Spec.ledger.whole_rejected_unchanged`  tags `@id:whole_rejected_unchanged`

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
TESTED-ONLY  A batch applied as a whole that is rejected leaves the ledger unchanged
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 3 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-same-if-rejected
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 363 of 363 grid points
  tested           4 of 4 rows pass on compiled Rust (cucumber-rs); 4 of 4 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### COUNTEREXAMPLE: A batch of valid transfers applied as a whole is accepted and applied

`features/ledger.feature:233`  id `Spec.ledger.whole_example_accept`  tags `@id:whole_example_accept`

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
COUNTEREXAMPLE  A batch of valid transfers applied as a whole is accepted and applied
  tested           counterexample found on the Lean model; kernel confirmation attempted and FAILED (the call contains a loop: the generated script can only use a hand-proved loop lemma, and none says enough at this input)
  counterexample   |  |
                   |  |
                   When the batch [0->1:30, 1->2:50] is applied to ledger Main as a whole  =>  returned false; Main: balances [100, 20, 0]
                   failed Then: "it is accepted"; "ledger Main now holds the balances [70, 0, 50]"
  tested           the same input on the compiled Rust (cucumber-rs): reproduced
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-accepted, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           0 of 1 rows pass on compiled Rust (cucumber-rs); 0 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1 inputs, counterexample found
```

### TESTED-ONLY: A batch applied as a whole is rolled back when its third transfer is invalid

`features/ledger.feature:242`  id `Spec.ledger.whole_example_rollback_late`  tags `@id:whole_example_rollback_late`

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
TESTED-ONLY  A batch applied as a whole is rolled back when its third transfer is invalid
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1 inputs, no counterexample
```

### TESTED-ONLY: A batch applied as a whole is rolled back when a later transfer is invalid

`features/ledger.feature:250`  id `Spec.ledger.whole_example_rollback`  tags `@id:whole_example_rollback`

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
TESTED-ONLY  A batch applied as a whole is rolled back when a later transfer is invalid
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_all, not the Rust source
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_all: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.alloc.vec.CloneVec.clone, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-whole, LT-rejected, LT-now-holds
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 244 of 244 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1 inputs, no counterexample
```

### TESTED-ONLY: The total computed after any batch is the total before it, when that total fits

`features/ledger.feature:261`  id `Spec.ledger.batch_then_total`  tags `@id:batch_then_total`

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
TESTED-ONLY  The total computed after any batch is the total before it, when that total fits
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop, Aeneas.Std.U64.checked_add, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sums-to, LW-batch, LW-total, LT-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 217 of 217 grid points
  tested           3 of 3 rows pass on compiled Rust (cucumber-rs); 3 of 3 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 1782 inputs, no counterexample
```

### TESTED-ONLY: The total computed after any batch is still absent when it did not fit before

`features/ledger.feature:276`  id `Spec.ledger.batch_then_total_overflow`  tags `@id:batch_then_total_overflow`

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
TESTED-ONLY  The total computed after any batch is still absent when it did not fit before
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.total, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch, ledger.Ledger.total: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop, Aeneas.Std.U64.checked_add, Aeneas.Std.alloc.vec.Vec.len, Aeneas.Std.alloc.vec.Vec.index
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 5 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LG-sum-too-big, LW-batch, LW-total, LT-no-result
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 137 of 137 grid points
  tested           2 of 2 rows pass on compiled Rust (cucumber-rs); 2 of 2 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 297 inputs, no counterexample
```

### TESTED-ONLY: Two batches applied one after the other conserve the total

`features/ledger.feature:290`  id `Spec.ledger.two_batches_conserve`  tags `@id:two_batches_conserve`

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
TESTED-ONLY  Two batches applied one after the other conserve the total
  not proved       the proof does not compile (it depends on Ledger.Lemmas.Apply, which does not compile (see out/proofs.log))
  about            the Lean model ledger.Ledger.apply_batch, then ledger.Ledger.apply_batch, not the Rust source
  sequence         2 Whens run in order, each on the state the one before left; every call must return; `the result` in a Then is the LAST When's, and earlier results are otherwise unconstrained
  tool-trusted     model = Rust: rustc 1.100.0-nightly (923c95cdf 2026-09-16), charon 0.1.315 (454586e9b770231e66d2062993e632dfc06463e2), aeneas nightly-2026.11.09-5a392f4
  tool-trusted     Aeneas library models used by ledger.Ledger.apply_batch: Aeneas.Std.instHAddUScalarResult, Aeneas.Std.Slice.len, Aeneas.Std.Slice.index_usize, Aeneas.Std.loop
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
  NOT ASSERTED     0 of 4 glossary phrases signed off by anyone - UNREVIEWED: LG-holds, LW-batch, LT-total-same, LT-at-most
  tested           the Lean definition and the Rust predicate of each Given/Then phrase agree on 377 of 377 grid points
  tested           1 of 1 rows pass on compiled Rust (cucumber-rs); 1 of 1 pass on the Lean model; they agree
  tested           boundary grid on the Lean model: 8019 inputs, no counterexample
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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
  tool-trusted     statement generated by slicegen 4174fa563dab (slicegen-rule/2); printed for comparison with the scenario; constants it uses match the glossary: yes
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

`out/graph.json`: 366 nodes, 875 edges, 47 verdicts. Evidence entries by kind: kernel-checked 57, tested 388, tool-trusted 503. Edges claimed with no evidence at all: 80 (the unsigned glossary bindings). Schema: `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`.
