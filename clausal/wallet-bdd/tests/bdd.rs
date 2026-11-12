//! cucumber-rs runner: the feature files, executed against the compiled Rust, with NO hand-written step.
//!
//! `clausal` compiles every step of every scenario to a tree of vocabulary pieces and writes one entry per
//! distinct step form to ../build/trees.json: a regular expression that captures every actor name, literal and
//! outline value of the step, and the tree with those captures as its leaves. This runner registers each
//! regular expression with the SAME generic step function, which looks its tree up (through the empty named
//! group `T<n>`) and evaluates it with the per-piece Rust readings of wallet_bdd::pieces:
//!
//!   Given   "<measure that is the whole actor> is <value>" builds the actor; any other Given is a condition on
//!           the state before the first When and must hold (otherwise GIVEN-FALSE: the row is outside the Givens)
//!   When    runs the operation on the compiled crate; a call that gives no answer (a panic) fails the step
//!   Then    each frame of the step, read on the state before the first When, the state now, and the last answer
//!
//! A step that clausal could not compile has no entry: cucumber reports it as undefined and skips the rest
//! of its scenario, as before. Writes Cucumber JSON to ../out/cucumber.json for the report; if
//! ../build/replay/ holds a generated feature file (counterexamples found on the Lean model), it is run as
//! well and written to ../out/cucumber-replay.json.
use std::sync::OnceLock;

use cucumber::codegen::{LocalBoxFuture, Regex};
use cucumber::step::Context;
use cucumber::{writer, World as _, WriterExt as _};
use serde_json::Value as J;
use wallet_bdd::pieces::{self as pc, Actors, Bind, Env, Run, Val};

static TREES: OnceLock<J> = OnceLock::new();

fn trees() -> &'static J {
    TREES.get().expect("build/trees.json is loaded before any step runs")
}

#[derive(Debug, Default, cucumber::World)]
struct World {
    actors: Actors,         // every actor a Given built, as it is now
    before: Option<Actors>, // ... as it was before the first When
    ops: Vec<String>,       // the Whens so far
    state: Vec<String>,     // the actors the Whens act on, in the order of the operation's roles
    inputs: Vec<Val>,
    answer: Option<Val>, // the LAST When's answer
}

const GIVEN_FALSE: &str = "GIVEN-FALSE: row is outside the Givens";

