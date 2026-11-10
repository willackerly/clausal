//! Differential oracle (NOT one of the four arms): run the mutated crate and the original on
//! the same inputs and report the first input on which they behave differently (different
//! return value, different state afterwards, or one panics and the other does not).
//!
//!   cargo run --quiet -- [--extra 1000003,7] [--random 200000] [--timeout-secs 120]
//!
//! Prints one JSON line per function: {"fn", "differs", "witness", "tried"} and, if the mutated
//! code hangs, {"fn", "differs": true, "witness": "hang"}.
//!
//! Inputs: (1) every combination of a set of interesting integers (small values, powers of two,
//! values near u64::MAX, every integer literal of the mutated source and its neighbours, passed
//! with --extra); (2) every small ledger with every batch of at most two transfers over small
//! values; (3) pseudo-random inputs, half of them near the ends of the range.
//! "No difference found" is not a proof of equivalence; TRADES.md says which survivors were
//! argued equivalent by reading the diff.
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::sync::mpsc;
use std::time::Duration;

const MAX: u64 = u64::MAX;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, n: u64) -> u64 {
        if n == 0 { 0 } else { self.next() % n }
    }
    /// a u64: a quarter small, a quarter near the top, half anywhere
    fn amount(&mut self) -> u64 {
        match self.below(4) {
            0 => self.below(6),
            1 => MAX - self.below(6),
            _ => self.next(),
        }
    }
}

#[derive(Debug, PartialEq)]
enum R<T> {
    Value(T),
    Panic,
}
fn guard<T>(f: impl FnOnce() -> T) -> R<T> {
    match catch_unwind(AssertUnwindSafe(f)) {
        Ok(v) => R::Value(v),
        Err(_) => R::Panic,
    }
}

type T = (usize, usize, u64);

fn w_err(r: Result<(), wallet::WalletError>) -> u8 {
    match r { Ok(()) => 0, Err(wallet::WalletError::InsufficientFunds) => 1, Err(wallet::WalletError::Overflow) => 2 }
}
fn o_err(r: Result<(), wallet_orig::WalletError>) -> u8 {
    match r { Ok(()) => 0, Err(wallet_orig::WalletError::InsufficientFunds) => 1, Err(wallet_orig::WalletError::Overflow) => 2 }
}

fn deposit(a: u64, n: u64) -> Option<String> {
    let m = guard(|| { let mut w = wallet::Wallet { balance: a }; let r = w_err(w.deposit(n)); (r, w.balance) });
    let o = guard(|| { let mut w = wallet_orig::Wallet { balance: a }; let r = o_err(w.deposit(n)); (r, w.balance) });
    (m != o).then(|| format!("deposit: balance {a}, amount {n}: original {o:?}, mutant {m:?}"))
}
fn withdraw(a: u64, n: u64) -> Option<String> {
    let m = guard(|| { let mut w = wallet::Wallet { balance: a }; let r = w_err(w.withdraw(n)); (r, w.balance) });
    let o = guard(|| { let mut w = wallet_orig::Wallet { balance: a }; let r = o_err(w.withdraw(n)); (r, w.balance) });
    (m != o).then(|| format!("withdraw: balance {a}, amount {n}: original {o:?}, mutant {m:?}"))
}
fn transfer(a: u64, b: u64, n: u64) -> Option<String> {
    let m = guard(|| {
        let (mut s, mut d) = (wallet::Wallet { balance: a }, wallet::Wallet { balance: b });
        let r = w_err(wallet::transfer(&mut s, &mut d, n));
        (r, s.balance, d.balance)
    });
    let o = guard(|| {
        let (mut s, mut d) = (wallet_orig::Wallet { balance: a }, wallet_orig::Wallet { balance: b });
        let r = o_err(wallet_orig::transfer(&mut s, &mut d, n));
        (r, s.balance, d.balance)
    });
    (m != o).then(|| format!("transfer: balances {a} and {b}, amount {n}: original {o:?}, mutant {m:?}"))
}

fn mb(b: &[T]) -> Vec<ledger::Transfer> {
    b.iter().map(|&(from, to, amount)| ledger::Transfer { from, to, amount }).collect()
}
fn ob(b: &[T]) -> Vec<ledger_orig::Transfer> {
    b.iter().map(|&(from, to, amount)| ledger_orig::Transfer { from, to, amount }).collect()
}

