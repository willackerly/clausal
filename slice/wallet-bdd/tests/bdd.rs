//! cucumber-rs runner: the same .feature files, executed against the compiled
//! Rust. Writes Cucumber JSON to ../out/cucumber.json for the report.
//!
//! The step bodies assert the pure predicates of wallet_bdd (src/lib.rs), which are
//! the SECOND hand-written reading of each glossary phrase (the first is
//! lean/Wallet/Vocab.lean). The regexes are checked to be identical to the
//! glossary's (`python3 -m slicegen steps`); the two readings are compared on a
//! grid of arguments by tests/readings.rs and the report.
//!
//! If ../build/replay/ holds a generated feature file (the counterexamples found on
//! the Lean model), it is run as well and written to ../out/cucumber-replay.json.
use std::collections::BTreeMap;

use cucumber::{given, then, when, writer, World as _, WriterExt as _};
use ledger::{Ledger, Transfer};
use wallet::{transfer as wallet_transfer, Wallet, WalletError};
use wallet_bdd::{self as reading, Outcome};

fn outcome(r: Result<(), WalletError>) -> Outcome {
    match r {
        Ok(()) => Outcome::Ok,
        Err(WalletError::InsufficientFunds) => Outcome::InsufficientFunds,
        Err(WalletError::Overflow) => Outcome::Overflow,
    }
}

#[derive(Debug, Default, cucumber::World)]
struct World {
    before: BTreeMap<String, u64>, // balances before the first When
    after: BTreeMap<String, u64>,  // balances now: a When reads and writes these, so several Whens run in sequence
    outcome: Option<Outcome>,
    // ledger: balances before the first When / now; and what the LAST When returned
    l_before: BTreeMap<String, Vec<u64>>,
    l_after: BTreeMap<String, Vec<u64>>,
    count: Option<usize>,       // apply_batch
    result: Option<Option<u64>>, // total, balance
    flag: Option<bool>,         // apply, apply_all
}

impl World {
    fn pre(&self, who: &str) -> u64 {
        *self.before.get(who).unwrap_or_else(|| panic!("no Given builds {who}"))
    }
    fn post(&self, who: &str) -> u64 {
        *self.after.get(who).unwrap_or_else(|| panic!("no Given builds {who}"))
    }
    fn done(&mut self, r: Result<(), WalletError>) {
        self.outcome = Some(outcome(r));
    }
    fn lpre(&self, who: &str) -> &[u64] {
        self.l_before.get(who).unwrap_or_else(|| panic!("no Given builds ledger {who}"))
    }
    fn lpost(&self, who: &str) -> &[u64] {
        self.l_after.get(who).unwrap_or_else(|| panic!("no Given builds ledger {who}"))
    }
    /// The ledger as it is now, as a value of the crate under test.
    fn ledger(&self, who: &str) -> Ledger {
        Ledger { balances: self.lpost(who).to_vec() }
    }
    /// A new When forgets the previous When's result: `the result` is the last one's.
    fn clear_results(&mut self) {
        self.count = None;
        self.result = None;
        self.flag = None;
    }
}

fn balances(s: &str) -> Vec<u64> {
    reading::parse_balances(s).unwrap_or_else(|| panic!("not a list of balances: {s}"))
}
fn transfer(s: &str) -> reading::Transfer {
    reading::parse_transfer(s).unwrap_or_else(|| panic!("not a transfer: {s}"))
}
fn batch(s: &str) -> Vec<reading::Transfer> {
    reading::parse_batch(s).unwrap_or_else(|| panic!("not a batch: {s}"))
}
fn to_crate(b: &[reading::Transfer]) -> Vec<Transfer> {
    b.iter().map(|&(from, to, amount)| Transfer { from, to, amount }).collect()
}

const GIVEN_FALSE: &str = "GIVEN-FALSE: row is outside the Givens";

