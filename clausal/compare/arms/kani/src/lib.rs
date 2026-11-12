//! Arm (c): bounded model checking with Kani, one proof harness per universal rule.
//!
//!   cargo kani --harness <rule>          (or no --harness for all 23)
//!
//! Every integer is fully symbolic (all 2^64 values). What is BOUNDED is the size of the
//! collections: a ledger has at most ACCOUNTS accounts and a batch at most BATCH transfers
//! (constants below). Within those sizes a successful harness is exhaustive; beyond them it
//! says nothing. A panic, an arithmetic overflow or an out-of-range index in the code under
//! test fails the harness (Kani checks them), as does a loop that runs for more iterations
//! than the unwinding bound allows.
#![cfg(kani)]
#![allow(unused_variables, unused_mut)] // every ledger harness starts with the same three lines

use ledger::{Ledger, Transfer};
use wallet::{transfer, Wallet, WalletError};

const MAX: u64 = u64::MAX;
/// Bounds, chosen as PREREG.md says: the largest sizes at which the harness verifies the
/// unmutated crate within the time budget. Rules that assert a TOTAL (a sum over all accounts,
/// compared before and after a batch) get smaller sizes: that comparison is what the SAT solver
/// finds hard (see ../../TRADES.md). The unwind numbers below must exceed every bound by 2.
const ACCOUNTS: usize = 4;
const BATCH: usize = 3;
const SUM_ACCOUNTS: usize = 2;
const SUM_BATCH: usize = 2;
/// `transfer_valid_moves` (one transfer, but it also asserts the total): 3 accounts.
const MOVE_ACCOUNTS: usize = 3;
/// `two_batches_conserve`: each of the two batches has at most this many transfers.
const TWO_BATCH: usize = 1;

// ---- shared helpers (counted once, not per rule) --------------------------------------------

/// Any ledger of at most N accounts, with fully symbolic balances: the ledger handed to the
/// code under test, and the test's own copy of its balances as they were (a slice of a fixed-size
/// array). Built from the array and cut to a symbolic length, and never cloned by the harness: a
/// reallocation or a copy of symbolic size is very expensive for the solver.
fn any_ledger<const N: usize>(before: &mut [u64; N]) -> (Ledger, usize) {
    *before = kani::any();
    let len: usize = kani::any();
    kani::assume(len <= N);
    let mut balances = before.to_vec();
    balances.truncate(len);
    (Ledger { balances }, len)
}

/// (from, to, amount)
type T = (usize, usize, u64);

fn any_transfer() -> T {
    (kani::any(), kani::any(), kani::any())
}

/// Any batch of `min`..=B transfers: the test's own copy of the values, the values as the
/// crate's type, and the length. The code under test is handed the slice `&batch[..len]`.
fn any_batch<const B: usize>(min: usize) -> ([T; B], [Transfer; B], usize) {
    let len: usize = kani::any();
    kani::assume(min <= len && len <= B);
    let ts: [T; B] = kani::any();
    let batch = ts.map(|(from, to, amount)| Transfer { from, to, amount });
    (ts, batch, len)
}

fn sum(bs: &[u64]) -> u128 {
    let mut s: u128 = 0;
    let mut i = 0;
    while i < bs.len() {
        s += bs[i] as u128;
        i += 1;
    }
    s
}

fn same(a: &[u64], b: &[u64]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut i = 0;
    while i < a.len() {
        if a[i] != b[i] {
            return false;
        }
        i += 1;
    }
    true
}

/// "A transfer the ledger can carry out exactly": both accounts exist and differ, the sender
/// covers the amount, and the receiver's balance stays within u64.
fn valid(bs: &[u64], t: T) -> bool {
    let (from, to, amount) = t;
    from < bs.len() && to < bs.len() && from != to && amount <= bs[from] && bs[to] as u128 + amount as u128 <= MAX as u128
}

// ---- the rules -------------------------------------------------------------------------------
// Each block between "RULE <id>" and "END RULE" is everything written for that rule.

