# lean-rosette

**An English sentence about what software must do, a machine-checked proof that the code does it, and an honest account of what that proof rests on.**

This is a research prototype (November 2026, Apache-2.0). It is built by one person working with AI agents, and it keeps its negative results.

## Why this exists

Most software is specified in prose and checked by tests. Tests show that some cases work. They cannot show that no case fails, and the prose is never checked at all.

Formal verification closes that gap, but it has stayed rare for three reasons:

1. **Writing proofs was expensive.** That is changing quickly: language models can now write many of them.
2. **The formal statement is unreadable to the people who own the requirement.** A proof of the wrong statement is worthless, and nobody who knows the requirement can tell.
3. **Everything is bespoke.** Each project invents its own way of stating things, so nothing accumulates.

This project works on the second and third. The bet is that if proofs are becoming cheap, the scarce things are *knowing what was proved* and *not starting from zero each time*.

The goal is formally modelled software as the default: a chain of assurance from a plain-English description down to the code that runs, with the trust placed in each link stated, bounded and repeatable.

## The idea in one picture

![From an English rule to running code: every link names its evidence](docs/diagrams/chain.vector180.svg)

No link in that chain is free of trust, and the project does not pretend otherwise. What it insists on is that every link is named and carries a known kind of evidence:

| Link | The question it answers | Evidence |
|---|---|---|
| Meaning | Does the formal reading say what the author meant? | A small signed vocabulary; the reading echoed back in English for the author to confirm |
| Composition | Were the pieces assembled correctly? | Mechanical and typed; Lean rejects what does not fit |
| Proof | Is the statement true of the model? | Lean's kernel |
| Translation | Does the model behave as the Rust does? | A trusted tool, cross-checked by running both |
| Compilation | Does the binary do what the source says? | Trusted; not addressed yet |

The meaning link is the weakest and gets the most design attention. It cannot be proved, only made small enough to audit.

## A rule, end to end

