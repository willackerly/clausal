//! The Rust-side reading of each Given/Then glossary phrase, as pure predicates.
//!
//! This is the SECOND hand-written reading of each phrase; the first is the Lean
//! definition in lean/Vocab/Inventory.lean. The cucumber steps (tests/bdd.rs) assert
//! these predicates, and tests/readings.rs evaluates them on a grid of arguments so
//! the report can compare them, point by point, with the Lean definitions.
//! A warehouse is its list of bins (product, units), bin 0 first; an order is (product, units).
//! Sums are taken in u128 so they cannot wrap.

use std::collections::BTreeSet;

pub type Bins = Vec<(u32, u64)>;
pub type Orders = Vec<(u32, u64)>;

/// Units of product `p`, summed over all bins.
pub fn stock(w: &[(u32, u64)], p: u32) -> u128 {
    w.iter().filter(|b| b.0 == p).map(|b| b.1 as u128).sum()
}
/// How many bins hold product `p`.
pub fn bins_of(w: &[(u32, u64)], p: u32) -> usize {
    w.iter().filter(|b| b.0 == p).count()
}
fn holds_at_least(b: (u32, u64), p: u32, n: u64) -> bool {
    b.0 == p && b.1 >= n
}
fn in_more_than_half(w: &[(u32, u64)], p: u32) -> bool {
    2 * bins_of(w, p) > w.len()
}
/// Second reading of the reference `takeFrom`: take `need` units of `p`, earliest bins first.
pub fn take_from(w: &[(u32, u64)], p: u32, need: u128) -> Bins {
    let mut need = need;
    let mut out = Vec::new();
    for &(q, u) in w {
        if q == p {
            let t = need.min(u as u128);
            out.push((q, (u as u128 - t) as u64));
            need -= t;
        } else {
            out.push((q, u));
        }
    }
    out
}
/// Second reading of the reference `fillFrom`: (orders filled, bins afterwards).
pub fn fill_from(w: &[(u32, u64)], os: &[(u32, u64)]) -> (usize, Bins) {
    let mut bins = w.to_vec();
    let mut filled = 0;
    for &(p, u) in os {
        if u as u128 <= stock(&bins, p) {
            bins = take_from(&bins, p, u as u128);
            filled += 1;
        }
    }
    (filled, bins)
}

