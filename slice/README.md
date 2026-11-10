# slice/: Gherkin scenarios with machine-checked verdicts about real Rust

A deliberately small end-to-end probe, on two Rust crates: `wallet/` (three straight-line functions)
and `ledger/` (a `Vec` of balances, two `while` loops, a batch of transfers; see "The ledger" below). A plain-English scenario (Given / When / Then) is bound,
through an explicit glossary, to a Lean statement about the Lean model that Aeneas generates from
real Rust code. The statement is then proved, refuted with a concrete counterexample, or reported
as unbound or vacuous. The same feature file also runs as ordinary tests against the compiled Rust.

    ./run.sh            # regenerate everything, print the per-scenario and per-Rule report. Warm, on a lightly loaded
                        # machine: 33 s measured before the suite adequacy note was added; the note adds two Lean
                        # processes (21 s and 12 s measured alone) that run beside the other steps. Not re-measured
                        # as a whole on an idle machine; longer when the slice's own Lean modules are rebuilt
    ./run.sh --strict   # also fail while a proved scenario rests on a glossary entry nobody has signed off
    ./run.sh --no-rust  # the same without the cucumber-rs runs
    ./run.sh --no-adequacy   # the same without the suite adequacy note (informational; every verdict is the same)
    python3 -m slicegen rules [graph.json]     # the per-Rule blocks again, from a stored graph and nothing else
    python3 mutation/run_mutants.py --jobs 8   # mutation test of the scenarios + negative controls (45 Rust mutants, 20 controls;
                                               # see mutation/results.md for the last run)
    ./lakebuild.sh <Lean module>               # `lake build` of one module, with the attempt logged in effort/attempts.tsv
    python3 effort/count.py                    # hand-written Lean per crate against Rust code lines

`run.sh` deletes and recreates `out/`. Outputs: `out/report.md` (one block per Gherkin `Rule:` with its verdict,
example rows, suite adequacy note and what it rests on; beneath it each scenario's English beside its Lean
statement and verdict; input coverage per operation, the glossary table, the trusted base) and `out/graph.json`
(the refinement graph; schema `schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`).
Exit status is 0 iff every scenario got the verdict it is expected to get. The suite adequacy note never
changes it.

## Rules, suites and the adequacy note

Scenarios sit under Gherkin `Rule:` lines (`features/wallet.feature`, `features/ledger.feature`). The same files
run as ordinary cucumber tests: cucumber-rs 0.23.0 executes a Scenario Outline with Examples under a `Rule:`
(checked by running it; `review/rule-probe/`).

- **The rule line is a plain-English claim and is not compiled.** It and the text under it are carried into the
  report and the graph as written. What is proved is each scenario beneath it; together they are the rule's suite.
  Nothing checks that the rule line says what its scenarios say.
- **A tag on a Rule (or on the Feature) applies to every scenario beneath it**; `@id:` is not inherited. A
  Background under a Rule runs after the Feature's.
- **Suite adequacy note (informational, never a failure).** For each operation, trivial implementations are
  generated as Lean models of exactly the type of the Aeneas model: *reject-all*, *no-op* (does nothing but report
  success), *identity* (answers as the code does, never changes the state), *constant*. Each proved universal
  scenario is stated again with the trivial model in place of the call and searched for a failing input on the
  counterexample grid; kernel confirmation is attempted both ways. The report prints, per operation and per Rule,
  `suite rules out: ...; still allows: ...`, and says in neutral terms where one rule or one scenario alone would
  hold of a trivial implementation that the wider suite rules out (the normal case). Configuration: the `trivial:`
  section of `glossary.yaml`. Scenarios tagged `@control` are left out. Code: `slicegen/adequacy.py`.
- **The per-Rule block is generated from `out/graph.json`** (`slicegen/rules.py`): rule text, verdict, examples
  passing, suite note, and a "rests on" block with meaning (vocabulary entries used, how many signed), proof
  (theorems, axioms), translation (tool, version, example rows cross-checked) and compilation. A compiled reading
  of the rule line is not echoed back yet; the generated Lean statement of each scenario is printed as before.

## The chain, and what kind of evidence each link has

| Link | Where | Evidence kind |
|---|---|---|
| English phrase means this Lean definition | `glossary.yaml`, `lean/Wallet/Vocab.lean`, `lean/Ledger/Vocab.lean` | human-asserted once someone signs; today NO evidence (all 44 entries unsigned) |
| The Lean definition and the Rust predicate of a phrase agree | `lean/Run/Search.lean`, `wallet-bdd/tests/readings.rs` | tested (argument grid) |
| Scenario becomes this Lean statement | `slicegen/` (untrusted Python) writes `lean/Wallet/Statements.lean` | tool-trusted; Lean type-checks it, the audit compares its constants with the glossary, the report prints it |
| Statement holds for all inputs | `lean/Wallet/Proofs/<feature>/<scenario>.lean` (hand-written, one module per scenario) | kernel-checked; axioms listed; the audit checks the theorem's type is exactly the statement |
| Loop invariants and exact results of the ledger's loops | `lean/Ledger/Lemmas/*.lean` (hand-written `@[step]` lemmas, one module per Rust function) | kernel-checked; used by the scenario proofs and by generated refutations; they appear in no statement |
| No input of an operation falls outside its proved scenarios | `lean/Run/Audit.lean` (generated `Coverage.g*`) | kernel-checked |
| Statement is false | `lean/Run/Audit.lean` (generated from a found counterexample) | kernel-checked; the counterexample is also replayed on the compiled Rust (tested) |
| Givens are satisfiable / contradictory | `lean/Run/Audit.lean` | kernel-checked |
| A suite rules out / still allows a trivial implementation (informational) | `lean/Run/Adequacy.lean` (search), `lean/Run/AdequacyAudit.lean` (kernel attempts) | tested; kernel-checked where the generated script goes through |
| Lean model means what the Rust means | `translate.sh`: Charon + Aeneas write `lean/Generated/Wallet.lean`, `lean/Generated/Ledger.lean` | tool-trusted |
| std operations (`checked_add`, `-`, `Vec` and slice indexing, `Vec::clone`, the `loop` combinator) | Aeneas's hand-written Lean library models | tool-trusted |
| Examples rows | cucumber-rs on compiled Rust; interpreter on the Lean model | tested (and compared with each other) |

