//! Arm (b): property-based tests (proptest) of the universal rules, one property per rule.
//!
//!   cargo run --quiet -- [--profile plain|edge] [--cases 10000] [--seed 20261110]
//!                        [--crate wallet|ledger|all] [--timeout-secs 120] [--only rule,rule]
//!
//! Prints one JSON object per rule on stdout:
//!   {"rule", "crate", "profile", "status": "pass" | "fail" | "hang" | "abort",
//!    "calls_to_first_failure", "calls", "elapsed_ms", "row": {column: cell} | null, "message"}
//! `row` is the SHRUNK failing input, written as a row of the rule's Examples table, so that it
//! can be pasted into the feature file and replayed on the Lean model and under cucumber.
//!
//! Each property is the English rule and nothing else: the Givens decide which inputs are
//! generated, the Thens are asserted with plain integer arithmetic in u128. No helper of
//! wallet-bdd is used, so this is a third reading of the phrases (after Lean and wallet-bdd).
//!
//! Two generator profiles, the SAME properties:
//!   plain  integers uniform over the range the Givens allow
//!   edge   the same ranges, but half of the draws are within 3 of an end of the range
//! A panic inside the code under test fails the property (proptest catches it). A property that
//! does not finish within the timeout is reported as "hang".
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{mpsc, Arc};
use std::time::{Duration, Instant};

use ledger::{Ledger, Transfer};
use proptest::collection::vec;
use proptest::prelude::*;
use proptest::test_runner::{Config, RngAlgorithm, TestCaseError, TestError, TestRng, TestRunner};
use wallet::{transfer, Wallet, WalletError};

const MAX: u64 = u64::MAX;
/// Largest number of accounts / of transfers in a batch that is generated.
const SIZE: usize = 6;

#[derive(Clone, Copy, PartialEq, Debug)]
enum Profile {
    Plain,
    Edge,
}

// ---- shared helpers (counted once, not per rule) --------------------------------------------

/// An integer in lo..=hi.
fn int(p: Profile, lo: u64, hi: u64) -> BoxedStrategy<u64> {
    assert!(lo <= hi);
    match p {
        Profile::Plain => (lo..=hi).boxed(),
        Profile::Edge => {
            let near_lo = lo.saturating_add(3).min(hi);
            let near_hi = hi.saturating_sub(3).max(lo);
            prop_oneof![4 => lo..=hi, 2 => lo..=near_lo, 2 => near_hi..=hi].boxed()
        }
    }
}

