//! THE RUST READING OF EVERY VOCABULARY PIECE, and the evaluator of composition trees.
//!
//! There is no step and no predicate per sentence here. `clausal` compiles a sentence to a tree of
//! vocabulary pieces (../build/trees.json); this module gives each piece (domain word, modifier, frame)
//! ONE Rust reading and evaluates the tree. It is a second implementation of each piece, by the same author as
//! the first (so agreement shows consistency, not independent confirmation): the first is the Lean
//! definition (lean/Wallet/Pieces.lean, lean/Ledger/Pieces.lean, lean/Frames). The two are compared on
//! generated inputs by tests/grid.rs, and the cucumber steps of tests/bdd.rs are this evaluator applied to
//! the tree of the step at hand.
//!
//! The one place a piece is read:   `eval`            domain words and modifiers (one match arm per piece id)
//!                                  `run_op`, `accepted`   operations, on the COMPILED crates under test
//!                                  `frame_content`   frames about one call (one arm per frame id)
//!                                  `frame2_content`  frames that compare two calls
//!                                  `variation`, `reference`   relations between two calls; reference functions
//!                                  `tie`             how the second input of a tied sequence is got from the first
//! and the fail-closed defaults are in `holds_at` / `holds_at2` (the counterpart of `Frames.Op.HoldsAt`).
//!
//! Numbers are u128 so that sums of u64 balances cannot wrap.
use serde_json::Value as J;
use std::panic::{catch_unwind, AssertUnwindSafe};

#[derive(Debug, Clone, PartialEq)]
pub enum Val {
    Num(u128),
    Bool(bool),
    List(Vec<Val>),
    Opt(Option<Box<Val>>),
    Transfer(usize, usize, u64),
    Name(String),    // a named value: a wallet error, or the wallet answer "ok"
    Wallet(u64),     // an actor: a wallet is its balance
    Ledger(Vec<u64>), // an actor: a ledger is its balances, account 0 first
    Counter(u64),    // an actor: a counter is its count
    Key(u64),        // an actor of the signed intake: the expected key is its number
    Seq(u64),        // an actor of the signed intake: the last counter is its number
    Msg(u64, u64, u64, u64), // a message: payload, counter, tag, hint
    Parser(u64),     // an actor: a parser is its size limit
    Record(bool, u8, bool, u8), // what a parse answers: for each key, whether it was given and its digit
    Unit,
}

impl Val {
    pub fn num(&self) -> u128 {
        match self {
            Val::Num(n) => *n,
            v => panic!("a number is needed, got {v:?}"),
        }
    }
    pub fn truth(&self) -> bool {
        match self {
            Val::Bool(b) => *b,
            v => panic!("a condition is needed, got {v:?}"),
        }
    }
    pub fn list(&self) -> &[Val] {
        match self {
            Val::List(l) => l,
            v => panic!("a collection is needed, got {v:?}"),
        }
    }
    pub fn ledger(&self) -> &[u64] {
        match self {
            Val::Ledger(l) => l,
            v => panic!("a ledger is needed, got {v:?}"),
        }
    }
    pub fn msg(&self) -> (u64, u64, u64, u64) {
        match self {
            Val::Msg(p, c, t, h) => (*p, *c, *t, *h),
            v => panic!("a message is needed, got {v:?}"),
        }
    }
    pub fn transfer(&self) -> (usize, usize, u64) {
        match self {
            Val::Transfer(f, t, a) => (*f, *t, *a),
            v => panic!("a transfer is needed, got {v:?}"),
        }
    }
}

/// The actors of a scenario (or the roles of a Rule), in order of first mention, each with its state.
pub type Actors = Vec<(String, Val)>;

pub fn actor<'a>(actors: &'a Actors, name: &str) -> &'a Val {
    actors.iter().find(|(n, _)| n == name).map(|(_, v)| v).unwrap_or_else(|| panic!("no Given builds {name}"))
}

// ---------------------------------------------------------------------------------------------- literals

pub fn parse_transfer(s: &str) -> (usize, usize, u64) {
    let (from, rest) = s.trim().split_once("->").unwrap_or_else(|| panic!("not a transfer: {s}"));
    let (to, amount) = rest.split_once(':').unwrap_or_else(|| panic!("not a transfer: {s}"));
    (from.parse().expect("sender"), to.parse().expect("receiver"), amount.parse().expect("amount"))
}

fn items(s: &str) -> Vec<&str> {
    let inner = s.trim().strip_prefix('[').and_then(|x| x.strip_suffix(']')).unwrap_or_else(|| panic!("not a list: {s}")).trim();
    if inner.is_empty() {
        vec![]
    } else {
        inner.split(", ").collect()
    }
}

/// A literal of one of the vocabulary's literal types (glossary.yaml `param_types`), as a value.
pub fn parse_lit(typ: &str, s: &str) -> Val {
    match typ {
        "amount" | "index" => Val::Num(s.trim().parse().unwrap_or_else(|_| panic!("not a number: {s}"))),
        "balances" => Val::List(items(s).into_iter().map(|x| parse_lit("amount", x)).collect()),
        "transfer" => {
            let (f, t, a) = parse_transfer(s);
            Val::Transfer(f, t, a)
        }
        "batch" => Val::List(items(s).into_iter().map(|x| parse_lit("transfer", x)).collect()),
        "error" => Val::Name(s.to_string()),
        "message" => {
            let f: Vec<u64> = s.trim().split('/').map(|x| x.parse().unwrap_or_else(|_| panic!("not a message: {s}"))).collect();
            assert!(f.len() == 4, "not a message: {s}");
            Val::Msg(f[0], f[1], f[2], f[3])
        }
        "size" => Val::Num(s.trim().parse().unwrap_or_else(|_| panic!("not a number: {s}"))),
        // an input, written as text between double quotes: its bytes
        "bytes" => {
            let t = s.trim().strip_prefix('"').and_then(|x| x.strip_suffix('"')).unwrap_or_else(|| panic!("not an input: {s}"));
            Val::List(t.bytes().map(|b| Val::Num(b as u128)).collect())
        }
        t => panic!("unknown literal type {t}"),
    }
}