// RULE transfer_conserves
// A covered transfer moves the money and conserves the total.
#[kani::proof]
fn transfer_conserves() {
    let (a, b, amount): (u64, u64, u64) = kani::any();
    kani::assume(amount <= a); // amount is not more than Alice's balance
    kani::assume(b as u128 + amount as u128 <= MAX as u128); // Bob's balance plus amount does not exceed the maximum
    let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
    let r = transfer(&mut alice, &mut bob, amount);
    assert!(matches!(r, Ok(())), "the operation succeeds");
    assert!(alice.balance as u128 + amount as u128 == a as u128, "Alice's balance is decreased by amount");
    assert!(bob.balance as u128 == b as u128 + amount as u128, "Bob's balance is increased by amount");
    assert!(alice.balance as u128 + bob.balance as u128 == a as u128 + b as u128, "the total of all balances is unchanged");
}
// END RULE

// RULE withdraw_too_much
// Withdrawing more than the balance is rejected and changes nothing.
#[kani::proof]
fn withdraw_too_much() {
    let (a, amount): (u64, u64) = kani::any();
    kani::assume(amount > a); // amount is more than Alice's balance
    let mut alice = Wallet { balance: a };
    let r = alice.withdraw(amount);
    assert!(matches!(r, Err(WalletError::InsufficientFunds)), "the operation is rejected with insufficient funds");
    assert!(alice.balance == a, "Alice's balance is unchanged");
}
// END RULE

// RULE deposit_overflow
// A deposit that would overflow is rejected and changes nothing.
#[kani::proof]
fn deposit_overflow() {
    let (a, amount): (u64, u64) = kani::any();
    kani::assume(a as u128 + amount as u128 > MAX as u128); // Alice's balance plus amount exceeds the maximum
    let mut alice = Wallet { balance: a };
    let r = alice.deposit(amount);
    assert!(matches!(r, Err(WalletError::Overflow)), "the operation is rejected with overflow");
    assert!(alice.balance == a, "Alice's balance is unchanged");
}
// END RULE

// RULE withdraw_covered
// A covered withdrawal succeeds and takes exactly the amount.
#[kani::proof]
fn withdraw_covered() {
    let (a, amount): (u64, u64) = kani::any();
    kani::assume(amount <= a); // amount is not more than Alice's balance
    let mut alice = Wallet { balance: a };
    let r = alice.withdraw(amount);
    assert!(matches!(r, Ok(())), "the operation succeeds");
    assert!(alice.balance as u128 + amount as u128 == a as u128, "Alice's balance is decreased by amount");
}
// END RULE

// RULE deposit_with_room
// A deposit with room succeeds and adds exactly the amount.
#[kani::proof]
fn deposit_with_room() {
    let (a, amount): (u64, u64) = kani::any();
    kani::assume(a as u128 + amount as u128 <= MAX as u128); // Alice's balance plus amount does not exceed the maximum
    let mut alice = Wallet { balance: a };
    let r = alice.deposit(amount);
    assert!(matches!(r, Ok(())), "the operation succeeds");
    assert!(alice.balance as u128 == a as u128 + amount as u128, "Alice's balance is increased by amount");
}
// END RULE

// RULE transfer_short
// Transferring more than the sender has is rejected and changes nothing.
#[kani::proof]
fn transfer_short() {
    let (a, b, amount): (u64, u64, u64) = kani::any();
    kani::assume(amount > a); // amount is more than Alice's balance
    let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
    let r = transfer(&mut alice, &mut bob, amount);
    assert!(matches!(r, Err(WalletError::InsufficientFunds)), "the operation is rejected with insufficient funds");
    assert!(alice.balance == a, "Alice's balance is unchanged");
    assert!(bob.balance == b, "Bob's balance is unchanged");
}
// END RULE