type Row = Vec<(&'static str, String)>;
type Check = Result<(), String>;

fn ensure(cond: bool, what: &str) -> Check {
    if cond {
        Ok(())
    } else {
        Err(format!("Then failed: {what}"))
    }
}

/// (from, to, amount): the test's own value for a transfer (ledger::Transfer has no Clone/Debug).
type T = (usize, usize, u64);

fn sum(bs: &[u64]) -> u128 {
    bs.iter().map(|&b| b as u128).sum()
}

/// "A transfer the ledger can carry out exactly": both accounts exist and differ, the sender
/// covers the amount, and the receiver's balance stays within u64.
fn valid(bs: &[u64], t: T) -> bool {
    let (from, to, amount) = t;
    from < bs.len() && to < bs.len() && from != to && amount <= bs[from] && bs[to] as u128 + amount as u128 <= MAX as u128
}

fn to_batch(b: &[T]) -> Vec<Transfer> {
    b.iter().map(|&(from, to, amount)| Transfer { from, to, amount }).collect()
}

fn show_balances(bs: &[u64]) -> String {
    format!("[{}]", bs.iter().map(|b| b.to_string()).collect::<Vec<_>>().join(", "))
}
fn show_transfer(t: &T) -> String {
    format!("{}->{}:{}", t.0, t.1, t.2)
}
fn show_batch(b: &[T]) -> String {
    format!("[{}]", b.iter().map(show_transfer).collect::<Vec<_>>().join(", "))
}

fn balances(p: Profile, min_len: usize) -> BoxedStrategy<Vec<u64>> {
    vec(int(p, 0, MAX), min_len..=SIZE).boxed()
}
/// An account number for a ledger of `len` accounts: existing ones and the first that does not exist.
fn account(p: Profile, len: usize) -> BoxedStrategy<usize> {
    int(p, 0, len as u64).prop_map(|i| i as usize).boxed()
}
fn any_transfer(p: Profile, len: usize) -> BoxedStrategy<T> {
    (account(p, len), account(p, len), int(p, 0, MAX)).boxed()
}
fn any_batch(p: Profile, len: usize, min: usize) -> BoxedStrategy<Vec<T>> {
    vec(any_transfer(p, len), min..=SIZE).boxed()
}
fn ledger_and_batch(p: Profile) -> BoxedStrategy<(Vec<u64>, Vec<T>)> {
    balances(p, 0).prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_batch(p, n, 0)) }).boxed()
}
fn ledger_and_batch_first_invalid(p: Profile) -> BoxedStrategy<(Vec<u64>, Vec<T>)> {
    balances(p, 0)
        .prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_batch(p, n, 1)) })
        .prop_filter("the first transfer is not valid", |(bs, b)| !valid(bs, b[0]))
        .boxed()
}
fn balances_that_fit(p: Profile) -> BoxedStrategy<Vec<u64>> {
    balances(p, 0).prop_filter("the balances add up to a u64", |bs| sum(bs) <= MAX as u128).boxed()
}
fn balances_too_big(p: Profile) -> BoxedStrategy<Vec<u64>> {
    balances(p, 0).prop_filter("the balances add up to more than the maximum", |bs| sum(bs) > MAX as u128).boxed()
}

struct Outcome {
    status: &'static str,
    calls_to_first_failure: u64,
    calls: u64,
    row: Option<Row>,
    message: String,
}

fn seed_for(seed: u64, rule: &str) -> [u8; 32] {
    // FNV-1a of the rule name, mixed with the run seed: every rule gets its own stream.
    let mut h: u64 = 0xcbf29ce484222325 ^ seed;
    let mut out = [0u8; 32];
    for k in 0..4 {
        for b in rule.bytes() {
            h ^= b as u64;
            h = h.wrapping_mul(0x100000001b3);
        }
        h ^= k as u64 + 1;
        h = h.wrapping_mul(0x100000001b3);
        out[k * 8..k * 8 + 8].copy_from_slice(&h.to_le_bytes());
    }
    out
}

/// Run one property: `cases` generated inputs, shrinking on failure.
fn run<V: std::fmt::Debug + Clone + 'static>(
    rule: &str, seed: u64, cases: u32, strategy: BoxedStrategy<V>, row: fn(&V) -> Row, check: fn(&V) -> Check,
) -> Outcome {
    let config = Config {
        cases,
        failure_persistence: None,
        max_global_rejects: 4_000_000,
        max_local_rejects: 4_000_000,
        max_shrink_iters: 100_000,
        verbose: 0,
        ..Config::default()
    };
    let mut runner = TestRunner::new_with_rng(config, TestRng::from_seed(RngAlgorithm::ChaCha, &seed_for(seed, rule)));
    let calls = AtomicU64::new(0);
    let first_failure = AtomicU64::new(0);
    let result = runner.run(&strategy, |v| {
        let n = calls.fetch_add(1, Ordering::SeqCst) + 1;
        let r = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| check(&v)));
        let r = match r {
            Ok(r) => r,
            Err(e) => Err(format!(
                "the code under test panicked: {}",
                e.downcast_ref::<String>().cloned().or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string())).unwrap_or_default()
            )),
        };
        r.map_err(|m| {
            let _ = first_failure.compare_exchange(0, n, Ordering::SeqCst, Ordering::SeqCst);
            TestCaseError::fail(m)
        })
    });
    let (status, r, message) = match result {
        Ok(()) => ("pass", None, String::new()),
        Err(TestError::Fail(reason, v)) => ("fail", Some(row(&v)), reason.message().to_string()),
        Err(TestError::Abort(reason)) => ("abort", None, reason.message().to_string()),
    };
    Outcome { status, calls_to_first_failure: first_failure.load(Ordering::SeqCst), calls: calls.load(Ordering::SeqCst), row: r, message }
}