/// An actor built from the one value that is the whole of it (a wallet from its balance, a ledger from its balances).
pub fn build_actor(typ: &str, v: &Val) -> Val {
    match typ {
        "wallet" => Val::Wallet(u64::try_from(v.num()).expect("a wallet balance is a u64")),
        "ledger" => Val::Ledger(v.list().iter().map(|x| u64::try_from(x.num()).expect("a balance is a u64")).collect()),
        "counter" => Val::Counter(u64::try_from(v.num()).expect("a count is a u64")),
        "sigkey" => Val::Key(u64::try_from(v.num()).expect("a key number is a u64")),
        "sigcounter" => Val::Seq(u64::try_from(v.num()).expect("a counter is a u64")),
        "parser" => Val::Parser(u64::try_from(v.num()).expect("a size limit is a u64")),
        t => panic!("unknown actor type {t}"),
    }
}

// ---------------------------------------------------------------------------------------------- where leaves point

/// Where the leaves of a tree point: captures of a cucumber step (`slot`), names bound by the caller (`ref`:
/// outline parameters, the roles of a Rule), or literals written in the sentence (`lit`).
#[derive(Default, Clone)]
pub struct Bind {
    pub slots: Vec<String>,
    pub refs: Vec<(String, Val)>,
}

impl Bind {
    pub fn actor_name(&self, leaf: &J) -> String {
        if let Some(n) = leaf.get("slot").and_then(J::as_u64) {
            return self.slots[n as usize].clone();
        }
        leaf["ref"].as_str().expect("an actor leaf has a slot or a ref").to_string()
    }
    pub fn value(&self, leaf: &J) -> Val {
        let typ = leaf["type"].as_str().expect("a value leaf has a type");
        if let Some(n) = leaf.get("slot").and_then(J::as_u64) {
            return parse_lit(typ, &self.slots[n as usize]);
        }
        if let Some(l) = leaf.get("lit").and_then(J::as_str) {
            return parse_lit(typ, l);
        }
        let r = leaf["ref"].as_str().expect("a value leaf has a slot, a lit or a ref");
        self.refs.iter().find(|(n, _)| n == r).map(|(_, v)| v.clone()).unwrap_or_else(|| panic!("nothing binds {r}"))
    }
}

/// What a piece is read on: a state (before or after the call), the answer, and the item a quantifier is at.
pub struct Env<'a> {
    pub bind: &'a Bind,
    pub actors: &'a Actors,
    pub ans: Option<&'a Val>,
    pub item: Option<&'a Val>,
    pub op: &'a str, // the (last) operation: "accepted" is the operation's own word
}

impl<'a> Env<'a> {
    fn with_item(&self, item: &'a Val) -> Env<'a> {
        Env { bind: self.bind, actors: self.actors, ans: self.ans, item: Some(item), op: self.op }
    }
    fn actor(&self, leaf: &J) -> &'a Val {
        actor(self.actors, &self.bind.actor_name(leaf))
    }
    fn ans(&self) -> &'a Val {
        self.ans.expect("this piece speaks of the answer, and there is none here")
    }
}

// ---------------------------------------------------------------------------------------------- the ledger's own words

pub fn bal(l: &[u64], k: u128) -> u128 {
    usize::try_from(k).ok().and_then(|i| l.get(i)).map(|&v| v as u128).unwrap_or(0)
}

/// "valid on": both accounts exist and differ, the sender covers the amount, the receiver's balance stays within u64.
pub fn valid(l: &[u64], t: (usize, usize, u64)) -> bool {
    let (from, to, amount) = t;
    from < l.len() && to < l.len() && from != to && amount as u128 <= bal(l, from as u128) && bal(l, to as u128) + amount as u128 <= u64::MAX as u128
}

// ---------------------------------------------------------------------------------------------- the parser's own words
// The format of kvparse written out a THIRD time (the code under test; lean/Kvparse/Pieces.lean; here), by one author.

fn kv_bytes(v: &Val) -> Vec<u8> {
    v.list().iter().map(|x| u8::try_from(x.num()).expect("a byte")).collect()
}

fn kv_val(b: &[u8]) -> Val {
    Val::List(b.iter().map(|&x| Val::Num(x as u128)).collect())
}

/// "the fields of the input": what stands between its `;`. The empty input has no field.
pub fn kv_fields(b: &[u8]) -> Vec<Vec<u8>> {
    if b.is_empty() {
        vec![]
    } else {
        b.split(|&c| c == b';').map(|f| f.to_vec()).collect()
    }
}

/// the key of a field: its bytes before the first `=`
pub fn kv_key(f: &[u8]) -> Vec<u8> {
    f.iter().copied().take_while(|&c| c != b'=').collect()
}

