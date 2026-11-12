//! Evaluates the Rust reading of every Given/Then phrase (wallet_bdd::eval) on the grid
//! that clausal wrote to ../build/phrase_grid.tsv, and writes one line per glossary
//! entry to ../out/readings.tsv:  <id> TAB <one character per grid row: 1, 0, or ? if
//! the entry or an argument was not understood>. The Lean side prints the same thing
//! (PHRASE lines of Run/Search.lean); the report compares the two.
use std::collections::BTreeMap;
use std::fmt::Write as _;

fn main() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let grid = std::fs::read_to_string(dir.join("../build/phrase_grid.tsv")).expect("build/phrase_grid.tsv (run clausal gen)");
    let mut order: Vec<String> = Vec::new();
    let mut bits: BTreeMap<String, String> = BTreeMap::new();
    for line in grid.lines().filter(|l| !l.is_empty()) {
        let mut cols = line.split('\t');
        let id = cols.next().unwrap().to_string();
        let args: Vec<&str> = cols.collect();
        if !bits.contains_key(&id) {
            order.push(id.clone());
        }
        let c = match wallet_bdd::eval(&id, &args) {
            Some(true) => '1',
            Some(false) => '0',
            None => '?',
        };
        bits.entry(id).or_default().push(c);
    }
    let mut out = String::new();
    for id in &order {
        writeln!(out, "{id}\t{}", bits[id]).unwrap();
    }
    std::fs::create_dir_all(dir.join("../out")).unwrap();
    std::fs::write(dir.join("../out/readings.tsv"), out).unwrap();
    println!("readings: {} glossary entries evaluated on {} grid rows", order.len(), grid.lines().count());
}
