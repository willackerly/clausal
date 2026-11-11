# Architecture

How lean-rosette is put together, why each part is the way it is, and where it is weak. Written 2026-11-10. The frame library and vocabulary described here were under independent review on that date, so details may move; `slice/DESIGN.md` is the working design record and wins where the two differ.

Read the [README](../README.md) first for what the project is for.

## Contents

1. [The problem, stated precisely](#1-the-problem-stated-precisely)
2. [The chain of assurance](#2-the-chain-of-assurance)
3. [The pipeline](#3-the-pipeline)
4. [The vocabulary](#4-the-vocabulary)
5. [Verdicts](#5-verdicts)
6. [Evidence in layers](#6-evidence-in-layers)
7. [How the tool checks itself](#7-how-the-tool-checks-itself)
8. [The trusted base](#8-the-trusted-base)
9. [The evidence graph](#9-the-evidence-graph)
10. [Proofs and who writes them](#10-proofs-and-who-writes-them)
11. [The translator and the Rust profile](#11-the-translator-and-the-rust-profile)
12. [Code that is not Rust](#12-code-that-is-not-rust)
13. [The mathematics tooling](#13-the-mathematics-tooling)
14. [Repository and toolchains](#14-repository-and-toolchains)
15. [Open design questions](#15-open-design-questions)

## 1. The problem, stated precisely

A requirement lives in someone's head and in prose. An implementation lives in code. Three gaps separate them:

- **The meaning gap.** Does a formal statement say what the requirement's owner meant? This cannot be proved, because one side of it is not formal.
- **The proof gap.** Is the formal statement true of a model of the code? This can be proved.
- **The model gap.** Does the model behave as the running code does? This can be proved in principle and is tested in practice.

Most verification projects spend their effort on the proof gap, which is the one a machine can close, and leave the meaning gap to a few experts reading formal text. As proofs get cheaper, the meaning gap becomes the binding constraint. The architecture is organised around making that gap small, explicit and auditable, and around never letting evidence about one gap be mistaken for evidence about another.

Two design rules follow and recur throughout:

1. **Fail closed.** An unknown word, an ambiguous sentence, a failed proof or a missing check yields no claim. It never yields a guess.
2. **Say what it rests on.** Every verdict is reported with the evidence behind each link, by kind.

## 2. The chain of assurance

![The chain of assurance](diagrams/chain.vector180.svg)

| Link | From → to | What could go wrong | Evidence, and its kind | What limits the risk |
|---|---|---|---|---|
| Meaning | English rule → reading | The reading is not what the author meant | Signed vocabulary pieces; echo confirmed by the author. *Human-asserted* | Few pieces, each one line; a second independent reading of each piece compared on generated inputs; sign-off voided when a definition changes |
| Composition | Reading → Lean statement | Pieces assembled wrongly | Generated, then type-checked by Lean. *Machine-checked* | Typed holes; one way to parse or the sentence is refused |
| Proof | Statement → model | The statement is false, or the proof proves something else | Lean's kernel; the audit requires the proof's type to be exactly the statement. *Kernel-checked* | Standard axioms only; conditions shown satisfiable; suite checked against trivial implementations |
| Translation | Model → Rust source | The model does not behave as the code | Aeneas, with hand-written models of some standard-library functions. *Tool-trusted*, plus *tested* | The same examples and counterexamples run on both model and compiled Rust; versions and hashes recorded |
| Compilation | Rust source → running code | Miscompilation, hardware faults | rustc. *Trusted* | Not addressed |

The four evidence kinds are deliberately not ordered into a single scale. "Tested on a thousand inputs" and "trusted tool" are not comparable, so the report lists them side by side.

## 3. The pipeline

![What people write, what the tools generate and check, what comes out](diagrams/pipeline.vector180.svg)

One command, `slice/run.sh`, does the following. Paths are under `slice/`.

| Step | What happens | Where |
|---|---|---|
| Translate | Rust crates go through Charon and Aeneas into Lean models; a provenance file records hashes and tool versions | `translate.sh`, `lean/Generated/` |
| Compile sentences | Each scenario and each `Rule:` line is assembled from vocabulary pieces into one reading: frames applied to an operation | `slicegen/vocab.py`, `vocabulary.yaml`, `lean/*/Pieces.lean`, `lean/*/Readings.lean` |
| Build | Lean checks the models, the statements, the lemma libraries and the proofs. One module per scenario, so one broken proof costs one scenario | `lean/` |
| Search | Example rows are evaluated on the model; a search looks for an input that satisfies the conditions and for one that breaks the claim | `lean/Run/Search.lean`, `ReadingSearch.lean` |
| Link | For every scenario, the compiled reading is proved equivalent to the flat statement the proofs are about; for every rule, its statement is derived from its scenarios | `lean/Run/Links.lean` |
| Audit | Theorems derived from the search are kernel-checked (satisfiable conditions, refutation at a counterexample); axioms are collected; every proof's type is compared with its statement | `lean/Run/Audit.lean` |
| Run on Rust | cucumber-rs runs the same feature files on the compiled code, replays each counterexample, and evaluates the Rust reading of each phrase on the same inputs as the Lean one | `wallet-bdd/` |
| Suite note | Each operation's rules are re-stated against trivial implementations and searched | `lean/Run/Adequacy.lean` |
| Report | A block per rule and per scenario, and the evidence graph | `slicegen/report.py`, `out/report.md`, `out/graph.json` |

Two components are explicitly **not trusted**:

- **The sentence compiler.** It is a small program that finds the one way a sentence is built from known forms and writes out the Lean term the pieces spell. Lean type-checks the result, the report prints the reading beside the sentence, and the link step proves the reading equivalent to the statement that was proved.
- **Proof text.** Whoever or whatever wrote it, only kernel acceptance of a theorem with exactly the right type counts.

## 4. The vocabulary

![A sentence is compiled from reusable, typed pieces](diagrams/vocabulary.vector180.svg)

### Three kinds of piece

| Kind | Examples | In Lean | Reused across | Signed |
|---|---|---|---|---|
| Frame | never changes, always, only if, exactly when, changes only, is rejected and changes nothing, increases by exactly, at most, every … of, more never loses, agrees with, is independent of | A definition over an abstract operation with typed holes | Every project | Once |
| Modifier | given, successful, rejected, internal, aggregate, then, bystander, the first … of | A function from a piece to a piece of the same kind | Every project | Once |
| Domain word | account, balance, transfer, batch, accepted | A type, a measure, a condition, or an operation bound to a function of the generated model | One system | Per project |

### The abstract operation

Every frame is stated about one thing: an operation that takes a state and an input and either returns an answer and a new state, or fails to return. The operation also says which answers count as acceptance and which calls a claim covers. Frames therefore mean the same thing whether the operation is a wallet withdrawal or an access decision.

Holes are typed: a measure is a function from state to a value, a condition is a predicate on state and input, a collection is a list drawn from state, input and answer. There is no frame that takes an arbitrary relation between before and after, so a sentence cannot smuggle in an unreviewed claim through a catch-all.

### Defaults are strict and printed

- "Never" and "always" cover every call, accepted or rejected.
- Every frame includes "the call returns": no panic, no hang.
- "If" is one direction. The converse has its own frame ("only if") and both together have a third ("exactly when"). The converse is never inferred.
- "Successful" and "rejected" narrow a claim to some calls. They are the non-default reading and must be written.

The echo prints each default that was applied, so a reader sees what was added to their sentence.

### Granularity

Split a phrase where a part would be reused with a different partner. "Aggregate" is its own piece because "aggregate fees" will follow; "account value" stays whole until something forces a split. Start coarse, split on the second use.

### Composition and refusal

A sentence compiles only if there is exactly one way to build it from known forms. Otherwise it is refused, with a location and the nearest forms:

- **Unbound:** a word or form is not in the vocabulary.
- **Ill-typed:** the pieces exist but do not fit, and the two types are named.
- **Ambiguous:** more than one reading. The intended design is to show an input on which the readings differ and ask.

### Rules and their scenarios

A `Rule:` line compiles to one statement. The universally quantified scenarios beneath it are its parts: a generated, kernel-checked theorem derives the rule from them, usually by cases on their conditions. Only that direction is claimed. Example rows are the tested instances of the same claim.

### The second reading

Each frame has, beside its Lean definition, an independent executable checker. The two are compared on generated inputs on every run. Each domain word likewise has a Rust reading compared with its Lean definition. This catches a definition that is wrong in one place; it does not catch one that is wrong the same way in both.

### What a sentence still needs

Today a new sentence built from existing pieces gets a statement, an echo and a model search. It does not yet get a run on compiled Rust without a hand-written step, or a verdict without a proof being supplied. Closing that is the current work.

Design history and decisions: `docs/VOCABULARY.md`. Prior art: `out/prior_art_vocabulary.md`.

## 5. Verdicts

| Verdict | Meaning |
|---|---|
| Proved for all inputs | A kernel-checked theorem whose type is exactly the generated statement, standard axioms only, with conditions shown satisfiable |
| Proved for an instance | The same, for a scenario with literal values |
| Refuted | A concrete input on which the statement is false, checked in the kernel and replayed on the compiled code |
| Counterexample | A failing input found by testing, without a kernel-checked refutation |
| Tested only | Example rows pass; no proof, or a proof that does not check |
| Unbound / ill-typed / ambiguous | The sentence did not compile |
| Vacuous | The conditions cannot be met, so the claim says nothing |
| Unlinked | A proof exists but its statement was not shown equivalent to the compiled reading |

Two rules about verdicts matter more than the list:

- **A failed proof means "not shown", never "false".** In experiments, most lost proofs under an injected bug belonged to rules that were really false, but a large minority belonged to rules that were still true.
- **A verdict is recorded as "review", not "pass", while it rests on unsigned vocabulary.** A strict mode turns that into a failure.

## 6. Evidence in layers

![One compiled rule, four kinds of evidence](diagrams/evidence.vector180.svg)

Measured on the fixtures against tool-generated bugs (`slice/compare/TRADES.md`):

- Example rows caught most injected bugs but only about two thirds of the individual rule violations.
- Property-based tests with generators weighted toward boundary values found every violation.
- Bounded model checking found nearly all, on the real Rust with no translation step, and was the only technique to find bugs that occur at a single magic value. It could show a rule *holds* only up to small sizes.
- No bug needed a proof to be caught. The proofs' distinct contribution was a result independent of any sample or size bound.

The design consequence: because every frame already has an executable reading, a compiled rule can generate its own property test and bounded-checking harness as well as its Lean statement. A failing input from any layer is replayed on the Lean model. If it fails there too it becomes a refutation; if model and Rust disagree, that is a finding about the translation link. Generating these harnesses is in progress; today they are hand-written.

## 7. How the tool checks itself

Each check exists because a reviewer found the failure it prevents.

| Check | The failure it prevents |
|---|---|
| A proof's type must be exactly the generated statement, from that scenario's own module | A theorem of type `True` was once counted as a proof |
| Only the three standard axioms; no `sorry`; no native evaluation | A proof resting on something unchecked |
| A kernel-checked witness that the conditions can be met | A claim that is true because its conditions never hold |
| Suite adequacy note: rules restated against "rejects everything", "does nothing", identity and constant implementations | A safety rule that a do-nothing implementation also satisfies; reported for the suite, as information |
| A second reading of every piece, compared on generated inputs | A subtly weakened definition passing silently |
| Counterexamples replayed on compiled code | A refutation that is an artefact of the model |
| Mutation runs: bugs injected into the Rust must be shown false by some rule | A rule set that leaves real behaviour unconstrained |
| "Shown false" counted separately from "proof lost" | An agent re-proving around a bug and getting a green run |
| Negative controls that must fail | A check that cannot fail |
| Reading proved equivalent to the proved statement | A recompiled sentence quietly weakened |

## 8. The trusted base

What a "proved" verdict rests on, in full:

| Trusted | Size or nature | How it is bounded |
|---|---|---|
| The vocabulary | A few dozen pieces, one line each | Printed in every report; second readings; sign-off with staleness |
| Lean's kernel | Small, widely used | Standard |
| The audit code | About a hundred lines of Lean | Negative controls |
| Aeneas and Charon | A research translator | Cross-checking by execution; pinned versions; this project carries small patches |
| Aeneas's models of standard-library functions | Hand-written | Listed per report; not yet separately tested |
| The Gherkin parser and test glue | Small | The same files run under an independent runner |
| rustc and the hardware | Large | Assumption |

Not trusted: the sentence compiler, proof text, and any agent that wrote either.

## 9. The evidence graph

Every run writes a graph (`out/graph.json`; format in `docs/SCHEMA.md`):

- **Nodes** have an interface (a statement, a signature) and zero or more implementations (a proof, a function body). Kinds include rule group, scenario, vocabulary piece, theorem, model function, source function.
- **Edges** carry a list of evidence entries, each with a kind, the tool or person behind it, and digests of what it was computed from.
- **Staleness is computed, never stored.** If a vocabulary piece changes, every statement built from it, every proof of those statements and every sign-off is marked stale.

The "rests on" block of a report is generated from the graph. The same format is meant to describe mathematics (a theorem decomposed into lemmas, statements shared across proofs), so navigation and audit tools can be shared.

## 10. Proofs and who writes them

- **Straight-line code** proves almost automatically: a few lines per rule using Aeneas's step tactic and arithmetic automation.
- **Loops do not.** Each needs an invariant, usually a small pure description of what the loop computes, and a proof connecting the two. Measured cost is about six lines of hand-written Lean per line of Rust, stable across two experiments and two models. Once a loop's lemma exists, further rules about it are cheap.
- **Agents can write these proofs.** On a crate neither had seen, with rules by a separate author, two models each proved all seven loop functions in under fifteen minutes. The loops were textbook patterns; unfamiliar invariants are untested.
- **The hazard is an agent proving around a bug.** If no rule forbids a wrong behaviour, an agent asked to make the build green will re-prove the lemmas to fit. The defences are the mutation runs, the suite note and the rule that agents may not edit rules or vocabulary to get a proof through.
- **Exact results need a reference.** "The loop computes X" cannot be stated without saying what X is. Today that is a small pure definition in the vocabulary, signed like any other piece.

## 11. The translator and the Rust profile

A census of ten real crates (`census/CENSUS.md`) found that tool robustness, more than Rust idiom, decides how much translates: one error aborted whole crates. Five small patches (`census/fork/`) raise the share of functions ending as compiling Lean from 1% to 35%, and to 82% outside one crate that fails earlier in the toolchain.

`census/PROFILE.md` is a written profile of Rust that translates: how to write loops, which library functions are modelled, what to avoid. Code meant to be verified should be written to it, in the way code meant to be fast is written with the optimiser in mind.

## 12. Code that is not Rust

Much code worth verifying is not Rust. The pattern used on TDFLite's Go decision logic is a separate, weaker but still useful chain:

1. Write a Lean model from the source by hand (or by agent), keeping a line-by-line trace to the code.
2. Check the model against the real implementation by differential testing on generated inputs, and keep that as a one-command check for any later commit.
3. Write down every reasonable formal reading of each English guarantee. Where readings differ, find an input that separates them and ask the owner. Search for counterexamples to each reading and replay them on the real code.
4. Turn the owner's rulings into parameters of the model, prove the guarantees under them, and emit test vectors in the project's own format.

Here the model link is *tested*, not *tool-trusted*, and the report must say so. The method found real behaviour on real code, and its one mistake was instructive: a proposed change touched a path the model did not describe, and only a reviewer caught the regression. Anything outside the model needs its own evidence.

## 13. The mathematics tooling

A separate strand asks whether large formal developments can be made navigable. It shares the evidence graph and the habit of measuring against ground truth.

| Tool | What it does | Where |
|---|---|---|
| Candidate enumeration and lifting | Lists every proof-valued piece of a proof term; turns chosen pieces into real lemmas with the kernel re-checking the result | `Rosette/` |
| Corpus exporters | Declaration graphs, statements and proof sizes from built Lean projects, across Lean versions | `corpora/tools/`, `corpora/ns_export/` |
| Outline and validation | Dominator-based and definition-centred outlines; scoring against human blueprints and against the papers | `bench/outline*.py`, `bench/paper_truth.py` |
| Dead code | What a reader need not read, confirmed by deleting and rebuilding | `bench/deadcode.py`, `tools/deadcode/` |
| Friction census | Where proof bulk sits, by kind of side-condition | `bench/friction_*.py` |

What has been learned is mostly negative and is recorded in `out/FINDINGS.md` and `out/corpus/FINDINGS.md`: size and graph position do not identify what people find meaningful; the content of a large machine proof sits in its definitions.

## 14. Repository and toolchains

The repository holds several independent projects with different pinned toolchains, because the tools they depend on pin different versions.

| Project | Path | Lean |
|---|---|---|
| Restructuring tools | repo root (`Rosette/`) | 4.36.0-rc2, with Mathlib |
| The pipeline | `slice/lean` | 4.35.0 (Aeneas's pin) |
| Machine-generated corpus | `corpora/ns` | 4.34.0-rc2 |
| Human corpora | `corpora/pfr`, `corpora/carleson` | 4.36 |

Charon needs one exact Rust nightly; ordinary builds and tests use stable. Setup, disk use and rebuild steps: `docs/SETUP.md`.

## 15. Open design questions

- **Does echo-back work on people?** Model readers catch most seeded misreadings. Nobody has yet tested people, and that decides how much weight the meaning link can carry.
- **How should a loop be fully specified?** A signed reference definition, or rules that compare two runs ("applying a batch equals applying its first transfer then the rest").
- **Effects, input/output and concurrency.** Frames describe one pure call. A shell around a pure core is not covered, and real defects live there.
- **Two-run claims.** "More never loses" and "is independent of" compare two calls. They have definitions and tests; their sentence forms are new.
- **Who may sign what.** Domain words need a domain owner; the Lean behind them needs a different reviewer; shared frames need more than one signer.
- **Versioning the shared frame library.** A change to one frame voids signatures across every project that uses it, unless the change is proved meaning-preserving.
- **Time.** No current target needs "eventually" or "until". Step-by-step invariants cover the cases in hand.
- **The compilation link.** Verified compilation for Rust is an open problem in the field and is left as a stated assumption.
- **Presenting evidence to an auditor.** The graph has the content; the form an evaluator wants has not been designed.

The plan that sequences these is `docs/PLAN.md`.