pub fn kv_keys(b: &[u8]) -> Vec<Vec<u8>> {
    kv_fields(b).iter().map(|f| kv_key(f)).collect()
}

/// a field of the format: a known key, `=`, one decimal digit, and nothing else
fn kv_shaped(f: &[u8]) -> bool {
    f.len() == 3 && (f[0] == b'a' || f[0] == b'b') && f[1] == b'=' && f[2].is_ascii_digit()
}

/// "the input is well-formed": every field is a field of the format, and the keys are `a`, or `b`, or `a` then `b`.
pub fn kv_well_formed(b: &[u8]) -> bool {
    let keys = kv_keys(b);
    kv_fields(b).iter().all(|f| kv_shaped(f)) && (keys == [b"a".to_vec()] || keys == [b"b".to_vec()] || keys == [b"a".to_vec(), b"b".to_vec()])
}

/// the specification's encoder: a record written back in the format. PARTIAL (lean/Kvparse/Pieces.lean, `KV.encode`):
/// a record the format cannot write has no encoding. Writable: at least one key given, each digit at most 9, and the
/// digit of a key that is not given is 0.
pub fn kv_encode(has_a: bool, a: u8, has_b: bool, b: u8) -> Option<Vec<u8>> {
    if !((has_a || has_b) && a <= 9 && b <= 9 && (has_a || a == 0) && (has_b || b == 0)) {
        return None;
    }
    let mut out = vec![];
    if has_a {
        out.extend_from_slice(&[b'a', b'=', b'0' + a]);
    }
    if has_a && has_b {
        out.push(b';');
    }
    if has_b {
        out.extend_from_slice(&[b'b', b'=', b'0' + b]);
    }
    Some(out)
}

/// "the reference parse": the record of the input if it is within the limit and well-formed, otherwise none.
fn kv_ref_parse(limit: u64, b: &[u8]) -> Val {
    if b.len() as u128 > limit as u128 || !kv_well_formed(b) {
        return Val::Opt(None);
    }
    let value = |k: u8| kv_fields(b).iter().find(|f| f.first() == Some(&k)).map(|f| f[2] - b'0');
    Val::Opt(Some(Box::new(Val::Record(value(b'a').is_some(), value(b'a').unwrap_or(0), value(b'b').is_some(), value(b'b').unwrap_or(0)))))
}

fn kv_limit(v: &Val) -> u64 {
    match v {
        Val::Parser(n) => *n,
        v => panic!("a parser is needed, got {v:?}"),
    }
}

fn opt_num(o: Option<u64>) -> Val {
    Val::Opt(o.map(|v| Box::new(Val::Num(v as u128))))
}

// ---------------------------------------------------------------------------------------------- domain words and modifiers

fn arg<'j>(node: &'j J, name: &str) -> &'j J {
    node["a"].get(name).unwrap_or_else(|| panic!("piece {} has no argument {name}", node["p"]))
}

fn is_leaf(x: &J) -> bool {
    x.get("k").is_some()
}