// glossary: G-balance
#[given(regex = r"^([A-Z][a-z]+) has a balance of (\d+)$")]
fn has_balance(w: &mut World, who: String, n: u64) {
    w.before.insert(who.clone(), n); // constructive: this Given builds the wallet
    w.after.insert(who.clone(), n);
    assert!(reading::has_balance(w.pre(&who), n), "{GIVEN_FALSE}");
}

// glossary: G-covers
#[given(regex = r"^(\d+) is not more than ([A-Z][a-z]+)'s balance$")]
fn covers(w: &mut World, n: u64, who: String) {
    assert!(reading::covers(w.pre(&who), n), "{GIVEN_FALSE}");
}

// glossary: G-exceeds
#[given(regex = r"^(\d+) is more than ([A-Z][a-z]+)'s balance$")]
fn exceeds(w: &mut World, n: u64, who: String) {
    assert!(reading::exceeds(n, w.pre(&who)), "{GIVEN_FALSE}");
}

// glossary: G-room
#[given(regex = r"^([A-Z][a-z]+)'s balance plus (\d+) does not exceed the maximum$")]
fn room_for(w: &mut World, who: String, n: u64) {
    assert!(reading::room_for(w.pre(&who), n), "{GIVEN_FALSE}");
}

// glossary: G-noroom
#[given(regex = r"^([A-Z][a-z]+)'s balance plus (\d+) exceeds the maximum$")]
fn no_room_for(w: &mut World, who: String, n: u64) {
    assert!(reading::no_room_for(w.pre(&who), n), "{GIVEN_FALSE}");
}

// glossary: W-transfer
#[when(regex = r"^([A-Z][a-z]+) transfers (\d+) to ([A-Z][a-z]+)$")]
fn transfers(w: &mut World, src: String, n: u64, dst: String) {
    assert_ne!(src, dst, "two &mut borrows cannot alias");
    let mut s = Wallet { balance: w.post(&src) };
    let mut d = Wallet { balance: w.post(&dst) };
    let r = wallet_transfer(&mut s, &mut d, n);
    w.after.insert(src, s.balance);
    w.after.insert(dst, d.balance);
    w.done(r);
}

// glossary: W-deposit
#[when(regex = r"^([A-Z][a-z]+) deposits (\d+)$")]
fn deposits(w: &mut World, who: String, n: u64) {
    let mut x = Wallet { balance: w.post(&who) };
    let r = x.deposit(n);
    w.after.insert(who, x.balance);
    w.done(r);
}

// glossary: W-withdraw
#[when(regex = r"^([A-Z][a-z]+) withdraws (\d+)$")]
fn withdraws(w: &mut World, who: String, n: u64) {
    let mut x = Wallet { balance: w.post(&who) };
    let r = x.withdraw(n);
    w.after.insert(who, x.balance);
    w.done(r);
}

// glossary: T-ok
#[then(regex = r"^the operation succeeds$")]
fn succeeds(w: &mut World) {
    assert!(reading::succeeds(w.outcome.expect("no When ran")), "got {:?}", w.outcome);
}

// glossary: T-err
#[then(regex = r"^the operation is rejected with (insufficient funds|overflow)$")]
fn rejected_with(w: &mut World, e: String) {
    let want = Outcome::parse(&e).unwrap_or_else(|| panic!("unknown error {e}"));
    assert!(reading::rejected_with(w.outcome.expect("no When ran"), want), "got {:?}", w.outcome);
}

// glossary: T-dec
#[then(regex = r"^([A-Z][a-z]+)'s balance is decreased by (\d+)$")]
fn decreased_by(w: &mut World, who: String, n: u64) {
    assert!(reading::decreased_by(w.pre(&who), w.post(&who), n), "{} -> {}", w.pre(&who), w.post(&who));
}

// glossary: T-inc
#[then(regex = r"^([A-Z][a-z]+)'s balance is increased by (\d+)$")]
fn increased_by(w: &mut World, who: String, n: u64) {
    assert!(reading::increased_by(w.pre(&who), w.post(&who), n), "{} -> {}", w.pre(&who), w.post(&who));
}

