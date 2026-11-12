//! THE TYPED RUST READING OF EVERY VOCABULARY PIECE (plan node E1). Hand-written ONCE, like
//! ../../wallet-bdd/src/pieces.rs; nothing here is about one rule.
//!
//! `clausal` compiles a sentence to a composition tree (../../build/trees.json). pieces.rs evaluates that tree
//! with dynamically typed values, which a bounded model checker cannot digest (JSON, strings, boxed values).
//! This module gives each piece the same reading as a plain typed function, and `clausal evidence` turns each
//! tree into straight-line Rust that calls these functions (checks.rs, GENERATED). The generated predicate is
//! what the generated property test asserts and what the generated Kani harness asserts.
//!
//! It is therefore a THIRD reading of each piece by the same author. It is not trusted: the property test
//! compares it with the tree evaluator of pieces.rs at every generated case (and pieces.rs is compared with the
//! Lean definitions on the grid), and reports any difference as READING MISMATCH.
//!
//! Numbers are u128 so that sums of u64 balances cannot wrap. A ledger is seen as its balances (`&[u64]`),
//! a wallet as its balance (`u64`), a transfer as `(sender, receiver, amount)`.
//! Loops are written with indexes on purpose: Kani unwinds them to the size bound of the harness.
#![allow(dead_code)]

pub use ledger::{Ledger, Transfer};

pub type T = (usize, usize, u64);
pub const MAX: u128 = u64::MAX as u128;

/// A wallet operation's answer.
#[derive(Clone, Copy, PartialEq, Debug)]
pub enum WAns {
    Ok,
    InsufficientFunds,
    Overflow,
}

/// One point of a reading, as the grid comparison prints it: per unit its scope, per claim the relation between
/// two calls (two-run frames) and the claim. `scoped`: some claim is about this point. `holds`: every claim holds.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Pt<const W: usize> {
    pub bits: [bool; W],
    pub scoped: bool,
    pub holds: bool,
}

// ---------------------------------------------------------------------------------------------- collections

/// A named collection, read item by item.
pub trait Coll: Copy {
    type Item: Copy + PartialEq;
    fn n(&self) -> usize;
    fn at(&self, i: usize) -> Self::Item;
}
impl Coll for &[u64] {
    type Item = u128;
    fn n(&self) -> usize {
        self.len()
    }
    fn at(&self, i: usize) -> u128 {
        self[i] as u128
    }
}
impl Coll for &[T] {
    type Item = T;
    fn n(&self) -> usize {
        self.len()
    }
    fn at(&self, i: usize) -> T {
        self[i]
    }
}
impl Coll for Option<T> {
    type Item = T;
    fn n(&self) -> usize {
        self.is_some() as usize
    }
    fn at(&self, _: usize) -> T {
        self.unwrap()
    }
}
impl<const N: usize> Coll for [u128; N] {
    type Item = u128;
    fn n(&self) -> usize {
        N
    }
    fn at(&self, i: usize) -> u128 {
        self[i]
    }
}
/// "the accounts": the account numbers 0, 1, ... of a ledger with that many accounts.
#[derive(Clone, Copy)]
pub struct Accounts(pub usize);
impl Coll for Accounts {
    type Item = u128;
    fn n(&self) -> usize {
        self.0
    }
    fn at(&self, i: usize) -> u128 {
        i as u128
    }
}

pub fn all<C: Coll>(c: C, mut p: impl FnMut(C::Item) -> bool) -> bool {
    let mut i = 0;
    while i < c.n() {
        if !p(c.at(i)) {
            return false;
        }
        i += 1;
    }
    true
}
pub fn any<C: Coll>(c: C, mut p: impl FnMut(C::Item) -> bool) -> bool {
    let mut i = 0;
    while i < c.n() {
        if p(c.at(i)) {
            return true;
        }
        i += 1;
    }
    false
}
/// "the first X of XS": false if there is none.
pub fn first<C: Coll>(c: C, mut p: impl FnMut(C::Item) -> bool) -> bool {
    c.n() > 0 && p(c.at(0))
}
pub fn has<C: Coll>(c: C, x: C::Item) -> bool {
    any(c, |y| y == x)
}
/// Two collections are the same: the same items in the same order.
pub fn same<A: Coll, B: Coll<Item = A::Item>>(a: A, b: B) -> bool {
    if a.n() != b.n() {
        return false;
    }
    let mut i = 0;
    while i < a.n() {
        if a.at(i) != b.at(i) {
            return false;
        }
        i += 1;
    }
    true
}
/// "the total / the aggregate value": the sum.
pub fn sum<C: Coll<Item = u128>>(c: C) -> u128 {
    let mut s: u128 = 0;
    let mut i = 0;
    while i < c.n() {
        s += c.at(i);
        i += 1;
    }
    s
}

// ---------------------------------------------------------------------------------------------- the ledger's own words