/// The value of a tree: ONE arm per domain word and per modifier of the Clausebook (clausebook/).
pub fn eval(x: &J, e: &Env) -> Val {
    if is_leaf(x) {
        return if x["k"] == "actor" { e.actor(x).clone() } else { e.bind.value(x) };
    }
    if let Some(l) = x.as_array() {
        return Val::List(l.iter().map(|y| eval(y, e)).collect());
    }
    let p = x["p"].as_str().expect("a node names its piece");
    let a = |name: &str| eval(arg(x, name), e);
    let n = |name: &str| a(name).num();
    if let Some(typ) = x.get("per_actor").and_then(J::as_str) {
        // the plural of a per-actor measure: one number per actor of that type, in order of first mention
        return Val::List(e.actors.iter().filter(|(_, v)| matches!((typ, v), ("wallet", Val::Wallet(_)) | ("ledger", Val::Ledger(_))))
                         .map(|(_, v)| match (p, v) {
                             ("w.balance", Val::Wallet(b)) => Val::Num(*b as u128),
                             _ => panic!("no plural reading of {p}"),
                         }).collect());
    }
    match p {
        // ---- wallet
        "w.balance" => match a("w") {
            Val::Wallet(b) => Val::Num(b as u128),
            v => panic!("a wallet is needed, got {v:?}"),
        },
        "w.maximum" | "l.maximum" => Val::Num(u64::MAX as u128),
        "w.succeeds" => Val::Bool(*e.ans() == Val::Name("ok".into())),
        "w.rejected_with" => Val::Bool(*e.ans() == a("e")),
        // ---- counter
        "ctr.count" => match a("c") {
            Val::Counter(n) => Val::Num(n as u128),
            v => panic!("a counter is needed, got {v:?}"),
        },
        // ---- signed intake (the toy relation, written again here: the tag is three hex digits, one each from the key,
        //      the payload and the counter). A STAND-IN for a signature check.
        "in.verifies" => match (a("k"), a("m")) {
            (Val::Key(k), Val::Msg(p, c, t, _)) => Val::Bool(t as u128 == (k % 16) as u128 * 256 + (p % 16) as u128 * 16 + (c % 16) as u128),
            v => panic!("a key and a message are needed, got {v:?}"),
        },
        "in.last" => match a("c") {
            Val::Seq(n) => Val::Num(n as u128),
            v => panic!("a last counter is needed, got {v:?}"),
        },
        "in.counter_of" => Val::Num(a("m").msg().1 as u128),
        // ---- kvparse
        "kv.limit" => Val::Num(kv_limit(&a("p")) as u128),
        "kv.length" => Val::Num(a("i").list().len() as u128),
        "kv.well_formed" => Val::Bool(kv_well_formed(&kv_bytes(&a("i")))),
        "kv.fields" => Val::List(kv_fields(&kv_bytes(&a("i"))).iter().map(|f| kv_val(f)).collect()),
        "kv.known" => {
            let k = kv_key(&kv_bytes(e.item.expect("`is a known field` is said of a field")));
            Val::Bool(k == b"a" || k == b"b")
        }
        "kv.keys" => Val::List(kv_keys(&kv_bytes(&a("i"))).iter().map(|k| kv_val(k)).collect()),
        "kv.repeated" => {
            let k = kv_bytes(e.item.expect("`is repeated in` is said of a key"));
            Val::Bool(kv_keys(&kv_bytes(&a("i"))).iter().filter(|x| **x == k).count() >= 2)
        }
        "kv.count" => Val::Num(match e.ans() {
            Val::Opt(Some(r)) => match **r {
                Val::Record(ha, _, hb, _) => ha as u128 + hb as u128,
                ref v => panic!("a record is needed, got {v:?}"),
            },
            _ => 0,
        }),
        "kv.field_limit" => Val::Num(2),
        "kv.encoding" => Val::Opt(match e.ans() {
            Val::Opt(Some(r)) => match **r {
                Val::Record(ha, x, hb, y) => kv_encode(ha, x, hb, y).map(|b| Box::new(kv_val(&b))),
                ref v => panic!("a record is needed, got {v:?}"),
            },
            _ => None,
        }),
        "kv.as_encoding" => Val::Opt(Some(Box::new(a("x")))),
        // ---- ledger
        "l.ledger" => Val::List(a("l").ledger().iter().map(|&v| Val::Num(v as u128)).collect()),
        "l.balances_of" => Val::List(a("l").ledger().iter().map(|&v| Val::Num(v as u128)).collect()),
        "l.bal_of" => Val::Num(bal(a("l").ledger(), n("k"))),
        "l.balance_at" => opt_num(usize::try_from(n("i")).ok().and_then(|i| a("l").ledger().get(i).copied())),
        "l.accounts" => Val::List((0..a("l").ledger().len()).map(|k| Val::Num(k as u128)).collect()),
        "l.is_account" => Val::Bool(n("i") < a("l").ledger().len() as u128),
        "l.valid" => Val::Bool(valid(a("l").ledger(), e.item.expect("`valid on` is said of a transfer").transfer())),
        "l.the_transfer" => a("t"),
        "l.transfers" => a("b"),
        "l.length" => Val::Num(a("b").list().len() as u128),
        "l.sender" => Val::Num(a("t").transfer().0 as u128),
        "l.receiver" => Val::Num(a("t").transfer().1 as u128),
        "l.amount_of" => Val::Num(a("t").transfer().2 as u128),
        "l.applied" => Val::Num(e.ans().num()),
        "l.stopped_at" => Val::List(usize::try_from(e.ans().num()).ok().and_then(|k| a("b").list().get(k).cloned()).into_iter().collect()),
        "l.result" => e.ans().clone(),
        "l.accepted" => Val::Bool(*e.ans() == Val::Bool(true)),
        "l.found" => Val::Bool(matches!(e.ans(), Val::Opt(Some(_)))),
        // ---- modifiers: values
        "amount_value" | "index_number" | "index_count" | "balances_value" => a("x"),
        "amount_result" => Val::Opt(Some(Box::new(a("x")))),
        "zero" => Val::Num(0),
        // ---- modifiers: comparisons
        "is" => Val::Bool(a("m") == a("t")),
        "equals" => Val::Bool(a("a") == a("b")), // two values known before the call (its negation is `not` around it)
        "not_more_than" => Val::Bool(n("t") <= n("m")),
        "more_than" => Val::Bool(n("m") < n("t")),
        "exceeds" => Val::Bool(n("t") < n("m")),
        "at_most_value" => Val::Bool(n("m") <= n("t")),
        "sum_within" => Val::Bool(n("m") + n("t") <= n("z")),
        "sum_exceeds" => Val::Bool(n("z") < n("m") + n("t")),
        "not" => Val::Bool(!a("p").truth()),
        // ---- modifiers: measures from measures
        "aggregate" => Val::Num(a("ns").list().iter().map(Val::num).sum()),
        "all_of" => a("pm"),
        // ---- modifiers: quantifiers over a named collection
        "holds_of" => {
            let i = a("i");
            eval(arg(x, "p"), &e.with_item(&i))
        }
        "every" => Val::Bool(a("c").list().iter().all(|i| eval(arg(x, "p"), &e.with_item(i)).truth())),
        "no_such" => Val::Bool(!a("c").list().iter().any(|i| eval(arg(x, "p"), &e.with_item(i)).truth())),
        "some_of" => Val::Bool(a("c").list().iter().any(|i| eval(arg(x, "p"), &e.with_item(i)).truth())),
        "the_first" => {
            let c = a("c");
            Val::Bool(match c.list().first() {
                Some(i) => eval(arg(x, "p"), &e.with_item(i)).truth(),
                None => false,
            })
        }
        // ---- the operation's own notion of an accepted answer
        "accepted" => Val::Bool(accepted(e.op, e.ans())),
        _ => panic!("no Rust reading of vocabulary piece `{p}`"),
    }
}

