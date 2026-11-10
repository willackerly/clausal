//! cucumber-rs runner: the same .feature files, executed against the compiled
//! Rust. Writes Cucumber JSON to ../out/cucumber.json for the report.
//!
//! The step bodies assert the pure predicates of scenario_bdd (src/lib.rs), which are
//! the SECOND hand-written reading of each glossary phrase (the first is
//! lean/Vocab/Inventory.lean). The regexes are checked to be identical to the
//! glossary's (`python3 -m slicegen steps`); the two readings are compared on a
//! grid of arguments by tests/readings.rs and the report.
//!
//! If ../build/replay/ holds a generated feature file (the counterexamples found on
//! the Lean model), it is run as well and written to ../out/cucumber-replay.json.
use std::collections::BTreeMap;

use cucumber::{given, then, when, writer, World as _, WriterExt as _};
use inventory::{Bin, Order, Warehouse};
use scenario_bdd::{self as reading, Bins};

#[derive(Debug, Default, cucumber::World)]
struct World {
    before: BTreeMap<String, Bins>, // each warehouse before the first When
    after: BTreeMap<String, Bins>,  // each warehouse now: a When reads and writes these
    // what the LAST When returned
    count: Option<usize>,             // restock, fill_orders, product_count
    units: Option<u64>,               // take
    opt_units: Option<Option<u64>>,   // stock_of
    opt_index: Option<Option<usize>>, // find_bin
    opt_product: Option<Option<u32>>, // dominant_product
}

impl World {
    fn pre(&self, who: &str) -> &Bins {
        self.before.get(who).unwrap_or_else(|| panic!("no Given builds warehouse {who}"))
    }
    fn post(&self, who: &str) -> &Bins {
        self.after.get(who).unwrap_or_else(|| panic!("no Given builds warehouse {who}"))
    }
    /// The warehouse as it is now, as a value of the crate under test.
    fn warehouse(&self, who: &str) -> Warehouse {
        Warehouse { bins: self.post(who).iter().map(|&(product, qty)| Bin { product, qty }).collect() }
    }
    fn put(&mut self, who: String, w: &Warehouse) {
        self.after.insert(who, w.bins.iter().map(|b| (b.product, b.qty)).collect());
    }
    /// A new When forgets the previous When's result: `the result` is the last one's.
    fn clear_results(&mut self) {
        self.count = None;
        self.units = None;
        self.opt_units = None;
        self.opt_index = None;
        self.opt_product = None;
    }
}

fn pairs(s: &str) -> Bins {
    reading::parse_pairs(s).unwrap_or_else(|| panic!("not a list of product:units pairs: {s}"))
}
fn to_orders(os: &[(u32, u64)]) -> Vec<Order> {
    os.iter().map(|&(product, qty)| Order { product, qty }).collect()
}

const GIVEN_FALSE: &str = "GIVEN-FALSE: row is outside the Givens";

// glossary: G-holds
#[given(regex = r"^warehouse ([A-Z][a-z]+) holds the bins (\[(?:(?:\d+):(?:\d+)(?:, (?:\d+):(?:\d+))*)?\])$")]
fn holds(w: &mut World, who: String, bs: String) {
    let bs = pairs(&bs);
    w.before.insert(who.clone(), bs.clone()); // constructive: this Given builds the warehouse
    w.after.insert(who.clone(), bs.clone());
    assert!(reading::holds(w.pre(&who), &bs), "{GIVEN_FALSE}");
}

// glossary: G-stock-fits
#[given(regex = r"^the units of product (\d+) in warehouse ([A-Z][a-z]+) add up to at most the maximum$")]
fn stock_fits(w: &mut World, p: u32, who: String) {
    assert!(reading::stock_fits(w.pre(&who), p), "{GIVEN_FALSE}");
}

// glossary: G-stock-too-big
#[given(regex = r"^the units of product (\d+) in warehouse ([A-Z][a-z]+) add up to more than the maximum$")]
fn stock_too_big(w: &mut World, p: u32, who: String) {
    assert!(reading::stock_too_big(w.pre(&who), p), "{GIVEN_FALSE}");
}

// glossary: G-some-bin
#[given(regex = r"^some bin of warehouse ([A-Z][a-z]+) holds at least (\d+) units of product (\d+)$")]
fn some_bin(w: &mut World, who: String, n: u64, p: u32) {
    assert!(reading::some_bin_holds(w.pre(&who), p, n), "{GIVEN_FALSE}");
}

// glossary: G-no-bin
#[given(regex = r"^no bin of warehouse ([A-Z][a-z]+) holds at least (\d+) units of product (\d+)$")]
fn no_bin(w: &mut World, who: String, n: u64, p: u32) {
    assert!(reading::no_bin_holds(w.pre(&who), p, n), "{GIVEN_FALSE}");
}