type Prop = (&'static str, &'static str, fn(Profile, u64, u32) -> Outcome);

// ---- the rules -------------------------------------------------------------------------------
// Each block between "RULE <id>" and "END RULE" is everything written for that rule.

// RULE transfer_conserves
// A covered transfer moves the money and conserves the total.
fn transfer_conserves(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 0, MAX)
        .prop_flat_map(move |a| (Just(a), int(p, 0, a))) // amount is not more than Alice's balance
        .prop_flat_map(move |(a, amount)| (Just(a), int(p, 0, MAX - amount), Just(amount))) // Bob's balance plus amount does not exceed the maximum
        .boxed();
    run("transfer_conserves", seed, cases, inputs,
        |&(a, b, amount)| vec![("a", a.to_string()), ("b", b.to_string()), ("amount", amount.to_string())],
        |&(a, b, amount)| {
            let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
            let r = transfer(&mut alice, &mut bob, amount);
            ensure(matches!(r, Ok(())), "the operation succeeds")?;
            ensure(alice.balance as u128 + amount as u128 == a as u128, "Alice's balance is decreased by amount")?;
            ensure(bob.balance as u128 == b as u128 + amount as u128, "Bob's balance is increased by amount")?;
            ensure(alice.balance as u128 + bob.balance as u128 == a as u128 + b as u128, "the total of all balances is unchanged")
        })
}
// END RULE

// RULE withdraw_too_much
// Withdrawing more than the balance is rejected and changes nothing.
fn withdraw_too_much(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 0, MAX - 1).prop_flat_map(move |a| (Just(a), int(p, a + 1, MAX))).boxed(); // amount is more than Alice's balance
    run("withdraw_too_much", seed, cases, inputs,
        |&(a, amount)| vec![("a", a.to_string()), ("amount", amount.to_string())],
        |&(a, amount)| {
            let mut alice = Wallet { balance: a };
            let r = alice.withdraw(amount);
            ensure(matches!(r, Err(WalletError::InsufficientFunds)), "the operation is rejected with insufficient funds")?;
            ensure(alice.balance == a, "Alice's balance is unchanged")
        })
}
// END RULE

// RULE deposit_overflow
// A deposit that would overflow is rejected and changes nothing.
fn deposit_overflow(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 1, MAX).prop_flat_map(move |a| (Just(a), int(p, MAX - a + 1, MAX))).boxed(); // Alice's balance plus amount exceeds the maximum
    run("deposit_overflow", seed, cases, inputs,
        |&(a, amount)| vec![("a", a.to_string()), ("amount", amount.to_string())],
        |&(a, amount)| {
            let mut alice = Wallet { balance: a };
            let r = alice.deposit(amount);
            ensure(matches!(r, Err(WalletError::Overflow)), "the operation is rejected with overflow")?;
            ensure(alice.balance == a, "Alice's balance is unchanged")
        })
}
// END RULE

// RULE withdraw_covered
// A covered withdrawal succeeds and takes exactly the amount.
fn withdraw_covered(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 0, MAX).prop_flat_map(move |a| (Just(a), int(p, 0, a))).boxed(); // amount is not more than Alice's balance
    run("withdraw_covered", seed, cases, inputs,
        |&(a, amount)| vec![("a", a.to_string()), ("amount", amount.to_string())],
        |&(a, amount)| {
            let mut alice = Wallet { balance: a };
            let r = alice.withdraw(amount);
            ensure(matches!(r, Ok(())), "the operation succeeds")?;
            ensure(alice.balance as u128 + amount as u128 == a as u128, "Alice's balance is decreased by amount")
        })
}
// END RULE