/// "changes only": what is compared part by part (the domain word's `part_measure`).
fn part_measure(parts: &J, e: &Env, k: &Val) -> Val {
    match parts["p"].as_str() {
        Some("l.accounts") => Val::Num(bal(eval(arg(parts, "l"), e).ledger(), k.num())),
        p => panic!("no part measure for {p:?}"),
    }
}

// ---------------------------------------------------------------------------------------------- operations

/// One call of an operation on the COMPILED crate: `Some((answer, state afterwards))`, or `None` if it gave no
/// answer (it panicked). `state` holds the operation's actors in the order of its roles.
pub fn run_op(op: &str, state: &[Val], input: &Val) -> Option<(Val, Vec<Val>)> {
    let state = state.to_vec();
    let input = input.clone();
    let op = op.to_string();
    catch_unwind(AssertUnwindSafe(move || {
        let outcome = |r: Result<(), wallet::WalletError>| match r {
            Ok(()) => Val::Name("ok".into()),
            Err(wallet::WalletError::InsufficientFunds) => Val::Name("insufficient funds".into()),
            Err(wallet::WalletError::Overflow) => Val::Name("overflow".into()),
        };
        let w = |v: &Val| match v {
            Val::Wallet(b) => wallet::Wallet { balance: *b },
            v => panic!("a wallet is needed, got {v:?}"),
        };
        let amount = || u64::try_from(input.num()).expect("an amount is a u64");
        let batch = || -> Vec<ledger::Transfer> {
            input.list().iter().map(|t| { let (from, to, amount) = t.transfer(); ledger::Transfer { from, to, amount } }).collect()
        };
        let l = || ledger::Ledger { balances: state[0].ledger().to_vec() };
        match op.as_str() {
            "w.transfer" => {
                let (mut s, mut d) = (w(&state[0]), w(&state[1]));
                let r = wallet::transfer(&mut s, &mut d, amount());
                (outcome(r), vec![Val::Wallet(s.balance), Val::Wallet(d.balance)])
            }
            "w.deposit" => {
                let mut x = w(&state[0]);
                let r = x.deposit(amount());
                (outcome(r), vec![Val::Wallet(x.balance)])
            }
            "w.withdraw" => {
                let mut x = w(&state[0]);
                let r = x.withdraw(amount());
                (outcome(r), vec![Val::Wallet(x.balance)])
            }
            "l.apply_batch" => {
                let mut x = l();
                let n = x.apply_batch(&batch());
                (Val::Num(n as u128), vec![Val::Ledger(x.balances)])
            }
            "l.apply_all" => {
                let mut x = l();
                let ok = x.apply_all(&batch());
                (Val::Bool(ok), vec![Val::Ledger(x.balances)])
            }
            "l.apply" => {
                let mut x = l();
                let (from, to, amount) = input.transfer();
                let ok = x.apply(&ledger::Transfer { from, to, amount });
                (Val::Bool(ok), vec![Val::Ledger(x.balances)])
            }
            "ctr.bump" => {
                let mut x = match &state[0] {
                    Val::Counter(n) => counter::Counter { count: *n },
                    v => panic!("a counter is needed, got {v:?}"),
                };
                let ok = x.bump(amount());
                (Val::Bool(ok), vec![Val::Counter(x.count)])
            }
            "in.intake" => {
                let (mut k, mut c) = match (&state[0], &state[1]) {
                    (Val::Key(k), Val::Seq(c)) => (sigintake::Key { id: *k }, sigintake::Counter { last: *c }),
                    v => panic!("an expected key and a last counter are needed, got {v:?}"),
                };
                let (payload, counter, tag, hint) = input.msg();
                let ok = sigintake::intake(&mut k, &mut c, sigintake::Message { payload, counter, tag, hint });
                (Val::Bool(ok), vec![Val::Key(k.id), Val::Seq(c.last)])
            }
            "kv.parse" => {
                let p = kvparse::Parser { limit: usize::try_from(kv_limit(&state[0])).expect("a size limit is a usize") };
                let r = p.parse(&kv_bytes(&input));
                (Val::Opt(r.map(|r| Box::new(Val::Record(r.has_a, r.a, r.has_b, r.b)))), state.clone())
            }
            "l.total" => (opt_num(l().total()), state.clone()),
            "l.lookup" => (opt_num(l().balance(usize::try_from(input.num()).expect("an account number is a usize"))), state.clone()),
            o => panic!("no Rust binding of operation `{o}`"),
        }
    }))
    .ok()
}

/// Which answers of an operation count as accepted (the `accepted` argument of its Lean definition).
pub fn accepted(op: &str, ans: &Val) -> bool {
    match op {
        "w.transfer" | "w.deposit" | "w.withdraw" => *ans == Val::Name("ok".into()),
        "l.apply_batch" => true,
        "l.apply_all" | "l.apply" | "ctr.bump" | "in.intake" => *ans == Val::Bool(true),
        "l.total" | "l.lookup" | "kv.parse" => matches!(ans, Val::Opt(Some(_))),
        o => panic!("no Rust binding of operation `{o}`"),
    }
}

/// "internal": every party the input names is a member of the state.
pub fn internal(op: &str, state: &[Val], input: &Val) -> bool {
    match op {
        "l.apply" => {
            let (from, to, _) = input.transfer();
            from < state[0].ledger().len() && to < state[0].ledger().len()
        }
        o => panic!("`internal` has no reading for operation `{o}`"),
    }
}

