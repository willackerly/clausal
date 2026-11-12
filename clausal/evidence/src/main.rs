//! THE GENERIC PROPERTY-TEST RUNNER (plan node E1). Hand-written once; nothing here is about one rule.
//!
//!   cargo run --quiet -- [--trees ../build/trees.json] [--cases 10000] [--seed 20261111] [--only id,id]
//!                        [--prefix Spec.ledger.] [--timeout-secs 60] [--size 6]
//!   cargo run --quiet -- --replay inputs.jsonl      evaluate readings at given inputs instead ({"rule": id, "values": {var: literal}})
//!
//! For every compiled reading (table.rs, GENERATED from build/trees.json) it runs proptest with shrinking on the
//! generated predicate `check_<n>` (checks.rs, GENERATED), against the COMPILED crates. One JSON object per rule:
//!   {"rule", "status": "pass" | "fail" | "hang" | "abort" | "mismatch", "cases" (in scope and passed), "calls", "rejected",
//!    "calls_to_first_failure", "seed", "witness": {variable: literal} | null, "bits", "message", "elapsed_ms"}
//!
//! GENERATORS are derived from the types of the reading's variables and from its Givens, not written per rule:
//!   * a variable that a Given fixes (`ledger Main holds the balances <balances>`) is not generated: it IS that value;
//!   * every other Given is kept by rejection, so only inputs in the rule's scope count as cases;
//!   * values are EDGE-WEIGHTED: the ends of the u64 range, small numbers, the numbers written in the sentence, and values
//!     at or next to a number already generated for the same case (a balance, a length, the room left below the maximum),
//!     so that "equal to", "one more than" and "just fits" are hit; a list of balances is sometimes completed so that its
//!     sum is the maximum, give or take one;
//!   * the second call of a two-run rule is the first call again, or a small change of it, or independent.
//!
//! At every case the generated predicate is ALSO compared with the tree evaluator of wallet-bdd/src/pieces.rs on the
//! same tree; a difference is reported as "mismatch" (a fault of the generator or of a typed reading, never a verdict).
//! A panic of the code under test is "no answer", as in the reading. A rule that does not finish is "hang", with the
//! input it was evaluating; the process then stops, and the caller starts the remaining rules in a fresh one.
mod checks;
mod table;
mod typed;

use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::time::{Duration, Instant};

use proptest::collection::vec;
use proptest::prelude::*;
use proptest::test_runner::{Config, RngAlgorithm, TestCaseError, TestError, TestRng, TestRunner};
use serde_json::{json, Value as J};
use typed::T;
use wallet_bdd::pieces as pc;

const MAX: u64 = u64::MAX;

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Ty {
    Amount,
    Index,
    Balances,
    Transfer,
    Batch,
}

#[derive(Clone, Copy, Debug)]
pub enum Src {
    Free,
    /// a Given fixes this variable to be another variable's value
    SameAs(usize),
    /// a Given fixes this variable to a literal
    Lit(&'static str),
    /// this variable belongs to the second call of a two-run rule; its counterpart in the first call
    Twin(usize),
}

pub struct Var {
    pub name: &'static str,
    pub ty: Ty,
    pub src: Src,
}

pub struct Rule {
    pub id: &'static str,
    pub vars: &'static [Var],
    /// the numbers written in the sentence
    pub pool: &'static [u64],
    pub call: fn(&[GV]) -> (Vec<bool>, bool, bool),
}

/// A generated value of one of the vocabulary's literal types.
#[derive(Clone, Debug, PartialEq)]
pub enum GV {
    Num(u64),
    Bal(Vec<u64>),
    Tr(T),
    Batch(Vec<T>),
}

impl GV {
    pub fn num(&self) -> u64 {
        match self {
            GV::Num(n) => *n,
            v => panic!("a number is needed, got {v:?}"),
        }
    }
    pub fn bal(&self) -> &[u64] {
        match self {
            GV::Bal(b) => b,
            v => panic!("balances are needed, got {v:?}"),
        }
    }
    pub fn tr(&self) -> T {
        match self {
            GV::Tr(t) => *t,
            v => panic!("a transfer is needed, got {v:?}"),
        }
    }
    pub fn batch(&self) -> &[T] {
        match self {
            GV::Batch(b) => b,
            v => panic!("a batch is needed, got {v:?}"),
        }
    }
    fn text(&self) -> String {
        let tr = |t: &T| format!("{}->{}:{}", t.0, t.1, t.2);
        match self {
            GV::Num(n) => n.to_string(),
            GV::Bal(b) => format!("[{}]", b.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", ")),
            GV::Tr(t) => tr(t),
            GV::Batch(b) => format!("[{}]", b.iter().map(tr).collect::<Vec<_>>().join(", ")),
        }
    }
    fn parse(ty: Ty, s: &str) -> GV {
        let v = pc::parse_lit(ty_name(ty), s);
        let tr = |v: &pc::Val| v.transfer();
        match ty {
            Ty::Amount | Ty::Index => GV::Num(u64::try_from(v.num()).expect("a u64")),
            Ty::Balances => GV::Bal(v.list().iter().map(|x| u64::try_from(x.num()).expect("a u64")).collect()),
            Ty::Transfer => GV::Tr(tr(&v)),
            Ty::Batch => GV::Batch(v.list().iter().map(tr).collect()),
        }
    }
}

