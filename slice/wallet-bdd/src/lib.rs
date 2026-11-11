//! The Rust-side reading of each Given/Then glossary phrase, as pure predicates.
//!
//! This is the SECOND hand-written reading of each phrase; the first is the Lean
//! definition in lean/Wallet/Vocab.lean (wallet) or lean/Ledger/Vocab.lean (ledger). The cucumber steps (tests/bdd.rs) assert
//! these predicates, and tests/readings.rs evaluates them on a grid of arguments so
//! the report can compare them, point by point, with the Lean definitions.
//! Balances and amounts are u64; sums are taken in u128 so they cannot wrap.

/// The Rust reading of every vocabulary PIECE and the evaluator of composition trees (what the cucumber steps and
/// the grid comparison use). The predicates below are the older whole-phrase readings of glossary.yaml, kept
/// because the flat statements are still compared with them phrase by phrase (tests/readings.rs).
pub mod pieces;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome {
    Ok,
    InsufficientFunds,
    Overflow,
}

impl Outcome {
    pub fn parse(s: &str) -> Option<Outcome> {
        match s {
            "ok" => Some(Outcome::Ok),
            "insufficient funds" => Some(Outcome::InsufficientFunds),
            "overflow" => Some(Outcome::Overflow),
            _ => None,
        }
    }
}

// glossary: G-balance      "{w} has a balance of {n}"
pub fn has_balance(pre: u64, n: u64) -> bool {
    pre == n
}
// glossary: G-covers       "{n} is not more than {w}'s balance"
pub fn covers(pre: u64, n: u64) -> bool {
    n <= pre
}
// glossary: G-exceeds      "{n} is more than {w}'s balance"
pub fn exceeds(n: u64, pre: u64) -> bool {
    n > pre
}
// glossary: G-room         "{w}'s balance plus {n} does not exceed the maximum"
pub fn room_for(pre: u64, n: u64) -> bool {
    pre.checked_add(n).is_some()
}
// glossary: G-noroom       "{w}'s balance plus {n} exceeds the maximum"
pub fn no_room_for(pre: u64, n: u64) -> bool {
    pre.checked_add(n).is_none()
}
// glossary: T-ok           "the operation succeeds"
pub fn succeeds(o: Outcome) -> bool {
    o == Outcome::Ok
}
// glossary: T-err          "the operation is rejected with {e}"   (e is an error, never Ok)
pub fn rejected_with(o: Outcome, e: Outcome) -> bool {
    e != Outcome::Ok && o == e
}
// glossary: T-dec          "{w}'s balance is decreased by {n}"
pub fn decreased_by(pre: u64, post: u64, n: u64) -> bool {
    post as u128 + n as u128 == pre as u128
}
// glossary: T-inc          "{w}'s balance is increased by {n}"
pub fn increased_by(pre: u64, post: u64, n: u64) -> bool {
    post as u128 == pre as u128 + n as u128
}
// glossary: T-same         "{w}'s balance is unchanged"
pub fn unchanged(pre: u64, post: u64) -> bool {
    post == pre
}
// glossary: T-total        "the total of all balances is unchanged"
pub fn total_unchanged(pre: &[u64], post: &[u64]) -> bool {
    let sum = |xs: &[u64]| xs.iter().map(|&v| v as u128).sum::<u128>();
    sum(post) == sum(pre)
}

// ====================================================================== ledger
// The second reading of the ledger phrases (first: lean/Ledger/Vocab.lean, namespace LVocab).
// A ledger is its list of balances; a transfer is (from, to, amount).

pub type Transfer = (usize, usize, u64);

/// The balance of account `i` (0 if there is no such account).
pub fn bal(l: &[u64], i: usize) -> u64 {
    l.get(i).copied().unwrap_or(0)
}
pub fn total(l: &[u64]) -> u128 {
    l.iter().map(|&v| v as u128).sum()
}
/// A transfer the ledger can carry out exactly.
pub fn valid(l: &[u64], t: Transfer) -> bool {
    let (from, to, amount) = t;
    from < l.len() && to < l.len() && from != to && amount <= bal(l, from) && bal(l, to).checked_add(amount).is_some()
}