// glossary: T-same
#[then(regex = r"^([A-Z][a-z]+)'s balance is unchanged$")]
fn unchanged(w: &mut World, who: String) {
    assert!(reading::unchanged(w.pre(&who), w.post(&who)), "{} -> {}", w.pre(&who), w.post(&who));
}

// glossary: T-total
#[then(regex = r"^the total of all balances is unchanged$")]
fn total_unchanged(w: &mut World) {
    // BTreeMap: both maps hold the same actors in the same order
    let pre: Vec<u64> = w.before.values().copied().collect();
    let post: Vec<u64> = w.after.values().copied().collect();
    assert!(reading::total_unchanged(&pre, &post), "{pre:?} -> {post:?}");
}

// ====================================================================== ledger

// glossary: LG-holds
#[given(regex = r"^ledger ([A-Z][a-z]+) holds the balances (\[(?:\d+(?:, \d+)*)?\])$")]
fn l_holds(w: &mut World, who: String, bs: String) {
    let bs = balances(&bs);
    w.l_before.insert(who.clone(), bs.clone()); // constructive: this Given builds the ledger
    w.l_after.insert(who.clone(), bs.clone());
    assert!(reading::l_holds(w.lpre(&who), &bs), "{GIVEN_FALSE}");
}

// glossary: LG-sums-to
#[given(regex = r"^the balances of ledger ([A-Z][a-z]+) add up to (\d+)$")]
fn l_sums_to(w: &mut World, who: String, s: u64) {
    assert!(reading::l_sums_to(w.lpre(&who), s), "{GIVEN_FALSE}");
}

// glossary: LG-sum-too-big
#[given(regex = r"^the balances of ledger ([A-Z][a-z]+) add up to more than the maximum$")]
fn l_sum_too_big(w: &mut World, who: String) {
    assert!(reading::l_sum_too_big(w.lpre(&who)), "{GIVEN_FALSE}");
}

// glossary: LG-account
#[given(regex = r"^(\d+) is an account of ledger ([A-Z][a-z]+)$")]
fn l_is_account(w: &mut World, i: usize, who: String) {
    assert!(reading::l_is_account(w.lpre(&who), i), "{GIVEN_FALSE}");
}

// glossary: LG-no-account
#[given(regex = r"^(\d+) is not an account of ledger ([A-Z][a-z]+)$")]
fn l_not_account(w: &mut World, i: usize, who: String) {
    assert!(reading::l_not_account(w.lpre(&who), i), "{GIVEN_FALSE}");
}

// glossary: LG-valid
#[given(regex = r"^the transfer ((?:\d+)->(?:\d+):(?:\d+)) is valid on ledger ([A-Z][a-z]+)$")]
fn l_valid_on(w: &mut World, t: String, who: String) {
    assert!(reading::l_valid_on(w.lpre(&who), transfer(&t)), "{GIVEN_FALSE}");
}

// glossary: LG-invalid
#[given(regex = r"^the transfer ((?:\d+)->(?:\d+):(?:\d+)) is not valid on ledger ([A-Z][a-z]+)$")]
fn l_invalid_on(w: &mut World, t: String, who: String) {
    assert!(reading::l_invalid_on(w.lpre(&who), transfer(&t)), "{GIVEN_FALSE}");
}

// glossary: LG-first-invalid
#[given(regex = r"^the first transfer of (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) is not valid on ledger ([A-Z][a-z]+)$")]
fn l_first_invalid(w: &mut World, b: String, who: String) {
    assert!(reading::l_first_invalid(w.lpre(&who), &batch(&b)), "{GIVEN_FALSE}");
}

// glossary: LG-all-valid
#[given(regex = r"^every transfer of (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) is valid on ledger ([A-Z][a-z]+)$")]
fn l_all_valid(w: &mut World, b: String, who: String) {
    assert!(reading::l_all_valid(w.lpre(&who), &batch(&b)), "{GIVEN_FALSE}");
}