// RULE deposit_with_room
// A deposit with room succeeds and adds exactly the amount.
fn deposit_with_room(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 0, MAX).prop_flat_map(move |a| (Just(a), int(p, 0, MAX - a))).boxed(); // Alice's balance plus amount does not exceed the maximum
    run("deposit_with_room", seed, cases, inputs,
        |&(a, amount)| vec![("a", a.to_string()), ("amount", amount.to_string())],
        |&(a, amount)| {
            let mut alice = Wallet { balance: a };
            let r = alice.deposit(amount);
            ensure(matches!(r, Ok(())), "the operation succeeds")?;
            ensure(alice.balance as u128 == a as u128 + amount as u128, "Alice's balance is increased by amount")
        })
}
// END RULE

// RULE transfer_short
// Transferring more than the sender has is rejected and changes nothing.
fn transfer_short(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = (int(p, 0, MAX - 1), int(p, 0, MAX))
        .prop_flat_map(move |(a, b)| (Just(a), Just(b), int(p, a + 1, MAX))) // amount is more than Alice's balance
        .boxed();
    run("transfer_short", seed, cases, inputs,
        |&(a, b, amount)| vec![("a", a.to_string()), ("b", b.to_string()), ("amount", amount.to_string())],
        |&(a, b, amount)| {
            let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
            let r = transfer(&mut alice, &mut bob, amount);
            ensure(matches!(r, Err(WalletError::InsufficientFunds)), "the operation is rejected with insufficient funds")?;
            ensure(alice.balance == a, "Alice's balance is unchanged")?;
            ensure(bob.balance == b, "Bob's balance is unchanged")
        })
}
// END RULE

// RULE transfer_no_room
// A transfer the receiver has no room for is rejected and changes nothing.
fn transfer_no_room(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = int(p, 1, MAX)
        .prop_flat_map(move |a| (Just(a), int(p, 1, a))) // amount is not more than Alice's balance (and at least 1, or Bob always has room)
        .prop_flat_map(move |(a, amount)| (Just(a), int(p, MAX - amount + 1, MAX), Just(amount))) // Bob's balance plus amount exceeds the maximum
        .boxed();
    run("transfer_no_room", seed, cases, inputs,
        |&(a, b, amount)| vec![("a", a.to_string()), ("b", b.to_string()), ("amount", amount.to_string())],
        |&(a, b, amount)| {
            let (mut alice, mut bob) = (Wallet { balance: a }, Wallet { balance: b });
            let r = transfer(&mut alice, &mut bob, amount);
            ensure(matches!(r, Err(WalletError::Overflow)), "the operation is rejected with overflow")?;
            ensure(alice.balance == a, "Alice's balance is unchanged")?;
            ensure(bob.balance == b, "Bob's balance is unchanged")
        })
}
// END RULE