// glossary: G-more-than-half
#[given(regex = r"^product (\d+) is in more than half of the bins of warehouse ([A-Z][a-z]+)$")]
fn more_than_half(w: &mut World, p: u32, who: String) {
    assert!(reading::more_than_half(w.pre(&who), p), "{GIVEN_FALSE}");
}

// glossary: G-none-more-than-half
#[given(regex = r"^no product is in more than half of the bins of warehouse ([A-Z][a-z]+)$")]
fn none_more_than_half(w: &mut World, who: String) {
    assert!(reading::none_more_than_half(w.pre(&who)), "{GIVEN_FALSE}");
}

// glossary: W-stock
#[when(regex = r"^the units of product (\d+) in warehouse ([A-Z][a-z]+) are counted$")]
fn stock_of(w: &mut World, p: u32, who: String) {
    let r = w.warehouse(&who).stock_of(p);
    w.clear_results();
    w.opt_units = Some(r);
}

// glossary: W-find
#[when(regex = r"^a bin of product (\d+) with at least (\d+) units is looked for in warehouse ([A-Z][a-z]+)$")]
fn find_bin(w: &mut World, p: u32, n: u64, who: String) {
    let r = w.warehouse(&who).find_bin(p, n);
    w.clear_results();
    w.opt_index = Some(r);
}

// glossary: W-restock
#[when(regex = r"^every bin of product (\d+) in warehouse ([A-Z][a-z]+) is restocked with (\d+) units$")]
fn restock(w: &mut World, p: u32, who: String, a: u64) {
    let mut x = w.warehouse(&who);
    let r = x.restock(p, a);
    w.put(who, &x);
    w.clear_results();
    w.count = Some(r);
}

// glossary: W-take
#[when(regex = r"^(\d+) units of product (\d+) are taken from warehouse ([A-Z][a-z]+)$")]
fn take(w: &mut World, n: u64, p: u32, who: String) {
    let mut x = w.warehouse(&who);
    let r = x.take(p, n);
    w.put(who, &x);
    w.clear_results();
    w.units = Some(r);
}

// glossary: W-fill
#[when(regex = r"^the orders (\[(?:(?:\d+):(?:\d+)(?:, (?:\d+):(?:\d+))*)?\]) are filled from warehouse ([A-Z][a-z]+)$")]
fn fill_orders(w: &mut World, os: String, who: String) {
    let mut x = w.warehouse(&who);
    let r = x.fill_orders(&to_orders(&pairs(&os)));
    w.put(who, &x);
    w.clear_results();
    w.count = Some(r);
}

// glossary: W-count-products
#[when(regex = r"^the different products in warehouse ([A-Z][a-z]+) are counted$")]
fn product_count(w: &mut World, who: String) {
    let r = w.warehouse(&who).product_count();
    w.clear_results();
    w.count = Some(r);
}

// glossary: W-dominant
#[when(regex = r"^the dominant product of warehouse ([A-Z][a-z]+) is looked for$")]
fn dominant_product(w: &mut World, who: String) {
    let r = w.warehouse(&who).dominant_product();
    w.clear_results();
    w.opt_product = Some(r);
}

// glossary: T-stock
#[then(regex = r"^the result is the number of units of product (\d+) in warehouse ([A-Z][a-z]+)$")]
fn t_stock(w: &mut World, p: u32, who: String) {
    let o = w.opt_units.expect("the last When counted no units");
    assert!(reading::result_is_stock(o, w.pre(&who), p), "got {o:?}");
}

// glossary: T-no-count
#[then(regex = r"^no count is given$")]
fn t_no_count(w: &mut World) {
    let o = w.opt_units.expect("the last When counted no units");
    assert!(reading::no_count(o), "got {o:?}");
}

// glossary: T-first-bin
#[then(regex = r"^the result is the first bin of warehouse ([A-Z][a-z]+) that holds at least (\d+) units of product (\d+)$")]
fn t_first_bin(w: &mut World, who: String, n: u64, p: u32) {
    let o = w.opt_index.expect("the last When looked for no bin");
    assert!(reading::first_bin_is(o, w.pre(&who), p, n), "got {o:?}");
}

// glossary: T-no-bin
#[then(regex = r"^no bin is found$")]
fn t_no_bin(w: &mut World) {
    let o = w.opt_index.expect("the last When looked for no bin");
    assert!(reading::no_bin_found(o), "got {o:?}");
}