// glossary: LW-batch
#[when(regex = r"^the batch (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) is applied to ledger ([A-Z][a-z]+)$")]
fn l_apply_batch(w: &mut World, b: String, who: String) {
    let mut l = w.ledger(&who);
    let n = l.apply_batch(&to_crate(&batch(&b)));
    w.l_after.insert(who, l.balances);
    w.clear_results();
    w.count = Some(n);
}

// glossary: LW-whole
#[when(regex = r"^the batch (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) is applied to ledger ([A-Z][a-z]+) as a whole$")]
fn l_apply_all(w: &mut World, b: String, who: String) {
    let mut l = w.ledger(&who);
    let ok = l.apply_all(&to_crate(&batch(&b)));
    w.l_after.insert(who, l.balances);
    w.clear_results();
    w.flag = Some(ok);
}

// glossary: LW-transfer
#[when(regex = r"^the transfer ((?:\d+)->(?:\d+):(?:\d+)) is applied to ledger ([A-Z][a-z]+)$")]
fn l_apply(w: &mut World, t: String, who: String) {
    let mut l = w.ledger(&who);
    let ok = l.apply(&to_crate(&[transfer(&t)])[0]);
    w.l_after.insert(who, l.balances);
    w.clear_results();
    w.flag = Some(ok);
}

// glossary: LW-total
#[when(regex = r"^the total of ledger ([A-Z][a-z]+) is computed$")]
fn l_total(w: &mut World, who: String) {
    let r = w.ledger(&who).total();
    w.clear_results();
    w.result = Some(r);
}

// glossary: LW-balance
#[when(regex = r"^the balance of account (\d+) of ledger ([A-Z][a-z]+) is looked up$")]
fn l_balance(w: &mut World, i: usize, who: String) {
    let r = w.ledger(&who).balance(i);
    w.clear_results();
    w.result = Some(r);
}

// glossary: LT-total-same
#[then(regex = r"^the total of ledger ([A-Z][a-z]+)'s balances is unchanged$")]
fn l_total_unchanged(w: &mut World, who: String) {
    assert!(reading::l_total_unchanged(w.lpre(&who), w.lpost(&who)), "{:?} -> {:?}", w.lpre(&who), w.lpost(&who));
}

// glossary: LT-same
#[then(regex = r"^ledger ([A-Z][a-z]+) is unchanged$")]
fn l_unchanged(w: &mut World, who: String) {
    assert!(reading::l_unchanged(w.lpre(&who), w.lpost(&who)), "{:?} -> {:?}", w.lpre(&who), w.lpost(&who));
}

// glossary: LT-now-holds
#[then(regex = r"^ledger ([A-Z][a-z]+) now holds the balances (\[(?:\d+(?:, \d+)*)?\])$")]
fn l_now_holds(w: &mut World, who: String, bs: String) {
    assert!(reading::l_now_holds(w.lpost(&who), &balances(&bs)), "holds {:?}", w.lpost(&who));
}

// glossary: LT-at-most
#[then(regex = r"^the number of transfers applied is at most the length of (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\])$")]
fn l_applied_at_most(w: &mut World, b: String) {
    assert!(reading::l_applied_at_most(w.count.expect("the last When applied no batch"), &batch(&b)), "got {:?}", w.count);
}

// glossary: LT-none-applied
#[then(regex = r"^no transfer is applied$")]
fn l_applied_none(w: &mut World) {
    assert!(reading::l_applied_none(w.count.expect("the last When applied no batch")), "got {:?}", w.count);
}

// glossary: LT-all-applied
#[then(regex = r"^every transfer of (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) is applied$")]
fn l_applied_all(w: &mut World, b: String) {
    assert!(reading::l_applied_all(w.count.expect("the last When applied no batch"), &batch(&b)), "got {:?}", w.count);
}

// glossary: LT-exactly
#[then(regex = r"^exactly (\d+) transfers are applied$")]
fn l_applied_exactly(w: &mut World, k: usize) {
    assert!(reading::l_applied_exactly(w.count.expect("the last When applied no batch"), k), "got {:?}", w.count);
}

