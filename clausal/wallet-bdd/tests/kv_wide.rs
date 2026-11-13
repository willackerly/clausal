//! K1, fix round: A WIDER SEARCH for the Rule lines of the project `kvparse`, ON THE COMPILED RUST ONLY.
//!
//! Why it exists. The pipeline examines a kvparse rule on a grid of 240 inputs (8 size limits by 30 messages,
//! glossary.yaml) whose messages were written by the builder of K1 with the pack's seeded bug list in hand, and whose
//! literal type (printable ASCII) cannot write a control byte or a byte above 0x7F. A reviewer's two mutants, a sibling
//! of a seeded bug each (`:` taken as a digit; a trailing newline accepted), made rules false at 3 and 4 bytes and the
//! pipeline stayed green. This search takes its inputs from the FORMAT, not from a bug list:
//!
//!   limits     0, 1, .. 8 (one above the longest record) and 4294967295
//!   messages   (a) every byte string of length 0, 1 and 2 over all 256 byte values;
//!              (b) each of the 120 records of the format (`a=D`, `b=D`, `a=D;b=D`), and everything ONE BYTE EDIT away
//!                  from one: each byte replaced by each of the 256 values, each of the 256 values inserted at each
//!                  position, each byte deleted.
//!
//! WHAT IT IS NOT. It is not part of `./run.sh` and changes no verdict: a rule it finds false stays TESTED-ONLY in
//! out/graph.json. It evaluates the Rust readings of the words (wallet-bdd/src/pieces.rs), never the Lean definitions,
//! so what it finds false is not confirmed on the Lean model. Its input set was chosen AFTER the reviewer's two mutants
//! were known, and contains both of their inputs. It sees nothing that is two or more byte edits from every record and
//! longer than two bytes (a trailing `\r\n`, for one).
//!
//!   cd wallet-bdd && cargo test --release --quiet --test kv_wide        (needs ../build/trees.json: `python3 -m clausal gen`)
//!
//! KV_WIDE_OUT=<file>   where the JSON result goes (default ../out/kv_wide.json)
//! KV_WIDE_AT=<hex,hex> messages evaluated in addition, at every limit, and reported apart (`named`)
//! Exit status 1 if a rule is false somewhere in the set (not counting `named`), or a point could not be evaluated.
use std::collections::BTreeSet;

use serde_json::{json, Value as J};
use wallet_bdd::pieces::{self as pc, Val};

const PREFIX: &str = "Rule.kvparse_rules.";

fn limits() -> Vec<u64> {
    let mut l: Vec<u64> = (0..=8).collect();
    l.push(4294967295);
    l
}

fn records() -> Vec<Vec<u8>> {
    let mut out = vec![];
    for d in b'0'..=b'9' {
        out.push(vec![b'a', b'=', d]);
        out.push(vec![b'b', b'=', d]);
        for e in b'0'..=b'9' {
            out.push(vec![b'a', b'=', d, b';', b'b', b'=', e]);
        }
    }
    out
}

/// The messages, shortest first, then in byte order.
fn messages() -> Vec<Vec<u8>> {
    let mut set: BTreeSet<(usize, Vec<u8>)> = BTreeSet::new();
    let mut put = |m: Vec<u8>| {
        set.insert((m.len(), m));
    };
    put(vec![]);
    for x in 0..=255u8 {
        put(vec![x]);
        for y in 0..=255u8 {
            put(vec![x, y]);
        }
    }
    for r in records() {
        put(r.clone());
        for i in 0..r.len() {
            let mut d = r.clone();
            d.remove(i);
            put(d);
            for x in 0..=255u8 {
                let mut s = r.clone();
                s[i] = x;
                put(s);
            }
        }
        for i in 0..=r.len() {
            for x in 0..=255u8 {
                let mut s = r.clone();
                s.insert(i, x);
                put(s);
            }
        }
    }
    set.into_iter().map(|(_, m)| m).collect()
}

/// Whether a claim of the reading is false at the point: the bit string of `eval_point` is, per unit, its scope and
/// then one character per claim (kvparse has one-run claims only; checked in `main`).
fn claim_false(rd: &J, bits: &str) -> bool {
    let b = bits.as_bytes();
    let mut k = 0;
    let mut bad = false;
    for unit in rd["units"].as_array().expect("units") {
        k += 1;
        for _ in unit["claims"].as_array().expect("claims") {
            bad |= b[k] == b'0';
            k += 1;
        }
    }
    assert_eq!(k, b.len(), "the bit string has another layout");
    bad
}

fn show(m: &[u8]) -> String {
    m.iter().map(|&c| if (0x20..0x7f).contains(&c) && c != b'\\' { (c as char).to_string() } else { format!("\\x{c:02x}") }).collect()
}