// glossary: G-holds          "warehouse {w} holds the bins {bs}"
pub fn holds(pre: &[(u32, u64)], bs: &[(u32, u64)]) -> bool {
    pre == bs
}
// glossary: G-stock-fits     "the units of product {p} in warehouse {w} add up to at most the maximum"
pub fn stock_fits(pre: &[(u32, u64)], p: u32) -> bool {
    stock(pre, p) <= u64::MAX as u128
}
// glossary: G-stock-too-big  "the units of product {p} in warehouse {w} add up to more than the maximum"
pub fn stock_too_big(pre: &[(u32, u64)], p: u32) -> bool {
    stock(pre, p) > u64::MAX as u128
}
// glossary: G-some-bin       "some bin of warehouse {w} holds at least {n} units of product {p}"
pub fn some_bin_holds(pre: &[(u32, u64)], p: u32, n: u64) -> bool {
    pre.iter().any(|&b| holds_at_least(b, p, n))
}
// glossary: G-no-bin         "no bin of warehouse {w} holds at least {n} units of product {p}"
pub fn no_bin_holds(pre: &[(u32, u64)], p: u32, n: u64) -> bool {
    !pre.iter().any(|&b| holds_at_least(b, p, n))
}
// glossary: G-more-than-half "product {p} is in more than half of the bins of warehouse {w}"
pub fn more_than_half(pre: &[(u32, u64)], p: u32) -> bool {
    in_more_than_half(pre, p)
}
// glossary: G-none-more-than-half "no product is in more than half of the bins of warehouse {w}"
pub fn none_more_than_half(pre: &[(u32, u64)]) -> bool {
    !pre.iter().any(|b| in_more_than_half(pre, b.0))
}
// glossary: T-stock          "the result is the number of units of product {p} in warehouse {w}"
pub fn result_is_stock(o: Option<u64>, pre: &[(u32, u64)], p: u32) -> bool {
    o.map(|s| s as u128) == Some(stock(pre, p))
}
// glossary: T-no-count       "no count is given"
pub fn no_count(o: Option<u64>) -> bool {
    o.is_none()
}
// glossary: T-first-bin      "the result is the first bin of warehouse {w} that holds at least {n} units of product {p}"
pub fn first_bin_is(o: Option<usize>, pre: &[(u32, u64)], p: u32, n: u64) -> bool {
    match o {
        Some(i) => i < pre.len() && holds_at_least(pre[i], p, n) && pre[..i].iter().all(|&b| !holds_at_least(b, p, n)),
        None => false,
    }
}
// glossary: T-no-bin         "no bin is found"
pub fn no_bin_found(o: Option<usize>) -> bool {
    o.is_none()
}
// glossary: T-restocked      "every bin of product {p} in warehouse {w} has gained {a} units, up to the maximum, and no other bin has changed"
pub fn restocked(pre: &[(u32, u64)], post: &[(u32, u64)], p: u32, a: u64) -> bool {
    post.len() == pre.len()
        && pre.iter().zip(post).all(|(&(q, u), &(q2, u2))| {
            let want = if q == p { (u as u128 + a as u128).min(u64::MAX as u128) } else { u as u128 };
            q2 == q && u2 as u128 == want
        })
}
// glossary: T-restock-count  "the number of bins restocked is the number of bins of product {p} in warehouse {w}"
pub fn count_is_bins_of(n: usize, pre: &[(u32, u64)], p: u32) -> bool {
    n == bins_of(pre, p)
}
// glossary: T-taken-min      "the amount taken is the smaller of {n} and the units of product {p} that warehouse {w} held"
pub fn taken_is_min(t: u64, pre: &[(u32, u64)], p: u32, want: u64) -> bool {
    t as u128 == (want as u128).min(stock(pre, p))
}
// glossary: T-stock-down     "the units of product {p} in warehouse {w} have gone down by exactly the amount taken"
pub fn stock_down_by(t: u64, pre: &[(u32, u64)], post: &[(u32, u64)], p: u32) -> bool {
    stock(post, p) + t as u128 == stock(pre, p)
}
// glossary: T-taken-earliest "warehouse {w} now holds what is left after taking {n} units of product {p} from its earliest bins first"
pub fn taken_earliest_first(pre: &[(u32, u64)], post: &[(u32, u64)], p: u32, want: u64) -> bool {
    post == take_from(pre, p, want as u128).as_slice()
}
// glossary: T-filled-count   "the number of orders filled is the number of orders of {os} that can be filled in full, in turn, from warehouse {w}"
pub fn filled_count(n: usize, pre: &[(u32, u64)], os: &[(u32, u64)]) -> bool {
    n == fill_from(pre, os).0
}
// glossary: T-filled-state   "warehouse {w} now holds what is left after filling, in turn, each order of {os} that can be filled in full"
pub fn filled_state(pre: &[(u32, u64)], post: &[(u32, u64)], os: &[(u32, u64)]) -> bool {
    post == fill_from(pre, os).1.as_slice()
}
// glossary: T-filled-at-most "the number of orders filled is at most the number of orders in {os}"
pub fn filled_at_most(n: usize, os: &[(u32, u64)]) -> bool {
    n <= os.len()
}
// glossary: T-different-products "the result is the number of different products in warehouse {w}"
pub fn different_products(n: usize, pre: &[(u32, u64)]) -> bool {
    n == pre.iter().map(|b| b.0).collect::<BTreeSet<u32>>().len()
}
// glossary: T-at-most-bins   "the result is at most the number of bins of warehouse {w}"
pub fn at_most_bins(n: usize, pre: &[(u32, u64)]) -> bool {
    n <= pre.len()
}
// glossary: T-product        "the result is product {p}"
pub fn result_is_product(o: Option<u32>, p: u32) -> bool {
    o == Some(p)
}
// glossary: T-no-dominant    "there is no dominant product"
pub fn no_dominant(o: Option<u32>) -> bool {
    o.is_none()
}