// RULE batch_conserves
// Applying any batch of transfers conserves the total of all balances.
fn batch_conserves(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("batch_conserves", seed, cases, ledger_and_batch(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            main.apply_batch(&to_batch(b));
            ensure(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged")
        })
}
// END RULE

// RULE batch_first_invalid
// A batch whose first transfer is invalid changes nothing.
fn batch_first_invalid(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("batch_first_invalid", seed, cases, ledger_and_batch_first_invalid(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            let applied = main.apply_batch(&to_batch(b));
            ensure(applied == 0, "no transfer is applied")?;
            ensure(&main.balances == bs, "ledger Main is unchanged")
        })
}
// END RULE

// RULE batch_count_bounded
// The number of transfers applied is at most the length of the batch.
fn batch_count_bounded(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("batch_count_bounded", seed, cases, ledger_and_batch(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            let applied = main.apply_batch(&to_batch(b));
            ensure(applied <= b.len(), "the number of transfers applied is at most the length of the batch")
        })
}
// END RULE

// RULE batch_stops_at_invalid
// A batch stops only at a transfer that cannot be carried out.
fn batch_stops_at_invalid(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("batch_stops_at_invalid", seed, cases, ledger_and_batch(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            let applied = main.apply_batch(&to_batch(b));
            // if it stopped before the end, the transfer it stopped at is not valid on the ledger as it now stands
            ensure(applied >= b.len() || !valid(&main.balances, b[applied]),
                   "the batch has stopped only at a transfer that is not valid on ledger Main as it now stands")
        })
}
// END RULE

// RULE transfer_valid_moves
// A valid transfer is accepted and moves exactly its amount.
fn transfer_valid_moves(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances(p, 2)
        .prop_flat_map(|bs| { let n = bs.len(); (Just(bs), 0..n, 0..n - 1) }) // two different existing accounts
        .prop_flat_map(move |(bs, from, k)| {
            let to = if k >= from { k + 1 } else { k };
            let most = bs[from].min(MAX - bs[to]); // the sender covers it and the receiver has room
            (Just(bs), Just(from), Just(to), int(p, 0, most))
        })
        .prop_map(|(bs, from, to, amount)| (bs, (from, to, amount)))
        .boxed();
    run("transfer_valid_moves", seed, cases, inputs,
        |(bs, t)| vec![("balances", show_balances(bs)), ("t", show_transfer(t))],
        |(bs, t)| {
            let &(from, to, amount) = t;
            let mut main = Ledger { balances: bs.clone() };
            let ok = main.apply(&Transfer { from, to, amount });
            ensure(ok, "it is accepted")?;
            let post = &main.balances;
            ensure(post.len() == bs.len()
                   && post[from] as u128 + amount as u128 == bs[from] as u128
                   && post[to] as u128 == bs[to] as u128 + amount as u128
                   && (0..bs.len()).all(|k| k == from || k == to || post[k] == bs[k]),
                   "the amount has moved between its accounts and no other balance changed")?;
            ensure(sum(post) == sum(bs), "the total of ledger Main's balances is unchanged")
        })
}
// END RULE

// RULE transfer_invalid_rejected
// An invalid transfer is rejected and changes nothing.
fn transfer_invalid_rejected(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances(p, 0)
        .prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_transfer(p, n)) })
        .prop_filter("the transfer is not valid", |(bs, t)| !valid(bs, *t))
        .boxed();
    run("transfer_invalid_rejected", seed, cases, inputs,
        |(bs, t)| vec![("balances", show_balances(bs)), ("t", show_transfer(t))],
        |(bs, t)| {
            let mut main = Ledger { balances: bs.clone() };
            let ok = main.apply(&Transfer { from: t.0, to: t.1, amount: t.2 });
            ensure(!ok, "it is rejected")?;
            ensure(&main.balances == bs, "ledger Main is unchanged")
        })
}
// END RULE

// RULE total_is_sum
// The total is the sum of the balances when that fits.
fn total_is_sum(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("total_is_sum", seed, cases, balances_that_fit(p),
        |bs| vec![("balances", show_balances(bs)), ("sum", sum(bs).to_string())],
        |bs| {
            let main = Ledger { balances: bs.clone() };
            ensure(main.total().map(|s| s as u128) == Some(sum(bs)), "the result is the sum")
        })
}
// END RULE

// RULE total_overflow
// The total of balances that do not fit is reported as absent.
fn total_overflow(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("total_overflow", seed, cases, balances_too_big(p),
        |bs| vec![("balances", show_balances(bs))],
        |bs| {
            let main = Ledger { balances: bs.clone() };
            ensure(main.total().is_none(), "there is no result")
        })
}
// END RULE

// RULE balance_of_account
// Looking up an existing account gives its balance.
fn balance_of_account(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances(p, 1).prop_flat_map(|bs| { let n = bs.len(); (Just(bs), 0..n) }).boxed(); // i is an account
    run("balance_of_account", seed, cases, inputs,
        |(bs, i)| vec![("balances", show_balances(bs)), ("i", i.to_string())],
        |(bs, i)| {
            let main = Ledger { balances: bs.clone() };
            ensure(main.balance(*i) == Some(bs[*i]), "the result is the balance of account i")
        })
}
// END RULE