// ---------------------------------------------------------------------------------------------- one run of a (sequence of) operation(s)

/// What a scenario's Whens (or a Rule's subject) did from one state: the state before, each call's input, and
/// either the LAST call's answer with the state afterwards, or nothing if some call gave no answer.
#[derive(Debug, Clone)]
pub struct Run {
    pub ops: Vec<String>,
    pub state: Vec<String>, // the operation's actors, in the order of its roles
    pub inputs: Vec<Val>,   // one input per call
    pub before: Actors,
    pub result: Option<(Val, Actors)>,
}

/// Run `ops` in order from `before`, each on the state the one before left. `state` names the operation's actors
/// in the order of its roles; every other actor is a bystander and stays as it was.
pub fn run_seq(ops: &[String], state: &[String], inputs: &[Val], before: &Actors) -> Run {
    let mut cur = before.clone();
    let mut last = None;
    for (op, inp) in ops.iter().zip(inputs) {
        let st: Vec<Val> = state.iter().map(|n| actor(&cur, n).clone()).collect();
        match run_op(op, &st, inp) {
            None => return Run { ops: ops.to_vec(), state: state.to_vec(), inputs: inputs.to_vec(), before: before.clone(), result: None },
            Some((ans, after)) => {
                for (n, v) in state.iter().zip(after) {
                    cur.iter_mut().find(|(m, _)| m == n).expect("a role names an actor").1 = v;
                }
                last = Some(ans);
            }
        }
    }
    Run { ops: ops.to_vec(), state: state.to_vec(), inputs: inputs.to_vec(), before: before.clone(), result: last.map(|a| (a, cur)) }
}

// ---------------------------------------------------------------------------------------------- frames

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Calls {
    Every,
    Accepted,
    Rejected,
}

pub fn calls_of(mods: &J) -> Calls {
    let has = |m: &str| mods.as_array().map(|a| a.iter().any(|x| x == m)).unwrap_or(false);
    if has("rejected") {
        Calls::Rejected
    } else if has("successful") {
        Calls::Accepted
    } else {
        Calls::Every
    }
}

/// THE DEFAULTS, on the Rust side (the counterpart of `Frames.Op.HoldsAt`): what a frame with content `q` says
/// of one run that is in scope. Every call: it must answer and `q` holds. Accepted / rejected calls only: IF it
/// answers with that kind of answer, `q` holds.
pub fn holds_at(calls: Calls, run: &Run, q: impl Fn(&Val, &Actors) -> bool) -> bool {
    let op = run.ops.last().expect("a run has an operation");
    match (&run.result, calls) {
        (None, Calls::Every) => false,
        (None, _) => true,
        (Some((ans, after)), Calls::Every) => q(ans, after),
        (Some((ans, after)), Calls::Accepted) => !accepted(op, ans) || q(ans, after),
        (Some((ans, after)), Calls::Rejected) => accepted(op, ans) || q(ans, after),
    }
}

/// The same for two runs (the counterpart of `Frames.Op.HoldsAt2`), both in scope and related as stated.
pub fn holds_at2(calls: Calls, r1: &Run, r2: &Run, q: impl Fn(&Val, &Val) -> bool) -> bool {
    let op = r1.ops.last().expect("a run has an operation");
    match (&r1.result, &r2.result, calls) {
        (Some((a1, _)), Some((a2, _)), Calls::Every) => q(a1, a2),
        (Some((a1, _)), Some((a2, _)), Calls::Accepted) => !(accepted(op, a1) && accepted(op, a2)) || q(a1, a2),
        (Some((a1, _)), Some((a2, _)), Calls::Rejected) => !(!accepted(op, a1) && !accepted(op, a2)) || q(a1, a2),
        (_, _, Calls::Every) => false,
        _ => true,
    }
}

/// The content of a frame about ONE call: one arm per frame id of clausebook/core.yaml. `before` and `after` are the
/// states, `ans` the answer; conditions and values known before the call are read on `before`.
pub fn frame_content(node: &J, bind: &Bind, run: &Run, ans: &Val, after: &Actors) -> bool {
    let op = run.ops.last().expect("a run has an operation").as_str();
    let pre = Env { bind, actors: &run.before, ans: Some(ans), item: None, op };
    let post = Env { bind, actors: after, ans: Some(ans), item: None, op };
    let f = node["p"].as_str().expect("a claim names its frame");
    let before = |name: &str| eval(arg(node, name), &pre);
    let afterw = |name: &str| eval(arg(node, name), &post);
    match f {
        "always_answers" => true,
        "never_changes" => afterw("m") == before("m"),
        "changes_only" => {
            let parts = arg(node, "c");
            let xs = before("xs");
            afterw("c") == before("c")
                && before("c").list().iter().all(|k| xs.list().contains(k) || part_measure(parts, &post, k) == part_measure(parts, &pre, k))
        }
        "always" => before("c").truth(),
        "never" => !before("c").truth(),
        "if_then" => !before("k").truth() || before("c").truth(),
        "only_if" => !before("c").truth() || before("k").truth(),
        "exactly_when" => before("c").truth() == before("k").truth(),
        "rejected_unchanged" => !accepted(op, ans) && *after == run.before,
        "increases_by" => afterw("m").num() == before("m").num() + before("t").num(),
        "decreases_by" => afterw("m").num() + before("t").num() == before("m").num(),
        "becomes" => afterw("m") == before("t"),
        "result_is" => before("a") == before("t"),
        "result_at_most" => before("a").num() <= before("t").num(),
        "result_at_least" => before("t").num() <= before("a").num(),
        "at_most" => afterw("m").num() <= before("t").num(),
        "at_least" => before("t").num() <= afterw("m").num(),
        "each_at_most" => {
            // every number of the collection, read after the call, against a value known before it
            let bound = before("t").num();
            afterw("ns").list().iter().all(|n| n.num() <= bound)
        }
        "every_of" => afterw("c").list().iter().all(|i| eval(arg(node, "p"), &post.with_item(i)).truth()),
        "none_of" => !afterw("c").list().iter().any(|i| eval(arg(node, "p"), &post.with_item(i)).truth()),
        "within" => {
            let sup = before("d");
            afterw("c").list().iter().all(|i| sup.list().contains(i))
        }
        "covers" => {
            let sup = afterw("c");
            before("d").list().iter().all(|i| sup.list().contains(i))
        }
        "agrees_with" => {
            let state: Vec<Val> = run.state.iter().map(|n| actor(&run.before, n).clone()).collect();
            let (want_ans, want_state) =
                reference(arg(node, "r")["p"].as_str().expect("a reference names its piece"), &state, run.inputs.last().unwrap_or(&Val::Unit));
            *ans == want_ans && run.state.iter().map(|n| actor(after, n).clone()).collect::<Vec<_>>() == want_state
        }
        _ => panic!("no Rust reading of frame `{f}`"),
    }
}