// glossary: LT-result
#[then(regex = r"^the result is (\d+)$")]
fn l_result_is(w: &mut World, s: u64) {
    assert!(reading::l_result_is(w.result.expect("the last When computed no result"), s), "got {:?}", w.result);
}

// glossary: LT-no-result
#[then(regex = r"^there is no result$")]
fn l_no_result(w: &mut World) {
    assert!(reading::l_no_result(w.result.expect("the last When computed no result")), "got {:?}", w.result);
}

// glossary: LT-some-result
#[then(regex = r"^there is a result$")]
fn l_some_result(w: &mut World) {
    assert!(reading::l_some_result(w.result.expect("the last When computed no result")), "got {:?}", w.result);
}

// glossary: LT-balance
#[then(regex = r"^the result is the balance of account (\d+) of ledger ([A-Z][a-z]+)$")]
fn l_result_is_balance(w: &mut World, i: usize, who: String) {
    assert!(reading::l_result_is_balance(w.result.expect("the last When computed no result"), w.lpre(&who), i), "got {:?}", w.result);
}

// glossary: LT-stops-at-invalid
#[then(regex = r"^the batch (\[(?:(?:\d+)->(?:\d+):(?:\d+)(?:, (?:\d+)->(?:\d+):(?:\d+))*)?\]) has stopped only at a transfer that is not valid on ledger ([A-Z][a-z]+) as it now stands$")]
fn l_stops_at_invalid(w: &mut World, b: String, who: String) {
    assert!(reading::l_stops_at_invalid(w.count.expect("the last When applied no batch"), &batch(&b), w.lpost(&who)),
            "got {:?}, ledger {:?}", w.count, w.lpost(&who));
}

// glossary: LT-same-if-rejected
#[then(regex = r"^if it is rejected, ledger ([A-Z][a-z]+) is unchanged$")]
fn l_unchanged_if_rejected(w: &mut World, who: String) {
    assert!(reading::l_unchanged_if_rejected(w.flag.expect("the last When gave no yes/no answer"), w.lpre(&who), w.lpost(&who)),
            "{:?}: {:?} -> {:?}", w.flag, w.lpre(&who), w.lpost(&who));
}

// glossary: LT-accepted
#[then(regex = r"^it is accepted$")]
fn l_accepted(w: &mut World) {
    assert!(reading::l_accepted(w.flag.expect("the last When gave no yes/no answer")), "got {:?}", w.flag);
}

// glossary: LT-rejected
#[then(regex = r"^it is rejected$")]
fn l_rejected(w: &mut World) {
    assert!(reading::l_rejected(w.flag.expect("the last When gave no yes/no answer")), "got {:?}", w.flag);
}

// glossary: LT-moved
#[then(regex = r"^the amount of ((?:\d+)->(?:\d+):(?:\d+)) has moved between its accounts in ledger ([A-Z][a-z]+) and no other balance changed$")]
fn l_moved(w: &mut World, t: String, who: String) {
    assert!(reading::l_moved(w.lpre(&who), w.lpost(&who), transfer(&t)), "{:?} -> {:?}", w.lpre(&who), w.lpost(&who));
}

async fn run_features(features: std::path::PathBuf, json_out: std::path::PathBuf) {
    let json = std::fs::File::create(json_out).unwrap();
    // `run` (not `run_and_exit`): failing and undefined steps are data for the
    // report, which compares each scenario's result with its expected verdict.
    World::cucumber()
        .with_writer(
            writer::Basic::stdout()
                .summarized()
                .tee::<World, _>(writer::Json::for_tee(json))
                .normalized(),
        )
        .run(features)
        .await;
}

#[tokio::main]
async fn main() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    std::fs::create_dir_all(dir.join("../out")).unwrap();
    run_features(dir.join("../features"), dir.join("../out/cucumber.json")).await;
    let replay = dir.join("../build/replay");
    if replay.join("replay.feature").exists() {
        println!("-- counterexample replay --");
        run_features(replay, dir.join("../out/cucumber-replay.json")).await;
    }
}