fn ty_name(ty: Ty) -> &'static str {
    match ty {
        Ty::Amount => "amount",
        Ty::Index => "index",
        Ty::Balances => "balances",
        Ty::Transfer => "transfer",
        Ty::Batch => "batch",
    }
}

// ---------------------------------------------------------------------------------------------- generators

/// How one number is chosen. What proptest generates and shrinks is the CHOICE; the number is worked out from the
/// values already generated for the same case (`Pools`). Simplest first: proptest shrinks towards the first variant.
#[derive(Clone, Debug)]
enum NumPick {
    Small(u64),
    Abs(u64),
    High(u64),
    /// a number already in the case (or written in the sentence), plus -1, 0 or 1
    Near(usize, i8),
    /// what is left below the maximum after such a number, plus -1, 0 or 1
    Room(usize, i8),
}

#[derive(Clone, Debug)]
enum IdxPick {
    /// an existing position of a collection of the case
    In(usize, usize),
    Small(u64),
    /// the length of a collection of the case, plus -1, 0 or 1
    Len(usize, i8),
    Abs(u64),
}

type TrPick = (IdxPick, IdxPick, NumPick);

#[derive(Clone, Debug)]
enum Pick {
    Amount(NumPick),
    Index(IdxPick),
    /// the items, and whether the last one is replaced so that the sum is the maximum plus -1, 0 or 1
    Balances(Vec<NumPick>, Option<i8>),
    Transfer(TrPick),
    Batch(Vec<TrPick>),
    /// the second call: the first call's value again
    Same,
    /// the second call: a small change of the first call's value (same route with another amount; the same ledger
    /// with accounts added or one balance changed; a neighbouring number)
    Tweak(Box<Pick>, usize),
}

fn delta() -> impl Strategy<Value = i8> {
    prop_oneof![Just(0i8), Just(1i8), Just(-1i8)]
}

fn num_pick() -> BoxedStrategy<NumPick> {
    prop_oneof![
        2 => (0u64..=3).prop_map(NumPick::Small),
        3 => any::<u64>().prop_map(NumPick::Abs),
        2 => (0u64..=3).prop_map(NumPick::High),
        3 => (any::<usize>(), delta()).prop_map(|(i, d)| NumPick::Near(i, d)),
        2 => (any::<usize>(), delta()).prop_map(|(i, d)| NumPick::Room(i, d)),
    ]
    .boxed()
}

fn idx_pick() -> BoxedStrategy<IdxPick> {
    prop_oneof![
        6 => (0usize..8, any::<usize>()).prop_map(|(k, i)| IdxPick::In(k, i)),
        2 => (0u64..=7).prop_map(IdxPick::Small),
        2 => (any::<usize>(), delta()).prop_map(|(i, d)| IdxPick::Len(i, d)),
        1 => any::<u64>().prop_map(IdxPick::Abs),
    ]
    .boxed()
}

fn tr_pick() -> BoxedStrategy<TrPick> {
    (idx_pick(), idx_pick(), num_pick()).boxed()
}