fn hex(m: &[u8]) -> String {
    m.iter().map(|c| format!("{c:02x}")).collect()
}

fn unhex(s: &str) -> Vec<u8> {
    (0..s.len() / 2).map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).expect("hex")).collect()
}

fn member(id: &str) -> String {
    format!("VI-{}", &id[PREFIX.len() + 3..])
}

fn main() {
    let dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
    let text = std::fs::read_to_string(dir.join("../build/trees.json")).expect("build/trees.json (run `python3 -m clausal gen`)");
    let trees: J = serde_json::from_str(&text).expect("build/trees.json is JSON");
    let rules: Vec<&J> = trees["readings"].as_array().expect("readings").iter()
        .filter(|rd| rd["id"].as_str().is_some_and(|i| i.starts_with(PREFIX))).collect();
    assert!(!rules.is_empty(), "build/trees.json has no reading of a kvparse rule");
    for rd in &rules {
        assert!(rd["run2"].is_null(), "a two-run reading: this search does not evaluate it");
        let names: Vec<&str> = rd["vars"].as_array().expect("vars").iter().map(|v| v["name"].as_str().expect("name")).collect();
        assert_eq!(names, ["the_parser", "the_message"], "{}: other variables than a parser and a message", rd["id"]);
    }
    std::panic::set_hook(Box::new(|_| {}));
    let point = |rd: &J, limit: u64, m: &[u8]| -> Option<bool> {
        let vals = vec![("the_parser".to_string(), Val::Num(limit as u128)),
                        ("the_message".to_string(), Val::List(m.iter().map(|&c| Val::Num(c as u128)).collect()))];
        std::panic::catch_unwind(|| pc::eval_point(rd, &vals)).ok().map(|bits| claim_false(rd, &bits))
    };
    let (limits, msgs) = (limits(), messages());
    let (mut evals, mut errors) = (0u64, 0u64);
    let mut per_rule = serde_json::Map::new();
    let mut any_false = false;
    for rd in &rules {
        let (mut n_false, mut n_msgs, mut first) = (0u64, 0u64, J::Null);
        for m in &msgs {
            let mut here = false;
            for &l in &limits {
                evals += 1;
                match point(rd, l, m) {
                    Some(true) => {
                        n_false += 1;
                        here = true;
                        if first.is_null() {
                            first = json!({"limit": l, "message": show(m), "hex": hex(m)});
                        }
                    }
                    Some(false) => {}
                    None => errors += 1,
                }
            }
            n_msgs += here as u64;
        }
        any_false |= n_false > 0;
        per_rule.insert(member(rd["id"].as_str().unwrap()), json!({"false_points": n_false, "false_messages": n_msgs, "first": first}));
    }
    // messages named on the command line: reported apart, never counted above
    let mut named = serde_json::Map::new();
    for h in std::env::var("KV_WIDE_AT").unwrap_or_default().split(',').filter(|h| !h.is_empty()) {
        let m = unhex(h);
        let mut f = serde_json::Map::new();
        for rd in &rules {
            if let Some(&l) = limits.iter().find(|&&l| point(rd, l, &m) == Some(true)) {
                f.insert(member(rd["id"].as_str().unwrap()), json!(l));
            }
        }
        named.insert(show(&m), json!({"hex": h, "in_the_set": msgs.contains(&m), "false_at_limit": f}));
    }
    let res = json!({
        "what": "kvparse rules on the compiled Rust at inputs taken from the format (wallet-bdd/tests/kv_wide.rs); not a pipeline verdict; Rust readings only",
        "limits": limits, "messages": msgs.len(), "rules": rules.len(), "evaluations": evals, "could_not_be_evaluated": errors,
        "false": per_rule, "named": named,
    });
    let out = std::env::var("KV_WIDE_OUT").map(std::path::PathBuf::from).unwrap_or_else(|_| dir.join("../out/kv_wide.json"));
    std::fs::write(&out, serde_json::to_string_pretty(&res).unwrap() + "\n").expect("the result file");
    let bad: Vec<String> = res["false"].as_object().unwrap().iter().filter(|(_, v)| v["false_points"] != 0)
        .map(|(k, v)| format!("{k} at limit {}, \"{}\"", v["first"]["limit"], v["first"]["message"].as_str().unwrap())).collect();
    println!("kv_wide: {} rules x {} limits x {} messages = {evals} evaluations on the compiled Rust; {errors} could not be evaluated; FALSE: {}",
             rules.len(), limits.len(), msgs.len(), if bad.is_empty() { "no rule".to_string() } else { bad.join("; ") });
    std::process::exit((any_false || errors > 0) as i32);
}