// glossary: LG-holds         "ledger {l} holds the balances {bs}"
pub fn l_holds(pre: &[u64], bs: &[u64]) -> bool {
    pre == bs
}
// glossary: LG-sums-to       "the balances of ledger {l} add up to {s}"
pub fn l_sums_to(pre: &[u64], s: u64) -> bool {
    total(pre) == s as u128
}
// glossary: LG-sum-too-big   "the balances of ledger {l} add up to more than the maximum"
pub fn l_sum_too_big(pre: &[u64]) -> bool {
    total(pre) > u64::MAX as u128
}
// glossary: LG-account       "{i} is an account of ledger {l}"
pub fn l_is_account(pre: &[u64], i: usize) -> bool {
    i < pre.len()
}
// glossary: LG-no-account    "{i} is not an account of ledger {l}"
pub fn l_not_account(pre: &[u64], i: usize) -> bool {
    i >= pre.len()
}
// glossary: LG-valid         "the transfer {t} is valid on ledger {l}"
pub fn l_valid_on(pre: &[u64], t: Transfer) -> bool {
    valid(pre, t)
}
// glossary: LG-invalid       "the transfer {t} is not valid on ledger {l}"
pub fn l_invalid_on(pre: &[u64], t: Transfer) -> bool {
    !valid(pre, t)
}
// glossary: LG-first-invalid "the first transfer of {b} is not valid on ledger {l}"
pub fn l_first_invalid(pre: &[u64], b: &[Transfer]) -> bool {
    match b.first() {
        Some(&t) => !valid(pre, t),
        None => false,
    }
}
// glossary: LG-all-valid     "every transfer of {b} is valid on ledger {l}"
pub fn l_all_valid(pre: &[u64], b: &[Transfer]) -> bool {
    b.iter().all(|&t| valid(pre, t))
}
// glossary: LT-total-same    "the total of ledger {l}'s balances is unchanged"
pub fn l_total_unchanged(pre: &[u64], post: &[u64]) -> bool {
    total(post) == total(pre)
}
// glossary: LT-same          "ledger {l} is unchanged"
pub fn l_unchanged(pre: &[u64], post: &[u64]) -> bool {
    post == pre
}
// glossary: LT-now-holds     "ledger {l} now holds the balances {bs}"
pub fn l_now_holds(post: &[u64], bs: &[u64]) -> bool {
    post == bs
}
// glossary: LT-at-most       "the number of transfers applied is at most the length of {b}"
pub fn l_applied_at_most(n: usize, b: &[Transfer]) -> bool {
    n <= b.len()
}
// glossary: LT-none-applied  "no transfer is applied"
pub fn l_applied_none(n: usize) -> bool {
    n == 0
}
// glossary: LT-all-applied   "every transfer of {b} is applied"
pub fn l_applied_all(n: usize, b: &[Transfer]) -> bool {
    n == b.len()
}
// glossary: LT-exactly       "exactly {k} transfers are applied"
pub fn l_applied_exactly(n: usize, k: usize) -> bool {
    n == k
}
// glossary: LT-result        "the result is {s}"
pub fn l_result_is(o: Option<u64>, s: u64) -> bool {
    o == Some(s)
}
// glossary: LT-no-result     "there is no result"
pub fn l_no_result(o: Option<u64>) -> bool {
    o.is_none()
}
// glossary: LT-some-result   "there is a result"
pub fn l_some_result(o: Option<u64>) -> bool {
    o.is_some()
}
// glossary: LT-balance       "the result is the balance of account {i} of ledger {l}"
pub fn l_result_is_balance(o: Option<u64>, pre: &[u64], i: usize) -> bool {
    o.is_some() && o == pre.get(i).copied()
}
// glossary: LT-stops-at-invalid "the batch {b} has stopped only at a transfer that is not valid on ledger {l} as it now stands"
pub fn l_stops_at_invalid(n: usize, b: &[Transfer], post: &[u64]) -> bool {
    match b.get(n) {
        Some(&t) => !valid(post, t),
        None => true,
    }
}
// glossary: LT-same-if-rejected "if it is rejected, ledger {l} is unchanged"
pub fn l_unchanged_if_rejected(ok: bool, pre: &[u64], post: &[u64]) -> bool {
    ok || post == pre
}
// glossary: LT-accepted      "it is accepted"
pub fn l_accepted(ok: bool) -> bool {
    ok
}
// glossary: LT-rejected      "it is rejected"
pub fn l_rejected(ok: bool) -> bool {
    !ok
}
// glossary: LT-moved         "the amount of {t} has moved between its accounts in ledger {l} and no other balance changed"
pub fn l_moved(pre: &[u64], post: &[u64], t: Transfer) -> bool {
    let (from, to, amount) = t;
    post.len() == pre.len()
        && bal(post, from) as u128 + amount as u128 == bal(pre, from) as u128
        && bal(post, to) as u128 == bal(pre, to) as u128 + amount as u128
        && (0..pre.len()).all(|k| k == from || k == to || bal(post, k) == bal(pre, k))
}