fn free_pick(ty: Ty, size: usize) -> BoxedStrategy<Pick> {
    match ty {
        Ty::Amount => num_pick().prop_map(Pick::Amount).boxed(),
        Ty::Index => idx_pick().prop_map(Pick::Index).boxed(),
        Ty::Balances => (vec(num_pick(), 0..=size), prop_oneof![3 => Just(None), 1 => delta().prop_map(Some)]).prop_map(|(v, f)| Pick::Balances(v, f)).boxed(),
        Ty::Transfer => tr_pick().prop_map(Pick::Transfer).boxed(),
        Ty::Batch => vec(tr_pick(), 0..=size).prop_map(Pick::Batch).boxed(),
    }
}

fn pick_for(v: &Var, size: usize) -> BoxedStrategy<Pick> {
    match v.src {
        Src::Free => free_pick(v.ty, size),
        Src::SameAs(_) | Src::Lit(_) => Just(Pick::Same).boxed(),
        Src::Twin(_) => prop_oneof![
            3 => Just(Pick::Same),
            3 => (free_pick(v.ty, size), any::<usize>()).prop_map(|(p, k)| Pick::Tweak(Box::new(p), k)),
            2 => free_pick(v.ty, size),
        ]
        .boxed(),
    }
}

/// The numbers and lengths already in the case.
struct Pools {
    nums: Vec<u64>,
    lens: Vec<u64>,
}

impl Pools {
    fn num(&self, p: &NumPick) -> u64 {
        let near = |i: usize, d: i8, room: bool| -> u64 {
            if self.nums.is_empty() {
                return 0;
            }
            let base = self.nums[i % self.nums.len()];
            let base = if room { MAX - base } else { base };
            if d < 0 { base.saturating_sub(1) } else { base.saturating_add(d as u64) }
        };
        match *p {
            NumPick::Small(n) | NumPick::Abs(n) => n,
            NumPick::High(n) => MAX - n,
            NumPick::Near(i, d) => near(i, d, false),
            NumPick::Room(i, d) => near(i, d, true),
        }
    }
    fn idx(&self, p: &IdxPick) -> u64 {
        match *p {
            IdxPick::Small(n) | IdxPick::Abs(n) => n,
            IdxPick::In(k, i) => {
                let len = if self.lens.is_empty() { 0 } else { self.lens[i % self.lens.len()] };
                if len == 0 { k as u64 } else { k as u64 % len }
            }
            IdxPick::Len(i, d) => {
                if self.lens.is_empty() {
                    return 0;
                }
                let base = self.lens[i % self.lens.len()];
                if d < 0 { base.saturating_sub(1) } else { base.saturating_add(d as u64) }
            }
        }
    }
    fn tr(&self, p: &TrPick) -> T {
        (self.idx(&p.0) as usize, self.idx(&p.1) as usize, self.num(&p.2))
    }
    fn free(&self, p: &Pick) -> GV {
        match p {
            Pick::Amount(n) => GV::Num(self.num(n)),
            Pick::Index(i) => GV::Num(self.idx(i)),
            Pick::Balances(items, fix) => {
                let mut b: Vec<u64> = items.iter().map(|n| self.num(n)).collect();
                if let (Some(d), Some(last)) = (fix, b.len().checked_sub(1)) {
                    let rest: u128 = b[..last].iter().map(|&x| x as u128).sum();
                    let want = MAX as i128 + *d as i128 - rest as i128;
                    if (0..=MAX as i128).contains(&want) {
                        b[last] = want as u64;
                    }
                }
                GV::Bal(b)
            }
            Pick::Transfer(t) => GV::Tr(self.tr(t)),
            Pick::Batch(ts) => GV::Batch(ts.iter().map(|t| self.tr(t)).collect()),
            Pick::Same | Pick::Tweak(..) => unreachable!("not a free choice"),
        }
    }
    fn add(&mut self, v: &GV) {
        match v {
            GV::Num(n) => self.nums.push(*n),
            GV::Bal(b) => {
                self.nums.extend(b);
                self.lens.push(b.len() as u64);
                let s: u128 = b.iter().map(|&x| x as u128).sum();
                if s <= MAX as u128 {
                    self.nums.push(s as u64);
                }
            }
            GV::Tr(t) => self.nums.push(t.2),
            GV::Batch(b) => {
                self.nums.extend(b.iter().map(|t| t.2));
                self.lens.push(b.len() as u64);
            }
        }
    }
}

