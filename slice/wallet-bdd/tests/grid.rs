//! Every compiled reading (scenario or Rule) at every point of its grid of generated inputs, ON THE COMPILED
//! RUST, through the per-piece Rust readings of wallet_bdd::pieces.
//!
//! ../build/trees.json (written by `slicegen gen`) holds, per reading, its grid and its composition tree. The
//! Lean side (lean/Run/ReadingSearch.lean) prints for the same grid, in the same order, one character per
//! evaluation: per unit of the reading its scope (the Givens / "for which" / "internal"), and per claim the
//! relation between the two calls (two-run frames only) and the claim itself (`RBITS`). This program writes the
//! same string to ../out/rust_bits.tsv; the report compares the two. Agreement is the evidence that the Rust
//! reading of each piece and its Lean definition say the same, and that the Lean model behaves as the compiled
//! Rust does at those inputs; a counterexample to a Rule shows up here as a `0` at the same grid point.
use std::fmt::Write as _;

use serde_json::Value as J;
use wallet_bdd::pieces::{self as pc, Val};

fn eval_reading(rd: &J) -> String {
    let vars = rd["vars"].as_array().expect("vars");
    let names: Vec<String> = vars.iter().map(|v| v["name"].as_str().expect("name").to_string()).collect();
    let values: Vec<Vec<Val>> = vars.iter().map(|v| {
        let typ = v["type"].as_str().expect("type");
        v["values"].as_array().expect("values").iter().map(|x| pc::parse_lit(typ, x.as_str().expect("a literal"))).collect()
    }).collect();
    let mut idx = vec![0usize; vars.len()];
    let mut out = String::new();
    if values.iter().any(Vec::is_empty) {
        return out;
    }
    loop {
        let vals: Vec<(String, Val)> = names.iter().cloned().zip(idx.iter().enumerate().map(|(k, &i)| values[k][i].clone())).collect();
        out.push_str(&pc::eval_point(rd, &vals));
        // next grid point: the LAST variable runs fastest (the innermost loop of the Lean script)
        let mut k = vars.len();
        loop {
            if k == 0 {
                return out;
            }
            k -= 1;
            idx[k] += 1;
            if idx[k] < values[k].len() {
                break;
            }
            idx[k] = 0;
        }
    }
}

fn main() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let text = std::fs::read_to_string(dir.join("../build/trees.json")).expect("build/trees.json (run `python3 -m slicegen gen`)");
    let trees: J = serde_json::from_str(&text).expect("build/trees.json is JSON");
    std::panic::set_hook(Box::new(|_| {})); // a call that panics is data here ("no answer"), not noise
    let mut out = String::new();
    let (mut n, mut evals, mut failed) = (0usize, 0usize, 0usize);
    for rd in trees["readings"].as_array().expect("readings") {
        let id = rd["id"].as_str().expect("id");
        match std::panic::catch_unwind(|| eval_reading(rd)) {
            Ok(bits) => {
                evals += bits.len();
                n += 1;
                writeln!(out, "{id}\t{bits}").unwrap();
            }
            Err(e) => {
                failed += 1;
                let why = e.downcast_ref::<String>().cloned().or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string())).unwrap_or_default();
                writeln!(out, "{id}\tERROR {why}").unwrap();
            }
        }
    }
    std::fs::create_dir_all(dir.join("../out")).unwrap();
    std::fs::write(dir.join("../out/rust_bits.tsv"), out).unwrap();
    println!("grid: {n} compiled readings evaluated on the compiled Rust through the per-piece readings, {evals} evaluations; {failed} could not be evaluated");
}
