# lean-rosette

**Write what your software must do in plain English. Get back a proof that the code does it for every input, or the input that breaks it, and a plain account of what that answer rests on.**

Tests show that some cases work. This shows that no case fails, in terms the person who owns the requirement can read and check.

Research prototype, November 2026, Apache-2.0. **[Architecture](docs/ARCHITECTURE.md)** · [Results](docs/RESULTS.md) · [Plan](docs/PLAN.md)

## What it looks like

An engineer writes a rule in ordinary Gherkin, the format many teams already use for behaviour tests:

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

One command answers:

```text
Rule: Internal fund transfers never change aggregate account value
  Reading   for every ledger and every transfer between two of its accounts,
            accepted or rejected, the call returns, and the sum of all
            balances afterwards equals the sum before
  Verdict   PROVED FOR ALL INPUTS
  Examples  2 of 2 pass on the compiled Rust

  Rests on
    meaning      5 vocabulary pieces, all signed       human-asserted
    proof        checked by Lean's kernel              kernel-checked
    translation  Lean model generated from ledger.rs   tool-trusted, cross-checked
    compilation  rustc                                 trusted
```

Four things in that answer are the point of the project:

- **Proved for all inputs.** Not two examples: every ledger, every transfer.
- **The reading is echoed back.** The author sees how the sentence was understood, including what was assumed on their behalf, before trusting the verdict.
- **A false rule fails usefully.** The report shows a concrete input that breaks it, confirmed on the compiled code.
- **Nothing is hidden.** Each step from sentence to running code is listed with the kind of evidence behind it.

