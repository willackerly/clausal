# lean-rosette

Tools and experiments toward one goal: **formally modelled software as the default**, with a chain of assurance from a plain-English description of behaviour down to the code that runs, where the trust placed in each link is stated, bounded and repeatable.

## The target, in one example

This is the end-to-end outcome the project is working toward. It does not run yet in this form; the pieces that exist today are listed under Results.

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

One command then reports:

```text
Rule: Internal fund transfers never change aggregate account value
  Reading   for every ledger and every transfer between two of its accounts,
            accepted or rejected, the sum of all balances afterwards equals
            the sum before
  Verdict   PROVED FOR ALL INPUTS
  Examples  2 of 2 pass on the compiled Rust
  Suite     with "a covered transfer between two accounts is accepted"
            (also proved), the suite rules out a ledger that rejects everything

  Rests on
    meaning      5 vocabulary pieces, all signed            human-asserted
                 (internal, fund transfer, aggregate,
                  account value, never changes)
    proof        theorem checked by Lean's kernel,          kernel-checked
                 standard axioms only
    translation  Lean model generated from ledger.rs        tool-trusted, cross-checked
                 by Aeneas                                  on the examples
    compilation  rustc                                      trusted
```

What makes this more than a test run:

- **The rule line is proved for every input**, not just the example rows. The rows are the same claim as ordinary cucumber tests.
- **The sentence needed no new definitions.** It was compiled from pieces defined and signed earlier, most of them shared across projects.
- **The reading is echoed back** so the author can confirm the tool understood the sentence the way they meant it.
- **Every link in the chain is listed with the kind of evidence behind it.** Nothing is claimed beyond that.
- **Rules are read as a suite.** One rule rarely pins behaviour alone; the report notes what the suite as a whole still allows, such as an implementation that does nothing.
- **A false rule fails usefully:** the report shows a concrete input that breaks it, confirmed on the compiled code.

**Status: research prototype, 2026-11-10.** Apache-2.0. Three background runs were still in progress when this was written; their rows below are marked.

## Objectives

### The end goal

A person writes a behavioural claim in ordinary language, such as "internal fund transfers can never change the aggregate account value". The toolchain turns it into a precise statement, proves that statement about the real implementation, and reports exactly what the answer rests on. Doing this should be cheap enough to be routine, not a research project per system.

No link in that chain is free of trust. The aim is that every link is named, has a known kind of evidence behind it, and can be re-checked by someone else:

| Link | From → to | Evidence today | State here |
|---|---|---|---|
| Meaning | English sentence → formal statement | Human sign-off on a small vocabulary; a second independent reading | Working on a toy; vocabulary is phrase-level, not yet compositional |
| Proof | Formal statement → Lean model of the code | Lean's kernel | Working |
| Translation | Lean model → Rust source | Trusted tool (Aeneas), cross-checked by running both | Working on a small Rust subset |
| Compilation | Rust source → machine code | Trusted compiler, tests | Not addressed |
| Execution | Machine code → hardware | Trusted | Not addressed |

### Three strands of work

1. **A composable vocabulary for behaviour.** Sentences should be assembled from previously defined pieces, each bound once to a Lean definition and signed off once: domain words (*account*, *balance*, *transfer*), modifiers (*internal*, *aggregate*) and logical frames (*never changes*, *always*, *only if*). A new sentence built from known pieces should compile to a Lean statement with no new human judgement beyond confirming the reading. How fine-grained the pieces should be is an open design question.
2. **Binding statements to code, starting with Rust.** Gherkin-style scenarios (Given / When / Then) become Lean theorems about a model generated from the Rust source, with a verdict per scenario: proved for all inputs, refuted with a counterexample, tested only, unbound, or vacuous. See `slice/`.
3. **Making large formal developments navigable.** Proofs and models at scale are only useful if people can find their way around them. This is the pure Lean and mathematics strand: finding structure, reuse and a readable interface in large proofs, including machine-generated ones. It serves mathematics and physics directly, and software verification indirectly, since verified code produces large proofs too. See `Rosette/` and `out/corpus/`.

A shared graph format (`docs/SCHEMA.md`) ties the strands together: statements, their implementations, and links labelled with the kind of evidence behind them.

### Worked example: one sentence, compiled from pieces

> Internal fund transfers can never result in a change in aggregate account value.

| Phrase | Kind of piece | Reading | Reused |
|---|---|---|---|
| fund transfer | Domain word | The ledger's transfer operation, bound to the Rust function | This system |
| account value | Domain word | The balance of one account | This system |
| internal | Modifier | Both parties are accounts of this ledger | Any operation |
| aggregate | Modifier | Sum the measure over all accounts | Any measure |
| can never result in a change in | Logical frame | For every starting state and every input, the measure afterwards equals the measure before | Every system |

Compiled reading: **internal(transfer) preserves aggregate(account value)**. That is one Lean statement, built with no new definitions, which the toolchain then proves about the model generated from the Rust.

- **Granularity:** split a phrase where a part would be reused with a different partner. "Aggregate" is its own piece because "aggregate fees" will follow; "account value" stays whole until something forces a split.
- **Shared frames:** logical frames and generic modifiers live in one library used across projects, defined and signed off once.
- **Fail-closed defaults:** "never" and "always" cover every input, including ones the operation rejects. A weaker reading has to be asked for.
- **Ambiguity is surfaced, not resolved silently:** when a phrase has two formal readings, the tool finds an input on which they differ and asks which was meant.
- **Two modes:** *suggest* turns a loose sentence into precise candidates for the author to accept; *interpret* leaves a fixed source such as a signed contract untouched and produces the formal sentences that state how it will be read.
- **Authors:** product-minded senior engineers first; product and compliance people on the roadmap.