/// "the balance of account k": 0 if there is no such account.
pub fn bal_of(l: &[u64], k: u128) -> u128 {
    if k < l.len() as u128 {
        l[k as usize] as u128
    } else {
        0
    }
}
/// "the balance of account i" as a lookup would report it.
pub fn balance_at(l: &[u64], i: u128) -> Option<u128> {
    if i < l.len() as u128 {
        Some(l[i as usize] as u128)
    } else {
        None
    }
}
/// "valid on": both accounts exist and differ, the sender covers the amount, the receiver's balance stays within u64.
pub fn valid(l: &[u64], t: T) -> bool {
    let (from, to, amount) = t;
    from < l.len() && to < l.len() && from != to && amount as u128 <= l[from] as u128 && l[to] as u128 + amount as u128 <= MAX
}
/// "the transfer at which the batch stopped": the transfer at the position the count points to, if there is one.
pub fn stopped_at(b: &[T], n: u128) -> Option<T> {
    if n < b.len() as u128 {
        Some(b[n as usize])
    } else {
        None
    }
}
/// "internal": every account the transfer names is an account of the ledger.
pub fn internal_l_apply(l: &[u64], t: T) -> bool {
    t.0 < l.len() && t.1 < l.len()
}

// ---------------------------------------------------------------------------------------------- operations

/// One call on the COMPILED crate. `None`: it gave no answer (it panicked). Under Kani a panic is not caught:
/// Kani reports it as a failed check of its own, which the runner reads as "no answer".
#[cfg(not(kani))]
pub fn guard<R>(f: impl FnOnce() -> R) -> Option<R> {
    std::panic::catch_unwind(std::panic::AssertUnwindSafe(f)).ok()
}
#[cfg(kani)]
pub fn guard<R>(f: impl FnOnce() -> R) -> Option<R> {
    Some(f())
}

fn outcome(r: Result<(), wallet::WalletError>) -> WAns {
    match r {
        Ok(()) => WAns::Ok,
        Err(wallet::WalletError::InsufficientFunds) => WAns::InsufficientFunds,
        Err(wallet::WalletError::Overflow) => WAns::Overflow,
    }
}

pub fn w_transfer(s: u64, d: u64, amount: u64) -> Option<(WAns, u64, u64)> {
    guard(move || {
        let (mut s, mut d) = (wallet::Wallet { balance: s }, wallet::Wallet { balance: d });
        let r = wallet::transfer(&mut s, &mut d, amount);
        (outcome(r), s.balance, d.balance)
    })
}
pub fn w_deposit(w: u64, amount: u64) -> Option<(WAns, u64)> {
    guard(move || {
        let mut w = wallet::Wallet { balance: w };
        let r = w.deposit(amount);
        (outcome(r), w.balance)
    })
}
pub fn w_withdraw(w: u64, amount: u64) -> Option<(WAns, u64)> {
    guard(move || {
        let mut w = wallet::Wallet { balance: w };
        let r = w.withdraw(amount);
        (outcome(r), w.balance)
    })
}
pub fn ctr_bump(c: u64, amount: u64) -> Option<(bool, u64)> {
    guard(move || {
        let mut c = counter::Counter { count: c };
        let ok = c.bump(amount);
        (ok, c.count)
    })
}
pub fn l_apply_batch(mut l: Ledger, b: &[Transfer]) -> Option<(u128, Ledger)> {
    guard(move || {
        let n = l.apply_batch(b);
        (n as u128, l)
    })
}
pub fn l_apply_all(mut l: Ledger, b: &[Transfer]) -> Option<(bool, Ledger)> {
    guard(move || {
        let ok = l.apply_all(b);
        (ok, l)
    })
}
pub fn l_apply(mut l: Ledger, t: T) -> Option<(bool, Ledger)> {
    guard(move || {
        let ok = l.apply(&Transfer { from: t.0, to: t.1, amount: t.2 });
        (ok, l)
    })
}
pub fn l_total(l: Ledger) -> Option<(Option<u128>, Ledger)> {
    guard(move || {
        let r = l.total().map(|v| v as u128);
        (r, l)
    })
}
pub fn l_lookup(l: Ledger, i: u64) -> Option<(Option<u128>, Ledger)> {
    guard(move || {
        let r = l.balance(i as usize).map(|v| v as u128);
        (r, l)
    })
}

/// A ledger of the crate under test with these balances (used where the harness has not built one itself).
pub fn mk_ledger(l: &[u64]) -> Ledger {
    let mut balances = Vec::with_capacity(l.len());
    let mut i = 0;
    while i < l.len() {
        balances.push(l[i]);
        i += 1;
    }
    Ledger { balances }
}
pub fn mk_batch(b: &[T]) -> Vec<Transfer> {
    let mut out = Vec::with_capacity(b.len());
    let mut i = 0;
    while i < b.len() {
        out.push(Transfer { from: b[i].0, to: b[i].1, amount: b[i].2 });
        i += 1;
    }
    out
}

// ---------------------------------------------------------------------------------------------- the defaults

#[derive(Clone, Copy, PartialEq, Debug)]
pub enum Calls {
    Every,
    Accepted,
    Rejected,
}