fn l_balance(bs: &[u64], i: usize) -> Option<String> {
    let m = guard(|| ledger::Ledger { balances: bs.to_vec() }.balance(i));
    let o = guard(|| ledger_orig::Ledger { balances: bs.to_vec() }.balance(i));
    (m != o).then(|| format!("balance: ledger {bs:?}, account {i}: original {o:?}, mutant {m:?}"))
}
fn l_total(bs: &[u64]) -> Option<String> {
    let m = guard(|| ledger::Ledger { balances: bs.to_vec() }.total());
    let o = guard(|| ledger_orig::Ledger { balances: bs.to_vec() }.total());
    (m != o).then(|| format!("total: ledger {bs:?}: original {o:?}, mutant {m:?}"))
}
fn l_apply(bs: &[u64], t: T) -> Option<String> {
    let m = guard(|| { let mut l = ledger::Ledger { balances: bs.to_vec() }; let r = l.apply(&mb(&[t])[0]); (r, l.balances) });
    let o = guard(|| { let mut l = ledger_orig::Ledger { balances: bs.to_vec() }; let r = l.apply(&ob(&[t])[0]); (r, l.balances) });
    (m != o).then(|| format!("apply: ledger {bs:?}, transfer {t:?}: original {o:?}, mutant {m:?}"))
}
fn l_batch(bs: &[u64], b: &[T]) -> Option<String> {
    let m = guard(|| { let mut l = ledger::Ledger { balances: bs.to_vec() }; let r = l.apply_batch(&mb(b)); (r, l.balances) });
    let o = guard(|| { let mut l = ledger_orig::Ledger { balances: bs.to_vec() }; let r = l.apply_batch(&ob(b)); (r, l.balances) });
    (m != o).then(|| format!("apply_batch: ledger {bs:?}, batch {b:?}: original {o:?}, mutant {m:?}"))
}
fn l_all(bs: &[u64], b: &[T]) -> Option<String> {
    let m = guard(|| { let mut l = ledger::Ledger { balances: bs.to_vec() }; let r = l.apply_all(&mb(b)); (r, l.balances) });
    let o = guard(|| { let mut l = ledger_orig::Ledger { balances: bs.to_vec() }; let r = l.apply_all(&ob(b)); (r, l.balances) });
    (m != o).then(|| format!("apply_all: ledger {bs:?}, batch {b:?}: original {o:?}, mutant {m:?}"))
}

/// Every list of at most `max_len` values of `vals`.
fn lists<V: Clone>(vals: &[V], max_len: usize) -> Vec<Vec<V>> {
    let mut out = vec![vec![]];
    let mut last = vec![vec![]];
    for _ in 0..max_len {
        let mut next = Vec::new();
        for l in &last {
            for v in vals {
                let mut l2: Vec<V> = l.clone();
                l2.push(v.clone());
                next.push(l2);
            }
        }
        out.extend(next.iter().cloned());
        last = next;
    }
    out
}

fn rand_ledger(r: &mut Rng) -> Vec<u64> {
    (0..r.below(7)).map(|_| r.amount()).collect()
}
fn rand_transfer(r: &mut Rng, len: usize) -> T {
    (r.below(len as u64 + 2) as usize, r.below(len as u64 + 2) as usize, r.amount())
}
fn rand_batch(r: &mut Rng, len: usize) -> Vec<T> {
    (0..r.below(7)).map(|_| rand_transfer(r, len)).collect()
}