/// Parsers for the literals of glossary.yaml: `[1, 2]`, `0->1:30`, `[0->1:30, 1->2:50]`, `some 3` / `none`.
pub fn parse_balances(s: &str) -> Option<Vec<u64>> {
    let inner = s.trim().strip_prefix('[')?.strip_suffix(']')?.trim();
    if inner.is_empty() {
        return Some(vec![]);
    }
    inner.split(", ").map(|x| x.parse().ok()).collect()
}
pub fn parse_transfer(s: &str) -> Option<Transfer> {
    let (from, rest) = s.trim().split_once("->")?;
    let (to, amount) = rest.split_once(':')?;
    Some((from.parse().ok()?, to.parse().ok()?, amount.parse().ok()?))
}
pub fn parse_batch(s: &str) -> Option<Vec<Transfer>> {
    let inner = s.trim().strip_prefix('[')?.strip_suffix(']')?.trim();
    if inner.is_empty() {
        return Some(vec![]);
    }
    inner.split(", ").map(parse_transfer).collect()
}
pub fn parse_opt(s: &str) -> Option<Option<u64>> {
    match s {
        "none" => Some(None),
        _ => Some(Some(s.strip_prefix("some ")?.parse().ok()?)),
    }
}

/// Evaluate the predicate of glossary entry `id` on plain-text arguments, given in the
/// order of the entry's `args` in glossary.yaml. `None`: unknown id or unparsable argument.
pub fn eval(id: &str, a: &[&str]) -> Option<bool> {
    let u = |i: usize| a.get(i)?.parse::<u64>().ok();
    let o = |i: usize| Outcome::parse(a.get(i)?);
    let l = |i: usize| a.get(i)?.split(',').map(|x| x.parse::<u64>().ok()).collect::<Option<Vec<u64>>>();
    let n = |i: usize| a.get(i)?.parse::<usize>().ok();
    let bs = |i: usize| parse_balances(a.get(i)?);
    let t = |i: usize| parse_transfer(a.get(i)?);
    let b = |i: usize| parse_batch(a.get(i)?);
    let opt = |i: usize| parse_opt(a.get(i)?);
    let flag = |i: usize| a.get(i)?.parse::<bool>().ok();
    Some(match id {
        "LG-holds" => l_holds(&bs(0)?, &bs(1)?),
        "LG-sums-to" => l_sums_to(&bs(0)?, u(1)?),
        "LG-sum-too-big" => l_sum_too_big(&bs(0)?),
        "LG-account" => l_is_account(&bs(0)?, n(1)?),
        "LG-no-account" => l_not_account(&bs(0)?, n(1)?),
        "LG-valid" => l_valid_on(&bs(0)?, t(1)?),
        "LG-invalid" => l_invalid_on(&bs(0)?, t(1)?),
        "LG-first-invalid" => l_first_invalid(&bs(0)?, &b(1)?),
        "LG-all-valid" => l_all_valid(&bs(0)?, &b(1)?),
        "LT-total-same" => l_total_unchanged(&bs(0)?, &bs(1)?),
        "LT-same" => l_unchanged(&bs(0)?, &bs(1)?),
        "LT-now-holds" => l_now_holds(&bs(0)?, &bs(1)?),
        "LT-at-most" => l_applied_at_most(n(0)?, &b(1)?),
        "LT-none-applied" => l_applied_none(n(0)?),
        "LT-all-applied" => l_applied_all(n(0)?, &b(1)?),
        "LT-exactly" => l_applied_exactly(n(0)?, n(1)?),
        "LT-result" => l_result_is(opt(0)?, u(1)?),
        "LT-no-result" => l_no_result(opt(0)?),
        "LT-some-result" => l_some_result(opt(0)?),
        "LT-balance" => l_result_is_balance(opt(0)?, &bs(1)?, n(2)?),
        "LT-stops-at-invalid" => l_stops_at_invalid(n(0)?, &b(1)?, &bs(2)?),
        "LT-same-if-rejected" => l_unchanged_if_rejected(flag(0)?, &bs(1)?, &bs(2)?),
        "LT-accepted" => l_accepted(flag(0)?),
        "LT-rejected" => l_rejected(flag(0)?),
        "LT-moved" => l_moved(&bs(0)?, &bs(1)?, t(2)?),
        "G-balance" => has_balance(u(0)?, u(1)?),
        "G-covers" => covers(u(0)?, u(1)?),
        "G-exceeds" => exceeds(u(0)?, u(1)?),
        "G-room" => room_for(u(0)?, u(1)?),
        "G-noroom" => no_room_for(u(0)?, u(1)?),
        "T-ok" => succeeds(o(0)?),
        "T-err" => rejected_with(o(0)?, o(1)?),
        "T-dec" => decreased_by(u(0)?, u(1)?, u(2)?),
        "T-inc" => increased_by(u(0)?, u(1)?, u(2)?),
        "T-same" => unchanged(u(0)?, u(1)?),
        "T-total" => total_unchanged(&l(0)?, &l(1)?),
        _ => return None,
    })
}