/// A small change of the first call's value.
fn tweak(of: &GV, fresh: GV, k: usize) -> GV {
    match (of, fresh) {
        (GV::Num(n), GV::Num(f)) => GV::Num(match k % 3 {
            0 => n.saturating_add(1),
            1 => n.saturating_sub(1),
            _ => f,
        }),
        (GV::Tr(t), GV::Tr(f)) => GV::Tr((t.0, t.1, f.2)),
        (GV::Bal(b), GV::Bal(f)) => {
            let mut out = b.clone();
            if k % 2 == 0 || b.is_empty() {
                out.extend(f.iter().take(2));
            } else {
                let at = k % b.len();
                out[at] = f.first().copied().unwrap_or(0);
            }
            GV::Bal(out)
        }
        (GV::Batch(b), GV::Batch(f)) => {
            let mut out = b.clone();
            out.extend(f.iter().take(1));
            GV::Batch(out)
        }
        (_, f) => f,
    }
}

/// The values of every variable of a rule, from the choices proptest made.
fn materialise(rule: &Rule, picks: &[Pick]) -> Vec<GV> {
    let mut pools = Pools { nums: rule.pool.to_vec(), lens: vec![] };
    let mut out: Vec<Option<GV>> = vec![None; rule.vars.len()];
    // free lists of balances first: account numbers and amounts are chosen next to their lengths and items
    let order: Vec<usize> = (0..rule.vars.len()).filter(|&k| rule.vars[k].ty == Ty::Balances).chain((0..rule.vars.len()).filter(|&k| rule.vars[k].ty != Ty::Balances)).collect();
    for &k in &order {
        if let Src::Free = rule.vars[k].src {
            let v = pools.free(&picks[k]);
            pools.add(&v);
            out[k] = Some(v);
        }
    }
    for &k in &order {
        if let Src::Twin(of) = rule.vars[k].src {
            let first = out[of].clone().expect("the first call's value is generated before the second's");
            let v = match &picks[k] {
                Pick::Same => first,
                Pick::Tweak(p, n) => tweak(&first, pools.free(p), *n),
                p => pools.free(p),
            };
            pools.add(&v);
            out[k] = Some(v);
        }
    }
    for k in 0..rule.vars.len() {
        match rule.vars[k].src {
            Src::Lit(s) => out[k] = Some(GV::parse(rule.vars[k].ty, s)),
            Src::SameAs(of) => out[k] = out[of].clone(),
            _ => {}
        }
    }
    // a variable fixed to one that is itself fixed to a literal
    for k in 0..rule.vars.len() {
        if let (None, Src::SameAs(of)) = (&out[k], rule.vars[k].src) {
            out[k] = out[of].clone();
        }
    }
    out.into_iter().map(|v| v.expect("every variable has a value")).collect()
}

// ---------------------------------------------------------------------------------------------- one case

struct Point {
    bits: String,
    scoped: bool,
    holds: bool,
    tree_bits: Option<String>,
}

fn bits_text(bits: &[bool]) -> String {
    bits.iter().map(|&b| if b { '1' } else { '0' }).collect()
}

fn panic_text(e: Box<dyn std::any::Any + Send>) -> String {
    e.downcast_ref::<String>().cloned().or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string())).unwrap_or_default()
}

/// The generated predicate at one input, and the tree evaluator of pieces.rs at the same input.
fn evaluate(rule: &Rule, rd: Option<&J>, g: &[GV]) -> Result<Point, String> {
    let (bits, scoped, holds) = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| (rule.call)(g)))
        .map_err(|e| format!("the generated predicate panicked: {}", panic_text(e)))?;
    let tree_bits = match rd {
        None => None,
        Some(rd) => {
            let vals: Vec<(String, pc::Val)> = rule.vars.iter().zip(g).map(|(v, x)| (v.name.to_string(), pc::parse_lit(ty_name(v.ty), &x.text()))).collect();
            Some(std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| pc::eval_point(rd, &vals)))
                .map_err(|e| format!("the tree evaluator panicked: {}", panic_text(e)))?)
        }
    };
    Ok(Point { bits: bits_text(&bits), scoped, holds, tree_bits })
}

fn witness(rule: &Rule, g: &[GV]) -> J {
    J::Object(rule.vars.iter().zip(g).map(|(v, x)| (v.name.to_string(), J::String(x.text()))).collect())
}

