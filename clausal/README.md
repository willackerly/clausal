# clausal/: Gherkin rules and scenarios with machine-checked verdicts about real Rust

A deliberately small end-to-end probe, on two Rust crates: `wallet/` (three straight-line functions)
and `ledger/` (a `Vec` of balances, two `while` loops, a batch of transfers; see "The ledger" below).

A plain-English `Rule:` line, and each scenario beneath it (Given / When / Then), is **assembled from typed
pieces of a Clausebook** (`clausebook.yaml`: domain words, modifiers, frames), compiled to ONE Lean statement
about the Lean model that Aeneas generates from the real Rust, and **echoed back in fixed English** (applies
to / assuming / then / defaults applied) so the author can check how it was read. The statement is then
proved, refuted with a concrete counterexample, or reported as unbound, ill-typed or vacuous. The same
feature files also run as ordinary tests against the compiled Rust. See "The composable Clausebook" below;
design in `DESIGN.md` section 14.

    ./run.sh            # regenerate everything, print the per-scenario and per-Rule report. With the generated Kani
                        # harnesses (269 of them, 30 s each at most, 6 at a time): 10 min 39 s and 10 min 44 s measured
                        # on a shared machine, of which the bounded checks are about 7.5 min. With --quick: 2 min 23 s.
                        # Neither is a timing on an idle machine; longer when the slice's own Lean modules are rebuilt
    ./run.sh --strict   # also fail while a proved scenario rests on a glossary entry nobody has signed off
    ./run.sh --quick    # the same without the bounded checks (Kani); the generated property tests still run. For iteration
    ./run.sh --kani-timeout=60 --kani-jobs=6   # seconds per Kani harness (default 30) and harnesses at a time (default 6)
    ./run.sh --no-rust  # the same without the cucumber-rs runs (and without the generated property tests and bounded checks)
    ./run.sh --no-adequacy   # the same without the suite adequacy note (informational; every verdict is the same)
    ./run.sh --no-heldout    # the same without the informational step for heldout/*.feature (there is none in the tree now:
                             # the held-out sentences moved into features/ledger_rules.feature)
    python3 -m clausal compile <file.feature>  # compile sentences that are not in features/ from the Clausebook alone
    python3 -m clausal steps                  # the step forms the ONE generic cucumber step is registered for (build/trees.json)
    python3 -m clausal review <piece-id|all> --reviewer NAME   # sign off a Clausebook piece (void when its entry or Lean text changes)
    python3 -m clausal rules [graph.json]     # the per-Rule blocks again, from a stored graph and nothing else
    python3 -m clausal evidence [--quick] [--only id,id]   # the generated property tests and Kani harnesses alone -> out/evidence.json
    python3 mutation/run_mutants.py --jobs 8   # mutation test of the scenarios + negative controls (45 Rust mutants, 38 controls;
                                               # see mutation/results.md for the last run; every run there uses --quick except
                                               # control c36, which needs the bounded check)
    ./lakebuild.sh <Lean module>               # `lake build` of one module, with the attempt logged in effort/attempts.tsv
    python3 effort/count.py                    # hand-written Lean per crate against Rust code lines

`run.sh` deletes and recreates `out/`. Outputs: `out/report.md` (one block per Gherkin `Rule:` with the rule
line, its compiled reading echoed in English, the verdict of the rule statement, its scenarios, example rows,
suite adequacy note and what it rests on; beneath it each scenario with its own echo and verdict, the Lean
folded underneath; then input coverage per operation, the frame library, the Clausebook table, the regression
table NEW ↔ OLD, the new sentences, the trusted base) and `out/graph.json` (the refinement graph; schema
`schema/refinement-graph.v2.schema.json`, described in `../docs/SCHEMA.md`).
Exit status is 0 iff every scenario AND every rule statement got the verdict it is expected to get. The suite
adequacy note and the new sentences never change it.

## The composable Clausebook (plan nodes V2, V3)

- **Three kinds of piece** (`clausebook.yaml`), each with a type: 40 *domain words* (8 operations bound to the
  Aeneas model, measures, conditions, collections, answer words, relations between two calls, reference functions:
  `lean/Wallet/Pieces.lean`, `lean/Ledger/Pieces.lean`), 28 *modifiers* (`the total of`, `every … of`, `some … of`,
  `is not more than`, `successful`, `for which`, …) and 25 *frames* with a surface form (`never changes`, `is accepted
  exactly when`, `is decreased by`, `never loses acceptance when`, `agrees with`, …), plus 3 idioms: 96 entries a person
  would sign. Modifiers and frames are shared: `lean/Frames/` imports nothing but Lean core.
