//! REPLAY OF GIVEN INPUTS ON THE COMPILED RUST, for `python3 -m clausal separate` (plan node L3).
//!
//!   cargo run --quiet --example separate_replay -- ../build/separate/<key>/replay.json
//!
//! The file holds compiled readings in the format of build/trees.json (`readings`: id -> entry) and a list of
//! `points`: {"id": reading, "values": {variable: literal}}. For each point this prints one JSON line:
//!
//!   {"id", "values", "bits",          the reading at that input through the per-piece Rust readings
//!                                     (wallet_bdd::pieces::eval_point: the string the Lean side prints as RBITS)
//!    "calls": [{"unit", "run", "ops", "inputs", "before", "answered", "answer", "accepted", "after"}]}
//!                                     what the compiled operation did at that input: one entry per unit of the
//!                                     reading and per call the reading compares (run 1, and run 2 of a two-run claim)
//!
//! Nothing here reads a sentence: the tree evaluator and `run_seq` of src/pieces.rs do the work. This file only
//! builds the actors and inputs of one point (as `pieces::side` does; its fields are private) and prints values.
use serde_json::{json, Value as J};
use wallet_bdd::pieces::{self as pc, Actors, Val};

fn show(v: &Val) -> String {
    match v {
        Val::Num(n) => n.to_string(),
        Val::Bool(b) => (if *b { "yes" } else { "no" }).to_string(),
        Val::List(l) => format!("[{}]", l.iter().map(show).collect::<Vec<_>>().join(", ")),
        Val::Opt(None) => "none".to_string(),
        Val::Opt(Some(x)) => format!("some {}", show(x)),
        Val::Transfer(f, t, a) => format!("{f}->{t}:{a}"),
        Val::Name(s) => s.clone(),
        Val::Wallet(b) => b.to_string(),
        Val::Ledger(l) => format!("[{}]", l.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", ")),
        Val::Unit => "()".to_string(),
    }
}

fn strs(x: &J) -> Vec<String> {
    x.as_array().expect("a list").iter().map(|s| s.as_str().expect("a string").to_string()).collect()
}

/// The actors and the inputs of one call of a reading at one point (the public part of what `pieces::side` builds).
fn side(run: &J, vals: &[(String, Val)]) -> (Actors, Vec<Val>) {
    let get = |name: &str| vals.iter().find(|(n, _)| n == name).map(|(_, v)| v.clone()).unwrap_or_else(|| panic!("no variable {name}"));
    let actors: Actors = run["actors"].as_array().expect("actors").iter()
        .map(|a| (a["ref"].as_str().expect("ref").to_string(), pc::build_actor(a["type"].as_str().expect("type"), &get(a["var"].as_str().expect("var")))))
        .collect();
    let inputs = run["inputs"].as_array().expect("inputs").iter().map(|i| match (i["var"].as_str(), i["lit"].as_str()) {
        (Some(var), _) => get(var),
        (None, Some(lit)) => pc::parse_lit(i["type"].as_str().expect("type"), lit),
        _ => Val::Unit,
    }).collect();
    (actors, inputs)
}

fn named(actors: &Actors) -> J {
    J::Object(actors.iter().map(|(n, v)| (n.clone(), J::String(show(v)))).collect())
}

fn replay(rd: &J, point: &J) -> J {
    let vals: Vec<(String, Val)> = rd["vars"].as_array().expect("vars").iter().map(|v| {
        let name = v["name"].as_str().expect("name");
        let lit = point["values"][name].as_str().unwrap_or_else(|| panic!("the point gives no value for {name}"));
        (name.to_string(), pc::parse_lit(v["type"].as_str().expect("type"), lit))
    }).collect();
    let bits = pc::eval_point(rd, &vals);
    let mut calls = Vec::new();
    for (u, unit) in rd["units"].as_array().expect("units").iter().enumerate() {
        let ops = strs(&unit["ops"]);
        let state = strs(&unit["state"]);
        let two = unit["claims"].as_array().expect("claims").iter().any(|c| c["runs"] == 2);
        for (k, run) in [(1, &rd["run1"]), (2, &rd["run2"])] {
            if run.is_null() || (k == 2 && !two) {
                continue;
            }
            let (actors, inputs) = side(run, &vals);
            let r = pc::run_seq(&ops, &state, &inputs, &actors);
            let last = ops.last().expect("an operation");
            calls.push(json!({
                "unit": u, "run": k, "ops": ops, "inputs": inputs.iter().map(show).collect::<Vec<_>>(),
                "before": named(&r.before),
                "answered": r.result.is_some(),
                "answer": r.result.as_ref().map(|(a, _)| show(a)),
                "accepted": r.result.as_ref().map(|(a, _)| pc::accepted(last, a)),
                "after": r.result.as_ref().map(|(_, after)| named(after)),
            }));
        }
    }
    json!({"id": point["id"], "values": point["values"], "bits": bits, "calls": calls})
}

fn main() {
    let path = std::env::args().nth(1).expect("usage: separate_replay <replay.json>");
    let data: J = serde_json::from_str(&std::fs::read_to_string(&path).expect("the replay file")).expect("the replay file is JSON");
    std::panic::set_hook(Box::new(|_| {})); // a call that panics is data here ("no answer"), not noise
    for point in data["points"].as_array().expect("points") {
        let id = point["id"].as_str().expect("id");
        let rd = &data["readings"][id];
        match std::panic::catch_unwind(|| replay(rd, point)) {
            Ok(j) => println!("{j}"),
            Err(e) => {
                let why = e.downcast_ref::<String>().cloned().or_else(|| e.downcast_ref::<&str>().map(|s| s.to_string())).unwrap_or_default();
                println!("{}", json!({"id": id, "values": point["values"], "error": why}));
            }
        }
    }
}