// RULE balance_no_account
// Looking up an account that does not exist gives nothing.
fn balance_no_account(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances(p, 0)
        .prop_flat_map(move |bs| { let n = bs.len() as u64; (Just(bs), int(p, n, usize::MAX as u64)) }) // i is not an account
        .prop_map(|(bs, i)| (bs, i as usize))
        .boxed();
    run("balance_no_account", seed, cases, inputs,
        |(bs, i)| vec![("balances", show_balances(bs)), ("i", i.to_string())],
        |(bs, i)| {
            let main = Ledger { balances: bs.clone() };
            ensure(main.balance(*i).is_none(), "there is no result")
        })
}
// END RULE

// RULE whole_conserves
// Applying a batch as a whole conserves the total of all balances.
fn whole_conserves(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("whole_conserves", seed, cases, ledger_and_batch(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            main.apply_all(&to_batch(b));
            ensure(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged")
        })
}
// END RULE

// RULE whole_first_invalid
// A batch applied as a whole whose first transfer is invalid is rejected and changes nothing.
fn whole_first_invalid(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("whole_first_invalid", seed, cases, ledger_and_batch_first_invalid(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            let ok = main.apply_all(&to_batch(b));
            ensure(!ok, "it is rejected")?;
            ensure(&main.balances == bs, "ledger Main is unchanged")
        })
}
// END RULE

// RULE whole_rejected_unchanged
// A batch applied as a whole that is rejected leaves the ledger unchanged.
fn whole_rejected_unchanged(p: Profile, seed: u64, cases: u32) -> Outcome {
    run("whole_rejected_unchanged", seed, cases, ledger_and_batch(p),
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            let ok = main.apply_all(&to_batch(b));
            ensure(ok || &main.balances == bs, "if it is rejected, ledger Main is unchanged")
        })
}
// END RULE

// RULE batch_then_total
// The total computed after any batch is the total before it, when that total fits.
fn batch_then_total(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances_that_fit(p).prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_batch(p, n, 0)) }).boxed();
    run("batch_then_total", seed, cases, inputs,
        |(bs, b)| vec![("balances", show_balances(bs)), ("sum", sum(bs).to_string()), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            main.apply_batch(&to_batch(b));
            ensure(main.total().map(|s| s as u128) == Some(sum(bs)), "the result is the sum")
        })
}
// END RULE

// RULE batch_then_total_overflow
// The total computed after any batch is still absent when it did not fit before.
fn batch_then_total_overflow(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances_too_big(p).prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_batch(p, n, 0)) }).boxed();
    run("batch_then_total_overflow", seed, cases, inputs,
        |(bs, b)| vec![("balances", show_balances(bs)), ("batch", show_batch(b))],
        |(bs, b)| {
            let mut main = Ledger { balances: bs.clone() };
            main.apply_batch(&to_batch(b));
            ensure(main.total().is_none(), "there is no result")
        })
}
// END RULE

// RULE two_batches_conserve
// Two batches applied one after the other conserve the total.
fn two_batches_conserve(p: Profile, seed: u64, cases: u32) -> Outcome {
    let inputs = balances(p, 0).prop_flat_map(move |bs| { let n = bs.len(); (Just(bs), any_batch(p, n, 0), any_batch(p, n, 0)) }).boxed();
    run("two_batches_conserve", seed, cases, inputs,
        |(bs, first, second)| vec![("balances", show_balances(bs)), ("first", show_batch(first)), ("second", show_batch(second))],
        |(bs, first, second)| {
            let mut main = Ledger { balances: bs.clone() };
            main.apply_batch(&to_batch(first));
            let applied = main.apply_batch(&to_batch(second));
            ensure(sum(&main.balances) == sum(bs), "the total of ledger Main's balances is unchanged")?;
            ensure(applied <= second.len(), "the number of transfers applied is at most the length of the second batch")
        })
}
// END RULE

