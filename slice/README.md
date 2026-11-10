# slice/: Gherkin scenarios with machine-checked verdicts about real Rust

A deliberately small end-to-end probe, on two Rust crates: `wallet/` (three straight-line functions)
and `ledger/` (a `Vec` of balances, two `while` loops, a batch of transfers; see "The ledger" below). A plain-English scenario (Given / When / Then) is bound,
through an explicit glossary, to a Lean statement about the Lean model that Aeneas generates from
real Rust code. The statement is then proved, refuted with a concrete counterexample, or reported
as unbound or vacuous. The same feature file also runs as ordinary tests against the compiled Rust.

    ./run.sh            # regenerate everything, print the per-scenario report (about 25 s warm; 47 s when the slice's own Lean modules are rebuilt)
    ./run.sh --strict   # also fail while a proved scenario rests on a glossary entry nobody has signed off
    ./run.sh --no-rust  # the same without the cucumber-rs runs
    python3 mutation/run_mutants.py --jobs 8   # mutation test of the scenarios + negative controls (about 16 min)

`run.sh` deletes and recreates `out/`. Outputs: `out/report.md` (each scenario's English beside its Lean
statement and verdict, input coverage per operation, the glossary table, the trusted base) and `out/graph.json`
(the refinement graph; schema `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`).
Exit status is 0 iff every scenario got the verdict it is expected to get.

## The chain, and what kind of evidence each link has

| Link | Where | Evidence kind |
|---|---|---|
| English phrase means this Lean definition | `glossary.yaml`, `lean/Wallet/Vocab.lean`, `lean/Ledger/Vocab.lean` | human-asserted once someone signs; today NO evidence (all 42 entries unsigned) |
| The Lean definition and the Rust predicate of a phrase agree | `lean/Run/Search.lean`, `wallet-bdd/tests/readings.rs` | tested (argument grid) |
| Scenario becomes this Lean statement | `slicegen/` (untrusted Python) writes `lean/Wallet/Statements.lean` | tool-trusted; Lean type-checks it, the audit compares its constants with the glossary, the report prints it |
| Statement holds for all inputs | `lean/Wallet/Proofs/<feature>/<scenario>.lean` (hand-written, one module per scenario) | kernel-checked; axioms listed; the audit checks the theorem's type is exactly the statement |
| Loop invariants and exact results of the ledger's loops | `lean/Ledger/Lemmas/*.lean` (hand-written `@[step]` lemmas, one module per Rust function) | kernel-checked; used by the scenario proofs and by generated refutations; they appear in no statement |
| No input of an operation falls outside its proved scenarios | `lean/Run/Audit.lean` (generated `Coverage.g*`) | kernel-checked |
| Statement is false | `lean/Run/Audit.lean` (generated from a found counterexample) | kernel-checked; the counterexample is also replayed on the compiled Rust (tested) |
| Givens are satisfiable / contradictory | `lean/Run/Audit.lean` | kernel-checked |
| Lean model means what the Rust means | `translate.sh`: Charon + Aeneas write `lean/Generated/Wallet.lean`, `lean/Generated/Ledger.lean` | tool-trusted |
| std operations (`checked_add`, `-`, `Vec` and slice indexing, `Vec::clone`, the `loop` combinator) | Aeneas's hand-written Lean library models | tool-trusted |
| Examples rows | cucumber-rs on compiled Rust; interpreter on the Lean model | tested (and compared with each other) |

## Layout

    wallet/                 the Rust under test (src/lib.rs, about 45 lines) + unit tests in tests/
    ledger/                 the second Rust crate under test (src/lib.rs, 85 lines: Vec, slice, two while loops,
                            Vec::clone) + unit tests in tests/
    wallet-bdd/             cucumber-rs runner FOR BOTH CRATES: src/lib.rs (the Rust reading of each phrase, as
                            predicates), tests/bdd.rs (one step per glossary id), tests/readings.rs (predicates on a grid)
    features/wallet.feature 7 universal scenarios, 1 instance, 1 deliberately false, 1 with an unbound phrase
    features/ledger.feature 12 universal scenarios (2 of them with two Whens), 4 instance, 2 deliberately false
    features/negative.feature  contradictory Givens (vacuous); a Then that says nothing (trivial)
    glossary.yaml           phrase -> Lean definition / model function, and how arguments are wired
    slicegen/               generator and reporter: core.py (parse, bind), emit.py (Lean text),
                            pipeline.py (gen, proofs, derive), report.py (verdicts, graph, report),
                            graphlint.py (graph checks and staleness)
    lean/Generated/         Aeneas output, never edited
    lean/Bdd/               fixed support: bridge lemmas, executable Check, the audit
    lean/Wallet/Vocab.lean  hand-written glossary definitions (wallet; namespace Vocab)
    lean/Ledger/Vocab.lean  hand-written glossary definitions (ledger; namespace LVocab)
    lean/Ledger/Lemmas/     hand-written loop invariants, the pure model `runN` and the `@[step]` lemmas about the
                            ledger's functions (about 200 lines of Lean): Basic, Apply, Batch, Total, Balance, All
    lean/Wallet/Statements.lean, Checks.lean   GENERATED each run, for EVERY feature file (the library is
                            called `Wallet` for historical reasons; ledger statements are `Spec.ledger.*` in it)
    lean/Wallet/Proofs/     hand-written proofs, one module per scenario (`Proofs/ledger/*.lean` for the ledger);
                            slicegen only creates `sorry` stubs
    lean/Run/Search.lean, Audit.lean           GENERATED scripts, run once each per pipeline run
    mutation/               run_mutants.py (18 wallet + 22 ledger Rust mutants, 15 negative controls), workcopy.sh, results, logs
    schema/                 JSON Schema v2 of the graph; maths_fit.py + maths-example.graph.json; selftest.py
    review/                 evidence from the two reviews of the first build
    run.sh, translate.sh    the pipeline; Rust -> Lean translation only
    DESIGN.md, TOOLCHAIN.md design and its implementation notes; versions, pins, undo steps
    probe/                  throwaway evidence from the design stage