type Search = Box<dyn FnOnce(&[u64], u64) -> (Option<String>, u64) + Send>;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let arg = |name: &str, default: &str| -> String {
        args.iter().position(|a| a == name).and_then(|i| args.get(i + 1)).cloned().unwrap_or_else(|| default.to_string())
    };
    let random: u64 = arg("--random", "200000").parse().unwrap();
    let timeout = Duration::from_secs(arg("--timeout-secs", "120").parse().unwrap());
    let mut ints: Vec<u64> = vec![0, 1, 2, 3, 4, 5, 7, 10, 100, (1 << 32) - 1, 1 << 32, (1 << 63) - 1, 1 << 63, (1 << 63) + 1];
    ints.extend((0..6).map(|k| MAX - k));
    for e in arg("--extra", "").split(',').filter_map(|x| x.parse::<u64>().ok()) {
        ints.extend([e.wrapping_sub(1), e, e.wrapping_add(1)]);
    }
    ints.sort();
    ints.dedup();
    std::panic::set_hook(Box::new(|_| {}));

    let searches: Vec<(&str, Search)> = vec![
        ("wallet::deposit", Box::new(|ints, random| {
            let mut n = 0;
            for &a in ints { for &x in ints { n += 1; if let Some(w) = deposit(a, x) { return (Some(w), n); } } }
            let mut r = Rng(0x9e3779b97f4a7c15);
            for _ in 0..random { n += 1; if let Some(w) = deposit(r.amount(), r.amount()) { return (Some(w), n); } }
            (None, n)
        })),
        ("wallet::withdraw", Box::new(|ints, random| {
            let mut n = 0;
            for &a in ints { for &x in ints { n += 1; if let Some(w) = withdraw(a, x) { return (Some(w), n); } } }
            let mut r = Rng(0x9e3779b97f4a7c16);
            for _ in 0..random { n += 1; if let Some(w) = withdraw(r.amount(), r.amount()) { return (Some(w), n); } }
            (None, n)
        })),
        ("wallet::transfer", Box::new(|ints, random| {
            let mut n = 0;
            for &a in ints { for &b in ints { for &x in ints { n += 1; if let Some(w) = transfer(a, b, x) { return (Some(w), n); } } } }
            let mut r = Rng(0x9e3779b97f4a7c17);
            for _ in 0..random { n += 1; if let Some(w) = transfer(r.amount(), r.amount(), r.amount()) { return (Some(w), n); } }
            (None, n)
        })),
        ("ledger::balance", Box::new(|ints, random| {
            let mut n = 0;
            for bs in lists(&[0u64, 1, MAX], 4) {
                for i in (0..7).chain([usize::MAX - 1, usize::MAX]) { n += 1; if let Some(w) = l_balance(&bs, i) { return (Some(w), n); } }
            }
            let _ = ints;
            let mut r = Rng(0x9e3779b97f4a7c18);
            for _ in 0..random { n += 1; let bs = rand_ledger(&mut r); let i = r.below(bs.len() as u64 + 2) as usize; if let Some(w) = l_balance(&bs, i) { return (Some(w), n); } }
            (None, n)
        })),
        ("ledger::total", Box::new(|ints, random| {
            let mut n = 0;
            for bs in lists(&[0u64, 1, 2, MAX - 1, MAX], 5) { n += 1; if let Some(w) = l_total(&bs) { return (Some(w), n); } }
            for bs in lists(ints, 2) { n += 1; if let Some(w) = l_total(&bs) { return (Some(w), n); } }
            let mut r = Rng(0x9e3779b97f4a7c19);
            for _ in 0..random { n += 1; let bs = rand_ledger(&mut r); if let Some(w) = l_total(&bs) { return (Some(w), n); } }
            (None, n)
        })),
        ("ledger::apply", Box::new(|ints, random| {
            let mut n = 0;
            for bs in lists(&[0u64, 1, 2, MAX - 1, MAX], 3) {
                for from in 0..5 { for to in 0..5 { for &x in ints { n += 1; if let Some(w) = l_apply(&bs, (from, to, x)) { return (Some(w), n); } } } }
            }
            for &a in ints { for &b in ints { for &x in ints { n += 1; if let Some(w) = l_apply(&[a, b], (0, 1, x)) { return (Some(w), n); } } } }
            let mut r = Rng(0x9e3779b97f4a7c1a);
            for _ in 0..random { n += 1; let bs = rand_ledger(&mut r); let t = rand_transfer(&mut r, bs.len()); if let Some(w) = l_apply(&bs, t) { return (Some(w), n); } }
            (None, n)
        })),
        ("ledger::apply_batch", Box::new(|ints, random| {
            let mut n = 0;
            let mut ts: Vec<T> = Vec::new();
            for from in 0..4 { for to in 0..4 { for x in [0u64, 1, 2, MAX] { ts.push((from, to, x)); } } }
            let batches = lists(&ts, 2);
            for bs in lists(&[0u64, 1, 2, MAX], 3) { for b in &batches { n += 1; if let Some(w) = l_batch(&bs, b) { return (Some(w), n); } } }
            for &x in ints { for &y in ints { n += 1; if let Some(w) = l_batch(&[x, y, 0], &[(0, 1, x), (1, 2, y), (2, 0, 1)]) { return (Some(w), n); } } }
            let mut r = Rng(0x9e3779b97f4a7c1b);
            for _ in 0..random { n += 1; let bs = rand_ledger(&mut r); let b = rand_batch(&mut r, bs.len()); if let Some(w) = l_batch(&bs, &b) { return (Some(w), n); } }
            (None, n)
        })),
        ("ledger::apply_all", Box::new(|ints, random| {
            let mut n = 0;
            let mut ts: Vec<T> = Vec::new();
            for from in 0..4 { for to in 0..4 { for x in [0u64, 1, 2, MAX] { ts.push((from, to, x)); } } }
            let batches = lists(&ts, 2);
            for bs in lists(&[0u64, 1, 2, MAX], 3) { for b in &batches { n += 1; if let Some(w) = l_all(&bs, b) { return (Some(w), n); } } }
            for &x in ints { for &y in ints { n += 1; if let Some(w) = l_all(&[x, y, 0], &[(0, 1, x), (1, 2, y), (2, 0, 1)]) { return (Some(w), n); } } }
            let mut r = Rng(0x9e3779b97f4a7c1c);
            for _ in 0..random { n += 1; let bs = rand_ledger(&mut r); let b = rand_batch(&mut r, bs.len()); if let Some(w) = l_all(&bs, &b) { return (Some(w), n); } }
            (None, n)
        })),
    ];
    for (name, search) in searches {
        let (tx, rx) = mpsc::channel();
        let ints2 = ints.clone();
        std::thread::spawn(move || { let _ = tx.send(search(&ints2, random)); });
        match rx.recv_timeout(timeout) {
            Ok((w, n)) => println!("{{\"fn\": \"{name}\", \"differs\": {}, \"witness\": {}, \"tried\": {n}}}", w.is_some(),
                                   w.map(|s| format!("\"{}\"", s.replace('\\', "\\\\").replace('"', "'"))).unwrap_or("null".into())),
            Err(_) => println!("{{\"fn\": \"{name}\", \"differs\": true, \"witness\": \"hang: no answer within {} s\", \"tried\": 0}}", timeout.as_secs()),
        }
    }
    std::process::exit(0);
}