This is the design, not yet the implementation: the slice binds whole phrases today. Full note: `docs/VOCABULARY.md`.

### Where it started

The project began from a brainstorm about "decompiling" AI-generated Lean proofs into libraries of small, meaningful pieces. Several versions of that idea have now been tested against real data. Most of the scoring ideas failed; the lifting tooling and the software-side slice work. The rest of this file is the map.

## Start here

| If you want | Read |
|---|---|
| What has been tried and what happened | `docs/EXPERIMENTS.md` |
| The plan: hypotheses, tests, order of work | `docs/PLAN.md` |
| What to do next (task list) | `TODO.md` |
| Why each call was made, and how to undo it | `DECISIONS.md` |
| To get a machine working | `docs/SETUP.md` |
| The shared graph format | `docs/SCHEMA.md` |
| How sentences are built from reusable pieces | `docs/VOCABULARY.md` |
| How this applies to TDFLite | `docs/TDFLITE.md` |
| Rules for agents working here | `AGENTS.md` |

## Results so far

| Question | Answer | Status | Detail |
|---|---|---|---|
| Does "proof hidden per unit of statement" find the lemma boundaries humans choose inside a proof? | No. First pick 7.7%; at chance for small helpers; worse than random at choosing where to stop | Final, reviewed | `out/FINDINGS.md` |
| Does the original "small goal state" idea find them? | No. Worse than random | Final, reviewed | `out/FINDINGS.md` |
| Do statements recur across proofs in human-written Mathlib? | Not usefully: 0.2% of proof size after removing trivia | Final, reviewed | `out/reuse/REUSE.md` |
| Can pieces of a proof be lifted into real lemmas soundly? | Yes. Kernel-checked, no failures on 1,274 theorems | Final, reviewed | `Rosette/Lift.lean` |
| Are the lifted statements readable? | Sometimes: good for Pell and Erdős–Ginzburg–Ziv, poor for a Sobolev inequality | One rater, three theorems | `out/demo/README.md` |
| Was the idea new? | Partly not. Single-proof extraction is published (Proof-Refactor); the ratio is published as a descriptive measure | Checked by web search | `out/prior_art.md` |
| Can English scenarios be bound to proofs about real Rust? | Yes on a 45-line wallet: 7 proved for all inputs, a false claim refuted with a counterexample | Final, reviewed | `slice/FINDINGS.md` |
| Does that survive loops and collections? | Yes, at a price: about 6 lines of hand-written Lean per line of Rust (1.6 for straight-line code); nothing about a loop is automatic. Viable with an agent writing proofs, not push-button | Final, reviewed; two loops only | `slice/FINDINGS.md` |
| Do dominators in the lemma graph predict what humans put in a blueprint? | Preliminary no: graph signal is mostly proof size; "has a docstring" does as well | Awaiting review | `out/corpus/validation/VALIDATION.md` |
| Does the machine-generated Navier–Stokes proof have a recoverable outline? | Preliminary partial: 13 statements cover 54% of the proof, but most are not readable on their own | Awaiting review | `out/corpus/outline/` |
| Is there more redundancy in machine proofs than in Mathlib? | In progress | Running | `out/corpus/reuse/` |
| Where do analysis proofs spend their bulk (casts, measurability, constants)? Do "packets" help? | In progress | Running | `out/corpus/friction/` |

The recurring lesson: sizes and graph positions are measurable but do not by themselves identify what a mathematician finds meaningful. In the machine corpus the content sits in definitions, so an outline has to present those, not lemma signatures.

## Layout

| Path | What it is |
|---|---|
| `Rosette/`, `Rosette.lean`, `lakefile.toml` | Root Lean 4 + Mathlib project: candidate enumeration, lifting, Mathlib benchmarks |
| `bench/` | Benchmark corpus and scoring scripts (Python and shell) |
| `out/` | Results: `FINDINGS.md`, per-experiment reports, raw data, reviewers' evidence |
| `out/corpus/` | Exports and analyses of the external corpora |
| `corpora/` | External Lean projects, each with its own pins: `ns` (OpenAI Navier–Stokes/Euler, machine-generated), `pfr`, `carleson` (human-written, with blueprints), plus exporters |
| `slice/` | Gherkin → Lean → Rust vertical slice; separate Lake project and Rust crates |
| `docs/` | Schema, experiment inventory, setup, TDFLite notes |
| `tdflite-ideas/` | The owner's TDFLite verification plan (input, not produced here) |

## Quick commands

```sh
export PATH="$HOME/.elan/bin:$HOME/.cargo/bin:$PATH"

# Root project (about 1 minute; also regenerates demo outputs)
lake build Rosette

# Try the lifter on any theorem: add to a scratch .lean file importing Rosette.Lift
#   #rosette_lift Pell.exists_of_not_isSquare (k := 5)

# Mathlib benchmarks
bench/run_bench.sh        # boundary recovery (H1)
bench/run_reuse.sh        # reuse (H2), about 20 minutes

# Vertical slice
cd slice && ./run.sh      # report in slice/out/report.md
```

`docs/SETUP.md` has toolchains, disk use and how to rebuild the corpora.

## How the work is done

- Each idea is stated as a hypothesis, measured on real Lean data, attacked by independent reviewers, then fixed and rerun. Negative results are kept.
- Data comes from Lean's own environment, not from text matching.
- Judgement calls and system installs go in `DECISIONS.md` with an undo step.