fn seed_for(seed: u64, rule: &str) -> [u8; 32] {
    // FNV-1a of the rule id, mixed with the run seed: every rule gets its own stream.
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

fn run_rule(rule: &'static Rule, rd: Option<J>, cases: u32, seed: u64, size: usize, current: Arc<Mutex<Option<J>>>) -> J {
    let config = Config {
        cases,
        failure_persistence: None,
        max_global_rejects: cases.saturating_mul(100),
        max_local_rejects: cases.saturating_mul(100),
        max_shrink_iters: 20_000,
        verbose: 0,
        ..Config::default()
    };
    let mut runner = TestRunner::new_with_rng(config, TestRng::from_seed(RngAlgorithm::ChaCha, &seed_for(seed, rule.id)));
    let strategy: Vec<BoxedStrategy<Pick>> = rule.vars.iter().map(|v| pick_for(v, size)).collect();
    let (calls, passed, rejected, first_failure) = (AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0), AtomicU64::new(0));
    let mismatch = Mutex::new(None::<String>);
    let t0 = Instant::now();
    let result = runner.run(&strategy, |picks| {
        let g = materialise(rule, &picks);
        *current.lock().unwrap() = Some(witness(rule, &g));
        let n = calls.fetch_add(1, Ordering::SeqCst) + 1;
        let fail = |m: String| {
            let _ = first_failure.compare_exchange(0, n, Ordering::SeqCst, Ordering::SeqCst);
            Err(TestCaseError::fail(m))
        };
        let p = match evaluate(rule, rd.as_ref(), &g) {
            Ok(p) => p,
            Err(m) => {
                *mismatch.lock().unwrap() = Some(m.clone());
                return fail(m);
            }
        };
        if let Some(tb) = &p.tree_bits {
            if *tb != p.bits {
                let m = format!("READING MISMATCH: the generated predicate gives {} and the tree evaluator gives {}", p.bits, tb);
                *mismatch.lock().unwrap() = Some(m.clone());
                return fail(m);
            }
        }
        if !p.scoped {
            rejected.fetch_add(1, Ordering::SeqCst);
            return Err(TestCaseError::reject("outside the rule's scope"));
        }
        if !p.holds {
            return fail(format!("the rule is false here (bits {})", p.bits));
        }
        passed.fetch_add(1, Ordering::SeqCst);
        Ok(())
    });
    let (status, wit, bits, message) = match result {
        Ok(()) => ("pass", J::Null, J::Null, String::new()),
        Err(TestError::Fail(reason, picks)) => {
            let g = materialise(rule, &picks);
            let bits = evaluate(rule, rd.as_ref(), &g).map(|p| p.bits).unwrap_or_default();
            // a mismatch seen at the shrunk input, or only on the way there
            let is_mismatch = !reason.message().starts_with("the rule is false");
            (if is_mismatch { "mismatch" } else { "fail" }, witness(rule, &g), J::String(bits), reason.message().to_string())
        }
        Err(TestError::Abort(reason)) => ("abort", J::Null, J::Null, format!("too few inputs in the rule's scope: {}", reason.message())),
    };
    json!({"rule": rule.id, "status": status, "cases": passed.load(Ordering::SeqCst), "calls": calls.load(Ordering::SeqCst),
           "rejected": rejected.load(Ordering::SeqCst), "calls_to_first_failure": first_failure.load(Ordering::SeqCst), "seed": seed,
           "witness": wit, "bits": bits, "message": message, "elapsed_ms": t0.elapsed().as_millis() as u64,
           "compared_with_tree": rd.is_some()})
}

/// Run `f` on its own thread; `None` if it does not finish in time (the thread is left behind).
fn with_timeout<R: Send + 'static>(secs: u64, f: impl FnOnce() -> R + Send + 'static) -> Option<R> {
    let (tx, rx) = mpsc::channel();
    std::thread::Builder::new().stack_size(64 << 20).spawn(move || {
        let _ = tx.send(f());
    }).expect("a thread");
    rx.recv_timeout(Duration::from_secs(secs)).ok()
}