This is the target. The parts that exist today are listed under [Where it stands](#where-it-stands).

An engineer writes a rule in standard Gherkin, using words that already have signed definitions:

```gherkin
Rule: Internal fund transfers never change aggregate account value

  Scenario Outline: a transfer between two accounts of the ledger
    Given a ledger in which <from> and <to> are accounts
    When <amount> is transferred from <from> to <to>
    Then the aggregate account value is unchanged

    Examples:
      | from | to | amount |
      | 0    | 1  | 30     |
      | 1    | 0  | 500    |
```

One command reports:

```text
Rule: Internal fund transfers never change aggregate account value
  Reading   for every ledger and every transfer between two of its accounts,
            accepted or rejected, the call returns, and the sum of all
            balances afterwards equals the sum before
  Verdict   PROVED FOR ALL INPUTS
  Examples  2 of 2 pass on the compiled Rust
  Suite     with "a covered transfer between two accounts is accepted"
            (also proved), the suite rules out a ledger that rejects everything

  Rests on
    meaning      5 vocabulary pieces, all signed            human-asserted
    proof        theorem checked by Lean's kernel,          kernel-checked
                 standard axioms only
    translation  Lean model generated from ledger.rs        tool-trusted, cross-checked
                 by Aeneas                                  on the examples
    compilation  rustc                                      trusted
```

What makes this more than a test run:

- **The rule is proved for every input.** The example rows are the same claim as ordinary tests.
- **The sentence needed no new definitions.** It was compiled from pieces defined earlier.
- **The reading is echoed back,** so the author can see how the sentence was understood.
- **Rules are read as a suite.** One rule rarely pins behaviour alone, so the report says what the suite still allows.
- **A false rule fails usefully,** with a concrete input that breaks it, confirmed on the compiled code.

## Why Gherkin, Lean and Rust

Each was chosen for what it already does well, and each has a limit worth knowing.

### Gherkin: the surface people already use

- **What it gives.** Given / When / Then is a precondition, an operation and a postcondition: the shape of a formal claim, in a format product and test teams already read. A `Rule:` line states the claim; the scenarios beneath it are its examples. Existing runners execute the same file as ordinary tests, so every rule gets tested evidence for free.
- **Its limit.** Gherkin has no meaning of its own. Runners treat the rule line as a label. Reading it as "for all inputs" is this project's addition, and the vocabulary is what makes that reading precise.

### Lean: one small trusted checker

- **What it gives.** Definitions, statements and proofs in one language, checked by a small kernel. The same system is a programming language, so the tooling that compiles sentences, audits proofs and searches for counterexamples is written in it. Its mathematics library is the largest coherent body of formal mathematics available.
- **Its limit.** Proofs about loops are not automatic. In this project's measurements they cost about six lines of Lean per line of Rust, whoever writes them.

### Rust: code a translator can reason about

- **What it gives.** Ownership rules out aliasing and shared mutation, which is what lets Rust be translated into pure functions that a prover can handle. Aeneas does that translation into Lean. Rust is also where much new security-critical code is being written.
- **Its limit.** The translator is young. As shipped it handled 1% of functions in ten real crates; with five small patches, 35%, and 82% outside one crate that fails earlier in the toolchain. Idiomatic iterator chains and closures still need rewriting.

### The rest of the ecosystem

| Piece | Role here |
|---|---|
| Aeneas and Charon | Translate Rust into a Lean model |
| cucumber-rs | Runs the feature files as tests on the compiled code |
| Property-based testing, bounded model checking (Kani) | Find counterexamples quickly, on the real Rust |
| Mathlib | Mathematics the proofs draw on |
| NASA's FRET, property-pattern catalogues | Prior art for fixed sentence shapes with a formal reading |
| Cedar (AWS) | Precedent for a Lean model cross-checked against production code |

Nobody was found doing the whole chain. Several pieces overlap with existing work, and the survey says where: `out/prior_art_vocabulary.md`.

## Reusable libraries are the point

A proof effort that starts from nothing each time will never be the default. What should accumulate is a set of libraries, each written once and trusted once.

![A sentence is compiled from reusable, typed pieces](docs/diagrams/vocabulary.vector180.svg)

A sentence is built from three kinds of piece:

- **Frames** are the logical shape of a claim: *never changes*, *always*, *only if*, *exactly when*, *changes only*, *more never loses*, *agrees with*, *is independent of*. There are a couple of dozen. They are the same for every project, so they are defined and signed once.
- **Modifiers** narrow or combine: *internal*, *aggregate*, *successful*, *rejected*. Also shared.
- **Domain words** are the nouns and verbs of one system: *account*, *transfer*. They are bound to the actual code.

Defaults are strict. "Never" and "always" cover every input, including ones the operation rejects, and include "the call returns". A weaker reading has to be asked for in words.

The same idea applies at each layer of the chain:

| Layer | Library that accumulates |
|---|---|
| Meaning | Frames and modifiers shared across projects; domain vocabularies per system |
| Proof | Lemmas about common loop shapes and data structures; Mathlib |
| Translation | A written profile of Rust that translates; models of standard-library functions |
| Evidence | Generators for tests and bounded checks, derived from the frames |

The measure of success is simple: what fraction of new sentences compile, run and get a verdict with no new piece written.

## One rule, several kinds of evidence

![One compiled rule, four kinds of evidence](docs/diagrams/evidence.vector180.svg)

Proof is not the only evidence worth having, and it is the most expensive. On this project's fixtures, sampled tests and bounded checks found nearly every injected bug, faster than the proof pipeline did. Proof added the one thing they cannot: a result for every input and every size.

So each compiled rule is meant to produce all four, and the report says which is the strongest evidence held. Nothing is called proved without a kernel-checked proof.

## Where it stands

A critical summary. The full table of questions tested is in `docs/RESULTS.md`.

**Works today**

- Gherkin scenarios bound through a vocabulary to Lean statements about Rust translated by Aeneas, with a verdict per scenario: proved for all inputs, refuted with a counterexample, tested only, unbound, or vacuous. Two small fixtures, 35 scenarios.
- A frame library of 23 frames; every earlier statement proved equivalent to its recompiled form; rule lines compile and are echoed in English. (Under independent review as this is written.)
- Checks that the tool is not fooling itself: a proof must have exactly the generated statement as its type; conditions must be satisfiable; a rule suite is checked against trivial implementations; injected bugs must be noticed.
- On real code: a Lean model of TDFLite's access-decision logic, written from the Go source, agreeing with the Go on about 400,000 generated cases. It surfaced all six edge cases known from a manual review (the search was guided) and fifteen more. The owner has ruled on them; under those rulings five of the eight guarantees are proved outright and a sixth is proved given named facts about the compiler.
- Two language models each wrote the proofs for seven loop functions unaided in under fifteen minutes, on textbook loops.

**Does not work yet**

- A new sentence gets a statement and an echo but cannot yet run on compiled Rust without hand-written glue.
- Property tests and bounded checks are hand-written per rule, not generated.
- Everything about the meaning link has been tried only with language models as authors and readers. No person has taken the trials.
- The vocabulary is unsigned.
- Compilation and hardware are assumptions.

**Open risks**

- Whether people catch a wrong reading when it is echoed back. This decides how much the meaning link can bear.
- Code the model does not cover. The one real defect found in a proposed change was on a path outside the Lean model.
- Dependence on a young translator, which this project currently patches.
- How a loop's exact behaviour should be specified. Today it needs a small reference definition in the vocabulary.

## The mathematics strand

The project began with a different question: can large machine-generated Lean proofs be made navigable for mathematicians? That strand continues, at lower intensity, because verified software produces large formal developments too, and the shared vocabulary is itself a library people will need to find their way around.

It has been humbling. Five ideas for scoring proof structure by size or graph position were tested against human judgement and all failed. What did work:

- **Telling a reader what to ignore.** A quarter of a 640,000-line machine-generated corpus was deleted and its headline theorems still check.
- **Sound restructuring.** Pieces of a proof can be lifted into real lemmas with the kernel re-checking everything.
- **A ground truth.** The corpus's own papers mapped to its Lean declarations, so outlines can be scored against something external.
- **An observation worth chasing.** The machine re-invented a standard library abstraction several times without sharing it.

Details: `out/FINDINGS.md`, `out/corpus/FINDINGS.md`.

## Find your way around

| If you want | Read |
|---|---|
| Every question tested and its answer | `docs/RESULTS.md` |
| What was tried, how, and what happened | `docs/EXPERIMENTS.md` |
| The plan: hypotheses, targets, order of work | `docs/PLAN.md` |
| How sentences are built from pieces | `docs/VOCABULARY.md` |
| The shared graph of statements and evidence | `docs/SCHEMA.md` |
| What to do next | `TODO.md` |
| Why each call was made, and how to undo it | `DECISIONS.md` |
| To get a machine working | `docs/SETUP.md` |
| Rules for agents working here | `AGENTS.md` |

| Path | What it is |
|---|---|
| `slice/` | The Gherkin → Lean → Rust pipeline: frame library, vocabulary, fixtures, reports |
| `slice/compare/` | What each kind of evidence catches, and what it costs |
| `census/` | How much real Rust translates; the translator patches |
| `p2/` | The proof-writing comparison between two models |
| `trials/` | Reading and authoring trials, ready for people |
| `Rosette/`, `bench/`, `tools/` | Lean tooling for restructuring and analysing large proofs |
| `corpora/`, `out/` | External Lean projects under study, and results |
| `docs/diagrams/` | The figures above, as editable Vector180 sources |

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"

cd slice && ./run.sh      # the pipeline; report in slice/out/report.md
lake build Rosette        # the Lean restructuring tools (repo root)
```

## How the work is done

- **Hypothesis, measurement, attack, fix.** Each idea is stated with a target, measured on real data, checked by an independent reviewer on a different model, corrected and rerun.
- **Report, don't gate.** The destination is fixed. Results say how good the approach is and what the trades are; a miss changes what is built next.
- **Negative results are kept.** They are most of what has been learned about the mathematics strand.
- **Data comes from the tools, not from text matching.** Lean's own environment, real compiled code.
- **People decide judgement calls.** Language models are used as proxies and labelled as such.
- **Every judgement call is logged** with its reason and how to undo it.