/// The content of a frame that compares TWO calls: one arm per frame id.
pub fn frame2_content(node: &J, bind: &Bind, op: &str, a1: &Val, a2: &Val) -> bool {
    let none: Actors = vec![];
    let cls = |ans: &Val| eval(arg(node, "c"), &Env { bind, actors: &none, ans: Some(ans), item: None, op }).truth();
    match node["p"].as_str().expect("a claim names its frame") {
        "monotone" => !cls(a1) || cls(a2),
        "same_answer" => a1 == a2,
        "same_answer_if" => !cls(a1) || a1 == a2,
        f => panic!("no Rust reading of two-run frame `{f}`"),
    }
}

/// A relation between two calls (domain words of kind `variation`): one arm per piece id.
pub fn variation(piece: &str, s: &[Val], a: &Val, s2: &[Val], a2: &Val) -> bool {
    let same_route = || {
        let ((f, t, _), (f2, t2, _)) = (a.transfer(), a2.transfer());
        s2 == s && f2 == f && t2 == t
    };
    match piece {
        "l.smaller_amount" => same_route() && a2.transfer().2 <= a.transfer().2,
        "l.larger_amount" => same_route() && a.transfer().2 <= a2.transfer().2,
        "l.only_amount_differs" => same_route(),
        "l.agrees_at_account" => {
            let at = |l: &Val, i: u128| usize::try_from(i).ok().and_then(|k| l.ledger().get(k).copied());
            a2 == a && at(&s2[0], a.num()) == at(&s[0], a.num())
        }
        "l.extended" => a2 == a && s2[0].ledger().starts_with(s[0].ledger()),
        "in.unsigned_differs" => {
            let ((p, c, t, _), (p2, c2, t2, _)) = (a.msg(), a2.msg());
            s2 == s && p2 == p && c2 == c && t2 == t
        }
        p => panic!("no Rust reading of relation `{p}`"),
    }
}

/// A reference function (domain words of kind `reference`): what the call should answer and leave.
pub fn reference(piece: &str, s: &[Val], a: &Val) -> (Val, Vec<Val>) {
    let at = |i: u128| usize::try_from(i).ok().and_then(|k| s[0].ledger().get(k).copied());
    match piece {
        "l.ref_lookup" => (opt_num(at(a.num())), s.to_vec()),
        "l.ref_lookup_zero" => (opt_num(Some(at(a.num()).unwrap_or(0))), s.to_vec()),
        // references that are another operation of the same compiled crate (TRADES.md section 5)
        "l.ref_whole_by_batch" => match run_op("l.apply_batch", s, a) {
            Some((Val::Num(n), after)) if n == a.list().len() as u128 => (Val::Bool(true), after),
            _ => (Val::Bool(false), s.to_vec()),
        },
        "l.ref_batch_by_transfers" => {
            let (mut cur, mut n) = (s.to_vec(), 0u128);
            for t in a.list() {
                match run_op("l.apply", &cur, t) {
                    Some((Val::Bool(true), after)) => {
                        cur = after;
                        n += 1;
                    }
                    Some((_, after)) => {
                        cur = after; // the ledger the rejecting call left
                        break;
                    }
                    None => break,
                }
            }
            (Val::Num(n), cur)
        }
        "kv.ref_parse" => (kv_ref_parse(kv_limit(&s[0]), &kv_bytes(a)), s.to_vec()),
        p => panic!("no Rust reading of reference `{p}`"),
    }
}

/// A tie (pieces of category `tie`): the input of the second call of a sequence, got from the input of the first.
/// One arm per piece id.
pub fn tie(piece: &str, first: &Val) -> Val {
    match piece {
        "same_input" => first.clone(),
        p => panic!("no Rust reading of tie `{p}`"),
    }
}