This is the target. What already works is under [Where it stands](#where-it-stands).

## Why it matters

Formal verification has been possible for decades and rare in practice, for three reasons:

1. **Proofs were expensive to write.** Language models are changing that fast.
2. **Nobody who owns the requirement can read the formal statement.** A proof of the wrong statement is worthless, and it looks exactly like a proof of the right one.
3. **Every project starts from zero.** Nothing accumulates.

As proofs get cheap, the scarce things become *knowing what was actually proved* and *not starting over each time*. Those two are what this project works on.

The aim is for formally modelled software to be the default, not the exception.

## How it works

![From an English rule to running code: every link names its evidence](docs/diagrams/chain.vector180.svg)

A rule passes through a chain. The sentence is assembled into a precise reading from a small vocabulary of signed definitions. The reading becomes a statement in Lean, a proof assistant with a small trusted checker. The statement is proved about a model of the code that a translator generates from the Rust source.

No link in the chain is free of trust, and the project does not pretend otherwise. It insists that each link is named, carries a known kind of evidence, and can be re-checked by someone else. The first link, from English to a formal reading, can never be proved. So the design makes it small enough to audit.

The full design is in **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

## Why it can scale: reusable pieces

![A sentence is compiled from reusable, typed pieces](docs/diagrams/vocabulary.vector180.svg)

A sentence is not interpreted as a whole. It is compiled from pieces, each defined once in Lean and signed off once:

- **Frames** are the logical shapes of claims: *never changes*, *always*, *only if*, *exactly when*. There are a couple of dozen, shared by every project.
- **Modifiers** narrow or combine: *internal*, *aggregate*, *successful*.
- **Domain words** are the nouns and verbs of one system, tied to its actual code.

A new sentence built from known pieces needs no new definitions and no new human judgement beyond confirming the echo. Trust grows with the size of the vocabulary, not with the number of sentences.

The same principle is applied at every layer: shared proof lemmas for common loop shapes, a written profile of Rust that translates cleanly, generators for tests. Libraries are what turn a research exercise into something routine.

## More than one kind of evidence

![One compiled rule, four kinds of evidence](docs/diagrams/evidence.vector180.svg)

Proof is the strongest evidence and the most expensive. Sampled tests and bounded checks are cheap and, in this project's measurements, find most mistakes faster. So one compiled rule is meant to yield all of them, and the report says which is the strongest evidence held. Nothing is called proved without a kernel-checked proof.

## Why Gherkin, Lean and Rust

- **Gherkin** is already read by product and test teams, and Given / When / Then has the shape of a formal claim. The same file runs as ordinary tests.
- **Lean** puts definitions, statements, proofs and the tooling itself in one language checked by one small kernel.
- **Rust**'s ownership rules are what allow real code to be translated into a form a prover can reason about.

Each has limits, covered in the [architecture document](docs/ARCHITECTURE.md), along with the other tools this builds on.

## Where it stands

A critical summary. Every question tested, with its answer, is in [docs/RESULTS.md](docs/RESULTS.md).

**Works today**

- Gherkin scenarios bound to Lean statements about real Rust, with a verdict for each: proved for all inputs, refuted with a counterexample, tested only, or not understood. Two small example programs, 35 scenarios.
- A library of 23 frames. Rule lines compile and are echoed in English. (Under independent review as this is written.)
- Checks that the tool is not fooling itself. Each exists because a reviewer found the failure it prevents.
- On real code: a Lean model of TDFLite's access-decision logic agrees with the production Go on about 400,000 generated cases. Testing eight plain-English guarantees against it surfaced the six edge cases already known and fifteen more.
- Two language models each wrote the proofs for seven loop functions unaided, in under fifteen minutes.

**Does not work yet**

- A new sentence gets a reading but cannot yet run end to end without some hand-written glue.
- The extra evidence layers are hand-written per rule, not generated.
- Only language models have stood in as authors and readers. No person has taken the trials, and the vocabulary is unsigned.
- Compiler and hardware are assumed correct.

**Open risks**

- Whether people really catch a wrong reading when it is echoed back.
- Code outside the model. The one real defect found so far was on a path the model did not describe.
- The translator is young. As shipped it handled 1% of functions in ten real crates; with five small patches carried here, 35%.
- Proofs about loops cost about six lines of Lean per line of Rust.

## Also here: making large proofs navigable

The project began with a different question: can large machine-generated proofs be made readable for mathematicians? That strand continues at lower intensity, because verified software produces large formal developments too.

It has been humbling. Five ways of scoring proof structure were tested against human judgement and all failed. What worked: telling a reader what to ignore (a quarter of a 640,000-line machine-generated proof corpus was deleted and its main theorems still check), and restructuring proofs with the checker confirming every step. Details: [out/FINDINGS.md](out/FINDINGS.md), [out/corpus/FINDINGS.md](out/corpus/FINDINGS.md).

## Find your way around

| If you want | Read |
|---|---|
| The design in depth | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Every question tested and its answer | [docs/RESULTS.md](docs/RESULTS.md) |
| What was tried, how, and what happened | [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md) |
| The plan | [docs/PLAN.md](docs/PLAN.md) |
| How sentences are built from pieces | [docs/VOCABULARY.md](docs/VOCABULARY.md) |
| What to do next | [TODO.md](TODO.md) |
| Why each call was made | [DECISIONS.md](DECISIONS.md) |
| To get a machine working | [docs/SETUP.md](docs/SETUP.md) |

| Path | What it is |
|---|---|
| `slice/` | The pipeline from Gherkin through Lean to Rust |
| `census/` | How much real Rust translates; the translator patches |
| `p2/`, `trials/` | Proof-writing comparison; reading and authoring trials |
| `Rosette/`, `bench/`, `tools/` | Tooling for large proofs |
| `corpora/`, `out/` | Projects under study, and results |
| `docs/diagrams/` | The figures, as editable Vector180 sources |

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"
cd slice && ./run.sh      # report in slice/out/report.md
```

## How the work is done

- **Hypothesis, measurement, attack, fix.** Each idea is stated with a target, measured on real data, checked by an independent reviewer, corrected and rerun.
- **Report, don't gate.** The destination is fixed. Results say how good the approach is and what the trades are.
- **Negative results are kept.**
- **People decide judgement calls.** Language models stand in as proxies and are labelled as such.
- **Every judgement call is logged** with its reason and how to undo it.