const PROPS: &[Prop] = &[
    ("transfer_conserves", "wallet", transfer_conserves),
    ("withdraw_too_much", "wallet", withdraw_too_much),
    ("deposit_overflow", "wallet", deposit_overflow),
    ("withdraw_covered", "wallet", withdraw_covered),
    ("deposit_with_room", "wallet", deposit_with_room),
    ("transfer_short", "wallet", transfer_short),
    ("transfer_no_room", "wallet", transfer_no_room),
    ("batch_conserves", "ledger", batch_conserves),
    ("batch_first_invalid", "ledger", batch_first_invalid),
    ("batch_count_bounded", "ledger", batch_count_bounded),
    ("batch_stops_at_invalid", "ledger", batch_stops_at_invalid),
    ("transfer_valid_moves", "ledger", transfer_valid_moves),
    ("transfer_invalid_rejected", "ledger", transfer_invalid_rejected),
    ("total_is_sum", "ledger", total_is_sum),
    ("total_overflow", "ledger", total_overflow),
    ("balance_of_account", "ledger", balance_of_account),
    ("balance_no_account", "ledger", balance_no_account),
    ("whole_conserves", "ledger", whole_conserves),
    ("whole_first_invalid", "ledger", whole_first_invalid),
    ("whole_rejected_unchanged", "ledger", whole_rejected_unchanged),
    ("batch_then_total", "ledger", batch_then_total),
    ("batch_then_total_overflow", "ledger", batch_then_total_overflow),
    ("two_batches_conserve", "ledger", two_batches_conserve),
];

fn json_str(s: &str) -> String {
    let mut o = String::from("\"");
    for c in s.chars() {
        match c {
            '"' => o.push_str("\\\""),
            '\\' => o.push_str("\\\\"),
            '\n' => o.push_str("\\n"),
            c if (c as u32) < 0x20 => o.push_str(&format!("\\u{:04x}", c as u32)),
            c => o.push(c),
        }
    }
    o.push('"');
    o
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let arg = |name: &str, default: &str| -> String {
        args.iter().position(|a| a == name).and_then(|i| args.get(i + 1)).cloned().unwrap_or_else(|| default.to_string())
    };
    let profile = match arg("--profile", "plain").as_str() {
        "plain" => Profile::Plain,
        "edge" => Profile::Edge,
        other => panic!("unknown profile {other}"),
    };
    let cases: u32 = arg("--cases", "10000").parse().unwrap();
    let seed: u64 = arg("--seed", "20261110").parse().unwrap();
    let which = arg("--crate", "all");
    let timeout = Duration::from_secs(arg("--timeout-secs", "120").parse().unwrap());
    let only = arg("--only", "");
    let only: Vec<&str> = only.split(',').filter(|s| !s.is_empty()).collect();
    std::panic::set_hook(Box::new(|_| {})); // panics of the code under test are data, not output
    let hung = Arc::new(AtomicU64::new(0));
    for &(rule, krate, f) in PROPS {
        if (which != "all" && which != krate) || (!only.is_empty() && !only.contains(&rule)) {
            continue;
        }
        let (tx, rx) = mpsc::channel();
        let start = Instant::now();
        std::thread::spawn(move || {
            let _ = tx.send(f(profile, seed, cases));
        });
        let o = rx.recv_timeout(timeout).unwrap_or_else(|_| {
            hung.fetch_add(1, Ordering::SeqCst);
            Outcome { status: "hang", calls_to_first_failure: 0, calls: 0, row: None,
                      message: format!("the property did not finish within {} s", timeout.as_secs()) }
        });
        let row = match &o.row {
            None => "null".to_string(),
            Some(r) => format!("{{{}}}", r.iter().map(|(k, v)| format!("{}: {}", json_str(k), json_str(v))).collect::<Vec<_>>().join(", ")),
        };
        println!(
            "{{\"rule\": {}, \"crate\": {}, \"profile\": {}, \"status\": {}, \"calls_to_first_failure\": {}, \"calls\": {}, \"elapsed_ms\": {}, \"row\": {}, \"message\": {}}}",
            json_str(rule), json_str(krate), json_str(&format!("{profile:?}").to_lowercase()), json_str(o.status),
            o.calls_to_first_failure, o.calls, start.elapsed().as_millis(), row, json_str(&o.message)
        );
    }
    std::process::exit(0); // threads of hung properties are still running
}