/// The inputs of the calls of one unit: one per call as given, or, for a tied sequence (`tie`), the first call's input
/// and what the tie makes of it.
pub fn call_inputs(unit: &J, inputs: &[Val]) -> Vec<Val> {
    match unit.get("tie").and_then(J::as_str) {
        Some(piece) => vec![inputs[0].clone(), tie(piece, &inputs[0])],
        None => inputs.to_vec(),
    }
}

/// A claim (a frame with its holes filled and its call modifiers) about one run that is in scope.
pub fn claim_holds(claim: &J, bind: &Bind, run: &Run) -> bool {
    holds_at(calls_of(&claim["mods"]), run, |ans, after| frame_content(&claim["node"], bind, run, ans, after))
}

// ---------------------------------------------------------------------------------------------- one point of a reading

pub struct Side {
    actors: Actors,
    inputs: Vec<Val>,
    bind: Bind,
}

pub fn side(run: &J, vals: &[(String, Val)]) -> Side {
    let get = |name: &str| vals.iter().find(|(n, _)| n == name).map(|(_, v)| v.clone()).unwrap_or_else(|| panic!("no grid variable {name}"));
    let actors: Actors = run["actors"].as_array().expect("actors").iter()
        .map(|a| (a["ref"].as_str().expect("ref").to_string(), build_actor(a["type"].as_str().expect("type"), &get(a["var"].as_str().expect("var")))))
        .collect();
    let mut refs: Vec<(String, Val)> = vals.to_vec();
    let mut inputs = Vec::new();
    for i in run["inputs"].as_array().expect("inputs") {
        let v = match (i["var"].as_str(), i["lit"].as_str()) {
            (Some(var), _) => get(var),
            (None, Some(lit)) => parse_lit(i["type"].as_str().expect("type"), lit),
            _ => Val::Unit,
        };
        if let Some(r) = i["ref"].as_str() {
            refs.retain(|(n, _)| n != r);
            refs.push((r.to_string(), v.clone()));
        }
        inputs.push(v);
    }
    Side { actors, inputs, bind: Bind { slots: vec![], refs } }
}

fn strs(x: &J) -> Vec<String> {
    x.as_array().expect("a list").iter().map(|s| s.as_str().expect("a string").to_string()).collect()
}

/// ONE compiled reading (an entry of build/trees.json `readings`) at ONE point: `vals` gives every variable of the
/// reading its value. The result is the bit string the Lean side prints for that point (`RBITS`): per unit of the
/// reading its scope, then per claim the relation between the two calls (two-run frames only) and the claim itself.
/// tests/grid.rs walks the grid with it; the generated property tests (../evidence) compare it with the typed
/// reading of the same tree at every generated case.
pub fn eval_point(rd: &J, vals: &[(String, Val)]) -> String {
    let mut out = String::new();
    let s1 = side(&rd["run1"], &vals);
    let s2 = if rd["run2"].is_null() { None } else { Some(side(&rd["run2"], &vals)) };
    for unit in rd["units"].as_array().expect("units") {
        let ops = strs(&unit["ops"]);
        let state = strs(&unit["state"]);
        let last = ops.last().expect("an operation").clone();
        let in_scope = |s: &Side| {
            let st: Vec<Val> = state.iter().map(|n| actor(&s.actors, n).clone()).collect();
            (!unit["internal"].as_bool().unwrap_or(false) || internal(&ops[0], &st, &s.inputs[0]))
                && unit["conds"].as_array().expect("conds").iter()
                    .all(|c| eval(c, &Env { bind: &s.bind, actors: &s.actors, ans: None, item: None, op: &last }).truth())
        };
        let run = |s: &Side| -> Run { run_seq(&ops, &state, &call_inputs(unit, &s.inputs), &s.actors) };
        let sc1 = in_scope(&s1);
        out.push(if sc1 { '1' } else { '0' });
        let r1 = if sc1 { Some(run(&s1)) } else { None };
        for claim in unit["claims"].as_array().expect("claims") {
            if claim["runs"] == 2 {
                let s2 = s2.as_ref().expect("a two-run claim has a second call");
                let st = |s: &Side| -> Vec<Val> { state.iter().map(|n| actor(&s.actors, n).clone()).collect() };
                let rel_piece = claim["node"]["a"]["v"]["p"].as_str().expect("a two-run claim names its relation");
                let rel = variation(rel_piece, &st(&s1), &s1.inputs[0], &st(s2), &s2.inputs[0]);
                out.push(if rel { '1' } else { '0' });
                let holds = if sc1 && rel && in_scope(s2) {
                    holds_at2(calls_of(&claim["mods"]), r1.as_ref().expect("in scope"), &run(s2),
                                  |a1, a2| frame2_content(&claim["node"], &s1.bind, &last, a1, a2))
                } else {
                    true
                };
                out.push(if holds { '1' } else { '0' });
            } else {
                let holds = match &r1 {
                    Some(r) => claim_holds(claim, &s1.bind, r),
                    None => true,
                };
                out.push(if holds { '1' } else { '0' });
            }
        }
    }
    out
}

/// Every piece id a tree mentions (for the per-piece comparison counts).
pub fn pieces_of(x: &J, out: &mut Vec<String>) {
    if let Some(l) = x.as_array() {
        for y in l {
            pieces_of(y, out);
        }
    } else if let Some(p) = x.get("p").and_then(J::as_str) {
        if !out.iter().any(|q| q == p) {
            out.push(p.to_string());
        }
        if let Some(a) = x["a"].as_object() {
            for v in a.values() {
                pieces_of(v, out);
            }
        }
    }
}