/// Parsers for the literals of glossary.yaml: `[7:10, 3:5]` (bins or orders), `some 3` / `none`.
pub fn parse_pairs(s: &str) -> Option<Vec<(u32, u64)>> {
    let inner = s.trim().strip_prefix('[')?.strip_suffix(']')?.trim();
    if inner.is_empty() {
        return Some(vec![]);
    }
    inner
        .split(", ")
        .map(|x| {
            let (p, u) = x.split_once(':')?;
            Some((p.parse().ok()?, u.parse().ok()?))
        })
        .collect()
}
pub fn parse_opt<T: std::str::FromStr>(s: &str) -> Option<Option<T>> {
    match s {
        "none" => Some(None),
        _ => Some(Some(s.strip_prefix("some ")?.parse().ok()?)),
    }
}

/// Evaluate the predicate of glossary entry `id` on plain-text arguments, given in the
/// order of the entry's `args` in glossary.yaml. `None`: unknown id or unparsable argument.
pub fn eval(id: &str, a: &[&str]) -> Option<bool> {
    let w = |i: usize| parse_pairs(a.get(i)?);
    let p = |i: usize| a.get(i)?.parse::<u32>().ok();
    let u = |i: usize| a.get(i)?.parse::<u64>().ok();
    let n = |i: usize| a.get(i)?.parse::<usize>().ok();
    let o64 = |i: usize| parse_opt::<u64>(a.get(i)?);
    let osz = |i: usize| parse_opt::<usize>(a.get(i)?);
    let o32 = |i: usize| parse_opt::<u32>(a.get(i)?);
    Some(match id {
        "G-holds" => holds(&w(0)?, &w(1)?),
        "G-stock-fits" => stock_fits(&w(0)?, p(1)?),
        "G-stock-too-big" => stock_too_big(&w(0)?, p(1)?),
        "G-some-bin" => some_bin_holds(&w(0)?, p(1)?, u(2)?),
        "G-no-bin" => no_bin_holds(&w(0)?, p(1)?, u(2)?),
        "G-more-than-half" => more_than_half(&w(0)?, p(1)?),
        "G-none-more-than-half" => none_more_than_half(&w(0)?),
        "T-stock" => result_is_stock(o64(0)?, &w(1)?, p(2)?),
        "T-no-count" => no_count(o64(0)?),
        "T-first-bin" => first_bin_is(osz(0)?, &w(1)?, p(2)?, u(3)?),
        "T-no-bin" => no_bin_found(osz(0)?),
        "T-restocked" => restocked(&w(0)?, &w(1)?, p(2)?, u(3)?),
        "T-restock-count" => count_is_bins_of(n(0)?, &w(1)?, p(2)?),
        "T-taken-min" => taken_is_min(u(0)?, &w(1)?, p(2)?, u(3)?),
        "T-stock-down" => stock_down_by(u(0)?, &w(1)?, &w(2)?, p(3)?),
        "T-taken-earliest" => taken_earliest_first(&w(0)?, &w(1)?, p(2)?, u(3)?),
        "T-filled-count" => filled_count(n(0)?, &w(1)?, &w(2)?),
        "T-filled-state" => filled_state(&w(0)?, &w(1)?, &w(2)?),
        "T-filled-at-most" => filled_at_most(n(0)?, &w(1)?),
        "T-different-products" => different_products(n(0)?, &w(1)?),
        "T-at-most-bins" => at_most_bins(n(0)?, &w(1)?),
        "T-product" => result_is_product(o32(0)?, p(1)?),
        "T-no-dominant" => no_dominant(o32(0)?),
        _ => return None,
    })
}