fn replay(rules: &'static [Rule], trees: &Option<J>, path: &str, timeout: u64) {
    let text = std::fs::read_to_string(path).expect("the replay file");
    for line in text.lines().filter(|l| l.trim_start().starts_with('{')) {
        let req: J = serde_json::from_str(line).expect("a JSON object per line");
        let id = req["rule"].as_str().expect("rule").to_string();
        let Some(rule) = rules.iter().find(|r| r.id == id) else {
            println!("{}", json!({"rule": id, "status": "unknown rule"}));
            continue;
        };
        let mut g: Vec<Option<GV>> = rule.vars.iter().map(|v| req["values"].get(v.name).and_then(J::as_str).map(|s| GV::parse(v.ty, s))).collect();
        for _ in 0..2 {
            for k in 0..rule.vars.len() {
                if g[k].is_none() {
                    g[k] = match rule.vars[k].src {
                        Src::Lit(s) => Some(GV::parse(rule.vars[k].ty, s)),
                        Src::SameAs(of) => g[of].clone(),
                        _ => None,
                    };
                }
            }
        }
        if g.iter().any(Option::is_none) {
            println!("{}", json!({"rule": id, "status": "missing values", "tag": req["tag"]}));
            continue;
        }
        let g: Vec<GV> = g.into_iter().map(Option::unwrap).collect();
        let rd = reading(trees, &id);
        let w = witness(rule, &g);
        let out = match with_timeout(timeout, move || evaluate(rule, rd.as_ref(), &g)) {
            None => json!({"rule": id, "status": "hang", "values": w, "tag": req["tag"]}),
            Some(Err(m)) => json!({"rule": id, "status": "error", "message": m, "values": w, "tag": req["tag"]}),
            Some(Ok(p)) => {
                let status = if p.tree_bits.as_ref().is_some_and(|t| *t != p.bits) { "mismatch" } else if !p.scoped { "out-of-scope" } else if p.holds { "holds" } else { "fails" };
                json!({"rule": id, "status": status, "bits": p.bits, "tree_bits": p.tree_bits, "values": w, "tag": req["tag"]})
            }
        };
        println!("{out}");
    }
}

fn reading(trees: &Option<J>, id: &str) -> Option<J> {
    trees.as_ref().and_then(|t| t["readings"].as_array().and_then(|a| a.iter().find(|r| r["id"] == id).cloned()))
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let opt = |name: &str| args.iter().position(|a| a == name).and_then(|i| args.get(i + 1)).cloned();
    let cases: u32 = opt("--cases").map(|s| s.parse().expect("--cases")).unwrap_or(10_000);
    let seed: u64 = opt("--seed").map(|s| s.parse().expect("--seed")).unwrap_or(20261111);
    let size: usize = opt("--size").map(|s| s.parse().expect("--size")).unwrap_or(6);
    let timeout: u64 = opt("--timeout-secs").map(|s| s.parse().expect("--timeout-secs")).unwrap_or(60);
    let only: Option<Vec<String>> = opt("--only").map(|s| s.split(',').map(str::to_string).collect());
    let prefix = opt("--prefix");
    let trees_path = opt("--trees").unwrap_or_else(|| format!("{}/../build/trees.json", env!("CARGO_MANIFEST_DIR")));
    let trees: Option<J> = if args.iter().any(|a| a == "--no-tree") { None } else { std::fs::read_to_string(&trees_path).ok().and_then(|t| serde_json::from_str(&t).ok()) };
    std::panic::set_hook(Box::new(|_| {})); // a call that panics is data here ("no answer"), not noise
    if let Some(path) = opt("--replay") {
        replay(table::RULES, &trees, &path, timeout);
        std::process::exit(0);
    }
    for rule in table::RULES {
        if only.as_ref().is_some_and(|o| !o.iter().any(|x| x == rule.id)) || prefix.as_ref().is_some_and(|p| !rule.id.contains(p.as_str())) {
            continue;
        }
        let rd = reading(&trees, rule.id);
        let current = Arc::new(Mutex::new(None::<J>));
        let c2 = current.clone();
        let t0 = Instant::now();
        let out = match with_timeout(timeout, move || run_rule(rule, rd, cases, seed, size, c2)) {
            Some(o) => o,
            None => json!({"rule": rule.id, "status": "hang", "cases": J::Null, "calls": J::Null, "seed": seed,
                           "witness": current.lock().unwrap().clone(), "bits": J::Null,
                           "message": format!("did not finish within {timeout} s; the input shown is the one being evaluated"),
                           "elapsed_ms": t0.elapsed().as_millis() as u64}),
        };
        println!("{out}");
        if out["status"] == "hang" {
            // the thread that hangs cannot be stopped and would take a core from every rule after it: stop here; the caller
            // (clausal/evidence.py) starts the remaining rules in a fresh process
            std::process::exit(0);
        }
    }
    std::process::exit(0); // threads left behind by a hang must not keep the process alive
}