## Adding a scenario

1. Write it in `features/*.feature` using glossary phrases. Tag it `@id:<name>` to keep its Lean
   name stable. Universal claims are Scenario Outlines whose Thens are stated relative to the Givens.
2. `./run.sh`. An unknown phrase is reported as UNBOUND with a paste-ready glossary stub. A new
   scenario gets a `sorry` stub in its own file under `lean/Wallet/Proofs/` and shows as TESTED-ONLY, or as
   REFUTED / COUNTEREXAMPLE if the boundary search finds a failing input.
3. Replace the `sorry`. The nine wallet proofs are the same four lines:
   `intro ...; apply Bdd.okN_of_spec; unfold <model fn>; step*` (plus `simp; scalar_tac` for arithmetic).
   That recipe does NOT work for a function with a loop. The ledger proofs are 3 to 8 lines each, but only
   because each one takes what it needs from a lemma about the loop proved once in `lean/Ledger/Lemmas/`:
   `obtain ⟨⟨outputs⟩, e, facts⟩ := Bdd.ok_of_spec (<the function's .spec lemma>)`.

## The ledger (loops, a collection, multi-step scenarios)

`ledger/src/lib.rs`: `Ledger { balances: Vec<u64> }` with `balance(i)` (bounds-checked lookup), `total()` (a
`while` loop with `checked_add`), `apply(&Transfer)` (one transfer, rejected without change if invalid),
`apply_batch(&[Transfer])` (a `while` loop, stops at the first rejected transfer, returns how many were applied)
and `apply_all(&[Transfer])` (all or nothing: clones the balances and puts them back if a transfer is rejected).

What is different from the wallet, in one place each:

- **What Aeneas generates for a loop**: not a recursive function. Each `while` becomes two definitions,
  `<fn>_loop.body` (one iteration, returning `ControlFlow.cont state` or `ControlFlow.done result`) and
  `<fn>_loop`, which is `loop (fun state => body ...) initial`. `loop` is Aeneas's fixed-point combinator
  (`partial_fixpoint`), so it cannot be run by `decide`, `rfl` or `simp`, and `step*` does not step through it.
- **Proofs need a hand-written invariant.** `loop.spec_decr_nat measure invariant` is the rule; inside it,
  `unfold <fn>_loop.body; step*` works as on straight-line code. See `Ledger.apply_batch_loop.spec`
  in `lean/Ledger/Lemmas/Batch.lean`.
- **Literals** in scenarios: balances `[100, 20, 0]`, a transfer `0->1:30`, a batch `[0->1:30, 1->2:50]`
  (glossary `param_types` with `list_of:` / `fields:`).
- **Several Whens**: `When A` / `And B` / `Then ...` is one statement with one `∃ outputs, call = ok outputs ∧`
  per When, nested in order; each When runs on the state the one before left; `the result` in a Then is the
  last When's. A Then between two Whens is not supported.
- **Kernel-checked refutation through a loop** works only via a hand-proved lemma that fixes the loop's exact
  result (`runN`, a pure recursive model, in `Lemmas/Basic.lean`); see DESIGN.md section 12.

Other commands: `python3 -m slicegen steps` (cucumber regex of every glossary entry, checked
against `wallet-bdd/tests/bdd.rs`), `python3 -m slicegen review <id|all> --reviewer NAME`
(record a glossary sign-off in `glossary.signoff.json`),
`python3 -m slicegen.graphlint out/graph.json [--what-if <node-id>]` (validate the graph; show what would go stale),
`python3 schema/selftest.py` (the schema and lint must reject ten deliberately invalid graphs).