fn run_step(w: &mut World, ctx: Context) {
    let mut entry = None;
    let mut slots: Vec<(usize, String)> = Vec::new();
    for (name, text) in &ctx.matches {
        if let Some(n) = name {
            if let Some(k) = n.strip_prefix('T') {
                entry = Some(&trees()["steps"][k.parse::<usize>().expect("T<n>")]);
            } else if let Some(k) = n.strip_prefix('s') {
                slots.push((k.parse().expect("s<n>"), text.clone()));
            }
        }
    }
    let entry = entry.expect("the step regex names its tree");
    slots.sort();
    let bind = Bind { slots: slots.into_iter().map(|(_, t)| t).collect(), refs: vec![] };
    match entry["kind"].as_str().expect("kind") {
        "given" => {
            let tree = &entry["tree"];
            // constructive: "<the measure that is the whole of an actor> is <value>" builds that actor
            if tree["p"] == "is" {
                let m = &tree["a"]["m"];
                let whole = trees()["building_measures"].as_array().map(|a| a.contains(&m["p"])).unwrap_or(false);
                let who = m["a"].as_object().and_then(|o| o.values().next()).filter(|l| l["k"] == "actor");
                if let (true, Some(who)) = (whole, who) {
                    let name = bind.actor_name(who);
                    if !w.actors.iter().any(|(n, _)| *n == name) {
                        let none: Actors = vec![];
                        let v = pc::eval(&tree["a"]["t"], &Env { bind: &bind, actors: &none, ans: None, item: None, op: "" });
                        w.actors.push((name, pc::build_actor(who["type"].as_str().expect("type"), &v)));
                        return;
                    }
                }
            }
            let holds = pc::eval(tree, &Env { bind: &bind, actors: &w.actors, ans: None, item: None, op: "" }).truth();
            assert!(holds, "{GIVEN_FALSE}");
        }
        "when" => {
            let op = entry["op"].as_str().expect("op").to_string();
            let decl = &trees()["ops"][&op];
            let state: Vec<String> =
                decl["state"].as_array().expect("state").iter().map(|r| bind.actor_name(&entry["roles"][r[0].as_str().expect("role")])).collect();
            for (k, a) in state.iter().enumerate() {
                assert!(!state[..k].contains(a), "the same actor fills two roles of one operation");
            }
            let input = match decl["input"].as_array().expect("input").first() {
                Some(r) => bind.value(&entry["roles"][r[0].as_str().expect("role")]),
                None => Val::Unit,
            };
            if w.before.is_none() {
                w.before = Some(w.actors.clone());
                w.state = state.clone();
            }
            assert_eq!(w.state, state, "a sequence of Whens must be about the same actors, in the same roles");
            let run = pc::run_seq(&[op.clone()], &state, &[input.clone()], &w.actors);
            w.ops.push(op);
            w.inputs.push(input);
            match run.result {
                Some((ans, after)) => {
                    w.actors = after;
                    w.answer = Some(ans);
                }
                None => {
                    w.answer = None;
                    panic!("the call gave NO ANSWER (it panicked)");
                }
            }
        }
        "then" => {
            let ans = w.answer.clone().expect("no When gave an answer");
            let run = Run {
                ops: w.ops.clone(),
                state: w.state.clone(),
                inputs: w.inputs.clone(),
                before: w.before.clone().expect("a Then needs a When"),
                result: Some((ans, w.actors.clone())),
            };
            for claim in entry["claims"].as_array().expect("claims") {
                assert!(pc::claim_holds(claim, &bind, &run), "NOT `{}`: before {:?}, after {:?}, answer {:?}",
                        claim["frame"].as_str().unwrap_or("?"), run.before, w.actors, w.answer);
            }
        }
        k => panic!("unknown step kind {k}"),
    }
}

fn generic_step(w: &mut World, ctx: Context) -> LocalBoxFuture<'_, ()> {
    Box::pin(async move { run_step(w, ctx) })
}

async fn run_features(features: std::path::PathBuf, json_out: std::path::PathBuf) {
    let json = std::fs::File::create(json_out).unwrap();
    let mut c = World::cucumber();
    for e in trees()["steps"].as_array().expect("steps") {
        let re = Regex::new(e["regex"].as_str().expect("regex")).unwrap_or_else(|x| panic!("bad step regex {}: {x}", e["regex"]));
        c = match e["kind"].as_str().expect("kind") {
            "given" => c.given(re, generic_step),
            "when" => c.when(re, generic_step),
            _ => c.then(re, generic_step),
        };
    }
    // `run` (not `run_and_exit`): failing and undefined steps are data for the
    // report, which compares each scenario's result with its expected verdict.
    c.with_writer(
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
    let text = std::fs::read_to_string(dir.join("../build/trees.json")).expect("build/trees.json (run `python3 -m clausal gen`)");
    TREES.set(serde_json::from_str(&text).expect("build/trees.json is JSON")).ok();
    println!("generic steps: {} step forms registered from build/trees.json; hand-written steps: 0",
             trees()["steps"].as_array().map(Vec::len).unwrap_or(0));
    std::fs::create_dir_all(dir.join("../out")).unwrap();
    run_features(dir.join("../features"), dir.join("../out/cucumber.json")).await;
    let replay = dir.join("../build/replay");
    if replay.join("replay.feature").exists() {
        println!("-- counterexample replay --");
        run_features(replay, dir.join("../out/cucumber-replay.json")).await;
    }
}