// RULE transfer_no_room
// A transfer the receiver has no room for is rejected and changes nothing.
#[kani::proof]
fn transfer_no_room() {
    let (a, b, amount): (u64, u64, u64) = kani::any();
    kani::assume(amount <= a); // amount is not more than Alice's balance
    kani::assume(b as u128 + amount as u128 > MAX as u128); // Bob's balance plus amount exceeds the maximum
    let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
    let r = transfer(&mut alice, &mut bob, amount);
    assert!(matches!(r, Err(WalletError::Overflow)), "the operation is rejected with overflow");
    assert!(alice.balance == a, "Alice's balance is unchanged");
    assert!(bob.balance == b, "Bob's balance is unchanged");
}
// END RULE

// RULE batch_conserves
// Applying any batch of transfers conserves the total of all balances.
#[kani::proof]
#[kani::unwind(6)]
fn batch_conserves() {
    let mut before = [0; SUM_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<SUM_BATCH>(0);
    main.apply_batch(&batch[..len]);
    assert!(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged");
}
// END RULE

// RULE batch_first_invalid
// A batch whose first transfer is invalid changes nothing.
#[kani::proof]
#[kani::unwind(6)]
fn batch_first_invalid() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<BATCH>(1);
    kani::assume(!valid(bs, ts[0])); // the first transfer of the batch is not valid
    let applied = main.apply_batch(&batch[..len]);
    assert!(applied == 0, "no transfer is applied");
    assert!(same(&main.balances, bs), "ledger Main is unchanged");
}
// END RULE

// RULE batch_count_bounded
// The number of transfers applied is at most the length of the batch.
#[kani::proof]
#[kani::unwind(6)]
fn batch_count_bounded() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<BATCH>(0);
    let applied = main.apply_batch(&batch[..len]);
    assert!(applied <= len, "the number of transfers applied is at most the length of the batch");
}
// END RULE

// RULE batch_stops_at_invalid
// A batch stops only at a transfer that cannot be carried out.
#[kani::proof]
#[kani::unwind(6)]
fn batch_stops_at_invalid() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<BATCH>(0);
    let applied = main.apply_batch(&batch[..len]);
    // if it stopped before the end, the transfer it stopped at is not valid on the ledger as it now stands
    assert!(applied >= len || !valid(&main.balances, ts[applied]),
            "the batch has stopped only at a transfer that is not valid on ledger Main as it now stands");
}
// END RULE

// RULE transfer_valid_moves
// A valid transfer is accepted and moves exactly its amount.
#[kani::proof]
#[kani::unwind(6)]
fn transfer_valid_moves() {
    let mut before = [0; MOVE_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let t = any_transfer();
    kani::assume(valid(bs, t)); // the transfer is valid
    let (from, to, amount) = t;
    let ok = main.apply(&Transfer { from, to, amount });
    assert!(ok, "it is accepted");
    let post = &main.balances;
    assert!(post.len() == bs.len(), "no account appeared or disappeared");
    assert!(post[from] as u128 + amount as u128 == bs[from] as u128, "the amount left the sender");
    assert!(post[to] as u128 == bs[to] as u128 + amount as u128, "the amount arrived at the receiver");
    let mut k = 0;
    while k < bs.len() {
        assert!(k == from || k == to || post[k] == bs[k], "no other balance changed");
        k += 1;
    }
    assert!(sum(post) == sum(bs), "the total of ledger Main's balances is unchanged");
}
// END RULE

// RULE transfer_invalid_rejected
// An invalid transfer is rejected and changes nothing.
#[kani::proof]
#[kani::unwind(6)]
fn transfer_invalid_rejected() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let t = any_transfer();
    kani::assume(!valid(bs, t)); // the transfer is not valid
    let ok = main.apply(&Transfer { from: t.0, to: t.1, amount: t.2 });
    assert!(!ok, "it is rejected");
    assert!(same(&main.balances, bs), "ledger Main is unchanged");
}
// END RULE

// RULE total_is_sum
// The total is the sum of the balances when that fits.
#[kani::proof]
#[kani::unwind(6)]
fn total_is_sum() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let s = sum(bs);
    kani::assume(s <= MAX as u128); // the balances add up to a sum that fits
    assert!(main.total() == Some(s as u64), "the result is the sum");
}
// END RULE