// glossary: T-restocked
#[then(regex = r"^every bin of product (\d+) in warehouse ([A-Z][a-z]+) has gained (\d+) units, up to the maximum, and no other bin has changed$")]
fn t_restocked(w: &mut World, p: u32, who: String, a: u64) {
    assert!(reading::restocked(w.pre(&who), w.post(&who), p, a), "{:?} -> {:?}", w.pre(&who), w.post(&who));
}

// glossary: T-restock-count
#[then(regex = r"^the number of bins restocked is the number of bins of product (\d+) in warehouse ([A-Z][a-z]+)$")]
fn t_restock_count(w: &mut World, p: u32, who: String) {
    let n = w.count.expect("the last When returned no count");
    assert!(reading::count_is_bins_of(n, w.pre(&who), p), "got {n}");
}

// glossary: T-taken-min
#[then(regex = r"^the amount taken is the smaller of (\d+) and the units of product (\d+) that warehouse ([A-Z][a-z]+) held$")]
fn t_taken_min(w: &mut World, n: u64, p: u32, who: String) {
    let t = w.units.expect("the last When took nothing");
    assert!(reading::taken_is_min(t, w.pre(&who), p, n), "got {t}");
}

// glossary: T-stock-down
#[then(regex = r"^the units of product (\d+) in warehouse ([A-Z][a-z]+) have gone down by exactly the amount taken$")]
fn t_stock_down(w: &mut World, p: u32, who: String) {
    let t = w.units.expect("the last When took nothing");
    assert!(reading::stock_down_by(t, w.pre(&who), w.post(&who), p), "took {t}: {:?} -> {:?}", w.pre(&who), w.post(&who));
}

// glossary: T-taken-earliest
#[then(regex = r"^warehouse ([A-Z][a-z]+) now holds what is left after taking (\d+) units of product (\d+) from its earliest bins first$")]
fn t_taken_earliest(w: &mut World, who: String, n: u64, p: u32) {
    assert!(reading::taken_earliest_first(w.pre(&who), w.post(&who), p, n), "{:?} -> {:?}", w.pre(&who), w.post(&who));
}

// glossary: T-filled-count
#[then(regex = r"^the number of orders filled is the number of orders of (\[(?:(?:\d+):(?:\d+)(?:, (?:\d+):(?:\d+))*)?\]) that can be filled in full, in turn, from warehouse ([A-Z][a-z]+)$")]
fn t_filled_count(w: &mut World, os: String, who: String) {
    let n = w.count.expect("the last When returned no count");
    assert!(reading::filled_count(n, w.pre(&who), &pairs(&os)), "got {n}");
}

// glossary: T-filled-state
#[then(regex = r"^warehouse ([A-Z][a-z]+) now holds what is left after filling, in turn, each order of (\[(?:(?:\d+):(?:\d+)(?:, (?:\d+):(?:\d+))*)?\]) that can be filled in full$")]
fn t_filled_state(w: &mut World, who: String, os: String) {
    assert!(reading::filled_state(w.pre(&who), w.post(&who), &pairs(&os)), "{:?} -> {:?}", w.pre(&who), w.post(&who));
}

// glossary: T-filled-at-most
#[then(regex = r"^the number of orders filled is at most the number of orders in (\[(?:(?:\d+):(?:\d+)(?:, (?:\d+):(?:\d+))*)?\])$")]
fn t_filled_at_most(w: &mut World, os: String) {
    let n = w.count.expect("the last When returned no count");
    assert!(reading::filled_at_most(n, &pairs(&os)), "got {n}");
}

// glossary: T-different-products
#[then(regex = r"^the result is the number of different products in warehouse ([A-Z][a-z]+)$")]
fn t_different_products(w: &mut World, who: String) {
    let n = w.count.expect("the last When returned no count");
    assert!(reading::different_products(n, w.pre(&who)), "got {n}");
}

// glossary: T-at-most-bins
#[then(regex = r"^the result is at most the number of bins of warehouse ([A-Z][a-z]+)$")]
fn t_at_most_bins(w: &mut World, who: String) {
    let n = w.count.expect("the last When returned no count");
    assert!(reading::at_most_bins(n, w.pre(&who)), "got {n}");
}

// glossary: T-product
#[then(regex = r"^the result is product (\d+)$")]
fn t_product(w: &mut World, p: u32) {
    let o = w.opt_product.expect("the last When looked for no product");
    assert!(reading::result_is_product(o, p), "got {o:?}");
}

// glossary: T-no-dominant
#[then(regex = r"^there is no dominant product$")]
fn t_no_dominant(w: &mut World) {
    let o = w.opt_product.expect("the last When looked for no product");
    assert!(reading::no_dominant(o), "got {o:?}");
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