/// THE DEFAULTS (the counterpart of `Frames.Op.HoldsAt` and of pieces.rs `holds_at`): what a frame says of one
/// call that is in scope. `r`: None if the call gave no answer, else (whether the answer is an acceptance,
/// whether the frame's content holds). Every call: it must answer and the content holds. Accepted / rejected
/// calls only: IF it answers with that kind of answer, the content holds.
pub fn holds_at(calls: Calls, r: Option<(bool, bool)>) -> bool {
    match (r, calls) {
        (None, Calls::Every) => false,
        (None, _) => true,
        (Some((_, q)), Calls::Every) => q,
        (Some((acc, q)), Calls::Accepted) => !acc || q,
        (Some((acc, q)), Calls::Rejected) => acc || q,
    }
}

/// The same for two calls, both in scope and related as stated (`Frames.Op.HoldsAt2`). `r`: None if either call
/// gave no answer, else (first accepted, second accepted, content).
pub fn holds_at2(calls: Calls, r: Option<(bool, bool, bool)>) -> bool {
    match (r, calls) {
        (Some((_, _, q)), Calls::Every) => q,
        (Some((a1, a2, q)), Calls::Accepted) => !(a1 && a2) || q,
        (Some((a1, a2, q)), Calls::Rejected) => !(!a1 && !a2) || q,
        (None, Calls::Every) => false,
        (None, _) => true,
    }
}

// ---------------------------------------------------------------------------------------------- ties of a sequence

/// "the same input": the second call of a tied sequence is given the first call's input again.
pub fn tie_same_input<X: Copy>(first: X) -> X {
    first
}

// ---------------------------------------------------------------------------------------------- relations between two calls

fn same_route(s: &[u64], a: T, s2: &[u64], a2: T) -> bool {
    same(s2, s) && a2.0 == a.0 && a2.1 == a.1
}
pub fn var_l_smaller_amount(s: &[u64], a: T, s2: &[u64], a2: T) -> bool {
    same_route(s, a, s2, a2) && a2.2 <= a.2
}
pub fn var_l_larger_amount(s: &[u64], a: T, s2: &[u64], a2: T) -> bool {
    same_route(s, a, s2, a2) && a.2 <= a2.2
}
pub fn var_l_only_amount_differs(s: &[u64], a: T, s2: &[u64], a2: T) -> bool {
    same_route(s, a, s2, a2)
}
pub fn var_l_agrees_at_account(s: &[u64], a: u64, s2: &[u64], a2: u64) -> bool {
    a2 == a && balance_at(s2, a as u128) == balance_at(s, a as u128)
}
pub fn var_l_extended(s: &[u64], a: u64, s2: &[u64], a2: u64) -> bool {
    if a2 != a || s2.len() < s.len() {
        return false;
    }
    let mut i = 0;
    while i < s.len() {
        if s2[i] != s[i] {
            return false;
        }
        i += 1;
    }
    true
}

// ---------------------------------------------------------------------------------------------- reference functions

/// What a reference function says the call should answer and leave: (answer, the ledger it leaves, or `None` for
/// "the ledger as it was"). `None` overall: the reference itself gave no answer, and then nothing agrees with it.
/// `fresh` is a ledger of the crate holding the state before the call, for the references that are another
/// operation of the crate (the harness builds it; `s` is the same state as a view).
pub type Ref<A> = Option<(A, Option<Ledger>)>;

pub fn ref_l_ref_lookup(_fresh: Ledger, s: &[u64], a: u64) -> Ref<Option<u128>> {
    Some((balance_at(s, a as u128), None))
}
pub fn ref_l_ref_lookup_zero(_fresh: Ledger, s: &[u64], a: u64) -> Ref<Option<u128>> {
    Some((Some(bal_of(s, a as u128)), None))
}
/// "the same batch applied transfer by transfer and kept only if every transfer is applied"
pub fn ref_l_ref_whole_by_batch(fresh: Ledger, _s: &[u64], b: &[Transfer]) -> Ref<bool> {
    match l_apply_batch(fresh, b) {
        Some((n, after)) if n == b.len() as u128 => Some((true, Some(after))),
        _ => Some((false, None)),
    }
}
/// "its transfers applied one at a time until one is rejected": the ledger is the one those calls leave.
pub fn ref_l_ref_batch_by_transfers(fresh: Ledger, _s: &[u64], b: &[Transfer]) -> Ref<u128> {
    let mut cur = fresh;
    let mut n: u128 = 0;
    let mut i = 0;
    while i < b.len() {
        // a call that gives no answer leaves the ledger as it was before it (under Kani a panic is a failed check
        // of Kani's own, so no copy is needed there)
        #[cfg(not(kani))]
        let before = mk_ledger(&cur.balances);
        match l_apply(cur, (b[i].from, b[i].to, b[i].amount)) {
            Some((true, after)) => {
                cur = after;
                n += 1;
            }
            Some((false, after)) => {
                cur = after;
                break;
            }
            None => {
                #[cfg(not(kani))]
                return Some((n, Some(before)));
                #[cfg(kani)]
                unreachable!();
            }
        }
        i += 1;
    }
    Some((n, Some(cur)))
}