// RULE total_overflow
// The total of balances that do not fit is reported as absent.
#[kani::proof]
#[kani::unwind(6)]
fn total_overflow() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    kani::assume(sum(bs) > MAX as u128); // the balances add up to more than the maximum
    assert!(main.total().is_none(), "there is no result");
}
// END RULE

// RULE balance_of_account
// Looking up an existing account gives its balance.
#[kani::proof]
#[kani::unwind(6)]
fn balance_of_account() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let i: usize = kani::any();
    kani::assume(i < bs.len()); // i is an account
    let expected = bs[i];
    assert!(main.balance(i) == Some(expected), "the result is the balance of account i");
}
// END RULE

// RULE balance_no_account
// Looking up an account that does not exist gives nothing.
#[kani::proof]
#[kani::unwind(6)]
fn balance_no_account() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let i: usize = kani::any();
    kani::assume(i >= bs.len()); // i is not an account
    assert!(main.balance(i).is_none(), "there is no result");
}
// END RULE

// RULE whole_conserves
// Applying a batch as a whole conserves the total of all balances.
#[kani::proof]
#[kani::unwind(6)]
fn whole_conserves() {
    let mut before = [0; SUM_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<SUM_BATCH>(0);
    main.apply_all(&batch[..len]);
    assert!(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged");
}
// END RULE

// RULE whole_first_invalid
// A batch applied as a whole whose first transfer is invalid is rejected and changes nothing.
#[kani::proof]
#[kani::unwind(6)]
fn whole_first_invalid() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<BATCH>(1);
    kani::assume(!valid(bs, ts[0])); // the first transfer of the batch is not valid
    let ok = main.apply_all(&batch[..len]);
    assert!(!ok, "it is rejected");
    assert!(same(&main.balances, bs), "ledger Main is unchanged");
}
// END RULE

// RULE whole_rejected_unchanged
// A batch applied as a whole that is rejected leaves the ledger unchanged.
#[kani::proof]
#[kani::unwind(6)]
fn whole_rejected_unchanged() {
    let mut before = [0; ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (ts, batch, len) = any_batch::<BATCH>(0);
    let ok = main.apply_all(&batch[..len]);
    assert!(ok || same(&main.balances, bs), "if it is rejected, ledger Main is unchanged");
}
// END RULE

// RULE batch_then_total
// The total computed after any batch is the total before it, when that total fits.
#[kani::proof]
#[kani::unwind(6)]
fn batch_then_total() {
    let mut before = [0; SUM_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let s = sum(bs);
    kani::assume(s <= MAX as u128); // the balances add up to a sum that fits
    let (ts, batch, len) = any_batch::<SUM_BATCH>(0);
    main.apply_batch(&batch[..len]);
    assert!(main.total() == Some(s as u64), "the result is the sum");
}
// END RULE

// RULE batch_then_total_overflow
// The total computed after any batch is still absent when it did not fit before.
#[kani::proof]
#[kani::unwind(6)]
fn batch_then_total_overflow() {
    let mut before = [0; SUM_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    kani::assume(sum(bs) > MAX as u128); // the balances add up to more than the maximum
    let (ts, batch, len) = any_batch::<SUM_BATCH>(0);
    main.apply_batch(&batch[..len]);
    assert!(main.total().is_none(), "there is no result");
}
// END RULE

// RULE two_batches_conserve
// Two batches applied one after the other conserve the total.
#[kani::proof]
#[kani::unwind(6)]
fn two_batches_conserve() {
    let mut before = [0; SUM_ACCOUNTS];
    let (mut main, n) = any_ledger(&mut before);
    let bs = &before[..n];
    let (_, first, first_len) = any_batch::<TWO_BATCH>(0);
    let (_, second, second_len) = any_batch::<TWO_BATCH>(0);
    main.apply_batch(&first[..first_len]);
    let applied = main.apply_batch(&second[..second_len]);
    assert!(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged");
    assert!(applied <= second_len, "the number of transfers applied is at most the length of the second batch");
}
// END RULE