- **Frames** are statement shapes about one call of an abstract operation, with typed holes; the fail-closed
  defaults (every input, rejected calls included, and the call must answer) are written once, in
  `Frames.Op.HoldsAt`. Each frame has a Lean definition, a fixed English paraphrase and an
  executable second reading (`lean/Frames/Check.lean`; same author, different style); the two are compared on
  generated inputs every run. On the fixtures that comparison has almost no power (a claim is rarely false and
  no call is silent), so every frame is also compared on a toy operation that gives no answer at one input and
  rejects another (`lean/Run/FrameToyTests.lean`).
- **A sentence that does not compose is refused**, with file:line: UNBOUND (no composition), ILL-TYPED (one
  exists only if types are ignored; the two types are named), AMBIGUOUS (several). Never a guess.
- **The `Rule:` line is compiled** to one statement that covers every input. The outline scenarios beneath it
  are its parts: a generated, kernel-checked theorem derives the rule statement from them
  (`<rule>.from_scenarios`); where that script fails, a hand-written proof of the rule statement may stand in
  (`lean/Wallet/RuleProofs/`). A false rule statement is refuted in the kernel at the input the search found.
- **Echo-back**: every reading is printed in slot-structured English with every default applied, first; the
  Lean is underneath.
- **The old whole-phrase glossary is still here** (`glossary.yaml`, `lean/*/Vocab.lean`), as the *flat statement*
  each hand-written proof of the 34 OLDER scenarios is about. It is no longer the key of the cucumber steps, and a
  new sentence needs no entry in it. It is no longer the link from English
  to Lean: for every scenario `<id>.reading ↔ <id>.stmt` is kernel-checked (`lean/Run/Links.lean`), and a
  reading without that equivalence gets the verdict UNLINKED.
- **A NEW sentence goes all the way** (added 2026-11-11; `DESIGN.md` section 15, `features/ledger_rules.feature`). The Rust
  side has ONE reading per piece (`wallet-bdd/src/pieces.rs`) and ONE generic cucumber step that evaluates the composition
  tree of a step (`build/trees.json`), so a sentence that compiles also runs on the compiled Rust; a flat proof obligation
  is generated from the pieces (`lean/Wallet/Obligations.lean`) with a `sorry` stub; the verdict is PROVED-FOR-ALL when a
  proof of the obligation is supplied, TESTED-ONLY while it is not, REFUTED when the search finds a counterexample and the
  kernel confirms it. Every compiled reading is also evaluated on generated inputs on the compiled Rust and compared with
  the Lean side.
- **Two-run and reference frames have sentence forms**: monotone, agrees with a reference, same answer under a change
  of input (also conditioned on the first answer), containment between a collection of the input and one of the answer,
  and "some X of XS" as a condition. They need domain words of two kinds, `variation` and `reference`.

## Layered evidence from one compiled rule (plan node E1)

From the composition tree that gives a sentence its Lean statement and its echo, `clausal gen` also writes a
**property test** and a **bounded-model-checking harness** for it (`evidence/`, generated by `clausal/evgen.py`).
No test code is written per rule.

- Both assert ONE generated predicate (`evidence/src/checks.rs`): the reading at one point, as straight-line Rust
  over one typed reading per Clausebook piece (`evidence/src/typed.rs`, written once).
- **Property test** (proptest, shrinking, 10,000 cases in scope, one seed): generators derived from the types of the
  rule's variables and from its Givens, weighted to edges. At every case the generated predicate is compared with
  the tree evaluator of `wallet-bdd/src/pieces.rs`; a difference is READING MISMATCH and fails the run.
- **Bounded check** (Kani): every integer symbolic, collections bounded by ONE ladder of sizes, the same for every
  rule: (accounts, transfers) = (2, 1), (2, 2), (4, 1), (2, 3), (6, 4). Each rung is reported as verified, failed, or
  no answer in the time allowed.