## Layout

    wallet/                 the Rust under test (src/lib.rs, about 45 lines) + unit tests in tests/
    ledger/                 the second Rust crate under test (src/lib.rs, 85 lines: Vec, slice, two while loops,
                            Vec::clone) + unit tests in tests/
    wallet-bdd/             cucumber-rs runner FOR BOTH CRATES: src/lib.rs (the Rust reading of each phrase, as
                            predicates), tests/bdd.rs (one step per glossary id), tests/readings.rs (predicates on a grid)
    features/wallet.feature 5 Rules: 7 universal scenarios, 1 instance, 1 deliberately false, 1 with an unbound phrase
    features/ledger.feature 9 Rules: 16 universal scenarios (3 of them with two Whens), 5 instance, 2 deliberately false
    features/negative.feature  no Rule, tagged @control: contradictory Givens (vacuous); a Then that says nothing (trivial)
    glossary.yaml           phrase -> Lean definition / model function, and how arguments are wired; `trivial:` says
                            which result values count as a rejection or a success (suite adequacy note only)
    slicegen/               generator and reporter: core.py (parse incl. `Rule:`, bind), emit.py (Lean text),
                            pipeline.py (gen, proofs, derive, adequacy), report.py (verdicts, graph, report),
                            adequacy.py (trivial models, the suite adequacy note), rules.py (per-Rule blocks, from
                            the graph only), graphlint.py (graph checks and staleness)
    lean/Generated/         Aeneas output, never edited
    lean/Bdd/               fixed support: bridge lemmas, executable Check, the audit
    lean/Wallet/Vocab.lean  hand-written glossary definitions (wallet; namespace Vocab)
    lean/Ledger/Vocab.lean  hand-written glossary definitions (ledger; namespace LVocab)
    lean/Ledger/Lemmas/     hand-written loop invariants, the pure model `runN` and the `@[step]` lemmas about the
                            ledger's functions (227 code lines of Lean, `python3 effort/count.py`): Basic, Apply, Batch, Total, Balance, All
    lean/Wallet/Statements.lean, Checks.lean   GENERATED each run, for EVERY feature file (the library is
                            called `Wallet` for historical reasons; ledger statements are `Spec.ledger.*` in it)
    lean/Wallet/Proofs/     hand-written proofs, one module per scenario (`Proofs/ledger/*.lean` for the ledger);
                            slicegen only creates `sorry` stubs
    lean/Run/Search.lean, Audit.lean           GENERATED scripts, run once each per pipeline run
    lean/Run/Adequacy.lean, AdequacyAudit.lean GENERATED scripts for the suite adequacy note; imported by nothing
    mutation/               run_mutants.py (18 wallet + 27 ledger Rust mutants, 20 negative controls), workcopy.sh, results, logs
    effort/                 attempts.tsv (every `./lakebuild.sh` call: time, target, ok/FAILED, seconds), count.py
    schema/                 JSON Schema v2 of the graph; maths_fit.py + maths-example.graph.json; selftest.py
    review/                 evidence from the reviews: spec/, schema/ (first build), loops/ (adversarial review of the ledger),
                            loops-fix/ (what was rerun when that review's findings were fixed)
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
- **What the ledger scenarios do not say.** The universal scenarios about the two loops are: the total is
  conserved; the count is at most the batch length; a batch stops only at a transfer that is invalid on the ledger
  it left; a rejected whole batch changes nothing; and what happens when the first transfer is invalid. They do
  not determine which ledger a batch leaves. The lemma library proves that exactly, but a lemma is not a scenario:
  the report lists, per operation, what the proved scenarios say about each output, and the mutation run reports
  "a scenario is shown false" separately from "the run fails only because a proof stopped compiling". See
  DESIGN.md 12.8.

Other commands: `python3 -m slicegen steps` (cucumber regex of every glossary entry, checked
against `wallet-bdd/tests/bdd.rs`), `python3 -m slicegen review <id|all> --reviewer NAME`
(record a glossary sign-off in `glossary.signoff.json`),
`python3 -m slicegen.graphlint out/graph.json [--what-if <node-id>]` (validate the graph; show what would go stale),
`python3 schema/selftest.py` (the schema and lint must reject ten deliberately invalid graphs).