- **Feed-back**: every input either of them finds false is evaluated on the Lean model through the reading. If it
  fails there too it becomes the reading's counterexample and gets the usual kernel-checked refutation, with its
  source named. If the model does not fail where the compiled Rust did, the verdict is flagged MODEL MISMATCH (a
  finding about the translation link) and the run fails.
- **The per-Rule block has an evidence ladder**: example rows, property test, bounded check, proof, each with what it
  rests on, then STRONGEST HELD. A rule may hold property-test and bounded evidence only; it is then TESTED-ONLY.
  Nothing is called proved without a kernel-checked theorem.
- **A false rule can pass every layer** when its only failing inputs lie outside the grid, the sampled cases and the
  ladder (a reviewer's probe needs a batch of five transfers; no layer found it). Such a rule is TESTED-ONLY and is
  never called proved, but it is not flagged either. `FINDINGS.md`, E1 addendum.

Measured against the K2 trade map on the same mutants: `compare/e1/E1_TRADES.md`. Design: `DESIGN.md` section 16.

## Rules, suites and the adequacy note

Scenarios sit under Gherkin `Rule:` lines (`features/wallet.feature`, `features/ledger.feature`). The same files
run as ordinary cucumber tests: cucumber-rs 0.23.0 executes a Scenario Outline with Examples under a `Rule:`
(checked by running it; `review/rule-probe/`).

- **The rule line is compiled** (see above) and has a verdict of its own; the free text under it is carried into
  the report and the graph as written. The scenarios beneath it are its suite, its tested instances, and, where
  they are outlines meant to hold, the parts its statement is proved from.
- **A tag on a Rule (or on the Feature) applies to every scenario beneath it**; `@id:` is not inherited. A
  Background under a Rule runs after the Feature's.
- **Suite adequacy note (informational, never a failure).** For each operation, trivial implementations are
  generated as Lean models of exactly the type of the Aeneas model: *reject-all*, *no-op* (does nothing but report
  success), *identity* (answers as the code does, never changes the state), *constant*. Each proved universal
  scenario is stated again with the trivial model in place of the call and searched for a failing input on the
  counterexample grid; kernel confirmation is attempted both ways. The report prints, per operation and per Rule,
  `suite rules out: ...; still allows: ...`, and says in neutral terms where one rule or one scenario alone would
  hold of a trivial implementation that the wider suite rules out (the normal case). Configuration: the `trivial:`
  section of `glossary.yaml`. Scenarios tagged `@control` are left out. Code: `clausal/adequacy.py`.
- **The per-Rule block is generated from `out/graph.json`** (`clausal/rules.py`): rule text, verdict, examples
  passing, suite note, and a "rests on" block with meaning (Clausebook entries used, how many signed), proof
  (theorems, axioms), translation (tool, version, example rows cross-checked) and compilation. The block
  now starts with the rule's compiled reading (the echo) and the verdict of the rule statement, and its
  meaning line counts Clausebook pieces. Since 2026-11-11 it leads with the form of the root README's target
  (Rule, Reading as one sentence, Verdict, Examples, Generated, Suite, Rests on with each piece's sign-off state,
  proof, translation, compilation) and keeps the slot-by-slot echo and the evidence lines under `Detail`. The root
  README's own rule is `@id:readme_internal_transfers` in `features/ledger_rules.feature`.

## The chain, and what kind of evidence each link has

| Link | Where | Evidence kind |
|---|---|---|
| English piece means this Lean definition | `clausebook.yaml`, `lean/Frames/`, `lean/Wallet/Pieces.lean`, `lean/Ledger/Pieces.lean` | human-asserted once someone signs; today NO evidence (all 96 entries unsigned) |
| A sentence is this composition of pieces | `clausal/vocab.py` (untrusted) writes `lean/Wallet/Readings.lean` | tool-trusted; Lean type-checks it; echoed in English for the author |
| A frame's definition and its executable reading agree | `lean/Run/ReadingSearch.lean`, `lean/Run/FrameTests.lean`, `lean/Run/FrameToyTests.lean` | tested (generated inputs; the report says per frame whether a false claim and a silent call were among them) |
| The compiled reading says what the flat statement says | `lean/Run/Links.lean` (generated `<id>.reading_iff`), `lean/Bdd/AuditLinks.lean` | kernel-checked; the audit checks the theorem's type is exactly `reading ↔ stmt`, that its proof uses no proof of either side, and that the reading mentions only what its pieces name |
| A rule statement follows from its scenarios | `lean/Run/Links.lean` (generated `<rule>.from_scenarios`), or `lean/Wallet/RuleProofs/` (hand-written) | kernel-checked |
| Old phrase means this Lean definition (flat statements, Rust steps) | `glossary.yaml`, `lean/Wallet/Vocab.lean`, `lean/Ledger/Vocab.lean` | no longer on the path from English to a verdict; all 44 entries unsigned |
| The Lean definition and the Rust predicate of an OLD phrase agree | `lean/Run/Search.lean`, `wallet-bdd/tests/readings.rs` | tested (argument grid) |
| The Lean definition and the Rust reading of each Clausebook PIECE agree, and the model behaves as the compiled Rust | `lean/Run/ReadingSearch.lean` (`RBITS`), `wallet-bdd/src/pieces.rs`, `wallet-bdd/tests/grid.rs` | tested: every compiled reading at every point of its grid of generated inputs, on both sides |
| A new sentence's flat proof obligation says what its reading says | `lean/Wallet/Obligations.lean` (generated), `lean/Run/Links.lean` (generated `<id>.reading_iff_obligation`) | kernel-checked; the audit checks the type and that the proof uses no proof of either side |
| A new sentence's obligation holds | `lean/Wallet/Proofs/<feature>/<scenario>.lean`, `lean/Wallet/RuleProofs/<feature>/<rule>.lean` (supplied by hand or by an agent; a `sorry` stub until then) | kernel-checked; carried to the reading as `<id>.reading_holds` / `<id>.proved` |
| Scenario becomes this Lean statement | `clausal/` (untrusted Python) writes `lean/Wallet/Statements.lean` | tool-trusted; Lean type-checks it, the audit compares its constants with the glossary, the report prints it |
| Statement holds for all inputs | `lean/Wallet/Proofs/<feature>/<scenario>.lean` (hand-written, one module per scenario) | kernel-checked; axioms listed; the audit checks the theorem's type is exactly the statement |
| Loop invariants and exact results of the ledger's loops | `lean/Ledger/Lemmas/*.lean` (hand-written `@[step]` lemmas, one module per Rust function) | kernel-checked; used by the scenario proofs and by generated refutations; they appear in no statement |
| No input of an operation falls outside its proved scenarios | `lean/Run/Audit.lean` (generated `Coverage.g*`) | kernel-checked |
| Statement is false | `lean/Run/Audit.lean` (generated from a found counterexample) | kernel-checked; the counterexample is also replayed on the compiled Rust (tested) |
| Givens are satisfiable / contradictory | `lean/Run/Audit.lean` | kernel-checked |
| A suite rules out / still allows a trivial implementation (informational) | `lean/Run/Adequacy.lean` (search), `lean/Run/AdequacyAudit.lean` (kernel attempts) | tested; kernel-checked where the generated script goes through |
| A rule holds on generated inputs of the compiled Rust | `evidence/` (generated property test; proptest) | tested, sampled: 10,000 cases in the rule's scope, edge-weighted; says nothing about inputs it did not draw |
| A rule holds for every input up to a size, on the compiled Rust | `evidence/kani/` (generated harness; Kani, CBMC) | tool-checked, bounded: the sizes of the ladder at which Kani answered; nothing beyond them |
| The generated typed predicate says what the composition tree says | `evidence/src/main.rs` against `wallet-bdd/src/pieces.rs` (`eval_point`) | tested at every generated case; one author on both sides |
| An input found false on the compiled Rust is false on the model too | `lean/Run/Witness.lean` (generated), `clausal/evidence.py` | evaluated on the model; then kernel-checked as a refutation, or reported as MODEL MISMATCH |
| Lean model means what the Rust means | `translate.sh`: Charon + Aeneas write `lean/Generated/Wallet.lean`, `lean/Generated/Ledger.lean` | tool-trusted |
| std operations (`checked_add`, `-`, `Vec` and slice indexing, `Vec::clone`, the `loop` combinator) | Aeneas's hand-written Lean library models | tool-trusted |
| Examples rows | cucumber-rs on compiled Rust; interpreter on the Lean model | tested (and compared with each other) |

## Layout

    wallet/                 the Rust under test (src/lib.rs, about 45 lines) + unit tests in tests/
    ledger/                 the second Rust crate under test (src/lib.rs, 85 lines: Vec, slice, two while loops,
                            Vec::clone) + unit tests in tests/
    wallet-bdd/             the Rust side FOR BOTH CRATES: src/pieces.rs (ONE Rust reading per Clausebook piece and the
                            evaluator of composition trees), tests/bdd.rs (cucumber-rs with ONE generic step, no step per
                            sentence), tests/grid.rs (every compiled reading on its grid, on the compiled Rust);
                            src/lib.rs + tests/readings.rs (the older whole-phrase predicates, compared on a grid only)
    evidence/               GENERATED EVIDENCE (plan node E1). src/typed.rs: one typed Rust reading per Clausebook piece
                            (written once). src/main.rs: the generic property-test runner (written once). src/checks.rs,
                            src/table.rs, kani/src/harnesses.rs: GENERATED each run from build/trees.json: the reading of every
                            sentence at one point, what the generators need, one Kani harness per reading and rung
    features/ledger_rules.feature  NEW SENTENCES: 32 Rules and 4 scenarios with no entry in the old glossary (the root README's
                            rule, the five formerly held-out rules, the two-run and reference frames each true once and false
                            once, the two candidate rules of compare/TRADES.md, a false rule the grid search does not find,
                            false rules about successful / rejected calls and a sequence, the remaining frames)
    features/wallet.feature 5 Rules: 7 universal scenarios, 1 instance, 1 deliberately false, 1 with an unbound phrase
    features/ledger.feature 9 Rules: 16 universal scenarios (3 of them with two Whens), 5 instance, 2 deliberately false
    features/negative.feature  no Rule, tagged @control: contradictory Givens (vacuous); a Then that says nothing (trivial)
    clausebook.yaml         THE CLAUSEBOOK: operations, pieces (domain / modifier / frame), idioms, the defaults
    lean/Wallet/Obligations.lean   GENERATED each run: the flat proof obligation of every new scenario and every Rule line
    build/trees.json        GENERATED each run: the composition trees the Rust side evaluates (step forms; readings with grids)
    lean/Frames/            the shared frame library: Core (operation, typed holes, modifiers), Frames (26 definitions:
                            the 14 catalogue frames and frames 15, 16), Check (the executable readings), Lemmas (glue facts)
    lean/Wallet/Pieces.lean, lean/Ledger/Pieces.lean   domain words of the two crates (namespaces W, L)
    lean/Wallet/Readings.lean   GENERATED each run: the compiled reading of every scenario and Rule line
    lean/Wallet/RuleProofs/ hand-written proofs of rule statements whose generated glue does not go through
    lean/Run/ReadingSearch.lean, Links.lean, NewReadings.lean   GENERATED scripts: readings on generated inputs (two
                            ways); NEW ↔ OLD equivalences, non-vacuity, rule glue and refutations; the held-out sentences
    lean/Run/FrameTests.lean    hand-written: the frames with no surface form, definition against executable reading
    lean/Run/FrameToyTests.lean hand-written, core Lean only: EVERY frame on a toy operation with a silent and a rejected input
    lean/Bdd/Ops.lean, Bridge.lean, AuditLinks.lean   model function -> Frames.Op; bridge facts for glue proofs; link audit
    glossary.yaml           THE OLD whole-phrase glossary: phrase -> Lean definition / model function, and how arguments are wired; `trivial:` says
                            which result values count as a rejection or a success (suite adequacy note only)
    clausal/               generator and reporter: vocab.py (the Clausebook: parse, type, compile, echo), links.py (glue
                            proofs), rsearch.py (readings on generated inputs), vreport.py (echo, rule verdicts, piece
                            sign-off, report sections), newrules.py (`compile`); and, for the flat statements:
                            core.py (parse incl. `Rule:`, bind), emit.py (Lean text),
                            pipeline.py (gen, proofs, derive, adequacy), report.py (verdicts, graph, report),
                            adequacy.py (trivial models, the suite adequacy note), rules.py (per-Rule blocks, from
                            the graph only), graphlint.py (graph checks and staleness); evgen.py (generates the property
                            tests and Kani harnesses from the trees), evidence.py (runs them, feeds falsifying inputs back)
    lean/Generated/         Aeneas output, never edited
    lean/Bdd/               fixed support: bridge lemmas, executable Check, the audit
    lean/Wallet/Vocab.lean  hand-written glossary definitions (wallet; namespace Vocab)
    lean/Ledger/Vocab.lean  hand-written glossary definitions (ledger; namespace LVocab)
    lean/Ledger/Lemmas/     hand-written loop invariants, the pure model `runN` and the `@[step]` lemmas about the
                            ledger's functions (227 code lines of Lean, `python3 effort/count.py`): Basic, Apply, Batch, Total, Balance, All
    lean/Wallet/Statements.lean, Checks.lean   GENERATED each run, for EVERY feature file (the library is
                            called `Wallet` for historical reasons; ledger statements are `Spec.ledger.*` in it)
    lean/Wallet/Proofs/     hand-written proofs, one module per scenario (`Proofs/ledger/*.lean` for the ledger);
                            clausal only creates `sorry` stubs
    lean/Run/Search.lean, Audit.lean           GENERATED scripts, run once each per pipeline run
    lean/Run/Witness.lean   GENERATED: every falsifying input the generated harnesses found, evaluated on the model
    compare/e1/             plan node E1: the generated harness set on the K2 mutants (run.py, analyse.py, feedback.py,
                            results/, E1_TRADES.md)
    lean/Run/Adequacy.lean, AdequacyAudit.lean GENERATED scripts for the suite adequacy note; imported by nothing
    mutation/               run_mutants.py (18 wallet + 27 ledger Rust mutants, 38 negative controls), workcopy.sh, results, logs
    effort/                 attempts.tsv (every `./lakebuild.sh` call: time, target, ok/FAILED, seconds), count.py
    schema/                 JSON Schema v2 of the graph; maths_fit.py + maths-example.graph.json; selftest.py
    review/                 evidence from the reviews: spec/, schema/ (first build), loops/ (adversarial review of the ledger),
                            loops-fix/ (what was rerun when that review's findings were fixed)
    run.sh, translate.sh    the pipeline; Rust -> Lean translation only
    DESIGN.md, TOOLCHAIN.md design and its implementation notes; versions, pins, undo steps
    probe/                  throwaway evidence from the design stage

## Adding a sentence

A NEW rule or scenario, with words the Clausebook has (this is how everything in `features/ledger_rules.feature`
was added; no entry of `glossary.yaml`, no step and no Rust predicate is written):

1. Write it in a feature file under `features/`, with `@id:<name>`. Give a scenario Examples rows; a Rule line may
   stand alone. `python3 -m clausal compile <file>` tells you at once whether it composes (UNBOUND / ILL-TYPED /
   AMBIGUOUS with file:line and the nearest forms otherwise; add a piece to `clausebook.yaml`, with its Lean
   definition, its Rust reading in `wallet-bdd/src/pieces.rs` and its typed Rust reading in `evidence/src/typed.rs`
   with an arm in `clausal/evgen.py`, only if the words are really new).
2. `./run.sh`. It is echoed, run on the compiled Rust (rows through the generic step; the reading on generated
   inputs), searched, given a generated property test and a generated Kani harness (no test code to write), and gets
   a flat proof obligation in `lean/Wallet/Obligations.lean` and a `sorry` stub under `lean/Wallet/Proofs/`
   (scenario) or `lean/Wallet/RuleProofs/` (a Rule nothing beneath could prove). Verdict: TESTED-ONLY, with the
   evidence ladder of its block saying what it holds (property test, bounded check up to which sizes), or REFUTED /
   COUNTEREXAMPLE if the search or a generated harness finds a failing input. Tag a deliberately false one
   `@expect-refuted`, one deliberately left unproved `@expect-unproved`.
3. Replace the `sorry` with a proof of the obligation (see the header of the stub). The verdict becomes
   PROVED-FOR-ALL when the kernel accepts it and the generated equivalence with the reading.

A sentence written with the phrases of the OLD glossary (the 34 older scenarios) goes the older way:

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

Other commands: `python3 -m clausal steps` (the step forms the generic cucumber step is registered for),
`python3 -m clausal review <id|all> --reviewer NAME`
(record a glossary sign-off in `glossary.signoff.json`),
`python3 -m clausal.graphlint out/graph.json [--what-if <node-id>]` (validate the graph; show what would go stale),
`python3 schema/selftest.py` (the schema and lint must reject ten deliberately invalid graphs).
